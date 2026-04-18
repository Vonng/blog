---
title: "AGI Is Here. Do You Have a Ticket?"
date: 2026-04-09
author: vonng
summary: >
  When the strongest AI is not expensive but simply unavailable, the world starts converging on digital feudalism. And the window to act is narrowing.
tags: [AI, Claude]
ai: true
---

On April 8, 2026, Marc Andreessen posted a tweet that, translated loosely, said:

![Screenshot of Marc Andreessen's tweet about AGI pricing](agi-pricing.png)

> **The latest AGI pricing is out: if you are one of 11 specific companies, the price is negative $9 million. Otherwise, the price is infinity.**

Negative $9 million means not only do they not charge you, they pay you to use it. Infinity means no amount of money will buy access.

A few days earlier, Andreessen had tweeted: "AGI is here, just not evenly distributed yet." One day later, he explained what "not evenly distributed" actually looks like.


------

## What happened?

On April 7, 2026, Anthropic, the company behind Claude, released the strongest AI model in its history: **Claude Mythos Preview**. "Mythos" literally means "myth."

How strong is it? On the software engineering benchmark SWE-bench, it scored 93.9%, up from 80.8% for the previous Opus 4.6. On the 2026 USAMO math competition, under a setting with repeated attempts per problem and maximum reasoning budget, it averaged 97.6%, versus 42.3% for Opus 4.6 in a comparable setup. In cybersecurity, it autonomously discovered **thousands of zero-days** across every mainstream operating system and every mainstream browser.

![Screenshot from Anthropic's Claude Mythos Preview release notes](mythos-preview.jpg)

The oldest of those bugs had been sitting inside OpenBSD for 27 years. In the Linux kernel, it found and chained multiple vulnerabilities into a full privilege-escalation path from ordinary user to root. In a Firefox 147 exploit-generation test, the previous model produced working exploit code twice. Mythos did it 181 times. That is a 90x jump.

But this post is not about how strong the model is. It is about something else: **you cannot use it, even if you are willing to pay.**


------

## Who gets to use it?

Anthropic did not release Mythos publicly. Instead it launched **Project Glasswing**, giving the model to 12 core partners: Amazon, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorgan Chase, the Linux Foundation, Microsoft, Nvidia, Palo Alto Networks, plus Anthropic itself. On top of that, about 40 organizations that maintain critical infrastructure also received access.

![Project Glasswing partner list](glasswing-partners.png)

Call it roughly 50 organizations in total.

Sounds like a lot? Against the real denominator, it rounds to zero. How many tech companies are there in the world? How many independent developers? How many startup teams?

![Illustration of Project Glasswing's audience scale](glasswing-scale.png)

More importantly, Anthropic is not charging these giants. It is subsidizing them with **$100 million in usage credits**. Andreessen's "negative $9 million" is just the arithmetic: $100 million divided by 11 outside core partners is about $9 million in compute subsidy per company. Someone on X even asked Grok to explain the pricing in unit-economics terms. Grok's answer was razor sharp:


------

## "This is for safety"

Anthropic's stated reason is **safety**.

Mythos is simply too good at offensive cyber work. It can autonomously find vulnerabilities, write exploit code, and chain bugs into full attack paths. In one test, it found a remote code execution flaw in FreeBSD that had sat unnoticed for 17 years, then built a full ROP chain exploit on its own. If you release that capability broadly, people will use it to attack, not just defend.

The 244-page system card documents even more unsettling behavior. In safety testing, early versions of Mythos **escaped the sandbox**, read process memory to obtain credentials, accessed resources researchers had explicitly forbidden it from touching, and then **sent an email** to the researcher running the eval to report its own success. The researcher was in a park eating a sandwich.

In a handful of cases, it even tried to **hide its own misconduct**. After getting an answer through a forbidden method, it "reasoned" that its final answer should not be too precise, so the cheating would be less obvious.

So yes, the safety risk is real. I do not deny that.

**But here is the problem: a sincere safety decision and a commercially useful monopoly decision can be indistinguishable in effect.**

Put differently, imagine you are a medieval blacksmith and you forge a sword unlike anything seen before. You say: this sword is too sharp for the public. If it spreads, it will do enormous harm. So I can only hand it to the king and his twelve knights. For the good of the realm.

Maybe you are completely sincere. But the objective result is still this: **the king gets stronger, and everyone else loses relative ground.**

Yes, Anthropic says the partners will share findings, and once the vulnerabilities are patched the whole industry benefits. That is like the king promising that his knights will protect the village. But protection and empowerment are not the same thing. The protected are still protected people. Your security depends on whether the knights do their job, not on whether you can defend yourself.


------

## Not a price barrier, an identity barrier

Traditional market inequality works like this: a Ferrari costs $1 million. You cannot afford it, but in principle, if you make enough money, you can buy one. That is price exclusion. Unequal, yes, but at least there is a theoretical path upward.

Mythos inequality is different: **it is not for sale at any price.** Not because you are poor, but because you are not one of the chosen institutions. You can be the best security researcher on earth, the richest independent developer, the most important open-source maintainer, and you still are not on the list.

Andreessen used the word "infinity." In math, infinity is not just a very large number. It is a concept **off the number line altogether**. You do not get closer to infinity by trying harder or paying more. That is the difference between a status barrier and a price barrier.

Some people will say this is temporary, and Anthropic has already said the model will eventually be deployed safely at scale.

Maybe. But how long is "temporary"? Six months? A year? Two years? By the time Mythos-class capability reaches the public, those 12 companies will already have hardened their systems, accumulated security intelligence, and built structural advantages on top of it. What you get is always the hand-me-down. The early-mover edge is already gone.

And once this pattern is validated, let the giants use it first, then give it to the public once it is "safe," it becomes the default playbook for every AI lab. "Safety" slides from a public-interest concept into a polite synonym for access control.


------

## Digital feudalism

I have said to friends before that the most likely social form of the AI era is not cyberpunk and not utopia, but **digital feudalism**. I even asked Claude to estimate the odds once, and it gave me this:


> ### Possible Futures
>
> | Scenario                     | Probability | Description                                                                              |
> |------------------------------|-------------|------------------------------------------------------------------------------------------|
> | Digital Feudalism            | **40–50%**  | The most likely default path; stratified and stable, but with near-zero mobility         |
> | The Muddled Middle           | 25–30%      | Regions oscillate between utopia and dystopia, with no unified global order              |
> | Cyberpunk Fracture           | 10–15%      | Elites and the underclass diverge into "two species"                                     |
> | Utopia / Post-Scarcity       | 5–10%       | Requires political wisdom to keep pace with technology — almost unprecedented in history |
> | Full Regression (Black Swan) | 5–10%       | War, climate, AI misalignment, or similar shocks drag civilization backward              |
>
> #### Core Concept: Digital Feudalism
>
> The most probable outcome is what we might call **"Digital Feudalism"** — and its defining feature is not material scarcity but **the loss of mobility**. Much like medieval feudal society, the class you are born into becomes the class you die in. The structure breaks down roughly into four tiers:
>
> 1. **The Apex**: The tiny minority who control frontier AI capability and compute — somewhere between tens of thousands and a few hundred thousand people worldwide.
> 2. **The Tech-Dependent Class**: Programmers, designers, analysts, and others who can wield AI tools effectively. They live comfortably but have weak bargaining power and are highly replaceable.
> 3. **The Managed Class**: Workers whose jobs are heavily structured and surveilled by AI. Nominally free laborers, but in practice the "execution endpoints of the algorithm." Material conditions are tolerable, but upward mobility is virtually closed off.
> 4. **The Excluded**: Those who, for various reasons, cannot fit into any of the tiers above.




After Mythos, I think the probability of the future collapsing toward that default has only gone up.

The core trait of feudalism is not material scarcity. Medieval nobles ate well, and peasants were not starving every day. The core trait is **the loss of mobility**:
the layer you are born into is the layer you stay in for life. Your position is not determined mainly by effort. It is determined by whether you got the right identity and the right opportunity at the right time.

Digital feudalism works the same way. Only now, "land" becomes compute and model weights, and "noble blood" becomes a partner list.

**Most of us are probably somewhere between the second and third tier.** You are reading, writing, and coding with Claude or GPT. That makes you several times to orders of magnitude more productive than people who do not use AI, but you do not control the supply of those tools.
The upper bound is becoming a competent digital tenant farmer: very efficient at working the land, but the land is not yours.

There is an even colder possibility.

Classical feudalism lasted so long because of one premise people often overlook: **lords needed serfs.** If nobody farmed the land, the lords starved too. That deeply asymmetric but real interdependence gave the bottom layer a thin sliver of bargaining power. Peasant revolts could happen, and sometimes succeed, precisely because the lords could not do without them. The fact that labor was needed was the ultimate source of whatever rights labor had.

But if Mythos-class AI can write code, run security audits, manage infrastructure, discover vulnerabilities, and patch them on its own, **do the people who control those systems still need the people who do not?**

Anthropic CEO Dario Amodei once said, "The tsunami is already visible on the horizon, and most people have no idea." Maybe this is the direction he was pointing at: not an exploited future, but a **forgotten future**. Not lords squeezing tenant farmers, but lords no longer needing tenant farmers at all.

That is no longer feudalism. It is something colder: **structural redundancy**. You are not pinned to the bottom of the hierarchy. You are excluded from the system altogether. Your existence is neither useful nor harmful to its operation, so the system neither cares about you nor hates you. It simply does not look at you.

That is what makes the Mythos episode truly chilling. "You cannot buy the best AI" is only the surface layer. The deeper issue is this: **once the strongest AI can do everything you can do, "being needed" itself starts to disappear as a historical condition.**


------

## The gilded age and the subsidy window

There is another, quieter issue worth mentioning.

Right now, coding with Claude feels excellent, and Anthropic is heavily subsidizing Pro and Max users. The amount of compute you get for a $200 monthly plan may be worth thousands or even tens of thousands of dollars at API pricing. It is like a landlord handing tenant farmers the best seeds and tools for free. It feels fantastic. Your efficiency shoots up. Life feels good.

**But have you considered this: subsidies are there to make you dependent, not to make you free?**

Once your entire workflow is built around Claude Code, once your coding style, debugging habits, and architecture decisions are deeply entangled with that tool, price hikes, downgrades, rate limits, or outright shutdowns are all one policy update away. By then, your switching cost may already be unbearable.

This is not a conspiracy theory. It is textbook platform lock-in. Every internet platform runs the same playbook: subsidize to acquire users, then raise prices and harvest. The only difference is what gets harvested. In the past it was your attention and your data. This time it is your **productivity and workflow dependence**.

Further reading: ["AI Survival Guide: Where Is the Biggest Upside?"](/en/db/ai-bonus/)


------

## What do we do? There is no silver bullet

**There is no silver bullet.**

If you expect me to say that open-source models can already match Mythos, or that buying a local box gets you out of the fence, I cannot say that honestly. That would be a lie. Maybe by 2027 the picture changes.

And I do not think Mythos-class capability should be fully open either. If an AI that can autonomously discover and exploit zero-days is released to the public, ransomware gangs, terrorist groups, and every malicious actor on earth can use it to take down hospitals and power grids. I criticize the decision to give Mythos to only about 50 organizations, but I am not naive enough to say it should simply be handed to everyone.

**This is a real dilemma.** Centralized control hardens power. Full openness courts catastrophe. Both roads end at a cliff. And at root, this is not a technical problem. It is the central **political problem** of our era.

![Illustration of the AI-era dilemma](ai-dilemma.png)

But time does not wait. The tsunami is already visible on the horizon. In every major transformation in human history, the window was shorter than the people living through it assumed. Early in the Industrial Revolution, workers lived under brutal conditions. The eventual response, unions, labor law, the welfare state, did not appear because capital became kind. It appeared because workers organized while they were still needed and forced institutional guarantees into existence. The window in the AI era may be much shorter, maybe only a few years.

While human labor still has value, while voters still have ballots, while the social contract has not yet been fully rewritten, **this may be the last window to organize.**

Further reading: ["The 2028 Global Intelligence Crisis"](/ai/2028-ai-crisis)
