---
title: "The PostgreSQL 'Supply Cut' and Trust Issues in Software Supply Chain"
date: 2025-08-15
author: vonng
summary: >
  PostgreSQL official repos cut off global mirror sync channels, open-source binaries supply disrupted, revealing the true colors of various database and cloud vendors.
tags: [PostgreSQL,PG Administration]
---

This month saw a high-profile "open source supply cut" incident — [KubeSphere deleting images and running away](/en/cloud/kubesphere-rugpull),
but there's another slightly more subtle "chokepoint case" I mentioned last month — ["Chokepoint: PGDG Cuts Mirror Sync Channels"](/en/pg/pg-mirror-break).
This "PostgreSQL supply cut" played the role of litmus test, nicely revealing the true colors of various database and cloud vendors.

I'm deeply disappointed and have stopped treating domestic cloud vendors and university mirrors as upstream software supply chain sources, directly building my own up-to-date domestic mirror of PGDG YUM/APT repositories.



## PGDG's "Supply Cut"

PostgreSQL is the grandmaster-level open source project in the database field, also the world's most popular, beloved, and in-demand database.
The vast majority of users install PostgreSQL on Linux through PGDG APT/YUM repositories.
Unfortunately, PGDG (PostgreSQL Global Development Group) closed their APT/YUM software artifact repository's FTP and rsync sync channels to the outside world in mid-May this year,
causing almost all global mirror sites to lose sync with upstream repositories, storing months-old software packages.

I covered this in detail in ["Chokepoint: PGDG Cuts Mirror Sync Channels"](/en/pg/pg-mirror-break) on July 7th.
At that time, I observed Germany's XTOM actually attempting a manual monthly update strategy, while basically all other mirrors were completely down, stuck at March/April/May status. Yesterday I rechecked and found Russia's YANDEX also manually followed the APT repository, but other mirrors remain the same.


| Provider        | Region  | Sync Timestamp     | URL                                                                   |
|-----------------|---------|-------------------|-----------------------------------------------------------------------|
| Alibaba Cloud   | China   | 2025-03-31        | https://mirrors.aliyun.com/postgresql/sync_timestamp                  |
| Tencent Cloud   | China   | 2025-03-31        | https://mirrors.cloud.tencent.com/postgresql/sync_timestamp           |
| Volcano Cloud   | China   | 2025-03-10        | https://mirrors.volces.com/postgresql/sync_timestamp                  |
| Huawei Cloud    | China   | 2024-01-02        | https://repo.huaweicloud.com/postgresql/sync_timestamp                |
| Tsinghua TUNA   | China   | 2025-03-31        | https://mirrors.tuna.tsinghua.edu.cn/postgresql/sync_timestamp        |
| Zhejiang Univ   | China   | 2025-03-31        | http://mirrors.zju.edu.cn/postgresql/sync_timestamp                   |
| USTC            | China   | Removed           | https://servers.ustclug.org/2025/05/wine-postgresql-removal/          |
| TrueNetwork     | Russia  | 2025-01-31        | http://mirror.truenetwork.ru/postgresql/sync_timestamp                |
| JAIST           | Japan   | 2025-03-31        | https://ftp.jaist.ac.jp/pub/postgresql/sync_timestamp                 |
| DOTSRC          | Denmark | 2025-03-31        | https://mirrors.dotsrc.org/postgresql/sync_timestamp                  |
| MirrorService   | UK      | 2025-03-31        | https://www.mirrorservice.org/sites/ftp.postgresql.org/sync_timestamp |
| Princeton Univ  | USA     | 2025-03-31        | https://mirror.math.princeton.edu/pub/postgresql/sync_timestamp       |
| YANDEX          | Russia  | **2025-08-13**    | https://mirror.yandex.ru/mirrors/postgresql/                          |
| XTOM            | Germany | **2025-07-24**    | https://mirrors.xtom.de/postgresql/                                   |
| PIGSTY          | China   | **2025-08-14**    | https://repo.pigsty.cc/                                               |



## Mirrors "Stop Updating"

