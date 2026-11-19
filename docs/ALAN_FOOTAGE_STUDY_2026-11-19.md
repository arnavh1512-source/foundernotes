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

- **Cut 11 (sound):** measured Alan's audio: AvA ~2.4 hits/s, sound present 34%, -16.4 LUFS, LRA 13.9 (effects only, silence between); Geometry Dash 1.7 hits/s over music, -16.6 LUFS. Added `SOUND_EVENTS` tied to contacts and `scripts/stick-sfx.py`, which synthesises original effects (steps, clanks, rattle, twang, whoosh, thuds, slam, pluck, chime) with no samples. Result: 2.14 hits/s, sound present 43%, 23/23 effects within one frame of their contact, about -17 LUFS. Fixed masking (heave clanks under the rattle, the bounce under the impact tail, the last step under the chime). **Listening by a person is still required**; the assistant measures audio but cannot hear it.

## Open gaps (update every cycle)
- Passing step still tight at the knees; legs about 51% of height.
- Timing still smoother than Alan's: more snap-and-hold through the whole piece (not only the fall).
- Dust still faint against the floor colour.
- No ensemble yet. Sound exists but is unheard by a person; 10.6–13.4 s is deliberately silent (judge once narration exists).

## Where claude-youtube comes in
When we move from craft exercises to real videos, `.claude/skills/claude-youtube/` is used after the animation and narration are locked: `hook` variants to test in the pilot, `seo`/`metadata` for titles, descriptions, tags and chapters, `thumbnail` briefs, `shorts` for the summary Short, and `analyze` once the owner shares real analytics. Its adapter rules apply (benchmarks are heuristics; no keys, OAuth or paid tools without approval).
