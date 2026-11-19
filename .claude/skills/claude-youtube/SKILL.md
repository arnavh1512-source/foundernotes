---
name: claude-youtube
description: YouTube creator toolkit (vendored MIT, AgriciDaniel/claude-youtube) adapted for Founder Notes. 14 sub-skills for video SEO, hooks, retention structure, thumbnail briefs, upload metadata, Shorts, content calendar, topic ideation, analytics interpretation, channel audit, repurposing, monetization planning and (owner-requested only) competitor analysis, plus read-only YouTube Data/Analytics API scripts. Use for packaging, topic planning and post-publish review; never as a substitute for the studio's research, fact lock, script, narration or QC.
license: MIT
---

# Claude YouTube for Founder Notes

Vendored from [AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube) at commit `84c3fa6` (2026-04-10), MIT licence in `LICENSE`. The upstream files are unchanged; the upstream entry point is kept as [`references/upstream-SKILL.md`](references/upstream-SKILL.md) (its paths such as `sub-skills/…` are relative to this skill folder). Not vendored: the upstream installer/uninstaller scripts and plugin metadata.

**This page overrides the upstream entry point wherever they differ.** Channel policy in `CLAUDE.md` and `channel-profile.md` overrides both.

## Context: don't ask, read

The upstream protocol asks for niche, size tier and goal before every task. For Founder Notes, take them from `channel-profile.md`:

- **Niche:** the hidden mechanisms, mental models and counter-intuitive playbooks behind great founders and systems, drawn step by step.
- **Channel type:** Education (`templates/education-channel.md`), with Niche Authority (`templates/niche-authority-channel.md`) as a secondary lens.
- **Size tier and goal:** ask the owner only if a task actually depends on them and they aren't recorded. Never guess subscriber counts.

## How each sub-skill fits the studio

| Sub-skill | Use in FounderNotes | Constraint |
| --- | --- | --- |
| `ideate`, `strategy`, `calendar` | Topic pipeline and planning, alongside `marketing-growth` | Ideas still go through the viewer-first gate and research before any script |
| `hook` | Extra hook variants to test in the 60–90 s pilot | The opening must deliver a real insight within 30 s (viewer-first rule); no promise the film doesn't pay off |
| `script` | **Retention review only** of a studio script: pattern-interrupt spacing, forward hooks, drop-off risks | `studio-scriptwriter` writes the script. Ignore upstream's ~150 wpm and length math: narration is ~179 wpm at speed 1.0 and long-form is ≥ 480 s with no padding |
| `seo`, `metadata` | Titles, description, tags, chapters for `studio-packager` | Chapters come from `timings.json`; never name the source podcast, host or guest; keep sources and synthetic-narration disclosure; `package_lint.py` is the final check |
| `thumbnail` | Brief and A/B concepts | The shipped thumbnail is rendered in the video's own art style (see `studio-packager`). No AI image generation (NanoBanana/Gemini, MuAPI) without owner approval |
| `shorts`, `repurpose` | Summary Short and clip plan | Short follows `references/video-delivery-package.md` in podcast-scout-skill |
| `analyze`, `audit` | Post-publish review of **owner-provided** analytics | Never invent impressions, CTR, retention, views or subscriber numbers |
| `monetize` | Only when the owner asks | No income promises |
| `competitor` | **Only when the owner explicitly asks** (CLAUDE.md rule) | Upstream's 4 parallel agents count as delegation: follow `model-routing.md` |

## Benchmarks are heuristics, not evidence

The `references/*.md` files contain many unsourced figures (CTR bands, AVD averages, traffic-source percentages, dated "algorithm changes", CPM/RPM ranges). Treat them as **upstream editorial heuristics**:

- Never put them in narration, on screen or in a description as fact.
- When a recommendation leans on one, label it "upstream heuristic, unverified".
- Upstream's "data grounding" gate ("every benchmark must come from a reference file") does not make a figure verified. Real claims need primary sources under the studio fact lock.
- Prefer the channel's own observed analytics once they exist.

## Data sources, keys and money

- **Transcripts and public research:** use `.claude/skills/podcast-scout-skill/scripts/research_gateway.py` first (yt-dlp first for YouTube, Agent-Reach as backup). `execution/fetch_transcript.py` (yt-dlp subtitles only, no media download) also works; it needs the studio venv active so `yt-dlp` is on `PATH`. See `.claude/skills/podcast-scout-skill/references/yt-dlp.md`.
- **YouTube Data API scripts** (`fetch_channel_data.py`, `search_competitor_videos.py`) need `YOUTUBE_API_KEY`. Never ask for a key in chat and never commit one; the owner configures it. `search.list` costs 100 quota units, so prefer `fetch_channel_data.py` (~16 units).
- **Analytics API** (`fetch_video_analytics.py`) runs a browser OAuth flow for the owner's own channel. Run it only when the owner asks and is present to sign in. Tokens are stored outside the repo in `~/.claude/.tmp/`.
- **DataForSEO** (paid per call) and **NanoBanana** MCP servers are optional and not configured here. Don't install, configure or call them without the owner's approval; upstream's WebSearch fallback is the default.
- The scripts are read-only. Nothing in this skill uploads, edits or publishes on YouTube.

## Quality

Upstream's three gates (specificity, data grounding, completeness) and its self-anneal loop still apply, on top of the studio's gates. Record real outcomes with `evaluate_skills.py` as `external/claude-youtube`; presence of the skill is not a pass.
