# Creative production loop

The executable coordinator is scripts/studio_loop.py. The host AI performs reference analysis, script/scene authoring and independent creative critique; the Python tool validates evidence, tracks revisions and runs local rendering, assembly and technical QC. It is not an autonomous model service.

## Start
Run from the repository root:
```sh
python .claude/skills/podcast-scout-skill/scripts/studio_loop.py studio-output/my-video init my-video --maximum-cuts 3
python .claude/skills/podcast-scout-skill/scripts/studio_loop.py studio-output/my-video packet
python .claude/skills/podcast-scout-skill/scripts/studio_loop.py studio-output/my-video retrieve https://www.youtube.com/watch?v=VIDEO_ID
```

All report and artifact paths are relative to the episode folder. Never commit private narration reference files. Agent Reach is attempted by retrieve; save its actual failure envelope and document the real fallback if unavailable. Do not evade access controls. Analyze only material actually accessed. A transcript cannot establish visual or voice quality.

Commands: reference analysis.json → learn pattern.json → produce recipe.json → critic critique.json → revise fixes.json → produce recipe.json. Use status or packet between stages. A successful critique advances to owner_review; approve --owner NAME --evidence owner-review.txt records an explicit owner review, never publication. Maximum cuts defaults to three. Missing audiovisual review remains pending, never an invented pass.

## Reference and knowledge schemas
Reference:
```json
{"url":"https://www.youtube.com/watch?v=VIDEO_ID","scope":"audiovisual","retrieval":{"provider":"manual","reason":"Actual gateway failure and fallback evidence"},"observations":[{"dimension":"animation","time_s":1.4,"observation":"Describe the visible technique","evidence":["reference/frame-001.jpg"]}]}
```
Scope is transcript, frames or audiovisual. Dimensions are storytelling, animation, editing, pacing and voice, restricted by actual scope. Evidence files must exist and be nonempty; the host reviewer must verify their contents and source rights.

Knowledge:
```json
{"reference_index":0,"pattern":"Keep a held prop attached to its hand","application":"Original character, local wrist transform","tags":["motion","continuity"]}
```
Reference patterns remain hypotheses about effectiveness. Export writes content-addressed records into .claude/memory/creative-knowledge. knowledge-search QUERY retrieves lessons for subsequent episodes. Critic findings export as reviewer observations, never proven successful recipes. Existing record_lesson.py remains the path for separately verified successful recipes and the production ledger.

## Production
Explicitly install the pinned packages in .claude/skills/motion/remotion before using its CLI. No automatic installation, login, billing or voice substitution occurs.

Recipe:
```json
{"mode":"pilot","viewer_plan":"viewer-plan.json","shot_plan":"shot-plan.json","narration":"narration.wav","captions":"captions.srt","entry":"src/index.ts","composition":"Episode","producer":"scene-author","format":"horizontal"}
```
Copy the existing viewer-first and shot-plan templates and fill them with real evidence. Narration is already produced using the approved narrator workflow. The producer checks viewer/rights gates and actual narration duration, runs Remotion, rejects picture/voice length mismatch, burns captions through assemble.py, and runs qc_video.py. Pilot is 60–90 seconds; full production is at least 480 seconds and additionally requires approved_pilot_workflow pointing to the completed pilot workflow inside the episode. Keep that entire pilot folder with its media and evidence. Failed attempts retain logs in renders/cut-N/attempt-N and can be retried without overwriting evidence. Technical warnings cannot receive an automatic creative pass.

For external pictures, replace entry/composition with:
```json
{"picture":"exports/picture.mp4","backend":"opentoonz","picture_provenance":{"creator":"Actual creator","source":"Original project file or licensed source","license":"Actual asset license","export_method":"OpenToonz render and encode"}}
```
Merge these fields with the other recipe fields. Imports bypass only Remotion rendering; actual duration checks, narration assembly, captions, QC and creative review still run. A registered backend is not an installed or tested application. A picture is the assembled episode edit, not an arbitrary short clip padded to fill narration.

## Critic and revision
```json
{"render_sha256":"FROM_WORKFLOW","reviewer":"independent-critic","method":"human-audiovisual","model":null,"categories":{"storytelling":{"status":"pass","finding":"Specific observation","evidence":["review/notes.txt"]},"motion":{"status":"fail","finding":"Prop drift","evidence":["review/hands.jpg"]},"voice":{"status":"pass","finding":"Actual listening observation","evidence":["review/listening.txt"]},"editing":{"status":"pass","finding":"Specific pacing observation","evidence":["review/notes.txt"]}},"findings":[{"id":"F1","category":"motion","start_s":1.4,"end_s":2,"issue":"Prop separates from palm","fix":"Attach to actual clamped wrist","evidence":["review/hands.jpg"]}]}
```
Methods: human-audiovisual, model-audiovisual (actual model/version required), frames-and-transcript, transcript-only. Voice pass requires actual audiovisual listening. Identity/method declarations require honest host execution; they are not authentication. Evidence is hashed and render/QC hashes reject stale reviews. The low-level Python registration API is not an untrusted report ingestion interface.

Revision: {"changes":[{"finding_id":"F1","action":"Attach prop to hand group"}]}. Every open finding must be addressed. Re-review missing evidence without rerendering using critic again in review_required. Rerender changed scenes; old cuts remain available.

## Review frames
```sh
python .claude/skills/podcast-scout-skill/scripts/review_frames.py VIDEO --out NEW_REVIEW_FOLDER --times 1.2 1.4 1.6 --crop 600 300 400 400
```
Generates exact-time decoded frames, enlarged crops, a strip and source hash. Watch the actual motion and listen to the audio as well. A contact sheet does not establish temporal continuity or voice quality.
