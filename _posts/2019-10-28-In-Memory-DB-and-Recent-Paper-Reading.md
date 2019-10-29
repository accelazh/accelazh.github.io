---
layout: post
title: "In-Memory DB and Recent Paper Reading"
tagline : "In-Memory DB and Recent Paper Reading"
description: "In-Memory DB and Recent Paper Reading"
category: "storage"
tags: [storage, paper, in-memory DB]
---
{% include JB/setup %}


Recent paper reading. Limited selection to only recommended papers. The in-memory DB survey paper is good landscape.

Section 1

```
1. readings: note previous separated paper reading notes
 ---- starting from 2019-06-24 ----
    1. In-Memory Big Data Management and Processing: A Survey    [2015, 256 refs]
       https://www.comp.nus.edu.sg/~ooibc/TKDE-2015-inmemory.pdf
        1. very good paper. summarized leading in-memory database and their key technologies in depth.
        2. highlights
            1. leading in-memory database projects
                1. VoltDB
                    1. OLTP
                    2. concurrency: single thread per core, single thread no locking
                    3. partition: Horticulture auto partition
                                  and Markov model-based approach to predict, speculative commit
                    4. data overflow: use a transaction to evict cold tuple
                    5. checkpoint: a distributed transaction to put sites to shadow copy-on-write
                    6. command logging scheme /  light-weight logging strategy [131]
                    n. more
                        1. https://www.voltdb.com/product/data-architecture/no-wait-design/
                        2. https://www.voltdb.com/product/data-architecture/modern-disk-persistence/
                        3. https://www.voltdb.com/product/features-benefits/indexes-materialized-views/
                2. Hekaton
                    1. OLTP. totally integrated with SQL Server, allow transaction cross other stores
                    2. concurrency: lock-free, bw-tree, hash index, non-blocking MVCC
                                    appending update delta to pages, avoid update-in-place
                                    page management by LLAMA [229], good paper too, to cope with append-only B-tree's delta changes propagate to root issue
                    3. query: compile SQL to C code, than native code, compile once and run many times
                    4. fault tolerance: incremental checkpoing, group commit logging
                    5. data overflow: Project Siberia
                        1. offline classification of hot/cold by logging tuple access
                        2. use Adaptive Range Filter and Bloom Filter to tell which data is stored cold on disk
                            1. Adaptive Range Filters for Cold Data: Avoiding Trips to Siberia    [2013, 44 refs]
                               http://www.vldb.org/pvldb/vol6/p1714-kossmann.pdf
                                1. good paper.
                                2. Range Filter is essentially a tree of ranges
                                3. Adaptive: Really clever design. The tree nodes can split and merge according to access miss/hit, w.r.t to Bloom Filter.
                                             the tree can be trained through data and workload
                    n. related
                        1. Hekaton: SQL Server’s Memory-Optimized OLTP Engine   [2013, 323 refs]
                           https://www.microsoft.com/en-us/research/wp-content/uploads/2013/06/Hekaton-Sigmod2013-final.pdf
                            1. good paper. it is famous as referenced in in-memory databases

                3. HyPer (http://hyper-db.de/index.html)
                    1. combines both OLTP and OLAP
                    2. OLAP: very clever. use fork() to shadow memory pages, as a snapsot to run OLAP.
                             OS and hardware shadow virtual memory support to speedup
                    3. concurrency: Adaptive Radix Tree (ART) tree.
                                    transactions executed sequentially in a lockless style, in partitions (like VoltDB's?)
                    4. query: compiled into Low Level Virtual Machine (LLVM). JIT.
                              this approach is also used by MapD.
                    5. snapshot: also by fork() the process
                    6. key paper
                        1. Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems    [2015, 104 refs]
                           https://db.in.tum.de/~muehlbau/papers/mvcc.pdf
                            1. good paper.
                            2. highlights
                                1. different from Hekaton, Hyper write-in-place. so that, scan can be efficient because doesn't need to follow delta versions
                                2. to support multi-version, a record is linked by a VersionVector, to each previous version
                                   and a transaction's modification set are tracked by undo buffer, cross-linked with the above
                                3. serialization validation: before commit, must pass the serialization validation
                                    1. different from Hekaton or PostgreSQL's SIREAD lock, i.e. per record locking, which is expensive for large read scan
                                       we use Precision Locking. it checks the overlap of Predictates (derived in SQL), rather than per-record, to discover conflict.
                                       underlyingly, it uses a Predicate Tree (PT) data structure to manage predicates overlap detection. Predicate Logging to track.
                                       a table tracks recentlyCommited transactions for checking.
                                    2. question: how to ensure no new transaction violation, after serialization validation passed, but before write commit?
                                        1. I guess it's by a atomic operation update .. didn't find details in paper.
                                4. VersionedPositions
                                    1. this is to indicate in a range, outside of [begin, end) has no versions.
                                       so scan can go with max speed
            2. more: core technologies, main techniques, future opportunities, etc
                     and the Table 3 QUALITATIVE COMPARISON
        n. related
            1. MapD - GPU database
               https://devblogs.nvidia.com/mapd-massive-throughput-database-queries-llvm-gpus/
               https://www.zhihu.com/question/21003317
               http://www.smallake.kr/wp-content/uploads/2014/09/mapd_overview.pdf
                1. interesting.
                   it also uses LLVM to compile queries JIT.
                   GPU has high FLOPS and high memory bandwidth than CPU
                   rich analytics and visaulization support in database

    2. A Unified Theory of Garbage Collection    [2004, 66 refs]
       https://www.cs.virginia.edu/~cs415/reading/bacon-garbage.pdf
        1. good paper. one paper to go through all major GC designs
        2. highlights
            1. reference counting and tracing and too main approaches for GC.
               they are foundamentally equivalent to each other, and complementary to each other
               morden GC implementation is essentially a mix of each other
            2. tracing can detect cycles. but how to GC cycles in reference counting?
                1. backup tracing
                2. trial deletion
            3. interesting GC algorithms
                1. the train algorithm
                    1. multi-heap GC by separating "Cars" and "Trains"
                    2. to detect cycles, move objects referenced cross car by later referencer's car
                        1. it's a equivalent to trial deletion
            4. cost analysis
                1. the abstraction of pointer density, mutation rate, allocation rate are interesting
                   we can divide object graph to sections according their patterns. and use probability theory to further model 
        n. related materials
            1. Hacknews discussion
               https://news.ycombinator.com/item?id=14823054

    3. Socrates: The New SQL Server in the Cloud    [2019, 0 refs]
       https://www.microsoft.com/en-us/research/uploads/prod/2019/05/socrates.pdf
        1. Microsoft SQL Server architecture change to match with Amazon Aurora.
        2. highlights
            1. separation of availability and durability
                1. primary -> multiple read secondaries. nodes for compute
                2. quick data durable by Landing Zone,
                   then replicate by XLOG to read replica secondaries
                   to Azure Storage for longer persistence
                3. Azure Storage for snapshot PIT (Point-in-Time) recovery
                4. compatible to exsiting SQL Server
                    1. "A Socrates Primary Compute node behaves almost identically to a standalone process
                        in an on-premise SQL Server installation. The database instance itself is unaware of the
                        presence of other replicas"
            2. concernts on
                1. long-running transactions
                2. size-of-data operations
            3. pushdown storage functions to Page Servers, to close to data
                1. bulk loading, index creation, DB reorgs, deep page repair, and table scans
        3. questions
            1. the paper says Landing Zone is for durability, but that looks like only a single node

    4. 论文笔记：[FTNDB''07] Architecture of a Database System
       https://zhuanlan.zhihu.com/p/72585869
       Architecture of a Database System - Joseph M. Hellerstein, Michael Stonebraker and James Hamilton
       http://db.cs.berkeley.edu/papers/fntdb07-architecture.pdf

    5. X-Engine: An Optimized Storage Engine for Large-scale E-commerce Transaction Processing  [2019, 0 refs]
       https://dl.acm.org/citation.cfm?id=3314041
        1. very good paper. LSM-tree based MySQL engine, with various optimizations.
        2. highlights
            1.  Alibaba e-commerce's notable traffic pattern
                1. drastic TPS increase with major sales promotion events
                    1. the tsunami problem
                    2. the flood discharge problem
                2. quick shift of hot/cold of different records
                    1. the fast-moving current problem
            2. X-Engine is a LSM-tree based engine, for OLTP, can be used for MySQL (vs InnoDB, MyRock)
               X-Engine can also be used as part of PolarDB atop PolarFS
               Table stored in row-oriented format
                1. hot/ward/cold data tier - memory/NVM/SSD/HDD
                2. read path
                    1. extent layout
                        1. 2MB per extent for reusable during compaction
                           and for incremental cache replacement
                    2. Row cache - for point lookups
                       Block cache - for range queries
                    3. Multi-version Metadata Index - copy-on-write to create metasnaphost
                        1. LSM-tree is easy to hit the problem that, if a read misses in memtable
                           it has to scan each level to find the data
                        2. the metadata index tracks extents across memtable and levels
                    4. Incremental cache replacement
                        1. instead of simply evicting old cache, we replace old blocks in cache with new ones
                           during compaction
                3. write path
                    1. Multi-version memtable
                        1. distinct keys organized in skiplist
                           each key's multiple versions stored in linked list
                        2. to reudce overhead of scanning unnecessary old versions
                    2. Asynchronous writes in transactions
                        1. transtion thread drop IOs in task queue
                           IO threads drain queue async
                        2. batching tasks
                    3. Multi-staged pipeline
                        1. decompose write path into multiple stages
                           each stage async with separated thread pools
                    4. Flush and Compaction
                        1. flush to avoid out-of-memory failures in X-Engine, upon incoming spikes of transtions
                        2. Data reuse - extent split, merge, and reuse. extent index to point fragments
                        3. FPGA offloading to reduce CPU usage during compactions
                            1. split compaction into mutliple small tasks, streaming them
                        4. Scheduling compactions
                            1. rule-based compactions
                            2. intra-Level0 compactions
                               minor compactions to merge adjacent levels
                               major compactions to merge largest level and largest level - 1
                               self-major compactions for merge intra-largest level
                            3. compaction jobs are enqueued into a priority queue
                4. Evaluation
                    1. ~10% less QPS vs InnoDB for high read workload, but significantly faster for high write workload (Figure 9)
                       Range lookup QPS less than InnoDB (Figure 14)
                        1. For write QPS and latency, anyway better than MyRock/RocksDB
                    2. challenges and strategies
                        1. The tsunami problem
                            1. asynchronous writes, the write task queues, and the multistaged pipeline
                        2. The flood discharge problem
                            1.  FPGA improves throughput by 27% with reduced variances
                        3. The fast-moving current problem
                            1. Zipf, row cache and block cache
        3. related materials
            1. Zipf Distribution
               https://en.wikipedia.org/wiki/Zipf%27s_law
               https://zh.wikipedia.org/wiki/%E9%BD%8A%E5%A4%AB%E5%AE%9A%E5%BE%8B
                1. it is used to generate biased traffic. handy

            2. Faster: A Concurrent Key-Value Store with In-Place Updates    [2018, 18 refs]
               https://www.microsoft.com/en-us/research/uploads/prod/2018/03/faster-sigmod18.pdf
               source code: https://github.com/microsoft/FASTER
                1. very good paper.
                   declare to be the fastest hashtable. opensourced. And written in C# (amazingly).
                   epoch protection framework for lasy synchronization. But In-place just means to update memory ..
                2. highlights
                   1. epoch protection framework - lazy synchronization
                        1. threads share a table to each own an Epoch
                           an action only happens when all threads passed certain epoch.
                        2. compared the lock and do, the "epoch" acts like an "agreement"
                           when all threads passed the "epoch" -> all threads agree.
                           then we can do the action
                            1. E.g. to delete a block after all threads released it
                        3. impact of adopting Epoch Protection Framework is that,
                           the entire design of memory buffer and disk data looks like a circular buffer
                           so that threads are always rolling forward, so that Epoch applies to such pattern
                        4. questions
                            1. since threads share the Epoch table, and they need to update it
                               would that cause a lot of cache invalidation, cache bunching, etc?
                    2. the hashtable index
                        1. Faster's data are plain in circular buffer, it all needs the hashtable to access
                        2. Hash bucket format - very cache aligned - 64 bytes split into 8 slots
                        3. Figure 3. To handle Insert bug, use the tentative bit
                            1. 2 threads, first insert a value in the first empty slot - this prevents further threads to come race insert
                               due to deletion, thread 1 and thread 2 may happen to have inserted duplicated value, which is not allowed
                               here is only a tentative insert, marked with tentative bit. threads need to scan again to confirm no duplicates.
                               if really no duplicates, clear tentative bit, so that is a successful insert
                            2. it's like a double-checked locking
                        4. hybrid log
                            1. Disk + memory are managed as a circular buffer, the boundaries are HeadOffsets and ReadOnlyOffset
                                1. after ReadOnlyOffset is the In-place update section.
                                   HeadOffset to ReadOnlyOffset is the read-only section
                                   before HeadOffset is on disk
                                2. this design makes newer data always in-place update, works like being cached
                                   older data enters the read-only section, to be later flushed to disk (NVM)
                                3. problems
                                    1. we can hardly control the time of new writes flushed to disk, it can lose data upon failure.
                                       but should be OK if we just use FASTER as a caching system, like memcache
                            2. Thread-local ReadOnlyOffset
                                1. thread-local RO Offset can be different.
                                2. We use Minimal RO Offset, Maximum RO Offset,
                                   Safe Read-only Offset (updated by Epoch Action), Fuzzy Region
                                   to fine-grain handle the updates

            3. Optimizing Space Amplification in RocksDB    [2017, 44 refs]
               http://cidrdb.org/cidr2017/papers/p82-dong-cidr17.pdf
                1. interesting papaer. Facebook's RocksDB engine for MySQL, to handle space amplification with various methods
                2. highlights
                    1. LSM-tree is more space efficient than B-tree, because B-tree pages have empty space
                       and LSM-tree writes space consecutively 
                    2. LSM-tree dynamic level size adapation - each level is 10x larger than upper,
                       3total 1.111x% space amplification
                    3. tiered compression given different levels have different access frequency
                    4. Prefix Bloom filters

    6. Nines are Not Enough: Meaningful Metrics for Clouds    [2019, 0 refs]
       https://storage.googleapis.com/pub-tools-public-publication-data/pdf/f647d24ee7eeb338acebf1eb73a5d11b357620b0.pdf
        1. interesting paper. rethinking the SLA/SLOs in clouds and give some different lights
        2. highlights
            1. Contractual SLOs
               Service Level Expectations
               Compositional uses of SLOs
            2. Some SLOs depend on customer behavior
            3. how many SLOs and how to collect data
            4. resource sharing w.r.t SLOs
            5. Customer Behavior Expectations, or CBEs

---- starting from 20190905 ----
    1. Exploiting Commutativity For Practical Fast Replication    [2019, 1 refs]
       https://www.usenix.org/sites/default/files/conference/protected-files/nsdi19_slides_park.pdf
       https://www.usenix.org/system/files/nsdi19-park.pdf
        1. interesting. if ordering between data blocks is not a concern, we can replicate them out of order to reduce RTT
        2. highlights
            1. the base problem of this paper is a master - backup replication
            2. client sends to 1 master, and in same time N Witness out of order for N fault tolerance
               so that 1 RTT. rather than first master then backup the 2 RTT
            3. for the dependent writes that needs ordering, need to send to master to order
                1. questions
                    1. problems: if Witness rejected due to need ordering,
                                 then it needs extra RTT to fallback to traditional ordered replication
                    2. comparing to cloud system, it may exploit parallel of replicating many objects in the same time
                       or it can use a bitmap to track data block received
                        1. but to reduce RTT, especially for SSD storage or in-memory storage, this method should be useful.
                        2. but if client to server network (internet) is much slower than server to server network (datacenter)
                           this paper's method may not be very effective
                        3. anyway, the view perspective of RTT is useful for analyzing similar problems
            4. implemented on Redis to support fast fault tolerant replication
                           on RAMCloud to make replication fast
                1. so, the target is mainly the in-memory systems

    2. DistCache: Provable Load Balancing for Large-Scale Storage Systems with Distributed Caching    [2019, 3 refs]
       https://www.usenix.org/sites/default/files/conference/protected-files/fast19_slides_liu.pdf
       https://www.usenix.org/system/files/fast19-liu.pdf
        1. FAST19 best paper. very good paper
           Based on "Small Cache, Big Effect"'s caching O(n_server * log(n_server)) can balance the cluster
           For multi-clusters, the paper introdced a second layer of caching. using a different hasing function.
           so that multi-cluster is now load balanced by caching.
        2. highlights
            1. how big is the second layer of caching?
                1. same number of nodes with first layer
                2. this is determined by throughput of a cache node should be as much as the cluster (n servers)
            2. how to partition / distribute keys across the cache nodes?
                1. use two different independent hasing. so hot keys are at least balanced in one caching layer
                    1. this is the smart place
                2. two caching layer caches duplicated keys. A key is duplicated twice
            3. how to query the two caching layer?
                1. "The power of two choices".
                   The client just check which of two cache nodes hosting the target key has smaller queue length
                   and then query that cache node.
                    1. this is the second smart place
                2. without even complex algorithm, the local greed plays well
            4. how to manange the cache replicaiton across the two cache layers?
                1. yes, compared to traditional caching, a key is replicated twice, twice the overhead, in the two caching layers
                2. the paper didn't mention much about cache replication.
                   typically it can be 2PC transactions
            5. implementations
                1. interesting SwitchKV / NetCache.
                   to put cache in switch nodes looks very applicable for this paper's case
            2. the paper gives math proof.
        n. related materials
            1. The Power of Two Choices in Randomized Load Balancing    [2001, 1072 refs]
               https://www.eecs.harvard.edu/~michaelm/postscripts/tpds2001.pdf
                1. the result is so obvious and foundamental today. it's the key of tail latency reduction
                   customer can select d out of n total servers to join in the shortest queue
                   d = 2 is exponentially better than d = 1. d = 3 is constant factor better than d = 2.
                    1. actually clients may cache queue status for available data copy to choice to best one
                       it should be the d = n case.

            2. Small Cache, Big Effect: Provable Load Balancing for Randomly Partitioned Cluster Services    [2011, 76 refs]
               http://www.istc-cc.cmu.edu/publications/papers/2011/loadbal-socc2011.pdf
                1. good paper and insights. Cache can do load balancing.
                   Suppose n servers, caching the hottest O(nlog(n)) objects, irrelavant to total object cound,
                    will bound the hottest sever load to a constant.
                    I.e. cache size O(nlog(n)) is enough to balance the cluster of n servers
                2. highlights
                    1. the paper has detailed math. See Equation (11) for the result
                    2. the instinctive view is, if a server is very hot, it means the access to object is hot and biased,
                       so that object will be cached, as a result the server shouldn't be that hot
                    3. questions
                        1. there is a foundamental limitation that, the paper assumes the adversary client queried x
                           different keys, are perfectly balancedly distributed on the servers.
                            1. however this is often not true. and if this is not true, the worst hot server load has no bound
                            2. the well side is, servers can do hot data migration / balancing, so to reach the theory bound

    3. EROFS: A Compression-friendly Readonly File System for Resource-scarce Devices    [2019, 0 refs]
       https://www.usenix.org/conference/atc19/presentation/gao
        1. good paper. fixed output size compression (in unit of page / block size) to improve system efficiency
           besides, the paper did many improvement to use memory more efficiently
           it is used in smartphones for readonly filesystems to host OS data.
           already shipped in 10M+ Huawei phone EMUI 9.1 and merged in Linux Kernel 4.19
        2. highlights
            1. why fixed output size compression?
                1. tranditional compression uses fixed input size chunks.
                   the output may span disk block boundaries, so reading small data has unnecessary overhead
                2. the fixed output size is aligned with page / block size, so fewer extra disk block reads
                   and according to paper, the output page / block size is smaller than tranditional
                3. to generate the fixed output size compression results, the paper LZ4 in a rolling window
                   to feed as much data as necessary to read the fixed output size.
                    1. according to evaluation results, the compression ratio is comparable to tranditional
                    2. though generating those fixed size output page / blocks must be slow,
                       but write speed is not a concern for readonly filesystems
            2. decompression improvement to save memory
                1. in general: reuse allocated pages, (including vmap)
                               don't copy data if not necessary
                               in-place decompression
                2. Per-CPU buffer decompression. for decompression smaller than four pages, just use this,
                   rather than allocate / map new memory. overhead is extra memory copy
                    1. per-cpu temporary page is also used in rolling decompression to buffer data
                3. rollout decompression. to decompress in-place,
                   and to exploit that LZ4 only looks back 64KB, so rolling window can be 64KB (16 pages)
            3. Image patching
                1. OS updates can be appended at tail of readonly FS, read like OverlayFS
                   this avoids expensive rewrites, which is even not possible since it needs to shift every piece of data
            4. Evaluation
                1. SquashFS and Ext4 look like typical candidate on smartphones, besides EROFS
                    1. SquashFS 128K has higher storage saving, while EXT4 has slightly higher memory saving.
                       But no one got the both well side like EROFSs
                2. reduce ~50% storage overhead while ~30% memory.
                   even higher throughput. (no latency chart?)
                   compression ratio is comparable
                3. workloads - random, sequential, and
                   stride - this is typical for OS load, reading first 4KB in every 128KB data

    4. Datacenter RPCs can be General and Fast    [2019, 17 refs]
       https://www.usenix.org/sites/default/files/conference/protected-files/nsdi19_slides_kalia.pdf
       https://www.usenix.org/system/files/nsdi19-kalia.pdf
       https://github.com/erpc-io/eRPC
        1. very good paper. NSDI19 best paper. pushing the boundary of RPC design, without special hardware.
           it achieves comparable latency and small/large PRC rate compared to those using programmable switches, FPGAs, or RDMA
        2. highlights
            1. Expect loss is rare in datacenter, because Switch bufer >> BDP (bandwidth-delay product)
                1. we choose to make the common case (no retransmission) fast
                   we use unsignaled packet transmission in eRPC
                    1. overhead is, we flush the TX DMA queue after queueing a retransmitted packet,
                       which blocks until all queued packets are DMA-ed
                        1. node failure events also cause expensive retransimision
            2. Message layout for small messages to reduce DMA count
                1. Header1 + Data1 .. DataN + Header2 .. HeaderN
            3. RDMA fundamental problems for RPC
                1. RDMA clients write requests directly to per-client circular buffers in server memory
                    1. server must poll these buffers to detect new requests
                    2. the number of circular buffers grows with the number of clients
            4. congestion control - based on observation that 99% datacenter links are < 10% utilized
                1. simplify and make congestion control fast, since congestion is few assumed in datacenter
                2. if RTT < 50us on ungested network, we bypass TX_rate update
                    1. TX_rate update is addictive
                3. if on ungested network, we bypass putting packet in rate limiter
                4. batch timestamp RTT measurement
            5. the RPC optimized to use special hardware are
                1. RDMA: FaRM, FaSST
                2. FPGA: KV-Direct
                3. Programmable Switches: NetChain

    5. SILK: Preventing Latency Spikes in Log-Structured Merge Key-Value Stores
       https://www.usenix.org/sites/default/files/conference/protected-files/atc19_slides_balmau_0.pdf
       https://www.usenix.org/system/files/atc19-balmau.pdf
        1. good paper. ATC19 best paper.
        2. highlights
            1. focus on LSM tree's write latency rather than throughtput
            2. root cause of write tail latency spikes
                1. On disk L0 layer reaches full capacity but didn't flush timely
                   so the in-memory component flush is temporarily paused
                2. naively rate limit disk compation may slow down L0 flushing
                   causing write tail latency spike too
                3. postponing compaction makes latency low at first, but
                   eventually slows down due to pack back
            3. SILK the IO scheduler
                1. allocate IO bandwidth to compaction if client reads/writes not busy
                2. prioritize lower-level disk compactions
                3. disk compaction on lower-levels can preempt higher-levels 
```

