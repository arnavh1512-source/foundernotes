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

### night-1-part-2 — Splitting narrator segments into character lines misaligned pictures: scene spans ran into the next character line (knife line played over the previous scene at 1:35).

- Recorded (UTC): 2026-11-23T04:59:20+00:00
- Evidence: Frame check of render 2026-11-21: caption 'Then suppose you'd had a knife on you' over whereGoal scene at 95 s.
- Cause / rationale: timing.js mixed split line ids and grouped scene ids; SPAN used the next key in object order instead of the next scene in original order.
- Correction / recipe: Write SEG only for original scene ids in original order, each spanning first-to-last of its lines (groups.json + scene_order.json); snap multi-shot boundaries to line starts; check one frame per scene against captions before rendering.
- Verification: Fixed render 2026-11-22 frame check at 22.5 s, 95 s, 530 s, 860 s matched captions.

### night-1-part-2 — Meeting the anti-slideshow motion gate with zoom pulses; owner rejected constant zoom in/out.

- Recorded (UTC): 2026-11-23T04:59:20+00:00
- Evidence: Owner message 2026-11-22: 'not zoom in and zoom out all the time'. Estimates: no zooms 1.8%, action beats 3.85%; real QC 4.00%.
- Cause / rationale: Character gestures barely change frame pixels, so zoom cuts were used to lift qc_video's fast-motion ratio.
- Correction / recipe: Use character-led action beats and new mini-scenes (S.duo, S.keys, vignettes), fast-moving objects, meaningful background changes and impact jolts; estimate with tools/estall.sh before rendering.
- Verification: Render 2026-11-22 qc.json fast-motion 0.0400 with no zoom pulsing; owner then asked only for gesture variety.

### night-1-part-2 — Edge-clipped text and blocks (GIVING UP, FAMILIAR, still driving?) and a label under the caption band were found only after a 75-minute render, forcing another render; the owner lost the time twice.

- Recorded (UTC): 2026-11-24T06:03:03+00:00
- Evidence: Full-file frame check 2026-11-23 at 5:06, 10:42, 14:24, 7:54; owner message 2026-11-24.
- Cause / rationale: Frames were spot-checked at a few times before rendering instead of all of them; 3-word block rows and moving props were never checked at their extremes.
- Correction / recipe: Run tools/precheck.sh (a frame every 3 s) and review every sheet before any full render; for late fixes use tools/patch.sh to re-render only the changed shots.
- Verification: Fixes confirmed on 25 engine frames across the five affected shots; patch splice render in progress.

### half-landing-a03-reel,a04-reel — Foley built mostly from sub-bass is near-silent on phone speakers, where most Reels are heard

- Recorded (UTC): 2026-11-27T15:41:01+00:00
- Evidence: ep_review.low_share: boom 99.7%, splat 94.5%, A04 bass 100% of energy below 150 Hz; A04 sync 5/13 because loudness normalisation boosted the sub-bass into a flat -12 dB bed
- Cause / rationale: the sound-check boom was a 46 Hz kick low-passed at 260 Hz; the bass a 41 Hz note; the splat low-passed
- Correction / recipe: canonical .claude/skills/entertainment-studio/sound/make_foley.sh: harmonics, a mid knock and a click on every low sound; ep_review.py flags any cue sound >85% below 150 Hz
- Verification: re-measured: boom 68%, splat 0%, bass 61% below 150 Hz; ep_review phone_flags empty on A03/A04/A06/A08; A04 sync rose to 11/13

### half-landing-a03,a04-reel,a06-reel,a08-reel — A long sound tail masks the next key sound, so a story beat goes unheard

- Recorded (UTC): 2026-11-27T15:41:01+00:00
- Evidence: onset rise over the previous moment: A03 snap +2.6 dB, A04 splat +1.2 dB; ep_review flagged A06 C02 and A08 C02 as not detected
- Cause / rationale: cues ran their full length: stretch sounds through the A03 snap, the A04 launch layers over the off-screen ceiling splat, the A06 lever spring into thump 1, the A08 buzz pulses over thump 1
- Correction / recipe: cut the masking cues with the cue 'dur' option so each key sound has a breath of quiet before it; review every take with ep_review.py
- Verification: A03 snap +11.9 dB, A04 ceiling splat +24.6 dB; A06 sync 11/11; A08 thump 1 in sync (only the frame-0 buzz flagged, a measurement artifact)

