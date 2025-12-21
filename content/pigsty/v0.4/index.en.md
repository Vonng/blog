---
title: "Pigsty v0.4: PG13 and Better Docs"
linkTitle: "Pigsty v0.4 Release Notes"
date: 2020-12-14
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v0.4.0)）
summary: >
  Pigsty v0.4 ships PG13 support, a Grafana 7.3 refresh, and a cleaned-up docs site for the second public beta.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v0.4.0

Pigsty v0.4 is our second public beta. The observability stack was rebuilt around Grafana 7.3, and ten curated dashboards became the default open-source payload. pg_exporter 0.3.1 drives metrics, and the alert wiring has been cleaned up for the new Grafana release.

## Open-Source Dashboards

The OSS build now exposes ten high-signal Grafana panels: PG Overview, Cluster, Service, Instance, Database, Query, Table, Table Catalog, Table Detail, and Node. Even with a lean set it easily outclasses most “enterprise” PG monitoring suites.

## Software Refresh

- PostgreSQL 13.1 + Patroni 2.0.1-4, with citus added to the repo
- pg_exporter upgraded to 0.3.1
- Grafana jumps to 7.3; a ton of compatibility fixes landed
- Prometheus 2.23 with the new UI enabled
- Consul 1.9 and related components updated

## Other Improvements

- Updated Prometheus alert rules and Alertmanager info links
- Fixed a batch of bugs and typos
- Added a tiny backup script for quick dumps

## Offline Bundle

Need an air-gapped install? Grab the CentOS 7.8 package bundle (`pkg.tgz`) from GitHub and deploy from local media.
