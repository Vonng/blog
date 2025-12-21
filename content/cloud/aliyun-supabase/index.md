---
title: "阿里云“借鉴”Supabase：开源与云的灰色地带"
date: 2025-11-06
author: 冯若航
summary: >
  国内创业可能被问到最多的问题：如果阿里这种大厂下场，你怎么办？这不，阿里云RDS上线了新品Supabase，就是一个鲜活案例。
tags: [阿里云, 开源, Supabase]
---


国内创业可能被问到最多的问题 ：如果阿里这种大厂下场，你怎么办？这不，阿里云 RDS 上线了新品 —— Supabase，就是一个鲜活案例。



## 背景：Supabase

Supabase 是一个开箱即用的 BaaS，在 PostgreSQL 基础上提供了数据库、用户鉴权、文件存储、实时订阅、边缘函数等一整套后端功能，可以省掉很多后端开发的工作。算是 AI 时代数据库领域的当红炸子鸡。

过去几年里，除了 PostgreSQL，老冯最看好的两个数据库产品就是 DuckDB 和 Supabase。
近年来 Supabase 在开发者和创业公司中人气飙升：GitHub 星标数接近九万，老冯听说 YC 80% 的 Startup 现在都用 Supabase 起步来搭建 SaaS 了。

在老冯自己的 PostgreSQL 发行版 Pigsty 里，早在两年前就提供了 Supabase 自建支持，也是 Supabase 官网推荐的两种自建方式（Ansible via Pigsty, K8S via StackGres）。
老冯自己也编译打包分发了 Supabase 所需的 PG 扩展插件，弄了开箱即用的自建方案，这个 Supabase 自建教程的访问量比首页还大，足以让我感受到 Supabase 的火爆。



## 阿里云的 Supabase

昨天有朋友在群里发给我一则新闻，说阿里云 RDS Supabase 上线了。我知道前几个月，阿里云在其 AnalyticDB 数据仓库产品中就集成过 Supabase 服务，
这次又在 RDS PostgreSQL（以及据称在 PolarDB）中纷纷加入 Supabase 支持。
好家伙，不愧互联网卷王，国产 Indian，搞个 Supabase 还要上三个团队来一起卷。

![rds-supabase-banner.jpg](rds-supabase-banner.jpg)

如此一来，阿里云相当于将 Supabase 正式纳入了自家数据库产品线的一部分**。
对于国内用户而言**，由于 Supabase 官方云服务主要面向海外且访问不便，阿里云提供本地化的 Supabase 服务在**使用层面**确实降低了门槛。
但对于 Supabase 这个原作者 创业公司来说，这无疑是 “噩梦成真” ，“**如果巨头下场做你在做的事怎么办？**” 
或者更进一步，因为你开了源，云厂商直接拿去包装成自己的云服务卖跟你竞争，你怎么办？ ——眼下这个案例就是一个活生生的例子。



## Supabase 怎么看

当然，会不会有一种可能，阿里云已经跟 Supabase 聊好了合作，所以才把它放进自己的产品线里呢？老冯反正是没有找到任何公开的合作公告。
但是为了确认一下，老冯在 X 上 @ 了 Supabase 的 CEO Paul Copplestone，问问他怎么看这件事。
结果 Paul 评论了一句 ： “Hacker ethics, I think you are assuming this exists in that part of the world” 。（极客道德？我觉得你预设了这东西在那个部分的世界真的存在）。

![x-comment.png](x-comment.png)

Paul 点赞转发评论三连，这种回应也就说明了其实也没什么合作，就是阿里云自己搞的花活。
老实说，这可真是一句辛辣的评论，老冯看到这个回复心里五味杂陈，感觉脸上火辣辣，因为我也算在 “That part of the world” 里。
但是俺也无法反驳，事实就摆在面前，恁国云计算一哥干的这么个事儿吧，丢脸丢到海外去了。



## 这样的操作是否合法？

Supabase 采用 Apache 2.0 和 MIT 许可证的组合策略，在法律层面为阿里云的做法开了绿灯。
Apache 2.0是最宽松的开源许可证之一，其核心条款明确允许商业使用、修改、分发和作为服务提供，无需支付任何费用或贡献代码。

