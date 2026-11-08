# FounderNotes 2.0 — Motion direction and continuous improvement

Status: DESIGN PROPOSAL. This document does not claim the new rendering pipeline or its evaluation gates are implemented.

## Source research ledger

Study upstream code, examples, tests, output clips, dependencies, and licensing before adapting techniques. Pin a commit SHA and retain source attribution for each adopted technique.

| Upstream | Mechanisms to benchmark | What not to assume |
| --- | --- | --- |
| bangtutorial/bang-motion | continuous world/camera, subject persistence, style briefs, deterministic HTML timelines, frame snapshots | a large style menu guarantees good storytelling |
| Alisa0808/vox-director | beat-map approvals, style bake-offs, keyframe-first collage, layered assembly, audio mix | AI image-to-video preserves factual details and continuity |
| alchaincyf/huashu-art-motion | art-specific motion grammar, parameterized explainer segments, beat-grid audio, motion/QA analysis | automated motion scores equal viewer engagement |
| cloveric/claude-drawing-skill | deterministic procedural art, stage-by-stage draw-on, composition and visual revision loops | still-image quality automatically translates to motion quality |
| XiaoyeCodes/code-animation-prompts | searchable style references, deterministic renderAt(t), per-style references and license tracking | all prompts or assets have identical reuse permissions |

Reference repositories are not copied wholesale. Inspect upstream licenses at the exact pinned revisions and record third-party asset restrictions.

## New directing contract

No old preset is the default. For each video, the director produces a **visual thesis** describing what the viewer should understand or feel. For each narrative beat, the plan must specify:

- narration word/time anchors, factual claim and evidence ID
- narrative purpose: reveal, compare, cause/effect, scale, tension, reaction or reset
- subject, spatial continuity, camera path, foreground/midground/background
- selected motion grammar and reason for choosing it
- style references and source/asset provenance
- expected visual change and sound event, with exact frame/time boundaries
- fallback if an asset or model fails, with no unapproved replacement footage

A scene may be still when a deliberate hold communicates something; anti-slideshow heuristics are diagnostics, not a mandate for constant motion.

## Production architecture

1. **Research + fact lock:** source-verified claims, uncertainty and visual evidence requirements.
2. **Narration lock:** prefer the currently working Voicebox route; measure synthesis time, dropped words, pacing, pronunciation and ASR alignment before selecting another engine. Never infer quality from speed alone.
3. **Beat director:** generate 3 structurally different visual treatments for one representative beat; human approves a direction before full production.
4. **Style/technique retrieval:** choose by narrative function, not random rotation. Keep separate registers for licensed source code, visual reference only, and generated assets.
5. **Shot graph:** persistent subject IDs, continuity constraints, deterministic timestamps, audio cues and edit decisions in one machine-readable manifest.
6. **Render:** combine deterministic HTML/SVG/Canvas, procedural drawings, collage layers and permitted generated assets; enforce reproducible time seeking.
7. **Automated QC:** sample boundaries and every planned event, decode media, validate timing, detect black/solid frames, corrupted media, clipping, dead air, missing captions and mismatched aspect ratio.
8. **Independent creative review:** an agent that did not create the scene critiques clarity, composition, repetition, visual fidelity, pacing and whether motion serves the spoken claim. Human approval is mandatory for the first pilot.
9. **Postmortem:** persist per-shot failures, root causes, fixes, before/after examples, and regression checks. Only promote a technique to the approved library after a successful benchmark.

## Multi-agent assignment

Use Claude Sonnet at medium effort for researcher, motion-director, style researcher, storyboarder, scene builders, sound editor and independent critic. Assign each agent bounded inputs and structured outputs. A different agent must inspect the rendered result. Agent labels alone do not constitute a functioning workflow.

## Required machine-readable artifacts

- `production/beat-map.json`: beats, factual claims, time anchors and visual purpose
- `production/shot-graph.json`: shot IDs, asset refs, camera, animation, timing and transitions
- `production/asset-manifest.json`: provenance, licenses, generation details and hashes
- `production/qc-report.json`: technical failures, measured metrics and inspected frames
- `production/creative-review.json`: scored criteria with evidence and timecodes
- `production/lessons.json`: error signature, root cause, fix, regression test and next-video status

These are target contracts, not existing files.

## Pilot acceptance gates

Before replacing the current production system, create one 30–60-second narrated pilot containing at least three distinct narrative functions. Approve its beat map and style bake-off; render reproducibly twice; verify audio/video synchronization and all transitions; inspect at 0.25×, 1× and without audio; and compare against a current FounderNotes sample. Do not declare a visual improvement without a human side-by-side review. Track editing time, failed renders, QC defects and reviewer preference.

## Learning loop

After each published video, collect viewer retention only when analytics are available, alongside qualitative feedback and production defects. Separate audience response from visual craftsmanship; views depend on topic, thumbnail, distribution and many other factors. Update technique selection and tests, never silently rewrite past approvals. Each future video reads the approved lessons before planning.

## Implementation sequence

A. Pin and inspect the five upstream repositories (including runnable examples and licenses).
B. Prototype shot-graph + one technique from each source on the same narrated beat.
C. Implement deterministic preview, frame/audio QC and independent review.
D. Run a full pilot, compare outputs and document failure modes.
E. Promote proven techniques into the studio; retire the old default only after the pilot passes.

The existing repair branch remains unmerged until current CI checks and new integration tests pass.
