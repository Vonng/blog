---
title: "PostgreSQL Data Page Corruption Repair"
linkTitle: "Incident-Report: Data Page Corruption"
date: 2018-11-29
author: "vonng"
summary: "Using binary editing to repair PostgreSQL data pages, and how to make a primary key query return two records."
tags: ["PostgreSQL","PG-Admin","Data-Corruption","Incident-Report"]
---

PostgreSQL is a very reliable database, but even the most reliable database will struggle when faced with unreliable hardware. This article introduces methods for dealing with data page corruption in PostgreSQL.

## The Initial Problem

A statistics database running offline tasks in production encountered an error when business users ran SQL:

```bash
ERROR:  invalid page in block 18858877 of relation base/16400/275852
```

Seeing this error message, the first instinct is that it's a relational data file corruption caused by hardware errors. The first step is to check and locate the specific problem.

Here, 16400 is the database's oid, and 275852 is the table's `relfilenode`, usually equal to OID.

```sql
somedb=# select 275852::RegClass;
      regclass
---------------------
 dailyuseractivities
 
-- If relfilenode doesn't match oid, use the following query
somedb=# select relname from pg_class where pg_relation_filenode(oid) = '275852';
       relname
---------------------
 dailyuseractivities
(1 row)
```

After locating the problematic table, check the problematic page. The error indicates that the page with block number 18858877 has issues.

```sql
somedb=# select * from dailyuseractivities where ctid = '(18858877,1)';
ERROR:  invalid page in block 18858877 of relation base/16400/275852

-- Print detailed error location
somedb=# \errverbose
ERROR:  XX001: invalid page in block 18858877 of relation base/16400/275852
LOCATION:  ReadBuffer_common, bufmgr.c:917
```

Through inspection, we found that this page cannot be accessed, but the pages before and after it can be accessed normally. Using `errverbose` can print the source code location where the error occurred. Searching PostgreSQL source code, we find this error message appears in only one location: https://github.com/postgres/postgres/blob/master/src/backend/storage/buffer/bufmgr.c. We can see that the error occurs when the page is loaded from disk to the memory shared buffer. PostgreSQL considers this an invalid page, so it reports an error and aborts the transaction.

```c
/* check for garbage data */
if (!PageIsVerified((Page) bufBlock, blockNum))
{
    if (mode == RBM_ZERO_ON_ERROR || zero_damaged_pages)
    {
        ereport(WARNING,
                (errcode(ERRCODE_DATA_CORRUPTED),
                 errmsg("invalid page in block %u of relation %s; zeroing out page",
                        blockNum,
                        relpath(smgr->smgr_rnode, forkNum))));
        MemSet((char *) bufBlock, 0, BLCKSZ);
    }
    else
        ereport(ERROR,
                (errcode(ERRCODE_DATA_CORRUPTED),
                 errmsg("invalid page in block %u of relation %s",
                        blockNum,
                        relpath(smgr->smgr_rnode, forkNum))));
}
```

Further examining the logic of the `PageIsVerified` function:

```c
/* This check doesn't guarantee that the page header is correct, 
 * it just says it looks normal enough to allow loading into the buffer pool.
 * Subsequent actual use of the page may still fail, which is why
 * we provide the checksum option. */

if ((p->pd_flags & ~PD_VALID_FLAG_BITS) == 0 &&
    p->pd_lower <= p->pd_upper &&
    p->pd_upper <= p->pd_special &&
    p->pd_special <= BLCKSZ &&
    p->pd_special == MAXALIGN(p->pd_special))
    header_sane = true;

if (header_sane && !checksum_failure)
    return true;
```

Next, we need to specifically locate the problem. The first step is to find the position of the problematic page on disk. This is actually two sub-problems: which file it's in, and the offset address within the file. Here, the relation file's `relfilenode` is 275852. In PostgreSQL, each relation file is split into 1GB segment files by default, named according to the rule `relfilenode, relfilenode.1, relfilenode.2, ...`.

Therefore, we can calculate: the 18858877th page, each page 8KB, one segment file 1GB. The offset is `18858877 * 2^13 = 154491920384`.

```c
154491920384 / (1024^3) = 143
154491920384 % (1024^3) = 946839552 = 0x386FA000
```

Thus, the problematic page is located within the 143rd segment at offset `0x386FA000`.

This translates to the specific file `${PGDATA}/base/16400/275852.143`.

