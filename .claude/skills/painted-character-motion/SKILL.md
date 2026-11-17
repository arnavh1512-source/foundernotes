---
name: painted-character-motion
description: "Original 16:9 animated character scenes for FounderNotes: expressive 2D poses, articulated limbs, attached props, 2.5D layer parallax, visual storytelling, measured narration timing and MP4 export via the existing motion renderer. Optional and rights-safe."
---

# Painted Character Motion — FounderNotes

This is a **new, original implementation** designed for the existing FounderNotes
`motion` HTML renderer. Its goals were informed by studying
[SahilScripts/mahabharat-motion-kit](https://github.com/SahilScripts/mahabharat-motion-kit),
**not** by copying its character assets or code. No confirmed reuse license was
present in the upstream repository at inspection time, so no upstream source,
characters, sample reels, voices, artwork, music, or dependencies were imported.
This is a clean-room-style implementation of common 2D animation techniques.

**What is implemented now:** deterministic pure-time SVG scenes, 16:9 composition,
original two-character study/gate/staircase assets, two-link puppet-like arms,
relative wrist-attached props, restrained facial expressions, background and
foreground camera parallax, reproducible grain, caption preview, reusable
Python timing adapter, and one five-beat demonstration.

**What is NOT implemented:** faithful human anatomical IK, real lip sync, live
speech synthesis, broad scene/prop libraries, automatic art direction, natural
walking cycles, full 4-minute or 8-minute productions. The sample is an
illustrative motion test, not a completed film. Do not mislabel it as a
fully hand-painted 2D production. Its drawings are original SVG vector art.

## How it fits FounderNotes

1. **Research + script:** follow viewer-first gate and originality/rights checks.
2. **Narration:** use approved Voicebox or VoiceStudio (VoiceStudio is provided
   by the integrated opt-in `voicestudio_narrate.py` adapter).
3. **Timings:** use measured `narration/timings.json`, not guessed script durations.
4. **Animation:** this skill's `engine.js` uses a time-indexed SVG program.
5. **Render:** the existing `.claude/skills/motion/scripts/render.mjs` captures
   frames with Chromium and encodes with FFmpeg. No second renderer is bundled.
6. **QC:** FounderNotes' still comparison, audio review, caption, motion and
   `qc_video.py` gates remain mandatory. This skill does not waive the 8+ minute
   long-form publishing rule. Short tests are private pilot material.

### Test the original sample in a browser

Open `examples/philosopher-map.html` in a local browser. The first frame moves
when the render time advances, and `?t=9` previews a deterministic frame.
The dialogue is original sample text about an old street map and overlooked
steps, not reproduced copyrighted book dialogue.

### Produce stills and sample MP4 using the existing motion renderer

From the FounderNotes repository root:

```bash
node --test .claude/skills/painted-character-motion/tests/test_engine.cjs
python3 -m unittest discover -s .claude/skills/painted-character-motion/tests -p 'test_*.py' -v

# On a computer with Playwright/Chromium and ffmpeg installed for /motion:
node .claude/skills/motion/scripts/render.mjs \
  .claude/skills/painted-character-motion/examples/philosopher-map.html \
  --stills 1,5,9,13,18 --out motion-output/painted-demo/stills

node .claude/skills/motion/scripts/render.mjs \
  .claude/skills/painted-character-motion/examples/philosopher-map.html \
  --out motion-output/painted-demo/pilot.mp4 --draft
```

`--draft` uses lower resolution and 15 fps. Render without `--draft` only
when it passes still, motion and listening reviews. The sample has no voiced
audio; do not claim VoiceStudio was used for its soundtrack.

### Use an actual FounderNotes two-character narration

The `scripts/build_from_timings.py` bridge maps every existing narration
segment to one of five illustrated scene types. It checks that segment starts
and ends are finite, ordered, non-overlapping and fit inside the master audio.
It preserves leading silence, pauses and trailing room tone.

```bash
python3 .claude/skills/painted-character-motion/scripts/build_from_timings.py \
  studio-output/philosopher-pilot/narration/timings.json \
  --out studio-output/philosopher-pilot/painted

node .claude/skills/motion/scripts/render.mjs \
  studio-output/philosopher-pilot/painted/index.html \
  --out studio-output/philosopher-pilot/painted/pilot.mp4 \
  --audio studio-output/philosopher-pilot/narration/narration.wav
```

These commands require narration files to **already exist**, created on the
user's machine by authorized local TTS. If TTS is missing, prepare only the
silent visual preview, clearly labeled as such. The bridge emits
`shot-timeline.json`, `index.html`, and its own copy of `engine.js` inside
`studio-output` so the visual scene can be rendered without importing another
codebase. The resulting video is 1920×1080 at 30 fps by default.

The adapter uses the `scene_id` in each `timings.json` segment. Defaults:

| Narration scene ID | Drawing |
| --- | --- |
| `hook`, `gates`, `gate` | Old town gate |
| `study`, `intro`, `meeting` | Hilltop philosopher's study |
| `map`, `question`, `drawing` | Animated paper map |
| `stairs`, `staircase`, `discovery` | Hidden pedestrian staircase |
| `close`, `closing`, `ending` | Study conclusion |

Custom mappings use `--mapping local-mapping.json`, a JSON object from the
narration `scene_id` to one of `gate`, `study`, `map`, `stairs`, or `close`.
**Unknown mappings fail** instead of silently illustrating the wrong idea.

**Subtitles:** `--show-captions` is only a rough preview, with a single
segment's text rendered at once. For release, leave it off and let the existing
FounderNotes `assemble.py` burn the reviewed `captions.srt`. Do not claim
word-accurate lip sync or caption timing based on this SVG engine.

## Extending it safely

- Add an independent visual beat as a new `case` to `draw()` in `engine.js`,
  then update `validate()` and the Python adapter `SUPPORTED` set.
- Never add vague visual filler. Each motion should communicate one concrete
  event. The sample is a **technical smoke test** and should be artistically
  improved before real publication.
- Keep faces, costumes, props and palette original; keep common animation
  concepts such as tweening and parallax but do not transplant source files
  from the upstream repository without a validated license or permission.
- Change character expression through `mood`, `tilt`, `nod`, and wrist
  positions; held props are attached in character-local coordinates.
- Distinct characters must use approved speech profiles. No unapproved voice
  cloning or external network data is needed by this library.
- Do a real browser screenshot pass for first/mid/last frames and verify
  no cut-off faces, hands or captions. Motion should be visually meaningful
  rather than constant arbitrary zooming.

## Status / provenance

- Reusable code, timing bridge and regression tests: integrated.
- Local Node/Python unit tests: recorded in PR validation notes.
- SVG browser screenshot smoke test: recorded in PR validation notes.
- Native `render.mjs` draft and frame-strip smoke test: covered by the painted CI job; passing checks are technical evidence, not creative approval.
- Commercial reuse: source code here is original and does not inherit unknown
  permissions from the inspiration repository; verify Remotion/other tool
  terms separately before production.

Build outputs require a fresh folder; earlier cuts are never overwritten. Use the registered `painted-character-motion` picture-import backend in studio_loop.py to retain assembly, captions, QC and approval gates.
