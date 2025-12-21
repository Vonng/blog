---
title: "Pigsty v0.6：架构增强"
linkTitle: "Pigsty v0.6 发布注记"
date: 2021-02-19
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v0.6.0)）
summary: >
  Pigsty v0.6 对数据库供给方案进行了大量改进
series: [Pigsty]
tags: [Pigsty]
---

> [**GitHub Release**](https://github.com/pgsty/pigsty/releases/tag/v0.6.0) | [**发布注记**](https://pigsty.cc/docs/releasenote/#v060)

[![](featured.jpg)](https://github.com/pgsty/pigsty/releases/tag/v0.6.0)

----------------

## v0.6.0

v0.6 对数据库供给方案进行了修改与调整，根据用户的反馈添加了一系列实用功能与修正。针对监控系统的移植性进行优化，便于与其他外部数据库供给方案对接，例如阿里云MyBase。


### BUG修复

* 修复了新版本Patroni重启后会重置PG HBA的问题
* 修复了PG Overview Dashboard标题中的别字
* 修复了沙箱集群`pg-test`的默认主库，原来为`pg-test-2`，应当为`pg-test-1`
* 修复了过时代码注释

### 功能改进

* 改造Prometheus与监控供给方式
  * 允许在无基础设施的情况下对已有PG集群进行监控部署，便于监控系统与其他供给方案集成。[#11](https://github.com/Vonng/pigsty/issues/11)
  * 基于Inventory渲染所有监控对象的静态列表，用于静态服务发现。[#11](https://github.com/Vonng/pigsty/issues/11)
  * Prometheus添加了静态对象模式，用于替代动态服务发现，集中进行身份管理[#11](https://github.com/Vonng/pigsty/issues/11)
  * 监控Exporter现在添加了`service_registry`选项，Consul服务注册变为可选项 [#13](https://github.com/Vonng/pigsty/issues/13)
  * Exporter现在可以通过拷贝二进制的方式直接安装：`exporter_binary_install`，[#14](https://github.com/Vonng/pigsty/issues)
  * Exporter现在具有`xxx_enabled`选项，控制是否启用该组件。
* Haproxy供给重构与改进  [#8](https://github.com/Vonng/pigsty/issues/8)
  * 新增了全局HAProxy管理界面导航，默认域名`h.pigsty`
  * 允许将主库加入只读服务集中，当集群中所有从库宕机时自动承接读流量。 [#8](https://github.com/Vonng/pigsty/issues/8)
  * 允许位Haproxy实例管理界面启用认证 `haproxy_admin_auth_enabled`
  * 允许通过配置项调整每个服务对应后端的流量权重. [#10](https://github.com/Vonng/pigsty/issues/10)
* 访问控制模型改进。[#7](https://github.com/Vonng/pigsty/issues/7)
  * 添加了默认角色`dbrole_offline`，用于慢查询，ETL，交互式查询场景。
  * 修改默认HBA规则，允许`dbrole_offline`分组的用户访问`pg_role == 'offline'`及`pg_offline_query == true`的实例。
* 软件更新 Release v0.6
  * PostgreSQL 13.2
  * Prometheus 2.25
  * PG Exporter 0.3.2
  * Node Exporter 1.1
  * Consul 1.9.3
  * 更新默认PG源：PostgreSQL现在默认使用浙江大学的镜像，加速下载安装

### **接口变更**

**新增选项**

```yaml
service_registry: consul                      # 服务注册机制：none | consul | etcd | both
prometheus_options: '--storage.tsdb.retention=30d'  # prometheus命令行选项
prometheus_sd_method: consul                  # Prometheus使用的服务发现机制：static|consul
prometheus_sd_interval: 2s                    # Prometheus服务发现刷新间隔
pg_offline_query: false                       # 设置后将允许dbrole_offline角色连接与查询该实例
node_exporter_enabled: true                   # 设置后将安装配置Node Exporter
pg_exporter_enabled: true                     # 设置后将安装配置PG Exporter
pgbouncer_exporter_enabled: true              # 设置后将安装配置Pgbouncer Exporter
dcs_disable_purge: false                      # 双保险，强制 dcs_exists_action = abort 避免误删除DCS实例
pg_disable_purge: false                       # 双保险，强制 pg_exists_action = abort 避免误删除数据库实例
haproxy_weight: 100                           # 配置实例的相对负载均衡权重
haproxy_weight_fallback: 1                    # 配置集群主库在只读服务中的相对权重
```

**移除选项**

```yaml
prometheus_metrics_path                       # 与 exporter_metrics_path 重复
prometheus_retention                          # 功能被 prometheus_options 覆盖
```