```bash
hexdump 275852.143 | grep -w10 386fa00

386f9fe0 003b 0000 0100 0000 0100 0000 4b00 07c8
386f9ff0 9b3d 5ed9 1f40 eb85 b851 44de 0040 0000
386fa000 0000 0000 0000 0000 0000 0000 0000 0000
*
386fb000 62df 3d7e 0000 0000 0452 0000 011f c37d
386fb010 0040 0003 0b02 0018 18f6 0000 d66a 0068
```

Using a binary editor to open and navigate to the corresponding offset, we found that the page content has been zeroed out and has no salvage value. Fortunately, online databases have at least a primary-replica configuration. If it's page corruption caused by bad blocks on the primary, the replica should still have the original data. Indeed, we can find the corresponding data on the replica:

```bash
386f9fe0:3b00 0000 0001 0000 0001 0000 004b c807  ;............K..
386f9ff0:3d9b d95e 401f 85eb 51b8 de44 4000 0000  =..^@...Q..D@...
386fa000:e3bd 0100 70c8 864a 0000 0400 f801 0002  ....p..J........
386fa010:0020 0420 0000 0000 c09f 7a00 809f 7a00  . . ......z...z.
386fa020:409f 7a00 009f 7a00 c09e 7a00 809e 7a00  @.z...z...z...z.
386fa030:409e 7a00 009e 7a00 c09d 7a00 809d 7a00  @.z...z...z...z.
```

Of course, if the page is normal, executing read operations on the replica won't report errors. Therefore, you can directly retrieve the corrupted data by filtering through `CTID`.

So far, although the data has been recovered, we can breathe a sigh of relief. But the bad block problem on the primary still needs to be handled. This is relatively simple - just rebuild the table and extract the latest data from the replica. There are various methods: `VACUUM FULL`, `pg_repack`, or manually rebuilding and copying data.

However, I noticed a parameter I'd never seen before in the code that determines page validity: `zero_damaged_pages`. Looking up the documentation, I found this is a developer debugging parameter that allows PostgreSQL to ignore corrupted data pages, treating them as all-zero empty pages. It uses WARNING instead of ERROR. This aroused my interest. After all, sometimes for some rough statistical business, having SQL that ran for several hours interrupted due to one or two dirty records might be more frustrating than missing those few records. Can this parameter meet such requirements?

> `zero_damaged_pages` (`boolean`)
>
> PostgreSQL normally reports an error and aborts the current transaction when it detects a corrupted page header. Setting `zero_damaged_pages` to `on` causes the system to instead report a warning and zero out the corrupted page in memory. However, this destroys data, meaning all rows on the corrupted page will be lost. But it does allow you to bypass the error and retrieve undamaged rows from uncorrupted pages in the table. This option is useful for recovering data when corruption is caused by software or hardware issues. Normally, you should only use this option when you've given up on recovering data from the corrupted pages. The zeroed pages are not forced to be written back to disk, so it's recommended to rebuild the corrupted table or index before turning off this option again. This option is off by default and can only be modified by superusers.

After all, when the table is rebuilt, the original bad blocks are released. If the hardware itself doesn't provide bad block identification and screening functionality, this becomes a time bomb that might cause problems again in the future. Unfortunately, the database on this machine is 14TB, using a 16TB SSD, and there are temporarily no machines of the same type available. We can only make do for now, so we need to research whether this parameter can allow queries to automatically skip bad pages when encountered.

## The Makeshift Solution

As follows, set up a test cluster locally, configure primary-replica. Try to reproduce the problem and determine:

```bash
# tear down
pg_ctl -D /pg/d1 stop
pg_ctl -D /pg/d2 stop
rm -rf /pg/d1 /pg/d2

# master @ port5432
pg_ctl -D /pg/d1 init
pg_ctl -D /pg/d1 start
psql postgres -c "CREATE USER replication replication;"

# slave @ port5433
pg_basebackup -Xs -Pv -R -D /pg/d2 -Ureplication 
pg_ctl -D /pg/d2 start -o"-p5433"
```

Connect to the primary, create a sample table and insert 555 records, occupying approximately three pages.

```sql
-- psql postgres
DROP TABLE IF EXISTS test;
CREATE TABLE test(id varchar(8) PRIMARY KEY);
ANALYZE test;

-- Note: after inserting data, must execute checkpoint to ensure disk persistence
INSERT INTO test SELECT generate_series(1,555)::TEXT;
CHECKPOINT;
```

Now, let's simulate bad block situation. First find the corresponding file for the `test` table in the primary.

```sql
SELECT pg_relation_filepath(oid) FROM pg_class WHERE relname = 'test';

base/12630/16385
```

