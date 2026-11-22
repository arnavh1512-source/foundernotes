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

### philosopher-pilot-palette-only-readings — Different readings were represented mainly by different background colors

- Recorded (UTC): 2026-11-17T19:49:51+00:00
- Evidence: Baseline picture093ebefb97b3726a0f689ac0f30d6cb78a3fe76fa2d56012282df98b57d63547; decoded46.5/49.5/51/54.5 seconds plus the shared hill drawing source.
- Cause / rationale: The panels retained the same hill and bird but used palette changes and a house outline to stand for interpretation, without a character action showing what the reading changed.
- Correction / recipe: Keep geometry, event and palette identical and show two original stick-character reactions to the same passing bird: protective crouch versus curious attention. Preserve the external event, supports and established character identities. Inspect actual changed frames and eventually comprehension in full playback; do not claim a universal psychology finding.
- Verification: Baseline frame/source gap verified. Fifteen geometry/contact tests and browser-script parse pass for source0ca144a8786ecfd6060d7882de9c0383020bb156. Follow-up: CI44162153584/artifact14364186513, pictureed04aeffe71bb733822c8d58518506b5fb78c96f47c12d2c97f824e738fe6a6d; eleven reaction samples and six V6 captioned samples inspected. Shared event and distinct crouch/curious responses are visible; continuous comprehension, artistic/audio/independent approval remain open.

### philosopher-pilot-remote-catch — The supposed missed catch stayed far from the falling work

- Recorded (UTC): 2026-11-17T20:03:23+00:00
- Evidence: V6 exact picture ed04aeffe71bb733822c8d58518506b5fb78c96f47c12d2c97f824e738fe6a6d; decoded34.5,35.6,36.5,37.3,37.7,38.1,38.6,39.2 seconds. Source catch target910/650 versus paper centers1230/1260 before spill.
- Cause / rationale: The hand and paper trajectories were authored separately; arm reach passed without establishing a plausible attempted interaction. Earlier records called this a missed catch too confidently.
- Correction / recipe: Stage the arriving work at the front of the desk closer to the Youth, move hips/chest/head into a committed late reach, keep the brace/support and phone grip, and land the failure with a specific forehead-in-hand reaction. Check the exact new picture; sampled poses do not validate continuous timing.
- Verification: Baseline separation verified in actual encoded frames and source. Source99c1284ffe58a69840e2c55b7b8789ef5a1df41f passes16 tests and browser-script parse. Follow-up: CI44165022116/artifact14365956057, picture SHA8e831772525985e9036085c0446b59e09b9e8f5bdf47795907b3ec0aba48ff8b;13 exact task and6 V7 captioned samples inspected. Torso/reach near the page edge and supported forehead-in-hand reaction are visible. Full decode and unchanged decoded audio verified. Continuous performance, listening and independent/owner approval remain pending.

### reference-browser-identity-2026-11-18 — Remote Chrome was incorrectly described as the owner local Chrome

- Recorded (UTC): 2026-11-17T20:09:50+00:00
- Evidence: Available browser inventory exposed a cdp Chrome inside the cloud environment; its docs identify it as remote. Owner corrected the wording after the Newgrounds attempt. Plugin discovery exposed no usable local Chrome connection.
- Cause / rationale: A browser named Chrome and an existing search tab were incorrectly taken to establish ownership/location.
- Correction / recipe: Check the actual provider/environment and local-connection availability before claiming to use the owner computer. Label cloud attempts as remote; do not use a remote failure as evidence about the owner local browser.
- Verification: Wording corrected to owner. Newgrounds limitation applies to the remote session only; local Chrome access remains unavailable and untested.

### philosopher-pilot-repeated-challenge — The challenge lacked distinct escalation between its successive intentions

- Recorded (UTC): 2026-11-17T20:18:02+00:00
- Evidence: V7 picture8e831772525985e9036085c0446b59e09b9e8f5bdf47795907b3ec0aba48ff8b; decoded16.3/22.4/28.8 plus source point envelopes15.2 and20 seconds.
- Cause / rationale: Two point envelopes reused the same leaning pose; the middle claim and final demand had no distinct whole-body state.
- Correction / recipe: Use a hand drawn toward the self and a checked posture for the middle intention, then commit the hip/chest/head and pointed hand forward for the demand. Keep feet, desk brace and subsequent listener beats. Frame the changed intention on the same room axis.
- Verification: Baseline source/selected-frame finding verified. Integrated sourcea94242892d0afa528508bc69d03ed409ca47af51 passes18 tests/browser-script parse. Final source5785e235d3d6f850b3a586a8bcf65c6a407c9e5a, CI44203545216/artifact14381759074, picture SHAc2278f5209780daab6930bc6d4d9c5d82c6b4986017b1081620a0b670d0e3695; exact final challenge, task/rebuttal and ending samples inspected. Integrated pose/gaze/framing changes and regression corrections are visible in sampled frames. V9 captioned review/full decode/probe complete; continuous motion, actual listening and independent/owner approval remain pending.

