---
title: PostgreSQL会修改开源许可证吗？
date: 2024-03-20
showAuthor: false
author: |
  [JONATHAN KATZ](https://jkatz05.com/post/postgres/) | 译：[冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [英文原文](https://jkatz05.com/post/postgres/postgres-license-2024/) | [微信公众号原文]()
summary: |
  PostgreSQL 不会改变其许可证 
tags: [PostgreSQL,PG生态,开源]
---

> 作者：[Jonathan Katz](https://jkatz05.com/post/postgres/)，PostgreSQL 核心组成员（1 of 7），AWS RDS 首席产品经理
>
> 译者：[冯若航](https://vonng.com)，PostgreSQL 专家，Free RDS PG Alternative —— Pigsty 作者



-----------

## PostgreSQL会修改开源许可证吗

> 声明：我是[PostgreSQL 核心组](https://www.postgresql.org/developer/core/) 的成员，但本文内容是我的个人观点，并非 PostgreSQL 官方声明 …… **除非我提供了指向官方声明的链接**；

今天得知 [Redis 项目将不再使用开源许可证发布](https://redis.com/blog/redis-adopts-dual-source-available-licensing/)，我感到非常遗憾。原因有二：一是作为长期的 Redis 用户和较早的采用者，二是作为一个开源贡献者。对于开源商业化这件事的挑战，我不得不说确实感同身受 —— 特别是我曾站在针锋相对的不同阵营之中（译注：作者也是 AWS RDS 首席产品经理）。我也清楚这些变化对下游的冲击，它们可能对用户采纳、应用技术的方式产生颠覆性的影响。

每当开源许可证领域出现重大变动时，尤其是在数据库及相关系统中（例如 MySQL => Sun => Oracle 就是第一个映入我脑海的），我总会听到这样的问题：“PostgreSQL会修改其许可证吗？”

PostgreSQL 的网站上其实 [有答案](https://www.postgresql.org/about/licence/)：

> PostgreSQL会使用不同的许可证发布吗？PostgreSQL 全球开发组（PGDG）依然致力于永远将 PostgreSQL  作为自由和开源软件提供。我们没有更改 PostgreSQL 许可证，或使用不同许可证发布 PostgreSQL 的计划。

> 声明：上面这段确实是我参与撰写的

[PostgreSQL许可证](https://www.postgresql.org/about/licence/)（又名 “**协议**” — [Dave Page](https://pgsnake.blogspot.com/) 和我在这个词上来回辩论挺有意思的）是一个[开源倡议组织（OSI）认可的许可证](https://opensource.org/license/postgresql)，采用非常宽松的许可模型。至于它与哪个许可证最为相似，我建议阅读 [Tom Lane在2009年写的这封电子邮件](https://www.postgresql.org/message-id/1776.1256525282@sss.pgh.pa.us) （大意是：更接近 MIT 协议，叫 BSD 也行）。

尽管这么说，但 PostgreSQL不会改变许可证，还是有一些原因在里面的：

- 许可证的名字就叫 “[PostgreSQL许可证](https://www.postgresql.org/about/licence/)” —— 你都用项目来命名许可证了，还改什么协议？
- PostgreSQL项目发起时，以开源社区协作为主旨，**意在防止任何单一实体控制本项目**。这一点作为项目的精神主旨已经延续了近三十年时间了，并且在项目 [项目政策 ](https://www.postgresql.org/about/policies/)中有着明确体现。
- [Dave Page 在这封邮件中明确表示过](https://www.postgresql.org/message-id/937d27e10910260840s1d28aab2o799f2c58d14dfb1e@mail.gmail.com) 😊

那么真正的问题就变成了，**如果 PostgreSQL 要改变许可证，会出于什么理由呢**？通常变更许可证的原因是出于商业决策 —— 但看起来围绕 PostgreSQL 的商业业务与 PostgreSQL 的功能集合一样强壮。冯若航（Vonng）最近[写了一篇博客文章](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4)，突出展现了围绕 PostgreSQL 打造的软件与商业生态，这还仅仅是一部分。

我说 “仅仅是一部分” 的意思是，在历史上和现在还有更多的项目和商业，是围绕着 PostgreSQL 代码库的某些部分构建的。这些项目中许多都使用了不同的许可证发布，或者干脆就是闭源的。但它们也直接或间接地推动了PostgreSQL 的采用，并使 PostgreSQL 协议变得无处不在。

但 PostgreSQL 不会改变其许可证的最大原因是，这将对所有 PostgreSQL 用户产生不利影响。对一项技术来说，建立信任需要很长时间，尤其是当该技术经常用于应用程序最关键的部分：数据存储与检索。[PostgreSQL赢得了良好的声誉 —— 凭借其久经考验的架构、可靠性、数据完整性、强大的功能集、可扩展性，以及背后充满奉献精神的开源社区，始终如一地提供优质、创新的解决方案](https://www.postgresql.org/about/)。修改 PostgreSQL 的许可证将破坏该项目过去近三十年来建立起的所有良好声誉。

尽管 PostgreSQL 项目确实有不完美之处（我当然也对这些不完美的地方有所贡献），但 PostgreSQL 许可证对PostgreSQL 社区和整个开源界来说，确实是一份真正的礼物，我们将继续珍惜并帮助保持 PostgreSQL 真正的自由和开源。毕竟，[官网上也是这么说的](https://www.postgresql.org/about/licence/) ;)


------

## 译者评论

能被 PostgreSQL 全球社区核心组成员提名推荐，我感到非常荣幸。上文中 Jonathan 提到我的文章是《[PostgreSQL正在吞噬数据库世界](https://mp.weixin.qq.com/s/8_uhRH93oAoHZqoC90DA6g)》，英文版为《[PostgreSQL is Eating The Database World](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4)》。发布于 Medium：https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4 ，并在 HackerNews ，X，LinkedIn 上引起相当热烈的讨论。

Redis 变更其许可证协议，是开源软件领域又一里程碑式的事件 —— 至此，所有头部的 NoSQL 数据库 ，包括 MongoDB， ElasticSearch，加上 Redis ，都已经切换到了 SSPL —— 一种不被 OSI 承认的许可证协议。

Redis 切换为更为严格的 SSPL 协议的核心原因，用 Redis Labs CEO 的话讲就是：“**多年来，我们就像个傻子一样，他们拿着我们开发的东西大赚了一笔**”。“他们”是谁？ —— **公有云**。切换 SSPL 的目的是，试图通过法律工具阻止这些云厂商白嫖吸血开源，成为体面的社区参与者，将软件的管理、监控、托管等方面的代码开源回馈社区。

不幸的是，你可以强迫一家公司提供他们的 GPL/SSPL 衍生软件项目的源码，但你不能强迫他们成为开源社区的好公民。公有云对于这样的协议往往也嗤之以鼻，大多数云厂商只是简单拒绝使用AGPL许可的软件：要么使用一个采用更宽松许可的替代实现版本，要么自己重新实现必要的功能，或者直接购买一个没有版权限制的商业许可。

当 Redis 宣布更改协议后，马上就有 AWS 员工跳出来 Fork Redis —— “Redis 不开源了，我们的分叉才是真开源！” 然后 AWS CTO 出来叫好，并假惺惺的说：这是我们员工的个人行为 —— 堪称是现实版杀人诛心。而同样的事情，已经发生过几次了，比如分叉 ElasticSearh 的 OpenSearch，分叉 MongoDB 的 DocumentDB。

因为引入了额外的限制与所谓的“歧视”条款，OSI 并没有将 SSPL 认定为开源协议。因此使用 SSPL 的举措被解读为 —— “Redis 不再开源”，而云厂商的各种 Fork 是“开源”的。从法律工具的角度来说，这是成立的。但从朴素道德情感出发，这样的说法对于 Redis 来说是极其不公正的抹黑与羞辱。

正如罗翔老师所说：法律工具的判断永远不能超越社区成员朴素的道德情感。如果协和与华西不是三甲，那么丢脸的不是这些医院，而是三甲这个标准。如果年度游戏不是巫师3，荒野之息，博德之门，那么丢脸的不是这些厂商，而是评级机构。如果 Redis 不再算“开源”，真正应该感到汗颜的应该是OSI 与开源这个理念。

越来越多的知名开源软件，都开始切换到敌视针对云厂商白嫖的许可证协议上来。不仅仅是 Redis 与 MongoDB，ElasticSearch 在 2021 年也从 Apache 2.0 修改为 SSL 与 ElasticSearch，知名的开源软件 MinIO 与 Grafana 分别在 2020，2021年从 Apache v2 协议切换到了 AGPLv3 协议。

一些老牌的开源项目例如 PostgreSQL ，正如 Jonathan 所说，历史沉淀（三十年的声誉！）让它们已经在事实上无法变更开源协议了。但我们可以看到，许多新强力的 PostgreSQL 扩展插件开始使用 AGPLv3 作为默认的开源协议，而不是以前默认使用的 BSD-like / PostgreSQL 友善协议。例如分布式扩展 Citus，列存扩展 Hydra，ES全文检索替代扩展 BM25，OLAP 加速组件 PG Analytics …… 等等等等。包括我们自己的 PostgreSQL 发行版 Pigsty，也在 2.0 的时候由 Apache 协议切换到了 AGPLv3 协议，背后的动机都是相似的 —— 针对软件自由的最大敌人 —— 云厂商进行反击。

在抵御云厂商白嫖的实践中，修改协议是最常见的做法：但AGPLv3 过于严格容易敌我皆伤，SSPL 因为明确表达这种敌我歧视，不被算作开源。业界需要一种新的歧视性软件许可证协议，来达到名正言顺区分敌我的效果。使用双协议进行明确的边界区分，也开始成为一种主流的开源商业化实践。

真正重要的事情一直都是软件自由，而“开源”只是实现软件自由的一种手段。而如果“开源”的理念无法适应新阶段矛盾斗争的需求，甚至会妨碍软件自由，它一样会过气，并不再重要，并最终被新的理念与实践所替代 —— 比如“本地优先”。




------

## 英文原文

### WILL POSTGRESQL EVER CHANGE ITS LICENSE?

(Disclosure: I’m on the [PostgreSQL Core Team](https://www.postgresql.org/developer/core/), but what’s written in this post are my personal views and not official project statements…unless I link to something that’s an official project statement ;)

I was very sad to learn today that the [Redis project will no longer be released under an open source license](https://redis.com/blog/redis-adopts-dual-source-available-licensing/). Sad for two reasons: as a longtime Redis user and pretty early adopter, and as an open source contributor. I’ll preface that I’m empathetic to the challenges of building businesses around open source, having been on multiple sides of this equation. I’m also cognizant of the downstream effects of these changes that can completely flip how a user adopts and uses a piece of technology.

Whenever there’s a shakeup in open source licensing, particularly amongst databases and related systems (MySQL => Sun => Oracle being the one that first springs to mind), I’ll hear the question “Will PostgreSQL ever change its license?”

The PostgreSQL website [has an answer](https://www.postgresql.org/about/licence/):

> Will PostgreSQL ever be released under a different license? The PostgreSQL Global Development Group remains committed to making PostgreSQL available as free and open > source software in perpetuity. There are no plans to change the PostgreSQL License or release PostgreSQL under a different license.

(Disclosure: I did help write the above paragraph).

[The PostgreSQL Licence](https://www.postgresql.org/about/licence/) (aka “License” – [Dave Page](https://pgsnake.blogspot.com/) and I have fun going back and forth on this) is an [Open Source Initiative (OSI) recognized license](https://opensource.org/license/postgresql), and has a very permissive model. In terms of which license it’s most similar to, I defer to this email that [Tom Lane wrote in 2009](https://www.postgresql.org/message-id/1776.1256525282@sss.pgh.pa.us).

That said, there are a few reasons why PostgreSQL won’t change it’s license:

- It’s “[The PostgreSQL Licence](https://www.postgresql.org/about/licence/)” – why change license when you have it named after the project?
- The PostgreSQL Project began as a collaborative open source effort and is set up to prevent a single entity to take control. This carries through in the project’s ethos almost 30 years later, and is even codified throughout the [project policies](https://www.postgresql.org/about/policies/).
- [Dave Page explicitly said so in this email](https://www.postgresql.org/message-id/937d27e10910260840s1d28aab2o799f2c58d14dfb1e@mail.gmail.com) :)

The question then becomes - is there a reason that PostgreSQL would change its license? Typically these changes happen as part of a business decision - but it seems that business around PostgreSQL is as robust as its feature set. Ruohang Feng (Vonng) recently [wrote a blog post](https://medium.com/@fengruohang/postgres-is-eating-the-database-world-157c204dcfc4) that highlighted just a slice of the PostgreSQL software and business ecosystem that’s been built around it, which is only possible through the PostgreSQL Licence. I say “just a slice” because there’s even more, both historically and current, projects and business that are built up around some portion of the PostgreSQL codebase. While many of these projects may be released under different licenses or be closed source, they have helped drive, both directly and indirectly, PostgreSQL adoption, and have helped make the PostgreSQL protocol ubiquitous.

But the biggest reason why PostgreSQL would not change its license is the disservice it would do to all PostgreSQL users. It takes a long time to build trust in a technology that is often used for the most critical part of an application: storage and retrieval of data. [PostgreSQL has earned a strong reputation for its proven architecture, reliability, data integrity, robust feature set, extensibility, and the dedication of the open source community behind the software to consistently deliver performant and innovative solutions](https://www.postgresql.org/about/). Changing the license of PostgreSQL would shatter all of the goodwill the project has built up through the past (nearly) 30 years.

While there are definitely parts of the PostgreSQL project that are imperfect (and I certainly contribute to those imperfections), the PostgreSQL Licence is a true gift to the PostgreSQL community and open source in general that we’ll continue to cherish and help keep PostgreSQL truly free and open source. After all, it says [so on the website](https://www.postgresql.org/about/licence/) ;)