```
$ hexdump /pg/d1/base/12630/16385 | head -n 20
0000000 00 00 00 00 d0 22 02 03 00 00 00 00 a0 03 c0 03
0000010 00 20 04 20 00 00 00 00 e0 9f 34 00 c0 9f 34 00
0000020 a0 9f 34 00 80 9f 34 00 60 9f 34 00 40 9f 34 00
0000030 20 9f 34 00 00 9f 34 00 e0 9e 34 00 c0 9e 36 00
0000040 a0 9e 36 00 80 9e 36 00 60 9e 36 00 40 9e 36 00
0000050 20 9e 36 00 00 9e 36 00 e0 9d 36 00 c0 9d 36 00
0000060 a0 9d 36 00 80 9d 36 00 60 9d 36 00 40 9d 36 00
0000070 20 9d 36 00 00 9d 36 00 e0 9c 36 00 c0 9c 36 00
```

We've already given the logic for PostgreSQL to determine whether a page is "normal". Here we'll modify the data page to make it "abnormal". Bytes 12-16 of the page, which are the last four bytes of the first line here `a0 03 c0 03`, are pointers to the upper and lower bounds of free space within the page. Interpreted in little-endian, this means that within this page, free space starts at `0x03A0` and ends at `0x03C0`. Logical free space ranges naturally need to satisfy upper bound ≤ lower bound. Here we'll modify the upper bound `0x03A0` to `0x03D0`, exceeding the lower bound `0x03C0`, i.e., changing the fourth-to-last byte of the first line from `A0` to `D0`.

```bash
# Open with vim and use :%!xxd to edit binary
# After editing, use :%!xxd -r to convert back to binary, then :wq to save
vi /pg/d1/base/12630/16385

# Check the result after modification
$ hexdump /pg/d1/base/12630/16385 | head -n 2
0000000 00 00 00 00 48 22 02 03 00 00 00 00 d0 03 c0 03
0000010 00 20 04 20 00 00 00 00 e0 9f 34 00 c0 9f 34 00
```

Here, although the page on disk has been modified, the page is already cached in the memory shared buffer pool. Therefore, from the primary database, we can still normally see results from page 1. Next, restart the primary to clear its buffer. Unfortunately, when the database is shut down or a checkpoint is executed, pages in memory will be flushed back to disk, overwriting our previously edited results. Therefore, first shut down the database, re-execute the edit, then start.

```bash
pg_ctl -D /pg/d1 stop
vi /pg/d1/base/12630/16385
pg_ctl -D /pg/d1 start

psql postgres -c 'select * from test;'
ERROR:  invalid page in block 0 of relation base/12630/16385

psql postgres -c "select * from test where id = '10';"
ERROR:  invalid page in block 0 of relation base/12630/16385

psql postgres -c "select * from test where ctid = '(0,1)';"
ERROR:  invalid page in block 0 of relation base/12630/16385

$ psql postgres -c "select * from test where ctid = '(1,1)';"
 id
-----
 227
```

We can see that the modified page 0 cannot be recognized by the database, but the unaffected page 1 can still be accessed normally.

Although queries on the primary fail due to page corruption, executing similar queries on the replica returns normal results:

```bash
$ psql -p5433 postgres -c 'select * from test limit 2;'
 id
----
 1
 2

$ psql -p5433 postgres -c "select * from test where id = '10';"
 id
----
 10

$ psql -p5433 postgres -c "select * from test where ctid = '(0,1)';"
 id
----
 1
(1 row)
```

Next, let's turn on the `zero_damaged_pages` parameter. Now queries on the primary don't error. Instead, there's a warning, data on page 0 evaporated, and returned results start from page 1.

```sql
postgres=# set zero_damaged_pages = on ;
SET
postgres=# select * from test;
WARNING:  invalid page in block 0 of relation base/12630/16385; zeroing out page
 id
-----
 227
 228
 229
 230
 231
```

Page 0 has indeed been loaded into the memory buffer pool, and the data in the page has been zeroed out.

```sql
create extension pg_buffercache ;

postgres=# select relblocknumber,isdirty,usagecount from pg_buffercache where relfilenode = 16385;
 relblocknumber | isdirty | usagecount
----------------+---------+------------
              0 | f       |          5
              1 | f       |          3
              2 | f       |          2
```

The `zero_damaged_pages` parameter needs to be configured at the instance level:

