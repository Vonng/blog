---
title: "展望 PostgreSQL 的2024"
date: 2024-01-05
authors: [jonathan-katz]
origin: "https://jkatz05.com/post/postgres/postgresql-2024/"
summary: >
  本文是 PostgreSQL 核心组成员 Jonathan Katz 对 2024 年 PostgreSQL 项目的未来展望，并回顾过去几年 PostgreSQL 所取得的进展。
tags: [PostgreSQL, PG生态, 翻译]
---

本文是 PostgreSQL 核心组成员 Jonathan Katz 对 2024 年 PostgreSQL 项目的未来展望，并回顾过去几年 PostgreSQL 所取得的进展。

> **作者**：Jonathan Kats，Amazon RDS 首席产品经理兼技术主管， PostgreSQL 全球开发组核心成员与主要贡献者。博客：https://jkatz05.com/。
>
> **译者**：Vonng，磐吉云数创始人 / CEO，[**PostgreSQL**](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485685&idx=1&sn=688f6d6d0f4128d7f77d710f04ff9024&chksm=fe4b3d2ec93cb438665b7e0d554511674091b2e486a70b8a3eb7e2c7a53681fb9834a08cb3c3&scene=21#wechat_redirect) 专家与布道师，开源 RDS PG —— [**Pigsty**](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485518&idx=1&sn=3d5f3c753facc829b2300a15df50d237&chksm=fe4b3d95c93cb4833b8e80433cff46a893f939154be60a2a24ee96598f96b32271301abfda1f&scene=21#wechat_redirect) 作者。博客：https://vonng.com
>
> 点击“查看原文”查看英文原文：https://jkatz05.com/post/postgres/postgresql-2024/



在我经常听到的问题中，有一个尤为深刻：***“PostgreSQL 将走向何方？”***  —— 这也是我经常问自己的一个问题。这个问题不仅仅局限在数据库内核引擎的技术层面，而关乎整个社区的方方面面 —— 包括相关的开源项目、活动和社区发展。PostgreSQL 已经广受欢迎，并且已经是第四次被 [DB Engine评为“**年度数据库**”](https://db-engines.com/en/blog_post/106)。尽管已取得显著成功，我们依然需要不时地后退一步，从更宏观的角度思考 PostgreSQL 的未来。虽然这种思考不会立即带来显著的变化，但它对于社区正在进行的工作提供了重要的背景板。

新年是思考 **“PostgreSQL的未来”** 这一问题的绝佳时机，我对2024年的PostgreSQL发展方向也有一些思考，这里是我的一些想法：这并不是一个路线图，而是我个人对 PostgreSQL 发展方向的一些想法。

-------


## PostgreSQL功能开发

在[PGCon 2023 开发者会议](https://wiki.postgresql.org/wiki/PgCon_2023_Developer_Meeting)上，我提出了一个题为“**PostgreSQL 用户面临的重大挑战是什么？**”的话题。这个话题旨在探讨用户的常见需求和数据库工作负载的发展趋势，以此来判断我们是否正在朝着正确的方向发展 PostgreSQL。通过多次交谈和观察，我提出了三个主要的特性类目：

- 可用性
- 性能
- 面向开发者的特性

这些特性组将成为 2024 年，甚至更长时间段里的工作重点。接下来，我将对每个特性类目进行更深入的探讨。


### 可用性

对于PostgreSQL现有用户和潜在用户来说，提高可用性是最迫切的需求。这个需求不仅仅是排在第一位，而且毫不夸张地讲，也同时能排在第二位和第三位。虽然重启 PostgreSQL 通常可以迅速完成，但在某些极端情况下，这个过程可能耗时过长。此外，长时间的写入阻塞，例如某些锁操作，也可被视作一种“停机时间”。

大部分 PostgreSQL 用户对现有的可用性水平已感满意，但有些工作负载对可用性的要求极为严格。为了更好地满足这些要求，我们需要进行额外的开发工作。这篇文章或这一小节就聚焦于这一点：通过改进使 PostgreSQL 适用于更多有严苛可用性需求的环境。



#### 逻辑复制是如何助益于双主，蓝绿部署，零停机升级，以及其他工作流的

对于现有的 PostgreSQL 用户，以及那些计划迁移至 PostgreSQL 的用户来说，提升可用性是最重要的需求。这通常指的是[高可用](https://en.wikipedia.org/wiki/High_availability)——即在计划内的更新或计划外的中断期间，数据库能够持续进行读写操作的能力。PostgreSQL 已经提供了许多支持高可用的特性，如流复制。然而为了实现最高水平的可用性，通常还需要借助额外的服务或诸如 [Patroni](https://github.com/zalando/patroni) 这样的工具。

我聊过许多用户，在绝大多数情况下，他们对 PostgreSQL 提供的可用性是满意的。但我也发现了一个新趋势：现在有一些负载对可用性的要求越来越高，15-30 秒的离线窗口已不够了。这包括计划内的中断（如小版本升级、大版本升级），以及计划外的中断。一些用户表示，他们的系统最多只能承受1秒的不可用时间。起初我对这种要求持怀疑态度，但了解到这些工作负载的具体用途后，我认为1秒确实是一个合理的需求。

在持续提高 PostgreSQL 可用性方面，[逻辑复制](https://www.postgresql.org/docs/current/logical-replication.html) 是一个关键特性。逻辑复制能够实时将 PostgreSQL 数据库中的变更流式传输到任何支持 PostgreSQL 逻辑复制协议的系统中。PostgreSQL 中的逻辑复制[已经存在了一段时间](https://jkatz05.com/post/postgres/postgres-10-tribute/)，而[最近的版本](https://www.postgresql.org/about/news/postgresql-16-released-2715/)在可用性方面带来了显著的改进，包括功能和性能上的新特性。

逻辑复制在 PostgreSQL 的大版本升级过程中扮演着关键角色，与传统的物理（或二进制）复制相比，它的一大优势在于能够实现跨版本的数据流转。举例来说，通过逻辑复制，我们可以轻松地将 PostgreSQL 15 的数据变更实时传输至 PostgreSQL 16，从而大幅缩减升级过程中的停机时间。这种方法已在 [Instacart 的零停机大版本升级](https://www.instacart.com/company/how-its-made/zero-downtime-postgresql-cutovers/)中得到成功应用。然而，PostgreSQL 在支持此类用例和其他高可用性场景方面仍有待提升。未来的发展预计将进一步优化支持[蓝绿部署](https://en.wikipedia.org/wiki/Blue-green_deployment)的功能，以实现更加无缝的数据迁移和应用升级。

除了在大版本升级中的用例，逻辑复制本身也是构建高可用系统的重要手段。"**多主复制**"就是其中的一个典型应用，它允许多个数据库实例同时接受写入操作，并在它们之间同步数据变更。这种模式尤其适用于对停机时间敏感的系统（例如：不接受1秒以上的不可用时间），其设计目标是在任何写入数据库出现问题时，应用能迅速切换到另一可用的写入数据库，而不必等待它被提升为新主库。构建与管理这样的双活系统是极度复杂的：它会影响到应用设计，并需要用户提供对写入冲突进行管理的策略，而且为了确保数据完整性（比如：冲突风暴），需要有仔细设计的容错监控系统 —— （比如，一个实例如果几个小时都无法复制它的变更会发生什么？）

大版本升级和双活复制案例为我们指明了改善 PostgreSQL 逻辑复制的方向。[Amit Kapila](https://amitkapila16.blogspot.com/) 是众多逻辑复制功能开发的领导者。今年，他和我共同在一场会议上发表了题为“[PostgreSQL 中的多主复制之旅](https://www.postgresql.eu/events/pgconfeu2023/sessions/session/4783/slides/434/pgconfeu2023_active_active.pdf)”的演讲（并提供了[视频版本](https://www.youtube.com/watch?v=jPp4XIY4XRw)），深入探讨了为何针对这些用例的解决方案至关重要、PostgreSQL 在逻辑复制方面取得的成就，以及为更好支持这些场景所需做的工作。好消息是从 PostgreSQL 16 版本起，我们已经有了大部分基础模块来支持双活复制、蓝绿部署和零停机大版本升级。虽然这些功能可能没有全部集成在内核中，但某些扩展（比如我参与开发的[`pgactive`](https://aws.amazon.com/blogs/database/using-pgactive-active-active-replication-extension-for-postgresql-on-amazon-rds-for-postgresql/)）已提供了这些能力。

在 2024 年，有多项努力旨在帮助缩小这些功能差距。对于 PostgreSQL 17 来说（惯例免责声明：这些特性可能不会发布），有一个重点是确保逻辑复制能够与关键工作流（如[`pg_upgrade`](https://www.postgresql.org/docs/current/pgupgrade.html)和[高可用系统](https://commitfest.postgresql.org/46/4423/)）协同工作，支持更多类型的数据变更（如[序列/Sequence](https://commitfest.postgresql.org/46/3823/)）的复制，扩展对更多命令（如 [DDL](https://commitfest.postgresql.org/46/3595/)）的支持，提高性能，以及增加简化逻辑复制管理的特性（如节点同步/再同步）。

这些努力能让 PostgreSQL 适用于更多种类的负载，特别是那些有着极致严苛可用性要求的场景，并简化用户在生产环境中滚动发布新变更的方式。尽管改进逻辑复制功能的道路仍然漫长，但 2024 年无疑将为 PostgreSQL 带来更多强大的功能特性，帮助用户在关键环境中更加高效地运行 PostgreSQL。



#### 减少锁定

另一个有关可用性的领域是**模式维护操作**（即[DDL](https://en.wikipedia.org/wiki/Data_definition_language)语句）。例如，[`ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html)的大部分形式会对表施加 [`ACCESS EXCLUSIVE`](https://www.postgresql.org/docs/current/explicit-locking.html#LOCKING-TABLES) 锁，从而阻止对该表的所有并发访问。对于许多用户来说这等同于不可用，即使这只是数据的一个子集。PostgreSQL 缺乏对非阻塞/在线模式维护操作的完整支持，随着其他关系数据库也开始支持这些功能，这方面的不足开始逐渐凸显。

目前虽有多种工具和扩展支持非阻塞模式更新，但如果 PostgreSQL 能原生支持更广泛的非阻塞模式变更，那肯定更方便，而且性能也会更好。从设计上来看，我们已有了开发此功能的基础，但还需要一些时间来实现。尽管我不确定是否有正在进行中的具体实现，但我相信在2024年我们应该在这方面取得更多进展：让用户能够在不阻塞写入的情况下执行大部分（或全部）DDL 命令



#### 性能

性能是一个不断持续演进的特性 —— 我们总是会追求更快的速度。好消息是，PostgreSQL 在垂直扩展能力上享有盛誉 —— 当你为单个实例提供更多硬件资源时，PostgreSQL 也能扩展自如。虽然在某些场景下，水平扩展读写操作是有意义的。但我们还是要确保 PostgreSQL 能够随着计算和内存资源的增加而持续扩展。

举个更具体的例子：考虑到 AWS EC2 实例中有着高达 [448 vCPU / 24TB 内存 ](https://aws.amazon.com/ec2/instance-types/high-memory/)的选配项 ——  PostgreSQL 能否在单个实例上充分利用这些资源呢？我们可以根据 PostgreSQL 用户现在与未来可能使用的硬件配置，设定一个性能提升的目标，并持续提升 PostgreSQL 的整体表现。

在 2024 年，已经有多项工作致力于继续垂直扩展 PostgreSQL。其中最大的努力之一，也是一个持续多年的项目，就是在 PostgreSQL 中支持 DirectIO（DIO）与 Asynchronous IO（AIO）。至于细节我就留给 Andres Freund 在[PGConf.EU](https://www.pgconf.eu/)上关于[在 PostgreSQL 中添加 AIO 的现状](https://anarazel.de/talks/2023-12-14-pgconf-eu-path-to-aio/path-to-aio.pdf)的PPT来讲了。看起来在 2024 年，我们将离完全支持 AIO 更进一步。

另一项让我感兴趣的工作是[并行恢复](https://wiki.postgresql.org/wiki/Parallel_Recovery)。有着大量写入负载的 PostgreSQL 用户往往会推迟 [Checkpoint](https://www.postgresql.org/docs/current/sql-checkpoint.html) 以减少 I/O 负载。对于忙碌的系统而言，如果 PostgreSQL 在执行 Checkpoint 的相当一段时间后才崩溃，那么当 PostgreSQL 重新启动时，它会进入 "崩溃恢复 "状态：它会重新执行自上次 Checkpoint 以来的所有变更，以便达到一致的状态 —— 在崩溃恢复期间，PostgreSQL 不能读也不能写，这意味着它不可用。这对繁忙的核心系统来说是个问题：虽然 PostgreSQL 可以接受并发写入，但它重放变更时只能使用单个进程。如果一个繁忙系统崩溃于上个检查点后的一小时，那么系统会需要离线追赶几个小时，才能达到一致的状态点重新上线！

克服这一局限性的方法之一是支持"[并行恢复](https://wiki.postgresql.org/wiki/Parallel_Recovery)"，或者说能够并行重放WAL变更。在[PGCon 2023](https://www.pgcon.org/)上，Koichi Suzuki做了一个 [关于PostgreSQL如何支持并行恢复](https://www.pgcon.org/events/pgcon_2023/sessions/session/392/slides/69/ParallelRecovery%20in%20PostgreSQL.pdf) 的详细介绍。这不仅适用于崩溃恢复，也适用于任何 PostgreSQL WAL 重放操作（例如：PITR 时间点恢复）。虽然这是一个极具挑战性的问题，但支持并行恢复有助于 PostgreSQL 继续垂直扩展，因为用户可以进一步针对重度写入负载进行优化，也能缓解 “从故障中恢复上线所需的延时超出承受范围” 的风险。

这并不是一份关于性能特性的详细清单。在 PostgreSQL 服务器性能上还有很多工作要做，包括索引优化、改进锁机制、充分利用硬件加速等。此外，客户端（如驱动程序和连接池）上的工作也能为应用与 PostgreSQL 的交互带来额外的性能提升。展望 2024 年，看看社区正在进行的工作，我相信 PostgreSQL 在各个领域上的性能都会有整体性提升。



### 开发者特性

我认为 "**开发者特性** "（developer features）是一个相当宽泛的类目，核心在于如何让用户围绕 PostgreSQL 来架构 & 构建应用。这里包括：SQL语法、函数、[存储过程语言支持](https://wiki.postgresql.org/wiki/PL_Matrix)，以及帮助用户从其他数据库系统迁移到 PostgreSQL 的功能。一个具体的创新例子是在 PostgreSQL 14 中引入的 [`multirange`](https://www.postgresql.org/docs/current/rangetypes.html) 数据类型，它允许用户将一些不连续的 **范围（Range）** 聚合在一起，这个特性非常实用，我个人在实现一个调度功能时，用它[将数百行PL/pgSQL代码减少到三行](https://www.crunchydata.com/blog/better-range-types-in-postgres-14-turning-100-lines-of-sql-into-3)。开发者特性也关乎 PostgreSQL 如何支持新出现的工作负载：例如[JSON 或向量](https://jkatz05.com/post/postgres/vectors-json-postgresql/)。

值得一提的是，许多开发者特性创新主要出现在**扩展（Extension）**上，而这正是 PostgreSQL 可扩展模型的优势所在。然而就数据库服务器本身而言，PostgreSQL 在某些开发者特性上的发布速度相比过去有所落后。例如，尽管PostgreSQL是[第一个将JSON作为可查询数据类型](https://jkatz05.com/post/postgres/vectors-json-postgresql/)的关系数据库，但它在实现 SQL/JSON 标准锁定义的语法与特性上已经开始变得迟缓。PostreSQL 16 发布了 SQL/JSON 中的一些语法特性，2024 年也会有更多的努力用在实现 SQL/JSON 标准上。

话既然说到这儿了，我们应当着力于 PostgreSQL 中那些**无法通过扩展插件实现的开发者特性**，比如 SQL标准特性。我的建议是集中精力关注那些其他数据库已经具备的功能，比如进一步实现 SQL/JSON 标准（例如： `JSON_TABLE`）、系统层面的版本化表（对于审计、闪回，与在特定时间点进行的时态查询非常有用），以及对模块的支持（对于“打包”存储过程来说尤其重要）。

此外，考虑到之前讨论的可用性和性能问题，我们应继续努力简化用户从其他数据库迁移到 PostgreSQL 的过程。在我的日常工作中，我有机会了解了大量与数据库迁移相关的内容：从商业数据库到 PostgreSQL 的迁移策略。当我们增强 PostgreSQL 功能的同时，也有许多机会可以简化迁移流程。包括引入其他数据库中现有的功能（例如全局临时表、全局分区索引、[自治事务](https://www.postgresql.org/message-id/f7470d5a-3cf1-4919-8404-5c4d91341a9f@tantorlabs.com)），并在 PL/pgSQL 中增加更多功能与性能优化（如批量数据处理函数、[模式变量](https://commitfest.postgresql.org/46/1608/)、[缓存函数元数据](https://commitfest.postgresql.org/46/4684/)）。所有这些都将改善 PostgreSQL 开发者的体验，并让其他关系数据库的用户更容易采纳 PostgreSQL。

最后我们需要了解，如何才能持续不断地支持来自 **AI/ML** 数据的新兴负载，特别是向量存储与检索。在2023年的[PGCon](https://www.pgcon.org/)会议上，尽管人们希望在 PostgreSQL 本身中看到原生的向量支持，但大家一致认为，在 [pgvector](https://github.com/pgvector/pgvector)这样的扩展中实现这类功能可以抢占先机，更快地支持这些工作负载（[这一策略似乎已经奏效](https://jkatz05.com/post/postgres/pgvector-overview-0.5.0/)，[在向量数据上性能表现优异](https://aws.amazon.com/blogs/database/accelerate-hnsw-indexing-and-searching-with-pgvector-on-amazon-rds-for-postgresql/)）。[有鉴于向量负载的诸多特征](https://www.postgresql.eu/events/pgconfeu2023/sessions/session/4592/slides/435/pgconfeu2023_vectors.pdf)，我们可以在PostgreSQL中添加一些额外的支持，以便进一步支持它们：其中包括对处理 [活动查询路径中的TOAST数据](https://www.postgresql.org/message-id/ad8a178f-bbe7-d89d-b407-2f0fede93144@postgresql.org)的规划器进行优化，并探索如何更好地支持带有大量过滤条件和 `ORDER BY` 子句的查询。

我确信在 2024 年，PostgreSQL 可以在这些领域取得显著进步。我们看到在 PostgreSQL 的扩展生态中，有大量的新能力正在涌现；但即便如此，我们还是可以继续直接为 PostgreSQL 添加新特性，让它更易于构建应用。



### 安全性如何？

我想快速过一下 PostgreSQL 的安全特性。众所周知在安全敏感型场景中，PostgreSQL 有着极佳的声誉。但总会有许多能改进的地方。在过去几年中，PostgreSQL社区对引入[透明数据加密](https://wiki.postgresql.org/wiki/Transparent_Data_Encryption)（TDE）的原生支持表现出许多兴趣与关注。然而还有许多其他地方可以搞搞创新，比如支持其他的身份验证方式/机制（主要需求是OIDC），或是探索联邦授权模式的可能性，使PostgreSQL能够继承其他系统的权限设置。尽管这些特性在当下都颇有挑战，我建议先在 “Per-Database” 层面上支持 TDE。这里我不想过多展开，因为已经有在 PostgreSQL 中满足这些特性需求的方法了，但我们还是应该不懈努力，争取实现完整的原生支持。

让我们再来看看PostgreSQL能在2024年里发力的其他方向。


-------

## 扩展

PostgreSQL 的设计是**高度可扩展的**。您可以为PostgreSQL添加新功能，而无需分叉项目。包括新的数据类型、索引方法、与其他数据库系统协同工作的方法、更易于管理PostgreSQL特性的实用工具、[额外的编程语言支持](https://wiki.postgresql.org/wiki/PL_Matrix)，甚至[编写自己的扩展插件](https://github.com/aws/pg_tle)。人们已经围绕一些特定的 PostgreSQL 扩展（如[PostGIS](https://postgis.net/)）建立了开源社区和公司；PostgreSQL 单一数据库便能支持不同类型的工作负载（地理空间、时间序列、数据分析、人工智能），正是**扩展**让这件事变得可能。[数千个可用的PostgreSQL扩展](https://gist.github.com/joelonsql/e5aa27f8cc9bd22b8999b7de8aee9d47)成为了PostgreSQL的 "力量倍增器" —— 它一方面让用户能够快速的为数据库新增功能，另一方面也极大推动了 PostgreSQL 的普及与采用。

然而这也产生了一个副作用，即“**扩展蔓延**”现象。用户如何去选择合适的扩展？扩展的支持程度如何？如何判断某个扩展是否有持续积极的维护？如何为扩展做出自己的贡献？甚至“在哪里可以下载扩展”也成为了一个大问题。postgresql.org 提供了一个[不完整的扩展列表](https://www.postgresql.org/download/products/6-postgresql-extensions/)，社区也维护了一些[扩展包](https://www.postgresql.org/download/)，也有其他几个可供选择的 PostgreSQL 扩展仓库（例如 [PGXN](https://pgxn.org/)、[dbdev](https://database.dev/)、[Trunk](https://pgt.dev/)）和 [pgxman](https://pgxman.com/) 可供选择。

PostgreSQL社区的一个优势是去中心化，广泛散布于世界各处。但我们可以做得更好，帮助用户在复杂的数据管理中做出明智的选择。我认为2024年是一个机遇，我们可以投入更多资源来整合与展示 PostgreSQL 扩展，帮助用户理解什么时候可以使用哪些扩展，并了解扩展们的开发成熟度，并同样为扩展开发者提供更好的管理支持与维护资源。

-------


## 社区建设

在谈论2024年社区建设的构想时，我深感自加入 PostgreSQL 贡献者社区以来，我们已取得显著进步。社区在[认可各类贡献者](https://www.postgresql.org/community/contributors/)方面表现突出（尽管仍有提升空间）—— 不仅限于代码贡献，还包括项目的各个方面。展望未来，我想着重强调三个关键领域：导师制、多元化、公平与包容（[DEI](https://en.wikipedia.org/wiki/Diversity,_equity,_and_inclusion)）以及透明度，这些都对项目的全方位发展至关重要。

在[PGCon 2023开发者会议](https://wiki.postgresql.org/wiki/PgCon_2023_Developer_Meeting#What_are_the_big_challenges_for_our_users.3F_What_are_the_big_challenges_for_us_to_solve.3F)上，[Melanie Plageman](https://mastodon.social/@melanieplageman/) 就新贡献者的体验和挑战进行了深入分析。她提到了诸多挑战，如初学者需要花费大量时间来掌握基本知识，包括使用代码库和邮件列表进行交流，以及将补丁提交到可审查状态所需的努力。她还指出，提供建设性指导意见（从审查补丁开始）可能比编写代码本身更具挑战性，同时也讨论了如何有效地提供反馈。

关于提供反馈，我想引用罗伯特-哈斯（Robert Haas）的一篇[优秀博文](https://rhaas.blogspot.com/2023/12/praise-criticism-and-dialogue.html)，其中他特别强调了在批评时同时给予表扬的重要性——这种方法可以产生显著的效果，并提醒我们即使在批评时也应保持支持态度。

回到 Melanie 的观点，我们应该在整个社区更好地实施导师计划。就我个人而言，我认为我在宣传项目方面做得不够好，包括帮助更多人为[网络基础设施](https://www.postgresql.org/developer/related-projects/)和[发布流程](https://www.postgresql.org/about/press/presskit16/) 做出贡献。这并不是说 PostgreSQL 缺乏优秀的导师，而是我们可以在帮助人们开始贡献和找到导师方面做得更好。

2024年将是建立更完善导师制度的起点。我们希望在5月于温哥华举行的 [PGConf.dev 2024](https://2024.pgconf.dev/) 上试验一些新想法。

> 在 [PGConf.dev](https://www.pgconf.dev/) 出现前，从2007年到2023年，[PGCon](https://www.pgcon.org/)一直是PostgreSQL贡献者们集结并讨论即将开始的开发周期和关键项目的重要活动。PGCon 一直由 Dan Langille 负责组织。经过多年的辛勤工作，他决定将组织职责扩展至一个团队，并协助成立了 [PGConf.dev](https://www.pgconf.dev/)。
>

[PGConf.dev](https://www.pgconf.dev/) 是专为那些希望为 PostgreSQL 做贡献的人士举办的会议。会议内容覆盖了 PostgreSQL 的开发工作（包括内核及所有相关的开源项目，如扩展和驱动程序）、社区建设以及开源意见领袖等主题。PGConf.dev 的一大特色是导师制，并计划举办关于如何为 PostgreSQL 贡献的研讨会。如果你正寻找为 PostgreSQL 贡献的机会，我强烈建议你考虑参加本活动或[提交演讲提案](https://2024.pgconf.dev/cfp/)！

接下来是 PostgreSQL 社区如何在多元化、公平与包容性（[DEI](https://en.wikipedia.org/wiki/Diversity,_equity,_and_inclusion)）上进步的话题。我强烈建议观看[凯伦·杰克斯](https://karenjex.blogspot.com/)和[莱蒂西亚·阿夫罗特](https://mydbanotebook.org/)在 2023 年 PGConf.eu 上的演讲： [在肯的 Mojo Dojo Casa House 里尝试成为芭比](https://www.postgresql.eu/events/pgconfeu2023/schedule/session/4913-trying-to-be-barbie-in-kens-mojo-dojo-casa-house/)：因为这是一场关于如何继续让 PostgreSQL 社区变得更加包容的深刻演讲。社区在这方面取得了进步（凯伦和莱蒂西亚指出了有助于此的一些举措），但我们还能做得更好，我们应该积极主动地处理反馈，以确保为 PostgreSQL 做出贡献是一种受欢迎的体验。我们所有人都可以采取行动，例如，在发生（诸如性别歧视的）不当行为时及时指出，并指出行为不当的原因。

最后是透明度问题。在开源领域这可能听起来有些奇怪，毕竟它本身就是开放的。但有不少治理问题并不会在公开场合讨论，了解决策制定的流程会很有帮助。[PostgreSQL 行为守则委员会](https://www.postgresql.org/about/policies/coc_committee/) 提供了一个优秀的例子：一个社区如何就需要敏感处理的问题保持透明度。该委员会每年都会发布一份报告（[这是 2022 年的报告](https://www.postgresql.org/about/policies/coc/reports/2022/)），包括案例的总体描述和整体统计数据。我们可以在许多 PostgreSQL 团队中复制这种做法 —— 这些团队参与的任务可能由于其敏感性需要保密。

-------


## 结论：本来这篇文章应该更短

最初，我以为这篇文章会是一篇简短的帖子，几小时内就能完成。但几天后，我意识到情况并非如此……

老实说，PostgreSQL目前处于一个非常好的状态。它依然备受欢迎，其可靠性、鲁棒性和性能的声誉稳如磐石。然而我们仍可以做得更好，令人感到振奋的是，社区正在积极地在各个方向上努力改善。

虽然上面这些是 PostgreSQL 在 2024 年及以后可以做的事情，但 PostgreSQL 走到今天已经做成了很多很多的事。提出 “PostgreSQL何去何从” 这样的问题，实际上为我们提供了一个机会：回顾过去几年 PostgreSQL 所取得的进展，并展望未来！