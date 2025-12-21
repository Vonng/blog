---
title: "Pigsty v0.9：GUI/CLI与日志集成"
linkTitle: "Pigsty v0.9 发布注记"
date: 2021-05-01
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/) | [发行注记](https://github.com/Vonng/pigsty/releases/tag/v0.9.0)）
summary: >
  Pigsty v0.9极大简化了安装流程，进行了大量日志相关改进，开发了命令行工具（Beta），并修复了一系列问题。
series: [Pigsty]
tags: [Pigsty]
---


----------------

## v0.9.0


### 新功能

* 一键安装模式：

  ```bash
  /bin/bash -c "$(curl -fsSL https://pigsty.cc/install)"
  ```

* 开发命令行工具 `pigsty-cli`封装常用Ansible命令，目前pigsty-cli处于Beta状态

* 使用Loki与Promtail收集日志：

  * 默认收集Postgres，Pgbouncer，Patroni日志
  * 新增部署脚本`infra-loki.yml` 与 `pgsql-promtail.yml`
  * 定义基于日志的监控指标
  * 使用Grafana制作日志相关可视化面板。

* 监控组件可以使用二进制安装，使用`files/get_bin.sh`下载监控二进制组件。

* 飞升模式：

  当集群元节点初始化完成后，可以使用`bin/upgrade`升级为动态Inventory

  使用pg-meta上的数据库代替YAML配置文件。


### 问题修复

* 集中修复日志相关问题：
  * 修复了HAProxy健康检查造成PG日志中大量 `connection reset by peer`的问题。
  * 修复了HAProxy健康检查造成Patroni日志中大量出现`Connect Reset` Exception的问题
  * 修复了Patroni日志时间戳格式，去除毫秒时间戳，附加完整时区信息。
  * 为`dbuser_monitor`配置1秒的`log_min_duration_statement`，避免监控查询出现在日志中。

* 重构Grafana角色
  * 在保持API不变的前提下重构Grafana角色。
  * 使用CDN下载预打包的Grafana插件，加速插件下载

* 其他问题修复
  * 修复了`pgbouncer-create-user` 未能正确处理 md5 密码的问题。
  * 完善了数据库与用户创建SQL模版中参数空置检查。
  * 修复了 NODE DNS配置时如果手工中断执行，DNS配置可能出错的问题。
  * 重构了Makefile快捷方式 Makefile 中的错别字


### 参数变更

* `node_disable_swap` 默认为 False，默认不会关闭SWAP。
* `node_sysctl_params` 不再有默认修改的系统参数。
*  `grafana_plugin` 的默认值`install` 现在意味着当插件缓存不存在时，从CDN下载。
* `repo_url_packages` 现在从 Pigsty CDN 下载额外的RPM包，解决墙内无法访问的问题。
* `proxy_env.no_proxy`现在将Pigsty CDN加入到NOPROXY列表中。
* `grafana_customize` 现在默认为`false`，启用意味着安装Pigsty Pro版UI（默认不开源所以不要启用）
* `node_admin_pk_current`，新增选项，启用后会将当前用户的`~/.ssh/id_rsa.pub`添加至管理员的Key中
* `loki_clean`：新增选项，安装Loki时是否清除现有数据
* `loki_data_dir`：新增选项，指明安装Loki时的数据目录
* `promtail_enabled` 是否启用Promtail日志收集服务？
* `promtail_clean` 是否在安装promtail时移除已有状态信息？
* `promtail_port` promtail使用的默认端口，默认为9080
* `promtail_status_file` 保存Promtail状态信息的文件位置
* `promtail_send_url` 用于接收日志的loki服务endpoint

