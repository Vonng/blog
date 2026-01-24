---
title: "Pigsty v4.0.0：可观测性革命与安全性大改进"
linkTitle: "Pigsty v4.0.0 发布注记"
date: 2026-01-25
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/pgsty/pigsty/releases/tag/v4.0.0)）
summary: >
  VictoriaMetrics/Logs 替代 Prometheus/Loki，新增 JUICE/VIBE 模块，安全性全面改进，多云支持，许可证变更为 Apache-2.0。
series: [Pigsty]
tags: [Pigsty]
---

## 快速上手

```bash
curl https://pigsty.cc/get | bash -s v4.0.0
```

**299 个提交**，595 文件变更，+117,624 / -327,455 行

**发布日期: 2025-12-25** | [GitHub](https://github.com/pgsty/pigsty/releases/tag/v4.0.0) | [英文文档](https://pigsty.io) | [中文文档](https://pigsty.cc)

---

## 亮点特性

- **可观测性革命**: Prometheus → VictoriaMetrics（10x 性能提升），Loki + Promtail → VictoriaLogs + Vector
- **安全加固**: 自动生成强密码、etcd RBAC、防火墙/SELinux 模式、权限收紧、Nginx Basic Auth
- **新增模块**：Juice，提供将 PG 挂载为文件系统并进行 PITR 的能力
- **新增模块**：VIBE，提供 Claude Code，Jupyter，VS Code Server 的配置与可观测性
- **数据库管理**: `pg_databases` state（create/absent/recreate）、`strategy` 瞬间克隆数据库
- **PITR 与分叉**: `/pg/bin/pg-fork` CoW 瞬间克隆、`pg-pitr` 增强支持 PITR 前备份
- **高可用增强**: `pg_rto` 提供四档 RTO 预置参数（fast/norm/safe/wide），`pg_crontab` 定时任务
- **多云 Terraform**: AWS、Azure、GCP、Hetzner、DigitalOcean、Linode、Vultr、腾讯云模板
- **许可证变更**: AGPL-3.0 → Apache-2.0


[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v4.0.0)


---

## 基础设施软件包更新

MinIO 开始使用 [**pgsty/minio**](https://github.com/pgsty/minio) fork RPM/DEB.

| 软件包               | 版本       | 软件包                 | 版本      |
|-------------------|----------|---------------------|---------|
| victoria-metrics  | 1.133.0  | victoria-logs       | 1.43.1  |
| vector            | 0.52.0   |                     |         |
| grafana           | 12.3.1   | alertmanager        | 0.30.0  |
| etcd              | 3.6.7    | duckdb              | 1.4.3   |
| pg_exporter       | 1.1.2    | pgbackrest_exporter | 0.22.0  |
| blackbox_exporter | 0.28.0   | node_exporter       | 1.10.2  |
| minio             | 20251203 | pig                 | 0.9.1   |
| claude            | 2.1.9    | opencode            | 1.1.23  |
| uv                | 0.9.26   | asciinema           | 3.1.0   |
| prometheus        | 3.9.1    | pushgateway         | 1.11.2  |
| juicefs           | 1.4.0    | code-server         | 4.100.2 |

---

## 新增模块

v4.0.0 新增两个**可选模块**，不影响 Pigsty 核心功能，按需安装即可：

**JUICE 模块**：JuiceFS 分布式文件系统

- 使用 PostgreSQL 作为元数据引擎，支持利用 PITR 恢复文件系统
- 支持多种存储后端：PostgreSQL 大对象、MinIO、S3
- 支持多实例部署，每个实例暴露 Prometheus 指标端口
- 新增 `node-juice` 仪表盘监控 JuiceFS 状态
- 新增剧本 `juice.yml` 用于部署和管理 JuiceFS 实例
- 参数：`juice_cache`、`juice_instances`

**VIBE 模块**：AI 辅助编程沙箱环境（整合了 Code-Server、JupyterLab 与 Claude Code）

- **Code-Server**：浏览器中的 VS Code
  - 在节点上部署 Code-Server，通过 Nginx 反向代理提供 HTTPS 访问
  - 支持 Open VSX 和 Microsoft 两种扩展市场
  - 设置 `code_enabled: false` 可禁用
  - 参数：`code_enabled`、`code_port`、`code_data`、`code_password`、`code_gallery`

- **JupyterLab**：交互式计算环境
  - 在节点上部署 JupyterLab，通过 Nginx 反向代理提供 HTTPS 访问
  - 支持 Python 虚拟环境配置，便于安装数据科学库
  - 设置 `jupyter_enabled: false` 可禁用
  - 参数：`jupyter_enabled`、`jupyter_port`、`jupyter_data`、`jupyter_password`、`jupyter_venv`

- **Claude Code**：AI 编程助手 CLI 配置
  - 配置 Claude Code CLI，跳过 onboarding 流程
  - 内置 OpenTelemetry 可观测性配置，将指标和日志发送到 VictoriaMetrics/VictoriaLogs
  - 新增 `claude-code` 仪表盘监控 Claude Code 的使用情况
  - 设置 `claude_enabled: false` 可禁用
  - 参数：`claude_enabled`、`claude_env`

- 新增剧本 `vibe.yml` 用于部署完整的 VIBE 模块
- 配合 `conf/vibe.yml` 配置模板，可快速搭建完整的 AI 辅助编程沙箱环境
- 公共参数：`vibe_data`（默认 `/fs`）指定 VIBE 工作空间目录

---

## PG 扩展更新

主要扩展添加 PG 18 支持：age, citus, documentdb, pg_search, timescaledb, pg_bulkload, rum 等

**新增扩展**：
- [pg_textsearch](https://github.com/timescale/pg_textsearch) 0.4.0 - TimescaleDB 全文搜索
- [pg_clickhouse](https://github.com/clickhouse/pg_clickhouse/) 0.1.2 - ClickHouse FDW
- [pg_ai_query](https://github.com/benodiwal/pg_ai_query) 0.1.1 - AI 查询扩展
- [etcd_fdw](https://github.com/pgsty/etcd_fdw) 0.0.0 - etcd 外部数据包装器
- [pg_ttl_index](https://github.com/pg-ttl-index) 0.1.0 - TTL 索引
- [pljs](https://github.com/plv8/pljs) 1.0.4 - JavaScript 存储过程语言
- [pg_retry](https://github.com/pg-retry/pg_retry) 1.0.0 - 重试扩展
- [pg_weighted_statistics](https://github.com/pgsty/pg_weighted_statistics) 1.0.0 - 加权统计
- [pg_enigma](https://github.com/pgsty/pg_enigma) 0.5.0 - 加密扩展
- [pglinter](https://github.com/pgsty/pglinter) 1.0.1 - SQL Linter
- [documentdb_extended_rum](https://github.com/microsoft/documentdb) 0.109 - DocumentDB RUM 扩展
- [mobilitydb_datagen](https://github.com/MobilityDB) 1.3.0 - MobilityDB 数据生成器

**重要更新**：

| 扩展             | 旧版本    | 新版本    | 备注                |
|----------------|--------|--------|-------------------|
| timescaledb    | 2.23.x | 2.24.0 | +PG18             |
| pg_search      | 0.19.x | 0.21.2 | ParadeDB, +PG18   |
| citus          | 13.2.0 | 14.0.0 | 分布式 PG, +PG18 预发布 |
| documentdb     | 0.106  | 0.109  | MongoDB 兼容, +PG18 |
| age            | 1.5.0  | 1.6.0  | 图数据库, +PG18       |
| pg_duckdb      | 1.1.0  | 1.1.1  | DuckDB 集成         |
| vchord         | 0.5.3  | 1.0.0  | VectorChord       |
| vchord_bm25    | 0.2.2  | 0.3.0  | BM25 全文搜索         |
| pg_biscuit     | 1.0    | 2.2.2  | Biscuit 认证        |
| pg_anon        | 2.4.1  | 2.5.1  | 数据脱敏              |
| wrappers       | 0.5.6  | 0.5.7  | Supabase FDW      |
| pg_vectorize   | 0.25.0 | 0.26.0 | 向量化               |
| pg_session_jwt | 0.3.3  | 0.4.0  | JWT 会话            |
| pg_partman     | 5.3.x  | 5.4.0  | 分区管理, PGDG        |
| pgmq           | 1.8.0  | 1.8.1  | 消息队列              |
| pg_bulkload    | 3.1.22 | 3.1.23 | 批量加载, +PG18       |
| pg_timeseries  | 0.1.7  | 0.2.0  | 时序扩展              |
| pg_convert     | 0.0.4  | 0.1.0  | 类型转换              |

pgBackRest 更新至 2.58，支持 HTTP。


---

## 可观测性

- 使用全新的 VictoriaMetrics 替代 Prometheus，用几分之一的资源实现数倍的性能
- 使用全新的日志收集方案：VictoriaLogs + Vector，取代 Promtail + Loki
- 统一调整了所有组件的日志格式，PG 日志使用 UTC 时间戳（log_timezone）
- 调整了 PostgreSQL 日志的轮换方式，使用按周循环截断日志轮转模式
- 在 PG 日志中记录超过 1MB 的临时文件分配，在特定模版中启用 PG 17/18 日志新参数
- 新增了 Nginx / Syslog / PG CSV / Pgbackrest / Grafana / Redis / etcd / MinIO 等日志的 Vector 解析配置
- 注册数据源现在会在所有 Infra 节点上进行，Victoria 数据源将自动注册入 Grafana
- 新增 `grafana_pgurl` 参数，允许指定 Grafana 使用 PG 作为后端存储元数据库
- 新增 `grafana_view_password` 参数，指定 Grafana Meta 数据源使用的密码
- `pgbackrest_exporter` 的默认选项现在设置 120 秒的内部缓存间隔（原本为 600s）
- `grafana_clean` 参数的默认值现在由 `true` 改为 `false`，即默认不清除
- 新增指标收集器 `pg_timeline`，收集更实时的时间线指标 `pg_timeline_id`
- `pg_exporter` 更新至 1.1.2，新增 `pg_timeline` 采集器，修复大量历史遗留问题
- 新增 `node-vector` 仪表盘，监控 Vector 日志收集器状态
- 新增 `node-juice` 仪表盘，监控 JuiceFS 分布式文件系统状态
- 新增 `claude-code` 仪表盘，监控 Claude Code AI 编程助手使用情况
- PGSQL Cluster/Instance 仪表盘新增版本横幅显示
- 所有仪表盘使用 compact JSON 格式，大幅减少文件体积

---

## 接口改进

**剧本重命名**
- `install.yml` 剧本现在重命名为 `deploy.yml` 以更符合语义
- 新增 `vibe.yml` 剧本，用于部署 VIBE AI 编程沙箱环境

**pg_databases 数据库制备功能改进**
- 添加删库能力：可以使用 `state` 字段指定 `create`, `absent`, `recreate` 三种状态
- 添加克隆能力：数据库定义中使用 `strategy` 参数指定克隆方法
- 支持较新版本引入的 locale 配置参数：`locale_provider`，`icu_locale`，`icu_rules`，`builtin_locale`
- 支持 `is_template` 参数，将数据库标记为模板数据库
- 添加了更多类型检查，避免了字符类参数的注入
- 允许在 extension 中指定 `state: absent` 以删除扩展

**pg_users 用户制备功能改进**
- 新增参数 `admin`，类似 `roles`，但是带有 `ADMIN OPTION` 权限可以转授
- 新增 `set` 和 `inherit` 选项定制用户角色属性

**pg_hba 访问控制改进**
- 支持 `order` 字段，允许指定 HBA 规则的排序优先级
- 支持 IPv6 的 localhost 访问
- 允许通过 `node_firewall_intranet` 指定 HBA 信任的 "内网网段"

**其他改进**
- 新增 Supabase 角色的默认权限配置
- `node_crontab` 在 `node-rm` 时会自动恢复原始 crontab
- 新增 `infra_extra_services` 参数用于首页额外服务入口导航

---

## 参数优化

**I/O 参数**
- `pg_io_method` 参数：auto, sync, worker, io_uring 四种方式可选，默认 worker
- `maintenance_io_concurrency` 设置为 100（如果使用 SSD）
- `effective_io_concurrency` 从 1000 减小为 200
- `file_copy_method` 参数为 PG18 默认设置为 `clone`，提供瞬间克隆数据库的能力

**复制槽与日志参数**
- `idle_replication_slot_timeout` 默认 7d，crit 模板 3d
- `log_lock_failures`：oltp, crit 模版开启
- `track_cost_delay_timing`：olap, crit 模版开启
- `log_connections`：oltp/olap 开启认证日志，crit 开启全部日志

**高可用参数**
- 新增 `pg_rto_plan` 参数，整合 Patroni 与 HAProxy 的 RTO 相关配置
  - `fast`: 最快故障转移（~15s），适合对可用性要求极高的场景
  - `norm`: 标准模式（~30s），平衡可用性与稳定性（默认）
  - `safe`: 安全模式（~60s），减少误判概率
  - `wide`: 宽松模式（~120s），适合跨地域部署
- `pg_crontab` 参数：为 postgres dbsu 配置定时任务
- 对于 PG17+，如果 `pg_checksums` 开关关闭，在 Patroni 初始化集群时显式禁用校验和
- Crit 模板启用 Patroni 严格同步模式

**备份恢复参数**
- PITR 默认 `archive_mode` 改为 `preserve`，确保恢复后保留归档能力
- `pg-pitr` 支持恢复前自动备份数据

**其他改进**
- 修复了 `duckdb.allow_community_extensions` 总是生效的问题
- 现在 pg_hba 与 pgbouncer_hba 支持 IPv6 的 localhost 访问

---

## 架构改进

**目录与门户**
- 在 Infra 节点上，设置固定的 `/infra` 软连接指向 Infra 数据目录 `/data/infra`
- 现在 Infra 的数据默认放置于 `/data/infra` 目录下，这使得在容器中使用更为便利
- 本地软件仓库现在放置于 `/data/nginx/pigsty`，`/www` 现在作为软链接指向 `/data/nginx` 确保兼容
- DNS 解析记录现在放置于 `/infra/hosts` 目录下，解决了 Ansible SELinux 竞态问题
- 默认首页域名从 `h.pigsty` 更名为 `i.pigsty`，新增中文首页支持

**运维脚本**
- 新增了 `/pg/bin/pg-fork` 脚本，用于快速创建 CoW 副本数据库实例
- 调整 `/pg/bin/pg-pitr` 脚本，现在可以用于实例级别的 PITR 恢复，支持恢复前自动备份
- 新增 `/pg/bin/pg-drop-role` 脚本，用于安全删除用户角色
- 新增 `bin/pgsql-ext` 脚本，用于安装 PostgreSQL 扩展
- 恢复 `pg-vacuum` 和 `pg-repack` 脚本

**新增剧本**
- `juice.yml`：部署 JuiceFS 分布式文件系统实例
- `vibe.yml`：部署 VIBE AI 编程沙箱环境（含 Code-Server、JupyterLab、Claude Code）

**模块改进**
- 显式安装 cron/cronie 包，确保定时任务功能在最小化安装的系统上可用
- UV Python 包管理器从 `infra` 模块迁移至 `node` 模块，新增 `node_uv_env` 参数指定虚拟环境路径
- `pg_remove`/`pg_pitr` 移除 etcd 元数据的任务，现在不再依赖 admin_ip 管理节点，而在 etcd 集群上执行
- 36 节点仿真模板 simu 简化为 20 节点的版本
- 适配上游变化，移除 PGDG sysupdate 仓库，移除 EL 系统上所有 llvmjit 的相关包
- 为 EPEL 10 / PGDG 9/10 仓库使用操作系统完整版本号（`major.minor`）
- 允许在仓库定义中指定 `meta` 参数，覆盖 yum 仓库的定义元数据
- 确保 Vagrant libvirt 模板默认带有 128GB 磁盘，以 xfs 挂载于 `/data`
- 确保 pgbouncer 不再将 `0.0.0.0` 监听地址修改为 `*`
- 新增 10 节点、Citus 等 Vagrant 配置模板
- 恢复 EL7 系统兼容性支持

**多云支持**
- 多云 Terraform 模板：AWS、Azure、GCP、Hetzner、DigitalOcean、Linode、Vultr、腾讯云

---

## 安全改进

**密码管理**

- `configure` 现在支持 `-g` 参数自动生成随机强密码，避免使用默认密码带来的安全隐患
- 更改了 MinIO 模块的默认密码，避免与众所周知的默认密码冲突

**防火墙与 SELinux**
- 移除 `node_disable_firewall`，新增 `node_firewall_mode`，支持 off, none, zone 三种模式
- 移除 `node_disable_selinux`，新增 `node_selinux_mode`，支持 disabled, permissive, enforcing 三种模式
- 为 HAProxy、Nginx、DNSMasq、Redis 等组件配置了正确的 SELinux 上下文

**访问控制**
- 启用了针对 etcd 的 RBAC，每个集群现在只能管理自己的 PostgreSQL 数据库集群
- etcd root 密码现在放置于 `/etc/etcd/etcd.pass` 文件中，仅对管理员可读
- 将 `admin_ip` 添加到 Patroni API 允许访问的 IP 列表白名单中
- 总是创建 admin 系统用户组，patronictl 配置收紧为仅限 admin 组用户访问
- 新增 `node_admin_sudo` 参数，允许指定/调整数据库管理员的 sudo 权限模式（all/nopass）
- 收回了所有非 root 用户对可执行脚本的拥有权限

**证书与认证**
- 新增 Nginx Basic Auth 支持，可以为 Nginx Server 设置可选的 HTTP Basic Auth
- 修复 ownca 证书有效期问题，确保了 Chrome 可以识别自签名证书
- 新增 `vip_auth_pass` 参数用于 VRRP 认证

**其他**
- 修复了若干 `ansible copy content` 字段为空时报错的问题
- 修复了 `pg_pitr` 中遗留的一些问题，确保 Patroni 集群恢复时没有竞态条件
- 使用 `mode 0700` 保护 `files/pki/ca` 目录


---

## 问题修复

| 问题                                       | 说明                            |
|------------------------------------------|-------------------------------|
| ownca 证书有效期 Chrome 兼容性问题                 | 正确设置 ownca_not_after 参数       |
| Vector 0.52 syslog_raw 解析问题              | 适配新版本 Vector 的解析格式变化          |
| pg_pitr 多副本 clonefrom 时序问题               | 修复 Patroni 集群恢复的竞态条件          |
| Ansible SELinux dnsmasq 竞态条件             | 将 DNS 记录移至 /infra/hosts 目录    |
| EL9 aarch64 patroni & llvmjit 问题         | 热修复 ARM64 架构兼容性问题             |
| Debian groupadd 路径问题                     | 修复 Debian 系统用户组添加路径           |
| 空 sudoers 文件生成问题                         | 防止生成空的 sudoers 配置文件           |
| pgbouncer pid 路径                         | 使用 `/run/postgresql` 替代旧路径    |
| `duckdb.allow_community_extensions` 始终生效 | 修复 DuckDB 扩展配置问题              |
| pg_partman EL8 上游问题                      | 因上游问题隐藏 EL8 上的 pg_partman 扩展  |
| HAProxy 服务模板变量路径                         | 修复变量引用路径错误                    |
| Redis remove 任务变量名                       | 修复 redis_seq 到 redis_node 变量名 |
| MinIO reload handler 无效                  | 移除无效的 reload 处理器              |
| vmetrics_port 默认值                        | 修正为正确的 8428 端口                |
| pg-failover-callback 脚本                  | 处理所有 Patroni 回调事件             |
| pg-vacuum 事务块问题                          | 修复事务块处理逻辑                     |
| pg_sub_16 并行逻辑复制 worker                  | 添加 PG16+ 并行逻辑复制支持             |
| FerretDB 证书 SAN 和重启策略                    | 修复证书配置和服务重启策略                 |
| Polar Exporter 指标类型                      | 修正监控指标类型定义                    |
| proxy_env 包安装缺失                          | 修复代理环境变量未传递问题                 |
| patroni_method=remove 服务问题               | 修复移除模式下 postgres 服务配置         |
| Docker 默认数据目录                            | 更新为正确的默认数据目录路径                |
| EL10 缓存兼容性                               | 修复 EL10 系统上的缓存问题              |
| etcd/MinIO 移除时清理不完整                      | 修复 systemd 服务和 DNS 条目清理       |


---

## 参数变化

**新增参数**

| 参数                       | 类型     | 默认值           | 说明                               |
|--------------------------|--------|---------------|----------------------------------|
| `node_firewall_mode`     | enum   | none          | 防火墙模式：off/none/zone              |
| `node_selinux_mode`      | enum   | permissive    | SELinux 模式                       |
| `node_firewall_intranet` | string | -             | HBA 信任的内网网段                      |
| `node_admin_sudo`        | enum   | nopass        | 管理员 sudo 权限级别                    |
| `pg_io_method`           | enum   | worker        | I/O 方法：auto/sync/worker/io_uring |
| `pg_rto_plan`            | dict   | -             | RTO 预设：fast/norm/safe/wide       |
| `pg_crontab`             | list   | []            | postgres dbsu 定时任务               |
| `vip_auth_pass`          | string | -             | VRRP 认证密码                        |
| `grafana_pgurl`          | string | -             | Grafana PG 后端连接字符串               |
| `grafana_view_password`  | string | DBUser.Viewer | Grafana Meta 数据源密码               |
| `infra_extra_services`   | list   | []            | 首页额外服务入口                         |
| `juice_cache`            | path   | /data/juice   | JuiceFS 共享缓存目录                   |
| `juice_instances`        | dict   | {}            | JuiceFS 实例定义                     |
| `vibe_data`              | path   | /fs           | VIBE 工作空间目录                      |
| `code_enabled`           | bool   | true          | 是否启用 Code-Server                 |
| `code_port`              | port   | 8443          | Code-Server 监听端口                 |
| `code_data`              | path   | /data/code    | Code-Server 数据目录                 |
| `code_password`          | string | Code.Server   | Code-Server 登录密码                 |
| `code_gallery`           | enum   | openvsx       | 扩展市场：openvsx/microsoft           |
| `jupyter_enabled`        | bool   | true          | 是否启用 JupyterLab                  |
| `jupyter_port`           | port   | 8888          | JupyterLab 监听端口                  |
| `jupyter_data`           | path   | /data/jupyter | JupyterLab 数据目录                  |
| `jupyter_password`       | string | Jupyter.Lab   | JupyterLab 登录 Token              |
| `jupyter_venv`           | path   | /data/venv    | Python 虚拟环境路径                    |
| `claude_enabled`         | bool   | true          | 是否启用 Claude Code 配置              |
| `claude_env`             | dict   | {}            | Claude Code 额外环境变量               |
| `node_uv_env`            | path   | /data/venv    | 节点 UV 虚拟环境路径，空则跳过                |
| `node_pip_packages`      | string | ''            | UV 虚拟环境中安装的 pip 包                |

**移除参数**

| 参数                      | 说明                        |
|-------------------------|---------------------------|
| `node_disable_firewall` | 由 `node_firewall_mode` 替代 |
| `node_disable_selinux`  | 由 `node_selinux_mode` 替代  |
| `infra_pip_packages`    | 由 `node_pip_packages` 替代  |
| `pgbackrest_clean`      | 未使用参数，已移除                 |
| `pg_pwd_enc`            | 已移除，统一使用 scram-sha-256    |
| `code_home`             | 由 `vibe_data` 替代          |
| `jupyter_home`          | 由 `vibe_data` 替代          |

**默认值变更**

| 参数                         | 变化                       | 说明         |
|----------------------------|--------------------------|------------|
| `grafana_clean`            | true → false             | 默认不清除      |
| `effective_io_concurrency` | 1000 → 200               | 更合理的默认值    |
| `node_firewall_mode`       | zone → none              | 默认不启用防火墙规则 |
| `install.yml`              | 重命名为 `deploy.yml`        | 更符合语义      |


---

## 兼容性

| 操作系统               | x86_64 | aarch64 |
|--------------------|:------:|:-------:|
| EL 8/9/10          |   ✅    |    ✅    |
| Debian 11/12/13    |   ✅    |    ✅    |
| Ubuntu 22.04/24.04 |   ✅    |    ✅    |

**PostgreSQL**: 13, 14, 15, 16, 17, 18

---

## 校验和

```bash
# v4.0.0 离线安装包校验和 (待补充)
```
