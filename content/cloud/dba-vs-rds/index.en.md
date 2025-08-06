---
title: Will DBAs Be Eliminated by Cloud?
date: 2024-02-02
hero: /hero/dba-vs-rds.jpg
author: |
  [Feng Ruohang](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [WeChat](https://mp.weixin.qq.com/s/W1hwbl3qmjC4Dcmadc8uSg)
summary: >
  Two days ago, the ninth episode of Open Source Talks had the theme "Will DBAs Be Eliminated by Cloud?" As the host, I restrained myself from jumping into the debate throughout, so I'm writing this article to discuss this question: Will DBAs be eliminated by cloud?  
tags: [cloud-exit,DBA,RDS]
---

Two days ago, the ninth episode of Open Source Talks had the theme "[Will DBAs Be Eliminated by Cloud?](https://mp.weixin.qq.com/s/T4waTPvcSRdCv8pCl4MdOw)" As the host, I restrained myself from jumping into the debate throughout, so I'm writing this article to discuss this question: Will DBAs be eliminated by cloud?

[![](featured.jpg)](https://mp.weixin.qq.com/s/W1hwbl3qmjC4Dcmadc8uSg)

------

## DBAs Help Users Use Databases Well

Many places need DBAs: terrible schema design, horrific query performance, backups of unknown utility; and so on. Unfortunately, among people working in software, few understand what a DBA is. Being a DBA means engaging in endless battles against the entropy created by developers.

DBA - Database Administrator - also formerly called database coordinator or database programmer. A DBA is a broad role spanning development and operations teams, involving DA, SA, Dev, Ops, and SRE responsibilities, handling various data and database-related issues: setting management policies and operational standards, planning software and hardware architecture, coordinating and managing databases, validating table schema design, optimizing SQL queries, analyzing execution plans, and even handling emergency failures and data recovery.

Many companies hire DBAs. Traditional DBAs are similar to Cobol programmers - beyond tech companies/startups: those less fancy-sounding manufacturing industries, banks, insurance, securities, and numerous government and military departments running local software also heavily use these relational databases. The cost spent on commercial database software licenses alone might reach six or seven figures, plus similar hardware costs and service subscription costs. If a company has already invested tens of millions on database software and hardware, spending more money to hire dedicated experts to care for these expensive and complex databases becomes natural - these experts are traditional DBAs.

Then with the rise of open source databases like PostgreSQL/MySQL, these companies had a new choice: using database software without software licensing fees, and they began (irrationally) to stop paying for database experts: database maintenance work became an implicit subsidiary responsibility of development and operations, and these two types of people usually: neither excel at, nor like, nor care about database maintenance. Only when the company grows large enough or suffers enough pain do some Dev/Ops develop corresponding capabilities and become DBAs - though this is quite rare, and these are today's protagonists - open source database DBAs.

------

## The Ability to Use Databases Well is Scarce

The core element for cultivating open source database DBAs is **scenarios**, and scenarios with sufficient complexity and scale are extremely scarce, usually only available to top-tier clients. Just like domestic MySQL DBAs mainly come from heavy MySQL users like Taobao and other top internet companies. Excellent PostgreSQL DBAs basically all come from companies that use PG at scale like Qunar, Ping An Bank, and Tantan. The sources of top-tier open source database DBAs are extremely limited, basically being operations/development experts proficient in databases at top-tier clients, forged through real money and major incidents with complex scenario-building experience.

Taking Chinese PostgreSQL DBAs as an example, based on pure technical article circulation readership, the circle size is roughly a thousand people; but DBAs who can build database systems exceeding RDS standards converge to dozens; those who can build better RDS and even export best practices for external replication are rare as phoenix feathers - countable on one hand.

So the main contradiction in today's database field isn't the lack of better and more powerful new kernels, but the **extreme scarcity of ability to use and manage existing database kernels well** - **too many databases, too few drivers!** Database kernels have developed for decades, and minor patches to kernels have diminishing marginal returns. With mature open source database kernel engines like PostgreSQL emerging, selling commercial databases becomes a bad business - open source databases don't need expensive software licensing fees, so **DBAs** who can use these free **open source databases** well become the biggest bottleneck and cost.

At this stage, advanced experience is "monopolized" by a few top experts. In fact, this is exactly the real "business model" of open source - creating high-paying technical expert positions. However, this also creates a new opportunity - commercial database products can no longer form monopolies due to open source alternatives, but DBA experts who can use open source databases well are countable, and monopolizing a few experts is much simpler than defeating open source databases. Can't monopolize database products? Then monopolize the ability to use them well!

| Stage | Name | Characteristics | "Business Model" |
|-------|------|----------------|------------------|
| Stage 1 | Commercial Databases | Commercial database software monopolized database product supply. | Expensive software licensing |
| Stage 2 | Open Source Databases | Open source broke commercial database monopoly,<br />but technical monopoly is in the hands of a few top open source experts. | High-paying expert positions |
| Stage 3 | Cloud Databases | Cloud broke the technical monopoly of open source experts<br />but formed monopoly on the ability to use databases well | Management software rental |
| Stage 4 | "Cloud Native?" | Open source management software broke cloud management software monopoly<br />The ability to use databases well spread to thousands of households | Consulting and insurance backup |

So, recruiting experts who can use open source databases well as much as possible, creating a shared expert pool allowing scarce senior DBAs to be time-shared, and packaging this with DBA experience-precipitated management software as rental services, becomes a very profitable business model - and cloud database RDS does exactly this, making tons of money.

Cloud databases use open source free kernels, so the core capability cloud databases provide is the same as DBAs - **the ability to help users use databases well!** Their real competitors aren't other commercial database kernels or open source database kernels, but DBAs - especially mid-to-lower tier DBAs. This is like taxi companies wanting to replace not car manufacturers, but full-time drivers.

------

## DBA Work and Automated Management

Besides DBA manpower, what other ways can provide the ability to use databases well? We need to first look at DBA work patterns.

DBA work is mainly divided into **construction** and **maintenance** phases in time. The intensive construction phase in the first few months is relatively hard, requiring building mature technical architecture and management systems; when automation construction is completed and enters the maintenance phase - DBA work becomes much easier.

|          |     Construction Phase      |                Maintenance Phase                 |
|:--------:|:---------------------------:|:-----------------------------------------------:|
|   Management Layer    |  Database selection, system building   |     Database modeling, query design, personnel training, SOP accumulation, development conventions      |
|   Application Layer    |   Architecture design, service access   | SQL review / SQL changes / SQL optimization / sharding / data recovery |
| **Database Layer** | Infrastructure building, database deployment |  Backup recovery / monitoring alerts / security compliance / version upgrades / parameter tuning   |
|  OS Layer   |   OS tuning, kernel parameters   |               Storage space management                |
|   Hardware Layer    |   Testing selection, driver adaptation   |               (Hardware replacement)                |

System building isn't a one-time purchase but an evolutionary process where proficiency grows logarithmically with time. Interested and dedicated DBAs continuously pursue higher levels of automation construction, condensing the construction process into replicable experience, documentation, processes, scripts, tools, solutions, platforms, **management software**. Management software might be the ultimate form of DBA experience precipitation - using software to replace yourself doing DBA work.

The higher the automation level of **management systems**, the less maintenance manpower needed during maintenance phases. But this also requires higher DBA proficiency and longer construction investment and time cycles. So at some balance point, either automation hits the DBA capability ceiling, or becomes so advanced it threatens DBA job security, construction evolution pauses and DBAs enter "tea and newspaper reading" continuous maintenance status.

Systems in maintenance status have significantly reduced [intellectual bandwidth requirements](https://mp.weixin.qq.com/s/FIOB_Oqefx1oez1iu7AGGg). In well-built system architectures, if it's just routine, standardized work, lower-level DBAs can maintain it, and the time demand for senior DBAs drops dramatically - entering a "train soldiers for a thousand days, use them for a moment" "idle" state, only when emergency failures and difficult problems occur can these database expert veterans demonstrate their value again.

|    Stage     |                  Capability Composition                  |
|:-----------:|:--------------------------------------:|
| Regular User - Construction Start | **100%** Expert Manpower |
| Regular User - Maintenance Phase |       **30%** Management + **70%** Expert Manpower        |
| Top User - Maintenance Phase | **90%** Management + **9%** Operations Manpower + **1%** Expert Manpower |

So DBA used to be a very good position - after the entrepreneurial construction phase, you could rest on your laurels and enjoy the efficiency dividends brought by construction achievements. For example, top-tier clients' DBAs after long-term construction might have 90% of work content highly automated - even hardware failures are handled by high-availability management self-healing. DBAs only need 10% of time for firefighting/optimization/guidance/management, so the remaining 90% of time can be freely allocated: continue improving management software for compound returns, or study kernel source code and translate books, or simply like DBA predecessors - "librarians" - drink tea and read newspapers in libraries, very comfortable.

However, DBAs' comfortable life was disrupted by cloud database models. First, cloud providers take ready-built management software and replicate it in batches, eliminating repetitive construction work in database building phases. Second, if there's no construction phase, only maintenance phase, and maintenance work only needs 10% of DBA time, rather than spending **90%** of time slacking off, there will always be workaholics choosing to be time management masters and work 10 jobs simultaneously. Cloud providers' database experts through management and shared DBAs made this rare leisurely IT position competitive too.

------

## Cloud Database Models and New Challenges

Why do cloud databases threaten DBAs? To explain this, we need to discuss cloud database RDS user value.

**The core value of cloud databases is "agility" and "backup"**. Things like "cheap," "simple," "elastic," "secure," "reliable" aren't actually core and may not even be true. So-called "**agility**" - translated means saving users several months of construction phase work, reaching maintenance phase in one step. So-called "**backup**" means when users truly encounter difficult problems needing top-tier DBAs' high intellectual bandwidth, cloud providers provide support through tickets - at least you can actually get someone to manage it.

The core technical barrier of cloud databases is **management software precipitated from senior DBA experience**. Most DBAs, including many top DBAs - although they're experts in database management, lack development capabilities - the ability to precipitate their domain knowledge and experience into replicable software products. Therefore, they usually need a development team's assistance to transform senior DBA domain knowledge into business software.

This management software precipitated from DBA experience becomes the core production material and [money tree](https://mp.weixin.qq.com/s/LefEAXTcBH-KBJNhXNoc7A) of cloud databases. Hardware resources costing 20 yuan per core·month, wrapped with management software, can be sold for 300~400 (Aliyun) or even 800~1300 (AWS) - dozens of times the sky-high price. However, it's precisely RDS's linear hardware resource binding pricing strategy that gives some mid-level DBAs breathing room - when RDS scale reaches 100+ cores, hiring a DBA for self-building reaches the ROI turning point.

Another benefit of management software replacing DBA work is that DBAs can add leverage! For example, if your management software can automate 90% of DBA work, then the same work only needs 10% of a DBA's time, using one DBA as ten - so the DBA multiplier is 10. If your management software is simple and easy to use with low barriers, letting regular operations/development play DBA cosplay and self-serve complete 9% of this 10% work, then only 1% of expert time is needed - 1 DBA can be used as 100! Of course, if a DBA large model appears in the future and replaces 0.9% of this remaining 1% work, the DBA multiplier can be amplified to 1000 times!

|             |                    Management Software                    | DBA Multiplier |
|-------------|:------------------------------------------:|:-----:|
| Regular User - Construction Start | **100%** DBA Manpower |   1   |
| Regular User - Maintenance Phase |           30% Management + **70%** DBA Manpower            | 1.43  |
| Cloud Database |       60% Management + 38% Manpower + **2%** DBA Manpower       |  50   |
| Top User - Maintenance Phase |       90% Management + 9% Manpower + **1%** DBA Manpower        |  100  |
| Future State Imagination | 95% Management + 4% Large Model + 0.9% Manpower + **0.1%** DBA Manpower | 1000  |

So cloud providers' model is similar to banks. There's so-called "deposit reserve ratio" and "DBA multiplier" - ten or even hundreds of jars with one lid. Fully releasing (exploiting) the idle time and surplus value of DBA veterans, using lower manpower costs to provide "backup" services for more customers. This solved the problem of very scarce "ability to use databases well" and made tons of money.

If I were to objectively evaluate cloud database service quality on a 100-point scale: top DBA self-building can reach 95~100 points, excellent DBA self-building can reach around 80 points; cloud databases are about 70 points. But mid-level DBA crude self-building is about 50-60 points, junior DBA crude self-building is about 30-40 points, operations part-time crude self-building might be only teens. Top-tier clients indeed look down on cloud databases' "big pot rice," but for mid-tier users, this is amazing - they want big pot rice, and compared to purchasing expensive commercial databases and hiring scarce database veterans, RDS truly deserves "good quality and low price."

First: Cloud databases are ready-to-eat meals, directly consumable without construction phases; Second: Cloud databases are cheap 70% correct qualified products, while quite a few junior-mid level DBAs' crude self-building can't reach RDS levels after months; Third: Cloud databases are standard components, reducing uncertainty and irreplaceability from DBAs' free-style creativity; Fourth: Cloud databases provide shared experts, "backing up" other DBA needs and solving concerns about being unable to get help when problems arise or encountering incompetent people. So for smaller-scale, average-level client users, cloud databases are very attractive compared to hiring and training junior-mid level DBAs for self-building.

Cloud database services' impact on DBAs is structural. Extremely scarce top DBAs aren't affected and will always be sought after by cloud providers. But mid-tier and below DBAs, or DBAs whose self-building doesn't reach 70 points, will directly face ecological niche competition from cloud database services. For the DBA industry, this isn't good - because senior DBAs all grow from junior and mid-level DBAs. If the soil for nurturing these junior-mid level DBAs - small and medium companies' database application scenarios - are monopolized and intercepted by cloud providers, then this industry pyramid will be cut in half, top DBA increments will be cut off, and existing stock will be eroded, eventually becoming rootless trees.

------

## Breaking Cloud Database Core Barriers

Will cloud databases be the future? Will cloud databases "replace horse carriages with cars" and eliminate DBAs? I don't think so, because where there's force, there's reaction. Progressive DBAs will arm themselves with tools, return to center stage and compete with RDS.

For DBAs to compete with cloud databases, Luddite resistance to technological progress won't work. They should use "you're strong, I'm stronger" methods to improve their competitiveness relative to cloud databases. To achieve this, DBAs need to provide higher value than RDS at lower cost. To do this, I'm not worried about DBAs' professional capabilities in quality, security, reliability - the key is "agility" and "backup" issues:

First, shorten several months of construction cycles to days or even hours, achieving "**agility**".

Second, when difficult problems truly arise, being able to get top DBAs for "**backup**".

Solving the former requires **management software**, solving the latter requires DBA veterans. The former's urgency far exceeds the latter - well-built systems might run for years without encountering problems needing "backup," and making every regular DBA become a veteran isn't realistic. How to agilely, low-cost spin up a 70+ point database service system is the core issue for DBAs responding to RDS challenges.

This is exactly my initial motivation for starting the [**Pigsty**](https://mp.weixin.qq.com/s/-E_-HZ7LvOze5lmzy3QbQA) open source project - providing a completely open source free, higher quality RDS PG alternative. Letting regular DBA/development/operations personnel build and deliver 80+ point local RDS services with the same agility! Completely solving the first problem. My business model is consulting and services, providing commercial support and final backup for these difficult problems, solving the second problem.

A good enough open source database management software will directly disrupt cloud database business models. For the simplest example, you can completely use equally elastic cloud servers ECS and cloud disks ESSD with open source management to self-build RDS services. Without losing the "elasticity" and "agility" and various RDS benefits that cloud touts, without needing additional manpower, immediately saving 60%~90% varying "pure RDS premiums." If using self-owned servers for pure self-building, the [cost reduction and efficiency improvement level](https://mp.weixin.qq.com/s/1OSRcBfd58s0tgZTUZHB9g) might exceed most users' cognition.

Pigsty will reset cloud database service baseline levels. All PG management software with quality inferior to it will gradually shrink to zero value. This is nuclear proliferation in the database management field, open source dumping from the moral high ground. Just like when open source databases overturned commercial database tables, only this time it happens in another dimension - management software. Pigsty immediately equips all PG DBAs with magic wands for instantly completing high-level database service construction and delivery, also letting more development/operations play PG DBA roles, instantly mass-producing many junior DBAs.

Of course, as open source management software, Pigsty indeed replaces a large portion of DBA work content like cloud database management, especially operational parts. But unlike cloud databases, it's controlled by DBAs themselves, owned, controlled, and used by DBAs, rather than only being able to rent from cloud computing lords and "replace" DBAs. Stronger productivity bringing leisure time dividends and DBA multiplier leverage will directly spread to every practitioner's hands. This is my response as a top DBA to RDS challenges.

------

## How to Face Cloud Database Impact

For the vast majority of junior-mid level DBAs, I think the best way to respond to cloud database challenges is to immediately abandon long-cycle, mixed-result crude self-building attempts and directly embrace mature open source management software, quickly amplifying your competitiveness relative to cloud databases - this part is completely open source free, production materials and capabilities in your own hands. If you need difficult problem backup, I'm very happy to provide support, consulting, and Q&A at extremely competitive prices compared to cloud databases.

Please don't ask me anymore: How to do PostgreSQL high availability? How to handle PITR backup recovery? How to build observability and monitoring systems? How to use configuration IaC to manage hundreds of database clusters? How to configure and manage connection pools? How to do load balancing and service access? How to compile, distribute, and package hundreds of extension plugins? How to tune host parameters? How to do online/offline/scaling/shrinking/rolling upgrades/data migration? These problems you'll actually encounter, which I've encountered before, I've already provided tooled best practices and version answers in Pigsty, with DBA SOP manuals, letting newbies quickly get started with DBA cosplay.

------

For top DBAs and peers, I advocate jointly building open source shared management software and providing professional database services based on this. Rather than you building one cloud management system, me building another, investing massive development manpower in low-level, repetitive construction, better to unite and build public open source management, creating truly world-influential open source project brands in Chinese communities. Pigsty is a very good candidate open source project - currently, it's already [the top-ranked project among Chinese-led PostgreSQL ecosystem open source projects](https://mp.weixin.qq.com/s/79_PnX-a5iSfDMgz_VUx5A). It might have a chance to become the Debian and Ubuntu of the PostgreSQL world, but this depends on every contributor and every user.

I don't make money from Pigsty either. Like many database service companies, I rely on providing professional consulting and services. This might not be the "Scale to the Moon" story capital markets like to hear, but it indeed solves users' pain points. Can I, no matter how awesome, work 200 PG DBA jobs? No! But Pigsty tool can let every PG DBA veteran add such leverage, provide truly valuable consulting and services to society, thus defeating cloud databases!

------

For example, Percona, which provides MySQL expert services, their PostgreSQL department head Umair Shahid keenly saw this trend. He left Percona and started his own company Stormatics to provide professional PostgreSQL services. He didn't "develop" another PG cloud database management platform but directly uses Pigsty for system delivery. Similarly, some Italian, American, and domestic database companies use Pigsty to deliver PostgreSQL services. I warmly welcome this and am willing to provide support and help.

Database product models are dying, while database consulting and expert service models are flourishing. Using databases well is a high-threshold field. Even strong as [cloud exit pioneer DHH](https://mp.weixin.qq.com/s/CicctyvV1xk5B-AsKfzPjw), the penny-pinching king still has an expense for purchasing Percona MySQL expert services to let professionals solve professional problems. Rather than selling dignity to package, reskin, shell, and brag about creating "new database kernel products" with minimal utility (Minor PG forks), better to honestly provide truly valuable database expert consulting and services for users.

------

Currently, server hardware resources are very cheap, database kernel software is open source free and awesome enough. Now, if management software is no longer monopolized by cloud providers, then the core element for providing complete database services is only the **expert capability** for backup! AI and GPT's emergence further amplifies individual database experts' leverage multipliers to an astonishing degree.

So many cloud provider internal database veterans keenly perceive this trend and choose to leave cloud providers to go solo! For example, those who left Alibaba Cloud include Teacher Tang Cheng's Chengxu Technology, Teacher Cao Wei's Kubeblocks, Teacher Ye Zhengsheng's NineData, etc. So even cloud database provider internal teams aren't monolithic. Teams are also undergoing dramatic changes, withering and bleeding, with people's hearts stirring.

I believe the future world won't be one monopolized by cloud databases. Each RDS management quality level has stagnated long-term, reaching the capability ceiling allowed by scenario soil. But productivity tools precipitated from top DBA experience go further, letting many mid-tier DBAs regain fighting capability against RDS. Progressive DBAs will arm themselves with tools and compete with RDS on the same stage. I'm willing to uphold justice, carry the banner of cloud exit and self-build alternatives, develop these management software and tools and spread them to every DBA's hands, helping DBAs win the battle against cloud databases!