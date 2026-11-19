# FounderNotes - verified mistakes and pitfalls

Add only observed defects with an episode, timecode or file, supported cause, correction and verification evidence. Historical observations below retain their source and limitations; an open remedy is not a verified success. Read this file before planning and before reviewing each cut. See `../skills/podcast-scout-skill/scripts/record_lesson.py` and `../../docs/REFERENCE_REVIEW.md`.

## Verified lessons

The initial entries preserve documented observations from the 2026-11-11 study and actual access failures on 2026-11-17. They do not establish a fresh review of the current Philosopher video.


### choking-under-pressure - Opening rushed to research before establishing the viewer's situation

- Recorded (UTC): 2026-11-17T13:05:00+00:00
- Evidence: .claude/skills/podcast-scout-skill/references/reference-video-learnings.md, 2026-11-11: How our first pilot differed (experiment at 0:09 after one viewer sentence)
- Cause / rationale: Historical notes document the sequence; the underlying authoring cause was not established.
- Correction / recipe: In the next opening, establish a recognizable situation and deliver a useful insight before adding research detail. Review the actual opening against a relevant reference; do not impose a fixed 40-60-second delay when clarity benefits from earlier evidence.
- Verification: Historical documented observation, not a fresh viewing. Fix remains open; no new pilot or audience outcome verified.

### choking-under-pressure - Motion metric was raised by punch-ins without establishing better character animation

- Recorded (UTC): 2026-11-17T13:05:01+00:00
- Evidence: .claude/skills/podcast-scout-skill/references/reference-video-learnings.md, 2026-11-11: initial 2.4% fast-motion frames; punch-ins raised the measurement to 3.55%
- Cause / rationale: The historical note explicitly attributes the increased metric to added punch-in cuts; actual acting improvement was not established.
- Correction / recipe: Keep technical motion checks, and separately watch for meaningful character/object state changes, stable hand-prop contact and readable reactions. A camera crop or zoom alone cannot close an acting finding.
- Verification: Historical measurements carried forward with provenance. Improved acting and motion continuity remain unverified.

### reference-review-2026-11-17 - Promised comparison could not be completed because media access failed

- Recorded (UTC): 2026-11-17T13:05:01+00:00
- Evidence: docs/REFERENCE_REVIEW.md, Current session limitations; gateway status NOT_INSTALLED and official uv tool install DNS failure on 2026-11-17
- Cause / rationale: Local media transfer failed; Agent-Reach was absent and its official release host could not be resolved. Browser playback also hit verification and the analysis service lacked credits.
- Correction / recipe: Run the gateway status at session start, preserve actual retrieval results, and mark unavailable reference footage pending. Complete useful production documentation, report the blocker plainly, and obtain accessible footage before assigning motion/voice passes.
- Verification: Blockers observed in this session. No fresh comparison, animation improvement or successful Agent-Reach installation is claimed.

### philosopher-motion-study-cut-1a - Scaled drawing strokes failed before encoding

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Pillow ImageDraw.line expects integer widths; scaled character limbs produced float widths.
- Correction / recipe: Round widths in the shared line helper. Run the all-shot deterministic rendering test before encoding.
- Verification: Two local tests passed and the revised 24-second MP4 encoded successfully. This verifies rendering, not artistic quality.

### philosopher-motion-study-cut-1a - Pointing hand was hidden by the table

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Characters were drawn before the tabletop, which then occluded the hand.
- Correction / recipe: Composite the pointing forearm and hand above the tabletop. Check occlusion in all prop interactions before final render.
- Verification: Revised stills at 5.8 and 7.7 seconds show the hand visible. Complete motion and anatomy remain pending.

### philosopher-motion-study-cut-1a - Map finger shortcut and premature route reveal

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Finger position used one straight interpolation while the map route had two segments; ink was drawn by whole segment.
- Correction / recipe: Use matching segmented positions and progressive ink reveal. Preserve a regression check that later ink is absent early.
- Verification: Revised map samples and the ink-reveal regression passed; full temporal review is pending.

### philosopher-motion-study-cut-1a - Stair traversal lacked planted foot positions

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Root moved along a diagonal while legs used a generic horizontal walking stride.
- Correction / recipe: Compute alternate planted and lifted feet from the actual stair coordinates. Check foot contact, weight transfer and sliding in playback.
- Verification: Revised samples at 15.8 and 18.3 seconds show tread contacts; complete walking cycle and weight transfer remain pending.

### philosopher-motion-study-cut-3 - Foreground arm replacement duplicated the base arm

