#!/usr/bin/env python3
"""Write references/style-ratings-all.md: one editorial rating per entry of the five external catalogs.

Ratings are judgement from each entry's index text (name, medium, stated fit), NOT audience data and NOT render tests.
Tiers: F full-video candidate | C chapter | I insert (5-20 s) | T title/transition/text card |
       S structure or technique (not a look) | X do not use | ? index has no description.
Run:  python3 build_style_ratings.py   (fails if any catalog entry is unrated or an unknown id is rated)"""
import json, pathlib, sys

REF = pathlib.Path(__file__).resolve().parent.parent / 'references'
TIER = {'F': 'Full video', 'C': 'Chapter', 'I': 'Insert', 'T': 'Title / transition', 'S': 'Structure, not a look', 'X': 'Do not use', '?': 'Cannot rate'}
DEF = {'F': 'Can show readable people and hold 8 minutes', 'C': 'Strong for one chapter; tiring or limiting for a whole video', 'I': '5-20 s mood or novelty shot',
       'T': 'Titles, chapter cards, transitions', 'S': 'A way to organise a video; combine with any look', 'X': '', '?': 'The index gives a number only, no name or description'}
FILM = 'Recreates a named film sequence; conflicts with the originality rule'
BRAND = 'Imitates a living artist, studio or show; conflicts with the originality rule'
OLD = 'Imitates one historical painter; public domain, use sparingly as a painted insert'

def parse(block):
    out = {}
    for line in block.strip().splitlines():
        p = [s.strip() for s in line.split('|')]
        out[p[0]] = (p[1], p[2] if len(p) > 2 else '', p[3] if len(p) > 3 else '')
    return out

