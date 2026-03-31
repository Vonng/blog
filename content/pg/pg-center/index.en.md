---
title: "pg.center: A Chinese Mirror of the PostgreSQL Website"
date: 2026-03-26
draft: true
author: |
  [Ruohang Feng](https://vonng.com)
summary: >
  pg.center is a full Chinese mirror of postgresql.org, including the homepage, docs, news, community pages, and developer resources, plus a newly translated PostgreSQL 18 manual.
tags: [PostgreSQL, Website, Documentation, Community]
---

One thing has always bothered me after all these years using PostgreSQL:
`postgresql.org` never had a Chinese edition.

For English-speaking users, the official site is a one-stop hub for project information, release notes, documentation, community events, and developer resources.
For the large PostgreSQL user base in China, the language barrier has always been there.

So I did the obvious thing:
**I forked the entire PostgreSQL website into Chinese.**

The domain is: **[pg.center](https://pg.center/)**.

![PG.center homepage](site-launch.webp)

That launch also includes something the ecosystem was still missing:
Chinese documentation for PostgreSQL 18.

![PostgreSQL 18 Chinese documentation](pg18-docs.webp)

------

## What Is Included

In short, pg.center is a full Chinese mirror of [postgresql.org](https://www.postgresql.org/).
This is not a handful of translated pages. The site's structure and content have both been localized end to end.

**Homepage**: project overview, current releases, recent community activity, and the Planet PostgreSQL feed, all in Chinese.

![PG.center homepage](homepage.webp)

**About**: what PostgreSQL is, why people use it, core features, project governance, and more than 130 supporting pages.
You no longer need to stand in front of a manager translating the English site by hand to explain why PostgreSQL is the right choice.

![About pages](about-pages.webp)

**Documentation**: this is the most important part.
`pg.center/docs` provides the official manuals for PostgreSQL 14 through 18.
The PostgreSQL 18.3 Chinese docs are a fully refreshed translation that cost me two weeks of Codex and Claude Max quota.

![Docs page and sidebar](docs-sidebar.png)

I also extended the sidebar with Chinese documentation links for major PostgreSQL ecosystem components, including Pigsty, PIG CLI, PostgreSQL extensions, Patroni, PgBouncer, pgBackRest, and `pg_exporter`.
That gives readers a single place to navigate the wider ecosystem.

**News, events, downloads, community, developers, support**: release announcements, community calendars, and security notices are all localized as well.
Information that previously required VPN access, or waiting for someone else to repost it, is now available directly in Chinese.

------

## Why Build This?

The PostgreSQL user base in China is already large, across internet companies, traditional enterprises, cloud vendors, and independent developers.
But the awkward reality is that many people use PostgreSQL for years without ever spending serious time on the official website.

The reason is simple:
it is all in English.

The official docs are one of the most underrated assets in the PostgreSQL world.
They are clear, broad, well-structured, and full of examples.
They cover everything from tutorials to internals, from SQL syntax to operations.
But because of the language barrier, many users fall back to search engines, blog posts, or ChatGPT, and the quality of those answers varies wildly.

There used to be a Chinese community site, `postgres.cn`, but it has not really been maintained and no longer reflects the current PostgreSQL ecosystem.
I had wanted to help modernize it, but at some point starting fresh was simply the cleaner path.

The goal of pg.center is straightforward:
**lower the barrier so Chinese-speaking users can access official PostgreSQL information at minimal cost.**

No VPN. No English hurdle. Open pg.center and read.

If this works, it can also serve as a first step toward rebuilding the Chinese PostgreSQL community around better source material.

------

## A Few Details

- The domain `pg.center` is easy to remember.
- The site structure mirrors `postgresql.org`, so if you already know the official navigation model, there is almost no learning curve.
- News and release information will keep syncing, and I plan to add scheduled RSS synchronization as well.
- The docs section also integrates key ecosystem components and extensions, and I plan to keep that maintained.
- There will be no junk ads. If you build PostgreSQL-related products, projects, services, or vendors, you are welcome to list them in the directory.

------

## Closing

I translated *DDIA*, built Pigsty, and wrote a long list of PostgreSQL technical articles.
The underlying motivation has always been the same:
**make good things easier to discover, easier to use, and easier to use well.**

A Chinese edition of the PostgreSQL website was a missing piece in that chain.
Now that piece exists.

If you find it useful, send it to someone who uses PostgreSQL.

------

> **[pg.center](https://pg.center/)**
> The PostgreSQL website in Chinese. Open it and use it. No VPN required. Kept up to date.
