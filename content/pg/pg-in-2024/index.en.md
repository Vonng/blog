---
title: Looking Ahead to PostgreSQL 2024
date: 2024-01-05
hero: /hero/pg-in-2024.jpg
showAuthor: false
author: |
  [Jonathan Katz](https://jkatz05.com/) | Translation: [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  PostgreSQL core member Jonathan Katz reflects on where PG is headed in 2024: availability, performance, developer features, community growth, and mentorship.
tags: [PostgreSQL,PG生态]
---

*(Translation of Jonathan Katz’s essay “PostgreSQL 2024.”)*

> **Author:** Jonathan Katz, Principal PM at Amazon RDS, PG core member.
> 
> **Translator’s note:** I’m Feng Ruohang, founder of Pigsty. Original post: https://jkatz05.com/post/postgres/postgresql-2024/

When people ask “Where is PostgreSQL going?” they rarely mean just internals. They mean the whole ecosystem: extensions, events, governance. PG just won DB-Engines “Database of the Year” for the fourth time, but we still need to step back and ask what’s next.

## Product focus

At PGCon 2023’s dev meeting we asked, “What challenges do our users face?” Three buckets emerged:

1. **Availability** – higher uptime expectations, zero-downtime upgrades, sub-second failovers, logical replication as the backbone for blue/green, multi-master, online migrations, and the need for better tooling (pgcopydb, pg_basebackup PQ formats) to support these workflows.
2. **Performance** – standardizing benchmarks so we can compare apples to apples, improving parallelism/partitioning, optimizing SSD and cloud storage access, revisiting how we measure tuning knobs.
3. **Developer features** – observability (DDL stalls, conflicting locks), declarative migrations, richer full-text/string tooling, smaller windows between postgres.git and packaged releases.

## Community focus

- **Mentorship** – newcomers face steep learning curves (codebase, mailing lists, patch workflow). Melanie Plageman’s PGCon talk highlighted the need for better mentoring. PGConf.dev (the successor to PGCon) will experiment with workshops and mentor tracks in Vancouver 2024.
- **DEI** – talks like Karen Jex & Lætitia Avrot’s “Trying to Be Barbie in Ken’s Mojo Dojo Casa House” remind us PG has become more inclusive but still needs active effort (calling out sexism, making contributors feel welcome).
- **Transparency** – even in open source, some governance happens behind closed doors. The CoC committee’s annual reports are a good model: anonymized summaries build trust. Other PG teams could do similar reports.

## Closing thoughts

PostgreSQL is in a great place—popular, trusted, performant. But there’s plenty to improve, and the community is actively working on it. Asking “where are we going?” lets us celebrate the last few years of progress while charting the next steps.
