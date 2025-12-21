---
title: "Pigsty v1.3：PGCAT大修，PGSQL增强，Redis支持"
linkTitle: "Pigsty v1.3 发布注记"
date: 2021-11-30
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v1.3.0)）
summary: >
  Pigsty v1.3.0 更新了 PGCAT 重整 & PGSQL 增强 & Redis Beta支持
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v1.3.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v130) | [微信公众号](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247484821&idx=1&sn=56e34b33f37b2555336591ad532ac7e7&chksm=fe4b304ec93cb9589c2bca821e5aaa1034c7dd5b9c580dec4b09ebe3b1ed20bb48df9dfd29ce&scene=21#wechat_redirect)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v1.3.0)

Pigsty v1.3 正式发布，新增 Redis 支持、PGCAT 应用重构、PGSQL 监控增强。


----------------

## Redis 支持

虽然 PostgreSQL 是**世界上最先进的开源关系型数据库**，但一个好汉三个帮。Pigsty v1.3 为 PostgreSQL 引入了一位得力的缓存伙伴：**世界上最快的数据库** —— Redis。

![redis-partner](redis-partner.jpg)

Redis 性能强悍，单核轻松达到二三十万 QPS。

![redis-fast](redis-fast.jpg)

Pigsty Demo 中已经纳入 Redis 集群样例：

![redis-demo](redis-demo.jpg)


### 三种部署模式

Redis 有三种经典部署模式：普通主从结构（Standalone）、原生集群（Cluster）、高可用哨兵（Sentinel）。Pigsty v1.3 全部支持。

![redis-overview](redis-overview.jpg)

Redis Overview 首页展示了三个样例集群，分别对应三种部署模式。


### 声明式配置

定义 Redis 集群的方式与 PostgreSQL 高度一致。声明完成后，使用 `redis.yml -l <cluster>` 即可创建对应集群：

![redis-config](redis-config.jpg)

只需少量必选身份参数即可声明一个 Redis 集群。当然，也可以使用更多参数进行精细配置：

![redis-params-1](redis-params-1.jpg)

![redis-params-2](redis-params-2.jpg)


### 自动监控

使用 Pigsty 创建的 Redis 集群与实例会自动纳入监控系统。

![redis-cluster](redis-cluster.jpg)

单个 Redis 集群的监控首页，点击具体实例可跳转至实例级监控：

![redis-instance](redis-instance.jpg)


----------------

## PGCAT 重构

v1.3 重构了 PGCAT 应用，这是一个直接从 Grafana 访问并可视化 PostgreSQL 系统目录的应用。

![pgcat-instance](pgcat-instance.jpg)

单个 PostgreSQL 实例的 Catalog 信息：数据库、活动会话、查询语句。

![pgcat-instance-2](pgcat-instance-2.jpg)

单个 PostgreSQL 实例的 Catalog 信息：配置、复制、内存使用、持久化、角色。

![pgcat-database](pgcat-database.jpg)

单个 PostgreSQL 数据库的 Catalog 信息，包括数据库内的模式、表、索引、序列等对象。

![pgcat-table](pgcat-table.jpg)

PGCAT TABLE Dashboard 改版：添加每一列的详细统计信息展示。


### 无侵入式设计

PGCAT 只需一个可访问的目标数据库 URL 即可使用，无需安装任何 Agent。即使是仅监控模式部署现有实例，也可以完整使用 PGCAT 功能。

![pgsql-monitor-only](pgsql-monitor-only.jpg)

在 Pigsty v1.3 的仅监控部署模式中，外部 PostgreSQL 实例也会在 Grafana 中注册并默认启用 PGCAT 功能。


----------------

## PGSQL 增强

核心 PGSQL 监控应用也有显著改进。

![pgsql-cluster](pgsql-cluster.jpg)

在 Pigsty v1.3 中，PGSQL Cluster 添加了 10 个核心指标的快速导览面板。

PGSQL Instance、PGSQL Cluster 都新增了若干快速导览面板，用于快速定位问题。PGSQL Service 完整重置，更为简洁直观，便于快速理清集群拓扑。其他 Dashboard 也有相应优化与改进。

此外，v1.3 还包含半自动数据库迁移剧本的改进、Profiling 工具支持等功能增强。


----------------

## v1.3.0 更新日志

**Redis 支持**

| 功能 | 说明 |
|------|------|
| Redis 部署 | 支持集群、哨兵、主从三种模式 |
| Redis 监控 | 提供总览、集群、实例三级仪表盘 |

**PGCAT 大修**

| 仪表盘 | 说明 |
|--------|------|
| PGCAT Instance | 新增实例级 Catalog 仪表盘 |
| PGCAT Database | 新增数据库级 Catalog 仪表盘 |
| PGCAT Table | 重做表级统计仪表盘 |

**PGSQL 增强**

| 仪表盘 | 改进内容 |
|--------|----------|
| PGSQL Cluster | 新增 10 个关键指标面板 |
| PGSQL Instance | 新增 10 个关键指标面板 |
| PGSQL Service | 简化重设计，更清晰直观 |
| 交叉引用 | 在 PGCAT 与 PGSQL 仪表盘间添加导航链接 |

**监控部署**

- Grafana 数据源在仅监控部署期间自动注册

**软件升级**

- 将 PostgreSQL 13 添加到默认包列表
- 默认升级到 PostgreSQL 14.1
- 添加 Greenplum RPM 和依赖项
- 添加 Redis RPM 及源码包
- 将 perf 添加为默认包


----------------

## v1.3.1 更新日志

**监控**

- PGSQL & PGCAT 仪表盘改进
- 优化 PGCAT Instance & PGCAT Database 布局
- 在 PGSQL Instance 仪表盘中添加关键指标面板，与 PGSQL Cluster 保持一致
- 在 PGCAT Database 中添加表/索引膨胀面板，移除 PGCAT Bloat 仪表盘
- 在 PGCAT Database 仪表盘中添加索引信息
- 修复 Grafana 8.3 中的损坏面板
- 在 Nginx 主页中添加 Redis 索引

**部署**

- 新增 `infra-demo.yml` 剧本用于一次性引导
- 使用 `infra-jupyter.yml` 剧本部署可选的 Jupyter Lab 服务器
- 使用 `infra-pgweb.yml` 剧本部署可选的 PgWeb 服务器
- 在 Meta 节点上新增 `pg` 别名，可从 admin 用户启动 PostgreSQL 集群
- 根据 `timescaledb-tune` 建议调整所有 Patroni 配置模板中的 `max_locks_per_transactions`
- 在配置模板中添加 `citus.node_conninfo: 'sslmode=prefer'` 以便在无 SSL 情况下使用 Citus
- 在 PGDG14 包列表中添加所有扩展（除 pgrouting 外）
- 将 node_exporter 升级到 v1.3.1
- 将 PostgREST v9.0.0 添加到包列表，支持从 PostgreSQL Schema 生成 API

**错误修复**

- Grafana 安全漏洞修复（升级到 v8.3.1，[详情](https://grafana.com/blog/2021/12/07/grafana-8.3.1-8.2.7-8.1.8-and-8.0.7-released-with-high-severity-security-fix/)）
- 修复 `pg_instance` & `pg_service` 在 `register` 角色中从剧本中间开始时的问题
- 修复在没有 `pg_cluster` 变量的主机上 Nginx 主页渲染问题
- 修复升级到 Grafana 8.3.1 时的样式问题
