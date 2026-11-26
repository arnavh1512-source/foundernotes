#!/usr/bin/env python3
"""Replace one shot in a 30 fps FounderNotes preview while preserving its audio."""

import argparse
import json
import subprocess
from pathlib import Path


def video_stream(path):
    result = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=width,height,r_frame_rate,avg_frame_rate,nb_read_frames",
        "-of", "json", str(path),
    ])
    streams = json.loads(result)["streams"]
    if not streams:
        raise ValueError(f"No video stream in {path}")
    return streams[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path, help="30 fps preview with the approved soundtrack")
    parser.add_argument("replacement", type=Path, help="Downloaded shot, cued to its first usable frame")
    parser.add_argument("output", type=Path, help="New comparison MP4")
    parser.add_argument("--start-frame", type=int, required=True, help="Zero-based inclusive frame")
    parser.add_argument("--end-frame", type=int, required=True, help="Zero-based exclusive frame")
    args = parser.parse_args()

    try:
        baseline = video_stream(args.baseline)
        total = int(baseline["nb_read_frames"])
        if any(baseline[key] != "30/1" for key in ("r_frame_rate", "avg_frame_rate")):
            parser.error("Baseline must be 30 fps")
        if not 0 <= args.start_frame < args.end_frame <= total:
            parser.error(f"Shot interval must be inside the {total}-frame baseline")
        width, height = baseline["width"], baseline["height"]
        if width % 2 or height % 2:
            parser.error("Baseline dimensions must be even")
    except (ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.error(str(error))

    start, end = args.start_frame, args.end_frame
    length = end - start
    # Count after conversion to the same frame rate used by the replacement filter.
    result = subprocess.run([
        "ffmpeg", "-v", "error", "-i", str(args.replacement),
        "-map", "0:v:0", "-vf", "fps=30", "-frames:v", str(length),
        "-progress", "pipe:1", "-f", "null", "-",
    ], check=True, capture_output=True, text=True)
    frames = [int(line.split("=")[1]) for line in result.stdout.splitlines() if line.startswith("frame=")]
    if not frames or frames[-1] < length:
        parser.error(f"Replacement needs at least {length} frames at 30 fps")

    head = f"[0:v]trim=end_frame={start},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[head]"
    shot = (
        f"[1:v]fps=30,trim=end_frame={length},setpts=PTS-STARTPTS,"
        f"scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[shot]"
    )
    tail = f"[0:v]trim=start_frame={end},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[tail]"
    filters = [head] if start else []
    labels = ["[head]"] if start else []
    filters.append(shot)
    labels.append("[shot]")
    if end < total:
        filters.append(tail)
        labels.append("[tail]")
    filters.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0[picture]")

    subprocess.run([
        "ffmpeg", "-n", "-v", "error", "-filter_complex_threads", "1", "-i", str(args.baseline),
        "-i", str(args.replacement), "-filter_complex", ";".join(filters),
        "-map", "[picture]", "-map", "0:a?", "-c:a", "copy",
        "-c:v", "libx264", "-fps_mode", "cfr", "-r", "30", "-movflags", "+faststart",
        str(args.output),
    ], check=True)


if __name__ == "__main__":
    main()
