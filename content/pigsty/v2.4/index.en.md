---
title: "Pigsty v2.4: Monitor Cloud RDS"
linkTitle: "Pigsty v2.4 Release Notes"
date: 2023-09-14
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v2.4.0)）
summary: >
  PG16 GA support, RDS/PolarDB monitoring, Redis Sentinel HA, and a wave of new extensions arrive with Pigsty 2.4.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v2.4.0

PostgreSQL 16 dropped, and Pigsty shipped support within an hour. v2.4 also makes Pigsty a monitoring plane for cloud fleets: feed it connection strings from RDS for PostgreSQL or PolarDB and the new PGRDS dashboards tell you what’s really happening. Redis Sentinel HA gets automated, and we’re launching an enterprise support program + LTS channel.

The extension catalog expands significantly: Apache AGE (graph), zhparser (Chinese FTS), pg_roaringbitmap, pg_embedding (HNSW vectors), pg_tle (trusted language extensions), pgsql-http, plus pg_auth_mon, pg_checksums, pg_failover_slots, pg_readonly, postgresql-unit, pg_store_plans, pg_uuidv7, set_user, and more. All are packaged for EL7–EL9 when technically feasible.

--------

## v2.4.0 Release Notes

- PostgreSQL 16 GA support across EL8/EL9 (PGDG dropped EL7 for PG16).
- Monitor cloud PG (RDS, PolarDB) via new PGRDS dashboards; remote-only mode just needs a URI.
- Commercial support + 3-year LTS channel launched.
- Redis Sentinel monitoring/HA automation with the new `redis_sentinel_monitor` parameter.
- New extensions: Apache AGE, zhparser, pg_roaringbitmap, pg_embedding, pg_tle, pgsql-http, pg_auth_mon, pg_checksums, pg_failover_slots, pg_readonly, postgresql-unit, pg_store_plans, pg_uuidv7, set_user.
- Fix: Grafana 10.1 datasource registration missing `uid`.
