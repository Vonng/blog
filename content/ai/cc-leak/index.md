---
title: "好消息！Claude Code 又双叒叕开源了！"
date: 2026-03-31
author: 冯若航
summary: >
  SOTA Coding Agent —— Claude Code 源代码又泄漏了，在同一个阴沟里翻了两次船。代码全部白给，堪称行为艺术。
tags: [开源, AI, Agent, Claude Code]
ai: true
aliases: ["/cloud/cc-leak/"]
---


好消息！好消息！走过路过不要错过！Anthropic 最新旗舰编码智能体 Claude Code，源代码全部公开了！

GitHub 仓库已有上千 Star，四千七百多个源文件，五十多万行代码，全部免费！不要 998，不要 98，点开就能看！
地表最强 Agent 实现全部白给，全场 TypeScript 统统白给！Tools 实现白给！多 Agent 协调白给！System Prompt 白给！
内部代号 KAIROS 都白给！挥泪大放送，走过路过千万不要错过！


--------

## 这是一个愚人节笑话吗？

不是，今天是 3 月 31 号，明天才是愚人节。

实际上是 Anthropic 打包流水线翻车了，Source Map **又泄了！**

![leak-news.webp](leak-news.webp)

不是 Anthropic 大发慈悲搞了个 Apache 2.0。而是有人发现：**NPM 发布包里的 `cli.js.map` 中完整保留了 `sourcesContent` 字段**。一行命令提取，全部源码还原。4756 个文件，整整齐齐。

![src-tree.webp](src-tree.webp)

这不是“开源”，这是 **开裆裤**。



-----

## 为什么是“又泄了”？

没错。**一模一样的翻车方式，一年前就来过一次。**

2025 年 2 月 24 日，Claude Code 作为研究预览版首次发布。TypeScript 开发者们兴冲冲地打开 `node_modules`，翻到 `cli.mjs` 的最后一行，赫然发现了 `sourceMappingURL`——直指完整的 Source Map 文件。

有位叫 Dave Schumaker 的开发者完整记录了这段经历：他发现泄露后，想去 NPM 下载旧版本备份——发现 Anthropic 已经从 NPM Registry 上下架了所有旧版本。去翻本地 npm cache——也没找到。正要认命关电脑，发现 Sublime Text 还开着那个文件，按了一下 `⌘+Z`……撤销大法好，Source Map 又回来了。

Anthropic 当时的反应堪称迅速：推更新删除 Source Map，同时从 NPM Registry 下架所有包含 Source Map 的旧版本。亡羊补牢，雷厉风行。

![old-leak.webp](old-leak.webp)

然后一年后，**同一个坑，又跳了进去**。

版本号从 `0.2.x` 涨到了 `2.1.88`，功能翻了好几倍，但构建流水线的 Source Map 配置显然没有写进 CI/CD 的 checklist 里。
有意思的是，截至发稿时 NPM 上显示的最新版本已经回退到了 `2.1.87`——看来 Anthropic 又开始了熟悉的“紧急撤包”流程。

这让我想起一句老话：**历史不会简单地重复，但它确实押韵。**


-----

## 上次翻车引发了什么？

这是很多人不知道的：**2025 年初 Claude Code 的第一次源码泄露，实质性地催化了 AI Coding Agent 赛道的“寒武纪大爆发”。**

在此之前，大家对“怎么构建一个 Coding Agent”这件事其实相当模糊。你能看到 Aider、Continue、Cursor 各有各的路子，但谁也不确定 SOTA 的做法是什么。

然后 Claude Code 的源码摊在了所有人面前：

- 用 System Prompt + Tool Use 组织工作流
- 用子代理分工处理不同类型的任务
- 用权限沙箱控制文件系统和命令执行

这不是什么火箭科学。但它告诉了整个行业：**SOTA 就是这么做的。原来就这？**

于是大家纷纷跟进。那一波爆发，Claude Code 的泄露功不可没——虽然 Anthropic 肯定不想承认这一点。



---

## 这次又暴露了什么？

一年过去了，Claude Code 从一个简单的 CLI 工具进化成了一个复杂的 Agent 平台。这次 `v2.1.88` 的泄露，展示了大量一年前完全不存在的新模块：

**`coordinator/` —— 多 Agent 协调**

这是 Agent Teams 功能背后的核心实现。如何让多个 Agent 各自拥有独立上下文窗口、独立工具权限、并行工作又不互相打架？答案就在这个目录里。开源社区之前只能通过 System Prompt 猜测其工作方式，现在能看到完整的工程实现了。

**`assistant/` —— 内部代号 KAIROS**

这个代号此前从未公开出现过。它代表什么？是一种新的交互范式？一种高级助手模式？源码里应该有答案。

**`voice/` —— 语音交互**

Claude Code 的语音模式。这在公开文档和 Changelog 中有所提及，但实现细节一直是黑箱。

**`plugins/` + `skills/` —— 插件和技能系统**

这是 Claude Code 的可扩展性架构。技能系统允许按需加载领域知识——源码中能看到完整的加载、匹配和注入机制。

**`buddy/` —— AI 伴侣 UI**

这又是个什么东西？

![claude-doc.webp](claude-doc.webp)

这几天所有搞 AI Agent 的应该都会来琢磨、研究这份泄露的代码。实际上我已经看到社区有人放出来一些研究结果了。
估计用不了几天，又会有一大堆编码助手冒出来了。

![zai-claude.webp](zai-claude.webp)

> https://zread.ai/instructkr/claude-code/1-overview


---

