---
title: "After the Debate, Let's Talk Seriously About 'Ontology'"
date: 2026-03-15
summary: >
  Palantir's Ontology is, technically, data modeling. The more interesting question is how a philosophy term got repurposed to market system integration and data modeling, and why that story is so likely to turn into another round of concept inflation in China's tech ecosystem.
tags: [Ontology, Palantir, Data Modeling, Industry Analysis]
---

Last month I wrote a post called ["The Palantir Ontology Scam"](https://vonng.com/db/ontology-bullshit/).
The core point was simple and summarized in a Rosetta Stone-style comparison table:
Palantir's Ontology is, at the technical level, database modeling.
Object Type is a table. Property is a column. Link is a foreign key. Action is a stored procedure.

The post triggered a lot of argument and eventually turned into a live public debate.
The debate result itself was not especially interesting. The audience vote ended with 75% on my side, but winning a debate is not the point.
The previous article did the demolition.
This one is about the deeper layer:
what ontology actually is, what Palantir did to the term, and why Chinese imitators are likely to fail if they try to copy the story.

---

## TL;DR

**On Palantir**

Palantir's products have real engineering value.
Data modeling, system integration, and analytics are all legitimate work.
The problem is not that the work is fake. The problem is attributing that value to "ontology."

Palantir is, in substance, a consulting company wearing a SaaS costume.
Its real moat is not a philosophical breakthrough.
It is Peter Thiel's political network, security-clearance access, a labor-intensive FDE model, and the path dependence created by vendor lock-in.
Ontology is camouflage for those actual sources of advantage.

Palantir's "Ontology" is not a technical innovation.
It is the philosophical packaging of database modeling.
Its own patents effectively admit as much.
This is a narrative architecture, not a technical architecture.

**On ontology**

Ontology is a 2,500-year-old branch of philosophy concerned with the deepest question of all:
what exists, and what is the fundamental structure of existence?
There is no single correct answer.
Philosophy has produced multiple competing frameworks, and those frameworks map surprisingly well onto different styles of database modeling.

Palantir's version grabs only one strand of that tradition:
an Aristotelian entity ontology.
It mistakes one part for the whole.
The irony is that both modern physics and much of modern software engineering increasingly move in the opposite direction:
relations can be more fundamental than entities, and events can be more fundamental than objects.

**On Chinese imitators**

Chinese companies copying "Ontology" are performing a classic cargo cult.
Ontology was Palantir's way of obscuring its actual moat.
The imitators copied the smoke instead of the engine.

This is likely to repeat the lifecycle of "data middle platform" in China:
canonized, overfunded, disillusioning, and then discarded.
The Chinese tech ecosystem lacks a strong mechanism for aggressive concept cleanup.
There is no local equivalent of a constant Hacker News or Reddit instinct that says, "X is just Y with extra steps."

That is why I keep mocking ontology.
Not because data modeling is worthless, but because concept pollution matters.

---

## 1. The Fact Pattern: Ontology Is Data Modeling

### The Moment the Patent Has to Tell the Truth

If you want to know what Palantir means by Ontology, do not start with the marketing site.
Start with the patents.
When companies need to speak precisely, they usually become much more honest.

In the background sections of Palantir's ontology-related patents, including `US7962495B2`, `US9589014B2`, and `US11714792B2`, the term is described this way:

> Computer-based database systems, such as relational database management systems, typically organize data according to a fixed structure of tables and relationships. The structure may be described using an ontology, embodied in a database schema, comprising a data model that is used to represent the structure and reason about objects in the structure.

Source: <https://patents.google.com/patent/US7962495B2/en>

That sentence matters.
The patent text is effectively saying:

> Ontology = embodied in a database schema = comprising a data model

In other words, in Palantir's own patent language, Ontology **is** a database schema.
It **is** a data model.
It is not some category that transcends schema. It is schema, reworded.

Some people respond by saying that the background section only describes prior art, not the invention itself, and that the claims must be where the magic is.
I read the claims.
They define ontology so broadly that it basically covers any structured way of describing and managing data, without giving a concrete technical definition that meaningfully exceeds a data model.

If Palantir had a genuinely revolutionary construction beyond data modeling, its patent lawyers would have described that novelty in the claims with precision, because more concrete innovation means stronger protection.
They did not.
That is a tell.

None of this means Palantir does nothing valuable.
System integration is real work.
Integrating messy systems under military-grade security constraints takes real engineering.
But the correct name for that work is still **system integration**, not ontology.
You would not call interior renovation "spatial ontology" just because renovation involves structure and function.

### The Most Important Sleight of Hand

The word "ontology" changes meaning multiple times on the way from philosophy to Palantir.
An uncountable discipline becomes a countable product.
A search for the true structure of the world becomes a search for a model everyone can agree on.
A descriptive inquiry into what the world is becomes a prescriptive decision about how the world should be represented.

But the most damaging substitution is a reversal of purpose.

Tom Gruber's 1993 work on ontology in the semantic-web sense focused on **portable ontology specifications**.
The key word there is **portable**.
The goal was knowledge sharing and interoperability, so systems could understand one another's data.

Palantir's Ontology pulls in the opposite direction.
The modeling process can take months. Switching costs are high. Data is hard to migrate out.
In 2017, when the NYPD ended its relationship with Palantir, it publicly complained that Palantir would not provide the resulting analytics in a portable format.
That dispute was documented by [BuzzFeed News](https://www.buzzfeednews.com/article/williamalden/theres-a-fight-brewing-between-the-nypd-and-silicon-valley) and the [Brennan Center for Justice](https://www.brennancenter.org/our-work/analysis-opinion/palantir-contract-dispute-exposes-nypds-lack-transparency).
Michael Burry later used this as an example of Palantir's moat being migration friction itself.

Gruber designed ontology to build bridges.
Palantir turns the bridge into a wall.

---

## 2. The Incentive Story: Carrots and Radar

Once the technical point is settled, the next question is obvious:
if there is nothing fundamentally new here, why insist on the word "Ontology"?

Because the word is valuable.

### Valuation Narrative

If Palantir told Wall Street, "our core capability is doing data modeling and system integration for difficult customers," then the natural comparison set would be firms like Booz Allen Hamilton or Accenture.
If it says, "we built an Ontology platform," then the comparison set shifts toward Snowflake or Databricks.

I am not claiming this one word creates the entire valuation premium.
Political ties, growth expectations, government contract stickiness, the AI narrative, and the scarcity of public defense-tech names all matter.
But the Ontology story performs one crucial cognitive shift:
it helps investors model a consulting-heavy business as if it were a pure software platform.

The multiple changes when the category changes.
One word can be worth a lot of money.

### The Real Moat Is in Washington

In 1940, British pilots used airborne interception radar to shoot down German bombers at night.
To protect the secret, the British government pushed the story that pilots had excellent night vision because they ate a lot of carrots.
They even invented "Doctor Carrot" as propaganda.
Reportedly, the Germans started feeding their own pilots more carrots too.

**Ontology is Palantir's carrot.**

The real weapon is the radar:
CIA roots, rare security clearances, and two decades of defense experience.
Palantir was founded in 2003. CIA-backed In-Q-Tel invested in 2004.
The amount was not huge, but the signaling value was enormous.
That kind of backing helped Palantir secure elite access and enter the post-9/11 defense market.

By 2024 and 2025, the scale of military contracts was staggering: Project Maven, large Navy deals, huge Army agreements.
Were those contracts won because of "ontology"?
No.
They were won because of political relationships, security accreditation, procurement positioning, and Silicon Valley competitors abandoning military work that Palantir was happy to accept.

Ontology had nothing to do with that.

### FDEs Are the Honest Counterexample

If Palantir's Ontology were truly a revolutionary intelligent platform, why does the company still need thousands of highly trained engineers embedded at client sites for long periods?

Because real enterprise data is chaos.
Any static model immediately collides with ugly operational reality.
Forward Deployed Engineers are doing exactly what system integrators always do:
writing ETL, fixing connectors, resolving schema mismatches, and manually cleaning dirty data.

Accenture calls those people a delivery team.
Palantir calls them FDEs.

The harder the system is to use, the more essential the FDEs become.
The more obscure the concept, the less replaceable those engineers look.
That is not a bug. It is part of the model.

Michael Burry once described Palantir bluntly as "a consulting company disguised as a SaaS company."
The existence of the FDE model is one of the strongest pieces of evidence for that view.

If your ontology platform were really that magical, why does it need so many human babysitters?

---

## 3. Ontology Proper: Databases Are the Closest Practical Version

At this point, saying "Ontology is just table design" is directionally correct, but still incomplete.
Because it hides the more interesting question:
**what does philosophical ontology actually have to do with databases?**

The answer is: quite a lot.
**Among engineered artifacts, databases may be one of the closest practical expressions of ontology.**
And the shallowness of Palantir's use of the term is exactly what makes it philosophically thin as well.

### A 2,500-Year Question

Ontology asks:
**what exists, and what is the fundamental structure of what exists?**

There is no settled answer after 2,500 years, not because philosophers are stupid, but because the question does not admit a single universally correct decomposition of the world.
How you carve reality determines what you see.

Databases are the engineering answer to exactly that carving problem.
Every database paradigm carries an implicit assumption about the structure of the world.

This is not mysticism.
If you model a domain relationally rather than as a graph, you have already made an ontological choice.
You are assuming that independent entities with properties are primary, rather than treating relationships as primary.

The following table is a heuristic analogy, not a formal proof in the history of philosophy.
No database designer chose a model because they were reading a particular philosopher.
But the structural correspondence is real enough to be useful:

| Ontological stance | Core claim | Rough database analogue | Engineering meaning |
|------|------|------|------|
| Aristotelian substance ontology | The world is made of independent entities with properties | Relational databases | Entity modeling, schema first |
| Whiteheadian process philosophy | Events are more fundamental than objects | Event stores / Kafka | Event sourcing, append-only |
| Structural realism | Relations are more fundamental than entities | Graph databases | Relationship-first modeling |
| Humean bundle theory | Entities have no fixed underlying structure | Document databases | Schema-light flexible documents |
| Ockham-style nominalism | Only individuals exist | Key-value stores | Minimal structure, minimal assumptions |
| Heraclitean flux | To be is to change | Time-series databases | Everything is a time series |

The lesson is simple:
ontology is not one method.
It is the field that asks what **kinds** of methods are possible, what each one assumes, and what each one hides.

### Palantir Took One Row and Named It the Whole Table

Once you see the table, Palantir's move becomes obvious:
**it took the first row only.**

Aristotelian entity ontology became Object -> Property -> Link -> Action, and then got branded as "Ontology."
That is like reading the first chapter of philosophy and declaring mastery over the entire subject.

The deeper problem is that once a specific paradigm gets named "Ontology," awareness of alternatives starts to collapse.
If something is called a **data model**, engineers understand that different data models exist.
You can switch to graph, document, event, or something else.

If something is called **Ontology**, the name implies that it corresponds to the structure of reality itself.
Who argues with "being"?

The danger of a grand term is not only that it says the wrong thing.
It also trains people to stop asking questions.

### What Better Ontology Practice Looks Like

If you want an example of ontology practice in the healthier sense,
meaning an environment that does not presuppose there is only one correct decomposition of the world, look at PostgreSQL.

Relational modeling is the center.
But through extensions PostgreSQL can also support document-style work (`JSONB`), graph (`Apache AGE`), vectors (`pgvector`), time-series (`TimescaleDB`), and event-driven patterns (logical replication plus CDC).

One system can host multiple ontological assumptions, and the user can choose the one that fits the problem.

That is not just better engineering.
It is also better philosophy:
accepting that the world may admit multiple useful structures, and that your current lens is not absolute.

Palantir's Ontology does not even seem aware of the limits of its own lens.

### Event Sourcing Is Enough to Break the Claim

I do not need to prove that event sourcing is universally superior to entity modeling.
I only need to show that **there exists a legitimate modeling paradigm that Palantir's Ontology cannot natively express**.
That alone is enough to show it does not deserve the universal title.

Event sourcing starts from a simple idea:
do not record the current state as primary truth.
Record what happened.
State can be derived from event history. The reverse is not generally true.

Finance, logistics, and microservices use this pattern more and more, not because engineers are reading Whitehead, but because reality keeps teaching the same lesson:
in many domains, events are more fundamental than objects.

Palantir's Ontology can attach Event objects to entities, but events remain subordinate.
They are linked to objects. Time-series data becomes just another property.
You cannot say, "my domain model is fundamentally an event stream, and entity state is only a derived view," and expect the framework to treat that as native.

That reversal of priority is not first-class there.

The irony is that Palantir engineers themselves have used event-sourcing ideas internally.
They have written about rewriting internal Foundry job orchestration away from CRUD toward event-sourced architecture.

They keep the meat.
Customers get the bones.

**Palantir sells Types. Ontology, in the serious sense, asks whether the Types themselves are the right ones.**

---

## 4. Waiting on the Bamboo Runway

### Cargo Cult

After World War II, some island communities in the South Pacific saw American planes bring in enormous quantities of material goods.
After the war, when the military left, people built bamboo control towers, made headphones out of coconuts, and laid out runways in the jungle, hoping the cargo planes would return.

Feynman used this story in his 1974 Caltech commencement speech to explain cargo-cult science:
all the forms are there, but the causal engine is missing.

Some Chinese companies imitating Ontology are doing the exact same thing.
Consultancies and data-platform vendors pick Palantir as a reference and then announce that they too are doing "ontology."
What they copy is the term, not the moat:
not the security clearances, not the Washington relationships, not the defense experience, not the labor model.

**Ontology was Palantir's way of hiding its real moat. The imitators copied the disguise itself.**

### We Have Seen This Movie Before: The Data Middle Platform

If the cargo-cult analogy feels too abstract, here is a much more Chinese example.

**Palantir's Ontology is roughly the American version of the "data middle platform."**

Around 2019, "data middle platform" became a mandatory executive talking point in China.
Companies spent enormous budgets on projects that were often little more than data warehouses, ETL pipelines, metadata systems, and service APIs wrapped in managerial theater.

Then the disillusionment arrived.
Projects missed ROI. Teams were cut. Even Alibaba, the company most associated with the concept, later dismantled its own middle-platform structure.
By 2024, the term was already treated as stale in many analyst contexts.

From altar to grave took about five years.

The technical substance of the data middle platform was:
warehouse + ETL + metadata + APIs + managerial narrative.

The technical substance of Palantir's Ontology is:
tables + columns + foreign keys + procedures + philosophical narrative.

The packaging logic is almost identical.
Only the wrapping paper changed.

The core demand behind data unification was real.
The failure was not that the need was fake.
The failure was that grand language systematically inflated expectations.

If you call something a "middle platform," the implied budget and timeline explode.
If you call it "a data warehouse project," people stay more rational.

Ontology is currently in that same expectation-inflation phase in China.
Five years from now, many of today's ontology chasers will look exactly like the middle-platform chasers of 2019.

---

## 5. Concept Sanitation

### Good Abstraction vs. Bad Naming

Some people respond by saying:
all abstraction is renaming.
SQL is just set theory. OOP is just structs with function pointers. React is just a state machine.
By that logic, every software innovation is old wine in a new bottle.

That sounds clever, but it conflates two different things.

The difference is actually easy to test.

**Good abstractions lower the barrier to entry.**
SQL lets non-programmers query data.
Kubernetes lets developers deploy without thinking directly about machine allocation.
The abstraction hides lower-level complexity and broadens access.

**Bad naming raises the barrier to entry.**
"Ontology" turns something learnable, namely the first few chapters of any data-modeling textbook, into something that sounds mystical and out of reach.
Young engineers come away thinking they need to study an exotic new discipline when `CREATE TABLE` is still the starting point.

**Good abstractions have open implementations.**
Linux has many distributions. SQL has many databases. HTTP is an open protocol.

**Bad naming manufactures lock-in.**
Palantir's Ontology takes months to model, is expensive to exit, and makes migration painful.
The bridge becomes a wall.

**Good abstractions work even if you do not know the term.**
You do not need to understand relational algebra to write `SELECT * FROM users`.

**Bad naming derives value from the name itself.**
"We need to build an Ontology" and "we need to build a unified data model" trigger very different expectations in enterprise buyers.
The former sounds like a three-year, multi-million-dollar strategic initiative.
The latter sounds like an engineering project.

## Why Keep Criticizing Ontology?

Praising Palantir and praising Ontology is safe.
Criticizing them annoys an entire class of data-consulting companies.
So why bother?

Because I dislike the abuse of grand words.
Palantir is only one especially clear case of a broader pattern.

The damage from grand terms is systemic.
Each hype cycle burns a little more trust:
cloud computing, big data, middle platforms, blockchain, large models, and whatever comes next.
After enough cycles, smart people become more cynical, and when a genuinely valuable concept finally appears, it gets buried in the rubble of exhausted trust.

In the US, a grand new term appears and within 48 hours someone on Hacker News is saying, "X is just Y with extra steps."
China's tech ecosystem lacks enough of that self-cleaning instinct.
The incentives on content platforms reward trend-chasing, not bubble-puncturing.
An imported concept arrives, and instead of being trimmed back, it grows wild.

Silicon Valley has both a Shenzhen side and a less flattering side.
Not everything imported from the US is good.
Importing low-grade concepts is not technology transfer.

Someone has to do concept cleanup.
If people keep littering the conceptual landscape, someone eventually has to sweep.

## Closing

If you are doing data modeling, call it data modeling.
That name is not beneath anyone.
People like Codd, Chen, Kimball, and Inmon spent decades giving the discipline dignity.
Renaming data modeling as "Ontology" does not elevate it.
It implies the original name was not good enough.

I am not against new concepts.
I am against people throwing conceptual garbage around and calling it innovation.

The next time you see a grand term, whether it is "World Model," "Logos," or something else, ask two questions first:
what is the underlying technical substance, and who benefits from the naming?

Respect for facts is still a basic engineering virtue.
