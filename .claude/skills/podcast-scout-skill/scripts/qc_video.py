
#!/usr/bin/env python3
"""
qc_video.py — Quality Control & Film Gate for Founder Notes Studio.

Checks:
1. Video existence, metadata, resolution, and frame rate.
2. Minimum video duration.
3. Audio stream, silence gaps, and timing consistency.
4. Film gate: motion, blank frames, and blue-purple dominance.
5. Contact sheet generation.

Fix 1: Fail closed on missing NumPy, FFmpeg decoding errors,
       incomplete frames, and insufficient decoded frames.
Fix 2: Stream decoded frames instead of loading the entire
       video into memory.
"""

import argparse
import json
import math
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


def mark_failure(qc_report, message):
    qc_report["status"] = "FAIL"
    qc_report["errors"].append(message)


def run_ffprobe(file_path):
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        file_path,
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        return json.loads(result.stdout)

    except (OSError, ValueError):
        return None


def generate_contact_sheet(
    video_path,
    output_sheet,
    duration,
    grid="4x6",
):
    cols, rows = map(int, grid.split("x"))
    total_tiles = cols * rows
    fps_val = max(total_tiles / max(duration, 1.0), 0.02)

    cmd = [
        "ffmpeg", "-y",
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
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Contact sheet generation failed: "
            + result.stderr[-500:]
        )

    if not os.path.isfile(output_sheet):
        raise RuntimeError(
            "Contact sheet output file was not created"
        )


