# FounderNotes — tested positive recipes

This is a **newly initialized** learning file. Do not call a technique a winning recipe unless a concrete video or benchmark demonstrated its value, and an independent review was recorded. See `../skills/podcast-scout-skill/scripts/record_lesson.py`.

## Verified recipes

_No tested recipes recorded yet._

### night-1-part-2 — Natural talk acting: gestures start ~0.15 s before stressed words found in the real voice, hold, then relax to rest; listeners mostly still.

- Recorded (UTC): 2026-11-23T04:59:20+00:00
- Evidence: Frame sequences 0.3 s apart at 209-213 s and 785-791 s showed hold/change/rest pattern.
- Cause / rationale: Owner rejected looping gestures ('same gestures', then 'forced').
- Correction / recipe: tools/emph.py (RMS peaks with min spacing per character) + planFor/gestureAt in stick.html; spring in, slow relax, single damped beats instead of continuous shaking.
- Verification: Rendered 2026-11-22, QC 3.90% fast motion; awaiting owner viewing feedback.

### night-1-part-2 — Faces on the stick cast: 10 expressions, voice-driven mouths, blinking; philosopher mouth dark #2a1f3d so it shows on his white beard.

- Recorded (UTC): 2026-11-23T04:59:21+00:00
- Evidence: face-expressions-test.png reviewed by owner 2026-11-23; owner approved adding faces.
- Cause / rationale: Faceless figures could not show emotion; owner flagged the philosopher's smile as invisible in purple.
- Correction / recipe: engine/faces.js + LEXPR per line (speaker and listener) + SCENE_EXPR for narrator moments + ENV mouth envelope.
- Verification: Frame check of 16 times showed correct expressions; full render in progress.

### half-landing-a03-reel — Seamless Reel loop: end on the first frame and hide the reset inside the story

