---
layout: post
title: "Recent Paper Reading: Alibaba Cloud DBs, PolarDB, Migration Downtime"
tagline : "Recent Paper Reading: Alibaba Cloud DBs, PolarDB, Migration Downtime"
description: "Recent Paper Reading: Alibaba Cloud DBs, PolarDB, Migration Downtime"
category: "storage"
tags: [storage, paper, cloud]
---
{% include JB/setup %}


Alibaba Cloud databases. PolarDB, OceanBase, AnalyticsDB. Huawei TaurusDB. AWS Aurora.

```
1. OceanBase Paetica: A Hybrid Shared-nothing/Shared-everything Database for Supporting Single Machine and Distributed Cluster    [2023, 4 refs, VLDB23, Alibaba]
   https://www.vldb.org/pvldb/vol16/p3728-xu.pdf
    1. Paetica is OceanBase 4.0. Maintain the performance of single node OceanBase comparable to single node databases. This is an interesting topic for commercial databases. Key techniques involves using function call instead of networking, using a single shared log stream.
    2. Highlights
        1. Key challenges
            1. Maintain the performance of single node OceanBase comparable to single node databases.
            2. Support small-scale enterprises.
        2. Backgrounds
            1. OceanBase 0.5
                1. Separation of write nodes and read nodes. Update Server vs Chunk Server
                2. LSM-tree engine. Incremental major compaction, staggered round-robin compaction
                3. 2PC transaction. Global Time Service (GTS).
            2. OceanBase 1.0 ~ 3.0
                1. Totally given up the architecture in OceanBase 0.5
                2. P2P shared nothing architecture. DB is partitioned. SQL layer runs on data nodes.
                3. Driver/OBProxy layer.
                4. 3-zone deployment.
                5. Weak consistency reads.
                6. Paxos replication-based log streams across 3-zone deployment - Disaster Recovery.
            3. OceanBase 4.0
                1. Continued from the architecture of OceanBase 3.0
                2. More optimizations
                    1. Reduce metadata and memory overhead
                    2. More DDL support, partitioned DML, direct insertion into static data
                    3. Thread stack optimization, on-demand load metadata, input restriction
                    4. Tenant isolation: isolate compaction merging, metadata, commit logs and SSTables
        2. Key solutions
            1. integrates several storage shards with a shared log stream
                1. process transactions without 2PC, without accessing GTC
            2. single node deployment runs only one process.
                1. threads interact with function calls rather than networking.
                2. Serial Execution, it doesn't need context switch
            3. OceanBase 2PC
                1. Standalone deployment doesn't need to access GTS
    3. My questions
        1. Compared to PolarDB which modifies MySQL, it seems OceanBase chooses to a total rewrite? This is tremendous amount of work.
        2. How CockroachDB and TiDB deal with the similar efficient single node deployment problem?
        3. Why not simply deploy all OceanBase components into one node to make an efficient single node deployment? Is there an analysis of the bottlenecks?
        4. There are still many open questions. The paper only shipped a few limited optimizations for standalone deployment. Is that enough?
        5. Does OceanBase support anything related to HTAP? What's the details?

    n. Related materials
        1. OceanBase 4.0版本到底牛逼在哪里？ - 萧筱姐姐
           https://www.zhihu.com/question/626978271/answer/3258653349
            1. "OceanBase 4.0 真正做到大规模数据处理能力的同时，又能做到可以与传统单机数据库媲美性能，所以这个版本还有非常不同又饱含深意的命名，叫做“小鱼”，可以独立为个体，也可以汇集成群。"
            2. "OceanBase 4.0可以做到在单机部署时，性能与单机数据库相当，甚至比某些流行的单机数据库的性能更好；当三机三副本部署时，相同的性能同时提供比传统主备库更好的高可用能力；当节点机器规格提升时，提供了线性的垂直扩展性；当每个Zone部署多节点时，提供了线性的水平扩展性。单机分布式一体化架构，让OceanBase数据库能够适应从个人小站点到银行核心系统和巨型电商网站等各种规模的业务。客户选用一种数据库产品，既可以在业务发展不同阶段满足不同性价比和高可用的要求，又可以随着业务规模扩展而平滑扩容，一次选择，终身受用。
            3. 区别于常见的利用多副本+双计算引擎构建的HTAP混合负载解决方案，OceanBase数据库采用了全自研的分布式SQL引擎，利用单计算引擎实现HTAP能力。

        2. OceanBase 4.0，单机与分布式的新拐点 - 申耀的科技观察
           https://zhuanlan.zhihu.com/p/554914189

    m. Related materials
        1. OceanBase: A 707 Million tpmC Distributed Relational Database System    [2022, 26 refs, VLDB22, Alibaba]
           https://vldb.org/pvldb/vol15/p3385-xu.pdf
            1. TPC-C test shows OceanBase performs well on a large scale with little jitter.
            2. Highlights
                1. Key challenges
                    1. Scale-out on commodity hardware and low TCO
                    2. Cross-region deployment and fault tolerance
                    3. Native compatible with mainstream RDMBS
                    4. Support all of large, medium, small organizations
                2. Key solutions
                    1. Scale-out shared nothing architecture
                    2. 3-AZ deployment
                    3. Multi-tenancy
                        1. System Tenant and Ordinary Tenant
                        2. Ordinary Tenant is like an MySQL instance. It can create users, databases, tables, etc.
                        3. Resource isolation
                            1. Resource Unit
                            2. An internal table for DBA to review resource allocation
                            3. OceanBase does NOT rely on Docker nor VM. It implements resource isolation within database. 
                    4. LSM-tree based storage engine
                        1. MemTable, SSTable, Row Cache, Block Cache
                        2. Microblock - 4KB or 8KB. Macroblock - 2MB, as the basic unit of allocation and GC.
                        3. Compaction optimization
                            1. Only a modified macroblock needs rewritten in compaction.
                                1. When the schema of a table is modified, e.g., adding or removing a column, or changing the attribute of a column, it is just a metadata operation
                            2. Compaction at off-peak time
                            3. OceanBase staggers the normal service and the merge time through a round-robin compaction mechanism
                    5. Paxos-based 2PC for transactions
                        1. For every partition, there is a replica in each zone, and these replicas form a Paxos group
                        2. Among all Paxos groups of an OceanBase cluster, one Paxos group is in charge of the management of the cluster, e.g., load balance, adding (removing) nodes, failure detection of nodes, and fault tolerance of failure nodes.
                        3. When a participant node fails, the Paxos protocol can quickly elect another replica to replace the original participant to continue providing services, and restore the state of the original participant.
                        4. OceanBase supports read committed and snapshot isolation
                        5. A normal read will only happen on the leader, and it refers to a query of general select
                            1. My questions
                                1. Secondary replicas cannot read? This is less performant. Where is the "weak consistency read" as shown in OceanBase Paetica paper?
                    6. OceanBase uses a fast parser ... 10 times faster as compared to a normal parser
                        1. Interesting, but no more details presented in paper
                3. TPC-C BENCHMARK TEST
                    1. 707M/60 TPS in TPC-C benchmark with 1554 node deployment, in total 55,944,000 warehouses and 499,000+ rows each.
                        1. Per node TPS ~7.8K.
                    2. "the cumulative variations of the performance throughput during the eight hours benchmark test measurement interval is less than 1%"
                        1. There are several background operations in OceanBase, e.g., minor compaction, merging compaction (merging several minor compactions into one), and copying minor compactions from a full replica to a data replica.
                            1. The CPU threads pool for all the background operations are reserved to minimize the performance throughput variations. 
                            2. The upper limit of the MemTable size should be chosen to be small enough for minor compaction to be completed before the RAM is exhausted by new transactions during minor compaction. 
                            3. Further, it must be large enough to exploit the RAM of each node and produce minimal minor compactions.
                4. Lessons learned
                    1. "stored procedure still has great value for OLTP applications"
                    2. "For example, a business system of Alipay was migrated from Oracle to OceanBase, and the data was compressed from 100TB to 33TB."
                    3. Internet vs. Non-Internet companies
                        1. "traditional IT companies pursue mainstream configuration and high cost performance"
                        2. "In traditional commercial enterprises and banks, users need to conduct business and access databases through special equipments such as bank terminals, ATM teller machines, and POS machines. Hundreds and thousands of concurrent requests to databases are relatively common, whereas requests exceeding tens of thousands of concurrent requests are scarce.""
                        3. "Compared with traditional databases, one of key features of OceanBase is the grayscale upgrade of software versions" ... "OceanBase avoids the “one-shot deal” upgrade of traditional databases"

            3. My questions
                1. Is tpmC referring to TPC-C benchmark? TPC-C is quite a common benchmark as you can also see it in CockroachDB paper, and many others.

            n. Related materials
                1. 我的七周七数据库 -- OceanBase: A 707 Million tpmC Distributed Relational Database System - 史成良
                   https://zhuanlan.zhihu.com/p/647403486
                    1. "这里提到了一个优化逻辑，在生成执行计划时，OB 会使用一个轻量框架来进行词法分析，之后会尝试匹配缓存中的执行计划（文中也提到其他数据库也有类似的逻辑），相比普通的解析器而言，这种方式会快 10 倍左右。（这里应该是 bypass 掉了语法和句法检查）下图是 SQL 引擎整体的模块结构", Figure 2
                    2. "接下来是多租户的部分，OB 主要有两类租户：系统租户和普通租户。系统租户主要是维护系统层面的数据表、系统函数和其他系统管理相关的资源。普通租户可以被理解成一个 MySQL 实例，能够能够创建自己的用户、按需创建数据库和数据表、维护自己的元数据、还有独立的系统变量。"
                        1. "OB 里面比较取巧地用了 Docker container，但是文中提到 OB实现了自己的租户隔离，实现了内存、CPU 和数据资源、事务管理的资源隔离。（这里我理解是在 docker 上做了魔改，其实没有什么特别大的魔法）"
                    3. "接着就是 LSM tree 的compaction，这里做了一个优化就是只对写操作的数据块做 compaction，其他就是常规的 LSM tree 的 compaction，感觉没有什么特别的地方。"
                    4. "OB 里面有多种不同的 replica，包括 full replica、data replica 和 log replica，下面是一个对比表", Table 1
                    5. "为了提供高可用的时间戳服务，OB 也将 Paxos 利用到了时间戳服务中，Paxos leader 通常位于数据表分片的相同 region 中，向 OB 的节点提供时间戳服务。"
                    6. "OB 把 Paxos 引入到两阶段提交中，如下图所示，在 OB 中，每个 2PC 的参与者都有一个 Paxos集群，在 2PC 过程中，如果某个参与者 fail 了，它可以直接切到自己的另一个 replica。"
                        1. This is like Spanner 2PC


2. AnalyticDB-V: A Hybrid Analytical Engine Towards Query Fusion for Structured and Unstructured Data    [2020, 67 refs, VLDB20, Alibaba]
   https://www.vldb.org/pvldb/vol13/p3152-wei.pdf
    1. AnalyticDB to support vector serving. Hybrid SQL queries, a new ANNS search algorithm, optimizer execution plan integration
    2. Highlights
        1. Key challenges
            1. Support vector in AnalyticDB
                1. high dimensional vectors
                2. hybrid queries
                3. searches like ANNS
        2. Key solutions
            1. hybrid queries for SQL and vectors
                1. See Section 2.2 SQL dialects
            2. lambda framework for streaming layer and batching layer
                1. Baseline data + incremental data
                2. Baseline data uses VGPG index.
                3. Incremental data uses HNSW index.
            3. clustering-based partitioning
                1. Use 256 K-means centroids to build 256 partitions
                2. Index building and data manipulation happens within each partition.
            3. A new ANNS algorithm - VGPQ
                1. HNSW is neighborhood based vs PQ is based on lossy reduction to low dimension
                2. VGPQ is based on IVFPQ [23]. It requires training encoding PQ codebook offline.
                3. Storage design for VGPQ
                    1. See section 4.3
            4. Accuracy-aware cost-based hybrid query optimization
                1. Insert ANN scan node into physical plan. Plan A,B,C,D in the paper Section 5.1 are evaluated through cost model. Cost model construction can be see Table 1.
                2. It's an interesting contribution by this paper as how to construct query optimizer and cost modeling for hybrid SQL + vector queries.

    n. Related materials
        1. AnalyticDB: Real-time OLAP Database System at Alibaba Cloud    [2019, 29 refs, VLDB19, Alibaba]
           https://www.vldb.org/pvldb/vol12/p2059-zhan.pdf
            1. Logged before

        2. 可用的向量数据库(vector DB)有哪些？ - zeta
           https://www.zhihu.com/question/610087406/answer/3446465314
            1. AnalyticDB-V 显然是 AnalyticDB 针对 V（vector）的优化版本


3. Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases    [2017, 298 refs, AWS]
   https://www.amazon.science/publications/amazon-aurora-design-considerations-for-high-throughput-cloud-native-relational-databases
    1. The biggest takeaway - THE LOG IS THE DATABASE. Good. And it writes into quite detail about how to building the logging storage.
       Another take away is, the previous shared nothing MySQL DB architecture is transformed into Aurora shared logging architecture, which is similar to the typical shared disk architecture.
    2. Highlights
        1. New durability challenges and solutions
            1. Key challenges
                1. Read 2 out of 3 by quorum is inadequate. Losing AZ+1 is not recoverable, as we don't know the last replica is new or stale. Section 2.1.
            2. Key solutions
                1. Use 10GB segments, which is replicated to 6 copies in 3 AZs (Protection Groups (PGs)). 4/6 quorum writes, 3/6 reads. SSD backed, 10Gbps network.
                    1. My questions
                        1. 6 copies is very much more expensive than 3 copies. Is it economic enough?
        2. THE LOG IS THE DATABASE (famous and referenced in many follow-ups)
            1. Key challenges
                1. MySQL generates many different actual IOs.
                    1. Write both data pages and redo logs (WAL)
                    2. A redo log consists of both after-image and before-image
                    3. Bin log used for replication
                2. The IO results in a point of synchronization that stalls pipeline
                3. Duplicate data written for replication and write to disk
                    1. It's clear to see Figure 2.
                        1. There are multiple types of logs.
                        2. Both disk write and replication need a copy of logs.
            2. Key solutions
                1. Don't write disk pages, only write redo logs to a shared storage.
                2. Only writing logs are synchronized operation, others can be async.
                3. For secondaries, log is database, disk pages are cache.
        3. Storage nodes
            1. Key solutions
                1. 4/6 quorum writes
                2. Delay GC until disk is almost full. 
                3. Avoid background processing if foreground is busy.
        4. THE LOG MARCHES FORWARD
            1. Logging design points
                1. Each segment of each PG only sees a subset of log records in the volume that affect the pages residing on that segment
                    1. The implication is PG recovery doesn't need to scan full logs
                    2. Each log record contains a backlink that identifies the previous log record for that PG
                2. 没有LSN的分配值会大于当前VDL加上一个常数（称为LSN分配限制LAL，目前设置为100万）。这个限制确保数据库不会过于超前于存储系统，并引入反压，以限制如果存储或网络无法跟上时的写入流量。
                3. it enforces a similar guarantee: a page in the buffer cache must always be of the latest version
                    1. Why?
                        1. First, to serve reads with the latest data.
                        2. Secondly, this protocol ensures that all changes in the page have been hardened in the log
                4. Protection Group Min Read Point LSN (PGMRPL) and represents the "low water mark" below which all the log records of the PG are unnecessary
                5. VDL <= VCL
                    1. LSN - log sequence number
                       CPL - Consistency Point LSN
                       VCL - Volume Complete LSN
                       VDL - Volume Durable LSN
                       SCL - Segment Complete LSN
                       PGMRP - PG Min Read Point LSN
                    2. mini-transaction - MTR
                        1. Each database-level transaction is broken up into multiple mini-transactions (MTRs) that are ordered and must be performed atomically
                        2. Each mini-transaction is composed of multiple contiguous log records (as many as needed).
                        3. The final log record in a mini-transaction is a CPL.
            2. Recovery is NOT using ARIES [7]
                1. 传统数据库的一个简化原则是，在正向处理路径和恢复过程中都使用相同的重做日志应用程序
                    1. "A great simplifying principle of a traditional database is that the same redo log applicator is used in the forward processing path as well as on recovery where it operates synchronously and in the foreground while the database is offline"
                    2. This is a good capture.
                2. In Aurora, the redo log applicator is decoupled from the database and operates on storage nodes, in parallel, and all the time in the background
        5. Others
            1. The database engine is a fork of "community" MySQL/InnoDB and diverges primarily in how InnoDB reads and writes data to disk.
                1. My questions
                    1. Like Alibaba PolarDB, both are forking from MySQL InnoDB.
            2. MTR is an InnoDB internal construct. It's reused in Aurora logging here.
            3. Archive old logs to S3 and restore from there. Support point-in-time restores.

    n. Related materials
        1. Amazon Aurora云原生数据库 论文解读 - SallyLeoqqdd
           https://zhuanlan.zhihu.com/p/687493648
            1. Translation of the parent paper

        2. Amazon Aurora论文盲点总结 - Diver
           https://zhuanlan.zhihu.com/p/623336613

        3. 浅谈Amazon Aurora - Trafalgar
           https://zhuanlan.zhihu.com/p/338582762


4. PolarDB-SCC: A Cloud-Native Database Ensuring Low Latency for Strongly Consistent Reads    [2023, 3 refs, VLDB23, Alibaba]
   https://www.vldb.org/pvldb/vol16/p3754-chen.pdf
    1. RO node to read-after-write against RW node. The solution is to track timestamps per page, implemented by LSN. I.e., Read-wait.
    2. Highlights
        1. Key challenges
            1. Strong consistency from RW node to RO node. Read-after-write. Don't be today's typical eventual consistency.
            2. RO node can delay more if log replay delays
            3. Scaleout the RO nodes, allow more RO nodes, in serverless usecase.
        2. Key solutions - Improved read-wait 
            1. hierarchical modification tracker
                1. Global level tracks DB timestamp, then table level, then page level timestamps
                2. Table and page level timestamp are actually implemented by LSN.
                3. Per query, if an upper level timestamp is satisfied, then no need to drill down to a lower level.
            2. Linear Lamport timestamp (LLT)
                1. Challenge: RO fetching timestamp from RW has cost, and it can accumulate many requests. 
                2. Solution: If one timestamp is fetched at RO, cache it. All requests earlier than it can be served by the cached timestamp.
            3. RDMA-based log shipment protocol

    n. Related materials
        1. PolarDB-SCC: A Cloud-Native Database Ensuring Low Latency for Strongly Consistent Reads | VLDB'23 - Dabtwice
           https://zhuanlan.zhihu.com/p/661033533
            1. A full translation

        2. PolarDB-SCC在强一致性读方向上的探索与落地 - 孙川
           https://zhuanlan.zhihu.com/p/678214571

    m. Related materials
        1. PolarDB-MP: A Multi-Primary Cloud-Native Database via Disaggregated Shared Memory    [2024, 0 refs, Alibaba, SIGMOD24 best paper]
           https://dl.acm.org/doi/10.1145/3626246.3653377
           https://www.youtube.com/watch?v=eKxdwhuPpQ0
            1. Very good paper. An architecture advancement from AWS Aurora "Log is database". The multi-primary is backed with a RDMA shared memory pool, and concurrency control by page locks rather than OCC. No distributed transaction is needed, as a node can access all pages.  
            2. Highlights
                1. Related works
                    1. Existing multi-primary architecture 
                        1. shared-nothing
                            1. Spanner[11], DynamoDB [15], CockroachDB [15], PolarDB-X [6], Aurora Limitless [2], TiDB [19] and OceanBase [55]
                            2. By partitioning and single primary per partition
                        2. shared-storage
                            1. IBM pureScale [20], Oracle RAC [9], AWS Aurora Multi-Master (Aurora-MM) [3] and Huawei Taurus-MM [16]. IBM pureScale
                            2. Aurora-MM utilizes optimistic concurrent control for write conflict, thus inducing a substantial abortion rate when conflicts occur.
                            3. Taurus-MM adopts the pessimistic concurrent control but it relies on page stores and log replays for cache coherence
                2. Key challenges
                    1. Multi-primary on disaggregated shared memory
                    2. Process transaction within a node without distributed transaction, because the node can access all data.
                        1. Interesting advantage as compared to Google Spanner
                3. Key solutions
                    1. The Polar DB servers (Polar Multi-Primary Fusion Server (PMFS)) compose a shared memory pool (Disaggregated Buffer Pool (DBP)) accessed via RDMA. A node is able to access all pages in the shared memory pool.
                        1. Note, see Figure 2, PolarDB servers and PMFS are two separated component. PMFS is a shared memory pool to manage buffer pages, locking, and transaction ordering.
                    2. The access unit is page. Locking unit is page or row (PLock, RLock). A transaction is performed by first setting locks on the remote pages.
                        1. Lock states are tracked in PMFS (rather than PolarDB server), See Figure 5. There are both shared lock and exclusive lock. A transaction follows two-phase locking protocol.
                        2. Technique "Lazy releasing"
                            1. We know a page unlocked is probably soon to be used again. Rather than let PolarDB server notify PMFS every time, PolarDB server internally maintain a lock reference count to this page.
                            2. When another node wants to lock this page, PMFS sends a notification to the lock holder node. If seeing zero reference count, lock can be released.
                        3. "Lock Fusion" is just the "Lock Manager" running in PMFS. "Transaction Fusion" is just the "Transaction Manager". "Buffer Fusion" is just the shared memory pool in PMFS. Buzzwords.
                    3. A page's LLSN is attached in this page's metadata. Each node, while updating the page, can increment the LLSN. For a single page, the LLSN is full ordering. For page to page, the LLSN doesn't have order.
                    4. Persistency only writes logs (redo + undo logs) rather than disk pages. A page's log is tagged by LLSN. Per recovery, PolarDB ensures a page's all redo logs are replayed in LLSN order, before pushing the page to DBP. Recovery follow ARIES protocol.
                        1. "Log is database" from AWS Aurora.
                        2. PolarDB ensures all logs of a page are persisted before pushing the updated page to DBP.
                            1. Similar with AWS Aurora paper "a page in the buffer cache must always be of the latest version"  
                        3. Note, PolarDB has both redo and undo logs.
                        4. "the key to recovery in this context is applying the redo logs for the same page in the order they were generated, while logs from different pages can be applied in any sequence"
                    5. Any PMFS can load any page, and once loaded, it registers the page to DBP for reuse by other servers
                        1. DBP tracks each page's active nodes. A loaded page is registered here. So that other nodes can find it.
                    6. Commit timestamp is requested from a Timestamp Oracle (TSO).
                        1. My questions
                            1. How does the commit wait, external consistency problem in Spanner work here?
                                1. So far PolarDB should be single DB deployment. It needs RDMA. A single TSO should be fine. It doesn't involve the tricky external consistency problem in Spanner.
                    7. PolarDB-MP also implements MVCC. Each node keeps local transactions in transaction information table (TIT). TIT has a version number to tell different transactions targeting the same slot. A row has CTS to tell its "version", and a transaction has its read view CTS, to tell if the row is visible to the transaction.
                        1. PolarDB-MP doesn't store the previous versions of a row. Instead, the transaction uses undo logs to construct the previous versions of the page. In this way, PolarDB-MP also doesn't need to GC older version pages.
                            1. This is an interesting design. See Section 4.1 "Transaction visibility".
                        2. Note, MySQL InnoDB supports MVCC natively.
                4. Others
                    1. See Figure 4, in Buffer Fusion design, PolarDB nodes can cache entry pointers locally (LBP). Thus, "When a new version of a page is stored in the DBP, Buffer Fusion remotely invalidates the copies on other nodes via the address of the invalid flag".
                        1. My questions
                            1. What does the "Invalid addr" in Figure 4 do? Not found description in paper

            3. My questions
                1. PolarDB architecture in this paper is quite different from its previous. What do the PolarFS, ParallelRaft, Chunk Server become now?
                2. What is DBP shared memory pool built on top of? RAMCloud, FaRM, Redis or something?
                3. It looks like LLSN (rather than LSN) is a side effect from multi-primary. Because updates are concurrent, so no full ordering LSN across all pages exist. Is there a better solution?
                4. In evaluation, the most tested is only 8 nodes. This is far less than than the partition count in Spanner, if to say PolarDB-MP replaces cross-partition distributed transaction to shared-memory design.
                    1. Essentially, the loaded pages are partitioned to different nodes. So this is still partition.
                    2. If to apply a big transaction, the node has to load all related pages, which also invalidates the cached pages at other nodes. Such threshing can be a problem.
                    3. More, the locking needed in node transaction is essentially similar with 2PC. Fundamentally there shouldn't be saving compared to Spanner architecture. And, the hidden partitioning loses control in this design.
                5. How to create a global snapshot of the database??

            n. Related materials
                1. 内附原文｜详解SIGMOD'24最佳论文：PolarDB如何破解多主架构经典难题？ - 阿里云瑶池数据库 - 知乎
                   https://zhuanlan.zhihu.com/p/705525367

                2. 【论文笔记】PolarDB-MP: A Multi-Primary Cloud-Native Database via Disaggregated Shared Memory - MaDianjun
                   https://zhuanlan.zhihu.com/p/713113741

                3. PolarDB-MP A Multi-Primary Cloud-Native Database - Hugo
                   https://zhuanlan.zhihu.com/p/706235101
                   1. "polar-mp 有点像借助 rdma 实现了一个 mesi 协议？"
                   2. "其实taurus mm 的方案也不错，polar mp的实验用一个昂贵的remote buffer pool：pmfs 和 taurus mm 没有 额外的buffer pool 方案进行对比，指出taurus mm 的缺点是有log apply的cpu，以及pull log和 read page的io，有点略微欺负人[可怜]， 我认为同样的成本下面，taurus mm 加一个可回放remote buffer pool service 也能有较大的提升空间"

            m. Related materials
                1. [16] Taurus MM: bringing multi-master to the cloud    [2023, 1 refs, VLDB23, Huawei]
                   https://www.vldb.org/pvldb/vol16/p3488-depoutovitch.pdf
                   https://www.youtube.com/watch?v=e3Yx5aLJKxI
                    0. From the parent paper
                        1. "When a node requests a page that has been modified by another node, it must request both the page and corresponding logs from the page/log stores, and then apply the logs to obtain the latest version of the page. This process typically involves storage I/Os, which can impact performance, and the log application also consumes extra CPU cycles."
                        2. "In their evaluations [16], the throughput of Taurus-MM's eight-node cluster is approximately 1.8× that of a single node under the SysBench write-only workload with 30% shared data, illustrating the trade-offs and challenges in optimizing multi-primary cloud databases."
                    1. Multi-master DB by vector+scalar clock and page+row locking. The paper went into details about how to process ordering, versions, and locks. Taurus is offered as GaussDB for MySQL in Huawei cloud service.
                        1. So, PolarDB-MM is essentially Taurus MM and adding a memory cache pool for pages and locks. It's reasonable that PolarDB-MM performs much better than Taurus MM. 
                        2. Reducing to the same hardware level, From Taurus MM Figure 7, however, you can see "Partitioned" yields the best performance compared to MM any shared%. Can we conclude that Multi-master is actually NOT a performant approach?
                            1. Interesting thinking here
                    2. Highlights
                        1. Key challenges
                            1. a shared-storage multi-master database optimized for cloud environments
                            2. reducing network traffic
                        2. Key solutions
                            1. Vector-scalar (VS) clocks algorithm
                                1. Motivation: To create clocks that have the size benefits of scalar and support the causality and snapshots features of vector clocks, we introduce VS (vector-scalar) clocks.
                                2. Solution: Based on vector clock. Node i carries a vector clock_i[N]. Upon receiving message, clock_i[i] also increments so it's bigger than all other clock_i[*], which means clock_i[N] is behaving as a scalar clock.
                                    1. vectors are used to establish causality and create global snapshots, while scalars are used for establishing the order of events when causality is known already
                                    2. My questions
                                        1. So, what the author wants is just a vector clock + scalar clock?
                                        2. How to handle the compression of vector clock if there are many nodes?
                                3. What's the relation between logical clock, vector clock, scalar clock?
                                    1. Logical clocks are a general concept used in distributed systems to order events and capture the notion of time without relying on physical clocks. They help in maintaining a consistent view of the sequence of events across different nodes in a distributed system.
                                        1. Scalar clocks, also known as Lamport clocks, are a type of logical clock that use a single integer counter to timestamp events. They are simple and space-efficient but cannot capture the causal relationships between events, which means they lose causality. 
                                        2. Vector clocks are another type of logical clock that use a vector of integers, with each element in the vector corresponding to a node in the system. This allows vector clocks to capture causal relationships between events by maintaining a separate counter for each node, thus preserving causality.
                                4. How VS clock is being used in Taurus?
                                    1. "Consequently, pages and log records can be stamped with the scalar component of the VS clock of the node that modified the page. This timestamp serves as the LSN for the log record and the page."
                                    2. "Each master, before sending an LFB to a log store, stamps it with the current vector value of its VS clock" ... "Fig. 6 has an example of the criteria used to check if an LFB from master M2 can be applied immediately on master M3"
                                    3. "The transaction then waits until the local master's VS clock passes this timestamp and, by that time, the local master is aware of all database changes that happened before the time when the transaction began"
                            2. Hybrid page-row locking algorithm
                                1. Backgrounds
                                    1. Page locks guard the physical consistency of a page by serializing modifications of the page among transactions. 
                                    2. Row locks guard the transactional consistency of user data and are held until the end of the transaction.
                                    3. A global lock manager (GLM), and, each master node has a local lock manager (LLM)
                                2. Techniques
                                    1. "Lazy releasing" like PolarDB-MM's: A master is not required to release a page lock immediately. If it is likely to need the lock again soon, it may just keep it and only release it when the GLM reclaims it.
                                        1. See Section "5.2.5 Row lock cleanup". Each master periodically (e.g., every second) sends the IDs of terminated transactions to the GLM, which then garbage collects its cached row locks.
                                    2. "Row locks follow page locks"
                                        1. When a master acquires a page lock on a page P, it also receives the list of row locks on P.
                                        2. GLM manages only the page lock. Row locks are managed by LLM.
                                            1. Note, GLM can cache and merge row lock info and redistribute to master nodes. See Section "5.2.5 Row lock cleanup" and "5.2.6 Handling of shared row locks".
                                        3. How does a master know if a row is locked by someone else?
                                            1. After the master locked P, P will return the list of row locks on the page. Then the master can follow the locks to find their original owner.
                                            2. To grant a row lock requested by a local transaction, the master must hold a covering page lock
                            3. Cloud-native multi-master database architecture
                                1. My questions
                                    1. See Figure 2, why it needs Page Stores? Compared to PolarDB-MM and AWS Aurora, the later two only need to write logs while considering pages as cache.
                                        1. "Like single-master Taurus, logs of all masters are sent to Page Stores, which update pages continuously and serve read page requests."
                                        2. So, Page Store also acts as a caching layer. But it doesn't require pages to always be updated with logs (see ordering in Figure 3), and pages can be stored on disks rather than PolarDB-MM in memory.
                                            1. Async flush to Page Store: "When the buffer is full, it is sent to the Page Stores (Step 4)"
                                            2. "The master waits for a reply from one of the Page Stores and releases the buffer (Step 5)" ... You can see it implies Page Store is the final storage, it must be persisted on disk, and has replicas and recovery, and the master node buffer is just a memory cache.
                            4. My questions
                                1. How does Gossip work with VS clock? It doesn't look like need to increment the clock upon receiving just a ping message.
                                2. Figure 7: Taurus MM performance on SysBench and TPC-C. Partitioned yields much better performance than MM any shared. Then why do we need to build Multi-master after all?

                2. [3] Amazon Aurora Multi-Master: Scaling Out Database Write Performance, by Eric Boutin and Steve Abraham    [2019]
                   https://d1.awsstatic.com/events/reinvent/2019/REPEAT_1_Amazon_Aurora_Multi-Master_Scaling_out_database_write_performance_DAT404-R1.pdf
                    0. From the parent paper
                        1. "However, a significant downside is that, in scenarios with conflicts, such as when different nodes attempt to modify the same data page simultaneously, it results in a high rate of transaction aborts."
                        2. "According to Taurus-MM 's research [16], Aurora-MM's four-node cluster only shows a throughput improvement of less than 50% compared to a single node under the SysBench read-write workload with a mere 10% data sharing between nodes."

        2. PolarDB-IMCI: A Cloud-Native HTAP Database System at Alibaba    [2023, 7 refs, SIGMOD23, Alibaba]
           https://arxiv.org/abs/2305.08468
            1. Logged before

        3. PolarDB-X: An Elastic Distributed Relational Database for Cloud-Native Applications    [2022, 13 refs, Alibaba]
           https://users.cs.utah.edu/~lifeifei/papers/icde22-polardbx.pdf
            1. A summary of main designs in PolarDB.
            2. Highlights
                1. Key challenges
                    1. To be cloud native
                2. Key solutions
                    1. Cross-DC Transactions with HLC-SI
                        1. My questions
                            1. But in PolarDB-MP 2024 paper, it's still using centralized TSO?
                            2. How to handle cross-datacenter clock drift / clock skew / uncertainty interval? I didn't find it in paper.
                                1. CockroachDB using HLC also needs Commit Wait like Spanner
                                   https://groups.google.com/g/cockroach-db/c/ALLI0aHEsL8?pli=1
                                2. The One Crucial Difference Between Spanner and CockroachDB
                                   https://authzed.com/blog/prevent-newenemy-cockroachdb
                                    1. Cockroach does NOT provide external consistency for transactions involving non-overlapping keys.
                                        1. While Spanner commit wait does it. Commit Wait ensures ordering is global and physical.
                                        2. This implies CockroachDB is NOT using Commit Wait.
                                    2. Cockroach does provide external consistency for transactions with overlapping keys, sometimes termed having a "causal relationship".
                                        1. This implies CockroachDB resolves external consistency by propagating causal consistency timestamps. CockroachDB generates timestamps using HLC.
                                        2. When a transaction is committed, CockroachDB doesn't need to wait in the same way Spanner does. Instead, it ensures that the commit timestamp of the transaction is causally consistent with the HLC across nodes. If a transaction sees a timestamp from another node that is in the future (which can happen due to clock skew or network delays), it adjusts its HLC accordingly but does not require a commit wait.
                                    3. Cockroach timestamps can only be off of cluster consensus time by up to the max_offset for the cluster - a clock skew beyond which a node is removed from the cluster for being too far off.
                                3. CockroachDB's consistency model
                                   https://www.cockroachlabs.com/blog/consistency-model/
                                    1. CockroachDB: The Resilient Geo-Distributed SQL Database
                                       https://dl.acm.org/doi/pdf/10.1145/3318464.3386134
                                        1. "When a transaction encounters a value on a key at a timestamp above its provisional commit timestamp but within its uncertainty interval, it performs an uncertainty restart"
                    
                    2. Elasticity with RO nodes, multi-tenancy, tenant migration
                        1. Multi-tenancy
                            1. "not supporting cross-tenant transactions"
                            2. "each tenant must be bound to only one specific RW node"
                            3. "different RW nodes operate on disjoint portions of the data (divided by tenants)"
                            4. My questions
                                1. Isn't the "tenant" simply a DB partition? This is hardly a multi-tenancy.
                    3. HTAP with PolarDB-ICMI
                        1. See the PolarDB-ICMI paper.
                3. My questions
                    1. What's the relation between PolarFS vs Pangu Filesystem? Can PolarDB be converged to running on Pangu?

            n. Related materials
                1. PolarDB-X 存储引擎核心技术 | Lizard 分布式事务系统
                   https://zhuanlan.zhihu.com/p/656922735
                   https://zhuanlan.zhihu.com/p/654126910
                    1. Logged before

        4. PolarDB CloudJump: Optimizing Cloud Databases for Cloud Storages    [2022, 5 refs, VLDB22, Alibaba]
           https://www.vldb.org/pvldb/vol15/p3432-chen.pdf
            1. The below article has already been a full summarize.
            2. My questions
                1. Per shipping on-premises database to cloud, how to handle below challenges like SnowFlake
                    1. Resource elasticity, with economic efficiency?
                    2. Data tiering, cold/hot, leveraging S3?
                    3. Super large scale?
                    4. Load balancing
                   However, this paper is mainly focusing on thread/task parallelism optimization. And re-iterating the same old PolarDB designs.
                2. PolarDB is built atop MySQL InnoDB: "PolarDB incorporates MySQL together with its default B-tree-based storage engine, InnoDB, as its computation layer"

            n. Related materials
                1. PolarDB-CloudJump：优化基于云存储服务的云数据库(发表于VLDB2022) - 陈宗志
                   https://zhuanlan.zhihu.com/p/535426034
                    1. Logged before

        5. PolarDB Serverless: A Cloud Native Database for Disaggregated Data Centers    [2021, 91 refs, Alibaba]
           http://www.cs.utah.edu/~lifeifei/papers/polardbserverless-sigmod21.pdf
            1. Logged before

        6. POLARDB Meets Computational Storage: Efficiently Support Analytical Workloads in Cloud-Native Relational Database    [2020, 100 refs, FAST20, Alibaba]
           https://www.usenix.org/conference/fast20/presentation/cao-wei
            1. Logged before

        7. PolarFS: an Ultra-low Latency and Failure Resilient Distributed File System for Shared Storage Cloud Database    [2018, , VLDB18, Alibaba]
           https://www.vldb.org/pvldb/vol11/p1849-cao.pdf
            1. Logged before.


5. Primary Data Deduplication – Large Scale Study and System Design    [2012, 245 refs, ATC12, Microsoft]
   https://www.usenix.org/system/files/conference/atc12/atc12-final293.pdf
    1. Dedup study from Windows Server filesystems. Targeting primary storage rather than backup systems.
    2. Highlights
        1. Background
            1. Data from 15 globally distributed file servers for over 2K users in 1 large multinational corporation.
            2. Using Rabin hash to cut dedup blocks, note this is variable chunk size, content dependent hashing.
        2. Key findings
            1. Sub-file deduplication is significantly more effective than whole-file deduplication
            2. High deduplication savings previously obtained using small ∼4KB variable sized chunking are achievable with 16-20x larger chunks, after chunk compression is included
            3. Chunk compressibility distribution is skewed with the majority of the benefit of compression coming from a minority of the data chunks
            4. Primary datasets are amenable to partitioned deduplication with comparable space savings and the partitions can be easily derived from native file metadata within the dataset
                1. partition methods
                    1. partitioning by file type (extension)
                        1. See, Table 3, this is more effective. This is actually an interesting finding. Partition by file extension is very simple but effectively improves dedup. Cloud storage vendors can hardly see file type, but commercial storage vendors running on cloud, e.g. NetApp, can implement this level of optimization. This can become a unique advantage in future.
                    2. partitioning by directory hierarchy where partitions correspond to directory subtrees with total bytes at most 10% of the overall namespace
                2. Little saving as in Table 4: Dedup savings benefit of cross-server deduplication, as fraction of original dataset size
            5. See Figure 2, high deduplication savings achieved with 4KB chunk size are attainable with larger 64KB chunks with chunk compression, as the loss in deduplication opportunities arising from use of larger chunk sizes is canceled out by increased compressibility of the larger chunks
        3. Other findings
            1. Our earlier data analysis has shown that for primary datasets, whole file and subfile fixed-size chunk deduplication were significantly inferior to sub-file variable size chunk deduplication
        4. Dedup system design
            1. Chunk Indexing
                1. Log-structured organization
                2. Low RAM footprint index
                3. Prefetch cache
            2. Two-phase Deduplication
                1. Deduplication within a partition
                2. Reconciliation of partitions
                    1. deduplication across partitions
```

