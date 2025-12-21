---
title: "Pgbouncer Quick Start"
date: 2018-02-07
author: "vonng"
summary: "Pgbouncer is a lightweight database connection pool. This guide covers basic Pgbouncer configuration, management, and usage."
tags: [PostgreSQL, "PG-Admin", "Connection-Pool"]
---

Pgbouncer is a lightweight database connection pool.

### Synopsis

```bash
pgbouncer [-d][-R][-v][-u user] <pgbouncer.ini>
pgbouncer -V|-h
```

### Description

**pgbouncer** is a PostgreSQL connection pooler. Any target application can connect to **pgbouncer** as if it were a PostgreSQL server, and **pgbouncer** will create connections to the actual server or reuse existing connections.

The purpose of **pgbouncer** is to reduce the performance impact of opening new PostgreSQL connections.

To avoid affecting connection pool transaction semantics, **pgbouncer** supports several types of pooling when switching connections:

- **Session pooling**

  The most polite method. When a client connects, a server connection will be assigned for the entire duration of the client connection. When the client disconnects, the server connection is returned to the pool. This is the default method.

- **Transaction pooling**

  A server connection is only assigned to a client for the duration of a transaction. When PgBouncer detects transaction end, the server connection is returned to the pool.

- **Statement pooling**

  The most aggressive mode. Server connections are immediately returned to the pool after query completion. Multi-statement transactions are not allowed in this mode as they would break.

The **pgbouncer** management interface is available through some new `SHOW` commands when connecting to the special 'virtual' database **pgbouncer**.

### Getting Started

Basic setup and usage:

1. Create a pgbouncer.ini file. See **pgbouncer(5)** for details. Simple example:

   ```ini
   [databases]
   template1 = host=127.0.0.1 port=5432 dbname=template1
   
   [pgbouncer]
   listen_port = 6543
   listen_addr = 127.0.0.1
   auth_type = md5
   auth_file = users.txt
   logfile = pgbouncer.log
   pidfile = pgbouncer.pid
   admin_users = someuser
   ```

2. Create `users.txt` file containing allowed users:

   ```bash
   "someuser" "same_password_as_in_server"
   ```

3. Launch **pgbouncer**:

   ```bash
   $ pgbouncer -d pgbouncer.ini
   ```

4. Have your application (or **psql**) connect to **pgbouncer** instead of directly to PostgreSQL server:

   ```bash
    psql -p 6543 -U someuser template1
   ```

5. Manage **pgbouncer** by connecting to the special admin database **pgbouncer** and issue `show help;` to start:

   ```bash
   $ psql -p 6543 -U someuser pgbouncer
   pgbouncer=# show help;
   NOTICE:  Console usage
   DETAIL:
     SHOW [HELP|CONFIG|DATABASES|FDS|POOLS|CLIENTS|SERVERS|SOCKETS|LISTS|VERSION]
     SET key = arg
     RELOAD
     PAUSE
     SUSPEND
     RESUME
     SHUTDOWN
   ```

6. If you modify pgbouncer.ini file, you can reload it with:

   ```bash
   pgbouncer=# RELOAD;
   ```

### Command Line Switches

| -d             | Run in background. Without it, the process runs in foreground. Note: Doesn't work on Windows, **pgbouncer** needs to run as a service. |
| -------------- | ------------------------------------------------------------ |
| -R             | Do online restart. This means connect to running process, load open sockets from it, then use them. If no active process, boot normally. Note: Only works if OS supports Unix sockets and `unix_socket_dir` is not disabled in config. Doesn't work on Windows. TLS connections are not used, they are dropped. |
| -u user        | Switch to given user on startup.                             |
| -v             | Increase verbosity. Can be used multiple times.             |
| -q             | Be quiet - don't log to stdout. Note this doesn't affect logging verbosity, only that stdout is not used. For init.d scripts. |
| -V             | Show version.                                                   |
| -h             | Show brief help.                                               |
| --regservice   | Win32: register pgbouncer to run as Windows service. **service_name** config parameter value is used as the name to register. |
| --unregservice | Win32: unregister Windows service.                                   |

### Admin Console

Console is available by connecting normally to database **pgbouncer**:

```
$ psql -p 6543 pgbouncer
```

