---
title: "What Kind of Database Do AI Agents Need?"
date: 2025-12-21
authors: [vonng]
summary: >
  The bottleneck for AI agents is not the database kernel, but integration above it. Muscle memory (in-database computation), associative memory (vector-graph fusion), and the courage to experiment (Git for Data) will be critical—none of them requires a new engine.
tags: [PostgreSQL, AI, Agent, Database]
ai: true
aliases: ["/ai/agent-native-db/"]
---


When we talk about “databases for the AI era,” it is easy to fall into a familiar trap: assuming the shift requires a brand-new storage engine, a revolutionary index structure, or a disruptive query language.

But a clear-eyed look at the problem suggests the opposite: **the real transformation is not in the database kernel, but in the layer above it.**

> [Original WeChat post](https://mp.weixin.qq.com/s/zFpFECMOCbllihvuh-2BaQ)

------

## 1. A Brain in a Vat

Today’s AI agents are in an awkward position.

They have astonishing reasoning capabilities. They can write code, perform analysis, and build complex multistep plans. Yet they are forced to inhabit a crude environment of “file systems plus external scripts.” LangChain defaults to `InMemoryStore`, so a process restart wipes its memory. AutoGPT writes state to JSON files, inviting race conditions when multiple agents collaborate. Even the most advanced agent frameworks must maintain three separate systems: a vector database, a relational database, and a cache.

This architecture resembles a **brain in a vat**: a powerful mind suspended in nutrient fluid, connected to the outside world through a few narrow tubes. Every perception must traverse a long chain of data extraction, serialization, network transfer, external processing, and writeback. The agent’s “neural transmission speed” slows by orders of magnitude.

What is the root cause?

It is not that databases are too slow or their indexes too weak. It is that **agents lack a unified “digital body”**—an integrated container that brings together skills, memory, and reasoning.

------

## 2. Three Missing Organs

If we use human intelligence as our model, today’s agent architectures are missing exactly three critical “organs”:

**No muscle memory.** Once humans learn to ride a bicycle, we do not have to “think” about how to balance every time. The skill has been internalized as unconscious instinct. But every time an agent performs a task, it must generate code again, invoke an external runtime, and wait for the result. It has no “reflexes,” only deliberation.

**No associative memory.** Human memory is not a keyword index but a network of associations. A song can remind us of a first love; a smell can evoke our hometown. But agent memory is split between vector databases, which understand only semantic similarity, and knowledge graphs, which understand only explicit relationships. The two operate in isolation and cannot make connections across domains.

**No imagination.** Before acting, humans can mentally rehearse different possibilities, assess risk, and choose the best path. But the database an agent sees has a “single timeline”: every operation acts directly on production, leaving no safe imaginative space in which to experiment.

Together, these three missing pieces put a ceiling on agent autonomy. Without muscle memory, an agent reacts slowly. Without associative memory, it is blind to context. Without counterfactual simulation, it cannot afford to take risks.

------

## 3. Three Dimensions of a Paradigm Shift

Once we understand the problem, the shape of the solution comes into focus.

**First: from storing data to internalizing skills.** A database should be more than a passive data warehouse; it should become an agent’s “digital muscle.” In-database computation moves frequently used logic down into the data layer, allowing an agent to invoke a skill as naturally as a reflex. PostgreSQL’s multilingual runtimes—PL/Python, PL/Rust, and PL/V8—make this possible: functions live beside the data, eliminating the external execution path.

**Second: from keyword search to associative memory.** Vector similarity search alone cannot answer a question such as, “Who is the CEO of the company that released GPT-4?” which requires multihop reasoning. We must erase the boundary between vectors and graphs and build dynamic semantic graphs that support both fuzzy semantic matching and traversal over structural relationships. GraphRAG experiments show that this fused architecture can reach 87% accuracy on multihop reasoning tasks, versus just 23% for vector-only approaches.

**Third: from CRUD to counterfactual simulation.** Agents need “Git for Data”: the ability to create database branches instantly, simulate the consequences of different decisions in isolated environments, and then selectively merge or discard the results. This gives an agent real “imagination.” It can experiment boldly in parallel universes without risking damage to production.

------

## 4. An Overlooked Truth

But there is an easily overlooked truth here: **none of these three capabilities requires reinventing the database kernel.**

Vector indexing with pgvector is simply another application of PostgreSQL’s extension mechanism. The same is true of graph queries with Apache AGE. In-database computation is a natural extension of stored procedures. Branching and time travel rely on MVCC and copy-on-write, both mature technologies.

The underlying mechanisms these capabilities need—ACID transactions, B-tree indexes, write-ahead logging (WAL), and query optimizers—are all **boring technology**, proven over decades to be stable and reliable.

In other words, the Agent-Native Database revolution is not about a new kernel, a new storage layer, or a new engine. Agents still need the database core as a precision instrument, and nothing is replacing it. **The real transformation comes from combining these “boring” technologies to support seemingly flashy new capabilities.**

This distinction is crucial. It tells us where to focus.

------

## 5. PostgreSQL’s Overwhelming Advantage

If the real battleground is the layer above the database, which system is best positioned to serve as the foundation?

There is really only one answer: **PostgreSQL.**

Not because it has the fastest queries—ClickHouse and DuckDB can beat it in analytics. Not because it has the strongest vector search—specialized vector databases still have an edge at billion-item scale. PostgreSQL’s advantage is its **unique extension architecture**.

PostgreSQL’s extension mechanism is not a shallow plugin system. It effectively opens the kernel to third-party code, allowing deep integration with the query planner, executor, storage engine, and transaction system. That means the community can turn any new capability—vector search, graph queries, time-series analysis, geospatial processing, or machine learning—into a native PostgreSQL feature without forking the core code.

**Even more important is composability.**

TimescaleDB plus PostGIS enables spatiotemporal analysis. pgvector plus BM25 enables hybrid search. Apache AGE plus pgvector enables GraphRAG. Specialized databases cannot match these combinatorial possibilities.

Pinecone only does vectors; Neo4j only does graphs. That is not a criticism: focus is the source of their strength. But an agent needs vector, graph, relational, time-series, and full-text capabilities **at the same time**, all within **one ACID transaction boundary**. Its “digital body” can then remain unified and consistent, with no separate systems to maintain, no cross-database synchronization to worry about, and no need to reinvent transactional consistency in the application layer.

One PostgreSQL instance is a complete cognitive infrastructure.

------

## 6. Where the Real Competition Is

If PostgreSQL is the settled foundation, where does the real competition happen?

The answer is **the upper layers of the PostgreSQL ecosystem**: the distributions and platforms that package extensions into products and turn boring technology into capabilities agents can use.

We can already see the outlines of this competition.

**At the extension layer**, three major arenas are fiercely contested: OLAP (pg_duckdb, pg_mooncake), full-text search (ParadeDB, vchord_bm25), and vector search (pgvector, pgvectorscale, vchord). Each arena has multiple contenders fighting to become the standard choice for that capability.

**At the platform layer**, Supabase packages PostgreSQL as an alternative to Firebase. Neon focuses on serverless operation and branching, provisioning databases in under 500 milliseconds. Pigsty offers a production-ready distribution with an integrated stack for monitoring, high availability, backup, and recovery.

Databricks’ acquisition of Neon for roughly $1 billion is a landmark event in this competition. It validates a thesis: **database infrastructure has strategic value in the agent era, and that value lies not in the underlying kernel, but in ecosystem integration.**

------

## 7. The Shape of a New Species

Over the next few years, we have reason to expect a new species to emerge from the PostgreSQL ecosystem: some form of **Agent-Native Platform**.

It will integrate pgvector, Apache AGE, PL runtimes, and database branching behind first-class APIs for agents. Developers will no longer need to learn each extension separately. They will call higher-level abstractions such as “memory storage,” “skill registration,” and “branch simulation” directly.

It will support MCP or similar protocols natively, allowing agent frameworks to connect to databases seamlessly. The database itself will become a tool for an agent—one that can be discovered, invoked, and orchestrated.

It may include built-in abstractions for memory hierarchies. The distinctions among working, episodic, and semantic memory will no longer be implemented in the application layer; the platform will support them natively, including automatic memory consolidation and forgetting policies.

This new species may evolve from an existing player or come from a disruptive newcomer. Either way, its foundation will inevitably be PostgreSQL, because only PostgreSQL has the extension depth and ecosystem breadth required to support such a unified platform.

------

## 8. Body and Soul

The metaphor of a database as an agent’s “digital body” contains a deep insight.

The body is not the soul, but the soul needs a body to act. An LLM is an agent’s reasoning core, but without a reliable memory system, an internalized library of skills, and a safe place to experiment, it remains a brain in a vat—intelligent but powerless.

A truly Agent-Native Database does not need to reinvent the wheel. A B-tree is still a B-tree, WAL is still WAL, and MVCC is still MVCC. These boring technologies are already good enough and reliable enough. What we need is a new abstraction layer built on this solid foundation—one that lets an agent use the database as naturally and fluidly as it uses its own body, without consciously thinking about low-level details.

**PostgreSQL is ready. Its extension ecosystem has already proved that this higher layer is possible.**

The only question left is: who will be first to integrate these scattered capabilities into a unified, agent-oriented platform?

The answer will emerge from the competition ahead.

And we are standing at the beginning of that transformation.
