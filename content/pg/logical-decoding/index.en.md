---
title: "CDC Change Data Capture Mechanisms"
date: 2019-06-12
author: "vonng"
summary: >
  Change Data Capture is an interesting ETL alternative solution.
tags: [PostgreSQL, PG Development, CDC]
---

In actual production, we often need to synchronize database states to other places, such as synchronizing to data warehouses for analysis, to message queues for downstream consumption, or to caches to accelerate queries. Generally speaking, there are two major methods for moving state: ETL and CDC.


--------------------

## Prerequisites

### CDC and ETL

A database is essentially a **collection of states**, and any **changes** (inserts, updates, deletes) to the database are essentially modifications to state.

In actual production, we often need to synchronize database states to other places, such as synchronizing to data warehouses for analysis, to message queues for downstream consumption, or to caches to accelerate queries. Generally speaking, there are two major methods for moving state: ETL and CDC.

* ETL (Extract Transform Load) focuses on state itself, using scheduled batch polling to pull state itself.

* CDC (Change Data Capture) focuses on changes, continuously collecting state change events (changes) in a streaming manner.

Everyone is familiar with ETL - running daily batch ETL tasks to **extract (E)**, **transform (T)** format, and **load (L)** from production OLTP databases to data warehouses. We won't elaborate on this here. Compared to ETL, CDC is relatively new and is increasingly entering people's view with the rise of stream computing.

**Change data capture (CDC)** is a process of observing all data changes written to a database and extracting and transforming them into forms that can be replicated to other systems. CDC is interesting, especially when **changes** can be used for subsequent **stream processing** immediately after being written to the database.

For example, users can capture changes in databases and continuously apply the same changes to **search indexes** (e.g., elasticsearch). If change logs are applied in the same order, it can be expected that data in search indexes matches data in databases. Similarly, these changes can also be applied to refresh **caches** (redis) in the background, sent to **message queues** (Kafka), imported into **data warehouses** (EventSourcing, storing immutable fact event records rather than taking daily snapshots), **collecting statistics and monitoring** (Prometheus), and so on. In this sense, external indexes, caches, and data warehouses all become **logical replicas of PostgreSQL**, and these derived data systems all become consumers of change streams, while PostgreSQL becomes the master database of the entire **data system**. In this architecture, applications only need to worry about how to write data to the database, leaving the rest to CDC. System design can be greatly simplified: all data components can automatically maintain (eventual) consistency with the master database logically. Users no longer need to worry about how to keep data synchronized between multiple heterogeneous data systems.

![](cdc-system.png)

Actually, PostgreSQL's **logical replication** functionality provided since version 10.0 is essentially a **CDC application**: extracting change event streams from the master database: `INSERT, UPDATE, DELETE, TRUNCATE`, and replaying them on another PostgreSQL **master database** instance. If these insert/update/delete events can be parsed out, they can be used for any interested consumer, not just limited to another PostgreSQL instance.

### Logical Replication

Implementing CDC on traditional relational databases is not easy. The traditional relational database's **write-ahead log WAL** is actually a record of change events in the database. Therefore, capturing changes from databases can basically be considered equivalent to consuming WAL logs/replication logs produced by databases. (Of course, there are other change capture methods, such as building triggers on tables that write change records to another change log table when changes occur, and clients continuously tailing this log table, though this has certain limitations).

The problem with most database replication logs is that they have always been treated as internal implementation details of databases, not public APIs. Clients should query databases through their data models and query languages, not parse replication logs and try to extract data from them. Many databases have no documented way to access change logs at all. Therefore, capturing all changes in databases and then replicating them to other state stores (search indexes, caches, data warehouses) is quite difficult.

Furthermore, having **only** database change logs is still insufficient. If you have **complete** change logs, you can certainly rebuild the complete state of the database by replaying logs. But in many cases, keeping complete historical WAL logs is not a feasible option (due to disk space and replay time limitations). For example, building new full-text indexes requires a complete copy of the entire database — simply applying the latest change logs is insufficient because this would miss items that haven't been updated recently. Therefore, if you can't keep complete historical logs, you at least need to maintain a consistent database snapshot and keep change logs from that snapshot.

