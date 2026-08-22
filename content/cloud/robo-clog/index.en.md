---
title: "When AI Gets the Power to Gridlock a City"
date: 2026-04-01
authors: [vonng]
summary: >
  On the night of March 31, a large number of Apollo Go robotaxis in Wuhan failed at the same time. The real concern is not merely that autonomous driving failed, but that a centrally controlled, cloud-based architecture may amplify a single-vehicle failure into a city-scale systemic risk.
tags: [AI, Incident, Society]
---

> On the night of March 31, a large number of Apollo Go robotaxis in Wuhan failed at the same time. The real concern is not merely that autonomous driving failed, but that a centrally controlled, cloud-based architecture may amplify a single-vehicle failure into a city-scale systemic risk.

## What Happened in Wuhan Last Night

On the night of March 31, Baidu's Apollo Go robotaxi service—known in China as Luobo Kuaipao (萝卜快跑)—suffered a large-scale system failure in Wuhan, a major city in central China. According to a [report by Fast Technology](https://finance.eastmoney.com/a/202604013691391126.html), videos posted by drivers and passengers on social media showed multiple Apollo Go vehicles suddenly stopping in traffic that evening.

As of publication, Wuhan traffic police said their preliminary assessment was a system failure. All passengers had exited safely, no one was injured, and the exact cause remained under investigation. The technical analysis below is therefore an inference based on public information and common industry knowledge.

One passenger posted a video saying that the vehicle had stopped in the middle of the road. Its screen promised that staff would arrive within five minutes, but no one appeared after 20 minutes. The customer-service line connected for one second, then hung up.
Other social-media users reported Apollo Go vehicles stopped across the road network, creating risks of crashes and congestion. Dashcam footage from Wuhan's Second Ring Road—an urban expressway—showed at least three Apollo Go vehicles stopped in the fast lane while heading from the railway station toward Wanda Plaza in the Economic Development Zone. One had already been rear-ended.

A Wuhan traffic-police officer told the media:

> **"Apollo Go's system failed. It is the company's problem, affecting roughly a hundred vehicles. Passengers can press a button to open the door, but they cannot safely get out on the ring road. We rescued a lot of people today."**

"We rescued a lot of people today." This was not a police officer talking about a flood or an earthquake. He was talking about people who had taken a taxi. The official statement stressed that no one was injured, but the mere fact that large numbers of passengers were stranded on ring roads and elevated expressways is alarming enough.

Last night's incident came nowhere close to paralyzing the entire city. But it exposed a clear path to that outcome.

--------

## What Does a Large-Scale Simultaneous Failure Tell Us?

The key technical inference is this: **from the public information available so far, this looks less like failures in individual vehicles' perception or control systems and more like a systemic coupling problem between the fleet and the cloud.**

For the sake of discussion, autonomous-driving systems can be sketched as two broad architectural models:

**The first is onboard autonomy:** each vehicle carries a complete perception, planning, and control stack, with enough onboard compute to operate independently. Tesla FSD and Waymo take different technical approaches, but both emphasize closing the core driving loop onboard the vehicle. The cloud can collect telemetry, deliver OTA updates, and provide remote monitoring, but the vehicle's core driving capability does not depend on it. If the cloud goes down, the vehicle should at least remain capable of pulling over safely.

**The second is cloud-controlled fleet operation:** vehicle behavior is governed to a large extent by cloud-based dispatch and control systems. Route planning, job assignment, remote intervention, status monitoring, and perhaps even some driving decisions depend on real-time communication with the cloud.

Judging from last night's failure mode, Apollo Go's operating model appears **closer to the latter**. It is not merely "driverless"; it looks more like a cloud-managed platform for operating a driverless fleet.

Why draw that inference? Because **a large number of vehicles failing at once is itself evidence.** If the problem were local to individual driving systems—a defect in a particular sensor model, for example, or a bug in an onboard algorithm—we would expect failures to be **random, scattered, and gradual**. Different vehicles would encounter them at different times and under different road conditions. A large-scale simultaneous breakdown on the same evening would be unlikely.

There are, of course, other possible explanations for simultaneous failure: a buggy OTA software update pushed to the vehicles, a carrier's cell sites failing in the area, or a safety policy triggered across the fleet under some shared condition. Whatever the specific cause, however, each possibility points to the same conclusion: **the vehicles shared a critical dependency—a single point of failure.** When it failed, many vehicles could no longer operate normally.

