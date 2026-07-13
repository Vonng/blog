---
title: "The Karma of Open Source: When Code Is Worthless, Where Does Trust Come From?"
date: 2026-06-11
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  AI is driving the cost of producing code toward zero. It cannot compress time, track records, or accountability. The real value of open source is not yesterday's code, but a system trusted to deliver on tomorrow's promises.
tags: [AI, Open Source, Trust, Agent, Trademark]
ai: true
---

> Credit does not require a soul. It requires an account.

## Introduction: The Overnight Rewrite

Not long ago, someone used AI to rewrite an open-source Python library in Rust overnight. The new project had no fork history, no evidence of copied code, and no license violation. The original author's only recourse was a DMCA request to GitHub. The only result was a new name for the rewrite.

The rewriter broke no law. They had merely compressed three months of work into one night.

That small incident cuts through a forty-year-old assumption at the foundation of open source. If any codebase can be clean-room reimplemented overnight, what does copyright still protect? Whom do licenses constrain? What remains valuable?

The deeper question is: **where does software's value actually live?**

The answer runs through code, process, trademarks, and accountability, before arriving at an unlikely destination: karma.

## 1. Code Is Cheap. Track Records Aren't.

"Code" has at least three roles: it is a means of production, an executable specification, and a coordination point.

AI destroys the scarcity of the first. When the marginal cost of generating a system that appears to work approaches zero, code loses much of its value as an asset, as IP, or as a secret. But the other two roles become more valuable. In a market flooded with plausible implementations, the one tested in thousands of production environments, where each odd-looking line reflects a real postmortem, commands a premium. Bad code makes proven code more valuable.

The key distinction is simple: **AI compresses labor, not calendar time.** The cost of writing code is collapsing. The rate at which trust accumulates is not. Trust is the integral of deployment, time, and exposure to risk. Anyone may soon generate something shaped like PostgreSQL in three weeks. Nobody can generate its thirty-year operational history. An overnight rewrite may be legally clean, but it begins with a validation balance of zero.

SQLite turned this insight into a business model long ago. Its source is in the public domain, more permissive than any open-source license. Its TH3 test suite, however, is proprietary. Consortium members pay for its 100% MC/DC coverage, validation, and warranty. **The code is free; the proof costs money.** SQLite has looked like an AI-era software company for two decades.

So "code no longer matters" is too broad. **The text of the code is cheap; its track record is not.** Copyright may be losing force, but an artifact proven across ten thousand clusters remains valuable. This is also why binaries and distribution channels matter more than ever. A binary crystallizes a track record. Its checksum anchors not only bytes, but history.

## 2. Three Verdicts on Licenses

Licenses are not dead. They deserve three separate verdicts: **as a sword, dead; as a flag, alive; as a bomb, unexploded.**

As a sword against copying, the license is largely dead. Copyright protects expression, not function. Clean-room reimplementation was always legal. In the past, however, reimplementation cost roughly as much as the original development, so copyright protected functionality in practice. AI has pushed that cost toward zero. The law did not change; its economic foundation did. In the opening example, the only enforceable remedy was a new name.

As a flag to the ecosystem, the license remains useful and may matter more. Google's long-standing internal restrictions on AGPL software are sometimes cited as evidence that licensing has failed. I read them as evidence that the AGPL works. For commercial open-source companies, it is less a litigation tool than a deterrent: it tells large companies to buy a commercial license or stay away. Nuclear weapons do not need to be detonated in court to have an effect. Choosing Apache or AGPL now says less about who may copy the project than about what the maintainers intend. AGPL says, "I plan to monetize this." Apache says, "I plan to be everywhere."

As a bomb, licensing has yet to go off. Model training may be the largest licensing event in history: the entire open-source commons has been absorbed into model weights, while courts have yet to settle whether those weights are derivative works. A clear ruling could revive copyright at the scale of training corpora. The fiercest license conflict has already moved up the stack, from source code to open-weight models.

## 3. From Product to Process: A Fork Is a Photograph of a River

Put those observations together and a larger shift appears. **Software's value is moving from artifact to process. Value capture is moving from writing code to running it, and from creating software to distributing and maintaining it.** Code is becoming a consumable flowing through a system. The durable asset is the system that keeps producing good software: its mechanisms, organization, community, and feedback loops. Software is becoming a process business. **The recipe is free; the cold chain is not.**

The graveyard of forks offers strong evidence. Open-source code can be copied perfectly, yet most forks die. If the value lived in the code, that should not happen. Source code is a projection of a system at one point in time. Forking it is like photographing a river: the image is complete, but the water has moved on.

