---
title: "Linux 常用统计 CLI 工具"
date: 2017-09-07
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)）
summary: >
  top, free, vmstat, iostat：四大常用 CLI 工具命令速查
tags: [PostgreSQL,PG管理,工具]
---

- [`top`](#top)
- [`free`](#free)
- [`vmstat`](#vmstat)
- [`iostat`](#iostat)


-----------------------

## `top`

显示Linux任务

### 摘要

- 按下空格或回车强制刷新
- 使用`h`打开帮助
- 使用`l,t,m`收起摘要部分。
- 使用`d`修改刷新周期
- 使用`z`开启颜色高亮
- 使用`u`列出指定用户的进程
- 使用`<>`来改变排序列
- 使用`P`按CPU使用率排序
- 使用`M`按驻留内存大小排序
- 使用`T`按累计时间排序

### 批处理模式

`-b`参数可以用于批处理模式，配合`-n`参数指定批次数目。同时`-d`参数可以指定批次的间隔时间

例如获取机器当前的负载使用情况，以0.1秒为间隔获取三次，获取最后一次的CPU摘要。

```bash
$ top -bn3 -d0.1 | grep Cpu | tail -n1
Cpu(s):  4.1%us,  1.0%sy,  0.0%ni, 94.8%id,  0.0%wa,  0.0%hi,  0.1%si,  0.0%st
```

### 输出格式

`top`的输出分为两部分，上面几行是系统摘要，下面是进程列表，两者通过一个空行分割。下面是`top`命令的输出样例：

```
top - 12:11:01 up 401 days, 19:17,  2 users,  load average: 1.12, 1.26, 1.40
Tasks: 1178 total,   3 running, 1175 sleeping,   0 stopped,   0 zombie
Cpu(s):  5.4%us,  1.7%sy,  0.0%ni, 92.5%id,  0.1%wa,  0.0%hi,  0.4%si,  0.0%st
Mem:  396791756k total, 389547376k used,  7244380k free,   263828k buffers
Swap: 67108860k total,        0k used, 67108860k free, 366252364k cached

   PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
  5094 postgres  20   0 37.2g 829m 795m S 14.2  0.2   0:04.11 postmaster
  5093 postgres  20   0 37.2g 926m 891m S 13.2  0.2   0:04.96 postmaster
165359 postgres  20   0 37.2g 4.0g 4.0g S 12.6  1.1   0:44.93 postmaster
 93426 postgres  20   0 37.2g 6.8g 6.7g S 12.2  1.8   1:32.94 postmaster
  5092 postgres  20   0 37.2g 856m 818m R 11.2  0.2   0:04.21 postmaster
 67634 root      20   0  569m 520m  328 S 11.2  0.1 140720:15 haproxy
 93429 postgres  20   0 37.2g 8.7g 8.7g S 11.2  2.3   2:12.23 postmaster
129653 postgres  20   0 37.2g 6.8g 6.7g S 11.2  1.8   1:27.92 postmaster
```

### 摘要部分

摘要默认由三个部分，共计五行组成：

* 系统运行时间，平均负载，共计一行（`l`切换内容）
* 任务、CPU状态，各一行（`t`切换内容）
* 内存使用，Swap使用，各一行（`m`切换内容）

**系统运行时间和平均负载**

```
top - 12:11:01 up 401 days, 19:17,  2 users,  load average: 1.12, 1.26, 1.40
```

- 当前时间：`12:11:01`
- 系统已运行的时间：`up 401 days`
- 当前登录用户的数量：`2 users`
- 相应最近5、10和15分钟内的平均负载：`load average: 1.12, 1.26, 1.40`。

> Load表示操作系统的负载，即，当前运行的任务数目。而load average表示一段时间内平均的load，也就是过去一段时间内平均有多少个任务在运行。注意Load与CPU利用率并不是一回事。

**任务**

```
Tasks: 1178 total,   3 running, 1175 sleeping,   0 stopped,   0 zombie
```

第二行显示的是任务或者进程的总结。进程可以处于不同的状态。这里显示了全部进程的数量。除此之外，还有正在运行、睡眠、停止、僵尸进程的数量（僵尸是一种进程的状态）。

**CPU状态**

```bash
Cpu(s):  5.4%us,  1.7%sy,  0.0%ni, 92.5%id,  0.1%wa,  0.0%hi,  0.4%si,  0.0%st
```

下一行显示的是CPU状态。 这里显示了不同模式下的所占CPU时间的百分比。这些不同的CPU时间表示:

- us, user： 运行(未调整优先级的) 用户进程的CPU时间
- sy，system: 运行内核进程的CPU时间
- ni，niced：运行已调整优先级的用户进程的CPU时间
- id，idle：空闲CPU时间
- wa，IO wait: 用于等待IO完成的CPU时间
- hi：处理硬件中断的CPU时间
- si: 处理软件中断的CPU时间
- st：虚拟机被hypervisor偷去的CPU时间（如果当前处于一个虚拟机内，宿主机消耗的CPU处理时间）。

**内存使用**

```
Mem:  396791756k total, 389547376k used,  7244380k free,   263828k buffers
Swap: 67108860k total,        0k used, 67108860k free, 366252364k cached
```

* 内存部分：全部可用内存、已使用内存、空闲内存、缓冲内存。
* SWAP部分：全部、已使用、空闲和缓冲交换空间。


### 进程部分

进程部分默认会显示一些关键信息

```
   PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
  5094 postgres  20   0 37.2g 829m 795m S 14.2  0.2   0:04.11 postmaster
  5093 postgres  20   0 37.2g 926m 891m S 13.2  0.2   0:04.96 postmaster
165359 postgres  20   0 37.2g 4.0g 4.0g S 12.6  1.1   0:44.93 postmaster
 93426 postgres  20   0 37.2g 6.8g 6.7g S 12.2  1.8   1:32.94 postmaster
  5092 postgres  20   0 37.2g 856m 818m R 11.2  0.2   0:04.21 postmaster
 67634 root      20   0  569m 520m  328 S 11.2  0.1 140720:15 haproxy
 93429 postgres  20   0 37.2g 8.7g 8.7g S 11.2  2.3   2:12.23 postmaster
129653 postgres  20   0 37.2g 6.8g 6.7g S 11.2  1.8   1:27.92 postmaster
```

- **PID**：进程ID，进程的唯一标识符
- **USER**：进程所有者的实际用户名。
- **PR**：进程的调度优先级。这个字段的一些值是'rt'。这意味这这些进程运行在实时态。
- **NI**：进程的nice值（优先级）。越小的值意味着越高的优先级。
- **VIRT**：进程使用的虚拟内存。
- **RES**：驻留内存大小。驻留内存是任务使用的非交换物理内存大小。
- **SHR**：SHR是进程使用的共享内存。
- **S**这个是进程的状态。它有以下不同的值:

- D - 不可中断的睡眠态。
- R – 运行态
- S – 睡眠态
- T – Trace或Stop
- Z – 僵尸态

- **%CPU**：自从上一次更新时到现在任务所使用的CPU时间百分比。
- **%MEM**：进程使用的可用物理内存百分比。
- **TIME+**：任务启动后到现在所使用的全部CPU时间，单位为百分之一秒。
- **COMMAND**：运行进程所使用的命令。

### Linux进程的状态

```c
static const char * const task_state_array[] = {
  "R (running)", /* 0 */
  "S (sleeping)", /* 1 */
  "D (disk sleep)", /* 2 */
  "T (stopped)", /* 4 */
  "t (tracing stop)", /* 8 */
  "X (dead)", /* 16 */
  "Z (zombie)", /* 32 */
};
```

- `R (TASK_RUNNING)`，可执行状态。实际运行与`Ready`在Linux都算做Running状态
- `S (TASK_INTERRUPTIBLE)`，可中断的睡眠态，进程等待事件，位于等待队列中。
- `D (TASK_UNINTERRUPTIBLE)`，不可中断的睡眠态，无法响应异步信号，例如硬件操作，内核线程
- `T (TASK_STOPPED | TASK_TRACED)`，暂停状态或跟踪状态，由SIGSTOP或断点触发
- `Z (TASK_DEAD)`，子进程退出后，父进程还没有来收尸，留下`task_structure`的进程就处于这种状态。













-----------------------

## `free`

显示系统的内存使用情况

```bash
free -b | -k | -m | -g | -h -s delay  -a -l
```

* 其中`-b | -k | -m | -g | -h `可用于控制显示大小时的单位（字节，KB,MB,GB，自动适配）
* `-s`可以指定轮询周期，`-c`指定轮询次数。

### 输出样例

```bash
$ free -m
             total       used       free     shared    buffers     cached
Mem:        387491     379383       8107      37762        182     348862
-/+ buffers/cache:      30338     357153
Swap:        65535          0      65535
```

* 这里，总内存有378GB，使用370GB，空闲8GB。三者存在`total=used+free`的关系。共享内存占36GB。
* buffers与cache由操作系统分配管理，用于提高I/O性能，其中Buffer是写入缓冲，而Cache是读取缓存。这一行表示，应用程序**已使用**的`buffers/cached`，以及理论上**可使用**的`buffers/cache`。
    `-/+ buffers/cache:      30338     357153`
* 最后一行显示了SWAP信息，总的SWAP空间，实际使用的SWAP空间，以及可用的SWAP空间。只要没有用到SWAP（used = 0），就说明内存空间仍然够用。

    
### 数据来源

free实际上是通过`cat /proc/meminfo`获取信息的。

详细信息：https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/s2-proc-meminfo

```bash
$ cat /proc/meminfo
MemTotal:       396791752 kB	# 总可用RAM, 物理内存减去内核二进制与保留位
MemFree:         7447460 kB		# 系统可用物理内存
Buffers:          186540 kB		# 磁盘快的临时存储大小
Cached:         357066928 kB	# 缓存
SwapCached:            0 kB		# 曾移入SWAP又移回内存的大小
Active:         260698732 kB	# 最近使用过，如非强制不会回收的内存。
Inactive:       112228764 kB	# 最近没怎么用过的内存，可能会回收
Active(anon):   53811184 kB		# 活跃的匿名内存(不与具体文件关联)
Inactive(anon):   532504 kB		# 不活跃的匿名内存
Active(file):   206887548 kB	# 活跃的文件缓存
Inactive(file): 111696260 kB	# 不活跃的文件缓存
Unevictable:           0 kB		# 不可淘汰的内存
Mlocked:               0 kB		# 被钉在内存中
SwapTotal:      67108860 kB		# 总SWAP
SwapFree:       67108860 kB		# 可用SWAP
Dirty:            115852 kB		# 被写脏的内存
Writeback:             0 kB		# 回写磁盘的内存
AnonPages:      15676608 kB		# 匿名页面
Mapped:         38698484 kB		# 用于mmap的内存，例如共享库
Shmem:          38668836 kB		# 共享内存
Slab:            6072524 kB		# 内核数据结构使用内存
SReclaimable:    5900704 kB		# 可回收的slab
SUnreclaim:       171820 kB		# 不可回收的slab
KernelStack:       25840 kB		# 内核栈使用的内存
PageTables:      2480532 kB		# 页表大小
NFS_Unstable:          0 kB		# 发送但尚未提交的NFS页面
Bounce:                0 kB		# bounce buffers
WritebackTmp:          0 kB
CommitLimit:    396446012 kB
Committed_AS:   57195364 kB
VmallocTotal:   34359738367 kB
VmallocUsed:     6214036 kB
VmallocChunk:   34353427992 kB
HardwareCorrupted:     0 kB
AnonHugePages:         0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
DirectMap4k:        5120 kB
DirectMap2M:     2021376 kB
DirectMap1G:    400556032 kB
```

其中，free与`/proc/meminfo`中指标的对应关系为：

```
total	= (MemTotal + SwapTotal)
used	= (total - free - buffers - cache)
free	= (MemFree + SwapFree)
shared	= Shmem
buffers	= Buffers
cache	= Cached
buffer/cached = Buffers + Cached
```

### 清理缓存

可以通过以下命令强制清理缓存：

```bash
$ sync # flush fs buffers
$ echo 1 > /proc/sys/vm/drop_caches	# drop page cache
$ echo 2 > /proc/sys/vm/drop_caches	# drop dentries & inode
$ echo 3 > /proc/sys/vm/drop_caches	# drop all
```











-----------------------

## `vmstat`


汇报虚拟内存统计信息

### 摘要

```bash
vmstat [-a] [-n] [-t] [-S unit] [delay [ count]]
vmstat [-s] [-n] [-S unit]
vmstat [-m] [-n] [delay [ count]]
vmstat [-d] [-n] [delay [ count]]
vmstat [-p disk partition] [-n] [delay [ count]]
vmstat [-f]
vmstat [-V]
```

最常用的用法是：

```bash
vmstat <delay> <count>
```

例如`vmstat 1 10`就是以1秒为间隔，采样10次内存统计信息。

### 样例输出

```bash
$ vmstat 1 4 -S M
procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 3  0      0   7288    170 344210    0    0   158   158    0    0  2  1 97  0  0
 5  0      0   7259    170 344228    0    0  7680 13292 38783 36814  6  1 93  0  0
 3  0      0   7247    170 344246    0    0  8720 21024 40584 39686  6  1 93  0  0
 1  0      0   7233    170 344255    0    0  6800 24404 39461 36984  6  1 93  0  0
```

```
Procs
    r: 等待运行的进程数目
    b: 处于不可中断睡眠状态的进程数(Block)
Memory
    swpd: 使用的交换区大小，大于0则说明内存过小
    free: 空闲内存
    buff: 缓冲区内存
    cache: 页面缓存
    inact: 不活跃内存 (-a 选项)
    active: 活跃内存 (-a 选项)
Swap
    si: 每秒从磁盘中换入的内存 (/s).
    so: 每秒从换出到磁盘的内存 (/s).
IO
    bi: 从块设备每秒收到的块数目 (blocks/s).
    bo: 向块设备每秒发送的快数目 (blocks/s).
System
    in: 每秒中断数，包括时钟中断
    cs: 每秒上下文切换数目
CPU
    总CPU时间的百分比
    us: 用户态时间 (包括nice的时间)
    sy: 内核态时间
    id: 空闲时间（在2.5.41前包括等待IO的时间）
    wa: 等待IO的时间（在2.5.41前包括在id里）
    st: 空闲时间（在2.6.11前没有）
```

### 数据来源

从下面三个文件中提取信息：

- `/proc/meminfo`
- `/proc/stat`
- `/proc/*/stat`











-----------------------

## `iostat`

汇报IO相关统计信息

### 摘要

```bash
iostat [ -c ] [ -d ] [ -N ] [ -n ] [ -h ] [ -k | -m ] [ -t ] [ -V ] [ -x ] [ -y ] [ -z ] [ -j { ID | LABEL | PATH | UUID | ... } [ device [...] | ALL ] ] [ device [...] | ALL ] [ -p [ device [,...] | ALL ] ] [interval [ count ] ]
```

默认情况下iostat会打印cpu信息和磁盘io信息，使用`-d`参数只显示IO部分，使用`-x`打印更多信息。样例输出：

```
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           5.77    0.00    1.31    0.07    0.00   92.85

Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
sdb               0.00         0.00         0.00          0          0
sda               0.00         0.00         0.00          0          0
dfa            5020.00     15856.00     35632.00      15856      35632
dm-0              0.00         0.00         0.00          0          0
```

### 常用选项

- 使用`-d`参数只显示IO部分的信息，而`-c`参数则只显示CPU部分的信息。
- 使用`-x`会打印更详细的扩展信息
- 使用`-k`会使用KB替代块数目作为部分数值的单位，`-m`则使用MB。

### 输出说明

不带`-x`选项默认会为每个设备打印5列：

- tps：该设备每秒的传输次数。（多个逻辑请求可能会合并为一个IO请求，传输量未知）
-kB_read/s：每秒从设备读取的数据量；kB_wrtn/s：每秒向设备写入的数据量；kB_read：读取的总数据量；kB_wrtn：写入的总数量数据量；这些单位都为Kilobytes，这是使用`-k`参数的情况。默认则以块数为单位。

带有`-x`选项后，会打印更多信息：

- rrqm/s：每秒这个设备相关的读取请求有多少被Merge了（当系统调用需要读取数据的时候，VFS将请求发到各个FS，如果FS发现不同的读取请求读取的是相同Block的数据，FS会将这个请求合并Merge）；
- wrqm/s：每秒这个设备相关的写入请求有多少被Merge了。
- r/s 与 w/s：（合并后）每秒读取/写入请求次数
- rsec/s 与 wsec/s：每秒读取/写入扇区的数目
- avgrq-sz：请求的平均大小（以扇区计）
- avgqu-sz：平均请求队列长度
- await：每一个IO请求的处理的平均时间（单位是毫秒）
- r_await/w_await：读/写的平均响应时间。
- %util：设备的带宽利用率，IO时间占比。在统计时间内所有处理IO时间。一般该参数是100%表示设备已经接近满负荷运行了。


### 常用方法

收集 `/dev/dfa` 的IO信息，按kB计算，每秒一次，连续 10 次。

```bash
iostat -dxk /dev/dfa 1 10
```

### 数据来源

其实是从下面几个文件中提取信息的：

```
/proc/stat contains system statistics.
/proc/uptime contains system uptime.
/proc/partitions contains disk statistics (for pre 2.5 kernels that have been patched).
/proc/diskstats contains disks statistics (for post 2.5 kernels).
/sys contains statistics for block devices (post 2.5 kernels).
/proc/self/mountstats contains statistics for network filesystems.
/dev/disk contains persistent device names.
```




