---
title: "Git for Data: 瞬间克隆PG数据库"
linkTitle: "Git for Data: 瞬间克隆PG数据库"
date: 2025-12-27
author: 冯若航
summary: >
  如何在瞬间克隆一个巨大的 PostgreSQL 数据库，还不占用额外的存储？PG 18 与 XFS 可以擦出很多火花。
tags: [PostgreSQL, PG开发, GIS]
---

每个程序员都用过 `git clone`。敲下回车，几秒钟后，一个完整的代码仓库就躺在硬盘上了。

但数据库呢？

想给测试环境搞一份生产数据的副本？传统方案是 `pg_dump` + `pg_restore`。一个 100GB 的库，喝杯咖啡回来可能还没完。想做并行测试？再等一轮。想给 AI Agent 一个可以随便折腾的沙盒？那得准备好足够的磁盘和耐心。

最近一堆数据库公司都在卷 "Git for Data"，理由是：有了数据版本控制，Agent 就可以放心在数据库里乱搞，坏了随时回滚。

但这玩意，PostgreSQL 其实早就有了。

只不过 **PostgreSQL 18 把它提升到了一个新阶段**：一个 100GB 的数据库，克隆时间从"分钟级"变成了 **200 毫秒**。不是快了一点，是快了几百倍。更神奇的是，克隆完的数据库**不占用额外存储空间**。1TB、10TB 的库？一样是 200 毫秒，一样零额外开销。

这不是魔法，是**写时复制（Copy-on-Write）** 技术终于被 PostgreSQL 原生支持了。
今天我们就来聊聊这个特性，以及它对整个"数据版本控制"生态意味着什么。

---

## 写时复制：为什么能这么快？

PostgreSQL 18 新增了一个参数 `file_copy_method`，可选值为 `copy`（传统字节拷贝）和 `clone`（基于 reflink 的瞬间克隆）。设置 `file_copy_method = clone` 后执行：

```sql
CREATE DATABASE db_clone TEMPLATE db STRATEGY FILE_COPY;
```

PostgreSQL 会调用操作系统的 **reflink** 接口。Linux 上是 `FICLONE` ioctl，macOS 上是 `copyfile()`。

关键来了：**操作系统不会真的复制数据**。

它只是创建一组新的元数据指针，指向相同的物理磁盘块。就像你在文件管理器里创建了一个"快捷方式"，但这个快捷方式可以独立修改。

**没有数据移动，只有元数据操作。** 所以无论数据库是 1GB 还是 1TB，克隆时间都是常数级的 —— 在现代 NVMe SSD 上，老冯测试 120GB 的库复制大约 200 毫秒。797G 的数据复制大概 569 毫秒左右。


------

## 写时复制：为什么不占空间？

克隆后，源库和新库共享所有物理存储。当任意一方修改某个数据页时，文件系统才会把这个页复制出来单独存储：

这意味着：**存储开销 = 实际变更量**，而不是完整副本。

你可以同时跑 10 个克隆库做并行测试，只要它们不大量写入，存储几乎不增长。对测试环境来说，这是巨大的福音。

不过，不是所有文件系统都支持 reflink。好消息是，大多数现代 Linux 发行版已经默认启用：

| 文件系统      | 支持情况   | 备注                             |
|-----------|--------|--------------------------------|
| **XFS**   | ✅ 完整支持 | 现代 mkfs.xfs 默认启用 `reflink=1`   |
| **Btrfs** | ✅ 完整支持 | 原生 CoW 文件系统                    |
| **ZFS**   | ✅ 支持   | OpenZFS 2.2+ 需启用 block_cloning |
| **APFS**  | ✅ 完整支持 | macOS 原生                       |
| **ext4**  | ❌ 不支持  | 回退到传统复制                        |

如果你用的是 EL 8/9/10、Debian 11/12/13、Ubuntu 20.04/22.04/24.04 等主流发行版，默认的 XFS 都已经支持并启用 reflink。

还在用 CentOS 7.9 和 ext4？那确实就没办法了，早点升级吧。



### 关键限制：模板库不能有连接

这个功能虽然好，有一个绕不开的限制：克隆时，模板数据库**不能有任何活动连接**。
原因很直接：PostgreSQL 需要确保克隆时数据处于一致状态。如果有连接在跑，可能产生写入，数据就不一致了。

