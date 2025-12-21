---
title: "Pigsty v3.3: 404 Extensions + Turnkey Apps"
linkTitle: "Pigsty v3.3 Release Notes"
date: 2025-02-20
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.3.0)）
summary: >
  Extension coverage jumps past 400, FerretDB 2.0 lands, Nginx certbot automation makes hosting easy, and Docker app templates get a first-class playbook.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.3.0

Pigsty 3.3 keeps pushing PostgreSQL’s envelope: 404 extensions are now packaged, including Microsoft’s PGDocumentDB, AWS’s PGCollection, Datadog’s pg_tracing, pg_curl, pgpdf, and 30+ Omnigres modules for building web apps inside PG. FerretDB 2.0 (backed by Microsoft DocumentDB) lets PG speak MongoDB natively. ParadeDB/DuckDB integrations continue to close the OLAP gap.

A new `app.yml` playbook turns Odoo, Dify, Supabase, and other Dockerized stacks into one-command installs. Nginx IaC plus certbot automation delivers free HTTPS in minutes; the Pigsty docs/demo/proxy infrastructure itself now runs on Pigsty. The `pig` CLI gained `pig build` for extension packaging, and the new Next.js site lives at pigsty.io (with pigsty.cc maintained for China).

--------

## v3.3.0 Release Notes

- Highlights: 404 extensions, Omnigres partnership, FerretDB 2.0, PGDocumentDB/PGCollection/pg_tracing/pg_curl/pgpdf, app templates (`app.yml`), certbot integration, new website + doc split, `pig build` subcommands.
- Software: follow upstream PG17.2/16.6 sets, pg_duckdb 0.3.1, pg_mooncake 0.1.2, pg_analytics 0.5.4, Grafana/Nginx scripts updated for quick HTTPS.
- Nginx: declarative server defs + automated cert issuance; only expose 80/443 inbound.
- App templates: Odoo ERP, Dify, Supabase, more; run `app.yml -l <name>` to provision.
- `pig` CLI: `pig build` installs toolchains, fetches specs/source, and builds RPM/DEB packages for any distro.