Investigation on partition migration/movement without downtime.

```
1. VM live migration
    1. Wikipedia
       https://en.wikipedia.org/wiki/Live_migration
        1. Stop-and-copy phase introduces downtime ranging from a few ms to seconds to transfer dirty pages
        2. Post-copy migration is the dest "pull" type of migration.
            1. It doesn't need the downtime at source->dest handover, but each "pull" later can introduce another type of suspension of delay.
            2. Another problem of dest "pull" model is, if the destination fails during live migration, pre-copy can recover the VM, whereas post-copy cannot

2. Existing distributed databases
    1. Megastore: Providing Scalable, Highly Available Storage for Interactive Services
       http://cidrdb.org/cidr2011/Papers/CIDR11_Paper32.pdf
        1. Table partitions are replicated via Paxos.
            1. Good. This naturally allows add/move machine instances without interruption.
    
    2. Spanner: Google's Globally-Distributed Database
       https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf
        1. "Load-based splitting"
           https://cloud.google.com/spanner/docs/schema-and-data-model
            1. Didn't find details
        2. Movedir
            1. "Directories are the unit of data movement between Paxos groups"
        3. Paxos
            1. Like Megastore, partitions are managed by Paxos
        4. [25] SMART migrate
            1. "Movedir is also used to add or remove replicas to Paxos groups [25], because Spanner does not yet support in-Paxos configuration changes" 
            2. The SMART way to migrate replicated stateful services    [2006, 116 refs, Microsoft]
               https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/eurosys2006.pdf
                1. SMART migrates RSL (replicated state machine). So this implies Spanner is using Paxos quorum to serve its directories, which then migration happens as Paxos Reconfiguration or migrating an RSL replica.

    3. F1 Query: Declarative Querying at Scale
       https://www.vldb.org/pvldb/vol11/p1835-samwel.pdf
        1. Didn't find non-interruptive partition move/migrate/split. OK as F1 is served by Spanner/BigTable

    4. Bigtable: A Distributed Storage System for Structured Data
       https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf
        1. Partitions (tablet) support split and move
            1. "Incoming read and write operations can continue while tablets are split and merged"
            2. "Speeding up tablet recovery: If the master moves a tablet from one tablet server to another, the source tablet server first does a minor compaction on that tablet. This compaction reduces recovery time by reducing the amount of uncompacted state in the tablet server's commit log. After finishing this compaction, the tablet server stops serving the tablet. Before it actually unloads the tablet, the tablet server does another (usually very fast) minor compaction to eliminate any remaining uncompacted state in the tablet server's log that arrived while the first minor compaction was being performed. After this second minor compaction is complete, the tablet can be loaded on another tablet server without requiring any recovery of log entries."
        2. So, partition movement does have a short downtime, which is handled alike VM migration. 

    5. CockroachDB
        0. Source lists
            1. CockroachDB: The Resilient Geo-Distributed SQL Database
               https://dl.acm.org/doi/pdf/10.1145/3318464.3386134
        1. No source found in papers nor articles.
        2. *Guessed*: the partition forms a Paxos/Raft quorum. Partition migration is simply the process of Paxos Reconfiguration, which is naturally zero downtime.
            1. The problem is, the running memory cost is N replicas, and each update needs to pass through all Paxos replicas.

    6. YugabyteDB 
        1. None found.

    7. TiDB
        0. Source lists
            1. TiDB: A Raft-based HTAP Database
               https://www.vldb.org/pvldb/vol13/p3072-huang.pdf
        1. See Dynamic Region Split and Merge. The Region is a Raft/Paxos group. So live migration is simply Paxos Reconfiguration, zero downtime involved.

    8. OceanBase
        0. Source lists
            1. OceanBase Paetica: A Hybrid Shared-nothing/Shared-everything Database for Supporting Single Machine and Distributed Cluster
               https://www.vldb.org/pvldb/vol16/p3728-xu.pdf
            2. OceanBase: A 707 Million tpmC Distributed Relational Database System
               https://vldb.org/pvldb/vol15/p3385-xu.pdf
        1. None found.

    9. AnalyticDB
        0. Source lists
            1. AnalyticDB: Real-time OLAP Database System at Alibaba Cloud
               https://www.vldb.org/pvldb/vol12/p2059-zhan.pdf
            2. AnalyticDB-V: A Hybrid Analytical Engine Towards Query Fusion for Structured and Unstructured Data
               https://www.vldb.org/pvldb/vol13/p3152-wei.pdf
        1. None found

    10. PolarDB
        0. Source lists
            1. PolarDB-SCC: A Cloud-Native Database Ensuring Low Latency for Strongly Consistent Reads
               https://www.vldb.org/pvldb/vol16/p3754-chen.pdf
            2. PolarDB Serverless: A Cloud Native Database for Disaggregated Data Centers
               https://users.cs.utah.edu/~lifeifei/papers/polardbserverless-sigmod21.pdf
            3. PolarDB-X: An Elastic Distributed Relational Database for Cloud-Native Applications
               https://users.cs.utah.edu/~lifeifei/papers/icde22-polardbx.pdf
        1. None found

    11. FoundationDB
        0. Source lists
            1. FoundationDB: A Distributed Unbundled Transactional Key
               https://www.foundationdb.org/files/fdb-paper.pdf
        1. None found

    12. ZippyDB
        0. Source lists
            1. How we built a general purpose key value store for Facebook with ZippyDB
               https://engineering.fb.com/2021/08/06/core-infra/zippydb/
        1. None found

    13. AWS Aurora
        0. Source lists
            1. Partition and shard consolidation on Amazon Aurora
               https://docs.aws.amazon.com/whitepapers/latest/amazon-aurora-mysql-migration-handbook/partition-and-shard-consolidation-on-amazon-aurora.html
            2. Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases
               https://pages.cs.wisc.edu/~yxy/cs764-f20/papers/aurora-sigmod-17.pdf
        1. None found

    14. AWS Redshift
        0. Source lists
            1. Amazon Redshi! Re-invented
               https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf
        1. None found

    15. HBase
        1. None found

    16. Cassandra
        0. Source lists
            1. Cassandra - A Decentralized Structured Storage System
               https://www.cs.cornell.edu/projects/ladis2009/papers/lakshman-ladis2009.pdf
        1. None found

    17. DynamoDB
        0. Source lists
            1. Dynamo: Amazon's Highly Available Key-value Store
               https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
            2. Amazon DynamoDB: A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service
               https://www.usenix.org/system/files/atc22-elhemali.pdf
        1. None found

--------

1. VM大规模在线迁移 - edwu
   https://zhuanlan.zhihu.com/p/660302695
    1. Google VM migration paper
    2. Highlights
        1. 源端阶段（Source brownout） -> 停机阶段（Blackout） -> 目标端阶段（Target brownout）
        2. 预复制 vs 后复制
            1. 一小部分工作负载具有足够高的写入速率，导致黑屏时间非常长
            2. 后复制[8]，虚拟机可以在所有脏内存迁移完成之前在目标上恢复。我们使用后台获取机制来继续从源迁移内存内容。如果虚拟机的虚拟CPU尝试访问尚未获取的页面，就会从源请求该页面，直到复制到虚拟机之前，该虚拟CPU将被阻塞。

2. NetMigrate: In-Memory Key-Value Store Live Migration with NetMigrate
    1. Live migration with zero downtime on KV stores
        1. Logged elsewhere
    2. Related works
        1. Fulva: Efficient live migration for in-memory key-value stores with zero downtime
            1. Logged elsewhere
        2. Rocksteady: Fast Migration for Low-latency In-memory Storage
            1. Logged elsewhere

--------

1. Summary of migration approaches to pursuit zero downtime.
    1. Src driven migration: Copy states to dest first, and then handover to dest. A short downtime happens in the handover state.
    2. Dest driven migration: Redirect writes to dest first, and then dest uses page faults to pull what it's missing. There is no downtime during ownership transfer, but the page fault "pull" can introduce suspension delay.
    3. Hybrid of 1 and 2: See NetMigrate.
    4. Paxos backed replication: The partition is a Paxos quorum. Migration is simply Paxos Reconfiguration, which naturally has zero downtime.
        1. My questions
            1. Is it possible for a single node partition to temporarily transition to Paxos quorum backed partition, so as to leverage its zero downtime migration?
                1. But the "transition" itself implies a remote node must sync state with source node. This implies downtime exists just like Approach 1.
```
