---
layout: post
title: "Recent Paper Reading: EC, PMem, B+tree Concurrency, ML for DB"
tagline : "Recent Paper Reading: EC, PMem, B+tree Concurrency, ML for DB"
description: "Recent Paper Reading: EC, PMem, B+tree Concurrency, ML for DB"
category: "Paper Reading"
tags: [storage, paper, database]
---
{% include JB/setup %}

Search good / (very) interesting / (very) useful, to find recommended papers. Search "question" to find feedback.


Misc papers about Erasure Coding

```
1. Erasure Coding Stripping
    1. RAID implements Erasure Coding by striping
       https://data-flair.training/blogs/hadoop-hdfs-erasure-coding/
    2. EC striped layout vs contiguous layout 
       https://blog.cloudera.com/introduction-to-hdfs-erasure-coding-in-apache-hadoop/
    3. Understanding System Characteristics of Online Erasure Coding on Scalable, Distributed and Large-Scale SSD Array Systems
       https://arxiv.org/pdf/1709.05365.pdf
    4. Storage tiering and erasure coding in Ceph (SCaLE13x)
       https://www.slideshare.net/sageweil1/20150222-scale-sdc-tiering-and-ec
        1. "Zero-fill shards (logically_ in partial tail stripe"
    5. KV-Store/Storage with Erasure Coding
       https://nan01ab.github.io/2019/05/EC.html
    
    6. "Partial stripe write", "EC partial writes", "parity update" in RAID
        1. PARIX: Speculative Partial Writes in Erasure-Coded Systems
           https://www.usenix.org/conference/atc17/technical-sessions/presentation/li-huiba
            1. Speculative Partial Writing Technology in Erasure Code Storage System
               https://www.programmersought.com/article/41305135697/
                1. useful. this paper is for Speculative Parity Logging to handle Partial Writes
                2. highlights
                    1. "incremental coding based on the difference between the new and old data"
                    2. "Parity Logging with Reserved Space: Towards Efficient Updates and Recovery in Erasure-coded Clustered Storage"
                       https://www.usenix.org/sites/default/files/conference/protected-files/fast14_slides_chan.pdf

        2. Correlation-Aware Stripe Organization for Efficient Writes in Erasure-Coded Storage: Algorithms and Evaluation
        
        3. "Partial stripe write" - Figure 2-5 - uploaded by John K. Ousterhout
           https://www.researchgate.net/figure/5-Partial-stripe-write-A-write-that-does-not-fill-a-whole-stripe-requires-a-parity_fig2_220439180
        
        4. Always-On Erasure Coding - Datrium
           https://cdna.datrium.com/wp-content/uploads/2017/11/02104439/Erasure-Coding-WP.pdf
           1. "Controllers use writecoalescing to combine small writes to adjacent logical blocks into a single large write in order to convert partial stripe writes into full stripe writes"

        5. EXPLORATION OF ERASURE-CODED STORAGE SYSTEMS FOR HIGH PERFORMANCE, RELIABILITY, AND INTER-OPERABILITY
           https://core.ac.uk/download/pdf/51295522.pdf
            1. "[42] proposes to reduce the parity update overhead .."

3. PARIX: Speculative Partial Writes in Erasure-Coded Systems    [2017, 15 refs]
   https://www.usenix.org/conference/atc17/technical-sessions/presentation/li-huiba
    1. interesting paper. use logging to absort ranodm updates to data. and a method to handle partial update to EC group
    2. highlights
        1. partital updates in EC group usually use Parity Logging
            1. I.e. convert updates to Parity to journal appends behind
            2. why Data symbols not use logging? because logging makes addresses non-consecutive, less favorable for reading
            3. Parity Updates, existing approaches
                1. RAID-based approaches
                    1. reconstruct writes
                    2. read-modfiy wriets
                    3. discussion: many existing approaches are for single host deploy, they are expensive on distribtued schema
                2. Delta-based approaches
                    1. Full-overwrite
                    2. Full-logging
                    3. Parity logging
        2. this paper, compared to Parity Logging, parity writes data delta rather than parity update delta to journal
            1. this saves every data change needs to calculate parity delta which needs to read original data block
            2. speculative, data server sends original data block to parity server to calculate parity delta
            3. questions
                1. how to maintain the distributed transaction / consistency across the data servers and parity servers
                2. Figure 2 shows only one, but there are many data symbols, together their update can bloat parity size many times
    n. related
        1. Parity Logging with Reserved Space: Towards Efficient Updates and Recovery in Erasure-coded Clustered Storage    [FAST14, 2014, 61 refs]
           https://www.usenix.org/system/files/conference/fast14/fast14-paper_chan.pdf
            1. instead of parity logging to a shard journal, it allocate space behind each block, to put the parity delta
                1. this needs further to predict and shrink the reserved space. using exponential smoothing
            2. questions
                1. the reserved space can take so much storage overhead ..
                2. the shrink operation is expensive that needs to move all the data

4. 一文带你看透基于LSM-tree的NoSQL系统优化方向
   https://zhuanlan.zhihu.com/p/351241814
    1. very good. the author surveyed/summarized all remarkable LSM-tree literatures/papers with good review quality
    2. highlights
        1. Thinking about LSM-tree write amplification
            1. Question: The paper style (listed in this article) write amplification only includes a key from start to drop to the bottom level. What happens after that is omitted. A key1 can further be rewritten, due to key2 at bottom level gots an rewrite in the same file
            2. Analyzing Azure Storage Table layer GC/compaction
                1. New key write won't trigger GC
                2. Deletion triggers GC, Old key update triggers GC
                3. When deletion/update reaches GC threshold (e.g. a%) of an extent -> (100-a)% data rewrite.
                4. Suppose all writes are deletion/update, and they evenly distributed to all extents, it's a%->(100-a)% write amplification
            3. question: Why LSM-tree needs multiple layers?
                1. question, even it's all new key write, no delete/update, typical LSM-tree still triggers compaction due to layer full, causing write amplification?
                2. For, Azure Storage Table layer GC/compaction, it's possible to use different extent sizes. upper layer use smaller extent size, so less amplification upon GC rewrite, colder/bottom layer uses larger extent size.
                    1. it should also work with GC/compaction with different data temperature related layering stuff
                    2. don't omit the scan cost
                3. so question, is LSM-tree really need to have the layer structure?
                    1. anyway, the original says different layers reflect hotness and lifecycle, they can even reside on different media, e.g. memory, SSD, HDD
        2. interesting (papers)
            1. TRIAD - hot keys keep in memory rather than flush to disk, to reduce write amplification
            2. WriteBuffer(WB) Tree - B+tree with per node buffer, like Be-tree
            3. leveling vs tiering - non-overlapping key range inside a level, index/bloomfilter skipping
            4. 降低合并后buffer cache 的失效率, and cache回填 ; LSbM-tree
            5. Pipelined, 预读和后写 in compaction
            6. 使用Skiplist能够一定程度得加速点读，并且运训在range场景并发seek来加速查找性能
            7. FD-tree: 通过级联的方式来提升读性能 而非Bloom-filter, Level2中的page数据，很多page和一个Level1的page指针链接起来
            8. Wisckey: Key value 分离. HashKV improve Wisckey GC scan by partitioning
            9. NoFTL-KV: Open-channel SSD, ZNS, 将闪存垃圾回收机制和LSM-tree的compaction 集成到一块，一起由FTL调度 从而减少写放大
            10. Monkey的研究中发现应该为lower level的sst构建bloom filter分配更多的位数来降低误报率，higher level的sst文件中分配更少的位数
            11. Dostoevsky lazy-leveling合并策略
            12. Mutant 在云存储中优化了LSM-tree的数据放置策略, 将热点sstable文件放置到高速存储设备之中
            13. RocksDB支持了一个RMW(read-modify-write)的新特性，实际很多应用需要针对已经存在的数据执行RMW操作
            14. Facebook 使用LSM-tree的初衷是因为它优于B+-tree的空间利用率。B+-tree的 in-place updates会导致大量的内存碎片，而LSM-tree 虽然Appen-only形态，存在空间放大，但空间利用率相比于B+-tree高很多
        3. secondary index on LSM-tree
            1. the author didn't finish this part, but I found another survey 
               LSM-based Storage Techniques: A Survey: https://arxiv.org/pdf/1812.07527.pdf (Chen Luo, Michael J. Carey)
                1. from pictures pasted, it pretty much looks like this original zhihu article
                2. very good paper
            2. Filters [11]: an sstable file can header embed min/max of a given key
               Qadar et al. [57] even a secondary index for sstable can be embedded in its header, also bloomfilter for secondary index
               Diff-Index [66] use LSM-tree as index, Sync-insert style obsoletes entries lazily
                1. DELI [67] uses primary index scan when doing compaction to cleanup secondary index
                2. Luo and Carey [47] secondary index query must access primary index to validate the results.
                   A mutable-bitmap filter makes detecting old deleted records faster
                   primary index ONLY stores which only stores primary keys, for use in index maintenance
                    1. interesting useful techniques to further reduce LSM-tree cost
                       Efficient Data Ingestion and Query Processing for LSM-Based Storage Systems: https://www.vldb.org/pvldb/vol12/p531-luo.pdf (Same author)
                        1. Batched Point Lookup
                        2. Stateful B+-tree Lookup
                        3. Blocked Bloom Filter
            3. Joseph et al. [29] HBase global secondary index vs local secondary index
                1. global secondary index update may happen on a remote node
                2. local secondary index of all partitions must be searched, because they are first partitioned by primary key rather than secondary key
                    1. a (bloom) filter first?
                3. Duan et al. [30] create global secondary index by scanning then re-partitioning local secondary index
            4. Duan et al. [30] create materialized view for LSM-tree. by append delta list to materialized view and lazy apply
            5. Absalyamov et al. [7]  statistics collection framework for LSM-tree. Flush and merge derives statistical summaries, e.g. histograms and wavelets.
                1. they can be used for cost-based query optimization on LSM-based systems
        4. Table 3: Summary of trade-offs made by LSM-tree improvements
            1. very useful to summarize all reviewed techniques and their trade-offs

13. ECWide: Exploiting Combined Locality for Wide-Stripe Erasure Coding in Distributed Storage    [2021, 3 refs]
    https://www.usenix.org/conference/fast21/presentation/hu
    1. good paper. new area Wide Stripes EC codec to reach 1.0x storage overhead, and to mitigate repair amplification by exploiting LRC and rack locality
    2. highlights
        1. Wide stripes - (n, k) > 100 to achieve 1.0x storage overhead
            1. Figure 2c shows the example, Figure 3 shows the bounds
        2. two types of locality
            1. parity locality - LRC
            2. topology locality - placement to exploit rack local repair to reduce cross rack traffic, especially long codecs to place more than one fragments per rack
        n. my questions
            1. putting fragments from same local group into same rack impairs reliability against TOR down, usually bad practice
            2. for reliability, long codec is subject to easier node failure due to that are more fragments to be vulnerable,
               but probably the LRC and TC provided faster repair can help
    n. related materials
        1. Tencent ultra-cold storage system optimization with Intel ISA-L - a case study
           https://software.intel.com/content/www/us/en/develop/articles/tencent-ultra-cold-storage-system-optimization-with-intel-isa-l-a-case-study.html
            1. interesting .. including optimized instruction set and asm for EC speedup
        2. VastData - mentioned in paper as classic Wide Stripe product
           https://vastdata.com/blog/providing-resilience-efficiently-part-ii/
           https://vastdata.com/blog/breaking-resiliency-trade-offs-with-locally-decodable-erasure-codes/
            1. EC overhead varies between 2% and 11%. The number of data blocks in the stripe between 36 and 146 - the number of parity blocks is always 4
               https://support.vastdata.com/hc/en-us/articles/360036872354-Understanding-VAST-Capacity
```