- Recorded (UTC): 2026-11-17T13:28:56+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; Cut 3 study stills and Cut 3a at 7.7 seconds; revised SHA-256 e6b174358ac802132ad7523d1bbfb77d6dadbc86d6d8cf487b49f0de48fccabf
- Cause / rationale: The character drew its original right arm before the table; a separately composited foreground arm was added without suppressing the original.
- Correction / recipe: Suppress the original arm when a foreground replacement is drawn. Inspect complete limb silhouettes and count hands in all replacement poses; preserve two-link length checks.
- Verification: Cut 3a frame at 7.7 seconds inspected after rerender; duplicate absent there. Full playback, independent critique and reference comparison remain pending.

### philosopher-stick-performance-v1 - Hand contact and second-character arrival snapped between states

- Recorded (UTC): 2026-11-17T13:49:02+00:00
- Evidence: docs/STICK_PERFORMANCE_REVIEW_2026-11-17.md; v1 decoded sample positions at 2.95/3.125 and 7.2/7.4 seconds; v3 source hash 644f25a1f2112b81938c0c2981c3bbbd458572e9eda79e393828f9c89256968a
- Cause / rationale: A Boolean grip state switched hand position instantly; the entering character first appeared already inside the frame.
- Correction / recipe: Interpolate a full reach and release and start the second character beyond the frame edge. Review entry, contact and release boundaries in decoded frames and actual playback.
- Verification: v3 sampled poses inspected and grip-weight boundary tests passed. Full motion, foot sliding and sound review remain pending.

### philosopher-stick-performance-v2 - Resting stick arms folded into awkward triangles

- Recorded (UTC): 2026-11-17T13:49:02+00:00
- Evidence: docs/STICK_PERFORMANCE_REVIEW_2026-11-17.md; v2 sampled render and v3 decoded frames at 1.5/2.8/3.25/5.7/7.5/10.5 seconds
- Cause / rationale: The rest pose reused a long contact-arm IK configuration and an unsuitable bend direction; moving the hand alone did not define a readable rest silhouette.
- Correction / recipe: Define resting upper/forearm angles and rotate fixed-length segments toward the contact pose. Place the torso within reach instead of stretching bones. Check rest silhouette as well as final contact.
- Verification: v3 sampled arms read without the prior folded rest triangles. All intermediate arm lengths and the final contact endpoint pass a geometry test. Natural full playback and reference parity remain pending.

### stick-performance-rebuild-contact-revision - Recovery and stair interpolation moved supposed support feet

- Recorded (UTC): 2026-11-17T14:15:48+00:00
- Evidence: Source at commit 12eb1da5f309b60636903c1ce32fd68836fbe5ee: foot 1 moves from [650,830] at 4.15 s to [630,830] at 4.8 s; foot 0 moves from [420,800] at 9.4 s to [350,770] at 10.5 s without a lift arc. These are source/geometry observations, not playback findings.
- Cause / rationale: Pose keys changed contact positions during recovery and changed both feet during a stair step; prior tests only held the initial force-phase foot.
- Correction / recipe: Hold both recovery contacts through 7.0 s, lift the repositioning foot during 7.0-8.3 s, then alternate fixed support and lifted stair steps. Test each support interval and intermediate clearance.
- Verification: Local Node test runner: all 3 tests passed, covering 316 sampled poses with unchanged reach, bone lengths and grip checks plus new recovery/stair support checks. No clamped limb in 316 samples. Revised rendered motion remains unreviewed; local artifact download DNS failed and browser file navigation was blocked by policy. Keep draft status.

### stick-performance-preview-review - Correct limb lengths hid crossed silhouettes and a missing action payoff

- Recorded (UTC): 2026-11-17T14:29:34+00:00
- Evidence: docs/STICK_VISUAL_REVIEW_2026-11-17.md; actual browser previews of the prior contact revision at 0.0/4.8/10.5 seconds showed crossed neutral knees, folded rest arms and stairs ending without a destination.
- Cause / rationale: The IK used opposite knee branches for the two legs, short rest-arm targets and low neutral pelvis keys; tests checked lengths/contact but not silhouettes. The storyboard ended before the chosen route reached anything.
- Correction / recipe: Extend neutral poses, use coherent knee facing with a nearly straight turn, revise force poses for separation, thin strokes, and connect the stairs to an open arch with a complete arrival. Add support and silhouette invariants.
- Verification: Five local Node tests and offline builder passed. Final browser poses at 0/2.5/3.5/4.15/5.8/14.5 seconds and six screenshots of the running preview inspected. Specific silhouettes and visible arrival improved in those samples. Encoded MP4, full temporal review, sound, independent critique and benchmark parity remain pending.

