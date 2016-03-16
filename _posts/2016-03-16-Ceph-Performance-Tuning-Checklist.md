---
layout: post
title: "Ceph Performance Tuning Checklist"
tagline : "Ceph Performance Tuning Checklist"
description: "Ceph Performance Tuning Checklist"
category: "Ceph"
tags: [ceph, performance, storage]
---
{% include JB/setup %}

Here's my checklist of ceph performance tuning. It can be used for deployment or performance troubleshooting. I borrowed from [the great framework posted by RaySun](http://xiaoquqi.github.io/blog/2015/06/28/ceph-performance-optimization-summary/).

### Hardware Layer

About the server nodes
  
  * Choose proper CPU, memory (e.g. frequency, size, etc) for different work nodes of Ceph, such as OSD, MON, MDS. If you use erasure code, it needs more CPU resource.
  * Enable HT and VT in BIOS. Optionally shut off NUMA and power-saving.
  * Number of nodes
  * How many disks for each storage node

About the storage

  * Choose proper storage for example disk rotation rate, disk internface (SAS, SATA), or SSD, with respect to cost/GB vs throughput vs latency.
  * Use SSD for journal
  * Choose between using JBOD (recommended) or RAID, local disk (recommended) or SAN.
  * Whether or to use what HBA/RAID card.
  * RAID card use write-through or write-back. Whether it has battery or capacitor

About the network

  * NIC card count and bandwidth, for different type of Ceph work nodes.
  * Enable jumbo frame if your switch supports it
  * The bandwidth of internal cluster network should be no less than 10Gb.

