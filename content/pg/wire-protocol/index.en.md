---
title: "Frontend-Backend Communication Wire Protocol"
date: 2019-11-12
author: "vonng"
summary: >
  Understanding the TCP protocol used for communication between PostgreSQL server and client, and printing messages using Go
tags: [PostgreSQL, PG Development, PG Kernel]
---

Understanding the TCP protocol used for communication between PostgreSQL server and client

------------------

## Startup Phase

The basic flow of the startup phase is as follows:

* Client sends a `StartupMessage (F)` to initiate connection request to server

  Payload includes `0x30000` Int32 version number magic, and a series of kv-structured runtime parameters (NULL0 separated, required parameter is `user`),

* Client waits for server response, mainly waiting for `ReadyForQuery (Z)` event sent by server, which represents that server is ready to receive requests.

The above are the two main events in connection establishment process. Other events include authentication messages `AuthenticationXXX (R)`, backend key messages `BackendKeyData (K)`, error messages `ErrorResponse (E)`, and a series of context-independent messages (`NoticeResponse (N)`, `NotificationResponse (A)`, `ParameterStatus(S)`)

We can write a Go program to simulate this process:

```go
package main

import (
	"fmt"
	"net"
	"time"

	"github.com/jackc/pgx/pgproto3"
)

func GetFrontend(address string) *pgproto3.Frontend {
	conn, _ := (&net.Dialer{KeepAlive: 5 * time.Minute}).Dial("tcp4", address)
	frontend, _ := pgproto3.NewFrontend(conn, conn)
	return frontend
}

func main() {
	frontend := GetFrontend("127.0.0.1:5432")

	// Establish connection
	startupMsg := &pgproto3.StartupMessage{
		ProtocolVersion: pgproto3.ProtocolVersionNumber,
		Parameters:      map[string]string{"user": "vonng"},
	}
	frontend.Send(startupMsg)

	// Startup process, receiving ReadyForQuery message indicates startup process completion
	for {
		msg, _ := frontend.Receive()
		fmt.Printf("%T %v\n", msg, msg)
		if _, ok := msg.(*pgproto3.ReadyForQuery); ok {
			fmt.Println("[STARTUP] connection established")
			break
		}
	}

	// Simple query protocol
	simpleQueryMsg := &pgproto3.Query{String: `SELECT 1 as a;`}
	frontend.Send(simpleQueryMsg)
	// Receiving CommandComplete message indicates query completion
	for {
		msg, _ := frontend.Receive()
		fmt.Printf("%T %v\n", msg, msg)
		if _, ok := msg.(*pgproto3.CommandComplete); ok {
			fmt.Println("[QUERY] query complete")
			break
		}
	}
}
```

Output result:

```bash
*pgproto3.Authentication &{0 [0 0 0 0] [] []}
*pgproto3.ParameterStatus &{application_name }
*pgproto3.ParameterStatus &{client_encoding UTF8}
*pgproto3.ParameterStatus &{DateStyle ISO, MDY}
*pgproto3.ParameterStatus &{integer_datetimes on}
*pgproto3.ParameterStatus &{IntervalStyle postgres}
*pgproto3.ParameterStatus &{is_superuser on}
*pgproto3.ParameterStatus &{server_encoding UTF8}
*pgproto3.ParameterStatus &{server_version 11.3}
*pgproto3.ParameterStatus &{session_authorization vonng}
*pgproto3.ParameterStatus &{standard_conforming_strings on}
*pgproto3.ParameterStatus &{TimeZone PRC}
*pgproto3.BackendKeyData &{35703 345830596}
*pgproto3.ReadyForQuery &{73}
[STARTUP] connection established
*pgproto3.RowDescription &{[{a 0 0 23 4 -1 0}]}
*pgproto3.DataRow &{[[49]]}
*pgproto3.CommandComplete &{SELECT 1}
[QUERY] query complete
```

------------------

## Connection Proxy

Based on `jackc/pgx/pgproto3`, you can easily write some middleware. For example, the following code is a very simple "connection proxy":

