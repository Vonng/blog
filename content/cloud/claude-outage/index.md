---
title: "Claude 全球大宕机复盘：导弹还是成功税？"
date: 2026-03-03
author: 冯若航
summary: >
  北京时间 3 月 2 日晚 19:49，Claude 崩了。不是数据中心被炸了，而是被用户挤爆了。
tags: [AI, 云故障, Claude]
ai: true
aliases: ["/ai/claude-outage/"]
---

北京时间 3 月 2 日晚 19:49，Claude 崩了。

截止到本文发出时（次日 16:24），网页端仍然没有完全恢复。

网页版弹出“Claude is currently experiencing a temporary service disruption”，客户端登录失败，Console 报 500 错误。高峰时近 2000 名用户同时报障。消息迅速传开，社交媒体上一片哀嚎。

与此同时，另一条新闻正在刷屏：**伊朗无人机炸了 AWS 在阿联酋的数据中心**。

两件事撞到一起，一个极具戏剧性的叙事立刻成型——“AWS 中东机房被炸，Claude 跟着一起挂了！”媒体争相报道，连 Bloomberg 都出了快讯。全球程序员瑟瑟发抖，纷纷感叹“第三次世界大战先打掉了我的 AI 编程助手”。

![Claude 故障期间的状态页截图](outage.webp)


但这个叙事，**大概率是错的**。

------

## 事实一：到底什么挂了，什么没挂？

这是分析问题的起点，也是绝大多数人没搞清楚的关键。

Anthropic 在事故发生后明确确认：**Claude API（api.anthropic.com）工作正常**。出问题的是：


| 服务                             | 状态     |
|--------------------------------|--------|
| Claude API (api.anthropic.com) | **正常** |
| claude.ai（网页版）                 | 中断     |
| platform.claude.com（开发者控制台）    | 中断     |
| Claude Code（IDE 插件等）           | 错误率升高  |
| Claude for Government          | 正常     |


注意这个模式：**后端模型推理没挂，前端界面和认证系统挂了**。

Claude Code 的情况比较微妙——它本身走的是 API 通道，但在认证、会话管理等环节依赖了前端基础设施，所以出现了“错误率升高”但并非完全不可用的症状。如果你在故障期间用的是直接调 API 的方式，你甚至可能完全没感知到这次事故。正好比老冯这篇文章，正是使用 Claude Code 进行事实核查的。

这是一个非常重要的线索。这更像“认证与流量入口先爆，再向后扩散”，不是“核心推理集群被物理摧毁”。

------

## 事实二：AWS 中东被炸了什么？

我在另一篇分析中已经详细梳理过，这里简要回顾。

3 月 1 日，伊朗对阿联酋和巴林发射无人机/导弹，AWS 在中东的数据中心遭遇直接打击：

- **UAE（me-central-1）**：3 个可用区中 2 个瘫痪，`mec1-az2` 被直接命中起火，`mec1-az3` 连锁断电。
- **Bahrain（me-south-1）**：3 个可用区中 1 个受损，`mes1-az2` 附近打击造成物理损伤。
- **Israel（il-central-1）**：未受影响。

### 受影响的可用区

| 区域                   | 受影响 AZ       | 影响方式          | 影响程度     |
|----------------------|--------------|---------------|----------|
| UAE `me-central-1`   | **mec1-az2** | 无人机直接命中，引发火灾  | **完全瘫痪** |
| UAE `me-central-1`   | **mec1-az3** | 连锁电力中断        | **严重受损** |
| Bahrain `me-south-1` | **mes1-az2** | 附近无人机打击造成物理损伤 | **部分瘫痪** |

### 受打击占比

| 统计维度          | 受影响 / 总数 | 占比           |
|---------------|----------|--------------|
| 中东运营 AZ       | 3 / 9    | **33.3%**    |
| UAE 区域 AZ     | 2 / 3    | **66.7%**    |
| Bahrain 区域 AZ | 1 / 3    | **33.3%**    |
| 以色列区域 AZ      | 0 / 3    | **0%（未受影响）** |

中东 9 个运营可用区里挂了 3 个，占比 33%。UAE 区域丧失 2/3 容量。这确实是 AWS 历史上前所未有的物理灾难——人类第一次用导弹无人机打掉了云计算基础设施。但问题来了：**Anthropic 的服务跑在中东吗？**

------

## 事实三：Claude 不在中东

问题的关键在于，Anthropic 是一家总部位于旧金山的 AI 公司。Claude 的模型推理集群，需要的是大规模 GPU 算力——H100/H200 集群。这些资源部署在 AWS 的 `us-east-1`（弗吉尼亚）、`us-west-2`（俄勒冈）等美国本土核心区域，而不是中东。

