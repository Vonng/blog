---
title: "Pigsty v0.8：服务供给"
linkTitle: "Pigsty v0.8 发布注记"
date: 2021-03-16
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v0.8.0)）
summary: >
  Pigsty v0.8 重做了服务供给部分，提供了集成外部负载均衡器的扩展接口。
series: [Pigsty]
tags: [Pigsty]
---


----------------

## v0.8.0

v0.8 针对 **服务（Service）** 接入部分进行了彻底的重做。现在除了默认的`primary`, `replica`服务外，用户可以自行定义新的服务。服务的接口可以支持多种不同的实现，例如L4 DPKG VIP可作为Haproxy的替代品与Pigsty集成。同时，针对用户反馈的一些问题进行了集中处理与改进。


### 改动内容

v0.8是供给方案定稿版本，此后供给系统的API将保持稳定。

#### API变更

原有`vip`与`haproxy`角色的所有配置项，现在迁移至`service`角色中。

```yaml
#------------------------------------------------------------------------------
# SERVICE PROVISION
#------------------------------------------------------------------------------
pg_weight: 100              # default load balance weight (instance level)

# - service - #
pg_services:                                  # how to expose postgres service in cluster?
  # primary service will route {ip|name}:5433 to primary pgbouncer (5433->6432 rw)
  - name: primary           # service name {{ pg_cluster }}_primary
    src_ip: "*"
    src_port: 5433
    dst_port: pgbouncer     # 5433 route to pgbouncer
    check_url: /primary     # primary health check, success when instance is primary
    selector: "[]"          # select all instance as primary service candidate

  # replica service will route {ip|name}:5434 to replica pgbouncer (5434->6432 ro)
  - name: replica           # service name {{ pg_cluster }}_replica
    src_ip: "*"
    src_port: 5434
    dst_port: pgbouncer
    check_url: /read-only   # read-only health check. (including primary)
    selector: "[]"          # select all instance as replica service candidate
    selector_backup: "[? pg_role == `primary`]"   # primary are used as backup server in replica service

  # default service will route {ip|name}:5436 to primary postgres (5436->5432 primary)
  - name: default           # service's actual name is {{ pg_cluster }}-{{ service.name }}
    src_ip: "*"             # service bind ip address, * for all, vip for cluster virtual ip address
    src_port: 5436          # bind port, mandatory
    dst_port: postgres      # target port: postgres|pgbouncer|port_number , pgbouncer(6432) by default
    check_method: http      # health check method: only http is available for now
    check_port: patroni     # health check port:  patroni|pg_exporter|port_number , patroni by default
    check_url: /primary     # health check url path, / as default
    check_code: 200         # health check http code, 200 as default
    selector: "[]"          # instance selector
    haproxy:                # haproxy specific fields
      maxconn: 3000         # default front-end connection
      balance: roundrobin   # load balance algorithm (roundrobin by default)
      default_server_options: 'inter 3s fastinter 1s downinter 5s rise 3 fall 3 on-marked-down shutdown-sessions slowstart 30s maxconn 3000 maxqueue 128 weight 100'

  # offline service will route {ip|name}:5438 to offline postgres (5438->5432 offline)
  - name: offline           # service name {{ pg_cluster }}_replica
    src_ip: "*"
    src_port: 5438
    dst_port: postgres
    check_url: /replica     # offline MUST be a replica
    selector: "[? pg_role == `offline` || pg_offline_query ]"         # instances with pg_role == 'offline' or instance marked with 'pg_offline_query == true'
    selector_backup: "[? pg_role == `replica` && !pg_offline_query]"  # replica are used as backup server in offline service

pg_services_extra: []        # extra services to be added

# - haproxy - #
haproxy_enabled: true                         # enable haproxy among every cluster members
haproxy_reload: true                          # reload haproxy after config
haproxy_policy: roundrobin                    # roundrobin, leastconn
haproxy_admin_auth_enabled: false             # enable authentication for haproxy admin?
haproxy_admin_username: admin                 # default haproxy admin username
haproxy_admin_password: admin                 # default haproxy admin password
haproxy_exporter_port: 9101                   # default admin/exporter port
haproxy_client_timeout: 3h                    # client side connection timeout
haproxy_server_timeout: 3h                    # server side connection timeout

# - vip - #
vip_mode: none                                # none | l2 | l4
vip_reload: true                              # whether reload service after config
# vip_address: 127.0.0.1                      # virtual ip address ip (l2 or l4)
# vip_cidrmask: 24                            # virtual ip address cidr mask (l2 only)
# vip_interface: eth0                         # virtual ip network interface (l2 only)
```

