# Glow Sketch

Drawings made of tiny glowing dots on near-black, like a blueprint traced in light.

## Must have
- Background near black (#07070c), with a soft vignette.
- Contours are DOTTED: round dots spaced along the path (about 10-14 px apart at 1080 wide), with a faint solid guide line underneath at ~30% opacity.
- A soft glow around the lines (a blurred copy underneath, kept subtle).
- One warm accent (gold #ffc85a by default) for whatever matters most in the beat. Everything else stays pale white-blue.
- Big empty dark areas. Light is precious.

## Make any script work
- Draw the real outline of each subject (a car, a heart, a city skyline, a phone) from its distinctive edges, plus a few interior lines.
- Depth: far objects get smaller, dimmer, sparser dots. Near objects get brighter, denser dots.
- The story's key object gets the gold light; when the focus changes, the gold moves.

## Motion
Slow tracing (dots appear along the path in order), gentle drift and parallax, a single soft pulse or ring on an important moment. Calm and elegant.

## Text
A clean thin sans in pale white, one gold word for emphasis.

## Avoid
Solid neon tubes, glow everywhere, muddy purple contrast, random orbs that don't belong to the story.

## Code starter
```js
// dots along a polyline, revealed to fraction k
function dotted(pts, k, col = "rgba(220,230,255,.9)", gap = 12, r = 2.6) {
  let acc = 0, total = 0; const L = [];
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i-1][0], pts[i][1] - pts[i-1][1]); L.push(d); total += d; }
  ctx.fillStyle = col; ctx.shadowColor = col; ctx.shadowBlur = 10;
  for (let s = 0; s < total * k; s += gap) {
    let i = 0, a = s; while (i < L.length && a > L[i]) { a -= L[i]; i++; } if (i >= L.length) break;
    const f = a / L[i], x = lerp(pts[i][0], pts[i+1][0], f), y = lerp(pts[i][1], pts[i+1][1], f);
    ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
  }
  ctx.shadowBlur = 0;
}
```
