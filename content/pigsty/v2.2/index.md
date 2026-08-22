---
title: "Pigsty v2.2：监控全面翻新"
linkTitle: "Pigsty v2.2 发布注记"
date: 2023-08-04
authors: [vonng]
summary: >
  监控面板 & 沙箱置备重做，构建流程优化，UOS兼容性
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v2.2.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v220) | [微信公众号](https://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485827&idx=1&sn=9b13273b559fa63e96d4ac77268bd00a&chksm=fe4b3c58c93cb54e87b062c6db4b3a712037e25dbfbe69aa50ad9b79abf2c97967b625fe1a7f&scene=21#wechat_redirect)

[![](featured.webp)](https://github.com/pgsty/pigsty/releases/tag/v2.2.0)

Pigsty v2.2 发布了 🎉，欢迎大家尝鲜！ 地表最强 PostgreSQL 监控系统迎来史诗级重大升级，基于 Grafana v10 彻底重制，将 PG 可观测性拔高到一个全新阶段，带来了全新的用户体验。**Demo**: **http://demo.pigsty.cc** 。

此外 Pigsty v2.2 还提供了一个 **42** 节点的生产仿真环境沙箱模板，支持了 Citus 12，PG 16beta2，提供了使用KVM虚拟机的vagrant模板，为零散/墙外RPM包提供了专用的 Pigsty Yum 源，并支持了国产信创操作系统统信UOS20。

欢迎大家试用尝鲜，提出反馈意见。加 PG x Pigsty 微信讨论群请搜 pigsty-cc 小助手。

另外：8月9号晚7点开源中国出品的直播 《 PostgreSQL vs MySQL》以及8月16号的DTCC 2023，我将代表 PG 一方出战与 MySQL 对喷：谁才是数据库一哥，欢迎大家收看。

---------

## 监控系统重制：视觉配色

Pigsty v2.2 中，对监控面板进行了彻底的重制，充分利用 Grafana v10 的新特性，为用户带来耳目一新的可视化体验。

最直观的变化是色彩。Pigsty v2.2 采用了全新的配色方案.以 PGSQL Overview 面板为例，新配色方案降低了饱和度，整体视觉体验比旧版本更加协调美观。

![图片](01-pgsql-overview-v20.jpg)

> Pigsty v2.0 使用Grafana默认的高饱和配色

![图片](02-pgsql-overview-v22.jpg)

> Pigsty v2.2：失效实例标黑，点击可直达故障现场

在 Pigsty v2.2 的监控面板中使用了 PG蓝，Nginx绿，Redis红，Python黄，Grafana橙等颜色作为基准，这套配色方案的灵感来自这篇文章：SCI，但《天气之子》~当SCI论文插图遇上新海诚天气之子配色 https://zhuanlan.zhihu.com/p/619556088 。

![color-scheme](color-scheme.jpg)

---------

## 监控系统重制：集群导航

当然除了配色，v2.2 也在内容编排和布局上重新进行了设计。例如，使用 Stats 色块统计替代了大量表格式导航，让有问题的服务能够在首屏即可一目了然。点击异常色块即可直达故障现场。

当然，老式的导航表格可以提供更丰富的信息，也并没有移除，而是移动到了专门的 Instances / Members 分栏中去。让我们以最常用的 PGSQL Cluster 面板为例：

![图片](03-pgsql-cluster-stats.jpg)

首屏是基于色块的图元导航，展现了集群组件存活状态与服务可用性，核心指标，负载水平与告警事件图。且提供了到集群内部资源 —— 实例，连接池，负载均衡器，服务，数据库的快速导航

![图片](04-pgsql-cluster-table.jpg)

PGSQL Cluster 的表格式导航

具体的集群资源表，则是在第二栏中，以备查阅详情。配合后面的 指标栏与日志栏，完整的呈现了一个 PostgreSQL 数据库集群的核心状态。

![图片](05-pgsql-cluster-metrics.jpg)

---------

## 监控系统重制：实例

PGSQL Instance 展现了一个实例的详细状态，在 v2.2 中也进行了重制。最基本的设计原则就是：不是蓝/绿色的状态才需要关注。这样通过颜色视觉编码，用户可以在事故分析时快速定位一个数据库实例的故障根因。

![图片](06-pgsql-instance.jpg)

其他的实例，主机节点，ETCD，MinIO，Redis，也都使用了类似的设计，例如 Node Instance 的首屏就是这样的。

![图片](07-node-instance.jpg)

Node Instance 的指标部分基本保持不变，但首屏概览部分进行了重制。MinIO Overview 亦然。

![图片](08-minio-overview.jpg)

Etcd Overview 则使用 State Timeline 来可视化 DCS 服务的可用性状态。例如下图展现了一个模拟 etcd 故障的现场：在一个5节点的 ETCD 集群中依次关闭各个实例，集群可以容忍两个节点故障，但3个节点故障将导致 ETCD 服务整体不可用（黄色的条转为暗蓝色，代表 ETCD 服务整体不可用）。

![图片](09-etcd-overview.jpg)

当 DCS 出现故障时，依赖 ETCD 进行高可用的 PostgreSQL 集群默认会启用 FailSafeMode：在确认所有集群成员可达，不是自身而是DCS故障的前提下，可以避免出现主库降级的故障。而这一点，也会在 PG 的监控中体现出来

![图片](10-pg-failsafe.jpg)

---------

## 监控系统重制：服务

另一个进行重新设计的部分是 Service 与 Proxy 。Service 面板现在添加了关于服务的重要信息：SLI ，通过条状的 Statetimeline，用户可以直观的看出服务中断情况，获取服务可用性指标，并理解负载均衡器与后端真实数据库服务器的状态。

![图片](11-pgsql-service.jpg)

本例中，对 pg-test 集群的四个 HAProxy，分别进行了 排干，设置维护状态操作，然后关闭后端数据库服务器。只有当一个集群的全部实例都下线后， pg-test-replica 这个只读服务才会进入不可用状态。

![图片](12-haproxy-drain.jpg)

这是 pg-test 集群 1 号 HAProxy 负载均衡器的监控面板，每一个由其承载的服务都会列于其中，展示后端服务器状态并计算 SLI。HAProxy 本身的状态与监控放置在 Node Haproxy 监控面板中。

![图片](13-haproxy-instance.jpg)

在全局总览中，可以看到 Pigsty 中所有数据库服务的整体状态时间线与 SLI 指标。

---------

## 监控系统重制：数据库统计

在 Pigsty 中，除了会对数据库服务器进行监控外，也会对数据库服务器所承载的逻辑对象 —— 数据库，表，查询，索引等逻辑。

PGSQL Databases 展示了集群层面的数据库统计指标。例如，在 pg-test 集群中有4个数据库实例，与一个数据库 test ，而这里就展示出了这4个实例数据库指标的水平对比。

![图片](14-pgsql-databases.jpg)

用户可以进一步下钻到 **单个** 数据库实例内部的统计，也就是 PGSQL Database 面板。这个面板提供了一些关于数据库与连接池的关键指标，但最重要的是，PGSQL Database 面板提供了对数据库内最活跃醒目的 **表** 与 **查询** 的索引 —— 这是两类最为重要的库内对象。

![图片](15-pgsql-database.jpg)

用户可以进一步下钻到 **单个** 数据库实例内部的统计，也就是 PGSQL Database 面板。这个面板提供了一些关于数据库与连接池的关键指标，但最重要的是，PGSQL Database 面板提供了对数据库内最活跃醒目的 **表** 与 **查询** 的索引 —— 这是两类最为重要的库内对象。

![图片](16-pgsql-database-tables.jpg)

![图片](17-pgsql-database-queries.jpg)

---------

## 监控系统重制：系统目录

在 Pigsty 中，除了使用 pg exporter 采集到的指标数据之外，还会使用另外一类 **可选** 的重要补充数据 —— 系统目录。这也是 PGCAT 系列 Dashboard 所做的事情。PGCAT Instance 将直接访问数据库系统目录（使用最多8条监控只读连接），获取并呈现所需的信息。

例如，您可以获取数据库当前正在运行的活动，按照各种指标对数据库中的慢查询，无用索引，全表扫描进行定位与分析。查阅数据库的角色，会话，复制情况，配置修改状态，内存使用详情，备份与持久化的具体细节。

![图片](18-pgcat-instance-1.jpg)

![图片](19-pgcat-instance-2.jpg)

如果说 PGCAT Instance 关注的是数据库服务器本身，那么 PGCAT Database 就更关注单个数据库内部的对象细节：例如 Schema，Table，Index，膨胀，Top SQL， Top Table，等等。

![图片](20-pgcat-database.jpg)

每一个 Schema，Table ，Index 都可以点击下钻，进入更详细的专用面板中。例如 PGCAT Schema，就进一步展现了一个架构模式内的对象细节。

![图片](21-pgcat-schema.jpg)

数据库内的查询，也按照执行计划进行聚合，便于用户找到问题 SQL，快速定位慢查询问题。

![图片](22-pgcat-query.jpg)

---------

## 监控系统重制：表与查询

在 Pigsty 中，您可以查阅一张表的方方面面。PGCAT Table 面板可以让您查看表的元数据，上面的索引，每一列的统计信息，以及相关的查询。

![图片](23-pgcat-table.jpg)

当然，您也可以使用 PGSQL Table 面板，从指标的维度，查阅一张表在任意历史时间段上的关键指标。点击表名即可轻松在两个视角进行切换。

![图片](24-pgsql-table.jpg)

相应地，您也可以获取（具有相同执行计划）的同一类 SQL 的详细信息。

![图片](25-pgsql-query-1.jpg)

![图片](26-pgsql-query-2.jpg)

在 Pigsty 中，还有许多关于特定主题的 Dashboard。限于篇幅，关于监控系统的介绍就是这些。最直观的体验方式，就是访问 Pigsty 提供的公开 Demo：http://demo.pigsty.cc ，亲自上手把玩一番。虽然这只是一个4台1C虚拟机的简陋环境，但用来展示Pigsty最基本的监控系统能力已经是足够了。

---------

## 大号仿真环境

Pigsty 提供了一个基于 Vagrant 与 Virtualbox 的沙箱环境，可以跑在你的笔记本电脑/Mac上，有一个 1 节点的最小版本，和一个4节点的完整版本，用与演示与学习，而现在 v2.2 中又多了一个 **42** 节点的生产仿真版本沙箱。

生产沙箱的所有细节都由 prod.yml 这个五百行不到的配置文件描述，它可以轻松跑在一台普通的服务器物理机上，而拉起它过程与4节点并无二致：make prod install 即可完工。

![图片](27-prod-config.jpg)

Pigsty v2.2 提供了基于 libvirt 的 Vagrantfile 模板，您只需要调整上面配置中的机器清单，即可一键创建出所需的虚拟机来。所有东西都可以轻松跑在一台 Dell R730 48C 256G 物理机上，二手价不到三千元。当然，您依然可以使用 Pigsty Terraform 模板一键在云厂商上拉起虚拟机。

安装完成后环境如下所示，包含两节点的监控基础设施，一主一备。5节点的专用 etcd 集群，3 节点的样例 MinIO 集群提供对象存储服务存放 PG 备份，还有一个两节点的专用 HAProxy 集群，可以统一为数据库服务提供负载均衡。

![图片](28-prod-infra.jpg)

在此之上，还有3套Redis数据库集群与10套规格各异的 PostgreSQL 数据库集群与，其中还包括一套开箱即用的 5 分片的 Citus 12 分布式 PostgreSQL 集群。

这个配置是中大型企业运行管理大规模数据库集群的参考样例，而您可以在单台物理服务器上用半个小时完整一键拉起。

---------

## 更丝滑的构建流程

当您选择直接从互联网下载 Pigsty 所需的软件时，可能会遭遇到功夫网的烦恼。例如，默认的 Grafana / Prometheus Yum 源下载速度极慢。除此之外，还有一些零散的 RPM 包需要通过 Web URL 的方式，而不是 repotrack RPM 的方式进行下载。

在 Pigsty v2.2 中，解决了这个问题。Pigsty 提供了一个官方的 yum 源：http://get.pigsty.cc ，并配置为默认的上游源之一。所有零散的 RPM，需要翻墙的 RPM 都放置其中，可以有效加快在线安装/构建速度。

此外， Pigsty 还在 v2.2 中提供了对信创操作系统，统信 UOS 1050e uel20 的支持，满足一些特殊客户的特殊需求。Pigsty 针对这些系统重新编译了 PG相关的 RPM 包，为有需求的客户提供支持。

---------

## 安装

从 v2.2 开始，Pigsty 的安装命令变为：

**bash -c "$(curl -fsSL http://get.pigsty.cc/latest)"**

一行命令，即可在全新机器上完整安装 Pigsty. 如果您想要尝鲜 beta 版本，将 latest 换为 beta 即可。对于没有互联网访问的特殊环境，您也可以使用以下链接下载 Pigsty，以及打包了所有软件的离线安装包：

```bash
http://get.pigsty.cc/v2.2.0/pigsty-v2.2.0.tgz
http://get.pigsty.cc/v2.2.0/pigsty-pkg-v2.2.0.el7.x86_64.tgz
http://get.pigsty.cc/v2.2.0/pigsty-pkg-v2.2.0.el8.x86_64.tgz
http://get.pigsty.cc/v2.2.0/pigsty-pkg-v2.2.0.el9.x86_64.tgz
```

以上，就是 Pigsty v2.2 带来的变化。

更多细节，请参考 Pigsty 官方文档：https://vonng.github.io/pigsty/ 与 Github Release Note： https://github.com/Vonng/pigsty/releases/tag/v2.2.0

----------------

## v2.2.0

相关文章：《[Pigsty v2.2 发布 —— 监控系统大升级](https://mp.weixin.qq.com/s/NfQEL6fM8FA-ErijucXJ4g)》

发布注记：https://github.com/Vonng/pigsty/releases/tag/v2.2.0

快速开始： `bash -c "$(curl -fsSL https://get.pigsty.cc/latest)"`

**亮点特性**

* 监控面板重做: https://demo.pigsty.cc
* Vagrant沙箱重做: 支持 libvirt 与新的配置模板
* Pigsty EL Yum 仓库: 统一收纳零碎 RPM，简化安装构建流程。
* 操作系统兼容性: 新增信创操作系统 UOS-v20-1050e 支持
* 新的配置模板：42 节点的生产仿真配置
* 统一使用官方 PGDG citus 软件包（el7）

**软件升级**

* PostgreSQL 16 beta2
* Citus 12 / PostGIS 3.3.3 / TimescaleDB 2.11.1 / PGVector 0.44
* patroni 3.0.4 / pgbackrest 2.47 / pgbouncer 1.20
* grafana 10.0.3 / loki/promtail/logcli 2.8.3
* etcd 3.5.9 / haproxy v2.8.1 / redis v7.0.12
* minio 20230711212934 / mcli 20230711233044

**Bug修复**

* 修复了 Docker 组权限的问题 [29434bd]https://github.com/Vonng/pigsty/commit/29434bdd39548d95d80a236de9099874ed564f9b
* 将 `infra` 操作系统用户组作为额外的组，而不是首要用户组。
* 修复了 Redis Sentinel Systemd 服务的自动启用状态 [5c96feb](https://github.com/Vonng/pigsty/commit/5c96feb598ad6e44daa7a595e34c87e67952777b)
* 放宽了 `bootstrap` & `configure` 的检查，特别是当 `/etc/redhat-release` 不存在的时候。
* 升级到 Grafana 10，修复了 Grafana 9.x [CVE-2023-1410](https://grafana.com/blog/2023/03/22/grafana-security-release-new-versions-with-security-fixes-for-cve-2023-1410/)
* 在 CMDB `pglog` 模式中添加了 PG 14 - 16 的 command tags 与 错误代码。

**API变化**

新增1个变量

- `INFRA`.`NGINX`.`nginx_exporter_enabled`: 现在用户可以通过设置这个参数来禁用 nginx_exporter 。

默认值变化:

- `repo_modules`: `node,pgsql,infra` : redis 现在由 pigsty-el 仓库提供，不再需要 `redis` 模块。
- `repo_upstream`:
    - 新增 `pigsty-el`: 与具体EL版本无关的RPM: 例如 grafana, minio, pg_exporter, 等等……
    - 新增 `pigsty-misc`: 与具体EL版本有关的RPM: 例如 redis, prometheus 全家桶，等等……
    - 移除 `citus`: 现在 PGDG 中有完整的 EL7 - EL9 citus 12 支持
    - 移除 `remi`: redis 现在由 pigsty-el 仓库提供，不再需要 `redis` 模块。
- `repo_packages`:
    - ansible python3 python3-pip python3-requests python3.11-jmespath dnf-utils modulemd-tools # el7: python36-requests python36-idna yum-utils
    - grafana loki logcli promtail prometheus2 alertmanager karma pushgateway node_exporter blackbox_exporter nginx_exporter redis_exporter
    - redis etcd minio mcli haproxy vip-manager pg_exporter nginx createrepo_c sshpass chrony dnsmasq docker-ce docker-compose-plugin flamegraph
    - lz4 unzip bzip2 zlib yum pv jq git ncdu make patch bash lsof wget uuid tuned perf nvme-cli numactl grubby sysstat iotop htop rsync tcpdump
    - netcat socat ftp lrzsz net-tools ipvsadm bind-utils telnet audit ca-certificates openssl openssh-clients readline vim-minimal
    - postgresql13* wal2json_13* pg_repack_13* passwordcheck_cracklib_13* postgresql12* wal2json_12* pg_repack_12* passwordcheck_cracklib_12* postgresql16* timescaledb-tools
    - postgresql15 postgresql15* citus_15* pglogical_15* wal2json_15* pg_repack_15* pgvector_15* timescaledb-2-postgresql-15* postgis33_15* passwordcheck_cracklib_15* pg_cron_15*
    - postgresql14 postgresql14* citus_14* pglogical_14* wal2json_14* pg_repack_14* pgvector_14* timescaledb-2-postgresql-14* postgis33_14* passwordcheck_cracklib_14* pg_cron_14*
    - patroni patroni-etcd pgbouncer pgbadger pgbackrest pgloader pg_activity pg_partman_15 pg_permissions_15 pgaudit17_15 pgexportdoc_15 pgimportdoc_15 pg_statement_rollback_15*
    - orafce_15* mysqlcompat_15 mongo_fdw_15* tds_fdw_15* mysql_fdw_15 hdfs_fdw_15 sqlite_fdw_15 pgbouncer_fdw_15 multicorn2_15* powa_15* pg_stat_kcache_15* pg_stat_monitor_15* pg_qualstats_15 pg_track_settings_15 pg_wait_sampling_15 system_stats_15
    - plprofiler_15* plproxy_15 plsh_15* pldebugger_15 plpgsql_check_15*  pgtt_15 pgq_15* pgsql_tweaks_15 count_distinct_15 hypopg_15 timestamp9_15* semver_15* prefix_15* rum_15 geoip_15 periods_15 ip4r_15 tdigest_15 hll_15 pgmp_15 extra_window_functions_15 topn_15
    - pg_background_15 e-maj_15 pg_catcheck_15 pg_prioritize_15 pgcopydb_15 pg_filedump_15 pgcryptokey_15 logerrors_15 pg_top_15 pg_comparator_15 pg_ivm_15* pgsodium_15* pgfincore_15* ddlx_15 credcheck_15 safeupdate_15 pg_squeeze_15* pg_fkpart_15 pg_jobmon_15
- `repo_url_packages`:
    - https://get.pigsty.cc/rpm/pev.html
    - https://get.pigsty.cc/rpm/chart.tgz
- `node_default_packages`:
    - lz4,unzip,bzip2,zlib,yum,pv,jq,git,ncdu,make,patch,bash,lsof,wget,uuid,tuned,nvme-cli,numactl,grubby,sysstat,iotop,htop,rsync,tcpdump
    - netcat,socat,ftp,lrzsz,net-tools,ipvsadm,bind-utils,telnet,audit,ca-certificates,openssl,readline,vim-minimal,node_exporter,etcd,haproxy,python3,python3-pip
- `infra_packages`
    - grafana,loki,logcli,promtail,prometheus2,alertmanager,karma,pushgateway
    - node_exporter,blackbox_exporter,nginx_exporter,redis_exporter,pg_exporter
    - nginx,dnsmasq,ansible,postgresql15,redis,mcli,python3-requests
- `PGSERVICE` in `.pigsty` 被移除了，取而代之的是 `PGDATABASE=postgres`，这用户只需 IP 地址就可以从管理节点访问特定实例。

目录结构变化:

- `bin/dns` and `bin/ssh` 现在被移动到 `vagrant/` 目录中。

```bash
MD5 (pigsty-pkg-v2.2.0.el7.x86_64.tgz) = 5fb6a449a234e36c0d895a35c76add3c
MD5 (pigsty-pkg-v2.2.0.el8.x86_64.tgz) = c7211730998d3b32671234e91f529fd0
MD5 (pigsty-pkg-v2.2.0.el9.x86_64.tgz) = 385432fe86ee0f8cbccbbc9454472fdd
```
