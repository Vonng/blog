---
title: "OPC 一个月烧 1000 刀订阅，能有多少产出？"
date: 2026-08-12
author: 冯若航
summary: >
  过去一个多月，我同时蹬着 7 个每月 200 美元的 AI 订阅，盘点 Silo、Pigsty、PGEXT、SOW、OINK 等项目，看看上千亿 Token 最后变成了哪些代码、产品与长期资产。
tags: [AI, Agent ]
ai: true
---

很多人问我：你同时蹬着 7 个每月 200 美元的 Max 订阅（包括开源白送的两个），最后到底烧出了什么？说实话，我自己也已经数不过来了。

上一篇《[Codex Reset 狂欢结束，免费的鸡蛋没了](/ai/codex-reset-end/)》发出去以后，我说下一篇会专门盘点产出。不过这两天 Tibo 连续 Reset 两次，老冯又开始蹬车，这篇就搁置了。随便找了两个项目发布公告糊弄一下，今天额度差不多又快烧完了，也就不急了，补上这篇。

我让 Codex 扫了一下最近两三个月的 Token 用量，累计超过千亿 Token，而且我一律只用顶级模型最高强度。当然，单纯数豆子没有任何意义。真正有意义的是：这些词元最后有没有变成代码、软件包、文档、发布版本、可以交付的产品，或沉淀下来的资产？

---

## 先说结论

这一个多月里，老冯和 AI Agent 主要干了这么几类事情：

- 正式发布 Silo，目前是最活跃的 MinIO 社区分支。
- 发布 Pigsty 4.4/4.5，新增 Kafka、MySQL 模块支持；MinIO 支持新分支 Silo 与 RustFS，Redis 支持 Valkey 分支，还有试点的 ClickHouse 与 K3s 支持。
- 扩展生态：把 PostgreSQL 扩展包数量提升到 572 个，收录 2,200+ PG 扩展的元数据与双语文档，建设 PGEXT.CLOUD 网站，成为最大最全的 PG 扩展目录。
- 接手维护 12 款 PostgreSQL 内核分支在 16 个 Linux 平台组合上的构建分发。重做将近 100 款可观测性生态软件的 RPM/DEB 打包。维持 PostgreSQL.org 新闻同步、技术日报、双语文档、博客文章和大量日常 issue、PR、打包维护。这个就懒得说了。
- 新项目：Boar，Pigsty 的图形化管控平台。
- 新项目：SOW，Pigsty 使用的 APT/DNF 企业级制品仓库管理器。
- 新项目：OINK，一个专门针对工程文档优化的 Hugo 文档主题。
- 新项目：go-patroni，用 Go 重写了 PG 高可用组件 Patroni，发布了客户端 SDK。
- 新项目：snort，用 Go 强化改进了 pg_exporter，现在一个组件就可以收集 PG 全部指标与日志。
- 可视化：Pigsty 数字孪生、大盘与 Grafana 面板插件。
- 可视化：Pigsty 可交互主板模型。
- 新项目：一个 macOS 原生 App——CapsLock Enhancement 键盘魔改应用。
- 翻译：DDIA v2 中文翻译全本校对交付。
- 写作：《PG 三十六计》，AI 生成全书初稿。
- 网站：上面所有这些项目，基本都有使用 OINK 框架的配套网站和文档。

上面的东西都已经完工或者基本接近完工，当然有一些还没来得及发布，比如 Pigsty v4.5 就会在本周发布。RustFS 集成做过，但将在 Pigsty v5 再发布；K3s 与 ClickHouse 目前还是私有 Beta 模块，并没有成为 Pigsty 的正式部署模块；Boar 和 CapsLock 也还在蹬车进行时。但其他这些东西，你都能看到公开的产出了。

下面简单过一下吧。

---

## Silo：从 Fork 到一整套产品

