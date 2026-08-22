---
title: "Pigsty v4.5: 575 Extensions, Silo, Valkey, Kafka, and MySQL"
linkTitle: "Pigsty v4.5 Released"
date: 2026-08-15
authors: [vonng]
summary: >
  Pigsty v4.5 is out, bringing the PostgreSQL extension count to 575, replacing MinIO with Silo for object storage, adding Valkey to the Redis module, and introducing pilot Kafka and MySQL modules, along with broad improvements to orchestration safety and observability.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.5.0) | [**Release Note**](https://pigsty.io/docs/about/release/#v450)

Pigsty v4.5 is officially out. At the end of the previous release, I said there might be a transitional v4.5 before 5.0. Here it is—except this "transitional" release ended up more packed than many full-fledged major releases.

Here is the short version of what is new in v4.5:

- **575 PostgreSQL extensions**: up from 531, with new additions including pg_lake, pg_jieba, and plruby.
- **Silo object storage**: the MINIO module has switched engines and now runs Silo, Pigsty's own maintained MinIO fork.
- **Valkey**: the REDIS module adds Valkey as an engine. One parameter switches it over while preserving the inventory, monitoring, and dashboards.
- **Kafka module**: a new pilot module with native KRaft orchestration for multiple clusters, dynamic membership, SCRAM/TLS, and four monitoring dashboards.
- **MySQL module**: yes, MySQL. You read that right. It supports MySQL 8.4 LTS as either a standalone instance or a three-node InnoDB Cluster, also as a pilot module.
- And a long tail of smaller but useful changes: explicit cluster identities, safer removal workflows, pg_exporter 1.4, the SOW repository tool, 51 configuration templates, and more.

Let's go through them in order.

------

## 575 Extensions

Every release gets a new extension count. This time it is **575**—46 additions and two removals since v4.4's 531, for a net gain of 44. The full catalog is still available in the [**extension list**](https://pigsty.io/ext/list). Here are a few of the more notable arrivals:

- The complete [**`pg_lake`**](https://pigsty.io/ext/e/pg_lake) suite: the lakehouse stack that Snowflake open-sourced after acquiring Crunchy Data. It uses DuckDB as a vectorized execution engine and brings Iceberg and Parquet directly into PostgreSQL. This is the most important new development in the PostgreSQL data-lake ecosystem this year, and Pigsty packaged it immediately for PostgreSQL 16–18. On the RPM side, it is currently available only for EL 9/10.
- **`pg_jieba`** and **`pg_cjk_parser`**: Chinese and CJK tokenizers. Anyone building Chinese full-text search knows what this means—people who used to compile pg_jieba themselves can finally stop.
- **`plruby`**: the Ruby procedural language, packaged together with its three type-conversion subextensions for hstore, jsonb, and ltree. Another piece of the procedural-language puzzle is in place. I am also curious who will actually write stored procedures in Ruby.
- **`pgmemento`**: auditing and data-change tracking implemented entirely in SQL, giving tables a complete timeline.
- **`online_advisor`**: recommends indexes online based on queries that actually run.
- **`pg_turbovec`**, **`pgcontext`**, and **`pg_tiktoken_c`**: more depth for vector search and RAG, joined by `pgmnemo` 0.16 for agent memory. The AI toolkit keeps getting thicker.
- There are also more specialized additions such as `pgwasm` for WebAssembly, `postbis` for bioinformatics sequences, `qdgc` for geographic grids with a PostGIS subextension, and `pg_vault_tde` for transparent encryption backed by Vault.

Beyond the additions, this cycle rebuilt almost every Rust extension against pgrx 0.19.1. Many package version numbers look unchanged, but the entire build matrix was rerun behind the scenes. An unchanged version number does not mean no work happened.

Two extensions were removed: `pg_analytics`, which upstream has archived, and `spat`, a discontinued alpha project. Five others—`emailaddr`, `explain_ui`, `oidc_validator`, `pg_summarize`, and `smlar`—were removed from the default installation groups because upstream provides no license. The packages remain available, but you must install them explicitly and assess the licensing and redistribution boundaries yourself. A distribution can package software for you; it cannot assume your compliance obligations.

Routine upgrades continued as well: Citus 14.2, TimescaleDB 2.29.1, pgvector 0.8.6, pg_search 0.25.2, DocumentDB 0.114, pg_partman 5.5, pgmq 1.12, and more. The complete package change log runs for more than 200 lines; see the [**release note**](https://pigsty.io/docs/about/release/#v450) rather than making me reproduce it here.

------

## Silo: A New Engine for Object Storage

Long-time readers know the MinIO story. Upstream reduced its admin console to little more than a login page, the community edition was effectively abandoned, and I forked it to keep it alive and patch CVEs. I wrote about that in [**MinIO Is Dead**](/db/minio-is-dead) and [**Two Months into Maintaining a MinIO Fork**](/db/minio-promise-kept). That fork eventually got its own name: **Silo**. Put a grain silo beside the Pigsty, add the `pig` package manager and the `sow` repository tool, and the whole family is together.

v4.5 takes that transition to its conclusion: **the MINIO module now deploys Silo, and only Silo**. The only valid value for `minio_type` is currently `silo`. Compatibility should not be a concern: the S3 and Admin APIs, `/minio/*` routes, `MINIO_*` environment variables, and on-disk data format all remain unchanged. Only the package, binary, and systemd service names have changed. For existing users, this is closer to swapping in an engine with a new badge while leaving the chassis and controls untouched.

Protocol compatibility does not validate the migration for you, of course. Before switching production object storage, you still need backups, a rollback plan, and real read/write verification.

The Silo transition comes with several related improvements:

- Startup now verifies three signals: the systemd Invocation ID, `ActiveState`, and Silo cluster health. It waits up to roughly 600 seconds and no longer mistakes the state of an old process for a successful start of the current one.
- Object-storage nodes are grouped by `minio_cluster` identity. One inventory can declare multiple clusters, each with its own `minio_alias` and `minio_endpoint`.
- The `ha/trio` high-availability template replaces its single-node object store with a three-node, single-drive Silo cluster using EC:1, exposed on port 9002 through a VIP and HAProxy.
- Distributed Silo requires `/data/minio` to be a separate filesystem. A normal directory on the root filesystem is rejected outright—this guardrail is there to prevent the all-too-common mistake of putting production object storage on the root volume.

What about RustFS? We did implement a RustFS backend during this development cycle, then pulled it before release. It is not quite ready; we will revisit it once it reaches a genuinely stable GA release. The repository still contains the RustFS 1.0.0-rc.1 package if you want to experiment, but it is not a backend supported by the v4.5 MINIO module.

------

## Valkey: An Alternative to Redis

I have written plenty about the Redis licensing drama, including [**Redis Going Non-Open-Source Is a Disgrace to "Open Source" and Public Clouds**](/db/redis-oss). Redis 8 later returned under the AGPL, but the community fork Valkey has developed into an ecosystem of its own, backed by the Linux Foundation and packaged by every major distribution. Users kept asking whether Pigsty could run Valkey.

Now it can: set `redis_type: valkey`. That is all it takes.

We deliberately designed this as a transparent switch. Pigsty installs `valkey-server` and `valkey-cli`, while configuration paths, data directories, service names, monitoring jobs, and module parameters all stay under the `redis` namespace. Existing inventories, dashboards, and alert rules require no changes. The engine choice applies per cluster, so do not mix engines within one cluster. Before converting an existing Redis cluster to Valkey, rehearse in a test environment and verify data and replication compatibility for yourself. For an idea of how deep the official-package rabbit hole goes, see [**A Packaging Patch Has Been Corrupting Valkey's Memory Accounting Since 2017**](/db/valkey-bug).

The Redis/Valkey systemd units now use `Type=notify`, and the startup timeout has been extended to 1,800 seconds so systemd no longer kills large instances while they load data. Topology construction, password handling, and removal safeguards were hardened as well.

------

## Kafka: From Package to Module

Why should a PostgreSQL distribution manage Kafka? Because in real data architectures, a Kafka cluster is very often sitting next to PostgreSQL. Change data capture, message queues, and event streams all need to run somewhere. Pigsty already shipped Kafka packages—and `kafka_fdw`—but deployment was manual. v4.5 adds a complete [**KAFKA module**](https://pigsty.io/docs/kafka/).

The module is based on Kafka 4.3, runs pure KRaft with no ZooKeeper, and provides orchestration built from scratch in the Pigsty style:

- `kafka_cluster` and `kafka_seq` define cluster identity. Nodes can take combined, broker, or controller roles, and one inventory can contain multiple Kafka clusters.
- Dynamic KRaft quorum management covers controller onboarding, broker admission, member retirement, and three-stage replacement of failed members, all as standardized playbook workflows.
- Security includes SCRAM-SHA-512 and TLS. Credentials and certificates can be rotated, followed automatically by partition health checks.
- Monitoring is comprehensive: JMX Exporter plus Kafka Exporter, alert rules, and four Grafana dashboards for Overview, Instance, Topic, and Consumer views.
- Dangerous operations follow strict rules. `kafka-rm.yml` requires an explicit scope through `-l`, then validates data directories and surviving nodes before stopping services. An incomplete `--limit` is rejected outright, eliminating the chance of touching only half the quorum by mistake.

To try it, use the ready-made `conf/demo/kafka.yml` template.

Kafka is currently a pilot module. Keep one architectural constraint in mind: the Kafka protocol requires clients to connect directly to every broker, so its data plane cannot sit behind HAProxy, a VIP, or a Layer 4 load balancer. That is not a Pigsty limitation; it is simply how Kafka works.

------

## MySQL: Bet You Didn't See That Coming

What happened to [**Postgres Is Eating the Database World**](/pg/pg-eat-db-world)? Why turn around and ship a MySQL module in Pigsty?

Easy. Even world domination has an order of operations. The installed base of MySQL is enormous. Many users put new systems on PostgreSQL while still having to maintain legacy MySQL applications. Others have committed to migrating, but still need someone to operate dozens of MySQL clusters until that migration finishes. Instead of making them build a separate monitoring, backup, and high-availability stack for legacy systems, Pigsty can manage them on the same foundation. Monitoring, alerting, backup, recovery, and cluster orchestration are generic infrastructure anyway.

Bring them into the fold first; digest them later. Perfectly reasonable.

The new pilot [**MYSQL module**](https://pigsty.io/docs/mysql/) in v4.5 looks like this:

- It targets **MySQL 8.4 LTS**, using packages from the official community repository together with Percona XtraBackup.
- It supports either a standalone instance or a three-node **InnoDB Cluster** using Group Replication, with MySQL Shell and MySQL Router. Cluster membership must be exactly one or three nodes; nothing else is accepted.
- Users and databases are provisioned declaratively through `mysql_users` and `mysql_databases`. Scheduled full backups use XtraBackup, and TLS is enabled by default.
- `mysql_parameters` exposes tunables, but settings reserved for replication, TLS, and the platform are protected. Prefixes such as `loose_` and `skip_` cannot bypass those protections.
- Five dashboards cover Overview, Cluster, Instance, Replication, and Alert views. mysqld_exporter plugs into the unified service-discovery and alerting system.
- The `mysql-rm.yml` removal playbook is the most conservative of all the modules: if a target host has no MySQL identity, it fails immediately rather than "helpfully" cleaning anything up.

The demo template is `conf/demo/mysql.yml`. If what you really want is for PostgreSQL to speak the MySQL protocol, Pigsty also offers [**OpenHalo**](/pg/openhalo-mysql). As for whether PostgreSQL or MySQL is better, I will leave that for another essay: [**PostgreSQL vs. MySQL in 2026**](/pg/pg-vs-mysql-2026).

------

## The Rest of the List

Those are the headline changes. Here are the smaller ones still worth knowing about.

### The FERRET Module Is Split Up

The standalone FERRET module and its `mongo.yml` playbook have been removed. MongoDB compatibility is now divided into two layers: PostgreSQL with the DocumentDB extension provides the data layer, configured through the `conf/mongo.yml` template, while FerretDB runs as a Docker application and provides the protocol layer. The old ferretdb systemd service, dedicated monitoring, and dashboards are no longer included. This makes the division of responsibility clearer: data belongs to the database, and protocol translation belongs to the container.

### Safer Orchestration

This release invests heavily in making sure playbooks do not cause collateral damage:

- Initialization and removal playbooks for PGSQL, REDIS, MINIO, KAFKA, and MYSQL now select members by explicit cluster identity—parameters such as `pg_cluster`—instead of relying only on inventory group names. A playbook run against the wrong group skips unrelated hosts rather than "helpfully" installing something on them.
- PITR and removal now delete only the etcd subtree bounded by `/<cluster-name>/`. Previously, if one cluster name was a prefix of another—`pg-test` and `pg-test2`, for example—cleanup could delete the neighboring cluster's metadata. It cannot anymore.
- The initial pgBackRest backup writes its marker file only after the backup command actually succeeds. No more markers claiming that a backup exists when it does not.
- Removal workflows across all modules now stop services before deleting data. Kafka, MySQL, and object storage also perform additional checks on data directories, quorums, and surviving members.
- The full `pgsql.yml` playbook is now explicitly marked for first-time initialization only. It restarts Patroni/PostgreSQL and reapplies configuration and initialization SQL; it is not a day-to-day convergence tool. Do not rerun the whole playbook against a production cluster.
- DBSU SSH keys are exchanged among the actual cluster members, correctly covering cross-group topologies such as Citus. Pigsty-rendered systemd units now live consistently under `/etc/systemd/system`, and permissions are tighter for sensitive configuration and privileged files.

None of these changes is a new feature. Every one of them corresponds to a real class of production incident.

### Observability

- The entire Grafana dashboard set was re-exported through the `pig` toolchain in Dashboard API v2 format. Four Kafka dashboards and five MySQL dashboards were added, while the Node, PGSQL, Redis, and Infra dashboards were refreshed.
- `pg_exporter` moves to the 1.4 series. It includes new PostgreSQL 19 collectors for subscriptions, recovery status, WAL, lock waits, and vacuum pressure. PostgreSQL 10 and later also gain a `pg_xact_age` transaction-age histogram, making the remaining distance to transaction ID wraparound directly visible.
- The MinIO/Silo dashboard now uses the Metrics V3 endpoint and drops high-cardinality samples labeled by bucket, substantially reducing time-series load for users with large numbers of buckets.

### Repositories and Supply Chain

- Local software repositories are now generated by **SOW**, the repository-management tool previewed at the end of v4.4—named, naturally, after a mother pig. `sow create --pigsty` atomically generates DNF/APT metadata and a SHA-256 completion marker, and the old injected fake ModuleMD metadata is gone entirely.
- Offline package bundles can now include versioned source packages. Pigsty-built packages consistently use SHA-256-pinned inputs, SPDX license expressions, and the `1PGSTY` release suffix.
- Exporter RPM names now use hyphens instead of underscores (`node_exporter` → `node-exporter`), with a smooth transition from the old names through Provides/Obsoletes.
- Mirror routing for China has been completely refreshed: Tencent Cloud is preferred, with Huawei Cloud, Alibaba Cloud, and USTC as platform-specific fallbacks.

### Kernels and Platforms

- The default PostgreSQL version is now **18.6**. Four standard Patroni templates add an `output_plugin_libraries` allowlist for logical decoding plugins—`pgoutput`, `test_decoding`, and `wal2json`—and Patroni automatically filters out the parameter on older PostgreSQL versions.
- The PostgreSQL 19 beta template now supports backups through pgBackRest 2.59. In v4.4, pgBackRest could not yet recognize the PostgreSQL 19 control file; PostgreSQL 19 test environments can now take proper backups.
- Percona PostgreSQL 18 TDE enables cluster mode. IvorySQL fixes default-database initialization and enables compatible WAL compression.
- OS baselines move to Rocky Linux 9.8/10.2, Debian 12.15/13.6, and Ubuntu 22.04.5/24.04.4/26.04. The Docker base image moves to Debian 13.6.
- There are now **51 configuration templates**, including the new `demo/kafka`, `demo/mysql`, and the eight-node `ha/octo` simulation environment. `ha/trio` now uses a three-node Silo topology.
- The Vagrant root-disk size is configurable through `root_disk`, which defaults to 64 GB. `disk` continues to represent the additional `/data` data disk. VM login shells are now consistently Bash.

### Component Versions

| Component          | v4.4.0  | v4.5.0   | Notes                              |
|:-------------------|:--------|:---------|:-----------------------------------|
| `pig`              | 1.5.1   | 1.8.0    | Extension catalog refreshed        |
| `sow`              | 0.2.0   | 0.3.0    | Core dependency for local repos    |
| `silo`             | -       | 20260806 | Replaces the MinIO server          |
| `pg_exporter`      | 1.3.0   | 1.4.1    | PostgreSQL 19 metrics support      |
| `etcd`             | 3.6.13  | 3.7.1    |                                    |
| `grafana`          | 13.1.0  | 13.1.3   | Includes security fixes            |
| `victoria-metrics` | 1.147.0 | 1.149.0  | Entire Victoria suite updated      |
| `loki`             | 3.6.7   | 3.7.6    | promtail remains frozen at 3.6.7   |
| `postgrest`        | 14.14   | 16.1     | Major-version upgrade              |
| `pg-timetable`     | 6.3.0   | 7.0.0    | Major-version upgrade              |
| `vip-manager`      | 4.2.0   | 5.0.0    | Configuration is not backward-compatible |
| `jmx-exporter`     | -       | 1.6.0    | Added for Kafka monitoring         |
| `k3s`              | -       | 1.36.3   | Added with matching offline images |
| `duckdb`           | 1.5.4   | 1.5.5    |                                    |

For the complete Infra and extension package change logs, see the [**release note**](https://pigsty.io/docs/about/release/#v450).

------

## Upgrade Notes

Before upgrading from v4.4, work through this list. Every item can bite:

1. **`minio_type` accepts only `silo`**: the protocol and disk format are compatible, but the package, binary, and service names have changed. Do not switch production object storage without tested backups and rollback procedures.
2. **The `ha/trio` object-storage topology has changed**: the new template uses three single-drive Silo nodes. You cannot expand an existing single-node pool in place simply by adding two machines; build a new cluster and migrate the data.
3. **FERRET is split up**: the `mongo.yml` playbook, `mongo_*` parameters, and dedicated dashboards are gone. Redeploy using the Mongo configuration template plus the Docker application.
4. **Cluster identities are required**: custom inventories must define `pg_cluster`, `redis_cluster`, `minio_cluster`, `kafka_cluster`, or `mysql_cluster` as appropriate on every target host.
5. **`pgsql.yml` is only for initial provisioning**: use precise tags for routine maintenance on initialized clusters; do not rerun the entire playbook.
6. **Valkey is opt-in**: without `redis_type: valkey`, Pigsty still deploys Redis. Engine changes apply per cluster; rehearse before switching.
7. **SOW is now a hard dependency of REPO/CACHE**: if an older offline bundle or local repository lacks sow 0.3.0, install it from the Pigsty Infra repository first.
8. **Exporter RPMs have been renamed**: external automation and private repositories should migrate from names such as `node_exporter` and `redis_exporter` to the new hyphenated package names.
9. **Five unlicensed extensions left the default installation groups**: environments that depend on `emailaddr`, `explain_ui`, `oidc_validator`, `pg_summarize`, or `smlar` must install them explicitly.
10. **HAProxy unit semantics have changed**: Pigsty no longer renders `/etc/default/haproxy`. If you override `EXTRAOPTS`, preserve the master-socket option and do not put `-f` in it.
11. **`make purge` deletes `./data` immediately**: cleanup under the Docker directory no longer has a countdown and no longer accepts an external `DATA` variable. Check the target yourself before running it.
12. **Kafka and MySQL are pilot modules**: Kafka clients must be able to reach every broker directly; MySQL clusters must contain exactly one or three members.

------

## Get v4.5

On a fresh, supported Linux node:

```bash
curl -fsSL https://repo.pigsty.io/get | bash -s v4.5.0
cd ~/pigsty
./bootstrap
./configure
./install.yml
```

Users in mainland China can replace `repo.pigsty.io` with `repo.pigsty.cc`. A production upgrade is not a matter of installing over the existing deployment: read the upgrade notes above, verify inventory identities, backups, and the actual runtime state, then roll out changes with an explicit `-l` scope.

------

## Closing Thoughts

The theme of v4.4 was "from integration to distribution." The theme of v4.5 might be "expanding boundaries." Inside the PostgreSQL ecosystem, the extension catalog has grown to 575. Looking outward, object storage, caching, message queues, and even MySQL now share the same orchestration, monitoring, and delivery system.

Some may ask why a PostgreSQL distribution should cover so much. My view is that users never really want "a database"; they want an entire data infrastructure stack that can run their business. PostgreSQL sits at its core, but everything around that core—caches, object storage, message queues, and legacy databases—still needs to be managed to the same standards. Pigsty is a pigsty, after all, and it was never home to just one pig.

The next stop is 5.0. PostgreSQL 19 is due for release in September, and Pigsty 5.0 will arrive with full PostgreSQL 19 support. The groundwork is already in this release: PostgreSQL 19 metrics in pg_exporter, parameter placeholders in the Patroni templates, and backup support in pgBackRest. SOW, built in preparation for the enterprise edition's conservative package repository, is now a formal dependency as well. See you in September.

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.5.0) | [**Release Note**](https://pigsty.io/docs/about/release/#v450)
