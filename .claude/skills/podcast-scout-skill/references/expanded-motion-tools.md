# Extended animation tools — source study and selection contract

The new sources supplement the **17 native style references** and the existing production stack. A source repository is not an automatically installed engine or a passed render test. Check actual upstream revisions, installation requirements, software and asset licenses before copying, executing or commercially publishing its outputs.

## Verified upstream descriptions (README-level review)

| Source | Distinct contribution | Routing recommendation | Constraints |
|---|---|---|---|
| [HeyGen HyperFrames](https://github.com/HeyGen-com/hyperframes) | HTML to deterministic video oriented to agents; frame control and component techniques | HTML-based explainers, diagrams, typography and UI actions | Apache-2.0; Node >=22 per README; test alongside bundled motion bridge |
| [OneTake](https://github.com/feitangyuan/onetake) | One continuous evolving camera world, measured shot continuity | Learn transition planning and continuity measurement | **PolyForm Noncommercial** public license: DO NOT copy or embed code for the monetized channel without separate commercial rights; original implementation only |
| [gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) | Metaphor → still approval → generated layered collage B-roll, frame checks | Short editorial collage inserts with a strong concrete metaphor | Paid Gemini generation and image-gen dependency; ask before spending; independent asset rights review |
| [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | Original hand-painted animated-character production | Recurring acting and emotional performance | Make original characters; already included in studio catalog |
| [Lemo Opuscar](https://github.com/lemomo-ai/lemo-opuscar) | Code-made film structures, style examples, instrument/foley/audio methods | Learn directing/score and reusable QC methods | Model/sample-specific licenses and attribution; already listed in stack |
| [p5.brush](https://github.com/acamposuribe/p5.brush) | Pencil/charcoal/watercolor/hatching and seeded organic strokes | Painted plates, drawn-on explainer layers, controlled hand-made textures | WebGL2 requirements, test standalone/p5 builds and reproduce frames |
| [OpenToonz](https://github.com/opentoonz/opentoonz) | Full 2D animation desktop production suite | High-touch drawn animation and complex ink/paint | Not a Claude skill/drop-in CLI; require separate install, export tests and licensing checks |
| [Synfig](https://github.com/synfig/synfig) | Vector/bitmap rigged 2D animation | Bone rigs and reusable animated characters | Separate application; verify headless CLI and exported frame rate locally |
| [Pencil2D](https://github.com/pencil2d/pencil) | Traditional hand-drawn bitmap/vector animation | Frame-by-frame sketches and character acting | Separate desktop tool; validate actual export behavior locally |
| [Vox AI Motion Graphics Generator](https://github.com/Anil-matcha/vox-ai-motion-graphics-generator) | End-to-end editorial collage pipeline, beat maps and animation | Reference for bundled collage-director skill, not duplicate installation | Dependency/API costs, source/license and asset checks |
| [PixelFX](https://github.com/patch-gg/pixelfx) | Procedural pixel art effects, animated action posing and refinement | Pixel-art inserts, UI feedback, game-world metaphors | Rebuild only suitable effects; visual readability and no excessive spectacle |

## Technique decision rules

- Start with *what changes in the viewer's understanding*, not the prettiest sample. A frame without a new fact, causal step, emotional turn or reveal is candidate filler.
- Prefer one **coherent world and persistent subjects**; style switches must have a motivated transition or explicit chapter break.
- Use HyperFrames and existing motion bridge for tests of reproducible HTML scenes; compare actual output quality and tool overhead on the same narrated beat. Pick one primary exporter to reduce format bugs.
- Use OneTake's conceptual continuity methods, not restricted licensed source code, for commercial videos.
- For collage treatments, follow a treatment → keyframe → motion approval gate. Do not buy credits or use generated reference art without explicit owner approval.
- For drawing suites, export silent shot clips at the **measured** narration duration, consistent dimensions/frame rate and asset IDs, then normalize during assembly.
- Combine painted plates and particle effects sparingly; texture is not a replacement for explanation or acting.
- Use PixelFX selectively in pixel-art sequences, not as random explosions in factual videos.

## Required bake-off (not yet performed)

Render the *same* 8–12 second narration beat with two to three appropriate approaches; collect first/mid/last and boundary frames, actual frame-step repeatability, source/license manifest, render time, cost, typography/safe-zone, character continuity, and independent creative judgment. Then run one 30–60 second narrated pilot before calling any new engine production-ready. Record observed facts separately from expected capabilities.
