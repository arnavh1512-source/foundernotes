# FounderNotes production route: stick-animation core

Owner direction, 2026-11-17: use FounderNotes to its full extent, use stick animation as the core, and always compare with the reference set including Alan Becker. This means using the relevant established tools together and carrying evidence between them. It does not mean forcing every catalog style into a single film or claiming optional engines are installed.

## Existing capabilities and their roles

| Stage | Existing repo components | Required output |
| --- | --- | --- |
| Research and references | `research_gateway.py`, reference learnings, `docs/ALAN_BECKER_STUDY.md`, `docs/REFERENCE_REVIEW.md` | Source register with actual access scope and limitations |
| Viewer and evidence preparation | `viewer_first_gate.py`, viewer-value tools, viewer-first template | Specific learning promise, evidence and opening insight before a new script |
| Script and spoken delivery | Humanizer guidance, voice casting, `narrate.py`, episode-specific VoiceStudio/ElevenLabs adapters | Actual approved voice takes and measured timings; no silent voice substitution |
| Acting and visual direction | Stickman craft docs, animation-craft, motion-design, Huashu grammar, animation catalog | Original stick cast, pose sheet, contact states and one coherent storyboard |
| Character implementation | Existing motion engine/HTML render contract; reusable SVG character/parallax concepts from `painted-character-motion` where appropriate | Original time-driven stick performance; painted character defaults do not override the new core |
| Supporting explanation | Relevant native styles, diagrams and cleared background tools | A demonstrably clearer mechanism, not arbitrary style changes |
| Picture rendering | `.claude/skills/motion/scripts/render.mjs`; registered external/import route only when available | Real clips at the measured narration duration |
| Sound, captions and assembly | `assemble.py`, sound-design/listening guidance, licensed SFX route | Reviewed narration/mix and readable synchronized captions |
| Technical inspection | `review_frames.py`, `lint_scenes.py`, `qc_video.py` | Decoded frames and measured reports; no inferred artistic pass |
| Creative revision | `studio_loop.py` reference / learn / produce / critic / revise | Findings tied to the exact render and a new review after changes |
| Persistent learning | `record_lesson.py`, creative-knowledge export, skill evaluation, production ledger | Verified defects; untested reference patterns labeled hypotheses |
| Packaging and growth | `.claude/skills/claude-youtube/` (hook, seo, metadata, thumbnail, shorts, analyze) after picture and narration lock | Hook variants, titles, description, tags, chapters, thumbnail brief, Short plan |
| Delivery | `package_lint.py`, delivery-package guidance | Approved video and the required accompanying package |

Use the approved narrator policy in CLAUDE.md if an older supporting document suggests a different voice. Use the stick-core rule if an older visual recipe suggests a different main character style. Optional tool licenses and runtime checks still matter.

## Actual execution in this session

- Initialized `studio_loop.py` for `philosopher-stick-pilot`, with a three-cut budget.
- Ran its `retrieve` operation for Alan's principles tutorial. The saved response reports Agent-Reach `NOT_INSTALLED`; the previous official installer failed on DNS. Actual caption/metadata reading used host web tools.
- Submitted one transcript-scope reference about the anticipation chapter at its published 2:07 chapter marker. The marker locates a chapter, not a frame that was watched.
- Submitted one original application via `learn`: establish a grip and planted stance before a gate effort. Exported it to `.claude/memory/creative-knowledge/` as a hypothesis.
- The workflow packet now reports stage `production`, revision 1, **zero renders and zero critiques**. This stage name permits preparation; it is not a passing viewer-first plan, a rendered pilot, approval or publication.
- Ran `review_frames.py` against the actual prior Cut 3a H.264 file and inspected decoded stills at 3.5, 7.7, 12.7, 17.0 and 22.8 seconds. Source SHA-256: `e6b174358ac802132ad7523d1bbfb77d6dadbc86d6d8cf487b49f0de48fccabf`. The report keeps `creative_approval: false`.
- Queried the backend capability registry for characters. It lists Remotion, Synfig and the bundled optional character source; it does not establish installed runtimes.

## Current runtime blockers

| Dependency | Observed state | Consequence |
| --- | --- | --- |
| Python, Pillow, FFmpeg, FFprobe | Used successfully for the prior study and/or decoded frame review | Local craft tests and encoded-frame inspection work |
| Playwright / playwright-core | Module resolution unavailable in tested Node contexts; local npm cache query returned no matching package | Standard HTML renderer cannot yet run here |
| VoiceStudio at `127.0.0.1:3900/profiles` | Loopback request failed | Live dialogue synthesis was not run |
| Agent-Reach | Not installed; official install failed on DNS | Retain actual authorized fallback and access limitations |
| Reference video playback | Not verified in this study | Motion/voice/sound reference criteria stay pending |

Do not evade a platform verification page, replace the narrator, label the Pillow experiment as the normal production backend, or generate mock evidence to make a stage pass. The next concrete target is a small original stick-performance exercise, then a genuinely narrated 60-90-second pilot once its dependencies and preparation are ready.

## Resume the existing loop

Preserve the episode's `workflow.json`, evidence files and media under its existing studio-output folder. Use `packet` to inspect the actual state. On a fresh machine initialize a new episode and register the accessible sources honestly; do not paste an old approval or invent missing renders. Read the standing mistakes file and reference study before each scene assignment.

The owner request authorizes continuing this work, but the documents and coordinator are not a continuously running video-generation service. Report concrete blockers and unresolved review criteria without disguising them as successful automation.
