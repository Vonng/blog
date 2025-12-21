---
title: "Victoria: The Observability Stack That Slaps the Industry"
linkTitle: "Victoria: Observability Stack Arrives"
date: 2025-12-17
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat](https://mp.weixin.qq.com/s/RLN0DMzfvSibkGgq2VRcoQ)
summary: >
  VictoriaMetrics is brutally efficient—using a fraction of Prometheus + Loki’s resources for multiples of the performance. Pigsty v4 swaps to the Victoria stack; here’s the beta for anyone eager to try it.
tags: [Victoria,Observability]
---

I’ve spent the last few weeks preparing Pigsty v4.0. The headliner: ripping out Prometheus + Loki and dropping in the full Victoria stack. **VictoriaMetrics is no-frills brute force**—it just works and it’s ridiculous. The observability portion is done, so here’s a beta for early testers.


--------

## First impressions

Maybe you haven’t heard of VictoriaMetrics, but you definitely know Prometheus. Victoria is Prometheus’ big brother—built by Belarusian wizard Aliaksandr Valialkin. Back at Tantan we tracked ~50 M time series using twelve 64C/256G nodes of Prometheus. I swapped in a three-node distributed Victoria cluster and it didn’t even break a sweat. Later tests showed a single beefy node could handle it. Memory/disk dropped to **¼** of Prometheus; query speed jumped **4×**. It blew me away.

Industry benchmarks back it up. VM routinely crushes InfluxDB, Prometheus, TimescaleDB in ingestion throughput and high-cardinality queries.

![benchmark-comparison.png](benchmark-comparison.png)

Pigsty used to ship Prometheus by default and keep VM as a “pro” module. Two things pushed me to refactor:

1. Grafana Loki/Promtail were aging out. VictoriaLogs was the obvious replacement.
2. A customer (the film studio behind *Movie Hurricane*) needed production-grade Victoria. I decided to redo the entire infra layer.

Victoria is a full suite: metrics, logs, traces. So Pigsty v4 rewrites the infra module accordingly.

--------

## Why Victoria?

Before performance, let’s talk about the man behind it — Aliaksandr Valialkin (@valyala). Before Victoria he was CTO at ad-tech shop VertaMedia. In Go circles he’s legendary.
His **fasthttp** has 23k stars and is **10×** faster than net/http (150M concurrent connections, 200k RPS). His **quicktemplate** is **20×** faster than html/template; **fastjson** beats encoding/json by **15×**.

Common thread: **zero allocations on the hot path**. That philosophy permeates Victoria. No third-party deps, ruthless memory management, 
simple architecture with AK‑47 reliability. He also has the swagger to back it up: he publishes benchmarks that faceplant competitors and never blinks.


--------

## How strong is Victoria?

We tested on ten nodes ingesting all metrics/logs. Pigsty v4’s VictoriaMetrics + VictoriaLogs consumed 0.2 vCPU and 1GB RAM for the entire stack (Grafana, Alertmanager included). Daily load: 120k time series in 600 MB RAM, 1.1B samples in 440MB storage, 500k log lines in under 6MB.

![victoria-metrics-stats.png](victoria-metrics-stats.png)

![resource-usage-overview.png](resource-usage-overview.png)

For comparison, Pigsty v3.7 on the same ten nodes with Prometheus + Loki ate about the same resources in just ten hours—data volume too small to highlight the disparity, but it scales horribly.

![prometheus-loki-comparison.png](prometheus-loki-comparison.png)

Victoria won’t just sip resources—it’s faster queries, better compression, higher cardinality tolerance, and effortless clustering.


--------

## Architecture

Pigsty v4 builds a fully distributed Victoria setup: separate ingest/query nodes, replication, HA, plus VictoriaLogs and VictoriaTraces. The stack exposes Grafana dashboards, Alertmanager routes, Nginx ingress, and integrates with existing host/DB exporters.

![nginx-services-architecture.png](nginx-services-architecture.png)

Even self-monitoring is wired up, and adding your own app metrics is a matter of dropping in config files.

![self-monitoring-dashboard.png](self-monitoring-dashboard.png)

Pigsty is no longer just a PostgreSQL distro—it’s now an observability distro too.


--------

## Getting started

We introduced `infra.yml`, which installs only the Victoria stack (no PostgreSQL/Etcd). Want pure Victoria on any mainstream Linux? Run:

```bash
curl https://repo.pigsty.cc/beta | bash
./configure -c infra
./infra.yml
```

The config is straightforward; add more nodes or replicas as needed.

![infra-config-example.png](infra-config-example.png)

Everything bootstraps itself:

![installation-complete.png](installation-complete.png)

A three-node install gives three independent replicas out of the box:

![three-node-cluster.png](three-node-cluster.png)

Pigsty v4 is still beta, but the Victoria portion is rock solid. Remaining work is dashboard polish and docs. If you want the easiest way to try Victoria, this is it.

v4.0 stable ships January 2026 with full docs and additional features, including Victoria’s native distributed mode.


--------

## Final thoughts

Upgrading to Victoria benefited me directly. Opening Grafana and having sub-second, buttery-smooth queries is pure joy. Remember waiting seconds for Loki searches? Never again.

VictoriaMetrics embodies the purest form of open source: a lone expert ships something that dunks on industry giants, releases it under a permissive license, and doesn’t play licensing shell games. No VC puppet strings, no bait-and-switch—just product excellence. More people should know about it and use it.
