# Coverage and payoff revision: gate-to-arch exercise
Date: 2026-11-19. Internal craft revision; not creatively approved. Three-cut budget used (cut 1 baseline, cuts 2 and 3).

## Reference access this session
yt-dlp 2026.10.26 (new research-gateway default for YouTube) listed every reference channel's uploads with titles and durations, but every individual video page returned YouTube's "Sign in to confirm you're not a bot", including with a JavaScript runtime. The Newgrounds original of Animator vs. Animation returned HTTP 403. Nothing was bypassed. Comparisons therefore use the benchmark notes already on record: `ALAN_BECKER_STUDY.md`, `BENCHMARK_CORRECTION_2026-11-17.md` (Animator vs. Animation frame samples) and `reference-video-learnings.md` (two supplied psychology explainers). All reference criteria stay **pending** until footage is reviewed. To unblock: the owner's own exported cookies file (`--cookies`, stored outside the repo) or owner-uploaded clips.

Listing metadata only: DayOne Films uploads run about 2.5–4.5 minutes; PsychToonsHQ and PsychDoodleTV about 13–16 minutes.

## Renders (local Playwright, 1920×1080, 30 fps, 435 frames, silent; all decode fully)
| Cut | SHA-256 | Change |
| --- | --- | --- |
| 1 | `6a8c6c8821698eefdf04fd75bb31ebf72c9241857f2c701ce22d0f7fe961d180` | Baseline (code at `4c5cf35`) |
| 2 | `8c22335d8f7e0b94311717a32b15e72c58030a0c26df23965c03736bcdd9da59` | Brisk climb, arrival push-in, payoff beats |
| 3 | `26c438db78bde9f7974510309bcbb29f645e7f5b57be853972860f0293e8934d` | Eight-shot coverage, stronger look-back and release (committed source) |
| 3b | `7ebe2a42e0dc3dd217520efe7118e07f4be37a53370cac644d8d868b4fc57328` | Reframed medium shot; reverted (see below) |

Local rendering now works in the cloud container (the earlier Chromium socket failure did not recur).

## Findings and fixes
1. **Late stillness (cut 1).** Per-second mean frame difference was 0.32–0.53 from 8 to 13 s against 2.2–8.7 during the strain and reveal: a small figure shuffled up three steps for about five seconds and ended in a neutral stand. Fix: about 0.6 s per stair step (the character has decided), arrival at 10.6 s instead of 13.3 s, then breathe, look back at the still-locked gate with a hand on the arch frame, release, and recede into the arch (figure scales about its floor contact). New test: no 2 s window after the reveal without visible motion.
2. **Single-camera coverage (cuts 1–2).** One continuous camera for 14.5 s with zero cuts, against a measured median shot of about 3 s in the supplied explainers and framing that changes around the object or action. Fix: medium; close on the grip and padlock during the strain (2.9 s); cut on the slip (3.8 s); continuous widen after the head turn (6.2 s); arch push-in (10.6 s); face close-up for the look-back (11.5 s); padlock eyeline insert (12.4 s); arch (13.0 s). Tests check that every close-up or insert frames its subject, that full shots keep the whole figure in frame, and that no cut is shorter than 0.5 s.
3. **Look-back too small (cut 2).** A 19 px head shift did not read. Cut 3 leans the chest and head toward the gate (head 30 px past the chest) and holds the look through the insert; the release drops the chest and head by more than 12 px.
4. **Stair stub visible before the reveal (all cuts).** Cut 3b reframed the medium shot to hide it but crowded the figure against the left edge during the slip and left the right 40% empty. Reverted. Resolve it in the pilot's world layout, not by a camera shift.

## Still failing or pending
- **Acting range:** frustration after the slip and relief at the end are close to neutral poses; the blank head carries no expression. Next: a distinct frustrated beat after the catch and a clearer exhale; test a minimal eye or brow cue against the benchmark once footage is available.
- **Sound:** none. Contact effects on grip, rattle, slip and arrival, then actual listening.
- **Pacing:** shots now run 0.6–4.4 s (median about 1.2 s); retime to narration in the pilot.
- **Reference parity:** pending for every criterion until footage is reviewed.

Full per-criterion record: `studio-output/stick-rebuild/review/cut-3-comparison.json` (local, not committed). Lessons recorded with `record_lesson.py`.
