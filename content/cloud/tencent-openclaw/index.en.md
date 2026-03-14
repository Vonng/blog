---
title: "Tencent Cloud 'Reduced' the Lobster King's Load by 180 GB"
date: 2026-03-12
author: vonng
summary: >
  Tencent Cloud mirrored OpenClaw's official skill marketplace into its own SkillHub and then claimed it was helping the upstream project. The incident turned into a case study in open-source manners, mirror ethics, and platform power.
tags: [Tencent Cloud, Open Source, AI, Agent]
---

> Dedicated to the open-source projects that Tencent kindly "helps."

## 1. Good news: the goose strikes again

On March 11, 2026, Tencent Cloud quietly launched a platform called **SkillHub**. It copied more than **13,000 skills** from OpenClaw's official marketplace, ClawHub, onto Tencent's own servers, with a tiny note in the corner saying "Skill data sourced from ClawHub."

![Tencent SkillHub says its data comes from ClawHub](mirror.webp)

Impressive. If you cite the source, it's a "mirror." If you don't, it's "original work."

## 2. The lobster king gets angry

The story first broke on X when SnowShadow (@Alfredxia) publicly asked OpenClaw founder Peter Steinberger whether he knew Tencent had copied the entire ClawHub marketplace.

![SnowShadow calling Tencent out on X](callout.webp)

Peter's response, paraphrased:

> "More or less. I even got emails from people complaining that my rate limits slowed down their scraping. They copy the project and support it in no way."

That line says everything. People were not only scraping his project. They were upset that his anti-abuse measures made the scraping less efficient.

Peter then tagged Tencent Hunyuan directly and asked, again paraphrased, whether they would consider helping instead of driving his infrastructure costs into five digits.

![Peter says Tencent pushed his server bill into five digits](bill.webp)

That number matters. A solo developer maintaining an open-source project suddenly gets hit with a five-figure hosting bill because a giant platform decides to mirror first and talk later.

## 3. Tencent responds with math

Tencent AI's response was textbook PR:

> "In the first week, we served 180 GB of traffic for users, while only pulling 1 GB from the official source through non-concurrent requests."

![Tencent AI's 180 GB response](response.webp)

Translated into plain English: once Tencent moved 13,000 skills onto its own servers, Chinese traffic naturally stopped hitting ClawHub. Tencent then proudly declared that it had saved the upstream project bandwidth.

> Editor's note: a 200 GB Tencent CDN traffic package is priced at roughly RMB 68, with internal cost far below that.

That logic is like opening a clone store across the street from someone else's shop and then saying, "Look, your foot traffic is down. I reduced your operating pressure."

Andy Stewart (@manateelazycat) called out the absurdity on X: Tencent was criticized for pushing the upstream bill higher, yet its answer was not apology or sponsorship, but a calculator.

![Community criticism of Tencent's response](criticism.webp)

Peter later clarified that he was not against mirrors in principle. He objected to Tencent doing it without communication, without an official arrangement, and without even the minimal courtesy of asking first.

## 4. Thirteen warlords circle the lobster

Tencent is not the only company that smelled opportunity in OpenClaw. People quickly compiled lists of Chinese internet giants building their own Claw variants, gateways, managed editions, and mobile wrappers.

The underlying logic is obvious:

> "It can sell model tokens and serve as a new user-input entry point. If you don't occupy that territory, someone else will."

To big platforms, the OpenClaw ecosystem is not just a tool. It is a **traffic entrance** and a user-acquisition channel. Tencent's move simply looked worse because it cloned the marketplace itself instead of merely building a client or deployment solution around it.

## 5. Closing thought

The core issue is simple: **a trillion-dollar company copied data maintained by an independent open-source developer, then argued it was helping.**

Open source does not mean "take whatever you want with zero human decency." You can mirror. You can build on top. But saying hello first, or offering sponsorship if you clearly benefit, is basic manners even when it is not a legal requirement.

Tencent says it wants to become a better ecosystem sponsor. Great. A practical first step would be paying Peter's server bill.

![Peter's GitHub Sponsors page](sponsors.webp)

All factual claims here are based on public reporting and public statements by the parties involved. Quoted remarks are paraphrased.
