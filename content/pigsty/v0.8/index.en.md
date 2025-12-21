---
title: "Pigsty v0.8: Service Provisioning"
linkTitle: "Pigsty v0.8 Release Notes"
date: 2021-03-16
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [Release Notes](https://github.com/pgsty/pigsty/releases/tag/v0.8.0)）
summary: >
  Services are now first-class objects, so you can define any routing policy—built-in HAProxy, L4 VIPs, or your own balancer.
series: [Pigsty]
tags: [Pigsty]
---

> GitHub Release: https://github.com/pgsty/pigsty/releases/tag/v0.8.0

v0.8 finalizes the provisioning API. Services are completely rebuilt: instead of a hard-coded primary/replica pair you can now declare any number of services, plug in HAProxy, swap in an external load balancer, or hand off to a custom VIP controller. Everything else in the supply chain stabilizes on top of this model.

## Service API

The old `vip` and `haproxy` knobs moved under the `service` role. `pg_services` (plus `pg_services_extra`) define each exposed endpoint—name, ports, selectors, health checks, weights, and balancer hints. Selectors are JMESPath filters over cluster members, and optional `selector_backup` pools handle fail-in when replicas are gone. Out of the box we ship `primary`, `replica`, `default`, and `offline` service definitions; swap `dst_port` to point at `postgres`, `pgbouncer`, or any number.

The HAProxy stanza keeps per-service tuning (maxconn, algorithm, timeouts) while VIP config distinguishes L2/L4 implementations so you can drop Pigsty behind an existing load balancer.

## Database Interface Tweaks

Locales can now be split into `lc_collate` and `lc_ctype` so extensions like `pg_trgm` behave with non-`C` collations. The rest of the `pg_databases` schema stays the same—owner/template/encoding/connlimit/revokeconn/pgbouncer/comment—just with better defaults and inline comments.