### half-landing-a03,a06-reel — Stick-engine scenes: a partial pose makes the figure vanish, and a pose defined in one shot file is missing in the others

- Recorded (UTC): 2026-11-27T15:41:01+00:00
- Evidence: A03 precheck: Dev absent from S01, S02 and the start of S03; A06 precheck: page error 'GROOVE is not defined' in K04
- Cause / rationale: pose objects built without P() lack leg angles (NaN joints); each shot page loads only _common.js and its own scene file
- Correction / recipe: build every pose with P(); put anything two shots use in scenes/_common.js; run ep_build.py --precheck before every render
- Verification: re-ran the prechecks: Dev drawn in every frame; all A06 shots render

### bench-bump — Judged a reference match from thumbnails, so the face came out generic twice (owner: 'not a monkey face, look at it literally')

- Recorded (UTC): 2026-11-28T05:09:52+00:00
- Evidence: owner messages 2026-11-28; v1/v2 heads compared only on 144-216 px contact tiles; full-size reference frame (0.1 s, 1.3 s) shows brow ridge ledge, eye in socket with lashes, speckled brow, rim/front/terminator/side tone bands, specular streaks
- Cause / rationale: compared at thumbnail size and listed only story beats, never the forms and shading of the reference drawing
- Correction / recipe: before drawing, open matched reference frames at full size (ref_compare.py) and write down the forms and tone planes; review our frames the same way before showing the owner
- Verification: v3 head rebuilt from full-size frames; compare-v3.jpg shows matched forms and framing; owner review pending

### bench-bump — The subject vanished at transitions: a crossfade swapped the bump for the section, and healing went to zero before cutting back

- Recorded (UTC): 2026-11-28T05:09:53+00:00
- Evidence: owner message 2026-11-28 ('the bump just vanished suddenly'); reference 1.6-2.1 s rolls the camera so the bump dome becomes the section dome, and day 14 keeps a small dome that fades on the face 22.6-23.3 s
- Cause / rationale: transitions were built as dissolves between two drawings instead of carrying one shape across the cut
- Correction / recipe: carry the subject's shape across every transition (match cut, camera roll, same silhouette on both sides); change states gradually and never to zero on a cut
- Verification: v2/v3 frames 0-2.6 s and 21-23.3 s: bump continuous through the roll in and out, leftover dome fades over 1 s

### bench-bump,half-landing-a06-reel — An inline // comment inside a one-line function swallowed the rest of the line, the whole _common.js failed and every shot errored

- Recorded (UTC): 2026-11-28T05:09:53+00:00
- Evidence: precheck 2026-11-28: 'gridBg is not defined' (B01); node parse: SyntaxError Unexpected token ')' at _common.js:104; same failure on A06 ('up is not defined')
- Cause / rationale: a sed edit appended '// ...' to a line that continues after it
- Correction / recipe: never put // comments on code lines; comments go on their own line; run a node parse check after every scripted edit
- Verification: comment removed; _common.js parses; precheck 0 page errors

### bench-bump — Reviewed stale precheck frames after a page error and judged a change that had not been drawn

- Recorded (UTC): 2026-11-28T05:09:53+00:00
- Evidence: 2026-11-28: the mallet-handle fix looked unchanged on the sheet; precheck had exited on a page error, old frames stayed on disk
- Cause / rationale: precheck kept the previous run's frames and the error was hidden by tail in the command
- Correction / recipe: ep_build.py --precheck now deletes the previous frames and sheet first; read the full precheck output before looking at the sheet
- Verification: code change in ep_build.precheck; tests pass

### half-landing-a04-reel — Held poses were frozen: 28-30% of frame steps had nothing moving, against 1.3% in the bump reference and ~1% (over two frames) in the stick-fight reference

