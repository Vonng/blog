---
title: "I Finished Translating the Second Edition of DDIA: An Eight-Year Parable About AI"
date: 2026-02-15
authors: [vonng]
summary: >
  Codex translated DDIA's second edition in a single morning. Eight years ago,
  I spent three months translating the first edition by hand. The contrast
  reveals just how far AI has come.
tags: [Distributed Systems, Database, Translation]
---

This morning, I ran ten Codex sessions in parallel and, in less than half a day,
translated the final four newly released chapters of DDIA's second edition.

The results surprised me. Formatting, terminology, footnotes, and anchors were
nearly perfect on the first pass. The Chinese prose was fluent enough to shed
the machine-translated feel of earlier years. I will still do a complete review
and polish over the Lunar New Year holiday, but AI has effectively closed the
gap between a first draft and a readable manuscript.

Meanwhile, I had Pigsty's control plane running through its development loop in
several other terminal windows, while documentation edits moved ahead in
parallel. I had just [wrapped up the remaining work on MinIO's
console](/en/db/minio-resurrect/). Translating DDIA was only one side quest that
morning.

When I translated the first edition in 2017, I worked through it alone, sentence
by sentence. It took nearly three months of spare time. Eight years later, the
same job went from "three months" to "one morning." That is quite a change.

But here is the point I care about more: now that AI is taking off, DDIA is even
more worth reading than it was eight years ago.

Preview: https://ddia.vonng.com

---

## First, Some Context: Why DDIA Is Worth the Trouble

Some readers may never have heard of DDIA, or may know it only as "that famous
book." So let me briefly explain why it matters.

DDIA stands for *Designing Data-Intensive Applications*, published by Martin
Kleppmann in 2017. Its cover features a wild boar, hence its Chinese nickname,
"the boar book." Kleppmann has an unusual background: he first worked on
large-scale data infrastructure at LinkedIn, then returned to the University of
Cambridge to research distributed systems. The book therefore occupies a rare
intersection: it brings research-paper rigor to the real problems
engineers face every day.

It has achieved a rare degree of consensus across the global software industry.
On Hacker News, Blind, Reddit, and other engineering communities, it is
repeatedly recommended as a book every software engineer should read. Within
engineering teams at Google, Meta, and Amazon, it effectively serves as an
unofficial textbook. Nobody assigns it, yet its influence appears everywhere:
system-design interviews, new-hire onboarding, and architecture reviews. It
held the No. 1 spot in Amazon's database category for eight straight years.

To place it among the classics of computer science: Brooks's *The Mythical
Man-Month* defined a framework for thinking about software-project management,
and the Gang of Four's *Design Patterns* established a common language for
object-oriented design. DDIA did the same for data systems. It did not invent a
new theory. It gave a fast-moving, increasingly complex field a shared mental
model and analytical vocabulary.

Its longevity rests on one crucial writing decision: Kleppmann focused on
principles and trade-offs rather than particular tools. The trade-offs between
LSM-trees and B-trees, the fundamental tensions in replication and partitioning,
and the hierarchy of consistency models do not become obsolete when one product
rises and another falls. Tools die; principles endure.

DDIA is not an entry-level book, of course. Some chapters are so dense that they
feel like an entire course compressed into one chapter. Nor will it teach you
how to configure a particular system from scratch. Its purpose has always been
clear: it gives you judgment, not a runbook.

---

## A Repository That Captures the Evolution of AI

The Chinese translation of DDIA lives in a GitHub repository with 22.6K stars,
active since 2017. But the star count is not what interests me today. The
repository contains translations from four distinct moments in time, each one
capturing the state of AI translation at that point.

The book, the translator, and the quality bar remained the same. The only
variable was AI. You do not even have to take my word for it; just inspect the
historical diffs.

**2017: the first edition, carefully translated by hand.**
This came from an era when humans still did the real work. The workflow had
three stages: "machine translation → rough edit → final polish." Google
Translate laid the groundwork, DeepL improved it, and I manually refined every
sentence. How to translate a term, where to break a long sentence, how to land a
paragraph: every decision was mine. Three months of spare time. Slow, but solid.
That edition remains the stylistic baseline for the entire repository.

**September 2024: Part One of the second edition, translated with ChatGPT.**
O'Reilly released the second edition in Early Access, with the first four
chapters available. I decided to let AI try. I gave ChatGPT the first-edition
translation as a reference and asked it to preserve the same style and
terminology. The result was sobering. It was clearly capable of "translation,"
but the prose was stiff and terminology drifted. One commenter simply called it
"awkward." Looking back at it now makes me wince. At that stage, AI was still
mostly replacing English words with Chinese ones. It had not yet reached the
level of Chinese technical writing.

**August 2025: Part Two of the second edition, translated with Claude Sonnet.**
When the middle four chapters arrived, I switched to Claude Code with Sonnet
3.7. It was a clear improvement over ChatGPT: smoother sentences and fewer
errors. Yet readers still described it as "somehow off." This was not a grammar
problem. It was about the rhythm of technical writing, consistent terminology,
and the ability to land concepts precisely. Readable, but uncomfortable.