Papers about persistent memory filesystem, outlining recent directions

```
10. Octopus: an RDMA-enabled Distributed Persistent Memory File System    [ATC17, 106 refs]
    https://www.usenix.org/conference/atc17/technical-sessions/presentation/lu&quot;&gt;Octopus
    1. Good using RDMA to PMEM. Filesystem side, client does everything. Directly expose PMEM
    2. highlights
        1. RDMA to (a shared pool of) PMEM
        2. selfidentified metadata RPC
            1. Client RDMA write but with notification to host
        3. Removing memory copy operations
            1. EXT4-DAX - directly access persistent memory storage without going through kernel page cache
            2. Octopus - expose FS image in PMEM to RDMA, bypassing OS and FS stack
    n. related materials
        1. Orion: A Distributed File System for Non-Volatile Main Memory and RDMA-Capable Networks
            1. Octopus limitations
                assumes a simplifed file system model
                uses client-side partitioning
                no replication

14. Basic Performance Measurements of the Intel Optane DC Persistent Memory Module    [2019, 206 refs]
    https://arxiv.org/pdf/1903.05714.pdf
    1. useful paper to reveal Intel Optance DC PMM performance in detail
    2. highlights
        1. NV DIMMs finally commercially available with Intel Optane DC PMM
        2. Optane DC PMM has higher latency (346 ns) than DRAM
           Unlike DRAM, its bandwidth is asymmetric, max read bandwidth is 6.6 GB/s, max write bandwidth is 2.3 GB/s
        3. DRAM cached mode: use Optance DC PMM as memory, and DRAM as a cache.
           App Direct mode: use PMM as persistent storage device
        4. User-space Optance DC persistence generally outperformed their filesystem counterparts
    n. related
        1. An Empirical Guide to the Behavior and Use of Scalable Persistent Memory     [FAST20]
           https://www.usenix.org/conference/fast20/presentation/yang
            1. The two papers somehow didn't mention each other

15. Orion: A Distributed File System for Non-Volatile Main Memory and RDMA-Capable Networks    [2019, 43 refs]
    https://www.usenix.org/system/files/fast19-yang.pdf
    1. Continue PMEM FS work from NOVA (per-inode logging), Octopus (RDMA to PMEM). Made a distributed filesystem.
       Useful paper, interesting, can be used as a reference implementation. Metadata and data flows are in detail
    2. highlights
        1. NVMM is Faster than RDMA
            1. NVMe 70us, RDMA 3us, NVMM 300ns
            2. Orion tries to store data local, the convergence storage approach again
        2. Orion approach
            1. A kernel filesystem that can do networking
            2. NVMM devices are exposed and become a pool
                1. Data: Globally addressed pages
                2. Metadata: a memory region to be DMAed with, and RDMAed with
            3. local DAX access, remote RDMA access
                1. DAX vs O_DIRECT
                   https://www.unix.com/filesystems-disks-and-memory/268555-what-difference-between-o_direct-dax-ext4-filesystem.html
                    1. DAX is optimized for PMEM, byte-addressable, no extra copy
            4. Inherited from NOVA
                1. Per-inode metadata (operation) log
                2. Build in-DRAM data structures on recovery
                3. Atomic log append
            5. Accelerating Metadata Access
                1. RDMA perfers inbound operations (reads IOPS is ~7.8x higher)
                    prefers small operations (8B sends has lower latency than 512B)
                2. strategy: , Log Commit, RPC
                    1. Tailcheck - by pass MDS via 8B RDMA_read
                        1. client maintains a local copy of inode and logs from MDS
                           log is append-only and needs to be in sync with MDS
                    2. Speculative Log Commit: try local first, then log tailcheck, if conflict then rollback
                        1. client arbitration - multiple clients accessing single inode without distributed locking
                            1. If the MDS has committed multiple log entries in a different
                                order due to concurrent accesses, the client blocks the current
                                request and finds the last log entry that is in sync with the
                                MDS, it then fetches all following log entries from the MDS,
                                rebuilds its in-DRAM structures, and re-executes the user
                                request
            6. strong consistency data updates
                1. Achieving strong consistency over RDMA is hard because
                    RDMA hardware does not provide a standard mechanism to
                    force writes into remote NVMM
                2. paper solution - interesting
                    1. a client uses copy-on-write when updating multiple nodes pages
                    2. an RDMA trick: client includes pages's global address when sending to data store
                       so data store knows the modification, it forces pages into NVMM, and then send ack to MDS
                       MDS after received enough number of data store ack, then process client's log commit
            7. replication
                1. Mojim-like [76] high-availability pair consisting of a primary MDS and a mirror
            8. data migration to exploit local NVMM access is faster than RDMA
                1. For internal clients, the copy-on-write migrates the block into the local NVMM if space is available
                2. MDS allocates internal clients chunks of its local NVMM when possible since local writes are faster
            9. delegated allocation - to avoid allocation on critical path; using a distributed two-stage memory allocation
                1. MDS keeps a bitmap of all the pages Orion manages
                   Clients request large chunks of storage space from the MDS via an RPC.
                   The client can then autonomously allocate space within those chunks

16. SplitFS: Reducing Software Overhead in File Systems for Persistent Memory    [SOSP19, 59 refs]
    https://arxiv.org/abs/1909.10123
    https://sekwonlee.github.io/publications/sosp19_splitfs
    https://www.youtube.com/watch?v=TJNn0k3lENM
    1. Data path at userspace, while metadata operations served in kernel by building atop Ext4-DAX. Kernel bypassing via mmap
       compared to Orion, it builds userspace data path, interesting new direction, which is followed up by many papers
    2. highlights
        1. POSIX filesystem aimed at reducing software overhead for PM
            1. serves data operations from userspace
                1. using DAX mmap to operate PMEM. No passing through kernel. mmap region is allocated by Kernel-Split
            2. metadata operations using ext4-DAX kenrel filesystem
                1. provide strong guarantees such as atomic and synchronous
                    1. uses logging and out of place updates for providing atomic and synchronous operations
                        1. a staging file, mmap bypassing kernel, and then re-link
                            1. an alternative approach given up - Staging writes in DRAM
                                1. While DRAM staging files incur less allocation costs than PM staging files,
                                    we found that the cost of copying data from DRAM to PM on
                                    fsync() overshadowed the benefit of staging data in DRAM.
                                    In general, DRAM buffering is less useful in PM systems
                                    because PM and DRAM performances are similar
                        2. per-application log, logs every logical operation
                            1. Each log entry fits in one cache line
                            2. Persisted using a single non-temporal store and sfence instruction
                    2. U-Split is able to provide different consistency level, different for each App
                2. putting metadata also in userspace, didn't choosen, because of high complexity
            3. SplitFS does not optimize for multiple processes concurrently access the same file
    
    n. related
        1. Scalable Persistent Memory File System with Kernel-Userspace Collaboration    [FAST21, 1 refs]
           https://www.usenix.org/conference/fast21/presentation/chen-youmin
            1. in general PMEM filesystem recent years trend is moving to userspace. but compared to Orion and SplitFS, this paper the design and implementation are made with more completeness. interesting paper
               KucoFS improved more that 1) offloading as much in ULib (userspace) to KFS (kernel space) - collaborative indexing, kernel-userspace two-level locking, 2）Data protection that read-only in userspace, only write to new pages
               this paper is basically following SplitFS userspace/hybrid-space FS direction, Orion is mentioned by less compared
            2. FAST21-Advanced File Systems
               https://zhuanlan.zhihu.com/p/353355462
                1. "SplitFS，ZoFS，提出了内核态文件系统和用户态文件系统协作的混合架构。由于内核态文件系统和用户态文件系统各有优势和缺陷，如何能够让他们之间相互协作，并发挥他们的优势就很关键了"
                2. 用户态和内核态协作的文件系统Kuco
                    1. Ulib (userspacef)为上层应用提供标准的API接口，负责与Kfs交互（通过Msg Buf）, Kfs (kernel space)负责处理元数据以及访问控制
                    2. 尽可能的将Kfs的任务交给Ulib进行处理，减少Kfs的延迟。
                        1. 采用Collaborative indexing，将路径名遍历任务offload到Ulib上，完成后将相关信息封装到请求中发送给Kfs，Kfs直接使用相关路径地址执行元数据调整
                        2. Two-level locking to avoid KFS frequently inovled in concurrency control.
                           this is done by assigning write leases on files, a coarse-level concurrency control; only processes with leases can exclusively access file write
                            The second level locking control is userspace range lock. threads in same process can access the leased file concurrently, writes are serialized
                    3. Data writes and protection - Three-Phase Write
                        1. PM mapped to userspace with read-only mode. "在Ulib写之前，Kfs在页表中调整写权限，可以看出由于ulib和kfs进行的交互会成为瓶颈，Kfs采用了预分配的方式，一次为ulib分配更多的page"
                            1. Kuco采用COW的方式写数据。newly written data is always redirected to new PM pages
                            2. 由于采用了COW的写方式，会存在新旧版本，Kuco采用Versioned Read机制执行用户空间的读操作
                    4. Data layout - KucoFS实现的是DRAM+PM的混合架构
                        1. DRAM中维护的有inode table，PM中维护的有Operaton log和 data page和metapage in 4KB size

        2. ZUFS Overview Developing PMEM-based File-System in User-Space
           https://lwn.net/Articles/756625/
           https://www.youtube.com/watch?v=Nd0f3yd5nVg
           https://pirl.nvsl.io/PIRL2019-content/PIRL-2019-Shachar-Sharon.pdf
           https://www.snia.org/sites/default/files/SDCEMEA/2020/2%20-%20Shachar%20Sharon%20NetApp%20-%20PMEM%20File-system.pdf
            1. NetApp filesystem for Persistent Memory, Userspace + Kernel Module, opensourced, zero-copy. Developed as part of NetApp MAX Data product
               https://github.com/NetApp/zufs-zus
            2. highlights
                1. ZUFS compared to FUSE
                    1. ZUFS is PMEM oriented, an framework to build more FS. FUSE is general purpose but slower
                2. challenges and solutions
                    1. How to avoid extra copies?
                        – Let zusd write directly into application pages
                        – User-space mapping, in-kernel I/O
                       How to do efficient mmap?
                        – Direct mapping to PMEM (bypass page-cache)
                       How to preserve affinity?
                        – Dedicated user-space thread per CPU

17. High Velocity Kernel File Systems with Bento    [FAST21 Best paper award, 0 refs]
    https://www.usenix.org/conference/fast21/presentation/miller
    1. interesting paper. First time made available implementing Linux Kernel filesystem with Rust,
       and support live upgrade without interrupting user traffic. and switch to FUSE with a changed build flag
    2. highlights
        1. designs
            1. why not FUSE nor eBPF
                1. FUSE: cannot reuse kernel features such as buffer cache, and performance overhead
                2. eBPF: VM restrictions made hard to implement large/complex functionalities
            2. Use CrashMonkey[34] to check correctness and crash consistency
            3. BentoFS -> libBentoFS -> FS -> libBentoKS -> Kernel Services
                1. BentoFS is built in C to work with VFS. Other parts are in Rust
                   libBentoFS does C-to-Rust translations. libBentoKS translates to Kernel calls. The two are thin layers
            4. about performance overhead
                1. the paper solutions evaluated shows little overhead, as most are just another of abstraction layer redirection calls
        2. key features
            1. live upgrade with ~15ms delay
                1. good part.
                2. libBentoFS can first quiescent (drain) user calls.
                   this is done by using a read-write lock, where read lock for user calls, and write lock for FS upgrade
                3. FS state needs to be transferred, e.g. in-process requests, memory states, journal states, TCP connections
                   this is done by letting FS define two interfaces to serialize out current states, and serialize in resumed states
                n. questions
                    1. how to upgrade the libBentoFS and libBentoKS itself?
                    2. it seems in distributed system UD upgrade is already a solution, no need for non-interruptive FS upgrade
                       besides, OS upgrade will need do restart node and interrupt user calls anyway ..
            2. userspace debugging, by changing a build flag to rn in FUSE instead of Kernel
                1. changing a build flag, Bento can run in FUSE mode rather than in kernel
                2. for APIs mismatched between FUSE and Kernel dev, Bento provides two version of lib to implement differnetly for the same API
    n. related materials
        1. FAST21-Advanced File Systems - Lancer
           https://zhuanlan.zhihu.com/p/353355462
            1. summarized most paper key points
        2. Linux Kernel中AEP的现状和发展
           https://developer.aliyun.com/article/703891
        3. ZUFS - NetApp zero-copy userspace FS for PMEM
           https://pirl.nvsl.io/PIRL2019-content/PIRL-2019-Shachar-Sharon.pdf

20. Rethinking File Mapping for Persistent Memory    [FAST 2021, 0 refs]
    https://www.usenix.org/conference/fast21/presentation/neal
    https://www.youtube.com/watch?v=YDnW-wXd6bc&t=453s
     1. // TODO
     2. highlights
        1. mapping file address to PMEM block address. traditional structure is slow.
           this paper proposes HashFS using hash table to do the mapping, and parallel with SIMD
            1. page cache is not necessary, bypass it
            2. using the same hash table to do both file address mapping and block allocation
            3. compared to traditional index, the hash table avoids resizing which can be expensive

21. SpanDB: A Fast, Cost-Effective LSM-tree Based KV Store on Hybrid Storage    [FAST 2021, 0 refs]
    https://www.usenix.org/conference/fast21/presentation/chen-hao
    https://www.youtube.com/watch?v=a_eDVmh6CSc&feature=emb_imp_woyt
    1. // TODO
    2. highlights
        1. parallel WAL writes via SPDK, WAL targets NVMe SSD, data targets SSD
            1. bypass Linux kernel, using polling IO, handle async processing

22. Performance and Protection in the ZoFS User-space NVM File System    [SOSP 2019, 32 refs]
    https://ipads.se.sjtu.edu.cn/_media/publications/dongsosp19-rev.pdf
    https://www.youtube.com/watch?v=x6Gcc34L3vs
    https://sosp19.rcs.uwaterloo.ca/slides/dong.pdf
    1. good paper. Using virtual memory MMU to isolate users' Coffers, and use MPK to secure Coffer internal metadata, and shared Coffer.
       Coffer management is still by Kernel. Userspace only a per user app FS lib is needed, no FS server               
      Userspace direct updates in ZoFS improve 33% throughput compared to kernel implementation, latency reduced from ~3.5us to ~2.5us
    2. highlights
        1. Userspace PMEM filesystem, grant userspace control to both metadata and data
            1. "Coffer" abstraction to group resource and do isolation
                1. Hardware supported paging isolation for different users
                2. Stray writes corrupt metadata in mapped Coffers
                    1. Concept "Write Window": only temprarily enable write access in short time when uFS needs modification
                        1. questions: the solution sounds more like a mitigation but fixing the root problem
                3. Malicious manipulations: an attacker can manipulate a pointer to another coffer of another user
                    1. Approach: at most one coffer is accessible at any time for each thread
                        1. questions: the solution sounds more like a mitigation but fixing the root problem
                4. An error in FS library can terminate the whole process
                    1. like Kernel crash?
                    2. approach: setjmp, hook SIGSEGV, i.e. to handle exceptions.
                       transform segmentation fault to report to App as an FS error code
        2. questions
            1. what's the security / isolation issue if implementing FS metadata path also in userspace?
                1. as far as I see, it's
                    1) cannot reuse kernel API e.g. page cache, journaling etc
                    2) even IO path is in userspace, the memory management, paging, and processes are still in kernel. this means the FS process mixes different user requests in same memory paging and process, potential breach.
                        1. e.g. virtual memory address cannot be used
                           essentially, this is still that userspace impl cannot leverage kernel provided management abilities / or API
                    3) file mode/owner/perm change, still handled by kernel
                        1. question: but how that is passed to userspace FS to respect the permission
                2. if the user is using a clientlib to operate PMEM and shared memory to operate filesystem
                    1. OK .. that's really easy to leak attacks to other users.
                       the write must goes through something middle server to do protection
                       then an extra layer of delay
        3. re-reading the paper
            1. There are different approaches to handle the protection of metadata per userspace PMEM filesystem
                1. Aerie[56] uses a dedicated process to audit metadata modifications, user side FS libraries need to send requests to the server via IPC
                2. Strata[31] user side FS lib record updates in PMEM log, kernel does digestion and apply
                3. this paper approach, ZoFS
                    1. only userspace FS lib, no audit central process, the lib runs at user permission and user control
                    2. the PMEM pages are grouped in to Coffer, and mmap to userspace to the user's app, user app has full control
                       the mapping process is done by Kernel. mapping uses virtual memory management MMU, i.e. hardware MMU, to achieve isolation from other Coffers
                       user side FS lib has full control to the Coffer, userspace lib does a uFS in the Coffer, including both data path and metadata management
                    3. how to protect Stray Writes? - using Intel MPK
                        1. Stray Write - the user app or FS lib bug can write in unexpected place / unexpected time, to corrupt the metadata (or data)
                           using MPK to achieve (MPK can be controlled by user app userspace, no need kernel or privileged access)
                             G1 - A coffer can be accessible only when the uFS is accessing the coffer
                        2. MPK register is per thread, so concurrent thread cannot exploit the window opened by this thread
                        3. Fault Isolation
                            1. G2 - At any time, at most one coffer is accessible in userspace for each thread
                            2. at most 15 coffers can be mapped to a user app, because Intel MPK has 16 pairs in total
                                1. question: as paper mentioned, this also blocks user app itself from using Intel MPK
                        4. Metadata security - when two users are sharing the same coffer
                            1. attacker to corrupt local data in shared coffer is OK
                               the paper identified the only needed protection is a file metadata is tampered to point to another coffer, this breaks the isolation
                            2. the protect from the above. 1) Using G2, an thread can only one Coffer at a time 2) file/dentry path needs to be verified before follow
            2. related works
                1. questions
                    1. in summary, this paper is pretty much like container-based FS, but enhance inside coffer protection with MPK, and enhance share coffer protection
                       tradition block device isolation / userspace virtualization, e.g. docker, is done by creating different block devices in VFS and map to container
                       in this paper, they are instead the Coffers. Isolation is done by virtual memory paging / MMU

```

