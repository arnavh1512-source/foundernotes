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

## Cut 4: first real reference footage, then facial expression
**Access.** With the owner's own YouTube cookies, YouTube accepted requests from this server but offered only storyboard thumbnails (320×180, about one every 2 s), not video streams. These were fetched for Alan Becker's "Animation vs. Game Design" (`dz04yXwSkQY`, 3:12) and DayOne Films' "SELF RESPECT" (`D8T891uWpiE`, 2:34). Minutes later YouTube returned 401 for further requests (the session was most likely revoked after use from a new location), and both local copies of the cookies were deleted. The thumbnails stay private in git-ignored `studio-output/references/`. They support shot-structure and pose observations only; timing, motion quality and sound remain unreviewed.

**DayOne storyboard observations.** Plain round heads carry emotion with two eye dots, two brow strokes and a mouth line (crying, determined, smug, content). One recurring prop stands for the abstract idea: a price tag re-marked in insert shots ($100 → $80 → $20 → $50 → $80). Bookended settings show change (2 a.m. bed and phone: sad early, calm later). A shadow figure personifies the inner voice. A new picture in nearly every thumbnail.

**Alan storyboard observations.** Much of the sampled film is a sponsored tablet-app segment. Character frames show an ensemble reacting in clearly different whole-body poses in the same shot (sprawled on the floor, arms thrown up, leaning in), framing that changes in nearly every thumbnail, and characters handling the world's objects. His figures have no faces.

**Cut 4 change.** A per-beat face track (`faceAt`): curious, focused, strain (squeezed eyes, wide gritted mouth), shock (wide eyes, round mouth), frustrated, noticing, determined, breathing, wistful look-back, relieved (eyes closed, smile), content, plus two short blinks. Twelve tests pass. Render (cut 4b, committed source) SHA-256 in the comparison record; decodes fully at 1920×1080, 30 fps, 435 frames.

**Owner benchmark (2026-11-19): reach Alan Becker's level.** Alan's figures are faceless; his acting lives in whole-body poses, timing, physics and choreography. The face follows DayOne's approach and is an open owner decision for the stick core. Gaps to Alan's level, in order: (1) motion quality and timing (snappy anticipation, overshoot, smears, follow-through; our keyed IK motion is smooth and even); (2) pose range and exaggeration (airborne, compressed and stretched poses; ours stay mostly upright); (3) physical interaction where the world reacts (our gate only rattles); (4) ensemble acting; (5) sound. These need real video at full frame rate, not thumbnails, to judge.

## Cuts 5–6: real Alan Becker footage
**Access.** The owner downloaded and uploaded "Animator vs. Animation (HD)" (`Qb1VvUf21L4`, 132.8 s, 990×720, 29.97 fps) and "Animation vs. Geometry Dash" (`C637UcpHfNY`, 143.1 s, 1280×720, 23.98 fps). They stay private in git-ignored `studio-output/references/alan/` for study only; nothing is reused.

**Measured (frame differences on 320 px greyscale; scene detection at 0.3):**
| | AvA original | Geometry Dash | Our cut 4 |
| --- | --- | --- | --- |
| Hard cuts | 0 | 0 | 7 |
| New drawings per second | ~17 (43% held frames) | ~23 | ~26 |
| Mean motion per frame | 2.0 | 12.3 | 2.4 |
| Low-motion seconds | 19% | 3% | 21% |
Alan stages both films as one continuous screen (pushes and pans, almost no hard cuts); the energy comes from character motion. Our coverage cuts come from the DayOne and psychology references, not from Alan.

**Observed in frames.** AvA sampled every 5 s shows a new silhouette in nearly every sample (crouching, flying horizontally, crawling, hanging, kicking, lying flat); the cursor and tools act on the character; objects get drawn and used; the timeline breaks with flying debris. One second at full frame rate (96–97 s) shows a body tumbling upside down, a chain of figures whipping in an arc with each body trailing the last (overlapping action), several actions at once, and drawings changing about every second frame.

**Cut 5 (SHA-256 `e371613a…`, as 5b).** The slip became a full-body event: grip release (ease-out), airborne with the spine tipped back past 40° and both feet off the floor, an accelerating fall into a sitting impact, squash and bounce, a frustrated fist slam, and a push back to standing. The gate springs back and settles while staying locked. Motion in 3.8–5.8 s rose from 1.13 to 2.87 mean frame difference.

**Cut 6 (SHA-256 `612da2b7…`).** Owner note: "the character looks like a stick insect man". Ours had a head about 1/7 of body height, a visible neck about 55 px long and 7–10 px lines (under 2% of height). Alan's figures (visual estimate from AvA frames) have a head about 1/4–1/5 of height sitting on the body and heavy even strokes. Fix: head radius 31 → 47, positioned on the chest with no neck, lines 7–10 → 13–17 px, face scaled with the head. Poses and motion are unchanged. Fourteen tests pass, including a proportion check.

**Remaining gaps to Alan's level.** Legs about 51% of height (somewhat long); timing still smoother and more even than his (more holds and snaps needed through the whole piece, not only the fall); the world reacts only at the gate; no ensemble; no sound; the face remains an open owner decision (Alan's figures are faceless).
