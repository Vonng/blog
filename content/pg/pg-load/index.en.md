---
title: "PostgreSQL's KPI"
linkTitle: "PostgreSQL's KPI"
date: 2020-05-29
author: "vonng"
summary: "Managing databases is similar to managing people - both need KPIs (Key Performance Indicators). So what are database KPIs? This article introduces a way to measure PostgreSQL load: using a single horizontally comparable metric that is basically independent of workload type and machine type, called **PG Load**."
tags: ["PostgreSQL","PG Management","Monitoring","Metrics"]
---

Managing databases is similar to managing people - both need KPIs (Key Performance Indicators). So what are database KPIs? This article introduces a way to measure PostgreSQL load: using a single horizontally comparable metric that is basically independent of workload type and machine type, called **PG Load**.

------

## 0x01 Introduction

In real production environments, there are often needs to measure database performance and load, and evaluate database utilization levels. One of the most basic forms is: can we have a single KPI-like metric that directly tells users whether their beloved database load has exceeded warning thresholds? Is the workload saturated or not?

Of course, there's an important piece of information implied here - users expect the load metric to be a **Saturation** indicator. Saturation refers to how "full" the service capacity is, usually measured by a specific indicator of the most constrained resource in the system. Generally speaking, 0% saturation means the system is completely idle, 100% saturation means full load. Systems experience severe performance degradation before reaching 100% utilization, so setting indicators also requires including a **utilization target**, or **warning thresholds (red line, yellow line)**. When system instantaneous load exceeds the red line, alerts should be triggered; when long-term load exceeds the yellow line, capacity expansion should be performed.

Unfortunately, defining how "saturated" a system is isn't easy and often requires indirect indicators. Evaluating a database's load level traditionally involves comprehensive assessment based on these types of indicators:

* Traffic: Queries per second (QPS), or transactions per second (TPS)
* Latency: Average query response time (Query RT), or average transaction response time (Xact RT)
* Saturation: Machine load, CPU usage, disk I/O bandwidth saturation, network I/O bandwidth saturation
* Errors: Database client connection queuing

These indicators all have reference value for database performance evaluation, but they also have various problems.

------

## 0x02 Problems with Common Evaluation Indicators

Let's look at what problems these existing common indicators have.

The first to pass are error-type indicators, such as connection pool queuing. The biggest problem with error-type indicators is that when errors appear, saturation may already be meaningless. **An important reason for evaluating saturation is to prevent system overload. If the system is already overloaded with many errors, using error phenomena to define saturation in reverse is meaningless**. Additionally, error-type indicators are difficult to quantify precisely. We can only say: when connection pools have queuing, database load is relatively high; the longer the queue, the higher the load; when there's no queuing, database load isn't very high, that's all. Such definitions certainly can't satisfy people.

The second to pass are system-level (machine-level) indicators. Databases run on machines, and indicators like CPU usage and I/O usage are closely related to database load levels. **If CPU and I/O are bottlenecks, theoretically bottleneck resource saturation indicators can directly be used** as database saturation indicators. But this isn't always true - the system bottleneck might be in the database itself. Moreover, strictly speaking, they are machine KPIs rather than DB KPIs. **When evaluating database load, system-level indicators can certainly be referenced, but the DB layer should also have its own evaluation indicators**. Database saturation indicators should exist first before comparing whether underlying resources or the database itself saturates first and becomes the bottleneck. This principle also applies to indicators observed at the application layer.

Traffic-type indicators have great potential, especially QPS and TPS which are quite representative. But these indicators also have problems. Queries on a database instance are often varied and diverse. A query taking 10 microseconds and one taking 10 seconds are both counted as one Q in statistics. **Indicators like QPS cannot be compared horizontally and only have rough reference value**. Even when query types change, they can't be compared vertically with their own historical data. It's also difficult to set utilization targets for QPS and TPS indicators. The same database executing `SELECT 1` can achieve hundreds of thousands of QPS, but when executing complex SQL, it might only achieve thousands of QPS. Different workload types and machine hardware significantly affect database QPS limits. Only when queries on a database are highly uniform and without complex changes can QPS have reference value. Under such strict conditions, QPS watermark targets can be set through stress testing.

