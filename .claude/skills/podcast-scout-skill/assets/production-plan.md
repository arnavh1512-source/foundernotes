# Production plan — <working title>

slug: `<slug>` · brief: `brief-NN.md` · target runtime: `m:ss` · format: 16:9 1920×1080@30
narrator: male — `<engine>/<voice>` · look: `<visual language>` · personality: `<premium|…>`

## Mandatory viewer-first promise — COMPLETE BEFORE scripting

> This video is for someone struggling with ___; they’ll understand ___ and leave knowing how to ___.

**Viewer:** ___ · **Daily-life situation:** ___ · **Specific relevance now:** ___

**Evidence and original angle:** ___ · **Interesting details:** ___ · **Limits next to claims:** ___

**First 15–30 seconds:** viewer recognition → curiosity → **delivered early insight** (not a tease)

**Chapter progression:** each section answers a NEW question, adds distinct learning, or provides a unique practical application. No repetition to fill 8+ minutes. Every meaningful scene explains a change; one coherent visual style. Characters only AFTER the viewer problem is clear. Narration must be naturally spoken, paced and qualified.

- Plan: `research/viewer-first-plan.json` (copy `assets/viewer-first-plan.template.json`)
- Before script: `python3 .claude/skills/podcast-scout-skill/scripts/viewer_first_gate.py studio-output/<slug>/research/viewer-first-plan.json --stage pre-script` (**FAIL = STOP**)
- Before expanding to full video: reviewed **60–90s pilot** (measured duration, actual playback, human/editorial critique) and `--stage full-production` (**FAIL = STOP**)
- Outsider test: **understands the problem / wants the answer / has already learned something**. Record each result, with honest proof. If substance is too shallow for 8 minutes, deepen evidence or rescope, never add filler.

## Stage status
| Stage | Owner | Status | Evidence / file |
|---|---|---|---|
| Viewer-first (Gate V) | Producer + viewer analyst | ☐ | research/viewer-first-plan.json, pre-script PASS |
| Script | studio-scriptwriter | ☐ | script.md |
| Fact lock (Gate F) | studio-reality-checker | ☐ | claims.md |
| Storyboard + look (Gate L) | studio-visual-director | ☐ | storyboard.md, looks/*.png |
| Reviewed 60–90s pilot (Gate V2) | Producer + reality checker | ☐ | pilot video, measured seconds, review notes, full-production PASS |
| Narration | studio-sound-engineer | ☐ | narration/timings.json |
| Scenes | studio-animator | ☐ | scenes/*.mp4 |
| Assembly | studio-editor | ☐ | final/video.mp4 |
| QA (Gate Q) | studio-reality-checker | ☐ | final/qc.json, sheet.jpg |
| Package (Gate P) | studio-packager | ☐ | package/* |

## Storyboard
| # | Scene id = segment id | Start–end (from timings.json) | Engine | Enters / moves / settles | On-screen text | Claim IDs | Carry-over |
|---|---|---|---|---|---|---|---|

## Claim table
| Claim ID | Sentence in script | Source (ledger) | Status (supported/qualified/cut) |
|---|---|---|---|

## Folder layout
```
studio-output/<slug>/
  ledger.md            decisions, approvals, licences, open issues
  research/            viewer-first-plan.json, viewer-value.json/md (for source videos), podcast-report.md/json, brief-NN.md, sources
  script.md claims.md storyboard.md
  narration/           script.json → narration.wav, timings.json, captions.srt/.vtt, segments/
  pilot/               60–90s sample, real playback notes, evidence of review
  looks/               one still per look (approval)
  scenes/              NN-<id>/ sources + NN-<id>.mp4 ; list.txt (clip order)
  final/               video.mp4, video.srt, sheet.jpg, stills/, qc.json
  package/             package.json, thumbnail.png, description.txt, upload-checklist.md, shorts/
```
