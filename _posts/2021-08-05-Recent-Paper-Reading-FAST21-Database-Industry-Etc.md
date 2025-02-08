---
layout: post
title: "Recent Paper Reading: FAST21, Database, Industry, Etc"
tagline : "Recent Paper Reading: FAST21, Database, Industry, Etc"
description: "Recent Paper Reading: FAST21, Database, Industry, Etc"
category: "Paper Reading"
tags: [storage, paper, database]
---
{% include JB/setup %}

Search good / (very) interesting / (very) useful, to find recommended papers. Search "question" to find feedback.

Industry papers.

```
1. Helios: Hyperscale Indexing for the Cloud & Edge (Microsoft)    [2020, 2 refs]
   http://www.vldb.org/pvldb/vol13/p3231-potharaju.pdf
    1. good. new direction to build global scale secondary index, eventual consistency, with log is the system/database principles.
       Hyperscale to index 10s of PBs of logs per data for debugging Cosmos/ADL and monitoring & alerting
    2. highlights
        1. log is the system / log is the database
            1. the key idea is to use a replicated log to build the global secondary index
                1. log is the single source of truth of raw index data
                   log is where the data handles durability / persistence
                    1. the alternative design not choosen here, which is traditional, is to use distributed transaction to group data update + index update
                    2. Helios approach is quite different from how other distributed DBs build secondary index
                        1. traditionally, usual approach: 1) global index bound with distributed transaction to data updates
                             2) local index, bound to each local data partition. it only needs local transaction. but a index lookup needs to query all partition's local index.
                2. on-disk and in-memory structure to translate logs into read favorable format
                    1. Figure 6 the LSM-tree on-disk compact layers, but key differences are
                        1. there is no sort order maintained
                            1. question: it seems the Helios index only handles point lookup but no range scan?
                        2. the higher level (most bottom and compacted layer in LSM-tree) is used to start query
                            1. question: there should be many history data left in Level 2 in Figure 2. Level 2 is not really "small", how is read handled efficiently?
                        3. not like LSM-tree data flows from memory to disk
                           Helios the data flows from source -> logs -> on-disk compacting -> Level >=2 higher -> small enough to keep in memory
                            1. question: funny that this paper didn't give evaluation results about index access latency .. which means potentially the architecture maybe has relatively higher latency accessing such many layers of index files
                3. GC and data comaction
                    1. the paper defined primitives, "Add" and "Merge" to build the index structure
            2. another alternative design not choosen is, sync by page or sync by log
                1. relates to
                    1. 华为Taurus云原生数据库论文分析
                       https://zhuanlan.zhihu.com/p/151086982
                    2. And the Aurora Multi-master
                2. for DB, besides logging, it must maintain a read favorable copy of data. it can be combined with snapshots / checkpoints. how to update it efficiently?
                    1. option 1: sync from pages in memory to disk. this is how traditional DB handles it. and there is "steal, no force" techniques.
                    2. option 2: log is the system / log is the database.  We only pass logs as the source of truth and the durability in the system, no page sync.  Logs only hold delta info, more efficient, unlike page sync where unchanged data in page also introduces IOs.
                        1. this design is naturally more close to LSM-tree familiies
        2. new opensource / system directions of building a separated large scale index service
            1. "stream" maps to the logging oriented design here. it naturally can work with streaming systems and IoT
            2. How to handle consistency if index is separated? Helios uses eventual consistency
                1. Index is only eventual consistency with the data. Data parts are NOT managed by Helios. the versioning is the timestamp
                2. per versioning: Helios supports read commited and read snapshot
                    1. question: consistent snapshot cannot be supported? Support data Tx has read 1 and read 2 but ingested into Helios in two different timestamp version
                       as a result, you cannot read such consistent snapshot from Helios read suppoorts
            3. Figure 6 the index structure, data freshness, watermarks
                1. log contains the most latest data, Level 0 less fresh, .. Level 2 most stale
                   watermarks are used to mark the data version at each level different
        3. Data source side, agents - pushing to the "Edge" (computing)
            1. the agents run on customer machine which generate data
               it uses customer machine CPU/mem to aggregate, parse, build index first
               the cpu/mem consumed is throttled
            2. Key production workload: Azure Cosmos/ADL to collect 10s of PBs log data per day, Helios index them. in production for last 5 years
                1. and related debugging search point lookup
                2. and incidents management, alerting, and monitoring & reporing queries
                3. internally classfied as Ring-0 debugging services
        4. GDPR
            1. "Forget Me" button, that Heios indexes all user data positions which to be deleted
        5. Others
            1. sharding policy: first by hashing, then intra zone by ranged based tree
            2. the global index is optimized for workload that is write Heavy
                1. yes .. think about how debugging logs are used ..
            3. use URI to locate data blocks being indexed to
            4. query optimizer from external systems can do cost-based index access path selection
                1. interesting here, the Figure 6 index structure also poses need to select how to travseral through index at different paths with a cost-based selection
            5. integrate Apache Spark with no changes to its optimizer/compiler
                1. and, how to support batch processing in the same streaming system? i.e to deprecate lambda architecture
    n. related
        1. the morning paper - Helios paper
           https://blog.acolyer.org/2020/10/26/helios-part-1/
           https://blog.acolyer.org/2020/11/02/helios-part-ii/

2. FoundationDB: A Distributed Unbundled Transactional Key (Apple)    [2021, 1 refs]
   https://www.foundationdb.org/files/fdb-paper.pdf
    1. good. One of first to support ACID transaction in distributed KV store. impressive parts are
         The fast recovery (which Apple production upgrades by restarting all processes together)
         The deterministic simulation testing
       Log is the system/database, vs. LSM-tree flush. Many diffs. Design shifts are changing.
         very good at reflecting this design shift.
    2. highlights
        1. Deterministic Simulation Testing - proven extremely useful for high development velocity
            1. all code is built upon Flow, C++ async/wait primitives. all execution be deterministic
                1. multi-threaded concurrency is replaced by running one DB instance per code
                2. Flow Actor model, scheduled by runtime, one process can simulate multiple FDB servers, run abstract network, clock
                    1. where all nondeterminism and communication are abstracted
                    2. the run is fast, and can also run many simulations in parallel to cover combinatinos
                        1. discrete-event simulation can run arbitrarily faster than real-time
                3. covers many failures
                    1. inject machine, rack failures
                    2. randomized event times, randomized config parameters, cluster size
                    3. buggification e.g. code return unnecessary error, delay
                    4. TEST macros to tell how many specific case in code is covered
                4. limitation
                    1. must build on Flow
                    2. external code cannot be tested
        2. Fast recovery
            1. Apple production upgrades by restarting all processes at the same time, which usually finishes in a few seconds.
                1. Relies the very recovery speed of FoundationDB
                2. saves need to maintain RPC protocol compatibility between versions
            2. The first ingestion stream made durable is the log in "Log System" role
                1. Log is the database/system. actually the structure quite like Aurora
            3. why recovery is so fast - mapping to traditional DB
                1. recovery redo logs is the Log from PEV to RV. need to reply, usually a few seconds window
                2. the "checkpoint" / "snapshot" / read favorable data on-disk, is the by the "Stoarge Server"
                   "Stoarge Server" actively applies log, to make PEV->RV small
                    1. this is also unlike LSM-tree that flushes entire in-mem B+-tree, which still lags the log
                    2. applying logs to pages of Storage Server, actually have more random writes than LSM-tree flush, but
                        1. user latency and durability is already captured by Log System, so delay is OK
                        2. Storage Server can batch updates coalescing to be more IO efficient
                            1. or, compared to Helios paper, build higher level of indexes with compacting
                        3. question: how is memory and fast how to serve recent user reads supported? not much mentioned by the paper
                3. no need for undo logs. (ARIES)
                    1. undo logs were previously necessary in traditional DB, because of "steal, no force" where non-committed pages can be flushed into Storage Server, because they also carry other transaction's data
                    2. but in FoundationDB, there is no path that a page sync from memory directly to Storage Server. all must be through Log Server
                4. question
                    1. isn't the log as system/database approach introduces the double write problem
                       where ceph trying to solve years before?
            4. question: the paper didn't talk much about Storage Server design. here's the problem
                1. Storage Server needs to store a read favorable data on-disk and quickly apply updates from Log Server, how to maintain that?
                    1. if it's B+tree on-disk like traditional DB, random writes can be many, but we can scale out to more Storage Servers, because Log Server already handles latency and durability
                        1. just like Aurora Page Storage
                    2. if it's like LSM-tree, writes ingested are made sequenal dump to disk
                        1. then you need to handle compaction, and B+-tree fragments merging
                           or like Helios
                        2. so LSM-tree is not conflicting with Log is system/database designs
                            1. Compared to directly to LSM-tree, the key diff is Storage Server can independently scale out, separated from LSM-tree's logging
                    3. nowadays, designs are changing
                        1. LSM-tree tradition: user data -> partiton -> LSM-tree -> logging + on-disk read favorable format
                        2. Log is the system/database: user data -> central logging service
                            async/higher delay apply to Storage Server -> on-disk read favorable format
                            Storage Server can use B+-tree or LSM-tree internally
        3. Log is the system / log is the database
            1. it's like Aurora again, In Figure 1 Storage System acquires updates from logs, rather than from page sync like traditional DB systems
        4. unbundled architecture: all below roles are separated
            1. Contorl Plane: coordinators, data distributor, load balancing, etc separated
               Transactions systems: proxies, sequencer, resolver
               Log systems
               Storage systems
            2. question: any successful reuse of separated components by other systems?
        5. other points
            1. transaction management: serializability or snapshot level. the implementation is quite typical and paper illustrating is simple and straightforward
                1. useful, can be used as a reference how to implement distributed transaction
                2. transaction space is sharded into different proxies and resolvers
                    1. proxies acts as the primary to do single point of commit
                3. sequencer is a single node oracle, but supports faster recovery
                    1. sequencer ensure no gaps between LSNs, by returning previous LSN
                4. question: as paper says, MVCC window is only 5s? too short if want to query older data
                    1. and papers for long reporting transaction, they need to split into many small trnasactions
                        1. so question: how to consistent snapshot?
            1. detect failure and quorum reconfiguration, so to tolerate f failures with f+1 rather than 2f+1
            2. multi-zone deployment, in zone sync repl, across region async rpl
            3. FoundationDB offers minimal feature set, for other system to build atop
            4. FoundationDB is a distributed transactional KV. the SQL DB approach is different from building atop single node KV
                1. question, how to handle SQL push down to data nodes? rather than fetching data from FoundationDB to SQL gateway which is not efficient
            5. StorageServer is a modified version of Sqlite
                1. question: SQL is not needed here, overhead unnecessary? 
                2. future RocksDB as drop in replacement
            6. useful to list distributed system design points
                A production database needs to solve many problems, including data persistence, data partitioning, load balancing, membership and failure detection, failure recovery, replica placement and synchronization, overload control, scaling, concurrency and job scheduling, system monitoring and alerting, backup, multi-language client library, system upgrade and deployment, and configuration management.

6. MyRocks: LSM-Tree Database Storage Engine Serving Facebook's Social Graph    [2020, 5 refs]
   https://vldb.org/pvldb/vol13/p3217-matsunobu.pdf
    1. good paper. production proven that RocksDB can use as MySQL engine.
       explained why InnoDB (and B+-tree) structure has storage and write amplification
       may feature improvements to fill the gap from RocksDB to InnoDB
       MyShadow migration framework and practices to do global scale data migration
    2. highlights
        1. Facebook social activities such as likes, comments, shares, are served on global scale MySQL database. (UDB)
           UDB completes migration from InnoDB to RocksDB at 2017. UDB runs on SSD. The main purpose is to reduce storage amplification, reduced instance size by ~60%. also reduced CPU%
        2. why InnoDB has high storage amplificaiton?
            1. index fragmentation because the pages are not filled up, especially after compressed. e.g. the 8KB page
                1. besides, defragmentation hurts performance and flash durability
            2. even a single row modification in InnoDB results in entire 8KB page to be written
            n. related
                1. complies with analysis at 华为Taurus云原生数据库论文分析
                   https://zhuanlan.zhihu.com/p/151086982
        3. UDB general
            1. TAO servers hot reads, where left for UDB are batch jobs and TAO cold restarts 
            2. Binlog Server (Log Backup Unit) for geo-replication
            3. One database copy for each region
            4. secondary indexes
        4. engineer enhancements for the gaps between RocksDB vs InnoDB
            1. reverse key comparator in RocksDB to reduce compares to reduce CPU%
            2. RocksDB implements finding block location and size distance for min/max for SQL query optimizer
            3. prefix bloom filter in RocksDB to improve short range scan performance
            4. Scan performance degrade upon excessive number of Tombstones in RocksDB
                1. SingleDelete
                2. DTC - Deletion Triggered Compaction
            5. DRAM usage regression
                1. skip creating a bloom filter for the last sorted run
                2. using Direct I/O instead of Buffered I/O to reduce avg slab size by 8~0%
            6. Compaction competes with user
                1. add rate limits
            7. Bulk Loading to skip mem and directly create SST files and skip compaction
            8. interesting: RocksDB "per level compression" algorithms, hybrid compression algorithms
        5. Production migration - MyShadow - good part
            1. replay incoming user queries to MyShadow
                1. A custom MySQL Audit Plugin that capturd production queries
            2. replace MySQL read replicas, then primary replica, and then all replicas
                1. a few months baking read replica. started MyRocks serve prod from mid 2016, finish migration at Aug 2017
                2. culmination of years of effort to replaced primary
            3. Data correctness tool
                1. Single mode: check DB constraints
                2. Pair mode: run full table scan to check row count and checksum of InnoDB vs RocksDB
                3. Select mode: run select statements to compare

7. Fast Database Restarts at Facebook    [2014, 32 refs]
   https://research.fb.com/wp-content/uploads/2016/11/fast-database-restarts-at-facebook.pdf
    1. Good technique to use shared memory to speedup in-memory workload restart
       also, an useful example to write a simple paper with enough contents
    2. highlights
        1. Scuba in-memory distributed DB for Facebook's code regression analysis, bug report monitoring, ads revenue monitoring, and performance debugging
            1. usually rolling restart 2% of all services, take ~12 hours to finish upgrade
            2. Facebook use shared memory to keep data alive across upgrades at TAO and Memcache
        2. shared memory restart
            1. need serialization when dump heap memory into shared memory, of different formats
               key diff is blocks can be allocated in contiguous memory at shared memory

8. Shasta: Interactive Reporting At Scale (Google)    [2016, 4 refs]
   https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45394.pdf
    1. How to build interactive reporting with RVL outsourcing UI to wide contributors
       and TableCache for data freshness in-memory caching
       How F1, AdWords architecture looks like in Google and the power of F1 UDF
    2. highlights
        1. instead of (ETL) transformation, Shasta directly SQL query to underlying storage
        2. Figure 1: (Simplified) AdWords data-processing architectur
            1. good chart to show how F1, BigTable, Mesa, AdWords are used at Google
            2. Spanner underlyingly F1 (see 5.1 "Hash-based repartitioning")
        2. RVL language - joining 50 tables and fresh data
            1. implicit aggregation
            2. named SQL table views, to be reused in code, and avoid issuing duplicated SQLs
                1. subquery assignment
            3. rule-based instead of cost-based query compilier
            4. views code to invoke custom C++ or Java code
                1. see F1 UDF server
            5. Use F1 federated query across F1, Mesa, TableCache, Combine query
                1. ScanOperator, GetPartitons to determine F1 parallelism
            6. engineering
                1. instead of have 15 engineers developing complex UI needing domain knowledge
                   exposing it to 200+ code contributors across BUs with RVL is more effective
                2. application tends to become platforms, offering users with powerful programmatic programmatic APIs where query input sizes are larger, and interactive latencies are less critical, yet where data freshness and consistency requirements are just as stringent 
            n. question: like Power BI?
        3. F1 UDF servers - good part
            1. C++/Java binaries deployed on F1 UDF servers, must implement RPC API
            2. decouples release schedule and failure from F1 process
            3. for performance gap, A F1 slave thread calling UDF can distribute rows across hundreds of UDF servers, with batching and pipeling
        4. TableCache - in-memory read through
            1. F1 Change History, a first class table version of "binlog", SQL queryable
            2. use F1 Change History to keep data freshed, with versioning
            3. works for app that expects 100% fresh data immediately after writes issued to F1

2. Facebook's Tectonic Filesystem: Efficiency from Exascale    [2021, FAST21, 0 refs]
   https://www.usenix.org/conference/fast21/presentation/pan
    1. good paper, awfully similar to metadata scale-out version of Azure Storage Stream layer
       there are a few good useful aspects to learn from.
    2. highlights
        1. Data warehouse (non latency sensitive) uses inline EC
            1. the inline EC uses quorum writes, e.g. RS(9,6) writes to 19 storage nodes
            2. rather than sending writes directly, it sends *reservation request* with empty size first
               faster response 15 nodes are selected to write actual data
            3. questions
                1. "reservation request" are good design. but it adds one round trip time
                   how about instead write small size first, rather than zero size?
                2. for RS(9,6), we can allow writing RS 9+5 actually, and filling the last 1
                   as temporary reliability is enough. this should be a better way to do quorum write
                3. so quorum write now has two classes
                    1. out bound quorum write - need 3 write 4
                    2. in bound quorum write - need 3 write 2
        2. metadata partitioning & balancing
            1. ideally the directory tree needs to be partitioned properly to balance hotspots
               however needs to put related pieces together to address colocality
            2. Tectonic's solution is simply, just use hash partitioning and declare it's balanced
        3. Why need consolidate Haystack/F4 (blob storage) and Data Warehouse?
            1. per Haystack, IOPS per HDD remain steady, but HDD capacity keep increasing. thus IOPS/GB decline.
               Haystack has to overprovision storage for warm blob. increasing replication factor excessively (from 3.6x to 5.3x)
            2. Haystack overprovisioned storage to accommodate peak IOPS
               whereas f4 had an abundance of IOPS from storing a large volume of less frequently-accessed data
        4. Use of Copyset placement
            1. Tectonic adopted Copyset. It's trade-off between how frequent cluster has DU vs how many lost if DU happen
            2. besides, a data node needs to be placed that it share copyset with entire cluster, so that node down can involve whole cluster repairing
            3. besides, repairing can be heavier. E.g. 2 data nodes down for 3-replica
               without copyset, you get 2 node data of medium priority repairs
               with copyset, you get 1 node data of high priority repairs
        5. Multitenancy - how to co-run Blob + Data warehosue, maintaining SLA and efficient resouse sharing
            1. this is useful part too. Each tenant is tagged with TrafficGroup & TrafficClass
                1. tenant has quota on "ephemeral resources". surplus resource shared within own group first than given to other groups
            2. Client lib checks spare capacity in its own TrafficGroup, and uses Leaky bucket to do rate limiting
                1. And, Node uses weighted round-robin (WRR) scheduler to give up turn if a TrafficGroup exceeded limit
            3. nodes ensure that small gold IOs (e.g., blob storage operations) do not delay by colocation with large, spiky IO requests (e.g., data warehouse operations)
                1. Node WRR allow low pri IO to cede turn for gold IOs
                2. limit how many non-Gold IOs in flight
                3. stop schedule non-Gold IO if gold IO has been pending (for some time) on that disk
            4. Tenant-Specific Configuration
                1. per-call level, e.g. allow Data Warehouse to quorum write inline EC, while Blob write 2-out-of-3 replica 
        6. More points
            1. From Figure 2, it seems GC, rebalancer, Data repair etc services are running in separated processes
                1. paper didn't mention how these separated process interact closely with metadata store 
            2. Metadata store internally runs RocksDB on SSD
                1. question: that means using a small DB for metadata should be more favorable than plain arrays?
                2. it seems part of metadata is offloaded to SSD, rather than fully in-memory
                   it matches the metadata needs a disk_id=>file/block mapping to avoid full scan upon data repair
            3. the classic distributed transaction issue of mv directory
                1. Tectonic uses simply method, don't support full transaction syntax, just implement per shard transction
                2. it relies on upper layer users to properly call this APIs
            4. Tectonic didn't implement Geo-replication
                1. Tectonic its local cluster only. but it relies on upper layer to do geo-replication
                2. Tectonic doesn't have `du`
            5. Hierarchical namespace are required for most data warehouse workloads
                1. this explains why Tectonic needs directory=>file=>block metadata
                2. it seems Hadoop on default put the big files on one node only, resulting bin-packing problem
                   Tectonic breaks files into blocks. That explains why Tectonic needs a block layer

3. Programmable Solid-State Storage in Future Cloud Datacenters    [2017, 20 refs, SDC 2017]
   https://cacm.acm.org/magazines/2019/6/237002-programmable-solid-state-storage-in-future-cloud-datacenters/fulltext
    1. interesting summary on new industry directions - Programmable SSD
    2. highlights
        1. Agile, flexible storage interface
            1. stream aware by checking block content inside SSD
            2. upgrade firmware agility
                1. bad: cloud updates everyday but disks (firmwares) stay static in 5-year lifecycle
            3. better prioritization and preemptive between high pri user IO vs in-fly background IO.
            4. disk scrubbing inside the SSD disk.
                1. Ideally any single node background job can be offloaded to disk,
                   and multiple node can be offloaded too with SSD Remote-access-no-host fabric
        2. Moving compute close to data
            1. bigdata analysis inside ssd for large bandwidth and reduce outside
            2. more energy efficiency than host cpu
            3. access any remote storage device without involving the remote host server
                1. a micro server inside storage can expose a richer interface like a distributed key-value store or distributed streams.
                2. Or the storage infrastructure can be managed as a fabric, not as individual devices.
        3. Secure computation in the cloud
            1. clear text no out of ssd. secure computation domain.
            2. but computation inside ssd saves repeat decrypt then encrypt, compared to get data out compute at host.
        4. example hardware
            1. dragon fire card: main board contains an ARMv8 processor, 16GB of RAM, 
               and various on-chip hardware accelerators (such as 20Gbps compression/decompression, 20Gbps SEC-crypto, and 10Gbps RegEx engines)
        n. questions
            1. why Smart HDD didn't come up like SSD?
                1. bandwidth gap bewteen host and HDD is much smaller than SSD
    n. related
        1. Alibaba invest in Computational SSD (https://www.youtube.com/watch?v=_8gEmK1L4EY) (ScaleFlux corp.) to pushdown OLAP row filtering down to SSD.
        2. Smart SSDs

18. PolarDB Serverless: A Cloud Native Database for Disaggregated Data Centers
    http://www.cs.utah.edu/~lifeifei/papers/polardbserverless-sigmod21.pdf
    1. goes beyond shared storage, add shared memory pool - disaggregated architecture.
       key usecases, interesting:
         RW node and RO node don't need keep private duplicated copy of page, use page in shared memory instead
         RW node pass latest page to RO node via shared memory page, traditionlly this needs RW->redo log->shared storage->RO replay log
         Scale out/in CPU/memory according to workload, e.g. OLAP needs more mem, OLTP needs more CPU. 
       This paper also reveals in details how PolarDB works and designs
    2. highlights
        1. like Snowflake, besides storage is remote, memory is also remote
        2. multi-tenant scale-out memory pool
            1. to execute transaction correctly
                1. invalidate cache for read after write not to miss any updates
                2. global page latch to see B-tree structure consistent while changing in middle
            2. to execute transaction efficiently
                1. one-sided RDMA, RDMA CAS
                2. page materialization offloading to allow dirty pages evicted from remote memory without flushing them to storage
                    1. PolarDB serverless now stores dirty page in shared memory.
                       it allows share page between RW and RO node, rather than maintain a private copy each
                    2. instead of flush pages, which stresses networking, PolarDB write redo logs to the storage and materialize pages from logs asynchroniously. like Aurora and Socrates
                    3. traditionally, after RW node updated a page, RO node needs to replay redo logs in local buffer pool to obtain the latest page
                       but in PolarDB Serverless, the RW node can instead write dirty page to remote memory, and then the RO node immediately obtain the latest via shared page
                3. index-aware prefetching to improve query performance
                    1. Batched Key PrePare (BKP) - accept a group of keys to prefetch in background
                    2. BKP has many usage cases, e.g. loading SQL query fields, hash join. in many cases, which keys will to be loaded can be accuratedly predicted to prefetch
            3. datacenter and serveless
                1. networking in CLOS architecture, bunch of servers in PoD, compute/memory/storage are delivered in PoD
                2. serverless scale-out/in, e.g. OLAP and OLTP workload has different CPU vs Memory needs.
                   tranditional DB bound CPU & Mem together to serverless scale-out/in is unwise
                    1. per scale-in, CPU can be easily shrinked, but memory can be kept (in-mem or freezed), saving the reload from storage 
            4. disaggregated memory - the remote shared memory pool
                1. libmem interface is page level, page_register/read/write etc. access with one-sided RDMA
                    1. memory allocation by 1GB slab
                    2. Page Address Table (PAT) - a hash table maps page id, slab, and track page reference count
                    3. Page Latch Table (PLT) - global physical lock, per page level, to protect B+tree structurual integrity
                2. global page locking
                    1. similar with crabbing/lock coupling, but to protect B+tree pages scattered to multi-node
                        1. to lock, use RDMA CAS, if fail then failback to negotiation
                        2. questions
                            1. all reads/writes and SMO need to check and place locks, interacting the remote PLT ... overhead?
                3. home node (the first slab node) contains critical metadata (PAT, PIB, PRD, PLT). it is backed up with another secondary replica in sync manner
```

