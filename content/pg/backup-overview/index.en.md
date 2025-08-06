---
title: "Backup and Recovery Methods Overview"
date: 2018-02-09
author: vonng
summary: >
  Backup is the foundation of a DBA's livelihood. With backups, there's no need to panic.
tags: [PostgreSQL,PG Administration,Backup]
---

> Author: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/))

Backup is the foundation of a DBA's livelihood. With backups, there's no need to panic.

There are three forms of backup: SQL dumps, file system backups, and continuous archiving.

## 1. SQL Dumps

The idea behind the SQL dump method is:

Create a file composed of SQL commands that the server can use to rebuild a database in the same state as when the dump was made.

### 1.1 Dumping

The tools `pg_dump` and `pg_dumpall` are used for SQL dumps. Results are output to stdout.

```bash
pg_dump dbname > filename
pg_dump dbname -f filename
```

* `pg_dump` is a regular PostgreSQL client application. Backup work can be done from any remote host that can access the database.
* `pg_dump` doesn't run with any special privileges and must have read access to the tables you want to back up, following the same HBA mechanisms.
* To back up an entire database, you almost always need database superuser privileges.
* The important advantage of this backup method is that it's cross-version and cross-machine architecture compatible. (Can trace back to version 7.0)
* `pg_dump` backups are internally consistent, representing a database snapshot at the moment the dump started. Updates during the dump are not included.
* `pg_dump` doesn't block other database operations, except for commands requiring exclusive locks (like most ALTER TABLE commands).

### 1.2 Restoring

Text dump files can be read by psql. The common command to restore from a dump is:

```bash
psql dbname < infile
```

* This command doesn't create the database `dbname`; you must create it from `template0` before running psql. For example, use the command `createdb -T template0 dbname`. By default, `template1` and `template0` are the same, and newly created databases default to using `template1` as a template.

  `CREATE DATABASE dbname TEMPLATE template0;`

