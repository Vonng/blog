---
title: 为什么PG将主宰AI时代的数据库
linkTitle: "为什么PG将主宰AI时代的数据库"
date: 2025-12-01
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/)）
summary: >
  上下文窗口经济学，多元持久化的问题，以及零胶水架构的胜利，让 PG 成为 AI 时代的数据库之王。
tags: [PostgreSQL, AI, 数据库]
---

Agent 时代，软件架构的底层逻辑变了。

过去十年，我们为了迁就人类团队的协作边界，搞出了微服务和“多元持久化”（Polyglot Persistence），把系统拆得七零八落。
但在 AI Agent 崛起的新范式下，这种碎片化架构正在成为一种昂贵的“技术负债”。

最稀缺的资源不再是存储或算力，而是 LLM 的**注意力带宽（Context Window）**。

微服务带来的复杂度与碎片化，正在向 AI Agent 征收巨额的“认知税”。
而这剂毒药的解药，只有 PostgreSQL。本文就来聊聊，为什么 PG 会成为 AI 时代的“数据库之王”。

> —— 老冯在 “第八届中国 PG 生态大会” 上的闪电演讲


### 多元持久化：碎片化的认知噩梦

在传统的“最佳实践”中，我们习惯把数据拆得支离破碎：MySQL 存交易，Redis 做缓存，Mongo 存文档，Elasticsearch 搞搜索，Milvus 存向量。

这种设计理念被称作“多元持久化”（Polyglot Persistence） —— 在单个系统中使用多种数据存储技术，以满足不同的数据存储需求

看上去 “用专业的工具做专业的事”很美好，然而这为 AI Agent （以及人类工程师）带来了一个高度对抗性的环境。
Agent 主要在上下文窗口的边界内运作，这个有限的缓冲区——无论是 8k、128k 还是 1M Token——就是 Agent 的全部：短期记忆、工作草稿、接口定义，全部挤在这里。

想象一个典型的跨域查询任务：“找出购买了 X 商品并访问过 Y 页面，且工单情绪负面的用户”。在多元持久化架构下，Agent 必须经历一场“由于数据孤岛导致的消耗战”：

1. **加载驱动与 Schema（烧钱）**：Agent 必须把 MongoDB 的语法、ES 的 DSL、Neo4j 的 Cypher，以及各端的 Schema 定义统统塞进上下文。每一个用于解释 API 的 Token，都是从核心推理能力中窃取的资源。
2. **编写胶水代码（高危）**：Agent 被迫充当“分布式调度器”，编写 Python 代码去连接三个不同的系统，处理网络超时、认证失败和版本不匹配。
3. **应用层 Join（低效）**：数据在不同系统间搬运，Agent 被迫在有限的内存里做数据清洗和连接。

这种“乒乓（Ping-Pong）”架构不仅效率低下，更会导致**上下文过载**。
将所有工具定义塞进一个巨型 Agent 会迅速耗尽预算，当无关的 Schema 和中间数据填满窗口，LLM 的推理能力会被锁死天花板，直接导致“幻觉”飙升。

**上下文经济学偏爱“小而美”的工具，厌恶庞杂的异构系统。**


--------

## PostgreSQL：零胶水架构

解药是什么？是大一统。

我们需要一个能在一个连接、一种方言里解决所有问题的“数据操作系统”。PostgreSQL 凭借其独步天下的扩展性（Extensibility），早已超越了关系型数据库的范畴，进化为全能的数据平台。

PG 的哲学很简单：把复杂性下推（Push-down）到数据库内核，让 Agent 保持轻量。

### 全栈数据融合：三位一体

PG 的扩展生态系统有效吸收了专用系统的能力：

在 PG 生态中，你不需要为了一个新特性去引入一个新的数据库组件：

| **领域** | **扩展**                                      | **替代对象**                   |
|--------|---------------------------------------------|----------------------------|
| 向量搜索   | pgvector, pgvectorscale, vchord             | Milvus, Pinecone, Weaviate |
| 全文检索   | pg_search, pgroonga, zhparser, vchord_bm25  | Elasticsearch              |
| 时序数据   | TimescaleDB                                 | InfluxDB, TDengine         |
| 地理空间   | PostGIS                                     | 专用 GIS 数据库                 |
| 文档存储   | jsonb + GIN 索引                              | MongoDB                    |
| 消息队列   | pgq, pgmq                                   | Kafka                      |
| 缓存     | spat, pgmemched, redis_fdw, unlogged table  | Redis                      |
| 数据湖仓   | pg_duckdb, pg_mooncake, pg_parquet, pg_lake | ClickHouse，StarRocks       |

