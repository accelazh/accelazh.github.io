---
layout: post
title: "Recent Paper Reading: Alibaba Cloud DBs, and A Few Investigations"
tagline : "Recent Paper Reading: Alibaba Cloud DBs, and A Few Investigations"
description: "Recent Paper Reading: Alibaba Cloud DBs, and A Few Investigations"
category: "Paper Reading"
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
        1. Amazon Aurora: On Avoiding Distributed Consensus for I/Os, Commits, and Membership Changes    [2018, 45 refs, AWS]
           https://pages.cs.wisc.edu/~yxy/cs839-s20/papers/aurora-sigmod-18.pdf
            1. In details to explain how Aurora write protection groups and do "Log is database"
            2. Highlights
                1. How Aurora performs writes using asynchronous flows, establishes local consistency points, uses consistency points for commit processing, and re-establishes them upon crash recovery.
                    1. "In Aurora, the only writes that cross the network from the database instance to the storage node are redo log records"
                    2. "Once the database instance observes SCL advance at four of six members of the protection group, it is able to locally advance the Protection Group Complete LSN (PGCL)"
                2. How Aurora avoids quorum reads and how reads are scaled across replicas.
                    1. "Aurora uses read views to support snapshot isolation using MultiVersion Concurrency Control (MVCC)."
                    2. "Aurora MySQL does this by establishing the most recent SCN and a list of transactions active as of that LSN"
                3. How Aurora uses quorum sets and epochs to make non-blocking reversible membership changes to process failures, grow storage, and reduce costs.
                    1. See Figure 5 for quorum membership change steps
                    2. "We make at least two transitions per membership change, ensuring each transition is reversible"
                    3. Membership change or the quorum happen on "protection group", "protection group" is also the write/read quorum, it requires to write 4/6 and read 3/6
                        1. Interesting, So AWS Aurora is also using something similar to Raft to for data replication.
                           The difference is it's write/read to N. The quorum write techniques should originates from AWS Dynamo.
                    4. Section 4.2 Using Quorum Sets to Reduce Costs
                        1. "In Aurora, a protection group is composed of three full segments, which store both redo log records and materialized data blocks, and three tail segments, which contain redo log records alone."
                            1. Good design here. Raft data replication can also learn from here that to use log-only replicas to extend the quorum size but without adding storage cost.
                            2. And "Protection Group" is quite a common concept in many systems, like Ceph's "Placement Group / PG", Raft replication group, etc.
                                1. Section 2.1 Aurora System Architecture. 
                                    1. Protection Group is a quorum NOT on nodes, but on segments. This is also an important design. So that a node can host many quorums spanning to the entire cluster. If the node is down, it can involve the entire cluster for repairing.
                                    2. "Segments in Aurora are the minimum unit of failure"
                                       "currently representing no more than 10GB of addressable data blocks"
                                       "Segments are replicated into protection groups"
                                       "These six copies are spread across three AZs, with two copies in each of the three AZs"
                                       "Protection groups are concatenated together to form a storage volume, which has a one to one relationship with the database instance"
                                    3. How CockroachDB and TiDB make the Protection Group?
                                        1. CockroachDB: "Replicas of a Range form a Raft group"
                                        2. TiDB: "Data is stored in multiple Raft groups using row format ..."
                        2. "Our write quorum is 4/6 of any segment OR 3/3 of full segments. Our read quorum is therefore 3/6 of any segment AND 1/3 of full segments"

    m. Related materials
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
                        0. Citation: "PolarDB-MP forces that a node persists all logs related to a page before pushing the page to the DBP."
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
            1. Our earlier data analysis has shown that for primary datasets, whole file and subfile fixed-size chunk deduplication were significantly inferior to sub-file variable size chunk deduplication
        4. Dedup system design
            1. Chunk Indexing
                1. Log-structured organization
                2. Low RAM footprint index
                3. Prefetch cache
            2. Two-phase Deduplication
                1. Deduplication within a partition
                2. Reconciliation of partitions
                    1. deduplication across partitions

