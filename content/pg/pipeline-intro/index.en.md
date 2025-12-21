---
title: Getting Started with PipelineDB
date: 2018-09-07
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  PipelineDB is a PostgreSQL extension for streaming analytics. Here’s how to install it and build continuous views over live data.
tags: [PostgreSQL,PG管理,扩展]
---

PipelineDB extends PostgreSQL with streaming primitives—continuous views over unbounded input. Although the upstream project was discontinued, the concepts remain useful.

## Install & configure

PipelineDB ships as an extension. Install the RPM/DEB, then edit `postgresql.conf`:

```ini
shared_preload_libraries = 'pipelinedb'
max_worker_processes = 128
```

Restart Postgres. You must raise `max_worker_processes` or PipelineDB will fail to launch.

## Example: Wikipedia page views

1. **Create a stream** (foreign table backed by the PipelineDB handler):

```sql
CREATE FOREIGN TABLE wiki_stream (
  hour timestamp,
  project text,
  title text,
  view_count bigint,
  size bigint
) SERVER pipelinedb;
```

2. **Create a continuous view** to materialize rolling aggregates:

```sql
CREATE VIEW wiki_stats WITH (action = materialize) AS
SELECT hour,
       project,
       count(*) AS total_pages,
       sum(view_count) AS total_views,
       min(view_count) AS min_views,
       max(view_count) AS max_views,
       avg(view_count) AS avg_views,
       percentile_cont(0.99) WITHIN GROUP (ORDER BY view_count) AS p99_views,
       sum(size) AS total_bytes_served
FROM wiki_stream
GROUP BY hour, project;
```

3. **Ingest data** via `COPY`:

```bash
curl -sL http://pipelinedb.com/data/wiki-pagecounts | gunzip |
  psql -c "COPY wiki_stream (hour, project, title, view_count, size) FROM STDIN"
```

`wiki_stats` now updates continuously as new rows arrive.

## Core concepts

- **Streams** – foreign tables representing append-only input.
- **Continuous views** – materialized aggregates that update incrementally as stream events arrive.
- **Transforms** – optional preprocessing stages.

PipelineDB lets you express streaming jobs with plain SQL and reuse the Postgres toolchain you already know.
