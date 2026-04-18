---
title: "Can You Distill an Expert?"
date: 2026-04-08
author: vonng
summary: >
  Polanyi's tacit knowledge explains the 70% ceiling of AI agents: real intuition, feel, and judgment do not serialize cleanly. They grow, if at all, through practice.
tags: [AI]
ai: true
aliases: ["/en/misc/tacit-knowledge/"]
---

> Polanyi's tacit knowledge explains the 70% ceiling of AI agents: real intuition, feel, and judgment do not serialize cleanly. They grow, if at all, through practice.

## 1. Distilling Employees

A popular idea lately is to "distill" employee knowledge into AI.

The playbook is always similar. Ask senior staff to write SOPs, organize troubleshooting manuals, and turn years of experience into documents. Then feed that material into an agent as context and try to clone the person's capability.

It sounds compelling. One human can babysit one system 24/7. AI can watch ten thousand at once. Distill one expert into an agent, and you have copied that expert ten thousand times.

A lot of companies are already doing exactly this. DBA agents, ops agents, support agents, legal agents, everywhere. I am building a DBA agent myself.

But there is an uncomfortable fact here: **this path has a very hard ceiling, and most people have not hit it yet.**


----

## 2. The 70% Ceiling

I am my own example.

I have spent ten years on PostgreSQL. In the PG DBA niche, I have more or less reached the top of what one person can do. A lot of what I know can absolutely be written down: how to tune parameters, build indexes, design HA, do backup and recovery. That knowledge can be made explicit. Once it becomes SOPs, AI can use it. My open-source PG distribution Pigsty is itself a form of distillation: expert experience frozen into code and configuration.

But I can say this very honestly: **what I can write down is maybe 70% of what I can actually do.**

What is the other 30%?

It is the feeling that something is off after one glance at a Grafana dashboard. It is picking the "right" option when two plans both sound plausible, then being unable to explain the choice except by saying "intuition." It is facing a production failure I have never seen before, with no documentation covering it, and still being able to assemble a new path out of fragments of past experience.

I cannot write those things down. Not because I do not want to. They do not exist in a form that can be written down. I hit this constantly while writing SOPs: I get to a step where I know that in real life I would make a judgment call based on how the situation feels, but that judgment cannot be turned into a rule. All I can write is "use judgment based on actual conditions." That stock phrase is just the missing 30% hiding in plain sight.

If a junior engineer reads "use judgment based on actual conditions," they just freeze. Because the ability to make that judgment is not in the document.


----

## 3. Polanyi Already Explained This

I was not the first person to notice this. Someone explained it cleanly more than sixty years ago.

In 1958, the British scholar Michael Polanyi wrote a line in *Personal Knowledge*:

**"We can know more than we can tell."**

We know far more than we can say.

Polanyi was not an armchair philosopher. He was first a serious scientist, a physical chemist. He spent thirteen years at the Kaiser Wilhelm Institute in Berlin, published more than two hundred papers, and helped lay the foundation for potential energy surface theory. In 1948 he gave up his chair in physical chemistry for a chair in social studies and moved into philosophy full-time, because scientific practice had taught him that the most important knowledge is exactly the part formal methods cannot capture.

He spent the rest of his life building the theory. The core has three layers:

**First: background and focus.** Every act of knowing has a two-layer structure. When you hammer a nail, your attention is on the nail itself, the focus, while the sensation in your palm stays in the background. When you drive, your attention is on the road, while your grip on the wheel and pressure on the pedals stay in the background. The key point is that this structure is not reversible. If you shift your attention from the nail to the exact motion of your hand, you immediately stop hammering well. If an experienced driver starts consciously monitoring how their foot presses the brake, they are more likely to get it wrong. **Some knowledge only works when it stays in the background. The moment you drag it into focal attention and inspect it directly, it stops working.**

**Second: indwelling.** A blind person using a cane is not conscious of the handle but of the ground ahead. The cane has become an extension of the body. The person has, in Polanyi's term, "dwelt in" the cane. The same is true for an experienced driver and a car, a veteran chef and a kitchen, a programmer and an editor. If you take someone who has used Vim for ten years and force them into another editor, you are not just swapping tools. You are cutting off part of how they think. Between expert and tool, or expert and environment, the relationship is not "use." It is fusion.

**Third: knowledge is never fully formalizable.** This is not just a temporary communication problem. Polanyi's claim is stronger: tacit knowledge is the foundation under all knowledge. You can write a skill into a manual, but the reader needs fresh tacit knowledge in order to understand the manual. Externalize one layer and there is another layer underneath it. Like peeling an onion, you never reach a skinless core.

