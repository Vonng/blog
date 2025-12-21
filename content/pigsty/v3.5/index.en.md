---
title: "Pigsty v3.5: PG18 Beta + 421 Extensions"
linkTitle: "Pigsty v3.5 Release Notes"
date: 2025-06-22
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v3.5.0)）
summary: >
  Pigsty crosses 4K GitHub stars, adds PG18 beta support, delivers 421 extensions, new doc site, and Supabase/OrioleDB/OpenHalo improvements.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v3.5.0

Pigsty 3.5 celebrates 4k stars with a new docs site, PostgreSQL 18 beta templates, 421 packaged extensions, Supabase hardening (pgsodium key flow, logflare slot fixes), and GA support for OrioleDB + OpenHalo across all ten supported distros. Grafana 12 dashboards adjust for breaking changes, `pg_sentinal` adds ASH-style wait history, and Apple Silicon Vagrant boxes now run Pigsty smoothly.

--------

## v3.5.0 Release Notes

- Highlights: PG18 beta template, pg_exporter 1.0 with new metrics, Supabase self-hosting enhancers, `pig do` subcommand, PG/AWR-style wait event coverage via `pgsentinel`, Apple ARM Vagrant support.
- Extensions: 421 available; new ones include pgsentinel (wait history) and spat (shared-memory Redis experiment). Extension catalog lives at https://pgsty.com/ext.
- Kernels: OrioleDB + OpenHalo full-platform packages; Supabase-ready builds; Citus 13.0.2; PostgreSQL 17.5/16.9/15.13/14.18/13.21.
- Docs: brand new Next.js site (pgsty.com) with rewritten guides; Chinese version coming soon.
