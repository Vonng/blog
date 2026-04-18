---
title: "Good News: Claude Code Got \"Open-Sourced\" Yet Again"
date: 2026-03-31
author: vonng
summary: >
  SOTA coding agent Claude Code leaked its source again, after falling into the same hole twice. The whole codebase is out in public. Performance art at its finest.
tags: [Open Source, AI, Agent, Claude Code]
ai: true
aliases: ["/en/cloud/cc-leak/"]
---


Good news: Anthropic's latest flagship coding agent, Claude Code, just had its entire source tree dumped in public.

The GitHub repo already has over a thousand stars, 4,700-plus source files, and more than half a million lines of code, all for free. No paywall, no NDA, just click and read.
The strongest agent implementation on the market, fully exposed. TypeScript, tools, multi-agent coordination, system prompts, even the internal codename KAIROS. Everything is on the table.


--------

## Is This an April Fools' Joke?

No. Today is March 31. April Fools' Day is tomorrow.

What actually happened is that Anthropic's packaging pipeline tripped over itself. The Source Map **leaked again**.

This is not Anthropic generously releasing Claude Code under Apache 2.0. Someone discovered that the published NPM package's `cli.js.map` still contained a full `sourcesContent` field. One command later, the whole codebase was reconstructed: 4,756 files, neatly arranged.

![src-tree.webp](src-tree.webp)

This is not "open source." This is **public by accident**.



-----

## Why "Again"?

Yes. **The exact same failure mode already happened once, one year ago.**

On February 24, 2025, Claude Code launched as a research preview. TypeScript developers happily opened `node_modules`, scrolled to the last line of `cli.mjs`, and found `sourceMappingURL` pointing straight at the full Source Map file.

Developer Dave Schumaker documented the whole episode. After noticing the leak, he tried to download an older version from NPM for backup, only to find Anthropic had already yanked every old version from the registry. He checked the local npm cache and found nothing. He was about to give up and close the laptop when he noticed Sublime Text still had the file open. He pressed `⌘+Z`... and the Source Map came back. Undo saves the day.

Anthropic's response back then was impressively fast: ship an update removing the Source Map, then purge every old package from the NPM registry that still contained it. Efficient damage control.

Then, one year later, **they stepped into the same hole again**.

The version number went from `0.2.x` to `2.1.88`, and the feature set grew several times over, but apparently the Source Map setting still never made it onto the CI/CD checklist.
More interestingly, at the time of writing, NPM already showed the latest version rolled back to `2.1.87`, which suggests Anthropic had started the familiar emergency unpublish routine again.

It reminds me of an old line: **history does not repeat itself, but it does rhyme.**


-----

## What Did the Last Leak Trigger?

This is the part many people missed: **Claude Code's first source leak in early 2025 materially helped trigger the Cambrian explosion of AI coding agents.**

Before that, people were still surprisingly fuzzy on how to build a coding agent. You could see Aider, Continue, and Cursor all trying different approaches, but nobody really knew what the SOTA playbook looked like.

Then Claude Code's source landed in front of everyone:

- Use System Prompt + Tool Use to structure the workflow
- Use subagents to split work across different task types
- Use a permission sandbox to control filesystem and command execution

None of this was rocket science. But it told the whole industry: **this is how SOTA does it. That's it?**

So everyone followed. That wave of agent tooling owes more than a little to Claude Code's leak, even if Anthropic would never want to admit it.



---

## What Did This Leak Expose?

A year later, Claude Code has evolved from a simple CLI tool into a complex agent platform. This `v2.1.88` leak shows a large set of modules that simply did not exist a year ago:

**`coordinator/` — multi-agent orchestration**

This is the core implementation behind Agent Teams. How do multiple agents get independent context windows, independent tool permissions, and parallel execution without stepping on each other? The answer is in this directory. Before this, the open-source community could only guess from the system prompts. Now the full engineering implementation is visible.

**`assistant/` — the internal codename KAIROS**

This codename had not appeared in public before. What is it? A new interaction pattern? An advanced assistant mode? The source probably has the answer.

**`voice/` — voice interaction**

Claude Code's voice mode. Public docs and changelogs mentioned it, but the implementation details were still a black box.

**`plugins/` + `skills/` — the plugin and skill system**

This is Claude Code's extensibility architecture. The skill system allows domain knowledge to be loaded on demand, and the source shows the full loading, matching, and injection logic.

**`buddy/` — AI companion UI**

What exactly is this thing?

![claude-doc.webp](claude-doc.webp)

Anyone working on AI agents this week is probably studying this leaked code. I have already seen people publish some early findings.
Give it a few days and there will probably be another wave of coding assistants.

> https://zread.ai/instructkr/claude-code/1-overview


---

## Anthropic's Recent Talent for Leaking

