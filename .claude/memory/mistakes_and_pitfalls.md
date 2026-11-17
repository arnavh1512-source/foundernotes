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

### philosopher-pilot-64s-first-picture — The full argument used an unvarying distant wide shot

- Recorded (UTC): 2026-11-17T18:37:22+00:00
- Evidence: CI run 44147976041, artifact 14356749290, decoded contact sheet at 14.5/20/25/41/42/45.9 seconds. docs/PHILOSOPHER_STICK_PILOT_REVIEW_2026-11-18.md.
- Cause / rationale: The study and cup shots shared the same untransformed room drawing despite different speaking intentions and a small consequential prop.
- Correction / recipe: Keep an establishing view, cut to the challenging Youth, then the replying Philosopher, isolate the cup set-down, and return to a closer two-shot. Inspect the encoded changed views and subtitle-safe area; do not declare artistic improvement from geometry tests.
- Verification: Initial wide-shot defect verified in encoded samples. Source correction at 55842bb3fbc09d0cf4fba042f09f843c751ea000; subsequently inspected its encoded overview and 24 selected close/cut samples. The final cup-arm correction is separately verified in docs/PHILOSOPHER_STICK_PILOT_REVIEW_2026-11-18.md. Continuous motion, listening and artistic approval remain pending.

### philosopher-pilot-cup-silhouette — Cup set-down swept the elbow into the face area

- Recorded (UTC): 2026-11-17T18:44:58+00:00
- Evidence: Encoded picture b63d95d3b5ee6d9359afd58ac649a44ba186b23cf968b7a1555501a08b7ce562, decoded 41.4/41.7/42 seconds. At 41.7 seconds the source elbow is [1273.33,447.06], only 12.06 pixels below the head center.
- Cause / rationale: The held-cup arm reused the Youth bend direction; the wrist passes close to its shoulder while lowering the prop, forcing the elbow around the high side.
- Correction / recipe: Use one consistent opposite bend for the Philosopher cup arm for both lift and lowering. Keep wrist attached to the actual handle; require elbow clearance below the head over the set-down. Re-render and inspect held, intermediate and settled silhouettes.
- Verification: Defect verified in encoded samples and matching geometry. Twelve tests pass after the correction, including the new elbow clearance check. Follow-up: CI44151191616/artifact14358329040, picture SHAe141561465f36b4256502908e5debda5aa66521c810d1794d7493ac721e4a743; ten decoded cup/rest/lowering samples inspected. Elbow clears the face in those samples. Full temporal and auditory review remain pending.

### philosopher-pilot-responsibility-cards — Responsibility cards named the idea without a concrete attempted task or consequence

- Recorded (UTC): 2026-11-17T19:00:17+00:00
- Evidence: Baseline picture e141561465f36b4256502908e5debda5aa66521c810d1794d7493ac721e4a743; decoded samples at31,34,36,39 seconds in the previous assembly review. docs/PHILOSOPHER_STICK_PILOT_REVIEW_2026-11-18.md.
- Cause / rationale: The scene drew three labeled rectangles on cords while the Youth changed pose; there was no everyday goal, interruption, prop handling or failed action for the viewer to follow.
- Correction / recipe: Stage written work interrupted by a phone, then incoming work and a missed catch. Preserve phone-hand contact during lift/lowering, leave the released pen on the table, start incoming work outside the frame and keep fallen papers visible. Compare changed encoded samples against the exact baseline before claiming improvement.
- Verification: Baseline defect verified in decoded samples. Thirteen geometry/contact tests pass and the viewer-first pre-script preparation still passes. Follow-up: source33e7c24390bdb53fd77665ab77631fa8ad39a0c6, CI44155539009/artifact14361645915; eighteen decoded task/transition samples inspected. The attempted work, interruption, missed catch and persistent papers are visible in those samples. Continuous/auditory/independent review and creative approval remain pending.

### philosopher-pilot-workspace-overlap — A correctly gripped phone covered the action it was supposed to interrupt

