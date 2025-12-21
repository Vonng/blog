---
title: A Methodology for Diagnosing PostgreSQL Slow Queries
date: 2021-02-23
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Slow queries are the sworn enemy of OLTP databases. Here’s how to identify, analyze, and fix them using metrics (Pigsty dashboards), pg_stat_statements, and logs.
tags: [PostgreSQL, PG-Admin, Performance]
---

> “You can’t optimize what you can’t measure.”

Slow queries hog connections, hold locks, block replication, trigger deadlocks, and waste resources. Every DBA must know how to find and fix them quickly.

## Traditional tools

- **`pg_stat_statements`** – essential extension that aggregates execution stats per normalized query: calls, total/mean/max time, rows per call, I/O time, etc. Always enable it.
- **Slow query logs** – controlled via `log_min_duration_statement`. Great for one-off incidents or forensic analysis, but sampling thresholds mean you miss sub-threshold issues. Full logging is expensive but the ultimate truth when you need it.

## Why monitoring helps

Static snapshots don’t show trends. Monitoring systems (Pigsty in my case) sample every few seconds, letting you rewind, compare before/after, and show stakeholders what’s happening. They also calm nervous bosses during incidents.

## Workflow (simulated incident)

We spin up the Pigsty sandbox, run pgbench load (50 TPS writes on the primary, 1000 TPS reads on a replica), then deliberately drop `pgbench_accounts_pkey` to break index scans.

### 1. Detection

Cluster dashboards show QPS collapsing and response times spiking (1 ms → 300 ms). System load shoots above 200%, alarms fire.

### 2. Identification

Use the **PG Query** dashboard to find the worst offender. Query ID `-6041100154778468427` has mean latency jumping from microseconds to hundreds of milliseconds while QPS plummets. Drill into **PG Stat Statements** to see the normalized SQL: `SELECT abalance FROM pgbench_accounts WHERE aid = $1`.

### 3. Hypothesis

Simple point lookup suddenly slow? Most likely the index vanished. Check **PG Table Catalog** and **PG Table Detail**: index scans drop to zero, seq scans soar. Hypothesis confirmed.

### 4. Fix

Recreate the index:

```sql
ALTER TABLE pgbench_accounts ADD PRIMARY KEY (aid);
```

Latency falls from seconds to milliseconds, QPS recovers, system load normalizes. Dashboards provide immediate feedback.

## Summary

1. **Detect** – monitor query latency, concurrency, and system load.
2. **Identify** – use pg_stat_statements/monitoring to find the exact query (by query ID).
3. **Hypothesize** – analyze the SQL, review table/index metrics.
4. **Fix & verify** – add indexes, rewrite queries, adjust schema, then watch metrics confirm success.

Pigsty’s dashboards wrap these steps into a workflow, but the methodology applies with any monitoring stack: measure, locate, hypothesize, fix, verify.
