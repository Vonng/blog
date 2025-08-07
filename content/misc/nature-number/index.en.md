---
title: "What Exactly Are Natural Numbers?"
date: 2013-04-26
author: vonng
math: true
summary: |
  The concept of natural numbers should have been learned in elementary school. The foundation of all elementary mathematics begins with such a definition. However, when I entered university, I encountered this question again in discrete mathematics.
---

{{< katex >}}

The concept of natural numbers should have been learned in elementary school. The foundation of all elementary mathematics begins with such a definition. However, when I entered university, I encountered this question again in discrete mathematics.


**What is the definition of natural numbers?**

In one sentence, it can be expressed as:

$$
0=∅ ∧ n+1=n∪\{n\}
$$

People who haven't studied discrete mathematics probably wouldn't answer this way. So how would normal people answer this seemingly simple question?
 

At first glance, this question seems easy to solve. Natural numbers are: 0, 1, 2, 3... such numbers are called natural numbers. But can such a description be satisfactory?

Perhaps we can make the definition of natural numbers a bit more rigorous using set-theoretic description? Like this: the set of non-negative integers $\{x|x≥0∧x∈Z\}$. But this raises new problems: what are integers? If we continue asking, what are rational numbers, what are real numbers, what are complex numbers? Ultimately we still cannot solve this problem. This series of questions should be solved from front to back: we should define integers from natural numbers, not define natural numbers from integers. So this solution is also unreasonable.

 

Perhaps going further, we can define a formal system to express it?

Define a 4-tuple $<A(N),E(N),Ax(N),R(N)>$

Respectively representing the system's alphabet, set of well-formed formulas, axiom set, and inference rule set.

Alphabet $A(N)={0,1,2,3,4,5,6,7,8,9}$

Stipulate that sequences like $N= A_n …A_4 A_3 A_2A_1$ constitute natural numbers, assigning corresponding place values to each digit.

Of course, the remaining rules and regulations can be filled in by oneself.

Of course there's a problem: why are natural numbers in decimal?

At the same time, more seriously, such a definition obviously still stays at "what natural numbers look like." It doesn't solve the most fundamental problem: "what natural numbers are."


Often the simpler the question, the harder it is to answer.

"What are natural numbers" is such a question.

 

So what exactly are natural numbers?

The Pythagorean school believed: everything is number.

Natural numbers, as the name suggests, are natural numbers, numbers existing in nature.

To understand what natural numbers are, we need to understand how natural numbers were born.

So let us simulate ancient people's thinking, starting from the birth of natural numbers.

 

First, we need to understand the huge difference between our thinking and that of ancient people, and the most crucial reason is: the ability to use concepts. This can also be viewed from another angle: abstract thinking ability.

Concepts are powerful and effective weapons of thought. We can use many, many concepts in communication: such as matter, consciousness, thought, existence. But before such concepts were formed, people found it very difficult to communicate so conveniently. For example, when I say: "matter determines consciousness," the meaning of this sentence is very clear and explicit - modern people can understand it at a glance. But for people in ancient times, it would seem inexplicable: what is matter? What is consciousness?

Some thinkers understood this principle. To convey concepts they understood to others, they had to use specific examples and stories. For instance, telling stories in the form of fables, or using concrete things to embody principles, using "phenomena" to transmit "the way." Without abstract concepts, they couldn't communicate as concisely, clearly, and efficiently as we do now. But undoubtedly, ancient people were extremely great - it was they who ingeniously created these concepts, giving us tools for reasoning.

So how was the concept of numbers formed? Actually, everyone has experienced this process - when learning mathematics in elementary school, people gradually form the concept of numbers. Unfortunately, I think not many people can remember this process. So to understand this question, let's still imitate ancient people's thinking. We might as well remove the concept of numbers from our minds. Now, about numbers we know nothing, just like ancient people - what is 0, what is 1, we have no concept at all.

Suppose such a scenario: I have an apple. Then I picked up another apple. Because I don't know the concept of "two," to express such information to others, I can only say: "I have an apple, I have an apple." Ancient people had no concept of numbers and could only express quantity through such "repetition." Obviously, one or two can be counted, using fingers when not enough, then toes. But what about hundreds or thousands of things? To solve this problem, ancient people invented knot-tying for counting.

