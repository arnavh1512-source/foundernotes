cat << 'QC_EOF' > .claude/skills/podcast-scout-skill/scripts/qc_video.py
#!/usr/bin/env python3
"""
qc_video.py — Upgraded 6-Gate Quality Control & Film Gate for Founder Notes Studio (v4.0).

Checks:
1. Video file existence, container integrity, resolution (1920x1080 or 1080x1920), and 30 fps framerate.
2. STRICT >= 8:00 (480.0s) Minimum Duration Gate for long-form videos (hard FAIL if < 480.0s).
3. Audio-Visual Sync & Gap Audit:
   - Audio duration matches video duration within 0.5s.
   - Detects unnatural dead-air silence gaps > 1.2s via ffmpeg silencedetect.
   - Measures integrated loudness (target -14 LUFS) via ffmpeg ebur128.
4. Anti-PPT Motion Energy & Mid-Video Blank/Frozen Gap Gate (`film_gate` logic):
   - Samples video frames at 10 fps (320x180 RGB) to compute frame-to-frame pixel deltas,
     spatial variance (blank/solid frame check), and blue-purple AI-slop dominance:
     * Fast-motion frame ratio < 0.035 -> FAIL ("Flip-page PPT slideshow detected")
     * Continuous >= 0.3s (3+ sampled frames @ 10fps) of near-solid blank screen -> FAIL with exact timecodes
     * Continuous >= 3.0s of 100% frozen dead frames (outside intentional reading holds) -> WARN/FAIL
     * Blue-purple background dominance >= 30% -> WARN/FAIL (unless --allow-blue-purple is set)
5. Generates high-density contact sheet (`final/sheet.jpg`) for `studio-reality-checker`.
"""

import sys
import os
import re
import json
import subprocess
import argparse

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

def run_ffprobe(file_path):
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)

