---
title: "Cloud-Exit High Availability Secret: Rejecting Complexity Masturbation"
hero: /hero/uptime.jpg
date: 2024-01-10
authors: ["dhh"]
summary: |
  Programmers are drawn to complexity like moths to flame. The more complex the system architecture diagram, the greater the intellectual masturbation high. Steadfast resistance to this behavior is a key reason for DHH's success in cloud-free availability.
tags: [Cloud-Exit]
---

We don't need Kubernetes masters or fancy new databases — programmers are drawn to complexity like moths to flame. The more complex the system architecture diagram, the greater the intellectual masturbation high. Our steadfast resistance to this behavior is a key reason for our success in cloud-free availability.

> Author: **David Heinemeier Hansson**, known as DHH, Co-founder & CTO of 37signals, Creator of Ruby on Rails, cloud exit advocate, practitioner, and pioneer. Frontrunner in fighting tech giant monopolies. [Hey Blog](https://world.hey.com/dhh)
>
> Translator: **Vonng (Feng Ruohang)**, Founder & CEO of PIGSTY. Author of [Pigsty](https://pigsty.io), PostgreSQL expert/evangelist. Host of WeChat public account "Illegal Plus Feng", cloud computing mudslide, database veteran.
>
> This article is translated from DHH's [blog post](https://world.hey.com/dhh/keeping-the-lights-on-while-leaving-the-cloud-be7c2d67)

-----------

## Keeping the Lights On While Leaving the Cloud

> [*Keeping the lights on while leaving the cloud*](https://world.hey.com/dhh/keeping-the-lights-on-while-leaving-the-cloud-be7c2d67)

For the ops team at [37signals](https://37signals.com/), 2023 was undoubtedly a challenging year. We migrated seven core applications from the cloud, including the email service [HEY](https://hey.com/) that was born in the cloud — which has extremely stringent availability requirements that our cloud exit process couldn't compromise. Fortunately, we succeeded. In 2023, HEY achieved a remarkable **99.99%** uptime!

This is critically important because if people can't access their email, they might miss flight check-ins, fail to complete time-sensitive transactions, or miss critical medical test results. We take this responsibility very seriously, so achieving this near-perfect four nines during a year that required completely transforming how HEY operates became a source of tremendous pride.

But HEY wasn't the only application receiving this meticulous operational treatment. In 2023, all our major applications achieved at least **99.99%** availability. This includes Highrise, Backpack, Campfire, and all versions of [Basecamp](https://basecamp.com/). We didn't encounter zero issues — but our team quickly resolved all problems, keeping total downtime for the entire year under **0.01%**.

No application better illustrates our ability to ensure application reliability and stability outside the cloud than Basecamp 2. This is the version of Basecamp we sold from 2012 to 2015, still serving thousands of users and generating millions in revenue. It has been running on our own hardware for years, and this is now the second consecutive year achieving an almost unbelievable **100%** availability — 365 days of zero downtime in 2023, continuing the glory of 2022.

I won't pretend that such excellent availability is effortless, because it's not. Achieving this is far from easy. We have a skilled and dedicated ops team that deserves high praise for their tremendous contributions to this goal. But it's also not rocket science!

A considerable portion of Basecamp 2's magic in achieving 100% availability for two consecutive years, and all other applications reaching 99.99% availability, comes from **our choice of simple, boring, fundamentally solid technology**. We use F5, Linux, KVM, Docker, MySQL, Redis, ElasticCache, and of course Ruby on Rails. Our tech stack is unassuming and straightforward, primarily because complexity is low — **we don't need Kubernetes masters or fancy databases and storage. Most of the time, you won't need them either.**

**But programmers are drawn to complexity like moths to flame. The more complex the system architecture diagram, the greater the intellectual masturbation high. Our steadfast resistance to this behavior is the fundamental reason for our victory in availability.**

I'm not talking about the technology needed to operate Netflix, Google, or Amazon. At that scale, you indeed encounter truly pioneering problems with no ready-made solutions to borrow from. But for the rest of us 99.99%, mimicking their imagination and cognition to model our own infrastructure is an alluring but deadly siren song.

To have good availability, you need not the cloud, but mature technology running on redundant hardware with proper backups configured, as always.

> Note: DHH saved nearly $10 million in high cloud costs. This article translates DHH's latest cloud exit progress. For the cloud exit backstory and complete process, refer to: "[Cloud-Exit Odyssey](https://blog.vonng.com/en/cloud//odyssey/)", "[Is It Time to Give Up on Cloud Computing?](https://blog.vonng.com/en/cloud//odyssey/)", and "[DHH Cloud-Exit FAQ](https://blog.vonng.com/en/cloud//cloud/-exit-faq/)".

--------------

## Translator's Commentary

DHH points out the best practice for maintaining good availability — **running humble, mature, foundational technology on redundant hardware**. Most of software's cost overhead isn't in the initial development phase, but in the ongoing maintenance phase. And **simplicity** is crucial for system maintainability.

Some programmers, out of **intellectual masturbation** or **job security** reasons, pile unnecessary additional complexity into architectural designs — such as throwing Kubernetes at everything regardless of scale and load appropriateness, or using glue code to wire together a bunch of flashy databases. Seeking "cool enough" things to satisfy personal value needs, rather than considering whether the problems to be solved actually need these dragon-slaying techniques.

![](featured.jpg)

> Rube Goldberg machine: "Accomplishing through extremely complex and circuitous methods what could actually or seemingly be done easily" — a form of intellectual masturbation through complexity.

Complexity slows everyone down and significantly increases maintenance costs. Making changes in complex systems carries greater risk of introducing bugs (such as the major failures described in "[From Cost-Reduction Jokes to Real Cost Reduction](https://blog.vonng.com/en/cloud//smile/)"). When complexity leads to maintenance difficulties, budgets and timelines typically overrun. When developers struggle to understand the system, hidden assumptions, unintended consequences, and unexpected interactions are more easily overlooked. Reducing complexity can dramatically improve software maintainability, so **simplicity** should be a key goal in building systems.

Not every company has Google's scale and scenarios, requiring starships to solve their unique problems. PostgreSQL + Go/Ruby/Python on bare metal/VMs or classic LAMP has taken countless companies all the way to IPO. Never forget that **designing for unneeded scale is wasted effort** — this is a form of **premature optimization** — and that is the root of all evil.

Using my personal experience as an example, during Tantan's early-to-mid stages with millions of daily active users, the tech stack remained very humble — applications written purely in Go, database using only PostgreSQL. At the scale of 2.5M TPS and 200TB of data, **single PostgreSQL selection** could stably and reliably support the business: beyond its primary OLTP role, it also served for quite a long time as cache, OLAP, batch processing, and even message queue. Eventually some moonlighting functions were gradually **separated** to dedicated components, but that was already at nearly 10 million daily active users, and in hindsight, the necessity of some of those new components is questionable.

Therefore, when we conduct architectural design and reviews, we might use the complexity perspective for additional scrutiny. For more discussion on complexity, please refer to the following articles:

[Should Databases Go into K8S?](https://blog.vonng.com/en/cloud//k8s-vs-db/)

[From Cost-Reduction Jokes to Real Cost Reduction](https://blog.vonng.com/en/cloud//smile/)

[Is Putting Databases in Docker a Good Idea?](https://blog.vonng.com/en/cloud//docker-vs-db/)

[Are Microservices a Stupid Idea?](https://blog.vonng.com/en/cloud//microservices/)

[Are Distributed Databases False Needs?](https://blog.vonng.com/en/cloud//distributed-db/)