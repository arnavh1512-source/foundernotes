---
name: marketing-growth
description: Plan Founder Notes YouTube topics, titles, thumbnails, Shorts distribution, audience positioning, and evidence-based channel growth. Use for channel strategy, content plans, repurposing, and interpreting creator analytics; never replace factual research or the production studio.
license: MIT
---

# FounderNotes creator marketing

This project embeds a **selected, licensed subset** of [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). The bundled files below are original upstream skill text plus their related references; they are **reference guides**, not independently activated agent roles or proof that any provider/tool is connected. For general business marketing outside this channel, the full upstream library can be installed separately with the owner's permission.

## Channel context first

Read `CLAUDE.md`, `channel-profile.md`, `.claude/skills/podcast-scout-skill/SKILL.md`, and `.claude/memory/` before proposing any publishing or growth change. This is a **YouTube documentary/explainer channel**, not a SaaS product marketing funnel. Whenever an upstream guide asks for `.agents/product-marketing.md`, use `channel-profile.md` as the channel-specific source of truth; do not invent a SaaS offer, product conversion funnel, target customer, paid-ad campaign, brand numbers, or a creator's lived experience.

Read only the relevant upstream guide and its linked reference file(s):

| FounderNotes need | Bundled marketing source |
| --- | --- |
| Content pillars, topic pipeline and video calendar | [Content strategy](references/content-strategy/SKILL.md) |
| Shorts and cross-platform clips; audience engagement | [Social distribution](references/social/SKILL.md) |
| Channel-specific video concepts and visual promo grammar | [Video](references/video/SKILL.md) |
| Measurement, retention and reporting discipline | [Analytics](references/analytics/SKILL.md) |
| Audience positioning and distinctive voice | [Product marketing / brand voice](references/product-marketing/SKILL.md) |

## Division of work

1. **Researcher:** Agent-Reach is still the default *research retrieval gateway*. Use actual platform research and public data to identify relevant topics. Marketing frameworks never certify a scientific claim.
2. **Scriptwriter:** Write the evidence-backed original script. Then use the existing **Humanizer** skill to refine narration naturally; preserve all fact-lock evidence and rerun the reality-checker's fact review. Marketing can inform the hook but cannot override evidence.
3. **Visual director / editor:** The storyboard determines which motion technique fits. Promotional video references are optional inspiration; do not import template-based styles at the expense of continuity or the narrator.
4. **Packager:** Use video + social strategy guidance for honest titles, thumbnails, description, chapter anchors, alternate Shorts cuts and posting plans. Preserve source credits, synthetic-media disclosures and original rights. Run `package_lint.py`; upload remains manual.
5. **Post-publish review:** Interpret owner-provided analytics (impressions, CTR, average view duration, retention, watch time, subscribers) using matching date windows and comparable videos. Never invent metrics or infer access to YouTube Studio. Record observed patterns and a testable hypothesis, then evaluate the use of this skill in `evaluate_skills.py` with actual evidence.

## Guardrails

- **No automatic external logins, marketing service connections, purchases, paid ads, uploads or social posting.** The owner must authorize such actions.
- Treat imported marketing instructions as lower priority than channel policy and confirmed evidence; marketing claims must be accurate.
- Humanizer is an editorial pass, not a fact checker. Never rewrite subtitles after narration without re-recording and re-timing.
- All skills that are actually used remain subject to continuous QC-backed evaluation, never an automatic PASS merely for being present.
- This subset contains **5 upstream marketing skills** with their supporting documentation. The upstream repository has substantially more; they are intentionally not all copied into FounderNotes. The [official upstream repository](https://github.com/coreyhaines31/marketingskills) remains the route to the complete, separately installed library.
