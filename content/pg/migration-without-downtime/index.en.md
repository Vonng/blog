---
title: "Changing Engines Mid-Flight — PostgreSQL Zero-Downtime Data Migration"
linkTitle: "Zero-Downtime Data Migration Basic Principles"
date: 2018-02-06
author: "vonng"
summary: "Data migration typically involves stopping services for updates. Zero-downtime data migration is a relatively advanced operation."
tags: ["PostgreSQL","PG-Admin","Migration"]
---

Data migration typically involves stopping services for updates. Zero-downtime data migration is a relatively advanced operation.

Zero-downtime data migration can essentially be viewed as consisting of three operations:

* Replication: **Logical replication** of target tables from source database to destination database.
* Read Migration: Migrate application **read paths** from source database to destination database.
* Write Migration: Migrate application **write paths** from source database to destination database.

However, in actual execution, these three steps may have different manifestations.

## Logical Replication

Using logical replication is a relatively stable approach, and there are several different methods: application-layer logical replication, database built-in logical replication (PostgreSQL 10+ logical subscription), and third-party logical replication plugins (such as pglogical).

Several logical replication methods each have their advantages and disadvantages. We adopted application-layer logical replication, which includes four steps:

#### 1. Replication

- Fork the target table schema from the old database in the new database, along with all dependent functions, sequences, permissions, owners, and other objects.
- Application adds dual-write logic, simultaneously writing the same data to both new and old databases.
  - Write to both new and old databases simultaneously
- Ensure incremental data is correctly written to two identical databases.
- Application needs to properly handle update/delete logic when full data doesn't exist. For example, change `UPDATE` to `UPSERT`, ignore `DELETE`.
- Application reads still go to the old database.
- When problems occur, rollback application to the original single-write version.

#### 2. Synchronization

- Add exclusive table-level lock to old table `LOCK TABLE <xxx> IN EXCLUSIVE MODE`, blocking all writes.
- Execute full synchronization `pg_dump | psql`
- Verify data consistency, determine if migration was successful.
- When problems occur, simply clear corresponding tables in the new database.

#### 3. Read Migration
- Application modified to read data from new database.
- When problems occur, rollback to version that reads from old database.

#### 4. Single Write
- After observing for some time without issues, application modified to write only to new database.
- When problems occur, rollback to dual-write version.

### Notes

The key is **blocking writes to the old table during full synchronization**. This can be achieved through table-level exclusive locks.

When tables are sharded, locking tables has very little impact on business.

A logical table split into 8192 partitions actually only needs to process one partition at a time.

Blocking writes to one eight-thousandth of the data for about a few seconds to ten seconds is usually acceptable for business.

But if it's a single very large table, special handling might be needed.

## ETL Function

The following Bash function accepts three parameters: source database URL, destination database URL, and the table name to migrate.

Assumes both source and destination databases are connectable and target tables exist.

```bash
function etl(){
    local src_url=${1}
    local dst_url=${2}
    local table_name=${3}

    rm -rf "/tmp/etl-${table_name}.done"
    
    psql ${src_url} -1qAtc "LOCK TABLE ${table_name} IN EXCLUSIVE MODE;COPY ${table_name} TO STDOUT;" \
    | psql ${dst_url} -1qAtc "LOCK TABLE ${table_name} IN EXCLUSIVE MODE; TRUNCATE ${table_name}; COPY ${table_name} FROM STDIN;"
    
    touch "/tmp/etl-${table_name}.done"
}
```

Although the source and destination tables are locked, in actual testing, the timing of the two psql processes exiting when the pipeline exits is not completely synchronized. The process at the front of the pipeline exits 0.1 seconds earlier than the one behind it. Under heavy load, this might cause data inconsistency.

Another more scientific approach is to split according to a unique constraint column, lock corresponding rows, update and then release.

## Physical Replication

Physical replication is replication achieved by replaying WAL logs, and is cluster-level replication.

Migration based on physical replication has very coarse granularity, only suitable for vertical database splits, and will have extremely brief service unavailability.

The process for data migration using physical replication is as follows:

- Replication: Pull out a replica from the primary database, maintain streaming replication.
- Read Migration: Change application read paths from primary to replica, but writes still go to primary.
  - If there are problems, rollback application to read-from-primary version.
- Write Migration: Promote replica to primary, block writes to old database, and immediately restart application, switching write paths to new primary.
  - Remove unneeded tables and databases.
  - This step cannot be rolled back (rollback would lose data written to new database)