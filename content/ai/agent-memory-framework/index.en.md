---
title: "The Three-Way Endgame: Why Agent Memory Frameworks Are a Dead End"
date: 2026-04-19
author: Ruohang Feng
summary: >
  A cold shower for the red-hot agent memory market—not because agents do not need memory, but because memory is the endgame moat. That moat belongs to models, harnesses, and databases, not today's "memory frameworks."
tags: [AI, Agent, Memory, PostgreSQL, Database]
---


A few months ago, I wrote [The OS Moment for AI Agents](/en/ai/agent-os/). I made a prediction there: the next frenzy in agent infrastructure would be memory. Startups and open-source projects would swarm around the question of how agents should remember things. Capital would pour in. The architecture diagrams would grow ever more elaborate.

Sure enough, Mem0 raised another round. MemGPT renamed itself Letta and kept raising. Then there are Zep, Cognee, Hindsight, MemoryScope, Memobase, SuperMemory, Graphiti, LangMem, EverMemOS—the list goes on. Their technical blogs all feature roughly the same architecture diagram: an episodic layer at the bottom, a semantic layer in the middle, and a reflection or procedural layer on top, with arrows labeled consolidation, retrieval, and forgetting running between them. GitHub stars are climbing, arXiv papers are racing up the charts, and every technical conference seems to have an Agent Memory track. The hype is real.

But let me throw some cold water on it: **this category may be hot today, but it may not exist in two years**.

That is intuition, not yet an argument. So let me be clear: I am not saying agents do not need memory. Quite the opposite. Memory is the biggest prize in the entire agent revolution. It is where the endgame moat lies. What I am saying is this: **agents need memory, but they do not need what we currently call "memory frameworks."**

Those statements sound almost identical. The small distinction between them is a matter of life or death for an entire category.

Here is why.

-------

## 1. The Endgame Is a Three-Way Split

To understand today's market, start by drawing the end state.

One qualification first: by "end state," I mean **serious enterprise agents, plus any organization or individual that treats data as a core asset**. The consumer market may look different. An ordinary user may simply use ChatGPT or Gemini and let the vendor bundle in memory.

My view of the agent endgame is simple: **the market splits three ways**. A mature agent will look roughly like this:

![divide.png](divide.png)

```bash
MODEL_URL=https://api.anthropic.com/v1
DB_URL=postgres://user:pass@host:5432/memory
```

One URL provides intelligence. Another provides memory. Between them sits a harness that wraps the model and drives it through concrete tasks: loading Skills, assembling context, calling tools, and managing loops. Want to switch model vendors? Change `MODEL_URL`. Want to move your data elsewhere? Change `DB_URL`. Want to self-host? Point both at localhost. The three layers are fully decoupled: model vendors provide the intelligence layer, database vendors provide the memory layer, and **the harness owns execution and control**. Claude Code, Cursor, Devin, and the other products evolving at breakneck speed today are all harnesses at heart.

This arrangement is not an architect's aesthetic preference. It follows from a simple set of forces.

In the endgame, the real moat is neither compute nor the model. Compute matters in the short term but commoditizes over time; there is no permanent monopoly on electricity. Models matter in the medium term but eventually democratize. Open models climb another rung every year, and the gap between GPT-5 and DeepSeek V4 is already far smaller than it was in the GPT-4 era. In another two years, agents will probably be choosing from a broad commodity market, with a model for every budget and workload. Only one moat truly holds: **private data**.

Serious enterprise users will not allow a single vendor to swallow all their core data, nor will they tolerate having it mixed haphazardly with everyone else's inside a vendor's black box. Once locked in, that vendor gains permanent pricing power over them. The last thirty years of database and cloud procurement tell the same story. The equilibrium is therefore the architecture above: **model vendors own intelligence, harnesses own execution and control, and database vendors own memory**. None can absorb the others; each keeps the others in check.

That is the three-way endgame: **model, harness, and database—each independent, each sovereign**.

Now we can return to the key question: where do today's memory frameworks fit?

-------

## 2. What Is a Memory Framework?

We first need to separate these projects more carefully, so we do not condemn a whole field with one broad stroke.

The projects currently tossed into the "memory framework" bucket are not all the same. They fall into several categories, each with a different fate.

**The first category is database-wrapper SDKs.** Early Mem0, LangMem, MemoryScope, and SuperMemory are representative. Their core capability is an `extract / store / retrieve / update` API wrapped around a database, usually PostgreSQL plus pgvector or SQLite. They put episodic and semantic memory in separate tables, then add a few rules for importance scoring and time decay. These projects are **little more than thin database wrappers: no technical moat, but some product mindshare**.

**The second category is knowledge-graph and temporal-graph builders.** Graphiti, Cognee, and Hindsight are representative. They do more than the first category: bi-temporal knowledge graphs, incremental entity resolution, conflict detection and invalidation, and hybrid retrieval across semantic search, keywords, and graph traversal. There is real engineering in this strategy layer; it cannot be dismissed as "a few SQL queries." But its fate is still clear: **models will absorb the strategy layer by handling entity resolution and conflict judgment themselves, while the storage layer will return to databases through PostgreSQL extensions or dedicated graph databases. There is still no independent category here**.

