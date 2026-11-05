# Hunting Titles — "Ink & Gold" house style (v1)

Original style for the channel. Not a copy of any repo's look: it borrows *practices*
(voice-first timing, render contract, draft→polish, stills review) and invents its own look.

## Idea
A channel about chasing titles. Night-blue worlds lit by one warm source. Gold = the thing
being chased (trophies, scores, the gold thread). Cream = people and warmth. Ember = feeling.

## Palette (only these)
| token | hex | use |
|---|---|---|
| ink | #0E1822 | deepest background, outlines |
| night | #17293A | main background |
| slate | #2A4052 | mid-ground shapes |
| fog | #6F8899 | far silhouettes, secondary text |
| cream | #F3E8D2 | type, character highlights, people |
| gold | #E8B34A | trophies, the gold thread, key numbers |
| goldLt | #FFD98A | glints, light cores |
| ember | #E0703A | emotion, warnings, "job two" |
| sea | #4FA3A0 | needs gauges / growth (sparingly) |

## Light & depth (every scene)
- Exactly one key light (stadium, lamp, moon, window). Radial glow + soft beam + floating dust motes.
- Character gets a cream rim light on the light side and a long soft shadow away from it.
- 3 depth layers: far (fog silhouettes, slow parallax), mid (set), near (dark blurred shapes passing).
- Fine film grain + vignette always on.

## The gold thread
A 6 px gold line with a soft glow. It is the chase: it leads the character, becomes the
graph line, the gauge fill, the runway edge. Draw it on with `K.thread()`; it should appear in
most scenes and connect one idea to the next across cuts.

## Type
- Titles: HTSerif (Lora Bold), cream, 72–110 px, tight leading.
- Labels: HTSans Bold, UPPERCASE, letter-spacing 6, 30–40 px, gold or cream.
- Quotes: HTSerif in cream on an ink card with gold hairline border; speaker + source under it.
- Source lines: `K.source()` bottom-left, 24 px fog. Required whenever a claim is on screen.
- Max 7 words per label. Keep y > 900 clear (captions).

## Motion
- Premium/calm. Ease out in, ease in out; never linear for movement.
- Three durations: 0.45 s (quick), 0.9 s (standard), 1.4 s (slow reveal). Stagger 80–120 ms.
- Every hold has ambient motion: dust motes, camera drift (≤3 % zoom per 10 s), breathing.
- Nothing static > 2.5 s. Cuts land on narration beats (`S.at(id, f)`).

## Character — "the hunter"
Late-20s man, tall and lean, warm brown skin, dark wavy hair, deep-teal jacket over a cream
tee, charcoal trousers, white sneakers. Poses come from `K.POSE` + `K.walk`; animate with
breathing, blinks, head turns and jacket sway. Keep him ≤ 50 % of frame height in wide
shots, use push-ins for emotion.
