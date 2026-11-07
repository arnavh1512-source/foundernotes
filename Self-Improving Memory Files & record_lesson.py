cat << 'MEM1_EOF' > .claude/memory/mistakes_and_pitfalls.md
# Studio Mistakes & Pitfalls Log ("踩过的坑" — Never Repeat Twice)

Every visual, choreography, timing, gap, or audio mistake caught during production or owner review is logged here with its exact code fix and linter check. All agents MUST read this file before starting work.

| # | Category | Mistake / Failure Symptom | Root Cause | Permanent Fix & Automated Gate Added |
| :- | :--- | :--- | :--- | :--- |
| 1 | **Visual Variety** | Every video looked like the same dark corporate slide deck (`#101418` + `Inter` + static `K.backdrop`). | `channel-profile.md` locked one palette/font across all scenes instead of rotating the 17 native `animation-styles` + 5 external engines. | Unlocked all 17 `animation-styles` + 5 external engines; `.claude/memory/production_ledger.json` blocks repeating any primary style within 5 videos. |
| 2 | **Motion Physics** | Animations felt robotic and AI-generated. | Every element used the same symmetric `cubic-bezier(0.4, 0, 0.2, 1)` curve or faded `<section>` slides. | Enforced asymmetric curves (`expo.out`, `back.out(1.4)`, `MO.step(12)`, `power2.in`) and continuous `#world` camera rigs; `lint_scenes.py` rejects `>= 3` `<section>` blocks. |
| 3 | **Shot Cadence & Gaps** | 10-second static layouts and mid-video blank/dead gaps caused viewer boredom. | Storyboard mapped 1 static scene per 10s narration paragraph without mid-sentence detail cuts. | Enforced `2.0s–6.0s` beats (`<= 8.0s` cap in `lint_scenes.py`) and added pixel-level `film_gate` in `qc_video.py` (rejects fast-motion `< 0.035` or blank gaps `>= 0.3s`). |
| 4 | **Video Length** | Videos ran short (< 8 minutes). | Scriptwriter targeted 450–900 words instead of `1,450+` words at 179 wpm (`speed: 1.0`). | Enforced `>= 480.0s` (8:00+) and `1,450–2,000+` words in `studio-scriptwriter.md`, `lint_scenes.py`, and `qc_video.py`. |
| 5 | **Narration Drift** | Agents defaulted to `kokoro` instead of the owner's fast Voicebox pipeline. | `studio-*.md` files still had legacy Kokoro instructions. | Unified all agent prompts on Voicebox (`"Founder Notes Narrator"`, `voicebox_server.sh`, `narrate.py --asr --retake 2`). |
MEM1_EOF

cat << 'MEM2_EOF' > .claude/memory/positive_recipes.md
# Proven Winning Animation & Sound Recipes ("07-正面经验")

High-scoring (`>= 8.5/10`) visual, choreography, and audio patterns verified in production.

1. **2-Shots-Per-Beat Mid-Sentence Cut (`vox-director` + `huashu`):** Split every `8–10s` narration sentence into **Shot A (Wide Establishing + `<= 7`-word headline)** and **Shot B (Tight Mechanism Cut-In without headline)** cutting mid-sentence while Voicebox narration flows continuously.
2. **Frame-1 Poster Law (`animation-styles/checklist.md`):** Render the hero subject at full scale on Frame 0 (`t = 0.0s`) with zero fade-from-black so the video hooks viewers in the first `0.1s`.
3. **Asymmetric Entrance/Exit Rhythm (`bang-motion`):** Enter with `cubic-bezier(0.16, 1, 0.3, 1)` (`0.6s–0.9s`) or `cubic-bezier(0.34, 1.56, 0.64, 1)` (`back.out(1.4)`), hold steady while viewers read (`>= 0.5s + 0.3s * word_count`), and exit faster with `power2.in` (`0.3s–0.45s`) overlapping the next beat by `0.3s`.
4. **Perceptual SFX Sync (`mg-styles-15` / `mgaudio`):** Align `whoosh` peak amplitude to the midpoint of camera whip pans, `impact`/`thud` transient to frame 0 of text slams, and `12fps` stepped ticks/scribbles to `chalkboard`, `comic-art`, `lego`, and `y2_vox` draws.
MEM2_EOF

