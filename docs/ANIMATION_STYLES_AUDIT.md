# Animation styles audit — FounderNotes 2.0

## Scope and evidence

Reviewed the current `.claude/skills/animation-styles/SKILL.md` and all 17 individual `references/styles/*.md` documents on the repair branch. **This is a source-instruction audit, not a rendered-video benchmark**: the reference files describe techniques and starters; they do not prove how well production renders look. Rendering, source-code inspection of the shared player/export bridge, visual comparison, and audio checks remain open.

## All 17 documented styles

| Style | Distinctive mechanism | Key failure risk | Suggested narrative use |
|---|---|---|---|
| Pixel Art | low-resolution integer-grid drawing and nearest-neighbor scaling | fake pixelation, jittering camera | systems, game-like journeys |
| Chalkboard | multi-pass broken chalk strokes that draw on | smooth vector lines masquerading as chalk | mechanisms, diagrams |
| Glow Sketch | dotted contours and controlled glow | illegible bloom and visual monotony | abstract connections |
| PS2 | low-poly 3D, flat shading and low-res render | toy-like generic geometry | nostalgic virtual environments |
| Comic Art | ink contours, halftone and panel composition | random panels and unmotivated impact words | conflict and decisive reveals |
| Flat Vector | layered flat color planes and limited palette | static infographic slides | explanatory mechanisms |
| Dan Koe-inspired | monochrome line-and-dot diagrams | generic repeated symbolism | abstract mental models |
| CGI Motion | 3D material, lighting and deliberate camera moves | poor materials, camera drift | physical processes |
| Lego-inspired | modular brick geometry and stepped motion | repetitive block gimmicks | construction and assembly |
| ZackD-inspired | soft 3D explainer shapes and short cuts | generic AI-looking clay | accessible physical explainers |
| One-Line Graph | persistent continuous stroke through the film | impossible path continuity | causal chains |
| One-Ball Showreel | one hero object persists across motion techniques | becomes an effects demo | transformation metaphor |
| ASCII Terminal | luminance sampled into monospace character grid | unreadable density | computation and digital worlds |
| Pixel Dither | intentional resolution collapse and dither | low-res obscures facts | technological change |
| Risograph Cutout | two-ink layered paper with imperfect motion | arbitrary paper clutter | editorial storytelling |
| Renaissance Codex | original parchment drawings becoming animated | static antique wallpaper | inventions and history |
| Ink in Water | particle bloom with turbulence and drag | expensive spectacle without explanation | emergence and transformation |

## Cross-cutting findings

1. The entrypoint described **ten** looks despite listing seventeen; the repair branch now corrects the wording.
2. Its fallback style question offered only ten styles; the repair branch now requests a relevant shortlist for standalone use and delegates studio selection to the director.
3. The old channel rules mandated adjacent scenes use different looks and new casts, which can damage continuity. These are replaced by narrative-motivated style changes and persistent scene identity.
4. The style references describe visual rules, but do not constitute an independent benchmark or an automatically improving system.
5. Several 3D techniques depend on externally loaded three.js; offline reproducibility and dependency pinning need testing.
6. Current narration guidance in the style entrypoint still references Kokoro, while production documentation references other engines. The studio should use the verified current narrator and measured alignment rather than selecting a voice by style.

## Benchmark protocol (pending execution)

For each style: render the **same 8–12-second narration beat**, log frame rate, resolution, generation/render time, missing assets, frame determinism, continuity errors, visual readability at phone size, and sound-to-action alignment. Have a separate critic review muted and audible versions, with timestamps and a 1–5 rubric for clarity, craft, continuity, pacing, and novelty. Include a motionless control to test whether movement helps.

Then compare promising styles against one representative implementation from each of Bang Motion, Vox Director, Huashu Art Motion, Claude Drawing Skill and Code Animation Prompts. Record pinned upstream revisions and licenses. Select by beat function, not by number of styles used.

## Promotion gate

A technique is eligible for production only after its reproducible sample renders, technical checks pass, an independent critic provides concrete feedback, and the channel owner approves a side-by-side comparison. Archive rejected treatments with failure reasons for future learning. The old presets are not automatically deleted.
