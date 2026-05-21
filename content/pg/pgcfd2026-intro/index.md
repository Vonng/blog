---
title: "PGConf.Dev 2026 今天在温哥华开幕"
linkTitle: "PGConf.Dev 2026 开幕"
date: 2026-05-19
author: 冯若航
summary: >
  PGConf.Dev 2026 在温哥华开幕。今年恰逢 PostgreSQL 项目 30 周年，我也会在大会上分享 Extensions for Everyone。
tags: [PostgreSQL, PG生态, 会议]
---

温哥华时间 5 月 19 日，[PGConf.Dev 2026](https://2026.pgconf.dev/) 正式拉开序幕。今年的会场在 Simon Fraser University 市区校区，也就是 SFU Vancouver Harbour Centre，和第一届 PGConf.Dev 一样，还是在温哥华。

PGConf.Dev 是 PostgreSQL 全球开发者大会，前身是 PGCon。它是核心开发者、扩展作者、社区组织者一年一度最重要的聚会之一。今年又刚好赶上 **PostgreSQL 项目 30 周年**，社区围绕这个节点专门安排了不少活动。

今天的议程更偏社区、工作组和开放讨论；5 月 20 日、21 日两天，则是三个厅并行的正式 Session，从核心 Patch、查询优化、逻辑复制，一路聊到扩展、生态和社区。照例，老冯这两天还在赶 PPT 和演讲稿——希望能给到场的朋友留下点印象，别让大家在台下打瞌睡就好。


## 我的话题：Extensions for Everyone

这次我有一个正式演讲，题目是 **Extensions for Everyone**，安排在 **5 月 20 日（周三）16:00–16:25，Canfor 厅（1600）**。

主题不用绕弯子。作为一个常年在一线折腾 PostgreSQL 扩展分发的中国开发者，我想聊聊这几年看到的问题和踩过的坑：扩展生态当下面临的真实挑战是什么，分发为什么这么难，跨发行版打包到底卡在哪里，社区生态又可以往哪个方向再推一步。

Pigsty、PGEXT.CLOUD、`pig` CLI 这一路攒下来的经验，我会尽量系统地讲一遍。


## 中国厂商在这个舞台上

这次来参会的中国厂商，依然有老朋友瀚高 / IvorySQL。温哥华当地的 **Grant Zhou** 和 **Carry Huang** 都是老熟人了。瀚高 / IvorySQL 原本也有更多核心同学计划到场，不过后来部分行程受签证影响，没能如期成行。

这几次 PG 开发者大会里，瀚高和老冯可以说是平行参与这件事：

- **第一届大会**，大家都还只是参与者，主要是到现场感受氛围。
- **第二届大会**，我和 Grant 都抽中了一个 5 分钟的闪电演讲（Lightning Talk），算是第一次在这个场子里开口。
- **这一届大会**，我们俩都升级到了正式的 25 分钟 Session，而且还撞在同一个时间段，算是挺有意思的巧合。

所以，中国声音出现在这个舞台上，并不是一夜之间的事，而是一步一步走过来的。


## 两场来自中国的正式分享

这届大会里，当前官方日程上来自中国讲者的正式分享有两场，恰好覆盖了“产品/生态”和“社区桥梁”两个维度。

### Extensions for Everyone

**Ruohang Feng（老冯）**  
**5 月 20 日（周三）16:00–16:25，Canfor 厅（1600）**

我会从一个中国开发者的角度，分享 PostgreSQL 扩展分发与生态建设的一线观察。更具体地说，就是扩展如何从源码变成可安装、可升级、可运维的生产级软件包，以及这件事对 PostgreSQL 生态意味着什么。

### The Missing Link: Connecting Tens of Thousands of Chinese Users to the PostgreSQL Core

**Grant Zhou**  
**5 月 20 日（周三）16:00–16:25，Fletcher 厅（1900）**

Grant 要聊的是中国数以万计的 PostgreSQL 用户和全球核心社区之间那条“缺失的链路”：中国用户和贡献者如何更顺畅地接入上游社区，社区又该如何理解和回应这一边的需求。

这是一个长期被低估、但越来越重要的话题。

另外，瀚高架构师 **Chao Li（厉超）** 的议题 **Learning PostgreSQL Hacking Fast: Lessons and Mistakes from a Newcomer** 此前也已入选，原本计划分享自己从 PostgreSQL Beginner，到能够认真给上游提 Patch 的成长经历，以及这一路上踩过的坑和走过的弯路。

可惜因为签证没有及时批下来，这场最终没能成行，当前大会官网也已经不再列出这个议题。原本同一时间段的 Fletcher 厅（1900），现在替换成了 Masahiko Sawada 的 **Implementing DDL Deparsing and DDL Replication**；主题相近的新人贡献者成长分享，则是 Labatt 厅（1700）的 **My Journey into PostgreSQL Development**。


## 大会整体安排

这届大会的主题很丰富，节奏也比往届更紧凑一些：

- **5 月 19 日（周二）**：开幕日，主要是 Community Session、工作组讨论，以及一部分内部/闭门会议，比如 Committers Meeting、Security Team 等。今年特意把过去半天起步的大议题切成了更小颗粒度的环节，注册参会者可以挑感兴趣的加入。
- **5 月 20 日（周三）至 5 月 21 日（周四）**：两天主议程，三个厅并行，从核心 Patch、查询优化、逻辑复制，到 Extensions、生态、社区，覆盖面很广。
- **5 月 22 日（周五）**：经典的 Unconference 日，议程当天由参会者现场提议并投票产生。
- **周三晚上**：还有 **30 Years of PostgreSQL Retrospective**。Bruce Momjian、Tom Lane、Jan Wieck、Vadim Mikheev 等一众核心人物同台回顾 PostgreSQL 30 年。这种场子，错过就再难凑齐了。


大体就这些。这几天大会开始，估计也没太多空闲，但我会尽量把现场一些有意思的片段同步到这边来，包括话题、走廊里的对话，以及一些值得留下来的瞬间。

如果你也在温哥华，欢迎来 Canfor 厅找我——**5 月 20 日（周三）下午 4 点，扩展生态那场，咱们见。**

顺便一提，5 月 23 日之后，我准备自驾 Banff / Jasper，大概一两周。路线两年前已经蹚过一遍，算是轻车熟路。如果你也在附近，最近正好准备自驾，可以考虑搭伙一起走，哈哈。
