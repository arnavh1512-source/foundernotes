# Alan Becker footage study: craft rules for our stick animation
Date: 2026-11-19. Read this before animating or reviewing any stick scene. It turns the owner-supplied reference footage into rules we test against every cut. Owner benchmark: **reach Alan Becker's level**. Owner decision: **keep faces** for expression (Alan's own figures are faceless; we combine his body acting with DayOne-style minimal faces).

## Sources actually studied
| Film | Access | What was examined |
| --- | --- | --- |
| Animator vs. Animation (HD), `Qb1VvUf21L4` | Owner download, 132.8 s, 990×720, 29.97 fps | Every-5 s overview; every frame of 96–97 s and 56–57 s; frame-difference and held-frame measurement |
| Animation vs. Geometry Dash, `C637UcpHfNY` | Owner download, 143.1 s, 1280×720, 23.98 fps | Frame-difference and held-frame measurement |
| Animation vs. Game Design, `dz04yXwSkQY` | YouTube storyboard thumbnails (~2 s apart) | Shot and pose observations; much of it is a sponsored app segment |
| DayOne Films "SELF RESPECT", `D8T891uWpiE` | YouTube storyboard thumbnails (~2 s apart) | Faces, recurring prop, bookends |
Reference media stays private in git-ignored `studio-output/references/`; nothing is copied into our films. Sound has not been reviewed yet. More Alan films (for example Animator vs. Animation 4) are pending.

## Measurements (frame difference on 320 px greyscale; ffmpeg scene detection at 0.3)
| | AvA original | Geometry Dash | Our cut 4 | Our cut 8 |
| --- | --- | --- | --- | --- |
| Hard cuts | 0 | 0 | 7 | 7 |
| New drawings per second | ~17 (43% held) | ~23 | ~26 | ~26 |
| Mean motion per frame | 2.0 | 12.3 | 2.4 | 3.3 |
| Seconds with little motion | 19% | 3% | 21% | **7%** |
Pixel motion depends on figure size and background, so compare trends, not absolute parity.

## Rules (each is checked in review; most have a test in `tests/stick-performance.test.mjs`)
1. **Start in motion.** Characters enter acting; no static opening hold. (Cut 8 walk-in.)
2. **Failures are full-body events:** release → airborne (spine tipped well back, feet off the floor) → impact with squash and bounce → emotional reaction → recovery. Ease out of a release; accelerate into an impact.
3. **The world reacts.** Obstacles spring back and settle; impacts throw dust and shake the frame; objects are handled, broken or used. The obstacle's real state (locked) never changes by magic.
4. **Overlapping action.** Parts lag and overshoot: a springy head that whips on impacts and settles after turns; trailing limbs.
5. **Pose range.** Each beat gets a clearly different silhouette (crouched, stretched, airborne, sprawled), not variations of upright.
6. **Effort has rhythm:** heaves and pulses instead of a frozen strain.
7. **Weight on contact:** hips dip when a foot lands; planted feet never slide.
8. **Sturdy proportions:** a big head (at least about 1/5.5 of standing height) sitting on the shoulders with no neck; bold, even lines (about 3% of height). Thin lines, a tiny head and a long neck read as a "stick insect" (owner note).
9. **Several actions at once** when the story allows (an ensemble reacting differently).
10. **Faces (our addition, from DayOne):** two eyes, two brows, one mouth; an expression per beat; effort (wide gritted mouth, brows down) must differ from shock (wide eyes, round mouth).
11. **Staging:** Alan holds one continuous screen and moves within it. Our explainer channel may cut (DayOne and psychology references do), but the characters must still carry the motion energy.

## Cycle log
- **Cut 9 (`0fa885e2…`):** walk bob (body rises on the passing step, sinks on contact) applied to walk and stairs, hands carried with the body; dust rebuilt as an irregular billowing cloud.
- **Cut 10/10b (`6ea8490e…`):** face features turn toward where the head points (the climb no longer reads as walking backwards); lower foot lift, so no prancing; walk-in arms swing nearly straight and opposite the legs (no "chicken wing" elbows). Fifteen tests pass.

