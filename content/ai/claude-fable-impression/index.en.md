---
title: "Claude Fable First Impressions: The Pendulum Swings Back"
date: 2026-06-10
authors: [vonng]
summary: >
  Claude Fable is genuinely insightful and deserves to be called the new SOTA. But its high price, dynamic downgrades, limited subscription window, and mandatory data retention badly undermine the experience.
tags: [AI, Claude, Agent]
ai: true
---

This morning, Anthropic officially released its new **Claude Fable** model—the consumer-grade, nerfed version of the much-rumored Mythos. Since it was billed as an "[AGI-level model](/en/ai/agi-is-coming/)," I naturally tried it right away to see what it could actually do.

The short version: it really is strong, and it is the new SOTA. But it is expensive, and the way Anthropic is serving it up leaves a bad taste.

![Claude Fable launch announcement](claude-x.webp)

Two months ago, when the first word of the Mythos Preview emerged, I wrote ["AGI Is Here. Do You Have a Ticket?"](/en/ai/agi-is-coming/) about top-tier AI capabilities being locked away. That warning now looks prescient. This time, even the names make no attempt to hide it: **Mythos is kept for approved "lords"; Fable is told to the commoners.** It is the same underlying model, but Fable is the crippled, locked-down edition.

![Claude Fable benchmark comparison](benchmark.webp)

Before this release, I had already downgraded Claude to the $100 plan, where it mostly sat idle. Codex was my daily driver; Claude handled odd jobs and code review. After using Fable, my verdict is that Claude is back in the game. I immediately upgraded to the $200 Max plan. Across several real-world tasks, one quality stood out: **Fable is genuinely insightful and deserves to be called the new SOTA.**

Just as I wrote in ["Cancel Claude, Switch to Codex"](/en/ai/move-to-codex/), the crown keeps changing hands in AI. A new model takes the SOTA title every few months.

---

## Hands-On: Can It See What Codex Misses?

My test is deliberately simple: no benchmarks and no arena leaderboards. I give the model real work to review and see whether it can find problems that matter and propose concrete improvements.

My usual vibe-coding workflow pits two models against each other: **Codex 5.5 is the primary, and Claude 4.8 is the backup reviewer.** I do not sign off on a patch until both agree there is no room left to improve it. That makes my standard straightforward: if a new model can uncover fresh problems after the two-model process has already converged, it is meaningfully more capable. To me, that is far more persuasive than any score.

**Case one: reviewing MinIO CVE patches.** I asked Fable to review several security patches I had previously applied to the community fork of MinIO and look for further improvements. It found several new issues. When I took them back to Codex, Codex agreed that they were worth fixing.

![Review of MinIO CVE patches](minio-review.webp)

**Case two: PostgreSQL 19 support in pg_exporter.** I had previously asked Codex to make pg_exporter compatible with PostgreSQL 19 Beta 1 and add the new release's observability metrics. This time I had Fable do the job again, and its result was clearly better than Codex's previously converged version.

![Review of pg_exporter's PostgreSQL 19 support](pg-exporter-review.webp)

**Case three: improving Pigsty's PITR script.** I had previously written an emergency point-in-time recovery script for the database. I asked Claude Fable to review it again, and it filled in nearly every detail the earlier work had missed. Even after the script seemed comprehensive and Codex could improve it no further, Fable still found new opportunities.

![Review of Pigsty's PITR script](pitr-review.webp)

---

## The Catch: Great Model, Miserable Product

Of course, I also have plenty of complaints about the Fable launch.

**Gripe one: dynamic downgrades.** Fable includes anti-distillation and poisoning mechanisms, plus an infuriating dynamic downgrade system. Once the system detects AI-agent work, it deliberately drops you to a weaker model. Mid-session, Fable can abruptly fall back to Opus 4.8; even routine questions may trigger it. The resulting experience is frankly miserable.

For example, whenever I discussed one of my earlier agent/AI topics with Claude, it immediately switched me from Fable back to Opus 4.8. Anthropic's official line is that "more than 95% of conversations will not trigger a downgrade." In other words, up to roughly 5%, or one in twenty, may. That is absurdly high.

![Claude Fable conversation](fable-session.webp)

![Fable dynamically downgraded to Opus 4.8](opus-fallback.webp)

![SemiAnalysis on Fable's model-filtering system](model-filter.webp)

**Gripe two: a 12-day trial.** Fable is not currently part of the Claude Code subscription plans. For the 12 days from today until June 22, subscribers on the $100 and $200 plans get a limited trial. After that, the only option is metered API access. The official explanation is insufficient capacity: there is not enough compute to go around. Fable may become part of the standard subscription once capacity improves, but there is no timeline.

![Fable's limited trial in Claude Code](trial-window.webp)

**Gripe three: mandatory data retention.** If you use Fable, all traffic is retained for 30 days and is subject to review, whether or not you are an enterprise customer. That is a significant departure from the previous policy. It is the same old bargain: **data in exchange for compute.** For enterprise users who care about privacy and compliance, this change is impossible to ignore.

---

## So, Let's Do the Math

What does the API cost? In ["AI Survival Guide: Where the Biggest Arbitrage Really Is"](/en/ai/ai-bonus/), I ran the numbers: if you fully exhaust a $200 subscription, you can consume roughly $10,000 worth of tokens at API list prices. Metered access is therefore about 50 times the effective price of a fully utilized subscription. Put differently, you pay dozens of times more for the same usage through the API.

![Claude Fable API price comparison](api-price.webp)

For everyday use, then, running Fable through the API over the long term is a sucker's bet. That is exactly why this 12-day subscription window is so valuable: it is the only way ordinary users can reach top-tier intelligence at subscription prices.

My plan for the next few days is to revisit every question and feature on which the previous models had already converged, then review and improve them again with Fable. I have three steps:

1. **Take it one day at a time and use the subsidy while it lasts;**
2. **Revisit worthwhile discussions and push them deeper with Fable;**
3. **Put every past patch and feature through another review.**

That is also what I suggest you do right now: make the most of this 12-day window, because unused access simply expires. One way or another, you should personally probe the limits of the current SOTA—or "AGI"—model. Reading a hundred reviews cannot replace that firsthand feel.

---

## A Few Other Interesting Cases and Updates

![Collection of Claude Fable examples](fable-cases.webp)

![Fable and Opus compared on a space simulation](space-simulation.webp)

![Fable's New York skyline and storm-battered city examples](city-simulation.webp)

![Mythos hands-on report](mythos-review.webp)

---

## Closing Thoughts

Overall, my judgment is that **Fable is overkill for routine use—even professional work.** Models at the GPT-5.5, Opus, or Sonnet level are already more than capable enough.

But Fable can deliver enormous value at the frontier: finding security vulnerabilities, diagnosing and isolating exceptionally difficult problems, and pursuing open-ended research. These are tasks where **more intelligence is always better and there is no upper bound.**

**The intelligence premium pays off only at the frontier of intelligence.** That may be the rule of the Mythos era: myths belong to the lords and high priests; fables are told to the commoners. For now, all you can do is get through the gate before it closes—and see for yourself.
