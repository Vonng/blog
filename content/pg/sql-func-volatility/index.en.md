---
title: "Function Volatility Classification Levels"
date: 2018-04-06
author: "vonng"
summary: >
  PostgreSQL functions have three volatility levels by default. Proper use can significantly improve performance.
tags: [PostgreSQL, PG-Development, Functions]
---

PostgreSQL functions have three volatility levels by default. Proper use can significantly improve performance.

## Core Differences

* `VOLATILE`: Has side effects, cannot be optimized.
* `STABLE`: Executes database queries.
* `IMMUTABLE`: Pure function, execution results may be pre-evaluated and cached during planning.

## When to Use?

- `VOLATILE`: Any writes, any side effects, needs to see changes made by external commands, or calls any `VOLATILE` function
- `STABLE`: Has database queries but no writes, or function results depend on configuration parameters (e.g., timezone)
- `IMMUTABLE`: Pure function.

## Detailed Explanation

Each function carries a **volatility** level. Possible values include `VOLATILE`, `STABLE`, and `IMMUTABLE`. If no volatility level is specified when creating a function, it defaults to `VOLATILE`. Volatility is the function's promise to the optimizer:

- `VOLATILE` functions can do anything, including modifying database state. They may return different results on consecutive calls even with the same arguments. The optimizer won't optimize away such functions; they are re-evaluated every time they're called.
- `STABLE` functions cannot modify database state, and guarantee that given the same arguments within a **single statement**, they will return the same result. Therefore, the optimizer can optimize multiple calls with the same parameters into a single call. `STABLE` functions are allowed in index scan conditions, but `VOLATILE` functions are not. (In an index scan, comparison values are evaluated only once, not once per row, so `VOLATILE` functions cannot be used in index scan conditions).
- `IMMUTABLE` functions cannot modify database state and guarantee that given inputs will always return the same result at any time. This classification allows the optimizer to pre-compute the function when it's called with constant parameters in a query. For example, a query like `SELECT ... WHERE x = 2 + 2` can be simplified to `SELECT ... WHERE x = 4` because the underlying function of the integer addition operator is marked as `IMMUTABLE`.

## Difference Between STABLE and IMMUTABLE

### Call Count Optimization

Take this function as an example, which simply returns the constant 2:

```sql
CREATE OR REPLACE FUNCTION return2() RETURNS INTEGER AS
$$
BEGIN
RAISE NOTICE 'INVOKED';
RETURN 2;
END;
$$ LANGUAGE PLPGSQL STABLE;
```

When using the `STABLE` tag, it actually calls 10 times, but when using the `IMMUTABLE` tag, it's optimized to a single call.

```
vonng=# select return2() from generate_series(1,10);
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
NOTICE:  INVOKED
 return2
---------
       2
       2
       2
       2
       2
       2
       2
       2
       2
       2
(10 rows)
```

Here we change the function tag to `IMMUTABLE`:

```sql
CREATE OR REPLACE FUNCTION return2() RETURNS INTEGER AS
$$
BEGIN
RAISE NOTICE 'INVOKED';
RETURN 2;
END;
$$ LANGUAGE PLPGSQL IMMUTABLE;
```

Running the same query again, this time the function is called only once:

```sql
vonng=# select return2() from generate_series(1,10);
NOTICE:  INVOKED
 return2
---------
       2
       2
       2
       2
       2
       2
       2
       2
       2
       2
(10 rows)
```

### Execution Plan Caching

The second example concerns function calls in index conditions. Suppose we have a table containing integers from 1 to 1000:

```sql
create table demo as select * from generate_series(1,1000) as id;
create index idx_id on demo(id);
```

Now create an `IMMUTABLE` function `mymax`:

```sql
CREATE OR REPLACE FUNCTION mymax(int, int)
RETURNS int
AS $$
BEGIN
     RETURN CASE WHEN $1 > $2 THEN $1 ELSE $2 END;
END;
$$ LANGUAGE 'plpgsql' IMMUTABLE;
```

We'll find that when we use this function directly in index conditions, the index condition in the execution plan is directly evaluated, cached, and solidified as `id=2`:

```sql
vonng=# EXPLAIN SELECT * FROM demo WHERE id = mymax(1,2);
                               QUERY PLAN
------------------------------------------------------------------------
 Index Only Scan using idx_id on demo  (cost=0.28..2.29 rows=1 width=4)
   Index Cond: (id = 2)
(2 rows)
```

But if we change it to a `STABLE` function, the result becomes runtime evaluation:

```sql
vonng=# EXPLAIN SELECT * FROM demo WHERE id = mymax(1,2);
                               QUERY PLAN
------------------------------------------------------------------------
 Index Only Scan using idx_id on demo  (cost=0.53..2.54 rows=1 width=4)
   Index Cond: (id = mymax(1, 2))
(2 rows)
```