That is the problem.

--------

## A Fleet in the Cloud, Roadblocks on the Ground

In a purely digital system, the cost of a single-point dependency can be tolerable. Your SaaS goes down, and users cannot reload a page. Your cloud database fails, and transactions are delayed for a few seconds. Once service returns, everything carries on, perhaps with an SLA credit. But when the system controls not pixels but **several tons of moving steel**, failure takes on an entirely different character.

A bad configuration push no longer produces an HTTP 500; it stops a fleet of vehicles on urban expressways. Your passenger does not see a "service temporarily unavailable" page; they are stranded in the fast lane of an elevated expressway, able to open the door but with nowhere safe to go, as traffic streams past at 80 km/h.

**A `NullPointerException` in your web app is a line in a log. In a driverless fleet, it is a roadblock, a trapped passenger, and kilometers of congestion on the Third Ring Road.**

Conventional taxis do not fail as a batch. A thousand drivers are a thousand independent nodes; one breakdown does not affect the rest. A tightly coupled driverless fleet is different. Its vehicles share the same core dependencies. When one of those dependencies fails, **every vehicle can become a roadblock at once**. This is not an ordinary traffic accident. It is a new kind of urban-infrastructure risk caused by flaws in software architecture.

It brings to mind an incident from 2022.

--------

## Didi's Cautionary Tale