- **Cut 11 (sound):** measured Alan's audio: AvA ~2.4 hits/s, sound present 34%, -16.4 LUFS, LRA 13.9 (effects only, silence between); Geometry Dash 1.7 hits/s over music, -16.6 LUFS. Added `SOUND_EVENTS` tied to contacts and `scripts/stick-sfx.py`, which synthesises original effects (steps, clanks, rattle, twang, whoosh, thuds, slam, pluck, chime) with no samples. Result: 2.14 hits/s, sound present 43%, 23/23 effects within one frame of their contact. Correction: the first final mix measured -18.7 LUFS; `scripts/stick-mix.sh` now compresses gently and two-pass normalises to -16.8 LUFS (true peak -1.5 dBFS target), matching Alan's ~-16.5. Fixed masking (heave clanks under the rattle, the bounce under the impact tail, the last step under the chime). **Listening by a person is still required**; the assistant measures audio but cannot hear it.

- **Cut 12 (`09b4916d…`, timing):** studied AvA 56–57 s: the blast reaches full size in about 5 frames, then lingers about 0.8 s while shifting from bright to dull, and the whole frame tilts on impact. Added anticipation (hands pull back before shooting to the bars, a head counter-move before the turn, a crouch before the first stair step), snap easing (slow start, fast middle, firm stop) on key actions, fast-build/slow-decay dust that dulls as it fades, and a frame tilt on the big impact. Motion 3.27 mean, 7% quiet seconds: energy moved into key moments rather than added. Seventeen tests pass.

- **Cut 13 (`87fc2dc2…`):** A/B of held drawings on twos for the character (`ON_TWOS` switch in the template): 40% held frames vs 8% on ones (Alan AvA 43%), but Alan's newer Geometry Dash is almost all new drawings (~23/s), so smooth motion stays the default and twos remains a style option. Added the claude-youtube retention lens (Shorts guide, unverified heuristics used as a checklist): hook in 1–3 s and an interrupt in the first 5 s pass; the camera held static and wide for 3.4 s (7.2–10.6 s), so it now pushes in from 8.8 s and follows the climb (figure larger sooner). New test: no static camera longer than 3 s. Eighteen tests pass. Owner asked for a copy of Alan's film for comparison; declined (copyright and the originality rule) in favour of a timing-matched study, ink-on-white comparison renders and a private side-by-side.


## Master study: timing-matched copy of one jump (private)
Owner request 2026-11-19: learn by copying. A ~1.6 s passage of AvA (25.3–26.9 s: a toss and look-up, crouch, jump onto the black block, landing squash) was studied by measuring his key drawings on a grid and animating them on his timing with his proportions. The study files and side-by-side reviews live only in git-ignored `studio-output/master-study/`; they are never committed, published or reused in a film. Only these measurements and rules are recorded here.

**Measured from his drawings (990×720 HD frame):**
- Animated at **16 drawings per second** (the Flash timeline in the footage reads 16.0 fps; the HD video repeats drawings).
- Jump timing: crouch at 0.78 s, launch 0.84 s (wind-up of about **2 drawings**), peak 0.96 s, over the block 1.09 s, landing **squash held about 3 drawings** (1.21–1.28 s), up at 1.34 s. Launch to landing takes about **5 drawings (0.31 s)**: the wind-up is short and sharp, the air time fast, and the landing squash held longer than the wind-up.
- Proportions: figure **170 px tall with a 60 px head (head about 1/3 of height)**, lines about 10–11 px (about 6% of height), no neck, legs about 44% of height.
- **Limbs are near-straight strokes.** Standing legs make a clean upside-down V and arms hang straight; knees and elbows bend only during action (crouch, landing). Our copy first used limbs longer than the joint spacing, which forced permanent bends (bow legs, boxy elbows, a folded "Z" at the peak). Making limb length about equal to the joint spacing (arms 27+27, legs 32+32 for his 170 px figure) fixed the standing and landing poses. The peak still tucks where his legs dangle (key pose not yet exact).

**Transfer to our rig (next rounds):** head toward about 1/3 of height; limb lengths close to typical joint spacing so neutral limbs read straight; jumps and failures with a ~2-drawing wind-up, a fast air phase and a landing squash held longer than the wind-up.

