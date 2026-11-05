# Dan Koe Style

Inspired by the minimalist line-and-dot visuals that thinker-creator Dan Koe made popular: white lines, small dots, black space, big ideas.

## Must have
- Pure black background, thin white lines (2-3 px at 1080 wide), small solid white dots at the joints (5-7 px).
- Strictly 2D and monochrome. No colour, no gradients, no 3D, no textures.
- Lots of empty space. One idea per frame.
- Objects are drawn as connected points, like a constellation: sample the object's outline into 25-40 points, dot each one, join them in order. It must still clearly look like the object.

## Make any script work
- Ideas (focus, money, time, habits, growth) become relationships between 2-3 simple elements: a dot travelling a path, a line splitting in two, a circle growing around a point.
- Use orbits, circles and sacred-geometry shapes only when they say something about the idea, not as decoration.
- People are a few gesture lines plus a head dot: a clear pose and action.

## Motion
Quiet and precise: lines draw on, dots travel along lines, slow zooms, pauses to let a thought land. The contrast comes from structure, not effects.

## Text
Small white sans, lowercase or sentence case, one short thought at a time.

## Avoid
Colour accents, starfields that bury the subject, pseudo-3D rotations, the same geometry on every topic, lines too thin for a phone.

## Code starter
```js
// constellation of an outline pts[] revealed to fraction k
function constellation(pts, k) {
  const n = Math.floor(pts.length * k);
  ctx.strokeStyle = "#fff"; ctx.lineWidth = 2.4; ctx.beginPath();
  for (let i = 0; i < n; i++) i ? ctx.lineTo(...pts[i]) : ctx.moveTo(...pts[i]);
  ctx.stroke(); ctx.fillStyle = "#fff";
  for (let i = 0; i < n; i++) { ctx.beginPath(); ctx.arc(pts[i][0], pts[i][1], 4.5, 0, 7); ctx.fill(); }
}
```
