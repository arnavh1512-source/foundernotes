# Lego Style

A toy-brick world, like a stop-motion brick film: everything is built from plastic bricks with studs.

## Must have
- Everything is made of bricks: buildings, ground, trees, vehicles, smoke, even water. Use a real grid: stud pitch 1, brick height 1.2, plate height 0.4, studs as short cylinders (radius 0.3, height 0.18).
- Glossy moulded plastic: `MeshPhysicalMaterial` with roughness ~0.3 and clearcoat ~0.6, soft studio light, slight seams between bricks.
- Bright toy colours that fit the story (red, yellow, blue, green, white, plus a few darker greys).
- Figures are your own design: blocky toy people with cylinder heads, simple faces, hinge arms and legs. Never copy a trademarked minifigure exactly, and never show real brand logos.

## Make any script work
- Pick brick builds that keep each object recognisable: a plane from plates and slopes, a tree from round plates, a city from stacked bricks with tile windows.
- Assembly ("snap together") is the signature move: use it when something gets built or appears, not on every shot.

## Motion
Stop-motion feel: step the animation on twos (update every 2 frames), pieces drop in and settle with a tiny bounce, figures move with stiff hinge joints. Smoke and splashes are clusters of round bricks.

## Text
Playful bold rounded type; a brick tile behind it if it needs contrast.

## Avoid
Smooth meshes with stud stickers, bricks passing through each other, floating studs, brand logos.

## Code starter
```js
const brickMat = c => new THREE.MeshPhysicalMaterial({ color: c, roughness: .3, clearcoat: .6, clearcoatRoughness: .2 });
function brick(w, d, h, col) {                  // w x d studs, h in plates (3 = one brick)
  const g = new THREE.Group(), m = brickMat(col);
  const b = new THREE.Mesh(new THREE.BoxGeometry(w - .02, h * .4, d - .02), m); b.position.y = h * .2; g.add(b);
  const stud = new THREE.CylinderGeometry(.3, .3, .18, 16);
  for (let i = 0; i < w; i++) for (let j = 0; j < d; j++) { const s = new THREE.Mesh(stud, m); s.position.set(i - (w - 1) / 2, h * .4 + .09, j - (d - 1) / 2); g.add(s); }
  return g;
}
// stop-motion: const ts = Math.floor(t * 12) / 12;  // animate with ts instead of t
```
