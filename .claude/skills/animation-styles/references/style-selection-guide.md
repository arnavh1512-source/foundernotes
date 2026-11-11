# Style selection guide for Founder Notes

Written 2026-11-11 after reading all 17 native style files and the five external catalogs, and after studying two owner-supplied reference videos (see `podcast-scout-skill/references/reference-video-learnings.md`).

**What this is:** an editorial judgement on fit, to shorten the choice for the next video.
**What this is not:** audience data. `production_ledger.json` has no finished videos yet, so nothing here is measured against Founder Notes viewers. Only one look has been render-tested in this studio so far (the hand-drawn character look used for *choking under pressure*). Replace opinions here with observed retention once videos are published.

## How to choose (in this order)

1. **What must the viewer see change?** A person's feeling, a mechanism, a number, or an abstract idea. This decides the family below.
2. **Is there a human in the story?** Founder Notes topics are mostly about a person's behaviour. The two reference videos (3M+ views each) are character-led for almost their whole length, with a new picture about every three seconds.
3. **Can it hold for 8 minutes?** Some looks are a strong 20 seconds and tiring at 8 minutes. Use those for a chapter or an insert.
4. **Then** compare 2–3 real treatments on the same 20–40 s of narration, as the channel rule requires.

## The 17 native styles

Fit = fit for a full 8-minute Founder Notes psychology or self-improvement explainer. Cost = effort and render risk with the tools installed here.

| Style | What it shows best | Fit for a full video | Better used as | Cost |
|---|---|---|---|---|
| `chalkboard` | Step-by-step explanation, diagrams drawn as a teacher would | **High** | Main look for "how it works" topics | Low (2D canvas) |
| `flat-vector` | Clean scenes, people, UI, step-by-step | **High** | Main look for business and habit topics | Low |
| `comic-art` | Emotion, conflict, before/after panels | **High** for story-led topics | Main look for case stories; panels for comparisons | Low to medium |
| `risograph-cutout` | Warm handmade scenes, simple characters | **Medium to high** | Main look for gentle, personal topics | Low |
| `zackd-films` | Physical "here is how it works" in soft 3D | **Medium to high** for body/brain mechanisms | Mechanism chapters | High (three.js, slower renders) |
| `one-line-graph` | One idea turning into the next; data that becomes a picture | **Medium** | A chapter on a trend or a turning point | Low |
| `dan-koe` | Abstract ideas as dots and lines on black | **Medium** | Philosophy and focus topics; no faces, so emotion is weak | Low |
| `glow-sketch` | Elegant outlines, one gold focus | **Medium** | Night, calm, reflective chapters | Low |
| `renaissance-codex` | An invention or mechanism drawn then brought to life | **Medium** | History-of-an-idea chapters | Medium |
| `cgi-motion` | Real objects, scale, drama | **Low to medium** | Cold open or a single hero shot | High |
| `pixel-art` | Game-like scenes, nostalgia | **Low to medium** | Topics about games, habits as "levels" | Medium |
| `lego` | Toy-brick worlds | **Low to medium** | A playful analogy chapter | High |
| `ps2` | Early-2000s game cutscene | **Low** | A nostalgia insert | High |
| `ink-in-water` | A word or shape forming from ink | **Low** | Title or chapter card only | Medium |
| `ascii-terminal` | Tech and code mood | **Low** | A tech-topic insert | Medium |
| `pixel-dither` | Resolution as an effect | **Low** | A transition or sting | Low |
| `one-ball-showreel` | A showreel of motion techniques | **Low** | Channel trailer or intro sting | Medium |

Why the low ratings: these looks either cannot show a readable human face (ink, ASCII, dither, showreel) or their novelty wears off well before eight minutes. They are still useful for 5–20 seconds.

## The character-led look (not one of the 17)

The channel's preferred starting direction for psychology explainers is original, simple, expressive illustrated characters. It has no style file of its own yet. *Choking under pressure* uses it: a dark slate ground, cream line, warm opaque skin, coral, cyan and green accents, gold for key numbers.

Rules that came out of that build, with the vendored stickman craft rules (`.claude/skills/stickman-video-director/`):

- Slender figure, about four heads tall, with a face large enough to read on a phone.
- Brows, eyes and mouth all change with the emotion; the body leans with it.
- Hands touch the prop they use.
- Something in the main picture moves at least every 2.5 seconds. A zoom or a typed label does not count.
- A dark ground needs opaque light skin and dark face features, or faces disappear.
- Sound effects on actions (a tick, a miss, a heartbeat), not on every cut.

**Suggested default for the next psychology video:** this look, with `chalkboard` or `flat-vector` for mechanism chapters. Worth writing up as an eighteenth style file once the owner has approved a finished video in it.

## External catalogs (575 entries)

| Catalog | Entries | Use it for | Limits |
|---|---|---|---|
| `anidoodle` | 32 | Hand-made media looks: crayon, charcoal, coloured pencil | Recipes, not a renderer |
| `claude-drawing` | 83 | Illustration styles for single drawn scenes | Entries are in Chinese |
| `huashu` | 53 | Art-history looks and nine explainer grammars | Entries are in Chinese; no characters included |
| `code-animation-prompts` | 341 | Kinetic type and abstract code animation | Mostly text effects: inserts, not a whole video |
| `lemo-opuscar` | 66 | Documentary formats: newsreel, split screen, investigation | Needs the separate Lemo checkout to render |
| `bang-motion`, `collage-director` | n/a | Motion-graphics and paper-collage engines | Collage needs paid MuAPI credit; never run without owner approval |

## Matching topic to look

| Topic type | First choice | Second choice |
|---|---|---|
| Why people behave a certain way (psychology) | Character-led look | `comic-art` |
| A study or experiment explained | Character-led look with diagram inserts | `chalkboard` |
| How the brain or body does something | `zackd-films` for the mechanism, characters around it | `flat-vector` |
| Money, business, productivity | `flat-vector` | `one-line-graph` for the data chapters |
| A big abstract idea (meaning, focus, time) | `dan-koe` | `glow-sketch` |
| History of an idea or invention | `renaissance-codex` | `comic-art` |
| A personal, gentle story | `risograph-cutout` | Character-led look |

## What to record after each video

So this guide can move from opinion to evidence, add to the production ledger for each published video: the look used, the average shot length, where viewers dropped off (from YouTube Studio), and which chapters held best. Do not record guesses.
