---
title: "On Computational Thinking"
date: 2014-05-11
author: vonng
summary: A paper for "History of Secrecy and Secrecy Systems" course, discussing computational thinking and its significance in undergraduate education, as well as methods for cultivating computational thinking among undergraduates.
math: true
---

{{< katex >}}

A paper for "History of Secrecy and Secrecy Systems" course, discussing computational thinking and its significance in undergraduate education. I guess this was the teacher's own assignment.

## 1. Abstract

This paper discusses related content on computational thinking. As required by the assignment, content related to undergraduate education has been specially added.

## 2. Introduction

Every discipline has its core ideas. In mathematics, axiomatic mathematical thinking is central; in engineering, approximation-based engineering thinking is the golden rule; in law, thinking about rights and obligations runs throughout; in economics, there is the concept of rational person as a basic assumption. In the learning process of a discipline, compared to the accumulation of knowledge, more important is the cultivation of this kind of thinking. The thinking of a discipline contains the worldview and methodology of the entire discipline's theoretical system, is a highly condensed and summarized experience of the entire discipline's research, and can truly be called the essence.

So what can we say about computer science? This paper aims to explain the thinking of computational science, namely computational thinking. Its origin, significance, and methods for cultivating computational thinking among undergraduates.

## 3. Origin of Computational Thinking

A very uninteresting thing is that almost every article discussing computational thinking tirelessly repeats Professor Zhou Yizhen's definition at the beginning. Therefore, I hope to explain this concept in a different way: starting from the origin of a concept. Explaining this question: What is computational thinking.

Computer science is essentially applied mathematics; it is a hybrid of mathematics and engineering. On one hand, it has the abstraction, rigor, and precision of mathematics; on the other hand, it widely applies approximation methods from engineering. Computer science inherits many characteristics of both. Its core ideas are also the essence of both. We can say:

Computational thinking = Mathematical thinking ∩ Engineering thinking.

Computational thinking is a subset of mathematical thinking; it is a subset obtained by adding practical constraints to mathematical thinking.

Then, we can begin to understand computational thinking. First, we study its connection with mathematical thinking.

Mathematical thinking belongs to the comprehensive thinking form of epistemology, empiricism, and methodology. Its greatest cognitive characteristic is: conceptualization, abstraction, and modeling. A person with mathematical thinking often has the following characteristics: when discussing problems, habitually emphasizes definitions, defines concepts, and clarifies problem conditions; when observing problems, habitually grasps the (functional) relationships within them, constructing comprehensive multi-factor macroscopic considerations based on microscopic understanding; when understanding problems, habitually generalizes existing rigorous mathematical concepts and applies them to the cognitive process of real-world problems. Applying mathematical ideas to practice, establishing isomorphism between mathematical concepts, mathematical models and things in the real world, using mathematical methodology to understand and process objective things. This is mathematical thinking.

We easily find that if we replace the word "mathematical" with "computational" in the above paragraph, it reads without any impropriety. This fully demonstrates the inheritance between computational thinking and mathematical thinking. In fact, the so-called concept of computational thinking, rather than saying it was proposed with the development of computer technology, it's better to say it appeared with the prosperity of applied mathematics.

The prerequisite for cultivating computational thinking is cultivating mathematical thinking. The core of mathematical thinking is axiomatization. Axiomatization can be understood as formalization + axioms. The content studied by mathematics is already determined when all definitions are clearly given. It starts from axioms and deduces according to specified rules, thereby constructing the entire mathematical system. The difference between computational thinking and mathematical thinking lies in: it emphasizes more the formalization part. It doesn't care whether the deductive starting point is intuitive or correct; what it cares about is whether there are correct connections between input and output, known quantities and unknown quantities.

Since knowledge from any discipline can be expressed in propositional form, we might as well use formal means to explain the difference between mathematical thinking and computational thinking.

We know the hypothetical reasoning rule: $(A→B)∧A=>B$

Problems that mathematical thinking needs to solve: not only include the truth value of the implication $A→B$, but also need to determine whether proposition $A$ is correct. The problems studied by computational thinking are $A→B$, which is simplified. It only needs to determine whether the process from $A$ to $B$ is correct.

Next, we study the connection between computational thinking and engineering thinking.

Engineering is a certain application of mathematics and science: solving the most problems with the least resources. As for engineering thinking, although there is no recognized definition, this doesn't hinder our understanding of it at all. The core of engineering thinking lies in approximation: **adding objective environmental constraints to actual theory. Proposing feasible solutions and evaluating feasibility, choosing the best to use.**

