#!/usr/bin/env python3
"""Turn Blowfish's data/authors/*.json into OINK `authors` taxonomy pages.

OINK renders an author profile from the term page itself, so the byline, the
avatar and the archive can never disagree with a parallel data file.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "authors"
OUT = ROOT / "content" / "authors"
ASSETS = ROOT / "assets"

LABELS = {
    "link": ("Website", "个人主页", "fa-solid fa-globe"),
    "email": ("Email", "邮箱", "fa-solid fa-envelope"),
    "github": ("GitHub", "GitHub", "fa-brands fa-github"),
    "gitlab": ("GitLab", "GitLab", "fa-brands fa-gitlab"),
    "twitter": ("X / Twitter", "X / Twitter", "fa-brands fa-x-twitter"),
    "linkedin": ("LinkedIn", "LinkedIn", "fa-brands fa-linkedin"),
    "medium": ("Medium", "Medium", "fa-brands fa-medium"),
    "discord": ("Discord", "Discord", "fa-brands fa-discord"),
    "telegram": ("Telegram", "Telegram", "fa-brands fa-telegram"),
    "mastodon": ("Mastodon", "Mastodon", "fa-brands fa-mastodon"),
    "bluesky": ("Bluesky", "Bluesky", "fa-brands fa-bluesky"),
}

SKIP = {"test"}


def links_markdown(social, lang):
    rows = []
    for entry in social or []:
        for kind, url in entry.items():
            label, label_zh, _ = LABELS.get(kind, (kind.title(), kind.title(), ""))
            rows.append(f"- [{label if lang == 'en' else label_zh}]({url})")
    return "\n".join(rows)


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def write(path: Path, body: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def main():
    written = 0
    for src in sorted(DATA.glob("*.json")):
        slug = src.stem
        if slug in SKIP:
            continue
        record = json.loads(src.read_text(encoding="utf-8"))
        name = record.get("name", slug)
        bio = record.get("bio", "").strip()
        image = record.get("image", "").strip()
        if image and not (ASSETS / image).exists():
            image = ""

        for lang, suffix in (("en", "_index.en.md"), ("zh", "_index.md")):
            target = OUT / slug / suffix
            if slug == "vonng" and target.exists():
                continue  # the site owner keeps his hand-written profile
            heading = "Elsewhere" if lang == "en" else "其他链接"
            front = [f"title: {yaml_quote(name)}"]
            if bio:
                front.append(f"description: {yaml_quote(bio)}")
            if image:
                front.append(f"images: [{image}]")
            links = links_markdown(record.get("social"), lang)
            body = f"---\n" + "\n".join(front) + "\n---\n"
            if links:
                body += f"\n## {heading}\n\n{links}\n"
            write(target, body)
            written += 1
    print(f"wrote {written} author profile pages")


if __name__ == "__main__":
    main()
