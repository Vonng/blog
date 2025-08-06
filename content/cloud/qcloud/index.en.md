---
title: What Can We Learn from Tencent Cloud's Major Outage?
date: 2024-04-14
author: |
  [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Tencent Cloud's epic global outage after Double 11 set industry records. How should we evaluate and view this failure, and what lessons can we learn from it?
tags: [CloudExit,TencentCloud,CloudOutage]
---

Eight days after the outage, Tencent Cloud published a [**postmortem report**](https://mp.weixin.qq.com/s/2e2ovuwDrmwlu-vW0cKqcA) for the April 8th major outage. I think this is a good thing, because Alibaba Cloud's [Double 11 major outage](https://mp.weixin.qq.com/s/cTge3xOlIQCALQc8Mi-P8w) official postmortem is still overdue. If public cloud vendors want to truly become **providers of water and electricity-like public infrastructure**, they need to take responsibility and accept public oversight—cloud vendors have an obligation to disclose their outage causes and propose concrete reliability improvement plans and measures.

So let's examine this postmortem report, see what information it contains, and what lessons we can learn from it.

- [What are the facts?](#what-are-the-facts)
- [What are the causes?](#what-are-the-causes)
- [What is the impact?](#what-is-the-impact)
- [Comments and opinions?](#comments-and-opinions)
- [What can we learn?](#what-can-we-learn)

-------------------

## What are the facts?

According to Tencent Cloud's official postmortem report (the "authoritative facts" published officially):

1. 15:23, detected the outage, immediately executed service recovery while investigating causes;
2. 15:47, found that rollback versions couldn't fully restore services, further located the problem;
3. 15:57, identified root cause as configuration data errors, urgently designed data repair solution;
4. 16:02, performed data repair work across all regions, API services recovering region by region;
5. 16:05, observed that API services in all regions except Shanghai had recovered, further investigated Shanghai region recovery issues;
6. 16:25, identified API circular dependency issues in Shanghai's technical components, decided to restore through traffic scheduling to other regions;
7. 16:45, observed Shanghai region recovery, API and API-dependent PaaS services completely restored, but console traffic surged, expanded capacity by 9x;
8. 16:50, request volume gradually returned to normal levels, business running stably, console services fully restored;
9. 17:45, continuous observation for one hour, no issues found, handled according to plan completion.

The postmortem report attributes the cause to: **insufficient forward compatibility consideration and inadequate configuration data gradual rollout mechanisms in the new cloud API service version**

> During this API upgrade process, due to interface protocol changes in the new version, after deploying the new version backend, data processing logic for old version frontend data was abnormal, generating erroneous configuration data. Due to insufficient gradual rollout mechanisms, abnormal data rapidly spread to all network regions, causing overall API usage anomalies.
>
> After the outage, following standard rollback procedures, both service backend and configuration data were rolled back to old versions, and API backend services were restarted. However, since the container platform hosting API services also depended on API services for scheduling capabilities, circular dependency occurred, preventing services from automatically starting. Only through manual operational startup could API services restart, completing the entire outage recovery.

There's a questionable point in this postmortem report: the report attributes the outage to insufficient forward compatibility consideration. **Forward Compatibility** means old version code can use data produced by new version code. If management rollback to old version couldn't read dirty data produced by new version—that would indeed be a forward compatibility issue. But in the explanation below: new version code didn't handle old version data well—this is a typical **Backward Compatibility** problem. For a ToB service product, I think this kind of precision issue is problematic.

## What are the causes?

As a customer, I also obtained privately circulated outage postmortem process before this, a high-confidence inside source:

1. 15:25 Platform monitoring detected cloud API process failure alerts, engineers immediately intervened for analysis;
2. 15:36 Investigation found anomalies concentrated in cloud API production version, old version running normally, began rollback operations;
3. 15:47 Official website console cluster rollback completed, confirmed recovery through monitoring;
4. 15:50 Began rolling back non-console clusters;
5. 15:57 Identified root cause as erroneous data in configuration system;
6. 16:02 Deleted erroneous configuration data, regional clusters began automatic recovery;
7. 16:05 Due to historical configuration irregularities, Shanghai cluster couldn't quickly recover through rollback, decided to use traffic scheduling to restore Shanghai cluster;
8. 16:40 Shanghai cluster traffic fully switched to other regional clusters;
9. 16:45 Through observation and production monitoring, confirmed Shanghai cluster recovery.

The officially published version is basically consistent with the privately circulated version from days earlier on key points, just that the privately circulated version more specifically pointed out the root cause: **Compared to old version, production version newly introduced logic had bugs with empty dictionary configuration data compatibility, triggering bug logic in data reading scenarios, causing cloud API service process abnormal crashes**.

Based on these two postmortem information sources, we can confirm this was an outage caused by **human error**, not by natural disasters (hardware failure, data center power/network outages). We can basically **infer** the outage process occurred in two stages—two sub-problems.

The first problem was management API not maintaining good bidirectional compatibility—new management API crashed due to empty dictionaries in old configuration data. This reflects a series of software engineering problems—basic skills handling empty objects, exception handling logic, test coverage, deployment gradual rollout processes.

The second problem was circular dependency (container platform and management API) preventing automatic system startup, requiring manual operational intervention for Bootstrap. This reflects architectural design problems, and—**Tencent Cloud didn't learn the core lesson from Alibaba Cloud's major outage last year**.

-------------------

## What is the impact?

In the postmortem report, Tencent Cloud used lengthy descriptions of outage impact, explaining differences between control plane and data plane outages. Used some hotel front desk analogies. Similar outages already appeared in Alibaba Cloud's Double 11 major outage last year—control plane down, data plane normal. In "[What We Can Learn from Alibaba Cloud's Epic Outage](https://mp.weixin.qq.com/s/OIlR0rolEQff9YfCpj3wIQ)," we also analyzed that control plane outages indeed won't affect continued use of existing pure IaaS resources. But will affect cloud vendors' core services—for example, object storage is called COS on Tencent Cloud.

**Object storage COS is really too important**, arguably cloud computing's "defining service," perhaps the only service achieving basic consensus standards across all clouds. Cloud vendors' various "upper layer" services more or less directly/indirectly depend on COS. For example, CVM/RDS can run, but CVM snapshots and RDS backups obviously deeply depend on COS, CDN origin pulling depends on COS, various service logs often also write to COS**. So any outages involving basic services shouldn't be glossed over casually**.

Of course, most infuriating is actually Tencent Cloud's arrogant attitude—as a Tencent Cloud user myself, I submitted a ticket to test whether cloud SLA really works—facts proved: **no compensation without claims, claimed but denied can also avoid compensation—this SLA is indeed like toilet paper.** "[Are Cloud SLAs Placebo or Toilet Paper Contracts](https://mp.weixin.qq.com/s/mgkOybNeEH3LO0gRa1rQBQ)"

-------------------

## Comments and Opinions

Elon Musk's Twitter X and DHH's 37 Signal [saved tens of millions real money through cloud exit](/cloud/exit/), creating cost reduction "miracles," making cloud exit a trend. Cloud users hesitate over bills whether to exit cloud, non-cloud users are even more conflicted.

Against this background, domestic cloud leader Alibaba Cloud first experienced epic major outage, followed by Tencent Cloud's global control plane outage again—undoubtedly heavy blows to hesitant observers' confidence. If Alibaba Cloud's major outage was a **turning point-level landmark event** for public clouds, then Tencent Cloud's major outage again confirmed this trajectory's direction.

This outage again reveals key infrastructure's enormous risks—large numbers of network services relying on public clouds **lack most basic autonomous control** capabilities: when outages occur, they have no self-rescue abilities beyond waiting for death. It also reflects **monopolistic centralized infrastructure fragility**: the internet, this **decentralized** world wonder, now mainly runs on servers owned by a few large companies/cloud/ vendors—certain cloud vendors themselves become the biggest business single points of failure, not the internet's original design intent!

According to Heinrich's Law, behind one serious accident are dozens of minor incidents, hundreds of near-miss precursors, and thousands of accident hazards. Such accidents are absolutely fatal blows to Tencent Cloud's brand image, even **seriously damaging the entire industry's reputation**. After Cloudflare's control plane outage early this month, the CEO immediately wrote detailed [post-incident analysis](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/), recovering some reputation. Tencent Cloud's postmortem report this time can't be called timely, but at least better than Alibaba Cloud's cover-ups.

Through outage postmortems, proposing improvement measures, letting users see improvement attitudes—very important for user confidence. Doing outage postmortems might expose more amateur hour embarrassments—I won't retract my "amateur hour" assessment. But importantly—technical/management incompetence can be improved, but arrogant service attitudes are incurable.

If public cloud vendors want to truly become **providers of water and electricity-like public infrastructure**, they need to take responsibility and dare accept public and user oversight. In "[Tencent Cloud: Face-losing Amateur Hour](https://mp.weixin.qq.com/s/PgduTGIvWSUgHZhVfnb7Bg)" and "[Are Cloud SLAs Placebo or Toilet Paper Contracts](https://mp.weixin.qq.com/s/mgkOybNeEH3LO0gRa1rQBQ)," I pointed out Tencent Cloud's problems facing outages—untimely, inaccurate, non-transparent outage information release. On this point, I'm gratified to see in postmortem improvement measures that Tencent Cloud can acknowledge these problems and commit to improvements. But I cannot forgive—Tencent Cloud choosing to censor and silence articles on WeChat public accounts.

-------------------

## What can we learn?

Past cannot be retained, gone cannot be pursued. More important than mourning irretrievable losses is learning lessons from losses—even better if we can learn from others' losses. So, what can we learn from Tencent Cloud's epic outage?

-------------------

**Don't put all eggs in one basket**, prepare Plan B. For example, business domain resolution must add a CNAME layer, with CNAME domains using different service providers' resolution services. This intermediate layer is very important for global cloud vendor outages like Alibaba Cloud and Tencent Cloud—using another DNS provider at least gives you a choice to cut traffic elsewhere, rather than sitting helplessly in front of screens waiting for death with no self-rescue capability.

-------------------

**Carefully depend on things requiring cloud infrastructure**:

Cloud APIs are cloud service foundations—everyone expects them to always work normally. However, the more people feel things can't possibly fail, the more devastating when they actually do fail. If unnecessary, don't add entities. More dependencies mean more failure points, lower reliability: just as in this outage, CVM/RDS using their own authentication mechanisms weren't directly impacted. Deep use of cloud vendor AK/SK/IAM not only locks you into vendor lock-in, but exposes you to public infrastructure single-point risks.

My friend/opponent, public cloud advocate Swedish Ma and his friend AK Boss, always advocated using IAM/RAM for access control and deep utilization of cloud infrastructure. But after these two outages, Ma's exact words were:

> "I've always advocated everyone use IAM for access control, but both cloud providers had major outages, slapping my face. Whether PR or SRE, cloud vendors are using actual actions to prove to customers: '*Don't listen to Ma, if you use his approach, I'll make your systems die*'."

---------------

**Use cloud services carefully, prioritize pure resources**. In this outage, **cloud services** were affected, but **cloud resources** remained available. Pure **resources** like CVM/cloud/ disks, and RDS simply using these two, can continue running unaffected by control plane outages. Basic cloud resources (CVM/cloud/ disks) are the **greatest common denominator** of all cloud vendors' services. Using only resources helps users choose optimally between different public clouds and local self-building. However, it's hard to imagine not using object storage on public clouds—self-building object storage services with MinIO on CVM and astronomical cloud disks isn't a truly viable option. This involves public cloud business model core secrets: [cheap S3 for customer acquisition](/cloud/s3), [astronomical EBS pig-butchering](/cloud/ebs/).

-------------------

**Self-building is the ultimate path to mastering your own destiny**: If users want to truly control their destinies, they'll probably eventually walk the self-building path. Internet pioneers built these services from scratch, and doing it now would only be easier: IDC 2.0 solves hardware resource problems, open source alternatives solve software problems, mass layoffs released experts solving manpower problems. Short-circuiting public cloud middlemen, directly cooperating with IDCs is obviously more economical. For users with some scale, [money saved from cloud exit](/cloud/finops/) can hire several senior SREs from big companies with surplus. More importantly, when your own people have problems, you can reward/punish/motivate improvements, but when cloud has problems, can they compensate you with a few cents worth of coupons?

-------------------

**Clarify that cloud vendor SLAs are marketing tools, not performance commitments**

In the cloud computing world, [**Service Level Agreements**](/cloud/sla/) (SLAs) were once viewed as cloud vendors' promises of service quality. However, when we deeply study these agreements composed of multiple 9s, we find they can't "cover" as expected. Rather than SLAs being user compensation, SLAs are "punishment" for cloud vendors when service quality doesn't meet standards. Compared to experts who might lose bonuses and jobs due to outages, SLA punishment for cloud vendors is painless, more like self-penalty of three drinks. If punishment is meaningless, cloud vendors have no motivation to provide better service quality. So SLAs aren't insurance policies covering user losses. In worst cases, they're mute losses blocking substantial recourse; in best cases, they're placebo providing emotional value.