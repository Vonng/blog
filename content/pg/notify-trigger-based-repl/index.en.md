---
title: "Implementing Cache Synchronization with Go and PostgreSQL"
linkTitle: "Implementing Cache Synchronization with Go and PostgreSQL"
date: 2017-08-03
author: "vonng"
summary: "Cleverly utilizing PostgreSQL's Notify feature, you can conveniently notify applications of metadata changes and implement trigger-based logical replication."
tags: ["PostgreSQL","PG-Development","Triggers"]
---

Parallel and Hierarchy are the two great principles of architectural design, and **caching** is the embodiment of Hierarchy in the IO domain. Implementing caching mechanisms in single-threaded scenarios can be surprisingly simple, but it's hard to imagine mature applications having only one instance. When introducing concurrency while using caches, one must consider a problem: how to ensure data consistency (and real-time nature) between each instance's cache and the underlying data replicas.

PostgreSQL introduced streaming replication in version 9 and logical replication in version 10, but these are all for PostgreSQL databases. If we want partial data from a PostgreSQL table to remain consistent with the state in application memory, we still need to implement our own logical replication mechanism. For critical small amounts of metadata, using triggers and Notify-Listen is a good choice.

----------------

## Traditional Methods

The simplest brute-force approach is to regularly re-fetch data, for example, every hour, all applications go to the database together to pull the latest version of data. Many applications do this. Of course, there are many problems: if the pull interval is long, changes can't be applied promptly, resulting in poor user experience; if pulled frequently, IO pressure is high. Moreover, once the number of instances and data size expand, it's a huge waste of precious IO resources.

Asynchronous notification is a better approach, especially when read requests far exceed write requests. The instance receiving write requests notifies other instances by broadcasting. Redis's PubSub can implement this functionality very well. If the underlying storage is already Redis, this is naturally very convenient, but if the underlying storage is a relational database, introducing a new component for such functionality seems somewhat counterproductive. Moreover, considering that backend management programs or other applications would also need to publish notifications to Redis after modifying the database, it's really too troublesome. One feasible approach is to monitor RDS changes and broadcast notifications through database middleware - many things at Taobao work this way. But if the DB itself can handle things, why need additional components? Through PostgreSQL's Notify-Listen mechanism, this functionality can be conveniently implemented.

----------------

## Objective

Any database record changes (insert, delete, update) generated through any channel should be perceived in real-time by all related applications, for maintaining consistency between their own cache and database content.

----------------

## Principle

PostgreSQL row-level triggers + Notify mechanism + custom protocol + Smart Client

* Row-level triggers: By creating a row-level write trigger for tables we're interested in, every Update, Delete, Insert operation on each record in the data table will trigger execution of a custom function.
* Notify: Send notifications to specified channels through PostgreSQL's built-in asynchronous notification mechanism
* Custom protocol: Negotiate message format, transmit operation types and identifiers of changed records
* Smart Client: Client listens for message changes and performs corresponding operations on the cache based on messages.

Actually, such a system is a super-simplified WAL (Write *After* Log) implementation, allowing application internal cache states to maintain *real-time* consistency with the database (compare to poll).

----------------

## DDL

Here we use the simplest table as an example, a `users` table identified by primary key.

```sql
-- Users table
CREATE TABLE users (
  id   TEXT,
  name TEXT,
  PRIMARY KEY (id)
);
```

----------------

## Triggers

```sql
-- Notification trigger
CREATE OR REPLACE FUNCTION notify_change() RETURNS TRIGGER AS $$
BEGIN
  IF    (TG_OP = 'INSERT') THEN 
	PERFORM pg_notify(TG_RELNAME || '_chan', 'I' || NEW.id); RETURN NEW;
  ELSIF (TG_OP = 'UPDATE') THEN 
	PERFORM pg_notify(TG_RELNAME || '_chan', 'U' || NEW.id); RETURN NEW;
  ELSIF (TG_OP = 'DELETE') THEN 
	PERFORM pg_notify(TG_RELNAME || '_chan', 'D' || OLD.id); RETURN OLD;
  END IF;
END; $$ LANGUAGE plpgsql SECURITY DEFINER;
```

Here we created a trigger function that gets operation names through built-in variable `TG_OP` and table names through `TG_RELNAME`. Whenever the trigger executes, it sends messages in specified format to a channel named `<table_name>_chan`: `[I|U|D]<id>`

