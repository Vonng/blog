---
title: "MongoDB: Now Powered by PostgreSQL?"
linkTitle: "MongoDB: Now Powered by PostgreSQL"
date: 2024-09-03
author: |
  [John De Goes](https://www.linkedin.com/in/jdegoes) [Original Article](https://www.linkedin.com/pulse/mongodb-32-now-powered-postgresql-john-de-goes)
summary: >
  MongoDB 3.2's analytics subsystem turned out to be an embedded PostgreSQL database? A whistleblowing story from MongoDB's partner about betrayal and disillusionment.
tags: [Database]
---

-------------
 
#### Preface

Tomorrow I'll publish an article criticizing MongoDB, as a response to their recent malicious marketing that provocatively targets PostgreSQL. But before that, I want to share a brilliant article from 2015 that exposes some of MongoDB's dark history.

The most classic aspect of this article is that it's a tearful complaint from a MongoDB partner. MongoDB dismissed partners trying to build analytics in their ecosystem, instead opting to grab a PostgreSQL database as their own analytics engine to deceive users, ultimately leaving partners completely disillusioned.

> Original article link: https://www.linkedin.com/pulse/mongodb-32-now-powered-postgresql-john-de-goes (Behind dual firewalls, you need incognito mode with a proxy to access)

-------------

> Author: John De Goes — Challenging the status quo at Ziverge
>
> Published: December 8, 2015

*Opinions expressed are solely my own and do not represent the views or opinions of my [employer](http://slamdata.com/).*

When I finally pieced together all the clues, I was *shocked*. If my speculation was correct, [MongoDB](http://mongodb.com/) might be about to commit what I believe is the **biggest mistake** in database company history.

I am a developer of an [open source analytics tool](http://github.com/slamdata/slamdata) that supports connections to NoSQL databases like MongoDB, and I spend every day working to help these next-generation database vendors succeed.

In fact, I recently presented to a [packed room](https://twitter.com/slamdata/status/672166743255592960) at [MongoDB Days Silicon Valley](https://www.mongodb.com/events/mongodb-days-siliconvalley), giving a [talk](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) about the many benefits of adopting these new databases.

So when I realized this potentially destructive secret, I immediately sounded the alarm. On November 12, 2015, I sent an email to Asya Kamsky, MongoDB's Lead Product Manager.

Although worded politely, I made my point crystal clear: *MongoDB is making a huge mistake and should reconsider their decision while there's still time to correct it.*

However, I never received a response from Asya or anyone else. My previous success in persuading MongoDB to [change strategy](https://www.mongodb.com/blog/post/revisiting-usdlookup) and avoid commercializing [wrong features](http://slamdata.com/blog/2015/10/21/mongodb-missing-join.html) would not be repeated this time.

Here's how I found clues from press releases, YouTube videos, and source code scattered across Github, and how I ultimately failed to convince MongoDB to change direction.

The story begins on June 1, 2015, at the annual MongoWorld conference in New York City.



## MongoWorld 2015

[SlamData](http://slamdata.com/) is my new analytics startup, which sponsored MongoWorld 2015, so I got a rare VIP party ticket for the evening before the conference.

Held at NASDAQ MarketWatch, in a beautiful space overlooking Times Square, I felt distinctly underdressed in my cargo pants and startup t-shirt. Fancy hors d'oeuvres and alcohol flowed freely, and MongoDB's management team was out in full force.

I shook hands with MongoDB's new CEO Dev ("Dave") Ittycheria and offered him a few words of encouragement for the road ahead.

Earlier this year, Fidelity Investments [slashed](http://fortune.com/2015/11/12/fidelity-marks-down-tech-unicorns/) MongoDB's valuation to half of what it was in 2013 ($1.6 billion), downgrading the startup from "unicorn" to "donkey." Dev's job was to prove Fidelity and other skeptics wrong.

Dev inherited the company from Max Schireson (who [famously resigned](http://maxschireson.com/2014/08/05/1137/) in 2014), and during his tenure, Dev built a new management team that had ripple effects throughout MongoDB.

Although I only spoke with Dev for a few minutes, he seemed bright, friendly, and eager to learn about what my company was doing. He handed me his business card and said I could contact him anytime if needed.

Next was Eliot Horowitz, MongoDB's CTO and co-founder. I shook his hand, introduced myself, and delivered a 30-second pitch about my startup.

At the time, I thought my pitch must have been terrible because Eliot seemed disinterested in everything I was saying. It turns out Eliot hates SQL and views analytics as a nuisance, so it's not surprising I bored him!

However, Eliot did catch the word "analytics" and revealed that tomorrow at the conference, MongoDB would announce some interesting news about the upcoming 3.2 release.

I pleaded for more details, but no, that was strictly confidential. I would have to wait until the next day, along with the rest of the world.

I passed this news to my co-founder Jeff Carr, and we shared a brief moment of panic. For our four-person, self-funded startup, the biggest fear was that MongoDB would announce their own analytics tool, which could hurt our chances of raising money.

To our relief, we discovered the next day that MongoDB's big announcement wasn't an analytics tool, but rather a solution called the *MongoDB BI Connector*, a headline feature of the upcoming 3.2 release.

--------



## MongoDB 3.2 BI Connector

Eliot had the honor of announcing the BI connector. Of all the things he was announcing that day, he seemed least interested in the connector, so it barely got more than a mention.

However, details soon spread like wildfire through an [official press release](https://www.mongodb.com/press/opens-modern-application-data-to-new-generation-visual-analysis-and-traditional-bi-tools), which contained this concise summary:

> MongoDB today announced a new connector for BI and visualization that connects MongoDB databases to industry-standard business intelligence (BI) and data visualization tools. Designed to work with every SQL-compliant data analysis tool on the market, including Tableau, SAP Business Objects, Qlik, and IBM Cognos Business Intelligence, the connector is currently in preview and expected to become generally available in Q4 2015.

According to the press release, the BI connector would allow *any BI software in the world* to interface with MongoDB databases.

This news quickly [spread](https://twitter.com/search?f=tweets&vertical=default&q=mongodb bi connector&src=typd) on Twitter and generated widespread media coverage. [TechCrunch](http://techcrunch.com/2015/06/02/new-mongodb-connector-creates-direct-connection-to-data-visualization-tools/) and many others picked up the story, with each retelling adding new details. Fortune even claimed the BI connector had actually been [released](http://fortune.com/2015/06/03/couchbase-mongodb-embrace-sql/) at MongoWorld!

Given the nature of the announcement, the media's enthusiastic response seemed justified.

### When Worlds Collide

MongoDB, like many other NoSQL databases, doesn't store relational data. It stores complex data structures that traditional relational BI software cannot understand. MongoDB's VP of Strategy Kelly Stirman explained this succinctly:

> *"These applications called modern are so named because they use complex data structures that don't fit neatly into the traditional database row-column format."*

A connector that could enable any BI software in the world to perform robust analytics on these complex data structures *without losing analytical precision* would be *major news*.

Had MongoDB really achieved the impossible? Had they developed a connector that satisfies all [NoSQL analytics requirements](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/) while exposing relational semantics on flattened, uniform data so legacy BI software could handle it?

A few months earlier, I had spoken with Ron Avnur, MongoDB's VP of Products. Ron indicated that all of MongoDB's customers wanted analytics capabilities, but the company hadn't decided whether to build in-house or work with partners.

This meant MongoDB had gone from *nothing* to a *magical solution* in just a few months.



### Pulling Back the Curtain

After the announcement, Jeff and I returned to our sponsor booth. Jeff asked me the most obvious question: **"How did they go from nothing to a BI connector that works with all possible BI tools in just a couple of months?!"**

I thought carefully about this question.

Among the many problems a BI connector would need to solve, one major challenge would be efficiently executing SQL-like analytics on MongoDB. From my [deep](http://github.com/quasar-analytics/)[background](http://github.com/precog) in analytics, I knew that efficiently executing general-purpose analytics on modern databases like MongoDB is extremely challenging.

These databases support very rich data structures, and their interfaces are designed for so-called **operational** use cases (not **analytical** use cases). The technology capable of leveraging operational interfaces to run arbitrary analytics on rich data structures takes **years** to develop. It's not something you can whip up in two months.

So I gave Jeff my gut response: **"They didn't develop a new BI connector. That's impossible. Something else is going on here!"**

I didn't know exactly what. But between handshakes and business card exchanges, I did some investigating.

Tableau showed a demo of their software working with the MongoDB BI Connector, which piqued my curiosity. Tableau has set the standard for visual analytics on relational databases, and their forward-thinking big data team has been seriously considering NoSQL.

Thanks to their relationship with MongoDB, Tableau issued a [press release](http://www.tableau.com/about/blog/2015/6/tableau-mongodb-visual-analytics-json-speed-thought-39557) to coincide with the MongoWorld announcement, which I found on their website.

I carefully read through this press release hoping to learn new details. Buried deep inside, I discovered a faint clue:

> MongoDB will soon announce beta availability of the connector, with general availability planned around the MongoDB 3.2 release later this year. During MongoDB's beta period, Tableau will support the MongoDB connector on both Windows and Mac **via our PostgreSQL driver**.

These words gave me my first clue: **via our PostgreSQL driver**. This meant, at minimum, that MongoDB's BI Connector would speak the same "language" (*wire protocol*) as PostgreSQL databases.

This struck me as suspicious: was MongoDB really re-implementing the **entire** PostgreSQL wire protocol, including support for hundreds of PostgreSQL functions?

While **possible**, this seemed **extremely unlikely**.

I turned to Github, looking for open source projects MongoDB might have leveraged. The conference WiFi was unstable, so I had to use my phone's hotspot to search through dozens of repositories mentioning both PostgreSQL and MongoDB.

Eventually, I found what I was looking for: [mongoose_fdw](https://github.com/asya999/mongoose_fdw/commits/master), an open source repository forked by Asya Kamsky (whom I didn't know at the time, but her profile mentioned she worked for MongoDB).

This repository contained a so-called *Foreign Data Wrapper* (FDW) for PostgreSQL databases. The FDW interface allows developers to plug in other data sources so PostgreSQL can extract data and execute SQL on it (NoSQL data must be flattened, null-padded, and otherwise simplified for BI tools to work properly).

**"I think I know what's going on,"** I told Jeff. **"It looks like they might be flattening the data for the prototype and using another database to execute SQL statements generated by BI software."**

**"What database?"** he immediately asked.

**"PostgreSQL."**

Jeff was speechless. He didn't say a word. But I could tell exactly what he was thinking, because I was thinking the same thing.

**Shit. This is bad news for MongoDB. Really bad.**


--------



## PostgreSQL: The MongoDB Killer

PostgreSQL is a popular open source relational database. It's so popular that it currently [ranks](http://db-engines.com/en/ranking) almost neck-and-neck with MongoDB.

This database poses *fierce competition* for MongoDB, primarily because it has acquired some of MongoDB's features, including the ability to store, validate, manipulate, and index [JSON documents](https://en.wikipedia.org/wiki/JSON). Third-party software even [gives it](https://www.citusdata.com/) horizontal scaling capabilities (or should I say, *humongous* scaling capabilities).

Every month or so, someone writes an article recommending PostgreSQL over MongoDB. These articles often go viral and rocket to the top of HackerNews. Here are links to some of these articles:

- [Goodbye MongoDB. Hello PostgreSQL](http://developer.olery.com/blog/goodbye-mongodb-hello-postgresql/)
- [Postgres Outperforms MongoDB and Ushers in New Developer Reality](http://www.enterprisedb.com/postgres-plus-edb-blog/marc-linster/postgres-outperforms-mongodb-and-ushers-new-developer-reality)
- [MongoDB is dead. Long live PostgreSQL :)](https://github.com/errbit/errbit/issues/614)
- [Why You Should Never Use MongoDB](http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/)
- [SQL vs NoSQL KO. Postgres vs Mongo](https://www.airpair.com/postgresql/posts/sql-vs-nosql-ko-postgres-vs-mongo)
- [Why I Migrated Away from MongoDB](http://svs.io/post/31724990463/why-i-migrated-away-from-mongodb)
- [Why you should never, ever, ever use MongoDB](http://cryto.net/~joepie91/blog/2015/07/19/why-you-should-never-ever-ever-use-mongodb/)
- [Is Postgres NoSQL Better than MongoDB?](http://www.aptuz.com/blog/is-postgres-nosql-database-better-than-mongodb/)
- [Bye Bye MongoDB. Guten Tag PostgreSQL](https://www.userlike.com/en/blog/2015/10/09/bye-by-mysql-and-mongodb-guten-tag-postgresql)

The largest company commercializing PostgreSQL is [EnterpriseDB](http://enterprisedb.com/) (though there are many others, some older or equally active), which maintains a [large content repository](http://www.enterprisedb.com/nosql-for-enterprise) on their official website arguing that PostgreSQL is a better NoSQL database than MongoDB.

Whatever your opinion on this point, one thing is clear: MongoDB and PostgreSQL are locked in a fierce, bloody battle for developer mindshare.




--------

## From Prototype to Production

Any experienced engineer will tell you that **prototypes aren't for production**.

Even if MongoDB *was* using PostgreSQL as a prototype BI connector, perhaps some brilliant MongoDB engineers were locked in a room somewhere, working on a standalone production version.

Indeed, Tableau's press release wording even suggested the PostgreSQL driver dependency *might* be temporary:

> **During MongoDB's beta phase**, Tableau will support the MongoDB connector on both Windows and Mac via our PostgreSQL driver.

Perhaps, I thought, MongoDB 3.2's release would ship with the *real deal*: a BI connector that exposes the rich data structures MongoDB supports (instead of flattening, null-padding, and discarding data), executes all queries 100% within the database, and has no dependencies on competing databases.

In July, more than a month after MongoWorld, I visited MongoDB's Palo Alto offices during a business trip. What I learned was very encouraging.


------

## A Visit to MongoDB

By Palo Alto standards, MongoDB's office is quite large.

I had seen the company's sign during previous Valley trips, but this was my first chance to go inside.

The week before, I had been chatting via email with Asya Kamsky and Ron Anvur. We discussed my company's [open source work](http://quasar-analytics.org/) on executing advanced analytics directly inside MongoDB.

Since we happened to be in Palo Alto at the same time, Asya invited me over to chat over catered pizza and office soda.

Within the first few minutes, I could tell Asya was smart, technical, and detail-oriented—exactly the traits you'd hope for in a product manager for a highly technical product like MongoDB.

I explained what my company was doing to Asya and helped her get our open source software running on her machine so she could try it out. At some point, we started chatting about BI connectors for MongoDB, of which there were several on the market (Simba, DataDirect, CData, and others).

We both seemed to share the same view: BI software needs to gain the ability to understand more complex data. The alternative, which involves dumbing down data to fit the limitations of older BI software, means throwing away so much information that you lose the ability to solve [key problems](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/) in NoSQL analytics.

Asya thought MongoDB's BI connector should expose native MongoDB data structures, such as arrays, without any flattening or transformations. This characteristic, which I call an *isomorphic data model*, is one of the key requirements for general-purpose NoSQL analytics systems, a topic I've written about extensively in [multiple articles](http://www.infoworld.com/article/2983953/nosql/how-to-choose-a-nosql-analytics-system.html).

I was very encouraged that Asya had independently reached the same conclusion, and I felt confident that MongoDB understood the problem. I thought MongoDB's analytics future looked very bright.

Unfortunately, I couldn't have been more wrong.



--------

## MongoDB: Built for Giant ~~Ideas~~ Mistakes

After learning that MongoDB was on the right track, I relaxed my vigilance about the BI connector and didn't pay much attention to it over the next few months, though I did exchange a few emails with Asya and Ron.

However, by September, I found the MongoDB product team had fallen silent. After weeks of unreturned emails, I grew restless and started poking around on my own.

I discovered that Asya had forked a project called [Multicorn](https://github.com/asya999/Multicorn), which allows Python developers to write Foreign Data Wrappers for PostgreSQL.

*Uh oh*, I thought, *MongoDB is back to their old tricks.*

Further digging revealed the so-called "holy grail": a new project called [yam_fdw](https://github.com/asya999/yam_fdw) (Yet Another MongoDB Foreign Data Wrapper), a brand new FDW written in Python using Multicorn.

According to the commit log (which tracks repository changes), this project was developed after my July meeting with Asya Kamsky. In other words, this was *post-prototype* development work!

The final nail in the coffin that convinced me MongoDB planned to ship PostgreSQL database as their "BI connector" came when someone forwarded me a [YouTube video](https://www.youtube.com/watch?v=0kwopDp0bmg) where Asya demonstrated the connector.

Worded very cautiously and omitting any incriminating information, the video nonetheless concluded with this summary:

> The BI Connector receives connections and can use the **same wire protocol as the Postgres database**, so if your reporting tool can connect via ODBC, we will provide an ODBC driver that you can use to connect from your tool to the BI Connector.

At that point, I had zero doubt: the production version of the BI connector shipping with MongoDB 3.2 was, in fact, a disguised PostgreSQL database!

Most likely, the actual logic for sucking data out of MongoDB into PostgreSQL was a souped-up version of the Python-based Multicorn wrapper I had discovered earlier.

By this point, no one at MongoDB was returning my emails, which would have been enough for any sane person to give up.

However, I decided to give it one more try at the MongoDB Days conference on December 2, just one week before the 3.2 release.

Eliot Horowitz would deliver a keynote, Asya Kamsky would speak, and Ron Avnur would probably attend. Even Dev himself might show up.

That would be my best chance to convince MongoDB to abandon the BI connector shenanigans.



--------

## MongoDB Days 2015, Silicon Valley

Thanks to MongoDB's excellent marketing team, and based on the success of a similar talk I gave in Seattle at a MongoDB roadshow, I got a 45-minute presentation slot at the MongoDB Days conference.

My *official* purpose at the conference was to deliver a talk about MongoDB-powered analytics and make users aware of the open source software my company develops.

But my *personal* agenda was quite different: convincing MongoDB to can the BI connector before the impending 3.2 release. If that lofty and most likely *delusional* goal couldn't be achieved, I at least wanted to confirm my suspicions about the connector.

On the day of the conference, I made a point of greeting old and new faces at MongoDB. Regardless of how much I might disagree with certain product decisions, there are many amazing people at the company just trying to do their jobs.

I had gotten sick a few days earlier, but copious amounts of coffee kept me (mostly) awake. As the day progressed, I rehearsed my presentation several times, pacing the long corridors of the San Jose Convention Center.

When afternoon rolled around, I was ready and gave [my talk](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) to a packed room. I was excited about how many people were interested in the esoteric topic of [visual analytics on MongoDB](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) (clearly the space was growing).

After shaking hands and exchanging cards with some attendees, I went hunting for MongoDB's management team.

I first ran into Eliot Horowitz, moments before he was about to begin his keynote. We chatted about kids and food, and I told him how things were going at my company.

The keynote started sharply at 5:10. Eliot talked about some 3.0 features, since apparently many companies are still stuck on older versions. He then proceeded to give a whirlwind tour of MongoDB 3.2 features.

I wondered what Eliot would say about the BI connector. Would he even mention it?

It turns out the BI connector was a leading feature of the keynote, having its own dedicated segment and even a flashy demo.



### BI Connector

Eliot introduced the BI connector by loudly proclaiming, *"MongoDB has no native analytics tools."*

I found this somewhat amusing, since I had written a guest post for MongoDB titled [Native Analytics for MongoDB with SlamData](https://www.mongodb.com/blog/post/native-sql-analytics-mongodb-slamdata). (Editor's note: MongoDB has since taken down this blog post, but as of 15:30 MDT, it's still [in the search index](https://www.mongodb.com/blog?utf8=✓&search=slamdata#)). SlamData is also a MongoDB partner and sponsored the MongoDB Days conference.

When introducing the BI connector's purpose, Eliot seemed to stumble a bit (getting actions from... actionable insights? *Pesky analytics!*). He looked relieved when he handed the presentation over to Asya Kamsky, who had prepared a nice demo for the event.

During the presentation, Asya seemed uncharacteristically nervous to me. She chose her words carefully, omitting all details about what the connector was, only covering the non-incriminating parts of how it worked (such as its reliance on DRDL to define MongoDB schemas). Most of the presentation focused not on the BI connector but on Tableau (which, of course, demos very well!).

All my feedback hadn't even slowed down the BI connector.

### Pulling Out All the Stops

After the keynote, the swarm of conference attendees proceeded to the cocktail reception in the adjacent room. Attendees mostly talked to other attendees, while MongoDB employees tended to cluster together.

I saw Ron Avnur chatting with Dan Pasette, VP of Server Engineering, a few feet from where they were serving Lagunitas IPA to attendees.

Now was the time to act. The 3.2 release was coming out in just days. No one at MongoDB was returning emails. Eliot had just told the world there were no native analytics tools for MongoDB and positioned the BI connector as a revolutionary tool for NoSQL analytics.

With nothing to lose, I walked up to Ron, inserted myself into the conversation, and began what was probably a two-minute, highly-animated monologue violently attacking the BI connector.

I told him I expected more from MongoDB than disguising PostgreSQL database as the magical solution to MongoDB analytics. I told him MongoDB should have demonstrated integrity and leadership by shipping a solution that supports the rich data structures MongoDB supports, pushes all computation into the database, and doesn't depend on a competing database.

Ron was stunned. He began defending the BI connector's "pushdown" in vague terms, and I realized this was my chance to confirm my suspicions.

"Postgres foreign data wrappers barely support any pushdown," I stated matter-of-factly. "This is especially true in the Multicorn wrapper you're using for the BI connector, which is based on an older Postgres version and doesn't even support the full pushdown capabilities of Postgres FDW."

Ron admitted defeat. "That's true," he said.

I pushed him to defend the decision. But he had no answer. I told him to pull the emergency brake right now, before MongoDB released the "BI connector." When Ron shrugged off that possibility, I told him the whole thing would blow up in his face. "You might be right," he said, "but I have bigger things to worry about right now," possibly referring to the upcoming 3.2 release.

The three of us had a beer together. I pointed at Dan and said, "This guy's team built a database that can actually do analytics. Why aren't you using it in the BI connector?" But it was no use. Ron wasn't budging.

We parted ways, agreeing to disagree.

I spotted Dev Ittycheria from across the room and walked over to chat with him for a few minutes. I complimented the marketing department's work, then moved on to criticize the product. I told Dev, "In my opinion, the product team is making some mistakes." He wanted to know more, so I gave him my spiel, which I had repeated often enough to know by heart. He told me to follow up by email, and of course I did, but I never heard back.

After my conversation with Dev, it finally sunk in that I wouldn't be able to change MongoDB 3.2's release course. It would ship with the BI connector, and there wasn't a single thing I could do about it.

I was disappointed, but at the same time, I felt a huge wave of relief. I had talked to everyone I could reach. I had pulled out all the stops. I had given it my all.

As I left the cocktail reception and headed back to my hotel, I couldn't help but speculate on why the company was making decisions I so strongly opposed.


--------

## MongoDB: An Island of One

After much reflection, I now think MongoDB's poor product decisions stem from an inability to focus on the core database. This inability to focus is caused by their failure to cultivate a NoSQL ecosystem.

Relational databases rose to dominance partly because of the massive ecosystem that developed around these databases.

This ecosystem gave birth to applications for backup, replication, analytics, reporting, security, governance, and many other categories. They depend on and contribute to each other's success, creating network effects and high switching costs that challenge today's NoSQL vendors.

In contrast, there's virtually *no ecosystem* around MongoDB, and I'm not the only one to [notice this](http://slamdata.com/blog/2014/12/09/where-is-the-nosql-ecosystem.html).

Why isn't there an ecosystem around MongoDB?

My snarky answer is that if you're a MongoDB partner providing native analytics for MongoDB, the CTO will get up on stage and say there are no tools that provide native analytics for MongoDB.

More objectively, however, I think the above is just a symptom. The *real problem* is that MongoDB's partner program is completely broken.

MongoDB's partner team reports directly to the Chief Revenue Officer (Carlos Delatorre), which means the partner team's primary job is to extract revenue from partners. This inherently skews partner activities toward large companies with no vested interest in NoSQL ecosystem success (indeed, many produce competing relational solutions).

This contrasts with small, NoSQL-centric companies like SlamData, Datos IO, and others. These companies succeed *precisely* when NoSQL succeeds, and they provide functionality standard in the relational world that NoSQL databases *need* to thrive in enterprise environments.

After being a partner for more than a year, I can tell you almost no one at MongoDB knew about SlamData's existence, despite SlamData acting as a powerful incentive for companies to choose MongoDB over other NoSQL databases (e.g., MarkLogic) and an enabler for companies considering switching from relational technology (e.g., Oracle).

Despite partners' efforts, MongoDB appears completely unconcerned about joint revenue and sales opportunities presented by NoSQL-centric partners. No reseller agreements. No revenue sharing. No sales materials. No joint marketing. Nothing but a logo.

This means organizationally, MongoDB ignores the NoSQL-centric partners who could most benefit them. Meanwhile, their largest customers and prospects keep demanding infrastructure common in the relational world: backup, replication, monitoring, analytics, data visualization, reporting, data governance, query analysis, and much more.

This incessant demand from larger companies, combined with inability to cultivate an ecosystem, forms a *toxic combination*. It leads MongoDB's product team to try to *create their own ecosystem* by building *every possible product*!

Backup? Check. Replication? Check. Monitoring? Check. BI connectivity? Check. Data discovery? Check. Visual analytics? Check.

But a single NoSQL database vendor with finite resources cannot possibly build an ecosystem around itself to compete with the massive ecosystem around relational technology (it's far too expensive!). So this leads to distractions like MongoDB Compass and "sham" technology like the BI connector.

What's the alternative? In my opinion, it's quite simple.

First, MongoDB should nurture a vibrant, venture-funded ecosystem of NoSQL-centric partners (*not* well-funded relational partners!). These partners should have deep domain expertise in their respective areas, and all should succeed precisely when MongoDB succeeds.

MongoDB sales reps and account managers should be equipped with partner-provided information that helps them overcome objections and reduce churn, and MongoDB should build this into a healthy revenue stream.

Second, with customer demand for related infrastructure satisfied by NoSQL-centric partners, MongoDB should focus both product *and* sales on the core database, which is how a *database vendor* should make money!

MongoDB should develop features with significant enterprise value (such as ACID transactions, NVRAM storage engines, columnar storage engines, cross-datacenter replication, etc.) and thoughtfully draw the line between Community and Enterprise editions. All in a way that gives *developers* the same capabilities across editions.

The goal should be for MongoDB to drive enough revenue from the database that the product team won't be tempted to invent an inferior ecosystem.

You can judge for yourself, but I think it's pretty clear which is the winning strategy.




--------

## Goodbye, MongoDB!

Obviously, I cannot support product decisions like shipping a competing relational database as the definitive solution for analytics on a post-relational database like MongoDB.

In my opinion, this decision is bad for the community, bad for customers, and bad for the emerging NoSQL analytics space.

Furthermore, if this isn't done with *full transparency*, it's also harmful to integrity, which is the foundation of *all companies* (especially open source companies).

So with this post, I'm officially giving up.

No more frantic emails to MongoDB. No more monopolizing management at MongoDB cocktail parties. No more sharing my opinions privately with a company that doesn't even return emails.

Been there, done that, didn't work.

Obviously, I'm now blowing the whistle. By the time you read this, the whole world will know that the MongoDB 3.2 BI Connector is actually PostgreSQL database with some glue to flatten data, discard bits and pieces, and suck what's left into PostgreSQL.

What does this mean for companies evaluating MongoDB?

That's your call, but personally, if you're looking for a NoSQL database, need legacy BI connectivity, and are also considering PostgreSQL, you should probably just choose PostgreSQL.

After all, MongoDB's *own answer* to the analytics problem on MongoDB is to extract data from MongoDB, flatten it, and dump it into PostgreSQL. If your data will end up as flattened relational data in PostgreSQL anyway, why not start there? Kill two birds with one stone!

At least you can count on the PostgreSQL community to innovate around NoSQL, which they've been doing for years. There's zero chance the community would package up MongoDB database into a fake "PostgreSQL NoSQL" product and call it a revolution in NoSQL database technology.

Which is, sadly, *exactly* what MongoDB has done in reverse.

------

*The "Shame" photo was taken by [Grey World](https://www.flickr.com/photos/greyworld/), copyright Grey World, and licensed under [CC By 2.0](https://creativecommons.org/licenses/by/2.0/).*









--------

# MongoDB 3.2: Now Powered by PostgreSQL

> John De Goes — Challenging the status quo at Ziverge

Published: December 8, 2015


*Opinions expressed are solely my own, and do not express the views or opinions of my [employer](http://slamdata.com/).*

When I finally pieced together all the clues, I was *shocked*. If I was right, [MongoDB](http://mongodb.com/) was about to make what I would call the *biggest mistake ever made* in the history of database companies.

I work on an [open source analytics tool](http://github.com/slamdata/slamdata) that connects to NoSQL databases like MongoDB, so I spend my days rooting for these next-generation database vendors to succeed.

In fact, I just presented to a [packed room](https://twitter.com/slamdata/status/672166743255592960) at [MongoDB Days Silicon Valley](https://www.mongodb.com/events/mongodb-days-siliconvalley), [making a case](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) for companies to adopt the new database.

So when I uncovered a secret this destructive, I hit the panic button: on November 12th, 2015, I sent an email to Asya Kamsky, Lead Product Manager at MongoDB.

While polite, I made my opinion crystal clear: *MongoDB is about to make a giant mistake, and should reconsider while there's still time*.

I would never hear back from Asya — or anyone else about the matter. My earlier success in helping convince MongoDB to [reverse course](https://www.mongodb.com/blog/post/revisiting-usdlookup) when they tried to monetize [the wrong feature](http://slamdata.com/blog/2015/10/21/mongodb-missing-join.html) would not be repeated.

This is the story of what I discovered, how I pieced together the clues from press releases, YouTube videos, and source code scattered on Github, and how I ultimately failed to convince MongoDB to change course.

The story begins on June 1st 2015, at the annual MongoWorld conference in New York City.


--------

## MongoWorld 2015

[SlamData](http://slamdata.com/), my new analytics startup, was sponsoring MongoWorld 2015, so I got a rare ticket to the VIP party the night before the conference.

Hosted at NASDAQ MarketWatch, in a beautiful space overlooking Times Square, I felt distinctly underdressed in my cargo pants and startup t-shirt. Fancy h'ordeuvres and alcohol flowed freely, and MongoDB's management team was out in full force.

I shook hands with MongoDB's new CEO, Dev ("Dave") Ittycheria, and offered him a few words of encouragement for the road ahead.

Only this year, Fidelity Investments [slashed](http://fortune.com/2015/11/12/fidelity-marks-down-tech-unicorns/) its valuation of MongoDB to 50% of what it was back in 2013 ($1.6B), downgrading the startup from "unicorn"  to "donkey".

It's been Dev's job to prove Fidelity and the rest of the naysayers wrong.

Dev inherited the company from Max Schireson (who [famously resigned](http://maxschireson.com/2014/08/05/1137/) in 2014), and in his tenure, Dev has built out a new management team at MongoDB, with ripples felt across the company.

Though I only spoke with Dev for a few minutes, he seemed bright, friendly, and eager to learn about what my company was doing. He handed me his card and asked me to call him if I ever needed anything.

Next up was Eliot Horowitz, CTO and co-founder of MongoDB. I shook his hand, introduced myself, and delivered a 30 second pitch for my startup.

At the time, I thought my pitch must have been terrible, since Eliot seemed disinterested in everything I was saying. Turns out Eliot hates SQL and views analytics as a nuisance, so it's not surprising I bored him!

Eliot did catch the word "analytics", however, and dropped that tomorrow at the conference, MongoDB would have some news about the upcoming 3.2 release that I would find very interesting.

I pleaded for more details, but nope, that was strictly confidential. I'd find out the following day, along with the rest of the world.

I passed along the tip to my co-founder, Jeff Carr, and we shared a brief moment of panic. The big fear for our four-person, self-funded startup was that MongoDB would be announcing their own analytics tool for MongoDB, which could hurt our chances of raising money.

Much to our relief, we'd find out the following day that MongoDB's big announcement wasn't an analytics tool. Instead, it was a solution called *MongoDB BI Connector*, a headline feature of the upcoming 3.2 release.



--------

## The MongoDB 3.2 BI Connector

Eliot had the honor of announcing the BI connector. Of all the things he was announcing, Eliot seemed least interested in the connector, so it got barely more than a mention.

But details soon spread like wildfire thanks to an [official press release](https://www.mongodb.com/press/opens-modern-application-data-to-new-generation-visual-analysis-and-traditional-bi-tools), which contained this succinct summary:

> MongoDB today announced a new connector for BI and visualization, which connects MongoDB to industry-standard business intelligence (BI) and data visualization tools. Designed to work with every SQL-compliant data analysis tool on the market, including Tableau, SAP Business Objects, Qlik and IBM Cognos Business Intelligence, the connector is currently in preview release and expected to become generally available in the fourth quarter of 2015.

According to the press release, the BI connector would allow *any BI software in the world* to interface with the MongoDB database.

News of the connector [caught fire](https://twitter.com/search?f=tweets&vertical=default&q=mongodb bi connector&src=typd) on Twitter, and the media went into a frenzy. The story was picked up by [TechCrunch](http://techcrunch.com/2015/06/02/new-mongodb-connector-creates-direct-connection-to-data-visualization-tools/) and many others. Every retelling added new embellishments, with Fortune even claiming the BI connector had actually been [released at MongoWorld](http://fortune.com/2015/06/03/couchbase-mongodb-embrace-sql/)!

Given the nature of the announcement, the media hoopla was probably justified.

### When Worlds Collide

MongoDB, like many other NoSQL databases, does not store relational data. It stores rich data structures that relational BI software cannot understand.

Kelly Stirman, VP of Strategy at MongoDB, explained the problem well:

> *"The thing that defines these apps as modern is rich data structures that don't fit neatly into rows and columns of traditional databases*."

A connector that enabled any BI software in the world to do robust analytics on rich data structures, *with no loss of analytic fidelity*, would be *giant news*.

Had MongoDB really done the impossible? Had they developed a connector which satisfies all the [requirements of NoSQL analytics](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/), but exposes relational semantics on flat, uniform data, so legacy BI software can handle it?

A couple months earlier, I had chatted with Ron Avnur, VP of Products at MongoDB. Ron indicated that all of MongoDB's customers wanted analytics, but that they hadn't decided whether to build something in-house or work with a partner.

This meant that MongoDB had gone from *nothing* to *magic* in just a few months.



### Pulling Back the Curtain

After the announcement, Jeff and I headed back to our sponsor booth, and Jeff asked me the most obvious question: *"How did they go from nothing to a BI connector that works with all possible BI tools in just a couple months?!?"*

I thought carefully about the question.

Among other problems that a BI connector would need to solve, it would have to be capable of efficiently executing SQL-like analytics on MongoDB. From my [deep](http://github.com/quasar-analytics/)[background](http://github.com/precog) in analytics, I knew that efficiently executing general-purpose analytics on modern databases like MongoDB is very challenging.

These databases support very rich data structures and their interfaces are designed for so-called *operational* use cases (not *analytical* use cases). The kind of technology that can leverage operational interfaces to run arbitrary analytics on rich data structures takes *years* to develop. It's not something you can crank out in two months.

So I gave Jeff my gut response: *"They didn't create a new BI connector. It's impossible. Something else is going on here!"*

I didn't know what, exactly. But in between shaking hands and handing out cards, I did some digging.

Tableau showed a demo of their software working with the MongoDB BI Connector, which piqued my curiosity. Tableau has set the standard for visual analytics on relational databases, and their forward-thinking big data team has been giving NoSQL some serious thought.

Thanks to their relationship with MongoDB, Tableau issued a [press release](http://www.tableau.com/about/blog/2015/6/tableau-mongodb-visual-analytics-json-speed-thought-39557) to coincide with the MongoWorld announcement, which I found on their website.

I pored through this press release hoping to learn some new details. Burried deep inside, I discovered the faintest hint about what was going on:

> MongoDB will soon announce beta availability of the connector, with general availability planned around the MongoDB 3.2 release late this year. During MongoDB's beta, Tableau will be supporting the MongoDB connector on both Windows and Mac **via our PostgreSQL driver**.

These were the words that gave me my first clue: *via our PostgreSQL driver*. This implied, at a minimum, that MongoDB's BI Connector would speak the same "language" (*wire protocol*) as the PostgreSQL database.

That struck me as more than a little suspicious: was MongoDB actually re-implementing the *entirety* of the PostgreSQL wire protocol, including support for hundreds of PostgreSQL functions?

While *possible*, this seemed *extremely unlikely*.

I turned my gaze to Github, looking for open source projects that MongoDB might have leveraged. The conference Wifi was flaky, so I had to tether to my phone while I looked through dozens of repositories that mentioned both PostgreSQL and MongoDB.

Eventually, I found what I was looking for: [mongoose_fdw](https://github.com/asya999/mongoose_fdw/commits/master), an open source repository forked by Asya Kamsky (whom I did not know at the time, but her profile mentioned she worked for MongoDB).

The repository contained a so-called *Foreign Data Wrapper* (FDW) for the PostgreSQL database. The FDW interface allows developers to plug in other data sources, so that PostgreSQL can pull the data out and execute SQL on the data (NoSQL data must be flattened, null-padded, and otherwise dumbed-down for this to work properly for BI tools).

*"I think I know what's going on"*, I told Jeff. *"For the prototype, it looks like they might be flattening out the data and using a different database to execute the SQL generated by the BI software."*

*"What database?"* he shot back.

*"PostgreSQL."*

Jeff was speechless. He didn't say a word. But I could tell *exactly* what he was thinking, because I was thinking it too.

*Shit. This is bad news for MongoDB. Really bad.*



--------

## PostgreSQL: The MongoDB Killer

PostgreSQL is a popular open source relational database. So popular, in fact, it's currently [neck-and-neck with MongoDB](http://db-engines.com/en/ranking).

The database is *fierce competition* for MongoDB, primarily because it has acquired some of the features of MongoDB, including the ability to store, validate, manipulate, and index [JSON documents](https://en.wikipedia.org/wiki/JSON). Third-party software even [gives it the ability](https://www.citusdata.com/) to scale horizontally (or should I say, hu*mongo*usly).

Every month or so, someone writes an article that recommends PostgreSQL over MongoDB. Often, the article goes viral and skyrockets to the top of hacker websites. A few of these articles are shown below:

- [Goodbye MongoDB. Hello PostgreSQL](http://developer.olery.com/blog/goodbye-mongodb-hello-postgresql/)
- [Postgres Outperforms MongoDB and Ushers in New Developer Reality](http://www.enterprisedb.com/postgres-plus-edb-blog/marc-linster/postgres-outperforms-mongodb-and-ushers-new-developer-reality)
- [MongoDB is dead. Long live Postgresql :)](https://github.com/errbit/errbit/issues/614)
- [Why You Should Never Use MongoDB](http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/)
- [SQL vs NoSQL KO. Postgres vs Mongo](https://www.airpair.com/postgresql/posts/sql-vs-nosql-ko-postgres-vs-mongo)
- [Why I Migrated Away from MongoDB](http://svs.io/post/31724990463/why-i-migrated-away-from-mongodb)
- [Why you should never, ever, ever use MongoDB](http://cryto.net/~joepie91/blog/2015/07/19/why-you-should-never-ever-ever-use-mongodb/)
- [Is Postgres NoSQL Better than MongoDB?](http://www.aptuz.com/blog/is-postgres-nosql-database-better-than-mongodb/)
- [Bye Bye MongoDB. Guten Tag PostgreSQL](https://www.userlike.com/en/blog/2015/10/09/bye-by-mysql-and-mongodb-guten-tag-postgresql)

The largest company commercializing PostgreSQL is [EnterpriseDB](http://enterprisedb.com/) (though there are plenty of others, some older or just as active), which maintains a [large repository of content](http://www.enterprisedb.com/nosql-for-enterprise) on the official website arguing that PostgreSQL is a better NoSQL database than MongoDB.

Whatever your opinion on that point, one thing is clear: MongoDB and PostgreSQL are locked in a vicious, bloody battle for mind share among developers.



--------

## From Prototype to Production

As any engineer worth her salt will tell you, *prototypes aren't for production*.

Even if MongoDB *was* using PostgreSQL as a prototype BI connector, maybe some brilliant MongoDB engineers were locked in a room somewhere, working on a standalone production version.

Indeed, the way Tableau worded their press release even implied the dependency on the PostgreSQL driver *might* be temporary:

> **During MongoDB's beta**, Tableau will be supporting the MongoDB connector on both Windows and Mac via our PostgreSQL driver.

Perhaps, I thought, the 3.2 release of MongoDB would ship with the *real deal*: a BI connector that exposes the rich data structures that MongoDB supports (instead of flattening, null-padding, and throwing away data), executes all queries 100% in-database, and has no dependencies on competing databases.

In July, more than a month after MongoWorld, I dropped by MongoDB's offices in Palo Alto during a business trip. And I was very encouraged by what I learned.


--------

## A Trip to MongoDB

By Palo Alto's standards, MongoDB's office is quite large.

I had seen the company's sign during previous trips to the Valley, but this was the first time I had a chance to go inside.

The week before, I was chatting with Asya Kamsky and Ron Anvur by email. We were discussing my company's [open source work](http://quasar-analytics.org/) in executing advanced analytics on rich data structures directly inside MongoDB.

Since we happened to be in Palo Alto at the same time, Asya invited me over to chat over catered pizza and office soda.

Within the first few minutes, I could tell that Asya was smart, technical, and detail-oriented — exactly the traits you'd hope for in a product manager for a highly technical product like MongoDB.

I explained to Asya what my company was doing, and helped her get our open source software up and running on her machine so she could play with it. At some point, we started chatting about BI connectors for MongoDB, of which there were several in the market (Simba, DataDirect, CData, and others).

We both seemed to share the same view: that BI software needs to gain the ability to understand more complex data. The alternative, which involves dumbing down the data to fit the limitations of older BI software, means throwing away so much information, you lose the ability to solve [key problems](http://slamdata.com/whitepapers/characteristics-of-nosql-analytics-systems/) in NoSQL analytics.

Asya thought a BI connector for MongoDB should expose the native MongoDB data structures, such as arrays, without any flattening or transformations. This characteristic, which I have termed *isomorphic data model*, is one of the key requirements for a general-purpose NoSQL analytics, a topic I've [written about](http://www.infoworld.com/article/2983953/nosql/how-to-choose-a-nosql-analytics-system.html) extensively.

I was very encouraged that Asya had independently come to the same conclusion, and felt confident that MongoDB understood the problem. I thought the future of analytics for MongoDB looked very bright.

Unfortunately, I could not have been more wrong.

--------

## MongoDB: For Giant ~~Ideas~~Mistakes

Delighted that MongoDB was on the right track, I paid little attention to the BI connector for the next couple of months, though I did exchange a few emails with Asya and Ron.

Heading into September, however, I encountered utter silence from the product team at MongoDB. After a few weeks of unreturned emails, I grew restless, and started poking around on my own.

I discovered that Asya had forked a project called [Multicorn](https://github.com/asya999/Multicorn), which allows Python developers to write Foreign Data Wrappers for PostgreSQL.

*Uh oh*, I thought, *MongoDB is back to its old tricks.*

More digging turned up the holy grail: a new project called [yam_fdw](https://github.com/asya999/yam_fdw) (Yet Another MongoDB Foreign Data Wrapper), a brand new FDW written in Python using Multicorn.

According to the commit log (which tracks changes to the repository), the project had been built recently, after my July meeting with Asya Kamsky. In other words, this was *post-prototype* development work!

The final nail in the coffin, which convinced me that MongoDB was planning on shipping the PostgreSQL database as their "BI connector", happened when someone forwarded me a [video on YouTube](https://www.youtube.com/watch?v=0kwopDp0bmg), in which Asya demoed the connector.

Worded very cautiously, and omitting any incriminating information, the video nonetheless ended with this summary:

> The BI Connector receives connections and can speak the **same wire protocol that the Postgres database****does**, so if your reporting tool can connect via ODBC, we will have an ODBC driver that you will be able to use from your tool to the BI Connector.

At that point, I had zero doubt: the production version of the BI connector, to be shipped with MongoDB 3.2, was, in fact, the PostgreSQL database in disguise!

Most likely, the actual logic that sucked data out of MongoDB into PostgreSQL was a souped-up version of the Python-based Multicorn wrapper I had discovered earlier.

At this point, no one at MongoDB was returning emails, which to any sane person, would have been enough to call it quits.

Instead, I decided to give it one more try, at the MongoDB Days conference on December 2, just one week before the release of 3.2.

Eliot Horowitz was delivering a keynote, Asya Kamsky would be speaking, and Ron Avnur would probably attend. Possibly, even Dev himself might drop by.

That's when I'd have my best chance of convincing MongoDB to ditch the BI connector shenanigans.


--------

## MongoDB Days 2015, Silicon Valley

Thanks to the wonderful marketing team at MongoDB, and based on the success of a similar talk I gave in Seattle at a MongoDB road show, I had a 45 minute presentation at the MongoDB Days conference.

My *official* purpose at the conference was to deliver my talk on MongoDB-powered analytics, and make users aware of the open source software that my company develops.

But my *personal* agenda was quite different: convincing MongoDB to can the BI connector before the impending 3.2 release. Failing that lofty and most likely *delusional* goal, I wanted to confirm my suspicions about the connector.

On the day of the conference, I went out of my way to say hello to old and new faces at MongoDB. Regardless of how much I may disagree with certain product decisions, there are many amazing people at the company just trying to do their jobs.

I had gotten sick a few days earlier, but copious amounts of coffee kept me (mostly) awake. As the day progressed, I rehearsed my talk a few times, pacing the long corridors of the San Jose Convention Center.

When the afternoon rolled around, I was ready, and gave [my talk](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) to a packed room. I was excited about how many people were interested in the esoteric topic of [visual analytics on MongoDB](http://www.slideshare.net/jdegoes/slamdata-how-mongodb-is-powering-a-revolution-in-visual-analytics) (clearly the space was growing).

After shaking hands and exchanging cards with some of the attendees, I went on the hunt for the MongoDB management team.

I first ran into Eliot Horowitz, moments before his keynote. We chatted kids and food, and I told him how things were going at my company.

The keynote started sharply at 5:10. Eliot talked about some of the features in 3.0, since a lot of companies are apparently stuck on older versions. He then proceeded to give a whirlwind tour of the features of MongoDB 3.2.

I wondered what Eliot would say about the BI connector. Would he even mention it?

Turns out, the BI connector was a leading feature of the keynote, having its own dedicated segment and even a whiz-bang demo.

### The BI Connector

Eliot introduced the BI connector by loudly making the proclamation, *"MongoDB has no native analytics tools."*

I found that somewhat amusing, since I wrote a guest post for MongoDB titled [Native Analytics for MongoDB with SlamData](https://www.mongodb.com/blog/post/native-sql-analytics-mongodb-slamdata) *(Edit: MongoDB has taken down the blog post, but as of 15:30 MDT, it's [still in the search index](https://www.mongodb.com/blog?utf8=✓&search=slamdata#))*. SlamData is also a MongoDB partner and sponsored the MongoDB Days conference. 

Eliot seemed to stumble a bit when describing the purpose of the BI connector (getting actions from... actionable insights? *Pesky analytics*!). He looked relieved when he handed the presentation over to Asya Kamsky, who had prepared a nice demo for the event.

During the presentation, Asya seemed uncharacteristically nervous to me. She chose every word carefully, and left out all details about what the connector was,  only covering the non-incriminating parts of how it worked (such as its reliance on DRDL to define MongoDB schemas). Most of the presentation focused not on the BI connector, but on Tableau (which, of course, demos very well!).

All my feedback hadn't even slowed the BI connector down.

### Pulling Out All the Stops

After the keynote, the swarm of conference attendees proceeded to the cocktail reception in the adjacent room. Attendees spent most of their time talking to other attendees, while MongoDB employees tended to congregate in bunches.

I saw Ron Avnur chatting with Dan Pasette, VP of Server Engineering, a few feet from the keg of Lagunitas IPA they were serving attendees.

Now was the time to act.

The 3.2 release was coming out in mere days. No one at MongoDB was returning emails. Eliot had just told the world there were no native analytics tools for MongoDB, and had positioned the BI connector as a revolution for NoSQL analytics.

With nothing to lose, I walked up to Ron, inserted myself into the conversation, and then began ranting against the BI connector in what was probably a two-minute, highly-animated monologue.

I told him I expected more from MongoDB than disguising the PostgreSQL database as the magical solution to MongoDB analytics. I told him that MongoDB should have demonstrated integrity and leadership, and shipped a solution that supports the rich data structures that MongoDB supports, pushes all computation into the database, and doesn't have any dependencies on a competing database.

Ron was stunned. He began to defend the BI connector's "pushdown" in vague terms, and I realized this was my chance to confirm my suspicions.

*"Postgres foreign data wrappers support barely any pushdown,"* I stated matter-of-factly. *"This is all the more true in the Multicorn wrapper you're using for the BI connector, which is based on an older Postgres and doesn't even support the full pushdown capabilities of the Postgres FDW."*

Ron admitted defeat. *"That's true,"* he said.

I pushed him to defend the decision. But he had no answer. I told him to pull the stop cord right now, before MongoDB released the "BI connector". When Ron shrugged off that possibility, I told him the whole thing was going to blow up in his face. *"You might be right,"* he said, *"But I have bigger things to worry about right now,"* possibly referring to the upcoming 3.2 release.

We had a beer together, the three of us. I pointed to Dan, *"This guy's team has built a database that can actually do analytics. Why aren't you using it in the BI connector?"* But it was no use. Ron wasn't budging.

We parted ways, agreeing to disagree.

I spotted Dev Ittycheria from across the room, and walked over to him. I complimented the work that the marketing department was doing, before moving on to critique product. I told Dev, *"In my opinion, product is making some mistakes."* He wanted to know more, so I gave him my spiel, which I had repeated often enough to know by heart. He told me to followup by email, and of course I did, but I never heard back.

After my conversation with Dev, it finally sunk in that I would not be able to change the course of MongoDB 3.2. It would ship with the BI connector, and there wasn't a single thing that I could do about it.

I was disappointed, but at the same time, I felt a huge wave of relief. I had talked to everyone I could. I had pulled out all the stops. I had given it my all.

As I left the cocktail reception, and headed back to my hotel, I couldn't help but speculate on why the company was making decisions that I so strongly opposed.

## MongoDB: An Island of One

After much reflection, I now think that MongoDB's poor product decisions are caused by an inability to focus on the core database. This inability to focus is caused by an inability to cultivate a NoSQL ecosystem.

Relational databases rose to dominance, in part, because of the astounding ecosystem that grew around these databases.

This ecosystem gave birth to backup, replication, analytics, reporting, security, governance, and numerous other category-defining applications. Each depended on and contributed to the success of the others, creating network benefits and high switching costs that are proving troublesome for modern-day NoSQL vendors.

In contrast, there's virtually *no ecosystem* around MongoDB, and I'm not the only one to [notice this fact](http://slamdata.com/blog/2014/12/09/where-is-the-nosql-ecosystem.html).

Why isn't there an ecosystem around MongoDB?

My snarky answer is that because, if you are a MongoDB partner that provides native analytics for MongoDB, the CTO will get up on stage and say there are no tools that provide native analytics for MongoDB.

More objectively, however, I think the above is just a symptom. The *actual problem* is that the MongoDB partner program is totally broken.

The partner team at MongoDB reports directly to the Chief Revenue Officer (Carlos Delatorre), which implies the primary job of the partner team is to extract revenue from partners. This inherently skews partner activities towards large companies that have no vested interest in the success of the NoSQL ecosystem (indeed, many of them produce competing relational solutions).

Contrast that with small, NoSQL-centric companies like SlamData, Datos IO, and others. These companies succeed *precisely* in the case that NoSQL succeeds, and they provide functionality that's standard in the relational world, which NoSQL databases *need* to thrive in the Enterprise.

After being a partner for more than a year, I can tell you that almost no one in MongoDB knew about the existence of SlamData, despite the fact that SlamData acted as a powerful incentive for companies to choose MongoDB over other NoSQL databases (e.g. MarkLogic), and an enabler for companies considering the switch from relational technology (e.g. Oracle).

Despite the fact that partners try, MongoDB appears completely unconcerned about the joint revenue and sales opportunities presented by NoSQL-centric partners. No reseller agreements. No revenue sharing. No sales one-pagers. No cross-marketing. Nothing but a logo.

This means that organizationally, MongoDB ignores the NoSQL-centric partners who could most benefit them. Meanwhile, their largest customers and prospects keep demanding infrastructure common to the relational world, such as backup, replication, monitoring, analytics, data visualization, reporting, data governance, query analysis, and much more.

This incessant demand from larger companies, combined with the inability to cultivate an ecosystem, forms a *toxic combination*. It leads MongoDB product to try to *create its own ecosystem* by building *all possible products*!

Backup? Check. Replication? Check. Monitoring? Check. BI connectivity? Check. Data discovery? Check. Visual analytics? Check.

But a single NoSQL database vendor with finite resources cannot possibly build an ecosystem around itself to compete with the massive ecosystem around relational technology (it's far too expensive!). So this leads to distractions, like MongoDB Compass, and "sham" technology, like the BI connector.

What's the alternative? In my humble opinion, it's quite simple.

First, MongoDB should nurture a vibrant, venture-funded ecosystem of NoSQL-centric partners (*not* relational partners with deep pockets!). These partners should have deep domain expertise in their respective spaces, and all of them should succeed precisely in the case that MongoDB succeeds.

MongoDB sales reps and account managers should be empowered with partner-provided information that helps them overcome objections and reduce churn, and MongoDB should build this into a healthy revenue stream.

Second, with customer demand for related infrastructure satisfied by NoSQL-centric partners, MongoDB should focus both product *and* sales on the core database, which is how a *database vendor* should make money!

MongoDB should develop features that have significant value to Enterprise (such as ACID transactions, NVRAM storage engines, columnar storage engines, cross data center replication, etc.), and thoughtfully draw the line between Community and Enterprise. All in a way that gives *developers* the same capabilities across editions.

The goal should be for MongoDB to drive enough revenue off the database that product won't be tempted to invent an inferior ecosystem.

You be the judge, but I think it's pretty clear which is the winning strategy.

## Bye-Bye, MongoDB

Clearly, I cannot get behind product decisions like shipping a competing relational database as the definitive answer to analytics on a post-relational database like MongoDB.

In my opinion, this decision is bad for the community, it's bad for customers, and it's bad for the emerging space of NoSQL analytics.

In addition, to the extent it's not done with *full transparency*, it's also bad for integrity, which is a pillar on which *all companies* should be founded (especially open source companies).

So with this post, I'm officially giving up.

No more frantic emails to MongoDB. No more monopolizing management at MongoDB cocktail parties. No more sharing my opinions in private with a company that doesn't even return emails.

Been there, done that, didn't work.

I'm also, obviously, blowing the whistle. By the time you're reading this, the whole world will know that the MongoDB 3.2 BI Connector is the PostgreSQL database, with some glue to flatten data, throw away bits and pieces, and suck out whatever's left into PostgreSQL.

What does all this mean for companies evaluating MongoDB?

That's your call, but personally, I'd say if you're in the market for a NoSQL database, you need legacy BI connectivity, and you're also considering PostgreSQL, you should probably just pick PostgreSQL.

After all, MongoDB's *own answer* to the problem of analytics on MongoDB is to pump the data out of MongoDB, flatten it out, and dump it into PostgreSQL. If your data is going to end up as flat relational data in PostgreSQL, why not start out there, too? Kill two birds with one stone!

At least you can count on the PostgreSQL community to innovate around NoSQL, which they've been doing for years. There's zero chance the community would package up the MongoDB database into a sham "PostgreSQL NoSQL" product, and call it a revolution in NoSQL database technology.

Which is, sadly, *exactly* what MongoDB has done in reverse.

--------

*The Shame photo taken by [Grey World](https://www.flickr.com/photos/greyworld/), copyright Grey World, and licensed under [CC By 2.0](https://creativecommons.org/licenses/by/2.0/).*