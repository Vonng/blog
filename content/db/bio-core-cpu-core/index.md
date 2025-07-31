---
title: 先优化碳基BIO核，再优化硅基CPU核
linkTitle: 先优化BIO核，再优化CPU核
date: 2024-09-07
author: |
  [DHH](https://world.hey.com/dhh/optimize-for-bio-cores-first-silicon-cores-second-112a6c3f) | [译者：冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）| [微信公众号]()
summary: >
  程序员是昂贵稀缺的生物计算核心，软件成本的锚钉 —— 优化CPU核前请优先考虑优化生物核。
module: []
tags: [数据库]
---


## 先优化生物核，再优化硅内核

企业痴迷于 AI 的一个重要原因是，它有可能显著降低程序员的薪酬成本。如果一个公司需要 10 名程序员完成一项任务，而每个程序员的年薪为 20 万美元，那这就是一个每年 200 万美元的问题。如果 AI 能砍掉四分之一的成本，他们就能省出 50 万美元！如果能砍一半那就是 100 万美元！提高效率在程序员的薪资成本上会很快转化为利润！

这就是为什么我喜欢 Ruby！这就是我搞 Rails 的原因！过去 20 年，我一直坚信编程领域的趋势是：程序员的成本会越来越高，而计算机的成本却在不断下降。因此，聪明的做法是提高程序员的生产力，**即使以牺牲计算机资源为代价**！

很多程序员难以理解这一点 —— 他们实际上是非常昂贵的“生物计算核”，而且是真正稀缺的资源。而硅制计算内核却非常丰富，成本也在不断下降。所以随着时间推移，用计算机的时间换取程序员生产力的交易会越来越划算。AI 是实现此目标的方式之一，但像 Ruby on Rails 这样的工具从一开始关注的也是这个问题。

我们再看看那个年薪 20 万美元的程序员。你可以从 Hetzner 租用 1 个 AMD EPYC CPU核，年租金是 55 美元（批发模式，一台 48 核的服务器月租金 220 \$元，所以 220 x 12 / 48 = 55）。这意味着一个生物核的价格，相当于 3663 个硅基核。如果你能让生物核的效率提高 10%，你就相当于节省了 366 个硅核的成本。如果你能让生物核的效率提高 25%，那你就相当于节省了接近一千个硅基核！

但是，许多“软绵绵的”生物编程内核对它们的硅制同类怀有一种独特的人类同情，这种情感超越了理性的数学计算。他们单纯地觉得 —— 自己可以花更多时间，通过使用对自己不高效、但对硅内核更高效的工具和技术，来减少硅内核的负担，而不是要求硅内核做更多的工作。对于某些人来说，减轻硅内核的负担几乎成了一种道德责任，似乎他们认为自己有义务尽量承担这些任务。

从艺术和精神层面上讲，我其实还挺尊重这种做法的！让计算机用更少的资源完成更多任务，确实有一种美好的感觉。我依然对 Commodore 64 和 Amiga 时代的 Demo 充满怀念。当年那些技术高手仅用 [区区4KB](https://www.youtube.com/watch?v=wl6mXn_wHEw) 就能让计算机呈现出惊艳的音画效果，实在是令人难以置信。

然而在大多数情况下，这种做法在经济上并不划算。当然，在计算性能的前沿阵地上依然需要有人去挖掘最后一丝性能。比如，需要有人从 NVIDIA 4090 显卡中榨干最后一滴性能，我们的 3D 引擎才能在 4K / 120FPS 下进行光线追踪。但这对于软件行业中的绝大多数业务场景都不现实 —— 它们的业务是写业务软件！对于这类工作，不需要什么史诗级优化，计算机在很久以前就已经足够快了。

这也是我过去 20 年来，我一直在做的工作！开发业务软件并将其作为 SaaS 销售。整个行业都在做同样的事情，带来了巨大的利润和就业机会。这是一次历史性的牛市行情，主要由使用高级语言解决业务逻辑的程序员驱动 —— 他们找出产品与市场的契合点（PMF）来推动进步。

所以，每当听到关于计算效率的讨论时，你应该想起这个“软绵绵的”生物核。世界上大多数软件的价格都是基于它们的人工成本，而不是所需的硅内核。因而哪怕只是稍微提高生物核的生产力，也值得在硅芯片采购上花大钱。而且这种成本效益的比例，只会年复一年更偏向于充分利用生物核。

—— 至少在 AGI 霸主到来前，生物核都不会彻底过时！但没有人知道这一天何时会来，或者是否会到来。所以最好着眼于当下的经济学，选择对你来说最能提高生产力的工具链，并相信快乐的程序员将是你投资中最划算的一笔。


> 作者：David Heinemeier Hansson，DHH，37 Signal CTO，Ruby on Rails 作者
>
> 译者：冯若航，PostgreSQL Hacker，开源 RDS PG —— Pigsty 作者，数据库老司机，云计算泥石流。
>
> [优先优化生物内核，其次是硅内核](https://world.hey.com/dhh/optimize-for-bio-cores-first-silicon-cores-second-112a6c3f) @ 2024-09-06




--------

## 老冯评论

DHH 的博客一如既往地充满洞见 —— 虽然事实听上去可能并不讨喜，但程序员本质上也是一种生物计算核 —— Bio Core ，而很多程序员已经忘记了这一点。

实际上在一百年前，Computer 指的还是 “计算员” 而非 “计算机”；而在上世纪四五十 年代，算力的衡量单位更一度是 ——  “Kilo-Girls”，即一千名女孩的计算速度，类似的单位还有 `kilo-girl-hour` 等。当然，随着信息技术的突飞猛进，这些枯燥乏味的计算活计都交给计算机了，程序员得以专注于更高层次的抽象和创造。

对于我所在的数据库行业，我认为这篇文章能带给用户的一个启示是 —— 数据库的真正瓶颈早就不是 CPU 硅基核了，而是能用好数据库的生物核。对于绝大多数用例，数据库的瓶颈早已不再是 CPU，内存， I/O，网络，存储，而是开发者与 DBA 的思维，认知，经验，智慧。

因此，没人会在乎你的数据库能否支持 100 万 TPS，而是你的软件是否能用最小的时间成本，复杂度成本，认知成本解决问题。
易用性、简单性、可维护性成为了竞争的焦点 —— 专注于此道的 RDS 数据库服务也因此大获成功（同理还有 Neon, Supabase，Pigsty 等）。

像 AWS 这样的云厂商拿着开源的 MySQL 和 PostgreSQL 内核一路杀到了数据库市场一哥的位置，是因为 AWS 比 Oracle / EDB 有更深的数据库内核造诣，懂得如何利用硅基核吗？非也。而是因为比起优化硅基核，他们更懂得如何优化生物核 —— 他们懂得如何让开发者，DBA，运维更容易用好数据库 —— 用好数据库，而非制造数据库，成为了新的核心瓶颈点。

所以，传统数据库内核是一个夕阳产业，将与格力空调，联想电脑一样成为低毛利的制造业。 而真正的高科技与技术创新，将发生在数据库管控上 —— 用软件辅助、赋能、甚至冒天下之大不韪的“替代” 一部分开发者 —— 如何用好数据库内核与硅基CPU核，提高生物核的生产力，降低认知成本，简化复杂度，提高易用性。这才是未来数据库行业的发展方向。




高科技行业就是要依靠技术创新驱动。如果你能用开源 PG 内核替代 Oracle ，SQL Server，那别人也能 —— 最好的结果无非就是甲骨文微软都放弃传统数据库转型做云服务，传统数据库成为低利润的制造业。正如二十年的 PC 行业一样。二十年前 IBM 戴尔惠普都是国际玩家，中国联想说要做到世界一流。今天看联想确实做到了，但是 PC 行业早就不是高科技行业了，只是一个最无聊普通的制造业。

即使是在国内看起来很能打的[真自研分布式数据库内核](/zh/blog/db/distributive-bullshit)，如果选错了赛道，那所能期待的最好结局也不过是成为数据库行业的长虹，赚五个点的利润。然后被拿着开源 PostgreSQL 内核提供服务的 云厂商 RDS 和本地优先 RDS 骑脸输出，最终成为数据库领域的 “Kilo-Girl”。




--------

## Optimize for bio cores first, silicon cores second

> David Heinemeier Hansson 2024-09-06
>
> [Optimize for bio cores first, silicon cores second](https://world.hey.com/dhh/optimize-for-bio-cores-first-silicon-cores-second-112a6c3f)

A big part of the reason that companies are going ga-ga over AI right now is the promise that it might materially lower their payroll for programmers. If a company currently needs 10 programmers to do a job, each have a cost of $200,000/year, then that's a $2m/year problem. If AI could even cut off 1/4 of that, they would have saved half a million! Cut double that, and it's a million. Efficiency gains add up quick on the bottom line when it comes to programmers!


That's why I love Ruby! That's why I work on Rails! For twenty years, it's been clear to me that this is where the puck was going. Programmers continuing to become more expensive, computers continuing to become less so. Therefore, the smart bet was on making those programmers more productive EVEN AT THE EXPENSE OF THE COMPUTER!


That's what so many programmers have a difficult time internalizing. They are in effect very expensive biological computing cores, and the real scarce resource. Silicon computing cores are far more plentiful, and their cost keeps going down. So as every year passes, it becomes an even better deal trading compute time for programmer productivity. AI is one way of doing that, but it's also what tools like Ruby on Rails were about since the start.


Let's return to that $200,000/year programmer. You can rent 1 AMD EPYC core from Hetzner for $55/year (they sell them in bulk, $220/month for a box of 48, so 220 x 12 / 48 = 55). That means the price of one biological core is the same as the price of 3663 silicon cores. Meaning that if you manage to make the bio core 10% more efficient, you will have saved the equivalent cost of 366 silicon cores. Make the bio core a quarter more efficient, and you'll have saved nearly ONE THOUSAND silicon cores!


But many of these squishy, biological programming cores have a distinctly human sympathy for their silicon counterparts that overrides the math. They simply feel bad asking the silicon to do more work, if they could spend more of their own time to reduce the load by using less efficient for them / more efficient for silicon tools and techniques. For some, it seems to be damn near a moral duty to relieve the silicon of as many burdens they might believe they're able carry instead.



And I actually respect that from an artsy, spiritual perspective! There *is* something beautifully wholesome about making computers do more with fewer resources. I still look oh-so-fondly back on the demo days of the Commodore 64 and Amiga. What those wizards were able to squeeze out of [a mere 4kb](https://www.youtube.com/watch?v=wl6mXn_wHEw) to make the computer dance in sound and picture was truly incredible.


It just doesn't make much economic sense, most of the time. Sure, there's still work at the vanguard of the computing threshold. Somebody's gotta squeeze the last drop of performance out of that NVIDIA 4090, such that our 3D engines can raytrace at 4K and 120FPS. But that's not the reality at most software businesses that are in the business of making business software (say that three times fast!). Computers have long since been way fast enough for that work to happen without heroic optimization efforts.


And that's the kind of work I've been doing for said twenty years! Making business software and selling it as SaaS. That's what an entire industry has been doing to tremendous profit and gainful employment across the land. It's been a bull run for the ages, and it's been mostly driven by programmers working in high-level languages figuring out business logic and finding product-market fit.



So whenever you hear a discussion about computing efficiency, you should always have the squishy, biological cores in mind. Most software around the world is priced on their inputs, not on the silicon it requires. Meaning even small incremental improvements to bio core productivity is worth large additional expenditures on silicon chips. And every year, the ratio grows greater in favor of the bio cores.



At least up until the point that we make them obsolete and welcome our AGI overlords! But nobody seems to know when or if that's going to happen, so best you deal in the economics of the present day, pick the most productive tool chain available to you, and bet that happy programmers will be the best bang for your buck.