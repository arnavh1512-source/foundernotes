# YouTube packaging (prepared for manual upload)

Rules combined from agency-agents' Video Optimization Specialist and youtube-agent-skill's
title/thumbnail/chapter/SEO tools (both MIT), adapted. `scripts/package_lint.py` enforces the
mechanical parts. Nothing here predicts CTR or views.

## Title + thumbnail = one micro-story

- Write 5–10 titles across different honest triggers (curiosity, direct-search, benefit,
  challenge, contrast); shortlist three, recommend one.
- ≤ 60 characters; the meaning must survive mobile truncation at ~40.
- Name the question or benefit. Curiosity without lying: the video must pay the title off in the
  first third. Keep the evidence's qualification ("can", "often", "in some studies").
- Thumbnail: one focal object, high contrast, readable at 160 px wide, ≤ 3 words that *add* to
  the title rather than repeat it. No fake reactions, no arrows pointing at nothing, no
  before/after the evidence doesn't support. 1280×720 PNG/JPG < 2 MB, built from a real frame
  style of the video (same engine) so the click matches the watch.
- Make 2–3 thumbnail variants for YouTube's Test & Compare when the owner wants it.

## Description

- First two lines (≈150 chars) = the search snippet: what the viewer will understand.
- Then: a short summary, chapters (from `timings.json` scene starts), **sources** (every on-screen
  claim's link), credits for licensed music/assets, the podcast credit ("Inspired by a
  conversation on <Show>, <link>" — no implied endorsement), and a note that narration is synthetic.
- Chapters: first `00:00`, ≥ 3 chapters, each ≥ 10 s, 3–5-word titles naming the idea.

## Tags, hashtags, comments, end screen

- ≤ 15 tags, disambiguation only (they are a weak signal); 1–3 hashtags.
- Pinned comment asks a specific question the video set up, or links the main source.
- End screen (last 5–20 s): point to the next most relevant video or playlist; no
  "thanks for watching" recap.

## Shorts cut (optional)

20–55 s self-contained span that teaches one thing; new first line written for cold viewers;
1080×1920 with text inside the 984×1500 safe zone; burned-in captions; loop the last frame into
the first if natural; link the long video.

## Files

`package/package.json` (input to package_lint), `package/thumbnail.png`, `package/description.txt`,
`package/upload-checklist.md` (visibility, category, audience "not made for kids" unless it is,
captions file, synthetic-content disclosure decision, end screen, cards, playlist, schedule).
