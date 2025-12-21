---
title: Locks in PostgreSQL
date: 2019-06-11
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Snapshot isolation does most of the heavy lifting in PG, but locks still matter. Here’s a practical guide to table locks, row locks, intention locks, and `pg_locks`.
tags: [PostgreSQL, Development, Lock]
---

PostgreSQL relies on **snapshot isolation (SI)** for concurrency and **two-phase locking (2PL)** as a supporting act. DML (`SELECT/INSERT/UPDATE/DELETE`) uses SSI; DDL (`CREATE TABLE` etc.) still uses 2PL. Understanding locks is essential when diagnosing blocking, deadlocks, or weird error messages.

## Table-level locks

Table locks are automatically acquired when you run most SQL commands, or explicitly via `LOCK`. Each mode has a conflict set; incompatible locks can’t coexist on the same table.

### Evolution of lock modes

PG started with two modes: `SHARE` (read) and `EXCLUSIVE` (write). MVCC changed the rules—reads shouldn’t block writes and vice versa—so `ACCESS SHARE` and `ACCESS EXCLUSIVE` were born. `ACCESS SHARE` is the modern read lock (plain `SELECT`); `ACCESS EXCLUSIVE` blocks everything (`DROP`, `TRUNCATE`, `VACUUM FULL`). Classic `EXCLUSIVE` is still used by DML.

### Intention locks

Row-level locks need coordination with table locks. **Intention locks** advertise upcoming row locks on a table so the lock manager can detect conflicts quickly. `RowShareLock` (taken by `SELECT ... FOR SHARE/UPDATE`) and `RowExclusiveLock` (taken by `INSERT/UPDATE/DELETE`) are the intention locks that guard row-level `FOR` locks.

### Table lock modes at a glance

| Mode | Typical command |
|------|-----------------|
| ACCESS SHARE | `SELECT` |
| ROW SHARE | `SELECT ... FOR UPDATE/SHARE` |
| ROW EXCLUSIVE | `INSERT/UPDATE/DELETE` |
| SHARE UPDATE EXCLUSIVE | `VACUUM`, `ANALYZE`, `CREATE INDEX CONCURRENTLY` |
| SHARE | `CREATE INDEX` (non-concurrent) |
| SHARE ROW EXCLUSIVE | `CREATE TRIGGER` |
| EXCLUSIVE | `REFRESH MATERIALIZED VIEW` |
| ACCESS EXCLUSIVE | `ALTER TABLE`, `DROP`, `TRUNCATE`, `VACUUM FULL` |

The higher you go in that list, the more restrictive the lock.

## Row-level locks

Row locks come from `SELECT ... FOR UPDATE|SHARE|KEY SHARE|NO KEY UPDATE`. They block conflicting actions on the same row but coexist nicely with MVCC readers. Row locks don’t show up explicitly in `pg_locks`; instead you’ll see transactions waiting on each other’s `transactionid` locks.

## Advisory locks

Advisory locks are user-managed locks keyed on 64-bit integers. Use them for application-level coordination: `pg_advisory_lock(…)` blocks until the key is free; `pg_try_advisory_lock` is non-blocking.

## Inspecting locks with `pg_locks`

`pg_locks` aggregates the lock table (plus fast-path locks). Key columns:

- `locktype` – relation, transactionid, virtualxid, advisory, etc.
- `database`, `relation`, `page`, `tuple` – which object is locked.
- `transactionid` / `virtualtransaction` – who holds or waits.
- `pid` – backend PID.
- `mode` – lock mode.
- `granted` – true if held, false if waiting.

Notes:

- It’s cluster-wide; you’ll see locks from all databases.
- Each backend can wait on at most one lock at a time (`granted = f`).
- Transactions always hold `ExclusiveLock` on their own `virtualxid`; writers also hold it on their `transactionid`. When you wait on someone else’s transaction, you’re really waiting for that lock to release.
- Row locks don’t appear directly; contention shows up as one transaction waiting on another’s `xid`.
- Advisory locks are represented via `classid/objid` carrying the 64-bit key.

## Takeaways

- MVCC avoids read/write blocking, but writers still block writers; intention + row locks coordinate that.
- Know your table lock modes; `ACCESS EXCLUSIVE` is the nuclear option.
- Use `pg_locks` (and friends like `pg_stat_activity`) to diagnose blocking, but be mindful of overhead.
- Advisory locks are great for application-level mutexes.
