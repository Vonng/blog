---
title: "阿里云rds_duckdb：致敬还是抄袭？"
description: "有人觉得rds缝个duckdb，开源PG就是小垃圾了？商业与开源本应共生共赢，企业若只想坐享其成而不反哺开源，最终只会沦为社区鄙视的对象。"
date: 2025-03-06
tags: ["PostgreSQL", "PG生态"]
categories: ["Blog"]
---


看到有人发了一篇《[天上的“PostgreSQL” 说 地上的 PostgreSQL 都是“小垃圾”](https://mp.weixin.qq.com/s/fFTTRioeTvCmjKip0lx3Cg)》，
文中大肆宣扬阿里云 RDS 新增了一个 rds_duckdb 插件，可以用来做 OLAP 分析， 并进一步带出“云 RDS PG 高高在上、PostgreSQL 开源只是‘小垃圾’”的极端观点，令人不适。

我对 DuckDB 及衍生的 `pg_duckdb` 扩展都很熟悉。
其实无论阿里云或其他云厂商在技术层面如何整合开源，只要合法合理合情，我个人都乐见商业与开源互利共赢。
但如果有人在宣传层面贬低开源、抬高云服务，甚至暗示开源价值低下，那我确实有必要出来说两句以正视听。


-------

## 关于 PG DuckDB

DuckDB 是一个高性能的嵌入式 OLAP 分析数据库，我已经关注它很久了。
在一年前我写的《[PostgreSQL正在吞噬数据库世界](/pg/pg-eat-db-world/)》一文中，
着重介绍了 PG 在 OLAP 领域缝合 DuckDB 实现真HTAP的巨大潜力，[并成功点燃了全球 PG 社区缝合 DuckDB 的热情](/db/pg-kiss-duckdb/)。
PG 社区中涌现出好几个将 DuckDB 整合进 PG 的扩展玩家，而这甚至成为了 [2024 年数据库领域的一个标志性事件](https://mp.weixin.qq.com/s/jgYDHdCqWDRDfoFkfs7W8Q)。

在这些整合 PostgreSQL 与 DuckDB 的项目中，由 DuckDB 官方母公司 MotherDuck 联合 PG OLAP 生态初创企业 Hydra 共同开发的 `pg_duckdb`，可谓最具潜力。
我在其公开发布的第一时间就着手跟进，不仅为 EL 8/9、Debian 12、Ubuntu 22/24 等多种 Linux 发行版的 x86 和 ARM 架构制作并分发了对应的 RPM/DEB 包，还在日常使用和测试中投入了大量精力。

事实上，在我维护的两百多个 PG 扩展插件包里，与 DuckDB 相关的四个扩展是最令我头痛却又最让我兴奋的：`pg_duckdb` 以及基于它衍生的 `pg_mooncake` —— 
硕大无朋的依赖，复杂的编译过程，多个 libduckdb 的冲突，兼容不同操作系统、不同大版本的 PostgreSQL，难度可想而知。 
但我相信，这种真正实现 “OLTP + OLAP” 深度融合的探索，十分难得，也值得全力投入。


-------

## 致敬还是抄袭？

当去年十月阿里云宣布在 RDS 上发布 `rds_duckdb` 时，我最初的想法是“这总算是好事”。 毕竟 `pg_duckdb` 刚开源两个月，就有云厂商跟进，多少还是在推动产业发展。
但很遗憾的是，`rds_duckdb`并没有开源，具体实现、细节接口，我们无从得知。 不过，从它展现给外部的功能接口上，多少能看出和 `pg_duckdb` 的相似之处：

比如，早期第一个公开发布的 `pg_duckdb` 版本，核心接口非常简单，就是 `SET pg_duckdb.execution = on;`，然后就可以直接用 DuckDB 引擎来查询 PostgreSQL 表了。 
而 `rds_duckdb` 的核心接口就是 `SET rds_duckdb.execution = on;`，不过名字从 `pg_duckdb` 变为 `rds_duckdb`。

结合 `rds_duckdb` 公开发布的时间点（`pg_duckdb` 问世后两个月），再加上它的操作方式与行为表现高度相似，可以合理猜想：`rds_duckdb` 至少在接口与理念上借鉴了 `pg_duckdb`。
至于代码层面是否有直接引用，由于 `rds_duckdb`并未开源，我们也无可考证。

当然，`rds_duckdb` 自己也“加了点料”，比如支持 PG 12 / 13，多了几个管理 DuckDB 表的小函数（拷贝数据、查看大小等），但技术上并不复杂。
要我说，这个功能现在只能算是一个简易原型，远无法跟后续版本的 `pg_duckdb` 以及基于它构建的 `pg_mooncake` 相提并论。
换句话说，以现在这个“半成品”水平，谈不上什么“剽窃”或“抄袭”。**“抄袭”也得抄得更像样一点吧？**

然而，如果说它是“致敬”，却也让人无从认同。因为无论是在接口文档还是其他地方，我们都看不到任何对 `pg_duckdb`，甚至对 `duckdb` 的署名或感谢。


-------

## MIT协议的义务

无论是 `duckdb` 本身还是基于它的 `pg_duckdb`，使用的都是非常宽松的 MIT 协议。 因此如果使用了 MIT 项目的代码，只要遵循 MIT 协议的基本要求 —— 
**（1）保留原始版权声明；（2）保留 MIT 许可证文本** —— 就能够做到合规。 这个要求说白了就是：人家写了代码白给你用，你别把人家作者名字删了就好了。

不过，让人玩味的是，我在阿里云 RDS 文档里搜索翻找了半天，也没看到任何地方留存着 DuckDB 的版权声明或许可证文本。
假如 `rds_duckdb` 并未直接使用 `pg_duckdb` 的代码，倒还可以解释说“我没用你的东西”，而且知识产权只保护具体的代码而不保护想法，所以不提也就算了。
—— 但你肯定用了 MIT 协议的 `duckdb` 对吧？ **那么 DuckDB 的 Credit 和 License 在哪里呢？**

尽管法律层面最主要的合规点仍是保留版权和许可证文本，但云厂商提供的是在线服务，“交付物”是一个URL和文档，而非 RPM / DEB 软件包，所以用户能接触到的材料就是官方文档。
**如果在说明文档等对外宣传中，有意无意地淡化或隐去所使用的第三方开源项目，使得公众认为“这是完全自研或完全原创”，那么在舆论与道德层面会被质疑为“抄袭”或“剽窃”**

类似的例子比比皆是，先前“何同学”开源抄袭风波、[抖音美摄案](https://mp.weixin.qq.com/s/72Yp7d6yjIezS9iQZgNw9w)、
“[高春辉诉阿里云抄袭IPIP 案](https://mp.weixin.qq.com/s/Qqgkofmy5_jFFEhVZx-6bQ)，” 以及大家耳熟能详的鹅厂。
更别提有大把“国产数据库公司”将开源的 PG 换皮套壳魔改称为“100%纯自研”数据库。 都是因为不尊重开源版权、把别人的东西当成“自研”，最终声名狼藉、备受质疑。

在我看来，“从开源社区取经，做成服务售卖”本来不丢人，这在全球范围早就是商业惯例，无可厚非； 可“拿了人家的东西，当成自己的发明”就会令人不齿。
因为这会留下极其恶劣的印象：企业既没有对外披露应有的来源，也没为社区带来多少贡献，却能坐享其成，大肆盈利。
如此一来，开源作者失去了正当的尊重与声望，用户也被蒙在鼓里，这种行为不仅违背了开源精神，更破坏了生态的可持续发展。


-------

## 对开源的攻讦

说实话，我并不（很）清楚那篇文章的公众号和阿里云之间是否有某种合作关系，也不知道他们为何如此排斥开源。
从其近期的文章风格看出，一连串“捧云踩开源”桥段已经不是头一回了： 
例如《[天上的“PostgreSQL” 说 地上的 PostgreSQL 都是“小垃圾”](https://mp.weixin.qq.com/s/fFTTRioeTvCmjKip0lx3Cg)》将开源的 PostgreSQL 视为垃圾；
《[云原生数据库砸了 K8S云自建数据库的饭碗](https://mp.weixin.qq.com/s/YCUBDWzPGs2meubY2uYqXQ)》说K8S自建数据库是垃圾，
以及《[开源软件是心怀鬼胎的大骗局 – 开源软件是人类最好的正能量 — 一个人的辩论会](https://mp.weixin.qq.com/s/iTow4Pu8DjDNJl3CnuiLBA)》，体现出对开源软件的偏见。

这种对开源的偏见与攻讦，实在令人费解。要知道，恰恰是因为开源，一系列核心基础软件才得以百花齐放、加速迭代。
Deepseek 的成功也好，PostgreSQL 越做越大也好，都是脚踏实地站在前人开源巨人的肩膀之上。
各大云厂商的“云数据库”大多直接或间接基于开源数据库衍生、优化、深度整合，没了开源，他们的产品根基都将不复存在。

然而时至今日，云厂商从开源社区赚得盆满钵满，却很少进行对等贡献或反馈，导致围绕“[云厂商白嫖开源](https://mp.weixin.qq.com/s/W5kOLxeJCIHjnWbIHc1Pzw)”这个问题，
[矛盾正逐渐加剧](https://mp.weixin.qq.com/s/jgYDHdCqWDRDfoFkfs7W8Q)。 但公道自在人心，也并不是所有云厂商都只知道白拿不还：
比如 AWS RDS 在这两年投入资源推动 PG 生态的 pgvector 成为向量数据库扩展的事实标准，开源了 log_fdw、pgcollection、pgtle 等多款插件，对社区的反哺社区也是看在眼里的。

再看看阿里云 RDS，似乎仍在拘泥于“从开源社区和初创公司碗里捞食”的老思路，吃相不体面也就罢了，问题在于致敬都致不到精髓，
[产品做得简陋不堪](https://mp.weixin.qq.com/s/kOIw8uPjZUZ0-QisC1TBOA)，难以给用户真正的信心。
实际上，对用户来说，不能容忍的不是“云厂商利用开源”，而是“云厂商家大业大，却端出一个半吊子东西敷衍了事”，搞得像个草台班子，丢的还是阿里云自己的脸。


-------

## 参考阅读

[草台班子唱大戏，阿里云RDS翻车记](https://mp.weixin.qq.com/s/kOIw8uPjZUZ0-QisC1TBOA)

[云盘是不是杀猪盘？](https://mp.weixin.qq.com/s/UxjiUBTpb1pRUfGtR9V3ag)

[云数据库是不是智商税](https://mp.weixin.qq.com/s/LefEAXTcBH-KBJNhXNoc7A)

[阿里云：高可用容灾神话的破灭](https://mp.weixin.qq.com/s/rXwEayprvDKCgba4m-naoQ)

[从降本增笑到真的降本增效](https://mp.weixin.qq.com/s/FIOB_Oqefx1oez1iu7AGGg)

[我们能从阿里云史诗级故障中学到什么](https://mp.weixin.qq.com/s/OIlR0rolEQff9YfCpj3wIQ)

[支付宝崩了？双十一整活王又来了](https://mp.weixin.qq.com/s/D2XmL2YYN2kqHtwFN4FVGQ)

[记一次阿里云 DCDN 加速仅 32 秒就欠了 1600 的问题处理（扯皮）](https://mp.weixin.qq.com/s/0Wnv1B80Tk4J03X3uAm4Ww) 转

[阿里云故障预报：本次事故将持续至20年后？](https://mp.weixin.qq.com/s/G41IN2y8DrC002FQ_BXtXw)

[阿里云新加坡可用区C故障，网传机房着火](https://mp.weixin.qq.com/s/EDRmP7ninfSx-CgNDb8mpg)

[阿里云又挂了，这次是光缆被挖断了？](https://mp.weixin.qq.com/s/cb2Lh56uINxacM2uUaB6Vw)

[云计算：菜就是一种原罪](https://mp.weixin.qq.com/s/jYIqj94B07oTu9KC85bjtQ)

[taobao.com 证书过期](https://mp.weixin.qq.com/s/-ntsNfdEq3b4qs5tKP7tfQ)

[牙膏云？您可别吹捧云厂商了](https://mp.weixin.qq.com/s/XZqe4tbJ9lgf8a6PWj7vjw)

[罗永浩救不了牙膏云](https://mp.weixin.qq.com/s/s_MCdaCByDBuocXkY1tvKw)

[迷失在阿里云的年轻人](https://mp.weixin.qq.com/s/w7YzdxSrAsIqk2gXBks9CA)

[剖析云算力成本，阿里云真的降价了吗？](https://mp.weixin.qq.com/s/rp8Dtvyo9cItBJSsvfrKjw)

[阿里云周爆：云数据库管控又挂了](https://mp.weixin.qq.com/s/3F1ud-tWB3eymu1-dxSHMA)

[【阿里】云计算史诗级大翻车来了](https://mp.weixin.qq.com/s/cTge3xOlIQCALQc8Mi-P8w)

[云厂商眼中的客户：又穷又闲又缺爱](https://mp.weixin.qq.com/s/y9IradwxTxOsUGcOHia1XQ) 马工