这一个月里，最像“凭空造出一个新产品”的项目，还是 [Silo](https://silo.pgsty.com/zh/)（[GitHub](https://github.com/pgsty/silo)）。MinIO 社区版事实上停止维护以后，老冯接手做了这个 fork。到了 8 月，它已经不再只是“修几个 bug + 打包的 MinIO 分支”，而成为了一个独立的开源项目。

目前，Silo 的 GitHub 仓库已经有约 **2,200 stars**，[Docker Hub 镜像](https://hub.docker.com/r/pgsty/minio)超过 **52 万次 pull**。从公开可见的数据看，它已经是 MinIO 社区 fork 中最活跃、跑得最前面的一个。

这件事我在《[**MinIO 已死，Silo 长存**](/db/long-live-silo/)》里有更详细的记录。在当下，一个人通过合理利用 Agent，可以接下 MinIO 这种由无数人耗资 N 亿美元、开发十年的顶级开源项目，已经成为活生生的例子。老冯已经笑晕在厕所。

[![Silo 项目主页](silo-home.webp)](https://silo.pgsty.com/zh/)

[![Silo 对象存储控制台](silo-console.webp)](https://silo.pgsty.com/zh/)

---

## Pigsty：发行版这台大机器

老冯的日常基础工作，本来就包含一个巨大的 PostgreSQL 发行版 [Pigsty](https://pigsty.cc/)。它不是一个单独的软件，而是一整套开箱即用的 PostgreSQL 发行版：内核、扩展、备份、高可用、监控、服务治理、软件仓库和大量外围组件，全都要在 16 个 Linux 发行版大版本与 5 个活跃的 PG 大版本上工作。

[![Pigsty 项目主页](pigsty-home.webp)](https://pigsty.cc/)

v4.5 有很多新东西。我们有个客户想要在 Pigsty 里使用 Kafka。我想了一下，AI Engineering 了两天，就把 Kafka 支持加了进去：支持 Apache Kafka 4.1+ 的动态 KRaft 集群，既能部署单机，也能部署多节点。

既然 Kafka 做了，我也顺手一不做二不休把 MySQL 给做进来了，另外把 MySQL 8.4 LTS 单机与三节点 InnoDB Cluster、MySQL Router、TLS、XtraBackup 和监控面板放进 Pigsty 的管理体系里。

此外，Redis 模块现在可以选择 BSD 协议的 Redis 7.2，也可以选择 Valkey 9.1；MinIO 模块则可以在原生 MinIO、老冯自己的 Silo 与 RustFS 之间切换。这类“引擎插槽”看上去只是多了一个参数，背后却涉及不少东西。

冯王在全平台打包构建 Valkey 的过程中，还发现了 Valkey 包的一个 bug。Debian 和 Valkey 官方的 DEB 包全部翻车。我也给他们提了 issue，修了这个问题，并写了篇文章记录这件事：《[Valkey 上游没有的 Bug，为何出现在官方包里？](/db/valkey-bug/)》。

当然，Kafka 和 MySQL 严格来说还是试点模块；另外还顺手做了 K8s 和 K3s 两个模块。如此一来，Pigsty 已经不再是一个 PostgreSQL 数据库发行版，而是一套开源数据库基础设施 PaaS。你可以拥有 PG、MinIO、Redis、MySQL、Kafka、DuckDB、Victoria 监控全家桶、ClickHouse，以及 Kubernetes……

---

## PGEXT.CLOUD：扩展生态

在 PG 扩展生态里，老冯发布了新版本的 [PGEXT.CLOUD](https://pgext.cloud/zh/)。

如果说扩展是 PG 的精髓，那么 PGEXT.CLOUD 绝对是 PG 扩展世界的 No. 1 目录与仓库。PGEXT 收录的扩展数量达到了史无前例的 2,239 个，而且对于其中质量好、有实用价值的项目，提供了开箱即用的 RPM/DEB 二进制包。

[![PGEXT.CLOUD 扩展目录](pgext-catalog.webp)](https://pgext.cloud/zh/)

可以这么理解：PG 官方仓库提供 92 组扩展包，老冯在 PG 官方基础上额外提供 340 组。而且还修复了 PG 官方扩展的各种组合遗漏与缺陷，实现了一个壮举——在 16 个 Linux 平台、5 个 PG 大版本的构建矩阵中，实现 32,240 个构建组合零遗漏、全覆盖。

[![PG 扩展全平台构建矩阵](pgext-build-matrix.webp)](https://pgext.cloud/zh/)

[![PGEXT.CLOUD 软件包与下载](pgext-packages.webp)](https://pgext.cloud/zh/)

---

## Boar：Pigsty 管控平台

有很多用户一直想在 Pigsty 里面有一个图形化的管理工具，我一直懒得做，主要也是没那个时间捣鼓这些东西。

不过现在有了无限 Token，这事也就可以提上日程了。这个项目还没正式发布，但大体上可以理解为 Grafana、ClusterControl、pgAdmin，还有其他各种控制台、控制面板功能的集合。

![Boar 图形化管控平台](boar-console.webp)

没发布也没啥好说的，看看里面一个小组件吧：Pigsty 数字孪生（[在线演示](https://pgsty.github.io/sim/)／[GitHub](https://github.com/pgsty/sim)）。

[![Pigsty 数字孪生动画](pigsty-sim.gif)](https://pgsty.github.io/sim/)

![Pigsty 可交互主板模型](pigsty-board.webp)

---

## SOW：仓库管理器

[SOW 项目网站](https://sow.pgsty.com/zh/)已经上线，[昨天也专门写了文章介绍这个项目](/db/sow/)，这里就不展开了。这个东西的最终目标是重写 APT、DNF、reprepro、createrepo_c 和 aptly。外行看热闹，内行看门道。跨发行版的企业级分发与仓库制品管理，在开源世界还是一个空白生态位。做好了完全可以专门商业化成一个服务——类似 PackageCloud、Copr 仓库之类的。

说白了，就是 Pigsty 要搞企业级制品仓库，需要用到这个，就自己做了一个。

[![SOW 软件仓库管理器主页](sow-home.webp)](https://sow.pgsty.com/zh/)

---

## OINK：文档主题

[OINK 项目网站](https://oink.pgsty.com/zh/)已经上线，前几天也写过文章介绍：《[OINK：文档框架这件事，折腾了六年，终于靠 Codex 毕业了](/db/oink-release/)》。这是个从 Google 的 Docsy 文档框架二次定制而来的衍生主题。也是因为我们这次有大量新的项目要发布，每一个都要有配套的文档，实在不想从零开始做一些重复工作，就把这些东西都沉淀成了一个文档框架。基本上是整合了 Docsy、Hextra、Nextra、Fumadocs 众家所长。目前我自己的网站基本都已经搬上去了。

[![OINK 文档主题主页](oink-home.webp)](https://oink.pgsty.com/zh/)

下面全都是样例站点：

- [pgsty.com](https://pgsty.com/)、[pigsty.cc](https://pigsty.cc/)、[pigsty.io](https://pigsty.io/)
- [silo.pgsty.com](https://silo.pgsty.com/)、[oink.pgsty.com](https://oink.pgsty.com/)
- [sow.pgsty.com](https://sow.pgsty.com/)、[pig.pgsty.com](https://pig.pgsty.com/)、[exp.pgsty.com](https://exp.pgsty.com/)

---

## go-patroni

用 Rust 重写 PostgreSQL 可能是吃饱撑的，但是用 Go 重写 Patroni 这样的生态组件，我认为还是有不少收益的。当然，步子迈太大容易扯到蛋。虽然重写完了，目前我也只先把 [go-patroni](https://github.com/pgsty/go-patroni) 客户端部分发布出来。

因为 Boar 管理平台和 pig 命令行工具正好需要对接 Patroni，所以这么一个公共基础包先开源出来了。而且这个 [SDK](https://github.com/pgsty/go-patroni) 还提供一个完整的用 Go 写的 patronictl 命令行工具。

[![go-patroni 客户端 SDK 与文档](go-patroni.webp)](https://github.com/pgsty/go-patroni)

---

## snort

原本 PG 生态有很多组件，每个组件都有自己的监控工具，整个架构变得比较复杂。所以我一直在考虑一个问题：能不能用一个监控组件，把所有 PG 相关组件的监控指标和日志都采集好、处理好，统一丢到 Victoria 平台上去？这就是 [snort／PG Exporter](https://exp.pgsty.com/zh/) 这一轮强化的目标。

现在这件事已经实现了，大概会在 Pigsty 5.0 版本实装。

[![snort 与 PG Exporter 项目主页](snort-pg-exporter.webp)](https://exp.pgsty.com/zh/)

---

## CapsLock Enhancement

这个是老冯十几年前写的开源项目 [CapsLock Enhancement](https://capslock.vonng.com/zh/) 的第二春。简单来说，就是通过把键盘上的大写锁定键 CapsLock 转换成一个新的修饰键，从而给你带来最多 16 个完整的新控制平面，让你用键盘高效地完成各种操作。不夸张地说，俺操作电脑的速度，在这个软件和十年肌肉记忆的帮助下，可以提升 10 倍左右。

[![CapsLock Enhancement 的由来与用户反馈](capslock-history.webp)](https://capslock.vonng.com/zh/)

当然，这个十年前的形态是基于 Karabiner 这个开源软件的一份[配置文档](https://github.com/Vonng/Capslock)。后来也有不少人借鉴参考，还有做成商业软件去卖的，我也懒得去折腾。不过现在既然有富余 Token 了，我也不介意自己做一个 macOS 原生 App 玩一玩。这个还没有正式发布，这两天还在烧。

大体上你可以把它理解为 Karabiner 改键，加上防休眠、窗口管理、剪贴板、应用启动器、切换器之类的小功能，完整整合成的一个东西。这也正好解决了我自己不想装一些鸡零狗碎小软件的痛点。

[![CapsLock Enhancement 原生 macOS 应用](capslock-app.webp)](https://capslock.vonng.com/zh/)

---

## AI 翻译 DDIA v2

《设计数据密集型应用》这本书的第二版已经出来了。年初的时候，我用 5.3 翻译过一版，质量凑合能看。现在我用 5.6、SoMax 和 Fable，参照第一版的风格重新校正了一版。这一版我认为就跟人翻译的差不多了，目前[这个新版本](https://ddia.vonng.com/)也已经发布了。

[![《设计数据密集型应用》第二版中文翻译](ddia-v2.webp)](https://ddia.vonng.com/)

翻译这个行当确确实实是凉透了，老冯都懒得说自己翻译了多少文档了：PG 官方文档、PG 官方网站，还有 2,200 多个扩展的中文文档翻译。每次我有 Token 要到期了、用不完了，我就随便找一个项目，把它的文档翻译掉。

当然，除了翻译文档，你也可以拿来写书。比如说，老冯之前挖了个坑——[《PG 三十六计》](https://pg36g.vonng.com/)，一直没时间写，反正我先让 AI 写了一版。但既然是 AI 写的，我也不好意思去宣传发布，到时候人工校审之后，再正式发布吧。

[![《PG 三十六计》初稿](pg36.webp)](https://pg36g.vonng.com/)

---

## 小结

上面是最近一个月老冯干的一些大活。其实越是大的活，可能看上去越是不起眼。就像是你把 PG 生态里面几万个构建给完整补完，这事轻描淡写的一句话，但这意味着十几万个制品的 QA。

再比如接盘 MinIO 这样的顶级开源项目，rebranding 的工作量非常大：还要建设一整个配套的文档站、重新设计并交付控制台，以及进行完整的 QA 测试。说起来轻描淡写，实际上事儿还真的挺多。

但老实说，老冯虽然嘴上说脚踏车蹬得快冒烟了，实际上却还是比较清闲的。7 个订阅说多不多，一天平均能蹬掉 1.5 到 2 个。每周重置的话，7 个还不够用嘞，纯粹靠 Reset 和存下来的重置撑着。而且，Token 消耗的主力有些是那种一跑就一两天、四五天的大型工程。我人工花个两三个小时调研、出好 PRD，剩下的也不需要我管。

小型任务可能跑个二三十分钟，我需要验收一下。中间我就可以刷刷短剧、看看小说、上网冲浪什么的，其实还是比较闲的。要不是这么闲得慌，我也不会去做 CapsLock 改进、macOS 原生 App、文档主页站这些跟主业八竿子打不着的东西。

当然，作为 OPC，老冯还有其他很多事情：合同、法务、商务跟进、咨询答疑，折腾域名、VPS、网站、仓库；还有个公众号要写文章，还要在 X 和 LinkedIn 上宣传。其实事也挺多的，总能填满这些空档。

所以最近老有人说，这个文章怎么开始带 AI 味儿了？那也没办法啊，事情多就没空写了呗，只能是我口述一下观点，让 AI 代笔，我都没时间润色了。

BTW：就在本文发布时，本号关注人数到了 61,000。

![公众号关注人数达到 61,000](wechat-61000.webp)

所以你要是问我 OPC，甚至是一人独角兽是不是真的成立，老冯自己就是活生生的例子：一家一人公司，靠企业级 PG 发行版稳定盈利。随便做一单就够我买 AI 订阅，把我活活累死。一个人指挥一堆 Agent，搞俩头部大型开源项目（Debian/Nginx 级），还能有余力折腾各种花活，我是很满意现在这种状态。

不过我个人还是比较克制的，做的都是些跟主业有关系，或者已经攒了很久的需求。我的朋友蒋老板则是天马行空。他指挥 Codex 用 Rust 重写了三个数据库，最近又开始琢磨编程语言和操作系统了，一直在这些没什么用的东西上烧 Token，纯粹就是开心、找乐子。下次可以专门写一篇聊一聊。
