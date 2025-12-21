---
title: "Pigsty v2.3：丰富应用生态"
linkTitle: "Pigsty v2.3 发布注记"
date: 2023-08-20
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v2.3.0)）
summary: >
  PGSQL/REDIS升级，NODE集群可绑VIP，Mongo初步支持与MySQL存根
series: [Pigsty]
tags: [Pigsty]
---



Pigsty v2.3 发布了 🎉，在这个版本中进一步完善了监控系统、应用生态、并跟进 PostgreSQL 例行的小版本更新（CVE修复）。

Pigsty v2.3 跟随 PostgreSQL 主干小版本进行更新，包括 15.4, 14.9, 13.12, 12.16 以及 16.beta3，此更新修复了一个 CVE 安全漏洞。此外高可用管控 Patroni 也升级到 3.1 版本，解决了一些 BUG 。

v2.3 提供了对 FerretDB 的支持，它是一个构建在 PostgreSQL 之上，真正开源的 MongoDB 替代。用户可以使用 MongoDB 客户端访问它，但是真正的数据都存储在底层的 PostgreSQL 里。

v2.3 还默认添加了一款名为 NocoDB 的开源应用：这是 AirTable 的开源替代：这是一个数据库-电子表格的混合体，可以用低代码的方式快速打造一个多人在线协作应用。

Pigsty v2.3 新增了为主机节点集群绑定一个 **L2 VIP** 的功能，使用 VRRP 协议确保全链路上没有单点，并提供了完整的监控：keepalived_exporter 被用于收集监控数据。而且每一个 Node VIP （keepalived）与 PGSQL VIP （vip-manager）都会添加到 blackbox_exporter 的 ICMP / PING 监控列表中。

在监控系统上，Pigsty v2.3 在 v2.2 的基础上进行了打磨优化：新增了 VIP 监控，VIP 与节点 PING 指标被加入到 NODE / PGSQL 监控的醒目位置；PGSQL 监控新增了锁等待树视图；REDIS 监控进行了风格优化；MinIO 监控适配的新的监控指标名称；MySQL / MongoDB 监控新增了实现存根，为后续实现奠定基础。



顺带一提，PGSQL x Pigsty 交流群新开3群了，对 PostgreSQL 与 Pigsty 感兴趣的朋友可以直接扫码加入（仅限前200人），如果加入不了请微信搜索 pigsty-cc 小助手加入。





## MongoDB 支持？

MongoDB 是一个很受欢迎的 NoSQL 文档数据库。但由于开源协议问题（SSPL），与软件定位问题（Postgres发型版），Pigsty 决定使用 FerretDB 来提供对 MongoDB 的支持。FerretDB 是一个有趣的开源项目：**它让 PostgreSQL 可以提供 MongoDB 的能力**。

![ferretdb](ferretdb.webp)

MongoDB 与 PostgreSQL 是两个非常不同的数据库系统：MongoDB 使用文档模型，使用专用的查询语言进行交互 。但是鉴于 PostgreSQL 也提供了完整的 JSON/JSONB/GIN 功能支持，所以这么做在理论上也是完全可行的：FerretDB 负责将您的 SON 查询转换为 SQL 查询：

```
use test-- CREATE SCHEMA test;
db.dropDatabase()-- DROP DATABASE test;
db.createCollection('posts')-- CREATE TABLE posts(_data JSONB,...)
db.posts.insert({title: 'Post One',body: 'Body of post one',category: 'News',tags: ['news', 'events'],user: {name: 'John Doe',status: 'author'},date: Date()})-- INSERT INTO posts VALUES(...);
db.posts.find().limit(2).pretty()-- SELECT * FROM posts LIMIT 2;
db.posts.createIndex({ title: 1 })-- CREATE INDEX ON posts(_data->>'title');
```

在 Pigsty 定义一个 FerretDB 集群与其他类型的数据库并无二致，您仅需要提供核心的身份参数：集群名称与实例号。需要关注的是 mongo_pgurl 参数，它指定了 FerretDB 底层使用的 PostgreSQL 地址。

```
ferret:  hosts:    10.10.10.45: { mongo_seq: 1 }    10.10.10.46: { mongo_seq: 2 }    10.10.10.47: { mongo_seq: 3 }  vars:    mongo_cluster: ferret    mongo_pgurl: 'postgres://test:test@10.10.10.3:5436/test'
```

