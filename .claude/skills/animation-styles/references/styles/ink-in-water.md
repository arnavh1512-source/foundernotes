# Ink in Water
*(adapted from @janustiu's tutorial)*

A particle simulation of ink dropped into water: it blooms in slow motion, then condenses into a word or shape.

## Must have
- **The simulation:** about 20–30k particles with curl-noise turbulence, slight gravity and drag.
- **The rendering:** additive blending at low opacity, so dense areas build rich colour. Seeded randomness, so every render is identical.
- **The letter phase:** blend each particle toward a target point sampled from the word's shape.
- **Look:** clean white water (#FAFAFA) with subtle caustics; deep indigo (#1B1F6B) and magenta (#C2185B) inks with a violet mix; no hard edges.
## Motion
Slow motion throughout, organic and never linear. Letters form gradually, never snapped.
## Sound
Cinematic ambient piano with long reverb and no drums, a deep underwater plunk per drop, low rumbles as the ink blooms, and a rising swell as the letters form.
## If it goes wrong
This is the heaviest render. If the word doesn't read, settle more particles into the letters.