Therefore, to implement CDC, databases need to provide at least the following functionality:

1. Access database **change logs (WAL)** and decode them into logical events (inserts/updates/deletes on tables rather than database internal representations)

2. Access database "**consistent snapshots**" so subscribers can start subscribing from any consistent state rather than from database creation.

3. Save **consumer offsets** to track subscriber consumption progress and timely cleanup/recycle unused change logs to prevent disk overflow.

We'll find that PostgreSQL, while implementing logical replication, has already provided all the infrastructure needed for CDC.

* **Logical Decoding**, used to parse logical change events from WAL logs
* **Replication Protocol**: provides mechanisms for consumers to subscribe to database changes in real-time (even synchronous subscription)
* **Snapshot Export**: allows exporting consistent database snapshots (`pg_export_snapshot`)
* **Replication Slots**: used to save consumer offsets and track subscriber progress.

Therefore, the most intuitive and elegant way to implement CDC on PostgreSQL is **to write a "logical replica" according to PostgreSQL's replication protocol** that receives logically decoded change events from the database in real-time and streaming fashion, completes its own defined processing logic, and timely reports its message consumption progress to the database. Just like using Kafka. Here, CDC clients can masquerade as PostgreSQL replicas to continuously receive logically decoded change content from PostgreSQL master databases in real-time. At the same time, CDC clients can also save their **consumer offsets** (i.e., consumption progress) through PostgreSQL's **Replication Slot** mechanism, implementing **at-least-once** guarantees similar to message queues, ensuring no change data is missed. (Clients can record consumer offsets themselves and skip duplicate records to achieve "**exactly-once**" guarantees)

### Logical Decoding

Before starting further discussion, let's first look at what the expected output results actually look like.

PostgreSQL's change events are saved in **binary internal representation** form in write-ahead logs (WAL). Some human-readable information can be parsed using its built-in `pg_waldump` tool:

```
rmgr: Btree       len (rec/tot):     64/    64, tx:       1342, lsn: 2D/AAFFC9F0, prev 2D/AAFFC810, desc: INSERT_LEAF off 126, blkref #0: rel 1663/3101882/3105398 blk 4
rmgr: Heap        len (rec/tot):    485/   485, tx:       1342, lsn: 2D/AAFFCA30, prev 2D/AAFFC9F0, desc: INSERT off 10, blkref #0: rel 1663/3101882/3105391 blk 139
```

WAL logs contain complete authoritative change event records, but this record format is too low-level. Users are not interested in binary changes on some data page on disk (file A page B offset C append binary data D), they're interested in which rows and fields were inserted/updated/deleted in which tables. **Logical decoding** is the mechanism that translates physical change records into logical change events expected by users (such as insert/update/delete events on table A).

For example, users might expect decoded equivalent SQL statements:

```
INSERT INTO public.test (id, data) VALUES (14, 'hoho');
```

Or the most common JSON structure (here recording an UPDATE event in JSON format):

```json
{
  "change": [
    {
      "kind": "update",
      "schema": "public",
      "table": "test",
      "columnnames": ["id", "data" ],
      "columntypes": [ "integer", "text" ],
      "columnvalues": [ 1, "hoho"],
      "oldkeys": { "keynames": [ "id"],
        "keytypes": ["integer" ],
        "keyvalues": [1]
      }
    }
  ]
}
```

Of course, it can also be more compact and efficient strict Protobuf format, more flexible Avro format, or any format users are interested in.

**Logical decoding** solves the problem of **decoding** database internal binary representation change events into formats users are interested in. This process is necessary because database internal representations are very compact. To interpret raw binary WAL logs, you need not only knowledge about WAL structure but also **System Catalog**, i.e., metadata. Without metadata, you can only parse a series of oids that only the database can understand, not schema names, table names, column names that users might be interested in.

Regarding stream replication protocols, replication slots, transaction snapshots and other concepts and functions, we won't expand on them here. Let's move to the hands-on section.



--------------------

## Quick Start

