---
title: "Pigsty v3.3: 404 Extensions, Turnkey Apps, New Website"
linkTitle: "Pigsty v3.3 Release"
date: 2025-02-20
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v3.3.0))
summary: >
  Pigsty v3.3 pushes available extensions to 404, adds turnkey app deployment with app.yml, delivers Certbot integration for automated HTTPS, and launches a redesigned website.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.3.0) | [**Release Note**](https://pigsty.io/docs/releasenote/#v330)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.3.0)

After two months of careful refinement, Pigsty v3.3 is officially released. As an open-source "batteries-included" PostgreSQL distribution, Pigsty aims to harness the collective power of the PG ecosystem, delivering a maintenance-free experience for self-hosting that rivals cloud RDS.

This version focuses on three key areas: **extensions**, **website deployment**, and **application templates**, significantly enhancing development, operations, and deployment capabilities.


--------

## 400+ Extensions Available

PostgreSQL is renowned for its rich extension mechanism, fostering a vast database ecosystem. Pigsty takes PostgreSQL's extension capabilities to the extreme.

A year ago when "[PostgreSQL is Eating the Database World](/blog/pg/pg-eat-db-world)" was published, Pigsty had about 150 available extensions, primarily from PG built-ins (70) and the official PGDG repository.

![](ext-growth.jpg)

Today, Pigsty v3.3 pushes the available extension count to **404**! Users can plug-and-play virtually any PostgreSQL extension they want — more importantly, they can [combine these extensions like building blocks](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247489151&idx=1&sn=8098166e6231965283d8d65315ccbab9&scene=21#wechat_redirect).

![](ext-ecosystem.jpg)

**Notable new extensions**:

| Extension | Description |
|-----|------|
| PGDocumentDB | Microsoft open-source, adds document database capabilities to PostgreSQL |
| PGCollection | From AWS, high-performance memory-optimized collection data types |
| pg_tracing | DataDog open-source, distributed call chain tracing |
| pg_curl | Supports dozens of network protocols for requests |
| pgpdf | Directly read/store PDFs, SQL full-text search on PDF content |
| Omni series | 30+ extensions from Omnigres for web app development inside PG |

![](omnigres.jpg)

Pigsty has formed a deep partnership with Omnigres: Pigsty integrates and distributes Omnigres extensions, while Omnigres as a downstream delivers extensions from Pigsty's repository to its users — a mutually beneficial arrangement.


--------

## FerretDB 2.0: PostgreSQL Becomes MongoDB

In collaboration with the FerretDB team, delivering a MongoDB solution based on PostgreSQL. FerretDB 2.0 uses Microsoft's open-source DocumentDB as the backend implementation, providing better performance and more complete functionality.

![](ferretdb.jpg)

Transform PG into a core-feature-complete MongoDB 5.0, accessing PostgreSQL data via MongoDB clients and wire protocol.


--------

## DuckDB Integration Race Continues

Pigsty v3.3 immediately tracks pg_duckdb 0.3.1, pg_mooncake 0.1.2, pg_analytics 0.5.4 — the latest versions adding ClickHouse-level analytics capabilities to PostgreSQL from different angles.

![](clickbench.jpg)

On ClickHouse's own ClickBench leaderboard, the PG extension mooncake has successfully broken into the Top 10 T1 tier. Under intense competition, the PostgreSQL ecosystem will soon produce an OLAP player comparable to `pgvector` in the vector database ecosystem.


--------

## pig and Extension Repository

Managing so many extensions becomes challenging. Pigsty's solution is the `pig` CLI tool and extension repository. One command gives PostgreSQL the combined superpowers of 400 extensions — even without using Pigsty.

While this unique extension library could serve as Pigsty's core competitive advantage, we'd rather contribute more to the PostgreSQL ecosystem. Therefore, the `pig` package manager and PostgreSQL extension repository are open-sourced under the permissive **Apache 2.0** license, open to the public and peers.

Several PostgreSQL vendors now install extensions from Pigsty's extension repository, becoming Pigsty downstream users. This is a solid way to participate in the global software supply chain.


--------

## Website Experience: Nginx IaC and Free HTTPS Certificates

Pigsty isn't just a PostgreSQL distribution — it's also a complete monitoring infrastructure, Etcd, MinIO, Redis, and Docker deployment management solution, and can even serve as a web hosting tool.

Pigsty provides full-featured Nginx configuration and certificate issuance SOPs. The Pigsty website and software repository are built using Pigsty itself.

![](nginx.jpg)

Simply define Nginx Servers in your config file, and Pigsty automatically creates the required configuration and applies for HTTPS certificates.

![](certbot.jpg)

Pigsty v3.2 already integrated certbot with default installation. One command handles HTTPS certificate issuance and renewal. You can proxy various services with Nginx, differentiate by domain, and unify access through ports 80/443 — just open inbound 80/443 TCP ports.


--------

## Application Templates: One-Click Docker Software Delivery

Many software packages use PostgreSQL. Previously, Pigsty provided Docker Compose templates, but users still had to manually copy directories, edit `.env` configs, and start containers manually.

Pigsty v3.3 provides a new `app.yml` playbook, compressing PostgreSQL-based Docker software delivery to a single command.

**Odoo ERP System**:

![](odoo.jpg)

**Dify AI Workflow Orchestration**:

![](dify.jpg)

**Self-hosted Supabase**:

![](supabase.jpg)

From bare metal to complete production application services — just a few commands and a few minutes of waiting.


--------

## pig CLI Enhancements

`pig` v0.3 adds the `pig build` subcommand for quickly setting up PG extension build environments.

```bash
curl https://repo.pigsty.cc/pig | bash # Install pig
pig build repo        # Add upstream repos
pig build tool        # Install build tools
pig build rust        # Configure rust/pgrx toolchain (optional)
pig build spec        # Download build specs
pig build get citus   # Download an extension source package
pig build ext citus   # Build an extension
```

The 200+ extensions Pigsty maintains are all built this way. Even if your OS isn't among Pigsty's supported ten distros, you can easily DIY extension RPM/DEB packages.


--------

## New Website Design

Starting with v3.3, Pigsty's international site (pigsty.io) and Chinese site (pigsty.cc) are officially separated, using independent domains, documentation, demos, and repositories.

![](homepage-1.jpg)

A brand-new homepage built on a Next.js template. With help from GPT o1-pro and Cursor, modern landing page development was completed quickly.

![](homepage-2.jpg)

For hosting, we tried various solutions: Vercel, Cloudflare Pages, Alibaba Cloud, Tencent Cloud EdgeOne, etc. Final conclusion: put overseas on Cloudflare, domestic on cloud servers.

The website deployment process is highly automated — within ten minutes, you can spin up Pigsty documentation + repository infrastructure sites in any region.

![](infra.jpg)

The PG extension catalog is now integrated into the documentation site at pigsty.cc/ext, with Chinese version available. A small tool automatically scans Pigsty and PGDG repository extension package versions and generates database records and info pages — users can browse and download extension RPM/DEB packages directly from the web.


--------

## Multi-Kernel Support Updates

v3.3 tracks IvorySQL 4.2 (PG 17 compatible version), resolving the issue where pgbackrest backups couldn't work with IvorySQL. IvorySQL experience is now consistent with standard PG kernel.

![](ivorysql.jpg)

We also pushed the PolarDB team to provide DEB packages for Debian and ARM64 platforms. PolarDB can now run smoothly on all 10 Linux distributions supported by Pigsty.

Use case for PolarDB kernel: If you have "localization" requirements, PolarDB is the simplest, most cost-effective solution — Pigsty can wrap the PolarDB kernel RPM/DEB into a powerful RDS service.



--------

## v3.3.0 Release Notes

Pigsty v3.3.0 released — available extensions increase to **404**!

```bash
curl https://repo.pigsty.cc/get | bash -s v3.3.0
```

### Highlights

- Available extensions increase to [**404**](/docs/pgsql/ext/)!
- PostgreSQL February minor updates: 17.4, 16.8, 15.12, 14.17, 13.20
- New feature: `app.yml` script for auto-installing Odoo, Supabase, Dify, etc.
- New feature: Further customize Nginx config in `infra_portal`
- New feature: Certbot support for quick free HTTPS certificate issuance
- New feature: `pg_default_extensions` now supports plain-text extension lists
- New feature: Default repos now include mongo, redis, groonga, haproxy, etc.
- New parameter: `node_aliases` for adding command aliases to nodes
- Fix: Resolved default EPEL repo address issue in Bootstrap script
- Improvement: Added Alibaba Cloud mirror for Debian Security repos
- Improvement: pgBackRest backup support for IvorySQL kernel
- Improvement: ARM64 and Debian/Ubuntu support for PolarDB

### Tool Improvements

- pg_exporter 0.8.0 now supports new metrics in pgbouncer 1.24
- New feature: Auto-completion for common commands like `git`, `docker`, `systemctl` [#506](https://github.com/pgsty/pigsty/pull/506) [#507](https://github.com/pgsty/pigsty/pull/507) by [@waitingsong](https://github.com/waitingsong)
- Improvement: Optimized `ignore_startup_parameters` in pgbouncer config template [#488](https://github.com/pgsty/pigsty/pull/488) by [@waitingsong](https://github.com/waitingsong)

### Website and Documentation

- New homepage design: Pigsty's website now has a fresh new look
- Extension catalog: Detailed info and download links for RPM/DEB binaries
- Extension building: `pig` CLI now auto-sets up PostgreSQL extension build environments

See [GitHub Release](https://github.com/pgsty/pigsty/releases/tag/v3.3.0) for more details.
