---
layout: post
title: "Recent Articles Reading Notes: "
tagline : "Recent Articles Reading Notes: "
description: "Recent Articles Reading Notes: "
category: "technology"
tags: [cloud, storage, paper]
---
{% include JB/setup %}


CockroachDB SSI, C++ coroutine, 文件/存储系统调研

```
1. 分布式文件系统调研（详细版）- 贺大伟
   https://zhuanlan.zhihu.com/p/493647334
    1. typical distributed filesystems
        1. GFS
        2. HDFS
        3. Openstack Swift
        4. MinIO
        5. Ceph
        6. TFS
        7. Lustre
        8. MooseFS
        9. MogileFS
        10. FastDFS
        11. GlusterFS
        12. GridFS
        13. JuiceFS
        14. ChubaoFS
        15. Ozone
        16. PolarFS

2. Cloudy with High Chance of DBMS: A 10-year Prediction for Enterprise-Grade ML - 约修亚
   https://zhuanlan.zhihu.com/p/446414853
   https://arxiv.org/pdf/1909.00084
    1. A visionary paper. Logged in paper section

3. Databases in 2022: A Year in Review - Andy Pavlo
   https://ottertune.com/blog/2022-databases-retrospective/
    1. New Database Systems
        1. Google AlloyDB
        2. Snowflake Unistore
        3. MySQL Heatwave
        4. Velox
        5. InfluxDB IOx

4. 2022 年数据库发展总结 - wubx - 吴炳锡 @ Databend 联合创始人& 架构师 
   https://zhuanlan.zhihu.com/p/596852461
5. Vectorization vs. Compilation in Query Execution - henry liang
   https://zhuanlan.zhihu.com/p/393961205

6. RocksDB merge operator
    1. rocksdb_wiki/Merge-Operator-Implementation.md
       https://github.com/EighteenZi/rocksdb_wiki/blob/master/Merge-Operator-Implementation.md
    2. RocksDB merge operators - jiawei
       https://jiaweichiu.github.io/articles/2018-12/rocksdb-merge-operators

1. CockroachDB: What write skew looks like by Justin Jaffray
   https://www.cockroachlabs.com/blog/what-write-skew-looks-like/
    1. very good article that explained how SSI works and Write Skew

2. C++无锁(lock free)数据结构与有锁数据结构相比，速度，性能等有何区别?多线程中如何选择？ - 郭忠明
    1. good. reveals many industrial design and implementation details.
    2. Wait free ring buffer - no CAS

3. 数学家破解了约会网站中男女匹配算法的故事 - 十一点半
   https://www.zhihu.com/question/20150963/answer/2871700210?utm_id=0
    1. ELO algorithm

4. Heap vs Priority queue
    1. Heap: https://en.wikipedia.org/wiki/Heap_(data_structure)
    2. Heap vs Priority queue: https://www.hackerearth.com/practice/data-structures/trees/heapspriority-queues/tutorial/
    3. Heap extract max
        1. OK, it takes O(logN) time complexity. So why not just use a linked list per priority to build priority queue?
           Linked list implementation is simpler, thus more robust to adding new features, e.g. get job count per priority, take a task from specific priority for anti-starvation
    4. Timer Wheel algorithm
       https://blog.csdn.net/tianyaleixiaowu/article/details/121401246
        1. OK .. it's just a bucket sort, with multi layers of buckets for different precision

5. On Finding Non-Intersecting Paths in Grids and Its Applications
    1. Recursive Backtracking
       https://brilliant.org/wiki/recursive-backtracking/
    
    2. ChatGPT's algorithm answer
        1. OK .. it's actually incorrect .. ChatGPT explains it as if it's really doing the right thing
    
   3. The Problem: "there is an infinite grid, a person starts at (0,0). he can move N steps (up, down, left, right), each step requires x >= 0 and y >= 0, and he cannot go to a position he already went to. He has to go exactly N steps. Please return the number of possible paths that this person could go, N's range is from 1 to 25, and the algorithm complexity should be within the level of O(10^7)"
        1. DP solution, N=22 is the max. Still too slow
           https://gist.github.com/accelazh/a22cf536158d1090b3c0383d83104f2e
    
    4. Approximation Algorithm for non-intersecting paths in a grid
       https://stackoverflow.com/questions/31080969/approximation-algorithm-for-non-intersecting-paths-in-a-grid

    5. Unique paths in a Grid with Obstacles
       https://www.geeksforgeeks.org/unique-paths-in-a-grid-with-obstacles/
    
    6. Count all Hamiltonian paths in a given directed graph
       https://www.geeksforgeeks.org/count-all-hamiltonian-paths-in-a-given-directed-graph/

    7. 一瓜算法小册: Ford-Fulkerson 最大流求解方法
       https://www.desgard.com/algo/docs/part4/ch03/2-ford-fulkerson/

6. Asymmetric Transfer: understanding C++ coroutines
   https://lewissbaker.github.io/2017/09/25/coroutine-theory
   https://lewissbaker.github.io/2017/11/17/understanding-operator-co-await
   https://lewissbaker.github.io/2018/09/05/understanding-the-promise-type
   1. good articles
   2. highlights
    1. activation frame = stack frame (in stack) + coroutine frame (in heap)
    2. it's the "suspension point" that defines what to put in stack frame, and what to put in coroutine frame
        1. those need to be resumed after suspension point, are put into coroutine frame
        2. so, even async await is frequently used in imperative for loop when no IO involved, coroutine in theory should have no overhead
    3. in physical thread execution view, suspension point directly returns a handle, i.e. future object
       from programming view, execution flow async resumes from suspension point 
```

Ceph snapshot mechanism

```
1. Ceph Snapshots: Diving into Deep Waters
   https://events.static.linuxfound.org/sites/events/files/slides/2017-03-23%20Vault%20Snapshots.pdf
    1. Ceph snapshot is per-object, backed by OSD transaction, COW. RBD snapshot, CephFS snapshot are implemented by object snapshot
    2. My questions
        1. We know an RBD image is stripped to many objects to different OSDs. If snapshot is per-object, how to ensure the RBD images takes a consistent snapshot?

2. Ceph SnapContext
   https://docs.ceph.com/en/mimic/dev/osd_internals/snaps/
3. Ceph快照详解 - thierryzhou
   https://zhuanlan.zhihu.com/p/588587416
4. Ceph consistent snapshot
    1. Working with RBD snapshots (Ceph: Designing and Implementing Scalable Storage Systems - Published 2019)
       https://learning.oreilly.com/library/view/ceph-designing-and/9781788295413/1ee61bb3-69a5-4a46-940f-7cceab523e2f.xhtml
        1. "If you take a snapshot of an RBD image while I/O is in progress to the image the snapshot may be inconsistent."
           "When taking snapshots it is recommended to cease I/O from the application to the image before taking the snapshot"
        2. App to `fsfreeze` command to filesystem 
    2. Ceph (RBD) group snapshot support #3143
       https://github.com/OpenNebula/one/issues/3143
    3. Ceph wiki - Consistency Groups
       https://tracker.ceph.com/projects/ceph/wiki/Consistency_groups
        1. setup mirroring of multiple volumes in the same consistency group
    4. OpenShift - Persistent Volume Snapshots
       https://docs.openshift.com/container-platform/3.11/install_config/persistent_storage/persistent_volume_snapshots.html
        1. "It is the user’s responsibility to ensure data consistency (stop the pod/application, flush caches, freeze the file system, and so on)."	
```