After Polanyi, the Japanese management scholar Ikujiro Nonaka simplified this into the SECI model, which assumes tacit knowledge can be "externalized" into explicit knowledge. That simplified version became extremely popular and is how tacit knowledge spread through much of the Chinese-speaking management world. But it also blunted Polanyi's sharpest insight. Today's talk about "distilling employees" is basically the AI-era reboot of SECI. It rests on the same assumption: if you use the right method, tacit knowledge can be made explicit.

Polanyi's answer would be: **no. You think you are distilling knowledge. In reality you are distilling a by-product of knowledge.**


----

## 4. A Recipe Is Not the Chef's Feel

Here is a deep-learning analogy.

An expert brain is a neural network trained for ten years. Asking that expert to write SOPs is like asking the network to export a batch of reasoning traces. Those traces do reflect part of the network's capability, but they are not the network itself.

Then you take those traces and stuff them into an agent as prompts.

**The expert's output becomes the agent's input. You are already one layer removed.**

Many models today are trained on Claude outputs. But none of them actually reaches Claude's level.

What you get is the chef's recipe, not the chef. The recipe says "stir-fry on medium heat for two minutes," but the chef does not look at a timer. The chef hears the oil and knows whether the temperature is right. The chef feels the wok and knows when to pull it off the fire.
Those things do not fit in a recipe, because "medium heat" is different on every stove, with every pan, with every ingredient.

A recipe can help a beginner make a passable dish. But reading recipes without cooking never turns you into a great chef, because the chef's real ability is not in the recipe. It is in the feel.

What is that feel? It is the weights. It is the neural circuitry hammered into shape by ten years of cooking. It determines **how** the chef thinks, not just **what** the chef thinks about.
You can give AI more and more recipes, more SOPs, but that changes what it thinks about, not how it thinks.

**That is the essence of the 70% ceiling: SOPs encode reasoning traces, but expert intuition lives in the weights. You cannot distill the weights.**


----

## 5. The Wetware Feel

So what is that last 30%, and where does it come from?

In computer culture, alongside hardware and software, the human brain and body are sometimes called **wetware**: carbon-based, water-filled, living computation. I call that last 30% of expert judgment **wetware feel**.

Hardware and software can be copied and serialized. Wetware has one crucial difference: **computation and storage are inseparable.** In the von Neumann architecture, CPU and memory are separate. In the brain, neurons are both compute units and storage units. The knowledge structure shapes perception, and perception reshapes the knowledge structure. Every act of use modifies the substrate itself.

And "feel" is not just a metaphor. Damasio's somatic marker hypothesis argues that when the brain makes decisions, it reactivates bodily states from similar past situations: heart rate, muscle tension, visceral sensation. Those signals let it collapse the decision space quickly. High-level expert judgment really does operate through bodily feeling: a tight chest, a sense that something is wrong, discomfort without a clean verbal reason.

An experienced pilot feels whether turbulence is routine or whether the plane needs to climb. A veteran driver feels how much throttle a turn can take. A veteran chef knows whether the seasoning is right from the feel in the hand while tossing the pan. A traditional physician feels whether a pulse is slippery or rough under three fingers. This is not formal reasoning. It is the body replaying patterns from countless similar situations in the past.

The Dreyfus model of skill acquisition sharpens the point further. Classical expert systems depended on "knowledge engineers" extracting rules from domain experts and encoding them explicitly. But the Dreyfus argument is that experts are experts precisely because their core ability has already been absorbed into bodily, situational, tacit knowledge. In plain English, expert performance is embodied intuition.

How does that feel grow? Four conditions are all required:

**Time.** Not ten thousand hours of reading, but ten thousand hours of exposure in real environments.

**Consequence.** Mistakes must have real consequences. Without real stakes, no emotional marker is formed and no pattern gets carved into the body.

**Attribution.** After a decision, you need to see the result quickly and know that it came from your own choice.

**Variation.** Similar problems must keep appearing in different forms, forcing the body to grow flexibility instead of memorizing one answer.

Put together, this is not information input, storage, and retrieval. It is **neural circuitry being repeatedly carved under the pressure of real consequences**.

This used to have a simple name: **apprenticeship**. A master did not just hand the apprentice an SOP. The apprentice followed along in real environments, touched the work, watched closely, and learned through embodied trial and error. You can read forever without ever developing feel. Feel only grows in contact with reality.

Polanyi made that point sixty years ago.


----

## 6. The Ceiling of AI Agents

Now point this framework at AI agents.

