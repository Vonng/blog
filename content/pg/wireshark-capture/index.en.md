---
title: "Wireshark Packet Capture Protocol Analysis"
date: 2018-01-05
author: "vonng"
summary: >
  Wireshark is a very useful tool, especially suitable for analyzing network protocols. Here's a simple introduction to using Wireshark for packet capture and PostgreSQL protocol analysis.
tags: [PostgreSQL, PG Management, Tools]
---

Wireshark is a very useful tool, especially suitable for analyzing network protocols.

Here's a simple introduction to using Wireshark for packet capture and PostgreSQL protocol analysis.

Assuming debugging local PostgreSQL instance: 127.0.0.1:5432

## Quick Start

1. Download and install Wireshark: [Download link](https://www.wireshark.org/download.html)
2. Select the network interface for packet capture. For local testing, select `lo0`.
3. Add capture filter. If PostgreSQL uses default settings, use `port 5432`.
4. Start packet capture
5. Add display filter `pgsql` to filter out irrelevant TCP protocol packets.
6. Then you can perform some operations to observe and analyze the protocol

![](wireshark-capture.png)

-----------------

## Packet Capture Example

Let's start with the simplest case: no authentication, no SSL, execute the following command to establish a connection to PostgreSQL.

```bash
psql postgres://localhost:5432/postgres?sslmode=disable -c 'SELECT 1 AS a, 2 AS b;'
```

Note that `sslmode=disable` cannot be omitted here, otherwise the client will attempt to send SSL requests by default. `localhost` also cannot be omitted, otherwise the client will attempt to use unix socket by default.

This Bash command actually corresponds to three protocol phases and 5 groups of protocol packets in PostgreSQL:

* Startup phase: Client establishes a connection to PostgreSQL server.
* Simple query protocol: Client sends query command, server returns query results.
* Termination: Client terminates connection.

![](wireshark-capture-sample.png)

Wireshark has built-in PGSQL decoding, allowing us to conveniently view PostgreSQL protocol packet contents.

In the startup phase, the client sent a `StartupMessage (F)` to the server, and the server returned a series of messages, including `AuthenticationOK(R)`, `ParameterStatus(S)`, `BackendKeyData(K)`, `ReadyForQuery(Z)`. Here these messages are all packaged in the same TCP packet and sent to the client.

In the simple query phase, the client sent a `Query (F)` message, directly sending the SQL statement `SELECT 1 AS a, 2 AS b;` as content to the server. The server returned `RowDescription(T)`, `DataRow(D)`, `CommandComplete(C)`, `ReadyForQuery(Z)` in sequence.

In the termination phase, the client sent a `Terminate(X)` message to terminate the connection.

-----------------

## Aside: Using Mac for Wireless Network Sniffing

Conclusion: Mac: airport, tcpdump Windows: Omnipeek Linux: tcpdump, airmon-ng

Ethernet packet capture is simple, with many software options like Wireshark, Ethereal, Sniffer Pro. However, wireless packet capture is slightly more complicated. I found many verbose articles online that beat around the bush - actually capturing wireless packets can be done with one command.

Windows is more troublesome because wireless network card drivers refuse to enter promiscuous mode, typically using Omnipeek, won't go into detail.

Linux and Mac are very convenient. Just use tcpdump, which is generally built into systems. The -i option parameter is the network device name you want to capture. Mac's default WiFi card is en0. `tcpdump -Ine -i en0`

The key is specifying the -I parameter to enter monitor mode. `-I :Put the interface in "monitor mode"; this is supported only on IEEE 802.11 Wi-Fi interfaces, and supported only on some operating systems.` After entering monitor mode, the wireless card used for monitoring cannot access the internet, so consider buying an external wireless card for capturing packets while maintaining internet access.

Captured packets can be used for many malicious purposes, like breaking WEP network passwords with a few IV packets using aircrack, or running dictionary attacks on WPA networks with captured handshake packets. If on the same network, you can also see various unencrypted traffic... like photos, private images, etc...

If I already know a phone's MAC address, then `tcpdump -Ine -i en0 | grep $MAC_ADDRESS` filters out WiFi traffic related to that phone.

For specific frame type details, see 802.11 protocol, "802.11 Wireless Networks: The Definitive Guide", etc.

Incidentally, explaining the difference between promiscuous mode and monitor mode: Promiscuous mode means: receiving all packets in the same network, regardless of whether they're addressed to yourself. Monitor mode means: receiving all packets transmitted on a specific physical channel.

> RFMON RFMON is short for radio frequency monitoring mode and is sometimes also described as monitor mode or raw monitoring mode. In this mode an 802.11 wireless card is in listening mode ("sniffer" mode).
>
> The wireless card does not have to associate to an access point or ad-hoc network but can passively listen to all traffic on the channel it is monitoring. Also, the wireless card does not require the frames to pass CRC checks and forwards all frames (corrupted or not with 802.11 headers) to upper level protocols for processing. This can come in handy when troubleshooting protocol issues and bad hardware.
>
> RFMON/Monitor Mode vs. Promiscuous Mode Promiscuous mode in wired and wireless networks instructs a wired or wireless card to process any traffic regardless of the destination mac address. In wireless networks promiscuous mode requires that the wireless card be associated to an access point or ad-hoc network. While in promiscuous mode a wireless card can transmit and receive but will only captures traffic for the network (SSID) to which it is associated.
>
> RFMON mode is only possible for wireless cards and does not require the wireless card to be associated to a wireless network. While in monitor mode the wireless card can passively monitor traffic of all networks and devices within listening range (SSIDs, stations, access points). In most cases the wireless card is not able to transmit and does not follow the typical 802.11 protocol when receiving traffic (i.e. transmit an 802.11 ACK for received packet).
>
> Both modes have to be supported by the driver of the wired or wireless card.

Also, while researching packet capture tools, I discovered a very useful command-line tool called airport on Mac for packet capture and manipulating Macbook WiFi. Located at `/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport`

You can create a symbolic link for convenient use: `sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport`

Common commands include: Display current network info: `airport -I` Scan surrounding wireless networks: `airport -s` Disconnect current wireless network: `airport -z` Force specify wireless channel: `airport -c=$CHANNEL`

Capture wireless packets, can specify channel: `airport en0 sniff [$CHANNEL]` Captured packets are placed in /tmp/airportSniffXXXXX.cap, can be read with tcpdump, tshark, wireshark, etc.

The most practical function is scanning surrounding wireless networks.