### stick-timing-revision - One easing curve stopped every stride and obscured a faster loss of support

- Recorded (UTC): 2026-11-17T14:57:12+00:00
- Evidence: docs/STICK_TIMING_REVIEW_2026-11-17.md; source prior to timing pass used progress for every pelvis/torso interpolation and fixed toe direction. Browser candidate at 2.78 s additionally showed knee-elbow overlap.
- Cause / rationale: All movements shared a symmetric start/stop curve; acting phases lacked independent timing and the brace contact was too high for the preload silhouette.
- Correction / recipe: Delay reach, add a load, accelerate the slip, lead the head turn, carry the stair root, turn fixed-length toes and lower the bracing contact. Preserve support/grip invariants and review the actual motion.
- Verification: Seven Node tests passed and builder executed. Final 2.78/3.5 s browser poses and six running-preview screenshots inspected after brace correction. Full-rate CI is configured; encoded motion, sound and creative approval remain pending.


### stick-route-reveal-2026-11-17 — The alternative route was visible before the intended discovery

- Recorded (UTC): 2026-11-17T16:06:12+00:00
- Evidence: docs/STICK_REVEAL_REVIEW_2026-11-17.md; baseline encoded SHA f03004bb20de71496a636b88b9e9dcbf647a56b0cfc2426de986443d72232fd0 at 0/6.2 seconds; revised encoded SHA 1b9db90aa9eee238fa013738e9f4ca13f872e311e7bb7121fbd486d0fbaf0bc3 at 0/6.2/6.5/6.7/7.2 seconds.
- Cause / rationale: One fixed wide composition showed the open arch throughout the failed gate attempt and reassessment.
- Correction / recipe: Stage the failed tactic more closely, then widen only after the head turns. Reuse the existing camera matrix helper, keep world/contact coordinates fixed, and protect figure bounds and reveal timing with tests.
- Verification: Eight local Node tests passed. CI run 44120771407 passed and its exact MP4 was downloaded and decoded. Selected encoded frames and all 36 frames of the reveal transition were inspected. Arch visibility timing verified; comprehension, continuous playback, sound and artistic approval remain pending.

### stick-rebuild-cut-1 — Silent stick exercise used one continuous camera for 14.5 s with zero cuts

- Recorded (UTC): 2026-11-19T03:11:32+00:00
- Evidence: cut-1 sha 6a8c6c88... sheet; benchmark notes reference-video-learnings.md (median shot ~3 s, framing changes around object/action)
- Cause / rationale: Exercise was built as a single camera move; coverage (close-ups, inserts, cut on action) was never planned
- Correction / recipe: Plan coverage per beat before animating: close on the contact/obstacle during effort, cut on action, eyeline insert for what the character looks at. Test that each close/insert frames its subject and that no shot is under 0.5 s.
- Verification: Internally fixed in cut-3 (sha 26c438db...); 11 tests pass. Reference parity pending: footage blocked.

### stick-rebuild-cut-1 — After the reveal the figure shuffled up three steps for ~5 s and ended in a neutral stand

- Recorded (UTC): 2026-11-19T03:11:32+00:00
- Evidence: cut-1 per-second mean frame diff 0.32-0.53 at 8-13 s vs 2.2-8.7 during strain/reveal
- Cause / rationale: Stair keys spaced ~1 s apart with linear body travel; no story beat planned after arrival
- Correction / recipe: Once a character has decided, move decisively (~0.6 s per step) and give arrival a payoff (look back at the obstacle, release, exit). Test: no 2 s window after the reveal without visible motion.
- Verification: Internally fixed in cut-2/3; frame-diff and tests rechecked. Real-time viewing and reference parity pending.

### stick-rebuild-cut-3 — Blank stick heads left frustration and relief unreadable

- Recorded (UTC): 2026-11-19T03:19:06+00:00
- Evidence: cut-3 frames 4.8-6.2 s and 13.0-13.4 s; DayOne Films D8T891uWpiE storyboard thumbnails (2026-11-19) show 2-3-stroke faces carrying each emotional beat
- Cause / rationale: Emotion was left to body poses alone, and the frustration and relief poses were near neutral
- Correction / recipe: Plan an expression per beat (eyes, brows, mouth) alongside the pose; distinguish effort (wide gritted mouth, brows down) from shock (wide eyes, round mouth). If the target is Alan Becker's faceless style, push the body pose instead and test readability without the face.
- Verification: Cut 4b stills at 3.2, 4.1, 5.3, 6.6, 12.0 and 13.6 s read as distinct expressions in medium and close shots; tiny in wide shots. Real-time viewing, owner style decision and reference parity pending.

