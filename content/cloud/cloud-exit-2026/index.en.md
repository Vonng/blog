---
title: "Those Who Left the Cloud Made a Killing"
date: 2026-08-15
authors: [vonng]
summary: >
  I spent years urging people to leave the cloud. Those who listened two years ago made a killing. Leaving has never been just about savings; it is about buying back your freedom. Cost curves move. Sovereignty does not.
tags: [Cloud-Exit, Cloud, Data Sovereignty]
---

Leaving the cloud has never been just about saving money. It is about buying back your freedom. Cost curves move; sovereignty does not. I have spent years urging people to get out. Friends who listened two years ago made a killing.

---

## 1. The Best Trade of a Lifetime

This morning, I spotted a spectacular humblebrag from DHH on X:

![DHH looks back at the 19 PB all-flash system bought for the AWS S3 exit](dhh-s3-tweet.webp)

“Don’t know if I’ve ever timed a trade this well in my life.” A system bought for $1.5 million carried a $19 million list price just over a year later—more than 12×.

But this was never meant as an investment. DHH simply thought the S3 bill was too high and wanted to bring the data home. He set out to cut a bill and ended up turning a rack of flash into the best-performing asset he had ever bought.

The people trying to save money got rich; the fence-sitters are kicking themselves. That is the surreal reality of the 2026 storage market. Anyone still paying rent in the cloud should study the numbers behind that post.

![My follow-up post on DHH’s cloud-exit trade](cloud-exit-tweet.webp)

---

## 2. Three Years of Receipts

I followed DHH and 37signals—the company behind Basecamp and HEY—through the entire migration in my [Cloud Exit](/en/cloud/exit/) series.

![Timeline of DHH’s cloud-exit odyssey](odyssey-timeline.webp)