### philosopher-pilot-understated-rebuttal — The rebuttal returned to the same resting mentor and a small Youth recoil

- Recorded (UTC): 2026-11-17T20:18:02+00:00
- Evidence: V7 picture8e831772525985e9036085c0446b59e09b9e8f5bdf47795907b3ec0aba48ff8b; actual42.7/43.5/44.6/45.8 samples and matching source. Task34.4 sample also keeps pupil level despite the phone below the face.
- Cause / rationale: The camera supplied a two-shot but listener resistance, follow-up reception and prop-directed gaze had no corresponding explicit states.
- Correction / recipe: Isolate the Youth defensive reception, then return to the two-shot for a skeptical check and the mentor open-palm explanation. Keep the seated supports and real cup grip; direct task pupils toward the active prop. Do not treat a receptive pose as agreement or word-accurate synchronization.
- Verification: Baseline source/selected-frame finding verified. Integrated sourcea94242892d0afa528508bc69d03ed409ca47af51 passes18 tests/browser-script parse. Final source5785e235d3d6f850b3a586a8bcf65c6a407c9e5a, CI44203545216/artifact14381759074, picture SHAc2278f5209780daab6930bc6d4d9c5d82c6b4986017b1081620a0b670d0e3695; exact final challenge, task/rebuttal and ending samples inspected. Integrated pose/gaze/framing changes and regression corrections are visible in sampled frames. V9 captioned review/full decode/probe complete; continuous motion, actual listening and independent/owner approval remain pending.

### philosopher-pilot-undifferentiated-ending — The qualified ending repeated a distant walk instead of distinguishing constraint from next approach

- Recorded (UTC): 2026-11-17T20:18:02+00:00
- Evidence: V7 picture8e831772525985e9036085c0446b59e09b9e8f5bdf47795907b3ec0aba48ff8b; actual56/58/60/62/64.4 decoded samples show the same view, shrinking walker and small persistent question.
- Cause / rationale: One framing state ran across the entire eight-and-a-half-second ending, without emphasizing the still-closed lock separately from the used route.
- Correction / recipe: Reuse the original unchanged world: first isolate the actual closed lock, then re-establish it beside the arch, then move closer to the chosen route and larger practical question. Share world/actor transforms; preserve projected foot contacts and voice speed.
- Verification: Baseline source/selected-frame finding verified. Integrated sourcea94242892d0afa528508bc69d03ed409ca47af51 passes18 tests/browser-script parse. Final source5785e235d3d6f850b3a586a8bcf65c6a407c9e5a, CI44203545216/artifact14381759074, picture SHAc2278f5209780daab6930bc6d4d9c5d82c6b4986017b1081620a0b670d0e3695; exact final challenge, task/rebuttal and ending samples inspected. Integrated pose/gaze/framing changes and regression corrections are visible in sampled frames. V9 captioned review/full decode/probe complete; continuous motion, actual listening and independent/owner approval remain pending.

### philosopher-pilot-close-face-fragment — Youth close-up left a distracting fragment of the mentor face at the frame edge

- Recorded (UTC): 2026-11-17T23:56:39+00:00
- Evidence: Actual V8 picture7ea61b8f6ac64ea3e8dcbd089dc9a82da4035b7bf976ead5bc65a1a2e238ed8e, sourcea94242892d0afa528508bc69d03ed409ca47af51, decoded18.4/19.6; the mentor face arc appears on the right edge.
- Cause / rationale: The camera right bound1270 intersected a face beginning near1260 instead of excluding the entire offscreen character.
- Correction / recipe: Move the close claim center from790 to760 on the unchanged room axis; test the whole mentor head radius plus a margin against the viewport, and inspect exact newly encoded18.4/19.6 samples.
- Verification: Defect verified in encoded V8 samples and matching geometry. Source5785e235d3d6f850b3a586a8bcf65c6a407c9e5a passes19 tests; final encoded samples were rechecked: face fragment absent at18.4/19.6 and explanation elbow clear at44.6/45.4/45.9. This closes the sampled composition defect, not creative or full-motion approval.

