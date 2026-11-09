---
name: raea-renderer
description: Optional local GPU render and visual-quality backend for FounderNotes. Use when a scene needs TypeScript/React motion graphics, composited media or 3D and the owner has installed the raea engine. Never replace the studio's fact lock, voice, or film QC.
---

# Raea — optional FounderNotes renderer

Use the independent [shinyobjectz/raea](https://github.com/shinyobjectz/raea) (**Render Anything Engine**) as one optional scene exporter within the FounderNotes studio, never as a replacement for the eight-agent pipeline. Its actual engine is **not included in this repository**. The studio's original [raea backend script](../podcast-scout-skill/scripts/raea_backend.py) calls the installed CLI in a controlled, offline-first way.

**License and readiness:** Upstream engine is *Functional Source License 1.1 with Apache-2.0 conversion two years after each release*, not MIT or standard Apache-2.0 today. Its terms prohibit competing commercial products/services. Creator video production may qualify, but check your specific business use and the current upstream terms. Upstream calls its current release **canary** and notes Windows as least tested. We do **not** vendor the engine or promise a production-ready GPU on every host.

For current syntax, prefer `raea help`, `raea guide` and the [official Raea agent skills](https://github.com/shinyobjectz/raea-skills). The upstream agent skill is version-sensitive; use the version distributed with an installed engine, not stale examples. Its agent skills are a separate Apache-2.0 project. This file is a **FounderNotes-specific wrapper**, not a copy of that upstream skill.

## Selection and gate

1. Read `CLAUDE.md`, `channel-profile.md` and `../podcast-scout-skill/references/agency-production-system.md`. Require approved evidence, visual direction, scene continuity and measured narration duration.
2. Choose Raea **only when** a TSX/React or Bevy 3D composition benefits the scene and the owner has explicitly opted into using an installed renderer. Compare with the existing HTML/motion renderer on a representative 8–12-second beat, without assuming the new engine wins.
3. From the repo root, run the backend `status` command. If `RAEA_NOT_INSTALLED`, keep the existing renderer; **do not run a remote installer** or automatically install packages.
4. Develop an original `.tsx` scene from the approved shot plan and narrator timing. Time-driven state should be reproducible; preserve subject/material/camera continuity. Test the first, middle and last frames.
5. Render to a new path under `studio-output/<slug>/scenes/` with a manifest when supported. Review PNG frame stills and transition boundaries before a full export.
6. Run **both** `raea_backend.py check` and FounderNotes `lint_scenes.py` / `qc_video.py` after final assembly; Raea's P0/P1 checks alone do not replace the owner's film standards or independent listening review.
7. Log original source path, output file, actual local engine version, frame rate, dimensions, license/cost decision, CLI command, and QC findings. Evaluate this tool as `external/raea` with real samples in the continuous skill ledger.

## Commands (from repository root)

```bash
python3 .claude/skills/podcast-scout-skill/scripts/raea_backend.py status

# Use for a sample after installing raea and creating these directories.
python3 .claude/skills/podcast-scout-skill/scripts/raea_backend.py frame \
  studio-output/pilot/scenes/01.tsx studio-output/pilot/looks/01-mid.png --frame 45

python3 .claude/skills/podcast-scout-skill/scripts/raea_backend.py render \
  studio-output/pilot/scenes/01.tsx studio-output/pilot/scenes/01.mp4 \
  --manifest studio-output/pilot/scenes/01-render.json

python3 .claude/skills/podcast-scout-skill/scripts/raea_backend.py check \
  studio-output/pilot/scenes/01.mp4 \
  --manifest studio-output/pilot/scenes/01-render.json \
  --report studio-output/pilot/scenes/01-check.json
```

The wrapper refuses to overwrite files, requires directories to exist, does not call a shell, and sets `RAEA_OFFLINE=1` by default. Only use `--allow-network` if the owner explicitly approves necessary remote assets/services. The wrapper cannot guarantee deterministic rendering, artistic quality, hardware support, third-party asset rights or engine compatibility by itself.

If an output contains multiple tracks or unexpected formats, convert and inspect it with established FFmpeg tooling before appending to the scene list. Keep one consistent approved male narrator (the existing Voicebox profile), subtitles and original research provenance. Never imply that installing Raea makes narration or upload automatic.

## Local installation by the owner

Review the official [Raea releases](https://github.com/shinyobjectz/raea/releases) and [install instructions](https://github.com/shinyobjectz/raea#install) before choosing an installer. Windows x86_64 requires appropriate GPU drivers and an up-to-date Visual C++ runtime. The optional engine must be separately installed and tested on the host that runs Claude Code. No production installation has been performed by adding this skill file.
