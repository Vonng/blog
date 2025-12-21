---
title: "对比Oracle与PostgreSQL事务系统"
summary: "PG社区确实出息了，开始骑在Oracle头上输出了 —— Cybertec专家点评PG与Oracle的事务系统。"
date: 2025-02-27
tags: [数据库,PostgreSQL,Oracle]
---

> 原文：**[Laurenz Albe](https://www.cybertec-postgresql.com/en/comparison-of-the-transaction-systems-of-oracle-and-postgresql/)

事务系统是关系型数据库的核心组成部分，在应用开发中，为确保 **数据完整性** 提供了重要支持。 SQL 标准规范了数据库事务的一些功能，但并未明确规定许多细节。因此，关系型数据库的事务系统可能存在显著差异。

近年来，许多人尝试从 Oracle 数据库迁移到 PostgreSQL。为了顺利将应用从 Oracle 迁移到 PostgreSQL，理解两者事务系统之间的差异至关重要。 否则，您可能会遇到一些令人头痛的意外情况，危及到性能和数据完整性。所以，我认为有必要编写一篇文章，对比 Oracle 和 PostgreSQL 事务系统的特性。

-------

## ACID：数据库事务提供的服务

这里的 ACID 不是什么化学或药品术语，而是以下四个词的首字母缩写：

  * **A** tomicity（原子性）：保证在单个数据库事务中，所有语句作为一个整体执行，要么全部成功，要么全部不生效。这应涵盖所有类型的问题，包括硬件故障。
  * **C** onsistency（一致性）：保证任何数据库事务都不会违反数据库中定义的约束。
  * **I** solation（隔离性）：保证并发运行的事务不会导致某些“异常”（即数据库中一些不可由串行执行的事务产生的可见状态）。
  * **D** urability（持久性）：保证一旦数据库事务提交（完成），即使发生系统崩溃或硬件故障，事务也无法被撤销。



接下来，我们将详细讨论这些类别。

-------

## Oracle 与 PostgreSQL 事务的相似之处

首先，描述一下 Oracle 和 PostgreSQL 在事务管理中相同的部分是有帮助的。幸运的是，许多重要的特性都属于这一类：

  * 两个数据库系统都使用多版本并发控制（MVCC）：读取和写入操作互不阻塞。读取操作会读取旧数据，而在更新或删除事务进行时，不会阻塞读取。
  * 两个数据库系统都在事务结束前保持锁定。
  * 两个数据库系统都将 [行锁](https://www.cybertec-postgresql.com/en/row-locks-in-postgresql/) 保存在行本身，而不是在锁表中。因此，锁定一行可能会导致额外的磁盘写入，但不需要进行 _锁升级_ 。
  * 两个数据库系统都支持 `SELECT ... FOR UPDATE` 进行显式的并发控制。更多关于差异的讨论，后面会说。
  * 两个数据库系统都使用 `READ COMMITTED` 作为默认的事务隔离级别，这在两个系统中的行为非常相似。



-------

## 原子性对比

在这两个数据库中，原子性有一些微妙的差异：

### 自动提交

在 Oracle 中，任何 [DML](https://en.wikipedia.org/wiki/Data_manipulation_language) 语句会隐式启动一个数据库事务，除非已经有一个事务处于开启状态。您必须显式地使用 `COMMIT` 或 `ROLLBACK` 来结束这些事务。没有特定的语句来启动一个事务。

而 PostgreSQL 则处于 _自动提交模式_ ：除非您显式启动一个多语句事务（通过 `START TRANSACTION` 或 `BEGIN`），每个语句都会在自己的事务中运行。在此类单语句事务结束时，PostgreSQL 会自动执行 `COMMIT`。

许多数据库 API 允许您关闭自动提交。由于 PostgreSQL 服务器不支持禁用自动提交，客户端通过适当的时候自动发送 `BEGIN` 来模拟这一点。使用这样的 API，您无需担心这种差异。

### 语句级回滚

在 Oracle 中，导致错误的 SQL 语句不会中止事务。相反，Oracle 会回滚失败语句的效果，事务仍然可以继续。要回滚整个事务，您需要处理错误并主动调用 `ROLLBACK`。

而在 PostgreSQL 中，如果事务中的 SQL 语句发生错误，整个事务会被中止。直到您使用 `ROLLBACK` 或 `COMMIT`（两者都会回滚事务）结束事务时，所有后续的语句都会被忽略。

大多数编写良好的应用程序不会遇到这个差异的问题，因为通常情况下，当发生错误时，您会希望回滚整个事务。 然而，PostgreSQL 的这种行为在某些特定情况下可能会令人烦恼：想象一个长时间运行的批处理任务，其中坏数据可能会导致错误。 您可能希望能够处理错误，而不是回滚已经完成的所有操作。在这种情况下，您应该在 PostgreSQL 中使用（符合 SQL 标准的）保存点。 请注意，您应谨慎使用保存点：它们是通过 [子事务实现的，可能会严重影响性能](https://www.cybertec-postgresql.com/en/subtransactions-and-performance-in-postgresql/)。

### 事务性DDL

在 Oracle 数据库中，任何 [DDL](https://en.wikipedia.org/wiki/Data_definition_language) 语句会自动执行 `COMMIT`，因此 **无法回滚 DDL 语句** 。

在 PostgreSQL 中则没有这种限制。除了少数例外（如 `VACUUM`、`CREATE DATABASE`、`CREATE INDEX CONCURRENTLY`等），您可以 **回滚任何 SQL 语句** 。

-------

## 一致性对比

在这一领域，Oracle 和 PostgreSQL 之间差异不大；两者都会确保事务不违反约束。

或许值得一提的是，Oracle 允许您使用 `ALTER TABLE` 启用或禁用约束。例如，您可以禁用约束，执行违反约束的数据修改操作，然后使用 `ENABLE NOVALIDATE` 启用约束（对于主键和唯一约束，只有在它们是 `DEFERRABLE` 时才有效）。 而在 PostgreSQL 中，只有超级用户才能禁用实现外键约束以及可推迟唯一和主键约束的触发器。设置 `session_replication_role = replica` 也是一个禁用此类触发器的方式，但同样需要超级用户权限。

### 主键和唯一约束在 Oracle 和 PostgreSQL 中的验证时机

以下 SQL 脚本在 Oracle 中不会报错：
    
    ```sql
    CREATE TABLE tab (id NUMBER PRIMARY KEY);
    INSERT INTO tab (id) VALUES (1);
    INSERT INTO tab (id) VALUES (2);
    COMMIT;
    UPDATE tab SET id = id + 1;
    COMMIT;
    ```
    

在 PostgreSQL 中，同样的脚本会报错：
    
    
    CREATE TABLE tab (id numeric PRIMARY KEY);
    INSERT INTO tab (id) VALUES (1);
    INSERT INTO tab (id) VALUES (2);
    UPDATE tab SET id = id + 1;
    ERROR: duplicate key value violates unique constraint "tab_pkey"
    DETAIL: Key (id)=(2) already exists.
    

原因在于，PostgreSQL 默认在每行变化时检查约束（不同于SQL标准），而 Oracle 在语句结束时检查约束。 不过这个问题可以通过将约束创建为 `DEFERRABLE` 来解决，这样 PostgreSQL 会在语句结束时检查约束，并与 Oracle 的行为保持一致。

-------

## 隔离性对比

这是 Oracle 和 PostgreSQL 差异最明显的领域。Oracle 对事务隔离的支持相对有限。

### 事务隔离级别的对比

SQL 标准定义了四个事务隔离级别：`READ UNCOMMITTED`、`READ COMMITTED`、`REPEATABLE READ` 和 `SERIALIZABLE`。 但与标准的详细程度相比，单独的级别定义得比较模糊。例如，标准提到，“脏读”（读取其他事务未提交的数据）在 `READ UNCOMMITTED` 隔离级别下是“可能”的，但并没有明确指出这是否为必需。

Oracle 只提供 `READ COMMITTED` 和 `SERIALIZABLE` 隔离级别。然而后者其实并不完全准确；Oracle 提供的是快照隔离。例如，以下并发事务均会成功（第二个会话如下所示）：
    
    
    CREATE TABLE tab (name VARCHAR2(50), is_highlander NUMBER(1) NOT NULL);
    
    -- start a new serializable transaction
    SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    
    SELECT count(*) FROM tab WHERE is_highlander = 1;
    
    COUNT(*)
    ----------
         0
    
                                                                    -- start a new serializable transaction
                                                                    SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
                                                                    
                                                                    SELECT count(*) FROM tab WHERE is_highlander = 1;
                                                                    
                                                                    COUNT(*)
                                                                         ----------
                                                                         0
    
    -- the count is zero, so let's proceed
    INSERT INTO tab VALUES ('MacLeod', 1);
    
    COMMIT;
    
    -- the count is zero, so let's proceed
    INSERT INTO tab VALUES ('Kurgan', 1);
    
    COMMIT;
    

如果这些事务串行执行，第二个事务的结果应该是 count 为 1。

除了不准确，Oracle 的实现还存在许多问题。例如，如果您创建一个表时未指定 `SEGMENT CREATION IMMEDIATE`，然后在 `SERIALIZABLE` 事务中尝试插入第一行，就会遇到序列化错误。 虽然这在技术上是合法的，但如果在更高的隔离级别遇到问题时，Oracle 会经常抛出序列化错误。

PostgreSQL 支持所有四个隔离级别，但它会默默地将 `READ UNCOMMITTED` 升级为 `READ COMMITTED`（这在 SQL 标准中可能并不符合要求）。 而 `SERIALIZABLE` 事务则是真正的串行化事务。PostgreSQL 的 `REPEATABLE READ` 行为类似于 Oracle 的 `SERIALIZABLE`，但实际上 PostgreSQL 的实现更好。

### `READ COMMITTED` 级别下并发数据修改的对比

默认的事务隔离级别 `READ COMMITTED` 是一个低隔离级别，这意味着许多异常仍然可能发生。

我在之前的文章中描述了其中的一种异常：[事务异常与 `SELECT FOR UPDATE`](https://www.cybertec-postgresql.com/en/transaction-anomalies-with-select-for-update/)。简而言之，情况如下：

  * 一个事务修改了表中的一行，但尚未提交
  * 第二个事务执行了一个锁定行的语句（例如 `SELECT ... FOR UPDATE`），并且挂起
  * 第一个事务提交



在这种情况下，两个数据库系统会有什么结果？在 Oracle 和 PostgreSQL 中，您都能看到最新提交的数据，但细节有所不同：

  * PostgreSQL 只重新评估被锁定的行，操作较快，但可能会导致不一致的结果
  * Oracle 会 **重新执行完整查询** ，尽管速度较慢，但能够提供一致的结果



-------

## 持久性对比

两个数据库系统都通过事务日志实现持久性（Oracle 中为“REDO 日志”，PostgreSQL 中为“WAL日志”）。在这一领域，Oracle 和 PostgreSQL 提供的保证是相同的。

-------

## 其他事务差异

### 事务的大小和持续时间限制

这一领域的差异主要源于 Oracle 和 PostgreSQL 实现多版本并发控制（MVCC）的方式不同。Oracle 使用 _UNDO 表空间_ 来存储已修改行的旧版本，而 PostgreSQL 将多个版本的行存储在表中。

由于这个原因，**Oracle 事务中数据修改的数量受限于 UNDO 表空间的大小** 。对于大批量删除或更新，Oracle 通常会采用分批处理并在每批之间执行 `COMMIT`。 而在 PostgreSQL 中没有这种限制，但大规模更新会导致表膨胀，因此您也可能希望分批更新，并在更新间运行 `VACUUM`。然而在 PostgreSQL 中，并没有理由限制大批量删除的规模。

长时间运行的事务在任何关系型数据库中都是一个问题，因为它们会占用锁并增加阻塞其他会话的几率，长事务也更容易遭遇死锁。 在 PostgreSQL 中，长事务会比 Oracle 更加棘手一些，因为它们还会阻塞“自动清理”（autovacuum）任务的进程，从而导致表膨胀，治理起来要费些事。

### `SELECT ... FOR UPDATE` 的对比

两个数据库系统都知道这个命令，它用于同时读取并锁定一行。Oracle 和 PostgreSQL 都支持 `NOWAIT` 和 `SKIP LOCKED` 子句。 PostgreSQL 缺少 `WAIT <integer>` 子句，但是可以通过动态调整 `lock_timeout` 参数实现类似的功能。

这里最重要的区别在于，PostgreSQL 中如果你打算更新某一行，`FOR UPDATE` **并非** 合适的语句 —— 除非你打算删除某行或修改主键或唯一键列，否则正确的锁定模式应为 `FOR NO KEY UPDATE`。

### 事务ID回卷

[事务ID回卷](https://www.cybertec-postgresql.com/en/autovacuum-wraparound-protection-in-postgresql/) 只在 PostgreSQL 中存在。 PostgreSQL 的多版本控制通过在每一行中存储 [事务ID](https://www.postgresql.org/docs/current/transaction-id.html) 来管理行版本的可见性。

这些编号来自一个 32 位整型计数器，最终会发生回卷。 所以 PostgreSQL 需要执行维护操作（`FREEZE`）来避免出现事务ID回卷。在高事务量（TPS）的系统中，这可能成为一个需要特别关注和调整的问题。

-------

## 结论

在大多数方面，Oracle 和 PostgreSQL 的事务行为非常相似。但它们之间确实存在差异，如果您计划迁移到 PostgreSQL，了解这些差异是很重要的。本文中的对比有助于您在迁移过程中识别潜在的问题。

-------

## 老冯评论

在 [PostgreSQL 17 发布：摊牌了，我不装了！](https://mp.weixin.qq.com/s/oOZIP1CYj4a319YvoT7Y1w) 中提到过，在最近一年，PostgreSQL 社区在心态与精神上有了显著的转变： 不再采用过去佛系与世无争的姿态，而是转变为一种积极进取的姿态，它已经做好了接管与征服整个数据库世界的心理建设与准备。喊出了干翻“顶级商业数据库”（Oracle）的口号。

现在看来，PostgreSQL 社区确实出息了，前有 EDB TPC-C 评测炮打 Oracle 性能，现在又有 Cybertec 点评 Oracle 事务正确性，开始炮轰 Oracle 了。

就比如这篇文章吧，看上去很中立的说了一堆事务系统的对比，也很客观的指出了 PG 和 Oracle 存在的问题。 但实际上在 ACID 的 ACD 上大家都是大同小异，真正的重点是在事务隔离等级上 —— Oracle 的缺陷实现。

是的，号称顶级商业数据库的 Oracle，Serializable 的隔离等级其实是虚标，实际上是 SI 快照隔离。 这个问题其实我在 [MySQL的正确性为何如此拉垮？](https://mp.weixin.qq.com/s/gQZ3Q5JKV8gaBNhc1puPcA) 中已经提到了。

在主流 DBMS 中，只有 PostgreSQL （以及基于PostgreSQL的CockroachDB）提供了真正的 Serializable 。

  * [←上一页](/blog/db/db-is-the-arch/)
  * [下一页→](/blog/db/pg-kiss-duckdb/)



最后修改 2025-02-27: [optimize image (7cb69ff)](https://github.com/pgsty/web.cc/commit/7cb69ff32df80eba158e90dfd39b124ff85b79ab)