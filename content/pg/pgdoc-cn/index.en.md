---
title: "Chinese Docs for Five PostgreSQL Versions Are Now Live"
date: 2026-03-27
draft: true
author: |
  [Ruohang Feng](https://vonng.com)
summary: >
  PG.center now provides Chinese documentation for PostgreSQL 18, 17, 16, 15, and 14, covering every major version still in active support.
tags: [PostgreSQL, Documentation, Translation]
---

Yesterday I launched [PG.center](https://pg.center/), a Chinese mirror of the PostgreSQL website. The response was immediate.

There was one obvious gap, though: at launch, the site only had Chinese docs for PostgreSQL 18. Versions 17, 16, 15, and 14 are all still within lifecycle support, but I had taken the lazy route and temporarily left those sections in English.

Today my Codex quota reset, so I burned through this week's allowance and finished the rest.
At this point, all five actively supported PostgreSQL major versions now have full Chinese documentation online:

- [PostgreSQL 18 Chinese Docs](https://pg.center/docs/18/index.html) (current latest major version)
- [PostgreSQL 17 Chinese Docs](https://pg.center/docs/17/index.html)
- [PostgreSQL 16 Chinese Docs](https://pg.center/docs/16/index.html)
- [PostgreSQL 15 Chinese Docs](https://pg.center/docs/15/index.html)
- [PostgreSQL 14 Chinese Docs](https://pg.center/docs/14/index.html)

Because PG 18 had already been translated carefully, the work for 17 through 14 was mostly incremental. Even so, it still took a full day and several review passes to get them into shape.

## About These Docs

The Chinese PostgreSQL community has organized volunteer translation efforts before, but timeliness was always the weak point. Sometimes a major version had been out for a year and the documentation still was not fully translated.

With AI, I think this problem is finally tractable.

I plan to maintain these docs continuously. Whenever PostgreSQL ships a minor release, I will sync the updates and keep the Chinese version current.

The hardest part was not the literal translation. It was establishing a stable terminology standard first.
We normalized a lot of core terms, for example translating "token" consistently as a standardized Chinese equivalent instead of letting terminology drift from page to page.
That terminology work matters. It is what keeps the docs coherent instead of turning them into a pile of individually translated pages.

The source will also be published on GitHub. If you spot anything awkward or incorrect, feel free to send corrections.

## More Than Translation

PostgreSQL's official docs have long been one of the best technical resources in the database world. They are still the best place to learn PostgreSQL seriously.

Now [PG.center](https://pg.center/) provides Chinese translations for every active PostgreSQL release, which should be a clear win for Chinese-speaking users.

I also added a product directory to the site and listed a number of PostgreSQL kernels and PG-based tools there. If you maintain a PostgreSQL-related utility that is not listed on the official site, you are welcome to register and submit it.

That is the update:
**Chinese docs for all five active PostgreSQL major versions are now live**, and you can read them on **[PG.center](https://pg.center/)**.

> Is there any selfish motive here? Sure, a little.
> Having this corpus available also makes it easier for me to build useful things later, such as a PostgreSQL knowledge base.
> But no, I am not going to plaster the site with low-grade ads.
> At most I might leave a small Pigsty link in some corner. That is about it.