**February 2026: Part Three of the second edition, translated with Codex.**
That brings us to today. When the final four chapters arrived, I ran ten Codex
sessions in parallel and finished them all in one morning. This time was
different. Codex extracted clean Markdown from the raw HTML. It understood the
2017 translation and carried over its style and voice. It strictly followed the
more than 3,000 index terms I had prepared in advance, keeping terminology
highly consistent across the book. The result came out close to the quality of
a careful human translation.

Four versions spanning eight years, all preserved in the same Git repository.
For anyone studying the evolution of AI translation, this is a remarkably clean
comparison: the book and translator are held constant, AI is the independent
variable, and translation quality is the dependent variable.

Of course, "finished in one morning" does not mean I merely pressed Enter. I
invested real effort in the glossary. I designed the engineering workflow and
prompts. The final review and polish still have to happen. No matter how strong
AI becomes, it still needs someone who knows what a good translation looks like
to act as the final judge. But the central fact remains: the shift from three
months to one morning—two orders of magnitude—is etched into that repository's
Git history.

---

## The Stronger AI Gets, the More DDIA Is Worth Reading

If AI can translate all of DDIA in a morning, do people still need to read it?

My answer is yes—and more than ever.

The reason is simple. I could bring AI's output close to a deliverable standard
not because I am better at pressing buttons, but because the hard work I did in
2017 gave me a baseline. I know how the terms should be translated. I know which
sentences look correct but still feel wrong. And I understand the trade-offs the
book is actually trying to convey.

Without the version of me who did that grueling work in 2017, the version of me
running ten parallel sessions in 2026 could not exist.

This is a basic truth of the AI era:
**you do not need to translate better than AI, write code better than AI, or
design architectures better than AI. But you do need to judge whether what AI
gives you is correct, good, and sufficient.**
AI can make output faster, but it cannot automatically make that output right.
Only when you can judge correctness do you get to benefit from speed.

That judgment does not fall from the sky. It comes from understanding the
underlying principles. DDIA provides exactly that understanding.

AI has made me much more productive as a programmer. Much of the code in Pigsty
4.0 was generated by AI. But the more I use it, the more often I encounter a
kind of dangerous fluency: AI produces a professional-looking architecture
proposal in polished language, with every term apparently used correctly.
Without your own framework for judgment, it is easy to be carried along by that
fluency.

Consider two common examples.

**The temptation of distributed systems.**
AI will readily propose a multi-node, sharded, eventually consistent design—and
sound very confident about it. But DDIA keeps reminding you that distribution
is not a higher stage of evolution. It is a cost. The first question should be:
do you really need it? If your data volume does not demand it, one PostgreSQL
primary and a few read replicas may be the optimal design. The complexity of
distributed systems carries a real cost, and many people underestimate it.

**A complete set of concepts does not guarantee a correct decision.**
AI can explain transaction isolation levels, replication consistency, and
RTO/RPO with impressive fluency. But in your particular system, what should you
trade away, and for what? Which consistency guarantees can be relaxed, and which
must be preserved? Which failures require recovery within seconds, and which
can tolerate minutes? This is not about reciting definitions. It is about
making the call. Making the call requires a framework, not a glossary.

**DDIA is not a manual for operating databases; AI will replace manuals.
It is a book about how to think about data systems, and frameworks for thinking
will not be replaced.**

---

## What Is New in the Second Edition: Trade-Offs Take Center Stage

The second edition is not a simple revision. It is more like a structural
upgrade: trade-offs move from an implicit theme running through the book to its
explicit starting point.

Rather than recap every chapter, I will highlight the most important changes.

**A new opening chapter puts architecture decisions first.**
The second edition adds an entirely new first chapter, effectively a road map:
cloud services vs. self-hosting, distributed vs. single-node, OLTP vs. OLAP,
systems of record vs. derived data. Before you enter any technical detail, you
receive a complete framework for making decisions. The first chapter of the
first edition was called "Reliable, Scalable, and Maintainable Applications."
In the second edition, it is "Trade-Offs in Data Systems Architecture." The
title change alone says a great deal.

**Vector search joins the main story.**
In the storage and retrieval chapter, vector embedding search appears alongside
B-trees and LSM-trees. This is not chasing a fad. It reflects a judgment:
Kleppmann considers vector search part of the standard repertoire of data
systems. The AI era has made it into the textbook's core.

**Cloud-native architecture is fully integrated.**
Cloud data warehouses, disaggregated storage and compute, and cloud-era
operations: the second edition systematically incorporates the industry's most
fundamental architectural shift between 2017 and 2025, from self-managed
clusters to managed cloud services. Meanwhile, technologies such as Hadoop
MapReduce, which have receded from center stage, receive far less space.

