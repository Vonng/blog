---
title: "Claude Code 可观测性怎么做？"
date: 2026-01-25
summary: >
  获取 Claude Code 的详细 OTEL 日志与指标，放入 Victoria 全家桶，放进并通过 Grafana 监控面板呈现。
tags: [ClaudeCode, 可观测性, Victoria, Grafana]
---

# Claude Code 可观测性怎么做？

昨天老冯 [发了条推特](https://x.com/RonVonng/status/2014972720489091514)：「做了个 Claude Code Grafana Dashboard，研究下它是怎么做决策、用工具、
调 API 花钱的。」结果发现非常多的用户都对这个主题感兴趣。

![推文截图](tweet-dashboard.webp)

这是我没想到的，所以今天就来聊一聊 Claude Code 的可观测性。

-------

## Claude 的可观测性

老冯的想法其实很简单 —— 我想了解 Claude Code 内部工作细节。虽然 Claude Code 不开源（[**其实被开源过一次**](https://mp.weixin.qq.com/s/xaeVafPxUfAgQSzl-n3w2w)），
但你可以通过它的监控指标和日志，分析出它的大概工作原理。

![Grafana监控面板](grafana-dashboard.webp)

Claude Code 提供 OTEL 格式的指标和日志，配置起来也很简单。
你只要指定几个环境变量，就可以让它主动推送到支持 OTEL 的监控系统，然后用 Grafana 进行可视化。

```bash
# Claude Code OTEL 配置
export CLAUDE_CODE_ENABLE_TELEMETRY=1             # 启用监控
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_LOG_USER_PROMPTS=1                    # 如果要隐藏 Prompt，设置为 0
export OTEL_RESOURCE_ATTRIBUTES="job=claude"      # 添加你自己的标签
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://10.10.10.10:8428/opentelemetry/v1/metrics     # 指标端点，打入 VictoriaMetrics
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://10.10.10.10:9428/insert/opentelemetry/v1/logs    # 日志端点，打入 VictoriaLogs
export OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=cumulative
```

> 你可以放在 `.bash_profile` / `/etc/profile.d/claude.sh` 或者直接写入 `~/.claude/settings.json` 的 `env` 字段。


难点在于：我去哪找这么一个监控系统和 Grafana 呢？后来我看见这么多人都有需求，就干脆做了一个开箱即用的配置模板。


--------

## 监控系统

你只要找一台 Linux 服务器，运行几行命令把它拉起来，就会自带一个 Claude Code 环境，所有东西都帮你配好了（包括监控）。你也可以直接把自己的 Claude Code 监控接进去。

![Piglet沙箱文档](piglet-doc.webp)

实际上，如果你已经会用 Claude Code，并不需要了解太多细节。你只要告诉它有这么个东西、能干这么个事，并给它准备一台虚拟机，剩下的事它都能帮你自动搞定。我看有人评论留言就是这么说的，哈哈！

![用户部署反馈](tweet-user-feedback.webp)


## 监控事件说明

- [Claude Code 可观测性文档](https://code.claude.com/docs/en/monitoring-usage)

这个监控面板其实很朴素：上方可以选择会话（Session ID），选择之后，下方会列出各种事件。你可以通过拖动时间轴来查看处理任务过程中产生了哪些事件。

目前最主要的事件分为以下四类：

1. **User Prompt**：你对它说了什么，或者给了什么提示词
2. **API Request**：调用 API 的请求
3. **Tool Decision**：系统决定使用什么工具
4. **Tool Result**：工具返回的具体结果

每个事件都有对应的字段。大体上，只要看一眼这个面板，就能明白整个任务的处理流程是怎么回事了。

举个例子，最简单的事件就是 User Prompt，你给 Claude Code 发一条消息，就会产生一个该事件：

![User Prompt事件](event-user-prompt.webp)

**User Prompt** 事件之后，通常是 **API Request**，也就是调用 API 模型。这里会有一个 model 字段——Claude Code 区分了快速模型和高质量模型，这里我用的是 GLM-4.7 作为例子，有些简单快速的请求会由 GLM-4.5-air 来处理。

API Request 事件有几个核心字段：Cost 是开销，然后是四个 Token 指标。Token.In/Out 是输入输出的 Token 数，Token Cache Read 则是缓存命中的指标。

![API Request事件](event-api-request.webp)

**API Request** 完成之后，通常会有一个 **Tool Decision** 事件，即模型决定使用什么工具。比如 Bash、Read、Write、Search 等，然后会有一个 Decision Source/Result，表示根据什么标准（配置文件/询问用户/……）选择「批准」或「拒绝」。

**Tool Decision** 事件之后是 **Tool Result** 事件。这是调用工具的关键事件，关键字段包括：Tool 的命令、说明、错误、参数、UserID、成功与否等。

![Tool Result事件](event-tool-result.webp)

其实还有一些其他类型的事件，但最主要的就是上面这四类。更多细节可以参考 Claude Code 的监控文档：https://docs.anthropic.com/en/docs/claude-code/monitoring

## 沙箱环境

当然，老冯也知道「授人以**鱼**不如授人以**渔**」，但光说原理没用，干脆直接把东西做好给你算了。所以我做了一个开箱即用的沙箱环境，里面包含了一套完整的 Victoria 监控系统与 Grafana 监控大盘，随便找台 1C2G 的 Linux 虚拟机几分钟就能装好。

这个沙箱除了监控 Claude Code，还可以干很多有趣的事情。最主要的是，它已经替你配置好了常用的 Web Coding 工具：Claude Code、VS Code、Open Code。里面自带 PostgreSQL 和 Nginx，所以如果你需要一个云服务器开发环境，也可以试试。

![VS Code Vibe界面](vscode-vibe.webp)

你也可以在这里直接使用不用翻墙的 GLM 模型，多配置一行参数就好了。关于 Claude Code 最美妙的就是：既然你都已经用它了，那大概也不需要操心这些细节是怎么弄的，**直接动嘴让它自己去 Vibe 就好了**。

```yaml
# 切换为其他模型，比如 GLM 4.7
claude_env:
  ANTHROPIC_BASE_URL: https://open.bigmodel.cn/api/anthropic
  ANTHROPIC_API_URL: https://open.bigmodel.cn/api/anthropic
  ANTHROPIC_AUTH_TOKEN: your_api_service_token # 填入你的 KEY！
  ANTHROPIC_MODEL: glm-4.7
  ANTHROPIC_SMALL_FAST_MODEL: glm-4.5-air
```

PIGLET.RUN 的另一个妙处就在于，只要提供好高度确定性的基础设施，它已经能完成很多工作了。
扮演一个中级 DBA / 开发者的角色，直接用它来写代码、调试、测试、部署，效率会非常高。
这一点老冯会在后面专门写一篇 DBA Agent 相关的介绍文章。

![数据库需求金字塔](tweet-pyramid.webp)
