---
title: 面向未来数据库的现代硬件
linkTitle: "面向未来数据库的现代硬件"
date: 2024-11-20
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [微信原文](https://mp.weixin.qq.com/s/0Y17J-opjq1fceRi8777Xg) | [英文原文](https://transactional.blog/blog/2024-modern-database-hardware)
summary: >
  本文是一篇关于硬件发展如何影响数据库设计的综述，分别介绍了在网络，存储，计算三个领域的关键硬件进展
tags: [数据库]
---


> 作者：Alex Miller 2024-11-19 @ Snowflake, Apple, Google
>
> 译者：冯若航 & GPT o1，PG 大法师，数据库老司机，云计算泥石流

译者推荐：本文是一篇关于硬件发展如何影响数据库设计的综述，分别介绍了在网络，存储，计算三个领域的关键硬件进展。我一直都认为，充分利用好新硬件（而非折腾所谓分布式）才是数据库内核发展的正路。
请看《[重新拿回计算机硬件的红利](https://mp.weixin.qq.com/s/1OSRcBfd58s0tgZTUZHB9g)》与《[分布式数据库是伪需求吗](https://mp.weixin.qq.com/s/-eaCoZR9Z5srQ-1YZm1QJA)》。
而这篇文章很好地介绍了一些数据库领域的前沿软硬件结合实践，值得一读。




--------


[原文：Modern Hardware for Future Databases](https://transactional.blog/blog/2024-modern-database-hardware)

我们正处于一个令人兴奋的数据库时代，每个主要资源领域都在不断进步，每一项进步都有可能影响最优的数据库架构。总的来说，我希望在未来十年内，能看到数据库架构发生一些有趣的转变，但我不确定是否能有必要的硬件支持。


--------

## 网络

根据 [Stonebraker 在 HPTS 2024 的演讲](https://muratbuffalo.blogspot.com/2024/09/hpts24-day-1-part-1.html)，使用 VoltDB 的一些基准测试发现，其服务器端大约 60% 的 CPU 时间花在了 TCP/IP 协议栈上。VoltDB 本身就是一种旨在尽可能消除非查询处理工作以服务请求的数据库架构，所以这是一个极端的例子。然而，这仍然有效地指出了 TCP 的计算开销并不小，且随着网络带宽的增加，这一问题会变得更加明显。尽管这并不是新的观察结果，但已有一系列逐步升级的解决方案被提出。

一种被提议的解决方案是用另一种基于 UDP 的协议替换 TCP，QUIC 就是一个常被选择的例子。然而，这种想法存在误区。["虽然这是一个严重不准确的简化，但在最简单的层面上，QUIC 只是将 TCP 封装并加密在 UDP 负载中。"](https://blog.apnic.net/2022/11/03/comparing-tcp-and-quic/) TCP 和 QUIC 的 CPU 开销[也非常相似](https://www.fastly.com/blog/measuring-quic-vs-tcp-computational-efficiency)。要想实现显著的改进，需要进一步偏离 TCP 并针对特定环境进行专门化，例如 [Homa](https://networking.harshkapadia.me/files/homa/research-papers/its-time-to-replace-tcp-in-the-datacenter-v2.pdf) 这样的论文展示了在数据中心环境中的一些改进。但即使有了更好的协议，更大的优化潜力还是在于减少内核网络栈的开销。

> **注释**：如果你在阅读时想知道为什么这里提到了 QUIC，那是因为我多次参与了关于 TCP 或 TLS 被指责为某些问题的讨论，而迁移到 QUIC 被建议为解决方案。QUIC 确实能帮助解决一些问题，但也有一些问题它并不能改善，甚至可能使其更糟。需要理解的是，在稳定状态下的延迟和带宽属于后者。

一种减少内核工作量的方法是将计算密集但简单的部分移至硬件。这在一段时间内已经逐步实现，例如增强了[将分段和校验任务卸载到网卡](https://docs.kernel.org/networking/segmentation-offloads.html)。更近期的改进是 [KTLS](https://www.kernel.org/doc/html/v5.2/networking/tls-offload.html)，它允许将 TLS 中的数据包加密也卸载到网卡。尝试将整个 TCP 卸载到硬件中，以 [TCP 卸载引擎（TOE）](https://wiki.linuxfoundation.org/networking/toe) 的形式，已被 Linux 维护者系统性地拒绝了。因此，尽管有了这些不错的改进，但 TCP 协议栈的主要部分仍然是内核的责任。

因此，另一种解决方案是去除内核作为网卡和应用程序之间的中间层。像 [数据平面开发套件（DPDK）](https://www.dpdk.org/) 这样的框架允许用户空间轮询网卡以获取数据包，消除了中断的开销，将所有处理保留在用户空间意味着不需要进入和退出内核。DPDK 在采用方面也遇到了困难，因为它需要对网卡的独占控制。因此，每个主机需要有两个网卡，一个用于 DPDK，另一个用于操作系统和其他所有进程。Marc Richards 制作了一个不错的[Linux 内核 vs DPDK基准测试](https://talawah.io/blog/linux-kernel-vs-dpdk-http-performance-showdown/)，结果显示 DPDK 提供了 50% 的吞吐量提升，随后列举了为获得这 50% 增益而需要接受的一系列缺点。看来这是大多数数据库不感兴趣的权衡，甚至 ScyllaDB 也基本上放弃了对此的投入。

更新的硬件提供了一个有趣的新选项：将 CPU 从网络路径中移除。[RDMA（远程直接内存访问）](https://www.naddod.com/blog/easily-understand-rdma-technology) 提供了 *verbs*，一组有限的操作（主要是读、写和 8 字节的 CAS），这些操作可以完全在网卡内执行，无需 CPU 交互。切断 CPU 后，远程读取的延迟接近 1 微秒，而 TCP 的延迟则超过 100 微秒。作为 RDMA 的一部分，数据包丢失和流量控制的责任也完全下放到网卡。切断 CPU 还意味着可以在不使 CPU 成为瓶颈的情况下传输大量数据。

> **注释**：为什么将丢包检测和流量控制下放到硬件对于 RDMA 是可接受的，但 Linux 维护者一直拒绝对 TCP 这样做？因为这是一个不同且受限得多的 API，减少了网卡与主机之间的复杂性。[《TCP 卸载是一个愚蠢但已经到来的想法》](https://scholar.google.com/scholar?cluster=4106138525527042387) 是在这个领域一篇有趣的阅读材料。（来自 2003 年！）

将 RDMA 作为低延迟和高吞吐量的网络原语，改变了人们设计数据库的方式。[《神话的终结：分布式事务可以扩展》](https://www.vldb.org/pvldb/vol10/p685-zamanian.pdf/) 显示了 RDMA 的低延迟使经典的 2PL+2PC 能够扩展到大型集群。[《云中可扩展的 OLTP 是一个已解决的问题吗？》](https://www.cidrdb.org/cidr2023/papers/p50-ziegler.pdf) 提出了在节点之间共享可写页面缓存的想法，因为低延迟使组件的更紧密耦合变得可行。RDMA 不仅适用于 OLTP 数据库；BigQuery 使用了基于 [RDMA Shuffle 的连接](https://cloud.google.com/blog/products/bigquery/in-memory-query-execution-in-google-bigquery)，因为其高吞吐量。改变给定吞吐量下的延迟和 CPU 利用率，改变了最佳设计的选择，或者解锁了以前被认为不可行的新设计[^3]。

> **注释**：要使用 RDMA，我强烈建议使用 [libfabric](https://ofiwg.github.io/libfabric/)，因为它对所有不同的 RDMA 供应商和库进行了抽象。[RDMAmojo 博客](https://rdmamojo.com/) 有多年关于 RDMA 的专业内容，是学习 RDMA 各个方面的最佳资源之一。

最后，还有一类更新的硬件，延续了将更多计算能力放入网卡本身的趋势，即 SmartNIC 或数据处理单元（DPUs）。它们允许将任意计算下放到网卡，并可能响应其他网卡的请求而被调用。这些技术相当新颖，我建议查看 [《DPDPU：使用 DPU 进行数据处理》](https://scholar.google.com/scholar?cluster=14622696590036176289) 以获取概览，[《DDS：DPU 优化的分布式存储》](https://scholar.google.com/scholar?cluster=12305794631120951674) 了解如何将它们集成到数据库中，以及 [《Azure 加速网络：公共云中的 SmartNIC》](https://www.microsoft.com/en-us/research/uploads/prod/2018/03/Azure_SmartNIC_NSDI_2018.pdf) 了解部署细节。总体而言，我预计 SmartNIC 会将 RDMA 从简单的读写扩展到允许绕过 CPU 的通用 RPC（用于计算成本低的请求回复）。


--------

## 存储

在存储设备方面，有一些旨在降低特定用例中存储设备总拥有成本的进展。制造商巧妙地发现，可以读取比写入产生的磁化硬盘盘片的磁道宽度更小的条带，因此可以重叠磁道以达到最小宽度。于是，我们有了[叠瓦式磁记录（SMR）](https://www.storagereview.com/news/what-is-shingled-magnetic-recording-smr)硬盘驱动器，引入了将存储划分为**区域**（zones）的概念，这些区域只支持追加或擦除。SMR HDD 针对的是像[对象存储](https://dropbox.tech/infrastructure/four-years-of-smr-storage-what-we-love-and-whats-next)这样访问不频繁但需要存储大量数据的用例。

类似的想法已被应用到 SSD，**分区 SSD**（Zoned SSDs）也已出现。在 SSD 中暴露区域意味着驱动器不需要提供闪存转换层（FTL）或复杂的垃圾回收过程。与 SMR 类似，这降低了 ZNS SSD 相对于“常规”SSD 的成本，但还特别关注应用驱动的垃圾回收效率更高，从而减少总的写放大效应并延长驱动器寿命。考虑在 SSD 上的 LSM（Log-Structured Merge Trees），它们已经通过增量追加和大擦除块进行操作。移除 LSM 和 SSD 之间的 FTL，打开了优化的机会。最近，Google 和 Meta 合作提出了[灵活数据放置（FDP）](https://www.micron.com/about/blog/storage/innovations/eliminating-the-io-blender-promise-of-flexible-data-placement)的提案，它更像是对具有相关生命周期的写入进行分组的提示，而不是像 ZNS 那样严格执行分区。目标是实现更容易的升级路径，使 SSD 可以忽略写请求的 FDP 部分，仍然在语义上正确，只是性能或写放大效应更差。

> **注释**：如果你期待关于[持久内存](https://pmem.io/pmdk/libpmem/)的讨论，遗憾的是 Intel 已经终止了 [Optane](https://en.wikipedia.org/wiki/3D_XPoint)，所以目前这是一个死胡同。似乎还有一些公司，如 [Kioxia](https://americas.kioxia.com/en-ca/business/news/2021/memory-20210913-1.html) 或 [Everspin](https://investor.everspin.com/news-releases/news-release-details/everspin-technologies-unveils-persyst-simplifying-persistent) 继续在这方面努力，但我还没有听说过它们的实际应用。

其他改进并非针对成本效率，而是提高存储设备支持的功能集。特别关注 NVMe，NVMe 添加了[复制命令](https://www.snia.org/educational-library/towards-copy-offload-linux-nvme-2021)，以消除读取和写入相同数据的浪费。[融合的比较与写入命令](https://files.futurememorystorage.com/proceedings/2013/20130812_PreConfD_Marks.pdf#page=46)允许将 CAS 操作下放到驱动器本身，从而实现诸如将[乐观锁耦合](https://scholar.google.com/scholar?cluster=7804091931900436017)下放到驱动器的创新设计。NVMe 从 SCSI 继承了[数据完整性字段（DIF）](https://lwn.net/Articles/548294/)和[数据完整性扩展（DIX）](https://oss.oracle.com/~mkp/docs/dix.pdf)的支持，这使得可以将页面校验和下放到驱动器中（Oracle 就显著地使用了这一点）。还有像 [KV-SSD](https://blocksandfiles.com/2019/09/05/samsungs-potentially-groundbreaking-keyvalue-ssd/)这样的项目，将整个数据模型从按索引存储块改变为按键存储对象，甚至走向完全取代软件存储引擎。SSD 制造商持续让 SSD 具备更多的操作能力。

> **注释**：截至 2024 年 7 月 25 日，AWS 已[取消发布 S3 Select](https://aws.amazon.com/blogs/storage/how-to-optimize-querying-your-data-in-amazon-s3/)，可能是为了支持 [S3 Object Lambda](https://aws.amazon.com/s3/features/object-lambda/)。

作为 SSD 功能的倒数第二步，**SmartSSD** 正在出现，它允许在 SSD 中集成任意计算。[《在 SmartSSD 上进行查询处理：机会与挑战》](http://pages.cs.wisc.edu/~yxy/cs764-f20/papers/SmartSSD.pdf) 综述了它们在查询处理任务中的应用。将过滤器下推到存储总是有利的；我经常引用之前的工作，如利用 S3 Select 的 [PushdownDB](https://marcoserafini.github.io/assets/pdf/pushdown.pdf)，作为分析领域的优秀案例。使用 SmartSSD，我们有像 [《POLARDB 与计算存储的融合》](https://www.usenix.org/conference/fast20/presentation/cao-wei) 这样的论文。即使没有专门的集成，也有人认为，即使是透明的驱动器内压缩也能在写放大方面缩小 B+ 树和 LSM 之间的差距（[参考](https://www.usenix.org/conference/fast22/presentation/qiao)）。利用 SmartSSD 仍然是一个新兴的研究领域，但其潜在影响巨大。


--------

## 计算

### 事务处理

在最近的 VLDB 会议上，两位数据库研究领域的权威发表了一篇立场论文：[《云原生数据库系统和 Unikernels：为现代硬件重新想象操作系统抽象》](https://www.vldb.org/pvldb/vol17/p2115-leis.pdf)，主张 Unikernel 允许数据库针对其确切需求定制操作系统。早期关于 [VMCache](https://scholar.google.com/scholar?cluster=7903866005464261403) 的工作特别强调了高效数据库缓冲区管理的挑战，在这个领域，要么接受[指针变换（pointerswizzling）](https://db.in.tum.de/~leis/papers/leanstore.pdf)的复杂性，要么频繁地挂钩内核并调用 `mmap()` 相关的系统调用。

两种选择都不理想，而 Unikernel 则提供了对虚拟内存原语的直接访问。随着该领域受到更多关注，开发 Unikernel 所需的努力正在减少。[黑金章（Akira Kurogane）](https://jp.linkedin.com/in/akira-kurogane) 通过 [Unikraft](https://unikraft.org/) 以极小的代价就让 [MongoDB 作为Unikernel 运行](https://www.linkedin.com/pulse/mongodb-booted-unikernel-os-akira-kurogane-vdf7c/)，后续的帖子显示，在没有任何 MongoDB 内部更改的情况下，性能有所提升。一直以来都有一个无休止的笑话，称数据库想要成为操作系统，因为对性能改进的渴望需要对网络、文件系统、磁盘 I/O、内存等有更多的控制，而 Unikernel 数据库正好提供了这一切，使其成为可能。

为了实现超越 TLS 或磁盘加密的数据机密性，安全飞地（secure enclaves）允许执行可验证的未被篡改的代码，使所操作的数据免受被破坏的操作系统的侵害。[可信平台模块（TPM）](https://learn.microsoft.com/en-us/windows/security/hardware-security/tpm/tpm-fundamentals) 允许密钥在机器中安全保存，而安全飞地则扩展到任意的代码和数据。这使得构建对恶意攻击具有极高弹性的数据库成为可能，但对其设计有若干限制。微软已经发表了将[安全飞地集成到 Hekaton 中](https://blog.acolyer.org/2018/07/05/enclavedb-a-secure-database-using-sgx/)的研究，并已将该工作作为 [SQL Server Always Encrypted](https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-enclaves?view=sql-server-ver16) 的一部分发布。阿里巴巴也发表了他们在为担心数据机密性的企业客户构建[飞地原生存储引擎](https://vldb.org/pvldb/vol14/p1019-sun.pdf)方面的努力。数据库一直以来通过[合规监管](https://www.fortanix.com/faq/confidential-computing/how-does-confidential-computing-help-with-regulatory-compliance-requirements)这一渠道推广安全改进，安全飞地在数据机密性方面是一个有意义的进步。

自从 Spanner 引入 [TrueTime](https://sookocheff.com/post/time/truetime/) 以来，时钟同步在地理分布式数据库的事务排序中变得备受关注。每个主要的云提供商都有一个与原子钟或 GPS 卫星连接的 NTP 服务（[AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html)、[Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/time-sync#overview)、[GCP](https://developers.google.com/time/faq#whatis)）。这对任何类似的设计都非常有用，例如 CockroachDB 或 Yugabyte，它们的正确性对时钟同步至关重要，而保守的宽误差范围会降低性能。AWS 最近的 Aurora Limitless 也[使用了类似 TrueTime 的设计](https://www.youtube.com/watch?v=a9FfjuVJ9d8&t=29m25s)。这是唯一提到的特定云的、并非完全硬件的内容，因为这是主要的云供应商向用户提供昂贵的硬件（原子钟），而用户原本不会考虑自行购买。

硬件事务内存有着相当不幸的历史。[Sun 的 Rock 处理器](https://www.theregister.com/2007/08/21/sun_transactional_memory_rock/)具备硬件事务内存功能，直到 Sun 被收购并且 Rock 项目被终止。英特尔曾两次尝试发布它，但两次都不得不禁用。在将硬件事务内存应用于内存数据库的主题上有一些有趣的工作，但除了找到一些旧的 CPU 进行实验之外，我们都必须等待 CPU 制造商宣布他们计划再次尝试。

> **注释**：第一次是由于[一个错误](http://techreport.com/news/26911/errata-prompts-intel-to-disable-tsx-in-haswell-early-broadwell-cpus)，第二次是由于[一个破坏 KASLR 的侧信道攻击](https://www.blackhat.com/docs/us-16/materials/us-16-Jang-Breaking-Kernel-Address-Space-Layout-Randomization-KASLR-With-Intel-TSX-wp.pdf)。还有一个通过[误解CTF 挑战的意图](https://blog.ret2.io/2019/06/26/attacking-intel-tsx/)而发现的投机执行定时攻击。

### 查询处理

一直以来，不断有公司成立，试图利用专用硬件来加速查询处理，以实现比仅使用 CPU 的竞争对手更好的性能和成本效率。像 [Voltron](https://voltrondata.com/theseus.html)、[HEAVY.ai](https://www.heavy.ai/) 和 [Brytlyt](https://brytlyt.io/) 这样的 GPU 驱动数据库，就是朝这个方向迈出的第一步。如果英特尔或 AMD 的集成显卡在未来某个时候获得 OpenCL 支持，我不会感到太惊讶，这将为所有数据库在更广泛的硬件配置中假设一定程度的 GPU 能力打开大门。

> **注释**：OpenGL 计算着色器是使用 GPU 进行任意计算的最通用和可移植的形式，而集成显卡芯片组已经支持这些。不过，我找不到任何关于使用它们的数据库相关论文。

还有机会使用更高能效的硬件。最新的神经处理单元（NPU）和张量处理单元（TPU）已经在类似 [《TCUDB：使用张量处理器加速数据库》](https://dl.acm.org/doi/pdf/10.1145/3514221.3517869) 的工作中被证明可用于查询处理。一些公司尝试利用 FPGA。[Swarm64](https://dbdb.io/db/swarm64) 曾试图（但可能失败了）进入这个市场。AWS 自己也以 [Redshift AQUA](https://aws.amazon.com/blogs/aws/new-aqua-advanced-query-accelerator-for-amazon-redshift/) 进行了尝试。即使是最大的公司，走到 ASIC 这一步似乎也不值得，因为连 Oracle 都在 2017 年[停止了他们的 SPARC 开发](https://www.hpcwire.com/2017/09/07/oracle-layoffs-reportedly-hit-sparc-solaris-hard/)。我对 FPGA 到 ASIC 的前景并不十分乐观，因为内存带宽无论如何都会在某个时候成为主要瓶颈，但 [ADMS](https://adms-conf.org/) 是关注该领域论文的会议。

> **注释**：严格来说，ADMS 是附属于 VLDB 的一个研讨会，但我不知道泛指会议、期刊和研讨会的词是什么。


--------

## 云端可用性

最后，让我们直面这个令人沮丧的事实：如果无法获得，这些硬件进步都无关紧要。对于当今的系统，这意味着云端，而云端并未向客户提供最前沿的硬件进步。

在网络方面，情况并不理想。DPDK 是相对容易获取的最先进网络技术，因为大多数云允许某些类型的实例拥有多个网卡。AWS 以 [安全可靠数据报（SRD）](https://scholar.google.com/scholar?cluster=7115577907027624509) 的形式提供了伪 RDMA，根据[基准测试](https://scholar.google.com/scholar?cluster=9445549416525532418)，其性能大约介于 TCP 和 RDMA 之间。真正的 RDMA 仅在 Azure、GCP 和 OCI 的高性能计算实例中可用。只有阿里巴巴在通用计算实例上提供了 [RDMA](https://www.alibabacloud.com/help/en/ecs/user-guide/erdma-overview)。

> **注释**：尽管可能会有类似于 SRD 较差的延迟影响。阿里巴巴通过 iWARP 部署了 RDMA，速度可能会稍慢一些，但我还没有看到任何基准测试。

SmartNIC 在任何公开场合都不可用。这其中有充分的理由：微软发表的论文指出，[部署 RDMA 是困难的](https://scholar.google.com/scholar?cluster=12305794631120951674)。事实上，[非常困难](https://scholar.google.com/scholar?cluster=2434531805096404846)。即使是他们关于[成功使用 RDMA](https://scholar.google.com/scholar?cluster=6986943445603020796) 的论文也强调了这非常困难。距离微软开始在内部使用 RDMA 已经接近十年了，但它仍未在他们的云端提供。我无法猜测它是否或何时会出现。

在存储方面，情况并没有好多少。SMR HDD 少数几次进入消费市场时，仍以支持块存储 API 的驱动器形式出现，消费者[对此非常反感](https://arstechnica.com/gadgets/2020/04/caveat-emptor-smr-disks-are-being-submarined-into-unexpected-channels/)。ZNS SSD 似乎同样被锁定在仅限企业采购的协议背后。有人可能认为英特尔停止了 Optane 品牌的持久内存和 SSD，这意味着它们在云端不可用，但阿里巴巴仍然提供了[持久内存优化的实例](https://www.alibabacloud.com/help/en/tair/product-overview/persistent-memory-optimized-instances)。[Spare Cores](https://sparecores.com/) 的优秀团队实际上向我提供了每个云供应商的 `nvme id-ctrl` 输出，他们获取的 NVMe 设备都没有支持任何可选功能：复制、融合的比较和写入、数据完整性扩展，或多块原子写入。

> **注释**：尽管 AWS 支持[防止撕裂写入](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/storage-twp.html)，GCP 以前也有类似的文档。

阿里巴巴也是唯一一家在 SmartSSD 上进行投资的云供应商，与 ScaleFlux 合作在 PolarDB 上进行了研究。这仍然意味着 SmartSSD 对公众不可用，但即使论文也承认，这是“首次在公开文献中报道的、使用计算存储驱动器的云原生数据库的实际部署”。

在计算方面，情况终于有所改善。云完全允许 Unikernel，TPM 也广泛可用，但据我所知，只有 [AWS](https://aws.amazon.com/ec2/nitro/nitro-enclaves/) 和 [Azure](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-computing-enclaves)支持安全飞地。时间同步已可用，但没有承诺的误差范围使得无法关键依赖。（硬件事务内存不可用，但这很难责怪云供应商。）AI 的爆炸式增长意味着有足够的资金支持更高效的计算资源。GPU 在所有云中都可用。AWS[^5]、Azure、IBM 和阿里巴巴提供了 FPGA 实例。（GCP 和 OCI 没有。）不幸的现实是，只有当计算成为瓶颈时，更快的计算才有意义。GPU 和 FPGA 都受到内存限制的影响，因此无法在其本地内存中维护数据库。相反，需要依赖数据的流入和流出，这意味着受到 PCIe 速度的限制。所有这些都会鼓励在本地设备中进行周到的主板布局和总线设计，但这在云中是不可行的。

> **注释**：理想情况下，人们希望有对等 DMA 支持，能够直接从磁盘读取数据到 FPGA 中，而至少 AWS 的 F1 不支持这一点。

因此，我对下一代数据库的看法是悲观的：在新硬件进步可用之前，没人能够构建严重依赖它们的数据库，但没有云供应商愿意部署无法立即使用的硬件。下一代数据库正被这种循环依赖所束缚，因为它们尚未存在。

> **注释**：除了云供应商自己。最值得注意的是，微软和谷歌在内部已经拥有 RDMA 并在他们的数据库产品中广泛利用，同时不允许公众使用。我一直有一篇草稿文章的提纲，标题是“云供应商的 RDMA 竞争优势”。

然而，阿里巴巴的表现令人惊讶地出色。他们始终处于让所有硬件进步可用的前沿。我很惊讶在学术界和工业界中没有经常看到使用阿里巴巴进行基准测试。