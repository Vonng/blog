---
title: PG生态新玩家：ParadeDB
date: 2024-02-18
hero: /hero/paradedb.jpg
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）
summary: >
  ParadeDB 旨在成为 Elasticsearch 的替代：Modern Elasticsearch Alternative built on Postgres —— 就是用于搜索和分析的 PostgreSQL。
tags: [PostgreSQL,PG生态,扩展]
---

> [微信公众号原文链接](https://mp.weixin.qq.com/s/bx2dRxlrtLcM6AD2qsplQQ)


---------------

## PG生态新玩家ParadeDB

YC S23 投了一个新项目 [ParadeDB](https://www.paradedb.com/)， 非常有意思。他们的 Slogan 是 “Postgres for Search & Analytics —— Modern Elasticsearch Alternative built on Postgres”。就是用于搜索和分析的 PostgreSQL，旨在成为 Elasticsearch 的替代。

PostgreSQL 的生态确实越来越繁荣了，在基于 PG 的扩展与衍生中，我们已经有了基于 MongoDB 开源替代 —— FerretDB，SQL Server 开源替代 Babelfish，Firebase 开源替代 Supabase，AirTable 开源替代 NocoDB，现在又多了 ElasticSearch 开源替代 —— ParadeDB。

ParadeDB 实际上是由三个 PostgreSQL 扩展组成：`pg_bm25`，`pg_analytics`，以及 `pg_sparse`。这三个扩展都可以独立使用了。我已经将这几个扩展打好包（v0.5.6），并将会在 Pigsty 的下个 Release 中默认收录，让用户能够开箱即用。

我翻译了 ParadeDB 的官网介绍与四篇博客文章，为您介绍这个 PostgreSQL 生态的新星。 今天是第一篇 —— 概览

![](paradedb-rank.png)



---------------

## ParadeDB

我们荣幸地向您介绍 ParadeDB：针对搜索场景优化的 PostgreSQL 数据库。**ParadeDB** 是第一个旨在成为 Elasticsearch 替代的 Postgres 数据库构建，被设计为可以在PG表上进行闪电般快速的全文检索、语义检索、以及混合检索。

![](paradedb-logo.png)


### ParadeDB解决什么问题？

对于许多组织而言，搜索依然是一个未解问题 —— 尽管有像 Elasticsearch 这样的巨头存在，但大多数与其打过交道的开发者都知道，运行、调优和管理 Elasticsearch 是多么痛苦的一件事。虽然也有其他的搜索引擎服务，但在现有数据库上粘连对接这些外部服务，会引入更多重建索引和数据复制的复杂难题与成本。

那些追求统一权威数据源与搜索引擎的开发者转了 Postgres，PG 已经通过 `tsvector` 提供了基本的全文检索能力，也通过 `pgvector` 提供了向量语义检索能力。这些工具也许对于简单用例和中等大小的数据集来说很好使，但当表变大或查询变得复杂时就有些不够用了：

1. 大表上的排序和关键词搜索非常缓慢
2. 不支持 BM25 计算
3. 没有混合检索支持，将向量搜索与全文搜索的技术
4. 没有实时搜索 — 数据必须手动重新索引或重新嵌入
5. 对复杂查询如分面或相关性调优的支持有限

到目前为止，我们已经目睹了许多工程团队用很勉强的方式在 Postgres 上叠加了一套 Elasticsearch，随即因为后者太过于臃肿、昂贵或复杂，而最终放弃。我们在想：如果 Postgres 本身就带有 ElasticSearch 水平的搜索会发生什么？那么开发者就不会有这种两难选择了 —— 统一使用 PostgreSQL 但搜索能力受限，还是使用事实源和搜索引擎两种独立的服务？

### ParadeDB适用于谁？

Elasticsearch 拥有广泛的应用场景，但我们并不企图一蹴而就地覆盖所有场景——至少现阶段不是。我们更倾向于专注于一些核心场景 —— 专为那些希望在 PostgreSQL 上进行搜索的用户服务。对于以下情况，ParadeDB 会是您的理想选择：

- 希望使用单一 Postgres 作为事实来源，厌恶在多个服务之间搬运复制数据。
- 希望在不损害性能与可伸缩性的前提下，对存储在 Postgres 中的海量文档进行全文搜索。
- 希望 ANN/相似度搜索与全文搜索相结合，从而获得更精准的语义匹配效果

### ParadeDB产品介绍

ParadeDB 是一个完全托管的 Postgres 数据库，具有在任何其他 Postgres 提供者中未发现的索引和搜索 Postgres 表的能力：

| 特性       | 描述                                           |
|----------|----------------------------------------------|
| BM25全文搜索 | 支持布尔、模糊、提升和关键字查询的全文搜索。搜索结果使用 BM25 算法打分。      |
| 分面搜索     | Postgres 列可以定义为分面，以便轻松分桶和收集指标。               |
| 混合搜索     | 搜索结果可以打分，综合考虑语义相关性（向量搜索）与全文相关性（ BM25）。       |
| 分布式搜索    | 表可以进行分片，以便进行并行查询加速。                          |
| 生成式搜索    | Postgres 列可以输入到大型语言模型（LLMs）中，用于自动摘要、分类或文本生成。 |
| 实时搜索     | 文本索引和向量列自动与底层数据保持同步。                         |

与 AWS RDS 等托管服务不同，ParadeDB 是一个 PostgreSQL 扩展插件，不需要任何设置，可以与整个 PG 生态集成，并完全可定制。ParadeDB 是开源的（AGPLv3），并提供了一个简单的 Docker Compose 模板以满足需要自建/定制的开发者的需求。

### ParadeDB 的构建方式

ParadeDB 的核心是一个带有自定义扩展的标准 Postgres 数据库，这些扩展使用 Rust 编写，引入了增强的搜索能力。

ParadeDB 的搜索引擎基于 Tantivy 构建，Tantivy 是受 Apache Lucene 启发的开源 Rust 搜索库。其索引作为原生的 PG 索引存储在PG中，从而避免了繁琐的数据复制/ETL工作，并同时可以确保事务 ACID。

ParadeDB 为 Postgres 生态提供了一个新扩展：`pg_bm25`。`pg_bm25` 使用 BM25 评分算法在 Postgres 中实现了基于 Rust 的全文搜索。ParadeDB 会预装这个扩展插件。

### 下一步是什么？

ParadeDB 的托管云版本目前处于 PrivateBeta 阶段。我们的目标是在 2024 年初推出一个自助服务的云平台。如果你想在此期间访问 PrivateBeta 版本，欢迎[加入我们的等待名单](https://paradedb.typeform.com/to/jHkLmIzx?typeform-source=www.paradedb.com)。

我们核心团队的重点是开发 ParadeDB 的开源版本，将在 2023 年冬季推出。

我们 Build in Public，并很高兴能与整个社区分享 ParadeDB。欢迎关注我们，在未来的博文中我们会进一步详细介绍 ParadeDB 背后的有趣技术挑战。