Only users listed in config parameters **admin_users** or **stats_users** are allowed to login to console. (Exception: when auth_mode=any, any user can login as stats_user.)

Additionally, when logged in via Unix socket and the client has the same Unix user UID as the running process, username **pgbouncer** is allowed to login without password.

### SHOW Commands

#### `SHOW STATS;`

Shows statistics.

| Field               | Description                      |
| ------------------- | -------------------------------- |
| `database`          | Statistics organized by database |
| `total_xact_count`  | Total number of SQL transactions |
| `total_query_count` | Total number of SQL queries      |
| `total_received`    | Total network traffic received (bytes) |
| `total_sent`        | Total network traffic sent (bytes) |
| `total_xact_time`   | Total time spent in transactions |
| `total_query_time`  | Total time spent in queries      |
| `total_wait_time`   | Total time spent waiting         |
| `avg_xact_count`    | Average transactions per second (current) |
| `avg_query_count`   | Average queries per second (current) |
| `avg_recv`          | Average bytes received per second (current) |
| `avg_sent`          | Average bytes sent per second (current) |
| `avg_xact_time`     | Average transaction time (milliseconds) |
| `avg_query_time`    | Average query time (milliseconds) |
| `avg_wait_time`     | Average wait time (milliseconds) |

Two variants: `SHOW STATS_TOTALS` and `SHOW STATS_AVERAGES`, showing totals and averages respectively.

TOTAL metrics are actually counters, while AVG are typically gauges. For monitoring, it's recommended to collect TOTAL, and use AVG for viewing.

#### `SHOW SERVERS`

| Field           | Description                                                         |
| -------------- | ------------------------------------------------------------ |
| `type`         | Server type fixed as S                                          |
| `user`         | Username PgBouncer uses to connect to database                              |
| `state`        | State of pgbouncer server connection: **active**, **used**, or **idle** |
| `addr`         | IP address of PostgreSQL server                            |
| `port`         | Port of PostgreSQL server                                     |
| `local_addr`   | Local address connection originates from                                         |
| `local_port`   | Local port connection originates from                                       |
| `connect_time` | Time when connection was established                                             |
| `request_time` | Time when last request was issued                                     |
| `ptr`          | Address of internal object for this connection, used as unique identifier                         |
| `link`         | Address of paired client connection                                 |
| `remote_pid`   | PID of backend server process. If connected via unix socket and OS supports getting process ID info, it's the OS pid. Otherwise extracted from cancel packet sent by server - if server is Postgres, should be PID, but if server is another PgBouncer, it's a random number. |

#### `SHOW CLIENTS`

| Field           | Description                                                         |
| -------------- | ------------------------------------------------------------ |
| `type`         | Client type fixed as C                                          |
| `user`         | User client uses to connect                                         |
| `state`        | State of pgbouncer client connection: **active**, **used**, **waiting**, or **idle** |
| `addr`         | IP address of client                                             |
| `port`         | Client port                                                 |
| `local_addr`   | Local address                                                     |
| `local_port`   | Local port                                                     |
| `connect_time` | Time when connection was established                                             |
| `request_time` | Time when last request was issued                                     |
| `ptr`          | Address of internal object for this connection, used as unique identifier                         |
| `link`         | Address of paired server connection                                     |
| `remote_pid`   | If connected via unix socket and OS supports getting process ID info, it's the OS pid |

#### SHOW POOLS;

A new connection pool is created for each (database, user) pair.

- database: Database name
- user: Username
- cl_active: Client connections linked to server connection and can process queries
- cl_waiting: Client connections that have sent queries but not yet gotten server connection
- sv_active: Server connections linked to client
- sv_idle: Server connections unused and immediately available for client queries
- sv_used: Server connections idle longer than server_check_delay, so need to run server_check_query before they can be used
- sv_tested: Server connections currently running server_reset_query or server_check_query
- sv_login: Server connections currently in login process
- maxwait: How long the first (oldest) client in queue has been waiting, in seconds. If it starts increasing, the current connection pool can't handle requests fast enough. Cause could be server overload or **pool_size** setting too small
- pool_mode: Connection pooling mode being used

#### SHOW LISTS;

Shows following internal information in columns (not rows):

