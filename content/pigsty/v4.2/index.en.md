---
title: "Pigsty v4.2: 12 Kernels in Bloom"
linkTitle: "Pigsty v4.2: 12 Kernels in Bloom"
date: 2026-02-28
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v4.2.0))
summary: >
  Harness the superpower of 12 PostgreSQL kernels in one stack: Babelfish, AgensGraph, pgEdge, OriolePG, OpenHalo, Cloudberry, and more.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.2.0) | [**Release Note**](https://pigsty.io/docs/about/release/#v420)

Pigsty v4.2 is officially released, hot on the heels of PostgreSQL's emergency out-of-band minor updates.

This release ships three brand-new PG kernels — the graph database AgensGraph, the multi-master distributed pgEdge, and the MPP data warehouse Cloudberry — while rebuilding three existing kernels: Babelfish, OrioleDB, and OpenHalo. With these additions, Pigsty now supports a total of **12 kernels**.

With a single configuration file, you can deploy all these different flavors of PostgreSQL as enterprise-grade database services — complete with monitoring, high availability, point-in-time recovery, and Infrastructure as Code. That is essentially what a "Meta PG Distribution" means.

------

## A Garden of Kernels

PostgreSQL is renowned for its extreme extensibility. The ecosystem offers over 1,000 extensions, and Pigsty provides 461 of them out of the box.

But some capabilities are beyond what extensions can achieve — namely, **custom syntax**. If you want native Oracle PL/SQL, SQL Server T-SQL, MongoDB's BSON wire protocol, or Cypher graph queries inside PostgreSQL — not emulated through function calls, but as first-class syntax — you need to modify the kernel. That is why Pigsty not only provides the largest collection of extensions in the ecosystem, but also supports different kernel forks.

Using these kernels in Pigsty is virtually identical to using vanilla PostgreSQL — the same deployment workflow, the same monitoring dashboards, the same HA mechanisms, the same backup and recovery. The only difference is changing one `pg_mode` value in your configuration file. A one-line config change, an engineering grand unification.

| Kernel                    | pg_mode  | Positioning                                  | PG Baseline |
|:--------------------------|:---------|:---------------------------------------------|:------------|
| **PostgreSQL**            | `pgsql`  | Vanilla kernel + 461 extensions              | 14 – 18     |
| **Babelfish**             | `mssql`  | SQL Server compatible (T-SQL / TDS)          | 17          |
| **IvorySQL**              | `ivory`  | Oracle compatible (PL/iSQL)                  | 18          |
| **OrioleDB**              | `oriole` | New storage engine, solves MVCC bloat        | 17          |
| **pgEdge**                | `pgedge` | Multi-master distributed replication         | 17          |
| **Percona TDE**           | `tde`    | Transparent data encryption                  | 17          |
| **AgensGraph**            | `agens`  | Graph database (Cypher)                      | 16          |
| **OpenHalo**              | `halo`   | MySQL wire-protocol compatible               | 14          |
| **Cloudberry**            | `gpsql`  | MPP analytical data warehouse                | 14          |
| **PolarDB**               | `polar`  | Shared-storage architecture                  | 15          |
| **Citus**                 | `citus`  | Distributed HTAP                             | 17          |
| **Ferret / DocumentDB**   | `mongo`  | MongoDB wire-protocol compatible             | 17          |

Twelve kernels, one config file. Let's walk through them one by one.

------

## Vanilla PostgreSQL

This round of PostgreSQL minor releases deserves a special mention.

The 18.2 series introduced regression bugs related to `substring` and WAL replay — fixing a vulnerability inadvertently created new bugs. The community reacted swiftly, shipping emergency patches 18.3 / 17.9 / 16.13 / 15.17 / 14.22 just two weeks later. Pigsty's approach remains the same as always — the day after new versions drop, offline packages are ready, all extensions are recompiled and verified, and documentation is updated. All you need to do is run a single command.

The total extension count also climbed to **461**.

If you prize maximum extensibility and the best stability, vanilla PostgreSQL remains the optimal default choice. Pigsty supports PG 14 through PG 18 across their active lifecycle. Worth noting: this is the last release to support PG 13; the minimum version will be raised to PG 14 going forward.

------

## pgEdge: Native Multi-Master Replication

pgEdge is the heavyweight newcomer in this release.

Traditional PostgreSQL high availability follows a primary-standby model — writes can only go to the primary node. pgEdge's core extension, Spock, breaks this constraint: every node in the cluster can handle reads and writes, with data asynchronously synchronized between nodes via logical replication, and conflicts resolved automatically through configurable strategies.

Strictly speaking, pgEdge is not an entirely new kernel but rather a multi-master solution built on standard PostgreSQL + the Spock extension. However, since some low-level multi-master capabilities require kernel patches (which have not yet been merged into the PostgreSQL mainline), it currently ships as a "patched kernel + extension" combination. This is similar to OrioleDB and Percona TDE — if the PostgreSQL mainline eventually merges these patches, they could all transition to pure extension form. That is a very promising trend to watch.

I'm quite bullish on this project. The pgEdge team includes several PostgreSQL community kernel veterans with deep technical expertise. Its open-source journey is also worth mentioning: previously it used a Confluent-style Source Available license (pgEdge Community License), which was not strictly open source. But in September 2025, it fully transitioned to the PostgreSQL License.

One nuance to be aware of, though: **the source code is under the PostgreSQL License, but the official binary packages remain under a commercial license**. Specifically, development use is free, but production use requires a paid subscription.

I built the packages directly from the PostgreSQL-licensed source code myself — creating patched PostgreSQL kernel packages and adapting them for all major operating systems that Pigsty supports. No external dependencies; just install from the Pigsty repo. No production licensing issues. Of course, if you want their cloud service and commercial support, you're welcome to go support them.

pgEdge consists of three core extensions:

- **Spock 5.0.5**: The multi-master logical replication engine; every node handles reads and writes.
- **Lolor 1.2.2**: Large object logical replication.
- **Snowflake 2.4**: Distributed sequence number generation.

For conflict resolution, pgEdge provides multiple strategies: simple "last-write-wins" (LWW), dedicated CRDT-based approaches, conflict log tables, and user-defined custom strategies. If you have globally distributed needs — say, a node each in Beijing, Frankfurt, and Virginia, with users reading and writing from the nearest one — this multi-master model is an excellent fit. It essentially brings native CockroachDB/TiDB-style multi-write capabilities into the PostgreSQL ecosystem, except the foundation is still the PostgreSQL you know and love.

To use it in Pigsty: `configure -c pgedge`.

------

## AgensGraph: Graph Database

AgensGraph positions itself as a multi-model graph database built on PostgreSQL — natively supporting both relational and property graph models within a single engine, rather than starting from scratch like Neo4j. The project is led by the Korean team at Bitnine.

Some may ask: doesn't the PostgreSQL ecosystem already have Apache AGE as a graph extension? Why bother forking the kernel?

There is an interesting backstory here: **AGE and AgensGraph were actually created by the same team**. They originally built AgensGraph as a kernel fork, which earned around 1,000+ stars. Later, they tried implementing similar functionality in extension form, creating AGE and donating it to Apache. The extension form turned out to be far more popular, garnering 4,000+ stars. AGE went through a brief maintenance hiccup last year but has since resumed updates, releasing version 1.7.0 targeting PG 17/18.

So what is the value of the fork? At least four things:

**First, native syntax.** In AGE, you execute Cypher queries through function calls (passing query strings as arguments). In AgensGraph, you write `CREATE GRAPH` directly — Cypher is first-class syntax.

**Second, storage optimization.** Its storage engine is specifically optimized for graph properties, theoretically yielding better performance (though I have not personally benchmarked it yet).

**Third, unified query optimization.** Cypher, JSON, and SQL queries are handled uniformly at the optimizer level — a very interesting native implementation approach.

**Fourth, vector compatibility.** AgensGraph recently announced pgvector compatibility, meaning you can do Graph RAG — combined graph + vector retrieval — within a single database. This is an extremely hot frontier area right now. I have not yet packaged this specific vector plugin, but may add it later.

Of course, the cost of the fork path is also obvious: keeping up with the PG mainline is extremely difficult. PG is now at 18, while AgensGraph is still based on PG 16. This is the eternal fate of forks — always one or two major versions behind.

To use it in Pigsty: `configure -c agens`.

------

## Cloudberry: MPP Data Warehouse

Cloudberry is the third new kernel in this release. It is an Apache project led by the HashData team, essentially a fork of Greenplum 7 — but with significant improvements, such as upgrading the kernel from Greenplum's PG 12 to PG 14, filling in many useful newer features.

After Cloudberry 2.0 was released, official binary packages were no longer provided — version 1.6 previously had RPMs, but now even those are gone. After waiting several months with no sign of the team addressing this, I decided to build them myself with Claude's help. The packaging process went smoothly overall, requiring only minor code changes and patches on some newer operating systems. Previously there were only RPMs; now DEBs are available too, across all 14 Linux distributions that Pigsty supports.

As for Cloudberry/Greenplum deployment scripts and monitoring, we actually had those back in Pigsty v1.4, but removed them later due to very low usage. After all, the scale needed for an MPP data warehouse is beyond most organizations. So after careful consideration, we are offering it as a Beta module on demand — the packages are built and available in the repo for direct download; full deployment playbooks will be provided in a future release as appropriate.

------

## Babelfish: SQL Server Compatibility

Having covered the three new kernels, let's talk about the three **rebuilt** kernels.

Babelfish is AWS's open-source SQL Server compatibility layer — it lets PostgreSQL understand T-SQL syntax and the TDS protocol, so your SQL Server applications can connect to PostgreSQL without changing drivers or most queries. Great project, but the build process is notoriously complex — so complex that there is an entire open-source project, WiltonDB, dedicated to just this task.

Previously, I took the easy route and used WiltonDB's packages. Honestly, their package quality always left me a bit uneasy: no support for the full Debian series or EL10, a dependency system that differs from standard PG, and the version was stuck on PG15 — while upstream Babelfish already supported PG17.

This time I bit the bullet and built it myself. With the packaging experience gained from the other kernels, this turned out to be straightforward — bundling Babelfish's four core extensions into a single package alongside a patched kernel package, ready to go. It **no longer depends on the external WiltonDB repository** and installs directly from the Pigsty repo. The version has been upgraded to **Babelfish 5.5 + PG17**.

To use it in Pigsty: `configure -c mssql`.

------

## OrioleDB: New Storage Engine

OrioleDB is the next-generation PostgreSQL storage engine project acquired by Supabase, aiming to fundamentally solve MVCC bloat — replacing the traditional dead tuple + VACUUM mechanism with an Undo Log approach.

This rebuild upgrades to **OrioleDB Beta14**, built on OriolePG 17.16. A key advancement in this version is the addition of PITR incremental backup and recovery support. It is still in Beta and not recommended for critical production workloads. But as one of the future evolution paths for PostgreSQL storage engines, it is well worth continued attention and experimentation.

To use it in Pigsty: `configure -c oriole`.

------

## OpenHalo: MySQL Wire-Protocol Compatibility

OpenHalo is the third rebuilt kernel. It provides MySQL wire-protocol compatibility — you can simultaneously use MySQL clients and PG clients to read from and write to the same database, which is a very interesting capability.

Developed by the YiJing XiHe team, they are one of the few domestic Chinese database companies that quietly does solid work and is willing to open-source the results. That is genuinely rare.

Changes in this update:

- Version upgraded from PG 14.10 to **PG 14.18**
- Version number officially updated to **1.0**, with naming adjusted to follow Pigsty's packaging conventions

Although the PG 14 baseline is a bit dated, it is a worthwhile option for MySQL migration scenarios.

To use it in Pigsty: `configure -c mysql`.

------

## The Other Six Regulars

Besides the six kernels added or rebuilt in this release, Pigsty has six long-standing "regulars":

**IvorySQL** (`pg_mode: ivory`) — Oracle PL/SQL compatible kernel by Highgo, currently based on PG 18.1.

**Percona TDE** (`pg_mode: tde`) — Transparent data encryption, meeting the hard compliance requirement of "encryption at rest." Updates trail the PG mainline slightly; future releases will catch up.

**PolarDB** (`pg_mode: polar`) — Alibaba's open-source shared-storage PG kernel, with minor version updates. Notably, this release **drops support for PolarDB-O** (the version with domestic compliance certification); the open-source edition retains only the community PG version.

**Citus** (`pg_mode: citus`) — Microsoft's distributed extension, with the official release of version 14.0.0, now supporting PG 18.

**Ferret / DocumentDB** (`pg_mode: mongo`) — MongoDB wire-protocol compatibility, letting you connect to PostgreSQL directly with MongoDB drivers.

**Supabase** self-hosted template has also been routinely updated to the latest version.

------

## One Config, Ten Kernels in Flight

After all this talk about kernels, the most fun part is actually this: we created a `demo/kernels.yml` config file — if you have 10 VMs, you can use this template to **spin up 10 different PG kernels with a single command**.

Each cluster gets its own monitoring dashboards, high availability, and backup recovery, managed just like 10 standard PostgreSQL instances. Pure showing off, but also a great reference template: if you want to mix-deploy multiple kernels within a single Pigsty installation, this shows exactly how to configure it.

This is not an architecture diagram on a slide deck. It is running code.


------

## Other Improvements

Beyond the kernel showcase, v4.2 includes several notable engineering improvements:

**Redis directory normalization**: The default directory changes from `/data` to `/data/redis`. Existing configs still using `/data` need to be updated before upgrading; deployment will block the old path.

**Configure script improvements**: Supports `-o` absolute path output with auto-created directories; region detection is now tri-state (domestic/international/offline fallback), fixing the `behind_gfw()` hang issue.

**pgBackRest initialization resilience**: `stanza-create` now retries (2 attempts, 5-second interval), mitigating lock contention with `archive-push`. If you have hit this issue, you know how annoying it is.

**Supabase stack upgrade**: PostgREST 14.5, Vector 0.53.0, and S3 access key variables are now properly included.

**Vibe template updates**: Ships `@anthropic-ai/claude-code`, `@openai/codex`, `happy-coder`, and more — AI coding sandbox out of the box.

**Infrastructure routine upgrades**: Grafana 12.4, Prometheus 3.10, VictoriaMetrics 1.136, etcd 3.6.8, Kafka 4.2, among others. Note that Grafana 12.4 changes data link merge behavior; review custom dashboards accordingly.

**Homepage redesign**: Previously hacked together with Claude Code, and people rightfully complained it was ugly. This time Codex gave it an optimization pass, and it looks much better. Will continue polishing when time permits.

------

## Looking Ahead

As an open-source project, I think Pigsty has reached a fairly mature state. The focus going forward will gradually shift to sub-projects:

**Pig CLI** has recently gained many powerful features — wrapping PostgreSQL, Patroni, PgBouncer, and pgBackRest management into a unified command-line tool, convenient for DBA Agents like Claude Code to invoke. This kind of CLI designed simultaneously for human DBAs and AI Agents is what I call an Agent-Native CLI.

**DBA Agent** work has also progressed — I have recently written some Claude Skills and prompt templates that make the Pigsty environment perceptible to AI tools. This way you can drop Claude Code into a Pigsty environment and let it work for you.

Pigsty itself will continue to follow the PG minor release cadence. The next version may officially include the Cloudberry deployment playbook, plus local SMTP server support (maddy / stalwart). No rush for big new features — the current architecture running stably is just fine.


--------

## v4.2.0 Release Note

**Highlights**

- Aligned with PostgreSQL out-of-band minor updates: 18.3, 17.9, 16.13, 15.17, 14.22.
- Total PostgreSQL extension coverage reaches 461 packages.
- Kernel updates across Babelfish, AgensGraph, pgEdge, OriolePG, OpenHalo, and Cloudberry.
- Babelfish template now uses a Pigsty-maintained PG17-compatible build, with no WiltonDB repo dependency.
- Supabase images and self-hosted templates are refreshed to the latest stack, using Pigsty-maintained [pgsty/minio](https://github.com/pgsty/minio).

**Major Changes**

- `mssql` now defaults to Babelfish PG17 (`pg_version: 17`, `pg_packages: [babelfish, pgsql-common, sqlcmd]`) and no longer requires an extra `mssql` repo.
- Kernel install paths are normalized in `pg_home_map`: `mssql -> /usr/babelfish-$v/`, `gpsql -> /usr/local/cloudberry`.
- `package_map` adds a dedicated `cloudberry` mapping and fixes `babelfish*` aliases to versioned RPM/DEB package names.
- Redis data root default changes from `/data` to `/data/redis`; deployment blocks legacy defaults, while `redis_remove` keeps backward-compatible cleanup.
- `configure` now supports absolute `-o` output paths with auto-created parent directories, tri-state region detection (CN/global/offline fallback), and a fix for `behind_gfw()` hangs.
- Debian/Ubuntu default repo URL mappings (`updates/backports/security`) and China mirror components are corrected to prevent bootstrap package failures.
- Supabase stack is updated (including PostgREST `14.5` and Vector `0.53.0`) and now includes missing S3 protocol credential variables.
- Rich/Sample templates explicitly define `dbuser_meta` defaults; `node.sh` systemd completion is simplified.
- `pgbackrest` stanza initialization now retries (2 attempts, 5-second interval) to reduce lock contention with `archive-push`.
- Vibe template now ships `@anthropic-ai/claude-code`, `@openai/codex`, and `happy-coder`, and includes `age` in the default example.

**PG Software Updates**

- PostgreSQL 18.3, 17.9, 16.13, 15.17, 14.22
- [RPM Changelog 2026-02-27](https://pigsty.io/docs/repo/pgsql/rpm/#2026-02-27)
- [DEB Changelog 2026-02-27](https://pigsty.io/docs/repo/pgsql/deb/#2026-02-27)
- Core upgrades: `timescaledb 2.25.0 -> 2.25.1`, `citus 14.0.0-3 -> 14.0.0-4`, `pg_search -> 0.21.9`
- New/rebuilt: `pgedge 17.9`, `spock 5.0.5`, `lolor 1.2.2`, `snowflake 2.4`, `babelfish 5.5.0`, `cloudberry 2.0.0`
- Kernel-side updates: `oriolepg 17.11 -> 17.16`, `orioledb beta12 -> beta14`, `openhalo 14.10 -> 1.0(14.18)`

| Package             | Old Version     | New Version | Notes                                    |
|:--------------------|:----------------|:------------|:-----------------------------------------|
| `timescaledb`       | 2.25.0          | 2.25.1      |                                          |
| `citus`             | 14.0.0-3        | 14.0.0-4    | Rebuilt from the latest official release |
| `age`               | 1.7.0           | 1.7.0       | Added PG 17 support for version 1.7.0    |
| `pgmq`              | 1.10.0          | 1.10.1      | Package currently unavailable            |
| `pg_search`         | 0.21.7 / 0.21.6 | 0.21.9      | Previous RPM/DEB versions differ         |
| `oriolepg`          | 17.11           | 17.16       | OriolePG kernel update                   |
| `orioledb`          | beta12          | beta14      | Matches OriolePG 17.16                   |
| `openhalo`          | 14.10           | 1.0         | Updated and renamed, based on 14.18      |
| `pgedge`            | -               | 17.9        | New multi-master edge-distributed kernel |
| `spock`             | -               | 5.0.5       | New core pgEdge extension                |
| `lolor`             | -               | 1.2.2       | New core pgEdge extension                |
| `snowflake`         | -               | 2.4         | New core pgEdge extension                |
| `babelfishpg`       | -               | 5.5.0       | New BabelfishPG package group            |
| `babelfish`         | -               | 5.5.0       | New Babelfish compatibility package      |
| `antlr4-runtime413` | -               | 4.13        | New runtime dependency for Babelfish     |
| `cloudberry`        | -               | 2.0.0       | RPM build only                           |
| `pg_background`     | -               | 1.8         | DEB build only                           |

**Infrastructure Software Updates**

| Name                          | Old Version      | New Version      |
|:------------------------------|:-----------------|:-----------------|
| `grafana`                     | 12.3.2           | 12.4.0           |
| `prometheus`                  | 3.9.1            | 3.10.0           |
| `mongodb_exporter`            | 0.47.2           | 0.49.0           |
| `victoria-metrics`            | 1.135.0          | 1.136.0          |
| `victoria-metrics-cluster`    | 1.135.0          | 1.136.0          |
| `vmutils`                     | 1.135.0          | 1.136.0          |
| `victoria-logs`               | 1.45.0           | 1.47.0           |
| `vlagent`                     | 1.45.0           | 1.47.0           |
| `vlogscli`                    | 1.45.0           | 1.47.0           |
| `loki`                        | 3.6.5            | 3.6.7            |
| `promtail`                    | 3.6.5            | 3.6.7            |
| `logcli`                      | 3.6.5            | 3.6.7            |
| `grafana-victorialogs-ds`     | 0.24.1           | 0.26.2           |
| `grafana-victoriametrics-ds`  | 0.21.0           | 0.23.1           |
| `grafana-infinity-ds`         | 3.7.0            | 3.7.2            |
| `redis_exporter`              | 1.80.2           | 1.81.0           |
| `etcd`                        | 3.6.7            | 3.6.8            |
| `dblab`                       | 0.34.2           | 0.34.3           |
| `tigerbeetle`                 | 0.16.72          | 0.16.74          |
| `seaweedfs`                   | 4.09             | 4.13             |
| `rustfs`                      | 1.0.0-alpha.82   | 1.0.0-alpha.83   |
| `uv`                          | 0.10.0           | 0.10.4           |
| `kafka`                       | 4.1.1            | 4.2.0            |
| `npgsqlrest`                  | 3.7.0            | 3.10.0           |
| `postgrest`                   | 14.4             | 14.5             |
| `caddy`                       | 2.10.2           | 2.11.1           |
| `rclone`                      | 1.73.0           | 1.73.1           |
| `pev2`                        | 1.20.1           | 1.20.2           |
| `genai-toolbox`               | 0.25.0           | 0.27.0           |
| `opencode`                    | 1.1.59           | 1.2.15           |
| `claude`                      | 2.1.37           | 2.1.59           |
| `codex`                       | 0.104.0          | 0.105.0          |
| `code`                        | 1.109.2          | 1.109.4          |
| `code-server`                 | 4.108.2          | 4.109.2          |
| `nodejs`                      | 24.13.1          | 24.14.0          |
| `pig`                         | 1.1.2            | 1.3.0            |
| `stalwart`                    | -                | 0.15.5           |
| `maddy`                       | -                | 0.8.2            |

**API Changes**

- `pg_mode` now includes `agens` and `pgedge`.
- `mssql` defaults are updated to `pg_version: 17` and `pg_packages: [babelfish, pgsql-common, sqlcmd]`.
- Kernel/package alias mappings are updated in `pg_home_map` and `package_map` (Babelfish, OpenHalo, IvorySQL, Cloudberry, pgEdge family).
- `redis_fs_main` now defaults to `/data/redis`, with deployment guardrails and backward-compatible cleanup behavior.
- `configure` output path handling and region detection logic are updated, with offline fallback warnings and unified SSH probe timeouts.
- `grafana.ini.j2` is updated for Grafana 12.4 config changes and deprecations.

**Compatibility Notes**

- If existing Redis configs still use `redis_fs_main: /data`, migrate to `/data/redis` before deployment.
- Grafana 12.4 changes data link merge behavior. This release moves key links into field overrides; review custom dashboards accordingly.

**26 commits**, 122 files changed, +2,116 / -2,215 lines (`v4.1.0..v4.2.0`, 2026-02-15 ~ 2026-02-28)

**Checksums**

```bash
24a90427a7e7351ca1a43a7d53289970  pigsty-v4.2.0.tgz
d980edf5eeb0419d4f1aa7feb0100e14  pigsty-pkg-v4.2.0.d12.aarch64.tgz
24bc237d841457fbdcc899e1d0a3f87e  pigsty-pkg-v4.2.0.d12.x86_64.tgz
e395b38685e2ecbe9c3a2850876d9b7b  pigsty-pkg-v4.2.0.d13.aarch64.tgz
c5c8776f9bead9f29528b26058801f83  pigsty-pkg-v4.2.0.d13.x86_64.tgz
28ea40434bd06135fc8adc0df1c8407d  pigsty-pkg-v4.2.0.el10.aarch64.tgz
58ad715ac20dc1717d1687daecfcf625  pigsty-pkg-v4.2.0.el10.x86_64.tgz
008f955439ea311581dd0ebcf5b8bd34  pigsty-pkg-v4.2.0.el8.aarch64.tgz
2acfd127a517b09f07540f808fe9547a  pigsty-pkg-v4.2.0.el8.x86_64.tgz
58e62a92f35291a40e3f05839a1b6bc4  pigsty-pkg-v4.2.0.el9.aarch64.tgz
d311bfdf5d5f60df5fe6cb3d4ced4f9c  pigsty-pkg-v4.2.0.el9.x86_64.tgz
c98972fe9226657ac1faa7b72a22498b  pigsty-pkg-v4.2.0.u22.aarch64.tgz
44a174ee9ba030ac1ea386cf0b85f6e7  pigsty-pkg-v4.2.0.u22.x86_64.tgz
143e404f4681c7d0bbd78ef7982cd652  pigsty-pkg-v4.2.0.u24.aarch64.tgz
00dfa86f477f3adff984906211ab3190  pigsty-pkg-v4.2.0.u24.x86_64.tgz
```




## v4.2.1

A maintenance release that adds 3 new extensions.

**Major Changes**

- **New Extensions**: `pg_eviltransform` is added to the GIS package group, `pg_pinyin` to the FTS group, and `pg_qos` to the admin group — all for PG 14–18.
- **PG13 Removed**: All `pgdg13`, `pgdg13-nonfree` repo entries and PG13 package aliases (`pg13-*`) are removed from every platform variant (EL7/8/9/10, Debian 12/13, Ubuntu 22/24, both x86_64 and aarch64).
- Config templates (`fat.yml`, `pro.yml`, `dev.yml`, `el.yml`, `debian.yml`) no longer reference PG13 packages or repos. Extension version comments are updated to reflect PG 14–18 coverage only.
- **Percona Repo**: Origin URL updated from `ppg-18.1` to `ppg-18.3` to track the latest Percona PostgreSQL distribution.
- **Nginx Repo**: Module tag for the Nginx upstream APT repo corrected from `infra` to `nginx` on Debian/Ubuntu platforms.
- **UV Venv Fix**: `roles/node/tasks/pkg.yml` now checks for an existing virtualenv before running `uv venv`, preventing redundant re-creation and potential errors on re-provisioning.
- **Docker Image**: `less` is added to the Pigsty Docker image base packages.
- **Demo Config**: Default firewall rules in `el.yml` and `debian.yml` demo configs now include port `5432` for direct PostgreSQL access.

**Compatibility Notes**

PostgreSQL 13 reached its [end of life](https://www.postgresql.org/support/versioning/) on 2025-11-13.
The PGDG YUM repository has archived and removed the [pg13](https://yum.postgresql.org/news/pg13-end-of-life/) / [pg12](https://yum.postgresql.org/news/pg12-end-of-life/) directories.
If you install Pigsty on EL systems (even without using PG 13), repo access failures may cause installation or update errors.

You can either upgrade directly to Pigsty v4.2.1, or manually edit the `repo_upstream_default` variable in your corresponding OS file under `roles/node_id/vars/` and remove the pg13 repo line.

Additionally, EL8 remains in the Pigsty compatible OS list, but starting from this release, offline packages for EL8 will no longer be published.

No other breaking API or configuration changes in this release.

**7 commits**, 84 files changed, +4,925 / -5,351 lines (`v4.2.0..v4.2.1`, 2026-03-04 ~ 2026-03-06)

**PostgreSQL Package Updates**

| Package          | Old Version | New Version | Notes                                   |
|:-----------------|:------------|:------------|:----------------------------------------|
| timescaledb      | 2.25.1      | 2.25.2      |                                         |
| vchord           | 1.1.0       | 1.1.1       | Added clang build dependency, bug fixes |
| vchord_bm25      | 0.3.0-1     | 0.3.0-2     | Fix the CI version injection issue      |
| aggs_for_vecs    | 1.4.0       | 1.4.1       |                                         |
| pg_search        | 0.21.9      | 0.21.12     |                                         |
| pg_pinyin        | -           | 0.0.2       | New extension                           |
| pg_eviltransform | -           | 0.0.2       | New extension                           |
| pg_qos           | -           | 1.0.0       | New extension, QoS resource governance  |

**Infrastructure Package Updates**

| Name                         | Old Version    | New Version    | Notes |
|:-----------------------------|:---------------|:---------------|:------|
| `asciinema`                  | 3.1.0          | 3.2.0          |       |
| `grafana-infinity-ds`        | 3.7.2          | 3.7.3          |       |
| `victoria-metrics`           | 1.136.0        | 1.137.0        |       |
| `victoria-metrics-cluster`   | 1.136.0        | 1.137.0        |       |
| `vmutils`                    | 1.136.0        | 1.137.0        |       |
| `hugo`                       | 0.155.3        | 0.157.0        |       |
| `opencode`                   | 1.2.15         | 1.2.17         |       |
| `rustfs`                     | 1.0.0-alpha.83 | 1.0.0-alpha.85 |       |
| `seaweedfs`                  | 4.13           | 4.15           |       |
| `tigerbeetle`                | 0.16.74        | 0.16.75        |       |
| `uv`                         | 0.10.4         | 0.10.8         |       |
| `codex`                      | 0.105.0        | 0.110.0        |       |
| `claude`                     | 2.1.59         | 2.1.68         |       |
| `xray`                       | -              | 26.2.6         | New   |
| `gost`                       | -              | 2.12.0         | New   |
| `sabiql`                     | -              | 1.6.2          | New   |
| `agentsview`                 | -              | 0.10.0         | New   |

**Checksums**

```bash
262b7671424a38b208872582fe835ef8  pigsty-v4.2.1.tgz
62edcca1d1e572a247be018e1c26eda8  pigsty-pkg-v4.2.1.d12.aarch64.tgz
1d55367e2fd9106e6f18b7ee112be736  pigsty-pkg-v4.2.1.d12.x86_64.tgz
f122b1e5ba8a7ae8e3dc6e6dd53eba65  pigsty-pkg-v4.2.1.d13.aarch64.tgz
617a76bfc8df8766e78abf24339152eb  pigsty-pkg-v4.2.1.d13.x86_64.tgz
908509b350403ad1a4a27a88795fee06  pigsty-pkg-v4.2.1.el10.aarch64.tgz
70cb4afd90ed7aea6ab43a264f8eb4a8  pigsty-pkg-v4.2.1.el10.x86_64.tgz
98fbd67334f5c674b12e6af81ef76923  pigsty-pkg-v4.2.1.el9.aarch64.tgz
687fa741ccd9dcf611a2aa964bcf1de8  pigsty-pkg-v4.2.1.el9.x86_64.tgz
a2a30f4b1146b3e79be91d5be57615b6  pigsty-pkg-v4.2.1.u22.aarch64.tgz
7a1f571bd8526106775c175ba728eee1  pigsty-pkg-v4.2.1.u22.x86_64.tgz
a5574071bac1955798265f71ad73c3d4  pigsty-pkg-v4.2.1.u24.aarch64.tgz
59a7632c650a3c034f1fe6cd589d7ab5  pigsty-pkg-v4.2.1.u24.x86_64.tgz
```