Assume we have a user table and we want to capture any changes occurring on it. Assume the database undergoes the following change operations:

The following commands will be used repeatedly:

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users(id SERIAL PRIMARY KEY, name TEXT);

INSERT INTO users VALUES (100, 'Vonng');
INSERT INTO users VALUES (101, 'Xiao Wang');
DELETE FROM users WHERE id = 100;
UPDATE users SET name = 'Lao Wang' WHERE id = 101;
```

The final database state is: only one record `(101, 'Lao Wang')`. Whether there was once a user named `Vonng` or the fact that Old Wang was once young, all disappeared with database deletions and modifications. We hope these facts should not vanish with the wind and need to be recorded.

### Operation Flow

Generally speaking, subscribing to changes requires the following steps:

* Choose a consistent database snapshot as the starting point for subscribing to changes. (Create a replication slot)
* (Some changes occurred in the database)
* Read these changes and update your consumption progress.

So, let's start with the simplest method, using PostgreSQL's built-in SQL interface.

### SQL Interface

APIs for logical replication slot create/read/delete:

```sql
TABLE pg_replication_slots; -- Read
pg_create_logical_replication_slot(slot_name name, plugin name) -- Create
pg_drop_replication_slot(slot_name name) -- Delete
```

Get latest change data from logical replication slot:

```sql
pg_logical_slot_get_changes(slot_name name, ...)  -- Consume
pg_logical_slot_peek_changes(slot_name name, ...) -- Peek only, don't consume
```

Before officially starting, some database parameter modifications are needed. Modify `wal_level = logical` so that information in WAL logs is sufficient for logical decoding.

```sql
-- Create a replication slot test_slot, using the system's built-in test decoding plugin test_decoding, decoding plugins will be introduced later
SELECT * FROM pg_create_logical_replication_slot('test_slot', 'test_decoding');

-- Replay the above table creation and insert/update/delete operations
-- DROP TABLE | CREATE TABLE | INSERT 1 | INSERT 1 | DELETE 1 | UPDATE 1

-- Read the latest unconsumed change event stream in replication slot test_slot
SELECT * FROM  pg_logical_slot_get_changes('test_slot', NULL, NULL);
    lsn    | xid |                                data
-----------+-----+--------------------------------------------------------------------
 0/167C7E8 | 569 | BEGIN 569
 0/169F6F8 | 569 | COMMIT 569
 0/169F6F8 | 570 | BEGIN 570
 0/169F6F8 | 570 | table public.users: INSERT: id[integer]:100 name[text]:'Vonng'
 0/169F810 | 570 | COMMIT 570
 0/169F810 | 571 | BEGIN 571
 0/169F810 | 571 | table public.users: INSERT: id[integer]:101 name[text]:'Xiao Wang'
 0/169F8C8 | 571 | COMMIT 571
 0/169F8C8 | 572 | BEGIN 572
 0/169F8C8 | 572 | table public.users: DELETE: id[integer]:100
 0/169F938 | 572 | COMMIT 572
 0/169F970 | 573 | BEGIN 573
 0/169F970 | 573 | table public.users: UPDATE: id[integer]:101 name[text]:'Lao Wang'
 0/169F9F0 | 573 | COMMIT 573

-- Clean up created replication slot
SELECT pg_drop_replication_slot('test_slot');
```

Here, we can see a series of triggered events, where the beginning and commit of each transaction trigger an event. Because the current logical decoding mechanism doesn't support DDL changes, `CREATE TABLE` and `DROP TABLE` don't appear in the event stream - we can only see empty `BEGIN+COMMIT`. Another point to note is that **only successfully committed transactions produce logical decoding change events**. That is, users don't need to worry about receiving and processing many row change messages only to find out the transaction was rolled back and then worry about how to notify consumers to rollback changes.

Through the SQL interface, users can already pull the latest changes. This also means any language with PostgreSQL drivers can capture the latest changes from databases this way. Of course, this method is frankly quite primitive. A better approach is to use PostgreSQL's replication protocol to directly subscribe to change data streams from databases. Of course, this requires more work compared to using SQL interfaces.

### Using Clients to Receive Changes

Before writing our own CDC client, let's first try using the official built-in CDC client sample — `pg_recvlogical`. Similar to `pg_receivewal`, but it receives logically decoded changes. Here's a specific example:

```bash
# Start a CDC client, connect to database postgres, create slot named test_slot, use test_decoding decoding plugin, output to stdout
pg_recvlogical \
	-d postgres \
	--create-slot --if-not-exists --slot=test_slot \
	--plugin=test_decoding \
	--start -f -

