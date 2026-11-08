# Uploaded Claude creative skills — adapted integration (10 skills)

Source: six ZIP archives supplied by the channel owner. The archives contain **ten**, not eleven, distinct `SKILL.md` files. The packages are treated as **untrusted third-party instruction reference material**, not as code we have audited or installed into the runtime. Their author/license provenance is not established by the ZIP filenames alone. This document adapts their techniques in our own wording; it does not re-publish their full instruction texts, sample assets, or executables.

The FounderNotes [production charter](agency-production-system.md) **always takes precedence**, followed by the fact lock, measured narration timings, [expanded motion tool routing](expanded-motion-tools.md), [sound design guidance](sound-design-and-listening.md), and the episode-specific continuity bible. A style recipe must not silently swap the narrator, produce copyrighted replicas, misrepresent fictional scenes as documentary facts, call paid services, or skip quality review.

## Routing inventory

| Key | Uploaded skill | What to borrow | Best FounderNotes use | Avoid |
|---|---|---|---|---|
| `3d-animation` | 3D Animation | script → scene/asset bible → timed blocks → clip assembly, concrete reference IDs | original 3D concept explainers, myth-busting diagrams | treating model-generated clips as factual footage |
| `cartoon-episodes` | Cartoon Episodes | recurring character/world bible, character/prop/location reference sheets, scene actions & dialogue anchors | recurring host character, narrative skits or explainers | changing the established cast between scenes |
| `documentary` | Documentary | research case file, verified event timeline, asset registry, timecoded reenactments | evidence-led investigations and historical context | its suggestion to treat **all** stories as real; invented incidents must be labeled fiction |
| `commercial-pipeline` | Commercial Pipeline | phased asset → edit → fix process, controlled complexity and review gates | occasional channel promo, original product/business mechanism scenes | promotional claims without evidence, unapproved ad generation |
| `paper-cut-motion` | Motion Design Prompt | reference image → composition still → sheet → motion prompt | editorial paper cutouts and title transitions | applying the same cutout template for unrelated subjects |
| `talking-object` | Talking Object | consistent expressive object plate, dialogue and action per beat | narratively justified object mascots that explain a mechanism | replacing narrator with inconsistent character voices |
| `skeleton-ads` | Skeleton Ads | recurring articulated hero and physical cause/effect action | anatomy/systems analogies with a clearly stylized **original** character | medical-sounding certainty unsupported by sources |
| `song-style-ad` | Song-style Ad | music-first beat mapping and lip-sync/shot planning | only explicitly approved jingles or rhythmic promos | switching the whole channel to singing or female narration; copyrighted song reuse |
| `claymation` | Claymation | texture/physicality: fingerprints, imperfect modeled props, stepped action, cast shadows | stylized mechanical or historical metaphors | polished generic CGI mistakenly labeled clay |
| `paper-animation` | Paper Animation | paper grain, thickness, real layered shadows, cut/pivot/parallax, consistent physical space | collage explainers, origami assembly and diagram reveal | flat unmotivated slide fades |

## The owner’s priorities, applied across all ten

**Narration:** use the channel's authorized, consistent **male** Voicebox narrator when available; permitted male fallback must be recorded as an exception. Imported scripts that specify other genders, music-only dialogue, or character voice switching are not channel defaults. Spoken durations are measured from final WAV. Rendered characters can remain silent while the narrator explains; when a character must speak, require explicit owner approval and a separate vocal identity/rights review.

**Style and scene continuity:** lock characters, materials, palette, props, lenses and geography in a `visual_bible` before generating beats. Every beat names purpose, claim, persistent subject, visible action, camera position, source asset IDs and start/end-state connections. Clip duration derives from narration words, not an arbitrary 10- or 30-second model block. A generated clip with extra time must be cut intentionally; never fill an evidence gap with fabricated action.

**Factuality:** documentary incident reconstructions are labeled reenactments where relevant, and source coverage is recorded. An arbitrary pop-culture story is **not** a real incident just because a documentary template says so. Ads, skeleton metaphors, and talking objects cannot substitute fictional benefit claims for verified data.

**Rights and cost:** using a reference prompt does not prove license to publish its demo characters, style images or music. Build original characters/assets. Paid generators require a per-shot approval and budget before calling them. Never claim the references were installed or their renderers tested merely from ZIP inspection.

## Handoff format and validator

Use the original `creative_router.py` CLI in `../scripts/` to discover eligible recipes and validate a JSON shot plan. This is an independent **preflight validation tool**, not a renderer. It deliberately fails on missing narration identity, unapproved paid actions, missing asset evidence, invalid timing and unspecified style routes.

A proposed shot plan should include:
- `narrator`: `{"voice_id":"founder-notes","gender":"male","approved":true}`
- `shots`: ordered objects with `id`, `format` (a registry key), `start_s`, `end_s`, `claim_id`, `asset_ids` and `paid` boolean. A paid shot requires `cost_approved:true`.
- `asset_manifest`: records keyed by asset ID with `rights_verified:true`, `source` and `license`.
- `claims`: records keyed by claim ID with `verified:true` and `source`.
- `narration_duration_s`: measured from the final audio. A plan is rejected when end-of-picture drift is significant.

**Acceptance** still requires actual engine execution, contact sheets, subtitle and sound QC, and an independent reviewer. The router cannot prove visual quality, legal rights, or a synthesized narrator's vocal quality on its own.

## Production adoption checklist

1. Register and identify all ten techniques without copying third-party ZIP code into the core renderer.
2. Run the creative router on the proposed script's shot plan; fix errors.
3. Build a 30–60-second pilot using no more than two matching recipes, with a persistent protagonist and coherent transitions.
4. Render all shots with an actually installed and licensed engine; never confuse a text-to-video *prompt* with a generated video.
5. Verify the male narrator, sound-design provenance, subtitle placement, actual frame/audio synchronization and final listening.
6. Log creative defects and corrections to the production ledger. Promote only techniques that pass the same-voice comparison and owner review.

## Original source files in the uploaded packages

- `Animation Skill.zip`: `3D Animations/.claude/skills/3d-animation/SKILL.md`
- `Cartoon Episodes.zip`: `Cartoon Episodes/.claude/skills/cartoon-episodes/SKILL.md`
- `Documentary-Skill-Claude (1).zip`: `documentary-skill/.claude/skills/documentary/SKILL.md`
- `Commercial Pipeline (1).zip`: `Commercial Pipeline/.claude/skills/commercial-pipeline/SKILL.md`
- `motion-design-prompt (1).zip`: `motion-design-prompts/skills/motion-design/SKILL.md`
- `Creative_Formats_Claude (1).zip`: five `SKILL.md` files under `talking-object`, `skeleton-ads`, `song-style-ad`, `claymation` and `paper-animation`.

Archive-local shell/Python scripts were **not executed**. Their individual instructions may conflict with the channel's production policies; follow this adapted contract instead.
