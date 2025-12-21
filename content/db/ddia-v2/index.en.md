---
title: DDIA 2nd Edition, Chinese Translation
date: 2025-08-10
author: vonng
summary: |
  The second edition of Designing Data-Intensive Applications has released ten chapters. I translated them into Chinese and rebuilt a clean Hugo/Hextra web version for the community.
tags: [DDIA]
---

The new DDIA—Designing Data-Intensive Applications, 2nd Edition—has published its first ten chapters. With Claude Code Max 20× on my side, it took two days to translate the released chapters into Chinese and re-render them via Hugo + Hextra for a tidy Markdown/Web reading experience.

> [Read it online](https://ddia.vonng.com): https://ddia.vonng.com

This is still a preview. Martin is publishing as he writes; Parts I and II are done, Part III (“Batch,” “Stream,” “Do the Right Thing”) should follow within months. The English version is freely available on [O’Reilly Safari](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/).

The second edition isn’t a light edit. Chapter 1 is brand new, and many others were rewritten to reflect recent shifts—e.g., the indexing chapter now covers vector indexes like HNSW. Translating let me re-read the material; it felt like seeing old ideas with fresh eyes.

Bottom line: this book won’t make you a master of any specific database, but it gives you the conceptual map to navigate the field, recognize the real problems, and spot BS instantly. Even veterans get something out of revisiting it, and the updated references are a fantastic jumping-off point for deeper study.

> Most modern apps are data-intensive. This book walks from storage internals to architecture with clarity. Architects, DBAs, backend engineers, PMs—all win.
> 
> It blends theory and practice. Almost every scenario it describes has smacked me in real life. “If only I’d read this earlier…”
> 
> It explains origins instead of dumping definitions, traces evolution instead of stacking facts, makes complex ideas approachable without losing depth. The citations at each chapter’s end are gold.
> 
> It arms you with a framework to design, implement, and critique data systems. Once you internalize it, you can duel “experts” with confidence 🤣.
> 
> Back in 2017 this was the best tech book I read. Leaving it untranslated felt wrong. Translating was my way of paying it forward—and a great excuse to sharpen both English and Chinese.

I finished the first translation in 2017. Eight years flew by. That was when I pivoted from “full-stack engineer” to PostgreSQL DBA; DDIA nudged me down that path. Translating it opened doors, built reputation, and gave me my first taste of open source fun.

Back then it took about three months of nights/weekends. This time? GPT/Claude plus an existing baseline made it painless. Honestly I spent more time tweaking Hugo/Hextra themes than translating—the Claude Code Max subscription (USD 250/month) earned its keep. I let it chew through English/Chinese, polish, and reformat for an entire day and just dinged the Opus 4.1 quota.

Getting good AI translations still takes craft. Dumping whole chapters fails token limits and quality. My workflow:

1. Extract the terminology list, polish the translations.
2. Pull the table of contents, have GPT-5 think hard about the phrasing.
3. Feed Claude the outline, chunk the work, have it read English + v1 Chinese to build context (compacting history as needed).
4. Translate incrementally using the glossary + outline as guardrails.

This beats brute-force prompting by miles.

Presentation-wise, I ditched plain Markdown/Docsify in favor of Hugo + Hextra. It solved most layout quirks and taught me some new Markdown extensions. I’m pretty happy with the result.

I’m now proofreading the second edition in full. Claude’s output is remarkably readable—light-years ahead of old Google Translate or DeepL. Some sentences still carry translation cadence, but nothing blocking comprehension. I’ll keep polishing.

The project is open source. Found a typo? Have a better phrase? File an issue or PR on GitHub. Contributions welcome:

https://github.com/Vonng/ddia
