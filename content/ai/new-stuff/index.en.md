---
title: "A Busy Few Days in Infrastructure and AI"
date: 2026-04-23
author: |
  [Ruohang Feng](https://vonng.com) ([@Vonng](https://vonng.com/en/))
summary: >
  Ubuntu 26.04 LTS, Qwen3.6-27B, ChatGPT Images 2.0, Privacy Filter, Anthropic Mythos, and the Claude Pro controversy all landed in quick succession. Here are the infrastructure and AI developments worth watching.
tags: [AI, Ubuntu, Qwen, OpenAI, Anthropic]
ai: true
---

The past couple of days have been unusually busy for the infrastructure crowd. Ubuntu released its biennial LTS today. Alibaba's Qwen team dropped a 27B dense model yesterday that beats its own previous 397B MoE flagship. The day before that, OpenAI launched Images 2.0, then followed it yesterday with a small open-source model built specifically for data redaction. Here are a few of the more interesting developments.

## Ubuntu 26.04 LTS Is Out

Today, April 23, Canonical officially released Ubuntu 26.04 LTS, code-named "Resolute Raccoon." April 23 is something of a favorite date in Ubuntu history: Ubuntu 9.04, 15.04, and 20.04 LTS all launched that day.

As the first LTS release in two years, 26.04 has a long support horizon. Standard support runs through April 2031, Ubuntu Pro's extended ESM support through 2036, and the optional Legacy add-on through 2041. For enterprise users, this is essentially a foundation you can choose once and run for a decade.

A few highlights matter to me in particular.

**First, the Linux 7.0 kernel.** The version number looks like a milestone, but it is really just Linus deciding that the 6.x minor-version numbering had gone on long enough and rolling over to 7.0. The changes themselves are not revolutionary. For Ubuntu, however, the jump from the 6.8 kernel in the 24.04 era to 7.0 naturally brings much broader hardware and driver coverage.

**Second, both AMD ROCm and NVIDIA CUDA are now in the repositories.** Canonical worked closely with AMD to bring ROCm into the official repository, so installing the AI compute stack for AMD GPUs is now as simple as `sudo apt install rocm`. CUDA gets the same treatment. Anyone who moves between the two ecosystems can finally stop hunting down driver packages and wrestling with dependency hell.

**Third, security has been modernized across the board.** TPM-backed full-disk encryption, post-quantum cryptography enabled by default, a Rust rewrite of sudo (`sudo-rs`), and mandatory cgroup v2—systems using container stacks older than Docker 20.10 will be blocked from upgrading. None of these changes is spectacular on its own, but together they strengthen Ubuntu's position in compliance-heavy server environments.

For public-cloud images, AWS, GCP, and Azure have all promised launch-day support. Chinese clouds such as Alibaba Cloud, Tencent Cloud, and Huawei Cloud will probably lag by a few months, as they historically have. There is no need to wait for local testing, though: the Docker image is already available, and a Vagrant box can be started directly with `cloud-image/ubuntu-26.04`.

I have also started adapting Pigsty for 26.04, beginning with the repository layout. Missing dependencies are inevitable on a new operating system; I will add the PostgreSQL extensions one by one.

## Qwen3.6-27B: A 27B Dense Model Beats a 397B MoE

Yesterday, April 22, the Qwen team released the second open-source model in the Qwen3.6 family: **Qwen3.6-27B**, a 27B dense model.

According to Qwen, Qwen3.6-27B beats its previous open-source flagship, Qwen3.5-397B-A17B—a mixture-of-experts model with 397B total parameters and 17B active parameters—across all major coding benchmarks. The team published the numbers: 77.2 versus 76.2 on SWE-bench Verified, 53.5 versus 50.9 on SWE-bench Pro, 59.3 versus 52.5 on Terminal-Bench 2.0, and 48.2 versus 30.0 on SkillsBench. The gaps on the last two are substantial.

That is remarkable. A 27B dense model reaching the level of its own previous flagship is a milestone in itself. The Qwen3.5-397B-A17B weights on Hugging Face take up 807 GB; Qwen3.6-27B is only 55.6 GB, or just over 14 GB after 4-bit quantization. An RTX 5090 or an M5 Max can run it without breaking a sweat, with tens of tokens per second as the baseline.

This means running personal-assistant workloads locally is becoming practical. An assistant like that does not need frontier-level intelligence; it needs to be capable enough, fast enough, and private enough. Qwen3.6-27B lands right on that line. I am glad Qwen is still committed to open source. Frankly, Alibaba Cloud and Qwen have done the open-model ecosystem a real service. It has been quite a while since I last roasted Alibaba Cloud.

## Two Releases from OpenAI in Two Days

### ChatGPT Images 2.0

First, **ChatGPT Images 2.0**, launched the day before yesterday, April 21. In the API it is called `gpt-image-2`. Many friends have asked where to use it. There is nothing to hunt down: just ask ChatGPT to draw something in the regular chat box. The default has already switched to the new model.

Friends in my group chats have spent the past few days putting it through its paces and producing all kinds of stunts. Someone designed a Taobao storefront mockup for pigsty.io. Someone else typed "comic-book-style Pigsty beating up RDS" and got remarkably polished design assets.

The shock to designers is every bit as large as the one Claude Code delivered to programmers a year ago. Images 2.0 is also so good at fabricating screenshots and interfaces that the naked eye can no longer tell what is real. The old "pics or it didn't happen" standard can go straight in the trash.

### Privacy Filter: A Small Model Built for PII Redaction

Yesterday, OpenAI also released an interesting open model called [Privacy Filter](https://openai.com/index/introducing-openai-privacy-filter/). Its weights are available on [Hugging Face](https://huggingface.co/openai/privacy-filter) under the Apache 2.0 license.

This is not a chat model. It is a **small model built specifically to detect and redact PII—personally identifiable information**. It uses the gpt-oss sparse-MoE architecture, with 1.5B total parameters and 50M active parameters, supports a 128K context window, and runs directly on a laptop or even in a browser. It is not an autoregressive generative model, either. It has been converted into a bidirectional token classifier: one forward pass labels every token, then Viterbi-constrained decoding emits BIOES-style span annotations. It can identify eight classes of private information: account numbers, private addresses, email addresses, names, phone numbers, URLs, dates, and keys. Out of the box, it reaches 96% F1 on the PII-Masking-300k benchmark and 97.43% on the corrected dataset.

Its positioning is the interesting part. OpenAI explicitly says this is not an anonymization tool, not a compliance certification, and not a substitute for policy review. **It is simply one component in a privacy-by-design system.** The use case is straightforward: when processing enterprise data in bulk, run it through a local PII filter before sending the redacted content to a cloud LLM. For organizations that want ChatGPT in internal workflows but worry about sensitive data leaking out, this model provides a lightweight component for the very front of the data pipeline.

This release also highlights an industry trend I have been watching for some time. Compared with the hundred-billion-parameter arms race, more vendors this year are getting serious about **small, specialized models**. A 1.5B model that does one job, runs on a laptop or in a browser, and permits commercial use under Apache 2.0 can sometimes deliver more practical value to enterprise AI engineering than yet another 600B model advertised as a GPT killer.

## Anthropic: Unauthorized Mythos Access and the Pro Plan Fiasco

Anthropic has had a rough couple of days.

First, Mythos. **Claude Mythos Preview** is a vulnerability-research model Anthropic introduced recently and described as "too dangerous to release publicly." It found a 27-year-old vulnerability in OpenBSD and a 16-year-old bug in FFmpeg that automated testing tools had exercised five million times without catching. It also autonomously chained several Linux kernel vulnerabilities into a local privilege-escalation exploit. Anthropic gave limited access to companies including Amazon, Apple, Cisco, JPMorgan, and NVIDIA as part of a defensive collaboration called Project Glasswing.

Then Bloomberg reported that a small Discord group had obtained unauthorized access to Mythos through an environment run by one of Anthropic's third-party vendors. Anthropic confirmed that it was investigating and said it had found no evidence that its own systems were affected. The group appears to have been motivated by curiosity rather than sabotage. Even so, it is an awkward episode: a model deemed "too dangerous to release" was accessed by a small Discord circle.

Then came the Pro-plan fiasco. On the afternoon of April 21, users discovered that Anthropic had removed Claude Code from the $20-per-month Pro plan. The documentation and pricing page had both been updated, leaving Claude Code available only on the $100 and $200 Max plans. Reddit and Twitter erupted. A few hours later, Anthropic's head of Growth, Amol Avasare, posted an explanation on Twitter: this was only a small experiment affecting **2% of new signups**, while existing Pro and Max users were unaffected. Anthropic then reverted the pricing page and documentation.

What his explanation implied is more interesting than the experiment itself. When the Max plan was first designed, Claude Code did not exist, Cowork did not exist, and agents running for hours were not part of the everyday workflow. Over the course of a year, per-subscriber usage has exploded. **The current plan structure can no longer bear the load.** I have made this point before: a heavy user can extract $10,000 worth of API usage at list price from a $200 subscription, effectively receiving a 50x subsidy.

That structure cannot last. OpenClaw creator Peter Steinberger has put it plainly: coding plans are, bluntly, compute subsidies in exchange for your code data. For me, that is a great deal. My code is open source, so vendors can take all of it. But anyone working with private code and data should think carefully about that trade-off.

## A Mysterious Product in Private Beta

One more interesting AI product entered early private beta last night. I tried it, and the experience was excellent. But this is an early private beta, so I obviously cannot say what it is. My assessment: it is at least in the same league as Manus, with a potentially higher ceiling. I will say more when broader testing begins.

## Closing Thoughts

There has been a lot to digest over the past two days, so I have focused on the main developments. Ubuntu 26.04 will have the longest-lasting impact as a foundational operating system release. Qwen3.6-27B and Privacy Filter point toward the "small and specialized" model trend. The impact of OpenAI Images 2.0 is still unfolding. Anthropic's Mythos incident and Pro-plan controversy, meanwhile, reveal two new problems created by rapidly advancing model capabilities: security boundaries are constantly being tested, while subscription economics collide with the reality of growing usage.

Well, infrastructure in 2026 is certainly not boring.
