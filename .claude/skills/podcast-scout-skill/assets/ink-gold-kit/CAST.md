# Cast log (owner rule: new characters every video)

Every film gets its own cast. Before building, read this log and choose leads that differ from **every**
earlier lead in at least four of these six:
- skin tone;
- hair style (`wavy`, `crop`, `curly`, `bald`, `long`);
- facial hair (`none`, `stubble`, `full`, `moustache`);
- glasses;
- build (`0.9`–`1.15`);
- outfit colours.

Define the cast in the film's `kit-loop.js` (`K.DEFAULT_CAST` plus named casts passed as `{ colors: … }`),
render a cast sheet, and add a row here.

Rig options for `new K.Hunter(layer, { colors: {...} })`:
- colours: skin, skinDk, skinLt, hair, jacket, jacketDk, tee, pants, pantsDk, shoe;
- style: hairStyle, facialHair, glasses (true or a colour), build.

| Film | Character | Skin | Hair | Facial hair | Glasses | Build | Outfit |
|---|---|---|---|---|---|---|---|
| After the Win (2026-11) | the hunter (lead) | medium `#B9774F` | wavy | none | no | 1.0 | teal jacket, cream tee, charcoal jeans |
| One Year, Twenty Times (2026-11) | Climber | deep `#7B4A2E` | crop | none | yes | 0.94 | navy jacket, olive trousers |
| One Year, Twenty Times (2026-11) | Looper | light-olive `#D7A47C` | curly | full beard | no | 1.1 | rust jacket, grey trousers |
