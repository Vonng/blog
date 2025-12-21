---
title: "Bash and psql Tips"
date: 2018-04-07
author: "vonng"
summary: "Some tips for interacting between PostgreSQL and Bash."
tags: [PostgreSQL, "PG-Admin", Tools]
---

Some tips for interacting between PostgreSQL and Bash.

## Using Strict Mode for Bash Scripts

Using [Bash strict mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/) can avoid many unnecessary errors. It's useful to put this line at the beginning of Bash scripts:

```bash
set -euo pipefail
```

- `-e`: Exit with error when program returns non-zero status code
- `-u`: Report error when using uninitialized variables instead of treating them as NULL
- `-o pipefail`: Use the status code of the failing command in a pipe (rather than the last one) as the overall pipe status code[^i].

[^i]: Exit statuses of pipe programs are placed in the environment variable array `PIPESTATUS`

## Bash Wrapper Script for Executing SQL Scripts

When running SQL scripts through psql, we want these two features:

1. Ability to pass variables into scripts
2. Script stops immediately after error (instead of default behavior of continuing execution)

Here's a practical example that includes both features above. Use a Bash script wrapper to pass in two parameters.

```bash
#!/usr/bin/env bash
set -euo pipefail

if [ $# != 2 ]; then
    echo "please enter a db host and a table suffix"
    exit 1
fi

export DBHOST=$1
export TSUFF=$2

psql \
    -X \
    -U user \
    -h $DBHOST \
    -f /path/to/sql/file.sql \
    --echo-all \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --set TSUFF=$TSUFF \
    --set QTSTUFF=\'$TSUFF\' \
    mydatabase

psql_exit_status=$?

if [ $psql_exit_status != 0 ]; then
    echo "psql failed while trying to run this sql script" 1>&2
    exit $psql_exit_status
fi

echo "sql script successful"
exit 0
```

Key points:

- The `TSTUFF` parameter is passed into the SQL script both as a bare value and as a single-quote surrounded value, so the bare value can be used as table names, schema names, and the quoted value can be used as string values.
- Use `-X` option to ensure the current user's `.psqlrc` file isn't automatically loaded
- Print all messages to console so you can see script execution status (very useful when things fail)
- Use `ON_ERROR_STOP` option to terminate immediately when problems occur.
- Turn off `AUTOCOMMIT`, so the SQL script file doesn't commit every line. Instead, it only commits when `COMMIT` appears in the SQL script. If you want the entire script to commit as one transaction, add `COMMIT` at the last line of the sql script (don't add elsewhere), otherwise the entire script will run successfully but commit nothing (auto-rollback). You can also use the `--single-transaction` flag to achieve this.

The content of `/path/to/sql/file.sql`:

```sql
begin;
drop index this_index_:TSUFF;
commit;

begin;
create table new_table_:TSUFF (
    greeting text not null default '');
commit;

begin;
insert into new_table_:TSUFF (greeting)
values ('Hello from table ' || :QTSUFF);
commit;
```

## Using PG Environment Variables to Make Scripts More Concise

Using PG environment variables is very convenient, for example using `PGUSER` instead of `-U <user>`, `PGHOST` instead of `-h <host>`. Users can switch data sources by modifying environment variables. You can also provide default values for these environment variables through Bash.

```bash
#!/bin/bash

set -euo pipefail

# Set these environmental variables to override them,
# but they have safe defaults.
export PGHOST=${PGHOST-localhost}
export PGPORT=${PGPORT-5432}
export PGDATABASE=${PGDATABASE-my_database}
export PGUSER=${PGUSER-my_user}
export PGPASSWORD=${PGPASSWORD-my_password}

RUN_PSQL="psql -X --set AUTOCOMMIT=off --set ON_ERROR_STOP=on "

${RUN_PSQL} <<SQL
select blah_column 
  from blahs 
 where blah_column = 'foo';
rollback;
SQL
```

## Executing a Series of SQL Commands in a Single Transaction

You have a script full of SQL and want to execute the entire script as a single transaction. A common situation is forgetting to add a `COMMIT` line at the end. One solution is to use the `—single-transaction` flag:

```bash
psql \
    -X \
    -U myuser \
    -h myhost \
    -f /path/to/sql/file.sql \
    --echo-all \
    --single-transaction \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    mydatabase
```

The content of `file.sql` becomes:

```bash
insert into foo (bar) values ('baz');
insert into yikes (mycol) values ('hello');
```

Both inserts will be wrapped in the same `BEGIN/COMMIT` pair.

## Making Multi-line SQL Statements More Beautiful

