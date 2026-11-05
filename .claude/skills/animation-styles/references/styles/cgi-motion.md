# CGI Motion

Cinematic 3D, like a game engine trailer: real materials, real light, real camera moves.

## Must have
- three.js with physical materials (`MeshPhysicalMaterial` / `MeshStandardMaterial`): metal looks like metal, paper like paper, glass like glass.
- Lighting designed like a film set: a key light, a fill, a rim light that separates the subject from the background. ACES tone mapping. Soft shadows.
- Depth: foreground, subject and background at different distances; atmospheric haze for scale.
- A little bloom on highlights (keep it gentle), a slight vignette.

## Make any script work
- Pick the setting the script implies (a lab, a stadium, a street at night, open sky, an ocean at sunrise) and give it believable light for that time of day.
- Build the named objects with the right silhouette first (a sports car is low and wide, a jet has swept wings), then detail.
- Without detailed models, keep characters stylised rather than faking photoreal humans.

## Motion
Real physics feel: arcs, inertia, banking into turns. Camera: slow push-ins, tracking shots alongside moving subjects, a low hero angle for big moments. Vary the shots; don't use one angle for everything.

## Text
Cinematic: wide-tracked bold sans, short, appears with the beat.

## Avoid
Plastic-looking everything, blown-out bloom, unreadable dark scenes, a mannequin where a character matters.

## Code starter
```js
const gl = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true }); gl.setPixelRatio(1); gl.setSize(W, H, false);
gl.toneMapping = THREE.ACESFilmicToneMapping; gl.toneMappingExposure = 1.1; gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
const key = new THREE.DirectionalLight(0xfff1dc, 2.2); key.castShadow = true;
const rim = new THREE.DirectionalLight(0x9fc4ff, 1.2);
scene.add(new THREE.HemisphereLight(0xbfd8ff, 0x203040, .6), key, rim);
// cheap reflection on water: render a mirrored copy of the subject below the surface at lower opacity
```
