---
title: The Ideal Way to Deliver PostgreSQL Extensions
date: 2024-11-02
author: |
  [Vonng](https://vonng.com/en/about/) ([@Vonng](https://github.com/Vonng))
summary: >
  PostgreSQL is eating the database world through extensibility. This post introduces the Pigsty extension repository, which packaged 390 PostgreSQL extensions at launch and keeps growing through the Pigsty extension catalog.
tags: [PostgreSQL, PG-Ecosystem, Extension]
---

[**PostgreSQL Is Eating the Database World**](/en/pg/pg-eat-db-world/) through the power of **extensibility**.
When this post was first published, the repository packaged **390** PostgreSQL extensions as RPM / DEB packages for mainstream Linux distributions.
The live [Pigsty Extension Catalog](https://pigsty.io/ext/list/) has kept growing since then.

I believe the PostgreSQL community has reached a consensus on the importance of extensions.
So the real question now becomes: **"What should we do about it?"**

What's the primary problem with PostgreSQL extensions? In my opinion, it’s their **accessibility**.
Extensions are useless if most users can’t easily install and enable them. But it's not that easy.

Even the largest cloud PostgreSQL vendors are struggling with this.
They have some inherent limitations (multi-tenancy, security, licensing) that make it hard for them to fully address this issue.

So here's my plan: I've created a [**repository**](https://pigsty.io/docs/pgsql/ext/repo/) that hosts [**390**](https://pigsty.io/ext/list/) of the most capable extensions in the PostgreSQL ecosystem,
available as RPM / DEB packages on mainstream Linux OS distros. The goal is to take PostgreSQL one solid step closer to becoming the all-powerful database and achieve **the great alignment** between the Debian and EL OS ecosystems.

> [**TL;DR: Take me to the HOW-TO part!**](#apt-repo)

<a href="/en/pg/pg-eat-db-world/"><img src="/pg/pg-eat-db-world/ecosystem.jpg" alt="PostgreSQL extension ecosystem" style="max-width: 1000px; max-height: 1000px; width: 100%; height: auto;"></a>



--------

## The status quo

The PostgreSQL ecosystem is rich with extensions, but how do you actually install and use them? This initial hurdle becomes a roadblock for many. There are some existing solutions:

PGXN says, "*You can download and compile extensions on the fly with `pgxnclient`.*"
Tembo says, "*We have prepared pre-configured extension stack as Docker images.*"
StackGres & Omnigres says, "*We download `.so` files on the fly.*" All solid ideas.

Based on my experience, the vast majority of users still rely on their operating system's package manager to install PG extensions.
On-the-fly compilation and downloading shared libraries might not be viable for production environments, because many database setups don’t have internet access or a proper toolchain ready.

In the meantime, existing OS package managers like `yum`/`dnf`/`apt` already solve issues like dependency resolution, upgrades, and version management well.
There's no need to reinvent the wheel or disrupt existing standards. So the real question is: Who's going to package these extensions into ready-to-use software?

PGDG has already made a fantastic effort with official [YUM](https://download.postgresql.org/pub/repos/yum/) and [APT](http://apt.postgresql.org/pub/repos/apt/) repositories.
In addition to the **70** built-in [Contrib](https://www.postgresql.org/docs/current/contrib.html) extensions bundled with PostgreSQL, the PGDG YUM repo offers **128** RPM extensions, while the APT repo offers **104** DEB extensions.
These extensions are compiled and packaged in the same environment as the PostgreSQL kernel, making them easy to install alongside the PostgreSQL binary packages.
In fact, even most PostgreSQL Docker images rely on the PGDG repo to install extensions.

I’m deeply grateful for Devrim's maintenance of the PGDG YUM repo and Christoph's work with the APT repo. Their efforts to make PostgreSQL installation and extension management seamless are incredibly valuable.
But as a distribution creator myself, I’ve encountered some challenges with PostgreSQL extension distribution.




--------

## What's the challenge?

The first major issue facing extension users is **Alignment**.

In the two primary Linux distro camps — Debian and EL — there’s a significant number of PostgreSQL extensions.
Excluding the **70** built-in Contrib extensions bundled with PostgreSQL, the YUM repo offers **128** extensions, and the APT repo provides **104**.

However, when we dig deeper, we see that alignment between the two repos is not ideal.
The combined total of extensions across both repos is **153**, but the overlap is just **79**. That means **only half** of the extensions are available in both ecosystems!

<a href="/pg/pg-ext-repo/pgdg-ext.png"><img src="/pg/pg-ext-repo/pgdg-ext.png" alt="PGDG extension availability matrix" style="max-width: 1000px; max-height: 1000px; width: 100%; height: auto;"></a>

> Only half of the extensions are available in both EL and Debian ecosystems!

Next, we run into further alignment issues within each ecosystem itself. The availability of extensions can vary between different major OS versions.
For instance, `pljava`, `sequential_uuids`, and `firebird_fdw` are only available in EL9, but not in EL8. Similarly, `rdkit` is available in Ubuntu 22+ / Debian 12+, but not in Ubuntu 20 / Debian 11.
There’s also the issue of architecture support. For example, `citus` does not provide `arm64` packages in the Debian repo.

And then we have alignment issues across different PostgreSQL major versions. Some extensions won’t compile on older PostgreSQL versions, while others won’t work on newer ones.
Some extensions are only available for specific PostgreSQL versions in certain distributions, and so on.

These alignment issues lead to a significant number of permutations. For example, if we consider five mainstream OS distributions (el8, el9, debian12, ubuntu22, ubuntu24),
two CPU architectures (`x86_64` and `arm64`), and six PostgreSQL major versions (12–17), that’s **60-70** RPM/DEB packages per extension, just for one extension!

On top of alignment, there’s the problem of **completeness**. PGXN lists over **375** extensions, but the PostgreSQL ecosystem could have as many as [**1,000+**](https://gist.github.com/joelonsql/e5aa27f8cc9bd22b8999b7de8aee9d47). The PGDG repos, however, contain only about **one-tenth** of them.

There are also several powerful new Rust-based extensions that PGDG doesn’t include, such as [`pg_graphql`](https://pigsty.io/ext/e/pg_graphql/), [`pg_jsonschema`](https://pigsty.io/ext/e/pg_jsonschema/), and [`wrappers`](https://pigsty.io/ext/e/wrappers/) for [self-hosting Supabase](https://pigsty.io/docs/app/supabase/);
[`pg_search`](https://pigsty.io/ext/e/pg_search/) as an Elasticsearch alternative; and [`pg_analytics`](https://pigsty.io/ext/e/pg_analytics/), [`pg_parquet`](https://pigsty.io/ext/e/pg_parquet/), and [`pg_mooncake`](https://pigsty.io/ext/e/pg_mooncake/) for OLAP processing. The reason? They are too slow to compile...





--------

## What's the solution?

Over the past six months, I’ve focused on consolidating the PostgreSQL extension ecosystem.
Recently, I reached a milestone I’m quite happy with. I’ve created a PG YUM/APT repository with a catalog of **390** available PostgreSQL extensions.

Here are some key stats for the repo: It hosts **390** extensions in total. Excluding the **70** built-in extensions that come with PostgreSQL, this leaves **270** third-party extensions.
Of these, about half are maintained by the official PGDG repos (**126** RPM, **102** DEB). The other half (**131** RPM, **143** DEB) are maintained, fixed, compiled, packaged, and distributed by myself.

|               OS \ Entry               | All | PGDG | PIGSTY | CONTRIB | MISC | MISS | PG17 | PG16 | PG15 | PG14 | PG13 | PG12 |
|:--------------------------------------:|:---:|:----:|:------:|:-------:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| [**RPM**](https://pigsty.io/ext/rpm/) | 334 | 115  |  143   |   70    |  4   |  6   | 301  | 330  | 333  | 319  | 307  | 294  |
| [**DEB**](https://pigsty.io/ext/deb/) | 326 | 104  |  144   |   70    |  4   |  14  | 302  | 322  | 325  | 316  | 303  | 293  |

For each extension, I’ve built versions for the **6** major PostgreSQL versions (12–17) across five popular Linux distributions: EL8, EL9, Ubuntu 22.04, Ubuntu 24.04, and Debian 12.
I’ve also provided some limited support for older OS versions like EL7, Debian 11, and Ubuntu 20.04.

This repository also addresses most of the **alignment** issue. Initially, there were extensions in the APT and YUM repos that were unique to each, but I’ve worked to port as many of these unique extensions to the other ecosystem.
Now, only **7** APT extensions are missing from the YUM repo, and **16** extensions are missing in APT—just **6%** of the total. Many missing PGDG extensions have also been resolved.

<a href="https://pigsty.io/ext/list/"><img src="/pg/pg-ext-repo/pigsty-ext.png" alt="Pigsty extension availability matrix" style="max-width: 1000px; max-height: 1000px; width: 100%; height: auto;"></a>

I’ve created a comprehensive directory listing all supported extensions, with detailed info, dependency installation instructions, and other important notes.

<a href="https://pigsty.io/ext/e/citus/"><img src="/pg/pg-ext-repo/citus.png" alt="Citus extension detail page" style="max-width: 800px; max-height: 1000px; width: 100%; height: auto;"></a>

I hope this repository can serve as the ultimate solution to the frustration users face when extensions are difficult to find, compile, or install.



--------

## How to use this repo?

Now, for a quick plug — what’s the easiest way to install and use these extensions?

The simplest option is to use the OSS PostgreSQL distribution: [**Pigsty**](https://pigsty.io/).
The repo is autoconfigured by default, so all you need to do is declare them in the [config inventory](https://pigsty.io/docs/setup/config/).

For example, the [self-hosting Supabase config](https://pigsty.io/docs/conf/supabase/) requires extensions that aren’t available in the PGDG repo.
You can simply [download](https://pigsty.io/docs/pgsql/ext/download/), [install](https://pigsty.io/docs/pgsql/ext/install/), [configure/preload](https://pigsty.io/docs/pgsql/ext/config/), and [create](https://pigsty.io/docs/pgsql/ext/create/) extensions by referring to their names.

```yaml
all:
  children:
    pg-meta:
      hosts: { 10.10.10.10: { pg_seq: 1, pg_role: primary } }
      vars:
        pg_cluster: pg-meta

        # INSTALL EXTENSIONS
        pg_extensions:
          - supa-stack   # essential extensions for Supabase
          - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
          - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
          - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit

        # LOAD EXTENSIONS
        pg_libs: 'pg_stat_statements, plpgsql, plpgsql_check, pg_cron, pg_net, timescaledb, auto_explain, pg_tle, plan_filter'

        # CONFIG EXTENSIONS
        pg_parameters:
          cron.database_name: postgres
          pgsodium.enable_event_trigger: off

        # CREATE EXTENSIONS
        pg_databases:
          - name: postgres
            baseline: supabase.sql
            schemas: [ extensions ,auth ,realtime ,storage ,graphql_public ,supabase_functions ,_analytics ,_realtime ]
            extensions:
              - { name: pgcrypto  ,schema: extensions  }
              - { name: pg_net    ,schema: extensions  }
              - { name: pgjwt     ,schema: extensions  }
              - { name: uuid-ossp ,schema: extensions  }
              - { name: pgsodium        }               
              - { name: supabase_vault  }               
              - { name: pg_graphql      }               
              - { name: pg_jsonschema   }               
              - { name: wrappers        }               
              - { name: http            }               
              - { name: pg_cron         }               
              - { name: timescaledb     }               
              - { name: pg_tle          }               
              - { name: vector          }               
  vars:
    pg_version: 17

    # DOWNLOAD EXTENSIONS
    repo_extra_packages:
      - pgsql-main
      - supa-stack   # essential extensions for Supabase
      - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
      - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
      - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
```

To simply add extensions to existing clusters:

```bash
./infra.yml -t repo_build -e '{"repo_extra_packages":["citus"]}'  # download
./pgsql.yml -t pg_extension -e '{"pg_extensions":["citus"]}'      # install
```

Although this repo is designed to be used with Pigsty, it is **not mandatory**. You can still enable this repository on any EL/Debian/Ubuntu system with a simple one-liner in the shell:


### APT Repo

<a href="https://pigsty.io/docs/pgsql/ext/repo/#apt-repository"><img alt="Linux x86_64" src="https://img.shields.io/badge/Linux-x86_64-%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black"></a>
<a href="https://pigsty.io/ext/os/u24.x86_64/"><img alt="Ubuntu 24.04 support" src="https://img.shields.io/badge/Ubuntu-24/noble-%23E95420?style=flat&logo=ubuntu&logoColor=%23E95420"></a>
<a href="https://pigsty.io/ext/os/u22.x86_64/"><img alt="Ubuntu 22.04 support" src="https://img.shields.io/badge/Ubuntu-22/jammy-%23E95420?style=flat&logo=ubuntu&logoColor=%23E95420"></a>
<a href="https://pigsty.io/ext/os/d12.x86_64/"><img alt="Debian 12 support" src="https://img.shields.io/badge/Debian-12/bookworm-%23A81D33?style=flat&logo=debian&logoColor=%23A81D33"></a>

For Debian 11/12/13, Ubuntu 22.04/24.04/26.04, or compatible platforms, use the following commands to add the APT repo:

```bash
curl -fsSL https://repo.pigsty.io/key | sudo gpg --dearmor -o /etc/apt/keyrings/pigsty.gpg
sudo tee /etc/apt/sources.list.d/pigsty-io.list > /dev/null <<EOF
deb [signed-by=/etc/apt/keyrings/pigsty.gpg] https://repo.pigsty.io/apt/infra generic main 
deb [signed-by=/etc/apt/keyrings/pigsty.gpg] https://repo.pigsty.io/apt/pgsql/$(lsb_release -cs) $(lsb_release -cs) main
EOF
sudo apt update
```

### YUM Repo

<a href="https://pigsty.io/docs/pgsql/ext/repo/#yum-repository"><img alt="Linux x86_64" src="https://img.shields.io/badge/Linux-x86_64-%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black"></a>
<a href="https://pigsty.io/ext/os/el9.x86_64/"><img alt="EL 9 support" src="https://img.shields.io/badge/EL-9-red?style=flat&logo=redhat&logoColor=red"></a>
<a href="https://pigsty.io/ext/os/el8.x86_64/"><img alt="EL 8 support" src="https://img.shields.io/badge/EL-8-red?style=flat&logo=redhat&logoColor=red"></a>
<a href="https://pigsty.io/ext/rpm/"><img alt="RHEL compatible RPM packages" src="https://img.shields.io/badge/RPM-packages-slategray?style=flat&logo=redhat&logoColor=red"></a>
<a href="https://almalinux.org/"><img alt="AlmaLinux compatible" src="https://img.shields.io/badge/AlmaLinux-compatible-slategray?style=flat&logo=almalinux&logoColor=black"></a>

For EL 7/8/9/10 and compatible platforms, use the following commands to add the YUM repo:

```bash
curl -fsSL https://repo.pigsty.io/key      | sudo tee /etc/pki/rpm-gpg/RPM-GPG-KEY-pigsty >/dev/null  # add gpg key
curl -fsSL https://repo.pigsty.io/yum/repo | sudo tee /etc/yum.repos.d/pigsty.repo        >/dev/null  # add repo file
sudo yum makecache
```


--------------

## What's in this repo?

The live catalog organizes extensions by category, platform, repository, language, license, and attributes. It started with categories such as TIME, GIS, RAG, FTS, OLAP, FEAT, LANG, TYPE, FUNC, ADMIN, STAT, SEC, FDW, SIM, and ETL, and continues to evolve as the extension ecosystem grows.

Check the [Pigsty Extension Catalog](https://pigsty.io/ext/list/) for the current details.



--------

## Some Thoughts

Each major PostgreSQL version introduces changes, making the maintenance of **140+** extension packages a bit of a beast.

Especially when some extension authors haven’t updated their work in years. In these cases, you often have no choice but to take matters into your own hands.
I’ve personally fixed several extensions and ensured they support the latest PostgreSQL major versions. For those authors I could reach, I’ve submitted numerous PRs and issues to keep things moving forward.

<a href="https://github.com/Vonng"><img src="/pg/pg-ext-repo/github-contrib.webp" alt="GitHub contribution activity" style="max-width: 800px; width: 100%; height: auto;"></a>

Back to the point: **my goal with this repo is to establish a standard for PostgreSQL extension installation and distribution, solving the distribution challenges that have long troubled users**.

A recent milestone is that, the popular open-source PostgreSQL HA cluster project [**postgresql_cluster**](https://autobase.tech/docs/extensions/list), has made this extension repository the default upstream for PG extension installation.

Currently, this repository (repo.pigsty.io) is hosted on Cloudflare. In the past month, the repo and its mirrors have served about **300GB** of downloads.
Given that most extensions are just a few KB to a few MB, that amounts to nearly **a million downloads per month**.
Since Cloudflare doesn’t charge for traffic, I can confidently commit to keeping this repository completely free and under active maintenance for the foreseeable future, as long as Cloudflare doesn't charge me too much.

I believe my work can help PostgreSQL users worldwide and contribute to the thriving PostgreSQL ecosystem. I hope it proves useful to you as well. **Enjoy PostgreSQL!**
