# Original stick-performance exercise: gate interaction

## What was produced

[View the saved v3 exercise](https://chatgpt.com/library?file_id=libfile_6fadb73f88488191808d4953f1478f5e&account_id=personal).

An original 12-second stick-character scene, H.264 1280 x 720 at 24 fps, with an AAC track of original procedural footsteps and metal-contact cues. No narration, external artwork, copied reference characters, purchased assets or third-party music. This remains a local craft exercise, not the 60-90-second pilot, final film, mastered soundtrack or evidence of benchmark parity.

The existing `tools/philosopher_motion_study.py` was extended with `--style stick`; it reuses the repo's two-link geometry, deterministic time functions, encoding path and tests. Actual encoded frames were extracted with the repository's `review_frames.py`. Because the normal browser renderer and live narration route remain unavailable here, this is still the explicitly limited Pillow fallback. It is not represented as an HTML/Remotion pipeline run or a production approval.

## Reference-derived question

Alan Becker is now in the benchmark register. The anticipation chapter at 2:07 in his published principles compilation was studied through captions/chapter metadata. It suggests a concrete question for our original exercise: does the character visibly prepare for the physical action before the main effort? Tutorial: https://www.youtube.com/watch?v=uDqjIdI4bF4 . This is a proposed application, not evidence that the reference's movement or sound was watched or matched. Day One Films, PsychToons, PsychDoodle and the Bahaa tutorial remain part of the reference set; direct audiovisual comparison remains pending.

## Render-review-revision history

| Version | Observed issue / change | Evidence and limits |
| --- | --- | --- |
| v1 | First stick scene: approach, grip, effort, release and another character indicating an alternative | SHA-256 `d059c9ef6b058ad794df3f9120ba5befec2a47bf09884d1b29065e1b2afcece8`; reviewed sampled poses; extracted encoded frames around grip and release |
| v2 | Added interpolated contact/release and entrance from beyond the left edge; changed elbow bend | SHA-256 `6a767f0585c8dfee8b467fb8f2a50e6d5887657fb6ce155d7f5614981675ea8c`; sampled poses revealed awkward folded rest arms |
| v3 | Replaced rest-to-grip point interpolation with rotation of fixed-length arm segments; moved the final stance closer to keep the target reachable | SHA-256 `644f25a1f2112b81938c0c2981c3bbbd458572e9eda79e393828f9c89256968a`; encoded samples inspected at 1.5, 2.8, 3.25, 5.7, 7.5 and 10.5 s |

Reviewer: the authoring assistant, using source inspection, rendered pose sheets and decoded video stills. No independent critic or full audiovisual playback was completed. The prior versions were retained locally; the current source produces the latest stick treatment. The `--cut` value labels the revision for the stick treatment; the earlier blocking treatment retains its separate variants.

Five local tests pass: all-shot rendering/determinism for the prior scene; prior arm lengths; progressive map reveal; stick grip-weight boundary continuity; and stick arm lengths throughout reach, including exact contact endpoint. Technical probe confirms 12.000 seconds, H.264 video and AAC audio. These checks do not prove natural motion, comfortable sound, audience response or complete physical realism.

## Still unresolved

- Walking remains simplified; foot sliding, knee paths and weight transfer need full playback review.
- The reaction and alternate-route cue need stronger silhouette differentiation and a better payoff before expansion.
- Procedural cues were generated and muxed but not listened to; final sound quality and perceptual sync remain pending. No speech was synthesized.
- The scene has one wide composition; future framing changes must earn their place rather than conceal acting problems.
- Reference footage and sound have not been compared directly. No benchmark category is passed by assumption.

## Reproduce current treatment

```powershell
python -m unittest discover -s tools -p 'test_philosopher_motion_study.py' -v
python tools/philosopher_motion_study.py --out studio-output/philosopher-stick-pilot/stick-exercise-v3.mp4 --cut 3 --style stick
python .claude/skills/podcast-scout-skill/scripts/review_frames.py studio-output/philosopher-stick-pilot/stick-exercise-v3.mp4 --out studio-output/philosopher-stick-pilot/review-v3 --times 1.5 2.8 3.25 5.7 7.5 10.5
```

Use a fresh output path. Windows font paths are currently required by the fallback drawing script. The standard measured-narration production route and all pilot/QC/review gates remain authoritative.
