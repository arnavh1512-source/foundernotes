# Channel profile

Values left as `TBD` fall back to the defaults shown.

## Identity
- **Channel name:** Founder Notes (@FounderNotesin, https://www.youtube.com/@FounderNotesin)
- **Niche / promise:** TBD (e.g. "the mechanisms behind ideas experts argue about, in under 10 minutes")
- **Audience:** English-speaking, global, curious non-specialists; no assumed prior knowledge
- **What we never do:** clickbait we can't pay off; medical/financial advice; reuse of podcast footage or voices

## Voice (narration)
- **Narrator:** male (required default)
- **Engine / voice:** kokoro `am_michael`, speed 0.88  (fallback: piper `en_US-ryan-high`)
- **Delivery:** calm, warm, clear; conversational; 140–160 wpm
- **Pronunciation notes:** TBD (respellings for recurring names/terms)

## Look
- **Visual language:** TBD — pick one: clean diagram (motion skill) · chalkboard (anidoodle/HandDraw) ·
  3b1b maths (Manim) · paper-craft/collage · stickman · watercolour storybook
- **Palette:** background `#101418`, ink `#F2EFE9`, accent 1 `#F2B134`, accent 2 `#4E79A7`, alert `#E15759`
- **Type:** headings Inter/Space Grotesk Bold; labels Inter Medium (ship font files locally)
- **Motion personality:** Premium/calm — signature easing cubic-bezier(0.4,0,0.2,1); durations 0.4 / 0.7 / 1.2 s
- **Recurring element:** TBD (a character, object or frame device)
- **Thumbnail system:** one focal object, ≤3 words, accent colour, same art style as the video

## Format & cadence
- **Long-form:** 1920×1080 · 30 fps · 5–12 min, length follows the teaching scope
- **Shorts:** optional, 1080×1920, cut from each long video
- **Cadence:** TBD
- **Music:** low ambient bed, CC0/licensed/own-composed only, ducked under voice

## Approvals
- **Autonomous end-to-end allowed:** no (stop at script+storyboard and at look stills)  ← change to yes to skip
- **Paid tools allowed:** no (ask with a cost estimate first)

## Source podcasts (owner rule)
- Never name, credit or mention the podcast, host or guest an idea came from: not in narration, on screen,
  in captions, the description, tags, pinned comment or CREDITS. Scouting notes stay internal (studio-output/).
- Because of that, never quote a guest's exact words. Put ideas in our own words; present a well-known
  saying as a saying ("origin unclear" if unknown). Factual claims still cite their primary research on screen
  and in the description.

## Subtitles (owner rule)
- Every video has subtitles burned into the picture (assemble.py default), in the channel font, cream on a
  translucent ink box at the bottom. Keep the bottom ~180 px of every scene clear. Also upload the .srt as captions.

## Backgrounds (owner rule)
- Change backgrounds regularly. No two adjacent scenes share a backdrop, and use at least 6 different backdrops per film.
- Use `K.backdrop` (assets/ink-gold-kit), and let the backdrop follow the meaning (e.g. clinic for hospital data, fog for uncertainty, sunrise for the turn).

## Characters (owner rule)
- New characters in every video. Check `assets/ink-gold-kit/CAST.md` and differ from every earlier lead in
  at least 4 of: skin tone, hair style, facial hair, glasses, build, outfit colours. Log the new cast there.
- Real people are never drawn.

## Channel identity and the ending (owner rule)
- **The channel:** Founder Notes, at https://www.youtube.com/@FounderNotesin. The tagline is "One big idea from every founder story".
  Note that @FounderNotes is a different channel.
- **The logo:** the channel's own avatar, in `assets/ink-gold-kit/channel/logo.png`.
- **The ending of every video:**
  - the **closing narration line** asks viewers to subscribe and asks the comment question, e.g. "…subscribe to Founder Notes. And tell us in the comments: what topic should we cover next?";
  - the **end card** is `K.endCard(S)`: logo, "Subscribe to FOUNDER NOTES", a cursor clicking the subscribe button, then the question card "What topic should we cover next? / Tell us in the comments".
- **The package:** the description ends with the subscribe link plus the question, and the pinned comment opens with the question.

## Length (owner rule, 2026-11-06)
Every long-form video runs **at least 5 minutes**. Keep the narration exactly as approved (voicebox narrator, speed 1.0, ~179 wpm; never slowed down). Script ~900+ spoken words. Add researched beats (evidence detail, how-to-judge-it checklists, counter-arguments), never filler.
