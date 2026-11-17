# Encoded review: reveal the route after reassessment
Date: 2026-11-17. Internal craft revision; not creatively approved.

## Baseline actually inspected
Retrieved CI artifact 14339657212 and verified its encoded SHA-256 f03004bb20de71496a636b88b9e9dcbf647a56b0cfc2426de986443d72232fd0. FFprobe reports 1920×1080, 30 fps, 435 frames and 14.5 seconds, with no audio stream. Inspected its supplied 24-frame contact sheet and decoded additional frames at 0, 1.2, 3.5, 5.8, 6.2, 6.5, 6.7, 7.2, 9.4 and 14.4 seconds. This is encoded-frame inspection, not continuous video viewing or listening.

At 0 seconds the open arch and connected steps are already plainly visible beside the locked gate. The composition remains wide through the character's reassessment. The intended discovery therefore does not introduce new visual information to the viewer. This is a staging finding; audience comprehension was not tested.

## Reference consultation in this run
Agent-Reach status returned NOT_INSTALLED and authorized native fallback. The creator's original Alan Becker upload at https://www.newgrounds.com/portal/view/316541 displayed Site Unavailable / Unable to access this site in the current cloud browser. No verification challenge was solved, access restriction bypassed, or fresh Alan playback claimed. Earlier Alan observations remain documented in ALAN_BECKER_STUDY.md and STICK_TIMING_REVIEW_2026-11-17.md.

Recovered the owner's supplied Psychology-of-Discipline-SnapYT.App.mp4, SHA-256 bdd6c9d1a08fbb9362d00a254732c06d84a31fdb2be7d65d71e53fdbadc20012. Its total duration is 884.169433 seconds; only the opening 0–48-second region was sampled at one frame per two seconds. The displayed frames move between clock details, character reactions, room views and later tasks/settings. That supports testing framing changes around the object/action a viewer needs to understand. It does not establish precise cuts, sound quality or retention. The original channel identity was not independently verified from this file, so no specific channel attribution is asserted. Day One Films, PsychToonsHQ, PsychDoodleTV and gly2wBcnZUQ remain pending for fresh direct comparison. No reference media or assets are committed or reused.

## Correction
Keep the framing on the character and locked gate during the attempt. Start the continuous wider reveal at 6.2 seconds, after the existing 6.0–6.2-second head turn, and finish at 7.2 seconds. Then retain the established wide composition for the stair traversal and arrival. The world, obstacle, poses, timing, contacts and original artwork are unchanged.

Implementation reuses layerMatrix from story-motion.mjs through a deterministic cameraAt helper. The added test verifies that the arch is outside the opening frame, remains hidden through reassessment, becomes visible afterward, and the complete character stays within the frame over 436 samples. This camera change is not counted as better character acting or as a way to raise a motion score.

## Render and actual re-review
Local Node tests: all eight pass. The standard renderer is installed in this Linux environment but could not launch Chromium: process socket creation returned Operation not permitted. No restriction-weakening launch workaround was attempted. Used the existing GitHub renderer instead.

Code commit de307c2e11a3d8e4a6dd33cb65cbb9379f5fa37d; Actions run 44120771407; all three jobs passed. Retrieved artifact 14344897475. The exact new MP4 SHA-256 is 1b9db90aa9eee238fa013738e9f4ca13f872e311e7bb7121fbd486d0fbaf0bc3. FFprobe verifies 1920×1080, 30 fps, 435 frames and 14.5 seconds, with no audio stream. Full FFmpeg decoding completed successfully.

Inspected newly decoded frames at 0, 1.2, 3.5, 5.8, 6.2, 6.5, 6.7, 7.2, 9.4 and 14.4 seconds. The arch is absent at 0 and 6.2, begins entering at 6.5, is recognizable at 6.7, and is fully staged at 7.2 before the climb. The gate remains locked. Inspected all 36 decoded transition frames 183–218 (6.1–7.2667 seconds) in a contact sheet: no blank frame, double exposure or clipped character was observed there. Tests additionally protect the complete pose bounds throughout the source timeline. Full-resolution individual transition frames and actual continuous playback are still separate review work; this sheet is not claimed as an independent review.

## Remaining and next work
The silent craft study is still not the narrated pilot. Voice/sound, continuous temporal review, broader benchmark coverage and independent/owner review remain pending. The opening gate top is intentionally cropped; this exercise has no captions and must be recomposed for the pilot's subtitle safe area. Do not add another isolated camera demo unless a concrete defect requires it. Resume PHILOSOPHER_PILOT_READINESS_2026-11-17.md: recover approved dialogue/timings and complete viewer-first preparation before adapting a pilot script. Do not substitute a narrator or approve factual claims from the shooting script without verification.
