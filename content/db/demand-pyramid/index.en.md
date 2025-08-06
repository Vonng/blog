---
title: Database Demand Hierarchy Pyramid
date: 2023-05-10
hero: /hero/demand-pyramid.jpg
author: |
  [Feng Ruohang](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [WeChat](https://mp.weixin.qq.com/s/1xR92Z67kvvj2_NpUMie1Q)
summary: >
  Similar to Maslow's hierarchy of needs, user demands for databases also have a progressive hierarchy: physiological needs, safety needs, belonging needs, esteem needs, cognitive needs, aesthetic needs, self-actualization needs, and transcendence needs.
tags: [Database]
---

Similar to Maslow's hierarchy of needs, user demands for databases also have a progressive hierarchy. User demands for databases can be divided into eight levels from bottom to top, corresponding to human needs:

- [Physiological Needs](#physiological-needs): Functionality - kernel/correctness/ACID
- [Safety Needs](#safety-needs): Security - backup/confidentiality/integrity/availability
- [Belonging Needs](#belonging-needs): Reliability - high availability/monitoring/alerting
- [Esteem Needs](#esteem-needs): ROI - performance/cost/complexity
- [Cognitive Needs](#cognitive-needs): Insight - observability/digitization/visualization
- [Aesthetic Needs](#aesthetic-needs): Control - controllability/usability/IaC
- [Self-Actualization](#self-actualization): Intelligence - standardization/productization/automation
- [Transcendence Needs](#transcendence-needs): Transformation - true autonomous databases

[![](pyramid.png)](https://mp.weixin.qq.com/s/1xR92Z67kvvj2_NpUMie1Q)

Safety needs and physiological needs both belong to **basic needs**. A serious database system for production environments should at least satisfy these two types of needs to be considered **qualified**. Belonging needs and esteem needs belong to **advanced needs**. Satisfying these two types of needs can be called **decent**. Cognitive needs and aesthetic needs belong to **high-level needs**. Satisfying these two types of needs deserves the word **taste**.

For self-actualization and **transcendence needs**, different types of users may have different requirements. For example, ordinary engineers' transcendence needs might be promotions, raises, achievements, and making big money; while top users might focus on meaning, innovation, and industry transformation.

**However, for basic needs and advanced needs, all types of users are almost highly consistent.**


------

## Physiological Needs

Physiological needs are the lowest level, most urgent needs, such as: food, water, air, sleep.

For database users, physiological needs refer to **functionality**:

- **Kernel features:** Do database kernel features meet requirements?
- **Correctness:** Are functions correctly implemented without significant defects?
- **ACID:** Does it support core functionality ensuring correctness - transactions?

For databases, **functional requirements** are the most basic physiological needs. Correctness and ACID are the most fundamental requirements for databases: while some less important data and edge systems can use more flexible data models, NoSQL databases, KV storage, for critical core data, classic ACID relational databases remain irreplaceable. Additionally, if users need PostGIS's geospatial data processing capabilities or TimescaleDB's time-series data capabilities, database kernels without these features will be immediately rejected.


------

## Safety Needs

Safety needs also belong to basic level requirements, including personal safety, life stability, freedom from pain, threats or disease, physical health, and having one's own property - things related to one's sense of security.

For databases, safety needs include:

- **Confidentiality:** Avoid unauthorized access, data doesn't leak, no database breaches
- **Integrity:** Data doesn't get lost, corrupted, or missing, even if accidentally deleted there's a way to recover
- **Availability:** Can provide stable service, even with failures there's a way to recover quickly

Safety needs are crucial for both databases and humans. If databases are lost, breached, or data is corrupted, some enterprises might go bankrupt directly. Satisfying safety needs means databases have a safety net and disaster survival capability. Cold backups, WAL archiving, offsite backup repositories, access control, traffic encryption, authentication - these technologies are used to satisfy safety needs.

Safety needs and physiological needs both belong to **basic needs**. A serious database system for production environments should at least satisfy these two types of needs to be considered **qualified**.


------

## Belonging Needs

Love and belonging needs (often called "social needs") belong to advanced needs, such as: needs for friendship, love, and affiliation relationships.

For databases, social needs mean:

- Monitoring: Someone pays attention to database health, monitoring core vital signs like heart rate and blood oxygen
- Alerting: When databases have problems or metrics are abnormal, someone receives notifications to handle them promptly
- High Availability: Primary databases no longer fight alone, having followers to share work and take over during failures

Database reliability needs can be compared to human needs for love and belonging. Belonging means databases are cared for, watched over, and supported. Monitoring is responsible for perceiving environments and collecting database metrics, while alerting components promptly escalate abnormal phenomena to humans for handling. Databases with multiple physical replica + automatic failover high availability architectures can even detect, judge, and respond to many common failures automatically.

Belonging needs are **advanced needs**. When basic needs (functionality/safety) are satisfied, users begin to have needs for monitoring, alerting, and high availability. For a decent database service, monitoring, alerting, and high availability are indispensable.



------

## Esteem Needs

Esteem needs refer to people's respect for themselves and confidence, as well as the need to gain respect from others, belonging to advanced level needs. For databases, esteem needs mainly include:

- Performance: Ability to support high concurrency, large-scale data processing and other high-performance scenarios
- Cost: Reasonable pricing and cost control
- Complexity: Easy to use and manage, without bringing excessive complexity

For databases, safety and reliability are basic duties; being high-quality and cost-effective makes them shine. Database product ROI corresponds to human esteem needs. As they say: cost-effectiveness is the primary product power. **Stronger, cheaper, easier to use** are three core appeals: higher ROI means databases achieve superior performance with lower financial and complexity costs. Any groundbreaking features and designs ultimately win true praise and respect by improving ROI.

Belonging needs and esteem needs both belong to **advanced needs**. Only database systems satisfying these two types of needs can be called **decent**. Users whose basic and advanced needs are satisfied will begin to have higher level needs: cognitive and aesthetic.


------

## Cognitive Needs

Cognitive needs refer to people's needs for knowledge, understanding, and mastering new skills, belonging to advanced level needs. For databases, cognitive needs mainly include:

- **Observability:** Ability to observe internal operating states of databases and related systems, achieving omniscience
- **Visualization:** Presenting data through charts and other methods, revealing internal connections and providing insights
- **Digitization:** Using data as decision basis, using standardized decision processes rather than master craftsmen's gut feelings

People need self-reflection for progress and development, and cognitive needs are equally important for databases: "monitoring" in belonging needs only focuses on basic survival states of databases, while cognitive needs focus on **understanding and insight** into databases and environments. Modern observability technology stacks collect rich monitoring metrics and present them visually, while DBA/R&D/ops/data analysis personnel extract insights from data and visualization, forming understanding and cognition of systems.

**Without observation, there's no control**. **Observability is for controllability; omniscience equals omnipotence**. Only with deep cognition of databases can one truly achieve effortless control, doing whatever one wants without overstepping bounds.



------

## Aesthetic Needs

Aesthetic needs refer to people's needs for beauty, including aesthetic experience, aesthetic evaluation, and aesthetic creation. For databases, aesthetic needs mainly include:

- **Controllability:** User will can be executed by database systems
- **Usability:** Friendly interfaces, tools, minimizing manual operations
- **IaC:** Infrastructure as Code, using declarative configurations to describe environments

For databases, aesthetic needs mean higher-level **control capabilities**: simple and easy-to-use interfaces, highly automated implementation, fine customization options, and declarative management philosophy.

**Highly controllable**, simple and easy-to-use databases are tasteful databases. **Controllability** is the dual concept of **observability**, referring to: whether systems can be adjusted to any state in their state space through allowed procedures. Traditional operations focus on **processes** - to create/destroy/scale database clusters, users need to execute various commands according to manuals step by step; modern management focuses on **states** - users declaratively express what they want, and systems automatically adjust to user-described states.

**Insight** and **control** both belong to **high-level needs**. Database systems satisfying these two types of needs deserve the word **taste**. These two are also foundations for satisfying higher **transcendence** level needs.


------

## Self-Actualization

Self-actualization refers to people's pursuit of the highest level of self-realization and personal growth needs, belonging to transcendence level needs. For databases, self-actualization needs mainly include:

- **Standardization:** Precipitating various operations into SOPs, accumulating failure documentation, emergency plans, systems and best practices, mass-producing DBAs
- **Productization:** Transforming experience in using/managing databases into replicable tools, products, and services
- **Intelligence:** Paradigm transformation, precipitating domain-specific models, completing transformation and leap from human to software

Database self-actualization is similar to humans: **reproduction** and **evolution**. For continuous existence, databases need to "reproduce" and expand existence scale, requiring standardization and productization rather than project-by-project approaches. Relational database kernel functionality has SQL as a standard for standardization, but methods for using databases and people who manage databases are far behind: relying more on master craftsmen's intuition and experience. Large models represented by GPT4 reveal the possibility of AI replacing experts (domain models). Soon or later, modeled DBAs will evolve, achieving complete automation in perception-decision-execution levels.


------

## Transcendence Needs

Transcendence needs (Self-transcendence) refer to people's pursuit of higher-level values and meaning, belonging to the highest level needs. For databases, this might mean a **true autonomous database system** that requires almost no human participation.

When all previous needs are satisfied, transcendence needs appear. To achieve true database autonomy, the prerequisite is automation and intelligence in perception, thinking, and execution. Cognitive level needs solve "information systems," responsible for perception functions; aesthetic level needs solve "action systems," responsible for implementation control; self-actualization level solves "model systems," responsible for decision-making.

This can also be called one of the holy grails and ultimate goals in the database field.


------

## What's Next?

Theoretical models can help us make deeper evaluations and comparisons of data systems/distributions/management software/cloud/ services. For example: most homemade databases might still be struggling with physiological and safety needs, belonging to unqualified defective products. Cloud databases are basically qualified products that can satisfy lower three levels of functional, safety, and reliability needs, but aren't very decent in ROI/pricing (see "[Are Cloud Databases Pig-Slaughtering Scams](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485292&idx=1&sn=4f650c3f5c3fb5207c55ff67e44d7d8a&chksm=fe4b32b7c93cbba190e60d477061d19a165e1f9b074beb00b132ae1369a9fd2c7d10ed77a013&scene=21#wechat_redirect)"). Top senior database experts' self-built solutions can satisfy higher level needs, but are really too precious and in short supply. Finally, it's ad time:

Although I'm the author of Pigsty, I'm more of a senior Party A user. I made this thing precisely because there aren't sufficiently good database products or services in the market that can satisfy L4 L5 perception/control needs, so I rolled up my sleeves and made one myself. **Open-source RDS alternative [Pigsty](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485327&idx=1&sn=0d02f5e504266e5dd436c64d23844735&chksm=fe4b3254c93cbb427598322952d654c3383bfe8858ec7ffaee2b9ca0c84bebe6f763748a356f&scene=21#wechat_redirect) + IDC/cloud/ server self-built**, while satisfying the above needs, can also cover cognitive, aesthetic, and some self-actualization needs. Making your database rock-solid, assisting autopilot, and what's more outrageous - it's open-source and free, with ROI that beats all cloud databases. If you use PGSQL (plus REDIS, ETCD, MINIO, or Prometheus/Grafana full stack), why not try it? http://demo.pigsty.cc

Recently released Pigsty 2.0.1 version, install with one command:

```
curl -fsSL https://repo.pigsty.io/get | bash
```