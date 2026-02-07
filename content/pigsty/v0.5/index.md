---
title: "Pigsty v0.5：数据库定制模板"
linkTitle: "Pigsty v0.5 发布注记"
date: 2020-12-26
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v0.5.0)）
summary: >
  Pigsty v0.5.0 对数据库内部的定制模板进行了大幅改进，允许您用声明式的方法管理用户，角色，数据库，权限，扩展以及模式。
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v0.5.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v050)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v0.5.0)

## v0.5.0

### 大纲

* Pigsty官方[文档站](http://pigsty.cc/)正式上线！
* 添加了数据库模板的定制支持，用户可以通过配置文件定制所需的数据库内部对象。
* 对默认[访问控制](https://pigsty.cc/docs/setup/security)模型进行了改进
* 重构了HBA管理的逻辑，现在将由Pigsty替代Patroni直接负责生成HBA
* 将Grafana监控系统的供给方案从sqlite改为JSON文件静态Provision
* 将`pg-cluster-replication`面板加入Pigsty开源免费套餐。
* 最新的经过测试的离线安装包：[pkg.tgz](https://github.com/Vonng/pigsty/releases/download/v0.5.0/pkg.tgz) (v0.5)

### 定制数据库

您是否烦恼过单实例多租户的问题？比如总有研发拿着PostgreSQL当MySQL使，明明是一个Schema就能解决的问题，非要创建一个新的数据库出来，在一个实例中创建出几十个不同的DB。
不要忧伤，不要心急。Pigsty已经提供数据库内部对象的Provision方案，您可以轻松地在配置文件中指定所需的数据库内对象，包括：

* 角色
  * 用户/角色名
  * 密码
  * 用户属性
  * 用户备注
  * 用户所属的权限组
* 数据库
  * 属主
  * 额外的模式
  * 额外的扩展插件
  * 数据库级的自定义配置参数
* 数据库
  * 属主
  * 额外的模式
  * 额外的扩展插件
  * 数据库级的自定义配置参数
* 默认权限
  * 默认情况下这里配置的权限会应用至所有由 超级用户 和 管理员用户创建的对象上。
* 默认扩展
  * 所有新创建的业务数据库都会安装有这些默认扩展
* 默认模式
  * 所有新创建的业务数据库都会创建有这些默认的模式

配置样例

```yaml
# 通常是每个DB集群配置的变量
pg_users:
  - username: test
    password: test
    comment: default test user
    groups: [ dbrole_readwrite ]    # dborole_admin|dbrole_readwrite|dbrole_readonly
pg_databases:                       # create a business database 'test'
  - name: test
    extensions: [{name: postgis}]   # create extra extension postgis
    parameters:                     # overwrite database meta's default search_path
      search_path: public,monitor

# 通常是整个环境统一配置的全局变量
# - system roles - #
pg_replication_username: replicator           # system replication user
pg_replication_password: DBUser.Replicator    # system replication password
pg_monitor_username: dbuser_monitor           # system monitor user
pg_monitor_password: DBUser.Monitor           # system monitor password
pg_admin_username: dbuser_admin               # system admin user
pg_admin_password: DBUser.Admin               # system admin password

# - default roles - #
pg_default_roles:
  - username: dbrole_readonly                 # sample user:
    options: NOLOGIN                          # role can not login
    comment: role for readonly access         # comment string

  - username: dbrole_readwrite                # sample user: one object for each user
    options: NOLOGIN
    comment: role for read-write access
    groups: [ dbrole_readonly ]               # read-write includes read-only access

  - username: dbrole_admin                    # sample user: one object for each user
    options: NOLOGIN BYPASSRLS                # admin can bypass row level security
    comment: role for object creation
    groups: [dbrole_readwrite,pg_monitor,pg_signal_backend]

  # NOTE: replicator, monitor, admin password are overwritten by separated config entry
  - username: postgres                        # reset dbsu password to NULL (if dbsu is not postgres)
    options: SUPERUSER LOGIN
    comment: system superuser

  - username: replicator
    options: REPLICATION LOGIN
    groups: [pg_monitor, dbrole_readonly]
    comment: system replicator

  - username: dbuser_monitor
    options: LOGIN CONNECTION LIMIT 10
    comment: system monitor user
    groups: [pg_monitor, dbrole_readonly]

  - username: dbuser_admin
    options: LOGIN BYPASSRLS
    comment: system admin user
    groups: [dbrole_admin]

  - username: dbuser_stats
    password: DBUser.Stats
    options: LOGIN
    comment: business read-only user for statistics
    groups: [dbrole_readonly]


# object created by dbsu and admin will have their privileges properly set
pg_default_privilegs:
  - GRANT USAGE                         ON SCHEMAS   TO dbrole_readonly
  - GRANT SELECT                        ON TABLES    TO dbrole_readonly
  - GRANT SELECT                        ON SEQUENCES TO dbrole_readonly
  - GRANT EXECUTE                       ON FUNCTIONS TO dbrole_readonly
  - GRANT INSERT, UPDATE, DELETE        ON TABLES    TO dbrole_readwrite
  - GRANT USAGE,  UPDATE                ON SEQUENCES TO dbrole_readwrite
  - GRANT TRUNCATE, REFERENCES, TRIGGER ON TABLES    TO dbrole_admin
  - GRANT CREATE                        ON SCHEMAS   TO dbrole_admin
  - GRANT USAGE                         ON TYPES     TO dbrole_admin

# schemas
pg_default_schemas: [monitor]

# extension
pg_default_extensions:
  - { name: 'pg_stat_statements',  schema: 'monitor' }
  - { name: 'pgstattuple',         schema: 'monitor' }
  - { name: 'pg_qualstats',        schema: 'monitor' }
  - { name: 'pg_buffercache',      schema: 'monitor' }
  - { name: 'pageinspect',         schema: 'monitor' }
  - { name: 'pg_prewarm',          schema: 'monitor' }
  - { name: 'pg_visibility',       schema: 'monitor' }
  - { name: 'pg_freespacemap',     schema: 'monitor' }
  - { name: 'pg_repack',           schema: 'monitor' }
  - name: postgres_fdw
  - name: file_fdw
  - name: btree_gist
  - name: btree_gin
  - name: pg_trgm
  - name: intagg
  - name: intarray

# postgres host-based authentication rules
pg_hba_rules:
  - title: allow meta node password access
    role: common
    rules:
      - host    all     all                         10.10.10.10/32      md5

  - title: allow intranet admin password access
    role: common
    rules:
      - host    all     +dbrole_admin               10.0.0.0/8          md5
      - host    all     +dbrole_admin               172.16.0.0/12       md5
      - host    all     +dbrole_admin               192.168.0.0/16      md5

  - title: allow intranet password access
    role: common
    rules:
      - host    all             all                 10.0.0.0/8          md5
      - host    all             all                 172.16.0.0/12       md5
      - host    all             all                 192.168.0.0/16      md5

  - title: allow local read-write access (local production user via pgbouncer)
    role: common
    rules:
      - local   all     +dbrole_readwrite                               md5
      - host    all     +dbrole_readwrite           127.0.0.1/32        md5

  - title: allow read-only user (stats, personal) password directly access
    role: replica
    rules:
      - local   all     +dbrole_readonly                               md5
      - host    all     +dbrole_readonly           127.0.0.1/32        md5
pg_hba_rules_extra: []

# pgbouncer host-based authentication rules
pgbouncer_hba_rules:
  - title: local password access
    role: common
    rules:
      - local  all          all                                     md5
      - host   all          all                     127.0.0.1/32    md5

  - title: intranet password access
    role: common
    rules:
      - host   all          all                     10.0.0.0/8      md5
      - host   all          all                     172.16.0.0/12   md5
      - host   all          all                     192.168.0.0/16  md5
pgbouncer_hba_rules_extra: []

```


### 数据库模板

* [pg-init-template.sql](https://github.com/Vonng/pigsty/blob/master/roles/postgres/templates/pg-init-template.sql) 用于初始化`template1`数据的脚本模板
* [pg-init-business.sql](https://github.com/Vonng/pigsty/blob/master/roles/postgres/templates/pg-init-business.sql) 用于初始化其他业务数据库的脚本模板


### 权限模型

v0.5 改善了默认的权限模型，主要是针对单实例多租户的场景进行优化，并收紧权限控制。

* 撤回了普通业务用户对非所属数据库的默认`CONNECT`权限
* 撤回了非管理员用户对所属数据库的默认`CREATE`权限
* 撤回了所有用户在`public`模式下的默认创建权限。


## 供给方式

原先Pigsty采用直接拷贝Grafana自带的grafana.db的方式完成监控系统的初始化。
这种方式虽然简单粗暴管用，但不适合进行精细化的版本控制管理。在v0.5中，Pigsty采用了Grafana API完成了监控系统面板供给的工作。
您所需的就是在`grafana_url`中填入带有用户名密码的Grafana URL。
因此，监控系统可以背方便地添加至已有的Grafana中。