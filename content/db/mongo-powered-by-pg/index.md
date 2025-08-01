
---
title: "MongoDB: 现在由PostgreSQL强力驱动？"
linkTitle: "MongoDB：现由PGSQL驱动"
date: 2024-09-03
author: |
  [John De Goes](https://www.linkedin.com/in/jdegoes) [原文地址](https://www.linkedin.com/pulse/mongodb-32-now-powered-postgresql-john-de-goes)
summary: >
  MongoDB 3.2 的分析子系统竟然是一个嵌入式的 PostgreSQL 数据库？由 MongoDB 的合作伙伴发出的血泪控诉与吹哨故事。
tags: [数据库]
---

-------------
 
#### 前言

明天我会发一篇批判 MongoDB 的文章，作为对其近期恶劣营销碰瓷 PostgreSQL 的回应。在那之前，我想先分享一篇在 2015 年时的精彩文章，揭露了 MongoDB 的一些黑历史。

这篇文章最经典的一点在于，它是由 MongoDB 的合作伙伴发出的血泪控诉，MongoDB 对尝试在生态中做分析的伙伴不屑一顾，而是跑去拿了一个 PostgreSQL 作为自己的分析引擎忽悠用户，从而让合作伙伴彻底灰心丧气的故事。

> 本文原文链接：https://www.linkedin.com/pulse/mongodb-32-now-powered-postgresql-john-de-goes （双向被墙状态，你需要开无痕模式挂代理方能访问）

-------------

> 作者：John De Goes —— 挑战 Ziverge 的现状
>
> 发布日期: 2015年12月8日

*本文所述观点仅为个人看法，不代表我[雇主](http://slamdata.com/)的立场或观点。*

在将各种线索综合起来后，我感到极度*震惊*。若我的猜测属实，[MongoDB](http://mongodb.com/)可能正要犯下我认为是数据库公司历史上**最大的错误**。

我是一个[开源分析工具](http://github.com/slamdata/slamdata)的开发者，该工具支持连接至如 MongoDB 这类的 NoSQL 数据库，我每天都在努力推动这些新一代数据库供应商更加走向成功。

事实上，我不久前在 [MongoDB Days Silicon Valley](https://www.mongodb.com/events/mongodb-days-siliconvalley) 上向[一室之内的众人](https://twitter.com/slamdata/status/672166743255592960)进行了[演讲](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics)，阐述了采纳这种新型数据库的诸多益处。

因此当我意识到这一潜在的破坏性秘密时，我立即敲响了警钟。在 2015 年 11 月 12 日，我发送了一封邮件至 MongoDB 的首席产品经理 Asya Kamsky。

尽管措辞谦和，但我表达得十分明确：*MongoDB 正在犯下一个巨大的错误，并应当在还有机会纠正前，重新考虑自身决策。*

然而我没有再接收到 Asya 或其他任何人的回应。我曾成功劝说 MongoDB [改变策略](https://www.mongodb.com/blog/post/revisiting-usdlookup)，避免将[错误的功能](http://slamdata.com/blog/2015/10/21/mongodb-missing-join.html)商业化的经历，这一次未能重演。

以下我如何从新闻稿、YouTube 视频以及散布在 Github 上的源代码中找到线索，以及我最终未能说服 MongoDB 改变方向的经过。

故事起始于 2015 年 6 月 1 日，在纽约市举行的年度 MongoWorld 大会上。



## MongoWorld 2015

[SlamData](http://slamdata.com/) 是我新创办的分析初创公司，它赞助了 2015 年的 MongoWorld，因此我得到了一个难得的 VIP 派对门票，得以参加大会前夜的活动。

活动在 NASDAQ MarketWatch 举行，地点优雅，俯瞰时代广场。我穿着工装裤和初创公司的 T 恤，明显感觉自己穿得不合时宜。高级小吃和酒水随意畅饮，MongoDB 的管理团队也全员出动。

我与 MongoDB 的新任 CEO Dev ("Dave") Ittycheria 握了手，并对他未来的工作表示了几句鼓励。

今年早些时候，富达投资公司[Fidelity Investments](http://fortune.com/2015/11/12/fidelity-marks-down-tech-unicorns/) 将 MongoDB 的估值削减至 2013 年的一半（16 亿美元），将这个初创公司从“独角兽”降级为“驴子”。Dev 的任务就是证明 Fidelity 以及其他质疑者是错误的。

Dev 从 Max Schireson 手中接过了公司（Max 在 2014 年[著名辞职](http://maxschireson.com/2014/08/05/1137/)），在任期间，Dev 组建了一个新的管理团队，对 MongoDB 整个公司产生了深远影响。

虽然我只与 Dev 交谈了几分钟，但他给我的感觉是聪明、友善的，而且非常渴望了解我公司正在做的事情。他递给我一张名片，并表示如果我有需要可以随时联系他。

接下来是 MongoDB 的 CTO 兼联合创始人 Eliot Horowitz。我与他握手，自我介绍，并用 30 秒钟介绍了我的初创公司。

当时，我觉得我的介绍一定很糟糕，因为 Eliot 对我说的每一句话似乎都不感兴趣。事实证明，Eliot 讨厌 SQL，把分析工具视为一种麻烦，所以不难理解我为什么让他感到无聊！

不过，Eliot 确实听到了“分析”这个词，并透露说第二天的大会上，MongoDB 将发布 3.2 版本的一些有趣的新消息。

我请求他透露更多细节，但不行，这些内容严格保密。我只能等到第二天，与全世界一同揭晓答案。

我将这个消息告诉了我的联合创始人 Jeff Carr，我们短暂地感到了一丝恐慌。对于我们这个由四个人组成、完全自筹资金的初创公司来说，最大的担忧是 MongoDB 会宣布推出自己的分析工具，这可能会影响我们融资的机会。

令人宽慰的是，第二天我们发现 MongoDB 的重大宣布并不是分析工具，而是一个名为 *MongoDB BI Connector*的解决方案，这是即将发布的 3.2 版本中的一个重要功能。

--------



## MongoDB 3.2 BI Connector

Eliot 得以宣布 BI 连接器的推出。尽管当天的公告众多，但他对这一连接器似乎不甚感兴趣，因此仅略加提及。

然而，详细信息很快通过一份[官方新闻稿](https://www.mongodb.com/press/opens-modern-application-data-to-new-generation-visual-analysis-and-traditional-bi-tools)发布，其概括如下：

> MongoDB 今日宣布推出一款全新的 BI 和数据可视化连接器，该连接器将 MongoDB 数据库与业界标准的商业智能（BI）及数据可视化工具相连。该连接器设计以兼容市场上所有符合 SQL 标准的数据分析工具，如 Tableau、SAP Business Objects、Qlik 以及 IBM Cognos Business Intelligence 等。目前该连接器处于预览阶段，预计将在 2015 年第四季度全面发布。

根据该新闻稿，BI 连接器将使*全球任何 BI 软件*都能与 MongoDB 数据库进行交互。

这则消息迅速在 Twitter 上[传播开来](https://twitter.com/search?f=tweets&vertical=default&q=mongodb bi connector&src=typd)，并引发了媒体广泛报道。[TechCrunch](http://techcrunch.com/2015/06/02/new-mongodb-connector-creates-direct-connection-to-data-visualization-tools/) 等多家媒体均转载了这一消息，每次报道都为人们提供了新的细节，甚至《财富》杂志还宣称该 BI 连接器实际上已在 MongoWorld [发布](http://fortune.com/2015/06/03/couchbase-mongodb-embrace-sql/)！

考虑到公告的性质，媒体的这种热烈反响似乎是合理的。

### 当世界碰撞

MongoDB 与许多其他 NoSQL 数据库一样，不存储关系型数据。它存储的是复杂的数据结构，这些结构是传统的关系型 BI 软件无法理解的。MongoDB 的战略副总裁 Kelly Stirman 对此进行了精辟的解释：

> *“这些被称为现代应用的软件之所以如此命名，是因为它们采用了不适用于传统数据库行列格式的复杂数据结构。”*

一个能让全球任何 BI 软件在这些复杂数据结构上进行强力分析而且*不损失分析精度*的连接器，无疑是*重大新闻*。

MongoDB 是否真的做到了不可能的事？他们是否开发出了一种既能满足所有 [NoSQL 分析需求](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/)，又能在扁平化、统一的数据上暴露关系语义，使传统 BI 软件能够处理的连接器？

几个月前，我曾与 MongoDB 的产品副总裁 Ron Avnur 交谈。Ron 表示，所有 MongoDB 的客户都在寻求分析功能，但公司尚未决定是自主开发还是寻找合作伙伴。

这意味着 MongoDB 可能在短短几个月内，从*一无所有*迅速转变为拥有*神奇解决方案*。



### 掀开内幕

发布会结束后，我和 Jeff 回到了我们赞助商的展位。Jeff 问了我一个显而易见的问题：**“他们怎么能在短短几个月内，从无到有做出一个能兼容所有 BI 工具的 BI 连接器？！”**

我仔细思考了这个问题。

BI 连接器需要解决的诸多问题中，有一个是如何在 MongoDB 上高效执行类似 SQL 的分析任务。凭借我在分析领域的[深厚](http://github.com/quasar-analytics/)[背景](http://github.com/precog)，我知道要在像 MongoDB 这样现代数据库上高效地执行通用分析是非常具有挑战性的。

这些数据库支持非常丰富的数据结构，并且它们的接口是为所谓的**操作型**用例设计的（而不是**分析型**用例）。能够利用操作型接口在丰富的数据结构上运行任意分析的技术，需要**多年**的开发。不是你能在两个月内搞定的事情。

于是我直觉性地回答了 Jeff：**“他们没有开发新的 BI 连接器。这不可能。这里面肯定有其他问题！”**

具体是什么问题，我并不清楚。但在握手和发名片的间隙，我做了一些调查。

Tableau 展示了他们的软件与 MongoDB BI 连接器配合使用的演示，这引起了我的好奇心。Tableau 在关系型数据库上的可视化分析领域设立了标准，而他们前瞻性的大数据团队一直在认真思考 NoSQL。

借助与 MongoDB 的关系，Tableau 发布了一份与 MongoWorld 发布会同步的[新闻稿](http://www.tableau.com/about/blog/2015/6/tableau-mongodb-visual-analytics-json-speed-thought-39557)，我在他们的网站上找到了这篇新闻稿。

我仔细阅读了这篇新闻稿，想要了解一些新的细节。在深处，我发现了一个微弱的线索：

> MongoDB 将很快宣布连接器的测试版，计划在今年晚些时候 MongoDB 3.2 版本发布时提供正式版。在 MongoDB 的测试期间，Tableau 将通过**我们的 PostgreSQL 驱动程序**在 Windows 和 Mac 上支持 MongoDB 连接器。

这些话给了我第一个线索：**通过我们的 PostgreSQL 驱动程序**。这至少意味着 MongoDB 的 BI 连接器将使用与 PostgreSQL 数据库相同的“语言”（*wire protocol*）。

这让我感到有些可疑：MongoDB 是否真的在重新实现**整个** PostgreSQL 的通信协议，包括对数百个 PostgreSQL 函数的支持？

虽然**可能**，但这看起来**极其不可能**。

我转向 Github，寻找 MongoDB 可能借鉴的开源项目。由于会议的 WiFi 不稳定，我不得不通过手机热点，查找了几十个同时提到 PostgreSQL 和 MongoDB 的仓库。

最终，我找到了我要找的东西：[mongoose_fdw](https://github.com/asya999/mongoose_fdw/commits/master)，一个由 Asya Kamsky（当时我不认识她，但她的简介提到她为 MongoDB 工作）分叉的开源仓库。

这个仓库包含一个所谓的 *Foreign Data Wrapper* (FDW) for PostgreSQL 数据库。FDW 接口允许开发者插入其他数据源，以便 PostgreSQL 可以提取数据并在这些数据上执行 SQL（为使 BI 工具正常工作，NoSQL 数据必须被展平、填充空值，并做其他简化处理）。

**“我想我知道是怎么回事了。”** 我对 Jeff 说。**“看起来，他们可能在原型中将数据展平，然后使用另一个数据库来执行由 BI 软件生成的 SQL 语句。”**

**“什么数据库？”** 他马上问道。

**“PostgreSQL。”**

Jeff 哑口无言。他一句话也没说。但我能完全明白他在想什么，因为我也在想同样的事。

**糟了。这对 MongoDB 来说是个坏消息。真的很糟糕。**


--------



## PostgreSQL：MongoDB 终结者

PostgreSQL 是一个流行的开源关系型数据库。它的受欢迎程度如此之高，以至于目前在[排名](http://db-engines.com/en/ranking)上几乎与 MongoDB 并驾齐驱。

这个数据库对 MongoDB 构成了*激烈竞争*，主要原因是它已经获得了 MongoDB 的一些功能，包括存储、验证、操作和索引 [JSON 文档](https://en.wikipedia.org/wiki/JSON)的能力。第三方软件甚至[赋予了它](https://www.citusdata.com/)横向扩展的能力（或者我该说，*巨量*扩展的能力）。

每隔一个月左右，就会有人写文章推荐使用 PostgreSQL 而不是 MongoDB。这些文章往往会迅速传播，飙升到 HackerNews 网站的热榜。以下是其中一些文章的链接：

- [告别 MongoDB。迎接 PostgreSQL](http://developer.olery.com/blog/goodbye-mongodb-hello-postgresql/)
- [Postgres 性能优于 MongoDB，并引领开发者新现实](http://www.enterprisedb.com/postgres-plus-edb-blog/marc-linster/postgres-outperforms-mongodb-and-ushers-new-developer-reality)
- [MongoDB 已死。PostgreSQL 万岁 :)](https://github.com/errbit/errbit/issues/614)
- [你永远不应该使用 MongoDB 的理由](http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/)
- [SQL vs NoSQL 决斗。Postgres vs Mongo](https://www.airpair.com/postgresql/posts/sql-vs-nosql-ko-postgres-vs-mongo)
- [为什么我放弃了 MongoDB](http://svs.io/post/31724990463/why-i-migrated-away-from-mongodb)
- [为什么你永远永远永远不该使用 MongoDB](http://cryto.net/~joepie91/blog/2015/07/19/why-you-should-never-ever-ever-use-mongodb/)
- [Postgres NoSQL 比 MongoDB 更好吗？](http://www.aptuz.com/blog/is-postgres-nosql-database-better-than-mongodb/)
- [再见 MongoDB。你好 PostgreSQL](https://www.userlike.com/en/blog/2015/10/09/bye-by-mysql-and-mongodb-guten-tag-postgresql)

商业化 PostgreSQL 的最大公司是 [EnterpriseDB](http://enterprisedb.com/)（虽然还有很多其他公司，一些历史更悠久或同样活跃），它在官网上维护了一个[大量的内容库](http://www.enterprisedb.com/nosql-for-enterprise)，主张 PostgreSQL 是比 MongoDB 更好的 NoSQL 数据库。

无论你对这个观点有何看法，有一点是明确的：MongoDB 和 PostgreSQL 在开发者的认知中正进行着一场激烈而血腥的争夺战。





--------

## 从原型到生产

任何有经验的工程师都会告诉你，**原型不能直接用于生产环境**。

即便 MongoDB *确实*在使用 PostgreSQL 作为原型的 BI 连接器，也许某些聪明的 MongoDB 工程师正被关在某个房间里，努力开发一个独立的生产版本。

实际上，从 Tableau 的新闻稿措辞来看，依赖 PostgreSQL 驱动的情况*可能*只是暂时的：

> **在 MongoDB 的测试阶段**，Tableau 将通过我们的 PostgreSQL 驱动程序，在 Windows 和 Mac 上支持 MongoDB 连接器。

我猜测，或许 MongoDB 3.2 版本发布时会带来真正的产品：一个能够暴露 MongoDB 所支持的丰富数据结构（而不是展平、填充空值和丢弃数据）、完全在数据库内执行所有查询，并且无需依赖竞争数据库的 BI 连接器。

七月，在 MongoWorld 结束一个多月后，我在一次商务旅行中顺道拜访了 MongoDB 在帕洛阿尔托的办公室。我所了解到的情况让我倍感鼓舞。


------

## 拜访 MongoDB

以帕洛阿尔托的标准来看，MongoDB 的办公室相当大。

之前几次去硅谷时，我看到过这家公司的招牌，但这是我第一次有机会进去看看。

就在前一周，我通过邮件与 Asya Kamsky 和 Ron Anvur 聊过天。我们讨论了我公司在 MongoDB 内部直接执行高级分析的[开源工作](http://quasar-analytics.org/)。

由于我们恰巧同时在帕洛阿尔托，Asya 邀请我过去，一边吃着外卖披萨喝着办公室的汽水，一边聊聊。

刚聊了几分钟，我就能感觉到 Asya 非常聪明、技术过硬且注重细节——这些正是你希望在像 MongoDB 这样高度技术化产品的产品经理身上看到的特质。

我向 Asya 解释了我们公司正在做的事情，并帮助她在她的电脑上运行我们的开源软件，让她可以亲自试试。我们聊着聊着，自然而然地谈到了 MongoDB 的 BI 连接器市场，上面有很多产品（如 Simba、DataDirect、CData 等等）。

我们似乎都持有相同的观点：BI 软件需要具备理解更复杂数据的能力。另一种选择是简化数据以适应老旧 BI 软件的限制，但这意味着会丢失大量信息，从而失去解决 NoSQL 分析中[关键问题](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/)的能力。

Asya 认为，MongoDB 的 BI 连接器应该能够暴露原生的 MongoDB 数据结构，比如数组，而不需要进行任何展平或转换。这种特性，我称之为*同构数据模型*，是通用 NoSQL 分析系统的关键需求之一，我在[多篇文章](http://www.infoworld.com/article/2983953/nosql/how-to-choose-a-nosql-analytics-system.html)中对此进行了深入讨论。

让我感到非常鼓舞的是，Asya 独立得出了相同的结论，这让我相信 MongoDB 已经充分理解了这个问题。我当时认为，MongoDB 的分析未来一片光明。

然而，不幸的是，我错得离谱。



--------

## MongoDB：为巨大的~~创意~~错误而生

在得知 MongoDB 走在正确的道路上之后，我对 BI 连接器放松了警惕，在接下来的几个月里没怎么关注它，虽然期间我和 Asya 以及 Ron 交换了几封电子邮件。

然而，到了九月份，我发现 MongoDB 的产品团队陷入了沉默。经过几周没有回复的电子邮件，我变得不安，开始自己四处查找线索。

我发现 Asya 分叉了一个名为 [Multicorn](https://github.com/asya999/Multicorn) 的项目，这个项目允许 Python 开发者为 PostgreSQL 编写 Foreign Data Wrappers（外部数据封装器）。

*糟糕*，我心想，*MongoDB 又要故技重施了。*

进一步挖掘后，我发现了所谓的“圣杯”：一个名为 [yam_fdw](https://github.com/asya999/yam_fdw) （Yet Another MongoDB Foreign Data Wrapper）的新项目，这是一个基于 Multicorn 用 Python 编写的全新 FDW。

根据提交日志（用于追踪代码库的更改），该项目是在我与 Asya Kamsky 于七月份会面之后才开发的。换句话说，这已经是*原型之后*的开发工作了！

最后一根稻草让我确信 MongoDB 计划将 PostgreSQL 数据库作为其“BI 连接器”发布，是当有人转发给我一个 [YouTube 视频](https://www.youtube.com/watch?v=0kwopDp0bmg)，视频中 Asya 演示了该连接器。

视频中的措辞非常谨慎，省去了任何可能带来麻烦的信息，但视频最后总结道：

> BI 连接器接收连接，并且可以使用与 Postgres 数据库**相同的网络协议**，因此如果你的报表工具可以通过 ODBC 连接，我们将提供一个 ODBC 驱动程序，您可以使用该驱动程序从您的工具连接到 BI 连接器。

此时，我毫无疑问地确认：即将随 MongoDB 3.2 一起发布的 BI 连接器实际上是伪装成 PostgreSQL 数据库的产物！

很可能，将 MongoDB 数据吸入 PostgreSQL 的实际逻辑是我之前发现的基于 Python 的 Multicorn 封装器的强化版。

到这个时候，MongoDB 的任何人都没有回复我的邮件，这对任何理智的人来说，应该已经足够让他们放弃了。

然而，我决定再尝试一次，机会是在 12 月 2 日的 MongoDB Days 会议上，那时距离 3.2 发布只有一周时间。

Eliot Horowitz 将发表主题演讲，Asya Kamsky 将会发言，Ron Avnur 可能也会出席。甚至 Dev 自己也可能会来。

那将是我说服 MongoDB 放弃 BI 连接器把戏的最佳机会。



--------

## MongoDB Days 2015，硅谷

感谢 MongoDB 出色的市场团队，再加上我在西雅图 MongoDB 巡回演讲中类似演讲的成功经验，我在 MongoDB Days 会议上获得了 45 分钟的演讲时间。

我在会议上的*官方*任务是做一场关于 MongoDB 驱动的分析的演讲，并让用户了解我们公司开发的开源软件。

但我的*个人*议程却截然不同：在 3.2 版本即将发布前，说服 MongoDB 放弃 BI 连接器。如果这个宏大的目标（很可能是*妄想*）无法实现，我至少想确认自己对该连接器的怀疑。

在会议当天，我特意向 MongoDB 的老朋友和新面孔打招呼。尽管我可能不同意某些产品决策，但公司里还是有很多出色的人，他们只是努力在做好自己的工作。

几天前我刚刚生病，但大量的咖啡让我（大部分时间）保持清醒。随着时间的推移，我在圣何塞会议中心长长的走廊里反复练习了几次演讲。

下午时分，我已经准备就绪，并在满员的会场上做了[我的演讲](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics)。让我兴奋的是，有这么多人对[MongoDB 上的视觉分析](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics)这一深奥的主题感兴趣（显然这个领域正在发展壮大）。

在与一些与会者握手并交换名片后，我开始寻找 MongoDB 的管理团队。

我首先遇到了 Eliot Horowitz，就在他即将开始主题演讲前几分钟。我们聊了聊孩子和美食，我还告诉他我公司的一些近况。

主题演讲在下午 5:10 准时开始。Eliot 先谈到了一些 3.0 版本的功能，因为显然很多公司仍停留在旧版本上。随后，他快速介绍了 MongoDB 3.2 的各种新功能。

我当时在想，Eliot 会说些什么关于 BI 连接器的内容呢？他会提到它吗？

结果发现，BI 连接器是主题演讲的一个重要内容，不仅有专门的介绍环节，甚至还进行了一场精彩的演示。



### BI Connector

Eliot 大声宣布：“MongoDB 没有原生的分析工具”，由此引出了 BI 连接器。

我觉得这有点儿好笑，因为我曾为 MongoDB 写过一篇题为 [Native Analytics for MongoDB with SlamData](https://www.mongodb.com/blog/post/native-sql-analytics-mongodb-slamdata) 的客座文章。（编辑注：MongoDB 已经撤下了这篇博客，但截至山地时间15:30，它仍然在搜索索引中 [仍在搜索索引中](https://www.mongodb.com/blog?utf8=✓&search=slamdata#)）。SlamData 也是 MongoDB 的合作伙伴，并赞助了 MongoDB Days 大会。

在介绍 BI 连接器的用途时，Eliot 似乎有些磕磕绊绊（从...可操作的洞察中获取操作？*麻烦的分析！*）。当他把演示交给 Asya Kamsky 时，似乎松了一口气，后者为活动准备了一个不错的演示。

在演示过程中，我发现 Asya 表现得比平时紧张。她斟词酌句，省略了关于连接器是什么的所有细节，只提到了它如何工作的无罪部分（比如它依赖 DRDL 来定义 MongoDB 的 schema）。大部分演示内容并没有集中在 BI 连接器上，而是更多地展示了 Tableau（当然，Tableau 的演示效果确实很好！）。

我所有的反馈都没能减缓 BI 连接器的进展。

### 全力以赴

主题演讲结束后，大批与会者前往隔壁房间参加鸡尾酒会。与会者大多在与其他与会者交谈，而 MongoDB 的员工则倾向于聚在一起。

我看到 Ron Avnur 与服务器工程副总裁 Dan Pasette 聊天，距离他们几英尺远的地方，正为与会者提供 Lagunitas IPA 的啤酒。

现在是行动的时候了。3.2 版本即将发布，几天之内就会面世。MongoDB 的人都不再回复邮件。Eliot 刚刚告诉全世界 MongoDB 没有原生的分析工具，并将 BI 连接器定位为 NoSQL 分析的革命性工具。

没有什么可失去的了，我走到 Ron 面前，加入了他们的对话，然后开始了一段大约两分钟的激烈独白，猛烈抨击 BI 连接器。

我告诉他，我对 MongoDB 的期望不仅仅是把 PostgreSQL 数据库伪装成 MongoDB 分析的神奇解决方案。我告诉他，MongoDB 应该表现出诚信和领导力，推出一个支持 MongoDB 丰富数据结构的解决方案，将所有计算都推送到数据库中，并且不依赖于竞争对手的数据库。

Ron 被震住了。他开始用模糊的语言为 BI 连接器的“下推”（pushdown）辩护，我意识到这是确认我怀疑的机会。

“Postgres 外部数据封装器几乎不支持下推”，我不动声色地说道。“这在你用于 BI 连接器的 Multicorn 封装器中更是如此，这个封装器基于较旧的 Postgres 版本，甚至不支持 Postgres FDW 的完整下推功能。”

Ron 承认失败。“这是事实”，他说。

我逼他为这个决定辩护。但他无言以对。我告诉他，在 MongoDB 发布“BI 连接器”之前，立即拉下停止绳。Ron 对这个可能性不以为然，我告诉他，这件事会彻底让他难堪。“你可能是对的，”他说，“但我现在有更大的事情要担心，”可能指的是即将发布的 3.2 版本。

我们三个人一起喝了杯啤酒。我指着 Dan 说，“这家伙的团队开发了一个真正能够进行分析的数据库。你们为什么不在 BI 连接器中使用它？”但这没有用，Ron 不为所动。

我们分道扬镳，同意彼此保留不同意见。

我从房间另一头看到了 Dev Ittycheria，走过去和他聊了几句。我称赞了市场部的工作，然后开始批评产品。我告诉 Dev，“在我看来，产品团队正在犯一些错误。”他想了解更多，所以我告诉了他我的看法，我已经重复了很多次，以至于我都能倒背如流了。他让我发邮件跟进，当然我发了，但再也没收到回复。

与 Dev 交谈后，我终于意识到我无法改变 MongoDB 3.2 的发布进程。它将与 BI 连接器一起发布，而我对此无能为力。

我很失望，但同时也感觉到一阵巨大的解脱。我已经和我能接触到的每个人都谈过了。我已经全力以赴。我已经竭尽全力。

当我离开鸡尾酒会，回到酒店时，不禁猜测公司为什么会做出我如此强烈反对的决定。


--------

## MongoDB：孤家寡人，孤岛一座

经过深思熟虑，我现在认为 MongoDB 做出糟糕产品决策的原因在于无法专注于核心数据库。而这种无法专注的原因，则在于其未能培育出一个 NoSQL 生态系统。

关系型数据库之所以能占据主导地位，部分原因在于围绕这些数据库发展的庞大生态系统。

这个生态系统催生了备份、复制、分析、报告、安全、治理以及许多其他类别的应用程序。它们相互依赖，并促进彼此的成功，形成了网络效应和高转换成本，这些都对当今的 NoSQL 厂商构成了挑战。

与之形成鲜明对比的是，MongoDB 周围几乎*没有生态系统*，而且不仅我一个人注意到了这一点 [注意到这一点](http://slamdata.com/blog/2014/12/09/where-is-the-nosql-ecosystem.html)。

为什么 MongoDB 没有生态系统？

我带有讽刺意味的回答是，如果你是一个为 MongoDB 提供原生分析的合作伙伴，MongoDB 的 CTO 会站在舞台上说，没有工具可以为 MongoDB 提供原生分析。

然而，更客观地说，我认为上述现象只是一个表象。*真正的问题*是 MongoDB 的合作伙伴计划完全失效了。

MongoDB 的合作伙伴团队直接向首席营收官（Carlos Delatorre）汇报工作，这意味着合作伙伴团队的主要任务是从合作伙伴那里获取收入。这种设置本质上会让合作伙伴活动偏向那些没有兴趣推动 NoSQL 生态系统发展的大型公司（事实上，其中许多公司还在生产与 MongoDB 竞争的关系型解决方案）。

这与 SlamData、Datos IO 等小型、以 NoSQL 为中心的公司形成鲜明对比。这些公司之所以能够成功，*正是因为* NoSQL 的成功，它们提供了关系型数据库世界中标准的功能，而 NoSQL 数据库*需要*这些功能才能在企业级环境中蓬勃发展。

作为合作伙伴已经超过一年，我可以告诉你，几乎没有人知道 SlamData 的存在，尽管 SlamData 是企业选择 MongoDB 而不是其他 NoSQL 数据库（例如 MarkLogic）的一个强大动因，也是那些考虑从关系型技术（例如 Oracle）转向 MongoDB 的公司转型的推动者。

尽管合作伙伴们在努力，但 MongoDB 似乎对由 NoSQL 为中心的合作伙伴所带来的联合收入和销售机会完全不感兴趣。没有转售协议、没有收入分享、没有销售简介、没有联合营销，只有一个 Logo。

这意味着在组织上，MongoDB 忽视了那些可能对他们最有帮助的 NoSQL 为中心的合作伙伴。同时，他们的最大客户和潜在客户不断要求提供在关系型世界中常见的基础设施，比如备份、复制、监控、分析、数据可视化、报告、数据治理、查询分析等。

这些来自大公司源源不断的需求，结合未能培养出生态系统的无力，形成了一种*有毒的组合*。它导致 MongoDB 产品团队试图通过构建*所有可能的产品*来*创造自己的生态系统*！

备份？有。复制？有。监控？有。BI 连接性？有。数据发现？有。可视化分析？有。

但一个有限资源的 NoSQL 数据库供应商不可能围绕自己建立一个生态系统，去与围绕关系型技术的庞大生态系统竞争（代价太高了！）。因此，这导致了像 MongoDB Compass 这样的分散注意力的项目，以及像 BI 连接器这样的“伪”技术。

替代方案是什么？在我看来，非常简单。

首先，MongoDB 应该培育一个充满活力的、由风险投资支持的 NoSQL 为中心的合作伙伴生态系统（*而不是*拥有雄厚资金的关系型合作伙伴！）。这些合作伙伴应该在各自的领域内具有深厚的专业知识，并且它们都应该在 MongoDB 成功的情况下成功。

MongoDB 的销售代表和客户经理应该掌握由合作伙伴提供的信息，这些信息可以帮助他们克服异议并减少客户流失，而 MongoDB 应该将其构建为一个健康的收入来源。

其次，在通过 NoSQL 为中心的合作伙伴满足了客户对相关基础设施的需求之后，MongoDB 应该将产品和销售重点放在核心数据库上，这才是*数据库供应商*应当赚钱的方式！

MongoDB 应该开发对企业有重要价值的功能（例如 ACID 事务、NVRAM 存储引擎、列式存储引擎、跨数据中心复制等），并仔细划定社区版和企业版之间的界限。所有这一切都应该以一种方式进行，使*开发者*在不同版本中拥有相同的能力。

目标应该是让 MongoDB 从数据库中获得足够的收入，以至于产品团队不会再受到诱惑去发明一个劣质的生态系统。

你可以自己判断，但我认为哪个是更有可能成功的战略已经非常明显了。




--------

## 再见了，MongoDB！

显然，我无法支持这样的产品决策——推出一个竞争性的关系型数据库，作为在像 MongoDB 这样后关系型数据库上进行分析的最终解决方案。

在我看来，这个决定对社区不利，对客户不利，对新兴的 NoSQL 分析领域也不利。

此外，如果这种做法没有 *完全透明*，它对诚信也是有害的，而诚信是 *所有公司* 的基石（尤其是开源公司）。

所以，通过这篇文章，我正式放弃。

不再给 MongoDB 发狂热的邮件。不再在 MongoDB 的鸡尾酒会上缠着管理层。不再与一个连邮件都不回的公司私下分享我的意见。

这条路我走过了，做过了，但没有效果。

显然，我现在要揭发这个事实。当你读到这篇文章时，全世界都将知道 MongoDB 3.2 BI 连接器实际上就是 PostgreSQL 数据库，附带一些拼接数据的工具，把一些数据丢弃，然后把剩下的部分吸入 PostgreSQL。

这对那些正在评估 MongoDB 的公司意味着什么？

这取决于你们自己，但就我个人而言，如果你在寻找一个 NoSQL 数据库，同时需要传统的 BI 连接性，并且也在考虑 PostgreSQL，那么你可能应该直接选择 PostgreSQL。

毕竟，MongoDB 对 MongoDB 上的分析问题的 *自己答案* 就是将数据从 MongoDB 中导出，扁平化，然后倒入 PostgreSQL。如果你的数据最终会变成在 PostgreSQL 中的扁平化关系数据，那为什么不直接从那里开始呢？一石二鸟！

至少你可以指望 PostgreSQL 社区在 NoSQL 领域的创新，他们已经这么做很多年了。社区绝不会将 MongoDB 数据库打包成一个假的“PostgreSQL NoSQL”产品，然后称其为 NoSQL 数据库技术的革命。

而遗憾的是，这恰恰就是 MongoDB 反其道而行之的做法。

------

*这张“Shame”的照片由 [Grey World](https://www.flickr.com/photos/greyworld/) 拍摄，版权归 Grey World 所有，并根据 [CC By 2.0](https://creativecommons.org/licenses/by/2.0/) 许可发布。*









--------

# MongoDB 3.2: Now Powered by PostgreSQL

> John De Goes —— Challenging the status quo at Ziverge

发布日期: 2015年12月8日


*Opinions expressed are solely my own, and do not express the views or opinions of my [employer](http://slamdata.com/).*

When I finally pieced together all the clues, I was *shocked*. If I was right, [MongoDB](http://mongodb.com/)was about to make what I would call the *biggest mistake ever made* in the history of database companies.

I work on an [open source analytics tool](http://github.com/slamdata/slamdata) that connects to NoSQL databases like MongoDB, so I spend my days rooting for these next-generation database vendors to succeed.

In fact, I just presented to a [packed room](https://twitter.com/slamdata/status/672166743255592960) at [MongoDB Days Silicon Valley](https://www.mongodb.com/events/mongodb-days-siliconvalley), [making a case](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) for companies to adopt the new database.

So when I uncovered a secret this destructive, I hit the panic button: on November 12th, 2015, I sent an email to Asya Kamsky, Lead Product Manager at MongoDB.

While polite, I made my opinion crystal clear: *MongoDB is about to make a giant mistake, and should reconsider while there's still time*.

I would never hear back from Asya — or anyone else about the matter. My earlier success in helping convince MongoDB to [reverse course](https://www.mongodb.com/blog/post/revisiting-usdlookup) when they tried to monetize [the wrong feature](http://slamdata.com/blog/2015/10/21/mongodb-missing-join.html) would not be repeated.

This is the story of what I discovered, how I pieced together the clues from press releases, YouTube videos, and source code scattered on Github, and how I ultimately failed to convince MongoDB to change course.

The story begins on June 1st 2015, at the annual MongoWorld conference in New York City.


--------

## MongoWorld 2015

[SlamData](http://slamdata.com/), my new analytics startup, was sponsoring MongoWorld 2015, so I got a rare ticket to the VIP party the night before the conference.

Hosted at NASDAQ MarketWatch, in a beautiful space overlooking Times Square, I felt distinctly underdressed in my cargo pants and startup t-shirt. Fancy h'ordeuvres and alcohol flowed freely, and MongoDB's management team was out in full force.

I shook hands with MongoDB's new CEO, Dev ("Dave") Ittycheria, and offered him a few words of encouragement for the road ahead.

Only this year, Fidelity Investments [slashed](http://fortune.com/2015/11/12/fidelity-marks-down-tech-unicorns/) its valuation of MongoDB to 50% of what it was back in 2013 ($1.6B), downgrading the startup from "unicorn"  to "donkey".

It's been Dev's job to prove Fidelity and the rest of the naysayers wrong.

Dev inherited the company from Max Schireson (who [famously resigned](http://maxschireson.com/2014/08/05/1137/) in 2014), and in his tenure, Dev has built out a new management team at MongoDB, with ripples felt across the company.

Though I only spoke with Dev for a few minutes, he seemed bright, friendly, and eager to learn about what my company was doing. He handed me his card and asked me to call him if I ever needed anything.

Next up was Eliot Horowitz, CTO and co-founder of MongoDB. I shook his hand, introduced myself, and delivered a 30 second pitch for my startup.

At the time, I thought my pitch must have been terrible, since Eliot seemed disinterested in everything I was saying. Turns out Eliot hates SQL and views analytics as a nuisance, so it's not surprising I bored him!

Eliot did catch the word "analytics", however, and dropped that tomorrow at the conference, MongoDB would have some news about the upcoming 3.2 release that I would find very interesting.

I pleaded for more details, but nope, that was strictly confidential. I'd find out the following day, along with the rest of the world.

I passed along the tip to my co-founder, Jeff Carr, and we shared a brief moment of panic. The big fear for our four-person, self-funded startup was that MongoDB would be announcing their own analytics tool for MongoDB, which could hurt our chances of raising money.

Much to our relief, we'd find out the following day that MongoDB's big announcement wasn't an analytics tool. Instead, it was a solution called *MongoDB BI Connector*, a headline feature of the upcoming 3.2 release.



--------

## The MongoDB 3.2 BI Connector

Eliot had the honor of announcing the BI connector. Of all the things he was announcing, Eliot seemed least interested in the connector, so it got barely more than a mention.

But details soon spread like wildfire thanks to an [official press release](https://www.mongodb.com/press/opens-modern-application-data-to-new-generation-visual-analysis-and-traditional-bi-tools), which contained this succinct summary:

> MongoDB today announced a new connector for BI and visualization, which connects MongoDB to industry-standard business intelligence (BI) and data visualization tools. Designed to work with every SQL-compliant data analysis tool on the market, including Tableau, SAP Business Objects, Qlik and IBM Cognos Business Intelligence, the connector is currently in preview release and expected to become generally available in the fourth quarter of 2015.

According to the press release, the BI connector would allow *any BI software in the world* to interface with the MongoDB database.

News of the connector [caught fire](https://twitter.com/search?f=tweets&vertical=default&q=mongodb bi connector&src=typd) on Twitter, and the media went into a frenzy. The story was picked up by [TechCrunch](http://techcrunch.com/2015/06/02/new-mongodb-connector-creates-direct-connection-to-data-visualization-tools/) and many others. Every retelling added new embellishments, with Fortune even claiming the BI connector had actually been [released at MongoWorld](http://fortune.com/2015/06/03/couchbase-mongodb-embrace-sql/)!

Given the nature of the announcement, the media hoopla was probably justified.

### When Worlds Collide

MongoDB, like many other NoSQL databases, does not store relational data. It stores rich data structures that relational BI software cannot understand.

Kelly Stirman, VP of Strategy at MongoDB, explained the problem well:

> *“The thing that defines these apps as modern is rich data structures that don’t fit neatly into rows and columns of traditional databases*."

A connector that enabled any BI software in the world to do robust analytics on rich data structures, *with no loss of analytic fidelity*, would be *giant news*.

Had MongoDB really done the impossible? Had they developed a connector which satisfies all the [requirements of NoSQL analytics](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/), but exposes relational semantics on flat, uniform data, so legacy BI software can handle it?

A couple months earlier, I had chatted with Ron Avnur, VP of Products at MongoDB. Ron indicated that all of MongoDB's customers wanted analytics, but that they hadn't decided whether to build something in-house or work with a partner.

This meant that MongoDB had gone from *nothing* to *magic* in just a few months.



### Pulling Back the Curtain

After the announcement, Jeff and I headed back to our sponsor booth, and Jeff asked me the most obvious question: *"How did they go from nothing to a BI connector that works with all possible BI tools in just a couple months?!?"*

I thought carefully about the question.

Among other problems that a BI connector would need to solve, it would have to be capable of efficiently executing SQL-like analytics on MongoDB. From my [deep](http://github.com/quasar-analytics/)[background](http://github.com/precog) in analytics, I knew that efficiently executing general-purpose analytics on modern databases like MongoDB is very challenging.

These databases support very rich data structures and their interfaces are designed for so-called *operational* use cases (not *analytical* use cases). The kind of technology that can leverage operational interfaces to run arbitrary analytics on rich data structures takes *years* to develop. It's not something you can crank out in two months.

So I gave Jeff my gut response: *"They didn't create a new BI connector. It's impossible. Something else is going on here!"*

I didn't know what, exactly. But in between shaking hands and handing out cards, I did some digging.

Tableau showed a demo of their software working with the MongoDB BI Connector, which piqued my curiosity. Tableau has set the standard for visual analytics on relational databases, and their forward-thinking big data team has been giving NoSQL some serious thought.

Thanks to their relationship with MongoDB, Tableau issued a [press release](http://www.tableau.com/about/blog/2015/6/tableau-mongodb-visual-analytics-json-speed-thought-39557) to coincide with the MongoWorld announcement, which I found on their website.

I pored through this press release hoping to learn some new details. Burried deep inside, I discovered the faintest hint about what was going on:

> MongoDB will soon announce beta availability of the connector, with general availability planned around the MongoDB 3.2 release late this year. During MongoDB’s beta, Tableau will be supporting the MongoDB connector on both Windows and Mac **via our PostgreSQL driver**.

These were the words that gave me my first clue: *via our PostgreSQL driver*. This implied, at a minimum, that MongoDB's BI Connector would speak the same "language" (*wire protocol*) as the PostgreSQL database.

That struck me as more than a little suspicious: was MongoDB actually re-implementing the *entirety* of the PostgreSQL wire protocol, including support for hundreds of PostgreSQL functions?

While *possible*, this seemed *extremely unlikely*.

I turned my gaze to Github, looking for open source projects that MongoDB might have leveraged. The conference Wifi was flaky, so I had to tether to my phone while I looked through dozens of repositories that mentioned both PostgreSQL and MongoDB.

Eventually, I found what I was looking for: [mongoose_fdw](https://github.com/asya999/mongoose_fdw/commits/master), an open source repository forked by Asya Kamsky (whom I did not know at the time, but her profile mentioned she worked for MongoDB).

The repository contained a so-called *Foreign Data Wrapper* (FDW) for the PostgreSQL database. The FDW interface allows developers to plug in other data sources, so that PostgreSQL can pull the data out and execute SQL on the data (NoSQL data must be flattened, null-padded, and otherwise dumbed-down for this to work properly for BI tools).

*"I think I know what's going on"*, I told Jeff. *"For the prototype, it looks like they might be flattening out the data and using a different database to execute the SQL generated by the BI software."*

*"What database?"* he shot back.

*"PostgreSQL."*

Jeff was speechless. He didn't say a word. But I could tell *exactly* what he was thinking, because I was thinking it too.

*Shit. This is bad news for MongoDB. Really bad.*



--------

## PostgreSQL: The MongoDB Killer

PostgreSQL is a popular open source relational database. So popular, in fact, it's currently [neck-and-neck with MongoDB](http://db-engines.com/en/ranking).

The database is *fierce competition* for MongoDB, primarily because it has acquired some of the features of MongoDB, including the ability to store, validate, manipulate, and index [JSON documents](https://en.wikipedia.org/wiki/JSON). Third-party software even [gives it the ability](https://www.citusdata.com/) to scale horizontally (or should I say, hu*mongo*usly).

Every month or so, someone writes an article that recommends PostgreSQL over MongoDB. Often, the article goes viral and skyrockets to the top of hacker websites. A few of these articles are shown below:

- [Goodbye MongoDB. Hello PostgreSQL](http://developer.olery.com/blog/goodbye-mongodb-hello-postgresql/)
- [Postgres Outperforms MongoDB and Ushers in New Developer Reality](http://www.enterprisedb.com/postgres-plus-edb-blog/marc-linster/postgres-outperforms-mongodb-and-ushers-new-developer-reality)
- [MongoDB is dead. Long live Postgresql :)](https://github.com/errbit/errbit/issues/614)
- [Why You Should Never Use MongoDB](http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/)
- [SQL vs NoSQL KO. Postgres vs Mongo](https://www.airpair.com/postgresql/posts/sql-vs-nosql-ko-postgres-vs-mongo)
- [Why I Migrated Away from MongoDB](http://svs.io/post/31724990463/why-i-migrated-away-from-mongodb)
- [Why you should never, ever, ever use MongoDB](http://cryto.net/~joepie91/blog/2015/07/19/why-you-should-never-ever-ever-use-mongodb/)
- [Is Postgres NoSQL Better than MongoDB?](http://www.aptuz.com/blog/is-postgres-nosql-database-better-than-mongodb/)
- [Bye Bye MongoDB. Guten Tag PostgreSQL](https://www.userlike.com/en/blog/2015/10/09/bye-by-mysql-and-mongodb-guten-tag-postgresql)

The largest company commercializing PostgreSQL is [EnterpriseDB](http://enterprisedb.com/) (though there are plenty of others, some older or just as active), which maintains a [large repository of content](http://www.enterprisedb.com/nosql-for-enterprise) on the official website arguing that PostgreSQL is a better NoSQL database than MongoDB.

Whatever your opinion on that point, one thing is clear: MongoDB and PostgreSQL are locked in a vicious, bloody battle for mind share among developers.



--------

## From Prototype to Production

As any engineer worth her salt will tell you, *prototypes aren't for production*.

Even if MongoDB *was* using PostgreSQL as a prototype BI connector, maybe some brilliant MongoDB engineers were locked in a room somewhere, working on a standalone production version.

Indeed, the way Tableau worded their press release even implied the dependency on the PostgreSQL driver *might* be temporary:

> **During MongoDB’s beta**, Tableau will be supporting the MongoDB connector on both Windows and Mac via our PostgreSQL driver.

Perhaps, I thought, the 3.2 release of MongoDB would ship with the *real deal*: a BI connector that exposes the rich data structures that MongoDB supports (instead of flattening, null-padding, and throwing away data), executes all queries 100% in-database, and has no dependencies on competing databases.

In July, more than a month after MongoWorld, I dropped by MongoDB's offices in Palo Alto during a business trip. And I was very encouraged by what I learned.


--------

## A Trip to MongoDB

By Palo Alto's standards, MongoDB's office is quite large.

I had seen the company's sign during previous trips to the Valley, but this was the first time I had a chance to go inside.

The week before, I was chatting with Asya Kamsky and Ron Anvur by email. We were discussing my company's [open source work](http://quasar-analytics.org/) in executing advanced analytics on rich data structures directly inside MongoDB.

Since we happened to be in Palo Alto at the same time, Asya invited me over to chat over catered pizza and office soda.

Within the first few minutes, I could tell that Asya was smart, technical, and detail-oriented — exactly the traits you'd hope for in a product manager for a highly technical product like MongoDB.

I explained to Asya what my company was doing, and helped her get our open source software up and running on her machine so she could play with it. At some point, we started chatting about BI connectors for MongoDB, of which there were several in the market (Simba, DataDirect, CData, and others).

We both seemed to share the same view: that BI software needs to gain the ability to understand more complex data. The alternative, which involves dumbing down the data to fit the limitations of older BI software, means throwing away so much information, you lose the ability to solve [key problems](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/) in NoSQL analytics.

Asya thought a BI connector for MongoDB should expose the native MongoDB data structures, such as arrays, without any flattening or transformations. This characteristic, which I have termed *isomorphic data model*, is one of the key requirements for a general-purpose NoSQL analytics, a topic I've [written about](http://www.infoworld.com/article/2983953/nosql/how-to-choose-a-nosql-analytics-system.html) extensively.

I was very encouraged that Asya had independently come to the same conclusion, and felt confident that MongoDB understood the problem. I thought the future of analytics for MongoDB looked very bright.

Unfortunately, I could not have been more wrong.

--------

## MongoDB: For Giant ~~Ideas~~Mistakes

Delighted that MongoDB was on the right track, I paid little attention to the BI connector for the next couple of months, though I did exchange a few emails with Asya and Ron.

Heading into September, however, I encountered utter silence from the product team at MongoDB. After a few weeks of unreturned emails, I grew restless, and started poking around on my own.

I discovered that Asya had forked a project called [Multicorn](https://github.com/asya999/Multicorn), which allows Python developers to write Foreign Data Wrappers for PostgreSQL.

*Uh oh*, I thought, *MongoDB is back to its old tricks.*

More digging turned up the holy grail: a new project called [yam_fdw](https://github.com/asya999/yam_fdw) (Yet Another MongoDB Foreign Data Wrapper), a brand new FDW written in Python using Multicorn.

According to the commit log (which tracks changes to the repository), the project had been built recently, after my July meeting with Asya Kamsky. In other words, this was *post-prototype* development work!

The final nail in the coffin, which convinced me that MongoDB was planning on shipping the PostgreSQL database as their "BI connector", happened when someone forwarded me a [video on YouTube](https://www.youtube.com/watch?v=0kwopDp0bmg), in which Asya demoed the connector.

Worded very cautiously, and omitting any incriminating information, the video nonetheless ended with this summary:

> The BI Connector receives connections and can speak the **same wire protocol that the Postgres database****does**, so if your reporting tool can connect via ODBC, we will have an ODBC driver that you will be able to use from your tool to the BI Connector.

At that point, I had zero doubt: the production version of the BI connector, to be shipped with MongoDB 3.2, was, in fact, the PostgreSQL database in disguise!

Most likely, the actual logic that sucked data out of MongoDB into PostgreSQL was a souped-up version of the Python-based Multicorn wrapper I had discovered earlier.

At this point, no one at MongoDB was returning emails, which to any sane person, would have been enough to call it quits.

Instead, I decided to give it one more try, at the MongoDB Days conference on December 2, just one week before the release of 3.2.

Eliot Horowitz was delivering a keynote, Asya Kamsky would be speaking, and Ron Avnur would probably attend. Possibly, even Dev himself might drop by.

That's when I'd have my best chance of convincing MongoDB to ditch the BI connector shenanigans.


--------

## MongoDB Days 2015, Silicon Valley

Thanks to the wonderful marketing team at MongoDB, and based on the success of a similar talk I gave in Seattle at a MongoDB road show, I had a 45 minute presentation at the MongoDB Days conference.

My *official* purpose at the conference was to deliver my talk on MongoDB-powered analytics, and make users aware of the open source software that my company develops.

But my *personal* agenda was quite different: convincing MongoDB to can the BI connector before the impending 3.2 release. Failing that lofty and most likely *delusional* goal, I wanted to confirm my suspicions about the connector.

On the day of the conference, I went out of my way to say hello to old and new faces at MongoDB. Regardless of how much I may disagree with certain product decisions, there are many amazing people at the company just trying to do their jobs.

I had gotten sick a few days earlier, but copious amounts of coffee kept me (mostly) awake. As the day progressed, I rehearsed my talk a few times, pacing the long corridors of the San Jose Convention Center.

When the afternoon rolled around, I was ready, and gave [my talk](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) to a packed room. I was excited about how many people were interested in the esoteric topic of [visual analytics on MongoDB](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) (clearly the space was growing).

After shaking hands and exchanging cards with some of the attendees, I went on the hunt for the MongoDB management team.

I first ran into Eliot Horowitz, moments before his keynote. We chatted kids and food, and I told him how things were going at my company.

The keynote started sharply at 5:10. Eliot talked about some of the features in 3.0, since a lot of companies are apparently stuck on older versions. He then proceeded to give a whirlwind tour of the features of MongoDB 3.2.

I wondered what Eliot would say about the BI connector. Would he even mention it?

Turns out, the BI connector was a leading feature of the keynote, having its own dedicated segment and even a whiz-bang demo.

### The BI Connector

Eliot introduced the BI connector by loudly making the proclamation, *"MongoDB has no native analytics tools."*

I found that somewhat amusing, since I wrote a guest post for MongoDB titled [Native Analytics for MongoDB with SlamData](https://www.mongodb.com/blog/post/native-sql-analytics-mongodb-slamdata) *(Edit: MongoDB has taken down the blog post, but as of 15:30 MDT, it's [still in the search index](https://www.mongodb.com/blog?utf8=✓&search=slamdata#))*. SlamData is also a MongoDB partner and sponsored the MongoDB Days conference. 

Eliot seemed to stumble a bit when describing the purpose of the BI connector (getting actions from... actionable insights? *Pesky analytics*!). He looked relieved when he handed the presentation over to Asya Kamsky, who had prepared a nice demo for the event.

During the presentation, Asya seemed uncharacteristically nervous to me. She chose every word carefully, and left out all details about what the connector was,  only covering the non-incriminating parts of how it worked (such as its reliance on DRDL to define MongoDB schemas). Most of the presentation focused not on the BI connector, but on Tableau (which, of course, demos very well!).

All my feedback hadn't even slowed the BI connector down.

### Pulling Out All the Stops

After the keynote, the swarm of conference attendees proceeded to the cocktail reception in the adjacent room. Attendees spent most of their time talking to other attendees, while MongoDB employees tended to congregate in bunches.

I saw Ron Avnur chatting with Dan Pasette, VP of Server Engineering, a few feet from the keg of Lagunitas IPA they were serving attendees.

Now was the time to act.

The 3.2 release was coming out in mere days. No one at MongoDB was returning emails. Eliot had just told the world there were no native analytics tools for MongoDB, and had positioned the BI connector as a revolution for NoSQL analytics.

With nothing to lose, I walked up to Ron, inserted myself into the conversation, and then began ranting against the BI connector in what was probably a two-minute, highly-animated monologue.

I told him I expected more from MongoDB than disguising the PostgreSQL database as the magical solution to MongoDB analytics. I told him that MongoDB should have demonstrated integrity and leadership, and shipped a solution that supports the rich data structures that MongoDB supports, pushes all computation into the database, and doesn't have any dependencies on a competing database.

Ron was stunned. He began to defend the BI connector's "pushdown" in vague terms, and I realized this was my chance to confirm my suspicions.

*"Postgres foreign data wrappers support barely any pushdown,"* I stated matter-of-factly. *"This is all the more true in the Multicorn wrapper you're using for the BI connector, which is based on an older Postgres and doesn't even support the full pushdown capabilities of the Postgres FDW."*

Ron admitted defeat. *"That's true,"* he said.

I pushed him to defend the decision. But he had no answer. I told him to pull the stop cord right now, before MongoDB released the "BI connector". When Ron shrugged off that possibility, I told him the whole thing was going to blow up in his face. *"You might be right,"* he said, *"But I have bigger things to worry about right now,"* possibly referring to the upcoming 3.2 release.

We had a beer together, the three of us. I pointed to Dan, *"This guy's team has built a database that can actually do analytics. Why aren't you using it in the BI connector?"* But it was no use. Ron wasn't budging.

We parted ways, agreeing to disagree.

I spotted Dev Ittycheria from across the room, and walked over to him. I complimented the work that the marketing department was doing, before moving on to critique product. I told Dev, *"In my opinion, product is making some mistakes."* He wanted to know more, so I gave him my spiel, which I had repeated often enough to know by heart. He told me to followup by email, and of course I did, but I never heard back.

After my conversation with Dev, it finally sunk in that I would not be able to change the course of MongoDB 3.2. It would ship with the BI connector, and there wasn't a single thing that I could do about it.

I was disappointed, but at the same time, I felt a huge wave of relief. I had talked to everyone I could. I had pulled out all the stops. I had given it my all.

As I left the cocktail reception, and headed back to my hotel, I couldn't help but speculate on why the company was making decisions that I so strongly opposed.

## MongoDB: An Island of One

After much reflection, I now think that MongoDB's poor product decisions are caused by an inability to focus on the core database. This inability to focus is caused by an inability to cultivate a NoSQL ecosystem.

Relational databases rose to dominance, in part, because of the astounding ecosystem that grew around these databases.

This ecosystem gave birth to backup, replication, analytics, reporting, security, governance, and numerous other category-defining applications. Each depended on and contributed to the success of the others, creating network benefits and high switching costs that are proving troublesome for modern-day NoSQL vendors.

In contrast, there's virtually *no ecosystem* around MongoDB, and I'm not the only one to [notice this fact](http://slamdata.com/blog/2014/12/09/where-is-the-nosql-ecosystem.html).

Why isn't there an ecosystem around MongoDB?

My snarky answer is that because, if you are a MongoDB partner that provides native analytics for MongoDB, the CTO will get up on stage and say there are no tools that provide native analytics for MongoDB.

More objectively, however, I think the above is just a symptom. The *actual problem* is that the MongoDB partner program is totally broken.

The partner team at MongoDB reports directly to the Chief Revenue Officer (Carlos Delatorre), which implies the primary job of the partner team is to extract revenue from partners. This inherently skews partner activities towards large companies that have no vested interest in the success of the NoSQL ecosystem (indeed, many of them produce competing relational solutions).

Contrast that with small, NoSQL-centric companies like SlamData, Datos IO, and others. These companies succeed *precisely* in the case that NoSQL succeeds, and they provide functionality that's standard in the relational world, which NoSQL databases *need* to thrive in the Enterprise.

After being a partner for more than a year, I can tell you that almost no one in MongoDB knew about the existence of SlamData, despite the fact that SlamData acted as a powerful incentive for companies to choose MongoDB over other NoSQL databases (e.g. MarkLogic), and an enabler for companies considering the switch from relational technology (e.g. Oracle).

Despite the fact that partners try, MongoDB appears completely unconcerned about the joint revenue and sales opportunities presented by NoSQL-centric partners. No reseller agreements. No revenue sharing. No sales one-pagers. No cross-marketing. Nothing but a logo.

This means that organizationally, MongoDB ignores the NoSQL-centric partners who could most benefit them. Meanwhile, their largest customers and prospects keep demanding infrastructure common to the relational world, such as backup, replication, monitoring, analytics, data visualization, reporting, data governance, query analysis, and much more.

This incessant demand from larger companies, combined with the inability to cultivate an ecosystem, forms a *toxic combination*. It leads MongoDB product to try to *create its own ecosystem* by building *all possible products*!

Backup? Check. Replication? Check. Monitoring? Check. BI connectivity? Check. Data discovery? Check. Visual analytics? Check.

But a single NoSQL database vendor with finite resources cannot possibly build an ecosystem around itself to compete with the massive ecosystem around relational technology (it's far too expensive!). So this leads to distractions, like MongoDB Compass, and "sham" technology, like the BI connector.

What's the alternative? In my humble opinion, it's quite simple.

First, MongoDB should nurture a vibrant, venture-funded ecosystem of NoSQL-centric partners (*not* relational partners with deep pockets!). These partners should have deep domain expertise in their respective spaces, and all of them should succeed precisely in the case that MongoDB succeeds.

MongoDB sales reps and account managers should be empowered with partner-provided information that helps them overcome objections and reduce churn, and MongoDB should build this into a healthy revenue stream.

Second, with customer demand for related infrastructure satisfied by NoSQL-centric partners, MongoDB should focus both product *and* sales on the core database, which is how a *database vendor* should make money!

MongoDB should develop features that have significant value to Enterprise (such as ACID transactions, NVRAM storage engines, columnar storage engines, cross data center replication, etc.), and thoughtfully draw the line between Community and Enterprise. All in a way that gives *developers* the same capabilities across editions.

The goal should be for MongoDB to drive enough revenue off the database that product won't be tempted to invent an inferior ecosystem.

You be the judge, but I think it's pretty clear which is the winning strategy.

## Bye-Bye, MongoDB

Clearly, I cannot get behind product decisions like shipping a competing relational database as the definitive answer to analytics on a post-relational database like MongoDB.

In my opinion, this decision is bad for the community, it's bad for customers, and it's bad for the emerging space of NoSQL analytics.

In addition, to the extent it's not done with *full transparency*, it's also bad for integrity, which is a pillar on which *all companies* should be founded (especially open source companies).

So with this post, I'm officially giving up.

No more frantic emails to MongoDB. No more monopolizing management at MongoDB cocktail parties. No more sharing my opinions in private with a company that doesn't even return emails.

Been there, done that, didn't work.

I'm also, obviously, blowing the whistle. By the time you're reading this, the whole world will know that the MongoDB 3.2 BI Connector is the PostgreSQL database, with some glue to flatten data, throw away bits and pieces, and suck out whatever's left into PostgreSQL.

What does all this mean for companies evaluating MongoDB?

That's your call, but personally, I'd say if you're in the market for a NoSQL database, you need legacy BI connectivity, and you're also considering PostgreSQL, you should probably just pick PostgreSQL.

After all, MongoDB's *own answer* to the problem of analytics on MongoDB is to pump the data out of MongoDB, flatten it out, and dump it into PostgreSQL. If your data is going to end up as flat relational data in PostgreSQL, why not start out there, too? Kill two birds with one stone!

At least you can count on the PostgreSQL community to innovate around NoSQL, which they've been doing for years. There's zero chance the community would package up the MongoDB database into a sham "PostgreSQL NoSQL" product, and call it a revolution in NoSQL database technology.

Which is, sadly, *exactly* what MongoDB has done in reverse.

--------

*The Shame photo taken by [Grey World](https://www.flickr.com/photos/greyworld/), copyright Grey World, and licensed under [CC By 2.0](https://creativecommons.org/licenses/by/2.0/).*

