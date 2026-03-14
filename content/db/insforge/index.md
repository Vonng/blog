---
title: "InsForge：为 Vibe Coding 而生的 Supabase"
date: 2026-03-11
author: 冯若航
summary: >
  InsForge 试图把数据库、认证、文件存储和语义层一起打包成一个更适合 AI Agent 的后端底座，像一个专为 Vibe Coding 设计的 Supabase。
tags: [AI, PostgreSQL, 开源]
---

老冯最近发现了一个有意思的项目：**InsForge**。口号是——为 AI 编程设计的 Supabase。

Apache 2.0 开源，GitHub 约 2000 Star，核心技术栈是 PostgreSQL + PostgREST + Deno + TypeScript，5 个容器就能跑起来。老冯收集大宝贝的毛病又犯了，赶紧把它加入到 Pigsty 代自建全家桶里来（随下个版本一起发布）。

这个项目触及了一个真实的痛点，值得展开聊聊。

--------

## Vibe Coding 的“最后一公里”

2025 年以来，“Vibe Coding” 已经从一个 meme 变成了真实的生产力。你打开 Cursor，用自然语言告诉 Agent：“给我做一个带评论功能的博客”，十分钟后一个漂亮的 React 前端就出来了。

然后呢？

**前端搭好了，数据往哪存？用户怎么登录？文件传到哪里去？** Agent 对着后端基础设施一脸茫然。你得手动去开数据库，配 RLS 策略，搞 OAuth，部署 Serverless Function……一顿操作猛如虎，一看时间凌晨三点半。

这就是 Vibe Coding 的悖论：**AI 能在几分钟内生成任意复杂的前端代码，却搞不定后端那一坨配置、认证、存储的苦活。** 不是 Agent 不够聪明，而是传统后端服务压根不是为 Agent 准备的。正如 Vibe Coding 之父 Andrej Karpathy 说的，他只花了一天把那个算热量的小程序写出来，却花了整整七天才让它在服务器上跑起来。

![Karpathy 关于部署最后一公里的说法](last-mile.webp)

InsForge 想解决的，就是这个“最后一公里”。老冯的 Pigsty 之前其实也有过类似的原型——目录里写好 CLAUDE.md，你用 Claude Code 说“给我做一个应用”，它也会用 PostgreSQL 给你搞出来。现在好了，有个更完整的开源方案出来了，也省老冯的事儿了。


--------

## 它到底是什么？

从技术架构上看，InsForge 提供六大后端原语：

| 模块                 | 说明                      | 底层实现             |
|--------------------|-------------------------|------------------|
| **Database**       | PostgreSQL 数据库，建表即出 API | PostgREST v12    |
| **Authentication** | 注册/登录/OAuth/会话管理        | 自建 JWT 认证        |
| **Storage**        | S3 兼容的文件存储              | 本地磁盘或 AWS S3     |
| **Edge Functions** | Serverless 函数           | Deno Runtime     |
| **Model Gateway**  | 统一 LLM 接口               | OpenRouter 路由    |
| **Realtime**       | WebSocket 实时消息          | PG LISTEN/NOTIFY |

另外最近还加了站点部署（Site Deployment）和邮件等实验性功能。

听起来跟 Supabase 差不多？差别在架构层面。


--------

## 关键差异：语义层

InsForge 的核心设计是在 AI Agent 和后端原语之间加了一层**语义层（Semantic Layer）**，通过 MCP 协议暴露给 Agent：

```
AI Coding Agent（Cursor / Claude Code / Copilot / ...）
        │
        ▼
InsForge Semantic Layer（MCP Server）
        │
        ├── Authentication
        ├── Database（PostgreSQL）
        ├── Storage（S3）
        ├── Edge Functions（Deno）
        ├── Model Gateway
        ├── Realtime
        └── Deployment
```

这层语义层做三件事：**暴露上下文**——Agent 通过 MCP 直接“看到”后端的表结构、Schema、RLS 规则；**操作原语**——Agent 直接通过 MCP 工具调用来建表、配 OAuth、部署函数，不需要你在 Dashboard 上点来点去；**检查状态**——执行完可以查日志、验证结果，形成闭环。

用他们的话说，这叫 **Context Engineering for AI Agents**。


--------

## 实际体验

以自建部署为例：

```bash
git clone https://github.com/insforge/insforge.git
cd insforge
cp .env.example .env
docker compose -f docker-compose.prod.yml up
```

跑起来一共 5 个容器：PostgreSQL 15（`ghcr.io/insforge/postgres:v15.13.2`）、PostgREST v12.2、InsForge 主服务、Deno 2.0 运行时、Vector 0.28 日志收集。跟 Supabase 自建动辄十几个容器比起来，确实清爽。

然后打开 `http://localhost:7130` 的 Dashboard，按页面引导连接 MCP Server 到你的编辑器。也可以直接命令行装：

