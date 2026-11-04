# Production plan — <working title>

slug: `<slug>` · brief: `brief-NN.md` · target runtime: `m:ss` · format: 16:9 1920×1080@30
narrator: male — `<engine>/<voice>` · look: `<visual language>` · personality: `<premium|…>`

## Stage status
| Stage | Owner | Status | Evidence / file |
|---|---|---|---|
| Script | studio-scriptwriter | ☐ | script.md |
| Fact lock (Gate F) | studio-reality-checker | ☐ | claims.md |
| Storyboard + look (Gate L) | studio-visual-director | ☐ | storyboard.md, looks/*.png |
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
  research/            podcast-report.md/json, brief-NN.md, sources
  script.md claims.md storyboard.md
  narration/           script.json → narration.wav, timings.json, captions.srt/.vtt, segments/
  looks/               one still per look (approval)
  scenes/              NN-<id>/ sources + NN-<id>.mp4 ; list.txt (clip order)
  final/               video.mp4, video.srt, sheet.jpg, stills/, qc.json
  package/             package.json, thumbnail.png, description.txt, upload-checklist.md, shorts/
```
