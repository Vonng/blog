---
title: "云下高可用秘诀：拒绝复杂度自慰"
date: 2024-01-10
authors: ["dhh"]
origin: "https://world.hey.com/dhh/keeping-the-lights-on-while-leaving-the-cloud-be7c2d67"
summary: >
  程序员极易被复杂度所吸引，就像飞蛾扑火一样。系统架构图越复杂，智力自慰的快感就越大。坚决抵制这种行为，是下云可用性上成功的重要原因。
tags: [下云, DHH]
---


我们不需要Kubernetes大师或花哨的新数据库 —— 程序员极易被复杂度所吸引，就像飞蛾扑火一样。系统架构图越复杂，智力自慰的快感就越大。我们坚决抵制这种行为，是在云下可用性上成功的重要原因。

> 作者：**David Heinemeier Hansson**，网名DHH，37 Signal 联创与CTO，Ruby on Rails 作者，下云倡导者、实践者、领跑者。反击科技巨头垄断的先锋。[Hey博客](https://world.hey.com/dhh)
>
> 译者：**Vonng**，PIGSTY 创始人与CEO。[Pigsty](https://mp.weixin.qq.com/s/-E_-HZ7LvOze5lmzy3QbQA) 作者，PostgreSQL 专家/布道师。公众号《[非法加冯](https://mp.weixin.qq.com/s/p4Ys10ZdEDAuqNAiRmcnIQ)》主理人，云计算泥石流，数据库老司机。
>
> 本文翻译自 DHH [博客](https://world.hey.com/dhh/keeping-the-lights-on-while-leaving-the-cloud-be7c2d67)，


-----------

## 下云的同时确保系统稳定运行

> [*Keeping the lights on while leaving the cloud*](https://world.hey.com/dhh/keeping-the-lights-on-while-leaving-the-cloud-be7c2d67)

对 [37signals](https://37signals.com/) 的运维团队来说，2023年无疑是充满挑战的一年。我们把包括七大核心应用从云上迁移了下来，其中包括在云上诞生的电子邮件服务 [HEY](https://hey.com/) —— 它有着极为严苛的可用性要求，我们下云的过程不能影响这一承诺。幸运的是，我们确实做到了。2023年，HEY的可用时间达到了令人瞩目的 99.99%！

这一点非常重要，因为如果人们无法访问他们的电子邮件，他们可能会错过飞机登机，无法及时完成交易，或者无法获知医疗检测结果。我们非常重视这项责任，因而在这个需要彻底改变运行 HEY 运行方式的一年里，实现了这接近完美的四个九，成为了让我引以为傲的重要成就。

但不仅仅是 HEY 有这种细致运维待遇。在2023年，我们运营的所有主要应用可用性最低都达到了 **99.99%** 以上。这里包 Highrise、Backpack、Campfire 以及所有版本的 [Basecamp](https://basecamp.com/)。我们并非没有遇到任何问题 —— 而是靠团队迅速解决了所有问题，使全年的总停机时间没有超过 **0.01%**。

在云外能否确保应用可靠性和稳定性，没有一个应用能比 Basecamp 2 更能说明这个问题。这是我们从 2012 年到 2015 年销售的 Basecamp 版本，至今仍有数千用户，创造了数百万美元的收入。它多年来一直运行在我们自己的硬件上，现在已经是连续第二年实现了几乎难以置信的 **100%** 可用性 —— 2023年整整365天零停机，延续了2022年的辉煌。

我不会假装如此卓越的可用性是一件轻而易举的事情，因为事实并非如此。做到这一点绝非易事。我们拥有一支技艺精湛、敬业奉献的运维团队，他们为实现这一目标做出了巨大贡献，理应获得高度赞扬。但这也并非什么高深莫测的火箭科学！

Basecamp 2 连续两年实现100%可用性的魔法，以及其他所有应用达到99.99%可用性的成绩，相当一部分归功于**我们选择了简单枯燥、基础扎实的技术**。我们使用了 F5、Linux、KVM、Docker、MySQL、Redis、ElasticCache，当然还有 Ruby on Rails。我们的技术栈朴实无华，主要是复杂度很低 —— **我们并不需要 Kubernetes 大师或花哨的数据库与存储。大多数情况下，你也不会需要的。**



**但是程序员极易被复杂度所吸引，就像飞蛾扑火一样。系统架构图越复杂，智力自慰的快感就越大。我们坚决抵制这种行为的投入，才是在可用性上胜利的根本原因。**



这里我讨论的并不是运营 Netflix、Google 或 Amazon 所需的技术。在那种规模下，你确实会遇到真正的开拓性问题，没有现成的解决方案可供借鉴。但对于我们其他 99.99% 的人来说，效仿他们的想象与认知来建模自己的基础设施，是诱人但致命的塞壬歌声。

想要拥有良好的可用性，你需要的不是云，而是在冗余硬件上运行成熟的技术，并配置好备份，一如既往。



> 注：DHH 省下近千万美元的高昂云开销，本文翻译了DHH下云的最新进展。下云前情提要与完整过程请参考：《[下云奥德赛](https://mp.weixin.qq.com/s/H2S3TV-AsqS43A5Hh-XMhQ)》，《[是时候放弃云计算了吗](https://mp.weixin.qq.com/s/CicctyvV1xk5B-AsKfzPjw)》，以及《[DHH下云FAQ](https://mp.weixin.qq.com/s/xaa079P4DRCz0hzNovGoOA)》。


--------------

## 译者评论

DHH指出了维护良好可用性的最佳实践 —— **在冗余硬件上运行朴实无华、成熟基础的技术**。软件的大部分成本开销并不在最初的研发阶段，而是在持续的维护阶段。而**简单性**对于系统的可维护性至关重要。

有一些程序员出于**智力自慰（Intellectual Masturbation）**或**工作安全（Job Security）**的原因，会在架构设计中堆砌无谓的额外复杂度 —— 例如不管规模负载合适与否就[一股脑全上 Kubernetes](https://mp.weixin.qq.com/s/4a8Qy4O80xqsnytC4l9lRg)，或者使用胶水代码飞线串联起一堆花里胡哨的数据库。寻找“足够酷的“的东西来满足个人价值的需求，而不是考虑要解决问题是否真的需要这些屠龙术。

![](featured.jpg)

> 鲁布·戈德堡机械：“以极为繁复而迂回的方法去完成实际上或看起来可以容易做到事情” —— 一种通过复杂度进行智力自慰的行为。

复杂度会拖慢所有人的速度，并显著增加维护成本。在复杂的系统中进行变更，引入错误的风险也更大（例如《[从降本增笑到真的降本增效](https://mp.weixin.qq.com/s/FIOB_Oqefx1oez1iu7AGGg)》介绍的大故障）。因为复杂度导致维护困难时，预算和时间安排通常会超支。当开发人员难以理解系统时，隐藏的假设、无意的后果和意外的交互就更容易被忽略。降低复杂度能极大地提高软件的可维护性，因此**简单性**应该是构建系统的一个关键目标。

并不是所有公司都有 Google 那样的规模与场景，需要用宇宙战舰去解决他们特有的问题。裸机/虚机上的 PostgreSQL + Go/Ruby/Python 或者经典 LAMP 已经让无数公司一路干到上市了。切莫忘记，**为了不需要的规模而设计是白费功夫**，这属于**过早优化**的一种形式 —— 而这正是万恶之源。

以我亲身经历为例，在探探早中期的时候，几百万日活时的技术栈仍然非常朴素 —— 应用纯用 Go 写，数据库只用 PostgreSQL。在 250w TPS与 200TB 数据的量级下，**单一PostgreSQL选型**能稳定可靠地撑起业务：除了本职的OLTP，还在相当长的时间里兼任了缓存，OLAP，批处理，甚至消息队列的角色。最终一些兼职功能逐渐被**分拆**出去由专用组件负责，但那已经是近千万日活时的事了，而且事后来看其中一些新组件的必要性也存疑。

因此当我们在进行架构设计与评审时，不妨用复杂性的视角来进行额外的审视。更多关于复杂度的讨论，请参考下列文章：

[数据库应该放入K8S里吗？](https://mp.weixin.qq.com/s/4a8Qy4O80xqsnytC4l9lRg)

[从降本增笑到真的降本增效](https://mp.weixin.qq.com/s/FIOB_Oqefx1oez1iu7AGGg)

[把数据库放入Docker是一个好主意吗？](https://mp.weixin.qq.com/s/kFftay1IokBDqyMuArqOpg)

[微服务是不是个蠢主意？](https://mp.weixin.qq.com/s/mEmz8pviahEAWy1-SA8vcg)

[分布式数据库是伪需求吗？](https://mp.weixin.qq.com/s/-eaCoZR9Z5srQ-1YZm1QJA)

