# FounderNotes production system — specialized crew and animation routing

**Goal:** original, factual, watchable long-form videos for the Founder Notes YouTube channel. This is a directing and review protocol, not proof that every external skill is installed. Reference: [Agency Agents](https://github.com/msitarzewski/agency-agents), MIT. Adopt the **specialist-role, clear deliverable, critic and handoff** pattern; do not copy whole agent personas or inflate the crew unnecessarily.

## Model and session contract

The owner requests **Claude Sonnet 5.5, medium effort** for crew members. Existing Claude Code agent frontmatter uses `model: sonnet` and `effort: medium`; the alias is **not proof of a particular version**. On the actual host, verify Sonnet 5.5 is offered and selected, or explicitly report the model that did run. No tools are granted beyond the host's permitted permissions. One coordinator controls stage handoffs and budgets. Never claim agent execution when only instructions were edited.

## Specialists, inputs and required artifacts

| Specialist | Reads | Writes | Must not claim |
|---|---|---|---|
| Researcher | brief, transcripts, source access | `research/claims.json`, evidence log with URLs/dates/timestamps | fact-checked from snippets only |
| Scriptwriter | approved claims, channel profile | `script/script.md`, spoken word count, claim map | narration duration from guessed words/minute |
| Motion director | locked script, narration timings, style catalog | `production/beat-map.json`, 3 treatments, style justification | art style alone proves story quality |
| Storyboarder | approved treatment, continuity bible | `production/shot-graph.json`, assets/cues | all scenes are motion-ready |
| Animator | chosen engine specifications, shot graph | frame-steppable scenes, preview frames, render manifest | deterministic render without seek recheck |
| Sound engineer | script, original/safely licensed male voice, timings | narration WAV, alignment, SFX/music cue sheet | checked voice or timing without listening |
| Editor | validated scene clips, narration, captions | master MP4, export provenance | QC pass without running it |
| Independent critic | finished cut, facts, test reports | timecoded defects, grades, fixes, verdict | independent review if they built the scene |
| Packager | approved master and evidence | titles, thumbnail brief, chapters, source disclosure | video published without owner approval |

Use the eight existing `studio-*.md` agents. Motion director and storyboarder can be two phases of `studio-visual-director`; no extra agent files required.

## Narrative-first workflow and handoff gates

1. **Research lock:** identify claim IDs, independent sources and what cannot be verified. Reject unsupported assertions.
2. **Script lock:** clear audience promise, first 15-second hook, five-to-seven chapter causal progression, non-repetitive reveals and original exposition. Confirm 8-minute minimum on actual recorded audio, not guessed text length.
3. **Narrator lock:** use the channel's existing **male** Voicebox narrator where installed and legally authorized; fallback to a documented male preset only after quality comparison and approval. Never copy another person's voice without rights. Keep one narrator across the film. ASR-check words and preserve narration WAV and measured word timing.
4. **Creative treatment bake-off:** propose three meaningfully different treatments for one representative beat. Compare storytelling clarity, composition, motion, implementation cost, legal status, and continuity; approve one.
5. **Style routing:** each shot selects *one technique for a reason*: explain a mechanism, illustrate stakes, show evidence, or convey a transition. A style switch needs a designed bridge; default to coherent sets and shared assets, not unrelated adjacent looks.
6. **Shot contract:** narration word span; beat objective; claim ID; engine; primary subject identity; world/camera position; visible action; compositional hierarchy; SFX cue; entry/exit continuity; fallback. Explicitly design silence/holds for suspense and comprehension.
7. **Preview gate:** inspect first/middle/last frame, transition boundary frames, reading areas and subject identity. Run technical scene lint and deterministic scrubs. Reject slides masquerading as animation and excessive effects without narrative function.
8. **Master QC:** render and listen to the whole master; use available objective checks for blank/frozen sequences, unintended silences, sync drift, clipping, loudness, subtitle safe zones, source accuracy, and end card. Treat automated thresholds as **signals**; inspect false positives (e.g. intentional stillness/silence) before rejecting.
9. **Independent creative critique:** at least one reviewer other than the author, with timestamped problems and evidence. Require corrections and reruns of relevant tests. Record unresolved limitations.
10. **Approval and learning:** never publish automatically. Store what worked, what failed and its verified remedy in the existing production ledger and lessons files; retrieve them before the next video.

## External source registry (not installed by this documentation)

| Source | Purpose | Adoption boundary |
|---|---|---|
| [Agency Agents](https://github.com/msitarzewski/agency-agents) | Specialist handoffs and accountability | methods only, independent roles |
| [Anidoodle](https://github.com/alexgreensh/anidoodle) | 32 hand-drawn style techniques and timed drawing | benchmark renders, review art rights |
| [Huashu Art Motion](https://github.com/alchaincyf/huashu-art-motion) | moving art, explainers, motion grammar | don't copy excluded characters |
| [Claude Drawing Skill](https://github.com/cloveric/claude-drawing-skill) | deterministic painted/drawn plates | current upstream catalog varies; pin revisions |
| [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | character acting, expressions | original character only |
| [LunaAI motion-skill](https://github.com/LunaAI519/motion-skill) | keyframe-to-collage clips | paid APIs; owner approval per spend |
| [LottieFiles Motion Design](https://github.com/LottieFiles/motion-design-skill) | easing, hierarchy, choreography | reusable design principles |
| [HandDraw Skill](https://github.com/ToBeWin/HandDraw-Skill) | whiteboard SVG/Remotion DSL | verify Remotion commercial terms |
| [Manim Skill](https://github.com/adithya-s-k/manim_skill) | mathematical exposition | reproducible CE renders |
| [JavaScript Animation Skills](https://github.com/iart-ai/javascript-animation-skills) | code-made canvas films | deterministic render tests |
| [Stickman Video Director](https://github.com/kaomei/stickman-video-director) | character storytelling | adapt only suitable visual grammar |
| [YouTube Agent Skill](https://github.com/Jakeschincariol/youtube-agent-skill) | hooks, packaging, retention analysis | no invented metrics |
| [OpenMontage](https://github.com/calesthio/OpenMontage) | budgeted pipeline and stage review | AGPL: method study, no unreviewed code copying |
| [Voicebox](https://github.com/jamiepine/voicebox) | male narrator production | use authorized synthetic/preset profile |
| [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | research and transcripts | preferred optional adapter; login consent |
| [Obscura](https://github.com/h4ckf0r0day/obscura) | former browser reader | legacy retained; not default |

Additional current studio references include the 17 native animation styles and Bang Motion, Vox Director and Code Animation Prompts; see `production-stack.md` and `docs/ANIMATION_STYLES_AUDIT.md`. **Do not add up catalogs as independent integrated engines.** License and attribution obligations vary by repository, component, model and asset.

## Ten owner-supplied creative formats

Six owner-uploaded ZIP archives add **ten distinct production recipe references** (3D Animation, Cartoon Episodes, Documentary, Commercial Pipeline, Paper-Cut Motion Design, Talking Object, Skeleton Ads, Song-style Ads, Claymation and Paper Animation). Review [`uploaded-creative-formats.md`](uploaded-creative-formats.md) for adapted selection rules and the `scripts/creative_router.py` metadata preflight. Their bundled instructions/scripts are not automatically trusted, copied or executed. Channel narration, factual accuracy, paid generation consent, verified asset rights and production QC remain mandatory.

## Additional registered animation and sonic references

Read [`expanded-motion-tools.md`](expanded-motion-tools.md) for HyperFrames, OneTake (noncommercial-code restriction), gbro Collage B-roll, p5.brush, OpenToonz, Synfig, Pencil2D, PixelFX, and the existing Vox AI Motion Graphics Generator adaptation. Read [`sound-design-and-listening.md`](sound-design-and-listening.md) for the earshot / Openverse / Lemo Opuscar workflow, source licenses, perceptual sync, narrator protection, listening audits and sound-mix outputs. These registered sources are **not automatically installed or tested**.

## Prove it before expanding

Start with one **30–60 second narrated pilot**: one difficult factual explanation, one continuous protagonist or object, at least two appropriate shot techniques, one designed transition and one intentionally quiet moment. Compare candidate looks on the *same narration*. Require reproducible output, confirmed male narration, frame/audio/subtitle checks, a blinded creative critique and owner approval. Only then attempt a full 8+ minute production. Capture the actual commands, versions, durations and reports. Do not mark planned tests as passed.