6. POLARIS: The Distributed SQL Engine in Azure Synapse    [2020, 38 refs, VLDB, Microsoft]
   https://15721.courses.cs.cmu.edu/spring2024/papers/23-synapse/p3204-saborit.pdf
    1. Good paper. Synapse is Azure OLAP engine (data warehouse) + data lake engine (semi-structured data). The architecture resembles Snowflake. DB is based on SQL Server. Features in 1) Cell data abstraction, 2) Distributed Query Optimizer, 3) Global resource-aware scheduling and DAG.

    n. Related materials
        1. Hyperspace: The Indexing Subsystem of Azure Synapse    [2021, 7 refs, VLDB, Microsoft]
           https://wentaowu.github.io/papers/vldb21-hyperspace.pdf
            1. Logged before

    m. Related materials
        1. POLARIS: The Distributed SQL Engine in Azure Synapse - 梁辰
           https://zhuanlan.zhihu.com/p/409131883
            1. Synapse的两个主要的设计目标：
                1. 融合结构化与非结构化数据，对海量异构数据实现统一且高效的处理
                2. 利用云上基础设施，实现计算与状态的分离，从而提供灵活的服务模式
            2. 技术特点
                1. Cell data abstraction
                    1. 为了能够对下层的异构数据直接在原地做统一的处理，Polaris对来自不同storage system的不同data format的数据，统一抽象为"data cell"这个逻辑上的数据块概念，有了这层抽象就可以屏蔽掉底层存储的异构特点，统一处理逻辑。
                2. Scale out + Scale up结合
                    1. Microsoft在数据库上算是出了名的不喜欢重复造轮子，他们尽可能会利用已有的技术来做适配改造，在Polaris的设计中也充分的体现了这一点，每个计算节点本质都是单机的SQL Server，内部会复用其改造后的优化器 + 执行器，同时也会复用PDW中的分布式优化器，这样可以充分利用SQL Server积累多年的技术优势。
                    2. 在单节点内尽可能获取最优的执行效率，而多节点间则由Polaris新的执行引擎负责管理调度，保证大数据量查询的扩展性、稳定性和高效性。
                3. 全局resource-aware的调度
                    1. 通过实现跨query的细粒度的、感知资源负载的调度框架，可以从全局角度实现对资源的高效利用，并控制多query的并发查询。
                4. 灵活的服务模型
                    1. 基于以上提到的多个能力，Polaris可以提供多种服务形态（类似于snowflake)，包括
                        1. server-less 节点数可以从 0 -> N动态调整，根据实际负载情况
                        2. reserved pool 节点数从 min -> max动态调整，但不会完全销毁，预留了固定资源
                        3. multiple reserved pools，允许多个pool同时允许，提供多租户 + 弹性的能力
                5. 多level的存储层级
                    1. 利用SQL Server在2012年就实现的Resilient bufferpool功能，可以将buffer pool扩展到本地的SSD中，从而形成了memory -> SSD -> Remote Storage的3层存储层级，尽量利用数据的本地化提升性能。
            3. 整体架构
                1. 计算/状态分离
                    1. Figure 1. Decoupling state from compute
                        1. 第3种，计算节点上只有cache，其他的状态都持久化在外部存储中（例如snowflake把事务状态和metadata保存在FoundationDB中），而cache本身是可以重建的，因此可以说计算节点实现了真正的无状态。好处是不言而喻的，如果一个node失效，从持久化状态中完全可以判断该node负责了哪些数据执行到了哪种状态，就可以有策略做partial retry，避免了大查询整体失败，提升了执行的容错能力。
                2. Figure 9. Polaris service architecture
                    1. 上图中展示了两个Polaris Pools共享同一个持久化元数据存储以及底层的海量数据存储。可以看到架构上和snowflake是基本一致的：
                        1. Polaris Pool <-> VirtualWareHouse
                        2. Centralized Service <-> Cloud Service
                        3. 底层异构数据存储 <-> AWS S3
                3. Data Abstraction
                    1. 引入了"data cell"这个干净的抽象
                    2. Polaris只需要关心data cells就可以了，屏蔽了下层众多的存储系统（事务型/分析型）
                4. 弹性的query processing
                    1. query的执行可能涉及大量节点，node fail的概率会显著升高，此外为了实现弹性，集群topo会随着workload的改变而调整也会是常态。因此要求Polaris能够根据集群topo的变化，动态的将data cell分配到node上(当然为了实现这一点，将所有state保存在外部是前提条件)，弹性一般会提现在如下几种场景
                    2. Skewed Computations
                        1. 在架构图中我们看到DQP和ES之间是有control channel的，基于这个channel实现了feedback loop机制，跟踪在node上执行task的状态，如果node负载过重可以做一些re-balance的操作，调度走一些task，如果这样也无法解决hot spot问题，就会触发auto-scale，加入更多节点实现负载均摊。
                    3. Affinitizing Tasks to Compute
                        1. 由于SQL Server的Resilient bufferpool能力，其上的local SSD也称为了cache的一部分，这部分cache会尽可能的被利用，来避免从remote storage上重新拉数据，DQP会根据cache中数据的分布情况，将task分发到要计算的data cache上去，但对cache的具体管理算法paper里没有提到。
                5. 查询优化
                    1. Polaris中的查询优化基于SQL Server PDW演进而来，整体的优化流程和计划形态基本保持一致，优化过程分为2个阶段
                        1. 单个SQL Server Frond End从metadata存储中获取cell相关信息，并利用单机SQL Server的Cascades QO生成单节点的search space(MEMO)
                        2. MEMO被发送到DQP组件，DQP基于MEMO做bottom-up enumeration，枚举每个算子可能的分布式执行方式，比基于输出的物理属性划分等价类，逐步向上传递局部最优解
                    2. Polaris的paper中主要讲解了第2阶段也就是分布式优化的一些内容
                    3. Task DAGs
            4. 总结 - 一些takeaway：
                1. 湖仓一体是大数据分析发展的新赛道，目前snowflake/databricks/各大云厂商已经挤了进去，大大小小做AP的厂商也在发力
                2. 随着AI/data science的发展，schema-less数据越来越重要
                3. 计算与状态分离 + 云基础设施，发挥成本+弹性的最大优势
                4. query-level的容错能力非常重要
                5. 为保证可预期的性能，workload-level的资源协调是难点
                6. 复用有优势的竞争力，避免不必要的新轮子

        2. [VLDB2020] POLARIS: The Distributed SQL Engine in Azure Synapse - 猫吃面
           https://zhuanlan.zhihu.com/p/388391672

