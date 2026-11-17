# Philosopher motion study: first revision cycle

## Scope and provenance

An original 24-second silent blocking study, not the 60-90-second narrated pilot, completed film or evidence of parity with the reference channels. Five beats: closed gate, study, map insert, staircase, overlook. Original procedural vector-style drawings with reproducible grain; no external artwork, voice, music or footage. This is not hand-painted animation.

The existing Philosopher/map concept is being tested for visible explanatory action: a blocked familiar route leads to inspecting a map and testing an overlooked path. No empirical psychological claims are made. Do not extend this craft test into a new script or a full film without the existing viewer-first and pilot gates.

## Artifacts

| Item | Result |
| --- | --- |
| First encoded cut | `Philosopher-Motion-Cut-1a.mp4`, SHA-256 `9661084f4092c2793af6fdad62de87eb281c6f366bb7dba2c7467a69932b2307` |
| Revised encoded cut | `Philosopher-Motion-Cut-2a.mp4`, SHA-256 `21b4286b78ec40f207ba74afde8327512859c684fa99a0b59942f08c4294a394` |
| Revised video | https://chatgpt.com/library?file_id=libfile_c868f13d44108191a68b42045618bffa&account_id=personal |
| Technical probe | H.264, 1280 x 720, 24 fps, 24.000 seconds, no audio stream |
| Source | `tools/philosopher_motion_study.py` |
| Tests | `tools/test_philosopher_motion_study.py`: two tests passed locally |

Initial encoding failed because Pillow requires an integer line width; scaled limb widths were floats. Rounded at the shared drawing boundary, then verified by rendering all five shots at multiple times. The failed attempt is not a completed cut.

## Review method and revisions

Reviewer: this session's authoring assistant. Method: source inspection plus ten sampled stills from each cut, at 0.8, 2.8, 5.8, 7.7, 10.3, 12.7, 15.8, 18.3, 20.5 and 23 seconds. Sampling does not establish full temporal continuity. No independent critic, full playback, listening, owner approval or accessible reference-footage comparison occurred. This cycle is not a `studio_loop.py` approved production run: the 24-second study is intentionally below its pilot duration and lacks narration.

| Finding | Evidence | Change | Verification and remaining work |
| --- | --- | --- | --- |
| Table hides pointing hand | Cut 1a study frames, 5.8 / 7.7 s | Draw foreground forearm and hand above the tabletop | Cut 2a samples show the hand on top. Arm anatomy and complete motion still need review. |
| Map gesture cuts across a bent route; ink appears in whole segments | Cut 1a map frames, 10.3 / 12.7 s and source interpolation | Match finger movement to both route segments; reveal ink progressively | Revised sampled positions align; regression test checks later ink is not revealed prematurely. Complete playback remains pending. |
| Stairs use a diagonal glide without planted steps | Cut 1a staircase samples, 15.8 / 18.3 s and source position formula | Alternate a planted foot with a lifted swing foot on stair coordinates | Cut 2a samples show feet on stair treads. Weight transfer, knee anatomy and sliding across the complete cycle remain pending. |

Additional revised details: downward gaze in the study, a strained gate expression, and a ground shadow. They are authoring changes, not proof of improved audience retention.

## What still fails the intended standard

- The simple geometric figures and environments need richer art direction, more nuanced poses and stronger expressions for the requested final look.
- Gate/overlook shots include prolonged stillness. Full motion pacing has not been reviewed.
- The wide map points and close-up action need more careful spatial and gesture continuity.
- No natural narration, dialogue timing, lip sync, sound design or final subtitles exist in this test. Text is a visual caption for the silent study.
- The supplied reference videos remain unavailable for audiovisual comparison; no reference criterion is marked passed by assumption.

Next cycle: review actual playback, refine one character interaction and its anatomy before expanding the scene count, obtain usable narration and measured timings, then produce the actual 60-90-second pilot through the existing evidence-bound workflow. Read the mistakes file before starting. This work does not run indefinitely or continue unattended after the session.

## Reproduce on this host

Requirements: Python with Pillow and FFmpeg on PATH. The drawing script currently uses Windows Georgia/Arial fonts; configure equivalent licensed font paths before porting it to another OS.

```powershell
python -m unittest discover -s tools -p 'test_philosopher_motion_study.py' -v
python tools/philosopher_motion_study.py --out studio-output/philosopher-study/cut-1.mp4 --cut 1
python tools/philosopher_motion_study.py --out studio-output/philosopher-study/cut-2.mp4 --cut 2
```

Use new output names for later runs; the script refuses to overwrite a prior cut. Keep source, reviews and correction history in git; rendered media belongs with the episode artifacts.
