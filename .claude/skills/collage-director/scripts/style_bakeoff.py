#!/usr/bin/env python3
"""
Style bake-off: render ONE representative beat in candidate collage styles so
the user can pick the visual idiom before generating the full film.
"""
import json
import os

import paid
from provider import get_provider, run_jobs
from styles import compose_collage_prompt, STYLE_LIBRARY, resolve_theme, image_params

IMAGE_MODEL = "flux-dev"
DEFAULT_CANDIDATES = ["american-retro", "swiss-modern", "punk-zine", "atomic-age"]


def first_shot(beat):
    return beat["shots"][0] if beat.get("shots") else beat


def run(project_dir, styles=None, beat_index=0, generate=False, max_jobs=paid.DEFAULT_MAX_JOBS):
    styles = styles or DEFAULT_CANDIDATES
    with open(os.path.join(project_dir, "beats.json"), encoding="utf-8") as f:
        doc = json.load(f)
    aspect = doc.get("aspect", "16:9")
    img_model = doc.get("image_model", IMAGE_MODEL)
    img_res = doc.get("image_resolution", "1k")
    beat = doc["beats"][beat_index]
    shot = first_shot(beat)
    scene, bg = shot["scene"], beat.get("bg", "warm ochre")
    tcn, ten = beat.get("title_cn", ""), beat.get("title_en", "")
    out = os.path.join(project_dir, "style-bakeoff")

    prov = get_provider(doc.get("provider"))
    specs = {}
    for name in styles:
        tp = resolve_theme(name) or {}
        prompt = compose_collage_prompt(scene, tcn, ten, bg, aspect,
                                        style=tp.get("idiom", name), palette=tp.get("palette"),
                                        type_style=tp.get("type_style"), finish=tp.get("finish"))
        specs[name] = (lambda p=prompt: prov.submit_image(img_model, p,
                                                          **image_params(img_model, aspect, img_res)))
        tag = "library" if name in STYLE_LIBRARY else "custom"
        print(f"[{name}] ({tag}) queued")

    plan = [(name, img_model, os.path.join(out, f"{name}.jpg")) for name in specs]
    if not paid.approve(plan, generate, max_jobs):
        return
    os.makedirs(out, exist_ok=True)
    done = run_jobs(prov, specs, poll_s=3, stall_s=75, max_retries=2, deadline_s=240)

    for name, url in done.items():
        if url:
            prov.download(url, os.path.join(out, f"{name}.jpg"))
    print(f"\nSaved candidates to {out} — review, then set 'collage_style' in beats.json.")


if __name__ == "__main__":
    ap = paid.parser(__doc__)
    ap.add_argument("styles", nargs="?", help="comma-separated candidate styles")
    ap.add_argument("beat_index", nargs="?", type=int, default=0)
    a = ap.parse_args()
    run(os.path.abspath(a.project_dir), a.styles.split(",") if a.styles else None, a.beat_index,
        a.generate, a.max_jobs)
