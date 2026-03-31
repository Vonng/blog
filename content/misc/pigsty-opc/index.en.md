---
title: "Pigsty Goes Global: 1.44M Visitors, Zero Ad Revenue"
date: 2026-03-19
author: |
  [Ruohang Feng](https://vonng.com)
summary: >
  Over the last 30 days, pigsty.io served 1.44 million unique visitors, 18.11 million page views, and 1.1 TB of traffic. For a one-person open source project, the real asset here is not ad inventory. It is trust.
tags: [Open Source, Startup, Pigsty]
---

Traffic on `pigsty.io` jumped by roughly an order of magnitude over the last month. I opened the Cloudflare dashboard today and had to stare at it for a second.

![Pigsty docs site traffic overview in Cloudflare](cloudflare-traffic.webp)

**1.44 million unique visitors, 18.11 million page views, 1.1 TB of traffic.**

That is over 30 days.
For the documentation site of an open source project maintained by one person.

I asked Claude to benchmark the numbers. Its answer was basically: this looks like the traffic profile of a mid-sized SaaS product.

![Traffic level analysis](traffic-analysis.webp)

Which is amusing, because I did not build a SaaS product.
I built a PostgreSQL distribution, and it is for local deployment.

So where is all this traffic coming from?

By country, the US is first with 13.98 million requests, far ahead of everyone else. Vietnam is second with 3.03 million, followed by the UK, France, Singapore, Germany, and then China in sixth place.
This is an open source project built by a Chinese developer, and Chinese traffic is only sixth.
The site reached users in 177 countries and regions. The UN only has 193 member states.

I still do not know why Vietnam is so enthusiastic, but several Vietnamese people added me on LinkedIn recently, so clearly something is happening there.

------

## No Ads, No Monetization

Claude also did the obvious back-of-the-envelope calculation.
At this traffic level, a vanilla Google AdSense setup would probably generate something like $5,000 to $10,000 per month.
If I sold sponsorship placements directly to database vendors, it could be several times higher.

![Estimated ad revenue](adsense-estimate.webp)

I did none of that.
No ads. No popups. 1.44 million people came and went, and I made exactly zero dollars from the traffic.

And this is only the international site, `pigsty.io`.
There is also the domestic `pigsty.cc` site behind a China CDN, and those numbers are not even included here.

That said, I am used to this pattern.
My WeChat public account is already one of the larger personal database accounts in China. The backend fills up with "business cooperation" messages every day, and I still have not taken a single sponsored deal.

------

## The GitHub Side of the Story

Of course, a decent amount of Cloudflare traffic is probably crawler traffic.
But even if only ten percent is real human traffic, that is still far beyond what I expected for an open source project.

And traffic is only one signal.
On GitHub, Pigsty has also been growing quickly and is about to cross 5,000 stars.

![Pigsty GitHub star growth](github-stars.webp)

Among PostgreSQL distributions, Pigsty is now third.
At this rate it should reach second before long.
Right now number one is EDB's CloudNativePG, but the two projects sit in different niches anyway: they are doing Kubernetes-native PG, while I am doing Linux-native PG.

![PostgreSQL distribution ranking](pg-distro-ranking.webp)

The difference is that EDB is one of the old giants of the PostgreSQL world, with a large team and a long list of contributors behind CloudNativePG.

Pigsty is just me.
Literally a **database one-man business**.
The fashionable term now is OPC: One Person Company.

------

## How Far Can One Person Go?

Within the Chinese PostgreSQL ecosystem, Pigsty is probably the open source project with the strongest international reach built by a domestic vendor or developer.
Its GitHub stars are already comfortably ahead of several PostgreSQL kernel projects backed by Alibaba, Huawei, and Tencent.

![Chinese PostgreSQL project comparison](china-pg-projects.webp)

![Star comparison across Chinese PostgreSQL projects](pg-project-comparison.webp)

Getting here as a solo builder is still a little surreal.

In a few weeks it will be exactly four years since I went independent.
Pigsty started as a one-person project.
Technology, product, docs, marketing, sales, consulting, delivery: I did all of it myself.

To be clear, it has not been easy.
But the timing helped. AI made it realistic for one person to do work that used to require a team.
If you want to run an OPC, this is a much better era than the one before it.

------

## Where Things Stand Now

Honestly, I like the current state of affairs.

The consulting business keeps growing and easily covers expenses. Customer retention is perfect. The global user base keeps growing organically. There is no fundraising pressure, no KPI theater, no boss, no morning standup.

I write the code I want to write, build the product I want to build, and work with customers worth working with.

Four years ago this was just a tool I built for myself.
Now it has users across 177 countries and regions.
That fact says something:

**if you make something genuinely good, the world will eventually find it.**

You do not necessarily need a team. You do not necessarily need a marketing budget.
Build something solid, put it out there, and let the tailwinds arrive when they arrive.

That is what open source does.
You give your best work away for free, and the world pays you back in its own currency.
That currency is not always money.
Often it is something more valuable:
**trust**.

![Users from 177 countries and regions](global-users.webp)

Trust from users in 177 countries and regions.

That is worth more than ad revenue.