您可以直接填入一个已由 Pigsty 创建的任意 PostgreSQL 服务地址。数据库不需要预先配置什么，你只需要确保所使用的用户具有 DDL 权限即可。

![ferretdb-monitoring](ferretdb-monitoring.webp)

配置完成后，使用 ./mongo.yml -l ferret 即可完成安装。当然，如果您更喜欢使用容器，也可以直接 cd pigsty/app/ferretdb; make 使用 docker-compose 拉起 FerretDB 使用。安装完成后，您可以使用任何 MongoDB Client 访问 FerretDB，例如 MongoSH：

```
mongosh 'mongodb://test:test@10.10.10.45:27017/test?authMechanism=PLAIN'
```

对于那些希望从 MongoDB 迁移到 PostgreSQL 的用户来说，这是一种改造成本极小的折衷手段。Pigsty 同样提供了另一种支持方式 MongoFDW：在 PostgreSQL 中使用 SQL 查询现有的 MongoDB 集群。

## 新应用：NocoDB

在 Pigsty v2.3 中，添加了对 NocoDB 的内置支持，您可以使用默认的 Docker Compose 模板，一键拉起 NocoDB 并使用内置的 PostgreSQL 作为存储。

NocoDB 是 Airtable 的开源替代品，那 AirTable 又是什么呢？其实有点类似于 Google Docs / 腾讯云文档。但是提供了非常丰富的接口，钩子，可以用来实现一些非常强大的功能。

![nocodb](nocodb.webp)

NocoDB 可以让各种关系型数据库变身成为 Excel ，运行你自己的本地云文档软件。它也可以让用户用低代码的方式实现一些需求：比如你可以把自动生成的表单发送给别人填写，将结果自动整理成为实时共享、可协作、可编程的多维表格。

在 Pigsty 中，拉起 NocoDB 非常容易，只需要一行命令即可。您可以修改 .env 中的 DATABASE_URL 参数来使用不同的数据库。

```
cd ~/pigsty/app/nocodb; make up
```



## Node VIP 支持

Pigsty v2.3 新增了为主机节点集群绑定一个 **L2 VIP** 的功能，使用 VRRP 协议确保全链路上没有单点，并提供了完整的监控。

在古早的 Pigsty 版本中（0.5前），曾经提供过基于 Keepalived 的 L2 VIP 功能实现。但随后被 HAProxy + VIP-Manager 所取代：HAProxy 不挑网络，可以进行灵活的健康检查、流量分发，更是提供了一个简单易用的管控界面。而 VIP Manager 则可以将一个 L2 VIP 绑定在数据库集群主库上。

但通用的 L2 VIP 需求仍然是存在的，例如，如果用户选择使用 HAProxy 集群接入，那么 HAProxy 本身的可靠性如何保证？尽管您可以使用 DNS LB 的方式进行切换，但 VRRP 在可靠性与易用性上显然更胜一筹。此外，MinIO / ETCD ，Prometheus 这些组件，有时也会有这样的需求。

想要为集群绑定一个 L2 VIP 其实很简单，只需要启用 vip_enabled，分配一个 VLAN 中唯一的 VirtualRouterID 号与 VIP 地址就可以了。默认情况下，所有集群成员使用 BACKUP 初始状态以非抢占模式工作。你可以通过设置 vip_role 与 vip_preempt 来改变这一行为。



![vip-config](vip-config.webp)

L2 VIP 会自动被纳入监控中。当 MASTER 宕机后， BACKUP 会立即进行接管。

![vip-failover](vip-failover.webp)



## 监控系统改进