iSCSI, iSER, NVMe-oF

```
1. Comparing iSCSI, iSER, and NVMe over Fabrics (NVMe-oF): Ecosystem, Interoperability, Performance, and Use Cases
   https://sniansfblog.org/comparing-iscsi-iser-and-nvme-over-fabrics-nvme-of-ecosystem-interoperability-performance-and-use-cases/
2. 一文浅析NVMe over Fabric技术发展简史
   https://blog.csdn.net/BtB5e6Nsu1g511Eg5XEg/article/details/85811072
3. iSCSI - is it the future of Cloud Storage or doomed by NVMe-oF
   https://www.snia.org/sites/default/files/news/iSCSI-Future-Cloud-Storage-Doomed-NVMe-oF.pdf
4. lightbits: NVMe/TCP 对比 iSCSI 
   https://cdn2.hubspot.net/hubfs/4565714/Downloadable%20Asset_Chinese/3_NVMe%20vs%20iSCSI%20%E7%9A%84%E6%AF%94%E8%BE%83.pdf

3. SPDK NVMF
    1. Target
       https://spdk.io/doc/nvmf.html
    2. Host
       https://spdk.io/doc/nvme.html#nvme_fabrics_host
    3. https://www.snia.org/educational-library/spdk-based-user-space-nvme-over-tcp-transport-solution-2019
       SPDK based user space NVMe over TCP transport solution

4. SPDK bdev
    1. Guide
        1. https://spdk.io/doc/bdev.html
    2. 【SPDK】一、概述
       https://rootw.github.io/2018/05/SPDK-all/
       【SPDK】二、IO栈对比与线程模型
       https://rootw.github.io/2018/05/SPDK-iostack/
       【SPDK】三、IO流程代码解析
       https://rootw.github.io/2018/05/SPDK-ioanalyze/
       【SPDK】四、reactor线程
       https://rootw.github.io/2018/05/SPDK-reactors-init/
       【SPDK】五、bdev子系统
       https://rootw.github.io/2018/05/SPDK-subsys-bdev/
       【SPDK】六、vhost子系统
       https://rootw.github.io/2018/05/SPDK-subsys-vhost/
       【SPDK】七、vhost客户端连接请求处理
       https://rootw.github.io/2018/05/SPDK-vhost-msg-handle/

3. NVMe-oF private fabric / auth how-to
    1. didn't find materials
    2. https://nvmexpress.org/wp-content/uploads/NVMe-over-Fabrics-1.1-2019.10.22-Ratified.pdf
4. SPDK polling
    1. Event Framework
       https://spdk.io/doc/event.html
        1. useful, the article reveals SPDK thread model.
        2. it's a co-routine model. "polling" is a special "event" that is pushed to reactor queue in high frequency (one execution per iterator round of main event loop)
           event loop is one per core, one thread per core.
           polling replaces interruption handling. all in user space. no thread switch
```

Abase, Physalia, VMCACHE, Pangu. 

