---
title: "Incident Report: Connection Pool Contamination Caused by pg_dump"
linkTitle: "Incident Report: Connection Pool Contamination"
date: 2018-12-11
author: "vonng"
summary: "Sometimes, interactions between components manifest in subtle ways. For example, using pg_dump to export data from a connection pool can cause connection pool contamination issues."
tags: ["PostgreSQL","PG Management","Incident Report"]
---

PostgreSQL is great, but that doesn't mean it's Bug-Free. This time in the production environment, I encountered another very interesting case: a production incident caused by `pg_dump`. This is a very subtle bug triggered by Pgbouncer, `search_path`, and special `pg_dump` operations.

-------------------

## Background Knowledge

### Connection Contamination

In PostgreSQL, each database connection corresponds to a backend process that holds some temporary resources (state), which are destroyed when the connection ends, including:

* Parameters modified in this session. `RESET ALL;`
* Prepared statements. `DEALLOCATE ALL`
* Open cursors. `CLOSE ALL;`
* Listened message channels. `UNLISTEN *`
* Execution plan cache. `DISCARD PLANS;`
* Pre-allocated sequence values and their cache. `DISCARD SEQUENCES;`
* Temporary tables. `DISCARD TEMP`

Web applications frequently establish large numbers of database connections, so in practice, connection pools are usually used to reuse connections and reduce the overhead of connection creation and destruction. Besides using various language/driver built-in connection pools, Pgbouncer is the most commonly used third-party middleware connection pool. Pgbouncer provides a Transaction Pooling mode, where the connection pool assigns a server connection to the client connection when a client transaction begins, and when the transaction ends, the server connection is returned to the pool.

Transaction pooling mode also has some issues, such as **connection contamination**. When a client modifies the connection state and returns the connection to the pool, other applications may be affected unexpectedly. As shown in the diagram below:

![](pg-dump-failure.png)

Assume there are four client connections (frontend connections) C1, C2, C3, C4, and two server connections (backend connections) S1, S2. The database default search path is configured as: `app,$user,public`, and the application knows this assumption and uses `SELECT * FROM tbl;` to access table `app.tbl` in schema `app` by default. Now suppose client C2 executed `set search_path = ''` while using server connection S2, clearing the search path on connection S2. When S2 is reused by another client C3, C3 executing `SELECT * FROM tbl` will error because it cannot find the corresponding table in the `search_path`.

When client assumptions about connections are broken, various errors can easily occur.

-------------------

## Incident Investigation

The production application suddenly reported massive errors triggering circuit breaker, with error content being large amounts of objects (tables, functions) not found.

The first instinct was that the connection pool was contaminated: some connection modified the `search_path` and then returned the connection to the pool. When this backend connection is reused by other frontend connections, objects cannot be found.

Connecting to the corresponding pool, I found that indeed there were cases of connection `search_path` contamination - some connections had their `search_path` cleared, so applications using these connections couldn't find objects.

```bash
psql -p6432 somedb
# show search_path; \watch 0.1
```

Using the administrator account in Pgbouncer to execute the `RECONNECT` command, forcing reconnection of all connections, `search_path` was reset to default values, and the problem was resolved.

```bash
reconnect somedb
```

But the question arose: what application modified the `search_path`? If the source of the problem isn't investigated clearly, it might recur in the future. There are several possibilities: business code changes, application driver bugs, manual operations, or connection pool bugs. The most suspicious of course is manual operations - if someone used a production account to connect to the connection pool with `psql`, manually modified `search_path`, then exited, this connection would be returned to the production pool, causing contamination.

First, I checked the database logs and found that all error log records came from the same server connection `5c06218b.2ca6c`, meaning only one connection was contaminated. I found the critical moment when this connection started continuously erroring:

```python
cat postgresql-Tue.csv | grep 5c06218b.2ca6c

2018-12-04 14:44:42.766 CST,"xxx","xxx-xxx",182892,"127.0.0.1:60114",5c06218b.2ca6c,36,"SELECT",2018-12-04 14:41:15 CST,24/0,0,LOG,00000,"duration: 1067.392 ms  statement: SELECT xxxx FROM x",,,,,,,,,"app - xx.xx.xx.xx:23962"

2018-12-04 14:45:03.857 CST,"xxx","xxx-xxx",182892,"127.0.0.1:60114",5c06218b.2ca6c,37,"SELECT",2018-12-04 14:41:15 CST,24/368400961,0,ERROR,42883,"function upsert_xxxxxx(xxx) does not exist",,"No function matches the given name and argument types. You might need to add explicit type casts.",,,,"select upsert_phone_plan('965+6628',1,0,0,0,1,0,'2018-12-03 19:00:00'::timestamp)",8,,"app - 10.191.160.49:46382"
```

