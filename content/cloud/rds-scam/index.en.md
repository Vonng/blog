---
title: "Cloud Database: Michelin Prices for Cafeteria Pre-made Meals"
date: 2024-10-06
author: |
  [Feng Ruohang](https://vonng.com)（[@Vonng](https://vonng.com/en/)）
summary: >
  The paradigm shift brought by RDS, whether cloud databases are overpriced cafeteria meals. Quality, security, efficiency, and cost analysis, cloud exit database self-building: how to implement in practice!
tags: [Cloud-Exit,RDS]
---

Are cloud databases overpriced cafeteria meals

The paradigm shift brought by RDS

Quality, security, efficiency, and cost analysis,

Cloud exit database self-building: how to implement in practice!


----------

## TL;DR

From commercial software to open source software to cloud software, the software industry has undergone paradigm shifts, and databases are no exception: cloud vendors took open source database kernels and defeated traditional enterprise database companies.

Cloud databases are a very profitable business: they can sell hardware computing power costing less than 20¥/core·month at ten to dozens of times markup, easily achieving 50%-70% or even higher gross margins.

However, as hardware follows Moore's Law and open source alternatives emerge for cloud management software, this business faces severe challenges: cloud database services lose cost-effectiveness, and cloud exit self-building becomes a trend.


-----------

**Cloud databases are overpriced pre-made meals - how to understand this?**

You spend 10 yuan heating yellow braised chicken rice meal packets in your microwave at home. Restaurant owners heat the same in their microwave, serve it in bowls for 30 yuan - you wouldn't mind, rent, utilities, labor, and service all cost money.
But if the owner now serves the same bowl of rice for 1000 yuan saying: we don't provide yellow braised chicken rice, **but reliable guaranteed elastic dining services**, the price was the same ten years ago anyway,
wouldn't you feel like beating up this owner? This exact thing happens with cloud databases and various other cloud services.

For large-scale computing power and storage, cloud service pricing can only be described as outrageous: cloud database markup rates can reach dozens of times.
As a business, cloud database gross margins can easily reach 50%-70%, contrasting sharply with the struggling resource-selling IaaS (10%-15%).
Unfortunately, cloud services don't provide quality service matching their high prices: cloud database service quality, security, and performance are also disappointing.

The more serious problem is: as hardware follows Moore's Law development and open source alternatives emerge for cloud management software, the cloud database model faces severe challenges:
Cloud database services lose cost-effectiveness, and cloud exit self-building becomes a trend.


-----------

**What are cloud databases?**

Cloud databases are database services in the cloud - a new software delivery paradigm: users don't "own software" but "rent services."

Traditional commercial databases (like Oracle, DB2, SQL Server) and open source databases (like PostgreSQL, MySQL) correspond to this cloud database concept.
The common feature of these two delivery paradigms is that software is a "product" (database kernel), users "own" software copies, buy/freely download and run on their own hardware;

Cloud database services (AWS/Alibaba-Cloud/... RDS) typically bundle software and hardware resources, packaging open source database kernels running on cloud servers as "services":
Users access and use database services through cloud platform-provided database URLs, managing databases through cloud vendor proprietary management software (platform/PaaS).


-----------

**What are the database software delivery paradigms?**

**Initially, software devoured the world**. Commercial databases represented by Oracle replaced manual bookkeeping with software for data analysis and transaction processing, greatly improving efficiency. However, commercial databases like Oracle are very expensive - software licensing alone can cost over 10,000 per core per month, not affordable for most institutions. Even Taobao, despite being wealthy, had to "de-Oracle" after scaling up.

**Then, open source devoured software**. "**Open source** free" databases like PostgreSQL and MySQL emerged. Open source software itself is free, costing only dozens per core per month for hardware. In most scenarios, finding one or two database experts to help enterprises use open source databases well would be much more cost-effective than foolishly sending money to Oracle.

Open source software brought huge industry transformation - **the history of the internet is the history of open source software**. Nevertheless, open source software is free, but **experts are scarce and expensive**. Experts who can help enterprises **use/manage** open source databases well are very scarce, even priceless. In a sense, this is the business logic of the "open source" model: **free open source software attracts users, user demand creates open source expert positions, open source experts produce better open source software**. However, expert scarcity also hindered further adoption of open source databases. Thus, "cloud software" emerged.

**Then, cloud devoured open source**. Public cloud software is the result of internet giants productizing their ability to use open source software for external output. Public cloud vendors wrap open source database kernels with shells, package them with management software running on managed hardware, and hire shared DBA experts for support, becoming **cloud database services** (RDS). **Cloud is indeed a valuable service, also providing new monetization paths for much software. But cloud vendors' free-riding behavior is undoubtedly exploitation and extraction from open source software communities**, and cloud computing Robin Hoods are also gathering to organize counterattacks.


-----------


**Classic commercial databases Oracle, DB2, SQL Server all sell very expensively - why can't cloud databases sell at high prices?**

In the commercial software era, which can be called Software 1.0 era, databases represented by Oracle, SQL Server, IBM were indeed very expensive.




-----------

**Question: You think it's expensive, let me argue - isn't this normal business logic?**

Expensive isn't the big problem - there are customers who only want the best regardless of price. However, the problem is cloud databases aren't good enough. First: the kernel is open source PG/MySQL, what they actually do is just management. Yet in their marketing, they claim to be cure-all panaceas: storage-compute separation, Serverless, HTAP, cloud-native, hyper-converged... RDS is an advanced car while old databases are horse carriages... blah

-----------

**Question: If it's not horse carriage vs car, what should it be?**

The difference is at most gas car vs electric car. Elaborating the analogy between database industry and automotive industry. Database:automobile; DBA:driver; commercial database:branded car; open source database:assembled car; cloud database:taxi+rental driver, Didi ride-hailing; this model has its applicable spectrum.

-----------

**Question: Cloud database's applicable spectrum?**

Startup phase, extremely small traffic simple applications / 2 completely unpredictable, highly volatile loads / 3 global expansion compliance scenarios, rent-to-buy ratio. Small enterprises shouldn't bother, go to cloud (but which cloud is worth discussing), large enterprises undoubtedly should exit cloud. A more practical approach is buy baseline, rent peaks, hybrid cloud - mainly exit cloud, elastically go to cloud.

-----------

**Question: So it seems cloud computing indeed has its value and ecological niche.**

1. "Tech Feudalism," monopoly giants' damage to ecosystems. / 2. Cloud marketing, bragging should be taxed.

3. Setting aside grand narratives, cloud database costs are not cheap. ... (elasticity/0-100km acceleration), introducing cost issues.




-----------

**Why this saying? Why feel expensive?**

Let's use specific examples to illustrate.

For example at Tantan, we once evaluated post-cloud costs. Our overall server TCO was

, one was... 75k for 5 years, 15k annual TCO. Two servers for high availability would be 30k annually. Alibaba-Cloud East China 1 default AZ, dedicated 64-core 256GB instance: pg.x4m.8xlarge.2c, plus a 3.2TB ESSD PL3 cloud disk. Annual costs range from 250k (3 years) to 750k (on-demand). AWS overall ranges from 1.6-2.17 million annually.

Not just us, Ruby on Rails author DHH shared their complete 37 Signal company cloud exit journey in 2023.

Introducing [DHH's cloud exit example](https://pigsty.io/zh/cloud//odyssey/), $3M annual consumption. After one-time **$600k** investment in self-hosted servers, annual spending dropped to $1M, one-third of original. Could save $7M over five years. Cloud exit took half a year without requiring more personnel for operations.




Especially considering open source alternatives' emergence
— 

"Virtue doesn't match position leads to disaster"

Literal meaning: using cloud databases is actually paying five-star hotel Michelin restaurant prices for cafeteria pre-made meal packages.


For example on AWS, if you want to purchase a high-spec PostgreSQL cloud database instance, you typically need to pay over ten times the price of corresponding cloud servers. Considering cloud servers themselves have about 5x markup, cloud services compared to scale self-building




-----------

## RDS Database Paradigm Shift

Last episode's cloud computing mudslide discussed Luo Yonghao selling "cloud" in Taobao livestream: first selling robot vacuums, then tardy Luo read scripts selling "cloud" for forty minutes, then abruptly switched to selling **Colgate enzyme-free toothpaste**. This was clearly a failed livestream attempt: over a thousand enterprises ordered cloud servers in the livestream, 100-200 yuan cloud server unit prices plus one-per-company purchase limits meant at most 200k revenue, possibly less than Luo's appearance fee.

I wrote an article "[Luo Yonghao Can't Save Toothpaste Cloud](https://mp.weixin.qq.com/s/s_MCdaCByDBuocXkY1tvKw)" mocking Alibaba-Cloud selling virtual machines in livestreams as toothpaste cloud. Then my friend Swedish Ma immediately wrote "[Toothpaste Cloud? You're Flattering Cloud Vendors](https://mp.weixin.qq.com/s/ffrwbLiGxTLO1jVh8mHiBA)" refuting: "No domestic cloud vendor deserves the toothpaste cloud title. From profit margins to social value to brand management, quality management and market education, public cloud vendors are completely outclassed by toothpaste manufacturers."


-----------

**What are cloud databases - a software paradigm shift?**

**Initially, software devoured the world**. Commercial databases represented by Oracle replaced manual bookkeeping with software for data analysis and transaction processing, greatly improving efficiency. However, commercial databases like Oracle are very expensive - software licensing alone can cost over 10,000 per core per month, not affordable for most institutions. Even Taobao, despite being wealthy, had to "de-Oracle" after scaling up.

**Then, open source devoured software**. "**Open source** free" databases like PostgreSQL and MySQL emerged. Open source software itself is free, costing only dozens per core per month for hardware. In most scenarios, finding one or two database experts to help enterprises use open source databases well would be much more cost-effective than foolishly sending money to Oracle.

Open source software brought huge industry transformation - **the history of the internet is the history of open source software**. Nevertheless, open source software is free, but **experts are scarce and expensive**. Experts who can help enterprises **use/manage** open source databases well are very scarce, even priceless. In a sense, this is the business logic of the "open source" model: **free open source software attracts users, user demand creates open source expert positions, open source experts produce better open source software**. However, expert scarcity also hindered further adoption of open source databases. Thus, "cloud software" emerged.

**Then, cloud devoured open source**. Public cloud software is the result of internet giants productizing their own ability to use open source software for external output. Public cloud vendors wrap open source database kernels with shells, package them with management software running on managed hardware, and hire shared DBA experts for support, becoming **cloud database services** (RDS). **This is indeed a valuable service, also providing new monetization paths for much software. But cloud vendors' free-riding behavior is undoubtedly exploitation and extraction from open source software communities**, and defenders of computing freedom in open source organizations and developers will naturally fight back.




-------------

## Are Cloud Databases Overpriced Cafeteria Meals

**Question: Let's first discuss the cost issue - isn't cost a claimed advantage of cloud databases?**

Depends on comparison - compared to traditional commercial databases Oracle it's fine, compared to open source databases it doesn't work - especially small scale is okay (DBA), but any scale doesn't work.

-----------


**Question: Can cloud save DBA/database expert costs?**

Yes, good DBAs are scarce and hard to find. But using cloud databases doesn't mean you no longer need DBAs - you just save system construction work and daily operational work, but there are parts you can't save. Second, we can calculate specifically at what scale hiring a DBA is cost-effective compared to cloud databases. (Discussing several pricing models)


-----------


**Question: What's the relationship between RDS and DBAs?**

The core value RDS and DBAs provide isn't database products, but the capability to use open source database kernels well. ... One mainly relies on DBA veterans, one mainly relies on management software. One is employment, one is rental. I think the ecosystem lacks one model - owning management software, so what I made is open source database management software.

-----------

**Question: So cloud databases have no cost advantage?**

Very small scale has advantages, standard size or large-scale databases have no cost advantages.

To compare costs you need to see how. Cloud database billing items: compute + storage, plus traffic fees, database proxy fees, monitoring fees, backup fees.

The big items are compute and storage, compute unit is..., storage unit is... (some key numbers)

-----------

**Question: How to calculate instance costs?**

Alibaba RDS: 7x-11x, PolarDB: 6x~10x, AWS: 14x ~ 22x

| Dual-Instance HA Price     | 4x Core/Month Price | 8x Core/Month Price |
|---------------------------|-------------------|-------------------|
| HA RDS Series Core/Month Avg | **¥339**          | **¥432**          |
| AWS RDS HA Reference      | **¥1,160**        | **¥1,582**        |
| Alibaba-Cloud PolarDB Ref | **¥250**          | **¥400**          |
| DHH Tantan Self-Built 1C Computing (Excluding Storage) |                  | **¥40**           |

Cloud servers - on-demand, monthly, annual, 5-year prepaid unit prices are **187¥, 125¥, 81¥, 37¥** respectively, compared to self-built **20¥** with markups of **8x, 5x, 3x, 1x**. After configuring common-ratio block storage (1 core:64GB, ESSD PL3), unit prices are: **571¥, 381¥, 298¥, 165¥**, compared to self-built **22.4¥** with markups of **24x, 16x, 12x, 6x**.

-----------

**Question: How to calculate storage costs?**

First look at retail unit prices, GB·month unit price, 2 cents, Alibaba-Cloud ESSD has several different tiers, from 1-4 yuan.

1TB storage·month price (full discount): self-purchase 16, AWS 1900, Alibaba-Cloud 3200


-----------

**Question: We've discussed cost issues above, but how can you focus only on cost? How important is cost really?**

When you have leading advantages in technology and products, cost isn't that important. But when technology and products can't differentiate, i.e., you're selling irreplaceable commodity standard products, cost becomes very important. Ten years ago, cloud databases might have been product/technology-driven, justifiably enjoying high margins. But today, ten years later, cloud isn't high-tech anymore, cloud has become commoditized. The market has shifted from value pricing to cost pricing, cost is crucial.

Alibaba's main business e-commerce was badly beaten by "cheap" Pinduoduo. What does Pinduoduo rely on? Just plain old cheapness. What you can sell on Taobao Tmall, I can sell the same but cheaper - that's core competitiveness. You're not Hermès, Rolex, luxury goods logic where you need to buy several times the goods to even sell to you. What can commodity cloud servers sandwiched between toothpaste and vacuum cleaners in Luo's livestream compete on besides cheapness?


-----------

**Question: When is cost not important?**

Second point is economic upswing prosperity periods, startup companies racing for speed during growth phases - calculating costs might be premature. But now it's obviously economic downturn recession... Also, if your product is good enough, users can ignore costs. Like going to five-star hotels, Michelin restaurants - you don't care about their ingredient costs, right? OpenAI ChatGPT is unique, take it or leave it. But going to wet markets to buy vegetables, you do look at costs. Cloud databases, cloud servers, cloud disks are all "ingredients," not dishes, requiring cost calculation and price comparison. (Yellow braised chicken rice story)


-----------

## Quality Security Efficiency Cost Analysis

**Question: We've thoroughly discussed price/cost in cost-effectiveness, now let's talk about quality, security, efficiency**

Cloud databases are expensive, so they have sales pitches when selling. Though we're expensive, we're good! ***Databases are the crown jewel of infrastructure software, embodying countless intangible intellectual property BlahBlah***. Therefore software prices far exceeding hardware are very reasonable... But are cloud databases really good?

-----------

**Question: Functionally, how are cloud databases?**

We won't discuss MySQL that can only do OLTP, but RDS PostgreSQL is worth discussing. Although PostgreSQL is the world's most advanced open source relational database, its unique feature is **extreme extensibility and thriving extension ecosystem**! Unfortunately, **"[Cloud RDS Castrated PostgreSQL's Soul](https://mp.weixin.qq.com/s/EH7RPB6ImfMHXhOMU7P5Qg)"** - users can't freely install extensions on RDS, and some powerful extensions are destined never to appear in [**RDS**](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng&mid=2247485745&idx=5&sn=a7d610ea37c3f3fa78ee4ba0ee705962&chksm=fe4b3ceac93cb5fc6f1975f94be04424e7b3690eedd1658951deb8d016f5f19ade8806d86417&scene=21#wechat_redirect). Using RDS cannot unleash PostgreSQL's true power - this is an **unsolvable deficiency** for cloud vendors.

-----------

**Question: What deficiencies do cloud PostgreSQL databases have in functionality extension?**

Contrib modules as part of PostgreSQL itself include 73 extension plugins. Among PG's built-in 73 extensions, Alibaba-Cloud kept 23 and castrated 49; AWS kept 49 and castrated 24. PostgreSQL official repository PGDG contains about 100 extensions. Pigsty as a PG distribution maintains and packages 20 powerful extension plugins. Total available extensions on EL/Deb platforms reach 234 - AWS RDS only provides 94 extensions, Alibaba-Cloud RDS provides 104 extensions.

For important extensions, the situation is worse. Missing extensions from AWS and Alibaba-Cloud include: (time-series TimescaleDB, distributed Citus, columnar Hydra, full-text search BM25, OLAP PG Analytics, message queue pgq, even some basic important components aren't provided, like WAL2JSON for CDC), version updates are also unsatisfactory.

-----------

**Question: Why can't cloud databases provide these extensions?**

Cloud vendors' official line is: security, stability, but this doesn't make sense. Cloud extensions all use tested rpm/deb packages downloaded from PostgreSQL official repository PGDG. What does cloud vendors need to test? But I think a more important issue is open source licensing, AGPLv3 challenges. Facing cloud vendors' freeloading, open source communities have started collective shifts, more and more open source software uses stricter, cloud-vendor-discriminatory licenses. For example, XXX all use AGPL releases - cloud vendors can't provide them without open-sourcing their cash cow management software.

We can discuss this separately in a later episode.

-----------

**Question: Regarding security mentioned above, are cloud databases really secure?**

1. Multi-tenant security challenges (malicious neighbors, KubeCon cases); 2. Larger attack surface on public networks (SSH brute force, SHGA);

3. Poor engineering practices (AK/SK, Replicator passwords, HBA modifications); 4. No confidentiality, integrity safeguards.

5. Lack of observability, making security issues hard to discover, evidence harder to collect, let alone accountability.

-----------

**Question: Cloud database observability is terrible - how so?**

Information, data, intelligence are crucial for management. But the monitoring systems provided by cloud are, quality-wise, hard to describe. Back in 2017 I surveyed all PostgreSQL database monitoring systems available... indicator count, chart count, information content. Observability concepts, all terrible. Monitoring granularity is also low (minute-level), want 5-second level? Sorry, please pay more.

AustinDatabase host just published "[Give Me One Reason Not to Fire DBAs After Going to Cloud](https://mp.weixin.qq.com/s/IMgJBZ9uqU5x738p9mED4w)" discussing this issue: wanting to open tickets on Alibaba-Cloud for problem analysis, customer service frantically recommends DAS (Database Autonomous Service), please pay more, 6K monthly per instance at sky-high prices.

Without good enough monitoring systems, how do you assign responsibility, how do you seek accountability? (Like hardware issues, overselling, IO contention causing performance avalanches, primary-replica failovers causing customer losses)

-----------

**Question: Besides security and observability issues, many users care more about quality reliability**

Cloud databases don't provide reliability guarantees, no SLA clauses backing this up.

Only availability SLAs, which are lousy SLAs with joke-level compensation ratios. Marketing confusion: mixing SLA with actual reliability track records.

Basic standard version databases don't even have WAL archiving and PITR, just simple rollback to specific backups, users have no self-service problem resolution capabilities.

Famous Double 11 outages, amateur hour theory, cost reduction jokes. Zhongting gang... observability team amateurs, fresh graduates maintaining systems.

Business continuity track record isn't ideal: RTO, RPO, claimed as =0 =0, actually... Tencent Cloud disk failures causing startup data loss cases.

-----------

**Question: Are cloud databases really good? (Performance dimension)**

Let's first discuss performance. We talked about cloud disk prices earlier, not cloud disk performance. Typical EBS block storage performance, IOPS, latency, local disks. More importantly, these high-tier cloud disks [aren't available just because you want them](https://pigsty.io/zh/cloud//ecs/#云存储对单价的影响). If you buy less than 1.2TB, they won't sell you ESSD PL3. The next tier ESSD PL2's IOPS throughput is only 1/10 of ESSD PL3.

Second issue is resource utilization. RDS management eats 2GB... doing nothing but consuming half the memory. Java management, log agents.

High-availability cloud databases have replicas but don't let you read them. Consuming double your resources, right? If you want read-only instances you need to apply separately.

Finally, improved resource utilization profits go to cloud vendors, benefits harvested by cloud vendors, costs borne by users.


-----------

**Question: Other points? Like maintainability?**

Every operation requires SMS verification codes - what about 100 PostgreSQL clusters? ClickOps small-scale agriculture, real enterprise users and developers need IaC, but performance here is lacking. K8S Pigsty both do well, natively built-in IaC. RPA robotic process automation. Poor API design, for example, several different styles of [error codes](https://help.aliyun.com/zh/rds/developer-reference/api-rds-2014-08-15-errorcodes?spm=a2c4g.11186623.0.0.604b1fbaxZLPDN), [instance state tables](https://help.aliyun.com/zh/rds/developer-reference/instance-state-table?spm=a2c4g.11186623.0.0.437f5df9BftH2v) (camelCase, snake_case, ALL_CAPS, two-segment) reflecting poor software engineering quality.

Business continuity, RTO RPO, like doing PITR through creating new on-demand instances. What about the original instance? How to rollback? How to ensure recovery time? Qualified DBAs should know these things - why doesn't cloud RDS know?

-----------

## Do Cloud Databases Excel Anywhere?

**Question: Don't cloud databases have any outstanding aspects?**

Yes, elasticity. Public cloud elasticity is designed for its business model: extremely low startup costs, extremely high maintenance costs. Low startup costs attract users to cloud, and good elasticity can adapt to business growth anytime. But after business stabilizes, vendor lock-in occurs, making it hard to leave, and extremely high maintenance costs make users suffer. This model has a colloquial name - **pig-slaughtering scam**. This model's extreme is Serverless. Cloud vendors' fake Serverless.

-----------

**Question: Another often mentioned with elasticity is agility?**

Agility used to be cloud databases' unique advantage, but not anymore. First, true Serverless, Neon, Supabase, Vercel free tiers, cyber bodhisattvas. Second, Pigsty management, launching new databases also takes 5 minutes. Cloud vendors' ultimate elasticity, second-level scaling is actually deceptive - hundreds of seconds are still seconds...

-----------

**Question: Let's talk Serverless - is this the future? Why call it money-extraction technique?**

Cloud vendors' RDS Serverless is essentially an elastic billing model, not technological innovation. Real technologically innovative Serverless RDS can reference Neon:

1. Scale to Zero,
2. No pre-configuration needed, directly connect to auto-create instances and use.

RDS Serverless is marketing deception. Just billing model differences, a terrible joke. Following cloud vendors' marketing strategy, I take a shared PG cluster, create a new Database for each tenant, no resource isolation, charge by actual Query count or Query Time - this can also be called Serverless.

Then according to this definition, all cloud vendor products suddenly become Serverless. Then Serverless word's real meaning gets usurped, becoming mundane boring billing technology. Real good Serverless should look at cyber bodhisattva Cloudflare.

Here I'll mention that Serverless claims to solve ultimate elasticity problems, but elasticity itself isn't that important

-----------

**Question: Why isn't elasticity important? How do traditional enterprises handle elasticity?**

Elastic peaks reaching dozens or hundreds of times normal levels, I think elasticity has value. Otherwise with current physical resource prices, directly over-provisioning 10x doesn't cost much... Cloud vendors' elasticity markup is about ten-plus times. Large clients' thinking is clear: with money for renting, why not over-provision 10x. Small users using serverless is understandable. Elasticity turning point, 40 QPS. Only scenario is those MicroSaaS. But those MicroSaaS can directly use free tiers from Vercel, Neon, Supabase, Cloudflare...

How do traditional enterprises solve this? We have 15% machine buffer pools. If insufficient, remove a few low-utilization replicas, machines arrive, PG online in 5 minutes. Server to IDC rack installation about two weeks, now IDC installation down to half day/one day.

-----------

**Question: So overall, how are cloud databases?**

Just now we analyzed cloud databases from quality, efficiency, security, cost aspects. Basically except for elasticity, performance is mediocre, and the only outstanding elasticity isn't as important as they claim. My overall evaluation of cloud databases is - pre-made meals. Can you eat them? Yes, won't kill you, but don't expect cafeteria food to taste good.

Amateur hour stages, no brand image. Like IBM DeveloperWorks. "[Defense Broken, Who Understands Family: Recording a MySQL Problem Investigation](https://mp.weixin.qq.com/s/Fc5oALMo1OJGIRK_Tf5VVA)"

-----------

## Cloud-Exit Database Self-Building: Practical Implementation!

**Question: When should you use cloud databases, when shouldn't you? Or what scale should go to cloud, what scale should exit cloud?**

Spectrum endpoints, DBaaS replacement, open source self-building. Classic threshold, team level.

Average technical teams: 1-3 million annual consumption, cloud KA. No one who understands, server manufacturers estimate 10 million scale.

Excellent technical teams: one physical machine ~ one rack volume, exit cloud, annual consumption tens of thousands to hundreds of thousands.

-----------

**Question: What other database options do small enterprises have?**

Neon, Supabase, Vercel, or directly host on cyber buddha Cloudflare.

-----------

**Question: You gave cloud databases thorough criticism from top-tier client, top DBA perspectives. Average enterprises don't have these conditions, what to do?**

Do three things well: how to solve open source alternatives to management software, how to solve hardware resource procurement and supply, how to solve people?

-----------

**Question: Open source management software, how so?**

For example, open source management software for managing servers: KVM/Proxmox/OpenStack, new generation is Kubernetes. Open source alternatives to object storage MinIO, or cost-effective Cloudflare R2

-----------

**Question: How to procure and manage hardware resources?**

IDC: Deft, Equinix, 21Vianet. IDCs can also be monthly payment, they're clear, not greedy at all, 30% gross margin plainly visible.

Servers + 30% gross margin, monthly payment, rack costs: 4000-6000 ¥/month (42U 10A/20A), can house over ten servers. Network bandwidth: shared bandwidth (general) 100/MB·month; dedicated bandwidth can reach 20 ¥/MB·month

You can also consider long-term rental of cloud vendors' cloud servers - five-year rentals cost double IDC prices. Choose instances with local NVMe storage for self-building, don't use EBS cloud disks.

-----------

**Question: Another issue - how to solve online problems? Cloud network/availability zones aren't something general IDCs can solve?**

Cloudflare solves the problem.

-----------

**Question: How to solve people, DBAs?**

Current economic situation and employment rate background, finding usable people at reasonable prices isn't difficult. Junior operations and DBAs are everywhere, senior experts find consulting companies - I provide such services.

-----------

**Question: Professional people doing professional things - from cloud centralized management to cloud-off self-building, isn't this regressive behavior?**

Whether cloud vendors have the most professional people doing this, I quite doubt. 1. Cloud vendors spread too thin, not investing much in each specific area; 2. Cloud vendors' elite employees have serious attrition, many start their own businesses. 3. Self-building definitely isn't historical regression but historical progress. Historical development is inherently pendulum-like reciprocal, spiral upward development.

-----------

**Question: Cloud database problems solved, but exiting cloud requires solving more than databases - what about other things? Object storage, virtualization, containers**

Leave for next episode discussion!