We can still replace "engineering" with "computation" without harm. For example, in computer science, our constraint indicators for algorithms are: time complexity and space complexity.

Computational thinking originates from mathematical thinking and engineering thinking, but its connotation is not merely this. Computation, essentially, is using a series of operations, that is, mappings, to establish mapping relationships from unknowns to knowns, establishing relationships from input to output. It is an extremely rigorous science: computational results can be tested for correctness—sufficient falsifiability; it is a practical engineering project that needs to consider constraint factors such as complexity and robustness—realistic constraints; it is also an elegant art, as there are many, many implementation ways for the same mapping from A to B, some complex, some simple, some beautiful, and some ugly. The input and output of the problem have been defined—but the implementation process is full of creativity. Computational thinking is a construction activity: it's just that the building materials are not wood, stone, brick, and tile, but various basic operations. With these materials, we can unleash unlimited creativity to build the houses we want.

We can also study the connotation of computational thinking more deeply. If we notice another important concept: algorithm. All the connotations of computational thinking proposed by Professor Zhou Yizhen in "Computational Thinking" are concepts from algorithms. In fact, any content that can be classified into the category of computational thinking can find corresponding things in algorithms. In other words, isomorphism can be established between computational thinking and algorithm application. Going further, computational thinking is the methodology for using algorithms. One point of difference to note is that computational thinking is not directly equivalent to algorithms; thinking belongs to "the Way" while algorithms belong to "tools," and how to use "tools" is "the Way." Another point to note: the concept of "computational thinking" implies that the execution subject of this process is humans, not machines.

In summary, we can define computational thinking in two other different ways.

The first definition is specific difference + genus concept: computational thinking is engineered mathematical thinking.

The second definition is: computational thinking is thinking that applies algorithms.

## 4. Significance of Computational Thinking

Whether it's thinking about the mysteries of the universe or controlling muscles for the next step, we are constantly thinking, whether consciously or unconsciously. This thinking is a computation because it indeed fits the definition of computation: calculating unknowns from knowns. However, the computation that occurs in our daily minds differs from the computation that happens inside computers: this difference lies in that most humans, most of the time, tend to compute using inductive methods, in other words, a neural network approach. No one knows what kind of black magic exists among 10 billion neurons and their connections that are 100,000 times that number; computers, on the other hand, strictly follow deductive methods and act according to strict rules. If we happen to use computational thinking to make an analogy: computers use exactly RISC instruction sets, while human brains use extremely complex CISC instruction sets.

For the difference between human brains and computers, a better evaluation method is: whether they fit the environment. For the complex and changeable material world, human brains have achieved flexibility and adaptability that computers can't match through extremely large redundant design; however, for stable environments and determined conditions, computer performance has overwhelming advantages. In the performance of simple repetitive work, computers are always more efficient and more trustworthy than human brains. It is exactly this characteristic of computers that has liberated scientists and engineers from slave-like mechanical calculations, enabling them to use precious mental resources more on creative work, directly triggering the third industrial revolution.

Computational thinking is a conceptual model, a methodology extracted from computer science. When we apply a thinking model, we go through three stages: modeling, solving, and interpretation. Correspondingly, these are abstract thinking, deductive thinking, and divergent thinking. Through abstraction and formalization, we summarize the problems we need to study, express them in a paradigm, and establish models; then through rigorous deductive reasoning, we solve this model; finally, using divergent thinking, we express the meaning contained in this model in natural language. Past scientific research often fell into bottlenecks at the model-solving stage: computational load. The appearance of computers solved this problem, thus making scientific and technological research develop by leaps and bounds.

Not only that, computational thinking was once the patent of mathematicians, computer scientists, software engineers, and others. However, with the popularization of computers, the explosive development of application fields, and the continuous breakthrough of computational ability bottlenecks, the threshold of computation as an intellectual activity has been broken. Computational thinking should no longer be the exclusive domain of these people; it will gradually spread, first becoming an essential skill for all science and engineering students, further expanding to become a basic quality for all college students, and ultimately extending step by step to become collective intuition for all humanity. Computational thinking, through the unstoppable momentum of the information wave, has received more and more attention.

## 5. Current Status of Computational Thinking Cultivation in Undergraduate Education

On this point, I express deep regret for domestic teachers. Because from the big direction, the educational approach is wrong. Of course, I also express deep sympathy, as this is also a compromise to reality: without reasonable incentive mechanisms, who would do this laborious work? The second point is also a student problem: it's very easy to teach a few elite students well, but trying to teach a good class to a nest of students with varying levels of understanding, that's really laborious and thankless.

