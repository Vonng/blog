---
title: "Oracle 兼容的 PG 真的有用吗？"
date: 2026-02-22
author: 冯若航
summary: >
  从一个“只有 JAR 没有源码”的迁移案例出发，解释为什么 Oracle 语法兼容并非伪需求，以及如何用 IvorySQL + Pigsty 低成本接住历史包袱。
tags: [PostgreSQL, Oracle, IvorySQL]
---

很多国产数据库都以 “兼容 Oracle” 作为卖点，说实话，老冯一直都对这件事不感冒。有时候我也会怀疑，PG 去兼容 Oracle 到底是不是一个伪需求—— 改改业务代码能死吗？但是最近我真的碰到了一个极端情况，让我略微改了看法。


## 一个没有源码的 JAR 包

最近老冯接了个小活儿，挺有意思的。某世界 500 强车企，手里跑着一套 EDB —— 也就是 EnterpriseDB 出品的、带 Oracle 兼容的 PostgreSQL。版本是 **9.1**。

9.1 是什么概念？2011 年 9 月发布的版本，到今天已经整整 **15 年** 了。

这套系统跑在某个云平台上（美国信创云），出过好几次大故障。客户终于忍不了了，找到我说：老冯，帮我们升一下级吧。升级本身不难，但从 9.1 到现在的 PG 18，中间差了十五个大版本，一年一个，年年不落。这个跨度属实有点大。

不过真正要命的不是版本跨度，而是他们的应用 —— **没有源码了**。

对，你没听错。就是一个 JAR 包，代码全写死在里面了，改不了。更麻烦的是，这个 JAR 包里的 SQL 用了 EDB 提供的 Oracle 兼容语法，比如 `SYSDATE`。


## 为什么 SYSDATE 这么棘手？

`SYSDATE` 在 Oracle 里是一个内置的关键字/变量，用来获取当前时间戳，类似于 PostgreSQL 里的 `current_timestamp`。

你可能会想：这有什么难的？建个函数不就完了吗？分分钟给你写一个：

```sql
CREATE FUNCTION sysdate() RETURNS timestamp(0) AS
  $$SELECT clock_timestamp()::timestamp(0) $$ LANGUAGE SQL;
```

没那么简单。问题在于，应用里写的不是 `sysdate()` 这种函数调用语法，而是直接用 `SYSDATE` 这个光秃秃的标识符。在 PostgreSQL 的 Parser（解析器）看来，这个东西既不是函数调用，也不是已知的关键字。Parser 直接就不认识它，报语法错误。

```bash
postgres@pg-meta-1:5432/postgres=# SELECT SYSDATE;
ERROR: ivory column "sysdate" does not exist
LINE 1: SELECT SYSDATE;
               ^
Time: 0.249 ms
```

而且，你无法通过写扩展来解决这个问题。PostgreSQL 的可扩展性覆盖了绝大多数场景 —— 你可以自定义类型、操作符、索引方法、存储引擎、执行逻辑、甚至外部数据源。**但唯独语法，是不允许通过扩展来定制的。** 这是 PostgreSQL 可定制性上唯一的遗憾。

要让 PostgreSQL 认识 `SYSDATE` 这个 token，你必须去改 Parser 的语法规则文件，也就是要动内核源码。

如果应用有源码，这事儿根本不叫事儿 —— 现在用 AI 做个全局替换，把 `SYSDATE` 改成 `clock_timestamp()::timestamp(0)`，分分钟搞定。但源码没了，JAR 包写死了，这条路堵死了。

你让我怎么办？去反编译 JAR 包然后改 SQL 字符串字面值？这听着就不太靠谱。

所以你看，脏活累活最后全跑到数据库这儿来了。


## IvorySQL：开源的 Oracle 兼容内核

虽然需求很扯淡，但既然是客户的活儿，还是要想办法。

我琢磨了一下，能在 PG 内核层面提供 Oracle 语法兼容的，目前就那么几家。做得最好的是 EDB，但 EDB 是商业产品，价格不菲，而且人家本来就准备换掉。国内号称兼容 Oracle 的数据库倒是一堆，但人家客户不吃信创这一套。所以 PolarDB-O （其实也跟 EDB PG Oracle 兼容有说不清道不明的微妙联系）也不可能。

所以我想了一下，还真就只有 **IvorySQL** 能干这个事。IvorySQL 是瀚高做的一个开源项目，Apache 2.0 许可证，基于 PostgreSQL 内核提供 Oracle 兼容性 —— 包括 PL/SQL、Oracle 语法、内置函数、数据类型、系统视图等等。最新的 IvorySQL 5.1 与 PostgreSQL 18.1 保持同步。

这里要说明一下，IvorySQL 的 Oracle 兼容是 **SQL 语法层面** 的兼容，不是线缆协议兼容。也就是说，客户端还是用 PostgreSQL 的驱动来连接，但连上之后可以跑 Oracle 风格的 SQL。能理解这里的考虑 —— Oracle 的法务在业界可是臭名昭著的，搞客户端协议兼容怕是要被告。

