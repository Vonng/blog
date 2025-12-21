---
title: Forging a China-Rooted, Global PostgreSQL Distro
date: 2025-11-27
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  PostgreSQL already won. The real battle is the distro layer. Will Chinese developers watch from the sideline or craft a PG “Ubuntu” for the world?
tags: [PostgreSQL,Pigsty]
---

Hi, I’m Feng Ruohang, author of Pigsty and an independent open-source contributor. Let’s talk about **how to build a PostgreSQL distribution that is rooted in China and useful to the whole world.**

The question isn’t whether PG will win—it already has. The question is: **What role do we play in that victory?** Spectator or protagonist? Follower or leader?

## Why now

### PostgreSQL is the default database

Stack Overflow’s 2025 survey shows **58.2%** of professional developers use PG—18.6 points ahead of MySQL, and the gap is widening. New SaaS, AI startups, even OpenAI default to PG. DB-Engines rankings and JetBrains surveys tell the same story.

Capital agrees: in 2025 Databricks bought Neon (~$1 B) and Snowflake bought Crunchy Data ($250 M). AWS Aurora DSQL, Azure HorizonDB, GCP AlloyDB—all PG. **Technology won, money followed.**

### China is missing from the PG narrative

Despite hundreds of domestic “PG-derived” products, our presence in the global ecosystem is faint. Until recently **there wasn’t a single Chinese committer** on the PG core list. The most visible Chinese-led PG project by GitHub stars is… Pigsty, a one-man project. That’s both flattering and a little sad.

At PG conferences I’ve met only a handful of Chinese developers. We’re spectators at our own victory parade.

## What must change

The kernel wars are over; the fight shifts to distributions. Whoever controls the distro controls the experience—like Ubuntu did for Linux. We need a PG “Ubuntu” built with China’s strengths but serving global developers, the way DeepSeek did in AI.

## Pigsty as a case study

Pigsty started at **Tantan** (China’s #2 dating app). We were dealing with **2.5 M global QPS**, PL/pgSQL-heavy business logic, hundreds of physical clusters. Off-the-shelf tooling couldn’t cope, so we built our own HA, backups, monitoring, IaC. **China’s scale was the forge.** If it survives Tantan, it’s overkill everywhere else.

But “rooted in China” isn’t enough; “facing the world” means becoming part of the global supply chain. That requires obsessing over developer experience, not just DBA comfort.

In 2023 Pigsty already did HA + backups + observability + bare-metal delivery. Yet something was missing—**features.** PG’s true power is extensions. MySQL spends years grafting on vectors; PG’s community ships pgvector and kneecaps an entire market in months.

So I built an extension repository. I waited for others to do it, nobody did, so I compiled them myself: first a dozen, then dozens, then hundreds. Today Pigsty provides **437 extensions** across EL9/EL8/Debian/Ubuntu, more than the official PGDG repos. That makes Pigsty part of the upstream supply chain: when developers `apt install` an extension, they’re using binaries built in China yet serving users worldwide.

## Vision

- **Rooted in China:** leverage our scale, scenarios, and demand to harden solutions under extreme stress.
- **Facing the world:** ship battle-tested, developer-friendly distros and extension repos that anyone can consume, just like they consume Debian packages.
- **Play to our strengths:** we may not have a kernel committer yet, but we can dominate tooling, packaging, automation, and integrations—the layers that actually reach users.

Pigsty isn’t the only answer, but it proves a point: **a single Chinese engineer, working the right problem, can earn a seat at PostgreSQL’s global table.** Imagine what we could do together.
