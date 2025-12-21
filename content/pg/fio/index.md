---
title: "使用FIO测试磁盘性能"
date: 2018-02-06
author: 冯若航
summary: >
  FIO可以很方便地测试磁盘IO性能。
tags: [PostgreSQL, PG管理, 性能]
---

Fio是一个很好用的磁盘性能测试工具，可以通过以下命令测试磁盘的读写性能。

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

测试裸盘（例如NVMe）性能（危险！不要在生产运行）：

```bash
fio -name=8krandw  -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=8K    -size=100g -iodepth=256 -numjobs=8 -rw=randwrite             -group_reporting -time_based 
fio -name=8krandr  -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=8K    -size=100g -iodepth=256 -numjobs=8 -rw=randread              -group_reporting -time_based 
fio -name=8krandrw -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=8k    -size=100g -iodepth=256 -numjobs=8 -rw=randrw -rwmixwrite=30 -group_reporting -time_based 
fio -name=1mseqw   -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=write                 -group_reporting -time_based 
fio -name=1mseqr   -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=read                  -group_reporting -time_based 
fio -name=1mseqrw  -runtime=120 -filename=/dev/nvme0n1 -ioengine=libaio -direct=1 -bs=1024k -size=200g -iodepth=256 -numjobs=8 -rw=rw     -rwmixwrite=30 -group_reporting -time_based 
```

测试 FS 性能（xfs）： 4K, 8K, 1Mseq：

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


测试 PostgreSQL 相关的 IO 性能表现时，应当主要以 8KB 随机IO为主，可以考虑以下参数组合。

3个维度：RW Ratio, Block Size, N Jobs 进行排列组合

* RW Ratio:  Pure Read, Pure Write, rwmixwrite=80, rwmixwrite=20
* Block Size = 4KB (OS granular), 8KB (DB granular)
* N jobs: 1 , 4 , 8 , 16 ,32