```
1. 工业界推荐系统怎么做特征？ - Sanders: 推荐特征引擎 - Feature Store
   https://www.zhihu.com/question/419906651/answer/2491472559?utm_id=0
2. 金雪锋: AI编译器的概览、挑战和实践
   https://zhuanlan.zhihu.com/p/508345356?utm_id=0
3. QianLing: 有利用 GPU 的数据库吗？
   https://www.zhihu.com/question/547529833?utm_id=0
4. DataFunTalk: 知识图谱技术体系总览
   https://zhuanlan.zhihu.com/p/613855167?utm_id=0
5. TPC-C 的前生今世
   https://zhuanlan.zhihu.com/p/618943360?utm_id=0
6. 300美元复刻ChatGPT九成功力，GPT-4亲自监考，130亿参数开源模型「小羊驼」来了
   https://zhuanlan.zhihu.com/p/618699807?utm_id=0

7. Presto：Meta十年数据分析之旅
   https://zhuanlan.zhihu.com/p/620364854?utm_id=0
    1. Shared Foundations: Modernizing Meta’s Data Lakehouse    [2023, CIDR, Facebook, 0 refs]
       https://www.cidrdb.org/cidr2023/papers/p77-chattopadhyay.pdf

8. PingCAP 前景分析 vs 达梦,Cockroach (一)
   https://zhuanlan.zhihu.com/p/620361848?utm_id=0
9. 多模数据库系统研究综述（未完成）
   https://zhuanlan.zhihu.com/p/611436611?utm_id=0
10. 微信打电话和直接打电话有什么区别吗？
    https://www.zhihu.com/question/575816676/answer/2824200541?utm_id=0
11. 总结：数据库副本复制方式对比
    https://zhuanlan.zhihu.com/p/611248487?utm_id=0
12. 思维链（Chain-of-thoughts）作为提示
    https://zhuanlan.zhihu.com/p/493533589?utm_id=0

13. Facebook Velox 运行机制全面剖析
    https://zhuanlan.zhihu.com/p/614918289?utm_id=0
14. OpenAI 背后的 Kubernetes 发展历程（翻译
    https://mp.weixin.qq.com/s/VXHZkgjni-ve_eBJ0pK-FA

15. 字节跳动极高可用 KV 存储系统详解
    https://zhuanlan.zhihu.com/p/614227806?utm_id=0
    1. "极"高可用：Multi-master active-active mode (无主架构), conflict resolution by Last Write Win + CRDT. Like Dynamo. Interesting
    2. highlights
        1. scope and impact
            1. Abase - 大容量缓存、持久化KV、Redis兼容、跨地区同步
               目前 Abase 在字节跳动已经部署超过 5 万台服务器，QPS 在百亿级别
               Abase 支持的业务数超过 5000，基本覆盖了字节的全部产品线，有超过百 P 级别的数据量
        2. Key designs
            1. Abase 2.0 是一套多写架构，可以做到极致高可用。多写的架构没有了主从架构的切换主节点的时间，也没有秒级别的主从切换不可用问题；多写架构也从架构层面屏蔽了慢节点，规避了慢节点问题。
                1. Abase 2.0 解决多写架构的写冲突方面，对于 KV 结构支持 last write win 这种通过时间戳的方式解决冲突
                   对于一些复杂数据结构，如 string 的 incr、append 或者哈希结构，支持 CRDT 的解决方案
                   此外 Abase 2.0 还会做快速的数据一致
            2. Abase 2.0 没有用纯异步的编程框架，我们用协程的方式让所有请求都在单线程内完成，让请求尽量 RunToComplete，没有线程切换的开销和代价
            3. Abase 2.0 原生支持多租户
                1. 虽然 SSD 的随机 IO 性能很好，但如果 IO 模式过于离散会导致性能变差，因此最好保证有单一的写入流。多租户会把不同用户的写入做聚合
            4. Abase 2.0 原生支持异地多活架构
        3. Others
            1. "但在数据恢复时是否需要等所有数据同步完成后才能接受写请求呢？针对这个问题，我们对部分场景做了优化，让 Abase 允许乱序提交，但只有在主从落后太多时才允许乱序提交。这样我们就保证了整体一致性的算法效率较高的同时保证了可用性。"
            2. "我们第一期实现的方案是把时间戳直接拼在 Key 后作为编码，数据存储到 RocksDB 中。这个实现带来的问题是用户需要查某个 Key 时，RocksDB 中只能通过 Scan 操作查询数据，而 Scan 操作比点查开销大、性能差。"
                1. "我们的优化方案是定期地处理数据冲突和打平，在正常网络状况下秒级别即可同步所有数据。某个时间戳之前的数据已经完全一致，即可把多版本进行合并。"
                2. "Abase 把引擎分为两层，把多版本数据合并后唯一的单版本数据存储进 KV 引擎。目前 KV 引擎支持 RocksDB 和字节的 RocksDB 优化版和哈希引擎。"
                   "未打平的数据存储在 Log 内，而 Log 不支持查询，Abase 就在内存中建了索引，在内存中指向 Log 支持查询。"
    n. related materials
        1. Abase2：字节跳动新一代高可用 NoSQL 数据库
           https://mp.weixin.qq.com/s/UaiL8goZ_u0Jo9dDNnBP0w
            1. CRDT
                1. "对于幂等类命令如 Set，LWW 能简单有效地解决数据冲突问题，但 Redis String 还需要考虑 Append, Incrby 等非幂等操作的兼容，并且，其它例如 Hash, ZSet 等数据结构则更为复杂。于是，我们引入了 CRDT 支持，实现了 Redis 常见数据结构的 CRDT，包括 String/Hash/Zset/List，并且保持语义完全兼容 Redis。"
            2. Redis CRDT - Conflict-Free Replicated Data Types (CRDTs)
               https://redis.com/blog/diving-into-crdts/
                1. Good. Employing CRDT to resolve conflict is a major different from Cassandra/Dynamo's Quorum write/read or Last Write Wins
                2. Example of CRDT - merge two sets. CRDTs perform replication as commutative operations
                3. "The locking mechanism used in strong consistency is inconsistent with the need for real-time performance. This is where eventual consistency and CRDTs come into play."
            3. 负载均衡流程的概要主要分为 3 个步骤：
                1. 根据近期的 QPS 与磁盘空间使用率的最大值，为每个 Core 构建二维负载向量；
                   计算全局最优二维负载向量，即资源池中所有 Core 负载向量在两个维度上的平均值；
                   将高负载 Core 上的 Replica 调度到低负载 Core 上，使高、低负载的 Core 在执行 Replica 调度后，Core 的负载向量与最优负载向量距离变小。
            4. Others
                1. 图 10: 边缘-中心机房部署
                    1. Edge vs Central IDC
                2. Squirrel 智能迁移
                3. Cellar 快慢列队

16. 万亿级KV存储架构与实践
    https://zhuanlan.zhihu.com/p/618780794?utm_id=0
    1. Redis => 自研Squirrel
       阿里 Tair => 自研Cellar

17. 百度：万亿级对象存储的元数据系统架构设计和实践
    https://zhuanlan.zhihu.com/p/607801586?utm_id=0
    1. 下面讨论如何解决规模问题，以实现单桶万亿级对象数。
        1. 数据引擎基于 RocksDB 的优化版本，日志 I/O 和数据 I/O 做了分离 ... 同时也做了数据压缩和编码优化
        2. 使用复合分区，先 hash 分区，再 range 分区。具体做法就是在元数据的编码最前面增加一位的 hash 产生的 shardKey
        3. 心跳合并，Master 管理的单位是分片，满载时单机分片数接近 1W
    2. 下面再讨论性能方面如何实现单桶百万 QPS, 优化后的单机引擎支持高达 10W QPS 的吞吐
        1. 日志的合并，把 Raft log 和 RocksDB 的日志合并成一路，节省了 I/O
        2. 支持了批量操作，批量 Commit Raft log 和存储引擎
        3. 针对热点问题，我们设计了多维度探测机制，包括单机 CPU 负载、API 延迟长尾、单分片的请求数等
        4. 让从节点提供读服务，提供两种模式，默认强一致读，从节点要去主节点通信一次判断从节点的 applied index 是否跟主节点一致 ... 另一种模式是高频访问降级读模式
        5. 我们也针对事务操作进行了优化。
            1. 对象存储要支持数据的生命周期，所以要支持按时间维度的索引。这个时候如果每次写入都要写数据表、索引表，每次都要 2PC，效率非常低。
            2. 对象存储这个场景下并不要求索引和数据完全一致，所以做了特殊的优化，写数据表成功就返回，索引表采用异步批量的方式写入

18. ARM云服务器技术分析
    https://zhuanlan.zhihu.com/p/613762397?utm_id=0
    1. 亚马逊是第一家将基于 Arm 的处理器推向市场的公司，尽管它只向自己出售处理器
       AWS 于 2018 年底推出了其内部设计的基于 Arm 的处理器 Graviton，此后该公司几乎每年都发布新一代 Graviton

19. TPC-C 的前生今世
    https://zhuanlan.zhihu.com/p/618943360?utm_id=0
    1. 2019 年 10 月 1 日，蚂蚁的 OceanBase 以 60,880,800 TPM 夺得了 TPC-C 的榜首
       2020 年 5 月 18 日，OceanBase 又以 707,351,007 TPM 的性能将性能榜首提高了 11.6 倍
20. TPCH 深入剖析 - part1 Hidden Messages and Lessons Learned from an Influential Benchmark
    https://zhuanlan.zhihu.com/p/369455226?utm_id=0
    1. TPC-H可以说是世界上最为流行的OLAP workload的benchmark程序，无论你看什么样的论文或技术文章，只要是和query processing相关的，大多会在evaluation时使用TPC-H作为评估工具
    2. ChatGPT: TPC-C vs TPC-H
        "TPC-H and TPC-C are both benchmark standards developed by the Transaction Processing Performance Council (TPC), but they target different types of workloads and have different goals.

        TPC-C (Transaction Processing Performance Council Benchmark C) is an online transaction processing (OLTP) benchmark. It is designed to evaluate the performance of database systems under a heavy load of concurrent transactions, simulating a real-world e-commerce or retail environment. TPC-C measures the number of transactions per minute that a system can handle (expressed as tpmC). The benchmark focuses on a mix of read and write operations, testing the system's ability to handle high concurrency, maintain consistency, and provide low-latency responses.

        TPC-H (Transaction Processing Performance Council Benchmark H) is a decision support benchmark. It focuses on evaluating the performance of database systems in handling complex ad-hoc queries, often used for business intelligence and analytics purposes. TPC-H simulates a scenario where users submit a variety of queries to gain insights from large volumes of data. The benchmark measures the system's performance in executing these queries and returning the results (expressed as the TPC-H Composite Query-per-Hour Performance Metric, or QphH). TPC-H tests the system's ability to handle complex read-heavy operations, optimize query execution, and manage large amounts of data.

        In summary, TPC-C and TPC-H benchmarks serve different purposes: TPC-C evaluates the performance of database systems for OLTP workloads, focusing on concurrent transaction processing, while TPC-H evaluates the performance of database systems for decision support and analytics workloads, focusing on complex query processing over large datasets."

21. 飞猪旅行场景下的实时用户理解服务
    https://zhuanlan.zhihu.com/p/618707844?utm_id=0
22. 国产数据库存储引擎 X-Engine 的科研之路
    https://zhuanlan.zhihu.com/p/114353917?utm_id=0

23. Physalia: Millions of Tiny Databases——AWS NSDI'20 Paper 解读
    https://zhuanlan.zhihu.com/p/109891109?utm_id=0
    https://www.amazon.science/blog/amazon-ebs-addresses-the-challenge-of-the-cap-theorem-at-scale
    1. Interesting. Cell (a configuration function unit) follows EBS client to ensure staying in one network partition failure domain. Millions of Cells for different EBS client location.
    2. highlight
        1. background
            1. "2011年4月，ASW 发生了网络Partition。EBS(Elastic Block Store) 管控服务提供强一致性语义， 需要让 EC2实例（client）、各个StorageServer完成Failover，确保它们对新的primary replica达成共识，在网络Partition的时候无法完成处理。这个管控服务和对外的API共享一个数据库，在大面积failover的的时候，更多的failure需要管控服务处理更多的请求，引起雪崩，最终造成一个可用区中13%的EBS Volume不可服务。 之后，AWS EBS开始考虑如何控制爆炸半径（控制爆炸半径很重要，硬件故障、压力过载、软件bug都可能引入失败），就有了这篇Paper描述的系统。"
            2. "在大面积Failover发生时，由于大量client需要访问 管控服务，来分配新的replica，切换Primary replica，这个workload是burst型的，因此不仅需要控制爆炸半径，还需要 管控服务具备高性能、高可用、高可靠存储、强一致的特性。其他维度不难实现，关键是强一致和高可用之间的矛盾如何调和？"
            3. "Physalia，这篇Paper的主角，是AWS EBS服务的元数据管理服务，旨在 解决爆炸半径问题，并打破强一致和高可用的矛盾"
        2. Key design
            1. "一个核心的观察是：单个EC2实例只需要访问它挂载的EBS Volume的数据，不需要要看到所有的数据。虽然全局的CAP——在网络分区的情况下所有的数据对所有的client保持一致性和可用性，还是不能达到的，但是在client和它需要的数据上同时满足CAP是可以达到的。"
            2. "这篇Paper的精髓是 基础设施感知的Placement策略和细致的系统架构设计。基于对网络和供电系统拓扑的知识，把Cell被调度到离EC2实例"不近不远"的地方，大幅减少网络分区的影响。"不近不远"指的是网络拓扑上的距离："
                1. "不近"，Cell成员之间的Placement保证高可用，要容忍一些故障域，比如供电单元之类
                2. "不远"，Cell成员（至少是Majority）位置和EC2实例之间，在发生网络分区时，能够处在分区同一侧，能够继续工作！
            3. "Cell基于预先划分好的一些PlacementGroup来简化placment计算，在这篇Paper里叫Color"

24. 阿里健康供应链智能补货算法
    https://zhuanlan.zhihu.com/p/612099867?utm_id=0
    1. "库存决策：在建立了预测能力之后，就能进行上层库存决策。在预测了未来销量后，会需要对当前库存进行判断（货品数量是否够用），如果货品数量不够，则需要进货，这部分就是由“智能补货”模块决定。在货品不够的情况下，除了从供应商处进货，还能从其他仓库划拨，这种仓与仓之间的库存划拨则由“智能调拨”模块进行决策。“仓网规划”模块主要包含订仓和订配：订仓主要解决哪些货品该放入哪些仓的问题；订配主要解决仓该对哪些区域进行配送，以及配送时该用哪个快递等问题。最后的模块是“智能采购”，进货时通过分析供应商相关的询报价、审价、送货时长、滞销等一系列因素，来决定从哪些供应商进行采购。"
    2. 上图展示了智能补货算法的演进过程：
    （1）传统模型 ss：最左边展示了业内通用的传统 ss 模型，该模型主要基于安全库存。模型优点是整体框架成熟、稳定、易解释，容易直接取得结果；缺点是受限于框架，考虑因素不足。
    （2）运筹优化 OR 模型：运筹模型的优点是灵活性较高，针对性较强，即求解某个最优化问题即可；缺点是整体的建模和求解难度需要得到保证，如果要求最优解，时效性需要保证，如果追求时效而去求次优解，这样求解的稳定性也会受到影响。
    （3）深度学习/强化学习：深度学习和强化学习在补货算法场景中的尝试。该类方法的优点是能够考虑更多的因子，网络结构和深度都可调，也能学习到更多的表征；缺点则是深度学习方法相关的缺点，即模型调参、训练时长、效果稳定性等，此外在 RL 学习中 Reward 的设计也比较有挑战性。

25. 简谈论文：LeanStore: In-Memory Data Management Beyond Main Memory
    https://zhuanlan.zhihu.com/p/611563854?utm_id=0
    1. Interesting paper. Recommended in CMU 15-721. Key points at pointer swizzling and eviction policy.
    2. Highlights
        1. LeanStore 的创新主要是在 Eviction Policies （可以理解成将不常用的 tuple 淘汰到磁盘上的策略），是 Andy 比较认可的一个方案，其实现也是非常巧妙。其核心思想是想保留传统磁盘数据库的 BufferManager 方案，但是保留的同时又摒弃掉其中会造成瓶颈的技术。
            1. 所以传统数据库的 BufferManager 有哪些需要摒弃的技术？论文认为在内存数据库上会造成严重开销的是 HashTable 的使用，这也是大部分主流内存数据库抛弃 BufferManager 的主要原因
            2. 所以 LeanStore 抛弃了 HashTable ，选择了一种更加巧妙的方案来替代 - pointer swizzling
        2. 那么 LeanStore 是如何判断热数据和冷数据，并将冷数据装入磁盘的？通常来说，比较直观的方案是设计一个记录数据冷热的机制如 LRU，或者给 Tuple 加一个计数位。但 LeanStore 的想法就比较另类了，既然要简洁高效，那它就贯彻到底 —— 随机选择需要放入磁盘的 page
            1. 第一步，随机选择 N 个page，进入 cooling 状态，并将这些 page 放入一个 FIFO 队列中，这个队列实际上还是在内存中的。
               第二步，如果在 FIFO 中的 page 被访问到了，则将这个 page 视作热数据，将其变回 hot 状态。所以这个 FIFO 队列本质上可以看作是一个冷静期观察室，如果有 page 热起来了，会被马上拎出去。
               第三步，对于已经从末尾走到队列头部的 page，则可以视为冷数据了，可以将其放入磁盘。

26. 精读论文：VMCACHE: Virtual-Memory Assisted Buffer Management
    https://zhuanlan.zhihu.com/p/611616867
    0. good paper. Bring MMAP to DB buffer management, need to fix MMAP problems, but able to leverage MMAP advantages.
    1. key designs
        1. vmcache：解决了 mmap 不可控的缺点，设计出了一种更加高效可靠的 buffer 管理方案，弥补了 mmap 的诸多不足（mmap为什么不行）。
            1. OS 却有一些高效的硬件资源是 DBMS 没有办法使用的，如TLB
            2. Comparable but worse solutions to manage page lookup
                1. Hash table-based translation（DBMS）- traditional Buffer Manager
                2. Main-memory DB （DBMS）
                3. Pointer swizzling (DBMS) - LeanStore
                4. mmap（OS）
            3. vmcache 横空出世了，它基于虚拟内存，但是它在可以使用页表和 TLB 的同时，让 DBMS 决定什么时候，哪些 page 需要被 evict 或者需要从磁盘中获取，从而结合了 DBMS 和 OS 的优点。简单来说，vmcache 是一个更加可靠的 Buffer Management 部件，DBMS 可以直接在它分配的虚拟内存空间上安全地进行 page 管理。在实际数据库的应用中，vmcache 的应用远比 LeanStore 的 swizzlling 技术更加容易实现。
                1. 需要修改Linux内核。可以理解为 vmcache 在管理 page 时使用到的系统 API，分别用于实现三个基本的操作：a.分配虚拟内存空间，b.从外存中读取一个page到内存，c.以及从内存淘汰一个 page 到外存。
                2. 还有一个细节问题，vmcache 如何快速地知道每个 page 的状态？作者的做法是分配一个数组，每个数组项大小是 64bit，每个 page_id 对应一个数组项。
                3. eviction 策略。vmcache 使用的是 CLock 策略，每一次循环，都尝试将 Marked 标记为1的page写入磁盘。由于每一次循环都需要遍历状态数组，这个开销是比较大的，vmcache 使用了一个固定长度的 hash table 来存储 Marked 状态的 page_id，这样的优化可以减少遍历的开销。（这里的 hash table 同传统的 hash table 不同，这里只会在 page 被 evict 或者缺页错误的时候被使用到）。除此之外，vmcache 还做了另一个优化：一次尝试淘汰 64 个page。
            4. 除了上述类似于 BufferManager 的基本功能外，vmcache 还提供了多种 page size 的支持（4kb 的倍数）。
        2. exmap：指出了 Linux 在页表处理上的一些局限，在内核上设计了一种更加高效的虚拟内存页面管理方案，并提供了 API 供用户层使用。
            1. 作者并不满足于 vmcache 本身，因为他认为Linux的页面置换策略是有问题的，尤其是在换页比较频繁的负载下会有性能瓶颈。作者通过一个简单的实验证明了他的想法：让一个程序通过触发缺页来分配一个 page ，然后又立即 evict 这个 page。在 128 线程的情况下，它分配空间的带宽几乎同 SSD 磁盘的带宽相同，也就是说它把全部的 CPU 都花在了换页上。
                问题一：TLB shootdowns，指的是每当页表发生改变，OS 都要删除所有核心上 TLB 对应的表项，也就是说每一次页表变化都会打断所有 CPU 核心。
                问题二：所有线程在分配和释放 page 时都会在一个中心化的内存空间进行，且为了安全起见，free 时要将这个 page 的内容置为0。
            2. EXMAP：Fast virtual memory manipulation
                1. 方案一：为了解决 TLB shootdown 的问题，exmap 提出了两个解决办法
                    1. 提供batching方法一次性释放多个 page
                    2. 放弃执行 shootdown，而是在页表上为被释放了的 page 设置一个读保护位，表示这个 page 不可读
                2. 方案二：预分配 thread-local 内存池，所有的 page 从这个池子里面获取。
                3. Design details
                    1. Scalable page allocator
                    2. Interface steal polic
                    3. Lock free page table manipulation
                    4. read improvement
                        1. 如果用户想一次性从磁盘读取多个连续或者不连续的 page，Linux 只能相应地由产生多次缺页异常来实现
                        2. 所以 exmap 实现了这样的优化：只需要一次系统调用就可以读取一系列连续（vector）或者不连续的（scattered）pages，并且不需要用缺页异常来实现
                    5. multiple exmaps
                        1. exmap 预分配内存池并独立管理的特点，可以让多个 exmap 在同一台物理机上完美地独立运行
    n. related materials
        1. mmap为什么不行: Why Andy hates MMAP
           https://zhuanlan.zhihu.com/p/470109297
            1. Problems with MMAP
                1. 第一大原罪，transactional safety！我一个 dirty page 明明还没到 commit 的时候你就自动给我落盘了，这我万一要回滚呢？我原来的数据都被覆盖了啊。
                2. 第二，IO stall。在不能保证什么时候自动落盘的时候，你也不知道什么 page 已经被加载到内存里了，以及还在不在内存里。
                3. 第三，error handling。这是第一点的延续，因为不知道什么时候 page 被 evict 了，每次读的时候都要做正确性校验（e.g., check sum）。另外，如果有 corrupted page，MMAP 不会做检查。
                4. 第四，performance issus。作者发现 MMAP 的性能在高带宽存储（e.g., PCIe 5.0 NVMe）上的性能表现并不能很好地 scale
            2. So, database designed its own page management - BufferManager.
        2. Virtual-Memory Assisted Buffer Management    [2023, SIGMOD, 1 refs]
           https://www.cs.cit.tum.de/fileadmin/w00cfj/dis/_my_direct_uploads/vmcache.pdf

27. pipeline执行引擎和一些工程优化
https://zhuanlan.zhihu.com/p/614907875?utm_id=0
28. 干货 | PostgreSQL数据表文件底层结构布局分析
    https://zhuanlan.zhihu.com/p/471815579?utm_id=0
29. 性能优化-磁盘I/O篇
    https://juejin.cn/post/7031043765192097822
30. 探索Snowflake auto clustering 设计
    https://zhuanlan.zhihu.com/p/490719154?utm_id=0
    1. good
31. 【SIGMOD '2018】Columnstore and B+ tree – Are Hybrid Physical Designs Important?
    https://zhuanlan.zhihu.com/p/546536492?utm_id=0
32. 优化器技术演进：统计信息feedback
    https://zhuanlan.zhihu.com/p/381127564?utm_id=0
33. OSDI 2020 论文笔记连载（0xB）——调度
    https://zhuanlan.zhihu.com/p/530533753?utm_id=0
34. [SIGMOD2021] Nova-LSM: A Distributed, Component-based LSM-tree Key-value Store
    https://zhuanlan.zhihu.com/p/385151808?utm_id=0
    1. 本文核心思想在于研究把LSM KV store进行存算分离，计算和存储分为不同的组件并通过RDMA通信。为了充分利用多存储节点的多disk带宽，memtable的数量会比传统的耦合lsm storage engine要更多，为了解决带来的写放大，通过引入Drange来做compaction的并行化，同时也引入相应索引来解决point/range query的性能问题。
35. PolarDB-X 全局 Binlog 解读之理论篇
    https://zhuanlan.zhihu.com/p/462995079?utm_id=0
36. PolarDB-X 数据分布解读（二） ：Hash vs Range
    https://zhuanlan.zhihu.com/p/424174858?utm_id=0
37. 云原生数据库的计算下推技术解读：Near Data Processing in Taurus Database
    https://zhuanlan.zhihu.com/p/613652367?utm_id=0
38. 深度复盘-重启 etcd 引发的异常
    https://zhuanlan.zhihu.com/p/604891779?utm_id=0
39. 一篇论文讲透Cache优化
    https://zhuanlan.zhihu.com/p/608663298?utm_id=0

40. Write Combine 和 Cache 是什么关系
    https://zhuanlan.zhihu.com/p/607637105?utm_id=0
41. 再议 IOMMU
    https://zhuanlan.zhihu.com/p/610416847
42. SMMU和IOMMU技术 [一]
    https://zhuanlan.zhihu.com/p/75978422
43. Multi-Core Cache Hierarchies（一）：大型缓存设计的基本要素
    https://zhuanlan.zhihu.com/p/621910178?utm_id=0
    1. interesting
44. 【目录序言翻译】多核心缓存层次结构《Multi-Core Cache Hierarchies》
    https://zhuanlan.zhihu.com/p/374496519
45. Pangu 2.0: 如何打造一个高性能的分布式存储系统
    https://zhuanlan.zhihu.com/p/611583679?utm_id=0
    1. good
    2. highlights
        1. Chunkserver的用户态文件系统基于RDMA的网络栈(DPDK)和SPDK的存储栈。在两种协议的基础上进行了如下的优化
        2. 采用高性能的NIC/RNIC、光模块（QSFP28 DAC、QSFP28 AOC、QSFP28等），单模/多模光纤和高性能交换机
        3. 动态为前端和后台流量分配网络带宽。 如果集群还有很多空闲流量，那么可以调低后台GC的带宽占用阈值，还有比如夜间调大GC带宽使用阈值，白天减小阈值等
        3. 远端缓存直接访问。 Pangu团队发现数据离开网卡后在内存中时间非常短（平均几百微秒）。假设在内存中停留的时间平均为200微秒的，对于双端口100 Gbps的网卡，只需要5 MB的临时存储来存储离开NIC的数据，因此他们使用英特尔的DDIO在商用硬件上实现了RDCA(Remote Direct Cache Access)使得发送这可以绕过接受者的内存直接访问Cache。在盘古的一些集群上的广泛评估结果表明，对于典型的存储工作负载，RDCA每台服务器消耗12MB LLC缓存(占总缓存的20%)，平均内存带宽消耗减少了89%，网络吞吐量提高了9%。RDCA在非存储工作负载中也很有效，例如，在延迟敏感的HPC应用程序中，它将集合通信的平均延迟降低了多达35.1%
        4. 混合RPC。 Pangu团队发现RPC请求中序列化/反序列化消耗了30%的CPU，因此他们对数据链路使用类似FlatBuffer替代Protobuf，但是在控制链路依然使用ProtoBuf，最终优化后单核CPU网络吞吐增加了59%
        5. 使用CPU wait指令支持超线程。 引入cpu wait指令解决超线程存在的同一个物理核线程切换的开销以及两个线程同时执行相互干扰带来的性能退化，最终单核CPU网络吞吐增加了31.6%
        6. Pangu的USSFS中提供了一系列机制来加速HDD的性能，例如利用自包含的块布局来减少元数据操作次数，利用磁盘内部和外部轨道的差异来提高写入效率
        7. 硬件卸载的成本与收益权衡。Pangu硬件卸载压缩的整个开发过程用了20人团队两年时间，期间也解决了许多问题，如FPGA硬件成本、压缩数据的完整性以及与硬件中的其他功能共存等问题
```