ANI = parse("""
balloon|F|Crayon|Warm, friendly characters; childhood and habit topics
blueprint|C|Cyanotype blueprint|How a system is built
brokenColour|I|Broken colour (oil dabs)|
charcoalErasure|C|Charcoal, erased and redrawn|Struggle, doubt, memory
colouredPencil|F|Coloured pencil|Gentle character explainer
dreamGlaze|I|Dream glaze|
embroidery|I|Hand embroidery|
flatVector|F|Flat vector|Business, habits, step-by-step
folkTale|F|Folk-tale storybook|Story-led topics
fox|C|Cut-paper collage|A personal story
halftone|C|Newsprint halftone|History, exposing a myth
isometric|C|Isometric cutaway|Systems and processes
koi|F|Marker comic|Emotion and conflict
lighthouse|C|Risograph|Warm handmade chapter
lowPoly|I|Low-poly|
mellan|T|Single-line engraving|Portrait or title
midCentury|F|Mid-century gouache|Classic explainer look
moonPhases|F|Chalkboard|Explaining a mechanism
paintedOil|I|Oil on canvas|
paperCraft|C|Toy-theatre paper collage|A staged story
pixelArt|C|Pixel art|Habits as a game
pocketWatch|C|Ballpoint sketch|Notebook, personal reflection
ranunculus|C|Pencil and watercolour|Gentle, reflective chapter
rubberHose|C|Rubber hose|Playful analogy
scrapbook|C|Archival scrapbook|Biography, looking back
scratchboard|I|Scratchboard|
stipple|I|Pen-and-ink stipple|
storybook|F|Storybook pencil and watercolour|Story-led, personal topics
sumiE|C|Sumi-e ink painting|Calm, reflective chapter
toyBrick|I|Toy brick|
woodcut|I|Ukiyo-e colour woodblock|
wren|C|Ink and line-wash|Everyday scenes
""")
CD = parse("""
inkpaint|C|Ink painting|Calm, reflective chapter
watercolor|C|Watercolour|Emotion and memory
papercut|C|Paper-cut collage|A story chapter
colorpencil|F|Coloured pencil|Gentle character explainer
anime|C|Anime-style drawing|A dramatic story beat; hard to sustain in code
editorial|F|Editorial hand-drawn|Ideas with people; magazine feel
oilpaint|I|Thick oil paint|
ukiyoe|I|Ukiyo-e woodblock|
pixelart|C|Pixel art|Habits as a game
clay|C|Clay stop-motion|Playful analogy
cyanotype|I|Cyanotype|
stitch|I|Cross-stitch|
panel|I|Retro instrument panel|A dial or meter moment
sticker|C|Sticker collage and receipt|Lists, "add it up" moments
notebook|C|Lab notebook with stickers|Explaining a study
chalk|F|Chalkboard writing|Explaining a mechanism
cyberpunk|I|Cyberpunk|
cartoon|F|Hand-drawn cartoon, frame by frame|Character-led explainer
isometric|C|Isometric 2.5D|Systems and processes
lineart|C|Single-line drawing|One idea turning into the next
soft3d|C|Soft-light 3D|Body or brain mechanism
morph|T|Shape morph|Transitions between ideas
newscollage|C|Newspaper collage|History, public events
aurora|T|Diffuse glass gradient|Quiet title card
bauhaus|I|Bauhaus geometry|
synthwave|I|Retro synthwave|
perler|I|Fuse beads|
petroglyph|I|Rock carving|
tomb|I|Egyptian tomb mural|
mosaic|I|Roman mosaic|
stainedglass|I|Stained glass|
illuminated|I|Illuminated manuscript|
codex|C|Inventor's notebook|History of an idea
silhouette|C|Silhouette|Anonymous "you" stories
letterpress|T|Letterpress poster|Quote card
constructivism|I|Constructivist poster|
artdeco|T|Art Deco|Title card
comic|F|Golden-age comic|Emotion, conflict, case stories
popart|I|Pop silkscreen|
lineprinter|I|ASCII line-printer art|
lowpoly|I|Low-poly 3D|
stencil|I|Spray stencil|
patch|I|Embroidered patch|
blueprint|C|Engineering blueprint|How something is built
crayon|F|Children's crayon|Warm, friendly characters
crt|I|Green-screen terminal|
thermal|I|Thermal camera|Stress or heat as a picture
delft|I|Delft blue tile|
cave|I|Cave painting|
macpaint|I|1-bit early paint program|
blackfigure|I|Greek black-figure vase|
graphite|C|Pencil sketch|Quiet, honest chapter
xray|I|X-ray film|Looking inside the body
rubberhose|C|1930s rubber-hose cartoon|Playful analogy
linocut|I|Black-and-white linocut|
vhs|I|VHS home video|A memory
flatvector|F|Flat vector|Business, habits, step-by-step
storybook|F|Picture-book character animation|Story-led, personal topics
ballpoint|C|Ballpoint doodle|Notebook, personal reflection
overlay|C|Tracing-paper layers|A mechanism built up in layers
pastelui|I|Pastel interface|
grading|C|Exam marking|Test, exam and school topics
shadowpuppet|C|Shadow puppetry|A story told simply
penwash|C|Pen and wash|Everyday scenes
gouache|F|Retro gouache|Classic explainer look
bluebook|C|Blue picture book|Night, sadness, calm
jiangnan|I|Garden landscape|
drybrush|I|Dry-brush blocks|
twilight|C|Twilight miniature storybook|Evening, reflection
nocturne|C|Hatched night scene|Night, worry
obsidianui|I|Note-app interface|
canvasboard|C|Whiteboard cards|Frameworks, lists of ideas
flexoki|I|Paper-tone palette|
pencilbook|F|Warm pencil storybook|Gentle character explainer
colortown|I|Colourful town|
pastelvignette|I|Pastel vignette|
poetichalloween|I|Poetic Halloween|
oilpastel|I|Oil-pastel portrait|
sketchbook|F|Sketchbook doodle|Casual character explainer
spotillo|C|Flat spot illustration|Small scenes between ideas
grainbook|F|Grainy picture book|Story-led, personal topics
dreamhills|I|Soft-light hills|
sunlitgreen|I|Sunlit greenery|
""")
HS = parse("""
01_cave|I|Cave art|
02_egypt|I|Egyptian|
03_greek|I|Greek|
04_roman|I|Roman|
05_gothic|I|Gothic|
06_renaissance|C|Renaissance|History of an idea
08_impressionism|I|Impressionism|
09_postimp|I|Post-impressionism|
10_nouveau|T|Art Nouveau|Title card
11_cubism|I|Cubism|
12_bauhaus|I|Bauhaus|
13_pop|I|Pop art|
14_8bit|C|8-bit|Habits as a game
15_raytrace|I|Early ray-traced 3D|
16_2026|I|Contemporary digital|
17_ink|C|Ink|Calm, reflective chapter
18_klimt|I|Klimt|OLD
19_munch|I|Munch|OLD
20_dunhuang|I|Dunhuang mural|
21_kusama|X|Kusama|BRAND
22_constructivism|I|Constructivism|
23_dali|X|Dali|BRAND
24_hopper|X|Hopper|BRAND
25_ghibli|X|Ghibli|BRAND
26_vaporwave|I|Vaporwave|
27_kirby|X|Kirby|BRAND
28_monet|I|Monet|OLD
29_seurat|I|Seurat|OLD
30_matisse|X|Matisse|BRAND
31_haring|X|Haring|BRAND
32_rembrandt|I|Rembrandt|OLD
33_rubberhose|C|Rubber hose|Playful analogy
34_shadowpuppet|C|Shadow puppet|A story told simply
35_shinkai|X|Shinkai|BRAND
36_picasso_blue|X|Picasso blue period|BRAND
37_rick_morty|X|Rick and Morty|BRAND
38_giotto|I|Giotto (research stage)|OLD
39_piero|I|Piero (research stage)|OLD
40_raphael|I|Raphael (research stage)|OLD
41_michelangelo|I|Michelangelo (research stage)|OLD
42_guardi|I|Guardi (research stage)|OLD
43_lorenzetti|I|Lorenzetti (research stage)|OLD
44_cortona|I|Cortona (research stage)|OLD
45_renoir|I|Renoir (research stage)|OLD
46_pissarro|I|Pissarro (research stage)|OLD
47_sisley|I|Sisley (research stage)|OLD
48_gauguin|I|Gauguin (research stage)|OLD
49_chagall|X|Chagall (research stage)|BRAND
50_ma_yuan|I|Ma Yuan (research stage)|OLD
51_persian_miniature|I|Persian miniature (research stage)|
52_south_park|X|South Park (research stage)|BRAND
53_pixar|X|Pixar (research stage)|BRAND
55_dunhuang|I|Dunhuang (research stage)|
""")
LEMO = parse("""
caption-news|C|Caption News|Works with sound off; Shorts
newsreel|I|1920s Newsreel|
countdown|I|Live Countdown Split-screen|
city-symphony|I|Time-lapse Symphony|
visual-investigation|C|Visual Investigation|Tracing how something happened
kino-montage|I|Constructivist Montage|
telestrator|C|Sports telestrator|Freezing and marking up one moment
news-package|T|TV news package|Opening sting
satellite-briefing|I|Satellite briefing|
briefing-board|C|Briefing board|Comparing options side by side
lidar-survey|I|Lidar survey|
white-model|I|White model projection|
data-physical|C|Data made physical|Making a number felt
teardown|C|Exploded teardown|What something is made of
microscope|C|Microscope story|Zooming into the body or brain
archive-lighttable|C|Archive light table|Old documents, looking back
crayon-book|F|Crayon picture book|Warm, friendly characters
watercolor|C|Watercolour|Emotion and memory
ink-wash|C|Ink wash|Calm, reflective chapter
impasto|I|Impasto oil|
one-line|C|One line|One idea turning into the next
whiteboard|F|Whiteboard|Explaining a mechanism step by step
urban-sketch|C|Urban sketch|Everyday scenes
chalkboard|F|Chalkboard|Explaining a mechanism
shadow-puppet|C|Shadow puppet|A story told simply
ukiyoe|I|Ukiyo-e|
papercut-red|I|Red paper-cut|
paper-lantern|I|Paper lantern|
risograph|C|Risograph|Warm handmade chapter
halftone-dossier|C|Halftone dossier|Exposing a myth
woodcut|I|Woodcut|
engraving|I|Engraving|
silkscreen-poster|T|Silkscreen poster|Title or thumbnail look
printed-long-take|I|Printed long take|
swiss-motion|T|Swiss motion type|Clean text cards
spy-titles|T|1960s spy titles|Opening titles
art-deco|T|Art Deco|Title card
blueprint|C|Blueprint|How something is built
stained-glass|I|Stained glass|
pictogram-motion|C|Pictogram motion|Steps and numbers
ascii-crt|I|ASCII / CRT|
dataviz|C|Data story|A chapter built on numbers
iso-infographic|C|Isometric infographic|A process as a small world
dark-keynote|I|Dark keynote|
living-screencast|I|Living screencast|
hologram-hud|I|Hologram interface|
transit-map|C|Transit map|A journey or sequence of stages
isometric-picture-book|C|Isometric picture book|A small world that grows
circuit-board|I|Circuit board|
rubber-hose|C|1930s rubber hose|Playful analogy
cel-anime-80s|I|1980s cel animation|
scifi-toon|I|Sci-fi sitcom cartoon|
midcentury-toon|F|1950s flat cartoon|Old educational-film feel; people and ideas
pixel-rpg|C|16-bit pixel RPG|Habits as levels
hd-2d|I|HD-2D|
microgame|I|Microgame flash|
game-show|I|Game show|
silent-film|I|1920s silent film|
backrooms|I|Backrooms|Unease, fear of the unknown
brick-toy|I|Brick toy|
paper-popup|C|Paper pop-up book|A story chapter
tilt-shift|I|Tilt-shift miniature|
lowpoly-island|I|Low-poly island|
glass-product|I|Glass product|
memphis-diorama|I|Memphis diorama|
desktop-flythrough|I|Desktop flythrough|
""")
CAP = parse("""
A1|I|Word rain|Being lectured, pressure
A2|I|Cursor typing|Inner monologue
A3|T|Big-word impact|A key line
A4|I|Tunnel of words|Overthinking
A5|I|Words scatter and regroup|A change of mind
B1|I|Flowing threads|
B2|I|Firefly dust|
B3|I|Particles forming a shape|
B4|I|Constellation lines|Connection, loneliness
B5|I|Breathing circle|Calming down
C1|I|Ink bloom|
C2|C|One-stroke drawing|The outline of a person or event
C3|I|Contour map of feeling|
C4|I|Ripples|After-effects of one remark
D1|I|Rain on a window|
D2|I|Window light and dust|
D3|I|Snow and sparks|
D4|T|Daybreak|Ending, hope
E1|C|Minimal geometry|Making a complex thing clear
E2|C|Layered paper-cut|Childhood, gentle passages
E3|I|Character art|
F1|C|Growing charts|Data and study results
F2|C|Relationship diagram|Cause and effect
F3|C|Split-screen comparison|Before and after
G1|I|Old film|
G2|I|Signal glitch|Breakdown, interruption
M1|F|Whiteboard hand-drawn explainer|Concepts and mechanisms
M2|F|Paper handwritten notes|Methods and "you can do this" passages
M18|C|Maths and science explainer|Principles and data
M19|F|Beginner-level science explainer|A whole "what is X" episode
M20|C|Timeline / history|How something developed
M21|C|How-it-works teardown|A mechanism step by step
M22|C|Recipe-style steps|"Do these few steps"
M23|S|Five-act explainer template|Skeleton for an episode
M24|I|Four-part launch film|
M8|S|Voice-over with word-level captions|Captioning method
M9|S|Emotional arc: chaos, control, clarity|Episode structure
M10|C|An abstract feeling made visible|Fear, anxiety, overthinking
M11|I|Life loop|
M12|C|Paper-cut shadow play|Home, memory, warmth
M13|C|Hand-drawn stop-motion, first person|An object speaks for itself
M27|T|Wordless short|Intro, outro, bridge
M28|I|Symmetrical warm scenery|
M29|I|3D sunset sky with one line|The emotional peak
M30|I|Eastern mood landscape|
M31|I|Clay stop-motion music video|
M3|T|Word architecture|The closing line
M25|I|Lyric beats|
M36|I|Breaking the frame|A turning point
M4|S|One element through the whole film|Ties mixed looks together
M5|S|One continuous shot|Showing a change
M33|I|Pull back from a point to the universe|Scale
M38|C|One shape that keeps changing|Listing many examples quickly
M37|T|Logo assembling|Channel intro or outro
M6|I|Product-keynote look|
M7|I|Minimal beat cuts|
M32|I|Fast vertical point-of-view|First 3 s of a Short
M34|I|News roundup|
M14|?||
M15|?||
M16|?||
M17|?||
M26|?||
M35|?||
M39|?||
M40|?||
K1|F|Flat vector character|Clean, bright narrator figure
K2|C|Chibi character|Light, playful chapter
K3|I|Kawaii character|
K4|F|Minimal line figure|Closest to the current Founder Notes look
K5|C|Long-limbed flat corporate figure|Reads as generic stock art
K6|F|Clear-line comic|Stories with settings
K7|C|Anime-style character|Dramatic beat; hard to sustain in code
K8|F|Picture-book character|Warm, personal topics
K9|C|Doodle|"The old me", self-mockery
K10|F|Chalk on blackboard|Explaining a principle
K11|C|Journal notes|Listing methods and steps
K12|C|Four-panel newspaper strip|A light joke
K13|C|Halftone comic|Satire
K14|I|Pop art|
K15|C|1930s rubber hose|Playful analogy
K16|F|Mid-century modern|Designed, classic explainer
K17|C|Geometry|Structures and systems
K18|C|Watercolour|Emotion and memory
K19|I|Thick paint|
K20|C|Paper-cut|Telling a story
K21|C|Handmade papercraft|Warm science passage
K22|I|Origami|
K23|I|Collage|
K24|I|Clay|
K25|I|Feature-film-style 3D|Too heavy for this toolchain
K26|I|Toon-shaded 3D|
K27|I|Low-poly|
K28|C|Pixel|Game feel
K29|C|Blueprint|Structure of a tool
K30|C|Instruction-manual line art|Steps
K31|I|Knolling flat-lay|
K32|I|Building blocks|
K33|C|Subway map|A process or route
K34|I|Cyber neon|
K35|I|Old-academy look|
K36|T|Silkscreen|Poster frame
K37|I|Gothic|Fear, the dark side
K38|C|Sitcom scene|Everyday situations
Z1|I|Ink wash|
Z2|I|Fine-brush painting|
Z3|I|Freehand brush painting|
Z4|I|Mountain-and-water landscape|
Z5|I|Red paper-cut|
Z6|I|New Year print|
Z7|C|Shadow puppetry|A story told simply
Z8|I|Dunhuang mural|
Z9|I|Blue-and-white porcelain|
Z10|I|Woodblock print|
Z11|I|Opera mask|
Z12|T|Calligraphy|A key word written stroke by stroke
Z13|C|Ink-brush comic|A story chapter
Z14|F|Coloured-pencil hand drawing|Gentle character explainer
Z15|F|Warm watercolour explainer card|Friendly science explainer
H1|T|Layout: Biennale Yellow|Text card
H2|T|Layout: BlockFrame|Text card
H3|T|Layout: Blue Professional|Text card
H4|T|Layout: Bold Poster|Text card
H5|T|Layout: Broadside|Text card
H6|T|Layout: Capsule|Text card
H7|T|Layout: Cartesian|Text card
H8|T|Layout: Cobalt Grid|Text card
H9|T|Layout: Coral|Text card
H10|T|Layout: Creative Mode|Text card
H11|T|Layout: Daisy Days|Text card
H12|T|Layout: Editorial Forest|Text card
L1|C|Caption news|Works with sound off; Shorts
L2|I|1920s newsreel|
L3|I|Countdown split-screen|
L4|I|Time-lapse symphony|
L5|C|Visual investigation|Tracing how something happened
L6|I|Constructivist montage|
L7|C|Sports tactics board|Freezing and marking up one moment
L8|T|TV news package|Opening sting
L9|I|Satellite map briefing|
L10|C|Options comparison wall|Comparing choices
L11|I|Laser point-cloud scan|
L12|I|White model projection|
L13|C|Data made physical|Making a number felt
L14|C|Exploded teardown|What something is made of
L15|C|Microscope story|Zooming into eyes, nerves, the brain
L16|C|Archive light box|Old documents, memory
L17|F|Crayon picture book|Warmth, childhood
L18|C|Watercolour brush|Gentle emotional passage
L19|C|Ink wash|Calm, reflective chapter
L20|I|Thick oil paint|
L21|C|One-stroke drawing|One line through an idea
L22|F|Whiteboard explainer|Principles and steps
L23|C|Pen and wash|Everyday scenes
L24|C|Shadow puppet|A story told simply
L25|I|Ukiyo-e|
L26|I|Red window paper-cut|
L27|I|Paper lantern layers|
L28|C|Risograph|Magazine feel
L29|C|Retro halftone dossier|Exposing a myth
L30|I|Woodcut|
L31|I|Copperplate engraving|
L32|T|Silkscreen travel poster|Title or cover
L33|T|Swiss motion type|Clean text cards
L34|T|1960s spy titles|Opening titles
L35|T|Art Deco|Title card
L36|C|Blueprint|Principles and structure
L37|I|Stained glass|
L38|C|Pictogram motion|Steps and numbers
L39|I|ASCII / CRT terminal|
L40|C|Data storytelling|A chapter built on numbers
L41|C|Isometric infographic|A process as a small world
L42|I|Dark tech keynote|
L43|I|Live screen recording with a character|
L44|I|Sci-fi hologram interface|
L45|C|1930s rubber hose|Playful analogy
L46|I|1980s cel animation|
L47|I|Sci-fi sitcom cartoon|
L48|F|1950s flat cartoon|Old educational-film feel; perception and behaviour topics
L49|C|16-bit pixel RPG|Learning as levelling up
L50|I|HD-2D|
L51|I|Microgame flash|
L52|I|Variety-show flat|
L53|I|1920s silent film|
L54|I|Backrooms|Unease, fear of the unknown
L55|I|Brick toy|
L56|C|Paper pop-up book|A story chapter
L57|I|Tilt-shift miniature|
L58|I|Low-poly isometric|
L59|I|Glass product|
V1|F|Hand-drawn boiling line|Warm character explainer
V2|C|Isometric 2.5D|A small world that grows
V3|F|Flat vector|Clean narrator figure
V4|C|Line drawing|One line carrying an idea
V5|I|Soft 3D render|Needs Blender, not installed
V6|T|Shape morph|Transitions between ideas
V7|C|Sticker explainer|Light explanation
V8|I|Cyberpunk interface|
V9|C|Collage|Clippings, memory
V10|T|Aurora and frosted glass|Quiet title card
V11|I|Bauhaus geometry|
V12|I|1980s synthwave / VHS|
V13|C|Pixel|Memory, game feel
V14|T|Liquid flow|Soft transitions
V15|I|Variety-show captions|Vertical Shorts captions
X1|F|Hand-drawn|Explaining and recording
X2|T|Brand motion graphics|Channel intro
X3|C|Sand painting|Memory, emotion
X4|I|Lyric video|
X5|I|Beat-cut footage edit|
X6|I|Interface morph|
X7|C|Hero comic|A turning point
X8|C|Journal scrapbook|Looking back over a period
X9|C|Torn-paper collage|Memory, piecing things together
X10|I|Particles|
X11|T|Split-flap board|Titles and numbers
X12|T|Neon sign|A key line
X13|I|16-bit arcade|
X14|I|CRT terminal|
X15|I|Thermal receipt|"Add it up" lists
X16|C|Subway line map|How you got from there to here
X17|C|Blueprint|Structure
X18|F|Comic book|Panel-by-panel story
X19|C|Documentary|Treating one thing seriously
X20|C|Museum exhibit|Showing items one by one
X21|T|Breaking news|Opening sting
X22|C|Detective evidence board|Connecting clues; "why does this happen"
X23|F|Picture book|Telling a story warmly
X24|C|RPG quest|Learning as a quest
X25|C|Weather forecast|Moods as weather
X26|I|TV shopping parody|Satire of hype
X27|I|Sports broadcast|
X28|C|Assembly instructions|Steps
X29|F|Whiteboard lecture|Explaining a principle
X30|T|Film trailer|Next-episode teaser
X31|C|Maths proof lecture|Reasoning to a conclusion step by step
R1|I|Neon rainy night|
R2|I|Retro anime night drive|
R3|I|Graffiti comic|
R4|I|Dark industrial sci-fi|
R5|I|Pixel cyber city|
R6|I|Eastern cyber fantasy|
R7|I|Flat dusk rooftops|
""")

