#!/usr/bin/env python3
"""Extract an exact-time frame strip or enlarged hand/face crop using FFmpeg.

review_frames.py video.mp4 --out review/hands --times 1.2 1.4 1.6 --crop 600 300 400 400
No vision model or creative approval is implied by generating a contact sheet.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


def validate(times, duration, width, height, crop):
    if not times or len(times) > 60 or any(isinstance(t, bool) or not isinstance(t, (float, int))
                                         or not math.isfinite(t) or not 0 <= t < duration for t in times):
        raise ValueError("Choose 1-60 finite frame times within [0, duration)")
    if crop is not None:
        if len(crop) != 4 or any(type(n) is not int for n in crop):
            raise ValueError("Crop must be integer x y width height")
        x, y, w, h = crop
        if min(x, y) < 0 or min(w, h) < 1 or x + w > width or y + h > height:
            raise ValueError("Crop must fit inside the decoded video")


def extract(video, output, times, crop=None, size=480):
    video, output = Path(video).resolve(), Path(output).resolve()
    if not video.is_file() or type(size) is not int or not 64 <= size <= 1920:
        raise ValueError("Video must exist and review width must be 64-1920px")
    result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                             "stream=width,height:format=duration", "-of", "json", str(video)],
                            check=True, capture_output=True, text=True, timeout=60)
    info = json.loads(result.stdout)
    stream = info["streams"][0]
    duration = float(info["format"]["duration"])
    validate(times, duration, stream["width"], stream["height"], crop)
    if output.exists():
        raise ValueError("Review output already exists; use a fresh directory to preserve evidence")
    output.mkdir(parents=True)
    filters = [] if crop is None else ["crop=" + ":".join(map(str, crop))]
    filters += [f"scale={size}:-2"]
    frames = []
    for index, time in enumerate(times):
        name = f"frame-{index:03d}.jpg"
        # Seek after -i for accurate decoding rather than nearest keyframe.
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-ss", str(time), "-frames:v", "1",
                        "-vf", ",".join(filters), "-q:v", "2", str(output / name)], check=True, timeout=120)
        if not (output / name).is_file() or not (output / name).stat().st_size:
            raise ValueError(f"No decoded frame at {time}; inspect the source video")
        frames.append({"file": name, "requested_time_s": time})
    columns = min(4, len(times))
    rows = math.ceil(len(times) / columns)
    subprocess.run(["ffmpeg", "-v", "error", "-framerate", "1", "-i", str(output / "frame-%03d.jpg"),
                    "-vf", f"tile={columns}x{rows}:padding=4:margin=4", "-frames:v", "1", "-q:v", "2",
                    str(output / "strip.jpg")], check=True, timeout=120)
    with video.open("rb") as source:
        sha = hashlib.file_digest(source, "sha256").hexdigest()
    report = {"source": str(video), "source_sha256": sha, "duration": duration, "crop": crop,
              "frames": frames, "strip": "strip.jpg", "creative_approval": False}
    (output / "review.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--times", required=True, nargs="+", type=float)
    parser.add_argument("--crop", nargs=4, type=int, metavar=("X", "Y", "W", "H"))
    parser.add_argument("--width", type=int, default=480)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(extract(args.video, args.out, args.times, args.crop, args.width), indent=2))
        return 0
    except (ValueError, KeyError, IndexError, OSError, subprocess.SubprocessError) as exc:
        print(f"review_frames: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
