---
title: Optimize Bio Cores First, CPU Cores Second
linkTitle: Optimize Bio Cores First, CPU Cores Second
date: 2024-09-07
author: |
  [DHH](https://world.hey.com/dhh/optimize-for-bio-cores-first-silicon-cores-second-112a6c3f) | [Translator: Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat Official Account]()
summary: >
  Programmers are expensive, scarce biological computing cores, the anchor point of software costs — please prioritize optimizing biological cores before optimizing CPU cores.
module: []
tags: [Database]
---


## Optimize Bio Cores First, Silicon Cores Second

A big part of the reason that companies are going ga-ga over AI right now is the promise that it might materially lower their payroll for programmers. If a company currently needs 10 programmers to do a job, each having a cost of $200,000/year, then that's a $2M/year problem. If AI could even cut off 1/4 of that, they would have saved half a million! Cut double that, and it's a million. Efficiency gains add up quick on the bottom line when it comes to programmers!

That's why I love Ruby! That's why I work on Rails! For twenty years, it's been clear to me that this is where the puck was going. Programmers continuing to become more expensive, computers continuing to become less so. Therefore, the smart bet was on making those programmers more productive **EVEN AT THE EXPENSE OF THE COMPUTER**!

That's what so many programmers have a difficult time internalizing. They are in effect very expensive "biological computing cores," and the real scarce resource. Silicon computing cores are far more plentiful, and their cost keeps going down. So as every year passes, it becomes an even better deal trading compute time for programmer productivity. AI is one way of doing that, but it's also what tools like Ruby on Rails were about since the start.

Let's return to that $200,000/year programmer. You can rent 1 AMD EPYC core from Hetzner for $55/year (they sell them in bulk, $220/month for a box of 48, so 220 x 12 / 48 = 55). That means the price of one biological core is the same as the price of 3663 silicon cores. Meaning that if you manage to make the bio core 10% more efficient, you will have saved the equivalent cost of 366 silicon cores. Make the bio core a quarter more efficient, and you'll have saved nearly ONE THOUSAND silicon cores!

But many of these squishy, biological programming cores have a distinctly human sympathy for their silicon counterparts that overrides the math. They simply feel bad asking the silicon to do more work, if they could spend more of their own time to reduce the load by using less efficient for them / more efficient for silicon tools and techniques. For some, it seems to be damn near a moral duty to relieve the silicon of as many burdens they might believe they're able carry instead.

And I actually respect that from an artsy, spiritual perspective! There *is* something beautifully wholesome about making computers do more with fewer resources. I still look oh-so-fondly back on the demo days of the Commodore 64 and Amiga. What those wizards were able to squeeze out of [a mere 4kb](https://www.youtube.com/watch?v=wl6mXn_wHEw) to make the computer dance in sound and picture was truly incredible.

It just doesn't make much economic sense, most of the time. Sure, there's still work at the vanguard of the computing threshold. Somebody's gotta squeeze the last drop of performance out of that NVIDIA 4090, such that our 3D engines can raytrace at 4K and 120FPS. But that's not the reality at most software businesses that are in the business of making business software! For that work, computers have long since been way fast enough without heroic optimization efforts.

That's the kind of work I've been doing for said twenty years! Making business software and selling it as SaaS. That's what an entire industry has been doing to tremendous profit and gainful employment across the land. It's been a bull run for the ages, mostly driven by programmers working in high-level languages figuring out business logic and finding product-market fit.

So, whenever you hear a discussion about computing efficiency, you should always have the squishy, biological cores in mind. Most software around the world is priced on their inputs, not on the silicon it requires. Meaning even small incremental improvements to bio core productivity is worth large additional expenditures on silicon chips. And this cost-effectiveness ratio only becomes more favorable toward fully utilizing bio cores year after year.

— At least up until the point that we make them obsolete and welcome our AGI overlords! But nobody seems to know when or if that's going to happen, so best you deal with the economics of the present day, pick the most productive tool chain available to you, and bet that happy programmers will be the best bang for your buck.


> Author: David Heinemeier Hansson, DHH, 37signals CTO, Ruby on Rails creator
>
> Translator: Feng Ruohang, PostgreSQL Hacker, author of open-source RDS PG — Pigsty, database veteran, cloud computing mudslide.
>
> [Optimize for bio cores first, silicon cores second](https://world.hey.com/dhh/optimize-for-bio-cores-first-silicon-cores-second-112a6c3f) @ 2024-09-06




--------

## Feng's Commentary

DHH's blog is as insightful as ever — though the truth might not sound pleasant, programmers are essentially a type of biological computing core — Bio Core, and many programmers have forgotten this point.

Actually, a hundred years ago, "Computer" referred to "computer operators" rather than "computers"; and in the 1940s-50s, computing power was once measured in units of "Kilo-Girls," the computational speed of a thousand girls, with similar units like `kilo-girl-hour`. Of course, with the rapid advancement of information technology, these tedious computational tasks were handed over to computers, allowing programmers to focus on higher-level abstractions and creation.

For the database industry I'm in, I think this article can give users an insight — the real bottleneck of databases is no longer CPU silicon cores, but biological cores that can use databases well. For the vast majority of use cases, the database bottleneck is no longer CPU, memory, I/O, network, storage, but developers' and DBAs' thinking, cognition, experience, and wisdom.

Therefore, nobody cares whether your database can support 1 million TPS, but whether your software can solve problems with minimal time cost, complexity cost, and cognitive cost.
Usability, simplicity, and maintainability have become the focus of competition — RDS database services that focus on this have therefore been highly successful (similarly for Neon, Supabase, Pigsty, etc.).

Cloud vendors like AWS took open-source MySQL and PostgreSQL kernels all the way to the top position in the database market. Is it because AWS has deeper database kernel expertise than Oracle/EDB and knows how to better utilize silicon cores? Not at all. It's because compared to optimizing silicon cores, they better understand how to optimize biological cores — they know how to make developers, DBAs, and operations personnel more easily use databases well — using databases well, rather than manufacturing databases, has become the new core bottleneck.

So, traditional database kernels are a sunset industry that will become low-margin manufacturing like Gree air conditioners and Lenovo computers. The real high-tech and technological innovation will happen in database management — using software to assist, empower, or even dare to "replace" part of developers — how to better use database kernels and silicon CPU cores, improve biological core productivity, reduce cognitive costs, simplify complexity, and improve usability. This is the future development direction of the database industry.




The high-tech industry must rely on technological innovation as the driver. If you can use open-source PG kernel to replace Oracle and SQL Server, others can too — the best result is nothing more than Oracle and Microsoft both abandoning traditional databases to transform into cloud services, with traditional databases becoming low-profit manufacturing. Just like the PC industry twenty years ago. Twenty years ago, IBM, Dell, and HP were all international players, and China's Lenovo said it wanted to be world-class. Today, Lenovo indeed achieved this, but the PC industry is no longer a high-tech industry — just the most boring ordinary manufacturing.

Even the [truly self-developed distributed database kernels](/db/distributive-bullshit) that look quite capable domestically, if they choose the wrong track, the best ending they can expect is to become the Changhong of the database industry, earning a five-point profit margin. Then being crushed by cloud vendor RDS and local-first RDS services using open-source PostgreSQL kernels, ultimately becoming the "Kilo-Girl" of the database field.




--------

## Optimize for bio cores first, silicon cores second

> David Heinemeier Hansson 2024-09-06
>
> [Optimize for bio cores first, silicon cores second](https://world.hey.com/dhh/optimize-for-bio-cores-first-silicon-cores-second-112a6c3f)

A big part of the reason that companies are going ga-ga over AI right now is the promise that it might materially lower their payroll for programmers. If a company currently needs 10 programmers to do a job, each have a cost of $200,000/year, then that's a $2M/year problem. If AI could even cut off 1/4 of that, they would have saved half a million! Cut double that, and it's a million. Efficiency gains add up quick on the bottom line when it comes to programmers!


That's why I love Ruby! That's why I work on Rails! For twenty years, it's been clear to me that this is where the puck was going. Programmers continuing to become more expensive, computers continuing to become less so. Therefore, the smart bet was on making those programmers more productive EVEN AT THE EXPENSE OF THE COMPUTER!


That's what so many programmers have a difficult time internalizing. They are in effect very expensive biological computing cores, and the real scarce resource. Silicon computing cores are far more plentiful, and their cost keeps going down. So as every year passes, it becomes an even better deal trading compute time for programmer productivity. AI is one way of doing that, but it's also what tools like Ruby on Rails were about since the start.


Let's return to that $200,000/year programmer. You can rent 1 AMD EPYC core from Hetzner for $55/year (they sell them in bulk, $220/month for a box of 48, so 220 x 12 / 48 = 55). That means the price of one biological core is the same as the price of 3663 silicon cores. Meaning that if you manage to make the bio core 10% more efficient, you will have saved the equivalent cost of 366 silicon cores. Make the bio core a quarter more efficient, and you'll have saved nearly ONE THOUSAND silicon cores!


But many of these squishy, biological programming cores have a distinctly human sympathy for their silicon counterparts that overrides the math. They simply feel bad asking the silicon to do more work, if they could spend more of their own time to reduce the load by using less efficient for them / more efficient for silicon tools and techniques. For some, it seems to be damn near a moral duty to relieve the silicon of as many burdens they might believe they're able carry instead.



And I actually respect that from an artsy, spiritual perspective! There *is* something beautifully wholesome about making computers do more with fewer resources. I still look oh-so-fondly back on the demo days of the Commodore 64 and Amiga. What those wizards were able to squeeze out of [a mere 4kb](https://www.youtube.com/watch?v=wl6mXn_wHEw) to make the computer dance in sound and picture was truly incredible.


It just doesn't make much economic sense, most of the time. Sure, there's still work at the vanguard of the computing threshold. Somebody's gotta squeeze the last drop of performance out of that NVIDIA 4090, such that our 3D engines can raytrace at 4K and 120FPS. But that's not the reality at most software businesses that are in the business of making business software (say that three times fast!). Computers have long since been way fast enough for that work to happen without heroic optimization efforts.


And that's the kind of work I've been doing for said twenty years! Making business software and selling it as SaaS. That's what an entire industry has been doing to tremendous profit and gainful employment across the land. It's been a bull run for the ages, and it's been mostly driven by programmers working in high-level languages figuring out business logic and finding product-market fit.



So whenever you hear a discussion about computing efficiency, you should always have the squishy, biological cores in mind. Most software around the world is priced on their inputs, not on the silicon it requires. Meaning even small incremental improvements to bio core productivity is worth large additional expenditures on silicon chips. And every year, the ratio grows greater in favor of the bio cores.



At least up until the point that we make them obsolete and welcome our AGI overlords! But nobody seems to know when or if that's going to happen, so best you deal in the economics of the present day, pick the most productive tool chain available to you, and bet that happy programmers will be the best bang for your buck.