CephFS, CurveFS, MinIO.

```
1. CurveFS
    1. Netease developed CurveFS
       https://github.com/opencurve/curve
    2. CurveFS core dev's blob: Aspirer - 我这4年都做了什么
       https://aspirer.wang/?p=1707
        1. very good article. About Career. And,
           About Curve vs Ceph, key problems in very technical detail.

    """
    Curve文件存储研发目标：
    * 高性能
    * 高性价比
    * 支持公有云部署
    * 支持混合云部署
    * 支持冷热数据分层存储及数据生命周期管理
    * 支持多级缓存
    * 完整的POSIX兼容性

    Curve块存储：
    * 全链路瓶颈梳理
    * 大文件顺序读写性能优化
    * raft相关优化
    * 高性能硬件适配

    Curve文件存储：
    * 元数据性能优化
    * 数据面性能优化
    * FUSE优化
    * 多级缓存

    curvefs要做到什么样的优势才能替换cephfs，业务认为主要有两点：1）性能有较大优势；2）成本也更低；简单来说就是性价比要高才行。但我理解还有一层隐含要求，稳定性不能比cephfs差

    * 挑战1：EC存储引擎小文件空间利用率问题. 解决方案：针对小文件合并方案
    * 挑战2：冷归档存储业务需求和小规模成本问题. 解决方案：最终选择xx云作为冷归档存储类型的底层存储供应商，NOS做全托管的封装，据此把xx云给到网易集团的折扣，从y折砍到了x折，x/y=0.6
    * 挑战3：业务拓展问题. 存储系统关注的3大核心要素: 单位存储成本, 服务稳定性, 数据可靠性, 

    为了降本和拓展业务，我们还有很多挑战没有详细描述：
    * 低频、归档存储演进过程中的数据可靠性保障问题，我们转存了超过60%的数据到低频或归档存储引擎，同时我们还在底层把大量数据从filestore集群转移到bluestore集群，以及从1.5副本转移到1.2副本甚至更低冗余度的集群，这一系列过程中，我们承担了极大的数据可靠性风险（也在转存到各个阶段做了大量的校验程序），但是我们做到了转存xxPB数据的100%可靠性，并且做到了对业务无感知，没有造成任何性能和故障问题
    * 通过cdn进行直传优化，节省了大量的边缘节点成本（之前是aws海外虚拟机，或者国内idc租赁服务器来搭建直传边缘加速节点）
    * 我们还在公有云和私有云环境完成了网宿CDN到融合CDN的数千个域名的平稳迁移工作，也是为了给业务节省成本，改造了CDN管控服务，并且修复了多个CDN厂商间的兼容性问题
    * 我们调整了计费策略，让业务可以享受更多折扣，为此我们多次改造统计计费服务，承担了大量的改造工作量
    * 还有我们正在进行的ddb改造tidb工作，由于ddb存储的对象数量已经超过千亿，要扩容已经非常困难并且会导致空间严重浪费
    * 老旧腐化存储引擎的维护工作，也非常有挑战，比如sdfs，已经是10年前的软件，nefs也有5年历史，目前NOS日增数据近百TB，都是靠这两个引擎承担，并且我们为了节约成本又不适合进行扩容，因此这两个引擎的IO压力非常大，同时机器也比较老旧，各种异常都容易触发，而这两个引擎已经没有非常专业的人可以维护，为此我们也做了大量工作，来熟悉并掌控他们，也解决了多个严重问题
    * 为了提升xx业务数据转存到NOS的速度，我们对转存服务也做了大量性能优化工作，从最初的媒体xTB，到xxTB，提升了10倍；为了提升xx业务转存NOS低频存储数据到冷归档存储的速度，我们也对转存服务再次进行了优化，从每天xxTB提升到xxxTB，速度提升了4倍，数据转存时间从半年左右降低到了1.5个月，为业务节约了大量成本
    * 富媒体处理业务私有化部署改造，为云音乐海外云上私有化部署提供支持，节约业务开发成本，我们也有比较大的工作量
    * 与视频云共建视频处理服务，简化业务方使用逻辑的同时还可以为业务节省成本（价格更低）
    * 我们也做了很多安全增强工作，来提升业务使用nos的安全性
    """

    9. Aspirer - Curve vs Ceph    [2020]
       https://aspirer.wang/?p=1528

    """
    两个项目把集群部署起来都还算简单，ceph-deploy有个问题，部署比较慢，要串行操作，为此我们还优化了一下ceph-deploy工具。ceph部署完服务才算第一步，后面还要创建crush rule（这个如果没有经过深入研究，还是有比较高的门槛的），配置pool的各项参数等操作。

    curve应该只需要修改几个比较简单的配置文件（playbook的yaml），就可以一键部署搞定了，相对比较简单。

    维护的话，ceph一大问题是经常遇到慢盘、坏盘，影响client的IO，用户经常抱怨（会收到一堆util超过90%告警），长时间抖动要帮用户手工解决（停掉慢盘osd），或者短时间的抖动要帮用户确认是否ceph导致的util飙高。为此我们也做了大量的工作来搞定这一场景（如增加各种监控，进行巡检等及时发现问题，甚至发现慢盘自动停止osd等等），但总归是治标不治本，只能尽量规避。

    除了抖动，还有容量均衡问题（没有中心化的调度节点，只能根据使用情况进行osd的pg数量调整），集群缩容问题等比较难处理，老版本的pg数量不支持减少，是个比较大的问题（L版本也只能增加pg，更新的版本才支持减少pg），以及缩容后，即使只剩下少量的卷，也很难迁移到其他存储池（qemu用到了存储池，可以迁移到其他root rule，但是pg数量无法减少也是个问题），导致存储池使用的存储节点很难下线。

    扩容场景下，除非新建root rule和存储池，否则ceph需要对已有数据进行迁移均衡到新增加的节点上，这方面curve也是类似的（物理池逻辑与ceph的root rule类似），curve的好处是可以做到精确的带宽控制，减少对正常业务的影响。

    日常的坏盘替换场景下，ceph可以做到只迁移一次数据（L版本，H版本还不太行），也即坏盘下线的时候不做数据迁出，新盘上线时进行数据恢复即可（当然也可以做到自动迁出和迁入）。curve的话当前是下线自动迁出，上线自动迁入。二者区别不大，curve好处依然是精确带宽控制。

    压力检测是一个比较困难的场景（如何找出压力比较大的client，并及时对其进行限制防止雪崩效应？），也是一个强需求（虽然client有qos，但集群一般都有性能超售，部分client压力飙升可能影响整个集群），ceph场景下，由于只能看到集群压力情况，很难做到所有client的汇集（当前是qemu端做的监控）和分析（当然可能跟我们使用的自研监控服务不支持这种场景有一定关系），导致很难找出那个或者那些影响了整个集群的client。一般我们都是用土方法，查看压力大的osd，打开message日志，找出消息比较多client ip，然后再根据client的监控情况判断是否跑满，同时找出同样业务的其他虚拟机，然后逐个进行限速处理。这一过程肯定比较耗时耗力，还不一定准确（可能新版本已经支持了单个rbd卷的性能统计）。curve场景下就比较简单了，看下grafana的client监控，找到压力大的client对其进行限速即可。

    监控告警也是一大运维重点，ceph的话可以基于perf counter机制来做一部分，做不了的可以自己定制化扩展。也可以基于ceph-mgr+prometheus+grafana来做，一般还要配合存储节点的NODE_EXPORTER来做会比较全面。我们内部没有用这套机制，是基于自研的监控系统来做的，主要是用到了perf counter+监控脚本模式。

    相比ceph的模式，curve基于bvar+prometheus+grafana，监控指标拉取更及时，都是秒级的，可以实时显示性能、时延曲线。bvar另外一个好处是它对外提供的是http api，不是perf counter那种命令行，也就是说不需要在本地部署agent或者脚本即可拉取数据，管理起来比较方便。
    """

    3. CurveFS 设计要点
       https://github.com/opencurve/curve/blob/master/docs/cn/curvefs_architecture.md
       https://github.com/opencurve/curve/blob/master/docs/cn/curvefs-metaserver-overview.md
       https://github.com/opencurve/curve-meetup-slides/blob/main/CurveFS/Curve%E6%94%AF%E6%8C%81S3%20%E6%95%B0%E6%8D%AE%E7%BC%93%E5%AD%98%E6%96%B9%E6%A1%88.pdf
       https://github.com/opencurve/curve-meetup-slides/blob/main/CurveFS/Curve%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E7%A9%BA%E9%97%B4%E5%88%86%E9%85%8D%E6%96%B9%E6%A1%88.pdf
       https://github.com/opencurve/curve-meetup-slides/blob/main/CurveFS/Curve%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E5%85%83%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86.pdf
       https://github.com/opencurve/curve-meetup-slides/blob/main/CurveFS/Curve%E6%94%AF%E6%8C%81S3%20%E6%95%B0%E6%8D%AE%E7%BC%93%E5%AD%98%E6%96%B9%E6%A1%88.pdf

    4. CurveFS 源代码解读
       https://github.com/opencurve/curve/wiki/Curve%E6%BA%90%E7%A0%81%E5%8F%8A%E6%A0%B8%E5%BF%83%E6%B5%81%E7%A8%8B%E6%B7%B1%E5%BA%A6%E8%A7%A3%E8%AF%BB
       https://aspirer.wang/?p=1583
    5. CurveFS 元数据性能优化实践
       https://zhuanlan.zhihu.com/p/560236822
        1. 通过目录扩展属性的方式规避系统命令 du 递归查询的特性，通过在目录的扩展属性中记录本层文件和目录的统计信息
           https://zhuanlan.zhihu.com/p/560236822
           https://github.com/opencurve/curve/blob/master/docs/cn/curvefs_summary_xattr.md
            1. "CubeFS将子文件的容量记录在父目录的方式实际上是对两种方式的一个折中。由于目前CurveFS的元数据管理方式是类似于CubeFS的方式，即文件的元数据inode存储在父目录的inode所在的同一个partition中，那么像CubeFS那样记录子文件的容量在父目录中的xattr中是可行的"
    6. CurveFS预览版重磅首发，Curve加速迈向云原生软件定义存储
       https://juejin.cn/post/7042213839139504135
        1. Curve技术解析之MDS元数据管理
           https://zhuanlan.zhihu.com/p/333878236
    7. Curve 基于 Raft 的写时延优化
       https://blog.csdn.net/NetEaseResearch/article/details/124464440
    8. Curve 技术解析之 MDS 元数据管理
       https://my.oschina.net/u/4565392/blog/4749815


2. CephFS
    1. ChatGPT
       https://chat.openai.com/c/0697e08e-56dc-4e6c-83ad-0d8995fd68d4
       https://chat.openai.com/c/711df35f-4ed1-4863-b283-af1bf97bc52f
    2. Distributed transactions for rename and mv
        1. ChatGPT: No distributed transaction or 2PC. MDS are using locks.

    """
    CephFS uses a dynamic subtree partitioning strategy to distribute the metadata across multiple active MDS nodes (also known as MDS cluster). This strategy means that each directory inode and its descendants are managed by a single MDS at any given time, reducing the need for distributed transactions or coordination between MDSs for most operations.

    However, certain operations, like rename or mv, where inodes may span different subtrees (thus different MDSs), require coordination between multiple MDS nodes. The operation must be atomic and consistent; it should either fully complete or not happen at all, and the state of the filesystem should remain consistent before and after the operation.

    CephFS manages this by creating a system where all MDSs involved in an operation lock the inodes involved and agree on the sequence of events. This can be understood as a form of a distributed transaction. Here's a simplified explanation of how it works:

    1. The client sends the rename request to the MDS responsible for the source directory.
    2. The source MDS forwards the request to the destination MDS (if it's different).
    3. Both MDSs lock the inodes involved in the operation to prevent other operations on them.
    4. The MDSs perform the rename operation, updating the inodes and directory entries as necessary.
    5. The changes are journaled by each MDS.
    6. The inodes are unlocked, allowing other operations on them.

    This process ensures that the rename operation is atomic and consistent across different MDSs. If a failure occurs during the operation, the MDS can use its journal to revert to a consistent state. This is not a traditional two-phase commit because it doesn't involve a prepare and commit phase, but it ensures atomicity and consistency across multiple MDS nodes for these types of operations.

    --

    Handling failures during complex operations such as rename or mv is crucial in a distributed file system. In CephFS, there are multiple mechanisms in place to ensure that the file system remains consistent and can recover from failures.

    Firstly, the metadata operations in CephFS are journaled by the Metadata Server (MDS). This means that before an operation like a rename or mv is performed, the MDS writes the operation to its journal. The journal serves as a persistent record of all metadata operations. If a failure occurs during an operation, the MDS can replay its journal to recover to a consistent state.

    Secondly, in a multi-MDS configuration, CephFS ensures that each directory inode and its descendants are managed by a single MDS at a time. This reduces the need for complex coordination between multiple MDSs for most operations.

    However, operations like rename or mv that may involve multiple MDSs due to the inodes spanning across different subtrees are handled with care. The MDSs lock the inodes involved in the operation, preventing other operations from interfering. They then perform the operation, journal the changes, and finally unlock the inodes. This coordinated sequence ensures atomicity of the operation even in the presence of failures.

    In the event of an MDS failure, CephFS is designed to failover to another MDS. The journaling mechanism allows the new MDS to recover to a consistent state by replaying the journal.

    Moreover, CephFS maintains multiple copies of the metadata (the number can be configured) in the Ceph storage cluster. This replication of metadata ensures that if an MDS goes down, the metadata it was managing is not lost.

    In summary, through a combination of journaling, inode locking, MDS failover, and metadata replication, CephFS ensures that complex operations like rename or mv can recover from failures while maintaining the consistency of the file system.

    --

    The Metadata Server (MDS) in CephFS stores its journal in the Ceph RADOS cluster. The MDS's journal is essentially a sequence of RADOS objects. 
    """

3. MinIO
    1. It's an object storage systems. Feature in EC, and being lightweighted.
    2. ChatGPT: See CephFS vs MinIO in https://chat.openai.com/c/711df35f-4ed1-4863-b283-af1bf97bc52f
        1. What are the key differences between CephFS and MinIO in terms of architecture, design, and functionality?
        2. For a specific use case (such as storing large amounts of unstructured data, running a data-intensive application, etc.), which would be more appropriate to use, CephFS or MinIO, and why?
        3. How do the performance, scalability, and reliability characteristics of CephFS and MinIO compare?
```