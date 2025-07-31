---
title: PostgreSQL 17 beta1 发布！
date: 2024-05-24
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [微信](https://mp.weixin.qq.com/s/3EBoAHWEI6zZ-T0nNQsk4Q)
summary: >
  PostgreSQL 全球开发组宣布，PostgreSQL 17 的首个 Beta 版本现已开放，这次 PG 真的是把牙膏管给挤爆啦！
tags: [PostgreSQL]
---


PostgreSQL 全球开发组宣布，PostgreSQL 17 的首个 Beta 版本现已开放[下载](https://www.postgresql.org/download/)。
这一版本包含了 PostgreSQL 17 正式发布时所有功能的预览，但在 Beta 测试期间，某些细节可能会有所调整。

您可以在[发布说明](https://www.postgresql.org/docs/17/release-17.html)中找到关于 PostgreSQL 17 的所有功能和变更的信息：

https://www.postgresql.org/docs/17/release-17.html

秉承 PostgreSQL 开源社区的精神，我们强烈支持您在您的系统上测试 PostgreSQL 17 的新功能，帮助我们发现和修复潜在的错误或其他问题。
虽然我们不建议在生产环境中运行 PostgreSQL 17 Beta 1，但我们希望您能在测试环境中运行此 Beta 版本，并尽可能模拟您的实际工作负载。

社区将持续确保 PostgreSQL 17 作为世界上最先进的开源关系型数据库的稳定性和可靠性，但这离不开您的测试与反馈。
详情请参阅我们的 [Beta 测试流程](https://www.postgresql.org/developer/beta/)，以及您可以如何作出贡献：https://www.postgresql.org/developer/beta/

------

## PostgreSQL 17 亮点功能

### 查询和写入性能改善

PostgreSQL 17 最近的版本与构建，持续致力于整体的系统性能优化。负责回收存储空间的 PostgreSQL [Vacuum](https://www.postgresql.org/docs/17/routine-vacuuming.html) 进程使用了新的内部数据结构，使得垃圾回收过程的内存使用减少，最高可以减少 20 倍，同时减少了执行所需的时间。
此外 Vacuum 进程不再受到 `1GB` 内存的使用限制，而由 [`maintenance_work_mem`](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM) 来控制，这意味着您可以为 Vacuum 进程分配更多资源。

这个版本引入了流式 I/O 接口，使得执行顺序扫描和运行 [`ANALYZE`](https://www.postgresql.org/docs/17/sql-analyze.html) 的性能有所提高。
PostgreSQL 17 还新增了配置参数，可控制 [事务、子事务和 multixact 缓冲区](https://www.postgresql.org/docs/17/runtime-config-resource.html#GUC-MULTIXACT-MEMBER-BUFFERS) 的大小。

PostgreSQL 17 现在可以同时利用 Planner 的统计信息与 [公共表表达式 CTE](https://www.postgresql.org/docs/17/queries-with.html)（即 [`WITH` 查询](https://www.postgresql.org/docs/17/queries-with.html)）结果中的排序顺序，进一步优化这些查询的速度。
此外，这个版本显著提高了带有 `IN` 子句的查询，在使用 [B-tree 索引](https://www.postgresql.org/docs/17/indexes-types.html#INDEXES-TYPES-BTREE) 时的查询执行时间。
从这个版本开始，对于那些带有 `NOT NULL` 约束的列，如果查询中带有冗余的 `IS NOT NULL` 语句，PostgreSQL 会直接把它优化掉，同理，那些带有 `IS NULL` 的查询也会直接优化掉，PostgreSQL 17 还支持并行构建 [BRIN](https://www.postgresql.org/docs/17/brin.html) 索引。

高并发写入类的工作负载，可以显著受益于 PostgreSQL 17 的预写日志（[WAL](https://www.postgresql.org/docs/17/wal-intro.html)）锁管理改进，测试显示，性能提升 **最多高达两倍**。

最后，PostgreSQL 17 添加了更多显式的 SIMD 指令，比如为 [`bit_count`](https://www.postgresql.org/docs/17/functions-bitstring.html) 函数启用 AVX-512 指令支持。

------

### 分区和分布式工作负载增强

PostgreSQL 17  的分区管理更为灵活，新增了**拆分**与**合并**分区的能力，并允许分区表使用 **身份列（Identity Column）** 和**排它约束**（Exclude Constraints）。
此外，[PostgreSQL 外部数据包装器](https://www.postgresql.org/docs/17/postgres-fdw.html)（[`postgres_fdw`](https://www.postgresql.org/docs/17/postgres-fdw.html)）现在可以将 `EXISTS` 和 `IN` 子查询下推到远端服务器，从而提升性能。

PostgreSQL 17 为逻辑复制添加了新功能，使其在高可用架构和大版本升级中更加易用。
从 PostgreSQL 17 使用  [`pg_upgrade`](https://www.postgresql.org/docs/17/pgupgrade.html) 升级到更高版本时，不再需要删除 [逻辑复制槽](https://www.postgresql.org/docs/17/logical-replication-subscription.html#LOGICAL-REPLICATION-SUBSCRIPTION-SLOT) 了，从而避免了升级后需要重新同步数据的麻烦。
此外，你还可以控制逻辑复制的 Failover 过程，为高可用性架构中管理 PostgreSQL 提供了更好的可控制性。PostgreSQL 17 还允许逻辑复制的订阅者使用 `hash` 索引进行查找，并引入了 `pg_createsubscriber` 命令行工具，用于在使用物理复制的副本从库上创建逻辑复制。

------

### 开发者体验

PostgreSQL 17 继续深化了对 SQL/JSON 标准的支持，新增了 `JSON_TABLE` 功能，可以将 JSON 转换为标准的 PostgreSQL 表，以及 SQL/JSON 构造函数（`JSON`、`JSON_SCALAR`、`JSON_SERIALIZE`）和查询函数（`JSON_EXISTS`、`JSON_QUERY`、`JSON_VALUE`）。
值得注意的是，这些功能最初计划在 PostgreSQL 15 中发布，但出于设计权衡考虑，在 Beta 期间被撤回 —— 这也是我们希望请您在 Beta 期间帮忙测试新功能的原因之一！此外，PostgreSQL 17 为 `jsonpath` 的实现增添了更多功能，包括将 JSON 类型的值转换为各种不同特定数据类型的能力。

[`MERGE`](https://www.postgresql.org/docs/17/sql-merge.html) 命令现在支持 `RETURNING` 子句了，让您可以在同一条命令中进一步处理修改过的行。
您还可以使用新的 `merge_action` 函数查看 `MERGE` 命令修改了哪一部分。
PostgreSQL 17 还允许使用 `MERGE` 命令更新视图，并新增了 `WHEN NOT MATCHED BY SOURCE` 子句，允许用户指定当源中的行没有任何匹配时，应该执行什么操作。

[`COPY`](https://www.postgresql.org/docs/17/sql-copy.html) 命令用于高效地从 PostgreSQL 批量加载与导出数据。在 PostgreSQL 17 中，**导出大行时的性能最多有两倍的提升**。
此外，当源编码与目标编码相匹配时，`COPY` 的性能也有所提升。COPY 新增了一个 `ON_ERROR` 选项，即使插入行时出现错误也可继续进行。
此外在 PostgreSQL 17 中，驱动程序可以利用 libpq API 使用 [异步和更为安全的查询取消方法](https://www.postgresql.org/docs/17/libpq-cancel.html)。

PostgreSQL 17 引入了内置的排序规则提供程序，该提供程序提供与 `C` 排序规则类似的排序语义，但编码为 `UTF-8` 而非 `SQL_ASCII`。这种新的排序规则提供了不变性保证，确保您的排序结果在不同系统上都不会改变。

------

### 安全功能

PostgreSQL 17 新增了一个新的连接参数 `sslnegotation`，允许 PostgreSQL 在使用 [ALPN](https://en.wikipedia.org/wiki/Application-Layer_Protocol_Negotiation) 时直接进行 TLS 握手，减少一次网络往返。PostgreSQL 会在 ALPN 目录中注册为 `postgresql`。

这个版本引入了新的 EventTrigger 事件 —— 当用户认证时触发。并且在 libpq 中提供了一个新的名为 `PQchangePassword` 的 API，可以在客户端侧自动对密码取哈希，以防止在服务器中意外记录下明文密码。

PostgreSQL 17 增加了一个新的 [预定义角色](https://www.postgresql.org/docs/17/predefined-roles.html)，名为 `pg_maintain`，赋予用户执行 `VACUUM`、`ANALYZE`、`CLUSTER`、`REFRESH MATERIALIZED VIEW`、`REINDEX` 和 `LOCK TABLE` 的权限，
并确保  `search_path` 对于 `VACUUM`、`ANALYZE`、`CLUSTER`、`REFRESH MATERIALIZED VIEW` 和 `INDEX` 等维护操作是安全的。
最后，用户现在可以使用 `ALTER SYSTEM` 来设置系统无法识别的未定义配置参数了。

------

### 备份与导出管理

PostgreSQL 17 可以使用 [`pg_basebackup`](https://www.postgresql.org/docs/17/app-pgbasebackup.html) 进行增量备份，并增加了一个新的实用工具 [`pg_combinebackup`](https://www.postgresql.org/docs/17/app-pgcombinebackup.html)，用于备份恢复过程中将备份合并。
该版本为 [`pg_dump`](https://www.postgresql.org/docs/17/app-pgdump.html) 新增了一个参数项 `--filter`，允许您指定一个文件来进一步指定在 dump 过程中要包含或排除哪些对象。

------

### 监控

[`EXPLAIN`](https://www.postgresql.org/docs/17/sql-explain.html) 命令可以提供有关查询计划和执行详情的信息，现在它新增了两个选项：`SERIALIZE` 会显示将数据序列化为网络传输形式时的耗时；`MEMORY` 会报告优化器内存使用情况。此外，`EXPLAIN` 现在还可以显示花费在 I/O 块读写上的时间。

PostgreSQL 17 标准化了 [`pg_stat_statements`](https://www.postgresql.org/docs/17/pgstatstatements.html) 中 `CALL` 的参数，减少了频繁调用的存储过程所产生的记录数量。
此外，[`VACUUM` 进度报告](https://www.postgresql.org/docs/devel/progress-reporting.html#VACUUM-PROGRESS-REPORTING) 现在会显示索引垃圾回收的进度。
PostgreSQL 17 还引入了一个新视图，[`pg_wait_events`](https://www.postgresql.org/docs/17/view-pg-wait-events.html)，提供关于等待事件的描述，可以与 `pg_stat_activity` 共同使用，以便深入了解活动会话出现等待的原因。
此外，[`pg_stat_bgwriter`](https://www.postgresql.org/docs/17/monitoring-stats.html#MONITORING-PG-STAT-BGWRITER-VIEW) 视图中的一些信息，现在被拆分到新的 [`pg_stat_checkpointer`](https://www.postgresql.org/docs/17/monitoring-stats.html#MONITORING-PG-STAT-CHECKPOINTER-VIEW) 视图中了。



------

## 其他功能

PostgreSQL 17 还有许多其他新功能与改进，很多改进都可能会对您的用例有所帮助。请参阅[发布说明](https://www.postgresql.org/docs/17/release-17.html)以获取完整的新功能和变更列表：

https://www.postgresql.org/docs/17/release-17.html



------

## 错误和兼容性测试

每个 PostgreSQL 版本的稳定性，在很大程度上依赖于诸位 PG社区用户，您可以用你们的工作负载和测试工具来测试即将发布的版本，以便在 PostgreSQL 17 正式发布前发现错误并完成回归。由于这是一个 Beta 版本，针对数据库行为、功能细节和 API 的小改动仍然可能会发生。您的反馈和测试将有助于调整并敲定这些新功能，因此请在近期进行测试。用户测试的质量有助于我们确定何时可以进行最终发布。

PostgreSQL wiki 中公开提供了[开放问题](https://wiki.postgresql.org/wiki/PostgreSQL_17_Open_Items)列表。您可以使用 PostgreSQL 网站上的此表单[报告错误](https://www.postgresql.org/account/submitbug/)：

https://www.postgresql.org/account/submitbug/



------

## Beta 时间表

这是 PostgreSQL 17 的第一个 Beta 版本。PostgreSQL 项目将根据测试需要发布更多的 Beta 版本，随后是一或多个 RC 版本，最终版本大约会在 2024 年 9 月或 10 月发布。详细信息请参阅 [Beta 测试](https://www.postgresql.org/developer/beta/) 页面。


------

## 链接

- [下载](https://www.postgresql.org/download/)
- [Beta 测试信息](https://www.postgresql.org/developer/beta/)
- [PostgreSQL 17 Beta 发布说明](https://www.postgresql.org/docs/17/release-17.html)
- [PostgreSQL 17 开放问题](https://wiki.postgresql.org/wiki/PostgreSQL_17_Open_Items)
- [功能矩阵](https://www.postgresql.org/about/featurematrix/)
- [提交错误](https://www.postgresql.org/account/submitbug/)
- [在 X/Twitter 上关注 @postgresql](https://twitter.com/postgresql)
- [捐赠](https://www.postgresql.org/about/donate/)
