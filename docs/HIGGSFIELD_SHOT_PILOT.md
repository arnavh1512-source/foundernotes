# Higgsfield shot pilot for Think!

Use the existing 20–40 second narrated treatment comparison. Test one character or environment shot first. Keep the approved narration, captions and duration identical across versions.

## What the investigation established

- REA 6.10.1 parsed the public Cinema Studio guide's entry point and two directly imported scripts as inert JavaScript (8,289 bytes, three parsed files, zero parse failures). The broader first pass timed out on a larger bundle. A targeted retry inventoried the 1,023,791-byte bootstrap bundle, but REA skipped analysis because its intermediate static facts exceeded the tool's fixed 8 MiB ceiling. Retry evidence ID `ev_e5b12e393fa227ef002bd167493ed8c744f4147940ad929717d2137f8399025c`. This covers public frontend code. Live browser capture could not reach the local DevTools port, so live generation and model behavior remain unverified. REA evidence ID `ev_508e0b0597b23769791283456c62890260657f19a3364d6c05f0d51cdb2472b8`.
- Higgsfield's public guides describe locking a storyboard and using reusable character and location references, then choosing the framing and one camera move per shot. [Storyboard workflow](https://higgsfield.ai/blog/script-to-ai-storyboard-shot-list) · [Cinema Studio controls](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide)
- Its documented Kling image-to-video workflow requires an opening image and accepts ordered intermediate keyframes and an optional ending frame. [API reference](https://open.higgsfield.ai/models/kling-video/v4.0/image-to-video/api-reference)

## Live public workspace check

- The public Cinema Studio video workspace exposes separate references, elements, film setup, camera, palette, lighting, and camera movement controls. Output defaults observed were 1080p, 16:9, five seconds and one variant. The Generate button displayed 80 next to its credit icon. These are observed settings, which can change. [Cinema Studio](https://higgsfield.ai/generate)
- Opening camera movement required sign-in. The sign-in screen requires users to confirm they are at least 18. The live check ended there, without submitting a generation.
- A targeted REA retry on the 321,326-byte public runtime module parsed its syntax but reached the member-mutation analysis limit and produced zero findings. Evidence ID `ev_d24cef3e154c7361dd3d33e33bfe77228230c707f56ce05cec1971a3d81f6ebc`.
- For the Think! pilot, save references and visual defaults at episode level, then record framing, camera intent and the physical contact pose on the individual shot. Keep the generated-video comparison optional and use the same shot brief for a local engine treatment.

## Copy into the storyboard for the candidate shot

| Field | Example |
| --- | --- |
| Visual job | Make a deliberate pause before acting readable |
| Approved references | Think! character sheet and existing study background |
| Opening pose | Medium three-quarter shot. Student's hand rests on desk, phone face up |
| Action and timing | Phone buzzes. Hand reaches, pauses, then grips and turns it face down |
| Intermediate contact pose | Fingers visibly grip the phone before the turn. Keep the wrist and phone aligned |
| Ending pose | Phone face down in the same spot. Student's eyes return to the page |
| Camera | Locked medium shot. Hands, phone and face stay readable |
| Continuity | Same silhouette, desk layout, light and palette at both cuts |
| Duration | Use the exact in/out frame range from the recorded narration |
| Review | Check hand contact, identity, timing, caption-safe space and continuity |

Compare two generations with the same model, prompt, duration and framing. Use the original opening and ending frames in both. Add the intermediate contact pose in the second generation to test whether it improves the grip and turn. Cue each downloaded clip to the first usable frame before comparison. Keep each clip's source and settings in the production ledger.

## Run the local stick-engine scene

Add this entry to `window.SHOTS2` in the episode's `film/shots.js`. Replace `attention` with the measured segment ID from `timing.js`.

```js
{seg: 'attention', a: 0, b: 1, n: 'phonePause'}
```

The scene uses a locked camera and scales its action to the narration span. The hand pauses before contact, holds the phone joint through the turn, then releases it in the original position. Save a frame near 43% of the shot for the grip and near 56% for the turn if an external comparison is available. Review at playback speed before using the shot.

## Test the prop attachment on a second object

Use `{seg: 'attention', a: 0, b: 1, n: 'cupPause'}` to lift a cup, hold it, and set it back on the table. The scene uses the same hand attachment as `phonePause`. It uses the cup handle as the grip point and switches back to the fixed table position when the character releases it.

## Make the comparison

Export a 30 fps baseline excerpt with its approved soundtrack and clean picture. Use the same caption track on both versions during review. This example replaces five seconds beginning at frame 180 of the excerpt.

```bash
python3 .claude/skills/think-stick-engine/tools/compare_external_shot.py \
  baseline.mp4 higgsfield-shot.mp4 candidate.mp4 \
  --start-frame 180 --end-frame 330
```

Frame numbers are zero-based and the end is exclusive. The tool fits the candidate into the baseline dimensions, trims it to the assigned frame count and stream-copies the baseline audio. A candidate that is too short is rejected. The output preview re-encodes the picture. Record the result in the existing visual-treatment comparison and review both cuts at playback speed before selecting the shot for the pilot.