然而，Apache 2.0 许可证的唯一的实质性限制是 **商标保护**。
许可证第6条明确规定："本许可证不授予使用许可方的商号、商标、服务标志或产品名称的权限"，仅允许在描述作品来源时的合理和惯例使用。
这意味着阿里云可以使用 Supabase 的代码，但理论上不能使用 "Supabase" 这个名称

之前 AWS 在这件事上已经翻过车了 —— 觉得 ElasticSearch 开源嘛，就拉到云上包装成云服务卖，结果因为 ElasticSearch 这个商标的名字翻了大车，最后不得不用了个 OpenSearch 的名字。
同理还有 DocumentDB 和 Valkey ，阿里云显然是没有吸取这个教训，大大咧咧地用着 RDS Supabase，PolarDB Supabase，AnalyticDB Supabase 这样的名称提供服务。

![trademark.jpg](trademark.jpg)

通常来说，第三方若要在商业产品中使用他人的商标名称，需获得授权，否则可能构成商标侵权或不正当竞争。
但可惜的是 ，Supabase 是在美国注册的商标（注册号99258169 USPTO），没有在中国注册，中国的 SUPABASE 42 类商标持有者是 “昆山市巴城镇隆卡尔贸易商行” 。
而且中国商标法采用的是 “申请在先” 而非美国的 “使用在先”，未注册的外国商标在中国没有任何保护，除非能证明是 “驰名商标” —— 要我说乔丹都翻车了，Supabase 这种成立才五年的公司指望这个显然不现实。


## 然而，吃相太过难看

从**道德和惯例**来看，大厂如此直接借用创业公司商标来推自家产品，是非常不体面的跌份行为。即使勉强不违法，也有“傍名牌”“偷品牌”之嫌。
这不仅可能让一些不了解内幕的用户误以为 Supabase 官方与阿里云有合作或背书，更有挖空 Supabase 品牌在本土价值的风险。
毕竟，一旦阿里云版Supabase占据市场，日后 Supabase 若想亲自进入中国发展，其自己的品牌可能反而被模糊甚至贬值了。

从**贡献回馈**角度看，阿里云享受了 Supabase 开源社区几年来的研发成果，省去了从0到1开发同类服务的时间和成本，
却并未公开宣称会对 Supabase 开源项目有所回馈，例如代码贡献、社区共建或赞助支持。这种行为有点类似 “吃绝户” 
—— 也就是把别人辛苦养大的“孩子”一把抢过来，连汤带水端走，令原作者一无所获。这种“不劳而获”的印象，加剧了社区对大厂的不信任和反感。

巨头公司利用自身资源和渠道优势，去提供一个创业公司辛苦打造的开源产品服务，哪怕法律上无可指摘，也被视作缺乏基本的尊重和良知。
国产云厂商做不起来生态，就是因为喜欢吃独食**。大厂往往希望自己提供一切，不愿让第三方独立软件厂商分享到利益。
**这种倾向导致的结果是：生态体系贫瘠，创新公司难以存活，最终反过来使得云厂商自己也缺乏繁荣的生态支撑，陷入恶性循环。
从这个角度看，阿里云此次对Supabase的争食，正是国内互联网巨头生态弊病的一个缩影。

**在国外，AWS、Azure、GCP 等虽然也被批评“侵占”开源红利，但它们依然有庞大的合作伙伴市场，许多软件公司通过云市场或官方合作获得成长机会。
**比如云计算一哥 AWS 就使用合作伙伴模式与 Supabase 进行收入共享。2024年Supabase进入AWS Marketplace，作为SaaS解决方案提供，购买计入AWS支出承诺，AWS Activate 项目为初创公司提供300美元Supabase 积分。
这种做法既让用户方便获取服务，又确保了原厂能从中获利。然而阿里云选择了另一条路——直接自己动手，把别人的开放成果据为己有打造产品卖点，**完全绕开了原始开发团队**。

![aws-supabase.png](aws-supabase.png)

> AWS 上的 Supabase 订阅计划




