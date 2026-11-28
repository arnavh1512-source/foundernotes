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

### reference-ig-04 — A series template: the same creator repeats the exact beat grammar and length (26.1 s) with a new subject each time, so viewers learn the format once; make the invisible visible on the surface before going inside; keep atmosphere (floating motes) in every frame

- Recorded (UTC): 2026-11-28T12:59:16+00:00
- Evidence: reference-ig-04 vs reference-ig-01: identical length and beat order (hit, surface reveal, roll in, rewind, slow press, fast clock with labels, roll out, scan band, loop); ref_motion: local motion 6.2% vs 7.6%, rolls at 2.5/13.6/21.3 s
- Cause / rationale: a fixed format lets a channel publish consistently and lets viewers enjoy the variation instead of relearning the structure
- Correction / recipe: Half Landing keeps its own template (written in the playbook): hook in frame one, three thumps, visible cause, multi-tool key moment, look to camera, +1 apron stain, seamless loop; vary prop, gag and set only
- Verification: template written into the playbook; existing episodes A03-A13 already follow it

### reference-ig-05 — Dialogue comedy grammar: establishing two-shot -> over-the-shoulder shot/reverse shot, one line per ~2.5 s shot -> in-scene chorus that voices the joke -> close-up punchline + short reaction shot -> running verbal tic -> words contradicting action -> escalating callback ending

- Recorded (UTC): 2026-11-28T13:31:25+00:00
- Evidence: reference-ig-05: 29 shots, mean 2.5 s (1.4-4.4 s), shot-by-shot midframes reviewed at 240 px plus rea-video breakdown
- Cause / rationale: each cut answers who speaks and who reacts; the chorus and the reaction shots tell the viewer where the laugh is
- Correction / recipe: for any dialogue scene (Think! or a future talking episode) plan shots by line: establish once, then OTS pairs, a close-up for each punchline, a reaction after it; give the straight character a repeated verbal tic; end on a callback that tops the earlier beats
- Verification: study only; to be tested in a drill

### bench-zap — Effect frames: copy the timing exactly, then match the effect's mass, not just its shape

- Recorded (UTC): 2026-11-28T14:14:11+00:00
- Evidence: studio-output/bench-zap/review/compare.jpg, compare2.jpg, compare3.jpg vs reference-ig-04 at 0.5 s and 0.9 s (full-size ref_compare)
- Cause / rationale: v1 copied the idea (bat hits elbow, zap runs to the fingers) but every element was undersized: spike-fan hand, thin bat, small burst, two thin strands. Timing was right; mass was wrong.
- Correction / recipe: Impact on one frame with a smear the frame before; burst of flat blocks for 2 frames; one-frame travel; redraw the zap every frame (4 strands, mixed widths 8-16 px, spikes, branches at the fingers); label 0.7 s after the hit. Then judge mass: the effect should cover about a third of the frame, the subject should fill the frame, and the room needs props plus motes.
- Verification: v3 render QC PASS; compare3 shows matched timing, block burst and denser zap. Still open (not verified): zap clustering at elbow and hand, larger arm in frame, bigger burst blocks, richer room.

### learn/environment-richness-01 — Lived-in room recipe, the impact camera recoil, and breath on the character, never the frame

