---
title: "Drones Took Out Three AWS AZ: Into the Era of Bombable Data Centers"
date: 2026-03-03
author: vonng
summary: >
  On March 1, 2026, Iranian drones reportedly hit AWS facilities in the UAE and Bahrain. If the reporting is accurate, this may be the first public case of a hyperscale cloud provider suffering direct military damage to data-center infrastructure.
tags: [Cloud Exit, AWS, Cloud Outage]
---

On March 1, 2026, Iranian drones reportedly hit AWS facilities in the UAE and Bahrain. If the public reporting is accurate, this may be the first time a hyperscale cloud provider has suffered direct military damage to physical data-center infrastructure.

## What happened?

Following an escalation in the Middle East, Iran launched drone and missile strikes against multiple targets in the UAE and Bahrain, including assets linked to U.S. presence in the region.

In that wave, AWS facilities in the UAE and Bahrain were reportedly hit directly. Not a power failure. Not a fiber cut. Not an HVAC failure. A physical strike on the building itself, followed by fire and structural damage.

![AWS facility after the reported strike](featured.webp)

AWS initially described the event in vague terms, saying that "objects" had struck the facility and caused sparks and fire. Only later did it explicitly acknowledge drone strikes.

## How much of the region was affected?

AWS operates three regions in the broader Middle East, for a total of **nine availability zones**:

![AWS Middle East regions and AZ distribution](regions.webp)

According to public reports, the damage looked like this:

![Damage to AWS availability zones in the Middle East](damage.webp)

Three out of nine AZs were affected overall, or about **33%** of the regional footprint. The UAE region was hit hardest: two of its three AZs were knocked out, which meant that carefully designed multi-AZ redundancy suddenly looked much less reassuring.

## How large was the blast radius?

The UAE region reportedly saw **38 AWS services** impacted. Bahrain reportedly saw **46 services** affected, including outages tied to power and network interruptions.

![Service impact across the affected AWS regions](impact.webp)

The service counts overlap and should not simply be summed, but the operational message was clear: this was not a narrow incident. Core services such as EC2, Lambda, EKS, VPC, RDS, CloudFormation, and S3 were all in the blast radius.

AWS reportedly advised affected customers to restore from remote backups into other regions, ideally in Europe. That is about as close as a cloud vendor can get to saying: do not expect a quick return to normal.

As of March 3, the directly hit `mec1-az2` remained in a **physical offline** state while fire and safety teams still restricted re-entry.

![AWS status showing mec1-az2 as physically offline](offline.webp)

![AWS cross-region recovery guidance](recovery.webp)

## What about AI services?

The same weekend, several major AI services experienced turbulence. Claude and Claude Code suffered a major global incident on March 2. Gemini and GPT also showed signs of instability.

That said, the public evidence does **not** establish a direct causal line from the AWS Middle East damage to those incidents. At most, it shows that multiple forms of fragility surfaced during the same weekend.

## The real lesson

Technically, there is not much to debate. If the physical layer is destroyed, software architecture alone cannot save you. Multi-AZ, multi-region, automatic failover: none of those patterns were designed around drones hitting buildings.

The deeper lesson is that data-center site selection has gained a new variable:

**Can this place get bombed?**

Cloud providers have always optimized for power, networking, climate, regulation, and talent. Going forward, geopolitics and military risk belong on the same checklist.

To AWS's credit, region isolation itself appears to have held. The event did not globally collapse AWS control planes. That reinforces an old truth: real resilience is not same-city dual active or even cross-AZ. It is **cross-region, and sometimes cross-cloud**.

## Closing thought

For decades, the tech industry quietly assumed that data centers were civilian infrastructure and would remain outside the battlefield. That assumption did not survive March 1, 2026.

Future architecture reviews may need to ask a question that once sounded absurd:

> What if this region gets bombed?

That is no longer a joke question.
