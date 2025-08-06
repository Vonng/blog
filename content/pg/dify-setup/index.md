---
title: 使用Pigsty,PG,PGVector自建Dify -- AI工作流平台
linktitle: 使用Pigsty自建Dify，AI工作流 
date: 2024-06-22
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [微信公众号](https://mp.weixin.qq.com)
summary: >
  Dify 是一个生成式 AI 应用创新引擎，开源的 LLM 应用开发平台，本文介绍了如何使用 Pigsty 自建 Dify。
tags: [PostgreSQL,Docker,PigstyApp]
---


[**Dify**](https://dify.ai/zh) 是一个生成式 AI 应用创新引擎，开源的 LLM 应用开发平台。提供从 Agent 构建到 AI workflow 编排、RAG 检索、模型管理等能力，帮助用户轻松构建和运营生成式 AI 原生应用。

当然，像这样的一个 AI 工作流编排软件，在底下也少不得用到数据库 —— Dify 便是用 PostgreSQL 存储数据的，当然还有 Redis 缓存，与一个专用的向量数据库。Docker 镜像拉起来本地玩玩可以，生产环境部署的话，数据库肯定不能这么搞，高可用，备份，监控啥都没有。
好在 Pigsty 就提供了开箱即用的生产级高可用 PostgreSQL 集群，也正好提供了 Dify 需要用到的 Redis 与 S3 （MinIO） 服务，也提供了 Nginx 可以对外暴露 Web 服务，堪称 Dify 最佳拍档。

[![docker-compose.png](docker-compose.png)](https://github.com/langgenius/dify/blob/main/docker/docker-compose.yaml)

> 有了 Pigsty，你只需要用 `docker compose` 拉起无状态的蓝圈部分就好了，状态放在由外部服务由 Pigsty 管理。

这里我不得不吐槽一下 Dify 模板的设计，元数据都已经用 PostgreSQL 存储了，你直接加个 `pgvector` 不就能拿来当向量数据库了？更让人想吐槽的是 `pgvector` 竟然还是一个单独的镜像与容器，你直接用一个带 pgvector 的 PG 镜像不就行了？
Dify “支持” 了一堆花里胡哨的向量数据库，但你既然已经选定了 PostgreSQL 了，向量数据库默认也用 `pgvector` 就是自然而然地选择了。同理，我觉得 Dify 官方应该考虑一下把 Redis 去掉，Celery 任务队列又不是不能用 PostgreSQL 作为后端存储，弄那么多数据库纯属吃饱了撑着。如无必要，勿增实体。

所以 Pigsty 提供的 [Dify Docker Compose 模板](https://github.com/Vonng/pigsty/tree/master/app/dify) 也对官方的样例做了一些修改，把 `db` 和 `redis` 两个数据库镜像给去掉了，使用由 Pigsty 管理的实例，向量数据库固定使用 `pgvector`，复用同一个 PostgreSQL 实例。

最后上面那个架构就被简化为无状态的：`dify-api`，`dify-web`，`dify-worker` 三个无状态容器，可以随意创建销毁。当然还有两个可选的 `ssrf_proxy` 与 `nginx`，用于提供代理与些许安全特性。
还有一点状态尾巴是 [文件系统卷](https://github.com/Vonng/pigsty/blob/master/app/dify/docker-compose.yml#L128)，存放私钥之类的东西，定期备份一下就好了，也可以使用 MinIO 替代。

参考资料：

- [GitHub: langgenius/Dify](https://github.com/langgenius/dify/)
- [Pigsty: Dify Docker Compose Template](https://github.com/Vonng/pigsty/tree/master/app/dify)




------

## Pigsty的准备工作

我们用 [单机安装](/zh/docs/concept/arch/#单机安装) 的 Pigsty 为例，假设你有一台 IP 地址为 `10.10.10.10` 的机器，已经 [安装好了单机 Pigsty](https://doc.pgsty.com/install/start)。

当然，我们需要在 Pigsty 配置文件 `pigsty.yml` 中定义一下我们所需的数据库集群。
这里定义了一个名为 `pg-meta` 的集群，其中有一个名为 `dbuser_dify` 的超级业务用户（它这个实现的有点挫，在 Migration 脚本里面执行了 `CREATE EXTENSION` ），一个安装了 `pgvector` 扩展插件的数据库 `dify`，以及一条特定的防火墙规则，允许用户通过密码从任何地方访问数据库（你也可以将其限制为docker的网段 `172.0.0.0/8` 之类更精确的范围）。

同时，上面还定义了一个单实例的标准 Redis 集群 `redis-dify`，设置了密码 `redis.dify`。

```yaml
pg-meta:
  hosts: { 10.10.10.10: { pg_seq: 1, pg_role: primary } }
  vars:
    pg_cluster: pg-meta
    pg_users: [ { name: dbuser_dify ,password: DBUser.Dify  ,superuser: true ,pgbouncer: true ,roles: [ dbrole_admin ] } ]
    pg_databases: [ { name: dify, owner: dbuser_dify, extensions: [ { name: pgvector } ] } ]
    pg_hba_rules: [ { user: dbuser_dify , db: all ,addr: world ,auth: pwd ,title: 'allow dify user world pwd access' } ]

redis-dify:
  hosts: { 10.10.10.10: { redis_node: 1 , redis_instances: { 6379: { } } } }
  vars: { redis_cluster: redis-dify ,redis_password: 'redis.dify' ,redis_max_memory: 64MB }
```

这里出于演示目的，我们全部使用单实例配置，你可以参考 Pigsty 文档部署 [高可用](https://ext.pgsty.com/zh/pgsql/arch) 的 PG 集群与 Redis 集群。总之，在定义完成后，使用以下命令创建 PG 和 Redis 。

```bash
bin/pgsql-add  pg-meta                # create the dify database cluster
bin/redis-add  redis-dify             # create redis cluster
```

当然，您也可以在现有的 PostgreSQL 集群，例如 `pg-meta` 上新定义业务用户与业务数据库，并通过以下命令创建：

```bash
bin/pgsql-user pg-meta dbuser_dify    # create dify biz user
bin/pgsql-db   pg-meta dify           # create dify biz database
```

您应该可以通过以下的连接串，访问到 PostgreSQL 与 Redis，当然连接信息请根据实际情况进行修改。

```bash
psql postgres://dbuser_dify:DBUser.Dify@10.10.10.10:5432/dify -c 'SELECT 1'
redis-cli -u redis://redis.dify@10.10.10.10:6379/0 ping
```

当你确认这两个连接串可用后，大功告成，你可以开始部署 Dify 了。

这里出于演示方便的原因，使用IP直连的土办法，如果是多节点的高可用 PG 集群，请参考 [接入](/zh/docs/concept/svc/) 一节。

当然，上面的部分是假设你已经是 Pigsty 用户，了解如何部署 PostgreSQL 与 Redis 集群。你可以直接跳过下一节，查看 [Dify 如何配置](#dify的配置工作)。



------

## 从零开始的一些说明

如果您已经了解如何配置使用 Pigsty，可以略过本节。

[从零安装](https://doc.pgsty.com/zh/install/start) Pigsty 需要 [准备](https://doc.pgsty.com/zh/prepare) 一台符合要求的机器节点： Linux / x86_64，静态 IP，使用带有免密 `sudo` 权限的用户，执行以下命令：

```bash
curl -fsSL https://repo.pigsty.cc/get | bash
```

然后依次完成以下步骤：

```bash
cd ~/pigsty      # 下载源码包解压后进入 Pigsty 源码目录，完成后续 准备、配置、安装 三个步骤
./bootstrap      # 【可选项】用于确保 Ansible 正常安装，如果 /tmp/pkg.tgz 离线包则使用它
./configure      # 【可选项】执行环境检测，并生成相应的推荐配置文件，如果知道如何配置可以跳过

# …… 这里请修改自动生成的配置 pigsty.yml ，将上面的集群定义填入 all.children 部分内

./install.yml    # 根据生成的配置文件开始在当前节点上执行安装，使用离线安装包大概需要10分钟完成
```

您应当将上面的 PostgreSQL 集群与 Redis 集群定义填入 `pigsty.yml` 文件中，然后执行 [`install.yml`](https://doc.pgsty.com/zh/infra/playbook) 完成安装。

**Redis安装问题**

Pigsty 默认不会安装 Redis，所以您需要使用 [`redis.yml`](https://doc.pgsty.com/zh/redis/playbook#redisyml) 剧本显式完成 Redis 安装：

```bash
./redis.yml
```


**Docker安装问题**

Pigsty 默认不会在当前节点安装 Docker，所以您需要使用 [`docker.yml`](https://doc.pgsty.com/zh/docker/playbook#redisyml) 剧本安装 Docker。

```bash
./docker.yml
```


**Docker Hub 被墙问题**

请注意，对于中国大陆用户来说，Docker Hub 与各镜像站点目前出于封锁状态，需要 “科学上网” 才能拉取 Dify 所需的镜像，您可以考虑 `docker save|load`，或者为 Docker Daemon 配置代理。

要为 Docker Daemon 配置代理，您需要在 [`proxy_env`](https://doc.pgsty.com/zh/infra/playbook#proxy_env) 中指定 `http_proxy` 与 `https_proxy` 环境变量，该参数会在 `docker_config` 任务中被写入 `/etc/docker/daemon.json` 中：

```json
{
  "proxies": {
    "http-proxy": "http://192.168.x.x:8118",
    "https-proxy": "http://192.168.x.x:8118",
    "no-proxy": "localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,*.pigsty,*.aliyun.com,mirrors.*,*.myqcloud.com,*.tsinghua.edu.cn"
  }
}
```

当然您也可以直接在配置文件中填入您的 HTTP/HTTPS 代理地址，并使用 `systemctl restart docker` 重启生效。

```bash
$ docker compose pull
[+] Pulling 5/5
✔ worker Skipped - Image is already being pulled by api
✔ web Pulled
✔ api Pulled
✔ ssrf_proxy Pulled
✔ nginx Pulled
```

配置代理后，镜像都可以成功拉取了。当然您也可以使用其他可用的镜像站点，例如 quay.io 等。


------

## Dify的配置工作

Dify 的配置参数一如往常地放在 [`.env`](https://github.com/Vonng/pigsty/blob/master/app/dify/.env) 文件中，内容如下所示：

所有参数都顾名思义，已经填入了在 [Pigsty默认沙箱环境](https://doc.pgsty.com/zh/prepare/sandbox/) 中可以直接工作的默认值，数据库连接信息请根据您的真实配置，与上面 PG / Redis 集群配置保持一致即可。
我们建议你随便改一下这个 `SECRET_KEY` 字段，可以使用 `openssl rand -base64 42` 生成一个强密钥。

```bash
# meta parameter
DIFY_PORT=8001 # expose dify nginx service with port 8001 by default
LOG_LEVEL=INFO # The log level for the application. Supported values are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
SECRET_KEY=sk-9f73s3ljTXVcMT3Blb3ljTqtsKiGHXVcMT3BlbkFJLK7U # A secret key for signing and encryption, gen with `openssl rand -base64 42`

# postgres credential
PG_USERNAME=dbuser_dify
PG_PASSWORD=DBUser.Dify
PG_HOST=10.10.10.10
PG_PORT=5432
PG_DATABASE=dify

# redis credential
REDIS_HOST=10.10.10.10
REDIS_PORT=6379
REDIS_USERNAME=''
REDIS_PASSWORD=redis.dify

# minio/s3 [OPTIONAL] when STORAGE_TYPE=s3
STORAGE_TYPE=local
S3_ENDPOINT='https://sss.pigsty'
S3_BUCKET_NAME='infra'
S3_ACCESS_KEY='dba'
S3_SECRET_KEY='S3User.DBA'
S3_REGION='us-east-1'
```

填好连接信息后，我们就可以使用 Docker Compose 拉起 Dify 服务了：

```bash
cd pigsty/app/dify && make up
```



------

## 使用Nginx暴露Web服务

Dify 的 Docker Compose 模板里面已经包含了一个 Nginx Server，占据了宿主机的 80 端口。如果你的这台机器就是拿来专门跑 Dify 的那没问题。如果你用的是 Pigsty 单机安装，那么这台宿主机上的 80 端口已经被 Pigsty 部署的 Nginx Web Portal 占据了。

所以，Pigsty 提供的模板中，`DIFY_PORT` 默认使用了 `8001`，并通过宿主机上 Pigsty 部署的 Nginx 转发至此端口。当然我们也提供选项B，你也可以直接在 `/etc/nginx/conf.d/dify.conf` 里使用样例配置，直接指向 Dify 的 `web` 与 `api` 端口。 

在 `pigsty.yml` 配置文件中的 `infra_portal` 参数中新增一行 Dify 的配置

```yaml
infra_portal:                     # domain names and upstream servers
  home         : { domain: h.pigsty }
  grafana      : { domain: g.pigsty ,endpoint: "${admin_ip}:3000" , websocket: true }
  prometheus   : { domain: p.pigsty ,endpoint: "${admin_ip}:9090" }
  alertmanager : { domain: a.pigsty ,endpoint: "${admin_ip}:9093" }
  blackbox     : { endpoint: "${admin_ip}:9115" }
  loki         : { endpoint: "${admin_ip}:3100" }
  
  dify         : { domain: dify.pigsty ,endpoint: "10.10.10.10:8001", websocket: true }
```

执行以下剧本，重新生成 Nginx 配置、证书并应用：

```bash
./infra.yml -t nginx
```

当然如果要通过域名访问，你要把自己的域名 `dify.pigsty` 添加到域名服务器，或者简单地写入：`/etc/hosts` 或 `C:\Windows\System32\drivers\etc\hosts` 之类的静态域名解析文件。

然后，你就可以从浏览器中，通过 http://dify.pigsty 访问 Dify IDE 了。

