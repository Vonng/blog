---
title: "Why Are People Who Leave Big Tech So Useless?"
date: 2026-08-14
authors: [vonng]
summary: >
  People who leave Big Tech are not stupid. They have simply spent too long using a rented mental map. Only after leaving the platform do they discover that the map has to be returned.
tags: [Cloud, Software Engineering, Architecture, Career]
---

A cutting remark supposedly from Sam Altman has been making the rounds online: by the time people leave a big company, their ambition, aspiration, and capacity to think have withered to almost nothing. Tell one of them about something that could change an industry, and their first question is who has to approve it.

That rings painfully true to me, because I have seen it far too often. There are exceptions, but not many.

The comments predictably split into two camps. One says, “Of course—they were just cogs in a machine.” The other says, “Sour grapes. They make three times what you do.”

Neither side has much to offer. Reducing the whole thing to “the people just aren’t good enough” is the easiest explanation of all—and the least informative.
The question worth asking is different: what, exactly, turns a smart, hardworking person who made it through round after round of screening into this?

---

## TL;DR

Here is the conclusion up front: people who leave Big Tech are not useless. They have simply spent too long using a rented **mental map**, believing it was their own.

The defining technique of a modern organization is decomposition: breaking a whole into pieces small enough for each person to own just one. The benefit is efficiency; the cost is that no one understands the whole anymore.
As a result, “understanding the whole” no longer grows out of your own lived experience. It has to be issued to you by the organization: OKRs, technology radars, promotion reviews, internal briefings, and vendor white papers. Everything it issues to you has to be returned when the contract expires.

![An engineer holding an incomplete map in a digital jungle](featured.webp)

---

## A Pig and a Cannon

A hunter in a tribal society who wants meat must hunt the animal, skin it, butcher it, light the fire, cook the meat, and eat it. From living animal to full stomach, the entire chain is in his hands. Nobody ever issued him a copy of *Hunting Best Practices*. He does not need one.

Goethe was no physician, but he observed surgical operations and understood what he saw. He disagreed with Newton’s optics, so he developed a theory of color himself. To him, the world was a whole.

Next comes the worker in a Krupp steel mill. He performs his step quickly and well, working to a tolerance of a few millimeters and turning out a part every few minutes—a hundred times more precise than the tribal hunter. But he has no idea how an entire cannon is made, nor does he need to. As for how that cannon relates to Germany’s place in the world, none of that comes from his own experience. It comes from newspapers, textbooks, and speeches.

What disappeared between the tribal hunter and the Krupp worker is what I will call a **mental map**: the picture in your head of how the whole thing actually works.

The hunter assembled his map piece by piece. It is crude, but complete, and nobody can take it away. The Krupp worker’s map was issued to him.

The trade was obviously worth making. Humanity traded away the map for a hundredfold increase in output. A good deal. The only problem is that, even today, most people do not realize what they paid.