**新增选项**

```yml
# - localization - #
pg_encoding: UTF8                             # default to UTF8
pg_locale: C                                  # default to C
pg_lc_collate: C                              # default to C
pg_lc_ctype: en_US.UTF8                       # default to en_US.UTF8

pg_reload: true                               # reload postgres after hba changes
vip_mode: none                                # none | l2 | l4
vip_reload: true                              # whether reload service after config
```

**移除选项**

```bash
haproxy_check_port                            # Haproxy相关参数已经被Service定义覆盖
haproxy_primary_port
haproxy_replica_port
haproxy_backend_port
haproxy_weight
haproxy_weight_fallback
vip_enabled                                   # vip_enabled参数被vip_mode覆盖
```



#### 服务管理

`pg_services` 与 `pg_services_extra` 定义了集群中的**服务**，每一个服务的定义结构如下例所示：

一个服务必须指定以下内容：

* **名称**：服务的完整名称以数据库集群名为前缀，以`service.name`为后缀，通过`-`连接。例如在`pg-test`集群中`name=primary`的服务，其完整服务名称为`pg-test-primary`。

* **端口**：在Pigsty中，服务默认采用NodePort的形式对外暴露，因此暴露端口为必选项。但如果使用外部负载均衡服务接入方案，您也可以通过其他的方式区分服务。

* **选择器**：选择器指定了服务的成员，采用JMESPath的形式，从所有集群实例成员中筛选变量。默认的`[]`选择器会选取所有的集群成员。

  此外`selector_backup`会选择或标记用于backup的实例列表（当集群中所有其他成员失效时方才接管服务）

```yaml
  # default service will route {ip|name}:5436 to primary postgres (5436->5432 primary)
  - name: default           # service's actual name is {{ pg_cluster }}-{{ service.name }}
    src_ip: "*"             # service bind ip address, * for all, vip for cluster virtual ip address
    src_port: 5436          # bind port, mandatory
    dst_port: postgres      # target port: postgres|pgbouncer|port_number , pgbouncer(6432) by default
    check_method: http      # health check method: only http is available for now
    check_port: patroni     # health check port:  patroni|pg_exporter|port_number , patroni by default
    check_url: /primary     # health check url path, / as default
    check_code: 200         # health check http code, 200 as default
    selector: "[]"          # instance selector
    haproxy:                # haproxy specific fields
      maxconn: 3000         # default front-end connection
      balance: roundrobin   # load balance algorithm (roundrobin by default)
      default_server_options: 'inter 3s fastinter 1s downinter 5s rise 3 fall 3 on-marked-down shutdown-sessions slowstart 30s maxconn 3000 maxqueue 128 weight 100'
```







### 数据库管理

数据库现在可以对locale的细分选项：`lc_ctype`与`lc_collate`分别进行指定。支持这一功能的主要原因是PG的扩展插件`pg_trgm`需要在`lc_ctype!=C`的环境中才能正常支持中文。

#### 旧接口定义

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

#### 新的接口定义

```yaml
pg_databases:
  - name: meta                      # name is the only required field for a database
    # owner: postgres                 # optional, database owner
    # template: template1             # optional, template1 by default
    # encoding: UTF8                # optional, UTF8 by default , must same as template database, leave blank to set to db default
    # locale: C                     # optional, C by default , must same as template database, leave blank to set to db default
    # lc_collate: C                 # optional, C by default , must same as template database, leave blank to set to db default
    # lc_ctype: C                   # optional, C by default , must same as template database, leave blank to set to db default
    allowconn: true                 # optional, true by default, false disable connect at all
    revokeconn: false               # optional, false by default, true revoke connect from public # (only default user and owner have connect privilege on database)
    # tablespace: pg_default          # optional, 'pg_default' is the default tablespace
    connlimit: -1                   # optional, connection limit, -1 or none disable limit (default)
    extensions:                     # optional, extension name and where to create
      - {name: postgis, schema: public}
    parameters:                     # optional, extra parameters with ALTER DATABASE
      enable_partitionwise_join: true
    pgbouncer: true                 # optional, add this database to pgbouncer list? true by default
    comment: pigsty meta database   # optional, comment string for database
```




