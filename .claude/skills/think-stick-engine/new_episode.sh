#!/bin/bash
# Set up a Think! stick-engine episode: bash new_episode.sh <slug>  ->  studio-output/<slug>/full/{film,tools}
set -e; SLUG=${1:?usage: new_episode.sh <slug>}; E="$(cd "$(dirname "$0")" && pwd)"; R=$(git -C "$E" rev-parse --show-toplevel)
F="$R/studio-output/$SLUG/full"; mkdir -p "$F/film/fonts" "$F/narration" "$F/dialogue"
cp "$E"/engine/*.js "$E"/engine/stick.html "$E"/engine/sfx.py "$F/film/"
cp "$E"/tools/*.py "$E"/tools/*.sh "$E"/tools/*.mjs "$F/"
cp "$R/.claude/skills/podcast-scout-skill/assets/brand/think-logo.png" "$F/film/logo.png"
cp "$R"/.claude/skills/podcast-scout-skill/assets/ink-gold-kit/fonts/InstrumentSans-*.ttf "$R"/.claude/skills/podcast-scout-skill/assets/ink-gold-kit/fonts/InstrumentSans-OFL.txt "$F/film/fonts/"
bash "$E/fetch_music.sh"
echo "Episode ready: $F  (write film/shots.js + scenes, order.json, narration/ and dialogue/ scripts; see SKILL.md)"