## Anthropic 最近的“泄露体质”

如果只是 Source Map 泄露，还可以说是个 “oops” 级别的工程事故。

但联系上下文看就有意思了：就在上周（3 月 26 日），Fortune 杂志报道 Anthropic 因为 CMS 配置错误，导致未发布的 **Claude Mythos** 模型信息（内部定位为 Opus 之上的新层级）和一场欧洲 CEO 闭门峰会的细节被安全研究者在公开数据湖中发现。

再往前推，今年 1 月 Check Point 披露了 Claude Code 的安全漏洞 CVE-2026-21852——恶意仓库可以通过 `.claude/settings.json` 中的 `ANTHROPIC_BASE_URL` 配置窃取用户的 API Key，用户只需要打开仓库就会中招。

Source Map 泄露 + CMS 数据湖泄露 + 安全漏洞……对于一家以 “AI Safety” 为核心招牌的公司来说，2026 年 Q1 的表现多少有些行为艺术的味道。


---

## 为什么会反复翻车？

答案很简单：**因为他们选择了 NPM。**

Claude Code 用 TypeScript 编写，通过 `npm install -g` 全局安装分发。这意味着：

1. **NPM 包是透明的。** 任何人都可以解压 `.tgz` 检查内容，这是 JS 生态的基本特性。
2. **Source Map 是 JS 生态的标准调试工具。** 构建流水线中只要有一个配置项没关对，它就会跟着包一起发出去。
3. **即使是 minified 的 JS，也可以通过 LLM 辅助逆向还原。** 有人（Yuyz0112）专门做了一个项目，让 Claude 自己反编译自己的代码。

如果 Claude Code 像 Cursor 一样用 Electron 打包二进制分发，或者像 Devin 那样做纯 SaaS，Source Map 泄露这个问题根本不会存在。但 Anthropic 选择了 NPM——选择了 JS 生态的便利性，就要接受它的透明性。

而说到 NPM 生态的风险，Source Map 泄露其实只是最温和的那种。**就在今天（3 月 31 日），NPM 生态爆出了一起严重得多的事件：Axios 供应链投毒攻击。**

**一个 `npm install`，两秒钟，木马就已经开始向攻击者的服务器回传数据了——`npm` 甚至还没解析完依赖树。
** StepSecurity 的安全研究者称这是“有记录以来针对 Top-10 NPM 包最精密的供应链攻击之一”。Anthropic 的 Source Map 泄露简直是“小巫见大巫”。

老实说，前端圈 JS、TS 圈的这些花活，真是让人瞠目结舌。


-----

## 所以影响是什么？

**对行业：又一次免费技术培训。**

一年前的泄露让大家知道了“Coding Agent 该怎么做”。这一次让大家知道了“SOTA Coding Agent 现在进化到了什么程度”。
多 Agent 编排、插件系统、语音交互、技能按需加载……这些都是 2025-2026 年 Agent 工程的前沿实践。开源社区会消化得很快。

**对 Anthropic：尴尬但不致命。**

Claude Code 的核心竞争力从来不是客户端代码 —— 而是底层的 Claude 模型能力。
Anthropic 在 Harness 维度上和大家共产了一把，虽然尴尬，但不会伤筋动骨。

**对安全：可能反而是好事。**

更多人能审计 Claude Code 的权限模型、Hooks 机制、MCP 信任边界，意味着更多漏洞会被更快发现。Check Point 已经证明了这一点。

当然也少不了 Claude 的自我反思环节。我请 Claude Opus 自我点评了这场泄露事件，看上去它还透露出一股高兴的劲儿。

![claude-comment.webp](claude-comment.webp)


---

## 愚人节前的滑稽戏

如果我告诉你 SOTA Agent “Claude Code 开源了”，你可能会觉得这是愚人节玩笑。

但事实是：Claude Code 的完整源码确实在 GitHub 上公开了。只不过不是 Anthropic 主动开源的，而是他们的构建流水线替他们做了这个决定。

**这大概是 2026 年最好的愚人节笑话：它是真的。**

历史告诉我们，一年前的那次泄露，Anthropic 紧急删除、清理、封堵。这次大概率也会重复同样的流程。所以如果你想看的话——趁现在赶紧去保存一份吧。



---

**参考链接：**

- [ChinaSiro/claude-code-sourcemap](https://github.com/ChinaSiro/claude-code-sourcemap) — 本次 `v2.1.88` 源码还原
- [Digging into the Claude Code source](https://daveschumaker.net/digging-into-the-claude-code-source-saved-by-sublime-text/) — 一年前第一次泄露的完整记录
- [Hacker News: Claude Code source code leaked (2025)](https://news.ycombinator.com/item?id=43173324) — HN 上的历史讨论
- [Hacker News: Claude Code source code leaked (2026)](https://news.ycombinator.com/item?id=47584540) — 这次的 HN 讨论
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — 每个版本的 System Prompt 追踪
- [Fortune: Anthropic Mythos Leak](https://fortune.com/2026/03/26/anthropic-says-testing-mythos-powerful-new-ai-model-after-data-leak-reveals-its-existence-step-change-in-capabilities/) — Anthropic CMS 泄露事件
- [Check Point: Claude Code RCE Vulnerabilities](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) — Claude Code 安全漏洞分析
- [Socket: Axios Supply Chain Attack](https://socket.dev/blog/axios-npm-package-compromised) — Axios 供应链投毒事件分析
- [StepSecurity: Axios Compromised on npm](https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan) — Axios 攻击链技术细节

---

*提前祝大家愚人节快乐*
