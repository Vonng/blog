---
title: "Pigsty v0.7：仅监控部署"
linkTitle: "Pigsty v0.7 发布注记"
date: 2021-03-01
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v0.7.0)）
summary: >
  Pigsty v0.7 新增了仅监控部署模式，改进了数据库与用户的供给接口。
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v0.7.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v070)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v0.7.0)

----------------

## v0.7.0

v0.7 针对**接入已有数据库实例**进行了改进，现在用户可以采用 **仅监控部署（Monly Deployment）** 模式使用Pigsty。同时新增了专用于管理数据库与用户、以及单独部署监控的剧本，并对数据库与用户的定义进行改进。


### 改动内容

#### Features

* [Monitor Only Deployment Support #25](https://github.com/Vonng/pigsty/issues/25)
* [Split monolith static monitor target file into per-cluster conf #36](https://github.com/Vonng/pigsty/issues/36)
* [Add create user playbook #29](https://github.com/Vonng/pigsty/issues/29)
* [Add create database playbook #28](https://github.com/Vonng/pigsty/issues/28)
* [Database provisioning interface enhancement #33](https://github.com/Vonng/pigsty/issues/33)
* [User provisioning interface enhancement #34](https://github.com/Vonng/pigsty/issues/34)

#### Bug Fix

* [Create extension with schema typo #32](https://github.com/Vonng/pigsty/issues/32)
* [pgbouncer reload with systemctl not work #35](https://github.com/Vonng/pigsty/issues/35)

#### API变更

**新增选项**

```yml
prometheus_sd_target: batch                   # batch|single    监控目标定义文件采用单体还是每个实例一个
exporter_install: none                        # none|yum|binary 监控Exporter的安装模式
exporter_repo_url: ''                         # 如果设置，这里的REPO连接会加入目标的Yum源中
node_exporter_options: '--no-collector.softnet --collector.systemd --collector.ntp --collector.tcpstat --collector.processes'                          # Node Exporter默认的命令行选项
pg_exporter_url: ''                           # 可选，PG Exporter监控对象的URL
pgbouncer_exporter_url: ''                    # 可选，PGBOUNCER EXPORTER监控对象的URL
```

**移除选项**

```yml
exporter_binary_install: false                 # 功能被 exporter_install 覆盖
```

**定义结构变更**

```yaml
pg_default_roles                               # 变化细节参考 用户管理。
pg_users                                       # 变化细节参考 用户管理。
pg_databases                                   # 变化细节参考 数据库管理。
```

**重命名选项**

```yml
pg_default_privilegs -> pg_default_privileges # 很明显这是一个错别字
```





## 仅监控模式

有时用户不希望使用Pigsty供给方案，只希望使用Pigsty监控系统管理现有PostgreSQL实例。

Pigsty提供了 [**仅监控部署（monly, monitor-only）**](https://pigsty.cc/zh/docs/deploy/integration/) 模式，剥离供给方案部分，可用于监控现有PostgreSQL集群。

仅监控模式的部署流程与标准模式大体上保持一致，但省略了很多步骤

- 在**元节点**上完成[基础设施初始化](/docs/pgsql/playbook)的部分与标准流程保持一致，仍然通过`./infra.yml`完成。
- 不需要在**数据库节点**上完成 **基础设施初始化**。
- 不需要在**数据库节点**上执行[数据库初始化](/docs/pgsql/playbook)的绝大多数任务，而是通过专用的`./pgsql-monitor.yml` 完成仅监控系统部署。
- 实际使用的配置项大大减少，只保留基础设施相关变量，与 [监控系统](/docs/pgsql/monitor/) 相关的少量变量。



## 数据库管理

[Database provisioning interface enhancement #33](https://github.com/Vonng/pigsty/issues/33)

### 旧接口定义

```yaml
pg_databases:                       # create a business database 'meta'
  - name: meta
    schemas: [meta]                 # create extra schema named 'meta'
    extensions: [{name: postgis}]   # create extra extension postgis
    parameters:                     # overwrite database meta's default search_path
      search_path: public, monitor
```

### 新的接口定义

```yaml
pg_databases:
  - name: meta                      # name is the only required field for a database
    owner: postgres                 # optional, database owner
    template: template1             # optional, template1 by default
    encoding: UTF8                  # optional, UTF8 by default
    locale: C                       # optional, C by default
    allowconn: true                 # optional, true by default, false disable connect at all
    revokeconn: false               # optional, false by default, true revoke connect from public # (only default user and owner have connect privilege on database)
    tablespace: pg_default          # optional, 'pg_default' is the default tablespace
    connlimit: -1                   # optional, connection limit, -1 or none disable limit (default)
    extensions:                     # optional, extension name and where to create
      - {name: postgis, schema: public}
    parameters:                     # optional, extra parameters with ALTER DATABASE
      enable_partitionwise_join: true
    pgbouncer: true                 # optional, add this database to pgbouncer list? true by default
    comment: pigsty meta database   # optional, comment string for database
```

### 接口变更

* Add new options: `template` , `encoding`, `locale`, `allowconn`, `tablespace`, `connlimit`
* Add new option `revokeconn`, which revoke connect privileges from public for this database
* Add `comment` field for database

### 数据库变更

在运行中集群中创建新数据库可以使用`pgsql-createdb.yml`剧本，在配置中定义完新数据库后，执行以下剧本。

```bash
./pgsql-createdb.yml -e pg_database=<your_new_database_name>
```

通过`-e pg_datbase=`告知需要创建的数据库名称，则该数据库即会被创建（或修改）。具体执行的命令参见集群主库`/pg/tmp/pg-db-{{ database.name}}.sql`文件。



## 用户管理

[User provisioning interface enhancement #34](https://github.com/Vonng/pigsty/issues/34)

### 旧接口定义

```yaml
pg_users:
  - username: test                  # example production user have read-write access
    password: test                  # example user's password
    options: LOGIN                  # extra options
    groups: [ dbrole_readwrite ]    # dborole_admin|dbrole_readwrite|dbrole_readonly
    comment: default test user for production usage
    pgbouncer: true                 # add to pgbouncer
```

### 新接口定义

```yaml
pg_users:
  # complete example of user/role definition for production user
  - name: dbuser_meta               # example production user have read-write access
    password: DBUser.Meta           # example user's password, can be encrypted
    login: true                     # can login, true by default (should be false for role)
    superuser: false                # is superuser? false by default
    createdb: false                 # can create database? false by default
    createrole: false               # can create role? false by default
    inherit: true                   # can this role use inherited privileges?
    replication: false              # can this role do replication? false by default
    bypassrls: false                # can this role bypass row level security? false by default
    connlimit: -1                   # connection limit, -1 disable limit
    expire_at: '2030-12-31'         # 'timestamp' when this role is expired
    expire_in: 365                  # now + n days when this role is expired (OVERWRITE expire_at)
    roles: [dbrole_readwrite]       # dborole_admin|dbrole_readwrite|dbrole_readonly
    pgbouncer: true                 # add this user to pgbouncer? false by default (true for production user)
    parameters:                     # user's default search path
      search_path: public
    comment: test user
```

### 接口变更

* `username` field rename to `name`

* `groups` field rename to `roles`

* `options` now split into separated configration entries: 

  `login`, `superuser`, `createdb`, `createrole`, `inherit`, `replication`,`bypassrls`,`connlimit`

* `expire_at` and `expire_in` options

* `pgbouncer` option for user is now `false` by default

### 用户管理

在运行中集群中创建新数据库可以使用`pgsql-createuser.yml`剧本，在配置中定义完新数据库后，执行以下剧本。

```bash
./pgsql-createuser.yml -e pg_user=<your_new_user_name>
```

通过`-e pg_user=`告知需要创建的数据库名称，则该数据库即会被创建（或修改）。具体执行的命令参见集群主库`/pg/tmp/pg-user-{{ user.name}}.sql`文件。


