#!/usr/bin/env python3
"""Check and optionally fix dead internal Markdown links under content/.

Workflow:
1. Build route map from generated Hugo public/ directory.
2. Extract Markdown inline links from content/*.md (exclude image links).
3. Resolve relative links against source page URL, then check if route exists.
4. Optionally apply safe rewrite rules:
   - /blog/...    -> /...
   - /en/blog/... -> /en/...
   - /cloud/oss   -> /cloud/s3

Usage:
  python3 bin/check_internal_links.py
  python3 bin/check_internal_links.py --fix
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlsplit, urlunsplit


LANG_SUFFIX_RE = re.compile(r"^(?P<name>.+?)\.(?P<lang>[a-z]{2}(?:-[a-z]{2})?)\.md$", re.IGNORECASE)
MD_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")
MD_IMAGE_LINK_RE = re.compile(r"\[\!\[[^\]]*\]\([^)]+\)\]\(([^)]+)\)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

# Skip asset-like targets for dead-page checks.
ASSET_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tgz",
    ".bz2",
    ".xz",
    ".mp4",
    ".mov",
    ".avi",
    ".webm",
    ".mp3",
    ".wav",
    ".csv",
    ".sql",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".txt",
    ".js",
    ".css",
    ".woff",
    ".woff2",
    ".ttf",
}


@dataclass(frozen=True)
class LinkOccurrence:
    file: Path
    line: int
    target_raw: str
    target_url: str
    resolved_path: str
    base_url: str


@dataclass(frozen=True)
class BrokenLink:
    occurrence: LinkOccurrence


@dataclass(frozen=True)
class SuggestedFix:
    old: str
    new: str
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check internal dead links in content markdown")
    parser.add_argument("--content-dir", default="content", help="content directory")
    parser.add_argument("--public-dir", default="public", help="Hugo public output directory")
    parser.add_argument("--fix", action="store_true", help="apply safe automatic fixes")
    parser.add_argument(
        "--fix-docs-domain",
        action="store_true",
        help="also rewrite /docs style dead links to verified pigsty.cc/pigsty.io URLs",
    )
    parser.add_argument("--verbose", action="store_true", help="print all broken links")
    return parser.parse_args()


def build_valid_routes(public_dir: Path) -> Set[str]:
    routes: Set[str] = set()

    # Directory-style pages from index.html.
    for html in public_dir.rglob("index.html"):
        rel = "/" + html.relative_to(public_dir).as_posix()
        dirname = rel[: -len("index.html")]
        routes.add(dirname)
        if dirname != "/" and dirname.endswith("/"):
            routes.add(dirname[:-1])

    # Fallback for standalone html pages.
    for html in public_dir.rglob("*.html"):
        rel = "/" + html.relative_to(public_dir).as_posix()
        routes.add(rel)
        if not rel.endswith("/index.html"):
            routes.add(rel[: -len(".html")])

    return routes


def split_target_and_title(raw_target: str) -> Tuple[str, str]:
    """Split markdown target into URL part and optional title suffix.

    Example: /foo "bar"  -> (/foo,  "bar")
    """
    target = raw_target.strip()
    if not target or target.startswith("<"):
        return target.strip("<>"), ""

    if " " not in target:
        return target.strip("<>"), ""

    first, rest = target.split(" ", 1)
    if first.startswith(("/", "./", "../", "http://", "https://")) or not SCHEME_RE.match(first):
        return first.strip("<>"), " " + rest

    return target.strip("<>"), ""


def is_internal_candidate(target_url: str) -> bool:
    if not target_url:
        return False
    if target_url.startswith("#"):
        return False
    if target_url.startswith("{{") or target_url.startswith("{%"):
        return False
    if SCHEME_RE.match(target_url):
        # http(s) treated as external for this checker.
        return False
    return True


def is_asset_path(path: str) -> bool:
    name = Path(path.lower()).name
    if "." not in name:
        return False
    ext = "." + name.split(".")[-1]
    return ext in ASSET_EXTENSIONS


def source_page_base_url(md_file: Path, content_dir: Path) -> str:
    rel = md_file.relative_to(content_dir).as_posix()
    lang = "zh-cn"

    match = LANG_SUFFIX_RE.match(rel)
    if match:
        rel = match.group("name") + ".md"
        lang = match.group("lang").lower()

    stem = rel[: -len(".md")]
    if stem in {"index", "_index"}:
        base = "/"
    elif stem.endswith("/index"):
        base = "/" + stem[: -len("/index")].strip("/") + "/"
    elif stem.endswith("/_index"):
        base = "/" + stem[: -len("/_index")].strip("/") + "/"
    else:
        base = "/" + stem.strip("/") + "/"

    if lang == "en":
        return "/en/" if base == "/" else "/en" + base
    return base


def normalize_path(path: str) -> str:
    cleaned = re.sub(r"/+", "/", path)
    if not cleaned.startswith("/"):
        cleaned = "/" + cleaned
    return cleaned


def route_exists(path: str, valid_routes: Set[str]) -> bool:
    if path in valid_routes:
        return True
    if path != "/" and path.endswith("/") and path[:-1] in valid_routes:
        return True
    if path != "/" and not path.endswith("/") and path + "/" in valid_routes:
        return True
    return False


def find_line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def iter_markdown_links(md_file: Path) -> Iterable[Tuple[int, str, str, int]]:
    """Yield (line, raw_target, url_part, match_index)."""
    text = md_file.read_text(encoding="utf-8", errors="ignore")
    # 1) Handle [![img](...)](target) first (outer link target).
    covered: List[Tuple[int, int]] = []
    for match in MD_IMAGE_LINK_RE.finditer(text):
        covered.append((match.start(), match.end()))
        raw = match.group(1).strip()
        if not raw:
            continue
        url_part, _title = split_target_and_title(raw)
        line = find_line_number(text, match.start(1))
        yield line, raw, url_part, match.start(1)

    # 2) Handle normal links, skip matches inside nested image-link spans.
    for match in MD_LINK_RE.finditer(text):
        start = match.start()
        if any(lo <= start < hi for lo, hi in covered):
            continue
        raw = match.group(1).strip()
        if not raw:
            continue
        url_part, _title = split_target_and_title(raw)
        line = find_line_number(text, match.start(1))
        yield line, raw, url_part, match.start(1)


def collect_broken_links(content_dir: Path, valid_routes: Set[str]) -> List[BrokenLink]:
    broken: List[BrokenLink] = []

    for md_file in sorted(content_dir.rglob("*.md")):
        base = source_page_base_url(md_file, content_dir)

        for line, raw_target, target_url, _pos in iter_markdown_links(md_file):
            if not is_internal_candidate(target_url):
                continue

            parts = urlsplit(target_url)
            path = parts.path
            if not path:
                continue
            if is_asset_path(path):
                continue

            if path.startswith("/"):
                resolved = normalize_path(path)
            else:
                resolved = normalize_path(urlsplit(urljoin(base, path)).path)

            if route_exists(resolved, valid_routes):
                continue

            broken.append(
                BrokenLink(
                    occurrence=LinkOccurrence(
                        file=md_file,
                        line=line,
                        target_raw=raw_target,
                        target_url=target_url,
                        resolved_path=resolved,
                        base_url=base,
                    )
                )
            )

    return broken


def remote_url_ok(url: str, cache: Dict[str, bool], timeout: float = 8.0) -> bool:
    if url in cache:
        return cache[url]

    request = Request(url, headers={"User-Agent": "internal-link-checker/1.0"})
    ok = False
    try:
        with urlopen(request, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            ok = 200 <= int(status) < 400
    except HTTPError as exc:
        ok = 200 <= int(exc.code) < 400
    except URLError:
        ok = False
    except Exception:
        ok = False

    cache[url] = ok
    return ok


def normalize_docs_path(path: str) -> Optional[str]:
    if path.startswith("/docs/"):
        return path
    if path.startswith("/zh/docs/"):
        return "/docs/" + path[len("/zh/docs/") :]
    if path.startswith("/en/docs/"):
        return "/docs/" + path[len("/en/docs/") :]
    return None


def suggest_docs_domain_fix(
    target_url: str,
    path: str,
    remote_cache: Dict[str, bool],
) -> Optional[SuggestedFix]:
    normalized = normalize_docs_path(path)
    if not normalized:
        return None

    parts = urlsplit(target_url)
    # Order matters: zh/doc-like URLs usually map better to pigsty.cc.
    candidates = [
        "https://pigsty.cc" + normalized,
        "https://pigsty.io" + normalized,
    ]
    if path.startswith("/en/docs/"):
        candidates = [candidates[1], candidates[0]]

    for base_url in candidates:
        check_url = urlunsplit((urlsplit(base_url).scheme, urlsplit(base_url).netloc, urlsplit(base_url).path, "", ""))
        if not remote_url_ok(check_url, remote_cache):
            continue
        new_target = urlunsplit(
            (urlsplit(base_url).scheme, urlsplit(base_url).netloc, urlsplit(base_url).path, parts.query, parts.fragment)
        )
        if new_target == target_url:
            return None
        return SuggestedFix(old=target_url, new=new_target, reason="rewrite /docs link to verified docs site")
    return None


def suggest_fix(
    target_url: str,
    resolved_path: str,
    valid_routes: Set[str],
    fix_docs_domain: bool,
    remote_cache: Dict[str, bool],
) -> Optional[SuggestedFix]:
    """Return a safe deterministic suggestion for raw target_url."""

    parts = urlsplit(target_url)
    path = normalize_path(parts.path)

    candidate_path: Optional[str] = None
    reason = ""

    if path.startswith("/en/blog/"):
        candidate_path = "/en/" + path[len("/en/blog/") :]
        reason = "drop /en/blog prefix"
    elif path.startswith("/blog/"):
        candidate_path = "/" + path[len("/blog/") :]
        reason = "drop /blog prefix"
    elif path == "/cloud/oss" or path.startswith("/cloud/oss/"):
        candidate_path = "/cloud/s3" + path[len("/cloud/oss") :]
        reason = "rename cloud oss slug to s3"

    if not candidate_path:
        if fix_docs_domain:
            return suggest_docs_domain_fix(target_url, path, remote_cache)
        return None
    if not route_exists(candidate_path, valid_routes):
        if fix_docs_domain:
            return suggest_docs_domain_fix(target_url, path, remote_cache)
        return None

    new_parts = (
        parts.scheme,
        parts.netloc,
        candidate_path,
        parts.query,
        parts.fragment,
    )
    new_target = urlunsplit(new_parts)
    if new_target == target_url:
        return None

    return SuggestedFix(old=target_url, new=new_target, reason=reason)


def build_suggestion_map(
    broken_links: Sequence[BrokenLink],
    valid_routes: Set[str],
    fix_docs_domain: bool,
) -> Dict[str, SuggestedFix]:
    suggestions: Dict[str, SuggestedFix] = {}
    remote_cache: Dict[str, bool] = {}
    for item in broken_links:
        suggestion = suggest_fix(
            item.occurrence.target_url,
            item.occurrence.resolved_path,
            valid_routes,
            fix_docs_domain,
            remote_cache,
        )
        if suggestion:
            suggestions[item.occurrence.target_url] = suggestion
    return suggestions


def apply_fixes(content_dir: Path, suggestions: Dict[str, SuggestedFix]) -> Tuple[int, int]:
    """Apply fixes to markdown files. Returns (files_changed, replacements)."""
    files_changed = 0
    replacements = 0

    for md_file in sorted(content_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        changed = False

        def replace_match(match: re.Match[str]) -> str:
            nonlocal changed, replacements
            raw_target = match.group(1)
            url_part, title_suffix = split_target_and_title(raw_target)
            suggestion = suggestions.get(url_part)
            if not suggestion:
                return match.group(0)

            changed = True
            replacements += 1
            new_target = suggestion.new + title_suffix
            return match.group(0)[: match.group(0).find("(") + 1] + new_target + ")"

        new_text = MD_LINK_RE.sub(replace_match, text)
        if changed and new_text != text:
            md_file.write_text(new_text, encoding="utf-8")
            files_changed += 1

    return files_changed, replacements


def print_summary(
    broken_links: Sequence[BrokenLink],
    suggestions: Dict[str, SuggestedFix],
    verbose: bool,
) -> None:
    unique_targets = sorted({b.occurrence.resolved_path for b in broken_links})
    print(f"broken_link_occurrences={len(broken_links)}")
    print(f"broken_unique_targets={len(unique_targets)}")
    print(f"auto_fixable_targets={len(suggestions)}")

    if verbose:
        for item in broken_links:
            occ = item.occurrence
            print(
                f"{occ.file}:{occ.line}\t{occ.target_url}\t=> {occ.resolved_path}"
            )
    else:
        # Print compact top list.
        counts: Dict[str, int] = {}
        first_example: Dict[str, Tuple[Path, int, str]] = {}
        for item in broken_links:
            key = item.occurrence.resolved_path
            counts[key] = counts.get(key, 0) + 1
            first_example.setdefault(
                key,
                (item.occurrence.file, item.occurrence.line, item.occurrence.target_url),
            )

        for path, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:60]:
            file, line, target = first_example[path]
            print(f"{count:3d} {path}\t<- {target} ({file}:{line})")


def main() -> int:
    args = parse_args()

    repo_root = Path.cwd()
    content_dir = (repo_root / args.content_dir).resolve()
    public_dir = (repo_root / args.public_dir).resolve()

    if not content_dir.exists():
        print(f"content directory not found: {content_dir}")
        return 2
    if not public_dir.exists():
        print(f"public directory not found: {public_dir}")
        print("hint: run `hugo` first")
        return 2

    valid_routes = build_valid_routes(public_dir)
    broken_links = collect_broken_links(content_dir, valid_routes)
    suggestions = build_suggestion_map(broken_links, valid_routes, args.fix_docs_domain)

    if args.fix and suggestions:
        files_changed, replacements = apply_fixes(content_dir, suggestions)
        print(f"applied_fixes_files={files_changed}")
        print(f"applied_fixes_replacements={replacements}")

        # Re-scan after rewrite.
        broken_links = collect_broken_links(content_dir, valid_routes)
        suggestions = build_suggestion_map(broken_links, valid_routes, args.fix_docs_domain)

    print_summary(broken_links, suggestions, args.verbose)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