Every current agent framework, no matter how it is packaged, is doing work on the same layer: the **Harness** layer. System prompts, tool definitions, RAG knowledge bases, SOP decision trees, few-shot examples. All of it is explicit and serializable. In Polanyi's language, all of it is focal knowledge. All of it is reasoning traces.

The Harness layer can absolutely reach a useful level. If a top expert manages to encode 70% of their capability, the agent can perform like a solid mid-level practitioner in most routine scenarios. That already has major commercial value, because a large share of day-to-day work really is repetitive and rule-like.

**But the ceiling is there.**

That expert intuition, the part no SOP can fully state and only real situations reveal, does not live in the Harness layer. It lives in the weights. And current agent architectures do not touch weights. During inference, the LLM is read-only. No matter how rich the context is, not a single parameter changes.

That means: **current agents can remember a past mistake in context, but they do not thereby become the kind of agent that no longer makes that mistake.** Remembering a lesson is a data-layer operation. Growing intuition is a weight-layer change.

An agent can simulate the diligent mid-level engineer who follows the playbook. It cannot yet simulate expert intuition.


----

## 7. Give the Agent a Body

So what do we do? My answer is two steps.

**Step one: give the agent an environment it can "dwell in."**

Polanyi's point was that knowledge must be indwelt in an environment. In engineering terms, that means an agent cannot just have a brain, the LLM. It also needs a persistent, stateful environment with real consequences. Call that [**Runtime**](/en/db/agent-moat/), the agent's body.

For the DBA agent I am building, Pigsty is that Runtime. Pigsty is the environment it dwells in. The monitoring system is its eyes. CLI tools are its hands and feet. It runs continuously inside that environment. Every action has real consequences, and those consequences get recorded and affect later decisions. That is apprenticeship. That is practice accumulating into feel.

An agent that has run for a year and a newly deployed agent on the same model can differ enormously in capability. Not because the model changed, but because the first agent accumulated experience in the Runtime: operational history, failure records, memory of this particular system's temperament.

**Step two: let that feel sediment back into the weights.**

Runtime alone is not enough. You can log practical experience and feed it back into prompts, raising the Harness ceiling from 70% toward 80% or maybe even 90% in some domains. But real expert intuition, the kind that knows what to do without checking notes, probably requires weight updates in the end. The experience an agent accumulates cannot live only in context. It has to flow back into the parameters and change how the model thinks.

That is the fundamental gap in current AI architecture. During inference, LLM weights do not change. Today's action does not make tomorrow's model better. Biological brains, by contrast, are constantly reshaping synaptic connections, especially during sleep. Maybe the future is some form of continual learning: work during the day, accumulate experience, then do periodic incremental fine-tuning at night.

But even then, the separation of compute and storage in the von Neumann model remains a deep bottleneck. A system where every act of use truly changes the self may need a new hardware paradigm. That might also become the real killer use case for local inference: models that grow wetware feel inside real environments and diverge person by person.

That part is still ahead of us. The direction, though, is clear.


----

## 8. Intelligence Can Be Downloaded, Feel Can Only Grow

Back to the original question: can an expert be distilled?

Yes. But only to about 70%.

That 70% is SOPs, documents, and rules. It can be fed to AI, and the payoff is immediate. A mid-to-high-level agent can handle a large amount of repetitive work, and the effort required to build that is absolutely worth it.

But the remaining 30%, expert intuition, practiced feel, the judgment that is real even when it cannot be explained, **cannot be distilled.** Polanyi explained why sixty years ago. It is not information but structure. Not reasoning traces but weights. Not something you merely have, but something you become.

For humans, the part of you that is hardest to replace is not what you know. It is the judge you have become after repeated contact with real consequences. Your moat is not just in your head. It is in your body. AI can copy everything you write down. It cannot copy you.

For agents, a brain and a knowledge base are not enough. They also need a body, Runtime, and a growth path, weight updates. The Harness layer may get you to 70%. Runtime experience may get you to 85%. But getting close to expert level means touching the weight layer, and that is exactly what current architectures are missing.

Polanyi spent his life arguing for one idea: knowledge is not a thing. It is a relationship, a living, dynamic coupling between the knower and the world. Once you pull it out of that relationship and turn it into an object for transmission, it is no longer the same thing.

**Intelligence can be downloaded. Feel can only grow.**

A truth stated sixty years ago by a scientist who walked away from the lab is still one of the few firm anchors in the AI age.

---

*References*

- *Michael Polanyi, Personal Knowledge, 1958*
- *Michael Polanyi, The Tacit Dimension, 1966*
- *Antonio Damasio, Descartes' Error, 1994*
- *Ikujiro Nonaka, The Knowledge-Creating Company, 1995*
