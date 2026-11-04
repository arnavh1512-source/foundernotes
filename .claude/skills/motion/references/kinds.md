# Kinds of video

Each kind has its own job. Find yours, take its shape and traps into the plan, then follow the
main skill. A request can mix kinds (a launch video with a data beat); use the dominant one's
shape.

## ad — brand or product ad

- **Job:** one viewer, scrolling, decides in 2 s whether to stop. Leave them with one message and
  one action.
- **Shape:** hook (a problem, a surprise, the product doing something striking) → the product
  answering it → 1–2 proofs → logo and CTA held ≥2 s.
- **Format:** vertical 1080×1920 for Reels, TikTok, Shorts and Stories; square 1080×1080 for
  feeds; landscape for YouTube pre-roll. 6 s (bumper), 15 s (standard), 30 s at most.
- **Traps:** the logo first (nobody stays for a logo); claims you can't back; tiny CTA text;
  copy that sits under the platform UI. A brand you don't own is a spec piece — say so.

## launch — show off something built

- **Job:** a stranger understands what it is, who it's for, and how to get it, after one view.
- **Shape:** hook (2–3 s) → reveal the product (2–4 s) → 2–3 highlights of it *in use* → name,
  URL or install command.
- **Format:** landscape 1920×1080 for X, LinkedIn and sites; 18–22 s.
- **Traps:** leading with the tech stack; a landing page instead of the working product;
  invented metrics.

## explainer — teach one idea

- **Job:** the viewer can explain the idea back afterwards.
- **Shape:** the question → the intuition (one picture) → 2–4 steps building on it → the
  takeaway restated in one line.
- **Format:** landscape; 30–90 s. Usually voice-over led: write and time the script first, then
  animate to it.
- **Traps:** text paragraphs on screen; a new visual metaphor every scene (keep one and build on
  it); maths without the geometry (use Manim when the shapes must be exact).

## data — numbers that move

- **Job:** one comparison or trend lands. Every number is exact and sourced.
- **Shape:** the question the data answers → the build (axes, then bars or lines growing) → the
  highlight (one value called out) → the source line.
- **Format:** any; 10–30 s.
- **Traps:** rounding or "approximately" numbers that are known; truncated axes that exaggerate;
  too many series. Read the data file, never retype numbers by hand.

## kinetic — kinetic typography, lyric or quote videos

- **Job:** the words *are* the visual. Timing follows the voice or the beat exactly.
- **Shape:** one phrase per beat group; emphasis words get size, weight or colour; motion follows
  the meaning (a word about falling, falls).
- **Format:** any; the length of the audio.
- **Traps:** the same entrance on every word; text too long to read at the pace; ignoring the
  natural stress of the line.

## social — short vertical clip, TikTok, Reels, Shorts

- **Job:** stop the scroll, keep them to the end, make them comment or follow.
- **Shape:** the payoff promised in frame 0 → fast build → payoff → loop point (the last frame
  leads back into the first so a replay feels seamless).
- **Format:** vertical 1080×1920; 7–30 s. Burn in captions — most people watch muted.
- **Traps:** fade from black; content under the UI (keep inside y 12–78 %); slow starts.

## sting — logo sting, intro, title card

- **Job:** a recognisable brand moment in 2–6 s.
- **Shape:** build-up (shapes, strokes or letters assembling) → the logo resolves → hold ≥1 s.
- **Format:** landscape or square; 2–6 s; often needs `--alpha` for overlay use.
- **Traps:** redrawing a logo you could reuse as SVG; distorting it (never squash, recolour or
  re-letter someone's logo); a resolve that never settles.

## lower-third — name tags and overlays

- **Job:** label a person or topic over other footage without covering it.
- **Shape:** in (0.4–0.6 s) → hold for the reading time → out (0.3 s).
- **Format:** `--alpha` (ProRes 4444 `.mov`) at the footage's size; the page paints no
  background. Sits in the bottom-left safe area.
- **Traps:** a painted background (kills the transparency); text too small for phones; animating
  past the safe area.