- databases: Database count
- users: User count  
- pools: Pool count
- free_clients: Free client count
- used_clients: Used client count
- login_clients: Client count in **login** state
- free_servers: Free server count
- used_servers: Used server count

#### SHOW USERS;

- name: Username
- pool_mode: User's overridden pool_mode, NULL if using default

#### SHOW DATABASES;

- name: Name of configured database entry
- host: Host pgbouncer connects to
- port: Port pgbouncer connects to  
- database: Actual database name pgbouncer connects to
- force_user: When user is part of connection string, connection between pgbouncer and PostgreSQL is forced to given user, regardless of client user
- pool_size: Maximum number of server connections
- pool_mode: Database's overridden pool_mode, NULL if using default

#### SHOW FDS;

Internal command - shows list of fds used with accompanying internal state.

When connected user uses username "pgbouncer", connected via Unix socket and has same UID as running process, actual fds are passed over connection. This mechanism is used for online restart. Note: Doesn't work on Windows.

This command also blocks internal event loop, so shouldn't be used while PgBouncer is in use.

- fd: File descriptor numeric value
- task: One of **pooler**, **client**, or **server**
- user: User of connection using this FD
- database: Database of connection using this FD
- addr: IP address of connection using FD, or **unix** if using unix socket
- port: Port of connection using FD
- cancel: Cancel key for this connection
- link: Corresponding server/client fd. NULL if idle

#### SHOW CONFIG;

Shows current configuration settings, one per line, with following fields:

- key: Configuration variable name
- value: Configuration value
- changeable: **yes** or **no**, shows whether runtime variable is changeable. If **no**, variable can only be changed at startup

#### SHOW DNS_HOSTS;

Shows hostnames in DNS cache.

- hostname: Hostname
- ttl: Seconds until next lookup
- addrs: Comma-separated list of addresses

#### SHOW DNS_ZONES

Shows DNS zones in cache.

- zonename: Zone name
- serial: Current serial number  
- count: Hostnames belonging to this zone

### Process Control Commands

#### `PAUSE [db];`

PgBouncer tries to disconnect all servers, first waiting for all queries to complete. Command doesn't return until all queries complete. Use during database restart. If database name provided, only that database is paused.

#### `DISABLE db;`

Reject all new client connections on given database.

#### `ENABLE db;`

Allow new client connections after previous **DISABLE** command.

#### `KILL db;`

Immediately drop all client and server connections on given database.

#### `SUSPEND;`

All socket buffers are flushed and PgBouncer stops listening for data on them. Command doesn't return until all buffers are empty. Use during PgBouncer online restart.

#### `RESUME [db];`

Resume work from previous **PAUSE** or **SUSPEND** command.

#### `SHUTDOWN;`

PgBouncer process will exit.

#### `RELOAD;`

PgBouncer process will reload its configuration file and update changeable settings.

### Signals

- SIGHUP: Reload config. Same as issuing **RELOAD;** command on console.
- SIGINT: Safe shutdown. Same as issuing **PAUSE;** and **SHUTDOWN;** on console.
- SIGTERM: Immediate shutdown. Same as issuing **SHUTDOWN;** on console.

### Libevent Settings

From libevent documentation:

```
Support for epoll, kqueue, devpoll, poll or select can be disabled by setting 
the environment variables EVENT_NOEPOLL, EVENT_NOKQUEUE, EVENT_NODEVPOLL, 
EVENT_NOPOLL or EVENT_NOSELECT respectively.

By setting the environment variable EVENT_SHOW_METHOD, libevent displays the 
kernel notification method it uses.
```

## Pgbouncer Parameter Configuration

### Default Configuration

