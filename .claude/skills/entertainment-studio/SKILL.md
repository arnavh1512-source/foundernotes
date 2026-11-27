---
name: entertainment-studio
description: Entertainment IP profile for FounderNotes (scripted comedy and story series such as Half Landing), separate from Think! educational videos. One episode workspace links the script revision, reusable assets with stable IDs and versions, the shot plan, audio cues, rendered takes, the selected take and the export. Shots render one by one into a cache, so variants reuse identical shots and a revised shot re-renders alone. Use for script-to-animatic work on Entertainment IP episodes. Think! remains the default for educational work.
---

# Entertainment Studio

**Think! is the default.** Educational videos keep every Think! rule in CLAUDE.md (viewer-first gate, 8-minute minimum, owner narrator, Think! logo). This skill applies only when a workspace says `"profile": "entertainment-ip"`. Entertainment IP episodes carry their own series brand, never the Think! logo or narrator, and are checked by `ep_check.py` instead of the long-form gates.

The idea, borrowed as a workflow lesson (no service is used): a project keeps its visual references, shot direction, alternate takes and approvals connected, so any frame can be traced back to the script line and the exact asset versions it was drawn from.

## Workspace

One folder per episode under `studio-output/<series>-<episode>/` (git-ignored, unpublished material stays local):

```
workspace.json        the manifest: everything below is linked from here
script/<ep>.r<N>.md   script revisions; the manifest pins one revision and its sha256
assets/<ID>.v<N>.json reusable references (character, wardrobe, prop, location), one file per version
scenes/_common.js     drawing helpers shared by every shot of the episode
scenes/<scene>.js     one file per shot scene (so a change re-renders only that shot)
film/                 generated per-shot pages (engine rig + one scene); do not edit
takes/clips/          rendered shot clips, named <shot>-<render key>.mp4 (the cache)
takes/<variant>.mp4   assembled takes
export/               the approved take, copied with its labels (e.g. TEMP-AUDIO)
review/               review notes, frames and small-screen checks
```

The manifest holds:
- `script`: path, revision and sha256 of the pinned script.
- `assets`: stable IDs (`<SERIES>-<KIND>-<NAME>`, e.g. `HL-PROP-SPOON`) with versioned files.
- `shots`: id, scene, duration, framing, script lines covered, and `uses`: the exact asset versions the shot draws.
- `audio_cues`: per shot, at a local time; `temporary: true` plus a note when no approved sound or voice exists.
- `variants`: alternate takes as small overrides (e.g. a hold shot's duration). Everything not overridden is the same shot render, so framing, performance and audio stay identical by construction.
- `takes`, `selected` (take id, reason, reviewer notes with timestamps) and `export`: written by the build and the review.

## Build

```bash
python3 .claude/skills/entertainment-studio/scripts/ep_build.py studio-output/<ws> --precheck # frames from every shot first: nothing renders until checked
python3 .claude/skills/entertainment-studio/scripts/ep_build.py studio-output/<ws>          # render missing shots, assemble takes
python3 .claude/skills/entertainment-studio/scripts/ep_build.py studio-output/<ws> --export # copy the selected take to export/
python3 .claude/skills/entertainment-studio/scripts/ep_check.py studio-output/<ws>          # entertainment checks
python3 .claude/skills/entertainment-studio/scripts/ep_review.py studio-output/<ws>         # measured review: loop seam, sound sync, phone safe zones
```

`ep_build.py` reuses the studio's tools: the Think! stick-engine rig (`think-stick-engine/engine/stick.html`, `faces.js`) for drawing, `motion/scripts/render.mjs` for frame-accurate rendering, `assemble.py` for concatenation and loudness, and `qc_video.py` (with `--min-duration`) for technical QC. Each shot's render key is a hash of the rig, `_common.js`, its own scene file, its shot definition and the asset version files it uses. A shot re-renders only when one of those changes; the build reports which shots rendered and which were reused. **Phone rule for sound:** most viewers hear Reels on a phone speaker, which reproduces little below ~150 Hz. Start every episode's `sound/` from the canonical `.claude/skills/entertainment-studio/sound/make_foley.sh` (every sound keeps real energy above 150 Hz); `ep_review.py` flags any cue sound that is mostly below it. Found on A03/A04: the sound-check boom was 99.7% sub-bass, so the cause of the gag was near-silent on phones.

An episode's own sounds go in `sound/` (e.g. foley synthesised by a local script) and are used before the shared CC0 bank; a cue's optional `dur` cuts a sound so it can stop on an action. Measure sync rather than assume it: the A03 snap was buried until the stretch sounds were cut to end just before it.

Audio is rebuilt every time (cheap): cues are placed at shot start plus local time over a quiet room tone, compressed, and normalised with a measured two-pass `loudnorm` before assembly, because `assemble.py`'s single pass undershoots on short clips with sparse cues.

Lessons from A03 (first use): build every pose with `P()` (a partial pose has no legs and the figure silently vanishes); IK picks the lower elbow so arms never swing up across the face; per-frame motion measurement catches a "moving hold" that is actually frozen. When a character pulls a prop, pull it toward the character's own shoulder: pulling it away from the body runs out of arm reach, the IK clamps and the hand leaves the prop. Give every gag beat a visible cause and plant what the payoff depends on (A03: the sound-check thump knocks the spoon off; the caramel string shows it is sticky before it sticks), and keep the physics consistent (a spoon glued caramel side down shows its clean back).

## Vertical Reels and Shorts

Set `"format": "vertical"` in the manifest for a 1080x1920 canvas (Instagram Reels, Shorts): the same rig and scenes, vertical assembly and QC. `"overlay_tag": false` drops the on-screen ANIMATIC label for a post-ready cut (the export filename still says TEMP-AUDIO while sound is temporary). A vertical render never reuses a landscape clip. Frame for the phone: keep the key action out of the bottom ~20% and the right edge, where Instagram's buttons and caption sit. First Reel: `studio-output/half-landing-a03-reel/` (A03 re-cut with a hook at 0 s, close-ups, a third-thump ending and a seamless loop).

## Checks (`ep_check.py`)

Fails when the links break: missing or changed script, duplicate or malformed asset IDs, a shot using an asset version that does not exist or whose file changed, a cue pointing at a missing shot, temporary sound without a note, a take built from an outdated shot render, a selected take without a recorded reason, or an export that is not the selected take. Temporary sound must also show in the export filename.

## Rules

- Original characters, scenes and assets only. References guide craft, never copied.
- Temporary sound is labelled as temporary in the manifest, the export filename and on screen. Approved voices only from owner-approved profiles (see CLAUDE.md); never clone a voice for a character.
- No paid services, uploads or publishing without the owner's approval.
- Review at playback speed and say what was actually observed. A structural PASS from `ep_check.py` is not a creative approval.
- A reference clip, when the owner supplies one, can be broken down with `rea-video` (offline only); report exactly what it verified.
