# Reference comparison and revision

Owner request: 2026-11-17. Make videos, compare them with the supplied references, improve failed criteria, and preserve mistakes for the next person using this repo.

## Reference register

| Reference | URL | Current evidence status |
| --- | --- | --- |
| Alan Becker | https://www.youtube.com/@alanbecker | Core stick-animation benchmark; tutorials and creator process sources studied in `ALAN_BECKER_STUDY.md`; finished-film audiovisual review pending |
| DayOne Films | https://www.youtube.com/@dayonefilmsofficial | Owner-selected channel; representative video and timestamped study pending |
| PsychToonsHQ | https://www.youtube.com/@psychtoonshq | Owner-selected channel; representative video and timestamped study pending |
| Individual reference | https://www.youtube.com/watch?v=gly2wBcnZUQ | Playback blocked on 2026-11-17; not watched in this session |
| PsychDoodleTV | https://www.youtube.com/@psychdoodletv | Owner-selected channel; representative video and timestamped study pending |

Do not infer a channel's style from its name, thumbnail or subscriber count. Select one relevant video per channel when access works; record its canonical video URL, title, sampled intervals, method and limitations. Keep the existing dated study in `.claude/skills/podcast-scout-skill/references/reference-video-learnings.md`; do not attribute those uploaded videos to these channels without evidence.

## Review each cut

1. Read the mistakes file and existing reference learnings before planning. Attempt the existing `research_gateway.py` Agent-Reach route first for discovery/subtitles. Use the actual provider in the record. Subtitles establish wording only, not acting, temporal motion or voice delivery. Respect access restrictions.
2. Copy `docs/reference-comparison.template.json` into `studio-output/<slug>/review/cut-N-comparison.json`. Replace every placeholder with real evidence. Hash the exact output file. List every supplied reference as reviewed, pending or blocked; never silently omit one.
3. Compare like-for-like segments: opening against opening, explanation against explanation, emotional beat against emotional beat. Record our start/end and reference start/end, the observed difference, evidence location and a concrete action for each criterion below. These are production targets, not measured properties of the supplied channels.
4. Review the complete pilot in motion, with sound. For longer edits, inspect the complete output and record coverage. Frames can support pose/composition findings, but cannot establish temporal continuity or voice quality. Distinguish camera movement from actual changes in character pose or object state.
5. Mark each criterion pass, fail or pending. A pass needs evidence; missing footage/listening remains pending. Overall ready requires every criterion passing, every prior finding closed with new evidence, technical QC passing and the existing independent critique/owner-review stages. Averages cannot conceal a failed criterion.
6. For each failure, submit the finding through the existing `studio_loop.py critic` / `revise` flow; its JSON schema remains authoritative. Rerender changed scenes, compare the new cut, and check for regressions. Never edit a score to simulate an improvement. This Markdown/JSON checklist is a host-review requirement, not a new machine-enforced gate.
7. Use the existing maximum-cuts setting (default three). If a cut still fails at the limit, stop with specific remaining defects and a proposed rescope. Never claim that a failed cut matches the references.

## Criteria

| Criterion | Passing evidence required |
| --- | --- |
| Viewer clarity | The opening identifies a recognizable problem and delivers an understandable insight; each scene has a clear explanatory or story purpose. |
| Character acting | Intent is visible in posture, expression, gaze and reaction. Actions suit the line; repeated generic gestures do not stand in for acting. |
| Meaningful motion | A character or object visibly changes in a way that carries meaning. No accidental sliding, prop drift, popping or broken contact. Intentional stillness has a recorded reason. |
| Shot variety and continuity | Wide/medium/close framing and settings serve story beats; identity, eye lines, props, screen direction and lighting remain coherent across cuts. |
| Visual explanation | Abstract ideas become readable original actions, situations or metaphors. Label-heavy slides do not replace explanation. |
| Pacing | Actual cut timing and pauses support comprehension and emotional beats. The historical roughly three-second shot cadence is a candidate, not a mandatory timer. |
| Voice and sound | Actual listening confirms natural phrasing, distinct dialogue intentions, complete words, purposeful pauses, unobtrusive music and synchronized key actions. Measurements alone cannot pass this. |
| Finish and readability | No clipping, blank gaps, subtitle collisions or unreadable small details in the target format. Check beginning, transitions and ending, plus the full edit. |

Use techniques as inspiration. Keep artwork, scripts and characters original; do not copy a creator's identity or clone their voice. Do not claim these choices guarantee views.

## Persistent mistakes

Use `.claude/skills/podcast-scout-skill/scripts/record_lesson.py` to append to `.claude/memory/mistakes_and_pitfalls.md`. Keep one record per distinct defect with episode/cut, time range or file, observed problem, supported cause (or `unknown`), correction, prevention check, evidence and verification status. Clearly distinguish proposed fixes from verified fixes. Log current access blockers as process limitations, not invented animation defects. Preserve prior records.

Example invocation: `python .claude/skills/podcast-scout-skill/scripts/record_lesson.py studio-output/<slug>/review/lesson.json`. Follow the script's existing schema (`type`, `video_id`, `summary`, `evidence`, `cause`, `action`, `verification`). Put prevention instructions in `action` and explicit open/verified status in `verification`. Never record a successful recipe until the result was actually reviewed.

## Current session limitations

**2026-11-19:** yt-dlp listed every reference channel's uploads (titles, durations), but every individual YouTube video page returned the sign-in bot check, and Newgrounds returned HTTP 403. Not bypassed. Footage review needs the owner's exported cookies file or uploaded clips. See `STICK_COVERAGE_REVIEW_2026-11-19.md`.


On 2026-11-17, the latest Philosopher MP4 could not be downloaded in this environment; no fresh animation verdict was obtained. The external video-watch service had insufficient credits and charged none. YouTube's browser watch page showed a verification challenge; no challenge was solved. Agent-Reach installation/use must be reported from the actual command result, never assumed from this document.

Actual Agent-Reach result: `research_gateway.py status` returned `NOT_INSTALLED`. An owner-authorized installation was attempted with the official `uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip` source. It failed to download because the execution host could not resolve `github.com`. Agent-Reach was not installed or used to retrieve reference content. Retry only when normal network access is available; do not weaken network restrictions or substitute the unrelated PyPI package.
