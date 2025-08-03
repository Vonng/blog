---
title: "Oracle 还能挽救 MySQL 吗？"
date: 2024-06-21
author: |
  [Peter Zaitsev](https://www.percona.com/blog/author/pz/) | 译：[冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [微信原文](https://mp.weixin.qq.com/s/0OgcduKvmprBcECgtn73Cg) | [Percona's Blog](https://www.percona.com/blog/can-oracle-save-mysql/)
summary: >
  Percona 创始人 Peter Zaitsev 在官方博客上公开表达了对 MySQL，及其知识产权属主 Oracle 的失望，以及对版本越高性能越差的不满，这确实是一个值得关注的信号。
tags: [数据库,MySQL]
---

Percona 作为 MySQL 生态的主要扛旗者，开发了一系列用户耳熟能详的工具：PMM 监控，XtraBackup 备份，PT 系列工具，以及 MySQL 发行版。
然而近日，Percona 创始人 Peter Zaitsev 在官方博客上公开表达了对 MySQL，及其知识产权属主 Oracle 的失望，以及对版本越高性能越差的不满，这确实是一个值得关注的信号。

- [Oracle最终还是干死了MySQL](https://mp.weixin.qq.com/s/1zlDPie_bVvP7eO6_uTkSw)
- [Percona：Sakila啊，你将何去何从？](https://mp.weixin.qq.com/s/nKD00j84R-EcOU1VPL1ibA)

> 作者：Percona Blog，Marco Tusa，MySQL 生态的重要贡献者，开发了知名的PT系列工具，MySQL备份工具，监控工具与发行版。
>
> 译者：冯若航，网名 Vonng，Pigsty 作者，PostgreSQL 专家与布道师。下云倡导者，数据库下云实践者。


我之前写了篇文章 [Oracle最终还是杀死了MySQL](/zh/blog/oracle-kill-mysql/) ，引发了不少回应 —— 包括 The Register 上的几篇精彩文章（[1](https://www.theregister.com/2024/06/11/early_mysql_engineer_questions_whether/), [2](https://www.theregister.com/2024/06/14/oracles_love_and_hate_relationship/)）。这确实引出了几个值得讨论的问题：

> **AWS和其他云厂商参与竞争，却不回馈任何贡献，那你还指望 Oracle 做啥呢？**

首先 —— 我认为 AWS 和其他云厂商如果愿意对 MySQL 作出更多贡献，那当然是一件好事。
不过我们也应该注意到， Oracle 与这些公司都是竞争关系，并且在 MySQL 这并没有一个公平的竞争环境（AWS 为什么会来参与这种不公平的竞争是另一个话题）。

对你的竞争对手贡献知识产权可能并不是一个很好的商业决策，特别是 Oracle 还要求贡献者签署的 CLA（贡献者授权协议）。
只要 Oracle 拥有这些知识产权，合理的预期就是由 Oracle 自己来承担大部分维护、改进和推广 MySQL 的责任。

没错 …… ，但如果 Oracle 不愿意，或不再有能力管理好 MySQL，而仅仅只关注它自己的云版本，就像 AWS 仅仅专注于其 RDS 和 Aurora 服务，我们又能怎么办呢？

**有一个解决方案 —— Oracle 应该将 MySQL Community 转让给 Linux Foundation、Apache Foundation 或其他独立实体，允许公平竞争，并专注于他们的 Cloud（Heatwave）和企业级产品。** 有趣的是，Oracle 已经有了这样的先例：[将 OpenOffice 转交给 Apache 软件基金会](https://www.zdnet.com/article/oracle-gives-openoffice-to-apache/)。

另一个很好的例子是 [LinkerD](https://linkerd.io/) —— 它由 Buoyant 公司 [引入 CNCF](https://linkerd.io/2017/01/24/linkerd-joins-the-cloud-native-computing-foundation/) —— 而 Buoyant 也在持续构建它的扩展版本 — [Buoyant Enterprise for LinkerD](https://buoyant.io/linkerd-enterprise)。

在这种情况下，维护和发展开源的 MySQL 成为了一个生态问题：我很确信，如果不是向竞争对手拥有的知识产权贡献，AWS 与其他云厂商肯定愿意参与更多。实际上我们确实可以在 PostgreSQL、Linux 或 Kubernetes 项目中看到云厂商在大力参与。

> **有了 PostgreSQL；谁还需要 MySQL 呢？**

PostgreSQL 确实是一个出色的数据库，有着活跃的社区，并且近年来发展迅速。然而仍有很多人更偏好于 MySQL ，也有很多现有应用程序仍然在使用 MySQL —— 因此我们希望 MySQL 能继续健康发展，长命百岁。

当然还有一点：如果 MySQL 死掉了，开源关系型数据库实际上就被 PostgreSQL 一家垄断了，在我看来，垄断并不是一件好事，因为它会导致发展停滞与创新减缓。PostgreSQL 要想进入全盛状态，有一个 MySQL 作为竞争对手并不是坏事。

> **难道 MariaDB 不是一个新的、更好的、由社区管理的 MySQL 吗？**

我认为 MariaDB 的存在很好地向 Oracle 施加了压力，迫使其不得不投资 MySQL 。虽然我们没法确定地说如果没有 MariaDB 会怎样，但如果没有它，很可能 MySQL 很久以前就被 Oracle 忽视了。

话虽如此，虽然 MariaDB 在组织架构上与 Oracle 大有不同，但它也显然不是像 PostgreSQL 那种 “由社区拥有和管理” 的数据库，也没有 PostgreSQL 那样广泛的独立公司贡献者。我认为 MariaDB 确实可以采取一些措施，争取 MySQL 领域的领导地位，但这值得另单一篇文章展开。

**总结一下**

PostgreSQL 和 MariaDB 是出色的数据库，如果没有它们，开源社区将被绑死在 Oracle 的贼船上，陷入糟糕的境地，但它们今天都还不能完全替代 MySQL。
MySQL 社区的最好结果应该是 Oracle 与达成协议，共同努力，尽可能一起建设好 MySQL。如果不行，MySQL 社区需要一个计划B。



------

## 参考阅读

[Can Oracle Save MySQL?](https://www.percona.com/blog/can-oracle-save-mysql/)

[MySQL性能越来越差，Sakila将何去何从？](/db/sakila-where-are-you-going/)

[MySQL 的正确性为何如此垃圾？](/db/bad-mysql/)

[Is Oracle Finally Killing MySQL?](https://www.percona.com/blog/is-oracle-finally-killing-mysql/)

[Can Oracle Save MySQL?](https://www.percona.com/blog/can-oracle-save-mysql/)

[Sakila, Where Are You Going?](https://www.percona.com/blog/sakila-where-are-you-going/)

[Postgres vs MySQL: the impact of CPU overhead on performance](https://smalldatum.blogspot.com/2023/10/postgres-vs-mysql-impact-of-cpu.html)

[Perf regressions in MySQL from 5.6.21 to 8.0.36 using sysbench and a small server](https://smalldatum.blogspot.com/2024/02/perf-regressions-in-mysql-from-5621-to.html)




--------

## 英文原文

I got quite a response to my article on whether [Oracle is Killing MySQL,](https://www.percona.com/blog/is-oracle-finally-killing-mysql/) including a couple of great write-ups on The Register ([1](https://www.theregister.com/2024/06/11/early_mysql_engineer_questions_whether/), [2](https://www.theregister.com/2024/06/14/oracles_love_and_hate_relationship/)) on the topic. There are a few questions in this discussion that I think are worth addressing. 

> **AWS and other cloud vendors compete, without giving anything back, what else would you expect Oracle to do ?**

First, yes. I think it would be great if AWS and other cloud providers would contribute more to MySQL. We should note, though, that Oracle is a competitor for many of those companies, and there is no “level playing field” when it comes to MySQL (the fact AWS is willing on this unlevel field is another point). Contributing IP to your competitor, especially considering CLA Oracle requires might not be a great business decision. Until Oracle owns that IP, it is reasonable to expect, for Oracle to have most of the burden to maintain, improve, and promote MySQL, too.

Yes… but what if Oracle is unwilling or unable to be a great MySQL steward anymore and would rather only focus on its cloud version, similar to AWS being solely focused on its RDS and Aurora offerings?  ***There is a solution for that – Oracle should transfer MySQL Community to Linux Foundation, Apache Foundation, or another independent entity, open up the level playing field, and focus on their Cloud (Heatwave) and Enterprise offering.\*** Interestingly enough, there is already a precedent for that with Oracle [transferring OpenOffice to Apache Software Foundation](https://www.zdnet.com/article/oracle-gives-openoffice-to-apache/).

Another great example would be[ LinkerD](https://linkerd.io/) — which [was brought to CNCF](https://linkerd.io/2017/01/24/linkerd-joins-the-cloud-native-computing-foundation/) by Buyant — which continues to build its extended edition[ – Buoyant Enterprise for LinkerD](https://buoyant.io/linkerd-enterprise).

In this case, maintaining and growing open source MySQL will become an ecosystem problem and I’m quite sure AWS and other cloud vendors will participate more when they are not contributing to IP owned by their competitors. We can actually see it with PostgreSQL, Linux, or Kubernetes projects which have great participation from cloud vendors.

> **There is PostgreSQL; who needs MySQL anyway?** 

Indeed, PostgreSQL is a fantastic database with a great community and has been growing a lot recently. Yet there are still a lot of existing applications on MySQL and many folks who prefer MySQL, and so we need MySQL healthy for many years to come. But there is more; if MySQL were to die, we would essentially have a monopoly with popular open source relational databases, and, in my opinion, monopoly is not a good thing as it leads to stagnation and slows innovation. To have PostgreSQL to be as great as it can be it is very helpful to have healthy competition from MySQL!

> **Isn’t MariaDB a new, better, community-governed MySQL ?**

I think MariaDB’s existence has been great at putting pressure on Oracle to invest in MySQL. We can’t know for certain “what would have been,” but chances are we would have seen more MySQL neglect earlier if not for MariaDB. Having said that, while organizationally, MariaDB is not Oracle, it is not as cleanly “community owned and governed” as PostgreSQL and does not have as broad a number of independent corporate contributors as PostgreSQL.I think there are steps MariaDB can do to really take a leadership position in MySQL space… but it deserves another article.

**To sum things up** 

PostgreSQL and MariaDB are fantastic databases, and if not for them, the open source community would be in a very bad bind with Oracle’s current MySQL stewardship. Neither is quite a MySQL replacement today, and the best outcome for the MySQL community would be for Oracle to come to terms and work with the community to build MySQL into the best database it can be. If not, the MySQL community needs to come up with a plan B.