- **Cut 14/14b (`a9b01d5a…`, master-study transfer):** checked our rest poses: shoulder–hand 155–167 px against a 174 px arm, hip–foot 219–233 px against a 235 px leg (89–97% of length, close to Alan's ~93%), so the main rig does not have the study copy's bent-limb problem. Head radius 47 → 62 (about 1/4 of height, toward Alan's 1/3), lines 15 → 20 px (Alan about 1/6 of head width), landing squash held 0.12 s before the bounce (Alan about 3 drawings), bounce sound moved to match. Eighteen tests pass; mix -16.8 LUFS. Sent to the owner for a quality check.

- **Cut 15/15b (`4a05a553…`, owner QC "still stiff"; owner: remove footsteps):** cut 14b frames 5.4–6.6 s showed the figure rising like a rigid board: both arms held one shape for 18 frames and the standing pose froze apart from the face. Measured frozen-arm frames (elbows moving under 0.5 px, grip excluded): **30%**. Systemic fixes: free hands follow through on a damped spring relative to the chest (contacts blend in and out over 0.12 s), arc bulge and idle drift, breathing and weight-shift on holds, spine drag against chest velocity, hands clamped above the floor. A procedural pass alone only reached 14% and still looked almost the same, so an **acting beat** was added: he brushes the dust off his hands after getting up. Result: **9%** frozen-arm frames and visibly changing arm shapes. Footstep sounds removed at the owner's request (effects remain on the gate, fall, slam, notice and relief). Eighteen tests pass. A body-proportion change (shorter legs and torso) is parked as a work-in-progress patch; its hip solver works, but the facing-turn knees and some tests still need work.

- **Cut 16/16d (`68b30ff1…`, owner QC "the hands are so odd"):** cut 15b frames showed (1) back-arm elbows jutting sideways like a hand on the hip, because both arms always used the same IK bend direction; (2) knob dots at the hand ends; (3) forearms folded across the chest in the brush beat. Picking the lower-elbow branch alone caused visible flips, so each elbow now keeps its bend side and switches only near full extension (a hysteresis track); the remaining 42 large elbow jumps are all genuine fast moves. That exposed the root cause: free hands sat too close to the shoulders, forcing 60°+ bends, so any bend direction looked odd. Applying the master-study rule, relaxed free hands now extend to ~98.5% of arm length (near-straight strokes), the arch-jamb contact moved lower so that arm hangs straight, the brush moved to belly height, and the hand dots were removed. Strongly bent free arms: 15% → 10%. Eighteen tests pass.

- **Cut 17 (`86fb56a6…`, remaining stiffness):** measured frozen hip/torso/knee frames (all moving under 0.6 px): **23%**, in three dead stretches: 5.83–6.43 s (brushing off, only the arms moved), 10.93–11.23 s (the "breath" had no breath) and 11.63–13.07 s (a 1.4 s statue on the look back). Added whole-body acting: during the brush the upper body leans back huffily and bobs with each rub; on arrival a real breath (shoulders rise, knees give on the exhale); on the look back the weight drifts toward the gate, the head tilts and a sigh lifts and drops the shoulders. Frozen frames **13%**; one 0.47 s stillness remains at the start of the look-back close-up (kept as an intentional dramatic hold). Head-hold timing tests now check the head relative to the body. Eighteen tests pass.

## Open gaps (update every cycle)
- **Legs too long:** about 1.9× head height against Alan's ~1.25× (torso also long). Needs a re-keyed skeleton (dedicated round). Passing step still tight at the knees.
- Timing: anticipation and snap now on key actions; held drawings (Alan animates largely on twos, 43% held frames) not yet tried.

- No ensemble yet. Owner removed footsteps; remaining effects not yet confirmed by listening.
- **Stiffness:** arms (9% frozen) and body holds (13% frozen) improved; owner re-check pending.

## Where claude-youtube comes in
When we move from craft exercises to real videos, `.claude/skills/claude-youtube/` is used after the animation and narration are locked: `hook` variants to test in the pilot, `seo`/`metadata` for titles, descriptions, tags and chapters, `thumbnail` briefs, `shorts` for the summary Short, and `analyze` once the owner shares real analytics. Its adapter rules apply (benchmarks are heuristics; no keys, OAuth or paid tools without approval).
