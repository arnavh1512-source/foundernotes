---
name: podcast-scout-skill
description: Turn podcast links, audio/video files, transcripts or a plain topic into researched 8+ minute educational YouTube videos — evidence-checked ideas, editorial scores, scripts, storyboards, Voicebox male narration, multi-style animated scenes, captions, a rendered MP4 master and an upload package.
---
# Podcast Scout Studio (v4.0 — Self-Improving Multi-Style Edition)

Find the teachable ideas inside an expert conversation, prove them, and turn the best ones into original **8+ minute (`>= 480s`)** animated explainers for an English-speaking global YouTube audience.

## Session defaults (apply unless the channel owner changes them)

| Setting | Default |
|---|---|
| **Narrator** | **Voicebox (`Chatterbox`) profile `"Founder Notes Narrator"`** (`assets/voice/founder-notes-narrator-ref.wav`, `speed: 1.0`, `--asr --retake 2`). Fallbacks: Parler (`assets/voice/founder-notes-narrator.wav`) -> Kokoro `am_michael`. |
| **Minimum Length** | **>= 8:00 (`480+ seconds`, target 8–12 min = `1,450–2,100+ spoken words` at ~179 wpm)**. Never speed up audio. |
| **Crew Models** | Target **Sonnet 5.5 with medium effort** when the installed Claude Code host offers it. Agent files request `model: sonnet`, `effort: medium` (version alias must be verified at runtime; do not claim 5.5 if not confirmed). |
| **Style Universe** | Choose narrative-appropriate techniques from all **17 native `.claude/skills/animation-styles/references/styles/*.md`** + **5 external engines** (`bang-motion`, `vox-director`/`collage-director`, `huashu-art-motion`, `claude-drawing-skill`, `code-animation-prompts`). Check `.claude/memory/production_ledger.json` for repetition; prefer continuity and scene relevance over forced switches. Consult `references/agency-production-system.md` for the expanded engine catalog and approval gates. |
| **Format & QA** | `1920x1080`, `30 fps`, H.264/AAC, `-14 LUFS`; `2.0s–6.0s` shot cadence (`<= 8.0s` max); `0.25s` overlap check; zero `>= 0.3s` blank mid-video gaps; `< 3.5%` fast-motion diagnostic (review intentional holds). |
| **Self-Improvement** | Read `.claude/memory/mistakes_and_pitfalls.md` & `positive_recipes.md` before starting; log every new mistake and winning recipe after QA via `scripts/record_lesson.py`. |

## Production constitution (read before every video)

Read `references/agency-production-system.md` and `references/production-stack.md` first. The studio is an accountable crew, not a preset shuffler: **researcher → scriptwriter → visual director/storyboarder → animator → sound engineer → editor → independent reality checker → packager**. Every handoff includes actual files and evidence. Do not manufacture QC reports, citations, model versions, voice checks or rendered outputs. A film is complete only when its master has been played, inspected, and approved. Read `references/agent-reach.md` for the preferred optional research adapter.

**Narration lock:** maintain the channel's consistent male narrator. Use the authorized Voicebox profile when available; fallbacks must also use male voices. Lock and measure audio before shot timing. No narration duration guess can replace actual `ffprobe` measurement. Never clone a third party's voice without permission.

**Animation sources:** use the 17 native reference styles plus the listed external engines, including Anidoodle, ClaudeAnimationBase, HandDraw, Manim, JavaScript Animation Skills, LottieFiles motion-design craft, Huashu, and Claude Drawing Skill. Additional animation, YouTube and production repositories are inventoried in `references/agency-production-system.md`. A listed repository is **not installed** by this skill and not proof of benchmarked rendering.

**Pilot before scale:** make a 30–60 second pilot with real male audio, a coherent world, proofed frame transitions and an independent critique; fix failures before the full 8+ minute video. No automatically scheduled publishing.

## Stages 1-6: Scout pipeline
1. **Ingest & Extract:** Ingest input (URL, file, transcript, or topic). Identify core subject and raw key points.
2. **Fact Check & Deepen:** Search web/academic literature for ground-truth evidence on every key point. Drop unverified claims; attach primary citations.
3. **Score Opportunities:** Score *Surprise*, *Evidence Density*, *Visual Explanability*, *Utility*, and *Search Interest* (1-5 each; require >= 16/25).
4. **Draft Briefs:** Write detailed briefs for top 1-3 ideas designed to sustain an **8–12 minute (`1,450–2,100+ word`)** multi-chapter breakdown.
5. **Review Gate:** Present ranked briefs to the user unless end-to-end production was requested.

## Stages 7-12: Studio pipeline
7. **Scriptwriting (`studio-scriptwriter.md`):** Write `script/script.md` with **at least 1,450–1,800+ spoken words** (`>= 8:00` at 179 wpm), structured into 5–7 chapters with 2 visual beats per sentence (`2.0s–6.0s` per beat).
8. **Storyboard & Multi-Style Visual Direction (`studio-visual-director.md`):** Read `.claude/memory/` first. Pick a story-appropriate primary visual grammar from the 17 native styles and the external catalog, maintaining coherence across shots. Review recent styles but never force visually unrelated scenes just to maximize diversity. Write `storyboard.md` and `cues.json` (every row has a Concrete Noun + Active Verb + Camera Move, zero 3-in-a-row zoom-ins, `<= 7` words per label). Render 3-way style bake-off stills (`--stills`).
9. **Voicebox Narration & Perceptual Audio (`studio-sound-engineer.md`):** Start `voicebox_server.sh`, run `narrate.py --asr --retake 2` (`"Founder Notes Narrator"`, `speed=1.0`), verify total audio duration is **`>= 480.0s` (8:00+)**, extract word-level ASR timestamps (`timings.json`) and pause grids (`SEG`/`PARA`), and align perceptual SFX hits to `cues.json`.
10. **Deterministic Scene Rendering (`studio-animator.md`):** Implement `window.seek = window.renderAt = window.OPENER.seekFrame` for 100% deterministic frame stepping. Proof keyframe stills (`--stills`) first, fix any overlaps or `180px` bottom-zone intrusions, run `lint_scenes.py`, and render `1920x1080 @ 30fps` scene clips.
11. **Edit, Assembly & Automated QC (`studio-editor.md`):** Assemble scenes, Voicebox narration, burned-in captions (`karaoke_ass.py`), ducked BGM (`0.6` under `1.25` VO), and `K.endCard(S)` via `assemble.py`. Run `qc_video.py` (enforcing `>= 480.0s`, `< 3.5%` anti-PPT motion gate, no unexplained `>= 0.3s` blank/dead gaps, and audio sync).
12. **Blind Critic Jury & Memory Reflow (`studio-reality-checker.md` & `studio-packager.md`):** Run 2 rounds of 7-dimension rubric grading (`>= 8.0/10` required), package YouTube metadata, and append all lessons learned and style fingerprints to `.claude/memory/` via `scripts/record_lesson.py`.

