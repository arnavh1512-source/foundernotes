# Sources and licences

Podcast Scout Studio is original work. It integrates external tools by reference (installed
separately, never vendored) and adapts ideas and rules from these projects:

| Project | Licence | How it is used |
|---|---|---|
| [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | MIT | Orchestrator/NEXUS gate pattern, handoff template, and rules from the Video Optimization Specialist, Visual Storyteller, Narratologist, Research Synthesist, Statistician, Data Visualization Engineer, Inclusive Visuals, Brand Guardian, Short-Video Editing Coach, Reality Checker and Evidence Collector personas — rewritten as the studio crew |
| [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | MIT | Timing, easing, stagger and choreography numbers (scaled for video) in animation-craft.md |
| [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) | MIT | Manim engine; 3b1b teaching principles |
| [ToBeWin/HandDraw-Skill](https://github.com/ToBeWin/HandDraw-Skill) | MIT | Whiteboard engine |
| [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle) | Apache-2.0 | Hand-drawn film engine (32 styles) |
| [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | MIT (character art excluded) | Explainer grammars / art-in-motion engine |
| [cloveric/claude-drawing-skill](https://github.com/cloveric/claude-drawing-skill) | MIT | Illustration stills (77 styles) |
| [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | MIT | Character animation engine |
| [LunaAI519/motion-skill](https://github.com/LunaAI519/motion-skill) | MIT | Optional paid collage B-roll |
| [iart-ai/javascript-animation-skills](https://github.com/iart-ai/javascript-animation-skills) | MIT | Canvas film engine; storyboard/beat rules |
| [kaomei/stickman-video-director](https://github.com/kaomei/stickman-video-director) | MIT | Stickman engine; 2.5 s inactivity rule, sample-before-render, semantic captions |
| [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) | MIT | Title/thumbnail/chapter/hook rules re-implemented in package_lint.py and the scriptwriter role |
| [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | AGPL-3.0 | Ideas only (stage gates, sample-first, budget approval, Shorts safe zone); no code or text copied |
| [jamiepine/voicebox](https://github.com/jamiepine/voicebox) | MIT | Optional local TTS server with male presets |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | MIT | Preferred optional research channel integration (not vendored or installed by this repository) |
| [h4ckf0r0day/obscura](https://github.com/h4ckf0r0day/obscura) | Apache-2.0 | Legacy bundled research-helper references only; no distributed browser binary |
| [HeyGen-com/hyperframes](https://github.com/HeyGen-com/hyperframes) | Apache-2.0 | Documented optional agent-first HTML animation renderer, not installed |
| [feitangyuan/onetake](https://github.com/feitangyuan/onetake) | PolyForm Noncommercial 1.0.0 | Continuity ideas only; **do not vendor/use source commercially without license** |
| [Anil-matcha/vox-ai-motion-graphics-generator](https://github.com/Anil-matcha/vox-ai-motion-graphics-generator) | MIT indicated by upstream README | Existing collage-director adaptation; verify per-component rights |
| [patch-gg/pixelfx](https://github.com/patch-gg/pixelfx) | MIT indicated by upstream README | Procedural pixel effect and action-pose ideas, not copied |
| [opentoonz/opentoonz](https://github.com/opentoonz/opentoonz) | Check upstream component notices | Optional external desktop 2D suite, not vendored |
| [synfig/synfig](https://github.com/synfig/synfig) | Check upstream component notices | Optional external vector animation app, not vendored |
| [pencil2d/pencil](https://github.com/pencil2d/pencil) | Check upstream component notices | Optional external frame-by-frame animator, not vendored |
| [acamposuribe/p5.brush](https://github.com/acamposuribe/p5.brush) | MIT | Painted background plates (standalone build vendored per film) |
| [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | MIT | Directing method ideas; sampler/sfx/ASR tools used from an installed copy; instrument samples CC0 / CC BY 3.0 (Salamander) |
| [WordPress/openverse](https://github.com/WordPress/openverse) | MIT (API); media per file | `fetch_sfx.py` searches CC0 sound effects and records each file's licence |
| [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot) | MIT | Code-made SFX bank, film sync/loudness listening and critique (installed separately) |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | Seam doctrine ideas (vector law, the current, carriers, no idle wobble) re-implemented in our kit |
| [feitangyuan/onetake](https://github.com/feitangyuan/onetake) | PolyForm Noncommercial | Ideas only (carry, rhythm variance, operated camera, no particle flourishes); no code used |
| [pyang5166/gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) | MIT | Method idea: one metaphor per narration line, gated metaphor → still → motion |
| Synfig / OpenToonz / Pencil2D | GPL-3 / BSD / GPL-2 | Optional desktop engines for owner-drawn shots |
| Kokoro-82M / [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) | Apache-2.0 / MIT | Default male narration (am_michael) |
| [Piper](https://github.com/rhasspy/piper) voices | MIT (voice cards vary; check each) | Fallback male narration (en_US-ryan-high) |
- Open Generative AI (Anil-matcha/Open-Generative-AI), MIT. `scripts/gen_media.py` follows its MuAPI client's request pattern (submit + poll); no code is copied. Generated assets are subject to MuAPI's and each model's terms.
- vox-ai-motion-graphics-generator (Anil-matcha), MIT per its package.json/README (no LICENSE file upstream). Vendored as .claude/skills/collage-director with changes: male-voice allowlist, voice-cloning guard, proxy key support, channel rules.
- pixelfx (patch-gg/pixelfx), MIT: ideas only (acts: wind-up, snap, hit-stop, shake; poses on 12 fps; colour/light buffers; the check tool's idea). K.onTwos/K.act/K.keys in assets/ink-gold-kit/kit-loop.js and scripts/lint_scenes.py are our own code.
