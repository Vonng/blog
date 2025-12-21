---
title: "微服务是不是个蠢主意？"
date: 2023-05-07
authors: [dhh]
origin: "https://world.hey.com/dhh/microservices-are-a-bad-idea-7a8dbddc"
summary: >
  连SOA典范亚马逊自己都觉得微服务和Serverless拉胯了。Prime Video团队放弃微服务改用单体架构，运营成本节省了惊人的90%。微服务就像塞壬歌声一样诱惑你为系统添加毫无必要的复杂度。
series: ["正本清源"]
tags: [架构设计, 微服务, Serverless, 技术评论, 翻译]
---

亚马逊的Prime Video团队发表了一篇非常引人注目的案例研究[2] ，讲述了他们为什么放弃了微服务与Serverless架构而改用单体架构。这一举措让他们在运营成本上节省了惊人的 90%，还简化了系统复杂度，堪称一个巨大的胜利。

但除了赞扬他们的明智之举之外，我认为这里还有一个重要洞察适用于我们整个行业：

> “我们最初设计的解决方案是：使用Serverless组件的分布式系统架构… 理论上这个架构可以让我们独立伸缩扩展每个服务组件。然而，我们使用某些组件的方式导致我们在大约5%的预期负载时，就遇到了硬性的伸缩限制。”

“**理论上的**” —— 这是对近年来在科技行业肆虐的微服务狂热做的精辟概括。现在纸上谈兵的理论终于有了真实世界的结论：在实践中，微服务的理念就像塞壬歌声一样诱惑着你，为系统添加毫无必要的复杂度，而 Serverless 只会让事情更糟糕。

这个故事最搞笑的地方是：亚马逊自己就是面向服务架构 / SOA 的最初典范与原始代言人。在微服务流行之前，这种组织模式还是很合理的：在一个疯狂的规模下，公司内部通信使用 API 调用的模式，是能吊打协调跨团队会议的模式的。

SOA 在亚马逊的规模下很有意义，没有任何一个团队能够知道或理解 驾驶这么一艘巨无霸邮轮所需的方方面面，而让团队之间通过公开发布的 API 进行协作简直是神来之笔。

但正如很多“好主意”一样，**这种模式在脱离了原本的场景用在其他地方后，就开始变得极为有害了**：特别是塞进单一应用架构内部时 —— 而人们就是这么搞微服务的。

![](microservice-bad-idea-1.jpeg)

从很多层面上来说，微服务是一种僵尸架构，是一种顽强的思想病毒：从 J2EE 的黑暗时代（Remote Server Beans，有人听说过吗），一直到 WS-Deathstar[3] 死星式的胡言乱语，再到现在微服务与 Serverless 的形式，它一直在吞噬大脑，消磨人们的智力。

不过这第三波浪潮总算是到顶了，我在 2016 年就写过一首关于 “宏伟的单体应用[4]” 的赞歌。Kubernetes 背后的意见领袖高塔先生也在 2020年 单体才是未来[5] 一文中表达过这一点：

> “我们要打破单体应用，找到先前从未有过的工程纪律… 现在人们从编写垃圾代码变成打造垃圾平台与基础设施。
>
> 人们沉迷于这些与时髦术语绑定的热钱与炒作，因为微服务带来了大量的新开销，招聘机会与工作岗位，唯独对于解决他们的问题来说实际上并没有必要。“

![](microservice-bad-idea-2.png)

没错，当你拥有一个连贯的单一团队与单体应用程序时，用网络调用和服务拆分取代方法调用与模块切分，在几乎所有情况下都是一个无比疯狂的想法。

我很高兴在记忆中已经是第三次击退这种僵尸狂潮一样的蠢主意了。但我们必须保持警惕，因为我们早晚还得继续这么干：有些山炮想法无论弄死多少次都会卷土重来。你能做的就是当它们借尸还魂的时候及时认出来，用文章霰弹枪给他喷个稀巴烂。


> 有效的复杂系统总是从简单的系统演化而来。反之亦然：从零设计的复杂系统没一个能有效工作的。
>
> —— 约翰・加尔，Systemantics（1975）


本文作者 DHH， Ruby on Rails 作者，37signals CTO，译者 Vonng。

原题为  Even Amazon can't make sense of serverless or microservices[1] 。即《亚马逊自个都觉得微服务和Serverless扯淡了》

[![](featured.jpg)](https://mp.weixin.qq.com/s/mEmz8pviahEAWy1-SA8vcg)


### References

`[1]` Even Amazon can't make sense of serverless or microservices: *https://world.hey.com/dhh/even-amazon-can-t-make-sense-of-serverless-or-microservices-59625580*
`[2]` 引人注目的案例研究: *https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90*
`[3]` WS-Deathstar: *https://www.flickr.com/photos/psd/1428661128/*
`[4]` 宏伟的单体应用: *https://m.signalvnoise.com/the-majestic-monolith/*
`[5]` 单体才是未来: *https://changelog.com/posts/monoliths-are-the-future*