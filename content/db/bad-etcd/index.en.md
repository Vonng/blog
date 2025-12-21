---
title: How Many Shops Has etcd Torched?
summary: "Plenty. If you’re rolling your own Kubernetes, odds are you’ll crash because etcd ships with a 2 GB time bomb."
date: 2025-05-07
tags: [数据库,etcd]
categories: [Blog]
---

A few days ago [Yingshi Hurricane shared their Pigsty/PostgreSQL HA incident](https://mp.weixin.qq.com/s/7zJe6_HJU7Q2_Uf9-lS2vQ). The root cause? etcd hit its default 2 GB limit because auto-compaction wasn’t enabled. As @ayanamist put it on X: “Let’s see how many companies this stupid 2 GB design can screw.”

etcd bills itself as “a distributed, reliable key-value store for the most critical configuration data.” Today it mostly underpins Kubernetes metadata. Patroni-style PG failover setups also use it as the DCS.

Judging by the replies under that X thread, tons of teams stumbled over the same landmine—mostly K8s users, plus a few PG HA deployments.

-------

## etcd’s facepalm defaults

In the default config, etcd dies after writing 2 GB. Every write creates a new version; once versions exceed 2 GB, etcd drops into maintenance mode (read: it’s down). It’s like running a Java VM without GC.

There *is* a fix: set auto-compaction to keep only recent revisions, e.g.

```yaml
auto-compaction-retention: "24h"
```

But the default is `0`, which means “retain everything forever.” And the docs are misleading. The [maintenance](https://etcd.io/docs/v3.4/op-guide/maintenance/) page cheerily says maintenance “can typically be automated without downtime.” The “Auto Compaction” section reads as if a sane default already exists—hourly cleanup, 10-hour retention. Unless you dig into the configuration reference, you’ll think you’re covered. You’re not.

Worse, the issue doesn’t show up immediately. It explodes months later, right when you’re least ready.

-------

## PostgreSQL had this problem too

Back in the 8.0 era (pre-2005), PostgreSQL had a similar issue. MVCC means every write creates a new version. Without cleanup, dead tuples pile up until the database chokes. For years DBAs had to run manual VACUUMs—an infamous pain point.

Postgres fixed it with autovacuum: background workers scan and reclaim junk automatically. On modern hardware, default settings rarely let bloat run wild. Not every database is as considerate. etcd is the stark counterexample.

-------

## Pigsty’s scar tissue

Pigsty shipped etcd as the DCS starting with v2.0.0 (2023‑02‑28). We didn’t patch the auto-compaction landmine until v2.6.0 (2024‑02‑13). That means an entire year of releases inherited the flaw. We call it out repeatedly in the docs: see the [Bug Log](/en/docs/bug/) and the [ETCD FAQ](/en/docs/etcd/faq/).

If you’re still on Pigsty v2.0–v2.5, update your etcd config now. Don’t wait for the 2 GB wall to punch you in the face.
