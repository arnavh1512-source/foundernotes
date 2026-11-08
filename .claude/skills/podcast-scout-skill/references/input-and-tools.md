# Input access and tool selection

Use the host's actual tool inventory. The names below describe optional capabilities, not tools guaranteed to be installed. Read each tool's current schema before calling it.

**Agent-Reach is the default first-attempt research gateway for FounderNotes.** For public webpages, web queries and YouTube discovery/subtitles, run `python3 .claude/skills/podcast-scout-skill/scripts/research_gateway.py status` and then its `search`, `read`, `youtube-search`, or `transcript` action. The adapter calls only public, read-only Agent-Reach channels and reports a structured native-tool fallback if unavailable; follow its `fallback.allowed` flag. See `agent-reach.md`. Account login, paid transcription and installation require explicit owner authorization. Obscura is legacy, not default.

| Input / job | Preferred route | If unavailable |
| --- | --- | --- |
| YouTube podcast | Agent-Reach `research_gateway.py transcript URL` (real captions, not metadata); when unavailable, connected transcript/caption tools such as vidIQ `video_transcript` | Open an accessible official transcript or request pasted/uploaded captions. A YouTube link alone is not content access. |
| Audio/video upload | Native supported media understanding/transcription; distinguish audio from visual inspection | Use an available local transcription tool with authorized files, or request TXT/SRT/VTT. Do not claim general video playback capability. |
| TXT/SRT/VTT | Read original text and preserve cue timestamps | Analyze supplied excerpt and declare partial coverage. |
| Other podcast URL | Agent-Reach public URL reading, then publisher transcript or supported connected media tool | Read public metadata only to identify the episode; ask for the conversation text before analysis. |
| Current evidence | Agent-Reach `search` then `read` for primary sources (use native search/reader if fallback.allowed) | Disclosed fallback reader; if no reader works, explicit provisional mode without fabricated citations. |
| YouTube demand | Connected vidIQ keyword research, outliers, YouTube search, video stats or equivalent | Public dated examples as proxies, otherwise unavailable. |
| Public source page, including script-heavy pages | Agent-Reach `read` first; otherwise an authorized native reader | Native browsing or another supported reader, with a specific fallback reason. |

For connectors requiring account authorization, use the host's connection flow. Do not ask for passwords/API keys in chat, extract browser cookies, or promise connector access in another product. Claude and ChatGPT have separate tool inventories and account connections.

## Coverage ledger

Record these before analysis: episode title; canonical source URL when known; episode date if verified; transcript provider/file; original language; translation used; first/last observed timestamp; expected episode duration if independently available; gaps/truncation; whether visuals were inspected. An end timestamp alone does not prove full coverage.

For plain text without times, use paragraph/line references and null timestamps. For translated transcripts, label translated paraphrases; do not claim they are exact original-language quotations. Machine captions may misrecognize names, numbers, or technical terms: verify consequential wording against available audio or flag it.

For a multi-hour episode, create an evidence ledger across the whole accessible transcript before ranking. Sectioning is for context management, not a reason to prefer topics from the beginning. Save the ledger locally when the environment allows it. Do not include private raw transcripts in shared outputs unnecessarily.

## Tool calls and costs

Read tool instructions, especially asynchronous jobs and credit consumption. Use the existing user's authorized task scope and the host's approval rules; do not repeatedly ask to approve routine research already requested. Do not buy subscriptions or change account settings to complete research. Poll started jobs through their returned IDs; report failures instead of silently replacing the source.

Use exact citations and retrieval timestamps for metrics. Report counts as observations at that time, never future predictions. A view count without upload date/channel baseline cannot establish an outlier. A search results page does not establish keyword search volume.

## No-content and no-browsing responses

- **No transcript/media access:** Explain the specific failed capability and ask for a transcript or supported media. Do not use the episode title as evidence for five topics.
- **Transcript accessible, web unavailable:** Deliver provisional opportunities with source anchors, tentative editorial scores, and specific verification queries. Mark demand unavailable and confidence appropriately low. Do not call any candidate research-complete.
- **Only part of the transcript:** Report the available range and analyze it; state that unobserved sections could change the ranking.
- **Too little educational substance:** Say how many distinct topics the source supports. Offer adjacent ideas in a separate, labeled section only if useful.
