---
title: "Is Oracle-Compatible PostgreSQL Actually Useful?"
date: 2026-02-22
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  A migration case with only a JAR and no source code shows why Oracle syntax compatibility is not always a fake requirement, and how IvorySQL + Pigsty can absorb legacy debt at low cost.
tags: [PostgreSQL, Oracle, IvorySQL]
---

Lots of domestic databases sell "Oracle compatibility" as a headline feature.
To be honest, I used to roll my eyes at that.
My default take was: if you need this, just fix your app code.

Then I ran into a case that changed my mind.


## A JAR with no source code

I recently took a small migration job for a Fortune 500 auto company.
They were running EDB (EnterpriseDB's Oracle-compatible PostgreSQL), on version **9.1**.

PG 9.1 was released in September 2011.
As of 2026, that's roughly **15 years old**.

Their system had already seen several major incidents on their cloud platform.
Eventually they said: please upgrade this thing.
From a pure database angle, an upgrade is doable.
But going from 9.1 to modern PG 18 means crossing about fifteen major versions.

Still, the real problem was not version gap.
The real problem was the application: **the source code was gone**.

What they still had was a JAR.
SQL strings were baked inside it, and those SQLs used EDB Oracle-style syntax, like `SYSDATE`.


## Why `SYSDATE` is awkward in PostgreSQL

In Oracle, `SYSDATE` is a built-in keyword-like object for current timestamp.
In PostgreSQL, the equivalent idea would be `current_timestamp`.

At first glance this sounds easy: create a function and move on.

```sql
CREATE FUNCTION sysdate() RETURNS timestamp(0) AS
  $$SELECT clock_timestamp()::timestamp(0) $$ LANGUAGE SQL;
```

But that does not solve this case.
The application does not call `sysdate()` as a function.
It sends bare `SYSDATE` as an identifier.
PostgreSQL parses that as a column reference, not a callable function, so it errors out:

```bash
postgres@pg-meta-1:5432/postgres=# SELECT SYSDATE;
ERROR: ivory column "sysdate" does not exist
LINE 1: SELECT SYSDATE;
               ^
Time: 0.249 ms
```

And you cannot fix this with a normal extension.
PostgreSQL is extensible in many places (types, operators, indexes, storage, execution logic, foreign data).
But SQL grammar is not extension-driven.
If you want PostgreSQL to understand `SYSDATE` as a token, you need parser-level changes in core source.

If source code existed, this would be trivial today:
run a global replacement from `SYSDATE` to `clock_timestamp()::timestamp(0)`.
No source code means that path is closed.
Decompiling and patching SQL literals inside a JAR is possible in theory, but risky and fragile in practice.

So the legacy debt landed on the database layer.


## IvorySQL: open-source Oracle compatibility in the kernel

The requirement is awkward, but still real.
So what are the options?

EDB does this well, but it is commercial and expensive.
The customer also wanted to move away from it.
There are many "Oracle-compatible" products in China, but that was not acceptable for this client.
After filtering constraints, the practical option left was **IvorySQL**.

IvorySQL is an Apache-2.0 open-source project from HighGo.
It is based on PostgreSQL core and adds Oracle compatibility: PL/SQL, Oracle-style syntax, built-in functions, data types, system views, and so on.
IvorySQL 5.1 is aligned with PostgreSQL 18.1.

Important detail: this is **SQL syntax compatibility**, not Oracle wire-protocol compatibility.
Clients still connect with PostgreSQL drivers.
You get Oracle-like SQL behavior after connection, without pretending to be Oracle on the network protocol level.

The other key point for me was this:
**IvorySQL is just the kernel, and Pigsty turns it into a full RDS stack.**

HA, backup/restore, monitoring, IaC all stay integrated.
Operationally this was a tiny change:

```bash
curl -fsSL https://repo.pigsty.cc/get | bash; cd ~/pigsty
./configure -c ivory    # use the IvorySQL template
./deploy.yml
```

![ivory-dashboard.webp](ivory-dashboard.webp)

Three commands later, an Oracle-compatible PostgreSQL RDS was up.
On the default PG port `5432`, `SYSDATE` fails.
On IvorySQL's Oracle-compatible port `1521`, it works:

```bash
vagrant@meta:~$ psql -p 5432 -c 'select sysdate'
ERROR:  column "sysdate" does not exist
LINE 1: select sysdate
               ^
vagrant@meta:~$ psql -p 1521 -c 'select sysdate'
  sysdate
------------
 2026-02-22
(1 row)

vagrant@meta:~$ psql -p 1521 -c 'select version()'
                                              version
-----------------------------------------------------------------------------
 PostgreSQL 18.1 (IvorySQL 5.1) on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 10.2.0, 64-bit
(1 row)
```

This project is a low five-figure RMB/year service engagement for me.
Compared with EDB subscription cost, it is dramatically cheaper.

To be precise, I do not sell IvorySQL core warranty.
If IvorySQL itself breaks, that belongs to HighGo support.
I own the Pigsty RDS delivery and operations side.
From my tests so far, IvorySQL changes look incremental rather than a deep rewrite, and I have not seen crash/dump issues in practice.

So yes, this solved a very specific legacy Oracle-compatibility problem cleanly.
It is a niche, but clearly not a fake one.


## Pigsty as a "meta-distribution"

Since this case came up, here are a few recent kernel-side things around Pigsty.

**Babelfish rebuild.**
Babelfish (AWS's SQL Server-compatible PG kernel) used to rely on WiltonDB packages.
Those packages were old (PG15), limited in platform coverage (EL8/9 + Ubuntu 22/24), and missed Debian + EL10.
They also required another vendor repo.
So I rebuilt the packaging pipeline to Pigsty standards with Codex.
Now Babelfish installs directly from Pigsty's own repo, with broader platform support, and on PG 17.

![cloudberry.webp](cloudberry.webp)

**Cloudberry data warehouse kernel.**
After Babelfish, I also packaged Apache Cloudberry (the open-source warehouse line based on Greenplum 7).
Cloudberry 1.6 at least had EL8/9 RPMs; after 2.0, we waited months without official binaries.
So I built them myself: EL 8-10, Debian 12/13, Ubuntu 22/24, x86_64 + ARM64, 14 Linux targets total.
This was non-trivial; Codex ran a lot of integration/unit tests and we had to patch a few issues before EL10/Debian13 were clean.

Also updated recently:
- OrioleDB to Beta 14
- Percona PGTDE to 18.1

This is why I call Pigsty a **meta-distribution**, not just another PostgreSQL distribution.

You pick the kernel by requirement:

- Need **Oracle compatibility**: IvorySQL kernel (and Polar-O kernel)
- Need **SQL Server compatibility**: Babelfish kernel
- Need **MongoDB compatibility**: DocumentDB extension + FerretDB
- Need **maximum OLTP performance**: OrioleDB kernel
- Need **transparent data encryption**: PGTDE kernel
- Need **horizontal scale-out**: Citus kernel
- Need **data warehouse**: Cloudberry kernel

No matter which kernel you choose, Pigsty's platform layer is the same: monitoring, HA, backup/restore, and IaC.
Kernel can change. Platform capability stays stable.
That is what a distribution should do.
