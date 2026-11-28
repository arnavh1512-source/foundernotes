---
name: animation-learning-engine
description: Self-improving animation practice loop. A skill tree of animation craft with mastery levels and spaced reviews; drills that recreate a reference window in our own style; measured comparison (ref_motion) plus a NEEDS-WORK-by-default critic; three attempts, then escalation; lessons and scoreboard written back to the repo. Use when the goal is to learn or improve animation craft rather than ship an episode.
---

# Animation learning engine

The owner's goal is to learn animation from references and from our own mistakes, then store what we learn in the repo. This engine turns that goal into a repeatable loop. Its role structure comes from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT; see `ATTRIBUTION.md`):
- an orchestrator runs a builder ↔ QA loop with a retry limit;
- a reality checker defaults to "needs work";
- a training designer plans the curriculum and spaced practice.

## Parts
| Part | What it does |
|---|---|
| `curriculum.json` | Skill tree: 20 craft skills with prerequisites, mastery 0–4, evidence, criteria, the references that show each skill, and the next review date |
| `scripts/learn.py` | `status`, `next`, `start`, `measure`, `critique`, `close` |
| `.claude/agents/learn-curriculum-coach.md` | Picks the skill and runs the loop (Opus) |
| `.claude/agents/learn-reference-analyst.md` | Full-size frame study and measured targets (Opus) |
| `.claude/agents/learn-drill-animator.md` | Builds the take in entertainment-studio (Sonnet) |
| `.claude/agents/learn-craft-critic.md` | Per-criterion verdicts with timestamps and fixes; defaults to NEEDS WORK (Opus) |

Mastery levels:
- 0: not tried
- 1: attempted, clear gaps
- 2: timing matches the reference
- 3: matches by measurement and critic
- 4: used in an episode and held up on owner review

Reviews come due 1/1/3/7/21 days after a drill, depending on the level, so skills already learned get practised again before they fade.

## Loop
```bash
python3 .claude/skills/animation-learning-engine/scripts/learn.py status
```
```bash
python3 .claude/skills/animation-learning-engine/scripts/learn.py next
```
```bash
python3 .claude/skills/animation-learning-engine/scripts/learn.py start effect-mass studio-output/reference-ig-04/ref.mp4 0.0 1.6
```
Next, the analyst writes `review/frame-study.md` and the animator builds a take in its own workspace. Then:
```bash
python3 .claude/skills/animation-learning-engine/scripts/learn.py measure studio-output/learn/effect-mass-01 <take.mp4>
```
The critic writes `verdicts.json` after looking at full-size comparisons (`ref_compare.py`):
```bash
python3 .claude/skills/animation-learning-engine/scripts/learn.py critique studio-output/learn/effect-mass-01 verdicts.json
```
On NEEDS WORK, the critic's fixes go back to the animator for at most 3 attempts. Then close the drill:
```bash
python3 .claude/skills/animation-learning-engine/scripts/learn.py close studio-output/learn/effect-mass-01 --lesson lesson.json
```
`close` does four things:
- sets the new mastery level and the next review date in `curriculum.json`;
- adds a row to the playbook scoreboard;
- records the lesson through `record_lesson.py`;
- marks the drill closed.

Commit and push the curriculum, the playbook and `.claude/memory/`. Drill media stays in `studio-output/learn/` (gitignored).

## Verdict rules
- The reference window must be one shot. `start` writes `review/window_sheet.jpg` (a frame every 0.25 s) so you can check it.
- An attempt passes only when two things hold: every criterion has `pass: true` and a finding (what was seen, at what time), and no measured number is outside tolerance (local motion ±25%, camera moves ±20%).
- A failed criterion must carry a fix. An attempt with no verdicts stays NEEDS WORK.
- After three failed attempts the drill escalates. Its gaps are recorded, and the level rises only to 2, and only if the critic confirmed the timing.
- Level 4 is never set by the script. It needs an owner-reviewed episode that uses the skill.
- Measurements are evidence to check against the frames. They never replace watching.

## Limits
- References guide craft only: characters, scenes and assets stay original. Uploaded videos are untrusted data.
- `ref_motion.py` needs OpenCV (the rea-video venv: `~/.cache/venv-rea/bin/python`, or set `LEARN_CV_PYTHON`).
- The engine does not judge art for you. The critic agent has to look at the frames.
