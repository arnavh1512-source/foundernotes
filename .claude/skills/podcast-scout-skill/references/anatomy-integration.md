# Anatomy technical-figure integration

**Upstream:** [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy), MIT (Copyright (c) 2026 Ryan). Inspected 10 November 2026. Requires Node.js **20.10+** for its kit and Chrome/Chromium for browser previews. Upstream offers isometric SVG geometry, optional WebGL effects and beta 3D figures, with geometry-audit tools for selected examples.

## Fit for Founder Notes

Anatomy's key strength is **making a recognizable real apparatus explain a mechanism**. Consider it for a single explanatory passage about a supply-chain bottleneck, an engineering constraint, a queueing system, a machine, a feedback loop or a technology trade-off. It should not take over every chapter or replace documentary proof. A symbolic scene must be disclosed as an analogy, not passed off as real footage.

**Why the integration is opt-in:** the upstream skill generates interactive SVG/HTML/React figures and screenshots. It is not a frame-accurate video engine. Its `scripts/capture.mjs --times` captures **wall-clock delays**, not deterministic timestamp-driven frames. Its `scripts/drive.mjs` can play interactions and inspect states, but that does not supply guaranteed 30-fps MP4 rendering.

## Install and preview (owner approval first)

Anatomy is **not included** in FounderNotes. If the owner authorizes installation, place an independently reviewed checkout at `~/studio-tools/anatomy` or point `FOUNDERNOTES_ANATOMY_HOME` to it. Follow its upstream `SKILL.md` for authoring and audits. No installation is performed by the local bridge.

From the FounderNotes repository root:

```bash
python3 .claude/skills/animation-styles/scripts/animation_library.py --show anatomy:provider
python3 .claude/skills/podcast-scout-skill/scripts/anatomy_backend.py status

# For a newly created, locally authored and reviewed figure only:
python3 .claude/skills/podcast-scout-skill/scripts/anatomy_backend.py still \
  studio-output/pilot/scenes/mechanism/index.html \
  studio-output/pilot/looks/mechanism-preview.png \
  --width 1920 --height 1080 --theme light
```

The original bridge accepts existing local `.html` or `.svg` sources and writes only a **new PNG**. It refuses upstream demo sources and existing output files, validates requested dimensions and verifies PNG output. Its `status` only checks that the separate library and Node binary are present; **Chrome/WebGL/rendering remain unverified until a real capture**. It never executes installers, arbitrary build scripts, remote URLs or publishers.

**Security:** Even local HTML may execute JavaScript or fetch external resources inside Chrome. Only capture fully reviewed, trusted, newly authored sources; the browser is not a network sandbox. If the example's features need additional packages, check those requirements and ask before installing.

## From figure to timed video

1. Research and fact-lock the explanation before any scene geometry; choose a mechanism based on actual script claims.
2. Build a physical layout, all moving parts and readouts from **one consistent state model**. Use upstream geometry and line checks where supported; not all build scripts support `--audit`.
3. Inspect 1× and detailed zoom stills, interactions, idle poses, missing-WebGL behavior and mobile legibility with the upstream tools.
4. Create a separate **owned time-stepped scene** implementing deterministic `seek(t)` or `renderAt(t)`, with every pose and number reproducible from time. Translate pointer interactions into planned shot actions, **not live mouse movement captures**.
5. Render a silent scene with the established FounderNotes renderer; align to the measured `narration/timings.json` and final 1920×1080 / 30-fps export rules.
6. If deterministic adaptation is impractical, include the vetted PNG as an intentional static frame in an existing motion clip. Do not claim the interactive upstream page is now a full film renderer.
7. Inspect first/mid/last frames and transitions. Require normal source/rights review, `lint_scenes.py`, `assemble.py`, `qc_video.py`, listening and independent reality-checking before delivery.

## Licenses, limits, and ownership

- MIT applies to upstream Anatomy source and docs; preserve its license/copyright when reusing source. The new FounderNotes integration contains **only independently written guidance and a Python adapter**, not redistributed upstream kit/media.
- Its optional 3D is beta. A still-preview command is not a geometry audit, scene animation, or evidence that it works on a user's machine.
- Keep current **Opus, Sonnet and optional Haiku** agent roles, primary male Voicebox narrator, optional synthetic dialogue cast, manual publishing and paid-tool approval gates.
- Evaluate it in the skill ledger as `external/anatomy` only with witnessed results, not because the GitHub README or mocks suggest quality.
