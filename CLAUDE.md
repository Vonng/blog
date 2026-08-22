# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project overview

`vonng.com` is a bilingual (`zh-cn` default, `en` under `/en/`) Hugo blog about
PostgreSQL, databases, cloud-exit and AI. The theme is the
[**OINK**](https://oink.pgsty.com/) Hugo Module, pinned in `go.mod`; there is no
vendored theme directory and no Node.js toolchain.

## Commands

```bash
make dev      # hugo server on :1313
make build    # hugo --gc --minify --cleanDestinationDir
make check    # the strict build every change has to pass
make sync     # build, sanity-check for localhost URLs, rsync to the server
```

`make check` runs `hugo --printPathWarnings --panicOnWarning`. It must reach
`Total in …` with no WARN — a front matter typo, an unknown landing section and
a broken math expression all surface there.

`python3 bin/check_internal_links.py` resolves every internal Markdown link
against the generated `public/` tree; run it after moving or deleting a page.

## Structure

- `hugo.yaml` — the entire configuration: outputs, taxonomies, `params`, `params.ui`, and both languages with their own menus. There is no `config/` directory.
- `content/<column>/` — one top-level directory per blog column, ordered `db`, `cloud`, `pg`, `ai`, `pigsty`, `trip`, `misc` by `weight` (`misc` is titled 碎银). Each `_index.md` sets `type: blog`, cascades it, and carries a `profile:` block (`avatar`, `headline`) that `layouts/_partials/page-title.html` renders as the centred round-portrait opening. **Top-level directory names are the URLs and must not change.**
- `content/about/` — `layout: landing`, assembled from `data/landing/about/<lang>.yaml`.
- `content/tags/<term>/` — term pages that exist only to carry `aliases` for the tags merged into them; generated, not hand-written.
- `content/authors/<slug>/` — author profile pages. This is the `authors` taxonomy, and the only source of author identity; there is no `data/authors`.
- `content/dossier/` — `layout: dossier`, rendered by `layouts/dossier.html`.
- `data/home.yaml` — the whole home page, both languages: hero copy, column cards, project and publication grids, closing CTA. The only part not configured there is the `recent` list itself, which comes from the content tree.
- `data/landing/about/{zh-cn,en}.yaml` — the About page's sections.
- `data/footer/{zh-cn,en}.yaml` — the fat footer's link grid.
- `assets/scss/_variables_project.scss` / `_styles_project.scss` — the palette. Nothing else customizes appearance.
- `layouts/` — only what the theme does not provide:
  - `dossier.html`, `alias.html` — the two standalone page templates;
  - `_shortcodes/column_index.html` — the AI column's cross-section index;
  - `_partials/landing/sections/recent-posts.html` — the home page's recent-articles grid;
  - `_partials/landing/sections/hero-featured.html` — the home page's opening, painting `images` from `content/_index.md` full-bleed through the theme's own `featured_image: hero` resolver;
  - `_partials/landing/sections/link-cards.html` — the Projects and Publications grids: a 2:1 image, then title / eyebrow / description, the whole card a link;
  - `_partials/landing/sections/column-cards.html` — the home page's column cards. Each item names a column by content path and the partial reads the logo, link and live post count from that page, so a card cannot drift from the column it opens;
  - `_partials/page-title.html` — the column profile opening, falling through to the theme's heading everywhere else;
  - `_partials/shell/blog-card.html` — the theme's card with a 2:1 crop and no series badge;
  - `blog/list.html` — the theme's blog index, with the table form kept as a complete archive rather than narrowed to the current page when the form toggle is on.

## Writing a post

A post is a leaf bundle: `content/<column>/<slug>/index.md` plus its images,
with `index.en.md` beside it for the English version. Front matter that matters:

```yaml
title: 标题
date: 2026-01-01          # required; decides ordering and the RSS timestamp
authors: [vonng]          # the `authors` taxonomy; several names byline in order
summary: >                # card summary and meta description
  一句话摘要。
tags: [PostgreSQL]         # 1-4 from the fixed vocabulary, usually 2-3
```

### The tag vocabulary

Tags are a **closed vocabulary of 57 terms per language**, defined once in
`bin/retag.py` (`VOCAB`) and paired zh↔en so the two term trees mirror each
other. A translated pair carries the same tags in its own language.

Rules when tagging a new post:

- One to four tags, usually two or three. `bin/retag.py` enforces the cap by
  tier: tier 1 is the subject (PostgreSQL, AI, 下云), tier 2 the craft or
  domain (PG管理, 监控, 故障复盘), tier 3 the register (开源, 技术评论, 翻译).
- **Do not invent a tag.** If nothing in the vocabulary fits, add it to
  `VOCAB` with both labels and a tier, add its aliases, and re-run the script
  — do not leave a one-off term in one post's front matter.
- `python3 bin/retag.py` reports without writing and lists anything it cannot
  map; `--write` applies. It is idempotent and safe to re-run.
- Retired terms keep their old URLs: `content/tags/<term>/_index.md` carries
  the `aliases` list, generated by `bin/gen-tag-aliases.py` from a dump of the
  previously published URLs.

Put a `featured.jpg` (or `.webp`) in the bundle and it becomes the card
thumbnail, the share card, and the article's full-bleed Hero — no front matter
needed. `images: []` opts a post out.

Column presentation is a site-wide decision in `params.ui`
(`featured_image: hero`, `blog_index: cards`, `toc_style: flow`,
`sidebar_enabled: false`); do not repeat it per page. Card thumbnails are
cropped to 2.35:1 — the crop is in `layouts/_partials/shell/blog-card.html`
and the matching frame is in `assets/scss/_styles_project.scss`; changing one
without the other leaves unprocessable images (SVG, static, remote) at the
wrong ratio.

## The home page

`data/home.yaml` holds both languages under `zh-cn:` and `en:`, each listing
six sections: `hero`, the six `columns` cards, `recent` posts, `project`,
`publication`, and the closing `cta`. Four of them render through the site's
own partials named in the `partial` key — adding a section type the theme does
not have needs a partial under `layouts/_partials/landing/sections/` and
nothing else.

A column card takes `page` (a content path), `title`, `subtitle` and `desc`.
The convention across the site is that the title is in the page's language and
the subtitle is the same name in the other one.

## Page width

`params.page_width: wide` is the site default, so every list surface — column
indexes, tag, category, series and author pages — uses the wide shell. Articles
read at the standard measure instead, and each column's `_index.md` does that
with two keys:

```yaml
page_width: wide          # this index
cascade:
  page_width: normal      # every post under it
```

Hugo's cascade applies to the node itself as well as its descendants, so the
index needs its own key to win its width back. Landing pages ignore
`page_width` entirely; they size through `.td-site-container`.

## Components

Use OINK's Markdown-native components, not shortcodes from the old theme:
`> [!NOTE]` callouts, ```` ```mermaid ```` diagrams, `{.cards}` link grids,
`{{< cards >}}` / `{{< card >}}` for cards with icons and images, and `$…$` /
`$$…$$` for math (rendered at build time, so a KaTeX syntax error is a build
warning). The full catalog is at https://oink.pgsty.com/docs/components/.

## Deployment

`make sync` rsyncs `public/` to `jp:/data/web/vonng.com/`. Comments use giscus
against `Vonng/vonng.com` Discussions with giscus's own built-in themes, so the
production host needs no CORS header for them.
