---
title: FerretDB：假扮成MongoDB的PG
date: 2023-10-08
hero: /hero/ferretdb.jpg
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [微信公众号](https://mp.weixin.qq.com/s/gfs8pBJuYjE_wfAvjcak8Q)
summary: >
  FerretDB旨在提供一个基于 PostgreSQL 的，真正开源的 MongoDB 替代。
tags: [PostgreSQL,PG生态,MongoDB,扩展]
---


**MongoDB** 曾经是一项令人惊叹的技术，让开发者能够抛开关系型数据库的“模式束缚”，快速构建应用程序。然而随着时间推移，MongoDB 放弃了它的开源本质，这使得许多开源项目和早期商业项目无法使用它。

大多数 MongoDB 用户其实并不需要 MongoDB 提供的高级功能，但他们确实需要一个易于使用的**开源**文档数据库解决方案。PostgreSQL 的 JSON 功能支持已经足够完善了：二进制存储 JSONB，GIN 任意字段索引 ，各种 JSON 处理函数，JSON PATH 和 JSON Schema，PG早已是一个功能完备，性能强大的文档数据库了。但是提供替代的功能，和**直接仿真**还是不一样的。

为了填补这个空白，**FerretDB** 应运而生，旨在提供一个**真正开源**的 **MongoDB** 替代。这是一个非常有趣的项目，之前的名字叫 “**MangoDB**”，因为有碰瓷 "**MongoDB**" 的嫌疑（芒果DB vs 蒙古DB），所以在 1.0 版本改成了现在的名字 FerretDB。FerretDB 可以为使用 MongoDB 驱动的应用提供一个丝滑迁移到 PostgreSQL 的过渡方案。

它的功能就是让 PostgreSQL 假扮成 MongoDB。它是一个为 PG 提供 MongoDB Wire Protocol 支持的协议转换中间件/Proxy。上次做过这种事的插件是 AWS 的 Babelfish，让 PostgreSQL 兼容 SQL Service 的线缆协议假扮成 Microsoft SQL Server。

FerretDB 作为一个选装组件，对丰富 PostgreSQL 生态大有裨益。Pigsty 在 1.x 中就提供了基于 Docker 的 FerretDB 模板，在 v2.3 中更是提供了原生部署支持。目前，Pigsty 社区已经与 FerretDB 社区成为了合作伙伴，后续将进行深度的合作与适配支持。

本文简单介绍了 FerretDB 的安装、部署与使用。





------

## 配置

在部署 Mongo (FerretDB) 集群前，你需要先在配置清单中使用相关参数定义好它。下面的例子将默认的单节点 `pg-meta` 集群的 `meta` 数据库作为 FerretDB 的底层存储：

```
ferret:
  hosts: { 10.10.10.10: { mongo_seq: 1 } }
  vars:
    mongo_cluster: ferret
    mongo_pgurl: 'postgres://dbuser_meta:DBUser.Meta@10.10.10.10:5432/meta'
```

这里 `mongo_cluster` 与 `mongo_seq` 属于不可或缺的身份参数，对于 FerretDB 来说，还有一个必须提供的参数是 `mongo_pgurl`，指定了底层 PG 的位置。

您可以使用 服务 来接入高可用的 PostgreSQL 集群，并部署多个 FerretDB 实例副本并绑定 L2 VIP 以实现 FerretDB 层本身的高可用。

```
ferret-ha:
  hosts:
    10.10.10.45: { mongo_seq: 1 }
    10.10.10.46: { mongo_seq: 2 }
    10.10.10.47: { mongo_seq: 3 }
  vars:
    mongo_cluster: ferret
    mongo_pgurl: 'postgres://test:test@10.10.10.3:5436/test'
    vip_enabled: true
    vip_vrid: 128
    vip_address: 10.10.10.99
    vip_interface: eth1
```




------

## 管理

### 创建Mongo集群

在配置清单中定义好MONGO集群后，您可以使用以下命令完成安装。

```bash
./mongo.yml -l ferret   # 在 ferret 分组上安装“MongoDB/FerretDB”
```

因为 FerretDB 使用了 PostgreSQL 作为底层存储，所以重复运行此剧本通常并无大碍。

### 移除Mongo集群

要移除 Mongo/FerretDB 集群，运行 `mongo.yml`剧本的子任务：`mongo_purge`，并使用 `mongo_purge` 命令行参数即可：

```bash
./mongo.yml -e mongo_purge=true -t mongo_purge
```

### 安装MongoSH

您可以使用 MongoSH 作为客户端工具访问 FerretDB 集群

```bash
cat > /etc/yum.repos.d/mongo.repo <<EOF
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/6.0/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
EOF
yum install -y mongodb-mongosh
```

当然，您也可以直接安装 `mongosh` 的 RPM 包：

```bash
rpm -ivh https://mirrors.tuna.tsinghua.edu.cn/mongodb/yum/el7/RPMS/mongodb-mongosh-1.9.1.x86_64.rpm
```

### 连接到FerretDB

你可以使用 MongoDB 连接串，用任何语言的 MongoDB 驱动访问 FerretDB，这里以上面安装的 `mongosh` 命令行工具为例：

```bash
mongosh 'mongodb://dbuser_meta:DBUser.Meta@10.10.10.10:27017?authMechanism=PLAIN'mongosh 'mongodb://test:test@10.10.10.11:27017/test?authMechanism=PLAIN'
```

Pigsty 管理的 PostgreSQL 集群默认使用 `scram-sha-256` 作为默认的认证方式，因此，您必须使用 `PLAIN` 认证方式连接至 FerretDB。参阅 FerretDB：认证[17] 获取详细信息。

你也可以使用其他 PostgreSQL 用户来访问 FerretDB，只要在连接串中指定即可：

```bash
mongosh 'mongodb://dbuser_dba:DBUser.DBA@10.10.10.10:27017?authMechanism=PLAIN'
```

------

## 快速上手

你可以连接到 FerretDB 并假装它是一个 MongoDB 集群。

```
$ mongosh 'mongodb://dbuser_meta:DBUser.Meta@10.10.10.10:27017?authMechanism=PLAIN'
```

MongoDB 的命令会被翻译为`SQL`命令，在底下的 PostgreSQL 中执行：

```bash
use test                            # CREATE SCHEMA test;
db.dropDatabase()                   # DROP SCHEMA test;
db.createCollection('posts')        # CREATE TABLE posts(_data JSONB,...)
db.posts.insert({                   # INSERT INTO posts VALUES(...);
    title: 'Post One',body: 'Body of post one',category: 'News',tags: ['news', 'events'],
    user: {name: 'John Doe',status: 'author'},date: Date()}
)
db.posts.find().limit(2).pretty()   # SELECT * FROM posts LIMIT 2;
db.posts.createIndex({ title: 1 })  # CREATE INDEX ON posts(_data->>'title');
```

如果你不是很熟悉 MongoDB，这里有一个快速上手教程，同样适用于 FerretDB： Perform CRUD Operations with MongoDB Shell[18]

如果你希望生成一些样例负载，可以使用 `mongosh` 执行以下的简易测试剧本：

```bash
cat > benchmark.js <<'EOF'
const coll = "testColl";
const numDocs = 10000;

for (let i = 0; i < numDocs; i++) {  // insert
  db.getCollection(coll).insert({ num: i, name: "MongoDB Benchmark Test" });
}

for (let i = 0; i < numDocs; i++) {  // select
  db.getCollection(coll).find({ num: i });
}

for (let i = 0; i < numDocs; i++) {  // update
  db.getCollection(coll).update({ num: i }, { $set: { name: "Updated" } });
}

for (let i = 0; i < numDocs; i++) {  // delete
  db.getCollection(coll).deleteOne({ num: i });
}
EOF

mongosh 'mongodb://dbuser_meta:DBUser.Meta@10.10.10.10:27017?authMechanism=PLAIN' benchmark.js
```

你可以查阅 FerretDB 支持的 MongoDB命令，同时还有一些[已知的区别](https://docs.ferretdb.io/diff/)，对于基本的使用来说，通常不是什么大问题。

1. FerretDB uses the same protocol error names and codes, but the exact error messages may be different in some cases.
2. FerretDB does not support NUL (`\0`) characters in strings.
3. FerretDB does not support nested arrays.
4. FerretDB converts `-0` (negative zero) to `0` (positive zero).
5. Document restrictions:
    - document keys must not contain `.` sign;
    - document keys must not start with `$` sign;
    - document fields of double type must not contain `Infinity`, `-Infinity`, or `NaN` values.
6. When insert command is called, insert documents must not have duplicate keys.
7. Update command restrictions:
    - update operations producing `Infinity`, `-Infinity`, or `NaN` are not supported.
8. Database and collection names restrictions:
    - name cannot start with the reserved prefix `_ferretdb_`;
    - database name must not include non-latin letters;
    - collection name must be valid UTF-8 characters;
9. FerretDB offers the same validation rules for the `scale` parameter in both the `collStats` and `dbStats` commands. If an invalid `scale` value is provided in the `dbStats` command, the same error codes will be triggered as with the `collStats` command.




------

## 剧本

Pigsty 提供了一个内置的剧本： `mongo.yml`，用于在节点上安装 FerretDB 集群。

### `mongo.yml`

该剧本由以下子任务组成：

* `mongo_check` ：检查 mongo 身份参数•`mongo_dbsu` ：创建操作系统用户 mongod•`mongo_install` ：安装 mongo/ferretdb RPM包•`mongo_purge` ：清理现有 mongo/ferretdb 集群（默认不执行）•`mongo_config` ：配置 mongo/ferretdb
* `mongo_cert` ：签发 mongo/ferretdb SSL证书
* `mongo_launch` ：启动 mongo/ferretdb 服务•`mongo_register`：将 mongo/ferretdb 注册到 Prometheus 监控中



------

## 监控

MONGO 模块提供了一个简单的监控面板：Mongo Overview

### Mongo Overview

Mongo Overview: Mongo/FerretDB 集群概览

这个监控面板提供了关于 FerretDB 的基本监控指标，因为 FerretDB 底层使用了 PostgreSQL，所以更多的监控指标，还请参考 PostgreSQL 本身的监控。

![](ferretdb-dashboard.png)



------

## 参数

`MONGO`[24] 模块中提供了9个相关的配置参数，如下表所示：

| 参数                    | 类型     | 级别  | 注释                                 |
|-----------------------|--------|-----|------------------------------------|
| `mongo_seq`           | int    | I   | mongo 实例号，必选身份参数                   |
| `mongo_cluster`       | string | C   | mongo 集群名，必选身份参数                   |
| `mongo_pgurl`         | pgurl  | C/I | mongo/ferretdb 底层使用的 PGURL 连接串，必选  |
| `mongo_ssl_enabled`   | bool   | C   | mongo/ferretdb 是否启用SSL？默认为 `false` |
| `mongo_listen`        | ip     | C   | mongo 监听地址，默认留控则监听所有地址             |
| `mongo_port`          | port   | C   | mongo 服务端口，默认使用 27017              |
| `mongo_ssl_port`      | port   | C   | mongo TLS 监听端口，默认使用 27018          |
| `mongo_exporter_port` | port   | C   | mongo exporter 端口，默认使用 9216        |
| `mongo_extra_vars`    | string | C   | MONGO 服务器额外环境变量，默认为空白字符串           |