### stick-rebuild-cut-5 — Stick character read as a 'stick insect': tiny head, long neck, thin lines

- Recorded (UTC): 2026-11-19T05:48:35+00:00
- Evidence: Owner note 2026-11-19; cut-5b head about 1/7 of height, neck about 55 px, lines 7-10 px (<2% of height); Alan Becker AvA frames (Qb1VvUf21L4) show a head about 1/4-1/5 of height on the body and heavy even strokes (visual estimate)
- Cause / rationale: Rig followed 'slender figure' guidance with realistic limb lengths and a separate neck; proportions were never compared to the benchmark
- Correction / recipe: Check proportions against the benchmark before animating: big head sitting on the shoulders, no neck, line weight about 3% of height. Keep a test for head/height ratio and head-to-chest distance.
- Verification: Cut 6 stills read as a sturdy stick figure; 14 tests pass. Owner confirmation and full-speed viewing pending; legs still about 51% of height.

### stick-rebuild-cut-4 — The failure beat sagged instead of being a full-body event

- Recorded (UTC): 2026-11-19T05:48:35+00:00
- Evidence: cut-4b 3.8-5.8 s mean frame difference 1.13; Alan Becker AvA 96-97 s frames show an airborne, upside-down tumble and overlapping action; Geometry Dash mean motion 12.3 vs our 2.4
- Cause / rationale: Slip keyed as a short lowering of the hips with feet planted; no airborne phase, impact or world reaction
- Correction / recipe: Stage failures as release, airborne, impact with squash and bounce, an emotional reaction and recovery; make the obstacle react (spring back, settle). Use different easing per phase: ease out of a release, accelerate into an impact.
- Verification: Cut 5b: 3.8-5.8 s mean frame difference 2.87; tests check the airborne tilt, feet off the floor, squash/bounce, accelerating fall and gate swing. Full-speed viewing against Alan pending.

### stick-rebuild-cut-10 — Stick exercise had no sound while the benchmark puts an effect on every contact

- Recorded (UTC): 2026-11-19T06:01:27+00:00
- Evidence: Alan Becker AvA (Qb1VvUf21L4): ~2.4 sound hits/s, sound present 34% of the time, -16.4 LUFS, LRA 13.9; Geometry Dash 1.7 hits/s over music, -16.6 LUFS. Our cut 10 had no audio stream.
- Cause / rationale: Sound was deferred until narration; contact moments never had sound events
- Correction / recipe: Keep a SOUND_EVENTS list beside the pose keys, tied to contacts (steps on plants, impacts on IMPACTS, grip and release on the gate), and synthesise original effects (stick-sfx.py). Check hit density, onset sync within one frame, and loudness against the benchmark; avoid stacking a soft event inside a louder tail.
- Verification: Cut 11: 2.14 hits/s, sound present 43%, 23/23 effects within one frame of their contact, -17.3 LUFS two-pass (benchmark ~-16.5). Actual listening by a person still pending; the assistant cannot hear audio.

### stick-rebuild-cut-11 — Key actions moved with one soft, even easing and effects faded linearly

- Recorded (UTC): 2026-11-19T06:06:56+00:00
- Evidence: Alan Becker AvA (Qb1VvUf21L4) 56-57 s frames: the blast reaches full size in ~5 frames, lingers ~0.8 s while dulling, and the frame tilts on impact; our cut 11 reach and dust ramped evenly
- Cause / rationale: A single smoothstep easing was reused for most segments; effects used linear growth and fade
- Correction / recipe: Give key actions anticipation (a small counter-move) and snap easing; build effects fast and fade them slowly with a colour shift; tilt as well as shake on big impacts. Keep tests for the wind-up, crouch, counter-move and snap speed.
- Verification: Cut 12 frames show the hands pull back then reach the bars in two frames, and the dust bursts and lingers; 17 tests pass. Real-time viewing by a person pending.

### master-study-ava-jump — Limbs longer than the joint spacing forced permanent bends (bow legs, boxy elbows, folded legs)

- Recorded (UTC): 2026-11-19T06:18:42+00:00
- Evidence: Private master study of Alan Becker AvA (Qb1VvUf21L4) 25.3-26.9 s, key drawings measured on a grid: his standing legs form a straight upside-down V and arms hang straight; our first copy with arms 36+36 and legs 40+40 showed bent knees and elbows in every pose; arms 27+27 and legs 32+32 fixed standing and landing. His figure: 170 px tall, head 60 px (about 1/3), lines 10-11 px.
- Cause / rationale: IK limb lengths were chosen for reach, not for the neutral joint spacing, so the solver always bent the joints
- Correction / recipe: Set limb lengths close to the neutral joint spacing so rest poses read as straight strokes; bend only for action. Heads about 1/3 of height for Alan-style figures. Time jumps with a ~2-drawing wind-up, ~0.3 s air time and a landing squash held about 3 drawings.
- Verification: Study render compared drawing by drawing with the reference at 8 fps: standing, crouch and landing now match; the jump peak still tucks. Not yet transferred to the main stick rig.

