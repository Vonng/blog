---
title: "Pigsty v1.1：主页，Jupyter，Pev2，Pgbadger"
linkTitle: "Pigsty v1.1 发布注记"
date: 2021-10-12
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v1.1.0)）
summary: >
  Pigsty v1.1.0 更新了主页设计, JupyterLab, PGWEB, Pev2 & pgbadger 支持
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v1.1.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v110) | [微信公众号](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247484774&idx=1&sn=8b9e8f5bec8fb8492ebce3ebc6b60d88&chksm=fe4b30bdc93cb9ab1dfcaed066a1a90919027f6c72d63003b3b839eb9ba2871ec663db7469f1&scene=21#wechat_redirect)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v1.1.0)

Pigsty v1.1 正式发布，新增全新首页设计、Jupyter Lab、PGWeb、PEV2、PgBadger 等实用工具支持。

![featured](featured.jpg)


----------------

## 全新首页

Grafana 监控系统中的 Home Dashboard 一直扮演着 Pigsty "主页"的角色，现在 Pigsty 终于有了一个独立的、设计精良的首页。

![homepage](homepage.jpg)

这个首页是一个本地版的文档站，由默认的 Nginx 提供服务。


### 服务导航

首页提供前往 Pigsty 各个服务组件的导航，包括 Consul、Grafana、Prometheus、AlertManager，以及 v1.1 新引入的 **PGWeb** 与 **Jupyter Lab**。可直接点击首页正中的组件名称/URL，或通过导航栏右上角的 `Service` 下拉菜单进入。


### 监控导航

首页可呈现 Pigsty 部署中的集群与实例（可选），并提供到具体集群、实例监控首页及管控界面的直接跳转。

![monitor-nav](monitor-nav.jpg)


### 应用导航

右上角的 App 下拉选单是 Pigsty 扩展功能的入口。在 v1.1 中，Pigsty 自带了几个实用而有趣的应用，均可通过配置选项添加。

![app-nav](app-nav.jpg)


### 本地文档

在 Pigsty v1.1 中，可直接从首页访问本地离线文档，包括中英双语。

![local-docs](local-docs.jpg)


----------------

## Jupyter Lab

使用 Python 进行数据分析的用户对 Jupyter 一定不陌生。Pigsty v1.0 打包了 Jupyter Lab 软件包，v1.1 则更进一步将其纳入原生支持。在演示与个人配置模板中，Jupyter Lab 默认启用；在生产环境部署中则默认不启用。

![jupyter-1](jupyter-1.jpg)

通过 Jupyter Notebook，可以高效、敏捷地提取数据，进行处理、分析、转换及可视化，组合使用 Python 与 SQL 的强大能力。

![jupyter-2](jupyter-2.jpg)

强大与便利往往也蕴含风险。Jupyter 执行任意代码的能力对于生产环境过于冒险，因此默认不在生产环境配置模板中启用。


----------------

## PGWeb

作为开箱即用的数据库发行版，提供开箱即用的图形化客户端工具也很重要。PGWeb 是一个使用 Go 编写的小巧的、基于浏览器的 PostgreSQL 图形客户端。

![pgweb-1](pgweb-1.jpg)

与 Jupyter 类似，PGWeb 在演示与个人配置模板中默认启用，在生产环境部署中则默认不启用。但 PGWeb 要求用户拥有访问数据库的连接串，因此相对安全，可用于生产环境中个人用户查询少量数据的场景。

![pgweb-2](pgweb-2.jpg)

用户可以浏览数据库中的模式、对象，快速浏览表中的数据，执行查询等。


----------------

## PEV2

PEV2 是一个实用的执行计划分析器，可将 PostgreSQL 查询 EXPLAIN 的结果转换为直观的执行计划树。

![pev2](pev2.jpg)

这个工具对于优化慢查询、分析 auto_explain 结果非常好用。


----------------

## PgBadger

PgBadger 是一个优秀的 PostgreSQL 日志分析组件，可从 CSV 日志中快速生成精美全面的分析报告。

使用 `bin/pglog-summary [ip] [date]` 即可拉取特定节点特定日期的日志，并创建日志分析报告。

![pgbadger](pgbadger.jpg)

为该命令添加 Crontab，即可每天或准实时地自动生成数据库运行报表。


----------------

## 软件更新

PostgreSQL 14 已正式发布，Pigsty v1.1 第一时间进行了跟进与支持。`pigsty-pg14` 模板已可在生产环境中创建默认版本为 14 的 PostgreSQL 数据库。但因 TimescaleDB 尚未正式支持 PG14（预计时间 10-30），因此 PG14 暂不作为 Pigsty 的默认数据库版本。

![pg14](pg14.jpg)

Pigsty 将于 **v1.2** 进行默认 PG 版本升级，将默认数据库版本升级为 PG14。

软件升级列表：

| 组件 | 版本 |
|------|------|
| PostgreSQL | v13.4 |
| pgbouncer | v1.16 |
| Grafana | v8.1.4 |
| Prometheus | v2.2.29 |
| node_exporter | v1.2.2 |
| HAProxy | v2.1.1 |
| Consul | v1.10.2 |
| vip-manager | v1.0.1 |


----------------

## 数据库迁移剧本

Pigsty 内置了一个数据库在线迁移辅助脚本：`pgsql-migration.yml`，提供开箱即用的基于逻辑复制的不停机数据库迁移方案。

填入源集群与目标集群相关信息，该剧本即会自动创建迁移所需的脚本，在数据库迁移时只需依次执行即可。

![migration-1](migration-1.jpg)

![migration-2](migration-2.jpg)


----------------

## 示例应用：隐私日志可视化

Pigsty 自带的默认演示应用新增一个：苹果应用隐私日志可视化（AppLog）。可在 iOS15 系统中导出应用程序访问隐私的记录，并在此应用中进行可视化。

![applog-1](applog-1.jpg)

![applog-2](applog-2.jpg)


----------------

## 实用小功能

**Dummy File 占位符**

v1.1 加入了一个数据库实例上的新特性：Dummy File。原理很简单，创建一个一定尺寸（例如 1～4GB）的 `/pg/dummy`，当出现磁盘写满故障时（通常很多操作都无法正常完成），只需将其删除，就可以释放出一定的应急空间。

**Promscale 支持**

v1.1 添加了 Promscale 安装包，这是一个有趣的组件，可将 Prometheus 的时序数据存储替换为 TimescaleDB（PostgreSQL）。


----------------

## v1.1.0 更新日志

**功能增强**

- 增加 `pg_dummy_filesize` 以创建文件系统空间占位符
- 主页大改版
- 增加 Jupyter Lab 整合
- 增加 PGWeb 控制台整合
- 增加 PgBadger 支持
- 增加 PEV2 支持，执行计划可视化工具
- 增加 pglog 工具

**软件升级**

- PostgreSQL 升级至 v13.4（支持官方 PG14）
- pgbouncer 升级至 v1.16（指标定义更新）
- Grafana 升级至 v8.1.4
- Prometheus 升级至 v2.2.29
- node_exporter 升级至 v1.2.2
- HAProxy 升级至 v2.1.1
- Consul 升级至 v1.10.2
- vip-manager 升级至 v1.0.1

**API 变更**

- `nginx_upstream` 现持有不同结构（不兼容）
- 新配置条目：`app_list`，渲染至主页的导航条目
- 新配置条目：`docs_enabled`，在默认服务器上设置本地文档
- 新配置条目：`pev2_enabled`，设置本地 PEV2 工具
- 新配置条目：`pgbadger_enabled`，创建日志概要/报告目录
- 新配置条目：`jupyter_enabled`，在元节点上启用 Jupyter Lab 服务器
- 新配置条目：`jupyter_username`，指定运行 Jupyter Lab 的用户
- 新配置条目：`jupyter_password`，指定 Jupyter Lab 的默认密码
- 新配置条目：`pgweb_enabled`，在元节点上启用 PGWeb 服务器
- 新配置条目：`pgweb_username`，指定运行 PGWeb 的用户
- 将内部标记 `repo_exist` 重命名为 `repo_exists`
- `repo_address` 默认值改为 `pigsty` 而非 `yum.pigsty`
- HAProxy 访问点改为 `http://pigsty` 而非 `http://h.pigsty`


----------------

## v1.1.1 更新日志

- 用 `timescale` 版本替换 TimescaleDB 的 `apache` 版本
- 升级 Prometheus 到 2.30
- 修复 pg_exporter 配置目录属主问题（改为 `{{ pg_dbsu }}`）

**升级说明**

此版本主要变动是 TimescaleDB，使用 TimescaleDB License（TSL）的官方版本替代了 PGDG 仓库中 Apache License v2 的版本。

```bash
# 停止带有 timescaledb 的 postgres 实例
yum remove -y timescaledb_13

# 添加 TimescaleDB 官方仓库
[timescale_timescaledb]
name=timescale_timescaledb
baseurl=https://packagecloud.io/timescale/timescaledb/el/7/$basearch
repo_gpgcheck=0
gpgcheck=0
enabled=1

yum install timescaledb-2-postgresql13
```
