---
title: "Pigsty v4.4: From Integration to Distribution"
linkTitle: "Pigsty v4.4: From Integration to Distribution"
date: 2026-07-11
authors: [vonng]
summary: >
  Pigsty v4.4 adds Immich and JumpServer application templates, improves the Supabase and VIP experience, and begins standardizing the packages and filesystem layouts used to distribute PostgreSQL forks such as PolarDB and IvorySQL.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.4.0) | [**Release Note**](https://pigsty.io/docs/about/release/#v440)

Pigsty v4.4 is officially out. On the surface, this is a routine maintenance release: PostgreSQL 18.4, 531 extensions, a PostgreSQL 19 beta, and 14 validated offline installation artifacts. The changes really worth discussing, however, are concentrated in the software repository and command-line tooling.

Pig 1.5 completes a redesign of the command line for day-to-day PostgreSQL operations. Cloning a database, forking an instance, performing point-in-time recovery—actions once scattered across Ansible, shell scripts, Patroni, and pgBackRest—now share one consistent CLI.

At the same time, we reorganized the PostgreSQL kernel forks in the repository: adding Babelfish PG 18, filling out pgEdge PG 15–18, AgensGraph PG 17, and OrioleDB PG 16–18, and providing our own packages for PolarDB and IvorySQL.

This release also updates the self-hosted Supabase template to the latest upstream versions and resolves a batch of compatibility issues. It adds one-click deployment templates for Immich, a self-hosted photo library; JumpServer, a bastion host; and Maybe, a personal finance manager.

------

## Pig 1.5: One Interface for Operations

`pig` began as a PostgreSQL extension package manager, then gradually took on Pigsty installation, software repository, and PostgreSQL management duties. By version 1.5, it is no longer merely a tool that "can run lots of commands." It is becoming a coherent interface for operating PostgreSQL.

| Command    | Boundary                    | Typical Uses                                                                  |
|:-----------|:----------------------------|:------------------------------------------------------------------------------|
| `pig pg`   | Local PostgreSQL primitives | Start/stop, status, connect, maintenance, database cloning, local PGDATA forks |
| `pig pt`   | Patroni cluster operations  | Restart, rebuild replicas, switchover, failover, configuration, and logs       |
| `pig pb`   | Low-level pgBackRest primitives | Backups, repositories, backup sets, cleanup, and low-level restore          |
| `pig pitr` | Recovery orchestration      | Coordinate Patroni, PostgreSQL, and pgBackRest to perform PITR                  |

The most important change in this round is not the number of commands, but the **separation of responsibilities**. In the past, these operations depended largely on DBAs remembering SOPs and command aliases: which tool to call, what to do next, and what side effects to expect. That operational knowledge is now encoded directly in the commands, with high-risk operations consistently proceeding through the same chain:

> `state → plan → precheck → execute → verify → result → next_actions`

Results and help at every stage can be emitted as human-readable text or as JSON/YAML for machines and agents. Through this Agent-Native interface, DBAs, scripts, and agents can all use the same entry point and receive the context, risk assessment, and suggested next steps they need.

Enough abstraction. Let's look at a few concrete examples.

------

### Clone: Branch a Single Database

The new `pig pg clone` command can clone a single database quickly.

```bash
pig pg clone meta meta_dev --plan   # Preview the plan
pig pg clone meta meta_dev -y       # Create the database copy
```

There is an often-overlooked boundary here: `CREATE DATABASE ... TEMPLATE` terminates existing sessions on the source database. In other words, database cloning is fast, but it is not impact-free. The point of `--plan` is to lay out those side effects before you take action.

These cheap branches are extremely useful for development and testing, data analysis, model experiments, and counterfactual reasoning by agents. Production stays untouched while experiments run against the copy. If you break it, delete it and create another branch. For details, see [Instantly Clone a PostgreSQL Database—No Black Magic Required](/en/pg/pg-pig-clone/).

------

### Fork: Sandbox an Entire Instance

Database cloning creates a copy of one database. `pig pg fork` works at the level of an entire PostgreSQL instance: a physical, PGDATA-level fork.

```bash
pig pg fork init dev --start        # Fork to /pg/data-dev and start it
pig pg fork list                    # List local forked instances
pig pg fork stop dev                # Stop a forked instance
```

Pig writes metadata for managed forks and provides `list`, `start`, `stop`, and `rm` lifecycle commands. On CoW-capable XFS, a new fork initially consumes virtually no additional space; only newly written or modified blocks use capacity afterward. Pig also assigns a free port automatically, allowing the forked instance to run alongside the original.

This is especially useful in two situations: preserving a low-cost local branch before a large-scale operation that is difficult to roll back, and starting an out-of-band instance during incident recovery to verify a PITR target and inspect data quickly.

------

### Go Back in Time: Recovery Starts with a Plan

The most dangerous part of database recovery has never been the absence of one command. It is the number of steps, the blurry boundaries, and the ease of making mistakes under incident pressure.

Pig 1.5 draws a clear line between low-level recovery and high-level orchestration:

- `pig pb restore` is the low-level pgBackRest recovery primitive, responsible only for files and the recovery target.
- `pig pitr` is the recovery orchestrator for Pigsty/Patroni environments, coordinating Patroni, PostgreSQL, and pgBackRest.

```bash
pig pitr -t "2026-07-10 12:00:00+08" --plan
pig pitr -t "2026-07-10 12:00:00+08" -y
```

Recovery commands must now specify an explicit target: the latest state, a backup consistency point, a timestamp, an LSN, a transaction ID, or a named restore point. Omitting the target can no longer be interpreted as some dangerous default. Structured output no longer counts as confirmation either; automation that performs destructive operations must explicitly pass `-y/--yes`.

For managed data directories, `pig pitr` checks the environment, stops Patroni and PostgreSQL, runs the pgBackRest restore, starts PostgreSQL according to policy, verifies the recovered state, and finally reports follow-up actions. A human operator or higher-level automation then validates the data, returns the instance to Patroni control, and switches traffic.

The point is not "one-click recovery." It is to codify the SOP most likely to go wrong during an incident: review the plan, execute it, then verify the result.

------

## PostgreSQL 18.4, 19 Beta, and 531 Extensions

The operational interface is the through line of this release, but the distribution's foundation has not stood still.

Pigsty v4.4 makes **PostgreSQL 18.4** the production default and adds a minimal **PostgreSQL 19 beta** template for evaluation. PG 19 beta1 is not production-ready, and pgBackRest 2.58 as shipped with v4.4 cannot recognize its control-file format, so this template is strictly for experimentation and evaluation.

Pigsty's PostgreSQL extension catalog grows from **510** in v4.3 to **531**. By category, `pg_ducklake` brings DuckDB, Parquet, and lakehouse capabilities into PostgreSQL; `pg_stat_plans` and `pg_stat_backtrace` improve observability for query plans and process call stacks; and the upgraded `pgmnemo` and newly added `psql_bm25s` target agent memory and BM25 full-text search, respectively.

Meanwhile, OrioleDB expands to PG 16–18 and now defaults to PG 18; pgEdge covers PG 15–18; Babelfish covers PG 17–18; IvorySQL enters the 5.x line; AgensGraph moves to PG 17; and Cloudberry and PolarDB both receive reorganized paths and packages.

These details may look miscellaneous, but this is the work of a distribution: keeping the PostgreSQL mainline, extension ecosystem, and kernel forks simultaneously usable, installable, and upgradeable.

------

## Application Updates: Immich, JumpServer, Maybe, and Supabase

This release adds templates for [Immich](https://pigsty.io/docs/app/immich/), [JumpServer](https://pigsty.io/docs/app/jumpserver/), and Maybe, and updates Supabase.

### Immich: Put Your Photo Library on Real PostgreSQL

Immich is an open-source, self-hosted photo and video management service—think Google Photos or iCloud Photos in your own home. It provides automatic mobile backup, albums, maps, face recognition, and semantic search. Its backend uses PostgreSQL, vector search, caching, and machine-learning services. Smart search and face recognition require VectorChord's `vchord` extension, which Pigsty provides directly.

Immich still stores original photos in a filesystem directory and does not support object storage directly. If you want to separate the storage pool, JuiceFS can mount MinIO or S3 as a local filesystem.

### JumpServer: Bring the Bastion Host into the Stack

Bastion hosts are a hard requirement for many enterprises, and JumpServer is one of the common open-source choices. JumpServer 4.x stores its core metadata in PostgreSQL, so Pigsty now provides a matching deployment template.

Maybe also joins the application catalog in this release. It is a personal finance and asset management tool. The three templates serve different purposes, but they share the same principle: applications can run in containers without letting their data drift along with the containers.

### Supabase: Updating Means More Than Swapping Images

Supabase moves quickly. It also has the most components—and the most opportunities for compatibility problems—of any Pigsty application template. v4.4 brings Studio, Auth, PostgREST, Realtime, Storage, Analytics, Edge Runtime, and the rest of the stack up to their July 2026 upstream versions, along with a coordinated round of adjustments.

Analytics now lives in a dedicated `_supabase` database and `_analytics` schema, keeping log-analysis tables separate from application objects. We added a `pg_stat_statements` compatibility view for Studio so its query-performance page works correctly. We also adapted the stack for the new Publishable Key and Secret Key, and adjusted Kong routes, sensitive Realtime endpoints, S3-compatible APIs, and service health checks.

With an application like Supabase, getting one container to start means nothing. The job is done only when more than a dozen components can be upgraded together and still work together. v4.4 fixes exactly these unglamorous issues that determine whether the template is actually usable.

------

## No More Manually Entering the VIP Interface

Another change I particularly like is automatic VIP interface detection.

Previously, `vip_interface` and `pg_vip_interface` defaulted to `eth0`. Enabling a NODE/PG VIP required users to configure the interface name manually, which was tedious.

v4.4 adds automatic detection and changes the defaults to `auto`: Pigsty takes each node IP from the inventory, resolves the actual network interface that owns it, and passes that result to Keepalived or VIP Manager. Explicit configuration is still supported, but most users no longer need to log in, run `ip addr`, and come back to fill in a parameter. This feature is only a few lines of configuration, yet it directly prevents an entire class of deployment failures. The experience of a distribution is often defined by small details like this.

------

## Backups Now Default to Zstandard

pgBackRest previously used LZ4 compression by default. LZ4 is fast and offers high throughput, and it remains a good fit for `wal_compression`. Backup repositories, however, care more about compression ratio, so v4.4 changes pgBackRest's default algorithm to Zstandard. In testing, a small increase in decompression overhead improved the compression ratio from 2.x to 3.x and saved roughly another third of the backup space. That is an excellent trade.

The switch also exposed a problem: the official IvorySQL kernel was not built with options such as `--with-lz4` and `--with-zstd`, so it could use neither LZ4 nor Zstandard. That led directly to the next change: standardizing how PostgreSQL kernel forks are built.

------

## Standardizing PostgreSQL Kernel Fork Builds

Pigsty supports many flavors of the PostgreSQL kernel. PolarDB and IvorySQL previously used packages built upstream. IvorySQL's official build omitted several important compile-time options, while PolarDB had no Ubuntu 26.04 packages. I reported both issues upstream. Ubuntu 26.04 build support has now been merged in [PolarDB #650](https://github.com/polardb/PolarDB-for-PostgreSQL/issues/650), and [IvorySQL #1377](https://github.com/IvorySQL/IvorySQL/issues/1377) confirms that the missing options will be added in the next release. The upstream binary packages, however, will take another release cycle.

I was not going to wait that long. Since I already build so many kernel forks myself, two more will not hurt—and this is a good opportunity to standardize the FHS layout once and for all. Take PolarDB: the upstream package is named `polardb-for-postgresql` and installs to `/u01/polardb_pg_17`; Pigsty's package is named `polardb-17` and installs to `/usr/polar-17`. The default port, runtime search paths, development headers, and extension build tooling are standardized along with it.

To make PolarDB builds reproducible, we also split its PFSD development library into a separate `polarstore` package. The open-source edition also removes the PolarDB Oracle-compatibility kernel and its dedicated monitoring configuration; this closed-source compatibility path is no longer listed as built-in support.

This work also prepares for the next step. Pigsty's 500-plus extensions currently target mainly vanilla PostgreSQL. Next, I want to extend the build matrix—"5 vanilla PG major versions × 16 Linux platforms, including online-only EL8 on both architectures"—to more than a dozen PostgreSQL kernel forks, giving them access to the complete PostgreSQL extension ecosystem instead of leaving each one to bundle a handful of extensions piecemeal in RPMs or Docker images. That is what a Meta Distribution should look like.

------

## Closing Notes and What's Next

Most of the work involved in building a distribution does not make for a pretty demo: rename packages, straighten out directories, add dependencies, fix build scripts, then run all 14 deployment tests. But if nobody does that work, "out of the box" is just advertising copy.

**Bring upstream diversity under one set of engineering conventions, and leave the last-mile headaches to the distribution.** That is Pigsty v4.4.

With Pigsty 4.4 complete, we have already begun preparing version 5.0. There may be a transitional 4.5 release before 5.0.

Version 5.0 will ship alongside full support for PG 19 this September. PG 19 introduces many powerful features, and Pigsty 5.0 will make targeted adjustments to take full advantage of them. Some of the groundwork is already done. For example, this release updates pg_exporter to 1.3.0, adding support for new PG 19 monitoring metrics; Patroni parameter templates have also reserved the necessary positions and placeholder values for PG 19 changes.

Pigsty 5.0 will have a dedicated enterprise software artifact repository with a different policy from the open-source edition: more conservative updates, retention of every historical package version, debug packages and hotfix packages, plus regular snapshots. To make that possible, we built a repository management tool that unifies repository operations across APT and DNF. We call it sow—a female pig—a natural counterpart to Pig, the package manager and resident piglet.

We are also trying a few interesting things. One is rewriting Patroni in Go; for the first phase, at least, we have rewritten Patroni's client tool to provide a better management experience. We call this project Boar—as in a male pig. Together with sow and Pig, it completes the family, right at home in Pigsty.

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.4.0) | [**Release Note**](https://pigsty.io/docs/about/release/#v440)

------

## v4.4.0 Release Notes

Pigsty v4.4.0 is a maintenance release focused on PostgreSQL 18.4, preview support for PostgreSQL 19 beta, 531 extensions, kernel variant updates, and broader platform coverage.

Released on **2026-07-10**. See the [GitHub release](https://github.com/pgsty/pigsty/releases/tag/v4.4.0) and the [complete changes since v4.3.0](https://github.com/pgsty/pigsty/compare/v4.3.0...v4.4.0).

**Highlights**

- **PostgreSQL 18.4 / 19 beta**: PostgreSQL 18.4 is now the production default, with a minimal PostgreSQL 19 beta template available for evaluation.
- **531 extensions and kernel updates**: The extension catalog adds 21 extensions, with major PostgreSQL kernel variants updated across the supported platform matrix.
- **Pig 1.5.1 and safer operations**: New clone, fork, and PITR workflows, plus automatic VIP interface discovery, pgBackRest Zstandard compression, and dedicated Patroni log collection.
- **Security, applications, and tooling**: Hardened handling of sensitive configuration and repository security automation, new application templates, a redesigned infrastructure portal, and optional Codex support.
- **Platform validation**: All 14 offline deployment tests across seven operating-system baselines on `x86_64` and `aarch64` passed.
- **Offline artifacts**: The Community Edition publishes six dual-architecture offline bundles on GitHub for Debian 13, EL 10, and Ubuntu 24.04; prebuilt bundles for the other validated baselines are available through the Professional Edition.

**Compatibility Changes**

- Newly generated pgBackRest configurations now use `compress-type=zst`; preserve any intentional local customizations before rendering them again. [#744](https://github.com/pgsty/pigsty/issues/744)
- Patroni logs now use `/pg/log/patroni` and `job=patroni`; custom log queries and alerting rules that use the old syslog selector must be updated accordingly.
- VIP interface defaults have changed to `auto`, dnsmasq records have moved to `/etc/dnsmasq.d/pigsty`, and Pigsty now manages `/etc/default/haproxy`; nonstandard network environments should preserve explicit overrides.
- The default etcd backend quota has been reduced from 16 GiB to 8 GiB; check current backend usage before applying the new configuration.
- `pig` automation scripts must pass `-y/--yes` when running destructive commands; both `pig pb restore` and `pig pitr` require exactly one explicit recovery target. See the [`pig` v1.5](https://pigsty.io/docs/pig/release/#v150) release notes.
- Supabase Analytics now uses the `_supabase` database and `_analytics` schema; create these objects before switching an existing deployment to the new stack.

**Security and Operations**

- The `pg-pitr` wrapper adds safer recovery-target selection, timeline and dry-run support, and stronger checks for unsafe recovery targets.
- Ansible output no longer exposes sensitive application configuration, generated `.env` files are set to mode `0600`, and Grafana no longer prints the administrator password.
- The `dbsu` sudo policy adds controlled log-viewing permissions; the repository also adds a security policy, CodeQL, Dependabot, pinned GitHub Actions dependencies, and release-signing automation.

**Applications and Tooling**

- Added Immich, Maybe, and JumpServer templates, and updated Supabase, Dify, InsForge, Registry, Jupyter, Kong, Odoo, Teable, Mattermost, and related startup scripts.
- Redesigned the bilingual Chinese/English infrastructure portal; the experimental VIBE module can install Codex CLI on demand, while Claude Code remains its default managed coding agent.
- Removed the legacy FerretDB Compose template; the FERRET module remains available.

**Bug Fixes**

- Fixed EL10 PostgreSQL/libpq package-provider conflicts, EPEL path handling, and PGDG minor-version repository rules. [#752](https://github.com/pgsty/pigsty/issues/752)
- `bootstrap` now reuses an existing `/www` directory, and Redis Sentinel HA password rendering has been fixed. [#753](https://github.com/pgsty/pigsty/issues/753) [#748](https://github.com/pgsty/pigsty/issues/748)
- Corrected RPM package names and package groups for `pg_http`, `pg_gzip`, `apache-age`, and `odbc_fdw`. [#750](https://github.com/pgsty/pigsty/issues/750)
- Prevented services from starting unexpectedly during package installation on Debian and Ubuntu, and improved EL9 aarch64 Patroni package handling.
- Fixed VirtualBox private-network routing and default-interface selection.
- Fixed shell compatibility and Vector log-lifecycle issues, along with PG 19 `io_workers`, Teable HBA, and several application runtime defaults.

**PostgreSQL and Extension Package Changes**

This release adds 21 extensions, refreshes the PostgreSQL 18.4 package set, introduces a PostgreSQL 19 beta template, and updates the major kernel variants. The versions below follow the final repository metadata; versions included in offline bundles were also cross-checked against the v4.4.0 artifacts. PostgreSQL major-version ranges indicate coverage in the extension catalog and software repositories.

[PostgreSQL RPM Changes](https://pigsty.io/docs/repo/pgsql/rpm/) · [PostgreSQL DEB Changes](https://pigsty.io/docs/repo/pgsql/deb/) · [Infrastructure Package Changes](https://pigsty.io/docs/repo/infra/log/)

| Package                 | Old Version     | New Version                      | Notes                                                   |
|-------------------------|-----------------|----------------------------------|---------------------------------------------------------|
| `polardb-17`            | `17.9.1.0`      | `17.10.1.0`                      | PG 17; new RPM package                                  |
| `agensgraph-17`         | `2.16.0`        | `2.17.0`                         | PG 17.10                                                |
| `openhalodb-14`         | `1.0-beta`      | `1.0-2`                          | OpenHaloDB                                              |
| `babelfish-17`          | `5.4.0`         | `5.4.0`                          | PG 17.7; rebuilt                                        |
| `babelfish-18`          | -               | `6.0.0`                          | PG 18.3                                                 |
| `pgedge`                | `17.9 / 18.3`   | `15.18 / 16.14 / 17.10 / 18.4`  | Added PG 15/16; updated PG 17/18; Spock 5.0.10          |
| `ivorysql-18`           | `5.0`           | `5.4`                            | PG 18; new RPM package                                  |
| `cloudberry`            | `2.1.0-1`       | `2.1.0-2 / 2.1.0-3`              | DEB/RPM rebuild; RPM path is `/usr/cloudberry`           |
| `cloudberry-backup`     | `2.1.0-1`       | `2.1.0-2 / 2.1.0-3`              | Backup subpackage                                       |
| `cloudberry-pxf`        | `2.1.0-1`       | `2.1.0-2 / 2.1.0-3`              | PXF subpackage                                          |
| `pg_ducklake`           | -               | `1.0.0`                          | PG 14-18                                                |
| `psql_bm25s`            | -               | `0.4.13`                         | BM25 search; PG 17-18                                   |
| `mongo_fdw`             | `5.5.3`         | `5.5.3`                          | New DEB package; PGDG RPM already available; PG 14-18   |
| `multicorn`             | `3.2`           | `3.2`                            | New DEB package; PGDG RPM already available; PG 14-18   |
| `pg_orca`               | -               | `1.0.0`                          | PG 18 only                                              |
| `pg_sorted_heap`        | -               | `0.14.0`                         | PG 16-18                                                |
| `pg_stl`                | -               | `1.0.0`                          | PG 16-18                                                |
| `fsm_core`              | -               | `1.1.0`                          | PG 15-18                                                |
| `pg_projection`         | -               | `1.0.0`                          | PG 14-18                                                |
| `graph`                 | -               | `0.1.7`                          | PG 14-18                                                |
| `jsonschema`            | -               | `0.1.9`                          | PG 14-18                                                |
| `pg_durable`            | -               | `0.2.2`                          | PG 14-18                                                |
| `pg_stat_log`           | -               | `0.1`                            | PG 18 only                                              |
| `pg_stat_plans`         | -               | `2.1.0`                          | PG 16-18                                                |
| `pg_task`               | `1.0.0`         | `2.1.29`                         | PG 14-18; fixes pcre2grep dependency                    |
| `pg_stat_backtrace`     | -               | `1.0.0`                          | PG 14-18; depends on libunwind                          |
| `pg_mockable`           | -               | `1.1.0`                          | PG 14-18                                                |
| `db2fce`                | -               | `0.0.17`                         | PG 14-18                                                |
| `pg_uuid_v8`            | -               | `1.0.0`                          | PG 14-18                                                |
| `pg_extra_time`         | `2.0.0`         | `2.1.0`                          | PG 14-18                                                |
| `pg_pinyin`             | `0.0.2`         | `0.0.4`                          | PG 14-18                                                |
| `passwordpolicy`        | -               | `2.0.5`                          | PG 14-18                                                |
| `pgdisablelogerror`     | -               | `1.0`                            | PG 14-18                                                |
| `plpgsql_wrap`          | -               | `1.0`                            | PG 14-18                                                |
| `timescaledb`           | `2.26.4`        | `2.28.2`                         | PG 15-18                                                |
| `documentdb`            | `0.110`         | `0.113`                          | PG 15-18                                                |
| `citus`                 | `14.0.0-4`      | `14.1.0`                         | PG 16-18                                                |
| `pgvector`              | `0.8.2`         | `0.8.4`                          | PG 14-18                                                |
| `orioledb`              | `1.7-beta15`    | `1.8-beta16`                     | Built for PG 16/17/18                                   |
| `pg_search`             | `0.23.1`        | `0.24.0`                         | PG 15-18                                                |
| `pg_textsearch`         | `1.1.0`         | `1.2.0`                          | BM25 full-text search; PG 17-18                         |
| `storage_engine`        | `1.3.4`         | `2.4.0`                          | Updated to PGXN 2.x; PG 15-18                           |
| `pg_clickhouse`         | `0.2.0`         | `0.3.2`                          | PGXN version update; ClickHouse integration             |
| `provsql`               | `1.2.3`         | `1.10.0`                         | PGXN version update; PG 14-18                           |
| `pgclone`               | `4.0.0`         | `4.3.2`                          | PGXN version update; PG 14-18                           |
| `biscuit`               | `2.2.2`         | `2.4.0` DEB / `2.4.1` RPM        | PG 16-18                                                |
| `pgmnemo`               | `0.7.2`         | `0.12.1`                         | PG 14-18                                                |
| `rdf_fdw`               | `2.5.0`         | `2.6.0`                          | PG 14-18; libcurl compatibility patch                   |
| `roaringbitmap`         | `1.1.0`         | `1.2.0-2`                        | PG 14-18; fixes llvm-lto packaging                      |
| `plpgsql_check`         | `2.9.0`         | `2.9.2`                          | PG 14-18                                                |
| `timescaledb_toolkit`   | `1.22.0`        | `1.23.0`                         | PG 15-18; pgrx 0.18.1                                  |
| `wrappers`              | `0.6.0`         | `0.6.1`                          | PG 14-18; pgrx 0.18.1                                  |
| `pgrdf`                 | `0.5.0`         | `0.6.4`                          | PG 14-17; pgrx 0.18.1                                  |
| `pg_graphql`            | `1.5.12`        | `1.6.1`                          | PG 14-18; pgrx 0.18.1                                  |
| `pg_anon`               | `3.0.13`        | `3.1.1`                          | PG 14-18; pgrx 0.18.1                                  |
| `pg_kazsearch`          | `2.0.0`         | `2.2.0`                          | PG 16-18; pgrx 0.18.1                                  |
| `pg_session_jwt`        | `0.4.0`         | `0.5.0`                          | PG 14-18; pgrx 0.18.1                                  |
| `pg_tzf`                | `0.2.4`         | `0.3.0`                          | PG 14-18; pgrx 0.18.1                                  |
| `pg_vectorize`          | `0.26.1`        | `0.26.2`                         | PG 14-18; pgrx 0.18.1                                  |
| `pglinter`              | `1.1.2`         | `2.0.0`                          | PG 14-18; pgrx 0.18.1                                  |
| `pgmqtt`                | `0.1.0`         | `0.3.0`                          | PG 14-18; pgrx 0.18.1                                  |
| `etcd_fdw`              | `0.0.0`         | `0.0.1`                          | PG 14-18; pgrx 0.18.1                                  |
| `pg_http`               | `1.7.0`         | `1.7.1`                          | PG 14-18; RPM renamed to `pgsql_http_$v`                 |
| `pg_gzip`               | `1.0.0`         | `1.1.0`                          | PG 14-18; RPM renamed to `pgsql_gzip_$v`                 |
| `age`                   | `1.7.0`         | `1.7.0`                          | PG 17-18; RPM renamed to `age_$v`                        |
| `pg_trickle`            | `0.40.0`        | `0.81.0`                         | PG 18 only                                              |
| `re2`                   | `0.1.1`         | `0.4.0`                          | PG 16-18                                                |
| `pg_background`         | `1.9.2`         | `2.0.2` DEB / `2.0` RPM          | PG 14-18                                                |
| `firebird_fdw`          | `1.4.1`         | `1.4.2`                          | PG 14-18                                                |
| `pg_net`                | `0.20.2`        | `0.20.3`                         | DEB and EL10 RPM updated; EL8/9 RPM stays at `0.9.2`     |
| `pg_dirtyread`          | `2.7`           | `2.8`                            | PG 14-18                                                |
| `pg_stat_ch`            | `0.3.6`         | `0.3.6`                          | PG 16-18; rebuilt                                       |
| `pggraph`               | `0.1.5`         | `0.1.7`                          | PG 14-18                                                |
| `pgsql_tweaks`          | `1.0.2`         | `1.0.5`                          | PG 14-18; PGDG RPM also contains `1.0.3`                 |
| `pgfincore`             | `1.3.1`         | `1.4.0`                          | PG 14-18                                                |
| `toastinfo`             | `1.5`           | `1.7`                            | PG 14-18                                                |
| `pg_ivm`                | `1.14`          | `1.15` DEB / `1.14` RPM          | PG 14-18                                                |
| `timeseries`            | `0.2.0`         | `0.2.1`                          | PG 14-18                                                |

**Infrastructure Package Changes**

| Package                        | Old Version        | New Version        | Notes                                    |
|--------------------------------|--------------------|--------------------|------------------------------------------|
| `pig`                          | `1.4.1`            | `1.5.1`            |                                          |
| `pg_exporter`                  | `1.2.2`            | `1.3.0`            |                                          |
| `pgschema`                     | `1.9.0`            | `1.12.0`           |                                          |
| `pgstream`                     | `1.0.1`            | `1.1.1`            |                                          |
| `pg-hardstorage`               | -                  | `1.0.8`            |                                          |
| `codex`                        | `0.125.0`          | `0.144.1`          |                                          |
| `claude`                       | `2.1.123`          | `2.1.206`          |                                          |
| `opencode`                     | `1.14.30`          | `1.17.18`          |                                          |
| `agentsview`                   | `0.26.0`           | `0.37.5`           |                                          |
| `genai-toolbox`                | `1.1.0`            | `1.6.0`            | Package name is `mcp-toolbox`             |
| `crush`                        | `0.64.0`           | `0.84.0`           |                                          |
| `code`                         | `1.118.1`          | `1.128.0`          |                                          |
| `code-server`                  | `4.117.0`          | `4.127.0`          |                                          |
| `victoria-metrics`             | `1.142.0`          | `1.147.0`          |                                          |
| `victoria-metrics-cluster`     | `1.142.0`          | `1.147.0`          |                                          |
| `vmutils`                      | `1.142.0`          | `1.147.0`          |                                          |
| `victoria-logs`                | `1.50.0`           | `1.51.0`           |                                          |
| `vlagent`                      | `1.50.0`           | `1.51.0`           |                                          |
| `vlogscli`                     | `1.50.0`           | `1.51.0`           |                                          |
| `victoria-traces`              | `0.8.2`            | `0.9.4`            |                                          |
| `prometheus`                   | `3.11.3`           | `3.13.1`           |                                          |
| `alertmanager`                 | `0.32.1`           | `0.33.1`           |                                          |
| `pushgateway`                  | `1.11.2`           | `1.11.3`           |                                          |
| `node_exporter`                | `1.11.1`           | `1.11.1`           | Backfilled the tarball cache; corrected version metadata |
| `redis_exporter`               | `1.82.0`           | `1.86.0`           |                                          |
| `mongodb_exporter`             | `0.50.0`           | `0.51.0`           |                                          |
| `grafana`                      | `13.0.1`           | `13.1.0`           |                                          |
| `grafana-victorialogs-ds`      | `0.26.3`           | `0.29.0`           |                                          |
| `grafana-victoriametrics-ds`   | `0.24.0`           | `0.25.2`           |                                          |
| `vector`                       | `0.55.0`           | `0.56.0`           |                                          |
| `minio`                        | `20260417000000`   | `20260618000000`   |                                          |
| `seaweedfs`                    | `4.22`             | `4.39`             |                                          |
| `rustfs`                       | `1.0.0-b1`         | `1.0.0-b8`         | Prerelease line                          |
| `duckdb`                       | `1.5.2`            | `1.5.4`            |                                          |
| `kafka`                        | `4.2.0`            | `4.3.1`            |                                          |
| `etcd`                         | `3.6.10`           | `3.6.13`           |                                          |
| `restic`                       | `0.18.1`           | `0.19.1`           |                                          |
| `juicefs`                      | `1.3.1`            | `1.4.0`            |                                          |
| `tigerbeetle`                  | `0.17.2`           | `0.17.9`           |                                          |
| `tigerfs`                      | `0.6.0`            | `0.7.0`            |                                          |
| `caddy`                        | `2.11.2`           | `2.11.4`           |                                          |
| `cloudflared`                  | `2026.2.0`         | `2026.7.1`         |                                          |
| `headscale`                    | `0.28.0`           | `0.29.2`           |                                          |
| `v2ray`                        | `5.48.0`           | `5.51.2`           |                                          |
| `nodejs`                       | `24.15.0`          | `24.18.0`          |                                          |
| `golang`                       | `1.26.2`           | `1.26.5`           |                                          |
| `hugo`                         | `0.161.1`          | `0.164.0`          |                                          |
| `uv`                           | `0.11.8`           | `0.11.28`          |                                          |
| `rclone`                       | `1.73.5`           | `1.74.4`           |                                          |
| `asciinema`                    | `3.2.0`            | `3.2.1`            |                                          |
| `stalwart`                     | `0.16.2`           | `0.16.12`          |                                          |
| `maddy`                        | `0.9.3`            | `0.9.5`            |                                          |
| `dblab`                        | `0.38.0`           | `0.43.0`           |                                          |
| `npgsqlrest`                   | `3.12.0`           | `3.20.0`           |                                          |
| `postgrest`                    | `14.10`            | `14.14`            |                                          |
| `sabiql`                       | `1.11.1`           | `1.14.0`           |                                          |
| `pev2`                         | `1.21.0`           | `1.22.0`           |                                          |
| `rainfrog`                     | `0.3.18`           | `0.3.19`           |                                          |

**Validation and Checksums**

All 14 offline deployment tests covering EL9/10, Debian 12/13, and Ubuntu 22/24/26 across `x86_64` and `aarch64` are complete, with `failed=0` and `unreachable=0` in every case; EL8 remains available for online installation only.

The MD5 checksums below cover all 14 validated artifacts. Six Community Edition artifacts are uploaded to GitHub, while the other eight are delivered through the Professional Edition; GitHub records SHA-256 digests for the uploaded Community Edition artifacts.

```bash
7de8b932412f1863fd9c033a7be355d7  pigsty-pkg-v4.4.0.d12.aarch64.tgz
2e5006a8d35eb1c087dc0ed11cf14d14  pigsty-pkg-v4.4.0.d12.x86_64.tgz
955308c00d3890f6e82a6a83bc624760  pigsty-pkg-v4.4.0.d13.aarch64.tgz
350f31c66de0aafff3bd91c2c9d740a0  pigsty-pkg-v4.4.0.d13.x86_64.tgz
0b4817a8edbab0bdf37ecee730fb0412  pigsty-pkg-v4.4.0.el10.aarch64.tgz
4584a61e4456749e68d86e4817cfe526  pigsty-pkg-v4.4.0.el10.x86_64.tgz
21621daf510a532829c36464d48f9198  pigsty-pkg-v4.4.0.el9.aarch64.tgz
504afd5030e2738a25e1b4c570d0e654  pigsty-pkg-v4.4.0.el9.x86_64.tgz
461c999424dee587ca33fe1a63df40d7  pigsty-pkg-v4.4.0.u22.aarch64.tgz
20ccc5ab8f9f4648b05bcd304f9fb5fc  pigsty-pkg-v4.4.0.u22.x86_64.tgz
d092c48ee55116ed5e2c99a3d909ccdd  pigsty-pkg-v4.4.0.u24.aarch64.tgz
24fa5399d8421305961fcaf91325b382  pigsty-pkg-v4.4.0.u24.x86_64.tgz
36f69b699d8b3041d35384970e157631  pigsty-pkg-v4.4.0.u26.aarch64.tgz
330047d117b20f04317dce506edd5d9a  pigsty-pkg-v4.4.0.u26.x86_64.tgz
3077203c0c656ec99abc32b227f6566b  pigsty-v4.4.0.tgz
```
