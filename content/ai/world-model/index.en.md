---
title: "Getting the Name Right: What Is a World Model?"
date: 2026-07-13
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Starting from the roots of "world" and "model," this essay uses Pearl's ladder of causation to redefine world models: they must capture not just space and time, but agents, interventions, and counterfactuals.
tags: [AI, World Models, Causal Reasoning, JEPA]
ai: true
---

## 1. The Naming Mess

In 2025 and 2026, "world model" became perhaps the hottest—and loosest—label in AI.

The video camp says coherent video generation is a world model. The 3D camp says only spatial reconstruction qualifies. Roboticists say a model must be able to rehearse the consequences of actions internally.
[Fei-Fei Li wrote a long essay arguing that language was no longer enough](https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models), quoting Wittgenstein's famous line:
"The limits of my language mean the limits of my world."

A side note: that sentence comes from the 1921 *Tractatus Logico-Philosophicus*.
At the time, Wittgenstein believed that language had a precise logical structure and that every word corresponded to a determinate fact.
Three decades later, he dismantled that view himself. Put a pin in that thread; we will pick it up again at the end.

LeCun, rejecting the purely autoregressive path and betting on JEPA, has placed predictive internal representations under the same label.

What finally prompted me to write was [a wonderfully strange essay](https://mp.weixin.qq.com/s/wQv_7RzTC0t_vfG_JpK1RA).
It recast the competing world-model approaches as rival schools of Chinese mysticism, matching them one by one with great comic effect.
It ended with a question: "Master, how accurate are your predictions?"

That question points in the right direction, but it is not yet specific enough.
This essay is an attempt to make it specific.
To do that, we first need to take the term "world model" apart and ask what each word commits us to.

Four camps use one term for four different things.
When the same term can mean a video generator, a 3D scene, a physics engine, and a robot planner, it is not meaningless. The label has simply mixed core, interface, and capability into one stew.

At that point, instead of rushing to certify one approach as orthodox, it is better to do something more pedestrian: take the term apart.

What is a "world"? What is a "model"? What do the two words promise when joined together?

Confucius called this "the rectification of names": if the names are wrong, the argument cannot proceed.
Curiously, once you trace both words to their roots, you find that the ancients had already carved part of the answer into the language itself.

---

## 2. "World": Time, Boundaries, and the Person Inside

The Chinese word for world, **世界** (*shìjiè*), has a long history as a major Buddhist term and is closely tied to Chinese translations of the Sanskrit *loka-dhātu*.
To recover its original sense, we have to examine its two characters separately.

Once separated, the clues become clear.

> **世 (*shì*)—the *Shuowen Jiezi*: "Thirty years make one *shì*."**

The key point is that **世** is a unit of time, not space.
Thirty years make a *shì*; the succession of father and son makes a generation. Chinese words for "generation" and "hereditary" both grow from this root.
Buddhist thought glosses it as "ceaseless flow": only where there are past, present, and future, and states changing from one into another, is there **世**.

> **界 (*jiè*)—the *Shuowen Jiezi*: "A boundary. From field, with *jie* as the sound."**

**界** is built on the character for a field. Its original meaning is the boundary or edge of a plot of land.
It does not answer "How large is the universe?" It asks a much more practical question: which patch of ground, exactly, are you drawing a line around?

Together, the two characters give "world" two precise meanings.
**世 is time**: a world is not a frozen cross-section but a process that moves forward.
**界 is boundary**: a world need not contain everything, but it must say where its boundary lies.

This is far more useful than treating "world" as a synonym for "universe."
A Go board is the world of a Go program. The road is the world of a self-driving car. The operating table is the world of a surgical robot.
Whether it is raining outside does not matter to a Go program.
For a self-driving car, the road surface, traffic, pedestrians, red lights, and even whatever the driver next to you is planning may all fall inside the boundary.
A world does not become truer by becoming larger. Draw the boundary too narrowly and you omit variables that decide success or failure; draw it too broadly and you waste finite compute on irrelevant detail.

Chinese has now given the world a skeleton: time as the warp, space as the weft.
But one thing is still missing, and English supplies it.

The English word *world* comes from Old English *weorold*, which can be traced to two older roots: **wer + eld**.

*Eld* is straightforward: age or era, cognate with *old*.
The crucial root is *wer*, meaning **man**.
You have seen it elsewhere: *werewolf* is *wer* (man) + *wolf*.

The literal root sense of *world*, then, is **the age of man**: the human age, the realm of human life.
In Old English it often referred less to the planet than to a person's lifetime, the human condition, or this earthly life as opposed to the next life or heaven.
That is why English has *this world and the next*, and why it has *worldly*: the word carries human life in its bones.
When we speak of "a child's world," "the business world," or "a game world," we never mean the universe.
We mean the small patch of reality that someone inhabits, can perceive and change, and whose consequences they must bear.

Chinese and English thus provide one half of the answer each:

**The Chinese 世界 is objective space-time: 世 is the warp and 界 the weft, whether or not anyone is inside.**
**The English *world* is the subjective human realm: *wer* is embedded in the root, and without that person there is no world.**

Two civilizations named the same concept. One caught the skeleton; the other, the breath inside it.

Turn next to Latin, and the ancients reveal a third understanding of "world"—the deepest one.

The Latin word for world is **mundus**, the ancestor of French *monde* and Spanish *mundo*.
But *mundus* began not as a noun but as an adjective meaning **clean, neat, orderly**.
(It is also an ancestor of English *mundane*; its opposite, *immundus*, meant "unclean.")
How did it become "world"?

It was a translation of the Greek **kosmos**, whose original meaning was **order, harmony, beauty**.
English *cosmetics* and *cosmos* share this root.
Why did the Greeks call the universe *kosmos*?
They looked up and saw the orderly motion of the stars, beautiful as something deliberately composed.
When the Romans translated the concept, they chose the Latin word that carried the same double sense of order and cleanliness: *mundus*.

The third meaning of "world" now comes into view, one that neither Chinese nor English states outright:

**A world is not a random pile of things, but an ordered, regular, and therefore intelligible whole.**

This sounds ordinary, but it is the foundation of the entire argument.
Something utterly chaotic and lawless—white noise—does not deserve to be called a world. You can say nothing about it and do nothing with it.
A world is a world only because it has order.
And because it has order, something can capture, compress, and reproduce it. That something is a model.

---

## 3. "Model": Negative Space and a Measuring Stick

Having taken apart "world," let us do the same to the Chinese word for model, **模型** (*móxíng*).
The fit between the two turns out to be exact.

> **型 (*xíng*)—the *Shuowen Jiezi*: "The method for casting a vessel. From earth, with *xing* as the sound."**

**型** is a casting mold: the hollow cavity into which molten bronze is poured.
It is **negative space**. By excluding every other shape, the cavity makes the bronze take the one shape you want.

The first meaning of **型**, then, is **constraint**.
A system that permits every result and can rationalize every observation after the fact is not a powerful model. It is a model that carries no information.
A model's dignity begins with its willingness to say what can happen and what cannot.

> **模 (*mó*)—the *Shuowen Jiezi*: "A rule. From wood, with *mo* as the sound."**

**模** is not merely one physical mold. Its meaning extends to a standard, exemplar, or rule that can be followed—the root behind the Chinese words for pattern, paradigm, and role model.
The purpose of a mold is not to remember one bronze object already cast. It is to **reproduce the same class of shape again and again**.

The meaning of **模**, then, is **reusable regularity**.
A model cannot merely memorize "what happened this time." It must extract "how things of this kind usually happen," compressing individual experience into a rule that can be transferred, replayed, and extrapolated to unseen cases.

The English word *model* adds a third meaning.
Through Latin **modulus**—a small measure or scale—it traces back to **modus**: manner, measure, proportion.
This root reminds us of something Chinese easily leaves implicit: **a model is never the original thing itself.**

The map is not the territory. A scale model is not the mountain range, and a weather model is not the sky.
A model is necessarily lossy. It must discard most details and preserve only the distinctions relevant to the task at hand.
The real question is never whether information was lost. It is whether the lost information changes the outcome we care about.

Three layers of meaning, three rules: **型 is constraint, 模 is regularity, and *modus* is scale.**
Weld them to "world," and a world model stops being the childish ambition of stuffing the entire universe into a chip.
It becomes a much calmer proposition:

> **A world model is an executable, lossy compression of a bounded, evolving process.**

More concretely, it does three things.
First, it compresses a jumble of observations into an internal state. That state might consist of pixels, a 3D point cloud, physical variables, or a sequence of latent vectors no human can interpret. Its form does not matter.
Second, it knows how that state moves forward: given the current state and an action, it can infer the next state.
Third, it can project its internal state into the output you need: an image frame, a coordinate, or the result of a collision.

A world model is therefore neither a miniature picture of the world nor a database full of facts.
It is more like **a state machine you can step forward**. Advance it one tick and the world continues; change the action and it branches down another path.

The question "What would happen under a different action?" is exactly what separates it from a beautiful image or a convincing video.
Judea Pearl spent a lifetime measuring that dividing line.

---

## 4. Pearl's Ladder of Causation: What Can a Model Answer?

[Pearl divides causal reasoning into three levels](/en/ai/cerebellum/#6-pearls-wall). The same distinction helps us judge what questions a world model can answer.

**Rung one: association, or "seeing."** `P(Y|X)`
When I observe X, how does the probability of Y change?
If the road is wet, is skidding more likely? When brake lights come on, does the car usually slow down?
Association can summarize data extremely well without knowing what caused what.

**Rung two: intervention, or "doing."** `P(Y|do(X=x))`
If I actively set X to a value, what happens to Y?
Seeing brake lights come on and a car slow down is association. Stomping on the brake myself and predicting how the car slows is intervention.

Game engineers wrote this distinction into code long ago.
Classic real-time strategy games synchronized multiple machines through deterministic lockstep: the network mostly transmitted player commands, not the complete state of every unit at every moment.
As long as every machine began with the same initial state, executed the same commands in the same order, and applied the same rules, each would produce exactly the same world.
That is how *Age of Empires* synchronized more than a thousand units over dial-up connections.
Notice what this architecture implies: in the state-transition function, actions stand alongside the laws of nature.
An action is not a label pasted onto a generated frame afterward. It directly participates in the state transition.
The engineers of 1997 may not have read Pearl, but their code stood on the second rung.

**Rung three: counterfactuals, or "imagining."**
The event has already happened. Given that exact scene and event, what would have happened if I had acted differently?
This is regret, "if only," and "I could have."

These are not three unrelated kinds of model. They mark how far a model's answers can reach.
Predicting the next step from history is already useful.
Comparing the consequences of different actions is what directly supports planning.
Answering "What if..." about an event that already occurred demands still more.
A model need not reach the third rung to count as a world model, but its rung determines what it can be used for.

In practice, two distinctions are especially easy to blur.

**First, including actions in the input does not mean the model understands intervention.**
Putting "left" and "right" tokens into the input proves only that the model accepts action conditioning.
If "left" always appears in the training data alongside a certain kind of scene or driving policy, the model may simply memorize the pairing rather than learn how turning left changes the subsequent state.
To show that it truly understands the action's effect, change the scene, the operator, or the action distribution, then test whether it still predicts the consequence of the same action correctly.
Otherwise, it has learned a correlation in the data, not a reusable state-transition rule.

**Second, generating a different video does not amount to counterfactual reasoning.**
A counterfactual asks: for this event that already happened, what if we changed only one action?
The model must therefore hold the scene, people, and other background conditions as fixed as possible, replace only the action in question, and roll out the new result.
If it merely starts from a similar state and generates another plausible-looking video, that is a different possible sample—not a counterfactual answer about this event.

Both distinctions reduce to the same standard: the model must make testable predictions in advance—predictions that can fail.
That is the real technical version of "Master, how accurate are your predictions?"
The problem with fortune-telling is not that it lacks a story.
It is that almost any outcome can be explained after the fact, leaving almost no explicit condition for failure.
A technical model is the opposite: a wrong prediction is wrong. You cannot rescue it by wrapping every outcome in another explanation.
A system that can never be wrong is not a technical model. It is a belief system.

---

## 5. The Spectrum of State: Five Schools, Five Mystic Arts

From this height on Pearl's ladder, we can look back over the battlefield below.

At least five banners now fly under the name "world model."
Some build worlds from pixels. Some use 3D geometry. Some compress the world into vectors no human can read. Some write down the physics directly. And some claim they can calculate how the world will change when "I" act.
The argument is lively, but most of the fire is aimed at representation: the pixel camp mocks the geometry camp's expensive data; the geometry camp points to objects clipping through one another in pixel models; the latent-space camp laughs at both for wasting compute on representations meant for human eyes.

The essay mentioned at the beginning translated this argument into a contest among Chinese mystic arts:
pixel readers practice physiognomy; geometry surveyors, feng shui; latent-vector readers, divination; causal modelers, the Five Elements; intervention planners, Qimen Dunjia.
It works as a joke, but on closer inspection it makes an abstract distinction tangible.
The joke runs on a serious insight worth stating plainly:

**Observation is not state.**

All you can ever obtain directly is an observation: a video, a photograph, a sensor reading, or the birth date and hour of the person whose fortune is being told.
What the model carries inside is a state.
The level at which that state is defined is the first fork among these approaches—and the sharpest measuring stick in the original essay:

**The shallower the state and the closer it is to observation, the cheaper the data, the faster the validation loop, and the lower the ceiling.**
**The deeper the state and the closer it is to the causal mechanism, the farther it lies from observation, the scarcer the data, and the harder the validation—but the stronger the generalization and the higher the ceiling.**

In terms of the characters we examined earlier, this is a question of **界**, the boundary:
do you draw the boundary of the model's internal world around appearances, or around mechanisms?

**The physiognomy school: a world of pixels.**
The state is every pixel in a frame.
Data is easiest to obtain: internet video, movies, television, and surveillance footage are all ready-made feedstock.
The validation loop is fastest: a person can tell at a glance whether the generated clip looks right.
The promise is also the shallowest: if it looks right, it is right.
This school stands on the first rung and models association. After seeing enough examples of "this frame," it can continue with "the next frame."
But when a cotton ball hits an iron ball, it owes you no physically correct result.
No wonder the original essay joked that AI microdramas excel at cultivation fantasy: those worlds never obeyed physics in the first place.

**The feng shui school: a world of geometry.**
The state is lifted into three dimensions: position, shape, and surface structure, represented as point clouds or Gaussian splats.
The data becomes an order of magnitude more expensive. You need multiple views, lidar, and depth cameras; random internet video will no longer do.
The validation loop gains a real ruler: by how many millimeters do the reconstructed coordinates miss the ground truth?
Yet the model still answers "What would it look like from another angle?" Reconstruction and extrapolation remain on the first rung.
A feng shui master can read form and layout, but cannot explain the forces at work. Geometric consistency is not physical correctness.
The approach finds practical use in digital twins, AR navigation, and scene understanding for autonomous driving.

**The divination school: a world of latent space.**
LeCun's JEPA takes the most uncompromising route: the state is a sequence of high-dimensional vectors with no physical meaning and no obligation to be human-readable.
Why should a machine have to translate its understanding of the world into human language?
Watching a basketball game, it keeps "player number three is beyond the three-point line" and "where the ball is going," while discarding the sweat, shoe tread, and spectators.
It then predicts inside that compressed space.

Game engines have been doing something similar for thirty years: do not render what is off-camera, reduce detail in the distance, and stop calculating physics for things that remain still for long enough.
**Discarding irrelevant detail is compression. Discarding information that changes the result is model error.**

The divination school's real problem is validation.
Using an error measured in latent space to validate a prediction made in latent space is like using a ruler to prove that the same ruler is accurate.
The original essay put it this way: the diviner says, "You have to use my divination to tell whether my divination was right."
The symbols need not be readable by humans, but their accuracy cannot be certified by the symbols themselves.
An external validation loop must redeem them: a downstream task, robot control, or an actual collision in the physical world.

**The Five Elements school: a world of physical causality.**
The state consists of mass, velocity, coefficients of friction, elastic moduli, and the causal structure among those variables.
It does not remember what something looks like, only why it moves as it does.
Its data is the most expensive: either high-precision sensors in the real world or a simulation engine.
Between simulation and reality lies the stubborn sim-to-real gap.

But this school has the strongest validation loop of all: physical correctness can be tested, and **verification is far easier than prediction**.
Judging whether objects interpenetrated during one collision is an order of magnitude easier than predicting the collision in full, which makes the reward signal unusually clean.
It also genuinely reaches the second rung. Actions appear in the dynamics; push an object and the world actually changes.

It is used in industrial robots, surgical robots, and edge cases in autonomous driving—places where one interpenetration means a defective part and one wrong collision means an accident.
Precisely because the cost is real, it is the least tolerant of error.
A platform game may let a character steer in midair, and a racing game may quietly increase tire grip. That is fake physics in service of playability; internal consistency inside the game is enough.
A robot simulator cannot bluff. Its physics must survive the trip out of simulation and live in reality.
**The use determines which errors are tolerable and which are fatal.**

**The Qimen school: a world of causal intervention.**
Here we need to pause: the fifth approach does not inhabit the same dimension as the first four.
The first four disagree about state representation—pixels, geometry, latent vectors, or physical quantities.
The Qimen school sets a capability requirement. It asks not only "What will happen?" but also "What should I do, and when, to make the outcome I want happen?"

**It is not a new representation. It is a requirement placed on the model's capabilities.**
A pixel, geometry, or latent-space model might merely extrapolate the future from history, or it might go further and compare the consequences of different actions.
What matters is not what the internal state looks like. What matters is whether actions genuinely participate in state transitions and whether the model has been trained and tested accordingly.
This is the climb up Pearl's ladder: from association to intervention to counterfactuals.

The map of schools therefore has two axes.
**The horizontal axis is depth of representation**: whether state is defined at the level of appearance or mechanism.
It determines the cost curve—where the data comes from, how fast the validation loop closes, and how much one iteration costs.
**The vertical axis is capability**: which rung of Pearl's ladder its answers can reach.
It determines the ceiling—whether the model can only continue history or can weigh the consequences of an untried action.
Most of the crossfire runs along the horizontal axis. The vertical axis is what ultimately separates their capabilities.

Measured against these axes, physiognomy and feng shui stand on the first rung.
Divination aspires to lay the foundation for the second, but its validation often remains on the first.
The Five Elements reaches the second. Qimen aims squarely at the second and third.
Whatever banner a system flies, it has to earn its position on the vertical axis through training and testing, not assertion.

The vertical axis also requires us to distinguish three things: the world model, the objective function, and the planner.
The world model answers, "What happens if I take this action?"
The objective function decides, "Which outcome is better?"
The planner uses both to choose, "What should I do now?"
The three often appear together in one system, but they are not the same thing.
Even with an accurate world model, the system can choose the wrong action if its objective is wrong or its planning is inadequate.
**A world model supplies the consequences of action, not the purpose of action.**

When evaluating a system, then, it is more useful to ask three questions than to argue about its school:
How does it represent the current state? How does it predict state changes? How do actions enter the model?
Once those answers are explicit, what the system has actually achieved becomes clear.

The original essay ended with a line from Patriarch Subhuti: "Within the Way are 360 side paths, and every side path can bear true fruit."
Then it unearthed a marginal note: "The key to the mystery is not found among the 3,600 gates."
Every side path can bear true fruit. Each of the five approaches can succeed for its intended use, provided its validation loop closes and its errors are judged against a clear purpose.
But the key does not lie in the school. It lies on these two axes: **where the state is defined, and how high the questions reach.**

---

## 6. After Getting the Name Right

After this long circuit, we can now offer a definition that is less dazzling but better able to survive scrutiny:

> **A world model is an internal model of an environment for a particular agent and task.**
> **It compresses a history of observations into task-relevant state and predicts how that state changes.**
> **More capable models can also compare the consequences of different actions and answer interventional and counterfactual questions.**

It need not contain the whole universe, use variables that humans can read directly, or predict a single future exactly.
Real environments may be stochastic and only partially observable.
They may also contain other agents with goals of their own.

**The world may have no purpose. A model always has a use.**
Whom the model serves and what problem it is meant to solve directly determine what it preserves, what it ignores, and how it should be tested.
What matters is not how much the model contains, but whether it can state its boundary, use, and degree of reliability.

Following the path we have taken—Chinese space-time, the person embedded in English, the order embedded in Latin, the model's constraints and scale, Pearl's three levels, and the two axes behind the five approaches—the promise of a world model reduces to six questions:

**世 — time:** Over what time horizon can it model change?

**界 — boundary:** What part of reality does it cover? Is state defined at the level of appearance or mechanism? How do influences from outside the boundary enter?

**人 — agent:** Which agent does it serve? Which actions can genuinely change the internal state?

**模 — regularity:** What reusable regularities has it extracted? Are they statistical associations or causal mechanisms?

**型 — constraint:** Which states and transitions does it rule out as impossible?

**度 — scale:** At what scale is it valid? How is error measured, and what counts as failure?

Only after answering these six questions does "world model" cease to be a broad label and become a set of testable technical claims.

This also explains why two apparently opposite judgments can both be true.
It is inaccurate to say that the term "world model" has no definition and is pure hype.
It has a clear core: construct an internal model of environmental state and change so that prediction can serve action.
It is equally inaccurate to say that "the definition of world model is fully settled and there is nothing left to debate."
State can be defined at different levels, and capability can stop on different rungs.
The core is clear; the boundary is broad.

So "Master, how accurate are your predictions?" is not wrong. It is merely underspecified.
A more complete question would be:

> **Master, whose world are you predicting? Where is its boundary? Which actions can you handle, and how far ahead can you see?**
> **Are you answering association, intervention, or counterfactual questions? How is error measured, and what counts as failure?**
> **And under what conditions are you willing to admit that your prediction was wrong?**

A good world model does not try to stuff the entire world into a chip.
Its job is to let an agent rehearse a step in a constrained, testable internal world before paying the cost in reality—and, if the step is wrong, to roll back and try again.
**Reality has no rollback. That is precisely why we need an internal world.**

First, rectify the name.
Only then can we ask whose predictions are actually right.
