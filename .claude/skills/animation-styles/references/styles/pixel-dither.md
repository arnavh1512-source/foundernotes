# Pixel Dither (handheld-console look)
*(adapted from @janustiu's tutorial; see also pixel-art.md)*

A smooth high-resolution object collapses into pixels on the beat; from then on, the resolution itself is the effect.

## Must have
- **Resolution:** render pixel scenes at a tiny size (135×240 for 9:16, 240×135 for 16:9), then upscale with nearest-neighbour. No anti-aliasing.
- **Shading:** ordered Bayer dithering for all shading, and a strict 4-colour palette (e.g. #0F380F #306230 #8BAC0F #9BBC0F).
- **Overlays:** a thin scanline overlay at low opacity, plus a faint LCD pixel grid.
- **The collapse:** resolution steps down on the beat, e.g. 1080 → 270 → 68 → native.
## Motion
Stepped and chunky, animated on twos (a 12 fps feel). Snaps are instant and holds are short. Bounces kick up 2×2-pixel dust, and glitches are horizontal pixel-sort tears.
## Sound
Chiptune around 140 BPM from square/triangle waves and noise, a blip on each resolution step, a boing on each bounce, and a bitcrushed burst on glitches.
## If it goes wrong
This is the easiest style; it usually works in one or two rounds.
