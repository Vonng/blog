---
title: Pig, The Postgres Extension Wizard
linkTitle: "Pig - The Postgres Extension Wizard"
date: 2024-12-29
author: |
  [RuohangFeng](https://vonng.com)([@Vonng](https://vonng.com/en/))| [WeChat](https://mp.weixin.qq.com/s/8zxeDQ7p5tPNGYED_1Bugg)
summary: Why would we need yet another package manager for PostgreSQL & extensions?
tags: [PostgreSQL,Tool]
---


## **Title**: Meet *Pig*: The Postgres Extension Wizard

Ever wished installing or upgrading PostgreSQL extensions didn’t feel like digging through outdated readmes, cryptic configure scripts, or random GitHub forks & patches? The painful truth is that Postgres’s richness of extension often comes at the cost of complicated setups—especially if you’re juggling multiple distros or CPU architectures.

Enter **Pig**, a Go-based package manager built to tame Postgres and its ecosystem of [440+](https://pgext.cloud/list) extensions in one fell swoop. TimescaleDB, Citus, PGVector, 20+ Rust extensions, plus every must-have piece to [self-host](https://pigsty.io/db/supabase) Supabase — Pig’s unified CLI makes them all effortlessly accessible. It cuts out messy source builds and half-baked repos, offering version-aligned RPM/DEB packages that work seamlessly across Debian, Ubuntu, and RedHat flavors. No guesswork, no drama.

Instead of reinventing the wheel, Pig piggyback your system’s native package manager (APT, YUM, DNF) and follow official PGDG packaging conventions to ensure a glitch-free fit. That means you don’t have to choose between “the right way” and “the quick way”; Pig respects your existing repos, aligns with standard OS best practices, and fits neatly alongside other packages you already use.

Ready to give your Postgres superpowers without the usual hassle? Check out **[GitHub](https://github.com/pgsty/pig)** for documentation, installation steps, and a peek at its massive [extension list](https://pgext.cloud/list). Then, watch your local Postgres instance transform into a powerhouse of specialized modules—no black magic is required. If [the future of Postgres is unstoppable extensibility](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4), Pig is the genie that helps you unlock it. Honestly, nobody ever complained that they had *too many* extensions.

[PIG v0.1 Release](https://github.com/pgsty/pig) | [GitHub Repo](https://github.com/pgsty/pig) | Blog: [The Idea Way to deliver PG Extensions](https://medium.com/@fengruohang/the-idea-way-to-deliver-postgresql-extensions-35646464bb71)


-------

## Get Started

[Install](#installation) the `pig` package itself with scripts or the traditional yum/apt way.

```bash
curl -fsSL https://repo.pigsty.io/pig | bash
```

Then it's ready to use; assume you want to install the [`pg_duckdb`](https://pgext.cloud/e/pg_duckdb) extension:


```bash
$ pig repo add pigsty pgdg -u  # add pgdg & pigsty repo, update cache
$ pig repo set -u              # overwrite all existing repos, brute but effective

$ pig ext install pg17         # install native PGDG PostgreSQL 17 kernels packages
$ pig ext install pg_duckdb    # install the pg_duckdb extension (for current pg17)
```

### **Extension Management**


```bash
pig ext list    [query]      # list & search extension      
pig ext info    [ext...]     # get information of a specific extension
pig ext status  [-v]         # show installed extension and pg status
pig ext add     [ext...]     # install extension for current pg version
pig ext rm      [ext...]     # remove extension for current pg version
pig ext update  [ext...]     # update extension to the latest version
pig ext import  [ext...]     # download extension to local repo
pig ext link    [ext...]     # link postgres installation to path
pig ext build   [ext...]     # setup building env for extension
```

### **Repo Management**


```bash
pig repo list                    # available repo list             (info)
pig repo info   [repo|module...] # show repo info                  (info)
pig repo status                  # show current repo status        (info)
pig repo add    [repo|module...] # add repo and modules            (root)
pig repo rm     [repo|module...] # remove repo & modules           (root)
pig repo update                  # update repo pkg cache           (root)
pig repo create                  # create repo on current system   (root)
pig repo boot                    # boot repo from offline package  (root)
pig repo cache                   # cache repo as offline package   (root)
```