**Distributed transactions return to the transactions chapter.**
The old transactions chapter was essentially a tutorial on isolation levels,
while distributed transactions appeared later in the book. The new edition
combines them: 2PC, 3PC, XA transactions, and exactly-once message processing
all move into the transactions chapter. It evolves from an introduction to
concurrency control into an engineering guide to end-to-end atomicity. The
transaction boundary in a modern system has long since extended beyond one
machine. The book's structure has caught up with reality.

**From knowing the risks to managing them.**
The distributed-systems chapters in the first edition mostly said, "These
failures will happen." The second edition adds formal verification, model
checking, fault injection, and deterministic simulation testing. It not only
tells you that the risks exist; it offers systematic ways to test whether they
can take down your system.

**Ethics gets its own chapter.**
Bias and discrimination in predictive analytics, privacy and tracking, data as
a source of power, and the GDPR: a data system is responsible not only for
technical correctness, but for its social consequences. This is not political
correctness. It is engineering reality. Data systems are now unavoidably
surrounded by legal and social constraints, and architecture decisions are no
longer driven by technical metrics alone.

In one sentence: the first edition was about establishing a common language;
the second is about giving you a decision map. It is more engineering-oriented,
more practical, and more modern. Yet the core principles—B-trees vs. LSM-trees,
replication and partitioning, consistency models—remain solid. That fact itself
validates the first edition's strategy: focus on principles, not tools.

---

## How to Read It: Advice for Different Readers

- **Newcomers:** Start with the overview and foundational chapters. Your goal is
  to build a mental map, not to finish the book as quickly as
  possible. Once you have the framework, returning to the relevant chapter when
  a concrete problem arises is actually more efficient.
- **Experienced engineers:** Treat it as a tool for reviewing what you know.
  Read by topic, paying particular attention to trade-offs and boundaries. The
  references and summaries at the end of each chapter are the best material for
  going deeper. Do not skip them.
- **Developers in the AI era:** Treat it as the standard against which you
  review AI's work. When AI writes 99 percent of your code, you still need to
  judge the critical decisions in the other one percent. DDIA gives you that
  judgment.

---

## On Translation Quality

I know some people instinctively recoil from "AI translation." That is
understandable. Over the past few years, plenty of technical translations have
been passable yet painful to read, exhausting readers' patience.

So let me be clear about my approach: AI is the execution layer here, not the
final arbiter.

I did three things:

1. **Turned terminology into a dictionary:** I fixed the translations of more
   than 3,000 index terms and supplied them as a source of truth. This
   prevents the same concept from receiving different translations in different
   places.
2. **Established a stylistic baseline:** Readers had already accepted the voice
   of the 2017 first-edition translation. I used it as the style reference and
   let the model carry that voice forward.
3. **Produced publication-ready formatting:** I turned HTML-to-Markdown
   conversion into a stable pipeline, handling footnotes, anchors, and
   quotations cleanly in one pass.

One caveat: the current version has not yet received its final human proofread.
It is a preview. When the Early Access period ends and the book is formally
released, I will conduct a complete human review. If you find a problem while
reading, please open an issue. Translation suffers from sloppiness, not
scrutiny.

---

## DDIA and My Eight Years

Let me end on a more personal note.

When I translated the first edition in 2017, the tech scene around me was in a
classic period of tool explosion. Distributed databases, enterprise "data
middle platforms"—a Chinese architecture pattern for shared data
capabilities—and big-data stacks were appearing everywhere, and much of the
conversation followed the marketing. At the time, not going distributed made
you look obsolete.

We tried plenty of options too: multi-node clusters, sharded architectures, and
different database systems. We experimented with Citus, Cassandra, and TiDB, and
even built our own distributed database, ttdb. Eventually, we decommissioned
everything we could and settled on primary-replica PostgreSQL. That proved to be
the right choice. Today, even a unicorn as large as OpenAI [runs its core
business on an ordinary PostgreSQL cluster with one primary and fifty
replicas](/en/db/openai-pg/).

The reason is no mystery. DDIA's most important influence on me was not any
particular technical detail, but a simple way of making decisions: lay out the
requirements, constraints, and costs before discussing solutions. If a simple
system can solve the problem, do not burden yourself with a complex one. The
complexity of a distributed system is never merely in the code. It also lies in
failures, operations, debugging, and organizational capacity. What many teams
lack is not another distributed component, but the engineering ability to
control complexity.

That mindset has guided many of my decisions in building Pigsty: do not chase
fads, do not bet on buzzwords, and try to make systems understandable,
maintainable, and operable. Looking back, DDIA gave me a lens for seeing through
the noise to the essential benefits, costs, and trade-offs behind an
architecture.

---

## Conclusion

I translated this book eight years ago. Eight years later, it remains the book
that has influenced my career more than any other.

The tools have changed enormously: translating the book went from three months
to half a day. But I am increasingly certain of one thing: the more powerful our
tools become, the more important foundational knowledge and mental frameworks
become.

Newcomers should read it to build a mental map and avoid three years of
wrong turns. Veterans should read it to weave scattered experience into a
coherent whole. In the AI era, read it to gain the ability to judge whether AI
is right.

Read the second edition online: https://ddia.vonng.com