### philosopher-pilot-explain-elbow-face — The explaining arm elbow crowded the mentor face

- Recorded (UTC): 2026-11-17T23:56:39+00:00
- Evidence: Actual V8 decoded44.6/45.4/45.9; sourcea94242892d0afa528508bc69d03ed409ca47af51 uses positive free-arm bend after29 seconds, bringing the elbow near the head.
- Cause / rationale: The raised hand was checked for wrist reach and cup clearance, but the elbow branch was not checked against the face.
- Correction / recipe: Use one consistent negative bend for both mentor arms across the dialogue; cup-arm bend remains unchanged and no bend flip occurs during the explanation. Require free elbow/head separation and inspect changed poses and cup-rest regressions.
- Verification: Defect verified in encoded V8 samples and matching geometry. Source5785e235d3d6f850b3a586a8bcf65c6a407c9e5a passes19 tests; final encoded samples were rechecked: face fragment absent at18.4/19.6 and explanation elbow clear at44.6/45.4/45.9. This closes the sampled composition defect, not creative or full-motion approval.

### philosopher-pilot-unsupported-work-release — The arriving work lost visible support before its fall began

- Recorded (UTC): 2026-11-18T00:59:44+00:00
- Evidence: V9 picturec2278f5209780daab6930bc6d4d9c5d82c6b4986017b1081620a0b670d0e3695; decoded36.5/36.9/37.3/37.7/38/38.4 plus source hand withdrawal36.9–37.3 versus first page fall37.4.
- Cause / rationale: Delivery-hand and paper cues were authored independently, leaving a floating interval and an ambiguous relationship to the desk surface.
- Correction / recipe: Tie the palm to the actual bottom of the first page, keep support until release, stage the offer at the desk front and accelerate the fall after support withdraws. Preserve the existing late catch and persistent floor consequence. Inspect exact new release samples, not reach tests alone.
- Verification: Baseline selected-frame/source finding verified. Sourcea5a661a0d21fd72ae0a0e9550e25e33cace9f91e passes21 tests/browser parse. Final sourcea5a661a0d21fd72ae0a0e9550e25e33cace9f91e, CI44212187807/artifact14387096605, picture SHA16b164aaa35a1dfd5a914fc8a84b5fb566e7488d89ad618fe8e140142682302e; ten release and twelve ending samples plus nine captioned V10 samples inspected. Supported release, accelerating fall and planted reconsideration/departure are visible in selected encoded frames. Full decode/probe and unchanged audio hash verified. Continuous timing, actual listening and independent/owner approval remain pending.

### philosopher-pilot-ending-without-reconsideration — The ending showed departure without a visible reconsideration of the unchanged constraint

- Recorded (UTC): 2026-11-18T00:59:44+00:00
- Evidence: V9 exact58.6/59.2/60/60.8/61.6 samples and pilotExitAt source: depth/gait advanced from56 with no pause, gaze target or head-turn state.
- Cause / rationale: The ending camera distinguished lock/context/route, but the character performance remained a generic receding walk through all of them.
- Correction / recipe: Hold both world-space feet while the Youth looks back at the unchanged lock, then turn and begin supported travel along the same path. Retain the measured ending and revise stance checks for the actual new gait intervals. Re-render the complete pilot and inspect turn, departure, foot contact and close-up bounds.
- Verification: Baseline selected-frame/source finding verified. Sourcea5a661a0d21fd72ae0a0e9550e25e33cace9f91e passes21 tests/browser parse. Final sourcea5a661a0d21fd72ae0a0e9550e25e33cace9f91e, CI44212187807/artifact14387096605, picture SHA16b164aaa35a1dfd5a914fc8a84b5fb566e7488d89ad618fe8e140142682302e; ten release and twelve ending samples plus nine captioned V10 samples inspected. Supported release, accelerating fall and planted reconsideration/departure are visible in selected encoded frames. Full decode/probe and unchanged audio hash verified. Continuous timing, actual listening and independent/owner approval remain pending.

### philosopher-pilot-paired-reaction-reset — The shared-event scene erased its acting distinction before the cut