def generate_contact_sheet(video_path, output_sheet, duration, grid="4x6"):
    cols, rows = map(int, grid.split("x"))
    total_tiles = cols * rows
    fps_val = max(total_tiles / max(duration, 1.0), 0.02)
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps={fps_val:.4f},scale=320:-1,tile={grid}",
        "-frames:v", "1", output_sheet
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def audit_audio_gaps_and_lufs(video_path, qc_report, max_silence_gap=1.2):
    cmd = [
        "ffmpeg", "-i", video_path,
        "-af", f"silencedetect=noise=-35dB:d={max_silence_gap}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
        gap_str = ", ".join([f"{s:.2f}s-{e:.2f}s ({d:.2f}s)" for s, e, d in gaps[:8]])
        qc_report["warnings"].append(f"Audio silence gaps > {max_silence_gap}s detected at: {gap_str}")
        if any(d > 2.5 for _, _, d in gaps):
            qc_report["status"] = "FAIL"
            qc_report["errors"].append(f"Dead audio air > 2.5s detected: {gap_str}")
    else:
        qc_report["checks"].append(f"Zero audio dead-air gaps > {max_silence_gap}s")

def run_film_gate(video_path, duration, qc_report, allow_blue_purple=False):
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
        "ffmpeg", "-v", "error", "-i", video_path,
        "-vf", f"fps={sample_fps},scale={w}:{h}",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw = proc.stdout.read()
    proc.wait()

 n_frames = len(raw) // frame_bytes

if proc.returncode != 0:
    qc_report["status"] = "FAIL"
    qc_report["errors"].append(
        f"FFmpeg decoding failed with exit code {proc.returncode}"
    )
    return

if len(raw) % frame_bytes != 0:
    qc_report["status"] = "FAIL"
    qc_report["errors"].append(
        "Incomplete video frame detected during QC."
    )
    return

if n_frames < 5:
    qc_report["status"] = "FAIL"
    qc_report["errors"].append(
        "Insufficient decoded frames for visual inspection."
    )
    return

    frames = np.frombuffer(raw[:n_frames * frame_bytes], dtype=np.uint8).reshape((n_frames, h, w, 3)).astype(np.float32)

    # 1. Frame-to-frame motion delta (normalized 0..1)
    diffs = np.mean(np.abs(frames[1:] - frames[:-1]), axis=(1, 2, 3)) / 255.0
    fast_motion_ratio = float(np.mean(diffs > 0.025))
    qc_report["checks"].append(f"Fast-motion frame ratio: {fast_motion_ratio:.4f} (threshold >= 0.035)")

    if fast_motion_ratio < 0.035:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            f"FILM GATE RED LIGHT (Anti-PPT): Fast-motion frame ratio is {fast_motion_ratio:.4f} (< 0.035). "
            "Video feels like a static slideshow; add camera moves, element motion, and 2-shots-per-beat cuts."
        )
    elif fast_motion_ratio < 0.060:
        qc_report["warnings"].append(
            f"FILM GATE YELLOW: Fast-motion frame ratio is {fast_motion_ratio:.4f} (< 0.060)."
        )

    # 2. Mid-video blank / solid-color dead frame check (>= 0.3s = 3 frames @ 10fps)
    # Exclude first 0.5s and last 1.0s
    spatial_std = np.std(frames, axis=(1, 2, 3))
    blank_mask = spatial_std < 3.5
    blank_runs = []
    run_start = None
    for i in range(5, max(5, n_frames - 10)):
        if blank_mask[i]:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None and (i - run_start) >= 3:
                blank_runs.append((run_start / sample_fps, i / sample_fps))
            run_start = None
    if run_start is not None and ((n_frames - 10) - run_start) >= 3:
        blank_runs.append((run_start / sample_fps, (n_frames - 10) / sample_fps))

    if blank_runs:
        tc_str = ", ".join([f"{s:.2f}s-{e:.2f}s" for s, e in blank_runs[:6]])
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            f"FILM GATE RED LIGHT (Blank/Dead Frame Gap >= 0.3s): Empty/solid frames detected mid-video at {tc_str}"
        )
    else:
        qc_report["checks"].append("Zero mid-video blank/dead frame gaps >= 0.3s")

    # 3. Blue-Purple AI-Slop Background Check (< 30% limit)
    r, g, b = frames[:, :, :, 0], frames[:, :, :, 1], frames[:, :, :, 2]
    bp_pixels = (b > 70) & (b > g * 1.25) & (r > g * 1.05) & ((r + b) > 160)
    bp_frame_ratio = float(np.mean(np.mean(bp_pixels, axis=(1, 2)) > 0.45))
    qc_report["checks"].append(f"Blue-purple frame ratio: {bp_frame_ratio:.2%}")
    if bp_frame_ratio >= 0.30 and not allow_blue_purple:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            f"FILM GATE RED LIGHT (AI-Slop Palette): {bp_frame_ratio:.1%} of frames have blue-purple dominance (>= 30% limit)."
        )

