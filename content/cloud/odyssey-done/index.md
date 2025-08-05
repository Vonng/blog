---
title: DHH：下云省下千万美元，比预想的还要多！
date: 2023-07-07
hero: /hero/odyssey.jpg
author: |
  [DHH](https://world.hey.com/dhh) | 译：[冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [微信公众号](https://mp.weixin.qq.com/s/mknFXO5DSfxw7st8hhxjBQ)
summary: >
  DHH 将他们的七个云上应用从 AWS 迁移到自己的硬件上，2024年是第一个完全实现节省的年份。他们欣喜地发现，节省的费用比最初估计的还要多。
tags: [下云,DHH]
---


> 作者：DHH，《[Our cloud-exit savings will now top ten million over five years](https://world.hey.com/dhh/our-cloud-exit-savings-will-now-top-ten-million-over-five-years-c7d9b5bd)》

去年夏天，我们[完成了下云工作](https://world.hey.com/dhh/we-have-left-the-cloud-251760fb)，将包括 [HEY](https://hey.com/) 在内的七个云上应用从 AWS 迁移到我们自己的硬件上来。但直到年底，我们的所有长期合同才结束，所以2024年是第一个完全实现节省的年份。我们欣喜地发现，节省的费用比最初估计的还要多。

在2024年，我们已将云账单从每年 **320万美元 降至 130万美元，每年节省了近200万美元！** 之所以比我们最初[预估的五年节省700万美元](https://world.hey.com/dhh/we-stand-to-save-7m-over-five-years-from-our-cloud-exit-53996caa)还要多，是因为我们成功地将所有新硬件安装在我们现有的数据中心的机架上和电力限制内。

购买这些新的 [戴尔硬件](https://world.hey.com/dhh/the-hardware-we-need-for-our-cloud-exit-has-arrived-99d66966) 花费了约70万美元，但在2023年期间，随着长期合同逐步到期，我们已完全收回成本。想想看，这些设备我们预计可以使用五年，甚至七年！所有费用都由2023年下半年积累的节省来支付，真是太棒了！

但好事还在后头。**目前我们仍在云服务上花费的130万美元，全部花在了 AWS S3 上**。虽然我们之前的云计算和托管数据库/搜索服务都是预付一年的合同，但我们的文件存储被锁定在一个从 2021 年开始的，长达四年的合同中，所以我们计划中，完整下掉 S3 要到明年夏天了。

我们现在在 S3 中存储了近 **10 PB** 的数据，包括 Basecamp 和 HEY 等的重要客户文件，并通过不同区域进行冗余存储。我们采用混合存储类别，权衡了可靠性、访问性和成本。但即便有长期合同的折扣，保存这些数据每年仍需一百多万美元！

明年夏天下云后，我们将迁移到双数据中心的 [Pure Storage](https://www.purestorage.com/) 系统，总容量为18 PB。初始硬件成本约等于一年使用 AWS S3 的费用。但得益于 Pure 闪存阵列的高密度和高能效，我们可以将这些设备安装在现有的数据中心机架内。因此，后续成本只是一些常规的服务合同，**我们预计在五年内再节省四百万美元**。

因此，我们下云预计的总收益将在五年内超过一千万美元！**同时，我们还获得了更快的算力和更大的存储空间**。

当然，云上和本地自建的对比从来不是完全对等的。如果您完全在云上，而没有现成的数据中心机架，那么你也需要支付租赁费用 —— （但相比云服务的费用，您可能会惊讶于其便宜程度！）。但也别忘了对于我们的下云案例来说，节约估算的目标也是在不断变化的 —— 因为随着 Basecamp 和 HEY 的业务持续增长，我们需要更多的硬件和存储。

但令人瞩目的是，我们通过下云获得了如此巨大省钱收益。我们已经下云一年多了，然而团队规模仍然保持不变。当我们宣布下云时，有人猜测可能会有大量的额外工作，需要我们扩大团队规模才行，但实际上并没有。我们在 [下云 FAQ ](https://world.hey.com/dhh/the-big-cloud-exit-faq-20274010) 中的回复依然成立。

不过，这仍然需要付出努力！在两个数据中心（很快还会在海外增加至少一个）上运营像 [Basecamp](https://basecamp.com/) 和 HEY 这样的大型应用，需要一支专注的团队。总有工作要做，维护所有的应用、数据库、虚拟机，偶尔还需要请求更换出现警示灯的机器的电源或硬盘（但这些由 [Deft](https://deft.com/) 的专业服务处理） —— 而大部分工作在云上也需要我们自己来做！

自从我们最初宣布[下云计划](https://world.hey.com/dhh/why-we-re-leaving-the-cloud-654b47e0)以来，业界对同样的下云举措 [兴趣激增](https://x.com/MichaelDell/status/1780672823167742135)。2010 到 2020 早期的口号 —— “全部上云、所有东西上云、一直在云端！” —— 似乎总算达峰到头了，谢天谢地！

当然，云服务仍然有其价值。尤其是在初创阶段 —— 当您甚至不需要一整台服务器，或者不确定公司能否撑到年底。或者当您需要处理巨大的负载波动时，这也是亚马逊创建 AWS 的初衷。

但一旦云账单开始飙升，我认为您有责任为自己、投资者和基本商业常识着想，至少做一下计算。我们花了多少钱？购买这些设备而非租用需要多少成本？我们能否尝试使用 [Kamal](https://kamal-deploy.org/) 或类似工具，将部分系统迁移到自有硬件上？这些问题的答案可能带来惊人的降本增效。

在 [37signals](https://37signals.com/)，我们期待在明年夏天彻底删除我们的 AWS 账户，我们仍然感谢在使用该云平台期间得到的服务和经验。显而易见，亚马逊为何能在云领域保持领先。我也很高兴现在从 S3 中迁出数据是完全免费的，如果您决定永久离开该平台。这会让成本计算更加有利。再见，感谢你们的一切！


--------

## 参考阅读

以下是 DHH 下云过程的完整记录与答疑。

- [是时候放弃云计算了吗？](https://mp.weixin.qq.com/s/CicctyvV1xk5B-AsKfzPjw)
- [下云奥德赛](https://mp.weixin.qq.com/s/H2S3TV-AsqS43A5Hh-XMhQ)
- [半年下云省千万：DHH下云FAQ答疑](https://mp.weixin.qq.com/s/xaa079P4DRCz0hzNovGoOA)
- [先优化碳基BIO核，再优化硅基CPU核](https://mp.weixin.qq.com/s/Yxyir8kjRDUZwkkE_dscZQ)
- [单租户时代：SaaS范式转移](https://mp.weixin.qq.com/s/jKv9l_ro6rWei4QnXck-zw)
- [拒绝用复杂度自慰，下云也保稳定运行](https://mp.weixin.qq.com/s/yIVal-9U6_TXX-dZpVtjBg)


--------

## 老冯评论

作为下云倡导者，我很欣慰地看到 DHH 在下云过程中取得的巨大成功。世界总是会奖赏那些有智慧发现问题，且有勇气采取行动的领导者。

在过去两年里，云炒作达峰下坡，而下云运动却在蓬勃发展 —— 根据 Barclays 2024 上半年进行的 CIO 调查中，计划将负载迁回到本地部署/私有云上的 CIO 占比，从前几年的 50% - 60 飙升到 83%。下云，作为一种切实的降本增效选项，已经完全进入主流视野，并开始产生巨大的现实影响。

![dell.png](dell.png)

> Dell 老板：选择搬回自建/私有云的CIO比例

在我的 《云计算泥石流》 系列专栏中，我已经深入剖析过云资源的成本，介绍过云背后的商业模式，并提供了下云替代的切实可行路径。
我自己也在过去两年中帮助过不少企业从云上下来 —— 通过解决了他们下云关键卡点的数据库服务自建问题。


下云可以带来的巨大节省收益，以 DHH 没迁移完的 S3 对象存储服务为例，每年 130 万美元（约合 900 万人民币）—— 
通过一次性投入一年的 S3 费用，就能下到一个容量近乎翻倍的本体 Pure Storage 系统，也就是说，第一年完成回本，后面四到六年每一年都相当于白赚。

这里的帐很好算，之前我们核算过自建对象存储的 TCO（假设使用60盘位 12PB 存储机型，世纪互联托管，三副本），约为 200 - 300 ¥/TB （买断价格，用五到七年） —— 那么 10 PB 的存储也不过是 35 万¥ 一次性投入。
相比之下，AWS / 阿里云这样的云厂商对象存储则要 110 - 170 ¥/TB （**每月**，这还只是存储空间部分，没算请求量、流量费、取回费），与自建的成本拉开了两个数量级。 

是的，自建对象存储可以实现相比云对象存储两个数量级，几十倍的成本节省。作为一个自建过 25 PB MinIO 存储的人来说，我保证这些成本数字的真实性。

作为一个简单的证明，服务器托管服务商 Hentzer 提供的对象存储价格是 AWS 的 1/51 ……，他们并不需要什么高科技黑魔法，只要把硬件装上 Ceph/Minio 这样的开源软件加个GUI，真诚地卖给客户就可以做到这个价格，还能确保自己有不错的毛利。

![hetzner-s3.png](hetzner-s3.png)

> Hentzer 提供价格是 AWS S3 1/50 的兼容对象存储服务

不仅仅是对象存储，云上的带宽，流量，算力，存储，都贵的离谱 —— 如果你不是那种几个凑单1c羊毛虚拟机就能打发的用户，你真的应该好好算一算帐。
这里的数学计算并不复杂，任何有商业常识的人只要拥有这里的信息都会产生这样的想法 —— 我为云上的服务支付几倍到几十倍的溢价，**究竟买到的是什么东西？**

例如，DHH 在 Rails World 大会上的演讲就抛出了这个问题，用同样的价格，他在 Hetzner 上可以租到强大得多得多的专属服务器：

![dhh1.png](dhh1.png)

![hetzner.png](hetzner.png)

之前阻止用户这样做的主要阻碍是数据库，k8s这样的[**PaaS自建太难**](/cloud/finops)，但现在已经有无数的 PaaS 专门店供应商能比云厂商提供更好的解决方案了。（比如MinIO之于S3，[**Pigsty**](https://pigsty.io) 之于 RDS， SealOS 之于 K8S，AutoMQ 之于 Kafka，…… ）

实际上，越来越多的云厂商也开始意识到这一点，例如 DigitalOcean，Hentzer，Linode，Cloudflare 都开始推出 “诚实定价” ，物美价廉的云服务产品。
用户可以在享受到云上各种便利的前提下，使用几十分之一的成本直接从这些 “平价云” 购买相应的资源。

经典云厂商也开始 FOMO ，他们没法直接降价放弃手上的既得利益，但也对新一代云厂商的平价竞争感到焦虑，想参与其中。例如，最近新冒出来的廉价 “阿爪云” ClawCloud，就是某个头部云厂商的小号，跑出来和搬瓦工，Linode 抢生意。


我相信在这样的竞争刺激下，云计算市场的格局不久便会出现令人激动的变化。会有越来越多的用户识破云上炒作，并明智而审慎地花出自己的 IT 预算。



--------

## Our cloud-exit savings will now top ten million over five years

We [finished](https://world.hey.com/dhh/we-have-left-the-cloud-251760fb) pulling seven cloud apps, including [HEY](https://hey.com/), out of AWS and onto our own hardware last summer. But it took until the end of that year for all the long-term contract commitments to end, so 2024 has been the first clean year of savings, and we've been pleasantly surprised that they've been even better than originally estimated.



For 2024, we've brought the cloud bill down from the original $3.2 million/year run rate to $1.3 million. That's a saving of almost two million dollars per year for our setup! The reason it's more than [our original estimate of $7 million over five years](https://world.hey.com/dhh/we-stand-to-save-7m-over-five-years-from-our-cloud-exit-53996caa) is that we got away with putting all the new hardware into our existing data center racks and power limits.



The expenditure on [all that new Dell hardware](https://world.hey.com/dhh/the-hardware-we-need-for-our-cloud-exit-has-arrived-99d66966) – about $700,000 in the end – was also entirely recouped during 2023 while the long-term commitments slowly rolled off. Think about that for a second. This is gear we expect to use for the next five, maybe even seven years! All paid off from savings accrued during the second half of 2023. Pretty sweet!



But it's about to get sweeter still. The remaining $1.3 million we still spend on cloud services is all from AWS S3. While all our former cloud compute and managed database/search services were on one-year committed contracts, our file storage has been locked into a four(!!)-year contract since 2021, which doesn't expire until next summer. So that's when we plan to be out.


We store almost 10 petabytes of data in S3 now. That includes a lot of super critical customer files, like for Basecamp and HEY, stored in duplicate via separate regions. We use a mixture of storage classes to get an optimized solution that weighs reliability, access, and cost. But it's still well over a million dollars to keep all this data there (and that's after the big long-term commitment discounts!).



When we move out next summer, we'll be moving to a dual-DC [Pure Storage](https://www.purestorage.com/) setup, with a combined 18 petabytes of capacity. This setup will cost about the same as a year's worth of AWS S3 for the initial hardware. But thanks to the incredible density and power efficiency of the Pure flash arrays, we can also fit these within our existing data center racks. So ongoing costs are going to be some modest service contracts, and we expect to save another four million dollars over five years.



This brings our total projected savings from the combined cloud exit to well over ten million dollars over five years! While getting faster computers and much more storage.



Now, as with all things cloud vs on-prem, it's never fully apples-to-apples. If you're entirely in the cloud, and have no existing data center racks, you'll pay to rent those as well (but you'll probably be shocked at how cheap it is compared to the cloud!). And even for our savings estimates, the target keeps moving as we require more hardware and more storage as Basecamp and HEY continues to grow over the years.


But it's still remarkable that we're able to reap savings of this magnitude from leaving the cloud. We've been out for just over a year now, and the team managing everything is still the same. There were no hidden dragons of additional workload associated with the exit that required us to balloon the team, as some spectators speculated when we announced it. All the answers in our [Big Cloud Exit FAQ](https://world.hey.com/dhh/the-big-cloud-exit-faq-20274010) continue to hold.



It's still work, though! Running apps the size of [Basecamp](https://basecamp.com/) and HEY across two data centers (and soon at least one more internationally!) requires a substantial and dedicated crew. There's always work to be done maintaining all these applications, databases, virtual machines, and yes, occasionally, even requesting a power supply or drive swap on a machine throwing a warming light (but [our white gloves at Deft](https://deft.com/) take care of that). But most of that work was something we had to do in the cloud as well!


Since we originally announced [our plans to leave the cloud](https://world.hey.com/dhh/why-we-re-leaving-the-cloud-654b47e0), there's been a [surge of interest](https://x.com/MichaelDell/status/1780672823167742135) in doing the same across the industry. The motto of the 2010s and early 2020s – all-cloud, everything, all the time – seems to finally have peaked. And thank heavens for that!


The cloud can still make a lot of sense, though. Especially in the very early days when you don't even need a whole computer or are unsure whether you'll still be in business by the end of the year. Or when you're dealing with enormous fluctuations in load, like what motivated Amazon to create AWS in the first place.


But as soon as the cloud bills start to become substantial, I think you owe it to yourself, your investors, and common business sense to at least do the math. How much are we spending? What would it cost to buy these computers instead of renting them? Could we try moving some part of the setup onto our own hardware, maybe using [Kamal](https://kamal-deploy.org/) or a similar tool? The potential savings from these answers can be shocking.

At [37signals](https://37signals.com/), we're looking forward to literally deleting our AWS account come this summer, but remain grateful for the service and the lessons we learned while using the platform. It's obvious why Amazon continues to lead in cloud. And I'm also grateful that it's [now entirely free to move your data out of S3](https://aws.amazon.com/blogs/aws/free-data-transfer-out-to-internet-when-moving-out-of-aws/), if you're leaving the platform for good. Makes the math even better. So long and thanks for all the fish!