---
name: motion
description: "Make a motion video — ad, promo, launch video, explainer, kinetic type, data animation, social clip, title card, logo sting, lower third — and render it to MP4 with the tools on the machine (Chromium + ffmpeg by default). Identifies the product and picks the style that fits it, then covers the brief, a rough draft before the polish, design rules that keep it from looking generated, sound, a check loop that looks at real frames, and delivery. Use when the user says \"/motion\", \"make a video\", \"motion video\", \"make an ad\", \"launch video\", \"animate this\", \"promo\", \"reel\", \"explainer\", or wants to show off a project or website in a video.\n"
---

# /motion

One skill for every kind of short motion video. You make the whole thing — story, visuals,
sound, render — and you check it with your own eyes (stills and contact sheets) before the user
sees it.

Usage: `/motion [what] [options]`. Options can be flags or plain language:

| Option | Default |
|---|---|
| `--kind ad\|launch\|explainer\|data\|kinetic\|social\|sting\|lower-third` | inferred from the request |
| `--format landscape\|vertical\|square` | `vertical` (1080×1920) for ads and social, `landscape` (1920×1080) otherwise; 30 fps |
| `--duration <s>` | 15 s for ads and social, 20 s for launch, 30–60 s for explainers |
| `--style <name>` | picked from the product; see `references/styles.md` |
| `--tone <preset or freeform>` | inferred; see the tone table in `references/craft.md` |
| `--engine html\|fframes\|remotion\|manim` | `html` (see **Engines**) |

`what` can be a product or brand, the current project, a website URL, a script, a CSV, or just
an idea.

Write everything to `motion-output/<slug>/` in the current directory: `video.mp4`, `poster.jpg`,
`plan.md`, `share-copy.txt`. Keep sources, frames, downloads and stems in its `work/` subfolder.
`motion-output/` is gitignored.

Files in this skill:

| File | Use |
|---|---|
| `scripts/render.mjs` | renders a time-driven HTML page to MP4, stills, or a contact sheet |
| `scripts/setup.sh` | installs what rendering needs (Playwright, Chromium, ffmpeg) if missing; run first |
| `scripts/check.sh` | reads the real spec of an MP4 and flags frozen stretches and black frames |
| `assets/template.html` | starting page that already follows the render contract |
| `references/craft.md` | pacing, layout, type, colour and motion numbers; tones; recipes; sound |
| `references/kinds.md` | what each kind of video needs: shape, length, format, traps |
| `references/styles.md` | identify the product, then pick the style that fits it |

## 0. Setup — before the first render

Set `S` to this skill's `scripts` folder (locally `.claude/skills/motion/scripts`; in a cloud
session, wherever the skill was mounted: `find / -path '*motion/scripts/render.mjs' 2>/dev/null`).
Run `bash $S/setup.sh` once per machine or session. It installs only what is missing and prints
`ready to render` or the exact `MISS` lines. Cloud sessions start without `node_modules`, a
browser or ffmpeg, so always run it there. If something stays missing (no network, no root),
tell the user which line failed and keep going with the brief and the HTML draft; the page can
still be previewed in a browser and rendered later.

## 1. Brief

Find out what you are making before you draw anything. Read `references/kinds.md` for the kind
you are making.

**Gather the material.**

- **A project (no input, or "this"):** read the main page, styles (exact colours and fonts),
  README and key components. Find the product *in use*: entry → key action → result. You have
  the source, so reuse its real components, CSS, fonts and images in the video instead of
  redrawing them.
- **A website:** load it in headless Chromium (a plain fetch often returns an empty JS shell),
  dismiss overlays, scroll section by section. Take the headline, feature names, calls to
  action, exact colours from the CSS, the fonts it loads, the logo and product images. Reuse
  its markup and assets rather than panning over flat screenshots.
- **A brand or product with no source:** use what the user gives you and what is public. Never
  invent numbers, prices, quotes, testimonials or features.
- **Data:** read it, find the one comparison worth animating, and keep every number exact.

Skip build output, lock files, `.git/`, `.env*`, keys, credentials and anything gitignored for
those reasons. Nothing secret or personal goes into the video or share copy — no tokens,
internal URLs, real customer names or emails. If real UI shows such data, swap in plausible
fictional stand-ins and say so in the plan.

