---
title: "504 Extensions: Expand the PostgreSQL Landscape"
date: 2026-04-13
author: Ruohang Feng
summary: >
  One GitHub issue turned into an extension sprint. 32 new additions, 504 in total, say a lot about where PostgreSQL is headed.
tags: [PostgreSQL, Ecosystem, Extensions]
---

One GitHub issue turned into an extension sprint. Thirty-two new additions say a lot about where PostgreSQL is headed. With 504 extensions in the catalog, how far can this ecosystem go?


--------

## It Started with a Chemistry Extension

Two days ago, a user opened a GitHub [issue](https://github.com/pgsty/pigsty/issues/738): he was using RDKit, the de facto standard library in cheminformatics, to store molecular structures, run substructure searches, and compute similarity inside PostgreSQL.
He noticed that the official PGDG package was built without InChI support. After spending a while rebuilding it with the right compile flags, he got it working, but still hoped Pigsty could support it out of the box.

[![rdkit1-en.webp](rdkit1-en.webp)](https://github.com/pgsty/pigsty/issues/738)

RDKit really is a nasty one. I tried to bring it into the Pigsty extension repo about two years ago, porting it from Debian to EL.
The dependency tree was ugly: Boost, Eigen, RapidJSON, Cairo, plus optional modules like InChI and Avalon.
Each one came with its own build flags and OS-specific library-version problems.
I fought with it for a while, got nowhere, and shelved it.

This time was different. **I had coding agents.**

Using Codex or Claude Code for this kind of build-system archaeology is almost unfair.
Things that used to take endless rounds of trial and error now usually take one or two iterations of prompting and then waiting.
This release also fixed the missing InChI support in the PGDG package. In practice it came down to enabling one more build flag and bundling the InChI source. It worked on the first proper pass, and the user was happy.

![rdkit2-en.webp](rdkit2-en.webp)

Honestly, feedback like that is the best part of doing open source.


---------

## Strike While the Iron Is Hot

Once I was warmed up, I went after a few other long-standing problem cases.

**plv8**: PostgreSQL bindings for the V8 engine. It had refused to build on EL10 for a while. This time, after carrying a few patches, I finally got it building reliably.

**duckdb_fdw**: lets PostgreSQL read and write external DuckDB files. Previously it clashed with DuckDB's official `pg_duckdb` extension because both wanted the same shared library name, so I had to hide it temporarily. This time I turned `duckdb_fdw` into a sub-extension of `pg_duckdb`, so they share the same `libduckdb`. The conflict is gone, and both can coexist cleanly again.

At that point I figured: if the toolchain is already hot, why not finish the rest of the worthwhile extensions in the PostgreSQL ecosystem that had been sitting on the backlog?
That turned into this release: **32 new additions, 22 updates, and the Pigsty extension repo officially crossing 500, landing at 504 total extensions**.

> [Extension Catalog: pigsty.cc/ext](https://pigsty.cc/ext)

| **Category** | **All** | **PGDG** | **PIGSTY** | **CONTRIB** | **MISS** | **PG18** | **PG17** | **PG16** | **PG15** | **PG14** |
|:-------------|--------:|---------:|-----------:|------------:|---------:|---------:|---------:|---------:|---------:|---------:|
| **Total**    |     504 |      155 |        332 |          71 |        0 |      481 |      488 |      479 |      473 |      457 |
| **EL**       |     499 |      150 |        332 |          71 |        5 |      472 |      482 |      474 |      468 |      452 |
| **Debian**   |     489 |      107 |        311 |          71 |       15 |      466 |      474 |      464 |      458 |      442 |

Out of these 500-odd extensions, around 70 ship with PostgreSQL itself, roughly 150 are packaged by PGDG, and the remaining 330 are third-party extensions that I package and maintain myself.

To put that in perspective: most managed PostgreSQL cloud RDS expose a few dozen extensions at best.
Take Supabase, for example. It looks like a long list, but after you subtract the 35 contrib extensions that come with PostgreSQL, you are left with fewer than 30 third-party extensions.


------

## The New Extensions

This batch is pretty hardcore. Broadly, it falls into four groups:

**Data-domain extensions**: make chemical molecules, RDF triples, BSON, Protobuf, recurring schedules, and other complex objects first-class database citizens.

**Query extensions**: sparse linear algebra and graph algorithms, Datalog-style graph queries, full-text search, hybrid ranking fusion, recursive SQL template engines.

**Production engineering extensions**: deep observability, exported query telemetry, CDC to MQTT, COPY interception, DDL propagation for logical replication, lightweight distributed locks, soft-alert data quality management.

**Developer-experience extensions**: session variables, pseudo-autonomous transaction logging, natural-language time parsing.

Taken together, they point to a broader trend: PostgreSQL's extension layer is pushing the database toward the space between an application platform and a data platform. A lot of things that used to require separate services can now be handled inside a single SQL transaction boundary.

That is what extreme extensibility looks like in practice.


--------

# A Tour of the New Additions

This release adds 32 new extensions. The summaries below were compiled with help from Claude, Codex, and Gemini to give readers a quick way to understand what each one does, how it works, and where it fits.


-------

## 1. rdkit: Cheminformatics Inside PostgreSQL

RDKit is the de facto standard open-source library in cheminformatics. It was started by Greg Landrum, originally at Novartis and now at T5 Informatics. Its PostgreSQL cartridge brings molecular structure storage, substructure search, and similarity computation directly into a relational database. For pharmaceutical companies and chemistry labs, that means millions of compounds can be queried with standard SQL instead of a separate toolchain.

The cartridge adds two core data types, **`mol`** for molecules and **`qmol`** for query molecules expressed as SMARTS patterns, plus `bfp` and `sfp` for bit and sparse fingerprints. The main operators are `@>` for substructure matching, `%` for Tanimoto similarity, and `<%>` as a distance operator. All of them can be accelerated with **GiST indexes**. Internally the index uses fingerprint-based filtering for a fast first pass and then falls back to exact matching. Key functions include `mol_from_smiles()`, `morganbv_fp()` for Morgan fingerprints, and `tanimoto_sml()`. GUCs such as `rdkit.tanimoto_threshold` control match sensitivity.

Using the ChEMBL dataset with 1.87 million compounds as an example:

```sql
-- Substructure search: find molecules containing a given scaffold
SELECT count(*) FROM rdk.mols WHERE m @> 'c1cccc2c1nncc2';
-- Result: 461 matches, about 108 ms

-- Tanimoto similarity search using Morgan fingerprints
SELECT molregno, tanimoto_sml(morganbv_fp(mol_from_smiles('c1ccccc1C(=O)NC'::cstring)), mfp2) AS similarity
FROM rdk.fps JOIN rdk.mols USING (molregno)
WHERE morganbv_fp(mol_from_smiles('c1ccccc1C(=O)NC'::cstring)) % mfp2
ORDER BY morganbv_fp(mol_from_smiles('c1ccccc1C(=O)NC'::cstring)) <%> mfp2;

-- SMARTS pattern matching: oxadiazole or thiadiazole compounds
SELECT * FROM rdk.mols WHERE m @> 'c1[o,s]ncn1'::qmol LIMIT 500;
```

The obvious use cases are drug discovery workflows: **lead scaffold search** across million-scale compound libraries, **SAR analysis** via similarity search, **compound registration systems** that use fingerprints for duplicate detection, and **commercial catalog search** over datasets such as eMolecules with 6 million-plus compounds.

In practice, the important question is not whether RDKit can compute the answer, but whether it can be indexed and whether the planner can use those indexes effectively. You want to settle index strategy and query templates early. Otherwise it is easy to write filters that are correct but slow. On a 1.87 million-compound dataset, substructure queries range from roughly 88 ms to 1.9 s. With tuning, it can handle datasets at **6 million-plus compounds**. BSD licensed. Docker images such as `mcs07/postgres-rdkit` and conda packages are already available.


-------

## 2. provsql: Semiring Provenance for Query Results

ProvSQL was developed by Pierre Senellart at ENS Paris and the INRIA Valda team, and published at VLDB 2018. It adds **(m-)semiring provenance** and uncertainty management to PostgreSQL. In plain terms, it tracks which base tuples each query result was derived from and lets you evaluate that provenance under different algebraic structures such as booleans, security levels, counts, or probabilities.

Under the hood it uses PostgreSQL hooks to intercept query execution and automatically adds a hidden `provsql` column to each table. That column stores a UUID pointing to a provenance circuit. The supported SQL subset is surprisingly broad: SELECT-FROM-WHERE, JOIN, GROUP BY, DISTINCT, UNION/EXCEPT, aggregates, HAVING, and on PG 14+ even provenance for INSERT, DELETE, and UPDATE. Core functions include `add_provenance()` to enable tracking, `provenance_evaluate()` to evaluate provenance, `formula()` to render boolean formulas, and `probability_evaluate()` to compute result probabilities. Probability evaluation supports multiple algorithms, from naive evaluation to Monte Carlo sampling to d-DNNF compilation with external solvers such as `d4` and `c2d`.

```sql
-- Security-level propagation: results inherit the highest source classification
SELECT create_provenance_mapping('personnel_level', 'personnel', 'classification');
SELECT p1.city, security(provenance(), 'personnel_level')
FROM personnel p1, personnel p2
WHERE p1.city = p2.city AND p1.id < p2.id
GROUP BY p1.city ORDER BY p1.city;

-- Boolean-formula provenance: show the derivation formula for each row
SELECT *, formula(provenance(), 'witness_mapping') FROM s;

-- Probabilistic queries: compute confidence for each result row
SELECT city, probability_evaluate(provenance()) FROM result;
```

ProvSQL fits four common scenarios: **security-label propagation**, where query results inherit the highest classification from source data; **probabilistic databases**, where base tuples come with confidence scores; **data lineage and audit**, where each output row must be traced back precisely and optionally exported as PROV-XML; and **credibility scoring**, for example in investigative workflows where witness statements have different reliability.

The main value here is composability. Provenance is not emitted as a dead log string, but as an object you can keep computing on. It makes sense on critical paths such as core reports, feature pipelines, or compliance calculations, not as something you switch on indiscriminately for the whole database. Implemented in C/C++ with Boost. Provenance circuits live in shared memory. Supports PG 10-18. MIT licensed.


-------

## 3. onesparse: Billion-Edge Graph Algorithms in SQL

OneSparse brings high-performance sparse linear algebra into PostgreSQL by wrapping SuiteSparse:GraphBLAS. Its developer, Michel Pelletier, is a member of the GraphBLAS C API committee, and the advisory team includes SuiteSparse author Timothy A. Davis. The core idea is simple: **represent graphs as sparse matrices**, then use matrix operations to implement BFS, PageRank, triangle centrality, and related graph algorithms, all from SQL.

The extension introduces data types such as `matrix`, `vector`, `scalar`, `semiring`, and `monoid`, plus operators like `@` for matrix multiplication under the `plus_times` semiring. It ships graph algorithms from LAGraph, including BFS in both level and parent modes, PageRank, triangle centrality, degree centrality, and single-source shortest path. Internally it wraps GraphBLAS opaque handles inside PostgreSQL's Expanded Object Header. Small graphs under 1 GB can live in TOAST; larger ones can be stored as Large Objects or on the filesystem. There is also a built-in JIT compiler with **NVIDIA CUDA GPU acceleration**.

```sql
-- Load a graph from a Matrix Market file
SELECT mmread('/home/postgres/onesparse/demo/karate.mtx') AS graph;

-- BFS traversal
SELECT (bfs(graph, 1)).level FROM karate;

-- Degree centrality by column reduction
SELECT reduce_cols(cast_to(graph, 'int32')) AS degree FROM karate;

-- PageRank
SELECT pagerank(graph) FROM karate;
```

On the GAP benchmark, BFS over a **4.3 billion-edge** graph reached **70+ billion traversed edges per second** on a 48-core AMD EPYC server. Natural targets include fraud detection on transaction graphs, social-network analysis, and Graph RAG workloads. The caveat is the usual one: whether it is actually usable depends on whether your load and serialization formats fit the rest of your pipeline, and whether the operators behave well with the SQL planner and parallel execution. Best approach: get a small end-to-end path working first.

OneSparse currently requires **PG 18 Beta or newer** and is still in alpha. Apache 2.0 licensed.


-------

## 4. pg_datasentinel: Deep Observability for PostgreSQL in the Container Era

`pg_datasentinel` was developed by Christophe Reveillere at Datasentinel and hit 1.0 on April 10, 2026. It adds four observability capabilities that fill real gaps in PostgreSQL's native views, especially for containerized deployments and operational alerting.

First, **extended activity monitoring**: it augments `pg_stat_activity` with per-backend memory usage, live temp-file bytes, and on PG 18+ the current plan ID. Second, **container resource visibility**: it reports CPU quotas, memory limits, current memory usage, and CPU pressure for Docker, Kubernetes, OpenShift, or any cgroup-managed environment. Third, **transaction wraparound forecasting**: it tracks XID and MXID burn rate and exposes live ETAs to aggressive vacuum and wraparound limits. Fourth, **log capture views**: it parses vacuum, analyze, temp-file, and checkpoint events into a structured shared-memory ring buffer that can be queried from SQL in real time.

```sql
-- Per-backend memory usage (extended pg_stat_activity)
SELECT pid, usename, query, backend_memory_bytes, temp_file_bytes
FROM pg_datasentinel_activity;

-- Container resource monitoring
SELECT cpu_quota, memory_limit, memory_usage, cpu_pressure
FROM pg_datasentinel_container_resources;

-- Wraparound risk forecasting
SELECT xid_current, xid_limit, xid_eta_aggressive_vacuum, xid_eta_wraparound
FROM pg_datasentinel_wraparound;
```

If you run PostgreSQL on Kubernetes, this gives you container-level visibility without shipping a separate monitoring agent. The **XID wraparound warning** is especially useful operationally. Everyone knows wraparound can take a database down hard; `pg_datasentinel` turns that from a firefight into something you can see coming. 3-Clause BSD. Requires PG 15+.


-------

## 5. datasketches: Approximate Analytics at Hundred-Million-Row Scale

Apache DataSketches is an Apache Foundation project that started at Yahoo and Verizon Media. Its PostgreSQL extension brings a family of **approximate query data structures, or sketches**, into SQL. The problem it solves is straightforward: exact `COUNT(DISTINCT)`, quantiles, and heavy-hitter analysis get expensive fast on large datasets.

The extension exposes seven sketch types: **`cpc_sketch`** for compressed probabilistic counting, **`hll_sketch`** for HyperLogLog, **`theta_sketch`** for distinct counting with set algebra, `aod_sketch` for tuple sketches, **`kll_float_sketch`** and **`kll_double_sketch`** for quantiles, `req_float_sketch` for high-accuracy tail quantiles, and `frequent_strings_sketch` for frequent items. Each comes with the usual build, union, and estimate API shape, such as `*_sketch_build()`, `*_sketch_union()`, and `*_sketch_get_estimate()`.

The important point is not that a function returns an estimate. It is that sketches are **serializable objects that can be merged**, which makes them perfect for cube-like approximate metrics. You can pre-aggregate sketches by dimension slice and then union them at query time for arbitrary distinct counts. In-memory footprint is **sublinear**, and the binary format is compatible across Java, C++, Python, Rust, and Go.

```sql
-- Approximate distinct count: about 6x faster than exact COUNT(DISTINCT)
SELECT cpc_sketch_distinct(id) FROM random_ints_100m;
-- Result: 63423695 (exact: 63208457), about 20 s vs about 2 min exact

-- Theta Sketch set algebra: intersection of two user cohorts
SELECT theta_sketch_get_estimate(
  theta_sketch_intersection(sketch1, sketch2)
) FROM theta_set_op_test;

-- KLL quantiles: median
SELECT kll_float_sketch_get_quantile(sketch, 0.5) FROM kll_float_sketch_test;

-- Multidimensional aggregation with sketch union
SELECT cpc_sketch_get_estimate(cpc_sketch_union(respondents_sketch)) AS num_respondents, flavor
FROM (
  SELECT cpc_sketch_build(respondent) AS respondents_sketch, flavor, country
  FROM (VALUES (1,'Vanilla','CH'),(1,'Chocolate','CH'),
               (2,'Chocolate','US'),(2,'Strawberry','US')) AS t(respondent, flavor, country)
  GROUP BY flavor, country
) bar GROUP BY flavor;
```

Typical use cases: **real-time UV counting** without storing raw user IDs, **distribution analysis** such as p50/p95/p99 latency over billions of events, and **audience overlap** with Theta Sketch intersections like "saw ad A and visited site B". On a 100 million-row dataset, CPC distinct counting finishes in about 20 seconds versus about 2 minutes for exact `COUNT(DISTINCT)`, with single-digit percentage relative error.


-------

## 6. pghydro: Drainage-Network Analysis from Brazil's National Water Agency

PgHydro was developed by Alexandre de Amorim Teixeira, a GIS specialist at Brazil's National Water and Sanitation Agency (ANA). Built on top of PostGIS, it is used as ANA's official tool for hydrology workflows across the country and was also presented at FOSS4G 2022.

Its capabilities cover the full hydrological network workflow: importing raw GIS data, validating topological consistency, computing flow direction, assigning **Otto Pfafstetter basin codes**, running upstream and downstream analysis, calculating catchment area, and computing Strahler stream order. The architecture is modular, with five sub-extensions: `pghydro` as the core, `pgh_raster` for DEM raster work, `pgh_hgm` for hydrogeomorphology, `pgh_consistency` for topological validation, and `pgh_output` for exports.

```sql
-- Import drainage-line data
SELECT pghydro.pghfn_input_data_drainage_line('public', 'input_drainage_line', 'geom', 'nome');

-- Compute flow direction and reverse inconsistent segments
SELECT pghydro.pghfn_CalculateFlowDirection();
SELECT pghydro.pghfn_ReverseDrainageLine();

-- Compute Pfafstetter basin codes
SELECT pghydro.pghfn_Calculate_Pfafstetter_Codification();

-- Compute upstream catchment area and distance to sea
SELECT pghydro.pghfn_CalculateUpstreamArea();
SELECT pghydro.pghfn_CalculateDistanceToSea(0);

-- Strahler stream order
SELECT pghydro.pghfn_calculatestrahlernumber();
```

It fits national-scale hydrology databases, basin planning and coding, upstream/downstream pollution impact analysis, and drainage-network topology validation. The right mental model is not "one extension with some GIS functions" but "a domain-specific ETL and analysis pipeline inside the database." Raw terrain and river-network data live in PostGIS, the processing chain is automated in SQL, and recomputing after source updates is much more reliable than ad hoc scripts. There is also a QGIS plugin, PgHydroTools, for visual interaction. Written entirely in PL/pgSQL. GPLv2.


-------

## 7. pg_stat_ch: PostgreSQL Query Telemetry, Exported to ClickHouse

`pg_stat_ch` is an open-source extension from ClickHouse, released during its February 2025 "Postgres Week at ClickHouse" event. The author is Kaushik Iska. Unlike `pg_stat_statements`, which aggregates statistics inside PostgreSQL, `pg_stat_ch` streams **every raw query execution event** out to ClickHouse. Each event has 45 fields and a fixed size of 4.6 KB. The idea is to let ClickHouse handle p50/p95/p99, top-query analysis, and error analytics on the raw stream.

The pipeline looks like this: **PostgreSQL hooks in foreground backends -> shared-memory ring buffer -> background worker -> ClickHouse**. The 45 fields cover query timing, row counts, buffer usage, WAL usage, CPU time, JIT metrics on PG 15+, parallel-worker stats on PG 18+, client context such as app name and IP, and error capture including SQLSTATE. It uses ClickHouse's native binary protocol with **LZ4 compression** and statically links `clickhouse-cpp`. To avoid backpressure on PostgreSQL, it drops events when the queue overflows and increments a drop counter instead of slowing the database down, very much in the spirit of StatsD.

```sql
-- PostgreSQL side: monitor extension health
SELECT * FROM pg_stat_ch_stats();
-- Returns enqueue/export/drop counters plus last success/failure timestamps

-- ClickHouse side: p95/p99 by app over the last hour
SELECT query_id, count() AS calls,
       quantile(0.95)(duration_us) / 1000 AS p95_ms,
       quantile(0.99)(duration_us) / 1000 AS p99_ms
FROM pg_stat_ch.events_raw
WHERE app = 'myapp' AND ts_start > now() - INTERVAL 1 HOUR
GROUP BY query_id ORDER BY p99_ms DESC LIMIT 10;
```

On the ClickHouse side it ships four materialized views: `events_recent_1h` for a rolling one-hour copy, `query_stats_5m` for five-minute buckets with TDigest quantiles, `db_app_user_1m` for database/app/user load attribution, and `errors_recent` for a rolling seven-day error window.

The performance numbers are impressive: **about 5 microseconds p99 overhead per query**. In a pgbench run at 36.6K TPS with 32 clients, it captured 7.7 million events in 30 seconds with zero drops and **less than 1% TPS impact** versus baseline. The design minimizes lock contention in three layers: atomic overflow checks, non-blocking `LWLock` attempts, and per-backend local buffers flushed per transaction, cutting lock acquisitions by about 5x. This is a good division of labor: PostgreSQL as the transaction system, ClickHouse as the telemetry warehouse. Much more robust than trying to reconstruct the same thing from log files. Supports PG 16-18. Apache 2.0.


-------

## 8. pg_rrf: Rank Fusion for Hybrid Search in One Function

`pg_rrf` was developed by the Japanese developer yuiseki and released in January 2026. It is written in Rust with `pgrx`. What it does is package **Reciprocal Rank Fusion (RRF)** as a native PostgreSQL function, which neatly solves the annoying engineering problem in hybrid retrieval where different retrievers output scores on incomparable scales. RRF avoids that by using rank only:

`score(d) = Σ 1 / (k + rank_i(d))`

The default `k` is 60, following Cormack et al., SIGIR 2009.

The extension exposes four functions: `rrf(rank_a, rank_b, k)` for two-way fusion, `rrf3()` for three-way fusion, `rrfn(ranks[], k)` for N-way fusion, and the most useful one in practice, **`rrf_fuse(ids_a bigint[], ids_b bigint[], k)`**, which takes two ranked ID arrays and returns a fused `(id, score)` table. It is NULL-safe: an ID that appears in only one list is scored from that list alone.

```sql
-- Hybrid retrieval with pg_rrf: pgvector + BM25
WITH fused AS (
  SELECT * FROM rrf_fuse(
    ARRAY(SELECT id FROM docs ORDER BY bm25_score DESC LIMIT 100),
    ARRAY(SELECT id FROM docs ORDER BY embedding <=> :qvec LIMIT 100),
    60
  )
)
SELECT d.*, fused.score
FROM fused JOIN docs d USING (id)
ORDER BY fused.score DESC LIMIT 20;
```

That replaces 20-plus lines of `FULL OUTER JOIN`, `COALESCE`, and hand-rolled score math with a single function call. Good fit for **RAG hybrid retrieval**, product search, and any document-ranking pipeline that combines multiple signals. Keeping the fusion step in the database also helps when the fused result still needs to join business tables. Current version is `v0.0.3`. MIT licensed.


-------

## 9. pg_kazsearch: Kazakh Full-Text Search, from Zero to One

`pg_kazsearch` is the first PostgreSQL full-text-search extension for Kazakh. Kazakh is a highly agglutinative language. A single word such as `мектептерімізде` can encode plurality, possession, and locative suffixes, and you have to strip all of that to get back to the root `мектеп`. Existing PostgreSQL and Elasticsearch analyzers do not handle this well.

The extension is written in Rust with `pgrx`. It provides a `kazakh_cfg` text-search configuration and a `pg_kazsearch_dict` dictionary. Stemming uses **BFS suffix stripping**, combined with vowel-harmony checks and a **21,863-root POS-tagged lexicon** derived from Apertium-kaz to avoid over-stemming. Runtime behavior can be tuned with `ALTER TEXT SEARCH DICTIONARY`.

```sql
-- Stemming
SELECT ts_lexize('pg_kazsearch_dict', 'алмаларымыздағы');
-- {алма}

-- Weighted tsvector construction and search
SELECT title FROM articles
WHERE fts @@ websearch_to_tsquery('kazakh_cfg', 'президенттің жарлығы')
ORDER BY ts_rank_cd(fts, websearch_to_tsquery('kazakh_cfg', 'президенттің жарлығы')) DESC
LIMIT 10;
```

Benchmarks on 2,999 articles show **0.5 ms** query latency, about 2.8x faster than `pg_trgm`, with a 25% gain in nDCG@10 and a 23% gain in Recall@10. That makes it useful for Kazakh-language news and government-document search, e-commerce search, and multilingual systems that want a real search stack for low-resource languages instead of falling back to crude trigram matching.


-------

## 10. pg_liquid: Datalog-Style Graph Queries

`pg_liquid` was developed by Michael Golfi. It brings Liquid/Datalog-style declarative graph queries into PostgreSQL. With `liquid.query(...)`, you can declare facts, define rules, and execute a terminal query in one call instead of standing up a separate graph database. Rules are local to a single `liquid.query` invocation. It supports fact assertions, **recursive transitive closure**, compound queries, and row normalizers.

```sql
SELECT target
FROM liquid.query($$
  Edge("a", "path", "b").
  Edge("b", "path", "c").
  Edge("c", "path", "d").

  Reach(x, y) :- Edge(x, "path", y).
  Reach(x, z) :- Reach(x, y), Reach(y, z).

  Reach("a", target)?
$$) AS t(target text)
ORDER BY 1;
```

It can also combine ontology predicate definitions such as `DefPred` with compounds like `OntologyClaim@(...)`, letting compounds carry provenance or confidence while rules implement subclass closure and similar inference. Good fit for knowledge-graph queries, hierarchical traversal such as org charts and taxonomy trees, and rule-based business logic when you do not want a separate graph engine. Implemented entirely in PL/pgSQL with no external dependencies. Still early-stage.

-------

## 11. logical_ddl: Logical Replication, but for DDL Too

PostgreSQL logical replication handles DML only. It does not replicate DDL such as `ALTER TABLE`, which is a real operational pain point because schema drift can break replication outright. `logical_ddl`, developed by Samed Yildirim, uses **event triggers** to intercept DDL, deparse it, store it in a table, and let logical replication carry it to subscribers, where equivalent SQL is generated and executed.

Supported DDL includes `ALTER TABLE RENAME TO`, `RENAME COLUMN`, `ADD COLUMN`, `ALTER COLUMN TYPE`, and `DROP COLUMN`. On the type side, built-in types, arrays, composite types, domains, and enums are usable, but replication of the **type definitions themselves** such as `CREATE TYPE` is out of scope. The `logical_ddl.publish_tablelist` table lets you control capture at per-table and per-command granularity.

```sql
-- Publisher-side config
INSERT INTO logical_ddl.settings (publish, source) VALUES (true, 'publisher1');

-- Track DDL for every table already in logical replication
INSERT INTO logical_ddl.publish_tablelist (relid)
SELECT prrelid FROM pg_catalog.pg_publication_rel;

-- Restrict captured DDL types per table
INSERT INTO logical_ddl.publish_tablelist (relid, cmd_list)
VALUES ('my_table'::regclass, ARRAY['ADD COLUMN', 'DROP COLUMN']);
```

This is useful for automated DDL sync in logical-replication setups, zero-downtime migrations, and multi-datacenter PostgreSQL topologies. The nice thing about the design is that DDL propagation becomes an auditable data flow instead of a side process people have to remember to run. MIT licensed. Available on PGXN. Constraints, indexes, and defaults are not implemented yet.


-------

## 12. rdf_fdw: Query the Semantic Web with SQL

`rdf_fdw`, developed by Jim Jones, is a foreign data wrapper for RDF triple stores behind SPARQL endpoints. It is basically a bridge between the relational SQL world and the semantic-web / linked-data world. The extension adds an `rdfnode` type for RDF terms such as IRIs, language tags, and typed literals. It supports **SQL-to-SPARQL pushdown** for `WHERE`, `LIMIT`, `ORDER BY`, and `DISTINCT`, and can also send `INSERT`, `UPDATE`, and `DELETE` through SPARQL UPDATE endpoints.

```sql
-- Create a foreign server backed by DBpedia
CREATE SERVER dbpedia
  FOREIGN DATA WRAPPER rdf_fdw
  OPTIONS (endpoint 'https://dbpedia.org/sparql');

-- Define a foreign table mapped to a SPARQL query
CREATE FOREIGN TABLE dbpedia_query (
    p rdfnode OPTIONS (variable '?p'),
    o rdfnode OPTIONS (variable '?o')
) SERVER dbpedia OPTIONS (
    sparql 'SELECT ?p ?o WHERE {<http://dbpedia.org/resource/Berlin> ?p ?o}'
);

-- Query RDF data with plain SQL
SELECT * FROM dbpedia_query WHERE o = 'some_value' LIMIT 10;
```

The `rdf_fdw_clone_table()` stored procedure can clone foreign-table data into local tables in batches. One implementation detail to watch: fetched data is loaded into memory before conversion, so large result sets need a careful look at pushdown effectiveness and memory usage. Good fit for linked-data integration with DBpedia or Wikidata and for using standard SQL and BI tooling on top of SPARQL endpoints. MIT licensed. Supports PG 9.5-18.


-------

## 13. pgbson: A More Exact Binary Document Type than JSONB

`pgbson`, also known as `postgresbson`, was developed by buzzm. It adds a native **BSON** type to PostgreSQL. Compared with JSON, BSON has first-class `datetime`, `decimal128`, `int32`, `int64`, `binary`, and related types, which matters when data moves across distributed systems and you care about exact round-tripping. The promise here is **binary-perfect BSON in, BSON out**.

The API has two access styles. The first is the fast one: **dotpath functions** such as `bson_get_string(bson, 'd.recordId')`, `bson_get_datetime()`, and `bson_get_decimal128()`, which walk the binary structure directly and allocate memory only at the leaf. The second is the JSON-like operator style using `->` and `->>`, but that constructs intermediate subdocuments at each step and gets expensive on deep paths. Combined with B-tree and HASH indexes, expression indexes on the function API can yield **10,000x** speedups over sequential scan in the right cases. Input also accepts EJSON.

```sql
-- Insert an EJSON document with rich types
INSERT INTO data_collection (data) VALUES (
   '{"d":{"recordId":"R1","amt":{"$numberDecimal":"77777809838.97"},
          "ts":{"$date":"2022-03-03T12:13:14.789Z"}}}');

-- Expression index + dotpath query (recommended)
CREATE INDEX ON data_collection(bson_get_string(data, 'd.recordId'));
SELECT bson_get_decimal128(data, 'd.amt')
FROM data_collection WHERE bson_get_string(data, 'd.recordId') = 'R1';

-- Arrow-chain access (slower on deep paths)
SELECT (data->'d'->'amt'->>'$numberDecimal')::numeric FROM data_collection;
```

Typical use cases include cross-language event and document pipelines that need exact type preservation, financial data where `decimal128` matters, and digital-signature workflows that rely on BSON's deterministic binary representation. MIT licensed. Supports PG 14-18.


-------

## 14. pg_when: Describe Time in Natural Language

`pg_when`, developed by frectonz, parses natural-language time expressions into PostgreSQL `timestamptz` values or Unix epochs. The main function, `when_is(text)`, returns a normalized timestamp. The grammar is built around date + `at` + time + `in` + time zone. If no time zone is specified, it defaults to UTC.

```sql
SELECT when_is('5 days ago at this hour in Asia/Tokyo');
SELECT when_is('next friday at 8:00 pm in America/New_York');
SELECT when_is('in 2 months at midnight in UTC-8');
SELECT when_is('December 31, 2026 at evening');
```

There are also `seconds_at()`, `millis_at()`, `micros_at()`, and `nanos_at()` for Unix timestamps at different precisions. This is a parser, not a scheduler. It fits operator- or support-facing tools that accept human time input, data backfill and repair scripts where natural language is easier than date math, and general time-zone normalization. MIT licensed.


-------

## 15. pgmqtt: Push Database Changes Straight to MQTT

`pgmqtt`, developed by RayElg in Rust, turns PostgreSQL row changes into MQTT messages and can also map inbound MQTT messages back into tables. This is not a general MQTT client. It is a way to wire **database CDC and a message broker** directly at the database layer, using SQL to define topic mappings and payload templates.

```sql
-- Outbound: table changes -> MQTT topic
SELECT pgmqtt_add_outbound_mapping(
  'public', 'my_table', 'topics/{{ op | lower }}', '{{ columns | tojson }}'
);

-- Inbound: MQTT topic -> table via JSONPath-style mapping
SELECT pgmqtt_add_inbound_mapping(
  'sensor/{site_id}/temperature', 'sensor_readings',
  '{"site_id": "{site_id}", "value": "$.temperature"}'::jsonb
);
```

This is an especially natural fit for IoT systems. You can push database state changes out to edge devices without an extra middleware layer, or ingest sensor readings from MQTT directly into tables. It also works for lightweight event-driven systems that want less application glue code. Elastic License 2.0.


-------

## 16. pg_query_rewrite: Transparent SQL Substitution

`pg_query_rewrite`, developed by Pierre Forstmann, uses the `ProcessUtility` hook to transparently replace SQL statements at runtime. Rules are stored in shared memory and matched by **exact string equality**, which means whitespace and case both matter.

```sql
-- Add a rewrite rule
SELECT pgqr_add_rule('select 10;', 'select 11;');

-- From here on, "select 10;" returns 11
SELECT 10;  -- returns 11

-- Show all rules and rewrite counters
SELECT pgqr_rules();
```

This is a sharp tool. It does not support parameterized statements, the maximum statement length is about 32 KB, matching is whitespace-, semicolon-, and case-sensitive, and rules are not persistent across restarts unless you reload them through startup SQL. Still, it is useful for transparently redirecting fixed SQL emitted by legacy systems during migrations, temporarily intercepting dangerous queries, and doing simple query A/B experiments. Default maximum is 10 rules. Supports PG 9.5-18.


-------

## 17. pgclone: Clone Database Objects with One Function Call

`pgclone`, developed by valehdba and published as version 2.0.0 on PGXN, is refreshingly literal in its scope: instead of `pg_dump` and `pg_restore`, or shell scripts, it lets you call SQL functions to clone tables, schemas, databases, functions, and even roles and privileges from a source instance into a target environment.

It uses the COPY protocol for fast data movement, supports asynchronous operation and progress tracking, selective cloning with row and column filters, and DDL coverage for indexes, constraints, triggers, views, materialized views, sequences, and more. It also includes masking support and automatic discovery of sensitive columns.

```sql
-- Clone a remote table into the local database, including data
SELECT pgclone_table(
  'host=source-server dbname=mydb user=postgres password=secret',
  'public', 'customers', true
);

-- Clone an entire remote database
SELECT pgclone_database(
  'host=source-server dbname=mydb user=postgres password=secret', true
);
```

Good fit for fast dev/test environment provisioning, sanitized production-to-staging clones, and cross-database migration and verification. Compared with `pg_dump`/`pg_restore`, the whole workflow stays inside the database boundary.


-------

## 18. pgproto: Native Protobuf Support

`pgproto`, developed by Apaezmx, adds native Protocol Buffers (`proto3`) storage, query, mutation, and indexing support to PostgreSQL. The core mechanism is **runtime schema registration plus binary traversal**: once a `FileDescriptorSet` is registered in `pb_schemas`, columns of type `protobuf` can expose nested fields through path arrays. It adds `->` field navigation, `#>` nested-path access, `||` message merge, and functions such as `pb_set()`, `pb_insert()`, `pb_delete()`, and `pb_to_json()`.

```sql
-- Extract a nested field
SELECT data #> '{Outer, inner, id}'::text[] FROM items;

-- Partial update, returning a new protobuf value
UPDATE items SET data = pb_set(data, ARRAY['Outer', 'a'], '42');

-- B-tree expression index
CREATE INDEX idx_pb ON items ((data #> '{Outer, inner, id}'::text[]));
```

In a 100,000-row benchmark, `pgproto` used only **16 MB** of storage, versus 46 MB for JSONB and 25 MB for the native relational layout, while full-document retrieval took **5.9 ms** versus 33.1 ms for the relational model that needed multi-table joins. If you want to keep the Protobuf ecosystem for RPC and messaging while still making the data indexable and filterable inside the database, this is compelling. Strong fit for IoT data, microservice event stores, and gRPC-backed data layers. PostgreSQL License.


-------

## 19. pg_fsql: A Recursive SQL Template Engine Driven by JSONB

`pg_fsql`, developed by yurc, turns "SQL template rendering + safe parameterized execution + recursive composition of template trees" into an extension. Templates are organized as dot-path trees. Child templates emit fragments or JSON, which are then injected into parent templates. It supports placeholder syntax such as `{d[key]}` with multiple escaping modes like `!r`, `!j`, and `!i`, optional SPI plan caching per template, and command types including `exec`, `ref`, `if`, `exec_tpl`, `map`, and `NULL`. Public APIs include `fsql.run` for execution, `fsql.render` for dry runs, plus `fsql.tree` and `fsql.explain`. No superuser required.

```sql
-- Define a template
INSERT INTO fsql.templates (path, cmd, body)
VALUES ('user_count','exec',
        'SELECT jsonb_build_object(''total'', count(*)) FROM users WHERE status = {d[status]!r}');

-- Execute a template
SELECT fsql.run('user_count', '{"status":"active"}');

-- Render without executing
SELECT fsql.render('user_count', '{"status":"active"}');
```

This is not "functional SQL" so much as a hierarchical template system for generating SQL from JSON request bodies. It reduces conditional branching in the application layer and fits dynamic report generation, ETL orchestration, multi-tenant query generation, and centralized, permission-controlled SQL templates stored in tables.


-------

## 20. pg_dispatch: Async SQL Dispatch on Top of pg_cron

`pg_dispatch`, developed by Snehil Shah, is an asynchronous task dispatcher and a TLE-compatible alternative to `pg_later`, built on top of `pg_cron`. The main functions are `pgdispatch.fire(command)` for immediate asynchronous execution and `pgdispatch.snooze(command, delay)` for delayed execution. The core use case is to get heavy work out of the foreground transaction. If an `AFTER INSERT` trigger wants to do something expensive, push it into the background instead.

```sql
SELECT pgdispatch.fire('SELECT pg_sleep(40);');
SELECT pgdispatch.snooze('SELECT pg_sleep(20);', '20 seconds');
```

Because it is pure PL/pgSQL and TLE-compatible, it can run in sandboxed environments like Supabase and AWS RDS. Requires `pg_cron >= 1.5`. Good fit for asynchronous side effects inside triggers and functions such as notifications, background rollups, or audit writes that should not hold up the main transaction.


-------

## 21. block_copy_command: Security Hardening by Intercepting COPY

`block_copy_command`, developed by rustwizard in Rust with `pgrx`, intercepts the `COPY` command cluster-wide via the `ProcessUtility` hook. The goal is simple: in compliance-sensitive environments such as PCI-DSS or HIPAA, block data exfiltration through `COPY TO` and block unauthorized bulk imports through `COPY FROM`.

It supports role-based blocklists, directional control via `block_to` and `block_from`, and always blocks `COPY ... TO PROGRAM` for all users by default. The `blocked_roles` list can even include superusers. Audit logging is built in.

```sql
COPY my_table TO STDOUT;     -- non-superuser: ERROR
COPY (SELECT 1) TO PROGRAM 'cat';  -- blocked for everyone by default

-- Audit log
SELECT ts, current_user_name, copy_direction, blocked, block_reason
FROM block_copy_command.audit_log
WHERE ts > now() - interval '1 hour'
ORDER BY ts DESC;
```

This is useful in hosted or multi-tenant environments where you do not want tenants exporting data with `COPY`, in enterprise compliance setups where centralized interception and audit matter, and in ETL environments where import and export privileges need to be tightly separated. The same author also maintains a broader command-firewall extension called `pg_command_fw`.


-------

## 22. pg_isok: Soft Alerts for Data Quality

`pg_isok`, or Isok, was developed by Karl O. Pinc and has been used in production for more than a decade. It is not a traditional constraint or trigger. Think of it as **soft-trigger data integrity management**: you write a SQL query that finds suspicious data patterns, and Isok records, classifies, and defers those findings, reporting only newly introduced problems or changes to previously accepted data. That way you are not forced to re-review the same historical anomalies forever.

```sql
-- A typical Isok rule: customers with no orders
INSERT INTO isok.isok_queries (query) VALUES (
  'SELECT customers.id::text,
          ''Customer '' || customers.id || '' has no related ORDERS'',
          NULL
   FROM customers
   WHERE NOT EXISTS (
     SELECT 1 FROM orders WHERE orders.customerid = customers.id
   )'
);
```

Unlike hard constraints that reject writes, Isok allows questionable data to exist while keeping it under ongoing review. The workflow is organized around tables like `isok_queries` and `isok_results`, plus the `run_isok_queries` function to execute checks. Results can be accepted row by row or deferred. This fits messy-data cleanup pipelines, or business rules that are too fuzzy to encode as hard constraints and still need human judgment. If you can write SQL, you can stand up a workable "alerts + dedupe + deferral" system.

-------

## 23. external_file: Oracle BFILE Semantics for PostgreSQL

`external_file`, maintained by Gilles Darold of HexaCluster Corp, provides the equivalent of Oracle's BFILE feature. It introduces an `EFILE` type that references server-side external files through a directory alias plus file name, and supports reading with `readEfile()`, writing with `writeEfile()`, and copying with `copyEfile()`. Internally it leans on the `lo_*` large-object machinery and uses directory-alias and privilege tables to control the accessible paths.

```sql
-- Register a directory
INSERT INTO directories(directory_name, directory_path) VALUES ('MY_DIR', '/data/files/');

-- Read an external file
SELECT readEfile(efilename('MY_DIR', 'document.pdf'));

-- Write a bytea value out to an external file
SELECT writeEfile(my_bytea_column, efilename('MY_DIR', 'output.bin')) FROM my_table;
```

This was built with Ora2Pg migrations in mind, but it is also useful for legacy systems that keep files outside the database and metadata inside it, or for database-driven batch import and export of external large objects.


-------

## 24. byteamagic: Detect File Types in `bytea`

`byteamagic`, developed by Nico Mandery, wraps `libmagic`, the same library behind the Unix `file` command. It exposes two functions: `byteamagic_mime(bytea)` returns the MIME type, and `byteamagic_text(bytea)` returns a human-readable description.

```sql
SELECT byteamagic_mime(file_data) FROM file_storage WHERE id = 1;
-- 'image/png'

SELECT byteamagic_mime(data) AS mime_type, count(*)
FROM uploads GROUP BY 1 ORDER BY 2 DESC;
```

If you have to store BLOBs in tables, this gives you a way to identify what they actually are from SQL: PDF, PNG, or something else. Good fit for upload governance, real-content-type detection, and cleanup of historical BLOB data.


-------

## 25. pg_text_semver: Native Semantic Versioning

`pg_text_semver`, developed by Rowan Rodrik van der Molen, implements a Semantic Versioning 2.0.0-compliant version type as a `text` domain. Unlike the C-based `semver` extension, it does **not** inherit a 32-bit integer limit for version components.

```sql
SELECT '0.9.3'::semver < '0.11.2'::semver;  -- true (semantic, not lexical, comparison)
SELECT '1.0.0-alpha'::semver < '1.0.0'::semver;  -- true (pre-release < release)
SELECT '8.8.8+bla'::semver = '8.8.8'::semver;  -- true (build metadata ignored)
SELECT semver_parsed('1.0.0-a.1+commit-y');
-- (1, 0, 0, 'a.1', 'commit-y')
```

It is pure SQL, supports min/max aggregation, and can validate PGXN version ranges. Useful for extension and package version management, dependency checks, and version-distribution analytics.


-------

## 26. parray_gin: Substring Matching Indexes for `text[]`

`parray_gin`, developed by Eugene Seliverstov, adds **partial-match** operators for `text[]` columns backed by GIN indexes. Native PostgreSQL array GIN operators only support exact element matching. `parray_gin` adds `@@>` for substring containment, using trigram decomposition under the hood by reusing `pg_trgm`, with recheck for false positives.

```sql
CREATE INDEX ON test_table USING gin (val parray_gin_ops);

-- Match 'post' against 'postgresql'
SELECT * FROM test_table WHERE val @@> array['post'];

-- LIKE-style partial containment
SELECT * FROM test_table WHERE val @@> array['%ar%'];
```

Useful for tag autocomplete and fuzzy tag search, or any case where you want array partial matching to hit an index instead of scanning in application code. Supports PG 9.1-18.


-------

## 27. pg_slug_gen: Cryptographically Secure Timestamp Slugs

`pg_slug_gen`, developed by Fernando Olle, generates short unique identifiers that combine timestamp information with cryptographically secure randomness. It uses `pg_strong_random()` to choose characters. Length determines timestamp precision: 10 characters for seconds, 13 for milliseconds, 16 for microseconds by default, and 19 for nanoseconds.

```sql
SELECT gen_random_slug();      -- microsecond precision
SELECT gen_random_slug(10);    -- second precision
SELECT gen_random_slug(19);    -- nanosecond precision
```

This is not a "slugify the title" URL helper. It is a short, hard-to-guess public identifier. Good fit for invite codes, short links, and public resource IDs where exposing auto-increment sequences is a bad idea, or for distributed writes where timestamp-based uniqueness windows are desirable. Much less predictable than `base62(sequence)`.


-------

## 28. pglock: Lightweight Distributed Locks Inside PostgreSQL

`pglock`, developed by fraruiz, implements a lightweight distributed-lock service on top of PostgreSQL itself. It is built around a lock table and functions such as `pglock.lock`, `pglock.unlock`, `pglock.ttl`, and `pglock.set_serializable`. Locks have TTL expiration, defaulting to 5 minutes, and can optionally be cleaned up on a schedule with `pg_cron` calling `pglock.ttl()`. The recommended isolation level is `SERIALIZABLE` to preserve correct concurrency semantics.

```sql
-- Acquire a lock
SELECT pglock.lock('b3d8a762-3a0e-495b-b6a1-dc8609839f7b', 'users');

-- Release a lock
SELECT pglock.unlock('b3d8a762-3a0e-495b-b6a1-dc8609839f7b', 'users');

-- Reap expired locks
SELECT pglock.ttl();
```

No Redis, ZooKeeper, or other external system required. This fits multi-instance apps competing for jobs or resources, leader election, idempotent consumers, and duplicate-work prevention. The nice part is that lock behavior and business writes stay inside the same database ecosystem. Pure SQL implementation.


-------

## 29. regresql: Language-Agnostic SQL Regression Testing

`regresql`, from boringSQL's Radim Marek, is a **standalone CLI tool**, written in Go, not a PostgreSQL extension. It scans `*.sql` files in a project, executes them, stores output snapshots and `EXPLAIN` plan baselines, and compares future runs against those baselines. It can emit JUnit, GitHub Actions, and pgTAP-style output.

```sql
-- Mark query names with comments in .sql files
-- name: get-user-by-id
SELECT * FROM users WHERE id = :id;

-- name: list-active-users
SELECT * FROM users WHERE active = true;
```

The workflow is built around commands like `discover`, `add`, `update`, `test`, `baseline`, and `snapshot`. This is useful for SQL snapshot testing, catching result drift after migrations or refactors, and recording `EXPLAIN` baselines in CI so you notice plan flips and performance regressions early.


-------

## 30. pgcalendar: Infinite Projection for Recurring Schedules

`pgcalendar`, developed by h4kbas, implements a full recurring-event calendar system. Events are logical entities, schedules define recurrence rules such as daily, weekly, monthly, or yearly patterns, projections generate concrete occurrences, and exceptions let you cancel or reschedule individual instances.

```sql
-- Create an event and a schedule
INSERT INTO pgcalendar.events (name, description, category)
VALUES ('Daily Standup', 'Team standup meeting', 'meeting');

INSERT INTO pgcalendar.schedules (event_id, start_date, end_date, recurrence_type, recurrence_interval)
VALUES (1, '2024-01-01 09:00:00', '2024-12-31 23:59:59', 'daily', 1);

-- Project actual occurrences for a week
SELECT * FROM pgcalendar.get_event_projections(1, '2024-01-01', '2024-01-07');

-- Add an exception: cancel one day
INSERT INTO pgcalendar.exceptions (schedule_id, exception_date, exception_type, notes)
VALUES (1, '2024-01-15', 'cancelled', 'Holiday');

-- Transition to a new schedule definition
SELECT pgcalendar.transition_event_schedule(
  p_event_id := 1, p_new_start_date := '2024-02-01 09:00:00',
  p_new_end_date := '2024-06-30 23:59:59',
  p_recurrence_type := 'weekly', p_recurrence_interval := 2,
  p_recurrence_day_of_week := 1
);
```

The interesting pieces here, infinite projection, schedule transitions over time, and exception handling, show up constantly in rostering, meetings, and billing cycles, but become a mess when every application reimplements them badly. Putting the logic into the database makes permissions, audit, and consistency much easier to centralize.


-------

## 31. pg_variables: Session Variables Faster than Temp Tables

`pg_variables`, developed by Postgres Professional, adds session-level variables for scalars, arrays, and records. Variables are grouped into named packages. Transaction semantics are configurable: by default they do **not** roll back with `BEGIN` / `ROLLBACK`, but when `is_transactional = true` they do honor rollback and savepoints.

```sql
SELECT pgv_set('vars', 'int1', 101);
SELECT pgv_get('vars', 'int1', NULL::int);  -- returns 101

-- Transactional variable: rolls back to SAVEPOINT
BEGIN;
SELECT pgv_set('vars', 'tx_val', 101, true);
SAVEPOINT sp1;
SELECT pgv_set('vars', 'tx_val', 102, true);
ROLLBACK TO sp1;
COMMIT;
SELECT pgv_get('vars', 'tx_val', NULL::int);  -- returns 101

-- Record-set operations
SELECT pgv_insert('pack', 'employees', row(1, 'Alice'::text));
SELECT * FROM pgv_select('pack', 'employees');
```

This is a high-performance alternative to temp tables that avoids catalog bloat. Useful for storing intermediate state in complex stored procedures and batch jobs, for connection-level caching, and as infrastructure for other extensions. `pgelog`, for example, uses it to cache `dblink` connections.


-------

## 32. pgelog: Logs That Survive Rollback

`pgelog`, developed by anfiau, uses `dblink` to simulate **pseudo-autonomous transactions**, so log records survive even when the calling transaction rolls back. That solves a classic problem in PL/pgSQL exception handling: if you write logs inside an `EXCEPTION` block and the outer transaction aborts, the logs normally disappear with it. `pg_variables` is used to cache `dblink` connections per session.

```sql
-- The log survives even if the outer transaction rolls back
DO $$
BEGIN
  PERFORM 1/0;  -- division by zero
EXCEPTION WHEN OTHERS THEN
  PERFORM pgelog_to_log('FAIL', 'my_func', 'division by zero', '1', SQLERRM, SQLSTATE);
  RAISE;
END $$;

-- Query logs
SELECT log_stamp, log_info FROM pgelog_logs ORDER BY log_stamp DESC LIMIT 5;

-- Configure log TTL
SELECT pgelog_set_param('pgelog_ttl_minutes', '2880');
```

If you care about audit trails on critical paths, losing the diagnostic trail because the business transaction rolled back is exactly what you do not want. It also makes staged batch or migration scripts easier to introspect than relying on `RAISE NOTICE`. Depends on both `dblink` and `pg_variables`. Because each session may open an extra connection, `max_connections` still deserves a look.


-------

## Conclusion

Taken together, these 32 additions trace out a few clear lines.

**First, PostgreSQL is internalizing more and more "professional objects."** BSON, Protobuf, RDF, recurring schedules, molecules, graph and ontology relationships: these extensions push the database beyond plain structured tables and toward a queryable store for complex domain objects. You still get the usual database infrastructure: permissions, audit, backup, and transaction semantics, with less data movement and fewer sidecar services.

**Second, query capabilities are turning into composable APIs.** RRF fusion, recursive SQL template trees, query rewriting, sparse algebra, sketch-based approximations: the shared goal is to express more complicated logic with fewer, more stable SQL building blocks, while keeping it auditable, reproducible, and optimizable.

**Third, the extension layer is taking on more platform and operations work.** From real-time telemetry export in `pg_stat_ch`, to container resource visibility in `pg_datasentinel`, to security hooks like `block_copy_command`, to soft-alert governance in `pg_isok`, more and more capabilities that used to live outside the database are being pulled inward.

**Fourth, PostgreSQL is going deeper into vertical domains.** From cheminformatics with `rdkit`, to hydrology with `pghydro`, to Kazakh-language NLP with `pg_kazsearch`, PostgreSQL keeps turning into the computational substrate for more specialized fields.

That is how the PostgreSQL extension ecosystem works. There are cathedrals, like Apache Foundation projects, and there are bazaars, like personal weekend builds. Together they are building the most advanced open-source database ecosystem in the world.
