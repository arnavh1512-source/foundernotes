#!/usr/bin/env python3
"""Generate images (or short video clips) through MuAPI, the cloud model hub behind
Open Generative AI (github.com/Anil-matcha/Open-Generative-AI, MIT). Same API pattern as that
app's studio client: POST /api/v1/<model>, then poll /api/v1/predictions/<id>/result.

    python3 gen_media.py --model flux-krea-dev --prompt "..." --aspect 16:9 --out plate.png --generate
    python3 gen_media.py --batch plates.json --out-dir film/plates --generate   # {"name": {"prompt": "...", "model": "...", ...}}

Without --generate it only prints the plan (no network). --max-jobs (default 20) caps a batch.
Key: MUAPI_KEY env var, or a network secret saved for api.muapi.ai (header x-api-key) that the
session proxy injects — then any placeholder key works. Generations cost money on MuAPI.

Studio rules (see channel-profile.md): use it for environment plates, textures, thumbnails and
b-roll stills. Never real people or their likeness, never logos/brands/copyrighted characters,
no text in the image (type is set in the scene). Record every generated asset (model, prompt,
seed, date) in CREDITS — the script writes <out>.json next to each file — and tick YouTube's
"altered or synthetic content" box when realistic AI imagery appears.
"""
import argparse, json, os, re, sys, time, tempfile, urllib.parse, urllib.request, urllib.error

from fetch_sfx import open_safe, safe_role

BASE = os.environ.get("MUAPI_BASE", "https://api.muapi.ai")
UA = {"User-Agent": "hunting-titles-studio/1.0", "Content-Type": "application/json"}
SIGNATURES = {
    ".png": lambda h: h.startswith(b"\x89PNG\r\n\x1a\n"),
    ".jpg": lambda h: h.startswith(b"\xff\xd8\xff"),
    ".jpeg": lambda h: h.startswith(b"\xff\xd8\xff"),
    ".webp": lambda h: h.startswith(b"RIFF") and h[8:12] == b"WEBP",
    ".mp4": lambda h: len(h) >= 12 and h[4:8] == b"ftyp",
}


def safe_model(model):
    """The model is a URL path segment: plain characters only, no '.', '..' or empty segments."""
    if not isinstance(model, str) or not re.fullmatch(r"[A-Za-z0-9._/-]{1,100}", model) or \
            any(part in ("", ".", "..") for part in model.split("/")):
        raise ValueError(f"unsafe model name: {model!r}")
    return model


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
    except (urllib.error.URLError, TimeoutError, ValueError) as e:  # network down, timeout, non-JSON reply
        raise SystemExit(f"gen_media: {method} {url} failed: {e}")


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
    # Download to a temporary file so failures never leave a corrupt final asset.
    destination = os.path.abspath(out)
    suffix = os.path.splitext(destination)[1].lower()
    if suffix not in SIGNATURES:
        raise SystemExit(f"gen_media: unsupported output extension: {suffix}")
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=os.path.dirname(destination), prefix=".media-", delete=False
        ) as f:
            tmp = f.name
            total = 0
            with open_safe(url, timeout=120) as response:  # https only, public hosts, safe redirects
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > 500 * 1024 * 1024:
                        raise ValueError("media download exceeds 500 MiB")
                    f.write(chunk)
        with open(tmp, "rb") as f:
            header = f.read(16)
        if not SIGNATURES[suffix](header):
            raise ValueError(f"download is not a valid {suffix} media container")
        os.replace(tmp, destination)
        tmp = None
    except (OSError, ValueError) as exc:
        raise SystemExit(f"gen_media: asset download failed: {exc}") from exc
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)
    meta = {"name": name, "model": model, "payload": payload, "request_id": res.get("request_id"), "source_url": url,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "provider": "MuAPI (via Open Generative AI API pattern)"}
    with open(out + ".json", "w", encoding="utf-8") as metadata_file:
        json.dump(meta, metadata_file, indent=1)
    print(f"{name}: {out}")
    return meta


def plan_jobs(a):
    """Validate everything before any network call; returns [(name, spec, out)]."""
    if a.batch:
        try:
            with open(a.batch, encoding="utf-8") as f:
                specs = json.load(f)
        except (OSError, ValueError) as e:
            raise ValueError(f"cannot read batch file {a.batch}: {e}")
        if not isinstance(specs, dict):
            raise ValueError("batch file must be a JSON object of {name: spec}")
        od, jobs = a.out_dir or ".", []
        for name, spec in specs.items():
            if name.startswith("_"): continue
            if not isinstance(spec, dict):
                raise ValueError(f"{name}: spec must be an object")
            ext = str(spec.get("ext", "png")).lower()
            if "." + ext not in SIGNATURES:
                raise ValueError(f"{name}: unsupported ext {ext!r}; use one of {sorted(s[1:] for s in SIGNATURES)}")
            safe_model(spec.get("model", "flux-krea-dev"))
            jobs.append((safe_role(name), {k: v for k, v in spec.items() if k != "ext"}, os.path.join(od, f"{name}.{ext}")))
        return jobs
    if not (a.prompt and a.out):
        raise ValueError("--prompt and --out are required (or use --batch)")
    if os.path.splitext(a.out)[1].lower() not in SIGNATURES:
        raise ValueError(f"unsupported output extension: {a.out}")
    spec = {"model": safe_model(a.model), "prompt": a.prompt, "aspect": a.aspect}
    if a.seed is not None: spec["seed"] = a.seed
    return [(os.path.basename(a.out), spec, a.out)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="flux-krea-dev"); ap.add_argument("--prompt"); ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--seed", type=int); ap.add_argument("--out")
    ap.add_argument("--batch"); ap.add_argument("--out-dir")
    ap.add_argument("--generate", action="store_true", help="really submit the paid MuAPI jobs (default: print the plan only)")
    ap.add_argument("--max-jobs", type=int, default=20, help="refuse to start when the plan has more jobs (default 20)")
    a = ap.parse_args(argv)
    if urllib.parse.urlsplit(BASE).scheme != "https":
        ap.error("MUAPI_BASE must be an https:// URL (the API key is sent to it)")
    try:
        jobs = plan_jobs(a)
    except ValueError as e:
        ap.error(str(e))
    print(f"gen_media: plan {len(jobs)} paid MuAPI job(s)")
    for name, spec, out in jobs:
        print(f"  [{name}] {spec.get('model', 'flux-krea-dev')} -> {out}")
    if len(jobs) > a.max_jobs:
        if a.generate:
            raise SystemExit(f"gen_media: plan has {len(jobs)} jobs, more than --max-jobs {a.max_jobs}; refusing to start.")
        print(f"note: {len(jobs)} jobs is more than --max-jobs {a.max_jobs}; raise it to run them all.")
    if not a.generate:
        print("dry run: nothing sent. Add --generate to submit (spends MuAPI credit).")
        return 0
    key = os.environ.get("MUAPI_KEY") or "proxy-injected"
    bal = balance(key)
    if bal <= 0:
        raise SystemExit("gen_media: MuAPI balance is $0 — generations would return placeholder samples. Top up at muapi.ai first.")
    print(f"gen_media: MuAPI balance ${bal:.2f}", file=sys.stderr)
    for name, spec, out in jobs:
        one(name, spec, out, key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
