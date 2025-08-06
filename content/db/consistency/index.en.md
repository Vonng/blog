---
title: "Consistency: An Overloaded Term"
date: 2018-05-08
hero: /hero/consistency.jpg
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [Zhihu Original](https://www.zhihu.com/question/275845393/answer/386816571)
summary: >
  The term "consistency" is heavily overloaded, representing different concepts in different contexts. For example, the C in ACID and the C in CAP actually refer to different concepts.
tags: [database]
---

The term **consistency** is heavily overloaded, representing different things in different contexts and situations:

- In the context of transactions, such as the C in ACID, it refers to the usual **Consistency**
- In the context of distributed systems, such as the C in CAP, it actually refers to **Linearizability**
- Additionally, "consistency" in terms like "consistent hashing" and "eventual consistency" also has different meanings.

[![](featured.jpg)](https://www.zhihu.com/question/275845393/answer/386816571)

--------------

These consistencies are different yet have intricate connections, so they often confuse people.

- In the context of transactions, the concept of **Consistency** is: **a specific set of statements about data must always hold true**. That is, **invariants**. Specifically in the context of distributed transactions, this invariant is: **all nodes participating in transactions maintain consistent state**: either all successfully commit or all fail and rollback, without some nodes succeeding and others failing.

- In the context of distributed systems, the concept of **Linearizability** is: **multi-replica systems can behave externally as if there's only a single replica** (the system guarantees that values read from any replica are the latest), **and all operations take effect atomically** (once a new value is read by any client, subsequent reads will never return old values).

- Linearizability might sound unfamiliar, but mentioning its other name makes it clear: **strong consistency**, and some nicknames: **atomic consistency**, **immediate consistency**, or **external consistency** all refer to it.

These two "consistencies" are completely different things, but there are subtle connections between them, and the bridge between them is **Consensus**.

--------------

## Simply Put

- **Distributed transaction consistency** introduces availability problems due to coordinator single points of failure
- To solve availability problems, distributed transaction nodes need to reach **consensus** on selecting new coordinators when coordinators fail
- **Solving the consensus problem** is equivalent to implementing **linearizable** storage
- **Solving the consensus problem** is equivalent to implementing **total order broadcast**
- **Paxos/Raft implement total order broadcast**

--------------

## Specifically Speaking

- **To ensure distributed transaction consistency**, distributed transactions usually need a **Coordinator/Transaction Manager** to decide the final commit state of transactions. But whether 2PC or 3PC, neither can handle coordinator failures and have tendencies to amplify failures. This sacrifices reliability, maintainability, and scalability. To make distributed transactions truly **available**, nodes need to quickly elect a new coordinator to resolve conflicts when coordinators fail, which requires all nodes to reach **Consensus** on who is the boss.

- **Consensus** means having several nodes agree on something, which can be used to determine which of several **mutually incompatible** operations is the winner. The consensus problem is usually formalized as: one or more nodes can **propose** certain values, and the consensus algorithm **decides** to adopt one of these values. In scenarios ensuring **distributed transaction consistency**, each node can vote and propose, and reach consensus on who is the new coordinator.

- The consensus problem is equivalent to many problems, with two most typical problems being:

  - Implementing a storage system with **linearizability**
  - Implementing **total order broadcast** (ensuring messages aren't lost and are delivered to each node in the same order)

The Raft algorithm solves the total order broadcast problem. **Maintaining consistency among multiple replica logs actually means having all nodes agree on the same global operation order, which actually means making the log system have linearizability.** Thus solving the consensus problem. (Of course, because the consensus problem is equivalent to implementing strongly consistent storage, Raft's specific implementation `etcd` is actually a linearizable distributed database.)

--------------

## To Summarize

- [Linearizability](https://en.wikipedia.org/wiki/Linearizability) is a precisely defined term. Linearizability is a **[consistency model](https://en.wikipedia.org/wiki/Consistency_model)** that makes very strong guarantees about distributed system behavior.

- **Consistency in distributed transactions** is consistent with the C in transaction ACID and is not a strict technical term. (Because what counts as consistent or inconsistent is actually determined by applications. In distributed transaction scenarios, it can be considered as: **all nodes' transaction states always remain the same**)

- **Distributed transaction consistency itself is guaranteed by atomic operations within coordinators and multi-phase commit protocols, not requiring consensus**; but solving availability problems caused by distributed transaction consistency requires consensus.

## Reference Reading

[1] [Consistency and Consensus](https://github.com/Vonng/ddia/blob/master/ch9.md)