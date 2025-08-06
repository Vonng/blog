---
title: The ideal way to deliver PostgreSQL Extensions
date: 2024-11-02
author: |
  [Vonng](https://vonng.com)([@Vonng](https://vonng.com/en/))
summary: >
  PostgreSQL Is Eating the Database World through the power of extensibility. With 390 extensions powering PG, we may not say it's invincible, but it’s definitely getting much closer.
tags: [PostgreSQL,Ecosystem,Extension]
---

[**PostgreSQL Is Eating the Database World**](/pg/pg-eat-db-world) through the power of **extensibility**.
With **390** extensions powering PostgreSQL, we may not say it's invincible, but it’s definitely getting much closer.

I believe the PostgreSQL community has reached a consensus on the importance of extensions.
So the real question now becomes: **"What should we do about it?"**

What's the primary problem with PostgreSQL extensions? In my opinion, it’s their **accessibility**.
Extensions are useless if most users can’t easily install and enable them. But it's not that easy.

Even the largest cloud postgres vendors are struggling with this.
They have some inherent limitations (multi-tenancy, security, licensing) that make it hard for them to fully address this issue.

So here's my plan, I've created a [**repository**](https://ext.pgsty.com/) that hosts [**390**](https://ext.pgsty.com/zh/e/list) of the most capable extensions in the PostgreSQL ecosystem,
available as RPM / DEB packages on mainstream Linux OS distros.  And the goal is to take PostgreSQL one solid step closer to becoming the all-powerful database and achieve **the great alignment** between the Debian and EL OS ecosystems.

> [**TL;DR: Take me to the HOW-TO part!**](#apt-repo)

<a href="/pg/pg-eat-deb-world"><img src="https://pigsty.io/img/ecosystem.jpg" style="max-width: 800px; max-height: 1000px; width: 100%; height: auto;"></a>



--------

## The status quo

The PostgreSQL ecosystem is rich with extensions, but how do you actually install and use them? This initial hurdle becomes a roadblock for many. There are some existing solutions:

PGXN says, "*You can download and compile extensions on the fly with `pgxnclient`.*"
Tembo says, "*We have prepared pre-configured extension stack as Docker images.*"
StackGres & Omnigres says, "*We download `.so` files on the fly.*" All solid ideas.

While based on my experience, the vast majority of users still rely on their operating system's package manager to install PG extensions.
On-the-fly compilation and downloading shared libraries might not be a viable option for production env. Since many DB setups don’t have internet access or a proper toolchain ready.

In the meantime, Existing OS package managers like `yum`/`dnf`/`apt` already solve issues like dependency resolution, upgrades, and version management well.
There's no need to reinvent the wheel or disrupt existing standards. So the real question is: Who's going to package these extensions into ready-to-use software?

PGDG has already made a fantastic effort with official [YUM](https://download.postgresql.org/pub/repos/yum/) and [APT](http://apt.postgresql.org/pub/repos/apt/) repositories.
In addition to the **70** built-in [Contrib](https://ext.pgsty.com/e/contrib) extensions bundled with PostgreSQL,the PGDG YUM repo offers **128** RPM extensions, while the APT repo offers **104** DEB extensions.
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

<a href="pgdg-ext.png"><img src="pgdg-ext.png" style="max-width: 1000px; max-height: 1000px; width: 100%; height: auto;"></a>

> Only half of the extensions are available in both EL and Debian ecosystems!

Next, we run into further alignment issues within each ecosystem itself. The availability of extensions can vary between different major OS versions.
For instance, `pljava`, `sequential_uuids`, and `firebird_fdw` are only available in EL9, but not in EL8. Similarly, `rdkit` is available in Ubuntu 22+ / Debian 12+, but not in Ubuntu 20 / Debian 11.
There’s also the issue of architecture support. For example, `citus` does not provide `arm64` packages in the Debian repo.

And then we have alignment issues across different PostgreSQL major versions. Some extensions won’t compile on older PostgreSQL versions, while others won’t work on newer ones.
Some extensions are only available for specific PostgreSQL versions in certain distributions, and so on.

These alignment issues lead to a significant number of permutations. For example, if we consider five mainstream OS distributions (el8, el9, debian12, ubuntu22, ubuntu24), 
two CPU architectures (`x86_64` and `arm64`), and six PostgreSQL major versions (12–17), that’s **60-70** RPM/DEB packages per extension—just for one extension!

On top of alignment, there’s the problem of **completeness**. PGXN lists over **375** extensions, but the PostgreSQL ecosystem could have as many as [**1,000+**](https://gist.github.com/joelonsql/e5aa27f8cc9bd22b8999b7de8aee9d47). The PGDG repos, however, contain only about **one-tenth** of them.

There are also several powerful new Rust-based extensions that PGDG doesn’t include, such as `pg_graphql`, `pg_jsonschema`, and `wrappers` for [self-hosting Supabase]();
`pg_search` as an Elasticsearch alternative; and `pg_analytics`, `pg_parquet`, `pg_mooncake` for OLAP processing. The reason? They are too slow to compile...





--------

## What's the solution?

Over the past six months, I’ve focused on consolidating the PostgreSQL extension ecosystem.
Recently, I reached a milestone I’m quite happy with. I’ve created a PG YUM/APT repository with a catalog of **390**available PostgreSQL extensions.

Here are some key stats for the repo: It hosts **390** extensions in total. Excluding the **70** built-in extensions that come with PostgreSQL, this leaves **270** third-party extensions.
Of these, about half are maintained by the official PGDG repos (**126** RPM, **102** DEB). The other half (**131** RPM, **143**DEB) are maintained, fixed, compiled, packaged, and distributed by myself.

|               OS \ Entry               | All | PGDG | PIGSTY | CONTRIB | MISC | MISS | PG17 | PG16 | PG15 | PG14 | PG13 | PG12 |
|:--------------------------------------:|:---:|:----:|:------:|:-------:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| [**RPM**](https://ext.pgsty.com/e/rpm) | 334 | 115  |  143   |   70    |  4   |  6   | 301  | 330  | 333  | 319  | 307  | 294  |
| [**DEB**](https://ext.pgsty.com/e/deb) | 326 | 104  |  144   |   70    |  4   |  14  | 302  | 322  | 325  | 316  | 303  | 293  |

For each extension, I’ve built versions for the **6** major PostgreSQL versions (12–17) across five popular Linux distributions: EL8, EL9, Ubuntu 22.04, Ubuntu 24.04, and Debian 12.
I’ve also provided some limited support for older OS versions like EL7, Debian 11, and Ubuntu 20.04.

This repository also addresses most of the **alignment** issue. Initially, there were extensions in the APT and YUM repos that were unique to each, but I’ve worked to port as many of these unique extensions to the other ecosystem.
Now, only **7** APT extensions are missing from the YUM repo, and **16** extensions are missing in APT—just **6%** of the total. Many missing PGDG extensions have also been resolved.

<a href="pigsty-ext.png"><img src="pigsty-ext.png" style="max-width: 1000px; max-height: 1000px; width: 100%; height: auto;"></a>

I’ve created a comprehensive directory listing all supported extensions, with detailed info, dependency installation instructions, and other important notes.

<a href="citus.png"><img src="citus.png" style="max-width: 800px; max-height: 1000px; width: 100%; height: auto;"></a>

I hope this repository can serve as the ultimate solution to the frustration users face when extensions are difficult to find, compile, or install.



--------

## How to use this repo?

Now, for a quick plug — what’s the easiest way to install and use these extensions?

The simplest option is to use the OSS PostgreSQL distribution: [**Pigsty**](https://ext.pigsty.io/).
The repo is autoconfigured by default, so all you need to do is declare them in the [config inventory](/docs/setup/config).

For example,  the [self-hosting supabase](/docs/db/supabase) template requires extensions that aren’t available in the PGDG repo.
You can simply  [download](/docs/pgext/usage/download/), [install](/docs/pgext/usage/install/), [preload](/docs/pgext/usage/load/), [config](/docs/pgext/usage/config) and [create](/docs/pgext/usage/create) extensions by referring to their names.

```yaml
all:
  children:
    pg-meta:
      hosts: { 10.10.10.10: { pg_seq: 1, pg_role: primary } }
      vars:
        pg_cluster: pg-meta

        # INSTALL EXTENSIONS
        pg_extensions:
          - supabase   # essential extensions for supabase
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
      - supabase   # essential extensions for supabase
      - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
      - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
      - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
```

To simply add extensions to existing clusters:

```bash
./infra.yml -t repo_build -e '{"repo_packages":[citus]}'         # download
./pgsql.yml -t pg_extension -e '{"pg_extensions": ["citus"]}'    # install
```

Through this repo was meant to be used with Pigsty, But it is **not mandatory**. You can still enable this repository on any EL/Debian/Ubuntu system with a simple one-liner in the shell:


### APT Repo

[![Linux](https://img.shields.io/badge/Linux-x86_64-%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black)](https://pigsty.io/docs/node)
[![Ubuntu Support: 24](https://img.shields.io/badge/Ubuntu-24/noble-%23E95420?style=flat&logo=ubuntu&logoColor=%23E95420)](https://pigsty.io/docs/pgext/list/deb/)
[![Ubuntu Support: 22](https://img.shields.io/badge/Ubuntu-22/jammy-%23E95420?style=flat&logo=ubuntu&logoColor=%23E95420)](https://pigsty.io/docs/pgext/list/deb/)
[![Debian Support: 12](https://img.shields.io/badge/Debian-12/bookworm-%23A81D33?style=flat&logo=debian&logoColor=%23A81D33)](https://pigsty.iohttps://pigsty.io/docs/reference/compatibility/)

For Ubuntu 22.04 & Debian 12 or any compatible platforms, use the following commands to add the APT repo:

```bash
curl -fsSL https://repo.pigsty.io/key | sudo gpg --dearmor -o /etc/apt/keyrings/pigsty.gpg
sudo tee /etc/apt/sources.list.d/pigsty-io.list > /dev/null <<EOF
deb [signed-by=/etc/apt/keyrings/pigsty.gpg] https://repo.pigsty.io/apt/infra generic main 
deb [signed-by=/etc/apt/keyrings/pigsty.gpg] https://repo.pigsty.io/apt/pgsql/$(lsb_release -cs) $(lsb_release -cs) main
EOF
sudo apt update
```

### YUM Repo

[![Linux](https://img.shields.io/badge/Linux-x86_64-%23FCC624?style=flat&logo=linux&labelColor=FCC624&logoColor=black)](https://pigsty.io/docs/node)
[![RHEL Support: 8/9](https://img.shields.io/badge/EL-7/8/9-red?style=flat&logo=redhat&logoColor=red)](https://pigsty.io/docs/pgext/list/rpm/)
[![RHEL](https://img.shields.io/badge/RHEL-slategray?style=flat&logo=redhat&logoColor=red)](https://pigsty.io/docs/pgext/list/rpm/)
[![CentOS](https://img.shields.io/badge/CentOS-slategray?style=flat&logo=centos&logoColor=%23262577)](https://almalinux.org/)
[![RockyLinux](https://img.shields.io/badge/RockyLinux-slategray?style=flat&logo=rockylinux&logoColor=%2310B981)](https://almalinux.org/)
[![AlmaLinux](https://img.shields.io/badge/AlmaLinux-slategray?style=flat&logo=almalinux&logoColor=black)](https://almalinux.org/)
[![OracleLinux](https://img.shields.io/badge/OracleLinux-slategray?style=flat&logo=oracle&logoColor=%23F80000)](https://almalinux.org/)

For EL 8/9 and compatible platforms, use the following commands to add the YUM repo:

```bash
curl -fsSL https://repo.pigsty.io/key      | sudo tee /etc/pki/rpm-gpg/RPM-GPG-KEY-pigsty >/dev/null  # add gpg key
curl -fsSL https://repo.pigsty.io/yum/repo | sudo tee /etc/yum.repos.d/pigsty.repo        >/dev/null  # add repo file
sudo yum makecache
```


--------------

## What's in this repo?

In this repo, all the extensions are categorized into one of the **15** categories: TIME, GIS, RAG, FTS, OLAP, FEAT, LANG, TYPE, FUNC, ADMIN, STAT, SEC, FDW, SIM, ETL, as shown below.

[**TIME**](https://ext.pgsty.com/cate/time): [`timescaledb`](https://ext.pgsty.com/e/timescaledb) [`timescaledb_toolkit`](https://ext.pgsty.com/e/timescaledb_toolkit) [`timeseries`](https://ext.pgsty.com/e/timeseries) [`periods`](https://ext.pgsty.com/e/periods) [`temporal_tables`](https://ext.pgsty.com/e/temporal_tables) [`emaj`](https://ext.pgsty.com/e/emaj) [`table_version`](https://ext.pgsty.com/e/table_version) [`pg_cron`](https://ext.pgsty.com/e/pg_cron) [`pg_later`](https://ext.pgsty.com/e/pg_later) [`pg_background`](https://ext.pgsty.com/e/pg_background)
[**GIS**](https://ext.pgsty.com/cate/gis): [`postgis`](https://ext.pgsty.com/e/postgis) [`postgis_topology`](https://ext.pgsty.com/e/postgis_topology) [`postgis_raster`](https://ext.pgsty.com/e/postgis_raster) [`postgis_sfcgal`](https://ext.pgsty.com/e/postgis_sfcgal) [`postgis_tiger_geocoder`](https://ext.pgsty.com/e/postgis_tiger_geocoder) [`address_standardizer`](https://ext.pgsty.com/e/address_standardizer) [`address_standardizer_data_us`](https://ext.pgsty.com/e/address_standardizer_data_us) [`pgrouting`](https://ext.pgsty.com/e/pgrouting) [`pointcloud`](https://ext.pgsty.com/e/pointcloud) [`pointcloud_postgis`](https://ext.pgsty.com/e/pointcloud_postgis) [`h3`](https://ext.pgsty.com/e/h3) [`h3_postgis`](https://ext.pgsty.com/e/h3_postgis) [`q3c`](https://ext.pgsty.com/e/q3c) [`ogr_fdw`](https://ext.pgsty.com/e/ogr_fdw) [`geoip`](https://ext.pgsty.com/e/geoip) [`pg_polyline`](https://ext.pgsty.com/e/pg_polyline) [`pg_geohash`](https://ext.pgsty.com/e/pg_geohash) [`mobilitydb`](https://ext.pgsty.com/e/mobilitydb) [`earthdistance`](https://ext.pgsty.com/e/earthdistance)
[**RAG**](https://ext.pgsty.com/cate/rag): [`vector`](https://ext.pgsty.com/e/vector) [`vectorscale`](https://ext.pgsty.com/e/vectorscale) [`vectorize`](https://ext.pgsty.com/e/vectorize) [`pg_similarity`](https://ext.pgsty.com/e/pg_similarity) [`smlar`](https://ext.pgsty.com/e/smlar) [`pg_summarize`](https://ext.pgsty.com/e/pg_summarize) [`pg_tiktoken`](https://ext.pgsty.com/e/pg_tiktoken) [`pgml`](https://ext.pgsty.com/e/pgml) [`pg4ml`](https://ext.pgsty.com/e/pg4ml)
[**FTS**](https://ext.pgsty.com/cate/fts): [`pg_search`](https://ext.pgsty.com/e/pg_search) [`pg_bigm`](https://ext.pgsty.com/e/pg_bigm) [`zhparser`](https://ext.pgsty.com/e/zhparser) [`hunspell_cs_cz`](https://ext.pgsty.com/e/hunspell_cs_cz) [`hunspell_de_de`](https://ext.pgsty.com/e/hunspell_de_de) [`hunspell_en_us`](https://ext.pgsty.com/e/hunspell_en_us) [`hunspell_fr`](https://ext.pgsty.com/e/hunspell_fr) [`hunspell_ne_np`](https://ext.pgsty.com/e/hunspell_ne_np) [`hunspell_nl_nl`](https://ext.pgsty.com/e/hunspell_nl_nl) [`hunspell_nn_no`](https://ext.pgsty.com/e/hunspell_nn_no) [`hunspell_pt_pt`](https://ext.pgsty.com/e/hunspell_pt_pt) [`hunspell_ru_ru`](https://ext.pgsty.com/e/hunspell_ru_ru) [`hunspell_ru_ru_aot`](https://ext.pgsty.com/e/hunspell_ru_ru_aot) [`fuzzystrmatch`](https://ext.pgsty.com/e/fuzzystrmatch) [`pg_trgm`](https://ext.pgsty.com/e/pg_trgm)
[**OLAP**](https://ext.pgsty.com/cate/olap): [`citus`](https://ext.pgsty.com/e/citus) [`citus_columnar`](https://ext.pgsty.com/e/citus_columnar) [`columnar`](https://ext.pgsty.com/e/columnar) [`pg_analytics`](https://ext.pgsty.com/e/pg_analytics) [`pg_duckdb`](https://ext.pgsty.com/e/pg_duckdb) [`pg_mooncake`](https://ext.pgsty.com/e/pg_mooncake) [`duckdb_fdw`](https://ext.pgsty.com/e/duckdb_fdw) [`pg_parquet`](https://ext.pgsty.com/e/pg_parquet) [`pg_fkpart`](https://ext.pgsty.com/e/pg_fkpart) [`pg_partman`](https://ext.pgsty.com/e/pg_partman) [`plproxy`](https://ext.pgsty.com/e/plproxy) [`pg_strom`](https://ext.pgsty.com/e/pg_strom) [`tablefunc`](https://ext.pgsty.com/e/tablefunc)
[**FEAT**](https://ext.pgsty.com/cate/feat): [`age`](https://ext.pgsty.com/e/age) [`hll`](https://ext.pgsty.com/e/hll) [`rum`](https://ext.pgsty.com/e/rum) [`pg_graphql`](https://ext.pgsty.com/e/pg_graphql) [`pg_jsonschema`](https://ext.pgsty.com/e/pg_jsonschema) [`jsquery`](https://ext.pgsty.com/e/jsquery) [`pg_hint_plan`](https://ext.pgsty.com/e/pg_hint_plan) [`hypopg`](https://ext.pgsty.com/e/hypopg) [`index_advisor`](https://ext.pgsty.com/e/index_advisor) [`plan_filter`](https://ext.pgsty.com/e/plan_filter) [`imgsmlr`](https://ext.pgsty.com/e/imgsmlr) [`pg_ivm`](https://ext.pgsty.com/e/pg_ivm) [`pgmq`](https://ext.pgsty.com/e/pgmq) [`pgq`](https://ext.pgsty.com/e/pgq) [`pg_cardano`](https://ext.pgsty.com/e/pg_cardano) [`rdkit`](https://ext.pgsty.com/e/rdkit) [`bloom`](https://ext.pgsty.com/e/bloom)
[**LANG**](https://ext.pgsty.com/cate/lang): [`pg_tle`](https://ext.pgsty.com/e/pg_tle) [`plv8`](https://ext.pgsty.com/e/plv8) [`pllua`](https://ext.pgsty.com/e/pllua) [`hstore_pllua`](https://ext.pgsty.com/e/hstore_pllua) [`plluau`](https://ext.pgsty.com/e/plluau) [`hstore_plluau`](https://ext.pgsty.com/e/hstore_plluau) [`plprql`](https://ext.pgsty.com/e/plprql) [`pldbgapi`](https://ext.pgsty.com/e/pldbgapi) [`plpgsql_check`](https://ext.pgsty.com/e/plpgsql_check) [`plprofiler`](https://ext.pgsty.com/e/plprofiler) [`plsh`](https://ext.pgsty.com/e/plsh) [`pljava`](https://ext.pgsty.com/e/pljava) [`plr`](https://ext.pgsty.com/e/plr) [`pgtap`](https://ext.pgsty.com/e/pgtap) [`faker`](https://ext.pgsty.com/e/faker) [`dbt2`](https://ext.pgsty.com/e/dbt2) [`pltcl`](https://ext.pgsty.com/e/pltcl) [`pltclu`](https://ext.pgsty.com/e/pltclu) [`plperl`](https://ext.pgsty.com/e/plperl) [`bool_plperl`](https://ext.pgsty.com/e/bool_plperl) [`hstore_plperl`](https://ext.pgsty.com/e/hstore_plperl) [`jsonb_plperl`](https://ext.pgsty.com/e/jsonb_plperl) [`plperlu`](https://ext.pgsty.com/e/plperlu) [`bool_plperlu`](https://ext.pgsty.com/e/bool_plperlu) [`jsonb_plperlu`](https://ext.pgsty.com/e/jsonb_plperlu) [`hstore_plperlu`](https://ext.pgsty.com/e/hstore_plperlu) [`plpgsql`](https://ext.pgsty.com/e/plpgsql) [`plpython3u`](https://ext.pgsty.com/e/plpython3u) [`jsonb_plpython3u`](https://ext.pgsty.com/e/jsonb_plpython3u) [`ltree_plpython3u`](https://ext.pgsty.com/e/ltree_plpython3u) [`hstore_plpython3u`](https://ext.pgsty.com/e/hstore_plpython3u)
[**TYPE**](https://ext.pgsty.com/cate/type): [`prefix`](https://ext.pgsty.com/e/prefix) [`semver`](https://ext.pgsty.com/e/semver) [`unit`](https://ext.pgsty.com/e/unit) [`md5hash`](https://ext.pgsty.com/e/md5hash) [`asn1oid`](https://ext.pgsty.com/e/asn1oid) [`roaringbitmap`](https://ext.pgsty.com/e/roaringbitmap) [`pgfaceting`](https://ext.pgsty.com/e/pgfaceting) [`pg_sphere`](https://ext.pgsty.com/e/pg_sphere) [`country`](https://ext.pgsty.com/e/country) [`currency`](https://ext.pgsty.com/e/currency) [`pgmp`](https://ext.pgsty.com/e/pgmp) [`numeral`](https://ext.pgsty.com/e/numeral) [`pg_rational`](https://ext.pgsty.com/e/pg_rational) [`uint`](https://ext.pgsty.com/e/uint) [`uint128`](https://ext.pgsty.com/e/uint128) [`ip4r`](https://ext.pgsty.com/e/ip4r) [`uri`](https://ext.pgsty.com/e/uri) [`pgemailaddr`](https://ext.pgsty.com/e/pgemailaddr) [`acl`](https://ext.pgsty.com/e/acl) [`debversion`](https://ext.pgsty.com/e/debversion) [`pg_rrule`](https://ext.pgsty.com/e/pg_rrule) [`timestamp9`](https://ext.pgsty.com/e/timestamp9) [`chkpass`](https://ext.pgsty.com/e/chkpass) [`isn`](https://ext.pgsty.com/e/isn) [`seg`](https://ext.pgsty.com/e/seg) [`cube`](https://ext.pgsty.com/e/cube) [`ltree`](https://ext.pgsty.com/e/ltree) [`hstore`](https://ext.pgsty.com/e/hstore) [`citext`](https://ext.pgsty.com/e/citext) [`xml2`](https://ext.pgsty.com/e/xml2)
[**FUNC**](https://ext.pgsty.com/cate/func): [`topn`](https://ext.pgsty.com/e/topn) [`gzip`](https://ext.pgsty.com/e/gzip) [`zstd`](https://ext.pgsty.com/e/zstd) [`http`](https://ext.pgsty.com/e/http) [`pg_net`](https://ext.pgsty.com/e/pg_net) [`pg_smtp_client`](https://ext.pgsty.com/e/pg_smtp_client) [`pg_html5_email_address`](https://ext.pgsty.com/e/pg_html5_email_address) [`pgsql_tweaks`](https://ext.pgsty.com/e/pgsql_tweaks) [`pg_extra_time`](https://ext.pgsty.com/e/pg_extra_time) [`timeit`](https://ext.pgsty.com/e/timeit) [`count_distinct`](https://ext.pgsty.com/e/count_distinct) [`extra_window_functions`](https://ext.pgsty.com/e/extra_window_functions) [`first_last_agg`](https://ext.pgsty.com/e/first_last_agg) [`tdigest`](https://ext.pgsty.com/e/tdigest) [`aggs_for_vecs`](https://ext.pgsty.com/e/aggs_for_vecs) [`aggs_for_arrays`](https://ext.pgsty.com/e/aggs_for_arrays) [`arraymath`](https://ext.pgsty.com/e/arraymath) [`quantile`](https://ext.pgsty.com/e/quantile) [`lower_quantile`](https://ext.pgsty.com/e/lower_quantile) [`pg_idkit`](https://ext.pgsty.com/e/pg_idkit) [`pg_uuidv7`](https://ext.pgsty.com/e/pg_uuidv7) [`permuteseq`](https://ext.pgsty.com/e/permuteseq) [`pg_hashids`](https://ext.pgsty.com/e/pg_hashids) [`sequential_uuids`](https://ext.pgsty.com/e/sequential_uuids) [`pg_math`](https://ext.pgsty.com/e/pg_math) [`random`](https://ext.pgsty.com/e/random) [`base36`](https://ext.pgsty.com/e/base36) [`base62`](https://ext.pgsty.com/e/base62) [`pg_base58`](https://ext.pgsty.com/e/pg_base58) [`floatvec`](https://ext.pgsty.com/e/floatvec) [`financial`](https://ext.pgsty.com/e/financial) [`pgjwt`](https://ext.pgsty.com/e/pgjwt) [`pg_hashlib`](https://ext.pgsty.com/e/pg_hashlib) [`shacrypt`](https://ext.pgsty.com/e/shacrypt) [`cryptint`](https://ext.pgsty.com/e/cryptint) [`pguecc`](https://ext.pgsty.com/e/pguecc) [`pgpcre`](https://ext.pgsty.com/e/pgpcre) [`icu_ext`](https://ext.pgsty.com/e/icu_ext) [`pgqr`](https://ext.pgsty.com/e/pgqr) [`envvar`](https://ext.pgsty.com/e/envvar) [`pg_protobuf`](https://ext.pgsty.com/e/pg_protobuf) [`url_encode`](https://ext.pgsty.com/e/url_encode) [`refint`](https://ext.pgsty.com/e/refint) [`autoinc`](https://ext.pgsty.com/e/autoinc) [`insert_username`](https://ext.pgsty.com/e/insert_username) [`moddatetime`](https://ext.pgsty.com/e/moddatetime) [`tsm_system_time`](https://ext.pgsty.com/e/tsm_system_time) [`dict_xsyn`](https://ext.pgsty.com/e/dict_xsyn) [`tsm_system_rows`](https://ext.pgsty.com/e/tsm_system_rows) [`tcn`](https://ext.pgsty.com/e/tcn) [`uuid-ossp`](https://ext.pgsty.com/e/uuid-ossp) [`btree_gist`](https://ext.pgsty.com/e/btree_gist) [`btree_gin`](https://ext.pgsty.com/e/btree_gin) [`intarray`](https://ext.pgsty.com/e/intarray) [`intagg`](https://ext.pgsty.com/e/intagg) [`dict_int`](https://ext.pgsty.com/e/dict_int) [`unaccent`](https://ext.pgsty.com/e/unaccent)
[**ADMIN**](https://ext.pgsty.com/cate/admin): [`pg_repack`](https://ext.pgsty.com/e/pg_repack) [`pg_squeeze`](https://ext.pgsty.com/e/pg_squeeze) [`pg_dirtyread`](https://ext.pgsty.com/e/pg_dirtyread) [`pgfincore`](https://ext.pgsty.com/e/pgfincore) [`pgdd`](https://ext.pgsty.com/e/pgdd) [`ddlx`](https://ext.pgsty.com/e/ddlx) [`prioritize`](https://ext.pgsty.com/e/prioritize) [`pg_checksums`](https://ext.pgsty.com/e/pg_checksums) [`pg_readonly`](https://ext.pgsty.com/e/pg_readonly) [`safeupdate`](https://ext.pgsty.com/e/safeupdate) [`pg_permissions`](https://ext.pgsty.com/e/pg_permissions) [`pgautofailover`](https://ext.pgsty.com/e/pgautofailover) [`pg_catcheck`](https://ext.pgsty.com/e/pg_catcheck) [`pre_prepare`](https://ext.pgsty.com/e/pre_prepare) [`pgcozy`](https://ext.pgsty.com/e/pgcozy) [`pg_orphaned`](https://ext.pgsty.com/e/pg_orphaned) [`pg_crash`](https://ext.pgsty.com/e/pg_crash) [`pg_cheat_funcs`](https://ext.pgsty.com/e/pg_cheat_funcs) [`pg_savior`](https://ext.pgsty.com/e/pg_savior) [`table_log`](https://ext.pgsty.com/e/table_log) [`pg_fio`](https://ext.pgsty.com/e/pg_fio) [`pgpool_adm`](https://ext.pgsty.com/e/pgpool_adm) [`pgpool_recovery`](https://ext.pgsty.com/e/pgpool_recovery) [`pgpool_regclass`](https://ext.pgsty.com/e/pgpool_regclass) [`pgagent`](https://ext.pgsty.com/e/pgagent) [`vacuumlo`](https://ext.pgsty.com/e/vacuumlo) [`pg_prewarm`](https://ext.pgsty.com/e/pg_prewarm) [`oid2name`](https://ext.pgsty.com/e/oid2name) [`lo`](https://ext.pgsty.com/e/lo) [`basic_archive`](https://ext.pgsty.com/e/basic_archive) [`basebackup_to_shell`](https://ext.pgsty.com/e/basebackup_to_shell) [`old_snapshot`](https://ext.pgsty.com/e/old_snapshot) [`adminpack`](https://ext.pgsty.com/e/adminpack) [`amcheck`](https://ext.pgsty.com/e/amcheck) [`pg_surgery`](https://ext.pgsty.com/e/pg_surgery)
[**STAT**](https://ext.pgsty.com/cate/stat): [`pg_profile`](https://ext.pgsty.com/e/pg_profile) [`pg_show_plans`](https://ext.pgsty.com/e/pg_show_plans) [`pg_stat_kcache`](https://ext.pgsty.com/e/pg_stat_kcache) [`pg_stat_monitor`](https://ext.pgsty.com/e/pg_stat_monitor) [`pg_qualstats`](https://ext.pgsty.com/e/pg_qualstats) [`pg_store_plans`](https://ext.pgsty.com/e/pg_store_plans) [`pg_track_settings`](https://ext.pgsty.com/e/pg_track_settings) [`pg_wait_sampling`](https://ext.pgsty.com/e/pg_wait_sampling) [`system_stats`](https://ext.pgsty.com/e/system_stats) [`meta`](https://ext.pgsty.com/e/meta) [`pgnodemx`](https://ext.pgsty.com/e/pgnodemx) [`pg_proctab`](https://ext.pgsty.com/e/pg_proctab) [`pg_sqlog`](https://ext.pgsty.com/e/pg_sqlog) [`bgw_replstatus`](https://ext.pgsty.com/e/bgw_replstatus) [`pgmeminfo`](https://ext.pgsty.com/e/pgmeminfo) [`toastinfo`](https://ext.pgsty.com/e/toastinfo) [`explain_ui`](https://ext.pgsty.com/e/explain_ui) [`pg_relusage`](https://ext.pgsty.com/e/pg_relusage) [`pg_top`](https://ext.pgsty.com/e/pg_top) [`pagevis`](https://ext.pgsty.com/e/pagevis) [`powa`](https://ext.pgsty.com/e/powa) [`pageinspect`](https://ext.pgsty.com/e/pageinspect) [`pgrowlocks`](https://ext.pgsty.com/e/pgrowlocks) [`sslinfo`](https://ext.pgsty.com/e/sslinfo) [`pg_buffercache`](https://ext.pgsty.com/e/pg_buffercache) [`pg_walinspect`](https://ext.pgsty.com/e/pg_walinspect) [`pg_freespacemap`](https://ext.pgsty.com/e/pg_freespacemap) [`pg_visibility`](https://ext.pgsty.com/e/pg_visibility) [`pgstattuple`](https://ext.pgsty.com/e/pgstattuple) [`auto_explain`](https://ext.pgsty.com/e/auto_explain) [`pg_stat_statements`](https://ext.pgsty.com/e/pg_stat_statements)
[**SEC**](https://ext.pgsty.com/cate/sec): [`passwordcheck_cracklib`](https://ext.pgsty.com/e/passwordcheck_cracklib) [`supautils`](https://ext.pgsty.com/e/supautils) [`pgsodium`](https://ext.pgsty.com/e/pgsodium) [`supabase_vault`](https://ext.pgsty.com/e/supabase_vault) [`pg_session_jwt`](https://ext.pgsty.com/e/pg_session_jwt) [`anon`](https://ext.pgsty.com/e/anon) [`pg_tde`](https://ext.pgsty.com/e/pg_tde) [`pgsmcrypto`](https://ext.pgsty.com/e/pgsmcrypto) [`pgaudit`](https://ext.pgsty.com/e/pgaudit) [`pgauditlogtofile`](https://ext.pgsty.com/e/pgauditlogtofile) [`pg_auth_mon`](https://ext.pgsty.com/e/pg_auth_mon) [`credcheck`](https://ext.pgsty.com/e/credcheck) [`pgcryptokey`](https://ext.pgsty.com/e/pgcryptokey) [`pg_jobmon`](https://ext.pgsty.com/e/pg_jobmon) [`logerrors`](https://ext.pgsty.com/e/logerrors) [`login_hook`](https://ext.pgsty.com/e/login_hook) [`set_user`](https://ext.pgsty.com/e/set_user) [`pg_snakeoil`](https://ext.pgsty.com/e/pg_snakeoil) [`pgextwlist`](https://ext.pgsty.com/e/pgextwlist) [`pg_auditor`](https://ext.pgsty.com/e/pg_auditor) [`sslutils`](https://ext.pgsty.com/e/sslutils) [`noset`](https://ext.pgsty.com/e/noset) [`sepgsql`](https://ext.pgsty.com/e/sepgsql) [`auth_delay`](https://ext.pgsty.com/e/auth_delay) [`pgcrypto`](https://ext.pgsty.com/e/pgcrypto) [`passwordcheck`](https://ext.pgsty.com/e/passwordcheck)
[**FDW**](https://ext.pgsty.com/cate/fdw): [`wrappers`](https://ext.pgsty.com/e/wrappers) [`multicorn`](https://ext.pgsty.com/e/multicorn) [`odbc_fdw`](https://ext.pgsty.com/e/odbc_fdw) [`jdbc_fdw`](https://ext.pgsty.com/e/jdbc_fdw) [`mysql_fdw`](https://ext.pgsty.com/e/mysql_fdw) [`oracle_fdw`](https://ext.pgsty.com/e/oracle_fdw) [`tds_fdw`](https://ext.pgsty.com/e/tds_fdw) [`db2_fdw`](https://ext.pgsty.com/e/db2_fdw) [`sqlite_fdw`](https://ext.pgsty.com/e/sqlite_fdw) [`pgbouncer_fdw`](https://ext.pgsty.com/e/pgbouncer_fdw) [`mongo_fdw`](https://ext.pgsty.com/e/mongo_fdw) [`redis_fdw`](https://ext.pgsty.com/e/redis_fdw) [`redis`](https://ext.pgsty.com/e/redis) [`kafka_fdw`](https://ext.pgsty.com/e/kafka_fdw) [`hdfs_fdw`](https://ext.pgsty.com/e/hdfs_fdw) [`firebird_fdw`](https://ext.pgsty.com/e/firebird_fdw) [`aws_s3`](https://ext.pgsty.com/e/aws_s3) [`log_fdw`](https://ext.pgsty.com/e/log_fdw) [`dblink`](https://ext.pgsty.com/e/dblink) [`file_fdw`](https://ext.pgsty.com/e/file_fdw) [`postgres_fdw`](https://ext.pgsty.com/e/postgres_fdw)
[**SIM**](https://ext.pgsty.com/cate/sim): [`orafce`](https://ext.pgsty.com/e/orafce) [`pgtt`](https://ext.pgsty.com/e/pgtt) [`session_variable`](https://ext.pgsty.com/e/session_variable) [`pg_statement_rollback`](https://ext.pgsty.com/e/pg_statement_rollback) [`pg_dbms_metadata`](https://ext.pgsty.com/e/pg_dbms_metadata) [`pg_dbms_lock`](https://ext.pgsty.com/e/pg_dbms_lock) [`pg_dbms_job`](https://ext.pgsty.com/e/pg_dbms_job) [`babelfishpg_common`](https://ext.pgsty.com/e/babelfishpg_common) [`babelfishpg_tsql`](https://ext.pgsty.com/e/babelfishpg_tsql) [`babelfishpg_tds`](https://ext.pgsty.com/e/babelfishpg_tds) [`babelfishpg_money`](https://ext.pgsty.com/e/babelfishpg_money) [`pgmemcache`](https://ext.pgsty.com/e/pgmemcache)
[**ETL**](https://ext.pgsty.com/cate/etl): [`pglogical`](https://ext.pgsty.com/e/pglogical) [`pglogical_origin`](https://ext.pgsty.com/e/pglogical_origin) [`pglogical_ticker`](https://ext.pgsty.com/e/pglogical_ticker) [`pgl_ddl_deploy`](https://ext.pgsty.com/e/pgl_ddl_deploy) [`pg_failover_slots`](https://ext.pgsty.com/e/pg_failover_slots) [`wal2json`](https://ext.pgsty.com/e/wal2json) [`wal2mongo`](https://ext.pgsty.com/e/wal2mongo) [`decoderbufs`](https://ext.pgsty.com/e/decoderbufs) [`decoder_raw`](https://ext.pgsty.com/e/decoder_raw) [`test_decoding`](https://ext.pgsty.com/e/test_decoding) [`mimeo`](https://ext.pgsty.com/e/mimeo) [`repmgr`](https://ext.pgsty.com/e/repmgr) [`pg_fact_loader`](https://ext.pgsty.com/e/pg_fact_loader) [`pg_bulkload`](https://ext.pgsty.com/e/pg_bulkload)

Check [ext.pigsty.io](https://ext.pigsty.io) for all the details.



--------

## Some Thoughts

Each major PostgreSQL version introduces changes, making the maintenance of **140+** extension packages a bit of a beast.

Especially when some extension authors haven’t updated their work in years. In these cases, you often have no choice but to take matters into your own hands.
I’ve personally fixed several extensions and ensured they support the latest PostgreSQL major versions. For those authors I could reach, I’ve submitted numerous PRs and issues to keep things moving forward.

<a href="https://github.com/Vonng"><img src="github-contrib.png" style="max-width: 800px; width: 100%; height: auto;"></a>

Back to the point: **my goal with this repo is to establish a standard for PostgreSQL extension installation and distribution, solving the distribution challenges that have long troubles the users**.

A recent milestone is that, the popular open-source PostgreSQL HA cluster project [**postgresql_cluster**](https://autobase.tech/docs/extensions/list), has made this extension repository the default upstream for PG extension installation.

Currently, this repository (repo.pigsty.io) is hosted on Cloudflare. In the past month, the repo and its mirrors have served about **300GB** of downloads.
Given that most extensions are just a few KB to a few MB, that amounts to nearly **a million downloads per month**.
Since Cloudflare doesn’t charge for traffic, I can confidently commit to keeping this repository completely free & under active maintenance for the foreseeable future, as long as cloudflare doesn't charge me too much.

I believe my work can help PostgreSQL users worldwide and contribute to the thriving PostgreSQL ecosystem. I hope it proves useful to you as well. **Enjoy PostgreSQL!**