FAST21 papers, database, and some other papers.

```
1. File System Aging (Fabian Hofbeck)   [2020]
   https://www4.cs.fau.de/Lehre/WS19/MS_AKSS/arbeiten/File_System_Aging_slides.pdf
    1. how to reduce filesystem aging
        1. large extent size
        2. delayed allocation
        3. grouping similar files
        4. packing small files into one
        5. Be-tree buffer modifications

2. Uncovering Access, Reuse, and Sharing Characteristics of I/O-Intensive Files on Large-Scale Production HPC Systems    [2019, 0 refs]
   https://www.usenix.org/conference/fast20/presentation/patel-hpc-systems
    1. Edison supercomputer
    2. findings
        1. Runs can be classified as “read runs” (68%) or “write runs” (32%)
        2. Most I/O-intensive files get re-accessed after a relatively long period (>50 hours) - much longer than the avg. runtime of jobs
        3. Some HPC files experience a very long string of consecutive read runs, in contrast with smaller consecutive write runs.
            1. Partitioning of I/O servers to separately serve RH files (which perform many onsecutive reads) and RW files (for read and write runs) can boost I/O performance
        4. High degree of variability in I/O time of ranks/processes with similar I/O size belonging to the same application. 

3. A Five-Year Study of File-System Metadata (microsoft) (FAST21 Test of Time Award)  [2007, 486 refs]
   https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/fast07-final.pdf
    1. FAST21 Test of Time Aware. Windows PC file and directories distribution study 
    2. highlights
        1. Data source: Windows PC filesystem metadata snapshots, temporal change
        2. key findings about files
            1. ~80% files are smaller than 64KB, ~80% files age <= 0.9year
            2. gif files occupy significant count, dll files occupy significant size
            3. ~50% filesystems have ~70% files unwritten since they were copied
        3. key findings about directories
            1. size, file count, path depth, see paper ..
        4. generative model for directory depth
            1. poisson distribution
            2. a maximum displacement of cumulative curves (MDCC)

4. Optimizing Garbage Collection Overhead of Host-level Flash Translation Layer for Journaling Filesystems (KoreaScience)   [2021, 0 refs]
    1. host-level FTL that separates journal from file data to reduce garbage collection overhead

5. FAST '21 - Keynote Address: DNA Data Storage and Near-Molecule Processing for the Yottabyte Era
   https://www.usenix.org/conference/fast21/presentation/keynote-ceze-strauss
    1. DNS storage. Super dense cold storage, long lifetime.
    2. GB scale now. Latency goes hours in batch, throughput/day is higher than transistors

6. Could cloud storage be disrupted in the next decade?
   https://www.usenix.org/conference/hotstorage20/presentation/chatzieleftheriou
    1. DNA, Holographic, 3d cross point, 

7. Data Deduplication Technology for Cloud Storage    [2020, 1 refs]
   https://hrcak.srce.hr/file/355621
    1. HDFS dedup. Hash at File level (SHA-1). Hash lookup table stored at HDFS.
       File uploaded is first stored at a temporary pool, and then offline calc hashing / dedup
       File hashing and compare can be done at client app, MapReduce, or FPGA circuit. Small hash collision rate is OK for Web Applications
    2. HDFS files bing operated are usually very large, 100MB is a minimal.
       so that the dedup overhead can be amortized across the transfer size
        1. paper conclusions still points there are significant system performance impact and client load issue

8. On the Feasibility of Parser-based Log Compression in Large-Scale Cloud Systems    [2021, 0 refs]
   https://www.usenix.org/conference/fast21/presentation/wei
    1. good. log compression by extracting common templates, with encoding on number and timestamps
       reaching ~40x compression ratio and comparable compression speed with LZMA
       log compression and retention is a daily problem for large scale cloud storage indeed
    2. highlights
        1. LogReducer is improved from LogZip, comparable compression speed to LZMA, compression ratio ~40%.
           Tested on AliCloud logging sample. opensourced at https://github.com/THUBear-wjy/LogReducer
        2. how it works
            1. logs have common templates, extract them
                1. logs are grouped by template ID, and then varables are stored in column-oriented manner
            2. better engineering in C++ compared to LogZip (python)
                1. besides, less templates, but more variables per template
            3. Elastic encoding: variable length encoding for numbers
                1. besides, number correlation, e.g. next IO offset = prev IO offset + size
            4. Delta timestamps: logs using many timestamps, with very small delta
        3. questions
            1. the paper didn't reveal decompression ratio (log search speed)
               and CPU and memory consumption (same node running the log compression)
            2. why parser-based log compressor? log printer called in prod code can already tell you log template. 
                1. parser approch is intersting. it's actually able to break log string into key-value objects.
                2. and then,  any attempt to translate logs into objects? key-value indexed in database and able to search, join, and SQL query
            3. what's the true compression speed with limitted CPU and memory? given co-locating logging on the same server node
        4. related works - useful summary
            1. General-purpose compression approaches
                1. Statistic-based compression methods (e.g., Huffman coding [40], Arithmetic coding [47]) first collect statistic information about input logs and then design variant length coding for each tokens
                    1. need to read the input log file twice. As a result, when the input log file is large, they are not efficient
                2. Predict-based compression methods (e.g., PPMd [4]) predict the next token based on current context during reading the input stream, and assigns a shorter encoding if prediction is successful.
                    1. the appearance of variables will decrease the prediction accuracy
                3. Dictionary-based compression methods (e.g., LZMA, gzip) search for similar tokens in a sliding window and store them in a dictionary when processing the input stream
                    1. may lose the chance to trim redundancy within a long distance, and do not take the delta of timestamps and correlation of variables into consideration, since they are not related to redundancy literally
            2. Log-specific compression approaches
                1. Non parser-based. CLC [22], LogArchive [3], Cowic [29] and MLC [13] 
                2. Parser-based: Logzip [30] extracts templates and processes templates and variables separately

9. Pattern-Guided File Compression with User-Experience Enhancement for Log-Structured File System on Mobile Devices    [2021, 1 refs]
   https://www.usenix.org/conference/fast21/presentation/ji
    1. mobile compression, content selective compression, packing correlated read data 
    2. highlights
        1. typical cases of using compressed filesystem on Mobile
            1. Mobile SQLite fragmented acesses
            2. App launch fixed pattern reads
        2. approaches
            1. barely read files, deep compression and large packing
               also packing db-journal metadata with compressible db page files
            2. executable files, highly compressible but subjects small random reads. background packing related blocks together
            3. FPC implemented log-strucutred F2FS, exploit out-of-place updates for small fragmented writes
            4. simply ignore files of incompressible types, e.g. *.mp4, *.jpg
               more .. real-time detect whether writes are compressible, try firs page then assuming later pages
        3. revealing traditional sequential compression drawbacks
            1. see paper introduction parts

12. 2DFQ: Two-Dimensional Fair Queuing for Multi-Tenant Cloud Services (Microsoft Azure)    [2016, 28 refs]
    https://cs.brown.edu/~jcmace/papers/mace162dfq.pdf
    https://www.youtube.com/watch?v=PMBsUTf-qZY
    https://www.youtube.com/watch?v=ATMODv8SYbk 
    https://conferences.sigcomm.org/sigcomm/2016/files/program/sigcomm/Session04-Paper01-2DFQ-Jonathan-Slides.pdf
    1. interesting. fair scheduling by separate large requests to another thread.
       simulated with Azure Storage workload, perform better than WFQ and WF^2Q (and explained their details)
    2. highlights
        1. compared 2DFQ with WFQ and WF^2Q
            1. the key diff is 2DFQ separate requests to threads according to their sizes. Large requests go to a separated thread
                1. besides, WFQ and WF^2Q generate burst schedules, i.e. small request users can be blocked for a short while by big request users, and then go, and repeat blocking
            2. 2DFQ modfies WF^2Q's eligible condition to put larger requests to higher index threads
            2. WFQ schedules the pending request with the lowest virtual ûnish time
            3. WF^2Q restricts WFQ to only schedule requests after they become eligible
        2. discrete event simulated with Azure Storage workloads
            1. no much hint about how to implement on distributed storage env. probably we need to track per storage account's usage status
            2. WFQ, WF^2Q didn't perform well in the simulate
                1. leads to bursty schedule, where large request block small ones by head-of-queue
        3. how to predict request size? (i.e. request cost)
            1. OK .. this is not very hard for storage systems with pretty straightforward API
            2. when request costs are unknown priori, 2DFQ uses pessimistic cost estimation
                1. moving average has feedback delay considering the user switched from small requests to large ones
                    1. and moving average can be "hacked" if user alternating between small requests and large requests to fool scheduler
            3. Retroactive Charging - actual cost is feedback, compared to estimate. extra charge or refund are applied
            4. Refresh charging is a ‘damage control’ mechanism that periodically measures the resource usage of long-running requests and incorporates measurements into the scheduler immediately. It lets us notice expensive requests quickly and immediately charge the tenant for the excess cost while the request is still running, short-circuiting the typical cost estimation feedback loop
    n. related materials
        1. 理想调度和2DFQ、WFQ、WF2Q生成的调度 ..
           https://www.jiqizhixin.com/articles/2016-08-31-2

19. Mainlining Databases: Supporting Fast Transactional Workloads on Universal Columnar Data File Formats    [VLDB 2020, 4 refs]
    https://arxiv.org/abs/2004.14471
    1. Interesting direction. HATP finally someone tried using Columnar format (favors OLAP) to support OLTP 
    2. highlights
    n. related materials
        1. noisepage paper分享：基于column-storage实现的事务存储引擎 (AnalyticDB PostgreSQL)
           https://zhuanlan.zhihu.com/p/351306672
            1. "这篇paper是CMU database group实现的self-driving database的系列paper的其中一篇，主要分享的是如何基于一个通用的列存格式来实现一个in-memory的HTAP系统。noisepage的前身是peloton，与monetdb（荷兰的CWI开发，open source），HyPer（德国慕尼黑TUM大学开发，已经被Tableau收购）齐名的列式数据库。

            HTAP从工业界目前的实现来看，除了HANA比较另类，基本都是一个行存用来服务TP，一个列存用来服务AP，更细分有2种策略，内部实现行转列，典型的代表是TiDB，用户自己做ETL来实现行列转换，例如Greenplum，TBase。noisepage的实现算是一种学术界的探索，在列存的引擎上同时实现AP和TP。

            因为作者在这篇paper中，基于arrow的in-memory的列存做的实现 ...

            数据在每个block被组织成PAX（行列混存）格式，一个tuple的所有列的数据都在这个block，每个block有一个layout对象，由下面3个部分组成：...

            arrow格式实现事务一个问题就是写放大，作者使用了一个灵活的arrow格式来实现高效的写入，当数据变冷（不再频繁做修改）的时候，通过一个轻量级的转换把一个block放入到arrow格式中。"

7. Azure RTable - sync cross-region Azure Table service
   https://github.com/Azure/rtable
    1. readings
        1. Leader or Majority: Why have one when you can have both?
            Improving Read Scalability in Raft-like consensus protocols
            https://www.usenix.org/system/files/conference/hotcloud17/hotcloud17-paper-arora.pdf
            1. leader read + back-off to read majority of secondaries
        2. In Search of a Scalable Raft-based Replication Architecture
           https://www4.cs.fau.de/Publications/2019/deyerl_19_papoc.pdf
            1. Instead of one, a server runs multiple instances of Raft, each primary assigned to different servers
            2. each instance of Raft generate independent logs. The logs are merged in deterministic manner (sequencer)
                1. sequencer selects log next entry in round-robin
                    1. questions: doesn't sound reliable, and need to wait if next round-robin hasn't been ready?
    2. rTable is using lock to group two operations to make them an atomic one
         the last node always hold the latest commit version.
         the previous nodes are locked thus not readable during transaction
       if tail node failed, we need to rely on the client to track whether last commit succeeded
         client needs to cleanup nodes, unlock in reverse order
         if client is also dead - region failure
           It should be OK just cleanup the last commit and unlock. we don't actually know whether last commit is succeeded, but since client is dead, we pretend it didn't succeed
       to handle read affinity of the local cluster
         we should put tail node in rTable at the local cluster, tail node always serve the reads best. other two nodes can serve reads if they are not locked
         the write is chain write which goes from the remote region node first
       to handle region failure (A->B->C chain write)
         A, B region failure should be OK, we just ignore them
         C failure - A->B just form new chain, B becomes new tail
         failover need manual configuration
    3. better, with paxos, and auto failover (but we only want <=3 copies?)
        1. data is partition by cluster. each cluster data form an individual paxos group. runs parallel raft
           * leader selection is free. but each update pass requires > 1/2 node, and the 1/2 node must include the local cluster's node
            1. this should ensure local cluster node always have the latest data
                1. a strong consistent read probably still needs to go to primary to ask whether a vote actually passed in quorum, even it passed in local cluster node
                   and then go to the local cluster node to fetch for the last data
                   it's possble execution decree is late from vote decree, the reader needs to wait on the local cluster node
    4. paxos / chain-replication, local cluster node always as leader
        1. it's pretty similar with rTable
           the local primary only marks a version visible after all secondaries write succeeds
        2. the read needs to ask the local primary which version is committed
            1. or we use locking to guarantee version update atomic, and we let primary do the locking rather than client. we make sure primary is HA, each participant is HA
        3. * so an fix to the rTable's orphan locked issue is
            1. let Azure Table itself, which is HA, to perform the locking. rather than build logic in client
            2. but Azure Table has no execution ability. so the client just log what it wants to an intent table (may not be cross region HA), sequentially
               write an local cluster HA engine to execute the intent
               or let clients compete to execute the intent, each intent is assigned an exclusive owner client and lease
    5. how replicated state machine - ReplicateStateMachine lib avoid this issue:
       if reader goes to a secondary node, the secondary node may have passed a vote version, then reader reads that version. but actually, the version hasn't been passed by majority of nodes, thus not commited yet
        1. i.e. read on secondary sees uncommited but local voted value
        2. solution: ReplicateStateMachine separates into two phases,
            1) passing vote decree
            2. do execution
           only after a decree is commited in quorum, the secondary will do execution. only after execution is done, the reader can see state data mapped to the voted version
            1. which implies, when reader sees a version, the decree must have already be commited by the quorum, not all secondaries may have already executed that, but even failover, eventually all execution on all nodes will be done
                so reads on secondary won't see uncommited value
                even though seeing stale value is possible
            2. essentially, this is doing a 2PC here, decree passing is prepare, execution is commit phase. Tx commit single point is whether >1/2 passed decree
        3. applying to the rTable issue, we have 
            1. let all nodes do prepare, requiring A,B,C all done prepare
               then tell them to commit
               new client (acting as the primary role) will first examine all prepare that passed by > 1/2 has been committed, and help it commit
            2. * protocol for A,B two regions
                1. a write client acquire write exclusive lease on A,B
                   write client examine A,B has uncommited prepare, if both A,B presents, commit it on both A,B
                   write client prepare A,B
                   write client commit on both A,B
                    1. the single point of commit is: both A and B have prepared value
                2. the write client guarantees
                    1) A will always commit first
                    2) it will only commit when both A,B has prepared
                   it implies, if a reader sees a version, prepare must all be done
                   reader can see stale value on B, must one A it must be fresh
                   no writes would be lost, only possible to prepared but uncommited
                3. so .. this is two PC again.

11. Understanding Operational 5G: A First Measurement Study on Its Coverage, Performance and Energy Consumption    [2020, 11 refs]
    http://xyzhang.ucsd.edu/papers/DXu_SIGCOMM20_5Gmeasure.pdf
    1. usuful experiments and summary about current operational 5G status, issues, and future directions.
       vendor side: 5G device is most costly, and same device covers less than 4G and less penetration ability.
                    5G mostly uses NSA mode, i.e. reuse 4G infra. this cannot get 5G's best
                    besides, to utilize full 5G throughput, all software/hardware infrastructure need upgrade. and networking algorithms. more costly
       consumer side: 5G module is more power consuming than 4G. and the signal coverage is worse.
    2. highlights
        1. vendor support: 5G is usualy installed via NSA (non-standalone architecture) mode, i.e. reuse 4G infra.
            1. 5G vendor device has higher cost, by per device has less coverage than 4G, and worse signal penetration
            2. due to reusing 4G towers, the 5G device placement and density cannot achieve optimal, there many signal holes in campus
            3. indoor is worse, due to 5G signal has higher frequence thus lower penetration through walls
        2. throughput and latency: 5G has ~3x throughput at TCP (~25MBps) / ~5x at UDP (~100MBps) compared to 4G. 5G avg latency (~22ms) is ~0.5x of 4G
            1. however, 5G UDP shows worse bandwidth utilization if compared to 5G TCP, or compared to UDP.
               the algorithms need update with 5G, e.g. buffer size. and e.g. most application finished loading page before TCP slow-start probing done
            2. most 5G latency reduction comes from the second hop (from the gNB to cellular core network). the following hops added latencies are similar to 4G
               there are less 5G users now, if as many as 4G, the NSA implies 5G infra has not enough bandwidth support
               NSA also implies there are unwanted latency in wirelink / infra path, also need upgrade with 5G
            3. per web browser, rending takes dominate latency, while 5G is faster downloading but only cut down ~21% time
               replacing slow-start probing with a deterministic bandwidth estimation [90]
        3. real-time Panoramic Video Telephony
            1. 5G shows ~22ms latency, not suffice for the Rel-8 TS 23.203 [6] required 10ms latency for interactive real-time applications e.g. VR
            2. 5G frame delay is ~1s, almost similar with 4G ~1.1s. transmission takes ~66ms, but 10x else spent at codec encode/decode, rendering, frame capture, patch splice
            3. to sum up, for 5G to work well, customer software/hardware, and vendor infra all need upgrade, to provide the best throughput/latency for 5G potential
        4. energy consumption
            1. the 5G module dominate the most energy cost, ~55%. about 2x than 4G. and consums more than even the screen
            2. mainstream smartphone solution uses a plugin 5G module, rather than SoC. This is less energy efficient
            3. example power management: switch to 5G only when necessasry, other time fallbacks to 4G.

12. Clock-SI: Snapshot Isolation for Partitioned Data Stores Using Loosely Synchronized Clocks    [2013, 70 refs]
       https://infoscience.epfl.ch/record/187553/files/srds2013_clocksi.pdf?version%3D1
       https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/samehe-clocksi.srds2013.pptx
        1. distributed transaction without central clock or TrueTime atomic clock, at snapshot isolation
           by delaying read upon node clock too small, or for write commit timestamp take max(all prepare timestamps)
           Ready delays. But I don't see commit needs wait. And so External Consistency may not be a concern in Clock-SI.
        2. highligthts
            1. using max(timestamps from all participant nodes) to acquire the final commit timestamp
                1. Question: Though compared with Spanner External Consistency, the paper didn't clearly state whether External Consistency is guaranteed
                    1. as far as I understand, the external consistency violation can still happen
                       but maybe it's not a concern of related usecases
                        1. i.e. a later committed transaction can obtain a smaller commit timestamp than the previously committed transaction
                2. Question: How to form consistent snapshot, when reading to multiple participant nodes, while each node has clock drift?
                    1. Figure 1 and Figure 2 are useful cases
                        1. In Figure 2, note T1's commit timestamp is t, but commit finishes at t'. T2's snapshot timestamp is t'' > t. So, T2 must read wait to t', so that data committed at t is visible it T2.
                        2. See Figure 1. Though Clock-SI doesn't need timestamp oracle, a read has to wait until each partition catches up to snapshot timestamp t. As a result, high clock drifting will kill read latency. Then, it still needs a cross partition clock synchronization protocol, NTP + HLC should be fine.
                    2. the paper chooses to delay reads. but that results in not a consistent snapshot w.r.t. physical absolute time
                3. Question: See Algorithm 1, the read wait instead of Spanner's commit wait?
                    1. if it's read intensive, isn't read wait even worse?
            2. For short readonly transactions, Clock-SI improves latency and throughput by 50% by avoiding communications with a centralized timestamp authority
            3. The core of these challenges is that, due to a clock skew or pending commit, a transaction may receive a snapshot timestamp forwhich the corresponding snapshot is not yet fully available.
                1. We delay operations that access the unavailable part of a snapshot until it becomes available.
                2. As an optimization, we can assign to a transaction a snapshot timestamp that is slightly smaller than the clock value to reduce the possibility of delayed operations.
            4. "Choosing Older Snapshots" - read at snapshot timestamp - ∆
                1. because read at snapshot timestamp t has to wait for every partition reach timestamp t
                   to avoid read wait, we can choose a smaller t, so that it's <= every partition's current timestamp
                   this is just like reading at snapshot timestamp t of low watermark agreed by all partitions 
        3. Interesting / good thoughts from paper
            1. attack timestamp Oracle throughout & latency is a good direction. can a closely sync cluster help?
                1. this is where TiDB SPOF timestamp oracle limit read/write latency. and every read/write wants a timestamp and gets impacted
                2. external consistency. can the abnormal case be fixed by causal consistency? participant group(A, B, C) commit forst , they have higher timestamp; (C, D, E) commit later, but they have lower timestamp.
                    1. Fix it with causal consistency: after (A, B, C) commit, C bump itself timestamp, so (C, D, E) now must have higher timestamp than (A, B, C) now.
                       Broader thinking: any sync problem, can use similar approch to pass causal timestamps to bypass needs for close sync e.g. TrueTime

13. Virtual Consensus in Delos    [2020, 0 refs]
   https://www.usenix.org/system/files/osdi20-balakrishnan.pdf
    1. Good paper. First propsoe the VirutalLog interface.
       Decouple Paxos data plane from control plane, providing unified log stream,
        and allow bridging into different log store implementations.
       production migrate, upgrading, hotfixing are made easier.
       Shared log interface is made more common in many different works

    2. Highlights
        1. history from Facebook
            1. initially it needs to reach production fast (8months), allow incremental evolution, and combine different metadata storage: ZooKeeper, LogDevice, ZippyDB, MySQL running on production
                1. these storage couples database and the consensus protocol, no boundary and API separation
            2. VirutalLog and Delos DB allows .. good applicable production features
                1. migrate backend data from one backend LogLet to another, totally transparent to user
                    1. transparent upgrade, e.g. from slow ZooKeeper to 10X faster NativeLogLet
                2. hotfixing for bugs, discovered but on NativeLogLet, then temporarily fallback to ZooKeeper for fixing
                3. allows deleting a single log entry from the VirtualLog, which is traditionally hard in Paxos
                    1. typical production issue surgery case, remove a corrupted log entry that poison many roles
            3. on production for 18+ months, 1.8 billion transactions per day
        2. key designs
            1. VirtualLog and LogLet are first clearly designed abstractions with simple APIs
                1. LogLet needs to provide consensus, durability, but no need for fault tolerant consensus
                2. LogLet needs to support Seal operation
                    1. Seal must be highly available, even though LogLet doesn't support fault tolerance consensus
                3. VirutalLog is the Control Plane, whiile LogLet is the Data Plane
                    1. where Raft is considered to have couple two planes into one protocol
            2. VirtualLog needs support reconfiguration, i.e. switch LogLet upon failure append
                1. A central MetaStore is necessary, to store the reconfiguration metadata, which LogLet which log range, etc
                    1. also, new chain is fetched from MetaStore
                2. MetaStore is first implemented an external ZooKeeper, then moved to an embedded Paxos implementation
                    1. Full paxos is not necessary for just to support reconfiguration
                3. Reconfiguration can have latency hit
            3. In one time, a log appends to one LogLet
                1. can switch to another LogLet upon failure aond user initiated Seal
                2. there is no stripping across LetLets, but LogLet internally can support StrippedLogLet
            4. Delos is a ACID database implemented upon the VirtualLog
                1. for metadata / control plan data service at Facebook
                    1. 1.8 billion transactions per day is ~20K IOPS.
                2. Each Delos server maintains a local copy of state in RocksDB
                   and keeps this state synchronized via state machine replication (SMR) over the VirtualLog
                    1. this is pretty much like AWS Aurora Multi-master design of "log is database"

    m. some thoughts / questions
        1. the Paxos quorum is typically a consensus shared log + replicated (memory) state (with checkpoints)
            1. the shared log can be easily sharded.
               however the replicated (memory) state needs to calculated based on all history logs, thus unable to get sharded?
            2. so the solution is to decouple the shared log and the replicated (memory) state?
               i.e. shared log (sharded) + DB?
                1. however, the processing loop: read DB state -> determination -> post to shared log -> apply update to DB state -> loop.
                   the throughput is still limited by DB state apply cannot be sharded
                2. but still useful if shared log IO processing is the bottleneck
                3. there is more CONFLICTING here, if we further allow DB to be sharded to scale-out throughput, that means the logs are disjoined, there is NO need for a total shared log
                    1. i.e. virtual shared log + shared, in combine with shared DB states
                       is internally contradictory in design concepts
            3. Reviewing the paper "Figure 1"
                1. There is one stream of log, and all DB (memory states / checkpoined) share the state
                   So this is only one instance of quorum replicating same state
                2. The log is NOT sharded. log first appends to LogLet1, then seal on failure, then append to LogLet2, then seal on failure, then LogLet3
                    1. so the append throughput is still limitted by single LogLet, i.e. an append chain
                3. Comparing with Azure Storage Stream
                    1. Stream itself is a virtual log
                    2. the EN append chain vs LogLet
                    3. seal and switch to another append chain vs seal and switch to another LogLet
                        1. seal and switch called reconfiguration in Delos.
                    4. the innovative side of VirtualLog is allowing LogLet (EN append chain) to adopt different implementations
                        1. and thus allow ease of migration
                        2. VirtualLog targets metadata handling, 1.8 billion transactions per day is 21K IOPS, single cluster not large
                            1. besides, common stream commonly has random reads, while shared log assume sequential reads
                    5. thinking about Azure Storage Stream, it can sell new types of services
                        1. how many customers/devs need shared log metadata state management?
                        2. how many customers/devs want to build application on shared log data management?
        2. VirtualLog interface can introduces performance penalty. I.e. interface impedance.
            1. The ZooKeeper LogLet replaced to NativeLogLet is a hint
                1. 10X perf sounds like a polit way to say the ZooKeeper LogLet is slow.
                2. But this can also be explained by ZooKeeper is itself slow.

    n. Relative materials
        1. CORFU: A Shared Log Design for Flash Clusters  (2012)
           https://blog.acolyer.org/2017/05/02/corfu-a-distributed-shared-log/
            1. vCorfu: A Cloud-Scale Object Store on a Shared Log (2017)
               https://blog.acolyer.org/2017/05/03/vcorfu-a-cloud-scale-object-store-on-a-shared-log/
            2. CorfuDB VMware
               https://github.com/CorfuDB/CorfuDB
                1. sharing author "MAHESH BALAKRISHNAN" Corfu paper and Delos paper
            3. Tango: Distributed Data Structures over a Shared Log  (2013)
               http://www.cs.cornell.edu/~taozou/sosp13/tangososp.pdf

            4. Facebook LogDevice
               https://logdevice.io/
                1. "This is an archived project and is no longer supported or updated by Facebook."
                2. "Non-deterministic record placement"
                    1. quorum write quorum read,  metadata log tracks copyset change
            5. Kalfa can also be seen as a shared log

        2. Aurora Multi-master: The log is the database
           https://www.allthingsdistributed.com/2019/03/Amazon-Aurora-design-cloud-native-relational-database.html
            1. 华为TaurusDB
               https://zhuanlan.zhihu.com/p/151086982
```