- Recorded (UTC): 2026-11-28T14:31:08+00:00
- Evidence: studio-output/learn/environment-richness-01: compare_a1/a2 vs reference-ig-04 0.2 s; review/ref_motion vs take2/take3 motion.json
- Cause / rationale: Our earlier rooms were a flat wall + floor band; the camera pushed before the hit and the whole frame bobbed with the breath, which ref_motion read as 7 camera moves vs the ref's 3. The zap drill's 12-move target came from a two-shot window, so it pushed us to over-move the camera.
- Correction / recipe: Room: depth layers (ceiling moulding, wall, panelled dado with top rail, floorboards), a ring of props around the subject (picture, window with a view and lit houses, curtain, dresser + plant, dark armchair, rug with border and fringe), the subject casts a shadow on the wall, the room stays dark and muted so the subject is the brightest form, and the story prop (the bat) waits on the set before it is used. Camera: locked before the hit; on contact one 0.33 s recoil = zoom out ~4% + ~175 px pan + ~1.5 deg roll with a short shake, then hold. Breath moves the character only.
- Verification: Attempt 3 recoil measured: zoom 0.95 / pan 145 px / roll -1.6 deg at 0.467 s vs ref 0.96 / 175 px / -1.4 deg at 0.433 s. Critic passed all 3 room criteria. Still open: local motion 5.3% vs 9.0% once the fake frame bob was removed (the ref's motion lives in the effect), and one false camera move at 1.2-1.6 s caused by the label box and zap (measurement limit). Escalated after 3 attempts.

### learn/dialogue-grammar-01 — Dialogue grammar in a 9:16 frame: tight two-shot, dark corner shoulder, eyes on the upper third, callback subject centred

- Recorded (UTC): 2026-11-28T14:52:51+00:00
- Evidence: studio-output/learn/dialogue-grammar-01: ours_sheet.jpg (attempt 1) vs ours_sheet2.jpg and review/a3.jpg (attempt 3); ref ig-05 0-17 s cuts at 4.4/8.4/14.7 s vs ours every 1.6-3.6 s
- Cause / rationale: Attempt 1 used landscape habits in a vertical frame: characters 12% of frame height, a bright foreground shoulder over 30% of the frame, close-up heads at the bottom, and the waiter who carries the callback outside the frame.
- Correction / recipe: Two-shot: seat the pair close (a narrow table) and push in so both heads sit in the top half; subtitles live in the lower half. OTS: the near shoulder is dark (brightness ~.45), soft and tucked into a lower corner. Close-up: camera centre y = head y + visible height / 6. Callback/topper: bring the paying-off character to the centre of a group shot. Keep background people moving in every shot (passers in the window, a dancing waiter). The ref opens slowly (shots 4.4 and 4.0 s) and cuts faster as the joke builds; don't start at full cutting speed. Engine: shots now take a subs key for burned subtitles.
- Verification: Critic passed all 4 grammar criteria on attempt 3. Still open: in-picture motion 1.6% vs ref 4.2% (flat stick dialogue needs constant listener reactions and gesture), opening shots too short vs the ref; escalated after 3 attempts.

### learn/logline-01 — A logline is about the character's want and irony, not the setting; every episode line needs its own want and obstacle

- Recorded (UTC): 2026-11-28T14:55:23+00:00
- Evidence: studio-output/learn/logline-01 draft1-3 with verdicts1-3
- Cause / rationale: Draft 1 described a setting ('a noisy kitchen'): no want, a vague obstacle ('chaos'), episode ideas that were situations without stakes. Draft 2 had all parts but ran 48 words, and one episode was an event plus a reveal with no want.
- Correction / recipe: Shape: [flawed character] wants [concrete thing], but [specific obstacle], and [ironic turn]. Keep it under 30 words. The engine is the part that changes per episode (a new sound + a new dish) plus a fixed arc (wrecked -> fight -> rhythm). Test each episode line separately for want + obstacle + turn.
- Verification: Draft 3 passed all three checks (self-review by the same agent, not an independent critic). Series line: 'A perfectionist cook wants one flawless service, but the concert hall next door keeps wrecking his dishes, and fighting the noise turns him into part of the band.'

### learn/kishotenketsu-01 — Kishotenketsu: the turn must look unrelated on the surface, and the reconcile needs a plant

- Recorded (UTC): 2026-11-28T15:00:04+00:00
- Evidence: studio-output/learn/kishotenketsu-01 draft1-2, verdicts1-2
- Cause / rationale: Draft 1's turn mirrored the development beat for beat (same tilt, same nod), so the link was obvious at once, and the ending depended on a crack in the wall never shown before.
- Correction / recipe: Beat 3 shows a different action in a different place (a light sweeping an empty hall), with the connection hidden. Plant the linking object in beat 1, inside an action with another purpose (Dev wipes around a seam). Save any echoed gesture (the shared nod) for the last beat as the button.
- Verification: Draft 2 passed all three checks (self-review).

### learn/setup-payoff-01 — Setup/payoff: the real fix must be planted, the obvious plant can pay off as the failed attempt, one plant per action

- Recorded (UTC): 2026-11-28T15:00:05+00:00
- Evidence: studio-output/learn/setup-payoff-01 draft1-2, verdicts1-2
- Cause / rationale: Draft 1 planted a tea light and a lighter together in one beat (the eye flags them) and then saved the soup with nothing planted (a cheat).
- Correction / recipe: Plant the real solution first, disguised as an annoyance (a pyro blast through the hatch that he shuts out). Let the obvious props pay off as the fix that fails (misdirection). Spread plants across beats, each inside an action with another purpose (reaching for salt, a favour for a roadie). Small echoes (singed eyebrows -> smoking eyebrows) add a button.
- Verification: Draft 2 passed all three checks (self-review).

### learn/secondary-overlap-01 — Overlap: stagger the settles (head +2 f, arms +3 f, cloth +4 f and more), keep loose parts in contrast, and give secondary actions a visible cause

- Recorded (UTC): 2026-11-28T15:04:49+00:00
- Evidence: studio-output/learn/secondary-overlap-01 ours_strip1-3 vs reference-ig-03 51.6-52.8 s (the broken beam keeps tipping after the slam)
- Cause / rationale: Attempt 1: a white towel on a cream wall (its drag was invisible) and a plank out of frame. Attempt 2: the plank stood away from the counter he hit, so its fall had no readable cause.
- Correction / recipe: After a hard stop: the body stops on the hit frame; head +2 frames, arms +3, cloth +4 and more, each a damped overshoot (amp*e^-kt*sin wt). Loose parts get a saturated colour and a dark outline. Secondary reactions sit on or next to the thing that was hit (the mill on the counter): wobble at once, topple about 0.3 s later. Skid dust and panting keep the hold alive.
- Verification: Critic passed both criteria on attempt 3. Still open: local motion 1.0% vs ref 7.4% (escalated after 3 attempts).

### learn/want-need-01 — The flaw must create the predicament, not just sit beside a chance event

- Recorded (UTC): 2026-11-28T15:05:57+00:00
- Evidence: studio-output/learn/want-need-01 draft1-2, verdicts1-2
- Cause / rationale: Draft 1's crisis was a chance bass drop; Dev's controlling flaw had no part in causing it, and the two re-doing beats were at the same level.
- Correction / recipe: Make the flaw put the character where the trouble hits. Dev undoes Ollie's safety fix to keep his tubs flush with the edge, so the bass drop throws exactly those tubs. Escalate the flaw beats (correct the work -> undo a safety fix). Show the change in one small action (he leaves the crooked tub).
- Verification: Draft 2 passed all three checks (self-review).

### learn/motion-in-picture-01 — Frame-filling subject + movers everywhere closes most of the motion gap; dense fields jostle in place (about a particle width per 2 frames), and a camera move should reveal something

- Recorded (UTC): 2026-11-28T15:11:40+00:00
- Evidence: studio-output/learn/motion-in-picture-01 take1-3 vs reference-ig-01 12.2-15.8 s; compare1/compare3.jpg; take*_motion/motion.json
- Cause / rationale: Earlier drills were 63-87% below the reference. Here: take 1 had all 150 bubbles rising one way (read by the tool as camera pans while our camera was locked) and a push-in where the ref pulls out and tilts up; I misread the ref's zoom direction from a contact sheet.
- Correction / recipe: Fill the frame with the subject; give every band its own movers (steam, surface, particles, hero chunks, flames). Dense fields: most particles jostle in place with slow drift (about a particle width per 2 frames), only some travel. Copy measured camera moves, not the contact-sheet impression; a pull-out/tilt should reveal a new subject (the ladle). Uniform one-direction particle flow fools the camera estimate.
- Verification: Local motion -23% / -19% / -34% vs earlier drills' -63% to -87%; false pans gone in take 3; camera now matches ref timing. Escalated: take 3 jostle too small (-34%).

### learn/rule-of-three-01 — Rule of three: the break is different in kind, not bigger, and it is the shortest beat

- Recorded (UTC): 2026-11-28T15:14:19+00:00
- Evidence: studio-output/learn/rule-of-three-01 draft1-2
- Cause / rationale: Draft 1's third beat was the same action made bigger (a huge thump, an exploding stack), which is escalation and the expected outcome, and it was the longest beat.
- Correction / recipe: Keep the trigger identical the third time and flip the pattern in kind (the tester becomes the tested: Dev wobbles and goes tink instead of the plates). Break in about 1.5 s, then a short button.
- Verification: Draft 2 passed (self-review).

### learn/escalation-01 — Escalation climbs by closeness to what the character cares about, not by a list of objects

- Recorded (UTC): 2026-11-28T15:14:20+00:00
- Evidence: studio-output/learn/escalation-01 draft1-2
- Cause / rationale: Draft 1 listed objects reacting (glass, pans, forks, fridge) with nothing at stake for Dev; the fourth beat was calmer than the third and there was no peak.
- Correction / recipe: Give the character something fragile they care about and climb by distance and energy toward it (across the room -> beside him -> moving toward it -> inside it); his response climbs too (unaware -> freeze -> block -> shield). Peak just before the end; the button can be a small reversal (his relief blows a strand off).
- Verification: Draft 2 passed (self-review).

### learn/hook-cold-open-01 — Hook: frame 1 is the wrong thing; answer the question with a picture at the end

- Recorded (UTC): 2026-11-28T15:14:20+00:00
- Evidence: studio-output/learn/hook-cold-open-01 draft1-2
- Cause / rationale: Draft 1 spent 2 s on an exterior and a walk-up before anything was wrong, and answered the mystery with a spoken explanation.
- Correction / recipe: Cut every establishing shot before the anomaly; open on it. Keep the answer for the last quarter and show it as an image (the subwoofer on its back), then land the payoff after it.
- Verification: Draft 2 passed (self-review).

### learn/dialogue-grammar-03 — Real shot sizes land with frameShot/ovShoulder; open problems are depth staging in 9:16, small gag beats in wide frames, and same-colour hand overlaps

- Recorded (UTC): 2026-11-28T17:05:59+00:00
- Evidence: independent learn-craft-critic verdicts1.json and verdicts2.json in studio-output/learn/dialogue-grammar-03; review/critic_*.jpg and critic2_*.jpg
- Cause / rationale: Attempt 1: all-wide habit fixed by frameShot, but the bob was 1-2 px and the waiter was too small. Attempt 2: depth staging too timid (Pip's head only 1.15x Moss's, at the same height, limbs tangling); S6 hands overlapped into one cluster; Moss's black grip vanished on his black thigh; the waiter's copied bob was ~2% of the frame. An un-critiqued re-measure used one attempt slot (engine bug, now fixed).
- Correction / recipe: 9:16 two-shot: near character's head ~1.6x the far one's, lower in frame, a body width apart, the table filling the bottom. A gag beat must be framed waist-up at least, the same size as the original beat. Never overlap two same-coloured hands; separate same-colour overlaps with a thin background-coloured gap line. The OTS shoulder and real CU/MCU framing now pass on sight.
- Verification: Critic passed cuts-on-the-line on both attempts; OTS shapes, readable S5 bob, S6 hands in frame and S7/S8 split landed in attempt 2. Escalated (one slot lost to the re-measure bug).

### learn/camera-grammar-01 — Hide a scale change inside one dive: diagram first, brackets lock, accelerate into a colour until it fills the frame, start the next scene in that colour

- Recorded (UTC): 2026-11-28T19:56:18+00:00
- Evidence: reference-ig-06 dive frames 2.0-2.8 s (study/dive_frames.jpg); ig-06 has no hard cuts in 27.7 s; ours: learn/camera-grammar-01 frames2/frames3.jpg; ref_motion: take1 3 cuts + 2.0x, take2 one continuous 6.3x zoom (half at 83%)
- Cause / rationale: Take 1 swapped layers mid-zoom with shapes that did not line up, so the tracker (and the eye) read cuts. The reference never cuts: it turns the face into the cut-away before the dive and swaps scenes on a matching colour field.
- Correction / recipe: Order: (1) change the look (face -> cut-away) while still, (2) brackets lock on the target, (3) accelerating zoom (log-zoom ~ size^(k^2.6..3), half done at ~75-80% of the move) into a glow around the target, (4) the glow fills the whole frame, (5) next scene starts in the same colour with a 2-frame scan glitch, (6) land with a decelerating pan and a ~2 degree roll. Measurement note: a flat colour field breaks camera tracking, so check the frames by eye.
- Verification: Take 3: continuous dive confirmed on frames; zoom measured half at 78% (ref 71%); still open: tissue motion 9.1% vs 22.5% (escalated).