cat << 'MEM3_EOF' > .claude/memory/production_ledger.json
{
  "schema_version": "4.0",
  "min_duration_seconds": 480.0,
  "no_repeat_window_videos": 5,
  "available_native_17_styles": [
    "ascii-terminal", "cgi-motion", "chalkboard", "comic-art", "dan-koe",
    "flat-vector", "glow-sketch", "ink-in-water", "lego", "one-ball-showreel",
    "one-line-graph", "pixel-art", "pixel-dither", "ps2", "renaissance-codex",
    "risograph-cutout", "zackd-films"
  ],
  "available_external_5_engines": [
    "bang-motion (6 explainer worlds + 19 opener concepts)",
    "vox-director / collage-director (9 collage themes + local-engine)",
    "huashu-art-motion (9 explainer grammars + 53 living art recipes)",
    "claude-drawing-skill (77 CPU physical media modules + --stages draw-on)",
    "code-animation-prompts (341 style prompts + mg-styles-15)"
  ],
  "completed_videos": []
}
MEM3_EOF

cat << 'REC_EOF' > .claude/skills/podcast-scout-skill/scripts/record_lesson.py
#!/usr/bin/env python3
"""
record_lesson.py — Self-Improving Memory Reflow Script for Founder Notes Studio.

Appends mistakes/fixes to `.claude/memory/mistakes_and_pitfalls.md`,
winning recipes to `.claude/memory/positive_recipes.md`, and completed
video fingerprints to `.claude/memory/production_ledger.json`.
"""

import os
import json
import argparse
from datetime import datetime, timezone

def main():
    parser = argparse.ArgumentParser(description="Record post-video QA lessons and style fingerprints")
    parser.add_argument("--mistake", help="Symptom of mistake caught during QA or review")
    parser.add_argument("--category", default="Animation/QA", help="Category of mistake")
    parser.add_argument("--cause", default="See QA report", help="Root cause of mistake")
    parser.add_argument("--fix", default="Patched in scene/script and added to checklist", help="Permanent fix applied")
    parser.add_argument("--recipe", help="Winning visual/motion/audio recipe to append to positive_recipes.md")
    parser.add_argument("--video-slug", help="Completed video slug to register in production_ledger.json")
    parser.add_argument("--primary-style", help="Primary style used in the video")
    parser.add_argument("--fingerprint", help="5-part fingerprint: concept · chapters · object · opener · closer")
    parser.add_argument("--duration", type=float, default=0.0, help="Final video duration in seconds")
    parser.add_argument("--score", type=float, default=0.0, help="Final 7-dimension rubric average score (1-10)")
    args = parser.parse_args()

    os.makedirs(".claude/memory", exist_ok=True)

    if args.mistake:
        path = ".claude/memory/mistakes_and_pitfalls.md"
        with open(path, "a", encoding="utf-8") as f:
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            f.write(f"| {ts} | **{args.category}** | {args.mistake} | {args.cause} | {args.fix} |\n")
        print(f"[Memory Reflow] Logged mistake to {path}")

    if args.recipe:
        path = ".claude/memory/positive_recipes.md"
        with open(path, "a", encoding="utf-8") as f:
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            f.write(f"- **[{ts}]** {args.recipe}\n")
        print(f"[Memory Reflow] Logged winning recipe to {path}")

    if args.video_slug and args.primary_style:
        path = ".claude/memory/production_ledger.json"
        data = {"completed_videos": []}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        data.setdefault("completed_videos", []).append({
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "slug": args.video_slug,
            "primary_style": args.primary_style,
            "fingerprint": args.fingerprint or "",
            "duration_sec": args.duration,
            "rubric_score": args.score
        })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[Memory Reflow] Registered video '{args.video_slug}' ({args.primary_style}, {args.duration:.1f}s, {args.score}/10) in {path}")

if __name__ == "__main__":
    main()
REC_EOF
chmod +x .claude/skills/podcast-scout-skill/scripts/record_lesson.py

echo "=== Upgrade Complete! Run 'git status' and 'git diff' to inspect all updated studio files. ==="
