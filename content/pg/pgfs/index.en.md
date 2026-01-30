---
title: "PGFS: Using Database as a Filesystem"
linkTitle: "PGFS: Using Database as a Filesystem"
date: 2025-03-21
author: vonng 
summary: Leverage JuiceFS to turn PostgreSQL into a filesystem with PITR capabilities!
tags: [PostgreSQL,JuiceFS]
---

A few days ago, I received a request from the Odoo community asking: "Databases support PITR (Point-in-Time Recovery), but is there a way to roll back the filesystem as well?"

------

### Why the "PGFS" Idea?

From a veteran database engineer's perspective, this is both a challenging and exciting question. We all know that for ERP systems like Odoo, the most valuable asset is indeed the core business data stored in a PostgreSQL database.

However, many "enterprise applications" inevitably deal with file operations - uploading attachments, storing images and documents, etc. While these files may not be as "mission-critical" as database data, having them rollback to the same point in time as the database would be excellent from security, data integrity, and convenience perspectives.

This led me to an interesting thought: **Is there a way to give filesystems PITR capabilities similar to databases?** Traditional approaches mostly point to expensive and complex CDP (Continuous Data Protection) solutions that require hardware appliances or block-level logging at the storage layer. But I wondered: for "poor folks," could we solve this problem more cleverly using open-source technologies?

After much consideration, a combination that made me "slap my forehead" emerged: JuiceFS + PostgreSQL. By transforming PG into a filesystem, all file writes would enter the database, sharing the same WAL logs and enabling rollback to any historical point in time. This sounds fantastical, but don't worry - it actually "works." Let's see how JuiceFS accomplishes this.

------

## Meet JuiceFS: Turning Database into Filesystem