# Open another session, replay the above table creation and insert/update/delete operations
# DROP TABLE | CREATE TABLE | INSERT 1 | INSERT 1 | DELETE 1 | UPDATE 1

# pg_recvlogical output results
BEGIN 585
COMMIT 585
BEGIN 586
table public.users: INSERT: id[integer]:100 name[text]:'Vonng'
COMMIT 586
BEGIN 587
table public.users: INSERT: id[integer]:101 name[text]:'Xiao Wang'
COMMIT 587
BEGIN 588
table public.users: DELETE: id[integer]:100
COMMIT 588
BEGIN 589
table public.users: UPDATE: id[integer]:101 name[text]:'Lao Wang'
COMMIT 589

# Cleanup: delete created replication slot
pg_recvlogical -d postgres --drop-slot --slot=test_slot
```

In the above example, main change events include transaction **begin** and **end**, and **row-level inserts/updates/deletes**. The default `test_decoding` plugin output format is:

```sql
BEGIN {transaction_id}
table {schema_name}.{table_name} {command_INSERT|UPDATE|DELETE}  {column_name}[{type}]:{value} ...
COMMIT {transaction_id}
```

Actually, PostgreSQL's logical decoding works like this: whenever specific events occur (table Truncate, row-level inserts/updates/deletes, transaction begin and commit), PostgreSQL calls a series of hook functions. The so-called **Logical Decoding Output Plugin** is such a collection of callback functions. They accept binary internal representation change events as input, consult some system catalogs, and translate binary data into results users are interested in.

### Logical Decoding Output Plugins

Besides PostgreSQL's built-in "for testing" logical decoding plugin: [`test_decoding`](https://github.com/postgres/postgres/blob/master/contrib/test_decoding/test_decoding.c), there are many ready-made output plugins, for example:

- JSON format output plugin: [`wal2json`](https://github.com/eulerto/wal2json)
- SQL format output plugin: [`decoder_raw`](https://github.com/michaelpq/pg_plugins/tree/master/decoder_raw)
- Protobuf output plugin: [`decoderbufs`](https://github.com/debezium/postgres-decoderbufs)

Of course, there's also the decoding plugin used by PostgreSQL's built-in logical replication: `pgoutput`, whose message format [documentation address](https://www.postgresql.org/docs/11/protocol-logicalrep-message-formats.html).

Installing these plugins is very simple. Some plugins (such as `wal2json`) can be easily installed directly from official binary sources.

```bash
yum install wal2json11
apt install postgresql-11-wal2json
```

Or if there are no binary packages, you can download and compile yourself. Just ensure `pg_config` is in your `PATH`, then execute `make & sudo make install`.

Taking the SQL format output `decoder_raw` plugin as an example:

```bash
git clone https://github.com/michaelpq/pg_plugins && cd pg_plugins/decoder_raw
make && sudo make install
```

Using `wal2json` to receive the same changes:

```bash
pg_recvlogical -d postgres --drop-slot --slot=test_slot
pg_recvlogical -d postgres --create-slot --if-not-exists --slot=test_slot \
	--plugin=wal2json --start -f -
