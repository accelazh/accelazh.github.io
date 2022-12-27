---
layout: post
title: "Archiving recent article reading notes"
tagline : "Archiving recent article reading notes"
description: "Archiving recent article reading notes"
category: "technology"
tags: [cloud, storage, paper]
---
{% include JB/setup %}

Archiving notes about recent reading articles. Many.

```
2. Misc: Readings: Recent piled up articles
    1. Slack 架构设计 - Cocolian 老熊看架构
       https://mp.weixin.qq.com/s/7RMYxu63juP4UHao0nMWkA
    2. Whatsapp 系统架构 - Cocolian 老熊看架构
       https://mp.weixin.qq.com/s/q1dE8xFRL5rTvfDITB6DYQ
    3. Microsoft Dynamics 365 简史 - Cocolian 老熊看架构
       https://mp.weixin.qq.com/s/Sw4U35EI6fkRKC47iuhcsg
       微软PowerPlatform简史 - Cocolian 老熊看架构
       https://mp.weixin.qq.com/s/6Gk1kwiPCy0DoFMhnRY7-w

8. Readings: recent articles
    1. Amazon DynamoDB – a Fast and Scalable NoSQL Database Service Designed for Internet Scale Applications
       https://www.allthingsdistributed.com/2012/01/amazon-dynamodb.html
        1. useful to track history of DynamoDB
        2. highlights
            1. Compared to Dynamo, DynamoDB is a cloud service to relive the operational complexity. and a NoSQL DB but with better data model support

5. Misc: Readings: Recent articles
    1. AI系统全栈技术思考与展望 - 杨军
       https://zhuanlan.zhihu.com/p/462810001
        1. Very good arcitle. deep insights about AI stack software/hardware co-design and driving factors.

    2. B+树数据库加锁历史 - CatKang
       https://zhuanlan.zhihu.com/p/462576086
        1. useful, a resummarize of B+tree history
        2. related: 陈宗志：路在脚下, 从BTree 到Polar Index
           https://zhuanlan.zhihu.com/p/374000358

    3. LeanStore 论文阅读笔记 - 李喆的文章
       https://zhuanlan.zhihu.com/p/443809984
        1. LeanStore: In-Memory Data Management Beyond Main Memory    [2018, 42 refs]
        2. good paper, key desgin for mainly in-memory and offloading to SSD databases
           key designs are BufferManager pointer swizzling, cold queue without tracking temperature info
        3. related: Umbra论文阅读笔记 - 李喆的文章
           https://zhuanlan.zhihu.com/p/462740928
            1. variable sized page size in B+tree

5. Readings: Design Patterns in Distributed Storage / articles
    1. Top 5 distributed system design patterns
       https://www.educative.io/blog/distributed-system-design-patterns
        1. listing
            1. Command and Query Responsibility Segregation
            2. Two-Phase Commit
            3. Saga
            4. Replicated Load-Balanced Services
            5. Sharded Services
        2. What to learn next
            1. Sidecar Pattern
            2. Write-ahead Log
            3. Split-Brain Pattern
            4. Hinted Handoff
            5. Read Repair
        3. System Design Patterns
           https://www.educative.io/courses/grokking-adv-system-design-intvw
            1. Bloom Filters
            2. Consistent Hashing
            3. Quorum
            4. Leader and Follower
            5. Write-ahead Log
            6. Segmented Log
            7. High-Water Mark
            8. Lease
            9. Heartbeat
            10. Gossip Protocol
            11. Phi Accrual Failure Detection
            12. Split Brain
            13. Fencing
            14. Checksum
            15. Vector Clocks
            16. CAP Theorem
            17. PACELC Theorem
            18. Hinted Handoff
            19. Read Repair
            20. Merkle Trees
    
    2. Patterns of Distributed Systems - martinfowler
       https://martinfowler.com/articles/patterns-of-distributed-systems/
        1. very good article, seems community are already studying the bigger design patterns in distributed system
        2. pattern listing
            Consistent Core
            Follower Reads
            Generation Clock
            Gossip Dissemination
            HeartBeat
            High-Water Mark
            Hybrid Clock
            Idempotent Receiver
            Lamport Clock
            Leader and Followers
            Lease
            Low-Water Mark
            Paxos
            Quorum
            Replicated Log
            Request Pipeline
            Segmented Log
            Single Socket Channel
            Singular Update Queue
            State Watch
            Two Phase Commit
            Version Vector
            Versioned Value
            Write-Ahead Log

    3. Design Patterns for Distributed Systems - Stefano Tempesta
       https://www.codemag.com/Article/1909071/Design-Patterns-for-Distributed-Systems

    4. Cloud Design Patterns - Azure Doc
       https://docs.microsoft.com/en-us/azure/architecture/patterns/
        1. good summary and well documented
            1. interesting ones: geodes, 
        2. Catalog of patterns
            Ambassador
            Anti-Corruption Layer
            Asynchronous Request-Reply
            Backends for Frontends
            Bulkhead
            Cache-Aside
            Choreography
            Circuit Breaker
            Claim Check
            Compensating Transaction
            Competing Consumers
            Compute Resource Consolidation
            CQRS
            Deployment Stamps
            Event Sourcing
            External Configuration Store
            Federated Identity
            Gatekeeper
            Gateway Aggregation
            Gateway Offloading
            Gateway Routing
            Geodes
            Health Endpoint Monitoring
            Index Table
            Leader Election
            Materialized View
            Pipes and Filters
            Priority Queue
            Publisher/Subscriber
            Queue-Based Load Leveling
            Retry
            Scheduler Agent Supervisor
            Sequential Convoy
            Sharding
            Sidecar
            Static Content Hosting
            Strangler Fig
            Throttling
            Valet Key

12. Readings: Recent piled up articles
    1. 谷歌下一代AI架构、Jeff Dean宣传大半年的Pathways终于有论文了
       https://zhuanlan.zhihu.com/p/489559324
       https://www.zhihu.com/question/524596983/answer/2411800437
    
    2. CockroachDB死锁处理
       https://zhuanlan.zhihu.com/p/449151313
       https://zhuanlan.zhihu.com/p/472573422
        1. interesting .. Path-Pushing Algorithms
        2. ConcurrencyManager implementation
            1. the author has good writing skill
            2. very good article, tells the why with a illustrative upgrading model
                1. txnWaitQueue
                2. latchManager
    
    3. ToplingDB 省略 L0 Flush
       https://zhuanlan.zhihu.com/p/487604396
    
    4. DSA AI芯片，相对于GPGPU，究竟有多大的能效优势？主要是从哪些方面提高了能效？
       https://zhuanlan.zhihu.com/p/457265026
        1. Tenstorrent Grayskull
        2. useful summary and compare analysis

    5. 探索Snowflake auto clustering 设计
       https://zhuanlan.zhihu.com/p/490719154
        1. interesting, auto find the partition strategy and key

2. Reading: Recent piled up articles
    1. 探索 Snowflake Automatic Clustering 设计
       https://zhuanlan.zhihu.com/p/507150586
        1. interesting design. it seems use one LSM-tree for all partitions. 
           Each SSTable maps to a Micro-partition, that non-overlapping is desired, but lower levels still overlap much
           In another perspective, it's a mix use of tiering and leveling like the Dostoevsky paper
        2. because Snowflake uses S3 to store the SSTables, so they are naturally be able to share across any server, in a shared storage
           this naturally eliminates the diff of a local LSM-tree / SSTable vs a distributed LSM-tree / SSTable

7. Reading: Recent articles piled up
    1. Lealone的过去现在将来 #16 - Codefollower
       https://github.com/codefollower/My-Blog/issues/16
    2. Aurora读写细节分析 - 叶提
       https://zhuanlan.zhihu.com/p/508928878
    3. 分布式数据库（DorisDB、Clickhouse、TiDB）调研 - bluesky
       https://zhuanlan.zhihu.com/p/505192098
        1. good that it lists "主要缺点" for each
    4. Databricks Photon尝鲜 - 不要叫醒我
       https://zhuanlan.zhihu.com/p/511493662
    
    5. 数据库系统小报：CRDT初探 - 张茄子
       https://zhuanlan.zhihu.com/p/510797688
        1. 而像微软Azure提供的CosmosDB已经开始针对类似场景提供简单的CRDT支持了。
        2. 因果序一致性(或实时因果序一致性，Realtime Causual）是能够实现全可用（Total Available）的最高一致性级别
           我们还称CRDT为强最终一致（Strong Eventual Consistency）。从定义上来讲，它需要：当接收到同样的消息（更新）后，所有副本的状态会收敛到同样的状态
        3. 结合律、分配律和幂等性

    6. LakeHouse 技术概览
       https://zhuanlan.zhihu.com/p/502745565
        0. good summary
        1. Data Warehouse 诞生之初，主要是为了解决决策支持、BI 等分析型问题，数据一般都是有 Schema 的。随着数据量急速增长，数据类型丰富多样，Data Warehouse 显现出如下问题：
        （1）存储和计算紧密耦合，无法单独弹性扩展，不符合云时代的潮流。当数据量增大时，成本很高。Snowflake 等云原生数仓也能解决这个问题，下一个问题才是关键。
        （2）无法存储诸如视频、音频、文档等非结构化数据，这些数据在爆炸性增长。
        Data Lake 的诞生就是为了解决以上问题。Data Lake 将原始数据以 Open formats 的方式（例如：Apache Parquet, ORC）存储在低成本的存储系统，以文件 API 直接访问。为了简化实现，Data Lake 砍掉了相当一部分 DBMS 的能力，例如：ACID 事务能力、良好的性能等。
        
        2. LakeHouse - Data Warehouse + Data Lake
        （1）一致性问题。要保证 Data Lake 与 Data Warehouse 一致性代价较高。两个系统之间不断 ETL 的流程比较复杂，如果出现问题，会影响数据分析的性能和准确性。
        （2）数据过时问题。Data Warehouse 的数据是从 Data Lake 传输过来的，天然存在一定的延时，这与第一代分析系统相比，是一种退步。论文给了数据： 86% of analysts use out-of-date data and 62% report waiting on engineering resources numerous times per month
        （3）对 Machine Learning 和 Data Science 的支持能力欠缺。目前所有流行的机器学习系统（例如 TensorFlow, PyTorch等）并不能完美地运行在 Data Warehouse/Data Lake 之上。对于 Data Warehouse，因为机器学习系统需要通过非 SQL 接口访问海量的数据集。通过传统的 ODBC/JDBC 访问的效率太低了，Warehouse的内部专有数据格式很难被直接使用。针对这些 case，一些 Warehouse 厂商建议将数据导出为文件，这既增加了复杂性，又让更加数据过时。当然也可以直接使用 Data Lake 的文件（Open Formats），但这样就丢失了 Warehouse ACID 事务、data 多版本和索引等高级特性， ML 和 DS 系统也迫切需要数据库解决这类问题。
        （4）成本问题。ETL本身需要成本。许多数据需要在 Data Lake 和 Warehouse 存两份，double 存储成本。
        那么，有没有可能构建一个一体化的系统，既能提（1）供类似 DW 的高性能与数据管理能力。（2）还能保持 DL 低成本、Open Formats 格式存储的优势。（2）还能更好地支持诸如 Machine Learning，Data Science 等高级分析能力 workloads 直接、实时、快速读取文件的需求。
        LakeHouse 是作者们预想的下一代 OLAP 系统，旨在解决上述问题
        
        3. 在 LakeHouse 上构建 SQL 查询，最主要的挑战是：传统 DBMS 的存储格式是数据库内部定义的，统一且高效，而 Data Lake 的文件类型多种多样，且现有的 open formats 格式也是多种多样。因此只能从一些 format-independent 的优化入手：
        （1）缓存。数据库常用优化方式了，将访问频繁的文件缓存在执行节点的 SSD 或者内存里。甚至可以将这些文件转换为某种中间格式，更有利于 query engine 使用。比如 Databricks 缓存的数据里解压了 Parquet 格式部分数据。
        （2）辅助数据结构。也是常见的优化方法，比如增加一些文件相关的统计信息列；加 Bloom Filter。
        （3）Data layout 优化。还是常见的优化方式，也有很多方法可以参考，比如尽量让可能同时访问的 records 存储在一起。Delta Lake 支持单个维度或者多个维度（利用 Z-Order/Hilbert 等空间填充曲线）的 locality。

    7. Crystal: A Unified Cache Storage System for Analytical Databases - henry liang
       https://zhuanlan.zhihu.com/p/498693473
        0. Interesting paper. Interesting trends.
        1. Highlights
            1. Problems to solve
                1. 每个DBMS系统都有自己的一套caching实现，导致了很多重复的轮子
                2. 数据分析系统开始越来越多的处理各类不同格式的数据源，包括CSV/JSON/AVRO/Parquet…，从工程角度需要能够统一对数据的处理方式
                3. 主流方案是基于data block/data file这个粒度做缓存，因此即使只需要其中少量数据也需要全量加载，cache利用率较低，考虑到local SD空间有限，而且可能和其他数据（query中间结果）共享空间，这个问题会更突出
                4. 很多云storage具备了计算下推能力，而主流的caching组件一般没有考虑到这方面
            2. Solutions
                1. 通过目前大多数据系统支持的data source API的方式，适配到各种不同DBMS中，尽量避免对数据库内核的修改，并且可以为各类系统提供公共caching服务
                2. 利用目前Parquet + Arrow生态的不断适配和融合，在crystal系统cache的数据都以parquet文件存储，而系统内部的计算则基于arrow高效完成
                3. 缓存的方式不再是简单的block/file，而是semantic caching，即基于查询语义的缓存，这有些类似于materialized view，即针对单表，缓存其经过谓词过滤+目标列过滤后的结果数据，供后续使用。
                4. 由于缓存的本身就是计算后的数据，因此可以透明的利用上计算下推的能力，如果storage不具备该能力则需要download全量数据在cache层完成过滤
        n. related materials
            1. 云原生数仓的优化 - FlexPushdownDB: Hybrid Pushdown and Caching in a Cloud DBMS - henry liang
               https://zhuanlan.zhihu.com/p/493739926
                1. Snowflake saves data file at S3. Like DB's query push down, we also need S3 computation pushdown
                2. Combing cache + pushdown is a valid approach. Need to merge results returned from Local Cache and Pushdown Storage
                3. When to use Cache or Pushdown, the query executor needs fine-grained scheduling, separate case by case
                   In general, if data present in Cache, use Cache first, other parts use Pushdown
                   The underlying assumption is: bottleneck is networking transfer from S3 to Local node. Compared to leveraging parallel computing from S3, favor use local node to compute locally from cache

4. Readings: recent articles piled up
    1. PebblesDB - Fragmented LSM-tree - Guards in LSM-tree levels
       https://zhuanlan.zhihu.com/p/46069535
       https://vigourtyy-zhg.blog.csdn.net/article/details/109005795
        1. the original paper
           https://www.cs.utexas.edu/~vijay/papers/pebblesdb-sosp17-slides.pdf
           https://www.cs.utexas.edu/~rak/papers/sosp17-pebblesdb.pdf

4. Reading: Recent articles piled up
    1. Influxdb中的Compaction操作 - 扫帚的影子
       https://zhuanlan.zhihu.com/p/64764457
    2. 阿里云发布CIPU，对云计算产业有什么影响？ - 卧闻海棠花
       https://www.zhihu.com/question/537455142/answer/2527647290
    3. 读后感：SuRF（SIGMOD 2018 Best）
       https://zhuanlan.zhihu.com/p/45152394
    4. 云原生消息队列Pulsar浅析 - 阿里开发者
       https://zhuanlan.zhihu.com/p/518687208
        1. Apache BookKeeper 分布式日志

    5. FAST21 论文学习：REMIX: Efficient Range Query for LSM-trees - Goclis Yao
       https://zhuanlan.zhihu.com/p/357024916
        1. existing art: LSM-Tree 进行范围查询是一个归并的过程
            1. 在每个 run 内用二分得到首个大于等于 begin key 的位置，作为该 run 的初始化 cursor。
            2. 利用最小堆维护这些 cursor。
            3. 每次 pop 堆顶 cursor 对应的数据，然后得到新的堆顶，直到堆顶 key 大于 end key。
        2. LSM-tree run 的基础属性之一是不变性（immutability），而在底层 table 不变的情况下，基于 run 构造的 sorted view 同样继承了这一特性。
           因此，如果能够将 sorted view 高效地存储下来，那么它天然就是多个 run 的索引，能够有效地加速查询
            1. additionally
                1. Cursor offsets 记录了每个 run 中首个大于等于 anchor key 的 key offse
                2. Run selectors 顺序记录了 segment 内每个 key 所在的 run 序号

    6. 通过数据组织加速大规模数据分析 - 李呈祥
       https://zhuanlan.zhihu.com/p/354334895
        1. Data Clustering是指数据按照读取时的IO粒度紧密聚集，而Data Skipping则根据过滤条件在读取时跳过不相干的数据，
           Data Clustering的方式以及查询中的过滤条件共同决定了Data Skipping的效果
        2. 在大数据分析的典型场景中，多维分析一般都会带有过滤条件，对于这种类型的查询，尤其是在高基数字段上的过滤查询，
           理论上可以在读取数据的时候跳过所有不相关的数据，只读取极少部分需要的数据，这种技术一般称为Data Clustering以及Data Skipping
        3. Z-Order

    7. 深入浅出GPU优化系列：GEMM优化（三） - 有了琦琦的棍子
       https://zhuanlan.zhihu.com/p/481600052
    8. 是否真的存在天才？ - Iris Pan
       https://www.zhihu.com/question/34054445/answer/446806457
    9. 哪些思维方式是你刻意训练过的？ - Iris Pan
       https://www.zhihu.com/question/23913984/answer/748002225
    10. 从 Redis7.0 发布看 Redis 的过去与未来 - 阿里云云栖号
        https://zhuanlan.zhihu.com/p/527916427
    11. 存储日报-20220615 - StorPlus
        https://zhuanlan.zhihu.com/p/528945047?utm_source=ZHShareTargetIDMore&utm_medium=social&utm_oi=30546549800960
        1. Lyve Cloud Archive 存储服务和 Lyve Cloud Marketplace。Lyve Cloud Archive 存储是 Seagate 为大型视频和图像存储库、辅助数据集、备份副本以及分析或事务密集型工作流程之外的数据专门设计的

    12. 万字长文详述对话推荐系统的逻辑与演化 - 尚琛展
        https://mp.weixin.qq.com/s/Bqq9VDJeRNzPFaKqSEURfg
    13. B站 API 网关的发展 -  哔哩哔哩技术
        https://mp.weixin.qq.com/s/-bV1gZq7GO6bGPcYGAwc9g
    14. 十年磨一剑！OceanBase查询优化器的设计之道和工程实践哲学 - 聿明leslie
        https://zhuanlan.zhihu.com/p/67078227
    15. 浅谈内存分层（memory tiering) - 秦冕
        https://zhuanlan.zhihu.com/p/483517959
    16. 你所需要了解的几种纹理压缩格式原理 - 蕾芙丽Reverie
        https://zhuanlan.zhihu.com/p/237940807
    17. 大规模图计算系统综述 - 围城
        https://zhuanlan.zhihu.com/p/38010945

    18. 百亿级小文件存储，JuiceFS 在自动驾驶行业的最佳实践
        https://juicefs.com/blog/cn/posts/ten-billion-level-small-files-storage-juicefs-best-practice-in-the-autonomous-driving-industry/
        1. Targets LOSF lots of small files problem, interesting JuiceFS
    19. 如何将知识图谱引入推荐系统？ - 王鸿伟
        https://mp.weixin.qq.com/s/OmfqCUcE0XglOeWrPFmDPg
    20. 从DPU开始到RDMA到CUDA - 吴建明wujianming
        https://zhuanlan.zhihu.com/p/517176491
    21. 关于时序数据库中时间线膨胀(高基数Cardinality)问题的探索 - 胡津铭
        https://zhuanlan.zhihu.com/p/514845817
    22. 字节跳动一站式数据治理解决方案及平台架构
        https://mp.weixin.qq.com/s/Eg8MzyP-sv449vDYNLucwg
    23. Facebook专家：Huge Page是否为拯救性能的万能良药？
        https://mp.weixin.qq.com/s/p1mO-8TTtNSbIoTnHTHfaQ
    24. 自动驾驶的基本过程（一）：感知
        https://zhuanlan.zhihu.com/p/421068097
        自动驾驶的基本过程（二）：决策
        https://zhuanlan.zhihu.com/p/421078810

1. Reading: Recent articles piled up
    1. 面向高性能计算场景的存储系统解决方案
       https://mp.weixin.qq.com/s/qd8Su0IKSGQic509BS6FAA
    2. Designing a Userspace Disk I/O Scheduler for Modern Datastores: the ScyllaDB example
       https://www.scylladb.com/2016/04/14/io-scheduler-1/
       https://www.scylladb.com/2016/04/29/io-scheduler-2/
    3. 从 SIGMOD 22 论文看 Redshift 的最新进展
       https://zhuanlan.zhihu.com/p/545348145?utm_source=ZHShareTargetIDMore&utm_medium=social&utm_oi=30546549800960
    4. 2021.07.13 我们是这样崩的 - 哔哩哔哩技术
       https://mp.weixin.qq.com/s/nGtC5lBX_Iaj57HIdXq3Qg

    5. 火山引擎总裁谭待解析超视频时代音视频架构建设与演进
       https://mp.weixin.qq.com/s/KXD847vRRhCMM0nQOgElyA
        1. "ROI编码，其基本原理是用户对显著性区域的视频质量比较敏感，希望通过检测+编码来提升显著性区域画质"
           good interesting technology. So an video has asymmetric encoding at different spots even on the same image. well attentioned spots use better quality encoding

    6. SingleStore 在高盛资产管理公司领投的一轮融资中筹集了 1.16 亿美元。该公司总部位于旧金山，是面向数据密集型应用程序的云原生关系数据库的开发商
       https://zhuanlan.zhihu.com/p/541709185
       https://images.go.singlestore.com/Web/MemSQL/%7B39161d94-1112-44f4-bb81-f287ed088842%7D_whitepaper_introduction_to_singlestoredb_2022.pdf
        1. Formly known as MemSQL. 

    7. Hyper DataBlocks - 谁人识君
       https://zhuanlan.zhihu.com/p/489441544
    8. 一些有趣的B+树优化实验 - TencentDB腾讯云数据库
       https://zhuanlan.zhihu.com/p/526143517
        1. "主题为“基于硬件透明压缩的B+树优化”。本次分享的论文针对可计算存储SSD（支持硬件透明压缩）提出了三种有趣的设计方法，从而极大地减少了B+-tree的写放大（10X）以使其接近甚至超越LSM-tree"

    9. Runtime Filter in OLAP joins
       https://www.51cto.com/article/712334.html
       (字节跳动数据平台技术揭秘：基于ClickHouse的复杂查询实现与优化)
       https://cloud.tencent.com/document/product/1387/70895
    10. ZNS : 解决传统SSD问题的高性能存储栈设计（fs--＞io--＞device）
        https://zhuanlan.zhihu.com/p/425123214

    12. Lindorm: Ribbon filter: practically smaller than Bloom and Xor
        https://zhuanlan.zhihu.com/p/543943112
    13. OceanBase的memtable设计成key为主键，value为行操作链表的目的是什么？ - 李晨曦
        https://www.zhihu.com/question/62125049/answer/195568837
    14. 研发了5年的时序数据库，到底要解决什么问题？ - 陶建辉
        https://mp.weixin.qq.com/s/MFGbnKabuKd528cQRzcllg
    15. 每秒10W次分词搜索，产品经理又提了一个需求！！！ - KG沈剑
        https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651970886&idx=1&sn=c941d38dd361977ecc667fac3312966a

    16. 字节跳动自研万亿级图数据库 & 图计算实践 - ByteGraph
        https://zhuanlan.zhihu.com/p/109401046
        1. good, can be used as a reference for industry level graph database
        2. "采用灵活的边聚合方式，使得 KV store 中的 value 大小是均匀的，具体可以用以下四条来描述
            1. 一个点（Vertex）和其所有相连的边组成了一数据组（Group）；不同的起点和及其终点是属于不同的 Group，是存储在不同的 KV 对的；比如用户 A 的粉丝和用户 B 的粉丝，就是分成不同 KV 存储；
            2. 对于某一个点的及其出边，当出度数量比较小（KB 级别），将其所有出度即所有终点序列化为一个 KV 对，我们称之为一级存储方式（后面会展开描述）；
            3. 当一个点的出度逐渐增多，比如一个普通用户逐渐成长为抖音大 V，我们则采用分布式 B-Tree 组织这百万粉丝，我们称之为二级存储；
            4. 一级存储和二级存储之间可以在线并发安全的互相切换"
        3. 中国信通院发布了国内图数据库功能白皮书
        4. "Tencent Plato 是基于 Gemini 思想的开源图计算系统，采用了 Gemini 的核心设计思路，但相比 Gemini 的开源版本有更加完善的工程实现，我们基于此，做了大量重构和二次开发，将其应用到生成环境中，这里分享下我们的实践"
            1. "Gemini 是 16 年发表再在 OSDI 的一篇图计算系统论文，结合了多种图计算系统的优势，并且有开源实现，作为最快的图计算引擎之一，得到了业界的普遍认可。

                正如《Scalability! But at what COST? 》一文指出，多数的图计算系统为了拓展性，忽视了单机的性能，加之分布式带来的巨大通信开销，导致多机环境下的计算性能有时甚至反而不如单机环境。针对这些问题，Gemini 的做了针对性优化设计，简单总结为：

                * 图存储格式优化内存开销：采用 CSC 和 CSR 的方式存储图，并对 CSC/CSR 进一步建立索引降低内存占用；
                * Hierarchical Chunk-Based Partitioning：通过在 Node、Numa、Socket 多个维度做区域感知的图切分，减少通信开销；
                * 自适应的 Push / Pull 计算：采用了双模式通信策略，能根据当前活跃节点的数量动态地切换到稠密或稀疏模式。
                * 兼顾单机性能和扩展性，使得 Gemini 处于图计算性能最前沿，同时，Gemini 团队也成立了商业公司专注图数据的处理"

4. Readings: Recent articles piled up
    1. OpenTelemetry
       https://opentelemetry.io/docs/concepts/
        1. Pretty much stems the MicroService distributed tracing framework originated from Google Dapper
           https://research.google/pubs/pub36356/

6. Reading: Recent articles: ZNS SSD knowledge background
    1. SDC: Zoned Namespaces (ZNS) SSDs: Disrupting the Storage Industry
       https://www.snia.org/educational-library/zoned-namespaces-zns-ssds-disrupting-storage-industry-2020
        1. Conventional SSD problems
            1. Over-provisioning wasted disk space
            2. Non-deterministic throughput drop when SSD GC kicks off
            3. Latency cost due to FTL internal mapping
        2. An industrial standard version of open-channel SSD
    2. ZonedStorage.io - more technical documentation for ZNS
       https://zonedstorage.io/docs/introduction/zoned-storage
    3. ReFS Support For Shingled Magnetic Recording Drives
       https://www.snia.org/educational-library/refs-support-shingled-magnetic-recording-drives-2017
        1. All metadata in SSD flash tier, not on SMR
        2. GC controled by application, pausable/resumable/abortable
            1. Large file gets dedicated bands
            2. Small file share bands
    4. Zone Random Write Area
       https://0x10.sh/zone-namespace-ssd

4. Readings: Recent articles piled up
    1. Yann Lecun: A Path Towards Autonomous Machine Intelligence 自主机器学习和AGI - HeptaAI
       https://zhuanlan.zhihu.com/p/535157931
        1. 分层规划（Hierarchical Planning）
    2. 回顾6年深度学习的算法实践和演进 - Peter潘欣
       https://mp.weixin.qq.com/s/Z-w0OvBDrrbEp08xowD-YA
    3. 解读谷歌Pathways架构 - OneFlow
       https://zhuanlan.zhihu.com/p/495592456
       https://mp.weixin.qq.com/s?__biz=MzU5ODY2MTk3Nw==&mid=2247487190&idx=1&sn=b8c171fbbda735cab41abdcfc7247cfb
        n. related
            1. 如何评价 Google 在 2022 年 3 月公开的 Pathways 架构设计？
               https://www.zhihu.com/question/524596983/answer/2420225275

    4. QoS in Quincy: Comparison of mClock and WPQ schedulers with background operations
       https://ceph.com/en/news/blog/2022/mclock-vs-wpq-testing-with-background-ops-part1/
       https://ceph.com/en/news/blog/2022/mclock-vs-wpq-testing-with-background-ops-part2/

    5. Google AlloyDB for PostgreSQL    [2022-05-11]
       https://cloud.google.com/blog/products/databases/alloydb-for-postgresql-intelligent-scalable-storage
        1. Like AWS Aurora (single master), but AlloyDB is disaggregated, with dedicated Log Processing servers, and Log Storage / Block Storage are separated and backed by a shared GFS.
           AlloyDB is a regional service across AZs. Only one primary instance hands change, no active-active, but promises fast recovery.
        2. Highlights
            1. Key designs
                1. Only one primary instance processes DB modifications
                   Primary generates WAL that is stored in low latency Log Storage
                   Log Processing Service consumes WAL and generate blocks
                   Blocks are persisted in Block Storage
                   Blocks are fed to replica instances.
                   Blocks are served to primary instance if it restarts or needs cache load
                   Primary also stream WAL to replica instances to notify about recent changes.
                2. Log Storage and Block Storage are regional
                   Primary instance and replica instances are at different zones
                   Log Storage and Block Storage backed with a shared Google Distributed Filesystem
                   Compute layer only communicates WAL to storage layer, no page sync, no checkpointing. Storage layer continuously replay WAL.
                   To scale out LPS, DB is sharded and each shard assigns to one LPS. Shards can reassign
                3. PostegreSQL is disaggregated: Compute Server, Log Processing, Log Storage, Block Storage
        n. related materials
            1. 如何评价 Google 在2022年推出的 AlloyDB 全托管式 PostgreSQL 数据库?
               https://www.zhihu.com/question/532611092/answer/2485873878
            2. Spanner系share nothing架构和Aurora系共享存储架构哪种在将来的竞争中更有优势？
               https://www.zhihu.com/question/547714000
            3. AlloyDB for PostgreSQL under the hood: Intelligent, database-aware storage
               https://zhuanlan.zhihu.com/p/522460906
            
            4. 从分布式Distributed、日志Log、一致性Consistency分析AWS Aurora for MySQL - Tony
               https://zhuanlan.zhihu.com/p/549700484
                0. very good article that explains AWS Aurora in very details. it should be the first time that someone explains clearly how these LSNs work and why the motivation.
                1. "但Aurora是整个数据data set有6个copy，而且每个copy，是做了shard，即segment方式分割数据。每个segment不允许超过10G，data set超过此大小限制即形成新的segment，segment之间是数据连续分布的。比如：整个dataset是20G，那么是2个segment，又必须有6个copy，则总共有12个segment。这12个segment，至少可以用6个Storage node去承担，也可以最多12个Storage node去成承担（也可以6-12中间任何一个数字）。并且，segment可以后台移动，即从一个Storage node，作为一个整体单位（segment为单位），移动到另外一个Storage node上。"

                   "Spanner是先考虑shard（比如：最少2个key就可以分布了），将数据分散到多个node上，然后执行数据处理时，预先用Distributed Transaction做了准备。

                    而Aurora是先不考虑shard，即10G下，不需要多个segment。同时，做数据处理时，即使数据分布在多个segment上，也不需要Distribute Transaction考虑。即多个segment虚拟连接成好像一个独立的数据库存储空间（可以抽象成一个文件或一个table space，所有表table对应的clustered index和second index都在里面，即所有的B tree），所以，我们仍然可以用B tree对应的页page，以及任何一个page都只有唯一的Number（即Page No.）标识此page，只是Page No.需要根据node、segment进行一个相应的换算即可。"
                2. "Aurora后期也提供多Master（Multi Master）的支持，但提供较晚，而且是基于前期Single Master模式上改造的，本文只分析早期的Single Master模式。"
                3. "因为乱序，所以，可以并发。即站在master眼里，上一个redo log record暂时还没有成功，并不影响处理下一个recoord发送给存储层。"
                   "master上的DB cache page的内容，可以远远领先于存储层对应的page内容。注：为了防止超前太多，Aurora加了一个LAL约束，LAL = 10 million，即不能跑太快，超过千万"
                4. "但是，Aurora不是这样处理的（因为LSN并不是严格增1连续的，即continuous，它只保证唯一unique和递增increasing，实际上，LSN是对应record在redo里的字节偏移量，byte offset），所以，Aurora用了另外一个技术，链表，即每个redo log record，都记录了前一个redo log record的LSN，即prev LSN。"
                   "所以Aurora里面，是存了三个prev LSN，分别是，基于整个redo log record链表的prev LSN，基于segment的prev LSN，和基于Block的prev LSN。"
                5. "统的MySQL，在收到App的commit请求时，必须先生成对应的redo log record（先在内存里，即redo buffer），然后必须保证写盘成功（flush to disk，同时也保证之前的redo log record和相关的undo record log也写盘成功），然后才能接着处理后续的相关内容，包括解锁、改变Transaction状态（从transaction list里删除此Transaction ID）和返回commit成功信息给客户App。

                    如果到了Aurora这里，生成的commit redo log record收到了Storage node的四个response，虽然此record被标识某种成功了（success of collecting quorum response），但仍不算write success，必须保证前面的所有的乱序和异步发送的redo log record也标识成功（success of collecting quorum response），此commit redo record才算写成功（success of quorum write），然后才能接着处理解锁、改transaction list以及回应App成功这些动作。

                    但注意：其他非commit类型的redo log record的动作，master可以继续做，不受任何约束。"
                6. "如果再转义一下，VCL就是站在Computing node视角，针对存储层，落盘成功的最大的LSN，且保证之前的LSN全部落盘成功。

                    注意：Aurora master实现VCL计算时，不是通过保存所有的redo record log记录的状态进行的，它只要收集所有Storage nodes的redo log record的连续状态，然后简单计算即可获得这个VCL。这样一是简化了master上的状态保存复杂度，二是可以保证六台Storage node（如果都活的话）都满足VCL，或者至少哪4台Storage node满足VCL。"
                7. "因为mini transaction保证了B tree的完整性（否则，如果有split和merge动作只完成一半，整个B tree的遍历traverse会出错，即mini transaction定义了一连串split和merge页面动作，以保护后续的其他事务对B tree可以安全遍历）。而一个mini transaction形成的多个（最少可以一个）redo log records是一个整体，这里面的最后一个LSN，相当于逻辑上的mini transaction logic mini commit log record。而VDL就是这样一个logic mini commit log record，它最接近VCL。"
                8. "但上面分析说了，slave apply是可以略过（omit or skip）那些不在DB cache for slave的页面page，所以，当slave到Storage node去读某个page时，它必须读到截止到slave VDL时刻的页面值，即：如果从master角度看，这些slave从Storage node读出的page，必须是master在slave VDL时刻完全一模一样的内存page（注意：master DB cache里，此时，即物理上slave write时刻，可能有更新的页面内容，而且，这个对应更新页面内容的redo log，可能也已经发给了Storage node）。

                这个如何解决？

                当slave从Storage node去读page时，它必须传入slave VDL作为参数，而Storage node在形成这个page时，不能用up-to-now的最新值，而必须是截止到slave VDL的page，而我们上面《Log的妙趣》分析了，我们可以通过page的初始值，然后再apply redo log records，获得任何一个时刻的page。因此，Storage node只要apply到小于和等于slave VDL的redo log records，就能返回合适的page值。

                所以，Storage node必须保持redo log records的链表，这样，才能形成各个版本的page（有点类似MVCC）。"
                "上面的分析还带来一个问题，Storage node如果一直保留redo log records，不会撑破Storage nodes的内存？

                解决方法也很简单：在所有的slave中，总有一个最小的read only transaction，它起始的read snapshot是基于某个slave VDL，对于这个最小的VDL，它之前的redo log records，Storage node都不用保存（因为未来发来的slave VDL参数只可能比这个大）。而随着read only transaction for slave的结束，这个slave VDL一定是向前推进的（slave VDL会越来越大）。这个不断推进的最小的slave VDL，在Aurora里，被叫做Protection Group Minimum Read Point LSN (PGMRPL)。master和所有的slave交互，获得这个PGMRPL，然后发给Storage nodes，然后Storage node就可以根据PGMRPL，去做相关的清理purge工作，即从Storage node内存里的链表里，删除PGMRPL之前的redo log record，还可以删除相应的磁盘page image，也就是说，Storage node可以做purge或GC了。"
                8. "补注：再解释一下，为什么master的读可以只受VCL的约束，而slave却要受VDL的约束，是因为master上的事务，是真事务，是有锁保障其安全的，即使某个时刻B tree不一致，因为master的锁机制，它保护不一致的B tree，然后再继续执行的mini transaction中修补这个不一致同时防止其他事务读到这个broken B tree（只需要保护B tree里的broken part）。但slave上，并不是真正的transaction在执行，slave write只是apply atomic redo records from master，slave只有apply时，才能用stop the world的方式（即slave并不用真正的事务锁），保证B tree由不一致转化为一致，如果中间切换read only transaction for slave来执行，就打破了这个atomic约束而且没有真正的写事务锁来保护，让read only transaction for slave可能遍历到不一致的B tree。"

    6. JuiceFS - A POSIX, HDFS and S3 compatible, cloud native, distributed filesystem. 
       https://juicefs.com/docs/community/architecture/
        1. "JuiceFS is designed to bring back the gold-old memories and experience of file systems in local disks to the cloud".
           Key feature: multi-cloud and cross-cloud. Tens of billions of files management. Fully POSIX-compatible, support old tool chains
           "The metadata engine is a pluggable architecture" - Redis/TiKV/MySQL. The usecase seems brewed from automatic driving area
        2. highlights
            1. File -> split into 64MB chunks -> one or more Slices -> 4MiB Blocks -> Stored in Object Storage
               Metadata about file, chunks (map to OS directory), slices, blocks are stored in Metadata Engine via JuiceFS. Metadata Engine is (usually) backed by Redis/TiKV/MySQL
            2. JuiceFS doesn't support Snapshot.
               https://juicefs.com/docs/community/comparison/juicefs_vs_cephfs
            3. 10 billion small file storage - Usecase: Automatic driving
               https://car.inotgo.com/2021/11/20211119205838587J.html
               https://juicefs.com/blog/cn/posts/ten-billion-level-small-files-storage-juicefs-best-practice-in-the-autonomous-driving-industry/
                1. My questions
                    1. Handling large volume of metadata is the key problem of LOSF. But JuiceFS's solution is "The metadata engine is a pluggable architecture"
                       I didn't see special design or optimziation for this part
            4. JuiceFS 在携程海量冷数据场景下的实践
               https://mp.weixin.qq.com/s/n3rkD-0nxTCHEEYWGe_GzA
                1. Metadata by TiKV, data by Ceph
                2. JuiceFS在创建文件/目录时在TiKV里的Key是父目录 inode + 新条目的名字，所以目录深度不影响TiKV里的键值对大小

    7. Amazon Redshift: Ten years of continuous reinvention    [2022-05-18]
       https://www.amazon.science/latest-news/amazon-redshift-ten-years-of-continuous-reinvention
       Amazon Redshift Re-invented     [2022, 0 refs, SIGMOD]
       https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf
        1. "our pricing at $1000 a terabyte per year, people just couldn’t believe we could offer a product with that much capability at such a low price point"
        2. "you could provision a data warehouse in minutes instead of months also caught everyone’s attention"
           "working with customers’ on-premises systems where it would take us several days or weeks to resolve an issue, whereas with a cloud data warehouse like Redshift, it would take minutes"
           "In the on-premises world, it was taking months if not years to get new functionality into a software release"
        3. "Analytics has always been super important, but eight or ten years ago it wasn’t necessarily mission critical for customers in the same way transactional databases were"
        4. "Another big trend has been the desire of customers to query across and integrate disparate datasets"
        5. "Now, if you are offering data warehousing as a service, the systems must be capable of auto tuning, auto healing, and auto optimizing"
        6. "Redshift Serverless removes all of the management of instances and clusters"
        7. "Then customers said they needed access to high-velocity business data in operational databases like Aurora and RDS .. Then we added support for streams, as well as integration with SageMaker and Lambda so customers can run machine learning training and inference without moving their data"

    9. 浅谈这些年做的算法经验 - FlyEgle
       https://zhuanlan.zhihu.com/p/539203832
    10. AI芯片技术市场思考 - 吴建明wujianming
        https://zhuanlan.zhihu.com/p/539749699
    11. 下篇：技术 Leader 的思考方式
        https://zhuanlan.zhihu.com/p/526571851
        https://mp.weixin.qq.com/s?__biz=MzU4NzU0MDIzOQ==&mid=2247510077&idx=1&sn=c8093891ea8bc0871c680c27a71ab8b8
    12. LLVM之父Chris Lattner：编译器的黄金时代
        https://zhuanlan.zhihu.com/p/500904014
    13. Snowflake发布HTAP解决方案Unistore，用于同时处理交易和分析的业务负载
        https://www.modb.pro/db/417488

    14. Lethe 如何优化 LSM-Tree delete 难题
        https://zhuanlan.zhihu.com/p/291135599?utm_id=0
        Lethe: A Tunable Delete-Aware LSM Engine    [2020, 30 refs]
        https://cs-people.bu.edu/dstara/pdfs/Lethe.pdf
        1. FADE: Tombstone deletion time is bounded. 
                 This is tracked by tracking the oldest one per file, and update on compaction.
                 This is done by scheduled compaction and a wise selection of SSTfiles being compacted
        2. KiWi (Key Weaving Storage Layout)
            1. SSTFile -> Delete tiles (sorted by sort key S) -> Pages (cross page sorted by deleted key D) -> records (intra page sorted by S)
            2. Range query for delete key is fast: by skipping Pages. Trade off: slower range query for sort key S

    15. Colocate Join ：ClickHouse的一种高性能分布式join查询模型 - 华为云开发者联盟
        https://zhuanlan.zhihu.com/p/552103878
        1. 根据“相同JOIN KEY必定相同分片”原理，我们将涉及JOIN计算的表，按JOIN KEY在集群维度作分片。将分布式JOIN转为节点的本地JOIN
    16. 最新中国PaaS市场报告说了点啥？
        https://mp.weixin.qq.com/s/nxlkp6fIfnnVEPZrqX0WTA
    17. 高性能索引Bw-Tree综述
        https://zhuanlan.zhihu.com/p/549953001
    18. OSDI 2022 论文评述-0x0：Persistent Memory
        https://zhuanlan.zhihu.com/p/541162485
        OSDI 2022 论文评述-0x1：Distributed Storage and Far Memory
        https://zhuanlan.zhihu.com/p/541262524
        1. Carbink: Fault-Tolerant Far Memory
            1. "Carbink采用了基于Spanset而非单个Span的擦除码。具体地说，它不像传统擦除码那样使用单个Span分割后的碎片生成奇偶校验，而是用相同大小的Span生成校验，这样对单个Span进行换入换出只需要一次网络IO"
    19. 如何用PM(NVM)优化LSM-Tree - ssynn
        https://zhuanlan.zhihu.com/p/458669973

    20. 来自Redis的官方吐槽：13年来，总有人想替Redis换套新架构 vs Dragonfly - Yiftach Shoolman 、Yossi Gottlieb 和 Filipe Oliveira
        https://mp.weixin.qq.com/s/Y9IYB_VepsouHQ0Pd8yVoQ
        1. Key points
            1. Redis runs on a single core. Scale out by running multiple Redis instances
               "我们不允许单一 Redis 进程的大小超过 25 GB"
    21. 现代数据栈：一些深入的思考 - Yingjun Wu
        https://zhuanlan.zhihu.com/p/551722728
        1. "公司不再会为某一个技术产品建立堆栈，而是为自己的数据建立堆栈。"
        2. "从传统的Extract，Transform，Load（ETL）变成Extract，Load，Transform（ELT）所谓ETL"
           "ELT的本质其实就是将数据仓库变成整个数据管理的中心"

    22. 突破性能瓶颈，火山引擎自研vSwitch技术实践揭秘
        https://mp.weixin.qq.com/s/K8XaU2ieeJspMhJO3JP5GA
    23. MySQL分析型执行引擎HeatWave
        https://zhuanlan.zhihu.com/p/386109853
        1. "MySQL官方团队发布了新的分析执行引擎 – Heatwave，遗憾的是目前这一服务仅限于Orcale Cloud Infrastruct上使用"
    24. 数据库故障恢复机制的前世今生
        https://zhuanlan.zhihu.com/p/54981906
        1. for NVM  
            1. MARS - Redo logs + No steal, log supports random access and can be copied to as data
            2. WBL - Not append-only, Force + Undo logs 

    25. PolarDB-CloudJump：优化基于云存储服务的云数据库(发表于VLDB2022) - 陈宗志
        https://zhuanlan.zhihu.com/p/535426034
        1. 我们发现CloudJump面临以下技术挑战：
            1. 远程分布式存储集群的访问导致云存储服务的I/O延迟高；
            2. 通常聚合I/O带宽未被充分利用；
            3. 在具有本地存储的单机上运行良好但需要适应云存储而导致特性改变的传统设计，例如文件cache缓存；
            4. 长链路导致各种数据库I/O操作之间的隔离度较低（例如，日志刷写与大量数据I/O的竞争）；
            5. 云用户允许且可能使用非常大的单表文件（例如数十TB）而不进行数据切分，这加剧了I/O问题的影响。
        2. CloudJump针对上述挑战，提出7条优化准则：
            1. Thread-level Parallelism：例如依据I/O特性实验，采用（更）多线程的日志、数据I/O线程及异步I/O模型，将数据充分打散到多个存储节点上。
            2. Task-level Parallelism：例如对集中Log buffer按Page Partition分片，实现并行写入并基于分片进行并行Recovery。
            3. Reduce remote read and Prefetching：例如通过收集并聚合原分散meta至统一的superblock，将多个I/O合一实现fast validating；通过预读利用聚合读带宽、减少读任务延时；通过压缩、filter过滤减少读取数据量。与本地SSD上相比，这些技术在云存储上更能获得收益。
            4. Fine-grained Locking and Lock-free Data Structures：云存储中较长的I/O延迟放大了同步开销，主要针对Update-in-place系统，实现无锁刷脏、无锁SMO等。
            5. Scattering among Distributed Nodes：在云存储中，多个节点之间的分散访问可以利用更多的硬件资源，例如将单个大I/O并发分散至不同存储节点 ，充分利用聚合带宽。
            6. Bypassing Caches：通过Bypassing Caches来避免分布式文件系统的cache coherence，并在DB层面优化I/O格式匹配存储最佳request格式。
            7. Scheduling Prioritized I/O Tasks：由于访问链路更长（如路径中存在更多的排队情况），不填I/O请求间的隔离性相对本地存储更低，因此需要在DB层面对不同I/O进行打标、调度优先级，例：优先WAL、预读分级。
    26. CurveFS (网易Ceph) - 分布式存储限速(Qos)设计 - hongsong wu
        https://zhuanlan.zhihu.com/p/450656361

    27. Sparrow: Distributed, Low Latency Scheduling [2013, 700 refs] 学习笔记 - someoneATwu
        https://zhuanlan.zhihu.com/p/56608510
        1. Batch-based Sampling - probe worker queue length
        2. Late binding (interesting idea)
            1. "Sparrow提出了late binding来解决前面sample-based scheduling的两个问题。具体地，当用户收到探针后，不会立刻回复，而会放置一个task的reservation到worker的task queue中。当这个reservation到达了队列的第一个位置，worker会发送一个RPC给schedule这个job的scheduler。然后scheduler会将m个task调度给dm个中前m个返回的worker上，然后对于剩下的(d-1)m个worker，会发送一个no-op来取消对应worker上面task reservation。"
            2. Proactive Cancellation
    28. SIGMOD21 ArkDB: A Key-Value Engine for Scalable Cloud Storage Services [2021, 2 refs, SIGMOD21] - Simpo
        https://zhuanlan.zhihu.com/p/414054332
        1.
        2. highlights
            1. "ArkDB建立在盘古(一个append-only的分布式文件系统)之上"
            2. "存储的主干结构是一棵 B+ 树" "对于用户checkpoint，同一叶子page的数据更改形成了Host page的Delta Page"
               "从概念上讲，DeltaPageStream、BasePageStream和PageMappingTable一起形成了一个存储上的Bw-tree，这是一个B+树的变体"
            3. "为了降低PageMappingTable(一个并发哈希表)的大小，ArkDB使用物理页ID (PID)，由(ExtentID, Offset, PageSize)表示，无需搜索页面映射表找到数据的位置"

    29. 严选库存中心设计实践
        https://mp.weixin.qq.com/s/K0qlulP3gx5Qghv5mPwY3g
    30. 案例：百度的评论系统是怎么设计的？
        https://mp.weixin.qq.com/s/wveq1JA4AzHNJVpws6lJhA
    31. 一文了解编译时 if-constexpr
        https://mp.weixin.qq.com/s/Z3bcEitxdxXfRJxzvdcApA
    32. 从百度搜索质量谈起 - caoz的梦呓
        https://mp.weixin.qq.com/s/MjLvoz-BMGTmWirepYEo8g

1. Reading: Recent articles piled up    （12:30 - 13:00)
    1. 流处理的状态存储在设计时有哪些考虑? - 孙挺Sunt
       https://zhuanlan.zhihu.com/p/506869449
    2. 「万字长文」GPU渲染管线和硬件架构 （转载） - SlyerD
       https://zhuanlan.zhihu.com/p/550519794
    3. 揭秘流数据库中的共享索引和增量 Join
       https://zhuanlan.zhihu.com/p/521759464
    4. 《游戏设计心理学》试读：社会渗透理论（5万7千字长文慎入！） - 法师猫不凡
       https://zhuanlan.zhihu.com/p/529351858
    5. 揭秘 Chromium 渲染引擎（一）：RenderingNG
       https://zhuanlan.zhihu.com/p/438734215

6. Reading: Recent articles piled up
    1. 读懂黎曼猜想（11【完结篇】）——等差数列素数定理的余项（Siegel-Walfisz定理） - TravorLZH
       https://zhuanlan.zhihu.com/p/412127981
    
    2. Google: Spanner on a modern columnar storage engine
       https://cloud.google.com/blog/products/databases/spanner-modern-columnar-storage-engine
       1. 存储日报: https://zhuanlan.zhihu.com/p/561589853
          "Google Spanner 存储引擎迁移至列式存储。Spanner 最开始是基于 SSTable(Sorted String Table) 技术栈的，这种技术栈是 Bigtable 的完美匹配，但它并不是 Spanner 的最佳匹配，特别是遍历单列时是低效的。所以谷歌将 Spanner 的存储引擎迁移至一个新的面向列的存储引擎：Ressi。"

    3. 移动平台的AA技术调研
       https://zhuanlan.zhihu.com/p/552525041

    4. SingleStore (S2DB)论文阅读笔记 - 李喆
       https://zhuanlan.zhihu.com/p/536315172?utm_id=0
        1. Paper：Cloud-Native Transactions and Analytics in SingleStore (SIGMOD 2022)
        2. Unified table storage
            1. 对用户来讲，choosing rowstore 还是 columnstore 可能是个 hard choice，因为这需要让用户自己去判断涉及这张表的 workload 是更偏向于 TP 还是 AP，如果很均衡那就无了。为了解决这个问题，S2DB 提出 Unified table storage，将原本的 columnstore 进行优化来支持 AP 和 TP。其采用基于 LSM tree 的方式，将数据写入连续的 chunks 中。为了加速 TP 性能，做了如下优化：
                1. 做了个包存在内存中的 delete bitset，而不是像其他 LSM tree 实现（e.g., RocksDB）那样用 tombstone entry 来标记 delete (merge on read，读放大太大)。
                2. 和其他 LSM tree 实现类似，写入部分依然放在 in-memory 中 (不一样的事需要额外处理 metadata)。
                3. 构建了大量支持 LSM tree 的 secondary index 来支持 efficient point access。比如 bloom filter 和 inverted index 来过滤不需要访问的 segments。以及 S2DB 自己的 two-level index structure (如下图) 来定位 segment 和 offset。
                4. row-level lock 来避免 blocking。

    5. How we built a general purpose key value store for Facebook with ZippyDB
       https://engineering.fb.com/2021/08/06/core-data/zippydb/
        1. KV store, geographically distributed
           tunable durability, consistency, availability, and latency guarantees
           Small key-value data, Based on to RocksDB, In production for more than six years
        2. Highlights
            1. Combining Data Shuffle with Reusing RocksDB, with Shard Manager, ZooKeeper
                1. Data Shuffle does data replication with Paxos. Multi-Paxos
            2. Deployment unit - Tiers: compute and storage resources spread across several geographic regions
                1. placement hints, stickiness constraints
                2. caching layer
                3. a pub-sub system allowing subscriptions to data mutations
            3. Data model
                1. iterating over key prefixes and deleting a range of keys
                2. test-and-set, read-modify-write transaction, conditional writes
                3. access data on ZippyDB through an ORM
                4. p-shard, μshards (micro-shards) / u-shard - Akkio mapping
                5. Future: detecting failures entirely within Data Shuttle (“in-band”) and reelecting the leaders
                           without having to wait for ShardManager and incurring delays
                    1. question: why this is important? leader reselection is so frequent?
            4. tunable durability, consistency, and performance
                1. how many replicas need to write in a Paxos Quorum
                   when can ack to user writer
                    1. e.g. only primary finishes write, some app cannot tolerate cross-region latency for every write
                2. consistency levels
                    1. eventual consistency
                        1. total ordering for all writes within a shard
                        2.  reads aren’t served by replicas that are lagging behind primary/quorum beyond a certain configurable threshol
                    2. read-your-write
                        1. clients cache the latest sequence number returned by the server for writes and use the version to run at-or-later queries while reading
                    3. strong consistency
                        1. clients can see the effects of the most recent writes regardless of where the writes or reads come from
                        2. implemented by routing the reads to the primary in order to avoid the need to speak to a quorum, mostly for performance reasons
                           where the primary hasn’t heard about the lease renewal, strong reads on primary turn into a quorum check and read
            5. Transactions and conditional writes
                1. OCC: read snapshot, serializable isolation
                    1. The clients typically read from a secondary all of the data from a snapshot of the DB, compose the write set, and send both the read and write sets to the primary to commit
                    2. cost to maintain history versions: reject all transactions that have reads against a snapshot with lower version
            6. Future
                1. ZippyDB is still evolving and currently undergoing significant architectural changes, such as storage-compute disaggregation, fundamental changes to membership management, failure detection and recovery, and distributed transactions

    6. Black-box Concurrent Data Structures for NUMA Architectures - Dase314-ECNU
       https://zhuanlan.zhihu.com/p/559096522
        1. NR 在每个Node上持有数据结构副本
           在每个Node内部，NR 使用flat combining
           在Node之间，线程通过Shared Log进行协调

    7. B+树数据库故障恢复概述 - CatKang
       https://zhuanlan.zhihu.com/p/571426935

    8. 集群调度系统的演进 - 邵明岐
       https://zhuanlan.zhihu.com/p/51790388
    9. 为什么Kubernetes的架构是现在这个样子的？ - 邵明岐
        https://zhuanlan.zhihu.com/p/55401096

    10. Storage and Networking: Rook on Multus - Sébastien Han & Rohan Gupta, Red Hat
        https://www.youtube.com/watch?v=zIS5qaG_HRw&list=PLj6h78yzYM2Nd1U4RMhv7v88fdiFqeYAP&index=75 

    11. 从DynamoDB 2022 Paper回看Lindorm的一些设计
        https://zhuanlan.zhihu.com/p/565957106

    12. 国产数据库OceanBase，如今入选了国际顶会VLDB 2022
        OceanBase: A 707 Million tpmC Distributed Relational Database System
        https://mp.weixin.qq.com/s/MI5X1AdBiv05ScHJKbbFhA

    13. 端到端一致性,流系统Spark/Flink/Kafka/DataFlow对比总结(压箱宝具呕血之作) - 阿莱克西斯
        https://zhuanlan.zhihu.com/p/77677075
            1. very good

4. Reading: Openstack Summit 2022
    1. Summit video links
       https://www.openstack.org/videos/summits/berlin-2022
       https://openinfra.dev/summit/berlin-2022/summit-schedule
```