No one has explained this more clearly than Zygmunt Bauman in *[Modernity and the Holocaust](https://www.wiley-vch.de/en/areas-interest/humanities-social-sciences/sociology-12so/social-theory-12so1/modernity-and-the-holocaust-978-0-7456-0685-9)*, published in 1989. His question was this: how did Auschwitz emerge from the country with Europe’s most advanced industry and strongest rule-of-law tradition?

The standard answers at the time were a breakdown of civilization, a return of barbarism, or a pathology in the national character. Bauman said they were all wrong. This was not a failure of modern civilization, but a product of it. Everything it required was an achievement modernity took pride in: bureaucracy, fine-grained division of labor, process-driven management, and the ability to decompose a complex problem into executable tasks.

I am not equating engineering screwups with the Holocaust; the scales are incomparable. I am borrowing only the shape of the argument: **when something is broken into sufficiently small pieces and each person handles only one, the link between your action and its consequences is severed.**

You cannot see the consequences because they fall outside your box.

Bauman used the phrase “free-floating responsibility.” Everyone in the chain is accountable only to a superior and only for their own box. Responsibility therefore drifts around the organization: everyone touches some of it, but none bears its full weight. There is an even harsher point. Once something enters a process, every question of whether it *should* be done is reformulated as how to do it with the fewest resources. Option A or B? How much will it cost? How many weeks will it take? How many nines in the SLA? Right and wrong are replaced by efficiency, a purely technical criterion that lets everyone keep their head down.

In everyday corporate language, that becomes three sentences:

> That isn’t owned by our team.
>
> The architecture team hasn’t scheduled it.
>
> My metrics are on target.

Not one of those statements is false. Each is precise. Taken together, they account for the entire incident. Yet the postmortem finds that nobody failed to do their job.

The failure lives in no one’s job description. It lives in the seams between job descriptions. And the great talent of the modern organization is to divide systems into responsibilities: the finer the divisions, the smoother the management—and the more seams it creates.

---

## The Map Is Issued to You

People today find it difficult to assemble a complete map from lived experience alone.

If you cannot build one, someone else has to issue one to you.

We all know how Big Tech issues its maps: the annual strategy presentation, quarterly OKR alignment, internal technology radars, architecture committee rulings, cloud-native evangelism, competitors’ white papers, and an endless supply of beautifully worded intranet essays.

Spend five years immersed in that system and you will acquire an extraordinarily fluent, self-consistent, jargon-dense theory of “where the industry is headed.” You may have personally tested less than a tenth of it. The other nine-tenths is hearsay twice removed.

I am not speculating from the outside. I worked at Alibaba, Tantan, and Apple. The people I am talking about used to sit beside me.

Nothing illustrates the problem better than a promotion review.

The mechanism is intended to evaluate big-picture judgment. But over time, it settles into its own equilibrium: in this evaluation system, the thing you can optimize is the narrative, not the understanding. You must cut your own box cleanly out of the whole, package it, and present it with vision, depth, data, and a repeatable methodology. The cleaner the cut, the higher the score.

So everyone rationally optimizes the narrative. The skill you actually develop after years in Big Tech is packaging your local piece as the whole, not grasping the whole itself.

Inside the company, the two look almost identical. The difference appears only on the day you leave.

Some say people fail outside because the resources are gone: the platform’s reach, organizational resources, support from all the surrounding teams, and the other 90 percent of the complexity that someone else absorbed for you. Others say the problem is incentives: perhaps they can see the whole, but looking changes nothing and speaking up is pointless, so eventually they stop looking.

Both are true. But resources and incentives belong to the employer. You were never going to take them with you when you left.

Understanding is the one thing that should have been portable, yet somehow was not. That is why it is the only part worth discussing.

As the old saying goes, a plucked phoenix is no better than a chicken. People also have an ancient habit: the fortunate always invent a story about their good fortune, proving that it was not luck but their rightful due. While they are on the platform, they recast the platform’s tailwinds as personal ability. After they leave, every collision with reality becomes a run of bad luck. The same person tells two different stories in two different situations—and sincerely believes both.

That is why the person using the map is often the last to realize it was rented.

---

## Software Is Not Krupp

The logic above does not hold in software.

Why can a Krupp worker see only one step? Because making a cannon genuinely requires thousands of people. That is a hard physical constraint. No matter how ambitious he is, he cannot turn ore into a cannon by himself, much less build an entire workshop. Under those conditions, division of labor is not a conspiracy. It is the only possibility.

Software has no such constraint.

One person can hold an entire system in their head: from kernel parameters to the file system, from SQL to execution plans, from primary-replica setups to failover, from monitoring metrics to alerting rules, from backup strategy to recovery drills, all the way to how every line on the final bill was calculated.

I am not talking about the application layer. Hundreds of microservices, twenty years of shit code, and three technology stacks inherited through acquisitions—nobody can hold all of that in their head, nor is it worth trying. I mean the layer underneath.

Fred Brooks explained the distinction forty years ago in *[No Silver Bullet](https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf)*: there are two kinds of complexity, essential and accidental. Most business complexity is essential. It comes from the business itself and cannot be eliminated. But 90 percent of infrastructure complexity is accidental. It did not simply emerge; people chose and introduced it, one component at a time.

Forty years later, nobody is listening.

The layer I can hold in my own head is infrastructure. Above that—business, organization, compliance—I am just as blind as anyone else. There is no point pretending otherwise. Every map has a boundary. What matters is that you draw the boundary yourself, rather than letting someone else draw it for you.

---

## Complexity Has a Budget

Whether one person can hold the whole system in their head depends on two things: their capacity to understand it and the system’s complexity.

Human understanding has limits, and the human brain has received no meaningful upgrade in the past thousand years. That leaves only one variable we can control: complexity.

And complexity does not fall from the sky. People introduce it one decision at a time.

Dan McKinley’s *[Choose Boring Technology](https://mcfunley.com/choose-boring-technology)* contains what I consider one of the most practical engineering maxims in years: every company gets roughly three innovation tokens. Spend them however you like, but the total remains fixed for a long time.

Spend one on a two-year-old database, one on a service mesh, and one on a homegrown message broker. Congratulations: your budget is gone, and there is nothing left for the business.

An innovation token spent on infrastructure is the worst bargain of all. Infrastructure’s value never comes from novelty. It comes from **predictability**. Your only requirement is that, at 3 a.m., it behaves the way you expect. And the reason your expectation is correct is not that the system is simple, but that the map in your head matches it.

Conversely, every flashy component you insert into the architecture punches a hole in your map. You do not understand what is inside that hole, and you do not have time to learn. So you fill it with vendor documentation, community blog posts, and other people’s war stories. What fills the hole is not your experience, but someone else’s narrative.

The lower you go in the stack, the more boring the technology should be.

Linux, Nginx, PostgreSQL, and the S3 API have one thing in common: they have survived long enough for every trap to be known. That does not mean they have no traps. PostgreSQL’s XID wraparound, autovacuum tuning, and connection scaling still catch people today. The difference is that every one of those traps has been encountered, documented, and passed down. The unknowns are finite. The learning cost may be high, but it converges. With a two-year-old component whose documentation is stitched together from GitHub Issues, your map will always have a missing piece. The only thing that can fill it is faith.

Someone will ask: hasn’t AI slashed the cost of learning something new? Why worry about adding a few more components?

AI reduces the cost of the learning phase. It cannot reduce operational complexity, much less the coupling between components when something fails. At 3 a.m., a model can read the documentation for you. It cannot make sense of those layers of coupling for you. That requires a map that has already taken root in your head.

The real cost of architectural stunt work is not the server bill. It is willingly turning yourself back into a worker who knows only one step, just to show off.

---

## Someone Turned This Map into a Business

Most organizations solve the problem of not having a map by buying one.

The first layer consists of cloud services and SaaS. The two are fundamentally the same: you outsource a piece of the business along with your understanding of it.

For many companies, moving to the cloud was the first time they saw their cost structure clearly and gained real observability, because the cloud provider’s tooling was far better than the systems they had built themselves. They outsourced more than operations. They outsourced understanding too.

The sticker price appears on the bill. The hidden cost does not. From the day you sign the contract, everything you know about that part of the system is mediated by the vendor’s narrative. Whatever metrics the console displays, you assume those are the only metrics that exist. Whatever the documentation calls a best practice, you assume it really is a best practice. However many nines appear in the SLA, you assume that is your actual availability.

Most of the time, this causes no problem at all. It is often quite comfortable. The problem appears only on the day you genuinely need to make a judgment: during technology selection, capacity expansion, an outage, a price increase, or a migration. On that day, you discover that you cannot make the call. Not because you lack data, but because you lack a map.

A few days ago, I discussed *[The People Who Left the Cloud Made a Killing](/cloud/cloud-exit-2026/)* on Twitter. Someone replied that whether a company moves onto or off the cloud makes no difference to rank-and-file employees and means nothing to them. It is the boss’s concern; leaving the cloud is merely the boss trying to save money.

That response proves the point. It did not even occur to him that this might have something to do with his own capabilities. When outsourcing becomes thorough enough, the missing piece no longer feels like an absence.

The ultimate form of this business is Palantir.

Palantir is often described as a big data company or a defense software company. Both descriptions miss the point. What it sells is the mental map itself.

The central component in Foundry is called [**Ontology**](https://www.palantir.com/docs/foundry/architecture-center/ontology-system). In computer science, *ontology* is a standard term; there is no need to burden it with philosophy. But the fact that a company chose this word for its core product tells you what it believes it is selling. The product takes data scattered across ERP, MES, and CRM systems, hundreds of spreadsheets, and a dozen other internal systems and maps it into objects, properties, relationships, and actions, reconstructing a complete picture of how the company actually operates.

A conventional enterprise data platform sells pipelines. Palantir sells the map.

Its signature early delivery model makes the point even more clearly: the [Forward Deployed Engineer, or FDE](https://www.sec.gov/Archives/edgar/data/1321655/000119312520248369/d904406ds1a.htm). These were neither pre-sales engineers nor implementation consultants. They packed their bags and flew to a customer’s factory, base, or command center, where they embedded for months. They worked alongside factory workers and military officers, observed processes, asked questions, recorded everything that had never made it into a document, and then redrew how the customer’s organization operated. Palantir has spent years trying to productize this work because sending human beings into the field is exceedingly difficult to scale—which tells you just how valuable those human beings were.

What Palantir really sells is the person who can see the whole.

Some argue that it does not sell understanding, but the political legitimacy to cut across data silos, plus the sheer engineering labor of integration. Fine. That is worse. It means somebody inside these organizations wants to see the whole but is simply not allowed to.

A company employs tens of thousands of people, each working diligently inside their own box, with impeccable KPIs and perfect scores in promotion reviews. Yet put them all together and not one person can explain how the company operates. The same is true of armies and governments. So they have to buy the map from outside, whatever the price.

What they buy is still someone else’s map. It is far better than having none, far more useful, and far more respectable. But it is rented.

---

## AI Is the Mass-Market Version

Give two people the same problem and the same output. One glances at it and knows the sentence in the third paragraph is a hallucination, because it does not match the map in their head. The other cannot tell, because they have no map against which to check it.

The first uses AI to amplify judgment tenfold. The second uses it to eliminate the act of judgment altogether. After all, it sounds perfectly coherent, and it reads better than any white paper.

For someone with a map, AI is leverage. For someone without one, it is a substitute.

It will not close the gap. It will widen it beyond anything we have seen before.

---

## Rented or Owned

After that long detour, we return to the beginning.

A mental map can come from only two places: you build it yourself, or someone else issues it to you.

The issued version—from Big Tech, a cloud provider, a SaaS vendor, Palantir, or AI—is fast, polished, and prestigious. On most days, it is far more useful than the one you could assemble yourself.

Its only problem is that it is rented. When the price rises, you have no bargaining power. When it is withdrawn, you have no alternative. When it is wrong, you have no second frame of reference that tells you so.

The map you build yourself is slow, rough, and still bears the warmth of your hands. Its edges are marked by every trap you fell into along the way. But it is yours. It survives a layoff. It remains when the platform disappears, and it remains when the industry turns upside down.

In software, the cost of drawing your own map has become almost absurdly low. There are no physical constraints, every building block is open source, and the only remaining price is restraint: resisting the shiny toys and holding complexity firmly within the range you can understand end to end.

If that sounds too abstract, there is a very simple exercise. Set aside a weekend and bring up a complete stack from scratch. Use no managed services and no one-click scripts. Start with bare metal and continue until it can run a real workload. At every layer, ask yourself why you configured it that way, then answer the question. Once is enough. You will discover that you can draw the map yourself—and once you have, nobody can take it away.

So, back to the original question: why are people who leave Big Tech so useless?

They are not. They simply used a rented map for so long that they forgot it was rented.

Only when the contract expired did they discover they had to give it back.
