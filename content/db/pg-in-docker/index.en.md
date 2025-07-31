---
title: Is running postgres in docker a good idea?
linkTitle: "PG in Docker: Good or Bad?"
date: 2019-01-13
author: |
  [Ruohang Feng](https://vonng.com/en/) ([@Vonng](https://vonng.com/en/))
description: Thou shalt not run a prod database inside a container
tags: [Database,Docker]
---

For stateless app services, containers are an almost perfect devops solution. However, for stateful services like databases, it's not so straightforward. Whether production databases should be containerized remains controversial.

From a developer's perspective, I'm a big fan of Docker & Kubernetes and believe that they might be the future standard for software deployment and operations. But as a database administrator, I think hosting production databases in Docker/K8S is still a bad idea.


--------------

## What problems does Docker solve?

Docker is described with terms like lightweight, standardized, portable, cost-effective, efficient, automated, integrated, and high-performance in operations. These claims are valid, as Docker indeed simplifies both development and operations. This explains why many companies are eager to containerize their software and services. However, this enthusiasm sometimes goes to the extreme of containerizing everything, including **production databases**.

Containers were originally designed for **stateless** apps, where temporary data produced by the app is logically part of the container. A service is created with a container and destroyed after use. These apps are stateless, with the state typically stored outside in a database, reflecting the classic architecture and philosophy of containerization.

But when it comes to containerizing the production database itself, the scenario changes: databases are stateful. To maintain their state without losing it when the container stops, database containers need to "punch a hole" to the underlying OS, which is named data volumes.

Such containers are no longer ephemeral entities that can be freely created, destroyed, moved, or transferred; they become bound to the underlying environment. Thus, the many advantages of using containers for traditional apps are not applicable to database containers.



--------------

## Reliability

Getting software up & running is one thing; ensuring its reliability is another. Databases, central to information systems, are often critical, with failure leading to catastrophic consequences. This reflects common experience: while office software crashes can be tolerated and resolved with restarts, document loss or corruption is unresolvable and disastrous. Database failure without replica & backups can be terminal, particularly for internet/finance companies.

**Reliability** is the paramount attribute for databases. It's the system's ability to function correctly during adversity (hardware/software faults, human error), i.e. fault tolerance and resilience. Unlike **liveness attribute** such as performance, reliability, a safety attribute, proves itself over time or falsify by failures, often overlooked until disaster strikes.

Docker's description notably omits "reliability" —— the crucial attribute for database.


### Reliability Proof

As mentioned, reliability lacks a definitive measure. Confidence in a system's reliability builds over time through consistent, correct operation (MTTF). Deploying databases on bare metal has been a long-standing practice, proven reliable over decades. Docker, despite revolutionizing DevOps, has a mere ten-year track record, which is insufficient for establishing reliability, especially for mission-critical production databases. In essence, **there haven't been enough "guinea pigs" to clear the minefield**.

### Community Knowledge

Improving reliability hinges on learning from failures. Failures are invaluable, turning unknowns into knowns and forming the bedrock of operational knowledge. **Community experience with failures is predominantly based on bare-metal deployments**, with a plethora of issues well-trodden over decades. Encountering a problem often means finding a well-documented solution, thanks to previous experiences. However, add "Docker" to the mix, and the pool of useful information shrinks significantly. This implies a lower success rate in data recovery and longer times to resolve complex issues when they arise.

> A subtle reality is that, without compelling reasons, businesses and individuals are generally reluctant to share experiences with failures. Failures can tarnish a company’s reputation, potentially exposing sensitive data or reflecting poorly on the organization and team. Moreover, insights from failures are often the result of costly lessons and financial losses, representing core value for operations personnel, thus public documentation on failures is scarce.

### Extra Failure Point

Running databases in Docker doesn't reduce the chances of hardware failures, software bugs, or human errors. Hardware issues persist with or without Docker. Software defects, mainly application bugs, aren't lessened by containerization, and the same goes for human errors. In fact, Docker introduces **extra components, complexity, and failure points, decreasing overall system reliability**.

Consider this simple scenario: if the Docker daemon crashes, the database process dies. Such incidents, albeit rare, are non-existent on bare-metal.

Moreover, the failure points from an additional component like Docker aren’t limited to Docker itself. Issues could arise from interactions between Docker and the database, the OS, orchestration systems, VMs, networks, or disks. For evidence, see the issue tracker for the official PostgreSQL Docker image: https://github.com/docker-library/postgres/issues?q=.

**Intellectual power doesn't easily stack** — a team's intellect relies on the few seasoned members and their communication overhead. Database issues require database experts; container issues, container experts. However, when databases are deployed on kubernetes & dockers, merging the expertise of database and K8S specialists is challenging — you need a dual-expert to resolve issues, and such individuals are rarer than specialists in one domain.

Moreover, one man's meat is another man's poison. Certain Docker features might turn into bugs under specific conditions.

### Unnecessary Isolation

Docker provides process-level isolation, which generally benefits applications by reducing interaction-related issues, thereby enhancing system reliability. However, this isolation isn't always advantageous for databases.

A subtle **real-world case** involved starting two PostgreSQL server on the same data directory, either on the host or one in the host and another inside a container. On bare metal, the second instance would fail to start as PostgreSQL recognizes the existing instance and refuses to launch; however, Docker's **isolation** allows the second instance to start obliviously, potentially **toast** the data files if proper fencing mechanisms (like host port or PID file exclusivity) aren't in place.

Do databases need isolation? Absolutely, but not this kind. Databases often demand dedicated physical machines for performance reasons, with only the database process and essential tools running. Even in containers, they're typically bound exclusively to physical/virtual machines. Thus, the type of isolation Docker provides is somewhat irrelevant for such deployments, though it is a handy feature for cloud providers to efficiently oversell in a multi-tenant environment.



--------------

## Maintainability

> Docker simplify the day one setup, but bring much more troubles on day two operation.

The bulk of software expenses isn't in initial development but in ongoing maintenance, which includes fixing vulnerabilities, ensuring operational continuity, handling outages, upgrading versions, repaying technical debt, and adding new features. Maintainability is crucial for the quality of life in operations work. Docker shines in this aspect with its infrastructure-as-code approach, effectively turning operational knowledge into reusable code, accumulating it in a streamlined manner rather than scattered across various installation/setup documents. Docker excels here, especially for stateless applications with frequently changing logic. Docker and Kubernetes facilitate deployment, scaling, publishing, and rolling upgrades, allowing Devs to perform Ops tasks, and Ops to handle DBA duties (somewhat convincingly).


### Day 1 Setup

Perhaps Docker's greatest strength is the standardization of environment configuration. A standardized environment aids in delivering changes, discussing issues, and reproducing bugs. Using binary images (essentially materialized Dockerfile installation scripts) is quicker and easier to manage than running installation scripts. Not having to rebuild complex, dependency-heavy extensions each time is a notable advantage.

Unfortunately, databases don't behave like typical business applications with frequent updates, and creating new instances or delivering environments is a rare operation. Additionally, DBAs often accumulate various installation and configuration scripts, making environment setup almost as fast as using Docker. Thus, Docker's advantage in environment configuration isn't as pronounced, falling into the "nice to have" category. Of course, in the absence of a dedicated DBA, using Docker images might still be preferable as they encapsulate some operational experience.

Typically, it's not unusual for databases to run continuously for months or years after initialization. The primary aspect of database management isn't creating new instances or delivering environments, but the day-to-day operations — Day2 Operation. Unfortunately, Docker doesn't offer much benefit in this area and can introduce additional complications.

### Day2 Operation

Docker can significantly streamline the maintenance of stateless apps, enabling easy create/destroy, version upgrades, and scaling. However, does this extend to databases?

Unlike app containers, database containers can't be freely destroyed or created. Docker doesn't enhance the operational experience for databases; tools like Ansible are more beneficial. Often, operations require executing scripts inside containers via `docker exec`, adding unnecessary complexity.

CLI tools often struggle with Docker integration. For instance, `docker exec` mixes `stderr` and `stdout`, breaking pipeline-dependent commands. In bare-metal deployments, certain ETL tasks for PostgreSQL can be easily done with a single Bash line.

```bash
psql <src-url> -c 'COPY tbl TO STDOUT' | psql <dst-url> -c 'COPY tdb FROM STDIN'
```

Yet, without proper client binaries on the host, one must awkwardly use Docker's binaries like:

```bash
docker exec -it srcpg gosu postgres bash -c "psql -c \"COPY tbl TO STDOUT\" 2>/dev/null" |\ 
  docker exec -i dstpg gosu postgres psql -c 'COPY tbl FROM STDIN;'
```

complicating simple commands like physical backups, which require layers of command wrapping:

```bash
docker exec -i postgres_pg_1 gosu postgres bash -c 'pg_basebackup -Xf -Ft -c fast -D - 2>/dev/null' | tar -xC /tmp/backup/basebackup
```

> `docker`, `gosu`, `bash`, `pg_basebackup`

Client-side applications (`psql`, `pg_basebackup`, `pg_dump`) can bypass these issues with version-matched client tools on the host, but server-side solutions lack such workarounds. Upgrading containerized database software shouldn't necessitate host server binary upgrades.

Docker advocates for easy software versioning; updating a minor database version is straightforward by tweaking the Dockerfile and restarting the container. However, major version upgrades requiring state modification are more complex in Docker, often leading to convoluted processes like those in https://github.com/tianon/docker-postgres-upgrade.

If database containers can't be scheduled, scaled, or maintained as easily as AppServers, why use them in production? While stateless apps benefit from Docker and Kubernetes' scaling ease, stateful applications like databases don't enjoy such flexibility. Replicating a large production database is time-consuming and manual, questioning the efficiency of using `docker run` for such operations.

Docker's awkwardness in hosting production databases stems from the stateful nature of databases, requiring additional setup steps. Setting up a new PostgreSQL replica, for instance, involves a local data directory clone and starting the `postmaster` process. Container lifecycle tied to a single process complicates database scaling and replication, leading to inelegant and complex solutions. This process isolation in containers, or "abstraction leakage," fails to neatly cover the multiprocess, multitasking nature of databases, introducing unnecessary complexity and affecting maintainability.

In conclusion, while Docker can improve system maintainability in some aspects, like simplifying new instance creation, the introduced complexities often undermine these benefits.


### Tooling

Databases require tools for maintenance, including a variety of operational scripts, deployment, backup, archiving, failover, version upgrades, plugin installation, connection pooling, performance analysis, monitoring, tuning, inspection, and repair. Most of these tools are designed for bare-metal deployments. Like databases, these tools need thorough and careful testing. Getting something to run versus ensuring its stable, long-term, and correct operation are distinct levels of reliability.

A simple example is plugin and package management. PostgreSQL offers many useful plugins, such as PostGIS. On bare metal, installing this plugin is as easy as executing `yum install` followed by `create extension postgis`. However, in Docker, following best practices requires making changes at the image level to persist the extension beyond container restarts. This necessitates modifying the Dockerfile, rebuilding the image, pushing it to the server, and restarting the database container, undeniably a more cumbersome process.

Package management is a core aspect of OS distributions. Docker complicates this, as many PostgreSQL binaries are distributed not as RPM/DEB packages but as Docker images with pre-installed extensions. This raises a significant issue: how to consolidate multiple disparate images if one needs to use two, three, or over a hundred extensions from the PostgreSQL ecosystem? Compared to reliable OS package management, building Docker images invariably requires more time and effort to function properly.

Take monitoring as another example. In traditional bare-metal deployment, **machine metrics** are crucial for database monitoring. Monitoring in containers differs subtly from that on bare metal, and oversight can lead to pitfalls. For instance, the sum of various CPU mode durations always equals 100% on bare metal, but this assumption doesn't necessarily hold in containers. Moreover, monitoring tools relying on the `/proc` filesystem may yield metrics in containers that differ significantly from those on bare metal. While such issues are solvable (e.g., mounting the Proc filesystem inside the container), complex and ugly workarounds are generally unwelcome compared to straightforward solutions.

Similar issues arise with some failure detection tools and common system commands. Theoretically, these could be executed directly on the host, but can we guarantee that the results in the container will be identical to those on bare metal? More frustrating is the emergency troubleshooting process, where necessary tools might be missing in the container, and with no external network access, the Dockerfile→Image→Restart path can be exasperating.

Treating Docker like a VM, many tools may still function, but this defeats much of Docker's purpose, reducing it to just another package manager. Some argue that Docker enhances system reliability through standardized deployment, given the more controlled environment. While this is true, I believe that if the personnel managing the database understand how to configure the database environment, there's no fundamental difference between scripting environment initialization in a Shell script or in a Dockerfile.





--------------

## Scalability

Performance is another point that people concerned a lot. From the performance perspective, the basic principle of  database deployment is: The close to hardware, The better it is.  Additional isolation & abstraction layer is bad for database performance. More isolation means more overhead, even if it is just an additional `memcpy` in the kernel .

For performance-seeking scenarios, some databases choose to bypass the operating system's page management mechanism to operate the disk directly, while some databases may even use FPGA or GPU to speed up query processing. Docker as a lightweight container, performance suffers not much, and the impact to performance-insensitive scenarios may not be significant, but the extra abstract layer will definitely make performance worse than make it better.


--------------

## Summary

Container and orchestration technologies are valuable for operations, bridging the gap between software and services by aiming to codify and modularize operational expertise and capabilities. Container technology is poised to become the future of package management, while orchestration evolves into a "data center distributed cluster operating system," forming the underlying infrastructure runtime for all software. As more challenges are addressed, confidently running both stateful and stateless applications in containers will become feasible. However, for databases, this remains an ideal rather than a practical option, especially in production.

It's crucial to reiterate that the above discussion applies specifically to **production databases**. For development and testing, despite the existence of Vagrant-based virtual machine sandboxes, I advocate for Docker use—many developers are unfamiliar with configuring local test database environments, and Docker provides a clearer, simpler solution. For stateless production applications or those with non-critical derivative state data (like Redis caches), Docker is a good choice. But for core relational databases in production, where data integrity is paramount, one should carefully consider the risks and benefits: What's the value of using Docker here? Can it handle potential issues? Are you prepared to assume the responsibility if things go wrong?

Every technological decision involves balancing pros and cons, like the core trade-off here of **sacrificing reliability for maintainability** with Docker. Some scenarios may warrant this, such as cloud providers optimizing for containerization to oversell resources, where container isolation, high resource utilization, and management convenience align well. Here, the benefits might outweigh the drawbacks. However, in many cases, reliability is the top priority, and compromising it for maintainability is not advisable. Moreover, it's debatable whether using Docker significantly eases database management; sacrificing long-term operational maintainability for short-term deployment ease is unwise.

In conclusion, containerizing production databases is likely not a prudent choice.