Compared to QPS/TPS, RT (Response Time) indicators actually have more reference value. Because increasing response time is often a precursor to system saturation. According to experience, the higher the database load, the higher the average response time for queries and transactions. One advantage of RT over QPS is that **RT can have utilization targets set**, such as setting an absolute threshold for RT: not allowing production OLTP databases to have slow queries with RT exceeding 1ms. But indicators like QPS are hard to draw red lines for. However, RT has its own problems. The first problem is that it's still qualitative rather than quantitative - latency increases are warnings of system saturation but can't precisely measure system saturation. The second problem is that RT statistics indicators usually available from databases and middleware are averages, but what truly provides warning effects might be statistics like P99, P999.

After criticizing all common indicators here, what kind of indicators are suitable as database saturation indicators?

------

## 0x03 Measuring PG Load

Let's reference how **Node Load** and **CPU Utilization** evaluation indicators are designed.

### Node Load

To see machine load levels, you can use the `top` command in Linux systems. The first line of `top` command output prominently displays the current machine's **average load levels** for 1 minute, 5 minutes, and 15 minutes.

```bash
$ top -b1
top - 19:27:38 up 18:49,  1 user,  load average: 1.15, 0.72, 0.71
```

Here the three numbers after `load average` represent the system's average load levels for the last 1 minute, 5 minutes, and 15 minutes respectively.

What do these numbers actually mean? The simple explanation is: the larger this number, the busier the machine.

In single-core CPU scenarios, Node Load (hereafter referred to as load) is a very standard saturation indicator. For single-core CPUs, when load is 0, the CPU is in a completely idle state; when load is 1 (100%), the CPU is in exactly full working state. When load exceeds 100%, the portion exceeding 100% represents tasks queuing.

Node Load also has its own **utilization targets**. Usually the experience is that for single cores: 0.7 (70%) is the yellow line, meaning the system has problems and needs checking soon; 1.0 (100%) is the red line, load greater than 1 means processes start accumulating and need immediate attention; 5.0 (500%) is the death line, meaning the system is basically blocked.

For multi-core CPUs, things are slightly different. Assuming there are n cores, when system load is n, all CPUs are in full working state; when system load is n/2, we can roughly consider half the CPU cores are running at full load. Thus a 48-core CPU machine has a full load of 48. Overall, if we divide machine load by the machine's CPU core count, the resulting indicator stays consistent with single-core scenarios (0% idle, 100% full load).

### CPU Utilization

Another very instructive indicator is **CPU Utilization**. CPU utilization is actually calculated through a simple formula. For single-core CPUs:

```yaml
1 - irate(node_cpu_seconds_total{mode="idle"}[1m]
```

Here `node_cpu_seconds_total{mode="idle"}` is a counter indicator representing total time the CPU has been in idle state. The `irate` function derives this indicator with respect to time, yielding the time per second the CPU is in idle state, in other words, the CPU idle rate. Subtracting this value from 1 gives CPU utilization.

For multi-core CPUs, you just need to add up each CPU core's utilization and divide by the CPU core count to get overall CPU utilization.

So what reference value do these two indicators have for PG load?

### Database Load (PG Load)

Can PG load also be defined similarly to CPU utilization and machine load? Of course, and this is an excellent idea.

Let's first consider PG load in single-process scenarios. Suppose we need an indicator where the load factor is 0 when the PG process is completely idle, and load is 1 (100%) when the process is at full capacity. Analogous to CPU utilization definition, we can use "***the proportion of time a single PG process is in active state***" to represent "single PG backend process utilization".

As shown in Figure 1, within a one-second statistical period, PG is in active state (executing queries or transactions) for 0.6 seconds, so the PG load for this second is 60%. If this unique PG process is busy throughout the entire statistical period and has 0.4 seconds of tasks queuing, then PG load can be considered 140%.

![](../img/pg-load-fig.png)

For parallel scenarios, the calculation method is similar to multi-core CPU utilization. First, sum up the active time of all PG processes within the statistical period (1s), then divide by "**available PG processes/connections**", or "**available parallelism**", to get PG's own utilization indicator, as shown in Figure 3. Two PG backend processes have active durations of 200ms+400ms and 800ms respectively, so overall load level is: `(0.2s + 0.4s + 0.8s) / 1s / 2 = 70%`

To summarize, PG load for a certain time period can be defined as:

`pg_load = pg_active_seconds / time_period / parallel`