```bash
# Ensure this option is enabled by default and restart to take effect
psql postgres -c 'ALTER SYSTEM set zero_damaged_pages = on;'
pg_ctl -D /pg/d1 restart
psql postgres -c 'show zero_damaged_pages;'

zero_damaged_pages
--------------------
 on
```

Here, by configuring `zero_damaged_pages`, the primary can continue to cope even when encountering bad blocks.

After garbage pages are loaded into memory and zeroed, if a checkpoint is executed, will this all-zero page be flushed back to disk to overwrite the original data? This is very important because dirty data is still data with salvage value. Causing permanent irreversible loss for temporary convenience is certainly unacceptable.

```bash
psql postgres -c 'checkpoint;'
hexdump /pg/d1/base/12630/16385 | head -n 2
0000000 00 00 00 00 48 22 02 03 00 00 00 00 d0 03 c0 03
0000010 00 20 04 20 00 00 00 00 e0 9f 34 00 c0 9f 34 00
```

We can see that whether it's checkpoints or restarts, this all-zero page in memory won't forcibly replace the corrupted page on disk, leaving hope for recovery while ensuring online queries can continue. Excellent! This also matches the description in the documentation: "The zeroed pages are not forced to be written back to disk."

## A Subtle Problem

Just when I thought the experiment was complete and I could safely turn on this switch to cope temporarily, I suddenly remembered a subtle issue: the primary and replica read different data, which is quite awkward.

```bash
psql -p5432 postgres -Atqc 'select * from test limit 2;'
2018-11-29 22:31:20.777 CST [24175] WARNING:  invalid page in block 0 of relation base/12630/16385; zeroing out page
WARNING:  invalid page in block 0 of relation base/12630/16385; zeroing out page
227
228

psql -p5433 postgres -Atqc 'select * from test limit 2;'
1
2
```

More awkwardly, the primary cannot see tuples from page 0, meaning the primary thinks records from page 0 don't exist. Therefore, even with primary key constraints on the table, you can still insert records with the same primary key:

```bash
# The table already has a record with primary key id = 1, but the primary zeroed it out and can't see it!
psql postgres -c "INSERT INTO test VALUES(1);"
INSERT 0 1

# Querying from the replica, disaster! Primary key duplication!
psql postgres -p5433 -c "SELECT * FROM test;"

 id
-----
 1
 2
 3
...
 555
 1
 
# The id column is really the primary key...
$ psql postgres -p5433 -c "\d test;"
                      Table "public.test"
 Column |         Type         | Collation | Nullable | Default
--------+----------------------+-----------+----------+---------
 id     | character varying(8) |           | not null |
Indexes:
    "test_pkey" PRIMARY KEY, btree (id)
```

If we promote this replica to become the new primary, this problem still exists on the replica: one primary key can return two records! What a disaster...

Additionally, there's an interesting question: how will VACUUM handle such zero pages?

```bash
# Clean the table
psql postgres -c 'VACUUM VERBOSE;'

INFO:  vacuuming "public.test"
2018-11-29 22:18:05.212 CST [23572] WARNING:  invalid page in block 0 of relation base/12630/16385; zeroing out page
2018-11-29 22:18:05.212 CST [23572] WARNING:  relation "test" page 0 is uninitialized --- fixing
WARNING:  invalid page in block 0 of relation base/12630/16385; zeroing out page
WARNING:  relation "test" page 0 is uninitialized --- fixing
INFO:  index "test_pkey" now contains 329 row versions in 5 pages
DETAIL:  0 index row versions were removed.
0 index pages have been deleted, 0 are currently reusable.
CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s.
```

VACUUM "fixed" this page? But unfortunately, VACUUM taking it upon itself to fix dirty data pages isn't necessarily a good thing... Because when VACUUM completes the repair, this page is treated as a normal page and will be flushed back to disk during CHECKPOINT..., thereby overwriting the original dirty data. If this repair isn't the result you wanted, data may be lost.

## Summary

* Replication and backup are the best methods for dealing with hardware damage.
* When data page corruption occurs, you can find the corresponding physical page, compare it, and attempt repair.
* When page corruption prevents queries from proceeding, the parameter `zero_damaged_pages` can be used temporarily to skip errors.
* The parameter `zero_damaged_pages` is extremely dangerous
* When zeroing is enabled, corrupted pages are loaded into the memory buffer pool and zeroed, and won't overwrite the original disk pages during checkpoints.
* Pages zeroed in memory will be attempted to be repaired by VACUUM, and repaired pages will be flushed back to disk by checkpoints, overwriting original pages.
* Content in zeroed pages is invisible to the database, so constraint violations may occur.