**The third category is agent runtimes or agent operating systems.** Letta/MemGPT is the clearest example. What it does is not really the job of a memory framework at all: it treats the context window as RAM, external storage as disk, and lets the model swap data between the two through tool calls. That is virtual-memory management in the operating-system sense. The technical bar is real, but the accurate name is **Agent Runtime**—an execution-engine layer beneath the harness. It belongs in the Runtime/Harness market, not the Memory market.

In short: the first category will be replaced by a Skill plus a model that writes its own SQL; the second will split between models and databases; the third belongs to Runtime/Harness, not memory.

-------

## 3. There Is No Moat

Now return to the first category, database-wrapper SDKs. It accounts for most of the market and is the main target of this essay.

Strip these projects to the studs and they do two things: **design a few database schemas for the agent and wrap a few SQL queries for it**.

Splitting episodic and semantic memory into separate tables is schema design. Importance scores, time decay, and reflection-driven compression are a few rules run at write time. Vector retrieval plus BM25 plus cross-encoder reranking plus RRF fusion is query composition. Strip away the terminology in every press release and every brain-inspired arrow diagram, and what remains is **tables and SQL**.

Do tables and SQL constitute a moat? They are the kind of thing programmers learn in week one. So why should the framework be valuable? Because it has "figured out" the schema and queries for the agent.

How much is that worth?

I considered this recently: take PostgreSQL, add a few extensions and stored procedures, and recreate Mem0 from scratch. A few days would have been enough. I did not do it. Why? **It was not interesting, and there was no moat**. Any engineer who knows their way around PostgreSQL could hack together a basic Mem0 in an afternoon and get 90 percent of the functionality. The remaining 10 percent is the UI, the SaaS console, the release cadence, and developer relations. Those can be operational and product moats, but they are not technical ones.

And how much does it take to teach an agent to use the system? **One Skill. One Markdown file.**

A few hundred tokens of instruction: "You have a PostgreSQL database at `DATABASE_URL`. When the user speaks, decide which facts are worth storing. Before every answer, run hybrid vector and full-text retrieval. If new information conflicts with old information, `UPDATE` the old record." That is it. Mem0's ADD / UPDATE / DELETE / NOOP pipeline, Cognee's graph construction, Graphiti's temporal graph—the cognitive architectures behind them now do things that models can accomplish by writing SQL themselves, often with cleaner SQL.

Claude's Skills mechanism has already taken us halfway down this road. A user can write `memory-skill.md`, explain how memory should be stored and queried, and Claude will invoke it when needed—no external memory framework required. The day Anthropic or OpenAI publishes an official memory Skill as a best practice, this entire class of projects will be redundant at the model layer.

**What you thought was a moat is really a short Markdown file a few hundred tokens long.** In production, that file will of course connect to controlled tools and hardened database pipelines. But the harness owns the former and the database owns the latter. There is still no place for an independent memory framework.

-------

## 4. The Bitter Lesson

The previous section argued from industry structure that memory frameworks have nowhere to stand. A deeper methodological argument cuts the same way: **The Bitter Lesson**.

Sutton's thousand-word 2019 essay makes a simple point. For seventy years, AI has replayed the same script: researchers encode their painstaking domain understanding into a system; it performs well in the short term, then eventually loses to a general method that lets the model learn for itself. Chess evaluation functions lost to search. Handcrafted Go priors lost to self-play. Phoneme modeling in speech recognition lost to statistical methods. SIFT in computer vision lost to deep learning. Every time, the approach built on "domain understanding" lost. The winner was the method that looked unintelligent but could consume more compute and data.

That argument needs careful handling. It **does not cut down** every system abstraction. Operating systems, databases, and compilers are all human-designed abstractions. They have not been swallowed by end-to-end learning, and they will not be, because they provide reliable low-level building blocks rather than making decisions for the AI. Sutton's lesson targets the latter.

The problem with memory frameworks is that they stand on that side of the line. They hard-code judgments about what is worth remembering, which layer it belongs in, when reflection should trigger, and how vector and full-text retrieval should be combined. Every one of these is an opinion about cognition made on the agent's behalf, not a general-purpose building block. The real building blocks—vector storage, full-text search, transactions, and indexes—already come from the database. Agents need these opinions today only because models are not yet strong enough. Once models can make the judgments themselves—and that is already happening—these handcrafted cognitive strategies will turn into scrap metal overnight, just as SIFT did when AlexNet arrived.

Memory frameworks have no place in the industry structure, and the methodological case cuts against them too. The two lines meet here.

-------

## 5. Where the Real Moats Are

So what **does** have a moat?

Strictly speaking, the three-way diagram contains two positions with clear moats. The moat around the third is still taking shape.

**The model layer** will be a bloodbath: closed versus open, prices halving every year, and vendor rankings reshuffling every six months. There is a moat here, but it belongs to a handful of leading model vendors, and the landscape is still changing violently.

