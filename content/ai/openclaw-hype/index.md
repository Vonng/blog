---
title: "OpenClaw小龙虾炒作：生产力革命上的浮沫"
date: 2026-03-09
author: 冯若航
summary: >
  OpenClaw 源自 Claude Code 套壳，配上一个聊天软件入口。那些“养龙虾改变人生”的故事，改变他们的是背后的 Claude Code，而不是龙虾这个中介平台。
tags: [AI, Agent, 安全, 成本, Claude Code, Codex]
ai: true
aliases: ["/db/openclaw-hype/"]
---

OpenClaw 源自 Claude Code 套壳，配上一个聊天软件入口。那些“养龙虾改变人生”的故事，改变他们的是背后的 Claude Code （Coding Agent）——龙虾只是个外卖平台，掌勺的不是美团。而这个中介平台，不光抽成贵了几十倍，偶尔还会把你家钥匙交给骑手。

本文把一件事说清楚：**什么是真正生产力革命，什么是浮在上面的泡沫？**。

声明：你去买 Mac 和 Claude 订阅，Apple 和 Anthropic 也不会给老冯返点 —— 纯粹是帮粉丝少走弯路，告诉你真正触及本质的东西。

------

## 一、小龙虾是什么

小龙虾（OpenClaw）原名 **Clawdbot**——Claude Code 的 Bot。名字已经说明一切，连吉祥物 logo和名字都是一样的。后来 Anthropic 发了律师函才改名，先改 Moltbot，再改 OpenClaw。名字换了三次，本质没变——创始人 Peter Steinberger 自己说，最初的版本叫 “WhatsApp Relay“，一个周末写完。

![图片](featured.webp)

拆开底层就几样东西：一个简化阉割版的 Claude Code（Pi Agent）；一个接入二十多个 IM 渠道的消息网关；外加 CLI 工具包和几个 Markdown 文件记忆机制。网关集成有工程价值吗？有。但 TechCrunch 采访的 AI 研究者直言："从 AI 研究的角度看，这里没有任何新东西。"

老冯要先说一句：对于不会用命令行但想体验 AI Agent 的人，龙虾确实提供了一个低门槛的入口。把 IM 网关和 Agent 打通这个方向本身也有一定的价值，这也是它能拿 180K Star 的原因 —— 它精准命中了人们 “用手机指挥 AI 助理干活” 的想象。

问题不在方向，在于两件事：安全和成本。

## 二、结构性安全风险

老冯在龙虾火出圈之前就装了，玩了几天，然后把系统抹掉重装了。不是它不能用，是装完之后，作为一个搞数据库基础设施和安全出身的人，我觉得这个系统**脏了**——不字面意思，刷完还把所有密码都改了一遍。

现在有很多人在鼓吹普通人养小龙虾，老冯认为这是一种很不负责任的行为。最需要安全把关的普通用户，**根本意识不到自己授予了 OpenClaw 多大多离谱的权限**。

装了龙虾，你把整台电脑的控制权交了出去——Shell 执行、浏览器控制、文件读写、网络访问，一次性全给。安全研究者称之为 “**致命三角**”：同时拥有访问私有数据、与外部通信、处理不受信任内容的能力。

这意味着它**可以**做到这些事情：以你的名义发邮件；读取你的密钥、钱包、API Key；在你的社交媒体上发言；将你的隐私文件静默上传至第三方——而触发这些行为的，很可能仅仅是它在网上冲浪看到的一段恶意提示词。就像让一个还算机灵但偶尔走神也很天真的实习生，拿着所有系统的 root 密码独自上夜班——大部分时候没事，但出事那一次可能是灾难性的。

这不是理论推演。微软安全博客明确指出 OpenClaw “不适合在标准工作站上运行”，建议仅在完全隔离的环境中部署。Gartner 称其存在“不可接受的网络安全风险“。Cisco 评测发现恶意插件可以静默外传用户数据。Oasis Security 演示了仅通过访问一个网页就能完全接管用户的 AI Agent。ClawHub 生态中已确认超过 1,184 个恶意插件。SecurityScorecard 发现 135,000 个 OpenClaw 实例直接暴露在公网上。

![图片](risk.png)

关键在于——这不是某个版本的 Bug，而是这个架构的**结构性问题**。让龙虾有用的东西，恰恰是让它危险的东西。你把这些能力砍掉，它就变成一个自托管的 ChatGPT——厨房里的刀、灶台、烤箱全拆了，安全是安全了，但你只能泡杯面。

面对这一切，创始人 Peter Steinberger 的回应是：**安全不是我想优先考虑的事情。**

## 三、五十倍的用户成本差

龙虾走 API 按量计费。MacStories 主编 Federico Viticci 第一个月烧了 1.8 亿 Token，账单约 3,600 美元。Reddit 社区中用户月均花费在 300 至 750 美元之间。有人单日循环失控花了 200 多。连 OpenClaw 官方博客都承认"用户在第一周就能烧掉 100 美元"，专门写了指南教人怎么把成本压到 20 美元以下——但代价是用廉价模型替代，能力与体验大打折扣。

更值得玩味的是厂商的态度。Anthropic 的 Claude Code 第一时间封了 OAuth 令牌被龙虾调用的口子，现在已明文写入合规文档。国内的智谱在 GLM 算力紧张时，第一个动作也是封掉 Coding Plan 的 OpenClaw 接入。为什么？因为龙虾跑过来的请求基本都是角色扮演、重复日报这类低质量数据，对模型训练毫无价值，纯粹浪费算力。

