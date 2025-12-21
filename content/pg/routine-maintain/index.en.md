---
title: "PostgreSQL Routine Maintenance"
date: 2018-02-10
author: "vonng"
summary: >
  Cars need oil changes, databases need maintenance. For PG, three important maintenance tasks: backup, repack, vacuum
tags: [PostgreSQL, PG-Admin]
---

Cars need oil changes, databases need maintenance.

## Maintenance Tasks in PG

For PG, there are three important maintenance tasks: backup, repack, vacuum

* **Backup**: The most important routine work, a lifeline.
  * Create base backups
  * Archive incremental WAL
* **Repack**
  * Repacking tables and indexes eliminates bloat, saves space, and ensures query performance doesn't degrade.
* **Vacuum**
  * Maintains table and database age, prevents transaction ID wraparound failures.
  * Updates statistics, generates better execution plans.
  * Reclaims dead tuples, saves space, improves performance.

## Backup

Backup can use `pg_backrest` as an all-in-one solution, but here we consider using scripts for backup.

Reference: [`pg-backup`](https://github.com/Vonng/pigsty/blob/master/roles/postgres/files/pg/pg-backup)

## Repack

Repack uses `pg_repack`. PostgreSQL's official repository includes pg_repack.

Reference: [`pg-repack`](https://github.com/Vonng/pigsty/blob/master/roles/postgres/files/pg/pg-repack)

## Vacuum

Although AutoVacuum exists, manual vacuum execution is still helpful. Check database age and report promptly when aging occurs.

Reference: [`pg-vacuum`](https://github.com/Vonng/pigsty/blob/master/roles/postgres/files/pg/pg-vacuum)