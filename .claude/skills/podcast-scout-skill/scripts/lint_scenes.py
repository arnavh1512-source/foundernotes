#!/usr/bin/env python3
"""FounderNotes storyboard and scene-manifest *static* preflight.

This does not prove runtime determinism, frame continuity or subtitle safety.
Those require rendered frames and qc_video.py. Use --require-clips for a
post-render check of real media and the measured narration duration.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shlex
import subprocess
import sys
from pathlib import Path

MIN_TOTAL_DURATION_SEC = 480.0
MAX_BEAT_DURATION_SEC = 8.0
MAX_LABEL_WORDS = 7
SPAN_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(?:-|–|—|to)\s*(\d+(?:\.\d+)?)\s*$", re.I)


def _number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError, OverflowError):
        return None


def _cell_index(names, *candidates):
    for key in candidates:
        if key in names:
            return names.index(key)
    return None


def lint_storyboard(storyboard_path, errors, warnings):
    path = Path(storyboard_path)
    if not path.is_file():
        errors.append(f"Missing storyboard: {path}")
        return
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = line.strip()
        if value.startswith("|") and value.endswith("|"):
            cells = [c.strip() for c in value.strip("|").split("|")]
            if cells and not all(re.fullmatch(r"[-: ]+", c) for c in cells):
                rows.append((number, cells))
    if len(rows) < 2:
        errors.append("Storyboard must include a table heading and at least one shot.")
        return
    _, header = rows[0]
    headers = [re.sub(r"[^a-z0-9_]+", "_", c.lower()).strip("_") for c in header]
    camera_idx = _cell_index(headers, "camera_move", "camera", "move")
    label_idx = _cell_index(headers, "screen_text", "on_screen_text", "text", "label")
    start_idx = _cell_index(headers, "start_s", "start", "start_sec")
    end_idx = _cell_index(headers, "end_s", "end", "end_sec")
    span_idx = _cell_index(headers, "start_end", "time", "timing", "timecode", "start_end_from_timings_json")
    if (start_idx is None or end_idx is None) and span_idx is None:
        errors.append("Storyboard needs start_s/end_s or an explicit time-span column.")
    if camera_idx is None:
        warnings.append("Storyboard camera_move column is absent; push-in cadence is not checked.")
    if label_idx is None:
        warnings.append("Storyboard screen_text column is absent; text-length limits are not checked.")

    prev_end = None
    pushes = 0
    text_heavy = 0
    count = 0
    for number, cells in rows[1:]:
        if len(cells) != len(headers):
            errors.append(f"Storyboard line {number}: expected {len(headers)} cells, got {len(cells)}.")
            continue
        count += 1
        start = end = None
        if start_idx is not None and end_idx is not None:
            start, end = _number(cells[start_idx]), _number(cells[end_idx])
        elif span_idx is not None:
            match = SPAN_RE.fullmatch(cells[span_idx])
            if match:
                start, end = map(float, match.groups())
        if start is None or end is None or start < 0 or end <= start:
            errors.append(f"Storyboard line {number}: invalid start/end time.")
        else:
            if end - start > MAX_BEAT_DURATION_SEC + 1e-6:
                errors.append(f"Storyboard line {number}: shot duration {end - start:.2f}s exceeds {MAX_BEAT_DURATION_SEC:.0f}s.")
            if prev_end is not None and start < prev_end - 0.05:
                errors.append(f"Storyboard line {number}: overlaps previous shot.")
            elif prev_end is not None and start > prev_end + 0.25:
                warnings.append(f"Storyboard line {number}: {start - prev_end:.2f}s gap between shots.")
            prev_end = end

        move = cells[camera_idx].lower().replace("-", "_") if camera_idx is not None else ""
        if re.search(r"\b(push|push_in|zoom_in|zoom in)\b", move):
            pushes += 1
            if pushes == 3:
                errors.append(f"Storyboard line {number}: three consecutive push/zoom moves.")
        else:
            pushes = 0
        if label_idx is not None:
            text = cells[label_idx].strip().strip('"')
            words = len(text.split()) if text not in ("", "-", "none") else 0
            if words > MAX_LABEL_WORDS:
                errors.append(f"Storyboard line {number}: label has {words} words (max {MAX_LABEL_WORDS}).")
            if words >= 5:
                text_heavy += 1
            if words and start is not None and end is not None:
                needed = 0.5 + 0.3 * words
                if end - start < needed:
                    warnings.append(f"Storyboard line {number}: short text hold ({end - start:.1f}s < {needed:.1f}s).")
    if count and text_heavy / count > 0.30:
        warnings.append(f"Storyboard: {text_heavy}/{count} text-heavy shots; review for visual storytelling.")


def lint_html_scene(html_path, errors, warnings):
    path = Path(html_path)
    if not path.is_file():
        return
    code = path.read_text(encoding="utf-8", errors="replace")
    if not any(hook in code for hook in ("window.renderAt", "window.seek", "seekFrame")):
        errors.append(f"{path}: no time-addressable rendering hook.")
    if len(re.findall(r"<section\b|class=[\"']scene[\"']", code)) >= 3:
        warnings.append(f"{path}: multiple slide-like sections; inspect rendered output.")
    if re.search(r"\b(?:Date\.now|performance\.now|Math\.random)\s*\(", code):
        warnings.append(f"{path}: wall-clock or unseeded random API may compromise determinism.")


def parse_scene_list(path, errors):
    """Support both simple paths and ffconcat 'file ...' entries."""
    manifest = Path(path)
    if not manifest.is_file():
        errors.append(f"Missing scenes list: {manifest}")
        return []
    result = []
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        raw = line.strip()
        if not raw or raw.startswith("#") or raw == "ffconcat version 1.0":
            continue
        if raw.startswith(("duration ", "inpoint ", "outpoint ", "option ")):
            continue
        try:
            parts = shlex.split(raw)
        except ValueError:
            errors.append(f"Scene list line {number}: bad quoting.")
            continue
        if parts[0] == "file":
            if len(parts) != 2:
                errors.append(f"Scene list line {number}: expected file PATH.")
                continue
            name = parts[1]
        elif len(parts) == 1:
            name = parts[0]
        else:
            errors.append(f"Scene list line {number}: unsupported entry.")
            continue
        candidate = Path(name)
        if not candidate.is_absolute():
            candidate = manifest.parent / candidate
            if not candidate.exists() and Path(name).exists():
                candidate = Path(name)  # supports paths relative to cwd
        result.append(candidate)
    if not result:
        errors.append(f"Scenes list contains no clips: {manifest}")
    return result


def probe_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=False, timeout=30,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "ffprobe failed")
    value = _number(json.loads(result.stdout).get("format", {}).get("duration"))
    if value is None or value <= 0:
        raise ValueError("invalid media duration")
    return value


def lint_timings(path, min_duration, errors, warnings):
    p = Path(path)
    if not p.is_file():
        errors.append(f"Missing timings: {p}")
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("expected a JSON object")
        duration = _number(data.get("total_duration", data.get("duration")))
        if duration is None or duration <= 0:
            raise ValueError("missing/invalid total_duration")
        if duration < min_duration:
            errors.append(f"Narration duration {duration:.2f}s is below {min_duration:.0f}s minimum.")
        if not (data.get("sections") or data.get("segments")):
            warnings.append("No timed sections/segments found; word/scene alignment unverified.")
        return duration
    except (ValueError, OSError, TypeError) as exc:
        errors.append(f"Invalid timings JSON: {exc}")
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", default="scenes/list.txt")
    parser.add_argument("--timings", default="narration/timings.json")
    parser.add_argument("--storyboard", default="storyboard.md")
    parser.add_argument("--min-duration", type=float, default=MIN_TOTAL_DURATION_SEC)
    parser.add_argument("--require-clips", action="store_true",
                        help="Post-render: missing/unreadable clips fail, and sum duration must match narration")
    args = parser.parse_args(argv)
    errors, warnings = [], []
    if not math.isfinite(args.min_duration) or args.min_duration < 0:
        errors.append("--min-duration must be finite and nonnegative")
    lint_storyboard(args.storyboard, errors, warnings)
    duration = lint_timings(args.timings, args.min_duration, errors, warnings)
    clips = parse_scene_list(args.scenes, errors)
    actual_total = 0.0
    all_exist = True
    seen_html = set()
    for clip in clips:
        if not clip.is_file():
            all_exist = False
            (errors if args.require_clips else warnings).append(f"Scene clip not found: {clip}")
        elif args.require_clips:
            try:
                actual_total += probe_duration(clip)
            except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
                errors.append(f"Unreadable scene clip {clip}: {exc}")
        html = clip.with_suffix(".html")
        if html.is_file():
            seen_html.add(html.resolve())
            lint_html_scene(html, errors, warnings)
    scenes_dir = Path(args.scenes).parent
    if scenes_dir.is_dir():
        for html in scenes_dir.glob("*.html"):
            if html.resolve() not in seen_html:
                lint_html_scene(html, errors, warnings)
    if args.require_clips and all_exist and duration is not None and clips:
        if abs(actual_total - duration) > 0.5:
            errors.append(f"Scene clips total {actual_total:.2f}s vs narration {duration:.2f}s (>0.5s mismatch).")
    print("LINT RESULT:", "FAIL" if errors else "WARN" if warnings else "PASS")
    for error in errors:
        print("  ERROR:", error)
    for warning in warnings:
        print("  WARN:", warning)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
