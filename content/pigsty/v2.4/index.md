---
title: "Pigsty v2.4：监控云数据库"
linkTitle: "Pigsty v2.4 发布注记"
date: 2023-09-14
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v2.4.0)）
summary: >
  PG16，监控RDS，服务咨询支持，新扩展：中文分词全文检索/图/HTTP/嵌入等
series: [Pigsty]
tags: [Pigsty]
---



PostgreSQL 今天发布了新的大版本 16，带来了一系列改进。Pigsty在发布后的1小时内便立即跟进了全新版本 Pigsty v2.4 ，提供了对 PostgreSQL 16 正式版的完整支持。此外在 v2.4 中，还对监控已有PG实例，特别是 RDS for PostgreSQL 与 PolarDB 提供了额外的支持。Redis 监控基于 7.x 进行了改进，提供了自动化的基于 Sentinel 的高可用配置。

Pigsty v2.4 目前仍为 Beta 状态，可以使用以下命令快速上手。**文档修缮完成后，将正式发布**。

 `bash -c "$(curl -fsSL https://get.pigsty.cc/beta)"` 

![图片](banner.jpg)



-------

## 亮点特性

•PostgreSQL 16 正式发布，Pigsty在发布后1小时内提供支持。•可以监控云数据库，RDS for PostgreSQL，以及 PolarDB，提供全新的 PGRDS 监控面板•正式提供**商业支持与咨询服务**。并发布首个 LTS 版本，为订阅客户提供最长5年的支持。•新扩展插件: **Apache AGE** ，在 PostgreSQL 上提供图数据库查询能力•新扩展插件: **zhparser**，中文分词，用于支持中文全文检索功能•新扩展插件: **pg_roaringbitmap**，高效实现 RoaringBitmap 位图功能•新扩展插件: **pg_embedding**，另一种基于 HNSW 索引的向量数据库插件hnsw alternative to pgvector•新扩展插件: **pg_tle**，由 AWS 出品的可信语言存储过程管理/发布/打包扩展•新扩展插件: **pgsql-http**，在数据库中使用 SQL 接口直接发送HTTP请求处理响应。•其他新增插件：**pg_auth_mon，pg_checksums，pg_failover_slots，pg_readonly，postgresql-unit pg_store_plans，pg_uuidv7，set_user**•Redis改进：支持 Redis 哨兵监控，配置主从集群的自动高可用。

**API变化**

•新增参数，`REDIS`.`redis_sentinel_monitor`，用于指定 Sentinel 集群监控的主库列表


-------

## PG16支持

Pigsty 也许是最早提供 PostgreSQL 16 支持的发行版，从 16 beta1 就开始，因此当 PostgreSQL 16 发布后一个小时，Pigsty 即完成了对正式版本的支持。你已经可以拉起 PostgreSQL 16 的高可用集群，尽管有个别重要扩展还没有在官方的 PGDG 仓库提供，例如 Citus 与 TimescaleDB。但其他一些扩展已经可用：包括 postgis34，pgvector， pg_squeeze，wal2json，pg_cron，以及由 Pigsty 所维护打包的扩展插件：zhparser，roaringbitmap，pg_embedding， pgsql-http 等。

PostgreSQL 16 有一些比较实用的新功能：从库逻辑解码与逻辑复制，针对I/O的新统计视图，全连接的并行执行，更好的冻结性能，符合 SQL/JSON 标准的新函数集，以及在HBA认证中使用正则表达式等等。

不过要注意的是，PGDG 官方仓库目前决定在 PostgreSQL 16 中放弃对 EL7 的支持，所以 PG16 仅在 EL8 与 EL9 及其兼容操作系统发行版中可用。


-------

## 监控RDS与PolarDB

Pigsty v2.4 提供了对 RDS 监控的支持。特别是还添加了对 PolarDB 云数据库的监控支持。当您只有一个远程 PostgreSQL 连接串时，可以使用这种方式将其纳入 Pigsty 监控。

![图片](polardb-cluster.jpg)

样例：监控一个一主一从的 PolarDB RDS 集群

Pigsty v2.4 提供了对 RDS 监控的支持。特别是还添加了对 PolarDB 云数据库的监控支持。当您只有一个远程 PostgreSQL 连接串时，可以使用这种方式将其纳入 Pigsty 监控中。Pigsty 提供了两个全新 Dashboard：PGRDS Cluster 与 PGINS Cluster，用于呈现 RDS PG 的完整指标。

![图片](pgrds-cluster.jpg)

![图片](pgrds-dashboard-1.jpg)

![图片](pgrds-dashboard-2.jpg)



