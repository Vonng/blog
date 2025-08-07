---
title: "Modb Interviews Industry Leaders - Feng Ruohang"
date: 2023-09-08
author: vonng
summary: Recently, a historic debate in the database industry has sparked heated discussion. The post-90s entrepreneur Feng Ruohang, known as the "ace debater" in the database community, has come into public view. Why did he participate in such technical debates that could potentially "start flame wars"? What are his views on the future development of databases? In this exclusive interview, we invite him to discuss his technical journey and hot topics in the database field!
---


> [Original WeChat Article](https://mp.weixin.qq.com/s/93QZBS694UQJRTLwHnStPQ) | 【[Modb Interviews Industry Leaders: Feng Ruohang](https://www.modb.pro/topic/569382)】

> **Introduction:** Recently, a historic debate in the database industry has sparked heated discussion. The post-90s entrepreneur Feng Ruohang, known as the "ace debater" in the database community, has come into public view. Why did he participate in such technical debates that could potentially "start flame wars"? What are his views on the future development of databases? In this exclusive interview, we invite him to discuss his technical journey and hot topics in the database field!


![](vonng.png)

**Founder of Pigsty Cloud Data - Feng Ruohang**

> **Bio:** Founder of Pigsty Cloud Data, author of the open-source RDS PG alternative - Pigsty. PostgreSQL expert and full-stack developer, open-source contributor, member of the PostgreSQL Chinese Community Technical Committee, Modb MVP; PostgreSQL ACE; formerly worked at Alibaba, Tantan, Apple. Translated works include "PostgreSQL Guide: Internal Exploration" and "Designing Data-Intensive Applications."



**—— The following is the complete interview ——**



------

**1. How did you get involved with the database industry? What suddenly inspired your entrepreneurial idea?**



**Feng Ruohang**: My interest was actually in AI during my studies - working on neural networks/cellular automata and such interesting projects. When I entered the industry, I was also an algorithm engineer. However, I quickly discovered that the core of AI is actually **data**, or rather - the entire information system revolves around and serves the database at its core. So, I started tinkering with databases.

When I first graduated, I worked at Alibaba/Umeng doing data development/data analysis, then worked my way through frontend and backend development. Later, when I became an architect leading projects and could make technology choices, I used this opportunity to try many different databases. Eventually, I discovered that **PostgreSQL** was an incredibly powerful database with unlimited potential, so I decided to go ALL IN on this direction.

Later I joined Tantan because they had one of the largest PostgreSQL deployments in China. This Nordic-style startup had great technical taste, and I learned many new tricks from a group of old-school Swedish engineers. Open-source projects like Linux/MySQL often originate from Northern Europe for a reason - the work atmosphere there is quite relaxed, allowing for extensive experimentation with new technologies. I began researching the PG kernel, translated two books, and finally started working on database management and control - which became [**Pigsty**](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485518&idx=1&sn=3d5f3c753facc829b2300a15df50d237&chksm=fe4b3d95c93cb4833b8e80433cff46a893f939154be60a2a24ee96598f96b32271301abfda1f&scene=21#wechat_redirect).

The original motivation for creating Pigsty was simple: to automate my work as a PostgreSQL DBA as much as possible, enhancing my ability to slack off - and it was quite successful in this regard. But I realized it could go much further - so I open-sourced it, aiming to become the open-source implementation of RDS for PostgreSQL.

A sufficiently useful open-source software can immediately improve the productivity of the PG community and global users, potentially even disrupting the existence of cloud RDS - Schumpeter's "creative destruction." Soon, external users began trying Pigsty and providing feedback, and many asked if I offered consulting and support services - end-user demand made me see the opportunity here, thus inspiring my entrepreneurial idea.

> Extended reading: 《[Post-90s, Quit Job to Start Business, Claims to Kill Cloud Databases](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485182&idx=1&sn=b06b9f2f4e6375fdfd255a85e0f3b89a&scene=21#wechat_redirect)》



------

**2. In 2022, Pigsty completed seed funding. As free open-source software, what is the business model?**



**Feng Ruohang**: What made me decide to start full-time entrepreneurship was the support from Miracle Plus: I casually applied and ended up being selected from over five thousand projects, securing seed funding. Such opportunities are extremely rare, allowing me to do what I truly want to do - something truly meaningful. Since angels are funding me, I have no reason not to go for it, right?

Starting a business certainly requires a business model, but Pigsty itself is completely free open-source software, so we don't make money by selling software products. Actually, I believe open source is anti-business model: how can putting software intellectual property into the public domain be considered a business model? **Open source is not a business model, but a global collaborative software development model**. However, software value is realized in its **usage** process, not in the **development** process.

Open source is not a business model, but providing services based on open-source software is a viable business model - the success of public clouds powerfully demonstrates this: simply running, maintaining, and managing open-source software well can capture most of the commercial value in the software lifecycle. We provide an open-source alternative to public cloud RDS for PostgreSQL - allowing users to quickly and self-sufficiently build database services comparable to or exceeding RDS anywhere, at one-tenth or even lower pure hardware costs than RDS.

Pigsty is to PostgreSQL what RedHat is to Linux. **Software is open-source and free, services are subscription-based and paid**. Open-source management software might automatically solve 80% of high-frequency daily operational tasks, but low-frequency yet critical complex issues still need experts as backup. We provide such services for users in need. Later, we will also try selling database monitoring SaaS in public cloud markets, as well as ready-to-use images and managed services.

> Extended reading: 《[Better Open-Source RDS Alternative: Pigsty](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485518&idx=1&sn=3d5f3c753facc829b2300a15df50d237&scene=21#wechat_redirect)》



------

**3. As a senior PG practitioner, if you were to describe PostgreSQL's competitive advantages with three keywords, what would they be?**



**Feng Ruohang: Open-source, Advanced, Extensible.**

"**Open-source**" distinguishes PostgreSQL from all commercial databases; "**Advanced**" distinguishes PostgreSQL from MySQL/NoSQL; "**Extensible**" is PostgreSQL's unique flavor, its one-of-a-kind characteristic. Open-source and advanced are PostgreSQL's fundamentals, directly reflected in its slogan: "**The World's Most Advanced Open Source Relational Database**." In the database field's three-kingdom scenario: Oracle is advanced, MySQL is open-source, while PostgreSQL is both advanced and open-source.

I've written extensively about the open-source and advanced aspects, so here I want to specifically mention **extensibility**. PostgreSQL's extensibility mechanism and plugin system make it no longer just a single-threaded evolving database kernel, but capable of countless parallel development branches, like quantum computing simultaneously exploring possibilities in various directions. PG doesn't miss any subdivided vertical field of data processing. Take the recent **vector database** boom - while other databases haven't even reacted, several related plugins immediately emerged in the PG ecosystem, seizing this ecological niche with lightning speed.

PostgreSQL is **a versatile full-stack database**, naturally HTAP, a hyper-converged database. A single component can cover most database needs for small and medium enterprises: competing with Oracle/MySQL in relational OLTP, with JSONB/GIN competing with MongoDB, PostGIS competing with geospatial databases, TimescaleDB competing with time-series/streaming databases, Citus competing with distributed/columnar/HTAP databases, full-text search competing with ElasticSearch, AGE/EdgeDB competing with graph databases, [pgvector](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247486079&idx=1&sn=61e3010f6d717f042e91e06f3c8eeb4d&chksm=fe4b3fa4c93cb6b2732e5caf3524d8c7ff8d53e34e9400800a06b1d655e39ec40f69fe82ea70&scene=21#wechat_redirect) competing with specialized [vector databases](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485589&idx=1&sn=931f2d794e9b8486f623f746db9f00cd&chksm=fe4b3d4ec93cb4584c9bb44b1f347189868b6c8367d8c3f8dd8703d1a906786a55c900c23761&scene=21#wechat_redirect). These amazing multi-modal capabilities stem from PG's extensibility.

Within a considerable scale, PostgreSQL can independently play the role of a multi-tool, one database serving as multiple components. Even more wonderfully, these extended capabilities can integrate together, achieving 1+1 far greater than 2 effects. Single data component selection can greatly reduce project **additional complexity**, saving substantial costs and development time. If there really is a technology that can satisfy your various data needs, then using it is the best choice, rather than trying to re-implement it with multiple components.

> Extended reading: 《[PostgreSQL: The World's Most Successful Database](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485216&idx=1&sn=1b59c7dda5f347145c2f39d2679a274d&scene=21#wechat_redirect)》



------

**4. Some time ago, the MySQL vs PG themed debate activity was truly a historic battle in the database industry. Some say "the quality of technology is not determined by debate." Why did you participate in such technical debate activities that could potentially "start flame wars"? What's the story behind this? What was your biggest takeaway after participating?**



**Feng Ruohang**: The quality of technology itself is indeed not determined by debate, but debate reveals the superiority of technology: public debate transforms "shared knowledge" into "public knowledge," building consensus - which is extremely important for the **ecological** development of open-source software.

In this debate, I believe several consensuses were established: In terms of momentum, PostgreSQL has surpassed MySQL in MySQL's fundamental strength of "popularity," becoming the world's most popular database; In terms of kinetic energy, PostgreSQL's functionality/product capabilities comprehensively overwhelm MySQL; even MySQL experts cannot deny these facts, so the conclusion is quite obvious - **PostgreSQL is the standard answer**.

Regarding flame wars, I don't think this is a bad thing - truth becomes clearer through debate, and the masses have sharp eyes. The stronger you are, the less you fear fighting; only those who can't handle it hang up the "no war" sign. Besides, everyone's time is precious. Rather than being a nice guy saying correct but useless platitudes, it's better to plainly state your views - you can't please everyone, and fence-sitting doesn't end well.

Technology in some sense is similar to religion - no matter how sophisticated your Buddhist teachings are, you need monks to preach, right? When ecological niches in technology collide, conflict is hard to avoid. You may not actively start wars, but when others come knocking, there must be someone in the community brave enough to stand up and face challenges.

My takeaway is: to have an exciting debate, you need opponents with comparable strength and character. A certain MySQL debater wasn't very decent, but as they say **one hater is worth ten fans**: if the opponent can only make long speeches questioning details like P5 architect levels but doesn't dare to do any hard product, technical, or business head-to-head competition, that's actually admitting that PostgreSQL and Pigsty are already flawless.

> Extended reading: 《[How to View the MySQL vs PGSQL Live Streaming Drama](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247486025&idx=1&sn=463029f58b41b5835780b6d2203be889&scene=21#wechat_redirect)》



------

**5. Your public account has multiple articles about "cloud exit." Why do you advocate for "cloud exit"?**



**Feng Ruohang**: With economic downturn, cost reduction and efficiency improvement have become the main theme. [Cloud exit](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485760&idx=1&sn=97096da1077a4fbb4c43452a3c4983c7&chksm=fe4b3c9bc93cb58d5724454f0210c13362393a4abb05f9b9fbc0146a9b188b4520f6211bc891&scene=21#wechat_redirect) to reduce expensive cloud expenses is also being put on the agenda by more and more companies.

I believe public clouds have their place - for very early-stage companies, or those that won't exist in two years; for companies that don't care about wasting money at all, or truly have extremely irregular loads with massive fluctuations; for companies needing overseas compliance, CDN and other services, public clouds are still very worthwhile service options.

But for the vast majority of companies that have grown and have **certain scale**, if you can amortize assets within a few years, you should really seriously re-examine this cloud fever. The benefits have been greatly exaggerated - running things on the cloud is usually as complex as doing it yourself, [**but ridiculously expensive**](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485745&idx=4&sn=93746ecea381afd8e2f9820447b09ec7&chksm=fe4b3ceac93cb5fc44f33ffff226747bc317854acbb3882aeb0d9a7e196eeb5df002d0e77275&scene=21#wechat_redirect). As an experienced customer, I've felt the pain of this butcher's knife and can calculate this account clearly, so I also suggest you carefully review your cloud bills.

In the past decade, hardware has continued to evolve at **Moore's Law** speed, IDC2.0 and resource clouds have provided cost-effective alternatives to public cloud resources, and the emergence of open-source software and open-source management scheduling software has made self-building capabilities readily available - cloud exit and self-building will have significant returns in cost, performance, security, and autonomy.

**Cloud exit has real practical benefits** - both for users themselves and for us. We advocate cloud exit concepts and provide practical implementation paths, along with key RDS database service self-building alternatives like Pigsty - we will pave the way in both technical solutions and ideological aspects for followers who agree with this conclusion.

**More importantly, there are ideological reasons** - we hope all users can own their own digital homes, rather than renting farms from tech giant cloud lords. Cloud-native/local cloud - this is also a movement against internet centralization and a counterattack against cyber landlord monopoly rent-seeking, letting the internet - this beautiful free haven and ideal land - go further.

> Extended reading: 《[Public Cloud Mudslide Collection - Deconstructing Public Clouds with Data](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485781&idx=1&sn=c139a77e53572cb538d3fd087eb80c8b&scene=21#wechat_redirect)》



------

**6. From a technical perspective, what stage of international databases are domestic databases currently at? Please envision what the competitive landscape of domestic databases will be like in 20-30 years? Which domestic databases do you currently favor?**



**Feng Ruohang**: **For OLTP database kernels led by Chinese companies, my personal judgment is that there's about a 10-year gap with world-leading levels**. For example, in global search engine trend charts, you can significantly observe that the wave trends of MySQL/PostgreSQL, the world's two most popular databases, have about a ten-year lag in China. For instance, globally MySQL's popularity decline trend started peaking and declining from 2004, but in China it suddenly became popular in 2014, then peaked and entered decline.

Many mainstream domestic database kernels are based on modified open-source database kernels. For example, OpenGauss forked from PostgreSQL 9.2 released in 2012, PolarDB referenced Aurora from 2014 and modified PG 11/14. There are also many domestic re-skinned and shell-modified versions based on PG 9.x, PG XC, PG XL. Considering PostgreSQL's own distance from Oracle, and various NewSQL's distance from Google Spanner, I think lagging world-leading levels by 5-15 years is a fair assessment.

If the above judgment holds, then we can use **current global** database competitive landscape to infer China's database competitive landscape ten years from now. I believe the milestone event in today's global database ecosystem is PostgreSQL surpassing MySQL to become the [most popular](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485685&idx=1&sn=688f6d6d0f4128d7f77d710f04ff9024&chksm=fe4b3d2ec93cb438665b7e0d554511674091b2e486a70b8a3eb7e2c7a53681fb9834a08cb3c3&scene=21#wechat_redirect) database, while maintaining huge growth momentum. I believe the database field is about to welcome its Linux moment: **PostgreSQL becomes the Linux kernel of the database field, and real competition will happen among PostgreSQL database distributions**.

I favor companies and products that fully utilize open-source kernel power, build distributions and service systems, and do valuable practical work. I don't favor products that choose hard forks or more extreme "self-developed kernels" - competing with global community developers often means the harder you try, the further you fall behind. Moreover, what the nation pursues for basic software autonomy and control is **operational autonomy and control** - maintaining stable operation of existing/incremental systems, not flashy "**self-development**."

**Pursuing self-development must consider vitality issues**. Mature open-source kernels already exist in the transactional database field. Pursuing so-called kernel self-development in basic software has almost no practical value for the nation and users. *Only when a team's functional development/problem-solving speed exceeds the global open-source community does kernel self-development become a meaningful choice*. Most basic software vendors claiming "self-development" are essentially shell-wrapping, re-skinning, and modifying open-source kernels with extremely limited vitality. Their degree of autonomy and control is not as good as directly using open-source database kernels/distributions - at least you won't be locked in by one company.

Low-quality software forks not only have no use value but also waste scarce software talent and market opportunity space, ultimately leading to disconnection between China's software industry and global industrial chains, creating huge negative externalities. The more national, the more global - monopoly protection can dominate domestically for a while, but over a 20-30 year scale, truly valuable domestic databases are still those that rely on hard strength, can carve out bloody paths in global markets, and earn foreign exchange/users/influence.

> Extended reading: 《[What Kind of Autonomy and Control Does Basic Software Need?](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247486061&idx=1&sn=a1452dfa864f702d40bf612839a4e9e4&scene=21#wechat_redirect)》



------

**7. The constant emergence of new technologies has given databases new vitality. What directions do you think databases will develop in the future?**



**Feng Ruohang**: **Better and faster, trouble-free and cost-effective. Or: quality, security, efficiency, cost.**

"Better" refers to quality/functionality, "faster" refers to performance/efficiency, "trouble-free" refers to usability/security, and "cost-effective" refers to price/complexity. For the "better" aspect, I favor **multi-modal** databases. For efficiency, I favor **software-hardware integration** and am pessimistic about **distributed NewSQL**. For trouble-free operation, I favor **declarative IaC and DBA large models** and am cautious about OLTP databases entering K8S. For cost-effectiveness, I favor **local-first/cloud-native** movements and am pessimistic about **public cloud PaaS/FinOPS**.

I believe OLTP databases belong to working memory, and the characteristic of working memory is rich functionality, small and fast. Even for very large business systems, the working set active at any moment won't be particularly large. A basic rule of thumb in OLTP system design is: ***if your problem scale can be solved within a single machine, don't mess with distributed databases***. TP database kernels should focus on multi-modality, enriching functionality - databases like PostgreSQL that can do everything, where a single component can cover almost all data needs, rather than distributed databases that support massive data but can only do CRUD.

For **efficiency**, optimizing for throughput/capacity is the wrong path - this is mainly hardware's job, and it's doing quite well: disk price-performance follows Moore's Law, improving three orders of magnitude in ten years, so that now almost no TP database can fully utilize the terrifying performance of Gen4/Gen5 PCI-e NVMe SSD single cards with 64T/million-level IOPS. Hardware revolution has brought centralized database capacity and throughput to new heights, making distributed (TP) databases meaningless in most scenarios, becoming a [false requirement](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485549&idx=1&sn=7c34439d82431129c57aba211202b5ca&chksm=fe4b3db6c93cb4a0423daf3a226e04867821e34ba3c6b5a8145bd5319c728fb08d63b2544a43&scene=21#wechat_redirect).

I believe existing database software still has great room for improvement in **usability** - DBMS kernels are still far from out-of-the-box, still requiring careful attention from DBA experts or sufficiently useful management software. A control system consists of perception, decision-making, and execution subsystems, so I think there will be three key directions: for **observability**, a powerful monitoring system is needed to provide data support; for **controllability**, declarative Infrastructure as Code is needed to simplify management complexity; and for **decision models**, artificial intelligence provides us with an extremely attractive vision: **LLM as DBA**.

Additionally, the definition of databases will also evolve: what we now call "databases" usually refers to "DBMS" - software for managing DBs. However, DBMS itself has now become an object managed by software - many operational tasks originally done by humans are gradually being completed by management software. Slowly, like operating systems, **the original DBMS becomes the so-called database kernel**, while databases begin to refer to database distributions and management software. I believe the future of databases will be similar to the present of operating systems: diverse distributions evolving around several open-source kernels.

> Extended reading: 《[Are Distributed Databases a False Requirement?](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485549&idx=1&sn=7c34439d82431129c57aba211202b5ca&scene=21#wechat_redirect)》/《[Technical Reflection - Database Source Investigation](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485576&idx=1&sn=d13184a3cbbf756ee0c2ed0d0a288d7a&scene=21#wechat_redirect)》



------

**8. As a database practitioner, whether in database kernel development or as a DBA, what do you think is most important for achieving success in your field?**



**Feng Ruohang: I think the most important thing is going with the flow.**

When fortune comes, heaven and earth all lend their force; when luck runs out, heroes lose their freedom - this speaks to going with the flow. What is the current trend in the database field? PostgreSQL is about to welcome its Linux moment, but there hasn't yet emerged dominant distributions like Ubuntu, RedHat, SUSE. The main contradiction in today's database field is no longer the lack of better, more powerful new kernels, but the **extreme shortage of capability to use and manage existing database kernels well** - PostgreSQL is already a sufficiently perfect and useful engine, but users need ready-to-drive complete cars. This is a historic opportunity for DBAs.

Database kernel developers are experts in the development field, while DBAs are experts in application and management fields. There are no fresh graduate DBAs - real open-source database DBAs are all forged from senior development/operations piles with countless real money and silver failures. The best drivers are race car drivers, not car factory engineers; the best shooters are snipers, not gun designers; the best performers are pianists, not piano tuners. For using/managing databases well, DBMS/database kernel vendors are usually powerless - only senior first-party users and real-world complex scenarios can hone this experience. In database distributions/services, DBAs have more authority than database kernel developers.

Going with the flow, the key is "**taking action**." Wisdom helps you recognize the situation, but courage enables action. Wisdom is an important quality that helps you see through fog, understand future paths, and guide correct choices. But courage is the scarcest quality: whether it's the courage to speak truth, challenge authority, break the status quo, or go all-in, those who personally enter the game are always very few. To achieve something significant, both courage and wisdom are indispensable.

> Extended reading: [Refuting "Why You Shouldn't Hire DBAs Again"](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485335&idx=1&sn=c37c2ee787fe4fc1b6909500c5f05583&scene=21#wechat_redirect)



------

**9. Some say you are "the tech world's comedian, a tech fanatic among comedians." How do you view this assessment?**



**Feng Ruohang**: I think this assessment is quite good. I greatly admire Linus and Jobs - the former is a top tech fanatic (Hacker), the latter is a top comedian (Story Teller), and I'm naturally influenced by my idols, developing skills in both directions.

Designing software systems and transforming open-source ecosystems is **interest and entertainment** for me, not work for making a living. As Linus's autobiography "Just for Fun" says: "survival, order, entertainment." Although I was born relatively late and unlikely to create projects like Linux and PostgreSQL, making a Debian/RedHat-style PostgreSQL distribution is still possible. This work, aside from practical and economic value, is itself a form of ultimate entertainment like "creation."

Stories have the power to unite hearts and build consensus - human society/nations are all united by stories. Telling good stories is a rare ability, and Jobs was definitely a top master in this regard. To achieve successful presentations, carefully designing story lines that fit cognitive structures is very important, and extensive practice is indispensable. For example, many articles I've written in my public account are written to presentation standards - this is actually deliberate storytelling ability training.

Confucius said: "If substance exceeds refinement, one becomes crude; if refinement exceeds substance, one becomes pedantic. Only when substance and refinement are balanced does one become a gentleman." High technology, solid content - both high and solid are the hard truth.

> Extended reading: 《[Pigsty Pitch in Three Minutes](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485126&idx=1&sn=455f35f378e1c252aa52ceff3ebef976&scene=21#wechat_redirect)》



------

**10. Regarding PostgreSQL database, how do you recommend learning it?**



**Feng Ruohang**: I recommend Learn by Doing.

The principle of learning databases is learning for practical use. Only **practice** can bring deep understanding of problems; only by first knowing the what can you have conditions to know the why. Textbooks and books can be skimmed through once, then go directly to database documentation and get hands-on to build something. Having real requirement scenarios is naturally best; without conditions, the best approach is **creating scenarios yourself and discovering requirements yourself**.

For example, you could build a knowledge base semantic search: this would use [pgvector](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485589&idx=1&sn=931f2d794e9b8486f623f746db9f00cd&chksm=fe4b3d4ec93cb4584c9bb44b1f347189868b6c8367d8c3f8dd8703d1a906786a55c900c23761&scene=21#wechat_redirect)'s vector capabilities; if you want to make a photo check-in app, you could utilize [PostGIS](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247483688&idx=1&sn=0b08c7c47e28ceae77f89a78d38b029f&chksm=fe4b34f3c93cbde5bde0a59c705f7afb5426fb598285c2b69870e6f72ceaaa69afa6d8a754c2&scene=21#wechat_redirect) geographic spatial features; for [global meteorological data analysis](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485647&idx=1&sn=1ca65ee357516a06dca7ec13fa679f9a&chksm=fe4b3d14c93cb402b7ad8ba8f431d556503602a07994969e4c3df0c7518ee4c3a09313bb0fb6&scene=21#wechat_redirect), TimescaleDB functionality could help. For [IP geolocation queries](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247483692&idx=1&sn=0cdb3609daf22fa2a5614d280da96b66&chksm=fe4b34f7c93cbde13f17e410999cfb0f6ee935c54452db7cc3141b332409d6c565656ef876b2&scene=21#wechat_redirect), you'd use custom range types and operator classes; for product/crowd tag selection applications, arrays/JSONB/inverted GIN indexes would be useful. The great way is simple - cleverly using PostgreSQL features, development can achieve one SQL line worth a thousand words.

For operations management, the best learning method is referencing industry architectural best practices. For example, we've completely open-sourced the architecture we use in large-scale production environments - that's Pigsty. Studying Pigsty, you can learn host parameter tuning, master-slave setup, high availability configuration and automatic failover, connection pool management, backup and recovery details, load balancer usage and traffic management, read-write separation, database and table partitioning, etc. Pigsty's unique monitoring system provides a complete PostgreSQL cognitive framework, truly the ultimate weapon for studying database performance issues and troubleshooting.

For self-learning beginners, besides official documentation, I recommend "PostgreSQL from Novice to Expert" and "PostgreSQL in Action." Of course, as Xunzi said: "I once thought all day long, but it's not as good as what I learned in a moment." Having a teacher guide you is different from self-learning. The PostgreSQL Chinese Community has weekly public training and sharing sessions, and we also provide professional PostgreSQL training (application, operations, principles) for users in need.

Of course, interest is the best teacher. If you can understand "**why**" you want to learn PostgreSQL, I believe "**how to do it**" definitely won't stump you.

> Extended reading: 《[Why Study Database Principles?](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247483673&idx=1&sn=2a895a6f6e4b3e882395203757ec4e60&scene=21#wechat_redirect)》