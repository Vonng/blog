---
title: "Pigsty v3.0：海量扩展，插拔内核，RDS服务"
linkTitle: "Pigsty v3.0 发布注记"
date: 2024-08-25
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v3.0.0)）
summary: >
  Pigsty v3.0 提供了史无前例的 340 个可用扩展插件，并实现了Deb/EL生态插件大对齐，支持可插拔内核，提供 MSSQL，Oracle，PolarDB 兼容性模式，并提供本地优先的 SOTA RDS
series: [Pigsty]
tags: [Pigsty]
---



--------

### 亮点特性

**扩展大爆炸**：

Pigsty v3 提供了史无前例的 [**340**](/docs/pgsql/ext/) 个可用扩展插件。
包括 **121** 个扩展 [**RPM包**](/docs/pgsql/ext/) 与 **133** 个 [**DEB包**](/docs/pgsql/ext/)，数量已经超过了 PGDG 官方仓库提供的扩展数量总和（135 RPM/ 109 DEB）。
而且，Pigsty 还将EL系统与Debian生态的独有PG扩展插件相互移植，实现了两大发行版的插件生态大对齐。

```yaml
- timescaledb periods temporal_tables emaj table_version pg_cron pg_later pg_background pg_timetable
- postgis pgrouting pointcloud pg_h3 q3c ogr_fdw geoip #pg_geohash #mobilitydb
- pgvector pgvectorscale pg_vectorize pg_similarity pg_tiktoken pgml #smlar
- pg_search pg_bigm zhparser hunspell
- hydra pg_lakehouse pg_duckdb duckdb_fdw pg_fkpart pg_partman plproxy #pg_strom citus
- pg_hint_plan age hll rum pg_graphql pg_jsonschema jsquery index_advisor hypopg imgsmlr pg_ivm pgmq pgq #rdkit
- pg_tle plv8 pllua plprql pldebugger plpgsql_check plprofiler plsh #pljava plr pgtap faker dbt2
- prefix semver pgunit md5hash asn1oid roaringbitmap pgfaceting pgsphere pg_country pg_currency pgmp numeral pg_rational pguint ip4r timestamp9 chkpass #pg_uri #pgemailaddr #acl #debversion #pg_rrule
- topn pg_gzip pg_http pg_net pg_html5_email_address pgsql_tweaks pg_extra_time pg_timeit count_distinct extra_window_functions first_last_agg tdigest aggs_for_arrays pg_arraymath pg_idkit pg_uuidv7 permuteseq pg_hashids
- sequential_uuids pg_math pg_random pg_base36 pg_base62 floatvec pg_financial pgjwt pg_hashlib shacrypt cryptint pg_ecdsa pgpcre icu_ext envvar url_encode #pg_zstd #aggs_for_vecs #quantile #lower_quantile #pgqr #pg_protobuf
- pg_repack pg_squeeze pg_dirtyread pgfincore pgdd ddlx pg_prioritize pg_checksums pg_readonly safeupdate pg_permissions pgautofailover pg_catcheck preprepare pgcozy pg_orphaned pg_crash pg_cheat_funcs pg_savior table_log pg_fio #pgpool pgagent
- pg_profile pg_show_plans pg_stat_kcache pg_stat_monitor pg_qualstats pg_store_plans pg_track_settings pg_wait_sampling system_stats pg_meta pgnodemx pg_sqlog bgw_replstatus pgmeminfo toastinfo pagevis powa pg_top #pg_statviz #pgexporter_ext #pg_mon
- passwordcheck supautils pgsodium pg_vault anonymizer pg_tde pgsmcrypto pgaudit pgauditlogtofile pg_auth_mon credcheck pgcryptokey pg_jobmon logerrors login_hook set_user pg_snakeoil pgextwlist pg_auditor noset #sslutils
- wrappers multicorn mysql_fdw tds_fdw sqlite_fdw pgbouncer_fdw mongo_fdw redis_fdw pg_redis_pubsub kafka_fdw hdfs_fdw firebird_fdw aws_s3 log_fdw #oracle_fdw #db2_fdw
- orafce pgtt session_variable pg_statement_rollback pg_dbms_metadata pg_dbms_lock pgmemcache #pg_dbms_job #wiltondb
- pglogical pgl_ddl_deploy pg_failover_slots wal2json wal2mongo decoderbufs decoder_raw mimeo pgcopydb pgloader pg_fact_loader pg_bulkload pg_comparator pgimportdoc pgexportdoc #repmgr #slony
- gis-stack rag-stack fdw-stack fts-stack etl-stack feat-stack olap-stack supa-stack stat-stack json-stack
```

**换内核**：

