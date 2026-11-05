---
name: design-me
description: 'One-stop design and motion command that routes to 19 specialist skills: podcast-scout-skill (narrated YouTube explainers), extract-design, design-taste-frontend, impeccable, react-bits, transitions-dev, transitions-polish, transitions-ui-generation, the 8 gsap-* skills (core, react, frameworks, scrolltrigger, timeline, plugins, utils, performance), motion, playwright-cli and navigator. Use when the user says /design-me or asks to design, redesign, restyle, clone the look of a site, add animation or transitions, build an animated landing page, make a motion video, or polish and verify a frontend UI. Picks the right skills for the request, runs them in a brief → reference → design → components → motion → polish → verify pipeline, and loads each skill before using it.'
---

# /design-me — design + motion router

One entry point for every design and motion skill installed. Do not do the work from memory:
**load each chosen skill (Skill tool, or read its SKILL.md in cloud sessions) before using it,
then follow its instructions.** The skill's own rules beat anything summarised here.

## 1. Read the request

Take everything after `/design-me` as the brief. If it is empty, ask one question:
what to make (site, section, component, animation, video), for whom, and any reference URL.
Otherwise proceed with sensible defaults and state them.

## 2. Route — pick only what the brief needs

| Need in the brief | Skill(s) |
|---|---|
| Reference URL / "make it look like X" / brand tokens | `extract-design` |
| New page, landing, marketing site, art direction, anti-slop look | `design-taste-frontend` |
| Redesign, critique, audit, polish, harden an existing UI | `impeccable` |
| Animated React pieces (text effects, backgrounds, cursors, reveals) | `react-bits` |
| CSS transitions: dropdowns, modals, toasts, tabs, hovers | `transitions-dev` |
| Tune existing motion to a token scale (duration, easing, blur) | `transitions-polish` |
| AI-generation reveal effects (wireframe scan, dotted text, image reveal) | `transitions-ui-generation` |
| JS animation basics: tweens, easing, stagger, matchMedia | `gsap-core` |
| GSAP in React / Next.js (useGSAP, cleanup) | `gsap-react` |
| GSAP in Vue, Svelte, Nuxt | `gsap-frameworks` |
| Scroll animation, pinning, parallax, scrub | `gsap-scrolltrigger` |
| Sequenced, choreographed animation | `gsap-timeline` |
| SplitText, Flip, Draggable, ScrollSmoother, CustomEase, MorphSVG | `gsap-plugins` |
| clamp, mapRange, snap, interpolate helpers | `gsap-utils` |
| Jank, 60fps, layout thrash, will-change | `gsap-performance` |
| Motion video / ad / launch clip / kinetic type → MP4 | `motion` |
| Educational YouTube video, podcast → explainer, narrated (male voice) long-form | `podcast-scout-skill` (it uses `motion` for scenes) |
| Paper-collage motion graphics, collage explainer/Short, collage B-roll inserts (MuAPI, needs credit) | `collage-director` |
| Named animation looks: Pixel Art, Chalkboard, Glow Sketch, PS2, Comic Art, Flat Vector, line-and-dot minimal, CGI Motion, brick-toy, clay 3D explainer | `animation-styles` |
| Screenshot, click-through, visual check in a real browser | `playwright-cli` |
| Big multi-discipline project needing a specialist-agent plan | `navigator` |

Rules:
- Prefer CSS (`transitions-*`) for simple UI state changes; reach for GSAP only for
  timelines, scroll-driven or physics-heavy motion.
- In React, pair any `gsap-*` skill with `gsap-react`.
- Always finish with `playwright-cli` when there is a page to look at.

## 3. Default pipeline

Run the stages that apply, in this order, and say which ones you are skipping and why.

1. **Brief** — goal, audience, platform, stack (default: the project's stack, else
   Tailwind + plain HTML or Next.js), must-haves, references.
2. **Reference** — `extract-design` on any URL given; reuse its tokens instead of inventing.
3. **Design** — `design-taste-frontend` for new work, `impeccable` for existing UI.
   Lock type, palette, spacing and composition before writing components.
4. **Components** — build; pull animated pieces from `react-bits` where they fit the direction.
5. **Motion** — `transitions-dev` / `transitions-ui-generation` for UI states,
   `gsap-*` for scroll and timelines, `motion` if the deliverable is a video.
6. **Polish** — `transitions-polish` on all motion, `gsap-performance` if GSAP is used,
   `impeccable` polish/audit pass on the whole UI. Respect `prefers-reduced-motion`.
7. **Verify** — `playwright-cli`: screenshot desktop (1440) and mobile (375), check console
   errors, fix what looks wrong, re-shoot. At least two look-and-fix rounds.

## 4. Report

End with: skills used (in order), files changed, screenshots taken, open issues.
