---
title: Self-Hosting Supabase on PostgreSQL
linkTitle: "Self-Hosting Supabase"
date: 2024-11-25
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: Supabase is great, own your own Supabase is even better. A tutorial for self-hosting production-grade supabase on local/cloud/ VM/BMs.
tags: [Database,Supabase]
---

Supabase is great, own your own Supabase is even better. 
Here's a comprehensive tutorial for self-hosting production-grade supabase on local/cloud/ VM/BMs.


## What is Supabase?

[Supabase](https://supabase.com/) is an open-source Firebase alternative, a Backend as a Service (BaaS).

Supabase wraps PostgreSQL kernel and vector extensions, alone with authentication, realtime subscriptions, edge functions, object storage, and instant REST and GraphQL APIs from your postgres schema.
It let you skip most backend work, requiring only database design and frontend skills to ship quickly.

Currently, Supabase may be the [most popular](https://ossrank.com/cat/368-postgresql-extension-ecosystem) open-source project in the PostgreSQL ecosystem, boasting over 74,000 stars on GitHub.
And become quite popular among developers, and startups, since they have a [generous free plan](https://supabase.com/pricing), just like cloudflare & neon.



------

## Why Self-Hosting?

Supabase's slogan is: "**Build in a weekend, Scale to millions**". It has great cost-effectiveness in small scales (4c8g) indeed.
But there is no doubt that when you really grow to millions of users, some may choose to self-hosting their own Supabase —— for functionality, performance, cost, and other reasons.

That's where Pigsty comes in. Pigsty provides a complete one-click self-hosting solution for Supabase.
Self-hosted Supabase can enjoy full PostgreSQL monitoring, IaC, PITR, and high availability capability.

You can run the latest PostgreSQL 17(,16,15,14) kernels, (supabase is using the 15 currently), alone with [390](https://ext.pigsty.io/#/list) PostgreSQL extensions out-of-the-box.
Run on [mainstream](https://pigsty.io/docs/reference/compatibility) Linus OS distros with production grade [HA](/docs/concept/ha) [PostgreSQL](/docs/pgsql), [MinIO](/docs/minio), Prometheus & Grafana Stack for observability, and Nginx for reverse proxy.

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

Since most of the supabase maintained extensions are not available in the official PGDG repo, 
we have compiled all the RPM/DEBs for these extensions and put them in the [Pigsty repo](https://ext.pigsty.io):
[pg_graphql](https://ext.pigsty.io/#/pg_graphql), [pg_jsonschema](https://ext.pigsty.io/#/pg_jsonschema), [wrappers](https://ext.pigsty.io/#/wrappers), [index_advisor](https://ext.pigsty.io/#/index_advisor), [pg_net](https://ext.pigsty.io/#/pg_net), [vault](https://ext.pigsty.io/#/vault), [pgjwt](https://ext.pigsty.io/#/pgjwt), [supautils](https://ext.pigsty.io/#/supautils), [pg_plan_filter](https://ext.pigsty.io/#/plan_filter),  

Everything is under your control, you have the ability and freedom to scale PGSQL, MinIO, and Supabase itself.
And take full advantage of the performance and cost advantages of modern hardware like Gen5 NVMe SSD.

All you need is prepare a VM with several commands and wait for 10 minutes....


------

## Get Started

First, download & [install](https://pigsty.io/docs/setup/install) pigsty as usual, with the `supa` config template:

```bash
 curl -fsSL https://repo.pigsty.io/get | bash
./bootstrap          # install deps (ansible)
./configure -c supa  # use supa config template (IMPORTANT: CHANGE PASSWORDS!)
./install.yml        # install pigsty, create ha postgres & minio clusters 
```

> Please change the `pigsty.yml` config file according to your need before deploying Supabase. (**Credentials**)
> For dev/test/demo purposes, we will just skip that, and comes back later.

Then, run the [`supabase.yml`](https://github.com/Vonng/pigsty/blob/main/supabase.yml) to launch stateless part of supabase.

```bash
./supabase.yml       # launch stateless supabase containers with docker compose
```

You can access the supabase API / Web UI through the `8000/8443` directly.

with configured DNS, or a local `/etc/hosts` entry, you can also use the default `supa.pigsty` domain name via the 80/443 infra portal.

> Credentials for Supabase Studio: `supabase` : `pigsty`

[![asciicast](https://asciinema.org/a/692194.svg)](https://asciinema.org/a/692194)



-------

## Architecture

Pigsty's supabase is based on the [Supabase Docker Compose Template](https://supabase.com/docs/guides/self-hosting/docker), 
with some slight modifications to fit-in Pigsty's default [ACL](/docs/pgsql/acl) model.

The stateful part of this template is replaced by Pigsty's managed PostgreSQL cluster and MinIO cluster.
The container part are stateless, so you can launch / destroy / run multiple supabase containers on the same stateful PGSQL / MINIO cluster simultaneously to scale out.

![](https://pigsty.io/img/supa-arch.svg)

The built-in [`supa.yml`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml) [config](/docs/config/supa) template will create a single-node supabase, with a [singleton PostgreSQL](/docs/pgsql) and SNSD [MinIO](/docs/minio) server.
You can use [Multinode PostgreSQL Clusters](/docs/pgsql/config#replica) and [MNMD MinIO Clusters](/docs/minio/config#multi-node-multi-drive) / external S3 service instead in production, we will cover that later.



-------

## Config Detail

Here are checklists for self-hosting

- [x] [**Hardware**](/docs/setup/prepare#node): necessary VM/BM resources, one node at least, 3-4 are recommended for HA.
- [x] [**Linux OS**](/docs/setup/prepare#operating-system): Linux x86_64 server with fresh installed Linux, [check compatible distro](https://pigsty.io/docs/reference/compatibility)
- [x] [**Network**](/docs/setup/prepare#network): Static IPv4 address which can be used as node identity
- [x] [**Admin User**](/docs/setup/prepare#admin-user): nopass ssh & sudo are recommended for admin user
- [x] [**Conf Template**](/docs/setup/config): Use the [`supa`](/docs/conf/supa) config template, if you don't know how to manually configure pigsty

The built-in [`supa.yml`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml) config template is shown below.

<br>

<details><summary>The supa Config Template</summary>

```yaml
all:
  children:

    # infra cluster for proxy, monitor, alert, etc..
    infra: { hosts: { 10.10.10.10: { infra_seq: 1 } } }

    # etcd cluster for ha postgres
    etcd: { hosts: { 10.10.10.10: { etcd_seq: 1 } }, vars: { etcd_cluster: etcd } }

    # minio cluster, s3 compatible object storage
    minio: { hosts: { 10.10.10.10: { minio_seq: 1 } }, vars: { minio_cluster: minio } }

    # pg-meta, the underlying postgres database for supabase
    pg-meta:
      hosts: { 10.10.10.10: { pg_seq: 1, pg_role: primary } }
      vars:
        pg_cluster: pg-meta
        pg_users:
          # supabase roles: anon, authenticated, dashboard_user
          - { name: anon           ,login: false }
          - { name: authenticated  ,login: false }
          - { name: dashboard_user ,login: false ,replication: true ,createdb: true ,createrole: true }
          - { name: service_role   ,login: false ,bypassrls: true }
          # supabase users: please use the same password
          - { name: supabase_admin             ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: true   ,roles: [ dbrole_admin ] ,superuser: true ,replication: true ,createdb: true ,createrole: true ,bypassrls: true }
          - { name: authenticator              ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] }
          - { name: supabase_auth_admin        ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_storage_admin     ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] ,createrole: true }
          - { name: supabase_functions_admin   ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_replication_admin ,password: 'DBUser.Supa' ,replication: true ,roles: [ dbrole_admin ]}
          - { name: supabase_read_only_user    ,password: 'DBUser.Supa' ,bypassrls: true ,roles: [ dbrole_readonly, pg_read_all_data ] }
        pg_databases:
          - name: postgres
            baseline: supabase.sql
            owner: supabase_admin
            comment: supabase postgres database
            schemas: [ extensions ,auth ,realtime ,storage ,graphql_public ,supabase_functions ,_analytics ,_realtime ]
            extensions:
              - { name: pgcrypto  ,schema: extensions  } # 1.3   : cryptographic functions
              - { name: pg_net    ,schema: extensions  } # 0.9.2 : async HTTP
              - { name: pgjwt     ,schema: extensions  } # 0.2.0 : json web token API for postgres
              - { name: uuid-ossp ,schema: extensions  } # 1.1   : generate universally unique identifiers (UUIDs)
              - { name: pgsodium        }                # 3.1.9 : pgsodium is a modern cryptography library for Postgres.
              - { name: supabase_vault  }                # 0.2.8 : Supabase Vault Extension
              - { name: pg_graphql      }                # 1.5.9 : pg_graphql: GraphQL support
              - { name: pg_jsonschema   }                # 0.3.3 : pg_jsonschema: Validate json schema
              - { name: wrappers        }                # 0.4.3 : wrappers: FDW collections
              - { name: http            }                # 1.6   : http: allows web page retrieval inside the database.
              - { name: pg_cron         }                # 1.6   : pg_cron: Job scheduler for PostgreSQL
              - { name: timescaledb     }                # 2.17  : timescaledb: Enables scalable inserts and complex queries for time-series data
              - { name: pg_tle          }                # 1.2   : pg_tle: Trusted Language Extensions for PostgreSQL
              - { name: vector          }                # 0.8.0 : pgvector: the vector similarity search
        # supabase required extensions
        pg_libs: 'pg_stat_statements, plpgsql, plpgsql_check, pg_cron, pg_net, timescaledb, auto_explain, pg_tle, plan_filter'
        pg_extensions: # extensions to be installed on this cluster
          - supabase   # essential extensions for supabase
          - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
          - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
          - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
        pg_parameters:
          cron.database_name: postgres
          pgsodium.enable_event_trigger: off
        pg_hba_rules: # supabase hba rules, require access from docker network
          - { user: all ,db: postgres  ,addr: intra         ,auth: pwd ,title: 'allow supabase access from intranet'    }
          - { user: all ,db: postgres  ,addr: 172.17.0.0/16 ,auth: pwd ,title: 'allow access from local docker network' }
        node_crontab: [ '00 01 * * * postgres /pg/bin/pg-backup full' ] # make a full backup every 1am

    # launch supabase stateless part with docker compose: ./supabase.yml
    supabase:
      hosts:
        10.10.10.10: { supa_seq: 1 }  # instance id
      vars:
        supa_cluster: supa            # cluster name
        docker_enabled: true          # enable docker

        # use these to pull docker images via proxy and mirror registries
        #docker_registry_mirrors: ['https://docker.xxxxx.io']
        #proxy_env:   # add [OPTIONAL] proxy env to /etc/docker/daemon.json configuration file
        #  no_proxy: "localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,*.pigsty,*.aliyun.com,mirrors.*,*.myqcloud.com,*.tsinghua.edu.cn"
        #  #all_proxy: http://user:pass@host:port

        # these configuration entries will OVERWRITE or APPEND to /opt/supabase/.env file (src template: app/supabase/.env)
        # check https://github.com/Vonng/pigsty/blob/main/app/supabase/.env for default values
        supa_config:

          # IMPORTANT: CHANGE JWT_SECRET AND REGENERATE CREDENTIAL ACCORDING!!!!!!!!!!!
          # https://supabase.com/docs/guides/self-hosting/docker#securing-your-services
          jwt_secret: your-super-secret-jwt-token-with-at-least-32-characters-long
          anon_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
          service_role_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
          dashboard_username: supabase
          dashboard_password: pigsty

          # postgres connection string (use the correct ip and port)
          postgres_host: 10.10.10.10
          postgres_port: 5436             # access via the 'default' service, which always route to the primary postgres
          postgres_db: postgres
          postgres_password: DBUser.Supa  # password for supabase_admin and multiple supabase users

          # expose supabase via domain name
          site_url: http://supa.pigsty
          api_external_url: http://supa.pigsty
          supabase_public_url: http://supa.pigsty

          # if using s3/minio as file storage
          s3_bucket: supa
          s3_endpoint: https://sss.pigsty:9000
          s3_access_key: supabase
          s3_secret_key: S3User.Supabase
          s3_force_path_style: true
          s3_protocol: https
          s3_region: stub
          minio_domain_ip: 10.10.10.10  # sss.pigsty domain name will resolve to this ip statically

          # if using SMTP (optional)
          #smtp_admin_email: admin@example.com
          #smtp_host: supabase-mail
          #smtp_port: 2500
          #smtp_user: fake_mail_user
          #smtp_pass: fake_mail_password
          #smtp_sender_name: fake_sender
          #enable_anonymous_users: false


  vars:
    version: v3.1.0                   # pigsty version string
    admin_ip: 10.10.10.10             # admin node ip address
    region: default                   # upstream mirror region: default|china|europe
    node_tune: oltp                   # node tuning specs: oltp,olap,tiny,crit
    pg_conf: oltp.yml                 # pgsql tuning specs: {oltp,olap,tiny,crit}.yml
    infra_portal:                     # domain names and upstream servers
      home         : { domain: h.pigsty }
      grafana      : { domain: g.pigsty ,endpoint: "${admin_ip}:3000" , websocket: true }
      prometheus   : { domain: p.pigsty ,endpoint: "${admin_ip}:9090" }
      alertmanager : { domain: a.pigsty ,endpoint: "${admin_ip}:9093" }
      minio        : { domain: m.pigsty ,endpoint: "10.10.10.10:9001", https: true, websocket: true }
      blackbox     : { endpoint: "${admin_ip}:9115" }
      loki         : { endpoint: "${admin_ip}:3100" }  # expose supa studio UI and API via nginx
      supa         : { domain: supa.pigsty ,endpoint: "10.10.10.10:8000", websocket: true }

    #----------------------------------#
    # Credential: CHANGE THESE PASSWORDS
    #----------------------------------#
    #grafana_admin_username: admin
    grafana_admin_password: pigsty
    #pg_admin_username: dbuser_dba
    pg_admin_password: DBUser.DBA
    #pg_monitor_username: dbuser_monitor
    pg_monitor_password: DBUser.Monitor
    #pg_replication_username: replicator
    pg_replication_password: DBUser.Replicator
    #patroni_username: postgres
    patroni_password: Patroni.API
    #haproxy_admin_username: admin
    haproxy_admin_password: pigsty

    # use minio as supabase file storage, single node single driver mode for demonstration purpose
    minio_access_key: minioadmin      # root access key, `minioadmin` by default
    minio_secret_key: minioadmin      # root secret key, `minioadmin` by default
    minio_buckets: [ { name: pgsql }, { name: supa } ]
    minio_users:
      - { access_key: dba , secret_key: S3User.DBA, policy: consoleAdmin }
      - { access_key: pgbackrest , secret_key: S3User.Backup,   policy: readwrite }
      - { access_key: supabase   , secret_key: S3User.Supabase, policy: readwrite }
    minio_endpoint: https://sss.pigsty:9000    # explicit overwrite minio endpoint with haproxy port
    node_etc_hosts: ["10.10.10.10 sss.pigsty"] # domain name to access minio from all nodes (required)

    # use minio as default backup repo for PostgreSQL
    pgbackrest_method: minio          # pgbackrest repo method: local,minio,[user-defined...]
    pgbackrest_repo:                  # pgbackrest repo: https://pgbackrest.org/configuration.html#section-repository
      local:                          # default pgbackrest repo with local posix fs
        path: /pg/backup              # local backup directory, `/pg/backup` by default
        retention_full_type: count    # retention full backups by count
        retention_full: 2             # keep 2, at most 3 full backup when using local fs repo
      minio:                          # optional minio repo for pgbackrest
        type: s3                      # minio is s3-compatible, so s3 is used
        s3_endpoint: sss.pigsty       # minio endpoint domain name, `sss.pigsty` by default
        s3_region: us-east-1          # minio region, us-east-1 by default, useless for minio
        s3_bucket: pgsql              # minio bucket name, `pgsql` by default
        s3_key: pgbackrest            # minio user access key for pgbackrest
        s3_key_secret: S3User.Backup  # minio user secret key for pgbackrest
        s3_uri_style: path            # use path style uri for minio rather than host style
        path: /pgbackrest             # minio backup path, default is `/pgbackrest`
        storage_port: 9000            # minio port, 9000 by default
        storage_ca_file: /pg/cert/ca.crt  # minio ca file path, `/pg/cert/ca.crt` by default
        bundle: y                     # bundle small files into a single file
        cipher_type: aes-256-cbc      # enable AES encryption for remote backup repo
        cipher_pass: pgBackRest       # AES encryption password, default is 'pgBackRest'
        retention_full_type: time     # retention full backup by time on minio repo
        retention_full: 14            # keep full backup for last 14 days

    # download docker and supabase related extensions
    pg_version: 17
    repo_modules: node,pgsql,infra,docker
    repo_packages: [node-bootstrap, infra-package, infra-addons, node-package1, node-package2, pgsql-utility, docker ]
    repo_extra_packages:
      - pgsql-main
      - supabase   # essential extensions for supabase
      - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
      - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
      - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit

```

</details>

<br>

For advanced topics, we may need to modify the configuration file to fit our needs.

- [Security Enhancement](#security-enhancement)
- [Domain Name and HTTPS](#domain-name-and-https)
- [Sending Mail with SMTP](#sending-mail-with-smtp)
- [MinIO or External S3](#minio-or-external-s3)
- [True High Availability](#true-high-availability)



--------

## Security Enhancement

For security reasons, you should change the default passwords in the `pigsty.yml` config file.

- [`grafana_admin_password`](/docs/reference/param#grafana_admin_password): `pigsty`, Grafana admin password
- [`pg_admin_password`](/docs/reference/param#pg_admin_password): `DBUser.DBA`, PGSQL superuser password
- [`pg_monitor_password`](/docs/reference/param#pg_monitor_password): `DBUser.Monitor`, PGSQL monitor user password
- [`pg_replication_password`](/docs/reference/param#pg_replication_password): `DBUser.Replicator`, PGSQL replication user password
- [`patroni_password`](/docs/reference/param#patroni_password): `Patroni.API`, Patroni HA Agent Password
- [`haproxy_admin_password`](/docs/reference/param#haproxy_admin_password): `pigsty`, Load balancer admin password
- [`minio_access_key`](/docs/minio/param#grafana_admin_password): `minioadmin`, MinIO root username
- [`minio_secret_key`](/docs/minio/param#minio_secret_key): `minioadmin`, MinIO root password

Supabase will use PostgreSQL & MinIO as its backend, so also change the following passwords for supabase business users: 

- [`pg_users`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L49): password for supabase business users in postgres
- [`minio_users`](/docs/minio/param#minio_secret_key): `minioadmin`, MinIO business user's password

The pgbackrest will take backups and WALs to MinIO, so also change the following passwords reference

- [`pgbackrest_repo`](/docs/minio/param#pgbackrest_repo): refer to the 

PLEASE check the [Supabase Self-Hosting: Generate API Keys](https://supabase.com/docs/guides/self-hosting/docker#generate-api-keys) to generate supabase credentials:

- [`jwt_secret`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L114): a secret key with at least 40 characters
- [`anon_key`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L115): a jwt token generate for anonymous users, based on `jwt_secret`
- [`service_role_key`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L116): a jwt token generate for elevated service roles, based on `jwt_secret`
- [`dashboard_username`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L117): supabase studio web portal username, `supabase` by default
- [`dashboard_password`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L128): supabase studio web portal password, `pigsty` by default

If you have chanaged the default password for PostgreSQL and MinIO, you have to update the following parameters as well:

- [`postgres_password`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L126), according to [`pg_users`](/docs/pgsql/user)
- [`s3_access_key`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#136) and [`s3_secret_key`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#137), according to [`minio_users`](/docs/minio/param#minio_users)



--------

## Domain Name and HTTPS

For local or intranet use, you can connect directly to Kong port on `http://<IP>:8000` or `8443` for https.
This works but isn’t ideal. Using a domain with HTTPS is strongly recommended when serving Supabase to the public.

Pigsty has a Nginx server installed & configured on the admin node to act as a reverse proxy for all web based service. which is configured via the `infra_portal` parameter.

```yaml
all:
  vars:     # global vars
    #.....
    infra_portal:  # domain names and upstream servers
      home         : { domain: h.pigsty }
      grafana      : { domain: g.pigsty ,endpoint: "${admin_ip}:3000" , websocket: true }
      prometheus   : { domain: p.pigsty ,endpoint: "${admin_ip}:9090" }
      alertmanager : { domain: a.pigsty ,endpoint: "${admin_ip}:9093" }
      minio        : { domain: m.pigsty ,endpoint: "10.10.10.10:9001", https: true, websocket: true }
      blackbox     : { endpoint: "${admin_ip}:9115" }
      loki         : { endpoint: "${admin_ip}:3100" }  # expose supa studio UI and API via nginx
      supa         : { domain: supa.pigsty ,endpoint: "10.10.10.10:8000", websocket: true }
```

On the client side, you can use the domain `supa.pigsty` to access the Supabase Studio management interface.
You can add this domain to your local `/etc/hosts` file or use a local DNS server to resolve it to the server's **external** IP address.


To use a real domain with HTTPS, you will need to modify the `all.vars.infra_portal.supa` with updated domain name (such as `supa.pigsty.cc` here).
You can obtain a free HTTPS certificate from [Let’s Encrypt](https://letsencrypt.org/), and just put the cert/key files in the specified path.

```yaml
#supa : { domain: supa.pigsty ,endpoint: "10.10.10.10:8000", websocket: true }  # add your HTTPS certs/keys and specify the path
supa  : { domain: supa.pigsty.cc ,endpoint: "10.10.10.10:8000", websocket: true ,cert: /etc/cert/suap.pigsty.cc.crt ,key: /etc/cert/supa.pigsty.cc.key }
```

To reload the new configuration after installation, use the `infra.yml` playbook:

```bash
./infra.yml -t nginx_config,nginx_launch   # reload nginx config
```

You also have to update the `all.children.supabase.vars.supa_config` to tell supabase to use the new domain name:

```yaml
all:
  children:           # clusters
    supabase:         # supabase group
      vars:           # supabase param
        supa_config:  # supabase config
          
          # update supabase domain names here
          site_url: http://supa.pigsty.cc
          api_external_url: http://supa.pigsty.cc
          supabase_public_url: http://supa.pigsty.cc
```

And reload the supabase service to apply the new configuration:

```bash
./supabase.yml -t supa_config,supa_launch # reload supabase config
```




--------

## Sending Mail with SMTP

Some Supabase features require email. For production use, I'd recommend using an external SMTP service. 
Since self-hosted SMTP servers often result in rejected or spam-flagged emails.

To do this, modify the Supabase configuration and add SMTP credentials:

```yaml
all:
  children:
    supabase:
      vars:
        supa_config:
          smtp_host: smtpdm.aliyun.com:80
          smtp_port: 80
          smtp_user: no_reply@mail.your.domain.com
          smtp_pass: your_email_user_password
          smtp_sender_name: MySupabase
          smtp_admin_email: adminxxx@mail.your.domain.com
          enable_anonymous_users: false
```

And don't forget to reload the supabase service with `./supabase.yml -t supa_config,supa_launch`





--------

## MinIO or External S3

Pigsty's self-hosting supabase will use a local [SNSD MinIO](/docs/minio/config#single-node-single-drive) server,
which is used by Supabase itself for object storage, and by PostgreSQL for backups.
For production use, you should consider using a HA [MNMD MinIO](/docs/minio/config#multi-node-multi-drive) cluster or an external S3 compatible service instead.

We recommend using an external S3 when:

- you just have one single server available, then external s3 gives you a minimal disaster recovery guarantee, with RTO in hours and RPO in MBs.
- you are operating in the cloud, then using S3 directly is recommended rather than wrap expensively EBS with MinIO 

> The [`terraform/spec/aliyun-meta-s3.tf`](https://github.com/Vonng/pigsty/blob/main/terraform/spec/aliyun-meta-s3.tf) provides an example of how to provision a single node alone with an S3 bucket.

To use an external S3 compatible service, you'll have to update two related references in the `pigsty.yml` config.

For example, to use Aliyun OSS as the object storage for Supabase, you can modify the `all.children.supabase.vars.supa_config` to point to the Aliyun OSS bucket:

```yaml
all:
  children:
    supabase:
      vars:
        supa_config:
          s3_bucket: pigsty-oss
          s3_endpoint: https://oss-cn-beijing-internal.aliyuncs.com
          s3_access_key: xxxxxxxxxxxxxxxx
          s3_secret_key: xxxxxxxxxxxxxxxx
          s3_force_path_style: false
          s3_protocol: https
          s3_region: oss-cn-beijing
```

Reload the supabase service with `./supabase.yml -t supa_config,supa_launch` again.

The next reference is in the PostgreSQL backup repo:

```yaml
all:
  vars:
    # use minio as default backup repo for PostgreSQL
    pgbackrest_method: minio          # pgbackrest repo method: local,minio,[user-defined...]
    pgbackrest_repo:                  # pgbackrest repo: https://pgbackrest.org/configuration.html#section-repository
      local:                          # default pgbackrest repo with local posix fs
        path: /pg/backup              # local backup directory, `/pg/backup` by default
        retention_full_type: count    # retention full backups by count
        retention_full: 2             # keep 2, at most 3 full backup when using local fs repo
      minio:                          # optional minio repo for pgbackrest
        type: s3                      # minio is s3-compatible, so s3 is used
        
        # update your credentials here
        s3_endpoint: oss-cn-beijing-internal.aliyuncs.com
        s3_region: oss-cn-beijing
        s3_bucket: pigsty-oss
        s3_key: xxxxxxxxxxxxxx
        s3_key_secret: xxxxxxxx
        s3_uri_style: host

        path: /pgbackrest             # minio backup path, default is `/pgbackrest`
        storage_port: 9000            # minio port, 9000 by default
        storage_ca_file: /pg/cert/ca.crt  # minio ca file path, `/pg/cert/ca.crt` by default
        bundle: y                     # bundle small files into a single file
        cipher_type: aes-256-cbc      # enable AES encryption for remote backup repo
        cipher_pass: pgBackRest       # AES encryption password, default is 'pgBackRest'
        retention_full_type: time     # retention full backup by time on minio repo
        retention_full: 14            # keep full backup for last 14 days
```

After updating the `pgbackrest_repo`, you can reset the pgBackrest backup with `./pgsql.yml -t pgbackrest`.


--------

## True High Availability

The default single-node deployment (with external S3) provide a minimal disaster recovery guarantee, with RTO in hours and RPO in MBs.

To achieve RTO < 30s and zero data loss, you need a multi-node high availability cluster with at least 3-nodes.

Which involves high availability for these components:

- [ETCD](/docs/etcd): DCS requires at least three nodes to tolerate one node failure.
- [PGSQL](/docs/pgsql): PGSQL synchronous commit mode recommends at least three nodes.
- [INFRA](/docs/infra): It's good to have two or three copies of observability stack.
- Supabase itself can also have multiple replicas to achieve high availability.

We recommend you to refer to the [trio](/docs/conf/trio) and [safe](/docs/conf/safe) config to upgrade your cluster to three nodes or more.

In this case, you also need to modify the access points for PostgreSQL and MinIO to use the DNS / L2 VIP / HAProxy [HA access points](/docs/concept/svc).


```yaml
all:
  children:
    supabase:
      hosts:
        10.10.10.10: { supa_seq: 1 }
        10.10.10.11: { supa_seq: 2 }
        10.10.10.12: { supa_seq: 3 } 
      vars:
        supa_cluster: supa            # cluster name
        supa_config:
          postgres_host: 10.10.10.2             # use the PG L2 VIP
          postgres_port: 5433                   # use the 5433 port to access the primary instance through pgbouncer
          s3_endpoint: https://sss.pigsty:9002  # If you are using MinIO through the haproxy lb port 9002
          minio_domain_ip: 10.10.10.3           # use the L2 VIP binds to all proxy nodes
```


<details><summary>The 3-Node HA Supabase Config Template</summary>

```yaml
all:

  #==============================================================#
  # Clusters, Nodes, and Modules
  #==============================================================#
  children:

    # infra cluster for proxy, monitor, alert, etc..
    infra:
      hosts:
        10.10.10.10: { infra_seq: 1 ,nodename: infra-1 }
        10.10.10.11: { infra_seq: 2 ,nodename: infra-2, repo_enabled: false, grafana_enabled: false }
        10.10.10.12: { infra_seq: 3 ,nodename: infra-3, repo_enabled: false, grafana_enabled: false }
      vars:

        vip_enabled: true
        vip_vrid: 128
        vip_address: 10.10.10.3
        vip_interface: eth1
        haproxy_services:
          - name: minio                    # [REQUIRED] service name, unique
            port: 9002                     # [REQUIRED] service port, unique
            balance: leastconn             # [OPTIONAL] load balancer algorithm
            options:                       # [OPTIONAL] minio health check
              - option httpchk
              - option http-keep-alive
              - http-check send meth OPTIONS uri /minio/health/live
              - http-check expect status 200
            servers:
              - { name: minio-1 ,ip: 10.10.10.10 ,port: 9000 ,options: 'check-ssl ca-file /etc/pki/ca.crt check port 9000' }
              - { name: minio-2 ,ip: 10.10.10.11 ,port: 9000 ,options: 'check-ssl ca-file /etc/pki/ca.crt check port 9000' }
              - { name: minio-3 ,ip: 10.10.10.12 ,port: 9000 ,options: 'check-ssl ca-file /etc/pki/ca.crt check port 9000' }



    etcd: # dcs service for postgres/patroni ha consensus
      hosts: # 1 node for testing, 3 or 5 for production
        10.10.10.10: { etcd_seq: 1 }  # etcd_seq required
        10.10.10.11: { etcd_seq: 2 }  # assign from 1 ~ n
        10.10.10.12: { etcd_seq: 3 }  # odd number please
      vars: # cluster level parameter override roles/etcd
        etcd_cluster: etcd  # mark etcd cluster name etcd
        etcd_safeguard: false # safeguard against purging
        etcd_clean: true # purge etcd during init process

    # minio cluster 4-node
    minio:
      hosts:
        10.10.10.10: { minio_seq: 1 , nodename: minio-1 }
        10.10.10.11: { minio_seq: 2 , nodename: minio-2 }
        10.10.10.12: { minio_seq: 3 , nodename: minio-3 }
      vars:
        minio_cluster: minio
        minio_data: '/data{1...4}'
        minio_buckets: [ { name: pgsql }, { name: supa } ]
        minio_users:
          - { access_key: dba , secret_key: S3User.DBA, policy: consoleAdmin }
          - { access_key: pgbackrest , secret_key: S3User.Backup,   policy: readwrite }
          - { access_key: supabase   , secret_key: S3User.Supabase, policy: readwrite }

    # pg-meta, the underlying postgres database for supabase
    pg-meta:
      hosts:
        10.10.10.10: { pg_seq: 1, pg_role: primary }
        10.10.10.11: { pg_seq: 2, pg_role: replica }
        10.10.10.12: { pg_seq: 3, pg_role: replica }
      vars:
        pg_cluster: pg-meta
        pg_users:
          # supabase roles: anon, authenticated, dashboard_user
          - { name: anon           ,login: false }
          - { name: authenticated  ,login: false }
          - { name: dashboard_user ,login: false ,replication: true ,createdb: true ,createrole: true }
          - { name: service_role   ,login: false ,bypassrls: true }
          # supabase users: please use the same password
          - { name: supabase_admin             ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: true   ,roles: [ dbrole_admin ] ,superuser: true ,replication: true ,createdb: true ,createrole: true ,bypassrls: true }
          - { name: authenticator              ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] }
          - { name: supabase_auth_admin        ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_storage_admin     ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] ,createrole: true }
          - { name: supabase_functions_admin   ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_replication_admin ,password: 'DBUser.Supa' ,replication: true ,roles: [ dbrole_admin ]}
          - { name: supabase_read_only_user    ,password: 'DBUser.Supa' ,bypassrls: true ,roles: [ dbrole_readonly, pg_read_all_data ] }
        pg_databases:
          - name: postgres
            baseline: supabase.sql
            owner: supabase_admin
            comment: supabase postgres database
            schemas: [ extensions ,auth ,realtime ,storage ,graphql_public ,supabase_functions ,_analytics ,_realtime ]
            extensions:
              - { name: pgcrypto  ,schema: extensions  } # 1.3   : cryptographic functions
              - { name: pg_net    ,schema: extensions  } # 0.9.2 : async HTTP
              - { name: pgjwt     ,schema: extensions  } # 0.2.0 : json web token API for postgres
              - { name: uuid-ossp ,schema: extensions  } # 1.1   : generate universally unique identifiers (UUIDs)
              - { name: pgsodium        }                # 3.1.9 : pgsodium is a modern cryptography library for Postgres.
              - { name: supabase_vault  }                # 0.2.8 : Supabase Vault Extension
              - { name: pg_graphql      }                # 1.5.9 : pg_graphql: GraphQL support
              - { name: pg_jsonschema   }                # 0.3.3 : pg_jsonschema: Validate json schema
              - { name: wrappers        }                # 0.4.3 : wrappers: FDW collections
              - { name: http            }                # 1.6   : http: allows web page retrieval inside the database.
              - { name: pg_cron         }                # 1.6   : pg_cron: Job scheduler for PostgreSQL
              - { name: timescaledb     }                # 2.17  : timescaledb: Enables scalable inserts and complex queries for time-series data
              - { name: pg_tle          }                # 1.2   : pg_tle: Trusted Language Extensions for PostgreSQL
              - { name: vector          }                # 0.8.0 : pgvector: the vector similarity search
        # supabase required extensions
        pg_libs: 'pg_stat_statements, plpgsql, plpgsql_check, pg_cron, pg_net, timescaledb, auto_explain, pg_tle, plan_filter'
        pg_extensions: # extensions to be installed on this cluster
          - supabase   # essential extensions for supabase
          - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
          - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
          - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
        pg_parameters:
          cron.database_name: postgres
          pgsodium.enable_event_trigger: off
        pg_hba_rules: # supabase hba rules, require access from docker network
          - { user: all ,db: postgres  ,addr: intra         ,auth: pwd ,title: 'allow supabase access from intranet'    }
          - { user: all ,db: postgres  ,addr: 172.17.0.0/16 ,auth: pwd ,title: 'allow access from local docker network' }
        pg_vip_enabled: true
        pg_vip_address: 10.10.10.2/24
        pg_vip_interface: eth1
        node_crontab: [ '00 01 * * * postgres /pg/bin/pg-backup full' ] # make a full backup every 1am


    # launch supabase stateless part with docker compose: ./supabase.yml
    supabase:
      hosts:
        10.10.10.10: { supa_seq: 1 }  # instance 1
        10.10.10.11: { supa_seq: 2 }  # instance 2
        10.10.10.12: { supa_seq: 3 }  # instance 3
      vars:
        supa_cluster: supa            # cluster name
        docker_enabled: true          # enable docker

        # use these to pull docker images via proxy and mirror registries
        #docker_registry_mirrors: ['https://docker.xxxxx.io']
        #proxy_env:   # add [OPTIONAL] proxy env to /etc/docker/daemon.json configuration file
        #  no_proxy: "localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,*.pigsty,*.aliyun.com,mirrors.*,*.myqcloud.com,*.tsinghua.edu.cn"
        #  #all_proxy: http://user:pass@host:port

        # these configuration entries will OVERWRITE or APPEND to /opt/supabase/.env file (src template: app/supabase/.env)
        # check https://github.com/Vonng/pigsty/blob/main/app/supabase/.env for default values
        supa_config:

          # IMPORTANT: CHANGE JWT_SECRET AND REGENERATE CREDENTIAL ACCORDING!!!!!!!!!!!
          # https://supabase.com/docs/guides/self-hosting/docker#securing-your-services
          jwt_secret: your-super-secret-jwt-token-with-at-least-32-characters-long
          anon_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
          service_role_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
          dashboard_username: supabase
          dashboard_password: pigsty

          # postgres connection string (use the correct ip and port)
          postgres_host: 10.10.10.3       # use the pg_vip_address rather than single node ip
          postgres_port: 5433             # access via the 'default' service, which always route to the primary postgres
          postgres_db: postgres
          postgres_password: DBUser.Supa  # password for supabase_admin and multiple supabase users

          # expose supabase via domain name
          site_url: http://supa.pigsty
          api_external_url: http://supa.pigsty
          supabase_public_url: http://supa.pigsty

          # if using s3/minio as file storage
          s3_bucket: supa
          s3_endpoint: https://sss.pigsty:9002
          s3_access_key: supabase
          s3_secret_key: S3User.Supabase
          s3_force_path_style: true
          s3_protocol: https
          s3_region: stub
          minio_domain_ip: 10.10.10.3   # sss.pigsty domain name will resolve to this l2 vip that bind to all nodes

          # if using SMTP (optional)
          #smtp_admin_email: admin@example.com
          #smtp_host: supabase-mail
          #smtp_port: 2500
          #smtp_user: fake_mail_user
          #smtp_pass: fake_mail_password
          #smtp_sender_name: fake_sender
          #enable_anonymous_users: false



  #==============================================================#
  # Global Parameters
  #==============================================================#
  vars:
    version: v3.1.0                   # pigsty version string
    admin_ip: 10.10.10.10             # admin node ip address
    region: china                     # upstream mirror region: default|china|europe
    node_tune: oltp                   # node tuning specs: oltp,olap,tiny,crit
    pg_conf: oltp.yml                 # pgsql tuning specs: {oltp,olap,tiny,crit}.yml
    infra_portal:                     # domain names and upstream servers
      home         : { domain: h.pigsty }
      grafana      : { domain: g.pigsty ,endpoint: "${admin_ip}:3000" , websocket: true }
      prometheus   : { domain: p.pigsty ,endpoint: "${admin_ip}:9090" }
      alertmanager : { domain: a.pigsty ,endpoint: "${admin_ip}:9093" }
      minio        : { domain: m.pigsty ,endpoint: "10.10.10.10:9001", https: true, websocket: true }
      blackbox     : { endpoint: "${admin_ip}:9115" }
      loki         : { endpoint: "${admin_ip}:3100" }  # expose supa studio UI and API via nginx
      supa         : { domain: supa.pigsty ,endpoint: "10.10.10.10:8000", websocket: true }

    #----------------------------------#
    # Credential: CHANGE THESE PASSWORDS
    #----------------------------------#
    #grafana_admin_username: admin
    grafana_admin_password: pigsty
    #pg_admin_username: dbuser_dba
    pg_admin_password: DBUser.DBA
    #pg_monitor_username: dbuser_monitor
    pg_monitor_password: DBUser.Monitor
    #pg_replication_username: replicator
    pg_replication_password: DBUser.Replicator
    #patroni_username: postgres
    patroni_password: Patroni.API
    #haproxy_admin_username: admin
    haproxy_admin_password: pigsty

    # use minio as supabase file storage, single node single driver mode for demonstration purpose
    minio_access_key: minioadmin      # root access key, `minioadmin` by default
    minio_secret_key: minioadmin      # root secret key, `minioadmin` by default
    minio_buckets: [ { name: pgsql }, { name: supa } ]
    minio_users:
      - { access_key: dba , secret_key: S3User.DBA, policy: consoleAdmin }
      - { access_key: pgbackrest , secret_key: S3User.Backup,   policy: readwrite }
      - { access_key: supabase   , secret_key: S3User.Supabase, policy: readwrite }
    minio_endpoint: https://sss.pigsty:9000    # explicit overwrite minio endpoint with haproxy port
    node_etc_hosts: ["10.10.10.3 sss.pigsty"] # domain name to access minio from all nodes (required)

    # use minio as default backup repo for PostgreSQL
    pgbackrest_method: minio          # pgbackrest repo method: local,minio,[user-defined...]
    pgbackrest_repo:                  # pgbackrest repo: https://pgbackrest.org/configuration.html#section-repository
      local:                          # default pgbackrest repo with local posix fs
        path: /pg/backup              # local backup directory, `/pg/backup` by default
        retention_full_type: count    # retention full backups by count
        retention_full: 2             # keep 2, at most 3 full backup when using local fs repo
      minio:                          # optional minio repo for pgbackrest
        type: s3                      # minio is s3-compatible, so s3 is used
        s3_endpoint: sss.pigsty       # minio endpoint domain name, `sss.pigsty` by default
        s3_region: us-east-1          # minio region, us-east-1 by default, useless for minio
        s3_bucket: pgsql              # minio bucket name, `pgsql` by default
        s3_key: pgbackrest            # minio user access key for pgbackrest
        s3_key_secret: S3User.Backup  # minio user secret key for pgbackrest
        s3_uri_style: path            # use path style uri for minio rather than host style
        path: /pgbackrest             # minio backup path, default is `/pgbackrest`
        storage_port: 9002            # minio port, 9000 by default
        storage_ca_file: /pg/cert/ca.crt  # minio ca file path, `/pg/cert/ca.crt` by default
        bundle: y                     # bundle small files into a single file
        cipher_type: aes-256-cbc      # enable AES encryption for remote backup repo
        cipher_pass: pgBackRest       # AES encryption password, default is 'pgBackRest'
        retention_full_type: time     # retention full backup by time on minio repo
        retention_full: 14            # keep full backup for last 14 days

    # download docker and supabase related extensions
    pg_version: 17
    repo_modules: node,pgsql,infra,docker
    repo_packages: [node-bootstrap, infra-package, infra-addons, node-package1, node-package2, pgsql-utility, docker ]
    repo_extra_packages:
      - pgsql-main
      - supabase   # essential extensions for supabase
      - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
      - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
      - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
```

</details>


<br>

------------

<br>