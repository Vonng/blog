---
title: "PostgreSQL Slow Query Diagnostic Methodology"
date: 2021-02-23
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Slow queries are the arch-enemy of online business databases. This article introduces a general methodology for locating and diagnosing slow queries using monitoring systems.
tags: [PostgreSQL,PG Administration,Performance]
---


> You can't optimize what you can't measure

Slow queries are the arch-enemy of online business databases. How to diagnose and locate slow queries is a mandatory course for DBAs.

This article introduces the general methodology for diagnosing slow queries using the monitoring system — Pigsty.


---------------------

## Slow Queries: The Damage

For PostgreSQL databases that actually serve online business transaction processing, the damage from slow queries includes:

* Slow queries monopolize database connections, causing normal queries to have no connections available, piling up and leading to database avalanche.
* Slow queries lock old version tuples that have been cleaned up by the primary for a long time, causing streaming replication replay processes to deadlock, leading to primary-replica replication lag.
* The slower the query, the higher the probability of queries trampling on each other, making it easier to generate deadlocks, lock waits, transaction conflicts, and other problems.
* Slow queries waste system resources and raise system watermarks.

Therefore, a qualified DBA must know how to locate and handle slow queries in a timely manner.

![](slow-query-8.png)

> Figure: Before and after slow query optimization, the system's overall saturation dropped from 40% to 4%



---------------------

## Slow Query Diagnosis — Traditional Methods

Traditionally, PostgreSQL has two ways to obtain information related to slow queries: one is through the official extension `pg_stat_statements`, and the other is slow query logs.

The slow query log, as the name suggests, records all queries with execution time longer than the `log_min_duration_statement` parameter to PG's log. For locating slow queries, especially **for analyzing special cases and single slow queries, it is indispensable**. However, slow query logs also have their limitations. In production environments, for performance considerations, usually only queries exceeding a certain threshold are recorded, so much information cannot be obtained from slow query logs. Of course, it's worth mentioning that although the overhead is large, **full query logs are still the ultimate killer for slow query analysis**.

The more commonly used slow query diagnostic tool is probably `pg_stat_statements`. This is a very practical extension that collects statistical information about queries running in the database. **It is strongly recommended to enable this extension in any scenario**.



`pg_stat_statements` provides raw metric data in the form of system view tables. Each **type** of query in the system (i.e., queries with the same execution plan after extracting variables) is assigned a query ID, followed by metric data such as call count, total time consumed, maximum, minimum, average single execution time, response time standard deviation, average number of rows returned per call, and time spent on block IO.

A simple approach is to observe indicators like `mean_time/max_time`. From the system's catalog, you can indeed know the **historically average response time** of a certain type of query. For locating slow queries, this might be basically sufficient. However, indicators like this are just a **static snapshot** of the system at the current moment, so the questions they can answer are limited. For example, if you want to see whether the performance of a query has improved after adding a new index, using this method might be very cumbersome.

`pg_stat_statements` needs to be specified in `shared_preload_library` and explicitly created in the database via `CREATE EXTENSION pg_stat_statements`. After creating the extension, query statistical information can be accessed through the `pg_stat_statements` view.



### Definition of Slow Queries

How slow does a query have to be to be considered a slow query?

It should be said that this question **depends on the business** and the actual query type, and **there is no universal standard**.

As an empirical threshold, frequent CRUD point queries, if they exceed **1ms**, can be listed as slow queries.

For occasional single special queries, usually exceeding 100ms or 1s can be listed as slow queries.



## Slow Query Diagnosis — Pigsty

Monitoring systems can more comprehensively answer questions about slow queries. The data in monitoring systems is composed of countless **historical snapshots** (such as one snapshot sample every 5 seconds). Therefore, users can backtrack to any point in time and examine changes in query average response time over different time periods.

![](img/concept/slow-query.jpg)

> The above figure shows the interface provided by [PG Query Detail](/zh/docs/pgsql/dasdhboard/) in Pigsty, which displays detailed information about a single query.
>
> This is a typical slow query with an average response time of several seconds. After adding an index for it, from the Query RT dashboard in the upper right, you can see that the query's average response time dropped from several seconds to several milliseconds.

Users can use the **insights** provided by the monitoring system to quickly locate slow queries in the database, identify problems, and propose hypotheses. More importantly, users can **immediately** examine detailed metrics of tables and queries at different levels, apply solutions, and get **real-time feedback**, which is very helpful for emergency troubleshooting.

Sometimes the purpose of monitoring systems is not just to provide data and feedback; they can also serve as a soothing medicine for emotions: imagine a slow query causing a production database avalanche. If the boss or customer doesn't have a place to transparently know the current processing status, they will inevitably anxiously urge for updates, further affecting the speed of problem resolution. Monitoring systems can also serve as a basis for precise management. You can use changes in monitoring metrics to boast to bosses and customers with solid evidence.




---------------------

## A Simulated Slow Query Case

> Talk is cheap, show me the code

