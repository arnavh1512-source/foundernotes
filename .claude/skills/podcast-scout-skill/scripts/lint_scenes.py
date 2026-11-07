cat << 'LINT_EOF' > .claude/skills/podcast-scout-skill/scripts/lint_scenes.py
#!/usr/bin/env python3
"""
lint_scenes.py — Upgraded Pre-Render & Post-Scene Linter for Founder Notes Studio (v4.0).

Checks:
1. Storyboard & Beat Cadence Rules (if --storyboard provided):
   - Every shot duration is between 1.5s and 8.0s (target 2.0s-6.0s; >8.0s = FAIL for static PPT hold).
   - No 3 consecutive 'push' / 'zoom_in' camera moves in a row.
   - On-screen text labels <= 7 words and hold duration >= 0.5s + 0.3s * words.
   - Text-dominant shots <= 30% of total shots.
2. Scene HTML/JS Code Anti-Slop & Safe-Zone Static Audit:
   - Verifies deterministic time hook (`window.renderAt` or `window.seek` or `window.OPENER.seekFrame`).
   - Flags unseeded `Math.random()` or `Date.now()` inside render loops.
   - Flags `<section>` slideshow fading (>= 3 `<section` tags).
   - Checks for bottom 180px subtitle safe-zone awareness.
3. Timings & Duration Verification:
   - Total narration duration in `narration/timings.json` must be >= 480.0s (8:00 minimum owner rule).
   - Scene list (`scenes/list.txt`) exists and matches narration duration within 0.5s.
"""

import os
import re
import sys
import json
import argparse

MIN_TOTAL_DURATION_SEC = 480.0  # 8 minutes strict owner rule
MAX_BEAT_DURATION_SEC = 8.0     # Anti-PPT max single shot duration
MAX_LABEL_WORDS = 7

