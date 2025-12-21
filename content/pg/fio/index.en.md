---
title: "Testing Disk Performance with FIO"
date: 2018-02-06
author: vonng
summary: >
  FIO is a convenient tool for testing disk I/O performance
tags: [PostgreSQL, PG-Admin, Performance]
---

> Author: [Vonng](https://vonng.com/en/)

FIO is an excellent disk performance testing tool. You can test disk read/write performance using the following commands.

```bash
fio --filename=/tmp/fio.data \
    -direct=1 \
    -iodepth=32 \
    -rw=randrw \
    --rwmixread=80 \
    -bs=4k \
    -size=1G \
    -numjobs=16 \
    -runtime=60 \
    -group_reporting \
    -name=randrw \
    --output=/tmp/fio_randomrw.txt \
    && unlink /tmp/fio.data
```

Testing raw disk (e.g., NVMe) performance (Dangerous! Don't run in production):

```bash
fio -name=8krandw  -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=8K    -size=100g -iodepth=256 -numjobs=8 -rw=randwrite             -group_reporting -time_based 
fio -name=8krandr  -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=8K    -size=100g -iodepth=256 -numjobs=8 -rw=randread              -group_reporting -time_based 
fio -name=8krandrw -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=8k    -size=100g -iodepth=256 -numjobs=8 -rw=randrw -rwmixwrite=30 -group_reporting -time_based 
fio -name=1mseqw   -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=write                 -group_reporting -time_based 
fio -name=1mseqr   -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=read                  -group_reporting -time_based 
fio -name=1mseqrw  -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=rw     -rwmixwrite=30 -group_reporting -time_based 
```

Testing filesystem performance (XFS): 4K, 8K, 1M sequential:

```bash
mkfs.xfs /dev/nvme0n1; mkdir -p /data1; mount -o noatime -o nodiratime -t xfs /dev/nvme0n1 /data1;

fio -name=4krandw  -runtime=120 -filename=/data1/rand.txt -ioengine=libaio -direct=1 -bs=4K    -size=100g -iodepth=256 -numjobs=8 -rw=randwrite             -group_reporting -time_based
fio -name=4krandr  -runtime=120 -filename=/data1/rand.txt -ioengine=libaio -direct=1 -bs=4K    -size=100g -iodepth=256 -numjobs=8 -rw=randread              -group_reporting -time_based
fio -name=4krandrw -runtime=120 -filename=/data1/rand.txt -ioengine=libaio -direct=1 -bs=4k    -size=100g -iodepth=256 -numjobs=8 -rw=randrw -rwmixwrite=30 -group_reporting -time_based

fio -name=8krandw  -runtime=120 -filename=/data1/rand.txt -ioengine=libaio -direct=1 -bs=8K    -size=100g -iodepth=256 -numjobs=8 -rw=randwrite             -group_reporting -time_based
fio -name=8krandr  -runtime=120 -filename=/data1/rand.txt -ioengine=libaio -direct=1 -bs=8K    -size=100g -iodepth=256 -numjobs=8 -rw=randread              -group_reporting -time_based
fio -name=8krandrw -runtime=120 -filename=/data1/rand.txt -ioengine=libaio -direct=1 -bs=8k    -size=100g -iodepth=256 -numjobs=8 -rw=randrw -rwmixwrite=30 -group_reporting -time_based

fio -name=1mseqw   -runtime=120 -filename=/data1/seq.txt  -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=write                 -group_reporting -time_based
fio -name=1mseqr   -runtime=120 -filename=/data1/seq.txt  -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=read                  -group_reporting -time_based
fio -name=1mseqrw  -runtime=120 -filename=/data1/seq.txt  -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=rw     -rwmixwrite=30 -group_reporting -time_based
```


When testing PostgreSQL-related I/O performance, focus should primarily be on 8KB random I/O. Consider the following parameter combinations.

Three dimensions: RW Ratio, Block Size, N Jobs for permutation and combination

* RW Ratio: Pure Read, Pure Write, rwmixwrite=80, rwmixwrite=20
* Block Size = 4KB (OS granular), 8KB (DB granular)
* N jobs: 1, 4, 8, 16, 32