## 对于生态与开源社区的伤害

阿里云 RDS Supabase 事件反映出的不仅是个别厂商的行为，更揭示了一个**令人担忧的行业现象**：创业公司的创新成果难以在巨头环伺下得到应有的尊重和保护。

在中国创业圈，常常有人提出灵魂拷问：“要是阿里/腾讯/字节也来做你的业务，你怎么办？”Supabase 无疑是当下数据库/BaaS领域的明星创业公司，它选择了开源并构建社区来成长。
但现在，它的开源战略却被大厂当作武器反过来打压了它进入一块市场的可能性。这对其他创业者是一个警示：**过于宽松的开源许可在云时代可能让小公司陷入被动**，特别是面对平台型巨头时。

长远来看，这会不会让创业者对开源模式心生动摇？会不会迫使更多开源项目在许可上设防，减少开源分享的意愿？这些连锁反应都对开源生态不利。
我们已经看到越来越多的例子了，[Redis](https://mp.weixin.qq.com/s/W5kOLxeJCIHjnWbIHc1Pzw)，[ElasticSearch](https://mp.weixin.qq.com/s/NdeeYn10qQ0xBPL-67IXdQ)，[MongoDB](https://mp.weixin.qq.com/s/I3ug7Qv9jz3-uD3x_N1jKw)，Grafana，MinIO ，
都开始从宽松的开源许可证转向更为严格苛刻的许可证，甚至是商业许可证。开源生态因为云大厂的贪婪索取而面临 “盐碱地化”。

总而言之，阿里云 RDS Supabase 虽然打着“开箱即用 Supabase”旗号风风光光上线了，但其中的是非曲直值得每一位开发者深思。
在法律上它走了巧妙的灰色地带，在商业上却难言光彩。希望未来我们能看到更多互利合作的案例，而非这样的赤裸裸“拿来主义”。
开源世界需要的是良性循环，而不是被薅秃了羊毛的失望。大厂应该 **尊重创新，尊重开源，尊重小团队的生存空间**。
只有大公司愿意扶持而非扼杀新生事物，整个生态才能繁荣。反之，如果都是你方唱罢我登场的巧取豪夺，那么下次再有好项目恐怕就不愿意开源了。这对所有人都不是好事。

阿里云之前在开源生态上其实是有一定的口碑的，一些开源产品也是通过合作的方式共赢共建的，包括 Qwen 系列开源模型也为阿里云上了大分。
所以老冯也希望阿里云能爱惜自己的羽毛，毕竟口碑一旦臭了，就真的很难再救回来了 —— 等到阿里云也变成 “阿里高管空降山姆被全网疯狂抵制” ，那就太晚了。






## 参考阅读

#### Supabase

[别争了，AI时代数据库已经尘埃落定](https://mp.weixin.qq.com/s/bChEvpXgXKi5njr6Kj5YGg)

[数据库茶水间：OpenAI拟收购Supabase ？](https://mp.weixin.qq.com/s/RmU7RXl9ewwnpabjI4lw4Q)

[PG生态赢得资本市场青睐：Databricks收购Neon，Supabase融资两亿美元，微软财报点名PG](https://mp.weixin.qq.com/s/skxFplC0ow0Hh9gqs_N4hQ)

[PG系创业公司Supabase：$80M C轮融资](https://mp.weixin.qq.com/s/fi_p3tTZTnwP5XDJrkVbQw)

[创业出海神器 Supabase 自建指南](https://mp.weixin.qq.com/s/HJDfcSC8XFL_PkDlxHbqRQ)

[PG系创业公司Supabase：$80M C轮融资](https://mp.weixin.qq.com/s/fi_p3tTZTnwP5XDJrkVbQw)

[OrioleDB 奥利奥数据库来了！](https://mp.weixin.qq.com/s/QG7_UyT08fNFiBj6qujSEA)


#### 阿里云


[草台互殴，赔三千万？阿里大战小旺神](https://mp.weixin.qq.com/s/O4LvUspOgrVBWHzmBvfmUA)

[阿里云故障，CDN挂了，记得申请SLA赔付](https://mp.weixin.qq.com/s/Y2PZiH63EAXRKP8gele8NQ)

[大故障：阿里云核心域名被拖走了](https://mp.weixin.qq.com/s/l1b-eq06NyuN61cqZoYJjA)

[阿里云：从上到下烂到根了 去除原文版](https://mp.weixin.qq.com/s/0pT7wb0Y6ohgvEltED93hA)

[硬编码密码泄漏，阿里云的软件工程也太差了](https://mp.weixin.qq.com/s/43pIBxYvsszeBZGk7LU7_w) 马工

[花钱买罪受的大冤种：逃离云计算妙瓦底](https://mp.weixin.qq.com/s/zwJ2T2Vh_R7xD8IKPso31Q)

[支付宝崩了？双十一整活王又来了](https://mp.weixin.qq.com/s/D2XmL2YYN2kqHtwFN4FVGQ)

[记一次阿里云 DCDN 加速仅 32 秒就欠了 1600 的问题处理（扯皮）](https://mp.weixin.qq.com/s/0Wnv1B80Tk4J03X3uAm4Ww) 转

[阿里云：高可用容灾神话的破灭](https://mp.weixin.qq.com/s/rXwEayprvDKCgba4m-naoQ)

[阿里云故障预报：本次事故将持续至20年后？](https://mp.weixin.qq.com/s/G41IN2y8DrC002FQ_BXtXw)

[阿里云新加坡可用区C故障，网传机房着火](https://mp.weixin.qq.com/s/EDRmP7ninfSx-CgNDb8mpg)

[草台班子唱大戏，阿里云RDS翻车记](https://mp.weixin.qq.com/s/kOIw8uPjZUZ0-QisC1TBOA)

[阿里云又挂了，这次是光缆被挖断了？](https://mp.weixin.qq.com/s/cb2Lh56uINxacM2uUaB6Vw)

[云计算：菜就是一种原罪](https://mp.weixin.qq.com/s/jYIqj94B07oTu9KC85bjtQ)

[taobao.com 证书过期](https://mp.weixin.qq.com/s/-ntsNfdEq3b4qs5tKP7tfQ)

[牙膏云？您可别吹捧云厂商了](https://mp.weixin.qq.com/s/XZqe4tbJ9lgf8a6PWj7vjw)

[罗永浩救不了牙膏云](https://mp.weixin.qq.com/s/s_MCdaCByDBuocXkY1tvKw)

[迷失在阿里云的年轻人](https://mp.weixin.qq.com/s/w7YzdxSrAsIqk2gXBks9CA)

[剖析云算力成本，阿里云真的降价了吗？](https://mp.weixin.qq.com/s/rp8Dtvyo9cItBJSsvfrKjw)

[从降本增笑到真的降本增效](https://mp.weixin.qq.com/s/FIOB_Oqefx1oez1iu7AGGg)

[阿里云周爆：云数据库管控又挂了](https://mp.weixin.qq.com/s/3F1ud-tWB3eymu1-dxSHMA)

[我们能从阿里云史诗级故障中学到什么](https://mp.weixin.qq.com/s/OIlR0rolEQff9YfCpj3wIQ)

[【阿里】云计算史诗级大翻车来了](https://mp.weixin.qq.com/s/cTge3xOlIQCALQc8Mi-P8w)

[阿里云的羊毛抓紧薅，五千的云服务器三百拿](https://mp.weixin.qq.com/s/Nh28VahZkQMdR8fDoi0_rQ)

[云厂商眼中的客户：又穷又闲又缺爱](https://mp.weixin.qq.com/s/y9IradwxTxOsUGcOHia1XQ) 马工


#### 云与开源

[ElasticSearch又重新开源了？？？](https://mp.weixin.qq.com/s/NdeeYn10qQ0xBPL-67IXdQ)

[Redis不开源是“开源”之耻，更是公有云之耻](https://mp.weixin.qq.com/s/W5kOLxeJCIHjnWbIHc1Pzw)

[范式转移：从云到本地优先](https://mp.weixin.qq.com/s/Yp6L0hh4b4HuJQRPD3aJYw)
