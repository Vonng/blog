---
title: "A Packaging Patch Has Been Corrupting Valkey's Memory Accounting Since 2017"
date: 2026-08-09
authors: [vonng]
summary: >
  Codex found an old Valkey bug affecting Debian's packages and every official Valkey .deb.
  One line in a packaging patch releases a glibc allocation with Valkey's own deallocator, so the
  server either segfaults or silently stops accepting writes until you restart it.
tags: [Redis, Linux, Repository, Open Source]
---

I was updating the Redis module in Pigsty recently, adding Valkey as an alternative engine, and hit an upstream bug while packaging it.

**If your Valkey runs on Debian or Ubuntu, and one day the disk fills up or the data directory permissions go wrong so snapshots stop saving — every failed save drops the instance's memory counter a little. Once it goes below zero it wraps to `18446744073709518664`. From then on, if you have `maxmemory` set, the server refuses every write until you restart it.**

```
> SET foo bar
(error) OOM command not allowed when used memory > 'maxmemory'.
> GET foo
"bar"                          # reads are fine
```

There is plenty of free memory. Nothing appears in the logs. `used_memory_rss` stays normal and RSS graphs are flat. The only number moving is `used_memory`, and nobody alerts on memory usage slowly going *down*.

**If you built from source, or linked against the bundled jemalloc, it's blunter: one failed `SAVE` segfaults the server.**

The cause is a single line in a packaging patch. Its lineage goes back to 2017, it was fixed once in Redis, came back in Valkey, and eventually got copied into Valkey's own release pipeline — so **every `.deb` on `download.valkey.io`**, from 7.2 through 9.1, carried it.

The fix is now merged. Here's how it surfaced.

---

## What's wrong

Valkey has two error paths that log the working directory when a snapshot fails to land. Upstream uses a stack buffer, so there's nothing to release.

Debian's packaging patch moves it to the heap:

```c
char *cwdp = get_current_dir_name();        /* glibc malloc() */
serverLog(LL_WARNING, "... in server root dir %s ...", cwdp, ...);
zfree(cwdp);                                /* <- here */
```

The motivation is fine: keep a 4 KB array off the stack.

The problem is the last line. `get_current_dir_name()` allocates through **glibc's `malloc()`**. `zfree()` is **Valkey's own deallocator**. They are not interchangeable.

The usual reaction is "it's a free, what could go wrong". But `zfree()` isn't a wrapper around `free()`. It does three things: ask the allocator how big the block is, **subtract that from `used_memory`**, and then release it.

Step two is wrong unconditionally. This allocation never went through Valkey's allocator, so it was never added to `used_memory` — and `used_memory` is unsigned, so subtracting past zero wraps it.

Whether steps one and three break depends on which jemalloc the binary was linked against. With the system `libjemalloc.so` (Debian, Ubuntu, and the official `.deb`s), the pointer at least belongs to the right heap, so nothing crashes and you only get the corrupted counter. With the bundled private jemalloc — upstream's default — it can't find the pointer in its own bookkeeping and dereferences null:

```
valkey-server(je_malloc_usable_size+0x68)
valkey-server(valkey_free+0x28)
valkey-server(rdbSave+0x18c)
valkey-server(saveCommand+0x4c)
```

