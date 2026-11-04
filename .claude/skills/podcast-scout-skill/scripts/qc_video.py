#!/usr/bin/env python3
"""Measure a rendered video against the studio's delivery gates. You cannot watch a video,
so this turns it into numbers and a contact sheet you can read.

    python3 qc_video.py final.mp4 [--format landscape|vertical] [--fps 30]
                        [--timings narration/timings.json] [--captions captions.srt]
                        [--sheet out/sheet.jpg --sheet-frames 16] [--max-freeze 2.5] [--json report.json]

Checks (FAIL = must fix, WARN = look at it):
  spec        resolution, fps, H.264 + yuv420p, AAC audio present
  loudness    integrated -14 LUFS +/-1.5, true peak <= -1 dBTP
  opening     first frame is not black (the hook must be visible at t=0)
  black       black stretches > 0.5 s
  freeze      picture frozen longer than --max-freeze seconds (dead holds)
  dead air    audio silence > 2.0 s
  sync        video duration covers narration (+ tail); narration not cut
  captions    monotonic, no overlap, <= 42 chars per line, <= 20 chars/second, 0.7-7 s per cue
Exit code 0 = no FAIL, 1 = at least one FAIL, 2 = usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

FORMATS = {"landscape": (1920, 1080), "vertical": (1080, 1920), "square": (1080, 1080)}


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path])
    if r.returncode:
        raise SystemExit(f"qc: cannot probe {path}: {r.stderr}")
    return json.loads(r.stdout)


def loudness(path):
    r = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        return None, None
    d = json.loads(m.group(0))
    return float(d["input_i"]), float(d["input_tp"])


def detect(path, vf=None, af=None):
    args = ["ffmpeg", "-hide_banner", "-nostats", "-i", path]
    args += (["-vf", vf, "-an"] if vf else ["-af", af, "-vn"]) + ["-f", "null", "-"]
    return sh(args).stderr


def spans(log, start_key, end_key):
    starts = [float(x) for x in re.findall(start_key + r"[:=]\s*([\d.]+)", log)]
    ends = [float(x) for x in re.findall(end_key + r"[:=]\s*([\d.]+)", log)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def parse_srt(text):
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", lines[1] if "-->" in lines[1] else lines[0])
        if not m:
            continue
        g = list(map(int, m.groups()))
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        body = lines[2:] if "-->" in lines[1] else lines[1:]
        cues.append((a, b, body))
    return cues


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--format", choices=FORMATS, default="landscape")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--timings")
    ap.add_argument("--captions")
    ap.add_argument("--sheet")
    ap.add_argument("--sheet-frames", type=int, default=16)
    ap.add_argument("--max-freeze", type=float, default=2.5)
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    if not Path(a.video).exists():
        print(f"qc: no such file {a.video}", file=sys.stderr)
        return 2

    res = []

    def add(level, check, msg):
        res.append({"level": level, "check": check, "msg": msg})

    info = probe(a.video)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    W, H = FORMATS[a.format]
    if not v:
        add("FAIL", "spec", "no video stream")
    else:
        num, den = map(int, v.get("avg_frame_rate", "0/1").split("/"))
        fps = num / den if den else 0
        if (v["width"], v["height"]) != (W, H):
            add("FAIL", "spec", f"resolution {v['width']}x{v['height']} != {W}x{H}")
        if abs(fps - a.fps) > 0.05:
            add("FAIL", "spec", f"fps {fps:.2f} != {a.fps}")
        if v.get("codec_name") != "h264" or v.get("pix_fmt") != "yuv420p":
            add("WARN", "spec", f"video {v.get('codec_name')}/{v.get('pix_fmt')} (YouTube-safe is h264/yuv420p)")
        add("OK", "spec", f"{v['width']}x{v['height']} @ {fps:.2f} fps, {dur:.2f}s")
    if not au:
        add("FAIL", "spec", "no audio stream (narration missing)")
    else:
        i, tp = loudness(a.video)
        if i is None:
            add("WARN", "loudness", "could not measure")
        else:
            lvl = "OK" if abs(i - -14) <= 1.5 and tp <= -0.9 else "FAIL"
            add(lvl, "loudness", f"integrated {i:.1f} LUFS, true peak {tp:.1f} dBTP (target -14 / <= -1)")
        sil = spans(detect(a.video, af="silencedetect=noise=-45dB:d=2.0"), "silence_start", "silence_end")
        for s, e in sil:
            if e is None:
                e = dur
            if s < 0.5 or e > dur - 1.5:
                continue  # lead-in / outro tail
            add("WARN", "dead air", f"silence {s:.1f}-{e:.1f}s ({e - s:.1f}s)")

    blk = spans(detect(a.video, vf="blackdetect=d=0.1:pic_th=0.98:pix_th=0.03"), "black_start", "black_end")
    for s, e in blk:
        e = dur if e is None else e
        if s <= 0.04:
            add("FAIL", "opening", f"video opens on black ({s:.2f}-{e:.2f}s): show the subject at t=0")
        elif e - s > 0.5:
            add("WARN", "black", f"black {s:.2f}-{e:.2f}s")
    frz = spans(detect(a.video, vf=f"freezedetect=n=0.002:d={a.max_freeze}"), "freeze_start", "freeze_end")
    for s, e in frz:
        e = dur if e is None else e
        add("WARN", "freeze", f"picture frozen {s:.1f}-{e:.1f}s ({e - s:.1f}s > {a.max_freeze}s): add secondary motion or cut")

    if a.timings:
        t = json.loads(Path(a.timings).read_text())
        nd = float(t.get("duration", 0))
        if dur + 0.05 < nd:
            add("FAIL", "sync", f"video {dur:.2f}s is shorter than narration {nd:.2f}s")
        elif dur - nd > 4:
            add("WARN", "sync", f"video runs {dur - nd:.1f}s past narration (silent tail?)")
        else:
            add("OK", "sync", f"narration {nd:.2f}s fits video {dur:.2f}s")
        wpm = t.get("wpm_speech")
        if wpm and not 120 <= wpm <= 175:
            add("WARN", "pace", f"speech rate {wpm} wpm (explainer comfort band 130-165)")
        if t.get("male_voice_policy") is False:
            add("WARN", "voice", "narration was rendered with --allow-non-male")

    if a.captions:
        cues = parse_srt(Path(a.captions).read_text(encoding="utf-8-sig"))
        if not cues:
            add("FAIL", "captions", "no cues parsed")
        prev_end = 0.0
        for n, (s, e, body) in enumerate(cues, 1):
            text = " ".join(body)
            d = e - s
            if s + 1e-3 < prev_end:
                add("FAIL", "captions", f"cue {n} overlaps previous")
            if any(len(l) > 42 for l in body):
                add("WARN", "captions", f"cue {n} line > 42 chars: {text[:50]}")
            if d < 0.7 or d > 7:
                add("WARN", "captions", f"cue {n} on screen {d:.2f}s (0.7-7s)")
            if d > 0 and len(text) / d > 20:
                add("WARN", "captions", f"cue {n} reads at {len(text) / d:.0f} chars/s (> 20)")
            prev_end = e
        if cues and cues[-1][1] > dur + 0.2:
            add("FAIL", "captions", "captions run past end of video")
        add("OK", "captions", f"{len(cues)} cues checked")

    if a.sheet:
        n = max(4, a.sheet_frames)
        cols = 4
        rows = (n + cols - 1) // cols
        step = max(dur / n, 0.04)
        Path(a.sheet).parent.mkdir(parents=True, exist_ok=True)
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-vf",
            f"fps=1/{step:.3f},scale=480:-2,drawtext=text='%{{pts\\:hms}}':x=8:y=8:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile={cols}x{rows}",
            "-frames:v", "1", a.sheet])
        add("OK" if Path(a.sheet).exists() else "WARN", "sheet", f"contact sheet {a.sheet} (open it and look)")

    fails = [r for r in res if r["level"] == "FAIL"]
    for r in res:
        print(f"{r['level']:4s}  {r['check']:9s} {r['msg']}")
    print(f"\n{'FAIL' if fails else 'PASS'}: {len(fails)} fail, {sum(r['level'] == 'WARN' for r in res)} warn")
    if a.json:
        Path(a.json).write_text(json.dumps({"video": a.video, "pass": not fails, "results": res}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
