---
title: "Cloud Computing Mudslide: Deconstructing Public Cloud with Data"
hero: /hero/debris.jpg
date: 2023-07-08
author: |
  [Feng Ruohang](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [WeChat](https://mp.weixin.qq.com/s/eag0CqfUTeNPbIB6TZqFVg) 
summary: |
  Once upon a time, "going to cloud" was almost politically correct in tech circles, but few people use hard data to analyze the trade-offs involved. I'm willing to be this skeptic: let me use hard data and personal stories to explain the traps and value of public cloud rental models.
tags: [cloud-exit]
---

Once upon a time, "going to cloud" was almost politically correct in tech circles, but few people use hard data to analyze the trade-offs involved. I'm willing to be this skeptic: let me use hard data and personal stories to explain the traps and value of public cloud rental models - for your reference in this era of cost reduction and efficiency improvement.

[Cloud Exit Odyssey](/cloud/odyssey/)

[The End of FinOps is Cloud Exit](/cloud/finops/)

[Why Isn't Cloud Computing More Profitable Than Mining Sand?](/cloud/profit/)

[Are Cloud SLAs Just Placebos?](/cloud/sla/)

[Are Cloud Disks Pig-Killing Scams?](/cloud/ebs/)

[Are Cloud Databases Intelligence Tax?](/cloud/rds/)

[Paradigm Shift: From Cloud to Local-First](/cloud/paradigm/)

[Tencent Cloud CDN: From Getting Started to Giving Up](/cloud/cdn/)

[![](featured.png)](https://mp.weixin.qq.com/s/eag0CqfUTeNPbIB6TZqFVg)

-------------

## Preface

Economic downturn makes cost reduction and efficiency improvement the main theme. Besides layoffs, cloud exit to slash expensive cloud spending is increasingly being considered and put on the agenda by more enterprises.

We believe public cloud has its place - for very early-stage companies, or companies that won't exist in two years, for companies that don't care about spending money at all, or truly have extremely volatile irregular loads, for companies needing overseas compliance, CDN and other services, public cloud remains a very worthy service option.

However, for the vast majority of established companies with certain scale, if they can amortize assets over several years, you should really seriously re-examine this cloud fever. The benefits have been greatly exaggerated - running things in the cloud is usually as complex as doing it yourself, but ridiculously expensive. I really suggest you do the math.

Over the past decade, hardware has continuously evolved at Moore's Law pace, IDC 2.0 and resource clouds have provided cost-effective alternatives to public cloud resources, and the emergence of open source software and open source management/scheduling software has made self-building capabilities readily available - cloud exit and self-building will have very significant returns in cost, performance, and security autonomy.

This collection **"Database Mudslide - Deconstructing Public Cloud with Data"** contains our own first-hand experiences as clients in the process of going to/leaving cloud, collecting and analyzing actual performance cost data comparing self-building with cloud services, providing reference and lessons learned.

We advocate cloud exit concepts and provide practical paths and viable self-building alternatives - we'll pave the ideological and technical roads in advance for followers who agree with this conclusion.

For no other reason than hoping all users can own their digital homes, rather than renting farms from tech giant cloud lords. - This is also a movement against internet centralization and cyber landlord monopoly rent-seeking, allowing the internet - this beautiful free haven and utopia - to go further.

--------------

## [Cloud Exit Odyssey](/cloud/odyssey/)

The contemporary cloud exit epic, cloud repatriation odyssey. The legendary cloud exit story from 37 Signal: how to exit cloud and save 50 million yuan in 6 months. I selected 10 articles from @dhh's blog, presenting this magnificent journey in reverse chronological timeline, translated into Chinese for your reference.

Author: **David Heinemeier Hansson**, aka DHH, 37 Signal co-founder & CTO, Ruby on Rails creator, cloud exit advocate, practitioner, and leader. Pioneer fighting tech giant monopolies. Blog: https://world.hey.com/dhh

Translator: **Feng Ruohang**, aka Vonng. Founder & CEO of PieCloudDB. Pigsty author, PostgreSQL expert and evangelist. Cloud computing mudslide, database veteran, cloud exit advocate and practitioner.

--------------

## [The End of FinOps is Cloud Exit](/cloud/finops/)

At the SACC 2023 FinOps session, I heavily criticized cloud providers. This is the written transcript of my live speech, introducing the concept and practical path of ultimate FinOps - **cloud exit**.

**FinOps Focus is Misguided**: **Total Cost = Unit Price x Quantity**, FinOps people focus on reducing wasteful resource **quantity** but deliberately ignore the elephant in the room - **cloud resource unit prices**.

**Public Cloud is a Pig-Killing Scam**: Cheap EC2/S3 for customer acquisition, EBS/RDS for pig-killing. Cloud computing costs 5x self-building, while block storage costs can reach 100x+, the ultimate cost assassin.

**FinOps End Point is Cloud Exit**: For enterprises with certain scale, IDC self-building total costs are around 10% of cloud service list prices. Cloud exit is the end point of orthodox FinOps and the true starting point of real FinOps.

**Self-Building Capability Determines Negotiating Power**: Users with self-building capability can negotiate extremely low discounts even without leaving cloud, while companies without self-building capability can only pay high "no-expert tax" to public cloud providers.

**Database is Self-Building Key**: Stateless applications and data warehouses on K8S are relatively easy to migrate. The real difficulty is completing database self-building without affecting **quality and security**.

--------------

## [Why Isn't Cloud Computing More Profitable Than Mining Sand?](/cloud/profit/)

Public cloud gross margins are lower than mining sand. Why have pig-killing scams become money-losing operations?

Resource-selling models lead to price wars, open source alternatives shatter monopoly dreams.

Service competitiveness gradually gets leveled, where is cloud computing heading?

In "[Are Cloud Disks Pig-Killing Scams](/cloud/ebs/)", "[Are Cloud Databases Intelligence Tax](/cloud/rds/)" and "[Are Cloud SLAs Just Placebos](/cloud/sla/)", we've studied true costs of key cloud services. Cloud server costs calculated per core·month at scale are 5-10x self-building, cloud databases can reach 10+ times, cloud disks can reach 100+ times. With this pricing model, cloud gross margins of 80-90% wouldn't be surprising.

Industry benchmarks AWS and Azure can easily reach 60% and 70% gross margins. Looking at domestic cloud computing, gross margins generally hover around single digits to **15%**, with top dog Alibaba Cloud at most giving a "estimated long-term overall gross margin 40%". Cloud providers like Kingsoft Cloud have gross margins directly driven to **2.1%**, lower than manual sand mining.

Speaking of net profits, domestic public cloud providers are even more miserable. AWS/Azure net profit margins can reach 30%-40%. Benchmark Alibaba Cloud barely struggles around the break-even line. This makes one curious: **how did these domestic cloud providers manage to turn a 30-40% pure profit business into this state?**

--------------

## [Are Cloud SLAs Just Placebos?](/cloud/sla/)

In the cloud computing world, Service Level Agreements (SLAs) are viewed as cloud providers' commitments to service quality. However, when we deeply study these SLAs, we find they can't "back you up" as expected: you think you've insured your database and can sleep peacefully, but actually your hard-earned money bought emotion-value-providing placebos.

For cloud providers, **SLA isn't a real reliability commitment or historical track record, but a marketing tool aimed at making buyers believe cloud providers can host critical business applications**. For users, SLA isn't an insurance policy covering losses. In worst cases, it's a dumb loss you have to swallow. In best cases, it's a placebo providing emotional value.

**Rather than saying SLA compensates users, it's better to say SLA "punishes" cloud providers when service quality doesn't meet standards**. Cloud providers don't need to excel in reliability - missing targets just means a self-imposed penalty drink. However, customers must bear the bitter consequences themselves.

--------------

## [Are Cloud Disks Pig-Killing Scams?](/cloud/ebs/)

We've already answered "[Are Cloud Databases Intelligence Tax](/cloud/rds/)" with data, but facing **public cloud** **block storage's** **hundred-fold premium pig-killing ratio**, cloud databases pale in comparison. This article uses actual data to reveal public cloud's real business model - cheap EC2/S3 for customer acquisition, EBS/RDS for pig-killing. This practice also makes public cloud drift further from its original vision.

EC2/S3/EBS are the pricing anchors for all cloud services. If EC2/S3 pricing can barely be called reasonable, then EBS pricing is deliberate pig-killing. Public cloud providers' best block storage services have basically the same performance specs as self-building available PCI-E NVMe SSDs. However, compared to direct hardware procurement, **AWS EBS costs 120x more, while Alibaba Cloud's ESSD can reach 200x**.

Plug-and-play disk hardware with hundred-fold premiums - why? Cloud providers can't explain where such sky-high prices come from. Combined with other cloud storage services' design philosophy and pricing models, there's only one reasonable explanation: **EBS's high premium ratio is deliberately set as a threshold to facilitate cloud database pig-killing**.

As cloud database pricing anchors, EC2 and EBS have premiums of several times and dozens of times respectively, supporting cloud database pig-killing high gross margins. But such monopoly profits can't last: IDC 2.0/telecom operators/state-owned clouds impact IaaS; private cloud/cloud/-native/open source alternatives impact PaaS; tech industry layoffs, AI impact, and China's low labor costs impact cloud services (operations outsourcing/shared experts). **If public clouds persist with current pig-killing models, departing from "compute-storage infrastructure" original intentions, they'll inevitably face increasingly severe competition and challenges from the combined force of these three**.

--------------

## [Are Cloud Databases Intelligence Tax?](/cloud/rds/)

Recently, Basecamp & HEY co-founder DHH's article [1,2] caused heated discussion, summarized as: "*We spend $500K annually on cloud databases (RDS/ES), you know how many awesome servers $500K can buy? We're leaving cloud, goodbye!*"

So, how many awesome servers can $500K buy?

A 64C 384G + 3.2TB NVMe SSD high-spec database server, our local self-building, 5-year amortization, costs 15K yuan annually. Self-building two for HA costs 50K annually, same spec on Alibaba Cloud costs 250-500K (3-year 50% discount); AWS is even more outrageous: 1.6-2.17 million yuan.

So the question is: if using cloud database for 1 year costs enough to buy several or even dozens of better-performing servers, what's the point of using cloud databases? If you feel you lack self-building capability - we provide a ready-to-use, free RDS management alternative to solve this problem! - Pigsty!

**If your business fits the public cloud applicability spectrum, that's great; but paying several to dozens of times premium for unnecessary flexibility and elasticity is pure intelligence tax.**

--------------

## [Paradigm Shift: From Cloud to Local-First](/cloud/paradigm/)

**Initially, software ate the world**. Commercial databases represented by Oracle replaced manual bookkeeping with software for data analysis and transaction processing, greatly improving efficiency. However, commercial databases like Oracle are very expensive - just software licensing per core·month can cost over 10K, not affordable for most large institutions. Even wealthy companies like Taobao had to "de-Oracle" after scaling up.

**Then, open source ate software**. "Open source free" databases like PostgreSQL and MySQL emerged. Open source software itself is free, requiring only dozens of yuan per core per month in hardware costs. In most scenarios, if you can find one or two database experts to help enterprises use open source databases well, it's much more cost-effective than foolishly paying Oracle.

Open source software brought huge industry transformation - internet history is open source software history. Despite this, open source software is free, but experts are scarce and expensive. Experts who can help enterprises use/manage open source databases well are extremely scarce, even priceless. In a sense, this is the business logic of "open source" mode: free open source software attracts users, user demand creates open source expert positions, open source experts produce better open source software. However, expert scarcity also hindered further open source database adoption. Thus, "cloud software" appeared - **can't monopolize software? Monopolize experts instead**.

**Then, cloud ate open source**. Public cloud software resulted from internet giants productizing their open source software usage capabilities for external output. Public cloud providers wrap open source database kernels, package them with management software running on hosted hardware, and hire shared DBA experts for support, creating cloud database services (RDS). This is indeed valuable service and provides new monetization avenues for much software. But cloud providers' free-riding behavior is undoubtedly exploitation and extraction from open source software communities, and open source organizations and developers defending computing freedom naturally fight back.

Cloud software's rise triggers new balancing counter-forces: local-first software corresponding to cloud software begins emerging like mushrooms after rain. We're witnessing this **paradigm shift** firsthand.
