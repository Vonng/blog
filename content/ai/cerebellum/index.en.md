---
title: "The Cerebellum: The Other Half of Intelligence—and the Strongest AI Hasn't Touched It"
date: 2026-06-10
authors: [vonng]
summary: >
  The cerebellum changed how I see AI's frontier: LLMs have already absorbed humanity's explicit knowledge and are beginning to acquire interventional data through agentic RL. What they still lack is a vessel for individual history.
tags: [AI, Agent, Machine Learning, Philosophy]
ai: true
---

Let me start with an uncomfortable number.

The cerebral cortex—the part we usually point to as evidence that "I am thinking"—contains roughly 15 billion neurons.
The cerebellum, tucked beneath the back of the brain and rarely given much thought, contains more than 60 billion.

Four times as many.

People love to turn this number into an argument about compute: "See? The real compute is in the cerebellum. The resources we spend training LLMs today are just a rounding error on the way to AGI."

I don't buy it.
Most neurons in the cerebellum are granule cells, the smallest and simplest neurons in the mammalian brain.
Their connections are highly repetitive; the entire circuit is as regular as an enormous lookup table.
Using their number as a proxy for "compute" is a bit like citing transistor count to prove that a GPU is smarter than a CPU.

What interests me about the number has little to do with compute.

It reminds me that an entire continent inside our skulls contains most of our neurons, yet does not perform what we casually call "thinking."
It is busy doing something else—something for which today's LLMs have no corresponding organ.

And that something may be precisely what stands between AI as a near-master and AI as a true master.

----

## 1. Even the Strongest AI Is Only a Near-Master

By 2026, the capabilities of LLMs need no introduction.
In any domain with standard answers, a scoring function, or a well-defined corpus, they are already approaching or surpassing human experts.

Yet I keep feeling that something is missing.

I don't mean knowledge.
Humans no longer have much ground left to contest there.
A model has read more papers, code, manuals, and forum posts than any one person ever could.

I mean the kind of *feel* that experienced practitioners acquire.
A DBA with twenty years on the job glances at a dashboard and thinks, "Something's wrong."
A veteran doctor hears two sentences and already knows where to look.
A programmer with more than a decade of experience scans a diff and knows that this line will cause trouble sooner or later.

Ask them why, and they often cannot tell you.

These people are not the same as star students who have memorized every textbook and can explain every concept perfectly.

I would call the latter **near-masters**.

A near-master's ability comes mostly from combining declarative knowledge.
Feed them everything humanity has managed to write down and explain, and they can synthesize it all, answering fluently wherever the problem itself can be put into words.
That is roughly where today's LLMs stand: they have compressed the sum of human explicit knowledge into their weights.

What true masters have beyond that rarely sits quietly inside language.

The story of Cook Ding carving an ox is familiar in China.
He says, "I encounter it with the spirit rather than look with my eyes. The senses stop, and the spirit moves as it will."
The more I read that line, the more exact it seems.
Once a skill becomes that deeply familiar, sight and explanation recede; the movement itself knows where to go.

Ask Cook Ding to write *A Manual for Carving Oxen*, and he could set down principles and share some lessons.
But the manual would not equal Cook Ding.
The essential part was in his hands, in the feel that grew from carving thousands of oxen over nineteen years.

Today's AI is like a near-master that has read every ox-carving manual in the world.
It can explain bovine anatomy and the mechanics of a blade, and it can repeat Cook Ding's own advice.

But when the blade meets the animal, it has neither those hands nor those nineteen years.

----

## 2. What Can Be Said, and What Can Only Be Done

This distinction is an ancient problem in epistemology.

The ancient Greeks distinguished between two kinds of knowledge.
**Episteme** is articulable and generalizable knowledge about *why*: science, mathematics, and logic.
**Metis** is knowledge that resists articulation, changes with context, and concerns *how to act*: craft, judgment, and improvisation.

Modern science leans toward the former.
We want important knowledge to be expressible, testable, and reproducible.
The AI industry inherited the same ideal: tokenize everything, lay everything out as steps, and preferably explain it all through chain of thought.

But Polanyi's sentence still stands in the way:

**"We can know more than we can tell."**

What we know far exceeds what we can put into words.

I wrote about this before in "Can Experts Be Distilled?"
Much of the time, explicit knowledge is merely the portion of tacit knowledge that survives being squeezed into language.
A vast body of understanding first lives in the body, intuition, and background experience.
Language scoops out a cupful and does its best to solidify it into rules, manuals, and SOPs.