这个限制其实一直都有。以前它很致命 —— 你不可能让生产库停机几分钟等复制完成。但现在克隆只要亚秒级常数时间，**这个限制的杀伤力大大降低了**。
百毫秒级别的闪断，对于很多场景是可以接受的，特别是那些 AI Agent 使用的库——它们没那么娇气。这就带来了许多新鲜的可能性。

实操的话，要想实际把这个数据库克隆出来，你需要先终止所有连接，在两条紧挨着 SQL 语句里执行：

```bash
psql <-EOF
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'prod';
CREATE DATABASE dev TEMPLATE prod STRATEGY FILE_COPY;
EOF
```

请注意，这俩语句不能分开执行，但不能放在同一个事务里执行（`CREATE DATABASE` 不能在事务块内运行）。
所以你需要用 psql stdin 的方式来执行，用 `psql -c` 会自动包事务，反而会失败。


### Pigsty 中的优化

在 Pigsty 4.0 中，添加了对 PG18 这种克隆机制的支持：

```yaml
    pg-meta:
      hosts:
        10.10.10.10: { pg_seq: 1, pg_role: primary }
      vars:
        pg_cluster: pg-meta
        pg_version: 18
        pg_databases:
          - { name: meta }  # <----- 待克隆的数据库
          - { name: meta_dev ,template: meta , strategy: FILE_COPY}
```

比如，你已经有了一个 `meta` 数据库，现在想创建一个 `meta_dev` 的克隆库用于测试，
只需要在 `pg_databases` 里添加一条记录，指定 `template` 和 `strategy: FILE_COPY` 即可。
然后执行： `bin/pgsql-db pg-meta meta_dev`，Pigsty 会帮你自动处理好所有细节。

当然其实这里的细节还是不少的，比如，你要确保 `file_copy_method` 被正确设置为 `clone` 才有这个特性，这个 Pigsty 创建的集群全都已经针对 PG18+ 都配置好了。
如果你要克隆的数据库就是管理数据库 `postgres` 本身怎么办 (克隆的时候不允许连接)。再比如，克隆数据库之前要先终止所有连接，这些都帮你自动搞定了。




### 还有没有其他手段？

当然，即使是 200ms 的不可用时间，有时候对于比较严格的生产环境依然是不可接受的。
而且如果你的 PG 版本不是最新的 18，也没法用这个特性。

Pigsty 提供了两种更强大的克隆方式，场景稍微不太一样：

### 实例级克隆：pg-fork

实例级别的克隆思路和 PG18 的 CoW 类似，都需要你的文件系统支持 reflink（XFS/Btrfs/ZFS）。
之前生产环境的文件系统老冯一直都强烈推荐用 xfs，现在也是很多地方都默认，这个要求并不难满足。

用了 xfs 之后，你可以使用 `cp --reflink=auto` 来克隆整个 PGDATA 目录，从而克隆一个完全独立的 PostgreSQL 实例。
这个过程也是瞬间完成的，和数据库大小无关，而且克隆出来的不占用实际存储，除非你开始往里面写数据，才会触发 CoW。

```bash
postgres@vonng-aimax:/pg$ du -sh data
797G	data
postgres@vonng-aimax:/pg$ time cp -r data data2

real	0m0.586s
user	0m0.014s
sys	0m0.569s
```

当然，实际上细节要比这个复杂，你如果直接这么复制，大概率得到的是一个数据状态不一致的脏实例，启动不了。
所以还要配合 PostgreSQL 的原子备份 API 来确保数据一致性 —— 核心就是这一行：

```bash
psql <<EOF
CHECKPOINT;
SELECT pg_backup_start('pgfork', true);
\! rm -rf /pg/data2 && cp -r --reflink=auto /pg/data /pg/data2
SELECT * FROM pg_backup_stop(false);
EOF
```

当然实际上各种边界情况要复杂一些，比如克隆出来的实例如果你要拉起来，不能挤占原来实例的端口，
不能写脏原来生产实例的日志/WAL归档，诸如此类细节。所以 Pigsty 就提供了一个傻瓜式的克隆脚本 `pg-fork` 来解决这个问题。

```bash
pg-fork 1   # 克隆一个 1 号实例，/pg/data1 ，监听 15432 端口
```

实例级别克隆的好处是，克隆出来的是一个完全独立的 PostgreSQL 实例，同样不占用额外存储空间，同样是瞬间完成的。
但是它不需要你关闭原始模板数据库的连接，所以不会影响生产环境的可用性。
最多就是拉起来的时候吃掉点内存，但这种时候你就发现 PG 的双缓冲其实也有好处了。
默认配置 25% 的 Sharedbuffer，你可以很轻松的再拉起一两个实例。