In August 2022, the Chinese ride-hailing platform Didi ran a ["free rides from Xidan" promotion](https://www.ithome.com/0/634/977.htm) in Beijing. Thousands of ride-hailing cars converged on Xidan, a central shopping district, severely congesting the area. The traffic even [spread to nearby Fuyou Street](https://m.soundofhope.org/post/645617). Didi later admitted internally that the promotion had been badly planned.

One commenter observed at the time: "Didi can make any place congested whenever it wants." The fact that a single promotion could severely disrupt traffic in the center of the capital was itself unsettling.

Didi was also subjected to a [joint review by seven Chinese government agencies](https://www.cac.gov.cn/2021-07/02/c_1626811521011934.htm), then [fined roughly RMB 8 billion](https://www.cac.gov.cn/2022-07/21/c_1660021534306352.htm) by China's cyberspace regulator. The public debate focused on data security, but an [analysis by DeHeng Law Offices](https://www.dehenglaw.com/CN/tansuocontent/0008/022000/7.aspx?MID=0902) identified a deeper problem: once a company's data and capabilities reach sufficient scale, "as a profit-seeking organization, it will take on the character of a public institution ... If its 'power' is not constrained, the company will be able to affect the security and stability of the entire country."

Didi's "power," however, remained indirect. Its algorithms dispatched human drivers, but those drivers had free will. They could ignore an instruction, change lanes, or pull over. **A human being still stood between the platform and the physical world.**

Apollo Go removes that buffer. It does not "suggest" how a car should drive; it controls the car directly. When the system says stop, the vehicle stops. The passenger can only press a button to open the door, then discover they are standing in the fast lane of an elevated expressway.

**Didi's issue was "data is power." Apollo Go's is "control is power": direct, physical, non-negotiable control.**

--------

## The Path to Gridlock

In 2019, a team led by Georgia Tech physicist Peter Yunker published a [study](https://www.sciencedaily.com/releases/2019/07/190729111337.htm) in *Physical Review E*, using percolation theory to simulate what would happen if connected cars were disabled simultaneously:

**At rush hour, randomly stopping just 20% of the cars on the road would freeze a city's traffic completely.** Ten percent would be enough to prevent ambulances and fire engines from getting through. Those are conservative estimates that exclude spillover effects and public panic; in practice, the number required to cause gridlock could be [substantially lower](https://spectrum.ieee.org/hacking-gridlock).

Reports put the number of failed Apollo Go vehicles last night at "roughly a hundred." Against the millions of vehicles in Wuhan, that is negligible and nowhere near the 20% threshold for a citywide freeze. But urban traffic is not distributed uniformly. Media reports citing local traffic-management data put evening rush-hour volume on Wuhan's Third Ring Road—another orbital urban expressway—at about 22,000 vehicles, moving at only 11.3 km/h and already close to severe congestion. **On a saturated stretch of road, a few dozen vehicles stopping simultaneously in the fast lane can have a sharply amplified effect.**

This incident did not show us a citywide gridlock. It showed us a path to one. The study above examined a theoretical mechanism in which connected vehicles are disabled simultaneously; its thresholds cannot simply be mapped onto last night's incident in Wuhan. But it does establish one point: as driverless fleets grow, if an architectural flaw allows one failure to strand many vehicles at once, the number of disabled vehicles may one day reach that critical threshold.

Coincidentally, the researchers opened their paper with an imagined scene: *"In 2026, during rush hour, your autonomous car suddenly stops and blocks traffic. You climb out and see every street within view brought to a standstill..."* They chose 2026. It is now April 2026, and Wuhan has seen an unsettling echo of that scenario.

There is one difference: the paper assumed a cyberattack. There is currently no evidence that the real-world incident involved any external attack. But even an internal system failure can produce a similar outcome if the architecture contains a single-point dependency.

--------

## This Is Not a Technical Glitch; It Is an Architectural Choice

Let me make the logic explicit.

If every Apollo Go vehicle were autonomous in the full sense—with sufficient onboard compute, no reliance on the cloud for core driving decisions, and an independent ability to pull over safely—then, in theory, a mass stoppage like last night's should not happen so readily. Independent nodes should not fall over together this way.

The fact that the vehicles stopped in concert **shows at minimum that they were not independent at some critical point**. They shared a single-point dependency or a common failure mode that could be triggered across the fleet. Once it failed, many vehicles lost the ability to operate normally at the same time.

That is an architectural choice. Centralized control may be chosen for cost: onboard compute is expensive, while cloud scheduling is cheaper. Or it may be chosen for control: unified management makes the fleet easier to operate. But the price of that choice is that **the risk of a single-vehicle failure can more readily be amplified into a city-scale systemic risk.**

Consider an analogy: connecting every traffic light in a city to one central system, with no ability to degrade gracefully at the edge. While the system works, everything looks wonderful—central coordination, global optimization. When it fails, every traffic light loses control at once.

Anyone who has built distributed systems knows why that architecture is hard to trust in critical infrastructure. Power grids are segmented, banking systems are layered, and DNS has local caches. **Any system that can affect safety in the physical world must be able to operate independently or fail safely when its central node goes down.**

At least from the public information and what was observed at the scene, Apollo Go did not adequately demonstrate that capability last night.

--------

## Has Regulation Caught Up?

I do not oppose autonomous-driving technology. But its value is no excuse for failing to put the necessary governance in place. Operating an autonomous fleet means occupying and controlling urban transportation infrastructure. The regulatory standard should be no lower than it is for the electric grid, water, or gas—the lifeline systems of a city.

Nuclear power is valuable too. I am not saying an autonomous fleet poses the same hazards as a nuclear plant, but the two share one principle: **technology that affects public safety must not be deployed at scale until a regulatory framework is in place.** Allowing a company to build a nuclear plant in a city center without such a framework, then respond to an accident with "we will continue optimizing the technology," would plainly be absurd.

Several questions demand answers:

**Is the blast radius of a single system bounded?** Many vehicles stopping at once suggest inadequate fault isolation. Like an electric grid divided into sections, the fleet should be designed so that no single failure can reach every vehicle.

**Can each vehicle operate independently of the cloud?** If communications are lost, it must be able to pull over safely on its own rather than stop in the fast lane. That should be a mandatory condition of deployment approval.

**Does emergency-response capacity scale with fleet size?** A customer-service call that connects for one second and drops shows that the emergency system collapsed under a large-scale failure. If you put a fleet on the road, you need the capacity to handle that many simultaneous failures.

In March 2026, researchers also warned that, without controls, the robotaxi utopia promised by autonomous driving could instead become a permanent, high-tech traffic jam.

**We are handing the arteries of urban transportation to operators that, at minimum, have not yet demonstrated to the public that they have mature plans for a large-scale simultaneous failure. This is not merely a technical problem. It is a question of power and a question of responsibility.**

Today is April Fools' Day. Let us hope this was a warning serious enough to wake the industry up—not a preview of a larger disaster.