Knot-tying for counting can be said to be a great innovation in mathematical history, and the mathematical principle it embodies is: **unary**.

What is unary?! We've heard of decimal, duodecimal, sexagesimal, and binary, so what is unary?

It's simple: decimal carries over every ten, binary carries over every two.

Unary carries over every one, with each digit having equal weight, all being one.

        

Just like counting on fingers. For one apple, I bend one finger; each finger is equivalent, representing one apple. Similarly, time-sequence signals are binary encoded because they have two states 0 and 1, while pulse signals are unary because they only count the number of pulses - each additional pulse adds one count.

Unary is the most primitive base system, the most primitive counting method, and the foundation of all other base systems. In many regions, many people who haven't attended school still use this primitive method for calculations - tallying votes with marks is a typical unary counting system.



So how should the rules of this counting method be expressed in natural language?

* First, rule one: If I have no apples, I use "no symbols at all" to represent this
* Then, rule two: If I add one more apple to a pile of apples, then I add one more symbol.

 

For example, now I use * to represent one apple.

Then something like `  ` (nothing) represents I have no apples, and `*` represents I have one apple

If I add one more apple, I need to add one more symbol, resulting in: `**`

 

This is the foundation of natural numbers: unary. Naturally, we can introduce the formal language of discrete mathematics and set theory to define natural numbers:

1. Define 0 as ∅: zero is nothing, it's the empty set.

2. Define $n+1=n∪\{n\}:$ $n+1$ means the number after $n$

 

See it? This is a recursive definition, exactly the mathematical induction learned in middle school.

The essence of such a definition is still unary. It's just that the basic symbols used for counting have become ∅ and its derived symbols (derivation means nesting curly braces).

Using such a definition, let's derive a few examples:

$0 = ∅$

$1=\{∅\}$

$2=\{∅，\{∅\}\}$

$3=\{∅，\{∅\}，\{∅，\{∅\}\}\}$

$4=\{∅，\{∅\}，\{∅，\{∅\}\}，\{∅，\{∅\}，\{∅，\{∅\}\}\} \}$

 etc...

Let's look at what advantages such a definition has

0, which is the empty set, has no symbols inside.

For every non-zero set, each set not only **contains** all elements of previous sets, but also has **one more** element than the previous set.

**For each set, the number of elements inside exactly equals its corresponding natural number.** We call the number of elements in such a set the **cardinality** of the set.

 

But why use such a complex form for representation? Sets nested within sets?

The reason is that when defining the concept of sets, mathematicians stipulated that elements in sets cannot be repeated.

So they ingeniously put ∅ in curly braces. This way, ∅ and {∅} can be placed in the same set.

 

Why not represent it this way? Each new element gets a new layer of curly braces around the empty set:

{∅，{∅}，{{∅}}，{{{∅}}}，… }

If represented this way, it's barely acceptable, but unfortunately, such a form would lose many properties that natural numbers should have.

For example, trichotomy.

Natural numbers have trichotomy: for two natural numbers, either one is greater than the other, or one is smaller than the other, or the two are equal. There's no fourth possibility. Just like comparing two piles of apples, it will always be one of these three cases.

Such properties are important. How do we obtain such properties through this formal definition?

The formal definition just mentioned obviously satisfies the requirement.

If A is smaller than B, then A is a subset of B.

If A is greater than B, then B is a subset of A.

If A and B are the same size, then A and B are equipotent, meaning they contain the same number of elements.

This is the trichotomy possessed by natural numbers defined in set language.

Besides this, there are many other excellent properties, such as the definition of set cardinality, which won't be expanded upon here.

**Therefore, it can be said that this definition is both natural and ingeniously clever!**

It has all the properties that natural numbers have.

It performed a revolutionary expansion of the concept of natural numbers.

It unified natural numbers under sets, and then NZQRC were also naturally unified and defined on sets.

The foundation of the entire mathematical edifice is built upon these foundations.

In summary, **natural numbers are sets**.

**Not only are natural numbers as a whole a set**, **but more importantly: each natural number is a set.**

 

How about it? Don't you think this definition given by discrete mathematics set theory is too perfect?

Precise, concise, well-structured, full of orderly beauty?