So being able to explain something is not the same as truly understanding it.
Some forms of understanding are distorted by explanation.

The person who truly understands code is not necessarily the one who can annotate every line.
It is the one who glances at it and smells a bug.
Ask why, and they may have no immediate answer.
They have to stare at it a little longer, then slowly translate intuition into an explanation.

That is not a defect in their understanding.
Often, it is what understanding looks like after it has sunk to a deeper layer.

At this point, some readers will think of diffusion models.
Autoregressive models learn paths; diffusion models learn terrain.
An expert may look at a chessboard and simply feel that something is wrong, without running a complete chain of reasoning.
It is more as if the position has landed in a low-probability region of the distribution of plausible games.

I think the analogy holds.
But it describes tacit knowledge at the level of **perception**, where we have at least begun to glimpse a mathematical shape.

Cook Ding's skill goes beyond seeing.
It lives in movement, in the prediction that "if the blade moves this way, the tissue will part like that half a second from now."

That is tacit knowledge at the level of **action**.

And physiologically, action-level tacit knowledge leads us straight to the cerebellum.

----

## 3. What Does the Cerebellum Actually Compute?

Do not reduce the cerebellum to a "motor-coordination module."
That description is not wrong, but it is far too coarse.

I prefer an explanation familiar to engineers: the cerebellum runs a **forward model**.

When your brain wants your hand to pick up a glass of water, it first issues a motor command.
But tens to hundreds of milliseconds pass between sending the command, activating the muscles, and receiving sensory feedback about where the hand now is.

If every movement relied on a loop of "move a little, look, then adjust," humans would be unimaginably clumsy.
Feedback would always arrive half a beat late, and every movement would lag with it.

The cerebellum computes ahead.

Before the command has fully taken effect, it predicts: "If I issue this command, what will the hand, the glass, and the water's surface look like half a second from now?"
It uses that prediction to correct the movement in advance.
When real feedback arrives, it uses the discrepancy to calibrate the next prediction.

At a low level, this has something in common with an LLM predicting the next token.
Both are prediction machines, and both minimize the gap between prediction and reality.

The difference is equally clear.

An LLM's predictions are mostly open-loop.
It predicts a sentence, generates a token, and at most updates the representation in its context.
It does not physically act on the world and then receive the consequences back from that world.

The cerebellum predicts in a closed loop.
It predicts, acts, receives feedback from the world, and engraves that feedback into itself.

More important, the cerebellum's forward model is not a generic template.
It grows slowly around **this body, this environment, and this history**.

Your cerebellum encodes the length of your arm, the travel and rebound of the keyboard you use every day, the height of each step in your house, and the exact point where your car's clutch engages.

These things are hard to transfer.

Copying a concert pianist's cerebellar parameters wholesale into someone else would probably be meaningless.
Those parameters encode the coupling among these hands, this piano, and these decades—not an abstract document called *How to Play the Piano*.
Move them into another body, and many become invalid at once.

The word **non-transferable** will keep returning.

----

## 4. The Cerebellum Is Why You Are You

I am increasingly inclined to see the cerebellum as a hard substrate of individuality.

"Individuality" and "uniqueness" sound like airy philosophical terms.
Thinking about the cerebellum pulls them back into territory that engineers can discuss.

In computational terms, what is a particular person?

To a large extent, a person is a non-replicable set of forward models carved by that person's own history.

You are not you merely because of the knowledge stored in your brain.
Other people can learn that knowledge, you can look it up in books, and an LLM already contains more of it than you do.

You are you because your body has been shaped in a particular way by your experience.
The way you walk, the rhythm of your typing, the flicker of unease when you see a vaguely familiar failure—no one else can take those things from you or reproduce them in full.

The gap between a near-master and a master is therefore more than a matter of knowledge.

Near-masters work by combining declarative knowledge, which is exactly where LLMs excel.
What masters have beyond that is an individualized forward model engraved into the sensorimotor system.

That entire dimension is still largely empty in mainstream AI architectures.
Autoregressive or diffusion-based, regardless of parameter count, none of them yet has an organ like this.

----

## 5. Ten Thousand Hours Carve You, Not Knowledge

The "10,000-hour rule" is often reduced to motivational fluff: persist long enough and you can stuff enough material into your head.

I don't think the material is the point.

What ten thousand hours truly leaves behind is ten thousand hours of consequences.

A novice DBA can read every manual and end up knowing almost as much as an old hand.
What the novice lacks is feel.
That feel cannot be read from a book.
It grows in the body after countless hours watching dashboards and dozens of real production incidents.