- Recorded (UTC): 2026-11-27T15:41:01+00:00
- Evidence: A03 Reel: last frame vs first frame 0.00% of pixels differ; A04/A06/A08 0.43-0.46%
- Cause / rationale: a loop shows a jump when the end state differs from the start (e.g. a fresh stain that wasn't there at frame 0)
- Correction / recipe: design the last shot to land on frame 0's exact pose and props; give the wardrobe an old stain where the new one appears (asset v2: it happens every sound check), so the fresh mark fades into it
- Verification: measured by ep_review.seam on all four Reels

### bench-bump — Detailed close-up faces: build forms first (ridge, socket, lids, bridge), then shade in tone planes from the outline inward

- Recorded (UTC): 2026-11-28T05:09:53+00:00
- Evidence: reference-ig-01 full-size frames; compare-v3.jpg
- Cause / rationale: the reference reads as detailed because of anatomy and planes, not line detail
- Correction / recipe: outline from a spline; bands offset from the profile: rim highlight, lit front, mid, terminator shadow, side plane; specular streaks on the domes; ledge light and under-shadow on ridges; domes shaded with round shapes, never horizontal strips. Next step: crisper plane edges (the reference uses hard cel edges, ours are soft)
- Verification: v3 frames vs reference at 0.1, 1.3, 22.7 s

### half-landing-a04-rewind,bench-bump — Payoff first, then rewind, slow replay and fast-forward, told by a playback chip, a ticking clock and two-part typed labels

- Recorded (UTC): 2026-11-28T05:09:53+00:00
- Evidence: reference-ig-01 study; built into engine/overlay.js and the shot 'time' remap; A04 rewind sync 9/9, loop seam 2.57%
- Cause / rationale: the result first makes the viewer ask how; the playback device tells time without words
- Correction / recipe: use shot time remaps (from/to or keys speed ramps), ui chips, labels (noun white, verb yellow, at most 4 words), impact frames (hits), light grade, counters
- Verification: A04 rewind and bench-bump renders pass QC; frames checked

### bench-bump — Measure the reference's camera and impact timing, then copy the timing (not the art): punch-in on the hit, alternating slow push/pull every 1.5-2.5 s, accelerate into a transition and decelerate out, 3-frame contact hold with smear before it

- Recorded (UTC): 2026-11-28T05:32:23+00:00
- Evidence: ref_motion.py on reference-ig-01 vs bench-bump v3/v4; frame-by-frame crops 0.2-0.8 s of both
- Cause / rationale: v3 had long camera rests and a frozen 16-frame ending; the impact had no smear, contact hold or punch-in
- Correction / recipe: run ref_motion.py on the reference and on ours; match the camera move list and the impact anatomy; no hold of 3+ frames unless it is a deliberate beat
- Verification: v4: holds of 3+ frames 4 -> 0, still steps 7.7% -> 5.0%, zoom/roll moves 9 -> 10 (ref 12); hit frames 0.0-0.6 s match the reference sequence. Local motion still 2.8% vs 7.6% (open)

### bench-bump — High-level 'life': every element moves on its own each frame (cells drift and tumble, fat-cell outlines shimmer, marrow jiggles, blood flows inside vessels), not just a few

- Recorded (UTC): 2026-11-28T07:40:57+00:00
- Evidence: difference maps (frame t vs t+2) of reference-ig-01 and bench-bump at 6.0 s and 14.5 s: the reference lights up across every layer, ours only in parts; ref_motion local motion per 2 s segment: ref 6.5-13% vs ours 1.4-2.7% in 4-20 s
- Cause / rationale: only the pool cells moved; bone, fat and vessels were static drawings
- Correction / recipe: give every repeated element its own phase-shifted motion (position, rotation, outline wobble) and flow inside tubes; check with a difference map before rendering
- Verification: local motion 2.8% (v4) -> 3.7% (v5); reference 7.6%, gap still open

### bench-bump,half-landing-a04-rewind — Boil and transfer: re-pick small offsets every 2 frames so repeated elements jump like hand-drawn ones; carry the impact grammar (punch-in on the hit, smear trail, camera kick on landing) into the series

- Recorded (UTC): 2026-11-28T07:58:21+00:00
- Evidence: ref_motion local motion: bench-bump 3.7% -> 4.6% with boil (ref 7.6%); A04 rewind 5.9%, no holds of 3+ frames, sync 9/9; launch frames show the smear trail
- Cause / rationale: smooth sine motion reads as floating; the series had no punch-in or smear on its key beats
- Correction / recipe: boil = offset from rnd(id, floor(NOW*15)); on every gag hit: camera punch ~1.1x easing out then relax, smear ghosts on the fastest frames, a small camera kick on landing that settles back to the loop framing
- Verification: measured as above; A04 rewind exported and passes ep_check; owner phone review pending

### bench-stick — Stick strike grammar from reference-ig-03: coil -> spring (3 frames) -> wind-up -> one arc-smear frame -> extended contact pose held 3 frames -> hit body folds at the waist and holds 3 frames -> 2-frame blur launch -> land in a crouch with dust

- Recorded (UTC): 2026-11-28T08:07:28+00:00
- Evidence: reference-ig-03 9.6-10.4 s frame by frame at full crop; rebuilt in bench-stick (review/exchange-compare.mp4)
- Cause / rationale: a strike reads through holds at the extremes and clean silhouettes, not through many in-betweens
- Correction / recipe: author strikes as pose keys with holds at the extremes (track() keys in bench-stick/_common.js), knees bent in every fight pose, one smear frame, a reaction that folds around the impact point
- Verification: take 2 frames match the beat order and hold lengths of the reference exchange

### bench-stick — Stick flight and landing: arched C off the hit, tucked pose with hang time at the apex (pose nearly frozen for ~4 frames while it drifts), flat landing with an impact burst, a small bounce, and a dust column that rises and fades over ~15 frames; secondary motion: head snaps back on contact and settles, arms trail the body by 1-2 frames

- Recorded (UTC): 2026-11-28T08:14:26+00:00
- Evidence: reference-ig-03 11.85-12.55 s frame by frame (full crop); bench-stick take 3 frames 1.05-2.15 s; review/flight-compare.mp4
- Cause / rationale: take 2 flew in a stiff upright pose and landed straight into a crouch with no impact; a follow camera weighted at 0.55 pushed the other fighter off the frame edge
- Correction / recipe: author flight as keys with 'air' height: arch -> tuck (two near-identical keys for hang time) -> flat with 'inn' ease into the floor -> bounce key -> rest; add head snap and arm lag as offsets; camera follows the midpoint at ~0.3 weight with a lag and pulls back while a body is airborne
- Verification: take 3: hang time visible frames 9-16, impact burst + bounce + dust column, both fighters stay in frame; QC PASS

### bench-stick — Stick clinch and throw: the attacking arm is aimed at the opponent's neck every frame (two-bone aim), momentum shoves both bodies back together, the lift goes clearly above and forward of the thrower so the silhouettes separate, slam in front with burst, bounce and dust

- Recorded (UTC): 2026-11-28T08:24:43+00:00
- Evidence: reference-ig-03 12.6-12.9 s; bench-stick X02 (review/run-clinch-compare.mp4)
- Cause / rationale: the first heave overlapped the lifted body with the thrower's head and the silhouettes tangled
- Correction / recipe: aimFront() in bench-stick/_common.js for contacts; keep lifted bodies 200+ px above or clear of the other figure; slam where the floor is empty
- Verification: take 6: clinch contact reads, the lifted body is separate above the thrower, slam with dust; QC PASS

### half-landing-a09-reel — First episode built from director's sheets with the stick lessons on Dev: visible cause (eyes closed while the cup creeps), eyes pop -> crouch -> lunge with a smear frame -> low catch held -> punch-in -> a drop that becomes a new stain; a falling prop must travel through clear space, never across the character's body

- Recorded (UTC): 2026-11-28T08:35:04+00:00
- Evidence: A09 frames 3.1-3.9 s at 30 fps (three takes); ep_review: sync 7/7, loop seam 0.14%; QC PASS
- Cause / rationale: take 1 the lunge pushed Dev's head into the counter; take 2 the falling cup crossed his chest and read as already held; take 3 the step back pushed him out of frame
- Correction / recipe: before a catch or reach, place the character so the prop's path is clear of the body silhouette, keep heads clear of set pieces at full lean, then reframe the camera for both
- Verification: take 4: the cup falls through clear space, Dev lunges into it, both in frame; exported and ep_check PASS

### half-landing-a12-reel — Second episode from director's sheets: the world reacts in small comic beats (a foam blob lands on his head and stays, a stain moves by itself) before the payoff; payoff = tremble -> impact frame -> 3-frame snap -> hold -> chime; sparse foley needs a rhythm bed (scrub strokes, drips) to reach -14 LUFS

- Recorded (UTC): 2026-11-28T08:52:17+00:00
- Evidence: A12 precheck and render frames; QC fail at -16.2 LUFS before the scrub/drip cues, PASS after; sync 24/26
- Cause / rationale: the first precheck hid the scrubbing arm behind foam, put the smiley on the pocket and left his raised arm holding nothing
- Correction / recipe: check every shot against its sheet's eye target before rendering; give action sounds their full rhythm
- Verification: A12 exported, ep_check PASS, QC PASS

### half-landing-a07-reel — Clusters of small impacts (six glasses landing) need short ticks (cue dur ~0.06 s) spaced >= 0.1 s, in picture and sound; ringing clinks 75 ms apart merge into one sound

- Recorded (UTC): 2026-11-28T09:06:46+00:00
- Evidence: A07 sync 11/20 -> 14/20 after re-spacing to 0.1 s and cutting thump tails -> 20/20 after cutting each clink to 0.06 s
- Cause / rationale: each snap rang into the next and the onsets merged
- Correction / recipe: space rapid impacts >= 0.1 s apart and cut each to a short tick; cut thump tails before clinks
- Verification: A07 ep_review 20/20 within 50 ms

### half-landing-a10-reel — Action timed to music: drive every contact from one beat list (knife lift = ease-in down into the beat, 2-frame contact hold, ease-out up), escalate tempo to a smear on ones, then a silence before the payoff; sounds that happen together share one timestamp

- Recorded (UTC): 2026-11-28T09:15:36+00:00
- Evidence: A10 sync 36/46 with chop cues 20 ms after the kicks and long kick tails at 0.25 s spacing -> 45/46 with chops on the kick timestamp and shorter kicks; frames show contact holds and the smear
- Cause / rationale: two sounds 20 ms apart merge into one onset (to the detector and to the ear); kick tails rang into the next beat
- Correction / recipe: one beat list per shot feeds both picture (lift()) and cues; same-moment sounds share t; kick dur <= beat interval minus ~0.1 s
- Verification: A10 ep_review 45/46 (the miss is a soft bowl plop under the groove); QC PASS; exported

### reference-ig-03,half-landing-a09-reel — Mark the peak by changing the world: for the hero moment the scene grade turns cool teal and desaturated, other figures drop to silhouettes, and the hero leaves coloured afterimages (pink/cyan/violet), then everything snaps back on the next beat

- Recorded (UTC): 2026-11-28T09:18:00+00:00
- Evidence: reference-ig-03 44.2-47.2 s at 5 fps (teal grade, black silhouettes, chromatic ghost trails, shockwave arcs, snap back at 47.2 s); A09 E04 frames 3.3-3.7 s with the new tools
- Cause / rationale: our payoffs used only camera punches and impact frames; nothing told the viewer 'this is the special moment' at a glance
- Correction / recipe: shot key "special": [t0, t1] in workspace.json grades the stretch; afterimages(draw, n, step) in overlay.js tints earlier poses of black line art with a CSS filter (invert, sepia, saturate, hue-rotate); keep it short (0.2-0.5 s) and snap back
- Verification: A09 re-rendered E04 only (cache), QC PASS, ep_check PASS; frames show grade, ghosts and snap back

### half-landing-a13-reel — A chase reads only when pursuer and pursued share the frame: keep the gap small (about a body length), have the camera follow the runner and widen while he runs, and remember cam() scales zoom by 1.18 (visible width = 1080/(z*1.18)); an empty-frame beat before an entrance from the other side sells a loop-around

- Recorded (UTC): 2026-11-28T09:33:33+00:00
- Evidence: A13 O04 takes 1-3: the onion trailed 250 px behind and Dev's head clipped the right edge; take 4 with the gap at the heels, pan to 1150 and a 14% widening reads
- Cause / rationale: positions were planned in world units without the camera's real visible width; a lean of 0.7 puts the head ~166 px ahead of the hips
- Correction / recipe: compute the frame's world bounds from cam() before staging a chase; budget the head lead for running leans
- Verification: A13 exported; frames 4.2-5.1 s show both in frame and the stop at his feet

### half-landing-a03-reel,half-landing-a04-reel,half-landing-a06-reel,half-landing-a08-reel — Retrofit lessons into finished episodes cheaply: one shared-helper change (the breath in dev()) re-renders every shot once; an overlay key (hits) on one shot re-renders only that shot

- Recorded (UTC): 2026-11-28T09:47:54+00:00
- Evidence: still frames A03 21.2% -> 6.2%, A04 29.9% -> 6.8%, A08 15.2% -> 6.3% after the breath; impact frames on each key hit re-rendered 1 shot per Reel; all QC PASS, loops ok, ep_check PASS
- Cause / rationale: the first batch was made before the breath and impact lessons
- Correction / recipe: when a lesson lands, list the finished episodes it improves, apply it through _common.js or an overlay key, re-measure with ep_review and re-export
- Verification: four Reels re-exported 2026-11-28

### half-landing-a13-reel — An empty frame is not a dead frame: when a character leaves, the world remembers him (his dust hangs and settles); particles need on-twos boil and enough contrast to read as motion

- Recorded (UTC): 2026-11-28T12:37:45+00:00
- Evidence: A13 still 18.3% (empty-kitchen beat 44%, after-exit 33%) -> 17.9% with slow faint motes -> 4.9% with boiled, darker motes
- Cause / rationale: the deliberate pause had nothing moving; smooth, faint drift is below what reads frame to frame
- Correction / recipe: keep deliberate pauses but leave a trace of the last action moving through them (dust, steam, a swinging door); give particles a 2-frame boil
- Verification: A13 re-exported; still 4.9%, sync 18/18, QC PASS
