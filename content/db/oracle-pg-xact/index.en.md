---
title: Comparing Oracle and PostgreSQL Transaction Systems
summary: "The PG community has started punching up: Cybertec's Laurenz Albe breaks down how Oracle's transaction system stacks against PostgreSQL."
date: 2025-02-27
authors: ["laurenz-albe"]
tags: [Database, PostgreSQL, Oracle]
---

> Original by [Laurenz Albe](https://www.cybertec-postgresql.com/en/comparison-of-the-transaction-systems-of-oracle-and-postgresql/). Translation and commentary by Feng Ruohang.

Transactions sit at the heart of relational databases. They guarantee **data integrity** for applications. SQL defines some transactional behavior but leaves plenty unspecified, so implementations differ wildly.

With many orgs migrating from Oracle to PostgreSQL, understanding those differences keeps you from getting burned. Here’s the comparison.

-------

## ACID recap

ACID stands for:

- **Atomicity** – every statement in a transaction succeeds or the entire thing rolls back, even under hardware faults.
- **Consistency** – constraints stay satisfied.
- **Isolation** – concurrent transactions don’t produce anomalies; you only see states achievable via some serial order.
- **Durability** – once committed, a transaction survives crashes.

-------

## Where Oracle and PostgreSQL align

Plenty of fundamentals match:

- Both use MVCC: readers don’t block writers and vice versa.
- Locks are held until transaction end.
- Row locks live in the rows themselves, not in lock tables—no lock escalation, at the cost of extra writes.
- Both support `SELECT ... FOR UPDATE` for explicit concurrency control (details differ later).
- Default isolation is `READ COMMITTED` with very similar semantics.

-------

## Atomicity differences

### Autocommit

Oracle implicitly starts a transaction on any DML unless one is already running. You must `COMMIT` or `ROLLBACK`; there’s no “BEGIN.”

PostgreSQL runs in **autocommit**: every statement runs inside its own transaction unless you explicitly `BEGIN`/`START TRANSACTION`. The server auto-commits single-statement transactions.

Most client libraries hide the gap by sending `BEGIN` when you disable autocommit.

### Statement-level rollback

Oracle rolls back only the failed statement; the transaction stays alive. You decide whether to roll back the entire thing.

PostgreSQL aborts the entire transaction when any statement errors. Future statements are ignored until you `ROLLBACK` or `COMMIT` (both clear the failure).

Well-structured apps typically roll back on errors anyway, but for long-running batch jobs with bad rows you might prefer Oracle’s behavior. In PG you’d use SQL-standard savepoints—implemented as subtransactions, so they carry overhead.

### Transactional DDL

Oracle executes an implicit `COMMIT` before and after every DDL, so **DDL isn’t transactional**. PostgreSQL treats DDL like any other statement and guarantees atomicity, but DDL errors abort the entire transaction.

PG also has `SET CONSTRAINTS` to defer constraint checks; Oracle lacks the on/off toggles.

-------

## Isolation differences

### Isolation levels offered

Both expose the four SQL isolation levels.

Oracle implements:

- `SERIALIZABLE` → MVCC snapshot isolation (repeatable read).
- `READ COMMITTED` → true read committed.
- `READ ONLY` → static snapshot.
- `READ UNCOMMITTED` → behaves like read committed because dirty reads aren’t allowed.

Serializable in Oracle is speedy but not truly serializable. Consider two concurrent transactions both checking `count(*)` and inserting when it’s zero. Oracle lets both insert because the second sees its own uncommitted change and believes the count is still zero. It also throws serializable errors for unrelated reasons (e.g., the first insert into a table when `SEGMENT CREATION IMMEDIATE` wasn’t specified).

PostgreSQL also lists four levels, but `READ UNCOMMITTED` is silently promoted to `READ COMMITTED`. Its `SERIALIZABLE` is genuinely serializable via SSI, and `REPEATABLE READ` mirrors Oracle’s “serializable” snapshot behavior—only cleaner.

### `READ COMMITTED` anomalies

At `READ COMMITTED`, many anomalies are permitted. Example (detailed [here](https://www.cybertec-postgresql.com/en/transaction-anomalies-with-select-for-update/)):

1. Transaction A updates a row but hasn’t committed.
2. Transaction B runs `SELECT ... FOR UPDATE`, blocks.
3. Transaction A commits.

Both databases see the latest committed data, but differ:

- PostgreSQL only re-evaluates the locked rows—fast but potentially inconsistent.
- Oracle reruns the entire query—slower but consistent.

-------

## Durability

Both use write-ahead logging (Oracle “redo,” Postgres WAL). Guarantees are equivalent.

-------

## Other differences

### Transaction size/duration limits

Oracle stores old versions in UNDO tablespaces; Postgres stores them inline. Result: **Oracle transactions are bounded by UNDO size**, so deletes/updates are often chunked with commits between batches. PostgreSQL removes that cap, though huge updates cause bloat and require `VACUUM`. Massive deletes don’t need chunking.

Long transactions are bad everywhere: they hold locks and invite deadlocks. In Postgres they’re worse—they block autovacuum, causing bloat.

### `SELECT ... FOR UPDATE`

Both support `NOWAIT` and `SKIP LOCKED`. Oracle has `WAIT <n>`; PG lacks it but you can simulate it via `lock_timeout`.

Crucially, in PostgreSQL you shouldn’t use `FOR UPDATE` unless you’re deleting or changing a primary/unique key. For regular updates use `FOR NO KEY UPDATE`.

### Transaction ID wraparound

Only PostgreSQL suffers from [transaction ID wraparound](https://www.cybertec-postgresql.com/en/autovacuum-wraparound-protection-in-postgresql/). Each row stores a 32-bit transaction ID; as it wraps, rows must be `FREEZE`d. High-TPS systems must tune around it.

-------

## Conclusion

Oracle and PostgreSQL largely behave alike, but key differences matter—especially when migrating. Knowing them upfront avoids surprises.

-------

## Commentary

In “[PostgreSQL 17: Cards on the Table, We’re Not Pretending Anymore](https://mp.weixin.qq.com/s/oOZIP1CYj4a319YvoT7Y1w)” I noted a cultural shift: the PG community stopped being zen and started gunning for Oracle. EDB published TPC‑C headshots, now Cybertec is poking holes in Oracle’s transaction guarantees.

This piece reads neutral but lands the punch: ACID’s “A,” “C,” “D” are fine everywhere; the real story is isolation. Oracle’s “serializable” is mislabeled snapshot isolation. I already called it out in “[Why MySQL’s Correctness Falls Apart](https://mp.weixin.qq.com/s/gQZ3Q5JKV8gaBNhc1puPcA).” Among mainstream DBMSes, only PostgreSQL (and CockroachDB, derived from it) offers true serializable isolation.

- [← Previous](/en/blog/db/db-is-the-arch/)
- [Next →](/en/blog/db/pg-kiss-duckdb/)

Last updated 2025-02-27 — [optimize image (7cb69ff)](https://github.com/pgsty/web.cc/commit/7cb69ff32df80eba158e90dfd39b124ff85b79ab)