After all my years working with databases, I know exactly how hard this is to write down.
Many judgments do not come from a specific rule.
They arrive more like a thought: "This smells wrong."
CPU, I/O, connection counts, latency, replication lag, and traffic combine in some particular way, and suddenly your stomach tightens.

Ask me for a postmortem afterward and, of course, I can explain it.
But in the instant when it matters, the feeling usually arrives before the explanation.

The most important variable here is **real consequences**.

Practice in a simulation produces something different from work in production.
The tension of a 3 a.m. page, the cold regret rising through your body after deleting production data by mistake, and the release after staying up all night to bring the system back—each leaves a deep mark on experience.

A world that can always be reset, where mistakes hurt no one, struggles to produce that kind of judgment no matter how long you practice in it.

Software engineering has always done something similar: it turns slow thought into fast execution.

Kahneman divided cognition into System 1 and System 2.
System 2 is slow, deliberate, and conscious; System 1 is fast, automatic, and unconscious.
Learning a skill resembles compiling System 2 into System 1.
A novice driver thinks through every step; with experience, braking and steering become reflexes.

I often used to say: **code is fossilized thought.**

When a programmer writes code, that is slow thought.
Once the code is compiled and deployed, it becomes deterministic, high-speed, automatic execution that no longer has to think.
Much of software engineering's history is the story of humanity crystallizing the products of System 2 into System 1.

What LLMs lack today is this channel of crystallization at the level of the individual.
They use the same reasoning machinery to answer "1 + 1" and to discuss a difficult philosophical problem.
They have no mechanism that says, "I have done this so many times that it has become my reflex."

Distillation, caching, and fine-tuning certainly exist, but they are mostly population-level optimizations.
Experience is pooled into a new version, then distributed to every copy.

The cerebellum does something else.
One instance's experience slowly becomes the shape of that particular instance.

That distinction matters.

----

## 6. Pearl's Wall

Engineers will naturally ask: if the cerebellum is carved by experience, why not simply expose models to more experience?
Add more data, richer environments, and larger models, and surely they will converge eventually.

Along one dimension, that road runs into Judea Pearl's ladder of causation.

Pearl divides causality into three levels:

The first is **association**: given X, how likely is Y?
This is observation.

The second is **intervention**: if I actively do X, what happens to Y?

The third is **counterfactuals**: if I had not done X, would Y still have happened?

The crucial problem lies on the second rung.
Without additional causal assumptions, an observational distribution alone cannot, in principle, uniquely determine an interventional distribution.

In plain English: watching the world for a lifetime does not mean you know what will happen when you reach in and change it.

Seeing and doing produce two different kinds of knowledge.

No matter how large it becomes, an LLM trained on a static corpus learns mostly from the first rung: correlations in the world and human descriptions of causation.
It may have read endless accounts of "how to carve an ox" or "how to troubleshoot a system," but it has never personally done X and then watched Y happen.

It encounters human records and retellings of interventions, not the interventions themselves.

So this is not merely a question of data volume.
Where the data comes from determines what kind of knowledge it contains.

If this were 2025, I might have stopped here: purely observational data hits a wall; truly master-level AI needs a body and must enter the world to intervene for itself.

But this is already 2026.

----

## 7. In 2026, the Wall Is Starting to Give

To be honest, the argument above rests on an assumption that has become shaky in 2026.

The assumption is that AI has only observational data.

We have all seen what changed this year.
Agentic RL, RLVR (reinforcement learning with verifiable rewards), and agent training at scale in verifiable environments are allowing models not merely to read outcomes, but to take actions, receive feedback, and update from it.

A coding agent changes a line in a sandbox, runs the tests, sees them fail, and adjusts its next move.
It is no longer merely "watching someone else do it."
It has done X, and Y happened.

That is interventional data.

The gap between "seeing" and "doing" in Pearl's ladder is being crossed on an industrial scale, beginning in the world of software.

Does that make the cerebellum argument obsolete?
After a few more years of practice in sandboxes, will models simply become masters on their own?

I don't think so.

Moving from observation to action is only the first step.
The harder problem lies beyond it.

----

## 8. The Argument Is Not Dead; It Splits into Three Parts

Looking back, the "cerebellum thesis" should never have been compressed into one sentence.
It contains at least three separate requirements.

First, a model needs interventional data.
It must be able to act and receive feedback that says, "I did X, and Y happened."

In 2026, that requirement is beginning to be met.
That is the year's biggest change.