```

Results:

```json
{"change":[]}
{"change":[{"kind":"insert","schema":"public","table":"users","columnnames":["id","name"],"columntypes":["integer","text"],"columnvalues":[100,"Vonng"]}]}
{"change":[{"kind":"insert","schema":"public","table":"users","columnnames":["id","name"],"columntypes":["integer","text"],"columnvalues":[101,"Xiao Wang"]}]}
{"change":[{"kind":"delete","schema":"public","table":"users","oldkeys":{"keynames":["id"],"keytypes":["integer"],"keyvalues":[100]}}]}
{"change":[{"kind":"update","schema":"public","table":"users","columnnames":["id","name"],"columntypes":["integer","text"],"columnvalues":[101,"Lao Wang"],"oldkeys":{"keynames":["id"],"keytypes":["integer"],"keyvalues":[101]}}]}
```

And using `decoder_raw` to get SQL format output:

```bash
pg_recvlogical -d postgres --drop-slot --slot=test_slot
pg_recvlogical -d postgres --create-slot --if-not-exists --slot=test_slot \
	--plugin=decoder_raw --start -f -
```

Results:

```sql
INSERT INTO public.users (id, name) VALUES (100, 'Vonng');
INSERT INTO public.users (id, name) VALUES (101, 'Xiao Wang');
DELETE FROM public.users WHERE id = 100;
UPDATE public.users SET id = 101, name = 'Lao Wang' WHERE id = 101;
```

`decoder_raw` can be used to extract SQL-form state changes. Replaying these extracted SQL statements on the same base state can achieve the same results. PostgreSQL uses this mechanism to implement logical replication.

A typical application scenario is database migration without downtime. In traditional no-downtime migration modes (dual-write, change-read, change-write), the third step change-write cannot be quickly rolled back after completion because if problems are discovered after write traffic switches to the new master database and you want to rollback immediately, the old master database will lose some data. At this time, you can use `decoder_raw` to extract latest changes from the master database and synchronize changes from the new master database to the old master database in real-time through a simple Bash command. This ensures that you can quickly rollback to the old master database at any point during migration.

```bash
pg_recvlogical -d <new_master_url> --slot=test_slot --plugin=decoder_raw --start -f - |
psql <old_master_url>
```

Another interesting scenario is UNDO LOG. PostgreSQL's crash recovery is based on REDO LOG, replaying WAL to any historical time point. In situations where database schema doesn't change and only table content inserts/updates/deletes have mistakes, you can completely use methods similar to `decoder_raw` to reverse-generate UNDO logs. This improves the speed of such crash recovery.

Finally, output plugins can format change events into various forms. Decoding output as Redis kv operations, or just extracting some key fields for updating statistics or building external indexes, has great imagination space.

Writing custom logical decoding output plugins is not complex. You can refer to [this](https://www.postgresql.org/docs/11/logicaldecoding-output-plugin.html) official documentation. After all, logical decoding output plugins are essentially just a collection of string-concatenating callback functions. Based on [official samples](https://github.com/postgres/postgres/blob/master/contrib/test_decoding/test_decoding.c) with slight modifications, you can easily implement your own logical decoding output plugin.






--------------------

## CDC Clients

PostgreSQL comes with a client application called `pg_recvlogical` that can write logical change event streams to standard output. But not all consumers can or want to use Unix Pipes to complete all work. Additionally, according to the end-to-end principle, using `pg_recvlogical` to persist change data streams to disk doesn't mean consumers have received and acknowledged the message - only consumers personally confirming to the database can achieve this.

Writing PostgreSQL CDC client programs essentially implements a "monkey version" database replica. Clients establish a **Replication Connection** with the database, masquerading as a replica: receiving decoded change message streams from the master database and periodically reporting their consumption progress (persistence progress, flush progress, apply progress) to the master database.

### Replication Connection

Replication connection, as the name suggests, is a special connection for **replication**. When establishing a connection with a PostgreSQL server, if connection parameters provide `replication=database|on|yes|1`, a replication connection is established instead of a regular connection. Replication connections can execute some special commands, such as `IDENTIFY_SYSTEM`, `TIMELINE_HISTORY`, `CREATE_REPLICATION_SLOT`, `START_REPLICATION`, `BASE_BACKUP`. In logical replication cases, some simple SQL queries can also be executed. Specific details can be found in the PostgreSQL official documentation's frontend-backend protocol chapter: https://www.postgresql.org/docs/current/protocol-replication.html

For example, the following command establishes a replication connection:

```bash
$ psql 'postgres://localhost:5432/postgres?replication=on&application_name=mocker'
```

From the system view `pg_stat_replication`, you can see the master database has identified a new "replica":

```
vonng=# table pg_stat_replication ;
-[ RECORD 1 ]----+-----------------------------
pid              | 7218
usesysid         | 10
usename          | vonng
application_name | mocker
client_addr      | ::1
client_hostname  |
client_port      | 53420
```

### Writing Custom Logic

Whether JDBC or Go language PostgreSQL drivers, they all provide corresponding infrastructure for handling replication connections.

Here let's write a simple CDC client in Go language. The example uses [`jackc/pgx`](https://github.com/jackx/pgx), a pretty good PostgreSQL driver written in Go. The code here is just for concept demonstration, so error handling is ignored - very naive. Save the following code as `main.go` and execute `go run main.go`.

Default three parameters are database connection string, logical decoding output plugin name, and replication slot name. Default values are:

```go
dsn := "postgres://localhost:5432/postgres?application_name=cdc"
plugin := "test_decoding"
slot := "test_slot"
```

```
go run main.go postgres:/postgres?application_name=cdc test_decoding test_slot
```

Code as follows:

```go
package main