def note(t, n):
    n = {'OLD': OLD, 'BRAND': BRAND}.get(n, n)
    return n or DEF[t]

def table(title, src, ids, rated, orig=None, extra=''):
    miss = [i for i in ids if i not in rated]; unknown = [i for i in rated if i not in ids]
    if miss or unknown: sys.exit(f'{title}: unrated {miss[:8]} unknown {unknown[:8]}')
    rows = [f'\n## {title} ({len(ids)})\n', f'Source index: `{src}`. {extra}\n', '| ID | Name | Use | Best for / why |', '|---|---|---|---|']
    for i in ids:
        t, name, n = rated[i]
        if orig and orig.get(i) and orig[i] != name: name = f'{name} ({orig[i]})' if name else orig[i]
        rows.append(f'| `{i}` | {name or "(unnamed)"} | {TIER[t]} | {note(t, n)} |')
    return rows, [rated[i][0] for i in ids]

L = lambda f: json.load(open(REF / f))
ani, cd, hs, lemo, cap = L('anidoodle-catalog.json'), L('claude-drawing-catalog.json'), L('huashu-catalog.json'), L('lemo-opuscar-catalog.json'), L('code-animation-prompts-catalog.json')
for e in cap['entries']:
    if e['series'] == 'O': CAP[e['id']] = ('X', 'Film homage', FILM)