对 Agent 而言，这意味着语义宇宙的统一。它不需要在 SQL、DSL 和 API 之间精神分裂。

更重要的是**混合检索（Hybrid Search）**的民主化。你可以在一条 SQL 中，同时完成精准过滤、全文关键词检索和向量语义检索。这不是三个系统的拼凑，而是一个引擎内部算子的优雅流水线。

把数据逻辑收敛到单一的、符合 ACID 的 PostgreSQL 引擎中，Agent 不需要关心分布式事务的最终一致性，不需要处理跨服务的数据竞争。事务要么提交，要么回滚。这
种确定性让 Agent 能将数据层视为一个可靠的原子原语（Primitive），而不是一个充满不确定性的分布式混沌系统。

### FDW：零胶水架构与位置透明

如果你确实有外部数据需要访问，又怎么办呢？PG 的 外部数据包装器（FDW） 是 Agent 的“上帝视角”。

通过 FDW，Postgres 可以挂载万物：DuckDB、MySQL、Redis、Kafka、S3 上的 CSV，甚至是 Stripe 的 API 或系统监控指标。

对于 Agent，这实现了完美的位置透明性（Location Transparency）。 Agent 只需要执行 SELECT * FROM sales_data。
它不知道，也不需要知道这份数据到底是躺在 S3 冷存储里，还是在 Snowflake 的数仓里。PG 负责了所有的协议转换和数据搬运。

这就是“零胶水”架构的终极形态：Agent 不再需要写几百行 Python 代码来做 ETL，它只需要发送一段高密度的 SQL 指令，声明自己想要的东西。


### 存储过程：服务器端工具箱

PostgreSQL 支持用 Python、JavaScript、Rust 等二十多种语言编写存储过程。这不仅是功能，更是架构上的降维打击：

- **Token 节省**：复杂的业务逻辑（RAG 流程、数据清洗）固化在数据库函数中，不再占用宝贵的 Prompt 空间。
- **安全性与沙箱**：Agent 调用的是封装好的函数（Tool），而不是裸奔的 SQL，权限边界清晰可控。
- **性能**：逻辑贴着数据跑，消除了网络 IO 开销 —— 通常是最大的性能瓶颈


### 接口标准化：psql 即 IDE

PG 的 SQL 方言 ，`libpq` PG线缆协议几乎是所有 LLM 训练数据中都覆盖的知识。GPT-4 和 Claude 对写 PG 风格的 SQL 驾轻就熟。

通过在 Postgres 上标准化，我们为 Agent 提供了一个确定性的环境。
你甚至不需要 MCP，`pymongo`、`redis-py`、`neo4j-driver` 这些驱动都可以扔掉了。
命令行里的一个 `psql` + 连接串就可以开始工作，接口定义简化为一行： `postgresql://user:password@hostname:5432/db`

仅凭这一个连接，Agent 就能利用 `pg_net` / `pg_curl` 联网，利用 FDW 读写万物，利用 SQL 编排逻辑。甚至是执行 Shell 命令。

**psql 提供 Bash 的功能超集，天然适合成为 AI Agent 的下一个首选执行环境。**



## 结论

**上下文窗口经济学决定了软件架构的未来。** 在智能按 Token 定价、受 Prompt 大小限制的世界里，架构简洁性是终极优化目标。

多元持久化曾是技术能力的象征，现在已成负债——摩擦、延迟、Token 浪费的源头。它割裂 Agent 的现实，迫使 Agent 将认知资源浪费在胶水代码上，而非价值创造。

PostgreSQL 配备 pgvector、pg_net、postgres_fdw 等扩展生态，提供了统一、可编程、"主动"的环境——一个真正的 Agent 操作系统。它允许 Agent 通过单一标准接口（SQL）进行推理（Vector）、行动（Net）和观察（FDW）。

将数据逻辑整合到单一 ACID 引擎中，故障域被坍缩。事务要么提交，要么回滚。这种确定性对 Agent 价值连城——数据层成为可靠原语，而非充满不确定性的分布式混沌。

Databricks 和 Snowflake 的巨额收购是最终验证：**AI 的未来是 Agentic 的，而 Agent 的数据库是 PostgreSQL。**

