# FounderNotes — verified mistakes and pitfalls

Add only observed defects with an episode, timecode or file, supported cause, correction and verification evidence. Historical observations below retain their source and limitations; an open remedy is not a verified success. Read this file before planning and before reviewing each cut. See `../skills/podcast-scout-skill/scripts/record_lesson.py` and `../../docs/REFERENCE_REVIEW.md`.

## Verified lessons

The initial entries preserve documented observations from the 2026-11-11 study and actual access failures on 2026-11-17. They do not establish a fresh review of the current Philosopher video.


### choking-under-pressure — Opening rushed to research before establishing the viewer's situation

- Recorded (UTC): 2026-11-17T13:05:00+00:00
- Evidence: .claude/skills/podcast-scout-skill/references/reference-video-learnings.md, 2026-11-11: How our first pilot differed (experiment at 0:09 after one viewer sentence)
- Cause / rationale: Historical notes document the sequence; the underlying authoring cause was not established.
- Correction / recipe: In the next opening, establish a recognizable situation and deliver a useful insight before adding research detail. Review the actual opening against a relevant reference; do not impose a fixed 40-60-second delay when clarity benefits from earlier evidence.
- Verification: Historical documented observation, not a fresh viewing. Fix remains open; no new pilot or audience outcome verified.

### choking-under-pressure — Motion metric was raised by punch-ins without establishing better character animation

- Recorded (UTC): 2026-11-17T13:05:01+00:00
- Evidence: .claude/skills/podcast-scout-skill/references/reference-video-learnings.md, 2026-11-11: initial 2.4% fast-motion frames; punch-ins raised the measurement to 3.55%
- Cause / rationale: The historical note explicitly attributes the increased metric to added punch-in cuts; actual acting improvement was not established.
- Correction / recipe: Keep technical motion checks, and separately watch for meaningful character/object state changes, stable hand-prop contact and readable reactions. A camera crop or zoom alone cannot close an acting finding.
- Verification: Historical measurements carried forward with provenance. Improved acting and motion continuity remain unverified.

### reference-review-2026-11-17 — Promised comparison could not be completed because media access failed

- Recorded (UTC): 2026-11-17T13:05:01+00:00
- Evidence: docs/REFERENCE_REVIEW.md, Current session limitations; gateway status NOT_INSTALLED and official uv tool install DNS failure on 2026-11-17
- Cause / rationale: Local media transfer failed; Agent-Reach was absent and its official release host could not be resolved. Browser playback also hit verification and the analysis service lacked credits.
- Correction / recipe: Run the gateway status at session start, preserve actual retrieval results, and mark unavailable reference footage pending. Complete useful production documentation, report the blocker plainly, and obtain accessible footage before assigning motion/voice passes.
- Verification: Blockers observed in this session. No fresh comparison, animation improvement or successful Agent-Reach installation is claimed.

### philosopher-motion-study-cut-1a — Scaled drawing strokes failed before encoding

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Pillow ImageDraw.line expects integer widths; scaled character limbs produced float widths.
- Correction / recipe: Round widths in the shared line helper. Run the all-shot deterministic rendering test before encoding.
- Verification: Two local tests passed and the revised 24-second MP4 encoded successfully. This verifies rendering, not artistic quality.

### philosopher-motion-study-cut-1a — Pointing hand was hidden by the table

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Characters were drawn before the tabletop, which then occluded the hand.
- Correction / recipe: Composite the pointing forearm and hand above the tabletop. Check occlusion in all prop interactions before final render.
- Verification: Revised stills at 5.8 and 7.7 seconds show the hand visible. Complete motion and anatomy remain pending.

### philosopher-motion-study-cut-1a — Map finger shortcut and premature route reveal

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Finger position used one straight interpolation while the map route had two segments; ink was drawn by whole segment.
- Correction / recipe: Use matching segmented positions and progressive ink reveal. Preserve a regression check that later ink is absent early.
- Verification: Revised map samples and the ink-reveal regression passed; full temporal review is pending.

### philosopher-motion-study-cut-1a — Stair traversal lacked planted foot positions

- Recorded (UTC): 2026-11-17T13:22:17+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; first-cut hash 9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307; revised hash 21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394
- Cause / rationale: Root moved along a diagonal while legs used a generic horizontal walking stride.
- Correction / recipe: Compute alternate planted and lifted feet from the actual stair coordinates. Check foot contact, weight transfer and sliding in playback.
- Verification: Revised samples at 15.8 and 18.3 seconds show tread contacts; complete walking cycle and weight transfer remain pending.

### philosopher-motion-study-cut-3 — Foreground arm replacement duplicated the base arm

- Recorded (UTC): 2026-11-17T13:28:56+00:00
- Evidence: docs/PHILOSOPHER_MOTION_REVIEW_2026-11-17.md; Cut 3 study stills and Cut 3a at 7.7 seconds; revised SHA-256 e6b174358ac802132ad7523d1bbfb77d6dadbc86d6d8cf487b49f0de48fccabf
- Cause / rationale: The character drew its original right arm before the table; a separately composited foreground arm was added without suppressing the original.
- Correction / recipe: Suppress the original arm when a foreground replacement is drawn. Inspect complete limb silhouettes and count hands in all replacement poses; preserve two-link length checks.
- Verification: Cut 3a frame at 7.7 seconds inspected after rerender; duplicate absent there. Full playback, independent critique and reference comparison remain pending.
