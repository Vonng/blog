---
title: "自建Supabase：创业出海的首选数据库"
linkTitle: "自建Supabase其实很容易"
date: 2024-11-25
author: 冯若航
summary: >
  Supabase 非常棒，拥有你自己的 Supabase 那就是棒上加棒！本文介绍了如何在本地/云端物理机/裸金属/虚拟机上自建企业级 Supabase。
tags: [数据库, Supabase]
---



Supabase 很好，拥有属于你自己的 supabase 则好上加好。
Pigsty 可以帮助您在自己的服务器上（物理机/虚拟机/云服务器），一键自建企业级 supabase —— 更多扩展，更好性能，更深入的控制，更合算的成本。

> Pigsty 是 Supabase 官网文档上列举的三种自建部署之一：[Self-hosting: Third-Party Guides](https://supabase.com/docs/guides/self-hosting#third-party-guides)


--------

## 简短版本

[准备](https://doc.pgsty.com/zh/prepare) [Linux](https://doc.pgsty.com/zh/prepare/linux)，执行 Pigsty [标准安装](https://doc.pgsty.com/zh/install/) 流程，选择 `supabase` 配置模板，依次执行：

```bash
curl -fsSL https://repo.pigsty.io/get | bash; cd ~/pigsty
./configure -c supabase    # 使用 supabase 配置（请在 pigsty.yml 中更改凭据）
vi pigsty.yml              # 编辑域名、密码、密钥...
./install.yml              # 安装 pigsty
./docker.yml               # 安装 docker compose 组件
./app.yml                  # 使用 docker 启动 supabase 无状态部分（可能较慢）
```

安装完毕后，使用浏览器访问 `8000` 端口造访 Supa Studio，用户名 `supabase`，密码 `pigsty`。

![](https://doc.pgsty.com/img/docs/supabase-login.png)

------

## 目录

- [Supabase是什么？](#supabase是什么)
- [为什么要自建它？](#为什么要自建supabase)
- [单机自建快速上手](#单节点自建快速上手)
- [进阶主题：安全加固](#进阶主题安全加固)
- [进阶主题：域名接入](#进阶主题域名接入)
- [进阶主题：外部对象存储](#进阶主题外部对象存储)
- [进阶主题：使用SMTP](#进阶主题使用smtp)
- [进阶主题：真·高可用](#进阶主题真高可用)

------

## Supabase是什么？

[Supabase](https://supabase.com/) 是一个 BaaS （Backend as Service），开源的 Firebase，是 AI Agent 时代最火爆的数据库 + 后端解决方案。
Supabase 对 PostgreSQL 进行了封装，并提供了身份认证，消息传递，边缘函数，对象存储，并基于 PG 数据库模式自动生成 REST API 与 GraphQL API。

Supabase 旨在为开发者提供一条龙式的后端解决方案，减少开发和维护后端基础设施的复杂性。
它能让开发者告别绝大部分后端开发的工作，**只需要懂数据库设计与前端即可快速出活！**
开发者只要用 Vibe Coding 糊个前端与数据库模式设计，就可以快速完成一个完整的应用。

目前，Supabase 是 [PostgreSQL 开源生态](https://ossrank.com/cat/368-postgresql-ecosystem) 中人气最高的开源项目，在 GitHub 上已有 [八万](https://github.com/supabase/supabase/) Star。
Supabase 还为小微创业者提供了“慷慨”的免费云服务额度 —— 免费的 500 MB 空间，对于存个用户表，浏览数之类的东西绰绰有余。

------

## 为什么要自建？

既然 Supabase 云服务这么香，为什么要自建呢？

最直观的原因是是我们在《[云数据库是智商税吗？](https://blog.vonng.com/cloud/rds/)》中提到过的：当你的数据/计算规模超出云计算适用光谱（Supabase：4C/8G/500MB免费存储），成本很容易出现爆炸式增长。
而且在当下，足够可靠的 [本地企业级 NVMe SSD](https://blog.vonng.com/cloud/bonus/) 在性价比上与 [云端存储](https://blog.vonng.com/cloud/ebs/) 有着三到四个数量级的优势，而自建能更好地利用这一点。

另一个重要的原因是 **功能**， Supabase 云服务的功能受限 —— 很多强力PG扩展因为多租户安全挑战与许可证的原因无法以云服务的形式。
故而尽管 [扩展是 PostgreSQL 的核心特色](https://blog.vonng.com/pg/pg-eat-db-world)，在 Supabase 云服务上也依然只有 **64** 个扩展可用。
而通过 Pigsty 自建的 Supabase 则提供了多达 [**440**](https://pgext.cloud/zh/list) 个开箱即用的 PG 扩展。

此外，自主可控与规避供应商锁定也是自建的重要原因 —— 尽管 Supabase 虽然旨在提供一个无供应商锁定的 Google Firebase 开源替代，但实际上自建高标准企业级的 Supabase 门槛并不低。
Supabase 内置了一系列由他们自己开发维护的 PG 扩展插件，并计划将原生的 PostgreSQL 内核替换为收购的 [OrioleDB](https://doc.pgsty.com/zh/pgsql/kernel/orioledb)，而这些内核与扩展在 PGDG 官方仓库中并没有提供。

这实际上是某种隐性的供应商锁定，阻止了用户使用除了 supabase/postgres Docker 镜像之外的方式自建，Pigsty 则提供开源，透明，通用的方案解决这个问题。
我们将所有 Supabase 自研与用到的 10 个缺失的扩展打成开箱即用的 RPM/DEB 包，确保它们在所有 [主流Linux操作系统发行版](https://doc.pgsty.com/zh/prepare/linux) 上都可用：

| 扩展                                                        | 说明                                                     |
|-----------------------------------------------------------|--------------------------------------------------------|
| [`pg_graphql`](https://pgext.cloud/e/pg_graphql/)       | 提供PG内的GraphQL支持 (RUST)，Rust扩展，由PIGSTY提供                |
| [`pg_jsonschema`](https://pgext.cloud/e/pg_jsonschema/) | 提供JSON Schema校验能力，Rust扩展，由PIGSTY提供                     |
| [`wrappers`](https://pgext.cloud/e/wrappers/)           | Supabase提供的外部数据源包装器捆绑包,，Rust扩展，由PIGSTY提供               |
| [`index_advisor`](https://pgext.cloud/e/index_advisor/) | 查询索引建议器，SQL扩展，由PIGSTY提供                                |
| [`pg_net`](https://pgext.cloud/e/pg_net/)               | 用 SQL 进行异步非阻塞HTTP/HTTPS 请求的扩展 (supabase)，C扩展，由PIGSTY提供 |
| [`vault`](https://pgext.cloud/e/supabase_vault/)        | 在 Vault 中存储加密凭证的扩展 (supabase)，C扩展，由PIGSTY提供            |
| [`pgjwt`](https://pgext.cloud/e/pgjwt/)                 | JSON Web Token API 的PG实现 (supabase)，SQL扩展，由PIGSTY提供    |
| [`pgsodium`](https://pgext.cloud/e/pgsodium/)           | 表数据加密存储 TDE，扩展，由PIGSTY提供                               |
| [`supautils`](https://pgext.cloud/e/supautils/)         | 用于在云环境中确保数据库集群的安全，C扩展，由PIGSTY提供                        |
| [`pg_plan_filter`](https://pgext.cloud/e/plan_filter/)  | 使用执行计划代价过滤阻止特定查询语句，C扩展，由PIGSTY提供                       |

同时，我们在 Supabase 自建部署中默认 [安装](https://doc.pgsty.com/zh/pgsql/extension/install)绝大多数扩展，您可以参考可用扩展列表按需 [启用](https://doc.pgsty.com/zh/pgsql/extension/create)。

同时，Pigsty 还会负责好底层 [高可用](https://doc.pgsty.com/feat/ha/) [PostgreSQL](https://doc.pgsty.com/zh/pgsql/) 数据库集群，高可用 [MinIO](https://doc.pgsty.com/zh/minio/) 对象存储集群的自动搭建，甚至是 [Docker](https://doc.pgsty.com/zh/docker/) 容器底座的部署与 [Nginx](https://doc.pgsty.com/admin/portal) 反向代理，[域名配置](https://doc.pgsty.com/zh/admin/domain) 与 [HTTPS证书签发](https://doc.pgsty.com/zh/admin/cert)。 您可以使用 Docker Compose 拉起任意数量的无状态 Supabase 容器集群，并将状态存储在外部 Pigsty 自托管数据库服务中。

在这一自建部署架构中，您获得了使用不同内核的自由（PG 15-17，OrioleDB），加装 [**440**](https://pgext.cloud/list/) 个扩展的自由，扩容与伸缩 Supabase / Postgres / MinIO 的自由，
免于数据库运维杂务的自由，以及免于供应商锁定，本地运行到地老天荒的自由。 而相比于使用云服务需要付出的代价，不过是准备服务器和多敲几行命令而已。


------

## 单节点自建快速上手

让我们先从单节点 Supabase 部署开始，我们会在后面进一步介绍多节点高可用部署的方法。

[准备](https://doc.pgsty.com/zh/prepare) 一台全新 [Linux 服务器](https://doc.pgsty.com/zh/prepare/linux)，使用 Pigsty 提供的 [`supabase`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml) 配置模板执行 [标准安装](https://doc.pgsty.com/zh/install/start)，
然后额外运行 [`docker.yml`](https://doc.pgsty.com/zh/docker/playbook#dockeryml) 与 [`app.yml`](https://doc.pgsty.com/zh/app/playbook) 拉起无状态部分的 Supabase 容器即可（默认端口 `8000`/`8433`）。

```bash
curl -fsSL https://repo.pigsty.io/get | bash; cd ~/pigsty
./configure -c supabase    # 使用 supabase 配置（请在 pigsty.yml 中更改凭据）
vi pigsty.yml              # 编辑域名、密码、密钥...
./install.yml              # 安装 pigsty
./docker.yml               # 安装 docker compose 组件
./app.yml                  # 使用 docker 启动 supabase 无状态部分
```

在部署 Supabase 前请根据实际情况修改自动生成的 `pigsty.yml` 配置文件中的参数（域名与密码）
如果只是本地开发测试，可以先跳过，我们将在后面介绍如何通过修改配置文件来进一步定制。

[![asciicast](https://doc.pgsty.com/img/asciinema/supabase.svg)](https://asciinema.org/a/731206)

如果配置无误，大约十分钟后，就可以在本地网络通过 `http://<your_ip_address>:8000` 访问到 Supabase Studio 图形管理界面了。
默认的用户名与密码分别是： `supabase` 与 `pigsty`。

![](https://doc.pgsty.com/img/docs/supabase-home.png)

<Callout title="中国大陆地区 DockerHub 被墙" type="warning">

    在中国大陆地区，Pigsty 默认使用 1Panel 与 1ms 提供的 DockerHub 镜像站点下载 Supabase 相关镜像，可能会较慢。
    你也可以自行配置 [代理](https://doc.pgsty.com/zh/docker/config#proxy) 与 [镜像站](https://doc.pgsty.com/zh/docker/config#registry) ，`cd /opt/supabase; docker compose pull` 手动拉取镜像。
    我们亦提供包含完整离线安装方案的 [Supabase 自建专家咨询服务](https://doc.pgsty.com/zh/service)。

</Callout>

<Callout title="使用 Supabase 的对象存储需要HTTPS/域名" type="warning">

    如果你需要使用的对象存储功能，那么需要通过域名与 HTTPS 访问 Supabase，否则会出现报错。

</Callout>


<Callout title="生产部署请务必修改密码！" type="warning">

    对于严肃的生产部署，请 **务必** 修改所有默认密码！

</Callout>




------

## 自建关键技术决策

以下是一些自建 Supabase 会涉及到的关键技术决策，供您参考：

使用默认的**单节点部署** Supabase 无法享受到 PostgreSQL / MinIO 的高可用能力。
尽管如此，单节点部署相比官方纯 Docker Compose 方案依然要有显著优势： 例如开箱即用的监控系统，自由安装扩展的能力，各个组件的扩缩容能力，以及提供兜底数据库时间点恢复能力等。

如果您只有一台服务器，或者选择在云服务器上自建，Pigsty 建议您使用外部的 S3 替代本地的 MinIO 作为对象存储，存放 PostgreSQL 的备份，并承载 Supabase Storage 服务。
这样的部署在故障时可以在单机部署条件下，提供一个兜底级别的 RTO （小时级恢复时长）/ RPO （MB级数据损失）容灾水平。

在严肃的生产部署中，Pigsty 建议使用至少3～4个节点的部署策略，确保 MinIO 与 PostgreSQL 都使用满足企业级高可用要求的多节点部署。 在这种情况下，您需要相应准备更多节点与磁盘，并相应调整 `pigsty.yml` 配置清单中的集群配置，以及 supabase 集群配置中的接入信息，使用高可用接入点访问服务。

Supabase 的部分功能需要发送邮件，所以要用到 SMTP 服务。除非单纯用于内网，否则对于严肃的生产部署，建议使用 SMTP 云服务。自建的邮件服务器发送的邮件容易被标记为垃圾邮件导致拒收。

如果您的服务直接向公网暴露，我们强烈建议您使用真正的域名与 HTTPS 证书，并通过 [Nginx 门户](https://doc.pgsty.com/zh/admin/portal) 访问。

接下来，我们会依次讨论一些进阶主题。如何在单节点部署的基础上，进一步提升 Supabase 的安全性、可用性与性能。


------

## 进阶主题：安全加固

**Pigsty基础组件**

对于严肃的生产部署，我们强烈建议您修改 [Pigsty 基础组件的密码](https://doc.pgsty.com/zh/config/security#passwords)。因为这些默认值是公开且众所周知的，不改密码上生产无异于裸奔：

- [`grafana_admin_password`](https://doc.pgsty.com/infra/param/#grafana_admin_password): `pigsty`，Grafana管理员密码
- [`pg_admin_password`](https://doc.pgsty.com/pgsql/param/#pg_admin_password): `DBUser.DBA`，PG超级用户密码
- [`pg_monitor_password`](https://doc.pgsty.com/pgsql/param/#pg_monitor_password): `DBUser.Monitor`，PG监控用户密码
- [`pg_replication_password`](https://doc.pgsty.com/pgsql/param/#pg_replication_password): `DBUser.Replicator`，PG复制用户密码
- [`patroni_password`](https://doc.pgsty.com/pgsql/param/#patroni_password): `Patroni.API`，Patroni 高可用组件密码
- [`haproxy_admin_password`](https://doc.pgsty.com/node/param/#haproxy_admin_password): `pigsty`，负载均衡器管控密码
- [`minio_secret_key`](https://doc.pgsty.com/minio/param/#minio_secret_key): `minioadmin`，MinIO 根用户密钥
- 此外，强烈建议您修改 Supabase 使用的 [PostgreSQL 业务用户](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L68) 密码，默认为 `DBUser.Supa`

以上密码为 Pigsty 组件模块的密码，强烈建议在安装部署前就设置完毕。

**Supabase密钥**

除了 Pigsty 组件的密码，你还需要 [修改 Supabase 的密钥](https://supabase.com/docs/guides/self-hosting/docker#securing-your-services)，包括

- [`JWT_SECRET`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#130)
- [`ANON_KEY`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L131)
- [`SERVICE_ROLE_KEY`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L132)
- [`DASHBOARD_USERNAME`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L133) Supabase Studio Web 界面的默认用户名，默认为 `supabase`
- [`DASHBOARD_PASSWORD`](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L134) Supabase Studio Web 界面的默认密码，默认为 `pigsty`

这里请您务必参照 [Supabase教程：保护你的服务](https://supabase.com/docs/guides/self-hosting/docker#generate-api-keys) 里的说明：

- 生成一个长度超过 40 个字符的 `JWT_SECRET`，并使用教程中的工具签发 `ANON_KEY` 与 `SERVICE_ROLE_KEY` 两个 JWT。
- 使用教程中提供的工具，根据 `JWT_SECRET` 以及过期时间等属性，生成一个 `ANON_KEY` JWT，这是匿名用户的身份凭据。
- 使用教程中提供的工具，根据 `JWT_SECRET` 以及过期时间等属性，生成一个 `SERVICE_ROLE_KEY`，这是权限更高服务角色的身份凭据。
- 如果您使用的 PostgreSQL 业务用户使用了不同于默认值的密码，请相应修改 [`POSTGRES_PASSWORD``](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L144) 的值
- 如果您的对象存储使用了不同于默认值的密码，请相应修改 [`S3_ACCESS_KEY``](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L154) 与 [`S3_SECRET_KEY``](https://github.com/pgsty/pigsty/blob/main/conf/supabase.yml#L155) 的值

Supabase 部分的凭据修改后，您可以重启 Docker Compose 容器以应用新的配置：

```bash tab="剧本"
./app.yml -t app_config,app_launch
```
```bash tab="手工"
cd /opt/supabase; make up
```


------

## 进阶主题：域名接入

如果你在本机或局域网内使用 Supabase，那么可以选择 IP:Port 直连 Kong 对外暴露的 HTTP 8000 端口访问 Supabase。

你可以使用一个内网静态解析的域名，但对于严肃的生产部署，我们建议您使用真域名 + HTTPS 来访问 Supabase。
在这种情况下，您的服务器应当有一个公网 IP 地址，你应当拥有一个域名，使用云/DNS/CDN 供应商提供的 DNS 解析服务，将其指向安装节点的公网 IP（可选默认下位替代：本地 `/etc/hosts` 静态解析）。

比较简单的做法是，直接批量替换占位域名（`supa.pigsty`）为你的实际域名，假设为 `supa.pigsty.cc`：

```bash
sed -ie 's/supa.pigsty.cc/supa.pigsty/g/' ~/pigsty/pigsty.yml
```

如果你没有事先配置好，那么重载 Nginx 和 Supabase 的配置生效即可：

```bash
make nginx      # 重载 nginx 配置
make cert       # 申请 certbot 免费 HTTPS 证书
./app.yml       # 重载 Supabase 配置
```

修改后的配置应当类似下面的片段：

```yaml
all:
  vars:
    infra_portal:
      supa :
        domain: supa.pigsty.cc        # 替换为你的域名！
        endpoint: "10.10.10.10:8000"
        websocket: true
        certbot: supa.pigsty.cc       # 证书名称，通常与域名一致即可

  children:
    supabase:
      vars:
          supabase:                                       # the definition of supabase app
            conf:                                         # override /opt/supabase/.env
              SITE_URL: https://supa.pigsty                # <------- Change This to your external domain name
              API_EXTERNAL_URL: https://supa.pigsty        # <------- Otherwise the storage api may not work!
              SUPABASE_PUBLIC_URL: https://supa.pigsty     # <------- DO NOT FORGET TO PUT IT IN infra_portal!
```

完整的域名/HTTPS 配置可以参考 [证书管理](https://doc.pgsty.com/zh/admin/cert) 教程，您也可以使用 Pigsty 自带的本地静态解析与自签发 HTTPS 证书作为下位替代。

[![asciicast](https://doc.pgsty.com/img/asciinema/supa-domain.svg)](https://asciinema.org/a/731211)



------

## 进阶主题：外部对象存储

您可以使用 S3 或 S3 兼容的服务，来作为 PGSQL 备份与 Supabase 使用的对象存储。这里我们使用一个 阿里云 OSS 对象存储作为例子。

> Pigsty 提供了一个 [`terraform/spec/aliyun-meta-s3.tf`](https://github.com/pgsty/pigsty/blob/main/terraform/spec/aliyun-meta-s3.tf) 模板，
> 可以用于在阿里云上拉起一台服务器，以及一个 OSS 存储桶。

首先，我们修改 `all.children.supa.vars.apps.[supabase].conf` 中 S3 相关的配置，将其指向阿里云 OSS 存储桶：

```yaml
# if using s3/minio as file storage
S3_BUCKET: data                       # 替换为 S3 兼容服务的连接信息
S3_ENDPOINT: https://sss.pigsty:9000  # 替换为 S3 兼容服务的连接信息
S3_ACCESS_KEY: s3user_data            # 替换为 S3 兼容服务的连接信息
S3_SECRET_KEY: S3User.Data            # 替换为 S3 兼容服务的连接信息
S3_FORCE_PATH_STYLE: true             # 替换为 S3 兼容服务的连接信息
S3_REGION: stub                       # 替换为 S3 兼容服务的连接信息
S3_PROTOCOL: https                    # 替换为 S3 兼容服务的连接信息
```

同样使用以下命令重载 Supabase 配置：

```bash
./app.yml -t app_config,app_launch
```

您同样可以使用 S3 作为 PostgreSQL 的备份仓库，在 `all.vars.pgbackrest_repo` 新增一个 `aliyun` 备份仓库的定义：

```yaml
all:
  vars:
    pgbackrest_method: aliyun          # pgbackrest 备份方法：local,minio,[其他用户定义的仓库...]，本例中将备份存储到 MinIO 上
    pgbackrest_repo:                   # pgbackrest 备份仓库: https://pgbackrest.org/configuration.html#section-repository
      aliyun:                          # 定义一个新的备份仓库 aliyun
        type: s3                       # 阿里云 oss 是 s3-兼容的对象存储
        s3_endpoint: oss-cn-beijing-internal.aliyuncs.com
        s3_region: oss-cn-beijing
        s3_bucket: pigsty-oss
        s3_key: xxxxxxxxxxxxxx
        s3_key_secret: xxxxxxxx
        s3_uri_style: host
        path: /pgbackrest
        bundle: y                         # bundle small files into a single file
        bundle_limit: 20MiB               # Limit for file bundles, 20MiB for object storage
        bundle_size: 128MiB               # Target size for file bundles, 128MiB for object storage
        cipher_type: aes-256-cbc          # enable AES encryption for remote backup repo
        cipher_pass: pgBackRest.MyPass    # 设置一个加密密码，pgBackRest 备份仓库的加密密码
        retention_full_type: time         # retention full backup by time on minio repo
        retention_full: 14                # keep full backup for the last 14 days
```

然后在 `all.vars.pgbackrest_mehod` 中指定使用 `aliyun` 备份仓库，重置 pgBackrest 备份：

```bash
./pgsql.yml -t pgbackrest
```

Pigsty 会将备份仓库切换到外部对象存储上，更多备份配置可以参考 [PostgreSQL 备份](https://doc.pgsty.com/zh/pgsql/backup) 文档。



------

## 进阶主题：使用SMTP

你可以使用 SMTP 来发送邮件，修改 supabase 应用配置，添加 SMTP 信息：

```yaml
all:
  children:
    supabase:        # supa group
      vars:          # supa group vars
        apps:        # supa group app list
          supabase:  # the supabase app
            conf:    # the supabase app conf entries
              SMTP_HOST: smtpdm.aliyun.com:80
              SMTP_PORT: 80
              SMTP_USER: no_reply@mail.your.domain.com
              SMTP_PASS: your_email_user_password
              SMTP_SENDER_NAME: MySupabase
              SMTP_ADMIN_EMAIL: adminxxx@mail.your.domain.com
              ENABLE_ANONYMOUS_USERS: false
```

不要忘了使用 `app.yml` 来重载配置


------

## 进阶主题：真·高可用

经过这些配置，您拥有了一个带公网域名，HTTPS 证书，SMTP，PITR 备份，监控，IaC，以及 400+ 扩展的企业级 Supabase （基础单机版）。
高可用的配置请参考 Pigsty 其他部份的文档，如果您懒得阅读学习，我们提供手把手扶上马的 Supabase 自建专家咨询服务 —— ¥2000 元免去折腾与下载的烦恼。

单节点的 RTO / RPO 依赖外部对象存储服务提供兜底，如果您的这个节点挂了，外部 S3 存储中保留了备份，您可以在新的节点上重新部署 Supabase，然后从备份中恢复。
这样的部署在故障时可以提供一个最低标准的 RTO （小时级恢复时长）/ RPO （MB级数据损失）[兜底容灾水平](https://doc.pgsty.com/zh/pgsql/backup) 兜底。

如果想要达到 RTO < 30s ，切换零数据丢失，那么需要使用[多节点](https://doc.pgsty.com/zh/install/multinode)进行高可用部署，这涉及到：

- [ETCD](https://doc.pgsty.com/zh/etcd/)： DCS 需要使用三个节点或以上，才能容忍一个节点的故障。
- [PGSQL](https://doc.pgsty.com/zh/pgsql/)： PGSQL 同步提交不丢数据模式，建议使用至少三个节点。
- [INFRA](https://doc.pgsty.com/zh/infra/)：监控基础设施故障影响稍小，建议生产环境使用双副本
- Supabase 无状态容器本身也可以是多节点的副本，可以实现高可用。

在这种情况下，您还需要修改 PostgreSQL 与 MinIO 的接入点，使用 DNS / L2 VIP / HAProxy 等 [高可用接入点](https://doc.pgsty.com/zh/pgsql/service#access)
关于这些部分，您只需参考 Pigsty 中各个模块的文档进行配置部署即可。
建议您参考 [`conf/ha/trio.yml`](https://github.com/pgsty/pigsty/blob/main/conf/ha/trio.yml) 与 [`conf/ha/safe.yml`](https://github.com/pgsty/pigsty/blob/main/conf/ha/trio.yml) 中的配置，将集群规模升级到三节点或以上。