- Recorded (UTC): 2026-11-18T01:52:01+00:00
- Evidence: Actual V10 picture16b164aaa35a1dfd5a914fc8a84b5fb566e7488d89ad618fe8e140142682302e; exact46/48.8/49.3/50/51/52/53/54/55/55.9 samples inspected in review/views-baseline/strip.jpg.
- Cause / rationale: The Youth startle envelope returned completely to zero at53.1 and the mentor follow gesture returned to zero at55, restoring nearly identical opening silhouettes.
- Correction / recipe: Stage a guarded peek, partial rise and retained shielding hand while the mentor follows calmly; preserve the same external event and supports. Inspect the exact final encoded reaction, recovery and ending boundaries; do not use limb checks as comprehension approval.
- Verification: Baseline sampled-frame/source defect verified; source91cf7234fa241e911294ca9e98c045bd8cbe45e1 passes23 tests and bundled script parse. Exact source91cf7234fa241e911294ca9e98c045bd8cbe45e1, CI44218840887/artifact14390176125, picture SHAd3bad8769a5b3badb8daa73a6af452fb36a6504f188226fa4b19d67c5e51197e; six demand/twelve paired-event and nine captioned V11 samples inspected. Updated pose/attention states and retained guarded versus calm final silhouettes are visible in sampled encoded frames.23 source tests, bundled parse and full assembly decode/probe pass; decoded audio unchanged. Continuous timing, listening and independent/owner approval remain pending.

### philosopher-pilot-bird-gaze-target — Paired-event attention used a fixed upward pupil offset instead of the actual moving bird

- Recorded (UTC): 2026-11-18T01:52:02+00:00
- Evidence: V10 views-baseline samples49.3/51/53/55 and original pilotViewActorAt lookUp=notice; template actor draws a fixed upward offset despite shared bird moving left to right.
- Cause / rationale: Character lookUp was authored independently of the event coordinates and panel-to-rig transform.
- Correction / recipe: Convert the shared panel bird position into rig coordinates and use it for gaze, with noticing before the head/body response. Test transformed targets and inspect new encoded face/event samples; keep actual continuous attention and sound pending.
- Verification: Baseline source and selected-frame limitation verified; source91cf7234fa241e911294ca9e98c045bd8cbe45e1 passes23 tests and bundled parse. Exact source91cf7234fa241e911294ca9e98c045bd8cbe45e1, CI44218840887/artifact14390176125, picture SHAd3bad8769a5b3badb8daa73a6af452fb36a6504f188226fa4b19d67c5e51197e; six demand/twelve paired-event and nine captioned V11 samples inspected. Updated pose/attention states and retained guarded versus calm final silhouettes are visible in sampled encoded frames.23 source tests, bundled parse and full assembly decode/probe pass; decoded audio unchanged. Continuous timing, listening and independent/owner approval remain pending.

### review-frames-crop-order — The frame-review crop used FFmpeg positional arguments in the wrong order

- Recorded (UTC): 2026-11-18T01:57:48+00:00
- Evidence: Current V11 Youth/mentor crop sheets showed blank ground or feet while requesting full panels. Expanded real-decode test observed200x100 instead of200x160 for x80/y40/w100/h80.
- Cause / rationale: review_frames.py passed validated x/y/w/h directly to FFmpeg crop, whose positional order is w/h/x/y. Existing integration test checked only file existence and byte size.
- Correction / recipe: Translate the CLI crop to width/height/x/y before scaling. Keep input validation, preserve failed evidence, assert actual decoded crop aspect in the existing test and rerun meaningful own-render crops. Revalidate any older claim based only on a pre-fix crop; full-frame review is unaffected.
- Verification: Regression reproduced before fix; both existing review-frame tests pass after correction. Exact V11 corrected Youth48.98/49.3/52.5/55.9 and mentor48.8/50/52/55.9 crops inspected. This fixes evidence extraction, not artistic approval.

### philosopher-pilot-seated-support — The seated Philosopher used a split standing-like leg pose beside the chair

