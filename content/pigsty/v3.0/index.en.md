---
title: "Pigsty v3.0: Pluggable Kernels & 340 Extensions"
linkTitle: "Pigsty v3.0 Release"
date: 2024-08-25
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v3.0.0))
summary: >
  Pigsty v3.0 ships 340 extensions across EL/Deb with full parity, adds pluggable kernels (Babelfish, IvorySQL, PolarDB) for MSSQL/Oracle compatibility, and delivers a local-first state-of-the-art RDS experience.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.0.0) | [**Release Note**](https://pigsty.io/docs/releasenote/#v300)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.0.0)

--------

### Highlights

**Extension Explosion**:

Pigsty v3 ships an unprecedented [**340**](https://pigsty.cc/docs/pgsql/ext/) available PostgreSQL extensions.
This includes **121** extension [**RPM packages**](https://pigsty.cc/docs/pgsql/ext/) and **133** [**DEB packages**](https://pigsty.cc/docs/pgsql/ext/) — more than the total extension count in the official PGDG repositories (135 RPM / 109 DEB).
Moreover, Pigsty cross-ports EL-exclusive and Debian-exclusive extensions, achieving full ecosystem parity between the two major Linux families.

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

**Pluggable Kernels**:

Pigsty v3 lets you swap out the PostgreSQL kernel. Current options include SQL Server-compatible Babelfish (wire-protocol-level emulation), Oracle-compatible IvorySQL, and PolarDB (the PostgreSQL RAC). Self-hosted Supabase is also now available on Debian systems.
You can run production-grade PostgreSQL clusters with HA, IaC, PITR, and full observability while emulating MSSQL (via WiltonDB), Oracle (via IvorySQL), Oracle RAC (via PolarDB), MongoDB (via FerretDB), or Firebase (via Supabase).

**Pro Edition**:

We now offer Pigsty Pro [**Professional Edition**](https://pigsty.cc/docs/about/service), providing value-added services on top of the open-source version. Pro includes additional modules: MSSQL, Oracle, Mongo, K8S, Victoria, Kafka, TigerBeetle, and more, with broader support for PG major versions, operating systems, and chip architectures.
It provides precision-tuned offline packages for every OS minor version, plus support for legacy systems like EL7, Debian 11, and Ubuntu 20.04. Pro also offers customizable kernel support with native deployment, monitoring, and management for PolarDB PG/Oracle to meet localization requirements.

**Quick Install**:

```bash
curl -fsSL https://repo.pigsty.cc/get | bash
cd ~/pigsty; ./bootstrap; ./configure; ./install.yml
```


--------

### Breaking Changes

This Pigsty release bumps from 2.x to 3.0, introducing several breaking changes:

* Primary OS support shifts to: EL 8 / EL 9 / Debian 12 / Ubuntu 22.04
  * EL7 / Debian 11 / Ubuntu 20.04 are now deprecated and no longer supported
  * Users requiring these systems should consider our [subscription service](https://pigsty.io/docs/about/service)

* Default installation is now online; offline packages are no longer provided, resolving OS minor version compatibility issues.
  * The `bootstrap` process no longer prompts for offline package download, but will still auto-use one if `/tmp/pkg.tgz` exists.
  * For offline installation needs, build your own packages or consider our [subscription service](https://pigsty.io/docs/about/service)

* Pigsty upstream repositories have been consolidated, addresses changed, with GPG signing and verification for all packages
  * Standard repo: `https://repo.pigsty.io/{apt/yum}`
  * China mirror: `https://repo.pigsty.cc/{apt/yum}`

* API parameter changes and config template updates
  * EL and Debian config templates are now unified, with OS-specific parameters managed in [`roles/node_id/vars/`](https://github.com/Vonng/pigsty/tree/master/roles/node_id/vars).
  * Config directory restructured: all templates now in `conf/`, organized into `default`, `dbms`, `demo`, `build` categories.


--------

### Other Features

- Epic OLAP enhancement: DuckDB 1.0.0, DuckDB FDW, PG Lakehouse, and Hydra ported to Debian.
- Vector search and FTS improvements: Vectorscale brings DiskANN vector indexing, Hunspell dictionary support, pg_search 0.9.1.
- Helped ParadeDB resolve package build issues — this extension is now available on Debian/Ubuntu.
- All Supabase-required extensions now available on Debian/Ubuntu; Supabase can now self-host on all supported OSes.
- Scenario-based extension stacks: if you're unsure which extensions to install, we've prepared recommended bundles for specific use cases.
- Complete metadata tables, docs, indexes, and name mappings for all PostgreSQL ecosystem extensions, aligned across EL and Debian.
- Enhanced `proxy_env` parameter to address DockerHub access issues, with simplified configuration.
- Built a dedicated new repository providing all extensions for PostgreSQL 12-17, with PG16 extensions enabled by default in Pigsty.
- Upgraded existing repos with standard GPG signing and verification. APT repos now use standard layout built with `reprepro`.
- Sandbox environments for 1, 2, 3, 4, and 43 nodes: `meta`, `dual`, `trio`, `full`, `prod`, plus quick config templates for 7 major OS distros.
- PG Exporter adds PostgreSQL 17 and pgBouncer 1.23 metric collectors, with corresponding Grafana panels.
- Monitoring dashboard fixes, added log dashboards for PGSQL Pgbouncer and PGSQL Patroni panels.
- New `cache.yml` Ansible playbook replaces the old `bin/cache` and `bin/release-pkg` scripts for offline package creation.


--------

### API Changes

* New parameter option: `pg_mode` now supports `pgsql`, `citus`, `gpsql`, `mssql`, `ivory`, `polar` for specifying PostgreSQL cluster mode
  * `pgsql`: Standard PostgreSQL HA cluster
  * `citus`: Citus distributed PostgreSQL native HA cluster
  * `gpsql`: Monitoring for Greenplum and GP-compatible databases (Pro)
  * `mssql`: Install WiltonDB/Babelfish, providing Microsoft SQL Server compatibility mode with wire-protocol support, extensions unavailable
  * `ivory`: Install IvorySQL for Oracle-compatible PostgreSQL HA cluster with Oracle syntax/datatypes/functions/stored procedures, extensions unavailable (Pro)
  * `polar`: Install PolarDB for PostgreSQL (PG RAC) open-source version for localized database support, extensions unavailable (Pro)
* New parameter: `pg_parameters` for instance-level `postgresql.auto.conf` overrides, enabling per-instance customization.
* New parameter: `pg_files` for copying additional files to PGDATA, designed for commercial PostgreSQL forks requiring license files.
* New parameter: `repo_extra_packages` for specifying additional packages to download, works with `repo_packages` for OS-specific extension lists.
* Parameter rename: `patroni_citus_db` renamed to `pg_primary_db` for specifying the primary database in a cluster (used in Citus mode)
* Enhanced `proxy_env`: Proxy server config now written to Docker Daemon for network access; `configure -x` auto-writes current environment proxy settings.
* Enhanced `repo_url_packages`: `repo.pigsty.io` auto-replaces with `repo.pigsty.cc` when region is China; can now specify downloaded filenames.
* Enhanced `pg_databases.extensions`: The `extension` field now supports both dictionary and string modes; dictionary mode provides `version` support for installing specific extension versions.
* Enhanced `repo_upstream`: If not explicitly overridden, defaults are extracted from `repo_upstream_default` in [`rpm.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/rpm.yml) or [`deb.yml`](https://github.com/Vonng/pigsty/blob/master/roles/node_id/vars/deb.yml).
* Enhanced `repo_packages`: If not explicitly overridden, defaults are extracted from `repo_packages_default` in the corresponding OS vars file.
* Enhanced `infra_packages`: If not explicitly overridden, defaults are extracted from `infra_packages_default` in the corresponding OS vars file.
* Enhanced `node_default_packages`: If not explicitly overridden, defaults are extracted from `node_packages_default` in the corresponding OS vars file.
* Enhanced `pg_packages` and `pg_extensions`: Extensions now undergo lookup and translation from `pg_package_map` in the corresponding OS vars file.
* Enhanced `node_packages` and `pg_extensions`: Packages are upgraded to latest version during installation; `node_packages` default now includes `[openssh-server]` to help fix [OpenSSH CVE](https://pigsty.io/blog/db/cve-2024-6387/)
* Enhanced `pg_dbsu_uid`: Auto-adjusts to `26` (EL) or `543` (Debian) based on OS type, avoiding manual adjustment.
* Bootstrap logic change: No longer downloads offline packages; added `-k|--keep` flag to preserve existing package sources during local ansible installation.
* Configure: Removed `-m|--mode` parameter; use `-m|--conf` to specify config file, `-x|--proxy` for proxy config; no longer attempts to fix local SSH issues.
* pgbouncer defaults: `max_prepared_statements = 128` enables prepared statement support in transaction pooling mode; `server_lifetime` set to 600.
* Patroni template defaults: Increased `max_worker_processes` by +8, raised `max_wal_senders` and `max_replication_slots` to 50, increased OLAP template temp file limit to 1/5 of main disk.


--------

### Software Upgrades

At release time, Pigsty's major component versions are:

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

Pigsty has recompiled all PostgreSQL extensions. For the latest extension versions, see the [Extension List](https://pigsty.cc/docs/pgsql/ext/).


--------

### New Applications

Pigsty now provides out-of-the-box Docker Compose templates for Dify and Odoo:

- [Dify](https://pigsty.cc/docs/software/dify): AI agent workflow orchestration and LLMOps
- [Odoo](https://pigsty.cc/docs/software/odoo): Enterprise-grade open-source ERP system

Pigsty Pro now offers pilot Kubernetes deployment support and Kafka KRaft cluster deployment with monitoring:

- **`KUBE`**: Deploy Pigsty-managed Kubernetes clusters using cri-dockerd or containerd
- **`KAFKA`**: Deploy HA Kafka clusters powered by the KRaft protocol


--------

### Bug Fixes

- [CVE-2024-6387](https://pigsty.io/blog/db/cve-2024-6387/) is automatically patched during Pigsty installation via the `node_packages` default value `[openssh-server]`.
- Fixed Loki memory consumption issue caused by high-cardinality Nginx log labels.
- Fixed bootstrap failure on EL8 due to upstream Ansible dependency changes (python3.11-jmespath upgraded to python3.12-jmespath).


--------

## v3.0.0 Release Notes

**Highlights**

* PostgreSQL 16.4, 15.8, 14.13, 13.16, 12.20
* 340 PostgreSQL extensions available
* EL/Debian extension ecosystem parity achieved
* Pluggable kernels: Babelfish, IvorySQL, PolarDB support
* Supabase now available on Debian systems
* Pigsty Pro edition with extended OS and module support

**Breaking Changes**

* Primary OS support: EL8/EL9, Debian 12, Ubuntu 22.04
* Legacy systems (EL7, Debian 11, Ubuntu 20.04) require subscription
* Default online installation; offline packages discontinued
* Repository consolidation with GPG signing

**API Changes**

* New `pg_mode` options: `pgsql`, `citus`, `gpsql`, `mssql`, `ivory`, `polar`
* New parameters: `pg_parameters`, `pg_files`, `repo_extra_packages`
* `patroni_citus_db` renamed to `pg_primary_db`
* Enhanced: `proxy_env`, `repo_url_packages`, `pg_databases.extensions`
* Auto-derived defaults for `repo_upstream`, `repo_packages`, `infra_packages`, `node_default_packages`
* Bootstrap `-k|--keep` flag; Configure `-m|--conf` and `-x|--proxy` flags

**Bug Fixes**

* OpenSSH CVE-2024-6387 auto-remediation
* Loki high-cardinality label memory fix
* EL8 Ansible dependency bootstrap fix

```bash
MD5 (pigsty-v3.0.0.tgz) = acc802fc2a47a838f09a39e7615ee4d9
```