* `pg_active_seconds` is the sum of time all PG processes are in active state during this time period
* `time_period` is the statistical period for load calculation, usually 1 minute, 5 minutes, 15 minutes, and real-time (less than 10 seconds)
* `parallel` is PostgreSQL's available parallelism, which will be explained in detail later

Since the quotient of the first two items is actually the total active duration per second over a period of time, this formula can be further simplified to the derivative of active duration with respect to time divided by available parallelism:

`rate(pg_active_seconds[time_period]) / parallel`

`time_period` is usually a fixed constant (1, 5, 15 minutes), so the problem becomes how to obtain the PG process total active time indicator `pg_active_seconds` and how to evaluate the database's available parallelism `max_parallel`.

------

## 0x04 Calculating PG Load Saturation

### **Transaction or Query?**

When we say database processes are active/idle, what exactly are we talking about? **What does it mean when PG is in active state?** If PG backend processes are executing queries, then certainly we can consider PG to be in busy state. But as shown in Figure 4, if PG processes are executing interactive transactions but not actually executing queries, i.e., the so-called "Idle in Transaction" state, how should we calculate "active duration"? The 200ms idle time between two queries in Figure 4 - should this time be considered "active" or "idle"?

**The core issue here is how to define active state**: whether database processes being in transactions count as active, or only when actually executing queries. For scenarios without interactive transactions, one query is one transaction, so either way is the same. But for multi-statement, especially interactive multi-statement transactions, there's a clear difference. From a resource usage perspective, not executing queries means not consuming database resources. But idle transactions occupy connections preventing connection reuse, and Idle In Transaction itself should be a situation to avoid. Overall, both definition methods work; using the transaction method slightly overestimates application load but may be more suitable from a load evaluation perspective.

### **How to Obtain Active Duration**

After deciding on the database backend process activity definition, the second question is: how to obtain database active duration over a period of time? Unfortunately, in PG, users can hardly obtain this performance indicator through the database itself. PG provides a system view: `pg_stat_activity`, which shows the list of currently running Postgres processes, but this is a point-in-time snapshot that can only roughly tell how many backend processes are in active vs idle states at the current moment. Counting database active time over a period becomes difficult. One solution is using Load-like calculation methods, periodically sampling the number of active processes in PG to calculate a load indicator. However, there's a better approach here, but it requires middleware assistance.

Database middleware is very important for performance monitoring because many indicators aren't provided by the database itself and can only be exposed through middleware. Taking Pgbouncer as an example, Pgbouncer maintains a series of statistical counters internally. Using `SHOW STATS` prints these indicators, such as:

- total_xact_count: Total number of transactions executed
- total_query_count: Total number of queries executed
- total_xact_time: Total time spent on transaction execution
- total_query_time: Total time spent on query execution

Here `total_xact_time` is the data we need - it records the total transaction time spent on a database in the Pgbouncer middleware. We just need to derive this indicator with respect to time to get the desired data: active duration proportion per second.

Using Prometheus PromQL to express the calculation logic, first derive the transaction time counter to calculate **active duration per second** at 1-minute, 5-minute, 15-minute, and real-time granularities (between the last two sampling points). Then roll up to sum, rolling database-level indicators up to instance-level indicators. (Connection pool `SHOW STATS` statistics here are per database, so when calculating instance-level total active duration, should roll up and sum, eliminating database dimension labels: `sum without(datname)`)

```yaml
- record: pg:ins:xact_time_realtime
expr: sum without (datname) (irate(pgbouncer_stat_total_xact_time{}[1m]))
- record: pg:ins:xact_time_rate1m
expr: sum without (datname) (rate(pgbouncer_stat_total_xact_time{}[1m]))
- record: pg:ins:xact_time_rate5m
expr: sum without (datname) (rate(pgbouncer_stat_total_xact_time{}[5m]))
- record: pg:ins:xact_time_rate15m
expr: sum without (datname) (rate(pgbouncer_stat_total_xact_time{}[15m]))
```

The resulting indicators can already be compared vertically with themselves and horizontally between instances of the same specifications. And regardless of database workload type, this indicator can be used.

However, **instances of different specifications still can't be compared using this indicator**. For example, for single-core single-connection PG, active duration per second at full load might be 1 second, which is 100% utilization. For 64-core 64-connection PG, active duration per second at full load is 64 seconds, which is 6400% utilization. Therefore, normalization is needed, which brings us to another question.

### How to Define Available Parallelism?

