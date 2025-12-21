---
title: "Pigsty v4.0：可观测性与安全性史诗改进"
linkTitle: "Pigsty v4.0 发布注记"
date: 2025-12-19
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v4.0.0)）
summary: >
  Victoria全家桶，Infra/日志系统重制，安全性全面改进，UI 合并，使用体验优化。
series: [Pigsty]
tags: [Pigsty]
---


--------

## v4.0.0-b1


### 亮点

- Infra 模块彻底翻新，Victoria 可观测性全家桶带来 10x 性能提升！
- 日志方案升级为 VictoriaLogs + Vector，性能、易用性史诗级加强！
- Pigsty UI 集成，带来浑然一体的 UI 使用体验。
- 全局安全性提升，防火墙 SELinux 权限加固
- Docker 容器版本，可供快速评估试用

### 软件版本

**基础设施软件包**

其中 MinIO 开始使用 pgsty 自身维护打包的 RPM/DEB

- victoria-metrics  : 1.132.0
- victoria-logs     : 1.41.0
- blackbox_exporter : 0.28.0
- duckdb            : 1.4.3
- rclone            : 1.72.1
- pev2              : 1.19.0
- pg_exporrter      : 1.1.0
- pig               : 0.8.0
- rclone            : 1.72.1
- genai-toolbox     : 0.23.0
- minio             : 20251203120000

**PG 扩展软件包**

- [pg_textsearch](https://github.com/timescale/pg_textsearch): 0.1.0 新扩展
- [pg_clickhouse](https://github.com/clickhouse/pg_clickhouse/): 0.1.0 新扩展
- [pg_ai_query](https://github.com/benodiwal/pg_ai_query): 0.1.1 新扩展
- timescaledb    : 2.23.1  -> 2.24.0
- pg_search      : 0.20.0  -> 0.20.4
- pg_duckdb      : 1.1.0-1 -> 1.1.0-2 ，官方正式发布版本
- pg_biscuit     : 1.0     -> 2.0.1   ，仓库重命名
- pg_convert     : 0.0.4   -> 0.0.5   ，移除 PG 13 支持
- pgdd           : 0.6.0   -> 0.6.1   ，移除 PG 13 支持
- pglinter       : 1.0.0   -> 1.0.1
- pg_session_jwt : 0.3.3   -> 0.4.0
- pg_anon        : 2.4.1   -> 2.5.1
- pg_enigma      : 0.4.0   -> 0.5.0
- wrappers       : 0.5.6   -> 0.5.7
- pg_vectorize   : 0.25.0  -> 0.26.0

修复 PG 18 Deb 包：pg_vectorize ,pg_tiktoken ,pg_tzf ,pglite_fusion ,pgsmcrypto ,pgx_ulid ,plprql


### 可观测性

- 使用全新的 VictoriaMetrics 替代 Prometheus，用几分之一的资源实现几倍的性能。
- 使用全新的日志收集方案：VictoriaLogs + Vector，取代 Promtail + Loki。
- 统一调整了所有组件的日志格式，PG 日志使用 UTC 时间戳（log_timezone）
- 调整了 PostgreSQL 日志的轮换方式，使用按周循环截断日志轮转模式
- 在 PG 日志中记录超过 1MB 的临时文件分配，在特定模版中启用 PG 17/18 日志新参数
- 新增了 Nginx Access & Error / Syslog / PG CSV / Pgbackrest 的 vector 日志解析配置
- 注册数据源现在会在所有 Infra 节点上进行，Victoria 数据源将自动注册入 Grafana
- 新增 `grafana_pgurl` 参数，允许指定 Grafana 使用 PG 作为后端存储元数据库
- 新增 `grafana_view_pgpass` 参数，指定 Grafana Meta 数据源使用的密码

### 参数优化

- `pg_io_method` 参数，auto, sync, worker, io_uring, 四种方式可选，默认 worker
- `idle_replication_slot_timeout`, 默认 7d， crit 模板 3d
- `log_lock_failures`，oltp，crit 模版开启
- `track_cost_delay_timing`，olap，crit 模版开启
- `log_connections`，oltp/olap 开启认证日志，crit 开启全部日志。
- `maintenance_io_concurrency` 设置为 100，如果使用 SSD
- `effective_io_concurrency` 从 1000 减小为 200
- 对于 PG17+，如果 `pg_checksums` 开关关闭，在 patroni 初始化集群时显式禁用校验和
- 修复了 `duckdb.allow_community_extensions` 总是生效的问题
- 允许通过 `node_firewall_intranet` 指定 HBA 信任的 “内网网段”
- 现在 pg_hba 与 pgbouncer_hba 支持 IPv6 的 localhost 访问


### 架构改进

- 在 Infra 节点上，设置固定的 `/infra` 软连接指向 Infra 数据目录 `/data/infra`。
- 现在 infra 的数据默认放置于 /data/infra 目录下，这使得在容器中使用更为便利。
- 本地软件仓库现在放置于 /data/nginx/pigsty, /www 现在作为软链接指向 /data/nginx 确保兼容。
- DNS 解析记录现在放置于 `/infra/hosts` 目录下，解决了 Ansible SELinux 竞态问题
- pg_remove/pg_pitr 移除 etcd 元数据的任务，现在不再依赖 admin_ip 管理节点，而在 etcd 集群上执行


### 安全改进

- `configure` 现在会自动生成随机强密码，避免使用默认密码带来的安全隐患。
- 移除 `node_disable_firewall`，新增 `node_firewall_mode`，支持 off, none, zone 三种模式。
- 移除 `node_disable_selinux`，新增 `node_selinux_mode`，支持 disabled, permissive, enforcing 三种模式。
- 新增 nginx basic auth 支持，可以为 Nginx Server 设置可选的 HTTP Basic Auth。
- 修复 ownca 证书有效期问题，确保了 Chrome 可以识别自签名证书。
- 更改了 MinIO 模块的默认密码，避免与众所周知的默认密码冲突- 启用了针对 etcd 的 RBAC，每个集群现在只能管理自己的 PostgreSQL 数据库集群。
- etcd root 密码现在放置于 `/etc/etcd/etcd.pass` 文件中，仅对管理员可读
- 为 HAProxy，Nginx，DNSMasq，Redis 等组件配置了正确的 SELinux 上下文
- 收回了所有非 root 用户对可执行脚本的拥有权限
- 将 admin_ip 添加到 Patroni API 允许访问的 IP 列表白名单中
- 总是创建 admin 系统用户组，patronictl 配置收紧为仅限 admin 组用户访问
- 新增 `node_admin_sudo` 参数，允许指定/调整数据库管理员的 sudo 权限模式（all/nopass）