```bash
#!/usr/bin/env bash
set -euo pipefail

RUN_ON_MYDB="psql -X -U myuser -h myhost --set ON_ERROR_STOP=on --set AUTOCOMMIT=off mydb"

$RUN_ON_MYDB <<SQL
drop schema if exists new_my_schema;
create table my_new_schema.my_new_table (like my_schema.my_table);
create table my_new_schema.my_new_table2 (like my_schema.my_table2);
commit;
SQL

# Using ' to surround the delimiter means the content in the HereDocument won't be escaped by Bash.
$RUN_ON_MYDB <<'SQL'
create index my_new_table_id_idx on my_new_schema.my_new_table(id);
create index my_new_table2_id_idx on my_new_schema.my_new_table2(id);
commit;
SQL
```

You can also use Bash tricks to assign multi-line statements to variables and use them later.

Note that Bash automatically clears newlines in multi-line input. Actually, the entire HereDocument content is reformatted to one line during transmission, so you need to add appropriate delimiters, like semicolons, to avoid format corruption.

```bash
CREATE_MY_TABLE_SQL=$(cat <<EOF
    create table foo (
        id bigint not null,
        name text not null
    );
EOF
)

$RUN_ON_MYDB <<SQL
$CREATE_MY_TABLE_SQL
commit;
SQL
```

## How to Assign a Single SELECT Scalar Result to a Bash Variable

```bash
CURRENT_ID=$($PSQL -X -U $PROD_USER -h myhost -P t -P format=unaligned $PROD_DB -c "select max(id) from users")
let NEXT_ID=CURRENT_ID+1
echo "next user.id is $NEXT_ID"

echo "about to reset user id sequence on other database"
$PSQL -X -U $DEV_USER $DEV_DB -c "alter sequence user_ids restart with $NEXT_ID"
```

## How to Assign Single Row Results to Bash Variables

And each variable is named after the column name.

```bash
read username first_name last_name <<< $(psql \
    -X \
    -U myuser \
    -h myhost \
    -d mydb \
    --single-transaction \
    --set ON_ERROR_STOP=on \
    --no-align \
    -t \
    --field-separator ' ' \
    --quiet \
    -c "select username, first_name, last_name from users where id = 5489")

echo "username: $username, first_name: $first_name, last_name: $last_name"
```

You can also use arrays:

```bash
#!/usr/bin/env bash
set -euo pipefail

declare -a ROW=($(psql \
    -X \
    -h myhost \
    -U myuser \
    -c "select username, first_name, last_name from users where id = 5489" \
    --single-transaction \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --no-align \
    -t \
    --field-separator ' ' \
    --quiet \
    mydb))

username=${ROW[0]}
first_name=${ROW[1]}
last_name=${ROW[2]}

echo "username: $username, first_name: $first_name, last_name: $last_name"
```

## How to Iterate Over Query Result Sets in Bash Scripts

```bash
#!/usr/bin/env bash
set -euo pipefail
PSQL=/usr/bin/psql

DB_USER=myuser
DB_HOST=myhost
DB_NAME=mydb

$PSQL \
    -X \
    -h $DB_HOST \
    -U $DB_USER \
    -c "select username, password, first_name, last_name from users" \
    --single-transaction \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --no-align \
    -t \
    --field-separator ' ' \
    --quiet \
    -d $DB_NAME \
| while read username password first_name last_name ; do
    echo "USER: $username $password $first_name $last_name"
done
```

You can also read into arrays:

```bash
#!/usr/bin/env bash
set -euo pipefail

PSQL=/usr/bin/psql

DB_USER=myuser
DB_HOST=myhost
DB_NAME=mydb

$PSQL \
    -X \
    -h $DB_HOST \
    -U $DB_USER \
    -c "select username, password, first_name, last_name from users" \
    --single-transaction \
    --set AUTOCOMMIT=off \
    --set ON_ERROR_STOP=on \
    --no-align \
    -t \
    --field-separator ' ' \
    --quiet \
    $DB_NAME | while read -a Record ; do

    username=${Record[0]}
    password=${Record[1]}
    first_name=${Record[2]}
    last_name=${Record[3]}

    echo "USER: $username $password $first_name $last_name"
done
```

## How to Use Status Tables to Control Multiple PG Tasks

Suppose you have such a large job that you want to do it one thing at a time. You decide to do one task at a time, which is easier on the database than executing one long-running query. You create a table called my_schema.items_to_process containing item_id for each item to be processed, and you add a column called done to the items_to_process table that defaults to false. Then, you can use a script to get each unfinished item from items_to_process, process it, then update that item in items_to_process to done = true. A bash script can do this:

