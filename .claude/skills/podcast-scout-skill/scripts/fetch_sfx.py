#!/usr/bin/env python3
"""Fetch openly licensed recorded sound effects from Openverse (WordPress/openverse, api.openverse.org).

    python3 fetch_sfx.py sfx.json --out DIR [--per 4] [--license cc0]

sfx.json:  {"crowd": {"q": "stadium crowd cheer", "max_s": 20}, "paper": {"q": "paper slide"}, ...}

For each role it downloads up to --per candidates (shortest-first within max_s) as
DIR/<role>/<n>.<ext> and writes DIR/sources.json with title, creator, licence, licence URL and
landing page for every file — paste the used ones into CREDITS. Default licence filter is CC0
(no attribution needed); "by" also allows CC BY (attribution required). Never use NC/ND sounds
on a monetised channel. Pick between candidates by listening tools (earshot rank) — not by title.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

API = "https://api.openverse.org/v1/audio/"


def search(q, license_, n=20):
    params = {"q": q, "license": license_, "page_size": n, "mature": "false"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": "hunting-titles-studio/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("results", [])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec"); ap.add_argument("--out", required=True)
    ap.add_argument("--per", type=int, default=4); ap.add_argument("--license", default="cc0")
    a = ap.parse_args()
    spec = json.load(open(a.spec)); os.makedirs(a.out, exist_ok=True)
    sources = {}
    for role, s in spec.items():
        if role.startswith("_"): continue
        try:
            res = search(s["q"], a.license)
        except Exception as e:
            print(f"fetch_sfx: {role}: search failed ({e})", file=sys.stderr); continue
        max_ms = s.get("max_s", 12) * 1000
        res = [r for r in res if (r.get("duration") or 0) <= max_ms and r.get("url")]
        res.sort(key=lambda r: abs((r.get("duration") or 0) - s.get("ideal_s", 3) * 1000))
        os.makedirs(os.path.join(a.out, role), exist_ok=True)
        got = []
        for i, r in enumerate(res[: a.per]):
            ext = os.path.splitext(urllib.parse.urlparse(r["url"]).path)[1] or ".mp3"
            dst = os.path.join(a.out, role, f"{i}{ext}")
            try:
                req = urllib.request.Request(r["url"], headers={"User-Agent": "hunting-titles-studio/1.0"})
                with urllib.request.urlopen(req, timeout=60) as resp, open(dst, "wb") as f:
                    f.write(resp.read())
            except Exception as e:
                print(f"fetch_sfx: {role}/{i}: download failed ({e})", file=sys.stderr); continue
            got.append({"file": dst, "title": r.get("title"), "creator": r.get("creator"), "license": r.get("license"),
                        "license_version": r.get("license_version"), "license_url": r.get("license_url"),
                        "landing": r.get("foreign_landing_url"), "duration_s": (r.get("duration") or 0) / 1000})
            time.sleep(0.3)
        sources[role] = got
        print(f"{role:12s} {len(got)} files  ({s['q']})")
    json.dump(sources, open(os.path.join(a.out, "sources.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