[JuiceFS](https://juicefs.com/en/) is a high-performance, cloud-native distributed filesystem that can mount object storage (like S3/MinIO) as a local POSIX filesystem. It's extremely lightweight to install and use, requiring just a few commands for formatting, mounting, and read/write operations.

For example, these commands can use SQLite as JuiceFS's metadata store and use local paths as object storage for testing:

```bash
juicefs format sqlite3:/tmp/jfs.db myjfs     # Use SQLite3 for metadata, local FS for data
juicefs mount sqlite3:/tmp/jfs.db ~/jfs -d   # Mount this filesystem to ~/jfs 
```

**The magic is**: JuiceFS also supports using PostgreSQL as both **metadata** and **object data** storage backend! This means you only need to change JuiceFS's backend to an existing PostgreSQL instance to get a database-based "filesystem."

So if you have an existing PostgreSQL database (installed via Pigsty single-node setup, for example), you can spin up a "PGFS" with one command:

```bash
# Metadata engine URL (PostgreSQL connection string)
METAURL="postgres://dbuser_meta:DBUser.Meta@10.10.10.10:5432/meta"

# Format JuiceFS filesystem using PostgreSQL as metadata and data storage
juicefs format \
  --storage postgres \
  --bucket 10.10.10.10:5432/meta \
  --access-key dbuser_meta \
  --secret-key DBUser.Meta \
  "${METAURL}" jfs

# Mount filesystem to /data2 directory
juicefs mount "${METAURL}" /data2 -d

# Test performance
juicefs bench /data2

# Unmount
juicefs umount /data2
```

This way, any data written to the /data2 directory actually gets stored in PG's `jfs_blob` table. In other words, this filesystem and the PG database have become one!

------

## PGFS in Action: Filesystem PITR

Imagine we have an Odoo system that needs to store file data in directories like `/var/lib/odoo`. Traditionally, if we needed to restore Odoo's database to a previous point in time, while the database could use WAL logs for point-in-time recovery, the filesystem would still rely on external snapshots or CDP.

**But now, if we mount `/var/lib/odoo` on PGFS**, all filesystem write operations become database write operations. The database no longer just stores SQL data - it simultaneously carries filesystem information. This means: when I perform PITR, not only can the database return to a certain point in time, **but files can instantly "travel back with the database" to the same moment**.

Some might ask, doesn't ZFS support snapshots too? Yes, ZFS can create snapshots and rollback, but that's still based on specific snapshot points. For precision down to specific seconds or minutes, you need true log-based solutions or CDP functionality. The JuiceFS+PG combination essentially writes file operation logs into the database's WAL, which is exactly what PostgreSQL excels at naturally.

The following experimental workflow demonstrates everything. We write timestamps to the filesystem in a loop while continuously inserting heartbeat records into the database:

```bash
while true; do date "+%H-%M-%S" >> /data2/ts.log; sleep 1; done
/pg/bin/pg-heartbeat   # Generate database heartbeat records
tail -f /data2/ts.log
```

Then, verify the JuiceFS table in PostgreSQL:

```bash
postgres@meta:5432/meta=# SELECT min(modified),max(modified) FROM jfs_blob;
min             |            max
----------------------------+----------------------------
 2025-03-21 02:26:00.322397 | 2025-03-21 02:40:45.688779
```

When we decide to rollback to, say, one minute ago (`2025-03-21 02:39:00`), we simply execute:

```bash
pg-pitr --time="2025-03-21 02:39:00"  # Use pgbackrest to rollback to specific time, actual command:
pgbackrest --stanza=pg-meta --type=time --target='2025-03-21 02:39:00+00' restore
```

> What? Where did PITR and pgBackRest come from? Pigsty has already configured out-of-the-box monitoring, backup, high availability for you - just use it! You could set it up manually, but it would be somewhat troublesome.

Then when we check the filesystem logs and database heartbeat table again, both are frozen before the 02:39:00 timestamp:

```bash
$ tail -n1 /data2/ts.log
02-38-59

$ psql -c 'select * from monitor.heartbeat'
   id    |              ts               |    lsn    | txid
---------+-------------------------------+-----------+------
 pg-meta | 2025-03-21 02:38:59.129603+00 | 251871544 | 2546
```

This proves this approach works! We successfully achieved consistent FS/DB PITR through PGFS!

------

## How's the Performance?

So functionality exists, but what about performance?

I found a development server with SSD and tested it using the built-in `juicefs bench`. Results look decent - definitely more than sufficient for applications like Odoo.

```bash
$ juicefs bench ~/jfs # Simple single-thread performance test
BlockSize: 1.0 MiB, BigFileSize: 1.0 GiB, 
SmallFileSize: 128 KiB, SmallFileCount: 100, NumThreads: 1
Time used: 42.2 s, CPU: 687.2%, Memory: 179.4 MiB
+------------------+------------------+---------------+
|       ITEM       |       VALUE      |      COST     |
+------------------+------------------+---------------+
|   Write big file |     178.51 MiB/s |   5.74 s/file |
|    Read big file |      31.69 MiB/s |  32.31 s/file |
| Write small file |    149.4 files/s |  6.70 ms/file |
|  Read small file |    545.2 files/s |  1.83 ms/file |
|        Stat file |   1749.7 files/s |  0.57 ms/file |
|   FUSE operation | 17869 operations |    3.82 ms/op |
|      Update meta |  1164 operations |    1.09 ms/op |
|       Put object |   356 operations |  303.01 ms/op |
|       Get object |   256 operations | 1072.82 ms/op |
|    Delete object |     0 operations |    0.00 ms/op |
| Write into cache |   356 operations |    2.18 ms/op |
|  Read from cache |   100 operations |    0.11 ms/op |
+------------------+------------------+---------------+
```

<details><summary>Another sample: Aliyun ESSD PL1 budget disk test results</summary><pre><code></code></pre></details>

While throughput performance is certainly inferior to native FS, it's sufficient for scenarios with **small file volumes and low access frequency**. After all, using "database as filesystem" isn't meant for massive storage and high-concurrency writes, but to enable database and filesystem to "travel back in time together" - it just needs to work.

------

## Completing the Puzzle: One-Click "Enterprise" Delivery

Next, let's put this setup into a practical scenario - like one-click deployment of "enterprise-grade" Odoo, where files automatically have CDP capabilities.

Pigsty provides PG with external high availability, automatic backup, monitoring, PITR and other capabilities. Installing it is very easy:

```bash
curl -fsSL https://repo.pigsty.cc/get | bash; cd ~/pigsty 
./bootstrap                # Install Pigsty dependencies
./configure -c app/odoo    # Use Odoo configuration template
./install.yml              # Install Pigsty
```

Above is Pigsty's standard installation process. Below we use playbooks to install Docker, create PGFS mount, and spin up stateless Odoo with Docker Compose:

```bash
./docker.yml -l odoo # Install Docker module, spin up Odoo stateless part
./juice.yml  -l odoo # Install JuiceFS module, PGFS mounted to /data2
./app.yml    -l odoo # Spin up Odoo stateless part using external PG/PGFS
```

Yes, it's that simple - everything is ready. However, while the commands are simple, the key is the configuration file.

The configuration file `pigsty.yml` would look something like this, with the only modification being the addition of JuiceFS configuration, mounting PGFS to `/data/odoo`:

```yaml
odoo:
  hosts:
    10.10.10.10:
      # ./juice.yml -l odoo : JuiceFS instance config (host-level parameter)
      juice_instances:
        jfs:                           # filesystem name
          path  : /data/odoo           # mountpoint path
          meta  : postgres://dbuser_meta:DBUser.Meta@10.10.10.10:5432/meta
          data  : --storage postgres --bucket 10.10.10.10:5432/meta --access-key dbuser_meta --secret-key DBUser.Meta
          port  : 9567                 # Prometheus metrics port
          owner : '100'                # Odoo container user UID
          group : '101'                # Odoo container user GID

  vars:
    # ./app.yml -l odoo
    app: odoo   # specify app name to be installed (in the apps)
    apps:       # define all applications
      odoo:     # app name, should have corresponding ~/app/odoo folder
        file:   # optional directory to be created
          - { path: /data/odoo/webdata ,state: directory, owner: 100, group: 101 }
          - { path: /data/odoo/addons  ,state: directory, owner: 100, group: 101 }
        conf:   # override /opt/<app>/.env config file
          PG_HOST: 10.10.10.10            # postgres host
          PG_PORT: 5432                   # postgres port
          PG_USERNAME: odoo               # postgres user
          PG_PASSWORD: DBUser.Odoo        # postgres password
          ODOO_PORT: 8069                 # odoo app port
          ODOO_DATA: /data/odoo/webdata   # odoo webdata
          ODOO_ADDONS: /data/odoo/addons  # odoo plugins
          ODOO_DBNAME: odoo               # odoo database name
          ODOO_VERSION: 18.0              # odoo image version
```

After completing these steps, you'll have an "enterprise-grade" Odoo running on the same server: backend database managed by Pigsty, filesystem mounted by JuiceFS, and JuiceFS's backend connected to PG. **Once a "rollback need" arises**, simply perform PITR on PG to get both files and database "back to the specified moment" together. This applies equally to applications with similar needs like Dify, Gitlab, Gitea, MatterMost, etc.

Looking back at all this, you'll find: what originally required expensive, high-end storage hardware to achieve CDP can now be accomplished with a lightweight open-source combination. While it bears the DIY marks of "poor man's engineering," **it's indeed simple, stable, and sufficiently practical**, worthy of exploration and experimentation in more scenarios.
