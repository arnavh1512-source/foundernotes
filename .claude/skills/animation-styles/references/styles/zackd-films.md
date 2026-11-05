# ZackD Films Style

Inspired by the soft 3D explainer shorts that ZackD Films made famous: smooth clay-like 3D, friendly shapes, quick "here's how it works" shots.

## Must have
- three.js with soft rounded forms: generous bevels, capsules and spheres where the real object allows it, smooth matte-to-satin "vinyl clay" surfaces (`MeshPhysicalMaterial`, roughness ~0.45, clearcoat ~0.3).
- Soft, bright, readable light: a big warm-white key, a cool fill, broad soft shadows. Clean, simple backgrounds.
- Recognisable proportions: rounder and friendlier, but a heart is still a heart and a plane is still a plane.
- Characters, if any: simple rounded bodies, big expressive eyes, clear gestures.

## Make any script work
- Turn every claim into a little demonstration: a cutaway of the inside, a close-up of the mechanism, a before/after, a satisfying reveal.
- Camera grammar: a wide shot to set the scene, then a close-up on what's being explained, then the payoff.
- The setting follows the script (a bedroom, a lab, a jungle, inside a body), always with the same soft surface treatment.

## Motion
Smooth and purposeful: objects glide, squash a little on landing, settle softly. Quick clean cuts between angles. Gentle handheld drift on the camera.

## Text
A few words at a time in a bold, friendly sans, placed where it never covers the mechanism.

## Avoid
Featureless blobs instead of real objects, heavy blur, harsh shadows, the same green hills every time.

## Code starter
```js
const clay = c => new THREE.MeshPhysicalMaterial({ color: c, roughness: .45, clearcoat: .3, clearcoatRoughness: .5 });
// rounded box: extrude a rounded rectangle with a big bevel
function rbox(w, h, d, r = .25, col) {
  const s = new THREE.Shape(), x = -w / 2 + r, y = -h / 2 + r, iw = w - 2 * r, ih = h - 2 * r;
  s.moveTo(x, y - r); s.lineTo(x + iw, y - r); s.quadraticCurveTo(x + iw + r, y - r, x + iw + r, y); s.lineTo(x + iw + r, y + ih);
  s.quadraticCurveTo(x + iw + r, y + ih + r, x + iw, y + ih + r); s.lineTo(x, y + ih + r); s.quadraticCurveTo(x - r, y + ih + r, x - r, y + ih); s.lineTo(x - r, y); s.quadraticCurveTo(x - r, y - r, x, y - r);
  const g = new THREE.ExtrudeGeometry(s, { depth: d - 2 * r, bevelEnabled: true, bevelSize: r, bevelThickness: r, bevelSegments: 6, curveSegments: 10 });
  g.center(); return new THREE.Mesh(g, clay(col));
}
```