- Recorded (UTC): 2026-11-18T02:52:25+00:00
- Evidence: Actual V11 picture d3bad8769a5b3badb8daa73a6af452fb36a6504f188226fa4b19d67c5e51197e, sampled14.8/20.9/23.5/27.4/41.3/44.6/45.9 in review/seated-baseline/strip.jpg. Original hip1320/650, feet1240/830 and1400/830; knees1222.67/711.26 and1300.25/763.29.
- Cause / rationale: Leg IK reach and floor contacts were checked, but thigh direction/seat height and a seated silhouette were not. One lower leg extended behind the body and chair.
- Correction / recipe: Reblock the seated pelvis/chest/head and chair together, bring both feet forward on the same floor and preserve original limb and torso proportions. Adjust raised cup path for mouth height without moving its tabletop rest; retain exact handle contact and separate invitation/explanation from cup/steam. Rerender the full pilot and check framing, knees, gaze, cup/face and arm silhouettes.
- Verification: Baseline selected-frame/source finding verified. Source892b7000ec0a9f1782741e83c23301eaa7d189dc passes24 tests and bundled parse. Exact sourcec9898a2833c5f6b3bd5d6d9b3861aa94fd0aa2a4, CI44228817475/artifact14394139231, picture SHA747ce4a268c6f82b42c748f57d35be597dd56f3fdb912bfeb2b7864c81ffcb18;16 study/cup picture/nine captioned samples plus final critical-transition samples, integrated overview and corrected support/prop crops inspected. Chair-supported forward-thigh silhouette, planted feet, revised cup height and palm separation are visible in those samples.27 tests/bundled parse and full decode/probe pass; decoded audio unchanged. Continuous audiovisual, independent and owner approval remain pending.

### philosopher-pilot-seated-knee-fragment — The seated reblock exposed a knee fragment in the Youth close-up

- Recorded (UTC): 2026-11-18T03:04:48+00:00
- Evidence: V12 picture bcd7608b773e01b07b42f71023c1dfa8fff4fe5b8cf31728375a4c57f359b603, source892b7000ec0a9f1782741e83c23301eaa7d189dc, CI44226276203/artifact14392688090, actual18.4/19.6 full-frame samples.
- Cause / rationale: Moving the knees forward crossed the old close-up right/bottom bounds; the earlier face-only exclusion test did not cover the new lower body.
- Correction / recipe: Raise close-up camera center y510 to465 on the unchanged room axis and test the actual projected leg/toe segments against the viewport. Render the full pilot and inspect exact18.4/19.6 plus neighboring cuts.
- Verification: Regression verified in the exact V12 encoded samples. Source b16006bbc4edeca880ad99b4e18fef3318e66320 passes26 tests; exact final render recheck pending.

### philosopher-pilot-free-hand-cup-crossing — The invitation free hand passed through the held cup-handle region

- Recorded (UTC): 2026-11-18T03:04:48+00:00
- Evidence: V12 exact26.45/26.46/26.47 corrected crops inspected; free wrist-to-held-grip distances11.79/10.13/14.44 world pixels. Source892b7000ec0a9f1782741e83c23301eaa7d189dc, picture bcd7608b773e01b07b42f71023c1dfa8fff4fe5b8cf31728375a4c57f359b603.
- Cause / rationale: The lower rest hand and revised target were joined by a straight path. Checking only the final palm/cup gap missed the intermediate apparent second grip.
- Correction / recipe: Use an upward arc for both invitation and explanation, preserving endpoints, fixed bone lengths and the actual held-cup wrist. Check free hand/handle separation and elbow/head clearance throughout both motion intervals, then inspect final encoded transitions.
- Verification: Regression verified in exact V12 crops and geometry; source b16006bbc4edeca880ad99b4e18fef3318e66320 passes26 tests. Exact sourcec9898a2833c5f6b3bd5d6d9b3861aa94fd0aa2a4, CI44228817475/artifact14394139231, picture SHA747ce4a268c6f82b42c748f57d35be597dd56f3fdb912bfeb2b7864c81ffcb18;16 study/cup picture/nine captioned samples plus final critical-transition samples, integrated overview and corrected support/prop crops inspected. Chair-supported forward-thigh silhouette, planted feet, revised cup height and palm separation are visible in those samples.27 tests/bundled parse and full decode/probe pass; decoded audio unchanged. Continuous audiovisual, independent and owner approval remain pending.

### openmontage-cut-heuristic-scope — Automatic scene detection undercounted cuts in our similar-palette stick animation

- Recorded (UTC): 2026-11-18T03:07:14+00:00
- Evidence: Actual OpenMontage VideoAnalyzer standard run on V12 source892b7000ec0a9f1782741e83c23301eaa7d189dc Output artifacts/pilot-intermediate-v12/video_analysis_brief.json reports3 candidate scenes (0–56,56–58.6,58.6–64.5), while authored pilot shots include14.5/29/41/46 and additional room close-ups. Tool commit2e003e65fa99a0f329478a2c1cdcf26bc481933a.
- Cause / rationale: Whole-frame FFmpeg content-change threshold is sensitive to palette/area changes; sparse stick motion and same-room camera cuts may not cross it. This is a detector scope limitation, not proof of absent animation.
- Correction / recipe: Keep the actual source timeline and inspect exact cuts. Treat candidate counts, pacing labels, motion classes and default production-quality fields as unvalidated diagnostics; never add decorative motion or raise a creative score to satisfy them.
- Verification: Observed in real local OpenMontage analysis. Actual extracted reference keyframes inspected separately; continuous audiovisual comparison and creative approval remain pending.