body, tiers = [], []
for args in [('Anidoodle', 'anidoodle-catalog.json', [e['id'] for e in ani['entries']], ANI, None, 'Hand-made media looks.'),
             ('Claude Drawing', 'claude-drawing-catalog.json', [e['id'] for e in cd['entries']], CD, {e['id']: e['name'] for e in cd['entries']}, 'Illustration looks; upstream names kept in brackets.'),
             ('Huashu art styles', 'huashu-catalog.json', [e['id'] for e in hs['entries']], HS, None, 'Art-history looks. "Research stage" entries are unverified upstream.'),
             ('Lemo-Opuscar', 'lemo-opuscar-catalog.json', [e['slug'] for e in lemo['styles']], LEMO, None, 'Documentary and format looks; rendering needs the separate Lemo checkout.'),
             ('Code animation prompts', 'code-animation-prompts-catalog.json', [e['id'] for e in cap['entries']], CAP, {e['id']: e['name'] for e in cap['entries']}, 'Prompt library; upstream names kept in brackets. The O series is 98 film homages.')]:
    rows, t = table(*args); body += rows; tiers += t
count = {k: tiers.count(k) for k in TIER}
head = ['# Every external style entry, rated for Founder Notes', '',
        'Generated by `scripts/build_style_ratings.py` on 2026-11-11. Read `style-selection-guide.md` first; this file is the long list behind it.', '',
        '**How these were rated.** From each entry\'s index text only: its name, its stated medium and its stated use. No entry here was rendered or shown to an audience, so every rating is an editorial first guess. An entry marked "Full video" still has to win a real treatment comparison and a pilot.', '',
        '**The question asked of each entry:** can it show a readable person with a readable emotion, explain a mechanism, and stay comfortable for eight minutes? That is what Founder Notes psychology topics need.', '',
        f'**Totals across {len(tiers)} entries**', '', '| Use | Count | Meaning |', '|---|---|---|']
head += [f'| {TIER[k]} | {count[k]} | {DEF[k] or "Conflicts with the originality rule (reason given per row)"} |' for k in TIER]
(REF / 'style-ratings-all.md').write_text('\n'.join(head + body) + '\n')
print(len(tiers), 'entries', count)