Sidebar: Through row-level triggers, you can also implement some very practical features, such as In-DB Audit, automatic field value updates, statistics information, custom backup strategies and rollback logic, etc.

```sql
-- Create row-level trigger for users table, listening to INSERT UPDATE DELETE operations.
CREATE TRIGGER t_user_notify AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE PROCEDURE notify_change();
```

Creating triggers is also simple. Table-level triggers execute once per table change, while row-level triggers execute once per record. With this, all the work in the database is complete.

----------------

## Message Format

Notifications need to convey two pieces of information: the type of change operation and the identifier of the changed entity.

* The type of change operation is insert, delete, update: INSERT, DELETE, UPDATE. This can be identified by a leading character '[I|U|D]'.
* The changed object can be identified by entity primary key. If it's not a string type, you also need to determine an unambiguous serialization method.

Here, for simplicity, we directly use string type as ID. So inserting a record with `id=1` corresponds to message `I1`, updating a record with `id=5` corresponds to message `U5`, and deleting a record with `id=3` corresponds to message `D3`.

More powerful functionality can be implemented through more complex message protocols.

----------------

## Smart Client

Database mechanisms need client cooperation to take effect. Clients need to listen for database change notifications to apply changes to their own cache replicas in real-time. For inserts and updates, clients need to re-fetch corresponding entities based on ID. For deletes, clients need to delete corresponding entities from their cache replicas. Taking Go language as an example, we wrote a simple client module.

In this example, we use a concurrency-safe dictionary `Users sync.Map` as cache, with `User.ID` as key and `User` objects as values.

For demonstration, we started another goroutine that writes some changes to the database.

```go
package main

import "sync"
import "strings"
import "github.com/go-pg/pg"
import . "github.com/Vonng/gopher/db/pg"
import log "github.com/Sirupsen/logrus"

type User struct {
	ID   string `sql:",pk"`
	Name string
}

var Users sync.Map // Users internal data cache

func LoadAllUser() {
	var users []User
	Pg.Query(&users, `SELECT ID,name FROM users;`)
	for _, user := range users {
		Users.Store(user.ID, user)
	}
}

func LoadUser(id string) {
	user := User{ID: id}
	Pg.Select(&user)
	Users.Store(user.ID, user)
}

func PrintUsers() string {
	var buf []string
	Users.Range(func(key, value interface{}) bool {
		buf = append(buf, key.(string));
		return true
	})
	return strings.Join(buf, ",")
}

// ListenUserChange listens for change notifications in PostgreSQL users table
func ListenUserChange() {
	go func(c <-chan *pg.Notification) {
		for notify := range c {
			action, id := notify.Payload[0], notify.Payload[1:]
			switch action {
			case 'I':
				fallthrough
			case 'U':
				LoadUser(id);
			case 'D':
				Users.Delete(id)
			}
			log.Infof("[NOTIFY] Action:%c ID:%s Users: %s", action, id, PrintUsers())
		}
	}(Pg.Listen("users_chan").Channel())
}

// MakeSomeChange writes some changes to the database
func MakeSomeChange() {
	go func() {
		Pg.Insert(&User{"001", "Zhang San"})
		Pg.Insert(&User{"002", "Li Si"})
		Pg.Insert(&User{"003", "Wang Wu"})  // insert
		Pg.Update(&User{"003", "Wang Mazi"}) // rename
		Pg.Delete(&User{ID: "002"})    // delete
	}()
}

func main() {
	Pg = NewPg("postgres://localhost:5432/postgres")
	Pg.Exec(`TRUNCATE TABLE users;`)
	LoadAllUser()
	ListenUserChange()
	MakeSomeChange()
	<-make(chan struct{})
}
```

The running result is as follows:

```
[NOTIFY] Action:I ID:001 Users: 001          
[NOTIFY] Action:I ID:002 Users: 001,002      
[NOTIFY] Action:I ID:003 Users: 002,003,001  
[NOTIFY] Action:U ID:003 Users: 001,002,003  
[NOTIFY] Action:D ID:002 Users: 001,003      
```

You can see that the cache indeed maintained the same state as the database.

----------------

## Application Scenarios

This approach is quite reliable for small data volumes, but hasn't been thoroughly tested for large data volumes.

Actually, for the cache synchronization scenario in the above example, there's no need for custom message formats at all. Just send the ID of the changed record, have the application directly fetch it, then overwrite or delete the record in the cache.