- Recorded (UTC): 2026-11-17T19:12:37+00:00
- Evidence: Intermediate task picture67e37aea, CI44153691660/artifact14359024825, SHA9d7ab20de45cdbc5d052cf0e33e23a2f8f88ee7841fe1dc2afdac26769a9ee33; decoded29.5/31/32.6 seconds plus source bounds phone845–885, writing endpoint868.
- Cause / rationale: The phone was placed on the same part of the table as the writing stroke. Bone/contact checks did not protect the visible task area.
- Correction / recipe: Move the resting phone beside the paper and shift the torso/hip/head into a supported reach. Preserve grip while lifting/lowering and require clear writing/phone bounds. Inspect the actual picture before claiming that the task reads.
- Verification: Defect verified in intermediate decoded frames and matching source bounds. Source33e7c24390bdb53fd77665ab77631fa8ad39a0c6 passes thirteen tests; Follow-up: final picture SHAe1c1f8790f631c4168d16d3074647e3fbc97b762d900dea4f1734d461773be56; decoded writing and pickup samples show the phone beside the writing stroke, preserving its visibility. Full motion/listening/approval remain pending.

### philosopher-pilot-inactive-listeners — Shot changes hid static listener acting during the study exchange

- Recorded (UTC): 2026-11-17T19:23:00+00:00
- Evidence: Baseline source33e7c24390bdb53fd77665ab77631fa8ad39a0c6; exact picture e1c1f8790f631c4168d16d3074647e3fbc97b762d900dea4f1734d461773be56; eight decoded samples15,17,21.5,23,24,25.8,27,28.7 seconds. Mentor head[1310,435] and chest[1320,520] stay fixed in source; Youth returns to the same arms-down listening stance.
- Cause / rationale: The shot/cup changes supplied movement, but the non-speaking character had no defined reception, withheld response or turn-taking intention. Camera changes were not a substitute for acting.
- Correction / recipe: Keep the seated mentor anchored while leaning attentively, give the Youth a withheld interruption and prepared reply, and use an open-hand invitation as the speaking handoff. Keep the cup down during that reply window; preserve all actual prop/foot contacts. Review exact new frames and eventually listened normal-speed playback; do not add periodic idle movement.
- Verification: Baseline sampled-frame/source finding verified. Fourteen geometry/contact/intent tests pass for source68ac1fe0059ddae4409a8b2cba25f61c67a05751. Follow-up: final sourcea23acad9aa37cc51fcc96cedec954bd3c8a8a0d3/CI44158619348/artifact14362741826, overview plus12 study samples inspected. New listener states and speaking handoff are visible; normal-speed performance, listening, independent/owner approval remain pending.

### philosopher-pilot-invitation-over-cup — The invitation palm overlapped the steaming cup region

- Recorded (UTC): 2026-11-17T19:27:47+00:00
- Evidence: Intermediate picture394fb7fcf19d9d4c26ff35aea806a2833fa855d4247daae7d75e2f77dbbd1b94; decoded26.6/27/27.8/28.4/28.9 seconds; palm[1190,565] versus cup center[1200,597].
- Cause / rationale: The free-hand target was defined for reach but not its relation to the nearby prop. The palm above the steaming cup could read as warming a hand instead of offering the floor.
- Correction / recipe: Move the invitation up and toward the Youth, clear of cup/steam; keep reach, seated support and cup-hand contact. Require palm/cup separation and inspect the exact new encoded frames.
- Verification: Overlap verified in actual encoded samples and source bounds. Corrected sourcea23acad9aa37cc51fcc96cedec954bd3c8a8a0d3 passes fourteen tests; Follow-up: final picture SHA093ebefb97b3726a0f689ac0f30d6cb78a3fe76fa2d56012282df98b57d63547; final26.8/27.4/28/28.4/28.9 samples show the palm away from cup/steam. Continuous timing and semantic comprehension remain pending.