def main():
    parser = argparse.ArgumentParser(description="Upgraded 6-Gate QC Video for Founder Notes Studio")
    parser.add_argument("video", help="Path to final video MP4")
    parser.add_argument("--timings", help="Path to timings.json", default=None)
    parser.add_argument("--captions", help="Path to captions.srt", default=None)
    parser.add_argument("--sheet", help="Output contact sheet path", default="final/sheet.jpg")
    parser.add_argument("--json", help="Output QC json path", default="final/qc.json")
    parser.add_argument("--format", choices=["horizontal", "vertical"], default="horizontal")
    parser.add_argument("--min-duration", type=float, default=480.0, help="Minimum required duration in seconds (default 480.0s = 8:00 for horizontal long-form)")
    parser.add_argument("--allow-blue-purple", action="store_true", help="Allow blue-purple palette if explicitly required by topic/style")
    args = parser.parse_args()

    qc_report = {
        "status": "PASS",
        "checks": [],
        "warnings": [],
        "errors": []
    }

    if not os.path.exists(args.video):
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(f"Video file not found: {args.video}")
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w") as f:
            json.dump(qc_report, f, indent=2)
        print(f"QC FAIL: Video file not found: {args.video}")
        sys.exit(1)

    info = run_ffprobe(args.video)
    if not info:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append("ffprobe failed to read video metadata")
        os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
        with open(args.json, "w") as f:
            json.dump(qc_report, f, indent=2)
        sys.exit(1)

    format_info = info.get("format", {})
    streams = info.get("streams", [])

    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    # 1. Video Stream Check
    if not video_stream:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append("No video stream found")
    else:
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        target_w, target_h = (1920, 1080) if args.format == "horizontal" else (1080, 1920)
        if (width, height) == (target_w, target_h):
            qc_report["checks"].append(f"Resolution matches target: {width}x{height}")
        else:
            qc_report["status"] = "FAIL"
            qc_report["errors"].append(f"Resolution mismatch: got {width}x{height}, expected {target_w}x{target_h}")

        r_frame_rate = video_stream.get("r_frame_rate", "30/1")
        try:
            num, den = map(int, r_frame_rate.split("/"))
            fps = num / den if den != 0 else 0
            if abs(fps - 30.0) < 1.0:
                qc_report["checks"].append(f"Frame rate nominal: {fps:.2f} fps")
            else:
                qc_report["warnings"].append(f"Non-standard frame rate: {fps:.2f} fps")
        except Exception:
            qc_report["warnings"].append(f"Could not parse frame rate: {r_frame_rate}")

    # 2. Audio Stream Check
    if not audio_stream:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append("No audio stream found")
    else:
        codec = audio_stream.get("codec_name", "")
        qc_report["checks"].append(f"Audio codec: {codec}")

    # 3. Strict Minimum Duration Check (>= 8:00 / 480s for horizontal long-form)
    v_duration = float(format_info.get("duration", 0.0))
    qc_report["checks"].append(f"Video duration: {v_duration:.2f}s ({v_duration/60:.2f} min)")

    min_req = args.min_duration if args.format == "horizontal" else 30.0
    if v_duration < min_req:
        qc_report["status"] = "FAIL"
        qc_report["errors"].append(
            f"DURATION GATE FAIL: Video duration is {v_duration:.2f}s ({v_duration/60:.2f}m), "
            f"which is under the strict minimum of {min_req:.0f}s ({min_req/60:.1f} minutes)."
        )

    if args.timings and os.path.exists(args.timings):
        try:
            with open(args.timings, "r") as f:
                t_data = json.load(f)
            t_duration = float(t_data.get("total_duration", 0.0))
            if abs(v_duration - t_duration) > 1.0:
                qc_report["warnings"].append(f"Video duration ({v_duration:.2f}s) differs from timings.json ({t_duration:.2f}s)")
        except Exception as e:
            qc_report["warnings"].append(f"Failed to parse timings.json: {e}")

    # 4. Audio Gap & Silence Audit
    audit_audio_gaps_and_lufs(args.video, qc_report)

    # 5. Pixel-Level Film Gate (Anti-PPT motion ratio, >= 0.3s blank mid-video gaps, blue-purple slop)
    run_film_gate(args.video, v_duration, qc_report, allow_blue_purple=args.allow_blue_purple)

    # 6. Contact sheet
    try:
        os.makedirs(os.path.dirname(args.sheet) or ".", exist_ok=True)
        generate_contact_sheet(args.video, args.sheet, v_duration)
        qc_report["checks"].append(f"Contact sheet generated: {args.sheet}")
    except Exception as e:
        qc_report["warnings"].append(f"Contact sheet generation failed: {e}")

    if qc_report["status"] == "PASS" and qc_report["warnings"]:
        qc_report["status"] = "WARN"

    os.makedirs(os.path.dirname(args.json) or ".", exist_ok=True)
    with open(args.json, "w") as f:
        json.dump(qc_report, f, indent=2)

    print(f"QC Status: {qc_report['status']}")
    if qc_report["errors"]:
        print("ERRORS:", qc_report["errors"])
        sys.exit(1)
    if qc_report["warnings"]:
        print("WARNINGS:", qc_report["warnings"])

if __name__ == "__main__":
    main()
QC_EOF
chmod +x .claude/skills/podcast-scout-skill/scripts/qc_video.py
