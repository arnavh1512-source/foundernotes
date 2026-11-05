---
name: collage-director
description: >
  Paper-collage motion-graphics engine on MuAPI (adapted from Anil-matcha/vox-ai-motion-graphics-generator, MIT).
  Turns a topic or beat map into torn-paper collage keyframes (Flux), animates them (Veo/Kling image-to-video),
  and adds male narration, music and burned-in captions. Use it for a collage-style explainer or Short, or to
  generate collage B-roll inserts and alternative scene looks for podcast-scout-skill films. Needs MuAPI credit.
---

# Collage Director (Hunting Titles edition)

This is a second visual language for the studio, next to the Ink & Gold kit. Each beat is a torn-paper collage
poster that comes alive. It runs on the **MuAPI** cloud (the same service as `gen_media.py`) plus local ffmpeg.
The upstream instructions are kept unchanged in `SKILL.upstream.md`. This file overrides them where they differ.

## Channel rules (always apply; see repo `channel-profile.md`)
- **Look:**
  - Make the look our own. Don't call it or style it as any named outlet's brand (no "Vox look", logos or mastheads).
  - Pick a palette/theme that differs from the previous collage film, and write it in the film's ledger.
- **Male narrator only:**
  - Collage films are voiced like every other film: Kokoro `am_michael` via `podcast-scout-skill/scripts/narrate.py`.
  - When using this skill's own TTS, `scripts/audio.py` enforces a male allowlist (default `English_expressive_narrator`).
- **Voice cloning is disabled.** The only exception is the owner's own recording, flagged
  `voice.clone_ref_is_owner_own_voice: true`. Never clone anyone else.
- **Real people:** never generate a real person's likeness.
  - A-roll (talking head) and C-roll (photo anchor) take only footage or photos of the owner, or products we have the right to use.
- **Captions:** subtitles are burned in (upstream `assemble.py` already does this). Also keep the `.srt` for YouTube.
- **No podcast credit:** never name the podcast, host or guest an idea came from.
- **Facts:**
  - Every factual line still goes through the podcast-scout fact lock (FACTS.md).
  - Headline text in collage posters must match the locked wording exactly. Generated text can misspell, so check every keyframe.
- **Disclosure:** collage art is AI-generated. Record model, prompt and request id in CREDITS. Tick YouTube's
  "altered or synthetic content" box if anything looks realistic.

## Prerequisites
- **MuAPI access:**
  - A MuAPI key saved as the session network secret for `api.muapi.ai` (header `x-api-key`); the scripts then work without `MUAPI_API_KEY`.
  - **Credit on the account.** An unfunded account gets stock samples back. Check first:
    `curl -s -H "x-api-key: proxy-injected" https://api.muapi.ai/api/v1/account/balance`.
- **Local tools:** `ffmpeg`/`ffprobe`, and Python 3 with Pillow.

## Workflow (B-roll: topic → film)
1. Write `studio-output/<slug>/collage/beats.json`. Follow `examples/sample-beats.json`.
   - Hook-led beats.
   - Narration copied from the fact-locked script.
   - Set `"voice": {"voice_id": "English_expressive_narrator"}` only if not using our narrate.py.
2. `python3 scripts/style_bakeoff.py <dir>`: render one beat in 3–4 themes and **show the owner** before committing (gate 1).
3. `python3 scripts/keyframes.py <dir>`: generate the collage posters. Check every one for misspelled text and likenesses.
4. `python3 scripts/clips.py <dir>`: animate the posters. This is the expensive step, so ask before running a whole film.
5. Audio, either way:
   - preferred: `podcast-scout-skill/scripts/narrate.py` (am_michael) plus our own score;
   - or: `python3 scripts/audio.py <dir>`.
6. Assembly, either way:
   - `python3 scripts/assemble.py <dir>`;
   - or hand the clips to `podcast-scout-skill/scripts/assemble.py` with our narration (burned subtitles, −14 LUFS).
7. Run `podcast-scout-skill/scripts/qc_video.py` and the reality-checker gate as for any film.

**Inserts into an Ink & Gold film:** run steps 2–4 for selected beats only and drop the clips into
`scenes/` like any other scene. Keep the seam rules: the vector law, and no two adjacent scenes with the same backdrop.

A-roll and C-roll modes: see `SKILL.upstream.md`, under the real-people rule above.

## Prompt guide
Read `references/prompt-guide.md` (the 5-part prompt, theme presets, designing for animation) and
`references/beat-layer.md`. Upstream voices are in `references/voices.md`; use only the male ones.

## Licence
Upstream is MIT (stated in its package.json and README; no LICENSE file in the repo). Our changes:
- the male-voice allowlist;
- the cloning guard;
- proxy-key support;
- these rules.