Pigsty v3 允许您更换 PostgreSQL 内核，目前支持了 SQL Server 兼容的 Babelfish （线缆协议级仿真），Oracle 兼容的 IvorySQL，以及 PG 版的 RAC PolarDB；此外，现在自托管 Supabase 也在 Debian 系统中可用。
您可以让 Pigsty 中带有 HA，IaC，PITR，监控的生产级 PostgreSQL 集群仿真 MSSQL (via WiltonDB)，Oracle via (IvorySQL)，Oracle RAC (via PolarDB), MongoDB（via FerretDB），以及 Firebase （via Supabase）。

**企业版**：

我们现在提供 Pigsty Pro [**专业版**](/docs/about/service)，在开源版的功能基础上提供增值服务。专业版提供额外的功能模块：MSSQL，Oracle，Mongo，K8S，Victoria，Kafka，TigerBeetle 等……，并提供更广泛的 PG 大版本、操作系统、芯片架构的支持。
提供针对全系操作系统精准小版本定制的离线安装包，以及 EL7，Debian 11，Ubuntu 20.04 等过保老系统的支持；此外，专业版还提供内核可插拔定制服务，并对PolarDB PG/Oracle 的原生部署、监控管控支持以满足“国产化”需要。

使用以下命令[**快速安装**](/docs/setup/install)：

```bash
curl -fsSL https://repo.pigsty.cc/get | bash
cd ~/pigsty; ./bootstrap; ./configure; ./install.yml
```


--------

### 重大变更

本次 Pigsty 发布调整大版本号，从 2.x 升级到 3.0，带有一些重大变更：

