#!/usr/bin/env python3
"""Search FounderNotes native styles and LICENSE-AWARE external animation catalogs.

The index is a discovery tool, NOT an installer, rendering engine, or rights
grant. Entries link to upstream docs rather than copying restricted prompts.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"
SOURCES_FILE = REFS / "community-animation-sources.json"
CATALOGS = {
    "lemo-opuscar": "lemo-opuscar-catalog.json",
    "code-animation-prompts": "code-animation-prompts-catalog.json",
    "anidoodle": "anidoodle-catalog.json",
    "claude-drawing-skill": "claude-drawing-catalog.json",
    "huashu-art-motion": "huashu-catalog.json",
}


def source_registry():
    data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("sources"), list):
        raise ValueError("Bad upstream source registry")
    sources = {item["id"]: item for item in data["sources"]}
    if len(sources) != len(data["sources"]):
        raise ValueError("Duplicate upstream source IDs")
    return sources


def remote_url(repo, path):
    # Explicit source-file URLs, including correctly encoded Chinese paths.
    return "https://github.com/" + repo + "/blob/main/" + quote(path, safe="/-._")


def entries():
    sources = source_registry()
    result = []
    for path in sorted((REFS / "styles").glob("*.md")):
        slug = path.stem
        result.append({
            "id": f"native:{slug}", "source": "native", "name": slug.replace("-", " ").title(),
            "kind": "native-style-reference", "status": "local-reference",
            "category": "FounderNotes original styles", "source_file": str(path.relative_to(ROOT)),
            "source_url": None, "description": "Original FounderNotes style specification",
        })
    for sid, filename in CATALOGS.items():
        src = sources[sid]
        catalog = json.loads((REFS / filename).read_text(encoding="utf-8"))
        items = catalog.get("entries", catalog.get("styles", []))
        if not isinstance(items, list):
            raise ValueError(f"Invalid catalog for {sid}")
        for item in items:
            slug = str(item.get("slug") or item.get("id"))
            if sid == "lemo-opuscar":
                source_file = item["style_file"]
                kind = "code-film-style"
                desc = item.get("category", "")
                stage = "upstream-guidance"
            elif sid == "code-animation-prompts":
                source_file = item["source_file"]
                kind = "prompt-and-visual-reference"
                desc = " ".join(str(item.get(k, "")) for k in ("description", "fit", "tags"))
                stage = "metadata-only-restricted-sharing"
            elif sid == "anidoodle":
                source_file = item["film_module"]
                kind = "code-media-style"
                desc = item.get("medium", "")
                stage = "upstream-engine-required"
            elif sid == "claude-drawing-skill":
                source_file = item["source_file"]
                kind = "procedural-still-style"
                desc = item.get("class", "") + " " + (item.get("library_file") or "")
                stage = "upstream-still-generator-required"
            else:
                source_file = item["source_file"]
                kind = "art-motion-recipe"
                desc = item.get("note", "")
                stage = item.get("stage", "unverified")
            result.append({
                "id": f"{sid}:{slug}", "source": sid, "name": item["name"],
                "category": item.get("category") or src["kind"], "kind": kind,
                "status": stage, "source_file": source_file,
                "source_url": remote_url(src["repo"], source_file),
                "description": desc[:450],
            })
    ids = [x["id"] for x in result]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate animation IDs")
    return result



def provider_entries():
    """Expose reference-only providers in search without inflating style counts."""
    results = []
    for sid, src in source_registry().items():
        if sid in CATALOGS:
            continue
        results.append({
            "id": f"{sid}:provider", "source": sid,
            "name": sid.replace("-", " ").replace("_", " ").title(),
            "category": src["kind"], "kind": "external-provider-reference",
            "status": "upstream-skill-not-installed",
            "source_file": src["upstream_skill"],
            "source_url": remote_url(src["repo"], src["upstream_skill"]),
            "description": src["notes"] + " " + src["kind"],
        })
    return results


def search(text, *, source=None, limit=12):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Search query must be nonempty")
    if limit < 1 or limit > 100:
        raise ValueError("limit must be 1..100")
    # Make the common US/UK spelling of watercolour discover each other.
    normalized = text.casefold().replace("watercolour", "watercolor")
    words = re.findall(r"[\w-]+", normalized, re.UNICODE)
    if not words:
        raise ValueError("Invalid search query")
    ranked = []
    for item in entries() + provider_entries():
        if source and item["source"] != source:
            continue
        name = item["name"].casefold().replace("watercolour", "watercolor")
        hay = " ".join(str(item[k]) for k in ("id", "name", "category", "description")).casefold().replace("watercolour", "watercolor")
        score = sum(5 if word in name else 1 if word in hay else 0 for word in words)
        if score:
            ranked.append((score, item))
    ranked.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [x[1] for x in ranked[:limit]]


def available_sources():
    sources = source_registry()
    counts = {}
    for item in entries():
        sid = item["source"]
        counts[sid] = counts.get(sid, 0) + 1
    return [
        {"id": "native", "entry_count": counts.get("native", 0),
         "availability": "local-reference", "engine": "FounderNotes motion"},
        *[{"id": id_, "entry_count": counts.get(id_, 0),
           "availability": src["availability"], "kind": src["kind"],
           "license": src["license"], "source_url": src["homepage"],
           "notes": src["notes"]} for id_, src in sources.items()]
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sources", action="store_true", help="List source libraries and counts")
    group.add_argument("--search", metavar="QUERY", help="Search across catalogs, including Chinese")
    group.add_argument("--show", metavar="SOURCE:STYLE", help="Show one exact style ID")
    group.add_argument("--list", metavar="SOURCE", help="List styles from a source")
    parser.add_argument("--limit", type=int, default=15, help="Search/list page limit (1..100)")
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    if args.sources:
        answer = available_sources()
    elif args.show:
        answer = next((item for item in entries() + provider_entries() if item["id"] == args.show), None)
        if answer is None:
            parser.error("Style ID not in catalog; use --search or --list")
    elif args.list:
        if args.list not in {"native", *source_registry().keys()}:
            parser.error("Unknown source ID")
        answer = [x for x in entries() + provider_entries() if x["source"] == args.list][:args.limit]
    else:
        answer = search(args.search, limit=args.limit)
    print(json.dumps(answer, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