Second, the environment for intervention must resemble the world we actually care about.
Causality in the sandbox must line up with causality in reality.

This is partly true in closed domains such as code, mathematics, and chess.
The rules are clear, rewards are verifiable, and mistakes are cheap.
But the physical world, medicine, live financial systems, and real database incidents are another matter.
Your DBA agent can become very strong in a sandbox, but no sandbox contains a real phone call at 3 a.m. or real customers waiting for service to recover after an operator mistake.

Third—and this is the point that interests me most—the experience of intervention must belong to a persistent individual.

Those ten thousand trials must accumulate in **this particular agent**, gradually changing its own style of judgment.
Otherwise, the experience is merely public training material.
It never becomes an individual history.

Large-scale agentic RL today still works mostly like this: thousands of instances explore in parallel; their experience is collected, pooled, averaged, and distilled into the next checkpoint; that checkpoint is then distributed to every copy.

This certainly works.
The model gets stronger.

But the experience belongs to the population, not to any particular instance.

No copy becomes an irreplaceable *it* because it has traveled an irreversible path of its own.
What the copies share is the same upgrade package, not separate lives in which each had to bear the consequences.

The cerebellum thesis has not been refuted by the advances of 2026.
It has simply been decomposed.

The boundary from "seeing" to "doing" is being crossed.
The boundary from "population experience" to "individual history" has barely moved.

That is where I would now place the real wall:

**Can an AI's experience become the history of one particular AI?**

----

## 9. No One Is in a Hurry to Hit That Wall

Suppose agentic RL races ahead over the next few years.
Models become extraordinarily capable in every verifiable domain, yet no one addresses individualization.
What will we get?

Probably an omniscient, amnesiac observer: infinitely copyable, with no embodied history.

It will reach superhuman near-mastery in every articulable domain.
Every copy will be equally excellent—and equally devoid of the feel of a particular person.
Delete one and start another; nothing of substance changes, because no copy has been shaped by irreversible experiences of its own.

That alone is a civilizational event.
I am not dismissing it.
Such systems are immensely attractive economically: consistent, controllable, copyable, and auditable, with more than enough power to reorganize most knowledge work.

But we should see their shape clearly.

The lack of urgency around individualization does not necessarily mean the wall is technically impassable.

A system that cannot be copied or rolled back, with every instance different from the next, is hard to sell.
How do you QA it?
If every instance differs, which one do you test?
How do you ship it at scale?
A unique history cannot be packaged as a standard product.

It is also a safety problem.
How do you align an agent that has been shaped by its own history, cannot be predicted completely, and cannot be fixed by simply deleting it and starting over?
How do you audit it?
How do you make it fail-safe?

The market will therefore gravitate naturally toward AI as a tool.
Tools are easy to deliver, control, and reproduce.
Capability and safety become entangled here: beyond the wall may lie true masters, but also systems that are truly difficult to control.

That makes the situation more subtle.

The wall may not merely be something "we have not crossed yet."
It may be something "we do not want to cross yet."

----

## Epilogue: Machines Still Have No Vessel for Your Ten Thousand Hours

After the long detour, we return to the number from the beginning.

Sixty billion.

That unassuming cerebellum beneath the back of the brain contains most of our neurons, yet it is not responsible for the kind of thinking that produces papers.
It slowly carves a body, an environment, and a history into a shape that cannot be replicated.

Cook Ding's nineteen years did more than teach him "the structure of an ox."
A veteran DBA's ten years did more than teach them "the database manuals."
What settled in was a feel, a rhythm, a sense of what would happen next, and a sense of responsibility—things even they could barely explain.

The strongest AI of 2026 has read humanity's manuals and is beginning to learn through trial and error of its own.
That is real progress.

But each trial still mostly flows into a shared pool and becomes a capability of the next model generation.
The model is getting stronger, but it is not becoming **a particular self**.

And the part that makes you **this particular you** is also humanity's oldest limitation.
Masters die.
Crafts disappear.
A lifetime of skill cannot be copied in full.
The uniqueness we cherish and the finitude we cannot escape are two sides of the same thing.

Machines have caught up with the explicit-knowledge half of intelligence.
That battle is already over.

What still belongs to humans is the ten thousand hours: the irreversible consequences, the fear at 3 a.m., the regret of deleting data, the relief after reviving a system, and everything history has carved into the body that even its owner cannot explain.

It is **this particular you**.

In the end, what AI lacks is not just compute.

It lacks a body—and the unrepeatable history, lived by that body, that belongs to it alone.