AWS 中东区域（me-central-1、me-south-1）是面向中东本地客户的区域服务节点。这些区域主要服务于中东地区的企业客户，部署的是标准的云计算服务（EC2、S3、RDS 等），而非大规模 AI 推理集群。

AWS 官方故障隔离文档写得很直白：Region 之间相互隔离，单 Region 故障原则上不应拖垮其他 Region。

**如果 Claude 的核心推理引擎跑在中东，那 API 应该也挂了。** 但 API 完全正常——这直接否定了“导弹打掉 Claude 后端”的假说。有人可能会说：“也许 AWS 在全球做了流量重路由，导致其他区域过载？”理论上存在这种可能，但如果是后端过载，受影响的应该是 API 响应速度和可用性，而不是前端的登录认证系统。而实际表现恰恰相反——API 没事，前端认证挂了。

------

## 真正的原因：成功税

那么，真正的原因可能是什么呢？

让我们把时间线往前拨 48 小时，看看 3 月 2 日之前发生了什么。

### 五角大楼风波

2 月底，一场政治风暴席卷了 AI 行业：

1. **五角大楼要求 Anthropic 开放模型用于军事用途**，包括自主武器和监控系统，但被 Dario Amodei 拒绝。
2. **特朗普政府将 Anthropic 列为“激进左翼 AI 公司”**，下令联邦机构在 6 个月内停用。
3. **国防部长 Hegseth 将 Anthropic 定性为“供应链安全风险”**。
4. **OpenAI 随即签下 2 亿美元五角大楼合同**，接过了 Anthropic 拒绝的生意。

这在普通消费者中引发了剧烈反应。