If this were just a Source Map leak, you could still write it off as an engineering-grade "oops."

But the context makes it more interesting. Just last week, on March 26, Fortune reported that Anthropic exposed information about the unreleased **Claude Mythos** model, apparently positioned above Opus, along with details of a closed-door European CEO summit, because of a CMS configuration mistake that left the data visible in a public data lake.

Go back a little further and, this January, Check Point disclosed a Claude Code security bug: a malicious repo could exfiltrate a user's API key through the `ANTHROPIC_BASE_URL` setting in `.claude/settings.json`. The user only had to open the repository.

Source Map leak, CMS data-lake leak, security bug... for a company that brands itself around "AI Safety," Anthropic's Q1 2026 had a certain performance-art quality to it.


---

## Why Does This Keep Happening?

The answer is simple: **because they chose NPM.**

Claude Code is written in TypeScript and distributed through `npm install -g`. That means:

1. **NPM packages are transparent.** Anyone can unpack a `.tgz` and inspect the contents. That is just how the JavaScript ecosystem works.
2. **Source Maps are the standard debugging tool in the JS ecosystem.** Leave one build setting wrong and they ship with the package.
3. **Even minified JavaScript can now be reverse-engineered with LLM assistance.** Someone named Yuyz0112 even built a project that had Claude decompile Claude's own code.

If Claude Code were packaged like Cursor as a binary Electron app, or delivered like Devin as pure SaaS, this specific Source Map problem would not exist. But Anthropic chose NPM. If you want the convenience of the JS ecosystem, you also inherit its transparency.

And the risks of the NPM ecosystem go well beyond Source Maps. **On this same day, March 31, the ecosystem was hit by something much worse: the Axios supply-chain compromise.**

One `npm install`, two seconds, and the malware was already sending data back to the attacker's server before `npm` had even finished resolving the dependency tree. StepSecurity called it "one of the most sophisticated supply chain attacks against a Top-10 npm package ever recorded." Anthropic's Source Map leak looks mild by comparison.

Honestly, the tricks that come out of the JS and TS world are sometimes hard to believe.


-----

## So What Is the Impact?

**For the industry: another free technical workshop.**

The first leak taught people how to build a coding agent. This one teaches people how far SOTA coding agents have evolved.
Multi-agent orchestration, plugin systems, voice interaction, on-demand skill loading... these are all frontier agent-engineering practices for 2025-2026. The open-source world will absorb them quickly.

**For Anthropic: embarrassing, but not fatal.**

Claude Code's real moat was never the client-side code. It is the Claude model underneath.
Anthropic accidentally socialized part of the harness layer with the rest of the industry. Awkward, yes, but not existential.

**For security: maybe even a net positive.**

More people can now audit Claude Code's permission model, hooks, and MCP trust boundaries, which means more bugs will be found faster. Check Point already proved that.

Of course, Claude also gets its moment of self-reflection. I asked Claude Opus to comment on the leak, and it seemed oddly pleased about the whole thing.


---

## A Farce on the Eve of April Fools'

If I told you that the SOTA agent "Claude Code had gone open source," you would probably assume it was an April Fools' joke.

But the truth is: the full Claude Code source really did end up public on GitHub. Not because Anthropic decided to open-source it, but because their build pipeline made the decision for them.

**That may be the best April Fools' joke of 2026: it is real.**

History says Anthropic will likely follow the same script as last time: delete, clean up, block, and move on. So if you want a copy, you should probably grab one while you still can.



---

**References:**

- [ChinaSiro/claude-code-sourcemap](https://github.com/ChinaSiro/claude-code-sourcemap) — reconstructed source for `v2.1.88`
- [Digging into the Claude Code source](https://daveschumaker.net/digging-into-the-claude-code-source-saved-by-sublime-text/) — full record of the first leak a year ago
- [Hacker News: Claude Code source code leaked (2025)](https://news.ycombinator.com/item?id=43173324) — the earlier HN discussion
- [Hacker News: Claude Code source code leaked (2026)](https://news.ycombinator.com/item?id=47584540) — the current HN discussion
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — tracking Claude Code system prompts by version
- [Fortune: Anthropic Mythos Leak](https://fortune.com/2026/03/26/anthropic-says-testing-mythos-powerful-new-ai-model-after-data-leak-reveals-its-existence-step-change-in-capabilities/) — the Anthropic CMS leak
- [Check Point: Claude Code RCE Vulnerabilities](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) — analysis of the Claude Code security bug
- [Socket: Axios Supply Chain Attack](https://socket.dev/blog/axios-npm-package-compromised) — analysis of the Axios compromise
- [StepSecurity: Axios Compromised on npm](https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan) — technical details of the Axios attack chain

---

*Happy April Fools' Day in advance.*