**Answer these before planning:** What is it, in one sentence? Who watches this, and where (the
platform decides format and length)? What is the one thing they must remember? What is the hook
in the first 2 seconds? What real thing should be shown? What tone fits? What do they do after
watching (the call to action)?

Ask the user only for what is missing *and* matters (a logo file, a price, a deadline). Default
the rest and say what you assumed.

**References beat guesses.** If the user shares example videos or images, they define the style:
study them first (step 2). If the request is vague about the look, the style is still not a
guess — it comes from the product in step 2.

**Real brands.** A video for a brand the user does not own (a "Spotify ad", a "Nike promo") is a
spec or concept piece. Make it, keep it a local file, and say it is unofficial. Do not publish it
anywhere as if the brand made it, and do not make it look like an official announcement of
something that did not happen.

## 2. Pick the style

Read `references/styles.md`. Identify the product — category, audience, personality, the
assets that exist, the platform — and map it to a style, then apply the modifiers (missing
assets, brand personality, platform, mixing, references). Mixing styles across scenes is
encouraged when palette, type, tempo and carry-overs hold it together. Tell the user the style
or mix you picked, why, and two alternatives before building. If they seem unsure, show one still per candidate.

## 3. Plan

Write `plan.md` (with the product identification and the chosen style at the top): the angle, the hook, 2–3 highlights, the ending and call to action, the tone,
the palette and type, and a scene-by-scene storyboard with durations that sum to the target.
For each scene name what enters, how it moves, and what carries over the cut.

**Default shape:** Hook (≤2 s) → Reveal (2–4 s) → 2–3 sharp highlights → Ending / CTA (2–4 s).
It is a starting shape, not a template.

If the video is cut to music or a voice, choose the sound first: its tempo and phrases set the
timing of everything else.

## 4. Draft first

Before any polish, build a **rough draft** of the whole video: black and white, one system font,
flat boxes standing in for images, one simple move per scene, correct timing. Render it with
`--draft` and look at the contact sheet.

The draft answers the questions that polish can hide: does the hook land in time, is every line
on screen long enough to read, does the story make sense to a stranger, is anything doing
nothing? Fix the plan here, where changes are cheap. Then build the real thing on top of the
same timeline.

## 5. Build

### The render contract

The default engine is a single HTML page drawn by Chromium and captured frame by frame. Start
from `assets/template.html`. The page must:

1. Set `window.MOTION = { width, height, fps, duration }`.
2. Define `window.seek = async (t) => { … }` that draws the exact frame at `t` seconds. **Every
   frame is a pure function of `t`**: no `Date.now()`, no `requestAnimationFrame` clocks, no CSS
   transitions or `@keyframes` left running, no `Math.random()` without a seed. The same `t`
   must always give the same pixels, or frames will jitter and stills will lie.
3. Optionally define `window.motionAudio = async () => base64Wav` to make the soundtrack in the
   page itself with `OfflineAudioContext` (the template shows how).

`render.mjs` waits for fonts and images, then calls `seek` for every frame. Ship fonts and
images as local files next to the page or as data URIs; a CDN that fails at render time gives
you fallback type in the final video.

Open `?t=4.2` in a browser to see any moment; the template supports it.

### Rules that keep it from looking generated

- **Show the real thing.** Real UI, real copy, real product, real numbers. Rebuild only what you
  cannot reuse. Never abstract filler (floating blobs, generic gradient orbs, stock icons with
  no reason).
- **Specific.** Ask: would this video still work for a different product with only the text
  changed? If yes, change the idea, not the colours.
- **The hook is everything.** The first frame already shows something — no fade from black.
- **Readable.** A line meant to be read stays fully settled for about 0.3 s per word plus 1 s,
  counted from when it is all on screen. Pace comes from motion and cuts, not from pulling text
  away early.
- **Alive.** Things appear one by one, react to each other, get typed, clicked, swiped. During a
  hold something small still moves. A scene where one thing fades in, sits and fades out is a
  slide, not motion.
