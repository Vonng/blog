---
title: "Incident Report: PostgreSQL Transaction ID Wraparound"
date: 2018-07-20
author: "vonng"
summary: >
  XID WrapAround is perhaps a unique type of failure specific to PostgreSQL
tags: [PostgreSQL, PG Management, Incident Report]
---

Encountered a transaction wraparound failure caused by disk bad blocks:

* Primary database (PostgreSQL 9.3) disk bad blocks caused VACUUM FREEZE execution failure on several tables.
* Unable to reclaim old transaction IDs, causing database transaction IDs to near exhaustion, database entered self-protection state and became unavailable.
* Disk bad blocks made manual VACUUM rescue infeasible.
* After promoting standby, emergency VACUUM FREEZE was needed to continue service, further extending failure time.
* After primary entered protection state, commit log (clog) wasn't replicated to standby in time, standby generated dubious transactions and refused service.

----------------

## Summary

This was an old database about to be decommissioned, poorly managed. Bad block symptoms appeared a week ago but age wasn't monitored in time.
Usually AutoVacuum ensures this type of failure is unlikely, but once it occurs it often means when it rains, it pours... making firefighting even more difficult...

----------------

## Background

PostgreSQL implements **Snapshot Isolation**, where each transaction can get a database snapshot at the moment it begins (i.e., it can only see results committed by **past** transactions, not results committed by **subsequent** transactions). This powerful feature is implemented through MVCC, but introduces additional complexity, such as **transaction ID wraparound** issues.

Transaction ID (`xid`) is a **32-bit unsigned integer** used to identify transactions, allocated incrementally, where values 0,1,2 are reserved. After overflow, it wraps around back to 3. **The size relationship between transaction IDs determines transaction order**.

```c
/*
 * TransactionIdPrecedes --- is id1 logically < id2?
 */
bool
TransactionIdPrecedes(TransactionId id1, TransactionId id2)
{
	/*
	 * If either ID is a permanent XID then we can just do unsigned
	 * comparison.  If both are normal, do a modulo-2^32 comparison.
	 */
	int32		diff;

	if (!TransactionIdIsNormal(id1) || !TransactionIdIsNormal(id2))
		return (id1 < id2);

	diff = (int32) (id1 - id2);
	return (diff < 0);
}
```

![xid-wrap-around](xid-wrap-around.png)

You can view `xid`'s value domain as an integer ring, excluding the three special values `0,1,2`. 0 represents invalid transaction ID, 1 represents system transaction ID, 2 represents frozen transaction ID. Special transaction IDs are smaller than any normal transaction ID. Comparison between normal transaction IDs can be seen in the figure above: it depends on whether the difference between two transaction IDs exceeds `INT32_MAX`. For any transaction ID, there are about 2.1 billion transactions in the past and 2.1 billion transactions in the future.

xid doesn't just exist in active transactions; xid affects all tuples: transactions mark tuples they affect with their own xid as a tag. Each tuple uses `(xmin, xmax)` to identify its visibility. `xmin` records the transaction ID that last wrote (`INSERT`, `UPDATE`) the tuple, while `xmax` records the transaction ID that deleted or locked the tuple. Each transaction can only see tuples committed by previous transactions (`xmin < xid`) and not deleted (thus implementing snapshot isolation).

If a tuple was produced by a very old transaction, during routine database VACUUM FREEZE, it will find the oldest xid among current active transactions and mark all tuples with `xmin < xid` as `xmin = 2`, i.e., frozen transaction ID. This means the tuple jumps out of this comparison ring, becoming smaller than all normal transaction IDs, so it can be seen by all transactions. Through cleanup, the oldest xid in the database continuously catches up with the current xid, avoiding transaction wraparound.

Database or table **age** is defined as the difference between current transaction ID and the oldest `xid` existing in the database/table. The oldest `xid` might come from a multi-day long-running transaction, or from tuples written by old transactions days ago but not yet frozen. If database age exceeds `INT32_MAX`, catastrophic situation occurs. Past transactions become future transactions, and tuples written by past transactions become invisible.

To avoid this situation, we need to avoid **long-running transactions** and regularly VACUUM FREEZE old tuples. If a single database runs under extremely high load averaging 30K TPS, 2 billion transaction numbers would be exhausted within a day. On such databases, you cannot execute long-running transactions exceeding one day. If for some reason automatic cleanup cannot continue, transaction wraparound could occur within a day.

After 9.4, the FREEZE mechanism was modified to use separate flag bits in tuples.

PostgreSQL has self-protection mechanisms against transaction wraparound. When critical transaction numbers have **ten million** left, it enters emergency state.

## Queries

Query current age of all tables with the following SQL:

```sql
SELECT c.oid::regclass as table_name,
     greatest(age(c.relfrozenxid),age(t.relfrozenxid)) as age
FROM pg_class c
LEFT JOIN pg_class t ON c.reltoastrelid = t.oid
WHERE c.relkind IN ('r', 'm') order by 2 desc;
```

Query database age with the following SQL:

```sql
SELECT *, age(datfrozenxid) FROM pg_database; 
```

#### Cleanup

Execute `VACUUM FREEZE` to freeze old transaction IDs:

```sql
set vacuum_cost_limit = 10000;
set vacuum_cost_delay = 0;

VACUUM FREEZE VERBOSE;
```

You can target specific tables for VACUUM FREEZE, focusing on main issues.

## Problems

Usually, PostgreSQL's AutoVacuum mechanism automatically executes FREEZE operations, freezing old transaction IDs to reduce database age. Therefore, once transaction ID wraparound failure occurs, it usually means when it rains, it pours, indicating vacuum mechanism might be blocked by other failures.

Currently encountered three situations that trigger transaction ID wraparound failures:

### IDLE IN TRANSACTION

Idle transactions block VACUUM FREEZE of old tuples.

Solution is simple: kill IDLE IN TRANSACTION long transactions then execute VACUUM FREEZE.

### Dubious Transactions

clog corruption or not replicated to standby causes related tables to enter dubious transaction state, refusing service.

Need manual copying or using dd to generate virtual clog for forced escape.

### Disk/Memory Bad Blocks

VACUUM failure due to bad blocks is awkward.

Need to use binary search to locate and skip dirty data, or directly rescue standby.

### Notes

During emergency rescue, don't do the whole database at once - cleaning tables individually in descending age order is faster.

Note that when primary enters transaction wraparound protection state, standby faces the same problem.

## Solutions

### AutoVacuum Parameter Configuration

### Age Monitoring

[To be continued]