The Master was never weary in teaching. But in my academic career, teachers who truly achieved this can be counted on one hand. Most teachers today like to stick to the book. Even if there are some "teaching innovations," they're just formalism. Perhaps teachers think that applying analogies like comparing virtual storage systems to brain-library systems, network systems to highway systems, etc. to teaching counts as innovation. However, these means are only efforts for memorizing knowledge and shallow understanding, not touching the essence of the problem.

The core of the problem lies in: in today's China, the knowledge teachers teach is not valuable. The real reason causing students to be disconnected from social needs: **students' lack of insight and understanding**.

It's not some core secrets of aircraft carriers and missiles; the knowledge taught in class really isn't valuable. Anyone with even slight information retrieval ability can easily find many of these things online quickly. What's truly valuable is teachers' understanding and insight. Views on problems, detours taken in learning. Unfortunately, these contents are rarely mentioned in teaching. It's exactly these things not in the "syllabus" that are the real essence. Students don't lack knowledge; what they lack are methods for applying knowledge.

Why do we call Newton and Einstein geniuses? Is it because they mastered calculus and relativity? No, any qualified modern undergraduate knows these. They are called geniuses because they invented calculus and invented relativity. That kind of creative thinking spark is the most precious treasure. The difficulty of using wheels and reinventing wheels versus inventing wheels is vastly different. What's precious is not that knowledge, but that kind of enlightenment that creates knowledge.

In the four stages of learning: knowledge, understanding, awareness, and enlightenment. What teachers teach basically only exists at the first stage. Some good teachers have special teaching skills and can directly pass second-level information—understanding—to students. However, truly achieving mastery and forming awareness, that is, cultivating computational thinking, is not a task that teachers can directly complete. What can be named but cannot be spoken is a very common phenomenon. As for the final stage of learning, what teachers can do is inspire, induce, stimulate, and develop. But how many teachers have this ability and qualification?

Speaking back to it, the task that teaching should complete is to inspire students and recreate the process of knowledge creation.

For a concept, first, you need to know what problem it was proposed to solve. Then comes the question of how to apply this concept. Finally, knowing the knowledge content of this theory is far from enough; you also need to restore these theories to life practice and use them to solve specific problems. This counts as a complete teaching process.

Current teaching can be said to have only completed the middle part: knowledge content. If you don't believe it, open any computer science textbook or mathematics textbook at hand, then open a textbook used by American universities, make a slight comparison, and you can see the point. For example, after I finished reading "Thomas Calculus" and "Linear Algebra and Its Applications," I suddenly found that my notes were almost no different from domestic textbook content. In other words, these domestic textbooks can all be said to be knowledge content summarized by teachers after their own learning—second-hand digested products. From a systematic perspective, there's nothing to criticize. They might be good for review, as knowledge indexes. But when applied to teaching practice, that's a disaster. This is also why for many excellent students, self-study effects are much, much better than teacher lectures.

## 6. How to Cultivate Computational Thinking Among Undergraduates?

First point: correct positioning.

In fact, cultivating interest is what teachers should do. As they say, the master leads you to the door, but practice depends on the individual.

Knowledge is all in books; teachers don't need to teach it. What teachers really need to do is explain the reasons this theory was proposed and the problems it can solve. If this problem happens to be something students are interested in, then you can see how interest becomes the best teacher. Be a mentor, not a teacher.

Second point: history-driven learning mode.

Just as the study of philosophy is the study of the history of philosophy, mathematics and computer education can also consider trying this mode. Follow the timeline rather than system structure, and throughout the educational career, recreate the discipline's development process. Constantly experience the process of negation, from the most basic concepts, from the most intuitive phenomena, recreating the process by which predecessors built the entire theoretical system. Let students understand where theory comes from and where it's going. Theory distilled from problems must ultimately return to problems.

Third point: correction of incentive systems and evaluation systems

The current incentive system and reward-punishment evaluation systems have many problems, whether for students or teachers. Impetuous. Well, saying more about this brings tears.

For actual reform, I don't hold any hope. Such a large systematic project—small-scale educational experiments can be managed, but popularization would take several generations of effort to complete. Meanwhile, changing teaching modes at the current stage is not just a difficulty issue, but also a demand issue. After all, what the country needs now is a large number of cheap engineers who can work. As for innovation, except for high-end cutting-edge technology, copying foreign countries is quite mainstream, and following foreigners to pick up breadcrumbs can still feed quite a few people at the current stage. Really a sad story.