import (
	"log"
	"os"
	"time"

	"context"
	"github.com/jackc/pgx"
)

type Subscriber struct {
	URL    string
	Slot   string
	Plugin string
	Conn   *pgx.ReplicationConn
	LSN    uint64
}

// Connect establishes a replication connection to the server, differing by automatically adding replication=on|1|yes|dbname parameter
func (s *Subscriber) Connect() {
	connConfig, _ := pgx.ParseURI(s.URL)
	s.Conn, _ = pgx.ReplicationConnect(connConfig)
}

// ReportProgress reports write, flush, and apply progress coordinates (consumer offset) to master database
func (s *Subscriber) ReportProgress() {
	status, _ := pgx.NewStandbyStatus(s.LSN)
	s.Conn.SendStandbyStatus(status)
}

// CreateReplicationSlot creates logical replication slot using given decoding plugin
func (s *Subscriber) CreateReplicationSlot() {
	if consistPoint, snapshotName, err := s.Conn.CreateReplicationSlotEx(s.Slot, s.Plugin); err != nil {
		log.Fatalf("fail to create replication slot: %s", err.Error())
	} else {
		log.Printf("create replication slot %s with plugin %s : consist snapshot: %s, snapshot name: %s",
			s.Slot, s.Plugin, consistPoint, snapshotName)
		s.LSN, _ = pgx.ParseLSN(consistPoint)
	}
}

// StartReplication starts logical replication (server starts sending event messages)
func (s *Subscriber) StartReplication() {
	if err := s.Conn.StartReplication(s.Slot, 0, -1); err != nil {
		log.Fatalf("fail to start replication on slot %s : %s", s.Slot, err.Error())
	}
}

// DropReplicationSlot uses temporary regular connection to delete replication slot (if exists), note that slots in use by replication connections cannot be deleted.
func (s *Subscriber) DropReplicationSlot() {
	connConfig, _ := pgx.ParseURI(s.URL)
	conn, _ := pgx.Connect(connConfig)
	var slotExists bool
	conn.QueryRow(`SELECT EXISTS(SELECT 1 FROM pg_replication_slots WHERE slot_name = $1)`, s.Slot).Scan(&slotExists)
	if slotExists {
		if s.Conn != nil {
			s.Conn.Close()
		}
		conn.Exec("SELECT pg_drop_replication_slot($1)", s.Slot)
		log.Printf("drop replication slot %s", s.Slot)
	}
}

// Subscribe starts subscribing to change events, main message loop
func (s *Subscriber) Subscribe() {
	var message *pgx.ReplicationMessage
	for {
		// Wait for a message, message might be a real message or just a heartbeat
		message, _ = s.Conn.WaitForReplicationMessage(context.Background())
		if message.WalMessage != nil {
			DoSomething(message.WalMessage) // If it's a real message, consume it
			if message.WalMessage.WalStart > s.LSN { // After consumption, update consumption progress and report to master database
				s.LSN = message.WalMessage.WalStart + uint64(len(message.WalMessage.WalData))
				s.ReportProgress()
			}
		}
		// If it's a heartbeat message, according to protocol, check if server requires progress reply.
		if message.ServerHeartbeat != nil && message.ServerHeartbeat.ReplyRequested == 1 {
			s.ReportProgress() // If server heartbeat requests progress reply, report progress
		}
	}
}

