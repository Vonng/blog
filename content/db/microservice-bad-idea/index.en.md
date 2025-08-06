---
title: Are Microservices a Stupid Idea?
date: 2023-05-07
hero: /hero/microservice.jpg
author: |
  [DHH](https://world.hey.com/dhh) | Translator: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat Article](https://mp.weixin.qq.com/s/mEmz8pviahEAWy1-SA8vcg)
summary: >
  Even Amazon, the SOA exemplar, thinks microservices and serverless suck. Are microservice architectures still a good idea?
  Amazon's Prime Video team published a very compelling case study explaining why they abandoned microservices and serverless architecture.
tags: [database]
---

Amazon's Prime Video team published a very compelling case study [2] explaining why they abandoned microservices and serverless architecture in favor of a monolithic architecture. This move saved them an astounding 90% in operational costs while also simplifying system complexity — a massive win.

But beyond praising their wise decision, I think there's an important insight here that applies to our entire industry:

> "Our initial solution was designed as a distributed system using serverless components... In theory, this would allow us to scale each service component independently. However, the way we used certain components caused us to hit hard scaling limits at around 5% of expected load."

"**In theory**" — this is a brilliant summary of the microservices frenzy that has ravaged the tech industry in recent years. Now the theoretical paper discussions finally have real-world conclusions: in practice, the concept of microservices is like siren songs, tempting you to add unnecessary complexity to systems, and serverless only makes things worse.

The funniest part of this story is that Amazon itself was the original exemplar and spokesman for Service-Oriented Architecture (SOA). Before microservices became popular, this organizational model was quite reasonable: at a crazy scale, using API calls for internal company communication beats coordinating cross-team meetings.

SOA made sense at Amazon's scale — no single team could know or understand all aspects needed to steer such a massive ship, and having teams collaborate through publicly published APIs was brilliant.

But like many "good ideas," **this pattern becomes extremely harmful when taken out of its original context and applied elsewhere**: especially when stuffed into single application architectures — which is exactly how people do microservices.

![](microservice-bad-idea-1.jpeg)

In many ways, microservices are a zombie architecture, a persistent thought virus: from the dark ages of J2EE (Remote Server Beans, anyone heard of those?), through the WS-Deathstar [3] nonsense, to the current forms of microservices and serverless — it keeps devouring brains and eroding people's intelligence.

But this third wave has finally peaked. I wrote a paean to "The Majestic Monolith [4]" back in 2016. Kelsey Hightower, the thought leader behind Kubernetes, also expressed this in his 2020 article "Monoliths are the Future [5]":

> "We're going to break apart the monolith and find the engineering discipline we never had before... Now people went from writing terrible code to building terrible platforms and infrastructure.
>
> People get caught up in the hot money and hype tied to these trendy buzzwords, because microservices brought tons of new overhead, hiring opportunities, and job positions — everything except actually being necessary for solving their problems."

![](microservice-bad-idea-2.png)

That's right — when you have a coherent single team and monolithic application, replacing method calls and module separation with network calls and service splits is an incredibly insane idea in almost all cases.

I'm glad to have beaten back this zombie-like stupid idea for what feels like the third time in memory. But we must stay vigilant, because we'll have to do this again sooner or later: some half-baked ideas will keep coming back no matter how many times you kill them. All you can do is recognize them when they resurrect and blast them to pieces with article shotguns.

> Effective complex systems invariably evolve from simple systems. The converse is also true: complex systems designed from scratch never work effectively.
>
> — John Gall, Systemantics (1975)

This article is by DHH, creator of Ruby on Rails and CTO of 37signals, translated by Vonng.

The original title was "Even Amazon can't make sense of serverless or microservices [1]", meaning "Even Amazon thinks microservices and serverless are bullshit."

[![](featured.jpg)](https://mp.weixin.qq.com/s/mEmz8pviahEAWy1-SA8vcg)

### References

`[1]` Even Amazon can't make sense of serverless or microservices: *https://world.hey.com/dhh/even-amazon-can-t-make-sense-of-serverless-or-microservices-59625580*
`[2]` Compelling case study: *https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90*
`[3]` WS-Deathstar: *https://www.flickr.com/photos/psd/1428661128/*
`[4]` The Majestic Monolith: *https://m.signalvnoise.com/the-majestic-monolith/*
`[5]` Monoliths are the Future: *https://changelog.com/posts/monoliths-are-the-future*