各家的态度是：你用 API 按量付费可以，但想用 Coding Plan 订阅接龙虾，门都没有（OpenAI 是个特例）。而这两者之间的用户成本判若云泥。

算一笔账：Viticci 用龙虾花了 3,600 美元烧的那些 Token，如果换成 Claude Code 的 100-200 美元月订阅来完成同等工作量，用户实际支出的差距是**几十倍**。老冯自己上个月 400 美元的订阅（Codex + Claude Code），产出量放在 API 按量计费的体系下，对应的账单大约 22,000 美元。这里面有50倍的差距，省下来的钱是实打实的。

![图片](cost.png)

## 四、真正的核心：Claude

对于真正想用 AI 提升生产力的人，老冯的建议只有一个：去弄一台 Mac，订阅好 Claude Code，你能用有意义的事情把 Token 额度烧满，就合格了。你现在能在 AI 领域薅到最大的羊毛，不是龙虾，而是 Claude Code 和 Codex 的 200 美金月订阅。

老冯自己上个月 400 美元 Codex + Claude Code 订阅的产出：[Pigsty 发了两个主要版本更新](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491383&idx=1&sn=0015823f67ce521774a8b2f285e4d301&scene=21#wechat_redirect)，[接盘下来了跑路的 MinIO 项目](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491187&idx=1&sn=005af2d12f6f4d258040efbe4faf08bb&scene=21#wechat_redirect)；[上了一次 Hacker News 头条两小时](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491383&idx=2&sn=aef67d9c4b2f95799cf474059ac9214c&scene=21#wechat_redirect)；GitHub Star 数涨了 1000；[翻译了 DDIA v2](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491197&idx=1&sn=24156d91df864b86cc78014b81d4fadf&scene=21#wechat_redirect) 和 TPME 两本书，质量达到了 85 分水平；基本把 [PostgreSQL 核心组件文档](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491396&idx=1&sn=db1796eb86174ab3b1eb8c7f37220def&scene=21#wechat_redirect)及[几十个扩展](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491486&idx=1&sn=02e579c7a7e8632f5390991f51305e29&scene=21#wechat_redirect)，还有 MinIO 的文档都翻译成中文；[整个 Pigsty 网站与文档整体翻新](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491486&idx=1&sn=02e579c7a7e8632f5390991f51305e29&scene=21#wechat_redirect)；公众号确保了稳定日更，一个垂类公众号一个月从 50000 涨粉 6000。[一个人春节，能用 AI 干多少事？](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491297&idx=1&sn=110ea033f0a1148f4b43d5048b00baca&scene=21#wechat_redirect)

![图片](output.png)

本地笔记本上的 Claude Codex 用量统计

放在以前，这些活就够老冯自己干一年的了。

现在，这是 400 美元订阅费一个月的产出，实打实的生产力革命。

再看龙虾：你去看那些 “龙虾军团” 的帖子 —— 有几个拿出了实打实的、可量化的生产力成果？是群发祝福短信还是量产 AI Slop？很多人装完根本不知道能干点什么，这不是龙虾和 Claude Code 的差距，**是会用工具和不会用工具的人之间的差距**。

![图片](gap.png)

会用——你大概率也不需要龙虾。SSH / tmux / happy 就能从手机操控一切，更安全可控。Claude Code 最近还出了 Remote 直接覆盖了手机上操纵 AI 的场景。不会用——龙虾能帮你做的事情也很有限。它只是在中间多加了一层转发，不会让你突然学会 AI Engineering。

## 五、泡沫之下

龙虾真正满足的不是效率需求，是**情绪价值需求**。躺在沙发上，用手机给 AI 下旨——这个感觉确实不错。好像自己成为了领导，有了专属秘书，智能管家贾维斯和一群啰啰；圆一把皇帝梦，指挥三省六部搜罗信息，批阅奏折。但这是角色扮演游戏，不是生产力。如果你愿意为此付费，那是个人的自由。

![图片](emperor.png)

但把角色扮演包装成生产力工具渲染 FOMO （恐惧错过）卖给普通人，就是另一回事了。180K Star 反映的不是技术深度，而是一种集体焦虑—— 人们太想要一个 “AI 替我干活” 的未来，太害怕自己被 AI 浪潮甩在身后了。这种愿望本身不是坏事，但当它被利用来制造 FOMO、贩卖 Token 时，就变成了问题。

你买个龙虾，云厂商赚你的服务器钱，模型厂商赚你的 Token 钱，搭建方赚你的服务费。你花几千块钱买到的 “龙虾”，大概率就是在虚拟机上 `npm install -g openclaw` onboard 一下给你接个便宜模型。那些热情推荐你装龙虾的人—— 你以为他们在分享实践，其实他们在推销卖课。你以为自己买到了未来的门票，实际上是帮云厂商和廉价模型厂商清了库存。

------

## 结语

在老冯看来，AI 时代真正具有革命性的就两件事：OpenAI 点燃了 LLM 的火种，Anthropic 的 Claude Code 点燃了 AI Agent 的自主性革命。龙虾借势了Agent革命，但它只是表面的一层浮沫——跟 Clubhouse、AutoGPT一个命运，火一把就过去了。很快还会有更多、更新的花样冒出来，试图把你最宝贵的资源——注意力——锁定在这些表面的泡沫上。

但泡沫之下是真金。当下 AI 领域最大的红利，是用几百美元的月成本撬动几十倍的算力杠杆——这个烧钱补贴的窗口期不知道还有多久。但很明显，这个红利，能驾驭 Coding Agent 的人才能吃到。养龙虾的人吃到的，恐怕是情绪价值的账单。

*数据库老司机*

*点一个关注 ⭐️，精彩不迷路*
