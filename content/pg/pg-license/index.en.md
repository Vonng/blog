---
title: "Will PostgreSQL Change Its Open Source License?"
date: 2024-03-20
hero: /hero/vector-json-pg.jpg
author: |
  [Jonathan Katz](https://jkatz05.com/post/postgres/) | Translated by: [Feng Ruohang (Vonng)](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [Original English Article](https://jkatz05.com/post/postgres/postgres-license-2024/) | [Original Chinese WeChat Article]()
summary: |
  PostgreSQL will not change its license
tags: [PostgreSQL, PG Ecosystem, Open Source]
---

> Author: [Jonathan Katz](https://jkatz05.com/post/postgres/), PostgreSQL Core Team member (1 of 7), AWS RDS Principal Product Manager
>
> Translator: [Feng Ruohang (Vonng)](https://vonng.com), PostgreSQL Expert, Author of Free RDS PG Alternative — Pigsty

-----------

## Will PostgreSQL Change Its Open Source License?

> Disclaimer: I'm a member of the [PostgreSQL Core Team](https://www.postgresql.org/developer/core/), but the content of this article represents my personal views and not official PostgreSQL statements... **unless I provide links to official statements**;

Today I learned that the [Redis project will no longer be released under an open source license](https://redis.com/blog/redis-adopts-dual-source-available-licensing/), and I feel very sorry. There are two reasons: first, as a long-time Redis user and early adopter, and second, as an open source contributor. I must say I deeply empathize with the challenges of open source commercialization — especially having stood in diametrically opposed camps (translator's note: the author is also AWS RDS Principal Product Manager). I'm also aware of the downstream impact these changes can have, potentially completely disrupting how users adopt and use technology.

Whenever there are major changes in the open source licensing field, especially in databases and related systems (MySQL => Sun => Oracle is the first that comes to mind), I always hear the question: "Will PostgreSQL change its license?"

PostgreSQL's website actually [has an answer](https://www.postgresql.org/about/licence/):

> Will PostgreSQL ever be released under a different license? The PostgreSQL Global Development Group remains committed to making PostgreSQL available as free and open source software in perpetuity. There are no plans to change the PostgreSQL License or release PostgreSQL under a different license.

> Disclaimer: I did indeed participate in writing the above paragraph

The [PostgreSQL License](https://www.postgresql.org/about/licence/) (also called "**License**" — [Dave Page](https://pgsnake.blogspot.com/) and I have interesting back-and-forth debates about this term) is an [Open Source Initiative (OSI) approved license](https://opensource.org/license/postgresql), using a very permissive licensing model. As for which license it most resembles, I recommend reading [this email Tom Lane wrote in 2009](https://www.postgresql.org/message-id/1776.1256525282@sss.pgh.pa.us) (gist: closer to MIT license, calling it BSD is also fine).

Even so, there are still reasons why PostgreSQL won't change its license:

- The license is literally called the "[PostgreSQL License](https://www.postgresql.org/about/licence/)" — when you've named a license after your project, why change it?
- The PostgreSQL project started with open source community collaboration as its purpose, **intended to prevent any single entity from controlling this project**. This has continued as the project's spiritual tenet for nearly thirty years and is clearly reflected in the project [policies](https://www.postgresql.org/about/policies/).
- [Dave Page explicitly stated this in this email](https://www.postgresql.org/message-id/937d27e10910260840s1d28aab2o799f2c58d14dfb1e@mail.gmail.com) 😊

So the real question becomes, **what reason would PostgreSQL have to change its license?** Usually license changes happen for business decisions — but it seems the business around PostgreSQL is as robust as its feature set. Vonng recently [wrote a blog post](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4) highlighting the software and business ecosystem built around PostgreSQL, and that's just a part of it.

I say "just a part" because historically and currently, there are even more projects and businesses built around some portions of the PostgreSQL codebase. Many of these projects are released under different licenses or are simply closed source. But they also directly or indirectly promote PostgreSQL adoption and make the PostgreSQL protocol ubiquitous.

But the biggest reason PostgreSQL won't change its license is that it would be detrimental to all PostgreSQL users. Building trust in a technology takes a long time, especially when that technology is often used for the most critical part of applications: data storage and retrieval. [PostgreSQL has earned an excellent reputation — with its proven architecture, reliability, data integrity, powerful feature set, extensibility, and the dedicated open source community behind it, consistently delivering high-quality, innovative solutions](https://www.postgresql.org/about/). Changing PostgreSQL's license would destroy all the goodwill the project has built up over nearly thirty years.

While the PostgreSQL project certainly has imperfections (I certainly contribute to those imperfections too), the PostgreSQL License is truly a gift to the PostgreSQL community and the entire open source world, and we will continue to cherish and help keep PostgreSQL truly free and open source. After all, [the website says so too](https://www.postgresql.org/about/licence/) ;)

------

## Translator Commentary

I feel very honored to be mentioned and recommended by a PostgreSQL Global Community Core Team member. The article Jonathan mentioned is "[PostgreSQL Is Eating The Database World](https://mp.weixin.qq.com/s/8_uhRH93oAoHZqoC90DA6g)," with the English version "[PostgreSQL is Eating The Database World](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4)." Published on Medium: https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4, it sparked quite heated discussions on HackerNews, X, and LinkedIn.

Redis changing its license agreement is another milestone event in the open source software field — with this, all leading NoSQL databases, including MongoDB, ElasticSearch, and now Redis, have switched to SSPL — a license not recognized by OSI.

The core reason Redis switched to the more restrictive SSPL license, in the words of Redis Labs CEO, is: "**For years, we've been like fools while they made a fortune with what we developed**." Who are "they"? — **Public clouds**. The purpose of switching to SSPL is to try to use legal tools to prevent these cloud vendors from freeloading off open source, to become decent community participants, and to open source and give back to the community the management, monitoring, hosting and other aspects of their software.

Unfortunately, you can force a company to provide source code for their GPL/SSPL derivative software projects, but you can't force them to be good citizens of the open source community. Public clouds often scoff at such licenses, with most cloud vendors simply refusing to use AGPL licensed software: either using alternative implementations with more permissive licenses, reimplementing necessary functionality themselves, or directly purchasing commercial licenses without copyright restrictions.

When Redis announced its license change, AWS employees immediately jumped out to fork Redis — "Redis is no longer open source, our fork is truly open source!" Then AWS CTO came out to applaud, hypocritically saying: this is our employees' personal behavior — it's like a real-life version of killing someone and destroying their heart. The same thing has happened several times before, like forking ElasticSearch to create OpenSearch, and forking MongoDB to create DocumentDB.

Because it introduces additional restrictions and so-called "discriminatory" clauses, OSI has not recognized SSPL as an open source license. Therefore, using SSPL is interpreted as — "Redis is no longer open source," while cloud vendors' various forks are "open source." From a legal tool perspective, this is valid. But from naive moral sentiment, such statements are extremely unjust smearing and humiliation for Redis.

As Teacher Luo Xiang said: Legal tool judgments can never transcend community members' naive moral sentiments. If Xiehe and West China aren't top-tier hospitals, then it's not these hospitals that lose face, but the top-tier standard. If game of the year isn't Witcher 3, Breath of the Wild, or Baldur's Gate, then it's not these developers that lose face, but the rating agencies. If Redis is no longer considered "open source," what should really feel ashamed is OSI and the open source concept itself.

More and more well-known open source software is starting to switch to licenses hostile to cloud vendor freeloading. Not just Redis, MongoDB, and ElasticSearch — ElasticSearch also changed from Apache 2.0 to SSL and ElasticSearch in 2021, well-known open source software MinIO and Grafana switched from Apache v2 license to AGPLv3 license in 2020 and 2021 respectively.

Some old open source projects like PostgreSQL, as Jonathan said, have historical deposits (thirty years of reputation!) that make them factually unable to change open source licenses. But we can see many new powerful PostgreSQL extension plugins starting to use AGPLv3 as the default open source license, rather than previously defaulting to BSD-like/PostgreSQL-friendly licenses. For example, distributed extension Citus, columnar extension Hydra, ES full-text search alternative extension BM25, OLAP acceleration component PG Analytics... etc. Including our own PostgreSQL distribution Pigsty, which also switched from Apache license to AGPLv3 license when moving to 2.0, all with similar motivations behind them — counterattacking against software freedom's greatest enemy — cloud vendors.

In practice of resisting cloud vendor freeloading, license modification is the most common approach: but AGPLv3 is too strict and easily hurts both enemy and ally, while SSPL is not considered open source because it explicitly expresses this enemy-ally discrimination. The industry needs a new discriminatory software license agreement to achieve the effect of legitimately distinguishing between enemy and ally. Using dual licenses for clear boundary differentiation is also becoming a mainstream open source commercialization practice.

What's truly important has always been software freedom, and "open source" is just one means to achieve software freedom. If the "open source" concept cannot adapt to the needs of struggle in the new stage, and even hinders software freedom, it will likewise become outdated and no longer important, eventually being replaced by new concepts and practices — like "local-first."

------

## Original English Text

### WILL POSTGRESQL EVER CHANGE ITS LICENSE?

(Disclosure: I'm on the [PostgreSQL Core Team](https://www.postgresql.org/developer/core/), but what's written in this post are my personal views and not official project statements…unless I link to something that's an official project statement ;)

I was very sad to learn today that the [Redis project will no longer be released under an open source license](https://redis.com/blog/redis-adopts-dual-source-available-licensing/). Sad for two reasons: as a longtime Redis user and pretty early adopter, and as an open source contributor. I'll preface that I'm empathetic to the challenges of building businesses around open source, having been on multiple sides of this equation. I'm also cognizant of the downstream effects of these changes that can completely flip how a user adopts and uses a piece of technology.

Whenever there's a shakeup in open source licensing, particularly amongst databases and related systems (MySQL => Sun => Oracle being the one that first springs to mind), I'll hear the question "Will PostgreSQL ever change its license?"

The PostgreSQL website [has an answer](https://www.postgresql.org/about/licence/):

> Will PostgreSQL ever be released under a different license? The PostgreSQL Global Development Group remains committed to making PostgreSQL available as free and open > source software in perpetuity. There are no plans to change the PostgreSQL License or release PostgreSQL under a different license.

(Disclosure: I did help write the above paragraph).

[The PostgreSQL Licence](https://www.postgresql.org/about/licence/) (aka "License" – [Dave Page](https://pgsnake.blogspot.com/) and I have fun going back and forth on this) is an [Open Source Initiative (OSI) recognized license](https://opensource.org/license/postgresql), and has a very permissive model. In terms of which license it's most similar to, I defer to this email that [Tom Lane wrote in 2009](https://www.postgresql.org/message-id/1776.1256525282@sss.pgh.pa.us).

That said, there are a few reasons why PostgreSQL won't change it's license:

- It's "[The PostgreSQL Licence](https://www.postgresql.org/about/licence/)" – why change license when you have it named after the project?
- The PostgreSQL Project began as a collaborative open source effort and is set up to prevent a single entity to take control. This carries through in the project's ethos almost 30 years later, and is even codified throughout the [project policies](https://www.postgresql.org/about/policies/).
- [Dave Page explicitly said so in this email](https://www.postgresql.org/message-id/937d27e10910260840s1d28aab2o799f2c58d14dfb1e@mail.gmail.com) :)

The question then becomes - is there a reason that PostgreSQL would change its license? Typically these changes happen as part of a business decision - but it seems that business around PostgreSQL is as robust as its feature set. Ruohang Feng (Vonng) recently [wrote a blog post](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4) that highlighted just a slice of the PostgreSQL software and business ecosystem that's been built around it, which is only possible through the PostgreSQL Licence. I say "just a slice" because there's even more, both historically and current, projects and business that are built up around some portion of the PostgreSQL codebase. While many of these projects may be released under different licenses or be closed source, they have helped drive, both directly and indirectly, PostgreSQL adoption, and have helped make the PostgreSQL protocol ubiquitous.

But the biggest reason why PostgreSQL would not change its license is the disservice it would do to all PostgreSQL users. It takes a long time to build trust in a technology that is often used for the most critical part of an application: storage and retrieval of data. [PostgreSQL has earned a strong reputation for its proven architecture, reliability, data integrity, robust feature set, extensibility, and the dedication of the open source community behind the software to consistently deliver performant and innovative solutions](https://www.postgresql.org/about/). Changing the license of PostgreSQL would shatter all of the goodwill the project has built up through the past (nearly) 30 years.

While there are definitely parts of the PostgreSQL project that are imperfect (and I certainly contribute to those imperfections), the PostgreSQL Licence is a true gift to the PostgreSQL community and open source in general that we'll continue to cherish and help keep PostgreSQL truly free and open source. After all, it says [so on the website](https://www.postgresql.org/about/licence/) ;)