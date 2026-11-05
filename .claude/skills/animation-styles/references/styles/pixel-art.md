# Pixel Art

The look of a 16-bit console game: every shape is made of real, square pixels.

## Must have
- Draw on a small canvas, then scale it up with smoothing OFF. 9:16 at 1080x1920 → draw at 180x320 and scale x6. 16:9 → 320x180. 1:1 → 180x180. Never draw smooth art and add a "pixel filter" on top.
- Integer positions only (Math.round everything). Sprites move in whole pixels and may step every 2 frames for that game feel.
- 1-pixel dark outline around characters and key props. 3-4 shades per material (shadow, base, light, highlight).
- A limited palette (16-24 colours) chosen for this story: sunset rooftops, a green forest, a blue lab, whatever the script needs.
- Gradients become stepped bands, joined with a 4x4 ordered (Bayer) dither.

## Make any script work
- People: readable at 16-24 px tall with clear hair, clothes and one prop. Faces are 2-3 pixels; expression comes from pose.
- Places: tile-based, with 2-3 parallax layers (far skyline, mid buildings, near rooftops).
- Apps and products: rebuild the actual screen as a pixel mock-up, not a generic gadget.
- Abstract ideas: game language works well (a power-up for a skill, a health bar for energy, a level map for a plan), but only when it fits.

## Motion
Stepped, snappy, with whole-pixel squash and stretch. Dust puffs and sparkles are 1-2 px squares. Camera moves in whole pixels.

## Text
A pixel font drawn at the low resolution (or a 5x7 bitmap font you draw yourself), with a 1-px dark outline. 2-5 words at a time.

## Avoid
Blurry scaling, half-pixel positions, smooth gradients, anti-aliased lines, and tiny characters nobody can read.

## Code starter
```js
const S = 6, LW = W / S, LH = H / S;                 // low-res size
const low = document.createElement("canvas"); low.width = LW; low.height = LH;
const g = low.getContext("2d"); g.imageSmoothingEnabled = false;
const px = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(Math.round(x), Math.round(y), w, h); };
const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
const dither = (x, y, k) => k * 16 > BAYER[(y & 3) * 4 + (x & 3)];   // band blend
// in draw(t): draw everything into g, then:
ctx.imageSmoothingEnabled = false; ctx.drawImage(low, 0, 0, W, H);
```
