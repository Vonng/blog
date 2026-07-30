---
title: "PGConf.Dev 2026 Opens Today in Vancouver"
linkTitle: "PGConf.Dev 2026 Opens"
date: 2026-05-19
author: Ruohang Feng
summary: >
  PGConf.Dev 2026 opens in Vancouver as the PostgreSQL project marks its 30th anniversary. I will also be speaking on Extensions for Everyone.
tags: [PostgreSQL, PG Ecosystem, Conference]
---

On May 19, Vancouver time, [PGConf.Dev 2026](https://2026.pgconf.dev/) officially gets underway. This year's venue is Simon Fraser University's downtown campus, SFU Vancouver Harbour Centre. The conference has returned to Vancouver, host city of the inaugural PGConf.Dev.

PGConf.Dev is the global PostgreSQL developer conference and the successor to PGCon. It is one of the year's most important gatherings for core developers, extension authors, and community organizers. This year also marks the **30th anniversary of the PostgreSQL project**, and the community has organized a number of events around the milestone.

Today's program focuses more on the community, working groups, and open discussions. On May 20 and 21, the main conference program will run across three parallel rooms, covering everything from core patches, query optimization, and logical replication to extensions, the broader ecosystem, and the community itself. As usual, I am still finishing my slides and speaker notes. Hopefully I can leave an impression on the people in the room—or at least keep them awake.


## My Talk: Extensions for Everyone

I have one full-length conference talk this year: **Extensions for Everyone**, scheduled for **Wednesday, May 20, 4:00–4:25 p.m. Vancouver time, in the Canfor room (1600)**.

The subject is straightforward. As a Chinese developer who has spent years working on PostgreSQL extension distribution in the trenches, I want to talk about the problems I have seen and the lessons I have learned: the real challenges facing the extension ecosystem today, why distribution is so difficult, where cross-distribution packaging gets stuck, and where the community could take the ecosystem next.

I will try to give a systematic account of the experience I have accumulated while building Pigsty, PGEXT.CLOUD, and the `pig` CLI.


## Chinese Vendors on This Stage

Among the Chinese vendors attending this year are old friends from HighGo / IvorySQL. Vancouver-based **Grant Zhou** and **Carry Huang** are both familiar faces. More key members of the HighGo / IvorySQL team had also planned to attend, but visa issues ultimately prevented some of them from making the trip.

HighGo's participation and mine have followed parallel paths through the three editions of PGConf.Dev:

- **At the first conference**, we were simply attendees, there mainly to experience the event.
- **At the second**, Grant and I were each selected for a five-minute lightning talk, giving us our first chance to speak at the conference.
- **This year**, both of us have moved up to full 25-minute sessions—and, by an amusing coincidence, we are speaking in the same time slot.

Chinese voices did not appear on this stage overnight. We got here one step at a time.


## Two Full-Length Talks from China

The current official program includes two full-length talks by Chinese speakers, neatly spanning two dimensions: products and the ecosystem on one hand, and bridges between communities on the other.

### Extensions for Everyone

**Ruohang Feng**<br>
**Wednesday, May 20, 4:00–4:25 p.m. Vancouver time, Canfor room (1600)**

I will share a Chinese developer's firsthand perspective on PostgreSQL extension distribution and ecosystem building. More specifically, I will discuss how an extension goes from source code to a production-grade package that can be installed, upgraded, and operated—and what that process means for the PostgreSQL ecosystem.

### The Missing Link: Connecting Tens of Thousands of Chinese Users to the PostgreSQL Core

**Grant Zhou**<br>
**Wednesday, May 20, 4:00–4:25 p.m. Vancouver time, Fletcher room (1900)**

Grant will discuss the “missing link” between tens of thousands of PostgreSQL users in China and the global core community: how Chinese users and contributors can engage more smoothly with upstream, and how the community can better understand and respond to their needs.

This subject has long been underestimated, but it is becoming increasingly important.

HighGo architect **Chao Li** also previously had a talk accepted: **Learning PostgreSQL Hacking Fast: Lessons and Mistakes from a Newcomer**. He had planned to share his journey from PostgreSQL beginner to contributing substantive patches upstream, including the mistakes and detours along the way.

Unfortunately, his visa was not approved in time, so he could not make the trip. The conference website no longer lists the talk. The Fletcher room (1900) slot originally assigned to it has been replaced by Masahiko Sawada's **Implementing DDL Deparsing and DDL Replication**. A thematically similar talk about a new contributor's growth, **My Journey into PostgreSQL Development**, will take place in the Labatt room (1700).


## The Conference Program

This year's program covers a broad range of subjects, with a somewhat tighter pace than in previous years:

- **Tuesday, May 19**: Opening day, devoted mainly to community sessions, working-group discussions, and some internal or closed-door meetings, including the Committers Meeting and Security Team meetings. This year, several major topics that previously began as half-day blocks have been divided into smaller sessions, allowing registered attendees to join the ones that interest them.
- **Wednesday, May 20, through Thursday, May 21**: Two days of the main program, with three rooms running in parallel. Topics range from core patches, query optimization, and logical replication to extensions, the ecosystem, and the community.
- **Friday, May 22**: The traditional Unconference Day, with the agenda proposed and voted on by attendees that morning.
- **Wednesday evening**: The **30 Years of PostgreSQL Retrospective**, featuring Bruce Momjian, Tom Lane, Jan Wieck, Vadim Mikheev, and other central figures looking back on PostgreSQL's first 30 years together. Miss a gathering like this, and it may be a long time before the same group comes together again.


That is the broad outline. I probably will not have much free time once the conference gets going, but I will try to share some of the interesting moments here: talks, hallway conversations, and scenes worth remembering.

If you are also in Vancouver, come find me in the Canfor room—**Wednesday, May 20, at 4:00 p.m., for the extension ecosystem talk. See you there.**

Incidentally, after May 23 I plan to take a road trip through Banff and Jasper for a week or two. I drove the route two years ago, so I know it reasonably well. If you are nearby and planning a road trip around the same time, perhaps we can join forces. Haha.
