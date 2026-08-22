#!/usr/bin/env python3
"""Keep the retired tag URLs alive after the vocabulary consolidation.

Collapsing 357 tags into 57 retired 334 term pages. Rather than guess at
Hugo's slug rules, this reads the URLs the previous build actually published
(a sitemap dump), maps each one back through bin/retag.py's table, and writes
the alias onto the term page it merged into.

    python3 bin/gen-tag-aliases.py OLD_URLS.txt [--write]
"""
from __future__ import annotations

import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("retag", ROOT / "bin" / "retag.py")
retag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retag)


def slug(name: str) -> str:
    """Hugo's urlize, close enough for the tags this site actually uses."""
    s = name.strip().lower()
    s = re.sub(r"[\s/]+", "-", s)
    s = re.sub(r"[^\w一-鿿-]+", "", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def main(argv: list[str]) -> int:
    if not argv or argv[0].startswith("--"):
        print(__doc__)
        return 2
    old_urls = Path(argv[0]).read_text(encoding="utf-8").split()
    write = "--write" in argv

    # slug -> canonical key, for every tag name the corpus ever used.
    by_slug: dict[str, str] = {}
    for raw_lower, key in retag.MAP.items():
        by_slug.setdefault(slug(raw_lower), key)
    # The canonical labels themselves, so a surviving term is never aliased.
    live: dict[str, set[str]] = {"zh": set(), "en": set()}
    for zh, en, _ in retag.VOCAB.values():
        live["zh"].add(slug(zh))
        live["en"].add(slug(en))

    aliases: dict[tuple[str, str], list[str]] = defaultdict(list)
    unresolved: list[str] = []
    for url in old_urls:
        m = re.fullmatch(r"(?:/en)?/tags/([^/]+)/", url)
        if not m:
            continue
        lang = "en" if url.startswith("/en/") else "zh"
        s = slug(unquote(m.group(1)))
        if s in live[lang]:
            continue  # the term survived under its own name
        key = by_slug.get(s)
        if key is None:
            unresolved.append(url)
            continue
        aliases[(key, lang)].append(f"/tags/{unquote(m.group(1))}/")

    written = 0
    for key, (zh, en, _tier) in retag.VOCAB.items():
        for lang, label, suffix in (("zh", zh, "_index.md"), ("en", en, "_index.en.md")):
            got = sorted(set(aliases.get((key, lang), [])))
            if not got:
                continue
            target = ROOT / "content" / "tags" / slug(zh) / suffix
            body = "---\n"
            body += f"title: {label}\n"
            body += "# Terms merged into this one when the tag vocabulary was consolidated.\n"
            body += "aliases:\n"
            body += "".join(f'  - "{a}"\n' for a in got)
            body += "---\n"
            if write:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body, encoding="utf-8")
            written += 1

    verb = "wrote" if write else "would write"
    print(f"{verb} {written} term pages carrying "
          f"{sum(len(set(v)) for v in aliases.values())} aliases")
    if unresolved:
        print(f"unresolved ({len(unresolved)}):")
        for u in unresolved[:20]:
            print("   ", u)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