更妙的是，这种克隆出来的实例，还可以通过 `pg-pitr` 脚本，利用基于 pgBackRest 的备份，做时间点恢复（PITR）。
而且这个时间点恢复也是增量进行的，所以速度也很快。

这种机制最直接的应用场景就是，误删数据了，但是删的又不多，不至于全库回档。
那么这种情况下，就可以使用 `pg-fork` 脚本，瞬间克隆出一个和生产库一模一样的副本，
然后原地 pg-pitr 增量回滚到几分钟前，拉起来，把误删的数据查出来再写回去。


### 集群级别的克隆

当然，还有一种集群层面的克隆，利用的技术也是类似的，通过使用一个集中式的备份仓库，你可以从任意一个集群的备份中恢复到备份保留期限内的任意时间点。

```bash
./pgsql-pitr.yml -l pg-test -e '{"pg_pitr": { "cluster": "pg-meta" }}'
```

这种方式的集群克隆不用消耗原本生产集群的任何资源，云上的各种 “PITR” 其实就是这种，给你拉起一套新的集群，恢复到指定时间点。
但是这种方式的速度就慢多了，毕竟要把数据从备份仓库里拉出来，恢复到新的集群上，时间和数据量成正比。

### 应用场景

三种克隆方式，各有适用场景：

| 方式    | 速度        | 停机要求    | 权限要求     | 适用场景                |
|-------|-----------|---------|----------|---------------------|
| 数据库克隆 | ~200ms，常数 | 需要断连模板库 | 仅需数据库连接  | AI Agent、CI/CD、快速测试 |
| 实例克隆  | ~200ms，常数 | 无       | 需要文件系统访问 | 误删恢复、分支测试，CI/CD     |
| 集群克隆  | 分钟~小时级    | 无       | 需要备份仓库访问 | 跨机房恢复、灾备演练          |

虽然之前已经有了 `pg-fork` 这种实例级的 “瞬间克隆” 技术，而且没有数据库模版克隆要求几百毫秒停机时间的限制。
但这种操作要求你必须拥有数据库服务器的文件系统访问权限。而且你克隆出来的实例也仅限于在同一台机器上运行 —— 从库上是没有的。

而数据库克隆有一个独特的优点，就是这个操作是 “完全在数据库客户端连接” 内完成的，也就是可以通过纯 SQL 来完成，不需要服务器访问权限。
这就意味着，你可以在任何能连接到数据库的地方，执行这个克隆操作，唯一的代价就是 200ms 左右的断连时间。

这就打开了一扇新的大门：

**AI Agent 场景**：给 Agent 只开一个数据库连接的权限，每次需要"乱搞"的时候，让它自己克隆一个沙盒出来。搞烂了就 DROP，没有任何代价。10 个 Agent 并行跑，存储开销几乎为零。

**CI/CD 场景**：以前数据库发布胆战心惊。现在用极低成本克隆出一堆测试库跑集成测试，DDL 迁移在真实数据上验证完再上生产，心里有底多了。

**开发环境**：每个开发者一个完整的数据库副本，数据和生产一模一样，存储成本趋近于零。改坏了？重新克隆一个，200 毫秒的事。

---

## 写在最后

"Git for Data" 这个概念被吹了好几年，各种创业公司融了不少钱。但 PostgreSQL 用一个简单直接的方式给出了自己的答案：
**不需要额外的中间层，不需要复杂的架构，利用现代文件系统已有的能力，在数据库内核层面原生支持**。

几百毫秒，没有额外存储，一条 SQL 搞定。

有时候，最好的方案就是最简单的方案。


















------

### 文件系统的写时拷贝机制 

PostgreSQL 18 新增了一个参数 `file_copy_method`，可选值为 `copy`（默认，传统字节拷贝）和 `clone`（基于 reflink 的瞬间克隆）。

当你设置 `file_copy_method = clone` 并执行：

```sql
CREATE DATABASE db_clone TEMPLATE db STRATEGY FILE_COPY;
```

PostgreSQL 会调用操作系统的 **reflink** 接口（Linux 上是 `FICLONE` ioctl，macOS 上是 `copyfile()`）。
操作系统不会真的复制数据，而是创建一组新的元数据指针，指向相同的物理磁盘块。