[**特朗普下令全面封杀人工智能公司 Anthropic**](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491348&idx=1&sn=19e4d076c2013b354fca86af83b404b3&scene=21#wechat_redirect)。战争部长说这是“企业道德作秀”，但不得不说这个秀的效果确实极好。

### 用脚投票

- **2 月 28 日**：ChatGPT 在美国的卸载量暴涨 **295%**，远高于平日约 9% 的环比波动。
- **2 月 28 日**：Claude 下载量环比增长 **51%**。
- **2 月 28 日**：Claude **历史上首次在美国 App Store 下载量超过 ChatGPT**，登顶第一。
- **此前**：Claude 在 App Store 排名仅第 **42 位**，还是超级碗广告之后的高点。
- **2026 年以来**：Claude 免费活跃用户增长 **60%**，日注册量 **翻了四倍**。

Reddit 和 X 上掀起了 `#CancelChatGPT` 运动。用户自发撰写从 ChatGPT 迁移到 Claude 的教程。一场史无前例的 AI 产品“用脚投票”正在发生。

![Claude 下载量激增的统计截图](surge.webp)

### 然后 Claude 就挂了

从 App Store 第 42 名到第 1 名。日注册量翻四倍。海量新用户在同一个周末涌入。

**任何系统工程师看到这组数字，都知道接下来会发生什么。**

前端服务——Web 界面、认证系统、会话管理——这些不是按照“突然涌入几倍用户”来设计容量的。后端 GPU 推理集群可以通过排队和限流来扛住压力，但前端的登录、Session 管理、WebSocket 连接等服务，面对的是瞬时并发的冲击。

这完美解释了为什么：

- **API 没完全挂**：API 用户量相对稳定，本来就有较强的限流与配额机制。
- **前端挂了**：海量新用户涌入 `claude.ai` 注册和登录。
- **Claude Code 部分受影响**：依赖前端认证链路，但核心推理仍主要走 API。
- **Claude for Government 基本不受影响**：独立部署，用户量也不受消费级市场波动影响。

------

## 时间线对不上

再看时间线：


| 时间 (UTC)       | 事件                                |
|----------------|-----------------------------------|
| 3月1日 ~08:30    | AWS UAE 数据中心被无人机命中                |
| 3月1日 全天        | AWS 中东区域持续降级                      |
| 3月2日 06:56     | AWS Bahrain 设施断电                  |
| **3月2日 11:49** | **Claude 前端开始报错**                 |
| 3月2日 12:21     | Anthropic 确认 API 正常，问题在 claude.ai |
| 3月2日 13:22     | 问题定位为认证基础设施                       |
| 3月2日 ~17:00    | 修复上线，进入监控                         |

AWS 中东事件从 3 月 1 日凌晨就开始了。如果 Claude 的故障与之相关，为什么延迟了 **27 个小时**才出现？而且出现的不是后端推理故障，而是前端认证崩溃？

更合理的时间线是：经过一个周末的病毒式传播，周一（3 月 2 日）工作日开始，全球用户密集上线，前端系统在北京时间周一晚（美东周一早晨）迎来峰值流量，然后——扛不住了。

**11:49 UTC 恰好是美东早上 6:49**——美国东海岸用户开始新一天工作的时间。这不是巧合。

------

## Anthropic 自己怎么说？

Anthropic 官方在事后表示，公司过去一周一直在应对 **“unprecedented demand”（前所未有的需求）**。

这句话本身就是答案。他们没提 AWS 中东，没提导弹，没提区域故障。他们说的是——**需求太大了**。

这是一个好问题。甚至可以说，这是你能遇到的最好的问题之一。

在基础设施运维的世界里，有两种宕机：

1. **需求不足导致的宕机**：没人用你的服务，但它还是挂了，这说明系统质量有问题。
2. **需求过载导致的宕机**：太多人想用你的服务，这说明产品成功到超出容量预期。

Claude 遇到的是第二种。这不是一个工程灾难，这是一个 **成功税（Success Tax）**。

当然，“成功税”不代表可以不交。Anthropic 的前端基础设施在面对用户激增时的脆弱性暴露无遗。这也给所有 AI 公司上了一课：

- **前端和认证系统的弹性扩展同样关键**，不是只有 GPU 集群需要弹性。
- **消费级产品的流量特征与 API 完全不同**，API 增长往往是线性的，消费级产品却可能是指数型爆发。
- **政治事件可以在 48 小时内改变用户规模的数量级**，这不是传统容量规划能轻易预见的。

------

## 截至发稿：仍在波动

截至北京时间 3 月 3 日，Claude 的状态页显示仍有活跃事故：

- **06:59 UTC**：Claude Opus 4.6 出现 elevated errors，仍在调查。
- **03:15 - 04:43 UTC**：`claude.ai`、`cowork`、`platform`、Claude Code 出现 elevated errors。

![Anthropic 状态页后续更新](updates.webp)

服务在恢复与波动之间反复。这符合“容量不足逐步扩容”的特征，而不是“物理设施被毁等待重建”的特征。如果是后者，恢复曲线不会是这种渐进式的。

--------

## 结论

**AWS 中东数据中心被伊朗无人机炸了，这是事实。Claude 全球大宕机，这也是事实。但把这两件事画等号——那是在偷懒。**

证据链清晰地指向一个判断：Claude 的故障本质上是一次 **容量过载事故**，诱因是 OpenAI 五角大楼合同引发的大规模用户迁移。从 App Store 第 42 名到第 1 名，日注册量翻四倍——没有几个前端系统能在 48 小时内毫无准备地接住这种冲击。

导弹炸的是机房，挂的是中东客户的 EC2 和 S3。用户洪流冲的是登录页面，挂的是 claude.ai 的认证系统。

**两件事，两个原因，两条因果链。恰好撞在了同一个周末。**

对 Anthropic 来说，这反而是一个微妙的好消息：你的竞争对手（OpenAI）帮你做了你自己花多少钱都买不来的用户增长。代价只是一次前端宕机和一个尴尬的周末。

这个故障，恐怕 Dario Amodei 做梦都会笑醒。



------

声明：本文碳基智力含量约为 20%。

### References

`[1]` Anthropic confirms Claude is down in a worldwide outage - BleepingComputer:*https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-confirms-claude-is-down-in-a-worldwide-outage/*
`[2]`Anthropic's Claude Chatbot Goes Down For Thousands of Users - Bloomberg:*https://www.bloomberg.com/news/articles/2026-03-02/anthropic-s-claude-chatbot-goes-down-for-thousands-of-users*
`[3]`ChatGPT uninstalls surged by 295% after DoD deal - TechCrunch:*https://techcrunch.com/2026/03/02/chatgpt-uninstalls-surged-by-295-after-dod-deal/?type=AI*
`[4]`Claude beats ChatGPT in U.S. app downloads - Axios:*https://www.axios.com/2026/03/01/anthropic-claude-chatgpt-app-downloads-pentagon*
`[5]`Anthropic's Claude overtakes ChatGPT in App Store - Fortune:*https://fortune.com/2026/03/02/anthropic-claude-dario-amodei-number-one-app-store-openai-chatgpt-sam-altman-department-war/*
`[6]`AWS says drones hit two of its datacenters in UAE - The Register:*https://www.theregister.com/2026/03/02/amazon_outages_middle_east/*
`[7]`Claude Goes Down Globally as AWS Data Centers Burn - Awesome Agents:*https://awesomeagents.ai/news/claude-outage-march-2026-aws-middle-east/*
`[8]`Claude Status Page:*https://status.claude.com/*
`[9]`Why Is Claude Not Working? - Techloy:*https://www.techloy.com/why-is-claude-not-working-everything-we-know-about-the-anthropic-outage/*
`[10]`AWS Global Infrastructure: *https://aws.amazon.com/about-aws/global-infrastructure/regions_az/*