- **Not one motion for everything.** Vary entrances by what the element *is*: text rises, a
  card slides, a line draws on, a number counts up, a button gets pressed.
- **Beat discipline.** Small things land on beats (a word, a stroke, a spark). The whole frame
  changes only at a few cuts. No shaking or flashing on every beat.
- **Little text, and human.** Banned unless asked: "Introducing", "Unleash", "Seamless",
  "Next-level", "Streamline your workflow", three-word taglines ("Fast. Simple. Powerful.").
  Write on-screen text the way a person would say it.
- **Every frame postable.** Any frozen frame should be worth sharing.
- **Funny earns its place.** Humour comes from the subject's own absurdity, never from trying.

Numbers for pacing, safe areas, type sizes, easing and staggers are in `references/craft.md`.
Use them.

### Sound

Write music and effects as one piece: effects in the same key and the same space as the music,
sitting softly under it, nothing harsh, repeated little sounds kept in the background. Use the
user's track if they give one. Otherwise make it yourself in the page (`motionAudio`) or with
ffmpeg — `references/craft.md` has the mix targets. A silent video is acceptable only when the
platform plays muted by default *and* the user agrees; say so if you ship it silent.

## 6. Check

You cannot watch the video, so turn it into things you can read. Look at the PNGs before you
say anything looks right.

```bash
S=.claude/skills/motion/scripts   # or wherever this skill lives
node $S/render.mjs work/index.html --stills 0,1,2.5,5,9 --out work/stills   # PNGs + sheet.png
node $S/render.mjs work/index.html --sheet 12 --out work/stills             # 12 evenly spaced frames
node $S/render.mjs work/index.html --draft --out work/draft.mp4             # half size, 15 fps
```

1. Stills from every scene **and from mid-transition**. Fix overflow, text cut by the edge,
   collisions, low contrast, fallback fonts, missing images.
2. A crossfade between two busy layouts makes a muddy double exposure. Stagger it (old out,
   then new in) or dip through the background.
3. Check every readable line against the reading-time rule using the storyboard times.
4. After the full render, run `bash $S/check.sh video.mp4 1080x1920 30`. It asserts the spec,
   lists frozen stretches longer than 1.5 s (a dead hold) and black frames (a fade from black
   at the start breaks the hook), and writes a contact sheet of the encoded file.

Repeat until a contact sheet shows nothing you would fix.

## 7. Render and deliver

```bash
node $S/render.mjs work/index.html --out video.mp4 --poster 6.5
```

- **Poster.** `--poster <t>` makes frame 0 a copy of the strongest *settled* frame (text fully in,
  not mid-transition) so every platform's thumbnail shows it. It replaces frame 0 instead of
  adding one, so duration and audio sync stay the same. Save the same frame as `poster.jpg`
  (`--stills <t>`).
- **Transparent output** (lower thirds, overlays): `--alpha` renders a ProRes 4444 `.mov` with a
  transparent background. The page must not paint its own background.
- **`share-copy.txt`:** 1–3 sentences, postable as is, specific, in the video's tone. No
  "excited to share".
- **Tell the user** where the files are, give one sentence on the creative angle, and offer to
  re-roll a scene, try another tone, or cut another format (vertical ↔ landscape ↔ square).

## Engines

`html` (default) covers almost everything: CSS, SVG, Canvas 2D, WebGL and Three.js all render in
the same page under the same contract. Pick another engine only for a reason:

| Engine | Pick it when |
|---|---|
| `fframes` | the user wants Rust, the video is long, or render speed matters. Rust + SVG, GPU rendered, with its own `inspect`, `strip` and `preview` commands. Install its skill with `npx skills add https://fframes.studio`. |
| `remotion` | the project already uses React and Remotion, or the user asks for it |
| `manim` | maths and diagrams that need exact geometry and LaTeX |

Interactive motion *websites* (scroll-driven, pointer physics) are not videos; build the page
for real, then record a scripted pass through it with this skill's renderer if a video is also
wanted.

Whatever the engine, the brief, draft, rules, check loop and delivery above still apply.

## Sources

Distilled from six open-source projects; see `NOTICE.md` for what came from where and their
licences.
