---
title: "Pigsty v0.4：PG13 与文档站"
linkTitle: "Pigsty v0.4 发布注记"
date: 2020-12-14
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v0.4.0)）
summary: >
  Pigsty 第二个公开测试版 v0.4 现已正式发行，支持 PG13，并对监控系统进行了整体升级改造。
series: [Pigsty]
tags: [Pigsty]
---


----------------

## v0.4.0

第二个公开测试版v0.4现已正式发行

Pigsty v0.4 对监控系统进行了整体升级改造，精心挑选了10个面板作为标准的Pigsty开源内容。同时，针对Grafana 7.3的不兼容升级进行了大量适配改造工作。使用升级的`pg_exporter v0.3.1`作为默认指标导出器，调整了监控报警规则的监控面板连接。


### Pigsty开源版

Pigsty开源版选定了以下10个Dashboard作为开源内容。其他Dashboard作为可选的商业支持内容提供。

  * PG Overview
  * PG Cluster
  * PG Service
  * PG Instance
  * PG Database
  * PG Query
  * PG Table
  * PG Table Catalog
  * PG Table Detail
  * Node

尽管进行了少量阉割，这10个监控面板所涵盖的内容仍然可以吊打所有同类软件。
  
### 软件升级

Pigsty v0.4进行了大量软件适配工作，包括：

* Upgrade to PostgreSQL 13.1, Patroni 2.0.1-4, add citus to repo.
* Upgrade to [`pg_exporter 0.3.1`](https://github.com/Vonng/pg_exporter/releases/tag/v0.3.1)
* Upgrade to Grafana 7.3, Ton's of compatibility work
* Upgrade to prometheus 2.23, with new UI as default
* Upgrade to consul 1.9

### 其他改进

* Update prometheus alert rules
* Fix alertmanager info links
* Fix bugs and typos.
* add a simple backup script

### 离线安装包

* v0.4的离线安装包（CentOS 7.8）已经可以从Github下载：[pkg.tgz](https://github.com/Vonng/pigsty/releases/download/v0.4.0/pkg.tgz)

