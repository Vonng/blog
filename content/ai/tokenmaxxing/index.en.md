---
title: "Burning Hundreds of Millions of Tokens a Day. Then What?"
date: 2026-04-13
author: vonng
summary: >
  Once token burn turns from usage exhaust into a KPI and leaderboard, it quickly mutates into theater. Don't post fuel burn. Post where you got to.
tags: [AI, Agent]
ai: true
---

My friend Jiang recently got obsessed with flexing in group chat about burning hundreds of millions of tokens a day. What was he doing with them? One minute it was some ontology database, the next he had an agent rebuilding Pigsty in Go under the name Bigsty. He would drop a screenshot into the chat and announce, "Burned another XXX tokens." Same energy as posting your run mileage on social media. I could only smile.

------

## Silicon Valley's New Sport: Tokenmaxxing

Last week, a Meta internal leaderboard called **Claudeonomics** leaked. The name alone is funny enough: naming your own internal leaderboard after a competitor, Anthropic's Claude, is a kind of performance art.

The leaderboard covered Meta's 85,000 employees. Total usage over 30 days exceeded 60 trillion tokens. The number one user averaged 281 billion tokens by themselves. The system even had a badge ladder, from Bronze to Emerald, with titles ranging from "Cache Wizard" to "Session Immortal." The top one was called **Token Legend**.

Legendary indeed.

How did people climb the board? Some employees had AI agents idle for hours on fake "research tasks" just to farm volume. Two days after the leak, Meta shut the leaderboard down and left a note that basically said: this was supposed to be fun, but the data leaked, so we're turning it off for now.

Meta is not alone. OpenAI reportedly has a similar internal leaderboard, and someone there burned 210 billion tokens in a single week. Silicon Valley now has a name for the phenomenon: **Tokenmaxxing**.

Plenty of executives are cheering it on. Jensen Huang said at GTC that every engineer should have an annual token budget worth roughly half their base salary. If an engineer making $500,000 a year has not burned at least $250,000 of tokens, he says he would feel "deeply uncomfortable." Shopify's CEO put it more bluntly: use AI or do not work here. Anonymous employees say some companies already impose weekly AI-usage minimums, and if you miss them, you are out.

Just like that, a new office-politics movement was born.


--------

## Goodhart Is Never Absent

Management theory has a classic name for this kind of thing: **Goodhart's Law**.

> **Once a metric becomes a target, it stops being a good metric.**

Token consumption is a process metric. People took it as a proxy for "depth of AI use" and "productivity improvement." From proposal to corruption, the whole thing took less than a quarter. It may be one of the fastest-decaying KPIs in management history.

Wharton professor Ethan Mollick commented on this by citing an even older paper: Steven Kerr's 1975 classic, *On the Folly of Rewarding A, While Hoping for B*. What companies actually want is **higher productivity**. What they are rewarding is **token burn**. Is there a verified causal link between the two? No. People just assume "more use = better use" and build a leaderboard on top of that.

Burning tokens is easy. Give an agent an impossible task, "write me an operating system, and do not stop if you fail," run a few copies in parallel, and you can burn any amount of tokens you like in a day. I would bet that if the rule is "whoever burns the most tokens wins," an intern can beat Linus Torvalds.

How is this any different from measuring programmers by **lines of code**? I can `npm install` a scaffolding stack and drop millions of lines into a repo instantly. Push that to GitHub and I look incredibly productive. Any respectable software company abandoned LOC metrics a long time ago. Insiders laugh at this stuff, but outside managers keep falling for it.

If you insist on an analogy, this is **measuring drivers by fuel consumption**. A skilled driver uses less fuel and gets there faster. A bad driver floors it and still gets lost. Who has the higher fuel burn?


--------

## Who Benefits When You Burn More?

Ask one simple question: who gains the most from Tokenmaxxing?

**AI vendors and cloud vendors.**

Ramp's data shows enterprise token spending has grown 13x since January 2025. Jensen Huang pushing token budgets really means "buy more of my GPUs." Sam Altman's dream of "Universal Basic Compute" also translates pretty cleanly to "everyone pays me an electricity bill."

This is the shovel seller telling everyone to dig harder. Every token corresponds to real GPU time and real electricity. An idle agent produces no value, but the power meter is very real. Burning tokens on meaningless tasks is as absurd as turning on the faucet, watching the water run, and deciding that counts as "using water productively."

To be fair, this kind of performative consumption does amplify the bubble signal around AI demand. CNBC has already asked the obvious question: if a meaningful chunk of Silicon Valley's AI usage is just leaderboard farming, how much of the demand growth that Wall Street sees is real?

My own view is still that this is a genuine productivity revolution. Tokenmaxxing adds some froth, but the underlying value creation is real. The bubble can deflate. The trend is not reversing.


--------

## What Is Worth Spending Tokens On?

I have two MAX subscriptions myself, and I usually burn them close to the limit every week. That works out to roughly $450 a month buying about $22,000 worth of compute. I almost never look at how many tokens I burned. I just use up the subscriptions and move on. I had considered opening a couple more, but Codex recently doubled its quota, so it is mostly enough for now.

I have used those tokens to get real work done. In the last two days alone, I added more than 40 new PostgreSQL extensions, bringing Pigsty's extension catalog to 503. I also took over the abandoned open-source MinIO effort, crossed 1,000 stars and 10,000 downloads, and even made the Hacker News front page for a few hours. I translated the PostgreSQL website into Chinese, then gathered and organized documentation for 500 extensions and several important ecosystem projects, with English translations where needed. That is concrete output. The subscription fee was absolutely worth it.

The common thread is simple: every one of those tasks had a **clear, verifiable deliverable**. How many extensions got added? The number is right there. Is the translation good? Readers can tell immediately. Does the code run? CI will answer that. How much impact did it have? Look at stars, PV, and UV.

Now compare that to what the Tokenmaxxing crowd is doing. They ask an agent to "write an operating system," let it run all night, and wake up to a pile of garbage code. Or they send it off to "do deep research," let it spin for hours, and get back a report nobody will read. The token counter spins fast, and so does `rm -rf`. That is not AI usage. That is energy waste.

Are you using a tool to hit a goal, or using a tool for the sake of using the tool? The first is productivity. The second is performance art.


-------

## Individuals vs. Organizations: A Structural Gap

The logic is obvious enough. So why does Tokenmaxxing still spread so easily inside large companies?

Because when an individual, or a one-person company, uses AI, the process is driven by **output**. How many articles got translated? How much usable code got written? What problem got solved? You know the answer directly. No proxy metric is needed, and you cannot really fool yourself.

Organizations are different. Mediocre managers cannot directly perceive the quality of everyone's output, so they fall back to quantifiable intermediate metrics for evaluation and incentives. Those intermediate metrics are exactly the things that are easiest to game. That is the structural defect of bureaucracy. Lines of code, PR count, meeting hours, and now token burn: same play, different actor.

To be fair, forcing AI adoption during the 0-to-1 phase is understandable. A lot of people are inert; without a push, they will not move. But the moment it becomes a leaderboard or a performance metric, the whole thing slides into absurdity.

In the end, this management failure is only a transitional phase. Just as respectable software companies abandoned lines-of-code metrics, future evaluation of AI usage will return to output itself:
what did your tokens **produce**, what did you deliver, and how much time and cost did you save?

As for Jiang's screenshots in group chat, I only have one line for him:

**Don't post fuel burn. Post where you got to.**
