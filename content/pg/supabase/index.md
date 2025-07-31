---
title: 自建Supabase：创业出海的首选数据库
linkTitle: "自建Supabase其实很容易"
date: 2024-11-25
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）
summary: Supabase 非常棒，拥有你自己的 Supabase 那就是棒上加棒！本文介绍了如何在本地/云端物理机/裸金属/虚拟机上自建企业级 Supabase。
tags: [数据库,Supabase]
---


Supabase 非常棒，拥有你自己的 Supabase 那就是棒上加棒！
本文介绍了如何在本地/云端物理机/裸金属/虚拟机上自建企业级 Supabase。

--------

## 目录

- [Supabase是什么？](#supabase是什么)
- [为什么要自建它？](#为什么要自建supabase)
- [单机自建快速上手](#单节点自建快速上手) 
- [进阶主题：安全加固](#进阶主题安全加固)
- [进阶主题：域名接入](#进阶主题域名接入)
- [进阶主题：外部对象存储](#进阶主题外部对象存储)
- [进阶主题：使用SMTP](#进阶主题使用smtp)
- [进阶主题：真·高可用](#进阶主题真高可用)


-------

## Supabase是什么？

[Supabase](https://supabase.com/) 是一个开源的 Firebase，是一个 BaaS （Backend as Service）。
Supabase 对 PostgreSQL 进行了封装，并提供了身份认证，消息传递，边缘函数，对象存储，以及基于 PG 数据库模式自动生成的 REST API 与 GraphQL API。

Supabase 旨在为开发者提供一站式的后端解决方案，减少开发和维护后端基础设施的复杂性，使开发者专注于前端开发和用户体验。
用大白话来说就是：让开发者告别绝大部分后端开发的工作，只需要懂数据库设计与前端即可快速出活！

目前，Supabase 是 PostgreSQL 生态人气最高的开源项目，在 GitHub 上已经有高达7万4千的Star数。
并且和 Neon，Cloudflare 一起并称为赛博菩萨 —— 因为他们都提供了非常不错的云服务免费计划。
目前，Supabase 和 Neon 已经成为许多初创企业的首选数据库 —— 用起来非常方便，起步还是免费的。


-------

## 为什么要自建Supabase？

小微规模（4c8g）内的 Supabase 云服务[极富性价比](https://supabase.com/pricing)，人称赛博菩萨。那么 Supabase 云服务这么香，为什么要自建呢？

最直观的原因是是我们在《[云数据库是智商税吗？](/zh/blog/cloud/rds)》中提到过的：当你的规模超出云计算适用光谱，成本很容易出现爆炸式增长。
而且在当下，足够可靠的[本地企业级 NVMe SSD](/zh/blog/cloud/hardware-bonus)在性价比上与云端存储有着三到四个数量级的优势，而自建能更好地利用这一点。

另一个重要的原因是功能， Supabase 云服务的功能受限 —— [出于与RDS相同的逻辑](https://mp.weixin.qq.com/s/EH7RPB6ImfMHXhOMU7P5Qg)，
很多 [**强力PG扩展**](https://ext.pigsty.io/#/list) 因为多租户安全挑战与许可证的原因无法作为云服务提供。
故而尽管PG扩展是 Supabase 的一个核心特色，在云服务上也依然只有 64 个可用扩展，而 Pigsty 提供了多达 [**390**](https://ext.pigsty.io/#/list) 个开箱即用的 PG 扩展。

此外，尽管 Supabase 虽然旨在提供一个无供应商锁定的 Google Firebase 开源替代，但实际上自建高标准企业级的 Supabase 门槛并不低：
Supabase 内置了一系列由他们自己开发维护的 PG 扩展插件，而这些扩展在 PGDG 官方仓库中并没有提供。
这实际上是某种隐性的供应商锁定，阻止了用户使用除了 supabase/postgres Docker 镜像之外的方式自建。

Pigsty 解决了这些问题，我们将所有 Supabase 自研与用到的 10 个缺失的扩展打成开箱即用的 RPM/DEB 包，确保它们在所有[主流Linux操作系统发行版](/zh/docs/reference/compatibility)上都可用：

- [pg_graphql](https://ext.pigsty.io/#/pg_graphql)：提供PG内的GraphQL支持 (RUST)，Rust扩展，由PIGSTY提供
- [pg_jsonschema](https://ext.pigsty.io/#/pg_jsonschema)：提供JSON Schema校验能力，Rust扩展，由PIGSTY提供
- [wrappers](https://ext.pigsty.io/#/wrappers)：Supabase提供的外部数据源包装器捆绑包,，Rust扩展，由PIGSTY提供
- [index_advisor](https://ext.pigsty.io/#/index_advisor)：查询索引建议器，SQL扩展，由PIGSTY提供
- [pg_net](https://ext.pigsty.io/#/pg_net)：用 SQL 进行异步非阻塞HTTP/HTTPS 请求的扩展 (supabase)，C扩展，由PIGSTY提供
- [vault](https://ext.pigsty.io/#/vault)：在 Vault 中存储加密凭证的扩展 (supabase)，C扩展，由PIGSTY提供
- [pgjwt](https://ext.pigsty.io/#/pgjwt)：JSON Web Token API 的PG实现 (supabase)，SQL扩展，由PIGSTY提供
- [pgsodium](https://ext.pigsty.io/#/pgsodium)：表数据加密存储 TDE，扩展，由PIGSTY提供
- [supautils](https://ext.pigsty.io/#/supautils)：用于在云环境中确保数据库集群的安全，C扩展，由PIGSTY提供
- [pg_plan_filter](https://ext.pigsty.io/#/plan_filter)：使用执行计划代价过滤阻止特定查询语句，C扩展，由PIGSTY提供

我们还在 Supabase 中默认安装了以下扩展，您可以参考可用扩展列表启用更多。

```bash
- timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
- supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
- pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
```

同时，Pigsty 还会负责好底层[高可用](/zh/docs/concept/ha) [PostgreSQL](/zh/docs/pgsql) 数据库集群，高可用 [MinIO](/zh/docs/minio) 对象存储集群的自动搭建，甚至是 [Docker](/zh/docs/docker) 容器底座的部署。
最终，您可以使用 Docker Compose 拉起任意数量的无状态 Supabase 容器集群，并使用外部由 Pigsty 托管的企业级 PostgreSQL 数据库与 MinIO 对象存储，甚至连反向代理的 Nginx 等都已经为您配置准备完毕！

在这一自建部署架构中，您获得了使用不同内核的自由（PG 12-17），加装390个扩展的自由，扩容与伸缩Supabase/Postgres/MinIO的自由，免于数据库运维的自由，以及告别供应商锁定的自由。
而相比于使用 Supabase 云服务需要付出的代价，不过是准备一（几）台物理机/虚拟机 + 敲几行命令，等候十几分钟的区别。



--------

## 单节点自建快速上手

让我们先从单节点 Supabase 部署开始，我们会在后面进一步介绍多节点高可用部署的方法。

首先，使用 Pigsty [标准安装流程](/zh/docs/setup/install) 安装 Supabase 所需的 MinIO 与 PostgreSQL 实例；
然后额外运行 [`supabase.yml`](https://github.com/Vonng/pigsty/blob/main/supabase.yml) 完成剩余的工作，
拉起无状态部分的 Supabase 容器，Supabase 就可以使用了（默认端口 `8000`/`8433`）。

```bash
 curl -fsSL https://repo.pigsty.io/get | bash
./bootstrap          # 环境检查，自动安装依赖：Ansible
./configure -c supa  # 重要：请在配置文件中修改密码等关键信息！
./install.yml        # 安装 Pigsty，拉起 PGSQL 与 MINIO！
./supabase.yml       # 安装 Docker 并拉起 Supabase 无状态部分！
```

请在部署 Supabase 前，根据您的实际情况，修改自动生成的 `pigsty.yml` 配置文件中的参数（主要是密码！）
如果您只是将其用于本地开发测试，可以先不管这些，我们将在后面介绍如何通过修改配置文件来定制您的 Supabase。

如果您的配置没有问题，那么大约在 10 分钟后，您就可以在本地网络通过 `http://<your_ip_address>:8000` 访问到 Supabase Studio 管理界面了。

[![asciicast](https://asciinema.org/a/692194.svg)](https://asciinema.org/a/692194)


--------

## 检查清单

- [x] 硬件/软件：[准备所需的机器资源](/zh/docs/setup/prepare/)：Linux x86_64 服务器一台，全新安装[主流 Linux 操作系统](/zh/docs/reference/compatibility)
- [x] 网络/权限：有 [ssh](/zh/docs/setup/prepar/#管理用户准备) 免密登陆权限，所用用户有[免密 sudo 权限](/zh/docs/setup/prepare/#管理用户准备)
- [x] 确保机器有内网静态IPv4网络地址，并可以访问互联网。中国地区 DockerHub 需要翻墙，需要有可用的代理或镜像站点
  - [x] 在 `configure` 过程中，请输入节点的内网首要 IP 地址，或直接通过 `-i <primary_ip>` 命令行参数指定
  - [x] 如果您的网络环境无法访问 DockerHub，请指定 [`docker_registry_mirrors`](/zh/docs/docker/param#docker_registry_mirrors) 使用镜像站 或 [`proxy_env`](/zh/docs/reference/param#proxy_env) 参数翻墙。 
- 确保使用了 [`supa`](/zh/docs/conf/supa) 配置模板，并按需修改了参数
  - [x] 您是否修改了所有[与密码有关的配置参数](/zh/docs/setup/security#密码)？【可选】
  - [x] 您是否需要使用外部 SMTP 服务器？是否配置了 `supa_config` 中的 SMTP 参数？【可选】

> 中国地区的用户请注意，如果您没有配置好 Docker 镜像站点或代理服务器，那么会有极大概率会翻车在 ./supabase 最后一步的镜像拉取上。我们建议您掌握科学上网技巧，参考 [Docker 模块 FAQ](/zh/docs/docker/faq/) 的说明配置镜像或代理。
> 请注意，我们提供 [Supabase 自建专门咨询服务](/zh/docs/about/service)，¥2000 / 例·半小时，购买附赠预制离线安装包，可以无需互联网（自然也无需翻墙）安装，将您的企业级自建 Supabase 安稳扶上马！

> 离线软件包使用说明：请在执行安装前，将收到的 `pkg.tgz` 放置于 `/tmp/pkg.tgz`，将 `supabase` 目录整个放置在 `/tmp/supabase` 即可。 

修改后的配置文件，应该如下所示：

<details><summary>对默认生成的配置文件进行修改</summary>

```yaml
all:
  children:

    # infra 集群，包含 Prometheus & Grafana 监控基础设施
    infra: { hosts: { 10.10.10.10: { infra_seq: 1 } } }

    # etcd 集群，本例为单节点 Etcd，用于提供 PG 高可用
    etcd: { hosts: { 10.10.10.10: { etcd_seq: 1 } }, vars: { etcd_cluster: etcd } }

    # minio 集群，单节点 SNSD 的 S3 兼容对象存储
    minio: { hosts: { 10.10.10.10: { minio_seq: 1 } }, vars: { minio_cluster: minio } }

    # pg-meta， Supabase 底层实际的 PostgreSQL 数据库
    pg-meta:
      hosts: { 10.10.10.10: { pg_seq: 1, pg_role: primary } }
      vars:
        pg_cluster: pg-meta
        pg_users:
          # supabase 使用的角色
          - { name: anon           ,login: false }
          - { name: authenticated  ,login: false }
          - { name: dashboard_user ,login: false ,replication: true ,createdb: true ,createrole: true }
          - { name: service_role   ,login: false ,bypassrls: true }
          
          # 【注意】如果你要修改 Supabase 业务用户的密码，请在这里统一修改所有用户的密码
          - { name: supabase_admin             ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: true   ,roles: [ dbrole_admin ] ,superuser: true ,replication: true ,createdb: true ,createrole: true ,bypassrls: true }
          - { name: authenticator              ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] }
          - { name: supabase_auth_admin        ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_storage_admin     ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] ,createrole: true }
          - { name: supabase_functions_admin   ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_replication_admin ,password: 'DBUser.Supa' ,replication: true ,roles: [ dbrole_admin ]}
          - { name: supabase_read_only_user    ,password: 'DBUser.Supa' ,bypassrls: true ,roles: [ dbrole_readonly, pg_read_all_data ] }

        # 【注意】 这里定义了 Supabase 使用的底层 Postgres 业务数据库，
        pg_databases:
          - name: postgres
            baseline: supabase.sql  # 这里的 files/supabase.sql 文件包含了初始化 Supabase 所必需的模式迁移脚本，非常重要！
            owner: supabase_admin   # 这里的数据库所有者，必须是上面定义的 supabase_admin，我们建议使用此用户进行模式变更。
            comment: supabase postgres database
            schemas: [ extensions ,auth ,realtime ,storage ,graphql_public ,supabase_functions ,_analytics ,_realtime ]
            extensions:             # 定义在这里的扩展会默认在数据库中 “创建并启用”
              - { name: pgcrypto  ,schema: extensions  } # 1.3  
              - { name: pg_net    ,schema: extensions  } # 0.9.2
              - { name: pgjwt     ,schema: extensions  } # 0.2.0
              - { name: uuid-ossp ,schema: extensions  } # 1.1  
              - { name: pgsodium        }                # 3.1.9
              - { name: supabase_vault  }                # 0.2.8
              - { name: pg_graphql      }                # 1.5.9
              - { name: pg_jsonschema   }                # 0.3.3
              - { name: wrappers        }                # 0.4.3
              - { name: http            }                # 1.6  
              - { name: pg_cron         }                # 1.6  
              - { name: timescaledb     }                # 2.17 
              - { name: pg_tle          }                # 1.2  
              - { name: vector          }                # 0.8.0
        
        # 这些扩展默认需要动态加载
        pg_libs: 'pg_stat_statements, plpgsql, plpgsql_check, pg_cron, pg_net, timescaledb, auto_explain, pg_tle, plan_filter'
        
        # 如果你想安装其他扩展插件，请在这里指定，但请同样添加到下面的 repo_packages 中。
        pg_extensions:               # 在这里定义 “安装” 的扩展集合，安装后您可以按需手工 “启用/创建”
          - supabase                 # Supabase 所必需的关键扩展集合，其他扩展为可选
          - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
          - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
          - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
        pg_parameters:
          cron.database_name: postgres
          pgsodium.enable_event_trigger: off
        pg_hba_rules:                 # 额外的 HBA 规则，允许 Supabase 从容器网段访问
          - { user: all ,db: postgres  ,addr: intra         ,auth: pwd ,title: 'allow supabase access from intranet'    }
          - { user: all ,db: postgres  ,addr: 172.17.0.0/16 ,auth: pwd ,title: 'allow access from local docker network' }
        pg_vip_enabled: true
        pg_vip_address: 10.10.10.2/24
        pg_vip_interface: eth1


    # 这里定义的 Ansible 分组 supabase 包含了 Docker 与 Supabase 相关的配置，您可以使用 ./supabase.yml 剧本直接将其拉起
    supabase:
      hosts:
        10.10.10.10: { supa_seq: 1 }  # instance id
      vars:
        supa_cluster: supa
        docker_enabled: true          # 在 supabase 分组上启用 Docker，因为我们要用 Docker Compose 拉起无状态的部分

        # 【注意】中国大陆地区的用户请指定 DockerHub 镜像站点或代理服务器，否则拉取镜像会失败
        #docker_registry_mirrors: ['https://docker.xxxxx.io']
        #proxy_env:   # add [OPTIONAL] proxy env to /etc/docker/daemon.json configuration file
        #  no_proxy: "localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,*.pigsty,*.aliyun.com,mirrors.*,*.myqcloud.com,*.tsinghua.edu.cn"
        #  all_proxy: http://user:pass@host:port

        # 下面的 Supabase 配置项会自动覆盖或追加到 /opt/supabase/.env 文件中（模板路径：app/supabase/.env ，内容详见：https://github.com/Vonng/pigsty/blob/main/app/supabase/.env）
        supa_config:

          # 【非常重要】: 请修改下面的 JWT_SECRET 以及 ANON_KEY 与 SERVICE_ROLE_KEY : https://supabase.com/docs/guides/self-hosting/docker#securing-your-services
          jwt_secret: your-super-secret-jwt-token-with-at-least-32-characters-long
          anon_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
          service_role_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
          dashboard_username: supabase
          dashboard_password: pigsty

          #【注意】请在下面填入 PostgreSQL 链接串信息
          postgres_host: 10.10.10.10
          postgres_port: 5436             # 使用 5436 端口，通过 haproxy 始终访问主库
          postgres_db: postgres
          postgres_password: DBUser.Supa  # 如果你在上面修改了 PostgreSQL 业务用户的密码，请一并修改这里的 PG 用户密码

          # 如果您使用自定义域名，请修改下面的 domain 字段，将 supa.pigsty 替换为您自己的域名
          site_url: http://supa.pigsty
          api_external_url: http://supa.pigsty
          supabase_public_url: http://supa.pigsty

          #【可选】指定 S3/MinIO 对象存储的配置
          s3_bucket: supa                       # Supabase 使用的 S3/MinIO 桶名称
          s3_endpoint: https://sss.pigsty:9000  # 如果您使用负载均衡器访问 MinIO，或者使用外部 S3 服务，请修改这里的端点
          s3_access_key: supabase               # 对象存储 AK / 用户名
          s3_secret_key: S3User.Supabase        # 对象存储 SK / 密码
          s3_force_path_style: true             # MinIO 要求使用 PATH 样式的 URL
          s3_protocol: https
          s3_region: stub
          minio_domain_ip: 10.10.10.10  # 因为 Docker 使用自己的静态域名解析记录，所以你需要将内部 MinIO 域名 sss.pigsty 解析指向任意安装 MinIO 的节点地址

          #【可选】 指定 SMTP 服务器发送邮件
          #smtp_admin_email: admin@example.com
          #smtp_host: supabase-mail
          #smtp_port: 2500
          #smtp_user: fake_mail_user
          #smtp_pass: fake_mail_password
          #smtp_sender_name: fake_sender
          #enable_anonymous_users: false


  #==============================================================#
  # Global Parameters
  #==============================================================#
  vars:
    version: v3.1.0                   # pigsty version string
    admin_ip: 10.10.10.10             # admin node ip address
    region: default                   # upstream mirror region: default|china|europe
    node_tune: oltp                   # node tuning specs: oltp,olap,tiny,crit
    pg_conf: oltp.yml                 # pgsql tuning specs: {oltp,olap,tiny,crit}.yml
    infra_portal:                     # domain names and upstream servers
      home         : { domain: h.pigsty }
      grafana      : { domain: g.pigsty ,endpoint: "${admin_ip}:3000" , websocket: true }
      prometheus   : { domain: p.pigsty ,endpoint: "${admin_ip}:9090" }
      alertmanager : { domain: a.pigsty ,endpoint: "${admin_ip}:9093" }
      minio        : { domain: m.pigsty ,endpoint: "10.10.10.10:9001", https: true, websocket: true }
      blackbox     : { endpoint: "${admin_ip}:9115" }
      loki         : { endpoint: "${admin_ip}:3100" }  # expose supa studio UI and API via nginx
      
      #【注意】如果您使用公网域名，那么请修改下面的 domain 字段，将 supa.pigsty 替换为您自己的域名，您可以用 key / cert 指定自己的 HTTPS 证书路径
      supa         : { domain: supa.pigsty ,endpoint: "10.10.10.10:8000", websocket: true }

    #----------------------------------#
    # 【非常重要】请修改这些密码！！
    #----------------------------------#
    #grafana_admin_username: admin
    grafana_admin_password: pigsty
    #pg_admin_username: dbuser_dba
    pg_admin_password: DBUser.DBA
    #pg_monitor_username: dbuser_monitor
    pg_monitor_password: DBUser.Monitor
    #pg_replication_username: replicator
    pg_replication_password: DBUser.Replicator
    #patroni_username: postgres
    patroni_password: Patroni.API
    #haproxy_admin_username: admin
    haproxy_admin_password: pigsty

    # 【MINIO】 相关参数
    minio_access_key: minioadmin                                                    #【注意】 MinIO 的根用户名，默认为：`minioadmin`
    minio_secret_key: minioadmin                                                    #【注意】 MinIO 的根用户密码，默认为：`minioadmin`
    minio_buckets: [ { name: pgsql }, { name: supa } ]                              #【注意】 Pigsty 默认使用本地 MinIO 上的 pgsql 桶存放PG备份，supa 桶作为对象存储
    minio_users:                                                                    #【注意】 这是 MinIO 上创建的用户列表，默认创建三个业务用户
      - { access_key: dba , secret_key: S3User.DBA, policy: consoleAdmin }          #【注意】 这是默认的业务管理员用户，目前由用户自行使用，请修改这里的密码！
      - { access_key: pgbackrest , secret_key: S3User.Backup,   policy: readwrite } #【注意】 PGSQL 使用 MinIO 的用户，如果修改这里的密码，请相应调整 pgbackrest_repo 中的密码
      - { access_key: supabase   , secret_key: S3User.Supabase, policy: readwrite } #【注意】 SUPABASE 使用 MinIO 的用户，如果修改这里的密码，请相应调整 supabase 配置文件中的密码
    minio_endpoint: https://sss.pigsty:9000                                         #【信息】 如果你使用负载均衡器访问 MinIO，才需要修改这里的端口 
    node_etc_hosts: ["10.10.10.10 sss.pigsty"]                                      #【信息】 将 MinIO 默认域名 sss.pigsty 指向任意安装 MinIO 节点的地址 
    
    # PostgreSQL 备份存储仓库，如果你希望将备份存储到对象存储中，请修改这两个参数
    pgbackrest_method: minio          # pgbackrest 备份方法：local,minio,[其他用户定义的仓库...]，本例中将备份存储到 MinIO 上
    pgbackrest_repo:                  # pgbackrest 备份仓库: https://pgbackrest.org/configuration.html#section-repository
      
      local:                          # 默认的备份仓库是本地文件系统，但本例中我们【不用】这种方式
        path: /pg/backup              # 本地备份目录 `/pg/backup` （你可以修改 pg_fs_bkup 来修改实际备份盘位置而无需修改这里）
        retention_full_type: count    # 保留 N 个全量备份
        retention_full: 2             # N = 2
      
      #【非常重要】 Pigsty 这里使用 MinIO 存储备份，请在这里根据上面 MinIO 的配置情况进行相应修改
      minio:                             #
        type: s3                         #
        s3_endpoint: sss.pigsty          # 【重要】 如果你上面修改了 MinIO pgBackRest 备份用户的密码，那么这里也需要修改！
        s3_region: us-east-1             #
        s3_bucket: pgsql                 #
        s3_key: pgbackrest               #
        s3_key_secret: S3User.Backup     # 【重要】 如果你上面修改了 MinIO pgBackRest 备份用户的密码，那么这里也需要修改！
        s3_uri_style: path               #
        path: /pgbackrest                #
        storage_port: 9000               #
        storage_ca_file: /pg/cert/ca.crt #  对象存储使用的 CA 文件（如果您的对象存储使用的是自签名 CA 证书）
        bundle: y                        #  将小文件合并打包以减少碎片，提高上传效率
        cipher_type: aes-256-cbc         #  使用 AES-256-CBC 加密备份，如果您使用远程对象存储放备份，加密是合规建议项
        cipher_pass: pgBackRest          #  【重要】备份 AES 加密密码，我们建议修改这个密码，否则加密无意义
        retention_full_type: time        #  保留 一段时间 内的全量备份
        retention_full: 14               #  一段时间 = 14 天


    #【注意】如果你想使用其他 PG 大版本运行 Supabase，修改此变量，建议使用 15-17
    pg_version: 17
    repo_modules: node,pgsql,infra,docker
    repo_packages: [node-bootstrap, infra-package, infra-addons, node-package1, node-package2, pgsql-utility, docker ]
    # 【注意】如果你想安装其他扩展插件，请在这里添加到下载列表中
    repo_extra_packages:
      - pgsql-main
      - supabase   # supabase 别名包含了所有必须的扩展，下面则是一些可选的额外扩展插件
      - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
      - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
      - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
...
```

</details>


--------

## 自建关键技术决策

以下是一些自建 Supabase 会涉及到的关键技术决策，供您参考：

使用默认的**单节点部署** Supabase 无法享受到 PostgreSQL / MinIO 的高可用能力。
尽管如此，单节点部署相比官方纯 Docker Compose 方案依然要有显著优势：
例如开箱即用的监控系统，自由安装扩展的能力，各个组件的扩缩容能力，以及数据库时间点恢复能力等。

如果您只有一台服务器，Pigsty 建议您直接使用外部的 S3 作为对象存储，存放 PostgreSQL 的备份，并承载 Supabase Storage 服务。
这样的部署在故障时可以提供一个最低标准的 RTO （小时级恢复时长）/ RPO （MB级数据损失）[兜底容灾水平](/zh/docs/concept/pitr)。
此外，如果您选择在云上自建，我们也建议您直接使用 S3，而非默认使用的本体 MinIO ，单纯在本地 EBS 上再套一层 MinIO 转发，除了便于开发测试外，对生产实用并没有意义。

在严肃的生产部署中，Pigsty 建议使用至少3～4个节点的部署策略，确保 MinIO 与 PostgreSQL 都使用满足企业级高可用要求的多节点部署。
在这种情况下，您需要相应准备更多节点与磁盘，并相应调整 `pigsty.yml` 配置清单中的集群配置，以及 supabase 集群配置中的接入信息。

部分 Supabase 的功能需要发送邮件，所以要用到 SMTP。除非单纯用于内网，否则对于严肃的生产部署，我们建议您考虑使用外部的 SMTP 服务。
自建的邮件服务器发送的邮件可能会被对方邮件服务器拒收，或者被标记为垃圾邮件。

如果您的服务直接向公网暴露，我们建议您使用 Nginx 进行反向代理，使用真正的域名与 HTTPS 证书，并通过不同的域名区分不同的多个实例。

接下来，我们会依次讨论这几个主题：

- [进阶主题：安全加固](#安全加固)
- 高可用的 PostgreSQL 集群部署与接入
- 高可用的 MinIO 集群部署与接入
- 使用 S3 服务替代 MinIO
- 使用外部 SMTP 服务发送邮件
- 使用真实域名，证书，通过 Nginx 反向代理



--------

## 进阶主题：安全加固

**Pigsty基础组件**

对于严肃的生产部署，我们强烈建议您修改 Pigsty 基础组件的密码。因为这些默认值是公开且众所周知的，不改密码上生产无异于裸奔：

- [`grafana_admin_password`](/zh/docs/reference/param#grafana_admin_password): `pigsty`，Grafana管理员密码
- [`pg_admin_password`](/zh/docs/reference/param#pg_admin_password): `DBUser.DBA`，PG超级用户密码
- [`pg_monitor_password`](/zh/docs/reference/param#pg_monitor_password): `DBUser.Monitor`，PG监控用户密码
- [`pg_replication_password`](/zh/docs/reference/param#pg_replication_password): `DBUser.Replicator`，PG复制用户密码
- [`patroni_password`](/zh/docs/reference/param#patroni_password): `Patroni.API`，Patroni 高可用组件密码
- [`haproxy_admin_password`](/zh/docs/reference/param#haproxy_admin_password): `pigsty`，负载均衡器管控密码
- [`minio_access_key`](/zh/docs/minio/param#grafana_admin_password): `minioadmin`，MinIO 根用户名
- [`minio_secret_key`](/zh/docs/minio/param#minio_secret_key): `minioadmin`，MinIO 根用户密钥
- 此外，强烈建议您修改 Supabase 使用的 [PostgreSQL 业务用户](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L118) 密码，默认为 `DBUser.Supa`

以上密码为 Pigsty 组件模块的密码，强烈建议在安装部署前就设置完毕。

**Supabase密钥**

除了 Pigsty 组件的密码，你还需要 [修改 Supabase 的密钥](https://supabase.com/docs/guides/self-hosting/docker#securing-your-services)，包括

- [`jwt_secret`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L114): 
- [`anon_key`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L115):
- [`service_role_key`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L116): 
- [`dashboard_username`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L117): Supabase Studio Web 界面的默认用户名，默认为 `supabase`
- [`dashboard_password`](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L128): Supabase Studio Web 界面的默认密码，默认为 `pigsty`

这里请您务必参照 [Supabase教程：保护你的服务](https://supabase.com/docs/guides/self-hosting/docker#generate-api-keys) 里的说明：

- 生成一个长度超过 40 个字符的 `jwt_secret`，并使用教程中的工具签发 `anon_key` 与 `service_role_key` 两个 JWT。
- 使用教程中提供的工具，根据 `jwt_secret` 以及过期时间等属性，生成一个 `anon_key` JWT，这是匿名用户的身份凭据。
- 使用教程中提供的工具，根据 `jwt_secret` 以及过期时间等属性，生成一个 `service_role_key`，这是权限更高服务角色的身份凭据。
- 如果您使用的 PostgreSQL 业务用户使用了不同于默认值的密码，请相应修改 [`postgres_password``](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#L126) 的值 
- 如果您的对象存储使用了不同于默认值的密码，请相应修改 [`s3_access_key``](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#136) 与 [`s3_secret_key``](https://github.com/Vonng/pigsty/blob/main/conf/supa.yml#137) 的值

Supabase 部分的凭据修改后，您可以重启 Docker Compose 容器以应用新的配置：

```bash
cd /opt/supabase; docker compose up
```



--------

## 进阶主题：域名接入

如果你在本机或局域网内使用 Supabase，那么可以选择 IP:Port 直连 Kong 对外暴露的 HTTP 8000 端口，当然这样并不好，我们建议您使用域名与 HTTPS 来访问。

使用默认的本地域名 `supa.pigsty` 时，您可以在浏览器本机的 `/etc/hosts` 或局域网 DNS 里来配置它的解析，将其指向安装节点的【对外】IP地址。
Pigsty 管理节点上的 Nginx 会为此域名申请自签名的证书（浏览器显示《不安全》），并将请求转发到 8000 端口的 Kong，由 Supabase 处理。 

不过，更为实用与常见的用例是：Supabase 通过公网队外提供服务。在这种情况下，通常您需要进行以下准备：

- 您的服务器应当有一个公网 IP 地址
- 购买域名，使用 云/DNS/CDN 供应商提供的 DNS 解析服务，将其指向安装节点的公网 IP（下位替代：本地 `/etc/hosts`）
- 申请证书，使用 Let's Encrypt 等证书颁发机构签发的免费 HTTPS 证书，用于加密通信（下位替代：默认自签名证书，手工信任）

准备完成后，请修改 `pigsty.yml` 配置文件中 `all.vars.infra_portal` 部分的 `supa` 域名，以及 `all.children.supabase.vars.supa_config` 中的三个域名字段。

这里我们假设您使用的自定义域名是： `supa.pigsty.cc`

```yaml
all:
  vars:     # 全局配置 
    #.....
    infra_portal:                     # domain names and upstream servers
      home         : { domain: h.pigsty }
      grafana      : { domain: g.pigsty ,endpoint: "${admin_ip}:3000" , websocket: true }
      prometheus   : { domain: p.pigsty ,endpoint: "${admin_ip}:9090" }
      alertmanager : { domain: a.pigsty ,endpoint: "${admin_ip}:9093" }
      minio        : { domain: m.pigsty ,endpoint: "10.10.10.10:9001", https: true, websocket: true }
      blackbox     : { endpoint: "${admin_ip}:9115" }
      loki         : { endpoint: "${admin_ip}:3100" }
      
      #supa        : { domain: supa.pigsty ,endpoint: "10.10.10.10:8000", websocket: true }  # 如果使用申请的 HTTPS 证书，请在这里指定证书的存放路径
      supa         : { domain: supa.pigsty.cc ,endpoint: "10.10.10.10:8000", websocket: true ,cert: /etc/cert/suap.pigsty.cc.crt ,key: /etc/cert/supa.pigsty.cc.key }

  children:           # 集群定义
    supabase:         # supabase 分组
      vars:           # supabase 分组集群配置
        supa_config:  # supabase 配置项
          
          # 请在这里更新 Supabase 使用的域名
          site_url: http://supa.pigsty
          api_external_url: http://supa.pigsty
          supabase_public_url: http://supa.pigsty
```

申请 HTTPS 证书超出了本文范畴，请您自行用 acmebot 之类的工具处理，将申请好的证书放置于指定位置即可。

```bash
./infra.yml    -t nginx_config,nginx_launch
./supabase.yml -t supa_config,supa_launch
```

使用以上命令重新加载 Nginx 和 Supabase 的配置。




--------

## 进阶主题：外部对象存储

您可以使用 S3 或 S3 兼容的服务，来作为 PGSQL 备份与 Supabase 使用的对象存储。这里我们使用一个 阿里云 OSS 对象存储作为例子。

> Pigsty 提供了一个 [`terraform/spec/aliyun-meta-s3.tf`](https://github.com/Vonng/pigsty/blob/main/terraform/spec/aliyun-meta-s3.tf) 模板，用于在阿里云上拉起一台服务器，以及一个 OSS 存储桶。

首先，我们修改 `all.children.supabase.vars.supa_config` 中 S3 相关的配置，将其指向阿里云 OSS 存储桶：

```yaml
all:
  children:
    supabase:
      vars:
        supa_config:
          s3_bucket: pigsty-oss
          s3_endpoint: https://oss-cn-beijing-internal.aliyuncs.com
          s3_access_key: xxxxxxxxxxxxxxxx
          s3_secret_key: xxxxxxxxxxxxxxxx
          s3_force_path_style: false
          s3_protocol: https
          s3_region: oss-cn-beijing
```

同样使用以下命令重载 Supabase 配置：

```bash
./supabase.yml -t supa_config,supa_launch
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
        bundle: y
        cipher_type: aes-256-cbc
        cipher_pass: PG.${pg_cluster}   # 设置一个与集群名称绑定的加密密码
        retention_full_type: time 
        retention_full: 14
```

然后在 `all.vars.pgbackrest_mehod` 中指定使用 `aliyun` 备份仓库，重置 pgBackrest 备份：

```bash
./pgsql.yml -t pgbackrest
```

Pigsty 会将备份仓库切换到外部对象存储上。



--------

## 进阶主题：备份策略

你可以使用操作系统的 Crontab 来设置定时备份策略，例如，向默认的 `all.children.pg-meta.vars` 中添加 [`node_crontab`](/zh/docs/reference/param#node_crontab) 参数：

```yaml
all:
  children:
    pg-meta:
      hosts: { 10.10.10.10: { pg_seq: 1, pg_role: primary } }
      vars:
        pg_cluster: pg-meta  # 每天凌晨一点做个全量备份
        node_crontab: [ '00 01 * * * postgres /pg/bin/pg-backup full' ]
```

然后执行以下命令，将 Crontab 配置应用到节点上：

```bash
./node.yml -t node_crontab
```

更多关于备份策略的主题，请参考 [**备份策略**](/zh/docs/pgsql/pitr/)


--------

## 进阶主题：使用SMTP

你可以使用 SMTP 来发送邮件，修改 supabase 配置，添加 SMTP 信息：

```yaml
all:
  children:
    supabase:
      vars:
        supa_config:
          smtp_host: smtpdm.aliyun.com:80
          smtp_port: 80
          smtp_user: no_reply@mail.your.domain.com
          smtp_pass: your_email_user_password
          smtp_sender_name: MySupabase
          smtp_admin_email: adminxxx@mail.your.domain.com
          enable_anonymous_users: false
```

不要忘了使用 `supabase.yml -t supa_config,supa_launch` 来重载配置



--------

## 进阶主题：真·高可用

经过上面的配置，您已经可以使用一个带有公网域名，HTTPS 证书，SMTP 邮件服务器，备份的 Supabase 了。

如果您的这个节点挂了，起码外部 S3 存储中保留了备份，您可以在新的节点上重新部署 Supabase，然后从备份中恢复。
这样的部署在故障时可以提供一个最低标准的 RTO （小时级恢复时长）/ RPO （MB级数据损失）[兜底容灾水平](/zh/docs/concept/pitr) 兜底。

但如果您想要达到 RTO < 30s ，零数据丢失，那么就需要用到多节点高可用集群了。多节点部署有三个维度：

- [ETCD](/zh/docs/etcd)： DCS 需要使用三个节点或以上，才能容忍一个节点的故障。
- [PGSQL](/zh/docs/pgsql)： PGSQL 同步提交不丢数据模式，建议使用至少三个节点。
- [INFRA](/zh/docs/infra)：监控基础设施故障影响稍小，但我们建议生产环境使用三副本
- Supabase 本身也可以是多节点的副本，实现高可用

我们建议您参考 [trio](/zh/docs/conf/trio) 与 [safe](/zh/docs/conf/safe) 中的集群配置，将您的集群配置升级到三节点或以上。

在这种情况下，您还需要修改 PostgreSQL 与 MinIO 的接入点，使用 DNS / L2 VIP / HAProxy 等 [高可用接入点](/zh/docs/concept/svc)

例如，假设您使用 L2 VIP 接入 MinIO 集群与 PostgreSQL 集群，那么就需要相应修改配置：

```yaml
all:
  children:
    supabase:
      hosts:
        10.10.10.10: { supa_seq: 1 }
        10.10.10.11: { supa_seq: 2 }
        10.10.10.12: { supa_seq: 3 } 
      vars:
        supa_cluster: supa            # cluster name
        supa_config:
          postgres_host: 10.10.10.2             # 例如，使用 PG 集群上的 L2 VIP 接入服务
          postgres_port: 5436                   # 使用 5436 端口，始终直连主库，也可以使用 5433，通过连接池访问主库
          s3_endpoint: https://sss.pigsty:9002  # 假如您的负载均衡器使用了 9002 端口，那么请更改这里的 Endpoint
          minio_domain_ip: 10.10.10.3           # 修改此参数，将 sss.pigsty 的域名指向挂载在 MinIO 集群前面的 L2 VIP
```

应用 Supabase 的配置后，您可能还需要在 Supabase 集群前套上一个负载均衡器，用于将请求分发到后端的多个节点上。

以下是一个三节点的 高可用 Supabase 自建的参考配置文件：

<details><summary>3-Node HA Supabase Config Template</summary>

```yaml

all:

  #==============================================================#
  # Clusters, Nodes, and Modules
  #==============================================================#
  children:

    # infra cluster for proxy, monitor, alert, etc..
    infra:
      hosts:
        10.10.10.10: { infra_seq: 1 ,nodename: infra-1 }
        10.10.10.11: { infra_seq: 2 ,nodename: infra-2, repo_enabled: false, grafana_enabled: false }
        10.10.10.12: { infra_seq: 3 ,nodename: infra-3, repo_enabled: false, grafana_enabled: false }
      vars:

        vip_enabled: true
        vip_vrid: 128
        vip_address: 10.10.10.3
        vip_interface: eth1
        haproxy_services:
          - name: minio                    # [REQUIRED] service name, unique
            port: 9002                     # [REQUIRED] service port, unique
            balance: leastconn             # [OPTIONAL] load balancer algorithm
            options:                       # [OPTIONAL] minio health check
              - option httpchk
              - option http-keep-alive
              - http-check send meth OPTIONS uri /minio/health/live
              - http-check expect status 200
            servers:
              - { name: minio-1 ,ip: 10.10.10.10 ,port: 9000 ,options: 'check-ssl ca-file /etc/pki/ca.crt check port 9000' }
              - { name: minio-2 ,ip: 10.10.10.11 ,port: 9000 ,options: 'check-ssl ca-file /etc/pki/ca.crt check port 9000' }
              - { name: minio-3 ,ip: 10.10.10.12 ,port: 9000 ,options: 'check-ssl ca-file /etc/pki/ca.crt check port 9000' }



    etcd: # dcs service for postgres/patroni ha consensus
      hosts: # 1 node for testing, 3 or 5 for production
        10.10.10.10: { etcd_seq: 1 }  # etcd_seq required
        10.10.10.11: { etcd_seq: 2 }  # assign from 1 ~ n
        10.10.10.12: { etcd_seq: 3 }  # odd number please
      vars: # cluster level parameter override roles/etcd
        etcd_cluster: etcd  # mark etcd cluster name etcd
        etcd_safeguard: false # safeguard against purging
        etcd_clean: true # purge etcd during init process

    # minio cluster 4-node
    minio:
      hosts:
        10.10.10.10: { minio_seq: 1 , nodename: minio-1 }
        10.10.10.11: { minio_seq: 2 , nodename: minio-2 }
        10.10.10.12: { minio_seq: 3 , nodename: minio-3 }
      vars:
        minio_cluster: minio
        minio_data: '/data{1...4}'
        minio_buckets: [ { name: pgsql }, { name: supa } ]
        minio_users:
          - { access_key: dba , secret_key: S3User.DBA, policy: consoleAdmin }
          - { access_key: pgbackrest , secret_key: S3User.Backup,   policy: readwrite }
          - { access_key: supabase   , secret_key: S3User.Supabase, policy: readwrite }

    # pg-meta, the underlying postgres database for supabase
    pg-meta:
      hosts:
        10.10.10.10: { pg_seq: 1, pg_role: primary }
        10.10.10.11: { pg_seq: 2, pg_role: replica }
        10.10.10.12: { pg_seq: 3, pg_role: replica }
      vars:
        pg_cluster: pg-meta
        pg_users:
          # supabase roles: anon, authenticated, dashboard_user
          - { name: anon           ,login: false }
          - { name: authenticated  ,login: false }
          - { name: dashboard_user ,login: false ,replication: true ,createdb: true ,createrole: true }
          - { name: service_role   ,login: false ,bypassrls: true }
          # supabase users: please use the same password
          - { name: supabase_admin             ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: true   ,roles: [ dbrole_admin ] ,superuser: true ,replication: true ,createdb: true ,createrole: true ,bypassrls: true }
          - { name: authenticator              ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] }
          - { name: supabase_auth_admin        ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_storage_admin     ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin, authenticated ,anon ,service_role ] ,createrole: true }
          - { name: supabase_functions_admin   ,password: 'DBUser.Supa' ,pgbouncer: true ,inherit: false  ,roles: [ dbrole_admin ] ,createrole: true }
          - { name: supabase_replication_admin ,password: 'DBUser.Supa' ,replication: true ,roles: [ dbrole_admin ]}
          - { name: supabase_read_only_user    ,password: 'DBUser.Supa' ,bypassrls: true ,roles: [ dbrole_readonly, pg_read_all_data ] }
        pg_databases:
          - name: postgres
            baseline: supabase.sql
            owner: supabase_admin
            comment: supabase postgres database
            schemas: [ extensions ,auth ,realtime ,storage ,graphql_public ,supabase_functions ,_analytics ,_realtime ]
            extensions:
              - { name: pgcrypto  ,schema: extensions  } # 1.3   : cryptographic functions
              - { name: pg_net    ,schema: extensions  } # 0.9.2 : async HTTP
              - { name: pgjwt     ,schema: extensions  } # 0.2.0 : json web token API for postgres
              - { name: uuid-ossp ,schema: extensions  } # 1.1   : generate universally unique identifiers (UUIDs)
              - { name: pgsodium        }                # 3.1.9 : pgsodium is a modern cryptography library for Postgres.
              - { name: supabase_vault  }                # 0.2.8 : Supabase Vault Extension
              - { name: pg_graphql      }                # 1.5.9 : pg_graphql: GraphQL support
              - { name: pg_jsonschema   }                # 0.3.3 : pg_jsonschema: Validate json schema
              - { name: wrappers        }                # 0.4.3 : wrappers: FDW collections
              - { name: http            }                # 1.6   : http: allows web page retrieval inside the database.
              - { name: pg_cron         }                # 1.6   : pg_cron: Job scheduler for PostgreSQL
              - { name: timescaledb     }                # 2.17  : timescaledb: Enables scalable inserts and complex queries for time-series data
              - { name: pg_tle          }                # 1.2   : pg_tle: Trusted Language Extensions for PostgreSQL
              - { name: vector          }                # 0.8.0 : pgvector: the vector similarity search
        # supabase required extensions
        pg_libs: 'pg_stat_statements, plpgsql, plpgsql_check, pg_cron, pg_net, timescaledb, auto_explain, pg_tle, plan_filter'
        pg_extensions: # extensions to be installed on this cluster
          - supabase   # essential extensions for supabase
          - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
          - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
          - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
        pg_parameters:
          cron.database_name: postgres
          pgsodium.enable_event_trigger: off
        pg_hba_rules: # supabase hba rules, require access from docker network
          - { user: all ,db: postgres  ,addr: intra         ,auth: pwd ,title: 'allow supabase access from intranet'    }
          - { user: all ,db: postgres  ,addr: 172.17.0.0/16 ,auth: pwd ,title: 'allow access from local docker network' }
        pg_vip_enabled: true
        pg_vip_address: 10.10.10.2/24
        pg_vip_interface: eth1
        node_crontab: [ '00 01 * * * postgres /pg/bin/pg-backup full' ] # make a full backup every 1am


    # launch supabase stateless part with docker compose: ./supabase.yml
    supabase:
      hosts:
        10.10.10.10: { supa_seq: 1 }  # instance 1
        10.10.10.11: { supa_seq: 2 }  # instance 2
        10.10.10.12: { supa_seq: 3 }  # instance 3
      vars:
        supa_cluster: supa            # cluster name
        docker_enabled: true          # enable docker

        # use these to pull docker images via proxy and mirror registries
        #docker_registry_mirrors: ['https://docker.xxxxx.io']
        #proxy_env:   # add [OPTIONAL] proxy env to /etc/docker/daemon.json configuration file
        #  no_proxy: "localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,*.pigsty,*.aliyun.com,mirrors.*,*.myqcloud.com,*.tsinghua.edu.cn"
        #  #all_proxy: http://user:pass@host:port

        # these configuration entries will OVERWRITE or APPEND to /opt/supabase/.env file (src template: app/supabase/.env)
        # check https://github.com/Vonng/pigsty/blob/main/app/supabase/.env for default values
        supa_config:

          # IMPORTANT: CHANGE JWT_SECRET AND REGENERATE CREDENTIAL ACCORDING!!!!!!!!!!!
          # https://supabase.com/docs/guides/self-hosting/docker#securing-your-services
          jwt_secret: your-super-secret-jwt-token-with-at-least-32-characters-long
          anon_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE
          service_role_key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJzZXJ2aWNlX3JvbGUiLAogICAgImlzcyI6ICJzdXBhYmFzZS1kZW1vIiwKICAgICJpYXQiOiAxNjQxNzY5MjAwLAogICAgImV4cCI6IDE3OTk1MzU2MDAKfQ.DaYlNEoUrrEn2Ig7tqibS-PHK5vgusbcbo7X36XVt4Q
          dashboard_username: supabase
          dashboard_password: pigsty

          # postgres connection string (use the correct ip and port)
          postgres_host: 10.10.10.3       # use the pg_vip_address rather than single node ip
          postgres_port: 5433             # access via the 'default' service, which always route to the primary postgres
          postgres_db: postgres
          postgres_password: DBUser.Supa  # password for supabase_admin and multiple supabase users

          # expose supabase via domain name
          site_url: http://supa.pigsty
          api_external_url: http://supa.pigsty
          supabase_public_url: http://supa.pigsty

          # if using s3/minio as file storage
          s3_bucket: supa
          s3_endpoint: https://sss.pigsty:9002
          s3_access_key: supabase
          s3_secret_key: S3User.Supabase
          s3_force_path_style: true
          s3_protocol: https
          s3_region: stub
          minio_domain_ip: 10.10.10.3   # sss.pigsty domain name will resolve to this l2 vip that bind to all nodes

          # if using SMTP (optional)
          #smtp_admin_email: admin@example.com
          #smtp_host: supabase-mail
          #smtp_port: 2500
          #smtp_user: fake_mail_user
          #smtp_pass: fake_mail_password
          #smtp_sender_name: fake_sender
          #enable_anonymous_users: false



  #==============================================================#
  # Global Parameters
  #==============================================================#
  vars:
    version: v3.1.0                   # pigsty version string
    admin_ip: 10.10.10.10             # admin node ip address
    region: china                     # upstream mirror region: default|china|europe
    node_tune: oltp                   # node tuning specs: oltp,olap,tiny,crit
    pg_conf: oltp.yml                 # pgsql tuning specs: {oltp,olap,tiny,crit}.yml
    infra_portal:                     # domain names and upstream servers
      home         : { domain: h.pigsty }
      grafana      : { domain: g.pigsty ,endpoint: "${admin_ip}:3000" , websocket: true }
      prometheus   : { domain: p.pigsty ,endpoint: "${admin_ip}:9090" }
      alertmanager : { domain: a.pigsty ,endpoint: "${admin_ip}:9093" }
      minio        : { domain: m.pigsty ,endpoint: "10.10.10.10:9001", https: true, websocket: true }
      blackbox     : { endpoint: "${admin_ip}:9115" }
      loki         : { endpoint: "${admin_ip}:3100" }  # expose supa studio UI and API via nginx
      supa         : { domain: supa.pigsty ,endpoint: "10.10.10.10:8000", websocket: true }

    #----------------------------------#
    # Credential: CHANGE THESE PASSWORDS
    #----------------------------------#
    #grafana_admin_username: admin
    grafana_admin_password: pigsty
    #pg_admin_username: dbuser_dba
    pg_admin_password: DBUser.DBA
    #pg_monitor_username: dbuser_monitor
    pg_monitor_password: DBUser.Monitor
    #pg_replication_username: replicator
    pg_replication_password: DBUser.Replicator
    #patroni_username: postgres
    patroni_password: Patroni.API
    #haproxy_admin_username: admin
    haproxy_admin_password: pigsty

    # use minio as supabase file storage, single node single driver mode for demonstration purpose
    minio_access_key: minioadmin      # root access key, `minioadmin` by default
    minio_secret_key: minioadmin      # root secret key, `minioadmin` by default
    minio_buckets: [ { name: pgsql }, { name: supa } ]
    minio_users:
      - { access_key: dba , secret_key: S3User.DBA, policy: consoleAdmin }
      - { access_key: pgbackrest , secret_key: S3User.Backup,   policy: readwrite }
      - { access_key: supabase   , secret_key: S3User.Supabase, policy: readwrite }
    minio_endpoint: https://sss.pigsty:9000    # explicit overwrite minio endpoint with haproxy port
    node_etc_hosts: ["10.10.10.3 sss.pigsty"] # domain name to access minio from all nodes (required)

    # use minio as default backup repo for PostgreSQL
    pgbackrest_method: minio          # pgbackrest repo method: local,minio,[user-defined...]
    pgbackrest_repo:                  # pgbackrest repo: https://pgbackrest.org/configuration.html#section-repository
      local:                          # default pgbackrest repo with local posix fs
        path: /pg/backup              # local backup directory, `/pg/backup` by default
        retention_full_type: count    # retention full backups by count
        retention_full: 2             # keep 2, at most 3 full backup when using local fs repo
      minio:                          # optional minio repo for pgbackrest
        type: s3                      # minio is s3-compatible, so s3 is used
        s3_endpoint: sss.pigsty       # minio endpoint domain name, `sss.pigsty` by default
        s3_region: us-east-1          # minio region, us-east-1 by default, useless for minio
        s3_bucket: pgsql              # minio bucket name, `pgsql` by default
        s3_key: pgbackrest            # minio user access key for pgbackrest
        s3_key_secret: S3User.Backup  # minio user secret key for pgbackrest
        s3_uri_style: path            # use path style uri for minio rather than host style
        path: /pgbackrest             # minio backup path, default is `/pgbackrest`
        storage_port: 9002            # minio port, 9000 by default
        storage_ca_file: /pg/cert/ca.crt  # minio ca file path, `/pg/cert/ca.crt` by default
        bundle: y                     # bundle small files into a single file
        cipher_type: aes-256-cbc      # enable AES encryption for remote backup repo
        cipher_pass: pgBackRest       # AES encryption password, default is 'pgBackRest'
        retention_full_type: time     # retention full backup by time on minio repo
        retention_full: 14            # keep full backup for last 14 days

    # download docker and supabase related extensions
    pg_version: 17
    repo_modules: node,pgsql,infra,docker
    repo_packages: [node-bootstrap, infra-package, infra-addons, node-package1, node-package2, pgsql-utility, docker ]
    repo_extra_packages:
      - pgsql-main
      - supabase   # essential extensions for supabase
      - timescaledb postgis pg_graphql pg_jsonschema wrappers pg_search pg_analytics pg_parquet plv8 duckdb_fdw pg_cron pg_timetable pgqr
      - supautils pg_plan_filter passwordcheck plpgsql_check pgaudit pgsodium pg_vault pgjwt pg_ecdsa pg_session_jwt index_advisor
      - pgvector pgvectorscale pg_summarize pg_tiktoken pg_tle pg_stat_monitor hypopg pg_hint_plan pg_http pg_net pg_smtp_client pg_idkit
```

</details>


<br>

------------

<br>