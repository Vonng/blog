---
title: Blockchain and Distributed Databases
date: 2018-06-09
hero: /hero/blockchain.jpg
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [Original Zhihu Article](https://www.zhihu.com/question/275845393/answer/386816571)
summary: >
  The technical essence, functionality, and evolution of blockchain is distributed databases. Specifically, it's a **Byzantine Fault Tolerant (resistant to malicious node attacks) distributed (leaderless replication) database**.
tags: [database,distributed]
---


**The essence, intended functionality, and evolutionary direction of blockchain is distributed databases.**

To be precise, it's a **Byzantine Fault Tolerant (resistant to malicious node attacks) distributed (leaderless replication) database**.

![](blockchain.jpg)

If this distributed database is used to store **transaction records** of various coins, the system is called "XX coin". For example, Ethereum is such a distributed database that records not only transaction records of various altcoins but also all kinds of other content. By spending some Ether, you can leave [a record (a message)](https://etherscan.io/tx/0x2d6a7b0f6adeff38423d4c62cd8b6ccb708ddad85da5d3d06756ad4d8a04a6a2) in this distributed database. And so-called **smart contracts** are **stored procedures** on this distributed database.

Formally, **blockchain** and **Write-Ahead Log (WAL, Binlog, Redolog)** are highly consistent in their design principles.

WAL is the core data structure of databases, recording all changes from database creation to the current moment, used for implementing master-slave replication, backup rollback, failure recovery, and other functions. If full WAL logs are retained, you can replay the WAL from the beginning and time-travel to any moment's state, like PostgreSQL's PITR (Point-In-Time Recovery).

Blockchain is essentially such a log that records every transaction since genesis. Replaying the log can restore the database to any moment's state (but not vice versa). So blockchain can certainly be considered a database in some sense.

The two major characteristics of blockchain - decentralization and tamper-resistance - are easy to understand using database concepts:

- **Decentralization** is essentially **leaderless replication**, with the core being **distributed consensus**.
- **Tamper-resistance** is essentially **Byzantine fault tolerance**, i.e., making **the computational cost of tampering with WAL probabilistically infeasible**.

Just as WAL is divided into **log segments**, blockchain is also divided into individual **blocks**, and each segment carries the hash fingerprint of the previous log segment.

So-called mining is a public number-guessing competition (only numbers meeting certain conditions are accepted by consensus). The first to guess correctly gets the right to the next log segment: writing a record transferring funds to themselves (mining reward) and broadcasting it (if others also guess correctly, the one that broadcasts to the majority first wins). All nodes use consensus algorithms to ensure the current longest chain is the authoritative log version. Blockchain implements **leaderless replication** of log segments through **consensus algorithms**.

If you want to modify a transaction record in a certain WAL log segment, say, transfer ten thousand bitcoins to yourself, you need to forge the fingerprints of this block and all subsequent blocks (guessing numbers multiple times) and make the majority of nodes believe this forged version (creating a longer forged version means guessing more numbers). The six-block confirmation in Bitcoin refers to this - the computational cost of tampering with records before six log segments is usually probabilistically infeasible. Blockchain implements **Byzantine fault tolerance** through this mechanism (such as Merkle trees).

Among the technologies involved in blockchain, all are simple except **distributed consensus**, but this **application approach** and **mechanism design** is indeed quite stunning. Blockchain can be considered an evolutionary attempt at databases, with broad prospects in the long term. However, fields where blockchain can have immediate impact seem to all be Big Brother's territory. And no matter how much it's hyped, current blockchain is still far from being a true distributed database, so those entering now to build applications are likely to be martyrs.