Section 2

```
2. readings: recent storage papers
    1. The Adaptive Radix Tree: ARTful Indexing for Main-Memory Databases    [2013, 201 refs]
       https://db.in.tum.de/~leis/papers/ART.pdf
        1. good paper. For in-memory DB index, radix tree + adaptive node size + node merging
        2. highlights
            1. used in HyPer
            2. AFR's performance comparable to Hashtable, but friendly to range queries, and is very space efficient.
               index structure is key performance bottleneck for in-memory database
            3. trees, vs hashtables, vs trie trees
            4. radix tree - i.e. the common sense radix tree, each level indexed by a fixed length array (node)
               adaptive - i.e. change the node size
                1. node4, node16, node48, node256
                2. nod16, save explict key (chunk), find key by binary search, or SIMD instructions
                3. node48, clever, to use first a 256-slot array as index, then to 48 pointers
                   it's smaller than node256, because the 256-slot array can has < 1 byte per slot
            5. leaf nodes can be inline - multi-value leaves, combined pointer/value slots
            6. collapsing inner nodes
                1. lazy expansion - remove path to single leaf, but require keys to store at leaf
                2. path compression - single child nodes are merged into child node.
                                      a vector to track merged key prefix, or delay compare to leaf node
            7. Evaluations - abundant
        3. related materials
            1. http://daslab.seas.harvard.edu/classes/cs265/files/presentations/CS265_presentation_Sinyagin.pdf
            2. https://blog.csdn.net/matrixyy/article/details/70182527
            
            3. HOT: A Height Optimized Trie Index for Main-Memory Database Systems    [2018, 8 refs]
               https://dbis.uibk.ac.at/sites/default/files/2018-06/hot-height-optimized.pdf
               https://www.youtube.com/watch?v=1F1oMFwLTq0
                1. good paper. highly optimized Trie tree for in-memory DB index. outperforms all state-of-arts
                   compared to ART, features in that compound node of Patricia sub-trie act as a dynamic fanout span.
                2. highlights
                    1. typical in-memeory database index: ART, HOT, Masstree, Bw-tree, hashtables
                    2. problems from AFR, and improved in HOT
                        1. ART handles integer keys well,
                           but for string keys the lower levels usually have under desired fanout.
                            1. the underlying span size of different data at different levels depends on actual data pattern
                               i.e. sparsely distributed data
                        2. HOT adaptively increase fanout, thus reduces height
                           number of bits considered in each node is not fixed
                    2. general trie tree optimizations
                        1. merge nodes with only one child
                        2. increase the span (per node bits to discriminate branch out)
                        3. adaptive node structure (ART)
                        4. adaptive span bits
                    3. HOT
                        1. tree structure
                            1. it's a binary tree
                            2. Patricia sub-trees are grouped as a compound node. i.e. cross nodes are linked by pointers
                               inside compound node, conceptually it is a Patrica tree, but implemented as a compact bit string
                                1. so that, overall tree height are low
                            3. how to divide Patricia sub-trees - K-Constrained Tries
                                1. parent compound node hight = max(child node height) + 1
                                   as referenced [17], this gives optimized tree partitioning
                            4. how to maintain tree structure?
                                1. leaf node pushdown
                                2. parent pull up
                                3. overflow resolution
                        2. node structure
                            1. Partial Keys - those bits that branches in Patricia trie (discriminative bits)
                               use a bitmask to extra Partial Keys as the index to value slots
                            2. small to large node size
                            3. how to handle insertion to nodes that adds / remove discriminative bits?
                                1. Partial Key sparse representation to leave blanks for new key bits
                                2. Copy-on-write re-construct the node
                                   and borrowing the previous node until the first mismatching bit
                        3. Optimizations
                            1. SIMD instructions, PEXT, PDEP
                            2. cacheline aligned node structure
                            3. pack node type within each node pointer, so that can be prefetched by cache
                                1. this is clever
                                2. it allows overlap of two time-comusing operations, namely
                                   loading the node data, and branch misprediction due to node type
                        4. Synchronization
                            1. ROWEX - Read-Optimized Write EXclusion
                               i.e. read needs no lock, write locks
                            2. for tree structure changes, need to lock all descendants
                                1. change nodes by COW operation
                                2. obsolete nodes are reclaimed later by "epoch-based memory reclaimation"
                                    1. Epoch-based memory reclaimation
                                       https://aturon.github.io/blog/2015/08/27/epoch/#epoch-based-reclamation
                                       http://www.yebangyu.org/blog/2016/09/09/epochbasedreclamation/
                                           1. Exactly what we see in FASTER paper
                n. related materials
                    1. http://xszhao.science/blog/Paper-Review-HOT-A-Height-Optimized-Trie-Index-for-Main-MemoryDatabase-Systems/

    2. Direct Universal Access: Making Data Center Resources Available to FPGA  [2019, 1 refs]
       https://www.microsoft.com/en-us/research/uploads/prod/2018/10/nsdi19spring-final64.pdf
        1. looks like not production used. though MS is pioneering datacenter-level FPGA with Catapult
           DUA is an overlay network atop datacenter fabric
        2. highlights
            1. challenges for FPGA as datacenter resources
                1. differnet communication stacks. networking, GPU/FPGA direct, DMA
                2. server-centric local access, lack of global naming for FPGA resources
                    1. questions
                        1. why not just let servers to proxy FPGAs and provide virtual naming?
                3. current FPGA does not deal well with resource multiplexing
        n. related materials
            1. [Paper Review]NSDI'19 DUA
               https://zhuanlan.zhihu.com/p/61009436

    3. Understanding Lifecycle Management Complexity of Datacenter Topologies    [2019, 0 refs]
       https://www.usenix.org/conference/nsdi19/presentation/zhang
        1. intersting. pioneering work to manage datacenter topology complexity
           this is the NSDI'19 best paper
        2. highlights
            1. complexity metrics
                1. deployment: number of switches, patch panels, bundle types, 
                2. expansion: number of expansion steps, rewired links
                3. number of intra-rack connections vs inter-rack connections
            2. existing arts: Clos, Jellyfish, Xpander
            3. FatClique
                1. sub-block, block,
                   fat-edge connectivity

    4. Cuckoo Filter: Practically Better Than Bloom    [2014, 218 refs]
       https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf
        1. good paper. The Cuckoo hashing design is very clever. But it comes with a few potential drawbacks
        2. highlights
            1. Cuckoo filter has 2 hash functions, try to place at any of their slots
               if both cannot place, then kick an element to let it place
                1. need a limit for kicking
            2. to expand capacity, Cuckoo filter can 1) larger hashtable, 2) use one more hash function
            3. compared to bloomfilter, Cuckoo filter derives from Cucko hashtable. it stores the fingerprints in slot rather than the original key-value
               overall Cuckoo filter improves space efficiency as much to 80% with 3 hash functions
                1. question
                    1. sounds like Cuckoo filter has more false positive rate than bloom filter
                       because it uses only 1 bit for where to place the element
                           "the minimum fingerprint size used
                            in the cuckoo filter grows logarithmically with the number
                            of entries in the table"
            4. the problem / limitations
                1. inserting duplicated elements can easily cause loop kicking
                   if we want Cuckoo filter to support deletion, we must disallow an element to be inserted with (kb+1) times
                    1. this should still be OK for a hashtable interface
        n. related materials
            1. BloomFilter 与 CuckooFilter
               https://www.cnblogs.com/chenny7/p/4074250.html
            2. 布隆过滤器过时了，未来属于布谷鸟过滤器？
               https://zhuanlan.zhihu.com/p/68418134
```
