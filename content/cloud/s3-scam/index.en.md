---
title: "Cloud Dark Forest: Exploding Cloud Bills with Just S3 Bucket Names"
linkTitle: Exploding Cloud Bills with Just S3 Bucket Names
date: 2024-04-30
author: |
  [Maciej Pocwierz](https://medium.com/@maciej.pocwierz) | Translated by: [Feng Ruohang](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [WeChat Original](https://mp.weixin.qq.com/s/35ScjtPjC1GNGKaSArJhcA) | [English Original](https://medium.com/@maciej.pocwierz/how-an-empty-s3-bucket-can-make-your-aws-bill-explode-934a383cb8b1)
summary: >
  The dark forest law has emerged on public cloud: **Anyone who knows your S3 object storage bucket name can explode your cloud bill.** 
tags: [cloud-exit,AWS,S3]
---

The dark forest law has emerged on public cloud: **Anyone who knows your S3 object storage bucket name can explode your cloud bill.**

![](featured.webp)

------

Imagine this: you create an empty, **private** AWS S3 storage bucket in your favorite region. What would your AWS bill look like the next morning?

A few weeks ago, I started developing a proof-of-concept (PoC) for a document indexing system for a client. I created an S3 bucket in the `eu-west-1` region and uploaded some test files. Two days later, I checked the AWS billing page mainly to confirm my operations were within the free tier. The results were obviously disappointing — the bill exceeded **$1,300**, with the billing dashboard showing nearly **100 million** S3 PUT requests executed in just one day!

![](bill.jpg)

> My S3 bill, charged per day/per region

------

## Where Did These Requests Come From?

By default, AWS doesn't log requests to your S3 buckets. But you can enable such logging through [**AWS CloudTrail**](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloud/trail-logging.html) or [**S3 Server Access Logs**](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html). After enabling CloudTrail logs, I immediately discovered thousands of write requests from different accounts.

**Why would third-party accounts make unauthorized requests to my S3 bucket?**

Was this a DDoS-like attack against my account? Or against AWS? It turns out that **a popular open source tool's default configuration stores backups to S3. This tool's default bucket name was exactly the same as mine**. This means every instance deploying this tool without changing default settings was trying to store backup data to my S3 bucket!

> Note: Unfortunately, I cannot reveal this tool's name as it might put the related company at risk (details explained later).

So, a large number of unauthorized third-party users were trying to store data in my private S3 bucket. But why should I pay for this?

**S3 also charges you for unauthorized requests!**

This was confirmed in my communication with AWS support, their response was:

> Yes, S3 also charges for unauthorized requests (4xx), this is as expected.

Therefore, if I now open my terminal and type:

```bash
aws s3 cp ./file.txt s3://your-bucket-name/random_key
```

I would get an **`AccessDenied`** error, **but you have to pay for this request**.

Another issue puzzled me: why did over half my bill costs come from the **us-east-1** region? I had no buckets there at all! It turns out that S3 requests not specifying regions default to **us-east-1**, then get redirected as appropriate. And you still need to pay for redirect request costs.

### Security Issues

Now I understood why my S3 bucket received millions of requests and why I ended up with a huge S3 bill. At the time, I also had an idea. If all these misconfigured systems were trying to backup data to my S3 bucket, what if I set it to "**public write**"? I made the bucket public for less than 30 seconds and collected over 10GB of data in that short time. Of course, I can't reveal who owns this data. But this seemingly harmless configuration error could lead to serious data leaks — shocking!

------

## What Did I Learn?

**Lesson One: Anyone who knows your S3 bucket name can freely explode your AWS bill**

There's almost no way to prevent this except deleting the bucket. When accessed directly via S3 API, you can't use CloudFront or WAF to protect your bucket. Standard S3 PUT request costs are only $0.005 per thousand requests, but a single machine can easily make thousands of requests per second.

**Lesson Two: Adding random suffixes to your bucket names can improve security.**

This approach reduces threats from misconfigurations or intentional attacks. At minimum, avoid using short and common names for S3 bucket names.

**Lesson Three: When making large numbers of S3 requests, ensure you explicitly specify AWS regions.**

This way you can avoid additional costs from API redirects.

------

## Epilogue

1. I reported my findings to the maintainers of this vulnerable open source tool. They quickly fixed the default configuration, though already deployed instances can't be fixed.

2. I also reported this to AWS security team. I hoped they might restrict this unfortunate S3 bucket name, but they were unwilling to handle third-party product misconfigurations.

3. I reported this issue to two companies whose data I found in my bucket. They didn't reply to my emails, possibly treating them as spam.

4. AWS eventually agreed to cancel my S3 bill, but emphasized this was an exceptional case.

Thanks for taking time to read my article. Hope it helps you avoid unexpected AWS costs!



------

## Cloud Exit Lao Feng's Commentary

The dark forest law has emerged on public cloud: **Anyone who knows your S3 object storage bucket name can explode your AWS bill**. Just by knowing your bucket name, others don't need to know your ID or pass authentication — they can directly force PUT/GET your bucket, and regardless of success or failure, you'll be charged.

This introduces a new type of DDoS-like attack — DoCC (Denial of Cost Control), bill-exploding attacks.

In some groups, AWS after-sales and engineers gave their explanation — "AWS has a principle in designing charging strategies: if AWS incurred costs (users bear some responsibility), users must be charged." AWS sales' explanation was that this customer doesn't know how to use AWS and should attend AWS SA exam training before going online.

But from common sense, this is completely unreasonable — requests initiated by others that don't even pass Auth, why charge users? And users seem to have no way to prevent this situation except choosing not to use this service — this is a design flaw and a security vulnerability.

But in AWS's view, this feature is considered a Feature, not a security vulnerability or bug, usable to drain users' gold coins. The same design logic runs through AWS's product design logic. For example, Route53 charges for querying domains that don't resolve, so knowing a domain uses AWS resolution can also enable DDoS.


---------------

I'm not sure if domestic cloud vendors use the same handling logic. But they basically directly or indirectly learn from AWS. So there's a fairly high probability they would handle it the same way.

![](ddos.jpg)

> As someone from cybersecurity background, I know some industry practices, like DDoS attacks to sell high-defense services — screenshot from a group member


---------------

In "[**Cloudflare Roundtable Interview**](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247487400&idx=1&sn=cf5b94165d2791030e0e874dca8383c7&scene=21#wechat_redirect)", I also mentioned security issues, like insider traffic farming problems.

> Finally, I want to mention security. I think security is Cloudflare's core value proposition. Why do I say this? Let me give an example. An independent webmaster friend used a certain domestic cloud CDN, and in recent two years had mysterious excessive traffic. Monthly overseas traffic of several TB, single IPs consuming 10GB traffic then disappearing. After switching service providers, these strange traffic patterns disappeared. Operating costs became 1/10 of original, making one think deeply — **are these cloud vendors engaging in insider fraud, farming traffic? Or are cloud vendors themselves (or their affiliates) intentionally attacking to promote their high-defense IP services?** I've heard of such examples.
>
> Therefore, when using domestic cloud CDN, many users have natural concerns and distrust. But Cloudflare solves this problem — first, traffic is free, charged by request volume, so farming traffic is meaningless; second, it defends against DDoS for you, even Free Plan has this service. CF can't damage its own reputation — this solves a user pain point, the problem of exploded bills — I've indeed seen such cases where public cloud accounts with tens of thousands yuan got drained clean. Using Cloudflare completely eliminates this problem. I can ensure bill certainty — if not guaranteed zero.

Well, overall, exploded bills are also a unique security risk on public cloud — hope cloud users stay cautious and careful. Small mistakes might immediately cause irreparable losses on bills.

![](aws-joke.jpg)