Papers about cross datacenter erasure coding

```
1. AZ-Code: An Efficient Availability Zone Level Erasure Code to Provide High Fault Tolerance in Cloud Storage Systems   [Alibaba 2019, 13 refs]
    https://storageconference.us/2019/Research/AZ-Code.pdf
    1. LRC code where local group use MSR code and global parity uses RS code
       MSR code is a regenerating code that reduces reconstruct network cost, 
    2. questions
        1. MSR code is known to require high parity symbol. but seems recent progress relaxed it
           Minimum Storage Regenerating Codes For All Parameters: https://arxiv.org/abs/1602.04496
        2. is it used on Alibaba production? 

2. Giza: Erasure Coding Objects across Global Data Centers    [Microsoft ATC 17, 53 refs]
   https://www.usenix.org/conference/atc17/technical-sessions/presentation/chen-yu-lin
    1. works Azure Table level to group objects and EC
       build GIZA Put/Get upon Fast Paxos to resolve cross DC consensus
       workload type Microsoft OneDrive
    2. highlights
        1. OneDrive workload
            1. >1GB objects taking > 50%
            2. ~50% reads happen on first day
            3. cross-DC traffic can be reduced by ~50% by days of caching 
    n. related materials
        1. The Storage vs Repair-Bandwidth Trade-off for Clustered Storage Systems    [2018, 49 refs]
           https://arxiv.org/pdf/1701.04909.pdf
        2. CRaft: An erasure-coding-supported version of raft for reducing storage cost and network cost    [FAST 2020, 6 refs]
           https://www.usenix.org/system/files/fast20-wang_zizhong.pdf
            1. For GIZA metadata paxos, it's possible to use EC to reduce replication

3. The Storage vs Repair-Bandwidth Trade-off for Clustered Storage Systems    [2017, 49 refs]
   https://arxiv.org/pdf/1701.04909.pdf
    1. RLNCs, regenerating codes, file is split into n clusters * m nodes each
       the optimal trade-off between storage-overhead and inter-cluster repair-bandwidth
    2. it can be useful, if a user's data object is intentially split across mutiple datacenters
       or, we want to union different objects at different datacenters, to form an EC group
    3. it becomes more interesting for "cloud-of-clouds", where user data is first-place spread across different cloud vendors 

4. Incremental encoding for erasure-coded cross-datacenters cloud storage    [2018, 3 refs]
   https://www.researchgate.net/profile/Fangliang-Xu-2/publication/324766405_Incremental_encoding_for_erasure-coded_cross-datacenters_cloud_storage/links/5bb71d294585159e8d86a485/Incremental-encoding-for-erasure-coded-cross-datacenters-cloud-storage.pdf
    1. Replicating Encoding (offline EC) vs Stripping Encoding (Inline EC)
   paper proposed Incremental Encoding: Inline EC, partity server incrementally receive each data fragment, step by step adds up to the final parity
    2. questions
        1. higher network amplification compared to Stripped Encoding, because full data is sending to each parity server?
        2. probably the benefit is, even we don't enough user data to cut full data fragments, parity can be updated and generated .. but the storage overhead is high .. and to ensure each step on-disk, parity server needs to repeatedly update on-disk data
```

