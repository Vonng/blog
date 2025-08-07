---
title: "Common Linux Statistics CLI Tools"
date: 2017-09-07
author: "vonng"
summary: >
  top, free, vmstat, iostat: Quick reference for four commonly used CLI tools
tags: [PostgreSQL, PG Management, Tools]
---

- [`top`](#top)
- [`free`](#free)
- [`vmstat`](#vmstat)
- [`iostat`](#iostat)

-----------------------

## `top`

Display Linux tasks

### Summary

- Press space or enter to force refresh
- Use `h` to open help
- Use `l,t,m` to collapse summary sections
- Use `d` to modify refresh interval
- Use `z` to enable color highlighting
- Use `u` to list processes for specific user
- Use `<>` to change sort column
- Use `P` to sort by CPU usage
- Use `M` to sort by resident memory size
- Use `T` to sort by cumulative time

### Batch Mode

The `-b` parameter can be used for batch mode, combined with `-n` parameter to specify number of batches. The `-d` parameter can specify interval time between batches.

For example, to get current machine load usage, obtaining three times at 0.1 second intervals, getting CPU summary from the last time:

```bash
$ top -bn3 -d0.1 | grep Cpu | tail -n1
Cpu(s):  4.1%us,  1.0%sy,  0.0%ni, 94.8%id,  0.0%wa,  0.0%hi,  0.1%si,  0.0%st
```

### Output Format

`top` output is divided into two parts: system summary in the top few lines, process list below, separated by a blank line. Here's sample output from `top` command:

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

### Summary Section

Summary consists of three parts by default, totaling five lines:

* System runtime, average load, one line total (`l` toggles content)
* Tasks, CPU status, one line each (`t` toggles content)
* Memory usage, Swap usage, one line each (`m` toggles content)

**System Runtime and Average Load**

```
top - 12:11:01 up 401 days, 19:17,  2 users,  load average: 1.12, 1.26, 1.40
```

- Current time: `12:11:01`
- System uptime: `up 401 days`
- Number of currently logged in users: `2 users`
- Average load for the last 5, 10, and 15 minutes: `load average: 1.12, 1.26, 1.40`

> Load represents operating system load, i.e., number of currently running tasks. Load average represents average load over a period of time, i.e., how many tasks were running on average over a past period. Note that Load is not the same as CPU utilization.

**Tasks**

```
Tasks: 1178 total,   3 running, 1175 sleeping,   0 stopped,   0 zombie
```

The second line shows task or process summary. Processes can be in different states. This shows total number of processes. Additionally, it shows numbers of running, sleeping, stopped, zombie processes (zombie is a process state).

**CPU Status**

```bash
Cpu(s):  5.4%us,  1.7%sy,  0.0%ni, 92.5%id,  0.1%wa,  0.0%hi,  0.4%si,  0.0%st
```

The next line shows CPU status. This displays percentage of CPU time in different modes:

- us, user: CPU time for running (non-priority-adjusted) user processes
- sy, system: CPU time for running kernel processes
- ni, niced: CPU time for running priority-adjusted user processes
- id, idle: Idle CPU time
- wa, IO wait: CPU time spent waiting for IO completion
- hi: CPU time for handling hardware interrupts
- si: CPU time for handling software interrupts
- st: CPU time stolen by hypervisor from virtual machine (if currently in a virtual machine, CPU processing time consumed by host machine)

**Memory Usage**

```
Mem:  396791756k total, 389547376k used,  7244380k free,   263828k buffers
Swap: 67108860k total,        0k used, 67108860k free, 366252364k cached
```

* Memory section: total available memory, used memory, free memory, buffer memory
* SWAP section: total, used, free, and buffer swap space

### Process Section

Process section displays some key information by default:

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

- **PID**: Process ID, unique identifier for the process
- **USER**: Actual username of the process owner
- **PR**: Scheduling priority of the process. Some values in this field are 'rt', meaning these processes run in real-time state
- **NI**: Nice value (priority) of the process. Smaller values mean higher priority
- **VIRT**: Virtual memory used by the process
- **RES**: Resident memory size. Resident memory is the non-swap physical memory size used by the task
- **SHR**: Shared memory used by the process
- **S**: Process state. It has different values:

- D - Uninterruptible sleep state
- R – Running state  
- S – Sleep state
- T – Trace or Stop
- Z – Zombie state

- **%CPU**: Percentage of CPU time used by task since last update
- **%MEM**: Percentage of available physical memory used by the process
- **TIME+**: Total CPU time used by task since startup, in hundredths of seconds
- **COMMAND**: Command used to run the process

### Linux Process States

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

- `R (TASK_RUNNING)`: Runnable state. Both actually running and `Ready` are considered Running state in Linux
- `S (TASK_INTERRUPTIBLE)`: Interruptible sleep state, process waits for events, located in wait queue
- `D (TASK_UNINTERRUPTIBLE)`: Uninterruptible sleep state, cannot respond to asynchronous signals, e.g., hardware operations, kernel threads
- `T (TASK_STOPPED | TASK_TRACED)`: Stopped state or traced state, triggered by SIGSTOP or breakpoints
- `Z (TASK_DEAD)`: After child process exits, parent process hasn't cleaned up yet, leaving `task_structure` processes in this state

-----------------------

## `free`

Display system memory usage

```bash
free -b | -k | -m | -g | -h -s delay  -a -l
```

* `-b | -k | -m | -g | -h` can control units when displaying sizes (bytes, KB, MB, GB, auto-adapt)
* `-s` can specify polling interval, `-c` specifies polling count

### Sample Output

```bash
$ free -m
             total       used       free     shared    buffers     cached
Mem:        387491     379383       8107      37762        182     348862
-/+ buffers/cache:      30338     357153
Swap:        65535          0      65535
```

* Here, total memory is 378GB, used 370GB, free 8GB. The three have relationship `total=used+free`. Shared memory occupies 36GB.
* buffers and cache are allocated and managed by the operating system to improve I/O performance, where Buffer is write buffer and Cache is read cache. This line shows application **used** `buffers/cached` and theoretically **available** `buffers/cache`.
    `-/+ buffers/cache:      30338     357153`
* The last line shows SWAP information: total SWAP space, actually used SWAP space, and available SWAP space. As long as SWAP isn't used (used = 0), memory space is still sufficient.

### Data Source

free actually gets information through `cat /proc/meminfo`.

Details: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/s2-proc-meminfo

```bash
$ cat /proc/meminfo
 MemTotal:       396791752 kB	# Total available RAM, physical memory minus kernel binary and reserved bits
MemFree:         7447460 kB		# System available physical memory
Buffers:          186540 kB		# Temporary storage size for disk blocks
Cached:         357066928 kB	# Cache
SwapCached:            0 kB		# Size moved to SWAP then back to memory
Active:         260698732 kB	# Recently used, won't be reclaimed unless forced
Inactive:       112228764 kB	# Recently unused memory, might be reclaimed
Active(anon):   53811184 kB		# Active anonymous memory (not associated with specific files)
Inactive(anon):   532504 kB		# Inactive anonymous memory
Active(file):   206887548 kB	# Active file cache
Inactive(file): 111696260 kB	# Inactive file cache
Unevictable:           0 kB		# Non-evictable memory
Mlocked:               0 kB		# Memory locked in memory
SwapTotal:      67108860 kB		# Total SWAP
SwapFree:       67108860 kB		# Available SWAP
Dirty:            115852 kB		# Dirty memory
Writeback:             0 kB		# Memory being written back to disk
AnonPages:      15676608 kB		# Anonymous pages
Mapped:         38698484 kB		# Memory used for mmap, e.g., shared libraries
Shmem:          38668836 kB		# Shared memory
Slab:            6072524 kB		# Memory used by kernel data structures
SReclaimable:    5900704 kB		# Reclaimable slab
SUnreclaim:       171820 kB		# Non-reclaimable slab
KernelStack:       25840 kB		# Memory used by kernel stack
PageTables:      2480532 kB		# Page table size
NFS_Unstable:          0 kB		# NFS pages sent but not yet committed
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

The correspondence between free and `/proc/meminfo` indicators:

```
total	= (MemTotal + SwapTotal)
used	= (total - free - buffers - cache)
free	= (MemFree + SwapFree)
shared	= Shmem
buffers	= Buffers
cache	= Cached
buffer/cached = Buffers + Cached
```

### Clear Cache

You can force clear cache with the following commands:

```bash
$ sync # flush fs buffers
$ echo 1 > /proc/sys/vm/drop_caches	# drop page cache
$ echo 2 > /proc/sys/vm/drop_caches	# drop dentries & inode
$ echo 3 > /proc/sys/vm/drop_caches	# drop all
```

-----------------------

## `vmstat`

Report virtual memory statistics

### Summary

```bash
vmstat [-a] [-n] [-t] [-S unit] [delay [ count]]
vmstat [-s] [-n] [-S unit]
vmstat [-m] [-n] [delay [ count]]
vmstat [-d] [-n] [delay [ count]]
vmstat [-p disk partition] [-n] [delay [ count]]
vmstat [-f]
vmstat [-V]
```

Most commonly used:

```bash
vmstat <delay> <count>
```

For example, `vmstat 1 10` samples memory statistics 10 times at 1-second intervals.

### Sample Output

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
    r: Number of processes waiting to run
    b: Number of processes in uninterruptible sleep state (Block)
Memory
    swpd: Amount of swap space used, >0 indicates insufficient memory
    free: Free memory
    buff: Buffer memory
    cache: Page cache
    inact: Inactive memory (-a option)
    active: Active memory (-a option)
Swap
    si: Memory swapped in from disk per second (/s)
    so: Memory swapped out to disk per second (/s)
IO
    bi: Blocks received per second from block devices (blocks/s)
    bo: Blocks sent per second to block devices (blocks/s)
System
    in: Interrupts per second, including clock interrupts
    cs: Context switches per second
CPU
    Percentage of total CPU time
    us: User time (including nice time)
    sy: Kernel time
    id: Idle time (included IO wait time before 2.5.41)
    wa: IO wait time (included in id before 2.5.41)
    st: Idle time (not available before 2.6.11)
```

### Data Source

Extracts information from these three files:

- `/proc/meminfo`
- `/proc/stat`
- `/proc/*/stat`

-----------------------

## `iostat`

Report IO-related statistics

### Summary

```bash
iostat [ -c ] [ -d ] [ -N ] [ -n ] [ -h ] [ -k | -m ] [ -t ] [ -V ] [ -x ] [ -y ] [ -z ] [ -j { ID | LABEL | PATH | UUID | ... } [ device [...] | ALL ] ] [ device [...] | ALL ] [ -p [ device [,...] | ALL ] ] [interval [ count ] ]
```

By default iostat prints CPU and disk IO information. Use `-d` parameter to show only IO section, use `-x` to print more information. Sample output:

```
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           5.77    0.00    1.31    0.07    0.00   92.85

Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
sdb               0.00         0.00         0.00          0          0
sda               0.00         0.00         0.00          0          0
dfa            5020.00     15856.00     35632.00      15856      35632
dm-0              0.00         0.00         0.00          0          0
```

### Common Options

- Use `-d` parameter to show only IO section information, while `-c` parameter shows only CPU section information
- Use `-x` to print more detailed extended information
- Use `-k` to use KB instead of block count as unit for some values, `-m` uses MB

### Output Description

Without `-x` option, defaults to printing 5 columns for each device:

- tps: Transfers per second for this device. (Multiple logical requests may be merged into one IO request, transfer amount unknown)
- kB_read/s: Data read from device per second; kB_wrtn/s: Data written to device per second; kB_read: Total data read; kB_wrtn: Total data written; These units are all Kilobytes when using `-k` parameter. Default uses block count as unit.

With `-x` option, prints more information:

- rrqm/s: How many read requests related to this device were merged per second (when system calls need to read data, VFS sends requests to various FS, if FS finds different read requests reading the same Block data, FS will merge these requests)
- wrqm/s: How many write requests related to this device were merged per second
- r/s and w/s: (After merging) read/write requests per second
- rsec/s and wsec/s: Sectors read/written per second
- avgrq-sz: Average request size (in sectors)
- avgqu-sz: Average request queue length
- await: Average time for each IO request processing (in milliseconds)
- r_await/w_await: Average response time for read/write
- %util: Device bandwidth utilization, IO time percentage. All time processing IO during statistics time. Generally when this parameter reaches 100%, device is close to full load operation.

### Common Usage

Collect IO information for `/dev/dfa`, calculate in kB, once per second, 10 consecutive times:

```bash
iostat -dxk /dev/dfa 1 10
```

### Data Source

Actually extracts information from these files:

```
/proc/stat contains system statistics.
/proc/uptime contains system uptime.
/proc/partitions contains disk statistics (for pre 2.5 kernels that have been patched).
/proc/diskstats contains disks statistics (for post 2.5 kernels).
/sys contains statistics for block devices (post 2.5 kernels).
/proc/self/mountstats contains statistics for network filesystems.
/dev/disk contains persistent device names.
```