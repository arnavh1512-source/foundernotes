# Ink & Gold kit (Hunting Titles house style)

A time-driven SVG scene kit for the motion skill's render contract (`window.MOTION`, `window.seek(t)`).
Copy this folder into `studio-output/<slug>/film/` to start a film.

- `kit.js`: stage, camera with parallax, light (glow, beam, dust), gold thread, type, cards, props,
  the `K.Hunter` character rig (proportioned legs, hand anchors, poses, blink/anticipate/settle),
  p5.brush painted plates, vector-law seams, and the scene runner (`K.scene`).
- `kit-loop.js`: loop/spiral thread paths, `K.threadGrey`, calendar `K.page`, zero-based `K.bars`,
  the `K.qmark` pin, `K.floor`, `K.bow`, and **backdrops**.
- **Backdrops (owner rule: change backgrounds regularly).** `K.backdrop(S, name)` has 11 presets: night,
  teal, paper, dawn, chalk, clinic, ember, violet, fog, blueprint and sunrise. Each sets a matching floor,
  and returns type colours: use `.text`/`.sub`, which are dark on paper and sunrise.
  - No two adjacent scenes share a backdrop, and use at least 6 per film.
  - Set the per-film map in `K.FILM_BACKDROPS`.
- `make_timing.py`: writes `timing.js` (scene cuts + segment times + seams) from narration timings, `scenes.json` and `seams.json`.
- `still.mjs`: `node still.mjs /abs/scene.html /abs/out-prefix 1 4 8` writes stills for review.
- `example-sc01-threads.html`: an approved reference scene.
- `STYLE.md` / `CRAFT.md`: palette, light, type and craft rules.

## Licences
- Fonts: Lora, Instrument Sans and Caveat (SIL OFL 1.1, licence files included).
- `vendor/brush.js`: p5.brush (MIT).
- The kit code is original to this channel.