For instance, the 17.5 May update fixed [CVE-2025-4207](https://www.postgresql.org/support/security/CVE-2025-4207/) GB18030-related vulnerability,
and the just-released [17.6 series](https://www.postgresql.org/about/news/postgresql-176-1610-1514-1419-1322-and-18-beta-3-released-3118/) fixed 3 CVEs and 55 bugs. If you're a mirror user, you can't update and patch in time. Not to mention PostgreSQL 18 releasing next month. We're still in the early stages — just two PG minor versions behind, but soon it'll be a major version behind. All those accumulated vulnerability patches and security fixes become unavailable to domestic users, creating increasingly larger exposure risks.

From this perspective, upstream software supply chain stopping updates to downstream essentially fits the definition of "supply cut." Though PGDG's reason for "cutting supply" is somewhat justified — they moved to CDN.



## Why PGDG "Cut Supply"

In the PostgreSQL mailing list, on May 20th, a Korean mirror maintainer asked why rsync sync with PGDG official repository suddenly broke.

David Page explained that FTP/rsync was never an officially promised service. PGDG YUM/APT repositories only have two physical machines, yet face 10TB daily traffic, much of it "illegal traffic."
Bandwidth couldn't handle it! So they hosted the repository on Fastly CDN.

Their thinking is obvious — with CDN, wouldn't professional CDN nodes and experience be much better than scattered mirrors? Officials can directly serve global users bypassing mirrors,
so why need mirrors? So they shut down FTP rsync, allowing only HTTP access. Seems reasonable — though mirror sync broke, they provided an alternative — just use official CDN, fair enough.

— You can choose not to use any mirrors, directly use PGDG official repository (they just moved to Fastly CDN).



## China Got Choked?

Mirror sync interruption has relatively small impact on most global users, as they can always use PGDG's new CDN. But uniquely for China, this equals artifact supply cut —
for well-known reasons, China can't access these CDN nodes! If these mirrors don't update, Chinese users have nothing!

Sure, you can still use it with VPN or whatever. But you can't expect everyone to know this, and even with VPN it's still slow. So domestic mirrors remain crucial for Chinese users using PostgreSQL.
(Don't mention Docker either, DockerHub is blocked too, and most Docker Postgres images install from APT repositories anyway...)

From this angle, **Chinese users really got choked** — though essentially shooting ourselves in the foot — they just shut down incremental sync, and you can't use their alternative solution.
But this is the situation, what matters is how to solve users' problems in this context. Who will solve this?

Chinese users wanting YUM/APT PostgreSQL installation typically can only use domestic mirrors, most famously Alibaba Cloud and Tsinghua University's TUNA mirror, plus Zhejiang University/USTC sources.
Unfortunately, all these mirrors without exception lay flat, showing no responsibility — but you can't blame them, after all, it's free.



## Supply Chain Risk

Open source expert Tison explained in his articles ["How to Safely Use Open Source Software?"](https://mp.weixin.qq.com/s/-2CeJq1XZdwifZkJY2oXNA) and
["Does Open Source Software Have Supply Cut Risk?"](https://mp.weixin.qq.com/s/vSxWUcFgbS3D_0tZnBIfdg) that open source software (source code) itself has no "supply cut" risk —
the basic rights granted by open source licenses are irrevocable, in this dimension **"open source supply cut has never happened"**. Supply cut concerns often stem from misunderstanding due to excessive expectations of open source.

But user dependency on open source always happens in specific software supply chains, ensuring open source dependency supply chain security has costs —
open source artifacts, i.e., binary packages (RPM/DEB/images), and their delivery channels — software repositories (APT/YUM/Registry) do have supply cut risks.

The reason is simple, these have costs, who pays is a big issue. Open source developers willing to pay the bulk of R&D costs often see it as interesting entertainment.
However, distribution, packaging, building repositories, providing continuous stable enterprise services is largely pure burden. For example, if domestic GB traffic costs 80 cents, PGDG's 10TB daily traffic costs thousands daily, right? So you see those running open source mirrors are basically either universities or large internet companies — first they use it themselves, second adding extra chopsticks costs little traffic.

Conversely, did users of open source software pay PGDG and open source mirror sites? Nope, so honestly, legally or morally, you can't really criticize, because this is open source STYLE — no warranty —
after all they didn't charge, providing source code is duty, but open source licenses don't mandate providing binary artifacts, developers and mirror sites have no obligation for such charity.





## How to Solve Supply Chain Risk?

Can commercial services solve this? After all, so many domestic databases are PostgreSQL reskins, shells, or forks, yet the upstream ancestor gets banned — quite comical. Nobody sets up a Chinese mirror?
Well, maybe not — most database vendors just freeload off mirrors (Alibaba Cloud, Tsinghua) repositories, or rather, their delivery method isn't even software repositories but throwing you an EL7 RPM package, completely unable to maintain repositories.

I independently maintain a PostgreSQL extension repository containing 9 PG kernel flavors and 200+ PG extensions (423 available extensions total with PGDG). Currently the world's largest PG ecosystem repository with most available extension artifacts.
Not modestly, speaking of PostgreSQL packaging and building, me and Devrim (YUM repo), Christoph (APT repo), Álvaro (OCI repo), David Wheeler (PGXN) are top players and original suppliers in this track.

But though I can package, build, and maintain repositories, when installing and delivering native PG kernels, I still choose "official PG" PGDG APT/YUM repositories, with PIGSTY's own repository as extension supplement,
because Devrim and Christoph already do great work! I do complementary differentiated work. So for my PostgreSQL distribution Pigsty, PGDG repository is PIGSTY's upstream supply chain,
domestically due to the firewall, Alibaba Cloud mirror is my indirect upstream. Now the problem is this indirect upstream, including all mirrors like Alibaba Cloud, Tsinghua, Zhejiang University, various clouds, all broke and stopped updating. What to do?

When I discovered this issue, I immediately reported to Alibaba Cloud and Tsinghua TUNA mailing lists, also chatted with Dege. Unfortunately, dozens of days passed, still no ripples, no movement.
Nobody has the responsibility to step up and solve this. I'm really disappointed in these domestic cloud vendors, database vendors, and university mirror maintenance teams. But you can't blame them — right, they're letting you use it free, what can you say?



## I'll Do It Myself

So I stopped wasting time and just did it myself. Only after doing it did I realize how trivial this was — they don't give you FTP rsync access, so use apt-mirror and reposync
to sync directly from HTTP channel, right? Yesterday I spent two hours with Claude Code, wrote a sync process, pulled PGDG's YUM/APT repositories,
threw them into Pigsty's repository, tested once, super smooth. My feeling after finishing — that's it? Such trivial work got China stuck like this? The "everything is held together with duct tape" theory proves true.

Of course, total PG repository is hundreds of GB, downloading everything would be too large, so I only took Linux x86/aarch64 architecture packages, synced Debian 11/12/13, Ubuntu 22/24,
EL 7/8/9/10 these major Linux OS distribution versions' PG 13-17 packages, keeping only latest versions, total size just dozens of GB.
Pulled for two hours, synced back, threw on domestic CDN, now in pig 0.6.1 and pigsty 3.6.1, I've replaced Alibaba Cloud and Tsinghua sources, will release in coming days, completely getting rid of lying-flat middleman dependency, achieving true self-reliance.



Currently this repository, like Pigsty itself, is open source and free. Using Pigsty directly is definitely the better choice for self-hosting PostgreSQL services, but you absolutely can directly use the APT/YUM mirror repositories here.
Direct public user access will have considerable traffic costs, but I should be able to handle it — though open source essence is no warranty, fortunately I promise customers long-term continuous maintenance of this mirror repository, so free users can hitchhike. If anyone wants to sponsor (servers, CDN, money), I very much welcome it.

```bash
curl https://repo.pigsty.io/pig | bash
pig repo add pgdg  # Add PGDG repository
```


This reminds me of past events. Two years ago I wanted to get PG extensions in, but wanted to lazily leverage others. I saw companies like Tembo and pgxman trying to make PG extension package managers,
I waited and waited for months, finally finding they purely talked without working, so I stopped waiting and did it myself, made pig package manager, pg extension directory and extension repository, now becoming PG ecosystem's largest extension repository.
Like open source PG distributions/projects like Omnigres and Autobase also use the Pigsty extension repository I maintain to deliver to their customers. My software repository is becoming upstream in others' supply chains.

"Open source" indeed doesn't require providing reliable stable binary artifacts to users, **but what really matters isn't open source, it's trust**. Open source is just one form of building trust — continuous investment, delivery commitments, focused passion, responsibility facing problems.
To become trustworthy, respected community participants, many things matter more than throwing source code into a repository.