---
title: Claude 新模型 Fable 体验：风水轮流转
date: 2026-06-10
author: 冯若航
summary: >
  Claude Fable 确实有洞察力，是当之无愧的新 SOTA；但价格昂贵，动态降级、限时订阅与强制留档也让体验大打折扣。
tags: [AI, Claude, Anthropic, Fable, Agent]
ai: true
---

今天早上，Anthropic 正式发布了新模型 **Claude Fable** —— 就是前阵子传得沸沸扬扬的 Mythos「神话」的民用阉割版。毕竟是号称“[AGI 水准的模型](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491844&idx=1&sn=0237bd818c234299a31d3bbfe91ee8f6&scene=21#wechat_redirect)”，老冯当然第一时间上手实测了一把，看看它到底有几斤几两。

先说结论，确实强，新 SOTA。但是贵，吃相也难看。

![Claude Fable 发布公告](claude-x.webp)

两个月前 Mythos Preview 刚放出风声时，我写过一篇《[AGI已经来了，但你有船票吗？](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491844&idx=1&sn=0237bd818c234299a31d3bbfe91ee8f6&scene=21#wechat_redirect)》，聊的就是顶级 AI 能力正在被圈禁起来这件事。现在看来一语成谶 —— 这次连命名都懒得掩饰：**Mythos（神话）供奉给通过审查的「领主」，Fable（寓言）讲给平民听。** 同一个底层模型，Fable 是阉割加锁版。

![Claude Fable Benchmark 对比](benchmark.webp)

这次发布之前，我已经把 Claude 降级到了 100 刀套餐，平时也基本在吃灰 —— 主力是 Codex，Claude 就负责打打杂、做做 review。这回用完 Fable，我的评价是：Claude 又支棱起来了，又可以打了。原地升回 200 刀 Max 套餐。几个真实场景跑下来，我的感受是：**Fable 确实有洞察力，是当之无愧的新 SOTA。**

果然就像之前在《[退订 Claude，拥抱 Codex](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247492092&idx=1&sn=462593783ba20a0ad6878a0630eaf897&scene=21#wechat_redirect)》说的那样，AI 行业风水轮流转，城头变幻大王旗，SOTA 几个月就一换。

---

## 实测：能不能看见 Codex 看不见的问题？

我的测试方法简单粗暴：不跑 Benchmark，不看竞技场天梯，就拿手头真实的工作场景让它去 review，看它能不能发现真正有价值的问题，给出实打实的改进。

我平时 vibe coding 的工作流是双模型对抗：**Codex 5.5 当主力，Claude 4.8 当备用 reviewer** —— 一个补丁必须让两边都认可「没有进一步改进空间」，我才会验收提交。所以俺到判断标准也很直接：在双模型已经收敛的状态上，新模型还能挖出新问题，那它的能力就是实打实的更强。对我来说，这比任何跑分都有说服力。

**案例一：MinIO CVE 补丁复审。** 我让 Fable 去 review 之前给 MinIO 社区分支打的几个 CVE 安全补丁，看是否还有改进空间。结果它真挖出了几个新问题 —— 拿回去问 Codex，Codex 也承认：这些点确实值得修复补充。

![MinIO CVE 补丁复审](minio-review.webp)

**案例二：pg_exporter 的 PG 19 适配。** 之前我让 Codex 做了 PostgreSQL 19 Beta 1 的兼容工作，把新版本的可观测性指标加了进去。这次让 Fable 重做一遍，产出质量明显好于 Codex 此前能达到的收敛状态。

![pg_exporter PG 19 适配复审](pg-exporter-review.webp)

**案例三：Pigsty PITR 脚本改进。** 之前我在数据库里提供了一个应急用的时间点恢复脚本，那么这次，我也请 Claude Fable 重新 review 了一下，基本上将各个地方没有覆盖到的细节都填好了。在面面俱到、Codex 没法再进一步改进的状态下，Fable 反而能发现一些新的改进点。

![Pigsty PITR 脚本复审](pitr-review.webp)

---

## 槽点：能力给你，体验恶心你

当然，老冯对这次 Fable 发布也有一肚子意见。

**槽点一：动态降级机制。** Fable 加入了反蒸馏与投毒机制，外加一套极其讨厌的动态降级：系统一旦检测到你在做 AI Agent 相关的工作，就会主动给你降智 —— 用着用着，啪一下跳回 Opus 4.8，甚至聊点日常问题都可能触发。这种「吃屎」般的使用体验，实在让人不爽。

举个例子，我在跟 Claude 讨论之前那个 Agent／AI 相关主题的问题时，每次都给我从 Fable 原地跳回 Opus 4.8。Anthropic 给的官方口径是「超过 95% 的对话不会触发降级」。翻译一下：约有 5% 的概率会触发。这个比例，相当离谱。

![Claude Fable 对话](fable-session.webp)

![Fable 动态降级至 Opus 4.8](opus-fallback.webp)

![SemiAnalysis 对 Fable 审查机制的评价](model-filter.webp)

**槽点二：12 天限时体验。** Fable 目前不在 Claude Code 的订阅计划里。从今天到 22 号这 12 天，100／200 刀的订阅用户可以限时尝鲜；22 号之后，就只剩 API 按量付费一条路。官方解释是产能不足、算力不够，以后算力上来了可能进订阅标配 —— 但没有时间表。

![Claude Code 中的 Fable 限时体验](trial-window.webp)

**槽点三：强制数据留档。** 只要你用 Fable，无论是不是企业用户，所有流量一律强制保留 30 天，还会被 review，这跟之前可不太一样。说白了，还是那个老配方 ——「**数据换算力**」。对在意数据隐私与合规的企业用户来说，这是个没法装看不见的变化。

---

## So，算一笔经济账

API 什么价呢？老冯之前在《[AI时代的最大红利](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247491524&idx=1&sn=2259533174395bb9eb976c8e56c008a5&scene=21#wechat_redirect)》里面算过这笔账，两百刀的订阅用满，可以薅走 API 标价一万美元左右的 Token。也就是按量付费是订阅用满价格的 50倍。反过来说，走 API 计费，你要付出几十倍的成本去买同样的用量。

![Claude Fable API 价格对比](api-price.webp)

所以对日常使用而言，长期用 API 跑 Fable 纯属冤大头。也正因如此，这 12 天的订阅窗口期才显得格外珍贵 —— 这是普通用户以订阅价格触达顶级智力的唯一通道。

所以老冯这几天的计划，就是把之前模型都收敛的问题和特性，都用 Fable 重新审一遍、改一遍。我目前的计划分三步：

1. **走一步看一步，能薅的羊毛先薅到手；**
2. **把之前一些有价值的讨论，用 Fable 重新深挖一遍；**
3. **把过往的 patch 和 feature，统统让它再 review 一轮。**

这也是我建议你现在立刻去做的事：评估好这 12 天的窗口期，不用就过期作废了。无论如何，你都应该亲手摸一摸当前 SOTA 模型，或者说“AGI 模型”的能力边界在哪里 —— 这种体感，看一百篇评测文章也替代不了。

---

## 其他一些有趣的案例与消息

![Claude Fable 案例汇总](fable-cases.webp)

![Fable 与 Opus 的太空模拟对比](space-simulation.webp)

![Fable 的纽约天际线与风暴城市案例](city-simulation.webp)

![Mythos 体验报告](mythos-review.webp)

---

## 写在最后

总体而言，老冯的判断是：对于日常使用 —— 哪怕是专业的日常使用 —— **Fable 的能力过剩了**，GPT 5.5／Opus／Sonnet 级别的模型早已绰绰有余。

但对于前沿场景：安全漏洞挖掘、疑难杂症的诊断定位、开放式的研究探索 —— 这类「**智力越高越好、上不封顶**」的场景，Fable 才能兑现真正的巨大价值。

**智力溢价，只在智力边界上兑现。** 这大概就是 Mythos 时代的游戏规则：神话握在领主和大祭祀手里，寓言则是讲给平民听的。而你眼下能做的，就是趁城门还没关上 —— 进去亲眼看看。
