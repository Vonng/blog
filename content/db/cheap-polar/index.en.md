---
title: "The $20 Brother PolarDB: What Should Databases Actually Cost?"
date: 2024-04-25
author: vonng
summary: >
  Today we discuss the fair pricing of commercial databases, open-source databases, cloud databases, and domestic Chinese databases.
series: ["Xinchang Localization"]
series_order: 5
tags: [Database, Domestic-Database]
---

> [WeChat Public Account](https://mp.weixin.qq.com/s/AqcYpOgVj91JnkB1B3s4sA)

Yesterday, a bidding news attracted attention and heated discussion: "The IT industry is broken... 16.1 million dollar contract... 2.9 million (won)... maintenance fee 0.01 yuan... PolarDB unit price 130 yuan". When I first saw this title, I wasn't particularly surprised, because I'm very familiar with the unit price of PolarDB database on the cloud - the price per vCPU per month is around ¥250-400. Considering that big customers can negotiate 20-30% discounts, that's about 50-120 yuan, so the "unit price" of 130 yuan isn't an outrageous quote.

So when I saw that the billing unit for PolarDB's 130 yuan unit price was "node" - not the commonly used "per vCPU monthly" unit price on the cloud, but offline private deployment database per physical machine node license unit price - I couldn't hold back anymore. This "unit price" is pretty ridiculous.

PolarDB V2.0 isn't some modified rebranded knock-off database - it's a legitimate domestic Xinchang database that has passed national certification twice. This kind of business that Oracle can sell for hundreds of millions is now being sold at the cabbage price of two thousand yuan total. How do the domestic database vendors selling tens of thousands per node feel about this? Has China's IT industry rolled to this stage?

Today let's talk about what databases should actually cost.

## What Do Commercial Databases Cost?

Database management system software has been (and still is) a very profitable business.

As the benchmark for commercial database software, [Oracle database licensing](https://www.oracle.com/a/ocom/docs/corporate/pricing/technology-price-list-070617.pdf) costs about Enterprise + RAC ($47,500/4vCPU + $23,000/4vCPU), roughly 500,000 RMB. After the one-time license purchase, there's also an annual 22% **service fee**.

But note that Oracle's "billing unit" above is Processor, which equals two Intel physical cores, or 4 thread vCPU virtual cores. So if we convert to the commonly used unit vCPU·month today, the price per vCPU core is 127k one-time license + 28k/year service fee.

> 1 Oracle Processor = 2 Intel Core = 4 vCPU Thread

Assuming you have a 64-core server running Oracle database, the license cost would be 8 million yuan, plus 2 million yuan annual service fee. By the way, the so-called service means you submit a ticket when you have problems, and Oracle people answer your questions. If you want someone to come on-site for service, there are separate consulting fees.

Of course, as everyone knows, Oracle uses Paper License - you can download and use it freely (piracy). Of course, Oracle's strongest department - legal - is no joke. For small and medium users, it hasn't caught up yet - you can first buy a 500k protection fee license, and this matter temporarily passes. But when you get fat, these protection fees owed won't be reduced by a penny.

> https://www.oracle.com/a/ocom/docs/corporate/pricing/technology-price-list-070617.pdf

Overall, the traditional commercial database pricing model is like this: charge by processor, with unit prices in the hundreds of thousands.

> Oracle: y = a * x + b, a = 28K, b = 127K

Of course, in my opinion, this business model is outdated - hardware is completely different now: processors back then were just a few cores, modern physical machines easily have hundreds of cores; more importantly, software now has open-source alternatives: open-source PostgreSQL and ~~MySQL~~ are already good enough.

## What Do Open-Source Databases Cost?

Oracle CEO Larry said: "Once open-source alternatives become good enough, competing with them is crazy and stupid." And now, Oracle's open-source alternative "PostgreSQL" has far exceeded "good enough" - in fact, just like Linux swept the operating system field back then, it's frantically devouring the entire database world and has recently subtly shouted the slogan "overthrow Oracle".

**Open-source databases** represented by **PostgreSQL** / **MySQL** can save software **license** costs. That is, you can run as many cores as you want, and the software cost becomes zero. In fact, this is one of the core reasons for the prosperity of the internet: open-source software like Linux, MySQL, PG, Apache, PHP made the marginal cost of building websites infinitely close to zero.

However, this isn't a viable option for most companies and enterprises. Because experts who can truly master open-source databases are much rarer than commercial database DBAs, and most of these experts are concentrated in internet companies with good benefits and high salaries. For many small and medium companies, first: it's hard to find and recognize the right people; second: they may not be able to afford it, and experts may not be willing to go there.

The real "business model" of open source is actually: free open-source software attracts users, user demand creates open-source expert positions, open-source software experts as enterprise agents draw power from the open-source world's public software pool and produce better open-source software as prosumers. **So in the open-source model, software doesn't sell for money - what's sold is essentially expert services.**

Buying RHEL, EDB nominally buys "operating system", "database", but essentially buys expert services, more specifically consulting and man-days. The cost of using open-source databases is essentially human cost. How much open-source databases sell for depends on how much experts should sell for. Some people think using open source doesn't cost a penny - this is pure fantasy. Experts who can use open-source databases to commercial database levels are really not cheap.

Expert pricing depends on expert quality level and supply-demand relationship. There's a simple and reliable anchoring method: benchmark against Oracle/SQL Server's annual 20% "support service" fee, which is actually the market pricing for expert services. We can see companies like EDB and Fujitsu price according to this logic.

For example, [Fujitsu's PG service](https://swc.saas.ibm.com/en-us/redhat-marketplace/products/fujitsu-enterprise-postgres/pricing) support costs $3,200/physical Core, which is 11k RMB/vCPU/year. EDB's price isn't public, but I know their unit price is about double Fujitsu's, roughly close to Oracle's annual 20% support fee.

> PostgreSQL: y = a * vCPU, a = 11K ~ 22K

Of course, experts can be rented from professional service companies or directly from the market - as long as your scale is large enough, buying out experts directly is always more cost-effective (for example, getting two experts with million-yuan annual salaries = 2000K / 20K = 100 vCPU). You can directly convert the database cost model from linear growth with vCPU to logarithmic growth or fixed constant - provided you can actually find them and they're willing. But even so, most small and medium companies are unwilling or unable to pay this minimum scale startup cost, so cloud databases emerged.

## What Do Cloud Databases Cost?

Whether hiring experts or purchasing professional database services, there's a startup cost and minimum scale - starting from one year in time, generally several cores minimum in space, with startup costs in the range of hundreds of thousands to millions. Cloud databases solve this problem: they purchase experts wholesale, then break them down for retail, excellently solving the startup needs of small and medium enterprises.

Cloud database billing models are consistent with commercial databases/open-source service support, using CPU scale binding. The pricing model is:

> y = a * vCPU

This `a` is the monthly unit price per core for cloud databases. Internationally, cloud database unit prices fluctuate around $150-250/vCPU·month, plus storage costs, so this `a` is roughly in the 13K-21K range. This is basically in the same range as service support provided by open-source database companies. Considering that cloud vendors like AWS also provide hardware, smaller startup scale, more convenience, and don't pick customers, they have significant competitive advantages in small to medium scales.

Of course, domestic cloud vendors are more competitive, and the average level of experts is also somewhat behind international peers, so cloud databases are sold cheaper. For example: domestically, taking Alibaba-Cloud as an example, RDS/PolarDB unit prices fluctuate around 250-400 RMB/vCPU·month. So the `a` here is 3K-5K.

Overall, cloud database pricing is still anchored to expert service costs, more specifically designed by watching traditional enterprise database professional service pricing. However, there are some preferential treatments for SMB micro scenarios - because oversold instances for patching don't cost much anyway. Services like Neon/Supabase simply offer this scenario for free.

Of course, one core database costing 10-20k per year (PolarDB about 3-5k) doesn't sound expensive, but considering that a single rack can now pack **thousands of cores** of servers, for users with very large-scale databases, annual costs of tens of millions to hundreds of millions are frightening - after all, from a common-sense perspective, finding two database experts to self-build with hardware would only cost around 10 million.

For example, recent reports by LeiPhones about "[Exclusive | miHoYo May Drastically 'De-cloud', Halving Budget for Certain Cloud Vendor](https://mp.weixin.qq.com/s/DWw_C01zRD6kbbT_NRqSvw)" mentioned a vivid case - PolarDB's benchmark customer miHoYo slashed nearly 400 million yuan in database budget...

From another perspective, companies with annual cloud spending over 1 million should start calculating carefully; over 10 million should comprehensively go off-cloud; companies with annual cloud spending over 100 million who don't self-build are really carrying a "money-stupid" pig flag, attracting pig-killing schemes. MiHoYo's de-clouding - better late than never. As for companies like Xiaohongshu moving to cloud at this scale, we wish them good luck.

## How Much Does Self-Building Databases Cost?

Whether it's commercial database subscription support, open-source database professional services, or cloud databases, it's not hard to see that the core production factor here is "experts", not "software" and "hardware".

From a cost perspective, current comprehensive hardware unit costs are about 60-300 RMB/vCPU·year, which can be said to be negligible in database services. Because of the emergence of open-source databases, the license value of most commercial database products has directly returned to zero; many domestic databases are just PG rebranding with no R&D costs; so the core cost is experts and sales costs.

Therefore, in 2024, databases making money by **licensing** are either monopoly/vendor lock-in protection fees or cognitive asymmetry pig-slaughter money. Or essentially still selling dog meat under sheep's head, spreading expert fees into license costs.

**Database companies really sell expert service support, not software**. From the above examples, it's not hard to see that expert service support prices are tied to database scale, with international market fair selling prices of **10-20k RMB/vCPU per year**. Whether purchasing from database service companies or cloud vendors, it's roughly in this range.

Of course, if your database scale is large enough with enough vCPU cores, the most economical approach is directly hiring database experts rather than renting from elsewhere. For example, if you have 100 vCPU scale database, that corresponds to 1-2 million yuan expert maintenance budget - hiring a good enough database expert is completely feasible now. If you have 10,000 vCPU, maybe you need two or three database experts, but their salaries have an order of magnitude difference compared to hundreds of millions in procurement costs...

Of course, ideals are beautiful, reality is harsh. To be realistic, database experts aren't that easy to recruit. Not just small factories and small clients - even big cloud vendor giants can't find and retain these people.

For example, Apple once recruited a PostgreSQL expert position in Shanghai and couldn't find a suitable candidate for two years. The logic is simple: why would truly awesome experts not start their own companies to earn the 10-20k RMB/vCPU per year mentioned above, instead of working for employers?

The most typical example is PolarDB founder Cao Wei (nickname Mingsong), who left Alibaba-Cloud a couple years ago to start his own database management company Kubeblocks. There's also Ye Zhengsheng's Jiuzhang Technology. According to reports: ***An early investor told us that in the past year or two, she has contacted database entrepreneurs who left Alibaba in the double digits.***

## Back to the Twenty-Dollar Brother

Looking back at our twenty-dollar buddy PolarDB, according to market pricing, the annual cost per vCPU should be 10-20k for decent database service. Let's consider the relatively low-end scenario (funny thing: many cloud vendors mark 4c8g specs as "entry enterprise server"), with a 4c8thread low-end server, a node's quote should be around 100k yuan (provided it includes corresponding expert support services). 130 yuan is pure loss-making, not even enough for sales taxi fare to collect money.

Obviously this isn't a market-compliant quote, but wanting to lose money to create benchmark cases. After all, it's the People's Bank - after succeeding, sales can brag with more confidence. But price wars are double-edged swords - if you quote 130 yuan unit price to disrupt the market, naturally various peers will quote 1 yuan to lose even more, desperately losing money to pull you down - absolutely cannot let you create such benchmark cases.

Let me explain again - PolarDB isn't a single database, but a database brand. Brand means there are several databases in this basket: PolarDB for MySQL (flagship product), PolarDB for PostgreSQL (open source), and PolarDB for Oracle (modified from for PG), blah blah. The People's Bank contract for PolarDB v2.0 is actually PolarDB for Oracle, which is an Oracle-compatible version modified based on PolarDB for PG.

Of course, PolarDB for MySQL sells well on the cloud. As an early large-scale MySQL user domestically, Alibaba has deep expertise in MySQL and has produced many MySQL experts. PolarDB for MySQL is indeed the flagship product in PolarDB. Benchmark customer miHoYo also uses this. But offline private deployment and domestic Xinchang's for PostgreSQL/Oracle don't have benchmark cases like miHoYo for MySQL.

But now, de-clouding is becoming a trend. According to reports, PolarDB MySQL benchmark customer miHoYo slashed 400 million yuan (annually) database budget in one go... What's the concept of 400 million? Although Alibaba-Cloud's annual revenue is hundreds of billions, [profit in the past year was less than 9 billion](https://mp.weixin.qq.com/s/wUJiCKusK8GRe9yQd8inIQ). Database gross margins start at 50%, 70% isn't surprising - this cut is really hurtful.

So, encountering Waterloo on the cloud, naturally they need to open a second battlefield, create a second growth curve, doing offline private deployment. Although Alibaba-Cloud talks about public cloud priority, PolarDB's body is still honest about getting that Xinan national certification, creating a self-controllable domestic database identity. Watching illegitimate son OceanBase harvest everywhere with envy - Coach, I want to play basketball too! I want to be a domestic database too!

## Database Veteran Driver Commentary

As a database veteran driver, I think illegitimate son OceanBase's technical route made double wrong bets: first betting on distributed, which has become a false demand under contemporary hardware conditions; second betting on MySQL ecosystem, with ceiling already locked. While Alibaba's database legitimate son PolarDB (PG/Oracle) recognized the situation, corrected course in technical route, returning to RAC centralized, PostgreSQL ecosystem path - obviously has much brighter prospects in product/technical route.

Of course, having prospects or not is relative to other "domestic databases". Based on open-source database trunk providing expert services, distributions, extensions, and other incremental value is the right path. Indigenous R&D is the closed and rigid old path, magic-modifying open source is the flag-changing evil path. PolarDB for PostgreSQL overall doesn't heavily magic-modify PostgreSQL, basically can reuse PG ecosystem extensions, tools and components - I think this is very wise.

So, in our open-source out-of-the-box PostgreSQL distribution Pigsty v3.0, we also provide support for open-source PolarDB for PostgreSQL, meaning you can directly use PolarDB for PostgreSQL to replace native PG kernel, having out-of-the-box monitoring systems, high availability, backup recovery, IaC, connection pooling, load balancing, fault self-healing capabilities, turning an RPM package into a locally running enterprise RDS service. As for PolarDB for Oracle, because it's based on the for PG version, it's also supported, but to support the domestic database cause, this part won't be open-source and free. For the Pigsty & PolarDB v2 packaged domestic localized RDS solution, interested friends are welcome to contact me.