- Recorded (UTC): 2026-11-28T05:09:53+00:00
- Evidence: ep_review still_steps_pct: A04 29.9%, A04 rewind 28.5%; reference-ig-01 1.3%; reference-ig-03 1.0% still over 2 frames
- Cause / rationale: holds drew the exact same pose each frame
- Correction / recipe: add 'the breath' to every character (slow head bob and a hair of lean), keep something alive in every hold; ep_review reports still_steps_pct
- Verification: A04 rewind 28.5% -> 15.2% with the breath; bench-bump 7.7%

### bench-bump — The bump's colour spread into the forehead, so it read as a ball stuck on rather than a swelling

- Recorded (UTC): 2026-11-28T07:40:57+00:00
- Evidence: full-size side by side 2026-11-28 (reference 1.3 s vs ours 1.25 s): the reference keeps the red only inside the swollen part
- Cause / rationale: bump shading was drawn as ellipses inside the head clip, overlapping the unswollen forehead
- Correction / recipe: clip a swelling's shading to the region between the swollen outline and the original outline (plus a small margin); shade it in 3 flat tones with a highlight
- Verification: precheck frame 1.25 s: the red stays inside the swelling and blends into the forehead edge

### bench-bump — A tone-count measure of 'flat shading' was confounded by the engine's film grain, and a thumbnail tile showed a dark band that the full frame did not have

- Recorded (UTC): 2026-11-28T07:40:57+00:00
- Evidence: tone count (colours covering 90% of the face, 8-level bins): ref 7, ours 18 with gradients and still 19 after switching to flat planes; the B06 2.0 s tile showed a band absent from the full-size PNG
- Cause / rationale: grain noise spreads every flat colour across many bins; resized tiles can mislead
- Correction / recipe: read shading measures only on grain-free frames (or with the grain removed) and confirm every visual finding on the full-size frame
- Verification: full-size B06 2.0 s frame checked: no band; tone measure marked unreliable in the playbook

### bench-stick — First stick fight take: guard arms tangled over the heads, fighters overlapped (the fold reaction hid behind the puncher), and the launch 'blur' was a row of sharp clones

- Recorded (UTC): 2026-11-28T08:07:28+00:00
- Evidence: bench-stick take 1, frames 12-23 (0.4-0.8 s) vs reference-ig-03 9.6-10.4 s at full crop
- Cause / rationale: poses were chosen as angles without checking the silhouette; spacing set from body positions, not from where the reaction would land; ghosts drawn sharp and widely spaced
- Correction / recipe: check every key pose as a silhouette (no limb across the head or torso unless it is the point); space fighters about a fist's reach apart so the reaction reads clear; blur = 12 close ghosts under a canvas blur filter for 2 frames
- Verification: take 2: guards and jab/block read, the fold reads in silhouette for frames 17-20, the launch is a 2-frame streak; QC PASS after adding a quiet bed (sparse hits undershot loudness)

### bench-stick — Run cycle read as a hunched shuffle, then as a slide: both legs lined up under the body on the passing frames, and the forward leg swung up nearly horizontal and straight

- Recorded (UTC): 2026-11-28T08:24:43+00:00
- Evidence: bench-stick X02 frames 5.0-5.5 s (three takes) vs reference-ig-03 12.3-12.9 s at full crop
- Cause / rationale: both knees were driven by the same sin term; thigh swing 1.0 rad with a straight forward knee
- Correction / recipe: per leg: thigh .22 + .78*sin(phase), knee bends while that leg swings forward (cos>0) and keeps a bend when forward; lean ~45 deg, arms opposite the legs, poses on twos
- Verification: take 6 frames: driving stride, heel kicked up behind, never two straight legs together; QC PASS

### half-landing-a09-reel,half-landing-a12-reel — The loop check failed loops that move all the time: it demanded the last frame equal the first, which only holds for loops that end on a hold

- Recorded (UTC): 2026-11-28T08:52:17+00:00
- Evidence: A09 seam 3.15% and A12 1.44% after adding boil/hum and on-twos scrubbing; difference images showed a 1-px tremble and one twos-step of the scrub arm; typical frame steps 17.3% and 16.0%
- Cause / rationale: seam < 1% was calibrated on Reels that end on a still pose
- Correction / recipe: ep_review now also measures the 95th percentile frame step; a loop is ok when the seam is under 1% or no bigger than an ordinary step; drive looping motion from (t - shot duration) in the last shot so it lands on the first frame's phase
- Verification: tests pass; A09 and A12 loop_ok with seams 3.15% vs 17.26% and 1.44% vs 15.98%