The forks that survived did not merely take the code; they moved the system. MariaDB brought the founder and core developers. Jenkins brought the community, leaving Oracle with the Hudson trademark and code but an empty social shell. Valkey brought Redis maintainers. Manufacturing has shown the same pattern. Toyota opened its plants to competitors, and General Motors even operated a joint factory with it, yet Toyota's production system remained hard to copy. Institutional knowledge lives in process and relationships, not blueprints. Code is software's blueprint, and AI gives everyone an unlimited supply of blueprints.

Valuation points to the same conclusion. A company is the discounted value of future cash flow. A project is the discounted expectation of future releases: someone will fix the next vulnerability, port the next platform, and study the next incident. **A fork takes 100% of the artifact and 0% of the expected flow.**

## 4. Red Hat: A Thirty-Year Natural Experiment

Red Hat has spent thirty years running a natural experiment, complete with a control group, on the proposition that value does not live in code.

RHEL is GPL software. Anyone may legally clone it. CentOS shipped near-bit-for-bit clones at no charge for years; Oracle Linux still resells the same work. Yet RHEL became a multibillion-dollar annual business, and IBM paid $34 billion for Red Hat. **The same bits were worth zero on one side and supported a $34 billion acquisition on the other. The spread is the market price of everything except the code.**

What is in that spread? A certification matrix maintained with hardware and software vendors; SAP certifying a specific RHEL stream rather than "Linux" in the abstract; a ten-year lifecycle and ABI promises; backported security fixes; continuous CVE response and errata; compliance paperwork; legal indemnification, sold explicitly during the SCO era; and maintainers employed across critical upstream projects. In effect, Red Hat concentrated a deep reservoir of judgment.

An artifact is written in the past tense. Only a living system can write checks against the future. Red Hat does not really sell software. It sells a promise that these bits will be patched, certified, supported, and defended for the next decade. A subscription is a futures contract on maintenance. The business of open source can be reduced to one line: **give away the past; sell the future.** Past labor has already happened. Customers pay for promises about work that has not.

Red Hat acts as a **trust transformer**. Upstream communities produce chaotic alternating current; enterprises want stable direct current for ten years. Red Hat sits between them and rectifies it. The margin comes from the voltage difference, not the electricity.

That is why distribution matters. A distribution channel is the physical form of a supply chain and a chain of trust. But there is a trap: trust in binaries must derive from verifiable source through reproducible builds, signatures, and provenance. It cannot replace source-level verification. A distributor that says "trust our artifacts, but do not inspect our source" is structurally a proprietary vendor. What keeps a distributor honest is not virtue, but the customer's credible right to exit.

## 5. Trading Margin for Learning Rate

What drives this system? A loop. Use produces testing. Testing exposes failures. Failures flow upstream and improve quality. Better quality attracts more use.

This suggests an economic definition of open source: **open source trades gross margin for learning rate.** Free access maximizes installations; public issue trackers maximize captured feedback.

> Learning rate = installed base x feedback capture rate

AI may equalize production rates. It cannot equalize field learning, which still requires real deployments and real time.

The second factor is the bottleneck. Most users never report failures. Agents may make this worse: a coding agent can silently patch a local bug without ever opening an issue. The risk to the commons is no longer just free riding. It is becoming a quarry: mined into model weights while receiving no feedback in return. The garden becomes a pit.

That leads to a practical conclusion: **in the agent era, the most valuable community contribution is not a patch but a reproducible failure.** Fixes are becoming cheap. Reproduction is scarce. The successor to the pull request may be the failing test. Community tooling should shift from "make code contributions easy" toward "make it trivial to submit a crash scene."

There is another thing AI cannot consume: environment. **AI compresses text space, not world space.** The combinatorial explosion of distributions, kernels, hardware, and configuration lives in server rooms, not training corpora. In James C. Scott's terms, *episteme*, knowledge that can be written down, is absorbed into model weights; *metis*, practical knowledge, still requires contact with reality. Crowdsourced testing outsources that contact surface to the community. Vibe coding cannot replace it.

The optimal open-source strategy in the AI era may therefore be the opposite of instinct. Do not try to prevent copying. Put the code everywhere in the corpus. When a user asks an agent to deploy a database, the project it reaches for occupies the new shelf space. Representation in model weights is the new SEO. Then charge for what the weights cannot contain: fresh releases, real operations, and accountability when things break.

## 6. Trademarks: The Legal Container for Trust

If copyright on code is becoming hard to enforce, what can the law still protect? Increasingly, the IP stack is collapsing toward trademarks.

Copyright protects expression, which AI is turning into tap water. Patents protect function, but clean-room implementation remains legal, patents expire, and major open-source licenses include patent-retaliation clauses. Software patents have mostly served as defensive weapons. Trademarks protect something else: **origin**. They bind a name to an accountable entity. Copyright and patents protect things. Trademarks protect a relationship, and trust is a relationship.

