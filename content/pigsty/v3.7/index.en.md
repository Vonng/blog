---
title: "Pigsty v3.7: Magneto Award and PG18 Ready"
linkTitle: "Pigsty v3.7 Release"
date: 2025-12-03
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v3.7.0))
summary: >
  PostgreSQL 18 becomes the default version, EL10 and Debian 13 support added, extensions reach 437, and Pigsty wins the PostgreSQL Magneto Award.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.7.0) | [**Release Note**](https://pigsty.io/docs/releasenote/#v370)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.7.0)

Pigsty v3.7.0 is officially released, bringing complete production-grade PostgreSQL 18 support and support for four new operating systems: Debian 13 and EL 10 across both x86_64/ARM64 architectures. Extension count has grown from 423 to 437, with numerous extensions updated to latest versions.

Additionally, Supabase, IvorySQL, PolarDB, Percona TDE, and other kernels have all been upgraded to latest versions, and infrastructure components like Prometheus, Grafana, DuckDB, and Etcd have completed a round of concentrated updates.

For outstanding contributions to the PostgreSQL extension ecosystem, Pigsty received the **"PostgreSQL Magneto"** award at the 8th PostgreSQL Database Ecosystem Conference.

![](magneto-award.jpg)


--------

## PostgreSQL 18 Becomes Default Version

With the release of PostgreSQL 18.1, PG 18 is production-ready. Pigsty v3.7 officially sets it as the default version.

PG 18 introduces several important features: Temporal Primary Key, built-in UUIDv7, Index Skip Scan, Asynchronous I/O (AIO), virtual generated columns, EXPLAIN enhancements, OAuth 2.0 support, and more. If these features match your business needs, now is a good time to upgrade.

Meanwhile, PG 13.23 released in November will be the last PG 13 version — that major version has officially entered EOL status. Pigsty v3.7 is the last version with complete PG 13 extension support — all extensions have been recompiled, but will no longer be updated going forward.


--------

## Epic Extension Update

Supporting PG 18 goes far beyond kernel deployment. From the beta stage, Pigsty has provided PG 18 deployment capability, but to make it the production default, extension ecosystem follow-through is crucial. Currently, except for Citus, mainstream extensions all support PG 18. We've fixed dozens of extension compatibility issues and unified pgrx versions across 40+ Rust extensions.

This is an epic update. Available extensions on PG 18 reach 390-405 (varies slightly by distribution). Complete extension availability information is available at [PGEXT.CLOUD](https://pgext.cloud). Extension updates over the past three months:

![](changes.jpg)

Several extensions see milestone updates:

- **pg_duckdb 1.1**: Code quality significantly improved, EL8 compatibility issues fixed
- **pg_mooncake 0.2**: Rewritten in Rust, now a sub-extension of pg_duckdb, both can coexist
- **VectorChord 1.0**: Official stable version released
- **pg_search 0.20**: Major ParadeDB full-text search extension update

Supporting PG 18, Debian 13, and EL 10 means the compile/test matrix expanded from 50 combinations (5 PG × 10 OS) to 84 combinations (6 PG × 14 OS) — a 68% increase. RPM/DEB packages in the repository grew from 40,000+ to 60,000+.

To improve efficiency, we fully automated the entire extension build process. Now just spin up a container, execute `pig build pkg <ext>` to complete the build. This extension repository and build infrastructure is completely standalone — even without using Pigsty, you can install extensions directly via YUM/APT. All code is Apache-2.0 licensed open source.

**For this contribution, Pigsty received the "PostgreSQL Magneto" award at the 8th PostgreSQL Database Ecosystem Conference.**

![](magneto-cert.jpg)


--------

## New OS Support: EL 10 and Debian 13

This version adds four new OS support targets, bringing the mainstream support total to 14.

![](os.jpg)

**Major challenges during adaptation:**

- **EL 10 Missing Ansible**: Official repos lack `ansible-collection-community-crypto` — we ported and packaged the EL9 version
- **Ansible 2.19 Breaking Changes**: Extensive syntax incompatibilities required comprehensive adaptation to ensure both old and new versions work correctly
- **LLVM Version Upgrade**: PGDG repos on EL9/EL10 upgraded from LLVM 19 to LLVM 20, introducing compatibility issues
- **ARM64 Repository Adjustments**: el10.aarch64 PGDG repos underwent multiple rounds of adjustment
- **Frequent Dependency Changes**: Upstream package dependencies continuously shifting

This is also why we don't recommend users manually wrestling with PostgreSQL deployment: often the problem isn't operator error but [upstream changes](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247490601&idx=1&sn=6c5ae3fcfeb2714cf27ce6566f7b54bd&scene=21#wechat_redirect) causing dependency breakage. Using Pigsty offline packages locks in complete dependencies at a specific point in time, ensuring deployment stability.

**Maintenance Strategy Adjustment**: Pigsty will only maintain the two most recent major versions in each series. With EL 10 and Debian 13 joining, EL 8, Debian 11, and Ubuntu 20.04 will no longer receive proactive updates (support not removed) — new extension packages and test processes will no longer cover these older systems.


--------

## Multi-Kernel Synchronized Updates

Besides the vanilla PostgreSQL kernel, this version synchronizes updates across multiple derivative kernels:

![](kernels.jpg)

| Kernel | Update Content |
|------|----------|
| **Supabase** | All Docker images updated to latest, underlying upgraded to PG 18 |
| **IvorySQL** | Upgraded from 4.5 to 5.0, compatible with PG 18.0 |
| **Percona TDE** | Transparent encryption kernel upgraded from PG 17.5 to PG 18.1 compatible |
| **PolarDB** | Released 15.15.5.0, added Debian 13/EL 10 RPM/DEB packages |
| **FerretDB** | Updated to 2.7, underlying DocumentDB upgraded to 0.107 |
| **OpenHalo / OrioleDB** | Added Debian 13 and EL 10 support |

All these kernels work smoothly on new operating systems (except Babelfish), further solidifying Pigsty's position as a "Meta-Distribution" — a unified platform for out-of-the-box experience with various PostgreSQL flavors.


--------

## Parameter Template Optimization

Default parameter templates optimized for PG 18 and new scenarios:

![](parameters.jpg)

- Optimized CPU, process, thread, and parallel query related parameter configurations
- Ensured adequate background worker resources for various extensions
- Relaxed OLTP template restrictions on parallel queries
- Added maintenance, troubleshooting, and accidental deletion recovery SOP documentation


--------

## Vision: The Ubuntu of the PostgreSQL Ecosystem

Pigsty has become the highest-starred PostgreSQL ecosystem open-source project from China, establishing considerable recognition and influence internationally.

Our vision: Make Pigsty the mainstream distribution in the PostgreSQL world, occupying an ecosystem position in the database realm similar to Debian, Ubuntu, and RHEL in the operating system realm.

Implementation path:

- **Focus on Core Scenarios**: Large-scale production-grade PostgreSQL management on native Linux
- **Build Differentiated Advantages**: Industry-leading monitoring system and most complete extension ecosystem
- **Integrate Ecosystem Resources**: Incorporating core capabilities from distributions like Supabase and Percona
- **Optimize Developer Experience**: Balancing professionalism with usability



--------
--------

## v3.7.0

Pigsty v3.7.0 released with deep PostgreSQL 18 support!

```bash
curl https://repo.pigsty.cc/get | bash -s v3.7.0
```

### Highlights

- Deep PostgreSQL 18 support, becomes default PG major version, extensions ready!
- Added EL10 / Debian 13 OS support, total reaches 14!
- Added PostgreSQL extensions, total reaches 437!
- Supports Ansible 2.19 post-breaking-change versions!
- Supabase, PolarDB, IvorySQL, Percona kernels updated to latest versions!
- Optimized PG default parameter setting logic for better resource utilization.

### Version Updates

- PostgreSQL 18.1, 17.7, 16.11, 15.15, 14.20, 13.23
- Patroni 4.1.0
- Pgbouncer 1.25.0
- pg_exporter 1.0.3
- pgbackrest 2.57.0
- Supabase 2025-11
- PolarDB 15.15.5.0
- FerretDB 2.7.0
- DuckDB 1.4.2
- Etcd 3.6.6
- pig 0.7.4

For more software version updates, refer to:

- [INFRA Changelog](https://pgext.cloud/en/release/infra/)
- [RPM Changelog](https://pgext.cloud/en/release/rpm/)
- [DEB Changelog](https://pgext.cloud/en/release/deb/)

### API Changes

- Set more reasonable optimization strategies for parallel execution related parameters
- In `rich` and `full` templates, citus extension no longer installed by default because citus doesn't yet support PG 18
- PG parameter templates now include duckdb series extension stubs
- Set 200, 2000, 3000 GB upper limits for `min_wal_size`, `max_wal_size`, `max_slot_wal_keep_size`
- Set 200 GB upper limit for `temp_file_limit`, 2 TB for OLAP
- Appropriately increased default connection pool connection counts
- Added `prometheus_port` parameter with default value `9058`, avoiding conflict with EL10 RHEL Web Console port
- Changed `alertmanager_port` parameter default to `9059`, avoiding potential conflict with Kafka SSL port
- Added `pg_pkg` `pg_pre` subtask to remove `bpftool`, `python3-perf` causing LLVM conflicts on el9+ before installing PG packages
- Added llvm repository module to Debian/Ubuntu default repository definitions
- Fixed `infra-rm.yml` package removal logic

### Compatibility Fixes

- Fixed Ubuntu/Debian CA trust Warning return code error
- Fixed extensive compatibility issues introduced by Ansible 2.19, ensuring normal operation on old and new versions
- Added int type conversion for seq type variables to ensure compatibility
- Changed many with_items to loop syntax for compatibility
- Added a layer of list nesting for key exchange variables to avoid character iteration on strings in new versions
- Explicitly converted range usage to list before use
- Modified name, port and other reserved marker variable naming
- Changed `play_hosts` to `ansible_play_hosts`
- Added string forced type conversion for some string types to avoid runtime errors

### EL10 Logic Adaptation

- Fixed EL10 missing ansible-collection-community-crypto unable to generate keys issue
- Fixed EL10 missing ansible logical package issue
- Removed modulemd_tools flamegraph timescaledb-tool
- Use java-21-openjdk instead of java-17-openjdk
- aarch64 YUM repository name issues

### Debian 13 Logic Adaptation

- Use `bind9-dnsutils` instead of `dnsutils`

### Ubuntu 24 Fixes

- Temporarily removed tcpdump package with broken upstream dependencies

### Checksums

```bash
e00d0c2ac45e9eff1cc77927f9cd09df  pigsty-v3.7.0.tgz
987529769d85a3a01776caefefa93ecb  pigsty-pkg-v3.7.0.d12.aarch64.tgz
2d8272493784ae35abeac84568950623  pigsty-pkg-v3.7.0.d12.x86_64.tgz
090cc2531dcc25db3302f35cb3076dfa  pigsty-pkg-v3.7.0.d13.x86_64.tgz
ddc54a9c4a585da323c60736b8560f55  pigsty-pkg-v3.7.0.el10.aarch64.tgz
d376e75c490e8f326ea0f0fbb4a8fd9b  pigsty-pkg-v3.7.0.el10.x86_64.tgz
8c2deeba1e1d09ef3d46d77a99494e71  pigsty-pkg-v3.7.0.el8.aarch64.tgz
9795e059bd884b9d1b2208011abe43cd  pigsty-pkg-v3.7.0.el8.x86_64.tgz
08b860155d6764ae817ed25f2fcf9e5b  pigsty-pkg-v3.7.0.el9.aarch64.tgz
1ac430768e488a449d350ce245975baa  pigsty-pkg-v3.7.0.el9.x86_64.tgz
e033aaf23690755848db255904ab3bcd  pigsty-pkg-v3.7.0.u22.aarch64.tgz
cc022ea89181d89d271a9aaabca04165  pigsty-pkg-v3.7.0.u22.x86_64.tgz
0e978598796db3ce96caebd76c76e960  pigsty-pkg-v3.7.0.u24.aarch64.tgz
48223898ace8812cc4ea79cf3178476a  pigsty-pkg-v3.7.0.u24.x86_64.tgz
```

See [GitHub Release](https://github.com/pgsty/pigsty/releases/tag/v3.7.0) for more details.
