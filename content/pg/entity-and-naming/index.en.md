---
title: "Database Cluster Management Concepts and Entity Naming Conventions"
linkTitle: "Database Management Entities and Naming Conventions"
date: 2020-06-03
author: vonng
summary: >
  Concepts and their naming are very important. Naming style reflects an engineer's understanding of system architecture. Poorly defined concepts lead to communication confusion, while carelessly set names create unexpected additional burden. Therefore, they need careful design.
tags: [PostgreSQL,PG Administration,Architecture]
---

> Author: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/))

> "Once named, it can be spoken; once spoken, it can be acted upon."

Concepts and their naming are very important. Naming style reflects an engineer's understanding of system architecture. Poorly defined concepts lead to communication confusion, while carelessly set names create unexpected additional burden. Therefore, they need careful design.

## TL;DR

![entity-naming.png](entity-naming.png)

* **Cluster** is the basic autonomous unit, with unique identifiers specified by users, expressing business meaning, serving as the top-level namespace.
* Clusters contain a series of **Nodes** at the hardware level - physical machines, VMs (or Pods), uniquely identifiable by IP.
* Clusters contain a series of **Instances** at the software level - software servers, uniquely identifiable by IP:Port.
* Clusters contain a series of **Services** at the service level - accessible domain names and endpoints, uniquely identifiable by domain names.
* Cluster naming can use any name conforming to DNS domain specifications, but cannot contain dots ([a-zA-Z0-9-]+).
* Node/Pod naming uses Cluster name prefix followed by `-` connecting a sequence number starting from 0 (consistent with k8s).
* Instance naming usually stays consistent with Node, using `${cluster}-${seq}` format. This implies 1:1 deployment assumption between nodes and instances. If this assumption doesn't hold, independent sequence numbers can be used while maintaining the same naming rules.
* Service naming uses Cluster name prefix followed by `-` connecting service-specific content like `primary`, `standby`.

Using the above diagram as example, the test database cluster is named "`pg-test`". This cluster consists of three database server instances - one primary and two standbys - deployed on the cluster's three nodes. The `pg-test` cluster provides two external services: read-write service `pg-test-primary` and read-only replica service `pg-test-standby`.

## Basic Concepts

In Postgres cluster management, we have these concepts:

### **Cluster**

**Cluster** is the basic autonomous business unit, meaning the cluster can organize as a whole to provide external services. Similar to Deployment concept in k8s. Note this cluster is a software-level concept - don't confuse with PG Cluster (database cluster, single PG Server Instance containing multiple PG Database instances) or Node Cluster (machine cluster).

Cluster is one of the basic management units, an organizational unit for integrating various resources. For example, a PG cluster might include:

* Three physical machine nodes
* One primary instance providing database read-write services
* Two standby instances providing database read-only replica services  
* Two external services: read-write service, read-only replica service

Each cluster has a unique identifier defined by users based on business needs. In this example, we define a database cluster named `pg-test`.

### Node

**Node** is an abstraction of hardware resources, usually referring to a working machine, whether physical (bare metal) or virtual machine (vm), or Pod in k8s. Note that in k8s, Node is hardware resource abstraction, but in actual management usage, Pods in k8s are more similar to the Node concept here. In any case, the key elements of nodes are:

* Nodes are abstractions of hardware resources that can run a series of software services
* **Nodes can use IP addresses as unique identifiers**

Although `lan_ip` addresses can be used as node unique identifiers, for management convenience, nodes should have human-readable, meaningful names as node Hostnames, serving as another common node unique identifier.

### Service

Service is a **named abstraction** of software services (like Postgres, Redis). Services can have various implementations, but their key elements are:

* **Addressable service names** for external access, such as:
  * A DNS domain name (`pg-test-primary`)
  * An Nginx/Haproxy Endpoint
* **Service traffic routing resolution and load balancing mechanisms** to determine which instance handles requests, such as:
  * DNS L7: DNS resolution records
  * HTTP Proxy: Nginx/Ingress L7: Nginx Upstream configuration
  * TCP Proxy: Haproxy L4: Haproxy Backend configuration
  * Kubernetes: Ingress: **Pod Selector**

The same database cluster usually includes primary and standby databases, providing read-write service (primary) and read-only replica service (standby) respectively.

### Instance

Instance refers to **a specific database server** - it can be a single process, a group of processes sharing fate, or several tightly coupled containers in a Pod. The key elements of instances are:

* Uniquely identifiable by IP:Port
* Capable of processing requests

For example, we can view a Postgres process, its dedicated Pgbouncer connection pool, PgExporter monitoring component, high availability component, and management Agent as a service-providing whole - a database instance.

Instances belong to clusters. Each instance has its own unique identifier within the cluster for differentiation.

Instances are resolved by services. Instances provide addressability while Services resolve request traffic to specific instance groups.

## Naming Rules

![entity-naming.png](entity-naming.png)