```ini
;; Database name = connection string
;;
;; Connection string parameters:
;;   dbname= host= port= user= password=
;;   client_encoding= datestyle= timezone=
;;   pool_size= connect_query=
;;   auth_user=
[databases]

instanceA = host=10.1.1.1 dbname=core
instanceB = host=102.2.2.2 dbname=payment

; foodb over Unix socket
;foodb =

; Redirect bardb on localhost to bazdb 
;bardb = host=localhost dbname=bazdb

; Access target database with single user
;forcedb = host=127.0.0.1 port=300 user=baz password=foo client_encoding=UNICODE datestyle=ISO connect_query='SELECT 1'

; Use custom connection pool size
;nondefaultdb = pool_size=50 reserve_pool=10

; If user not in auth file, use auth_user as substitute; auth_user must be in auth file
; foodb = auth_user=bar

; Fallback wildcard connection string
;* = host=testserver

;; Pgbouncer configuration section
[pgbouncer]

;;;
;;; Administrative settings
;;;

logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid

;;;
;;; Where to listen for clients
;;;

; IP address to listen on, * means all IPs
listen_addr = *
listen_port = 6432

; Unix socket is also used by -R option
; On Debian this is /var/run/postgresql
;unix_socket_dir = /tmp
;unix_socket_mode = 0777
;unix_socket_group =

;;;
;;; TLS settings
;;;

;; Options: disable, allow, require, verify-ca, verify-full
;client_tls_sslmode = disable

;; Path to trusted CA certificate file
;client_tls_ca_file = <system default>

;; Private key and certificate paths for client representation
;; Required when accepting TLS connections from clients
;client_tls_key_file =
;client_tls_cert_file =

;; fast, normal, secure, legacy, <ciphersuite string>
;client_tls_ciphers = fast

;; all, secure, tlsv1.0, tlsv1.1, tlsv1.2
;client_tls_protocols = all

;; none, auto, legacy
;client_tls_dheparams = auto

;; none, auto, <curve name>
;client_tls_ecdhcurve = auto

;;;
;;; TLS settings for connecting to backend databases
;;;

;; disable, allow, require, verify-ca, verify-full
;server_tls_sslmode = disable

;; Path to trusted CA certificate file
;server_tls_ca_file = <system default>

;; Private key and certificate for backend representation
;; Only needed when backend server requires client certificates
;server_tls_key_file =
;server_tls_cert_file =

;; all, secure, tlsv1.0, tlsv1.1, tlsv1.2
;server_tls_protocols = all

;; fast, normal, secure, legacy, <ciphersuite string>
;server_tls_ciphers = fast

;;;
;;; Authentication settings
;;;

; any, trust, plain, crypt, md5, cert, hba, pam
auth_type = trust
auth_file = /etc/pgbouncer/userlist.txt

;; HBA-style authentication config file
# auth_hba_file = /pg/data/pg_hba.conf

;; Query to get password from database, result must contain two columns: username and password hash
;auth_query = SELECT usename, passwd FROM pg_shadow WHERE usename=$1

;;;
;;; Users allowed to access virtual database 'pgbouncer'
;;;

; Users allowed to modify settings, comma-separated list of usernames
admin_users = postgres

; Users allowed to use SHOW commands, comma-separated list of usernames
stats_users = stats, postgres

;;;
;;; Connection pooling settings
;;;

; When server connection is put back to pool? (default is session)
;   session      - session mode, when client disconnects
;   transaction  - transaction mode, when transaction ends  
;   statement    - statement mode, when statement ends
pool_mode = session

; Query for immediately cleaning connections when client releases connection
; Don't put ROLLBACK here, Pgbouncer won't reuse connections when transaction hasn't ended
;
; Query for 8.3 and higher versions:
;   DISCARD ALL;
;
; Older versions:
;   RESET ALL; SET SESSION AUTHORIZATION DEFAULT
;
; Empty if transaction-level connection pooling enabled
;
server_reset_query = DISCARD ALL

; Whether server_reset_query needs to execute in any case
; If off (default), server_reset_query only used in session-level connection pooling
;server_reset_query_always = 0

;
; Comma-separated list of parameters to ignore when given
; in startup packet. Newer JDBC versions require the
; extra_float_digits here.
;
;ignore_startup_parameters = extra_float_digits

;
; When taking idle server into use, this query is ran first.
;   SELECT 1
;
;server_check_query = select 1

; If server was used more recently that this many seconds ago,
; skip the check query. Value 0 may or may not run in immediately.
;server_check_delay = 30

; Close servers in session pooling mode after a RECONNECT, RELOAD,
; etc. when they are idle instead of at the end of the session.
;server_fast_close = 0

;; Use <appname - host> as application_name on server.
;application_name_add_host = 0

;;;
;;; Connection limits
;;;

; Maximum allowed connections
max_client_conn = 100

; Default pool size, 20 is appropriate for transaction connection pooling
; For session-level connection pooling, this is max connections you want to handle simultaneously
default_pool_size = 20

;; Minimum reserved connections in pool
;min_pool_size = 0

; How many additional connections allowed when problems occur
;reserve_pool_size = 0

; If client waits longer than this many seconds, use reserve pool
;reserve_pool_timeout = 5

; Maximum connections allowed per single database/user
;max_db_connections = 0
;max_user_connections = 0

; If off, then server connections are reused in LIFO manner
;server_round_robin = 0

;;;
;;; Logging
;;;

;; Syslog settings
;syslog = 0
;syslog_facility = daemon
;syslog_ident = pgbouncer

; log if client connects or server connection is made
;log_connections = 1

; log if and why connection was closed
;log_disconnections = 1

; log error messages pooler sends to clients
;log_pooler_errors = 1

;; Period for writing aggregated stats into log.
;stats_period = 60

;; Logging verbosity. Same as -v switch on command line.
;verbose = 0

;;;
;;; Timeouts
;;;

;; Close server connection if its been connected longer.
;server_lifetime = 3600

;; Close server connection if its not been used in this time.
;; Allows to clean unnecessary connections from pool after peak.
;server_idle_timeout = 600

;; Cancel connection attempt if server does not answer takes longer.
;server_connect_timeout = 15

;; If server login failed (server_connect_timeout or auth failure)
;; then wait this many second.
;server_login_retry = 15

;; Dangerous. Server connection is closed if query does not return
;; in this time. Should be used to survive network problems,
;; _not_ as statement_timeout. (default: 0)
;query_timeout = 0

;; Dangerous. Client connection is closed if the query is not assigned
;; to a server in this time. Should be used to limit the number of queued
;; queries in case of a database or network failure. (default: 120)
;query_wait_timeout = 120

;; Dangerous. Client connection is closed if no activity in this time.
;; Should be used to survive network problems. (default: 0)
;client_idle_timeout = 0

;; Disconnect clients who have not managed to log in after connecting
;; in this many seconds.
;client_login_timeout = 60

;; Clean automatically created database entries (via "*") if they
;; stay unused in this many seconds.
; autodb_idle_timeout = 3600

;; How long SUSPEND/-R waits for buffer flush before closing connection.
;suspend_timeout = 10

;; Close connections which are in "IDLE in transaction" state longer than
;; this many seconds.
;idle_transaction_timeout = 0

;;;
;;; Low-level tuning options
;;;

;; buffer for streaming packets
;pkt_buf = 4096

;; man 2 listen
;listen_backlog = 128

;; Max number pkt_buf to process in one event loop.
;sbuf_loopcnt = 5

;; Maximum PostgreSQL protocol packet size.
;max_packet_size = 2147483647

;; networking options, for info: man 7 tcp

;; Linux: notify program about new connection only if there
;; is also data received. (Seconds to wait.)
;; On Linux the default is 45, on other OS'es 0.
;tcp_defer_accept = 0

;; In-kernel buffer size (Linux default: 4096)
;tcp_socket_buffer = 0

;; whether tcp keepalive should be turned on (0/1)
;tcp_keepalive = 1

;; The following options are Linux-specific.
;; They also require tcp_keepalive=1.

;; count of keepalive packets
;tcp_keepcnt = 0

;; how long the connection can be idle,
;; before sending keepalive packets
;tcp_keepidle = 0

;; The time between individual keepalive probes.
;tcp_keepintvl = 0

;; DNS lookup caching time
;dns_max_ttl = 15

;; DNS zone SOA lookup period
;dns_zone_check_period = 0

;; DNS negative result caching time
;dns_nxdomain_ttl = 15

;;;
;;; Random stuff
;;;

;; Hackish security feature. Helps against SQL-injection - when PQexec is disabled,
;; multi-statement cannot be made.
;disable_pqexec = 0

;; Config file to use for next RELOAD/SIGHUP.
;; By default contains config file from command line.
;conffile

;; Win32 service name to register as. job_name is alias for service_name,
;; used by some Skytools scripts.
;service_name = pgbouncer
;job_name = pgbouncer

;; Read additional config from the /etc/pgbouncer/pgbouncer-other.ini file
;%include /etc/pgbouncer/pgbouncer-other.ini
```