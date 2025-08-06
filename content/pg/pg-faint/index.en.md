---
title: Don't Upgrade! Released and Immediately Pulled - Even PostgreSQL Isn't Immune to Epic Fails
linkTitle: "Released and Immediately Pulled - Even PostgreSQL Isn't Immune to Epic Fails"
date: 2024-11-16
author: |
  [Vonng](https://vonng.com) ([@Vonng](https://vonng.com/en/)) | [Original WeChat Article](https://mp.weixin.qq.com/s/l1BgfLaRKNNEqHyfx33E6A)
summary: >
  Never deploy on Friday, or you'll be working all weekend! PostgreSQL minor releases were pulled on the day of release, requiring emergency rollback.
tags: [PostgreSQL]
---

The old saying goes: never deploy code on Friday. The PostgreSQL minor releases issued two days ago deliberately avoided Friday deployment, but still gave the community a week's worth of extra work — the PostgreSQL community will release an unusual emergency minor version next Thursday: PostgreSQL 17.2, 16.6, 15.10, 14.15, 13.20, and even the just-EOL'd PG 12 will get 12.22...

This is the first time in the past decade that such a situation has occurred: on the day of PostgreSQL release, the new versions were immediately pulled due to community-discovered issues. There are two reasons for the emergency release: first is fixing the CVE-2024-10978 security vulnerability, which isn't the big problem. The real issue is: PostgreSQL's new minor versions changed the ABI, causing ABI-dependent extensions to crash — such as TimescaleDB.

Regarding PostgreSQL minor version ABI compatibility issues, at this year's June PGConf 2024, Yuri raised this issue during the Extensions Summit and in his talk "[Pushing boundaries with extensions, for extensions](https://www.pgevents.ca/events/pgconfdev2024/sessions/session/14-pushing-boundaries-with-extensions-for-extensions/)", but it didn't receive much attention. Now it has exploded spectacularly, and I bet Yuri is looking at this news thinking: "Told you so."

In any case, the PG community strongly recommends that everyone **NOT** upgrade PostgreSQL in the recent week. Tom Lane's proposed solution is to release an unusual emergency minor version set next Thursday to roll back these changes, then overwrite the old 17.1, 16.5, ... treating these problematic versions as "non-existent." So, the originally scheduled release for these days, Pigsty 3.1 which defaults to using the latest PostgreSQL 17.1, will also be delayed by one week accordingly.

Overall, I think the impact of this incident is positive. First, this isn't a core kernel quality issue, and second, because it was discovered early enough — found and stopped on the release day — it didn't cause substantial impact to users. It won't be like those other database/chip/OS vulnerabilities that explode everywhere once discovered.

Except for a few extremely enthusiastic update lovers or unlucky new installers, there shouldn't be much impact. Just like the last xz backdoor incident, it was also discovered by PG core developer Peter during PG testing, reflecting the vitality and insight of the PG ecosystem from the side.

--------

## What Happened

On the morning of November 14th, an email appeared in the PostgreSQL Hacker mailing list mentioning that the new minor versions actually broke the ABI. This isn't a problem for the PostgreSQL database kernel itself, but the ABI changes broke the contract between the PG kernel and extension plugins, causing extensions like TimescaleDB to fail to run correctly on the new PG minor versions.

PostgreSQL extension plugins are provided for specific major versions on specific OS distributions. For example, PostGIS, TimescaleDB, and Citus are built for PG major version numbers like 12, 13, 14, 15, 16, 17 released annually. Extensions built for PG 16.0 are expected by everyone to continue working on PG 16.1, 16.2, ... 16.x. This means you can rolling upgrade PG kernel minor versions without worrying about extension plugin failures.

However, this isn't an explicit promise, but rather an implicit community understanding — ABI belongs to internal implementation details and shouldn't have such promises and expectations. PG has just performed too well in the past, and everyone has gotten used to this, taking it as a working assumption, reflected in various aspects including PGDG repository package naming and installation scripts.

But this time, PG 17.1 and the minor versions backported to 16-12 modified the size of an internal structure, which could cause — extensions compiled for PG 17.0 when used on 17.1 might have conflicts, leading to illegal writes or program crashes. Note that this issue doesn't affect users using PostgreSQL kernel itself — PostgreSQL has internal assertions to check for this situation.

However, for users using extensions like TimescaleDB, this means if you're not using extension plugins recompiled for the current minor version, there will be such security risks. From the current PGDG repository maintenance logic, extension plugins are only compiled for the current latest PG minor version when new extension versions are released.

Regarding PostgreSQL ABI issues, Marco Slot from CrunchyData wrote a detailed tweet thread to explain. For professional readers' reference.

https://x.com/marcoslot/status/1857403646134153438

--------

## How to Avoid Such Problems

As I mentioned before in "[PG Extensions Complete Repository](https://mp.weixin.qq.com/s/Dv3--O0K70Fevz39r3T4Ag)", I maintain a repository containing many PG extension plugins for EL and Debian/Ubuntu, accounting for nearly half of the entire PG ecosystem's extensions.

The PostgreSQL ABI issue was actually mentioned by Yuri before. As long as your extension plugins are compiled for the PostgreSQL minor version you're currently using, there won't be problems. So whenever new minor versions are released, I recompile and package all these extension plugins.

------------

Last month, I just finished compiling all extension plugins for 17.0, and was starting updates to compile versions for 17.1 these days. It looks like I don't need to do that now — 17.2 will roll back the ABI changes, which means extensions compiled on 17.0 can continue to be used. But I'll still recompile and package for PG 17.2 and other major versions after 17.2 is released.

If you're used to installing PostgreSQL and extension plugins online from the internet and don't have the habit of upgrading minor versions promptly, then there really are such security risks — namely that your newly installed extensions aren't compiled for older kernel versions, encountering ABI conflicts and failing.

-------------

Honestly, I've seen this problem in the real world early on, which is why when developing Pigsty, this out-of-the-box PostgreSQL distribution, I chose from Day 1 to first download all needed software packages and their dependencies locally, build a local software source, then provide Yum/Apt repositories for all nodes in the environment. This approach ensures: all nodes in the entire environment install the same versions, and it's a consistent snapshot — extension versions match kernel versions.

Moreover, this approach can also achieve "autonomous and controllable" requirements, meaning after your deployment goes online, you won't encounter these stupid situations — the original software sources shut down or moved, or just because upstream repositories released incompatible new versions or new dependencies, causing your new machine/instance installations to crash and get stuck. This means you have complete software copies for replication/scaling, with the ability to keep your services running until the end of time without worrying about being "truly choked".

------------

For example, when 17.1 was recently released, RedHat updated the default LLVM version from 17 to 18 two days earlier, and coincidentally only updated EL8 without updating EL9. If users choose to install from upstream internet at this time, it will directly fail. After I reported this issue to Devrim, he spent two hours fixing it, adding LLVM-18 to the EL9-specific patch Fix repository.

PS: If you don't know about this independent repository, you'll probably continue encountering failures after the fix until RedHat fixes this issue themselves, but Pigsty will handle all these dirty details for you.

---------

Some say I can also solve such version problems with Docker, which is indeed correct. However, [running databases with Docker has other problems](https://mp.weixin.qq.com/s/kFftay1IokBDqyMuArqOpg), and these Docker image containers essentially also use the OS package manager in the Dockerfile to download RPM/DEB packages from official software sources for installation. In the end, someone has to do this work...

Of course, adapting different operating systems means a lot of maintenance workload. For example, I maintain 143 EL and 144 Debian PG extension plugins, each extension plugin needs to be compiled for 10 OS major versions (el 8/9, Ubuntu 22/24, Debian 12, five major systems, amd64 and arm64), and 6 database major versions (PG 17-12). The permutations and combinations of these factors mean nearly ten thousand software packages need to be built/tested/distributed, including twenty Rust extensions that take half an hour to compile each... But honestly, it's all semi-automated pipeline work, going from running once a year to once every 3 months isn't unacceptable.

--------

## Appendix: Explanation of ABI Issues

About PostgreSQL extension ABI issues in the latest patch versions (17.1, 16.5, etc.)

PostgreSQL extension C code includes header files from PostgreSQL itself. When extensions are compiled, functions in header files are represented as abstract symbols in binary files. These symbols are linked to actual function implementations based on function names when extensions are loaded. This way, an extension compiled for PostgreSQL 17.0 can usually still load into PostgreSQL 17.1, as long as function names and signatures in header files haven't changed (i.e., the Application Binary Interface or "ABI" is stable).

Header files also declare structs passed to functions (as pointers). Strictly speaking, struct definitions are also part of the ABI, but there are more subtleties. After compilation, structs are mainly defined by their size and field offsets, so for example, name changes don't affect ABI (though they affect API). Size changes slightly affect ABI. In most cases, PostgreSQL uses a macro ("makeNode") to allocate structs on the heap, which looks at the compile-time size of the struct and initializes bytes to 0.

The difference that appeared in 17.1 is that a new boolean was added to the `ResultRelInfo` struct, increasing its size. What happens next depends on who called `makeNode`. If it's PostgreSQL 17.1 code, it uses the new size. If it's an extension compiled for 17.0, it uses the old size. When it calls PostgreSQL functions with pointers allocated using the old size, PostgreSQL functions still assume the new size and might write beyond the allocated block. Generally, this is quite problematic. It could cause bytes to be written to unrelated memory areas, or cause program crashes.

When running tests, PostgreSQL has internal checks (assertions) to detect this situation and throw warnings. However, PostgreSQL uses its own allocator, which always rounds up allocated bytes to powers of 2. The `ResultRelInfo` struct is 376 bytes (on my laptop), so it rounds up to 512 bytes, and the same after changes (384 bytes on my laptop). Therefore, usually this specific struct change doesn't actually affect allocation size. There might be uninitialized bytes, but this is usually resolved by calling `InitResultRelInfo`.

This issue mainly triggers warnings in tests where extensions allocate `ResultRelInfo` or in assertion-enabled builds, especially when running these tests with extension binaries compiled for older PostgreSQL versions. Unfortunately, the story doesn't end there. TimescaleDB is a heavy user of `ResultRelInfo` and indeed encountered problems with size changes. For example, in one of its code paths, it needs to find an index in an array of `ResultRelInfo` pointers, for which it does pointer arithmetic. This array is allocated by PostgreSQL (384 bytes), but the Timescale binary assumes 376 bytes, resulting in a meaningless number, which then triggers assertion failures or segfaults. [https://github.com/timescale/timescaledb/blob/2.17.2/src/nodes/hypertable_modify.c#L1245…](https://t.co/f1vzxwF9l7)

The code here isn't actually wrong, but the contract with PostgreSQL isn't as expected. This is an interesting lesson for all of us. Similar issues might exist in other extensions, though not many extensions are as advanced as Timescale. Another advanced extension is Citus, but I verified and found Citus is safe. It does show assertion warnings. Everyone is advised to be cautious. The safest approach is to ensure extensions are compiled with header files for the PostgreSQL version you're running.