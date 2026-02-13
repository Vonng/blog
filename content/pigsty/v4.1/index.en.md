---
title: "Pigsty v4.1: Speed Is the Moat"
linkTitle: "Speed Is the Moat"
date: 2026-02-12
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/) | [Release](https://github.com/pgsty/pigsty/releases/tag/v4.1.0))
summary: >
  Same-day production support for PG 18.2 is the core message of Pigsty v4.1.
  In this cycle, very few vendors shipped day-zero readiness: AWS RDS, EDB, and Pigsty were among them.
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v4.1.0) | [**Release Note**](https://pigsty.io/docs/about/release/#v410)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v4.1.0)


If there is one takeaway from this release, it is that **speed matters**. 
On February 12, 2026, the PostgreSQL community released [18.2 / 17.8 / 16.12 / 15.16 / 14.21](https://www.postgresql.org/about/news/postgresql-182-178-1612-1516-and-1421-released-3235/) on the regular minor cadence.
As far as I could tell, the teams with production-grade support ready on the same day included **AWS RDS**, **EDB**, and **Pigsty**.

For an independent open-source project to keep pace with the world's largest cloud vendor
and a long-standing PostgreSQL leader -- that is the story I hope v4.1 can tell.

------

## Why Speed Matters So Much

After years of building a database distribution, one lesson keeps coming back: what users need most is not more features -- it is confidence that the project will be there when it counts.

Where does that confidence come from? Less from feature lists, and more from showing up reliably at the moments that matter. PostgreSQL minor releases carry bug fixes, stability improvements, and security patches. They are not optional upgrades. Every day of delay is another day users remain exposed.

In practice, many distributions follow a well-known pattern: upstream ships, internal testing begins, packaging takes a while, and a couple of months later a blog post announces support for the latest version.
By that point, users who needed the update have often already upgraded on their own. "Support" can end up feeling more like a formality than meaningful protection.

The experience I would love to provide is the opposite: follow-up so prompt that users never have to worry about it.
PostgreSQL ships a new release, you reach for Pigsty, and it is already there. That is the standard a distribution should aspire to.

So the theme of v4.1 is not "more features." It is about turning fast, reliable delivery into a repeatable capability -- not a one-time heroic sprint, but a steady engineering discipline.

------

## Not Just PostgreSQL: OS Minors Move Together

Being fast is one thing; being fast *and* correct is another. This round covers more than PostgreSQL minor upgrades -- we also advanced the Linux distro minor baselines:

- **EL**: `9.6/10.0 -> 9.7/10.1`
- **Debian**: `12.12/13.1 -> 12.13/13.3`

We prepared offline packages for the latest minor versions across 14 mainstream Linux distros.

One important note to keep in mind:

> **Offline packages for EL 9.7 / 10.1 are NOT compatible with EL 9.6 / 10.0.**

Many users deploy in intranet or fully air-gapped environments. If package versions do not match, online installation is the safe fallback.

------

## Pig Agent-Native CLI: Letting The Tool Speak for Itself

Here is a practical example: imagine asking Claude Code to install PostgreSQL 18 plus extensions on three machines.
When it calls [**pig**](https://github.com/pgsty/pig), you do not need to craft prompts explaining how `pig` works -- `pig` can describe itself to the agent directly. That is the idea behind Agent-Native design.

Traditional CLI tools are built for a human sitting at a terminal: colored output, formatted tables, progress bars. All great for people, but not ideal for agents. What agents really need are three things:

- **What the tool can do**: capabilities described explicitly, rather than requiring the agent to guess or parse documentation.
- **What it did**: execution results returned as structured JSON/YAML, not free-form text that requires regex parsing.
- **What context it sees**: environment information that is programmatically discoverable and transferable.

These principles sound straightforward, but applying them properly meant revisiting every subcommand. In `pig 1.1.0`, JSON/YAML output is no longer an afterthought; it is a first-class interface so that every operation can be invoked and parsed reliably by machines.

In the spirit of transparency: I proposed the concept and participated in design reviews, but the bulk of the implementation was carried out with the help of Codex and Claude Code. I handled the final review and acceptance. This is also Pigsty's first truly AI-native project.

------

## AI Coding: Less About Writing Code, More About Sweeping Blind Spots

During v4.1, I spent a good deal of time on `pig` and `pg_exporter`, leaning heavily on AI coding tools for review -- mainly Claude Code and Codex 5.3 Extra High.

The real value is not that "AI is magical." It is something more mundane but genuinely useful: **blind-spot sweeping**.

In mature systems, the most dangerous bugs are rarely obvious logic failures. The tricky ones are details that look fine, run fine, and only break at specific boundaries.
For example, a metric unit that differs between PG17 and PG18, or an `io_method` version guard written as `>= 17` when it should be `>= 18`.

We all miss things like these -- our eyes tend to glide over code that "looks right."
AI tooling is surprisingly good at catching them. It will methodically work through every line, especially when given targeted prompts like "verify version guards."

In this cycle, that kind of sweep surfaced and fixed roughly 10 to 20 additional issues. Each one is small on its own, but the cumulative effect is something users can feel.

A special thank you to community contributor [@l2dy](https://github.com/l2dy) for many thoughtful issues that helped us close a batch of dashboard and config edge cases. This is how open-source quality compounds -- through people who care about the details.

------

## Firewall Defaults: One Extra Command Is Better Than a Silent Risk

A small but important change: in v4.0, the default firewall mode was set to `none`, meaning "do not touch your firewall."
The intention was reasonable, but user feedback made it clear this was not the right call.

EL9 enables `firewalld` by default, and many users are not fully aware of their current firewall state.
When Pigsty takes the hands-off approach, users tend to assume everything is fine -- only to discover later that intra-network traffic is blocked, spending hours debugging mismatched rules. That experience is worse than a bit of upfront configuration.

So in v4.1, the default returns to `zone`, with a straightforward policy:

- Trust private network CIDRs by default.
- On public networks, open only `22` (SSH), `80` (HTTP), and `443` (HTTPS).
- Database port `5432` is **no longer exposed publicly by default**.

If you need public database access, you can add it explicitly. It may mean one extra command in some cases, but when it comes to security defaults, we believe a conservative approach is the safer choice.

------

## Seven New Extensions, Now 451 in Total

Every release brings updates to the extension ecosystem. This time we added 7, bringing total support to **451**. A few highlights:

- **pg_track_optimizer** `0.9.1`: automatic index tracking and optimization recommendations.
- **nominatim_fdw** `1.1.0`: OpenStreetMap geocoding FDW, useful for GIS workloads.
- **pg_utl_smtp** `1.0.0`: send email directly from PostgreSQL, familiar to Oracle migration users.
- **pg_strict** `1.0.2`: strict mode guardrails to avoid unqualified UPDATE/DELETE.

Meanwhile, TimescaleDB moved to 2.25.0, Citus 14.0.0 landed, and Postgres Anonymizer reached 3.0 -- all meaningful updates in their respective domains.

------

## Other Notable Changes

Here are a few more changes worth highlighting:

- **Autovacuum thresholds tuned**: raised `autovacuum_vacuum_threshold` from 50 to 500 and `analyze_threshold` from 50 to 250 in `oltp/crit/tiny`. This reduces noisy vacuum/analyze churn for many small tables (common in multi-tenant systems).
- **FD limit chain unified**: fixed hierarchy between `fs.nr_open` and `LimitNOFILE`, unified at 8M to avoid high-concurrency FD exhaustion caused by inconsistent kernel/systemd settings.
- **`checkpoint_completion_target`**: increased from 0.90 to 0.95 for smoother IO distribution and less checkpoint jitter.
- **Vibe defaults adjusted**: Jupyter is now off by default (since most users do not need it), and Claude Code is managed consistently via npm packages.
- **`infra-rm` refactor**: uninstall flow now includes segmented `deregister` cleanup instead of one-shot removal, so cleanup scope and order are easier to control.
- **New Mattermost app template**: one-click deployment with database, storage, and reverse proxy wiring.

------

## Closing

v4.1 is not a big-bang release. There is no architecture rewrite, no dramatic new module. But it demonstrates something we think matters: day-zero production-grade support is not a lucky sprint -- it can be a repeatable engineering capability.

Earlier I mentioned that users need confidence. That kind of trust is not built in a single moment. It is earned with every minor release, every security patch, every time you show up on schedule. v4.1 is one more step in that direction.
Below are the full commit notes and technical details.

--------

## v4.1.0 Commit Note

```bash
curl https://pigsty.io/get | bash -s v4.1.0
```

**72 commits**, 252 files changed, +5,744 / -5,015 lines (`v4.0.0..v4.1.0`, 2026-02-02 ~ 2026-02-13)

### Highlights

- Added 7 new extensions, total support reaches **451**.
- `pig` moved to an **Agent-Native CLI** (`1.0.0 -> 1.1.0`) with explicit context and JSON/YAML outputs.
- Unified PostgreSQL/OS **major/minor upgrade** workflows.
- `pg_exporter` upgraded to **v1.2.0** (`1.1.2 -> 1.2.0`) with PG17/18 metric and unit fixes.
- Default firewall policy tightened: `node_firewall_mode=zone`, `node_firewall_public_port=[22,80,443]`.
- PostgreSQL minor updates: 18.2, 17.8, 16.12, 15.16, 14.21.
- Default EL minors bumped to `9.7 / 10.1`, Debian minors to `12.13 / 13.3`.
- New one-click Mattermost app template with optional PGFS/JuiceFS.
- Refactored `infra-rm` with segmented `deregister` cleanup.
- Tuned autovacuum defaults and NOFILE chain consistency.

### Version Updates

- Pigsty: `v4.0.0 -> v4.1.0`
- `pig` CLI: `1.0.0 -> 1.1.0`
- `pg_exporter`: `1.1.2 -> 1.2.0`
- Default EL minors: `9.6/10.0 -> 9.7/10.1`
- Default Debian minors: `12.12/13.1 -> 12.13/13.3`

### Extension Updates

- [RPM Changelog 2026-02-12](https://pigsty.io/docs/repo/pgsql/rpm/#2026-02-12)
- [DEB Changelog 2026-02-12](https://pigsty.io/docs/repo/pgsql/deb/#2026-02-12)
- timescaledb `2.24.0 -> 2.25.0`
- pg_search `0.21.4 -> 0.21.7`
- pgmq `1.9.0 -> 1.10.0`
- pg_textsearch `0.4.0 -> 0.5.0`
- pljs `1.0.4 -> 1.0.5`
- pg_track_optimizer `0.9.1` (new)
- nominatim_fdw `1.1.0` (new)
- pg_utl_smtp `1.0.0` (new)
- pg_strict `1.0.2` (new)
- pgmb `1.0.0` (new)
- pg_pwhash (new support)
- informix_fdw (new support)

### API Changes

- Corrected `io_method` / `io_workers` template guard from `pg_version >= 17` to `pg_version >= 18`.
- Fixed PG18 guards for `idle_replication_slot_timeout` / `initdb --no-data-checksums`.
- Broadened `maintenance_io_concurrency` effective range to `PG13+`.
- Raised autovacuum thresholds for `oltp/crit/tiny/olap` profiles.
- Increased default `checkpoint_completion_target` from `0.90` to `0.95`.
- Added `fs.nr_open: 8388608` into defaults and aligned NOFILE chain.
- Changed firewall defaults: `node_firewall_mode=zone`, public ports `[22,80,443]`.
- Added validation support for `pg_databases[*].parameters` and `pg_hba_rules[*].order`.
- Added segmented tags in `infra-rm.yml`: `deregister`, `config`, `env`.
- Updated VIBE defaults and npm package set.
- PgBouncer alias cleanup: `pool_size_reserve -> pool_reserve`, `pool_max_db_conn -> pool_connlimit`.

### Compatibility Fixes (Grouped)

- Redis `replicaof` guard and systemd stop behavior.
- `pg_migration` identifier qualification, quoting, and logging safety.
- pgsql role handler restart target and variable usage fixes.
- blackbox cleanup naming and pgAdmin pgpass format fix.
- Non-blocking `pg_exporter` startup.
- VIP parsing simplification (default mask `24`).
- MinIO health-check retry bump (`3 -> 5`).
- Hostname setup switched to Ansible hostname module.
- `.env` normalization to `KEY=VALUE` in selected app templates.
- `pg_crontab` syntax fix in `pigsty.yml`.
- ETCD TLS/mTLS docs clarification.
- `repo-add`, Debian CN mirror compatibility, and Python 3 compatibility fixes.
- redis-exporter credential permission hardening.
- Sensitive credential logs masked in `pgsql-user.yml`.
- `pg_monitor` Victoria registration gate fixes.
- Cluster-scoped backup cleanup in `pg_remove`.

### Selected Commits

```text
7410de401 v4.1.0 release
fa31213ce conf(node): default firewall to zone with single-node 5432 override
bb8382c58 update default extension list to 451
770d01959 hide user credential in pgsql-user playbook
7219a896c pg_monitor: fix victoria registration gate conditions
7005617f1 pgsql: drop legacy pgbouncer pool parameter aliases
74c59aabe grafana: fix dashboard links, descriptions, and overrides
36c95c749 fix(cli): restore repo-add execution and HBA validation failure propagation
6f2576fd0 fix(node): set default fs.nr_open via node_sysctl_params
26e108788 fix(monitor): correct unit for time metrics scaled by pg_exporter
d439464b2 pgsql: fix pg_version guards for PG18-only settings
cb52375ac bump checkpoint_completion_target from 0.90 to 0.95
c402f0e6d fix: correct io_method/io_workers version guard from PG17 to PG18
3bf676546 vibe: disable jupyter by default and install claude-code via npm_packages
613c4efa9 fix: set fs.nr_open in tuned profiles and reduce LimitNOFILE to 8M
4cc68ed61 refine infra removal playbook
318d85e6e simplify VIP parsing and make pg_exporter non-blocking
4bff01100 fix redis replicaof guard and systemd stop
38445b68d minio: increase health check retries
a237e6c99 tune autovacuum threshold to reduce small table vacuum frequency
```

For the full 72-commit list, see the GitHub release page.

### Thanks

- Thanks to [@l2dy](https://github.com/l2dy) for valuable suggestions and issues.

### Checksums

```bash
8bc75e8df0e3830931f2ddab71b89630  pigsty-v4.1.0.tgz
da10de99d819421630f430d01bc9de62  pigsty-pkg-v4.1.0.d12.aarch64.tgz
e1f2ed2da0d6b8c360f9fa2faaa7e175  pigsty-pkg-v4.1.0.d12.x86_64.tgz
382bb38a81c138b1b3e7c194211c2138  pigsty-pkg-v4.1.0.d13.aarch64.tgz
13ceaa728901cc4202687f03d25f1479  pigsty-pkg-v4.1.0.d13.x86_64.tgz
92d061de4d495d05d42f91e4283e7502  pigsty-pkg-v4.1.0.el10.aarch64.tgz
be629ea91adf86bbd7e1c59b659d0069  pigsty-pkg-v4.1.0.el10.x86_64.tgz
c14be706119ba33dd06c71dda6c02298  pigsty-pkg-v4.1.0.el8.aarch64.tgz
0c8b6952ffc00e3b169896129ea39184  pigsty-pkg-v4.1.0.el8.x86_64.tgz
cfcc63b9ecc525165674f58f9365aa19  pigsty-pkg-v4.1.0.el9.aarch64.tgz
34f733080bfa9c8515d1573c35f3e870  pigsty-pkg-v4.1.0.el9.x86_64.tgz
ad52ce9bf25e4d834e55873b3f9ada51  pigsty-pkg-v4.1.0.u22.aarch64.tgz
300b2185c61a03ea7733248e526f3342  pigsty-pkg-v4.1.0.u22.x86_64.tgz
2e561e6ae9abb14796872059d2f694a8  pigsty-pkg-v4.1.0.u24.aarch64.tgz
c462bb4cb2359e771ffcad006888fbd4  pigsty-pkg-v4.1.0.u24.x86_64.tgz
```
