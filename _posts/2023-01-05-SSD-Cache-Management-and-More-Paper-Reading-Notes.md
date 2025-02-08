---
layout: post
title: "SSD Cache Management and More Paper Reading Notes"
tagline : "SSD Cache Management and More Paper Reading Notes"
description: "SSD Cache Management and More Paper Reading Notes"
category: "Paper Reading"
tags: [storage, paper, cache]
---
{% include JB/setup %}

As the new storage media being quickly adopted, it's interesting how to manage cache on SSD device and work together with DRAM memory.

```
1. Readings: Papers: Managing Cache on SSD device
    1. SSD as Cache: CacheLib and Kangaroo
       https://zhuanlan.zhihu.com/p/430451374
        1. good, as introducing key designs of caching on SSD
        2. papers
            1. Facebook CacheLib
            2. Kangaroo: Caching Billions of Tiny Objects on Flash
    
    2. Facebook flashcache
       https://github.com/facebookarchive/flashcache/blob/master/doc/flashcache-doc.txt
        1. Linux kernel set-associative cache built atop device mapper
        2. highlights
            1. a set associative hash, Linear probing within a set to find blocks
            2. a sequential range of disk blocks will all map onto a given set
            3. the storage unit is blocks, id-ed by disk block number.
            4. flashcache is built upon Linux Device Mapper (DM)
            5. Replacement by FIFO, LRU. cache by writeback. non atomic "Torn Page Problem" exists
                1. the cache eviction can make holes in SSD block, so it's relying on SSD GC to handle it
            6. cache metadata (block dirty or not), on clean shutodwn will be flush to SSD, VALID and DIRTY blocks will be persisted
               if node crash, only DIRTY blocks will be persisted. but on new startup, it doesn't know VALID or DIRTY or not
        3. Futures and Features
            1. Cache Mirroring
            2. Cache Resizing
            3. Integraiton with ATA TRIM Command
            4. Deeper integration with filesystems
            5. Fixing the "Torn Page Problem" (make Cache Writes atomic)
                1. sector size write is atomic (should be ..)
                2. use shadow paging, don't overwrite metadata but use a shadow page
            6. Breaking up the cache spinlock
            7. Make non-cacheability more robust
    
    3. BCache for Ceph
        1. Bcache against Flashcache for Ceph Object Storage
           https://blog.selectel.com/bcache-vs-flashcache/
            1. problems with Facebook Flashcache
            2. bcache merged into kernel
               https://www.kernel.org/doc/Documentation/bcache.txt
                1. write-back, write-through and write-around caching
                2. create a bcache device with more than one backing device
                3. operate on B+tree rather than set-associative, higher hit rate
                4. PI controller to count the write-back rate
        2. 企业级Ceph之路（二）：使用bcache为Ceph OSD加速的具体实践
           https://segmentfault.com/a/1190000038448569
            1. 利用Journal/WAL加速B+tree的修改, 写完journal以及内存中的B+tree节点缓存后写IO就可以返回了
            2. 无效的旧数据就会在其所在的bucket内形成“空洞”，但是由于bcache空间回收的单位是bucket，因此需要一个异步的垃圾回收（GC）线程来实现对这些数据的标记与清理，并将含有较多无效数据的多个bucket压缩成一个bucket
                1. GC分为两个阶段：
                    1）元数据的GC：即B+树的GC，主要原理是遍历B+树，根据bkey信息标记出无效的缓存数据以及有效的缓存数据（包括脏缓存数据与干净的缓存数据），以及元数据。然后压缩清理元数据bucket。
                    2）缓存数据的GC：在bcache中被称为Move GC，主要原理是根据元数据GC阶段遍历B+树后生成的数据bucket的标记信息，找出含有较多无效数据的多个bucket，将其中的有效数据搬移到一个新分配的bucket中去，以便及时回收更多的bucket。
        3. The Linux kernel user’s and administrator’s guide » A block layer cache (bcache)
           https://www.kernel.org/doc/html/latest/admin-guide/bcache.html
        4. A block layer cache (bcache)
           https://www.kernel.org/doc/Documentation/bcache.txt
            1. reliably handle unclean shutdown, writes are not complete until they are on stable storage
            2. rolling average detects sequential IO and skip it
        5. The Programmer's Guide to bcache:
           https://bcache.evilpiepirate.org/BcacheGuide/
            1. diving into the code base
            2. reliably handle unclean shutdown, writes are not complete until they are on stable storage
                1. Ordering of insertions/updates is always preserved, across unclean shutdowns and without any need for flushes
                2. sequential consistency, preserve ordering. ordering is preserved in journaling, data is added in btree nodes.
                   but updates at two different btree nodes can be flushed in any order, and they can even be flushed earlier than journal - steal, no force
                    1. upon recover, journal is to determine whether a flushed-too-early entry is valid. key overwrite will preserve older key data still on disk. so bcache doesn't need a undo log here.
            2. read lock, write lock, intent lock
                1. read lock cannot upgrade to write lock because it can lead to deadlock
                2. if only using upgrade lock, it would need longer lock held period, than introduce intent lock
            3. Bcache is extent based, not block based; its extents are much like extents in other filesystems that has them - a variable sized chunk of data
                1. Bcache's extents are indexed by inode:offset
                    1. extent supports compression, checksum is extent leve, nad needs read entire extent to update after compression
                    2. extent can have garbage ranges, garbage collection is needed for rewrite.
                        1. GC should also be able to copy valid data from dead bucket
                        2. OK .. bcache does have "garbage collection", "copygc", "trigger_gc" .. but this article skipped GC section
                    3. future supports of eraure coding / RAID
                        1. What we want is to be able to erasure encode unrelated data together - while avoiding update in place
                2. The devices bcache manages are divided up into fixed sized buckets (typically anywhere from 128k to 2M). The core of the allocator works in terms of buckets
                    1. use a bucket generation number for reusing bucket, invalidating any live pointer
                    2. When a bucket is allocated, it is written to once sequentially: then, it is never written to again until the entire bucket is reused
    
    4. Windows SBL SSD caching disk
        1. SNIA SDC - Software Defind Storage based on Direct Attached Storage - Slava Kuznetsov
           https://www.snia.org/sites/default/files/SDC15_presentations/sds/Slava%20Kuznetsov_Software_Defined_Storage_SpacesDirect.pdf
            1. Storage Bus Cache
               https://docs.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-storage-bus-cache
            2. Understanding the cache in Storage Spaces Direct
               https://docs.microsoft.com/en-us/windows-server/storage/storage-spaces/understand-the-cache
            3. Storage Spaces Direct overview
               https://docs.microsoft.com/en-us/windows-server/storage/storage-spaces/storage-spaces-direct-overview
                1. Storage Spaces Direct at Microsoft Ignite 2018 (1 hour)
                   https://www.youtube.com/watch?v=5kaUiW3qo30
            4. Storage Spaces Direct – Software Storage Bus
               http://michaelstoica.com/storage-spaces-direct-software-storage-bus/
    n. my thinking is either caching layer does GC, or rely on SSD FTL layer to do GC. Using SSD FTL to do GC should be more practical.
        1. first layer caching is in memory. after eviction from mem, entries goes into SSD, the write to SSD is sequential, with a in-mem index to remeber
        2. if the SSD item is hot again, it will be loaded into mem again.
        3. if the SSD item is cold, that means it's not in mem and only on SSD, we can delete entire oldest SSD block. so that less impacting SSD GC erasing
        4. on cache system startup, SSD data will be loaded into mem. We need previously checkpoint hot in-mem items into SSD, so now we can load.
           The SSD block loading process can be from new to old. The problem is there can be items in old blocks, but are actually hot in-mem. so we loading old block items in mem, we probably need to log a mark in SSD to know these are hot items too
        5. we also ned indexing in-mem, the index can be full rebuild from startup, or needs to manage disk checkpoints and logging updates
           besides, separating large size item and small size item into different pools, using different structures can also be thought
    n+1. new thinkings.
        1. relying on SSD GC will lead you to a block-based, overwrite, filesystem. Think how you need to write a large 4MB user data, but there is no contiguous blocks. Internal fragmentation can cost capacity, and in the end leads to GC by software layer again
        2. Software managing GC leads to an append-only, extent based, system, just like stream. It's free of fragmentation. and GC cost must be spent anyway in either layer. Besides, managing everything by software layer gives more chance for optimization. Think about cache KV are of variable size. It's an argue of MySQL InnoDB vs RocksDB, essentially Facebook switched InnoDB to RocksDB engine for MySQL.

    5. 如何保持mysql和redis中数据的一致性？
       https://www.zhihu.com/question/319817091/answer/2272821847
        1. 大宽宽's answer
            1. Cache Aside solution
                1. App update DB, then app invalid cache. Cache also has expire time
                2. has a <1 cache inconsistent window
            2. Cache as single source of truth
                1. App access cache only, DB pushes updates to cache; App never directly access DB 
                2. background sync pushes App update from Cache to DB. 
            3. Write Through solution
                1. Compared to "Cache as single source of truth", let App write to DB bypassing Cache. Reads always go to cache
        2. Scaling memcache at Facebook
           https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala
            1. Handling updates: Memcache needs to be  invalidated after DB write, Prefer deletes to sets
                1. this is the Write Through solution
            2. possible MC & DB inconsistency
                1. Extend memcache protocol with “leases”
                    1. when A updates and deletes a key in memcache, the old lease is expired
                       thus B cannot set the old value with the old lease
            3. sounds like a very good paper that has solved the fundamental DB+Cache problem, let's read later
        
        3. Scaling memcache at Facebook    [2013, NSDI13, 965 refs]
           https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala
           https://www.usenix.org/sites/default/files/conference/protected-files/nishtala_nsdi13_slides.pdf
            1. very good paper. funding architecture how to use mem cache for DB with large scale, cross geo-regions
               innovative thundering herd lease, McSqueal, McRouter, pooling, cross region writes designs. allow inconsistency in short time
            2. highlights
                1. workload targeting memcached
                    1. DB + many cache architecture, write few read many, typical Intenet company workload
                    2. data OK to be inconsistent for a short while
                2. cache consistency
                    1. demand-filled look aside. i.e. write to DB then invalid cache, read to cache and if miss fetch from DB fill cache
                3. handling the load
                    1. incast congestion
                        1. client uses a sliding window for throttling
                    2. thundering herd
                        1. key undergoes repeated heavy write - this is the good design
                        2. solution
                            1. writer to cache carries a lease token, memcached verifies whether the lease is valid. if interrupted in middle by another writer, lease will be invalidated
                            2. memcached regulates the rate to issue new lease token, once every 10s
                4. grow the regional scale
                    1. McSqueal: rather than client invalidate cache, McSqueal monitors MySQL commit log to batch the invalidation
                    2. McRouter: rather than N*N connections, use McRounters in middle to reduce to N+N connections
                    3. FrontEnd Memcached: DB is shared by clusters, but each cluster uses its own FE Memcache
                    4. replication pool
                        1. why replication rather than adding more services in consistent hash? good analysis
                            1. adding more services causes clients to split their requests. each request becomes smaller, but per server IOPS is same
                            2. use replication to reduce per server IOPS
                    5. regional pool
                        1. some objects are memory heavy, but load access bandwidth.
                           multiple clusters can share one pool of this objects, rather than duplicate FE Memcached
                        2. this is also a good example, why "pool" is a necessary design concept
                    6. upgrade and cold cluster warmup
                        1. allocate memory in shared memory pool, or serialize data to shared memory pool. so that upgrade kill process won't lose mem data
                        2. "cold cluster" clients can retrieve data from "warm clusters"
                5. grow to cross geo-regions
                    1. cross region write consistency
                        1. MySQL master is at master region. MySQL replica is at remote region. Memcached is viewing MySQL replica
                        2. When remote region Client writes, it 1) write to MySQL master 2) set Remote Marker at Memcached
                           the Remote Marker means: new data is at MySQL master, MySQL replica has stale data, don't cache for MySQL replica
                        3. race operation may incorrectly delete the Remote Marker, but OK for the inconsistency

    6. The CacheLib Caching Engine: Design and Experiences at Scale (Facebook)   [OSDI-2020, 15 refs]
       https://www.usenix.org/conference/osdi20/presentation/berg
        1. good example how a unified general purpose product can be better than specialized ones. opensourced.
           most writing are about why Facebook needs it, few about LOC, too few about SOC. But good as SOC is written detailed in Kangaroo paper
        2. highlight
            1. architecture
                1. DRAM -> LOC or SOC on flash.
                1.5. DRAM uses a chained hash table. slab mem allocation. each slab class size can be configured to match workload 
                2. LOC: Cache >2KB objects. B+-tree index at DRAM, append pages at flash.
                    1. object size can be inferred from where they store at flash, no need to occupy DRAM
                    2. writes are page level, eviction are entire region level 
                3. SOC: Cache <2KB objects. Set-associate caching at flash, like FlashCache
                    1. use 8B BloomFilter for each set to tell key in or not
                    2. admitting an object needs rewrite entire 4KB page, bad write amplification, bad random writes 
                    3. Compact cache: compact objects with same key size and object size in a single cache line
                4. compare to peer products
                    1. Memcached lacks support for data structures
                    2. Redis lacks support for flash
                    3. FlashCache lacks support for Negative Caching and data structures
            2. why need a unified general purpose cache
                1. saves 10Ks lines for duplicate code
                2. a shared bad for devs to develop, add features, and improve stability
                3. an aggregation point for optimization and best practices
                4. more importantly, CacheLib outperforms existing Facebook caches: CDN, KV (LookAside), Social Graph, Storage
                   Note database page buffer, e.g. RocksDB's, are not applicable for CacheLib
                5. in Facebook, no service has a more than 25% of total cache space
            3. why existing academic cache test workload is not enough (Figure 3-6). good useful part.
                1. Popularity: Zipf is not enough. SocialGraph and CDN has low Zipf a value. Storage is not Zipf
                2. Churn: YCSB assumes there is no churn. However Facebook workload changes rapidly with time
                3. Size variability
                4. Bursty: Poisson arrival sequence is not enough. Figure 6 shows there are many spikes not captured
            4. Negative Caching
                1. SocialGraph, 55.6% requests are for key that doesn't exist. SocialGraph relies on delete to maintain cache consistency
                2. When delete a key, i.e. now an empty key, RocksDB only adds marker. The next GC cleans up the key value. So an empty key has cost here
                   SOC evicts a key but rewrite entire page. an empty key has no cost then. This saves cache capacity.
                   the bad part is, flash cache is much more frequently rewritten compared to normal storage, harming flash endurance
            5. future directions
                1. better resource-management policies (e.g., eviction/admission policies, memory management)
                2. emerging hardware platforms (e.g., FPGA acceleration, non-volatile memories, zoned-namespace SSDs)
                3. novel application features (e.g., as seen in negative caching)
            6. others
                1. Engineers provision caches to equalize the marginal cost of the next by DRAM with the marginal benefit of the ensuring increase in hit ratio
                2. CacheLib explicitly gather features about objects beyond their DRAM-cache lifetime. We use Bloom filters to record the past six hours of accesses
                    1. this is interesting .. using BloomFilter to track accesses

    7. Kangaroo: Caching Billions of Tiny Objects on Flash (Facebook, Microsoft)    [SOSP-2021-Best Paper Award,  best paper]
       https://www.pdl.cmu.edu/PDL-FTP/NVM/McAllister-SOSP21.pdf
       https://saramcallister.github.io/files/sosp2021-mcallister-slides.pdf
        1. very good paper. Opensourced as CacheLib mod. CacheLib SOC reveals little detail but we can refer to Kangaroo.
           Reference design for caching 100B small objects. The key is to batch input requests with log first. 
           In appendix very good modeling for cache states and miss ratio, can be reused as a reference
           Facebook does have long track to develop memory caching: memcached, flashcache, CacheLib, Kangaroo
        2. highlights
            1. architecture
                1. DRAM -> KLog -> KSet
                2. KLog: DRAM index + log append writes
                    1. KLog uses 5% flash capacity. it's hash index, where the slot maps to a KSet. hash collision means objects map to same KSet
                    2. partitioned index - very good optimization
                        1. 64 partitions * 2^20 tables -> 16byte offset to index an object.
                        2. in this way, object index and pointer use less bits.
                           DRAM is saved for indexing object.
                           it's also how CPU cache saves index bits (tags and offset)
                    3. flushing to KSet is done by one consecutive segment each time.
                       each object's peers in same KSet are looked up, only flush to KSet if there are >= n objects in the KSet.
                       otherwise discard. but popular objects are re-admitted into KLog
                3. KSet: Set-associative caching, no DRAM index
                    1. RRIParoo - based on RRIP cache replacement policy
                        1. RRIP is an LRU, but using only 3 bits per object. (like Linux LRU). Change bits when 1) object is accessed 2) or no to-evict object is found
                        2. in RRIParoo, the 3-bit is at flash with each object. in DRAM, only 1 bit is needed to track whether object is read
                        3. eviction happens when object insertion
                            1. question: how to handle user explicit delete an object, which is a frequent usecase at SocialGraph?
                    2. From Figure 12
                        1. miss ratio is majorly related to RRIP policy
                        2. what KLog does is to reduce write amplification 
            2. comparing different flash cache architecture
                1. Log-structured cache: 
                    1. example: CacheLib LOC, KLog, Linux BCache, Flashield
                    2. writing objects sequentially and batching many insertions into each flash write
                       need DRAM index to tell where those objects are
                       advantage: 1x write amplification, sequential writes
                       problem: an object can be located anywhere on flash, thus you need a huge memory index, no feasible for many small objects
                                and cost per bit continue to decrease faster for flash than for DRAM
                2. Set-associate cache
                    1. example: FlashCache, CPU cache
                    2. if you don't want DRAM index, you need to limit where an object can be on the flash, i.e. set-associate
                       advantage: no DRAM index
                       problem: any new write to flash needs to rewrite entire set, big write amplification
                3. RocksDB / KV-Store
                    1. they are designed for storage, rather than cache.
                       KV-Store generally assumes deletions are rare, deleted value are kept until marker GCed.
                       thus wasting capacity, compared to Facebook SocialGraph which heavily relies on deletes, and requires Negative Caching
                    2. example: Netflix used RocksDB as a flash cache and had to over-provision by 67%
                4. Log-structured cache with coarse-grain objects
                    1. question: didn't see paper mention about batching small objects into a larger index unit?
                                 but this should also be bad, as updating the index unit needs worse write amplification
            3. key workload and why DRAM + flash for caching
                1. workload: Facebook SocialGraph, Twitter tweets, Azure sensor data. reference object size is 100B
                    1. question: ClientLib paper says SocialGraph has many deletes, I didn't see how deletes are handled more optimally in Kangaroo?
                    2. the challenge of caching many tiny objects is the huge metadata structure in DRAM
                2. why only DRAM cache? DRAM is expensive and demanded by many other services.
                   why flash? cheaper, large capacity, power efficient than DRAM
                   challenge: flash wear out are faster in cache than storage, due to many deletes
            4. modeling and analyzing the cache insertion amplification - very good part, see Theorem 1 and Appendix
                1. Concept: device level write amplification - DLWA. FTL mapping, erase blocks, GC
                            application level write amplification - ALWA. what Kangaroo introduces and controls
                2. Modeling: Markov, see Appendix
                    1. First, use Markov model to cover the transitions of a single object, cached / not cached
                    2. Clever definitions
                        1. per object being request probability is defined as ri
                        2. how many objects are in a batched write to KSet, is modeled by Binomial distribution
                        3. use stationary probability to study miss ratio after the cache is warmed stable
                    3. key results
                        1. after added KLog state, the miss ratio is same with baseline (need minor approximation)
                        2. after added threshold admission policy, the miss ratio is still same with baseline (need approximation)
                        3. write amplification is reduced each step by step
                        4. questions
                            1. where is the miss ratio formula for probabilistic admission policy?
                            2. shouldn't miss ratio be a direct result of how large is your cache? so it is expected these miss ratio formulas are same, unless cache policy is really bad

    8. Flat Combining and the Synchronization-Parallelism    [2010, 364 refs]
       https://www.cs.bgu.ac.il/~hendlerd/papers/flat-combining.pdf
       https://bholt.org/pubs/holt-pgas13-slides.pdf
        1. mentioned in CacheLib paper as "higher throughput is largely due to optimizations that reduces lock contention .. Flat combining"
           very good paper. a new fundamental concurrency design pattern break through from fine-grain locking / partitioning / lock-free / share-nothing.
           new data structure applicable to counters, queues, lists, stacks, etc, v.s. their lock-free version
        2. highlights
            1. what is flat combining
                1. each threads write its requests in thread local - publication list
                   all threads compete for a global lock with CAS, only one thread pass - the combiner thread
                   the combiner thread fetches requests from publication list, batch execute at the data structure
                   the combiner thread return results to publication list of each thread local
                2. flat combining is linearizable.
                   applicable to manycore / high concurrency level, where 1) CAS synchronization cost 2) and batched operation speedup, outperforms parallelism
                3. why flat combining is faster
                    1. 1) CAS synchronization cost of lock free, 2) and batched operation speedup
                    2. no all-thread-to-one access to a shared memory location in spin lock (at each publication list request)
                    3. the global CAS local doesn't need every thread to pass
                    4. batched sequential access and cache effective

    9. Minos: Size-aware Sharding For Improving Tail Latencies in In-memory Key-value Stores    [2019-NSDI, 42 refs]
       https://www.usenix.org/conference/nsdi19/presentation/didona
        1. mentioned in CacheLib paper as "the computational overhead of retrieving the size of objects stored on flash is too high to use size-aware sharding in practice"
        2. highlights
            1. problem to solve: small request high Q99 latency, due to head-of-line blocking by a large request.
                                 or Convoy effect, i.e. burst of large requests may take most cores
            2. solution: shard requests to different cores by their size. reserve some cores for small items. 
                         hardware dispatch for small items. adapting the number of cores to handle small vs large items.
            3. hardware dispatch
                1. small cores directly reads small requests from NIC by polling. Minos dispatch only large requests
            4. adapting number of cores
                1. by observing request count and request size
            5. implementation
                1. DPDK, UDP

    10. Could cloud storage be disrupted in the next decade    [2020-hotstorage, Best Presentation Award Finalist, Microsoft Research, 6 refs]
        https://www.usenix.org/conference/hotstorage20/presentation/chatzieleftheriou
        1. mentioned in CacheLib paper as "New flash technologies, such as multilayer QLC (four bits per cell) and PLC (five bits per cell) [28], increase capacity and decrease cost but significantly reduce write endurance"
        2. highlights
            1. S-Curve
            2. Cloud-First Storage Design, disaggregation
            3. DNA storage, Silica

    11. Flashield: a hybrid key-value cache that controls flash write amplification    [2019-NSDI, 24 refs]
        https://www.usenix.org/conference/nsdi19/presentation/eisenman
        1. Mentioned in CacheLib paper "CacheLib was updated to include a more advanced admission policy, similar to the Flashield policy", "Flashield would need 75 GB of DRAM to track 2 TB of 100 B objects"
           log-structured cache. optimized DRAM index reducing memory. ML SVM predict for whether flush to flash.
           targets reducing write-amplification, as flush can be quickly worn out using as cache
        2. highlights
            1. architecture
                1. DRAM index + append to flash, evict on flash by large segment
                2. Filter: Machine learning - SVM (reads#, updates#) to predict future access, to determine worth to put to flash
                3. RIPQ cache replacement policy
            2. key designs
                1. reducing DRAM in index
                    1. 19 bit per object. CLOCK algorithm for LRU. hash the key. bloomfilter indicates key exist on segment
                    2. index is a hashtable

2. Readings: recent papers
    1. Constructing and Analyzing the LSM Compaction Design Space    [VLDB 2021, 2 refs]
       http://vldb.org/pvldb/vol14/p2216-sarkar.pdf
        1. useful work for 1) how to analyze design space of a popular technology 2) how to construct experiments and do evaluation
           3) Table 1 lists known LSM engines and how they combine the design space. Figure 1 shows the perf results
        2. highlights
            1. evaluation space
                1. metrics: write amplification, write throughput, point and range lookup performance, space amplification, and delete performance
                2. technique space of LSM compaction
                    1. the compaction trigger: level saturation, #sorted runs, file staleness, space amplificaiton, tomestone-TTL
                    2. the data layout: leveling, tiering, 1-Leveling, L-Leveling, hybrid leveling (Dostoevsky)
                    3. the compaction granularity: Level, sorted run, File single/multiple (partial compaction)
                    4. the data movement policy: Round-robin, Least overlap (+1), Least overlap (+2), Coldest file, Oldest file, Tombstone density, Expired TS-TTL, N/A (entire level)
                3. workload types
                    1. size of ingested data
                    2. proportion of ingestion and lookups
                    3. proportion of empty and non-empty point lookups
                    4. the selectivity of range queries
                    5. fraction of updates and delete
                    6. the key-value size
                    7. the workload distribution (uniform, normal, and Zipfian)
            2. evaluation methods and results
                1. method: unify all techniques into a codebase, built into RocksDB. evaluate on AWS EC2 VM
                   YCSB benchmark + insert benchmark + self modify, workload generator published on Github
                2. tune to capture compaction numbers
                    1. assign compactions a higher priority than writes
                    2. enable direct I/Os for both read and write operations
                    3. limit the number of memory buffers (or memtables) to two (one immutable and one mutable)
                    4. set the number of background threads responsible for compactions to 1
                3. useful observations
                    1. Tiering may cause proloned write stalls (cascading compaction)
                        1. this should be some paper to optimize
                    2. with Tiering, theoretically, lookup cost should be Tx higher than leveling
                       but fact lookup is much faster, because of caching and bloomfilters
                    3. the impact of compaction policy to range scan is marginal, what matters is total sorted run count
                    4. for ingestion-only workload, the data distribution doesn't matter, whichever compaction strategy is used
            3. others
                1. A range scan requires sort-merging the runs qualifying for a range query across all levels of the tree
                2. A delete is eventually considered as persistent once the corresponding tombstone reaches the last tree-level, at which point the tombstone can be safely dropped
        3. questions
            1. the capacity amplification is only minimally evaluated, however which is important to cloud COGS
                1. and how long a deleted / updated key to reclaim the space?
            2. hope to see the evaluation of burst deletion scenario, as in some customer behaviors
            3. from Figure 1. RocksDB is worse in all aspects to many LSM engines ..
               Lethe engine (from same paper author) performs pretty well
            4. the paper didn't mention much about on to handle the VM perf stable issue on AWS EC2
                1. see paper "An Inquiry into Machine Learning-based Automatic Configuration Tuning Services on Real-World Database Management Systems"
                   the "noisy cloud environment"
            5. in future, possible to ML auto tune LSM products?
            6. the paper evaluation prepare data for compaction by ingesting dataset into LSM engine
               but the LSM engine nowadays should support like compacted ingestion / ingestion + compact combined
               how's that perform?
            7. how is the VM workload, mounted disk workload (block), blob workload, and how it performs with aging data / "fragmentation"
               and how point lookup / range look perform on old vs new data?

    2. Citus: Distributed PostgreSQL for Data-Intensive Applications    [2021, 0 refs]
       https://dl.acm.org/doi/pdf/10.1145/3448016.3457551
       https://github.com/citusdata/citus
       https://docs.microsoft.com/en-us/azure/postgresql/hyperscale/
        1. Citus is Azure Database for PostgreSQL. implemented as a PostgreSQL plugin
        2. highlights
            1. Citus is Azure Database for PostgreSQL. implemented as a PostgreSQL plugin, extending it by UDF, planner/executor hooks, user code in separated process, etc
            2. target workload: Multi-tenant, realtime analytics, high-performance CRUD, data warehousing
                1. Table 2 gives useful summary on which feature is needed for each workload
            3. architecture
                1. postgresql as central coordinator, postgresql as worker nodes
                2. when small, the postgresql coordinator can also be used to store data
                3. to scale out the coordinator, it can be pushed to worker nodes. i.e. each worker node assumes itself as a coordinator to take all distributed queries
                4. tables are hash partitioned, and more range partition for advanced use
                   tables co-location are automatic with key hash
                   reference table won't be sharded, but replicated to each node
                5. a shard rebalancer role to auto balance data according to cluster size
                    1. question: seems it would track shard placement metadata and track the migration states and select src/dest
                6. 2PC for distributed transaction, and no prepare just commit for single node transaction
                   data co-location makes more likely single node transaction
                7. a distributed deadlock detector to poll and kill cycle edges. wound-wait is unsuitable for Citus
                8. no distributed snapshot isolation support, not like Spanner, CockroachDB
            4. related work
                1. Vitess [12] is a sharding solution for MySQL
                   Unlike Citus, it is not an extension and therefore must be deployed separately
                2. TimescaleDB [11] is a PostgreSQL extension that optimizes PostgreSQL for time series data
                   currently incompatible with Citus due to conflicting usages of PostgreSQL hooks

    3. Greenplum: A Hybrid Database for Transactional and Analytical Workloads    [VLDB 2021, 1 refs]
       https://arxiv.org/pdf/2103.11080
        1. how Greenplum supports OLTP based on it's a row-wise in memory, column-wise in disk layout. the main changes is improving locking performance and deadlock detection, and resource isolation for co-running OLTP with OLAP
           I didn't see replication to extra copy of OLAP/OLTP favor layout, like what TiDB or F1 lightening did
        2. highlights
            1. related work, how popular DBs choose their paths to HTAP
                1. From OLTP to HTAP Databases
                    1. Oracle Exadata: a smart scale-out storage, RDMA and infiniBand networking, and NVMe flash to improve the HTAP performance
                                       column-level checksum with in-memory column cache and smart OLTP caching
                    2. Amazon Aurora - cloud OLTP. a features parallel queries to push down OLAP to thousands of CPUs
                2. From NewSQL Databases to HTAP Databases
                    1. TiDB introduced TiFlash, a new paxos replica to favor OLAP columnar format
                        1. Similarly, traditional OLAP databases (e.g., Vertica [14]) also use write-optimized stores (WOS) to handle insertion, update, and deletion queries.
                    2. F1 Lighting [26] offers “HTAP as a service”. In Google, Lighting is used to replicate data from OLTP databases such as Spanner and F1 DB, convert those data into column format for OLAP workloads. Unlike TiFlash, Lighting provides strong snapshot consistency with the source OLTP databases
                3. Greenplum adds OLTP capability to a traditional OLAP database, and also supports a fine-grained resource isolation
            2. key approaches
                1. Greenplum traditionally supports append-optimized column-oriented tables, the problem is 2PC commit poses performance penalty for OLTP only update a few tuples
                    1. Greenplum supports data tiering as 1) Heap (append-optimized row-oriented AO-row), 2) Months older (append-optimized column-oriented AO-column), 3) years older (external HDFS, S3).
                2. Greenplum is based on PostgreSQL. user is able to choose different optimizers for OLAP vs OLTP (Orca)
                3. Table 1 show Greenplum lock types. too heavy for OLTP. For OLTP, Greenplum relax locking to allow concurrent writes.
                   it further introduces the need of a global deadlock detection algorithm
                    1. The algorithm keeps removing waiting edges that might continue running later. When no more waiting edges can be removed, if there are any remaining waiting edges, then global deadlock might happen
                4. for 2PC transactions, the OLTP improve is to use instead one-phase commit, if data resident on an exactly one segment
                5. resouorce isolation
                    1. problem: OLAP workload co-running has heavy impact on OLTP workloads
                    2. CPU isolation is implemented based on cgroups.
                        1. question: so new query is by forking new processes? or group user into processes?
                    3. memory management by Vmemtracker. memory cannot be released immediately even exceeds limit. resource group introduces three layers to manage
                        1. The first layer is enforced on slot memory, which controls the memory usage of a single query in a group
                        2. The second layer is enforced on group shared memory, which can be used by the queries in the same resource group when they overuse the slot memory
                        3. The last layer is global shared memory, which is the last defender of memory usage among different groups
                        4. if all three layers fail, query cancel is triggered
                    4. in future, a workload prediction module, to allow a query to use more memory when the prediction of incoming workload is not heavy, even when the concurrency number of the resource group is set to be large
                    5. question: and how to resource isolation / limit the disk IO and network IO?
                        1. currently, throttling CPU usage can limit the usage of disk and network IO as well
        n. related materials
            1. Greenplum: A Hybrid Database for Transactional and Analytical Workloads
               https://zhuanlan.zhihu.com/p/391568439

    4. Bringing Decentralized Search to Decentralized Services    [OSDI 2021, 0 refs]
       https://www.usenix.org/conference/osdi21/presentation/li
       https://github.com/SJTU-IPADS/DeSearch
        1. DeSearch: the first decentralized search engine, like Blockchain apps. no central censor, verifiable, private search. no dependency to central search enginne corperations. scale horizontally with the number of workers.
           very good. the innovative work is potentially industry disruptive
           Figure 1: shows decentralized BlockChain solution vs each of the Centralized IT roles
            1. very interesting, very useful
        2. highlights
            1. problem of centralized search vendors: opaque censorship, bias listing
            2. architecture: decouple search engine into
                1. naive design but not taken
                    1. BlockChain app using Smart Contract
                        1. no .. they are too slow
                2. storage - states with HA
                    1. ingest & lock data source via blockchain and IPFS
                    1. global Kanban, data commited to it will lock hash on Blockchain
                    2. Crawlers will append data and its witnesses on Kanban
                3. computation - stateless
                    1. Indexers will use the data on Kanban to generate indexes and witnesses
                    2. computations are broken into short-lived Lambda, it is p2p and tolerates node unavailable
                        1. Lambdas are executed in TELL (e.g. Intel SGX)
                    3. Queries uses the indexes to provide search for clients
                    4. the Client can verify results by checking witnesses
                        1. as the process of verification can take hours long, DeSearch offers dedicated Verifiers
                4. verification
                    1. Witness, remove verification from lambda's fast paths. publich dataflow proofs.
                    2. <[Hash(Input)], Hash(Function), Hash(Output)>_signed
                    3. for each search pipeline, every Lambda generates a Witness
                       Witness records the causality between input and output, as then organized as the Witness Tree
                       The Witness Tree can be easily traced from root to leaves to learn if the covering items are complete
                    4. "verifiable lambda" - interesting new concept
                    5. need concept "epoch" to define data completeness.
                       verifier also cut verify work completeness by epoch
                        1. epoch snapshots and its digest hash is committed to BlockChain, provides "epoch-based data integrity"
            3. private search
                1. equalizing all message length
                2. execute with SGX + Circuit-ORAM
            4. evaluation
                1. Datasets: Steemit, OpenBazaar
                    1. Steemit - a blockchain-based blogging and social media website
                    2. OpenBazaar - a protocol for e-commerce transactions in a fully decentralized marketplace
                2. 1300+ t2.medium AWS EC2 instances, 2core 4GB RAM.
                3. latency < 50ms for single latency. throughput > 1500 req/sec
                    1. except ORAM reduces throughput to ~200 req/sec because no concurrency supported. and greatly increases latency
        3. questions
            1. what if the ingested source data into Kanban is initially poisoned?
            2. I thought IPFS is to store the states. but how come to use Kanban?
            3. the architecture is huge, but would be useful to see more details in each part
            4. "Masters hold the root key that serves as the identity of the DESEARCH system"
               How is Master role designed to be decentralized and verifiable? not mentioned in slides
            5. how fast is the client to traveral the verification tree and do verification upon a search result? - slow, needs to offload to Verifier
            6: exactly .. what's the root and chain of trust in this system? especially for witness
        n. related materials
            1. decentralized search engine - Presearch
               https://techcrunch.com/2019/04/27/how-a-blockchain-startup-with-1m-users-is-working-to-break-your-google-habit/
            2. Blockchain-Based Search Engines: All You Need to Know
               https://www.technology.org/2019/12/28/blockchain-based-search-engines-all-you-need-to-know/
            3. decentrailized search engine - Hacker news
               https://news.ycombinator.com/item?id=25717106

3. Readings: Kafka transactional messaging / transactional stream processing
    1. Consistency and Completeness: Rethinking Distributed Stream Processing in Apache Kafka
       https://www.confluent.io/blog/rethinking-distributed-stream-processing-in-kafka/

    2. Exactly-Once Semantics Are Possible: Here’s How Kafka Does It
       https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/
        1. Idempotency enables effective exactly-once processing
           Offset / sequence number used to dedup from at-least-once
        2. Atomic multi-partition writes

    3. Transactions in Apache Kafka
       https://www.confluent.io/blog/transactions-apache-kafka/

    4. The original design doc: Exactly Once Delivery and Transactional Messaging in Kafka
       https://docs.google.com/document/d/11Jqy_GjUGtdXJK94XGsEIK7CP1SnQGdp2eF0wSw9ra8/edit

    5. Consistency and Completeness: Rethinking Distributed Stream Processing in Apache Kafka    [2021, 1 refs]
       https://assets.confluent.io/m/2aaa060edb367628/original/20210504-WP-Consistency_and_Completeness_Rethinking_Optimized_Distributed_Stream_Processing_in_Apache_Kafka-pdf.pdf?mkt_tok=NTgyLVFIWC0yNjIAAAF_bB9hFMsmxnBiFp4ikCINGM_cs9bliy-QEdE0LxAKYTehJTvtswu-z5jn6uewJkSvkMgmOqdtF_EC_mDs89Sc-3jQ-0D-_oaaHQn3C6Ow6iyxvKE
        1. good paper, brings into realization of transactional streaming and stream first-clase database.
        2. highlights
            1. kafka architectures
                1. consumer group: topic stream is partitioned across consumer group, load balancing is automatically handled
                2. record's offset, vs logical event time
                3. ksqlDB ingests data streams from kafka, and applies continuous query that derive new streams or materialized views
                4. Operators within a sub-topology are effectively fused together
                   These repartition topics serve as linearized, durable, fault-tolerant channels of communication between sub-topologies
                5. tasks can be independently paused, resumed, and migrated between instances
                6. Optimizations are also applied in Kafka Streams when generating the topology
            2. consistency, exactly-once
                1. kafka logs record into persistent logging. logs are replicated in n replica. leader node to maintain replication consistency. leader can failover.
                2. record is tagged with sequence number, replay is idempotent
                3. transaction support when writing record to multiple nodes. by prepare-commit 2PC, with a dedicated coordinator to track transaction state/commit. Coordinator is also persisted in log stream and partitioned
                    1. coordinator bumps epoch to fence of other zombie coordinators (dead but thinks itself still working)
                       this is an alternatives to the lease-wait approach
                    2. atomic read-process-write. the read offset is also part of the transaction. the aborted transaction can be replayed, idempotently.
                4. performance
                    1. question: figure 3, what .. exactly-once enabled the latency is ~100ms? while the at-least-once latency is ~1ms or less ..
            3. completeness
                1. kafka approach: revisions, the time-evolving table. with a grace-period per operator to config how long it waits for delayed records
                2. alternatives: micro-batches. operator waits for a delay window, and reorder inside the window
                3. alternatives: ppunctuation records. insert special records in stream, to indicate low-watermark, e.g. Dataflow, MillWheel
            4. determinism
                1. in kafka, users can achieve determinism if they enable exactly-once processing mode and do not specify non-deterministic processors

4. Readings: Storage Field Day, and Vision of next 3 years
    1. Actifio Architecture Overview
       https://www.youtube.com/watch?v=6Dh0lkMBgsk&list=WL&index=17

    2. Data Storage Research Vision 2025 - NSF Visioning Workshop
       https://www.ece.iastate.edu/~mai/docs/papers/2018_DataStorage2025.pdf
        1. very good, this is key what I need to understand storage visions
        2. highlights
            1. tracks: (1) Storage for Cloud, Edge, and IoT Systems; (2) AI and Storage; (3) Rethinking Storage Systems Design; and (4) Evolution of Storage Systems with Emerging Hardware
            2. interesting lines
                1. 1) Efficient systems. 2) Unified systems. 3) Specified systems. 4) Elastic systems. 5) Explainable systems. 6) Sharable systems. 7) Application-driven systems. 8) Reliable systems. 9) Re-evaluable systems.
                2. Edge and its Impact on Cloud
                3. Storage for AI. AI for Storage
                4. Workload classification. Characterizing workloads across layers
                5. Rethinking Storage Systems Design
                    1. trends
                        1. IoT and exascale High Performance Computing (HPC) clusters are both on track to produce a torrent of data far greater than the storage and network capacity of current systems.
                        2. The rapid growth of data science is introducing new workloads with unique storage access patterns and performance demands.
                        3. Current storage systems with minimal schemas are poorly equipped to organize huge amounts of data, especially when the growth in data size is projected to be exponential in nature.
                        4. Emerging storage technologies, such as DNA [34] and glass [74] storage, and storage-class memory, require rethinking the entire storage hierarchy from applications to hardware.
                        5. Privacy and security increasingly require methods to reason about the relationships among data being stored, as well as the provenance and lineage of the data
                    2. response to trends
                        1. greater introspection into their operation and the data they store
                        2. more tightly integrate computation (e.g., indexing, aggregation, transformation) with data generation and movement through the storage stack, effectively enabling “in-situ” and “in-transit” processing of data
                        3. reconsider the fundamental design of the POSIX interface to support emerging storage technologies
                        4. tighter co-design of applications and storage
                6. Evolution of Storage Systems with Emerging Hardware
                    (1) Memory and storage devices
                    (2) Network fabrics
                    (3) Processor architecture
                    (4) Applications
                7. Operating System and Application Development Support
                    1. Distributed architecture
                    2. Software support
                        1. Transparent global naming
                        2. Transaction management
                        3. Reliability and availability
                        4. Consistency and coherence
                        5. Crash resilience and durability
                        6. Metadata management

5. Misc: Readings: Azure VFP
    1. VFP: A Virtual Switch Platform for Host SDN in the Public Cloud     (NSDI 2017, 111 refs)
       https://www.usenix.org/system/files/login/articles/login_fall17_02_firestone.pdf
       https://www.usenix.org/system/files/conference/nsdi17/nsdi17-firestone.pdf
        1. Azure large scale to handle SDN needs. VFPv2 in 2013. good paper.
           interesting as compared with OpenFlow/OVS. e.g. stateful connection based MAT, flow compile and caching, non-interrupting upgrade and migration, smart NIC / SR-IOV / FPGA offloading
        2. highlights
            1. cloud usecases
                1. virtual networks with customer supplied addresses
                    1. VFP based on VL2
                2. scalable L4 load balancers
                    1. VFP by Ananta
                3. security groups and ACLs, virtual route tables
                4. bandwidth metering and QoS
            2. compare with OpenFlow and Open vSwitch
                1. more than one controllers program the virtual switch
                2. stateful connection based classification, rather than stateless packet based
                3. programmable encap/decap matching conditions. MAT model
                    1. Action Contexts: hooks to implement custom logic, e.g. metering counters, via callback, besides the standard HTs
                4. frequent deployment/updates without interrupting VM connectivity for stateful flows
                    1. pause the data path < 1s, unload kernel drive (the VFP), install new VFP
                       to restore states, states are serialized ten deserialized before/after upgrade
                    2. support VM live migration
                         1. in a short VM blackout period, the rules are serialized and deserialized to apply to dest host
                5. high packet rate when many rules, e.g. 40G+ NIC on 10+ flow tables
                    1. compilation of flow actions
                    2. flow caching
                6. offload flow policy to programmable NIC, SR-IOV, FPGA (Catapult?)
            3. flow compilier, a central packet processor, learned from ASIC pipeline
                1. parse and act on packet metadata, only touch packet data in the end
                2. FlowID - Header + fields
                   UFID - all FlowID of a packet
                   Header Transpose Action: Match header and perform Pop/Push/Modify actions (HT)
                   Caching & compiling - actions for a UFID is relatively stable, cache UFID with resulting HT - Unified Flow Table

    2. Ananta: Cloud Scale Load Balancing   [SIGCOMM 2013, 290 refs]
       http://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p207.pdf
       http://conferences.sigcomm.org/sigcomm/2013/slides/sigcomm/19.pptx
        1. Mentioned in Azure VFP paper, control plan (not scalable) + MUX (router ECMP scalable) + host agent offloading
           VFP should be using at host agent. good part of Fastpath - intra DC traffic bypass LB via host agent offloading
           supports DSR, and with NAT across layer 2
           reminds of Google Maglev (2016), control plan also scalable runs on "MUX" with metadata sharded by consistent hashing
        2. highlights
            1. Fairness
                1. Each Mux keeps track of its top-talkers,
                   When packet drop happens, Ananta Manager withdraws the topmost top-talker from all Muxes
            2. Reliability
                1. When Ananta Manager fails - Paxos provides fault-tolerance by replication
                2. When Mux fails - 1st tier routers detect failure by BGP
                   The routers stop sending traffic to that Mux
                    1. Detection of MUX failure takes at most 30 seconds (BGP hold timer). improve?
            3. others
                1. preserve ordering of packets?
                2. ECMP - Equal-Cost Multi-Path Routing - Hash packet header and choose one of equal-cost paths
            4. scale out
                1. tier 1 router uses ECMP to spread packets to MUX
                2. an agent in each host for packet modification
                     1. MUX sends via an IP-in-IP protocol to host, the host agent unpack and send it to VM
                        host agent remembers NAT states, when VM sends response packet, host agent does DSR
                     2. the host agent is probably what VFP does
                3. direct server return (DSR) + NAT across layer 2. No out bound traffic passes through MUX
                4. FASTPATH
                    1. traditional Clos (VL2) DC net arch, intra DC traffic needs to go through LB. FASTPATH bypass it
                    2. the first packet goes through LB, then routing info passes to host agent, following packets bypass LB via host agent rewriting
```