Trademarks also have a unique property. They grow stronger through use and can last indefinitely. Copyright arrives at creation as a stock of rights. A trademark accumulates through continued commercial use and survives only if defended. It is a flow, a living metabolism. The shift in IP from stock to flow mirrors software's shift from product to process.

The fights are already here. Debian renamed Firefox to Iceweasel over trademark policy. RHEL clone pipelines include explicit debranding steps. Terraform's fork became OpenTofu; MySQL's became MariaDB. The WordPress-WP Engine dispute centered on trademarks, not code. The overnight rewrite from the introduction ended with a name change. Even "Linux" is Linus Torvalds's registered trademark.

But the container is not the content. Oracle still owns the Hudson trademark, yet the community voted to become Jenkins and left Oracle holding a hollow name. A trademark is the legal projection of legitimacy, not legitimacy itself. **It prevents impersonation: others cannot cheaply wear your face. It does not prevent disgrace: if you lose the community, the name will not save you.**

## 7. The Third Scarcity: Something to Lose

What does that protected relationship contain?

The AI era is producing an inversion of scarcity. Code production used to be scarce. Now that it is becoming abundant, other things matter more. Two popular answers are taste, the ability to ask the right question, and judgment, the ability to verify the answer. Both are correct, with limits.

The defensibility of taste depends on feedback delay, cost of failure, and rarity of the event. Where feedback is fast and cheap, machines will catch up quickly. Domains defined by events that happen once in years and kill you once—storage, security, financial infrastructure—are harder. You cannot run reinforcement learning on a 3 a.m. outage when samples are rare, failures are expensive, and most postmortems are private.

Beyond taste and judgment lies a third, deeper scarcity: **having something to lose.**

Trust requires a counterparty that can be punished. Accountability needs four things: a persistent and identifiable actor, a venue for judgment, something that can be forfeited, and confidence that the actor will still exist tomorrow. AI has none of them by default. It has no continuous identity, no balance sheet, no name that can be disgraced, and no guarantee that the next model version will preserve the current one. **AI can be verified, but it cannot yet be trusted.** No individuality, no karma; no karma, no credit.

Much of civilization is the history of prosthetics for accountability. Seals bind acts to identities. Double-entry bookkeeping turns business into an auditable confession. Professional licenses make an engineer's signature a wager of a career. An auditor's signature lets strangers invest.

These systems even have a death penalty. After Enron, an 89-year-old accounting firm disappeared within months. The US Supreme Court later overturned Arthur Andersen's conviction. It no longer mattered. **The real court was the ledger of reputation; the legal ruling was a late footnote.**

Humanity has already created one partly accountable artificial person: the corporation. Limited liability is deliberately capped karma. To encourage risk-taking, society limits what this artificial person can lose. It then spent four centuries surrounding the corporation with mandatory disclosure, audits, ratings, insurance, and, after Enron, CEO signatures that put personal responsibility back into the system.

**AI is the limit case: an artificial person with zero karma.** The answer will not be to ban it from critical systems forever. We will build the same institutional machinery around agents: identity, audit, bonding, insurance, and certification.

Intelligence will not set the pace. Elevators did not spread the day they became safe; they spread when insurers could price them. Autonomous driving will scale as fast as someone is willing to absorb its liability. **AI will enter critical infrastructure at the speed of underwriting, not intelligence.**

Frank Knight drew the distinction a century ago: risk can be priced; uncertainty cannot. A signature from someone with something to lose converts uncertainty into risk. Once converted, insurance, contracts, and markets can attach. Audits, certification, and the old rule that "nobody gets fired for buying IBM" are versions of the same converter. Enterprise buyers often do not buy code. They buy a neck to wring at 3 a.m.

Do not dismiss the ritual. Verification performed by someone who can be punished is what lets strangers transact.

## 8. A Genealogy of Credit: Collateral as a Prosthetic for Amnesia

Where does credit come from: collateral, or past performance?

There are two archetypes. The pawnshop trusts the object rather than the person and demands overcollateralization; DeFi reproduced this model on-chain. The other model is biographical: unsecured credit based on history and repeated interaction.

A well-known paper in monetary economics is titled *Money Is Memory*. Money and collateral can act as technical substitutes for a society-wide ledger. **Where society can remember, biographical and unsecured credit flourishes. Where it cannot, lenders demand collateral.** Anthropological evidence points in the same direction. Credit predates coins. Villages ran on remembered obligations; coins were useful for strangers and soldiers. **Collateral is a prosthetic for social amnesia.**