而且关键的是：**IvorySQL 只是一个内核，Pigsty 能把它变成一个完整的 RDS。**

高可用、备份恢复、监控、IaC —— 全都和 Pigsty 原生整合。对我来说，就是改两行配置的事。

```bash
curl -fsSL https://repo.pigsty.cc/get | bash; cd ~/pigsty
./configure -c ivory    # 使用 IvorySQL 配置模板
./deploy.yml
```

![ivory-dashboard.webp](ivory-dashboard.webp)

三条命令，一个 Oracle 兼容的 PG RDS 就拉起来了。让我们来看看，连接 5432 PG 默认端口，使用 Oracle 的 `SYSDATE` 查询就报错了，切换到 1521 Oracle 兼容端口，it works！

```bash
vagrant@meta:~$ psql -p 5432 -c 'select sysdate'
ERROR:  column "sysdate" does not exist
LINE 1: select sysdate
               ^
vagrant@meta:~$ psql -p 1521 -c 'select sysdate'
  sysdate
------------
 2026-02-22
(1 row)

vagrant@meta:~$ psql -p 1521 -c 'select version()'
                                              version
-----------------------------------------------------------------------------
 PostgreSQL 18.1 (IvorySQL 5.1) on aarch64-unknown-linux-gnu, compiled by gcc (GCC) 10.2.0, 64-bit
(1 row)
```

这活儿老冯收了几万块一年。相比 EnterpriseDB 的订阅费，那简直不知道要便宜到哪里去了。当然老冯也不提供 IvorySQL 的质保。如果 IvorySQL 炸了，你找瀚高去。我只管 Pigsty RDS 不出问题，不过老冯自己觉得呢，IvorySQL 没有魔改太多，而是做的增量特性，这个还是相对可控的。我在实际安装使用测试的时候，也还没遇到过 crash 或者 dump 的情况。

总的来说，这套方案相当完美地解决了历史遗留的 Oracle 兼容应用的问题。这也让我发现，虽然是一个很冷门的生态位，但确实有用户有这个需求。反正对老冯来说，这就是很简单的事情，顺手做了也就做了。


## Pigsty：一个"元发行版"

说完 IvorySQL 这个案例，顺便聊聊 Pigsty 最近在内核这块干的几件事。

**Babelfish 内核重建。** 这是 AWS 出品的 SQL Server 兼容内核。之前老粉为了偷懒，用的是 WiltonDB 打包的版本，但那个包比较老，还停留在 PG15，而且只支持 EL8/EL9 和 Ubuntu 22.04/24.04，缺 Debian 和 EL10 的支持，用起来还要用它的专有仓库，总感觉差点意思。

所以这次我一不做二不休，让 Codex 帮我把 Babelfish 的打包流程按 Pigsty 的标准重建了一遍。现在 Babelfish 不再依赖 WiltonDB 的仓库，直接从 Pigsty 自己的仓库安装，全平台通吃了，版本也升级到 PG 17。

![cloudberry.webp](cloudberry.webp)

**Cloudberry 数仓内核。** 既然做了 Babelfish，我也顺手把 Apache Cloudberry（基于 Greenplum 7 的开源数仓）也打包了。之前 1.6 版本的时候起码还提供 EL8/EL9 的 RPM 包，结果 2.0 到现在等了好几个月，都没有二进制产物，问了也是说暂时没这个计划。

所以我也干脆自己上了，Codex 一把梭，把 EL 8-10，Debian 12/13 ，Ubuntu 22/24 x86_64/ARM64 总共 14 个 Linux 平台上的 RPM/DEB 包都打好了。这其实是个挺复杂的大活儿，但 Codex 在那儿"糊"了半天，跑了各种集成测试和单元测试，还弄了几个 Patch 才在 EL10/Debian13 上跑通，最后总算搞定了。

除此之外，OrioleDB 更新到 Beta 14。Percona PGTDE 更新到 18.1。


所以你看，这就是 Pigsty 好玩的地方 —— 它不仅仅是一个 PostgreSQL 发行版，它是一个 **"元发行版"**。

什么意思呢？就是你可以根据需求，爱用什么内核就用什么内核：

- 想要 **Oracle 兼容** → IvorySQL 内核，还有 Polar-O 内核
- 想要 **SQL Server 兼容** → Babelfish 内核
- **想要 MongoDB 兼容** → DocumentDB 扩展 + FerretDB
- 想要 **极致 OLTP 性能** → OrioleDB 内核
- 想要 **透明数据加密** → PGTDE 内核
- 想要 **分布式水平扩展** → Citus 内核
- 想要 **数据仓库** → Cloudberry 内核

而无论你选哪个内核，Pigsty 提供的监控、高可用、备份恢复、IaC 能力都是一样的。**内核可以换，平台的能力不变。** 这才是发行版该干的事。