An object can have many **Tags** and **Metadata/Annotations**, but usually only one name.

Managing databases and software is similar to managing children or pets - both need careful attention. Naming is a very important part of this work. Careless names (like XÆA-12, NULL, Shi Zhenxiang) might introduce unnecessary trouble (additional complexity), while well-designed names can have unexpected benefits.

Generally, object naming should follow these principles:

* Simple and straightforward, human-readable: Names are for people, so they should be memorable and easy to use
* Reflect functionality, show characteristics: Names should reflect key characteristics of objects
* Unique identification: Names should be unique within their namespace and category for unique identification and addressing

* Don't stuff too many unrelated things into names: Embedding lots of important metadata in names is attractive but painful to maintain. Example anti-pattern: `pg:user:profile:10.11.12.13:5432:replica:13`

### Cluster Naming

Cluster names essentially serve as namespaces. All resources belonging to this cluster will use this namespace.

**Cluster naming format**: Recommend adopting DNS standard [RFC1034](https://tools.ietf.org/html/rfc1034) naming rules to avoid future migration pitfalls. For example, if you want to move to the cloud someday and find your old names aren't supported, you'll have to rename everything - massive cost.

I think a better approach is stricter limitations: cluster names shouldn't include **dots**. Should only use lowercase letters, numbers, and **hyphens** `-`. This way, all objects in the cluster can use this name as prefix for various purposes without worrying about breaking constraints. Cluster naming rules:

```c
cluster_name := [a-z][a-z0-9-]*
```

The emphasis on not using **dots** in cluster names is because a popular naming method used to be `com.foo.bar` - dot-separated hierarchical naming. While simple and fast, this has a problem: user-given names might have arbitrary hierarchy levels, making quantity uncontrollable. If clusters need to interact with external systems with naming constraints, such names cause trouble. A direct example is k8s Pods, whose naming rules don't allow `.`.

**Cluster naming semantics**: Recommend two-segment, three-segment names separated by `-`:

```bash
<cluster-type>-<business>-<business-line>
```

For example, `pg-test-tt` represents the `test` cluster under `tt` business line, type `pg`. `pg-user-fin` represents the `user` service under `fin` business line. When using multi-segment naming, it's best to keep segment count fixed.

### Node Naming

Node naming should adopt k8s Pod-consistent naming rules:

```
<cluster_name>-<seq>
```

Node names are determined during cluster resource allocation. Each node gets a sequence number `${seq}` - auto-incrementing integer starting from 0. This aligns with k8s StatefulSet naming rules, enabling consistent cloud-on-premises management.

For example, cluster `pg-test` has three nodes, so these nodes can be named:
`pg-test-0`, `pg-test-1`, and `pg-test-2`.

Node naming remains constant throughout cluster lifecycle, facilitating monitoring and management.

### Instance Naming

For databases, exclusive deployment is usually adopted - one instance occupies the entire machine node. PG instances correspond one-to-one with Nodes, so Node identifiers can simply be used as Instance identifiers. For example, the PG instance on node `pg-test-1` is named: `pg-test-1`, and so on.

Exclusive deployment has great advantages - one node equals one instance, minimizing management complexity. Mixed deployment needs usually come from resource utilization pressure, but VMs or cloud platforms can effectively solve this problem. Through VM or pod abstraction, even each redis instance (1 core 1GB) can have an exclusive node environment.

As convention, node 0 in each cluster serves as the default primary because it's the first allocated node during initialization.

### Service Naming

Usually, databases provide two basic services: `primary` read-write service and `standby` read-only replica service.

Services can adopt simple naming rules:

```ini
<cluster_name>-<service_name>
```

For example, the `pg-test` cluster contains two services: read-write service `pg-test-primary` and read-only replica service `pg-test-standby`.

Another popular instance/node naming rule is: `<cluster_name>-<service_role>-<sequence>` - embedding database primary-standby identity into instance names. This naming has pros and cons. Pros: you can immediately see which instance/node is primary and which are standby during management. Cons: once Failover occurs, instance and node names must be adjusted to maintain consistency, creating additional maintenance work. Additionally, services and node instances are relatively independent concepts. This Embedding naming distorts this relationship, making instances uniquely belong to services. But complex scenarios might not satisfy this assumption. For example, clusters might have several different service division methods with potential overlaps:

* Readable standby (resolves to all instances including primary)
* Synchronous standby (resolves to standbys using synchronous commit)
* Delayed standby, backup instance (resolves to specific instances)

Therefore, don't embed service roles in instance names - maintain target instance lists in services instead.

## Summary

Naming belongs to quite experiential knowledge, rarely discussed specifically anywhere. These "details" often reflect the namer's experience level.

Objects can be identified not only by ID and names, but also through Labels and Selectors. This approach is actually more universal and flexible. The next article in this series (maybe) will introduce label design and management for database objects.

> [WeChat Column](https://mp.weixin.qq.com/s/_C6cxh1e-pxqB_6viJPa8w)