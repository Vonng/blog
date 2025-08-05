---
title: PostgreSQL神功大成！最全扩展仓库来了！
linkTitle: "PostgreSQL神功大成！"
date: 2024-11-02
hero: /hero/pg-eat-db-world.jpg
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [微信原文](https://mp.weixin.qq.com/s/Dv3--O0K70Fevz39r3T4Ag)
summary: >
  PG扩展很多很强大，但如何安装并使用起来，一直都是社区的难题。现在有了Pigsty扩展仓库，390个强力插件开箱即用，有了这些扩展的加持，PG不能说在数据库里天下无敌，但也非常接近了。
tags: [PostgreSQL,PG生态,扩展]
---



最近没怎么更新，因为在憋大招。最近功成出关，遂发此文为贺 —— 我做了一个收录PG生态所有能打的390个扩展的[仓库](https://ext.pigsty.io)，让 PostgreSQL 在成为数据库全能王的道路上又往前迈出了坚实的一步！

自从我在 《[**PostgreSQL正在吞噬数据库世界**](/pg/pg-eat-db-world)》 一文中指出 **可扩展性** 对于 PostgreSQL 的重要性以来，PG 社区对此进行了[**热烈的讨论**](/pg/pgcondev-2024)，并且达成了共识。
最终体现在《[**PostgreSQL 17 发布注记！**](/pg/pg-17)》中。


<a href="/zh/blog/pg/pg-eat-deb-world"><img src="/img/pigsty/ecosystem.jpg" style="max-width: 1000px; max-height: 1000px; width: 100%; height: auto;"></a>


但真正重要的事情不是认识世界，而是改变世界。既然大家都已经认清了扩展很重要，**那么我们应该做什么，怎么做**，就成了真正关键的问题。 

那么什么是 PostgreSQL 扩展最关键的问题？在我看来，扩展用得上用不上，是 PG 扩展生态的首要问题。


--------

## PG 扩展分发现状

大家知道 PG 生态有很多扩展插件，但这些扩展插件如何安装使用？这第一道门槛就成了许多用户的拦路虎。怎么解决这个问题？
PGXN 说，用我的办法，我可以现场下载编译扩展；
Tembo 说，我提前帮你打好 docker 镜像；
StackGres 和 Omnigres 说，我们可以在线下载编译好的 So 文件；
八仙过海，各显神通。

大家都有很多好想法，唯独没仔细考虑绝大多数用户到底是如何安装扩展的。
作为前 DBA，我只能说什么现场编译，OCI镜像，下载so文件，在实战中都有些离谱了 —— **使用最广泛且最可靠的扩展安装方式，依然是用操作系统的包管理器安装签名二进制包**。
而 yum / dnf / apt 在解决这个问题上已经做的足够好了！所以真的问题其实是，谁来把这几百个扩展插件打成开箱即用的软件包？

[**TIME**](https://ext.pigsty.io/#/time): [`timescaledb`](https://ext.pigsty.io/#/timescaledb) [`timescaledb_toolkit`](https://ext.pigsty.io/#/timescaledb_toolkit) [`timeseries`](https://ext.pigsty.io/#/timeseries) [`periods`](https://ext.pigsty.io/#/periods) [`temporal_tables`](https://ext.pigsty.io/#/temporal_tables) [`emaj`](https://ext.pigsty.io/#/emaj) [`table_version`](https://ext.pigsty.io/#/table_version) [`pg_cron`](https://ext.pigsty.io/#/pg_cron) [`pg_later`](https://ext.pigsty.io/#/pg_later) [`pg_background`](https://ext.pigsty.io/#/pg_background) [**GIS**](https://ext.pigsty.io/#/gis): [`postgis`](https://ext.pigsty.io/#/postgis) [`postgis_topology`](https://ext.pigsty.io/#/postgis_topology) [`postgis_raster`](https://ext.pigsty.io/#/postgis_raster) [`postgis_sfcgal`](https://ext.pigsty.io/#/postgis_sfcgal) [`postgis_tiger_geocoder`](https://ext.pigsty.io/#/postgis_tiger_geocoder) [`address_standardizer`](https://ext.pigsty.io/#/address_standardizer) [`address_standardizer_data_us`](https://ext.pigsty.io/#/address_standardizer_data_us) [`pgrouting`](https://ext.pigsty.io/#/pgrouting) [`pointcloud`](https://ext.pigsty.io/#/pointcloud) [`pointcloud_postgis`](https://ext.pigsty.io/#/pointcloud_postgis) [`h3`](https://ext.pigsty.io/#/h3) [`h3_postgis`](https://ext.pigsty.io/#/h3_postgis) [`q3c`](https://ext.pigsty.io/#/q3c) [`ogr_fdw`](https://ext.pigsty.io/#/ogr_fdw) [`geoip`](https://ext.pigsty.io/#/geoip) [`pg_polyline`](https://ext.pigsty.io/#/pg_polyline) [`pg_geohash`](https://ext.pigsty.io/#/pg_geohash) [`mobilitydb`](https://ext.pigsty.io/#/mobilitydb) [`earthdistance`](https://ext.pigsty.io/#/earthdistance) [**RAG**](https://ext.pigsty.io/#/rag): [`vector`](https://ext.pigsty.io/#/vector) [`vectorscale`](https://ext.pigsty.io/#/vectorscale) [`vectorize`](https://ext.pigsty.io/#/vectorize) [`pg_similarity`](https://ext.pigsty.io/#/pg_similarity) [`smlar`](https://ext.pigsty.io/#/smlar) [`pg_summarize`](https://ext.pigsty.io/#/pg_summarize) [`pg_tiktoken`](https://ext.pigsty.io/#/pg_tiktoken) [`pgml`](https://ext.pigsty.io/#/pgml) [`pg4ml`](https://ext.pigsty.io/#/pg4ml) [**FTS**](https://ext.pigsty.io/#/fts): [`pg_search`](https://ext.pigsty.io/#/pg_search) [`pg_bigm`](https://ext.pigsty.io/#/pg_bigm) [`zhparser`](https://ext.pigsty.io/#/zhparser) [`hunspell_cs_cz`](https://ext.pigsty.io/#/hunspell_cs_cz) [`hunspell_de_de`](https://ext.pigsty.io/#/hunspell_de_de) [`hunspell_en_us`](https://ext.pigsty.io/#/hunspell_en_us) [`hunspell_fr`](https://ext.pigsty.io/#/hunspell_fr) [`hunspell_ne_np`](https://ext.pigsty.io/#/hunspell_ne_np) [`hunspell_nl_nl`](https://ext.pigsty.io/#/hunspell_nl_nl) [`hunspell_nn_no`](https://ext.pigsty.io/#/hunspell_nn_no) [`hunspell_pt_pt`](https://ext.pigsty.io/#/hunspell_pt_pt) [`hunspell_ru_ru`](https://ext.pigsty.io/#/hunspell_ru_ru) [`hunspell_ru_ru_aot`](https://ext.pigsty.io/#/hunspell_ru_ru_aot) [`fuzzystrmatch`](https://ext.pigsty.io/#/fuzzystrmatch) [`pg_trgm`](https://ext.pigsty.io/#/pg_trgm) [**OLAP**](https://ext.pigsty.io/#/olap): [`citus`](https://ext.pigsty.io/#/citus) [`citus_columnar`](https://ext.pigsty.io/#/citus_columnar) [`columnar`](https://ext.pigsty.io/#/columnar) [`pg_analytics`](https://ext.pigsty.io/#/pg_analytics) [`pg_duckdb`](https://ext.pigsty.io/#/pg_duckdb) [`pg_mooncake`](https://ext.pigsty.io/#/pg_mooncake) [`duckdb_fdw`](https://ext.pigsty.io/#/duckdb_fdw) [`pg_parquet`](https://ext.pigsty.io/#/pg_parquet) [`pg_fkpart`](https://ext.pigsty.io/#/pg_fkpart) [`pg_partman`](https://ext.pigsty.io/#/pg_partman) [`plproxy`](https://ext.pigsty.io/#/plproxy) [`pg_strom`](https://ext.pigsty.io/#/pg_strom) [`tablefunc`](https://ext.pigsty.io/#/tablefunc) [**FEAT**](https://ext.pigsty.io/#/feat): [`age`](https://ext.pigsty.io/#/age) [`hll`](https://ext.pigsty.io/#/hll) [`rum`](https://ext.pigsty.io/#/rum) [`pg_graphql`](https://ext.pigsty.io/#/pg_graphql) [`pg_jsonschema`](https://ext.pigsty.io/#/pg_jsonschema) [`jsquery`](https://ext.pigsty.io/#/jsquery) [`pg_hint_plan`](https://ext.pigsty.io/#/pg_hint_plan) [`hypopg`](https://ext.pigsty.io/#/hypopg) [`index_advisor`](https://ext.pigsty.io/#/index_advisor) [`plan_filter`](https://ext.pigsty.io/#/plan_filter) [`imgsmlr`](https://ext.pigsty.io/#/imgsmlr) [`pg_ivm`](https://ext.pigsty.io/#/pg_ivm) [`pgmq`](https://ext.pigsty.io/#/pgmq) [`pgq`](https://ext.pigsty.io/#/pgq) [`pg_cardano`](https://ext.pigsty.io/#/pg_cardano) [`rdkit`](https://ext.pigsty.io/#/rdkit) [`bloom`](https://ext.pigsty.io/#/bloom) [**LANG**](https://ext.pigsty.io/#/lang): [`pg_tle`](https://ext.pigsty.io/#/pg_tle) [`plv8`](https://ext.pigsty.io/#/plv8) [`pllua`](https://ext.pigsty.io/#/pllua) [`hstore_pllua`](https://ext.pigsty.io/#/hstore_pllua) [`plluau`](https://ext.pigsty.io/#/plluau) [`hstore_plluau`](https://ext.pigsty.io/#/hstore_plluau) [`plprql`](https://ext.pigsty.io/#/plprql) [`pldbgapi`](https://ext.pigsty.io/#/pldbgapi) [`plpgsql_check`](https://ext.pigsty.io/#/plpgsql_check) [`plprofiler`](https://ext.pigsty.io/#/plprofiler) [`plsh`](https://ext.pigsty.io/#/plsh) [`pljava`](https://ext.pigsty.io/#/pljava) [`plr`](https://ext.pigsty.io/#/plr) [`pgtap`](https://ext.pigsty.io/#/pgtap) [`faker`](https://ext.pigsty.io/#/faker) [`dbt2`](https://ext.pigsty.io/#/dbt2) [`pltcl`](https://ext.pigsty.io/#/pltcl) [`pltclu`](https://ext.pigsty.io/#/pltclu) [`plperl`](https://ext.pigsty.io/#/plperl) [`bool_plperl`](https://ext.pigsty.io/#/bool_plperl) [`hstore_plperl`](https://ext.pigsty.io/#/hstore_plperl) [`jsonb_plperl`](https://ext.pigsty.io/#/jsonb_plperl) [`plperlu`](https://ext.pigsty.io/#/plperlu) [`bool_plperlu`](https://ext.pigsty.io/#/bool_plperlu) [`jsonb_plperlu`](https://ext.pigsty.io/#/jsonb_plperlu) [`hstore_plperlu`](https://ext.pigsty.io/#/hstore_plperlu) [`plpgsql`](https://ext.pigsty.io/#/plpgsql) [`plpython3u`](https://ext.pigsty.io/#/plpython3u) [`jsonb_plpython3u`](https://ext.pigsty.io/#/jsonb_plpython3u) [`ltree_plpython3u`](https://ext.pigsty.io/#/ltree_plpython3u) [`hstore_plpython3u`](https://ext.pigsty.io/#/hstore_plpython3u) [**TYPE**](https://ext.pigsty.io/#/type): [`prefix`](https://ext.pigsty.io/#/prefix) [`semver`](https://ext.pigsty.io/#/semver) [`unit`](https://ext.pigsty.io/#/unit) [`md5hash`](https://ext.pigsty.io/#/md5hash) [`asn1oid`](https://ext.pigsty.io/#/asn1oid) [`roaringbitmap`](https://ext.pigsty.io/#/roaringbitmap) [`pgfaceting`](https://ext.pigsty.io/#/pgfaceting) [`pg_sphere`](https://ext.pigsty.io/#/pg_sphere) [`country`](https://ext.pigsty.io/#/country) [`currency`](https://ext.pigsty.io/#/currency) [`pgmp`](https://ext.pigsty.io/#/pgmp) [`numeral`](https://ext.pigsty.io/#/numeral) [`pg_rational`](https://ext.pigsty.io/#/pg_rational) [`uint`](https://ext.pigsty.io/#/uint) [`uint128`](https://ext.pigsty.io/#/uint128) [`ip4r`](https://ext.pigsty.io/#/ip4r) [`uri`](https://ext.pigsty.io/#/uri) [`pgemailaddr`](https://ext.pigsty.io/#/pgemailaddr) [`acl`](https://ext.pigsty.io/#/acl) [`debversion`](https://ext.pigsty.io/#/debversion) [`pg_rrule`](https://ext.pigsty.io/#/pg_rrule) [`timestamp9`](https://ext.pigsty.io/#/timestamp9) [`chkpass`](https://ext.pigsty.io/#/chkpass) [`isn`](https://ext.pigsty.io/#/isn) [`seg`](https://ext.pigsty.io/#/seg) [`cube`](https://ext.pigsty.io/#/cube) [`ltree`](https://ext.pigsty.io/#/ltree) [`hstore`](https://ext.pigsty.io/#/hstore) [`citext`](https://ext.pigsty.io/#/citext) [`xml2`](https://ext.pigsty.io/#/xml2) [**FUNC**](https://ext.pigsty.io/#/func): [`topn`](https://ext.pigsty.io/#/topn) [`gzip`](https://ext.pigsty.io/#/gzip) [`zstd`](https://ext.pigsty.io/#/zstd) [`http`](https://ext.pigsty.io/#/http) [`pg_net`](https://ext.pigsty.io/#/pg_net) [`pg_smtp_client`](https://ext.pigsty.io/#/pg_smtp_client) [`pg_html5_email_address`](https://ext.pigsty.io/#/pg_html5_email_address) [`pgsql_tweaks`](https://ext.pigsty.io/#/pgsql_tweaks) [`pg_extra_time`](https://ext.pigsty.io/#/pg_extra_time) [`timeit`](https://ext.pigsty.io/#/timeit) [`count_distinct`](https://ext.pigsty.io/#/count_distinct) [`extra_window_functions`](https://ext.pigsty.io/#/extra_window_functions) [`first_last_agg`](https://ext.pigsty.io/#/first_last_agg) [`tdigest`](https://ext.pigsty.io/#/tdigest) [`aggs_for_vecs`](https://ext.pigsty.io/#/aggs_for_vecs) [`aggs_for_arrays`](https://ext.pigsty.io/#/aggs_for_arrays) [`arraymath`](https://ext.pigsty.io/#/arraymath) [`quantile`](https://ext.pigsty.io/#/quantile) [`lower_quantile`](https://ext.pigsty.io/#/lower_quantile) [`pg_idkit`](https://ext.pigsty.io/#/pg_idkit) [`pg_uuidv7`](https://ext.pigsty.io/#/pg_uuidv7) [`permuteseq`](https://ext.pigsty.io/#/permuteseq) [`pg_hashids`](https://ext.pigsty.io/#/pg_hashids) [`sequential_uuids`](https://ext.pigsty.io/#/sequential_uuids) [`pg_math`](https://ext.pigsty.io/#/pg_math) [`random`](https://ext.pigsty.io/#/random) [`base36`](https://ext.pigsty.io/#/base36) [`base62`](https://ext.pigsty.io/#/base62) [`pg_base58`](https://ext.pigsty.io/#/pg_base58) [`floatvec`](https://ext.pigsty.io/#/floatvec) [`financial`](https://ext.pigsty.io/#/financial) [`pgjwt`](https://ext.pigsty.io/#/pgjwt) [`pg_hashlib`](https://ext.pigsty.io/#/pg_hashlib) [`shacrypt`](https://ext.pigsty.io/#/shacrypt) [`cryptint`](https://ext.pigsty.io/#/cryptint) [`pguecc`](https://ext.pigsty.io/#/pguecc) [`pgpcre`](https://ext.pigsty.io/#/pgpcre) [`icu_ext`](https://ext.pigsty.io/#/icu_ext) [`pgqr`](https://ext.pigsty.io/#/pgqr) [`envvar`](https://ext.pigsty.io/#/envvar) [`pg_protobuf`](https://ext.pigsty.io/#/pg_protobuf) [`url_encode`](https://ext.pigsty.io/#/url_encode) [`refint`](https://ext.pigsty.io/#/refint) [`autoinc`](https://ext.pigsty.io/#/autoinc) [`insert_username`](https://ext.pigsty.io/#/insert_username) [`moddatetime`](https://ext.pigsty.io/#/moddatetime) [`tsm_system_time`](https://ext.pigsty.io/#/tsm_system_time) [`dict_xsyn`](https://ext.pigsty.io/#/dict_xsyn) [`tsm_system_rows`](https://ext.pigsty.io/#/tsm_system_rows) [`tcn`](https://ext.pigsty.io/#/tcn) [`uuid-ossp`](https://ext.pigsty.io/#/uuid-ossp) [`btree_gist`](https://ext.pigsty.io/#/btree_gist) [`btree_gin`](https://ext.pigsty.io/#/btree_gin) [`intarray`](https://ext.pigsty.io/#/intarray) [`intagg`](https://ext.pigsty.io/#/intagg) [`dict_int`](https://ext.pigsty.io/#/dict_int) [`unaccent`](https://ext.pigsty.io/#/unaccent) [**ADMIN**](https://ext.pigsty.io/#/admin): [`pg_repack`](https://ext.pigsty.io/#/pg_repack) [`pg_squeeze`](https://ext.pigsty.io/#/pg_squeeze) [`pg_dirtyread`](https://ext.pigsty.io/#/pg_dirtyread) [`pgfincore`](https://ext.pigsty.io/#/pgfincore) [`pgdd`](https://ext.pigsty.io/#/pgdd) [`ddlx`](https://ext.pigsty.io/#/ddlx) [`prioritize`](https://ext.pigsty.io/#/prioritize) [`pg_checksums`](https://ext.pigsty.io/#/pg_checksums) [`pg_readonly`](https://ext.pigsty.io/#/pg_readonly) [`safeupdate`](https://ext.pigsty.io/#/safeupdate) [`pg_permissions`](https://ext.pigsty.io/#/pg_permissions) [`pgautofailover`](https://ext.pigsty.io/#/pgautofailover) [`pg_catcheck`](https://ext.pigsty.io/#/pg_catcheck) [`pre_prepare`](https://ext.pigsty.io/#/pre_prepare) [`pgcozy`](https://ext.pigsty.io/#/pgcozy) [`pg_orphaned`](https://ext.pigsty.io/#/pg_orphaned) [`pg_crash`](https://ext.pigsty.io/#/pg_crash) [`pg_cheat_funcs`](https://ext.pigsty.io/#/pg_cheat_funcs) [`pg_savior`](https://ext.pigsty.io/#/pg_savior) [`table_log`](https://ext.pigsty.io/#/table_log) [`pg_fio`](https://ext.pigsty.io/#/pg_fio) [`pgpool_adm`](https://ext.pigsty.io/#/pgpool_adm) [`pgpool_recovery`](https://ext.pigsty.io/#/pgpool_recovery) [`pgpool_regclass`](https://ext.pigsty.io/#/pgpool_regclass) [`pgagent`](https://ext.pigsty.io/#/pgagent) [`vacuumlo`](https://ext.pigsty.io/#/vacuumlo) [`pg_prewarm`](https://ext.pigsty.io/#/pg_prewarm) [`oid2name`](https://ext.pigsty.io/#/oid2name) [`lo`](https://ext.pigsty.io/#/lo) [`basic_archive`](https://ext.pigsty.io/#/basic_archive) [`basebackup_to_shell`](https://ext.pigsty.io/#/basebackup_to_shell) [`old_snapshot`](https://ext.pigsty.io/#/old_snapshot) [`adminpack`](https://ext.pigsty.io/#/adminpack) [`amcheck`](https://ext.pigsty.io/#/amcheck) [`pg_surgery`](https://ext.pigsty.io/#/pg_surgery) [**STAT**](https://ext.pigsty.io/#/stat): [`pg_profile`](https://ext.pigsty.io/#/pg_profile) [`pg_show_plans`](https://ext.pigsty.io/#/pg_show_plans) [`pg_stat_kcache`](https://ext.pigsty.io/#/pg_stat_kcache) [`pg_stat_monitor`](https://ext.pigsty.io/#/pg_stat_monitor) [`pg_qualstats`](https://ext.pigsty.io/#/pg_qualstats) [`pg_store_plans`](https://ext.pigsty.io/#/pg_store_plans) [`pg_track_settings`](https://ext.pigsty.io/#/pg_track_settings) [`pg_wait_sampling`](https://ext.pigsty.io/#/pg_wait_sampling) [`system_stats`](https://ext.pigsty.io/#/system_stats) [`meta`](https://ext.pigsty.io/#/meta) [`pgnodemx`](https://ext.pigsty.io/#/pgnodemx) [`pg_proctab`](https://ext.pigsty.io/#/pg_proctab) [`pg_sqlog`](https://ext.pigsty.io/#/pg_sqlog) [`bgw_replstatus`](https://ext.pigsty.io/#/bgw_replstatus) [`pgmeminfo`](https://ext.pigsty.io/#/pgmeminfo) [`toastinfo`](https://ext.pigsty.io/#/toastinfo) [`explain_ui`](https://ext.pigsty.io/#/explain_ui) [`pg_relusage`](https://ext.pigsty.io/#/pg_relusage) [`pg_top`](https://ext.pigsty.io/#/pg_top) [`pagevis`](https://ext.pigsty.io/#/pagevis) [`powa`](https://ext.pigsty.io/#/powa) [`pageinspect`](https://ext.pigsty.io/#/pageinspect) [`pgrowlocks`](https://ext.pigsty.io/#/pgrowlocks) [`sslinfo`](https://ext.pigsty.io/#/sslinfo) [`pg_buffercache`](https://ext.pigsty.io/#/pg_buffercache) [`pg_walinspect`](https://ext.pigsty.io/#/pg_walinspect) [`pg_freespacemap`](https://ext.pigsty.io/#/pg_freespacemap) [`pg_visibility`](https://ext.pigsty.io/#/pg_visibility) [`pgstattuple`](https://ext.pigsty.io/#/pgstattuple) [`auto_explain`](https://ext.pigsty.io/#/auto_explain) [`pg_stat_statements`](https://ext.pigsty.io/#/pg_stat_statements) [**SEC**](https://ext.pigsty.io/#/sec): [`passwordcheck_cracklib`](https://ext.pigsty.io/#/passwordcheck_cracklib) [`supautils`](https://ext.pigsty.io/#/supautils) [`pgsodium`](https://ext.pigsty.io/#/pgsodium) [`supabase_vault`](https://ext.pigsty.io/#/supabase_vault) [`pg_session_jwt`](https://ext.pigsty.io/#/pg_session_jwt) [`anon`](https://ext.pigsty.io/#/anon) [`pg_tde`](https://ext.pigsty.io/#/pg_tde) [`pgsmcrypto`](https://ext.pigsty.io/#/pgsmcrypto) [`pgaudit`](https://ext.pigsty.io/#/pgaudit) [`pgauditlogtofile`](https://ext.pigsty.io/#/pgauditlogtofile) [`pg_auth_mon`](https://ext.pigsty.io/#/pg_auth_mon) [`credcheck`](https://ext.pigsty.io/#/credcheck) [`pgcryptokey`](https://ext.pigsty.io/#/pgcryptokey) [`pg_jobmon`](https://ext.pigsty.io/#/pg_jobmon) [`logerrors`](https://ext.pigsty.io/#/logerrors) [`login_hook`](https://ext.pigsty.io/#/login_hook) [`set_user`](https://ext.pigsty.io/#/set_user) [`pg_snakeoil`](https://ext.pigsty.io/#/pg_snakeoil) [`pgextwlist`](https://ext.pigsty.io/#/pgextwlist) [`pg_auditor`](https://ext.pigsty.io/#/pg_auditor) [`sslutils`](https://ext.pigsty.io/#/sslutils) [`noset`](https://ext.pigsty.io/#/noset) [`sepgsql`](https://ext.pigsty.io/#/sepgsql) [`auth_delay`](https://ext.pigsty.io/#/auth_delay) [`pgcrypto`](https://ext.pigsty.io/#/pgcrypto) [`passwordcheck`](https://ext.pigsty.io/#/passwordcheck) [**FDW**](https://ext.pigsty.io/#/fdw): [`wrappers`](https://ext.pigsty.io/#/wrappers) [`multicorn`](https://ext.pigsty.io/#/multicorn) [`odbc_fdw`](https://ext.pigsty.io/#/odbc_fdw) [`jdbc_fdw`](https://ext.pigsty.io/#/jdbc_fdw) [`mysql_fdw`](https://ext.pigsty.io/#/mysql_fdw) [`oracle_fdw`](https://ext.pigsty.io/#/oracle_fdw) [`tds_fdw`](https://ext.pigsty.io/#/tds_fdw) [`db2_fdw`](https://ext.pigsty.io/#/db2_fdw) [`sqlite_fdw`](https://ext.pigsty.io/#/sqlite_fdw) [`pgbouncer_fdw`](https://ext.pigsty.io/#/pgbouncer_fdw) [`mongo_fdw`](https://ext.pigsty.io/#/mongo_fdw) [`redis_fdw`](https://ext.pigsty.io/#/redis_fdw) [`redis`](https://ext.pigsty.io/#/redis) [`kafka_fdw`](https://ext.pigsty.io/#/kafka_fdw) [`hdfs_fdw`](https://ext.pigsty.io/#/hdfs_fdw) [`firebird_fdw`](https://ext.pigsty.io/#/firebird_fdw) [`aws_s3`](https://ext.pigsty.io/#/aws_s3) [`log_fdw`](https://ext.pigsty.io/#/log_fdw) [`dblink`](https://ext.pigsty.io/#/dblink) [`file_fdw`](https://ext.pigsty.io/#/file_fdw) [`postgres_fdw`](https://ext.pigsty.io/#/postgres_fdw) [**SIM**](https://ext.pigsty.io/#/sim): [`orafce`](https://ext.pigsty.io/#/orafce) [`pgtt`](https://ext.pigsty.io/#/pgtt) [`session_variable`](https://ext.pigsty.io/#/session_variable) [`pg_statement_rollback`](https://ext.pigsty.io/#/pg_statement_rollback) [`pg_dbms_metadata`](https://ext.pigsty.io/#/pg_dbms_metadata) [`pg_dbms_lock`](https://ext.pigsty.io/#/pg_dbms_lock) [`pg_dbms_job`](https://ext.pigsty.io/#/pg_dbms_job) [`babelfishpg_common`](https://ext.pigsty.io/#/babelfishpg_common) [`babelfishpg_tsql`](https://ext.pigsty.io/#/babelfishpg_tsql) [`babelfishpg_tds`](https://ext.pigsty.io/#/babelfishpg_tds) [`babelfishpg_money`](https://ext.pigsty.io/#/babelfishpg_money) [`pgmemcache`](https://ext.pigsty.io/#/pgmemcache) [**ETL**](https://ext.pigsty.io/#/etl): [`pglogical`](https://ext.pigsty.io/#/pglogical) [`pglogical_origin`](https://ext.pigsty.io/#/pglogical_origin) [`pglogical_ticker`](https://ext.pigsty.io/#/pglogical_ticker) [`pgl_ddl_deploy`](https://ext.pigsty.io/#/pgl_ddl_deploy) [`pg_failover_slots`](https://ext.pigsty.io/#/pg_failover_slots) [`wal2json`](https://ext.pigsty.io/#/wal2json) [`wal2mongo`](https://ext.pigsty.io/#/wal2mongo) [`decoderbufs`](https://ext.pigsty.io/#/decoderbufs) [`decoder_raw`](https://ext.pigsty.io/#/decoder_raw) [`test_decoding`](https://ext.pigsty.io/#/test_decoding) [`mimeo`](https://ext.pigsty.io/#/mimeo) [`repmgr`](https://ext.pigsty.io/#/repmgr) [`pg_fact_loader`](https://ext.pigsty.io/#/pg_fact_loader) [`pg_bulkload`](https://ext.pigsty.io/#/pg_bulkload)


PostgreSQL 的 PGDG 官方仓库中，提供了大约 **100** 个左右的扩展，但存在各种问题：有的扩展在 Debian/Ubuntu 的 APT 仓库里有，在 EL 系统的 YUM 仓库里没有；
有的扩展在 EL8 上有，EL9 没有；有的扩展在 Ubuntu 22 上有，在 24 上没有；有的扩展针对 PostgreSQL 12 - 15 提供，PG 16，17 不提供；有的扩展只有 x86_64 架构，没有 arm 架构；有时候碰上这种问题确实蛮让人头疼。



--------

## 怎么办？我行我上！

作为一个 PostgreSQL 发行版维护者，我曾经寄希望于 PG 生态的其他人来解决这个问题。
每当我看见 PGDG 仓库有出现错漏缺失，我都会第一时间反馈给仓库维护者 Devrim 和 Cris 。

有的时候这种模式挺管用，比如去年当我发现 pgvector 这个强力向量数据库扩展还没有二进制软件包制成品时，我第一时间[提给 Devrim](https://github.com/pgvector/pgvector/issues/76) ，
[将其放入 PGDG 仓库](/pg/vector-json-pg/#译者评论)，然后 pgvector 遂成为 PG 生态中的向量数据库事实标准，进入到各家云厂商 RDS 中。

但有的时候，事情并不能总能如意。例如，**Devrim** 表示，他绝对不会接受任何 Rust 扩展插件进入 PGDG YUM 仓库。
但我确实有二十多个用 Rust 编写的 PostgreSQL 扩展需要分发（例如自建 Supabase 就需要 pg_graphql, pg_jsonschema, wrappers 三个 Rust 扩展），怎么办呢？

再比如说，最近 PG 生态非常火热的 [DuckDB 缝合大赛](/pg/pg-duckdb)，大家都在密集地更新跟进 DuckDB 系扩展 ，这些扩展插件我第一时间 [打好了 RPM/DEB 包](https://ext.pigsty.io/#/olap)，但是如何分发呢？

思来想去，我决定还是我行我上，自己维护一个 PostgreSQL 扩展插件的 APT / YUM 仓库，分发 PG 扩展。

<a href="https://ext.pigsty.io"><img src="ext-website.png" style="max-width: 800px; width: 100%; height: auto;"></a>


--------


## PG 扩展大全

在过去的半年中，我的工作重心放在 PG 扩展生态的整合上。而最近，这项工作终于达到了一个让我自己感到满意的里程碑。我建设了一个 PG Yum/APT 仓库，收录了 340 个可用 PG 扩展的元数据，以及二进制制成品。

| Entry / Filter | All | PGDG | PIGSTY | CONTRIB | MISC | MISS | PG17 | PG16 | PG15 | PG14 | PG13 | PG12 |
|:--------------:|:---:|:----:|:------:|:-------:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| RPM Extension  | 334 | 119  |  139   |   70    |  4   |  6   | 301  | 330  | 333  | 319  | 307  | 294  |
| DEB Extension  | 326 | 104  |  143   |   70    |  5   |  14  | 302  | 322  | 325  | 316  | 303  | 293  |
|  RPM Package   | 251 | 107  |  138   |    1    |  4   |  1   | 220  | 247  | 250  | 239  | 229  | 216  |
|  DEB Package   | 241 |  90  |  142   |    1    |  5   |  1   | 218  | 237  | 240  | 234  | 223  | 213  |


以上是这个仓库的一些统计数字：总共有 340 个可用 Extension，去除 PG 自带的 70 个，总共 270 个第三方扩展插件。这 270 个扩展插件中，有小一半是 PGDG 官方仓库维护的（126个RPM扩展，102个DEB扩展），另外的大一半（131个RPM，143个DEB）都是由我维护，修复，编译，打包，测试，分发的。

每一个扩展，我都针对最新的 PostgreSQL 12 - 17 这六个生命周期大版本分别打包构建，针对 EL8，EL9，Ubuntu 22.04，Ubuntu 24.04，以及 Debian 12 这五个绝对主流 Linux 发行版构建。此外也对 EL7，Debian 11， Ubuntu 20.04 这些过保系统提供部分有限支持。

<a href="https://ext.pigsty.io"><img src="usage.png" style="max-width: 800px; max-height: 800px; width: 100%; height: auto;"></a>


这个仓库还解决了扩展对齐的问题，例如，原本在 APT 和 YUM 仓库中的扩展，APT 有一小半几十个扩展 YUM 仓库没有，YUM 仓库有一小半 APT 仓库没有。我把两者独有的扩展都尽可能移植到另一个操作系统生态中，现在只有 7 个 APT 扩展在 YUM 仓库中缺失，16 个扩展在 APT 仓库缺失，只占总数的 6%。很多 PGDG 扩展版本缺失的问题，也在这里得到了一并修复。

我提供了一个完整的目录，列出了支持的扩展，并且对每一个扩展，都给出了详情，依赖安装说明与注意事项。


<a href="https://ext.pigsty.io/#/postgis"><img src="postgis.png" style="max-width: 1200px; width: 100%; height: auto;"></a>


我想，用户吭哧吭哧抱怨扩展编译失败的问题，应该能在这里得到最终的解决。

当然题外话是广告时间，安装这些扩展，使用这个仓库的最简单的方式是什么？当然是开箱即用的 PostgreSQL 数据库发行版 —— **Pigsty** —— **但这并非必选项**。
你依然可以用简单的一行 shell 在任何 EL/Debian/Ubuntu 系统上启用此仓库。





<details><summary>使用Pigsty一次性配置好并拉起用于自建Supabase的PostgreSQL集群，只要简单地声明要安装哪些扩展插件即可！</summary><br>

一键自建 Supabase 所需的 PostgreSQL 集群，请参考样例配置文件： [`conf/dbms/supabase.yml`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml)。

```yaml
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
    # supabase required extensions
    pg_libs: 'pg_stat_statements, pgaudit, plpgsql, plpgsql_check, pg_cron, pg_net, timescaledb, auto_explain, pg_tle, plan_filter'
    pg_extensions: # extensions to be installed on this cluster
      - supa-stack
      - timescaledb pg_cron pg_timetable
      - postgis pg_geohash
      - pgvector pgvectorscale pg_similarity smlar pg_summarize pg_tiktoken
      - pg_search pg_bigm zhparser hunspell
      - pg_analytics pg_parquet pg_duckdb
      - pg_hint_plan hll rum pg_graphql pg_jsonschema index_advisor pg_plan_filter hypopg pg_ivm pgmq pg_cardano
      - pg_tle plv8 plpgsql_check #pljava
      - pgunit md5hash asn1oid roaringbitmap pgfaceting pgsphere pg_country pg_currency pgmp numeral pg_rational pguint pg_uint128 ip4r pg_uri pgemailaddr acl timestamp9
      - pg_gzip pg_zstd pg_http pg_net pg_html5_email_address pgsql_tweaks pg_extra_time pg_timeit count_distinct extra_window_functions first_last_agg tdigest aggs_for_arrays aggs_for_vecs pg_arraymath quantile lower_quantile
      - pg_idkit pg_uuidv7 permuteseq pg_hashids sequential_uuids pg_math pg_random pg_base36 pg_base62 pg_base58 floatvec pg_financial pgjwt pg_hashlib shacrypt cryptint pg_ecdsa pgpcre icu_ext pgqr envvar pg_protobuf url_encode
      - pg_repack pg_squeeze pg_dirtyread ddlx pg_readonly safeupdate pg_permissions pg_savior pg_fio
      - pg_profile pg_show_plans pg_stat_kcache pg_stat_monitor pg_qualstats pg_track_settings system_stats pg_meta pgnodemx pg_sqlog bgw_replstatus toastinfo pg_explain_ui pg_relusage
      - passwordcheck supautils pgsodium pg_vault anonymizer pgsmcrypto pgaudit pgauditlogtofile pg_auth_mon credcheck logerrors login_hook set_user pgextwlist pg_auditor sslutils noset
      - wrappers mysql_fdw redis_fdw pg_redis_pubsub aws_s3 log_fdw
      - pglogical wal2json decoder_raw pg_fact_loader
    pg_parameters:
      cron.database_name: postgres
      pgsodium.enable_event_trigger: off
    pg_hba_rules: # supabase hba rules, require access from docker network
      - { user: all ,db: postgres  ,addr: intra         ,auth: pwd ,title: 'allow supabase access from intranet'    }
      - { user: all ,db: postgres  ,addr: 172.17.0.0/16 ,auth: pwd ,title: 'allow access from local docker network' }
    pg_vip_enabled: true
    pg_vip_address: 10.10.10.2/24
    pg_vip_interface: eth1
```


</details>



--------------

## 这个仓库里有什么？

在 Pigsty 的扩展仓库中，所有的扩展都已经被预先分为了十五类之一：TIME，GIS，RAG，FTS，OLAP，FEAT，LANG，TYPE，FUNC，ADMIN，STAT，SEC，FDW，SIM，ETL，如下所示。

请移步 [ext.pigsty.io](https://ext.pigsty.io) 查看完整详情。

[**TIME**](/time): [`timescaledb`](/timescaledb) [`timescaledb_toolkit`](/timescaledb_toolkit) [`timeseries`](/timeseries) [`periods`](/periods) [`temporal_tables`](/temporal_tables) [`emaj`](/emaj) [`table_version`](/table_version) [`pg_cron`](/pg_cron) [`pg_later`](/pg_later) [`pg_background`](/pg_background)
[**GIS**](/gis): [`postgis`](/postgis) [`postgis_topology`](/postgis_topology) [`postgis_raster`](/postgis_raster) [`postgis_sfcgal`](/postgis_sfcgal) [`postgis_tiger_geocoder`](/postgis_tiger_geocoder) [`address_standardizer`](/address_standardizer) [`address_standardizer_data_us`](/address_standardizer_data_us) [`pgrouting`](/pgrouting) [`pointcloud`](/pointcloud) [`pointcloud_postgis`](/pointcloud_postgis) [`h3`](/h3) [`h3_postgis`](/h3_postgis) [`q3c`](/q3c) [`ogr_fdw`](/ogr_fdw) [`geoip`](/geoip) [`pg_polyline`](/pg_polyline) [`pg_geohash`](/pg_geohash) [`mobilitydb`](/mobilitydb) [`earthdistance`](/earthdistance)
[**RAG**](/rag): [`vector`](/vector) [`vectorscale`](/vectorscale) [`vectorize`](/vectorize) [`pg_similarity`](/pg_similarity) [`smlar`](/smlar) [`pg_summarize`](/pg_summarize) [`pg_tiktoken`](/pg_tiktoken) [`pgml`](/pgml) [`pg4ml`](/pg4ml)
[**FTS**](/fts): [`pg_search`](/pg_search) [`pg_bigm`](/pg_bigm) [`zhparser`](/zhparser) [`hunspell_cs_cz`](/hunspell_cs_cz) [`hunspell_de_de`](/hunspell_de_de) [`hunspell_en_us`](/hunspell_en_us) [`hunspell_fr`](/hunspell_fr) [`hunspell_ne_np`](/hunspell_ne_np) [`hunspell_nl_nl`](/hunspell_nl_nl) [`hunspell_nn_no`](/hunspell_nn_no) [`hunspell_pt_pt`](/hunspell_pt_pt) [`hunspell_ru_ru`](/hunspell_ru_ru) [`hunspell_ru_ru_aot`](/hunspell_ru_ru_aot) [`fuzzystrmatch`](/fuzzystrmatch) [`pg_trgm`](/pg_trgm)
[**OLAP**](/olap): [`citus`](/citus) [`citus_columnar`](/citus_columnar) [`columnar`](/columnar) [`pg_analytics`](/pg_analytics) [`pg_duckdb`](/pg_duckdb) [`pg_mooncake`](/pg_mooncake) [`duckdb_fdw`](/duckdb_fdw) [`pg_parquet`](/pg_parquet) [`pg_fkpart`](/pg_fkpart) [`pg_partman`](/pg_partman) [`plproxy`](/plproxy) [`pg_strom`](/pg_strom) [`tablefunc`](/tablefunc)
[**FEAT**](/feat): [`age`](/age) [`hll`](/hll) [`rum`](/rum) [`pg_graphql`](/pg_graphql) [`pg_jsonschema`](/pg_jsonschema) [`jsquery`](/jsquery) [`pg_hint_plan`](/pg_hint_plan) [`hypopg`](/hypopg) [`index_advisor`](/index_advisor) [`plan_filter`](/plan_filter) [`imgsmlr`](/imgsmlr) [`pg_ivm`](/pg_ivm) [`pgmq`](/pgmq) [`pgq`](/pgq) [`pg_cardano`](/pg_cardano) [`rdkit`](/rdkit) [`bloom`](/bloom)
[**LANG**](/lang): [`pg_tle`](/pg_tle) [`plv8`](/plv8) [`pllua`](/pllua) [`hstore_pllua`](/hstore_pllua) [`plluau`](/plluau) [`hstore_plluau`](/hstore_plluau) [`plprql`](/plprql) [`pldbgapi`](/pldbgapi) [`plpgsql_check`](/plpgsql_check) [`plprofiler`](/plprofiler) [`plsh`](/plsh) [`pljava`](/pljava) [`plr`](/plr) [`pgtap`](/pgtap) [`faker`](/faker) [`dbt2`](/dbt2) [`pltcl`](/pltcl) [`pltclu`](/pltclu) [`plperl`](/plperl) [`bool_plperl`](/bool_plperl) [`hstore_plperl`](/hstore_plperl) [`jsonb_plperl`](/jsonb_plperl) [`plperlu`](/plperlu) [`bool_plperlu`](/bool_plperlu) [`jsonb_plperlu`](/jsonb_plperlu) [`hstore_plperlu`](/hstore_plperlu) [`plpgsql`](/plpgsql) [`plpython3u`](/plpython3u) [`jsonb_plpython3u`](/jsonb_plpython3u) [`ltree_plpython3u`](/ltree_plpython3u) [`hstore_plpython3u`](/hstore_plpython3u)
[**TYPE**](/type): [`prefix`](/prefix) [`semver`](/semver) [`unit`](/unit) [`md5hash`](/md5hash) [`asn1oid`](/asn1oid) [`roaringbitmap`](/roaringbitmap) [`pgfaceting`](/pgfaceting) [`pg_sphere`](/pg_sphere) [`country`](/country) [`currency`](/currency) [`pgmp`](/pgmp) [`numeral`](/numeral) [`pg_rational`](/pg_rational) [`uint`](/uint) [`uint128`](/uint128) [`ip4r`](/ip4r) [`uri`](/uri) [`pgemailaddr`](/pgemailaddr) [`acl`](/acl) [`debversion`](/debversion) [`pg_rrule`](/pg_rrule) [`timestamp9`](/timestamp9) [`chkpass`](/chkpass) [`isn`](/isn) [`seg`](/seg) [`cube`](/cube) [`ltree`](/ltree) [`hstore`](/hstore) [`citext`](/citext) [`xml2`](/xml2)
[**FUNC**](/func): [`topn`](/topn) [`gzip`](/gzip) [`zstd`](/zstd) [`http`](/http) [`pg_net`](/pg_net) [`pg_smtp_client`](/pg_smtp_client) [`pg_html5_email_address`](/pg_html5_email_address) [`pgsql_tweaks`](/pgsql_tweaks) [`pg_extra_time`](/pg_extra_time) [`timeit`](/timeit) [`count_distinct`](/count_distinct) [`extra_window_functions`](/extra_window_functions) [`first_last_agg`](/first_last_agg) [`tdigest`](/tdigest) [`aggs_for_vecs`](/aggs_for_vecs) [`aggs_for_arrays`](/aggs_for_arrays) [`arraymath`](/arraymath) [`quantile`](/quantile) [`lower_quantile`](/lower_quantile) [`pg_idkit`](/pg_idkit) [`pg_uuidv7`](/pg_uuidv7) [`permuteseq`](/permuteseq) [`pg_hashids`](/pg_hashids) [`sequential_uuids`](/sequential_uuids) [`pg_math`](/pg_math) [`random`](/random) [`base36`](/base36) [`base62`](/base62) [`pg_base58`](/pg_base58) [`floatvec`](/floatvec) [`financial`](/financial) [`pgjwt`](/pgjwt) [`pg_hashlib`](/pg_hashlib) [`shacrypt`](/shacrypt) [`cryptint`](/cryptint) [`pguecc`](/pguecc) [`pgpcre`](/pgpcre) [`icu_ext`](/icu_ext) [`pgqr`](/pgqr) [`envvar`](/envvar) [`pg_protobuf`](/pg_protobuf) [`url_encode`](/url_encode) [`refint`](/refint) [`autoinc`](/autoinc) [`insert_username`](/insert_username) [`moddatetime`](/moddatetime) [`tsm_system_time`](/tsm_system_time) [`dict_xsyn`](/dict_xsyn) [`tsm_system_rows`](/tsm_system_rows) [`tcn`](/tcn) [`uuid-ossp`](/uuid-ossp) [`btree_gist`](/btree_gist) [`btree_gin`](/btree_gin) [`intarray`](/intarray) [`intagg`](/intagg) [`dict_int`](/dict_int) [`unaccent`](/unaccent)
[**ADMIN**](/admin): [`pg_repack`](/pg_repack) [`pg_squeeze`](/pg_squeeze) [`pg_dirtyread`](/pg_dirtyread) [`pgfincore`](/pgfincore) [`pgdd`](/pgdd) [`ddlx`](/ddlx) [`prioritize`](/prioritize) [`pg_checksums`](/pg_checksums) [`pg_readonly`](/pg_readonly) [`safeupdate`](/safeupdate) [`pg_permissions`](/pg_permissions) [`pgautofailover`](/pgautofailover) [`pg_catcheck`](/pg_catcheck) [`pre_prepare`](/pre_prepare) [`pgcozy`](/pgcozy) [`pg_orphaned`](/pg_orphaned) [`pg_crash`](/pg_crash) [`pg_cheat_funcs`](/pg_cheat_funcs) [`pg_savior`](/pg_savior) [`table_log`](/table_log) [`pg_fio`](/pg_fio) [`pgpool_adm`](/pgpool_adm) [`pgpool_recovery`](/pgpool_recovery) [`pgpool_regclass`](/pgpool_regclass) [`pgagent`](/pgagent) [`vacuumlo`](/vacuumlo) [`pg_prewarm`](/pg_prewarm) [`oid2name`](/oid2name) [`lo`](/lo) [`basic_archive`](/basic_archive) [`basebackup_to_shell`](/basebackup_to_shell) [`old_snapshot`](/old_snapshot) [`adminpack`](/adminpack) [`amcheck`](/amcheck) [`pg_surgery`](/pg_surgery)
[**STAT**](/stat): [`pg_profile`](/pg_profile) [`pg_show_plans`](/pg_show_plans) [`pg_stat_kcache`](/pg_stat_kcache) [`pg_stat_monitor`](/pg_stat_monitor) [`pg_qualstats`](/pg_qualstats) [`pg_store_plans`](/pg_store_plans) [`pg_track_settings`](/pg_track_settings) [`pg_wait_sampling`](/pg_wait_sampling) [`system_stats`](/system_stats) [`meta`](/meta) [`pgnodemx`](/pgnodemx) [`pg_proctab`](/pg_proctab) [`pg_sqlog`](/pg_sqlog) [`bgw_replstatus`](/bgw_replstatus) [`pgmeminfo`](/pgmeminfo) [`toastinfo`](/toastinfo) [`explain_ui`](/explain_ui) [`pg_relusage`](/pg_relusage) [`pg_top`](/pg_top) [`pagevis`](/pagevis) [`powa`](/powa) [`pageinspect`](/pageinspect) [`pgrowlocks`](/pgrowlocks) [`sslinfo`](/sslinfo) [`pg_buffercache`](/pg_buffercache) [`pg_walinspect`](/pg_walinspect) [`pg_freespacemap`](/pg_freespacemap) [`pg_visibility`](/pg_visibility) [`pgstattuple`](/pgstattuple) [`auto_explain`](/auto_explain) [`pg_stat_statements`](/pg_stat_statements)
[**SEC**](/sec): [`passwordcheck_cracklib`](/passwordcheck_cracklib) [`supautils`](/supautils) [`pgsodium`](/pgsodium) [`supabase_vault`](/supabase_vault) [`pg_session_jwt`](/pg_session_jwt) [`anon`](/anon) [`pg_tde`](/pg_tde) [`pgsmcrypto`](/pgsmcrypto) [`pgaudit`](/pgaudit) [`pgauditlogtofile`](/pgauditlogtofile) [`pg_auth_mon`](/pg_auth_mon) [`credcheck`](/credcheck) [`pgcryptokey`](/pgcryptokey) [`pg_jobmon`](/pg_jobmon) [`logerrors`](/logerrors) [`login_hook`](/login_hook) [`set_user`](/set_user) [`pg_snakeoil`](/pg_snakeoil) [`pgextwlist`](/pgextwlist) [`pg_auditor`](/pg_auditor) [`sslutils`](/sslutils) [`noset`](/noset) [`sepgsql`](/sepgsql) [`auth_delay`](/auth_delay) [`pgcrypto`](/pgcrypto) [`passwordcheck`](/passwordcheck)
[**FDW**](/fdw): [`wrappers`](/wrappers) [`multicorn`](/multicorn) [`odbc_fdw`](/odbc_fdw) [`jdbc_fdw`](/jdbc_fdw) [`mysql_fdw`](/mysql_fdw) [`oracle_fdw`](/oracle_fdw) [`tds_fdw`](/tds_fdw) [`db2_fdw`](/db2_fdw) [`sqlite_fdw`](/sqlite_fdw) [`pgbouncer_fdw`](/pgbouncer_fdw) [`mongo_fdw`](/mongo_fdw) [`redis_fdw`](/redis_fdw) [`redis`](/redis) [`kafka_fdw`](/kafka_fdw) [`hdfs_fdw`](/hdfs_fdw) [`firebird_fdw`](/firebird_fdw) [`aws_s3`](/aws_s3) [`log_fdw`](/log_fdw) [`dblink`](/dblink) [`file_fdw`](/file_fdw) [`postgres_fdw`](/postgres_fdw)
[**SIM**](/sim): [`orafce`](/orafce) [`pgtt`](/pgtt) [`session_variable`](/session_variable) [`pg_statement_rollback`](/pg_statement_rollback) [`pg_dbms_metadata`](/pg_dbms_metadata) [`pg_dbms_lock`](/pg_dbms_lock) [`pg_dbms_job`](/pg_dbms_job) [`babelfishpg_common`](/babelfishpg_common) [`babelfishpg_tsql`](/babelfishpg_tsql) [`babelfishpg_tds`](/babelfishpg_tds) [`babelfishpg_money`](/babelfishpg_money) [`pgmemcache`](/pgmemcache)
[**ETL**](/etl): [`pglogical`](/pglogical) [`pglogical_origin`](/pglogical_origin) [`pglogical_ticker`](/pglogical_ticker) [`pgl_ddl_deploy`](/pgl_ddl_deploy) [`pg_failover_slots`](/pg_failover_slots) [`wal2json`](/wal2json) [`wal2mongo`](/wal2mongo) [`decoderbufs`](/decoderbufs) [`decoder_raw`](/decoder_raw) [`test_decoding`](/test_decoding) [`mimeo`](/mimeo) [`repmgr`](/repmgr) [`pg_fact_loader`](/pg_fact_loader) [`pg_bulkload`](/pg_bulkload)



--------

## 一些感想与体会

PG 每个大版本都会引入一些变动，因此维护一百多个扩展插件并不是一件轻松的事情。特别是一些扩展的作者都好几年没动静了，那还真就只能自己上。我自己修复了十几个扩展插件，提供了最新的 PG 大版本支持。能联系上作者的，我也提交了一堆 PR 或者 Issue，推动解决。

<a href="https://github.com/Vonng"><img src="github-contrib.png" style="max-width: 800px; width: 100%; height: auto;"></a>

在这个过程中，我和许多扩展作者都建立了联系。例如，我手把手帮助 ParadeDB 的老板与作者 [解决了](https://github.com/paradedb/paradedb/issues/1116) RPM / DEB 包打包与分发的问题。我说动了 duckdb_fdw 的作者使用一个单独的 libduckdb，并发布了 v1.0.0 ，我给一些PG扩展的作者发邮件/Issue，国产机器学习框架 PG4ML 的作者也找到了我希望能够通过这个渠道进行分发。

再比如说，最近 PG 生态 OLAP 缝合 DuckDB 的竞赛如火如荼，但不管是ParadeDB 的 pg_analytics，国内个人开发者李红艳编写的 duckdb_fdw，CrunchyData 的 pg_parquet，MooncakeLab 的 pg_mooncake， Hydra 和 DuckDB 原厂 MotherDuck 亲自下场搞的 pg_duckdb ，都被我在第一时间编译打包收录整合其中，做到了 —— 你卷你的，反正我全都要。

言归正传，**我希望这个仓库能设立起 PostgreSQL 扩展安装分发的标准，解决让人头大的分发难题**。目前最让我感到高兴的进展是，流行的开源 PostgreSQL高可用集群搭建项目 [`postgresql_cluster`](https://postgresql-cluster.org/) 的作者 Vitaliy Kukharik 已经将这个仓库作为默认启用的仓库来安装 PostgreSQL 扩展。

<a href="https://x.com/VKukharik/status/1853012121623155117"><img src="pg-clusters.png" style="max-width: 800px; width: 100%; height: auto;"></a>


目前这个仓库 (repo.pigsty.io) 托管在 Cloudflare 上，所以没有什么流量成本。国内有一个镜像站点 repo.pigsty.cc，方便墙内用户使用，每个有小几百块流量费，不是什么大问题。两个仓库加起来，过去一个月的下载流量大概 200GB ，考虑到扩展平均几十KB到几MB的大小，总下载量小几十万是有了。

因为[赛博菩萨 Cloudflare ](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247487240&idx=1&sn=ba535fd0c1026bc2482ea6ad1e1fb8bf&chksm=fe4b3ad3c93cb3c50bfeaed64963cce25c49bee80364d3a8ca78b87d7c9f19fd4d79d3c62ddc&scene=21#wechat_redirect)不收流量费，所以总的来说，我觉得做一个永久免费的声明与承诺并不困难，所以 So be it。我承诺这个仓库将持续维护并永久免费。如果有国内开源软件站点的朋友愿意赞助或提供镜像服务，欢迎联系我。

我相信我的工作可以帮助到全球PG用户，并对 PostgreSQL 生态的繁荣贡献一份力量。我也希望我的工作可以帮到您，**Enjoy PostgreSQL**！