Unlike CPU utilization, PG's available parallelism doesn't have a clear definition and has some subtle relationships with workload types. But what can be determined is that within a certain range, **maximum available parallelism has a rough linear relationship with CPU core count**. Of course this conclusion assumes maximum database connections significantly exceed CPU core count. If only 30 connections are allowed on a 64-core CPU, then certainly maximum available parallelism is 30, not 64 CPU cores. Software parallelism ultimately needs hardware parallelism support, so we can simply use the instance's CPU core count as available parallelism.

Running 64 active PG processes on 64-core CPU gives load of (6400% / 64 = 100%). Similarly, running 128 active PG processes gives load of (12800% / 64 = 200%).

Using the active duration per second indicator calculated above, we can compute instance-level PG load indices.

```yaml
- record: pg:ins:load0
expr:  pg:ins:xact_time_realtime / on (ip) group_left()  node:ins:cpu_count
- record: pg:ins:load1
expr: pg:ins:xact_time_rate1m  / on (ip) group_left()  node:ins:cpu_count
- record: pg:ins:load5
expr: pg:ins:xact_time_rate5m  / on (ip) group_left()  node:ins:cpu_count
- record: pg:ins:load15
expr: pg:ins:xact_time_rate15m  / on (ip) group_left()  node:ins:cpu_count
```

### Another Interpretation of PG LOAD

If we carefully examine the definition of PG Load, we can find that active duration per second can roughly equal: TPS x XactRT, or QPS x Query RT. This makes sense - assuming QPS is 1000 and each query RT is 1ms, then time spent on queries per second is 1000 * 1ms = 1s.

Therefore, PG Load can be viewed as a derived indicator composed of three core indicators: `tps * xact_rt / cpu_count`

TPS and RT each have their problems for load evaluation, but when combined through simple multiplication into a new composite indicator, they suddenly show magical power (although actually calculated through other more accurate methods).

------

## 0x05 Actual Effects of PG Load

Next, let's look at PG Load's performance in actual production environments.

PG Load has two most direct uses: alerting and capacity evaluation.

### Case 1: Used for Alerting: Service Unavailability Due to Slow Query Accumulation

The figure below shows a production incident scene where a business deployed a slow query, instantly causing connection pools to be occupied by slow queries, leading to accumulation. We can see that both PG Load and RT reflected the fault situation promptly and accurately, while TPS appeared to drop into a pit, not particularly noticeable.

In terms of effect, PG Load1 and PG Load0 (real-time load) are quite sensitive indicators that can promptly and accurately respond to most faults related to pressure and load. So they were adopted as core alerting indicators.

PG Load utilization targets have some empirical values: yellow line is usually 50%, meaning threshold requiring attention; red line is usually 70%, meaning alert line requiring immediate action; 500% or higher usually means this instance has been overwhelmed.

![](pg-load-compare.png)

### Case 2: Used for Utilization Assessment and Capacity Planning

Compared to alerting, utilization assessment and capacity planning are more like PG Load's core uses. After all, alerting needs can still be met through latency, queued connections and other indicators.

Here, the 15-minute load of PG clusters is a good reference value. Through historical averages, peaks, and other statistics of this indicator, we can easily see which clusters are in high-load states requiring expansion and which clusters are in low resource utilization states requiring downsizing.

CPU utilization is another very important capacity evaluation indicator. We can see that PG Load has a very close relationship with CPU Usage. However, compared to CPU usage, PG Load more purely reflects the database's own load level, filtering out irrelevant loads on the machine and maintenance work (backup, cleanup, garbage collection) noise, making it smoother. Therefore, it's very suitable for capacity evaluation.

When system load is long-term at 30%~50%, expansion should be considered.

![](pg-load-cluster.png)

------

## 0x06 Conclusion

This article introduces a quantitative way to measure PG load: the PG Load indicator.

This indicator can simply and intuitively reflect database instance load levels.

This indicator is very suitable for capacity evaluation and can also serve as a core alerting indicator.

This indicator can basically ignore workload type and machine type for vertical historical comparison and horizontal utilization comparison.

This indicator can be calculated through simple methods: total active time of backend processes per second divided by available concurrency.

Data required for this indicator needs to be obtained from database middleware.

PG Load's 0 represents no load, 100% represents full load. Yellow line empirical value is 50%, red line empirical value is 70%.

PG Load is a good indicator 👍