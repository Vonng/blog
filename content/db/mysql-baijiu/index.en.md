---
title: "MySQL and Baijiu: The Internet’s Obedience Test"
linkTitle: "MySQL and Baijiu: The Internet’s Obedience Test"
date: 2025-12-20
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat](https://mp.weixin.qq.com/s/SBZRQCCZ7PmsbDSgcRaqBQ)
summary: >
  MySQL is to the internet what baijiu is to China: harsh, hard to swallow, yet worshipped because culture demands obedience. Both are loyalty tests—will you endure discomfort to fit in?
series: [MySQL走好]
tags: [MySQL,数据库]
---

## 1. Two Painful Shots

Remember your first sip of baijiu? It scorched down your throat like a wire of fire. Your face contorted, eyes watered, stomach flipped. Every instinct screamed: **this isn’t food, it’s poison.**

The senior at the table grinned: “You’ll get used to it.”

MySQL feels the same. The first time you study it seriously, you hit absurd design choices:

- Default charset `latin1`, and when you finally switch to “utf8” you learn it’s fake—real UTF‑8 is `utf8mb4`.
- `TIMESTAMP` dies in 2038; the Y2K ghost never left.
- [ACID compliance is shaky; transactional correctness is a coin toss](/en/db/bad-mysql).
- `GROUP BY` lets you select non-aggregated columns—SQL standard? Never heard of her.
- No real boolean type; `BOOLEAN` is `TINYINT(1)`.
- DDL isn’t transactional; `ALTER TABLE` is a guillotine.
- Replica lag is eternal; the optimizer inspires existential dread.

Your brain whispers: **this isn’t design, this is an accident.**

Learn databases from scratch and PostgreSQL feels “how it should be.” MySQL makes you keep asking “why?”

Yet the veterans shrug: “You’ll get used to it.” No explanation. Just adaptation. Exactly like baijiu. “You’ll get used to it” is where every form of discipline begins.

--------

## 2. How Discipline Forms

Nobody is born liking baijiu. Ancient Chinese drank rice wine; “煮酒论英雄” wasn’t about Erguotou. Baijiu’s dominance is recent—a top-down spread: a specific organizational culture → bureaucracy → society. A powerful system declares something “the rule,” and the rule seeps everywhere via people and incentives. It’s not because baijiu tastes good; it’s because “the people upstairs drink it.” Copying authority is human nature.

![featured.jpg](featured.jpg)

MySQL rode the same pipeline. In the 2000s, the authority in tech was Silicon Valley + early giants. They pushed LAMP—not because it’s best, but because it’s free, easy, and used by the winners. BAT declared MySQL the standard; talent churn carried that decision to every Chinese internet company. Startups and SMEs followed like private firms mimicking bureaucratic banquets.

Generations of engineers grew up with “MySQL is the internet default.” They never evaluated other databases; the belief was preloaded. Questioning it felt like saying “I don’t drink baijiu” at a banquet—people wonder what’s wrong with you.

**Discipline isn’t organic. Power builds it, then dresses it up as “tradition.”**

--------

## 3. Obedience Tests

What’s baijiu’s real job? An obedience test. When a boss raises a glass, he’s not measuring your alcohol tolerance; he’s asking: **how much discomfort will you endure for this relationship?**

You drink, your body rebels, your will overrides it. You signal: “I’ll hurt myself for this team.” It’s primal loyalty theater.

MySQL does the same. On paper teams evaluate performance/features. In reality it’s often political:

- Picking MySQL = **obeying industry norms**
- Picking MySQL = **not challenging the status quo**
- Picking MySQL = **sharing the same pain** instead of taking “nonstandard” risks

Suggest PostgreSQL and you need detailed reports, stakeholder negotiations, and you own every future hiccup. Suggest MySQL? Nothing. “Industry standard” is the entire argument.

**MySQL requires no justification; alternatives require a defense.** That’s discipline at work: obedience is default, thinking requires effort.

--------

## 4. I’ve Lived It

I joined a major domestic cloud years ago. Our internal poster listed “technology values”: “embrace open source, pursuit of excellence.” Reality? Everyone was told: “all new systems use MySQL. PostgreSQL is forbidden, Oracle is legacy only.” Reasons? “Oracle maintenance is expensive.” “PostgreSQL is unfamiliar.” Translation: “Don’t rock the boat.”

I sat behind a developer who spent weeks debugging MySQL master-slave data divergence. He patched business logic to mask inconsistencies, added compensating jobs, went to weekly postmortems… but never asked whether the database was the source of the pain. When I suggested Postgres as a pilot, he said, “Let’s not stir up trouble.”

I’ve watched countless engineers nitpick every Postgres feature—“MySQL can do that,” “your benchmark isn’t fair”—while ignoring MySQL’s fatal flaws. They’re not doing technical due diligence; they’re protecting their comfort zone. Admitting MySQL’s issues means admitting years of sunk cost. That cognitive dissonance hurts, so they fight the messenger.

I get it. Empathy doesn’t equal agreement.

--------

## 5. The Tide Turns

There’s good news: discipline is cracking.

**Baijiu:** young people increasingly say “no.” Not drinking is no longer social suicide. Old-school banquets insisting “drink or disrespect” are losing traction.

**MySQL:** the tide is shifting too.

- **Cloud-native era:** AWS, Google, Azure all push PostgreSQL. Money talks.
- **AI era:** pgvector made Postgres the vector DB of choice while MySQL stands still.
- **Compliance era:** Postgres is pure BSD; MySQL is GPL under Oracle. Guess what enterprise lawyers prefer.
- **Ecosystem:** scan GitHub—new projects default to Postgres. The energy is palpable.

[DB-Engines trends plus StackOverflow/JetBrains surveys](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247490182&idx=1&sn=cf0b4bc25902467ef61494c4b782a9c8&scene=21#wechat_redirect) all say the same thing: **Postgres is the fastest-growing database of the past decade.** It’s the new default for startups and AI projects—exactly where MySQL used to sit.

Teams are finally asking: **“Why must we use MySQL?”** That question is the beginning of the end for any discipline.

--------

## 6. Courage to Choose

MySQL isn’t unusable. It powers countless systems. In some scenarios it’s fine. But **“fit for purpose” ≠ “default.”** The first is a decision; the second is conditioning.

Next time someone says “let’s just use MySQL,” pause and ask **why**. Not to be contrarian, but because the choice deserves thought.

How much time have you spent mastering MySQL’s quirks—charset voodoo, DDL outages, replica lag, optimizer roulette? If you invested that energy into a better-designed system, how far could you go?

How many “best practices” are really duct tape covering MySQL’s flaws—rewriting subqueries as joins, using middle tables instead of CTEs, bolting on external tooling to patch missing features?

PostgreSQL isn’t perfect. Nothing is. But it proves a point: **databases can be designed to make *you* comfortable instead of forcing you to adapt to their neuroses.**

Choosing PostgreSQL isn’t religion. No tech decision should be. But in China it still takes courage—the courage to break inertia, think independently, and own your choice. That courage is the same as saying “I don’t drink baijiu” at a banquet:

**Refuse discipline. Make your own call.**