Here `5c06218b.2ca6c` is the unique identifier for that connection, and the following numbers `36,37` are the line numbers of logs generated by that connection. Some operations aren't recorded in logs, but fortunately here, the normal and error logs are only 21 seconds apart, allowing precise location of the incident time.

By scanning command operation records at that moment on all whitelist machines, I precisely located one execution record:

```bash
pg_dump --host master.xxxx --port 6432 -d somedb -t sometable
```

Hmm? Isn't `pg_dump` an official built-in tool? Could it modify `search_path`? But intuition told me it's really not impossible. For example, I remember an interesting behavior - since `schema` is essentially a namespace, objects in different schemas can have the same name. In older versions, when using `-t` to dump specific tables, if the provided table name parameter doesn't have a schema prefix, `pg_dump` would dump all tables with the same name by default.

Looking at the source code of `pg_dump`, I found there really is such an operation. Taking version 10.5 as an example, I found that during `setup_connection`, it indeed modifies `search_path`.

```c
// src/bin/pg_dump/pg_dump.c line 287
int main(int argc, char **argv);

// src/bin/pg_dump/pg_dump.c line 681 main
setup_connection(fout, dumpencoding, dumpsnapshot, use_role);

// src/bin/pg_dump/pg_dump.c line 1006 setup_connection
PQclear(ExecuteSqlQueryForSingleRow(AH, ALWAYS_SECURE_SEARCH_PATH_SQL));

// include/server/fe_utils/connect.h
#define ALWAYS_SECURE_SEARCH_PATH_SQL \
   "SELECT pg_catalog.set_config('search_path', '', false)" 
```

-------------------

## Bug Reproduction

Next was reproducing the bug. But oddly, I couldn't reproduce the bug when using PostgreSQL 11. So I looked at the complete history of the culprit, restored its thought process (found pg_dump and server version mismatch, tried different things), and using different versions of pg_dump finally reproduced the bug.

Using an existing database named `data` for testing, version 11.1. The Pgbouncer configuration used is as follows. For easier debugging, the connection pool size has been reduced to allow only two server connections.

```ini
[databases]
postgres = host=127.0.0.1

[pgbouncer]
logfile = /Users/vonng/pgb/pgbouncer.log
pidfile = /Users/vonng/pgb/pgbouncer.pid
listen_addr = *
listen_port = 6432
auth_type = trust
admin_users = postgres
stats_users = stats, postgres
auth_file = /Users/vonng/pgb/userlist.txt
pool_mode = transaction
server_reset_query =
max_client_conn = 50000
default_pool_size = 2

reserve_pool_size = 0
reserve_pool_timeout = 5

log_connections = 1
log_disconnections = 1
application_name_add_host = 1

ignore_startup_parameters = extra_float_digits
```

Start the connection pool and check `search_path` - normal default configuration.

```bash
$ psql postgres://vonng:123456@:6432/data -c 'show search_path;'
     search_path
-----------------------
 app, "$user", public
```

Using pg_dump version 10.5, initiating dump from port 6432:

```bash
/usr/local/Cellar/postgresql/10.5/bin/pg_dump \
	postgres://vonng:123456@:6432/data \
	-t geo.pois -f /dev/null
pg_dump: server version: 11.1; pg_dump version: 10.5
pg_dump: aborting because of server version mismatch
```

Although the dump failed, when checking the `search_path` of all connections again, you'll find that connections in the pool have been contaminated - one connection's `search_path` has been modified to empty:

```bash
$ psql postgres://vonng:123456@:6432/data -c 'show search_path;'
 search_path
-------------

(1 row)
```

-------------------

## Solution

Configuring both pgbouncer's `server_reset_query` and `server_reset_query_always` parameters can completely solve this problem.

```ini
server_reset_query = DISCARD ALL
server_reset_query_always = 1
```

In TransactionPooling mode, `server_reset_query` is not executed by default, so you need to configure `server_reset_query_always=1` to force execution of `DISCARD ALL` to clear all connection state after each transaction. However, this configuration comes with a cost. `DISCARD ALL` essentially executes the following operations:

```sql
SET SESSION AUTHORIZATION DEFAULT;
RESET ALL;
DEALLOCATE ALL;
CLOSE ALL;
UNLISTEN *;
SELECT pg_advisory_unlock_all();
DISCARD PLANS;
DISCARD SEQUENCES;
DISCARD TEMP;
```

If these statements need to be executed after each transaction, it will indeed bring some additional performance overhead.

Of course, there are other methods, such as administrative solutions to eliminate the possibility of using `pg_dump` to access port 6432, managing database accounts with dedicated encrypted configuration centers. Or requiring business parties to use schema-qualified names to access database objects. But all might have gaps, not as direct as forced configuration.