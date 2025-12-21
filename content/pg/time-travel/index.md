---
title: "故障档案：时间回溯导致的Patroni故障"
linkTitle: "故障档案：NTP/Patroni"
date: 2021-02-22
author: 冯若航
summary: >
  机器因为故障重启，NTP服务在PG启动后修复了PG的时间，导致Patroni无法启动。
tags: [PostgreSQL, PG管理, 故障档案]
---


摘要：机器因为故障重启，NTP服务在PG启动后修复了PG的时间，导致 Patroni 无法启动。

Patroni中的故障信息如下所示：

```
Process %s is not postmaster, too much difference between PID file start time %s and process start time %s
```

patroni 进程启动时间和pid时间不一致。就会认为：postgres is not running。

两个时间相差超过30秒。patroni 就尿了，启动不了了。


打印错误信息的代码为：

```python
start_time = int(self._postmaster_pid.get('start_time', 0))
if start_time and abs(self.create_time() - start_time) > 3:
    logger.info('Process %s is not postmaster, too much difference between PID file start time %s and process start time %s', self.pid, self.create_time(), start_time)
```


同时，发现了Patroni里的一个BUG：https://github.com/zalando/patroni/issues/811 错误信息里两个时间戳打反了。

经验与教训： NTP 时间同步是非常重要的