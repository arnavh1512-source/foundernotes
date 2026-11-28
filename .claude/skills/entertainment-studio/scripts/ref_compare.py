#!/usr/bin/env python3
"""Put reference frames and our frames side by side at full size, at matched moments.

    python3 ref_compare.py <reference.mp4> <ours.mp4> <out.jpg> 0.1 1.3 22.5:22.0 ...

Each time is either one time for both videos, or REF:OURS when the moments sit at different times. Frames are scaled to
the same height (default 960 px) so details can be compared. Look at the sheet at full size: judging craft from
thumbnails is how the 2026-11-28 benchmark face came out far plainer than the reference.
"""
import argparse, subprocess, tempfile
from pathlib import Path

from PIL import Image, ImageDraw


def pairs(specs):
    out = []
    for s in specs:
        a, _, b = s.partition(":")
        out.append((float(a), float(b or a)))
    return out


def frame(video, t, path, h):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale=-2:{h}", str(path)], check=True)
    return Image.open(path).convert("RGB")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref"); ap.add_argument("ours"); ap.add_argument("out"); ap.add_argument("times", nargs="+")
    ap.add_argument("--height", type=int, default=960)
    a = ap.parse_args()
    rows = []
    with tempfile.TemporaryDirectory() as td:
        for i, (tr, to) in enumerate(pairs(a.times)):
            l, r = frame(a.ref, tr, Path(td) / f"r{i}.png", a.height), frame(a.ours, to, Path(td) / f"o{i}.png", a.height)
            row = Image.new("RGB", (l.width + r.width + 12, a.height), "white"); row.paste(l, (0, 0)); row.paste(r, (l.width + 12, 0))
            d = ImageDraw.Draw(row); d.rectangle([0, 0, 260, 34], fill="black"); d.text((8, 10), f"REFERENCE {tr:.2f}s", fill="white")
            d.rectangle([l.width + 12, 0, l.width + 272, 34], fill="black"); d.text((l.width + 20, 10), f"OURS {to:.2f}s", fill="white")
            rows.append(row)
    sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height + 12 for r in rows)), "white")
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height + 12
    sheet.save(a.out, quality=90)
    print(f"{len(rows)} pairs -> {a.out}")


if __name__ == "__main__":
    main()
