---
title: "Golden Monitoring Metrics: Errors, Latency, Throughput, Saturation"
date: 2020-11-06
author: "vonng"
summary: >
  Understanding the golden monitoring metrics in PostgreSQL
tags: [PostgreSQL, PG Administration, Monitoring, Metrics]
---


----------------

## Preface

Playing with databases and playing with cars have something in common - they both require frequently checking the dashboard.

What are you doing staring at the dashboard? Looking at metrics. Why look at metrics? You need to understand the current operating state to effectively apply control.

![](img/blog/golden-metrics-car.jpeg)

Cars have many metrics: speed, tire pressure, torque, brake pad wear, various temperatures, and so on - all kinds of different ones.

But human attention span is limited, and the dashboard is only so big.

So, metrics can be divided into two categories:

* **Ones you will look at**: **Golden metrics / Key metrics / Core metrics**
* **Ones you won't look at**: Black box metrics / Cold metrics

Golden metrics are those few critical core data points that need constant attention (or have an autopilot system/alarm system maintain constant attention for you), while cold metrics are usually only looked at during troubleshooting. Troubleshooting and post-mortems require restoring the scene as much as possible, so the more black box metrics the better. It's very frustrating when you need them but don't have them.

Today let's talk about PostgreSQL's core metrics. What are the core metrics for databases?


----------------

## Database Metrics

Before discussing database core metrics, let's take a look at what metrics are available.

```
avg(count by (ins) ({__name__=~"pg.*"}))
avg(count by (ins) ({__name__=~"node.*"}))
```

Over 1000 PostgreSQL metrics, over 2000 machine metrics.

These metrics are all data treasures, and mining and visualization can extract their value.

But for daily management, only a few core metrics are needed.

With thousands of available metrics, which ones are the core metrics?



----------------

## Core Metrics

Based on experience and usage frequency, continuously subtracting, we can filter out some core metrics:

| Metric | Abbreviation | Level | Source | Type |
|--------|-------------|-------|--------|------|
| Error Log Count | Error Count | SYS/DB/APP | Log System | Error |
| **Connection Pool Queue** | Queue Clients | DB | Connection Pool | Error |
| **Database Load** | PG Load | DB | Connection Pool | Saturation |
| **Database Saturation** | PG Saturation | DB | Connection Pool & Node | Saturation |
| **Master-Slave Replication Lag** | Repl Lag | DB | Database | Latency |
| **Average Query Response Time** | Query RT | DB | Connection Pool | Latency |
| **Active Backend Processes** | Backends | DB | Database | Saturation |
| **Database Age** | Age | DB | Database | Saturation |
| **Queries Per Second** | QPS | **APP** | Connection Pool | Traffic |
| **CPU Usage** | CPU Usage | SYS | Machine Node | Saturation |

In emergency situations: Errors are always the first priority golden metric.

In normal situations: Application perspective golden metrics: QPS and RT

In normal situations: DBA perspective golden metrics: DB saturation (water level)



----------------

## Why These?

### **Error Metrics**

The first priority metrics are always **errors** - errors are often directly user-facing.

If you could only choose one metric to monitor, then choose **error metrics** - like the number of error log entries per second at the application, system, and DB layers might be most appropriate.

For a car, if you could only choose one function on the dashboard, what would you choose?

Choose **error metrics** - keep the car moving.

Error-type metrics are very important and directly reflect system anomalies, such as connection pool queuing. But the biggest problem with error-type metrics is they're only meaningful when alerting, making them difficult to use for daily water level assessment and performance analysis. Additionally, error-type metrics are often difficult to quantify precisely and can usually only give qualitative results: problematic vs not problematic.

Furthermore, error-type metrics are difficult to quantify precisely. We can only say: when the connection pool has queuing, database load is relatively high; the longer the queue, the higher the load; when there's no queuing, database load isn't very high - that's all. For daily management, this capability is definitely insufficient.

**An important reason for setting metrics and building monitoring/alerting systems is to prevent system overload. If the system is already overloaded with lots of errors, then using error phenomena to define saturation in reverse is meaningless**.

The purpose of metrics is to measure the system's operating state. We also care about other aspects of system capability: throughput/traffic, response time/latency, saturation/utilization/water level. These three represent system capability, service quality, and load level respectively.

Different focus points - backends (database users) focus on system capability and service quality, DBAs (database administrators) focus more on system load level.



### **Traffic Metrics**

Traffic-type metrics have great potential, especially metrics like QPS and TPS which are quite representative.

Traffic metrics can directly measure system capability, such as how many orders processed per second, how many requests processed per second.

This is similar to a speedometer - highway speed limits, city speed limits. Environment, load.

But traffic metrics like TPS and QPS also have problems. Queries on a database instance are often varied and diverse. A query taking 10 microseconds and one taking 10 seconds are both counted as one Q in statistics. **Metrics like QPS cannot be compared horizontally and only have rough reference value**. Even when query types change, they can't be compared vertically with their own historical data. It's also difficult to set utilization targets for metrics like QPS and TPS. The same database executing `SELECT 1` can reach hundreds of thousands of QPS, but when executing complex SQL, it might only reach thousands of QPS. Different load types and machine hardware will significantly impact a database's QPS ceiling. QPS only has reference value when queries on a database are highly homogeneous with no complex changes. Under such strict conditions, you can set a QPS water level target through stress testing.



### **Latency Metrics**

Similar to gear levels - slow queries, low gear, slow speed. Low query tier, low TPS water level. High query tier, high TPS water level.

Latency is suitable for measuring system service quality.

Compared to QPS/TPS, metrics like RT (Response Time) actually have more reference value. Because increased response time is often a precursor to system saturation. According to empirical rules, the higher the database load, the higher the average response time for queries and transactions. An advantage of RT over QPS is that **RT can have a utilization target set** - for example, you can set an absolute threshold for RT: not allowing slow queries with RT over 1ms in production OLTP databases. But metrics like QPS are difficult to draw red lines for. However, RT also has its own problems. The first problem is it's still qualitative rather than quantitative - increased latency is just a warning of system saturation but can't be used to precisely measure system saturation. The second problem is that RT statistics available from databases and middleware are usually averages, but what really provides warning effect might be statistics like P99 and P999.



### **Saturation Metrics**

Saturation metrics are like a car's tachometer, fuel gauge, and temperature gauge.

Saturation metrics are suitable for measuring system load.

The load metric users expect is a **saturation** metric. So-called saturation is how "full" the service capacity is - usually a measure of a specific metric of the currently most limited resource in the system. Generally, 0% saturation means the system is completely idle, 100% saturation means full load. Systems will experience severe performance degradation before reaching 100% utilization, so setting metrics also needs to include a **utilization target** or **water level red line and yellow line**. When system instantaneous load exceeds the red line, it should trigger alerts; when long-term load exceeds the yellow line, it should trigger capacity expansion.

| **Other Optional Metrics** | | | | |
|------------|-----------|-----|------|-----|
| Transactions Per Second | TPS | APP | Connection Pool | Traffic |
| Disk IO Usage | Disk Usage | SYS | Machine Node | Saturation |
| Memory Usage | Mem Usage | SYS | Machine Node | Saturation |
| Network Bandwidth Usage | Net Usage | SYS | Machine Node | Saturation |
| TCP Errors: Overflow/Retransmission | TCP ERROR | SYS | Machine Node | Error |