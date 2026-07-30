---
title: "Digoal, the Face of PostgreSQL at Alibaba Cloud, Has Left"
date: 2026-04-02
author: Ruohang Feng
summary: >
  Alibaba Cloud's leading PostgreSQL advocate has walked away, exposing a deeper struggle over the direction of China's cloud database market.
tags: [Alibaba Cloud, PostgreSQL, Cloud Databases]
---


Yesterday was April Fools' Day, and Digoal published a post on his WeChat account titled "[My Last Day as a Corporate Workhorse at Alibaba](https://mp.weixin.qq.com/s/IAeSAMfdwnhWpmRXxJMR8A)."

The database community immediately erupted. Many assumed it was an April Fools' joke, but I knew it was not.
Weeks earlier, the poster for the HOW conference had quietly changed his title to "former Alibaba Cloud database expert."
Today, he followed up with "[My First Stop After Leaving Alibaba](https://mp.weixin.qq.com/s/HdpRhse9PNXy4NL2d_cL4g)," putting the matter beyond doubt.

I previously wrote about [the departure of Justin Lin, the technical lead behind Alibaba's Qwen models](/en/cloud/qwen-leave/). Foundation models are the hottest game in town, so that story naturally drew enormous attention.
Databases still matter in the AI era, but they do not generate anything like the same traffic. Even so, this departure sent shock waves through the industry. Everyone was asking the same question: where did Digoal go?

Here is my take.


## 1. Digoal

Anyone who works with PostgreSQL in China knows Digoal.

Zhou Zhengzhong, known online as `digoal` and throughout the community as Dege—"Brother De"—joined the Alibaba Cloud database team in 2015. For the next decade, he and former PostgreSQL China community chair Xiao Shaocong carried much of the technical evangelism, community work, and ecosystem building for Alibaba Cloud RDS for PostgreSQL. Digoal became the public face of PostgreSQL at Alibaba Cloud, and arguably in China.

Digoal and I joined Alibaba in the same year. One of my teammates was even in the same Bai-A new-hire orientation cohort as him. I was just getting started with PostgreSQL; he had already spent years in the field and built a mountain of blog posts.
Later, when I promoted PostgreSQL inside Alibaba, I was in frequent contact with him. We also met often at PostgreSQL events. We go back a long way.

At least during my years at Alibaba, Digoal was consistently the top contributor on ATA, the company's internal engineering forum. Open its home page on almost any day and another one or two of his PostgreSQL evangelism posts would appear.
Doing that, day after day, for ten years deserves profound respect. He has published thousands of technical articles on GitHub, earning 8.4K stars; holds more than 40 database patents; and helped found the PostgreSQL China community.
His blog opens with a line: "Public service is a lifetime commitment." Grand declarations are everywhere. People who actually live by one for a decade are rare.

Digoal is one of the defining figures of China's PostgreSQL community. Now that face has left Alibaba Cloud. To most people, this is just another story about someone leaving a Chinese tech giant.
To anyone watching PostgreSQL in China, however, the signal matters far more than the personnel news itself. An era for PostgreSQL at Alibaba Cloud may have ended.


## 2. Fighting for a Foothold

To understand why Digoal's departure matters, you first need to know what using PostgreSQL inside Alibaba was like.
Alibaba grew up in a MySQL world. Java plus MySQL ruled the company, and that stack was deeply entrenched. Building on PostgreSQL in that environment made you an outsider.

I know the feeling firsthand. I started in algorithms and data warehousing, but chose PostgreSQL for an internal startup project. Pressure came from every direction.
When everyone else runs Java and MySQL and your project runs on PostgreSQL, the skepticism and isolation are intense.
I eventually went from algorithm engineer to DBA, taking responsibility for database operations and even managing a fleet of bare-metal servers running PostgreSQL myself.
At Alibaba, merely choosing PostgreSQL meant fighting your way through.

Digoal faced much the same battle, only he entered it earlier and went much deeper. He joined Alibaba Cloud's database kernel group in 2015, initially designing the architecture for RDS PostgreSQL and providing solution design and proof-of-concept support to customers inside and outside Alibaba.
Promoting PostgreSQL in a company where MySQL held overwhelming dominance was always an uphill fight.

Digoal fought it for ten years.


## 3. A Battle over Direction

Digoal's decade at Alibaba also tracked a deeper strategic struggle. Alibaba Cloud's database portfolio broadly follows two paths:

**The first is RDS.** In essence, it takes community editions of open-source databases such as MySQL and PostgreSQL and offers them as managed cloud services. You still use upstream PostgreSQL; Alibaba Cloud handles operations, high availability, backups, and recovery. The competition here is operational: who can run it best, offer the fullest ecosystem, and deliver the smoothest experience?

**The second is PolarDB.** This is Alibaba Cloud's own cloud-native database line, adapting and substantially modifying MySQL and PostgreSQL for cloud environments.

After AWS launched Aurora, cloud vendors everywhere embraced a branding strategy: modify an open-source database, attach a proprietary name, and sell it as their own.
If RDS merely moved open-source software into the cloud, PolarDB gave Alibaba Cloud a "built in-house" story.
The logic is simple. RDS means selling the community's product; PolarDB means selling your own. It is the favored child. For a cloud vendor, the latter promises higher gross margins, a deeper moat, and a sexier narrative.

Digoal's changing role over those ten years mirrors this strategic shift. He began with RDS PostgreSQL architecture, moved to community operations for PolarDB, and later handled ecosystem building and advocacy across the database portfolio.
His focus kept moving with the corporate strategy: RDS PostgreSQL → PolarDB for PostgreSQL → PolarDB for Oracle → open-source PolarDB.

As someone from the PostgreSQL ecosystem, I understand how uncomfortable that must have felt. You built your identity around upstream, unadulterated PostgreSQL, and now the organization wants you to promote a heavily modified fork. How could that sit well?
Alibaba Cloud has deep MySQL expertise, so its genuinely formidable flagship, PolarDB for MySQL, remains closed source. The PostgreSQL edition? That one was open-sourced.

Then PolarDB for PostgreSQL, itself a second-generation PostgreSQL derivative, was certified as a "domestic database" for China's secure-and-reliable IT procurement program.
My own Pigsty project supports both upstream PostgreSQL and this fork. But if I am honest, the other engines and compatibility layers—MySQL, Oracle, SQL Server, MongoDB—each have at least one decisive use case.
For PolarDB PostgreSQL alone, beyond the domestic certification, I cannot think of a scenario where it is indispensable. I suspect that was another source of Digoal's frustration.

Digoal is a PostgreSQL person to his core. The overwhelming majority of his more than 2,000 blog posts are genuine PostgreSQL technical articles, not PolarDB marketing copy.
His standing in the community came from his love for PostgreSQL and years of deep work, not from his title at Alibaba Cloud.

**Put the soul of a PostgreSQL community inside an organization that increasingly has no need for that community, and the outcome is almost inevitable.**


## 4. PostgreSQL in China

PostgreSQL occupies an awkward position in China's cloud database market.

Every few weeks, Hacker News seems to feature another "Why PostgreSQL Is the Best Database" post. PostgreSQL has ranked as the most admired database in Stack Overflow's developer survey for years. In DB-Engines, its global growth has led the field by a wide margin.

In China, however, the ratio of MySQL deployments to PostgreSQL remains somewhere between 5:1 and 10:1. PostgreSQL is growing fast—from what I hear, nearly 100% year over year—but the installed-base gap remains substantial.
Chinese developers have an extraordinarily deep dependence on MySQL. The LAMP stack 15 years ago, the internet startup boom a decade ago, and the golden age of PHP plus MySQL trained generation after generation of MySQL DBAs.
That stack is deeply rooted, with little incentive to switch. Alibaba itself bears much of the responsibility: years of wall-to-wall promotion of the MySQL ecosystem helped create China's distorted, winner-take-all market.

PostgreSQL's core users in China are not really internet companies, but manufacturers and traditional industries. GIS and geospatial data through PostGIS are hard requirements. IoT time-series workloads, Oracle-compatible migrations, and newer vector-search and AI applications have brought substantial growth.
More awkward still, a significant share of PostgreSQL deployments in China are repackaged and sold as assorted "domestic databases," diverting both users and mindshare from the PostgreSQL community. You do the work; someone else changes the label and takes the result.

**For ten years, Digoal's PostgreSQL advocacy at Alibaba Cloud was, in a sense, one man's passion pushing against the inertia of an entire market.** That effort deserves admiration, but it is also fragile. It depends heavily on how much tolerance and support the organization is willing to give one person.
When the organization's attention shifts to PolarDB, "domestic databases," AI, or anything with greater commercial value, the evangelist ends up in an awkward place.


## 5. Ask Digoal. It Works.

The PostgreSQL community has a telling habit. When something goes wrong with Alibaba Cloud RDS PostgreSQL, users do not first open a support ticket. They assume the ticket will be mostly useless and tag Digoal directly in a group chat instead.

Ask Digoal. It works.

Those four words say a great deal. RDS PostgreSQL does not retain users through some unique technology; at bottom, it is PostgreSQL in the cloud, and every provider offers roughly the same thing.
Its stickiness comes from **ecosystem and trust**. Users trust that people who truly understand PostgreSQL are behind the product—people who keep improving it, respond to community needs, and push compatibility and extension support forward. They believe that if they hit a genuinely difficult PostgreSQL problem, an expert like Digoal will ultimately be there to backstop them.

Digoal made that trust tangible. His blog was where many people began learning PostgreSQL. His answers in community chats reassured countless DBAs. His conference talks were the best advertising RDS PostgreSQL could ask for.

Call it the community freeloading on Digoal, or call it Digoal freely giving his time. A senior database expert's time is valuable, yet he kept answering community questions.
That generosity is part of what makes the PostgreSQL community special, and part of Digoal's personal appeal.

It is difficult to quantify any of this in a KPI. Users still notice when it disappears.


## 6. The Distilled Hero

Digoal's departure was not a sudden event. It had been building for years.

From what I know, he had genuinely become disillusioned at Alibaba. The most obvious sign was his rank. On Alibaba's internal ladder, Digoal was a P7 ten years ago. A decade later, he was still a veteran P8. Given his stature and output, P9 or P10 would hardly have been excessive.

Digoal turned ten years of experience and insight into thousands of blog posts, videos, and courses. He made all of it public and free for anyone to use.
That selfless sharing creates a cruel paradox: once a person's knowledge has been thoroughly "distilled" into a public asset, the organization may begin to see the person himself as less irreplaceable.

That view is shortsighted. Digoal may not develop database kernels, but he is unquestionably one of China's foremost PostgreSQL experts in real-world use, operations, and administration.
More importantly, he is a central reason people took Alibaba Cloud's PostgreSQL offering seriously. The written material is only a snapshot of knowledge. Digoal's judgment, community influence, and insight into users' pain cannot be fully written down or distilled away.

The story shares a theme with Justin Lin's departure from Qwen. As large companies mature, they systematically replace individuals with processes and heroes with systems.
Management theory calls this greater organizational maturity. In practice, the price is often the exhaustion of the people with the most passion and influence.

**Heroes are not defeated by enemies. They are worn down.**

Qwen could not keep Justin Lin. Alibaba Cloud's database organization could not keep Digoal.
Perhaps this is not one company's problem, but another glimpse of the permanent fault line between the machinery of Big Tech and technical idealists.


## 7. A Personal Note

When I heard that Digoal had left Alibaba Cloud, my first reaction was happiness.

Someone at Digoal's level will never lack options. Chinese database vendors and enterprise IT organizations will surely come calling.
I believe he can create even more value for the PostgreSQL ecosystem and community outside Alibaba. Frankly, keeping him inside a giant corporation was a waste.

To be completely honest, only a handful of database players in China qualify as potential competitors for me, and Alibaba Cloud is certainly one of them.
Now that its public face has gone, I would be lying if I said I was not pleased. But the pleasure comes with real regret.

I am sorry to see this happen to Alibaba Cloud. I criticize cloud vendors often, Alibaba Cloud included, but there is still a certain sympathy between peers. On the whole, I want it to succeed.
Whatever its faults, it remains a pillar of cloud computing in China, and some idealism still survives there—especially compared with certain competitors. Alibaba's corporate culture can be overpowering, but it is still much better than what you find at some other vendors.

So I am not here to mock Alibaba because one of its pillars walked away. That would be mean-spirited.
I genuinely find it regrettable. Alibaba had the chance to do this well, but as with Qwen, it simply could not retain its best people.

These days I wake up full of energy. Why? Because I work alone. I run an OPC—a one-person company. There is no internal friction, no meetings, and no office politics.
I work when I want to. When I do not, I lie down and take a nap. My wife used to manage hundreds of people and found it exhausting; she envies me.
From the outside, management may look glamorous. In reality, it is draining. Dealing with people consumes enormous energy.

I imagine Digoal has felt much the same over his years at Alibaba. After ten years there, he should have achieved financial independence.
He could run an OPC like mine, do some PostgreSQL consulting, and enjoy an easy, comfortable life.


## 8. What Comes Next

Digoal is gone. What happens to PostgreSQL at Alibaba Cloud? And what happens to PostgreSQL in China?

Start with Alibaba Cloud. RDS PostgreSQL will most likely enter a low-priority maintenance phase. PolarDB is the strategic focus; RDS PostgreSQL is merely a community child Alibaba Cloud babysits.
Without Digoal's personal drive, PostgreSQL will lose even more influence inside the company. Executives may keep saying that "PostgreSQL has priority," but if the people at the helm have their hearts in MySQL, everyone can guess the outcome.

I am rather pleased by that result. Alibaba Cloud is genuinely good at MySQL, so it should focus on MySQL.
Leaving PostgreSQL to people who truly love it may be no bad thing.

As for Digoal, friends keep asking where he went. Right now, he is traveling and taking a break.
After burning at full intensity for ten years, he has earned a vacation.

The spark Digoal lit has long since spread beyond a small circle of early PostgreSQL enthusiasts into a prairie fire.
PostgreSQL's foundations in China no longer depend on any one person or company. The ecosystem has grown. The roots have taken hold.

I have spent the same ten years on this road and watched PostgreSQL's entire journey in China from niche technology to mainstream choice.
Any account of how it got here must recognize Digoal's contribution. It stands as a monument.
If he eventually decides to return and build something new, I will be delighted to support him.

I wish Digoal every success in what comes next.
