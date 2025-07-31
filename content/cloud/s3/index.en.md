---
title: "S3: Elite to Mediocre"
date: 2023-12-26
hero: /hero/s3.jpg
author: |
  [Ruohang Feng](https://vonng.com/en/) ([@Vonng](https://vonng.com/en/)) | [WeChat](https://mp.weixin.qq.com/s/HathxpQ_KUuqxyrtyCDzWw)
summary: >
  S3 is longer "cheap" with the evolution of hardware, and other challengers such as cloudflare R2.
tags: [Cloud,CloudExit,S3,MinIO]
---

Object storage (S3) has been a defining service of cloud computing, once hailed as a paragon of cost reduction in the cloud era. Unfortunately, with the evolution of hardware and the emergence of resources cloud (Cloudflare R2) and open-source alternatives (MinIO), the once "cost-effective" object storage services have lost their value for money, becoming as much a "cash cow" as EBS. In our "Mudslide of Cloud Computing" series, we've already delved into the cost structure of cloud-based EC2 compute power, EBS disks, and RDS databases. Today, let's examine the anchor of cloud services—object storage.

[![](featured.webp)](https://mp.weixin.qq.com/s/HathxpQ_KUuqxyrtyCDzWw)



------------

## From Cost Reduction to Cash Cow

**Object Storage**, also known as Simple Storage Service (abbreviated as **S3**, hereafter referred to as S3), was once the flagship product for its cost-effectiveness in the cloud.

A decade ago, hardware was expensive; managing to use a bunch of several hundred GB mechanical hard drives to build a reliable storage service and design an elegant HTTP API was a significant barrier. Therefore, compared to those "enterprise IT" storage solutions, the cost-effective S3 seemed very attractive.

However, the field of computer hardware is quite unique—with a Moore's Law that sees prices halve every two years. AWS S3 has indeed seen several price reductions in its history. The table below organizes the main post-reduction prices for S3 standard tier storage, along with the reference unit prices for enterprise-grade HDD/SSD in the corresponding years.

|                                                          Date                                                          |  $/GB·Month  |     ¥/TB·5年     |     HDD ¥/TB     |   SSD ¥/TB    |
|:----------------------------------------------------------------------------------------------------------------------:|:------------:|:---------------:|:----------------:|:-------------:|
|                               [2006](https://aws.amazon.com/cn/blogs/aws/amazon_s3/).03                                |    0.150     |      63000      |       2800       |               |
|          [2010](http://aws.typepad.com/aws/2010/11/what-can-i-say-another-amazon-s3-price-reduction.html).11           |    0.140     |      58800      |       1680       |               |
|              [2012](http://aws.typepad.com/aws/2012/11/amazon-s3-price-reduction-december-1-2012.html).12              |    0.095     |      39900      |       420        |     15400     |
| [2014](http://aws.typepad.com/aws/2014/03/aws-price-reduction-42-ec2-s3-rds-elasticache-and-elastic-mapreduce.html).04 |    0.030     |      12600      |       371        |     9051      |
|             [2016](https://aws.amazon.com/ru/blogs/aws/aws-storage-update-s3-glacier-price-reductions/).12             |    0.023     |      9660       |       245        |     3766      |
|                                    [2023](https://aws.amazon.com/cn/s3/pricing).12                                     |    0.023     |      9660       |       105        |      280      |

|                                                     **Price Ref**                                                      |   **EBS**    | **All Upfront** | **Buy NVMe SSD** | **Price Ref** |
|:----------------------------------------------------------------------------------------------------------------------:|:------------:|:---------------:|:----------------:|:-------------:|
|                                                       S3 Express                                                       |    0.160     |      67200      |     DHH 12T      |     1400      |
|                                                        EBS io2                                                         | 0.125 + IOPS |     114000      |   Shannon 3.2T   |      900      |

It's not hard to see that the unit price of S3's standard tier dropped from **$0.15/GB·month** in 2006 to **$0.023/GB·month** in 2023, a reduction to **15%** of the original or a **6-fold** decrease, which sounds good. However, when you consider that the price of the underlying HDDs for S3 dropped to **3.7%** of their original, a whopping **26-fold** decrease, the trickery becomes apparent.



**The resource premium multiple of S3 increased from 7 times in 2006 to 30 times today!**



In 2023, when we re-calculate the costs, it's clear that the value for money of storage services like S3/EBS has changed dramatically—cloud computing power EC2 compared to building one's own servers has a 5 – 10 times premium, while cloud block storage EBS has a several dozen to a hundred times premium compared to local SSDs. Cloud-based S3 compared to ordinary HDDs also has about a thirty times resource premium. And as the anchor of cloud services, the prices of S3/EBS/EC2 are passed on to almost all cloud services—completely stripping cloud services of their cost-effectiveness.

The core issue here is: **The price of hardware resources drops exponentially according to Moore's Law, but the savings are not passed through the cloud providers' intermediary layer to the end-user service prices.** **To not advance is to go back; failing to reduce prices at the pace of Moore's Law is effectively a price increase**. Taking S3 as an example, over the past decade, cloud providers' S3 has nominally reduced prices by 6-fold, but hardware resources have become 26 times cheaper, so how should we view this pricing now?




---------------

## Cost, Performance, Throughput

Despite the high premiums of cloud services, if it represents an irreplaceable **best choice**, the use by high-value, price-insensitive top-tier customers is not affected even with a high premium and low cost-effectiveness. However, it's not just about cost; the performance of storage hardware also follows Moore's Law. Over time, building one's own S3 has started to show a significant advantage in performance.

The performance of S3 is mainly reflected in its **throughput**. AWS S3's 100 Gb/s network provides up to 12.5 GB/s of access bandwidth, which is indeed commendable. Such throughput was undoubtedly impressive a decade ago. However, today, an enterprise-level 12 TB NVMe SSD, costing less than $20,000, can achieve 14 GB/s of read/write bandwidth. 100Gb switches and network cards have also become very common, making such performance readily achievable.

In another key performance indicator, "latency," S3 is significantly outperformed by local disks. The first-byte latency of the S3 standard tier is quite poor, ranging between **100-200ms** according to the documentation. Of course, AWS has just launched "High-Performance S3" — **S3 Express One Zone** at 2023 Re:Invent, which can achieve millisecond-level latency, addressing this shortcoming. However, it still falls far short of the NVMe's 4K random read/write latency of **55µs/9µs**.

S3 Express's millisecond-level latency sounds good, but when we compare it to a self-built NVMe SSD + MinIO setup, this "millisecond-level" performance is embarrassingly inadequate. Modern NVMe SSDs achieve 4K random read/write latencies of 55µs/9µs. With a thin layer of MinIO forwarding, the first-byte output latency is at least an order of magnitude better than S3 Express. If standard tier S3 is used for comparison, the performance gap widens to three orders of magnitude.

The gap in performance is just one aspect; the cost is even more crucial. The price of standard tier S3 has remained unchanged since 2016 at $0.023/GB·month, equating to **161 RMB/TB·month**. The higher-tier S3 Express One Zone is an order of magnitude more expensive, at **$0.16/GB·month**, equating to **1120 RMB/TB·month**. For reference, we can compare the data from ["Reclaiming the Dividends of Computer Hardware"](https://mp.weixin.qq.com/s/1OSRcBfd58s0tgZTUZHB9g) and ["Is Cloud Storage a Cash Cow?"](https://mp.weixin.qq.com/s/UxjiUBTpb1pRUfGtR9V3ag):

| **Factor**  | **Local PCI-E NVME SSD**                                                             | **Aliyun ESSD PL3**                                                                                                                                                                                                                                 | **AWS io2 Block Express**                                                                                                                                                                            |
|-------------|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Cost        | **14.5 RMB/TB·month** (5-year amortization / 3.2T MLC) 5-year warranty, ¥3000 retail | **3200 RMB/TB·month** (Original price 6400 RMB, monthly package 4000 RMB) 50% discount for 3-year upfront payment                                                                                                                                   | **1900 RMB/TB·month** Best discount for the largest specification 65536GB 256K IOPS                                                                                                                  |
| Capacity    | 32TB                                                                                 | 32 TB                                                                                                                                                                                                                                               | 64 TB                                                                                                                                                                                                |
| IOPS        | 4K random read: 600K ~ 1.1M 4K random write 200K ~ 350K                              | Max 4K random read: 1M                                                                                                                                                                                                                              | 16K random IOPS: 256K                                                                                                                                                                                |
| Latency     | 4K random read: 75µs 4K random write: 15µs                                           | 4K random read: 200µs                                                                                                                                                                                                                               | Random IO: 500µs (assumed 16K)                                                                                                                                                                       |
| Reliability | UBER < 1e-18, equivalent to 18 nines MTBF: 2 million hours 5DWPD, over three years   | Data reliability: 9 nines [Storage and Data Reliability](https://help.aliyun.com/document_detail/476273.html)                                                                                                                                       | **Durability**: 99.999%, 5 nines (0.001% annual failure rate) [io2 details](https://aws.amazon.com/cn/blogs/storage/achieve-higher-database-performance-using-amazon-ebs-io2-block-express-volumes/) |
| SLA         | 5-year warranty, direct replacement for issues                                       | [Aliyun RDS SLA](https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud201910310944_35008.html?spm=a2c4g.11186623.0.0.270e6e37n8Exh5) Availability 99.99%: 15% monthly fee 99%: 30% monthly fee 95%: 100% monthly fee | [Amazon RDS SLA](https://d1.awsstatic.com/legal/amazonrdsservice/Amazon-RDS-Service-Level-Agreement-Chinese.pdf) Availability 99.95%: 15% monthly fee 99%: 25% monthly fee 95%: 100% monthly fee     |

e local NVMe SSD example used here is the Shannon DirectIO G5i 3.2TB MLC particle enterprise-level SSD, extensively used by us. Brand new, disassembled retail pieces are priced at ¥2788 (available on Xianyu!), translating to a monthly cost per TB of 14.5 RMB over 60 months (5 years). Even if we calculate using the Inspur list price of ¥4388, the cost per TB·month is only 22.8. If this example is not convincing enough, we can refer to the 12 TB Gen4 NVMe enterprise-level SSDs purchased by DHH in ["Is It Time to Give Up on Cloud Computing?"](https://mp.weixin.qq.com/s/CicctyvV1xk5B-AsKfzPjw), priced at $2390 each, with a cost per TB·month of exactly **23** RMB.


So, why are NVMe SSDs, which outperform by several orders of magnitude, priced an order of magnitude cheaper than standard tier S3 (161 vs 23) and two orders of magnitude cheaper than S3 Express (1120 vs 23 x3)? If I were to use such hardware (even accounting for triple replication) + open-source software to build an object storage service, could I achieve a three orders of magnitude improvement in cost-effectiveness? (This doesn't even account for the reliability advantages of SSDs over HDDs.)

It's worth noting that the comparison above focuses solely on the cost of storage space. The cost of data transfer in and out of object storage is also a significant expense, with some tiers charging not for storage but for retrieval traffic. Additionally, there are issues of SSD reliability compared to HDD, data sovereignty in the cloud, etc., which will not be elaborated further here.

Of course, cloud providers might argue that their S3 service is not just about storage hardware resources but an out-of-the-box **service**. This includes software intellectual property and maintenance labor costs. They may claim that self-hosting has a higher failure rate, is riskier, and incurs significant operational labor costs. Unfortunately, these arguments might have been valid in 2006 or 2013, but they seem rather ludicrous today.




-----------

## Self-Hosted OSS S3

A decade and a half ago, the vast majority of users lacked the IT capabilities to self-host, and there were no mature open-source alternatives to S3. Users could tolerate the premium for this high technology. However, as various cloud providers and IDCs began offering object storage, and even open-source free object storage solutions like MinIO emerged, the market shifted from a seller's to a buyer's market. The logic of value pricing turned into cost pricing, and the unyielding premium on resources naturally faced scrutiny — what extra value does it actually provide to justify such significant costs?

Proponents of cloud storage claim that moving to the cloud is cheaper, simpler, and faster than self-hosting. For individual webmasters and small to medium-sized internet companies within the cloud's suitable spectrum, this claim certainly holds. If your data scale is only a few dozen GBs, or you have some medium-scale overseas business and CDN needs, I would not recommend jumping on the bandwagon to self-host object storage. You should instead turn to Cloudflare and use R2 — perhaps the best solution.

However, for the truly high-value, medium-to-large scale customers who contribute the majority of revenue, these value propositions do not necessarily hold. If you are primarily using local storage for TB/PB scale data, then you should seriously consider the cost and benefits of self-hosting object storage services — which has become very simple, stable, and mature with open-source software. Storage service reliability mainly depends on disk redundancy: apart from occasional hard drive failures (HDD AFR 1%, SSD 0.2-0.3%), requiring you (or a maintenance service provider) to replace parts, there isn't much additional burden.

If the open-source Ceph, which mixes EBS/S3 capabilities, is considered somewhat operationally complex and not fully feature-complete; then the fully S3-compatible object storage service MinIO can be considered truly plug-and-play — a standalone binary without external dependencies, requiring only a few configuration parameters to quickly set up, transforming server disk arrays into a standard local S3-compatible service, even integrating AWS's AK/SK/IAM compatible implementations!

From an operational management perspective, the operational complexity of Redis is an order of magnitude lower than PostgreSQL, and MinIO's operational complexity is another order of magnitude lower than Redis. It's so simple that I could spend less than a week to integrate MinIO deployment/monitoring as an add-on into our open-source PostgreSQL RDS solution, serving as an optional central backup storage repository.

At Tantan, several MinIO clusters were built and maintained this way: holding 25PB of data, possibly the largest scale of MinIO deployment in China at the time. How many people were needed for maintenance? Just a fraction of one operations engineer's working time was enough, and the overall self-hosting cost was about half of the cloud list price. Practice proves the point, if anyone tells you that self-hosting object storage is difficult and expensive, you can try it yourself — in just a few hours, these sales FUD tactics will fall apart.

For object storage services, the cloud's three core value propositions: "cheaper, simpler, faster", the "simpler" part may not hold up, "cheaper" has turned the other way, probably only leaving "faster" — indeed, no one can beat the cloud on this point. You can apply for PB-level storage services across all regions of the world in less than a minute on the cloud, which is amazing! However, you also have to pay a high premium, several times to dozens of times over for this privilege.

Therefore, for object storage services, among the cloud's three core value propositions: "cheaper, simpler, faster", the "simpler" part may not hold, and "cheaper" has gone in the opposite direction, probably only leaving "faster" — indeed, no one can beat the cloud on this point. You can indeed apply for PB-level storage services across all regions of the world in less than a minute on the cloud, which is amazing! However, you also have to pay a high premium for this privilege, several to dozens of times over. For enterprises of a certain scale, compared to the cost of operations increasing several times, waiting a couple of weeks or making a one-time capital investment is not a big deal.





-----------

## Summary

The exponential decline in hardware costs has not been fully reflected in the service prices of cloud providers, turning public clouds from universally beneficial infrastructure into monopolistic profit centers.

However, the tide is turning. Hardware is becoming interesting again, and cloud providers can no longer indefinitely hide this advantage. The savvy are starting to crunch the numbers, and the bold have already taken action. Pioneers like Elon Musk and DHH have fully realized this, moving away from the cloud to reap millions in financial benefits, enjoy performance gains, and gain more operational independence. More and more people are beginning to notice this, following in the footsteps of these pioneers to make the wise choice and reclaim their hardware dividends.



### References


`[1]` 2006: *https://aws.amazon.com/cn/blogs/aws/amazon_s3/*

`[2]` 2010: *http://aws.typepad.com/aws/2010/11/what-can-i-say-another-amazon-s3-price-reduction.html*

`[3]` 2012: *http://aws.typepad.com/aws/2012/11/amazon-s3-price-reduction-december-1-2012.html*

`[4]` 2014: *http://aws.typepad.com/aws/2014/03/aws-price-reduction-42-ec2-s3-rds-elasticache-and-elastic-mapreduce.html*

`[5]` 2016: *https://aws.amazon.com/ru/blogs/aws/aws-storage-update-s3-glacier-price-reductions/*

`[6]` 2023: *https://aws.amazon.com/cn/s3/pricing*

`[7]` First-byte Latency: *https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html*

`[8]` Storage & Reliability: *https://help.aliyun.com/document_detail/476273.html*

`[9]` EBS io2 Spec: *https://aws.amazon.com/cn/blogs/storage/achieve-higher-database-performance-using-amazon-ebs-io2-block-express-volumes/*

`[10]` Aliyun RDS SLA: *https://terms.aliyun.com/legal-agreement/terms/suit_bu1_ali_cloud/suit_bu1_ali_cloud201910310944_35008.html?spm=a2c4g.11186623.0.0.270e6e37n8Exh5*

`[11]` Amazon RDS SLA: *https://d1.awsstatic.com/legal/amazonrdsservice/Amazon-RDS-Service-Level-Agreement-Chinese.pdf*

