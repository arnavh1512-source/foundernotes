# Flat Vector

Clean editorial illustration: big simple shapes, flat colour, no outlines.

## Must have
- Shapes, not lines: every object is 2-3 flat colour planes (shadow, base, light) cut cleanly. No outlines, no gradients pretending to be flat.
- A tight palette of 6-8 colours chosen for the story, with ONE accent colour that marks the focus.
- Strong hierarchy and generous empty space. Crisp geometry for tech and buildings, softer curves for people and nature.
- Optional very light grain (3-5%) to unify the layers.

## Make any script work
- Real objects, simplified: the actual product, the actual city, a recognisable person (hair, clothes, pose), all in flat shapes.
- Explanations: clean diagrams, UI mock-ups, icons that morph from one to the next.
- Vary the shots: a wide scene, a close-up detail, a transformation, a step-by-step.

## Motion
Smooth eased moves, masked reveals (shapes slide out from behind edges), shape morphs, parallax layers, a gentle camera drift. Calm and confident.

## Text
Bold modern sans (Inter, Poppins or similar), few words, aligned to a grid.

## Avoid
Black outlines everywhere, glossy highlights, generic stock-illustration people, clutter, bouncing for no reason.

## Code starter
```js
// a shape with a clean cut shadow plane: base colour, then a darker band clipped to the shape
function flat(path, base, shade, cutX, cutAngle = 0.35) {
  ctx.fillStyle = base; ctx.fill(path);
  ctx.save(); ctx.clip(path); ctx.fillStyle = shade;
  ctx.beginPath(); ctx.moveTo(cutX, -H); ctx.lineTo(cutX + Math.tan(cutAngle) * 2 * H, H); ctx.lineTo(W * 2, H); ctx.lineTo(W * 2, -H); ctx.fill();
  ctx.restore();
}
// Path2D shapes + translate/scale per layer give clean parallax: far layers move ×0.3, near layers ×1.2
```
