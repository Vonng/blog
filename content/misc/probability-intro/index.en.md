---
title: "Basic Concepts of Probability Theory"
date: 2017-03-27
author: vonng
math: true
summary: |
  Basic knowledge notes on probability theory: axiomatic foundations, probability calculus, counting, conditional probability, random variables and distribution functions
---

{{< katex >}}

## 1. Set Theory

Sample space and sample points are undefined basic concepts in probability theory, like the concepts of points and lines in geometry.

##### Definition: Event

Event: An event is a **set** of sample points.

* $A=0$ means event A contains no sample points, i.e., A is an impossible event.

  $A=0$ is an algebraic expression rather than an arithmetic expression; 0 here is a symbol.

* The event consisting of all points in the sample space that do not belong to event A is called the complement of A, or the negation event. It is denoted as $A^C$, where $S^C=0$

* The intersection of events A, B, C is denoted as $A\cap B \cap C$, and the union is denoted as $A \cup B \cup C$

* $A\subset B$ is called A implies B, meaning every point of A is in B.



## 2. Foundations of Probability Theory

Here we use an axiomatic method to **define** probability. As for how to **interpret** probability, such as "frequency of event occurrence" (frequentist school) or "belief in event occurrence" (Bayesian school), we don't concern ourselves with that here.

### 2.1 Axiomatic Foundation

For every event A in sample space S, we want to assign A a number P(A) between 0 and 1, called the probability of A.

##### Definition: σ-algebra/Borel field

A family of subsets of S is called a **σ-algebra** or **Borel field**, denoted as $\mathcal{B}$, if it satisfies the following three properties:

* $\varnothing \in \mathcal{B}$
* $A \in \mathcal{B} \Rightarrow A^C \in \mathcal{B} $
* $\displaystyle A_1,A_2,\cdots \in \mathcal{B} \Rightarrow \bigcup_{i=1}^{\infty}{A_i} \in \mathcal{B}$

There are many σ-algebras satisfying these three properties (empty set exists, closed under complement and union operations). Here we discuss the smallest σ-algebra containing all open sets in S. For countable sample spaces, usually $\mathcal{B}=\{$all subsets of S, including S itself$\}$. For uncountable sample spaces, such as $S=(-\infty,\infty)$ being the real line, we can take $\mathcal{B}$ to contain all sets of the form $[a,b],(a,b],[a,b),(a,b)$, where $a,b \in \mathbb{R}$.

##### Definition: Probability function

Given sample space S and σ-algebra $\mathcal{B}$, a function P defined on $\mathcal{B}$ and satisfying the following conditions is called a **probability function**:

* $\forall A \in \mathcal{B}, P(A) \ge 0$
* $P(S) = 1$
* If $A_1,A_2,\cdots \in \mathcal{B}$ are pairwise disjoint, then $\displaystyle P(\bigcup_{i=1}^{\infty}{A_i}) = \sum_{i=1}^{\infty}{P(A_i)}$

Non-negativity of probability, normalization of probability, countable additivity of probability. These three properties are called probability axioms, or Kolmogorov axioms. As long as these three axioms are satisfied, function P can be called a probability function.

