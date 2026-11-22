#!/usr/bin/env python3
"""Optional animation backends: capability routing and checked picture imports.

This module does not install or pretend to run external applications.
Export an assembled picture with the episode's measured voice duration first.
"""
import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "assets/animation-backends.json"

def catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["backends"]

def validate_import(recipe, root):
    root = Path(root).resolve()
    if not isinstance(recipe, dict):
        raise ValueError("Import recipe must be a JSON object")
    backend = recipe.get("backend")
    if backend not in catalog():
        raise ValueError("Choose a registered animation backend")
    relative = recipe.get("picture")
    if not isinstance(relative, str) or not relative:
        raise ValueError("A rendered picture path is required")
    path = (root / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(root) or not path.is_file() or not path.stat().st_size:
        raise ValueError("Picture must be nonempty and inside the episode")
    provenance = recipe.get("picture_provenance")
    if not isinstance(provenance, dict) or provenance.get("rights_verified") is not True:
        raise ValueError("Verify imported picture rights")
    for key in ("creator", "source", "license", "export_method"):
        if not isinstance(provenance.get(key), str) or not provenance[key].strip():
            raise ValueError("Missing picture provenance: " + key)
    return path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--recommend", help="Search capabilities, e.g. character, particle or compositing")
    args = parser.parse_args()
    data = catalog()
    if args.recommend:
        query = args.recommend.casefold()
        data = {key: value for key, value in data.items() if query in (key + " " + value["purpose"]).casefold()}
    print(json.dumps(data, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