Pigsty v2.2 基于 Grafana 10 对监控系统进行了[彻底的翻新重制](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485827&idx=1&sn=9b13273b559fa63e96d4ac77268bd00a&chksm=fe4b3c58c93cb54e87b062c6db4b3a712037e25dbfbe69aa50ad9b79abf2c97967b625fe1a7f&scene=21#wechat_redirect)。v2.3 在 v2.2 的基础上进行了更多优化。

例如，新增的 NODE VIP 监控面板用于展示一个 VIP 的状态：所属集群/成员，网络RT，KA的状态等等等等。

![node-vip-dashboard](node-vip-dashboard.webp)

上图展示了一个 L2 VIP 自动故障转移的现场监控：绑定在 3 节点集群 MinIO 上。当原本的 Master （.27）宕机后，（.26）立即完成接管。

同样的信息也被展示在 NODE 与 PGSQL 监控面板的关键位置：例如，Overview 的实例列表中，现在就会添加 VIP 的快速导航（紫色）：

![node-overview](node-overview.webp)

![pgsql-overview](pgsql-overview.webp)

同理，在 NODE Cluster 与 PGSQL Cluster 中也会在醒目处列出 VIP 与所有成员的 ICMP 可达性状态（Ping 网络延迟）。

![node-cluster-ping](node-cluster-ping.webp)

![pgsql-cluster-ping](pgsql-cluster-ping.webp)

此外，在 PGCAT 中新增了默认 1s 刷新的 PGCAT Locks 监控面板，可以直观的观察数据库当前活跃的情况，以及锁等待的情况。

![pgcat-locks](pgcat-locks.webp)

锁等待会组织成一棵等待树，用 Level 与缩进标识层次。您可以选择不同的刷新率，最快每秒 10 次。

![图片](lock-wait-tree.gif)

在 REDIS 监控上，相关的监控面板也统一按照 PGSQL 与 NODE 的风格进行适配与调整：

![redis-monitoring](redis-monitoring.webp)

## 更丝滑的构建流程

Pigsty v2.2 提供了官方 Yum 源，在 v2.3 中则默认启用了全站 HTTPS。所有

当您选择直接从互联网下载 Pigsty 所需的软件时，可能会遭遇到功夫网的烦恼。例如，默认的 Grafana / Prometheus Yum 源下载速度极慢。除此之外，还有一些零散的 RPM 包需要通过 Web URL 的方式，而不是 repotrack RPM 的方式进行下载。

在 Pigsty v2.2 中，解决了这个问题。Pigsty 提供了一个官方的 yum 源：http://get.pigsty.cc ，并配置为默认的上游源之一。所有零散的 RPM，需要翻墙的 RPM 都放置其中，可以有效加快在线安装/构建速度。

此外， Pigsty 还在 v2.2 中提供了对信创操作系统，统信 UOS 1050e uel20 的支持，满足一些特殊客户的特殊需求。Pigsty 针对这些系统重新编译了 PG相关的 RPM 包，为有需求的客户提供支持。

## 安装



Pigsty v2.3 的安装命令为：

**bash -c "$(curl -fsSL https://get.pigsty.cc/latest)"**

一行命令，即可在全新机器上完整安装 Pigsty. 如果您想要尝鲜 beta 版本，将 latest 换为 beta 即可。对于没有互联网访问的特殊环境，您也可以使用以下链接下载 Pigsty，以及打包了所有软件的离线安装包：

![download](download.webp)

https://get.pigsty.cc/v2.3.0/pigsty-v2.3.0.tgz
https://get.pigsty.cc/v2.3.0/pigsty-pkg-v2.3.0.el7.x86_64.tgz
https://get.pigsty.cc/v2.3.0/pigsty-pkg-v2.3.0.el8.x86_64.tgz
https://get.pigsty.cc/v2.3.0/pigsty-pkg-v2.3.0.el9.x86_64.tgz



以上，就是 Pigsty v2.3 带来的变化。

更多细节，请参考 Pigsty 官方文档：https://vonng.github.io/pigsty/ 与 Github Release Note： https://github.com/Vonng/pigsty/releases/tag/v2.3.0




----------------

## v2.3.0

相关文章：《[Pigsty v2.3 发布：应用生态丰富](https://mp.weixin.qq.com/s/p5sP42xsAxKPhWb_T7DqSA)》

发布注记：https://github.com/Vonng/pigsty/releases/tag/v2.3.0

使用 `bash -c "$(curl -fsSL https://get.pigsty.cc/latest)"` 快速开始。

**亮点特性**

* INFRA: 添加了对 NODE/PGSQL VIP 的监控支持
* PGSQL: 通过小版本升级修复了 PostgreSQL [CVE-2023-39417](https://www.postgresql.org/about/news/postgresql-154-149-1312-1216-1121-and-postgresql-16-beta-3-released-2689/)： 15.4, 14.9, 13.12, 12.16，以及 Patroni v3.1.0
* NODE:  允许用户使用 `keepalived` 为一个节点集群绑定 L2 VIP
* REPO: Pigsty 专用 yum 源优化精简，全站默认使用 HTTPS： [`get.pigsty.cc`](https://get.pigsty.cc) 与 [`demo.pigsty.cc`](https://demo.pigsty.cc)
* APP:  升级 `app/bytebase` 版本至 v2.6.0， `app/ferretdb` 版本至 v1.8；添加新的应用模板：[nocodb](https://nocodb.com/)，开源的 Airtable。
* REDIS: 升级版本至 v7.2，并重制了 Redis 监控面板。
* MONGO: 添加基于 [FerretDB](https://www.ferretdb.io/) 1.8 实现的基本支持。
* MYSQL: 添加了 Prometheus / Grafana / CA 中的代码存根，便于后续纳管。

**API变化**

新增一个新的参数组 `NODE`.`NODE_VIP`：包含 8 个新参数

- `NODE`.`VIP`.`vip_enabled`：在此节点集群上启用 vip 吗？
- `NODE`.`VIP`.`vip_address`：ipv4 格式的节点 vip 地址，如果启用了 vip，则必需
- `NODE`.`VIP`.`vip_vrid`：必需，整数，1-255 在相同 VLAN 中应该是唯一的
- `NODE`.`VIP`.`vip_role`：master/backup，默认为备份，用作初始角色
- `NODE`.`VIP`.`vip_preempt`：可选，true/false，默认为 false，启用 vip 抢占
- `NODE`.`VIP`.`vip_interface`：节点 vip 网络接口监听，eth0 默认
- `NODE`.`VIP`.`vip_dns_suffix`：节点 vip dns 名称后缀，默认为 .vip
- `NODE`.`VIP`.`vip_exporter_port`：keepalived 导出器监听端口，默认为 9650


```
MD5 (pigsty-pkg-v2.3.0.el7.x86_64.tgz) = 81db95f1c591008725175d280ad23615
MD5 (pigsty-pkg-v2.3.0.el8.x86_64.tgz) = 6f4d169b36f6ec4aa33bfd5901c9abbe
MD5 (pigsty-pkg-v2.3.0.el9.x86_64.tgz) = 4bc9ae920e7de6dd8988ca7ee681459d
```





----------------

## v2.3.1

使用 `bash -c "$(curl -fsSL https://get.pigsty.cc/latest)"` 快速开始。

**最新特性**

- `pgvector` 更新至 0.5，添加 hnsw 算法支持。
- 支持 PostgreSQL 16 RC1 (el8/el9)
- 默认包中添加了 SealOS 用于快速部署Kubernetes集群。

**问题修复**

- 修复了 `infra`.`repo`.`repo_pkg` 任务：当 `repo_packages` 中包名包含 `*` 时，下载可能会受到 `/www/pigsty` 现有内容的影响。
- 将 `vip_dns_suffix` 的默认值由 `.vip` 调整为空字符串，即集群本身的名称将默认作为节点集群的 L2 VIP
- `modprobe watchdog` and `chown watchdog` if `patroni_watchdog_mode` is `required`
- 当 `pg_dbsu_sudo` = `limit` and `patroni_watchdog_mode` = `required` 时，授予数据库 dbsu 以下命令的 sudo 执行权限
  - `/usr/bin/sudo /sbin/modprobe softdog`：在启动 Patroni 服务时确保 softdog 内核模块启用
  - `/usr/bin/sudo /bin/chown {{ pg_dbsu }} /dev/watchdog`: 在启动 Patroni 服务时，确保 watchdog 属主正确

**文档更新**

- 向英文文档中添加了更新内容。
- 添加了简体中文版本的内置文档，修复了 pigsty.cc 文档站的中文文档。

**软件更新**

- PostgreSQL 16 RC1 for EL8/EL9
- PGVector 0.5.0，支持 hnsw 索引
- TimescaleDB 2.11.2
- grafana 10.1.0
- loki & promtail 2.8.4
- redis-stack 7.2 on el7/8
- mcli-20230829225506 / minio-20230829230735
- ferretdb 1.9
- sealos 4.3.3
- pgbadger 1.12.2

```
ce69791eb622fa87c543096cdf11f970  pigsty-pkg-v2.3.1.el7.x86_64.tgz
495aba9d6d18ce1ebed6271e6c96b63a  pigsty-pkg-v2.3.1.el8.x86_64.tgz
38b45582cbc337ff363144980d0d7b64  pigsty-pkg-v2.3.1.el9.x86_64.tgz
```
