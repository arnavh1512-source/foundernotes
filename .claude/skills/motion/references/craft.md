# Craft numbers

Defaults that already look finished. Break them on purpose, not by accident. Sizes are for
1920×1080; a 1080-wide vertical frame uses about the same pixel sizes.

## Pacing

- **Reading time:** about 3 words a second plus 1 s to notice the line, counted after it has
  finished animating in. A 9-word line needs about 4 s.
- **Scene lengths:** title 2.5–4 s, content 4–8 s, ending 2–3 s. Social: something is on screen
  in frame 0 and the hook lands by 1.5 s.
- **Entrances** 0.3–0.6 s, **exits** 0.2–0.3 s (exits are faster than entrances).
- **Holds** of 1–3 s are good if something small still moves. `check.sh` flags 1.5 s of total
  stillness.
- Cuts and entrances sit on the beat or on the voice.

## Layout

- **Safe area:** landscape keeps 8–10 % of the width clear on each side. Vertical keeps content
  inside x 8–92 %, y 12–78 % — platform UI covers the top and bottom.
- **Grid:** pick 2–3 x positions (left edge, centre, 60 %) and reuse them. Left-align text
  blocks; centre only short titles.
- **Whitespace** is the cheapest design. One element per scene is fine.
- **Rhythm:** line height 1.05–1.15 for big titles, 1.2–1.35 for body; gaps between groups twice
  the line gap.

## Type

- One family, two at most (display + text). Ship the font files and check they cover every
  glyph in the copy.
- **Sizes:** hero 140–200 px, title 96–120, subtitle 44–56, body 44–60, caption 28–34. Never
  below 28.
- **Weights:** titles 600–800, body 400–500. Letter-spacing −1 to −3 px on big titles, +2 to
  +6 px on small all-caps labels.
- At most ~8 words a line and ~3 lines a card. Numbers that count use tabular figures so the
  digits don't jiggle.

## Colour

- A background, a foreground, one accent, one or two supporting tints. Use the brand's exact
  values from its CSS or brand kit, never "close enough".
- Body text at least 4.5:1 contrast against what is behind it — check mid-transition stills
  too, where text crosses busy backgrounds.

## Motion

| Easing | Use |
|---|---|
| spring 300 / 26 (`spring(s, 300, 26)`) | UI-like, tiny overshoot: cards, buttons |
| spring 150 / 18 (default) | friendly, noticeable: titles |
| spring 220 / 12 | playful bounce; use rarely |
| ease-out expo | fast, then settles: slides, counters |
| ease-in-out cubic | camera moves, morphs, draw-ons |
| ease-in cubic | exits |

- Enter from a short distance (40–120 px) with opacity 0 → 1. Exit faster, to a shorter
  distance or just opacity.
- Stagger related items 60–120 ms; words 40–70 ms; letters 20–40 ms.
- Animate transform and opacity. Animating font size, width or layout jitters.
- Scale from 0.9–0.96, never from 0. Rotation within ±6°.
- One focal movement at a time; secondary elements move less and later.
- Ambient loops (a drifting background, a breathing glow) are long (6–12 s) and small.
- Carry something across a cut — a shape, a colour, a word — so scenes feel like one piece.

### Recipes

- **Word-by-word title:** split into word spans, stagger a small upward spring per word (the
  template does this).
- **Counter (0 → 12,480):** ease-out expo over 1.2–1.8 s, thousands separators, tabular figures,
  right- or left-anchored so the width change doesn't shift it.
- **Draw-on line or underline:** SVG path with `pathLength="1"` and `stroke-dasharray="1"`;
  animate `stroke-dashoffset` from 1 to 0.
- **Growing bar:** animate width or `scaleX` from a hairline, ease-in-out, with the value label
  arriving just after the bar settles.
- **Simulated tap:** scale 1 → 0.94 → 1 over ~0.2 s, plus a ripple or state change right after.
  A cursor that travels to the button first sells it.
- **Typing:** reveal characters at 25–40 per second with a blinking caret; pause briefly on
  spaces for a human feel. Use a seeded random for the jitter.
- **Masked reveal:** text rises from behind a clipping edge (`overflow: hidden` on the line)
  instead of fading in.
- **Transition between busy layouts:** old content out, then new content in (stagger), or dip
  through the background colour. Never a straight crossfade of two full layouts.

## Tones

Presets are defaults; freeform direction ("a 2016 startup launch, played straight") refines or
overrides them.

| Tone | Feel | Pacing and transitions |
|---|---|---|
| `default` | punchy, playful, clean | 4–5 scenes; soft transitions |
| `polished` | serious, elegant, restrained | 3–4 scenes, long holds; soft fades |
| `parody` | deadpan startup launch, played straight | 4–5 scenes, one claim each; hard cuts |
| `chaotic` | FAST, LOUD, ALL CAPS | 6–8 scenes, some under 2 s; flash and zoom cuts |
| `deadpan` | calm, dry, nothing is a joke | 3–4 scenes, big empty space; slow fades |
| `cinematic` | trailer scale, epic claims | 4–5 scenes, big type; dramatic wipes |
| `app-store` | clean feature cards | 4–6 scenes; smooth slides |

## Sound

- **Choose it first** when the cut follows it; put cuts on downbeats and phrase changes, small
  accents on off-beats.
- **One piece:** effects in the music's key and room. A click, whoosh or pop sits 10–15 dB under
  the music; repeated ones (every word, every card) quieter still.
- **No harshness:** short fades (5–20 ms) on every sound so nothing clicks; low-pass anything
  bright that repeats.
- **Ending:** the music resolves or fades with the last frame — never cut off mid-note.
- **Loudness:** `render.mjs` normalises to −14 LUFS integrated with a −1 dB true-peak ceiling,
  which suits every major social platform. Broadcast is −23 LUFS; re-run ffmpeg's `loudnorm`
  with `I=-23` if the user needs it.
- With a voice-over, the music ducks 8–12 dB under speech.
- Only use music the user owns or that is licensed for this use. Making it in the page with
  `OfflineAudioContext` (see the template) is always safe.
