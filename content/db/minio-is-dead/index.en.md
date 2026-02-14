---
title: MinIO is Dead
date: 2025-12-04
author: |
  [Ruohang Feng](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [Wechat](https://mp.weixin.qq.com/s/aBUwEMxZ_xKmHisaaT4uWw)
summary: >
  MinIO announces it is entering maintenance mode, the dragon-slayer has become the dragon – how MinIO transformed from an open-source S3 alternative to just another commercial software company
tags: [Database, MinIO, Open-Source]
---


December 3, 2025 was a day to mark in open-source software history. 
MinIO's team updated the project status on GitHub, announcing the MinIO open-source project was entering "**maintenance mode**." 
This basically declared the death of MinIO as an open-source project.

MinIO the company has finally completed its transformation from a dragon-slaying hero into the very dragon it once sought to slay.

![maintenance-mode.png](maintenance-mode.png)

------

## From Dragon-Slayer to Dragon

#### Democratization Era (2014–2019): The Apache of Object Storage

MinIO was founded in 2014 with a highly idealistic vision – to be "the Apache of object storage." 
In an era dominated by AWS S3, MinIO's ultra-lightweight design (a single static binary) 
and **100% S3 API compatibility** quickly won developers' hearts.

During this phase, MinIO was licensed under the liberal Apache 2.0 license, 
encouraging developers to integrate it into all kinds of applications. 
Its core pitch: **"turn any hardware into AWS S3."** This open strategy was wildly successful. 
MinIO claimed its Docker image had been pulled over **1 billion** times, making it the world's most widely deployed object storage service. 
At this point, MinIO was a darling of the cloud-native stack – the default storage backend in many Kubernetes setups.

#### License Weaponization (2019–2025): The AGPL War

The first major crack in community relations appeared around 2019–2021. 
MinIO announced it was changing its core license from Apache 2.0 to **GNU AGPLv3**.

The official explanation was that this move aimed to prevent cloud providers (like AWS, Azure) from "freeloading" the code and repackaging it as proprietary services — 
a common defensive tactic in open source. During this period, MinIO shifted from being a community guardian to an aggressive defender of its IP. 
In 2022, MinIO publicly accused Nutanix Objects of violating its license and **revoked Nutanix's right to use MinIO**; 
in 2023, MinIO sued high-performance filesystem vendor Weka on similar grounds. 
These legal actions, though legally contentious, sent a clear signal: **MinIO no longer welcomed commercial use without paying up.** 
This set the legal and psychological stage for the full lockdown that would come in 2025.

#### Control Plane Neutered (May 2025)

In May 2025, MinIO decided to strip the **MinIO Console** out of the community edition. 
The console was a critical GUI for bucket management, IAM, monitoring, and audit logging. 
After this removal, the open-source MinIO was left with only a basic "object browser" GUI – essentially just a file viewer/downloader.

Meanwhile, **key admin features** like policy management, site replication configuration, and lifecycle management were moved entirely into the commercial enterprise edition. 
This change downgraded the open-source MinIO from a full-featured storage management system into a mere data-plane component, robbing it of the control-plane capabilities needed to run as a standalone product in production.

#### Cutting Off Binary Distribution (Oct 2025)

On October 15, 2025 – right as a critical security vulnerability (CVE-2025-10-15T17-29-55Z / GHSA-jjjj-jwhf-8rgr) was disclosed – MinIO **stopped publishing** updated Docker images to Docker Hub and Quay.io. 
The timing of this move was highly strategic. By cutting off binaries during a major security incident, MinIO effectively used security as a bargaining chip.

This decision directly broke the automated deployment pipelines for countless users. Helm charts, Ansible playbooks, and Terraform scripts expecting `minio/minio` (or Bitnami's `minio`) image suddenly failed to find updates. 
Auto-scaling groups trying to pull new nodes hung due to missing images. For teams without a Go build environment or an internal container registry, MinIO instantly became unusable.

#### Maintenance Mode (Dec 2025)

On December 3, 2025, MinIO, Inc. officially updated its channels and GitHub repo to announce that the open-source project is now in "**maintenance mode**." 
The README stated that there will be no further feature additions or improvements, issues and PRs will no longer be reviewed, and even critical security fixes would be provided "as appropriate." 
No more RPM/DEB packages or Docker images will be released. Essentially, anyone needing updates or support is advised to switch to the **commercial** AIStor product.

![aistor.png](aistor.png)

------

## Technical Impact: Damage to the Open-Source Ecosystem

MinIO's move to maintenance mode dealt an immediate and far-reaching blow to many tech stacks.

#### Broken CI/CD Pipelines and an Automation Crisis

Thousands of Helm charts, Ansible playbooks, and Terraform scripts depend on the `minio/minio` (or Bitnami's `minio`) container image. 
With official images no longer published, third-party packagers like Bitnami — who can't get a stable upstream release — also had to stop updates.

- **Cascade effect:** Deployments in fresh environments started failing outright. Auto-scaling groups, upon launching new instances, would hang or error out when the MinIO image couldn't be pulled.
- **Cost of fixes:** Companies now have to rewrite their deployment scripts to point to a self-hosted image, and set up internal build pipelines to compile and package MinIO from source.

#### Security Vacuum: CVE Patches Go Private

The most lethal consequence of halting binary distribution is delayed security patches. In the October 2025 incident, for example, MinIO effectively **withheld the patched binaries** for the vulnerability.

- **Risk exposure:** Companies without dedicated security teams are forced to keep running older, vulnerable versions with known critical flaws.
- **Compliance nightmare:** For organizations under PCI-DSS, HIPAA, SOC2, etc., not being able to obtain vendor-signed security updates is a compliance disaster. Lacking official patches, they technically fall out of compliance.

#### Exponentially Higher Ops Complexity

Removing the UI wasn't just a hit to user experience – it increased operational burden. 
Tasks that used to be a few clicks in the Console (configuring bucket policies, setting user permissions) now require ops engineers to master the `mc` CLI or hand-craft complex JSON policy docs. 
This raises the skill floor and makes MinIO far less friendly as a lightweight internal tool.

------

## Underlying Reasons: Pressure from Capital and Commercialization

The driving force behind MinIO's decisions is the logic of venture capital. By 2025, MinIO had raised a total of **$126 million** in funding. 
The most significant was a $103 million Series B in January 2022 led by Intel Capital, SoftBank Vision Fund II, and General Catalyst, which crowned MinIO a unicorn (valued over $1 billion).

In VC terms, a $1B valuation means the company must show a clear path to IPO — typically demanding $100M+ in Annual Recurring Revenue (ARR) and rapid growth. 
In Feb 2025, MinIO announced its ARR had grown **149%** over the past two years [businesswire.com](https://www.businesswire.com/news/home/20251112590444/en/Ran-Kurup-Joins-MinIO-to-Accelerate-Corporate-Strategic-Growth). 
Impressive growth, but to live up to a sky-high valuation, organic conversion alone wasn't enough.

**Cutting off the free open-source offering is the most direct way to force a huge user base into paid customers.**

In 2025, MinIO underwent a full rebrand and launched "MinIO **AIStor**," styling itself as "the data backbone for enterprise AI." 
Management recognized that general-purpose object storage (for backups, file servers, etc.) was a red-ocean market with thin margins, 
whereas generative AI's appetite for high-throughput data (the exascale AI era) promised the next big surge. 
By tuning its product for AI workloads and focusing on Fortune 500 enterprises [linkedin.com](https://www.linkedin.com/posts/efrieberg_very-excited-to-share-that-minio-has-been-activity-7397305169798963200-mKCI), 
**MinIO essentially decided to cut loose its low-value open-source user base**. 
The move to maintenance mode signaled MinIO's official pivot from a broad open-source project into a vertical, high-end AI software vendor.

MinIO isn't a garage hobby project by a few geeks anymore; it's a company that took **$126M** in VC and is valued at **over $1B**. 
Backed by **Intel Capital** and **SoftBank**, once you take that money, your boss is no longer the users — it's the investors. 
And what do investors want? **ARR**, **growth**, **IPO**. You tell them, "We have a billion Docker pulls!" and they'll ask, "How many dimes did those pulls pay us?"

The reality is brutal. To the VCs, those small businesses and individual devs using free MinIO are **low-value assets**. 
They open issues and ask for support — consuming expensive engineer time, bandwidth, and servers — yet **will never convert to paying customers**. 
MinIO's leadership knows their real cash cows are the Fortune 500 firms doing **generative AI**. 
The ones training GPT models or running self-driving pipelines need **AIStor**, ultra-high performance, and 24/7 enterprise SLAs.

So flipping the project into "maintenance mode" is essentially an **asset carve-out**. 
MinIO is cutting away the "dead weight" (free users) and concentrating on the milkable "cash cows" (enterprise AI clients). 
In business strategy this is called **focus**. To the investors, it's being **responsible**.
But from the perspective of open source, it's simply **betrayal**.

------

## Personal Reflections

I started using MinIO around 2018 (back when it was Apache-licensed). 
We built a few multi-petabyte object storage clusters for videos, images, backups — 
probably one of the largest MinIO deployments in China at the time. 
I wrote deployment/monitoring playbooks for MinIO (still open-sourced in [Pigsty](https://pigsty.io/docs/minio)).

As an open-source startup founder, I *can* understand the motivation behind these moves. But as an open-source contributor and user — 
I also know many folks right now have one phrase in their minds: **"I have never seen such shamelessness."**

An open-source license isn't a shackle, but it is a **social contract**. Developers contribute code, users contribute testing, feedback, and reputation; 
together, they make a project successful. MinIO enjoyed a decade of community goodwill and parlayed the bragging rights of "#1 in global downloads" into venture funding. 
Then it turned around and told the very users who propped it up: *"You free-riders, get lost."* This kind of move breaks the fundamental trust that open source is built on.

This "bait and switch" tactic is even more nauseating than a crypto rug pull. A rug pull only takes your money — 
MinIO is pulling the rug out from under the tech stacks of thousands of companies. 
Adopting a technology isn't just picking up a binary; it's buying into an ecosystem and a design philosophy. 
They got everyone onboard, let the switching costs pile up sky-high, and then suddenly kicked away the ladder. 
In fact, as open-source expert Tison thoroughly discussed in his article [*The Bait-and-Switch Open-Source Strategy*](https://mp.weixin.qq.com/s/HsgoUoBzsyXSmDfV00DlgQ), the core issue with this model is **deception**. 

MinIO betrayed the community, so the community may abandon it as well. 
Alternatives like **Garage**, **SeaweedFS**, or the new **RustFS** are ready to step in.

If I have to sum up my feelings, I'd borrow a line from *The Hitchhiker's Guide to the Galaxy*: 

—— **"So long, and thanks for all the fish."**

> 2026-02-14 Update: [MinIO's official repo has been fully archived and is no longer maintained](/db/minio-resurrect).
> Besides, I've personally maintained an oss fork of minio: [`pgsty/minio`](https://github.com/pgsty/minio) / Docs: [https://silo.pigsty.io](https://silo.pigsty.io).
> Which based on the last upstream version 2025-12-03 with restored console capabilities.