// Function that actually consumes messages, here just prints messages, can also write to Redis, Kafka, update statistics, send emails, etc.
func DoSomething(message *pgx.WalMessage) {
	log.Printf("[LSN] %s [Payload] %s", 
             pgx.FormatLSN(message.WalStart), string(message.WalData))
}

// If using JSON decoding plugin, this is the Schema for decoding
type Payload struct {
	Change []struct {
		Kind         string        `json:"kind"`
		Schema       string        `json:"schema"`
		Table        string        `json:"table"`
		ColumnNames  []string      `json:"columnnames"`
		ColumnTypes  []string      `json:"columntypes"`
		ColumnValues []interface{} `json:"columnvalues"`
		OldKeys      struct {
			KeyNames  []string      `json:"keynames"`
			KeyTypes  []string      `json:"keytypes"`
			KeyValues []interface{} `json:"keyvalues"`
		} `json:"oldkeys"`
	} `json:"change"`
}

func main() {
	dsn := "postgres://localhost:5432/postgres?application_name=cdc"
	plugin := "test_decoding"
	slot := "test_slot"
	if len(os.Args) > 1 {
		dsn = os.Args[1]
	}
	if len(os.Args) > 2 {
		plugin = os.Args[2]
	}
	if len(os.Args) > 3 {
		slot = os.Args[3]
	}

	subscriber := &Subscriber{
		URL:    dsn,
		Slot:   slot,
		Plugin: plugin,
	}                                // Create new CDC client
	subscriber.DropReplicationSlot() // Clean up leftover slot if exists

	subscriber.Connect()                   // Establish replication connection
	defer subscriber.DropReplicationSlot() // Clean up replication slot before program termination
	subscriber.CreateReplicationSlot()     // Create replication slot
	subscriber.StartReplication()          // Start receiving change stream
	go func() {
		for {
			time.Sleep(5 * time.Second)
			subscriber.ReportProgress()
		}
	}()                                    // Goroutine 2 reports progress to master database every 5 seconds
	subscriber.Subscribe()                 // Main message loop
}