Assuming the user already has a [Pigsty sandbox demo environment](/zhhttps://pigsty.io/docs/setup/provision/), the following will use the Pigsty sandbox to demonstrate the simulated slow query location and handling process.



---------------------

### Slow Queries: Simulation

Since there's no actual business system, here we simulate slow queries in the system in a simple and quick way, using the `tpc-b`-like scenario that comes with `pgbench`.

Through `make ri / make ro / make rw`, initialize pgbench use cases on the `pg-test` cluster and apply read-write load to the cluster:

```bash
# 50TPS write load
while true; do pgbench -nv -P1 -c20 --rate=50 -T10 postgres://test:test@pg-test:5433/test; done

# 1000TPS read-only load
while true; do pgbench -nv -P1 -c40 --select-only --rate=1000 -T10 postgres://test:test@pg-test:5434/test; done
```

Now we have a simulated running business system. Let's simulate a slow query scenario through a simple and brutal method. Execute the following command on the primary of the `pg-test` cluster to delete the primary key of table `pgbench_accounts`:

```sql
ALTER TABLE pgbench_accounts DROP CONSTRAINT pgbench_accounts_pkey ;
```

This command will remove the primary key on the `pgbench_accounts` table, causing **related queries** to change from index scans to sequential full table scans, all becoming slow queries. Access [PG Instance](/zh/zh/docs/pgsql/dasdhboard) ➡️ Query ➡️ QPS, the result is shown in the figure below:

![](slow-query-1.jpg)

> Figure 1: Average query response time soared from 1ms to 300ms, and QPS of a single replica instance dropped from 500 to 7.

At the same time, due to slow query accumulation, the system will instantly **avalanche and overload**. Access the [PG Cluster](/zh/zh/docs/pgsql/dasdhboard) homepage to see cluster load spikes.


![](slow-query-2.png)

> Figure 2: System load reached 200%, triggering machine overload and query response time too long alert rules.




---------------------

### Slow Queries: Location

First, use the [PG Cluster](/zh/zh/docs/pgsql/dasdhboard) panel to locate the specific instance where the slow query is located, here using `pg-test-2` as an example.

Then, use the [PG Query](/zh/zh/docs/pgsql/dasdhboard) panel to locate the specific slow query: number **-6041100154778468427**

![](slow-query-3.jpg)

> Figure 3: Discover abnormal slow queries from the query overview

This query shows:

* Response time significantly increased: from 17us to 280ms 
* QPS significantly decreased: from 500 to 7
* Time spent on this query as a percentage significantly increased

It can be determined that this query has become slow!

Next, use the [PG Stat Statements](/zh/zh/docs/pgsql/dasdhboard/) panel or [PG Query Detail](/zh/zh/docs/pgsql/dasdhboard) to locate the **specific statement** of the slow query based on the query ID.

![](slow-query-4.png)

> Figure 4: Locate the query statement as `SELECT abalance FROM pgbench_accounts WHERE aid = $1`



---------------------

### Slow Queries: Hypothesis

After knowing the slow query statement, the next step is to infer the **cause** of the slow query.

```sql
SELECT abalance FROM pgbench_accounts WHERE aid = $1
```

This query uses `aid` as a filter condition to query the `pgbench_accounts` table. Such a simple query becoming slow is most likely due to an index problem on this table. *Anyone with a brain would know the index is missing, because we deleted it ourselves!*

After analyzing the query, we can **make a hypothesis**: This query became slow because the `aid` column on the `pgbench_accounts` table lacks an index.

The next step is to **verify the hypothesis**.

First, using [PG Table Catalog](/zh/zh/docs/pgsql/dasdhboard), we can examine table details, such as indexes built on the table.

Second, consult the [PG Table Detail](/zh/zh/docs/pgsql/dasdhboard) panel to check access to the `pgbench_accounts` table to verify our hypothesis.


![](slow-query-5.png)
> Figure 5: Access situation on the `pgbench_accounts` table

Through observation, we found that **index scans** on the table dropped to zero, while **sequential scans** increased correspondingly. This confirms our hypothesis!



---------------------

### Slow Queries: Solution

Once the hypothesis is established, we can proceed to propose solutions to solve the problem.

There are usually three ways to resolve slow queries: **modify table structure**, **modify queries**, **modify indexes**.

Modifying table structure and queries usually involves specific business knowledge and domain knowledge, requiring case-by-case analysis. But modifying indexes usually doesn't require much specific business knowledge.

The problem here can be solved by adding an index. The `aid` column on the `pgbench_accounts` table lacks an index, so let's try adding an index to the `aid` column on the `pgbench_accounts` table to see if this can solve the problem.

```sql
CREATE UNIQUE INDEX ON pgbench_accounts (aid);
```

After adding the index, something magical happened.

![](slow-query-6.png)

> Figure 6: You can see that the query's response time and QPS have returned to normal.

![](slow-query-7.png)

> Figure 7: The system load has also returned to normal


---------------------

### Slow Queries: Evaluation

As the final step in slow query handling, we usually need to record the operation process and evaluate the results.

Sometimes a simple optimization can produce dramatic effects. Maybe a problem that originally required spending hundreds of thousands on additional machines was solved by creating an index.

This kind of story can be expressed in a vivid and intuitive way through monitoring systems, earning KPIs and credit.

![](slow-query-8.png)

> Figure: Before and after slow query optimization, the system's overall saturation dropped from 40% to 4%
>
> (Equivalent to saving X machines, XX million yuan, the boss was delighted, and you're the next CTO!)



---------------------

### Slow Queries: Summary

Through this tutorial, you have mastered the general methodology for slow query optimization:

* Locate the problem

* Propose hypotheses
* Verify assumptions
* Develop solutions
* Evaluate effects

Monitoring systems can play an important role throughout the entire lifecycle of slow query handling. They can also express DBAs' "experience" and "achievements" in a visualized, quantifiable, and replicable way.
