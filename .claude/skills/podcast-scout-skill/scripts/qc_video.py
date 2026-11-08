
#!/usr/bin/env python3
"""
qc_video.py — Quality Control & Film Gate for Founder Notes Studio.

Checks:
1. Video existence, metadata, resolution, and frame rate.
2. Minimum video duration.
3. Audio stream, silence gaps, and timing consistency.
4. Film gate: motion, blank frames, and blue-purple dominance.
5. Contact sheet generation.
"""

import argparse
import json
import os
import re
import subprocess
import sys

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False


def run_ffprobe(file_path):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path,
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def generate_contact_sheet(video_path, output_sheet, duration, grid="4x6"):
    cols, rows = map(int, grid.split("x"))
    total_tiles = cols * rows
    fps_val = max(total_tiles / max(duration, 1.0), 0.02)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"fps={fps_val:.4f},scale=320:-1,tile={grid}",
        "-frames:v", "1",
        output_sheet,
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Contact sheet generation failed: {result.stderr[-500:]}"
        )

    if not os.path.isfile(output_sheet):
        raise RuntimeError("Contact sheet output file was not created")


def audit_audio_gaps_and_lufs(
    video_path,
    qc_report,
    max_silence_gap=1.2,
):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-af", f"silencedetect=noise=-35dB:d={max_silence_gap}",
        "-f", "null",
        "-",
    ]

    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if res.returncode != 0:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "Audio silence inspection failed during FFmpeg processing."
        )
        return

    stderr = res.stderr or ""
    gaps = []

    for line in stderr.splitlines():
        if "silence_end:" in line and "silence_duration:" in line:
            m_end = re.search(r"silence_end:\s*([0-9.]+)", line)
            m_dur = re.search(r"silence_duration:\s*([0-9.]+)", line)

            if m_end and m_dur:
                end_t = float(m_end.group(1))
                dur_t = float(m_dur.group(1))
                start_t = max(0.0, end_t - dur_t)
                gaps.append((start_t, end_t, dur_t))

    if gaps:
        gap_str = ", ".join(
            f"{s:.2f}s-{e:.2f}s ({d:.2f}s)"
            for s, e, d in gaps[:8]
        )

        qc_report["warnings"].append(
            f"Audio silence gaps > {max_silence_gap}s detected at: {gap_str}"
        )

        if any(d > 2.5 for _, _, d in gaps):
            qc_report["status"] = "FAIL"
            qc_report["errors"].append(
                f"Dead audio air > 2.5s detected: {gap_str}"
            )
    else:
        qc_report["checks"].append(
            f"Zero audio dead-air gaps > {max_silence_gap}s"
        )