### half-landing-a07-reel — Two rig traps: a helper constant named GW clashed with an engine global (the whole helpers file failed, 'CAM7 is not defined'); and a balance pose's back arm used a positive angle, so it shot up forward instead of reaching out behind

- Recorded (UTC): 2026-11-28T09:06:46+00:00
- Evidence: A07 precheck: 'Identifier GW has already been declared'; G03 frame at 0.5 s showed the back arm raised forward over the tray
- Cause / rationale: stick.html defines short global names; in the rig a positive limb angle points the way the character faces
- Correction / recipe: prefix episode constants (GLW, CAM7...) and read the precheck's ERR lines first; for limbs that go behind the body use negative angles
- Verification: precheck clean; G03 shows the back arm out behind and the back leg lifted (balance reads)

### half-landing-a12-reel,half-landing-a13-reel — Sparse foley kept failing loudness: our measured two-pass audio was -14.0 LUFS, but assemble.py's own single-pass loudnorm pulled the finished take down to -16.2

- Recorded (UTC): 2026-11-28T09:33:33+00:00
- Evidence: A13 takes/reel-audio.wav measured -14.0 LUFS (ebur128) while the assembled reel.mp4 failed QC at -16.2; A12 failed the same way
- Cause / rationale: two loudness stages in a row; the second (single pass, dynamic) undershoots on short clips with sparse transients
- Correction / recipe: ep_build now remuxes the measured audio into the take after assembly (picture copied), and lifts audio through a limiter when two-pass loudnorm still lands >1 LU short
- Verification: A13 QC PASS without extra cues; sync 18/18

### half-landing-a11-reel — First two-character staging tangled: the rider stopped so close to Dev that the bodies overlapped in most shots (juggle and double look unreadable); and the breath was missing because the helpers were copied from an episode made before it existed (also true of A05, A07, A09, A10, A12, A13)

- Recorded (UTC): 2026-11-28T12:12:48+00:00
- Evidence: A11 precheck: silhouettes overlapping in D01-D07; still 27.8% with no breath vs 12.0% after the breath, the rider's breath and a settling, steaming bag
- Cause / rationale: marks planned for one character; helper files copied forward from older episodes instead of the latest
- Correction / recipe: for two characters keep about a body width of clear space between silhouettes at rest and let only hands meet; reaction 3 frames after action; ep_review now warns when still frames exceed 15%; copy helpers from the newest episode
- Verification: A11 take: silhouettes separate, sync 13/13, still 12.0%, QC PASS; exported

### learn/effect-mass-01 — A drill window that spans two shots inflates the measured gap; and effects must stay alive until the shot ends

- Recorded (UTC): 2026-11-28T14:22:36+00:00
- Evidence: studio-output/learn/effect-mass-01: 0-5 s window local motion ref 12.1% vs take 4.2% (-65%); same take over the single shot 0-3 s: 9.15% vs 5.21% (-43%). review/win3/edge.jpg: ref rolls ~30 deg and pushes into the elbow at 2.8-3.4 s, then cuts inside the arm at ~3.6 s. compare_a2 t=2.5: our zap had faded while the ref's still ran the whole forearm
- Cause / rationale: Window chosen by duration, not by shot; ref_motion found no cut because the change is a roll-zoom then a wipe. Our zap faded at 2 s, so the picture went still while the label was up (repeated frames 14.1%, 3 holds of 3+ frames).
- Correction / recipe: Pick drill windows inside one shot: look at frames every 0.25 s and end the window before any roll-zoom, wipe or cut. Keep the effect alive until the shot ends: chaotic zap -> sustained chain -> settles into a clean double-outlined diamond zigzag along the nerve (chaos to clarity) -> camera roll-push into the subject leads into the next shot. Add background speed lines that flick on twos during the hold.
- Verification: Attempt 3: repeated frames 14.1% -> 0.0%, holds 3+ 3 -> 0, camera moves 2 -> 11 (ref 12), local motion 1.7% -> 4.2%. Single-shot gap still -43%: not closed (escalated after 3 attempts).
