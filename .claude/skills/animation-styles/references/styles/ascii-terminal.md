# ASCII Terminal
*(adapted from @janustiu's tutorial)*

Everything is rendered only with monospace characters, like a 3D demo running inside a terminal.

## Must have
- **The method:** render 3D geometry yourself, sample brightness into a character grid (90–120 columns), and draw each cell as a glyph from the ramp " .:-=+*#%@".
- **Nothing outside the grid:** no pixels outside the glyph grid.
- **Look:** a pure black terminal, phosphor green (#33FF66) with a faint glow and the brightest characters whiter, a subtle CRT curve, scanlines and flicker.
- **Opening:** a blinking cursor types the command that "renders" the film.
## Motion
Smooth 3D rotation inside a rigid character grid. Glitches last 2–3 frames (rows shift and cells flip, then lock back). Objects can shatter into falling characters that rebuild into the payoff word.
## Sound
Minimal techno around 124 BPM, mechanical key clicks, CRT hum, data chirps on glitches, and a deep hit when the word locks.
## If it goes wrong
If the object is blurry, use a denser grid of about 120 columns.
