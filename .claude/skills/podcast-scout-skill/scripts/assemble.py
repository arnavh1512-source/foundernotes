#!/usr/bin/env python3
"""Assemble the final YouTube master: scene clips + male narration + optional music + captions.

    python3 assemble.py --scenes s01.mp4 s02.mp4 ... --narration narration.wav --out final.mp4
                        [--music bed.wav --music-db -22] [--captions captions.srt [--no-burn] [--sub-font F --sub-fonts-dir DIR]]
                        [--format landscape|vertical] [--fps 30] [--crossfade 0]
    python3 assemble.py --scenes-list scenes.txt ...   (one clip path per line)

What it does
- normalises every clip to the same size/fps/pixel format (letterboxes, never stretches)
- concatenates them (hard cuts, or short crossfades with --crossfade SECONDS)
- if the picture is shorter than the narration, holds the last frame; never cuts the voice
- mixes music under the voice with side-chain ducking (voice always on top)
- loudness-normalises to -14 LUFS integrated, -1 dBTP (YouTube playback target)
- burns captions into the picture by default (channel rule; --no-burn for a soft mov_text track); always keeps the .srt sidecar
- H.264 High, yuv420p, +faststart, AAC 48 kHz 256 kb/s

Clips may be silent; any audio inside clips is dropped unless --keep-clip-audio is given.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FORMATS = {"landscape": (1920, 1080), "vertical": (1080, 1920), "square": (1080, 1080)}


def die(msg):
    print(f"assemble: {msg}", file=sys.stderr)
    sys.exit(2)


def ff(args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def duration(path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


def has_audio(path) -> bool:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return bool(out.strip())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scenes", nargs="*", default=[])
    ap.add_argument("--scenes-list")
    ap.add_argument("--narration", required=True)
    ap.add_argument("--music")
    ap.add_argument("--music-db", type=float, default=-22.0, help="music bed level before ducking (dB)")
    ap.add_argument("--captions")
    ap.add_argument("--burn", dest="burn", action="store_true", default=True,
                    help="burn captions into the picture (DEFAULT: channel rule, subtitles on every video)")
    ap.add_argument("--fill", choices=["black", "blur"], default="black",
                    help="how clips of another aspect ratio fill the frame: black bars or a blurred copy")
    ap.add_argument("--no-burn", dest="burn", action="store_false", help="soft captions only (mov_text track)")
    ap.add_argument("--sub-font", default="DejaVu Sans", help="font family for burned subtitles")
    ap.add_argument("--sub-fonts-dir", default=None, help="folder with the subtitle font files (e.g. film/fonts)")
    ap.add_argument("--sub-karaoke", action="store_true",
                    help="captions are a karaoke .ass from karaoke_ass.py: words turn gold as they are spoken")
    ap.add_argument("--sub-size", type=int, default=13, help="subtitle size in libass units (13 ≈ 49 px at 1080p)")
    ap.add_argument("--format", choices=FORMATS, default="landscape")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crossfade", type=float, default=0.0)
    ap.add_argument("--keep-clip-audio", action="store_true")
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.5, help="true-peak ceiling before AAC (AAC adds ~0.3-0.6 dB)")
    ap.add_argument("--grain", type=float, default=0.0, help="film grain strength added at encode (0 = none). WARNING: moving grain is random per frame and "
                         "compresses very badly (a 5-min 1080p film grew past 1.4 GB at strength 5). Use 1-2 at most, "
                         "or leave grain to YouTube's own compression")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)

    if a.fps <= 0 or a.fps > 120:
        die("--fps must be between 1 and 120")
    if not math.isfinite(a.crossfade) or a.crossfade < 0:
        die("--crossfade must be a finite, non-negative number")
    for name in ("music_db", "lufs", "tp", "grain"):
        if not math.isfinite(getattr(a, name)):
            die(f"--{name.replace('_', '-')} must be finite")
    if a.grain < 0:
        die("--grain must be non-negative")
    if a.sub_size <= 0:
        die("--sub-size must be positive")
    for name in ("narration", "music", "captions"):
        value = getattr(a, name)
        if value and not Path(value).is_file():
            die(f"missing {name} file: {value}")

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            die(f"{tool} not found")
    scenes = list(a.scenes)
    if a.scenes_list:
        scenes += [l.strip() for l in Path(a.scenes_list).read_text().splitlines() if l.strip() and not l.startswith("#")]
    if not scenes:
        die("no scene clips given")
    for s in scenes:
        if not Path(s).exists():
            die(f"missing clip {s}")
    W, H = FORMATS[a.format]
    narr_d = duration(a.narration)
    if not math.isfinite(narr_d) or narr_d <= 0:
        die("narration must have a finite, positive duration")
    if a.crossfade > 0 and len(scenes) > 1:
        for scene in scenes:
            scene_duration = duration(scene)
            if not math.isfinite(scene_duration) or scene_duration <= a.crossfade:
                die(f"crossfade must be shorter than every scene: {scene}")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        norm = []
        for i, s in enumerate(scenes):
            n = td / f"n{i:03d}.mp4"
            if a.fill == "blur":   # mismatched aspect: blurred, darkened copy of the clip behind it (no black bars)
                vf = (f"split[bgs][fgs];[bgs]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                      f"boxblur=26:2,eq=brightness=-0.06[bg];[fgs]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                      f"[bg][fg]overlay=(W-w)/2:(H-h)/2,fps={a.fps},format=yuv420p,setsar=1")
            else:
                vf = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,"
                      f"fps={a.fps},format=yuv420p,setsar=1")
            args = ["-i", s, "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "16"]
            if a.keep_clip_audio:
                if has_audio(s):
                    args += ["-map", "0:v:0", "-map", "0:a:0", "-c:a", "aac", "-ar", "48000", "-ac", "2"]
                else:   # every clip needs an audio track or concat drops audio for the whole film
                    args = ["-i", s, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", vf, "-c:v", "libx264",
                            "-preset", "medium", "-crf", "16", "-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-shortest"]
            else:
                args += ["-an"]
            ff(args + [str(n)])
            norm.append(n)

        picture = td / "picture.mp4"
        if a.crossfade > 0 and len(norm) > 1:
            inputs, chain, offset, last = [], [], 0.0, "[0:v]"
            for n in norm:
                inputs += ["-i", str(n)]
            alast = "[0:a]"
            for i in range(1, len(norm)):
                offset += duration(norm[i - 1]) - a.crossfade
                tag = f"[x{i}]"
                chain.append(f"{last}[{i}:v]xfade=transition=fade:duration={a.crossfade}:offset={offset:.3f}{tag}")
                last = tag
                if a.keep_clip_audio:   # carry clip audio through the same transitions
                    chain.append(f"{alast}[{i}:a]acrossfade=d={a.crossfade}:c1=tri:c2=tri[ax{i}]")
                    alast = f"[ax{i}]"
            amap = ["-map", alast, "-c:a", "aac", "-ar", "48000"] if a.keep_clip_audio else []
            ff(inputs + ["-filter_complex", ";".join(chain), "-map", last, *amap, "-c:v", "libx264", "-crf", "16",
                         "-pix_fmt", "yuv420p", str(picture)])
        else:
            lst = td / "list.txt"
            lst.write_text("".join(f"file '{n.as_posix()}'\n" for n in norm))
            ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(picture)])

        pic_d = duration(picture)
        if pic_d + 0.05 < narr_d:
            held = td / "held.mp4"
            ff(["-i", str(picture), "-vf", f"tpad=stop_mode=clone:stop_duration={narr_d - pic_d + 0.1:.3f}",
                "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(held)])
            picture = held
            print(f"assemble: picture was {narr_d - pic_d:.2f}s shorter than narration; held last frame "
                  f"(fix the edit so no hold is needed)", file=sys.stderr)
        final_d = max(duration(picture), narr_d)

        # ---- audio mix
        inputs = ["-i", str(picture), "-i", a.narration]
        # TTS has a high peak-to-average ratio: compress the voice before balancing it against music
        voice_chain = ("[1:a]aresample=48000,aformat=channel_layouts=stereo,"
                       "acompressor=threshold=0.1:ratio=3:attack=5:release=80:makeup=2,apad[voice0]")
        if a.keep_clip_audio and has_audio(picture):    # clip audio (dialogue, live sound) sits under the narration
            voice_chain += (";[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=-6dB,apad[clip];"
                            "[voice0][clip]amix=inputs=2:duration=first:normalize=0[voice]")
        else:
            voice_chain += ";[voice0]anull[voice]"
        if a.music:
            inputs += ["-stream_loop", "-1", "-i", a.music]
            fil = (f"{voice_chain};[voice]asplit=2[v1][vkey];"
                   f"[2:a]aresample=48000,aformat=channel_layouts=stereo,volume={a.music_db}dB[bed];"
                   f"[bed][vkey]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[ducked];"
                   f"[v1][ducked]amix=inputs=2:duration=first:normalize=0,"
                   f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11[aout]")
        else:
            fil = f"{voice_chain};[voice]loudnorm=I={a.lufs}:TP={a.tp}:LRA=11[aout]"

        vmap = "0:v"
        if a.grain > 0:
            fil += f";[0:v]noise=alls={a.grain:g}:allf=t[vg]"
            vmap = "[vg]"
        if a.captions and a.burn:
            # cream text on a translucent ink box, bottom centre (ASS colours are &HAABBGGRR)
            colours = ("PrimaryColour=&H0047B8E8,SecondaryColour=&H00D2E8F3," if a.sub_karaoke
                       else "PrimaryColour=&H00D2E8F3,")
            style = (f"FontName={a.sub_font},Fontsize={a.sub_size},Bold=1,{colours}"
                     "OutlineColour=&H5022180E,BackColour=&H5022180E,BorderStyle=3,Outline=6,Shadow=0,"
                     "MarginV=22,MarginL=40,MarginR=40,Alignment=2")
            if a.sub_karaoke:                       # per-word boxes overlap: a near-opaque box hides the seams
                style = style.replace("OutlineColour=&H5022180E,BackColour=&H5022180E", "OutlineColour=&H1022180E,BackColour=&H1022180E")
            sub = Path(a.captions).resolve().as_posix().replace(":", r"\:")
            src = "[vg]" if vmap == "[vg]" else "[0:v]"
            fdir = ""
            if a.sub_fonts_dir:
                fdir = ":fontsdir='" + Path(a.sub_fonts_dir).resolve().as_posix().replace(":", r"\:") + "'"
            fil += f";{src}subtitles='{sub}'{fdir}:force_style='{style}'[vout]"
            vmap = "[vout]"

        args = inputs[:]
        cap_in = None
        if a.captions and not a.burn:
            args += ["-i", a.captions]
            cap_in = len([x for x in inputs if x == "-i"])
        args += ["-filter_complex", fil, "-map", vmap, "-map", "[aout]"]
        if cap_in is not None:
            args += ["-map", f"{cap_in}:s", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng"]
        args += ["-c:v", "libx264" if vmap != "0:v" else "copy"]
        if vmap != "0:v":
            args += ["-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high"]
        args += ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{final_d:.3f}",
                 "-movflags", "+faststart", str(out)]
        ff(args)

    if a.captions:
        side = out.with_suffix(".srt")
        if Path(a.captions).resolve() != side.resolve():
            shutil.copyfile(a.captions, side)
    print(json.dumps({"out": str(out), "duration": round(duration(out), 3), "narration": round(narr_d, 3),
                      "format": f"{W}x{H}@{a.fps}", "music": bool(a.music), "captions": bool(a.captions),
                      "burned": bool(a.burn)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
