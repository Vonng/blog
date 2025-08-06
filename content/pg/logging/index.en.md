---
title: "PostgreSQL Server Log Regular Configuration"
date: 2018-02-06
author: "vonng"
summary: >
  It's recommended to configure PostgreSQL's log format as CSV for easy analysis, and it can be directly imported into PostgreSQL data tables.
tags: [PostgreSQL, PG Administration, Logging]
---



It's recommended to configure PostgreSQL's log format as CSV for easy analysis, and it can be directly imported into PostgreSQL data tables.



## Log-Related Configuration Items

```ini
log_destination ='csvlog'
logging_collector =on
log_directory ='log'
log_filename ='postgresql-%a.log'
log_min_duration_statement =1000
log_checkpoints =on
log_lock_waits =on
log_statement ='ddl'
log_replication_commands =on
log_timezone ='UTC'
log_autovacuum_min_duration =1000

track_io_timing =on
track_functions =all
track_activity_query_size =16384
```



## Log Collection

If you need to collect logs from external sources, consider using filebeat.

```yaml
filebeat.prospectors:

## input
- type: log
enabled: true
paths:
- /var/lib/postgresql/data/pg_log/postgresql-*.csv
document_type: db-trace
tail_files: true
multiline.pattern: '^20\d\d-\d\d-\d\d'
multiline.negate: true
multiline.match: after
multiline.max_lines: 20
max_cpus: 1

## modules
filebeat.config.modules:
path: ${path.config}/modules.d/*.yml
reload.enabled: false

## queue
queue.mem:
events: 1024
flush.min_events: 0
flush.timeout: 1s

## output
output.kafka:
hosts: ["10.10.10.10:9092","x.x.x.x:9092"]
topics:
- topic: 'log.db'
```




## CSV Log Format

Very interesting idea - converting CSV logs into PostgreSQL tables is very convenient for analysis.

The original CSV log format definition is as follows:

```sql
Log table structure definition
create table postgresql_log
(
  log_time               timestamp,
  user_name              text,
  database_name          text,
  process_id             integer,
  connection_from        text,
  session_id             text   not null,
  session_line_num       bigint not null,
  command_tag            text,
  session_start_time     timestamp with time zone,
  virtual_transaction_id text,
  transaction_id         bigint,
  error_severity         text,
  sql_state_code         text,
  message                text,
  detail                 text,
  hint                   text,
  internal_query         text,
  internal_query_pos     integer,
  context                text,
  query                  text,
  query_pos              integer,
  location               text,
  application_name       text,
  PRIMARY KEY (session_id, session_line_num)
);
```



## Importing Logs

Logs are well-structured CSV (CSV allows multi-line records), you can directly use the COPY command to import them.

```sql
COPY postgresql_log FROM '/var/lib/pgsql/data/pg_log/postgresql.log' CSV DELIMITER ',';
```



## Mapping Logs

Of course, besides copying logs directly to data tables for analysis, there's another method that allows PostgreSQL to directly map its local CSVLOG as a foreign table for SQL-based direct access.

```sql
CREATE SCHEMA IF NOT EXISTS monitor;

-- search path for su
ALTER ROLE postgres SET search_path = public, monitor;
SET search_path = public, monitor;

-- extension
CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA monitor;

-- log parent table: empty
CREATE TABLE monitor.pg_log
(
  log_time               timestamp(3) with time zone,
  user_name              text,
  database_name          text,
  process_id             integer,
  connection_from        text,
  session_id             text,
  session_line_num       bigint,
  command_tag            text,
  session_start_time     timestamp with time zone,
  virtual_transaction_id text,
  transaction_id         bigint,
  error_severity         text,
  sql_state_code         text,
  message                text,
  detail                 text,
  hint                   text,
  internal_query         text,
  internal_query_pos     integer,
  context                text,
  query                  text,
  query_pos              integer,
  location               text,
  application_name       text,
  PRIMARY KEY (session_id, session_line_num)
);
COMMENT ON TABLE monitor.pg_log IS 'PostgreSQL csv log schema';
-- local file server
CREATE SERVER IF NOT EXISTS pg_log FOREIGN DATA WRAPPER file_fdw;
-- Change filename to actual path
CREATE FOREIGN TABLE IF NOT EXISTS monitor.pg_log_mon() INHERITS (monitor.pg_log) SERVER pg_log OPTIONS (filename '/pg/data/log/postgresql-Mon.csv', format 'csv');
CREATE FOREIGN TABLE IF NOT EXISTS monitor.pg_log_tue() INHERITS (monitor.pg_log) SERVER pg_log OPTIONS (filename '/pg/data/log/postgresql-Tue.csv', format 'csv');
CREATE FOREIGN TABLE IF NOT EXISTS monitor.pg_log_wed() INHERITS (monitor.pg_log) SERVER pg_log OPTIONS (filename '/pg/data/log/postgresql-Wed.csv', format 'csv');
CREATE FOREIGN TABLE IF NOT EXISTS monitor.pg_log_thu() INHERITS (monitor.pg_log) SERVER pg_log OPTIONS (filename '/pg/data/log/postgresql-Thu.csv', format 'csv');
CREATE FOREIGN TABLE IF NOT EXISTS monitor.pg_log_fri() INHERITS (monitor.pg_log) SERVER pg_log OPTIONS (filename '/pg/data/log/postgresql-Fri.csv', format 'csv');
CREATE FOREIGN TABLE IF NOT EXISTS monitor.pg_log_sat() INHERITS (monitor.pg_log) SERVER pg_log OPTIONS (filename '/pg/data/log/postgresql-Sat.csv', format 'csv');
CREATE FOREIGN TABLE IF NOT EXISTS monitor.pg_log_sun() INHERITS (monitor.pg_log) SERVER pg_log OPTIONS (filename '/pg/data/log/postgresql-Sun.csv', format 'csv');

```






## Processing Logs

You can use the following stored procedures to further extract statement execution times from log messages:

```sql
CREATE OR REPLACE FUNCTION extract_duration(statement TEXT)
  RETURNS FLOAT AS $$
DECLARE
  found_duration BOOLEAN;
BEGIN
  SELECT position('duration' in statement) > 0
  into found_duration;
  IF found_duration
  THEN
    RETURN (SELECT regexp_matches [1] :: FLOAT
            FROM regexp_matches(statement, 'duration: (.*) ms')
            LIMIT 1);
  ELSE
    RETURN NULL;
  END IF;
END
$$
LANGUAGE plpgsql
IMMUTABLE;


CREATE OR REPLACE FUNCTION extract_statement(statement TEXT)
  RETURNS TEXT AS $$
DECLARE
  found_statement BOOLEAN;
BEGIN
  SELECT position('statement' in statement) > 0
  into found_statement;
  IF found_statement
  THEN
    RETURN (SELECT regexp_matches [1]
            FROM regexp_matches(statement, 'statement: (.*)')
            LIMIT 1);
  ELSE
    RETURN NULL;
  END IF;
END
$$
LANGUAGE plpgsql
IMMUTABLE;


CREATE OR REPLACE FUNCTION extract_ip(app_name TEXT)
  RETURNS TEXT AS $$
DECLARE
  ip TEXT;
BEGIN
  SELECT regexp_matches [1]
  into ip
  FROM regexp_matches(app_name, '(\d+\.\d+\.\d+\.\d+)')
  LIMIT 1;
  RETURN ip;
END
$$
LANGUAGE plpgsql
IMMUTABLE;
```