```go
package main

import (
	"io"
	"net"
	"strings"
	"time"

	"github.com/jackc/pgx/pgproto3"
)

type ProxyServer struct {
	UpstreamAddr string
	ListenAddr   string
	Listener     net.Listener
	Dialer       net.Dialer
}

func NewProxyServer(listenAddr, upstreamAddr string) *ProxyServer {
	ln, _ := net.Listen(`tcp4`, listenAddr)
	return &ProxyServer{
		ListenAddr:   listenAddr,
		UpstreamAddr: upstreamAddr,
		Listener:     ln,
		Dialer:       net.Dialer{KeepAlive: 1 * time.Minute},
	}
}

func (ps *ProxyServer) Serve() error {
	for {
		conn, err := ps.Listener.Accept()
		if err != nil {
			panic(err)
		}
		go ps.ServeOne(conn)
	}
}

func (ps *ProxyServer) ServeOne(clientConn net.Conn) error {
	backend, _ := pgproto3.NewBackend(clientConn, clientConn)
	startupMsg, err := backend.ReceiveStartupMessage()
	if err != nil && strings.Contains(err.Error(), "ssl") {
		if _, err := clientConn.Write([]byte(`N`)); err != nil {
			panic(err)
		}
		// ssl is not welcome, now receive real startup msg
		startupMsg, err = backend.ReceiveStartupMessage()
		if err != nil {
			panic(err)
		}
	}

	serverConn, _ := ps.Dialer.Dial(`tcp4`, ps.UpstreamAddr)
	frontend, _ := pgproto3.NewFrontend(serverConn, serverConn)
	frontend.Send(startupMsg)

	errChan := make(chan error, 2)
	go func() {
		_, err := io.Copy(clientConn, serverConn)
		errChan <- err
	}()
	go func() {
		_, err := io.Copy(serverConn, clientConn)
		errChan <- err
	}()

	return <-errChan
}

func main() {
	proxy := NewProxyServer("127.0.0.1:5433", "127.0.0.1:5432")
	proxy.Serve()
}
```

Here the proxy listens on port 5433 and parses and forwards messages to the real database server on port 5432. Execute the following command in another session:

```bash
$ psql postgres://127.0.0.1:5433/data?sslmode=disable -c 'SELECT * FROM pg_stat_activity LIMIT 1;'
```

You can observe message exchanges during this process:

```
[B2F] *pgproto3.ParameterStatus &{application_name psql}
[B2F] *pgproto3.ParameterStatus &{client_encoding UTF8}
[B2F] *pgproto3.ParameterStatus &{DateStyle ISO, MDY}
[B2F] *pgproto3.ParameterStatus &{integer_datetimes on}
[B2F] *pgproto3.ParameterStatus &{IntervalStyle postgres}
[B2F] *pgproto3.ParameterStatus &{is_superuser on}
[B2F] *pgproto3.ParameterStatus &{server_encoding UTF8}
[B2F] *pgproto3.ParameterStatus &{server_version 11.3}
[B2F] *pgproto3.ParameterStatus &{session_authorization vonng}
[B2F] *pgproto3.ParameterStatus &{standard_conforming_strings on}
[B2F] *pgproto3.ParameterStatus &{TimeZone PRC}
[B2F] *pgproto3.BackendKeyData &{41588 1354047533}
[B2F] *pgproto3.ReadyForQuery &{73}
[F2B] *pgproto3.Query &{SELECT * FROM pg_stat_activity LIMIT 1;}
[B2F] *pgproto3.RowDescription &{[{datid 11750 1 26 4 -1 0} {datname 11750 2 19 64 -1 0} {pid 11750 3 23 4 -1 0} {usesysid 11750 4 26 4 -1 0} {usename 11750 5 19 64 -1 0} {application_name 11750 6 25 -1 -1 0} {client_addr 11750 7 869 -1 -1 0} {client_hostname 11750 8 25 -1 -1 0} {client_port 11750 9 23 4 -1 0} {backend_start 11750 10 1184 8 -1 0} {xact_start 11750 11 1184 8 -1 0} {query_start 11750 12 1184 8 -1 0} {state_change 11750 13 1184 8 -1 0} {wait_event_type 11750 14 25 -1 -1 0} {wait_event 11750 15 25 -1 -1 0} {state 11750 16 25 -1 -1 0} {backend_xid 11750 17 28 4 -1 0} {backend_xmin 11750 18 28 4 -1 0} {query 11750 19 25 -1 -1 0} {backend_type 11750 20 25 -1 -1 0}]}
[B2F] *pgproto3.DataRow &{[[] [] [52 56 55 52] [] [] [] [] [] [] [50 48 49 57 45 48 53 45 49 56 32 50 48 58 52 56 58 49 57 46 51 50 55 50 54 55 43 48 56] [] [] [] [65 99 116 105 118 105 116 121] [65 117 116 111 86 97 99 117 117 109 77 97 105 110] [] [] [] [] [97 117 116 111 118 97 99 117 117 109 32 108 97 117 110 99 104 101 114]]}
[B2F] *pgproto3.CommandComplete &{SELECT 1}
[B2F] *pgproto3.ReadyForQuery &{73}
[F2B] *pgproto3.Terminate &{}
```