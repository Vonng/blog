---
title: "Can Oracle Still Save MySQL?"
date: 2024-06-21  
summary: >
  Percona founder Peter Zaitsev publicly expressed disappointment with MySQL and its IP owner Oracle in an official blog post, as well as dissatisfaction with performance degradation in newer versions. This is indeed a signal worth attention.
showAuthor: false
series: ["MySQL's Farewell"]
series_order: 4
tags: [database,MySQL]
---

> Author: [Peter Zaitsev](https://www.percona.com/blog/author/pz/) | Translator: [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat Original](https://mp.weixin.qq.com/s/0OgcduKvmprBcECgtn73Cg) | [Percona's Blog](https://www.percona.com/blog/can-oracle-save-mysql/)

As the main flag-bearer of the MySQL ecosystem, Percona has developed a series of tools familiar to users: PMM monitoring, XtraBackup backup, PT series tools, and MySQL distributions.
However, recently, Percona founder Peter Zaitsev publicly expressed disappointment with MySQL and its IP owner Oracle in an official blog post, as well as dissatisfaction with performance degradation in newer versions. This is indeed a signal worth attention.

- [Oracle Finally Killed MySQL](/db/can-oracle-save-mysql/)
- [Percona: Sakila, Where Are You Going?](/db/sakila-where-are-you-going)

> Author: Percona Blog, Marco Tusa, an important contributor to the MySQL ecosystem who developed the well-known PT series tools, MySQL backup tools, monitoring tools, and distributions.
>
> Translator: Feng Ruohang, alias Vonng, author of Pigsty, PostgreSQL expert and evangelist. Advocate of cloud exit, practitioner of database cloud exit.


I previously wrote an article [Oracle Finally Killed MySQL](/db/oracle-kill-mysql/) which generated quite a response - including several excellent articles on The Register ([1](https://www.theregister.com/2024/06/11/early_mysql_engineer_questions_whether/), [2](https://www.theregister.com/2024/06/14/oracles_love_and_hate_relationship/)). This indeed raised several questions worth discussing:

> **AWS and other cloud vendors compete without giving anything back, what else would you expect Oracle to do?**

First - I think it would be great if AWS and other cloud providers would contribute more to MySQL.
However, we should also note that Oracle is a competitor to many of these companies, and there's no level playing field when it comes to MySQL (why AWS would participate in this unfair competition is another topic).

Contributing intellectual property to your competitor might not be a great business decision, especially considering the CLA (Contributor License Agreement) that Oracle requires contributors to sign.
As long as Oracle owns this intellectual property, the reasonable expectation is that Oracle itself should bear most of the responsibility for maintaining, improving, and promoting MySQL.

Yes..., but if Oracle is unwilling or no longer capable of being a good MySQL steward and only focuses on its own cloud version, just like AWS only focuses on its RDS and Aurora services, what can we do?

**There is a solution - Oracle should transfer MySQL Community to Linux Foundation, Apache Foundation, or other independent entity, allow fair competition, and focus on their Cloud (Heatwave) and Enterprise products.** Interestingly, Oracle already has such a precedent: [transferring OpenOffice to Apache Software Foundation](https://www.zdnet.com/article/oracle-gives-openoffice-to-apache/).

Another great example is [LinkerD](https://linkerd.io/) - which was [brought to CNCF](https://linkerd.io/2017/01/24/linkerd-joins-the-cloud-native-computing-foundation/) by Buoyant - which continues to build its extended version - [Buoyant Enterprise for LinkerD](https://buoyant.io/linkerd-enterprise).

In this case, maintaining and developing open source MySQL becomes an ecosystem problem: I'm quite sure AWS and other cloud vendors would be willing to participate more if they weren't contributing to IP owned by their competitors. We can actually see cloud vendors participating heavily in PostgreSQL, Linux, or Kubernetes projects.

> **There is PostgreSQL; who needs MySQL anyway?**

PostgreSQL is indeed an excellent database with an active community and has been growing rapidly in recent years. However, there are still many people who prefer MySQL, and many existing applications are still using MySQL - so we hope MySQL can continue to develop healthily and live long.

There's also another point: if MySQL dies, open source relational databases would essentially be monopolized by PostgreSQL alone, and in my view, monopoly is not a good thing as it leads to stagnation and slowed innovation. For PostgreSQL to reach its full potential, having MySQL as a competitor is not a bad thing.

> **Isn't MariaDB a new, better, community-governed MySQL?**

I think MariaDB's existence has been great at putting pressure on Oracle, forcing it to invest in MySQL. While we can't know for certain what would have happened without MariaDB, MySQL would likely have been neglected by Oracle much earlier without it.

That said, while MariaDB is organizationally very different from Oracle, it's obviously not a database that's "owned and governed by the community" like PostgreSQL, nor does it have as broad independent corporate contributors as PostgreSQL. I think MariaDB could indeed take some measures to compete for leadership in the MySQL space, but that deserves a separate article.

**To summarize**

PostgreSQL and MariaDB are excellent databases, and without them, the open source community would be in a very bad bind with Oracle's current MySQL stewardship. But neither is quite a MySQL replacement today, and the best outcome for the MySQL community would be for Oracle to come to terms and work with the community to build MySQL into the best database it can be. If not, the MySQL community needs a plan B.



------

## References

[Can Oracle Save MySQL?](https://www.percona.com/blog/can-oracle-save-mysql/)

[MySQL Performance Getting Worse, Where is Sakila Going?](/db/sakila-where-are-you-going/)

[Why is MySQL's Correctness So Garbage?](/db/bad-mysql/)

[Is Oracle Finally Killing MySQL?](https://www.percona.com/blog/is-oracle-finally-killing-mysql/)

[Can Oracle Save MySQL?](https://www.percona.com/blog/can-oracle-save-mysql/)

[Sakila, Where Are You Going?](https://www.percona.com/blog/sakila-where-are-you-going/)

[Postgres vs MySQL: the impact of CPU overhead on performance](https://smalldatum.blogspot.com/2023/10/postgres-vs-mysql-impact-of-cpu.html)

[Perf regressions in MySQL from 5.6.21 to 8.0.36 using sysbench and a small server](https://smalldatum.blogspot.com/2024/02/perf-regressions-in-mysql-from-5621-to.html)




--------

## English Original

I got quite a response to my article on whether [Oracle is Killing MySQL,](https://www.percona.com/blog/is-oracle-finally-killing-mysql/) including a couple of great write-ups on The Register ([1](https://www.theregister.com/2024/06/11/early_mysql_engineer_questions_whether/), [2](https://www.theregister.com/2024/06/14/oracles_love_and_hate_relationship/)) on the topic. There are a few questions in this discussion that I think are worth addressing. 

> **AWS and other cloud vendors compete, without giving anything back, what else would you expect Oracle to do ?**

First, yes. I think it would be great if AWS and other cloud providers would contribute more to MySQL. We should note, though, that Oracle is a competitor for many of those companies, and there is no "level playing field" when it comes to MySQL (the fact AWS is willing on this unlevel field is another point). Contributing IP to your competitor, especially considering CLA Oracle requires might not be a great business decision. Until Oracle owns that IP, it is reasonable to expect, for Oracle to have most of the burden to maintain, improve, and promote MySQL, too.

Yes… but what if Oracle is unwilling or unable to be a great MySQL steward anymore and would rather only focus on its cloud version, similar to AWS being solely focused on its RDS and Aurora offerings?  ***There is a solution for that – Oracle should transfer MySQL Community to Linux Foundation, Apache Foundation, or another independent entity, open up the level playing field, and focus on their Cloud (Heatwave) and Enterprise offering.\*** Interestingly enough, there is already a precedent for that with Oracle [transferring OpenOffice to Apache Software Foundation](https://www.zdnet.com/article/oracle-gives-openoffice-to-apache/).

Another great example would be[ LinkerD](https://linkerd.io/) — which [was brought to CNCF](https://linkerd.io/2017/01/24/linkerd-joins-the-cloud-native-computing-foundation/) by Buyant — which continues to build its extended edition[ – Buoyant Enterprise for LinkerD](https://buoyant.io/linkerd-enterprise).

In this case, maintaining and growing open source MySQL will become an ecosystem problem and I'm quite sure AWS and other cloud vendors will participate more when they are not contributing to IP owned by their competitors. We can actually see it with PostgreSQL, Linux, or Kubernetes projects which have great participation from cloud vendors.

> **There is PostgreSQL; who needs MySQL anyway?** 

Indeed, PostgreSQL is a fantastic database with a great community and has been growing a lot recently. Yet there are still a lot of existing applications on MySQL and many folks who prefer MySQL, and so we need MySQL healthy for many years to come. But there is more; if MySQL were to die, we would essentially have a monopoly with popular open source relational databases, and, in my opinion, monopoly is not a good thing as it leads to stagnation and slows innovation. To have PostgreSQL to be as great as it can be it is very helpful to have healthy competition from MySQL!

> **Isn't MariaDB a new, better, community-governed MySQL ?**

I think MariaDB's existence has been great at putting pressure on Oracle to invest in MySQL. We can't know for certain "what would have been," but chances are we would have seen more MySQL neglect earlier if not for MariaDB. Having said that, while organizationally, MariaDB is not Oracle, it is not as cleanly "community owned and governed" as PostgreSQL and does not have as broad a number of independent corporate contributors as PostgreSQL.I think there are steps MariaDB can do to really take a leadership position in MySQL space… but it deserves another article.

**To sum things up** 

PostgreSQL and MariaDB are fantastic databases, and if not for them, the open source community would be in a very bad bind with Oracle's current MySQL stewardship. Neither is quite a MySQL replacement today, and the best outcome for the MySQL community would be for Oracle to come to terms and work with the community to build MySQL into the best database it can be. If not, the MySQL community needs to come up with a plan B.