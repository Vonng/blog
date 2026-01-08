---
title: "Andy Pavlo：2025 数据库世界年度总结"
date: 2026-01-05
showAuthor: false
authors: [andy-pavlo, vonng]
original: https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html
summary: >
  图灵奖得主 + CMU 教授：2025 数据库圈最犀利的一场对话。关于数据库，LLM，Agent，AI 落地的实际效果，程序员的职业生涯……
tags: [数据库, PostgreSQL]
---


> 原文地址：https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html
>
> 作者：Andy Pavlo，翻译与评论：冯若航


# 2025 数据库世界年度回顾

**作者**: Andy Pavlo - 卡内基梅隆大学  
**发布日期**: 2026 年 1 月 4 日  
**译者注**: 本文翻译自 [CMU Andy Pavlo 教授的博客](https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html)

---

又是一年过去了。本来想多写几篇文章，别光指着年底憋一篇大的，奈何春季学期实在太忙，差点[累死](https://bsky.app/profile/andypavlo.bsky.social/post/3lsvwhx2ixk2v)，根本抽不出时间。不管怎样，还是来聊聊过去这一年里，我眼中数据库领域的重大趋势和事件吧。

这一年，数据库世界发生了许多激动人心的大事："[氛围编程](https://twitter.com/karpathy/status/1886192184808149383)"（Vibe Coding）这个词风靡全网；嘻哈传奇武当派（Wu-Tang Clan）宣布了他们的[时间胶囊项目](https://www.youtube.com/watch?v=4u-bttzVubs)；Databricks 今年依然没有上市，却接连完成了两轮巨额融资。

与此同时，还有一些意料之中的事。Redis 公司在[背刺开源社区](https://redis.io/blog/redis-adopts-dual-source-available-licensing/)一年后，又把[许可证改了回来](https://antirez.com/news/151)（[去年我就预判到了](https://www.cs.cmu.edu/~pavlo/blog/2025/01/2024-databases-retrospective.html#licenses)）。
SurrealDB 发布了漂亮的基准测试数据，但后来被发现是因为他们[压根没把写入刷盘，数据丢了](https://blog.cf8.gg/surrealdbs-ch/)。
还有 Coldplay 能把你的婚姻搞砸（译者注：此处指某CEO外遇被曝）。不过话说回来，Astronomer 倒是把这事儿做成了一个不错的[宣传梗](https://www.youtube.com/watch?v=vich2C-Tl7Q)。

正式开始之前，我想回应一下每年评论区都会出现的问题。总有人问：为什么没提到 [系统X](https://www.reddit.com/r/programming/comments/1hr3xor/databases_in_2024_a_year_in_review/m4vone0/)？为什么不聊聊[数据库Y](https://news.ycombinator.com/item?id=42566660)？
为什么分析里没有[公司Z](https://news.ycombinator.com/item?id=34225377)？原因很简单：我能写的东西有限，除非过去一年发生了什么有趣或值得关注的事，否则没什么好讨论的。
但也不是所有数据库大事件都适合我来评论。比如最近试图[揭露 AvgDatabase CEO 身份](https://twitter.com/CeolinWill/status/2005601763051856293)的事件算公共话题，但 [MongoDB 自杀诉讼案](https://news.ycombinator.com/item?id=46403128)绝对不适合我置喙。

说完这些，咱们开始吧。这些年度总结一年比一年长，先说声抱歉。

往年回顾：

- [2024 数据库年度回顾](https://www.cs.cmu.edu/~pavlo/blog/2025/01/2024-databases-retrospective.html)
- [2023 数据库年度回顾](https://www.cs.cmu.edu/~pavlo/blog/2024/01/2023-databases-retrospective.html)
- [2022 数据库年度回顾](https://www.cs.cmu.edu/~pavlo/blog/2022/12/2022-databases-retrospective.html)
- [2021 数据库年度回顾](https://www.cs.cmu.edu/~pavlo/blog/2021/12/2021-databases-retrospective.html)

---

## PostgreSQL 持续称霸

2021 年，我首次写到 PostgreSQL 正在 [**吞噬整个数据库世界**](https://www.cs.cmu.edu/~pavlo/blog/2021/12/2021-databases-retrospective.html#dominance-of-postgresql)。这一趋势丝毫没有减缓，数据库领域最有趣的进展大多数还是围绕 PostgreSQL 展开。最新版本（[v18](https://www.postgresql.org/about/news/postgresql-18-released-3142/)）于 2025 年 11 月发布，最亮眼的特性是新的[异步 I/O 存储子系统](https://www.cybertec-postgresql.com/en/postgresql-18-and-beyond-from-aio-to-direct-io/)，这将最终让 PostgreSQL 摆脱对操作系统页面缓存的依赖。此外还增加了 [Skip Scan](https://www.pgedge.com/blog/postgres-18-skip-scan-breaking-free-from-the-left-most-index-limitation) 支持：即使缺少前导键（即前缀），查询仍可使用多键 B+ 树索引。查询优化器也有一些改进（例如[消除冗余自连接](https://betterstack.com/community/guides/databases/postgresql-18-new-features/#optimizer-and-query-planning-improvements)）。

资深数据库鉴赏家们肯定会急着指出：这些功能并不是什么开创性的东西，其他数据库早就有了。PostgreSQL 是唯一仍依赖操作系统页面缓存的主流数据库，而 Oracle 早在 2002 年（9i 版本）就[支持 Skip Scan](https://richardfoote.wordpress.com/2008/03/10/index-skip-scan-does-index-column-order-matter-any-more-warning-sign/) 了！那你可能会问：为什么我还说 2025 年数据库领域最火热的动作都发生在 PostgreSQL 身上？

### 收购与发布

原因在于：数据库领域的大部分能量和活动都涌向了 PostgreSQL 相关的公司、产品、项目和衍生系统。过去一年，最火的数据初创公司（[Databricks](https://www.databricks.com/)）花了 [10 亿美元收购了一家 PostgreSQL DBaaS 公司](https://www.wsj.com/articles/databricks-to-buy-startup-neon-for-1-billion-fdded971)（[Neon](https://neon.com/)）。紧接着，全球最大的数据库公司之一（[Snowflake](https://www.snowflake.com/en/)）又花了 [2.5 亿美元买下另一家 PostgreSQL DBaaS 公司](https://www.wsj.com/articles/snowflake-to-buy-crunchy-data-for-250-million-233543ab)（[CrunchyData](https://www.crunchydata.com/)）。然后，地球上最大的科技公司之一（Microsoft）[推出了新的 PostgreSQL DBaaS](https://techcommunity.microsoft.com/blog/adforpostgresql/announcing-azure-horizondb/4469710)（HorizonDB）。Neon 和 HorizonDB 沿用了 Amazon Aurora 在 2010 年代的[原始高层架构](https://doi.org/10.1145/3035918.3056101)：单主节点、计算存储分离。目前 Snowflake 的 PostgreSQL DBaaS 使用的核心架构与标准 PostgreSQL 相同，因为他们基于 [Crunchy Bridge](https://www.crunchydata.com/products/crunchy-bridge) 构建。

### 分布式 PostgreSQL

上述服务都是单主节点架构——应用把写请求发给主节点，主节点再把变更同步给从副本。但 2025 年，有两个新项目宣布要为 PostgreSQL 构建横向扩展（即水平分片）服务。

2025 年 6 月，Supabase 宣布聘请了 [Sugu](https://www.linkedin.com/in/sougou/)（Vitess 联合创始人、前 PlanetScale 联合创始人/CTO）来领导 [Multigres](https://multigres.com/) 项目，目标是为 PostgreSQL 创建类似 Vitess 为 MySQL 提供的分片中间件。Sugu 于 2023 年离开 PlanetScale，蛰伏了两年。现在他大概已经避开了所有法律问题，可以在 Supabase 大展拳脚了。你知道当一个数据库工程师加入公司时，[官宣](https://supabase.com/blog/multigres-vitess-for-postgres)重点在人而不是系统，那就说明这是[大事件](https://simonwillison.net/2025/Jul/1/planetscale-for-postgres/)。[SingleStore 的联合创始人/CTO](https://www.linkedin.com/in/adam-prout-0b347630/) 于 2024 年加入 Microsoft [领导 HorizonDB](https://www.linkedin.com/posts/adam-prout-0b347630_im-happy-to-share-that-im-starting-a-new-activity-7167922823800324096-v1OD)，但微软（错误地）没把这事当回事宣传。Sugu 加入 Supabase，就像 [Ol' Dirty Bastard](https://en.wikipedia.org/wiki/Ol%27_Dirty_Bastard)（RIP，武当派说唱歌手）[假释出狱两年后](https://youtu.be/TDXKvYQ3Xb4)，在出狱第一天就[宣布签约新唱片公司](https://www.nme.com/news/music/odb-3-1383866)。

Multigres 消息发布一个月后，PlanetScale [宣布](https://planetscale.com/blog/planetscale-for-postgres#neki-vitess-for-postgres)了自己的 Vitess-for-PostgreSQL 项目 [Neki](https://www.neki.io/)。PlanetScale 于 2025 年 3 月推出了其初始 [PostgreSQL DBaaS](https://planetscale.com/blog/announcing-metal)，但核心架构就是标准的 [PostgreSQL + pgBouncer](https://planetscale.com/blog/planetscale-for-postgres#performance-and-reliability)。

### 商业格局

随着 2025 年 Microsoft 推出 HorizonDB，所有主要云厂商现在都有了自己认真打造的增强版 PostgreSQL 产品。Amazon 自 2013 年提供 [RDS PostgreSQL](https://en.wikipedia.org/wiki/Amazon_Relational_Database_Service#History)，2017 年推出 [Aurora PostgreSQL](https://aws.amazon.com/about-aws/whats-new/2017/04/announcing-open-preview-of-amazon-aurora-with-postgresql-compatibility/)。Google 在 2022 年推出 [AlloyDB](https://venturebeat.com/data-infrastructure/google-announces-alloydb-a-faster-hosted-version-of-postgresql)。就连老古董 IBM 也从 2018 年就有[云版 PostgreSQL](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-postgresql-relnotes)。Oracle 在 2023 年发布了 [PostgreSQL 服务](https://docs.oracle.com/en-us/iaas/releasenotes/changes/9a4b73b5-d4d6-4c89-bd31-b1fa2098fa34/index.htm)，但有传言说其内部 PostgreSQL 团队在 2025 年 9 月的 [MySQL OCI 裁员](https://www.theregister.com/2025/09/11/oracle_slammed_for_mysql_job/)中被波及。ServiceNow 在 2024 年推出了 [RaptorDB 服务](https://www.investing.com/news/company-news/servicenow-unveils-raptordb-pro-and-future-knowledge-graph-93CH-3609528)，基于其 2021 年对 Swarm64 的[收购](https://www.zdnet.com/article/servicenow-acquires-database-performance-company-swarm64/)。

是的，我知道 Microsoft 在 2019 年收购了 Citus。Citus 在 2019 年被更名为 [Azure Database for PostgreSQL Hyperscale](https://techcommunity.microsoft.com/blog/adforpostgresql/azure-database-for-postgresql---hyperscale-citus-now-generally-available/1014865)，然后在 2022 年又改名为 [Azure Cosmos DB for PostgreSQL](https://devblogs.microsoft.com/cosmosdb/distributed-postgresql-comes-to-azure-cosmos-db/)。但还有个 [Azure Database for PostgreSQL with Elastic Clusters](https://learn.microsoft.com/en-us/azure/postgresql/elastic-clusters/concepts-elastic-clusters) 也使用 Citus，但它和 Citus 驱动的 Azure Cosmos DB for PostgreSQL 不是一回事。等等，我可能搞错了。Microsoft 在 2023 年停用了 [Azure PostgreSQL Single Server](https://techcommunity.microsoft.com/discussions/azuredatabaseforpostgresql/announcement---retiring-azure-postgresql-single-server-in-march-2025-and-introdu/3820887)，但保留了 Azure PostgreSQL Flexible Server。这有点像 Amazon 忍不住在 [DSQL](https://docs.aws.amazon.com/aurora-dsql/latest/userguide/what-is-aurora-dsql.html) 名字里加上"Aurora"一样。不管怎样，至少 Microsoft 这次聪明地把新系统就叫"Azure HorizonDB"（暂时）。

仍有一些独立软件供应商（ISV）的 PostgreSQL DBaaS 公司。[Supabase](https://supabase.com/) 按实例数量可能是最大的。其他包括 [YugabyteDB](https://www.yugabyte.com/)、[TigerData](https://www.tigerdata.com/)（前身为 TimeScale）、[PlanetScale](https://planetscale.com/)、[Xata](https://xata.io/)、[PgEdge](https://www.pgedge.com/) 和 [Nile](https://www.thenile.dev/)。还有一些系统提供 Postgres 兼容的前端，但后端系统并非基于 PostgreSQL（例如 [CockroachDB](https://www.cockroachlabs.com/docs/stable/postgresql-compatibility)、[CedarDB](https://cedardb.com/docs/compatibility/)、[Spanner](https://docs.cloud.google.com/spanner/docs/postgresql-interface)）。Xata 最初架构基于 [Amazon Aurora](https://xata.io/blog/serverless-postgres-platform#:~:text=AWS%20Aurora%20under%20the%20hood)，但今年宣布[切换到自己的基础设施](https://xata.io/blog/xata-postgres-with-data-branching-and-pii-anonymization)。[Tembo](https://www.tembo.io/) 在 2025 年[放弃了托管 PostgreSQL](https://tembo-io.notion.site/Tembo-Cloud-Migration-Guide-1de7c9367d6a80349570e7469ba7f17b)，转型为可以做一些数据库调优的编码 Agent。[ParadeDB](https://www.paradedb.com/) 尚未宣布其托管服务。[Hydra](https://www.hydra.so/) 和 PostgresML 在 2025 年倒闭了（见下文），出局了。还有像 [Aiven](https://aiven.io/) 和 [Tessel](https://www.tessell.com/) 这样的托管公司也提供 PostgreSQL DBaaS，但同时也提供其他系统。

### Andy 的看法

在 Databricks 和 Snowflake 收购 PostgreSQL 公司之后，下一个大买家会是谁还不清楚。再说一遍，每家大科技公司都已经有了 Postgres 产品。EnterpriseDB 是最老牌的 PostgreSQL ISV，但错过了过去五年最重大的两笔 PostgreSQL 收购。不过他们可以继续跟着 Bain Capital 混，或者指望 HPE 收购他们，尽管那个[合作关系](https://community.hpe.com/t5/oem-solutions/recap-hpe-greenlake-launch-discover-2017-madrid/ba-p/6991195)已经是八年前的事了。这种并购格局让人想起 2000 年代末的 OLAP 收购潮，当时 [Vertica](https://investor.hp.com/news-events/news/news-details/2011/HP-to-Acquire-Vertica-Customers-Can-Analyze-Massive-Amounts-of-Big-Data---at-Speed-and-Scale/default.aspx) 是最后一个在公交站等车的，等 [AsterData](https://techcrunch.com/2011/03/03/teradata-buys-aster-data-263-million/)、[Greenplum](https://techcrunch.com/2010/07/06/emc-acquires-data-warehousing-and-analytics-company-greenplum/) 和 [DATAllegro](https://news.microsoft.com/source/2008/07/24/microsoft-to-acquire-datallegro/) 都被收购之后。

两个相互竞争的分布式 PostgreSQL 项目（[Multigres](https://multigres.com/)、[Neki](https://planetscale.com/neki)）的出现是个好消息。这不是第一次有人尝试做这件事。当然，[Greenplum](https://www.vmware.com/products/app-platform/tanzu-greenplum)、[ParAccel](https://en.wikipedia.org/wiki/ParAccel) 和 [Citus](https://www.citusdata.com/) 在 OLAP 领域已经存在二十年了。是的，Citus 支持 OLTP 工作负载，但他们 2010 年起步时[重点是 OLAP](https://www.citusdata.com/blog/2018/06/07/what-is-citus-good-for/#:~:text=we%20focused%20on%20building%20a%20fast%20database%20to%20power%20analytics)。对于 OLTP，15 年前 NTT 的 RiTaDB 项目与 [GridSQL](https://wiki.postgresql.org/wiki/GridSQL) 联手创建了 Postgres-XC。Postgres-XC 的开发者创立了 [StormDB](https://dbdb.io/db/stormdb)，后来被 [Translattice](https://translattice.com/pr/TransLattice_Acquires_StormDB_to_Enhance_TransLattice_Elastic_Database.shtml) 在 2013 年收购。[Postgres-X2](https://postgres-x2.github.io/) 是现代化 XC 的尝试，但开发者放弃了这个努力。Translattice 将 StormDB 开源为 [Postgres-XL](https://en.wikipedia.org/wiki/Postgres-XL)，但项目自 2018 年以来就处于休眠状态。[YugabyteDB](https://www.yugabyte.com/) [诞生于 2016 年](https://www.yugabyte.com/blog/yugabyte-has-arrived/)，可能是部署最广泛的分片 PostgreSQL 系统（而且仍然[开源](https://github.com/yugabyte/yugabyte-db)！），但它是硬分叉，所以只兼容 [PostgreSQL v15](https://docs.yugabyte.com/stable/api/ysql/)。Amazon 在 2024 年宣布了自己的分片 PostgreSQL（[Aurora Limitless](https://aws.amazon.com/blogs/aws/amazon-aurora-postgresql-limitless-database-is-now-generally-available/)），但它是闭源的。

PlanetScale 那帮人[对对手毫不客气](https://youtu.be/CvgIRHhyRQE?t=143)，公开怼 [Neon](https://blog.alexoglou.com/posts/database-decisions/) 和 [Timescale](https://twitter.com/samlambert/status/1984010289348780137)。数据库公司互喷不是什么新鲜事（参见 [Yugabyte vs. CockroachDB](https://www.linkedin.com/posts/bobdoyleyugabyte_cockroach-labs-activity-7311530387271237634-xR78/)）。我猜随着 PostgreSQL 战争升温，以后这种情况会更多。我建议这些小公司[把枪口对准大型云厂商](https://twitter.com/samlambert/status/1996035931057652125)，而不是内斗。

---

## 全民 MCP 时代

如果说 2023 年是[每个 DBMS 都加入向量索引](https://www.cs.cmu.edu/~pavlo/blog/2024/01/2023-databases-retrospective.html#vector)的一年，那么 2025 年就是每个 DBMS 都加入 Anthropic [Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)（MCP）支持的一年。MCP 是一个标准化的客户端-服务器 JSON-RPC 接口，让 LLM 无需自定义胶水代码就能与外部工具和数据源交互。MCP 服务器充当数据库前面的中间件，暴露它提供的工具、数据和操作列表。MCP 客户端（例如 Claude 或 ChatGPT 等 LLM 宿主）发现并使用这些工具，通过向服务器发送请求来扩展模型能力。对于数据库来说，MCP 服务器将这些查询转换为适当的数据库查询（如 SQL）或管理命令。换句话说，MCP 就是那个让数据库和 LLM 互相信任并做生意的[中间人](https://youtu.be/VXuwljCWZMU)，负责把账算清楚。

Anthropic 在 2024 年 11 月[宣布](https://www.theverge.com/2024/11/25/24305774/anthropic-model-context-protocol-data-sources) MCP，但真正火起来是 2025 年 3 月 OpenAI 宣布将在其生态系统中[支持 MCP](https://techcrunch.com/2025/03/26/openai-adopts-rival-anthropics-standard-for-connecting-ai-models-to-data/)。接下来几个月，所有类别的 DBMS 厂商都发布了 MCP 服务器：OLAP（如 [ClickHouse](https://github.com/ClickHouse/mcp-clickhouse)、[Snowflake](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp)、[Firebolt](https://github.com/firebolt-db/mcp-server)、[Yellowbrick](https://yellowbrick.com/blog/application-development/yellowbrick-mcp-server-llms-cutting-code-time-and-speeding-up-etl-development/)）、SQL（如 [YugabyteDB](https://www.yugabyte.com/blog/yugabytedb-mcp-server/)、[Oracle](https://blogs.oracle.com/database/introducing-mcp-server-for-oracle-database)、[PlanetScale](https://planetscale.com/docs/vitess/connecting/mcp)）和 NoSQL（如 [MongoDB](https://www.mongodb.com/company/blog/announcing-mongodb-mcp-server)、[Neo4j](https://github.com/neo4j-contrib/mcp-neo4j)、[Redis](https://github.com/redis/mcp-redis)）。由于没有官方的 Postgres MCP 服务器，每个 Postgres DBaaS 都发布了自己的版本（如 [Timescale](https://github.com/timescale/pg-aiguide)、[Supabase](https://github.com/supabase-community/supabase-mcp)、[Xata](https://xata.io/blog/built-xata-mcp-server)）。云厂商发布了可以与其任何托管数据库服务通信的多数据库 MCP 服务器（如 [Amazon](https://aws.amazon.com/blogs/database/supercharging-aws-database-development-with-aws-mcp-servers/)、[Microsoft](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/tools/azure-sql)、[Google](https://cloud.google.com/blog/products/ai-machine-learning/mcp-toolbox-for-databases-now-supports-model-context-protocol)）。允许单一网关与异构数据库通信，这几乎但还不完全是圣杯级别的[联邦数据库](https://en.wikipedia.org/wiki/Federated_database_system)。据我所知，这些 MCP 服务器的每个请求一次只针对单个数据库，所以跨源连接还是应用自己负责。

除了官方厂商的 MCP 实现外，几乎所有 DBMS 都有[数百个](https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/databases.md)第三方 MCP 服务器实现。有些试图支持多个系统（如 [DBHub](https://dbhub.ai/)、[DB MCP Server](https://github.com/FreePeak/db-mcp-server)）。DBHub 发布了一篇关于 PostgreSQL MCP 服务器的[不错的概述](https://dbhub.ai/blog/state-of-postgres-mcp-servers-2025)。

一个对 Agent 特别有用的有趣功能是数据库分支。虽然不是 MCP 服务器特有的，但分支允许 Agent 快速测试数据库变更而不影响生产应用。Neon 在 2025 年 7 月报告说 Agent [创建了他们 80% 的数据库](https://www.linkedin.com/posts/amitkumarvsingh_ai-agents-are-creating-more-databases-on-activity-7336398117862371328-Q6pO/)。Neon 从一开始就设计为支持[分支](https://dev.to/semaphore/a-first-look-at-neon-a-postgres-database-that-branches-10e6)（Nikita 在系统还叫"[Zenith](https://dbdb.io/db/neon#history)"的时候给我展示过早期演示），而其他系统是后来才加入分支支持的。可以看看 Xata 最近关于数据库分支的[对比文章](https://xata.io/blog/neon-vs-supabase-vs-xata-postgres-branching-part-1)。

### Andy 的看法

一方面，我很高兴现在有了一个标准来将数据库暴露给更多应用。但没人应该信任一个对数据库有不受限访问权限的应用，无论是通过 MCP 还是系统的常规 API。最佳实践仍然是只给账户最小权限。当无人监管的 Agent 可能在你的数据库里撒野时，限制账户权限尤为重要。这意味着给每个账户管理员权限、或所有服务使用同一账户这种偷懒做法，在 LLM 开始胡来时会翻车。当然，如果你的公司把数据库[敞开给全世界](https://www.theregister.com/2025/01/30/deepseek_database_left_open/)的同时还让[最富有公司的股价暴跌 6000 亿美元](https://www.theregister.com/2025/01/30/deepseek_database_left_open/)，那失控的 MCP 请求就不是你最大的问题了。

从我粗略检查的几个 MCP 服务器实现来看，它们都是简单的代理，将 MCP JSON 请求翻译成数据库查询。没有深入的内省来理解请求的目的以及是否合适。总有人会在你的应用里[订购 18000 杯水](https://www.youtube.com/watch?v=DF8Pny3VTg8)，你得确保这不会搞崩你的数据库。一些 MCP 服务器有基本的保护机制（例如 ClickHouse 只允许[只读查询](https://clickhouse.com/docs/use-cases/AI/MCP#clickhouse-mcp-server)）。DBHub 提供了一些额外的[保护](https://dbhub.ai/#why-dbhub)，如限制每个请求返回的记录数和实现查询超时。Supabase 的文档提供了 MCP Agent 的[最佳实践指南](https://supabase.com/docs/guides/getting-started/mcp#recommendations)，但这依赖于人类去遵守。当然，如果你指望人类做对的事，[坏事就会发生](https://www.generalanalysis.com/blog/supabase-mcp-blog)。

企业级 DBMS 已经有了开源系统所缺乏的自动化护栏和其他安全机制，因此它们更好地为 Agent 生态做好了准备。例如，[IBM Guardium](https://www.ibm.com/docs/en/gdp/12.x?topic=overview-guardium) 和 [Oracle Database Firewall](https://www.oracle.com/security/database-security/audit-vault-database-firewall/) 可以识别和阻止异常查询。我不是在为这些大科技公司打广告，我知道未来会有更多 Agent 毁掉生活的例子，比如[不小心删除数据库](https://twitter.com/emil_priver/status/1783399265366052877)。将 MCP 服务器与代理（如连接池）结合，是引入自动化保护机制的好机会。

---

## MongoDB, Inc. 诉 FerretDB Inc.

MongoDB 二十年来一直是 NoSQL 的中坚力量。FerretDB 由 Percona 高管于 2021 年创立，提供一个中间件代理，将 MongoDB 查询转换为 SQL 发送到 PostgreSQL 后端。这个代理让 MongoDB 应用无需重写查询就能切换到 PostgreSQL。

他们共存了几年，直到 2023 年 MongoDB 向 FerretDB 发送了[律师函](https://blocksandfiles.com/wp-content/uploads/2025/04/Letter-from-MongoDB-to-FerretDB_3-Nov-2023-signed.pdf)，指控 FerretDB 侵犯了 MongoDB 的专利、版权和商标，并违反了 MongoDB 对其文档和线协议规范的许可。2025 年 5 月，MongoDB 对 FerretDB 提起联邦诉讼，这封信才公开。他们的主要争议之一是 FerretDB 对外声称拥有 MongoDB 的"[即插即用替代品](https://blog.ferretdb.io/ferretdb-1-0-ga-opensource-mongodb-alternative/#:~:text=drop%2Din%20replacement%20for%20MongoDB)"而没有获得授权。MongoDB 的[法庭文件](https://storage.courtlistener.com/recap/gov.uscourts.ded.89247/gov.uscourts.ded.89247.1.0.pdf)包含所有标准投诉：(1) 误导开发者，(2) 稀释商标，(3) 损害声誉。

故事因 Microsoft 宣布将其 MongoDB 兼容的 [DocumentDB](https://documentdb.io/) 捐赠给 [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-welcomes-documentdb-to-advance-open-developer-first-nosql-innovation) 而更加复杂。项目网站提到 DocumentDB 与 MongoDB 驱动兼容，并旨在"[构建一个 MongoDB 兼容的开源文档数据库](https://documentdb.io/#:~:text=our%20mission%20is%20to%20build%20a%20MongoDB%20compatible%20open%20source%20document%20database)"。Amazon 和 Yugabyte 等其他主要数据库厂商也参与了该项目。粗略一看，这些措辞似乎与 MongoDB 指控 FerretDB 做的事情类似。

### Andy 的看法

我找不到数据库公司因复制 API 而起诉另一家的先例。最接近的是 Oracle 起诉 Google 在 Android 中使用洁净室实现的 Java API。最高法院最终以合理使用为由[判决 Google 胜诉](https://en.wikipedia.org/wiki/Google_LLC_v._Oracle_America%2C_Inc.)，该案影响了重新实现在法律上的处理方式。

我不知道如果真的开庭，这场官司会怎么发展。一群随机挑选的陪审员可能理解 MongoDB 线协议的细节，但他们肯定能理解 FerretDB 最初的名字叫 [MangoDB](https://www.reddit.com/r/programming/comments/qlyalj/mangodb_a_truly_open_source_mongodb_alternative/)。当你只改了一个字母的公司名时，很难让陪审团相信你不是在试图截流客户。更别说这名字本身也不是原创的：已经有另一个叫 [MangoDB](https://dbdb.io/db/mangodb) 的恶搞数据库，把所有东西都写到 `/dev/null`。

说到数据库系统命名，Microsoft 选择"DocumentDB"这个名字很不幸。已经有 [Amazon DocumentDB](https://aws.amazon.com/documentdb/)（顺便说一下，它也与 MongoDB [兼容](https://docs.aws.amazon.com/documentdb/latest/developerguide/compatibility.html#mongodb-80)，但 Amazon 可能为此付了钱）、[InterSystems DocDB](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GDOCDB_intro) 和 [Yugabyte DocDB](https://docs.yugabyte.com/stable/architecture/docdb/)。Microsoft 在 2016 年"Cosmos DB"的原名也是 [DocumentDB](https://auth0.com/blog/documentdb-with-aspnetcore/)。

最后，MongoDB 的法庭文件声称他们"……开创了'非关系型'数据库的发展"。这种说法是错误的。第一批通用 DBMS 就是非关系型的，因为关系模型当时还没被发明。General Electric 的 [Integrated Data Store](https://en.wikipedia.org/wiki/Integrated_Data_Store)（1964）使用[网状数据模型](https://en.wikipedia.org/wiki/Network_model)，IBM 的 [Information Management System](https://en.wikipedia.org/wiki/IBM_Information_Management_System)（1966）使用[层次数据模型](https://en.wikipedia.org/wiki/Hierarchical_database_model)。MongoDB 也不是第一个文档数据库。那个头衔属于 1980 年代末的面向对象数据库（如 [Versant](http://www.versant.com/products/versant-object-database)）或 2000 年代的 XML 数据库（如 [MarkLogic](https://www.progress.com/marklogic)）。当然，MongoDB 是这些方法中最成功的（除了可能是 IMS）。

---

## 文件格式大战

文件格式是数据系统中过去十年基本处于休眠状态的领域。2011 年，Meta 发布了用于 Hadoop 的列式存储格式 [RCFile](https://en.wikipedia.org/wiki/RCFile)。两年后，Meta 改进了 RCFile 并宣布了基于 PAX 的 [ORC](https://orc.apache.org/)（Optimized Record Columnar File）格式。ORC 发布一个月后，Twitter 和 Cloudera 发布了 [Parquet](https://parquet.apache.org/) 的第一个版本。近 15 年后，Parquet 是主导的开源文件格式。

2025 年，有五个新的开源文件格式发布，试图挑战 Parquet 的王座：

* CWI [FastLanes](https://github.com/cwida/FastLanes)
* CMU + 清华 [F3](https://github.com/future-file-format/f3)
* SpiralDB [Vortex](https://vortex.dev)
* 德国人的 [AnyBlox](https://github.com/AnyBlox)
* Microsoft [Amudai](https://web.archive.org/web/20250802074742/https://github.com/microsoft/amudai)

这些新格式加入了 2024 年发布的其他格式：

* Meta [Nimble](https://github.com/facebookincubator/nimble)
* LanceDB [Lance](https://lancedb.com/blog/lance-v2/)
* IoTDB [TsFile](https://tsfile.apache.org/)

[SpiralDB](https://spiraldb.com/) 今年动静最大，宣布将 [Vortex 捐赠给 Linux Foundation](https://www.linuxfoundation.org/press/lf-ai-data-foundation-hosts-vortex-project-to-power-high-performance-data-access-for-ai-and-analytics) 并建立了多组织指导委员会。Microsoft 在 2025 年底某个时候悄悄砍掉了 Amudai（或至少闭源了）。其他项目（FastLanes、F3、Anyblox）是学术原型。Anyblox 今年获得了 [VLDB 最佳论文奖](https://www.linkedin.com/posts/janagiceva_im-thrilled-and-honored-to-share-that-our-activity-7368909487023329281-mhDv/)。

这场新竞争点燃了 Parquet 开发者社区[现代化其功能](https://docs.google.com/document/d/e/2PACX-1vSDHW7gvG8eO6aIxaIVPrZSqYYhtRDb5W1imnbpM4QRYNPsTwEO1fU5z7SEhVIFa4YqWJeSRJ9tcXYS/pub)的热情。可以看看 Parquet PMC 主席（[Julien Le Dem](http://julien.ledem.net/)）对列式文件格式现状的[深入技术分析](https://sympathetic.ink/2025/12/11/Column-Storage-for-the-AI-era.html)。

### Andy 的看法

Parquet 的主要问题不在于格式本身，规范可以而且已经在演进。没人期望组织会重写 PB 级的遗留文件来更新到最新 Parquet 版本。问题在于有太多不同语言的读写库实现，每个都支持规范的不同子集。我们对野生 Parquet 文件的[分析](https://bsky.app/profile/andypavlo.bsky.social/post/3m256lckmec2z)发现，94% 的文件只使用了 2013 年 v1 的功能，尽管它们的创建时间戳在 2020 年之后。这种最低公分母意味着，如果有人使用 v2 功能创建 Parquet 文件，不清楚系统是否有正确的版本来读取它。

我与清华（[曾星宇](https://xinyuzeng.github.io/)、[张焕晨](https://people.iiis.tsinghua.edu.cn/~huanchen/)）、CMU（[Martin Prammer](https://www.cs.cmu.edu/~mprammer/)、[Jignesh Patel](https://csd.cmu.edu/people/faculty/jignesh-patel)）和 [Wes McKinney](https://wesmckinney.com/) 等杰出人才一起开发了 [F3](https://db.cs.cmu.edu/projects/future-file-formats/) 文件格式。我们的重点是解决这个互操作性问题，通过提供原生解码器作为共享对象（Rust crates）和嵌入在文件中的 WASM 版本解码器。如果有人创建了新的编码方式而 DBMS 没有原生实现，它仍然可以通过传递 Arrow 缓冲区使用 WASM 版本读取数据。每个解码器针对单个列，允许 DBMS 对单个文件混合使用原生和 WASM 解码器。AnyBlox 采用了不同的方法，生成单个 WASM 程序来解码整个文件。

我不知道谁会赢得文件格式战争。下一场战役可能是 GPU 支持。SpiralDB 正在做出正确的举措，但 Parquet 的普及性将是一个难以克服的挑战。我甚至还没讨论 [DuckLake](https://ducklake.select/) 如何试图颠覆 Iceberg...

当然，每当讨论这个话题时，总有人会发这张 [xkcd 竞争标准漫画](https://xkcd.com/927/)。我看过了，不用再发给我了。

---

## 杂项动态

数据库是大生意。让我们逐一过一遍！

### 收购

今年的并购很多。Pinecone 在 9 月[更换了 CEO](https://venturebeat.com/data-infrastructure/pinecone-founder-edo-liberty-appoints-googler-ash-as-ceo) 以[准备被收购](https://archive.is/N5h2a)，但之后我没听到任何消息。以下是已经完成的收购：

**DataStax → IBM**
: Cassandra 的老牌公司在年初被 IBM 收购，估值约 [30 亿美元](https://www.linkedin.com/posts/nathanlatka_saas-datastax-activity-7300252058274672640-OQx_/)。

**Quickwit → DataDog**
: Lucene 替代品 [Tantivy](https://github.com/quickwit-oss/tantivy)（全文搜索引擎）背后的领先公司在年初被收购。好消息是 Tantivy 开发仍在继续。

**SDF → dbt**
: 这次收购是 dbt 今年 [Fusion](https://www.getdbt.com/product/fusion) 发布的重要组成部分，使他们能够在 DAG 中进行更严格的 SQL 分析。

**Voyage.ai → MongoDB**
: Mongo 收购了一家早期 AI 公司，以[扩展](https://news.ycombinator.com/item?id=43160731)其云产品中的 RAG 能力。我[最好的学生之一](https://www.linkedin.com/in/wangpatrick57/)在公告前一周加入了 Voyage。他以为没签数据库公司就是背叛"家族"，结果还是进了一家。

**Neon → Databricks**
: 显然，这家 PostgreSQL 公司有竞标战，但 Databricks 以[令人垂涎的 10 亿美元](https://www.wsj.com/articles/databricks-to-buy-startup-neon-for-1-billion-fdded971)拿下。Neon 今天仍作为独立服务存在，但 Databricks 很快将其在生态系统中更名为 [Lakebase](https://www.databricks.com/product/lakebase)。

**CrunchyData → Snowflake**
: 你知道 Snowflake 不会让 Databricks 独占夏天的头条，所以他们花了 2.5 亿美元收购了这家 13 年历史的 PostgreSQL 公司 CrunchyData。Crunchy 近年来招募了顶尖的前 Citus 人才，并在被 Snowflake 收购前扩展其 DBaaS 产品。Snowflake 在 2025 年 12 月宣布其 [Postgres](https://www.snowflake.com/en/product/features/postgres/) 服务的公开预览。

**Informatica → Salesforce**
: 1990 年代的老牌 ETL 公司 Informatica 被 Salesforce 以 [80 亿美元](https://finance.yahoo.com/news/salesforce-buys-informatica-8b-failed-150907984.html)收购。这是在他们 1999 年上市、2015 年被 PE 私有化、2021 年再次上市之后。

**Couchbase → 私募股权**
: 说实话，我从来没理解 Couchbase 2021 年是怎么上市的。我猜是蹭 MongoDB 的热度？Couchbase 几年前通过整合 [UC Irvine AsterixDB 项目](https://www.couchbase.com/press-releases/couchbase-announces-first-commercial-implementation-of-sql-with-n1ql-for-analytics/)的组件做了一些有趣的工作。

**Tecton → Databricks**
: Tecton 为 Databricks 提供了构建 Agent 的额外工具。我的另一个前学生是...

**Tobiko Data → Fivetran**
: 这个团队是两个实用工具的幕后：[SQLMesh](https://sqlmesh.readthedocs.io/) 和 [SQLglot](https://sqlglot.com/)。前者是 dbt 唯一可行的开源竞争者（见下文他们与 Fivetran 的合并）。SQLglot 是一个方便的 SQL 解析器/反解析器，支持基于启发式的查询优化器。这些工具在 Fivetran 以及 SDF 在 dbt 中的组合，在未来几年会是这个领域有趣的技术较量。

**SingleStore → 私募股权**
: 收购 SingleStore 的 PE 公司（[Vector Capital](https://www.vectorcapital.com/)）有管理数据库公司的经验。他们之前在 2020 年[收购了 XML 数据库公司 MarkLogic](https://www.businesswire.com/news/home/20201021005279/en/Vector-Capital-Completes-Acquisition-of-MarkLogic)，并在 2023 年[卖给了 Progress](https://investors.progress.com/news-releases/news-release-details/progress-announces-plans-acquire-marklogic)。

**Codership → MariaDB**
: 在 2024 年被 PE 收购后，MariaDB Corporation 今年开始了收购狂潮。首先是 MariaDB [Galera Cluster](https://mariadb.com/docs/galera-cluster) 横向扩展中间件背后的公司。参见我 2023 年关于 [MariaDB 垃圾场火灾](https://www.cs.cmu.edu/~pavlo/blog/2024/01/2023-databases-retrospective.html#mariadb)的概述。

**SkySQL → MariaDB**
: 然后是第二笔 MariaDB 收购。让大家搞清楚：支持 MariaDB 的原始商业公司在 2010 年叫"SkySQL Corporation"，2014 年更名为"MariaDB Corporation"。然后在 2020 年，MariaDB Corporation 发布了叫 SkySQL 的 MariaDB DBaaS。但因为他们在烧钱，MariaDB Corporation 在 2023 年将 SkySQL Inc. [拆分为独立公司](https://www.businesswire.com/news/home/20231214486927/en/MariaDB-Finalizes-Spinoff-of-SkySQL)。而现在，2025 年，MariaDB Corporation [回购了 SkySQL Inc](https://medium.com/@arbaudie.it/personal-opinion-mariadb-re-acquires-skysql-125181507358)，绕了一圈。这步棋不在我今年的数据库宾果卡上。

**Crystal DBA → Temporal**
: 自动化数据库优化工具公司去了 Temporal，自动优化他们的数据库！很高兴听到 Crystal 创始人、Berkeley 数据库组校友 [Johann Schleier-Smith](https://www.linkedin.com/in/jssmith/) 在那里发展不错。

**HeavyDB → Nvidia**
: 这个系统（前身为 OmniSci，更前身为 MapD）是最早的 GPU 加速数据库之一，可追溯到 2013 年。除了一家并购公司列出的成功交易外，我找不到他们关闭的官方公告。然后我们与 Nvidia 开会讨论潜在的数据库研究合作，一些 HeavyDB 朋友出现了。

**DGraph → Istari Digital**
: Dgraph 之前在 2023 年被 [Hypermode 收购](https://web.archive.org/web/20250806150448/https://hypermode.com/blog/the-future-of-dgraph-is-open-serverless-and-ai-ready)。看起来 Istari 只买了 Dgraph 而不是 Hypermode 的其他部分（或者他们抛弃了）。我还没遇到过任何正在积极使用 Dgraph 的人。

**DataChat → Mews**
: 这是最早的"与你的数据库聊天"系统之一，来自 Wisconsin 大学和现 CMU-DB 教授 Jignesh Patel。但他们被一家欧洲酒店管理 SaaS 收购了。你自己理解这意味着什么吧。

**Datometry → Snowflake**
: Datometry 多年来一直在解决将遗留 SQL 方言（如 Teradata）自动转换为较新 OLAP 系统这个棘手问题。Snowflake 收购他们以扩展其[迁移工具](https://www.snowflake.com/en/blog/accelerate-data-migration-datometry-technology/)。更多信息请参见 Datometry 2020 年的 [CMU-DB 技术讲座](https://www.youtube.com/watch?v=cL1-BIaQSYE&list=PLSE8ODhjZXjagqlf1NxuBQwaMkrHXi-iz&index=23)。

**LibreChat → ClickHouse**
: 像 Snowflake 收购 Datometry 一样，ClickHouse 的这次收购是改善高性能商用 OLAP 引擎开发者体验的好例子。

**Mooncake → Databricks**
: 收购 Neon 后，Databricks 又收购了 Mooncake，使 PostgreSQL 能够读写 Apache Iceberg 数据。更多信息请参见他们 2025 年 11 月的 [CMU-DB 讲座](https://www.youtube.com/watch?v=VqFZyWHGQVM&list=PLSE8ODhjZXjbEeW_bOCZ8c_nx_Jhoz-GW&index=8)。

**Confluent → IBM**
: 这是如何从草根开源项目打造公司的典范。Kafka 最初于 2011 年在 LinkedIn 开发。Confluent 于 2014 年作为独立创业公司拆分出来。七年后的 2021 年 IPO。然后 IBM 写了一张大支票接手。和 DataStax 一样，还需要观察 IBM 会不会对 Confluent 做 IBM 通常对[被收购公司](https://news.ycombinator.com/item?id=43200706)做的事，还是能像 RedHat 那样保持自治。

**Kuzu → ???**
: 来自 Waterloo 大学的嵌入式图数据库被一家未具名公司在 2025 年收购。KuzuDB 公司随后宣布放弃开源项目。[LadybugDB](https://ladybugdb.com/) 项目是维护 Kuzu 代码分叉的尝试。

### 合并

2025 年 10 月，[Fivetran](https://www.fivetran.com/) 和 [dbt Labs](https://www.getdbt.com/) 宣布[合并](https://www.reuters.com/business/a16z-backed-data-firms-fivetran-dbt-labs-merge-all-stock-deal-2025-10-13)为一家公司，这是意想不到的消息。

我能想到的数据库领域上一次合并是 2019 年 [Cloudera 和 Hortonworks 的合并](https://techcrunch.com/2018/10/03/cloudera-and-hortonworks-announce-5-2-billion-merger/)。但那笔交易就是[厨房里被掺了水的货](https://youtu.be/9qkOyiWJIXI)：两家在 Hadoop 市场挣扎求存的公司合并成一家来寻找市场定位（剧透：他们没找到）。2022 年 MariaDB Corporation 通过 [SPAC](https://en.wikipedia.org/wiki/Special-purpose_acquisition_company) 与 [Angel Pond Holdings Corporation](https://mariadb.com/newsroom/press-releases/mariadb-completes-merger-and-lands-on-nyse-as-mrdb/) 的合并在技术上也算，但那笔交易是为了让 MariaDB 走后门上市。而且[投资者](https://www.bizjournals.com/sanjose/news/2022/12/19/mariadb-goes-public-in-spac-merger.html)的结局并不好。Fivetran + dbt 合并不同（也更好），他们是两家互补的技术公司合并成为 ETL 巨头，为不久的将来正式 IPO 做准备。

### 融资

除非我漏掉了或者没有公布，今年数据库初创公司的早期融资轮次没有那么多。向量数据库的热度已经消退，VC 只给 LLM 公司开支票。

* **Databricks** - [40 亿美元 L 轮](https://www.databricks.com/company/newsroom/press-releases/databricks-surpasses-4-8b-revenue-run-rate-growing-55-year-over-year)
* **Databricks** - [10 亿美元 K 轮](https://www.reuters.com/business/databricks-eyes-over-100-billion-valuation-investors-back-ai-growth-plans-2025-08-19/)
* **ClickHouse** - [3.5 亿美元 C 轮](https://clickhouse.com/blog/clickhouse-raises-350-million-series-c-to-power-analytics-for-ai-era)
* **Supabase** - [2 亿美元 D 轮](https://finance.yahoo.com/news/exclusive-supabase-raises-200-million-112154867.html)
* **Astronomer** - [9300 万美元 D 轮](https://www.astronomer.io/press-releases/astronomer-secures-93-million-series-d-funding/)
* **Timescale** - [1.1 亿美元 C 轮](https://www.tigerdata.com/blog/year-of-the-tiger-110-million-to-build-the-future-of-data-for-developers-worldwide)
* **Tessel** - [6000 万美元 B 轮](https://www.tessell.com/press-releases/tessell-raises-60m-series-b-to-expand-ai-driven-multi-cloud-data-ecosystems)
* **ParadeDB** - [1200 万美元 A 轮](https://techcrunch.com/2025/07/15/paradedb-takes-on-elasticsearch-as-interest-in-postgres-explodes-amid-ai-boom/)
* **SpiralDB** - [2200 万美元 A 轮](https://www.axios.com/pro/enterprise-software-deals/2025/09/11/database-startup-spiral-22-million)
* **CedarDB** - [590 万美元种子轮](https://www.munich-startup.de/en/109750/cedardb-secures-53-million-euros/)
* **TopK** - [550 万美元种子轮](https://www.topk.io/blog/seed-round)
* **Columnar** - [400 万美元种子轮](https://columnar.tech/blog/announcing-columnar)
* **SereneDB** - [210 万美元 Pre-Seed](https://tech.eu/2025/12/03/serenedb-lands-21m-to-fuse-search-analytics-and-postgres-into-one-engine/)
* **Starburst** - [金额未公布](https://www.prnewswire.com/news-releases/starburst-announces-strategic-investment-from-citi-302456950.html)

### 改名

我年度总结中的新类别：数据库公司改名。

**HarperDB → Harper**
: 这家 JSON 数据库公司去掉了名字中的"DB"后缀，以强调其作为数据库支持应用平台的定位，类似于 Convex 和 Heroku。我喜欢 Harper 的人。他们 2021 年的 CMU-DB 技术讲座展示了我听过的[最糟糕的](https://twitter.com/andy_pavlo/status/1372673306445365250) DBMS 想法。好在他们意识到这有多糟糕后就放弃了，转向了 LMDB。

**EdgeDB → Gel**
: 这是个明智之举，因为"Edge"这个名字让人以为是边缘设备或服务的数据库（如 [Fly.io](http://fly.io)）。但我不确定"Gel"能传达项目的更高层次目标。可以看看 CMU 校友关于 [Gel 查询语言](https://www.youtube.com/watch?v=RzLo-pdUJ7I&list=PLSE8ODhjZXjbpOIrZheFWxkYG8HD87xW1&index=10)（仍叫 EdgeQL）的 2025 年讲座。

**Timescale → TigerData**
: 这是数据库公司将自己重命名以区别于其主要数据库产品的罕见案例。通常是公司把自己重命名为数据库的名字（如"Relational Software, Inc."改为"Oracle Systems Corporation"，"10gen, Inc."改为"MongoDB, Inc."）。但对公司来说，试图摆脱被视为专业时序数据库的印象，转而被看作通用应用的增强版 PostgreSQL 是有意义的，因为后者的市场规模要大得多。

### 死亡

完全披露：我曾是其中两家失败创业公司的技术顾问。到目前为止，我作为顾问的成功率很糟糕。我也是 [Splice Machine](https://dbdb.io/db/splice-machine) 的顾问，但他们 2021 年就关门了。在我辩护一下：我只和这些公司讨论技术想法，不是商业策略。我确实告诉过 Fauna 他们应该添加 SQL 支持，但他们没采纳我的建议。

**Fauna**
: 一个有趣的分布式 DBMS，基于 [Dan Abadi](https://www.cs.umd.edu/~abadi/) 关于[确定性并发控制](https://vldb.org/pvldb/vol3/R06.pdf)的研究。他们在 NoSQL 潮流退去、Spanner 让事务再次酷起来的时候提供了强一致性事务。但他们有[专有查询语言](https://faunadb-docs.netlify.app/fauna/current/learn/query/)，还在 GraphQL 上下了大赌注。

**PostgresML**
: 这个想法看起来很明显：让人们在 PostgreSQL DBMS 内部运行 ML/AI 操作。挑战在于说服人们把现有数据库迁移到他们的托管平台。他们推广 [pgCat](https://github.com/postgresml/pgcat) 作为镜像数据库流量的代理。其中一位联合创始人加入了 Anthropic。另一位联合创始人创建了新的代理项目 [pgDog](https://pgdog.dev/)。

**Derby**
: 这是最早用 Java 编写的 DBMS 之一，可追溯到 1997 年（最初叫"Java DB"或"JBMS"）。IBM 在 2000 年代将其捐赠给 Apache Foundation，并更名为 Derby。2025 年 10 月，项目宣布系统将进入"只读模式"，因为没人再积极维护了。

**Hydra**
: 虽然这家 DuckDB-inside-Postgres 创业公司没有官方公告，但联合创始人和员工已经分散到其他公司了。

**MyScaleDB**
: 这是 ClickHouse 的一个分叉，添加了使用 Tantivy 的向量搜索和全文索引。他们在 2025 年 5 月宣布关闭。

**Voltron Data**
: 这本应该是数据库公司的超级组合。想象一下 [Run the Jewels](https://youtu.be/G-S9mtYowPY) 级别的重量级阵容。你有来自 Nvidia Rapids 的顶尖工程师、Apache Arrow 和 Python Pandas 的[发明者](https://en.wikipedia.org/wiki/Wes_McKinney)，以及来自 [BlazingSQL](https://github.com/BlazingDB/blazingsql) 的秘鲁 GPU 奇才。再加上来自顶级公司的 [1.1 亿美元 VC 资金](https://waldencatalyst.com/blog/founder-spotlight-voltron-data)，其中包括未来的 Intel CEO（也是[卡内基梅隆大学董事会成员](https://en.wikipedia.org/wiki/Lip-Bu_Tan)）。他们构建了一个 GPU 加速数据库（Theseus），但未能及时推出。

最后，虽然不是商业公司，但我不得不提一下 [IBM Research Almaden](https://en.wikipedia.org/wiki/IBM_Research#Almaden_in_Silicon_Valley) 的[关闭](https://www.siliconvalley.com/2025/07/10/ibm-san-jose-tech-data-ai-internet-property-real-estate-economy-web/)。IBM 于 1986 年建造了这个园区，几十年来一直是数据库研究的圣地。我 [2013 年在 Almaden 面试](https://twitter.com/andy_pavlo/status/306455280823177216)时，发现那里的风景很美。IBM Research 数据库组已不是[当年的样子](https://dl.acm.org/doi/10.1145/126482.126493)了。但这片神圣的数据库土地的校友名单令人印象深刻：[Rakesh Agrawal](https://en.wikipedia.org/wiki/Rakesh_Agrawal_(computer_scientist))、[Donald Chamberlin](https://en.wikipedia.org/wiki/Donald_D._Chamberlin)、[Ronald Fagin](https://en.wikipedia.org/wiki/Ronald_Fagin)、[Laura Haas](https://en.wikipedia.org/wiki/Laura_M._Haas)、[Mohan](https://en.wikipedia.org/wiki/C._Mohan)、[Pat Selinger](https://en.wikipedia.org/wiki/Patricia_Selinger)、[Moshe Vardi](https://en.wikipedia.org/wiki/Moshe_Vardi)、[Jennifer Widom](https://en.wikipedia.org/wiki/Jennifer_Widom) 和 [Guy Lohman](https://scholar.google.com/citations?user=wUkamYwAAAAJ&hl=en)。


### Andy 的看法

有人[声称](https://news.ycombinator.com/item?id=42571405)我根据支持公司筹集的资金多少来判断数据库的质量。这显然不对。我追踪这些动态是因为数据库研究领域竞争激烈、能量充沛。我不仅要与其他大学的学者"竞争"，大科技公司和小型创业公司也在推出我需要关注的有趣系统。除了 Microsoft Research 仍在积极招聘顶尖人才并做出令人难以置信的工作外，行业研究实验室已不是当年的样子了。

我[在 2022 年预测](https://www.cs.cmu.edu/~pavlo/blog/2022/12/2022-databases-retrospective.html#:~:text=fate%20of%20database%20start%2Dups) 2025 年会有大量数据库公司倒闭。是的，今年的倒闭比往年多，但规模没有我预期的那么大。

Voltron 的死亡和 HEAVY 的类似收购整合似乎延续了 GPU 加速数据库不可行的趋势。[Kinetica](https://twitter.com/KineticaHQ/status/1988983193870156171) 多年来一直在榨取那些政府合同，[Sqream](https://sqream.com/) 似乎仍然活着。这些公司仍然是小众的，没有人能够在 CPU 驱动的 DBMS 的主导地位上取得重大突破。我不能说是谁或什么，但你会在 2026 年听到厂商的一些重大 GPU 加速数据库公告。这也进一步证明了 OLAP 引擎的商品化：现代系统在低级操作（扫描、连接）上已经变得如此之快，以至于它们之间的性能差异可以忽略不计，所以区分一个系统和另一个系统的是用户体验和优化器生成的查询计划质量。

私募股权（PE）公司收购 Couchbase 和 SingleStore 可能预示着数据库行业的未来趋势。当然，PE 收购以前也发生过，但它们似乎都是近期的：(1) 2020 年的 [MarkLogic](https://www.vectorcapital.com/investments/case-study/marklogic)，(2) 2021 年的 [Cloudera](https://techcrunch.com/2021/06/01/cloudera-to-go-private-as-kkr-cdr-grab-it-for-5-3b/)，(3) 2023 年的 [MariaDB](https://techcrunch.com/2024/09/10/mariadb-goes-private-with-new-ceo-as-k1-closes-acquisition/)。2020 年之前我只能找到 2007 年的 [SolidDB](https://www.channelinsider.com/tech-companies/ibm-buys-database-software-firm/) 和 2015 年的 [Informatica](https://www.aakashg.com/story-informatica-second-ipo/)。PE 收购可能会取代停滞不前的数据库公司被控股公司收购、榨取维护费直到永远的趋势（Actian、Rocket）。甚至 Oracle 在 30 年前收购 [RDB/VMS](https://www.oracle.com/database/technologies/related/rdb.html) 后仍在从中赚钱！

最后，向 [Nikita Shamgunov](https://www.linkedin.com/in/nikitashamgunov) 致敬。据我所知，他是唯一一个联合创立的两家数据库公司（[SingleStore](https://hackernoon.com/founder-interviews-nikita-shamgunov-of-memsql-8a9ca8d33552) 和 [Neon](https://www.madrona.com/building-a-modern-database-neon-nikita-shamgunov-serverless-postgres/)）都在同一年被收购的人。就像 DMX（RIP）在同一年发行了两张冠军专辑（[It's Dark and Hell Is Hot](https://en.wikipedia.org/wiki/It%27s_Dark_and_Hell_Is_Hot)、[Flesh of My Flesh](https://en.wikipedia.org/wiki/Flesh_of_My_Flesh,_Blood_of_My_Blood)）一样，我认为短期内不会有人打破 Nikita 的记录。

---

## 巅峰男性的极致表现

对数据库界 OG（元老）Larry Ellison 来说，这是辉煌的一年。这位 81 岁的老人在一年内取得的成就比大多数人一辈子都多。我按时间顺序一一道来。

Larry 年初时是全球第三富有的人。比 Mark Zuckerberg 身价低这件事让他夜不能寐。有人说 Larry 失眠是因为他[买了一家著名的英国酒吧](https://www.bbc.com/news/uk-england-oxfordshire-67221202)后改变了饮食，吃了更多的派。但我向你保证，Larry 30 年来的"[素食海鲜](https://tech.yahoo.com/science/articles/80-old-billionaire-larry-ellison-105236014.html)"饮食没有改变。然后在 2025 年 4 月，消息传来：Larry 成为了[全球第二富有的人](https://www.msn.com/en-in/autos/photos/larry-ellison-becomes-second-richest-person-beats-zuckerberg-bezos-after-oracle-stock-soars/ar-AA1GKdbu)。他睡得好了一点，但还是不够。他生活中还有很多事让他压力很大。比如，Larry 终于决定出售他那辆稀有的、半合法上路的 [McLaren F1 超级跑车](https://www.forbes.com/sites/maryroeloffs/2025/08/05/larry-ellisons-old-mclaren-f1-could-break-a-sales-record/)，附带手套箱里的原始车主手册。

2025 年 7 月，Larry 发布了他 13 年来的[第三条推文](https://twitter.com/larryellison/status/1945229587929337947)（Larry 爱好者如我称之为"#3"）。这是关于 Larry 在牛津大学附近建立的 [Ellison Institute of Technology](https://eit.org/)（EIT）的更新。从名字 EIT 及其与牛津的关联来看，它听起来像是一个纯粹的研究性非营利机构，类似于斯坦福的 [SRI](https://en.wikipedia.org/wiki/SRI_International) 或 CMU 的 [SEI](https://en.wikipedia.org/wiki/Software_Engineering_Institute)。但事实证明，它是一系列由加州有限责任公司持有的营利性公司的伞形组织。当然，一群怪人回复 #3，承诺[区块链驱动的冷冻保存](https://twitter.com/SFCryptoRounder/status/1946047224779030564)或[室温超导体](https://twitter.com/JackSarfatti/status/1975985052204101709)。Larry 告诉我他忽略那些。还有像[这位仁兄](https://twitter.com/aseemchandra/status/1945509650201301304)才是懂的。

年度（可能是世纪）最大的数据库新闻在 2025 年 9 月 10 日星期三下午约 3:00（美东时间）降临。在等待了几十年之后，Larry Joseph Ellison 终于加冕为[全球首富](https://www.theguardian.com/technology/2025/sep/10/larry-ellison-dislodges-elon-musk-as-worlds-richest-person)。[$ORCL](https://finance.yahoo.com/quote/ORCL/) 当天上午股价上涨 40%，由于 Larry 仍持有公司 40% 的股份，他的估计总身价达到 [3930 亿美元](https://www.bbc.com/news/articles/cx2rp992y88o)。从这个角度来看，这不仅使他成为世界上最富有的人，也是人类历史上最富有的人。[John D. Rockefeller](https://en.wikipedia.org/wiki/John_D._Rockefeller) 和 [Andrew Carnegie](https://en.wikipedia.org/wiki/Andrew_Carnegie)（是的，CMU 的那个"C"）经通胀调整后的峰值净资产分别只有 [3400 亿美元](https://www.buysidedigest.com/insights/the-top-10-wealthiest-historical-figures-adjusted-for-inflation/)和 [3100 亿美元](https://www.celebritynetworth.com/richest-businessmen/richest-billionaires/andrew-carnegie-net-worth/)。

在 Larry 登顶世界之巅的同时，Oracle 还参与了[收购控制 TikTok 的美国公司](https://www.npr.org/2025/12/18/nx-s1-5648844/tiktok-deal-oracle-trump)的交易，Larry 还[资助 Paramount](https://variety.com/2025/tv/news/paramount-skydance-larry-ellison-irrevocable-personal-guarantee-warner-bros-discovery-1236614728/)（由他第四次婚姻的儿子控制）竞标[收购华纳兄弟](https://www.nytimes.com/2025/12/24/business/media/larry-david-ellison-warner-bros-discovery-cbs.html)。美国总统甚至敦促 Larry [控制 CNN 新闻部门](https://www.theguardian.com/us-news/2025/nov/20/warner-bros-discovery-takeover-paramount-skydance-larry-ellison)，因为 Larry 是 Paramount 的大股东。

### Andy 的看法

我都不知道从哪里开始。当然，当我得知 Larry Ellison 成为世界首富，而且全靠数据库，我[深受鼓舞](https://twitter.com/andy_pavlo/status/1965865919223312495)，终于有好事发生在我们生活中了。我不在乎 Oracle 的股票是被[大肆宣传的 AI 数据中心交易](https://www.investors.com/news/technology/oracle-stock-orcl-ai-analyst-targets/)而不是传统软件业务人为抬高的。我不在乎他在两个月内[个人损失了 1300 亿美元](https://www.bloomberg.com/news/articles/2025-11-21/oracle-slump-sends-ellison-sliding-down-ranks-of-world-s-richest)后排名下滑。这就像你我[把一个月工资全砸在 FortuneCoins 上](https://www.reddit.com/r/gambling/comments/1j4xby2/blew_my_whole_paycheck/)。有点疼，我们不得不吃两周混着从 Taco Bell 顺来的过期辣酱包的米饭和豆子，但我们会没事的。

有人声称 Larry [与普通人脱节](https://news.ycombinator.com/item?id=45413203)。或者说他迷失了方向，因为他参与了与数据库不直接相关的事情。他们指出他的[夏威夷机器人农场以 24 美元/磅的价格出售生菜](https://beatofhawaii.com/the-most-expensive-lettuce-in-hawaii-billionaire-larry-ellisons-24-lb-experiment/)（41 欧元/公斤）。或者 81 岁的人[不会有天然金发](https://assets.sfstandard.com/image/994911177489/image_cooaesgkll0v99j57e84lobk7k/-S3840x2560-FPNG)。

事实是，Larry Ellison 已经征服了企业数据库世界、[竞技帆船](https://sg.finance.yahoo.com/news/why-oracle-founder-larry-ellison-205016907.html)和[科技兄弟养生水疗](https://www.businessinsider.com/larry-ellison-hawaii-wellness-spa-sensei-lanai-photos-2021-2)。显而易见的下一步是接管一个每天有成千上万人在机场等候时观看的有线电视频道。每次我和 Larry 交流，他都明确表示他一点也不在乎别人怎么说或怎么想他。他知道他的[粉丝爱他](https://twitter.com/HolgersenTobias/status/1945239198572712323)。他（新）妻子爱他。归根结底，这才是最重要的。

---

## 结语

在结束之前，我想简单致敬几位。首先是 PT，在监狱里用 Turso [保持数据库技术的精进](https://turso.tech/blog/working-on-databases-from-prison)（出来再见）。向 JT 表示慰问，因为私藏 [KevoDB](https://github.com/KevoDB/kevo) 数据库小三而[丢了工作](https://twitter.com/canoozie/status/1952305339824574576)。我和我的博士生们也有一个新的[创业公司](https://sydht.ai/)。希望很快能分享更多。一言为定。

---

*原文链接：https://www.cs.cmu.edu/~pavlo/blog/2026/01/2025-databases-retrospective.html*



--------

## 老冯评论

Andy Pavlo 这篇年终总结写得确实精彩，嘻哈梗玩得飞起，
这篇文章是 2025 年数据库领域最好的年终总结，没有之一。
他的信息量、洞察力和文笔都是顶级的。

作为一个在战壕里的前沿创业者，老冯也从不同的角度来聊聊两个主要问题。


### 一、PostgreSQL 赢了，然后呢？

早在从十年前，老冯就坚定的相信 PostgreSQL 一定会赢，但那时候这么说，也就自说自话罢了，应者寥寥。
到两年前，老冯写了《PostgreSQL 正在吞噬数据库世界》，在 HackerNews 上火了，点燃了 PG 社区的激情。一些观点成为了社区的共识。
再到今天，基本上 PostgreSQL 主宰数据库世界这件事，在全球已经是行业共识了。无数资本用真金白银证明了这一点。
但是老冯却感觉有点空虚，PG 确实赢了，然后呢？

但如果你仔细看这份胜利的账单，会发现一个尴尬的事实：项目赢了，公司却没了。
Neon 卖给了 Databricks，CrunchyData 卖给了 Snowflake，Citus 早就归了微软。
创始人们套现离场，云厂商则顺手把这些团队里最懂 PostgreSQL 的人才一网打尽。
剩下还在独立运营的 PostgreSQL ISV 屈指可数，而且每一家头上都悬着"何时被招安"的达摩克利斯之剑。

Andy 在文章里提了一句很有意思的话：这些小公司应该联合起来，把枪口对准云厂商，而不是自己先打起来。
PlanetScale 怼 Neon，Yugabyte 怼 CockroachDB——打来打去，最后便宜的是坐山观虎斗的 AWS 和 Google。
真正的对手是那些拿着开源代码做托管服务、一分钱不回馈社区、还用规模优势碾压所有独立厂商的巨头。

PostgreSQL 生态里需要一个真正体现自由软件精神的发行版立起来。
不是又一个 DBaaS，不是又一个被 VC 催着变现的创业公司，而是一个像 Debian 之于 Linux 那样的存在——坚持开放、坚持可自托管、坚持用户对自己数据的完全掌控权。
当所有人都被云厂商赶进围墙花园的时候，这样的项目就是那扇还没上锁的门。而老冯的 Pigsty，要做的就是这样的事情。


### 二、分布式的 PG 是伪需求吗？

Andy 花了不少笔墨写 Multigres 和 Neki 的对决，但他没有触及一个更根本的问题：为什么之前所有的分布式 PostgreSQL 尝试都 “失败了”？

Postgres-XC/XL 烂尾了，Citus 被微软收购后创新停滞，YugabyteDB 作为硬分叉永远追不上主版本。这些项目的命运难道只是偶然吗？

我的观点可能有些刺耳：在当下的硬件条件下，分布式 OLTP 数据库本身很可能是个伪需求。

问题在于，"单机"的定义已经被硬件革命彻底改写了。Gen5 NVMe SSD 单卡能到 256TB、几百万级的 IOPS；顶配服务器七八百个核、几TB 内存，全闪单机1U 放进 8个PB。
现在几乎没有哪个 TP 数据库能把这些恐怖的硬件性能榨干。硬件的进步让集中式数据库的容量和吞吐达到了前所未有的高度，而分布式数据库还在解决一个十年前的问题。

像 OpenAI 这样的独角兽巨无霸，用一套一主四十从的经典主从架构 PG 集群撑起了业务。那么普通用户使用 “分布式” 的意义又在哪里？

分布式不是死路，但它的生态位比很多人想象的小得多。 真正需要分布式的场景确实存在，但那是极少数的头部玩家 —— 人家大概率自己也就直接应用层分片搞了。
对于绝大多数企业来说，与其折腾分布式，不如把一套 PostgreSQL 用好、调好、管好。
