**没有数据移动，只有元数据操作。** 所以无论数据库是 1GB 还是 1TB，克隆时间都是常数级的 —— 
在现代 NVMe SSD 上大约 200 毫秒。



### 写时复制的精妙之处

克隆后，源库和新库共享所有物理存储。当任意一方修改某个 8KB 的数据页时，文件系统才会把这个页复制出来单独存储。这就是 Copy-on-Write。

CoW 的好处是，克隆的 **存储开销 = 实际变更量**，而不是完整副本。
这对测试环境是巨大的福音 —— 你可以同时跑 10 个克隆库做并行测试，只要它们不大量写入，存储几乎不增长。

不是所有文件系统都支持 reflink：

| 文件系统      | 支持情况   | 备注                                   |
|-----------|--------|--------------------------------------|
| **XFS**   | ✅ 完整支持 | 现代 mkfs.xfs 默认启用 `reflink=1`         |
| **Btrfs** | ✅ 完整支持 | 原生 COW 文件系统                          |
| **ZFS**   | ✅ 支持   | OpenZFS 2.2+ 需启用 block_cloning，但有点风险 |
| **APFS**  | ✅ 完整支持 | macOS 原生                             |
| **ext4**  | ❌ 不支持  | 会回退到传统复制                             |

大多数现代 Linux 发行版的 XFS 已经默认启用 reflink，所以你大概率不需要额外配置。
如果你用的是 EL 8/9/10，Debian 11/12/13，Ubuntu 20.04/22.04/24.04，等主流发行版，默认的 XFS 都已经支持并默认开启 reflink。

当然，如果你还用着 CentOS 7.9 和 ext4 文件系统，那就算了。







你可以使用完全不一样的配置来运行它。








### 这项功能的变迁与对比


在 PG 15 之后，`CREATE DATABASE ... TEMPLATE` 引入了 `STRATEGY` 参数，允许你选择 `WAL_LOG`（15后默认，传统方式）和 `FILE_COPY`（基于文件系统拷贝，15前的唯一策略）。
新的默认策略会把整个数据库的所有页面扫一遍给写入到 WAL 日志里面，这样所有从库都确保有一份一模一样的副本。
但这个过程比较慢，而且会往 WAL 里面写入大量数据。





在 PG 15 之前，`CREATE DATABASE ... TEMPLATE` 本来就要求模板库没有活动连接，所以这个限制并不新鲜。






------

## 二、三种克隆层次：选对工具做对事

PostgreSQL 世界里，"克隆"这个词在不同语境下指代完全不同的操作。搞清楚它们的边界，才能选对方案。

### 第一层：数据库级克隆（Database-Level）

就是上面说的 `CREATE DATABASE TEMPLATE`。

**适用场景**：

- 同一个 PostgreSQL 实例内，快速创建测试库
- CI/CD 流水线中为每个测试任务创建隔离环境
- 开发人员本地快速复制一份数据

**优势**：

- PG18 + reflink 下是 O(1) 时间复杂度
- 共享实例配置、扩展、连接池
- 存储效率极高（COW）

**局限**：

- 只能在同一实例内
- 模板库不能有活动连接
- 无法做时间点恢复（PITR）

### 第二层：实例级克隆（Instance-Level）

用文件系统快照（ZFS/Btrfs）或 XFS reflink 复制整个 `PGDATA` 目录。

bash

```bash
# ZFS 方案
zfs snapshot pgdata@baseline
zfs clone pgdata@baseline pgdata_clone

# 或者 XFS reflink 方案
pg_ctl stop -D /pg/data
cp -r --reflink=auto /pg/data /pg/data_clone
# 修改端口、关闭归档，然后启动
pg_ctl start -D /pg/data_clone -o "-p 5433"
```

**适用场景**：

- 每个开发者需要完全独立的 PostgreSQL 实例
- 测试需要修改 `postgresql.conf` 参数
- 模拟主从切换、故障恢复场景

**优势**：

- 完全隔离，互不干扰
- 可以测试不同配置
- ZFS 快照还支持回滚

**局限**：

- 只能在同一台机器上
- 需要手动处理端口冲突、pid 文件
- 占用更多系统资源（每个实例独立的 shared_buffers）

### 第三层：集群级克隆（Cluster-Level）

通过 pgBackRest 或 Barman 从中央备份仓库恢复，可选 PITR。

bash

```bash
# 从 pg-meta 集群恢复到 pg-test 集群
pgbackrest --stanza=pg-meta --delta restore --target-time="2025-01-15 14:30:00"
```

