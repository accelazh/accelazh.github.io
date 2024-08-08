---
layout: post
title: "Recent Paper Reading: WAFL Flash, BG3, MegaScale, MAST, etc"
tagline : "Recent Paper Reading: WAFL Flash, BG3, MegaScale, MAST, etc"
description: "Recent Paper Reading: WAFL Flash, BG3, MegaScale, MAST, etc"
category: "storage"
tags: [storage, paper, cloud]
---
{% include JB/setup %}

```
1. Combining Buffered I/O and Direct I/O in Distributed File Systems    [2024, 0 refs, FAST24]
   https://www.usenix.org/conference/fast24/presentation/qian
   https://www.youtube.com/watch?v=YPpTPQURy-U
    1. Target HPC / Lustre. Dynamically switch Buffered IO and Direct IO. AutoIO, Simple but achieved 20% to 50% performance. improvement. First paper to try this approach.
       Not in paper but may apply similar techniques to PMEM buffering writes.
    2. Highlights
        1. When to use Buffered IO? - Small writes. 
           When to use Direct IO? - Large sequential writes, high lock contention, high memory pressure, no cache locality.
        2. More optimizations
            1. Adaptive server-side locking for direct I/O
            2. Server-side adaptive write-back and write-through
                1. My questions
                    1. See "Moreover, we do not implement server-side read-ahead", the server memory mentioned looks too small. It cannot support several extra GBs.
            3. Cross-file batching for buffered writes
                1. My questions
                    1. Why combining other seemingly unnecessary optimizations if the main topic is auto switching buffered/direct IO?
        3. My questions
            1. Cloud storage or Ceph typically rely on Direct IO to ensure durability semantics. Auto switching to buffered IO would break such guarantee. How to walk around this problem? Maybe to apply this paper techniques to PMEM or Soft Updates?

2. I/O Passthru: Upstreaming a flexible and efficient I/O Path in Linux    [2024, 1 refs, FAST24, Samsung, Facebook]
   https://www.youtube.com/watch?v=cJ6J2z46FTA
   https://www.usenix.org/conference/fast24/presentation/joshi
    1. Simple but widely useful extension in Linux kernel upstream to support modern NVM specific commands for FDP, ZNS SSD, intra SSD copy command, etc.
    2. Highlights
        1. Slides page 1, very useful. "NVMe innovations vs. Kernel abstractions". It summarizes typical NVMe commands, interfaces, and use cases
            1. NVM, ZNS, Key-Value, Computational storage
                1. NVM is block access
                2. ZNS is using Zone Append
                3. FDP (Flexible data placement) write needs new interface
                4. Copy command - intra SSD device copy, useful for GC, typically seen in Computational Storage or a middle group between conventional SSD vs ZNS SSD.
            2. Paper section 6.2 Computational Storage tells the definition of Memory namespace and Compute namespace. 
        2. What exactly is the IO Passthru?
            1. Motivation: ioctl today can do what the authors want, but the interface is synchronous and not efficient.
                1. E.g., NVME_IOCTL_IO64_CMD
            2. Then, added a new /dev/nvme<X>n<Y>. It's a char device because it cannot be block device (interface not match). Char device allows inputting anything the authors want
            2. Use io_uring to pass NVM specific commands to this /dev/nvme<X>n<Y>. 
            3. Big SQE and Big CQE, make the default queue entry of io_uring bigger in bytes
            4. ioctl can also use /dev/nvme<X>n<Y>.
        3. IO Passthru has well usage to integrate with many existing tools/libs
            1. This paper's change is simple but widely-useful, e.g. xNVMe, SPDK, nvme-cli, data protection DIF, DIX, etc.
                1. Note, Figure 12. IO Passthru is NOT as performant as SPDK.
                    1. See text in paper "Overall, I/O Passthru reduces the per-core efficiency gap but is still far from kernel-bypass solutions like SPDK. There are multiple reasons .."
            2. Integrating FDP into CacheLib, IO Passthru enables NVM FDP commands.
                1. Figure 11, CacheLib WAF reduced from 2.4x to 1.0x with FDP. This is good, very effective. However, this paper didn't show much details how CacheLib works with it.
                    1. CacheLib internally uses two IO engines: BigHash and BlockCache. BigHash handles small objects.
                    2. NVMe FDP allows to send write hints to avoid intermixing BigHash and BlockCache placement on SSD.

                n. Related materials
                    1. Github: (PR2) Adds the support for Flexible Data Placement(FDP) over NVMe into the Cachelib
                       https://github.com/facebook/CacheLib/actions/runs/7046739879
                    
                    2. Flexible Data Placement: State of the Union    [2023, Flash Memory Summit 23, nvmexpress.org]
                       https://nvmexpress.org/wp-content/uploads/FMS-2023-Flexible-Data-Placement-FDP-Overview.pdf
                        1. Linux Kernal: I/O Passthru
                        2. Cachelib
                    
                    3. Kangaroo: Caching Billions of Tiny Objects on Flash    [2021]
                       https://www.pdl.cmu.edu/PDL-FTP/NVM/McAllister-SOSP21.pdf

                    4. The CacheLib Caching Engine: Design and Experiences at Scale    [2020]
                       https://www.usenix.org/conference/osdi20/presentation/berg

        4. Others
            1. "NOT using the I/O scheduler performs best on NVMe SSDs .. Linux I/O schedulers (BFQ, mq-deadline, kyber) add significant overheads (up to 50%) and hamper scalability [12, 57]."
                1. [12] Linux 5.6 i/o scheduler benchmarks. https://www.phoronix.com/review/linux-56-nvme.
                2. [57] Performance characterization of modern storage stacks: Posix i/o, libaio, spdk, and io_uring    [2023]

3. I/O in a Flash: Evolution of ONTAP to Low-Latency SSDs    [2024, refs, FAST24, NetApp]
   https://www.usenix.org/system/files/fast24-curtis-maury.pdf
   https://www.youtube.com/watch?v=RVs1JjYQAkU
    1. Enrolling an 30+ year old WAFL filesystem (core of ONTAP storage system), which was originally designed for HDD, to support modern SSD.
       The key challenge is to drive optimizations in incremental way to an old product. The key technology is FastPath, i.e. "Bypassing layers for the error-free data path". In another word, the Run-to-Completion model.
       Results see Figure 6, max throughput is much increased before latency hike occurs. 
    2. Highlights
        1. What is WAFL today?
            1. Built from 1994, 30 years ago. Append-only FS designed for HDD. At which time software overhead is negligible compared to slow HDDs.
                1. But now the main challenge with SSD is high software overhead, and read message overhead (also software). See Figure 3, Figure 7.
            2. Slides page 3: Typical enterprise features for WAFL
                1. Multi-protocol, multi-tenancy. NFS, CIFS, iSCSI, FCP
                2. Snapshots, HA, DR (Disaster Recovery)
                3. Dedup, compression, encryption, clones
                4. Designed to maximize HDD bandwidth
            3. Slides page 6, Projects across the system. Or paper section 1 and 2.
                1. Journaling: Allocation in multiples of erase block size
                    1. [25] Efficient search for free blocks in the WAFL file system
                2. Inline versions of dedup and compression
                3. Sub-block compaction [27]
                    1. Countering Fragmentation in an Enterprise Storage System
                4. Scheduling: Waffinity
                    1. "Based on its type and the data it intends to access, each request is dispatched to a specific affinity in the hierarchy. A dedicated pool of Waffinity threads execute requests on a per-affinity basis within the WAFL component in a thread-safe fashion."
                    
                    2. "load-modify" transaction model: "all resources necessary for the operation are accumulated in the load phase during which the message may suspend one or more times, after which the handler is completed in a single non-blocking modify phase"
                        1. The key challenges of this paper are shown here:
                            1. A read may need below. This is why high software overhead on SSD.
                                1) several message hops 
                                2) multiple suspensions and restarts 
                                3) wait for the next thread to be scheduled
                            2. The solution in this paper, FastPath, is Run-to-Completion model in another word. 
                                1. No extra queues nor thread pickups, no suspensions in middle of request execution, eliminate unnecessary data hops.
                    
                    n. Related materials
                        1. To Waffinity and Beyond: A Scalable Architecture for Incremental Parallelization of File System Code (NetApp)    [2016]
                           https://www.usenix.org/system/files/conference/osdi16/osdi16-curtis-maury.pdf

        2. What optimizations are made by this paper to enroll WAFL for SSD?
            1. FastPaths
                1. WAFL Reply Fastpath - bypassing WAFL Read-done and Read restart.
                    1. Introduced a new "iobuffer" to the existing WAFL buffer cache and page header hash
                2. RAID Fastpath - bypassing storage read and read-done steps. 
            2. TopSpin - Bypassing the WAFL read step.
                1. Introduce the Storage Location Cache (SLC) and Hierarchical Attributes Cache (HAC).
                    1. LRU, stale entry, version numbers are employed in cache management
                2. See Figure 8 (after) vs Figure 2 (before) for which hops are optimized away.

        3. Others
            1. Another product, FlashRay, is a cleansheet design SSD-optimized storage system. It's discontinued. Instead, NetApp has chosen WAFL with incremental optimization for SSD.
            2. XRP [71] allows the user to embed application logic within the device driver's interrupt handler using eBPF
                1. XRP: In-Kernel storage functions with eBPF
            3. I/O schedulers have been optimized [68] for low-latency devices and even evaluated as software overhead [64]
                1. [64] Do we still need io schedulers for low-latency disks?    [2023]
                2. [68] Split-level i/o scheduling    [2015]
                3. Note, paper I/O Passthru mentioned "NOT using the I/O scheduler performs best on NVMe SSDs .."

        n. Related materials
            1. Do we still need io schedulers for low-latency disks?    [2023, 4 refs, HotStorage23]
               https://www.hotstorage.org/2023/papers/hotstorage23-final1.pdf
                1. IO scheduler is traditionally designed for HDD and sequential access device, where IOs need to be reordered to reduce seek time.
                   However on SSD, it's a random access device, and IO parallelism is high.

            2. XRP: In-Kernel storage functions with eBPF    [2022, 49 refs, OSDI22]
               https://www.usenix.org/conference/osdi22/presentation/zhong
               https://www.youtube.com/watch?v=n6_QaWATz2A
                1. Traditionally the approach is to bypass kernel to eliminate overhead, typically SPDK.
                   But here are downsides of bypassing Kernel, e.g. isolation, thread scheduling, sharing cores.
                   XRP instead hooks storage functions into Kernel via eBPF. The key technique is to use BPF to resubmit requests without returning to userspace.
                   First paper in this approach. Interesting. 
                2. Highlights
                    1. XRP is opensourced at  https://github.com/xrp-project/XRP.
                    2. Key advantages of XRP compared to SPDK
                        1. OS-supported, isolation, threading, etc. Without user-kernel space crossing.
                        2. More performant when threads are sharing a core
                            1. "56% better p99 latency than SPDK with two threads sharing the same core"
                            2. Compared to the case in SPDK that there are more threads than physical cores.
                        3. "does not lead to low utilization due to busy-waiting", if few IOs and at which case SPDK is busy polling.
                    3. Solutions
                        1. XRP with support for EXT4
                            1. Resubmission Logic by associating eBPF function with interrupt handler.
                            2. Metadata digest - a minimal filesystem mapping data to pass around eBPF
                            3. Kernel modifications - need around 900 lines of code change
                            4. Fallback - Upon error, retry dispatch IO with traditional user space system calls
                        2. BPF-KV, a B+-tree based KV store
                            1. Use case "For example, to traverse a B-tree index, a lookup at each level traverses the kernel's entire storage stack only to be thrown away by the application once it obtains the pointer to the next child node in the tree. Instead of a sequence of system calls from user space, each of the intermediate pointer lookups could be executed by a BPF function, which would parse the B-tree node to find the pointer to the relevant child node. The kernel would then submit the I/O to fetch the next node. Chaining a sequence of such BPF functions could avoid the cost of traversing kernel layers and moving data to user space."
                        3. WiredTiger's LSM-tree (MongoDB)
                    4. My questions
                        1. Is the "stable data structure" assumption practical? It needs them to remain immutable for seconds.
                            1. "Stable data structures. XRP targets data structures, whose layout (i.e. pointers) remain immutable for a long period of time (i.e. seconds or more). Such data structures include the indices used in many popular commercial storage engines, such as RocksDB [44], LevelDB [12], TokuDB [12] and WiredTiger [27]."
                        2. A second constraint - Page cache cannot be used
                            1. "User-managed caches. XRP does not interface with the page cache, so XRP functions cannot safely be run concurrently if blocks are buffered in the kernel page cache"
                        3. "Synchronization Limitation .. BPF currently only supports a limited spinlock for synchronization."
                            1. The approach in this paper is innovative. But there are quite a few limitations in BPF. Will implementing a full-featured product be practical?

            3. Efficient search for free blocks in the WAFL file system    [2018, 5 refs, NetApp]
               https://dl.acm.org/doi/10.1145/3225058.3225072
                0. From parent paper: "Journaling" ... "Allocation in multiples of erase block size" ... "As described in prior work [25], we changed the block allocator to write contiguously down the SSD LBA-space in multiples of the SSD erase page size, thereby mitigating the log-on-log problem [67] and increasing SSD lifetimes."
                    1. The "erase block" here refers to SSD device erause block which is managed by FTL. NOT related to erasure coding. The "erase block" concept is also extended to SMR drive's zone.
                        1. My questions
                            1. SMR zone size (hundreds of MBs) is much larger than SSD erause block size (several MBs). Is it feasible to manage them within one concept?
                1. The paper to reveal working details of WAFL write allocator
                2. Highlights
                    1. Concepts
                        1. Partial vs full stripe write. Full stripe write is cheaper. Fragmentation leads to more partial stripe writes.
                        2. Long write chains. Strive to write logically sequential data into physically consecutive addresses.
                        3. Factors that affect write allocator
                            1. Throughput to allocate new blocks, and to reclaim free blocks
                            2. the underlying RAID geometry
                            3. SSD/SMR media-specific attributes such as erase block size
                            4. free space fragmentation
                    2. Tracking free space
                        1. AA - Allocation Area, a set of consecutive blocks
                        2. Practice shows always writing to the emptiest AA simplifies tracking and defragmentation while being effective to yield more full stripe writes
                        3. AA sizing
                            1. multiples of SSD erase blocks, and reserve space for AZCS (checksum)
                    3. AA Cache
                        1. All hosted in memory, rated by AA score, organized in data structure size bins -> AA list (HBPS).
                        2. AA score - number of free blocks in AA, obtained in GC. 
                        3. TopAA metafile - cache the top 512 best AAs, to avoid a full linear scan

                n. Related materials
                    1. Algorithms and Data Structures for Efficient Free Space Reclamation in WAFL    [2017, 20 refs, FAST17 best paper]
                       https://www.usenix.org/system/files/conference/fast17/fast17-kesavan.pdf
                        1. Logged before

            4. Countering Fragmentation in an Enterprise Storage System    [2020, 6 refs, NetApp]
               https://www.netapp.com/atg/publications/publications-countering-fragmentation-on-an-enterprise-storage-system-20205214/
                0. From the parent paper: "Sub-block compaction [27]"
                1. All four forms of defragmentation — CSC, WAR, recompaction, and object defragmentation—
                2. Highlights
                    1. overview of WAFL
                        1. append-only
                        2. virtual layer mapping between logical and physical block
                            1. allows relocating read-only snapshot
                            2. Container File
                                1. It stores the blocks in a FlexVol. L1 is Virtual VBN, L0 is physical VBN, it's 2-level tree called container map.
                        3. Consistency point (CP)
                            1. An atomic transaction that collects and flushes the results of thousands of operations from main memory to persistent storage. This delayed flushing of "dirty" blocks allows for better layout decisions and amortizes the associated metadata overhead
                    1. free space fragmentation
                        1. By segment cleaning, which happens at AA (Allocation Area) granularity, and relocates in-use blocks
                        2. continuous segment cleaning (CSC)
                    2. file layout fragmentation
                        1. Fragmentation that consecutive file addresses are not written to consecutive physical addresses. It happens in overwrite since WAFL is COW.
                        2. Defragmentation is by WAFL Aggregate Relocation (WAR), by relocating blocks.
                    3. intra-block fragmentation
                        1. sources of fragmentation
                            1. File tail that is not aligned with 4KiB block size
                            2. Compression group tail
                        2. Sub-block Compaction
                            1. Merge multiple small blocks into one 4KiB block.
                            2. Addressing is by virtual address from container file.
                            3. The compacted block file tracks ranges from each file, and there is an RefCount Metafile.
                        3. Recompaction
                            1. Defragmentation process for intra-block fragmentation, and to reclaim the freed space in compacted block
                            2. Recompraction scannter checks the RefCount MetaFile to make decisions
                    4. intra-object fragmentation
                        1. block temperature
                            1. cooling scan - periodically decrements per block hotness counter. (if a block is accessed, it is reset to hot.)
                            2. tiering scan - marks cold blocks to be moved away from SSD and into HDD tier.
                        2. object defragmentation 
                            1. relocate blocks from sparsely populated objects into new fully utilized objects


4. Baleen: ML Admission & Prefetching for Flash Caches    [2024, 3 refs, FAST24]
   https://www.youtube.com/watch?v=zplYhMLr30A&embeds_referring_euri=https%3A%2F%2Fwww.usenix.org%2F
   https://www.usenix.org/conference/fast24/presentation/wong
    1. ML based flash cache admission tiered atop HDD. Group consecutive accesses (episode) as the input to ML model. 17% saving in TCO. Built in Facebook CacheLib and evaluated with Tectonic production traces.
    2. Highlights
        1. Key challenge: ML based cache policy to balanced disk read time reduction vs flash write wear out.
           Key innovation: ML based on episode: the window from first miss/admission to eviction. Rather than plain access trace. Access trace biases towards a hot key with many accesses.
            1. Episode is an offline model.
        2. Section 3.1 DT modeling is simple and well matches production trace at Figure 3. The DT model is simply a constant seek time + constant byte transfer rate.
            1. This is actually a good side finding.
        3. ML is trained to optimize for highest score episode. Score is defined as disk-head time reduced / flash write added.
           Prefetch is trained by benefit > threshold ε.
           Baleen-TCO determines the optimal flash write rate by simulating over a range of flash write rates.
        4. Evaluation: production traces from Facebook Tectonic. 17% saving in TCO.
            1. ML admission is implemented in CacheLib. Trained by Gradient Boosting Machine (GBM). The admission policy is modeled as binary classification.
                1. Appendix C.3 has an evaluation to show GBM is better than Transformer or other NN architectures.
            2. Prefetch model: ML-Range is trained by two regression models each for range start/end. ML-When is trained by excluding bad episodes, whose benefit < threshold ε.
            3. See Figure 7, the block popularity vs access count chart perfectly matches Zipf distribution.
            4. Appendix A.10, Figure 21 shows that testbed and simulator are faithful to production counters.
                1. Interesting and useful analysis method.
        5. Related works
            1. CacheSack [55, 56]
            2. CacheLib ML is a ML model that Meta used in production for 3 years, which was first described by Berg et al [5]. Baleen uses the same ML architecture (GBT) and serving (inference) setup, but a different training setup (episodes and optimizing DT instead of hit rate).
            3. Facebook's Tectonic bulk storage system uses a CacheLib-managed flash cache, with an ML admission policy that does not use episodes and does not perform prefetching.
               Kangaroo [31] improves CacheLib's small object cache, and is orthogonal to Baleen, which improves performance for large objects.
            4. Amazon's AQUA [2] also fills a similar role for Redshift (data warehouse), acting as an off-cluster flash caching layer with S3 as the backing store.
            5. ML-based flash caching policies Flashield [14] addresses the lack of information on flash admission candidates by putting them in a DRAM buffer first. The item's usage history is used to generate features for a support vector machine classifier.
               We compared Baleen to Flashield, a state-of-the-art ML baseline. We adapted the implementation of Flashield used in the S3-FIFO paper in SOSP 2023 [53]. Flashield was worse than our RejectX baseline.

        n. Related materials
            1. CacheSack: Theory and experience of google's admission optimization for datacenter flash caches    [2023, 5 refs, Google]
               https://dl.acm.org/doi/pdf/10.1145/3582014
                0. From the parent paper: "CacheSack [55, 56] optimizes admission policies for the flash cache in front of Google's bulk storage system, Colossus.
               This design shares Baleen's objectives of co-optimizing backend disk reads and flash write endurance. 
               CacheSack partitions traffic into categories using metadata and user annotations, assigning probabilities to each of 4 simple admission policies for each category by solving a fractional knapsack problem."
                
                1. CacheSack is the cache admission algorithm used by Colossus Flash Cache at Google.
                   Improved from previous LARC cache policy. CacheSack dynamically solve cache admission policy as a greedy knapsack problem per every 5min. Allows fractional admission policy on each cache category.
                   Improvement: 7.7% TCO reduction, 9.5% disk read reduction, 17.8 flash wearout reduction.
                    1. In another word, CacheSack is proving the previous cache policy LARC (i.e. AdmissionOnSecondMiss) is actually pretty good given it's much simpler. 
                
                2. Highlights
                    1. Key motivations - Improving from LARC [21]
                        1. Illustrate the problem
                            1. Colossus Flash Cache previously used LARC [21] to exclude data that are accessed only once by inserting data at the second access. Figure 2 shows that more than 60% of the traffic of Colossus Flash Cache is accessed only once
                            2. However, excessive flash writes are still possible with LARC, and as a workaround, Colossus Flash Cache used a write rate limiter to avoid an excessively high write rate
                            3. However, a blunt approach, since it does not accurately factor in the impact on overall cost, and treats all workloads similarly.
                            4. It may be preferable to allow some highly cacheable workloads to burst writes at the expense of other less cacheable workloads rather than throttling all writes

                        2. In another word to summarize the problems
                            1. Workload needs to be categorized rather than equally rate limited.
                            2. 39% items are only accessed twice, they should not cache miss.
                        
                        3. Colossus Flash Cache is decentralized
                            1. It can only use the resources of individual cache index server
                            2. ML models are not available, because Colossus Flash Cache binaries are updated per week
                                1. But CacheSack is computing statistic models, see Section 6.5 Model Training

                    2. Overview of Colossus Flash Cache
                        1. It's consist of cache index servers. The server keeps index in memory, and cache entries in flash drives
                        2. Buffer cache is for disk servers, to support recent access or prefetch for only a few seconds
                        3. Cache eviction policy - use Second Chance [30] (see related works), based on LRU eviction
                            1. Cache blocks are organized as 1GiB Colossus files in LRU queue. When evicting queue tail, 28% (empirical) blocks are reinserted into queue head.
                        4. Ghost cache [21]
                            1. Even an item is not cache, its metadata such as last access time is still stored in the memory of cache index server. 
                            2. The metadata is used to construct caching policies.

                    3. CacheSack solutions
                        1. Cache categories
                            1. Being aware of traffic sources: BigTable, Spanner, database
                            2. Even knowing which table name, locality group
                                1. Locality Group in BigTable
                                    1. Bigtable: A Distributed Storage System for Structured Data    [2006, OSDI06]
                                       https://www.usenix.org/legacy/event/osdi06/tech/chang/chang.pdf
                                        1. Multiple column families can be grouped into a locality group. A separate SSTable is generated for it.
                                        2. Different policies can be set for a locality group, e.g. compression, bloom filters, 

                            3. Plus user defined annotation
                        2. Admission Policies
                            1. AdmitOnMiss, NeverAdmit < AdmitOnSecondMiss (LARC) < AdmitOnMiss < AdmitOnWrite
                        3. TTL approximation [17][23] in cache modeling to approximate LRU cache
                            1. See Section 5.3 for into
                            2. See Section 9.2 for how it's used in cache modeling
                        4. Knapsack Problem
                            1. Find optimal policy per cache category
                                1. cost by disk reads, flash storage, and written bytes
                            2. Fractional policies: CacheSack can apply a policy to a fraction of a category
                                1. Then the problem becomes a fractional knapsack problem [14]
                                2. The advantage of considering a fractional knapsack is that it can be solved efficiently by a greedy algorithm, as opposed to a combinatorial knapsack that is NP-Hard.
                        5. CacheSack in production
                            1. Hashing a category to one of 5,000 buckets
                                1. And, if a bucket contributes less than 0.1% lookups, it will be merged to a single cache-all bucket
                            2. Model Cache retention times D
                                1. CacheSack uses 127 predefined cache retention times. Each needs to run the Knapsack Problem.
                        6. Buffer Cache Simulators
                            1. CacheSack simulates the buffer cache to determine whether the current miss in Colossus Flash Cache is also likely a miss in the buffer cache
                            2. Running the simulators is the most computationally intensive component in the CacheSack model
                        7. Model Training
                            1. The model is reset every 5 min and is trained based on the lookups in this 5-min period
                                1. Very interesting topic here, use statistic model in realtime for cache admission control

                    4. Lessons Learned
                        1. The automatic cache provisioning brought by CacheSack requires almost no configuration and maintenance so that it can be set and forgotten
                            1. One user experimentally overrode CacheSack with manually optimized policies and found that CacheSack worked as well as manual policy tuning
                        2. The experiment infrastructure allows developers to test new features by using 10% of the cache index servers
                            1. cache index servers are independent and isolated
                        3. one requirement of deploying a new cache algorithm is that the model behavior can be fully understood and monitored by the developers and SREs
                            1. In particular, the optimization was implemented as a simple greedy algorithm instead of using a generic linear program solver library

                    5. Evaluation
                        1. AdmitOnSecondMiss is actually very effective and just slightly worse than CacheSack.
                        2. CacheSack with prefetch reduces TCO by 7.7% compared to LARC.

                    6. Mathematical Model of CacheSack
                        1. Because the model retrains per 5 min, it can leverages the past records for offline algorithms. Unlike online algorithms where knapsack algorithm is hardly possible. This is actually a practical good method to design cache.
                        2. See the details of this Section 9. How it leverages fractional to solve the original knapsack problem in simpler greedy way for each cache category is the good part of this paper
                            1. Andrew's lower convex hull algorithm [2]
                            2. Convert the problem to a convex optimization problem
                            3. Greedily choosing each fraction from {AOM, AOW, AOSM, POM, POW, POSM, NA}
                            4. What is solved: Cache retention time D, and fraction for each policy

                    7. Related works
                        1. CacheSack's high-level idea is similar to Flashield [16] and CacheLib [7]: keep the eviction simple to control write amplification, and use more sophisticated admission to improve cache performance and flash write endurance
                        2. However, LARC loses all the second-access hits and becomes undesirable for long-tail accesses like Facebook's cache for social network photos
                        3. TinyLFU [15] works by comparing the expected hit ratio of a newly accessed object against that of the object that would be evicted next from the cache

            2. CacheSack: Admission optimization for Google datacenter flash caches    [2022, 11 refs, ATC22, Google]
               https://www.usenix.org/conference/atc22/presentation/yang-tzu-wei
                1. Duplicated with the CacheSack 2023 paper


5. OmniCache: Collaborative Caching for Near-storage Accelerators    [2024, 0 refs, FAST24]
   https://www.youtube.com/watch?v=k9HDnNPg_XM
   https://www.usenix.org/conference/fast24/presentation/zhang-jian
    1. In the topic of near-storage, typically computational storage device, how to collaboratively managing on-device and host memory buffers for accelerating I/O or data processing.
    2. Highlights
        1. Background
            1. Near Storage: This approach emphasizes bringing computational capabilities closer to storage devices to reduce data movement and associated overheads. It involves integrating compute resources like ARM or RISC-V cores, FPGAs, and DRAM directly within storage devices to enhance data processing efficiency.
            2. Computational Storage: This term specifically refers to storage devices that have embedded processing capabilities, such as Computational Storage Devices (CSDs). These devices are designed to offload specific computational tasks from the host CPU to the storage device itself, thereby improving performance and reducing latency.
        2. Key challenges / Use cases
            1. Near-storage memory capacity is typically smaller than traditional host-level RAM. This introduces "caching".
            2. Unaligned IO size in data movement between the host and the device.
                1. E.g. fetching a 4KB block for a 1KB application request (slides have better demo)
            3. In hierarchical caching approaches, threads must wait for cache eviction.
                1. Instead, Omni Cache introduces parallelism, allows threads to update other cache in parallel.
                2. HostCache, DevCache, OmniIndex
            4. Dynamic Offloading whether to process on host or on device
                1. storage-centric metrics (e.g. data distribution, I/O-to-processing ratio, data movement bandwidth, and queuing costs)
                2. Case study: K-Nearest Neighbor Search (KNN)
                    1. The read-cal_distance-nearestK and prediction can run at either host or device. The estimated time at host and device are compared to decide where to run KNN. The monitoring continuously runs throughput the process to offload dynamically. 
                        1. An interesting design. OmniDynamic uses cost modeling like SQL optimizer or database CBO.
        3. Key designs and principles of Omni Cache
            1. HostCache, DevCache, OmniIndex, OmniDynamic, OmniDev, OmniLib
                1. OmniIndex: A range tree of block ranges. Each node can either reside in host or device.
                2. OmniDev: On device filesystem and processing engine
                3. OmniLib: User-level, at host side, the container HostCache.
            2. Simultaneously utilizes HostCache and DevCache
            3. Parallelism, concurrent IO, concurrent processing on both sides. Don't stall whenever possible.
                1. Two-step LRU Eviction (Section 4.2.3.)
                    1. My questions
                        1. How to ensure the consistency between Host and Device? E.g. don't lost any block, index consistency.
            4. Reduce unnecessary data movement.
                1. By reducing passing 4KB amplified IO size through PCIe.
            4. CXL integration
                1. enable direct access to the accelerator's memory
        4. Related works
            1. DevFS approach: FusionFS, CrossFS (author's prior work)
            2. Computational Storage Devices (CSD), such as ScaleFlux
            3. POLARDB Meets Computational Storage

6. CVSS: The Design and Implementation of a Capacity-Variant Storage System    [2024, 2 refs]
   https://www.usenix.org/conference/fast24/presentation/jiao
   https://www.youtube.com/watch?v=mVv_Dgk_H7w
    1. Wear leveling is considered harmful. Evenly worn out blocks lead to decreasing reliability and performance hits. Instead, let's remap blocks and shrink SSD space.
       CVSS reduces the latency, improves the throughput, and extends the lifetime by 8–53%, 49–316%, and 268–327%, respectively.
       Very interesting research direction. It has potential to further improve SSD COGS and paradigm shift SSD usage pattern and interface.
    2. Highlights
        1. Key challenges and motivations
            1. Figure 1, the performance of the SSD degrades as the SSD wears out
            2. SSD fail-slow behaviors. Trade performance as flash reliability deteriorates, such as data re-reads or preventive re-writes.
            3. [25] Wear leveling in SSDs considered harmful (Same author Ziyang Jiao)
                1. "However, WL leads to an overall increase in wear on the SSD, resulting in a significantly higher error rate as all the blocks age".
                2. The fail-slow further forces SSD to increase WA for error prevention.
        2. Figure 5: How to shrink the existing capacity?
            1. Non-contiguous address space
            2. Data relocation
            3. Addressing remapping
                1. This approach is chosen. It has relatively fast shrinking time and also relatively avoids fragmentation.
                2. A new REMAP interface is introduced to SSD device
                3. Potentially leverage filesystem defragmentation
        3. Key design of CVSS
            1. Wear Focusing (rather than Wear Leveling)
                1. Interesting concept and idea.
                2. Allocation policy
                    1. prioritize middle-aged blocks to accommodate host writes and young blocks for GC writes
                    2. read-intensive data should be stored in young blocks
                        1. My questions
                            1. Usually recent data is both hot for read and write. Which kind of blocks should host them?
            2. Shrink the existing capacity
                1. And, Degraded Mode
            3. SSD interface REMAP
        4. Implementation
            1. CV-FS is implemented upon the Linux kernel v5.15 and modified F2FS while using F2FS as baseline.
            2. To implement the remap command, we extend the block I/O layer.
            3. The capacity-variant SSD is built on top of the FEMU [37].
    3. My questions
        1. If the paper is proposing SV-SSD device, it should evaluate on common filesystems. Why the paper also proposes CV-FS a filesystem again?
            1. Filesystem needs to change. Today's typical filesystem assumes disk capacity is constant, and partition size is constant.
        2. What's the difference between SV-SSD vs a plain bad block management in FTL?
            1. Gray failure. A healthy block but with increasing error rate.
        3. With Wear Focusing, the SSD will be almost always using highly worn out blocks. As this paper mentioned, this has many fail-slow problems. How to deal with them?

    n. Related mateirals
        1. [25] Wear leveling in SSDs considered harmful    [2022, 8 refs, HotStorage22]
           https://www.hotstorage.org/2022/slides/hotstorage22-paper81-presentation_slides.pdf
           https://dl.acm.org/doi/pdf/10.1145/3538643.3539750
            1. Same author Ziyang Jiao with the parent paper.
            2. Highlights
                1. Figure 1: SSD's TBW/capacity keeps decreasing in recent years
                2. Typical wear leveling algorithm
                    1. DP [3] - Hot-cold swapping
                    2. PWL [6] - Cold-data migration
                    3. DAGC [7] - Adjust GC victim
                3. Evaluation methods
                    1. synthetic workload, simulate with FTLSim [9]
                    2. metrics: WA, erase count
                    3. access address space footprint
                    4. Github: https://github.com/ZiyangJiao/FTLSim-WL
                4. Proposing "capacity-variant SSD"

            n. Related materials
                1. Hacker News: Wear leveling in SSDs considered harmful
                   https://news.ycombinator.com/item?id=31900482
                    1 Why Wear Leveling needs to move blocks?
                        1. "Suppose the file system stores photos and videos that the owner tends to keep forever without ever modifying them. The first files will land on NAND blocks with close to zero PE cycles and will stay there forever."
                    2. How does CoW replace levelling?
                       https://news.ycombinator.com/item?id=31903729
                        1. "I should explain that what I had in mind is that nearly worn out blocks should be marked no-longer-to-be-written-to. I left that part out due to writing too quickly. The point is there's no need to move blocks, just stop writing to worn-out blocks, and then the CoW nature of the filesystem will take care of the rest. Eventually you'll run out of non-worn-out blocks and the filesystem will become effectively read-only."
                    3. ZFS BP rewrite problem
                       https://news.ycombinator.com/item?id=31903729
                        1. "As for BP rewrite, the fundamental design fault in ZFS that makes BP rewrite hard is that block pointers include locations in them and so the checksums of blocks that have block pointers must change when any of those pointer-to blocks are relocated. What should have happened instead is that physical locations should have been separated so as to avoid block checksums binding physical block addresses: 
                            a) block pointers should have had no physical location in them, 
                            b) every block that contain block pointers should have been followed immediately by a "cache" array of physical pointers corresponding to the logical block pointers in that block, 
                            c) the "cache" of physical block addresses would then be easily excluded from block checksum computations, 
                            d) block caches would have been easy to overwrite."

7. NetMigrate: In-Memory Key-Value Store Live Migration with NetMigrate    [2024, 0 refs, FAST24]
   https://www.usenix.org/conference/fast24/presentation/zhu
   https://www.youtube.com/watch?v=l1fZykAGdM0
    1. KV store migration with zero downtime. Implemented with Redis and P4 language.
       Key techniques: 
        1) Track migration before/on-going/after per key range group, 
        2) Reduce memory usage by BloomFilter,
        3) And only on-going migration keys use Double-READ to ensure consistency.
       Also, leverage programmable switch to direct packets to source/dest, because the switch has the central view.
       Table 1: Overview of live migration approaches, is useful.
    2. Highlights
        1. Existing migration approaches (See slides)
            1. Source-based
                1. Source machine drives migration. Read, write go to source.
                2. Source migrates all data to dest, switch, and then transfer dirty data logs.
                3. Problem: downtime after switch
                4. Related works: RAMCloud [TOCS '15], Remus [SIGMOD'22]
            2. Destination-based
                1. Dest machine drives migration. Read, write go to dest.
                2. Dest migrates all data from source, switch, and then read fetches missing data on-demand.
                3. Problem: High latency when reading missing data on dest
                4. Related works: Rocksteady [SOSP'17]
            3. Hybrid
                1. Dest machine drives migration. Write goes to dest.
                    1. Read goes to both source and dest - Double-READ. 
                    2. Completed migration ranges need to be tracked somewhere.
                2. Dest migrates all data from source, switch, and then read goes to both source and dest.
                3. Problem: Double read packets through network
                4. Related works: Fulva [SRDS '19]
        2. Background of Programmable Switch
            1. P4 programming language. This is also how this paper implements the code. Key value store to migrate is Redis.
            2. See slides for Parser, Match-Action Pipeline architecture of Programmable Switch.
        3. NetMigrate solution
            1. Based on the Hybrid migration approach ([30] Fulva)
                1. Also borrowed PriorityPulls from Rockstready [37] the Destination-based approach.
            2. Use programmable switch on TOR to track which key range has migrated, and direct packets to the right source/dest side.
            3. On switch SRAM is limited.
                1. Use BloomFilter to track which key has migrated. Merge keys into groups by consecutive range.
                2. Use Counted BloomFilter to track keys in-progress of migration. The number of keys in-progress of migration is limited.
            4. Maintain query consistency
                1. Data is consistent when not started migration, or after migration.
                2. Double-READ is used, only for keys within on-going migration, so extra cost is limited.
                3. My questions
                    1. How can transaction be executed during on-going migration?
                    2. What about zero downtime live migration for more complex schema or database?

    n. Related materials
        1. Fulva: Efficient live migration for in-memory key-value stores with zero downtime    [2019, 3 refs]
           https://i.cs.hku.hk/~heming/papers/srds19-fulva.pdf
            1. NetMigrate is very similar to Fulva except NetMigrate
                1) Leverages Programmable Switch
                2) Uses BloomFilter to track migration progress
                3) Only on-going migration needs to send to both nodes
            2. Highlights
                1. Fulva steps
                    1. Redirect write requests to dest node
                    2. Client uses Fulva RPC lib to track migration progress
                    3. Reads for already-migrated entries, are sent to dest node
                    4. Reads for not-yet-migrated entries, are sent to both nodes
                        1. My questions
                            1. Why not only send reads to on-going migrate entries to both nodes?
                            2. Since read and write are served by different nodes, how can read-modify-write transaction be executed?
                2. Fulva RPC lib and migration progress tracking
                    1. Migration completion ranges (MCR) to track which range completed migration
                    2. Sampling Pull (SampPull) to identify hot tuples to prioritize migration
                3. Fulva is implemented using DPDK and integrated it with RAMCloud

        2. Rocksteady: Fast Migration for Low-latency In-memory Storage    [2017, 47 refs, SOSP17]
           https://dl.acm.org/doi/10.1145/3132747.3132784
            1. Destination pull based migration with zero downtime, pauseless. Migration is made fast with parallel batched pipelines. Analysis and implementation is based on RAMCloud
            2. Highlights
                1. Key techniques in Rocksteady
                    1. Zero downtime or say "Pauseless".
                    2. Defer repartitioning until the momnent of pull. Make partitioning decision with latest info dynamically.
                    3. Kernel-bypass and scatter/gather DMA for zero-copy data transfer (rather than one-sided RDMA). DPDK.
                    4. Adaptive parallel pipeline.
                    5. Prioritizes migration of hot records. It creates headroom on source node to allow faster migration. PriorityPull.
                    6. Integrate migration processing with RAMCloud's dispatch/worker model
                    7. Leverage RAMCloud's update/recovery logs and 
                4. Rocksteady is implemented in RamCloud
            3. My questions
                1. How is ownership transfer managed? It also needs to be atomic and propagates to client.
                    1. "All the source needs to keep track of is the fact that the tablet is being migrated: if it receives a client request for a record that is in a migrating tablet, it returns a status indicating that it no longer owns the tablet, causing the client to re-fetch the tablet mapping from the coordinator."

8. What Modern NVMe Storage Can Do, And How To Exploit It: High-Performance I/O for High-Performance Storage Engines    [2023, 11 refs, VLDB23]
   https://vldb.org/pvldb/vol16/p2090-haas.pdf
    1. See "Related materials" which summarizes the most.
    n. Related materials
        1. [VLDB 2023] What Modern NVMe Storage Can Do, And How To Exploit It: High-Performance I/O for High - 张建
           https://zhuanlan.zhihu.com/p/700524651
            1. "这篇论文继续优化 LeanStore 使其能够充分利用多块 SSD 的总 IOPS 以提升系统吞吐，主要思路是采用 4KB page、采用协程以实现上百万 IOPS，采用 SPDK 提高 IO 性能减低 CPU 开销。"
                1. Good paper. It can be used as a reference architecture for storage/database to exploit the full IOPS/bandwidth of modern NVMe SSDs.
                2. See Figure 12, the evaluation results for LeanStore is remarkably good. Figure 13 has a breakdown of each optimization.
            2. Highlights
                1. Key challenges
                    1. 一块 PCIe 4.0 SSD 有超过 1M 的随机读 IOPS，7GB/s 的总带宽。企业级 SSD 的价格大约 $200/TB，比内存便宜了 10-50 倍。
                       虽然可以配置多块 SSD 实现更大存储容量，但现有存储引擎设计却并不能完全发挥它们的总 IOPS 和带宽。
                       即使表现最好的 LeanStore 距离理论上限也还有 3.5 倍的差距。
                        1. This is a good research topic in the recent years
                2. Key observations
                    1. Per benchmark, 4KB page size yields best IOPS, throughput, latency. 90% 随机读的总 IOPS 提升到了 8.9M，完全随机读的总 IOPS 可以达到 12.5M。
                    2. SSD 是个内部高度并行化的设备，提供了多个可以同时读写的数据通道。它的随机读延迟在 100us 级别，一次一个 page 的同步 IO 只能获得 10K IOPS，也就是 40MB/s 的带宽，距离单盘 1.5M IOPS 的上限相去甚远。 
                        1. 8 块 SSD 在不同 IO depth 下的 IOPS。当 IO depth 为 3000 时才能达到极限的 12.5M IOPS。而在单机数据库里实现和管理这 3000 并发是个非常大的挑战。
                    3. Figure 5: Comparison of Linux storage IO interfaces. This chart is useful.
                        1. SQPOLL + IOPOLL 模式的 io_uring，禁掉一些内核功能比如文件系统，RAID，OS page cache 后性能会好很多，使用 32 线程可以打满 IOPS。
                        2. SPDK 的性能最好，CPU 开销最低，3 线程就可以打满 IOPS。
                3. Key solutions
                    1. 系统在每个 CPU core 上启动一个工作线程，工作线程执行一批由 boost coroutine 实现的 user task，coroutine 调度由工作线程的 scheduler 负责，coroutine 调度开销远低于 context switch，只需 ~20 CPU 时钟周期。
                    2. Figure 9: Exemplary sequence of events in a worker thread when handling a page fault in a user task
                        1. 老版本的 LeanStore 使用后台线程 page provider 进行缓存替换，要满足上百万 IOPS 就需要多个 page provider，但具体数量很难提前预知，同时也很难适应动态变化的工作负载。
                        2. 新版本中，像 page provider 这样的后台任务和 user task 一样采用 boost coroutine 实现为 system task，和 user task 一样由 scheduler 调度执行。
                    3. Figure 10: I/O model comparison. We use the all-to-all model, which does not require message passing between threads.
                        1. All-to-All 模型中，每个工作线程都可以读写所有 SSD，工作线程为每个 SSD 都准备了独立的 submission/completion queue，不需要在工作线程间传递消息和线程同步，没有任何特殊角色的线程，只需要 1 个线程就可以把系统跑起来。
                        2. Figure 11: 下图测试对比了 SSD Assignment 和 All-to-All 两种模型，二者性能几乎一致，由于 All-to-All 模型的各种优点，IO backend 采用了该线程模型。
                    4. CPU Optimizations and Scalability
                        1. 当所有 IO 优化实现后，作者发现系统的 CPU 成为新的瓶颈，IOPS 仍旧没有打满。这个小结提了几个 LeanStore 的计算优化。
                        2. 早期 LeanStore 采用了全局大锁保护所有正在进行的 IO 操作，但在多块高性能 SSD 的场景下，这把大锁很快成为了性能瓶颈。作者将 inflight IO 按照 page id 进行分区，每个分区使用各自的小锁
                        3. 另一个显著的开销是 findParent。LeanStore 采用了 pointer swizzling

9. BG3: A Cost Effective and I/O Efficient Graph Database in Bytedance    [2024, 0 refs, SIGMOD24, ByteDance]
   https://dl.acm.org/doi/10.1145/3626246.3653373
    1. The essence of what happened in ByteGraph looks like
        1) Introduce Bw-tree to KV storage by learning from Alibaba ArkDB, and apply the related optimizations to GC, and with customizations.
        2) Convert KV storage into append only blob like Azure Storage stream, and introduced stream and extent (also concepts from ArkDB).
        3) RW to RO replication via logging rather than forwarding write requests. This is common, many storage systems are built atop shared logs or "log is database".
       Besides
        1) Gremlin API is increasingly being adopted as the common graph database API, like SQL for Relational DB.
        2) Bw-tree is increasingly getting adopted in many Internet companies.
       Further
        1）In BG3, RO node only needs to load pages requested by reads. This is a very good design. RW->RO commit replication can also be speeded up this way.
        2) GC by "Update Gradient" and TTL (workload-aware). Update Gradient is an interesting new concept.
        3) 对比 BG3 和 ByteGraph 2.0 (VLDB22) 的论文，可以发现 RocksDB + B-tree (Btree On LSM) 的架构被替换了，成为 Bw-tree on Append Only Blob 。同样的架构也出现在 Alibaba ArkDB (SIGMOD21) 中。 时代开始变化了，LSM-tree 不再是万金油了。
            1. This is very good. The most meaningful finding and soon-to-be game changer here. Given there are so many LSM-tree papers in recent years and LSM-tree is being used almost everywhere.
    
    2. Highlights
        1. Key architecture of ByteGraph
            1. Disaggregated: BGE, BGS, KV storage
            2. Query Execution layer - BGE
            3. In-memory caching layer - BGS
                1. Vertex + properties are stored into KV
                   But Super vertex's adjacency list are organized into edge-tree
                2. Edge-tree is organized in B-tree like data structure
                    1. Note, BGS caches vertices and edges in memory with Vertex Storage and Edge Storage, but the corresponding data is persisted in the underlying KV storage. See ByteGraph VLDB22 paper Section 4.1.
                3. RW node and RO node
                    1. At different AZs
            4. LSM-based KV Storage Engine
                1. e.g., RocksDB [12], TerarkDB [29], as mentioned in ByteGraph VLDB22 paper
                    1. ToplingDB 和 TerarkDB 有什么区别？
                       https://www.zhihu.com/question/507334544/answer/2280166589
                        1. Logged elsewhere
            5. Multiple AZ deployment, geo replication
        
        2. Key challenges of this paper
            1. More cost-efficient storage engine
            2. Workload-aware garbage collection
            3. RW->RO node synchronization within a bounded time interval
        
        3. More cost-efficient storage engine
            1. Introducing Bw-tree to replace the previous B-tree like edge list
                1. Learning from ArkDB: 1) Leverage Bw-tree, rather than the traditional B-tree or LSM-tree
            2. Space Optimized Bw-tree Forest
                1. Cold users / new users' likes are stored in an all data in one Bw-tree
                2. Hot users' likes are stored in each user's own Bw-tree. This separates concurrency conflicts
                    1. Hot is determined by edge count. The more edges a user has, the more frequently they get accessed.
                3. "Space optimized" is reflected in
                    1) Cold users are merged in one Bw-tree
                    2) User dedicated Bw-tree can use shorter keys
                4. My questions
                    1. Per storage optimized, how to efficiently pact records in a Bw-tree page? This seems not mentioned in this paper.
                    2. Why the previous B-tree for edge list is now replaced into Bw-tree? This seems not explained in this paper.
                        1. Looks like even the previous RocksDB is removed. The entire KV storage is using Bw-tree. Compared to the LSM-tree, Bw-tree yields better read performance and is still mostly append-only.
            3. Read optimized Bw-tree
                1. Instead of writing a delta, write a copy-on-write snapshot. See Figure 4. This "defragments" reads.
                2. Effective when both writes and reads a concurrent for the user and reads are heavy.
                3. Per trade off on write amplification increase vs read throughput increase, see Figure 9 and Figure 10 in evaluation.
                4. My questions
                    1. The paper didn't mention when will a Space optimized Bw-tree be converted into Read optimized Bw-tree or back?
                        1. It should be combined using both Space optimized Bw-tree + Read optimized Bw-tree
            4. In general, theses optimizations on Bw-tree are similar to Database table schema denormalization. 

        4. Workload-aware garbage collection
            1. Learning from ArkDB: 
                1) Leverage Bw-tree, 
                2) Separating base stream (cold) and delta stream (hot)
                3) Organize data into stream and extent
            2. Observation: 1) recent data is hot, 2) many data has TTL
            3. Update Gradient
                1. [26] Efficiently Reclaiming Space in a Log Structured Store    [2020, 4 refs]
                   https://arxiv.org/abs/2005.00044
                2. Interesting new concept.
                3. "we log both the time of the update and the count of invalid pages it currently contains."
                   "the update gradient for Extent A is calculated as (3-1)/(t1-t0)."
            3. Solution
                1. Don't only look garbage ratio (fragmentation rate). Instead, GC extents with no recent TTL and low update gradient.
        
        5. RW->RO node synchronization within a bounded time interval
            1. Replicate WAL rather than the previous forwarding write requests
                1. See Figure 7 or descriptions at Section 3.4
                2. "Meanwhile, the three dirty pages generated by the Bw-tree split in RW memory are asynchronously flushed to the shared storage by a background thread pool"
                    1. Delayed flush. It's using "Steal, No Force" technique here like the typical DB transaction
                    2. The delayed flushing is further optimized by Group Commit [19].
                3. Per evaluation, see Figure 12, the recall rate vs packet loss rate. B3 can recall 100% while ByteGraph shows nearly 20% failed to recall in high packet loss scenarios. 
                4. My questions
                    1. Can the step 1~8 in Figure 7 be simplified so as to reduce the total IO count? Avoid double write problem or excessive logging?
            2. Strong consistency guarantees
                1. I.e., once the RW node writes new data into the shared storage, the RO can immediately read the new data from the storage
            3. RO only needs to load necessary pages
                1. "Updates from the RW are applied in RO's memory only when a page is brought into RO's memory due to an upper-layer read request."
                    1. This is a very good design. Replicated what's from Aurora Multi-Master.
                        1. Besides, this further improves the speed of commit replication. Naively, the RW node needs to replicate all writes to RO node before RW node acks user completion. However, in this design, RW node only needs to tell RO node which pages are invalidate. Full replication to RO node is not necessary, until a user reads new pages from RO node; at which time RO node will fetch from the shared storage.
                    2. Sadly the paper didn't go into much details. Except Figure 7 Step 5. The process is organized by logs, pages, and page misses & load from storage.
                    3. This further justifies 读写分离
                        1. Usually you can have only 1 writer node, unless you piece up very delicated consistency control.
                        2. To scale out, then, you need RO nodes.
                        3. Further, RO nodes are allowed to load only necessary pages rather than full checkpoint.
                2. "To improve the efficiency of searching the log area in RO's memory, we built an index keyed by page number. Additionally, we regularly merge multiple modifications of the same page in the log area in the background."
                    1. This is another important optimization.

        6. My questions
            1. In Figure 13 per evaluation, why avg latency somehow dropped when write throughput further increased to 60 Kq/s?

    n. Related materials
        1. ByteGraph: A High-Performance Distributed Graph Database in ByteDance    [2022, 11 refs, VLDB22, ByteDance]
           https://vldb.org/pvldb/vol15/p3306-li.pdf
            1. Logged before

        2. 字节图数据库架构论文 SIGMOD 2024 - 小岛cc
           https://zhuanlan.zhihu.com/p/706651396
            1. This seems one of the authors of ByteGraph BG3. There are many pieces presented in this article but not in the paper.
            2. 我们发现上一代 ByteGraph 架构在字节业务中遇到以下几大痛点：
                1. 基于 LSM-based 的分布式 KV 构建系统，在字节图数据库的 Workload 下面存在一些劣势，主要体现为以下几个点
                    1. KV点查性能差：LSM-based 的 Key-Value 引擎，点查性能相比于 Btree 引擎不够稳定(无论 Compaction 策略采用 Level Compaction 还是 Size Tiered Compaction)，当 BGS 层出现 Cache Miss 时，读延迟不够稳定，而字节内很多场景，如抖音点赞等业务，Workload 都是读多写少，对读延迟有较高要求。
                    2. 写入放大高：采取 Btree On LSM 的架构，叠加了 Btree Page 写入放大（每次修改 Page 中的一行记录，都需要把 Page 写入 KV 系统）和 LSM 内部写放大（一般采用 Level Compaction ），最终总体写入放大较高。
                    3. 冗余的内存层次：分布式 KV 内部采用 RocksDB，当发生 Cache Miss 后，一份数据会同时在 BGS 和RocksDB 的 Block Cache 中缓存，造成了内存冗余，进一步导致了整体服务 TCO 上升。
                2. 基于LSM的分布式KV底存储在做垃圾回收的过程中采用两种策略 (1) RocksDB 默认 KV 不分离，使用 Level Compaction 回收数据 ，(2) TerarkDB 使用 KV 分离策略，Value 部分采用传统的基于垃圾率的空间回收策略。以上两者无法针对 ByteGraph 业务上的冷热访问数据进行针对性的优化。
                3. 随着字节电商，支付等业务的快速发展，越来越多的图计算，图神经网络在图数据上应用，这些应用要求更高的读扩展性，具体来说：当新数据写入ByteGraph 读写节点后，能在极短的时间内稳定的被只读节点读出。基于分布式 KV 的前一代 ByteGraph 实现的最终一致性，无法满足 Time-bounded 主从一致性的要求。
                4. 在字节的社交、推荐和风控的图查询 Workload 中，会涉及到对点邻居的复杂的计算模式，包括对邻居打分排序，过滤等计算。在这类重计算的场景下，2.0 的行存储引擎、执行引擎对只需要分析部分边属性的扫描不友好，以及大批量边的计算在基于行计算引擎中存在较高的解释开销。
            3. Read Optimized Bw-Tree
                1. 字节内大量业务对 ByteGraph 的 Workload 都是写少读多
            4. Workload aware space reclamation
                1. LastTimestamp: 以 Extent中 最晚更新的一条数据的时间戳作为整个extent的时间戳。
            5. I/O Efficient Synchronization Mechanism
                1. 其他系统解决方案：比如 Amazon Aurora / 火山引擎 VeDB 通过读取特定 LSN 的 Page 来解决这个问题（存储层提供多版本读取接口），Aliyun PolarDB 通过延迟 Page 的 Flush 流程，直到 RO 将相关的数据更新到内存中。
                2. BG3 的解决方案：BG3 提出了Unified WAL Stream，通过维护数据的多个版本，并在日志流中写入RW节点的Flush/Update Bw-tree Page Mapping 的操作（称作后台系统日志），将前台用户 WAL 和后台系统日志写到统一的物理日志流里面，RO 节点按顺序回放，总是先回放内存的数据，再看到磁盘更新，避免上文提高 Future Page 的问题
                    1. This is so much alike the UserTransactionLog and SystemTransactionLog in ArkDB
                3. 通过这套设计，我们仅仅依赖一套通用的 Append Only Blob 存储就解决了 Share Storage 架构的问题，工程实现更加简洁
            6. Optimized Column-based Engine
                1. 另一方面，行执行引擎执行框架中的虚函数调用开销和解释开销较高，为了解决这一问题，我们在 3.0 中引入了列执行引擎，以提升执行效率。
                2. BG3 设计了一套基于 Column 优化的存储布局 & 执行引擎

        3. [3] 从一到无穷大 #29 ByteGraph的计算，内存，存储三级分离方案是否可以通用化为多模数据库 - 大家好大家吃了吗
           https://zhuanlan.zhihu.com/p/704956012
            1. 从一到无穷大 #30 从阿里云盘古的屠龙之术看使用blob storage作为统一存储层的优势 - 大家好大家吃了吗
               https://zhuanlan.zhihu.com/p/706218967
                1. "在[3]的评论区中张威大佬提到BG3的存储层已经从kv更换为类似盘古的append only blob系统"
                    1. See Figure 2 in the parent paper, "Append-only Shared Cloud Storage"
            2. "张威: BG3下面也是类似aliyun pangu 的blob 存储，不是kv 了
                大家好大家吃了吗: 想请教下从kv换为blob是因为有什么收益吗，我没有看出来在kv稳定后非这么做的原因
                张威: kv下面一般是rocksdb 存储引擎，首先需要预留很多cpu和磁盘带宽做compaction，另外为了保证延迟稳定的读，一般也需要预留很多内存来做block cache 或者 row cache ，这会造成整体机器单核cpu 能支持的磁盘容量非常有限 而类似于aliyun pangu 或者 azure storage steam layer 的这种append only blob，理论上单盘能提供的iops 和带宽远胜kv ，另外由于api 的简单，它可以使用非常高密度的存储机型，不需要预留磁盘带宽，cpu ，内存啥的。 实测下来存储能省非常多"

        4. ArkDB: a key-value engine for scalable cloud storage services    [2021, 11 refs, SIGMOD21, Alibaba Cloud]
           https://www.youtube.com/watch?v=DV768PnBOxI
            1. SIGMOD21 ArkDB: A Key-Value Engine for Scalable Cloud Storage Services - Simpo
               https://zhuanlan.zhihu.com/p/414054332
                1. Logged before
            2. From the parent paper
                1. the state-of-the-art ArkDB [31] proposed writing base page and delta page data into two separate streams for individual space reclamation. Additionally, ArkDB divides each stream into extents of equal size and tracks the reclaimable space ratio of each extent. 
                3. When triggering space reclamation, ArkDB first targets extents with a high ratio of reclaimable space for data movement, thereby reducing the write amplification rate.

10. 谈谈大模型推理KVCache加速和内存池化 - zartbot
    https://mp.weixin.qq.com/s/FD6GLPHENrDE23R20T7ayA
    n. Related materials
        1. Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving    [2024, 0 refs, Moonshot AI]
           https://yiyibooks.cn/arxiv/2407.00079v3/index.html
           https://arxiv.org/abs/2407.00079
            1. From China's Moonshot AI, Kimi.ai.
               A KVCache-centric disaggregated architecture that separates the prefill and decoding clusters. It also leverages the underutilized CPU, DRAM, and SSD resources of the GPU cluster.
               Under real workloads, Mooncake's innovative architecture enables Kimi to handle 75% more requests.
               Good paper. Everyone is talking about Transfer needs the KVCache. Now Moonshot API pioneers how it's engineered in a distributed cluster.
            2. Highlights
                1. Figure 1:Mooncake Architecture. It shows most key designs.
                2. 这些 SLO 通常涉及满足与延迟相关的要求，主要是首次词符的时间 (TTFT) 和 Token 之间的时间 (TBT)。
                3. 我们发现KVCache的调度是大语言模型服务调度的核心，...，以KVCache为中心的分解架构，名为Mooncake
                4. Mooncake采用了分解式架构，不仅将预填充和解码节点分离，而且将GPU集群的CPU、DRAM、SSD和RDMA资源进行分组，实现分解式KVCache
                5. Conductor 负责根据 KVCache 和工作负载的当前分布来调度请求

            n. Related materials
                1. Mooncake阅读笔记：深入学习以Cache为中心的调度思想，谱写LLM服务降本增效新篇章
                   https://zhuanlan.zhihu.com/p/706097807
                    1. Mooncake分离式架构动机是Prefill和Decode阶段性质不同，Prefill是计算密集，受限算力带宽用不满，Decode是访存密集性，受限带宽算力用不满，所以用同一种硬件部署两阶段往往顾此失彼，不是最有性价比
                    2. 拆分Prefill/Decode之后，LLM推理系统就更像一个分布式内存系统+流处理系统，这就是传统计算机系统研究者最擅长的领域。某大佬和我讲的sys三板斧，batch， cache，调度都可以招呼上。比如，Decode可以进一步拆成Attention和非Attention算子分离调度


        2. 国产大模型第一梯队玩家，为什么pick了CPU？ -  云技术
           https://mp.weixin.qq.com/s/Il22xfBnsYXrA3jo9q81NA

        3. DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model    [2024, 0 refs, DeepSeek.com]
           https://yiyibooks.cn/arxiv/2405.04434v5/index.html
           https://arxiv.org/abs/2405.04434
            1. MoE model which was said to have driven ChatGPT 4. Multi-head Latent Attention (MLA) and DeepSeekMoE. 236B total parameters, 128K context tokens. 
               Compared to DeepSeek 67B, V2 saves 42.5% of training costs, reduces the KV cache by 93.3%, and boosts the maximum generation throughput to 5.76 times.
               The key of MLA is it used a latent vector to replace K, V, Q. Only 1 latent vector needs to cache now in KV cache, much smaller.
               RoPE is a technique from DeepSeek 67B and then adopted for MLA here.
                1. Good. The key technique and innovation is MLA.
            2. Highlights
                1. Why MoE?
                    1. Sparse model that can scale to large number of parameters. MoE models only activate a small subset of experts (specialized sub-models) for each input.
                        1. Different experts within an MoE model can specialize in different aspects of the data.
                        2. MoE models use a gating mechanism to dynamically select which experts to activate for each input.
                        3. DeepSeek-V2 includes 236 billion total parameters, but only 21 billion are activated for each token.
                    2. Because only a subset of experts is trained for each input, MoE models can be trained more efficiently.
                        1. Similar for reducing the cost of inference/generation, or improve the throughput.
                        2. Because of sparse activation, the memory footprint is reduced, this explains why KV cache size is reduced in DeepSeek-V2.
                        3. Also, experts can further be trained in parallel.
                        4. Token-Dropping Strategy: we drop tokens with the lowest affinity scores on each device until reaching the computational budget
                    3. Gate and expert routing
                        1. The base is top-K routing based on an expert's affinity score, see Formula (21). And then there are multiple improvements.
                            1. How is an expert's affinity score calculated?
                                1. Centroid of an Expert - a vector that acts as a summary or representative of the expert's characteristics
                                    1. My questions
                                        1. How is centroid calculated for an expert? Seems not mentioned in this paper
                                2. Affinity score - Calculated by similarity between the token's representation and the expert's centroid, see Formula (22)
                        2. Device-Limited Routing
                            1. To reduce communication cost, the target experts of each token will be distributed on at most 𝑀 devices
                        3. Load balance is considered, they are incorporated as Auxiliary Losses in training
                            1. expert-level load balance, 
                            2. device-level load balance, 
                            3. and communication balance
                    4. Shared experts
                        1. They are along side with routed experts, to mitigate knowledge redundancy
                
                2. Multi-head Latent Attention (MLA)
                    1. MLA significantly compresses the Key-Value (KV) cache into a latent vector, reducing the memory footprint and computational requirements during inference
                        1. This is key that how DeepSeek-V2 reduces KV cache size
                        2. Low-Rank Key-Value Joint Compression
                            1. During inference, MLA only needs to cache (c_t)^𝐾𝑉, so its KV cache has only (𝑑_𝑐)𝑙 elements, while MHA needs to cache 2(𝑛_ℎ)(𝑑_ℎ)𝑙 elements for each token
                            2. we also perform 7 low-rank compression for the queries, even if it cannot reduce the KV cache
                    2. RoPE (Rotary Position Embedding) is an improvement from Transformer's default positional encoding. RoPE preserves relative positional relationships between tokens. And, it can better capture the dependencies between tokens over long distances.
                    3. Figure 3 | Simplified illustration of Multi-Head Attention (MHA), Grouped-Query Attention (GQA), Multi-Query Attention (MQA), and Multi-head Latent Attention (MLA)
                        1. Useful to understand their relations.
                
                3. Infrastructures
                    1. DeepSeek-V2 is trained based on the HAI-LLM framework (High-flyer, 2023), internally developed
                        1. High-flyer. Hai-llm: 高效且轻量的大模型训练工具, 2023. URL https://www.high-flyer.cn/en/blog/hai-llm
                    3. We conduct all experiments on a cluster equipped with NVIDIA H800 GPUs
                        1. Each node inthe H800 cluster contains 8 GPUs connected using NVLink and NVSwitch within nodes. 
                        2. Across nodes, InfiniBand interconnects are utilized to facilitate communications.

            n. Related materials
                1. High-flyer. Hai-llm: 高效且轻量的大模型训练工具, 2023
                   https://www.high-flyer.cn/en/blog/hai-llm
                    0. As referenced in the parent paper
                        1. An efficient and light-weight training framework developed internally by our engineers
                        2. It employs a 16-way zero-bubble pipeline parallelism (Qi et al., 2023), an 8-way expert parallelism (Lepikhin et al., 2021, Gshard), and ZeRO-1 data parallelism (Rajbhandari et al., 2020, ZeRO).
                    0.5. I can see key areas of interest in LLM domain. Very useful, as listed below.
                        1. Training/inference cost reduction
                        2. KV cache
                        3. Attention
                        4. Pipeline scheduling
                            1. DNN compiler and framework
                        5. Chip design
                        6. Model compression
                        7. Large scale infra

                    1. 3D并行: 数据并行、流水并行、张量并行
                    2. ZeRO 数据并行
                        1. HAI-LLM 提供了hai_llm.optim.ZeroOptimizer 工具
                    3. 流水并行：Zero bubble pipeline parallelism
                        1. Prior works: Gpipe 和 PipeDream
                        2. 用户可以继承 hai_llm.builders.base_builder.BaseBuilder 并实现自己的 build_model 方法
                    4. 张量并行: haiscale.tensor 提供多个工具
                    5. 序列并行: Megatron-LM

                    n. Related materials
                        1. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models    [2019, 948 refs]
                           https://arxiv.org/abs/1910.02054
                            1. ZeRO (Zero Redundancy Optimizer). Partition model states to reduce memory size while incurs no extra communication cost.
                            2. Highlights
                                1. Key challenges
                                    1. 1T parameter training. Megatron-LM model parallelism is promising but requires high communication between each model layer, only suitable for single node multi GPU setup.
                            
                            n. Related works
                                1. ZeRO: DeepSpeed: Extreme-scale model training for everyone    [2020, Microsoft]
                                   https://www.microsoft.com/en-us/research/blog/deepspeed-extreme-scale-model-training-for-everyone/
                                    1. Logged before

                                2. DeepSpeed之ZeRO系列：将显存优化进行到底 - basicv8vc
                                   https://zhuanlan.zhihu.com/p/513571706
                                    1. ZeRO将模型训练阶段，每张卡中显存内容分为两类：
                                        1. 模型状态（model states）：Adam状态占75%
                                            1. ZeRO-DP
                                                1. 针对模型状态的存储优化（去除冗余），ZeRO使用的方法是分片（partition），即每张卡只存1/N 的模型状态量，这样系统内只维护一份模型状态。
                                        2. 剩余状态（residual states）：Activation，buffer，fragmentation
                                            1. ZeRO-R
                                            2. 激活值可以用activation checkpointing来大大减少
                                                1. "Activation checkpointing (or gradient checkpointing) is a technique to reduce memory usage by clearing activations of certain layers and recomputing them during a backward pass."
                                                   https://docs.aws.amazon.com/sagemaker/latest/dg/model-parallel-extended-features-pytorch-activation-checkpointing.html
                                    2. 通信数据量分析
                                        1. all-reduce
                                            0. Collective Operations
                                               https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html
                                            1. Step 1: reduce-scatter
                                            2. Step 2: all-gather
                                        2. ZeRO-DP incurs no additional communication overhead when using Optimizer State Partitioning and Gradient Partitioning. If further add Parameter Partitioning, then 1.5x communication overhead.
                                            1. Essentially, All-reduce collects partitions from each node. ZeRO-DP partitions are collected together with All-reduce's. So, no extra communication cost.
                                        3. How happens 1.5x communication cost in P_(os+g+p)?
                                            1. "Therefore, during the forward propagation it needs to receives the parameters for all the other partitions. However, this can be pipelined to avoid the memory overhead."
                                    3. 在DeepSpeed中，P_(os)对应ZeRO-1，P_(os+g)对应ZeRO-2，P_(os+g+p)对应ZeRO-3，一般使用ZeRO-1就足够了。
                                        1. os - optimizer state. g - gradients. p - parameters

                                3. 手把手推导Ring All-reduce的数学性质 - 袁进辉
                                   https://zhuanlan.zhihu.com/p/504957661

                                4. 模型并行训练：为什么要用Megatron，DeepSpeed不够用吗？ - 流逝
                                   https://zhuanlan.zhihu.com/p/670958880
                                    1. The Technology Behind BLOOM Training
                                       https://github.com/huggingface/blog/blob/main/bloom-megatron-deepspeed.md
                                        1. Useful compare table of Megatron vs DeepSpeed training frameworks

                                5. Parallelism in Distributed Deep Learning - Insu Jang
                                   https://insujang.github.io/2022-06-11/parallelism-in-distributed-deep-learning/#pipeline-model-parallelism-model-parallelism
                                    1. Pipeline parallelism (introduced in GPipe), unlike the former two, is inter-layer parallelism; it distributes whole layers into multiple accelerators.
                                    2. Model parallelism means that, a model is splitted into several groups of layers (or stages), and each accelerator handles one stage

                                6. 四大主流大模型训练框架对比--Megatron-LM/DeepSpeed/Colossal-AI/FairScale - Weigao Sun
                                   https://zhuanlan.zhihu.com/p/706178708
                                    1. Useful. Also, checkout what are the key features from the comparison table.

                                    n. Related materials
                                        1. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness    [2022, 1016 refs]
                                           https://arxiv.org/abs/2205.14135
                                            1. 为提高Attention计算的内存访问效率，将矩阵分块从HBM加载到SRAM计算。softmax的处理方法是关键。
                                            2. Highlights
                                                1. See articles

                                            n. Related materials
                                                1. 缓存与效果的极限拉扯：从MHA、MQA、GQA到MLA - 苏剑林
                                                   https://mp.weixin.qq.com/s/yCczYU0po0PvPTa-eh2pfg
                                                    1. 所以，减少 KV Cache 的根本目的是实现在更少的设备上推理更长的 Context，从而实现更快的推理速度以及更低的推理成本。
                                                        1. 要想更详细地了解这个问题，读者可以进一步阅读《FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness》[2]、《A guide to LLM inference and performance》[3]、《LLM inference speed of light》[4] 等文章

                                                    n. Related materials
                                                        1. A guide to LLM inference and performance - Varun Shenoy & Philip Kiely    [2023]
                                                           https://www.baseten.co/blog/llm-transformer-inference-guide/
                                                            1. Good guide to teach how to calculate model performance step by step
                                                            2. operations per byte (ops:byte) ratio
                                                                1. memory bound vs compute bound
                                                            3. arithmetic intensity
                                                                1. attention layers, which are computational expensive
                                                                    1. Prefill
                                                                    2. Autoregressive sampling
                                                                2. the FlashAttention paper 
                                                                    1. Step by step calculation arithmetic_intensity_llama 
                                                                3. Use batching to increase arithmetic_intensity_llama 
                                                            4. Evaluating GPUs for LLM inference
                                                                1. T4 vs A10 vs A100

                                                        2. A Guide to LLM Inference Performance Monitoring -  Kartik Talamadupula    [2024]
                                                           https://symbl.ai/developers/blog/a-guide-to-llm-inference-performance-monitoring/
                                                            1. Popular metrics
                                                                1. Time To First Token (TTFT):
                                                                2. Time Per Output Token (TPOT)
                                                                3. Total generation time


                                                2. flashattention - 才才
                                                   https://zhuanlan.zhihu.com/p/712022315
                                                    1. 主要思想：计算注意力的主要瓶颈是显存访问，因此减少对HBM的读写次数，有效利用更高速的SRAM来进行计算是非常重要的。
                                                    2. tiling，分块
                                                        1. SRAM的读写速度比HBM高一个数量级，但内存大小要小很多。通过kernel融合的方式，将多个操作融合为一个操作，利用高速的SRAM进行计算，可以减少读写HBM的次数，从而有效减少内存受限操作的运行时间。但SRAM的内存大小有限，不可能一次性计算完整的注意力，因此必须进行分块计算，使得分块计算需要的内存不超过SRAM的大小。
                                                        2. tiling的主要思想是分块计算注意力。分块计算的难点在于softmax的分块计算，softmax需要与所有的分数列耦合在一起。 ... 把softmax的计算分成更小的块，最终仍然得到完全相同的结果。

                                                3. FlashAttention-3:Fast and Accurate Attention with Asynchrony and Low-precision - 才才
                                                   https://zhuanlan.zhihu.com/p/712020021
                                                    1. Paper published at year 2024

                                                4. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning - 才才
                                                   https://zhuanlan.zhihu.com/p/712016399
                                                    1. Paper published at year 2023

                                                5. FlashAttention 的速度优化原理是怎样的？ - Civ
                                                   https://www.zhihu.com/question/611236756/answer/3132304304
                                                    1. FlashAttention将优化重点放在了降低存储访问开销（Memory Access Cost，MAC）
                                                        1. 但大多数Efficient Transformer通常只关注FLOPS，忽略了MAC
                                                    2. 通常说Transformer的复杂度为 O(dN^2)。Transformer的复杂度随序列长度的增长呈二次方增长。所以通常基于Transformer的大语言模型的上下文长度都不会特别长。
                                                    3. MAC对计算速度的影响，可以根据计算的密集程度，将operator分为两类
                                                        1. Compute-bound：大矩阵乘法、大channel size的卷积操作等
                                                        2. Memory-bound：逐元素操作（ReLU，Dropout等）、以及Reduce操作（求和、softmax、BatchNorm等）
                                                    4. FlashAttention的核心思路
                                                        1. 降低MAC，即使代价是增加了FLOPS
                                                        2. GPU：SRAM -> HBM -> DRAM
                                                            1. SRAM 19TB/s, size 20MB
                                                            2. HBM 1.5T/s, size 40GB
                                                            3. DRAM 12.8GB/s, size >1TB
                                                        3. 为了减少对HBM的读写，FlashAttention将参与计算的矩阵进行分块送进SRAM
                                                            1. 对于矩阵乘法而言，可以直接通过分块来达到分块计算的目的
                                                            2. 接下来看一下对 softmax 进行分块计算的基本方法
                                                                1. 为避免指数项溢出，使用softmax的稳定版本

                        2. Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism    [2019, 1514 refs]
                           https://arxiv.org/abs/1909.08053
                            1. Typical paper that showcases the model parallelism (MP).
                                1. "Model parallelism (MP) [5, 3] and pipeline parallelism (PP) [10, 11] split the model among processes, in vertical and horizontal way respectively."
                                    1. From: ZeRO: Memory Optimizations Toward Training Trillion Parameter Models
                                       https://arxiv.org/abs/1910.02054
                            2. "intra-layer model parallel"
                                1. "Hence, we partition the first GEMM in this column parallel fashion and split the second GEMM along its rows"

                            n. Related materials
                                1. PTD-P: Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM    [2021, NVIDIA, Microsoft]
                                   https://arxiv.org/abs/2104.04473
                                    1. Logged before

                                2. Megatron-LM: Training Multi-Billion Parameter Language Models Using 走读 - 阿北
                                   https://zhuanlan.zhihu.com/p/524202625

                        3. GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism    [2018, 1580 refs]
                           https://arxiv.org/abs/1811.06965
                            1. Popular Pipeline Parallelism (PP) implementation such as G-pipe

                            n. Related materials
                                1. 图解大模型训练之：流水线并行（Pipeline Parallelism），以Gpipe为例 - 猛猿的文章
                                   https://zhuanlan.zhihu.com/p/613196255
                                    1. Key challenges
                                        1. 横切模型的layer分配到不同GPU。Naive的调度有巨大的Pipeline Bubble。
                                            1. 可见Megatron-LM的按列切分Model Parallel是纵切而不是横切。
                                        2. 中间结果占据大量内存
                                    2. Key solutions
                                        1. 未划分前的数据，叫mini-batch。在mini-batch上再划分的数据，叫micro-batch
                                        2. GPipe图pipeline图，其中，第一个下标表示GPU编号，第二个下标表示micro-batch编号
                                            1. 不同GPU用mini-batch填充了pipeline bubble。
                                            2. 当mini-batch数量M >= 4K时，pipeline bubble变得可以忽略不计
                                                1. Evaluation: 当M=32时，表现最佳，且Transformer基本实现了训练速度和GPU个数的线性关系。
                                        3. re-materialization（active checkpoint）
                                            1. 几乎不存中间结果，等到backward的时候，再重新算一遍forward。用计算量减少GPU内存需求。
                                            2. Similar with activation checkpointing.
                                        4. 减少GPU内存需求，因未micro-batch比mini batch小，1/M。

                        4. PipeDream (1F1B): Generalized pipeline parallelism for DNN training    [2019， 781 refs]
                           https://people.eecs.berkeley.edu/~matei/papers/2019/sosp_pipedream.pdf
                            1. "经典的流水线并行范式有Google推出的Gpipe，和微软推出的PipeDream。两者的推出时间都在2019年左右，大体设计框架一致。主要差别为：在梯度更新上，Gpipe是同步的，PipeDream是异步的。异步方法更进一步降低了GPU的空转时间比。虽然PipeDream设计更精妙些，但是Gpipe因为其"够用"和浅显易懂，更受大众欢迎（torch的pp接口就基于Gpipe）。"
                                1. From: 图解大模型训练之：流水线并行（Pipeline Parallelism），以Gpipe为例 - 猛猿的文章
                                   https://zhuanlan.zhihu.com/p/613196255
                            2. PipeDream introduces the 1F1B scheduling. The key is to start a new micro-batch even before the previous micro-batches finish. It introduces "weight stashing" to adjust the proper weight to use in forward and backward passes.
                                1. Figure 9. Micro-batch 5 uses weights from micro-batch 1 (rather than 4). But Micro-batch 5 uses the same weights in both forward and backward passes.

                            n. Related materials
                                1. PipeDream: 数据并行+流水线 - 立交桥跳水冠军
                                   https://zhuanlan.zhihu.com/p/336849279
                                    1. Key challenges
                                        1. 我们引入了Pipeline的概念：如果我们同时进行多个iteration，每个节点在同一时刻负责不同的iteration的计算，就可以避免数据依赖，不用在原地干等了。
                                        2. 不过这种做法会产生新的问题：在普通情况下，我们算第二个iteration的情况下需要用第一个iteration后更新的模型来算，但是如上所示，对于Machine 1，我第二轮开始跑（深蓝色的2格子）的时候，第一轮（浅绿色的1格子）还没更新完。
                                    2. Key solutions
                                        1. 本质上Pipeline就是一种async SGD，我们来结合示意图看一下最朴素的情况: 我们来看一下Machine2，发现当他在forward算第5个batch（图中第二行深蓝色的5）的时候，它用的weights是更新两次的（即前面浅绿色的1和2更新了两次参数），而当backward算第5个batch（图作用第二行浅绿色的5）时，用到的weights是更新了4次的（即前面浅绿色的1,2,3,4）。无疑这种做法彻底改变了单节点深度学习的很多假设，自然会降低训练的效果（准确率下降）
                                        2. 针对于这个问题，作者提出了Weight Stashing，思路很简单，就是每个node多备份几个版本的weights，forward用哪个weights算的，backward就还用它
                                    3. Others
                                        1. 虽然有很多人提出了async SGD的训练，但是经过无数研究者的检验，发现它带来的精度损失所造成的负面影响远远大于应用它提升的性能。

                                2. FlexFlow: Beyond Data and Model Parallelism for Deep Neural Networks    [2018, 504 refs]
                                   https://arxiv.org/abs/1807.05358
                                    1. 大名鼎鼎的FlexFlow, 自动并行方向的开端。 Later DNN frameworks would move to operator scheduling and compilation mapping to GPU devices to pursuit for parallelism.
                                    2. Highlights
                                        1. Table 1 shows how DP, MP, PP map to SOAP
                                        2. FlexFlow solution
                                            1. Operator Graph
                                            2. Device Topology
                                            3. Execution Optimizer
                                                1. MCMC search algorithm
                                                    1. delta simulation algorithm
                                                    2. Metropolis-Hastings algorithm [21]
                                                2. Execution simulator
                                                    1. Task graph
                                                3. Distributed runtime

                                    n. Related materials
                                        1. FlexFlow Serve: Low-Latency, High-Performance LLM Serving
                                           https://github.com/flexflow/FlexFlow?utm_source=talkingdev.uwl.me
                                            1. Speculative Inference - Interesting new technique
                                                1. Parallel Processing: The system generates multiple possible next tokens in parallel using smaller models. This speeds up the inference process since these models are much faster and less resource-intensive than the full LLM.
                                                2. Verification Step: After generating speculative outputs, the system verifies them using the larger, more accurate model. If the predictions match, the speculative outputs are used directly; if not, the system reverts to the traditional inference method.
                                                3. Tree-Based Approach: In the context of FlexFlow Serve, a tree-based speculative inference approach is used. This method organizes possible token sequences into a tree structure, allowing for more efficient management of the speculative predictions and their verification.
                                                    1. Verification happens at the decoding step.

                                        2. 读论文《FlexFlow-Beyond Data and Model Parallelism for Deep Neural Networks》 - 鲁凯
                                           https://zhuanlan.zhihu.com/p/464355830
                                            1. Key summaries
                                                1. 相比于data-parallel和model-parallel，提出了更多维度的split方案。SOAP（sample，operator，atrribute，param）这四个维度的split方案。
                                                2. 在四个维度之上，提出了一种在候选空间搜索的方案
                                                3. 提出了一个更加轻量的simulator，可以更快速的对proposed split strategy做evaluate。相比直接执行的方案提升了3个数量级。
                                                4. 实现了总体的框架FlexFlow
                                            2. Good, it brings DB optimizer / operator scheduling into LLM parallelism
                                                1. 自动并行方向的开端
                                                2. Also, a next related parallel direction is MoE.
                                                    1. Here to summary the different parallelism schemas. Very useful.
                                                        1. Data parallel, Tensor parallel, Model pipeline parallel
                                                        2. 3D 并行（ZeRO-DP + PP + TP）
                                                        3. Auto parallel (distributed compiler)
                                                        4. MoE（Expert parallelism）

                                        3. 大模型分布式训练并行技术（九）-总结 - 吃果冻不吐果冻皮的文章
                                           https://zhuanlan.zhihu.com/p/667051845
                                            1. Useful articles to walk through each key areas
                                            2. 大模型分布式训练并行技术（一）
                                               概述大模型分布式训练并行技术（二）
                                               数据并行大模型分布式训练并行技术（三）
                                               流水线并行大模型分布式训练并行技术（四）
                                               张量并行大模型分布式训练并行技术（五）
                                               序列并行大模型分布式训练并行技术（六）
                                               多维混合并行大模型分布式训练并行技术（七）
                                               自动并行大模型分布式训练并行技术（八）
                                               MOE并行大模型分布式训练并行技术（九）

                                        4. 大模型分布式训练并行技术（七）-自动并行 - 吃果冻不吐果冻皮
                                           https://zhuanlan.zhihu.com/p/662517647
                                            1. 目前，很多的通用AI框架（如：PaddlePaddle、OneFlow、PyTorch、MindSpore、TensorFlow、JAX等）都对自动并行(全自动或半自动)进行了实现。
                                            2. FlexFlow
                                                1. 本文定义了一个 DNN 并行策略搜索空间（SOAP），其中，包括在Sample、Operator、Attribute和Parameter维度中并行 DNN 的策略；同时，本文还提出了 FlexFlow，这是一种深度学习框架，它使用 SOAP 空间的引导随机搜索来寻找针对特定的并行机器的快速的并行策略。
                                                2. 为了加速这种搜索，FlexFlow 引入了一种新颖的执行模拟器（execution simulator），它可以准确预测并行策略的性能，并且比之前直接执行每个策略的方法快三个数量级。
                                                3. 总之，FlexFlow 最核心工作就是提出了 execution simulator 来完善 cost model 。

                                3. 为什么现在的LLM都是Decoder only的架构？ - 成诚
                                   https://www.zhihu.com/question/588325646/answer/3422090041
                                    1. 个人觉得 Decoder-Only 的架构最核心的优势是非常方便于 Scale Up，基于 Scaling Laws 的实际训练成本最低
                                        1. 在 LLM 时代，如果你提出的新的算法结构可能有 5% 的效果提升，但是引入了额外 50% 的训练成本（计算时间 or 通信量） 的话，那这个新的算法一定是一个负优化。 因为这 50% 的训练成本，基于 Scaling Laws 我可以在原模型上多训练 50% 的 tokens ，或者训练大一半的模型， 带来的最终提升都远大于新算法的 5%。 因此，新的算法研究必然在探索阶段就需要引入 Infra 因素的考量。
                                    2. Transformer has an encoder and a decoder
                                       https://medium.com/@minh.hoque/a-comprehensive-overview-of-transformer-based-models-encoders-decoders-and-more-e9bc0644a4e5
                                    3. Llama is a decoder-only language model
                                       https://medium.com/@utsavtiwari9936/introduction-to-llama2-part-1-architectural-analysis-3e335e7b1104
                                        1. Llama uses a new kind of positional embedding mechanism called Rotary Position (RoPE)

                        5. Gshard: Scaling giant models with conditional computation and automatic sharding    [2020, 813 refs, Google]
                           https://arxiv.org/abs/2006.16668
                            1. 600B parameters MoE model with automatic sharding. Lightweight annotation APIs and an extension to the XLA compiler. Sparsely-Gated Mixture-of-Experts.
                            2. Highlights
                                1. Key principles 
                                    1. Sub-linear Scaling - Interesting point that shows why need MoE
                                        1. Of computation and communication cost vs model capacity
                                        2. Conditional computation by having a sub-network activated on the per-input basis
                                        3. Adding Position-wise Sparsely Gated Mixture-of-Experts (MoE) layers [16]
                                    2. The Power of Abstraction 
                                        1. Developer writes model network architecture as if on single node, XLA compiler translates partitioning and physical assignment
                                        2. GShard, user still needs to annotate a few critical tensors.
                                    3. Scalable Compilers
                                        1. Including compilation would scale to thousands of devices
                                2. Model
                                    1. Adding MoE layers to Transformer
                                        1. See Formula (3) for what is the MoE layer
                                    2. Choosing the Gate function
                                        1. Naive TopK softmax experts would have problem of load imbalance to experts
                                        2. Algorithm 1
                                            1. Expert capacity: To ensure load balanced, the number of tokens taken by an expert is below a uniform threshold
                                                1. Local group dispatching - parallel processed groups to ensure expert capacity
                                                    1. My questions
                                                        1. Local group dispatching is for data partitioning parallelism?
                                            2. Auxiliary loss - the classic load balance method
                                                1. also seen in DeepSeek
                                                2. we want to minimize mean square of c_e/S, which is the fraction of input routed to each expert. 
                                                3. The bias of load balance is considered a loss and then added to model loss
                                            3. Random routing
                                                1. If the weight of 2nd expert is small, we can ignore it. GATE(·) dispatches to the 2nd-best expert with the probability proportional to its weight g2
                                    3. GShard Annotation API for Parallel Execution
                                        1. APIs in TensorFlow/Lingvo
                                        2. replicate(tensor) annotates tensor to be replicated across partitions
                                        3. split(tensor, split_dimension, num_partitions) annotates tensor to be partitioned along split_dimension
                                        4. shard(tensor, device_assignment) generalizes split() to allow partitioning multiple dimensions


                            n. Related materials
                                1. 如何评价Google的GShard论文？ - 袁进辉的回答
                                   https://www.zhihu.com/question/404721763/answer/2111040851
                                    1. 好的，文献综述到此位置，我们总结一下：
                                        1. 所有这些工作的目的都是提供一个与编程语言"类型系统"类似的annotation 体系，这个体系需要最简且完备，这个体系定义了"自动并行"的搜索空间。
                                        2. 搜索空间中的任何一种构型，也就是任何一种并行策略，在数学上都是正确的，它们的区别仅仅是执行效率不同，我们目的是找到效率最高的并行策略。
                                        3. 框架需要这样一种能力，给定任何一种构型，都能翻译和转换成一个物理图（执行计划），确保这个并行策略可以成功执行，即使它的效率不高。
                                        4. 框架最好能够自动搜索到效率最高的那个构型。

                                2. 分布式深度学习的数学抽象：从GShard谈起 - OneFlow
                                   https://zhuanlan.zhihu.com/p/433869519

                                3. 大模型分布式训练并行技术（八）-MOE并行 - 吃果冻不吐果冻皮
                                   https://zhuanlan.zhihu.com/p/662518387
                                    1. Sparse MoE
                                        1. GLaM比GPT-3大7倍，但是由于使用了Sparse MoE的设计，训练成本却只有GPT-3的1/3，并且推理过程中的计算量减少了约一半；同时，在29个NLP任务上超越了GPT-3。
                                        2. 从 Google 发布的很多的论文和超大参数规模模型（千/万亿参数）可以看到，其基本都使用了 MOE 架构。除此之外，业界很多的AI训练框架中也继承了 MOE 并行，比如：PaddlePaddle、DeepSpeed、ColossalAI等。
                                    2. GShard 是第一个将 MoE 的思想拓展到 Transformer 上的工作
                                        1. 把 Transformer 的 encoder 和 decoder 中每隔一个（every other）的FFN层，替换成 position-wise 的 MoE 层，使用的都是 Top-2 gating network
                                        2. 此处之外，GShard还加入了很多其他设计：
                                            1. Expert capacity balancing：强制每个expert处理的tokens数量在一定范围内。
                                            2. Local group dispatching：通过把一个batch内所有的tokens分组，来实现并行化计算。
                                            3. Auxiliary loss：为了缓解"赢者通吃"问题，尽可能把token均分给各个专家。
                                            4. Random routing：在Top-2 gating的设计下，两个expert如何更高效地进行routing。

                                4. GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding 论文翻译与精读 - 为什么-不养猫
                                   https://zhuanlan.zhihu.com/p/672837901

                                5. [28] XLA compiler: Optimizing Compiler for TensorFlow
                                   https://www.tensorflow.org/xla
                                    1. Operation fusion
                                    2. Hardware-specific optimization
                                    3. Improve memory usage
                                    4. Automatic differentiation

                        6. ZB-H1/ZB-H2: Zero bubble pipeline parallelism    [2023, 6 refs]
                           https://arxiv.org/abs/2401.10241
                            1. Our method outperforms the 1F1B schedule up to 23% in throughput under a similar memory limit.
                                1. Good improvement. ZB-H2 is zero bubble
                            2. Highlights
                                1. Opensourced our implementation based on the popular Megatron-LM repository on https://github.com/sail-sg/zero-bubble-pipeline-parallelism
                                2. Key techniques
                                    1. Improving from PipeDream 1F1B. See Figure 3 ZB-H2, it almost has zero bubble
                                    2. Different from PipeDream 1F1B, ZB-H* further splits B step into B and W steps. 
                                    3. Warm-up and Steady Phases
                                    4. Bypassing optimizer synchronizations

                            n. Related materials
                                1. 【分布式训练技术分享五】聊聊 Zero Bubble Pipeline Parallelism - LLM迷思
                                   https://zhuanlan.zhihu.com/p/670301574

                                2. Zero Bubble 并行策略 - AndSonder
                                   https://zhuanlan.zhihu.com/p/685417501

                2. 缓存与效果的极限拉扯：从MHA、MQA、GQA到MLA - 苏剑林
                   https://mp.weixin.qq.com/s/yCczYU0po0PvPTa-eh2pfg
                    1. DeepSeek-V2 ... 如此便宜的价格背后的关键技术之一是它新提出的 MLA（Multi-head Latent Attention），这是对 GQA 的改进
                    2. 本文将跟大家一起梳理一下从 MHA、MQA、GQA 到 MLA 的演变历程
                        1. MHA - Multi-Head Attention
                            1. Multi-Head Attention, 是开山之作《Attention is all you need》所提出的一种 Attention 形式
                        2. MQA - Multi-Query Attention
                            1. 让所有 Attention Head 共享同一个 K、V
                        3. GQA - Grouped-Query Attention
                            1. 有人担心 MQA 对 KV Cache 的压缩太严重，为此，一个 MHA 与 MQA 之间的过渡版本 GQA 应运而生
                    3. MLA - Multi-Head Attention
                        1. 此时 KV Cache 只需要存下所有的 c_i 就行
                        2. 如果我们只需要跟 GQA 相近的能力，那么是不是就可以再次减少 KV Cache 了？d_c 取更小值
                        3. 不兼容 RoPE 的问题。

                3. LLaMA-13B: LLaMA: Open and Efficient Foundation Language Models    [2023, 7562 refs, Facebook]
                   https://arxiv.org/abs/2302.13971
                    1. LLaMA-13B, LLaMA-65B. LLaMA-13B outperforms GPT-3 while being more than 10× smaller, and LLaMA-65B is competitive with Chinchilla-70B and PaLM-540B
                    2. Highlights
                        1. Github: https://github.com/meta-llama/llama
                           https://github.com/facebookresearch/llama

                    n. Related materials
                        1. LLaMA 超详细解读（paper & code） - JOYWIN
                           https://zhuanlan.zhihu.com/p/632102048
                            1. LLaMA 是目前为止，效果最好的开源 LLM 之一。LLaMA-13B 优于 GPT-3，尽管只有1/10大小。 LLaMA-65B 是可以与 Chinchilla-70B 和 PaLM-540B 这种最佳的LLM相竞争的模型。
                            2. 使用了基于transformer的架构，并做了如下3点改进
                                1. Pre-normalization
                                    1. 为了提高训练的稳定性，对每个transformer层的输入进行归一化，而不是输出进行归一化。
                                2. SwiGLU
                                    1. 使用SwiGLU替代了ReLU作为激活函数。和PaLM中不同，维度采用 2/3*4d 而不是 4d 。
                                3. RoPE
                                    1. RoPE 的核心思想是"通过绝对位置编码的方式实现相对位置编码"，可以说是具备了绝对位置编码的方便性，同时可以表示不同 token 之间的相对位置关系。
                            3. 加速训练
                                1. 使用了xformers库。
                                2. 减少了activation checkpointing 中，重新计算 activation 的计算量。手动实现 transformer 层的反向传递函数，保存了计算成本高的 activations，例如线性层的输出。
                                3. 通过使用 model parallelism 和 sequence parallelism 来减少显存的使用量。
                                4. 尽可能地将 activations 的计算和GPU之间的通讯进行并行。
                                5. 效果
                                    1. 65B的模型，在2048个80G的A100 GPU上，可以达到380 tokens/sec/GPU的速度。训练1.4T tokens需要21天。
                                    2. 数据集
                                        1. 一共有1.4T的tokens

                        2. 如何看待MetaAI开源Llama3大模型？ - 终端研发部
                           https://www.zhihu.com/question/653375287/answer/3495071576
                            1. Llama 3 采用了一种相对传统的纯解码器架构，即基于Transformer的模型。与前代Llama 2模型相比，Llama 3 在以下几个关键方面进行了显著的改进：
                                1. 分词器和词汇表：Llama 3 引入了一个具有128K标记的分词器，这比前代模型的词汇表更大，从而使得模型能够更精确地编码语言信息，显著提升了性能。
                                2. GQA：为了增强模型的推理效率，Llama 3 在8B和70B两种规模的模型中都实施了分组查询注意力技术，这是一种优化的自注意力机制，可以提高处理长距离依赖关系时的效率。
                                3. 序列长度和自我注意力：Llama 3 在8192个令牌的序列上进行训练，利用掩码机制确保自我注意力操作不会跨越文档边界，这有助于模型更好地处理长文本数据。

        4. 目前针对大模型剪枝的方法有哪些？ - 吃果冻不吐果冻皮
           https://www.zhihu.com/question/652126515/answer/3457652467
            1. 分类
                1. 模型剪枝（Pruning）
                    1. 非结构化剪枝方法 - 非结构化剪枝通过删除特定参数而不考虑其内部结构来简化 LLM
                    2. 结构化剪枝方法 - 结构化剪枝通过删除整个结构组件（例如：神经元、通道或层）来简化 LLM
                2. 知识蒸馏（Knowledge Distillation）
                3. 模型量化（Quantization）
                4. 低秩分解（Low-Rank Factorization）

        5. 大模型的高效训练：从Infra到框架优化 - sunp0003
           https://zhuanlan.zhihu.com/p/711683629
            1. 这篇综述文章全面概述了LLM训练系统和基础设施的最新进展。从分布式训练基础设施到训练系统本身，探讨了GPU集群、高性能网络和为LLM工作负载定制的分布式存储系统的创新设。文章还深入分析了分布式训练系统的关键要素，包括并行策略、计算、通信和内存优化。文章还探讨了提高训练可靠性的容错机制。
            2. Efficient Training of Large Language Models on Distributed Infrastructures: A Survey    [2024, 0 refs]
               https://arxiv.org/abs/2407.20018
                1. Good paper to understand LLM infa landscape. The Figures are very useful. 
                2. Highlights
                    1. Figure 1. The general topics in LLM domain
                        1. Section 3 Infrastructure 
                                Section 3.1 AI Accelerators 
                                Section 3.2 Network Infrastructure 
                                Section 3.3 Storage 
                            Section 4 Parallelism Schemes 
                                Section 4.1 Hybrid Parallelism 
                                Section 4.2 Auto Parallelism 
                                Section 4.3 Heterogeneous Parallelism 
                            Section 5 Computation Optimizations 
                                Section 5.1 Operator Optimization 
                                Section 5.2 Mixed-Precision Training 
                            Section 6 Memory Optimizations 
                                Section 6.1 Activation Recomputation 
                                Section 6.2 Redundancy Reduction 
                                Section 6.3 Defragmentation 
                                Section 6.4 Offloading 
                            Section 7 Comm. Optimizations 
                                Section 7.1 Collective Communication 
                                Section 7.2 Communication Scheduling 
                                Section 7.3 In-Network Aggregation 
                            Section 8 Fault Tolerance 
                                Section 8.1 Failure Analysis 
                                Section 8.2 Anomaly Detection 
                                Section 8.3 Checkpoint-Based Recovery 
                                Section 8.4 Checkpoint-Free Recovery
                    2. Figure 5. Different chip-to-chip networking topologies
                        1. tree topology, cube-mesh topology, switch-based fully-connected topology, P2P-based fully-connected topology, and 2D-torus topology

            n. Related materials
                1. Full Stack Optimization of Transformer Inference: a Survey    [2023, 51 refs]
                   https://arxiv.org/abs/2302.14017
                    1. Good in detail analysis on model arithmetic intensity.
                    2. Highlights
                        1. Analysis on transformer architecture bottlenecks
                            1. Analytical Modelling
                            2. Non-linear operations
                        2. Accelerator designs
                            1. Gemmini, the open-source, full-stack deep neural network accelerator generator
                        3. Model optimization
                            1. Quantization
                            2. Sparsity (AKA. pruning)
                            3. Transformer-specific Optimization
                                1. Accelerating Attention
                                2. Reduce Non-linear operations
                                3. Accelerating Decoding
                        4. Mapping transformers to hardware
                            1. graph-level mapping
                            2. operation-level mapping
                            3. [128] The deep learning compiler: A comprehensive survey    [2021]
                            4. Mapping strategies, schedulers
                        5. Neural Architecture Search
                            1. Case Study: NAS search for Pareto-optimal architectures
                   
                    n. Related materials
                        1. UC Berkeley：Transformer推理全栈优化研究进展综述 - eyesighting
                           https://zhuanlan.zhihu.com/p/663879289

                2. A Survey on Efficient Inference for Large Language Models
                   https://yiyibooks.cn/arxiv/2404.14294v3/index.html
                   https://arxiv.org/abs/2404.14294
                    1. Good paper, now we have surveys on model training, inference, and model optimization
                    2. Highlights
                        1. Fig. 4. Taxonomy of efficient inference methods for Large Language Models
                            1. Data-level optimization
                                1. Input compression
                                    1. Prompt pruning
                                    2. Prompt summary
                                    3. Soft prompt-based compression
                                    4. RAG (Retrieval-augmented generation)
                                2. Output organization
                            2. Model-level optimization
                                1. Efficient structure design
                                    1. Efficient FNN design
                                    2. Efficient attention design
                                        1. Low-complexity attention
                                        2. Multi/Group-query attention
                                    3. Transformer alternative
                                2. Model compression
                                    1. Quantization
                                        1. Post-training quantization
                                        2. Quantization-aware training
                                    2. Sparsification
                                        1. Weight pruning
                                        2. Sparse attention
                                    3. Structure optimization
                                        1. Structure Factorization
                                        2. Neural architecture search
                                    4. Knowledge distillation
                                        1. White-box KD
                                        2. Black-box KD
                                    5. Dynamic inference
                            3. System-level optimization
                                1. Inference engine
                                    1. Graph and operator optimization
                                    2. Offloading
                                    3. Speculative decoding
                                2. Serving system
                                    1. Memory management
                                    2. Batching
                                    3. Scheduling
                                    4. Distributed systems
                        2. The paper is nicely written in that the first sentence in each section user-friendly tells what the technique does and why.

                    n. Related materials
                        1. 3万字详细解析清华大学最新综述工作：大模型高效推理综述 - fanmetasy
                           https://zhuanlan.zhihu.com/p/701417546

        6. 【芯片论文】存内计算(CIM)与近存计算(CNM)论文总结 - eyesighting
           https://zhuanlan.zhihu.com/p/676381771
            1. 本文总结了存内计算(CIM：Computing In Memory)、存内处理(PIM：Processing In Memory)、近存处理(PNM：Processing Near Memory)、近存计算(PNM：Computing Near Memory)领域的一些论文
            2. Memory-Centric Computing
                1. 1）使用内存进行处理，它利用内存结构的模拟操作特性在内存中执行大规模并行操作，2）近内存处理，它集成了内存控制器、逻辑和内存控制器中的处理能力。 3D 堆叠内存技术或内存芯片层，可实现对近内存逻辑的高带宽和低延迟内存访问。

        7. CachedAttention(原AttentionStore) - 手抓饼熊
           https://zhuanlan.zhihu.com/p/706249272
            1. 主要目的是解决多轮会话的问题
                1. 用一个session关联多轮会话，多轮会话之间的kv cache保存起来
                2. 多轮会话由于不知道什么时候结束，所以需要保存的kv cache时间就很长，那么此时kv cache放在gpu上就不合理了，应该放在cpu和磁盘上
                3. kv cache放在cpu上，那么加载的话，就要考虑性能问题，按照layer加载可以做到计算通信重叠
                4. kv cache放在磁盘上，直接从磁盘上去加载到gpu上肯定是不合适的，那么先需要从磁盘加载到cpu上，再按照3的方式从cpu加载到gpu上
                5. 针对第4步，那么如果请求需要计算的时候，再做第这个就肯定迟了，但是推理引擎不是有调度器嘛，请求实在调度器里排队的，调度器可以提前去进行磁盘到cpu的加载
                6. 3.4节分析历史标记超出上下文窗口的限制时的处理
                    1. "To address this problem, AttentionStore enables the KV caches after truncation to be still valid via decoupling the positional encoding"
            2. 讲到这里的时候做搜广推的同学是不是感觉很眼熟，这方法用于大模型的多轮会话真的是绝妙
            3. 根据上面的分析，我们发现，如果KV缓存可以在多次对话中重复使用，那么预填充成本可以减少高达98%
            4. The original paper
                1. AttentionStore: Cost-effective Attention Reuse across Multi-turn Conversations in Large Language Model Serving    [2024, 0 refs]
                   https://arxiv.org/pdf/2403.19708v2

            n. Related materials
                1. Efficient LongTerm Memory Management - 手抓饼熊
                   https://zhuanlan.zhihu.com/p/709926136
                    1. 相同类型的文章如: CachedAttention / AttentionStore
                    2. The original paper
                        1. Improving Large Language Model Throughput with Efficient LongTerm Memory Management    [2024, 0 refs]
                           https://people.eecs.berkeley.edu/~kubitron/courses/cs262a-F23/projects/reports/project1010_paper_64287652274076362722.pdf
                            1. Built on top of PagedAttention. Extending vLLM
                                1. vLLM: https://github.com/vllm-project/vllm
                            2. Switch Prefix Cache between GPU memory, CPU memory, and disk. New policies.

11. MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs    [2024, 27 refs, NSDI24, ByteDance]
    https://www.usenix.org/conference/nsdi24/presentation/jiang-ziheng
    https://www.youtube.com/watch?v=qa6q7J0hVUI
    1. Good. In-depth and in-detail optimization with many engineering experiences in large scale. Besides, stability and in-depth observability are key to high MFU.

    n. Related materials
        1. 【分布式训练技术分享七】聊聊字节 AML 万卡工作 MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs - LLM迷思
           https://zhuanlan.zhihu.com/p/684619370
            1. A stable production system MegaScale, >10K GPU cards training. co-designs algorithm and system across model block and optimizer design, computation and communication overlapping, operator optimization, data pipeline, and network performance tuning. Fault tolerance and mitigate stragglers. 
               In-depth observation is key to address stability issues on large scale. We develop a set of diagnosis tools to monitor system components and events. 
               Achieves 55.2% Model FLOPs Utilization (MFU) when training a 175B LLM model on 12,288 GPUs, improving the MFU by 1.34x compared to Megatron-LM
               The platforms ByteDance is using seems Kubernetes/K8S and MegaScale is modified from Megatron-LM.
            2. Highlights
                1. Key challenges
                    1. High MFU while training.
                    2. Stability is a necessity to high MFU.
                2. Key principles
                    1. 算法与系统的协同设计
                    2. 深入的可视化性
                3. 修改/优化包括：
                    1. 并行Transformer、滑动窗口注意力和LAMB 优化器。
                        1. Parallel transformer block. Attention block 和 MLP block 的计算可以并行执行
                        2. Sliding window attention (SWA). 滑动窗口 attention 是一种稀疏注意力机制，它在输入序列中的每个标记周围使用一个固定大小的窗口
                        3. LAMB optimizer. LAMB优化器已经证明可以将 BERT 的训练 batch size 扩展到 64K 而不降低准确性. MegaScale 减少了87.5%的 pipeline bubbles
                    
                    2. 利用混合并行策略，包括数据并行、流水线并行、张量并行和序列并行。
                        1. 重要的是，针对每种并行策略的模式设计了定制的技术，以最大程度地增加通信和计算之间的重叠。
                        2. Overlapping in data parallelism. 受 PyTorch FSDP 的启发，初始的 all-gather 操作在每次迭代开始时预取，使其能够与数据加载操作重叠，有效地将通信时间减少了1 /（2 * vpp_size）的因子
                        3. Overlapping in pipeline parallelism. interleaved 1F1B 调度方法，将发送和接收操作解耦，使发送操作能够与计算重叠。
                            1. Related: Zero Bubble Pipeline Parallelism    [2023]
                               https://arxiv.org/abs/2401.10241
                        4. Overlapping in tensor/sequence parallelism. 将 all-gather 和 reduce-scatter 与 FFN 路径上的并行线性层融合在一起

                    3. 应用 prefetching 和 treebased loading 来优化数据流水线。
                        1. attention part：采用了FlashAttention-2
                        2. LayerNorm 和 GeLU：将这些 kernel fuse 在一起
                    
                    4. 利用 non-blocking asynchronous operations 操作，并消除大规模集体通信组初始化的全局 barriers。
                        1. 异步数据预处理：数据预处理不在关键路径上
                        2. Redundant dataloader elimination：基于两层tree-based 的方法，在每台机器上使用一个单独的专用数据加载器将训练数据读入一块共享内存中。随后，每个 GPU 负责将必要的数据复制到对应的 GPU 内存中
                    
                    5. 设计了自定义的网络拓扑，减少了 ECMP 哈希冲突，定制了拥塞控制，并调整了重传超时参数以实现高网络性能。
                        1. 初始化时间过长（2048 GPU Megatron-LM 从 1047 秒，MegaScale 优化至 30 秒）
                            1. 同步步骤问题：每个进程在初始化特定通信组结束时都会进行 barrier 操作。解决：将 TCPStore 替换为 非阻塞、异步的 Redis。
                            2. 问题：全局 barrier 的不谨慎使用。解决：最小化对全局 barrier 的需求，将全局 barrier 的时间复杂度从O(n^2) 降低到 O(n)。
                        2. Network Performance Tuning
                            1. Topology
                                1. 字节的数据中心网络采用基于 Broadcom Tomahawk 4 芯片的高性能交换机构建。每个 Tomahawk 芯片的总带宽为 25.6Tbps，具有 64 个400Gbps端口。
                                2. 三层交换机以类似 CLOS 的拓扑结构连接，用于连接超过 10,000 个 GPU。对于每一层的交换机，下行链路和上行链路之间的带宽比例为1:1。
                            2. Reducing ECMP hashing conflicts
                                1. 将一个 400 G下行链路端口分成两个带有特定 AOC 电缆的 200G 下行链路端口
                                2. 服务器上的 8 个200G 网卡以多重连接方式连接到 8 个不同的交换机上
                                3. 将训练任务中的数据密集节点调度到同一个机架顶部（ToR）交换机下运行
                            3. 拥塞控制。
                                1. 当默认使用 DCQCN 协议时，all-to-all 通信可能导致拥塞和过度使用优先级流控制（PFC）
                                2. 字节开发了一种算法，结合了 Swift 和 DCQCN 的原理，将往返时延（RTT）的精确测量与显式拥塞通知（ECN）的快速拥塞响应能力相结合
                            4. Retransmit timeout setting
                                1. 可以通过设置 NCCL 中的参数来控制重传计时器和重试次数，我们调整这些参数以实现在链路抖动下的快速恢复
                                2. 为了进一步减少恢复时间，我们在网卡上启用了 adap_retrans 功能

                4. Fault Tolerance
                    1. The cluster manager is Kubernetes/K8S. Pod has daemon process to detect failure via heartbeat.
                    2. RDMA 流量指标起到了关键的指示作用。
                        1. 由于训练任务的周期性特性，每个步骤的网络流量特征应该呈现类似的模式。因此，RDMA 流量的显著下降或异常波动是潜在异常的信号。在检测到这种异常情况时，驱动程序将发出警报以进行手动调查。如果流量完全停止，驱动程序将自动启动故障恢复过程。
                    3. Diagnostic Tests
                        1. 在自检诊断中，执行时间和准确性之间存在权衡。延长诊断持续时间可能会对有效的训练时间产生不利影响，而高误报率可能会导致对实际上正常工作的机器进行不必要的排除
                        2. Intra-host network tests:
                            1. Loopback, RNIC to RNIC
                        3. NCCL tests
                            1. 在单个节点内的所有 GPU 之间运行全互连测试
                            2. 同一 ToR 交换机下与相邻机器进行全归约测试
                    4. Fast Checkpointing and Recovery
                        1. 这要求在训练过程中增加检查点的频率，同时减少加载 checkpoint 过程引入的延迟，特别是阻塞训练进度的关键路径上的时间
                        2. 为了实现快速的检查点操作，引入了一个优化的两阶段方法
                            1. 在第一阶段，每个 GPU 工作进程将其片上状态写入主机内存，然后继续训练过程
                            2. 在第二阶段，一个后台进程接管，异步地将状态从主机内存传输到分布式文件系统（部署中为HDFS）
                        3. recovery from a checkpoint
                            1. Multiple GPU workers often share the same state partition
                            2. As optimization, a single worker read the shared state partition from HDFS, and then broadcasts to all GPUs in group

                5. Training Troubleshooting
                    1. 字节实现了以下异常检测的监控和分析工具
                        1. Performance Diagnosis with CUDA Event Monitor
                            0. This is an interesting tool, which has potential to be widely adopted
                            1. We observed 各种训练任务的 MFU 随时间逐渐下降，但在单个 GPU 的 GEMM 微基准测试中没有发现明显的差异
                            2. 为了诊断这些性能问题，我们开发了一个性能分析工具，记录每个机器排名在运行过程中关键代码段的执行时间。与之前的工具（如 torch 分析器或 MegatronLM 计时器）不同，我们的工具基于 CUDA events 方法计时。这种方法最大程度地减少了对 CUDA 同步的需求，从而防止性能下降，并使我们能够在生产训练作业中始终稳定地运行它。
                            3. 这个工具提供了两种可视化模式
                                1. 第一种模式使用热图来显示不同维度上机器之间的时间消耗差异。热图显示，在训练过程中，大约有 0.5% 的机器表现出明显较慢的性能
                                    1. 在排除这些异常机器之后，各次运行的 MFU 变得一致
                                2. 另一种模式以跟踪格式显示不同分布式视图（数据并行、流水线并行、张量并行）上的机器事件时间线
                                    1. 传统的分析器（如PyTorch Profiler）主要设计用于单节点的活动分析。这种方法在执行依赖关系经常跨越多个节点的分布式训练场景中提供的信息有限。
                                    2. 通过将各个 rank 的跟踪跨度聚合到一个时间线上，我们获得了全面的视角，揭示了整体的执行顺序、流水线 bubble 和数据并行排名之间的同步特性。
                                3. 每个 CUDA events 计时器的数据都存储在远程分析数据库中，
                                    1. 虽然计时器数据以逐行格式写入本地文件，但一个独立的流处理进程会实时将此日志文件与 Kafka 队列同步。分析数据库通过消费来自 Kafka 队列的数据保持更新，实现了即时分析而不中断训练作业。
                                    2. 在真实的生产训练中，所有的监控功能都被打开，与训练时间相比，额外开销可以忽略不计。

                        2. 3D Parallel Training Visualization
                            1. 通过 3D 并行和字节的优化技术，数据流和任务序列的情况变得非常复杂。
                                1. 每个 GPU 工作节点在给定时刻可能同时进行多个同步或异步操作，导致它们之间存在复杂的依赖关系。
                                2. 这种复杂性增加了故障诊断的挑战：当单个GPU工作节点发生故障时，整个节点集群可能在 NCCL 通信操作中停滞，最终导致系统范围的超时。
                                3. 在外部，这种情况表现为通用的阻塞，但其根本原因往往被大量的超时消息所掩盖。
                            2. 字节让每个 GPU 工作节点在通信超时时记录其正在进行的事件。然后，利用这些日志根据 3D 并行设置中的逻辑拓扑构建数据依赖的可视化表示。

                6. 大模型训练经验
                    1. 在使用 3072 到 12288 个GPU进行训练时，将 batch size 设置为 6144
                    2. 消融研究
                        1. baseline 47.7%
                        2. with PTB 52.3% (4.6%)
                        3. with SWA 53.3% (5.6%)
                        4. with TP overlap 55.5% (7.8%)
                        5. with PP overlap 58.0% (10.3%)
                        6. with DP overlap 59.5% (11.8%)
                        7. with efficient operators 61.2% (13.5%)
                        8. with misc optimizations 62.3% (14.6%)
                        9. with LAMB (BS×3) 65.3% (17.6%)
                    3. 检测故障并执行诊断测试所需的平均时间不到10分钟。
                        1. 此外，系统可以在 latest checkpoints 后的 15 分钟内赶上训练进度，保持超过90%的有效训练时间比例。
                    4. MFU decreasing
                        1. 在这样的大规模训练实验中，字节观察到训练效率并不是始终保持一致的。相反，随着训练的进行，训练作业的 MFU 逐渐下降。通过基于CUDA events 计时器指标的逐步分析，我们注意到了几个关键发现。
                            1. 不规则的垃圾回收可能会给训练过程引入干扰
                            2. PyTorch 操作可能会导致性能波动。
                           在修改或删除这些有问题的代码段之后，不再观察到 MFU 的显著下降，如图16所示。
                    5. Frequent network interface flapping problem
                        1. 从中学到的第一个教训是应该将超时阈值明确地设置为较大的值（猜测是NCCL_IB_TIMEOUT），否则默认值会使 NCCL 的超时时间非常短，在网络卡重新连接之前就会返回完成错误。
                        2. 学到的第二个教训是，这个问题的根本原因是网卡、AOC电缆和交换机之间的链路质量不好。通过对网络卡信号强度、AOC 电缆质量和交换机侧信号强度进行较低级别的质量控制，可以将抖动频率降低到令人满意的水平。
                            1. Interesting topic here. How to do hardware level fault tolerance on NIC level. In compare, memory has ECC.

        2. 拆解一下字节的烧钱工作，MegaScale！ - 蛋糕店的蜡烛
           https://zhuanlan.zhihu.com/p/684712727

        3. NSDI 24 MegaScale：字节大模型在跳舞，万卡集群，全栈优化，MFU高达55.2% - MLSys2024
           https://mp.weixin.qq.com/s/rbTbzLPh5uFtpOxf4TThaA

        4. Building Meta's GenAI Infrastructure - Kevin Lee, Adi Gangidi, Mathew Oldham    [2024, Facebook]
            https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/
            1. Two 24k GPU clusters, built atop opensource Grand Teton, OpenRack, and PyTorch, will include 350,000 NVIDIA H100 GPUs. Llama 3. 
            2. Highlights
                1. Networking
                    1. RDMA on RoCE based on the Arista 7800 with Wedge400 and Minipack2 OCP rack switches,  NVIDIA Quantum2 InfiniBand fabric.
                2. Compute
                    1. Grand Teton, our in-house-designed, Open GPU contributed to Open Compute Project (OCP). 
                3. Storage
                    1. Our storage deployment addresses the data and checkpointing needs of the AI clusters via a home-grown Linux Filesystem in Userspace (FUSE) API backed by a version of Meta's 'Tectonic' distributed storage solution optimized for Flash media
                        1. Challenge of Thundering herd problem - thousands of GPUs to save and load checkpoints in a synchronized fashion
                    2. We have also partnered with Hammerspace to co-develop and land a parallel network file system (NFS) deployment to meet the developer experience requirements for this AI cluster.
                        1. Hammerspace enables engineers to perform interactive debugging for jobs using thousands of GPUs as code changes are immediately accessible to all nodes within the environment
                    3. Both Tectonic- and Hammerspace-backed, are based on the YV3 Sierra Point server platform, upgraded with the latest high capacity E1.S SSD
                        1. The servers per rack was customized to achieve the right balance of throughput capacity per server, rack count reduction, and associated power efficiency
            
            n. Related materials
                1. Meta大规模AI集群内部揭秘：构建60万个H100的强大算力 - Andy730
                   https://mp.weixin.qq.com/s/NBMshmGJvgcTYe6PrW_l-Q
                    1. 网络配置：
                        1. Arista 7800的RoCE网络解决方案，Wedge400和Minipack2 OCP机架交换机。
                        2. 另一集群采用NVIDIA Quantum2 InfiniBand架构。
                        3. 支持400Gbps端点连接，评估不同网络在大规模训练中的适用性和可扩展性。

                    2. 计算配置：
                        1. 自主设计的Grand Teton，为OCP贡献的开放GPU硬件平台。
                        2. Grand Teton集成了功率、控制、计算和网络接口于单个机箱，提升整体性能和热性能。
                        3. 设计简洁，使得数据中心能够快速部署，易于维护和扩展，如Open Rack电源和机架架构。

                    3. 存储配置：
                        1. 采用自主开发的FUSE文件系统API，结合闪存介质优化的Tectonic分布式存储解决方案。
                        2. Tectonic分布式存储支持数千个GPU的同步保存和加载检查点，提供灵活、高吞吐量的EB级存储。
                        3. 与Hammerspace合作开发并部署了并行NFS，提供交互式调试和快速迭代速度。
                        4. 基于YV3 Sierra Point服务器平台，配备最新高容量E1.S SSD，实现吞吐能力、机架数量减少以及功率效率之间的平衡。
                        5. 利用OCP服务器的模块化设计，实现存储层的灵活扩展和出色的容错能力。

                    4. 性能总结：
                        1. 总体目标：在不牺牲任何方面的前提下，最大化性能和易用性。
                        2. 测试方法：通过构建和优化系统，并实际运行测试，对比小规模集群与大规模集群的性能表现，以精准定位瓶颈所在。
                        3. 网络性能优化：优化内部作业调度器的网络拓扑感知功能，改进NCCL网络路由策略，实现网络资源的最佳利用。
                        4. 与训练框架团队合作：与编写训练框架和模型的团队紧密合作，确保其与基础设施相契合。
                        5. 调试工具开发：开发解同步调试或分布式集体飞行记录器等工具，帮助快速、便捷地定位问题。
                        6. PyTorch框架升级：持续对PyTorch框架进行迭代升级，以支持数十万甚至数百万GPU的训练需求。

                2. 构建 10 万卡 GPU 集群的技术挑战 - 慢慢学AIGC
                   https://mp.weixin.qq.com/s/yauPCUsXoILEDqkUWcn36A
                   100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing - SemiAnalysis
                   https://www.semianalysis.com/p/100000-h100-clusters-power-network
                    1. 一个 10 万 GPU 的集群需要超过 150MW 的数据中心容量，并在一年内消耗 1.59 太瓦时的电力，按照标准费率 $0.078/kWh 计算，成本为 1.239 亿美元。
                    2. 在 H100 上，AI 实验室在万亿参数训练运行中达到了高达 35% 的 FP8 模型 FLOPs 利用率（MFU）和 40% 的 FP16 MFU
                    3. 但我们正在追踪超过 15 个数据中心的建设，包括 Microsoft、Meta、Google、Amazon、Bytedance、X.AI、Oracle 等，它们将有足够的空间容纳 AI 服务器和网络设备。
                    
                    4. 为了最大化模型 FLOP 利用率（MFU），公司通常将三种并行性结合起来形成 3D 并行性。然后在 H100 服务器内应用张量并行性，在同一个岛内的节点之间使用流水线并行性。由于数据并行性通信量最小，岛之间的网络较慢，因此在岛之间使用数据并行性。
                    
                    5. NVIDIA 轨道优化是一种技术，每个 H100 服务器连接到 8 个不同的叶交换机（而不是全部连接到同一个机架中部交换机），使每个 GPU 只需一次交换机跳跃即可与更远的 GPU 通信。这提高了现实世界 all2all 集体通信性能。all2all 集合通信在混合专家模型（MoE）专家并行性中被广泛使用。
                        1. 为了提高维护性并增加铜线网络（< 3 米）和多模网络（< 50 米）的使用，一些客户选择放弃 NVIDIA 推荐的轨道优化设计，转而采用机架中部设计。
                    
                    6. 最常见的可靠性问题是 GPU HBM ECC 错误、GPU 驱动卡住、光学收发器故障、NIC 过热等
                        1. 频繁的检查点和故障容错训练技术会影响系统的整体 MFU
                            1. 另一种故障恢复方法是让备用节点通过后端结构从其他 GPU 上 RDMA 复制 ... 所以这只会丢失 2.3 GPU 天的计算+另一个 1.85 GPU 天从其他 GPU HBM 内存复制权重
                                1. This is an very interesting point, worth investing.
                                    1. Related to: MegaScale paper 2024
                        
                        2. 最常见的问题之一是 InfiniBand/RoCE 链路故障。即使每个 NIC 到叶交换机链路的故障平均时间（MTTF）为 5 年，由于收发器数量众多，新的工作集群在 26.28 分钟内就会发生第一次作业故障。
                            1. 由于每个 GPU 通过 PCIe 交换机直接连接到 ConnectX-7 NIC，因此网络架构级别没有故障容错，因此故障必须在用户训练代码中处理
                                1. This is an interesting topic. NIC level doesn't have fault tolerance like memory ECC.
                                    1. Related to: MegaScale paper 2024

                3. Meta：大规模AI基础设施 - Andy730
                   https://mp.weixin.qq.com/s/4GlCllUgMyqhz_SdxhPm2g
                    1. Source
                        1. Infrastructure for Large-Scale AI
                           会议：2022 OCP Global Summit
                    2. 仅在第二季度，我们的AI系统就删除了近2.5亿条违反平台安全性的内容，这一数字仅涵盖Facebook和Instagram平台
                    3. Grand Teton是Meta的下一代AI平台，相比Zion EX，它得到了全面的升级和优化，以支持更加多样化的工作负载
                    4. 目前，我们面临着对极高注入（injection）带宽和极高双向（bisectional）带宽的双重需求。

        5. Resiliency at Scale: Managing Google's TPUv4 Machine Learning Supercomputer    [2024, 3 refs, NSDI24, Google]
           https://www.usenix.org/conference/nsdi24/presentation/zu
           https://www.youtube.com/watch?v=9VpZ_E1NPbQ
            1. TPUv4 - 4096-node supercomputer with a custom 3D torus interconnect. Auto hardware recovery with reconfiguration in ICI fabric, enabled by OCS (optical circuit switching) and SDN.
               OCS is the key technology here. Then it comes to the reconfigurable ICI.
            2. Highlights
                1. TPUv4 supercomputer
                    1. A cube is a hardware unit with 64 TPU chips. Cube arranges in 4*4*4 3D mesh. A supercomputer has 64 cubes.
                    2. Proprietary ICI (inter-chip interconnect) fabric allows direct TPU to TPU communication (RDMA) bypassing CPU
                        1. Google版本的NVLink
                    3. Borg for cluster management. Manages job scheduler, cloud user to TPU assignment.
                    4. Pod Manager for mananging multi-cube connectivity by actuating OCS xconnect in response to Borg.
            3. My questions
                1. From Figure 5, it seems cube is the minimal scheduling unit in fault tolerance and job assignment. But a cube has 64 TPUs. Isn't the unit size too large? How to scheduler per single TPU?

            n. Related materials
                1. 大规模弹性部署：Google如何管理TPUv4集群  - zartbot
                   https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247489642&idx=1&sn=db30c4606db2f181f8f602c8e71abf91
                    1. Google TPU v4包含了如下一系列软硬件：
                        1. cubes: 通常以4x4x4的64个TPU芯片构成的立方体作为一个单元进行交付，每个Pod有4096块TPUv4
                            1. 每个3D立方体在X/Y/Z维度的每个面上暴露16个ICIs给光学交换机，每个立方体总共96个ICIs
                        2. ICI: 通俗地说Google版本的NVLink，全称Inter-Chip-Interconnect，它允许TPU之间不经过CPU直接通信
                        3. OCS: Optical Circuit Switch光交换机动态改变拓扑用于满足用户对不同Size Cube的需求以及失效路由等需求
                        4. Borg 集群管理和调度，也就是K8S的前身
                        5. Pod Manager 集群管理软件，类似于SDN的控制器，受Borg调度并修改OCS交换机管理多个cube的连接。
                        6. libtpunet TPU的网络库，用于请求ICI网络拓扑
                        7. healthd运行在集群内每个主机上用于监控硬件健康状态
                    
                    2. 如果没有TPUv4基于OCS的可重构性 ... 当所需的计算资源增加到1024个芯片时，作业的整体可用性急剧下降
                        1. 有了TPUv4的立方体级别可配置性，可用性保持在大约94%，对应于约50个立方体或3200个TPUv4芯片
                        2. 在TPUv4之前，TPUv3和TPUv2都是静态Pod架构，ICI互联网络是不可重构的
                    
                    3. 云上部署需要考虑的弹性能力
                        1. 网络可自动重新配置以屏蔽故障
                        2. 使用光交换价容易地重新编程，毫秒内切换
                            1. TPUv4的OCS可配置性极大地提高了可用性。即使训练作业使用的立方体在物理上不连续，也可以使用任何立方体
                            2. OCS和光纤的成本不到TPUv4 pod总资本成本的5%，其运行功率不到pod总功率的3%
                                1. Interesting point. But from Zartbot "但实际上，例如Tomhawk5这些白盒交换机的成本是非常低的，如果在以太网上实现ScaleUP和Scale-Out网络和OCS的成本差距并没有Google说的那么大".
                            3. 另外针对AlltoAll算子，也可以通过ICI重配置路由表构建Twisted Tori拓扑
                        3. Zartbot: NVIDIA产品尚缺乏对"弹性"的解决方案
                            1. 当一个Rail Interconnect交换机出现故障后，影响的规模会多达千卡，同时针对某个GPU硬件故障或者链路故障，在同一个Rail下没有备用机将会导致调度困难。
                    
                    4. 可编程的ICI协议
                        1. 一个TPUv4 pod（i.e., supercomputer）是一个ICI域，在其中任何一对TPU都可以彼此进行RDMA。
                        2. 每个ICI链路可以承载50GBps的单向带宽
                        3. TPUv4采用3D ICI网络拓扑结构
                        4. Figure 4: TPU chip layout and ICI switch component
                        5. ICI路由机制
                            1. ICI转发表在作业启动时由libtpunet编程一次，并在作业的整个生命周期中保持固定。每对源-目的对通过ICI拓扑沿着一条预定路径发送数据包。
                                1. 虽然这种方法很简单，但对于在ML模型并行过程中出现的典型集合通信模式（如all-gather、reduce-scatter、all-reduce、all-to-all）来说，已经足够实现高性能。
                            2. 当为常规环形拓扑配置时，ICI使用Torus中常用的Dimension-Order-Routing(DOR)
                                1. 所有数据包按照固定顺序（例如X然后Y然后Z）一次路由一个维度，沿着环形中源到目的的最短路径。维度顺序的选择方式是先路由环形较长的维度
                            3. 容错路由 - 当一个OCS不可用
                                1. 使用Wild-First Routing（WFR）创建替代路径。
                            4. 离线路由优化
                                1. 由于Torus有多个路径可以转发，因此需要对ICI交换机的静态转发表作出选择构建单一路径，
                                2. Google将路径选择问题形式化为整数线性规划（ILP），离线计算解决方案并缓存以供运行时使用
                                3. ILP的目标是通过解决最大并发流问题来最大化预定义流量模式的吞吐量。
                                4. 通常选择all-to-all作为流量模式，并附加约束确保其他集合通信（如allreduce）性能良好

                    5. 超级计算机的自动化管理
                        1. Section 3.1 "Overview" has the step by step workflow of job serving
                        2. 调度
                            1. 谷歌全球数据中心中有许多BorgCell，每个Cell可能包含几个TPUv4超级计算机。每个Cell由N个复制的Borg服务实例管理，这些实例共同提供一个逻辑Borg实例，称之为Borg Prime，其中包括一个集群调度器。
                            2. 每台TPU机器运行一个borglet守护程序，与Borg Prime合作处理作业生命周期管理。在Pod Manager批准后，Borg Prime指示分配立方体中的每个borglet创建一个任务容器，将机器的TPUv4设备暴露在任务的容器中。
                        3. Pod Manager - Similar with K8S's
                            1. Pod Manager完全依赖于模型数据来配置其服务。它定期轮询网络模型服务
                            2. Pod Manager通过复制实现高可用性
                            3. OCS支持两种拓扑，普通为Reduce优化的Torus拓扑， 以及针对AlltoAll算子，通过ICI重配置路由表构建Twisted Tori拓扑
                                1. Torus xconnect
                                2. Twisted-Torus xconnect
                        4. Libtpunet - ICI路由编程
                            1. libtpunet根据在拓扑发现过程中整理的信息计算并编程每个TPU的转发表
                            2. libtpunet还根据链路往返时间（RTT）的比例设置链路级流控缓冲区大小
                        5. healthd - 实时监控
                            1. 实时监控包括24个单向ICI链路、TPU与CPU之间的PCIe通道以及4个TPU ASIC自身在内的硬件部件
                        6. Preflight Check - 预检机制
                            1. 在每个用户作业开始之前运行一次预检检查，以确保硬件处于健康状态
                            2. 目前包括两种不同的检查器：
                                1. 端到端检查通过运行一个小型工作负载来验证TPU硬件，
                                2. 而意图驱动的检查器则将物理级别硬件指标与一组"在规格内"的阈值进行比较
                    
                    6. Evaluation & statistics
                        1. 平均每天有0.08%的TPU机器、0.005%的ICI电缆和0.04%的OCS发生故障

                    7. Related works
                        1. Nvidia使用基于NVswitch的两层胖树网络通过NVlink实现GPU间的集合通信。这些方案代表了一个与Google不同的设计点
                        2. Efficient Training of Large Language Models on Distributed Infrastructures: A Survey    [2024]
                           https://arxiv.org/abs/2407.20018
                            1. Figure 5 shows useful networking topologies compare. Google's Torus Topology, NVIDIA's Cube-Mesh Topology.

                    8. Future works
                        1. 短期主要优先事项是改进TPU Pod的性能和恢复开销：ML超级计算硬件需求旺盛，每一处改进都很重要
                        2. 未来，除了支持增加ICI链路的线路速率外，我们还计划向ICI交换机引入随机路由能力
                        3. 在发生中断事件时提供热备立方体，并直接将加速器状态迁移到新的TPU，而无需写入持久检查点
                        4. Zartbot: 宕机热迁移
                            1. Google在其论文结尾未来的工作中提到，针对大规模模型训练的宕机热迁移能力也是很重要的，这一点几乎所有的厂家都没拿出很好的方案来，以太网宕机热迁移要求保证通信的IP地址都不能修改，因此又要引入Overlay，针对Overlay RDMA能够做到at Scale的全球也就只有三家，能够成熟做好热迁移的大概只有两家。而针对RDMA能够实现热迁移的，至少Mellanox现在是完全不行的。

                    9. 如何在以太网上构建弹性的AI集群
                        1. Torus拓扑在allreduce集合通信加速上有天然的优势，但是对于All-to-all通信带宽上还是有一定的缺陷，这也是工业界准备转向Dragonfly拓扑的原因
                        2. 微软的Maia 100拓扑可能是一个好选择，在Torus的小cube外构建包交换机，然后获得大尺度下的bisection bw增强。

12. MAST: Global Scheduling of ML Training across Geo-Distributed Datacenters at Hyperscale    [2024, 0 refs, OSDI24, Facebook]
    https://www.usenix.org/conference/osdi24/presentation/choudhury
    1. ML scheduler for Facebook data warehouse, running on Twine. Features in temporal decoupling, scope decoupling, exhaustive search.
       Placement algorithm strives for data locality, balance regional usage, GPU demand-to-supply ratio. 
    2. Highlights
        1. Key challenges
            1. Need to allocate GPUs for ML workloads, but unaligned regional locality causes unnecessary GPU demand and unnecessary data movement
            2. Optimal placement of computation jobs and data sources to balance load across regions, and to reduce cross regional traffic.
            3. "Global Scheduling" concept. User simply submit their ML training workloads to global entry, no need to care about region.
            4. MAST also allocates CPU machines for data preprocessing.
            5. The scale of global. MAST needs to find from millions of machines across tens of regions.
            6. Datacenter hardware was procured incrementally at different times. Generation imbalance. E.g., Region6 is short of GPUs.
            7. ML training workloads often takes 10 times longer to finish than Spark analytics jobs.
                1. Therefore, a suboptimal placement decision has a bigger negative impact on ML training. This motivates the exhaustive search principle
                2. Moreover, when workloads run longer on a larger number of machines, the workload scheduling throughput decreases. Therefore, it is feasible to manage the job queue and resource allocation at the global and regional scope, respectively, rather than at the smaller cluster scope that leads to more fragmentation.
                3. This is an interesting analysis
            8. Separate application-level schedulers for ML and non-ML workloads
                1. Twine [44] allows all workloads to share a common cluster manager for machine and container management, while employing different application-level schedulers
                    1. For instance, MAST is used for ML training workloads
                    2. Shard Manager [29] for stateful databases, 
                    3. Turbine [32] for stream processing
                    4. and Chronos for analytics jobs
            9. Facebook chooses to separate ML and non-ML workloads into different clusters
                1. See Section 4.4 Cluster Management
        2. Key techniques
            1. Handling the scale of global
                1. A fast-path for realtime job scheduling, and a slow-path for continually optimization at background
                2. Dynamic cluster, generated by RAS, allows RMS to only search through machines within it
                3. Decouple responsibility and global scope
                    1. GMS - Global ML Scheduler - job queue and priority, at global scale
                    2. RMS - Regional ML Scheduler - resource allocation like bin-packing, at regional scale
                    3. CM - Cluster Manager - Container orchestration, at dynamic cluster scope
                        1. CM is Twine [44]. See Section 4.4 
                4. Scalability of RMS
                    1. RMS computation complexity is quadratic to h ML hardware per region. Current RMS can handle 12x increase in h.
                    2. Currently, the largest RMS manages around 20 dynamic clusters, comprising a total of 64,000 CPU machines and 20,000 GPUs
                5. Scalability of GMS
                    1. GMS periodically computes the <priority, credit> tuples for all workloads (a GMS-scan pass).
                    2. The code is Python. ~34 seconds to scan 6,000-10,000 workloads. Run one pass every 5 min.
            2. Scheduling and placement algorithms
                1. Model data placement as a mixed integer programming (MIP) problem. Allow GPU oversubscription and preempts low priority jobs.
                    1. Figure 4: Minimize: weight1 * table size * not locality + weight2 * imbalance of GPU demand-to-supply * regional overload + weight3 * imbalance of storage demand-to-supply
                2. Exhaustive search
                    1. Search all regions, multiple RMS concurrently computes allocation plans.
                        1. This is unlike traditional Federation Manager approach, where the global scheduler pushes down job to the least loaded cluster
                3. Placement locality
                    1. For tasks that belong to an ML training workload, we prefer to place them in the same rack, cluster, datacenter, and region, in that order
                    2. An ML job takes a table as input, then at least of of the table's regions should have required GPU types. - data-GPU collocation property
                    3. A table's replicas in other regions are more stale compared to those in the home region. Therefore, high priority jobs requiring fresh data must run in the home regions of their input table. - training-at-home-region property
                4. Tetris - MAST's slow path component - data placement/migration in Facebook data warehouse
                    1. MAST optimizes cross-region data placement on a daily basis using a slow-path component called Tetris. 
                       Optimizes data placement across regions, taking into account the data access patterns of Spark, Presto, and ML training jobs.
                       Spark and Presto and ML training can concurrently access the same data, Tetris jointly optimizes data placement for them
                    2. Data warehouse has hundreds of namespaces -> millions of tables -> billions of data partitions
                        1. Table must be in one region (home). Partitions can be placed at different clusters.
                    3. Tetris for data placement
                        1. RAS generates dynamic cluster
                        2. Tetris, slow-path, takes job history records, and calculates data placement
                        3. MAST fast-path scheduler manages first-time jobs upon submission
                            1. If no region satisfies necessary data and hardware, MAST will initiate data movement
                    4. Create additional table copy for DR, ML job running, or hot tables
                5. Sharing data partitions by ML workload jobs
                    1. This naturally happen, see Figure 3 hotness, and Section 3.1.
                    2. Furthermore, replicate hottest partitions across multiple regions to distribute load
                7. Lower priority jobs get preempted by higher priority ones, or if the team exceeded quota
                    1. Job <priority, credit> is calculated by GMS. And quota.
                        1. Higher credit is a job is waiting longer or belongs to a tenant that used fewer resources
                8. Negative cache
                    1. the most effective one to optimize RMS performance
                    2. If RMS cannot allocate resources for a job, it saves and reuses the decision in cache
            3. Fault tolerance
                1. Run multiple instances of GMS across region. GMS is stateless. States are persisted in replicated database.

        3. Related works
            1. MAST vs Google Borg [48]
                1. Table 1 has an interesting categorization. The key advantage of MAST over Borg is MAST can admit global jobs and schedule at regional level, while Borg is cluster level.
            2. Federated systems
                1. No global level job admissions, no regional level scheduling
                2. Section 5.6, Federated approach results in high SLO violation, because not able to dispatch a high-priority workload to the right region where it can preempt others
            3. The closest work to Tetris is Alibaba's Yugong [20], which uses MIP to place data for analytics jobs based on CPU (but not GPU)
                1. [20] Yugong: Geo-Distributed Data and Job Placement at Scale

        4. Limitations / Future works
            1. Inability to distribute a job's tasks across different clusters - virtual job
            2. Scheduling multiple workloads simultaneously in parallel
            3. Placement of recurring jobs, connect slow path to fast path.

    n. Related materials
        1. Rebalancer: Optimizing Resource Allocation in Hyperscale Datacenters: Scalability, Usability, and Experiences    [2024, 0 refs, OSDI24, Facebook]
           https://www.usenix.org/conference/osdi24/presentation/kumar
            1. Very interesting research direction. Use new domain language to solve the cloud / datacenter resource allocation problem which traditionally solves by MIP.
               Applied to dozens of large-scale use cases over the past seven years.
               Referenced in Shard Manager as "a popular constraint solver"

            2. Highlights
                1. Key challenges
                    1. Mixed Integer Programming (MIP) is widely used in resource allocation, but it has limitations
                        1. Usability - MIP has too many math formulas
                        2. Scalability - too large input size
                2. Key techniques
                    1. Rebalancer is organized as model specification, model representation, model solving
                    2. Model specification
                        1. Figure 1, dimensions and scopes, APIs to add constrains and objectives
                        2. Case Studies of Model Specification
                            1. Hardware placement [30]
                            2. Service Placement [32]
                            3. Service sharding [25]
                            4. Message Queue Placement
                            5. Kubernetes Scheduler
                        3. Table 1: List of 21 most frequently used specs
                    3. Model representation
                        1. The "Expression Graph", which is the core of Rebalancer. See Figure 2.
                    4. Model solving
                        1. For small problems, Rebalancer translates Expression Graph into a MIP problem and solves it with a MIP solver
                        2. For large problems, Rebalancer implements its own "Graph-Assisted Local Search"
                            1. See Algorithm 1. It's an interesting alternative to MIP on large problems

            3. Related works
                1. [38] DCM: Building scalable and flexible cluster managers using declarative programming    [2020]
                    1. Section 6.1 Comparison with DCM.
                    2. DCM [38] uses SQL to express policies for placing pods on nodes. It translates these SQL statements into a constraint satisfaction problem, which is then solved using the Google OR-tools CP-SAT solver.
                2. [31] POP: Solving large-scale granular resource allocation problems efficiently with pop    [2021]
                    1. Section 6.2 Comparison with Partitioned MIP
                    2. To scale MIP, we implemented a POP-like [31] partitioned MIP solver
                3. Systems utilizing MIP, such as Flux [10]
                    1. formal problem specification solved by a formal solver
                    2. [10] Global Capacity Management with Flux

        2. RAS: Continuously Optimized Region-Wide Datacenter Resource Allocation    [2021, 27 refs, SOSP21, Facebook]
           https://research.facebook.com/publications/ras-continuously-optimized-region-wide-datacenter-resource-allocation/
           https://www.youtube.com/watch?v=4wKKE9PIFA4
            0. In parent papers
                1. Referenced in the MAST paper
                    1. [36] RAS: allocate machines to dynamic clusters. RAS ensures
                        1. Machine capacity allocated to a dynamic cluster meets the requirements
                        2. Include sufficient buffers to handle both random and correlated machine failures
                        3. Distribute machines across fault domains
                        4. Reduce cross-datacenter communication by ensuring proper ratio of compute machines to storage machines
                        5. RAS reruns optimization every 30 minutes to adapt to changes
                2. Referenced in the Rebalancer paper
                    2. [32] RAS: Service-placement. Decide on the allocation of servers to services.
                        1. we model servers as objects and reservations as bins
                        2. we group servers by MSB, rack, and hardware type, which become object partitions
                        3. objectives and constraints
                            1. Capacity sufficiency
                            2. Spread, across MSB and rack partitions
                            3. Stability, avoid churn, As new reservation requests emerge or existing ones are updated
                            4. Fault tolerance, allocate additional buffer capacity

            1. Introduced dynamic clusters (reservation), introduced slow-path to offload optimize server-to-reservation assignments.
               The two are good designs as built atop Twine which treats the entire region as one single cluster.
            2. Highlights
                1. Key challenges
                    1. Problems of static cluster membership
                        1. Some clusters may run out of capacity and cannot sustain higher loads, while others are underutilized.
                        2. Server allocation may be suboptimal due to variation in power and network consumption of workloads and their different hardware requirements such as certain CPUs, flash storage, and memory capacity
                        3. Service owners have to individually prepare for datacenter scale failures by themselves
                    2. The problem from Twine [39]
                        1. See section 1.1, it's an interesting analysis. Logged in Twine's paper.
                            1. This well explains why Dynamic Cluster needs to be introduced
                2. Key techniques
                    1. RAS is a component of Facebook Twine.
                    2. Capacity abstraction - "Reservation", later called "Dynamic Cluster" in other papers
                    3. Two level approach
                        1. Fast-path for realtime placement of container to server
                            1. Immediately allocate a server from the "reservation", i.e. dynamical cluster. It's equivalent to allocating ahead of time
                        2. Slow-path for background continuous optimization of placement of server to dynamic cluster
                            1. MIP solver, runs every tens of minutes
                            2. Factors considered in placement
                                1. Capacity requirements, server availability, network, datacenter topology, as well as random and correlated failure buffer constraints
                                2. Stability and optimality objectives that minimize movement of servers and optimize server spread across fault domains of various scopes
                            3. The Online Mover is responsible for changing the ownership of a server following updates from RAS solve outputs
                    4. MIP Model
                        1. Stability objective - minimize machines moved out of a reservation
                        2. Spread-wide objective
                    5. RRU - Relative Resource Unit
                        1. abstracts the amount of heterogeneous hardware, so that RAS can treat them uniformly in the MIP model.

                3. Others
                    1. Prioritize buffer capacity - "RAS treats buffers just like a large, important service that cannot be downsized"

        3. Fault tolerance through optimal workload placement    [2020, Facebook]
           https://engineering.fb.com/2020/09/08/data-center-engineering/fault-tolerance-through-optimal-workload-placement/
            0. In parent papers
                1. Referenced in the Rebalancer paper
                    1. [30] Hardware placement: Decide when and where to add or remove server racks in a datacenter while balancing competing goals such as
                        1. Staff work schedule
                        2. Power budget
                        3. Spread across fault domains
                        4. Colocation for proximity, e.g., ML training servers requiring high-bandwidth network.

            1. Placing a hardware server also needs placement algorithm such as MIP. Buffer capacity and fault domain spread are top factors.
            2. Highlights
                1. Introducing "buffer capacity", given the fault domain
                    1. Case study: A snake in datacenter causes a loss of only 3% capacity, however it resulted in an outage
                2. Optimal workload placement
                    1. Hardware should be balancedly placed and in fault domains.
                        1. "Spread" concept
                    2. Facebook's hardware capacity planning runs on a quarterly cycle. Every three months, we determine how many racks and which rack types we need to purchase for each data center
                    3. Data center space, power, network, thermal effects, and, of course, spread across fault domains are all factored in when deciding on this physical placement
                        1. there are dozens of constraints that must be satisfied for each rack as we determine its placement. We use integer linear programming systems to compute the best plan
                            1. My questions
                                1. It looks like the placement / resource allocation at Facebook at different layers are all using Mixed Integer Programming.
                        2. Row/RPP power domain, Air shaft cooling domain, Pod network domain
                    4. Challenges
                        1. Changing demand for capacity
                        2. Evolving data center designs
                        3. Constraints
                            1. Specific hardware requirements
                            2. Service affinities
                    5. What about old or existing capacity? 
                        1. we perform physical rack moves
                    6. Continuous rebalancing to maintain optimal workload placement
                        1. This rebalancing is not a one-time event
                    7. we can simply treat maintenance as another form of sub-data center failure
                        1. We can then cycle through each fault domain in a data center and batch process maintenance for all capacity under each fault domain

        5. [44] Twine: A Unified Cluster Management System for Shared Infrastructure    [2020, 71 refs, OSDI20, Facebook]
           https://www.usenix.org/conference/osdi20/presentation/tang
           https://www.youtube.com/watch?v=_-K-DeA7n5s
            0. In parent papers
                1. From the RAS paper
                    1. Twine [39] is to forego the boundary of physical clusters and datacenters, and use a shared mega server pool that comprises all servers from datacenters in a geographical region connected by a low-latency network.
                        1. Conceptually, Twine organizes servers into logical clusters called entitlements. When a new container needs to be started but cannot fit on any existing server in an entitlement, a free server is greedily acquired from a shared region-level free-server pool and added to the entitlement to host the new container. When the last container running on a server is decommissioned, the server is returned to the shared free-server pool.
                        2. On one hand, this approach has the benefit that a single server pool eliminates server capacity stranded in many smaller physical clusters.
                        3. On the other hand, it puts a whole region's server-to-entitlement assignment on the critical path of container placement. As a result, previously we had to adopt simple heuristics to make quick server-assignment decisions, which led to sub-optimal server assignment and could not provide guaranteed capacity in the event of correlated failures.

            1. 18% power saving fleet-wide, 17% savings in total cost of ownership. Facebook's cluster management system evolving Twine over the past 10 years.
            2. Highlights
                1. Key challenges
                    1. Avoid stranded capacity in isolated clusters and enable fleet-wide optimizations
                    2. Support customization in a ubiquitous shared infrastructure
                    3. Achieve higher power efficiency with small machines (single 18-core CPU and 64GB of RAM)
                2. Key techniques
                    1. A single control plane to manage all machines in teh entire region
                    2. TaskControl API allows an application to collaborate with Twine to handle container lifecycle events, 
                        1. e.g., restarting a ZooKeeper deployment's followers first and its leader last during a rolling upgrade. 
                        2. Host profiles capture hardware and OS settings that workloads can tune to improve performance and reliability
                    3. Entitlements - for quota to team
                        1. A machine is either free or assigned to an entitlement
                        2. An entitlement can consist of machines from different
                        3. My questions
                            1. Why given Twine has Entitlement, RAS still introduces Dynamic Cluster?
                                1. Probably to make Entitlement dynamic
                                2. On the other hand, it puts a whole region's server-to-entitlement assignment on the critical path of container placement
                    4. Small machines - power saving
                        1. We have worked with Intel to define low power processors optimized for our environment, e.g., removing unneeded NUMA components.
                        2. Four small machines are tightly packed into one sled, sharing one multi-host NIC
                        3. They are replacing our big machines, each with dual CPUs, 256GB RAM, and a dedicated NIC
                        4. A small-machine rack delivers 57% higher total compute capacity measured in RRU. Averaged across all our services, using small machines led to 18% savings in power and 17% savings in total cost of ownership
                            1. Very interesting .. how it works our in the recent years?
                    5. Scaling Twine to 1M machines
                        1. Sharding rather than federation
                            1. We shard Twine schedulers by entitlements. Twine can transparently move an entitlement in the shard to another shard.
                            2. Twine can also migrate an individual job from one entitlement to another, via rolling upgrade
                            3. Currently, the largest scheduler shard manages ≈170K machines; the largest entitlement uses ≈60K machines; and the largest job has ≈15K tasks.
                        2. Separation of concerns
                            1. We avoid Kubernetes' centralized architecture where all components interact through one central API server and share one persistent store
                                1. Twine is sharded, each shard has its own persistent storage at the external
                            2. Separation of allocation and optimization
                                1. This is the the fast-path and slow-path thing, immediate allocation and background optimization of placement
                                2. My questions
                                    1. It looks like the ideas in RAS paper and in MAST paper already show up here in the Twine paper from the very early years
                            3. Comparison (sharding) vs Federation
                                1. Job cannot flow from one cluster to another
                                2. Stranded capacity in a cluster
                                3. Static cluster which cannot grow more servers

        4. [11] Global Capacity Management with Flux    [2023, 2 refs, OSDI23, Facebook]
           https://www.usenix.org/conference/osdi23/presentation/eriksen
           https://www.youtube.com/watch?v=KX6P5db9ZQo
            1. Running production for 2.5 years. Automate the previous cross-team manual bottom-up process to now top-down.
               Map complex service dependency to the proper regions. Using MIP solver. Product-service modelling with RPC tracing.
            2. Highlights
                1. Key challenges
                    1. Automate the process of assigning service to the right region
                    2. The service has complex dependencies
                    3. It needs to be assigned to a number of regions
                    4. Hardware is heterogeneous and requirements vary
                2. Key techniques
                    1. Product-service modelling with RPC tracing
                        1. The overall Flux workflow runs continuously in weekslong cycles to rebalance service capacity across regions according to changing hardware supplies and service demands
                    2. Joint capacity & traffic rationalization solver
                        1. Goals
                            1. Balance spars across regions
                            2. Minimize traffic redistribution
                            3. Minimize the largest region capacity allocation to minimize disaster readiness buffers
                            4. Reduce deviation from the service model
                            5. Deferentially distribute organic growth vs. service capacity growth
                        2. Solution: MIP again
                    3. Global Capacity Orchestrator
                        1. Execution plan
                            1. First provision to to upsize, then reassign and shrink to downsize
                        2. Orchestration
                        3. Capacity ledger
                        4. Reservation management - RAS [37]
                        5. Traffic management - Taiji [18]
                3. Others
                    1. Case Study: FeatureStore

        6. [29] Shard Manager: A Generic Shard Management Framework for Geo-distributed Applications    [2021, 23 refs, SOSP21, Facebook]
           https://research.facebook.com/publications/shard-manager-a-generic-shard-management-framework-for-geo-distributed-applications/
           https://www.youtube.com/watch?v=OMI52r-thFA
            0. In parent paper
                1. From the Rebalancer paper
                    1. "For example, Shard Manager [25] uses Rebalancer to move shards (objects) across servers (bins) to balance the load"

            1. General purpose Shard management framework in Facebook to address various placement and availability requirements in global scale.
               It's designed to onboard most Apps in Facebook. 54% adoption so far.
            2. Highlights
                1. Key challenges
                    1. Support region level shards
                    2. Maintain availability during planned events such as frequent upgrades
                    3. Support sophisticated shard placement requirements
                2. Key techniques
                    1. A generic solver framework
                        1. Figure 13, exactly the same syntax with the Rebalancer paper Figure 1 model spec, and the same "Local Search" to solve.
                            1. My questions
                                1. the Rebalance paper thing has already been running in Facebook production for several years
                        2. Section 5.2, "For ease of use, we adopt a popular constraint solver at Facebook called ReBalancer, which provides a high-level API interface to specify constraints and goals"
                        3. Scaling the Constraint Solver
                            1. Partition a large application. 
                            2. Use Local Search rather than MIP. 
                            3. Leverage domain-specific knowledge.
                    2. Primary-replica migration to uphold availability
                        1. Twine [60] notifies SM's TaskController of a set of pending container operations (start/stop/restart/move)
                        2. The concept of "Negotiable Events" and "Non-negotiable Events"
                    3. Region-aware shard placement
                    4. Leverage the Rebalance solver for complex shard placement.
                    5. Sharding abstraction: SM choose app-key and app-sharding
                    6. Shard Manager Programming Model
                        1. See Section 3.3. It's consumed by App to react to shard changes.
                3. Analysis of Sharded Applications
                    1. Many useful statistics here.
                4. Others
                    1. ZippyDB [45] is a Paxos-based geo-distributed database. It was started on SM in 2013 and has grown to become one of the most widely used databases at Facebook
                        1. ZippyDB: https://engineering.fb.com/2021/08/06/core-infra/zippydb/
                    2. Section 7, imposing adoption of SM, onboarding Apps with legacy sharding.
                        1. reuse a derived SM allocator called Data Placer.

        7. [32] Turbine: Facebook's service management platform for stream processing    [2020, 43 refs, ICDE20, Facebook]
           https://engineering.fb.com/2020/04/21/core-infra/turbine/
           https://research.fb.com/publications/turbine-facebooks-service-management-platform-for-stream-processing/
           https://www.youtube.com/watch?v=9GkETs6k4u0
            1. To bridge the gap between Twine to stream processing. Features in fast task scheduler, predictive auto scaler, and ACIDF application update mechanism.
               The gap is it needs fast & predictive auto-scaling, fast task scheduling, w.r.t. strict SLO, and needs ACIDF update applying.
            2. Highlights
                1. Key challenges
                    1. Bridge the gap between Twine vs stream processing needs
                        1. resource isolation, enforcement, and auto-scaling. realtime auto-scaling as first class citizen.
                        2. don't know resource requirement before hand.
                    2. Strict SLO on stream processing
                    3. Answering what to run (job management), where to run (task management), and how to run (resource management)
                    4. balancing workload fluctuation across clusters, predictively handling unplanned load spikes, and completing high-scale updates consistently and efficiently within minutes
                    5. Facebook's streaming workload is highly variable.
                        1. This is due to diurnal peak, quick experimentations, or even application bugs from upstream
                2. Key techniques
                    1. A solution with loosely coupled microservices
                    2. A fast and scalable task scheduler
                        1. two-level placement: Shard to container via Shard Manager, then place stream processing tasks to shards using hashing
                        2. Shards are periodically load balanced, and Turbine provides mechanisms to safely reschedule stream processing tasks when that happens
                        3. Turbine also performs failure handling to ensure that failures do not cause data corruption, loss, or duplication of data processing
                    2. an efficient predictive auto scaler
                        1. The autoscaler estimates the resources needed for a given stream processing job and then scales up or down the number of stream processing tasks, as well as the resources allocated per task, to achieve the service-level objectives (SLOs). 
                        2. Based on the effect of these scaling decisions (as well as historical workload patterns), the autoscaler can also iteratively adjust the original resource estimates.  
                        3. time_lagged = total_bytes_lagged / processing_rate 
                        4. Preactive Auto Scaler
                            1. not to cause unintended cluster instability ... To address this challenge, Turbine introduces the Pattern Analyzer whose goal is to infer patterns based on data seen and to apply this knowledge for pruning out potentially destabilizing scaling decisions
                        5. Vertical vs. Horizontal scaling
                            1. More tasks (more coordination cost) vs bigger task (more migration cost)
                    3. an atomic, consistent, isolated, durable, and fault-tolerant (ACIDF) application update mechanism
                        1. multiple actors (provisioner service, autoscaler, human operator) may concurrently update the same stream processing job, and the system must ensure that these updates are isolated and consistent
                        2. Turbine uses a hierarchical job configuration structure and merges updates from multiple actors based on which job takes precedence. 
                        3. By separating planned updates from actual updates, Turbine provides atomic, durable, and fault-tolerant updates. 
                        4. A state sync service performs synchronization between the expected and running job configurations, rolling back and retrying if the update fails.
                        5. Implementation
                            1. A hierarchical job configuration structure. It's a Thrift JSON config that merges from bottom to top layers. 
                            2. planned updates -> State Syncer -> Actual updates. Applies round by round per 30 seconds.
                3. Production experience
                    1.  Scuba Tailer service
                4. My questions
                    1. How is Turbine itself made fault tolerant while requiring highly efficient for stream processing?
                        1. The paper seems didn't mention Turbine itself, but Section IV-C described Failure Handling for tasks.
                            1. "Turbine uses a bi-directional heartbeat-based fail-over protocol with the Shard Manager. When the Shard Manager does not receive a heartbeat from a Task Manager for a full fail-over interval (default is 60 seconds), it assumes the corresponding Turbine container is dead, generates a new mapping for the shards in that container, and invokes the shard movement protocol"
                            2. "Each Task Manager has the full list of tasks, enabling Turbine to perform load balancing and fail-over even when the Task Service or Job Management layer are unavailable or degraded"
                            3. "If the Shard Manager becomes unavailable too, Turbine provides a further degraded mode where each Task Manager can fetch stored shard container mapping"
                    2. How does Turbine itself perform load balancing?
                        1. The paper seems didn't mention Turbine itself, but Section IV-B described load balancing for tasks
                        2. The system periodically re-evaluates load metrics and redistributes tasks accordingly to maintain balanced resource utilization. This proactive re-scheduling ensures that no single host becomes a bottleneck due to uneven load distribution. The load balancing algorithm considers resource consumption metrics such as CPU and memory usage, rather than just the number of tasks.

13. What Goes Around Comes Around... And Around...    [2024, 0 refs, SIGMOD24, Stonebraker]
    https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf
    1. Good paper as to review the recent decades of database evolving. 
       Note the paper carries many opinions, Stonebraker is known to be criticizing NoSQL, Hadoop, MapReduce for years.
       A take away is, even database interfaces are much various today, SQL still survived history testing and live lived today.
       The paper also covered in great scope in reviewing every DB branches with comprehensive summaries but nicely written.
       It's also worth reading how authors build their insights and support with analysis.
    2. Highlights
        1. We structure our commentary into the following areas:
            1. MapReduce Systems
                1. My questions
                    1. It's not fair to compare MR with database, because MR is a computation processing system. Seldom today people use database for computation. Stored procedure is usually considered bad engineering practice, which is not portable, not migratable, not compatible with anything new. Even NewSQL is not investing much in stored procedure. Computation shouldn't be put into database because it is a base of data. Database shouldn't be coupled with which platform you choose for computation.

                    The MR example `SELECT map() FROM crawl_table GROUP BY reduce()` requires using a storage procedure in database, otherwise you cannot write a SQL like it. Modern programming language like Python, Java, Javascript are much more expression and powerful than what SQL can do. To use them, you need a data source + processing engine. The processing engine allows you to use modern programming language. Then you come to database + MR. This is where MR is useful. Actually, the pattern of MR is generally observed in many distributed system use cases, which is a great discovery by Google. The successors or MR, Spark, is absolutely defacto popular today. Another outcome of Hadoop is HDFS. HDFS is becoming a defacto data exchange protocol, as you can see every product is trying to support this protocol. In summary, we cannot say Hadoop is a failure. 

                    SQL or the relational schema cannot solve all problems. SQL is not showing compatible with graph database, object storage. Many things that are easy to do in modern programming languages are hard to express in SQL, or not straightforward to express. When accessing database in Java, object-relational impedance mismatch is a common problem. Besides, frequently an App doesn't need all the language expressiveness of SQL, then it needs something more lightweighted than database, for cheaper price and higher throughput. Typical examples are Redis, RocksDB, BigTable, time-series DB.

                    I guess even a top expert may not be right on everything. Otherwise the top expert should be able to make all the money in the world. In fact, he/she can make a great deal of money, but not all the money, which means not all the problems are solved in the right way. Hadoop didn't die, it's evolved, and it becomes the whole big data community now being used everywhere. Without Hadoop or MR or HDFS, it's hard to say whether the same old database community would come out with what we are familiar today, or otherwise everything just sticks to the same old path.  Commonly say, 世界上存在于我20-25岁之前的发明都是自古以来本来就是，存在于我20-25岁之间的发明都是伟大的改变世界的，存在于我20-25岁之后的发明都是新瓶装旧酒。

                    Hadoop successors
                        Storage
                            Unstructured
                                Object storage
                            Structured
                                NewSQL databases
                        Filesystem
                            Distributed filesystems
                            Append-only shared logging infra
                        Computation
                            Spark
                            Stream processing
                        Access
                            NewSQL databases
                            SQL plugin in big data

                2. "At the time, Google had little expertise in DBMS technology, and they built MR to meet their crawl needs"
                    1. Isn't Google already be doing drop IOE and widely using MySQL? Google should have expertise in database. And at that time, there is no existing database production that can fit Google's use case in building global scale processing engines. Note BigTable paper is published at 2006. Using MySQL is common at Internet companies. Spanner paper comes out at 2012.

                    Besides,
                        What are the databases used by Google?
                        https://www.quora.com/What-are-the-databases-used-by-Google

                3. "Google announced that they were moving their crawl processing from MR to BigTable"
                    1. This shouldn't mean HDFS is dead. BigTable runs on Google Colossus Filesystem (GFS), while HDFS is the opensource effort to build something like GFS. Colossus is still alive now in Google. And cloud scale databases built atop a shared logging distributed filesystem is common today (Pangu, AWS Aurora, Azure Storage Stream, Apple FoundationDB), which is alike HDFS which appends big files.

                4. Both MapReduce and BigTable and Spanner are published in OSDI conference rather than SIGMOD.
                    1. My personal feeling is SIGMOD looks conservative and seldom publishes architecture innovation. Main papers in SIGMOD are following the same old database path, optimizing single node / small cluster database, rather than addressing the needs for distributed and scale out. This observation matches with how this paper comments MapReduce/Hadoop as a failed database. It's only in the recent years that SIGMOD/VLDB starts to publish distributed database papers, like CockroachDB and TiDB, but everything must be in SQL.

                5. NoSQL databases are moving to NewSQL
                    1. Long live the SQL. This is the comment that matches the parent paper. But it shouldn't say the papers related to NoSQL don't have value nor these papers shouldn't be published.
                        1) At that time, there is no mature scale-out solution for SQL database yet. ACID has an expensive price that many use cases don't need it.
                        2) NoSQL still generated long lasting value products like RocksDB, stream processing, graph databases, document databases, object storage. Only relational database is still moving to SQL. But today there is still large trend of unstructured data.
                        3) NoSQL is the parent of NewSQL. NoSQL unlocks the first stair, then the industry can move to the next stair. When the industry is moving to NoSQL, people think NoSQL will be the long lasting solution. You cannot predict future simply.
                        4) NoSQL databases did solve problems at the time when they are needed. Even there are better solutions in later years, you have to solve the problem first with the right price.
                    2. Actually, many techniques invented in NoSQL are now being used to build NewSQL.
                    3. Building a scale-out SQL database is non-trivial. It's reasonable for the industry to start with a simple NoSQL + scale-out path, or research starting from it.
                    4. Deprecated technologies are common, since everything is fast evolving. Most papers even didn't get chance to be adopted in industry, but they still got published. More importantly, when publishing a paper, you cannot know what's its future.
                    5. 科技会螺旋发展，螺旋的中部，成熟模式会被破坏，而再发展之后又会被修复
                    6. Today SIGMOD/VLDB are taking a lot of ML papers. They are even not database. It doesn't look reasonable at MR/Hadoop age that SIGMOD keeps rejecting paper saying they are not database. And, why this parent paper can be published in SIGMOD? It's not even a paper, but opinions.
                    7. If Google and almost all Internet companies decided to 另起炉灶 to build new database infra at the MR/Hadoop age, how can the DB research community like SIGMOD be said to be successful in how they guide the research direction or how they review papers?
                    8. Talking about Hadoop being replaced by Impala, Hive, Presto, Drill ... But if the Hadoop was never published, we even won't have those later ones.
                    9. Becoming SQL doesn't mean the DB is becoming relational. Though long live the SQL and many DBs are trying to be compatible with it.

                6. The End of the DB Culture Wars and the New Boom - The Data Dossier    [2021]
                   https://thedatadossier.blogspot.com/2021/03/the-end-of-db-culture-wars-and-new-boom.html

                7. "A lot of the discussion in the two papers was on implementation issues (e.g., indexing, parsing, push vs. pull query processing, failure recovery)"
                    1. Whether something is just implementation depends on the focus, or levels in the abstraction tower. If the focus is SQL, then every database paper is just an implementation issue. Paper review comments like "just engineering" and "too much math" are not uncommon. Actually, if something has value, it should be published. Implementation or optimization commonly has value in engineering or industry track. By narrowing down the focus, it can be called a "technique" which then sound more suitable for papers.

            2. Key-value Stores
                1. My questions
                    1. "It is not trivial to reengineer a KV store to make it support a complex data model, whereas RDBMSs easily emulates KV stores without any changes. If an application needs an embedded DBMS, there are full-featured choices available today, including SQLite [71] and DuckDB [180]."
                        1. From a developer perspective, in many scenarios that using a KV store is better than using a SQL database. Think you are building a distributed NewSQL database with RocksDB.
                            1) What KV store gives you is first simplicity. And simplicity has great engineering value. 
                            2) And, KV store is more performant than SQL DB. You don't need to pay for the complex SQL schema. You don't need to translate everything into SQL and back. And, how can SQL return you a blob, where SQL is weak at working with unstructured data.
                            3) And, KV store allows you to customize you needs. While SQL mostly already bound to certain App scenario, where you are an end user rather than a developer.

                    2. "Examples of this transition are Amazon's DynamoDB [129] and Aerospike [9]." Is DynamoDB still has value compared to NewSQL?
                        1. DynamoDB: Relational (SQL) or NoSQL?
                           https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SQLtoNoSQL.WhyDynamoDB.html
                        2. SQL may not be very friendly to programming. You have to convert data types every time. It doesn't support dynamic/relaxed/flexible table schema. Sometime you only want a simple programming API to access data rather than SQL. Also, SQL costs you the query parsing and query optimizer. Consistency, distributed transaction required in SQL database which is ACID are not cheap. 
                            1) Even the usecase is table interface, it doesn't mean it must be SQL schema. Flexible table schema is common usage today. Also Document databases.
                            2) NoSQL allows you to pay as you need. Get better performance. Rather than SQL DB which requires you to pay for full language feature. 
                            3) SQL is more like read-optimized. It has complex schema to support reads and query. NoSQL is more like write-optimized, simple schema, high write throughput.

            3. Document Databases
                1. My questions
                    1. "But the SQL standard added a JSON data type and operations in 2016 [165, 178]"
                        1. Document DB is moving to SQL, and SQL supports JSON. It appears we don't need Document DB from day 1 and we can build that directly in SQL. Is it true? I think probably only because we have Document DB market success first and then it's possible to push SQL standard to add JSON. From this perspective, it reflects the problem in traditional DB community that they are somehow too much conservative. It failed to adapt to market needs while it can. The industry needs something "unnecessary" to finally make the move.  

            4. Column Family / Wide-Column
                1. In the early 2010s, Google built RDBMSs on top of BigTable, including MegaStore [99] and the first version of Spanner. Since then, Google rewrote Spanner to remove the BigTable remnants [98], and it is now the primary database for many of its internal applications. Several NoSQL DBMSs deprecated their proprietary APIs in favor of SQL but still retain their non-relational architectures. Cassandra replaced their Thrift-API with a SQL-like language called CQL [15], and HBase now recommends the Phoenix SQL-frontend [57].
                    1. Useful summary.

            5. Text Search Engines
                1. The third option is a polystore system [187] that masks the system differences via middleware that exposes a unified interface
                    1. An interesting approach.
            6. Array Databases
            7. Vector Databases
                1. It took less than one year for several RDBMSs to add their own vector search extensions. ... NoSQL systems like MongoDB and CouchDB became popular in the late 2000s and it took several years for RDBMSs to add support for it.
            8. Graph Databases
                1. Can graph also merge into relational DB? Amazon Neptune [45] is a graph-oriented veneer on top of Aurora MySQL. 
                2. SQL:2023 introduced property graph queries (SQL/PGQ) for defining and traversing graphs in a RDBMS
        2. Advancements in DBMS architectures that address modern applications and hardware
            1. Columnar Systems
                1. Stonebraker is one of the creators of columnar DB (C-Store & Vertica).
            2. Cloud Databases
                1. First, because the compute nodes are disconnected from the storage nodes, a system can provide per-query elasticity
                    1. Per-query elasticity is an interesting feature for OLAP.
                2. A cloud environment also provides several benefits to vendors that are not possible with on-prem deployments.
                    1. Foremost is that vendors can track usage trends for all their customers: they can monitor unexpected behavior, performance degradations, and usage patterns. 
                    2. Moreover, they can push incremental updates and code patches without disrupting service.
            3. Data Lakes / Lakehouses
                1. bypassing the traditional route through the DBMS. DBMSs is no longer the "gatekeepers".
                2. challenges to query optimization ... a data lake system may completely lack statistics on newly ingested data files
                3. data lake systems backed by object stores are much cheaper per gigabyte than proprietary data warehouses
            4. NewSQL Systems
                1. Stonebrake is one of the creators of in-memory NewSQL DB H-Store and VoltDB
                2. Companies are most risk-averse with changing OLTP DBMSs than with OLAP.
                3. The aftermath of NewSQL is a new crop of distributed, transactional SQL RDBMSs. These include TiDB [141], CockroachDB [195], PlanetScale [60] (based on the Vitess sharding middleware [80]), and YugabyteDB [86]. The major NoSQL vendors also added transactions to their systems in the last decade despite previously strong claims that they were unnecessary. Notable DBMSs that made the shift include MongoDB, Cassandra, and DynamoDB. This is of course due to customer requests that transactions are in fact necessary. Google said this cogently when they discarded eventual consistency in favor of real transactions with Spanner in 2012 [119].
            5. Hardware Accelerators
                1. History goes around and around
                    1. In the 1980s, vendors fabricated custom hardware to accelerate DBMSs and marketed them as database machines [107].
                    2. The last 20 years have been about using commodity hardware (FPGAs, GPUs) to accelerate queries
                    3. There is more activity in the GPU-accelerated DBMS market.
                2. Several conclusions
                    1. First, these systems are all focused on the OLAP market and only for RDBMSs
                    2. OLAP workloads will continue to move aggressively to the cloud, but special-purpose hardware is not likely to find acceptance unless it is built by the cloud vendor
                    3. A hardware accelerator company has problem to find DBMS adopter company. And DBMS company may not be willing to outsource a critical component.
                       The true market is in large cloud vendors. It can justify the $50–100m R&D cost. They also control the entire stack (hardware and software).
                       Amazon did this already with their Redshift AQUA accelerators [102]. Google BigQuery has custom components for in-memory shuffles [89].
            6. Blockchain Databases
                1. A waning database technology fad is blockchains
                    1. Realworld society requires to place trust to entities, e.g. selling a house
                    2. Performance price, about five orders of magnitude
                    3. All the major cryptocurrency exchanges run their businesses off traditional RDBMSs and not blockchain systems
                    4. No sensible company would rely on random participants on the Internet as the backup solution for mission-critical databases
        3. Parting comments
            1. Never underestimate the value of good marketing for bad products
                1. Oracle did this in the 1980s, MySQL did this in the 2000s, and MongoDB did this in the 2010s. These systems got enough traction early on to buy them time to fix the engineering debt they accumulated earlier
            2. Beware of DBMSs from large non-DBMS vendors
                1. Notable examples include Meta (Hive [197], Presto [63], Cassandra [14], RocksDB [68]) and LinkedIn (Kafka [33], Pinot [59], Voldemort [82]). The most successful examples are 10gen (MongoDB) and PowerSet (HBase), but there also many failed endeavors.
            3. Do not ignore the out-of-box experience
                1. Most SQL systems require one first to create a database and then define their tables before they can load data. This is why data scientists use Python notebooks to analyze data files quickly.
                2. DuckDB’s rising popularity is partly due to its ability to do this well
            4. Developers need to query their database directly
                1. Developers fall back to writing explicit database queries to override the poor auto-generated queries. This is why using a RDBMS that supports SQL is the better choice.
            5. The impact of AI/ML on DBMSs will be significant
                1. powered query interfaces will render SQL obsolete. NL interfaces are an old research topic that dates back to the 1970s [139], but which historically has poor outcomes and thus little widespread use [88].

    n. Related materials
        1. 图灵奖数据库大师Stonebraker师徒对数据库近20年发展与展望的2万字论文 - 叶正盛
           https://mp.weixin.qq.com/s/E3cvL7H-VZNw-q89nofjLg
            1. 图灵奖数据库大师Michael Stonebraker（MIT）和他的学生Andrew Pavlo（CMU）联名
            2. Stonebraker是图灵奖获得者，不老战神，也是PostgreSQL数据库前身Ingres的创始人；Andy在CMU任教，数据库界的网红，他在数据库优化领域有很多探索，他的Database of databases网站几乎收入了全球所有的数据库，并且经常带来很多数据库发展的思考与总结。
            3. 这篇文章表达了关系模型（RM）与SQL依然具备强壮的生命力，一直在吸收业界新的思想，包括文档数据库、图数据库、向量数据库等等，在系统架构方面看好OLAP领域的列式存储模型、云数据库，作者一直鄙视Hadoop架构，认为是历史的倒退，也完全不看好区块链数据库，最后也对AI大模型代替SQL进行评论，并表示当前还并不完备

        2. M. Stonebraker and J. Hellerstein. Readings in Database Systems, chapter What Goes Around Comes Around, pages 2–41. 4th edition, 2005.
           https://people.cs.umass.edu/~yanlei/courses/CS691LL-f06/papers/SH05.pdf
            1. This is the 2005 version of "What Goes Around Comes Around". Also by Stonebraker etc.

14. FastCommit: resource-efficient, performant and cost-effective file system journaling    [2024, 0 refs, ATC24 best paper, Google]
    https://www.usenix.org/conference/atc24/presentation/shirwadkar
    1. Reducing the excessive fsync overhead in EXT4 JBD2, especially when working with NFS. From evaluation, FastCommit almost improves both latency and throughput by 2x.
    2. Highlights
        1. Key challenges
            1. NFS on EXT4 suffers from frequent fsync on small commits. JBD2 also has its own overhead on each commit. More IOs, more bytes overhead
        2. Key techniques
            1. Compact logging reduces journal byte overhead by packing multiple updates in a single FASTCOMMIT log (FCLog)
            2. Selective flushing reduces journal IO overhead by minimizing the number of flushes needed to perform commits
                1. Figure 7 shows what fsync does. Not only does 1 fsync has multiple rounds of interaction with disk, one user write also results in multiple fsync
                2. The optimization ideally can reduce fsync to 1 per commit.
            3. Inline journaling reuses the thread issuing fsync as an opportunistic journal thread instead of waking up the JBD2 thread avoiding an expensive context switch

15. μSlope: High Compression and Fast Search on Semi-Structured Logs    [2024, 0 refs, OSDI24, YScope, Uber]
    https://www.usenix.org/conference/osdi24/presentation/wang-rui
    1. Organize logs by their schema into tables and then apply columnar compression and search.
       Evaluation shows compression ratio 21.9:1 to 186.8:1, 2.34x of ZSTD and 1.70x of LZMA. uSlope search speed is 2.47x of ClickHouse, 8.09x of PostgreSQL.
       The results are so good. It unlocks the potential to build a new generation of log storing/searching platform in this technology.
    2. Highlights
        1. Key challenges
            1. At Uber, JSON 10PB/day semi-structured logs per day, expensive to store nor analysis.
            2. ElasticSearch has high cost on storing the index for logs (almost same magnitude size). And index needs SSD.
            3. ClickHouse, compression ratio is only 4:1, and also needs SSD for fast search.
        2. Key techniques
            1. A merged parse tree to store schemas
                1. Each unique schema is represented at tree leave with a schema map. Schema won't be duplicatedly stored, schema is decoupled from each record.
                2. Figure 2: The merged schema tree of the two records. Figure 7: Merged Parse Tree and Schema Map.
                3. My questions
                    1. how to schema tree is built and updated?
            2. Store log records to different tables by their schema. Compression in columnar manner.
                1. Given log records are now aligned, Columnar compression maximizes both compression ratio and search speed.  
                2. Compression
                    1. Strings
                        1. Timestamp
                        2. Variable
                        3. Log-text
                    2. Integers, float point, boolean
                    3. Arrays
                3. Preserving record order
                    1. Need to add an ID column
            3. Query processing
                1. Query -> AST -> filter through merged parse tree -> table scan
                2. Nearly 1/3 user queries can be early terminated because they do not match any schema in tree.
                3. Kibana Query Language (KQL) as its query language
        3. Background
            1. SSDMS - semi-structured data management systems
            2. CLP [27] - per evaluation, CLP is the second best compared uSlope. CLP is also published by YScope.
                1. CLP: Efficient and Scalable Search on Compressed Text Logs    [2021, 24 refs, OSDI21]
                   https://www.usenix.org/conference/osdi21/presentation/rodrigues
                2. YScope - CLP: Compress Your Logs. Search Without Decompression.
                   https://yscope.com/
                    1. Website use cases are Uber

16. Horus: Granular In-Network Task Scheduler for Cloud Datacenters    [2024, 1 refs, NSDI24]
    https://www.usenix.org/conference/nsdi24/presentation/yassini
    https://www.youtube.com/watch?v=kI1kCMLNTWs
    1. In-network scheduler at network switches for microsecond latency task scheduling at datecenter scale
    2. Highlights
        1. Background
            1. Granular computing, In-network scheduler
        2. Key challenges
            1. Need task scheduler with microsecond scale latency
            2. Today's in-Network scheduler can reduce latency but only works on rack scale. Need datacenter scale.
        3. Key techniques
            1. Load-aware scheduling
                1. a zero-queue scheduling system minimizes task tail response time
                2. takes 2 random samples from the queue lengths - the power of two random choices
                   https://medium.com/the-intuition-project/load-balancing-the-intuition-behind-the-power-of-two-random-choices-6de2e139ac2f
            2. Lazy state update
                1. a switch may not need to immediately update its state if it can make accurate decisions using its current state. Our approach identifies when an update is needed by calculating a drift between actual load values and the load information available at schedulers, and it only updates the state of a scheduler when the drift may negatively impact the scheduling quality
                2. Then, a leaf scheduler sends the update message only if the difference between the current and previous average load values is greater or equal to one
            3. Localized State
                1. logically grouping the distributed schedulers and maintaining the state within each group
                2. Distributing Worker State to the Leaf Layer. Distributing Rack State to the Spine Layer.
        4. Others
            1. Appendix A.4 Pesudo code and P4 implementation

17. Trinity: Syncretizing Multi-/Long-tail/Long-term Interests All in One    [2024, 0 refs, ByteDance]
    https://arxiv.org/abs/2402.02842
    1. One model to output all three, long-term interest, multi-interest, long-tail interest. On production at Douyin.
    2. Highlights
        1. Background
            1. Long-term interest reveals multi-interest. Multi-interest is valued for long-tail interest. Long-term interest clarifies long-tail interest.

    n. Related materials
        1. 抖音兴趣建模新突破——Trinity：多兴趣/长期兴趣/长尾兴趣三位一体 - 水哥
           https://zhuanlan.zhihu.com/p/681751105?utm_id=0
            0. Useful and well written. It reveals the backing thoughts of the paper.
            1. 相比购物，短视频的多兴趣的“多”可能是一个更大的数字，对多兴趣的优化渴望更加强烈
            2. 我们有三个“戒律”：
                1. 长期兴趣体现多兴趣（long-term interest reveals multi-interest）：虽然用户的历史序列我们一直用，但模型里用的往往是那种短期序列，比如最近20个xxx这类（SIM虽然长，但在精排以外的地方还比较少），有一个问题是它很容易被某种热点和潮流给塞满。我自己的亲身体会就是22年2-3月那会儿狂刷《老头环》，那我的行为序列里可能前50，前100都是这个游戏的视频，你根本不知道我以前还看塞尔达，刺客信条这些吧。但如果把行为序列拉的足够长，就能发现哦我原来还喜欢看这些。
                2. 多兴趣的价值在于长尾兴趣（multi-interest is valued for long-tail interest）：用户的兴趣里当然有很多都是热门内容，反过来说它能成为热门内容也是因为人人爱看。像小姐姐，热点新闻，美食这些的，谁都爱看。但问题是这些东西你不需要特别优化了，已有的环节已经优化的足够好了。一个较为成熟的系统，小姐姐那不是分发的驾轻就熟（要不然DAU咋上去的呢是吧）？所以我们说多兴趣，更多可能说的是一些相对没那么热门的主题，比如种地，赶海，甚至更冷门的书法这些。
                3. 长期兴趣辨别长尾兴趣（long-term interest clarifies long-tail interest）：虽然叫长尾兴趣，其实这些内容的分发量并不是很低，但问题是，谁是真正的受众需要鉴别。长尾内容分发不会很低的原因一部分是系统一直在持续探索，所以会给很多人分发，试探他们爱不爱看。但如果你就盯着人家一两次消费记录去追打，很可能会起到反效果。这时候需要的是更长时间的统计，假如我在最近一年的历史记录里面都被你断断续续找到了《完蛋》的消费记录，那我就只好含泪承认我对这游戏的喜爱了。
            3. 所以想要把兴趣建模好，绕不开要解决这个兴趣遗忘的问题。
                1. 这个逻辑给出的方向是，抛弃在online learning上做修改的思路，直接转向其他技术方案。
            4. 看看我们需要什么功能以及对应有什么工具：
                1. 一套聚类或者分类体系，它是可穷举的有限集合， 以此为基础可以完成统计。也就是说，统计直方图会是横坐标为cluster ID，而纵坐标是在这个cluster下的历史行为强度。
                2. 一套“公平”的embedding来组成这个聚类体系，它不会太偏向于现在的新题材，而对于较早之前的行为估计失准。
                3. 定制化的策略，针对直方图的形态具体进行分发。
            5. 那么这就是Trinity的训练过程了
                1. 首先对于当前的item，按照SIM的方法搜索出用户在同个tag下的历史序列，平均池化, 二者分别过MLP后得到对应的embedding（图中两个绿色方块）。
                2. 同时我们维护两层聚类的可学习的embedding，即一级128个cluster，二级1024个cluster，cluster的embedding在图中分别由深黄色，浅黄色两套方块组成。
                3. 对于当前item，首先它要和SIM出来的embedding来协同学习，也就是给一个推荐loss(比如按照staytime做一个带权重的in-batch loss这样，或者按照finish与否给一个BCE loss)。
                4. 同时，它在一二级聚类下找到最近邻作为它的代表embedding也去和SIM的embedding做推荐loss。第一个loss能够训练出较好的embedding表示，而后两个则是按照VQ-VAE的方式去做一个索引挂载，得到的是这个item对应一二级的cluster ID是什么。
                5. 这个信息会存储到一个实时的k-v存储工具中，在后面会用到。
                6. 我们有训练好的item embedding表示，也把item映射到了有限的cluster集合下，完成了进行统计的基础。
                7. 要注意的一点是，这个过程中索引挂载（即item属于哪个cluster）是随着训练实时流式完成的，并且整个过程完全对齐推荐目标，是end2end的。
            6. 接下来看看如何分别优化多兴趣，长尾兴趣和长期兴趣。
                1. 多兴趣
                    1. 核心是利用统计直方图识别出置信被消费，但欠分发的cluster进行加强。
                2. 长尾兴趣
                    1. 只要我们知道哪些cluster是长尾主题的，看用户的直方图在这些长尾主题上是不是有显著的兴趣表达就可以了，谁爱看某个长尾类目我们就给加强分发。
                    2. 越是时间间隔大的cluster，就越是表达长尾内容的cluster，这样我们就脱离了任何标签体系，仅靠Trinity自己识别出长尾cluster了。
                3. 长期兴趣
            7. 总结：
                1. Trinity的主体是借助了统计工具，它的路线选择不是【花力气优化现在的框架】，而是【彻底走新方向，让两个方法互补】
                2. 统计方法几乎直接指出要用直方图，实际上直方图在以前的很多领域都有广泛的运用，方法也很直观，最经典的就是词袋模型那一套了，里面涉及的编码方式也和Trinity用到的VQ-VAE有关联（如果有同学感兴趣请留言，我可以再写一篇来专门介绍）。
                3. 有了直方图以后解决三个兴趣的思路是很自然的，不过很多实现细节还是需要online learning模型。
```