(PS: Statisticians usually don't accept the countable additivity axiom, only accepting its corollary: finite additivity axiom $P(A\cup B)=P(A)+P(B)$)



### 2.2 Probability Calculus

Theorem: Let P be a probability function, $A,B \in \mathcal{B}$, then

* $P(\varnothing) = 0$
* $P(A) \le 1$
* $P(A^C) = 1- P(A)$
* $P(B \cap A^C) = P(B)- P(A \cap B)$
* $P(A \cup B) = P(A) + P(B)- P(A \cap B)$
* $A \subset B \Rightarrow P(A) \le P(B)$
* $P(A \cap B) \ge P(A) + P(B) - 1$, Bonferroni inequality, used to estimate concurrent probability from individual event probabilities
* For any partition $C_1,C_2,\cdots$, we have $\displaystyle P(A)= \sum_{i=1}^{\infty}{P(A \cap C_i)}$
* For any sets $A_1,A_2,\cdots$ we have $\displaystyle P(\bigcup_{i=1}^{\infty}{A_i})  \le \sum_{i=1}^{\infty}{P(A_i)}$, Boole inequality.




### 2.3 Counting

Counting involves much combinatorial analysis knowledge, all based on this theorem:

##### Theorem: Fundamental counting theorem

If a task consists of k mutually independent subtasks, where the i-th task can be completed in $n_i$ ways, then the entire task can be completed in $n_1 \times n_2 \times \cdots \times n_k$ ways.

The proof of this theorem can be derived from the definition and properties of Cartesian product operations.



Two basic counting problems include:

* Are samples ordered?
* Is sampling with replacement?



##### Definition: Population/Subpopulation/Ordered sample

* Population: We use a population of size n to represent a set consisting of n elements.

  Since a population is a set, populations are unordered. Populations are identical if and only if two populations contain the same elements.

* Subpopulation: Selecting r elements from a population of size n constitutes a subpopulation of size r.

* Numbering elements in a subpopulation gives an **ordered sample** of size r. There are $r!$ total ways.



##### Number of ways to select r objects from n objects

|       | Without replacement sampling                                    | With replacement sampling              |
| ----- | ---------------------------------------- | ------------------ |
| Ordered sample  | $\frac {n!} {(n-r)! } = \binom n r \cdot r! $ | $n^r$              |
| Unordered subpopulation | $\binom n r = \frac {n!}{(n-r)!r!}$      | $\binom {n+r-1} r$ |

* Ordered with replacement is simplest: n possibilities each time, r samplings, so $n^r$
* Ordered without replacement: selecting ordered samples of size r from n populations, so $\binom n r \cdot r! = \frac {n!}{(n-r)!}$
* Unordered without replacement is similar to ordered without replacement, except what's drawn is a subpopulation of size r rather than ordered sample
* With replacement unordered sampling is most complex. Can be understood as placing r marks on n elements. Treating element boundaries as elements, n boxes have n+1 boundaries total, with r marks. Excluding the two side boundaries, there are n-1+r positions total. Choose r from these positions to place marks. So it's $\binom {n-1+r} r$



##### Common combinatorial problems

* Population of size n, with replacement sampling of ordered sample of size r:

  $\displaystyle n^r$

* Population of size n, without replacement sampling of ordered sample of size r:

  $\displaystyle (n)_r=n(n-1)\cdots(n-r+1)=\frac{n!}{(n-r)!} = \binom n r \cdot r !$

* Population of size n, with replacement sampling of subpopulation of size r:

  $\displaystyle \binom n r = \frac{(n)_r}{r!} = \frac{n!}{(n-r)!r!}$

* Population of size n, without replacement sampling of subpopulation of size r:

  $\displaystyle \binom {n-1 +r} r$

* Population of size n divided into k groups, each with $r_1,\cdots, r_k$ elements:

  $\displaystyle \frac{n!} {r_1!r_2!\cdots r_k!}$

* Population of size n with m positive samples, without replacement sampling of subpopulation of size r, probability of k positive samples appearing:

  $\displaystyle \frac{\binom{m}{k} \binom{n-m}{r-k}}{\binom{n}{r}}$



## 3. Conditional Probability and Independence

##### Definition: Conditional probability

Let A,B be events in S, with $P(B) > 0$. The conditional probability of event A occurring given that event B has occurred is denoted $P(A |B)$ and defined as:

$$
\displaystyle
P(A|B) = \frac {P(A \cap B) } {P(B)}
$$

Intuitively this is easy to understand: the probability of AB occurring together equals the probability of B occurring times the probability of A occurring given B has occurred: $P(AB) = P(A|B)P(B)$

Naturally, the probability of A occurring given B is: probability of AB occurring together divided by probability of B occurring. Here the sample points of event B constitute the new sample space, and P(A|B) must satisfy the three probability axioms, forming a probability function on the new sample space.



##### Theorem: Bayes' formula

Let $A_1,A_2,\cdots$ be a partition of the sample space, B be any set, then for $i=1,2,\cdots$:

$$
\displaystyle
P(A_i | B) = \frac
{P(B|A_i)P(A_i)}
{\sum_{j=1}^{\infty}{P(B|A_j)P(A_j)}}
$$


##### Definition: Statistical independence

Events A and B are called statistically independent if $P(A \cap B) = P(A)P(B)$

A series of events $A_1,\cdots, A_n$ are called mutually independent if for any $A_{i_1},\cdots,A_{i_k}$:

$$
\displaystyle
P( \bigcap_{j=1}^{k}{A_{i_j}}) = \prod_{j=1}^{k}P(A_{i_j})
$$


## 4. Random Variables

Many experiments involve a variable with generalizing power that is much simpler to handle than the original probability model.

For example: voting results of 50 people, sample space is $2^{50}$. What we're actually interested in is just how many people agree, so define variable X = number of agreements, and the sample space becomes the integer set: $\{s| 0 \le s \le 50 \wedge s \in \mathbb{Z} \}$

##### Definition: Random variable

A function mapping from sample space to real numbers is called a **random variable**

Defining a random variable also defines a new sample space (the range of the random variable). More importantly, we need to define the **probability function of this random variable** through the **probability function** defined on the original sample space: the induced probability function $P_X$.

Suppose we have sample space $S=\{s_1,\cdots, s_n\}$ and probability function P, and define the range of random variable X as: $\mathcal{X} = \{x_1,\cdots, x_n\}$. We can define probability function $P_X$ on $\mathcal{X}$ as follows: observing event $X=x_i$ occurs if and only if the result $s_j \in S$ of the random experiment satisfies $X(s_j)=x_i$, i.e.:

$$
\displaystyle
P_x (X=x_i) = P(\{s_j \in S : X(s_j) =x_i\})
$$

Since $P_X$ is obtained through the known probability function P, it's called the **induced probability function** on $\mathcal{X}$. It's easy to prove this function also satisfies probability axioms.

For continuous sample space S, the situation is similar:

$$
\displaystyle
P_x (X \in A) = P(\{s_j \in S : X(s_j) \in A\})
$$

## 5. Distribution Functions

For any random variable, we can construct a function: **cumulative distribution function**, abbreviated as CDF.

##### Definition: Cumulative distribution function

The cumulative distribution function of random variable X, denoted $F_X(x)$, represents: $F_X(x) = P_X(X \le x)$

The distribution of X is $F_X$, which can be abbreviated as: $X \sim  F_X(x)$, where "~" reads as "is distributed as."



##### Example: Coin toss

Simultaneously toss three coins, let X = number of heads up, then X's cumulative distribution function is a step function:

$$
\displaystyle
F_X(x) = \left\{
\begin{aligned}
0     & &  -\infty < x < 0 \\
1/8 & & 0 \le x < 1 \\
1/2 & &  1 \le x < 2\\
7/8 & &  2 \le x < 3\\
1 & &  3 \le x < \infty\\
\end{aligned}
\right.
$$

From the definition of cumulative distribution function, $F_X(x)$ is **right-continuous**.



##### Properties: Cumulative distribution function

Function $F(x)$ is a cumulative distribution function if and only if it simultaneously satisfies the following three conditions:

* $\displaystyle \lim_{x\rightarrow -\infty}{F(x)} = 0$ and $\displaystyle \lim_{x\rightarrow \infty}{F(x)} = 1$
* $F(x)$ is a monotonically increasing function of $x$
* $F(x)$ is right-continuous: $\displaystyle  \forall x_0 ( \lim_{x\rightarrow x_0^+}{F(x) } = F(x_0) )$



##### Definition: Discrete/continuous random variables

Let X be a random variable. If $F_X(x)$ is a continuous function of x, then X is called **continuous**; if $F_X(x)$ is a step function of x, then X is called **discrete**.



The cumulative distribution function $F_X$ can completely determine the probability distribution of random variable X. This leads to the concept of identically distributed random variables.



##### Definition: Identically distributed random variables

Random variables X and Y are called **identically distributed** if for any set $A \in \mathcal{B}^1$, $P(X\in A)=P(Y\in A)$

Note that two identically distributed random variables don't mean $X=Y$. For example, let X and Y respectively be the number of heads and tails when tossing three coins.



##### Theorem: Properties of identically distributed random variables

Random variables X and Y are identically distributed if and only if $\forall x ( F_X(x) = F_Y(x))$




## 6. Probability Density Function and Probability Mass Function

Related to random variable X and cumulative distribution function $F_X$ is another function: if X is a continuous random variable, this function is called probability density function; if X is a discrete random variable, this function is called probability mass function. Both focus on the "point probability" of random variables.



##### Definition: Probability mass function (pmf)

The probability mass function of discrete random variable X is defined as:

$$
\displaystyle
\forall x (f_X(x) = P_X(X=x))
$$

Set interpretation of probability mass function: $P_X(X=x)$, i.e., $f_X(x)$ equals the jump height of the cumulative distribution function at x.



Extending to continuous variables:

$$
\displaystyle
P(X\le x) = F_X(x) = \int_{-\infty}^{x}{f_X(t)dt}
$$

##### Definition: Probability density function (pdf)

The probability density function of continuous random variable X is a function satisfying:

$$
\displaystyle
F_X(x) = \int_{-\infty}^{x}{f_X(t)dt}, \text{ for any } x
$$


##### Theorem: Properties of PDF/PMF

Function $f_X(x)$ is the probability density function (or probability mass function) of random variable X if and only if it satisfies both of the following conditions:

* $\forall x ( f_X(x) \ge 0)$
* $\sum_x {f_X(x) = 1}$  (probability mass function) or  $\int_{-\infty}^{\infty}{f_X(x)dx} = 1$ (probability density function)