Database B+tree and concurrency control, outlining typical approaches

```
4. Optimizing Optimistic Concurrency Control for Tree-Structured, Log-Structured Databases (Microsoft) (HyderDB)    [2015, 42 refs]
    1. Follow up to Hyder database design to make Meld algorithm faster by leveraging multi-cores 
    2. highlights
        1. log is the database / log is the system design. Hyder published first paper at 2011
            1. transaction commits to central logging as an Intent
               Intent can conflict, the Server who applies logs will resolve in deterministic Meld algorithm
            2. each Server sees whole log, there is no explict sharding, but Server is expected to only hold related data
                1. the Server internally construct a B-tree to favor reads
                2. per Intent resolving, a Server is possible to need to fetch data not in its scope
                   the Server needs to randomly access Log to fetch that piece of data
                    1. question: the random reads to log data .. bad to performance ..
        2. Making Meld faster
            1. to leverage multi-cores: deserialization -> premeld
               unable to multi-core: group meld
    n. related
        1. Hyder - A Transactional Record Manager for Shared Flash    [2011, 181 refs]
           http://web.eecs.umich.edu/~michjc/eecs584/Papers/cidr11_hyder.pdf
           http://accelazh.github.io/database/Distributed-Transaction-ACID-Study
            1. paper from Microsoft. using shared log + multiple * single-know-all sql database server.
               transactions broadcast so each node knows everything and can resolve conflicts.
               has some similarity to AWS Aurora Multi-master
            2. another log is the system / log is the database design

5. A Survey of B-Tree Locking Techniques    [2010, 99 refs]
   https://15721.courses.cs.cmu.edu/spring2017/papers/06-latching/a16-graefe.pdf
    1. useful paper to clarify latch vs lock and to cover common techniques for B+-tree locking
    2. highlights
        1. concept latch vs lock for protecting B+tree structure vs transaction content
        2. why B+tree needs latch protection
            1. no concurrent modify on a page
            2. no modify to parent to child pointer while following pointer to child
            3. ascending and descending index scan can deadlock
            4. a B-tree inserting can overflow and cause node split/merge propagating from leaf to root
        3. Lock coupling, sovling the above issues
            1. retaining the latch on parent node until child node is latched
            2. restarting root-to-leaf traversal, (with resumes)
            3. if child page needs IO load, lock coupling can instead hold latch on page descriptor
            4. asynchronous read ahead while traversaling
            5. opposite travseral direction try lock with immediate failure reather than deadlock
            6. shard latch and then upgrade
        4. tree load balancing and reorg can be async from user requests and execute at background
            1. "forward recovery" to complete a reorganization after system restart
        5. protect B-tree's logical content
            1. key range locking, predicate locking
            2. hierarchical locking
            3. increment lock modes
            4. separating locaks on individual key values and the gaps between key values

9. Latch-free Synchronization in Database Systems: Silver Bullet or Fool’s Gold?    [2017, 19 refs]
   http://cidrdb.org/cidr2017/slides/p121-faleiro-cidr17-slides.pdf
    1. very good paper, in-depth experiment and analysis on different types of latch and latch-free algorithms, and finding the key insights
       very useful. outlined the B+tree locking technique and lock-free algorithms 
    2. highlights
        1. typical latch-free and latch methods tested
            1. latching
                1. xchgq - lock the bus when exchanging value
                2. pthread - random backoff, built-in contention handling (acquire 2 cas if both fail - contention)
                3. MCS - queue threads, lock owner change flag, rather than all threads hitting the flag 
            2. latch-free
                1. compare-and-swap
                2. TATAS
        2. key conclusions
            1. CAS (or test-and-set) is executed serially. all threads flood CAS to the same shared memory location is extremely bad pattern
                1. besides, lock-free spends extra computation doing failed retry calculate again
                    1. and besides, lock-free alogirithms usually need extra memory management cost, e.g. read-copy-update, epoch-based memory reclaimation
                        1. essentially this is because latch-free must permit thread unrestricted access to data structure
                2. in general, latch-free algorithms perform bad in high contention cases
                3. when num of threads exceed num of physical cores, both latch-free and latch algorihtms drop throughput significantly
            2. experiements show that
                The importance of designing synchronization mechanisms that minimize repeated updates on contended shared memory locations.
                Repeated updates can cause scalability issues because they are processed sequentially, and therefore increase the amount of sequential execution in a concurrent program.
                A synchronization algorithm’s ability to reduce the number of these sequential operations on shared memory locations is the SINGLE BIGGEST FACTOR that influences its scalability
                    1. the figures at Experiment sections are very interesting
                    2. e.g. pthread's "two distinct latency profiles of requests"
            3. as modern database systems — especially main-memory database systems — move to a process model where there is a one-to-one mapping between OS contexts and processing cores, the progress guarantees of latchfree algorithms are MARGINALIZED
        3. survey on research directions
            1. limit shared-memory interactions within NUMA socket, while use message-passing across NUMA nodes
            2. schedule prior to execution, PALM B-tree, divides operation in non-conflicting sets, order before execution, thus no synchronization cost
            3. asynchronous coordination, physical replay of redo log records can therefore be imlemented in a coordination free manner by applying last-writer-wins rule
            4. threads holding lock can be preempted by OS, increasing locking delay
               thus DB may implement user-space non-preemptive scheduling itself
                1. SQL SERVER SQLOS
                2. database systems have a long tradition of implementing user-level scheduling of contexts (via DBMS threads) in environments where OS support for multi-processing was non-existent or inefficient
        4. Methods of locking a B+tree
            1. the classic Latch-coupling (lock coupling)
                1. lock parent while travseral to child, then lock child, release parent
                2. key insights
                    1. root node is the most frequently locked, but least needed to actually modify, the mismatch
                3. shared-intention-exclusive lock (SIX) - breaking the rw lock boundary
                    1. upon tree update, the thread may probe from leaf back to trunk to root, adding "intention" locks
                    2. the "intention" locks are exclusive to other tree updater, but still allow reads
                       the "intention" locks may also be dropped if the updater finds the node is not need to involve later
                    3. before executing the update, all readers on the "intention" locks must first be drained.
                2. latch free / optimistic concurrency control - ARIES/IM, B-link trees
                    1. OLFIT tree, improved from the B-link tree track
                        1. B-link tree is a starting, adding slibing link. but it has many non-realistic assumptions compared to today's systems
                        2. OLFIT tree, based on version number. reading is non-blocking non-locking/latching. updates still use latch.
                            1. thus avoided frequent latching the root, frequent modify the shared memory location (inside latching)
                    2. Masstree，B+树优化机制的集大成者
                       http://mysql.taobao.org/monthly/2018/09/01/
                        1. details in article. in general, Tri-tree for variable length key, B+tree for fixed length part in key. well-documented how to implement concurrency
                        2. Silo tree
                    3. Bw-tree - new approach for in-mem B+tree concurrency
                       https://www.microsoft.com/en-us/research/publication/the-bw-tree-a-b-tree-for-new-hardware/
                        1. changes are added as delta off-place. page-id mapping layer.
                           tree structure modification use two atomic phases

    n. related
        1. MySQL B+-tree lock coupling, blink tree, history
           http://mysql.taobao.org/monthly/2018/09/01/
            1. good. outlined the methods, histoy, and detailed into algorithms
               covering from MySQL implementation (basically lock-coupling), and to typical B+tree locking techniques
            2. related
                1. PolarDB B+-tree locking and history
                   https://zhuanlan.zhihu.com/p/50112182
                    1. same article

10. Building a Bw-Tree Takes More Than Just Buzz Words    [2018, 47 refs]
    https://www.cs.cmu.edu/~huanche1/publications/open_bwtree.pdf
    1. Opensource implementation OpenBw-tree, non-unique key support, and many optimizations
    2. high lights
        1. OpenBw-Tree
            1. question: I didn't find any link .. though
        2. listed other state-of-the-art in-memory data structures: (1) SkipList [8],
            (2) Masstree [31], (3) a B+Tree with optimistic lock coupling [22]
            and (4) ART [20] with optimistic lock coupling [22]
        3. address to Bw-tree's logical page id mapping table is how it supports atomic updating multiple links to a page (split, merge)
        4. epoch-based garbase collection
            1. decentralized GC scheme is better than centralized GC scheme (scalability issue)
                1. see figure 5
        5. SMO change (structure modification operation)
            1. help-along protocol [29]. threads must help complete prior before move to self job
        6. more optimizations
            1. non-unique key support
                1. Spresent Sdeleted algorithm
            2. pre-allocated virtual space (extent-based allocation?)
               from high to low to fill (so cpu scan from low to high, more optimized)
               node consolidation after space full
            3. faster node consolidation
                1. using key segments in node ..
            4. node search shortcuts
                1. micro-indexing [27]
```

