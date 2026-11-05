# PS2 Style

An early-2000s console cutscene: chunky low-poly 3D, soft low resolution, simple light.

## Must have
- Real 3D (three.js) with LOW polygon counts: boxes, 5-8-sided cylinders, flat-shaded faces (`flatShading: true`).
- Render small, then scale up with smoothing ON: about a quarter of the output (270x480 for 9:16). That soft, slightly blurry upscale IS the look.
- Simple lighting: strong ambient + one directional light, Lambert materials, round dark "blob" shadows under characters instead of real shadows.
- Small, chunky textures (16-64 px, drawn on a canvas), nearest filtering, slight colour banding (quantise colours, a little dither).
- Distance fog that fades into the sky colour.

## Make any script work
- Characters: blocky bodies, a painted face texture, chunky hair, stiff simple poses. Give each one a distinct outfit colour.
- Places: build the script's real setting (a street, an office, a beach) from boxes and planes with painted textures.
- Keep subjects recognisable; low-poly is a constraint, not an excuse for the wrong object.

## Motion
Cutscene acting: slightly mechanical walks, simple keyframed gestures, a slow camera push or a fixed angle with a cut. Small low-poly particles.

## Text
Game-style subtitles: white with a dark outline, bottom-centre inside the safe area.

## Avoid
Glossy modern materials, high-poly smooth meshes, real-time shadows, sharp pixel art (that's a different style).

## Code starter
```js
const LR = { w: Math.round(W / 4), h: Math.round(H / 4) };
const gl = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true }); gl.setPixelRatio(1); gl.setSize(LR.w, LR.h, false);
const mat = c => new THREE.MeshLambertMaterial({ color: c, flatShading: true });
// in draw(t): gl.render(scene, camera); ctx.imageSmoothingEnabled = true; ctx.drawImage(gl.domElement, 0, 0, W, H);
```