```bash
npx @insforge/install --client cursor \
  --env API_KEY=your_key \
  --env API_BASE_URL=http://localhost:7130
```

目前支持 Cursor、Claude Code、Windsurf、Cline、Roo Code、Trae 等主流 AI 编辑器。

![InsForge 支持的 AI 编辑器](editors.webp)

接下来就可以在编辑器里对 Agent 说：“帮我创建一个用户表，包含 email 和 name 字段，然后搞一个注册登录流程”。Agent 会自动通过 MCP 了解 InsForge 的能力、创建表、配置认证、生成前端代码。整个过程**你不需要打开任何 Dashboard、不需要手动配置任何东西**。


--------

## 老冯的看法

**InsForge 做对了一件事：把“Agent 能不能理解后端”作为第一优先级来设计。** 传统 BaaS（Supabase、Firebase）是为人设计的，Dashboard 做得再漂亮，对 AI Agent 来说也是不可见的。Agent 需要的是结构化的 API、一致的响应格式、可检查的状态——InsForge 围绕这个需求重新设计了接口。

**当然也有一些局限性：**

- 2025 年 7 月成立，团队 5 人，项目仍处于早期阶段。
- 底层还在使用 PG 15，而老冯这边已经把它拉到了 PG 18。
- 文档偏薄，高级自建场景如高可用、备份和安全加固基本没有覆盖。

说到底，它的组件（PostgREST + Deno + JWT）单个来看都不新，核心壁垒是那层 MCP 语义层的工程实现。

但从趋势上看，**“Agent-Native Infrastructure” 这个方向是真实存在的**。当越来越多的代码由 AI Agent 写出来时，后端基础设施如何更好地服务于 Agent，而不是继续要求人类在 Dashboard 上点鼠标，这是一个值得认真思考的问题。


--------

## 架构拆解：简化版 Supabase

| 组件       | Supabase               | InsForge                |
|----------|------------------------|-------------------------|
| 数据库      | PostgreSQL 15          | PostgreSQL 15.13（自定义镜像） |
| REST API | PostgREST              | PostgREST v12.2         |
| 认证       | GoTrue（Go）             | 自建 JWT（TypeScript）      |
| 实时       | Realtime（Elixir）       | WebSocket（TypeScript）   |
| 存储       | Storage API + imgproxy | 自建 Storage（TypeScript）  |
| 函数       | Deno Edge Runtime      | Deno 2.0 Runtime        |
| 网关       | Kong / Envoy           | 无（直连）                   |
| 连接池      | Supavisor（Elixir）      | 无                       |
| 日志       | Logflare + Vector      | Vector 0.28             |
| **总容器数** | **~15 个**              | **5 个**                 |

Insforge 策略很清楚：砍掉 Supabase 里的重量级组件（GoTrue、Realtime Elixir Server、Kong、Supavisor、imgproxy），全部用 TypeScript 重写，换来极简部署。对于 Vibe Coding 的典型场景——快速原型、个人项目、黑客松——够了。

最关键的是，**PostgreSQL 仍然是绝对的核心**。所有数据存在 PG 里，所有 API 从 PG Schema 自动生成，认证信息加密存储在 PG 中，RLS 策略在 PG 层面执行。InsForge 本质上就是一个围绕 PostgreSQL 构建的、面向 AI Agent 的薄封装层。


--------

## 纳入 Pigsty 全家桶

说到 PostgreSQL 就得提 Pigsty。

老冯看完 InsForge 架构之后，第一反应是：**它最大的弱点恰好是 Pigsty 最大的强项**。InsForge 自带的 PostgreSQL 只是一个单节点 Docker 容器，没有高可用、没有监控、没有自动备份。而 Pigsty 管理的 PG 集群天生就有 Patroni HA、VictoriaMetrics 监控、pgBackRest 备份、连接池、负载均衡——把 InsForge 的数据库层替换成 Pigsty 管理的实例，等于给一辆跑车换了个专业底盘。

![Pigsty 与 InsForge 结合的架构](stack.webp)

所以，**InsForge 已经被纳入了 Pigsty 全家桶**。（当然，也是 Claude 干的，哈哈）下个版本会作为可选模块一起发布。Pigsty 负责数据库层的高可用与运维，InsForge 负责面向 AI Agent 的应用层接口。当然，你也可以选择独立自建 InsForge，或者只用它的 MCP Server 对接自己的 PG 实例。

本来老冯自己还想糊一个 Pigsty 里面的 Vibe 平台，现在好，有现成的了，那我也很开心的划掉了这一项 TODO。这也是老冯一贯的理念：**PostgreSQL 是数据库世界的 Linux，围绕它的每一个优秀组件都值得被纳入生态、组合使用。** Pigsty 不是要把所有东西都自己写一遍，而是要让所有基于 PG 的好东西都能**用得上、管得住、跑得稳**。

当然，如果你都已经准备用这种产品形态了，用云服务耍一耍也不错。