Look familiar? Same top-of-stack as [redis/redis#7927](https://github.com/redis/redis/issues/7927) from 2020 — the same bug, in Redis.

The saving grace is that only synchronous saves in the main process accumulate. `BGSAVE` and scheduled saves fork, so the damage dies with the child. The real-world trigger is a full disk, wrong permissions, or a read-only filesystem, combined with something calling synchronous `SAVE` in a loop: a monitoring script, a backup cron, a client that retries.

It waits until you already have a problem, then quietly adds a second one.

## How I found it

Not through any clever analysis. Upstream's own test suite caught it.

While reworking the Valkey DEB packaging for [Pigsty](https://pigsty.io), I ran `runtest` as usual. Three cases in `unit/shutdown` failed and the server left a crash report.

Our packages use the bundled jemalloc, so we were on the crashing side — louder symptoms than the official packages, and much easier to catch. Following the crash trace up, then opening `debian/patches/0003-*.patch`, and there it was.

The relevant test, by the way, deliberately creates a **directory** named `dump.rdb` to force `rename(2)` to fail — which is exactly one of the two patched paths.

Once I understood the mechanism, the first thing I did was disbelieve myself: two Valkey versions, three builds each (pristine, patched, patched-and-fixed), against three allocators, on two architectures. The result held.

Then I spent longer than the technical work checking whether someone had already reported it. Worth noting one trap: two of Debian's search endpoints were broken at the time and **returned zero rows for bugs I knew existed**. Without a "this query should definitely return something" control, I'd have walked away with a confident false negative.

Nobody had reported it.

## Where the line came from

The patch header goes back further than I expected:

```
From: Chris Lamb <lamby@debian.org>
Date: Thu, 16 Nov 2017 03:40:26 +0900
Subject: Use get_current_dir_name over PATHMAX, etc.
```

- **2017** — Chris Lamb writes the patch for Debian's **Redis** packaging.
- **2020** — a `zfree(cwdp)` shows up in Redis's copy and blows up: [redis/redis#7927](https://github.com/redis/redis/issues/7927) and [Debian #972683](https://bugs.debian.org/972683), fixed by switching to libc `free()`.
- Debian's Valkey packaging is **derived** from the Redis packaging, patch included.
- Someone later notices the allocation is leaked and adds a free — writing `zfree(cwdp)` again. **The same mistake, in the same patch lineage, five years apart.**
- **March 2025** — Valkey maintainer zuiderkwast, reviewing these Debian patches, [spots the mismatch immediately](https://github.com/valkey-io/valkey/issues/1882):

  > ...the latter uses `malloc()` (rather than `zmalloc()`) and we later free it using `zfree()`. This means it will mess up the memory usage tracking done in zmalloc and zfree. Therefore, we may not want to take this patch, at least not unmodified.

  Correct diagnosis. He assumed the damage stopped at broken accounting, and the issue lost priority when jemalloc upstream was archived.
- **April 2026** — Valkey builds an automated pipeline covering 40 platform combinations, and **copies Debian's patch set wholesale**. The official `.deb`s inherit the bug.

Worth noting: that repository's test target is an **empty shell with the body commented out**. The upstream tests that catch this have never run in the official DEB build.

## Reporting it

Two channels, handled separately.

**Debian takes email.** No account needed — send a **plain text** message to `submit@bugs.debian.org` with pseudo-headers as the first lines of the body:

```
Package: src:valkey
Version: 8.1.4+dfsg1-2
Severity: normal
Tags: patch
```

My first attempt bounced, saying the body didn't start with `Package:`, so "**your message has been ignored completely**". Which was baffling, because it did:

```
00000000: 5061 636b 6167 653a      Package:
```

The answer was in the message-id: it was **Apple Mail**, which sends rich text by default. BTS only parses plain text, so it never saw the line.

So if you're filing a Debian bug from a Mac: switch to plain text first (`Format` → `Make Plain Text`), and turn off smart quotes, or the quote characters in your patch get mangled and the patch is worthless. Resent, it went through as [#1143239](https://bugs.debian.org/1143239).

**Upstream took a comment, then a PR.** zuiderkwast's year-old comment was the natural hook, so I picked up from there with what he didn't have: under the bundled allocator this is a segfault, not drift; the upstream test suite already catches it; and the official `.deb`s have it today.

He replied within the day asking for a PR. The change is one line:

```diff
-        zfree(cwdp);
+        zlibc_free(cwdp);
```

`zlibc_free()` exists in Valkey **for exactly this case** — it's defined specifically so callers can reach the real libc `free()`.

Which also explains how `zfree` got picked in the first place. A plain `free(cwdp)` **does not compile**: Valkey deliberately marks `free()` deprecated and builds with `-Werror`. The author was almost certainly blocked by the compiler and reached for the name that looked closest.

A defensive measure that pushed someone into the hole it was guarding.

## Outcome

zuiderkwast approved the same day, with a question: **why keep this patch at all?** The path is only used in one error message; just go back to the stack buffer.

Fair, and I'd listed dropping it as the alternative in the PR description. Since he was leaning that way, I did it downstream first — removed the patch entirely from Pigsty's Valkey and Redis packaging, rebuilt, and reported back: nothing changes for users, the error message still prints the full path, tests pass. **The problem goes away along with the patch.**

Then it went somewhere I didn't expect. zuiderkwast turned to the maintainers who built the pipeline:

> Why did we copy Debian's patches?
>
> If some things need to be patched, that's better fixed upstream in Valkey itself. **Bugs in this repo's patches are harder to spot than bugs in Valkey main repo IMHO.**

That last sentence is the best summary of the whole episode.

**The PR merged on 2026-08-07.** All five packaging lines are fixed. The maintainer who built the pipeline replied "Thanks for the notification. Will investigate this!" — a review of the whole patch stack is underway.

The Debian report has had no reply since August 1st, which is normal; response times there run in weeks. Still outstanding: **bookworm's Redis package has the identical defect**, which I mentioned inside the Valkey report but haven't filed separately.

## Takeaway

Nobody involved did anything stupid.

Lamb's 2017 patch was legitimate packaging hygiene. Whoever added `zfree(cwdp)` was fixing a real leak and picked the wrong deallocator — pushed there by `free()` being deliberately deprecated. zuiderkwast spotted the mismatch a year ago and diagnosed it correctly; he just underestimated the consequence. Copying Debian's patches into the release pipeline was the pragmatic move, and Debian's packaging quality is famously good.

Every step was reasonable. The result sat quietly across five product lines and four distributions.

**Packaging patches are where bugs hide.** They're not in upstream's CI, not in upstream's code review, not in anyone's `git log`. They get copy-pasted across projects (Redis → Valkey) and across organizations (Debian → Valkey's own pipeline), losing a little context each time.

And the reason this surfaced at all: that test case was sitting there the whole time, creating a directory named `dump.rdb` to force exactly this failure. The official pipeline had its test target commented out, so it never ran once.

Packaging is dull work. Run the tests anyway.

## Postscript: a question at PGConf

At PGConf this year I gave a talk called *Extension for Everyone*. Afterwards Christoph Berg, who maintains the PGDG APT repository, asked me a good question:

**How do you actually test all these packages?**

Pigsty maintains packaging for a few hundred extensions and components. The packaging repos alone carry over a hundred patches, a good share of them fixing small, fiddly details. One person cannot hand-verify every path in every package. There isn't enough time.

My answer: beyond whatever tests the package ships with, I have Codex run a smoke pass — model how the software actually gets used in production and try to hit the things that break.

It turns up a lot. This bug is the biggest thing it has found so far.

Which is worth sitting with for a moment: **why did this survive so long?**

Valkey is not an obscure project anymore; it's the default Redis replacement in several distributions. Debian is about as mainstream as it gets, with famously good packaging. Valkey's maintainers are excellent engineers — zuiderkwast diagnosed the mechanism correctly a year ago just by *reading* the patch. And Redis's own packaging copies Debian's patch the same way.

So the missing ingredient was never capability. It was **patience**.

Spending a full day on a footnote-grade bug in a cold error path — building a 3×3×2 build matrix, reproducing the crash thirty times, tracing a patch lineage back a decade, checking five different search endpoints to confirm nobody had reported it — does not pay off on a human time budget. It is too boring.

Which happens to be exactly the kind of work an agent is good at.

End to end on this one: it ran the tests, built the reproduction matrix, wrote the patch, drafted the Debian report, and worded the exchanges with the maintainers on GitHub. My job was assigning the work, pushing back, and making the final calls.

I should be clear that this is not "the AI does everything and I put my feet up". During this investigation I had a second agent do an adversarial review of my draft at maximum effort, and it pulled out four factual errors in one pass: I had misremembered how the old Debian bug was actually fixed, `FLUSHDB` doesn't reach this code path at all, "refuses every write" overstated the impact, and I had missed entirely that bookworm's Redis is still affected today. Sending any of that to maintainers as-is would have been my embarrassment, not the model's.

So the value isn't that the agent gets it right the first time. It's that **the cost of making it disprove itself over and over is low enough to be worth doing** — where a human would decide that six builds to chase a statistics counter isn't worth the afternoon.

The pace of this is genuinely startling. Two years ago every step in that loop was mine to do by hand. Now I sit here handing out tasks, asking follow-up questions, and signing off — and the rest of it just runs.