**适用场景**：

- 跨机器、跨机房创建副本
- 灾难恢复演练
- 将生产数据恢复到任意历史时间点
- 数据迁移

**优势**：

- 支持跨主机
- 支持任意时间点恢复
- 增量恢复（`--delta`）减少传输量

**局限**：

- 速度最慢（分钟到小时级）
- 需要预先配置备份基础设施
- 恢复后需要善后（stanza-upgrade、重建备份链）

### 对比总结

| 维度           | 数据库级     | 实例级          | 集群级      |
|--------------|----------|--------------|----------|
| **速度 (1TB)** | ~200ms   | 秒级           | 30分钟~数小时 |
| **跨主机**      | ❌        | 受限（ZFS send） | ✅        |
| **PITR**     | ❌        | 受限           | ✅        |
| **隔离程度**     | 共享实例     | 完全独立         | 完全独立     |
| **存储开销**     | 极低 (COW) | 低 (COW)      | 完整副本     |
| **典型用途**     | 测试库      | 开发环境         | DR/迁移    |

**经验法则**：能用数据库级就别用实例级，能用实例级就别用集群级。选最轻量的方案。

------

## 三、其他数据库怎么做的？

PostgreSQL 18 的原生 reflink 支持，让它在克隆能力上追平了商业数据库的最高水准。但各家的实现思路很不一样。

### Oracle：两套方案，各有侧重

**CloneDB** 基于 Direct NFS，用 RMAN 镜像备份作为只读数据源，写入走稀疏文件。适合需要与生产数据隔离的测试场景。

**PDB Snapshot Copy** 则是 Oracle 多租户架构的专属能力，在 Exascale 存储上实现原生 redirect-on-write。多 TB 的 PDB 克隆初始开销约 2GB，存储效率惊人。而且深度集成 Enterprise Manager，内置数据脱敏工作流——这是 PostgreSQL 生态暂时没有的。

### Neon：架构革新带来的降维打击

Neon 不是在传统 PostgreSQL 上打补丁，而是重构了存储层。计算和存储分离，自研的 Pageserver 消费 WAL 并管理一个不覆写的页面存储。

**1TB+ 的数据库分支，1 秒内完成**——不依赖文件系统，不受磁盘 IO 限制。

更厉害的是工作流集成：保护分支、自动 TTL 过期、GitHub/Vercel 预览环境联动、Scale-to-Zero……这些是 PostgreSQL 18 原生能力无法复刻的。但代价是你必须用 Neon 的托管服务。

### SQL Server：只读快照，定位不同

SQL Server 的 Database Snapshot 用 NTFS 稀疏文件实现 COW，但**快照是只读的**。定位是报表查询和管理员回滚保护，不是可写的开发环境。

SQL Server 2022 的 T-SQL Snapshot Backup 倒是加了存储阵列集成（Pure、NetApp），可以做近乎瞬时的时间点恢复，但这需要企业级存储硬件。

### MySQL：Clone Plugin 走的是另一条路

MySQL 8.0.17 引入的 Clone Plugin 做的是**物理快照的网络传输**——用于 InnoDB Cluster 的节点初始化和从库搭建。

时间与数据量成正比，需要完整存储空间。概念上更接近 `pg_basebackup`，而不是 PostgreSQL 18 的 reflink 瞬间克隆。MySQL 生态要做"thin clone"，得靠 ZFS 或者外部工具。

------

## 四、"Git for Data" 生态：哪些工具还有价值？

PostgreSQL 18 的瞬间克隆很强，但它只解决了一个问题：**快速创建数据库的时间点快照**。

真正的"Git for Data"需要的能力远不止这些：版本历史、差异对比、分支合并、冲突解决、分布式同步……这些 PostgreSQL 原生做不到。

### Dolt：真正的数据库版本控制

Dolt 是 MySQL 兼容的数据库，但底层用 Prolly Tree（概率 B 树 + Merkle DAG）实现，每个数据变更都被追踪。

sql

```sql
-- 时间旅行查询
SELECT * FROM users AS OF 'main~3';

-- 查看差异
SELECT * FROM dolt_diff('main', 'feature-branch', 'users');

-- 三路合并
CALL dolt_merge('feature-branch');
```

这是**单元格级别**的变更追踪，不是文件或页面级别。可以 diff 任意两个 commit，可以三路合并并解决冲突，有 DoltHub 提供类