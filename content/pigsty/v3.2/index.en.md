---
title: "Pigsty v3.2: pig CLI + ARM Extensions"
linkTitle: "Pigsty v3.2 Release Notes"
date: 2024-12-29
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.2.0)）
summary: >
  The new `pig` CLI manages PostgreSQL packages across 10 Linux distros, ARM64 gets a full extension repo, and Supabase/Grafana integrations stay fresh.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.2.0

Pigsty closes 2024 with v3.2 and two big moves: a Go-based `pig` CLI that treats PG + extensions like first-class packages, and full ARM64 coverage for 340+ extensions across EL8/9, Debian12, Ubuntu 22/24. Supabase self-hosting tracks the latest release-week changes, and Grafana plugins/data sources (ECharts, Infinity, Victoria, etc.) are now packaged as RPM/DEB for offline installs.

--------

## v3.2.0 Release Notes

- Highlights: `pig` CLI 0.2.0, ARM64 extension repo, up-to-date Supabase flows on every distro, Grafana 11.4 with Infinity data source.
- New extensions: TimescaleDB bundle (loader/toolkit/tool), pgroonga (EL builds), VectorChord 0.1.0, pg_bestmatch.rs 0.0.1, pglite_fusion 0.0.3, pgpdf 0.1.0.
- Updated extensions: pgvectorscale 0.4→0.5.1, pg_parquet 0.1→0.1.1.
- Supabase: follow-up on December release week; OrioleDB packaging underway for the new beta option.
- Grafana: plugin/data-source packages for both arch-independent and arch-specific plugins (Infinity, Victoria data sources, etc.).