```

Executing the above changes again in another database session, you can see the client timely receives change content. Here the client simply prints it out. In actual production, clients can do **any work**, such as writing to Kafka, Redis, disk logs, or just updating in-memory statistics and exposing to monitoring systems. Even, you can configure **synchronous commit** to ensure all system changes maintain strict synchronization at all times (though this affects performance compared to default async mode).

For PostgreSQL master databases, this looks like another replica.

```sql
postgres=# table pg_stat_replication; -- View current replicas
-[ RECORD 1 ]----+------------------------------
pid              | 14082
usesysid         | 10
usename          | vonng
application_name | cdc
client_addr      | 10.1.1.95
client_hostname  |
client_port      | 56609
backend_start    | 2019-05-19 13:14:34.606014+08
backend_xmin     |
state            | streaming
sent_lsn         | 2D/AB269AB8     -- Message coordinates server has sent
write_lsn        | 2D/AB269AB8     -- Message coordinates client has completed writing
flush_lsn        | 2D/AB269AB8     -- Message coordinates client has flushed to disk (won't be lost)
replay_lsn       | 2D/AB269AB8     -- Message coordinates client has applied (already effective)
write_lag        |
flush_lag        |
replay_lag       |
sync_priority    | 0
sync_state       | async

postgres=# table pg_replication_slots;  -- View current replication slots
-[ RECORD 1 ]-------+------------
slot_name           | test
plugin              | decoder_raw
slot_type           | logical
datoid              | 13382
database            | postgres
temporary           | f
active              | t
active_pid          | 14082
xmin                |
catalog_xmin        | 1371
restart_lsn         | 2D/AB269A80       -- Next client reconnection will start replaying from here
confirmed_flush_lsn | 2D/AB269AB8       -- Message progress client has confirmed completion
```






--------------------

## Limitations

To use CDC in production environments, some other issues need consideration. Regrettably, there are still two small clouds floating in PostgreSQL CDC's sky.

### Completeness

Currently, PostgreSQL's logical decoding only provides the following hooks:

```
LogicalDecodeStartupCB startup_cb;
LogicalDecodeBeginCB begin_cb;
LogicalDecodeChangeCB change_cb;
LogicalDecodeTruncateCB truncate_cb;
LogicalDecodeCommitCB commit_cb;
LogicalDecodeMessageCB message_cb;
LogicalDecodeFilterByOriginCB filter_by_origin_cb;
LogicalDecodeShutdownCB shutdown_cb;
```

Among these, the more important and mandatory ones are three callback functions: begin: transaction begin, change: row-level insert/update/delete events, commit: transaction commit. Regrettably, not all events have corresponding hooks, such as database schema changes, Sequence value changes, and special large object operations.

Usually, this is not a big problem because users are typically interested in table records rather than table structure inserts/updates/deletes. Moreover, if using flexible formats like JSON, Avro as decoding target formats, even if table structure changes, there won't be major problems.

But trying to generate complete UNDO logs from current change event streams is impossible because current schema change DDL is not recorded in logical decoding output. Good news is that more hooks and support will be available in the future, so this problem is solvable.

### Synchronous Commit

One thing to note is that **some output plugins ignore `Begin` and `Commit` messages**. These two messages are also part of database change logs. If output plugins ignore these messages, CDC clients might have deviations when reporting consumption progress (falling behind by one message offset). This might trigger issues in some boundary conditions: such as databases with very little write data enabling synchronous commit, where master databases wait indefinitely for replica confirmation of the last `Commit` message and get stuck.

### Failover

Ideals are beautiful, reality is harsh. When everything is normal, CDC workflows work well. But when databases fail or failover occurs, things become more complicated.

**Exactly-Once Guarantee**

Another issue with using PostgreSQL CDC is the classic **exactly-once** problem in message queues.

PostgreSQL's logical replication actually provides **at-least-once** guarantees because consumer offset values are saved during checkpoints. If PostgreSQL master databases crash, the restart point for resending change events may not exactly match the last position subscribers consumed. Therefore, duplicate messages might be sent.

The solution is: logical replication consumers also need to record their own consumer offsets to skip duplicate messages, achieving true **exactly-once** message delivery guarantees. This is not a real problem, just something anyone trying to implement CDC clients themselves should note.

**Failover Slot**

For current PostgreSQL CDC, Failover Slot is the biggest difficulty and pain point. Logical replication depends on replication slots because replication slots hold consumer state, recording consumer consumption progress, so databases won't clean up messages consumers haven't processed yet.

But with current implementation, replication slots can only be used on **master databases**, and **replication slots themselves are not replicated to replica databases**. Therefore, when master databases failover, consumer offsets are lost. If logical replication slots are not recreated on new master databases before they accept any writes, some data might be lost. For very strict scenarios, this functionality should be used cautiously.

This issue is planned to be resolved in the next major version (13). Failover Slot [Patch](https://commitfest.postgresql.org/23/1961/) is planned to be merged into mainline version 13 (2020).

Before then, if you want to use CDC in production, you must thoroughly test for failover scenarios. For example, failover operations when using CDC need modifications: the core idea is that operations and DBAs must manually complete replication slot replication work. Before failover, you can enable synchronous commit on the original master database, pause write traffic, and use scripts to copy original master database slots on the new master database, creating the same replication slots on the new master database, manually completing replication slot failover. For emergency failover scenarios where original master databases cannot be accessed and immediate switching is required, you can also use PITR afterward to recover missing changes.

Summary: CDC functionality mechanisms have reached production application requirements, but reliability mechanisms are still somewhat lacking. This problem can wait for the next mainline version or be solved through careful manual operations. Of course, aggressive users can also pull patches themselves to try early.