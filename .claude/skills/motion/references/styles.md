# Picking the style

The style decides more about how a video lands than any single scene. Never default to one look;
identify the product, then pick the style that fits it. The user's own references always win
over this file.

## 1. Identify the product

Read the signals before deciding. Write the answers into `plan.md`.

| Question | Where to look |
|---|---|
| **Category** — what kind of product is it? | the site's headline and meta description, README, `package.json` / app-store category, pricing page |
| **Audience** — developers, businesses, consumers, students, a niche? | who the copy talks to ("your team", "your code", "you"), the call to action |
| **Personality** — playful, serious, premium, technical, loud, calm? | the brand's colours, fonts, illustrations, how jokey the copy is |
| **Assets** — what real material exists? | a UI (screens, components), product photos, data or numbers, a logo, code, a voice or track |
| **Platform** — where will it play? | the user's ask; otherwise the category default below |

## 2. Map it to a style

Start from the category row, then apply the modifiers in step 3.

| Category | First choice | Runner-up | Why |
|---|---|---|---|
| Developer tool, API, CLI, library | **Code showcase** | Dark-grid kinetic | developers trust seeing the real code and output |
| B2B SaaS, productivity, HR, CRM | **SaaS UI promo** | Minimal premium | buyers want to see the product doing the job |
| AI product or model | **3D and generative** | Dark-grid kinetic | the "how is this possible" feeling is the hook |
| Consumer app (social, utility, lifestyle) | **Device mockup** | Bold kinetic | people picture it on their own phone |
| Fintech, analytics, anything with numbers | **Data motion** | SaaS UI promo | the number *is* the story |
| Music, audio, podcasts, entertainment | **Audio-reactive generative** | Bold kinetic | the visuals should move with the sound |
| Physical product, e-commerce | **Product hero** (needs photos) | Swiss editorial | the object is the star; without photos fall back to editorial type |
| Luxury, fashion, beauty | **Minimal premium** | Swiss editorial | restraint signals price |
| Food, cafe, local business, events | **Warm editorial** | Bold kinetic | appetite and atmosphere, human tone |
| Education, edtech, courses | **Friendly explainer** | Device mockup | show the learning moment, keep it approachable |
| Gaming, esports | **Retro or chaotic** | 3D and generative | energy and genre cues |
| Health, wellness, mental health | **Calm minimal** | Warm editorial | trust and calm, nothing jumpy |
| Nonprofit, cause, public service | **Swiss editorial** | Data motion | big honest statements, real figures |
| Personal brand, portfolio, showreel | **Mixed: a new style per scene** | Bold kinetic | show range and confidence |

## 3. Modifiers

Apply in this order; a later one beats an earlier one.

1. **Assets.** No UI → no SaaS UI promo or device mockup. No photos → no product hero. No real
   numbers → no data motion. Pick the next row's style instead of inventing the missing thing.
2. **Personality.** A playful brand in a serious category (a jokey fintech) gets springier
   motion, brighter accents and humour; a serious brand in a playful category gets calmer pacing.
   Always use the brand's own colours and fonts on top of the style.
3. **Platform.** TikTok, Reels and Shorts: vertical, faster (cuts every 1–2 s), burned-in
   captions, hook in 1 s. LinkedIn and X: landscape, can breathe. Website hero: loopable, no
   text that ages.
4. **Mixing.** Mix styles freely — a different style per scene is often what makes a video
   feel rich (3D wave → counter → huge type → UI cards → code). What holds a mix together is
   everything *around* the styles, so keep these fixed across every scene:
   - **one palette and one accent** (the brand's), even when the backgrounds change;
   - **one type family**;
   - **one tempo**: cuts land on the same beat grid;
   - **a carry-over at every cut**: a shape, colour, word or object leaves one scene and enters
     the next, so a style change reads as one move, not a new video.

   How much to mix depends on the job. Showreels, "look what this can do" reels and launch
   videos: switch style most scenes. A promo for one product: let one style carry the product
   scenes and use other styles for the hook, the proof beat and the ending. Calm or premium
   brands: two or three styles at most, slow transitions.
5. **References.** If the user shares videos, make contact sheets and find the cut points
   (`ffmpeg -vf "select='gt(scene,0.3)',showinfo"`). Match their pacing, palette, type and motion,
   but never their handles, logos or captions.

## 4. Say what you chose

Before building, tell the user in three lines: the style you picked and why (one sentence tying
it to what you found), and the two runners-up. If the request was vague and the user seems
unsure, render one still per candidate from quick draft pages (`render.mjs --stills`) and show
the contact sheets side by side, so they pick by looking rather than by name.

## The styles

| Style | Look | Motion and pace | Engine notes |
|---|---|---|---|
| **Code showcase** | dark editor or terminal, syntax colours, one accent | code types in, then the result appears; cuts on run | real code from the source, monospace font |
| **Dark-grid kinetic** | near-black, faint grid, white type, one hot accent (often orange) | lines draw on, words slide in, wipes; medium–fast | SVG lines, `stroke-dashoffset` draw-ons |
| **SaaS UI promo** | light or cream background, real UI cards, soft shadows, one accent | cursor travels and clicks, cards slide and stack, quick cuts every 2–4 s | reuse the product's components and CSS |
| **3D and generative** | depth, glow, waves, terrain, particles, fog | slow camera orbits, things assembling from particles | Three.js / WebGL in the page; seed every random |
| **Device mockup** | the app inside a phone or laptop frame, often tilted in 3D | screens swipe and scroll, device turns between features | CSS 3D transforms on a frame; real screenshots or components inside |
| **Data motion** | big numerals, charts, one highlight colour | counters run, bars grow, the key value gets called out | tabular figures; numbers read from the data, never retyped |
| **Audio-reactive generative** | waveforms, rings, shapes pulsing | everything locked to the beat and the waveform | analyse the track offline and drive visuals from it |
| **Product hero** | the product photo, big, with clean type | slow push-ins, reveals, hard cut to the price or CTA | needs real photos; cut them out and light them with gradients |
| **Minimal premium** | lots of empty space, one serif or thin sans, muted palette | slow fades and long holds, gentle springs | fewer elements, more time |
| **Swiss editorial** | huge bold type on a grid, flat colour blocks | hard cuts, words slam in, colour flips | one family, extreme size contrast |
| **Bold kinetic** | type as the whole visual, high contrast | words split, scale, stack; fast, rhythmic | stagger letters and words; cut on beats |
| **Warm editorial** | warm tones, textured paper, friendly rounded type | soft slides, hand-drawn underlines and doodles | SVG strokes, a grain overlay |
| **Friendly explainer** | simple shapes and icons, bright but soft colours | step-by-step builds, diagrams drawing themselves | one visual metaphor built on scene by scene |
| **Retro or chaotic** | pixel art, CRT scanlines, VHS, or all-caps flashes | glitches, zoom cuts, under-2 s scenes | scanline and noise overlays, seeded glitches |
| **Calm minimal** | soft gradients, rounded shapes, lots of air | breathing loops, very slow transitions | long easing, no shakes or flashes |

Any style can be shown "filmed off a laptop": render the flat video first, then place it on a
laptop screen in a dark scene with CSS 3D, a desk reflection and a caption. Offer this when the
user wants the look of a phone filming a screen.