**October 2022:** DHH published “[Why we’re leaving the cloud](https://world.hey.com/dhh/why-we-re-leaving-the-cloud-654b47e0).” The reason was blunt: the annual cloud bill had reached $3.2 million, and enough was enough.

**2023:** 37signals spent about $700,000 on Dell servers and moved seven applications out of the cloud in six months. That year’s savings alone paid for all the hardware.

**2024:** The first full, clean year. The company saved nearly $2 million as its annual bill fell from $3.2 million to $1.3 million. Every dollar of that remaining $1.3 million went to S3, locked behind a four-year contract that ran until mid-2025. The final [savings beat even the revised estimate](/en/cloud/odyssey-done/).

**June 30, 2025:** The S3 contract expired. By then, 37signals had installed 18 PB of Pure Storage all-flash capacity across two data centers. The hardware cost about $1.5 million; five years of warranty and support cost under $1 million. DHH wrote “[It’s five grand a day to miss our S3 exit](https://world.hey.com/dhh/it-s-five-grand-a-day-to-miss-our-s3-exit-b8293563)” to keep everyone on schedule: every extra day on S3 meant $5,000—$35,000 a week or $150,000 a month. AWS ultimately granted a free 60-day egress window, waiving roughly $250,000 in transfer fees. The data moved. They parted on good terms.

**Projected five-year savings:** The estimate climbed from $7 million to more than $10 million. Not a single person was added to the operations team. DHH’s [cloud-exit FAQ](https://world.hey.com/dhh/the-big-cloud-exit-faq-20274010) and the retrospective on [staying highly available after leaving the cloud](/en/cloud/uptime/) explain how.

That is only the cost ledger. Performance is a separate matter. On-premises all-NVMe flash and network-attached cloud volumes are different species. I was running PostgreSQL on all-NVMe storage ten years ago. Most cloud users are still stuck on bargain-bin volumes with miserable IOPS.

Nor is this an isolated case. A friend in one of my group chats shared his numbers today: **more than RMB 100 million saved in two years after leaving the cloud.** Then he added a caveat: “That road is closed now. Hardware has become too expensive.”

---

## 3. The Window Is Narrowing

Since the second half of 2025, AI infrastructure has sucked the storage market dry. In [September 2025](https://www.trendforce.com/presscenter/news/20250925-12736.html), TrendForce expected NAND flash contract prices to rise 5–10% quarter over quarter in Q4. By [February 2026](https://www.trendforce.com/presscenter/news/20260202-12911.html), it had raised its Q1 forecast from 33–38% to 55–60%. In [March](https://www.trendforce.com/presscenter/news/20260331-12995.html), it projected that Q2 prices would rise another 70–75%.

Retail prices followed. Some entry-level 1 TB SSDs that had sold for about $45 briefly hit $90. DRAM was tighter still, with [prices up roughly 172% year over year in Q3 2025](https://www.z2data.com/guides/ai-memory-chip-shortage). No quick supply relief is in sight. [Enterprise SSDs now consume roughly 60% of NAND output](https://www.blocksandfiles.com/data-management/2026/06/18/keep-your-data-and-your-budget-during-the-capacity-crunch/5248187). [SK hynix said in October 2025 that it had already secured customers for its entire 2026 DRAM and NAND output](https://news.skhynix.com/sk-hynix-announces-3q25-financial-results/). Meaningful new capacity is not expected before late 2027. PC makers have begun shrinking base storage or switching to cheaper NAND: [Dell’s new XPS 13 again offers a 256 GB option](https://www.tomshardware.com/laptops/dell-xps-13-targets-macbook-neo-with-intels-wildcat-lake-usd699-starting-price-usd599-for-students), while [Lenovo has begun shipping ThinkBook laptops with cheaper Chinese-made SSDs](https://www.techspot.com/news/112998-lenovo-starts-shipping-business-laptops-chinese-made-ymtc.html).

Consumer SSD and memory vendors—and PC makers—now face the same pressure: raise prices or cut specifications. A friend noted that a server once priced at RMB 100,000 now costs more than RMB 300,000. Consumers see the same thing. An [AMD AI Max mini PC I bought last year for a little over RMB 10,000](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247490389&idx=1&sn=c80d97f60ebe69fe303273de228e14c5&scene=21#wechat_redirect) now costs well over twice as much.

![Old and new prices for an AMD AI Max mini PC](ai-max-price.webp)

**Whether to move to the cloud or leave it comes down to where the cost curves cross. The larger you are, the more self-hosting pays.** Two years ago, hardware was dirt cheap, so even a tiny business could reach that crossover with a stretch. That was why I spent those two years shouting: if you can stretch to it, get out. Hardware prices have since soared, pushing the crossover into midsize-company territory. The window has narrowed.

The people who listened, bought servers, and left the cloud made a killing. Those scared off by “replacing disks is too much work” or “people cost too much” now have every reason to regret it. With a stretch, they could once have become cyber smallholders, if not landlords. Now they may be locked in as tenant farmers—or serfs—for life.

Still, better late than never. A narrower window does not invalidate the case for leaving the cloud.

---

## 4. Renting Leaves You Exposed; Buying Is a Hedge

DHH’s accidental 12-bagger exposes an often-missed fact:

**The cloud makes you rent hardware forever at whatever the market charges today.**

Think the cloud protects you from hardware inflation? It does not. Cloud providers still buy the DRAM and NAND in their servers from Samsung, SK hynix, and Micron. When their costs rise, your bill eventually follows: discounts shrink, renewals cost more, and new instance prices climb. You escaped nothing. You kept the entire exposure and merely delayed settlement.

A self-hoster locks in five years of hardware cost on the day of purchase. Prices can then go through the roof without changing that bill. In DHH’s case, the replacement list price rose more than 12×. In market terms: **renting cloud capacity leaves you naked short; buying hardware is a hedge.**

Moore’s law spoiled us for two decades. Everyone assumed hardware would only get cheaper, renting could never hurt, and waiting to buy guaranteed another discount. The AI boom has overturned that assumption. Compute and storage are now hard assets: owners get the appreciation; renters eat the inflation.

So “hardware is too expensive; forget about leaving the cloud” gets it exactly backward. Higher prices prove that the people who exited early made the right bet. They also show how much inflation is still buried in your cloud bill.

---

## 5. Discounts Follow Leverage

I have never believed leaving the cloud was only about cost. Savings are the surface; sovereignty is the substance.

Your cloud discount ultimately depends on one thing: your exit option. **Can you actually leave?**

Why was DHH’s S3 price so low? The four-year commitment helped. More importantly, AWS knew he could leave and would leave. He had already moved all compute out in 2023, proving the threat was credible. When the storage contract ended, AWS waived the egress fees, opened a free migration window, and sent him on his way without drama.

Now take a company whose database, object store, and message queue are welded to one vendor’s proprietary PaaS, with no credible migration plan. That company is a captive customer, ready to be fleeced. Why offer a deep discount to someone who cannot escape?

This is why I keep repeating: **without the ability to self-host, you have no exit; without an exit, you have no negotiating leverage.** Hybrid cloud and multicloud sound grand, but they only mean something if you can run the systems yourself. If you bring no Plan B to the table, it is not a negotiation. It is begging.

---

## 6. Servers Don’t Lock You In—Data Does

What actually traps you in the cloud? Not servers. IaaS resources—servers, bandwidth, disks, and now even AI model tokens—are commodities. If one supplier disappoints you, compare prices and buy from another. No vendor can lock you in at that layer.

What truly locks you in is PaaS—and the data inside it. Data has gravity. At a few hundred gigabytes, you can pick it up and leave. At tens of terabytes, the move hurts. At petabyte scale, egress fees alone can kill the idea. AWS added free exit transfers over the past two years only under pressure. Without them, moving DHH’s petabytes home would have cost hundreds of thousands of dollars in egress charges.

Among all PaaS services, two are the real choke points: **the database and the [object store](/en/db/long-live-silo/).**

You can skip Kubernetes. A huge share of the world’s services run perfectly well on bare Linux with systemd. You can skip the fancy managed middleware too. But you cannot avoid a database, and any business with files needs an object store or filesystem. **Your lock-in lives wherever your state does.** The first step toward leaving the cloud is therefore not buying servers or renting racks. It is **standardizing on interfaces with open-source implementations**:

- Standardize database access on the PostgreSQL wire protocol.
- Standardize object storage on the S3 API.

Both are de facto cloud standards with complete open-source implementations. Use managed PostgreSQL and managed object storage today; swap in self-hosted PostgreSQL and an open-source object store tomorrow without changing a line of application code. Neutral interfaces leave every door open.

Every proprietary PaaS interface with no portable equivalent is another signature on the indenture.

DHH noted one revealing detail. Pure Storage exposes an S3-compatible API, so 37signals needed neither Ceph nor MinIO. But he immediately added that an open-source object store is exactly what you want for the same job on commodity hardware. Big spenders can take the $1.5 million appliance route; everyone else can pair commodity servers with open-source software. Either route ends at the same place: an S3 interface under your control.

---

## 7. Three Tired Cloud Talking Points, Taken Apart

At this point, it is time to take apart the cloud camp’s three oldest talking points.

**Talking point one: “Self-hosting means replacing disks. What a hassle—and what if I lose data?”**

This horror story never dies. Apparently, the moment a company leaves the cloud, its CTO must crouch in a server room at midnight, screwdriver in hand.

Look closer. Servers carry multi-year warranties. When a disk fails, call the vendor and have a technician replace it. Even at a scale where disks fail every day—like my friend who saved more than RMB 100 million in two years—a rounding error from those savings can pay for 24/7 on-call coverage many times over. This is not a serious objection.

That fear is a hangover from the single-server RAID 5 era. One disk died; the array began rebuilding; another failed halfway through, and everything was gone. That was frightening for good reason. Modern redundancy lives at the cluster layer. Databases have replication and failover. Object stores have erasure coding and multiple replicas. A disk—or an entire machine—can fail while the service keeps running. These are standard runbook scenarios, drilled to exhaustion. Once availability is sound at the PaaS layer, replacing a disk is like changing sheets at a hotel. **The dirty sheet goes; the hotel stays open.** No hotel closes because laundry is inconvenient.

**Talking point two: “Self-hosting needs specialists, and people are expensive.”**

Two years ago, that argument had a point. Running databases and object storage demanded experienced operators. Tuning, backups, recovery, and difficult troubleshooting all depended on accumulated judgment. A good DBA could command tens of thousands of RMB per month. A small company genuinely could not afford one.

Today, a $200-per-month Claude or Codex subscription gives you 24/7 help and can analyze many obscure failures better than plenty of practitioners. The tools have changed too. Open-source distributions have turned operational know-how into a product. High availability, backup and restore, point-in-time recovery, monitoring, alerting—the lessons operators once paid for in production outages now ship as defaults.

The cloud locks customers in at three layers. The **resource layer** is replaceable and cannot hold you. The **data layer** has gravity and weighs the most. The most insidious is the **skills layer**. Spend ten years in the cloud and a team can collectively forget how to run its own systems. Eventually it stays not because it wants to, but because it no longer knows how to leave. That is the deepest lock. AI is now picking it, making once-scarce operational expertise broadly accessible again.

**Talking point three: “It isn’t my money anyway.”**

Why do companies that clearly should leave the cloud keep waiting? For the employee in charge, the move saves the company money while putting the employee’s neck on the line. If the cloud fails, “everyone does it this way,” and the vendor takes the blame. Nobody gets fired for buying IBM or Oracle. Do nothing, make no visible mistake. Infrastructure departments are full of career survivors whose safest move is to outlast every risky decision. Cloud exit is therefore not a technical call. It is an executive one. Nothing moves until the boss makes the call.

---

## 8. The Cyber-Feudal Hierarchy

My cyber-feudal model has five ranks, ordered by infrastructure sovereignty:

**Cyber kings:** large technology companies and cloud providers.

**Cyber landlords:** they own the data center, hardware, and software stack. They have full sovereignty. For them, higher hardware prices mean asset appreciation, not higher costs. DHH is now sitting comfortably on a $19 million “estate.”

**Cyber knights, or free agents:** they rent IaaS from cloud providers but self-host the entire PaaS layer. The database, object store, and monitoring stack are theirs. A cloud is merely a replaceable resource supplier. If one gets expensive, they move to another, playing the cloud lords against one another.

**Cyber tenant farmers:** they use the cloud and its managed services but at least hold the line on standard interfaces: the PostgreSQL wire protocol and the S3 API. They can leave in principle, though for now they keep paying annual rent.

**Cyber serfs:** they are deeply bound to proprietary PaaS. Their data formats, APIs, and workflows exist only inside one cloud. They cannot even produce a migration plan. The contract is an indenture; they are chained to the estate and must swallow every price increase.

![The cyber-feudal hierarchy ranked by infrastructure sovereignty](cyber-feudalism.webp)

A full exit onto your own colocated hardware has a real threshold. It starts to make economic sense only when annual infrastructure spending reaches several million RMB. But **“hardware is too expensive” can stop you from becoming a landlord; it cannot stop you from becoming a knight or free agent.** Moving from serf to knight requires no hardware purchase. Keep renting cloud servers, disks, and bandwidth; bring only the PaaS layer under your own control. You may not be able to buy the land, but you can still tear up the contract. Buying back your freedom takes no capex—only understanding and resolve.

It is never too late to build the ability to self-host, even if you never buy a physical server. It may not save money immediately, but it preserves your exit option every day. And the exit option is what creates negotiating leverage.

---

## 9. Freedom Is Expensive, but It Has Never Been This Cheap

Full disclosure: Pigsty, the project I have spent the past several years building, is a free armory for would-be cyber knights.

The ready-to-run PostgreSQL distribution handles the database. [Silo](/en/db/long-live-silo/), the maintained MinIO-compatible fork, handles object storage. A complete VictoriaMetrics observability stack rounds it out. Together they bring up production-grade data infrastructure on bare Linux with no external dependencies. Everything is open source and free. Run it on your own hardware or rented cloud servers—the choice and the sovereignty remain yours. [Pigsty v4.5 shipped today](https://github.com/pgsty/pigsty/releases/tag/v4.5.0) with PostgreSQL 18.6, 575 extensions, and Silo replacing MinIO as the object store.

![Pigsty’s website and PostgreSQL infrastructure stack](pigsty-home.webp)

This is the road that brought me here, and I have walked it myself. I can give you the armor and gear for free, along with a clear manual; AI can now help you through the remaining installation and debugging. It still takes more thought than clicking through a cloud console. Freedom has never been free—but it has never been cheaper.

That is the choice: convenience or freedom. DHH made his and, as a bonus, turned it into the best trade of his life.

What about you?

![The road away from public cloud toward sovereign infrastructure](featured.webp)
