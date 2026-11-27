#!/usr/bin/env python3
"""Measured review of a built take: loop seam, sound sync against the cue sheet, and a phone safe-zone sheet.

    python3 ep_review.py <workspace> [--take T-reel]

Writes review/auto-review.json and review/safezones.jpg. These are measurements, not a creative verdict: a person still
has to watch and listen.
"""
import argparse, json, subprocess, sys, tempfile, wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

SHARP_KINDS = {"boom", "bass", "thunk", "splat", "snap", "plop", "ting", "pop", "ding", "boing", "squelch", "crunch", "spring", "beep", "buzz", "knock"}


def onsets(samples, sr, rise_db=9.0, floor_db=-40.0, gap=0.08):
    """Times (s) where the 10 ms RMS jumps rise_db above the quietest of the previous 50 ms."""
    hop = max(1, int(0.01 * sr))
    rms = np.array([np.sqrt(np.mean(samples[i:i + hop] ** 2)) + 1e-6 for i in range(0, len(samples) - hop, hop)])
    db = 20 * np.log10(rms)
    out = []
    for i in range(5, len(db)):
        if db[i] - db[i - 5:i].min() > rise_db and db[i] > floor_db and (not out or i * 0.01 - out[-1] > gap):
            out.append(round(i * 0.01, 2))
    return out


def match(expected, found, tol=0.05):
    """For each (id, t) the nearest onset and whether it lands within tol seconds."""
    rows = []
    for cid, t in expected:
        n = min(found, key=lambda o: abs(o - t)) if found else None
        rows.append({"cue": cid, "t": round(t, 3), "onset": n, "error_ms": None if n is None else round((n - t) * 1000),
                     "ok": n is not None and abs(n - t) <= tol})
    return rows


def seam(first, last, thresh=12):
    """Percent of pixels that differ between two greyscale frames (the loop's cut)."""
    a, b = (np.asarray(im.convert("L").resize((270, 480)), dtype=np.int16) for im in (first, last))
    return round(float((np.abs(a - b) > thresh).mean() * 100), 2)


def low_share(path, cutoff=150.0):
    """Percent of a sound's energy below cutoff Hz. Phone speakers reproduce little below ~150 Hz."""
    w = wave.open(str(path)); ch = w.getnchannels()
    b = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    if ch > 1:
        b = b.reshape(-1, ch).mean(axis=1)
    f = np.fft.rfftfreq(len(b), 1 / w.getframerate()); p = np.abs(np.fft.rfft(b)) ** 2
    return round(float(100 * p[f < cutoff].sum() / max(p.sum(), 1e-12)), 1)


def frame_at(video, t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, t):.3f}", "-i", str(video), "-frames:v", "1", str(out)], check=True)
    return Image.open(out).convert("RGB")


def review(ws, take_id=None):
    ws = Path(ws).resolve()
    m = json.loads((ws / "workspace.json").read_text())
    take = next(t for t in m["takes"] if t["id"] == (take_id or m.get("selected", {}).get("take") or m["takes"][0]["id"]))
    video, dur = ws / take["file"], take["duration"]
    start = {r["id"]: r["start"] for r in take["shots"]}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(td / "a.wav")], check=True)
        w = wave.open(str(td / "a.wav"))
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
        found = onsets(a, w.getframerate())
        sharp = [(c["id"], start[c["shot"]] + c["t"]) for c in m["audio_cues"] if c["kind"] in SHARP_KINDS]
        sync = match(sharp, found)
        first, last = frame_at(video, 0, td / "f.png"), frame_at(video, dur - 1 / 30 - 0.001, td / "l.png")
        loop = seam(first, last)
        # safe-zone sheet: the middle of every shot, with Instagram's caption band and button column shaded
        tiles = []
        for r in take["shots"]:
            im = frame_at(video, r["start"] + r["dur"] / 2, td / f"{r['id']}.png").resize((216, 384))
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            d.rectangle([0, int(384 * .80), 216, 384], fill=(255, 0, 90, 70)); d.rectangle([int(216 * .86), int(384 * .45), 216, int(384 * .80)], fill=(255, 0, 90, 70))
            im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); ImageDraw.Draw(im).text((6, 6), r["id"], fill=(0, 0, 0))
            tiles.append(im)
        sheet = Image.new("RGB", (216 * len(tiles), 384), "white")
        for i, im in enumerate(tiles):
            sheet.paste(im, (i * 216, 0))
        sheet.save(ws / "review/safezones.jpg", quality=88)
    sys.path.insert(0, str(Path(__file__).resolve().parent)); import ep_build
    phone = {}
    for c in m["audio_cues"]:
        f = ep_build.cue_file(ws, c)
        phone.setdefault(f.name, low_share(f))
    phone_flags = sorted(k for k, v in phone.items() if v > 85)
    report = {"take": take["id"], "phone_low_share_pct": phone, "phone_flags": phone_flags, "duration": dur, "loop": m.get("loop", False), "loop_seam_pct": loop,
              "loop_ok": (loop < 1.0) if m.get("loop") else None,
              "sync_ok": sum(r["ok"] for r in sync), "sync_total": len(sync), "sync": sync,
              "note": "measured, not watched: misses can be soft swells or cues that start inside a louder sound"}
    (ws / "review/auto-review.json").write_text(json.dumps(report, indent=1) + "\n")
    print(f"{take['id']}: {dur}s  loop seam {loop}%{' (ok)' if report['loop_ok'] else '' if report['loop_ok'] is None else ' (CHECK)'}"
          f"  sync {report['sync_ok']}/{report['sync_total']} within 50 ms  -> review/auto-review.json, review/safezones.jpg")
    for k in phone_flags:
        print(f"  phone: {k} has {phone[k]}% of its energy below 150 Hz: near-silent on phone speakers")
    for r in sync:
        if not r["ok"]:
            print(f"  check {r['cue']} at {r['t']}s: nearest onset {r['onset']} ({r['error_ms']} ms)")
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workspace"); ap.add_argument("--take")
    a = ap.parse_args()
    review(a.workspace, a.take)
