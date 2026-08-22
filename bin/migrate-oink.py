#!/usr/bin/env python3
"""Rewrite Blowfish front matter and shortcodes into their OINK equivalents.

Line-oriented on purpose: only the keys that actually change are touched, so
the diff stays reviewable and every untouched line keeps its original bytes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# Blowfish display switches with no OINK counterpart: the theme decides these.
DROP_KEYS = {
    "showDate", "showDateOnlyInArticle", "showDateUpdated", "showAuthor",
    "showAuthorBottom", "showAuthorsBadges", "showHero", "showEdit",
    "showTaxonomies", "showBreadcrumbs", "showRelatedContent", "showPagination",
    "showZenMode", "showViews", "showLikes", "showWordCount", "showSummary",
    "showSectionPages", "showHeadingAnchors", "showDraftLabel", "showTableOfContents",
    "heroStyle", "layoutBackgroundBlur", "cardView", "groupByYear",
    "hideFeatureImage", "featured", "math", "menu", "module", "sectionHero",
    "seriesOpened", "sharingLinks", "smartTOC",
}

RENAME = {
    "externalUrl": "manual_link",
    "series_order": "series_weight",
    "showLayoutSwitch": "blog_index_toggle",
}

VONNG_NAMES = {
    "冯若航", "vonng", "Vonng", "VONNG", "Ruohang Feng", "Feng Ruohang",
    "冯若航 @Vonng", "@Vonng",
}

KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")


def split_front_matter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    nl = text.find("\n", end + 1)
    if nl == -1:
        return text[4:end], ""
    return text[4:end], text[nl + 1:]


def unquote(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def parse_blocks(fm: str):
    """Split front matter into (key, [lines]) blocks, preserving raw lines."""
    blocks = []
    current = None
    for line in fm.split("\n"):
        m = KEY_RE.match(line)
        if m:
            current = [m.group(1), [line]]
            blocks.append(current)
        elif current is not None and (line.startswith((" ", "\t", "-")) or not line.strip()):
            current[1].append(line)
        else:  # stray line before any key
            blocks.append(["", [line]])
            current = None
    return blocks


def author_is_vonng(lines: list[str]) -> bool:
    joined = "\n".join(lines)
    body = joined.split(":", 1)[1]
    plain = unquote(body).strip()
    if plain in VONNG_NAMES:
        return True
    return "vonng.com" in joined.lower() or "@Vonng" in joined or "冯若航" in joined


def convert_front_matter(fm: str, path: Path) -> tuple[str, list[str]]:
    notes = []
    blocks = parse_blocks(fm)
    keys = {k for k, _ in blocks}
    out: list[list[str]] = []
    add_authors = False

    for key, lines in blocks:
        if key == "author":
            if "authors" in keys:
                continue  # an explicit authors list already carries the byline
            if author_is_vonng(lines):
                add_authors = True
                continue
            # A name the site never gave a profile: OINK renders `author` as-is.
            out.append(lines)
            continue

        if key == "featureimage":
            if "images" in keys:
                continue
            value = unquote(lines[0].split(":", 1)[1])
            out.append([f"images: [{value}]"])
            notes.append("featureimage -> images")
            continue

        if key == "showTableOfContents":
            if unquote(lines[0].split(":", 1)[1]).lower() == "false":
                out.append(["notoc: true"])
            continue

        if key == "showComments":
            value = unquote(lines[0].split(":", 1)[1]).lower()
            out.append([f"comments: {value}"])
            continue

        if key == "showReadingTime":
            value = unquote(lines[0].split(":", 1)[1]).lower()
            out.append([f"reading_time: {value}"])
            continue

        if key == "icon":
            value = unquote(lines[0].split(":", 1)[1]).strip()
            value = re.sub(r"\bfas\b", "fa-solid", value)
            value = re.sub(r"\bfab\b", "fa-brands", value)
            value = re.sub(r"\bfar\b", "fa-regular", value)
            out.append([f"icon: {value}"])
            continue

        if key in RENAME:
            rest = lines[0].split(":", 1)[1]
            renamed = [f"{RENAME[key]}:{rest}"] + lines[1:]
            out.append(renamed)
            continue

        if key in DROP_KEYS:
            continue

        out.append(lines)

    if add_authors:
        # Byline order is the front matter order, so the site author leads.
        insert_at = 0
        for i, lines in enumerate(out):
            m = KEY_RE.match(lines[0])
            if m and m.group(1) in ("title", "linkTitle", "date", "lastmod"):
                insert_at = i + 1
        out.insert(insert_at, ["authors: [vonng]"])
        notes.append("author -> authors: [vonng]")

    flat: list[str] = []
    for lines in out:
        flat.extend(lines)
    # Collapse the blank lines a removed block may leave behind.
    cleaned: list[str] = []
    for line in flat:
        if not line.strip() and (not cleaned or not cleaned[-1].strip()):
            continue
        cleaned.append(line)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return "\n".join(cleaned), notes


ALERT_OPEN = re.compile(
    r'^\{\{%\s*alert\s*(?P<attrs>.*?)\s*%\}\}\s*$')
ALERT_CLOSE = re.compile(r'^\{\{%\s*/\s*alert\s*%\}\}\s*$')
ATTR = re.compile(r'(\w+)="([^"]*)"')

COLOR_TO_TYPE = {
    "danger": "DANGER", "warning": "WARNING", "success": "SUCCESS",
    "info": "NOTE", "primary": "IMPORTANT", "secondary": "NOTE",
    "dark": "NOTE", "light": "NOTE",
}


def convert_body(body: str) -> tuple[str, list[str]]:
    notes = []
    lines = body.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Blowfish loaded KaTeX with a shortcode; OINK loads it from the
        # passthrough math the page actually contains.
        if re.match(r'^\s*\{\{<\s*katex\s*/?\s*>\}\}\s*$', line):
            notes.append("dropped katex shortcode")
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            continue

        # The year-grouped index shortcodes are replaced by the native blog index.
        if re.match(r'^\s*\{\{<\s*section_index[^>]*>\}\}\s*$', line):
            notes.append("dropped section_index shortcode")
            i += 1
            continue

        m = ALERT_OPEN.match(line)
        if m:
            attrs = dict(ATTR.findall(m.group("attrs")))
            kind = COLOR_TO_TYPE.get(attrs.get("color", "info"), "NOTE")
            title = attrs.get("title", "").strip()
            inner: list[str] = []
            i += 1
            while i < len(lines) and not ALERT_CLOSE.match(lines[i]):
                inner.append(lines[i])
                i += 1
            i += 1  # skip the closing tag
            while inner and not inner[0].strip():
                inner.pop(0)
            while inner and not inner[-1].strip():
                inner.pop()
            out.append(f"> [!{kind}]{(' ' + title) if title else ''}")
            for text in inner:
                out.append("> " + text if text.strip() else ">")
            notes.append(f"alert -> [!{kind}]")
            i_advanced = True
            continue

        out.append(line)
        i += 1
    return "\n".join(out), notes


def main(argv: list[str]) -> int:
    write = "--write" in argv
    changed = 0
    summary: dict[str, int] = {}
    for path in sorted(CONTENT.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        fm, body = split_front_matter(original)
        if fm is None:
            continue
        new_fm, fm_notes = convert_front_matter(fm, path)
        new_body, body_notes = convert_body(body)
        notes = fm_notes + body_notes
        rebuilt = f"---\n{new_fm}\n---\n{new_body}"
        if rebuilt != original:
            changed += 1
            for note in notes:
                summary[note] = summary.get(note, 0) + 1
            if write:
                path.write_text(rebuilt, encoding="utf-8")
    verb = "rewrote" if write else "would rewrite"
    print(f"{verb} {changed} files")
    for note, count in sorted(summary.items(), key=lambda kv: -kv[1]):
        print(f"  {count:5d}  {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