### OS Layer

  * Enable NTP time synchronization. Ceph is sensitive to time.
  * It is recommend to put OS, OSD, journal each in a differnet disk, io at least a different partition
  * Make pid max and file limit large enough.
  * Set vm.swappiness to zero. Enable 
  * Enable kernel read_ahead.
  * Set the kernel block IO scheudler, noop for SSD, deadline for SATA/SAS disks. [Increase the block IO queue size](http://www.monperrus.net/martin/scheduler+queue+size+and+resilience+to+heavy+IO).
  * [Shut-off disk controller cache](http://www.cnblogs.com/wuhuiyuan/p/4648725.html), because it doesn't have battery/capacitor to protect from power outage.

### Filesystem Layer

  * FS type: XFS or BTRFS or EXT4 (XFS is recommended, BTFS is good but not production ready)
  * [FS block size, and inode size, inode count](http://www.cnblogs.com/wuhuiyuan/p/linux-filesystem-inodes.html). Beware of file count vs average file size.
  * FS parameters: [set noatime, nobarrier](http://www.phoronix.com/scan.php?page=article&item=ext4_linux35_tuning&num=1)
  * [Larger FS journal size](http://m.blog.chinaunix.net/uid-522675-id-4665059.html)
  * If SSD, add discard/trim to FS parameter

### Ceph Layer

  * OSD per disk. Monitor on separated node.
  * Put journal in separated OSD disk if you can.
  * CGroup pin each OSD to its CPU core.
  * Proper PG count. Briefly, PGs = round2((Total_number_of_OSD * 100) / max_replication_count). See [pgcalc](http://ceph.com/pgcalc/).
  * Scrubbing, if enabled, may severely impact performance.
  * Enable tcmalloc and adjust max thread cache, see [hustcat's blog](http://hustcat.github.io/ceph-performance-journal-and-tcmalloc/).
  * Choose to use erasure code or replica.
  * Enlarge almost everything in Ceph config: max open files, buffer sizes, flush intervals, ... a lot. See [RaySun's blog](http://xiaoquqi.github.io/blog/2015/06/28/ceph-performance-optimization-summary/).
  * Increase redundant parallel reads with erasure coding. Recovery throttling. Enable bucket sharding. See [Yahoo's](https://yahooeng.tumblr.com/post/116391291701/yahoo-cloud-object-store-object-storage-at).
  * OSD requires about 1 GB memory for per 1TB storage.
  * CRUSH map configurations to improve reliability by reducing number of copysets. See [UStack's blog](https://www.ustack.com/blog/build-block-storage-service/#Coepy_Set) and [this paper](https://www.usenix.org/conference/atc13/technical-sessions/presentation/cidon).

### Benchmarking Tools

  * Ceph perf counter, which is embedded in code
  * Benchmark commands: `rados bench`, `iperf`, `dd`, `fio`, `cbt`, `ceph osd perf`. See [Ceph wiki](http://tracker.ceph.com/projects/ceph/wiki/Benchmark_Ceph_Cluster_Performance).
  * Tracking commands: top, iowait, iostat, blktrace, debugfs.
  * Watch for "slow xxx" in ceph's log.
  * [Project CeTune](http://docslide.us/technology/ceph-day-beijing-cetune-a-framework-of-profile-and-tune-ceph-performance.html) the Ceph profiling and tuning framework. 
  * [Linux Performance Analysis in 60,000 Milliseconds](http://techblog.netflix.com/2015/11/linux-performance-analysis-in-60s.html) and [Netflix at Velocity 2015: Linux Performance Tools](http://techblog.netflix.com/2015/08/netflix-at-velocity-2015-linux.html)

### Troubleshooting Cases

  * Rebalancing, if currently carrying on, may severely impact performance.
  * If a disk is broken or deteriorated, the performance of whole cluster may be severely impacted.
  * If the snapshot chain is too long, it may becomes slow.
  * RAID card failure results in great IOPS decrease, see [this blog](http://www.cnblogs.com/wuhuiyuan/p/4649776.html).

### References

  * Ceph性能优化总结(v0.94): http://xiaoquqi.github.io/blog/2015/06/28/ceph-performance-optimization-summary/
  * One Ceph, Two ways of thinking: http://documents.tips/technology/ceph-day-beijing-one-ceph-two-ways-of-thinking-between-customers-and-developers.html
  * 几个 Ceph 性能优化的新方法和思路（2015 SH Ceph Day 参后感）: http://www.cnblogs.com/sammyliu/p/4905726.html
  * Scheduler queue size and resilience to heavy IO: http://www.monperrus.net/martin/scheduler+queue+size+and+resilience+to+heavy+IO
  * Ceph性能调优——Journal与tcmalloc: http://hustcat.github.io/ceph-performance-journal-and-tcmalloc/
  * 打造高性能高可靠块存储系统: https://www.ustack.com/blog/build-block-storage-service/
  * linux系统数据落盘之细节: http://www.cnblogs.com/wuhuiyuan/p/4648725.html
  * 海量小文件存储与Ceph实践: http://www.cnblogs.com/wuhuiyuan/p/4651698.html
  * Linux Performance Analysis in 60,000 Milliseconds: http://techblog.netflix.com/2015/11/linux-performance-analysis-in-60s.html
  * Netflix at Velocity 2015: Linux Performance Tools: http://techblog.netflix.com/2015/08/netflix-at-velocity-2015-linux.html
  * EXT4 File-System Tuning Benchmarks: http://www.phoronix.com/scan.php?page=article&item=ext4_linux35_tuning&num=1
  * xfs文件系统使用总结: http://m.blog.chinaunix.net/uid-522675-id-4665059.html
  * Ceph: Open Source Storage Software Optimizations on Intel® Architecture for Cloud Workloads: http://www.slideshare.net/LarryCover/ceph-open-source-storage-software-optimizations-on-intel-architecture-for-cloud-workloads
  * Yahoo Cloud Object Store - Object Storage at Exabyte Scale: https://yahooeng.tumblr.com/post/116391291701/yahoo-cloud-object-store-object-storage-at
  * BENCHMARK CEPH CLUSTER PERFORMANCE: http://tracker.ceph.com/projects/ceph/wiki/Benchmark_Ceph_Cluster_Performance
  * Ceph Benchmarks: http://www.sebastien-han.fr/blog/2012/08/26/ceph-benchmarks/