#!/usr/bin/env python3
"""Generate images (or short video clips) through MuAPI, the cloud model hub behind
Open Generative AI (github.com/Anil-matcha/Open-Generative-AI, MIT). Same API pattern as that
app's studio client: POST /api/v1/<model>, then poll /api/v1/predictions/<id>/result.

    python3 gen_media.py --model flux-krea-dev --prompt "..." --aspect 16:9 --out plate.png
    python3 gen_media.py --batch plates.json --out-dir film/plates     # {"name": {"prompt": "...", "model": "...", ...}}

Key: MUAPI_KEY env var, or a network secret saved for api.muapi.ai (header x-api-key) that the
session proxy injects — then any placeholder key works. Generations cost money on MuAPI.

Studio rules (see channel-profile.md): use it for environment plates, textures, thumbnails and
b-roll stills. Never real people or their likeness, never logos/brands/copyrighted characters,
no text in the image (type is set in the scene). Record every generated asset (model, prompt,
seed, date) in CREDITS — the script writes <out>.json next to each file — and tick YouTube's
"altered or synthetic content" box when realistic AI imagery appears.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

BASE = os.environ.get("MUAPI_BASE", "https://api.muapi.ai")
UA = {"User-Agent": "hunting-titles-studio/1.0", "Content-Type": "application/json"}


def _req(method, url, key, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers=dict(UA, **{"x-api-key": key}))
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        if e.code in (401, 403):
            raise SystemExit(f"gen_media: MuAPI refused the key ({e.code}). Save a key for api.muapi.ai (header x-api-key) or set MUAPI_KEY. {detail}")
        raise SystemExit(f"gen_media: {method} {url} failed: {e.code} {detail}")


def generate(model, payload, key, poll_s=2.0, max_wait=900):
    sub = _req("POST", f"{BASE}/api/v1/{model}", key, payload)
    rid = sub.get("request_id") or sub.get("id")
    if not rid:
        return sub
    t0 = time.time()
    while time.time() - t0 < max_wait:
        res = _req("GET", f"{BASE}/api/v1/predictions/{rid}/result", key)
        st = str(res.get("status", "")).lower()
        if st in ("completed", "succeeded", "success"):
            res["request_id"] = rid
            return res
        if st in ("failed", "error", "cancelled", "canceled"):
            raise SystemExit(f"gen_media: generation failed: {res.get('error') or res}")
        time.sleep(poll_s)
    raise SystemExit(f"gen_media: timed out after {max_wait}s (request {rid})")


def balance(key):
    b = _req("GET", f"{BASE}/api/v1/account/balance", key)
    return float(b.get("balance") or 0) + sum(float(v or 0) for v in (b.get("bonus_balances") or {}).values())


def one(name, spec, out, key):
    model = spec.get("model", "flux-krea-dev")
    payload = {k: v for k, v in spec.items() if k not in ("model",)}
    if "aspect" in payload:
        payload["aspect_ratio"] = payload.pop("aspect")
    res = generate(model, payload, key)
    url = (res.get("outputs") or [None])[0] or res.get("url") or (res.get("output") or {}).get("url")
    if not url:
        raise SystemExit(f"gen_media: no output URL in result: {json.dumps(res)[:300]}")
    cost = (res.get("cost") or {}).get("amount_usd")
    if "/webassets/" in url or cost == 0:
        # an unfunded account gets the model's stock sample back with "completed" — never use it
        raise SystemExit(f"gen_media: MuAPI returned a placeholder sample, not a generation ({url}, cost {cost}). "
                         "Top up the MuAPI account and retry.")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA["User-Agent"]}), timeout=120) as r, open(out, "wb") as f:
        f.write(r.read())
    meta = {"name": name, "model": model, "payload": payload, "request_id": res.get("request_id"), "source_url": url,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "provider": "MuAPI (via Open Generative AI API pattern)"}
    json.dump(meta, open(out + ".json", "w"), indent=1)
    print(f"{name}: {out}")
    return meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="flux-krea-dev"); ap.add_argument("--prompt"); ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--seed", type=int); ap.add_argument("--out")
    ap.add_argument("--batch"); ap.add_argument("--out-dir")
    a = ap.parse_args()
    key = os.environ.get("MUAPI_KEY") or "proxy-injected"
    bal = balance(key)
    if bal <= 0:
        raise SystemExit("gen_media: MuAPI balance is $0 — generations would return placeholder samples. Top up at muapi.ai first.")
    print(f"gen_media: MuAPI balance ${bal:.2f}", file=sys.stderr)
    if a.batch:
        specs = json.load(open(a.batch)); od = a.out_dir or "."
        for name, spec in specs.items():
            if name.startswith("_"): continue
            ext = spec.pop("ext", "png")
            one(name, spec, os.path.join(od, f"{name}.{ext}"), key)
        return
    if not (a.prompt and a.out):
        ap.error("--prompt and --out are required (or use --batch)")
    spec = {"model": a.model, "prompt": a.prompt, "aspect": a.aspect}
    if a.seed is not None: spec["seed"] = a.seed
    one(os.path.basename(a.out), spec, a.out, key)


if __name__ == "__main__":
    main()
