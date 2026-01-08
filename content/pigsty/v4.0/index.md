---
title: "Pigsty v4.0 RC1：可观测性与安全性大改进"
linkTitle: "Pigsty v4-c1 发布注记"
date: 2026-01-07
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/pgsty/pigsty/releases/tag/v4.0.0-c1)）
summary: >
  Victoria全家桶，Infra/日志系统重制，安全性全面改进，UI 合并，使用体验优化。
series: [Pigsty]
tags: [Pigsty]
---

## 快速上手

```bash
curl https://pigsty.cc/get | bash -s v4.0.0
```

**244 个提交**，554 文件变更，+94,508 / -41,374 行

**发布日期: 2026-01-07** | [GitHub](https://github.com/pgsty/pigsty/releases/tag/v4.0.0-c1) | [英文文档](https://pigsty.io) | [中文文档](https://pigsty.cc)

---

## 核心亮点

- **可观测性革命**: Prometheus → VictoriaMetrics（10x 性能），Loki+Promtail → VictoriaLogs+Vector
- **安全加固**: 自动生成强密码、etcd RBAC、防火墙/SELinux 模式、权限收紧
- **数据库管理**: `pg_databases` 删除与克隆能力、`strategy` 瞬间克隆能力
- **PITR 与分叉**: `/pg/bin/pg-fork` CoW 瞬间克隆、`pg-pitr` PITR 能力增强
- **AI Agent支持**: 添加 claude code，opencode，uv 支持
- **多云支持**: AWS、Azure、GCP、Hetzner、DigitalOcean、Linode、Vultr、腾讯云 Terraform 模板
- **许可证**: AGPL-3.0 → Apache-2.0，更为宽松友好。

---

## 软件版本

### 基础设施

| 软件包           | 版本             | 软件包                 | 版本              |
|---------------|----------------|---------------------|-----------------|
| grafana       | 12.3.1         | victoria-metrics    | 1.132.0         |
| victoria-logs | 1.43.1         | vector              | 0.52.0          |
| alertmanager  | 0.30.0         | blackbox_exporter   | 0.28.0          |
| etcd          | 3.6.7          | duckdb              | 1.4.3           |
| pg_exporter   | 1.1.1          | pgbackrest_exporter | 0.22.0          |
| minio         | 20251203       | pig                 | 0.9.0           |
| uv            | 0.9.18 (**新**) | opencode            | 1.0.223 (**新**) |

### PostgreSQL 扩展

**新扩展**: [pg_textsearch](https://github.com/timescale/pg_textsearch) 0.1.0, [pg_clickhouse](https://github.com/clickhouse/pg_clickhouse/) 0.1.0, [pg_ai_query](https://github.com/benodiwal/pg_ai_query) 0.1.1

**更新**: IvorySQL 5.1, timescaledb 2.24.0, pg_search 0.20.4, pg_duckdb 1.1.1, pg_biscuit 2.0.1, pg_anon 2.5.1, pg_enigma 0.5.0, pg_session_jwt 0.4.0, pg_vectorize 0.26.0, vchord_bm25 0.3.0, wrappers 0.5.7

**PG18 Deb 修复**: pg_vectorize, pg_tiktoken, pg_tzf, pglite_fusion, pgsmcrypto, pgx_ulid, plprql, pg_summarize, supautils


[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v4.0.0)


---

## 破坏性变更

### 可观测性栈

| 旧组件        | 新组件             |
|------------|-----------------|
| Prometheus | VictoriaMetrics |
| Loki       | VictoriaLogs    |
| Promtail   | Vector          |

### 参数变更

| 移除                      | 替代                                                  |
|-------------------------|-----------------------------------------------------|
| `node_disable_firewall` | `node_firewall_mode` (off/none/zone)                |
| `node_disable_selinux`  | `node_selinux_mode` (disabled/permissive/enforcing) |
| `pg_pwd_enc`            | 已移除                                                 |
| `infra_pip`             | `infra_uv`                                          |

### 默认值变更

| 参数                         | 变化                       |
|----------------------------|--------------------------|
| `grafana_clean`            | true → false             |
| `effective_io_concurrency` | 1000 → 200               |
| `install.yml`              | 重命名为 `deploy.yml`（保留软链接） |

---

## 可观测性

- 使用全新的 VictoriaMetrics 替代 Prometheus，用几分之一的资源实现几倍的性能。
- 使用全新的日志收集方案：VictoriaLogs + Vector，取代 Promtail + Loki。
- 统一调整了所有组件的日志格式，PG 日志使用 UTC 时间戳（log_timezone）
- 调整了 PostgreSQL 日志的轮换方式，使用按周循环截断日志轮转模式
- 在 PG 日志中记录超过 1MB 的临时文件分配，在特定模版中启用 PG 17/18 日志新参数
- 新增了 Nginx Access & Error / Syslog / PG CSV / Pgbackrest 的 vector 日志解析配置
- 注册数据源现在会在所有 Infra 节点上进行，Victoria 数据源将自动注册入 Grafana
- 新增 `grafana_pgurl` 参数，允许指定 Grafana 使用 PG 作为后端存储元数据库
- 新增 `grafana_view_pgpass` 参数，指定 Grafana Meta 数据源使用的密码
- `pgbackrest_exporter` 的默认选项现在将设置一个 120秒的内部缓存间隔（原本为 600s）。
- `grafana_clean` 参数的默认值现在由 `true` 改为 `false`，即默认不清除。
- 新增指标收集器 `pg_timeline`，收集更实时的时间线指标 `pg_timeline_id`
- `pg_exporter` 更新至 1.1.1，修复大量历史遗留问题。

---

## 接口改进

- `install.yml` 剧本现在重命名为 `deploy.yml` 以更符合语义。
- `pg_databases` 数据库制备功能改进
    - 添加删库能力：可以使用 `state` 字段指定 `create`, `absent`, `recreate` 三种状态。
    - 添加克隆能力：数据库定义中使用 `strategy` 参数指定克隆方法
    - 支持较新版本引入的 locale 配置参数：`locale_provider`，`icu_locale`，`icu_rules`，`builtin_locale`
    - 支持 `is_template` 参数，将数据库标记为模板数据库
    - 添加了更多类型检查，避免了字符类参数的注入
    - 允许在 extension 中指定 `state: absent` 以删除扩展
- `pg_users` 用户制备功能改进，新增参数 `admin`，类似 `roles`，但是带有 `ADMIN OPTION` 权限可以转授。

---

## 参数优化

- `pg_io_method` 参数，auto, sync, worker, io_uring, 四种方式可选，默认 worker
- `idle_replication_slot_timeout`, 默认 7d， crit 模板 3d
- `log_lock_failures`，oltp，crit 模版开启
- `track_cost_delay_timing`，olap，crit 模版开启
- `log_connections`，oltp/olap 开启认证日志，crit 开启全部日志。
- `maintenance_io_concurrency` 设置为 100，如果使用 SSD
- `effective_io_concurrency` 从 1000 减小为 200
- `file_copy_method` 参数为 PG18 默认设置为 `clone`，提供瞬间克隆数据库的能力
- 对于 PG17+，如果 `pg_checksums` 开关关闭，在 patroni 初始化集群时显式禁用校验和
- 修复了 `duckdb.allow_community_extensions` 总是生效的问题
- 允许通过 `node_firewall_intranet` 指定 HBA 信任的 "内网网段"
- 现在 pg_hba 与 pgbouncer_hba 支持 IPv6 的 localhost 访问

---

## 架构改进

- 在 Infra 节点上，设置固定的 `/infra` 软连接指向 Infra 数据目录 `/data/infra`。
- 现在 infra 的数据默认放置于 /data/infra 目录下，这使得在容器中使用更为便利。
- 本地软件仓库现在放置于 /data/nginx/pigsty, /www 现在作为软链接指向 /data/nginx 确保兼容。
- DNS 解析记录现在放置于 `/infra/hosts` 目录下，解决了 Ansible SELinux 竞态问题
- pg_remove/pg_pitr 移除 etcd 元数据的任务，现在不再依赖 admin_ip 管理节点，而在 etcd 集群上执行
- 36 节点仿真模板 simu 简化为 20 节点的版本。
- 适配上游变化，移除 PGDG sysupdate 仓库，移除 EL 系统上所有 llvmjit 的相关包
- 为 EPEL 10 / PGDG 9/10 仓库使用操作系统完整版本号（`major.minor`）
- 允许在仓库定义中指定 `meta` 参数，覆盖 yum 仓库的定义元数据
- 新增了 `/pg/bin/pg-fork` 脚本，用于快速创建 CoW 副本数据库实例
- 调整 `/pg/bin/pg-pitr` 脚本，现在可以用于实例级别的 PITR 恢复
- 确保 vagrant libvirt 模板默认带有 128GB 磁盘，以 xfs 挂载于 `/data` 。
- 确保 pgboucner 不再将 `0.0.0.0` 监听地址修改为 `*`。
- 多云 Terraform 模板：AWS、Azure、GCP、Hetzner、DigitalOcean、Linode、Vultr、腾讯云

---

## 安全改进

- `configure` 现在会自动生成随机强密码，避免使用默认密码带来的安全隐患。
- 移除 `node_disable_firewall`，新增 `node_firewall_mode`，支持 off, none, zone 三种模式。
- 移除 `node_disable_selinux`，新增 `node_selinux_mode`，支持 disabled, permissive, enforcing 三种模式。
- 新增 nginx basic auth 支持，可以为 Nginx Server 设置可选的 HTTP Basic Auth。
- 修复 ownca 证书有效期问题，确保了 Chrome 可以识别自签名证书。
- 更改了 MinIO 模块的默认密码，避免与众所周知的默认密码冲突
- 启用了针对 etcd 的 RBAC，每个集群现在只能管理自己的 PostgreSQL 数据库集群。
- etcd root 密码现在放置于 `/etc/etcd/etcd.pass` 文件中，仅对管理员可读
- 为 HAProxy，Nginx，DNSMasq，Redis 等组件配置了正确的 SELinux 上下文
- 收回了所有非 root 用户对可执行脚本的拥有权限
- 将 `admin_ip` 添加到 Patroni API 允许访问的 IP 列表白名单中
- 总是创建 admin 系统用户组，patronictl 配置收紧为仅限 admin 组用户访问
- 新增 `node_admin_sudo` 参数，允许指定/调整数据库管理员的 sudo 权限模式（all/nopass）
- 修复了若干 `ansible copy content` 字段为空时报错的问题。
- 修复了 `pg_pitr` 中遗留的一些问题，确保 patroni 集群恢复时没有竞态条件。

---

## 问题修复

- 修复 ownca 证书有效期 Chrome 兼容性问题
- 修复 Vector 0.52 syslog_raw 解析问题
- 修复 pg_pitr 多副本 clonefrom 时序问题
- 修复 Ansible SELinux dnsmasq 竞态条件
- 修复 EL9 aarch64 patroni & llvmjit 问题
- 修复 Debian groupadd 路径问题
- 修复空 sudoers 文件生成问题
- 修复 pgbouncer pid 路径（`/run/postgresql`）
- 修复 `duckdb.allow_community_extensions` 始终生效问题
- 因上游问题隐藏 EL8 上的 pg_partman 扩展

---

## 兼容性

| 操作系统               | x86_64 | aarch64 |
|--------------------|:------:|:-------:|
| EL 8/9/10          |   ✅    |    ✅    |
| Debian 11/12/13    |   ✅    |    ✅    |
| Ubuntu 22.04/24.04 |   ✅    |    ✅    |

**PostgreSQL**: 13, 14, 15, 16, 17, 18
