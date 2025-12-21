---
title: "Pigsty v0.3: First Public Beta"
linkTitle: "Pigsty v0.3 Release Notes"
date: 2020-10-24
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v0.3.0)）
summary: >
  Pigsty v0.3.0, the first public beta, lands with eight battle-tested dashboards and an offline bundle.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v0.3.0

Pigsty v0.3.0 is the very first public preview. It packages a lean observability stack plus a reproducible offline bundle so you can spin up a real PostgreSQL lab without touching the public Internet.

## Observability Stack

The open build ships eight curated Grafana dashboards: PG Overview, Cluster, Service, Instance, Database, Table Overview, Table Catalog, and a bare-metal Node view. Even with a trimmed set the coverage still crushes most "enterprise" monitoring stories.

## Offline Bundle

Shipyard environments can fetch the CentOS 7.8 offline bundle directly from GitHub (`pkg.tgz`). Drop it on the management node and you have a deterministic install no matter how broken the mirrors are.
