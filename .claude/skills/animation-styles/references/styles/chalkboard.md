# Chalkboard

A teacher's board: chalk lines draw themselves while the idea is explained.

## Must have
- A real board surface: dark green (#2c4436 → #22362b) or slate black, with faint eraser smears.
- Chalk lines, not vector lines: each stroke is 2-3 slightly offset passes with uneven width and gaps where the chalk skips. A grain mask breaks up the edges.
- Things are DRAWN in, stroke by stroke, in the order a person would draw them. Then circled, underlined, pointed at with arrows.
- Shading is hatching (diagonal strokes), never smooth fills.
- Mostly off-white chalk, plus 1-2 accent chalks (yellow, pink, sky blue) for the key idea.

## Make any script work
- Explanations: labelled diagrams, simple formulas, arrows showing cause and effect (FORCE →, LIFT ↑).
- Stories: quick sketched scenes in sequence, like a teacher drawing a story while telling it.
- Objects are drawn recognisably (a real paper plane, a real bridge), not as stick symbols.
- A wooden frame and chalk tray are optional; skip them on small vertical frames.

## Motion
Line draw-on (reveal along the path), a little boil (the line jitters between 2-3 versions, changing every 3 frames), a dust puff when a line ends, an eraser wipe to clear for the next idea.

## Text
Handwritten chalk lettering (a handwriting font with the same grain), short labels, big enough to read.

## Avoid
Perfect geometric curves, smooth gradients, constant scribbling with no meaning, unreadable thin text.

## Code starter
```js
// a chalk stroke along points pts[] revealed up to fraction k
function chalk(pts, k, col = "#f1efe6", w = 6, seed = 1) {
  const n = Math.max(2, Math.floor(pts.length * k));
  for (let pass = 0; pass < 3; pass++) {
    ctx.beginPath(); ctx.strokeStyle = col; ctx.globalAlpha = pass ? .4 : .85; ctx.lineWidth = w * (pass ? .55 : 1); ctx.lineCap = "round";
    for (let i = 0; i < n; i++) { const j = (rand(seed * 97 + i * 7 + pass) - .5) * 3; const [x, y] = pts[i]; i ? ctx.lineTo(x + j, y - j) : ctx.moveTo(x + j, y); }
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
}
// grain: pre-build a canvas of tiny transparent specks once, then draw it over the chalk layer with "destination-out"
```
