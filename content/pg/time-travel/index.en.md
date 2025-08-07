---
title: "Incident Report: Patroni Failure Due to Time Travel"
date: 2021-02-22
author: "vonng"
summary: >
  Machine restarted due to failure, NTP service corrected PG time after PG startup, causing Patroni to fail to start.
tags: [PostgreSQL, PG Management, Incident Report]
---

Summary: Machine restarted due to failure, NTP service corrected PG time after PG startup, causing Patroni to fail to start.

The failure information in Patroni is shown as follows:

```
Process %s is not postmaster, too much difference between PID file start time %s and process start time %s
```

When patroni process start time and pid time are inconsistent, it assumes: postgres is not running.

If the two times differ by more than 30 seconds, patroni fails and cannot start.

The code that prints the error message is:

```python
start_time = int(self._postmaster_pid.get('start_time', 0))
if start_time and abs(self.create_time() - start_time) > 3:
    logger.info('Process %s is not postmaster, too much difference between PID file start time %s and process start time %s', self.pid, self.create_time(), start_time)
```

Also discovered a BUG in Patroni: https://github.com/zalando/patroni/issues/811 The two timestamps in the error message are reversed.

Lessons learned: NTP time synchronization is very important