* Non-text file dumps can be restored using the [pg_restore](http://www.postgres.cn/docs/9.6/app-pgrestore.html) tool.

* Before starting restoration, object owners in the dump and users who have been granted privileges must already exist. If they don't exist, the restoration process won't be able to create objects with original ownership and privileges (sometimes this is what you need, but usually not).

* If restoration stops on errors, you can set the `ON_ERROR_STOP` variable to run psql, which exits with status 3 on SQL errors:

```bash
psql --set ON_ERROR_STOP=on dbname < infile
```

* During restoration, you can use a single transaction to ensure either complete correct restoration or complete rollback. Use `-1` or `--single-transaction`
* pg_dump and psql can do on-the-fly dumping and restoration through pipes

```
pg_dump -h host1 dbname | psql -h host2 dbname
```

### 1.3 Global Dumps

Some information belongs to the database cluster rather than individual databases, such as roles and tablespaces. If you want to dump these, use `pg_dumpall`

```
pg_dumpall > outfile
```

If you only want global data (roles and tablespaces), you can use the `-g, --globals-only` parameter.

The dump results can be restored using psql. Usually, loading the dump into an empty cluster can use `postgres` as the database name:

```
psql -f infile postgres
```

* Restoring a pg_dumpall dump often requires database superuser access privileges because it needs to restore role and tablespace information.
* If you used tablespaces, make sure the tablespace paths in the dump are appropriate for the new installation.
* pg_dumpall works by first creating role and tablespace dumps, then doing pg_dump for each database. This means each database is internally consistent, but snapshots of different databases are not synchronized.

### 1.4 Command Practice

Prepare environment, create test database:

```bash
psql postgres -c "CREATE DATABASE testdb;"
psql postgres -c "CREATE ROLE test_user LOGIN;"
psql testdb -c "CREATE TABLE test_table(i INTEGER);"
psql testdb -c "INSERT INTO test_table SELECT generate_series(1,16);"
```

```bash
# dump to local file
pg_dump testdb -f testdb.sql 

# dump and compress with xz, -c specifies accept from stdio, -d specifies decompress mode
pg_dump testdb | xz -cd > testdb.sql.xz

# dump, compress, split into 1m chunks
pg_dump testdb | xz | split -b 1m - testdb.sql.xz
cat testdb.sql.xz* | xz -cd | psql # restore

# pg_dump common parameter reference
-s --schema-only
-a --data-only
-t --table
-n --schema
-c --clean
-f --file

--inserts
--if-exists
-N --exclude-schema
-T --exclude-table
```

## 2. File System Dumps

The idea behind the file system dump method is: copy all files in the data directory. To get a usable backup, all backup files should remain consistent.

So usually, and to get a usable backup, all backup files should remain consistent.

* File system copying doesn't do logical parsing, just simple file copying. The advantage is fast execution, saving logical parsing and index rebuilding time. The disadvantage is larger space usage and can only be used for backing up entire database clusters.

- Simplest way: shut down, directly copy all files in the data directory.

- There are ways to get consistent frozen snapshots through file systems (like xfs) without shutting down, but WAL and data directories must be consistent.
- You can make pg_basebackup for remote archive backup without shutting down.

- You can use rsync to incrementally sync data changes to remote locations during shutdown.

## 3. PITR Continuous Archiving and Point-in-Time Recovery

PostgreSQL continuously generates WAL during operation. WAL records operation logs. Starting from a baseline full backup and replaying subsequent WAL can restore the database to any point in time. To implement this functionality, you need to configure WAL archiving to continuously save the WAL generated by the database.

WAL is logically an infinite byte stream. The `pg_lsn` type (bigint) can mark positions in WAL. `pg_lsn` represents a byte position offset in WAL. But in practice, WAL isn't a continuous single file but is segmented into 16MB chunks.

WAL file names follow a pattern and cannot be changed during archiving. Usually 24 hexadecimal digits, like `000000010000000000000003`, where the first 8 hex digits represent the timeline, and the last 16 digits represent the 16MB block sequence number, i.e., the value of `lsn >> 24`.

When viewing `pg_lsn`, for example `0/84A8300`, just remove the last six hex digits to get the latter part of the WAL file sequence number. Here, that's `8`. If using the default timeline 1, the corresponding WAL file is `000000010000000000000008`.

### 3.1 Environment Preparation

```bash
# Directories:
# Use /var/lib/pgsql/data as master directory, use /var/lib/pgsql/wal as log archive directory
# sudo mkdir /var/lib/pgsql && sudo chown postgres:postgres /var/lib/pgsql/
pg_ctl stop -D /var/lib/pgsql/data
rm -rf /var/lib/pgsql/{data,wal} && mkdir -p /var/lib/pgsql/{data,wal}

# Initialization:
# Initialize master and modify configuration files
pg_ctl -D /var/lib/pgsql/data init 

# Configuration files
# Create default additional configuration folder and configure include_dir in postgresql.conf
mkdir -p /var/lib/pgsql/data/conf.d
cat >> /var/lib/pgsql/data/postgresql.conf <<- 'EOF'
include_dir = 'conf.d'
EOF
```

### 3.2 Configure Automatic Archiving Command

```bash
# Archive configuration
# %p represents src wal path, %f represents filename
cat > /var/lib/pgsql/data/conf.d/archive.conf <<- 'EOF'
archive_mode = on
archive_command = 'conf.d/archive.sh %p %f'
EOF

# Archive script 
cat > /var/lib/pgsql/data/conf.d/archive.sh <<- 'EOF'
test ! -f /var/lib/pgsql/wal/${2} && cp ${1} /var/lib/pgsql/wal/${2}
EOF
chmod a+x /var/lib/pgsql/data/conf.d/archive.sh
```

Archive scripts can be as simple as just a `cp`, or very complex. But note the following:

- Archive commands execute under database user `postgres`, best placed in a 0700 directory.
- Archive commands should refuse to overwrite existing files, returning an error code when overwriting occurs.
- Archive commands can be updated by reloading configuration.

- Handle archive failure situations

- Archive files should retain original file names.

- WAL doesn't record configuration file changes.

- In archive commands: `%p` is replaced with the path of the WAL to be archived, and `%f` is replaced with the filename of the WAL to be archived

- Archive scripts can use more complex logic, for example the following archive command creates a folder named with date YYYYMMDD in the archive directory each day, removes the previous day's archive logs at 12 noon daily. Each day's archive logs are stored compressed with xz.

  ```bash
  wal_dir=/var/lib/pgsql/wal;
  [[ $(date +%H%M) == 1200 ]] && rm -rf ${wal_dir}/$(date -d"yesterday" +%Y%m%d); /bin/mkdir -p ${wal_dir}/$(date +%Y%m%d) && \
  test ! -f ${wal_dir}/ && \ 
  xz -c %p > ${wal_dir}/$(date +%Y%m%d)/%f.xz
  ```

- Archiving can also be done using external dedicated backup tools, such as `pgbackrest` and `barman`.

### 3.3 Test Archiving

```bash
# Start database
pg_ctl -D /var/lib/pgsql/data start

# Confirm configuration
psql postgres -c "SELECT name,setting FROM pg_settings where name like '%archive%';"
```

Start a monitoring loop in the current shell, continuously querying WAL position and file changes in archive directory and `pg_wal`:

```bash
for((i=0;i<100;i++)) do 
	sleep 1 && \
	ls /var/lib/pgsql/data/pg_wal && ls /var/lib/pgsql/data/pg_wal/archive_status/
	psql postgres -c 'SELECT pg_current_wal_lsn() as current, pg_current_wal_insert_lsn() as insert, pg_current_wal_flush_lsn() as flush;'
done
```

In another shell, create a test table `foobar` with a single timestamp column and introduce load, writing 10,000 records per second:

```bash
psql postgres -c 'CREATE TABLE foobar(ts TIMESTAMP);'
for((i=0;i<1000;i++)) do 
	sleep 1 && \
	psql postgres -c 'INSERT INTO foobar SELECT now() FROM generate_series(1,10000)' && \
	psql postgres -c 'SELECT pg_current_wal_lsn() as current, pg_current_wal_insert_lsn() as insert, pg_current_wal_flush_lsn() as flush;'
done
```

#### Natural WAL Switching

You can see that when the WAL LSN position exceeds 16M (representable by the last 6 hex digits), it rotates to a new WAL file, and the archive command archives the completed WAL.

```bash
000000010000000000000001 archive_status
  current  |  insert   |   flush
-----------+-----------+-----------
 0/1FC2630 | 0/1FC2630 | 0/1FC2630
(1 row)

# rotate here

000000010000000000000001 000000010000000000000002 archive_status
000000010000000000000001.done
  current  |  insert   |   flush
-----------+-----------+-----------
 0/205F1B8 | 0/205F1B8 | 0/205F1B8
```

#### Manual WAL Switching

Open another shell and execute `pg_switch_wal` to force writing a new WAL file:

```bash
psql postgres -c 'SELECT pg_switch_wal();'
```

You can see that although the position was only at `32C1D68`, it immediately jumped to the next 16MB boundary.

```bash
000000010000000000000001 000000010000000000000002 000000010000000000000003 archive_status
000000010000000000000001.done 000000010000000000000002.done
  current  |  insert   |   flush
-----------+-----------+-----------
 0/32C1D68 | 0/32C1D68 | 0/32C1D68
(1 row)

# switch here

000000010000000000000001 000000010000000000000002 000000010000000000000003 archive_status
000000010000000000000001.done 000000010000000000000002.done 000000010000000000000003.done
  current  |  insert   |   flush
-----------+-----------+-----------
 0/4000000 | 0/4000028 | 0/4000000
(1 row)

000000010000000000000001 000000010000000000000002 000000010000000000000003 000000010000000000000004 archive_status
000000010000000000000001.done 000000010000000000000002.done 000000010000000000000003.done
  current  |  insert   |   flush
-----------+-----------+-----------
 0/409CBA0 | 0/409CBA0 | 0/409CBA0
(1 row)
```

#### Force Kill Database

When the database shuts down abnormally due to failure, after restart, it will replay WAL starting from the most recent checkpoint, which is `0/2FB0160`.

```bash
[17:03:37] vonng@vonng-mac /var/lib/pgsql
$  ps axu | grep postgres | grep data | awk '{print $2}' | xargs kill -9

[17:06:31] vonng@vonng-mac /var/lib/pgsql
$ pg_ctl -D /var/lib/pgsql/data start
pg_ctl: another server might be running; trying to start server anyway
waiting for server to start....2018-01-25 17:07:27.063 CST [9762] LOG:  listening on IPv6 address "::1", port 5432
2018-01-25 17:07:27.063 CST [9762] LOG:  listening on IPv4 address "127.0.0.1", port 5432
2018-01-25 17:07:27.064 CST [9762] LOG:  listening on Unix socket "/tmp/.s.PGSQL.5432"
2018-01-25 17:07:27.078 CST [9763] LOG:  database system was interrupted; last known up at 2018-01-25 17:06:01 CST
2018-01-25 17:07:27.117 CST [9763] LOG:  database system was not properly shut down; automatic recovery in progress
2018-01-25 17:07:27.120 CST [9763] LOG:  redo starts at 0/2FB0160
2018-01-25 17:07:27.722 CST [9763] LOG:  invalid record length at 0/49CBE78: wanted 24, got 0
2018-01-25 17:07:27.722 CST [9763] LOG:  redo done at 0/49CBE50
2018-01-25 17:07:27.722 CST [9763] LOG:  last completed transaction was at log time 2018-01-25 17:06:30.158602+08
2018-01-25 17:07:27.741 CST [9762] LOG:  database system is ready to accept connections
 done
server started
```

At this point, WAL archiving has been confirmed to work normally.

### 3.4 Create Base Backup

First, check the current WAL position:

```bash
$ psql postgres -c 'SELECT pg_current_wal_lsn() as current, pg_current_wal_insert_lsn() as insert, pg_current_wal_flush_lsn() as flush;'

  current  |  insert   |   flush
-----------+-----------+-----------
 0/49CBF20 | 0/49CBF20 | 0/49CBF20
```

Use `pg_basebackup` to create a base backup:

```bash
psql postgres -c 'SELECT now();'
pg_basebackup -Fp -Pv -Xs -c fast -D /var/lib/pgsql/bkup

# Common options
-D  : Required, base backup location.
-Fp : Backup format: plain files, tar archive files
-Pv : -P enables progress reporting -v enables verbose output
-Xs : Include WAL logs generated during backup f:fetch after backup s:stream during backup
-c  : fast immediately execute checkpoint instead of spreading IO spread:spread IO
-R  : Set recovery.conf
```

When creating a base backup, a checkpoint is immediately created to ensure all dirty data pages are flushed to disk.

```bash
$ pg_basebackup -Fp -Pv -Xs -c fast -D /var/lib/pgsql/bkup
pg_basebackup: initiating base backup, waiting for checkpoint to complete
pg_basebackup: checkpoint completed
pg_basebackup: write-ahead log start point: 0/5000028 on timeline 1
pg_basebackup: starting background WAL receiver
45751/45751 kB (100%), 1/1 tablespace
pg_basebackup: write-ahead log end point: 0/50000F8
pg_basebackup: waiting for background process to finish streaming ...
pg_basebackup: base backup completed
```

### 3.5 Using Backups

#### Direct Use

The simplest way to use it is to start it directly with `pg_ctl`.

When `recovery.conf` doesn't exist, doing this starts a new complete database instance, preserving exactly the state when the backup was completed. The database won't realize it's a backup but thinks it didn't shut down properly last time and should apply WAL in the `pg_wal` directory for recovery, then restart normally.

Basic full backups might be made daily or weekly. To restore to the latest moment, you need to use them with WAL archiving.

#### Using WAL Archives to Catch Up

You can create a `recovery.conf` file in the backup database and specify the `restore_command` option. This way, when you start this data directory with `pg_ctl`, postgres will sequentially fetch the required WAL until there are no more.

```bash
cat >> /var/lib/pgsql/bkup/recovery.conf <<- 'EOF'
restore_command = 'cp /var/lib/pgsql/wal/%f %p' 
EOF
```

Continue executing load on the original master. At this time, WAL progress has reached `0/9060CE0`, while the backup position was still at `0/5000028` when it was made.

After starting the backup, you can see that the backup database automatically fetched WAL files 5-8 from the archive folder and applied them.

```bash
$ pg_ctl start -D /var/lib/pgsql/bkup -o '-p 5433'
waiting for server to start....2018-01-25 17:35:35.001 CST [10862] LOG:  listening on IPv6 address "::1", port 5433
2018-01-25 17:35:35.001 CST [10862] LOG:  listening on IPv4 address "127.0.0.1", port 5433
2018-01-25 17:35:35.002 CST [10862] LOG:  listening on Unix socket "/tmp/.s.PGSQL.5433"
2018-01-25 17:35:35.016 CST [10863] LOG:  database system was interrupted; last known up at 2018-01-25 17:21:15 CST
2018-01-25 17:35:35.051 CST [10863] LOG:  starting archive recovery
2018-01-25 17:35:35.063 CST [10863] LOG:  restored log file "000000010000000000000005" from archive
2018-01-25 17:35:35.069 CST [10863] LOG:  redo starts at 0/5000028
2018-01-25 17:35:35.069 CST [10863] LOG:  consistent recovery state reached at 0/50000F8
2018-01-25 17:35:35.070 CST [10862] LOG:  database system is ready to accept read only connections
 done
server started
2018-01-25 17:35:35.081 CST [10863] LOG:  restored log file "000000010000000000000006" from archive
$ 2018-01-25 17:35:35.924 CST [10863] LOG:  restored log file "000000010000000000000007" from archive
2018-01-25 17:35:36.783 CST [10863] LOG:  restored log file "000000010000000000000008" from archive
cp: /var/lib/pgsql/wal/000000010000000000000009: No such file or directory
2018-01-25 17:35:37.604 CST [10863] LOG:  redo done at 0/8FFFF90
2018-01-25 17:35:37.604 CST [10863] LOG:  last completed transaction was at log time 2018-01-25 17:30:39.107943+08
2018-01-25 17:35:37.614 CST [10863] LOG:  restored log file "000000010000000000000008" from archive
cp: /var/lib/pgsql/wal/00000002.history: No such file or directory
2018-01-25 17:35:37.629 CST [10863] LOG:  selected new timeline ID: 2
cp: /var/lib/pgsql/wal/00000001.history: No such file or directory
2018-01-25 17:35:37.678 CST [10863] LOG:  archive recovery complete
2018-01-25 17:35:37.783 CST [10862] LOG:  database system is ready to accept connections
```

But using WAL archives for recovery also has problems. For example, querying the latest data records from the master and standby, you find a one-second time difference. This means that WAL not yet written by the master hasn't been archived and thus wasn't applied.

```bash
[17:37:22] vonng@vonng-mac /var/lib/pgsql
$ psql postgres -c 'SELECT max(ts) FROM foobar;'
            max
----------------------------
 2018-01-25 17:30:40.159684
(1 row)


[17:37:42] vonng@vonng-mac /var/lib/pgsql
$ psql postgres -p 5433 -c 'SELECT max(ts) FROM foobar;'
            max
----------------------------
 2018-01-25 17:30:39.097167
(1 row)
```

Usually `archive_command, restore_command` are mainly used for emergency recovery, such as when both master and standby are down.

### 3.6 Specifying Progress

By default, recovery will continue to the end of the WAL log. The following parameters can be used to specify an earlier stopping point. At most one of the four options `recovery_target`, `recovery_target_name`, `recovery_target_time`, and `recovery_target_xid` can be used. If multiple are used in the configuration file, the last one will be used.

Among the four recovery targets above, `recovery_target_time` is commonly used to specify what time to restore the system to.

Several other commonly used options include:

- `recovery_target_inclusive` (`boolean`): Whether to include the target point, default is true
- `recovery_target_timeline` (`string`): Specify recovery to a specific timeline.
- `recovery_target_action` (`enum`): Specify the action the server should take immediately upon reaching the recovery target.
  - `pause`: Pause recovery, default option, can be resumed with `pg_wal_replay_resume`.
  - `shutdown`: Automatically shut down.
  - `promote`: Start accepting connections

For example, a backup was created at `2018-01-25 18:51:20`:

```bash
$ psql postgres -c 'SELECT now();'
             now
------------------------------
 2018-01-25 18:51:20.34732+08
(1 row)


[18:51:20] vonng@vonng-mac ~
$ pg_basebackup -Fp -Pv -Xs -c fast -D /var/lib/pgsql/bkup
pg_basebackup: initiating base backup, waiting for checkpoint to complete
pg_basebackup: checkpoint completed
pg_basebackup: write-ahead log start point: 0/3000028 on timeline 1
pg_basebackup: starting background WAL receiver
33007/33007 kB (100%), 1/1 tablespace
pg_basebackup: write-ahead log end point: 0/30000F8
pg_basebackup: waiting for background process to finish streaming ...
pg_basebackup: base backup completed
```

After running for two minutes, at `2018-01-25 18:53:05` we found some dirty data, so we recover from backup, hoping to restore to the state one minute before the dirty data appeared, for example `2018-01-25 18:52`

You can configure like this:

```bash
cat >> /var/lib/pgsql/bkup/recovery.conf <<- 'EOF'
restore_command = 'cp /var/lib/pgsql/wal/%f %p' 
recovery_target_time = '2018-01-25 18:52:30'
recovery_target_action = 'promote'
EOF
```

When the new database instance completes recovery, you can see its state has indeed returned to 18:52, which is exactly what we expected.

```bash
$ pg_ctl -D /var/lib/pgsql/bkup -o '-p 5433' start
waiting for server to start....2018-01-25 18:56:24.147 CST [13120] LOG:  listening on IPv6 address "::1", port 5433
2018-01-25 18:56:24.147 CST [13120] LOG:  listening on IPv4 address "127.0.0.1", port 5433
2018-01-25 18:56:24.148 CST [13120] LOG:  listening on Unix socket "/tmp/.s.PGSQL.5433"
2018-01-25 18:56:24.162 CST [13121] LOG:  database system was interrupted; last known up at 2018-01-25 18:51:22 CST
2018-01-25 18:56:24.197 CST [13121] LOG:  starting point-in-time recovery to 2018-01-25 18:52:30+08
2018-01-25 18:56:24.210 CST [13121] LOG:  restored log file "000000010000000000000003" from archive
2018-01-25 18:56:24.215 CST [13121] LOG:  redo starts at 0/3000028
2018-01-25 18:56:24.215 CST [13121] LOG:  consistent recovery state reached at 0/30000F8
2018-01-25 18:56:24.216 CST [13120] LOG:  database system is ready to accept read only connections
 done
server started
2018-01-25 18:56:24.228 CST [13121] LOG:  restored log file "000000010000000000000004" from archive
$ 2018-01-25 18:56:25.034 CST [13121] LOG:  restored log file "000000010000000000000005" from archive
2018-01-25 18:56:25.853 CST [13121] LOG:  restored log file "000000010000000000000006" from archive
2018-01-25 18:56:26.235 CST [13121] LOG:  recovery stopping before commit of transaction 649, time 2018-01-25 18:52:30.492371+08
2018-01-25 18:56:26.235 CST [13121] LOG:  redo done at 0/67CFD40
2018-01-25 18:56:26.235 CST [13121] LOG:  last completed transaction was at log time 2018-01-25 18:52:29.425596+08
cp: /var/lib/pgsql/wal/00000002.history: No such file or directory
2018-01-25 18:56:26.240 CST [13121] LOG:  selected new timeline ID: 2
cp: /var/lib/pgsql/wal/00000001.history: No such file or directory
2018-01-25 18:56:26.293 CST [13121] LOG:  archive recovery complete
2018-01-25 18:56:26.401 CST [13120] LOG:  database system is ready to accept connections
$

# query new server, indeed returned to 18:52
$ psql postgres -p 5433 -c 'SELECT max(ts) FROM foobar;'
            max
----------------------------
 2018-01-25 18:52:29.413911
(1 row)
```

### 3.7 Timelines

Whenever archive recovery is complete, that is, when the server can start accepting new queries and writing new WAL, a new timeline is created to distinguish newly generated WAL records. WAL file names consist of timeline and log sequence numbers, so new timeline WAL won't overwrite old timeline WAL. Timelines are mainly used to resolve complex recovery operation conflicts. For example, imagine a scenario: after restoring to 18:52 just now, the new server starts continuously accepting requests:

```bash
psql postgres -c 'CREATE TABLE foobar(ts TIMESTAMP);'
for((i=0;i<1000;i++)) do 
	sleep 1 && \
	psql -p 5433 postgres -c 'INSERT INTO foobar SELECT now() FROM generate_series(1,10000)' && \
	psql -p 5433 postgres -c 'SELECT pg_current_wal_lsn() as current, pg_current_wal_insert_lsn() as insert, pg_current_wal_flush_lsn() as flush;'
done
```

You can see that two WAL segment files numbered `6` appeared in the WAL archive directory. Without the timeline prefix for distinction, WAL would be overwritten.

```bash
$ ls -alh wal
total 262160
drwxr-xr-x  12 vonng  wheel   384B Jan 25 18:59 .
drwxr-xr-x   6 vonng  wheel   192B Jan 25 18:51 ..
-rw-------   1 vonng  wheel    16M Jan 25 18:51 000000010000000000000001
-rw-------   1 vonng  wheel    16M Jan 25 18:51 000000010000000000000002
-rw-------   1 vonng  wheel    16M Jan 25 18:51 000000010000000000000003
-rw-------   1 vonng  wheel   302B Jan 25 18:51 000000010000000000000003.00000028.backup
-rw-------   1 vonng  wheel    16M Jan 25 18:51 000000010000000000000004
-rw-------   1 vonng  wheel    16M Jan 25 18:52 000000010000000000000005
-rw-------   1 vonng  wheel    16M Jan 25 18:52 000000010000000000000006
-rw-------   1 vonng  wheel    50B Jan 25 18:56 00000002.history
-rw-------   1 vonng  wheel    16M Jan 25 18:58 000000020000000000000006
-rw-------   1 vonng  wheel    16M Jan 25 18:59 000000020000000000000007
```

If you regret after completing recovery, you can use the base backup to recover again to the state when first run to 18:53 by specifying `recovery_target_timeline = '1'`.

### 3.8 Other Considerations

* Before PostgreSQL 10, operations on hash indexes weren't recorded in WAL and needed manual REINDEX on slaves.
* Don't modify any **template databases** while creating base backups
* Note that tablespaces strictly record their paths literally. If you used tablespaces, be very careful during recovery.

## 4. Creating Standby Servers

Through master-slave setups, you can simultaneously improve availability and reliability.

- Master-slave read-write separation improves performance: write requests go to master, transmitted to standby through WAL streaming replication, standby accepts read requests.
- Improve reliability through backups: when one server fails, another can immediately take over (promote slave or make new slave)

Usually master-slave, replica, standby belong to high availability topics. But from another perspective, standby is also a form of backup.

#### Create Directories

```bash
sudo mkdir /var/lib/pgsql && sudo chown postgres:postgres /var/lib/pgsql/
mkdir -p /var/lib/pgsql/master /var/lib/pgsql/slave /var/lib/pgsql/wal
```

#### Create Master

```bash
pg_ctl -D /var/lib/pgsql/master init && pg_ctl -D /var/lib/pgsql/master start
```

#### Create User

Creating a standby requires a user with `REPLICATION` privileges. Here we create a `replication` user in the master:

```bash
psql postgres -c 'CREATE USER replication REPLICATION;'
```

To create a standby, you need a user with `REPLICATION` privileges and allow access in `pg_hba`. Version 10 allows by default:

```ini
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
```

#### Create Standby

Create a slave instance through `pg_basebackup`. Actually connects to the master instance and copies a data directory locally.

```bash
pg_basebackup -Fp -Pv -R -c fast -U replication -h localhost -D /var/lib/pgsql/slave
```

The key here is the `-R` option, which automatically fills master connection information into `recovery.conf` during backup creation. This way, when starting with `pg_ctl`, the database realizes it's a standby and automatically fetches WAL from the master to catch up.

#### Start Standby

```bash
pg_ctl -D /var/lib/pgsql/slave -o "-p 5433" start
```

The only difference between standby and master is an additional `recovery.conf` file in the data directory. This file not only identifies standby status but is also needed during failure recovery. For standbys created by `pg_basebackup`, it contains two parameters by default:

```ini
standby_mode = 'on'
primary_conninfo = 'user=replication passfile=''/Users/vonng/.pgpass'' host=localhost port=5432 sslmode=prefer sslcompression=1 krbsrvname=postgres target_session_attrs=any'
```

`standby_mode` specifies whether to start PostgreSQL as a standby.

During backup, `standby_mode` is off by default. This way, when all WAL is fetched, recovery completes and enters normal working mode.

If turned on, the database realizes it's a standby, so even when reaching the end of WAL, it won't stop but will continue fetching WAL from the master, catching up with the master's progress.

There are two ways to fetch WAL: through `primary_conninfo` streaming replication (new feature after 9.0, recommended, default), or through `restore_command` to manually specify WAL acquisition method (old method, used for recovery).

#### Check Status

All standbys of the master can be viewed through the system view `pg_stat_replication`:

```bash
$ psql postgres -tzxc 'SELECT * FROM pg_stat_replication;'
pid              | 1947
usesysid         | 16384
usename          | replication
application_name | walreceiver
client_addr      | ::1
client_hostname  |
client_port      | 54124
backend_start    | 2018-01-25 13:24:57.029203+08
backend_xmin     |
state            | streaming
sent_lsn         | 0/5017F88
write_lsn        | 0/5017F88
flush_lsn        | 0/5017F88
replay_lsn       | 0/5017F88
write_lag        |
flush_lag        |
replay_lag       |
sync_priority    | 0
sync_state       | async
```

Check master and standby status using function `pg_is_in_recovery`. Standby will be in recovery state:

```bash
$ psql postgres -Atzc 'SELECT pg_is_in_recovery()' && \
psql postgres -p 5433 -Atzc 'SELECT pg_is_in_recovery()'
f
t
```

Create table in master, standby can also see it:

```bash
psql postgres -c 'CREATE TABLE foobar(i INTEGER);' && psql postgres -p 5433 -c '\d'
```

Insert data in master, standby can also see it:

```bash
psql postgres -c 'INSERT INTO foobar VALUES (1);' && \
psql postgres -p 5433 -c 'SELECT * FROM foobar;'
```

Now master-standby is configured and ready.