### philosopher-pilot-offscreen-explanation — The explanation began outside the Youth close-up and exposed only a hand at the edge

- Recorded (UTC): 2026-11-18T03:13:27+00:00
- Evidence: Actual V14 sourceb16006bbc4edeca880ad99b4e18fef3318e66320, picture3037745a1321b455a112369e473f377862ffe1058c9249ddae58974bcc1cc70a, OpenMontage FrameSampler44.25/44.26/44.27 samples inspected. The same frames show a small knee fragment at the lower right.
- Cause / rationale: Mentor respond began43.9 while the Youth camera held until44.5. The earlier camera fix covered the challenge close-up but not the later reaction close-up.
- Correction / recipe: Begin respond on the existing44.5 return cut so the gesture is seen in context; raise both Youth close-ups to exclude forward knees. Keep full handle/face clearance throughout the new44.5–45.15 arc and inspect the exact close-up/return boundary.
- Verification: V14 selected-frame/source finding verified. Final sourcec9898a2833c5f6b3bd5d6d9b3861aa94fd0aa2a4 passes27 tests/bundled parse. Exact sourcec9898a2833c5f6b3bd5d6d9b3861aa94fd0aa2a4, CI44228817475/artifact14394139231, picture SHA747ce4a268c6f82b42c748f57d35be597dd56f3fdb912bfeb2b7864c81ffcb18;16 study/cup picture/nine captioned samples plus final critical-transition samples, integrated overview and corrected support/prop crops inspected. Chair-supported forward-thigh silhouette, planted feet, revised cup height and palm separation are visible in those samples.27 tests/bundled parse and full decode/probe pass; decoded audio unchanged. Continuous audiovisual, independent and owner approval remain pending.

### philosopher-stick-pilot — The final arch close-up retained a clipped strip of the spent gate

- Recorded (UTC): 2026-11-22T12:47:39+00:00
- Evidence: Exact V15 picture artifact 14394139231, OpenMontage samples at 62 and 64.4 seconds. The right edge shows cropped bars even after the wide shot established the gate and route. Samples at 56 and 58 show only the lock before the character reappears.
- Cause / rationale: The route crop centered on x540; its right edge extended into the gate world bounds.
- Correction / recipe: Frame the whole arch and exclude the gate edge after the visible lookback. Confirm the lock, full layout and destination read in successive shots and keep visual prompts in a consistent lower band.
- Verification: Exact V16 asset 14755181187. Selected frames around 57.35 and at 63.2/64.4 show an earlier return to the full layout and a complete arch with no gate fragment. Four encoded captioned samples show separate cue and caption bands. Continuous audiovisual and independent review are pending.

### philosopher-stick-pilot — The illustrative work vignette used the same visible set as the surrounding conversation

- Recorded (UTC): 2026-11-22T14:48:01+00:00
- Evidence: Exact V16 frame pairs 869/870 and 1229/1230. The bookcase, window and chair recur across the illustrative cut, while the mentor and cup disappear and reappear.
- Cause / rationale: The vignette called the full study background renderer to share the desk surface.
- Correction / recipe: Share the desk geometry but give the work vignette its own background and palette so the two situations can be distinguished before the label is read. Check both transitions in the exact encoded cut.
- Verification: Exact V17 encoded artifact 14758649327 shows the workroom as distinct at both boundaries. The phone, clock, and dropped papers remain visible. The paired-view cue is absent at entry and present during recovery. Four captioned samples show separated bands. Full-speed interpretation and actual listening remain pending.

### philosopher-stick-pilot — The pen changed apparent length during the interrupted task

- Recorded (UTC): 2026-11-22T15:47:57+00:00
- Evidence: Exact V17 frames 900, 963, 987 and 993
- Cause / rationale: Pen was drawn between independent wrist and paper points
- Correction / recipe: Keep a constant pen length and complete the set-down before the hand reaches the phone
- Verification: V17 defect supported by source and encoded samples. New exact render review pending.
