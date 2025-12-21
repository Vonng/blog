---
title: In the AI Era, Software Starts at the Database
summary: "Future software = Agent + Database. No middle tiers, just agents issuing CRUD. Database skills age well, and PostgreSQL is poised to be the agent-era default."
date: 2025-04-27
tags: [Database, PostgreSQL, AI]
---

> [WeChat](https://mp.weixin.qq.com/s/LykR-ewCx9aO9e09T45taw)

The future stack is “Agent + Database.” No front-end/back-end toll booths—agents talk CRUD straight to storage. Database skills hold their value, and PostgreSQL is the database of the agent era.

-------

## SaaS is dead? Software begins with the DB

GenAI exploded, but underneath the hype, software still begins with data stores. Microsoft CEO Satya Nadella said it bluntly: in the agent era, **SaaS is dead**; the future form factor is Agent + Database.

> “…the notion that **SaaS** business applications exist, that’s probably where they’ll all collapse, right in the Agent era…”
> — Satya Nadella (<https://medium.com/@iamdavidchan/did-satya-nadelle-really-say-saas-is-dead-fa064f3d65d1>)

> “Enterprise apps are basically CRUD databases plus business logic. Agents will move that logic into the AI layer—they’ll cross databases, they don’t care about backends, they’ll mutate whatever table they need. Once the logic lifts into AI, people will happily rip out the old middle tier.”

If you’ve tried Vibe Coding or an MCP desktop, you know what he means. You can talk to Claude or Cursor to query PostgreSQL directly—LLMs draft SQL, execute it, and weave the results back. For simple analysis it already beats my expectations.

As application logic migrates to agents, the only thing left holding the backend line is the database. That makes the DB the “calming stone” in the AI storm. Let’s dig into why DB skills hold value, which skills depreciate, and which engines thrive when agents rule.

-------

## Agent + DB: bye-bye middlemen

Apps used to be the broker between humans and data: click UI → backend → DB → UI render. AI agents threaten that role. They can talk to databases directly and drop the intermediate shell.

Take **booking a flight**. Historically you’d fill a form, the backend hit APIs, and you got HTML back. In the new pattern you say, “Book me the cheapest nonstop to Tokyo next Monday, window seat.” The agent hits every airline, compares, writes the reservation straight to their databases, and mails you the ticket. The agent is the UI; the middle tier disappears.

Sure, most users picture RPA-style agents moving a mouse. But the ideal endgame doesn’t need screens at all—those were built for humans. Machines can skip straight to the data. Security and permissions still need solving, but the macro trend is clear: logic climbs to the AI layer, and the database becomes the raw-material warehouse and workbench. Far from marginalized, it becomes the privileged interface.

Nadella is pointing at that end state. In the AI era, “no middleman markup” stops being a meme. Agents are universal assistants, and databases are their toolbox. MCP mania is just the prelude.

## Skills that rot vs. skills that stick

When agents can write UI, glue APIs, and reason over business logic, what’s left for humans? Anything that’s pure boilerplate—cranking REST endpoints, wiring forms, rote CRUD—is toast. The durable skills are the ones closest to data gravity: schema design, query optimization, transaction semantics, multi-tenant isolation, storage internals. Databases stay hard, and thus stay valuable.

## Which databases win?

So which engines should you bet on? The short answer: PostgreSQL, with SQLite playing the edge role. PostgreSQL already powers OpenAI, Cursor, Dify, Notion, Cohere, Replit, Perplexity, and virtually every new AI startup. Anthropic never said it publicly, but MCP samples ship with PostgreSQL alongside the filesystem.

Cursor CTO Sualeh Asif said it on Stanford’s CS153 Infra @ Scale stage (<https://www.youtube.com/watch?v=4jDQi9P9UIw>):

> “Just use Postgres. Don’t overthink it.”

Why? Because Postgres handles everything in one engine: relational data, vectors, JSON, GIS, full-text, graph-ish workloads, and, thanks to DuckDB fusion, OLAP that rivals ClickHouse. That all-in-one capability is exactly what multi-modal agents need. If you can solve in one SQL statement what used to take 1,000 lines of glue code, you slash the LLM’s cognitive load and token burn.

**PostgreSQL + pgvector** has become the default safe bet for LLM-native products. pgvector started as a hobby extension. Then the OpenAI Retrieval Plugin blew up the vector DB hype, and the PG ecosystem—AWS, Neon, Supabase—poured resources into pgvector. It leapfrogged half a dozen competing PG vector extensions, improved 150× in a year, and turned purpose-built vector databases into a punchline. Even Milvus, the strongest bespoke player, can’t beat a community backed by AWS RDS and a swarm of elite teams.

SQLite will have a renaissance on the agent edge too—hence PG-adjacent projects like PGLite and DuckDB embeddings.

And yes, my plug: PostgreSQL is fantastic but hard to run well. Managed RDS is pricey, senior DBAs scarce. Pigsty—the open-source PostgreSQL distro I maintain—bundles the best extensions (pgvector by default) and lets you spin up production-grade PG on bare metal in minutes. It’s free and open source; paid support is optional if you want experts on call. Use it to skip the yak shaving and let agents sit on top of a rock-solid Postgres stack.