def audit_audio_gaps_and_lufs(
    video_path,
    qc_report,
    max_silence_gap=1.2,
):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-af", f"silencedetect=noise=-35dB:d={max_silence_gap}",
        "-f", "null", "-",
    ]

    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except OSError as exc:
        mark_failure(
            qc_report,
            f"Audio inspection could not start: {exc}",
        )
        return

    if res.returncode != 0:
        mark_failure(
            qc_report,
            "Audio silence inspection failed during "
            "FFmpeg processing.",
        )
        return

    gaps = []
    pending_start = None

    for line in (res.stderr or "").splitlines():
        m_start = re.search(
            r"silence_start:\s*([0-9.]+)",
            line,
        )

        if m_start:
            pending_start = float(m_start.group(1))

        m_end = re.search(
            r"silence_end:\s*([0-9.]+)",
            line,
        )
        m_dur = re.search(
            r"silence_duration:\s*([0-9.]+)",
            line,
        )

        if m_end and m_dur:
            end_t = float(m_end.group(1))
            dur_t = float(m_dur.group(1))
            start_t = max(0.0, end_t - dur_t)
            gaps.append((start_t, end_t, dur_t))
            pending_start = None

    if pending_start is not None:
        info = run_ffprobe(video_path)

        try:
            duration = float(
                info["format"]["duration"]
            )
        except (TypeError, KeyError, ValueError):
            mark_failure(
                qc_report,
                "Cannot determine duration of "
                "unfinished audio silence.",
            )
            return

        if not (
            0 <= pending_start <= duration
            and duration < float("inf")
        ):
            mark_failure(
                qc_report,
                "Invalid trailing audio silence timing.",
            )
            return

        gap_duration = duration - pending_start

        if gap_duration >= max_silence_gap:
            gaps.append(
                (
                    pending_start,
                    duration,
                    gap_duration,
                )
            )

    if gaps:
        gap_str = ", ".join(
            f"{s:.2f}s-{e:.2f}s ({d:.2f}s)"
            for s, e, d in gaps[:8]
        )

        qc_report["warnings"].append(
            f"Audio silence gaps > {max_silence_gap}s "
            f"detected at: {gap_str}"
        )

        if any(d > 2.5 for _, _, d in gaps):
            mark_failure(
                qc_report,
                f"Dead audio air > 2.5s detected: {gap_str}",
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
    """
    Stream and analyze sampled frames.

    Memory usage remains approximately constant with
    video duration because frames are not accumulated.
    """

    if not HAS_NUMPY:
        mark_failure(
            qc_report,
            "CRITICAL: NumPy is missing. "
            "Mandatory visual inspection cannot run.",
        )
        return

    sample_fps = 10
    width = 160
    height = 90
    frame_bytes = width * height * 3

    cmd = [
        "ffmpeg",
        "-v", "error",
        "-i", video_path,
        "-vf",
        f"fps={sample_fps},scale={width}:{height}",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-",
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        mark_failure(
            qc_report,
            f"Unable to start FFmpeg visual inspection: {exc}",
        )
        return

    n_frames = 0
    motion_count = 0
    motion_total = 0
    blue_purple_count = 0

    previous_frame = None
    blank_start = None
    blank_runs = []

    incomplete_frame = False
    inspection_error = None

    try:
        while True:
            chunks = []
            remaining = frame_bytes

            # A pipe read can return fewer bytes than requested.
            # Continue until one complete frame is available.
            while remaining > 0:
                chunk = proc.stdout.read(remaining)

                if not chunk:
                    break

                chunks.append(chunk)
                remaining -= len(chunk)

            if not chunks:
                break

            if remaining != 0:
                incomplete_frame = True
                break

            raw_frame = b"".join(chunks)

            frame = np.frombuffer(
                raw_frame,
                dtype=np.uint8,
            ).reshape(
                height,
                width,
                3,
            )

            # Motion analysis
            if previous_frame is not None:
                delta = np.mean(
                    np.abs(
                        frame.astype(np.int16)
                        - previous_frame.astype(np.int16)
                    )
                ) / 255.0

                motion_total += 1

                if delta > 0.025:
                    motion_count += 1

            previous_frame = frame

            # Blank / solid-color frame detection
            spatial_std = float(np.std(frame))

            if spatial_std < 3.5:
                if blank_start is None:
                    blank_start = n_frames
            else:
                if blank_start is not None:
                    blank_runs.append(
                        (blank_start, n_frames)
                    )
                    blank_start = None

            # Blue-purple dominance detection
            pixels = frame.astype(np.float32)

            red = pixels[:, :, 0]
            green = pixels[:, :, 1]
            blue = pixels[:, :, 2]

            bp_pixels = (
                (blue > 70)
                & (blue > green * 1.25)
                & (red > green * 1.05)
                & ((red + blue) > 160)
            )

            if float(np.mean(bp_pixels)) > 0.45:
                blue_purple_count += 1

            n_frames += 1

    except (OSError, ValueError, MemoryError) as exc:
        inspection_error = str(exc)
        proc.kill()

    finally:
        if proc.stdout is not None:
            proc.stdout.close()

        return_code = proc.wait()

    if inspection_error is not None:
        mark_failure(
            qc_report,
            f"Video frame inspection failed: {inspection_error}",
        )
        return

    if return_code != 0:
        mark_failure(
            qc_report,
            "FFmpeg decoding failed with exit code "
            f"{return_code}",
        )
        return

    if incomplete_frame:
        mark_failure(
            qc_report,
            "Incomplete video frame detected during QC.",
        )
        return

    if n_frames < 5:
        mark_failure(
            qc_report,
            "Insufficient decoded frames for visual inspection.",
        )
        return

    if blank_start is not None:
        blank_runs.append(
            (blank_start, n_frames)
        )

    qc_report["checks"].append(
        f"Streamed {n_frames} sampled frames "
        f"at {sample_fps} fps"
    )

    # Motion quality gate
    fast_motion_ratio = (
        motion_count / motion_total
        if motion_total > 0
        else 0.0
    )

    qc_report["checks"].append(
        "Fast-motion frame ratio: "
        f"{fast_motion_ratio:.4f} "
        "(threshold >= 0.035)"
    )

    if fast_motion_ratio < 0.035:
        mark_failure(
            qc_report,
            "FILM GATE RED LIGHT (Anti-PPT): "
            f"Fast-motion frame ratio is "
            f"{fast_motion_ratio:.4f} (< 0.035). "
            "Video may resemble a static slideshow.",
        )

    elif fast_motion_ratio < 0.060:
        qc_report["warnings"].append(
            "FILM GATE YELLOW: "
            f"Fast-motion frame ratio is "
            f"{fast_motion_ratio:.4f} (< 0.060)."
        )

    # Blank frame quality gate
    # Exclude first 0.5s and last 1.0s.
    start_index = min(5, n_frames)
    end_index = max(
        start_index,
        n_frames - 10,
    )

    valid_blank_runs = []

    for start, end in blank_runs:
        clipped_start = max(
            start,
            start_index,
        )

        clipped_end = min(
            end,
            end_index,
        )

        if clipped_end - clipped_start >= 3:
            valid_blank_runs.append(
                (
                    clipped_start / sample_fps,
                    clipped_end / sample_fps,
                )
            )

    if valid_blank_runs:
        timecodes = ", ".join(
            f"{start:.2f}s-{end:.2f}s"
            for start, end in valid_blank_runs[:6]
        )

        mark_failure(
            qc_report,
            "FILM GATE RED LIGHT "
            "(Blank/Dead Frame Gap >= 0.3s): "
            f"Empty or solid frames detected at {timecodes}",
        )
    else:
        qc_report["checks"].append(
            "Zero mid-video blank/dead frame gaps >= 0.3s"
        )

    # Blue-purple palette quality gate
    bp_frame_ratio = blue_purple_count / n_frames

    qc_report["checks"].append(
        "Blue-purple frame ratio: "
        f"{bp_frame_ratio:.2%}"
    )

    if (
        bp_frame_ratio >= 0.30
        and not allow_blue_purple
    ):
        mark_failure(
            qc_report,
            "FILM GATE RED LIGHT (AI-Slop Palette): "
            f"{bp_frame_ratio:.1%} of frames have "
            "blue-purple dominance (>= 30% limit).",
        )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Quality Control Video for Founder Notes Studio"
        )
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

    # File existence
    if not os.path.isfile(args.video):
        mark_failure(
            qc_report,
            f"Video file not found: {args.video}",
        )
        write_report(args.json, qc_report)
        print(f"QC Status: {qc_report['status']}")
        sys.exit(1)

    # Metadata inspection
    info = run_ffprobe(args.video)

    if not info:
        mark_failure(
            qc_report,
            "ffprobe failed to read video metadata",
        )
        write_report(args.json, qc_report)
        print(f"QC Status: {qc_report['status']}")
        sys.exit(1)

    format_info = info.get("format", {})
    streams = info.get("streams", [])

    video_stream = next(
        (
            stream
            for stream in streams
            if stream.get("codec_type") == "video"
        ),
        None,
    )

    audio_stream = next(
        (
            stream
            for stream in streams
            if stream.get("codec_type") == "audio"
        ),
        None,
    )

    # Video stream validation
    if video_stream is None:
        mark_failure(
            qc_report,
            "No video stream found",
        )
    else:
      
        try:
            width = int(video_stream.get("width", 0))
            height = int(video_stream.get("height", 0))
        except (TypeError, ValueError, OverflowError):
            width = 0
            height = 0

        if width <= 0 or height <= 0:
            mark_failure(
                qc_report,
                "Invalid video resolution metadata.",
            )


        if args.format == "horizontal":
            target_width = 1920
            target_height = 1080
        else:
            target_width = 1080
            target_height = 1920

        if (width, height) == (
            target_width,
            target_height,
        ):
            qc_report["checks"].append(
                f"Resolution matches target: {width}x{height}"
            )
        else:
            mark_failure(
                qc_report,
                "Resolution mismatch: "
                f"got {width}x{height}, "
                f"expected {target_width}x{target_height}",
            )

        frame_rate = video_stream.get(
            "r_frame_rate",
            "30/1",
        )

        try:
            numerator, denominator = map(
                int,
                frame_rate.split("/"),
            )

            fps = (
                numerator / denominator
                if denominator != 0
                else 0.0
            )

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
                f"Could not parse frame rate: {frame_rate}"
            )

    # Audio stream validation
    if audio_stream is None:
        mark_failure(
            qc_report,
            "No audio stream found",
        )
    else:
        codec = audio_stream.get(
            "codec_name",
            "",
        )

        qc_report["checks"].append(
            f"Audio codec: {codec}"
        )

    # Duration validation
    try:
        duration = float(
            format_info.get("duration", 0.0)
        )
    except (TypeError, ValueError):
        duration = 0.0

    if not math.isfinite(duration) or duration <= 0:
        mark_failure(
            qc_report,
            "Invalid video duration metadata.",
        )
        duration = 0.0

    qc_report["checks"].append(
        f"Video duration: {duration:.2f}s "
        f"({duration / 60:.2f} min)"
    )

    min_required = (
        args.min_duration
        if args.format == "horizontal"
        else 30.0
    )

    if duration < min_required:
        mark_failure(
            qc_report,
            "DURATION GATE FAIL: "
            f"Video duration is {duration:.2f}s, "
            f"below the required {min_required:.0f}s.",
        )

    # Optional timing metadata
    if args.timings and os.path.isfile(args.timings):
        try:
            with open(
                args.timings,
                "r",
                encoding="utf-8",
            ) as file:
                timing_data = json.load(file)

            timing_duration = float(
                timing_data.get("total_duration", 0.0)
            )

            if abs(duration - timing_duration) > 1.0:
                qc_report["warnings"].append(
                    f"Video duration ({duration:.2f}s) "
                    "differs from timings.json "
                    f"({timing_duration:.2f}s)"
                )

        except (OSError, ValueError, TypeError) as exc:
            qc_report["warnings"].append(
                f"Failed to parse timings.json: {exc}"
            )

    # Audio inspection
    if audio_stream is not None:
        audit_audio_gaps_and_lufs(
            args.video,
            qc_report,
        )

    # Streaming visual inspection
    if video_stream is not None:
        run_film_gate(
            args.video,
            duration,
            qc_report,
            allow_blue_purple=args.allow_blue_purple,
        )

    # Contact sheet generation
    if video_stream is not None:
        try:
            os.makedirs(
                os.path.dirname(args.sheet) or ".",
                exist_ok=True,
            )

            generate_contact_sheet(
                args.video,
                args.sheet,
                duration,
            )

            qc_report["checks"].append(
                f"Contact sheet generated: {args.sheet}"
            )

        except (OSError, ValueError, RuntimeError) as exc:
            mark_failure(
                qc_report,
                f"Contact sheet generation failed: {exc}",
            )

    # Final status
    if (
        qc_report["status"] == "PASS"
        and qc_report["warnings"]
    ):
        qc_report["status"] = "WARN"

    write_report(args.json, qc_report)

    print(
        f"QC Status: {qc_report['status']}"
    )

    if qc_report["errors"]:
        print(
            "ERRORS:",
            qc_report["errors"],
        )
        sys.exit(1)

    if qc_report["warnings"]:
        print(
            "WARNINGS:",
            qc_report["warnings"],
        )


def write_report(output_path, qc_report):
    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            qc_report,
            file,
            indent=2,
        )


if __name__ == "__main__":
    main()
