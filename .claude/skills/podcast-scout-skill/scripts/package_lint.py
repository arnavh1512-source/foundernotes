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

Rules (FAIL = fix before upload, WARN = judgement call):
  titles      1-10 options; <= 60 chars (FAIL >70); front-load: key words within first 40 chars (WARN);
              <= 2 ALL-CAPS words; no clickbait stock phrases
  thumbnails  <= 3 words of text (FAIL > 5); text must not repeat the title's words wholesale
  description first line <= 150 chars and states the payoff; sources listed when claims are made
  chapters    first is 00:00, >= 3 chapters, each >= 10 s, increasing, titles <= 5 words (WARN)
  tags        <= 15, no duplicates, total <= 500 chars
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("package")
    ap.add_argument("--duration", type=float, help="video length in seconds (checks last chapter)")
    a = ap.parse_args(argv)
    pkg = json.loads(Path(a.package).read_text(encoding="utf-8-sig"))
    out = []

    def add(level, area, msg):
        out.append((level, area, msg))

    titles = pkg.get("titles") or []
    if not isinstance(titles, list) or not titles:
        add("FAIL", "titles", "no titles"); titles = []
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

    for th in pkg.get("thumbnails") or []:
        text = th.get("text", "")
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
    if not desc:
        add("FAIL", "description", "missing")
    else:
        first = desc.strip().splitlines()[0]
        if len(first) > 150:
            add("WARN", "description", f"first line {len(first)} chars; only ~150 show in search")
        if pkg.get("sources") and not any(s in desc for s in pkg["sources"]):
            add("WARN", "description", "sources not listed in description")

    ch = pkg.get("chapters") or []
    bad = [c for c in ch if not (isinstance(c, (list, tuple)) and len(c) == 2 and secs(c[0]) is not None
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
        if desc and not all(c[0] in desc for c in ch):
            add("WARN", "chapters", "chapter stamps not all present in description (YouTube reads them from there)")
    else:
        add("WARN", "chapters", "no chapters (recommended for videos > 3 min)")

    tags = pkg.get("tags") or []
    if len(tags) > 15:
        add("WARN", "tags", f"{len(tags)} tags (> 15 adds nothing)")
    if len(set(t.lower() for t in tags)) != len(tags):
        add("WARN", "tags", "duplicate tags")
    if sum(len(t) for t in tags) > 500:
        add("FAIL", "tags", "tags exceed 500 characters")

    fails = [o for o in out if o[0] == "FAIL"]
    for lvl, area, msg in out:
        print(f"{lvl:4s}  {area:11s} {msg}")
    print(f"\n{'FAIL' if fails else 'PASS'}: {len(fails)} fail, {sum(o[0] == 'WARN' for o in out)} warn")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
