---
title: Refuting "Why You Still Shouldn't Hire a DBA"
date: 2023-03-01
hero: /hero/no-dba-bullshit.jpg
author: |
  [Feng Ruohang](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [WeChat Official Account](https://mp.weixin.qq.com/s/CMRrqI2yBWlNbACHpNgL1g)
summary: >
  Guo Degang has a comedy routine: "Say I tell a rocket scientist, your rocket is no good, the fuel is wrong. I think it should burn wood, better yet coal, and it has to be premium coal, not washed coal. If that scientist takes me seriously, he loses."
tags: [cloud-exit,RDS,DBA]
---

> *Guo Degang has a comedy routine: "Say I tell a rocket scientist, your rocket is no good, the fuel is wrong. I think it should burn wood, better yet coal, and it has to be premium coal, not washed coal. If that scientist takes me seriously, he loses."*

But regardless, Ma is still a respectable Swedish R&D engineer. Having never worked as a DBA yet daring to make sweeping generalizations and inflammatory statements takes considerable courage. We've crossed swords before in "[Why Are You Still Hiring DBAs](https://mp.weixin.qq.com/s/PqCD80H927s0yJrBr4QQqw)" and my response "[Are Cloud Databases an IQ Tax](/cloud/rds)".

When someone throws mud at everyone in this profession, someone needs to stand up and speak out. Therefore, I'm writing today to refute Ma's fallacious arguments in "[Why You Still Shouldn't Hire a DBA](https://mp.weixin.qq.com/s/CMRrqI2yBWlNbACHpNgL1g)".

[![](featured.jpg)](https://mp.weixin.qq.com/s/CMRrqI2yBWlNbACHpNgL1g)

-------

**Ma's three arguments:**

1. DBAs hinder development teams from delivering new features

2. DBAs threaten enterprise data security

3. Manual DBAs need to be replaced by code-based software


**My perspective:**

1. The first point is invalid output - DBAs exist precisely to balance development on the stability side.

2. The second point is complete nonsense - DBAs are critical positions like finance that require trust.

3. The third point contains partial truth but severely overestimates short-term changes, and cloud databases aren't the only path.

Let me elaborate:


### DBAs Are Responsible for Stability

A fundamental principle of information systems is that **safety and liveness are in conflict** - overemphasizing safety and stability hurts liveness; overemphasizing liveness makes stability difficult. Any organization must find a **balance** between the two. Development and operations are the functional embodiments of these forces.

Development is responsible for new features, while SRE/DBAs are responsible for stability - one creates, one maintains, they collaborate but also check each other. Ma, as a developer, especially a startup developer, advocating for feature liveness is understandable from his position. But in larger organizations, **stability's position is often higher than new features**. Mature organizations like banks and large internet platforms always prioritize **stability above all**. After all, new features have uncertain benefits, while major outages have visible losses. Deploying 10 new versions daily might not bring much growth, but one major outage can destroy months of effort.

**"The obstacle to driving 200 mph on the highway was never the car's performance, but the driver's courage."** From a higher management perspective, Ma's emphasis on *"firing DBAs for faster DB delivery speed"* is pure developer wishful thinking: outsource operations to the cloud, no checks and balances, I can do whatever I want. **If such thinking were implemented, it would inevitably result in painful lessons at some point.**

I was once a DBA but also did plenty of Dev work. I have firsthand experience with both development and DBA mindsets. When I first started as a developer, I ran neural networks, recommendation systems, web servers, and crawlers "in the PostgreSQL database," used FDW to connect MongoDB, HBase, and a bunch of external systems. Stability? It ran fine! Until no operations or DBA was willing to maintain it, and I had to become a DBA myself to eat my own dog food and take responsibility. Only then did I develop empathy for DBAs/operations and learn to choose carefully what to do and what not to do.



### Who Cares About Delivery Speed?

**Evaluating a database requires considering many dimensions: stability, reliability, security, simplicity, scalability, extensibility, observability, maintainability, cost-effectiveness**, etc. **Delivery speed** barely qualifies as a minor subsidiary dimension within "scalability" and doesn't rank high among database system attributes that need attention.

More importantly, **cost-effectiveness is the primary product strength**. **Comparing solutions while ignoring costs is dishonest behavior**. I understand this developer psychology very well: **spending company money saves personal effort, so naturally few people are motivated to save money for the company**. Your boss and leadership won't care whether your database takes 30 minutes or 3-4 days to deploy. But your boss will care a lot if you spin up a database in 30 minutes and then add hundreds of thousands to the monthly bill.

![meme.png](no-dba-bullshit-meme.png)

Take AWS's 64-core 256GB `db.m5.16xlarge` RDS as an example, costing $25,817/month (about 180,000 RMB). One month's rent could buy two servers with much better performance outright. Any rational enterprise user can see the logic: **if purchasing such services isn't for short-term, temporary needs, it's absolutely a major financial misconduct**.



### Not Afraid of Delivery Speed Competition Either

But even if we step back ten thousand paces and say delivery speed really matters, Ma's proof case is full of holes.

Ma imagined a database deployment scenario: new PG version, dual-site three-center, same-city HA, remote disaster recovery, data encryption, automatic backup, built-in monitoring, app and DB separate networks, even DBAs can't delete databases. Then proudly claimed: "Using Terraform, I can complete all these requirements in just 28 minutes! Orders of magnitude faster than getting DBAs to build databases!"

Actually, with machines ready, networks connected, and planning complete: using Pigsty to deploy a database system meeting these requirements takes only about ten minutes. Not to mention self-built data centers, Pigsty can use the same logic: Terraform one-click EC2, storage, networking, then execute one additional command to [deploy databases](https://github.com/Vonng/pigsty/blob/master/terraform/spec/aws-cn.tf), taking possibly less time than Terraform alone. More importantly, **it saves 80-90% of the sky-high RDS [IQ tax](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485292&idx=1&sn=4f650c3f5c3fb5207c55ff67e44d7d8a&chksm=fe4b32b7c93cbba190e60d477061d19a165e1f9b074beb00b132ae1369a9fd2c7d10ed77a013&scene=21#wechat_redirect)**.

![price.jpeg](no-dba-bullshit-price.jpeg)

> The cloud database product manager who came up with this pricing must have had their head slammed in a door



### The Strawman of Sharding

Ma argues that database sharding is a tool DBAs use to inflate their value.

> Today, database capabilities have developed tremendously, and sharding that brings huge management costs to application developers is no longer necessary. Any system using sharding can be replaced with distributed databases or NoSQL databases. We can almost say that sharding is just a tool DBAs use to inflate their value.

To this day, **hardware storage technology development has left many old-timers unable to keep up with new trends**. Consumer PCIe NVMe SSD 2TB prices have entered three digits, commonly used enterprise-grade 3.2TB MLC NVMe SSDs cost only six to seven thousand, with maximum single-card capacities of tens of TBs. This completely outclasses many medium to large enterprises' total TB data volumes. Seven-digit IOPS makes thousands/tens of thousands IOPS cloud EBS selling at sky-high prices want to find a hole to hide in.

Software-wise, take PostgreSQL as an example: single tables using heap storage can handle tens of TBs and hundreds of billions of records without problem, plus the Citus extension can transform it into a distributed database in place. Various distributed databases' selling point is also "no need for sharding." This is all old news. Except for very specific scenarios, probably only orthodox MySQL users still play with sharding based on "single tables can't exceed 20M records."

Of course, distributed databases require **higher, not lower** DBA skill levels. So what Ma mainly wants to say here is NoSQL, more specifically DynamoDB - this supposedly "maintenance-free" database that can directly eliminate DBAs. However, a database with 10ms average latency, a flat KV storage abstraction equivalent to a file system, and RCU/WCU billing that's even more predatory than RDS - what qualifies it to claim it can replace DBAs?



## Expecting NoSQL to Replace DBAs Is Dreaming

Internet applications are mostly **data-intensive applications**. For real-world data-intensive applications, unless you're prepared to build foundational components from scratch, there aren't many opportunities to play with fancy data structures and algorithms. In actual production, **data tables are data structures, indexes and queries are algorithms**. Application development code often plays the role of **glue**, handling IO and business logic, with most other work being **moving data between data systems**.

In the broadest sense, **wherever there's state, there are databases**. They're everywhere - behind websites, inside applications, in standalone software, in blockchains. **Relational databases are just the tip of the iceberg** (or the peak of the iceberg) of data systems. In reality, there are various data system components:

- **Databases**: Store data so you or other applications can find it later (PostgreSQL, MySQL, Oracle)
- **Caches**: Remember results of expensive operations to speed up reads (Redis, Memcached)  
- **Search indexes**: Allow users to search data by keywords or filter in various ways (ElasticSearch)
- **Stream processing**: Send messages to other processes for asynchronous processing (Kafka, Flink, Storm)
- **Batch processing**: Periodically process accumulated large batches of data (Hadoop)

State management is an eternal problem in information systems. Ma thinks DBAs are typists clutching ancestral Oracle manuals, but internet company DBAs have become **data architects** mastering eighteen martial arts. **One of an architect's most important abilities is understanding these components' performance characteristics and use cases, being able to flexibly weigh trade-offs and integrate these data systems.** They push business teams toward best practices and pattern design at the top, dive deep into operating systems and hardware for troubleshooting and performance optimization at the bottom, and master countless data components in between. A gentleman is not a tool - relational database knowledge is just the most core and important part.

As I said in "[Why Learn Database Principles and Design](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247483673&idx=1&sn=2a895a6f6e4b3e882395203757ec4e60&chksm=fe4b34c2c93cbdd49686c79ba27327b0dd16f266a82ab7de6e9985b8808207646fa1c7796da4&scene=21#wechat_redirect)," those who only write code are code farmers; **learn databases well, and you can basically make a living**; add **operating systems and computer networks** on top of that, and you can be a decent programmer. Unfortunately, data modeling and SQL have almost become lost arts: this foundational knowledge is being forgotten by **new generation engineers** who design ridiculous schemas, don't know how to create indexes properly, then hastily conclude that relational databases and SQL are garbage, we must use crude and fast NoSQL to save time. However, people always need reliable systems to handle critical business data: in many enterprises, core data is still a regular relational database as **Source of Truth**, with NoSQL databases only used for non-critical data. Any developer jumping out to say DynamoDB/Redis/MongoDB/HBase is so awesome, I can put all my state there and never need DBAs again, is undoubtedly ridiculous.



### DBAs Are Guardians of Enterprise Databases

Ma's final shot targets DBA professional ethics: DBAs who want to delete databases can't be stopped by anyone.

This isn't wrong - DBAs and finance are both critical positions capable of fatal damage to enterprises: trust those you employ, don't employ those you don't trust. But this statement sidesteps an important fact: without DBAs gatekeeping, everyone can delete databases. In the Weimob and Baidu database deletion cases Ma cited, the perpetrators were ordinary developers and operations staff. It was precisely because there were no competent DBAs to gatekeep that database deletion opportunities arose.

Qualified DBAs can effectively reduce the range of people capable of delivering fatal blows to enterprises, narrowing it from all developers and operations to DBAs themselves. As for how to check DBAs themselves, either have two DBAs back each other up, or have operations/security teams manage cold backup deletion permissions. Ma's example of Tencent Cloud not allowing manual deletion of routine backups shows ignorance of industry practices.

I despise and am outraged by behavior that throws dirty water on the DBA community 😄. Following this logic, I could completely argue that the public cloud vendors Ma loves are the biggest threat to data security: using cloud is just outsourcing operations and DBAs to cloud vendors, **and you absolutely cannot prevent some privileged developer/operations/DBA at a cloud vendor from casually browsing your database or simply downloading a backup for entertainment. You have no recourse, no evidence, and mainly because you have no ability to know this happened**. There are many such people, one operations script glitch can blow up a large area, and the compensation you can expect is just painless service credit vouchers.

Reference reading: "[Cloud RDS: From Database Deletion to Running Away](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485093&idx=1&sn=5815f71f1d832101d35a75f5aa4acd3c&chksm=fe4b337ec93cba68fbf30eb0ed50d052c6e8972d42cf506051b5016668f4555edaa0756688dc&scene=21#wechat_redirect)"



### DBAs Retiring from History?

As an overall industry, DBAs are indeed on a downward trajectory, but people always overestimate short-term impact while underestimating long-term trends. Many large organizations employ DBAs. DBAs are like Cobol programmers - those unglamorous manufacturing industries, banks, insurance, securities, and vast government/military departments running local software heavily use relational databases. In the foreseeable future, DBAs finding work somewhere won't be a problem.

But the big trend is that databases themselves will become more intelligent and easier to use, while various tools, SaaS, PaaS continue emerging, further lowering database usage barriers. The emergence of public/private cloud DBaaS further reduces database management barriers. Lower technical barriers for databases will reduce DBA irreplaceability: the good old days of charging hundreds of thousands for software installation and millions for data recovery are gone forever. But in another sense, this also liberates DBAs from operational trivia, allowing them to invest more time in valuable performance optimization, hazard investigation, and system building.

Whether it's public cloud vendors or Kubernetes-represented cloud-native/private cloud, the core value is **using software, not people, to handle system complexity as much as possible**. But don't expect these to completely replace DBAs: cloud isn't maintenance-free operations outsourcing magic. According to complexity conservation law, whether system administrators or database administrators, the only way for administrator positions to disappear is being renamed "DevOps Engineer" or SRE/DRE. Good cloud software can help you shield operational chores and solve 70% of high-frequency daily problems, but there will always be complex problems only humans can handle. You might need fewer people to manage this cloud software, but you still need people to manage it. After all:

**You also need knowledgeable people to coordinate and handle things, so you won't be harvested like leeks by cloud vendors treating you like idiots.**

Sidebar: Some developers always want to use cloud - this operations outsourcing - cloud databases, cloud XX to eliminate DBA jobs. We made an out-of-the-box cloud database RDS PostgreSQL local open-source alternative **Pigsty**, recently released version 2.0 with monitoring/database out-of-the-box HA/PITR/IaC complete. It allows you to run enterprise-grade database services at near-hardware costs without database experts, saving 50%-90% of the "expertise tax" paid to RDS, making RDS look like a big joke in every aspect except its vaunted elasticity. For DBAs, this is a weapon to fight back. Let's be frank - we're here to destroy cloud database jobs and end developers' pipe dreams. https://pigsty.cc/zh/docs/feature

Finally, let's end today's topic with a copyright-free joke generated by some Notion AI.

![joke.png](no-dba-bullshit-joke.png)