* 首要支持操作系统调整为：EL 8 / EL 9 / Debian 12 / Ubuntu 22.04
  * EL7 / Debian 11 / Ubuntu 20.04 等系统进入弃用阶段，不再提供支持
  * 有在这些系统上运行需求的用户请考虑我们的 [订阅服务](https://pigsty.io/zh/docs/about/service)

* 默认使用在线安装，不再提供离线软件包，从而解决操作系统小版本兼容性问题。
  * `bootstrap` 过程现在不再询问是否下载离线安装包，但如果 `/tmp/pkg.tgz` 存在，仍然会自动使用离线安装包。 
  * 有离线安装需求请自行制作离线软件包或考虑我们的 [订阅服务](https://pigsty.io/zh/docs/about/service)

* Pigsty 使用的上游软件仓库进行统一调整，地址变更，并对所有软件包进行 GPG 签名与校验
  * 标准仓库： `https://repo.pigsty.io/{apt/yum}`
  * 国内镜像： `https://repo.pigsty.cc/{apt/yum}`

* API 参数变更与配置模板变更
  * EL 系与 Debian 系配置模板现在收拢统一，有差异的参数统一放置于 [`roles/node_id/vars/`](https://github.com/Vonng/pigsty/tree/master/roles/node_id/vars) 目录进行管理。
  * 配置目录变更，所有配置文件模板统一放置在 `conf` 目录下，并分为 `default`, `dbms`, `demo`, `build` 四大类。


--------

### 其他新特性

- PG OLAP 分析能力史诗级加强：DuckDB 1.0.0，DuckDB FDW，以及 PG Lakehouse，Hydra 移植至 Deb 系统中。
- PG 向量检索与全文检索能力加强：Vectorscale 提供 DiskANN 向量索引，Hunspell 分词字典支持，pg_search 0.9.1。
- 帮助 ParadeDB 解决了软件包构建问题，现在我们在 Debian/Ubuntu 上也能提供这一扩展。
- Supabase 所需的扩展在 Debian/Ubuntu 上全部可用，Supabase 现在可在全OS上自托管。
- 提供了场景化预置扩展堆栈的能力，如果您不知道安装哪些扩展，我们准备了针对特定应用场景的扩展推荐包（Stack）。
- 针对所有 PostgreSQL 生态的扩展，制作了元数据表格、文档、索引、名称映射，针对 EL与Deb 进行对齐，确保扩展可用性。
- 为了解决 DockerHub 被 Ban 的问题，我们加强了 `proxy_env` 参数的功能并简化其配置方式。
- 建设了一个专用的新软件仓库，提供了 12-17 版本的全部扩展插件，其中，PG16的扩展仓库会在 Pigsty 默认的版本中实装。
- 现有软件仓库升级改造，使用标准的签名与校验机制，确保软件包的完整性与安全性。APT 仓库采用新的标准布局通过 `reprepro` 构建。
- 提供了 1,2,3,4,43 节点的沙箱环境：`meta`, `dual`, `trio`, `full`, `prod`，以及针对 7 大 OS Distro 的快捷配置模板。
- PG Exporter 新增了 PostgreSQL 17 与 pgBouncer 1.23 新监控指标收集器的定义，与使用这些指标的 Grafana Panel
- 监控面板修缮，修复了各种问题，为 PGSQL Pgbouncer 与 PGSQL Patroni 监控面板添加了日志仪表盘。
- 使用全新的 `cache.yml` Ansible 剧本，替换了原有制作离线软件包的 `bin/cache` 与 `bin/release-pkg` 脚本。

--------

### API变更

* 新参数选项： `pg_mode` 现在支持的模式有 `pgsql`, `citus`, `gpsql`, `mssql`, `ivory`, `polar`，用于指定 PostgreSQL 集群的模式
  * `pgsql`： 标准 PostgreSQL 高可用集群
  * `citus`： Citus 水平分布式 PostgreSQL 原生高可用集群
  * `gpsql`： 用于 Greenplum 与 GP 兼容数据库的监控（专业版）
  * `mssql`： 安装 WiltonDB / Babelfish，提供 Microsoft SQL Server 兼容性模式的标准 PostgreSQL 高可用集群，线缆协议级支持，扩展不可用
  * `ivory`： 安装 IvorySQL 提供的 Oracle 兼容性 PostgreSQL 高可用集群，Oracle语法/数据类型/函数/存储过程兼容，扩展不可用 （专业版）
  * `polar`： 安装 PolarDB for PostgreSQL （PG RAC）开源版本，提供国产化数据库能力支持，扩展不可用。（专业版）
* 新参数： `pg_parameters`，用于在实例级别指定 `postgresql.auto.conf` 中的参数，覆盖集群配置，实现不同实例成员的个性化配置。
* 新参数： `pg_files`，用于将额外的文件拷贝到PGDATA数据目录，针对需要License文件的商业版PostgreSQL分叉内核设计。
* 新参数： `repo_extra_packages`，用于额外指定需要下载的软件包，与 `repo_packages` 共同使用，便于指定OS版本独有的扩展列表。
* 参数重命名： `patroni_citus_db` 重命名为 `pg_primary_db`，用于指定集群中的主要数据库（在 Citus 模式中使用）
* 参数强化：`proxy_env` 中的代理服务器配置会写入 Docker Daemon，解决科学上网问题，`configure -x` 选项会自动在配置中写入当前环境中的代理服务器配置。
* 参数强化：`repo_url_packages` 中的 `repo.pigsty.io` 会在区域为中国时自动替换为 `repo.pigsty.cc`，解决科学上网问题，此外，现在可以指定下载后的文件名称。
* 参数强化：`pg_databases.extensions` 中的 `extension` 字段现在可以支持字典与扩展名字符串两种模式，字典模式提供 `version` 支持，允许安装特定版本的扩展。
* 参数强化：`repo_upstream` 参数如果没有显式覆盖定义，将从 [`rpm.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 或 [`deb.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 中定义的 `repo_upstream_default` 提取对应系统的默认值。
* 参数强化：`repo_packages` 参数如果没有显式覆盖定义，将从 [`rpm.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 或 [`deb.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 中定义的 `repo_packages_default` 提取对应系统的默认值。
* 参数强化：`infra_packages` 参数如果没有显式覆盖定义，将从 [`rpm.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 或 [`deb.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 中定义的 `infra_packages_default` 提取对应系统的默认值。
* 参数强化：`node_default_packages` 参数如果没有显式覆盖定义，将从 [`rpm.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 或 [`deb.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 中定义的 `node_packages_default` 提取对应系统的默认值。
* 参数强化：`pg_packages` 与 `pg_extensions` 中的扩展现在都会从  [`rpm.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 或 [`deb.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) 中定义的 `pg_package_map` 执行一次查找与翻译。
* 参数强化：`node_packages` 与 `pg_extensions` 参数中指定的软件包在安装时会升级至最新版本， `node_packages` 中现在默认值变为 `[openssh-server`]，帮助修复 [OpenSSH CVE](https://pigsty.io/zh/blog/db/cve-2024-6387/)
* 参数强化：`pg_dbsu_uid` 会自动根据操作系统类型调整为 `26` （EL）或 `543` （Debian），避免了手工调整。
* Boostrap 逻辑变化，不再下载离线软件包，添加 `-k|--keep` 参数，用于指定在本地安装 ansible 时是否保留现有的软件源。
* Configure 移除了 `-m|--mode` 参数，使用 `-m|--conf` 参数指定配置文件，使用 `-x|--proxy` 参数指定代理服务器配置，不再尝试修复 ssh 本机问题。
* 设置了 pgbouncer 默认参数，`max_prepared_statements = 128` 启用了事物池化模式下的准备语句支持，并设置 `server_lifetime` 为 600，
* 修改了 patroni 模板默认参数，统一增大 `max_worker_processes` +8 可用后端进程，提高 `max_wal_senders` 与 `max_replication_slots` 至 50，并增大 OLAP 模板临时文件的大小限制为主磁盘的 1/5


--------

### 版本升级

截止至发布时刻，Pigsty 主要组件的版本升级如下：

- [**PostgreSQL**](https://www.postgresql.org/about/news/postgresql-164-158-1413-1316-1220-and-17-beta-3-released-2910/) 16.4, 15.8, 14.13, 13.16, 12.20
- [pg_exporter](https://github.com/Vonng/pg_exporter) : 0.7.0
- [Patroni](https://patroni.readthedocs.io/en/latest/): 3.3.2
- [pgBouncer](https://www.pgbouncer.org/2024/08/pgbouncer-1-23-1): 1.23.1
- [pgBackRest](https://pgbackrest.org/release.html#2.53.1): 2.53.1
- [duckdb](https://github.com/duckdb/duckdb) : 1.0.0
- [etcd](https://github.com/etcd-io/etcd) : 3.5.15
- [pg_timetable](https://github.com/cybertec-postgresql/pg_timetable): 5.9.0
- [ferretdb](https://github.com/FerretDB/FerretDB): 1.23.1
- [vip-manager](https://github.com/cybertec-postgresql/vip-manager): 2.6.0
- [minio](https://github.com/minio/minio): 20240817012454
- [mcli](https://github.com/minio/mc): 20240817113350
- [grafana](https://github.com/grafana/grafana/) : 11.1.4
- [loki](https://github.com/grafana/loki) : 3.1.1
- [promtail](https://github.com/grafana/loki) : 3.0.0
- [prometheus](https://github.com/prometheus/prometheus) : 2.54.0
- [pushgateway](https://github.com/prometheus/pushgateway) : 1.9.0
- [alertmanager](https://github.com/prometheus/alertmanager) : 0.27.0
- [blackbox_exporter](https://github.com/prometheus/blackbox_exporter) : 0.25.0
- [nginx_exporter](https://github.com/nginxinc/nginx-prometheus-exporter) : 1.3.0
- [node_exporter](https://github.com/prometheus/node_exporter) : 1.8.2
- [keepalived_exporter](https://github.com/gen2brain/keepalived_exporter) : 0.7.0
- [pgbackrest_exporter](https://github.com/woblerr/pgbackrest_exporter) 0.18.0
- [mysqld_exporter](https://github.com/prometheus/mysqld_exporter) : 0.15.1
- [redis_exporter](https://github.com/oliver006/redis_exporter) : v1.62.0
- [kafka_exporter](https://github.com/danielqsj/kafka_exporter) : 1.8.0
- [mongodb_exporter](https://github.com/percona/mongodb_exporter) : 0.40.0
- [VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics) : 1.102.1
- [VictoriaLogs](https://github.com/VictoriaMetrics/VictoriaMetrics/releases) : v0.28.0
- [sealos](https://github.com/labring/sealos): 5.0.0
- [vector](https://github.com/vectordotdev/vector/releases) : 0.40.0

Pigsty 重新编译了所有 PostgreSQL 扩展插件，PostgreSQL 扩展插件的最新版本，请参考 [扩展列表](/docs/pgsql/ext/)


--------

### 新应用

Pigsty 现在提供开箱即用的 Dify 与 Odoo Docker Compose 模板：

- [Dify](/docs/software/dify)： AI智能体工作流编排与 LLMOps
- [Odoo](/docs/software/odoo)： 企业级开源 ERP 系统

Pigsty 专业版现在提供试点的 Kubernetes 部署支持与 Kafka KRaft 集群部署与监控支持

- **`KUBE`**： 使用 cri-dockerd 或 containerd 部署由 Pigsty 托管的 Kubernetes 集群
- **`KAFKA`**：部署由 Kraft 协议支持的高可用 Kafka 集群


--------

### 问题修复

- 通过 `node_packages` 中的默认值 `[openssh-server`]，[CVE-2024-6387](https://pigsty.io/zh/blog/db/cve-2024-6387/) 可以在 Pigsty 安装过程中被自动修复。
- 修复了 Loki 解析 Nginx 日志标签基数过大导致的内存消耗问题。
- 修复了 EL8 系统中上游 Ansible 依赖变化导致的 bootstrap 失效问题（python3.11-jmespath 升级至 python3.12-jmespath）
