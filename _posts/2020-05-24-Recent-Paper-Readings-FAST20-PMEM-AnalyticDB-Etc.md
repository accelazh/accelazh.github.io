---
layout: post
title: "Recent Paper Readings FAST20 PMEM AnalyticsDB Etc"
tagline : "Recent Paper Readings FAST20 PMEM AnalyticsDB Etc"
description: "Recent Paper Readings FAST20 PMEM AnalyticsDB Etc"
category: "storage"
tags: [storage, paper, FAST]
---
{% include JB/setup %}

Recent paper readings. Search "very good", "good", "interesting", "useful" for my recommendations. Search "question" for my reviews.

```
1. Design of Global Data Deduplication for A Scale-out Distributed Storage System    [2018, 2 refs]
   https://ceph.com/wp-content/uploads/2018/07/ICDCS_2018_mwoh.pdf
    1. very good. global dedup implemented on Ceph. pioneer work dedup in scale-out cloud storage
    2. highlights
        1. key problems identified
            1. fingerprint index can be large
                1. suppose 100 PB storage, 64KB chunk size, 32B fingerprint => 50TB memory size required
                   even distributed memory store is very expensive
                    1. solution: double-hashing
                2. performance degradation
                    1. inline deduplication, no space rewrite amplification. latency increase.
                        1. throughput drop from 600MB/sec to ~350MBM/sec
                    2. post-preprocessing deduplication. interfere with customer workload
                        1. throughput drop from 600MB/sec to ~200MB/sec
                    3. solution. post-preprocessing with selective deduplication and rate control
        2. solutions
            1. double-hashing: i.e. hash(object content) as key to store object in Ceph.
                1. related to content-based addressing dedup, w.r.t. XtremIO
                2. question: I remeber Ceph strip file by fixed size as objects
                             so variable-length chunking dedup is not supported?
                    1. no. chunking algorithm can be changed to use content-based variable-length hashing to strip files
                3. how to read object content by customer object id?
                    1. chunk pool: object chunks, deduplicated
                    2. metadata pool: customer object id => map to object chunks
            2. reference counting
                1. track reference count in chunk object. update per each chunk update.
                   claim space when updated to zero reference. so no GC involved
            3. chunk caching
                1. Ceph can configure caching across storage pools.
                   This is handy here to cache data chunk to metadata pool
                2. using Ceph's HitSet
                   https://www.cnblogs.com/zhongguiyao/p/7941390.html
            4. deduplication rate control
                1. IOPS high/low watermark. Issue a dedup IO per e.g. 500 foreground IO
            5. transaction consistency
                1. dirty data chunk is first cached in metadata pool, ack to user
                   so whatever error happens later, post-processing deduplication can eventual consistency them
            6. chunking algorithm
                1. the paper is using a static fixed-size chunking algorithm for simplicity
        3. Evaluation
            1. it's using SSD disks, which means less impacted by the randomn read pattern introduced by dedup
               also, it's reasonable because it's SSD to be precious enough to employ dedup
            2. the replication factor is 2x, rather than commonly 3x
            3. latency
                1. random write: latency is basically the same with cache mode. ~20% non-cached. CPU usage doubled
                2. random read: with cache mode, similar. non-cache hit, more than doubled, due to redirection
            4. throughput
                1. sequential read: expect drop to 0.5x in 32KB in read.
                2. sequaltial write: drop to 0.7x in write (rate limiting at high watermark).
                    1. this is only measuring inference, not measuring dedup throughput itself.
            5. space saving
                1. this part is static if all data is crawed
                2. data recovery time is reduced due to dedup cuts down data size
    n. related materials
        1. Improving small file performance in object-based storage    [2006, 38 refs]
           https://www.pdl.cmu.edu/PDL-FTP/Storage/CMU-PDL-06-104.pdf
            1. server-driven metadata prefetching: batch multiple object metadata in one request
               namespace flattening: pack file path in to object ID

2. File Systems Unfit as Distributed Storage Backends: Lessons from 10 Years of Ceph Evolution    [2019, 1 refs]
   https://www.pdl.cmu.edu/PDL-FTP/Storage/ceph-exp-sosp19.pdf
    1. Answering why Ceph builds BlueStore. pioneer work to build custom FS for cloud storage. good.
    2. highligths
        1. emerging storage hardwares
            1. HDD - Shingled Magnetic Recording (SMR) - zone interface
            2. SSD - Zoned Namespace (ZNS) SSDs - remove FTL tail causing tail latency
            3. Ceph is also evaluating SeaStar framework for CPU vs NVMe SSD
        2. key gaps from existing FS
            1. efficient transactions
            2. fast metadata operations
            3. handle large directories, many small files
            4. support for novel, backward-incompatible storage hardware
        3. the solution
            1. metadata => RocksDB => BlueFS => Raw disk
                                      data   => Raw disk
            2. RocksBD for transactions.
            3. Pack small writes into RocksDB for one write
            4. BlueFS is kept simple. work in userspace, access disk by direct IO, no page cache
                1. caching: 2Q algorithm. and share requests to different cores
                2. copy-on-write support helps EC overwrite 2PC commit rollback needs
            5. saving into RocksDB: pack data structures
                1. compiler does this automatically for applications
                   but Ceph needs to do this explicitly for saving into RocksDB
                2. main techniques are delta and variable-integer encoding
        4. evaluation
            1. BlueStore is of 2x throughput, and reduced tail latencies from FileStore
            2. problems with RocksDB with ceph
                1. RocksDB's compaction and high write amplification impacts NVMe SSD in OSDs
                2. RocksDB is a blockbox, data serialized into and copied out of consumes CPU time
                3. RocksDB has own threading model, limits to do custom sharding
    n. related materials
        1. Lessons from 10 Years of Ceph Evolution
           https://zhuanlan.zhihu.com/p/90764255
    
3. Yahoo's Omid distributed database solution
    1. Lock-free Transactional Support for Distributed Data Stores    [2014, 23 refs]
       https://www.sigops.org/s/conferences/sosp/2011/posters/summaries/sosp11-final12.pdf
        1. Yahoo's transaction solution on HBase(-like).
           Compared to Percolator, Omid-2014 chose a centralized schema.
           Not as scale out, but faster. Features lock-free and TX metadata forwarding
        2. highlights
            1. challenge: TX metadata size bigger than centra TX status oracle (SO)
                1. technique: metadata truncation
                2. "lightly replication" to piggyback read-only TX metadata to client
                   client piece together (Snapshot Isolation (SI)) which version to read without contact SO
                    1. Omid 3 paper says this is "consumes high bandwidth and does not scale"

    2. Omid, Reloaded: Scalable and Highly-Available Transaction Processing    [2017, 6 refs]
       https://www.usenix.org/system/files/conference/fast17/fast17-shacham.pdf
        1. centra transaction manager (TM) & timestamp oracle. TM does primary and backup.
           TX metadata embedded in Hbase row, utilizing atomic row operations.
           TM never locks data record, compared to Percolator, but TM internally locks transaction (algorithm 2)
        2. highlights
            1. interesting optimizations
                1. forwarding TM transaction commit timestamp to per data record row metadata, i.e. commit field (CF)
                    1. this is like Omit 1's TX metadata forwarding to client
                2. TM separates key space into buckets. lock per bucket instead of entire TM
            2. TM primary and backup
                1. TM backup may falsefully think primary is dead. OK ..
                   this is history after paxos. but cheaper solution than need a paxos quorum of machines
                2. commit table is persistent in HBase 
        n. related materials
            1. Tephra: Transaction for Apache HBase
               https://tephra.io

    3. Taking Omid to the Clouds: Fast, Scalable Transactions for Real-Time Cloud Analytics    [2018, 0 refs]
        1. Still Omid 2, centralized TM. Performance improvement. Support secondary index (not included in paper)
           The direction is to become SQL compliant, i.e. the "Cloud" / "Analytics" (but paper didn't mention SQL)
        2. highlights
            1. Omid Low Latency (LL)
                1. commit table is highly contended, shard it
                2. forward commit table to per row transaction metadata (commit field, i.e. CF)
                    1. OK .. isn't Omid 2 paper already did this?
            2. Omid Fast-Path (FP)
                1. allow reader to force the writing transaction to abort, like Percolator / CockroachDB
                2. new APIs - Begin-Read-Commit, Begin-Write-Commit, etc
                    1. this saves bein/commit round trips with TM for short transactions

4. Singularity: Rethinking the Software Stack    [2007, 340 refs]
   https://courses.cs.washington.edu/courses/cse551/15sp/papers/singularity-osr07.pdf
    1. Microsoft Research. OS rethinking redesign
    2. highlights
        1. Software-Isolated Process (SIP)
            1. Do not share data with other processes, only by passing through "Channels"
            2. only programming languages of type and memory safe
            3. access kernel by Application Binary Interface (ABI). no complex UNIX's ioctl or Windows' CreateFile
            4. SIP has memory Garbage Collection
        2. Contract-Based Channels
        3. Manifest-Based Program (MBP)
            1. MBP describes program required system resources, its desired capabilities, and its dependencies
            2. runtime verification by OS
        4. Singularity kernel
            1. over 90% of the is written in Sing#
            2. programmable I/O processors to become first-class entities to OS scheduling and compute abstractions

5. The Pauseless GC Algorithm   [2005, 132 refs]
   https://www.usenix.org/legacy/events/vee05/full_papers/p46-click.pdf
    1. ZGC origin. Auzl Systems' pauseless GC is backed by embeded hardare, e.g. CPU supports read barrier.
       No need for write barrier. Read barrier has cost, to found missed mark and to update relocated pointers.
       Mark / last Remap, relocate, Remap / next Mark, all can gradually run, no rush no stop the world
       interesting paper .. there are many details ... something we can forcast for ZGC
        1) the "trap storm" issue 2) the future generational GC 3) read barrier does have cost
    2. highlights
        1. the read barrier is backed by CPU hardware (custom hardware). not like ZGC by software
        2. "Our read-barrier is used for Baker-style relocation [5][23], where the loaded value is corrected before the mutator is allowed to use it.
           We focus collection efforts on regions which are known to be mostly dead, similar to Garbage-First [14].
           Our mark phase uses an incremental update style instead of Snapshot-At-The-Beginning (SATB) style [30].
            SATB requires a modestly expensive write-barrier which first does a read (and generally a series of dependent tests).
           The Pauseless collector does not require a write barrier."
        3. Steal 1 Not-Marked-Through (NMT) bit from 64-bit address, to indicate whether read barrier to trap
            1. also each object has two mark bits, to indicaite marking state
        4. new objects created during marking, will be allocated to a separated place, hence not interleve with the relocate
        5. Stop-the-World (STW) and SATB invariant
            1. A mutator can read an unmarked ref into a register, then clear it from memory
               The object remains live (because its ref is in a register) but not visible to the marking threads
            2. This is typically solved by STW or SATB
            3. this paper solution: using NMT-bit, need read-barrier overhead
                1. "The invariant is that refs with a correct NMT have definitely been communicated to the Marking threads (even if they haven't yet been marked through).
                   Refs with incorrect NMT bits may have been marked through, but the mutator has no way to tell."
                2. "If a mutator thread loads and read-barriers a ref with the NMT bit set wrong, it has found a potentially unvisited ref."
                3. "The marking threads need to close the narrow race where a mutator may have loaded an unmarked ref (hence has the wrong NMT bit) but not yet executed the read-barrier.
                    Read-barriers never span a GC safepoint, so it suffices to require the mutators cross a GC safepoint without trapping."
                   "When all mutators complete the Checkpoint with none of them reporting any new refs, the Mark phase is complete."
                    1. Stop-the-World has its usage - GC safepoints, JVM yields to OS, STW can take place here. It's faster than patch-and-roll-forward schemes
                    2. what is a Checkpoint? "In a Checkpoint each mutator reaches a GC safepoint"
                       "In a STW pause, all mutators must reach a GC safepoint before any of them can proceeds"
                    3. "ZGC doesn't get rid of stop-the-world pauses completely. The collector needs pauses when starting marking, ending marking and starting relocation."
                        0. this maps to this paper's "Checkpoint"
                        1. ZGC "Another pause is required when ending the marking phase. In this pause the GC needs to empty and traverse all thread-local marking buffers"
                        2. ZGC "Root-set" pause .. Paper "The mutators scrub any existing stale refs from their root-set with a Checkpoint"
            6. Remap and the next GC's Mark phase are batched together
                1. as the both can be put in read barriers, overhead from the mutator
                2. after Remap down, side array is drained, all stale objects copied to relocated place
        7. Relocate phase
            1. moved objects are tracked by "side array", a hash table
            2. if the object is not yet moved, mutator calling read barrier needs to copy instead of GC.
               it can cause a short pause, related to live object ratio in page size
               i.e. "Each page in this set is protected from mutator access"
        8. "trap storm", "self-healing"
            1. "There are brief "trap storms" at some phase shifts, but due to the "self-healing" property of the algorithm these storms appear to be low cost"
                1. E.g. "each mutator flips its own working set as it runs. After a short period of high-intensity trapping (a "trap storm")
                         the working set is converted and the mutator proceeds at its normal pace
        9. future work: "Another obvious and desirable feature is a generational variation of Pauseless.
            As presented, Pauseless is a single-generation algorithm"
        10. evaluation - how to measure GC impact to JVM?
            1. transaction timespan and GC pause counts
            2. reported pause times can be highly misleading, 2x/6x/30%/100% under-reported
            3. Minimum Mutator Utilization figures to measure "trap storm"
                1. OK .. the number looks bad. MMU@50ms has ~40ms pause, 20ms accounted by STW, 20ms accounted by "trap storm"
    n. related materials
        1. A FIRST LOOK INTO ZGC - DOMINIK INFÜHR
           http://dinfuehr.github.io/blog/a-first-look-into-zgc/
        2. ZGC 原理是什么，它为什么能做到低延时？
           https://www.zhihu.com/question/287945354/answer/458761494

6. What does it mean to understand a neural network?    [2019, 5 refs]
   https://arxiv.org/pdf/1907.06374.pdf
    1. Knowing the learning rules, architectures, and loss functions; instead of inspecting the tons of parameters.
       Essentially this is to compress a neru network. Is human brain compressiable however?
       "Instead of asking how the brain works we should, arguably, ask how it learns to work"
    2. OK .. what is this paper's conclusion ..

7. AnalyticDB: Real-time OLAP Database System at Alibaba Cloud    [2019, 1 refs]
   http://www.vldb.org/pvldb/vol12/p2059-zhan.pdf
    1. very good paper. comprehensive and detailed to reveal how an OLAP DB is built.
       shared storage + statelss node like AWS Aurora Multi-Master; and 1 writer + n reader like MySQL (partitioned).
       hybrid row-column data layout. Baseline + Incremental's Lambda Architecture.
       Bitmap(-like) Index + Sorted Index. Off write path build & merge by Fuxi
    
    2. highlights
        1. Table partitioning
            1. seconary partition divides by time interval. old enough partitions are deleted.
                1. this sounds trace back to typical "分库分表"
            2. primary partition by primary key (e.g. id).
               partition to server assignment are by hash
                1. clever co-location reduces Join's cross node traffic
               partition is assigned to reader node
        
        2. Underlying framework architecture
            1. Fuxi: utilizing CPU/Memory on nodes for task execution
            2. Pangu: HDFS, shared data storage for writer and reader nodes. 
                      Fuxi runs MapReduce to convert Writer's log commits into Reader's data files
                        1. (should be) To merge the Baseline data and Incremental data of Lambda Architecture 
            3. Execution Engine
                DAG Scheduler in Coordinator
                Column-oriented vectorized
                Runtime code generation (CodeGen)
                Directly run on serialized binary data rather than Java objects
            4. Coordinator built on Zookeeper: critical path on read/write. metadata management
        
        3. write node vs read node separation
            1. write node => Pangu => read node's inital partitions
               but for faster propagation, read node pull updates directly from write node
                1. read node can also directly read from Pangu, if failed to contact write node, though higher latency
            2. read node are replicated, for scalability and reliability. a query can be resend if one reader node fails
               a partition has only one writer node, if writer node is dead, partition reassign
            3. reader node provide to customer: realtime reads and bounded-staleness reads
               But .. bounded-staleness is by default .. Oh .. ACID vs performance. OK for OLAP
                1. realtime read then introduces an extra data synchronization issue
                    1. Coordinator acts as central to pass versions. not like today's commonly client message piggyback
                    2. read node needs to pull updates if version too old to satisfy read. write nodes can also pushes updates
        
        4. Storage
            1. hybrid row-column storage layout
                1. why need row layout? OLAP favors column-oriented, but point-lookup still needs row layout
                2. rows are cut into row groups (default 30K rows). inside row group, data are stored in column-oriented style.
                   so small ranges of scan is column-oriented. row lookup only needs data within the same row group.
                    1. all values from the same column are called as a data block.
                       "data block" is the basic operation unit for fetch and cache
                3. Metadata is stored in a separated file from Detail File. (rather than typically in header area)
                    1. Metadata file stores statistics required by Query Optimizer. e.g. aggregates, cardinality
                    2. a dictionary automatically enabled for low cardinality column for space saving
            2. Complext data types JSON, vectors
                1. A row group is cut into smaller groups, each maps to an FBlock. FBlock is stored in a separated file.
                   the original column data stores a FBlock Block Entry, holding the start row and end row of the FBlock
            3. Data update
                1. Lambda architecture: separate Baseline Data and Incremental Data
                    1. Baseline Data: fully indexed, row-column data
                       Incremental Data: only simple sorted index.
                                         occurs only on read nodes when pulled and replayed logs from write nodes
                    2. delete marked by bit. copy-on-write for MVCC. version tracked
                    3. query pays double path for Baseline data and Incremental data
                2. to merge Baseline data and Incremental data
                    1. make current Incremental data immutable and create a new Incremental data to handle new arrivals
                    2. new Index is created for the merged version
                    3. (not explicit in paper, but should be) Fuxi runs MapReduce job to do the merge, files are stored on Pangu
                       (as you can compare with what 3.4.1 says)
            
            3. Index Engine
                1. What index to use?
                    1. B+ tree is to expensive to use. The Index is a inverted index by value => row id list look up.
                        0. just look like the typical bitmap index
                            1. to same index space, AnalyticsDB automatically select between bitmap index vs integer array
                            2. this should also explains why the Index Space & Build Time diff vs Greenplum (Table 1)
                                1. another Build Time diff is due to Analytics offline build, while GP in-write-path build index
                                2. Table 1 shows AnalyticsDB impact much less data insertion time
                        1. queries can be decomposed into union / intersect of filtering row ids
                        2. index path selection is by selectivity, from small to big
                        3. use k-way merge to save memory
                        4. use PForDelta algorithm to compress the row ids
                        5. each column is built with an inverted index, which is stored in a separated file
                    2. how to index JSON object?
                        1. flatten JSON object, each XML path is a key column to be indexed
                        2. pack all indexes of one object in single file in case a JSON object can have throusands of keys
                    3. how to index full-text?
                        1. still use the same inverted index, but extend with TF/IDF simularity
                    4. Vector Data
                        1. good. typical usecase is to store high dimensional feature vectors from machine learning
                        2. typical usecase of query is to nearest neighbour search (NNS)
                           using algorithms Product Quantization (PQ) or Proximity Graph (k-NNG)
                            1. PQ and k-NNG needs to build indexes.
                            2. PG has smaller index size, while k-NNG holds better search performance and accuracy
                2. When and how to build index
                    1. off the write path. When merge Baseline data and Incremental data on Pangu
                       new index is merged with full index
                    2. building and merging indexes are run by many Fuxi MapReudce tasks
                       the tasks automatically choose off-peak periods
                        1, the sorted index is stored at header of each data block, ~60KB
                    3. not like GreenPlum which builds index in write path, for Incremental data
                       Analytics have to use a temporary index - Sorted Index
                        1. Sorted Index - list of row ids corresponding to sorted data order
                        2. When to build - build independently on reader nodes
                            1. OK .. reader nodes replicas need to build multiple times, redundant work
                3. Index caching
                    1. using both index-page cache and query-condition cache
                    2. observation: large costly query change less, which hits query-condition cache
                                    small queries change dramatically, but OK to recompute

            n. my understanding
                1. so it's not using an append-only manner, nor LSM-tree stuff.
                   But Baseline Data + Incremental Data is essentially it.
                2. the underlying Pangu system manages the persistence, replication.
                   and Fuxi runs merge jobs by MapReduce.
                3. though OLAP, and default eventual consistency (bounded-staleness read)
                   but AnalyticsDB does support update existing data
                4. index took as much as 1x of original data size, and needs incremental build + merge
                   which means it can be another source and write amplification + CPU consumption
                5. index basically uses bitmap-like index, this should be due to column-oriented store.
                   e.g. if SQL is querying different columns, individual columns can be queried,
                     and eventually only needs to union/intersect row id sets.
                
        4. Query optimizer
            1. use STARs (STrategy Alternative Rules) to abstract capabilities of heterogenous data sources
            2. Join Push-down: using hash key to assign partition to server, related primary keys are assigned to same partition server
                               this helps data co-locating when joining
            3. some examples of pushdown: 1) aggregations like count can be returned directly from indexes
                                          2) filtering can be evaluated solely on indexes
            4. cost-based optimization relies on cardinality estimation that relies on realtime sampling statistics
                1. AnalyticsDB has an underlying framework.
                   It stores and caches and indexes sampling data in underlying storage.
                   It provides framework API for optimizer to call
                2. for business critical scenarios, custom optimizations are applied. E.g.
                     caching sampled results. optimized sampled algorithms, improved derived cardinalty
            5. the SQL operators are passing lists of row ids.
                   this is where SIMD & vectorization can take place. also it leverages the Sorted Index

        5. Evaluation
            1. The true opponent is GreenPlum, who has index on each column
            2. The query Q1 Q2 Q3 selected are clever, specially to attack GP's weakpoint.
                1. Q1: ORDER BY + LIMIT 10 can be accelerated by AnalyticsDB's Sorted Index (I guess)
                2. Q2: 1) AnalyticsDB filters by each column in parallel, while GP does it one by one
                       2) AnalyticsDB can do query-condition caching
                3. Q3: AnalyticsDB translates join to sub-queries and leverages indexes. GP uses hash john and hashmap

    4. questions
        1. question: From Figure 1, Writer & Read path needs go through Coordinator? this involves an extra data pass hop
            1. OK, Figure 5 and 3.4.2 confirmed that. why Coordinator as a central bottleneck, while everybody today are shifting to pass-through?
        2. question: Separate Write path & Read path?
            1. Does HDD / SSD becomes more performant when only processing reads or writes? Interesting
                1. Both Write path nodes and Read path node don't handle data persistence. So only to separate CPU read/write workload?
            2. Data immediately written, in the cache of Write node, won't be immediately readable leveraging the cache
               User needs to wait for a delay for data to be propagated to Read node, and needs eventual consistency / strict versioning?
                1. reader node directly pulls update from writer node. Pangu only provides the inital data for reader node
                2. also, reader node provide to customer: realtime reads and bounded-staleness reads. separationbounded-staleness by default
                    1. OK .. this is the burden introduced by write node / read node. Even it needs only 1 read node,
                       the customer needs to suffer from the synchronization latency. Or accept eventual consistency
                    2. but OK for OLAP. This is not OLTP.
                3. for writer to correctly process SQL updates, doesn't it needs the updated data too?
                   That's also what reader nodes is doing. So why the separation ..
            3. Read vs Write resource contention?
                1. Well .. isn't write-write and read-read content more, cuz they are of the same type so asking for same type of resources?
            4. a possible advantage is to individually scale out write nodes and read nodes.
               rather than, the 1 partition can only be served by 1 server, even the server is overloaded by reads
               compared to storage, the read node here carries query execution role, it's not easy to directly pass through the load to underlying storage
                1. a resemble can be "Readonly Partiiton", or "Learner" in paxos
                2. AWS Aurora Multi-master somehow allows multiple writer node. These writer nodes scales out read traffic too.
                   but it's still easier to just let 1 write node + n read node - a successful MySQL paradigm
                    3. so the real reason AnalyticsDB adopts read/write decoupling is to:
                       allow scale out a partition's read load, but without introducing the complexity of multi- write node (multi-master)
        
        3. assume it's the 1 writer + n reader mode. about the write throughput w.r.t AWS Aurora Multi-master
            1. writes are partitioned, so overall throughput is not limited
            2. if the hotspot is within a single partition, and cannot bi mitigated by spliting partition.
               Mult-master, i.e. multi-write node, should be an advantage here
            3. here to see usecase scenarios of AWS Aurora Multi-master
               https://aws.amazon.com/blogs/database/building-highly-available-mysql-applications-using-amazon-aurora-mmsr/
                1. "Aurora Multi-Master improves upon the high availability of the single-master version of Amazon Aurora
                    because all of the nodes in the cluster are read/write nodes.

                    With single-master Aurora, a failure of the single writer node requires the promotion of a read replica to be the new writer.
                    In the case of Aurora Multi-Master, the failure of a writer node merely requires the application using the writer
                    to open connections to another writer."
                2. Conflict management
                    1. writer writes to a quorum of storage nodes.
                       storage nodes determine whether to accept by comparing whether writer provided LSN is the most updated
                       multiple writers compete in a paxos way, a writer proposes and needs to win a quorum of wins to continue its transaction
                    2. conflict by page level. two different rows in the same page can conflict
                3. Global read-after-write consistency
                   "Reads that happen on other nodes immediately after a write may not
                       see the write change for a few milliseconds, depending on replication lag"
                    1. so it has the same issue with AnalyticsDB's writer node => reader node replication
                4. AWS Aurora Multi-master should be targeting OLTP. The official site compares it with MySQL
                   https://aws.amazon.com/rds/aurora/
                    1. so, AnalyticsDB is not in the same class. It's OLAP.
                    2. roughly the materials implies AWS Aurora Multi-master is row-oriented, while AnalyticsDB is column-oriented
                       https://www.slideshare.net/AmazonWebServices/which-database-is-right-for-my-workload
                       https://www.zhihu.com/question/279262046
                       https://blog.acolyer.org/2019/03/27/amazon-aurora-on-avoiding-distributed-consensus-for-i-os-commits-and-membership-changes/
        
        4. the paper didn't talk much about transaction ..
            1. maybe OLAP is complex read + ingestion i.e. simple writes. So transaction is not important?
               but the paper does says AnalyticsDB supports data updates
        5. about index management
            1. "4.2.1" Index Filtering. How does this bitmap-like index to support range queries?
            2. also, why not introduce more types of index and for user selection?
            3. also, how is ORDER BY + Limit 10 made faster by index?
                1. OK .. possibly the Sorted Index.
                   The implications are AnalyticsDB doesn't drop Sorted Index after Incremental data becomes Baseline data.
                   Anyway, Sorted Index is very small.
            4. if index are build off the write path async, how does the stale index lookup the correct data which is already changed?
                1. e.g. a range query where a value is already changed, but index doesn't know?
                   maybe the bitmap-like index used by AnalyticsDB here is easier to handle such situation?

        6. the SQL operators are passing lists of row ids.
                   this is where SIMD & vectorization can take place. also it leverages the Sorted Index
        7. query optimizer didn't mention which type of search is used
           cascades? simulated annealing? genetic? rule-based heuristics? DSL (cockroachDB)?

    n. relate materials
        1. Pangu [7]: https://www.alibabacloud.com/blog/pangu%E2%80%94the-highperformance-distributed-file-system-by-alibaba-cloud_594059
            1. Alibaba's HDFS改, So you can see where is the direction for future storage systems
            2. highlights
                1. Pangu 2.0 goals
                    1. for the next-generation network and storage software and hardware
                        1. from HDD to SATA SSD and NVMe SSD
                        2. Optane memory
                        3. networking: from GE and 10GE to 25GE, 40GE, 50GE, or even 100GE.
                                       A hop takes as short as five µs
                        4. RDMA
                        5. replace the device-based SSD with the host-based SSD
                    2. Distributed Metadata Management
                    3. Optimized Cost: Adopts the hierarchy, erasure coding (EC), compression, and deduplication
                        1. Multi-Medium Large Storage Pool, SSD and HDD
                    4. Elasticity: more scale, more business variety

        2. Fuxi [38]: Fuxi: a fault-tolerant resource management and job scheduling system at internet scale    [2014, 88 refs]
           http://www.vldb.org/pvldb/vol7/p1393-zhang.pdf
            1. Alibaba's Yarn改. referenced by Google Borg. Related Mesos [11], Yarn [18] and Omega [16]
            2. highlights
                1. challenges against scheduling
                    1. supporting resource allocation over multiple dimensions
                    2. fairness and quota constraints across competing applications
                    3. scheduling tasks close to data
                    4. fully-decentralized solution is hard on synchronization of global state. single master limits scale
                        1. Mesos adopts a multi-level resource offering framework
                        2. Yarn's architecture decouples resource management and programming paradigms (MapReduce)
                    5. states are exchanged periods long and short, and super lage cluster scale
                    6. how to cope with master failure
                    7. allow application to increase resource demand after initially specified
                2. fault tolerance
                    1. FuxiMaster is a central master, schedule by a locality tree based method, micro-seconds level response
                       hot-standby failover
                        1. master-standby mutually excluded by Apsara lock service (Zookeeper?)
                    2. FuxiMaster hot-standy failover, soft states vs hard states to reduce state recording overhead
                        1. application master monitored by FuxiMaster, application worker monitored by application master
                        2. faulty nodes are detected and blacklisted. detection cowork between FuxiMaster and Application master
                3. misc (diffs with Yarn)
                    1. separation of task and container
                    2. locality tree
                    3. quota, priority, multi-level prioritization
                        1. timely response event, slower compact and batch, more slower fixed time interval
                    4. two-level scheduling-like: FuxiMaster + AppMaster/JobMaster-TaskMaster (DAG)

        3. VLDB2019 | AnalyticDB: 阿里云实时分析服务 - Eric Fu
           https://zhuanlan.zhihu.com/p/85678930

        4. AnalyticDB: Real-time OLAP Database System at Alibaba Cloud - 吕信
           https://www.jianshu.com/p/ce05e29c4766

        5. VLDB 2019 笔记: AnalyticDB: Real-time OLAP Database System at Alibaba Cloud - haitaoyao
           https://www.jianshu.com/p/342a059af224
            n. related materials
                1. The Snowflake Elastic Data Warehouse    [2016, 45 refs]
                   http://pages.cs.wisc.edu/~remzi/Classes/739/Spring2004/Papers/p215-dageville-snowflake.pdf
                    1. already covered before

        6. Query Optimizer: Selectivity, Cardinalty, Cost
           https://docs.oracle.com/database/121/TGSQL/tgsql_optcncpt.htm#TGSQL213

        7. At what point does a database update its indexes in a transaction?
           https://dba.stackexchange.com/questions/165899/at-what-point-does-a-database-update-its-indexes-in-a-transaction
            1. SQL Server and Oracle: data and indexes will be updated at the same time

8. How to Architect a Query Compiler, Revisited    [2018, 29 refs]
   https://www.cs.purdue.edu/homes/rompf/papers/tahboub-sigmod18.pdf
    1. compared to Hyper or DBLAB, the paper doesn't need low-level coding nor multiple compiler passes.
       the project "LB2" uses single generation pass. "Futamura projections" links interpreters and compilers.
        i.e. "LB2" only needs to implement a query interpreter; partial evaluation / Futamura project will translate it to be a compiler
       good paper. I think it's going to be a milestone of Query Compiler field
    2. highlights
        1. "HyPer [33] uses the programmatic LLVM API and achieves excellent performance,
            at the expense of a rather low-level implementation that permeates large parts of the engine code"
        2. "The fundamental insight of Futamura was that compilers are not fundamentally different from interpreters,
            and that compilation can be profitably understood as specialization of an interpreter,
            without explicit reference to a given hardware platform or code generation strategy"
            1. e.g. "partial evaluation [22]". Figure 2bc shows the specialization process
            2. question: specialization looks like "prepared SQL statement"?

    n. related materials
        1. How to Architect a Query Compiler    [2016, 43 refs]
           https://infoscience.epfl.ch/record/218087/files/how-to-architect-a-query-compiler.pdf
            1. existing query complier are essential template expanders. they result to code explosion, and hard to express some low-level optimizations
               the paper proposes a new DSL stack, Data-Structure Aware Program, and abstract in middle to decouple the concerns
               the project is called "DBLAB"
            2. highlights
                1. ASL is not enough as the IR. See Figure 2 for the DSL *stack*.
                   because it needs multiple IR languages, the paper says "progressively lowering the level of abstraction"
                   using Scala to host these DSLs
                2. see Conclusion part, it also explains what the paper does, and clearer

        2. CMU SCS 15-721 ADVANCED DATABASE SYSTEMS
           https://15721.courses.cs.cmu.edu/spring2018/slides/03-compilation.pdf
           https://15721.courses.cs.cmu.edu/spring2020/slides/, https://15721.courses.cs.cmu.edu/spring2020/schedule.html
            1. very good. the slides are latest 2020 and in detail.
               The Schedule page covers major papers in recent in-memory DB / OLAP fields
               Note, year 2018/2019 have a few slides that 2020 is missing; need to cross walk
            2. highlights
                1. major fields
                    1. transaction, MVCC, MVCC GC,
                       OLTP indexes, OLAP indexes, In-memory DB indexes
                       Stoarge layer, data/index compression, NSM/DSM models
                       logging & recovery, checkpointing
                       networking, distributed partitioning/placement, process model / scheduling
                       query planning, query execution models, query compilation, vectorization
                       query optimiaztion, cost models, UDFs
                       hashjoin, sortmergejoin
                       larger than memory, new hardware, cloud
                    2. HYPER's RULES FOR PARALLELIZATION
                        Rule #1: No random writes to non-local memory
                            → Chunk the data, redistribute, and then each core sorts/works on local data.
                        Rule #2: Only perform sequential reads on non-local memory
                            → This allows the hardware prefetcher to hide remote access latency.
                        Rule #3: No core should ever wait for another
                            → Avoid fine-grained latching or sync barriers

            n. related materials
                1. Understanding How PostgreSQL Executes a Query
                   http://etutorials.org/SQL/Postgresql/Part+I+General+PostgreSQL+Use/Chapter+4.+Performance/Understanding+How+PostgreSQL+Executes+a+Query/
                    1. good. very useful
                    2. highlights
                        1. about PostgreSQL's execution plan sort seq scan
                            1. All you need to know about sorting in Postgres
                               https://madusudanan.com/blog/all-you-need-to-know-about-sorting-in-postgres/
                                1. PostgreSQL supports external sort
                    n. related materials
                        1. Is Your Postgres Query Starved for Memory?
                           http://patshaughnessy.net/2016/1/22/is-your-postgres-query-starved-for-memory
                            1. "Hybrid hash join", when hash join table bigger than work_mem
                
                2. How We Built a Vectorized Execution Engine - CockroachDB
                   https://www.cockroachlabs.com/blog/how-we-built-a-vectorized-execution-engine/
                   https://www.infoq.com/articles/columnar-databases-and-vectorization/
                    1. E.g. MonetDB-X100 (Vectorwise).
                       Vectorized execution is ususally equipped for OLAP, and can benefit from SIMD

                3. Cascades Optimizer
                   https://zhuanlan.zhihu.com/p/73545345
                    1. good, informative, if combined with CMU SCS 15-721
                       https://15721.courses.cs.cmu.edu/spring2020/slides/19-optimizer1.pdf
                    n. related materials
                        1. 深入了解 TiDB SQL 优化器
                           https://www.infoq.cn/article/cwuk2o*aW8ih9ygu5UeJ
                            1. "逻辑优化规则" => rule based?
                               Anyway, TiDB is OLTP, query optimizing is not as complex as OLAP
                        
                        2. SQL Query Optimization: Why Is It So Hard To Get Right?
                           http://db.lcs.mit.edu/6.830/lectures/lec10.pdf
                           https://www.youtube.com/watch?v=RQfJkNqmHB4
                            1. dynamic programming is frequently used in query optimization
                               either bottom up or top down, heuristics, pruning
                            2. selectivity (and correlated selectivity) is critical to choose best algorith
                               e.g. Nest Loops Join vs Sort Merge join vs Index Join
                            3. query plan space of 5 Tables joining
                                "Star" Join queries - 384 query plan candidates
                                "Chain" Join queries - 224 query plan candidates

9. D2-Tree : A Distributed Double-Layer Namespace Tree Partition Scheme for Metadata Management in Large-Scale Storage Systems    [2018, 2 refs]
   https://web.cs.ucla.edu/~tan/documents/icdcs18.pdf
    1. formulate sub-tree partitioning by math definitions and as an optimization problem. interesting new perspective.
       cut metadata tree as busy upper layer (global layer), replicated to each MDS, and the remaining lower layer (local layer).
    2. highlights
        1. Formula (7) to simplify locality formula for Locality Layer nodes. global layer has jump 0, local layer has jump 1
        2. See "Phiosophy". Dynamic Subtree partitioning, the self-organizing architecture, is treated as a more complicated solution

10. Strong and Efficient Consistency with Consistency-Aware Durability    [2020, 0 refs, FAST20 Best Paper]
    http://pages.cs.wisc.edu/~ag/cad.pdf, https://www.usenix.org/sites/default/files/conference/protected-files/fast20_slides_ganesan.pdf
    1. interesting paper. new way for strong consistency (monotonic reads) & higher performance,
       weakened durability, possible data loss. possible read stale version (unless overhead with Active Set)
       usecases: geo-distribution, edge-computing, video streaming, etc.
       project name "ORCA", built in ZooKeeper (which already tracks last-update index)
    2. highlights
        1. interesting view: replication sync vs async, persistence/durability sync vs async
        2. "Synchronous durability, while necessary, is not sufficient to prevent non-monotonic and stale reads"
            1. related: YugabyteDB: Low Latency Reads in Geo-Distributed SQL with Raft Leader Leases
               https://blog.yugabyte.com/low-latency-reads-in-geo-distributed-sql-with-raft-leader-leases/
        3. write ack after data in first node memory. replication async, persistence async.
           reads need to wait for replication done, persistence done
            1. using Update Index and Durability Index to do this
                1. question: Update Index and Durability Index themselves seem need strong consistency maintained across all nodes
                             they introduce another layer of overhead. How they are done? paper didn't mention much
            2. problem: a follower node may server stable read because it doesn't know latest update
                1. need introduce Active Set. more complexing ..
                    1. Only nodes in active set allows to server reads. Leader ensures durable in all nodes in Active Set
        4. "To the best of our knowledge,
            cross-client monotonic reads is provided only by linearizability [25, 38].
            However, linearizable systems require synchronous durability and most prevent reads at the followers.
            ORCA offers this property without synchronous durability
            while allowing reads at many nodes"
        5. questions
            1. why not a simpler solution?
               Just track versions, client asks follower versions before read.
               if stale, redirect to leader.
            2. talking about extra delays,
               reader still need to wait for data propagating to followers
               that's still delay comparable to redirect reads to leader ..?

11. A Study of SSD Reliability in Large Scale Enterprise Storage Deployments    [2020, 0 refs]
    https://www.usenix.org/conference/fast20/presentation/maneas
    1. study on 1.4M SSDs from NetApp. ARR related factors, "bathhub" not effective,
       consecutive replacements observed. large capacity drives failure, 3D-TLC failure.
    2. highlights
        1. Avg ARR (Anual Replacement Rate) is 0.22% << Goole's data center 1-2.5% [29], lower than HDD 2-9%, [26, 28]
           ARR can vary dramatically, 0.53% ~ 1.13%. 3D-TLC has higher ARR, MLC vs SLC are comparable.
           high capacity drives sees high ARR, and more serve failures.
            1. SSDs with a non-empty defect list have a higher chance of getting replaced
            2. firmware updates significantly reduce ARR
            3. large capacity drives require different type of failure predictors
        2. spare area (to map bad blocks) only consumed in average < 15%, Q99.9 is 33%, under utilized
        3. drives at Q99.9 consumes only 33% PE cycle limit, far under utilized
        4. 1/3 drive replacement reasons are "preventative" (category D)
        5. "bathhub" model is incorrect. paper observed long period of infant mortality,
           taking 20-40% life time in infrant mortality of the the 5-year lifespan.
           paper didn't observe an increase of ARR towards the end of life
            1. tradition burn-in period before deployment not as effective. need new solutions
        7. second drive replacement follows closely to the first. 46% within one day, 56% within one week
            1. single parity RAID is not as reliable

12. An Empirical Guide to the Behavior and Use of Scalable Persistent Memory    [2020, 6 refs]
    https://www.usenix.org/system/files/fast20-yang.pdf
    1. good paper. focus on Optane platform (the NVDIMM system) / 3D-XPoint (the storage media),
       focus on AppDirect Mode (NVDIMM for persistence) rather than Memory Mode (NVDIMM as far memory cached by DRAM)
       revealed many interesting characteristics and provided general suggestions.
    2. highlights
        1. XPLine is 256-bytes, due to Phase-Change memory page size.
           small writes subject to be translate to read-modify-write (256B),
           with XPBuffer (~16KB size) to coalesce writes
            1. Effective Write Ratio (EWR) is a good measurement
            2. small random writes are bad.
               small writes without locality are bad.
        2. multi-threading contention at XPBuffer, iMC (integrated Memory Controller),
           WPQ (write pending queue) head-of-line blocking
            1. too many threads accessing a single NVDIMM worsens the performans
               stripping / interleaving across mutilple Optance cards can be bad
                1. with interleave size 4KB, when write size is not n*4KB, it performs worse
                2. page buffer of 4KB pages performs worse, because it cannot access uniformly across DIMMs
        2. cache line flush / load uses extra DIMM bandwidth, and makes read/writes non-sequential
            1. flushing cache line after each 64KB store improves bandwidth for accesses larger than 64KB
               Because, compared to let cache line naturally evict, this makes the access (due to cache flush) more sequential
            2. more, for large writes, suggest to use `ntstore` instead of `store+clwb`
        4. general read/write characteristics
            1. sequential read (~170ns) is ~2x faster than random reads (~310ns). (DRAM ~80ns)
               sequential read is ~2x faster than writes (90ns).
            2. hotspot region within 128K can generate Q99.999 outlier at ~100x latency. DRAM won't.

13. Persistent Memeory Programming - Andy Rudoff - Login Summer17   [2017, 35 refs]
    https://www.usenix.org/system/files/login/articles/login_summer17_07_rudoff.pdf
    1. very good paper. 
    2. highlights
        1. compared to block-level MVM, NVDIMMs adds benefits of CPU cache coherency, direct memory access (DMA), cache line granularity access
           it enables Multiple TB per CPU socket (Optane Memory Mode). a new layer of persistence, capacity, cost
        2. Persistence Memory Programming Model
            1. SNIA TWG recommends OS uses standard file semantics
            2. mulitple NVDIMMs can be interleaved (stripped) for performance access, by memory controller
            3. DAX (Direct Access) - a persistent memory aware filesystem direct access PMem without using OS page cache
                1. Pmem can be mapped into memory using mmap() (MMU manages),
                   app performs load/stores with no Kernel involvement. no interrupts, no context switching, etc
            4. Persistence Domain (Optane ADR), writes inside which guarantees persistence
                1. currently not including the Cache, so still need `clflush` in x86 ISA
                   but some customized hardware may support putting Cache into Persistence Domain
            5. x86 ISA instructions related to PMem
                1. store + clflush: flush cache line, serialized
                2. store + clflushopt + sfense: flush cache line, non serialized
                3. store + clwb + sfense: cache line write back, don't invalid cache line
                4. ntstore + sfense: bypass cache, directly store to memory
                5. wbinvd: kernel mode only, invalid all cache line
            6. user space flush cache line to PMem - Optimized Flush
                1. Windows NTFS DAX supports it - clwb + sfense
                2. Linux EXT4 XFS suppot DAX, but not Optimized Flush
                   need to use DAX-device to mmap a PMem without file system
                3. libpmem provides function to tell whether Optimized Flush is supported
                   falling back to the standard method of flushing stores to mmap files otherwise
            7. programming libraries
                1. libpmem, libpmemobj; libpmemblk, libpmemlog; libmemkind
        3. Persistent Memory Challenges
                1. ACID - Anything larger than 8bytes are not guaranteed to persist atomically
                    1. this is exactly like Atomic disk sector write on disk
                2. Persistent heap to managing memory space. traditionally malloc

14. Repair Pipelining for Erasure-Coded Storage    [2017, 24 refs]
    https://www.usenix.org/sites/default/files/conference/protected-files/atc17_slides_li_0.pdf
    1. interesting paper. pipeline schema repair increase latency, but using pipeline will hide it.
       the scheme won't reduce traffic, but the congestion at the new parity being reconstructed.
       however, this is not a case for Ceph, which when node down, there are many reconstruct chains distributed cross the cluster

15. OpenEC: Toward Unified and Configurable Erasure Coding Management in Distributed Storage Systems    [2019, 4 refs]
    https://www.usenix.org/sites/default/files/conference/protected-files/fast19_slides_li.pdf
    1. Follow-up work from "Repair Pipelining for Erasure-Coded Storage".
       Using ECDAG to well represents the layered reconstruct pipeline, the language. OpenEC is the framework

16. AZ-Code: An Efficient Availability Zone Level Erasure Code to Provide High Fault Tolerance in Cloud Storage Systems    [2019, 2 refs]
    https://storageconference.us/2019/Research/AZ-Code.pdf, https://storageconference.us/2019/Research/AZ-Code.slides.pdf
    1. EC considering Availability Zone. Using MSR (regenerating code) for intra zone parities, using RS for cross zone global parities.
       "Hybrid Decoding with Global and Local Parities" is interesting
    2. highlights
        1. interesting analysis on different EC codec categories
            1. RS Code, LRC Code, MSR Code, GRID Code, AS-Code
        2. my questions
            1. however, AZ is subject to synced replication, the networking is fast, usually not a bottleneck
            2. per the example AZ-Code (k = 6, z=3, p=2, g = 3), the storage overhead is > 2, too high

17. Procella: Unifying serving and analytical data at YouTube    [2019, 0 refs]
    https://research.google/pubs/pub48388/
    the morning paper - Procella - https://blog.acolyer.org/2019/09/11/procella/ 
    1. Google already has Dremel, Mesa, Photon, F1, PowerDrill, and Spanner. Procella here to unify (it's a new DB, not proxy).
       Good, the query engine and the storage layout are really optimized in depth.
    2. highlights
        1. "an almost complete implementation of standard SQL, including complex multi-stage joins,
            analytic functions and set operations, with several useful extensions such as approximate aggregations,
            handling complex nested and repeated schemas, user-defined functions, and more"
        2. "segregating storage (in Colossus) from compute (on Borg)"
           "Procella employs multiple caches to mitigate this networking penalty"
        3. Artus - new columnar file format. Heavily optimise and pre-compute data formats
            1. Heavy use of custom encodings, instead of generic compression
            2. Multi-pass encoding, with a first fast pass to understand the shape of the data
            3. Artus uses a variety of methods to encode data: dictionary and indexer types, run-length, delta, etc.
                1. to achieve compression within 2x of strong general string compression (e.g. ZSTD)
                2. while still being able to directly operate on the data
                3. Each encoding has estimation methods for how small and fast it will be on the data supplied
                4. "... This allows us to aggressively push such computations down to the data format,
                    resulting in large performance gains in many common cases"
                5. Keeps rich metadata in file and column headers
                   (sort order, min and max, detailing encoding information, bloom filters, and so on),
                   making many pruning operations possible without the need to read the actual data in the column
        4. Query compilation & optimization - Superluminal
            1. LLAM is widely used, OK to OLAP. But Procella needs to serve both high TPS OLTP. It instead uses Superluminal
            2. Superluminal makes extensive use of C++ template metaprogramming and operates on the underlying data encodings natively.
               No intermediate representations are materialized.
            3. A rule-based optimiser applies standard logical rewrites. Then when the query is *running*,
               Procella gathers statistics based on sample of *actual data used in this query*, to determine what to do next
                1. Not like traditional cost-based optimizers. which collect and maintain statistics on data.
                2. Do not have to build complex estimation models, which likely useful only for limited subset of queries

18. Millions of Tiny Databases    [2020, 0 refs]
    https://www.usenix.org/conference/nsdi20/presentation/brooker
    the morning paper - https://blog.acolyer.org/2020/03/04/millions-of-tiny-databases/
    1. "In the same spirit as Paxos Made Live, this paper describes the details, choices and tradeoffs
        that are required to put a consensus system into production"

19. Distributed consensus revised    [2019, 2 refs]
    https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-935.pdf
    the morning paper - https://blog.acolyer.org/2019/05/07/distributed-consensus-revised-part-i/
                        https://blog.acolyer.org/2019/05/08/distributed-consensus-revised-part-ii/
                        https://blog.acolyer.org/2019/05/10/distributed-consensus-revised-part-iii/
    1. paxos variants. paoxs revised - is the algorithm still optimial?
    2. highlights
        1. known revisions to the classic Paxos algorithm
            1. Negative responses (NACKs)
            2. Bypassing phase two
            3. Termination - proposer return decided value without waiting majority of acceptors
            4. Distinguished proposer - widely utilised
            5. Phase ordering - need distinguished proposer, batch two phases in one
            6. Multi-Paxos - batch a sequence of values consensus in one run
            7. Roles - Merge proposers and acceptors roles. Introduce reader roles
            8. Epochs - compose (sid, pid, vid)
            9. Phase one "epochs by voting"
            10. Proposal copying - include last accepted proposals in NACKs
            11. Quorum generalisation - we only need any quorum intersets, we don't need > 1/2 nodes
        2. revised
            1. Classic Paxos requires all quorums to intersect, but
               "Our first finding is that it is only necessary for phase one quorums and phase two quorums to intersect.
                There is no need to require that phase one quorums intersect with each other
                nor that phase two quorums intersect with each other"
                2. related to "Flexible Paxos"
            2. Quorum-based value selection
            3. epoch allocation - Pre-allocation, Voting, Allocator, Value-based, Recovery

20. Automating chaos experiments in production (Netflix)    [2019, 1 refs]
    https://arxiv.org/pdf/1905.04648.pdf
    the morning paper - https://blog.acolyer.org/2019/07/05/automating-chaos-experiments-in-production/
    1. Netflix sharing how to architect chaos testing, automation and safety, auto experiment generation. interesting
    2. highlights
        1. Zuuel to redirect user traffc. Spinnaker for canary clusters, 1% size of original cluster
           Kayenta performs a statistical analysis of metrics collected on canary to compare with the baseline cluster
            1. question: if test does discovered bugs, that means user traffic is impacted? SLA failing is OK?
        2. Safeguards to minimize the blast radius
            1. experiments run in business hours on weekents
            2. cannot impact > 5% total traffic
        3. Chaos Monkey (old) - acts of random vandalism
           Monocle (new) - automatically uncovering service dependencies,
                           intelligent probing to seak out weakness,
                           automatically generate experiements
        4. experiement generation
            0. Hystrix provides RPC monitorings, dependency managements, timeout configs, etc
            1. basic experiment types
                1. Failure
                2. Latency just below the configured timeout
                3. Latency causing failure
            2. "Monocle using heuristics to try to identify the experiments
                with the highest likelihood of finding a vulnerability"
                1. dependency has a criticality score is product of
                    1. dependency priority
                    2. how frequently the dependency is triggered compared to all other dependencies in the cluster
                    3. the retry factor
                    4. and the number of dependent clients
                2. dependency score, safety score, experiement weight to produce the final prioritization score
    n. related
        1. Redliner - LinkedIn capacity testing
           https://engineering.linkedin.com/blog/2017/02/redliner--how-linkedin-determines-the-capacity-limits-of-its-ser
        2. Chaos Engineering Traps - Nora Jones
           https://medium.com/@njones_18523/chaos-engineering-traps-e3486c526059
            1. Trap 1: You can measure your success with Chaos Engineering by counting the number of vulnerabilities you find
            2. Good article. very useful experiences.

21. Mergeable replicated data types
    http://kcsrk.info/papers/oopsla19-mrdt.pdf 
    the morning paper: https://blog.acolyer.org/2019/11/25/mergeable-replicated-data-types-part-i/
                       https://blog.acolyer.org/2019/11/27/mergeable-replicated-data-types-part-ii/
    1. MRDT (related to CRDT). a specification for data structures, which can be modified locally,
           and then merged on remote central consistently
       enabling technology for collaborative local-first applications
    2. highlights
        1. versioned states and explicit merging operations, invertible relational specifications
        2. a abstraction function that maps the values of a type to the relational domain,
           and a concretization function that maps back again
        3. converting a data type to its relation domain (and convert back)
           haracteristic relations. how to automatically derive the merge specification
        4. Quark the implementation of MRDT
            1. How to efficiently store, compute, and retrieve the LCA given two concurrent versions?
            2. When is safe to garbage collect old versions that might be LCA of future merges?
            3. Git-like API
            4. a content-addressable block store
    n. related materials
        1. Hacker news: Mergeable replicated data types
           https://news.ycombinator.com/item?id=21625912
        2. CRDT: A Comprehensive study of Convergent and Commutative Replicated Data Types    [2011, 302 refs]
           https://blog.acolyer.org/2015/03/18/a-comprehensive-study-of-convergent-and-commutative-replicated-data-types/
            1. "Since, by design, a CRDT does not use consensus"

22. Taiji: managing global user traffic for large-scale Internet services at the edge (Facebook)    [2019, 0 refs]
    https://dl.acm.org/doi/pdf/10.1145/3341301.3359655
    the morning paper - https://blog.acolyer.org/2019/11/15/facebook-taiji/
    1. interesting. extends the thought of SocialHash to datacenter load balancing.
       Taiji works on Edge LB. connection-aware routing. improve DC utilization and cache hit.
    2. highlights
        1. friend groups are likely end up accessing similar content.
           can be exploited to improve cache utilization
            1. Taiji builds on top of "Social Hash" to provide "connection-aware routing"
            2. reduced query-load on backend databases by 17%, compared to a baseline implementation using Social Hash alone
            2. Social Hash on its own achieves 55% connection locality, with connection-aware routing on top, this goes up to 75%
        2. social graph partitioning is done offline on a weekly basis
            1. A binary tree of height H, the 2^H leaf nodes represents a bucket of 0.01% of users
            2. The 2^{L+1} nodes for level L+1 of the tree are generated by performing 2^L balanced bipartitions that minimize edge cuts
            3. users statically assigned to buckets during this weekly partitioning exercise
            4. to assign buckets of users to datacenters
                1. an online fashion via a Stable Segment Assignment algorithm
                2. by assigning a whole level of buckets (called a segment) in the community hierarchy to the same data center
                3. For stability, the same segments should be assigned to the same data centers as much as possible
        3. facebook load balancing
            1. www.facebook.com => DNS load balancing => one dozens of global edge nodes
               => datacenter
            2. question: does traffic goes through Edge LB?
               or Edge LB extents DNS to return routed datacenter IP to user?
        4. assignment solver
            1. a local search algorithm using the "best single move" strategy.
               it considers all single moves: swapping one unit of traffic between data centers,
               identifying the best one to apply, and iterating until no better results can be achieved
            2. The routing table is updated once every 5 minutes
        5. safety guards
            1. limit the volume of traffic change permitted in each update of the routing table
            2. limit how much the utilization of a datacenter can increase during an (five minute) epoch
            3. minimum shift limit prevents unnecessary thrashing by rejecting changes below 1%
            4. dampening factor, instead of making an exact traffic shift to the target value,
               which can lead to overshooting, Taiji aims for 80% of the target
    
    n. related materials
        1. SocialHash: An assignment framework for optimizing distributed systems operations on social networks (Facebook)    [2016, 25 refs]
           https://www.semanticscholar.org/paper/Social-Hash%3A-An-Assignment-Framework-for-Optimizing-Shalita-Karrer/7af56c6720fa1f554b419110f9b0cae0c7f7586d
           the morning paper - https://blog.acolyer.org/2016/05/25/socialhash-an-assignment-framework-for-optimizing-distributed-systems-operations-on-social-networks/
            1. good. new data partition/assignment methodology besides consistent hash. leveraging social group to exploit locality.
               Cache miss fell by 25%, avg response time fell by 50%
            2. highlights
                1. Almost all of the user-visible data and information served up by the Facebook app is maintained
                   in a single directed graph called the Social Graph.
                    1. Friends, Checkins, Tags, Posts, Likes, and Comments are all represented as vertices and edges in the graph.
                    2. The information presented to Facebook users is primarily
                       the result of dynamically generated queries on the Social Graph
                    3. Each weekly update resulted in about 1.5% of users switching groups
                       Edge locality has stayed steady at around 50%
                2. first stage: assign objects to groups
                    1. static assignment based on optimising a given scenario-dependent objective function
                       use graph partitioning. change on basis of daily
                    2. a cluster of a few hundred machines is able to partition the friendship graph of over 1.5B+ Facebook users
                       into 21,000 balanced groups such that each user shares her group with at least 50% of her friends
                        1. so, for fast lookup, 21K groups is OK to just put into memory.
                3. second starge: assign groups to components
                    1. dynamic assignment which rapidly respond to changes in the system and workload
                    2. both two stages need criteria
                        1. minimal average response times
                        2. load-balanced components
                        3. stability of assignment (avoiding too frequent changes)
                        4. and fast-lookup of the mapping
                n. questions
                    1. even user requests accessing same data are assigned to different app nodes,
                       they should eventually hit the same cache address in the lower layer of the system, e.g. DB cache
                       what social hashing does is to move lower layer DB cache hit to more fronter app node cache hit
                       so why is it so meaningful?
                        1. besiders assigning HTTP requests to app nodes, we also need to assign data records to storage nodes
                           the latter one we leverage Social Hashing to improve data locality (to avoid multi-get)
                    2. instead of leveraging social hashing,
                       why can't we just derive which data a user request is accessing by the user request itself?
                       then we can send them to the same node. i.e. content-aware routing

23. POLARDB Meets Computational Storage: Efficiently Support Analytical Workloads in Cloud-Native Relational Database    [2020, 0 refs]
    https://www.usenix.org/conference/fast20/presentation/cao-wei
    https://www.youtube.com/watch?v=_8gEmK1L4EY
    1. good. push down computation to SSD drive (Computational Storage Drives), e.g. inline compression, table scan. (customed hardware)
       this is a key technology of ScaleFlux@Inc (one author of paper). this is a new direction/area to research/adopt.
       PolarDB uses CSD to filter in SSD side, so less traffic needs to pass through even PCIe, nor network
    2. highlights
        1. Computational Storage Drive (CSD)
            1. V1: Table scan push down to stoarge node
               V2: Push computation hotspot to Accelerator (FPGA/CPU)
               V3: Replace SSD to CSD (Computational Stoarge Drive), no hotspot
                1. related coined: "Intelligent RAM", "Active Disk", "Intelligent SSD", "Smart SSD"
                                   "Smart NIC"
                2. concepts: V2 is "centralized heterogeneous computing architecture"
                             Vs is "distributed heterogeneous computing architecture"
            2. Improve benefit
                1. Focus on CPU-unfriendly tasks in mainstream applications
                    1. data path transparent compression
                        1. this is what ScaleFlux@Inc mentioned on website
                    2. inline data scan
            3. Reduce cost
                1. Make in-storage computation as transparent as possible
                2. Avoid any changes to the core structure/algorithm of applications
        2. adoption on PolarDB
            1. choosing FPGA to implement Table Scan, Flash Control on CSD
            2. how does FPGA understand the application defined table schema?
                1. FPGA code is designed to cope with flexible range of table schema. fullly customized for PolarDB
            3. how application knows the size change (for capacity management) after CSD does compression?
                1. CSD provides a simple API for applications to query the capacity info

24. Constant time recovery in Azure SQL database    [2019, 1 refs]
    https://www.microsoft.com/en-us/research/uploads/prod/2019/06/p700-antonopoulos.pdf
    1. Useful intro part for understanding ARIES.
       MVCC (when persistent earlier version) naturally makes DB recovery fast
    2. highlights
        1. long running transactions that slows down recovery
            1. a failure while customer transaction attempting to load millions of rows
               recovery took 12 hours; table exclusively locked inaccessible
        2. how ARIES / SQL Server database recovery works. Useful.
            1. Analysis step, determine redo start
            2. redo A: reacquire previous active transaction's locks by scanner former logs
               redo B: actually redo the logged but not-updated dirty pages
                1. here's problem
                    1. redo A steps need to scan as many logs as the longest running transaction
                2. SQL Server has former changes to parallelize the Redo phase
            3. undo: rolling back any transactions that were active in the failure
                1. Undo can be performed while serving user requests
                   because table is locked, user requests will be blocked if attempting to access the data under Undo
                    1. Oracle DB: "As new transactions encounter rows locked by dead transactions,
                                   they can automatically roll back the dead transaction to release the locks"
                        https://docs.oracle.com/cd/A87860_01/doc/server.817/a76965/c28recov.htm
                2. here's problem
                    1. Undo step too needs to scan as many logs as the longest running transaction
                3. Undo again needs to be logged by Compensation Log Records (CLR)
                    1. in case database failure during the Undo run
                4. questions
                    1. why need undo?
                        1. should be due to transaction was active but not committed when failure
                           we cannot push forward to finish those transactions neither
                    2. why need redo before undo, can't we just undo from the "redo start log"?
                        1. probably due to at (redo start log, newest log), some blocks can already be updated.
                    3. Why does Aries perform a redo before undo in database management recovery?
                       https://stackoverflow.com/questions/10289170/why-does-aries-perform-a-redo-before-undo-in-database-management-recovery
                        1. Because commit transactions may have unflushed pages
                           Redo needs to make sure the are flushed to on-disk pages
                           After that, Undo won't rollback those pages
                        2. The UNDO data log is logical, while the REDO data log is physical
                            1. We must do physical REDO, since we can't guarantee that the database is in a consistent state
                            2. We can do logical UNDO, because after REDO we know that things are consistent
                    4. does database recovery always need both redo and undo?
                        1. Deferred Modification Technique vs Immediate Modification Technique
                           https://www.geeksforgeeks.org/log-based-recovery-in-dbms/
                            1. Deferred - active transaction doesn't modifiy database until committed
                                1. E.g. the multi-version DB BigTable which preserves all modified versions
                                        and to use an atomic pointer update to switch stage to committed
                            2. sounds like using "deferred modification", DB doesn't need undo log.
                            3. "Hence, a deferred update is also known as the No-undo/redo algorithm"
                               https://www.geeksforgeeks.org/database-recovery-techniques-in-dbms/
                        2. Immediate Modification Technique
                            1. sounds like, the record must be locked. Not MVCC
                               otherwise, if multiple transactions are modifying the record to different values,
                               how to in-place modification?
                            2. how to rollback when the transaction aborts?
        3. how Constant Time Recovery is done?
            1. MVCC stores earlier versions (row level). Earlier versions are made persistent in Version Store.
               So, Undo just needs a mark, so earlier version is made visible
            2. How is "redo B" made constant time?
                1. CTR uses an additional SLog to track only relevant operations
                   not having to process the full transaction log
                2. since Undo is very fast using MVCC, we can also shutdown database during recovery
                   so that not locks are needed, no scanning are needed as in "redo B" step
        4. Persistent Version Store (PVS)
            1. In-row version store
                1. Just track the earlier versions data (diff) in row with the row data
                    1. like the BigTable solution
                    2. compared to using an indepenent Version Store, it saves the effort to mange
                       data layout, persistence, lookup and indexing
                2. negative impact
                    1. increase page size, which impacts B-tree page split
                    2. cap the row size, if exceeded, generate version data at Off-row version store, on a different page
            2. Off-row version store
                1. implemented as an internal table
                2. no index because all accesses are based on the version's physical locator
                    1. it sounds like, in a DB when building any new component and needs a data structure,
                       we just loop back and use the DB table iteself again
                3. off-row PVS is recovered using the tranditional recovery mechanism
                4. off-row PVS is highly optimized for concurrent inserts
                    1. accesses are cached and parititioned per cores
                        1. insert rows into different sets of pages to eleminate contention
                    2. inserts are logged in a non-transactional manner
                    3. space is pre-allocated
        3. SLog
            1. an in-memory log stream, serialized into the traditional transaction log
               the log entries are linked as a list

25. CRaft: An Erasure-coding-supported Version of Raft for Reducing Storage Cost and Network Cost    [2020, 0 refs]
    https://www.usenix.org/system/files/fast20-wang_zizhong.pdf
    1. Raft replicating EC fragments. for liveness, fallback to traditional replication.
       Candidate for systems using Raft to replicate data.
    2. highlights
        1. Raft to replicate log entries by EC fragmented format, for better performance
           if node count not satisfy liveness condition, will fallback to the traditional replication
            1. leader uses heartbeats to tell healthy node count
            2. example EC format: CRS 3+2
        n. questions
            1. so, it generally requires more nodes, because of EC, to form the quorum.
               so easier to hit liveness break due to node failures?
            2. per log entry to EC, is log entry large enough for compose an EC packet?
               or need to wait for more requests to fill up the EC packet? I.e. the delay
            3. the new failed over lead only has EC fragments. it needs to reconstruct the data
               what about the added recovery delay?
            4. EC reduces network bandwidth, but adds more IOPS. Is bandwidth the bottleneck of Raft?
                1. if paxos replicating metadata, that means bandwidth is usually small,
                   but leader node CPU and IOPS can be bottleneck
                2. if paxos replicating data (i.e. TiDB), this is the right scenario to ECed Raft

26. Serverless in the Wild: Characterizing and Optimizing the Serverless Workload at a Large Cloud Provider (Microsoft)  [2020, 0 refs]
    https://arxiv.org/pdf/2003.03423.pdf
    1. Observation from Azure Functions. CV of IAT and IT to measurement.
       Hybrid Histogram Policy for pre-warm window and keep-alive window
    2. highlights
        1. Study on Microsoft Azure Function.
        2. key problem: function execution needs warm up (to load up code, and related memory)
                        after execution, needs keep-alive (in case following invocations)
            1. need to avoid cold-start invocations
        3. observations
            1. some functions are invoked 10^8 times more frequently than the least popular ones
            2. a 4x range of function memory usage
                1. 90% apps never consume more than 400MB
                2. 50% apps allocate at most 170MB
            3. 50% function runs in less than 1 second
        4. invocation patterns
            1. CV of IAT - Coefficient of variation (CV), Inter-arrival time (IAT)
               to describe how stable the invocation interval can be
                1. categorized by trigger times: HTTP, Timer, Queue, Storage, Event, Orchestration, Others
             2. IT - Idle times. IT histogram reflexs the invocation intervals distribution
        5. Hybrid Histogram Policy - pre-warm window and keep-alive window
            1. pre-warm window: from the last execution, waits how long, to load the app image expecting next execution
            2. keep-alive window: the time duration for app image to be kept alive
            3. algorithm
                1. calculate the IT historgram. 5th percentile is usedas pre-warm, 99th percentile is used as keep-alive
                2. if too many out-of-bound ITs, use standard time-series forecasting - ARIMA
                3. it pattern not representative, fallback to conservative - fixed keep-alive

27. How to Copy Files (VMware)    [2020, 0 refs]
    https://www.usenix.org/conference/fast20/presentation/zhan
    1. clone operation (related to VM) needs high performance logical copy.
       A 4KB copy-on-write block is too large for space efficiency and too small for read/write locality
         the solution is to buffer the small writes together, together the increases space efficiency - copy-on-abundant-write
         and they colocated together, and flush to other nodes together, which improves the read/write locality
       very good paper. this is a new method to improve the very classic copy-on-write algorithm
       the youtube video is good intro how Be-tree works on BetrFS, and how this Be-DAGs/Bε-DAGs work
    2. highlights
        1. Existing logical copy implementations
            1. BTRFS: Leverages the underlying copy-on-write B-tree to implement `cp --reflink`
            2. XFS: Uses an update-in-place B-tree but supports sharing data blocks with copy-on-write via `cp --reflink`
            3. ZFS: Implements a limited version of copy-on-write copying via `zfs clone`
            4. problem
                1. Trade off: well - better space use vs bad - high fragmentation
                    1. faster reads & writes need locality, bad fragmentation
                    2. copy-on-write copies the inode, and allocate a new 4KB block on write
                        1. 4KB block is too large for space (e.g. only change 1 bit), too small for locality
                2. to measure space amplification
                    1. logically copy all files, then change 16B in each file (1KiB total)
                3. to measure fragmentation
                    1. logical copy number of times, vs, timing of grep the last copy
        2. Bε-DAGs: A high performance logical copy implementation in BεtrFS,
                    which leverages the properties of Copy-on-Write Bε-trees
            1. Be-tree has well locality and batch together small writes
                1. the key improvement of Be-tree compared to B-tree is, it buffers small changes in an node,
                   before flush them to the next node. where buffering reduces the IO cost
                2. i.e. copy-on-abundant-write
            2. copy is to add a new edge, turning the tree intoo DAG. pivots can include a path prefix translation
                1. a special "GoTo" message can act as a fake prefix transaction, until it turns into a real pivot node
        3. evaluations - something to notice
            1. Table 1 bottomline shows BetrFS 0.5's cleaning process creates huge space amplification.
               but after cleaning done, it is the most space efficient.
            2. Table 2 bottomeline shows BetrFS 0.5's random read performance is ~8% slower than ext4/BtrFS/XFS/ZFS
                1. no wonder Be-tree calls itself an "Write-Optimized Index"
                2. But, Table 3 shows `grep` on BetrFS is way faster than ext4/XFS/ZFS.
                   (baseline BetrFS is fast at `grep`, not by this paper)
        n. questions
            1. small writes are buffered at the top nodes in Be-tree first.
               how does user read knows which address those writes point to?
                1. Probably the addresses are inside the writes data. paper says Be-tree store key-value pairs
                   Be-tree calls them "messages"
                2. so .. if writes are too small, address itself is another space amplification?
                   but lower levels of the tree should need less address bits
            2. compared to LSM-tree, Be-tree buffers small writes than flush at once
               how to ensure the durability of each of the small-writes? than need a log again?
    n. related materials
        1. BetrFS: A Right-Optimized Write-Optimized File System    [2015, 77 refs]
           https://www.usenix.org/conference/fast15/technical-sessions/presentation/jannen
            1. Like LSM-tree for filesystem. But no need garbage collection,
               because Be-tree still allows a dgreee of in-place modification
            2. the paper calls Be-tree a "Write optimized indexes". Yes, reads are rediected
            3. Very good paper. The Be-tree index will leave its name in history. Now we have another alternative w.r.t. LSM-tree.
               And "How to Copy Files (VMware)" finds a new use for Be-tree index.

28. Reaping the performance of fast NVM storage with uDepot    [2019, 15 refs]
    https://www.usenix.org/conference/fast19/presentation/kourtis
    1. interesting. new KV store for NVDIMM (3DXpoint, Z-NAND).
       Index in DRAM by hash table. Log-structured on persistent device.
       IO Access by SPDK, userspace, polling (no interrupt), coroutine. - TRT
       Only very basic interface and feature set supported.
    2. highlights
        1. Fast NVMe Devices (FNDs) - new class of NVMs, e.g. 3DXpoint, Samsung Z-SSD / Z-NAND
        2. Existing KV stores cannot deliver FNDs' performance
            1. Built for slower devices (e.g., use synchronous IO)
            2. Data structures with inherent IO amplification (LSM- or B-trees)
            3. Cache data in DRAM, limiting scalability
            4. Rich feature set (e.g., transactions, snapshots)
                1. question: transactions, snapshots are right to give up?
        3. key design points
            1. minimize IO amplification
            2. scalability (cores, devices, capacity)
            3. only basic interface: point lookup, insert, delete. variable sized key value. bottom-up approach
        4. designs
            1. IO access
                1. SPDK: userspace IO, directly access device, polling instead of interrupts
                2. Linux AIO, epoll: receive IO completions
                3. syscalls: e.g. pread, blocking
                4. TRT: A task run-time system for asynchronous IO
                    1. avoid cross-core communication
                    2. userspace thread - coroutines
                    3. poller task for multiple IO backends
                    4. avoid stack ripping
                        1. http://bryanpendleton.blogspot.com/2011/01/stack-ripping.html
                        2. suppose there is a function, you do something, call an blocking IO, and then continue do things.
                           in event-based programming, you need to "rip" the later half to an event callback,
                             and pass the stack state as context.
            2. Index in DRAM - Two-level hopscotch hash table resizable
                1. two-level: directory + hash table
                    1. directory relates to set-associative cache
                    2. when growing
                        1. double the size of directory, hash table split and entry assign
                        2. no blocking to reads, no IO required, incremental
                    3. use an array of locks to protect concurrency, lock by neighborhood region
                       operations take two locks at most
                2. hopscotch [37] is a hash table collision strategy, similar to linear probing, but with a bound neighborhood 
            3. SALSA - On NVM log-structured allocation
                1. and need GC
        5. implemntation notes
            1. uDepot is implemented in C++11. uDepot's performance requires many optimizations
                1. eliminate heap allocations from the data path using corelocal slab allocators
                2. use huge pages
                3. favor static over dynamic polymorphism
                4. avoid copies using scattergather IO, and
                   placing data from the network at the proper location of IO buffers
                5. use batching
        n. questions
            1. how is DRAM index persistent? what if lost?
                1. flush index to FND on shutdown. If it's not clean (by checking checksum), do reconstruct
            2. does the hash table stores the original value of key (variable sized)?
                1. I didn't find it. only key fingerprint is stored in hash table
                2. so .. it means, if two key's hash value collides, they kick out the other?
    n. related
        1. libcuckoo, cuckoo hashing. it looks getting popular

29. A Comparison of Adaptive Radix Trees and Hash Tables    [2015, 22 refs]
    https://bigdata.uni-saarland.de/publications/ARCD15.pdf
    1. For NVDIMM indexing, ART and hashtable are competitive.
    2. highlights
        1. comparison candidates
            1. ART
            2. ART-PC - ART with path compression
            3. Cuckoo hashing varients
                1. standard Cuckoo hashing using 2 tables - CHFast
                2. standard Cuckoo hashing using 4 tables - CHMem
                3. Cuckoo hashing using 64-byte buckets - CHBucket
                4. hash method varients
                    1. MurmurHash64A - Murmur
                    2. multiplicative hashing - Simple
        2. experiement results
            1. ART has better memory efficiency
            2. hashtable families are relatively faster (insertion, lookup)

30. Building An Elastic Query Engine on Disaggregated Storage (Snowflake)    [2020, 2 refs]
    https://www.usenix.org/conference/nsdi20/presentation/vuppalapati
    the morning paper - https://blog.acolyer.org/2020/03/09/snowflake/
    1. disaggregating compute and storage is a direction of OLAP. (Actually the trend flips opposite sides every a few years)
       Snowflake architecting the cloud native OLAP database / data warehouse
       per cloud native, key methodology to improve underutilized resources, is to disaggregate them.
         And for highly utilized resources to protect from burst over utilized, elastic is the needed capability
            e.g. a pool of pre-warmed ready-to-add resources / nodes
         good paper. this is the new light for how to architecture on resource utilization (and cloud-native OLAP)
    2. hightlights
        1. problems at traditional share-nothing data warehouse systems
            1. CPU, memory, storage, and bandwidth resources are all aggregated at each node, and can't be scaled independently,
               making it hard to fit a workload efficiently across multiple dimensions.
            2. The unit of resource allocation is coarse-grained (a node) and the static partitioning makes elasticity difficult.
            3. An increasingly large fraction of data in modern workloads comes from less predictable and highly variable sources
        2. the morning paper author (Adrian Colyer) thinks about cloud-native architectures
            1. disaggregation (enabling each resource type to scale independently)
            2. fine-grained units of resource allocation (enabling rapid response to changing workload demands, i.e. elasticity)
            3. isolation (keeping tenants apart)
        3. what Snowflake does
            1. decoupling (disaggregation) of compute and storage
                1. Customer data is persisted in S3 (or the equivalent services when running on Azure or GCP),
                   and compute is handled in EC2 instances
                2. to avoid read from S3 every time, Snowflake has a caching layer
                    1. a distributed ephemeral storage service shared by all the nodes in a warehouse
                    2. Besides, the primary purpose is to handle the (potentially large volumes of) intermediate data
                       that is generated by query operators (e.g. joins) during query processing
                3. the emphemeral storage service
                    1. three-tier with in-memory data on a node spilling to local SSDs when needed,
                       which in turn spill over to S3 if they are exhausted
                    2. A consistent hashing scheme maps data to nodes
                    3. currently, the compute node and emphemeral storage services are not decoupled yet
                       decoupling them is future work
                    4. ephemeral storage can be small, OK for just 0.1% of customer's persistent data volume.
                       hit rates ~80% for read-only queries and ~60% for read-write queries
            2. Tenant isolation is achieved by provisioning a separate virtual warehouse (VW) for each tenant
                1. customer separated by virtual warehouse
                    1. problem: individual VW can be underutilized. but for isolation, we cannot simply colocate them
                    2. maintaining a pool of pre-warmed instances was cost-efficient, but
                        1. recent moves to per-second pricing by all major cloud infrastructure poses challenges
                        2. With per-second billing, we cannot charge unused cycles on pre-warmed nodes to any particular customer
                2. more underutilized issue, e.g. DRAM, probaly solution is to further disaggregate them
            3. some observations
                1. Predicting the volume of intermediate data generated by a query is "hard, or even impossible" for most queries.
                   Intermediate data sizes vary over multiple orders of magnitude across queries,
                   and have little or no correlation with the amount of persistent data read
                    or the expected execution time of the query.
            4. Elasticity
                1. Using pre-warmed pool of nodes, compute elasticity be provided at tens of seconds
                2. consistent hashing with work stealing to assign tasks to nodes
                3. upon consistent hashing reconfiguration, how to migrate data (data reshuffling)?
                    1. Snowflake does this lazily. at new node, data read from persistent storage and cached again
                       old node data will be evicted later from cache
                4. possiblity of using serverless (Firecracker) for auto-scaling, high elasticity, and fine-grained billing
                    1. key barrier for Snowflake is serverless lack of support for isolation (but .. Firecracker?)
                    2. require a disaggregated ephemeral storage solution first
        4. related systems
            1. Amazon Redshift [16], Aurora [4], Athena [3], Google BigQuery [30] and Microsoft Azure Synapse Analytics [24]
        n. questions
            1. what about pushing down computation close to data side? we are moving the the opposite direction?
                1. probably networking is way faster now.
                2. interesting compared to the PolarDB Computation Storage Drive (CSD) paper
                    1. PolarDB uses CSD to filter in SSD side, so less traffic needs to pass through even PCIe, nor network
            2. Snowflake is cloud native. What if it tries to build storage + computation in the same node?
                1. probably, managing the persistence layer by itself is complex, just not as handy to leverage S3 directly
            3. the emphemeral storage service is needs to plan capacity cost
               but paper aslo said hard to predict "intermediate data generated by a query". So a bit conflicting?
            4. disaggregating improves resource utilization, but it relies on networking to quickly pass data
               today networking is way faster than CPU and storage. there are latencies. OLAP is OK. what about OLTP? 

31. Shenango: Achieving High CPU Efficiency for Latency-sensitive Datacenter Workloads    [2019, 24 refs]
    https://www.usenix.org/conference/nsdi19/presentation/ousterhout
    1. improvement for ZygOS, which statically allocate cores spin polling NIC targeting peak load.
       Shenango reallocate cores per 5us, with IOKernel steers core allocations based on incoming packets
         So that CPU core utilizaition is improved. Note Shenango itself consumes one dedicate core
       good paper as to throw light on how to solve the old classic CPU utilization vs latency problem
         and with today's fast networking scenarios
    2. highlights
        1. current problems
            1. Datacenters usually fill latency-sensitive jobs and batch jobs to improve CPU utilization
               E.g. Microsoft Bing colocates latency-sensitive and batch jobs on over 90,000 servers [34]
            2. Linux can only support microsecond latency when CPU utilization is kept low,
               when leaving enough idle cores available to quickly handle incoming requests [41, 43, 76]
            3. More, these systems waste CPU cycles, because instead of interrupts, they rely on spin-polling NIC
               to detect packet arrivals, so the CPU is always in use even when there are no packets to process
                1. this is today's kernel bypassing, userspace networking, DPDK, RDMA stuff doing.
                   the CPU cores dedicated to polling are for peak load. wasting during lower load
            4. ZygOS, the comparison system, must dedicate all cores to the latency-sensitive spin server
        2. how Shenango does it
            1. reallocates cores every 5 us, orders of magnitude faster than other OS scheduling
                1. core reallocations complete in only 5.9 µs
            2. algorithm to accurately determines when applications would benefit from additional cores
               based on runnable threads and incoming packets
                1. IOKernel polls thread and packet queue to detect congestion.
                   this is when need to allocated more cores.
                    1. consider queued threads and queued ingress packets
                    2. the duration of queuing is a more robust signal than length of a queue
                        1. if any item is found present in two consecutive runs of detection algorithm
                           it means the item has been congested for at least 5us
            3. dedicates a single busy-spinning core per machine to IOKernel,
               which steers packets to applications and allocates cores across them
                1. IOKernel also does the work to re-steer packets after allocated new cores
        n. questions
            1. compared to "Building An Elastic Query Engine on Disaggregated Storage (Snowflake)"
               another way to improve resource utilization is to disaggregate them,
               allow decoupled scale-out/in, and also equipped with fast elasticity
            2. Shenago's scenario is mostly "idle cores must be reserved to absorb bursts in load, resulting in a loss in CPU efficiency"
               does it also work for scenario of placing latency-sensitive workloads with batch workloads,
               to maintain high CPU utilization, while same time keep latency low?
                1. current paper mostly talk about utilization at CPU core assignment level
                   no much mentioned about time slice scheduling, e.g. if latency-sensitive job wants to run,
                   but too many batch jobs queued already in CPU queue
                    1. "7.2 Resilience to Bursts in Load" and "Figure 5" is evaluating similar scenario
                       but it is targeted on TCP requests throughput burst.
                    2. Anyway, most systems, the load is represented by network requests, as the paper said

32. MAPX: Controlled Data Migration in the Expansion of Decentralized Object-Based Storage Systems    [2020, 0 refs]
    https://www.usenix.org/conference/fast20/presentation/wang-li
    1. Ceph CRUSH data rebalance migration problem needs solve. this paper adds new abstraction "layer"
       new data maps new PG maps to new layer. internally new vs old are differentiated by timestamp (tracked in metadata)
       good paper. it is handy to the data rebalance migration problem.
           note layer needs to be large enough to satisfy all failure domains of the PG (e.g. 3-replica)
    2. highlights
        1. current problems
            1. Ceph's CRUSH: uncontrolled data migration when expanding the clusters
                             which will cause significant performance degradation
        2. MAPX solution
            1. every capacity expansion adds a new layer. CRUSH adds a new step select(1, layer).
               a new set of PGs will be created for the new layer. new PG will be tagged with timestamp
               new objects created (tell by timestamp) will be assigned to new PGs
            2. to rebalance PGs across layers (which become imbalnace after time of changes)
                1. PG remapping
                    1. PG has a second dynamic timestamp. select(1, layer) can map to another layer
                       by manipulating this dynamic timestamp
                2. cluster shrinking
                    1. like capacity expansion, you can only add/remove entire layer.
                       "PG remapping" after removed layer
                3. layer merging
                    1. by setting one layer's timestamp same with the other layer
        n. questions & feedback
            1. if manage metadata in centralized metadata server, we don't have the migration problem
               we can just let new ingested data to fill up the new nodes.
            2. so .. to avoid rebalance, the cost is still to add metadata. this time, the metadata is the timestamp.
               and we need to be corase grain enough to reduce metadata size,
               i.e. the concept "layer" is a big size one, rather than to support per single node capacity expansion
    n. related materials
        1. 看了几篇FAST 2020 - 暗淡了乌云 - MAPX
           https://zhuanlan.zhihu.com/p/109774040
            1. author's feedback for MAPX.
                "显然这样的方法有还有一些问题：

                    * 这样做有一个明显的问题就是，如果新增的layer不满足故障域隔离怎么办 ？如上图（a）蓝色扩容，如果只增加了两个cap，那么只能选出PG的2个副本位置，第三个会选择失败；MAPX会select失败的从原先的root去继续选；

                    *如果由于删除等原因，出现数据imbalance怎么办 ？MAPX给出了一个PG remapping方案，为此增加了一个adynamic timestamp (tpgd)，它可以设置为任意一次扩容layer的扩容时间戳，和object到PG映射使用tpgs不同，PG到layer的映射则是根据PG的tpgd，其映射必须和layer的创建时间一致。同理缩容（Cluster shrinking）和集群合并（Layer merging）都可以通过类似的方法实现。

                MAPX通过两个时间戳来控制数据分布和PG的迁移，但是感觉这里难点是如何做PG remapping来保持PG在集群的均匀分布，但是文章并没有描述；除此之外，new data放到new layer PG上，或许是不会有数据迁移，但是数据热点的问题如何解决呢？

                其实对于ceph crush来说，其实是大规模的扩容带来的数据迁移会很大，如果能够合理的做好集群规划，那么每次按照cluster/pool级别来扩容，那么自然也不会有大量数据迁移。而一些简单坏盘等交给crush本身，做好流控，理论上也应该是可控的。"

33. HotRing: A Hotspot-Aware In-Memory Key-Value Store (Alibaba)    [2020, 0 refs]
    https://www.usenix.org/system/files/fast20-chen_jiqiang.pdf
    1. very good paper. improvement on classic DRAM hashtable of linklist chain. very simple but effective
       change the linklist to a circular list, hashtable entry points to hot item.
       the technique can be widely adopted, useful upon high collision scenario
    2. highlights
        1. For how it works, see "了几篇FAST 2020 - 暗淡了乌云 - HotRing"
        2. designs
            1. when searching in the ring, how to know we reached the end?
                1. ring is sorted, so if met a smaller key, this is end
                2. comparing key is expensive, comparing (tag, key) instead
            2. statistical sampling stategy
                1. Sampling needs CAS operations. If sampling flag is on, collect access counts
                2. adjust ring head to the item of highest access frequency
                3. after R requests finishes, determine whether need to resample by
                   check whether the Rth access is a hot acess. if yes, no need resampling
            3. lock-free
                1. write-intensive hotspot with RCU
                    1. a write-intensive hot item also makes its preceding item hot (due to ring traversal dependencies)
                    2. in-place update for small values (up to 8 bytes)
                    3. update large value by RCU (Read-Copy-Update)
                2. lock-free rehash
                    1. trigger by average number of memory accesses to retrieve an item, rather than load factor
                    2. a ring split to two rings, by a rehash node
        n. questions
            1. if the HotRing hashtable is truely useful, why not evaluation with production data?
            2. no comparison with Cuckoo Hashing?
    n. related materials
        1. 看了几篇FAST 2020 - 暗淡了乌云 - HotRing
           https://zhuanlan.zhihu.com/p/109774040
            1. "这也是本文HotRing巧妙之处，简单的说，就是HotRing通过特殊的设计可以自动识别出hotitem，
                并且将其放在collision chains的head，从而大大提升了访问hotspot data的性能。"
            2. "其将原本的是单链表的collision chains替换成了，双向链表的一个环（ring）"
            3. "那如何识别出hotspot item呢？"
                1. "这里介绍一种Random Movement Strategy"
                    1. "每个线程维护一个thread local的计数器，每当处理R个request后，会判断当前的访问的item是不是在collision chains head上，
                        如果在，那么不做任何处理，如果不在，那么让head指向当前访问的item，也就相当于当前命中的item转变成了hotspot item"
                2. "效果更好的但也更复杂的strategy：Statistical Sampling"
            4. "更多为了提升Concurrent Access而做的lock-free设计"

34. Dostoevsky: Better Space-Time Trade-Offs for LSM-Tree Based Key-Value Stores via Adaptive Removal of Superfluous Merging    [2018, 32 refs]
    https://www.youtube.com/watch?v=fmXgXripmh0, https://nivdayan.github.io/dostoevsky.pdf
    1. very good paper. it builds the model & approach how to analyze LSM-tree, how to trim it at different costs.
       the theory is simple and direct; Dostoevsky way outperforms existing LSM-tree implementations
       Summary: base Tiering layout, last layer has 1 segment, optimal Bloom filter memory assigment, Fluid bound adjustment
    2. highlights
        1. LSM-tree: IO cost of point/short-range/long-range lookup, vs merging, vs space amplification
            1. the YouTube video is easy to understand as how to derive those O(.) numbers
                1. the paper has more detailed modeling, into the data entry level
                2. updates: analyzed by amortizing the merge cost back to a single update.
                    1. leveling has more merges per level
                3. point lookup: analyzed meeded to combine Bloom filter FPR (False positive rate)
                    1. tiering has more segments per level, thus need more lookups
                    2. short-range lookup and long-range lookup don't involev Bloom filter, they are easier
                        1. the concept "selectivity" s is of good use
                4. space-amplification
                    1. defined as "total entries / unique entries - 1". this walks around the size calculation
            2. the knobs
                1. T controls the number of levels, i.e. how many times an entry need to merge across levels
                2. merge policy controls how many times an entry need to merge within a level
            3. the key trade-off is tiering vs leveling
                1. tiering (Cassandra): Only merge run within an level when the level reaches capacity limit
                2. leveling (RocksDB): Merge run within an level whennever a new run comes in
                3. key observation / formula results
                    1. point lookup cost, long range lookup cost,
                       and space-amplification derive mostly from the largest level,
                       while update cost derives equally from across all levels
                    2. so, lazy leveling - merges less at smaller levels
            n. some assumptions in paper need to note
                1. RocksDB merges in granularity of SSTable, while this paper simplifies them as "runs"
                2. An obsolete entry does not get removed until its update reaches the largest level
                    1. focus on worst case to analyze greatly simplies a lot of formulas,
                       as a technique used many times in this paper
                3. if you look at the formula, the point lookup cost analysis is only applicable to zero result lookup
                   so that the lookup queries each zeros, and the formula of each level is of same format so can easily add
                4. point lookup analysis requires using Monkey's or corresponding Bloom filter settings
                    1. Monkey's bloom filter: : Level i gets a +b · (L − i) bits per entry
                        1.  a small, asymptotically constant increase to the FPR at the largest level 
                        2. an exponential decrease to the FPRs across smaller levels
                    2. larger levels need more Bloom filter bits to reduce FPR
                5. space amplification als assumes worst case, level 1 to L-1 are all obsoleting entries.
                   only when they reach the bottom layer they find out to delete the old.
                   1. question: per space amplification, Tiering's O(T) is T^2 larger than Leveling's O(1/T). this is huge diff.
                       given T=10, it is true that Tiering can be 100x space amplification than Leveling?
        2. Lazy Leveling: Level 1 to L-1 use Tiering, Level L uses Leveling
            1. next, need to adjust the bloom filter. given memory budget M, by optimially assign them to
               each level, it can optimally reduce the FPR and then the point lookup complexity becomes
               the same with the original Leveling solution
                1. question: why not directly apply this technique to Tiering? so Tiering solution would be faster then
                   and then, the key improvement of Lazy Leveling is actually, set the last level segment count to 1. 
        3. Fluid LSM-Tree
            1. At most Z segments at the largest Level, and at most K segments at each other (smaller) levels
            2. again, need to setup the optimal Bloom filter assigment similar to Lazy Leveling
               necessary to achieve the optimal point lookup cost
                1. question: how to quickly adapt the running Bloom filter to changing workload
            3. Appendix C MEMORY REQUIREMENT
                1. using formula (23), it needs ~0.1265 bytes per element.
                   suppose we store 64KB elements, we need ~2MB per TB of data.
            4. to find the Bloom filter FPR per each level to achieve optimal point lookup cost
               given the constraint of total memory budget. we use Lagrange multiplier method
                1. Khan academy: Constrained optimization introduction, Lagrange multiplier
                   https://www.khanacademy.org/math/multivariable-calculus/applications-of-multivariable-derivatives/lagrange-multipliers-and-constrained-optimization/v/lagrange-multiplier-example-part-1
                    1. 在约束极值点，f(x,y)=maximal的等高线与约束函数φ(x,y)=0的等高线相切。那么，此处f(x,y)与φ(x,y)的gradient（梯度）同向。L(x,y)=f(x,y)+λφ(x,y)偏导为零，其实是让gradient平行的公式。
                    2. 拉格朗日函数L的梯度为零，等价于，f(x,y)与φ(x,y)梯度平行，并且φ(x,y)=0。这样，f(x,y)在约束下求极值的问题，就变成了L的无约束极值问题。
                2. 多元函数条件极值的求法 拉格朗日乘数法
                   https://blog.csdn.net/a493823882/article/details/80508455
                3. some more notes
                    1. we try to maximize f(x,y), with constraint φ(x,y)=0
                    2. let x=A(a,b), y=B(a,b), that φ(A(a,b),B(a,b))≡0 so, ∂φ/∂a=∂φ/∂b≡0
                    3. f(x,y)'s extremal point with constraint φ(x,y)=0 is equivalent with: ∂f/∂a=0, ∂f/∂b=0
                    4. let L(x,y)=f(x,y)+λφ(x,y), then ∂L/∂a=∂f/∂a, ∂L/∂b=∂f/∂b.
                       so, with constraint φ(x,y)=0, f(x,y)'s extremal point is equivalent with L(x,y)'s extremal point
                    5. L(x,y)'s extremal point on R, if cross with φ(x,y)=0, then it must also be the extremal point of L(x,y) under φ(x,y)=0
                       if (x,y) is extremal point of L(x,y) under φ(x,y)=0
        n. questions & feedbacks
            1. Note, SSTable merges in granularity of SSTable, while this simplifies them as "runs"
            2. given the model, is there production data to verify the actual gains?
            3. the lookup cost of Tiering is mainly due to need to search every segment in a level
               the paper says "one I/O to every run (i.e. segment)", but actually we can use smarter index
               to save it. This renders Tiering not so bad for point lookups
                1. this is also why Lazy Leveling needs a special handling bloom filter for point lookups
                   it's some sort of not so fair compare for the original Tiering
                2. question, why not directly add a bloom filter for each segment in Tiering.
                   then the main cost of Tiering solution is gone.
            4. Dostoevsky needs monitoring and quicky adapt data structures e.g. the optimal Bloom filter set
               against running workload. this is non-trivial. How is it built?
                1. implemented in RocksDB, implemented auto-tuning by measuring the proportion of different
                   operations in the workload during time windows and feeding them to Equation 14
                2. but anyway, even if we cannot realtime adapt, we can measure business workload and trim our LSM-tree
                3. Dostoevsky can be an auto tuning strategy of broader use?
            5. if it is so good why not test with some standard benchmark e.g. YCSB
            6. instead of using optimmal bloom filter or etc techniques to improve Tiering's lookup efficency
               across multiple segments in a level. Why not invent a better secondary index on those segments?
    n. related materials
        1. Monkey: Optimal Navigable Key-Value Store    [2017, 68 refs]
           https://stratos.seas.harvard.edu/files/stratos/files/monkeykeyvaluestore.pdf
            1. Same author's paper. Monkey is outpeformed by Dostoevsky
            2. "Our insight is that the recent Bloom filters optimization in Monkey [22] offers a new avenue
                for optimizing update cost by relaxing merging at lower levels while keeping point lookup cost fixed"
        2. SIGMOD'18|Dostoevsky - 叶提
           https://zhuanlan.zhihu.com/p/129355502
```