Papers about Machine Learning in Storage / Database

```
1. Bao: Learning to Steer Query Optimizers    [2020, 11 refs]
   https://arxiv.org/abs/2004.03814
    1. Learned model to give better query hints to PostgreSQL optimizer. Auto re-train, traning time ~1hrs
       redust cost by ~30% to ~80%. and give better performance even at tail latency
    2. highglights
        1. Existing issues of Learned Query Optimizer prior work
            1. Brittleness: Learned cardinality estimators must be retrained when data changes
            2. Tail catastrophe:  often perform catastrophically (e.g., 100x regression in query performance) in the tail
        2. Key approaches
            1. instead of replacing entire query optimizer, only try to steer PostgreSQL optimizer by using hints
            2. assumes a finite set of query hints, and treat each subset of hints as an arm - multi-armed bandit problem
               the model predicts which set of hints lead to better performance for a particular query
            3. tree convolution model [44]
                1. interesting to see how a query plan tree is represented into vectors to input into the TCNN. Figure 4
                2. TCNN uses tree-shaped filters over a larger query plan tree
                   filters are stacked, later layers can learn complex patterns.
                   a helpful inductive bias for query optimization: tuned for query optimizer tree problem
            4. Thompson sampling
                1. gaining popularity. instead of find best parameters to model training set,
                   instead resample parameters every n-th query, only store k most recent eperences
                2. this balances exploitation vs exploration
            5. auto retrain. support adding exception rules. overlap prediction time via CPU vs training via GPU
        3. related works
            1. other directions for query optimizer
                1. learned cardinality estimation
                2. using reinforcement learning to construct query optmizers.
                   Neo [39] can show competitive results with commercial systems, but after 24hrs of training
            2. reinforcement learning has been applied to managing elastic clusters [35, 50], scheduling [36], and physical design [53]
            3. A few selected works outside the context
                of data management systems include reinforcement learning
                for job scheduling [37], automatic performance analysis [9],
                loop vectorization [20] and garbage collection [23]

2. An Inquiry into Machine Learning-based Automatic Configuration Tuning Services on Real-World Database Management Systems [2021, 0 refs]
   https://db.cs.cmu.edu/papers/2021/p1241-aken.pdf
    1. Evaluation OtterTune algorithms on Oracle with realworld workload.
       It can outperfom DBA manual configuration performance by 45%
    2. highlights
        1. evaluated algorithms
            1. (1) Gaussian Process Regression (GPR) from OtterTune [38],
               (2) Deep Neural Networks (DNN) [4, 39], and
               (3) Deep Deterministic Policy Gradient (DDPG) from CDBTune [40]
            2. TCP-C unrealistic points
                1. TPC-C simplistic database schema and query complexity
                2. existence of temporary and large objects in production database, but didn't cover in TPC-C
            3. optimal performance improvement is heavily affected by how many knobs can be tweaked
                1. if only two config knobs recommended by DB doc, one can achieve 75-95% perf compared by ML-generated config
                2. the paper limits to as many as 40 knobs, it's enough to see results, and too many knobs needs too much training time
                3. the advantage of ML-generated config is, it can cover thousands of config knobs, but human can hardly
            4. noisy cloud environment
                1. Figure 8, the VM on cloud has 1x - 4x performance variability on DB Time
                2. from methodolofy, the paper run 3 VMs each 3 runs of workload, hundreds of iterations each.
                   it then takes median on VM, and avg 3 VMs 
            5. others
                1. for generated DB config that failed to launch DB, set objective function to use 2x worst value
                2. disable Oracle maintenance background tasks, which affect performance during training
        2. questions
            1. I didn't find Figure to directly compare with DBA manual configuration?
```