7. Firestore: The NoSQL Serverless Database for the Application Developer    [2023, 18 refs, Google]
   https://research.google/pubs/firestore-the-nosql-serverless-database-for-the-application-developer/
    1. Document DB emphasizing ease-of-use built atop Google Spanner. Features in Real-time queries and Disconnected operations, and all fields are indexed on default.
       Lightweighted built atop Google Spanner. Also reused Google Autopilot for auto-scaling and Google Slicer for auto-sharding. 
       Good case as how to reuse Google infra to build new cloud services in Google.
    2. Highlights
        1. Backgrounds
            1. Firestore database features
                1. Schemaless data model, ACID transactions, strong consistency, and index-everything default
                2. Fully Serverless Operation and Rapid Scaling
                3. Disconnected operations from mobile devices
                    1. Interesting topic
        2. Key challenges & techniques
            1. Firestore data model and simple query language that are key to enabling rapid application development
                1. Documents, maps, arrays. Key-ed by directories paths
                2. "To scale with increase in database size, Firestore executes all queries using secondary indexes"
                    1. "To reduce the burden of index management, Firestore automatically defines an ascending and a descending index on each field across all documents on a per-collection basis"
                    2. This is an interesting idea.
                3. Real-time queries
                    1. From the client view, it's a constant on query. Any updates from the local user or other users will immediately get reflected in the query results display
                        1. Good usecase captured and incremental update technologies to support it.
                4. Disconnected operations
                    1. Blind writes when disconnected and revalidated once reconnected.
                5. Do NOT support lock-based pessimistic concurrency control
                    1. Because it would allow a third-party to easily conduct DoS attack.
                6. Write Triggers
                    1. Follow up calls Google Cloud Functions, with change delta available.
            
            2. an effective approach for building a multi-tenant database service over a single underlying (scalable) relational database (Spanner).
                1. Billing and Free Quota
                    1. The free quota is enforced by integration with Google's quota system, 
                    2. operation-based billing is done by logging the count of documents accessed by each RPC and integration with Google's billing system that reads the logs, 3. storage usage is measured and billed daily
                2. Multi-tenancy and Isolation
                    1. We use a fair-CPU-share [13] scheduler in our Backend tasks, keyed by database ID. 
                        1. We also pass the database ID as a key to Spanner's similar fair-CPU-share scheduler. 
                    2. Certain batch and internal workloads set custom tags on their RPCs, which allow schedulers to prioritize latency-sensitive workloads over such RPCs. 
                    3. We limit the result-set size and the amount of work done for a single RPC, which protects the system against problematic workloads. 
                    4. Firestore APIs support returning partial results for a query as well as resuming a partially-executed query. 
                    5. Most parts of Firestore can split out traffic even on a document granularity to redistribute load. 
                    6. Some components do targeted load-shedding to drop excess work before auto-scaling can take effect
                3. My questions
                    1. I didn't see any concept of "Resource Unit" being used here. Why?
            
            3. how the multi-tenant architecture supports rapid scaling, high availability, data integrity, and isolation
                1. As a foundation, all components build on Google's auto-scaling infrastructure [11]
                    1. Interesting, worth drilling down.

            4. Implementing data and queries on Spanner
                1. Firestore maps each database in a region to a specific Spanner directory
                2. Each Firestore document is stored as a single row in the (fixed-schema) Spanner Entities table
                    1. The key-value pairs that constitute a schemaless Firestore document contents are encoded in a protocol buffer [14] stored in a single column
                    2. My questions
                        1. Encoding the whole document into one single column, is it a final solution? Would it make the document unable to query?
                            1. So it explains why Firestore needs to build index on every field
                            2. A second problem, if the user wants to exclude a field from the indexing, then it would make the field unable to be queried
                                1. "Firestore allows the customer to specify fields to exclude from automatic indexing (queries that would need the excluded index then fail)"
                            3. MongoDB does NOT index all fields on default
                               https://stackoverflow.com/questions/27256173/index-every-field-in-mongodb-by-default-or-auto-without-having-me-to-check-or-se
                        2. But this is an interesting case that how to quickly build a new cloud service on a global scale database like Google Spanner.
                
                3. Each Firestore index entry is stored in an inverted index: a single row in the (fixed-schema) Spanner IndexEntries table. 
                    1. The key of this table is an (index-id, values, name)
                
                4. Firestore's transactions map directly to Spanner transactions
                    1. The lack of consistency in many queries was a drawback for Datastore’s Megastore-based implementation; an important customer mentioned consistency as a reason for migrating from Datastore to Spanner [15]
                        1. How Pokémon GO scales to millions of requests?
                           https://cloud.google.com/blog/topics/developers-practitioners/how-pok%C3%A9mon-go-scales-millions-requests
                        1. My questions
                            1. This explains why Google MegaStore seems disappeared and all later words are saying about Spanner.
            
            4. Disconnected operation: how client-side SDK libraries enable disconnected operation
                1. The Client (Mobile and Web) SDKs build a local cache of the documents accessed by the client together with the necessary local indexes.

            5. Real-time queries: how Firestore computes and fans out notification updates for real-time queries to clients, and how these updates get presented to the end-user in a consistent fashion.
                1. A client registers one or more realtime queries via a long-lived connection with a Frontend task.
                2. The updates are delivered to applications as incremental, timestamped snapshots, comprised of a delta of documents added, deleted, and modified from the prior snapshot.
                3. The key component - Real-time Cache
                    1. the In-memory Changelog and the Query Matcher
                    2. See detailed steps at Figure 5 and "The request/response flow for a real-time query"
                    3. Changelog and Query Matcher tasks by leveraging the Slicer [17] auto-sharding framework

    m. Related materials
        1. 从一到无穷大 #9 Firestore：开发者友好的Serverless NoSQL Database - 大家好大家吃了吗
           https://zhuanlan.zhihu.com/p/704953096
            1. "这篇文章显然是一篇摸鱼文章。写下这篇文章的本质原因是我在看到摘要和介绍的时候以为Google的工程师们解决了这个我们头疼不已的问题，但原来还是和我们一样都是蒙起自己和客户的眼睛。"

    n. Related materials
        1. [11] Autopilot: workload autoscaling at google    [2020, 303 refs, Google]
           https://research.google/pubs/autopilot-workload-autoscaling-at-google-scale/
            1. Gradually adjust the soft quota for jobs running on Borg. Use "moving window average" to review and adjust soft quota. Use reinforcement learning to select from a range of moving window models.
            2. Highlights
                1. Figure 1: Autopilot dataflow diagram
                    1. The system runs on Borg. Scaling Actuator is straightforward, just set Borg task counts/limits. Then what's still an open question is the decision making part.
                2. chooses the recommender(s) for a job according to
                    1. memory or CPU
                    2. how tolerant the job is to out-of-resource events
                    3. optional user inputs
                2. The reinforcement learning
                    1. Multi-armed bandit similar (not same)
                        1. use cost function to choose from a range of the moving window models. Each model varies at several parameters decay rate d_m and safety margin M_m.

            n. Related materials
                1. Autopilot: workload autoscaling at Google 随笔 - s09g
                   https://zhuanlan.zhihu.com/p/414562470
                    1. Key challenges
                        1. 是用户在部署任务的时候，出于谨慎考虑，肯定会多申请一些资源。比如vns在大多数zone上平均消耗0.3～0.6个GCU （Google Compute Unit），偶尔遇上峰值会消耗1-2个GCU，过去几年只有一次因为事故消耗了5个GCU。但是因为有这种顾虑，所以在申请资源的时候一律申请15个GCU。Google Cloud总共100多个staging zone，200多个prod zone。每个zone申请15 GCU，但是平均消耗0.3 GCU，资源浪费你算算…这其实已经算少的了，因为vns承载的流量不多，以前每个cell courier要申请50个GCU。

                           所以资源浪费很大。这又进一步导致负载不均衡，比如两台机器提供了相等的资源，但是因为大家申请资源的时候都在拔高预算。结果看起来两台机器可能拉满了，实际情况可能一个跑了60% CPU，另一个跑了20% CPU。

                        2. 另外从sre的角度来看，borg或者说kubernetes，虽然不是操作系统，但是复杂度已经不下于操作系统了，人工管理已经很难了。大部分公司应该不能像谷歌一样每个team都有SRE。中小公司连devops建设都勉强，上kubernetes完全是nightmare。所以容器编排的人工管理成本很高，从Google的角度我们就应该尽量让程序管理这种自动化的工作。
            
                    2. Key solutions
                        1. 一个基本思路是，用户启动了一个任务，这个任务获得了一些资源配额。但是在整个执行过程中肯定有一些unused resources。这里借用linux quota的概念，每个任务申请的是hard quota，autopilot会去动态地调整soft quota，尽可能回收没被使用的资源。

                        2. autopilot用了两种主要算法，一个是moving window recommender。实际上是在一段时间内，如果没有持续使用申请的资源，soft quota就会按照某个衰退率下降。
                        
                        3. 另一个算法就比较牛逼了，强化学习（搞笑）。论文称之为Recommenders based on machine learning。简单来说，这个算法是用来调整上一个算法的参数的。比如CPU的soft quota每12个小时降低一半，但是不可能一到12个小时瞬间砍一半，而是在过去的12个小时里，一点点平滑下降。那么问题来了，什么时候下降。

                           论文表示，对于信号s，在时间t，从一组模型中计算全部可能的极值L，然后根据历史数据，计算underrun cost和overrun cost，加权之后，判断是否分配资源。用人话说，比如autopilot想要判断一下能不能收回点CPU资源，它会每隔一段时间采样一次，拿这些数据交给一堆训练好的模型跑个二分类，然后算算看自己是underrun还是overrun了。这个模型倒是也好训练，毕竟负反馈机制比较明显，CPU/RAM资源一下子衰退过多，job当场就OOM（Out of memory）了。


        2. [17] Slicer: Auto-sharding for datacenter applications    [2016, 107 refs, OSDI16, Google]
           https://www.usenix.org/system/files/conference/osdi16/osdi16-adya.pdf
            1. Interesting topic as to use a common framework to help Apps to manage sharding, including split/merge, load balance, geo deployment, (and replication), which can be quite sellable on a public cloud.
               Slicer uses hash for key assignment, store assignment in the underlying storage, and use split/merge for hotspots. HA essentially benefit from a globally available infra in Google. Scalability is by a "two-tier distribution tree" like CDN.

            n. Related materials
                1. Shard Manager: A Generic Shard Management Framework for Geo-distributed Applications    [2021, 23 refs, SOSP21, Facebook]
                   https://research.facebook.com/publications/shard-manager-a-generic-shard-management-framework-for-geo-distributed-applications/

                2. Slicer: Auto-Sharding for Datacenter Applications - 丁凯
                   https://zhuanlan.zhihu.com/p/462856965
                    1. Key challenges
                        1. Slicer诞生之前，每个业务都需要自己搞定这些应用逻辑之外的事情，如多节点甚至跨AZ、Region部署，节点负载不均衡、难以弹性等问题，这些问题比应用本身复杂度更高，这显著提升了应用的开发和运维难度。
                        2. Slicer的典型应用
                            1. In-memory Cache Applications
                                1. The most common cases
                            
                            2. Flywheel
                                1. Google内部专为移动设备设计的http proxy service，主要用来优化传统网站对移动设备的数据量不够友好问题，通过压缩、格式转化（如原始网站图片PNG转WebP格式）等手段降低移动设备访问网站时的数据传输量，节约用户成本。

                                   作为Proxy，Flywheel内部有一些Task专门用来追踪那些最近不可访问的网站，这样客户端访问这些网站时就可以立即返回错误而无需再去原始网站访问直到超时，提升用户体验。

                                2. Flywheel为该功能专门创建了一些Task。没有Slicer时，请求（更新与查询）会被发往任意一个Task，虽然可以工作，但效率比较低（如对于某个网站的状态更新被发往Task-A，而查询网站状态请求发往Task-B，但B上并没有缓存状态，于是，上层认为该网站还是可服务的，但实际并不是，应用会直接访问原始网站，直到超时后应用将Task-B上状态也更新。相当于Task-A上的缓存并未生效）。

                                   采用Slicer后，Flywheel将website url定义为key，这样，相同key的请求会被发往同一个Task，解决了问题。
                            
                            3. In-memory Store Applications
                                1. 这类应用不同于In-memory cache application，一旦请求在Task上未获取到状态，会从底层store中加载状态（而cache则是无法处理）。

                            4. Aggregation Applications
                                1. 这类应用特点是会将特定key的写入请求聚合成batch写入底层存储以减轻下层压力。

                            5. Event analysis
                                1. 这类应用收集event，根据source id做聚合然后建模分析。
                                2. 使用Slicer之前，应用不得不对每个event做复杂处理（例如多个节点写入同样的source id的event时需要处理并发控制等），代价非常大。
                                3. 有了Slicer，应用将source id定义为key，拥有相同key的event会被发往同一个Task处理。从而避免了多Task同时处理相同source id的event带来的复杂逻辑（并发控制、event聚合等）。
                    
                    2. Key solutions
                        1. 应用对接Slicer 接口
                            1. Slicelet: Get key, listener
                            2. Clerk: Assign key to task
                        2. Slicer利用了Google的Stubby来实现流量的负载均衡。
                            1. Slicer扩展了Stubby，在每个请求中携带Slice key，Stubby首先选择与客户端最近的数据中心（应用可能在很多数据中心都部署了Task），然后Slicer从该数据中心根据key定位到所在的Task。
                            2. 在每个数据中心内部又使用了GFE（Google Front End），它是数据中心内的HTTP请求代理层
                        3. Slicer 实现
                            1. Assigner
                                1. Assigner是Slicer核心模块。主要工作是根据分片算法生成assignment（其实就是Slice到Task的映射）。
                                2. 为了提供高可用能力，Google在全球多个数据中心部署了Assigner服务，任意一个Assigner都可以为任意数据中心内的应用生成assignment。
                                3. Assigner从底层的一致性存储系统中读取状态（状态内容是什么？），生成新的assignment，并为该assignment分配一个新的全局递增的序列号（谁来分配？全局TSO？），然后将该assignment写回到底层storage（通过事务）并且携带了读取时的value（这个value是上次读取时最后一个assigment的generation number吗？）。如果有多个Assigner并发写，本次事务将放弃，重新走一遍上面的流程。
                                4. 对于某个Job，只让一个特定的Assigner为其服务，避免了竞争
                                    1. 具体来说，每个Assigner会poll Google的全局load balancer服务，检查一下它自己是否是当前所服务的Job里面最近的一个（可能有多个Assigner服务一个Job，每个Job都去检查一下它与Job所在的数据中心的网络距离）。如果是，它就作为Job的唯一服务方，如果不是，应该就会放弃服务权。
                                    2. 如果一个Job的Task部署在多个数据中心（这些Task的作用是服务的冗余吧？）。Slicer首先根据Google load balancer选择一个数据中心，然后在数据中心内部选择一个Task。
                            2. Scalable of assignment
                                1. Assigner的核心任务是将Slice key space 映射到应用Tasks上，每个映射就是一次assigment。某些大型Job可能会有成千上万 Task，产生大量assigment。这些assigment信息需要被传递至所有的Task以及client上去
                                    1. （统一称之为subscribers。有几个问题：1. 为什么需要被传递至Task上去？Task维护自身的不就可以吗？难道是Task收到了不是自己的请求后根据这个全局信息进行转发？2. Client直接同Slicer要不就可以吗，效率太低？）
                                    2. 尤其是assigment时刻在动态变化，如何将这些变化迅速反馈呢？
                                2. Slicer使用了两层distribution来解决该问题
                                    1. Assigner生成assignment，分发给Distributor，Distributor再分发给client。确切地说，是一种pull的模式：Client监听Distributor，而Distributor监听Assigner，一旦Assigner上的Assigment有变化，Distributor会感知到，进而Client也能感知。
                                    2. 上述Watch是一种异步更新机制，这可能会导致某些对一致性要求较高的Application出问题，这通过一种独立的控制通道来解决该问题（论文中好像没有提及，应该是一种事后反馈：Client拿着错误信息去访问了错误Task，Task发现任务并不属于自身，返回一个错误，Client进而去主动拉取一次）。
                            3. 容错
                                1. Backup Assignment Retrieval Path
                                    1. Slicer包含一个Backup Distributor，一旦正常的Distributor无法服务，Backup Distributor会从Store中直接读取assignment状态并提供服务。即使Assigner和Distributor都挂了，Backup Distributor还可以对外提供一种只读服务。
                                2. Geographic Diversity
                                    1. Assigner和Distributor可以全球部署，任何的client可以通过Google load balancer联系任意的Distributor，Distributor也可以联系任意的Assigner。
                                        1. "Any Assigner may generate an assignment for any job in any datacenter" .. Interesting. Though not the topic of this paper, this reflects a strong capability from Google datacenter - whole region even whole world is a single datacenter. It's a worthwhile direction to drill.
                                    2. 每个Job有prefered Assigner（网络距离最近的那个），一旦Job的prefered Assigner挂掉，其他任意Assigner可以接手。这种策略可以容忍机器、数据中心以及网络故障。
                                3. Geographic Proximity
                                    1. 每个Job的prefered Assigner是与Job网络距离最近的那一个，Distributor也会在Assigner所在数据中心部署，这些策略都减少了跨数据中心的网络传输，提升效率且减少网络故障带来的影响。
                                    2. 甚至，如果应用需要，整个Slicer service都可以与应用统一独立部署。
                                4. Fate-Shared Storage Placement
                                    1. 这也叫命运共同体式部署。将Assigner同应用部署在相同数据中心（存储同样在一起）。可以进一步减少数据中心之间的网络分区对服务造成的影响。
                                5. Service-Independent Mode
                                    1. 在Clerk中增加cache。这样，即使所有的service都不可用了，靠着cache还可以勉强支撑。
                            4. Load Balance
                                1. Slicer的映射模型是首先将Application自定义的key（如user id）通过hash计算映射到一个key space(2^63)，然后将这个key space划分为多个slice（key range），然后再将slice映射至Task。
                                    1. 一般来说，通过第一步的hash计算得到的key分布应该是均匀的，但某些热点key还是会造成某些Task的负载上升。
                                    2. 有两种方式可以缓解负载不均衡：为key增加额外Task、改变key的映射。
                                    3. 另外，Slicer还支持slice的split和merge。通过将热点Slice进行split，一个Slice可以变为两个，进而负载自然就会分解到多个Task。同时，Merge可以控制系统Slice数量。
                                2. Sharding Algorithm: Weighted-move
                                    1. 描述流程性的东西，核心思想就是基于负载的迁移，忽略。
                                3. Rebalancing suppression
                                    1. 一旦达到某些负载均衡指标，迁移就会被抑制，避免无意义工作。
                                4. Limitations
                                    1. 当前的balance算法没有考虑两个方面：1. Task的异构性（没有太理解）2. 内存使用（内存使用和CPU利用率不一定正向相关）
                                5. A rejected design alternative
                                    1. paper阐述了为什么没有采用一致性hash（load-aware consistent hashing），有以下几点：
                                        1. evolving clients is burdensome
                                            1. "Slicer instead distributes assignments in decoded form" ... This reveals how Slicer implements the assignment, probably by plain key ranges. And these ranges are stored in *probably* Google Spanner. If hash mapping is wanted rather than range, hash the key first.
                                        2. consistent hashing gives us less control over hot spots
                                    2. "Centrifuge [10] ... After 18 months in service, we replaced it with the weighted-move algorithm"

                3. 论文笔记：[OSDI'16] Slicer: Auto-Sharding for... - 张帅
                   https://zhuanlan.zhihu.com/p/86420697
                    1. 强一致性
                        1. Slicer 通过租约（Lease）机制实现强一致性
                        2. 但是 Slicer 更进一步的可以只使用至多 3 个 Chubby locks 完成租约管理，并且由于租约管理是由 Chubby 进行的，所以即使 Slicer 挂掉也不会影响用户服务。
                            1. job lease: 首先需要一个锁来保证同一时刻内只有一个 Assigner 负责整个分配
                            2. guard lease: Assigner 会为每一轮分配生成一个租约，只有得到租约许可的 slicelet 才可以提供服务，这样当分配更新时，持有过期信息的 slicelet 就会停止提供服务，避免因信息不同步导致的多个 slicelet 对同一个 key 提供服务的情况
                            3. bridge lease: 如果只使用 guard lease，则在每一轮分配期间，都会导致全服务的 guard lease 整体失效。但是显然每一轮分配只改变了一小部分 key range 的分布，其他没有发生变化的部分不应该受影响。因此对这部分没有变化的分配，引入一个 bridge lease，使其不受 guard lease 失效的影响。
                        3. 个人觉得这个想法还是比较有意思的，相当于 Slicer 既可以控制分配，也可以控制选主，这样只要用户自己实现 replication 机制，就可以很容易的做一个有状态服务了。


        3. [10] Borg, omega, and kubernetes - Lessons learned from three container-management systems over a decade    [803 refs, 2016, Google]
           https://research.google/pubs/borg-omega-and-kubernetes/
            1. Good article. It tells the history of Google cluster management systems and their many insights and experiences. Major emphasis fall into Kubernetes.
            2. Highlights
                1. History: Borg -> Omega -> Kubernetes
                    1. Borg remains the primary container-management system within Google because of its scale, breadth of features, and extreme robustness
                    
                    2. Omega stored the state of the cluster in a centralized Paxos-based transaction-oriented store that was accessed by the different parts of the cluster control plane (such as schedulers), using optimistic concurrency control to handle the occasional conflicts. This decoupling allowed the Borgmaster's functionality to be broken into separate components that acted as peers, rather than funneling every change through a monolithic, centralized master.
                    
                    3. Like Omega, Kubernetes has at its core a shared persistent store, with components watching for changes to relevant objects. In contrast to Omega, which exposes the store directly to trusted control-plane components, state in Kubernetes is accessed exclusively through a domain-specific REST API that applies higher-level versioning, validation, semantics, and policy, in support of a more diverse array of clients. 

                       More importantly, Kubernetes was developed with a stronger focus on the experience of developers writing applications that run in a cluster: its main design goal is to make it easy to deploy and manage complex distributed systems, while still benefiting from the improved utilization that containers enable.
                
                2. Containers 
                    1. The resource isolation provided by containers has enabled Google to drive utilization significantly higher than industry norms. For example, Borg uses containers to co-locate batch jobs with latency-sensitive, user-facing jobs on the same physical machines. The user-facing jobs reserve more resources than they usually need—allowing them to handle load spikes and fail-over—and these mostly unused resources can be reclaimed to run batch jobs.

                3. Orchestration is the Beginning, Not the End
                    1. The idea of a reconciliation controller loop is shared throughout Borg, Omega, and Kubernetes to improve the resiliency of a system: it compares a desired state (e.g., how many pods should match a label-selector query) against the observed state (the number of such pods that it can find), and takes actions to converge the observed and desired states. Because all action is based on observation rather than a state diagram, reconciliation loops are robust to failures and perturbations: when a controller fails or restarts it simply picks up where it left off.

                       The design of Kubernetes as a combination of microservices and small control loops is an example of control through choreography—achieving a desired emergent behavior by combining the effects of separate, autonomous entities that collaborate. This is a conscious design choice in contrast to a centralized orchestration system, which may be easier to construct at first but tends to become brittle and rigid over time, especially in the presence of unanticipated errors or state changes.

                4. Things to Avoid
                    1. Don't Make the Container System Manage Port Numbers
                        1. Learning from our experiences with Borg, we decided that Kubernetes would allocate an IP address per pod, thus aligning network identity (IP address) with application identity. 
                    2. Don't Just Number Containers: Give Them Labels
                    3. Be Careful with Ownership
                        1. If one of these pods starts misbehaving, that pod can be quarantined from serving requests by removing one or more of the labels that cause it to be targeted by the Kubernetes service load balancer. The pod is no longer serving traffic, but it will remain up and can be debugged in situ.
                    4. Don't Expose Raw State

                5. Some Open, Hard Problems
                    1. Configuration
                    2. Dependency Management


8. FairyWren: A Sustainable Cache for Emerging Write-Read-Erase Flash Interfaces    [2024, 1 refs, OSDI24, Microsoft]
   https://www.usenix.org/conference/osdi24/presentation/mcallister
   https://www.microsoft.com/en-us/research/publication/fairyw-ren-a-sustainable-cache-for-emerging-write-read-erase-flash-interfaces/
    1. Major improvement from Kangaroo cache. Leveraging 1) ZNS/FDP SSD 2) Net packing 3) Separating data by lifetime. The WA reduction results (Figure 12) is ridiculously very good.
    2. Highlights
        1. Background
            1. WREN devices must let applications control which EU their data is placed in and when that EU is erased
            2. FDP: https://youtu.be/BENgm5a17ws?si=F6tCE7ue-1XRuTz7
        2. Key solutions
            1. nest packing
                1. When live data is rewritten during GC, FairyWREN has an opportunity to evict unpopular objects and admit new objects in their place
            2. FairyWREN groups data with similar lifetimes into the same EU
        3. Evaluation
            1. Section 6.5, Figure 16, Where are benefits coming from? Each below contributed ~1/3 saving
                1. physically separate the large and small objects into different erase units
                2. nest packing
                3. hot-cold object separation

    n. Related materials
        1. 2024年操作系统设计与实现研讨会（OSDI）有哪些值得关注的文章？ - SuSun
           https://www.zhihu.com/question/649626302/answer/3596509565
            1. FairyWREN 的创新设计：文章介绍了 FairyWREN，这是一种专为 WREN 接口设计的闪存缓存。FairyWREN 的独特之处在于它将缓存准入与垃圾回收相结合，通过 "嵌套打包" 算法在每次写入时实现这一点。这种方法显著减少了写入放大，从而延长了闪存寿命并降低了碳排放。
            2. 显著降低闪存写入： 相比于当前最先进的 Kangaroo，FairyWREN 将闪存写入减少了 92%，从 97 MB/s 降至 7.8 MB/s。这主要归功于 FairyWREN 巧妙地结合了缓存逻辑和垃圾回收，并根据预期寿命分离了不同类型的写入。

        2. OSDI 2024 论文评述 Day 3 Session 9: Data Management - IPADS-SYS
           https://zhuanlan.zhihu.com/p/708037149
            1. FairyWREN: A Sustainable Cache for Emerging Write-Read-Erase Flash Interfaces
                1. 在 ZNS, FDP 等 WREN SSD 上，FairyWREN 设计了一个基于 Flash 的 Cache ，通过 co-design 垃圾回收与 cache 放置策略，减少了12.5x 的写入量，降低了35%的 flash cost 和33%的碳排放。
                2. Highlights
                    1. Key challenges
                        1. 降低 Flash Cache 中小对象的写放大. Working on ZNS, FDP flashes
                        2. 直接把 WREN 用在 Set-associated 的 cache 上，用 log 的方式写，可以发现随着 Erase Unit 的增大，WA 会增大到最多8x
                    2. Key solutions
                        1. Key Insight: 每一次 flash write 都是 admit object 的机会，不管是来自应用写入还是 GC 写入
                        2. FairyWREN 的整体架构与 Kangaroo 类似，由以下部分组成
                            1. Large-Object Cache (LOC): 用于缓存大对象的 Cache，设计与前序工作类似，即以 Log-structured 的方式组织 SSD，在内存中维护 buffer 来缓存写入和 indexing 来索引 SSD 中的对象
                            2. Small-Object Cache (SOC): 用于缓存小对象的 Cache (10s Byte)，大致结构与 Kangaroo 相似
                                1. FwLog (5% of SOC's capacity)：一个 log-structured 的 Flash Cache，同样有内存来 buffer 和 indexing
                                2. FwSets (95% of SOC's capacity): 一个 set-associative 的 cache，把每个小对象 key 的 hash 值映射到 set，在内存中维护每个 set 在 SSD 中的位置（不索引每个 object，因为索引小对象开销过大）；同时，一个 set 对应一个 Erase Unit，在一个 set 里也是 log-structured 写入的
                            3. SOC Operation：
                                1. Insertion：所有小对象的写入都会先写入到 FwLog 中，当 FwLog 快满的时候，会进行 GC 把 FWLog 中的对象 admit 到 FwSets 中，当对应的 Set 也满了的时候，就需要进行 Evict
                                Eviction (nest packing， 主要设计):
                                2. 如果 FwLog 满了，就选中 FwLog 中的一个 Erase Unit，读取里面所有的对象，然后把它写到 FwSet 里面去
                                如果 FwSets 满了，选中一个 Victim Set（对应一个 Erase Unit），先读取 Log 里会写到这个这个 Set 里的对象，然后合并 FwSets 里的对象，如果需要 evict 的话就 evict，最后写回这个新的 set，擦除这个 Set
                        3. SOC 设计直觉
                            1. The key difference of FairyWREN from prior flash caches is its coordination of cache insertion and eviction with flash GC.
                            2. In the worst case, a set is copied by garbage collection and then is immediately rewritten to admit objects from FWLog
                        4. 一些优化
                            1. 把一个 Set 里进一步分成了 Hot Set 和 Cold Set 来进一步减小 GC 开销
                                1. By a modified RRIP algorithm [45, 67]
                            2. 把 FwLog 切分成多个 Slice 来减少键的空间，进而减少索引大小
                    3. 测试评估
                        1. Figure 12: FairyWREN 大大减小了写入带宽，同时 Miss Ratio 甚至比 Kangaroo 略好
                        2. 在 peak load 下，FairyWREN 在 thpt 和 read latency 表现都比 Kangaroo 好

        3. I/O Passthru: Upstreaming a flexible and efficient I/O Path in Linux    [2024, 1 refs, FAST24, Samsung, Facebook]
           https://www.youtube.com/watch?v=cJ6J2z46FTA
           https://www.usenix.org/conference/fast24/presentation/joshi
            1. Logged before. Also to optimizing for ZNS/FDP on Kangaroo cache.
            2. Figure 11, CacheLib WAF reduced from 2.4x to 1.0x with FDP.
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

Taxonomy of shared-nothing vs shared-storage architectures.

```
1. Shared-nothing architecture
    1. Built atop local KV Store
        1. AWS S3 [1]: https://assets.amazon.science/77/5e/4a7c238f4ce890efdc325df83263/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3-2.pdf
        2. CockroachDB: https://www.cockroachlabs.com/blog/cockroachdb-on-rocksd/
        3. TiDB: https://docs.pingcap.com/tidb/stable/rocksdb-overview
        4. YugabyteDB: https://docs.yugabyte.com/preview/architecture/docdb/performance/
    2. Built atop local filesystem
        1. AWS EBS [2][7]: https://d1.awsstatic.com/events/reinvent/2021/Amazon_EBS_A_tech_deep_dive_STG201.pdf
        2. Alibaba OceanBase: https://en.oceanbase.com/docs/common-oceanbase-database-10000000000829780
        3. Alibaba Pangu [7]: https://www.usenix.org/system/files/fast23-li-qiang_more.pdf
        4. Azure Storage Stream Layer: https://azure.microsoft.com/en-us/blog/sosp-paper-windows-azure-storage-a-highly-available-cloud-storage-service-with-strong-consistency/
        5. Azure DirectDrive [2]: https://www.sniadeveloper.org/events/agenda/session/347
        6. Azure CosmosDB [2]: https://azure.microsoft.com/en-us/blog/a-technical-overview-of-azure-cosmos-db/
        7. Google BigQuery [2]: https://cloud.google.com/bigquery/docs/storage_overview
        8. Ceph: https://docs.ceph.com/en/latest/rados/configuration/storage-devices/
        9. Facebook Tectonic: https://www.usenix.org/system/files/fast21-pan.pdf
    3. Built atop local object store
        1. I didn't find one. (Probably "files" are more preferred and functional to build atop than "objects".)
    4. Built atop local block store
        1. I didn't find one. (Probably "files" are more preferred than a binary block.)
    5. Built atop local disk
        1. I didn't find one (except local filesystems). (Probably "files" are more preferred than a raw disk.)

2. Shared-storage architecture
    1. Built atop shared logging
        1. AWS Aurora [7]: https://d1.awsstatic.com/events/reinvent/2019/REPEAT_1_Amazon_Aurora_Multi-Master_Scaling_out_database_write_performance_DAT404-R1.pdf
        2. AWS MemoryDB: https://www.amazon.science/publications/amazon-memorydb-a-fast-and-durable-memory-first-cloud-database
        3. Alibaba PolarDB: https://dl.acm.org/doi/10.1145/3626246.3653377
        4. Azure Storage: https://azure.microsoft.com/en-us/blog/sosp-paper-windows-azure-storage-a-highly-available-cloud-storage-service-with-strong-consistency/
        5. Apple FoundationDB: https://www.foundationdb.org/files/fdb-paper.pdf
        6. ByteDance BG3 [7]: https://dl.acm.org/doi/10.1145/3626246.3653373
    2. Built atop distributed KV Store
        1. I didn't find one. (Probably distribute KV Store is an end-product, i.e., NoSQL DB.)
    3. Built atop distributed filesystem
        1. Alibaba EBS [3]: https://www.usenix.org/conference/fast24/presentation/zhang-weidong
        2. Alibaba OSS [3]: https://www.usenix.org/conference/fast23/presentation/zhou
        3. Alibaba AnalyticsDB [3]: https://www.vldb.org/pvldb/vol13/p3152-wei.pdf
        4. Azure Synapse Analytics [3]: https://15721.courses.cs.cmu.edu/spring2024/papers/23-synapse/p3204-saborit.pdf
        5. Google Spanner [3]: https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf
        6. Google BigTable [3]: https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf
        7. Google Cloud Storage [3]: https://cloud.google.com/docs/storage
        8. Google Persistent Disk [3]: https://cloud.google.com/compute/docs/disks/persistent-disks
        9. Google Firestore [3]: https://research.google/pubs/firestore-the-nosql-serverless-database-for-the-application-developer/
    4. Built atop shared object storage
        1. AWS Redshift [4]: https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf
        2. Snowflake [4]: https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf
    5. Built atop shared block storage
        1. Azure SQL Database [5]: https://www.microsoft.com/en-us/research/uploads/prod/2019/05/socrates.pdf
    6. Built atop shared disk
        1. VAST DATA [6]: https://www.vastdata.com/whitepaper/#Introduction
        2. XSKY [6]: https://www.xsky.com/products/xsea#xsea-structure

3. Comments
    0. Covered systems: Object/block storage and OLTP/OLAP databases in major cloud vendors, plus a few notable opensource/commercial players.
    
    1. In AWS S3, a node stores data in ShardStore. ShardStore is a KV store backed by LSM-tree and GC internally. An S3 object is sharded then stored in ShardStore. ShardStore internally cuts a shard into several consecutive chunks. Chunks are organized into extents. Extent is the on-disk file format which is append-only. ShardStore implemented key-value separation like WiscKey.
        1. WiscKey: https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf

    2. The categorizations are guessed. There are not enough public details. DirectDrive stores data on a node called BSS.  AWS EBS never mentioned a Stream layer like Azure Storage nor sharing storage with AWS S3.  Google BigQuery stores data in columnar format in BigQuery Table. It's calling Google Cloud Storage as "external".  Azure CosmosDB should be managing its own storage rather than storing in Azure Storage.

    3. They can be thought as shared logging too. Google Spanner, BigTable, Cloud Storage, Persistent Disk, Firestore run on Colossus, formerly Google Filesystem (GFS). GFS "relying on appends rather than overwrites". The opensource counterpart HDFS is also append-only.  Alibaba EBS, OSS, AnalyticsDB run on Pangu Filesystem. Pangu is append-only.  Azure Synapse Analytics store analytical data at HDFS (Azure Data Lake Storage Gen2). HDFS is append-only.
        1. Cloud Storage: https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system
        2. Persistent Disk: https://cloud.google.com/blog/products/storage-data-transfer/learn-about-google-clouds-latest-storage-product-innovations
        3. Firestore: https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system
        4. Google Filesystem: https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf
        5. HDFS: https://www.quora.com/Is-HDFS-an-append-only-file-system-Then-how-do-people-modify-the-files-stored-on-HDFS
        6. Pangu Filesystem: https://www.usenix.org/system/files/fast23-li-qiang_more.pdf
        7. Azure Data Lake Storage Gen2: https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction

    4. Why categorized as shared object storage: In Snowflake, data is backed by AWS S3, and cached in compute nodes. In AWS Redshift, data is stored in Redshift Managed Storage (RMS), backed by AWS S3, and cached in compute nodes. RMS is a customized storage, but likely accessed as an object storage as described in paper. AWS S3 is a typical object storage.

    5. Why categorized as shared block storage: Azure SQL Database is the managed Microsoft SQL Server. Data is organized as pages and stored in Azure Storage. XLog service (backed by Azure Storage Premium) is the channel from primary DB to secondaries and Azure Storage pages.

    6. Why categorized as shared disk: In VAST DATA, any compute node can access SSDs on any data node via NVMe-oF. This effectively increases disk availability and enables high density erasure coding. XSKY uses similar technologies.

    7. A few systems even converted from other architectures to shared logging. Alibaba EBS shifted from V1's in-place updates to V2's append-only writes.  Alibaba Pangu supported random access files in V1.0 but replaced it with append-only in V2.0.  AWS Aurora is based on MySQL. MySQL needs to write both pages and logs to disk. But Aurora shifted to log-only – "log is database".  ByteDance BG was built atop RocksDB, but later in BG3 shifted to run on append-only cloud storage.

4. Additionally
    1. Stonebraker also mentioned the dominance of shared-storage architecture in his SIGMOD24 DB trends paper in the Cloud Database section.
        1. https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf
        2. "We expect this shared-disk to dominate DBMS architectures. Hence, we do not foresee shared-nothing architectures resurfacing in the future"
```
