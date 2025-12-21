---
title: "PG Extension Cloud: Unlocking PostgreSQL’s Entire Ecosystem"
linkTitle: PG Extension Cloud
date: 2025-11-12
summary: Free, open, no VPN. Install PostgreSQL and 431 extensions on 14 Linux distros × 6 PG versions via native RPM/DEB—and a tiny CLI.
tags: [PostgreSQL,Extension]
---

> [WeChat link](https://mp.weixin.qq.com/s/oHHzhbbt5suSxnJhyxTwQQ)

PostgreSQL’s killer feature is extensibility. PostGIS, pgvector, pg_duckdb, pg_search—extensions turn PG into GIS engine, vector DB, analytics warehouse, search cluster. But compiling and shipping them reliably across distros is a nightmare, especially when official mirrors freeze or your network can’t reach upstream.

After two years of grinding, I’m launching [**PGEXT.CLOUD**](https://pgext.cloud): the infrastructure for discovering, packaging, and installing PG extensions.

## What’s inside

- **Extension catalog** – Browse [431 extensions](https://pgext.cloud/list) with metadata, docs, compatibility matrices, how-to guides. Think “Wikipedia for PG extensions.”
- **Binary repos** – Native RPM/DEB packages for **14 Linux releases** and **6 major PG versions**. No Docker-only traps.
- **`pig` CLI** – A 4 MB Go tool that wraps your existing package manager and hides the matrix of platforms/versions.

Try it on a fresh server/container:

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
pig repo set
pig install -y -v 18 pgsql postgis timescaledb pgvector pg_duckdb
```

Behind those three lines sits combinatorial chaos—14 distros × 6 PG versions × 431 extensions. Now it’s a one-liner.

## Why we needed this

Official PGDG repos ship ~135 extensions. Popular ones (PostGIS, pgvector) are there, but many heavy-hitters aren’t: pg_duckdb, pg_mooncake, plv8, Supabase’s Rust extensions. PGDG maintainers understandably don’t want to maintain ten-minute Rust builds.

I hoped projects like Tembo’s `trunk` or pgxman would solve distribution. They didn’t. So I built it myself. Today PGEXT.CLOUD packages 260 EL extensions and 241 Debian extensions—about **72%** of everything listed. The catalog tracks availability by OS/version and documents installation for every extension.

## Smooth installs

`pig` isn’t a new package manager; it’s a piggyback layer over yum/dnf/apt. You can still use `apt install postgresql-pgvector` directly—the repos are standard. `pig` just automates repo setup, architecture detection, PG version switching, and dependency resolution.

## Open supply chain

Some folks asked, “You’re in China—how do we trust your binaries?” Supply-chain trust is hard regardless of nationality; even PGDG’s yum repo relies on Devrim’s reputation. My answer: everything is open. The build scripts, Dockerfiles, and tooling are public. You can rebuild any package yourself in an isolated environment:

```dockerfile
FROM debian:13
RUN apt update && apt install -y ca-certificates vim ncdu wget curl rsync unzip \
    && curl https://repo.pigsty.io/pig | bash -s v0.7.1 \
    && pig repo set && pig build tool && pig build spec && pig build rust && pig build pgrx
```

Then:

```bash
docker build -t d13 .
docker run -it d13 /bin/bash
pig build pkg timescaledb
```

The packages on PGEXT.CLOUD are built exactly this way. If you don’t trust me, rebuild locally and host your own repo. That’s the point: **open tooling, reproducible builds, no lock-in**.

PGEXT.CLOUD is my attempt to make PostgreSQL’s extension ecosystem accessible. Discover what exists, install it in seconds, and unleash PG’s full potential.
