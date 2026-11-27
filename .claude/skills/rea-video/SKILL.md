---
name: rea-video
description: Shot-by-shot video breakdown with rea-video (Apache-2.0, JuneYaooo/rea-video, installed pinned, not vendored). Finds cuts, shot lengths, camera framing and moves, caption timing, voice/music/sound-effect stems and beat alignment, and how each shot was made. Use on reference videos the owner supplies, and on our own rendered cuts and Shorts as a viewer-side review before delivery. Never a substitute for the studio's frame check, QC or watching.
---

# rea-video for Think!

[rea-video](https://github.com/JuneYaooo/rea-video) reverse-engineers a video shot by shot and writes a layered breakdown (`VIDEO.md`) plus a report. Its own agent guide is `skills/rea-video/SKILL.md` in the installed source (mostly Chinese). **This page overrides it** wherever they differ; CLAUDE.md overrides both.

## Install (once per machine)

```bash
bash .claude/skills/rea-video/setup.sh     # pinned commit, own venv at ~/.cache/venv-rea
```

The first `decompose` downloads about 220 MB of free audio-separation models into `~/.cache/rea-video/models`. Check disk space first.

## What we use it for

1. **Reference videos the owner supplies** (Alan Becker, DayOne Films, PsychToons, PsychDoodle, or any clip they hand over as a file). It measures cut rhythm, shot lengths, camera moves, caption style and sound-effect placement. Record what it measured, with the file and the limits, in `docs/REFERENCE_REVIEW.md` and the episode's `review/` folder. Never download YouTube media to feed it: the research gateway fetches subtitles and metadata only, and YouTube blocks downloads here.
2. **Our own cuts and Shorts, before delivery.** Run it on `final/video.mp4` and `short/final/summary-short.mp4` and read what a viewer-side tool sees: long static stretches, too few cuts, sound effects that don't land on visible events, captions too long or overlapping. On Night 1 Part 2's Short it found only 5 shots in 46 s, because the picture fills just the middle third of the vertical frame while the title and caption bands stay still. That is a real fix for the next Short.

```bash
R=~/.cache/venv-rea/bin/rea-video
$R --lang en decompose <video.mp4> -o studio-output/<slug>/review/rea/<name> --lang en
$R summary studio-output/<slug>/review/rea/<name>/breakdown.json
```

Read `VIDEO.md` first, then only the parts you need (`video/timeline.md`, `video/rhythm.md`, `video/sound.md`). Don't paste `breakdown.json` into a conversation.

## Rules

- **No paid or remote calls without the owner's approval:** no `--vlm` (Gemini or another vision model), no `remake-run`, Capsule Cinema or ChatCut. Offline runs are free. When images matter, do the visual review yourself with `rea-video review` / `apply-review`.
- **Its inferences are evidence, not facts.** It called our CC0 human-composed music "most likely AI-generated (52%)", and its signal-only sound-effect list is low-confidence. Confirm by looking and listening before acting on a finding, and never put its numbers in narration or a description as facts.
- **It doesn't replace the studio's checks:** `tools/precheck.sh` (every frame before a render), `qc_video.py`, the delivery package and watching the cut still apply.
- **Remake suggestions** (generation units, models, prompts) are for study only. Our videos stay original stick animation in the Think! engine; never copy a reference's characters, scenes or assets.
- Breakdowns go in `studio-output/<slug>/review/rea/` (git-ignored).
