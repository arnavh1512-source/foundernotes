# Channel profile

Values left as `TBD` fall back to the defaults shown.

## Identity
- **Channel name:** Founder Notes (@FounderNotesin, https://www.youtube.com/@FounderNotesin)
- **Niche / promise:** The hidden mechanisms, mental models, and counter-intuitive playbooks behind great founders and systems, drawn step by step.
- **Audience:** English-speaking, global, curious non-specialists and builders; no assumed prior knowledge
- **What we never do:** clickbait we can't pay off; medical/financial advice; reuse of podcast footage or voices; generic AI slideshow templates

## Voice (narration)
- **Narrator:** male (required default: "Founder Notes Narrator" on Voicebox)
- **Engine / voice:** **voicebox** (`Chatterbox`) profile `"Founder Notes Narrator"` cloned from `.claude/skills/podcast-scout-skill/assets/voice/founder-notes-narrator-ref.wav`, speed `1.0` (~179 wpm), with `--asr --retake 2` (fallbacks: Parler locked to `assets/voice/founder-notes-narrator.wav`, then Kokoro `am_michael`)
- **Delivery:** calm, warm, clear, authoritative; ~175–180 wpm at 1.0x speed
- **Pronunciation notes:** TBD (respellings for recurring names/terms)

## Look & Style Rotation (No Repetitive Slideshows)
- **Visual language router:** Every video selects a fresh primary visual style from `.claude/memory/production_ledger.json` across:
  1. **17 Native Code-Drawn Styles (`.claude/skills/animation-styles/references/styles/*.md`):** `zackd-films`, `dan-koe`, `one-ball-showreel`, `one-line-graph`, `cgi-motion`, `lego`, `ascii-terminal`, `ink-in-water`, `ps2`, `risograph-cutout`, `renaissance-codex`, `comic-art`, `chalkboard`, `glow-sketch`, `pixel-art`, `pixel-dither`, `flat-vector`.
  2. **5 External Master Engines:** `bang-motion` (6 explainer worlds & 19 opener concepts), `vox-director` / `collage-director` (9 tactile paper-collage themes + `local-engine` element assembly), `huashu-art-motion` (9 explainer grammars + 53 living art recipes), `claude-drawing-skill` (77 CPU physical media modules + `--stages` draw-on), and `code-animation-prompts` (341 style prompts + `mg-styles-15`).
- **Brand Frame Palette (for `K.endCard` & channel chrome):** background `#101418`, ink `#F2EFE9`, accent 1 `#F2B134`, accent 2 `#4E79A7`, alert `#E15759`. Scene palettes adapt to the chosen style's specification (banning generic neon blue-purple AI gradients).
- **Typography:** Match the selected style spec (e.g., `Bricolage Grotesque` + `Caveat`, `Barlow Condensed` + `IBM Plex Mono`, `Playfair Display` + `Cinzel`, `Archivo Black`); reserve `Space Grotesk Bold` / `Inter Medium` for UI/data labels and `K.endCard`.
- **Motion personality & Easing:** Asymmetric role-based curves—snappy entrances (`cubic-bezier(0.16, 1, 0.3, 1)` / `expo.out`), sticker/card pops (`cubic-bezier(0.34, 1.56, 0.64, 1)` / `back.out(1.4)`), stepped `12fps`/`8fps` for collage/stop-motion, and fast exits (`power2.in`, `0.3s`).
- **Shot Cadence:** Visual cut or camera move every **2.0–6.0 seconds** (`<= 8.0s` hard max). Every 8–10s narration sentence splits into **Shot A (Wide establishing + `<= 7`-word headline)** and **Shot B (Tight detail cut-in, no headline)** cutting mid-sentence.

## Format & Minimum Length (Strict Owner Rule, 2026-11-08)
- **Long-form:** `1920×1080` · `30 fps` · **Minimum 8:00 (480+ seconds, 8–15 minutes target)**, requiring **1,450–2,200+ spoken words** at 1.0x Voicebox speed (~179 wpm). Never speed up narration.
- **Shorts:** optional, `1080×1920`, cut from each long video
- **Music & SFX:** low ambient bed (0.6 gain ducked under 1.25 gain VO) + frame-accurate perceptual SFX (`cues.json` synced to `<= 1 frame`), mastered to `-14 LUFS` / `<= -1 dBTP`.

## Source podcasts (owner rule)
- Never name, credit or mention the podcast, host or guest an idea came from: not in narration, on screen, in captions, the description, tags, pinned comment or CREDITS. Scouting notes stay internal (`studio-output/`).
- Never quote a guest's exact words. Put ideas in our own words; present a well-known saying as a saying ("origin unclear" if unknown). Factual claims still cite their primary research on screen and in the description.

## Subtitles (owner rule)
- Every video has subtitles burned into the picture (`assemble.py` default), in the channel font, cream on a translucent ink box at the bottom. Keep the bottom `~180 px` of every scene clear. Also upload the `.srt` as captions.

## Backgrounds & Camera Worlds (owner rule)
- Change backgrounds and camera viewpoints regularly. No two adjacent scenes share a backdrop or static camera angle, and use at least 8–10 distinct backdrops/stages per 8+ minute video.

## Characters (owner rule)
- New characters in every video. Check `assets/ink-gold-kit/CAST.md` and differ from every earlier lead in at least 4 of: skin tone, hair style, facial hair, glasses, build, outfit colours. Log the new cast there.
- Real people are never drawn (unless using C-roll photographic cutout stickers for historical artifacts/products).

## Channel identity and the ending (owner rule)
- **The channel:** Founder Notes, at https://www.youtube.com/@FounderNotesin. The tagline is "One big idea from every conversation, drawn step by step."
- **The logo:** `assets/ink-gold-kit/channel/logo.png`.
- **The ending of every video:**
  - the **closing narration line** asks viewers to subscribe and asks the comment question.
  - the **end card** is `K.endCard(S)`: logo, "Subscribe to FOUNDER NOTES", a cursor clicking the subscribe button, and next-video card placeholder.
PROFILE_EOF
