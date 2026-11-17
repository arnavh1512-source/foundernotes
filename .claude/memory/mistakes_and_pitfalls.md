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