Avner Greif's eleventh-century Maghribi traders enforced contracts across the Mediterranean with no reliable courts. Letters maintained a multilateral reputation network: betray one member and the whole coalition would exclude you. Open-source communities have followed the same model for forty years. Mailing lists are the letters; commit access and conference handshakes are key-signing ceremonies for a trust network.

AI is breaking the identity assumption beneath that system. Contribution histories can be generated; people can be faked. The pressure has two outlets: stronger identity technology or heavier institutions.

Sovereign credit provides evidence at the largest scale. States cannot pledge their territory. US Treasuries have no collateral behind them, only fiscal history and market sanctions, yet they define the world's risk-free rate. **At the largest scale, credit is biographical, not collateralized.**

Look deeper and the two models collapse into one formula. A track record matters only if something is at stake. Collateral matters only if identity persists.

> **Credit = identity continuity x memory infrastructure x forfeitable value x time**

Klein and Leffler formalized the forfeitable-value term in 1981: **a brand premium is a bond paid continuously.** Consumers pay extra for a brand precisely to give the seller something to lose. Cheat once, and the capitalized stream of future premiums disappears. The premium is a hostage.

This produces a counterintuitive result: **pricing power is trust infrastructure. A zero-margin vendor's promises are financially unsecured.** The price difference between RHEL and a free clone is the public market quote for that bond.

The model also predicts what happens to defectors. Some projects begin under permissive licenses, use the community to build adoption and feedback, then change the license and move essential features out of the community edition. The community calls it a rug pull. The model calls it cashing out a trust bond. It may work once. The cost is the permanent loss of the premium stream. The forks that follow are the community enforcing forfeiture.

This points to the final form of an AI-era infrastructure company: **a media company for customer acquisition, an insurer for revenue, and a lab for staying current.**

## 9. Karma: Credit You Cannot Default On

The ancient term should now be clear.

**Karma is a credit system you cannot default on: perfect memory, no bankruptcy, automatic enforcement.** Consequences need no court or bailiff. Karma is the limiting case of the formula above: perfect memory, unlimited forfeitable value, and unbounded time.

Buddhist thought solved the accountability problem under the doctrine of *anattā*, or no permanent self. It denies an eternal soul but preserves continuity: a causal stream in which each moment follows the previous one. In Yogācāra Buddhism, *ālaya-vijñāna*, the storehouse consciousness, is the ledger that carries karmic seeds across that stream.

More than two thousand years ago, Buddhist thinkers arrived at a useful design principle: **accountability does not require an essence. It requires an account.**

That turns AI trust from a metaphysical problem back into an engineering problem. "AI has no soul, therefore it cannot be trusted" is a bad argument. Credit has never required a soul. Banks do not ask depositors to present one.

## 10. Markets Will Force AI Agents to Become Individuals

The blueprint for AI credit is the same four-part system:

- A persistent, named identity.
- An append-only, cryptographically verifiable record of actions—the engineering equivalent of the karmic ledger is an audit log.
- Something at stake: a bond or insurance reserve posted by the operator, or a costly track record accumulated by the agent itself. A named agent with five clean years in production is an asset. Destroying that identity has a real cost, so the agent acquires something to lose in the only sense economics requires. No consciousness is necessary.
- Actual service time in production.

This leads to a less obvious prediction: **markets will force AI agents to become individuals.**

Interchangeable, stateless, disposable agents are uninsurable. You cannot price an entity with no past and no future. Accountability requires non-fungibility; credit requires continuity. The agent economy will therefore select for persistent agents with individual histories.

**Individuality is not a philosophical luxury. It is a requirement of a credit economy.** Today we ask why AI lacks genuine individuality. Economics offers an eschatological answer: it will not lack it forever, because credit markets need a carrier for karma.

## Conclusion: The Ticket Will Be Reprinted

Return to the original question: where does software's value live?

Not in the code: text is cheap; track records are valuable. Not in the license: the sword is rusting, the flag still flies, and the bomb has not gone off. Value lives in the system—the loop that keeps producing, validating, and delivering on promises. Its legal shell is the trademark. Its economic substance is a bond paid continuously. Its final form is a ledger nobody can rewrite.

Open source spent forty years proving a business model: give away the past and sell the future. AI pushes that truth to its limit. When the cost of producing the past falls to zero, promises about the future become the only product.

Machines cannot yet make such promises—not because they are not intelligent enough, but because they do not have accounts.

A question has been circulating in the community: does open source still offer a ticket into the AI economy? Some say the word on the ticket has changed from "contributor" to "builder." Follow the argument one step further and the next ticket may say "account holder": an entity capable of carrying karma, whether carbon or silicon.

AI compresses everything that can be compressed: labor, corpora, blueprints, expression. One thing remains incompressible: calendar time.

**Trust accrues by the calendar. Karma settles by the account.**