-------

## 商业支持

Pigsty v2.4 是第一个 LTS 版本，将为企业订阅用户提供3年的长时间支持。同时，我们将正式开始对外提供订阅与支持服务，欢迎有需求的用户联系我们采购。

**https://pigsty.cc/zh/docs/support/**

![图片](support-page.jpg)



-------

## REDIS高可用

Pigsty v2.4 中，我们提供了一个新的参数 redis_sentinel_monitor ，用于自动配置经典主从 Redis 集群的高可用。该参数只能在 Sentinel 集群上定义，定义中的主库将会自动被哨兵集群所纳管

![图片](redis-sentinel.jpg)

与此同时，我们也在 Redis 监控中添加了 Sentinel 相关指标与面板，并针对 Redis 7.x 的新特性进行了适配。


-------

## 新扩展

Pigsty v2.4 提供了一系列的新扩展插件，包括尚未收录在 PGDG 官方仓库中的重要扩展。例如，图数据库插件 Apache AGE，中文分词全文检索插件 zhparser，HTTP插件pgsql-http，可信扩展打包插件 pg_tle ，位图插件 pg_roaringbitmap，以及向量数据库插件 PGVector 的另一种替代实现 pg_embedding ，等等等等。

所有插件都在 EL7 - EL9 上针对 PostgreSQL 12 至 PostgreSQL 16 进行编译打包，不过 EL7 因为编译器版本问题，尚未支持 pg_tle 与 pg_embedding 。这些 RPM 包将由 Pigsty 维护，并放置于 Pigsty 自己的 Yum 源中。

![图片](extension-list.jpg)

例如，您可以使用 AGE 为 PostgreSQL 加装图数据库能力，创建 Graph，并使用 Cypher 查询语言与 SQL 语言一起探索图数据，实现 Neo4j 的效果。

![图片](apache-age.jpg)

再比如，您可以使用 zhparser 中文分词插件，将中文文本与查询拆分为关键词，使用 PostgreSQL 经典的全文检索能力，实现搜索引擎与 ElasticSearch 的效果。

![图片](zhparser.jpg)

更有甚者，你还可以使用 pgsql-http 插件，使用 SQL 接口来发送 HTTP 请求，处理 HTTP 响应。这让数据库可以与外部系统深度集成与交互，打开无尽的想象空间：

![图片](pgsql-http.jpg)

您还可以使用 roaringbitmap ，使用极少的资源，高效地进行计数统计：

![图片](roaringbitmap.jpg)



具体细节就不在此展开了，后面我们会专门出一些文章，介绍这些强力扩展的使用方式。

欢迎大家使用 Pigsty 并提出反馈意见，加讨论群请微信搜索 Pigsty 小助手：pigsty-cc 。






----------------

## v2.4.0

使用 `bash -c "$(curl -fsSL https://get.pigsty.cc/latest)"` 快速上手。

**最新特性**

- PostgreSQL 16 正式发布，Pigsty提供支持。
- 可以监控云数据库，RDS for PostgreSQL，以及 PolarDB，提供全新的 PGRDS 监控面板
- 正式提供商业支持与咨询服务。并发布首个 LTS 版本，为订阅客户提供最长5年的支持。
- 新扩展插件: Apache AGE, openCypher graph query engine on PostgreSQL
- 新扩展插件: zhparser, full text search for Chinese language
- 新扩展插件: pg_roaringbitmap, roaring bitmap for PostgreSQL
- 新扩展插件: pg_embedding, hnsw alternative to pgvector
- 新扩展插件: pg_tle, admin / manage stored procedure extensions
- 新扩展插件: pgsql-http, issue http request with SQL interface
- 新增插件： pg_auth_mon pg_checksums pg_failover_slots pg_readonly postgresql-unit pg_store_plans pg_uuidv7 set_user
- Redis改进：支持 Redis 哨兵监控，配置主从集群的自动高可用。

**API变化**

- 新增参数，`REDIS`.`redis_sentinel_monitor`，用于指定 Sentinel 集群监控的主库列表

**问题修复**

- 修复 Grafana 10.1 注册数据源时缺少 `uid` 的问题

```
MD5 (pigsty-pkg-v2.4.0.el7.x86_64.tgz) = 257443e3c171439914cbfad8e9f72b17
MD5 (pigsty-pkg-v2.4.0.el8.x86_64.tgz) = 41ad8007ffbfe7d5e8ba5c4b51ff2adc
MD5 (pigsty-pkg-v2.4.0.el9.x86_64.tgz) = 9a950aed77a6df90b0265a6fa6029250
```
