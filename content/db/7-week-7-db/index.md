---
title: 七周七数据库（2025年）
date: 2024-12-03
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [微信公众号](https://mp.weixin.qq.com/s/gQZ3Q5JKV8gaBNhc1puPcA) | [英文原文](https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/)
summary: >
  PostgreSQL是无聊数据库之王？2025年哪些是有前途能打的数据库？
tags: [数据库,PostgreSQL]
---

> 作者：Matt Blewitt，原文：七周七数据库（2025年）
>
> 译者：冯若航，数据库老司机，云计算泥石流

https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/


长期以来，我一直在运营数据库即服务（Databases-as-a-Service），这个领域总有新鲜事物需要跟进 —— 新技术、解决问题的不同方法，更别提大学里不断涌现的研究成果了。展望2025年，考虑花一周时间深入了解以下每项数据库技术吧。

![A line drawing of a bookshelf, with the books labelled for each database covered - PostgreSQL, SQLite, DuckDB, ClickHouse, FoundationDB, TigerBeetle and CockroachDB](https://matt.blwt.io/7-databases-in-7-weeks-for-2025/header.webp)

--------

## 前言

这不是 “七大最佳数据库” 之类的文章，更不是给报菜单念书名式的列表做铺垫——这里只是我认为值得你花一周左右时间认真研究的七个数据库。你可能会问，“为什么不选Neo4j、MongoDB、MySQL / Vitess 或者其他数据库呢？”答案大多是：我觉得它们没啥意思。同时，我也不会涉及 Kafka 或其他类似的流数据服务——它们确实值得你花时间学习，但不在本文讨论范围内。


--------

## 目录

1. [PostgreSQL](#1-postgresql)
2. [SQLite](#2-sqlite)
3. [DuckDB](#3-duckdb)
4. [ClickHouse](#4-clickhouse)
5. [FoundationDB](#5-foundationdb)
6. [TigerBeetle](#6-tigerbeetle)
7. [CockroachDB](#7-cockroachdb)
8. [小结](https://matt.blwt.io/post/7-databases-in-7-weeks-for-2025/#wrap-up)


--------

## 1. PostgreSQL

### 默认数据库

“一切皆用 Postgres” 几乎成了一个梗，原因很简单。[PostgreSQL](https://www.postgresql.org/) 是 [枯燥技术](https://boringtechnology.club/) 的巅峰之作，当你需要 客户端-服务器 模型的数据库时，它应该是你的首选。PG 遵循ACID原则，拥有丰富的复制方法 —— 包括物理和逻辑复制—— 并且在所有主要供应商中都有极好的支持。

然而，我最喜欢 Postgres 功能是 [扩展](https://wiki.postgresql.org/wiki/Extensions)。在这一点上，Postgres 展现出了其他数据库难以企及的生命力。几乎你想要的功能都有相应的扩展——[AGE](https://age.apache.org/)支持图数据结构和Cypher查询语言，[TimescaleDB](https://docs.timescale.com/self-hosted/latest/)支持时间序列工作负载，[Hydra Columnar](https://github.com/hydradatabase/hydra/tree/main/columnar)提供了另一种列式存储引擎，等等。如果你有兴趣亲自尝试，我最近[写了一篇关于编写扩展的文章](https://matt.blwt.io/post/building-a-postgresql-extension-line-by-line)。

正因为如此，Postgres 作为一个优秀的 “默认” 数据库熠熠生辉，我们还看到越来越多的非 Postgres 服务使用 [Postgres 线缆协议](https://www.postgresql.org/docs/current/protocol.html) 作为通用的七层协议，以提供客户端兼容性。拥有丰富的生态系统、合理的默认行为，甚至可以用 [Wasm](https://pglite.dev/) 跑在浏览器中，这使得它成为一个值得深入理解的数据库。

花一周时间了解 Postgres 的各种可能性，同时也了解它的一些限制 ——[MVCC](https://www.geeksforgeeks.org/multiversion-concurrency-control-mvcc-in-postgresql/) 可能有些任性。用你最喜欢的编程语言实现一个简单的CRUD应用程序，甚至可以尝试构建一个 Postgres 扩展。



--------

## 2. SQLite

### 本地优先数据库

离开客户端-服务器模型，我们绕道进入 “嵌入式” 数据库，首先介绍 [SQLite](https://www.sqlite.org/index.html)。我将其称为“[本地优先](https://www.inkandswitch.com/local-first/)”数据库，因为SQLite数据库与应用程序直接共存。一个更著名的例子是[WhatsApp](https://www.whatsapp.com/)，它将聊天记录存储为设备上的本地 SQLite 数据库。[Signal](https://signal.org/) 也是如此。

除此之外，我们开始看到更多 SQLite 的创新玩法，而不仅仅是将其当成一个本地ACID数据库。像 [Litestream](https://litestream.io/) 这样的工具提供了流式备份的能力， [LiteFS](https://fly.io/docs/litefs/) 提供了分布式访问的能力，这让我们可以设计出更有趣的拓扑架构。像[CR-SQLite](https://github.com/vlcn-io/cr-sqlite) 这样的扩展允许使用 [CRDTs](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)，以避免在合并变更集时需要冲突解决，正如 [Corrosion](https://github.com/superfly/corrosion) 的例子一样。

得益于[Ruby on Rails 8.0](https://rubyonrails.org/2024/9/27/rails-8-beta1-no-paas-required)，SQLite也迎来了一个小型复兴 ——37signals 全面投入 SQLite，构建了一系列 Rails 模块，如 [Solid Queue](https://github.com/rails/solid_queue)，并通过`database.yml`配置 Rails 以操作多个 SQLite 数据库。[Bluesky](https://newsletter.pragmaticengineer.com/p/bluesky?open=false#§sqlite) 使用SQLite作为个人数据服务器 —— 每个用户都有自己的 SQLite 数据库。

花一周时间使用 SQLite ，探索一下本地优先架构，你甚至可以研究下是否能将使用 Postgres 的客户端-服务器模型迁移到只使用 SQLite 的模式上。


--------

## 3. DuckDB

### 万能查询数据库

接下来是另一个嵌入式数据库，[DuckDB](https://duckdb.org/)。与SQLite类似，DuckDB旨在成为一个内嵌于进程的数据库系统，但更侧重于在线分析处理（OLAP）而非在线事务处理（OLTP）。

DuckDB 的亮点在于它作为一个“万能查询”数据库，使用 SQL 作为首选方言。它可以原生地从 CSV、TSV、JSON ，甚至像 Parquet 这样的格式中导入数据 —— 看看 [DuckDB的数据源列表](https://duckdb.org/docs/data/data_sources.html) 支持的数据源列表吧！这赋予了它极大的灵活性 —— 不妨看看 [查询Bluesky火焰管道的这个示例](https://motherduck.com/blog/how-to-extract-analytics-from-bluesky/)。

与 Postgres 类似，DuckDB 也有 [扩展](https://duckdb.org/docs/extensions/overview)，尽管生态系统没有那么丰富 —— 毕竟DuckDB还相对年轻。许多社区贡献的扩展可以在[社区扩展列表](https://duckdb.org/community_extensions/list_of_extensions)中找到，我特别喜欢[`gsheets`](https://duckdb.org/community_extensions/extensions/gsheets.html)。

花一周时间使用DuckDB进行一些数据分析和处理——无论是通过 Python Notebook，还是像[Evidence](https://evidence.dev/)这样的工具，甚至看看它如何与SQLite的“本地优先”方法结合，将SQLite数据库的分析查询卸载到DuckDB，毕竟 DuckDB 也[可以读取SQLite数据](https://duckdb.org/docs/guides/database_integration/sqlite.html)。


--------

## 4. ClickHouse

### 列式数据库

离开嵌入式数据库领域，但继续看看分析领域，我们会遇上 [ClickHouse](https://clickhouse.com/)。如果我只能选择两种数据库，我会非常乐意只用 Postgres 和 ClickHouse——前者用于OLTP，后者用于OLAP。

ClickHouse 专注于分析工作负载，并且通过[横向扩展](https://clickhouse.com/docs/en/architecture/horizontal-scaling)和分片存储，支持非常高的摄取率。它还支持[分层存储](https://clickhouse.com/docs/en/guides/separation-storage-compute)，允许你将“热”数据和“冷”数据分开—— [GitLab](https://docs.gitlab.com/ee/development/database/clickhouse/tiered_storage.html)对此有相当详尽的文档。

当你需要在一个 DuckDB 吃不下的大数据集上运行分析查询，或者需要 “实时” 分析时，ClickHouse 会有优势。关于这些数据集已经有很多 “Benchmarketing”（打榜营销）了，所以我就不再赘述了。

我建议你了解 ClickHouse 的另一个原因是它的操作体验极佳 —— 部署、扩展、备份等都有[详尽的文档](https://clickhouse.com/docs/en/architecture/cluster-deployment)——甚至包括设置 [合适的 CPU Governor](https://clickhouse.com/docs/en/operations/tips)。

花一周时间探索一些更大的分析数据集，或者将上面 DuckDB 分析转换为 ClickHouse 部署。ClickHouse 还有一个嵌入式版本 —— [chDB](https://clickhouse.com/docs/en/chdb)—— 可以提供更直接的对比。


--------

## 5. FoundationDB

### 分层数据库

现在我们进入了这个列表中的 “脑洞大开” 部分，[FoundationDB](https://www.foundationdb.org/) 登场。可以说，FoundationDB 不是一个数据库，而是数据库的基础组件。被 Apple、Snowflake 和 [Tigris Data](https://www.tigrisdata.com/blog/building-a-database-using-foundationdb/) 等公司用于生产环境，FoundationDB 值得你花点时间，因为它在键值存储世界中相当独特。

是的，它是一个有序的键值存储，但这并不是它有趣的点。乍看它有一些奇特的[限制](https://apple.github.io/foundationdb/known-limitations.html)——例如事务不能影响超过10MB 以上的数据，事务首次读取后必须在五秒内结束。但正如他们所说，限制让我们自由。通过施加这些限制，它可以在非常大的规模上实现完整的 ACID 事务—— 我知道有超过 100 TiB 的集群在运行。

FoundationDB 针对特定的工作负载而设计，并使用仿真方法试进行了[广泛地测试](https://apple.github.io/foundationdb/testing.html)，这种测试方法被其他技术采纳，包括本列表中的另一个数据库和由一些前 FoundationDB 成员创立的 [Antithesis](https://www.antithesis.com/)。关于这一部分请参阅 [Tyler Neely](https://sled.rs/simulation.html) 和 [PhilEaton](https://notes.eatonphil.com/2024-08-20-deterministic-simulation-testing.html) 的相关笔记。

如前所述，FoundationDB 具有一些非常特定的语义，需要一些时间来适应——他们的 [特性](https://apple.github.io/foundationdb/features.html) 文档和 [反特性](https://apple.github.io/foundationdb/anti-features.html) （不打算在数据库中提供的功能）文档值得去了解，以理解他们试图解决的问题。

但为什么它是“分层”数据库？因为它提出了[分层的概念](https://apple.github.io/foundationdb/layer-concept.html)，而不是选择将存储引擎与数据模型耦合在一起，而是设计了一个足够灵活的存储引擎，可以将其功能重新映射到不同的层面上。[Tigris Data](https://www.tigrisdata.com/blog/data-layer-foundationdb/)有一篇关于构建此类层的优秀文章，FoundationDB 组织还有一些示例，如 [记录层](https://github.com/FoundationDB/fdb-record-layer) 和 [文档层](https://github.com/FoundationDB/fdb-document-layer)。

花一周时间浏览 [教程](https://apple.github.io/foundationdb/tutorials.html)，思考如何使用FoundationDB替代像 [RocksDB](https://rocksdb.org/) 这样的数据库。也许可以看看一些 [设计方案](https://apple.github.io/foundationdb/design-recipes.html) 并阅读 [论文](https://www.foundationdb.org/files/fdb-paper.pdf)。


--------

## 6. TigerBeetle

### 极致正确数据库

继确定性仿真测试之后，[TigerBeetle](https://tigerbeetle.com/) 打破了先前数据库的模式，因为它明确表示自己 **不是**一个通用数据库 —— 它完全专注于金融事务场景。

为什么值得一看？单一用途的数据库很少见，而像 TigerBeetle 这样痴迷于正确性的数据库更是稀有，尤其是考虑到它是开源的。它们包含了从 [NASA的十律](https://en.wikipedia.org/wiki/The_Power_of_10:_Rules_for_Developing_Safety-Critical_Code) 和 [协议感知恢复](https://www.usenix.org/conference/fast18/presentation/alagappan) 到严格的串行化和  Direct I/O 以避免内核页面缓存问题，这一切的一切真是 **非常** 令人印象深刻——看看他们的 [安全文档](https://github.com/tigerbeetle/tigerbeetle/blob/a43f2205f5335cb8f56d6e8bfcc6b2d99a4fc4a4/docs/about/safety.md) 和他们称之为 Tiger Style 的[编程方法](https://github.com/tigerbeetle/tigerbeetle/blob/a43f2205f5335cb8f56d6e8bfcc6b2d99a4fc4a4/docs/TIGER_STYLE.md) 吧！

另一个有趣的点是，TigerBeetle是用 [Zig](https://ziglang.org/) 编写的——这是一门相对新兴的系统编程语言，但显然与 TigerBeetle 团队的目标非常契合。

花一周时间在本地部署的 TigerBeetle 中建模你的金融账户——按照 [快速入门](https://docs.tigerbeetle.com/quick-start) 操作，并看看[系统架构](https://docs.tigerbeetle.com/coding/system-architecture)文档，了解如何将其与上述更通用的数据库结合使用。


--------

## 7. CockroachDB

### 全球分布数据库

最后，我们回到了起点。在最后一个位置上，我有点纠结。我最初的想法是 [Valkey](https://valkey.io/)，但 FoundationDB 已经满足了键值存储的需求。我还考虑过图数据库，或者像 [ScyllaDB](https://www.scylladb.com/) 或 [Cassandra](https://cassandra.apache.org/_/index.html) 这样的数据库。我还考虑过 [DynamoDB](https://aws.amazon.com/dynamodb/)，但无法本地/免费运行让我打消了这个想法。

最终，我决定以一个全球分布式数据库结束 —— [CockroachDB](https://www.cockroachlabs.com/)。它兼容 Postgres 线缆协议，并继承了前面讨论的一些有趣特性——大规模横向扩展、强一致性——还拥有自己的一些有趣功能。

CockroachDB 实现了跨多个地理区域的数据库伸缩能力，生态位与 Google [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) 系统重叠，但 Spanner 依赖原子钟和GPS时钟进行极其精确的时间同步，然而普通硬件没有这样的奢侈配置，因此 CockroachDB 有一些[巧妙的解决方案](https://www.cockroachlabs.com/blog/living-without-atomic-clocks/#How-does-CockroachDB-choose-transaction-timestamps?)，通过重试或延迟读取以应对 NTP 时钟同步延迟，节点之间还会比较时钟漂移，如果超过最大偏移量则会终止成员。

CockroachDB 的另一个有趣特性是如何使用[多区域配置](https://www.cockroachlabs.com/docs/stable/multiregion-overview)，包括[表的本地性](https://www.cockroachlabs.com/docs/stable/table-localities)，根据你想要的读写利弊权衡提供不同的选项。花一周时间在你选择的语言和框架中重新实现 [`movr`](https://www.cockroachlabs.com/docs/v24.3/movr) 示例吧。


--------

## 总结

我们探索了许多不同的数据库，这些数据库都被地球上一些最大的公司在生产环境中使用，希望这能让你接触到一些之前不熟悉的技术。带着这些知识，去解决有趣的问题吧！




--------

## 老冯评论

在 2013 年有一本书叫《七周七数据库》。那本书介绍了当时的 7 种 “新生（或者重生）” 的数据库技术，给我留下了印象。12 年后，这个系列又开始有更新了。



回头看看当年的七数据库，除了原本的 “锤子” PostgreSQL 还在，其他的数据库都已经物是人非了。而 PostgreSQL 已经从 “锤子” 成为了 “枯燥数据库之王” —— 成为了不会翻车的 “默认数据库”。

在这个列表中的数据库，基本都是我已经实践过或者感兴趣/有好感的对象。当然 ClickHouse 除外，CK 不错，但我觉得 DuckDB 以及其与 PostgreSQL 的组合有潜力把 CK 给拱翻，再加上是 MySQL 协议兼容生态，所以对它确实没有什么兴趣。如果让我来设计这份名单，我大概会把 CK 换成 Supabase 或 Neon 中的一个。



我认为作者非常精准的把握了数据库技术发展的趋势，我高度赞同他对数据库技术的选择。实际上在这七个数据库中，我已经深入涉猎了其中三个。Pigsty 本身是一个高可用的 PostgreSQL 发行版，里面也整合了 DuckDB，以及 DuckDB 缝合的PG扩展。Tigerbettle 我也做好了 RPM/DEB 包，作为专业版中默认下载的金融事务专用数据库。

另外两个数据库，正在我的整合 TODOLIST 中，SQLite 除了 FDW，下一步就是把 ElectricSQL 给弄进来；提供本地 PG 与远端 SQLite / PGLite 的同步能力；CockroachDB 则一直在我的 TODOLIST 中，准备一有空闲就做个部署支持。FoundationDB 是我感兴趣的对象，下一个我愿意花时间深入研究的数据库不出意料会是这个。



总的来说，我认为这些技术代表着领域前沿的发展趋势。如果让我设想一下十年后的格局，那么大概会是这样的： FoundationDB，TigerBeetle，CockRoachDB 能有自己的小众基本盘生态位。DuckDB 大概会在分析领域大放异彩，SQLite 会在本地优先的端侧继续攻城略地，而 PostgreSQL 会从 “默认数据库” 变成无处不在的的  “Linux 内核”，数据库领域的主旋律变成 Neon，Supabase，Vercel，RDS，Pigsty 这样 PostgreSQL 发行版竞争的战场。

毕竟，PostgreSQL 吞噬数据库世界可不只是说说而已，PostgreSQL生态的公司几乎拿光了这两年资本市场数据库领域的钱，早就有无数真金白银用脚投票押注上去了。当然，未来到底如何，还是让我们拭目以待吧。


