---
title: "PostgreSQL 生态前沿进展"
date: 2025-01-24
author: 冯若航
summary: >
  和大家分享一下最近 PG 生态有趣的一些进展：Omnigres、PG Mooncake、Citus 13、FerretDB 2.0、ParadeDB等。
tags: [PostgreSQL, 生态]
---


读者朋友们，今天我要开始休假了。也许会停更两周，在这里提前祝大家新年快乐。

当然在开始休假之前，这篇文章和大家分享一下最近 PG 生态有趣的一些进展。昨天我也赶紧趁着还有时间，推出了 Pigsty 3.2.2 版本与 Pig v0.1.3 ：这个版本将可用的 PG 扩展从 350 一路干到 400 个，其中包含了上面大部分花活，下面简单介绍一下：

**Omnigres**：在PG里搞前后端Web全栈开发

**PG Mooncake**：在PG中实现Clickhouse的分析性能

**Citus**：支持 PG17 的分布式扩展 Citus 13 终于上新了

**FerretDB**：将PG仿真为MongoDB，2.0有20倍性能提升

**ParadeDB**：在PG提供ES全文检索能力，PG块存储实现

Pigsty 3.2.2：将上面的东西装进一个盒子里，开箱即用

------

## Omnigres

在前天的《[数据库即架构](https://mp.weixin.qq.com/s/8NS15_fkuR_gSLG50MNtMQ)》中，我已经介绍过这个有趣的项目了 —— Omnigres。简单来说，它可以把所有业务逻辑，甚至是Web服务器和整个后端都塞进 PostgreSQL 数据库里。

例如以下 SQL，将会启动一个 Web 服务器，将 `/www` 作为一个 Web 服务器的根目录对外提供服务。这意味着，你可以把一个经典前端-后端-数据库三层架构的应用，完整地塞入一个数据库中！。

如果是熟悉 Oracle 的用户可能会发现，这有点类似于 Oracle Apex。但在 PostgreSQL 中，你可以用二十多种编程语言来开发存储过程，而不仅仅局限于 PL/SQL！而且这里 Omnigres 提供的也远远不止一个 HTTPD 服务器，而是有 33 个扩展插件，几乎是提供了一个 PG 中的 “Web开发标准库”。

俗话说：“分久必合，合久必分”。在上古时期，许多 C/S，B/S 架构的应用就是几个客户端直接读写数据库。 但是后来，随着业务逻辑的复杂化，以及硬件性能（相对于业务需求）的捉襟见肘，许多东西从数据库中被剥离出来，形成了传统的三层架构。

硬件的发展让数据库服务器的性能重新出现大量的富余，而数据库软件的发展让存储过程的编写变得更加容易， 那么拆分剥离的趋势也很有可能会逆转，原本从数据库中分离出去的业务逻辑，又会重新回到数据库中。我认为 Omnigres，以及 Supabase 就是这样一种重新 ‘合“ 的尝试。

如果你有几十万 TPS，几十 TB 的数据，或者运行着一些至关重要、人命关天、硕大无朋的核心系统，那么这种玩法可能不太合时宜。但如果你运行的是一些个人项目，小网站，或者是初创公司与边缘创新系统，那么这种架构会让你的迭代更为敏捷，开发、运维更加简单。

Pigsty v3.2.2 中提供了 Omnigres 扩展，确实花了我不少功夫，在原作者 Yurii 的手把手帮助下，才在 10 个 Linux 发行版大版本上完成构建与封装。注意，这些插件是一个可以独立使用的扩展仓库中，您并非一定要使用 Pigsty 才能拥有这些扩展 —— Omnigres 与 AutoBase 这样的 PostgreSQL 也在使用这个仓库进行扩展交付，这确实是一个开源生态互惠共赢的大好例子。

## pg_mooncake

《DuckDB 缝合大赛》开赛以来，pg_mooncake 是最后一个入场的选手。他们一度沉寂让我几乎以为它们都放弃维护了。结果上周它们整了个大的，发布了 0.1.0 ，并直接在 ClickBench 排行榜上干进了前十，跟 ClickHouse 一个水平线了。

这是第一次， PG + 扩展插件的分析性能，能直接杀入分析榜单的 Tier 0 ，值得铭记。看来 pg_duckdb 确实迎来了一个劲敌 —— 我认为这是一件大好事，在给用户提供更多选择的同事，避免了一家独大垄断，在生态内部赛马卷翻天的同时，让整个 PostgreSQL 生态与其他 DBMS 在分析能力上远远拉开差距。

多数人对 PostgreSQL 的印象仍然停留在稳健的 OLTP（联机事务处理）数据库，却很少把它与“实时分析”联系起来。然而，PostgreSQL 的可扩展性让它能够“突破”固有印象，在实时分析上打出一片天地。mooncake 团队利用 PostgreSQL 的可扩展性，编写了一个原生扩展 pg_mooncake。他们把 DuckDB 的执行引擎嵌入到了列式查询中，这样在执行流程中可以以批量的方式（而不是逐行）处理数据，并利用 SIMD 指令集，从而在扫描、分组和聚合等场景获得更高效率。

mooncake 采用了一种更高效的元数据机制：与其从 Parquet 等存储格式外部再拉取元数据和统计信息，不如把它们直接存储在 PostgreSQL 中，这样不仅提升了查询优化与执行的速度，同时也支持更高级的功能，例如文件级别跳过，加速扫描等。

通过这些优化与设计，mooncake 实现了惊人的性能成绩（号称1000x）。这让 PostgreSQL 不再只是传统意义上的 OLTP “重型马”。通过充分的优化与工程实践，它完全可以在分析性能上与专业分析型数据库一较高下，同时仍然保留了 PostgreSQL 灵活性强、生态成熟的优势。这意味着，以后的数据堆栈可能会比现在简单的多 —— 你不再需要什么大数据全家桶与 ETL —— 在 Postgres 内部就可以实现顶级的分析性能。

Pigsty 在 v3.2.2 中正式提供了 mooncake 0.1 版本的二进制，请注意，这个扩展和 pg_duckdb 互斥，因为它们都带了自己的 libduckdb ，因此在一套系统中只能二选一。这一点比较让人遗憾，但我提了 Issue 希望他们能够共享一个 libduckdb ，毕竟每次编译这两个扩展冤家，都要从头编译 DuckDB 可真是要老命了。

最后，从这个扩展的名字（月饼）上就不难看出，这是一个华人主导的团队，越来越多的中国人出现并活跃在 PostgreSQL 生态中，这真是一件非常让人高兴的事。

> 博客：ClickBench 说Postgres是一个很棒的分析数据库 https://www.mooncake.dev/blog/clickbench-v0.1

------

## ParadeDB

ParadeDB 是 Pigsty 的老朋友，我们从非常早期的时候就支持着 ParadeDB ，并见证着它一路发展壮大，成为 PostgreSQL 生态中提供 ElasticSearch 能力替代的领导者。

`pg_search` 是 ParadeDB 基于 Postgres 的扩展，它实现了自定义索引以支持全文搜索和分析功能。该扩展由用 Rust 编写、受 Lucene 启发的搜索库 [Tantivy](https://github.com/quickwit-oss/tantivy) 提供底层支持。

pg_search 在最近两周发布了新的 0.14 版本，这个版本中它们切换到了 PG 原生的块存储，而不再依赖 Tantivy 自己的文件格式。这一架构改进带来了极大的可靠性改进与几倍的性能提升，属实惊人，并标志着它不再是一个 “缝合怪”，而是深度原生融入了 PG 之中。

在 `v0.14.0` 之前，`pg_search` 并未使用 Postgres 的块存储和缓冲区缓存（buffer cache）。这意味着扩展会自己创建一些不受 Postgres 管理的文件，并直接从磁盘读取其内容。虽然让扩展直接访问文件系统并不罕见(见注1)，但迁移到块存储后，`pg_search` 同时达成了以下目标：

1. 与 Postgres 写前日志（WAL）的深度集成，从而可以对索引进行物理复制。
2. 支持崩溃恢复和任意时间点恢复（point-in-time recovery）。
3. 完整支持 Postgres 的 MVCC（多版本并发控制）。
4. 与 Postgres 缓冲区缓存集成，大幅提升索引创建速度与写入吞吐量。

![img](https://www.paradedb.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fblock_storage_create_index.de1454d3.png&w=3840&q=75) ![img](https://www.paradedb.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fblock_storage_tps.598e54c0.png&w=3840&q=75)

pg_search 的最新版本已经收录到了 Pigsty 中，当然，我们也提供其他提供类似全文检索/分词能力的扩展，比如 pgroonga，p g_bestmatch，hunspell，以及中文分词 zhparser，供用户按需使用。

> 博客：使用 Postgres 块存储布局的全文检索 https://www.paradedb.com/blog/block_storage_part_one

------

## citus

pg_duckdb 与 pg_mooncake 是 PG 生态的 OLAP 新秀，而 Citus 与 Hydra 则是 PG 生态的老牌 OLAP （或者说 HTAP）扩展。前天 Citus 发布了 13.0.0 版本，正式提供了对 PostgerSQL 最新大版本 17 的支持，这意味着所有 **主力** 扩展均已完成对 PG 17 的适配，PG 17 冲冲冲！

Citus 是 PG 生态的分布式扩展，能够丝滑地将单机 PostgreSQL 主从部署转换为一个水平分布式集群。Citus 被微软收购后完全开源，云服务版本叫 Hyperscale PG 或 CosmosDB PG。

一般来说在当代硬件条件下，绝大多数用户都不会有机会接触到非要用分布式数据库不可的场景 —— 但这样的场景确实存在，比如在 《[花钱买罪受的大冤种：逃离云计算妙瓦底](https://mp.weixin.qq.com/s/zwJ2T2Vh_R7xD8IKPso31Q)》中的这位朋友，就因为云上云盘太贵而动作走形，考虑使用 Citus。所以，Pigsty 也在最近更新跟进了对 Citus 的支持。

通常来说，分布式数据库的运维管理要比主从麻烦很多，但我们设计了一套优雅的抽象，让部署管理 Citus 变得非常简单 —— 你只需要把他们当作多套水平的 PostgreSQL 集群来处理就好了，下面这个配置就可以一件拉起一套10节点的 Citus。

我最近还写了一篇如何部署 Citus 高可用集群的教程，供感兴趣的用户参考： https://pigsty.cc/docs/tasks/citus/

> 博客：Citus v13.0.0 发布注记：https://github.com/citusdata/citus/blob/v13.0.0/CHANGELOG.md

------

## FerretDB

最后，我们迎来了 FerretDB 2.0 。FerretDB 是 Pigsty 的老朋友了。Marcin 第一时间与我分享了新版本发布的喜悦。可惜现在 FerretDB 2.0 还是 RC，我只能等正式版本发布后再更新到 Pigsty 仓库中了，所以错过了这次 Pigsty v3.2.2 的发布窗口。但是没关系，下一个版本它就进来了！

FerretDB 是将 PostgreSQL 转换成 MongoDB “线缆协议兼容” 的适配中间件 —— 提供 Apache 2.0 协议，“真正开源” 的 MongoDB。FerretDB 2.0 依托微软全新开源的 DocumentDB PostgreSQL 扩展， 在性能、兼容性、支持和灵活性方面实现了重大飞跃，可应对更复杂的使用场景。主要亮点包括：

- 实现超过 20 倍的性能提升
- 更高的功能兼容性
- 支持向量搜索
- 支持复制（replication）
- 广泛的支持与服务

FerretDB 为 MongoDB 用户丝滑迁移到 PostgreSQL 提供了一条阻力最小的选择 —— 你不需要修改应用代码，就可以完成偷天换日，在兼容 MongoDB API 的同时还能享受 PG 生态几百个扩展提供的各种超能力。

> 博客：https://blog.ferretdb.io/ferretdb-releases-v2-faster-more-compatible-mongodb-alternative/

------

## Pigsty 3.2.2

最后，就是 Pigsty v3.2.2 了。这一次 Release 版本号更新带来 40 个全新的扩展插件（当然其中 33 个来自 Omnigres），以及现有扩展的更新版本（比如 Citus，ParadeDB，PGML）。同时，我们还推动并跟进了 PolarDB PG 支持 ARM64，以及支持 Debian 系统，并跟进了 IvorySQL 最新 PostgreSQL 17.2 兼容的 4.2 版本。

Well ，听上去都是一些版本跟进的活儿，但要不是这样，我也不能在休假前一天发布上线呀！总之，欢迎大家试试这些新扩展插件，如果遇到任何问题，欢迎向我反馈，但休假中我可不保证什么哈哈。

顺便一提，有用户反馈 Pigsty 的老网站太 “丑” 了，一股浓郁的技术直男风味，把所有信息密密麻麻的全部糊在首页上。我觉得，他们说的有一定道理，所以我最近找了个前端模板，重新做了个网站首页，看上去似乎更有 “国际范” 了一些。

老实说我得有七八年没搞前端了，上次折腾还是 JQuery 一把梭的时代，这次 Next.js / Vercel 这些新花样让我眼花撩乱。但好在摸清楚了之后也不算复杂，特别是有了GPT o1 pro 和 Cursor 的帮助下，花了一天时间就全部搞定了，AI 带来的惊人生产力提升确实让人感叹 。

好吧，以上就是最近 PostgreSQL 生态的新闻，我也准备打包行李了，下午飞机出发去泰国，希望不要遇到电诈。在这里就提前祝大家新年快乐啦！

-
- 