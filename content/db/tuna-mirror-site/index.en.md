---
title: On Trusting Open-Source Supply Chains
date: 2025-11-22
author: |
  Feng Ruohang
summary: >
  In serious production you can’t rely on an upstream that explicitly says “no guarantees.” When someone says “don’t count on me,” the right answer is “then I’ll run it myself.”
tags: [Open-Source, Supply Chain]
---

Yesterday’s post “[PG ‘Export Controls’ and Supply-Chain Trust](/en/pg/pg-mirror-pigsty/)” drew a comment from someone claiming to be an admin at a university mirror site (Tsinghua TUNA):

> “As a university mirror admin, calling us ‘lying flat’ or ‘irresponsible’ is unfair and demoralizing.”

![comment.png](comment.png)

I replied:

> Thanks for the feedback and for everything TUNA/university mirrors have done over the years. I see the PostgreSQL repo [has synced again](https://mirrors.tuna.tsinghua.edu.cn/postgresql/repos/yum/18/)—credit where it’s due.
> 
> When I first spotted the issue I was using Alibaba-Cloud’s PG mirror. Later I noticed TUNA was in the same state, so out of community duty I [reported it on the mailing list](https://groups.google.com/g/tuna-general/c/BU8P7X3y4sI) and got “this list isn’t for Alibaba” followed by silence. That context colors my tone.
> 
> In hindsight, words like “lying flat” were too emotional—especially when applied to **your team**—and read like moral judgments on volunteers. That wasn’t my intent. If the wording hurt maintainers, I apologize. I already [changed the language](https://github.com/Vonng/blog/commit/916697a88f143679d658dc52338827ce603444fd) to neutral phrasing like “stale” or “no longer maintained.”
> 
> You’re right: university mirrors are volunteer efforts with no contractual SLA. There’s nothing to “demand.” But from a downstream perspective, when PGDG cuts rsync and major domestic mirrors stall for months, users depending on “recommended mirrors” experience a supply-chain outage. Trust erodes.
> 
> My takeaway: if there’s no service promise, treating a volunteer mirror as production infrastructure is a mistake. My own fix is to stop relying on external mirrors altogether—Pigsty now mirrors PGDG ourselves. Your perspective helps others understand what mirrors can and can’t do, which is valuable.

## My reflections

I checked TUNA again—PG 18 packages are there, though “Last Update” still shows 2025-05-16, so it was probably a manual sync. That’s great news: aside from Pigsty’s [PGEXT Cloud](https://pgext.cloud), we now have another local node with reasonably fresh PGDG content.

![tuna.png](tuna.png)

Pigsty originally pointed at Alibaba’s mirror, not TUNA. My “lying flat” rant was aimed mostly at a well-funded company doing the bare minimum—classic [Cloud Mudslide](https://vonng.com/cloud) material. Alibaba reaps enormous value from PostgreSQL yet let the repo rot. Ironically, it was the TUNA folks who responded, which I understand.

![aliyun.png](aliyun.png)

To be fair: neither Alibaba nor TUNA owes anyone anything. I said that repeatedly in the original piece. Free services don’t come with legal or moral obligations. But that doesn’t stop people from reacting to outcomes. Calling it “lying flat” was my subjective frustration—misplaced when applied to university volunteers, so I toned it down.

Why the frustration? When I noticed the [global sync breakage](/en/pg/pg-mirror-break), I immediately [emailed Alibaba](/en/pg/pg-mirror-pigsty) (still unresolved). I also checked other domestic mirrors and saw TUNA stuck, so I sent the same heads-up. The only reply was “not our business.” Months passed, nothing changed, and the repo remained outdated. From a downstream point of view, the mirror was effectively dead.

When you’re running mission-critical systems, you can’t depend on an upstream saying “no guarantees.” The right response to “don’t count on me” is “fine, I’ll run my own supply chain.”

Pigsty now ships everything from our own repo:

- Full PostgreSQL releases
- 450+ extensions for EL9, EL8, Debian 12, Ubuntu 22/24
- Ecosystem packages: IvorySQL, FerretDB, TigerBeetle, JuiceFS, Kafka, DuckDB, MinIO, etc.
- Observability stack: Prometheus, VictoriaMetrics, Grafana, Loki, exporters
- Utilities: Sealos, rclone, restic, sqlcmd, genai-toolbox, etc.

(See the table at the end of this article for full lists.)

Trust is earned. You can’t offload that responsibility to someone who told you, up front, “this is best effort.”

![pigsty.png](pigsty.png)

### Lessons

1. **Volunteers aren’t your SLA.** University mirrors are goodwill projects. Treating them as production vendors is unfair to them and dangerous for you.
2. **Corporate mirrors should do better.** If a hyperscaler profits from open source, it should keep its public mirrors current or shut them down.
3. **If trust matters, self-host.** Mirror what you need, automate the sync, and monitor it.

Below is the current snapshot of what Pigsty mirrors (PostgreSQL ecosystem, observability stack, and tooling). When someone asks “where do you get your packages?” I can point at a repo we control end to end.

| **DBMS** | | **Prometheus stack** | | **Grafana/Observability** | |
|:--:|:--:|:--:|:--:|:--:|:--:|
| [IvorySQL](https://github.com/IvorySQL/IvorySQL) 4.6 | | [prometheus](https://github.com/prometheus/prometheus) 3.7.3 | | [grafana](https://github.com/grafana/grafana/) 12.3.0 | |
| [etcd](https://github.com/etcd-io/etcd) 3.6.6 | | [pushgateway](https://github.com/prometheus/pushgateway) 1.11.2 | | [loki](https://github.com/grafana/loki) 3.1.1 | |
| [minio](https://github.com/minio/minio) 20250907161309 | | [alertmanager](https://github.com/prometheus/alertmanager) 0.29.0 | | [promtail](https://github.com/grafana/loki/releases/tag/v3.0.0) 3.0.0 | |
| [mc](https://github.com/minio/mc) 20250813083541 | | [blackbox_exporter](https://github.com/prometheus/blackbox_exporter) 0.27.0 | | [vector](https://github.com/vectordotdev/vector/releases) 0.51.1 | |
| [Kafka](https://kafka.apache.org/downloads) 4.0.0 | | [VictoriaMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics) 1.129.1 | | [grafana-infinity-ds](https://github.com/grafana/grafana-infinity-datasource/) 3.6.0 | |
| [DuckDB](https://github.com/duckdb/duckdb) 1.4.2 | | [VictoriaLogs](https://github.com/VictoriaMetrics/VictoriaMetrics/releases) 1.37.2 | | [grafana-vmlogs](https://github.com/VictoriaMetrics/victorialogs-datasource/releases/) 0.21.4 | |
| [FerretDB](https://github.com/FerretDB/FerretDB) 2.7.0 | | [pg_exporter](https://github.com/Vonng/pg_exporter) 1.0.3 | | [grafana-vmetrics](https://github.com/VictoriaMetrics/victoriametrics-datasource/releases/) 0.19.6 | |
| [TigerBeetle](https://github.com/tigerbeetle/tigerbeetle) 0.16.60 | | [pgbackrest_exporter](https://github.com/woblerr/pgbackrest_exporter) 0.21.0 | | [grafana-plugins](https://github.com/pgsty/infra-pkg/tree/main/noarch/grafana-plugins) 12.0.0 | |
| [JuiceFS](https://github.com/juicedata/juicefs) 1.3.0 | | [node_exporter](https://github.com/prometheus/node_exporter) 1.10.2 | | **Utils** | |
| [dblab](https://github.com/danvergara/dblab) 0.34.2 | | [keepalived_exporter](https://github.com/mehdy/keepalived-exporter) 1.7.0 | | [Sealos](https://github.com/labring/sealos) 5.1.1 | |
| [v2ray](https://github.com/v2fly/v2ray-core) 5.28.0 | | [nginx_exporter](https://github.com/nginxinc/nginx-prometheus-exporter) 1.5.1 | | [rclone](https://github.com/rclone/rclone/releases/) 1.71.2 | |
| [pig](https://github.com/pgsty/pig) 0.7.2 | | [zfs_exporter](https://github.com/waitingsong/zfs_exporter/releases/) 3.8.1 | | [restic](https://github.com/restic/restic) 0.18.1 | |
| [vip-manager](https://github.com/cybertec-postgresql/vip-manager) 4.0.0 | | [mysqld_exporter](https://github.com/prometheus/mysqld_exporter) 0.18.0 | | [mtail](https://github.com/google/mtail) 3.0.8 | |
| [pev2](https://github.com/pgsty/infra-pkg/tree/main/noarch/pev2) 1.17.0 | | [redis_exporter](https://github.com/oliver006/redis_exporter) 1.80.0 | | [genai-toolbox](https://github.com/googleapis/genai-toolbox) 0.18.0 | |
| [promscale](https://github.com/timescale/promscale) 0.17.0 | | [kafka_exporter](https://github.com/danielqsj/kafka_exporter) 1.9.0 | | [sqlcmd](https://github.com/microsoft/go-sqlcmd) 1.8.0 | |
| [pgschema](https://github.com/pgschema/pgschema) 1.4.2 | | [mongodb_exporter](https://github.com/percona/mongodb_exporter) 0.47.1 | | |
