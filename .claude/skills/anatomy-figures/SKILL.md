---
name: anatomy-figures
description: Optional technical-mechanism visual specialist for FounderNotes. Use for original isometric cutaways, working SVG/WebGL machinery and physical analogies after fact-lock and direction; preview via separately installed Anatomy. Retain the studio's voice, model routing and film QC.
---

# Anatomy figures — FounderNotes integration

This is an **original FounderNotes integration**, not a copy of the [upstream Anatomy skill](https://github.com/wheresryan22/anatomy), and **not a video-rendering engine**. Read [the integration guide](../podcast-scout-skill/references/anatomy-integration.md). The upstream engine is not bundled.

Use it **selectively** when a researched concept is better communicated through a **recognizable working physical mechanism**: technology, engineering, a supply chain, an operational feedback loop, mechanical process, or a detailed technical cutaway. Do not make every scene an isometric diagram.

## Responsible production

1. **Director (Opus medium)** selects the mechanism, validates the factual analogy, and records an original visual plan; **animator (Sonnet medium)** authors the figure. Preserve the task-based Claude model routing; do not require unavailable models.
2. Use the approved narration script and actual Voicebox timings; keep the established male narrator and optional approved synthetic character voices. No upstream voice generation or audio replacement.
3. Obtain the upstream Anatomy checkout **separately and only with owner approval**. Read its real `SKILL.md`, `references/craft.md`, `references/motion.md` and `references/verify.md` before creating complex geometry.
4. Author a new HTML/SVG/WebGL figure outside the upstream checkout, based on a real mechanism and a detailed parts list. Facts, numbers, readouts, parts and actions must agree. No copying demo videos or figures as deliverables.
5. Check the optional bridge: `python3 .claude/skills/podcast-scout-skill/scripts/anatomy_backend.py status`. Use its `still` command to capture an original local preview, then **inspect the actual PNG**.
6. **Interactive figure ≠ video.** The bridge cannot export synchronized MP4 clips. To animate the figure in FounderNotes, implement deterministic `seek(t)` / `renderAt(t)` in your **owned scene**, align it to narration timings and render through the established scene pipeline. If not feasible, use the vetted still within a standard animated scene.
7. Review readable poses at 1× and 4×, transitions, lines, depth, camera, evidence, rights and WebGL fallback where applicable. Run `lint_scenes.py`, `assemble.py`, `qc_video.py` and independent reality review. Record only real observed skill evaluations as `external/anatomy`.
8. Do not run unreviewed HTML, install software, access accounts, use paid services or publish without owner approval.

Anatomy's upstream source is **MIT (Copyright 2026 Ryan)**. Keep the MIT copyright and license notice if upstream code is later copied into any deliverable. The local integration currently vendors **no Anatomy code or example media**.