**The harness layer** has not settled. Claude Code and Codex currently lead the pack, but others are appearing: OpenClaw and Hermes, for example. Letta/MemGPT's agent-runtime approach could also become interesting if it works. Harnesses had only just begun to build moats when Claude Code went open source and flattened the field again.

That leaves **the database**, the position with **the highest certainty in the entire picture**.

That certainty comes from a structural fact: **databases are outside AI's blast radius**.

What does AI disrupt? Anything whose value comes from processing information: copywriting, design, junior programming, legal documents, customer support, and slide decks. Their essence is mapping information A to information B, which is exactly what an LLM does. The more capable the LLM becomes, the more those fields are compressed.

What is not on that front line? **The physical world's persistence layer.** A database stores bytes on real disks, through real operating systems and file systems. It withstands real power failures and crashes. It reaches consensus across nodes over real networks, so those bytes can still be read correctly twenty years later. This is not fundamentally information processing. It is **a reliability guarantee in the physical world**. No matter how intelligent an LLM becomes, it cannot conjure a disk, guarantee `fsync` semantics, or replace two-phase commit.

The more powerful an agent becomes, the more it needs a reliable anchor in the physical world. The agent revolution will not diminish the value of databases. **It will magnify it.**

So in the three-way endgame, the model vendors will fight until they bleed, and the harness builders are still feeling their way forward. **Only the database foundation was laid thirty years ago and will still be there thirty years from now.**

-------

## 6. All Roads Lead to PostgreSQL

Which database will own the memory layer?

The answer depends on the stage of development.

**Today**, for a personal agent running locally or a lightweight agent on one machine, **SQLite or even the file system is entirely sufficient**. SQLite is zero-ops, file-based, and local, with JSON support and vector extensions. It can comfortably handle the memory needs of a standalone agent. Many agent applications already use SQLite directly for local persistence. Insisting that the memory layer needs PostgreSQL at this stage is overengineering.

**Take one step forward, however. Once agents need cross-agent collaboration, cross-device persistence, portability across organizations, multi-tenancy, and concurrency—in other words, a universal, portable memory layer—the market converges.** On what?

**PostgreSQL.**

There are three reasons.

**First, the convergence is already happening.** Many projects serious about agent infrastructure are moving toward PostgreSQL or PostgreSQL-compatible backends. Letta officially supports PostgreSQL plus pgvector. Hindsight explicitly supports only PostgreSQL plus pgvector. Tiger Data named an entire product line Agentic Postgres. This is not the PostgreSQL family proving its own point—Supabase and Neon do not count. These are **projects that started elsewhere and are now converging on PostgreSQL**.

**Second, the wire protocol is the de facto standard.** The PostgreSQL protocol plays the same role for a universal memory layer that HTTP plays at the application layer: it is old, stable, general, and open. No vendor owns it, and no vendor can replace it. Models have seen SQL and `psql` millions of times in their training data. They already speak the language without additional training. A database with a proprietary protocol enters the AI era with half the battle already lost, because the model does not know it.

**Third, the extension ecosystem already covers every retrieval primitive a memory layer needs.** Vectors have pgvector. Full-text search has `tsvector` and GIN. Graphs have AGE and a new generation of PostgreSQL-based graph extensions. Time series has TimescaleDB. Geospatial has PostGIS. Horizontal scaling has Citus. These arrive as extensions rather than rewrites of the whole system, because PostgreSQL made one crucial decision thirty years ago: it would not impose upper-layer semantics. That is PostgreSQL's real superpower. Any new workload can still plug into it thirty years later.

The evolutionary path is therefore clear: **for a universal, portable memory layer, there is no alternative to the PostgreSQL protocol**. Graph databases, object storage, on-device SQLite, and dedicated search systems will continue to thrive in their specialized niches. There is no contradiction there. But for universal agent memory, PostgreSQL is the end state.

SQLite and PostgreSQL belong to the same architectural family. Both are general-purpose persistence layers. Neither imposes upper-layer semantics. Both have decades of accumulated reliability, sit outside AI's blast radius, and offer exceptionally flexible extension models. SQLite is PostgreSQL for the edge and local use; PostgreSQL is SQLite for servers and collaboration. They are two sizes of the same idea.

What the three sides carve up is the middleware sitting between database and application—in other words, today's memory frameworks.

------

Return to the three-way diagram. The model layer is fluid, the harness layer is taking shape, and the memory layer is settling. Each territory has its own sovereign. None contains a place for today's memory frameworks. The frameworks are not rivals to any one side. They are middlemen temporarily doing work for all three while the layers mature. Once those gaps are filled, the middlemen have nowhere to go.

When we look back ten years from now at the memory-framework frenzy of 2026, the story will be prosaic. The frameworks that claimed to "design cognition for agents" will leave behind only their most basic code: **the few lines of SQL that simply put the data into PostgreSQL**.

Everything else will be eaten by end-to-end learning.
