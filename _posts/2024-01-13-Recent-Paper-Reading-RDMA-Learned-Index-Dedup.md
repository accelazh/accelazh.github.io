---
layout: post
title: "Recent Paper Reading RDMA, Learned Index, Dedup"
tagline : "Recent Paper Reading RDMA, Learned Index, Dedup"
description: "Recent Paper Reading RDMA, Learned Index, Dedup"
category: "storage"
tags: [storage, paper, cloud]
---
{% include JB/setup %}


```
1. QuePaxa: Escaping the Tyranny of Timeouts in Consensus    [2023, SOSP23, 1 refs]
   https://expolab.org/ecs265-fall-2023/slices/QuePaxa-DDS.pdf
   https://bford.info/pub/os/quepaxa/quepaxa.pdf
    1. Very good, paradigm shift work from the Paxos algorithm. First invention.
        1. Paxos can be thought as each proposer is broadcasting itself to all replicas. In Paxos, each leader tries to shoot the others (destructive view change). In tcast (QuePaxa), each leader cooperate. The leaders have already determined who should win by random priority attached with proposals. In tcast, they just help broadcast the winner.
        2. QuePaxa can do as good as Multi-Paxos (Leader Paxos) with little more overhead (correctly tune hedge delay). Yet it's more robust to unstable networking delays and timeout configurations. The key is each proposal is attached with a random priority (i.e., ordered), and it changes proposers from shooting each other (destructive view change) to helping winner propagate (cooperative). The protocol is tcast.
    2. Highlights
        1. Concepts
            1. randomized asynchronous consensus core
                1. it's the tcast algorithm
            2. hedging delays
                1. MAB converges to the best leader after a short period of time, who has lower latency
                2. Usecase: a leader is slow, we want to switch to a new faster leader.
                3. difference between hedging and timeout. See paper section 5.1.
            3. multiple proposers to operate simultaneously without destructive interference
                1. tcast tries to broadcast the winner, unlike Paxos each leader broadcasts to shoot the other one.
            4. Adaptively choosing leaders
                1. Simply, just try every leader once. Why saying such a fancy word MAB?
            5. multi-armed bandit theory
                1. It's in the "Adaptively choosing leaders"
            6. tcast - threshold synchronous broadcast
                1. This is the core. QuePaxa is an implementation of tcast.
            7. FLP [27] - asynchronous consensus is deterministically unsolvable
                1. QuePaxa in each round has 1/2 chance to reach consensus. High probability, not saying a must.
                2. Broadcast has an end, that means it needs sync wait barrier here, e.g. in Algorithm 4 "Await R".
            8. fast path under partial synchrony
                1. corresponding to Multi-Paxos by a already-prepared leader
            9. Existence set, common set, universal set
                1. Existent set: Replica i knows Proposal p
                2. Common set: Replica i knows Proposal p is Existent to all replicas
                3. Universal set: Replica i knows Proposal p is Common to all replicas
                4. Proving Theorem (Safety)
                    1. Forget the paper, let's think by ourselves
                        1. From the view of a Replica
                            1. If my best is known by at least N/2+1 other replicas, and my best is the true best, I'm safe to deliver my best
                                1. Is it possible that the true best isn't delivered by the quorum, which incorrect?
                                    1. It implies, the true best is known by at least N/2+1 replicas.
                                       The false best is known by at least N/2+1 replicas.
                                    2. It then implies, the intersection Replica knows the true best, but delivered the false best.
                                       This is impossible.
                            2. So the condition of I can deliver my best is, at least N/2+1 other replicas also knows my chosen best.
                               I.e., I can deliver my best <= my best is in the Common set
                            3. Which can my best be accepted by the quorum, it's at least N/2+1 replicas choose my best.
                               Then, it means at least N/2+1 replicas think my best is in the common set
                               I.e., my best is in the Universal set
                                1. So, a proposal being in the Universal set, implies it will be accepted by the quorum.
                                   Then, this is how comes "if best(𝐸) = best(𝑈 ) then deliver(𝑣)" in tcast Algorithm 1
                        2. The true question underlying is, we know a Replica should propagate its knowledge, but to what extent the propagation is enough?
                            1. The paper choose to describe in some Common Knowledge theory math.
                5. Proving Theorem (Liveness)
                    1. Since the propagation requires at least N/2+1 Replicas to know something.
                       Then, a replica has >= 1/2 chance to know the true best proposal.
                       After several Rounds, the algorithm is guaranteed to converge, and quite fast
                        1. Even a Round can terminate too early before a Replica finished broadcasting its knowledge
        2. More detailed concepts
            1. When can current round fail to reach consensus
                1. See "Theorem (Liveness)". When the best proposal didn't appear in Replica i's Universal set. Chance is 1/2. Then it has to go to the next round.
            2. What determines the end of each phase (Figure 2)
                1. Each phase maps to one propagate step n Algorithm 1. The end is not associated to timeout, it's logical, i.e. the broadcast done.
                2. Per relaxed, a propagation needs to reach at least N/2+1 Replicas. This is why "Theorem (Liveness)" requires several Rounds to converge to the best answer, and each Round a Replica has 1/2 probability to discover the best proposal.
            3. Leader tuning in QuePaxa
                1. interesting
                2. switch the leader after each epoch, switch to the faster one
                3. monitor leader performance. recompute hedging delay.
        3. How QuePaxa works
            1. 1 Slot = N rounds = N * 4 phases
                1. The first 3 phases, each phase runs an instance of tcast
                2. Algorithm 1
                    1. In phase 1, propagate proposal.
                       In phase 2, propagate existent set.
                       In phase 3, propagate common set.
                       In phase 4, detect consensus by comparing with universal set
                3. 1 Slot maps to a consensus.
                   1 round maps to running full Algorithm 1, may or may not reach consensus.
                   1 phase is a tcast run.
            2. Hedging schedule
                1. Each proposal becomes active after an increasing delay 𝛿
            3. Auto-tuning automatically converge to the lowest latency leader. Interesting 
                1. MAB, multi-armed bandit.
                2. Try each replica as being leader for 2 epochs. After 2n+1 epochs, it knows the best leader.
                3. Converge to a hedging schedule with replicas sorted in descending order of their observed average epoch completion time.
                4. See Figure 9 leader timeout vs hedging delay. Interesting
                    1. QuePaxa allows setting a low hedging delay between 1/2 to 1x of network roundtrip latency, but Paxos leader timeout cannot do the similar.
            4. Recorder, Interval summary register (ISR)
                1. It's just the logging persistence, and also need to track the max value in each phase with in the active window.
                2. Logical clock = Slot + Round + Phase. it's a measure of the current step.
            5. Fast path: leader-based rounds
                1. like Leader Paxos
        4. Evaluation
            1. Adversarial network
                1. increase egress packet latency of a minority of replicas 
        5. My questions
            1. Geo regional Paxos replication is a right fit. It needs to handle unstable timeouts
                1. metadata plane synchronously replicated across region
            2. How many networking requests are necessary compared to Paxos?
                1. See "How is the overhead of QuePaxa vs Paxos"
            3. Can it still simplify process with a single leader like Leader Paxos?
                1. Yes. Fast Path with leader
            4. Protocol for membership change?
                1. Not mentioned in the paper, worth exploring
            5. Isn't the hedging delay a timeout? Though QuePaxa says not depending on timeout.
                1. Hedging delay needs tuning. But QuePaxa is more robust to a bad Hedge delay configured. See Figure 9.
            6. What if there are >=3 proposers? How can they reach consensus by majority
                1. See protocol details. Paxos has the similar issue, and that's why it may stall liveness.
            7. How is the random priority persistently memorize by the proposer
                1. Not mentioned in the paper. It should be fine for each proposer to persist locally.
            8. How is the overhead of QuePaxa vs Paxos?
                1. If hedge delay is tuned correctly, communication cost is O(n). this is the same with Leader Paxos.
                2. If the leader hits timeout, QuePaxa needs at least 4 phases to reach consensus. Paxos can reach consensus in 2 phases. Each phase is a N to N broadcast.
                3. If networking is unreliable that leader frequently hit timeout, Paxos can stall with liveness issue, because leaders try to shoot each other. But QuePaxa can guarantee to reach consensus in a few slots.
                4. QuePaxa allows switching a slow leader to a faster leader. This is what Leader Paxos can hardly do
            9. What happens if two proposals happen to have chosen the same random priority?
                1. not mentioned in paper
            10. How is fencing done after leader switched?
                1. Not mentioned in paper. Though QuePaxa makes leader switching cheaper, but the fencing does have a cost
            11. Many places in the protocol requiring every replica something. Unlike Paxos which only requires more than half. What will be the implication?
    n. related materials
        1. A game changer for building robust distributed systems - QuePaxa
           https://actu.epfl.ch/news/a-game-changer-for-building-robust-distributed-sys/

2. Farron: Understanding Silent Data Corruptions in a Large Production CPU Population    [2023, 0 refs, SOSP23, Alibaba]
   https://dl.acm.org/doi/pdf/10.1145/3600006.3613149
    1. Good paper. Silent data corruptions from CPU are generally less studied but can easily break common data protection techniques such as replication and EC. Temperature is the key trigger to less reproducible SDCs. Farron invented interesting techniques.
    2. highlights
        1. See Table 1: Most failures were detected in Re-install, i.e. prod running, after preprod testing
            1. Observation 1. In overall, 3.61‱ of the CPUs are identified to cause SDCs in our study
        2. See Table 2: Certain CPU micro-architecture can be ~10x higher failure rate
        3. See Figure 7: Single bit flip is more than ~10x to 2 or more bit flips
        4. Observation 9: Some SDCs are highly reproducible, resulting in large impact on applications.
            1. In 51.2% of the settings, the occurrence frequency is higher than once per minute.
            2. Observation 10: Among those less reproducible SDCs, temperature serves as an important SDC triggering condition
                1. Exponential growth in response to increasing temperature
                2. Minimum triggering temperature exists
                    1. Figure 9, but the occurrence frequency is exponential decreasing whit triggering temperature
                3. Other reasons besides temperature
                    1. instruction usage stress. several orders of magnitude more frequent usage
        5. SDC Mitigation using multiple strategies
            1. include high temperature in SDC testing. But be careful it can affect CPU health
            2. control the CPU temperature at run time, by cooling device, and workload util
        6. Farron: An Efficient SDC Mitigation Tool
            1. temperature controls as a complement to SDC testing
            2. the fine-grained processor decommission (Observation 4)
                1. If more than two cores within a processor are found defective, Farron deprecates the entire processor in line with the pattern presented in Observation 4. Conversely, Farron masks that particular defective core and continues utilizing the other cores as normal.
            3. maintains a reliable resource pool to manage unaffected cores
        7. concrete cases
            1. incorrect checksum calculation
            2. defective hashing calculation in hashmap

3. Perseus: A Fail-Slow Detection Framework for Cloud Storage Systems    [2023, 6 refs, FAST23, Alibaba, Best Paper Award]
   https://www.usenix.org/conference/fast23/presentation/lu
    1. Good. Using latency-vs-throughput (LvT) to detect fail-slow instances, outperformed peer evaluation and all previous attempts. Evaluation on SSDs and HDDs from different clusters.
    2. Highlights
        1. Failure types in datacenter
            1. Fail-slow
                1. Good category. When we evaluate availability, we need to include both Fail-stop and Fail-slow.
                2. Annual fail-slow failure rate is 1-2%
                    1. Contributing most tail latencies
            2. Fail-stop
            3. Byzantine
        2. Fail-Slow Detection (FSD) - Perseus
            1. Challenges
                1. Latency variation may be caused by temporary workload burst, rather than fail-slow issue
                2. Peer evaluation is time-consuming to fine-tune, e.g. the window
            2. Guidelines
                1. Model the latency-vs-throughput (LvT) distribution
                    1. Figure 6, SRCC scores show latency-vs-IOPS is not strongly correlated
                    1. Fit a polynomial regression model
                2. Non-binary output, model likelihood of fail-slow
            3. Designs
                1. Prediction upper bonds as adaptive latency thresholds without fine-tuning
                    1. Interesting. Using outlier detection, and prediction upper bonding.
                2. PCA, DBSCAN, polynomial regression
            4. Findings
                1. In RCA of fail-slow, ill-implemented scheduling (e.g., unnecessary resource contention), occupies 80% root causes.
                    1. Interesting
        3. Evaluation: (Table 5) Threshold vs Peer eval vs IASO vs Perseus 
            1. PERSEUS outperforms all previous attempts
            2. My questions
                1. How exactly does PERSEUS outperforms peer evaluation in details?
                    1. Didn't see paper explaining it
                2. "PERSEUS currently uses traces from 9PM to 12AM each day to reduce interference"
                    1. OK .. this is problematic. The trace can be biased.
                3. "Each node in these two clusters is equipped with 12 open-channel SSDs (OC SSDs), whose Flash Translation Layer (FTL) is managed by the host. For each node, the host allocates 12 CPU cores to manage 12 OC SSDs, respectively (e.g., core0-core11 for SSD0-SSD11)."
                    1. Sounds like Open-channel SSDs are already widely used in Alibaba clusters?
        4. Case study
            1. Ill-Implemented Scheduler
                1. Interesting.
            2. Hardware Defects
                1. Interesting.
    n. related materials
        1. Perseus: A Fail-Slow Detection Framework for Cloud Storage Systems
           https://www.micahlerner.com/2023/04/16/perseus-a-fail-slow-detection-framework-for-cloud-storage-systems.html
        2. Perseus test data released
           https://tianchi.aliyun.com/dataset/144479
            1. good.

4. InftyDedup: Scalable and Cost-Effective Cloud Tiering with Deduplication    [2023, 1 refs, FAST23, 9livesdata]
   https://www.usenix.org/conference/fast23/presentation/kotlarska
    1. First local tier + cloud-based dedup solution for backup system. 
       Commercial product. http://9livesdata.com/publications/ .
       Use cloud to store unique chunks and to carry out batch computation with VM spot instances.
    2. highlights
        1. Scenarios
            1. PBs of backup
            2. public cloud vendors doesn't support dedup
            3. high scalability
            4. dedup is offline.
                1. read from disk then write to disk again
            5. cost of traffic and cost of capacity are unified
                1. cloud selling unifies the prices
                2. so they can compare in GC-Strategy #2.
            6. improve GC by file expiration date
                1. unique user pattern for backup, backup expiration date is known
        2. Cost & Evaluation
            1. Data sets
                1. synthetic workloads in which a given fraction of data was modified and deleted each day
                    1. daily backups are kept for one week, weekly backups are kept for a month, monthly backups are kept for a year, and yearly backups are kept for five years
                    2.  each file is read with a given probability
                2. FSL traces [73]
        3. Mechanism
            1. Data chunking
            2. Leverage cloud infra to Batch Deduplication
                1. we used YARN [76] to schedule jobs, and HDFS [64] for reliable storage of temporary data, so the jobs can be run on spot instances as proposed in the AWS guide [12]
            3. Leverage cloud infra to garbage collect
            4. Moving data chunks to hot/cold tiers
            5. Managing persisted metadata
                1. UFR, PFR
                    1. A container of fingerprint mapped to blocks
                2. Fingerprint index.
            6. Local tier
                1. Minimizing data exchange to cloud
                    1. Local tier uploads UFR (finger print list) to cloud.
                       Cloud identifies unique blocks, send to local tier.
                       Local tier uploads unique blocks to cloud
                2. The local tier can composes of multiple systems
        4. Others
            1. Table 1 cloud storage prices compare. Very useful
        5. My questions
            1. Is pushdown feasible? The cost of fetch data to VM and then write down is much higher
            2. Can the background processing be co-scheduled with cloud workload to pick a more idle time?

    n. related materials
        1. Hydrastor: A scalable secondary storage    [2009, 367 refs, FAST09, 9livesdata]
           https://www.usenix.org/conference/fast09/technical-sessions/presentation/dubnicki
            1. Referenced in the main paper as "We integrate InftyDedup with HydraStor [33], a commercial backup system with deduplication"
            2. Highlights
                1. A file is organized as a tree of blocks (DAG). Only leaves are data.
                2. DHT data placement
                3. Data stream split to blocks
                4. Inline deduplication

5. Characterizing, Modeling, and Benchmarking RocksDB Key-Value Workloads at Facebook    [2020, 256 refs, Facebook]
   https://www.usenix.org/conference/fast20/presentation/cao-zhichao
    1. Analyzed workload characterization in details in RocksDB at Facebook
    2. Highlights
        1. Application traces
            1. UDB, ZippyDB, UP2X
            2. UDB
                1. Social graph data maintained in MySQL tables. Table rows stored as KV-pairs in RocksDB. I.e. MyRocks engine
            3. ZippyDB
                1. Distributed KV-store that uses RocksDB as backend. Usually stores photo metadata and object metadata
            4. UP2X
                1. UP2X is a special distributed KV-store based on RocksDB.
                2. UP2X stores the profile data (e.g., counters and statistics) used for the prediction and inferencing of several AI/ML services at Facebook.
                3. Therefore, the KV-pairs in UP2X are frequently updated
                4. Compaction Filter: delete keys during compaction without Delete operation
        2. Dimensions of workload characterization
            1. Query Composition: Get, Put, Delete, Single Delete, read-modify-write (Merge), Iterator
            2. Key size distribution
            3. Value size distribution
            4. Query Per Second (QPS) daily pattern
            5. KV-pair Hotness and Access Count Distributions
            6. Access Heat-map vs Key space
            7. Key-Space and Temporal Localities
        3. New benchmark vs YCSB
            1. Key-range hotness
                1. we use average number of KV-pairs per SST file as key-range size
                2. a Generalized Pareto Distribution [25]
                    1. 什么是帕累托分布？
                       https://www.zhihu.com/question/25498346
                        1. 帕累托分布是一个skewed，厚尾(fat-tailed)分布
                    2. Wikipedia: Generalized Pareto distribution
                       https://en.wikipedia.org/wiki/Generalized_Pareto_distribution
                        1. GPD is often used to model the tails of another distribution.
            2. Load a snapshot of the database and then replay reads
        4. My questions
            1. Garbage collection pattern is not analyzed?

    n. related materials
        1. MyRocks: LSM-Tree Database Storage Engine Serving Facebook's Social Graph    [2020, 75 refs, VLDB, Facebook]
           https://www.vldb.org/pvldb/vol13/p3217-matsunobu.pdf
            1. UDB
            2. How is query supported in RocksDB to match B+tree index?
                1. Point lookup
                    1. Memory table
                       Global index => levels => SSTs. Locating SSTs should be able to done in memory.
                       SST has an index block for binary search. Need disk reads.
                2. Range query
                    1. Prefix bloom filter to skip levels (sorted runs)
                    2. SingleDelete to walkaround tombstone overhead
                3. How is secondary index supported?
                    1. covering_index technique, by include all relevant columns in the index, so range scan can be completed without randomly reading from primary keys
                       https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos
                    2. Didn't see details. I guess secondary index is just another table. But how to maintain consistency?
            3. How is space made efficient given GC and levels?
                1. The MyRocks instance size was 37.7% compared to the InnoDB instance size with the same data sets
                    1. For InnoDB, space amplification mostly comes from fragmentation and less efficient compression.
                        1. InnoDB wasted 25-30% space in fragmentation
                        2. Also, InnoDB has significant space overhead per row for handling transactions
                    2. LSM-tree's dead data is removed by compaction, and by tuning compaction, we are able to maintain the ratio of dead data to as low as 10% [14]
                        1. Optimizing space amplification in RocksDB    [2017, 216 refs, CIDR]
                           https://www.cidrdb.org/cidr2017/papers/p82-dong-cidr17.pdf
                        2. If 16KB data was compressed to 5KB, RocksDB uses just 5KB while InnoDB aligns to 8KB, so RocksDB is much more space efficient

        2. Optimizing space amplification in RocksDB    [2017, 216 refs, CIDR, Facebook]
           https://www.cidrdb.org/cidr2017/papers/p82-dong-cidr17.pdf
            1. How to "we are able to maintain the ratio of dead data to as low as 10%"?
                1. RocksDB uses two strategies to reduce space amplification:
                    1. adapting the level sizes to the size of the data, and
                        1. The next level is 10x the size of the previous level
                            1. "For most of the Facebook production RocksDB installations, a size multiplier of 10 is used, although there are a few instances that use 8."
                    2. applying a number of compression strategies
                        1. Key prefix encoding
                        2. Sequence ID removed after GC
                        3. Dictionary-Based Compression

6. CFS: Scaling Metadata Service for Distributed File System via Pruned Scope of Critical Sections    [2023, 2 refs, EuroSys23]
   https://dl.acm.org/doi/10.1145/3552326.3587443
   https://mp.weixin.qq.com/s/1uQ1yRq0letKDVTaFDtXTA
    1. POSIX兼容、强一致、横向扩展，使用数据库TafDB管理元数据, RocksDB to mange file contents. Key designs
        1) Co-locating metadata, so most operations touch only one shard.
        2) Offloading file attributes to FileStore. They are not stored in metadata service.
        3) Use atomic primitives rather than locking to update ctime, mtime, atime.
        4) Rename/Move is serialized by Renamer, which is backed by Raft
    2. Highlights
        1. Key architecture
            1. 阶段三：分离式元数据架构
                1. 数据库层：这一层负责数据存储，通常采用 NewSQL 或分布式 KV 系统（以下统称 Table 系统），实现数据的持久化的同时提供分布式事务能力
                   元数据代理层：这一层对外提供 POSIX 或 HDFS 接口，对内将层级命名空间的数据转换成 Table 系统中的记录，处理时利用事务保证操作的正确性
                2. 文件属性分离
                    1. 文件属性（file attributes）从元数据服务中剥离出来，和文件数据（file data）一起放到数据服务（Data Service）中进行处理
                        1. My questions
                            1. How to ensure atomic update on the file content and file attributes?
                            2. How does co-locating work for file attributes if they are pushed down to FileStore?
                    2. Namespace 2.0: Instead of locking the entire file, use atomic variables to update ctime, mtime, atime.
                        1. Single-shard atomic primitives
                3. 读写分离
                    1. 对于读请求，我们绕过了元数据代理层直接访问 TafDB
                    2. Serializable Snapshot Isolation
                        1. 我们决定将每个文件系统的写请求收缩到一个单点进行处理，写扩展性和写延时的问题留到以后再去解决。
            2. TafDB
                1. Distributed table DB with partition split
            3. Renamer
                1. handling complex rename operations that are metadata-intensive
                2. Serialize all transaction into one node. E.g. rename, move.
                3. Multi-Raft 架构，每个文件系统由一个 Raft 复制组提供对复杂 rename，即所谓 Normal Path rename 的支持
            4. ClientLib
                1. ClientLib collapses the metadata proxy layer into the client side
                2. Move metadata prox into ClientLib. Metadata proxy is not needed any more.
                3. 目前支持 FUSE、Samba、NFS-Ganesha
            5. 分布式锁
                1. 上述的实验表明，锁冲突是影响系统扩展性和操作延时的关键。
                    1. 当冲突比例为 50% 和 100% 的时候，锁冲突在整个操作中的占比高达 83.18% 和 93.86%
                    2. 即使在无冲突的情况下，锁在整个操作里的耗时占比也达到了 52.9%
            5. FileStore
                1. Backed by RocksDB, to store file contents, and file attributes
            6. Caching
                1. 由于每个文件系统的元数据写都是单点，Namespace 模块任何时刻看到的数据都是最新的，具备引入缓存的条件，缓存命中情况下事务中的大部分读请求都可以被优化掉
        2. Key challenges
            1. 关联变更、原子性
                1. 例如创建子文件、更新父属性ctime
                2. How does CFS reduce locking overhead in metadata operations?
                    1. co-locating related metadata into one node. only single-shard atomic primitives are needed
            2. rename
            3. 路径查找
                1. <父目录 inode, 子项名称> 索引
                2. <inode> 索引
            4. 获取属性
            5. 范围读，目录遍历
    n. related materials
        1. 如何将千亿文件放进一个文件系统，EuroSys'23 CFS 论文背后的故事
           https://mp.weixin.qq.com/s/1uQ1yRq0letKDVTaFDtXTA
            1. 百度沧海·存储团队 - 百度智能云文件存储 CFS 的元数据系统
            2. good, well-explained DFS challenges
        2. HopsFS
        3. InifiniFS

7. OceanBase: LCL: A Lock Chain Length-based Distributed Algorithm for Deadlock Detection and Resolution    [2023, 0 refs, Alibaba, ICDE23]
    1. OceanBase 提出的方法 LCL 显著优于最先进的竞争对手 M&M 算法. Compared to CockroachDB's, LCL only needs to pass numbers across the graph. 
    2. highlights
        1. 如表1 所示，当前的死锁检测与消除算法主要有四种
            1. 集中式死锁检测，基本思想是选择一个中心节点作为检测器，收集所有节点的锁等待关系，生成全局锁等待图（WFG），应用案例为TiDB[1]。这种方法的缺点是典型应用的锁等待关系通常较为简单，整合所有局部 WFG（wait for graph）的开销较大；
            2. 死锁预防策略，基本思想是在死锁发生之前通过 Wound-Wait，Wait-Die 等策略有选择地杀死事务，应用案例为Google Spanner[2]。这种方法的缺点是大量不会导致死锁的事务被杀掉，用户无法接受；
            3. 路径推动算法(Path pushing)，基本思想是在每个顶点构建局部WFG，每个顶点将其本地WFG发送到多个相邻节点，并重复此过程。直到某个顶点有足够的视图来宣布死锁，应用案例为 CockroachDB[3]。这种方法的缺点是多个顶点会检测到同一个死锁，每个顶点都试图通过杀死一些事务来消除死锁，这可能具有多杀性；
            4. 边追逐算法(Edge chasing)，基本思想就是沿着事务 WFG 的边传播具有特殊意义的消息，死锁产生的环路关系最终将导致消息返回到它的发起者处，从而提示死锁的存在，应用案例为 Oracle RAC和 OceanBase[4]。
        2. Algorithm
            1. 繁殖阶段、扩散阶段和检测阶段
            2. ASG(scc) 中任何 LCLV 最多在 AsgWidth(scc) 轮推演之后传播到 scc
            3. 如果不限制繁殖过程的时间，循环上顶点的 LCLV 可以无限增大，所以 LCL 算法里面会设置时间上限
            4. 繁殖阶段的时间复杂度为 O(N)，其中 N 是 WFG 中有向边的数量
            5. WFG中只要存在死锁就会有 scc，只要存在 scc 就肯定有一个最顶层 scc，详细证明过程见论文附录
            6. cycle leads to infinite lock chain length (LCLV) growth.
            7. Figure 9 shows SCC, USC, and how the algorithm works
                1. My questions
                    1. Per deadlock resolution, which victim transactions should be aborted?
                        1. Probably those in SCC
        3. vs M&M
            1. M&M 和 LCL 主要差异在于: M&M 假设事务等待单一资源，LCL 对事务可以等待的资源数量没有任何限制
        4. Others
            1. 事务执行模拟器（TPE）
    n. related materials
        1. 国际顶会 ICDE入选 | OceanBase 死锁检测实现了哪些技术突破？
           https://zhuanlan.zhihu.com/p/624847601?utm_id=0
        2. CockroachDB死锁处理
           https://zhuanlan.zhihu.com/p/449151313
           https://zhuanlan.zhihu.com/p/472573422

8. MemBalancer: Optimal Heap Limits for Reducing Browser Memory Use    [2022, 1 refs, OOPSLA22]
   https://arxiv.org/abs/2204.10455
   https://www.bilibili.com/video/BV1Yj411977B/
    1. The square-root rule has wide applicable value for resource over-provisioning, e.g. caching, memory, reservation, bursts.
       But note, Square-root rule is derived in the context of garbage collection, and garbage grows at a constant speed g.
       Built upon Javascript engine V8. Evaluation shows MemBalancer can reduce GC time by almost 50% given the same memory usage.
       Good, but,
        1. My questions
            1. Why not just watch the speed of each heap grows and customize heap size?
            2. Why GC time is calculated by L/s, rather than M/s or (M-L)/s
    2. highlights
        1. key algorithms
            1. setting a small heap limit has trade off of longer and more frequent GC time
            2. Instead of individual limit for each heap, use a shared limit for all heaps
            3. derive the optimal heap limit by the "square-root" rule. it achieves coordination without communication
        2. The author's explanation
            1. "一般来说，一个runtime会有一个heap limit（L），当程序消耗内存量达到limit后，则会进行垃圾回收，使得内存使用量下降到limit以下。假设程序自己的live set size（无法被GC清掉的，还在用着的内存）是S, 那一般来说，会设置成L = N * S，其中N是一个2之类的常数。这代表着，一个带GC的程序的最大内存使用量，应该是手动内存管理的内存使用量的两倍。

                但，这其实并不合理！我们在paper里面对垃圾回收进行数学建模，然后寻找一个这个问题的最优解。我们最后发现，应该设置成L = S + N * Sqrt(S)，就是说 - S越大，我们对应于原先的算法，应该给的内存越小！这时候，我们的算法在v8 javascript engine上可以比原先的GC快30%（同等内存），又或者同等时间下节省15%的内存。我们的算法也实现进了racket，也一样有很好的结果。

                这对应着经济学的边际效用递减原理 - 对于一个用了很多内存的VM，我们再多给一些内存，并不会造成很大影响。但是对于一个只用了一点点内存的VM，再多给同样多的内存，会造成更显著的影响。做一个奇怪的例子，你v我50吃肯德基疯狂星期四，跟你v Bill Gate 50，是完全不一样的概念 - 人家不差你这50，但我差。KFC，很奇妙吧。"
            2. Square-root rule
                1. GC overhead = GC frequency * GC time = g/(M-L) * L/s
                   Summing up each heap's overhead
                2. Optimize: minimize sum of overhead
                             keep constant sum of M 
                   They we get we need M = L + c*sqrt(L)
                3. "For sum ratio to be minimized, a kind of “no-arbitrage condition” needs to hold: reducing one tab's heap limit by a tiny amount and then increasing another tab's heap limit by the same amount should not impact sum ratio. Therefore, 𝜕ratio/𝜕𝑀 must be equal for all tabs."
            3. My questions
                1. Why not just watch the speed of each heap grows and customize heap size?
                2. Why GC time is calculated by L/s, rather than M/s or (M-L)/s
    n. related materials
        1. OOPSLA 2022有什么值得关注的论文？
           https://www.zhihu.com/question/559160156/answer/2722391734
            1. The author's in personal reply
        2. TMO: Transparent Memory Offloading in Datacenters

9. Orthus/NHC: The Storage Hierarchy is Not a Hierarchy: Optimizing Caching on Modern Storage Devices with Orthus    [2021, 32 refs, FAST21]
   https://www.usenix.org/conference/fast21/presentation/wu-kan
    1. Allow overloaded cache hits to be offloaded to the lower layer slower device.
       The key takeaways, we should combine the max throughput of both cache + capacity device.
       Evaluation shows overall throughput improvement by ~20%.
    2. Highlights
        1. Non-Hierarchical Caching (NHC)
            1. Problems to solve
                1. The differences between today's neighboring layers are less clear and even overlapping (depending on workloads)
                2. Due to introducing Intel Optane SSD
            2. Non-Hierarchical Caching (NHC)
                1. Key idea: augmenting caching with dynamic load admission and request offloading
                2. avoid excess load to cache device when it is saturated, e.g., too many cache hits
                    1. Classic caching is (data_admit = true, load_admit_ratio = 100%)
                    2. Tune load_admit_ratio
                        1. Turn off data admission for read misses
                        2. feedback-based tune small step by step

10. Empowering Azure Storage with RDMA    [2023, 15 refs, microsoft, NSDI23]
    https://www.usenix.org/conference/nsdi23/presentation/bai
    1. Good. Azure Storage's experience of onboarding RDMA and DCQCN. Probably the largest RDMA deployment in the world
    2. Highlights - talk
        1. Why important?
            1. Majority of network traffic is storage-related
                1. ~70% percent of total
            2. Optimizing brings cost saving and better performance
                1. Sell freed-up CPU cores in compute
                2. Buy cheaper servers in storage
                3. Lower IO latency and jitter
        2. RDMA
            1. Offload network traffic from general purpose CPU
                1. NIC handles all DMA
            2. Performance
                1. RDMA single thread ~40Gbps
                2. RDMA latency 1~2 us
                3. Current NIC can achieve ~100Gbps for a single flow
            3. Our choice - RoCEv2
                1. Compatible with Ethernet/IP. Hence cheap
                2. Can scale to DC and beyond
                3. InfiniBand (IB) is completely custom stack (L1-L7)
        3. Challenges
            1. RoCEv2: PFC, buffer management, congestion control, etc
                1. PFC
                    1. Put InfiniBand L4 it into UDP packet
                    2. "InfiniBand L4" doesn't like packet drop - Lossless Ethernet
                        1. RoCEv2 relies on Priority-based Flow Control (PFC) to make the network lossless.
                        2. But, PFC has problems at scale. It sends PAUSE frames to pause upstream sender when queue > threshold. HOL blocking
                            1. But ... PFC is problematic at scale. Sending a spike of PAUSE frames
                                1. E.g., the switch sends PFC pause frames from port 1 and 2, but Flow 3 is paused though it doesn't create any congestion 
                                2. Solution: PFC as last resort - DCQCN
                                    1. Still use PFC, it's needed for IB transport
                                    2. But minimize PFC generation. Per-flow E2E Congestion Control
                                    3. This is DCQCN
                                        1. ECN-based, RTT-oblivious congestion control
            2. Tailor storage code for RDMA
                1. sU-RDMA additions for storage backend
                    0. sU-RDMA: storage user space RDMA
                    1. Translate sockets API to RDMA verbs
                    2. Multiple transfer modes based on message sizes
                    3. Automatic TCP/RDMA failover
                        1. RDMA doesn't like congestion rates. When you have a bad link that corrupting packets, TCP would be OK, but RDMA doesn't. You would have automated system to remove that link, but there still would be a few minutes that it suffers. In this window, you need RDMA to fall back to TCP.
                    4. Still passing through the OS kernel
                        1. My questions
                            1. Why not DPDK?
            3. Performance monitoring: RDMA Estats
                1. On host: RDMA Estats and NIC counters
                    1. Akin to TCP Estats.
                        1. It provides fine-grained latency breakdown for each RDMA operation between CPU/NIC/Remote NIC
                        2. Be careful to sync the CPU clock and NIC clock
                2. On routers: standard router telemetry
                    1. PFCs sent and received, per-queue traffic and drop counters, special PFC WD summary
            4. And many others
                1. Lessons learned
                    1. Focus more on "system" consideration
                        1. than details of congestion control algorithms
                    2. Design must accommodate legacy hardware and heterogeneity
                        1. No greenfield designs
                        2. Test, test, test
                    3. Monitoring, serviceability and backward compatibility are primary considerations
                        1. Cannot be bolted on later
                    4. Some tuning is unavoidable
                        1. Implementation details matter
                        2. Traffic patterns evolves
                        3. Router buffer management is complicated.
                    5. Joint design
                        1. Layering is good, but have gaps
                        2. Host networking stack, routing, buffer management must work together to deliver high performance
    3. Highlights - paper
        1. Combines RDMA send/write for different message sizes: [87] Transport protocol and interface for efficient data transfer over rdma fabric
        2. sK-RDMA fully kernel model RDMA, rather than fully user mode
        3. RDMA Extended Statistics like TCP's
        4. SONiC switch OS
        5. Hardware programmable traffic generator [9]
        6. Long links over T2 and RH
            1. deep packet buffers of off-chip DRAM
            2. shared PFC headroom pool and being oversubscribed with a reasonable ratio
        9. Figure 10, why SSD read/write latency with TCP vs RDMA are not much different? 
        10. Figure 11, DCQCN withOUT a right config can mess up the latency
        11. Message chunking, only allowing a single in-flight chunk, effective to mitigate high-degree incast 
        12. Switch/NIC firmware at scale can have bugs in performance plane
        13. Open problems for future
            1. Failovers are very expensive for RDMA. Think the extra CPU needs to be provisioned for falling over to TCP
            2. Host network and physical network should be converged. Speed of networking is catching up with intra host
            3. Switch buffer has a strong correlation with RDMA performance problems, need more buffer as higher link speed and farther distance
    
    n. related materials
        1. DCQCN: Congestion Control for Large-Scale RDMA Deployments
           https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p523.pdf
        2. 论文笔记：微软 Azure 网络演进 - Pavinberg
           https://zhuanlan.zhihu.com/p/624228199
            1. Many papers listed, useful 

        3. Meta：大规模分布式AI训练的RoCE网络（论文） - Andy730
           https://mp.weixin.qq.com/s/7oLhn51h1NE-XIZn_UOm3g

11. Distributed Transactions at Scale in Amazon DynamoDB    [2023, 0 refs, ATC23]
   https://www.usenix.org/conference/atc23/presentation/idziorek
    1. 2PC snapshot read and atomic write transaction implemented on KV store without MVCC. Serializable level.
       Timestamp ordering is implemented with OCC. Non-transaction RW pays no cost.
       Interesting optimizations on transaction read/write leveraging no MVCC support.
    2. Highlights
        1. Key design points
            1. Transaction is implemented by 2PC
            2. Non-transaction operations don't pay for transaction
            4. Transaction update items in place, no MVCC
                1. The implication of a single-version store for transaction processing is that read-only and read-write transactions might conflict
            5. Transactions are serially ordered using timestamps
                1. The clocks in the coordinator fleet are sourced from the AWS time-sync service [1]
                    https://aws.amazon.com/blogs/aws/keeping-time-with-amazon-time-sync-service/
                    1. NTP based
                    2. Aurora Limitless made TimeSync similar with Google TrueTime
                       https://zhuanlan.zhihu.com/p/670412648
                       https://youtu.be/a9FfjuVJ9d8?si=oEH5WM-zvpCD9dP8&t=1942
                1. Transactions do not acquire locks, use OCC
            7. Transaction semantics
                1. TransactGetItems - get a consistent snapshot
                2. TransactWriteItems - atomic write set
                3. CheckItem - check condition and write
        2. transaction coordinator
            1. Write Tx
                1. The storage node accepts the transaction if
                    1. The transaction's timestamp is greater than the item's timestamp indicating when it was last written
                        1. My questions
                            1. See Listing 3 "AND item . ongoingTransactions == NONE". This means a prepared item would reject any other Tx prepares. Isn't it a locking?
                    2. each participant storage node performs the desired writes on its local items and records the timestamp of the transaction as the items' last write timestamp.
                2. Items for which a precondition was checked but that are not being written also have their timestamps updated.
                    1. Interesting
            2. Read Tx
                1. OCC - read twice with data and LSN. If LSN no change in middle, read can succ
                    1. My questions
                        1. What about atomicity? It seems nothing prevents reading a half committed write Tx
            3. Recovery and fault tolerance
                1. coordinators maintain a persistent record of each transaction and its outcome in a ledger
                2. multiple Transaction coordinators. OK to reassign a slow transaction
                3. it is okay for multiple coordinators to be finishing the same transaction at the same time since duplicate attempts to write an item are ignored by its storage node
                    1. interesting
        3. optimizations
            1. Inserting transaction timestamp
                1. Read/write to individual item can succ even the item has prepared for a transaction.
                   The timestamp is generated as in middle of (the last time, the prepared Tx).
                    1. interesting
                    2. My questions
                        1. Write doing this is not likely to be correct. It breaks the condition check of prepared Tx.
                           Doing so is not actually serializable.
                           Or, only feasible because this paper's Tx is separating read Tx and write Tx cannot mix.
                            1. OK .. the paper noticed the problem. A write Tx also supports condition check, rather than blind write.
                2. Individual write can be committed if an item has prepared for a transaction but OK to overwrite.
                3. An item can prepare for more than one transactions, given they can commit in order, without violating condition checks.
                    1. Anyway, these optimizations are doing write overwrites, leveraging no MVCC is needed
        n. My questions
            1. Seems long running transactions are not supported yet
            2. Can TransactWriteItems include snapshot read? Otherwise how can read-write Tx be serializable?
                1. This is biggest problem from truly doing serializable
            3. No MVCC means read transaction can conflict with write transaction. How bad is it?
    n. Related materials
        1. [译] [论文] Dynamo: Amazon's Highly Available Key-value Store（SOSP 2007）
           https://zhuanlan.zhihu.com/p/374807359

13. Dayu: Fast and Low-interference Data Recovery in Very-large Storage Systems    [2019, 15 refs, ATC19, Alibaba]
    https://www.usenix.org/conference/atc19/presentation/wang-zhufan
    1. Interesting. Timeslot-based scheduling - drop the task if current timeslot doesn't have enough bandwidth.
       Build the convex hull to use binary search rather than scanning all the nodes which are too many.
       Evaluated on Pangu traces. 2.96x recovery speed faster than Pangu-slow, same recovery speed with Pangu-fast but lower latency.
    2. Highlights
        1. Alibaba production observation
            1. 3500 nodes in our observed cluster
            2. Every node stores 250K chunks on average
            3. Replicas of lost chunks are distributed unevenly among other nodes
            4. Recovery should adjust with foreground traffic
            5. Recovery should handle stagger nodes
        2. Dayu solution - recovery scheduler to be fast and high quality
            1. Centralized scheduler
            2. Timeslot-based scheduling
                1. gather latest info to schedule tasks
                2. overlapping timeslots
            3. Algorithm in one timeslot
                1. Bucket convex hull optimization to choose the source and destination
                    1. minimized (Accumulated size + task size) / node bandwidth - expected finish time.
                    2. choose from 2 candidates, the power of randomly two choices.
                    3. if the current timeslot doesn't have enough bandwidth, drop the task to the next.
                    4. Problem - too many nodes to scan them all
                        1. Build the convex hull, then find the best node on convex shell through binary search
                2. Underemployed node recognition to adjust the task priority
                3. iterative WSS algorithm to assign bandwidth (WSS - weighted shuffle scheduling)
                    1. WSS - Managing Data Transfers in Computer Clusters with Orchestra
                4. Heuristic algorithm to minimize the cost of re-scheduling stragglers
        3. Others
            1. Figure 1(c), 2(d). Use CoV to measure foreground traffic imbalance and churn.
            2. Figure 1(e), size of chunks are mostly 20GB to 40GB.
            3. Implemented by modifying Pangu MetaServer, RootServer, ChunkServer. and Introduced ObServer for global information.
               Testbed on 1000-node cluster deployed Pangu-based Dayu.
    n. Related materials
        1. WSS: Orchestra: Managing Data Transfers in Computer Clusters with Orchestra    [2011, 801 refs]
           https://www.mosharaf.com/wp-content/uploads/orchestra-sigcomm11.pdf
            0. As referenced in the parent paper
                1. "The key idea of WSS is that, to finish all the pairwise transfers at the same time, it guarantees that 1) transfer rates are proportional to data sizes for each transfer, and 2) at least one link is fully utilized."
                2. Dayu's improvement is to make WSS iterative, so that over multiple iterations, so that bottleneck links adapt and even out.
            1. Introduced ITC to manage data transfer in Spark or MapReduce-like framework.
            2. Highlights
                1. Inter-Transfer Controller (ITC)
                2. WSS
                    1. Each transfer pair is assigned a speed λ = data size / transfer time. So that all pairs finish transfer at the same time. Only one pair bandwidth is fully utilized.
                    2. WSS schedule must finish at least as fast as the progressive filling schedule, making it an optimal solution for shuffle scheduling

14. Presto: A Decade of SQL Analytics at Meta    [2023, 0 refs, Facebook, SIGMOD23]
    https://research.facebook.com/publications/presto-a-decade-of-sql-analytics-at-meta/
    1. Good and comprehensive. Years of Presto improvement and experience on latency/scalability and integration with Spark.
       Caching, vectorized execution, filtering and join, materialized views,
       multi-coordinator, Recoverable grouped execution, spark integration, spilling,
       cost-Based Optimizer, history-based optimizer, Adaptive execution
       Mutable delta data, UDT, UDF, graph extensions.
    2. Highlights
        1. See the attached article
    n. Related materials
        1. [SIGMOD-2023] Presto: A Decade of SQL Analytics at Meta - 水木清扬
           https://zhuanlan.zhihu.com/p/649803696
            1. Presto 是一个开源分布式SQL查询引擎，2013年在Meta推出，并于2019年捐赠给Linux基金会。在过去十年中，随着 Meta 数据量的超高速增长以及新的 SQL 分析要求，如何保持查询延迟和可扩展性给 Presto 带来了巨大挑战。Presto做了一些重要的优化，如分级缓存、native向量化执行引擎、物化视图和Presto on Spark。
            2. 因此presto提出了新的架构，如上图所示，分为了两种集群
                1. 原始presto架构，但（1）采用多个Coordinator避免单点故障。（2）使用native向量化执行引擎提高性能。（3）data cache on flash避免IO瓶颈。（4）其它改进
                2. Spark上的presto，利用Spark做runtime，presto作为evaluation library提高扩展性。
                3. 还有一些其它的改进
                    1. 支持物化视图来提高查询性能和数据可变性
                    2. 支持将内存中的数据溢出到临时存储中以克服内存限制（Spill）。
                    3. 原始presto架构支持物化中间结果，以提高recoverability。
                    4. 引入了额外的元数据。Type store用于支持用户定义的类型，function store用于支持sql function的编写和evaluation，statistics store用于更好的优化决策，remote functions用于运行user-defined functions。
            3. Latency Improvements
                1. Caching
                    1. presto引入了不同级别的缓存
                        1. Raw Data Cache
                        2. Fragment Result Cache
                        3. Metadata Cache and Catalog Servers
                    2. Cache locality
                        1. 为了最大限度提高缓存命中率，Coordinator使用哈希函数将同一文件的读取请求调度给同一个worker，为了避免出现热点worker，调度器可能会回退到第二选择的worker上，或在必要时跳过缓存。
                        2. 查询路由上也有相同的逻辑，由于presto在全球多个数据中心部署，路由器会将查询重定向到拥有缓存数据的集群上，同时将hotspot prevention作为fallback
                2. Native vectorized execution
                    1. Velox是Meta位支持C++向量化执行而从presto孵化出的一个项目，后来成为了一个通用的向量化执行库。
                3. Adaptive filtering
                    1. Subfield Pruning
                        1. 现代数据仓库中广泛使用map、array、struct等复杂类型结构，为了提高CPU效率，需要在不读取整个复杂对象的情况下有效提取子字段。Presto支持子字段剪枝，向reader发送所需的复杂对象的索引或key的信号。
                    2. Filter recordering
                        1. 有些filter能在更少的CPU cycle中删除更多的行。所以Presto会自动重排序filter，使选择性更强的filter排在前面。
                    3. Filter-based lazy materialization
                        1. 按顺序应用一组filter时，Presto会track那些满足filter谓词的行，那些不满足的行就不需要再过后面的filter了。比如现在有两个filter，分别为col1 > 10 and col2 = 5，先运算col1的表达式，col1是必须物化的，但是只有通过col1>10 的行才需要物化col2.
                    4. Dynamic join filtering
                        1. 比如对于inner join，通过build端数据提供能代表简易“摘要”的bloom filters/ranges/distinct values作为filter下推给probe端。
                        2. 这里另外说一下，这里的dynamic join filtering也可以称为runtime filter，在一些系统里叫dynamic filter，其核心思想主要是用于HashJoin中，使用build端构建一个轻量的filter，下推给probe端，可以通过build端的range信息和chunk的统计信息直接过滤掉chunk节省IO，也可以过滤每行数据，因为filter较为轻量，过滤度较好情况下可以减少CPU开销，也可以减少后续可能需要shuffle的网络开销。除了用于HashJoin里，也还有一些其它场景可以使用。
                            1. Good.
                5. Materialized views and near real-time data
                    1. 当前存在的问题：用户较少使用原始数据来构建dashboards，因为原始数据通常非常多，无法提供低延迟的体验。人们倾向于通过预计算表来提前减少基数，但是这种方法不适用于NRT（near real-time）实例，因为数据是连续不断变化的。
                    2. 因此，presto提供了物化视图的功能，物化视图是由查询表示的视图，其结果被存储起来。
                        1. 物化视图更新：当presto创建一个物化视图时，会创建一个automatic job来为该视图物化数据。只要基础表的某些单位（通常是小时或天）变得不可变，automatic job就会运行视图查询来物化视图的数据。
                        2. 物化视图查询：当用户查询物化视图时，presto会将物化数据的查询和非物化数据的查询union all起来，这样，由于数据量减少，查询既能保证fressness又能降低延迟
            4. Scalability Improvements
                1. Presto改进了架构，集成了各种改进以处理单点故障、worker crash、数据倾斜、内存限制等问题。
                2. Multiple Coordinators
                    1. Presto通过separating查询和集群的生命周期来解决这个问题。Coordinator只控制查询的生命周期，新引入的Resource managers负责集群的队列和资源利用率监控，其架构如上图所示。
                    2. Coordinator定期从resource managers获取排队信息，以决定执行哪些查询，或者队列中查询优先级较低，可以执行一个新提交的查询，以避免排队开销或网络跳转延迟。
                3. Recoverable grouped execution
                    1. 问题：1. 不能扩展内存限制，2. 不能可靠保证worker不会崩溃
                    2. 如果表扫描后的第一个聚合/连接/窗口函数的key是数据分区key的超集，查询就能以“分组”方式执行，查询时会逐个对分区进行扫描，如果发现内存超出限制，就会执行分组查询以降低峰值内存损耗。
                4. Presto on Spark
                    1. Presto on Spark架构用Spark取代了presto内置的调度器、洗牌、资源管理和任务执行
                    2. Presto的Coordinator和worker等presto服务都是library，它们之间不会互相通信，也不会管理内存、线程或网络。为了简化，这些方面都从库中移除，委托给了spark集群。
            5. Efficiency Improvements
                1. Cost-based optimizer
                2. History-based optimizer
                    1. 由于Meta的ETL工作大量使用Presto，因此查询具有高度重复性和可预测性，基于历史记录的优化器的理念是利用之前完成的重复查询的精确执行统计数据来指导未来重复查询的规划
                    2. Interesting
                3. Adaptive execution
                    1. 如果在运行期间执行计划不是最优的，就需要自适应执行来动态调整查询计划。自适应执行利用已完成的任务向Coordinator报告统计数据，以便Coordinator利用这些数据为下游任务重新优化计划。
                    2. 为了利用运行时统计数据，调度器会分阶段调度任务，从扫描任务一直到root，当上游任务完成后，优化器将根据新收集的统计数据重新计划，并根据新计划调度下游任务。
            6. Enable Richer Analytics
                1. 除了改进分析型工作负载的延迟、可扩展性和效率外，Meta 还越来越倾向于强调机器学习特征工程user cases，增加对隐私要求和图形分析的支持。
                    1. 以机器学习和隐私为重点的需求不断增长，已逐渐将传统的以分析为重点的数据仓库转变为更加开放和灵活的“数据湖”设置。分析数据不再是一成不变的。Meta需要能够根据用户的隐私选择删除用户数据。在机器学习特征工程中，可以灵活添加columns以尝试不同的候选特征。
                2. Handling mutability
                    1. 数据仓库历来只支持不可变数据，近几年，可变数据支持版本控制的趋势越来越明显。
                    2. Presto内置了Delta，允许表的变化，可以灵活地添加或移动列或行。Presto 读取主文件时，会启动额外的读取器来合并这些delta文件，以反映变化。delta 文件的关联和顺序保存在元数据存储中，并进行版本控制。
                3. User-defined types
                    1. 例如，可以根据 Long 类型定义 ProfileId 类型，并将 UserId 和 PageId 类型作为其子类型。用户定义的类型定义存储在远程元数据存储区中。
                    2. 还可以将额外信息与用户定义的类型关联起来。例如，通过 SQL 表达式表达的约束条件。这样就可以在运行时进行数据质量检查。例如，用户 ID 不能是负整数或超过一定长度。
                4. User-defined functions
                    1. In-process UDF：函数以library的形式编写和发布，presto在运行时加载library，并在与main evaluation engine相同的进程上执行。
                    2. UDF service：为了支持多租户模式或不同编程语言中的UDF，presto构建了UDF service，这些函数通过presto集群的RPC在远程服务器上调用。
                    3. 由于一个表达式既可以包含本地可执行函数，也可以包含远程UDF，因此在编译时，表达式将被分解为本地可执行和远程可执行。
                    4. SQL functions：虽然UDF具有灵活性，但出于审计和隐私保护的目的，查询必须能够被“reasoned”，不能有黑箱的执行。当函数逻辑可以用SQL表达时，允许用户定义SQL函数
                5. Graph extensions
                    1. 图查询会被解析为一个特殊的图逻辑计划，然后利用图查询的语义对其进行优化。最终，优化后的图逻辑计划被转换为关系计划，并像其他 Presto 查询一样执行。
                    2. Multi-step execution：像上图中这样的简单查询会转化为关系查询，其连接次数与路径的最大长度相同。这种查询可能会达到 Presto 的内存限制，尤其是当有太多的路径需要计算时。为了解决这个问题，presto实现了一种优化方法，将图查询计划转化为一系列较小的 Presto 查询计划。每个较小的查询计划都会计算一定长度的路径，并将其存储到临时中间表中，然后继续扩展路径。这样，每次迭代都不会超出内存限制。
                    3. Efficient path extension：还是看上图，一个简单的计划会计算长度为 1、2 等的路径，并对它们进行 UNION ALL。这将导致冗余计算。计算长度为 的路径所需的工作量与计算长度为 - 1 的路径相加上将它扩展为长度为 的路径相同。
                    4. Efficient subgraph computation：只需要跟踪已访问过的边。这样，子图计算规划就可以从存储中扫描一次edge table，然后在可以扩展的情况下将边标记为已访问过，从而最大限度地减少 IO。
                    5. Complex filter pushdown：然而，图语义信息允许在每次连接后直接向下推送这些过滤器，每个过滤器都会计算下一跳，从而最大限度地减少计算的中间路径数量。
            7. Performance in Production
                1. P75 is ~3 seconds. P90 is ~10 seconds. No change with fast growth of data.
                2. Presto on Spark usage is new but fast growing

15. Shared Foundations: Modernizing Meta's Data Lakehouse    [2023, 7 refs, CIDR DB]
    https://research.facebook.com/publications/shared-foundations-modernizing-metas-data-lakehouse/
    https://www.youtube.com/watch?v=wyOTpcYrEF0
    1. Generational leap in the data infrastructure landscape. Open formats, consolidating languages, engines: CoreSQL, Velox, Presto
    2. Highlights
        1. Background
            1. Usage Trends
                1. Data Explosion
                2. Machine Learning
                3. Freshness and Latency
                4. External Analytics
                5.  Complex Data Models
                6. Richer Query Methods
            2. Environmental Trends
                1. Disaggregation
                2. Horizontal Scaling
                3. Elastic Compute
                4. Power Efficiency
                5. Global Optimization
                6. Engineering Efficiency
            3. The problem: Fragmentation
                1. Layer
                    1. Language
                    2. Distribution/Runtime
                    3. Execution
                    4. Data Access
                2. Scope
                    1. SQL dialects, functions, entity & type metadata
                    2. Distributed execution, shuffle, resource management
                    3. Evaluation at node, caching
                    4. Formats, storage disaggregation
                3. Challenges
                    1. SQL dialect fragmentation, lack if expressibility
                    2. Scalability, Efficiency, Fragmentation
                    3. Latency, efficiency, Java / C++, dialect fragmentation
                    4. Library fragmentation, not data driven, poor encodings
        2. Solution: Open Data Lakehouse Analytics
            1. Direct data access
                1. Disaggregated storage
                2. Open file formats
                3. Open metadata APIs
            2. Diverse applications
                1. Batch
                2. Interactive
                3. Streaming
                4. Machine Learning
            3. Consolidation
                1. Language consolidation
                    1. PrestoSQL -> CoreSQL
                2. Execution consolidation 
                    1. Velox
                3. Engine consolidation
                    1. Presto -> RaptorX -> Prestissimo
                        1. Presto running on Velox
                    2. Presto on Spark
                    3. Stream Processing - XStream
                        1. CoreSQL
                        2. Velox for execution
                    4. Machine Learning
                        1. File format inefficiencies -> Alpha
                            1. make available via Velox

16. Towards Building Autonomous Data Services on Azure    [2023, 2 refs]            
    https://pages.cs.wisc.edu/~yxy/cs839-f23/slides/L17-2-auto-azure.pdf
    1. Highlights
        1. What is an autonomous data service?
            1. improving ease of use, optimizing performance, reducing costs, and maintaining data privacy
            2. layers
                1. Cloud Infrastructure layer
                2. Query engine layer
                    1. queries and jobs are often recurrent and similar
                3. Service layer
    n. Related materials
        1. SIGMOD 2023 有哪些值得关注的论文？ - James的回答
           https://www.zhihu.com/question/557505628
            1. "Towards Building Autonomous Data Services on Azure. 应该是今年sigmod作者最多的的文章，关注一下大工作。"

17. HQI: High-Throughput Vector Similarity Search in Knowledge Graphs    [2023, 0 refs, Apple]
    https://arxiv.org/abs/2304.01926
    1. Interesting. qd-tree based index for hybrid search (ANN + multiple relational predicts). it transformed vector similarity to relational numbers (k-means centroid id) that can be indexed by qd-tree.
    2. Highlights
        1. Background
            1. Knowledge Graph
            2. Hybrid vector similarity search - ANN with relational field filters
            3. filter commonality and filter stability. and relation predicts relate to query vectors
        3. Workload-aware index for hybrid search
            1. Traditional approach: partition by relational attribute first, and then construct vector index (IVF, HNSW) at each partition
            2. Our solution
                1. query predict attributes can cover multiple attributes
                2. Based on qd-tree, a learned index, and semantic description to each partition.
                    1. semantic description of the qd-tree is simply a bitmap donating which ancestor predict evaluated to true
                3. To work with qd-tree, transform vector similarty and relational attribtues to a uniformed manner
                    1. use k-means to get centroids. each vector is associated with a centroids which is transformed into a number. a query is transformed to matching a group of numbers, where each number is a centroid near to it.
    n. related materials
        1. SIGMOD 2023 有哪些值得关注的论文？ - James的回答
           https://www.zhihu.com/question/557505628
            1. "High-Throughput Vector Similarity Search in Knowledge Graphs. 苹果如何做高维向量搜索。"
        2. High-Throughput Vector Similarity Search in Knowledge Graphs - Chao.G
           https://zhuanlan.zhihu.com/p/641031533
            1. Background
                1. 混合查询 - 在向量检索领域一般认为是带上属性过滤条件的 ANN 查询
                2. workload-aware，作者发现在这种知识图谱的 workloads 中混合查询的过滤条件具备一定规律性（文章中根据过滤条件的选择率列出了 10 种作为 filter template）
                3. pre-filter 和 post-filter
            2. Query Batching
                1. 对于相同过滤条件的 query 可以 group 在一起
                2. 因为 HQI 采用的是 IVF 类的索引，对于访问相同 posting list 的 query 可以 group 在一起，利用硬件对矩阵乘法的深度优化

18. Photon: A Fast Query Engine for Lakehouse Systems    [2022, 32 refs, CIDR DB, Databricks]
    https://people.eecs.berkeley.edu/~matei/papers/2022/sigmod_photon.pdf
    https://www.youtube.com/watch?v=TDrIt1RDFqQ
    1. Databricks experience on improving query engine. Spark integration, native C++ and memory management, Interpreted vectorized execution.
    2. Highlights
        1. Background
            1. Lakehouse: performance with data warehouses, and flexibility and open formats like Datalakes
        2. Photon query engine
            1. 100% Apache Spark compatible, built ground up for best performance. ~2x faster than the preceder
            2. Key points
                1. Interpreted vectorized execution model rather than code generation
                    1. Based on MonetDB/X100 system
                2. native code using off-heap memory, JNI no copy
                    1. implement using native C++ rather than Databricks Runtime (DBR) which is based on JVM
                3. integration with Spark UDF
                    1. converting Spark plans to Photon plans
                    2. Photon hooks into Spark's memory manager
                4. querying raw uncurated data
                5. adaptive execution, at batch-level adaptivity
    n. related materials
        1. 论文解读 Photon: A Fast Query Engine for Lakehouse Systems - zhanglistar
           https://zhuanlan.zhihu.com/p/511400714
            1. "这篇论文是databricks公司首次将内部的基于c++的native执行引擎细节发表在SIGMOD 2022"
            2. Background
                1. "论文首先阐述了lakehouse的作用。首先，企业会将大量数据存储在弹性、可扩展的data lake上比如amazon s3、azure data lake storage，google cloud storage等，这些数据可能是以apache parquet、orc、delta lake等open file format存储的raw、uncurated datasets，客户/用户可以通过presto，spark等计算引擎访问，工作负载包括BI，ml等。

                其次，为了获取更高的性能、数据治理，企业会通过ETL把部分数据从data lake上传输到data warehouse（比如apache hive)中，实际这是一个两层的存储架构，这样带来的成本显而易见。

                所以，出现了所以lakehouse（databrick的产品就是Delta Lake）基于对象存储构建了data warehouse的能力，比如统一的数据访问、数据治理、SQL支持等，这样的单层架构对于用户访问数据非常友好。为了更好的查询performance，delta lake做了不少的优化，比如transactions和time travel，data clustering和data skipping indeices等。但是仅仅在存储层努力是不够的，还需要在query engine 这层努力，这就是本论文要阐述的photon。"
            3. Photon主要的挑战
                1. "与传统的data warehouse上的执行引擎不同，photon需要解决新问题，就是raw、uncurated data(可以理解为不规则数据），其特性是：可能存在是highly irregular datasets，poor physical layout，large fields，no useful clustering or data statistics，string来代表date或者int，数据缺失值不一定用NULL填充而是默认值等等。"
                2. "希望支持已有的spark，并且语义兼容，表现在SQL兼容和dataframe API兼容，也就是说对于上层用户来讲是透明的。"
                   "大体来说，Databricks有一个从apache spark fork的一个databricks runtime（DBR)，加入了更多的优化和改进。"
                3. "这毫无疑问，随着硬件发展目前计算引擎已经从早期的io bounding转向了cpu bounding，我们的集群也是如此，因此如果重构必然要基于c++重写，另外一个例证是presto也在基于c++做native query engine。现在的趋势就是基于c++或者rust构建native的执行引擎，未来jvm的执行引擎可能会逐渐淡出历史舞台完成其历史使命，在大数据早期因为受限于磁盘或者网络，整个系统的瓶颈往往在IO，因此jvm构建是合适的，可以更快的构建出产品比如hadoop spark presto等。

                目前网络普遍在20Gbps甚至50G/100G，RDMA技术，磁盘也从早期的HDD发展到SSD，傲腾等带宽更大、延迟更低，加上软件上的异步预取、cache、并行计算等技术，IO瓶颈已经基本消除。CPU重新成为瓶颈。"
            4. Photon key points
                1. The Databricks Runtime（DBR）
                2. 总体上，photon是用c++实现的一个列式、批处理也就是vectorized query engine，以shared lib迁入到DBR，run as part of single-threaded task in DBR within an executor's JVM process
                3. interpreted vectorization vs code-gen
                    1. 这里的主要问题是计算框架采用向量化还是code gen？前者代表论文是monetdb/x100，后者代表论文是hyper。前者的实现代表是clickhouse，monetdb，后者是spark sql，hyper，impala等。
                4. partial roll out. 如果部分算子还没有实现，那么需要能fallback到老的代码
                5. "所以在photon spilling operator比如hash join，group by等，对于输入数据的处理分为2个阶段，第一阶段是内存的reservation，第二阶段是allocation阶段，这样再第二阶段不会发生spill，这样就保证了当前op的高效处理，photon团队也强调这样的策略很关键，因为在context中数据量经常很大如果说在处理当前op经常会发生spill的话，整个流程就又卡磁盘IO了，并不能发挥出向量化执行引擎优势。"

19. PolarDB-IMCI: A Cloud-Native HTAP Database System at Alibaba    [2023, 3 refs, Alibaba, SIGMOD23]
    https://arxiv.org/abs/2305.08468
    1. Good. HTAP implemented with CALS commit-ahead log shipping, to dual-format RO nodes (row-wise vs columnar), and dedicate nodes to serve in-memory columnar index. user transparent of OLTP vs OLAP, by auto routing the queries.
       Replicate REDO log rather than binlog. 评估表明，重用REDO日志的开销明显低于使用Binlog. Two-Phase Conflict-Free Parallel Replay. Good innovation.
       TPC-H (100GB) 上将分析查询速度提高了 149 倍，OLTP工作负载上引入了低延迟和很小的性能扰动（<5%）。 Performance at ClickHouse level.
       PloarDB-IMCI claims to be the only database the achieved goals G#1 ~ G#5.
    2. Highlights
        1. See the article
        2. My questions
            1. PolarDB uses dedicated in-memory index served on dedicated node to support OLAP, but NOT columnar replica?
                1. "如图4所示，PolarDB-IMCI中的列索引作为现有行存储的补充存储。" Row Group data is still sent to Polar FS. It sees the columnar replica is just called in-memory column index here, and the in-memory index does have its on-disk components. maybe it requires all data to be loaded in-memory?
                2. It's called "index" probably due to RID locator, that is a link from keys to row ids.
                3. column index is rebuilt from row store. though column index have checkpoints.
                   "When adding a new RO node, PolarDB-IMCI first checks whether there is an available checkpoint of column indexes in PolarFS. If so, it loads the checkpoint and performs fast recovery; otherwise, it rebuilds column indexes from the row store."
            2. Single RW Nodes with Multiple RO Nodes. Is it really well to not scale out writers?
                1. partitioning should be supported
    n. related materials
        1. HTAP -- PolarDB-IMCI:A Cloud-Native HATP Database - Hugo
           https://zhuanlan.zhihu.com/p/639227492
        2. [SIGMOD2023] PolarDB-IMCI: A Cloud-Native HTAP Database System at Alibaba - 西西弗斯
           https://zhuanlan.zhihu.com/p/641678511
            1. Key points
                1. G#2: Advanced OLAP Performance
                    1. in-memory column index. 
                        1. Row Group 默认每个行组 64K 行， Pack meta跟踪最小值和最大值以及每个 Pack 的采样直方图。
                        2. RID Locator. 由于 Packs 中的数据按照插入顺序存储，PolarDB-IMCI 依靠Locator将主键映射到列索引中相应的物理位置。在PolarDB-IMCI中，每一行都根据其插入顺序分配一个递增且唯一的Row-ID (RID)。然后，RID Locator记录键值对的映射（即 <Primary Key, RID> ）
                        3. two-layer LSM tree.
                    2. 为了加速分析查询，PolarDB-IMCI支持在RO节点的行存储上构建in-memory列索引。列索引按插入顺序存储数据并执行out-place 写入以实现高效更新。插入顺序是指列索引中的一行可以通过其RID而不是其主键 (PK) 快速定位。为了支持基于PK的点查找，PolarDB-IMCI实现了用于PK-RID映射的RID locator（即两层LSM树）。
                    3. PolarDB常规的基于行的执行引擎用于服务OLTP查询，而新的基于列的批处理模式执行引擎则用于高效运行分析查询。批处理模式执行引擎利用列式数据库处理分析查询的技术，包括pipeline执行模型、并行算子和向量化表达式评估框架。
                    4. Handle Large Transactions
                        1. 如果一个事务包含过多的操作，则其事务缓冲单元可能会消耗巨大的内存。为了避免过多的内存消耗，PolarDB-IMCI对大事务进行了pre-commits ：当事务缓冲单元中的 DML 语句数量达到给定阈值时，就会pre-committed。
                    5. Plan Generation
                        1. PolarDB-IMCI不是自上而下构建面向列的执行计划，而是将其从面向行的执行计划转变为面向列的执行计划。PolarDB-IMCI使用DPhyp作为join order算法，通过随机采样的方式搜集统计信息。
                            1. Interesting
                        2. PolarDB-IMCI使用DPhyp作为join order算法，通过随机采样的方式搜集统计信息。
                2. G#3: 资源隔离
                    1. 索引驻留在单独的RO节点上，并采用共享存储架构
                3. G#4: 高数据新鲜度的实现
                    1. 重用REDO日志来在异构引擎间做同步
                        1. 评估表明，重用REDO日志的开销明显低于使用Binlog. 使用 Binlog 的开销明显更高，因为 Binlog 会产生额外的 fsync 和更多的日志 IO。
                        2. Data freshness is guaranteed because RO 节点的replay吞吐量远高于 RW 的 OLTP 吞吐量（图 13）
                    2. commit-ahead log shipping (CALS)和2-Phase conflict-free log replay (2P-COFFER)增强了更新传播框架。
                        1. CALS 在提交之前传送事务日志；2P-COFFER高效解析REDO日志并将其应用到RO节点。
                        2. Interesting.
                        3. Two-Phase Conflict-Free Parallel Replay
                            1. PolarDB-IMCI 不会为更新传播生成额外的逻辑日志，而是复用 REDO 日志。 
                                1. REDO日志只记录行存储中物理页的变化，缺乏数据库级或表级信息
                                2. 由行存储本身而不是用户DML引起的页面更改也包含在REDO日志中，例如B+树拆分/合并和页面合并。列索引不能应用这些日志，否则可能会出现不一致的情况。
                                3. REDO日志只包含差异，不包含完整更新
                            2. 如图6所示，PolarDB-IMCI通过两个重放阶段解决了这些挑战。
                                1. Phase#1 是将 REDO 日志replay到 RO 中行存储的in-memory副本。在这个阶段，PolarDB-IMCI捕获完整的信息，将REDO日志解析为逻辑DML语句。
                                2. Phase#2 是将 DML 语句replay到列索引。
                            2. replay的性能对于我们的系统至关重要，为了实现高性能，相关文献中提出了几种并行重放机制。这些工作要么在冲突处理辅助工具（例如锁或依赖图）或乐观控制的帮助下，以会话粒度或事务粒度进行并行重播。与这些作品不同的是，PolarDB-IMCI提出了一种新的重放方法2P-COFFER，使并行重放的两个阶段都无冲突。在2P-COFFER中，Phase#1是页粒度的，而Phase#2是行粒度的，以实现不同页/行的并发修改。修改同一页/行但属于不同事务的日志entry被视为相关日志，应按顺序replay。使用 2P-COFFER，RO 节点的replay吞吐量远高于 RW 的 OLTP 吞吐量（图 13）。
                                1. Good.
                4. G#1: Transparent Query Execution. 
                    1. 为了在单个数据库中服务混合工作负载，不应该要求数据库用户了解数据库的工作逻辑，也不应该手动识别查询类型
                    2. 新的查询路由机制，可以透明地调度查询
                        1. "另一种类型的 HTAP 数据库利用replication技术来维护多个实例。因此，TP和AP查询可以路由到不同的实例，以实现高效的性能隔离。"
                        2. PolarDB - 查询可以通过基于代价的路由协议在不同的节点和不同的执行引擎上执行。routing process对应用程序和用户完全透明，并具有两级策略：节点间路由和节点内路由。节点间路由通过proxy层实现读/写流拆分（带负载均衡），而节点内路由则通过优化器提供数据access path和执行引擎（基于行或基于列）的动态选择。
                5. G#5: Excellent Resource Elasticity
                    1. 列式索引的checkpoint机制被无缝内置到PolarDB原有的存储引擎中。因此，可以通过使用共享存储上的checkpoint快速拉起 RO 节点来实现快速横向扩展能力
            2. Background
                1. TP与AP之间数据同步的做法主要有：
                    1. SAP HANA 最近的一项工作提出了ATR（Asynchronous Table Replication），用于主实例和副本之间的数据同步
                    2. Google F1 Lightning 使用CDC，通过 BigTable shuffling数据
                    3. TiDB使用 Raft连接行存储引擎（TiKV）和列存储引擎（TiFlash）
                    4. IBM DB2 Analytics Accelerator (IDAA)通过集成同步维护基于行的表数据的副本，以支持增量更新
                    5. 新版本的 Oracle Dual支持将只读工作负载offloading到同构实例，并通过 REDO 日志同步数据。
                    6. ByteHTAP使用disaggregated存储，通过Binlog 同步异构引擎（用于 OLTP 的 ByteNDB 和用于 OLAP 的 Apache Flink）
                    7. Wildfire是一个与 Spark 兼容的数据库，还利用disaggregated存储进行数据同步。 
                    8. "与这些工作不同的是，PolarDB-IMCI直接复用REDO日志进行异构数据复制。据我们所知，PolarDB-IMCI是第一个使用物理日志来高效同步异构存储的工业数据库。"

20. ROLEX: A Scalable RDMA-oriented Learned Key-Value Store for Disaggregated Memory Systems    [2023, 7 refs, FAST23, Best paper award]
    https://www.usenix.org/conference/fast23/presentation/li-pengfei
    https://github.com/iotlpf/ROLEX
    1. Very good. PLR learned index, 2~4 orders of magnitudes smaller than B+tree, that can full index cached at client-side (compute node).
       Maintains (partial) sorting, allows asynchronized retrain withotu interruption, supports high write ingestion speed with SLT.
       Outperforms contemporary indexes either B+tree based or learned index based, as much as ~2.2x in a r/w mixed workload.
       The inode index structure in Distributed File System may find use.
        1. Following Orion/Octopus, to XStore, FORD, to ROLEX, Citron, we can look forward the entire database can be built with one-sided RDMA on mem/PMEM nodes in a disaggregated way. The index is large and distributed to nodes at all clusters.
    2. Highlights
        1. Background
            1. Disaggregated memory
                1. In-memory KV store that supports range query and point query. Index is distributed across multipe nodes.
                   If using B+tree, a lookup may need multiple RDMA rounds to each node. Think about Distributed Filesystem inodes.
                2. Memory nodes and compute nodes. Memory nodes have limited computation resource, but with FPGA or ARM chips.
                3. One-sided RDMA. Use RDMA FAA and CAS to support one-sided atomic operations. However, the max atomic unit is 8-byte.
                   The 8-byte poses limitation to the entry size and index size that need to be atomically operated.
                   But we can implement 1-bit lock to allow larger scope synchronization.
            2. Learned index
                1. PLR - Piece-wise Linear regression model. It first requests keys to be sorted. Then storage postition can be predicted with a linear model + accepted error range ε. Pattern can shift, then the total key space is cut into segments, where each piece uses a line linear.
                2. Compared to B+tree, Learned indexes can achieve 2~4 orders of magnitude memory saving.
                    1. While B+tree usually caches top nodes in compute node, Learned index allows caching all index into. Thus, a lookup can be done with one round of one-sided RDMA.
                        1. Good, this is the paradigm shift.
        2. ROLEX
            1. index structure
                1. A piece in PLR maps to a "Leaf", i.e., Leaf Region, as a consecutive range of keys, sorted.
                   Data movement is restricted with in a Leaf. A Leaf allows δ width of keys. PLR's resolution is Leaf.
                   δ is the extended error acceptance range of PLR's piece. In this way, updates won't make a stale PLR model miss to find data.

                2. Keep inserting keys into the Leaf, it may overflow, then the paper introduced Synonym-leaf.
                   It's extra regions linked to Leaf to absorb overflow data. So that a stale PLR model can still serve.
                3. Upper models: A PLR model can be too finer grain, then an upper level PLR can be trained. Layer and layer up.
                    1. like PGM-index [14]
                    2. All are fully cached at compute node
                4. Leaf Table (LT) and Synonym Leaf Table (SLT) to track Leafs
                    1. Retrain won't change Leaf, nor data movement or resorting. The PLR model and LT/SLT are separated.
            2. Retrain
                1. Generate new LT/SLT in the shadow mode, and then switch
                    1. Some concurrency guarantees need to check both old and new LT/SLT
                2. Retrain is fast, only ~300μs. Asynchronized and non-interrupting to concurrent writes
                    1. concurrent writes are offloaded to new Synonym Leafs, pending the next retrain
                3. Retrain is put to the memory node rather than compute node.
                    1. The argument is memory node's computation is limited, but still enough.
                       And this approach doesn't need to transfer huge data with compute node.
                4. Fine-grained model retraining. CirQ tracks the models pending training.
            3. Concurrency
                1. RDMA FAA and RDMA CAS on 8-byte entries.
                2. 1-bit lock field via RDMA CAS. Lock is at individual leaf level, rather than full LT
            4. Optimizations
                1. PLR's position prediction is transferred to the leaf prediction.
                2. Multiple writes into the same Leaf or Synonym Leafs can be batched to share the lock.
                3. ROLEX doesn't need to resort or move any data for retraining.
                4. RDMA Doorbell batching.
            5. Others
                1. By the narratives from the paper. ROLEX seems started from adapting XStore to disaggregated memory system, XStore-D.
                   Then it hits problem that XSTore-D cannot efficiently handle heavy modifications writes.
                    1. XStore uses a hybrid index, B+tree a memory nodes, and Learned Index cached at compute node.
                       The previous paper targets static workload with no or few modification, or use a monolithic compute+memory node.
                    2. ROLEX doesn't use B+tree at all. Fully learned index. Retrain is made fast and non-interruptive, and don't require RDMA communication between compute and memory nodes.
        3. My questions
            1. The paper keeps saying RDMA bandwidth has limitation and should avoid RDMA communication. But then why heading to the disaggregated memory architecture?
                1. Maybe XStore's monolithic architecture is the right way?
            2. PLR learned index requires keys to be maintained in sorted order. From this paper, maybe sort is only required within individual Leaf, but not cross Leaf.
               How much cost is needed for maintaining such sorting? Maybe this is why range query is a must-have brought into compare.
               Retrain then should need to use merge-sort across Leafs. Then that's why O(N) is mentioned in retrain complexity.
                1. Also, I didn't see a benchmark compare dedicated for range queries.
            3. PLR's position prediction is transferred to the leaf prediction. Is there extra cost to scan intra Leaf?
            4. After memory node done retrain, how does compute node's cached index gets updated and maintain consistency?
                1. Maybe old index is still kept, and compute node gets aware of the new index after the next read.
            5. The evaluation cluster only has 3 compute node and 3 memory nodes. How does it evaluate scalability?
                1. And, when there is a larger cluster, does it still work to cache full Leaned index in compute node?
            6. Figure 9 shows ROLEX is doing well at writes that outperforms others, but not as well in reads. Is this implicating Learned Index still has some overhead in reads? The improvements in writes should be attributed to Learned Index or something else? 

    n. related materials
        1. Correct, Fast Remote Persistence    [2019, 6 refs]
           https://arxiv.org/pdf/1909.02092.pdf
            1. RDMA FAA, CAS, 8-byte unit
                1. RDMA one-sided ATOMIC operation
            2. DDIO [12] is the feature on Intel processors that enables delivery of incoming RDMA data from the responder's RNIC directly into the L3 cache
        2. Design Guidelines for High Performance RDMA Systems    [2016, 386 refs]
           https://anujkalia.com/doc/atc16/rdma_bench_atc.pdf
            1. Doorbell batching

        3. FAST'23 ROLEX: A Scalable RDMA-oriented Learned Key-Value Store for Disaggregated Memory Systems - DielnADream
           https://zhuanlan.zhihu.com/p/613951397
        
        4. 深入解读ROLEX分离式内存系统：FAST'23 最佳论文揭秘 - 存储前沿技术评论
           https://zhuanlan.zhihu.com/p/665173526
            1. "虽然ROLEX全篇未提及CXL，但是了解CXL概念的研究人员应该能意识到分离式内存技术与CXL技术趋势的关联。"

        5. XStore: Fast RDMA-based Ordered Key-Value Store using Remote Learned Cache    [2020, 56 refs, OSDI 20]
           https://www.usenix.org/conference/osdi20/presentation/wei
            0. ROLEX is motivated by trying to apply XStore to disaggregated memory with async retrain.
            1. Good. The idea of client side to cache a learned index.
            2. Highlights
                1. Problems
                    1. Client needs multiple one-sided RDMA round trips are needed to traversal a big B+tree index
                2. XStore solution
                    1. Cache learned index at Client. Learned index takes 2~4 orders or magnitude less memory. 1 RTT is needed.
                        1. second problem: learned index assumes a sorted array. How to handle dynamic workload
                            1. solution: Translation table (TT) that makes keys logically sorted. Though B+tree insertion won't physically maintain keys sorted.
                    2. server centric update, since one-sided RDMA semantics are too simple
                        1. In compare ROLEX achieved compute node side index update
                    3. Model retraining at server side in background
                        1. two-layer RMI to organize the models. Fine-grained model retraining.
                        2. Stale model still can correctly find most keys, given logical address in TT didn't change
                        3. XMODEL uses a linear multi-variate regression model at level 0 (top-model) and simple linear regression models at level 1 (sub-model)
                        4. Model & TT retraining happens at Server. Client retrieves models and TT on-demand
                3. My questions
                    1. Can TT be integrated into the learned index model, so that the model doesn't require sorted keys?

        6. FORD: Fast One-sided RDMA-based Distributed Transactions for Disaggregated Persistent Memory    [2022, 29 refs, FAST22]
           https://www.usenix.org/conference/fast22/presentation/zhang-ming
            0. Same authors Yu Hua, Pengfei Zuo, Same school with ROLEX
            1. One-sided RDMA for distributed transaction on remote PMEM pool, with optimizations. Locking is needed.
            2. Highlights
                1. Problems to solve
                    1. Disaggregated memory, PMEM. Transaction needs to reduce one-sided RDMA round trips.
                        1. Too many RTTs: Execution, locking, validation, commit backup, commit primary each * replica count.
                    2. PEM pool has weak computation resources. Compute nodes have small RDMA caches.
                    3. Write consistency to the remote PMEM
                2. FORD solutions
                    1. Hitchhiked locking
                        1. Locking is attached to read requests, to save RTTs.
                        2. RDMA doorbell mechansim to batch the RDMA CAS followed by RDMA read in one request
                    2. Coalescent commit
                        1. In-place update. Parallel undo logging in execution phase, wait logging asynchronously.
                        2. Prevent reading partial updates, but release locks after commit.
                    3. Backup-enabled read
                        1. Allow backups to serve read-only (RO) requests. Correctness by version checks.
                    4. Selective remote flush
                        1. Only issue remote flushes to backups after the final write. RDMA supports such one-sided flash operation
                            1. My questions
                                1. think about Group Commit or Group Flush
                        2. "As RDMA FLUSH is currently unavailable in programming due to the needs of modifying RNIC and PCIe [48], we leverage one-sided RDMA READ-after-WRITE to flush the data in RNIC to memory like [27, 31]."

        7. Citron: Distributed Range Lock Management with One-sided RDMA    [2023, 1 refs, FAST23]
           https://www.usenix.org/conference/fast23/presentation/gao
            0. Quite a few one-sided RDMA papers from Huazhong University of Science and Technology, Shanghai Jiao Tong University, Tsinghua University, this year
            1. Lock management with Segment tree. Access and managing lock with one-sided RDMA. RDMA Ext-CAS, Ext-FAA.
               Evaluated with 3 clients + 1 server. Citron vs one-sided RDMA: Citron is better when more clients.
            2. Highlights
                1. Problems to solve - DRLM (Distributed Range Lock Management)
                    1. CPU solutions use too much CPU
                        1. E.g., Marple tree in Linux
                    2. Oversized lock
                        1. Throughput-optimal vs Latency-optimal
                            1. Precise mapping is well for throughput, but can lock O(logN) nodes in worst case
                               Lock only one node is fast, but can generate false conflicts
                2. Citron solution
                    1. Segment tree
                        1. Throughput-optimal vs Latency-optimal
                            1. Use k=2 lock 2 nodes. which reduces ~96% false conflicts than k=1
                        2. Selecting nodes - knapsack algorithm
                            1. Should I split here?
                                1. Weight: # children nodes to lock - 1
                                   Value: Preciseness improvement
                        3. Node X conflicts only with ancestors and descendants
                            1. Lock the node X -> notify ancestors/descendants -> detect
                                1. Citron simplifies lock conflict resolution into the communication between ancestor and descendant nodes on the tree
                        4. Others
                            1. fan-out degree is four
                            2. leaf nodes represent ranges of size 64, not the 1 in the orthodox definition
                            3. Starvation avoidance
                            4. Notify ancestors, wait for descendants: meet-in-the-middle (MITM)
                            5. Scale up/down the lock tree
                    2. RDMA extended atomics
                        1. Ext-CAS, Ext-FAA
                        2. occupied flag, head, rear, d_head, d_rear
                        3. Leaf node: bitmap
                3. My questions
                    1. But the CPU consumption is moved to Client side?

21. CJFS: Concurrent Journaling for Better Scalability    [2023, 0 refs, FAST23]
    https://www.usenix.org/conference/fast23/presentation/oh
    1. Interesting. How to commit filesystem journal transactions in parallel, even they are on the same CPU core.
       The solution is, dual-thread (upper half vs bottom half), multi-versioning snapshot (shadow paging), try_lock (opportunistic coalescing), and group commit/flush.
       The original motivation should be why BarrierFS performs even worse than EXT4 on varmail_shared workload. And also borrowed ideas from XFS.
    2. Highlights
        1. Problems to solve
            1. Commit transactions in parallel, even they are to the same region or on the same CPU core
                1. See section 3.3 analysis, and section 5 discussion. They are well summaries.
        2. CJFS
            1. Dual Thread Journaling
                1. A transaction is separated into two parts
                    1. host side: Lock up, Prepare DMA
                       storage side: DMA transfer, flush
                2. Previously, transactions are serial. They cannot overlap.
                   Now, host-side and storage-side can overlap.
                    1. Pipelined commit with order-preserving block device
            2. Multi-version Shadow Paging
                1. Previously, two transactions are serial, because they have overlapping write set.
                   Now, in the write set, non-overlapping keys are write in parallel. overlapping keys can write one by one with version tagged.
                   At transaction level, their writing are overlapping
            3. Opportunistic Coalescing
                1. Previously, when Tx1 is DMA transfer and flushing, Tx2 has to wait.
                   Now, Tx2 can coalescing itself into Tx1's DMA & flushing.
                2. try_lock. check conflict, then preempt or avoid get into the LOCKED state.
            4. and Compound Flush
                1. Now, Tx's host side and storage side each have to be serial, though the two can overlap
                   Next, Host side and DMA transfer each is serial, the two can overlap.
                   The Flush is moved to the last, and merged all Tx in group into one Flush.
        3. Evaluation
            1. CJFS vs BarrierFS vs EXT4
            2. Usecase: Varmail 40 threads. high queue depth as transactions are transferred in parallel
        4. Others
            1. Table 1: Categories of existing scalable filesystems
                1. Good summary.
            2. CJFS transaction lock-up is preemptive. It checks if there is conflict, transaction can be unlocked.
        5. My questions
            1. Log can be striped. App needs a sequence/timestamp/LSN, but it can be pure logical.
                Transactions non-conflicting don't need to wait for each other. They can write log in parallel. Their ordering can be logical.
                Unlike database transaction, filesystem metadata journaling transactions don't even need the explicit read/commit timestamp. Then inode locking is sufficient, no need for sequencer service.

            2. Concurrent writing can be allowed by multi-version. It maps to shadow paging in this paper.
                Tx1 read and Tx2 read can go parallel, rather than wait on a locked page. It works like reading snapshots. It maps to Opportunistic Transaction Coalescing in this paper.
                EXT4 filesystem doesn't require to ensure durability when transaction committed. So after Tx1 committed its writes to persistence shuttle bus, Tx2 can immediately start, even Tx1's persistence is still on-going. It maps to Dual Thread Journaling in this paper.
                Writes to disk can be batched, i.e., group commit or group write, to reduce the number of fsync() calls. It maps to Compound Flush in this paper.

            3. So, the key take away from this paper is. Instead of building a single serial log, we can allow non-conflicting transactions to read/write in parallel. MVCC helps allow concurrent Txs.
                Underlyingly, logs can also be partitioned to improve throughput. Like a few single serial logs are grouped together to become one high-throughput partitioned log.
                Besides, filesystem can build per-core or per-inode journaling. and In each core, further applies the optimization in this paper.
                There is another multi-threaded approach, that it cuts journal commit into multiple stages, and organize them into a multi-staged pipeline.

            4. This paper's prior work is BarrierFS. Reading section 3.3, the initial motivation should be how BarrierFS performs worse than EXT4 on varmail-shared. BarrierFS commits transactions in parallel, but they still become serial at flush. BarrierFS transactions commonly conflict on inode block and bitmap, while shadow paging is not effective. BarrierFS puts transaction at LOCKED state too early, and should have leveraged coalescing. Section 5 Discussion has more compares of CJFS vs BarrierFS. Another thing is this paper CJFS seems have borrowed quite a few from XFS. 

        n. related materials
            1. BarrierFS: Barrier-Enabled IO Stack for Flash Storage    [2018, 62 refs, FAST18 best paper award]
               https://www.usenix.org/conference/fast18/presentation/won
                0. Same author Youjip Won, Joontaek Oh.

            2. CORFU: A Shared Log Design for Flash Clusters
               https://www.cs.yale.edu/homes/mahesh/papers/corfumain-final.pdf
                1. compared to the parent paper, we can also shard the logs.
                   The serial log is striped to flash devices. stripe mapping is static.
                   A sequencer is introduced to optionally reduce the contention in acquiring the log tail.

            3. ScaleFS: Scaling a file system to many cores using an operation log    [2017, 66 refs]
               https://people.csail.mit.edu/nickolai/papers/bhat-scalefs.pdf
                0. As mentioned in the parent paper, per-core journaling
                1. sv6 [12] in-memory FS + xv6 [12] on-disk FS. In-memory per-core logs -> merge & order by timestamp -> fsync to disk.
                   commutative filesystem operations should run conflict free
                2. Highlights
                    1. Decouple the in-memory filesystem from the on-disk filesystem
                        1. Like CJFS dual thread. And Linux FS usually doesn't write commit durability unless fsync().
                        2. Both NOVA [42] and ScaleFS use per-core logs, but ScaleFS separates in-memory filesystem
                    2. In-memory filesystem is built with OpLog [5]
                        1. OpLog consists of
                            1) per-core logs
                            2) when fsync is called, ScaleFS merges per-core logs with timestamp and apply them to disk
                            3) ScaleFS is designed that no interaction is necessary between two cores 
                        2. mnode in memory vs inode on disk
                    3. Scalable Commutativity Rule [10] - The Scalable Commutativity Rule: Designing Scalable Software for Multicore Processors
                        1. ScaleFS uses sv6 [10] to build in-memory filesystem. sv[6] has special parallelism design that makes commutative operations conflict free (see Figure 8)
                        2. Disk filesystem is built with xv6 [12]. So ScaleFS is sv6 + xv6?
                    4. Handling non-local operations - rename
                        1. Operations take lock on inode
                           Use CPU clock RDTSCP to timestamp log operations
                           ALl directory modifications in in-memory FS must be linearizable
                           fsync orders the operations by their timestamp, in the same order that they were applied to MemFS. 
                n. Related materials
                    1. Scaling a file system to many cores using an operation log
                       https://nan01ab.github.io/2018/03/ScaleFS.html

                    2. The Scalable Commutativity Rule: Designing Scalable Software for Multicore Processors    [2015, 247 refs]
                       https://web.eecs.umich.edu/~ryanph/eecs582/fall23/readings/commutativity.pdf
                       https://dl.acm.org/doi/pdf/10.1145/3068914
                        1. scalable commutativity rule - whenever interface operations commute, they can be implemented in a way that scales, i.e., conflict-free.
                            1. Good, this is actually simple and intuitive. Even broader than the concept "symmetric multi-replica" 对称多副本
```