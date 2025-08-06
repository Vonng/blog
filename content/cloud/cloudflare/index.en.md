---
title: Cloudflare - The Cyber Buddha That Destroys Public Cloud
date: 2024-04-03
summary: |
  While I've always advocated for cloud exit, if it's about adopting a cyber bodhisattva cloud like Cloudflare, I'm all in with both hands raised.
author: |
  [Feng Ruohang](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [WeChat](https://mp.weixin.qq.com/s/i4wk9ebyUK7irNSwuT3NWQ)
tags: [cloud-exit,Cloudflare]
---

At today's 2024 Developer Week, Cloudflare released a series of exciting new features, such as Python Workers and Workers AI, elevating the convenience of application development and delivery to an entirely new level. Compared to Cloudflare's Serverless development experience, traditional cloud providers' so-called Serverless products look ridiculous.

Cloudflare is better known for its generous free tier, allowing small and medium websites to run here at virtually zero cost. Against Cloudflare's stark contrast, public cloud providers that rent out [CPU](/cloud/ecs), [disk](/cloud/ebs), and [bandwidth](/cloud/cdn/) at sky-high prices look repulsive. Clouds like Cloudflare deliver a development experience that truly deserves the name "cloud." In my view, Cloudflare should proactively compete with traditional public cloud providers for the right to define cloud computing.

Disclosure: Cloudflare didn't pay me - I actually paid Cloudflare. Purely because Cloudflare's products are excellent and solve my needs extremely well, making me very happy to pay a bit to support them and tell more friends about this benefit. In contrast, after paying traditional public cloud providers, my feeling is "what the hell is this stuff" - I must write articles to ruthlessly criticize them to ease my mental damage.

---------------

## What is Cloudflare

Cloudflare is an American company providing content delivery network (CDN), internet security, anti-DDoS (distributed denial of service), and distributed DNS services. It serves 20% of the world's internet traffic. If you access some websites with a VPN, you can often see Cloudflare's anti-DDoS verification pages and logo. They provide:

1. **Content Delivery Network (CDN)**: Cloudflare's CDN service caches customer website content through globally distributed data centers, speeding up website loading and reducing server pressure.
2. **Website Security**: Provides SSL encryption and security measures against SQL injection and cross-site scripting attacks, enhancing website security.
3. **DDoS Protection**: Features advanced DDoS protection capabilities that can resist attacks of various scales, protecting websites from interference.
4. **Smart Routing**: Uses Anycast network technology to intelligently identify optimal data transmission paths, reducing latency.
5. **Automatic HTTPS Redirect**: Automatically converts access to HTTPS, enhancing communication security.
6. **Workers Platform**: Provides Serverless architecture, allowing JavaScript or WASM (WebAssembly) code to run on Cloudflare's global network without managing servers.

Of course, Cloudflare also has some very nice services, such as Pages for hosting websites, R2 object storage, D1 distributed database, etc., with excellent developer experience.

![](cloudflare-1.jpg)

> [Cloudflare Official Introduction](https://www.cloudflare.com/zh-cn/what-is-cloudflare/)

------------

## Pages: Simple and Easy Website Hosting

For example, if you want to host a static website, how simple is it with Cloudflare? First, create a Repo on GitHub, throw your website content in, then link to your [Git Repo](https://developers.cloudflare.com/pages/configuration/git-integration/) in Cloudflare, assign a subdomain, and your website is automatically deployed to every corner of the world. If you want to update website content, just git push to a specific branch.

If you use specific [**web frameworks**](https://developers.cloudflare.com/pages/framework-guides/), you can even build directly online from repository content: Blazor, Brunch, Docusaurus, Gatsby, Gridsome, Hexo, Hono, Hugo, Jekyll, Next.js, Nuxt, Pelican, Preact, Qwik, React, Remix, Solid, Sphinx, Svelte, Vite 3, Vue, VuePress, Zola, Angular, Astro, Elder.js, Eleventy, Ember, MkDocs.

From having never touched Cloudflare to moving Pigsty's website to CF and completing deployment took me only about an hour. I don't need to worry about servers, CI/CD, HTTPS certificates, security, high defense against DDoS - Cloudflare has already done everything for me. More importantly, traffic is completely free. The only thing I did was bind a credit card and spend over ten yuan to buy a domain, but actually no additional fees are needed - everything is already included in the free plan.

What's even more shocking is that although access speed is a bit slower, websites on CF can be directly accessed from mainland China without even needing ICP filing! It's quite ironic that while domestic cloud providers can quickly provision website resources for you, the most time-consuming step is often getting stuck on ICP filing. This is indeed one of Cloudflare's beneficial features.

------------

## Worker: Ultimate Serverless Experience

Although you can put a lot of business logic in the frontend and solve it with JavaScript in the browser, a complex dynamic website also needs some backend development. Cloudflare has simplified this to the extreme - **you only need to write JavaScript functions for business logic**. Of course, you can also use TypeScript, and now it even supports Python - directly calling AI models, it's hard to imagine how many new tricks will emerge!

The functions written by users are deployed on Cloudflare's worldwide CDN edge server nodes, executing user-defined business logic. You can [**do all sorts of things**](https://developers.cloudflare.com/workers/examples/): return dynamic HTML and JSON, custom routing, redirects, forwarding, filtering, caching, A/B testing, rewrite requests, aggregate requests, perform authentication. Of course, you can also directly use object storage R2 and SQL database D1 in business code, or forward requests to your own data center servers for processing.

```js
export interface Env {
  // If you set another name in wrangler.toml as the value for 'binding',
  // replace "DB" with the variable name you defined.
  DB: D1Database;
}

export default {
  async fetch(request: Request, env: Env) {
    const { pathname } = new URL(request.url);

    if (pathname === "/api/beverages") {
      // If you did not use `DB` as your binding name, change it here
      const { results } = await env.DB.prepare(
        "SELECT * FROM Customers WHERE CompanyName = ?"
      )
        .bind("Bs Beverages")
        .all();
      return Response.json(results);
    }

    return new Response(
      "Call /api/beverages to see everyone who works at Bs Beverages"
    );
  },
};
```

> [Querying D1 in Worker](https://developers.cloudflare.com/d1/get-started/#write-queries-within-your-worker), as simple as calling a variable.

```ini
[[d1_databases]]
binding = "DB" # available in your Worker on env.DB
database_name = "prod-d1-tutorial"
database_id = "<unique-ID-for-your-database>"
```

> No complicated configuration needed, just specify the D1 database/R2 object storage name.

Compared to the clunky development and deployment experience on traditional clouds, CF Workers truly achieve a Serverless effect that makes developers ecstatic. Developers don't need to worry about database connection strings, AccessPoints, AK/SK key management, what database drivers to use, how to manage local logs, how to build CI/CD pipelines - at most just specify simple information like storage bucket names in environment variables. Write Worker glue code to implement business logic, and command-line deployment completes global deployment and goes live.

In contrast, the various so-called Serverless services provided by traditional public cloud providers, like RDS Serverless, are like a bad joke - just a difference in billing model - they can't Scale to Zero and don't improve usability much. You still have to create an RDS suite in the console by clicking around, instead of being like true Serverless like Neon where you can quickly spin up a new instance just by connecting with a connection string. More importantly, with even a few dozen to a hundred QPS, the bill explodes compared to annual/monthly packages - this mediocre "Serverless" indeed pollutes the original meaning of the term.

------------

## R2: Object Storage That Destroys S3

Cloudflare R2 provides object storage services. Compared to AWS S3, it's perhaps an order of magnitude cheaper - I mean, while just looking at storage prices \$ / GB·month, Cloudflare (0.015 \$) isn't much different from S3 (0.023 \$), but Cloudflare R2 has **free traffic**!

|    Monthly Free Tier    | Cloudflare R2  |   Amazon S3    |
|:-----------------------:|:--------------:|:--------------:|
|        Storage          |   10 GB / month    |    5 GB / month    |
|       Write Requests    |    1 M / month     |    2 K / month     |
|       Read Requests     |    10 M / month    |    20 K / month    |
|      Data Transfer      |    **Unlimited!**    |     100 GB     |
| **Pricing Beyond Free Tier** |                |                |
|        Storage          |  ¥ 0.11 / GB   |  ¥ 0.17 / GB   |
|       Write Requests    | ¥ 32.63 / million requests | ¥ 36.25 / million requests |
|       Read Requests     | ¥ 2.61 / million requests  |  ¥ 2.9 / million requests  |
|      Traffic Fees       |    **Free!**     |  ¥ 0.65 / GB   |

> Cloudflare [R2 pricing](https://www.cloudflare.com/pg-cloudflare-r2-vs-aws-s3/) vs AWS S3 comparison

For example, my website consumed 300 GB of traffic in the past month with R2. At domestic cloud prices of about 80 cents per GB, I would need to pay 240 yuan, but I didn't pay a cent. Moreover, I know even more extreme examples - like consuming 3TB of traffic in a month and still being within the free tier...

![](cloudflare-3.jpg)

Cloudflare R2 is integrated with CDN. With traditional cloud service providers, you still need to worry about additional CDN configuration, origin traffic, CDN traffic packages, anti-DDoS, etc. But Cloudflare doesn't need this - just check the configuration to enable it, and your R2 Bucket can be directly read worldwide. Most importantly, you don't have to worry about bill explosions - I know several cases on traditional cloud providers where attacks blew up CDN traffic, draining tens of thousands of yuan overnight into debt (including a case I personally experienced where the cloud provider's own stupid CDN origin design [exploded CDN traffic](/cloud/cdn/)). But on Cloudflare, you don't need to watch [**bills**](/cloud/finops) and traffic like a bulldog and owl. First, Cloudflare traffic is free... More powerfully, Cloudflare already has intelligent anti-DDoS service, even the free plan provides this service by default, effectively avoiding malicious attacks (on traditional cloud providers, this stuff is sold separately as expensive "high defense IP services" costing thousands to tens of thousands). Plus the generous monthly free 10 million read requests (which is already very large for images and software packages!), ensures costs here are highly predictable - if not zero.

------------

## Cloudflare: The Value of Being Online

Dr. Wang Jian's book "Online" about cloud computing makes it very clear that the real value of cloud computing is **being online** (not elasticity, agility, cheapness, etc.). For example: I have some cloud exit customers and users who, although they've moved their main business from public cloud to IDC or office servers, still keep some ECS and RDS tails in the cloud - because their data collection APIs are there, feeling that public cloud's network access is more stable and reliable than their own computer rooms/offices - note it's network access, not storage and computing.

![](cloudflare-4.jpg)

Many cloud customers pay [several times to dozens of times premium on computing power](/cloud/ebs), [dozens to hundreds of times premium on storage](/cloud/ebs), all for this network "online" capability. But Cloudflare, with its globally distributed CDN with edge computing capabilities, has elevated "online" capability to an entirely new level, solving this problem better than traditional public clouds. For example, AI's current darling OpenAI's website and API do exactly this - providing access through CF.

In this model, users can completely provide website and API access through Cloudflare while placing heavy storage and computing in IDCs, rather than renting at several times the price on traditional public clouds. Cloudflare's Workers can be used at the edge to send and receive data and forward requests to your own data centers for processing. If you want more reliable disaster recovery, you can also use R2 and D1 on Cloudflare as temporary local cache, preprocessing and aggregating data before pulling it to IDCs for processing.

------------

## CF and IDC Squeeze Public Cloud from Both Ends

On one side of the IT scale spectrum - individual webmasters and small businesses - new generation cloud services/SaaS (CF, Neon, Vercel, Supabase) cyber bodhisattvas' free tiers have obvious substitution and impact on public clouds - forget about 99 yuan annual cloud servers, even 9.99 might not be attractive - **how can anything be cheaper than free?** - especially when building websites with CF is much better than self-building on cloud servers.

But more importantly, on the other side of the spectrum for medium and large enterprises, the emerging IDC 2.0 and open source management software alternatives converge, short-circuiting public cloud middlemen, leveraging the cumulative advantages of [hardware Moore's Law](https://mp.weixin.qq.com/s/1OSRcBfd58s0tgZTUZHB9g), becoming [ultimate FinOps practice](https://mp.weixin.qq.com/s/Yp_PU8nmyK-NVq0clD98RQ), achieving [amazing cost reduction and efficiency improvement capabilities](https://mp.weixin.qq.com/s/CicctyvV1xk5B-AsKfzPjw). Cloudflare's emergence completes the last missing piece of the open source IDC self-build model - "**online**" capability.

Cloudflare doesn't provide those elastic computing, storage, [K8S](/db/db-in-k8s/), [RDS](/cloud/rds) services found on traditional public clouds. But fortunately, Cloudflare can cooperate well with public cloud/IDC - in a sense, because Cloudflare successfully solves the "online" problem, traditional data center IDC 2.0 can also have "online" capabilities comparable to or even exceeding public clouds. Together, they factually destroy some public cloud moats and squeeze the survival space of traditional public cloud providers.

I'm very bullish on Cloudflare's model. In fact, this kind of smooth experience deserves to be called cloud and enjoys the high margins of the high-tech industry. Traditional IDC 2.0 is also continuously improving, and the experience of renting cabinets and bare metal servers is not inferior to traditional public clouds (nothing more than servers going from two minutes to a few hours). Public cloud providers that cannot provide more technical added value and product irreplaceability will have increasingly smaller survival space - [ultimately retreating to traditional IDC/IaaS business](/cloud/profit/).