### stick-rebuild-cut-14b — Character read as stiff: arms froze in one shape and holds were dead still

- Recorded (UTC): 2026-11-19T06:33:59+00:00
- Evidence: Owner QC 2026-11-19 'still stiff'; cut 14b 5.4-6.6 s frames show identical arm shapes for 18 frames; 30% of non-grip frames had elbows moving under 0.5 px. Alan's AvA frames change the arms in nearly every drawing.
- Cause / rationale: Hands were interpolated in straight lines with the body and stopped dead on keys; holds had no motion; no acting was planned for the arms between big beats
- Correction / recipe: Plan an arm acting choice for every beat (e.g. brushing off the hands after the fall), add follow-through springs on free hands with contact blending, arcs, breathing holds and spine drag. Measure frozen-arm frames and also look at frames: the procedural pass alone moved the number but not the picture.
- Verification: Cut 15b: frozen-arm frames 9%, brushing beat visible at 5.8-6.2 s, 18 tests pass. Owner re-check pending; legs and torso still rigid on holds.

### stick-rebuild-cut-15b — Hands looked odd: elbows jutted sideways or forward and arms folded at rest

- Recorded (UTC): 2026-11-19T06:42:29+00:00
- Evidence: Owner QC 2026-11-19 'the hands are so odd'; cut 15b frames at 5.9, 6.0, 6.6, 9.2 and 12.0 s show hand-on-hip and robot-like elbows; free hands sat ~120-160 px from the shoulder against a 174 px arm
- Cause / rationale: A fixed IK bend sign for both arms plus hand targets too close to the shoulders, which forced large elbow bends; knob dots at the hand ends
- Correction / recipe: Keep relaxed free hands near full arm reach (near-straight strokes, as in the Alan master study), track each elbow's bend side with hysteresis (switch only near full extension), place contacts and deliberate gestures where the arm can stay long, and draw hands as rounded stroke ends. Check elbow jumps per frame and strongly bent free arms, and look at frames.
- Verification: Cut 16d frames at 0.4, 1.0, 6.6, 9.2, 12.0 and 13.6 s show relaxed straight arms; strongly bent free arms 10%; no elbow flips among large jumps; 18 tests pass. Owner re-check pending.

### stick-rebuild-cut-16d — Body froze on holds: hips, torso and knees did not move for up to 1.4 s

- Recorded (UTC): 2026-11-19T06:45:06+00:00
- Evidence: Frozen hip/torso/knee frames 23% in cut 16d, with stretches at 5.83-6.43 s, 10.93-11.23 s and 11.63-13.07 s; Alan's AvA pose changes nearly every drawing; owner QC 'still stiff'
- Cause / rationale: Holds were keyed as identical poses and only the face or arms changed; a labelled 'breathe' beat carried no breath
- Correction / recipe: Give every hold a whole-body acting choice (weight shift, lean toward what the character thinks about, a sigh or breath through the shoulders, knees giving). Measure frozen body frames and list the frozen stretches, then look at the frames. Keep only short, deliberate dramatic holds.
- Verification: Cut 17: frozen body frames 13%, the breath and look-back lean visible in frames, 18 tests pass. Owner re-check pending.

### stick-rebuild-cut-19 — Getting up from the floor looked wrong: knotted legs, frog squat, elevator rise

- Recorded (UTC): 2026-11-19T06:56:58+00:00
- Evidence: Owner QC 2026-11-19 'the moment he stands is not good'; cut 19 frames 5.0-6.0 s; feet slid under the hip and the hip rose vertically with a straight torso
- Cause / rationale: The push key tucked the feet straight under the hip and raised the body vertically; re-proportioning also sank seated hips to the floor and dragged them over the feet, folding the legs flat so the knees flipped
- Correction / recipe: Animate get-ups on the weight-over-base principle: tuck with the front foot ahead and the back leg folded under, rock the head and chest out over the feet, push off a knee, rise while leaning, then steady with a short step. Keep seated hips on the seat when re-proportioning. Check per-frame knee jumps and frames.
- Verification: Cut 20 stand-up frames read as kneel-to-stand; knee flips 0; 19 tests pass. Owner re-check pending.
