---
title: The idea way to install PostgreSQL Extensions
linkTitle: "The idea way to install PG Extension"
date: 2024-11-02
author: |
  [Vonng](https://vonng.com)([@Vonng](https://vonng.com/en/))
summary: >
  PostgreSQL Is Eating the Database World through the power of extensibility. With 390 extensions powering PG, we may not say it's invincible, but it’s definitely getting much closer.
tags: [PostgreSQL,Ecosystem,Extension]
---

[**PostgreSQL Is Eating the Database World**](/blog/pg/pg-eat-db-world) through the power of **extensibility**.
With **390** extensions powering PostgreSQL, we may not say it's invincible, but it’s definitely getting much closer.

I believe the PostgreSQL community has reached a consensus on the importance of extensions.
So the real question now becomes: **"What should we do about it?"**

What's the primary problem with PostgreSQL extensions? In my opinion, it’s their **accessibility**.
Extensions are useless if most users can’t easily install and enable them. But it's not that easy.

Even the largest cloud postgres vendors are struggling with this.
They have some inherent limitations (multi-tenancy, security, licensing) that make it hard for them to fully address this issue.

So here's my plan, I've created a [**repository**](https://ext.pigsty.io/) that hosts [**390**](https://ext.pigsty.io/#/list) of the most capable extensions in the PostgreSQL ecosystem,
available as RPM / DEB packages on mainstream Linux OS distros.  And the goal is to take PostgreSQL one solid step closer to becoming the all-powerful database and achieve **the great alignment** between the Debian and EL OS ecosystems.

> [**TL;DR: Take me to the HOW-TO part!**](#apt-repo)

<a href="/blog/pg/pg-eat-deb-world"><img src="/img/pigsty/ecosystem.jpg" style="max-width: 800px; max-height: 1000px; width: 100%; height: auto;"></a>



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
In addition to the **70** built-in [Contrib](https://ext.pigsty.io/#/contrib) extensions bundled with PostgreSQL,the PGDG YUM repo offers **128** RPM extensions, while the APT repo offers **104** DEB extensions.
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
| [**RPM**](https://ext.pigsty.io/#/rpm) | 334 | 115  |  143   |   70    |  4   |  6   | 301  | 330  | 333  | 319  | 307  | 294  |
| [**DEB**](https://ext.pigsty.io/#/deb) | 326 | 104  |  144   |   70    |  4   |  14  | 302  | 322  | 325  | 316  | 303  | 293  |

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
[![Debian Support: 12](https://img.shields.io/badge/Debian-12/bookworm-%23A81D33?style=flat&logo=debian&logoColor=%23A81D33)](https://pigsty.io/docs/reference/compatibility/)

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


[**TIME**](https://ext.pigsty.io/#/time): [`timescaledb`](https://ext.pigsty.io/#/timescaledb) [`timescaledb_toolkit`](https://ext.pigsty.io/#/timescaledb_toolkit) [`timeseries`](https://ext.pigsty.io/#/timeseries) [`periods`](https://ext.pigsty.io/#/periods) [`temporal_tables`](https://ext.pigsty.io/#/temporal_tables) [`emaj`](https://ext.pigsty.io/#/emaj) [`table_version`](https://ext.pigsty.io/#/table_version) [`pg_cron`](https://ext.pigsty.io/#/pg_cron) [`pg_later`](https://ext.pigsty.io/#/pg_later) [`pg_background`](https://ext.pigsty.io/#/pg_background)
[**GIS**](https://ext.pigsty.io/#/gis): [`postgis`](https://ext.pigsty.io/#/postgis) [`postgis_topology`](https://ext.pigsty.io/#/postgis_topology) [`postgis_raster`](https://ext.pigsty.io/#/postgis_raster) [`postgis_sfcgal`](https://ext.pigsty.io/#/postgis_sfcgal) [`postgis_tiger_geocoder`](https://ext.pigsty.io/#/postgis_tiger_geocoder) [`address_standardizer`](https://ext.pigsty.io/#/address_standardizer) [`address_standardizer_data_us`](https://ext.pigsty.io/#/address_standardizer_data_us) [`pgrouting`](https://ext.pigsty.io/#/pgrouting) [`pointcloud`](https://ext.pigsty.io/#/pointcloud) [`pointcloud_postgis`](https://ext.pigsty.io/#/pointcloud_postgis) [`h3`](https://ext.pigsty.io/#/h3) [`h3_postgis`](https://ext.pigsty.io/#/h3_postgis) [`q3c`](https://ext.pigsty.io/#/q3c) [`ogr_fdw`](https://ext.pigsty.io/#/ogr_fdw) [`geoip`](https://ext.pigsty.io/#/geoip) [`pg_polyline`](https://ext.pigsty.io/#/pg_polyline) [`pg_geohash`](https://ext.pigsty.io/#/pg_geohash) [`mobilitydb`](https://ext.pigsty.io/#/mobilitydb) [`earthdistance`](https://ext.pigsty.io/#/earthdistance)
[**RAG**](https://ext.pigsty.io/#/rag): [`vector`](https://ext.pigsty.io/#/vector) [`vectorscale`](https://ext.pigsty.io/#/vectorscale) [`vectorize`](https://ext.pigsty.io/#/vectorize) [`pg_similarity`](https://ext.pigsty.io/#/pg_similarity) [`smlar`](https://ext.pigsty.io/#/smlar) [`pg_summarize`](https://ext.pigsty.io/#/pg_summarize) [`pg_tiktoken`](https://ext.pigsty.io/#/pg_tiktoken) [`pgml`](https://ext.pigsty.io/#/pgml) [`pg4ml`](https://ext.pigsty.io/#/pg4ml)
[**FTS**](https://ext.pigsty.io/#/fts): [`pg_search`](https://ext.pigsty.io/#/pg_search) [`pg_bigm`](https://ext.pigsty.io/#/pg_bigm) [`zhparser`](https://ext.pigsty.io/#/zhparser) [`hunspell_cs_cz`](https://ext.pigsty.io/#/hunspell_cs_cz) [`hunspell_de_de`](https://ext.pigsty.io/#/hunspell_de_de) [`hunspell_en_us`](https://ext.pigsty.io/#/hunspell_en_us) [`hunspell_fr`](https://ext.pigsty.io/#/hunspell_fr) [`hunspell_ne_np`](https://ext.pigsty.io/#/hunspell_ne_np) [`hunspell_nl_nl`](https://ext.pigsty.io/#/hunspell_nl_nl) [`hunspell_nn_no`](https://ext.pigsty.io/#/hunspell_nn_no) [`hunspell_pt_pt`](https://ext.pigsty.io/#/hunspell_pt_pt) [`hunspell_ru_ru`](https://ext.pigsty.io/#/hunspell_ru_ru) [`hunspell_ru_ru_aot`](https://ext.pigsty.io/#/hunspell_ru_ru_aot) [`fuzzystrmatch`](https://ext.pigsty.io/#/fuzzystrmatch) [`pg_trgm`](https://ext.pigsty.io/#/pg_trgm)
[**OLAP**](https://ext.pigsty.io/#/olap): [`citus`](https://ext.pigsty.io/#/citus) [`citus_columnar`](https://ext.pigsty.io/#/citus_columnar) [`columnar`](https://ext.pigsty.io/#/columnar) [`pg_analytics`](https://ext.pigsty.io/#/pg_analytics) [`pg_duckdb`](https://ext.pigsty.io/#/pg_duckdb) [`pg_mooncake`](https://ext.pigsty.io/#/pg_mooncake) [`duckdb_fdw`](https://ext.pigsty.io/#/duckdb_fdw) [`pg_parquet`](https://ext.pigsty.io/#/pg_parquet) [`pg_fkpart`](https://ext.pigsty.io/#/pg_fkpart) [`pg_partman`](https://ext.pigsty.io/#/pg_partman) [`plproxy`](https://ext.pigsty.io/#/plproxy) [`pg_strom`](https://ext.pigsty.io/#/pg_strom) [`tablefunc`](https://ext.pigsty.io/#/tablefunc)
[**FEAT**](https://ext.pigsty.io/#/feat): [`age`](https://ext.pigsty.io/#/age) [`hll`](https://ext.pigsty.io/#/hll) [`rum`](https://ext.pigsty.io/#/rum) [`pg_graphql`](https://ext.pigsty.io/#/pg_graphql) [`pg_jsonschema`](https://ext.pigsty.io/#/pg_jsonschema) [`jsquery`](https://ext.pigsty.io/#/jsquery) [`pg_hint_plan`](https://ext.pigsty.io/#/pg_hint_plan) [`hypopg`](https://ext.pigsty.io/#/hypopg) [`index_advisor`](https://ext.pigsty.io/#/index_advisor) [`plan_filter`](https://ext.pigsty.io/#/plan_filter) [`imgsmlr`](https://ext.pigsty.io/#/imgsmlr) [`pg_ivm`](https://ext.pigsty.io/#/pg_ivm) [`pgmq`](https://ext.pigsty.io/#/pgmq) [`pgq`](https://ext.pigsty.io/#/pgq) [`pg_cardano`](https://ext.pigsty.io/#/pg_cardano) [`rdkit`](https://ext.pigsty.io/#/rdkit) [`bloom`](https://ext.pigsty.io/#/bloom)
[**LANG**](https://ext.pigsty.io/#/lang): [`pg_tle`](https://ext.pigsty.io/#/pg_tle) [`plv8`](https://ext.pigsty.io/#/plv8) [`pllua`](https://ext.pigsty.io/#/pllua) [`hstore_pllua`](https://ext.pigsty.io/#/hstore_pllua) [`plluau`](https://ext.pigsty.io/#/plluau) [`hstore_plluau`](https://ext.pigsty.io/#/hstore_plluau) [`plprql`](https://ext.pigsty.io/#/plprql) [`pldbgapi`](https://ext.pigsty.io/#/pldbgapi) [`plpgsql_check`](https://ext.pigsty.io/#/plpgsql_check) [`plprofiler`](https://ext.pigsty.io/#/plprofiler) [`plsh`](https://ext.pigsty.io/#/plsh) [`pljava`](https://ext.pigsty.io/#/pljava) [`plr`](https://ext.pigsty.io/#/plr) [`pgtap`](https://ext.pigsty.io/#/pgtap) [`faker`](https://ext.pigsty.io/#/faker) [`dbt2`](https://ext.pigsty.io/#/dbt2) [`pltcl`](https://ext.pigsty.io/#/pltcl) [`pltclu`](https://ext.pigsty.io/#/pltclu) [`plperl`](https://ext.pigsty.io/#/plperl) [`bool_plperl`](https://ext.pigsty.io/#/bool_plperl) [`hstore_plperl`](https://ext.pigsty.io/#/hstore_plperl) [`jsonb_plperl`](https://ext.pigsty.io/#/jsonb_plperl) [`plperlu`](https://ext.pigsty.io/#/plperlu) [`bool_plperlu`](https://ext.pigsty.io/#/bool_plperlu) [`jsonb_plperlu`](https://ext.pigsty.io/#/jsonb_plperlu) [`hstore_plperlu`](https://ext.pigsty.io/#/hstore_plperlu) [`plpgsql`](https://ext.pigsty.io/#/plpgsql) [`plpython3u`](https://ext.pigsty.io/#/plpython3u) [`jsonb_plpython3u`](https://ext.pigsty.io/#/jsonb_plpython3u) [`ltree_plpython3u`](https://ext.pigsty.io/#/ltree_plpython3u) [`hstore_plpython3u`](https://ext.pigsty.io/#/hstore_plpython3u)
[**TYPE**](https://ext.pigsty.io/#/type): [`prefix`](https://ext.pigsty.io/#/prefix) [`semver`](https://ext.pigsty.io/#/semver) [`unit`](https://ext.pigsty.io/#/unit) [`md5hash`](https://ext.pigsty.io/#/md5hash) [`asn1oid`](https://ext.pigsty.io/#/asn1oid) [`roaringbitmap`](https://ext.pigsty.io/#/roaringbitmap) [`pgfaceting`](https://ext.pigsty.io/#/pgfaceting) [`pg_sphere`](https://ext.pigsty.io/#/pg_sphere) [`country`](https://ext.pigsty.io/#/country) [`currency`](https://ext.pigsty.io/#/currency) [`pgmp`](https://ext.pigsty.io/#/pgmp) [`numeral`](https://ext.pigsty.io/#/numeral) [`pg_rational`](https://ext.pigsty.io/#/pg_rational) [`uint`](https://ext.pigsty.io/#/uint) [`uint128`](https://ext.pigsty.io/#/uint128) [`ip4r`](https://ext.pigsty.io/#/ip4r) [`uri`](https://ext.pigsty.io/#/uri) [`pgemailaddr`](https://ext.pigsty.io/#/pgemailaddr) [`acl`](https://ext.pigsty.io/#/acl) [`debversion`](https://ext.pigsty.io/#/debversion) [`pg_rrule`](https://ext.pigsty.io/#/pg_rrule) [`timestamp9`](https://ext.pigsty.io/#/timestamp9) [`chkpass`](https://ext.pigsty.io/#/chkpass) [`isn`](https://ext.pigsty.io/#/isn) [`seg`](https://ext.pigsty.io/#/seg) [`cube`](https://ext.pigsty.io/#/cube) [`ltree`](https://ext.pigsty.io/#/ltree) [`hstore`](https://ext.pigsty.io/#/hstore) [`citext`](https://ext.pigsty.io/#/citext) [`xml2`](https://ext.pigsty.io/#/xml2)
[**FUNC**](https://ext.pigsty.io/#/func): [`topn`](https://ext.pigsty.io/#/topn) [`gzip`](https://ext.pigsty.io/#/gzip) [`zstd`](https://ext.pigsty.io/#/zstd) [`http`](https://ext.pigsty.io/#/http) [`pg_net`](https://ext.pigsty.io/#/pg_net) [`pg_smtp_client`](https://ext.pigsty.io/#/pg_smtp_client) [`pg_html5_email_address`](https://ext.pigsty.io/#/pg_html5_email_address) [`pgsql_tweaks`](https://ext.pigsty.io/#/pgsql_tweaks) [`pg_extra_time`](https://ext.pigsty.io/#/pg_extra_time) [`timeit`](https://ext.pigsty.io/#/timeit) [`count_distinct`](https://ext.pigsty.io/#/count_distinct) [`extra_window_functions`](https://ext.pigsty.io/#/extra_window_functions) [`first_last_agg`](https://ext.pigsty.io/#/first_last_agg) [`tdigest`](https://ext.pigsty.io/#/tdigest) [`aggs_for_vecs`](https://ext.pigsty.io/#/aggs_for_vecs) [`aggs_for_arrays`](https://ext.pigsty.io/#/aggs_for_arrays) [`arraymath`](https://ext.pigsty.io/#/arraymath) [`quantile`](https://ext.pigsty.io/#/quantile) [`lower_quantile`](https://ext.pigsty.io/#/lower_quantile) [`pg_idkit`](https://ext.pigsty.io/#/pg_idkit) [`pg_uuidv7`](https://ext.pigsty.io/#/pg_uuidv7) [`permuteseq`](https://ext.pigsty.io/#/permuteseq) [`pg_hashids`](https://ext.pigsty.io/#/pg_hashids) [`sequential_uuids`](https://ext.pigsty.io/#/sequential_uuids) [`pg_math`](https://ext.pigsty.io/#/pg_math) [`random`](https://ext.pigsty.io/#/random) [`base36`](https://ext.pigsty.io/#/base36) [`base62`](https://ext.pigsty.io/#/base62) [`pg_base58`](https://ext.pigsty.io/#/pg_base58) [`floatvec`](https://ext.pigsty.io/#/floatvec) [`financial`](https://ext.pigsty.io/#/financial) [`pgjwt`](https://ext.pigsty.io/#/pgjwt) [`pg_hashlib`](https://ext.pigsty.io/#/pg_hashlib) [`shacrypt`](https://ext.pigsty.io/#/shacrypt) [`cryptint`](https://ext.pigsty.io/#/cryptint) [`pguecc`](https://ext.pigsty.io/#/pguecc) [`pgpcre`](https://ext.pigsty.io/#/pgpcre) [`icu_ext`](https://ext.pigsty.io/#/icu_ext) [`pgqr`](https://ext.pigsty.io/#/pgqr) [`envvar`](https://ext.pigsty.io/#/envvar) [`pg_protobuf`](https://ext.pigsty.io/#/pg_protobuf) [`url_encode`](https://ext.pigsty.io/#/url_encode) [`refint`](https://ext.pigsty.io/#/refint) [`autoinc`](https://ext.pigsty.io/#/autoinc) [`insert_username`](https://ext.pigsty.io/#/insert_username) [`moddatetime`](https://ext.pigsty.io/#/moddatetime) [`tsm_system_time`](https://ext.pigsty.io/#/tsm_system_time) [`dict_xsyn`](https://ext.pigsty.io/#/dict_xsyn) [`tsm_system_rows`](https://ext.pigsty.io/#/tsm_system_rows) [`tcn`](https://ext.pigsty.io/#/tcn) [`uuid-ossp`](https://ext.pigsty.io/#/uuid-ossp) [`btree_gist`](https://ext.pigsty.io/#/btree_gist) [`btree_gin`](https://ext.pigsty.io/#/btree_gin) [`intarray`](https://ext.pigsty.io/#/intarray) [`intagg`](https://ext.pigsty.io/#/intagg) [`dict_int`](https://ext.pigsty.io/#/dict_int) [`unaccent`](https://ext.pigsty.io/#/unaccent)
[**ADMIN**](https://ext.pigsty.io/#/admin): [`pg_repack`](https://ext.pigsty.io/#/pg_repack) [`pg_squeeze`](https://ext.pigsty.io/#/pg_squeeze) [`pg_dirtyread`](https://ext.pigsty.io/#/pg_dirtyread) [`pgfincore`](https://ext.pigsty.io/#/pgfincore) [`pgdd`](https://ext.pigsty.io/#/pgdd) [`ddlx`](https://ext.pigsty.io/#/ddlx) [`prioritize`](https://ext.pigsty.io/#/prioritize) [`pg_checksums`](https://ext.pigsty.io/#/pg_checksums) [`pg_readonly`](https://ext.pigsty.io/#/pg_readonly) [`safeupdate`](https://ext.pigsty.io/#/safeupdate) [`pg_permissions`](https://ext.pigsty.io/#/pg_permissions) [`pgautofailover`](https://ext.pigsty.io/#/pgautofailover) [`pg_catcheck`](https://ext.pigsty.io/#/pg_catcheck) [`pre_prepare`](https://ext.pigsty.io/#/pre_prepare) [`pgcozy`](https://ext.pigsty.io/#/pgcozy) [`pg_orphaned`](https://ext.pigsty.io/#/pg_orphaned) [`pg_crash`](https://ext.pigsty.io/#/pg_crash) [`pg_cheat_funcs`](https://ext.pigsty.io/#/pg_cheat_funcs) [`pg_savior`](https://ext.pigsty.io/#/pg_savior) [`table_log`](https://ext.pigsty.io/#/table_log) [`pg_fio`](https://ext.pigsty.io/#/pg_fio) [`pgpool_adm`](https://ext.pigsty.io/#/pgpool_adm) [`pgpool_recovery`](https://ext.pigsty.io/#/pgpool_recovery) [`pgpool_regclass`](https://ext.pigsty.io/#/pgpool_regclass) [`pgagent`](https://ext.pigsty.io/#/pgagent) [`vacuumlo`](https://ext.pigsty.io/#/vacuumlo) [`pg_prewarm`](https://ext.pigsty.io/#/pg_prewarm) [`oid2name`](https://ext.pigsty.io/#/oid2name) [`lo`](https://ext.pigsty.io/#/lo) [`basic_archive`](https://ext.pigsty.io/#/basic_archive) [`basebackup_to_shell`](https://ext.pigsty.io/#/basebackup_to_shell) [`old_snapshot`](https://ext.pigsty.io/#/old_snapshot) [`adminpack`](https://ext.pigsty.io/#/adminpack) [`amcheck`](https://ext.pigsty.io/#/amcheck) [`pg_surgery`](https://ext.pigsty.io/#/pg_surgery)
[**STAT**](https://ext.pigsty.io/#/stat): [`pg_profile`](https://ext.pigsty.io/#/pg_profile) [`pg_show_plans`](https://ext.pigsty.io/#/pg_show_plans) [`pg_stat_kcache`](https://ext.pigsty.io/#/pg_stat_kcache) [`pg_stat_monitor`](https://ext.pigsty.io/#/pg_stat_monitor) [`pg_qualstats`](https://ext.pigsty.io/#/pg_qualstats) [`pg_store_plans`](https://ext.pigsty.io/#/pg_store_plans) [`pg_track_settings`](https://ext.pigsty.io/#/pg_track_settings) [`pg_wait_sampling`](https://ext.pigsty.io/#/pg_wait_sampling) [`system_stats`](https://ext.pigsty.io/#/system_stats) [`meta`](https://ext.pigsty.io/#/meta) [`pgnodemx`](https://ext.pigsty.io/#/pgnodemx) [`pg_proctab`](https://ext.pigsty.io/#/pg_proctab) [`pg_sqlog`](https://ext.pigsty.io/#/pg_sqlog) [`bgw_replstatus`](https://ext.pigsty.io/#/bgw_replstatus) [`pgmeminfo`](https://ext.pigsty.io/#/pgmeminfo) [`toastinfo`](https://ext.pigsty.io/#/toastinfo) [`explain_ui`](https://ext.pigsty.io/#/explain_ui) [`pg_relusage`](https://ext.pigsty.io/#/pg_relusage) [`pg_top`](https://ext.pigsty.io/#/pg_top) [`pagevis`](https://ext.pigsty.io/#/pagevis) [`powa`](https://ext.pigsty.io/#/powa) [`pageinspect`](https://ext.pigsty.io/#/pageinspect) [`pgrowlocks`](https://ext.pigsty.io/#/pgrowlocks) [`sslinfo`](https://ext.pigsty.io/#/sslinfo) [`pg_buffercache`](https://ext.pigsty.io/#/pg_buffercache) [`pg_walinspect`](https://ext.pigsty.io/#/pg_walinspect) [`pg_freespacemap`](https://ext.pigsty.io/#/pg_freespacemap) [`pg_visibility`](https://ext.pigsty.io/#/pg_visibility) [`pgstattuple`](https://ext.pigsty.io/#/pgstattuple) [`auto_explain`](https://ext.pigsty.io/#/auto_explain) [`pg_stat_statements`](https://ext.pigsty.io/#/pg_stat_statements)
[**SEC**](https://ext.pigsty.io/#/sec): [`passwordcheck_cracklib`](https://ext.pigsty.io/#/passwordcheck_cracklib) [`supautils`](https://ext.pigsty.io/#/supautils) [`pgsodium`](https://ext.pigsty.io/#/pgsodium) [`supabase_vault`](https://ext.pigsty.io/#/supabase_vault) [`pg_session_jwt`](https://ext.pigsty.io/#/pg_session_jwt) [`anon`](https://ext.pigsty.io/#/anon) [`pg_tde`](https://ext.pigsty.io/#/pg_tde) [`pgsmcrypto`](https://ext.pigsty.io/#/pgsmcrypto) [`pgaudit`](https://ext.pigsty.io/#/pgaudit) [`pgauditlogtofile`](https://ext.pigsty.io/#/pgauditlogtofile) [`pg_auth_mon`](https://ext.pigsty.io/#/pg_auth_mon) [`credcheck`](https://ext.pigsty.io/#/credcheck) [`pgcryptokey`](https://ext.pigsty.io/#/pgcryptokey) [`pg_jobmon`](https://ext.pigsty.io/#/pg_jobmon) [`logerrors`](https://ext.pigsty.io/#/logerrors) [`login_hook`](https://ext.pigsty.io/#/login_hook) [`set_user`](https://ext.pigsty.io/#/set_user) [`pg_snakeoil`](https://ext.pigsty.io/#/pg_snakeoil) [`pgextwlist`](https://ext.pigsty.io/#/pgextwlist) [`pg_auditor`](https://ext.pigsty.io/#/pg_auditor) [`sslutils`](https://ext.pigsty.io/#/sslutils) [`noset`](https://ext.pigsty.io/#/noset) [`sepgsql`](https://ext.pigsty.io/#/sepgsql) [`auth_delay`](https://ext.pigsty.io/#/auth_delay) [`pgcrypto`](https://ext.pigsty.io/#/pgcrypto) [`passwordcheck`](https://ext.pigsty.io/#/passwordcheck)
[**FDW**](https://ext.pigsty.io/#/fdw): [`wrappers`](https://ext.pigsty.io/#/wrappers) [`multicorn`](https://ext.pigsty.io/#/multicorn) [`odbc_fdw`](https://ext.pigsty.io/#/odbc_fdw) [`jdbc_fdw`](https://ext.pigsty.io/#/jdbc_fdw) [`mysql_fdw`](https://ext.pigsty.io/#/mysql_fdw) [`oracle_fdw`](https://ext.pigsty.io/#/oracle_fdw) [`tds_fdw`](https://ext.pigsty.io/#/tds_fdw) [`db2_fdw`](https://ext.pigsty.io/#/db2_fdw) [`sqlite_fdw`](https://ext.pigsty.io/#/sqlite_fdw) [`pgbouncer_fdw`](https://ext.pigsty.io/#/pgbouncer_fdw) [`mongo_fdw`](https://ext.pigsty.io/#/mongo_fdw) [`redis_fdw`](https://ext.pigsty.io/#/redis_fdw) [`redis`](https://ext.pigsty.io/#/redis) [`kafka_fdw`](https://ext.pigsty.io/#/kafka_fdw) [`hdfs_fdw`](https://ext.pigsty.io/#/hdfs_fdw) [`firebird_fdw`](https://ext.pigsty.io/#/firebird_fdw) [`aws_s3`](https://ext.pigsty.io/#/aws_s3) [`log_fdw`](https://ext.pigsty.io/#/log_fdw) [`dblink`](https://ext.pigsty.io/#/dblink) [`file_fdw`](https://ext.pigsty.io/#/file_fdw) [`postgres_fdw`](https://ext.pigsty.io/#/postgres_fdw)
[**SIM**](https://ext.pigsty.io/#/sim): [`orafce`](https://ext.pigsty.io/#/orafce) [`pgtt`](https://ext.pigsty.io/#/pgtt) [`session_variable`](https://ext.pigsty.io/#/session_variable) [`pg_statement_rollback`](https://ext.pigsty.io/#/pg_statement_rollback) [`pg_dbms_metadata`](https://ext.pigsty.io/#/pg_dbms_metadata) [`pg_dbms_lock`](https://ext.pigsty.io/#/pg_dbms_lock) [`pg_dbms_job`](https://ext.pigsty.io/#/pg_dbms_job) [`babelfishpg_common`](https://ext.pigsty.io/#/babelfishpg_common) [`babelfishpg_tsql`](https://ext.pigsty.io/#/babelfishpg_tsql) [`babelfishpg_tds`](https://ext.pigsty.io/#/babelfishpg_tds) [`babelfishpg_money`](https://ext.pigsty.io/#/babelfishpg_money) [`pgmemcache`](https://ext.pigsty.io/#/pgmemcache)
[**ETL**](https://ext.pigsty.io/#/etl): [`pglogical`](https://ext.pigsty.io/#/pglogical) [`pglogical_origin`](https://ext.pigsty.io/#/pglogical_origin) [`pglogical_ticker`](https://ext.pigsty.io/#/pglogical_ticker) [`pgl_ddl_deploy`](https://ext.pigsty.io/#/pgl_ddl_deploy) [`pg_failover_slots`](https://ext.pigsty.io/#/pg_failover_slots) [`wal2json`](https://ext.pigsty.io/#/wal2json) [`wal2mongo`](https://ext.pigsty.io/#/wal2mongo) [`decoderbufs`](https://ext.pigsty.io/#/decoderbufs) [`decoder_raw`](https://ext.pigsty.io/#/decoder_raw) [`test_decoding`](https://ext.pigsty.io/#/test_decoding) [`mimeo`](https://ext.pigsty.io/#/mimeo) [`repmgr`](https://ext.pigsty.io/#/repmgr) [`pg_fact_loader`](https://ext.pigsty.io/#/pg_fact_loader) [`pg_bulkload`](https://ext.pigsty.io/#/pg_bulkload)

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
