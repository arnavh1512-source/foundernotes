# Higgsfield shot pilot for Think!

Use the existing 20–40 second narrated treatment comparison. Test one character or environment shot first. Keep the approved narration, captions and duration identical across versions.

## What the investigation established

- REA 6.10.1 statically parsed the public Cinema Studio guide's 222-byte module entry point as inert JavaScript. The evidence covers the page loader only. Live browser capture could not reach the local DevTools port, so there is no captured generation session or server-side model evidence. REA evidence ID: `ev_a96e0cc230f10311ff5e2c41d6382d09e4a5d202148a4654e1de6169071a5271`.
- Higgsfield's public guides describe locking a storyboard and using reusable character and location references, then choosing the framing and one camera move per shot. [Storyboard workflow](https://higgsfield.ai/blog/script-to-ai-storyboard-shot-list) · [Cinema Studio controls](https://higgsfield.ai/blog/cinema-studio-4-0-complete-guide)
- Its documented Kling image-to-video workflow accepts an opening image, reference images and ending frames. [API reference](https://open.higgsfield.ai/models/kling-video/v4.0/image-to-video/api-reference)

## Copy into the storyboard for the candidate shot

| Field | Example |
| --- | --- |
| Visual job | Make a deliberate pause before acting readable |
| Approved references | Think! character sheet and existing study background |
| Opening pose | Medium three-quarter shot. Student's hand rests on desk, phone face up |
| Action and timing | Phone buzzes. Hand reaches, pauses, then grips and turns it face down |
| Ending pose | Phone face down in the same spot. Student's eyes return to the page |
| Camera | Locked medium shot. Hands, phone and face stay readable |
| Continuity | Same silhouette, desk layout, light and palette at both cuts |
| Duration | Use the exact in/out frame range from the recorded narration |
| Review | Check hand contact, identity, timing, caption-safe space and continuity |

Generate the candidate from the original opening and ending frames. Cue the downloaded clip to the first usable frame before comparison. Keep its source and settings in the production ledger.

## Make the comparison

Export a 30 fps baseline excerpt with its approved soundtrack and clean picture. Use the same caption track on both versions during review. This example replaces five seconds beginning at frame 180 of the excerpt.

```bash
python3 .claude/skills/think-stick-engine/tools/compare_external_shot.py \
  baseline.mp4 higgsfield-shot.mp4 candidate.mp4 \
  --start-frame 180 --end-frame 330
```

Frame numbers are zero-based and the end is exclusive. The tool fits the candidate into the baseline dimensions, trims it to the assigned frame count and stream-copies the baseline audio. A candidate that is too short is rejected. The output preview re-encodes the picture. Record the result in the existing visual-treatment comparison and review both cuts at playback speed before selecting the shot for the pilot.
