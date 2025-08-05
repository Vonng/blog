---
title: PostgreSQL, The most successful database
linkTitle: "PG, The most successful database"
date: 2023-06-28
author: |
  [RuohangFeng](https://vonng.com)([@Vonng](https://vonng.com/en/))| [WeChat](https://mp.weixin.qq.com/s/xewE87WEaZHp-K5hjuk65A) | [Zhihu](https://zhuanlan.zhihu.com/p/542019272)
summary: "StackOverflow 2023 Survey shows PostgreSQL is the most popular, loved, and wanted database, solidifying its status as the 'Linux of Database'."
tags: [PostgreSQL,Ecosystem]
---


The [StackOverflow 2023 Survey](https://survey.stackoverflow.co/2023), featuring feedback from 90K developers across 185 countries, is out. PostgreSQL topped all three survey categories (used, loved, and wanted), earning its title as the undisputed "Decathlete Database" – it's hailed as the **"Linux of Database"**!

![](/img/blog/db/pg-is-no1-1.png)

> https://demo.pigsty.cc/d/sf-survey

What makes a database "successful"? It’s a mix of features, quality, security, performance, and cost, but success is mainly about adoption and legacy. The size, preference, and needs of its user base are what truly shape its ecosystem's prosperity. StackOverflow's annual surveys for seven years have provided a window into tech trends.

**PostgreSQL is now the world’s most popular database.**

**PostgreSQL is developers' favorite database!**

**PostgreSQL sees the highest demand among users!**

Popularity, the `used` reflects the past, the `loved` indicates the present, and the `wanted` suggests the future. These metrics vividly showcase the vitality of a technology. PostgreSQL stands strong in both stock and potential, unlikely to be rivaled soon.

As a dedicated user, community member, expert, evangelist, and contributor to PostgreSQL, witnessing this moment is profoundly moving. Let's delve into the "Why" and "What" behind this phenomenon.



------

## Source: Community Survey

Developers define the success of databases, and StackOverflow's survey, with popularity, love, and demand metrics, captures this directly. 

> “Which **database environments** have you done extensive development work in over the past year, and which do you want to work in over the next year? If you both worked with the database and want to continue to do so, please check both boxes in that row.”

Each database in the survey had two checkboxes: one for current use, marking the user as "Used," and one for future interest, marking them as "Wanted." Those who checked both were labeled as "Loved/Admired."

![](/img/blog/db/pg-is-no1-2.png)

> https://survey.stackoverflow.co/2023

The percentage of "Used" respondents represents **popularity** or usage rate, shown as a bar chart, while "Wanted" indicates demand or desire, marked with blue dots. "Loved/Admired" shows as red dots, indicating love or reputation. In 2023, PostgreSQL outstripped MySQL in popularity, becoming the world’s most popular database, and led by a wide margin in demand and reputation.

Reviewing seven years of data and plotting the top 10 databases on a scatter chart of popularity vs. net love percentage (2*love% - 100), we gain insights into the database field's evolution and sense of scale.

![](/img/blog/db/pg-is-no1-3.gif)

> X: Popularity, Y: Net Love Index (2 * loved - 100)

The 2023 snapshot shows PostgreSQL in the top right, popular and loved, while MySQL, popular yet less favored, sits in the bottom right. Redis, moderately popular but much loved, is in the top left, and Oracle, neither popular nor loved, is in the bottom left. In the middle lie SQLite, MongoDB, and SQL Server.

Trends indicate PostgreSQL's growing popularity and love; MySQL's love remains flat with falling popularity. Redis and SQLite are progressing, MongoDB is peaking and declining, and the commercial RDBMSs SQL Server and Oracle are on a downward trend.

The takeaway: PostgreSQL's standing in the database realm, akin to Linux in server OS, seems unshakeable for the foreseeable future.




------

## Historical Accumulation: Popularity

> PostgreSQL — The world's most popular database

Popularity is the percentage of total users who have used a technology in the past year. It reflects the accumulated usage over the past year and is a core metric of factual significance.

In 2023, PostgreSQL, branded as the "most advanced," surpassed the "most popular" database MySQL with a usage rate of 45.6%, leading by 4.5% and reaching 1.1 times the usage rate of MySQL at 41.1%. Among professional developers (about three-quarters of the sample), PostgreSQL had already overtaken MySQL in 2022, with a 0.8 percentage point lead (46.5% vs 45.7%); this gap widened in 2023 to 49.1% vs 40.6%, or 1.2 times the usage rate among professional developers.

Over the past years, MySQL enjoyed the top spot in database popularity, proudly claiming the title of the “world’s most popular open-source relational database.” However, PostgreSQL has now claimed the crown. Compared to PostgreSQL and MySQL, other databases are not in the same league in terms of popularity.

The key trend to note is that among the top-ranked databases, only PostgreSQL has shown a consistent increase in popularity, demonstrating strong growth momentum, while all other databases have seen a decline in usage. As time progresses, the gap in popularity between PostgreSQL and other databases will likely widen, making it hard for any challenger to displace PostgreSQL in the near future.

Notably, the "domestic database" TiDB has entered the StackOverflow rankings for the first time, securing the 32nd spot with a 0.2% usage rate.

Popularity reflects the current scale and potential of a database, while love indicates its future growth potential.


------

## Current Momentum: Love

> PostgreSQL — The database developers love the most

Love or admiration is a measure of the percentage of users who are willing to continue using a technology, acting as an annual "retention rate" metric that reflects the user's opinion and evaluation of the technology.

In 2023, PostgreSQL retained its title as the most loved database by developers. While Redis had been the favorite in previous years, PostgreSQL overtook Redis in 2022, becoming the top choice. PostgreSQL and Redis have maintained close reputation scores (around 70%), significantly outpacing other contenders.

![](/img/blog/db/pg-is-no1-6.png)

In the 2022 PostgreSQL community survey, the majority of existing PostgreSQL users reported increased usage and deeper engagement, highlighting the stability of its core user base.

![](/img/blog/db/pg-is-no1-7.png)

Redis, known for its simplicity and ease of use as a data structure cache server, is often paired with the relational database PostgreSQL, enjoying considerable popularity (20%, ranking sixth) among developers. Cross-analysis shows a strong connection between the two: 86% of Redis users are interested in using PostgreSQL, and 30% of PostgreSQL users want to use Redis. Other databases with positive reviews include SQLite, MongoDB, and SQL Server. MySQL and ElasticSearch receive mixed feedback, hovering around the 50% mark. The least favored databases include Access, IBM DB2, CouchDB, Couchbase, and Oracle.

Not all **potential** can be converted into kinetic energy. While user affection is significant, it doesn't always translate into action, leading to the third metric of interest – demand.



------

## Future Trends: Demand

> PostgreSQL - The Most Wanted Database

The demand rate, or the level of desire, represents the percentage of users who will actually opt for a technology in the coming year. PostgreSQL stands out in demand/desire, significantly outpacing other databases with a 42.3% rate for the second consecutive year, showing relentless growth and widening the gap with its competitors.

![](/img/blog/db/pg-is-no1-8.png)

In 2023, some databases saw notable demand increases, likely driven by the surge in large language model AI, spearheaded by OpenAI's ChatGPT. This demand for intelligence has, in turn, fueled the need for robust data infrastructure. A decade ago, support for NoSQL features like JSONB/GIN laid the groundwork for PostgreSQL's explosive growth during the internet boom. Today, the introduction of pgvector, the first vector extension built on a mature database, grants PostgreSQL a ticket into the AI era, setting the stage for growth in the next decade.


------

## But Why?

PostgreSQL leads in demand, usage, and popularity, with the right mix of timing, location, and human support, making it arguably the most successful database with no visible challengers in the near future. The secret to its success lies in its slogan: **"The World's Most Advanced Open Source Relational Database."**

Relational databases are so prevalent and crucial that they might dwarf the combined significance of other types like key-value, document, search engine, time-series, graph, and vector databases. Typically, "database" implicitly refers to "relational database," where no other category dares claim mainstream status. Last year's "Why PostgreSQL Will Be the Most Successful Database?" delves into the competitive landscape of relational databases—a tripartite dominance. Excluding Microsoft’s relatively isolated SQL Server, the database scene, currently in a phase of consolidation, has three key players rooted in WireProtocol: Oracle, MySQL, and PostgreSQL, mirroring a **"Three Kingdoms"** saga in the relational database realm.

![](/img/blog/db/pg-is-no1-9.png)

Oracle/MySQL are waning, while PostgreSQL is thriving. Oracle is an established commercial DB with deep tech history, rich features, and strong support, favored by well-funded, risk-averse enterprises, especially in finance. Yet, it's pricey and infamous for litigious practices. MS SQL Server shares similar traits with Oracle. Commercial databases are facing a slow decline due to the open-source wave.

MySQL, popular yet beleaguered, lags in stringent transaction processing and data analysis compared to PostgreSQL. Its agile development approach is also outperformed by NoSQL alternatives. Oracle's dominance, sibling rivalry with MariaDB, and competition from NewSQL players like TiDB/OB contribute to its decline.

Oracle, no doubt skilled, lacks integrity, hence "talented but unprincipled." MySQL, despite its open-source merit, is limited in capability and sophistication, hence "limited talent, weak ethics." PostgreSQL, embodying both capability and integrity, aligns with the open-source rise, popular demand, and advanced stability, epitomizing "talented and principled."


------

## Open Source & Advanced

The primary reasons for choosing PostgreSQL, as reflected in the TimescaleDB community survey, are its open-source nature and stability. Open-source implies free use, potential for modification, no vendor lock-in, and no "chokepoint" issues. Stability means reliable, consistent performance with a proven track record in large-scale production environments. Experienced developers value these attributes highly.

Broadly, aspects like extensibility, ecosystem, community, and protocols fall under "open-source." Stability, ACID compliance, SQL support, scalability, and availability define "advanced." These resonate with PostgreSQL's slogan: "The world's most advanced open source relational database."

![](/img/blog/db/pg-is-no1-10.png)

> https://www.timescale.com/state-of-postgres/2022




------

## The Virtue of Open Source

> powered by developers worldwide. Friendly BSD license, thriving ecosystem, extensive expansion. A robust Oracle alternative, leading the charge.

What is "virtue"? It's the manifestation of "the way," and this way is **open source**. PostgreSQL stands as a venerable giant among open-source projects, epitomizing global collaborative success.

Back in the day, developing software/information services required exorbitantly priced **commercial databases**. Just the software licensing fees could hit six or seven figures, not to mention similar costs for hardware and service subscriptions. Oracle's licensing fee per CPU core could reach hundreds of thousands annually, prompting even giants like Alibaba to seek **IOE alternatives**. The rise of **open-source databases** like **PostgreSQL** and **MySQL** offered a fresh choice.

Open-source databases, free of charge, spurred an industry revolution: from tens of thousands per core per month for commercial licenses to a mere 20 bucks per core per month for hardware. Databases became accessible to regular businesses, enabling the provision of free information services.

![](/img/blog/db/pg-is-no1-11.png)

Open source has been monumental: the history of the internet is a history of open-source software. The prosperity of the IT industry and the plethora of free information services owe much to open-source initiatives. **Open source represents a form of successful Communism** in software, with the industry's core means of production becoming communal property, available to developers worldwide as needed. Developers contribute according to their abilities, embracing the ethos of mutual benefit.

An open-source programmer's work encapsulates the intellect of countless top-tier developers. Programmers command high salaries because they are not mere laborers but **contractors** orchestrating software and hardware. They own the core means of production: software from the public domain and readily available server hardware. Thus, a few skilled engineers can swiftly tackle domain-specific problems leveraging the **open-source ecosystem**.

**Open source synergizes community efforts, drastically reducing redundancy and propelling technical advancements at an astonishing pace. Its momentum, now unstoppable, continues to grow like a snowball.** Open source dominates foundational software, and the industry now views insular development or so-called "self-reliance" in software, especially in foundational aspects, as a colossal joke.

![](/img/blog/db/pg-is-no1-12.png)

**For PostgreSQL, open source is its strongest asset against Oracle.**

Oracle is advanced, but PostgreSQL holds its own. It's the most Oracle-compatible open-source database, natively supporting 85% of Oracle's features, with specialized distributions reaching 96% compatibility. However, the real game-changer is cost: PG's open-source nature and significant cost advantage provide a substantial ecological niche. It doesn't need to surpass Oracle in features; being "90% right at a fraction of the cost" is enough to outcompete Oracle.

PostgreSQL is like an open-source "Oracle," the only real threat to Oracle's dominance. As a leader in the "de-Oracle" movement, PG has spawned numerous "domestically controllable" database companies. According to CITIC, 36% of "domestic databases" are based on PG modifications or rebranding, with Huawei's openGauss and GaussDB as prime examples. Crucially, PostgreSQL uses a BSD-Like license, permitting such adaptations — you can rebrand and sell without deceit. This open attitude is something Oracle-acquired, GPL-licensed MySQL can't match.


------

## The advanced in Talent

> The talent of PG lies in its advancement. Specializing in multiple areas, PostgreSQL offers a full-stack, multi-model approach: "Self-managed, autonomous driving temporal-geospatial AI vector distributed document graph with full-text search, programmable hyper-converged, federated stream-batch processing in a single HTAP Serverless full-stack platform database", covering almost all database needs with a single component.

PostgreSQL is not just a traditional OLTP "relational database" but a multi-modal database. For SMEs, a single PostgreSQL component can cover the vast majority of their data needs: OLTP, OLAP, time-series, GIS, tokenization and full-text search, JSON/XML documents, NoSQL features, graphs, vectors, and more.

![](/img/blog/db/pg-is-no1-13.png)

> Emperor of Databases — Self-managed, autonomous driving temporal-geospatial AI vector distributed document graph with full-text search, programmable hyper-converged, federated stream-batch processing in a single HTAP Serverless full-stack platform database.

The superiority of PostgreSQL is not only in its acclaimed **kernel stability** but also in its powerful **extensibility**. The plugin system transforms PostgreSQL from a single-threaded evolving database kernel to a platform with countless parallel-evolving extensions, exploring all possibilities simultaneously like quantum computing. PostgreSQL is omnipresent in every niche of data processing.

For instance, PostGIS for geospatial databases, TimescaleDB for time-series, Citus for distributed/columnar/HTAP databases, PGVector for AI vector databases, AGE for graph databases, PipelineDB for stream processing, and the ultimate trick — using Foreign Data Wrappers (FDW) for unified SQL access to all heterogeneous external databases. Thus, PG is a true full-stack database platform, far more advanced than a simple OLTP system like MySQL.


![](/img/blog/db/pg-is-no1-14.png)

Within a significant scale, PostgreSQL can play multiple roles with a single component, greatly reducing project complexity and cost. Remember, designing for unneeded scale is futile and an example of **premature optimization**. If one technology can meet all needs, it's the best choice rather than reimplementing it with multiple components.

Taking Tantan as an example, with **250 million TPS** and **200 TB** of unique TP data, **a single PostgreSQL selection** remains stable and reliable, covering a wide range of functions beyond its primary OLTP role, including caching, OLAP, batch processing, and even message queuing. However, as the user base approaches **tens of millions daily active users**, these additional functions will eventually need to be handled by dedicated components.

![](/img/blog/db/pg-is-no1-15.png)

PostgreSQL's advancement is also evident in its thriving ecosystem. Centered around the database kernel, there are specialized variants and "higher-level databases" built on it, like Greenplum, Supabase (an open-source alternative to Firebase), and the specialized graph database edgedb, among others. There are various open-source/commercial/cloud distributions integrating tools, like different RDS versions and the plug-and-play Pigsty; horizontally, there are even powerful mimetic components/versions emulating other databases without changing client drivers, like babelfish for SQL Server, FerretDB for MongoDB, and EnterpriseDB/IvorySQL for Oracle compatibility.

![](/img/blog/db/pg-is-no1-16.png)

PostgreSQL's advanced features are its core competitive strength against MySQL, another open-source relational database.

**Advancement is PostgreSQL's core competitive edge over MySQL.**

MySQL's slogan is "the world's most popular open-source relational database," characterized by being rough, fierce, and fast, catering to internet companies. These companies prioritize simplicity (mainly CRUD), data consistency and accuracy less than traditional sectors like banking, and can tolerate data inaccuracies over service downtime, unlike industries that cannot afford financial discrepancies.

However, times change, and PostgreSQL has rapidly advanced, surpassing MySQL in speed and robustness, leaving only "roughness" as MySQL's remaining trait.

![](/img/blog/db/pg-is-no1-17.png)

> MySQL allows partial transaction commits by default, shocked

MySQL allows partial transaction commits by default, revealing a gap between "popular" and "advanced." Popularity fades with obsolescence, while advancement gains popularity through innovation. In times of change, without advanced features, popularity is fleeting. Research shows MySQL's pride in "popularity" cannot stand against PostgreSQL's "advanced" superiority.

**Advancement** and **open-source** are PostgreSQL's success secrets. While Oracle is advanced and MySQL is open-source, PostgreSQL boasts both. With the right conditions, success is inevitable.




--------------

## Looking Ahead

The PostgreSQL database kernel's role in the database ecosystem mirrors the Linux kernel's in the operating system domain. For databases, particularly OLTP, the battle of kernels has settled—PostgreSQL is now a perfect engine.

However, users need more than an engine; they need the complete car, driving capabilities, and traffic services. The database competition has shifted from software to **Software enabled Service—complete database distributions and services**. The race for PostgreSQL-based distributions is just beginning. Who will be the PostgreSQL equivalent of Debian, RedHat, or Ubuntu?

This is why we created **[Pigsty](https://pigsty.io/)** — to develop an battery-included, open-source, local-first PostgreSQL distribution, making it easy for everyone to access and utilize a **quality database service**. Due to space limits, the detailed story is for [another time](/db/pgsql-x-pigsty/).

![](/img/blog/db/pg-is-no1-18.png)




--------------

## 参考阅读

2022-08 《[PostgreSQL 到底有多强？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485240&idx=1&sn=9052f03ae2ef21d9e21037fd7a1fa7fe&chksm=fe4b32e3c93cbbf522616346c1afd49e1e6edbb0898694df224fe2134a69c0c4562aab35587a&scene=21#wechat_redirect)》

2022-07 《[为什么PostgreSQL是最成功的数据库？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485216&idx=1&sn=1b59c7dda5f347145c2f39d2679a274d&chksm=fe4b32fbc93cbbed574358a3bcf127dd2e4f458638b46efaee1a885a5702a66a5d9ca18e3f90&scene=21#wechat_redirect)》

2022-06 《[StackOverflow 2022数据库年度调查](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485170&idx=1&sn=657c75be06557df26e4521ce64178f14&chksm=fe4b3329c93cba3f840283c9df0e836e96a410f540e34ac9b1b68ca4d6247d5f31c94e2a41f4&scene=21#wechat_redirect)》

2021-05 《[Why PostgreSQL Rocks!](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247484604&idx=1&sn=357b3381e7636709fa9e5e06894b7273&chksm=fe4b3167c93cb8719b7c6b048fd300a7773c73319ba0c119359f4f8a6684cd969434c5abbdfd&scene=21#wechat_redirect)》

2021-05 《[为什么说PostgreSQL前途无量？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247484591&idx=1&sn=a6ab13d93bfa26fca969ba163b01e1d5&chksm=fe4b3174c93cb862899cbce4b9063ed009bfe735df16bce6b246042e897d494648473eea3cea&scene=21#wechat_redirect)》

2018 《[PostgreSQL 好处都有啥？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247483706&idx=1&sn=b842684b41ac6dde8310448ae0a81a76&chksm=fe4b34e1c93cbdf7dcfcdae5f3ddc38bc422989421266dcda957fa2b596e361815624c92b3ec&scene=21#wechat_redirect)》

2023 《[更好的开源RDS替代：Pigsty](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485518&idx=1&sn=3d5f3c753facc829b2300a15df50d237&chksm=fe4b3d95c93cb4833b8e80433cff46a893f939154be60a2a24ee96598f96b32271301abfda1f&scene=21#wechat_redirect)》

2023 《[StackOverflow 7年调研数据跟踪](http://demo.pigsty.cc/d/sf-db-survey)》

2022 《[PostgreSQL 社区状态调查报告 2022](https://www.timescale.com/state-of-postgres/2022)》