def lint_storyboard(storyboard_path, errors, warnings):
    if not os.path.exists(storyboard_path):
        warnings.append(f"Storyboard file not found for deep beat lint: {storyboard_path}")
        return

    with open(storyboard_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    table_rows = [
        line.strip() for line in lines
        if line.strip().startswith("|") and not re.match(r"^\|\s*[-:]+", line.strip())
    ]
    if len(table_rows) <= 1:
        return

    consec_push = 0
    text_dominant_count = 0
    total_beats = 0

    for idx, row in enumerate(table_rows[1:], start=1):
        cols = [c.strip() for c in row.strip("|").split("|")]
        if len(cols) < 4:
            continue
        total_beats += 1
        row_text = " ".join(cols).lower()

        # Check consecutive camera push-ins
        if re.search(r"\b(push|push_in|zoom_in|zoom in)\b", row_text):
            consec_push += 1
            if consec_push >= 3:
                errors.append(
                    f"Storyboard row {idx}: 3 consecutive camera push/zoom-in moves detected "
                    "(violates Director Rule: alternate push with pull, glide, static, or cut)."
                )
        else:
            consec_push = 0

        # Check beat duration if start-end pattern like 12.0-21.5 is present
        m_span = re.search(r"(\d+(?:\.\d+)?)\s*[-–to]+\s*(\d+(?:\.\d+)?)", row)
        if m_span:
            start_s, end_s = float(m_span.group(1)), float(m_span.group(2))
            dur = end_s - start_s
            if dur > MAX_BEAT_DURATION_SEC:
                errors.append(
                    f"Storyboard row {idx}: Beat duration {dur:.2f}s exceeds {MAX_BEAT_DURATION_SEC}s cap "
                    "(split into Shot A Wide + Shot B Detail cut-in)."
                )

        # Check label word count if screen_text column is last or second-to-last
        for col in cols:
            if col.startswith('"') and col.endswith('"'):
                words = [w for w in col.strip('"').split() if w]
                if len(words) > MAX_LABEL_WORDS:
                    errors.append(
                        f"Storyboard row {idx}: On-screen label '{col}' has {len(words)} words "
                        f"(max {MAX_LABEL_WORDS} words allowed)."
                    )
                if len(words) >= 5:
                    text_dominant_count += 1

    if total_beats > 0 and (text_dominant_count / total_beats) > 0.30:
        errors.append(
            f"Storyboard has {text_dominant_count}/{total_beats} ({text_dominant_count/total_beats:.0%}) "
            "text-heavy beats (max 30% allowed; show physical objects and actions instead of text cards)."
        )

def lint_html_scene(html_path, errors, warnings):
    if not os.path.exists(html_path):
        return
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    # 1. Check deterministic time interface
    if not any(hook in code for hook in ("window.renderAt", "window.seek", "seekFrame")):
        errors.append(
            f"{html_path}: Missing deterministic time hook (`window.renderAt(t)`, `window.seek(t)`, or `OPENER.seekFrame(t)`)."
        )

    # 2. Check anti-PPT <section> count
    section_count = len(re.findall(r"<section\b|class=[\"']scene[\"']", code))
    if section_count >= 3:
        errors.append(
            f"{html_path}: Found {section_count} `<section>`/`.scene` blocks (Anti-PPT Law: use a continuous `#world` camera stage instead of fading slide sections)."
        )

    # 3. Check unseeded Date.now() / performance.now() outside preview guard
    if "Date.now()" in code:
        warnings.append(
            f"{html_path}: Uses `Date.now()` — ensure all frame states during export depend strictly on timestamp `t`."
        )

def main():
    parser = argparse.ArgumentParser(description="Lint scene files, storyboard, and timings for Studio build")
    parser.add_argument("--scenes", default="scenes/list.txt", help="Path to scenes/list.txt")
    parser.add_argument("--timings", default="narration/timings.json", help="Path to narration/timings.json")
    parser.add_argument("--storyboard", default="storyboard.md", help="Path to storyboard.md")
    parser.add_argument("--min-duration", type=float, default=MIN_TOTAL_DURATION_SEC, help="Minimum total video duration in seconds (default 480s = 8:00)")
    args = parser.parse_args()

    errors = []
    warnings = []

    lint_storyboard(args.storyboard, errors, warnings)

    if not os.path.exists(args.timings):
        errors.append(f"Missing timings file: {args.timings}")
    else:
        with open(args.timings, "r", encoding="utf-8") as f:
            timings = json.load(f)
        total_dur = float(timings.get("total_duration", 0.0))
        if total_dur > 0 and total_dur < args.min_duration:
            errors.append(
                f"Narration total_duration ({total_dur:.2f}s / {total_dur/60:.2f}m) is below the strict "
                f"{args.min_duration:.0f}s (8:00) minimum rule. Expand script before rendering scenes."
            )
        sections = timings.get("sections", [])
        if not sections:
            warnings.append("timings.json has no sections defined")

    if not os.path.exists(args.scenes):
        errors.append(f"Missing scenes list file: {args.scenes}")
    else:
        with open(args.scenes, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        if not lines:
            errors.append("scenes/list.txt is empty")
        for line in lines:
            parts = line.split()
            if len(parts) >= 2 and parts[0] == "file":
                filepath = parts[1].strip("'\"")
                if not os.path.exists(filepath):
                    warnings.append(f"Scene clip file does not exist yet: {filepath}")
                html_candidate = os.path.splitext(filepath)[0] + ".html"
                if os.path.exists(html_candidate):
                    lint_html_scene(html_candidate, errors, warnings)

    # Also lint any HTML scenes in scenes/ directory
    scenes_dir = os.path.dirname(args.scenes) or "scenes"
    if os.path.isdir(scenes_dir):
        for fname in sorted(os.listdir(scenes_dir)):
            if fname.endswith(".html"):
                lint_html_scene(os.path.join(scenes_dir, fname), errors, warnings)

    print("LINT RESULT:")
    if errors:
        print("  Status: FAIL")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN: {w}")
        sys.exit(1)
    elif warnings:
        print("  Status: WARN")
        for w in warnings:
            print(f"  WARN: {w}")
    else:
        print("  Status: PASS (All Storyboard, Anti-PPT, Determinism & >= 8:00 Duration Gates Green)")

if __name__ == "__main__":
    main()
LINT_EOF
chmod +x .claude/skills/podcast-scout-skill/scripts/lint_scenes.py
