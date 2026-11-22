#!/usr/bin/env python3
"""Lint a YouTube upload package before the owner uploads it.

    python3 package_lint.py package.json [--duration SECONDS]

package.json:
    {"titles": ["You Read It. Can You Explain It?", "..."],
     "thumbnails": [{"title_index": 0, "text": "EXPLAIN IT?", "focal": "page turning into empty bubble"}],
     "description": "First two lines are the search snippet...\n...",
     "chapters": [["00:00", "The one-sentence test"], ["00:41", "Why rereading feels like learning"]],
     "tags": ["active recall", "..."],
     "pinned_comment": "optional",
     "sources": ["https://..."]}

Rules (FAIL = fix before upload, WARN = judgement call). Every video ships with a thumbnail, a title plus
alternatives, and a description with chapters and sources (owner rule):
  package     must be a readable JSON object (FAIL)
  titles      1-10 options (FAIL); <= 60 chars (FAIL >70); <= 2 ALL-CAPS words (WARN); no clickbait stock phrases (FAIL)
  thumbnails  at least one (FAIL); each an object with text <= 3 words (WARN 4-5, FAIL > 5); text must not repeat the
              title's words wholesale (WARN); a focal visual (WARN)
  description present (FAIL); first line <= 150 chars (WARN); every listed source appears in it (FAIL);
              no sources listed (FAIL)
  chapters    present (FAIL); first is 00:00, >= 3 chapters, each >= 10 s, increasing (FAIL); every stamp starts a
              line of the description (FAIL); titles <= 5 words (WARN)
  tags        strings (FAIL); <= 15 (WARN), no duplicates (WARN), total <= 500 chars (FAIL)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BANNED = ["you won't believe", "shocking", "gone wrong", "insane", "mind-blowing", "secret they don't",
          "this changes everything", "100% guaranteed", "doctors hate"]


STAMP = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]\d)$")


def secs(stamp) -> int | None:
    """'MM:SS' or 'H:MM:SS' → seconds; None when malformed (YouTube ignores bad stamps)."""
    m = STAMP.match(str(stamp).strip()) if isinstance(stamp, str) else None
    if not m:
        return None
    h, mm, ss = m.groups()
    return int(h or 0) * 3600 + int(mm) * 60 + int(ss)


def words(s):
    return re.findall(r"[A-Za-z0-9']+", s.lower())


def report(out):
    fails = [o for o in out if o[0] == "FAIL"]
    for lvl, area, msg in out:
        print(f"{lvl:4s}  {area:11s} {msg}")
    print(f"\n{'FAIL' if fails else 'PASS'}: {len(fails)} fail, {sum(o[0] == 'WARN' for o in out)} warn")
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("package")
    ap.add_argument("--duration", type=float, help="video length in seconds (checks last chapter)")
    a = ap.parse_args(argv)
    try:
        pkg = json.loads(Path(a.package).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return report([("FAIL", "package", f"cannot read {a.package} as JSON: {exc}")])
    if not isinstance(pkg, dict):
        return report([("FAIL", "package", "top level must be a JSON object")])
    out = []

    def add(level, area, msg):
        out.append((level, area, msg))

    titles = pkg.get("titles") or []
    if not isinstance(titles, list) or not titles:
        add("FAIL", "titles", "no titles"); titles = []
    elif len(titles) > 10:
        add("FAIL", "titles", f"{len(titles)} options (max 10)")
    clean = []
    for i, t in enumerate(titles):
        if not isinstance(t, str) or not t.strip():
            add("FAIL", "titles", f"[{i}] empty title")
        else:
            clean.append(t.strip())
    titles = clean
    for i, t in enumerate(titles):
        n = len(t)
        if n > 70:
            add("FAIL", "titles", f"[{i}] {n} chars (> 70 truncates everywhere): {t}")
        elif n > 60:
            add("WARN", "titles", f"[{i}] {n} chars (> 60 truncates on desktop search): {t}")
        caps = [w for w in re.findall(r"\b[A-Z]{2,}\b", t) if w not in {"AI", "DNA", "USA", "UK", "CEO", "NASA", "GDP", "ADHD"}]
        if len(caps) > 2:
            add("WARN", "titles", f"[{i}] {len(caps)} ALL-CAPS words")
        for b in BANNED:
            if b in t.lower():
                add("FAIL", "titles", f"[{i}] clickbait phrase '{b}' promises more than evidence can carry")
    if titles:
        add("OK", "titles", f"{len(titles)} options")

    thumbs = pkg.get("thumbnails") or []
    if not isinstance(thumbs, list) or not thumbs:
        add("FAIL", "thumbnail", "no thumbnails (every video ships with one)"); thumbs = []
    for i, th in enumerate(thumbs):
        if not isinstance(th, dict):
            add("FAIL", "thumbnail", f"[{i}] must be an object with text/title_index/focal"); continue
        text = th.get("text", "")
        if not isinstance(text, str):
            add("FAIL", "thumbnail", f"[{i}] text must be a string"); continue
        wc = len(words(text))
        if wc > 5:
            add("FAIL", "thumbnail", f"'{text}' has {wc} words (aim <= 3; unreadable on phones)")
        elif wc > 3:
            add("WARN", "thumbnail", f"'{text}' has {wc} words (aim <= 3)")
        ti = th.get("title_index")
        if ti is not None and not (type(ti) is int and 0 <= ti < len(titles)):
            add("FAIL", "thumbnail", f"title_index {ti!r} does not point at a title (0..{len(titles) - 1})")
        elif isinstance(ti, int) and text:
            tw, xw = set(words(titles[ti])), set(words(text))
            if xw and len(xw & tw) / len(xw) > 0.8:
                add("WARN", "thumbnail", f"'{text}' repeats title [{ti}]; the thumbnail should add a visual question")
        if not th.get("focal"):
            add("WARN", "thumbnail", "no focal visual described")

    desc = pkg.get("description", "")
    if not isinstance(desc, str):
        add("FAIL", "description", "must be a string"); desc = ""
    if not desc.strip():
        add("FAIL", "description", "missing"); desc = ""
    else:
        first = desc.strip().splitlines()[0]
        if len(first) > 150:
            add("WARN", "description", f"first line {len(first)} chars; only ~150 show in search")
    sources = pkg.get("sources") or []
    if not isinstance(sources, list) or not all(isinstance(s, str) and s.strip() for s in sources):
        add("FAIL", "sources", "sources must be a list of non-empty strings"); sources = []
    if not sources:
        add("FAIL", "sources", "no sources listed (owner rule: every description lists its sources)")
    missing = [s for s in sources if s.strip() not in desc]
    if desc and missing:
        add("FAIL", "description", f"{len(missing)} of {len(sources)} sources not listed: {', '.join(missing)}")

    ch = pkg.get("chapters") or []
    if not isinstance(ch, list):
        ch = [ch]   # reported below as one malformed chapter
    bad =[c for c in ch if not (isinstance(c, (list, tuple)) and len(c) == 2 and secs(c[0]) is not None
                                and isinstance(c[1], str) and c[1].strip())]
    for c in bad:
        add("FAIL", "chapters", f"malformed chapter {c!r} (need [\"MM:SS\", \"title\"])")
    ch = [c for c in ch if c not in bad]
    if ch:
        times = [secs(c[0]) for c in ch]
        if times[0] != 0:
            add("FAIL", "chapters", "first chapter must be 00:00")
        if len(ch) < 3:
            add("FAIL", "chapters", "YouTube needs >= 3 chapters")
        for i in range(1, len(times)):
            if times[i] <= times[i - 1]:
                add("FAIL", "chapters", f"chapter {i} not after previous")
            elif times[i] - times[i - 1] < 10:
                add("FAIL", "chapters", f"chapter {i - 1} shorter than 10 s")
        if a.duration and times and a.duration - times[-1] < 10:
            add("FAIL", "chapters", "last chapter shorter than 10 s")
        for t, title in ch:
            if len(title.split()) > 5:
                add("WARN", "chapters", f"'{title}' > 5 words")
        # YouTube reads chapters from stamps that start a description line; "0:00" must not match inside "10:00"
        listed = {secs(m) for m in re.findall(r"(?m)^[ \t]*((?:\d+:)?\d{1,2}:\d{2})(?![\d:])", desc)}
        if desc and not all(t in listed for t in times):
            add("FAIL", "chapters", "chapter stamps not all at the start of a description line (YouTube reads them from there)")
    elif not bad:
        add("FAIL", "chapters", "no chapters (every video's description ships with them)")

    tags = pkg.get("tags") or []
    if not isinstance(tags, list):
        add("FAIL", "tags", "tags must be a list"); tags = []
    if not all(isinstance(t, str) for t in tags):
        add("FAIL", "tags", "every tag must be a string"); tags = [t for t in tags if isinstance(t, str)]
    if len(tags) > 15:
        add("WARN", "tags", f"{len(tags)} tags (> 15 adds nothing)")
    if len(set(t.lower() for t in tags)) != len(tags):
        add("WARN", "tags", "duplicate tags")
    if sum(len(t) for t in tags) > 500:
        add("FAIL", "tags", "tags exceed 500 characters")
    return report(out)


if __name__ == "__main__":
    sys.exit(main())
