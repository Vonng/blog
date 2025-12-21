---
title: "Pigsty v3.1：Supabase一键自建，PG17上位，ARM与Ubuntu24支持，MinIO改进"
linkTitle: "Pigsty v3.1 发布注记"
date: 2024-11-24
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v3.1.0)）
summary: >
  一键自建Supabase，MinIO自建改进，PG17作为默认大版本，提供ARM64与Ubuntu24支持，简化配置管理。
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v3.1.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v310) | [微信公众号](https://mp.weixin.qq.com/s/MNM5wlnIqa3QUAcvYGHKqg)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v3.1.0)

随着前天 PostgreSQL 17.2 的发布，Pigsty 也立即跟进了 v3.1 版本。
在这个版本中，PostgreSQL 17 被提升成为默认使用的大版本，近 340 个 PG 扩展插件开箱即用。

此外，Pigsty 3.1 还提供了一键 [自建 Supabase](/docs/pgsql/kernel/supabase) 的能力，改进了 [MinIO](/docs/minio) 对象存储的使用最佳实践。
与此同时，Pigsty还提供了ARM64 架构的初步支持，并且支持了新发布的 Ubuntu 24.04 大操作系统发行版大版本。
最后，这个版本提供了一系列开箱即用的场景化模板，统一了不同操作系统发行版使用配置文件，极大简化了配置管理工作。


--------

## 自建Supabase

Supabase 是一个开源的 Firebase 替代，对 PostgreSQL 进行了封装，并提供了认证，开箱即用的 API，边缘函数，实时订阅，对象存储，向量嵌入能力。
Supabase 的口号是：“**花个周末写写，随便扩容至百万**”。在试用之后，我觉得此言不虚。
这是一个低代码的一站式后端平台，能让你几乎告别大部分后端开发的工作，只需要懂数据库设计与前端即可快速出活了！

![supa-price.png](supa-price.jpg)

小微规模（4c8g）内的 Supabase 云服务[极有性价比](https://supabase.com/pricing)，堪称赛博菩萨。那 Supabase 云服务这么香，为什么要自建呢？有几个原因：

最直观的原因是是《[云计算泥石流](/blog/cloud)》中说过的：云数据库服务只要稍微上一点儿规模，成本就很容易爆炸。而且考虑到当下本地 NVMe 盘的无敌性价比，自建的成本与性能优势是显而易见的。

另一个重要的原因是 Supabase 云服务的功能受限 —— [与RDS逻辑相同](https://mp.weixin.qq.com/s/EH7RPB6ImfMHXhOMU7P5Qg)，很多强力扩展出于多租户的安全问题考虑是不太可能在云端提供的 —— supabase 云服务中有64个可用扩展，但使用 Pigsty 自建 supabase 时，你可以拥有全部 [**340**](https://pgext.cloud/zh/list) 个。
此外，Supabase 官方使用 PostgreSQL 15 作为底层数据库，而在 Pigsty 中，你可以使用 PG 14 - 17 的任意版本，运行在 EL / Debian / Ubuntu 主流 Linux [操作系统裸机](/docs/ref/compare) 上而无需虚拟化支持，充分地利用现代硬件的性能与成本优势。

我发现身边很多创业出海公司都在使用 Supabase，而其中一些的规模确实已经达到了需要自建的状态，而且有人愿意付费咨询来做这件事了。
所以 Pigsty 早在去年9月发布的 v2.4 就支持自建 Supabase （所需的 PostgreSQL）了。但那毕竟还涉及到一些手工操作，比如配置 PG 集群，拉起 Docker。
而在这个版本中，我们将体验优化到了这种状态 —— 一台新装操作系统的裸机，执行以下几条命令之后，一套新鲜的 Supabase 就出炉了！

![supabase-selfhosting.png](supabase-selfhosting.jpg)

这两天我会准备一些关于 [自建 Supabase 最佳实践](/docs/pgsql/kernel/supabase) 的教程，敬请期待。



--------

## PostgreSQL 17

在《[PG12过保，PG17上位](/blog/pg/pg12-eol-pg17-up/)》中，我们已经详细介绍了 PostgreSQL 17 的新特性与改进。

其中最令人欣慰的莫过于白给的性能优化了：PostgreSQL 17 据说在写入性能上有了显著提升。我找了一台物理机测试了一下，确实不错。
相比与三年前针对 PostgreSQL 14 的测试结果《[PostgreSQL到底有多强](/blog/pg/pg-performence)》，写入确实有不小的提升。

例如，以前 PG 14 在标准配置下，PG 的 WAL 写入吞吐量在 110 MB/s 附近，这是软件的瓶颈，不是硬件的。
而在 PG 17 下，这个数字能达到 180 MB/s。当然，把安全开关都关掉后性能还能翻几番，但体面评测就不玩那些作弊手段了

![perf.png](perf.jpg)

Pigsty 3.1 + PostgreSQL 17 的性能回归测试，详细的性能评测报告将会在最近几天发出，敬请期待。


----------------

## 340个扩展插件

Pigsty 3.1 版本的另一个亮点特性是，这个版本中提供了 **340** 个 PostgreSQL 扩展插件。
这是一个非常恐怖的数字了，而且这是在我进行审慎精选踢出十几个“扩展”后的结果，不然按照本期规划应该能到 360 个了。

为了实现这一目标，我建设了一个 YUM / APT 仓库，针对 EL 8/9, Ubuntu 22.04/24.04, Debian 12 这几个主流操作系统发行版，
以及 PG 12 - 17 这六个大版本提供开箱即用的扩展 RPM/DEB 包。目前提供 x86_64 的包，ARM64 和其他架构还在路上，目前仅对专业用户按需提供。
当然除了仓库之外，更重要的是我还维护了一个 [扩展目录](https://pgext.cloud/zh)，详细记录了每个扩展的元数据， OS/DB 版本可用性，以及一些使用说明，方便用户找到自己需要的扩展。

![ext-repo.png](ext-repo.jpg)

Pigsty 的扩展仓库基于原生的操作系统包管理器，公开共享，你不一定非要使用 Pigsty 才能按照这些扩展。
你完全可以在现有系统，Dockerfile中添加此仓库并通过 yum/apt install 的方式安装这些扩展。
目前我很欣慰的是有一个比较流行的开源集群部署项目 postgresql-cluster 已经默认用起了这个仓库，作为安装流程的一部分，向用户提供并分发扩展插件。

![postgresql-cluster.png](postgresql-cluster.jpg)

当然，更多细节，在《[PostgreSQL神功大成，最全扩展仓库](/blog/pg/pg-ext-repo/)》中对此已经有过介绍。
目前使用 Rust + pgrx 开发扩展的新项目不少，Pigsty 收录了 **23** 个 Rust 扩展。
如果你有好的扩展推荐，欢迎告诉我，我会考察测试后，尽快将其加入到仓库中。
如果你是 PostgreSQL 扩展作者，我们也欢迎将你的扩展提交到 Pigsty 仓库中，我们可以帮助您打包分发，解决最后一公里的交付问题。


----------------

## Ubuntu 24.04 支持

Ubuntu 24.04 noble 已经发布半年了，已经开始有一些用户在生产环境中真实使用它了。
因此，Pigsty v3.1 版本也提供了对 Ubuntu 24.04 的正式支持。

尽管如此，作为一个比较新的系统，Ubuntu 24.04 相比 22.04 还有一些缺陷，例如 `citus` 和 `topn` 扩展在整个系统上是缺位的，而 `timescaledb_toolkit` 目前还没有提供 u24 x86_64 的支持。
但总体来说，除了这些个例外，绝大部分扩展都已经支持 Ubuntu 24.04 了。因此将其纳入 Pigsty 的主要支持范围是没有问题的。

相应地，我们将 Ubuntu 20.04 focal 从 Pigsty 主力支持的操作系统中逐出，虽然 Ubuntu 20.04 在明年五月份才正式 EOL。
但是因为它的一些软件缺漏与依赖版本问题比较严重（PostGIS），我非常乐意能将其提早淘汰，踢出开源版本的支持范畴。
当然，理论上您还是可以继续在 Ubuntu 20.04 上安装并使用，而且在我们的订阅服务中也继续提供对 Ubuntu 20.04 的支持。

因此，目前 Pigsty 支持的主流操作系统发行版为：EL 8/9, Ubuntu 22.04 / Ubuntu 24.04, 以及 Debian 12 这五个。
我们会针对这五个操作系统发行版提供最新的软件包，完整的扩展插件。

|  Code   | OS Distro                         |   `x86_64`   |                       PG17                       |                        PG16                        |                        PG15                        |                        PG14                        |                        PG13                        |                      PG12                       |   `Arm64`   |                                             PG17 |                        PG16                        |                        PG15                        |                        PG14                        |                        PG13                        |                      PG12                       |
|:-------:|-----------------------------------|:------------:|:------------------------------------------------:|:--------------------------------------------------:|:--------------------------------------------------:|:--------------------------------------------------:|:--------------------------------------------------:|:-----------------------------------------------:|:-----------:|-------------------------------------------------:|:--------------------------------------------------:|:--------------------------------------------------:|:--------------------------------------------------:|:--------------------------------------------------:|:-----------------------------------------------:|
| **EL9** | RHEL 9 / Rocky9 / Alma9           | `el9.x86_64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> | `el9.arm64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> |
| **EL8** | RHEL 8 / Rocky8 / Alma8 / Anolis8 | `el8.x86_64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> | `el8.arm64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> |
| **U24** | Ubuntu 24.04 (`noble`)            | `u24.x86_64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> | `u24.arm64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> |
| **U22** | Ubuntu 22.04 (`jammy`)            | `u22.x86_64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> | `u22.arm64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> |
| **D12** | Debian 12 (`bookworm`)            | `d12.x86_64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> | `d12.arm64` | <i class="fas fa-circle-check text-primary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-secondary"></i> | <i class="fas fa-circle-check text-danger"></i> |
| **D11** | Debian 11 (`bullseye`)            | `d12.x86_64` | <i class="fas fa-circle-check text-danger"></i>  |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   | <i class="fas fa-circle-check text-danger"></i> | `d11.arm64` |                                                  |                                                    |                                                    |                                                    |                                                    |                                                 |
| **U20** | Ubuntu 20.04 (`focal`)            | `d12.x86_64` | <i class="fas fa-circle-check text-danger"></i>  |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   | <i class="fas fa-circle-check text-danger"></i> | `u20.arm64` |                                                  |                                                    |                                                    |                                                    |                                                    |                                                 |
| **EL7** | RHEL7 / CentOS7 / UOS ...         | `d12.x86_64` |                                                  |                                                    |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   |  <i class="fas fa-circle-check text-danger"></i>   | <i class="fas fa-circle-check text-danger"></i> | `el7.arm64` |                                                  |                                                    |                                                    |                                                    |                                                    |                                                 |

> <i class="fas fa-circle-check text-primary"></i> = 首要版本支持；<i class="fas fa-circle-check text-secondary"></i> = 配置可选支持； <i class="fas fa-circle-check text-danger"></i> = 过期版本商业支持


----------------

## ARM 支持

ARM 架构最近不断攻城略地，尤其是在云计算领域，ARM 服务器的市场份额正在逐渐增加。早在俩年前，就有用户提出对 ARM 架构支持的需求。
其实 Pigsty 在早先做 “国产化系统” 适配的时候，就已经有一个 ARM 支持了。但是在开源版本中提供 ARM64 架构支持，v3.1 版本是第一次。

当然，目前的版本，ARM 还处在一个 Beta 状态：功能是有了，也能跑通，但是到底效果怎么样还是要跑一段时间，有了反馈才知道。

目前 Pigsty 的主体功能已经都完成适配了，比如 Grafana / Prometheus  全家桶这些我也都打好了 ARM 的软件包，
尚未支持的部分主要是 PG 扩展 —— 特指由 Pigsty 维护的 140 个扩展 —— 目前还没有提供 ARM 支持，已经在做了。
不过，如果你用到的扩展都是 PGDG 中已经提供的（比如 postgis, pgvector 这种），那么没有问题。

目前，ARM 版本在 EL9，Debian 12，Ubuntu 22.04 上运行状态良好。
EL8 有一些PGDG官方包缺失，Ubuntu24有个别扩展缺失，所以目前还不建议在这两个系统上使用 ARM 版本。

我准备将 ARM 试点运行一两个小版本，当扩展齐全之后，我会将其标记为 GA。欢迎各位朋友试用 ARM 版本并向我提出反馈意见。




----------------

## 配置简化

另一个在 Pigsty v3.1 中进行的显著改进是配置简化，如何管理不同操作系统发行版，大小版本的软件包差异一直是一个比较让人头疼的问题。

比如，因为很多操作系统发行版上的包名，可用软件集合其实是有一些区别的，所以在此前的版本里，Pigsty 会根据每个操作系统发行版生成一个独立的配置文件。
但是这样很快就会出现排列组合爆炸，比如，Pigsty 默认提供十几种场景下的配置模板，如果每个模板都要针对 5 - 7 个 操作系统版本生成，那么总数就要爆炸了。

但计算机科学中的任何问题都可以通过增加一个间接层来解决，而这个问题呢也也不例外。在 v3.1 版本中，Pigsty 引入了一个新的配置文件 `package_map`，用于定义软件包的别名。
然后针对每个操作系统发行版，我们都会生成一个 `node_id/vars` 配置文件，将固定的包别名翻译为操作系统上具体的软件包列表。

![config.png](config.jpg)

比如，Supabase 自建模板中启用了几十个扩展，用户只需要提供扩展的名字就可以了，至于芯片架构，操作系统版本，PG版本，包名之类的细节差异全都在内部处理好了。

```bash
pg_extensions: # extensions to be installed on this cluster
- supabase   # essential extensions for supabase
- timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
- supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
- pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
```

举个例子，如果你想下载安装 PG 16 的内核与扩展，以前你需要把下载列表和安装列表里的包全换成16的版本，现在你只需要简单的修改一个 `pg_version` 参数就行了。
最后的效果非常好，基本实现了所有操作系统发行版都能使用相同的配置文件进行安装，将不同系统的差异与管理复杂度都隐藏在了内部。




----------------

## 基础设施改进

除了功能上的改进之外，我们还在不断改善基础设施。例如在 v3.0 引入的安装 MSSQL 兼容的 Babelfish 内核，Oracle 兼容的 IvorySQL 内核，以及国产 PolarDB 内核，都要求用户使用一个外部仓库在线安装。

现在，Pigsty 官方仓库直接提供了 Babelfish，IvorySQL，PolarDB 等内核的镜像仓库，安装这些“异国风味”PG替换内核变得更加简单了 —— 现在的效果就是，不需要什么额外的配置，使用预置模板一键安装即可。

此外，我们还维护着 Prometheus 与 Grafana 的 YUM/ATP x AMD/ARM 软件仓库，并实时跟进这些可观测性组件的版本。在这次升级中，Prometheus 升级到了 v3 大版本，而 VictoriaLogs 也正式发布了 v1 版本。
总的来说，如果你需要用到这些监控软件，Pigsty 的仓库也能帮到您。



----------------

## MinIO 改进

最后我们来聊一下开源对象存储自建，MinIO。
Pigsty 将 MinIO 用作 PostgreSQL 的备份存储，与 Supabase 的底层存储服务，
并致力于将 MinIO 的部署门槛压低到有手就行 —— Deploy in minutes, Scale to millions。

在我们最早内部使用 MinIO 的时候，还是 0.x 的版本，而从那时到现在 MinIO 也有了很大的进步。
当年我们用 MinIO 存 25 PB 数据，因为 MinIO 不支持在线扩容，所以只能拆出了七八个独立集群依次使用。
而现在 MinIO 虽然仍然不能在线修改磁盘/节点数量，但可以通过添加存储池 - 迁移 - 淘汰旧存储池的方式实现平滑扩容了。

![minio.png](minio.jpg)

在 Pigsty v3.1 中，我重新通读了 MinIO 的文档，并根据新版本的特性调整了 MinIO 的最佳实践配置模板与SOP。
除了之前的 MinIO 单机单盘，单机多盘，多机多盘模式，我们还支持了多存储池部署模式，并提供了 Pigsty 中 MinIO 的管理预案 ——
包括磁盘故障，节点故障的处理，集群上下线，存储扩缩容，使用 VIP 与 HAProxy 对外提供高可用接入的方案，全都有据可查，几行命令就能轻松解决。

对象存储是云上的基石性服务，MinIO 作为开源对象存储的代表，其性能与功能都非常优秀，更重要的是，它是一个云中立的开源软件。

您也可以使用 MinIO 来替代云上的对象存储服务，正如《[DHH：下云超预期，能省一个亿](https://mp.weixin.qq.com/s/mknFXO5DSfxw7st8hhxjBQ)》所述，
他们云上有 10PB 的对象存储（列表价每年300万），SavingPlan打折后每年130万美元，合 93万人民币 / PB·年。
而 1.2 PB的专用存储服务器一台十几万人民币上下，三副本冗余， 整几台套上MinIO就是对象存储了。
再加上网电运维，整个五年TCO 也超不过云上一年的折后消费，所以这里蕴含着惊人的降本增效潜力。
如果你的的业务在大量使用对象存储，那么本地 MinIO 自建 + Cloudflare 可能是非常值得考虑的一个更优解。


----------------

## 服务体系


Pigsty v3.1 达到了一个我比较满意的状态，接下来我的工作重心会放在服务体系的构建上。

Pigsty 是个开源免费的软件，它已经解决了 PG 运维中会遇到的绝大多数问题。如果你自己是开源老司机，真遇上疑难杂症自己也可以解决。
但是对于一些大型企业用户，特别是那些没有专职 DBA 的企业来说，还是需要有人来“兜底”的，毕竟，开源软件的核心就是 NO WARRANTY。

正如《[PolarDB20块好兄弟：数据库到底应该卖什么价](https://mp.weixin.qq.com/s/E0MtNxPVMQ4PAkIFmispTw)》中所述，体面数据库服务其实是有市场公允价的，一般在 **1~2万人民币 / vCPU·年**。
不论你是去买 Oracle 的服务支持，还是 EDB，Fujitsu 的开源PG服务，或者是 AWS 的 RDS / Aurora ，其实都是这个价位。

之前我定的服务价格太低，已经引起海内外同行微词 —— 乃这不是破坏市场，低价倾销吗？你作为国内顶级PG专家定这个价还公开，让我们怎么办。

![price.png](price.jpg)

所以这次我也重新调整了一下定价体系，基本锚定业界平均定价水平。反正这也是你情我愿的双向选择，欢迎有兴趣的朋友们选购专业服务，打钱支持！新人新办法，老客老价格。




----------------

## v3.1.0

**亮点特性**

- PostgreSQL 17 现已成为默认使用的主要版本 (17.2)
- Ubuntu 24.04 系统支持
- arm 架构支持：EL9, Debian12, Ubuntu 22.04
- Supabase 一键自建，新的剧本 `supabase.yml`
- MinIO 最佳实践改进，配置模板与 Vagrant 模板
- 提供了一系列开箱即用的配置模板与文档说明。
- 允许在 `configure` 过程中使用 `-v|--version` 指定使用的 PG 大版本。
- 调整 PG 默认插件策略：默认安装 `pg_repack`, `wal2json` 以及 `pgvector` 三个关键扩展。
- 大幅简化 `repo_packages` 本地软件源构建逻辑，允许在 `repo_packages` 中使用软件包组别名
- 提供了 WiltonDB，IvorySQL，PolarDB 的软件源镜像，简化三者的安装。
- 默认启用数据库校验和。
- 修复 ETCD 与 MINIO 日志面板

**软件升级**

- PostgreSQL 17.2, 16.6, 15.10, 14.15, 13.18, 12.22
- PostgreSQL 扩展版本变动请参考：https://pgext.cloud/zh
- Patroni 4.0.4
- MinIO 20241107 / MCLI 20241117
- Rclone 1.68.2
- Prometheus: 2.54.0 -> 3.0.0
- VictoriaMetrics 1.102.1 -> 1.106.1
- VictoriaLogs v0.28.0 -> 1.0.0
- vslogcli 1.0.0
- MySQL Exporter 0.15.1 -> 0.16.0
- Redis Exporter 1.62.0 -> 1.66.0
- MongoDB Exporter 0.41.2 -> 0.42.0
- Keepalived Exporter 1.3.3 -> 1.4.0
- DuckDB 1.1.2 -> 1.1.3
- etcd 3.5.16 -> 3.5.17
- tigerbeetle 16.8 -> 0.16.13



**API变更**

- `repo_upstream`: 针对每个具体的操作系统发行版生成默认值：[`roles/node_id/vars`](https://github.com/Vonng/pigsty/tree/main/roles/node_id/vars)
- `repo_packages`: 允许使用 `package_map` 中定义的别名。
- `repo_extra_packages`: 新增未指定时的默认值，允许使用 `package_map` 中定义的别名。
- `pg_checksum`: 默认值修改为 `true`，默认打开。
- `pg_packages`: 默认值修改为：`postgresql, wal2json pg_repack pgvector, patroni pgbouncer pgbackrest pg_exporter pgbadger vip-manager`
- `pg_extensions`: 默认值修改为空数组 `[]`。
- `infra_portal`: 允许为 `home` 服务器指定 `path`，替代默认的本地仓库路径 `nginx_home` (`/www`)