def run_film_gate(
    video_path,
    duration,
    qc_report,
    allow_blue_purple=False,
):
    # Mandatory NumPy dependency
    if not HAS_NUMPY:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "CRITICAL: NumPy is missing. "
            "Mandatory visual inspection cannot run."
        )
        return

    sample_fps = 10
    w, h = 160, 90
    frame_bytes = w * h * 3

    cmd = [
        "ffmpeg",
        "-v", "error",
        "-i", video_path,
        "-vf", f"fps={sample_fps},scale={w}:{h}",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-",
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        raw, stderr = proc.communicate()

    except OSError as exc:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            f"Unable to start FFmpeg visual inspection: {exc}"
        )
        return

    # Mandatory FFmpeg decoding check
    if proc.returncode != 0:
        qc_report["status"] = "FAIL"
        detail = stderr.decode("utf-8", errors="replace")[-500:]
        qc_report["errors"].append(
            f"FFmpeg decoding failed with exit code "
            f"{proc.returncode}: {detail}"
        )
        return

    # Detect incomplete raw frames
    if len(raw) % frame_bytes != 0:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "Incomplete video frame detected during QC."
        )
        return

    n_frames = len(raw) // frame_bytes

    # Mandatory minimum decoded frames
    if n_frames < 5:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "Insufficient decoded frames for visual inspection."
        )
        return

    frames = np.frombuffer(
        raw,
        dtype=np.uint8,
    ).reshape(
        (n_frames, h, w, 3)
    ).astype(np.float32)

    # 1. Frame-to-frame motion delta
    diffs = np.mean(
        np.abs(frames[1:] - frames[:-1]),
        axis=(1, 2, 3),
    ) / 255.0

    fast_motion_ratio = float(np.mean(diffs > 0.025))

    qc_report["checks"].append(
        f"Fast-motion frame ratio: {fast_motion_ratio:.4f} "
        "(threshold >= 0.035)"
    )

    if fast_motion_ratio < 0.035:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "FILM GATE RED LIGHT (Anti-PPT): "
            f"Fast-motion frame ratio is {fast_motion_ratio:.4f} "
            "(< 0.035). Video may resemble a static slideshow."
        )

    elif fast_motion_ratio < 0.060:
        qc_report["warnings"].append(
            "FILM GATE YELLOW: "
            f"Fast-motion frame ratio is {fast_motion_ratio:.4f} "
            "(< 0.060)."
        )

    # 2. Mid-video blank / solid-color frames
    spatial_std = np.std(
        frames,
        axis=(1, 2, 3),
    )

    blank_mask = spatial_std < 3.5
    blank_runs = []
    run_start = None

    start_index = min(5, n_frames)
    end_index = max(start_index, n_frames - 10)

    for i in range(start_index, end_index):
        if blank_mask[i]:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None:
                if i - run_start >= 3:
                    blank_runs.append(
                        (run_start / sample_fps, i / sample_fps)
                    )
                run_start = None

    if run_start is not None:
        if end_index - run_start >= 3:
            blank_runs.append(
                (
                    run_start / sample_fps,
                    end_index / sample_fps,
                )
            )

    if blank_runs:
        tc_str = ", ".join(
            f"{s:.2f}s-{e:.2f}s"
            for s, e in blank_runs[:6]
        )

        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "FILM GATE RED LIGHT "
            "(Blank/Dead Frame Gap >= 0.3s): "
            f"Empty or solid frames detected at {tc_str}"
        )
    else:
        qc_report["checks"].append(
            "Zero mid-video blank/dead frame gaps >= 0.3s"
        )

    # 3. Blue-purple background dominance
    r = frames[:, :, :, 0]
    g = frames[:, :, :, 1]
    b = frames[:, :, :, 2]

    bp_pixels = (
        (b > 70)
        & (b > g * 1.25)
        & (r > g * 1.05)
        & ((r + b) > 160)
    )

    bp_frame_ratio = float(
        np.mean(
            np.mean(bp_pixels, axis=(1, 2)) > 0.45
        )
    )

    qc_report["checks"].append(
        f"Blue-purple frame ratio: {bp_frame_ratio:.2%}"
    )

    if bp_frame_ratio >= 0.30 and not allow_blue_purple:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "FILM GATE RED LIGHT (AI-Slop Palette): "
            f"{bp_frame_ratio:.1%} of frames have "
            "blue-purple dominance (>= 30% limit)."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Quality Control Video for Founder Notes Studio"
    )

    parser.add_argument(
        "video",
        help="Path to final video MP4",
    )

    parser.add_argument(
        "--timings",
        default=None,
        help="Path to timings.json",
    )

    parser.add_argument(
        "--captions",
        default=None,
        help="Path to captions.srt",
    )

    parser.add_argument(
        "--sheet",
        default="final/sheet.jpg",
        help="Output contact sheet path",
    )

    parser.add_argument(
        "--json",
        default="final/qc.json",
        help="Output QC JSON path",
    )

    parser.add_argument(
        "--format",
        choices=["horizontal", "vertical"],
        default="horizontal",
    )

    parser.add_argument(
        "--min-duration",
        type=float,
        default=480.0,
        help="Minimum duration in seconds",
    )

    parser.add_argument(
        "--allow-blue-purple",
        action="store_true",
        help="Allow blue-purple palette when intentionally required",
    )

    args = parser.parse_args()

    qc_report = {
        "status": "PASS",
        "checks": [],
        "warnings": [],
        "errors": [],
    }

    if not os.path.exists(args.video):
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            f"Video file not found: {args.video}"
        )

        os.makedirs(
            os.path.dirname(args.json) or ".",
            exist_ok=True,
        )

        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(qc_report, f, indent=2)

        print(f"QC FAIL: Video file not found: {args.video}")
        sys.exit(1)

    info = run_ffprobe(args.video)

    if not info:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "ffprobe failed to read video metadata"
        )

        os.makedirs(
            os.path.dirname(args.json) or ".",
            exist_ok=True,
        )

        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(qc_report, f, indent=2)

        sys.exit(1)

    format_info = info.get("format", {})
    streams = info.get("streams", [])

    video_stream = next(
        (
            s for s in streams
            if s.get("codec_type") == "video"
        ),
        None,
    )

    audio_stream = next(
        (
            s for s in streams
            if s.get("codec_type") == "audio"
        ),
        None,
    )

    # 1. Video stream validation
    if not video_stream:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "No video stream found"
        )
    else:
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))

        if args.format == "horizontal":
            target_w, target_h = 1920, 1080
        else:
            target_w, target_h = 1080, 1920

        if (width, height) == (target_w, target_h):
            qc_report["checks"].append(
                f"Resolution matches target: {width}x{height}"
            )
        else:
            qc_report["status"] = "FAIL"
            qc_report["errors"].append(
                f"Resolution mismatch: got {width}x{height}, "
                f"expected {target_w}x{target_h}"
            )

        r_frame_rate = video_stream.get(
            "r_frame_rate",
            "30/1",
        )

        try:
            num, den = map(
                int,
                r_frame_rate.split("/"),
            )

            fps = num / den if den != 0 else 0

            if abs(fps - 30.0) < 1.0:
                qc_report["checks"].append(
                    f"Frame rate nominal: {fps:.2f} fps"
                )
            else:
                qc_report["warnings"].append(
                    f"Non-standard frame rate: {fps:.2f} fps"
                )

        except (ValueError, ZeroDivisionError):
            qc_report["warnings"].append(
                f"Could not parse frame rate: {r_frame_rate}"
            )

    # 2. Audio stream validation
    if not audio_stream:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "No audio stream found"
        )
    else:
        codec = audio_stream.get(
            "codec_name",
            "",
        )

        qc_report["checks"].append(
            f"Audio codec: {codec}"
        )

    # 3. Minimum duration validation
    try:
        v_duration = float(
            format_info.get("duration", 0.0)
        )
    except (ValueError, TypeError):
        v_duration = 0.0

    qc_report["checks"].append(
        f"Video duration: {v_duration:.2f}s "
        f"({v_duration / 60:.2f} min)"
    )

    if args.format == "horizontal":
        min_req = args.min_duration
    else:
        min_req = 30.0

    if v_duration < min_req:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            "DURATION GATE FAIL: "
            f"Video duration is {v_duration:.2f}s, "
            f"below the required {min_req:.0f}s."
        )

    # 4. Optional timing metadata
    if args.timings and os.path.exists(args.timings):
        try:
            with open(
                args.timings,
                "r",
                encoding="utf-8",
            ) as f:
                t_data = json.load(f)

            t_duration = float(
                t_data.get("total_duration", 0.0)
            )

            if abs(v_duration - t_duration) > 1.0:
                qc_report["warnings"].append(
                    f"Video duration ({v_duration:.2f}s) "
                    f"differs from timings.json ({t_duration:.2f}s)"
                )

        except (OSError, ValueError, TypeError) as exc:
            qc_report["warnings"].append(
                f"Failed to parse timings.json: {exc}"
            )

    # 5. Audio gap inspection
    if audio_stream:
        audit_audio_gaps_and_lufs(
            args.video,
            qc_report,
        )

    # 6. Pixel-level visual inspection
    if video_stream:
        run_film_gate(
            args.video,
            v_duration,
            qc_report,
            allow_blue_purple=args.allow_blue_purple,
        )

    # 7. Contact sheet generation
    if video_stream:
        try:
            os.makedirs(
                os.path.dirname(args.sheet) or ".",
                exist_ok=True,
            )

            generate_contact_sheet(
                args.video,
                args.sheet,
                v_duration,
            )

            qc_report["checks"].append(
                f"Contact sheet generated: {args.sheet}"
            )

        except (OSError, ValueError, RuntimeError) as exc:
            qc_report["warnings"].append(
                f"Contact sheet generation failed: {exc}"
            )

    if qc_report["status"] == "PASS" and qc_report["warnings"]:
        qc_report["status"] = "WARN"

    os.makedirs(
        os.path.dirname(args.json) or ".",
        exist_ok=True,
    )

    with open(
        args.json,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            qc_report,
            f,
            indent=2,
        )

    print(f"QC Status: {qc_report['status']}")

    if qc_report["errors"]:
        print("ERRORS:", qc_report["errors"])
        sys.exit(1)

    if qc_report["warnings"]:
        print("WARNINGS:", qc_report["warnings"])


if __name__ == "__main__":
    main()
