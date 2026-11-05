# Comic Art

A printed comic page that moves: thick ink, flat bold colours, halftone dots, big sound words.

## Must have
- Heavy black ink outlines (8-12 px at 1080 wide), slightly uneven like a brush pen.
- Flat print colours: red, blue, yellow, cream, black (adapt to the story, keep it bold).
- Shading with Ben-Day dots (a dot grid, bigger dots = darker), never smooth gradients.
- A cream paper tone and a slight print misregistration (colour offset by 2-3 px) for texture.

## Make any script work
- Use panels when comparing or showing steps (before/after, problem/solution). A single full-frame panel is fine for a big action moment.
- Sound words (WHOOSH, BOOM, ZAP) and speech bubbles are storytelling tools; use them on real moments, not every shot.
- Speed lines and starbursts mark motion and impact.
- People: expressive faces, strong poses held for a beat.

## Motion
Snappy: pop-in with a small overshoot, held poses, hard cuts, panel slides and wipes, a camera shake on impact. Motion lines show speed instead of motion blur.

## Text
Bold comic lettering in caption boxes or bubbles, short.

## Avoid
Thin outlines, soft gradients, the same yellow starburst in every shot, invented dialogue the user didn't write.

## Code starter
```js
// halftone fill clipped to the current path
function halftone(col, step = 22, maxR = 7, dir = [0.6, 0.8]) {
  ctx.save(); ctx.clip(); ctx.fillStyle = col;
  for (let y = 0; y < H + step; y += step) for (let x = (y / step) % 2 ? step / 2 : 0; x < W + step; x += step) {
    const k = clamp((x * dir[0] + y * dir[1]) / (W * dir[0] + H * dir[1])); ctx.beginPath(); ctx.arc(x, y, maxR * k, 0, 7); ctx.fill();
  }
  ctx.restore();
}
const ink = (w = 10) => { ctx.lineWidth = w; ctx.strokeStyle = "#111"; ctx.lineJoin = "round"; ctx.stroke(); };
```
