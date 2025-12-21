---
title: "OpenAI Global Outage Postmortem: K8S Circular Dependencies"
date: 2024-12-14
author: |
  [Original](https://status.openai.com/incidents/ctrsv3lwd797) Translated by: [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Even trillion-dollar unicorns can be a house of cards when operating outside their core expertise.
tags: [Cloud-Outage]
---

On December 11th, OpenAI experienced a global service outage affecting ChatGPT, API, Sora, Playground, and Labs. The outage lasted from 3:16 PM to 7:38 PM PT, spanning over four hours with significant impact.

According to OpenAI's [incident report](https://status.openai.com/incidents/ctrsv3lwd797) published afterward, the root cause was a newly deployed monitoring service that overwhelmed the Kubernetes control plane. The control plane failure then prevented direct rollback, amplifying the impact and causing extended unavailability.

This incident bears striking similarity to last year's [Alibaba-Cloud epic global outage](https://mp.weixin.qq.com/s/OIlR0rolEQff9YfCpj3wIQ). Both involved global control plane failures caused by circular dependencies (plus insufficient testing/deployment gradual rollout). The difference: Alibaba's was between OSS and IAM, OpenAI's was between DNS and K8S.

--------

Circular dependencies are architectural poison—like placing dynamite in your infrastructure foundation, easily triggered by temporary or sporadic failures. This incident serves as another wake-up call. The root cause goes deeper than testing/gradual rollout issues—it's architectural juggling:

Kubernetes officially recommends [maximum cluster size of 5,000 nodes](https://kubernetes.io/docs/setup/best-practices/cluster-large/), yet I clearly remember OpenAI's boastful article: "[How We Scaled Kubernetes to 7,500 Nodes by Removing One Component](https://newsletter.betterstack.com/p/how-openai-scaled-kubernetes-to-7500)." Not only did they eliminate redundancy, they pushed 50% beyond recommended limits. Ultimately, they did indeed crash due to cluster scale issues.

--------

OpenAI is the AI industry's darling, with undeniable product strength and popularity. This cannot mask their infrastructure weaknesses—reliable infrastructure is genuinely difficult, which is why companies like AWS and DataDog are printing money.

OpenAI also had a major outage last year with [PostgreSQL database and pgBouncer connection pooling](https://community.openai.com/t/postmortem-feb-20-2023-openai-suffered-a-major-db-outage/73068). Their infrastructure reliability track record over these two years hasn't been impressive. This incident again proves that even trillion-dollar unicorns can be a house of cards when operating outside their core expertise.

--------

#### **Further Reading**

[What We Can Learn from Alibaba-Cloud's Epic Failure](https://mp.weixin.qq.com/s/OIlR0rolEQff9YfCpj3wIQ)

[Tencent Cloud: Face-losing Amateur Hour](https://mp.weixin.qq.com/s/PgduTGIvWSUgHZhVfnb7Bg)

[Dark Forest: Bankrupting AWS Bills with Just an S3 Bucket Name](https://mp.weixin.qq.com/s/35ScjtPjC1GNGKaSArJhcA)

[Unparalleled Database Deletion: Google Cloud Nuked an Entire Fund Account](https://mp.weixin.qq.com/s/eH5HBbL7cQhjQY8rm1gFLQ)

[Global Windows Blue Screen: Both Sides Are Amateur Operations](https://mp.weixin.qq.com/s/s7i7bSYzNY8mrcpfkHPjOg)

[Alibaba-Cloud: Death of High Availability Disaster Recovery Myth](https://mp.weixin.qq.com/s/rXwEayprvDKCgba4m-naoQ)

[Amateur Hour Show: Alibaba-Cloud RDS Failure Chronicle](https://mp.weixin.qq.com/s/kOIw8uPjZUZ0-QisC1TBOA)

[The Amateur Operations Behind Internet Outages](https://mp.weixin.qq.com/s/OxhhJ4U80xqsnytC4l9lRg)

[Should Databases Run in Kubernetes?](https://mp.weixin.qq.com/s/4a8Qy4O80xqsnytC4l9lRg)

--------

## Original Incident-Report

### Issues with API, ChatGPT, and Sora

https://status.openai.com/incidents/ctrsv3lwd797

#### OpenAI Incident-Report

This document provides a detailed account of an incident that occurred on December 11, 2024, during which all OpenAI services experienced significant outages. The root cause was the deployment of a new telemetry service that unexpectedly overwhelmed the Kubernetes control plane, triggering cascading failures across critical systems. We'll dive into the fundamental causes, outline our response steps, and share the improvements we're implementing to prevent similar incidents.

------

### Impact

Between 3:16 PM and 7:38 PM PST on December 11, 2024, all OpenAI services experienced significant degradation or complete unavailability. This incident originated from a new telemetry service configuration rollout across all clusters and was **not** caused by security vulnerabilities or recent product releases. Starting at 3:16 PM, all products experienced significant performance degradation.

- **ChatGPT:** Began substantial recovery around 5:45 PM and fully recovered at 7:01 PM.
- **API:** Began substantial recovery around 5:36 PM, with all models fully recovered by 7:38 PM.
- **Sora:** Fully recovered at 7:01 PM.

------

### Root Cause

OpenAI operates hundreds of Kubernetes clusters globally. The Kubernetes control plane primarily handles cluster management, while the data plane runs actual workloads (like model inference services).

To improve organizational reliability, we've been enhancing cluster-level observability tools to increase visibility into system operations. At 3:12 PM PST, we deployed a new telemetry service across all clusters to collect detailed metrics from Kubernetes control planes.

Due to the telemetry service's broad operational scope, the new service configuration inadvertently caused all nodes in every cluster to execute expensive Kubernetes API operations that scaled exponentially with cluster size. Thousands of nodes simultaneously making these high-load requests overwhelmed the Kubernetes API servers, crippling the control planes of large clusters. The issue was most severe in our largest clusters, preventing detection in test environments; additionally, DNS caching reduced problem visibility in production until the issue spread throughout clusters.

Although Kubernetes data planes can largely operate independently of control planes, data plane DNS resolution depends on the control plane—if the control plane fails, services cannot communicate via DNS.

In summary, the new telemetry service configuration unexpectedly generated massive Kubernetes API load in large clusters, crashing control planes and disrupting DNS service discovery.

------

### Testing and Deployment

We tested the change in a staging cluster without detecting any issues. The failure primarily affected clusters above a certain size; combined with per-node DNS caching delaying failure visibility, the change didn't reveal obvious anomalies before widespread deployment in production.

Before deployment, our primary concern was the new telemetry service's resource consumption (CPU/memory). We assessed resource usage across all clusters pre-deployment to ensure new deployments wouldn't interfere with running services. While we tuned resource requests for different clusters, we didn't consider Kubernetes API server load. Meanwhile, change monitoring focused on the service's health status without comprehensive cluster health monitoring (especially control plane health).

Kubernetes data planes (handling user requests) are designed to continue operating when control planes are offline. However, Kubernetes API servers are crucial for DNS resolution, which is a core dependency for many services.

DNS caching provided temporary buffering during early failure stages, allowing stale but usable DNS records to continue providing address resolution for services. Over the next 20 minutes, these caches gradually expired, causing services dependent on real-time DNS to fail. This time lag exposed problems gradually as deployment continued, making the eventual failure scope more concentrated and obvious. Once DNS caches expired, all cluster services made new DNS requests, further burdening the control plane and making recovery difficult in the short term.

------

### Resolution

In most cases, monitoring deployments and rolling back problematic changes is relatively straightforward, and we have automated tools to detect and roll back faulty deployments. During this incident, our detection tools worked correctly—alerting engineers minutes before customer impact. However, actually fixing the problem required deleting the problematic telemetry service, which required accessing the Kubernetes control plane. With API servers unable to handle management operations under massive load, we couldn't immediately remove the faulty service.

We confirmed the problem within minutes and immediately initiated multiple workflows attempting different approaches to quickly restore clusters:

1. **Scale down cluster size:** Reduce total Kubernetes API load by decreasing node count.
2. **Block network access to Kubernetes management API:** Prevent new high-load requests, giving API servers time to recover.
3. **Scale up Kubernetes API servers:** Increase available resources to handle request backlogs, creating an operational window to remove the faulty service.

We simultaneously employed all three methods, eventually restoring access to some control planes, enabling us to delete the problematic telemetry service.

Once we restored access to some control planes, the system began rapidly improving. Where possible, we switched traffic to healthy clusters while further repairing other problematic clusters. Some clusters still experienced resource contention during recovery: many services simultaneously attempting to re-download required components, causing resource saturation requiring manual intervention.

This incident resulted from multiple systems and processes interacting and failing simultaneously:

- Test environments failed to capture the new configuration's impact on Kubernetes control planes.
- DNS caching created delayed service failures, allowing widespread change deployment before full failure exposure.
- Inability to access control planes during failure made recovery extremely slow.

------

### Timeline

- **December 10, 2024:** New telemetry service deployed to staging cluster, tested without issues.
- **December 11, 2024 2:23 PM:** Code introducing the service merged to main branch, triggering deployment pipeline.
- **2:51 PM to 3:20 PM:** Change gradually applied to all clusters.
- **3:13 PM:** Alerts triggered, notifying engineers.
- **3:16 PM:** Small number of customers began experiencing impact.
- **3:16 PM:** Root cause confirmed.
- **3:27 PM:** Engineers began migrating traffic from affected clusters.
- **3:40 PM:** Customer impact peaked.
- **4:36 PM:** First cluster recovered.
- **7:38 PM:** All clusters recovered.

------

### Prevention Measures

To prevent similar incidents, we're implementing the following measures:

##### 1. More Robust Staged Deployment

We will continue strengthening staged deployment and monitoring mechanisms for infrastructure changes, ensuring any failures are quickly detected and contained to smaller scopes. All future infrastructure-related configuration changes will use more comprehensive staged deployment processes with continuous monitoring of service workloads and Kubernetes control plane health during deployment.

##### 2. Fault Injection Testing

Kubernetes data planes need further enhancement for survival without control planes. We will introduce testing for this scenario, including intentionally injecting "misconfigurations" in test environments to verify system detection and rollback capabilities.

##### 3. Emergency Kubernetes Control Plane Access

We currently lack emergency mechanisms for accessing API servers when data planes put excessive pressure on control planes. We plan to establish "break-glass" mechanisms ensuring engineering teams can access Kubernetes API servers under any circumstances.

##### 4. Further Decouple Kubernetes Data and Control Planes

Our current dependency on Kubernetes DNS services creates coupling between data and control planes. We will invest more effort in making control planes non-critical for essential services and product workloads, reducing single-point dependency on DNS.

##### 5. Faster Recovery Speed

We will introduce more comprehensive caching and dynamic rate limiting for critical resources required for cluster startup, regularly conducting "rapid entire cluster replacement" drills to ensure correct, complete startup and recovery in minimum time.

------

### Conclusion

We sincerely apologize to all customers affected by this incident—whether ChatGPT users, API developers, or enterprises relying on OpenAI products. This incident fell short of our own expectations for system reliability. We recognize the critical importance of providing highly reliable services to all users and will prioritize implementing the above prevention measures while continuously improving service reliability. Thank you for your patience during this outage.

Published 23 hours ago. December 12, 2024 - 17:19 PST

------

**Resolved**

Between 3:16 PM and 7:38 PM on December 11, 2024, OpenAI services were unavailable. Starting around 5:40 PM, we observed gradual API traffic recovery; ChatGPT and Sora recovered around 6:50 PM. We resolved the issue at 7:38 PM and restored all services to normal operation.

OpenAI will conduct a complete root cause analysis of this incident and share follow-up details on this page.

December 11, 2024 - 22:23 PST

------

**Monitoring**

API, ChatGPT, and Sora traffic has largely recovered. We will continue monitoring to ensure the issue is completely resolved.

December 11, 2024 - 19:53 PST

------

**Update**

We are continuing recovery efforts. API traffic is recovering, and we're restoring ChatGPT traffic region by region. Sora has begun partial recovery.

December 11, 2024 - 18:54 PST

------

**Update**

We are working to fix the issue. API and ChatGPT have partially recovered; Sora remains offline.

December 11, 2024 - 17:50 PST

------

**Update**

We are continuing to develop recovery solutions.

December 11, 2024 - 17:03 PST

------

**Update**

We are continuing to develop recovery solutions.

December 11, 2024 - 16:59 PST

------

**Update**

We have found a viable recovery solution and are beginning to see some traffic successfully returning. We will continue working to restore services as quickly as possible.

December 11, 2024 - 16:55 PST

------

**Update**

ChatGPT, Sora, and API remain unavailable. We have identified the issue and are deploying a fix. We are working to restore services as quickly as possible and sincerely apologize for the outage impact.

December 11, 2024 - 16:24 PST

------

**Identified Issue**

We've received reports of API call errors and login issues with platform.openai.com and ChatGPT. We have confirmed the issue and are working on a fix.

December 11, 2024 - 15:53 PST

------

**Update**

We are continuing to investigate this issue.

December 11, 2024 - 15:45 PST

------

**Update**

We are continuing to investigate this issue.

December 11, 2024 - 15:42 PST

------

**Investigating**

We are currently investigating this issue and will provide more updates soon.

Published 2 days ago. December 11, 2024 - 15:17 PST

This incident affected API, ChatGPT, Sora, Playground, and Labs.