```bash
#!/usr/bin/env bash
set -euo pipefail

PSQL="/u99/pgsql-9.1/bin/psql"
DNL_TABLE="items_to_process"
#DNL_TABLE="test"
FETCH_QUERY="select item_id from my_schema.${DNL_TABLE} where done is false limit 1"

process_item() {
    local item_id=$1
    local dt=$(date)
    echo "[${dt}] processing item_id $item_id"
    $PSQL -X -U myuser -h myhost -c "insert into my_schema.thingies select thingie_id, salutation, name, ddr from thingies where item_id = $item_id and salutation like 'Mr.%'" mydb
}

item_id=$($PSQL -X -U myuser -h myhost -P t -P format=unaligned -c "${FETCH_QUERY}" mydb)
dt=$(date)
while [ -n "$item_id" ]; do
    process_item $item_id
    echo "[${dt}] marking item_id $item_id as done..."
    $PSQL -X -U myuser -h myhost -c "update my_schema.${DNL_TABLE} set done = true where item_id = $item_id" mydb
    item_id=$($PSQL -X -U myuser -h myhost -P t -P format=unaligned -c "${FETCH_QUERY}" mydb)
    dt=$(date)
done
```

## Cross-Database Table Copying

There are many ways to achieve this. Using `psql`'s `\copy` command is probably the simplest. Suppose you have two databases `olddb` and `newdb`, and there's a `users` table that needs to be synced from the old database to the new database. How to do it with one command:

```bash
psql \
    -X \
    -U user \
    -h oldhost \
    -d olddb \
    -c "\\copy users to stdout" \
| \
psql \
    -X \
    -U user \
    -h newhost \
    -d newdb \
    -c "\\copy users from stdin"
```

A more difficult example: suppose your table has three columns in the old database: `first_name`, `middle_name`, `last_name`.

But in the new database there are only two columns, `first_name`, `last_name`, you can use:

```bash
psql \
    -X \
    -U user \
    -h oldhost \
    -d olddb \
    -c "\\copy (select first_name, last_name from users) to stdout" \
| \
psql \
    -X \
    -U user \
    -h newhost \
    -d newdb \
    -c "\\copy users from stdin"
```

## Ways to Get Table Definitions

```bash
pg_dump \
    -U db_user \
    -h db_host \
    -p 55432 \
    --table my_table \
    --schema-only my_db
```

## Exporting Binary Data from bytea Columns to Files

Note that `bytea` columns in PostgreSQL 9.0+ are represented in hexadecimal with an annoying `\x` prefix, which can be removed with `substring`.

```bash
#!/usr/bin/env bash
set -euo pipefail

psql \
    -P t \
    -P format=unaligned \
    -X \
    -U myuser \
    -h myhost \
    -c "select substring(my_bytea_col::text from 3) from my_table where id = 12" \
    mydb \
| xxd -r -p > dump.txt
```

## Inserting File Contents as a Column Value

There are two approaches to accomplish this: first is building SQL externally, second is using it as a variable in scripts.

```sql
CREATE TABLE sample(
	filename	INTEGER,
    value		JSON
);
```

```bash
psql <<SQL
\set content `cat ${filename}`
INSERT INTO sample VALUES(\'${filename}\',:'content')
SQL
```

## Displaying Statistics for Specific Tables in Specific Databases

```bash
#!/usr/bin/env bash
set -euo pipefail
if [ -z "$1" ]; then
    echo "Usage: $0 table [db]"
    exit 1
fi

SCMTBL="$1"
SCHEMANAME="${SCMTBL%%.*}"  # everything before the dot (or SCMTBL if there is no dot)
TABLENAME="${SCMTBL#*.}"  # everything after the dot (or SCMTBL if there is no dot)

if [ "${SCHEMANAME}" = "${TABLENAME}" ]; then
    SCHEMANAME="public"
fi

if [ -n "$2" ]; then
    DB="$2"
else
    DB="my_default_db"
fi

PSQL="psql -U my_default_user -h my_default_host -d $DB -x -c "

$PSQL "
select '-----------' as \"-------------\", 
       schemaname,
       tablename,
       attname,
       null_frac,
       avg_width,
       n_distinct,
       correlation,
       most_common_vals,
       most_common_freqs,
       histogram_bounds
  from pg_stats
 where schemaname='$SCHEMANAME'
   and tablename='$TABLENAME';
" | grep -v "\-\[ RECORD "
```

Usage:

```bash
./table-stats.sh myschema.mytable
```

For tables in the public schema:

```bash
./table-stats.sh mytable
```

Connecting to other databases:

```bash
./table-stats.sh mytable myotherdb
```

## Converting psql Default Output to Markdown Tables

```bash
alias pg2md=' sed '\''s/+/|/g'\'' | sed '\''s/^/|/'\'' | sed '\''s/$/|/'\'' |  grep -v rows | grep -v '\''||'\'''

# Usage
psql -c 'SELECT * FROM pg_database' | pg2md
```

The resulting output can be pasted into Markdown editors.