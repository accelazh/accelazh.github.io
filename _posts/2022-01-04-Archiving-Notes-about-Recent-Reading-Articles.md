---
layout: post
title: "Archiving notes about recent reading articles"
tagline : "Archiving notes about recent reading articles"
description: "Archive notes about recent reading articles"
category: "technology"
tags: [cloud, storage, paper]
---
{% include JB/setup %}

Archiving notes about recent reading articles. Many.

```
2. Misc: Readings: Piled up Weichat articles    (3hrs)
    1. tidying up all opened tabs and move to bookmark and sync manually    (2hrs)
        1. WTF .. verbose .. hope chrome sync worked

    2. 读 Instructions for PhD Students 有感
       https://zhuanlan.zhihu.com/p/430479667
        1. Instructions for PhD Students - Dimitris Papadias, HKUST
           https://cse.hkust.edu.hk/~dimitris/Instructions%20for%20PhD%20Students.pdf
            1. TODS, TOIS, VLDBJ, TKDE, ICDE, besides SIGMOD, VLDB, (+PODS)
            2. useful guides for students. basic needs for SWE maturity
            3. key contributors of PHD working
                1. reading, CAKE, ICING
                2. motivation, paper acceptance and reject, get involved
                3. practicing writing, clarify your mind, presentation and go into details
                4. presentation is organized just like paper writing structure, need to ensure audience can understand
                5. how to write paper
                    1. "Presentation is as important (if not more) than the actual work. Presentation is easier to improve"
                    2. "Write the papers first and decide the topic later .. The most difficult paper is the first one"
                6. About Laziness
                    1. "The less you work, the less you want to work – which creates a vicious circle"
            3.5. details are important
                 Describe the problem in detail
                 Pay attention to the detail
            4. Concrete Advice
                • Read papers
                • Bother me with questions, ideas etc.
                • Ask to give presentations
                • Write drafts of your ideas, or summaries of the
                papers that you have read and seem important
                • Never miss a deadline
                – e.g., if you have a task that requires 1 week, ask for 2
                to be on the safe side.
                • Pay attention to the detail

    3. 3399 万元、湖南省省级电子政务外网统一云平台资源补充项目：中兴通讯中标
       https://mp.weixin.qq.com/s?__biz=MzI4OTc4MzI5OA==&mid=2247544948&idx=6&sn=e89031d33a1b7f753095164b022ae80d&chksm=ec2b9b19db5c120fd39a521a1d5014dc866fb7aff39cb741c2df54e22562722a1008067f3b87
        1. good useful. the bidding whitepaper is in good detail, for learning what end users are expecting about the architecture
        2. highlights
            1. "四横三纵架构，四横是IaaS（基础设施服务层）、DaaS（数据服务层）、PaaS（平台服务层）和SaaS（软件服务层），三纵是标准规范体系、安全保障体系、运维保障体系"
            2. Most concerns are IaaS level resource capacity, they need to grow now, and resource utilization
               Backup and disaster recovery, security firewall, 安全保障，运维管理
               management platform, data intelligence
            3. "将大数据中心由单一集群架构改造为“1+N”的多集群部署模式"

    4. AI软硬全栈设计 - 杨军 - 大规模机器学习
       https://zhuanlan.zhihu.com/p/399927702
       https://zhuanlan.zhihu.com/p/388682140
       https://zhuanlan.zhihu.com/p/419640679
       https://zhuanlan.zhihu.com/p/408783175
       https://zhuanlan.zhihu.com/p/424913344
       Hotchips 2021随感: https://zhuanlan.zhihu.com/p/403927377
       MLIR编译技术应对硬件设计挑战？—初探CIRCT项目: https://www.birentech.com/news/94.html
        1. LLAM compiler for 数据库、AI、EDA、搜索引擎
           AI DSA chips, System-on-Wafer
           MLIR + RISC-V + CIRCT - very interesting
        2. "Google推TensorFlow，FB推PyTorch，微软在推ONNX，国内的话，我们能看到百度在推PaddlePaddle，华为在推MindSpore，当然还有主打大规模高性能的Oneflow。"

    5. 两万字长文：聊聊程序人生 - 陈天
       https://zhuanlan.zhihu.com/p/355363343
        1. 你是怎么找到好玩的项目的？
            A：这是个好问题。这涉及到一个信息来源的问题。我平时会逛一些各种各样的软件网站，比如说我会订阅很多种语言的邮件列表，然后每周这些邮件列表发送时，不是说所有的文章我都会去看，我只是会扫一下他们的标题，看看有什么感兴趣的东西，然后我在深入了解。我一周会逛个两三次 hacker news 和 github trending
    
    6. 逃离Google后，我跌宕而精彩的两年 - 赵亚雄 / PixieLabs
       https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzI5MzAyOTYwNA==&mid=2247493847&idx=1&sn=7d22335de8126eae67538bd9e32f438d
        1. "我发现，随着Google应用规模和复杂度的指数增长，Borg越来越不能满足应用开发的需求。Borg作为Google的容器管理平台，自2003年开始研发，2005年全面进入生产系统，2008年基本成熟；经过多年的持续改进，在可扩展性、性能、效率、容错/容灾、资源调度效率等主要技术指标上都达到业界领先水平。但是近年来，Borg对于应用系统全生命周期，及其他基础设施系统（DevOps，Security & Privacy，Resource Management）的支持显得越来越吃力。我总结的具体问题包括：配置文件管理效率低下，并且经常导致生产环境事故；应用开发期间与Borg的交互过程自动化程度低，开发人员经常需要手动完成大量调试、配置，上线运营之后，又要花费大量时间调整和优化资源使用，导致开发人员在使用Borg过程中效率低下；系统整合缺乏明确API接口，导致容器平台基础之上的周边系统的开发成本极高，已有系统效率低下，晦涩难懂，用户和维护人员都苦不堪言。这些问题的一个具体反映就是当时用户提交的与开发体验相关的Bug report有700项之多，并且常年无法得到解决，个别Bug的历史甚至长达10年之久。"
        2. "然而，进度最糟糕还是寻找创业搭档。首先我要反思在Google的6年，我做成了个傻子、聋子、瞎子：Google的高质量人脉，我竟然没有有意识地利用起来。比如，过去6年，竟然没有深交过哪怕一个产品经理！"

    7. 《Optimal Column Layout for Hybrid Workloads》论文读后感 - 萌豆
       https://zhuanlan.zhihu.com/p/400225192
        1. the modeling is very interesting .. let's read paper. CMU 15-721

    8. Telltale：看 Netflix 如何简化应用程序监控体系
       https://mp.weixin.qq.com/s?__biz=MzA5OTAyNzQ2OA==&mid=2649731418&idx=1&sn=841237191a902468836e632438e57275&chksm=88938e39bfe4072fabce2bbe2bbb41b9c43c6e35cdacbe584fcf31b216ba695088e00de68ae8

    9. 阿里道延：我对技术架构的理解与架构师角色的思考
       https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzA5OTAyNzQ2OA==&mid=2649721202&idx=1&sn=97b3edaa344a1d901ee6ad4b8c4830e4&scene=94&subscene=315
        0. very good article to learn how architect works and what to practice
        1. 架构师角色打散再各个团队成员中，优秀的技术同学一直再用架构的意识解决问题
           前瞻性：大量的实践和知识积累，了解前代历史、上下游，接触更多的人和事，用新的方法解决问题
           解决复杂问题：基本面高并发和高可靠，紧迫问题用户体验、效率、成本，挑战用户分层、内部技术人员多
        2. 发现问题，定义和分析问题。阿里不缺解决问题的同学。定义问题这个要求非常高
           解决问题需要实施路径和解决方案，协同团队和上下游，推进问题的解决。抽象
        3. 还有就是要去看论文. 每天去学习。每天花 2 到 3 个小时去学习.

    10. 左耳朵耗子：我做系统架构的一些原则
        https://mp.weixin.qq.com/s?__biz=MzI1MTMwMTQ1MA==&mid=2247484721&idx=1&sn=b0ff955e69287cfe24f1110207af7800&chksm=e9f45e14de83d702e37c2d261e78079d513c0ab14c60a8578438c86500644e5050f3ea404533
        1. highlights
            1. outline
                原则一：关注于真正的收益而不是技术本身
                原则二：以应用服务和 API 为视角，而不是以资源和技术为视角
                原则三：选择最主流和成熟的技术
                原则四：完备性会比性能更重要
                原则五：制定并遵循符从标准、规范和最佳实践
                原则六：重视架构扩展性和可运维性
                原则七：对控制逻辑进行全面收口
                原则八：不要迁就老旧系统的技术债务
                原则九：不要依赖自己的经验，要依赖于数据和学习
                原则十：千万要小心 X – Y  问题
                    1. 用户为了解决 X问题，他觉得用 Y 可以解，于是问我 Y 怎么搞，结果搞到最后，发现原来要解决的 X 问题，这个时候最好的解决方案不是 Y，而是 Z
                原则十一：激进胜于保守，创新与实用并不冲突
                    1. 进步永远来自于探索，探索是要付出代价的，但是收益更大。对我而言，不敢冒险才是最大的冒险，不敢犯错才是最大的错误
            2. 一些软件设计的原则
               https://coolshell.cn/articles/4535.html
                1. good useful. it summarizes basically every design principles, e.g. SOLID
                2. highlights
                    1. Don’t Repeat Yourself (DRY)
                    2. Keep It Simple, Stupid (KISS)
                    3. Program to an interface, not an implementation
                    4. Command-Query Separation (CQS)  – 命令-查询分离原则
                    5. You Ain’t Gonna Need It (YAGNI)
                    6. Law of Demeter – 迪米特法则
                    7. 面向对象的S.O.L.I.D 原则
                    8. Common Closure Principle（CCP）– 共同封闭原则
                    9. Common Reuse Principle (CRP) – 共同重用原则
                    10. Hollywood Principle – 好莱坞原则
                    11. High Cohesion & Low/Loose coupling & – 高内聚， 低耦合
                    12. Convention over Configuration（CoC）– 惯例优于配置原则
                    13. Separation of Concerns (SoC) – 关注点分离
                    14. Design by Contract (DbC) – 契约式设计
                    15. Acyclic Dependencies Principle (ADP) – 无环依赖原则
                n. related
                    1. KISS - Keep it simple stupid. V.S. OO principles
            3. SteveY对Amazon和Google平台的吐槽
               https://coolshell.cn/articles/5701.html
                0. very good. rare material to learn from top company insights and the author is very mindful
                   Accessibility is top for production for everyone, only platform rather than product can do this, this is what Google is missing in gene
                1. 这份大命令大概有如下几个要点：（陈皓注：这里是本篇文章的要点！...那可是2002年左右啊）
                    1) 所有团队的程序模块都要以通过Service Interface 方式将其数据与功能开放出来。（陈皓注：Service Interface也就是Web Service）
                    2) 团队间的程序模块的信息通信，都要通过这些接口。
                    3) 除此之外没有其它的通信方式。其他形式一概不允许：不能使用直接链结程序、不能直接读取其他团队的数据库、不能使用共享内存模式、不能使用别人模块的后门、等等，等等，唯一允许的通信方式只能是能过调用 Service Interface。
                    4) 任何技术都可以使用。比如：HTTP、Corba、Pubsub、自定义的网络协议、等等，都可以，Bezos不管这些。（陈皓注：Bezos不是微控经理吗？呵呵。）
                    5) 所有的Service Interface，毫无例外，都必须从骨子里到表面上设计成能对外界开放的。也就是说，团队必须做好规划与设计，以便未来把接口开放给全世界的程序员，没有任何例外。
                2. challenges for large scale SOA .. "一切以Service第一"为系统架构
                    1. pager escalation - 20 teams * 15min each is bad
                    2. quota and throttle. every related team can be a DOS
                    3. 监控与QA是被统一了 .. 为了要确认整个服务能正常运作，你需要对Service的每一个部分都去Call一下。这个问题会以递归的形式地出现，直到你的监控系统能够全面性地系统地检查所有的Services和数据，此时，监控系统就跟自动化测试QA没什么两样了，所以两者完美的统一了
                    4. 上百个Services .. 一套Service发现机制
                    5. 调试其他人的代码以调查问题变得非常的难 .. 除非有一套全面性的标准的方式，他可以在可被调试的沙盒里运行所有的Services
                3. Accessibility，这是计算机世界中最最重要的事情
                    1. 当Software——或ideal-ware——如果因为某些原因不能被存取或使用，那么，这就是软件或是那想法的错了。这就是Accessibility failure
                    2. 不过，我会和你争论Accessibility要比安全性来的重要多了
                4. 没有平台的产品是没用的，再精确一点，去平台化的产品总是被平台化的产品所取代
                    1. Google+是我们完全失败的不懂Platform最明显的例子
                    2. Facebook的成功是因为他们建立了一个可以让外界在其上上面开发的产品群。所以对Facebook对每个人来都不一样
                    3. 我们没有领会平台，我们也无法领会到Accessibility。这两者本来就是同一件事，因为平台会解决Accessibility。而平台就是Accessibility
            4. 分布式系统的事务处理
               https://coolshell.cn/articles/10910.html
            5. GO语言、DOCKER 和新技术
               https://coolshell.cn/articles/18190.html

    11. 分布式存储相关内容
        https://zhuanlan.zhihu.com/p/447839843
        1. 分布式数据库
            OLTP
                Spanner CockroachDB YugabyteDB FoundationDB TiDB PolarDB-X
            OLAP
                Greenplum ClickHouse Snowflake AnalyticDB
            云原生数据库
                PolarDB PolarDB-X AnalyticDB Snowflake
        2. 分布式文件系统
            GFS HDFS Pangu CephFS GlusterFS Lustre JuiceFS PolarFS
            Alluxio

    12. ToplingDB 和 TerarkDB 有什么区别？
        https://www.zhihu.com/question/507334544/answer/2280166589
        https://github.com/topling/toplingdb
        1. 雷鹏是 Terark 和 Topling 的创始人（github id rockeet），TerarkDB 和 ToplingDB 有两个共同点：都 fork 自 rocksdb,都使用了同一套底层算法
        2. "We disallow bytedance using this software, other terms are identidal with upstream rocksdb license"

    13. 大数据技术漫谈 ——从Hadoop、Storm、Spark、HBase到Hive、Flink、Lindorm
        https://zhuanlan.zhihu.com/p/407175099
        1. very good summarize nowadays mainstream bigdata platforms covering streaming, resource management, storage, messsaging, logging
           with compares, and evolving history, and summarized tables
        2. highlights
            1. 流式计算框架有Storm/Jstorm、Spark Streaming、Flink/Blink, Flink/Blink是当前流式计算领域的主流框架
            2. 离线计算领域主要有Hadoop MapReduce、Spark、Hive/ODPS等, Hive的学习成本最低，各大公司应用最广泛
            3. NOSQL的概念博大精深，有键值（Key-Value）数据库、面向文档（Document-Oriented）数据库、列存储（Wide Column Store/Column-Family）数据库、图（Graph-Oriented）数据库等
               Lindorm是HBase的升级版本，性能和稳定性等等通通优于HBase
        3. Lindorm
            1. "Lindorm团队最初都是做阿里内部HBase的，他们基于HBase做了一系列优化，解决了HBase的一系列问题，并以此为基点，慢慢研发出自己的多模引擎，试图一统存储分析技术，凭一己之力，实现MySQL、HBase、时序数据库等等的完整功能"
               "云原生存储引擎LindormStore为统一的存储底座，向上构建各个垂直专用的多模引擎，包括宽表引擎、时序引擎、搜索引擎、文件引擎"
               "Lindorm既提供统一的SQL访问，支持跨模型的联合查询，又提供多个开源标准接口(HBase/Phoenix/Cassandra、OpenTSDB、Solr、HDFS)"
               "对于目前使用类HBase+ElasticSearch或HBase+OpenTSDB+ES的应用场景，比如监控、社交、广告等，利用Lindorm的原生多模能力，将很好地解决.."
               "全局二级索引", "多为索引SearchIndex"
            2. “但Lindorm二级索引也恰恰是它坑的地方，因为，它每创建一个二级索引就是重新copy一份数据，所以Lindorm的运维和开发同学会建议你慎用二级索引”
            3. “HBase的读写毛刺是怎么产生的，Lindorm如何解决HBase的读写毛刺? HBase底层是Java写的，毛刺的一大来源是JVM GC。Lindorm针对这个问题，一方面从HBase源码级别进行了优化，大幅度减少了系统运行时对象的创建，从而降低了GC的压力；另一方面也是和阿里内部jvm团队合作，使用了更加适合Lindorm的GC算法。Lindorm团队是阿里内部最早使用ZGC的两个团队之一，至少在2019年，ZGC还在实验阶段的时候，Lindorm就已经全量使用上ZGC了”
            4. “Lindorm对于单行跟MySQL对ACID的支持是等同的，但跨行是不支持事务的”
            5. other materials
                1. Alibaba Cloud: Lindorm (HBase Enhanced Edition)
                   https://partners-intl.aliyun.com/help/doc-detail/190575.htm
                   https://www.zhihu.com/column/c_1366104426311184386
                2. How Can Alibaba's Newest Databases Support 700 Million Requests a Second?
                   https://www.alibabacloud.com/blog/how-can-alibabas-newest-databases-support-700-million-requests-a-second_595828
                    1. "the Lindorm file LDFile, similar to HFile in HBase, was created in the read-only B+ tree structure"
                       HBase cached index block row keys have shared prefix. Lindorm compress it via Succinct Trie tree (SuRF). More densed index block, more efficient caching
                        1. "reducing the space required by up to massive 1200%" .. this is good
                    2. Z Garbage Collector enables a pause of five milliseconds for 100 GB. powered by Dragonwell JDK
                       It uses Mutator to identify pointer changes through read memory barriers
                       optimizing Lindorm memory management to reduce objects and memory allocation window
                    3. LindormBlockingQueue .. CAS, cache line padding, dirty read caches; a variety of wait policies, including spin, yield, and block
                    4. Lindorm kernel makes key links lockless, completely doing away with locks in the multiversion concurrency control (MVCC) and write-ahead logging (WAL) modules
                    5. Lindorm has developed Indexable Delta Encoding, which allows quick queries in blocks by index, greatly improving the seek performance. binary search
                    6. Other Improvements
                        Quorum-based writes to automatically avoid faulty nodes
                        Efficient group commits
                        High-performance cache without fragmentation using Shared BucketCache
                        The MemStore BloomFilter
                        An efficient read-write data structure
                        GC-invisible memory management
                        A separated online computing and offline job architecture
                        In-depth Java Development Kit and operating system optimization
                        FPGA offloading compaction
                        User-mode TCP acceleration

    14. 微博基于Flink的机器学习实践
        https://zhuanlan.zhihu.com/p/449209125

    15. cockroachdb 两阶段提交过程 - fleuria
        https://zhuanlan.zhihu.com/p/407170124
        1. comparing cockroachdb transaction with percolator. good writing flow. useful as reference
        2. highlights
            1. crdb 中也同样选取事务第一行使它扮演特殊角色，将 TransactionRecord 保存在第一行的同一 range，使事务中的所有 WriteIntent 指向 TransactionRecord
            2. 当所有 Key 都完成一阶段写入后，就会由 Coordinator 驱动进入两阶段提交的提交阶段：使 Transaction Record 标记为 COMMITTED 状态，作为 Commit Point，可以向用户返回提交成功，随后由 Coordinator 驱动异步地清理 Write Intent
            3. 与 percolator 不同，crdb 作为 Serializable 隔离级别，整个事务只有一个提交时间戳，而非 startTs 和 commitTs 两个时间戳。这种单一时间戳也是 Serializable 在逻辑上的体现：Serializable 等价于所有的事务依次执行，事务的开始和结束在一个原子的时间中完成
            4. 但当 Coordinator 挂掉时，其他访问者若碰到遗留的 WriteIntent，仍可以通过访问者驱动的清理过程使事务正常走完。这里与 percolator 是相同的思路
            5. "每当有写入发生，都会检测当前事务的时间戳是否小于 Timestamp Cache 中该 Key 的最新值。如果存在，则表示当前事务的写入操作会使最近一次其他事务读取到的内容失效。按常规的 Serializable 事务过程的话，到这里就应该宣告事务冲突失败了

                不过 crdb 这里并没有直接事务冲突退出，仍挽留了一把。思路大致上是：当前事务与其他事务发生Write after Read 冲突，我可不可以将事务的时间戳推后（push）到当前时间，再跑一次 Write After Read 冲突检查就没问题了。

                但是执行 Push Timestamp 时也需要满足一定前置，就是当前事务读取的键，在 [原时间戳，新时间戳] 范围内是否存在新的写入操作。如果不幸存在新的写入，就无法挽救了，只能认为事务冲突失败。这项检查称作 Read Refreshing。

                Push Timestamp 相比于直接报错事务冲突然后用户上层对整个事务进行重试，更轻量，也对用户会更友好，我们平时在业务代码中其实很少对事务做重试，挽回一个有救的事务，sentry 上就少一个异常出现。我想这也是悲观并发控制相比乐观并发控制更好的一个地方。"

    16. 2021-12 数据系统小报：Apache Arrow、DuckDB
        https://zhuanlan.zhihu.com/p/447267790
        1. Apache Arrow
            1. Apache Arrow主要设计用来作为内存数据Layout的格式，其主要目的是快速执行各种计算。因此，虽然是一种列式格式，但其很少采用压缩算法，在设计上偏向于可以快速在任意位置存取和实现向量化执行。（从这点来看，其设计思想和FlatBuffer有点接近）
            2. 虽然提供了文件存储和网络交换方面的支持，但是Apache Arrow也并非应用于网络传输（如上所述，其压缩比并不高），因此和ProtoBuf也有所差异。其内存布局的设计主要是方便计算执行，因此具有Cache友好和适于SIMD指令执行等优点
            3. 虽然提供了各种计算库，但Apache Arrow也不是Yet Another MPP框架（区别于Spark/Presto等），它所提供的计算库目前主要运行在单机环境，也并不特别关注并发执行和管理。相反，它提供了非常强大和方便易用的单线程执行工具
            4. Apache Arrow 特别引人注目的一个子项目是Gandiva。这是帮你实现最近特别流行的查询编译功能的工具
        2. DuckDB as SQL engine for Apache Arrow
           https://youtu.be/YhF8YR0OEFk
            1. DuckDB uses Morsel-Driven Parallelism
        3. Processing billions of events in real time at Twitter
           https://blog.twitter.com/engineering/en_us/topics/infrastructure/2021/processing-billions-of-events-in-real-time-at-twitter-
            1. Old architecture - a lambda architecture with both batch and real-time processing pipelines, built within the Summingbird Platform and integrated with TSAR
            2. kappa architecture to process the events in streaming-only mode, batch components and rely on real-time components to provide low latency and high accuracy of data
                1. converged to stream processing via Google Dataflow, query by BigTable
                2. deduping is a concern, from on-premise, to Dataflow dedup window

    17. Anti-Caching 论文阅读笔记 - 李喆
        https://zhuanlan.zhihu.com/p/444397266
        1. Anti-Caching: A New Approach to Database Management System Architecture (VLDB 2013, Brown + MIT)
        2. BufferManager is CPU killer, drop it. Save all data in memory, only "cache out" cold ones. That's Anti-Cache.
        3. 实现 Anti-Caching 的核心操作只有两步：
            1. 把要被排出内存的冷数据 tuple（根据 LRU）聚合成一个 block。
            2. 更新一个内存中的表（evicted table）来跟踪哪些 tuple 被写到了磁盘上。

    18. 内存一致性(Memory Consistency) - Shawn
        https://zhuanlan.zhihu.com/p/422848235
        1. memory operation atomicity
           cache consistency
           memory ordering (visible ordering to self and other threads)

    19. 复旦大学陈平博士：网络攻击猖獗，如何应对数据安全与内生安全挑战？
        https://mp.weixin.qq.com/s?__biz=MzA4ODExNDExNw==&mid=2649984415&idx=1&sn=1b02dd0663398fbf766c63a5b3cabd27&chksm=88283b35bf5fb2234a57749c695b6da518d1543720b1afa4259c72db220d6836a5f7f2218abf

    20. 一文读懂SmartNIC
        https://mp.weixin.qq.com/s?__biz=MzAxMDA1NjMwMQ==&mid=2651773740&idx=1&sn=fc62fcccfa114089730cbdd3cedc33d0&chksm=80ac5c2eb7dbd53819f3b4e35757230d26498017ad0b362d4675b554b16a3cdb89902404a728
        1. useful summary
        2. "0.0 代。具体来说，传统网卡面向的用户痛点包括：

                随着 VXLAN 等 Overlay 网络协议，以及 OpenFlow、Open vSwitch 等虚拟交换技术的引入，使得基于服务器的网络数据平面的复杂性急剧增加。

                网络接口带宽的增加，意味着在软件中执行这些功能会给 CPU 资源造成难以承受的负载，留给应用程序运行的 CPU 资源很少或根本没有。

                传统网卡固定功能的流量处理功能无法适应 SDN 和 NFV。

            1.0 代。在 SmartNIC 出现之前，解决这些问题的方法大概有：

                使用 DPDK 作为加速手段，但处理过程仍然依赖标配（未针对数据传输进行优化）的服务器及网卡，这始终是一个瓶颈，吞吐量性能低下，并且需要大量的 CPU 资源，还是没能节省昂贵的 CPU 资源。

                使用 SR-IOV 技术，将 PF 映射为多个 VFs，使得每个 VF 都可以绑定到 VM。如此，吞吐量性能和 CPU 使用效率确实得到了改善，但灵活性却降低了，复杂性也增加了。并且，大多数 SR-IOV 网卡最多有效支持 1Gb 以太网端口的 8-16 个 VFs，和 10Gb 以太网端口的 40-64 个 VFs。

            2.0 代。而 SmartNIC 的存在能够：

                将 vSwitch 完全 Offload 到 SmartNIC，释放昂贵的 Host CPU 资源，将计算能力还给应用程序。

                可以实现基于服务器的复杂网络数据平面功能，例如：多匹配操作处理、计量整形、流统计等。

                支持网络的可编程性（通过更新的固件或客户编程），即便 SmartNIC 已经被插入到服务器使用。

                与现有的开源生态系统无缝协作，以最大程度地提高软件功能的速度和影响力。

            3.0 代。白盒交换机作为最受欢迎的 COTS 硬件，可以加入 Plugin 轻松实现 SDN 和 NFV 的各种计算及网络功能。"

    21. 2万字|30张图带你领略glibc内存管理精髓 - 雨乐
        https://mp.weixin.qq.com/s/pdv5MMUQ9ACpeCpyGnxb1Q
        1. in detail, full summary, but less thinking and why
        2. highlights
            1. "内存管理" - app self managing, reduce interaction to OS
            2. glibc之内存管理(ptmalloc)
                1. allocation unit is "chunk", linked by free list
                2. different sized chunks are put in fast bin, small bin, large bin, unsorted bin
                   bin chunk size increases by 8 byte, 16 byte, 24 byte, etc
                3. chunk can be split / merged. free does merge by checking adjacent bin
                4. use bitmap to speedup bin checking, to track whether bin is empty
            3. glibc malloc problem: free will NOT return mem to OS. so OOM by OS
                1. solution: tcmalloc
        3. ptmalloc、tcmalloc与jemalloc对比分析
           https://www.cyningsun.com/07-07-2018/memory-allocator-contrasts.html
            1. good article. explains why and does the compare
            2. highlights
                1. ptmalloc adds dynamic arena besides main arena, each arena uses mutex, but threads can use different arena
                    1. 从上述来看ptmalloc的主要问题其实是内存浪费、内存碎片、以及加锁导致的性能问题
                        1. 如果后分配的内存先释放，无法及时归还系统。因为 ptmalloc 收缩内存是从 top chunk 开始,如果与 top chunk 相邻的 chunk 不能释放, top chunk 以下的 chunk 都无法释放。
                        2. 内存不能在线程间移动，多线程使用内存不均衡将导致内存浪费
                        3. 每个chunk至少8字节的开销很大
                        4. 不定期分配长生命周期的内存容易造成内存碎片，不利于回收。
                        5. 加锁耗时，无论当前分区有无耗时，在内存分配和释放时，会首先加锁。
                2. tcmalloc是Google开发的内存分配器，在Golang、Chrome中都有使用该分配器进行内存分配
                    1. TCMalloc是专门对多线并发的内存管理而设计的，TCMalloc主要是在线程级实现了缓存，使得用户在申请内存时大多情况下是无锁内存分配
                    2. 小内存可以在ThreadCache中不加锁分配(加锁的代价大约100ns), 大内存可以直接按照大小分配不需要再像ptmalloc一样进行查找
                    3. tcmalloc也带来了一些问题，使用自旋锁虽然减少了加锁效率，但是如果使用大内存较多的情况下，内存在Central Cache或者Page Heap加锁分配。而tcmalloc对大小内存的分配过于保守，在一些内存需求较大的服务（如推荐系统），小内存上限过低，当请求量上来，锁冲突严重，CPU使用率将指数暴增
                3. jemalloc
                    1. jemalloc最大的优势还是其强大的多核/多线程分配能力. 传统分配器中大量开销被浪费在lock contention和false sharing上
                        1. 引入arena.将内存划分成若干数量的arenas, 线程最终会与某一个arena绑定.由于两个arena在地址空间上几乎不存在任何联系
                        2. 由于arena的数量有限, 因此不能保证所有线程都能独占arena, 分享同一个arena的所有线程, 由该arena内部的lock保持同步
                    2. 作为基础库的ptmalloc是最为稳定的内存管理器，无论在什么环境下都能适应，但是分配效率相对较低。而tcmalloc针对多核情况有所优化，性能有所提高，但是内存占用稍高，大内存分配容易出现CPU飙升。jemalloc的内存占用更高，但是在多核多线程下的表现也最为优异

    22. VLDB'20 Magnet: 领英Spark Shuffle解决方案 - Sovnlo
        https://zhuanlan.zhihu.com/p/397391514
        1. paper: Magnet: Push-based Shuffle Service for Large-scale Data Processing    [2020, 3 refs]
        2. highlights
            1. problem: scale of blocks, scale of connections, Spark Shuffle can hardly handle
                1. note Spark already does multiple rounds of improving, mainly to reduce shuffle spillover file count
            2. Magnet Shuffle Service
                1. magnet shuffle service是一个强化版的ESS (spark external shuffle service).
                   增加了一个额外的操作push-merge，将数据推到远程shuffle服务上. 隶属于同一个shuffle partition的block，会在远程传输到magnet 后被merge到一个文件中
                2. 解决Task Straggler问题 - timeout and stop push-merge, start reduce immediately
                3. Data Skew 问题 - adaptive query execution

    23. Linux内核Page Cache和Buffer Cache关系及演化历史
        https://zhuanlan.zhihu.com/p/429548733
        original: https://lday.me/2019/09/09/0023_linux_page_cache_and_buffer_cache/
        1. 目前Linux Kernel代码中，Page Cache和Buffer Cache实际上是统一的，无论是文件的Page Cache还是Block的Buffer Cache最终都统一到Page上
        2. 是什么原因使得最终这两类缓存“走到了一起”？
            1. read()/write() loads data via buffer cache, but mmap() needs to copy to page cache, so they can map to userspace 
            2. write bypasses page cache, this is causing sync problem, as valid data is in buffer cache
               "同一份数据，可能在Page Cache中有一份，而同时，却还在Buffer Cache中有一份"
        3. related
            1. What is the major difference between the buffer cache and the page cache? Why were they separate entities in older kernels? Why were they merged later on?
               https://www.quora.com/What-is-the-major-difference-between-the-buffer-cache-and-the-page-cache-Why-were-they-separate-entities-in-older-kernels-Why-were-they-merged-later-on

    24. Facebook 十年集群管理系统简述 Twine: a Unified Cluster Management System for Shared Infrastructure [OSDI '20]
        https://zhuanlan.zhihu.com/p/359071322
        https://www.usenix.org/conference/osdi20/presentation/tang
        1. let's read paper later
        2. author's 个人评论
            1. Entitlement（权利） 其实和 Borg (EuroSys'15) 中的 quota 想法在本质上相似。相比同期 Microsoft 的 HiveD (OSDI'20)，其提出的 Virtual Private Cluster 则在此基础上增加了 locality 的要求。
            2. 宿主机配置 和 任务种类 的匹配是一个巨大的矩阵空间，如何找到合适的匹配，本身就是个课题。
            3. Facebook 的小机器在内存方面的缺点值得重视，往往适合计算密集（compute-bound）的业务。对于小机器，Twine 默认不超卖 CPU 和主存，但会对总消耗功率做超卖。
        3. related
            1. 如何评价Facebook在OSDI20发表的Twine和Delos论文？
               https://www.zhihu.com/question/429682314/answer/1574581196
                1. "Twine作为FB的IaaS层，应用已经普及到各大产品线，可以说绝大部分的脸书服务器都运行在这个系统下面。其实Twine本身并没有太多学术上的创新，而可以说是一个工程上的成功 .. 在单一系统规模这个方向，我的理解Twine是工业界领先的"
                2. "当然Twine本身有很多问题，stacking也好，resource isolation也好，可以说落后业界尤其是公有云很多年，这个基本上amazon/microsoft/google相关背景过来的员工都有同感"

    25. 深入理解 TCP 拥塞控制 - 拍乐云Pano
        https://mp.weixin.qq.com/s?__biz=MzU1MjAxNjI0Ng==&mid=2247485554&idx=1&sn=796049052c3c0bbdce51a372323e8a1e&chksm=fb89c86bccfe417d77083e7edd763cf50dea4384f9a56bd0519021a165789552764e71bec54d
        1. useful summary
        2. highlights
            1. "BBR是由Google设计，并于2016年发布的拥塞算法，以往大部分拥塞算法是基于丢包来作为降低传输速率的信号，而BBR基于模型主动探测"
            2. 如何基于WebRTC搭建一个视频会议 - Simulcast和SVC
               https://segmentfault.com/a/1190000022392153
                1. WebRTC，它是由谷歌推广的实时音视频技术栈，是音视频领域搜索热度最高的技术。它有多重身份，既是W3C的标准，也是一个开源项目，还有一个对应的IETF工作组(RTCWEB)
                    1. interesting technology
                2. 这里要借助于两种源端编码策略 - Simulcast和SVC
                    1. "Simulcast：同步广播，指的是同时编码/发送多路视频流，比如常规发送一路720p，外加一路180p的流，这样在SFU下发给接收端的时候，可以根据下行带宽的限制，选择下发不同分辨率的流"
                    2. "SVC：可伸缩编码，使用基于层次的方法，提供时间或空间可伸缩编码组合。在RTC的应用中，通常会选用时域SVC，通过改变帧率来实现伸缩性。SFU可以根据下行的实际带宽，从同一路SVC视频流中解析出不同的时域分层，分别传输给各个接收端"
                    3. "Simulcast和SVC在实际应用中各有优劣，Simulcast多路流的分辨率跨度大，主观体验不佳；SVC的时域分层会影响帧率，容易出现卡顿"
                3. 必须构建一个具备智能调度的实时传输网络
                    1. 分区域/分运营商部署SFU服务器，用户通过接入服务实现就近接入，保障了最后一公里的质量。
                    2. 灵活/按需部署路由节点，通过路由分配服务，能够根据实时网络质量选择最优的传输路径。
                    3. 分布式的SFU更有利于会议方数的扩展和服务扩容
                    4. 需要保障传输s网络内部的数据传输质量，可以尝试QUIC。

    26. HPC：程序优化思考
        https://zhuanlan.zhihu.com/p/438506418

    27. NVIDIA BlueField-3 DPU技术架构分析
        https://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247495357&idx=1&sn=69f0f6ad3eaec36ce0237636d1a940ca&chksm=faa216b7cdd59fa18edcc60fce1e47b7b7fbc94a69c02e7f1a81e7d07cac739f2b4dbb84a5c
        1. 网络：RDMA、连接跟踪（Connection Tracking）、ASAP, GPU-Direct RDMA
           安全：IPSec协议, TLS协议
           存储：块存储（Block Storage）、文件存储（File Storage）、对象存储（Object Storage)或者NVMe存储（NVMe Storage）的仿真
                数据落盘时加解密的操作（如AES-XTS）进行硬件卸载
                BlueField SNAP技术，允许用户访问与服务器连接的远程NVMe存储像访问本地存储一样
        2. 2021中国DPU行业发展白皮书
           https://mp.weixin.qq.com/s?__biz=MzUzMzY1NTkwOQ==&mid=2247495357&idx=1&sn=69f0f6ad3eaec36ce0237636d1a940ca&chksm=faa216b7cdd59fa18edcc60fce1e47b7b7fbc94a69c02e7f1a81e7d07cac739f2b4dbb84a5c3&mpshare=1&srcid=1213e7UAhUgMLewUhxswCpW8&sharer_sharetime=1639409105451&sharer_shareid=ed8ef0470c27695d5b0dab6e155358f0&from=timeline&scene=2&subscene=1&clicktime=1639440428&enterid=1639440428&ascene=2&devicetype=android-29&version=28001057&nettype=cmnet&abtest_cookie=AAACAA%3D%3D&lang=zh_CN&exportkey=AT7JY2u05T8e5GsFtXeyHH0%3D&pass_ticket=S5Ix51s%2F%2BCyEOgIOgDSuba%2ByEZpnNgC87OiiQ7NppfaLpRb07%2FdZ59W4e5vin4ZV&wx_header=1
        3. very interesting new technology. NVIDIA BlueField-3 DPU
           https://nvidianews.nvidia.com/news/nvidia-extends-data-center-infrastructure-processing-roadmap-with-bluefield-3

    28. 给 BI 砍头？聊聊指标平台的崛起
        https://mp.weixin.qq.com/s?__biz=MzkzMTE3Mjc5Mw==&mid=2247483688&idx=1&sn=44108da051d671ecd785409e716cea98&chksm=c26e59fef519d0e8472b897e9f35b3d462cd7bd2532c82d2889a095641ec957abf89f3a3a8a5
        1. good article, new market area
        2. highlights
            1. prior problems
                1. 将指标物化在数据仓库View, massive view needed, hard to debug upstream
                2. 用 SQL 定义指标太复杂，门槛太高
                3. 指标只能 BI 工具中使用，无法对接更多业务系统
                    1. traditional BI, if need to feed into running prod systems e.g. to assign user promotion strategy, the results are not easy to use
                4. 指标定义口径不一致，无法支撑业务决策
                    1. 一个很简单的业务问题在不同团队那里会得到不同的汇报数字。更糟糕的是，没有人知道究竟哪个数字是对的
            2. Headless BI: 指标只需定义一次，就可以统一地在仪表盘，以及自动化工具中使用
                1. 砍掉 BI 的“头”（报表可视化），只保留指标层，通过提供各类消费接口. 可以将指标资产沉淀下来，多系统复用
                2. Airbnb 的 Minerva
                    1. Minerva 会将维度表，度量表作为输入，进行数据反范式化（笔者注：应该是指将数据打平，聚合）并为下游应用系统提供聚合的数据。Minerva 的 API 填补了上游数据和下游消费系统之间的空缺。
                    2. Define metrics once, use them everywhere
                3. 从 Airbnb 出来创业的 Transform
                    1. 专注在 metric store，metric layer 领域的
                    2. 提供一套能将指标和其他企业工具集成的 API
            4. 以开发者为中心的 Supergrain
            5. 从开源项目到商业的 Cube.dev

    30. CPU与GPU之间是如何通信的？
        https://www.zhihu.com/question/22233341/answer/57756944

    31. Linux低延迟服务器系统调优 - 饶萌
        https://zhuanlan.zhihu.com/p/58669088

    32. 金融热点账户的设计
        https://zhuanlan.zhihu.com/p/443014196
        1. 几种方案的对比
            1：并发度控制
            2：汇总明细入账
            3：缓冲入账
            4：子账户拆分
            5：增加硬件处理能力CPU.内存等
            6：内存数据库实时地处理记账,异步入库

    33. Render Graph与现代图形API - litmin
        https://zhuanlan.zhihu.com/p/425830762
        1. Render Graph是近几年流行起来的一种组织渲染管线的架构. 基于整帧的信息验证渲染管线的正确性、剔除冗余的工作、充分利用现代图形API来优化性能
        2. 性能优化总结为以下三点：
            1. Asynchronous Compute：现代图形API提供的多个Command Queue可以实现Async Compute，Render Graph可以自动调度和同步
            2. Resource Barrier：Render Graph可以基于整帧的信息来尽早开始Barrier、剔除不必要的Barrier、合并Barrier
            3. Memory Aliasing：现代图形API使我们可以手动管理内存，Render Graph可以高效的复用内存

    34. 阿里云吴翰清：从技术人转型做产品经理是一种什么样的体验
        https://mp.weixin.qq.com/s?__biz=MzkyMDE0NTYxNQ==&mid=2247510636&idx=1&sn=f8dc49cb703748283d7285fa762d198a&chksm=c195b1ccf6e238daaac4a54afcf6683bbfc7d7a55b47da4646765ca8948b4195dc944778828d
        1. key points
            1. 产品经理最重要的能力叫做定义的能力，究其本质是一种对市场的洞察能力，然后衍生出一个定位的能力。
            2. 产品经理五件事（三定义两关注）：定义市场、定义机会、定义产品形态、关注客户体验、关注客户心智。
            3. 产品和商品的区别：提供了使用价值的叫产品，提供了交易价值的叫商品。商品交易的规模越大，交易的频率越快，这个商品的价值就会越高，或者说它的估值就会越高。
            4. 从产品到商品，要关注定价、营销和运营，并建立渠道。
        2. thinkings
            1. "当技术有稀缺性的时候，它会是一个竞争力。当技术没有稀缺性的时候，它就是一个工作量。"
               "产品经理是通过定位把别人给定死的。"
                1. from the defining, the key value in Alibaba is 业务/经理人/运营, rather than technology
                   technology is only a matter of 工作量, that means long working hours and schedule pushes are inevitable
                2. Ideas are not rare, many people have many. What's rare is who can drive and deliver the complex system.
                3. 工作量 means repeat. the principle of technology dev is don't repeat yourself. If the work becomes 工作量, it's not on right path
                4. the most IT success stories are new technologies open new market area, then more products come to compete. Companies win competitor because of better technology, rather than only by defining product
                    1. is this the diff between 2C companies vs 2B companies, drive by 流量 vs drive by technology?
                5. handling big 工作量, i.e. 大型软件开放, is itself a big technology
                6. "稀缺性" is vague, everything you need to pay a price has 稀缺性. competitive technology 稀缺性 needs to be built, as a competence of product
                7. even compare to US Internet companies, e.g. Facebook, Google, Amazon. Yes they make money by product. but they do top at the technology area

    35. 技术十年 - 虫爸说说
        https://mp.weixin.qq.com/s/ifypkq4tsQb8uuqRUqCXgQ
        1. "内存占用仍然居高不上 .. 在底层API中，即使调用了delete或者free，内存都不会被立即释放给操作系统，而是被放在缓冲区中(这就是内存占用比较高的原因)，等间隔一段时间，才会被操作系统回收，如果想立即被操作系统回收，需要malloc_trim(0)"
        2. 分析和解决问题的能力
           懂的底层API的实现原理，知其然，知其所以然
        3. 架构能力
            "完全搭建一个系统，是在五年前，也就是工作五年的时候，那个时候入职了现在的公司。刚开始要做商业化，什么都没有，所有的都要从0开始搭建。比如一个流量来了，该如何去请求各个业务线，一个广告订单来了，如果能够快速的进入广告系统。那么就需要合理的进行模块分配。

            随着代码写的越来越多，解决问题越来越多，越来越难，设计的模块越来越多，在潜移默化中，架构能力也就有了，在设计一个系统的时候，就开始有前瞻性，考虑解耦，考虑扩展。"

    36. Paper Read：ARIES故障恢复算法 - 温正湖 colleague
        https://zhuanlan.zhihu.com/p/440465035
        Algorithm for Recovery and Isolation Exploiting Semantics(ARIES)
        https://web.stanford.edu/class/cs345d-01/rl/aries.pdf
        1. very good summary. Useful to understand ARIES. The writer has good writing and logic, compared to other paper notes writing at Zhihu
        2. highlights
            1. "意向锁(Intention Lock)，主要针对表级锁，便于处理Table Lock和Row Lock的冲突，比如对某一Row加了X Lock，此时另一个事务需要对Table加上S Lock，本来需要遍历所有Rows判断是否有Row被加Lock，现在则根据Table上是否加了Intention Lock即可。下表为Lock的冲突判断。"
            2. 事务的故障恢复
                1. Shadow Paging
                    1. update on shadow page, switch to page table. commit will flush page
                    2. ETCD底层存储引擎采用了类似实现
                    3. problems:
                        1. 每次Commit会将Page整体落盘，如果包含未Commit事务的修改无法回滚，所以事务的并发粒度只能到Page Level。
                        2. 事务的修改操作会导致Page内的数据不断在磁盘上移动，无法有效利用数据的局部性。
                        3. 对于Page Table的原子修改可能会成为瓶颈。
                        4. Pages垃圾回收的压力，包括成功事务的Old Pages和失败事务的New Pages。
                2. Write Ahead Log
                    1. ARIES使用Page-Oriented Redo Log，在Recover时不需要访问其他Page，拥有很快的回放速度。
                        1. I.e. which page is modified, only which page needs recover touch
                        2. "This is to be contrasted with logical redo which is required in System R, SQL/DS and AS/400 for indexes [21, 621. In those systems, since index changes are not logged separately but are redone using the log records for the data pages, performing a redo requires accessing several descriptors and pages of the database"
                    2. ARIES使用Logical Undo Log，如果使用Physical Undo Log，当Page内有未Commit的内容时，其他事务不能移动这些数据，必须等到Page内的内容被Commit或Rollback。
                    3. Force and Steal
                        1. Redo和Undo分别可以保证Durability和Atomic两个特性。按照对Page刷盘的要求分为两个维度：
                            Force or No-Force：Commit时是否需要强制刷盘，采用Force的方式由于所有的已提交事务的数据一定已经存在于磁盘，自然而然地保证了Durability；
                            No-Steal or Steal：Commit前数据是否可以提前刷盘，采用No-Steal的方式由于保证事务提交前修改不会出现在磁盘上，自然而然地保证了Atomic。
                        为了获取最好的性能，ARIES采用No-Force以及Steal的机制，这样可以给予Buffer Management最大自由度的缓存管理策略以尽可能减少Disk IO
                    4. 目标, 一个好的故障恢复算法最好可以做到以下几点：
                        1. 尽可能简单，如果不够简单，很容易出错，虽然ARIES本身并不足够简单。
                        2. 灵活的存储管理，支持变长数据的存储，所以需要移动数据，垃圾回收，Page还需要Split / Merge。
                        3. Partial Rollbacks，支持回滚到Savepoint而不是完全回滚。
                        4. 灵活的缓存管理，即上文提到的Force和Steal的取舍。
                        5. Recover的独立性，Page-Oriented Recovery保证Page的恢复不受其他Page和Txn的影响。
                        6. Parallelism and Fast recovery，可以快速恢复服务。
                    5. Compensation Log Record(CLR)：回滚Undo时记录的Redo Only Log，避免回滚失败之后重复回滚。
                        1. 事务回滚时, Undo页面并记录伴随的CLR并写到Log里

    37. 网易汪源：我们怎么做开源 - 网易数帆 - 风轻扬
        https://zhuanlan.zhihu.com/p/431495100
        https://mp.weixin.qq.com/s/9eujTFc-MOmB8xbY07-V2A
        1. useful summary about why opensource
        2. highlights
            1. if do not opensource
                1. case 1: rewrite PG database, but cannot port new PG release
                2. case 2: NEMR (NetEase MapReduce), but find Hadoop community is better years later
                           if had opensourced NEMR, it should have taken the eco position
                3. case 3: DDB, earlier than ShardingSphere, but opensource ShardingSphere becomes the public use later
            2. if did opensource
                1. case 1: Spark vs Hadoop MapReduce - 只有开源才能打败开源
                2. case 2: MySQL vs Oracle / DB2 - 开源打商业机会很大
                3. 商业化套件的子产品不开源. i.e. “内核开源”，+ 安全、治理、监控、计量计费等等“企业级”功能
            3. what to opensource?
                1. 核心基础软件. Early Adopter主要是互联网企业, 不开源基本不敢用
                2. 围绕已有开源项目的配套软件，如KubeCube、KubeDiag都是K8S配套软件
            4. Other issues
                1. 防止IaaS巨头薅羊毛
                    1. 原厂的云服务自然是最畅销的。像Spark就和云产商合作的很好，TiDB看起来也不错。当然IaaS巨头的服务也会有市场
                2. 头等大事是经费来源。
                    1. 网易数帆开源项目主要是放在研究院的公技板块
                3. 做好开源项目的管理
                    1. 不要让不好的开源项目损害公司品牌
                    2. 开源项目多了，就要建立开源管理委员会，新开源项目都要经过委员会审议，每年每个项目都要向委员会汇报工作和计划。每个项目的价值也要严格评估，只是不评估赚钱而已，但社区情况、应用情况、影响力情况、技术创新与先进性、团队能力等等都要评估，据此确定预算
        3. related
            1. Envoy 代理开源五周年，创始人 Matt Klein 亲述开源心路历程及经验教训
               https://mp.weixin.qq.com/s?__biz=MzA5OTAyNzQ2OA==&mid=2649739031&idx=2&sn=0899fe0b51af9ce778eb51a2c604be35&chksm=8893f074bfe47962fa226c0976cef982eb61ad49113049631b6fc10510a7a5dc2a3f62fb19c5
                1. very good useful article. there are many experiences to learn from. many are less known missing practices
                2. highlights
                    1. story history
                        1. 根据我的定义，这种类型的项目需要 3-4 个月的时间
                        2. Envoy 从一开始就拥有一流的可观察性输出，以指标和日志的形式
                        3. Lyft 的基于负载的重大事件的数量从每 1-2 周一次慢慢减少
                        4. “胡萝卜”式的迁移几乎总是成功的。而“大棒”式的迁移则很少成功
                        5. 对于 Lyft 来说，Envoy 是一个重要的工程项目，领导层认为，开放源代码将使 Lyft 作为一个工程组织具有可信度，并有助于招聘工作
                        6. 我们在 2016 年夏天花了很大一部分时间来编写文档, 清理存储库，使其“不那么尴尬”，制作网站，发布博文等等. 如果我们要在开源领域有所作为，就必须通过高质量的文档、网站等给人留下良好的第一印象
                        7. 在此期间，我们还利用我们的行业关系，与 Lyft 的一些“同行公司”（湾区的“独角兽”互联网创业公司）会面，向他们展示我们在 Envoy 方面所做的工作，并获得他们的反馈，我们认为如果我们在正式开源前成功获得一个启动合作伙伴，这将是对项目的一个重大帮助。
                        8. 谷歌在发现 Envoy 的时候，正准备在 NGINX 的基础上推出 Istio。一次会议引出了另一次会议，然后是更多的会议，在 Envoy 开源之前，大量的谷歌员工已经看到了源代码和文档。
                        9. 具有讽刺意味的是（至少在 Twitter 的观点中），C++ 在这里是一种帮助，而不是一种阻碍。这些大公司都已经拥有充足的 C/C++ 开发资源，以及他们想要整合的现有库，等等。对他们来说，C++ 是一个卖点
                        10. 到了 2017 年初，很明显，Envoy 的开发正在加速。谷歌(GCP)承诺用 Envoy 取代 NGINX (2015 Autumn entered Lyft production)
                        11. 早期的谷歌云工程师最终成为维护者，Harvey Tuch 和 Alyssa Wilk，为项目带来了大量的人才，包括技术上的，以及对开源和社区的支持
                        12. 捐赠给 CNCF 且感到倦怠. 到 2017 年秋天，Envoy 已经超出了 Lyft OSS 设备所能提供的范围。该项目需要法律、公共关系、营销、活动组织等方面的帮助
                        13. 确保 Istio 和 GCP 团队与谷歌合作的成功之外，我们还花了大量时间与其他公司和维护者合作并加入他们，其中许多人对项目产生了巨大的影响
                        14. 随着项目的不断深入，我开始收到大量投资者对 Enovy 的兴趣。有强烈的愿望让我离开 Lyft，围绕这个项目开一家公司
                        15. 我的第一份工作是在内部领导网络团队，并在运营上支持 Lyft 的 Envoy。我的第二份工作是作为 Envoy 的公众形象，包括 OSS 领导，代码审查，修复错误，编写可以促进项目的功能，在会议上发言，帮助其他公司采用和部署 Envoy，等等。我开始变得过于分散
                    2. 成功的开源软件就像创办一个企业
                        1. 除了核心技术之外，创业还涉及很多因素：
                            招聘（在开源软件中，这意味着招聘贡献者和维护者）
                            获取客户（在开源软件中，这被转化为用户）
                            文档和技术写作
                            公共关系
                            市场营销
                            法律（商标、许可等）
                            人力资源（在开源软件中，这将转化为解决社区纠纷和制定文化）
                            资金（在开源软件中，这转化为辅助费用，如 CI、为维护者找到允许他们在项目中部分或全部时间工作的工作，等等）
                            总的说来，就是领导和方向的确定。资源有限，有很多事情可以做。企业/项目需要专注于最重要的事情，以实现产品的市场适应性。
                        2. 强烈鼓励那些考虑进行大规模开源工作的人提前在上述领域进行投资，以便在第一天就给人留下最佳印象
                        3. 新的开源项目应该准备在项目成长并开始看到采用时，在上述领域进行更多的投资
                        4. 毫不奇怪，这些天我在 Envoy 上做的编码工作相对较少。我在项目上的时间主要是管理项目的所有非技术方面（上述列表中的所有内容，甚至更多！），并确保事情按计划进行。我所做的大多数编码项目都是“清洁”的幕后项目，对项目有好处，但没有什么乐趣，也不可能激励其他贡献者（当然，我对他们每天的工作没有发言权，我有动力让他们尽可能的开心，这样他们就不会离开）
                    3. 终端用户驱动的开源软件是一种结构性优势
                        1. 最初的客户几乎肯定会从软件中获得价值，否则软件就不会得到资助。这种与客户一起建立东西的良性循环是非常强大的。它几乎普遍导致了更好的结果：软件更可靠、更专注、功能更少。有很多由最终用户驱动的开源软件的例子，然后取得了巨大的商业成功。
                        2. 不要跟风，要跟随客户. 不懈地关注客户的实际需求而不是炒作周期所认为的客户需求
                    4. 可扩展性是至关重要的
                        1. 提供一个强大的可扩展性模型，让用户可以满足他们的需求，而不需要将每一个改动和功能都推到上游
                        2. 开源软件的角度来看，失去对项目主要目标的关注会导致功能蔓延、软件无法维护和维护人员负担过重
                    5. 质量问题
                        1. 跟随客户的另一个推论是，质量确实很重要。用户希望软件易于操作，相对来说没有错误，关心安全，等等。曾几何时很多人会觉得因为开源软件是“免费的”，所以质量就得不到保证。这在理论上也许是正确的，但实际上，在一个项目对软件质量认真对待之前，用户不会大量地聚集在一个软件上。因为获得用户是一个飞轮，可以获得更多的用户（特别是当从早期采用者转向晚期采用者时），所以确保为整个软件质量编列时间预算就更加关键了。
                        2. 关于 Envoy，我一直有一个“零碰撞”的理念。任何崩溃都会被调查和修复，无论多么不频繁的错误
                    6. 社区是扩大规模的唯一途径
                        1. 社区是扩展开源软件的唯一途径。这是一个由维护者、贡献者和用户组成的社区。
                        2. 社区的基调在项目开始时就已经确定，而且极难改变。人类倾向于遵循规范。一旦规范被确定下来，无论规范是什么，与这些规范不一致的人都会被避开
                        3. 我在 GitHub 上投入了大量的精力与人们一起工作，使用建设性和欢迎性的语言。总的来说，我尽我所能让 Envoy 成为一个受欢迎的地方，让人们愿意来贡献自己的力量，无论是维护、偶尔的贡献，还是用户帮助其他用户
                    7. 混合商业和开源软件的利益是非常困难的
                        1. 该社区充满了选择在一个共同的基底上合作的公司，即使是通过在扩展/API/控制平面/UI/UX层上的创新，推出相互竞争的上层产品
                        2. 同时又能取得商业上的成功（我认为这对整个项目的成功是必要的，因为钱必须来自某处），那么预先考虑如何将核心层和商业层分开是极其重要的
                        3. 但我相信专注于强大的 API/扩展性的分割是一个富有成效的策略
                    8. 基金会是很棘手的
                    9. 提前考虑治理问题
                        1. 最重要的是，在项目变得庞大和成功之前，先认真思考治理问题。写下一套规则和规范，特别是花时间记录项目的冲突解决过程。
                    10. 对开源贡献的期望是至关重要的
                        1. 雇员应该问他们的雇主，为什么他们要开放源代码？
                        2. 雇主应该问他们的员工，为什么他们要开放源代码？（这个问题的答案和前一个问题的答案不同是完全合理的，但应该在公开场合讨论）。
                        3. 雇员应该问他们的雇主，如果项目成功了，会发生什么？该项目将有哪些资源可用？员工将有多少时间可以在通用的开源软件问题上工作，目的是直接推动项目的发展？
                    11. 代理容易，API 难
                        1. 事实证明，与为 Envoy 发展一个稳定的 API 生态系统所做的工作相比，代理部分（在我看来）相对简单
                        2. 平衡人类和计算机消费的 API 人体工程学，保持不同版本的稳定性，发展 API 以支持其他客户端，如 gRPC，指定协议语义以使 Envoy 能够与数百（可能是数千）个不同的管理服务器对话，等等，都是非常复杂的

            2. 维护一个大型开源项目是怎样的体验？ - 谷歌Keras团队软件工程师 - 金海峰
               https://www.zhihu.com/question/36292298/answer/1985977644
                1. useful as a reference
                2. highlights
                    1. 对工作的影响
                    2. 抢占先机很重要
                    3. 合作才是王道
                    4. 别小瞧任何人或作品
                    5. 运气是不可或缺的
                    6. 上手难度决定用户量
                    7. 好的上层管理也是必要条件

    38. Parquet文件存储格式详细解析 - 大数据学习与分享
        https://zhuanlan.zhihu.com/p/363509988
        1. Parquet仅仅是一种存储格式，它是语言、平台无关的. 将其它序列化工具生成的数据转换成Parquet格式
            查询引擎: Hive, Impala, Pig, Presto, Drill, Tajo, HAWQ, IBM Big SQL
            计算框架: MapReduce, Spark, Cascading, Crunch, Scalding, Kite
            数据模型: Avro, Thrift, Protocol Buffers, POJOs
        2. Difference between Apache parquet and arrow
           https://stackoverflow.com/questions/56472727/difference-between-apache-parquet-and-arrow
            1. Parquet is a columnar file format, space efficient, not for in-memory computing, need full decode before random access.
            2. Arrow is a library providing columnar data structures for in-memory computing
               a Parquet file can be decoded to load into Arrow columnar data structures, for in-memory analytics then
            3. Arrow files defines a binary "serialization" protocol to map Arrow columnar arrays on disk files, and mmap to memory

    39. 高梓尧：生存分析在快手的应用
        https://zhuanlan.zhihu.com/p/448764017
        1. 
        2. highlights
            1. problems
                1. DAU只体现了一定时间窗口内用户留存的结果，而用户行为是随时间推移陆续发生的
                2. 
            2. 生存分析最早被医学领域采⽤，研究病⼈从诊断出癌症后使⽤不同药物治疗后的死亡时间
                1. sounds like exponential distribution used in durability
            3. outline
                1. 开始事件：某用户上次使用快手app的时刻
                2. 结束事件：该用户再次使用快手app的时刻
                3. 删失状态：上次使用后，在观测期间再没有访问过
                4. 生存函数：截止某时刻，该用户仍未再次访问的概率
            3. use cases
                1. 用户活跃度分层和聚类
                2. 利用生存曲线进行防流失干预
                3. 推荐策略的优化
                    1. 根据各特征边际贡献的平均值排序，有针对性地调整召回和索引的相关策略，并优化推荐模型在粗排或者精排阶段的不同特征的权重
            4. KwaiSurvival - 快手自主开发的基于深度学习的生存分析模型, 已开源

    40. 分布式链路追踪在字节跳动的实践
        https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzI1MzYzMjE0MQ==&mid=2247490822&idx=1&sn=77e37f8b6f649774fe5da3458210a488
        1. good as compared to our implementation, and as a reference design. Transaction Trace, Semantic definition, sampling policies, query & indexing, multi-datacenter architecture.
           it does need dedicated storage and query processing hardware resources.
           the key driver is it has massive thousands of micro-services to monitor
        2. highlights
            1. Trace - linked tree structure of logs, can be visualized. too many micro-services.
            2. goals
                1. unified modeling and semantics. open and extensible. SDK 一站式
                2. 中心化配置管控：中心化动态管理采样、染色、自定义索引、熔断限流、索引、脱敏保密等各类策略。
                3. low overhead. balance storage and search indexing. Disaster Recovery at multiple datacenters
                4. minimal dependency to 3rd party, and architecture complexity
            3. solution
                1. Span, Event, Metric (tagged value), Trace, Transaction
                2. 语义规范: Service, DC, IP, Pod, Env
                            Method, code line, Target service, status code, Error, Latency, Size
                3. 采样策略
                    1. Based on LogId, sample by probability. Run full sampling for low frequency logs in periodical window
                    2. dynamic sampling rate based on changing QPS
                    3. 染色采样：对特定的请求添加染色标记，SDK 检测到染色标对该请求进行强制采样。
                    4. PostTrace 后置采样: 当一个 Trace 一开始未命中采样，但在执行过程中发生了一些令人感兴趣的事（例如出错或时延毛刺）时，可以在 Trace 中间状态发起采样。相较于先全采再后置采样，此方案开销极低。
                4. dedicated messaging queue, trace consumer, and LogStore, and query processor
                5. multi-datacenter: Cell architecture. LogStore is at local DC, query service is at 汇聚机房（同时在主机房部署备用查询节点）
                   query goes to all DC and aggregate results
                6. 全链路实时监控
                    1. 支持从任一微服务节点发起拓扑查询，实时观测各节点的流量/延迟/错误率/资源使用率/告警/变更等，快速从全链路视角获取整体状态信息
                    2. 活动大促全链路容量预估
                        1. 产品估算DAU -> 估算入口服务QPS增量 -> 估算全链路各环节QPS增量与容量需求
                    3. 故障来源与影响面分析

    41. 浅谈Hot Chips 2021 - 青031
        https://zhuanlan.zhihu.com/p/403881866
        1. good. this year's Hot Chips is very impressive. "总的来讲，这两年的计算机体系结构又来到一种百花齐放、百家争鸣的时代. .. 很明显，摩尔定律是在加速而不是停滞"
        2. highlights
            1. Intel Alder Lake 放弃了同构CPU核的设计, 转向了大小核
                1. 这个趋势对于很多AI芯片创业公司来说可能不是好消息：超大算力的AI训练集群，有能力的大公司都倾向于自己建设，比如谷歌TPU、特斯拉D1等，没能力的小公司都倾向于直接用英伟达GPU，毕竟插上卡就能跑，软件栈都是现成的；如果中小算力的AI场景再被CPU侵占，AI芯片创业公司可能真的到了生死存亡的时刻了
            2. AMD Zen 3
                1. Compared to Zen 2, 微架构层面的改进让IPC提升了19%
                2. 每个核的L2到L3支持64个Outstanding Misses，L3到Memory支持192个Outstanding Misses
                3. 3D V-Cache，L3的总容量达到惊人的192MB
            4. IBM Z
                1. 每个核有32MB私有的L2 Cache，这些L2 Cache合到一起就组成了整个Chip的Virtual L3 Cache
                2. 不同Chip的L3 Cache还能合到一起，组成Virtual L4 Cache
                3. Systolic Array，算力大于6 TFLOPS/Chip。不过，不同Chip组成了Socket之后，这些AI加速器是可以联动的

    42. 必须了解的mysql三大日志-binlog、redo log和undo log - 夜尽天明_
        https://juejin.cn/post/6860252224930070536
        https://zhuanlan.zhihu.com/p/400965090
        1. useful summary

    43. 在工业界和学术界中数据库的研究热点是什么？
        https://www.zhihu.com/question/318554064/answer/2093670308 
        1. one size can fit all or not - AP/TP 分离和融合
        2. ai for db/db for ai
        3. 安全数据库 - Building Enclave-Native Storage Engines for Practical Encrypted Databases
        4. 其实只要看看这两年的数据库顶会大家的工作都集中在什么方向，各个方向投稿数量就能一定程度的知道业界学界都在做什么，关心什么
            1. 差分隐私
            2. 图计算
            3. Data Streams数据库
            4. Persistent Memory

    44. 软硬件协同设计的一点思考和展望 - cloudcore
        https://zhuanlan.zhihu.com/p/397697428
            1. 软硬件的技术隔阂比我想象更深
                1. 碰到的第一个问题：一些硬件功能，设计时就没仔细考虑软件用法
                2. 第二个问题，编译器的后端优化自动化程度还远远不够，非常费时费力
                3. 第三个问题，就是硬件建模还是有很多看不清的工作量

    45. 特征平台（Feature Store）综述：序论篇 - 曾中铭
        https://zhuanlan.zhihu.com/p/406897374
        https://zhuanlan.zhihu.com/p/406962315 - Feast
        https://zhuanlan.zhihu.com/p/410767474 - Tecton
        https://databricks.com/product/feature-store?itm_data=product-link-featureStore - Databricks Feature Store 
            1. 开源Feast——第一个提出Feature Store概念的平台后
            2. goals
                1. 特征管理：特征抽取、处理、存储、元数据管理，以便于特征溯源、分享、复用
                2. 特征消费服务：为线上部署的模型，提供高吞吐、低延迟的特征获取能力
                3. 离线/在线特征一致性保证：避免Training-Serving Skew问题导致模型效果劣化，详细见之前的文章《AI算法模型中的特征穿越问题：原理篇》、《AI算法模型中的特征穿越问题：工程篇》
                5. 便利：易用、简单的交互和API
                6. 自治：特征回填、数据质量监控、联动模型效果评估等
            3. 元数据管理，Feature训练和生成，数据存储，缓存层

    46. 许中兴博士演讲：Fuchsia OS 简介完整实录及幻灯片下载 - 聞其詳
        https://zhuanlan.zhihu.com/p/55690708
        1. key designs
            1. 原⽣进程沙箱
            2. 在Fuchsia⾥，没有全局根⽂件系统. 没有file. ⽤namespace来定义⼀个进程能够访问的资源
            3. 微内核
        2. Fuchsia在各个平台上的可能的优势
            1. 在服务器平台上，原⽣的进程沙箱机制将带来新的安全特性和容器机制
            2、 在桌⾯平台上，类似于游戏3D引擎pipeline的图形栈以及毫⽆遗产负担的实现将使电⼦娱乐应⽤变得更为⾼效；⽆缝兼容庞⼤的Android⽣态
            3. 在移动平台上，系统的模块化⽅便第三⽅设备⼚商的全⾯定制，驱动框架⽅便硬件⼚商编写和维护私有驱动

    47. 美团MySQL数据库巡检系统的设计与应用 - bluesky
        https://zhuanlan.zhihu.com/p/422409005
        1. DB smoking test.
            1. 最早的巡检是由中控机+定时巡检脚本+前端展示构成的
               problems: 单点，分散无法统计，没有标准，重复开发接口
            2. 数据库巡检重点关注以下几方面进行检查：
                1. 数据库环境，如操作系统资源、操作系统配置、数据库软件版本等。
                2. 数据库配置，如数据库参数配置、redo日志配置等。
                3. 数据库资源，主要分为空间资源（如表空间、归档空间、闪回空间、备份空间）、内存资源、进程资源等。
                4. 数据库对象，如大表、大索引、无效对象是否合理等。
                5. 数据库安全，如是否存在超级权限、弱口令用户等。
                6. 数据库性能，主要分析数据库性能的变化趋势及发展规律等。
                7. 数据库灾备，主要分析数据库灾备是否运行正常。

    48. 多人协同编辑技术的演进 2021-10-24 - pubuzhixing
        https://zhuanlan.zhihu.com/p/425265438
        1. 协同编辑冲突处理 - 系统不需要是正确的，它只需要保持一致，并且需要努力保持你的意图。

    49. 云数据库与日志复制 - 华莱士的老朋友
        https://zhuanlan.zhihu.com/p/425491910
        1. PolarFS: 这个 WAL 会通过 Raft 协议和其余两台机器上的 Chunk 副本组成一个 Raft Group，同一个盘上的 WAL 会写入 SSD 特有的 3DXPoint SSD buffer，这个高速缓存可以把单次写 WAL 的延迟降低到最低 10us 并且还能保证数据不丢失
           to ChunkServer； 这意味着用户的一次更新可能会造成 （2 * 3 + 2 * 3）次 IO。 ... Avg should be less, as a page can merge many writes
           而是让计算节点直接将 data page 写入到存储节点
            1. PolarFS 为何不为 redolog 这样特殊的文件准备单独的接口，这样的话可以省略 apply 本身的一次 IO
        2. Aurora 的每一笔事务会把 MTRs 的修改 redolog 记录发送给不同的 segment。然后等待所有的 segment 都写入成功后返回成功

    50. 揭开高频交易巨头的神秘面纱: Latour Trading - Quan
        https://zhuanlan.zhihu.com/p/138023466
        1. 在2018年总利润达4.76亿美元，人均盈利是3千3百万美元，资金回报率高达1400%

    51. HiPress：梯度压缩感知的高性能数据并行分布式深度学习框架 - Orange Lee
        https://zhuanlan.zhihu.com/p/426472894
        1. 但我们发现梯度压缩技术在实际深度学习系统中的应用远不如预期，因为该技术在实际系统中面临着两点挑战：
            1）梯度压缩相关的计算开销不可忽略，由于现有传输框架的设计问题，导致梯度压缩相关的计算开销未被隐藏在网络传输过程中；
            2）梯度压缩算法的实现、优化、系统集成等过程给算法使用者带来沉重的负担，并且，开源的梯度压缩算法和系统的联合实现往往性能比较差

    52. DPU新范式: 网络大坝和可编程存内计算 - 扎波特的网线钳 zartbot
        https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzUxNzQ5MTExNw==&mid=2247486644&idx=1&sn=a2a18f661c18bfb96a37d5ac0d1a9653
        1. NetDAM
            1. 传统的冯诺依曼架构中，计算单元和存储单元是分离的，因此大量的数据流动产生了内存墙和冯诺依曼瓶颈
            2. 文章中我们比对了主机内各种通信总线(PCIE/CXL/CHI/AXI)和主机之间的通信协议(以太网、RDMA),
               得出结论需要在网络侧直接添加内存，并提供可编程的指令集实现SIMD访问和计算加速，
               这种做法对硬件和软件都非常友好，测试结果显示NetDAM网卡平均读延迟仅618ns，抖动39ns，远低于当前的RDMA实现

    53. SIGMOD21 ArkDB: A Key-Value Engine for Scalable Cloud Storage Services - Simpo
        https://zhuanlan.zhihu.com/p/414054332
        1. so .. how to do 范围查询?
        2. highlights
            1. ArkDB建立在盘古(一个append-only的分布式文件系统)
            2. 原始的Bw-tree使用8字节的逻辑页面id, ArkDB使用物理页ID (PID)，由(ExtentID, Offset, PageSize)表示

    54. FAST21 Rethinking File Mapping for Persistent Memory - Simpo
        https://zhuanlan.zhihu.com/p/415243922
        1. PM上的文件系统在实际工作负载上花费高达70%的IO路径执行文件映射(将文件偏移量映射到存储介质上的物理位置)
           设计了HashFS，一种基于哈希的文件映射方法。HashFS对所有映射和分配操作使用单个散列操作，绕过文件系统缓存，而是通过SIMD并行和显式缓存转换来预取映射
           HashFS将LevelDB上YCSB的吞吐量提高了45%
        2. prior arts
            1. Extent Tree
            2. Radix Tree
        3. PM-specific Global File Mapping
            1. Global Cuckoo Hash Table

    55. 阿里巴巴CTO独家自述：CTO就是要给CEO扫清障碍和风险 - 程立
        https://mp.weixin.qq.com/s?__biz=MjM5ODIzNTc2MA==&mid=2660857266&idx=1&sn=8df199f5adab4671dad54da9e6c247fb&chksm=bda00ead8ad787bb9ed656f5105e652e5c3543253a65a77bf074cfae9c123ea4702f8708d0bb
        1. summarize history of the author, Alibaba, and Ant. proposed key leadership abilities, CTO responsibilities
           very good article for thinking how to work on the large corporation scale
           and the author is very frank, wrote many detailed history, thinking, and decision making stories.
           they are accompanied with realworld production examples and experiences
        2. highlights
            1. 于是，2013年我开始带支付宝整个技术团队，经过一年的考察，在2014年公司任命我为蚂蚁CTO，2014年到2019年我一直在这个岗位
            2. 我挑了几个蚂蚁CTO工作的节点，非常好地印证了“商业和技术的共同进化”
            3. 未来我们更像一家银行，还是更像一家互联网公司？我们判断未来必须要用互联网架构去解决支付相关的问题。于是决定把系统做一个面向未来的架构设计：分布式改造。整整一年时间，我们将核心交易、核心账务、核心会员、核心支付，全部分布式化。
            4. 2020年，我已经是阿里巴巴集团的CTO了，我们完成了上云的封顶，所有核心业务基本都跑在云上，包括最具挑战性的业务，比如搜索、推荐、广告业务，云都能支撑
            5. 不同业务阶段下的三种技术领导力
                1. 俞永福: 企业发展就是这样波浪式的发展过程：一开始要先找到一个方向，进入一个业务的轨道;如果这个方向判断准了，企业就会进入快速增长阶段；发展到一定阶段，就必须要脱离现有的惯性，再去找新的发展方向——就是这么一波波的过程
                2. 在波浪式发展过程中，技术在每个阶段起的作用不一样。
                    1. 在入轨的阶段，CTO应该是整个公司业务一号位班子的成员，是支持一号位的二号位，班子一起看清方向，把业务带入正轨
                    2. 一旦入轨之后，业务进入快速增长期，CTO的核心不是看方向，而是怎么做好技术，这时首席架构师会变得非常重要，技术让业务更高速增长、加速成长，业务不要被技术拖慢增速
                        1. 同时，组织设计在这个阶段和技术架构一样重要。
                        2. 然后不能等到业务停滞时才去判断未来，CTO要提前判断未来会发生什么，第二曲线是什么，设计一条未来的路线
                    3. 整体上组织需要有两种领导力:一、专业的领导力：CTO、首席架构师、技术总监和VP；二、组织设计的管理领导力。
                        1. CTO在不同时候戴着不同帽子，有时会承担一个专业角色，有的时候会承担一个管理的角色，有的时候会承担一个战略的角色
            6. CTO的职责
                1. 建立商业与技术的“共振”连接
                    1. 前面讲到商业和技术是共同进化的，而共同进化的过程中两者要发生很好的共振连接
                    2. CTO要和CEO问清楚几个框架性的问题:一是我们公司服务谁，要把客户定义的非常清楚；二是我们为这些客户创造什么样的核心价值、差异化价值；三是我们的商业模式，用什么样的商业模式实现核心价值；四是为了实现这样的商业模式，我们需要什么样的能力、走过什么路径、构建什么样的组织。
                        1. 把这些问题理解清楚之后，技术就能理解业务要干什么了。
                2. 一张图、一场仗、一颗心，愿景牵引前行
                    1. 牵引团队往前是非常有挑战的事情
                    2. 我在团队里建立领导力的方式，是跟团队一起定义非常清晰的目标
                        1. 我觉得信任是要靠跟大家一起把事情做成，甚至没有必要让大家建立起对领导者的认同，就看大家能不能相信共同的目标，并把目标实现
                3. 关键决策，扫清前进中的障碍
                    1. 在蚂蚁做CTO时，第一个关键的决策是技术架构往金融方向还是互联网方向?最后决策是互联网。
                        第二个关键决策是关于OceanBase的转型
                        1. 当时我们采用了什么办法呢?第一先了解清楚OceanBase能干什么;第二，既然公司整体不能做，就搞一个小场景，在蚂蚁的核心交易里切了1%的流量给OceanBase，让它在1%流量里证明能力。OceanBase也很珍惜这个舞台，撑住了1%的流量，最终在这一年完成了从非关系型数据库向真正关系型数据库的转变
                    2. 后面几个决策也类似，作为CTO如何拿捏好风险和稳定，是非常关键的。
                        1. 比如余额宝上线的第一天我们就知道这个产品一定会成功. 一个月时间迅速就把原来准备的系统容量全部用掉了。
                           我们自己还好，因为蚂蚁的平台已经完全分布式化了，可以快速扩容。
                           但我们的合作伙伴天弘基金，因为老系统无法支撑余额宝这么快速的增长，扩容成了核心难题
                            1. 非常重要的决定:把天弘的系统搬到云上，用分布式架构重写一遍，三个月内必须完成。这件事也证明了金融云的价值，金融云的业务也就起来了
                    3. 应对风险，化危为机
                        1. 公司的技术风险有几类。
                            1. 第一类，技术架构不能够支持业务发展，这是业务不能接受的风险。
                                1. “去IOE”
                                2. “双11”大促被我们称为“人肉云计算”
                            2. 第二类风险不是技术架构的问题，而是稳定性出现重大问题。
                                1. 蚂蚁的“527”光纤被挖断
                            3. 第三类风险，可能是CTO和CEO都最担心的，一个新技术出现之后会不会颠覆原有的业务模式。
                                1. 蚂蚁面对移动互联网时代时，我们有一段时间很担心，通过好几年努力定义移动支付，基本上算是渡过这个危机，但当时对蚂蚁的挑战还是非常大的。
                                   当比特币开始成为一个现象时，我们也是非常担心的：它会不会把支付完全颠覆了？
                                   2019年6月Libra出现，更让人担心了:全球支付会不会被一种新的货币重新定义，这是一种降维打击。
                                2. 这时候CTO必须要站到一号位班子里去，帮助CEO做判断。
                                    1. 每一次对未来危机的判断，都可以触发未来新的商业机会。
                                    2. 大的策略是:面对任何技术风险不能只是看，要亲自去试，需要公司投入一些有价值的浪费。
                            4. 第四类风险，是温水煮青蛙。技术会不会反过来伤害公司，它不像风险那么直接，但是如果因为技术、架构或组织问题让公司效率变慢了
                                1. 阿里巴巴的中台就是一个很好的例子, 中台的优点在于可以减少很多重复建设, 
                                   我需要跟这么多中台打交道，需要他们去支撑我，过程中如果有任何一个中台支持不能到位，我的业务可能就做不成
                4. 组织设计与治理——平衡秩序与创新
                    1. 一个人当CTO的时间越长，专业能力下降得就越严重。我判断自己的专业能力大概每隔两年会降一级。
                       也有好处，你可以跟团队一起做，团队会更强。
                    2. 阿里巴巴围绕技术的组织，是有两条线的
                        1. 一条线是实的管理线，是分层分布的
                            1. 前台，面向业务的，为客户赢;中台，是能力中心，中台的客户是前台，让前台更加高效，让前台更有竞争力；底层后台，是强调技术先进性的，确保业务永续
                            2. 这个组织每一层都是独立的业务经营单元，现在我们在做一件事情，让每个独立的业务经营单元都有CTO。这个CTO会对这个业务经营单元负全责
                            3. 实现管理机制的核心就是把每一层之间的界面定义清楚
                        2. 但又带来了一个新问题，我们该统一发展的技术怎么形成合力，所以我们有另一条虚线:技术委员会
                            1. 下设二三十个核心的技术小组，把所有的共性领域横向拉通。通过技术委员会和技术小组的专业领导力，实现策略通、人才通
                            2. 这条虚线会转化成实线的管理决策，我们必须要打通这个链路，这个体系的运作会比较有挑战
                    3. 凝心聚气、薪火相传
                        1. 三年前定下阿里巴巴技术的slogan叫“技术创造新商业”，再之前的slogan是“技术拓展商业边界”
                           除了slogan，阿里巴巴的技术文化底色是务实
                        2. 这些文化、愿景能不能在一个大的场景里形成共识，尤其这个组织每年都有人离开、有新同学进来，还能保证一致的文化，其实是非常有挑战的
                5. CTO可能不是思想家，但一定是行动派
                    1. CTO的六步曲
                        1. 跟团队先一起定义好目标，先一起做成一些事情。
                        2. 多了解团队、了解业务，知道未来要去哪里，跟团队一起共创一个愿景，把大家热情点燃。
                        3. CTO的一个核心工作，是怎么能够让自己不要成为团队的天花板，而是把自己当成团队的地板，用人做事。
                            1. 如果CTO是公司技术天花板的话，那你把公司技术就压在一定的高度和范围内，公司技术永远是在一个小的、狭窄的领域。
                            2. 当CTO的技术能力是公司的地板时，公司可以通过新同学扩展边界。
                            3. 成为CTO还是用人做事为主，而不是做事用人为主。
                        4. 一切都很好时，别忘了晴天去修屋顶，永远居安思危。一旦危机出现，乐观地看待，每个危机背后都有机会，转危为机。
                        5. 过程中不只看当下，也要布局未来，为公司建立技术纵深。
                            1. 在业务发展早期，技术的纵深就是一个点。
                            2. 当发展到像阿里巴巴现在这个规模时，技术纵深就是一个多面体，必须有充分的、多面的布局，才能支撑一个大公司的发展。
                            3. 决定布局投入多少，要和CEO充分对焦。
                        6. 最后一点，人才。薪火相传，人才才是公司未来发展的关键。
                            1. 什么是一家公司技术的最高境界，就是谁来当CTO都能当好
                6. 如何发展与培养CTO
                    1. 每个经营单元要有一个小CTO，这个CTO怎么培养？基本上我们让他在战场里去练，为他设计发展路径
                    2. 当然最难的事情就是培养接班人, 我有两个小经验
                        1. CTO发展是“Z”字型的路线
                            1. 直线成为CTO的人，往往会因为路径太单一、没有足够磨炼而出问题。行癫负责过淘宝的业务，负责过B2B业务，再做阿里巴巴的CTO，再做阿里云的总裁。
                            2. 我做过蚂蚁的技术，做了两年蚂蚁国际业务，再做阿里巴巴的CTO。做过业务再回头看技术，跟CEO对话会有共同的框架，这一点很关键
                        2. 做“L”型职责设计
                            1. CTO最怕做虚了，毕竟这是公司里非常高的位置，每件具体事情都有相应的核心骨干帮你负责，但你手不伸下去就很容易做虚
                            2. 阿里巴巴怎么解决这个问题呢？就是给CTO一横一纵：横向管理的CTO，也给你一个纵向的业务技术一号岗位，保持与一线的对接
                                1. 我现在既是阿里巴巴集团的CTO，又是菜鸟的CTO。
                                2. 行癫也曾经既是阿里巴巴的CTO，也是阿里云的CTO
                        3. CTO应该具备怎样的特质？每个CTO都有不一样的风格，但有几点是共通的:
                            1. 一是要求真务实，真正“No Data No BB”，永远不是高高在上地做决定，而是做决定时能够看得到下面，这很重要;
                            2. 二是要有担当，在做关键决策时敢负历史责任，有进取心;
                            3. 三是必须时时自省和开放。如果不具备自省和开放的能力，是很难去进化的;
                            4. 四是一个大组织和大业务的CTO要有全局观，能够做架构，能把各方面、各种信息形成一张大图

    56. 如何评价Google的GShard论文？ - 袁进辉
        GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding
        https://www.zhihu.com/question/404721763/answer/2111040851
        1. 我们总结一下： 
            1，所有这些工作的目的都是提供一个与编程语言”类型系统“类似的annotation 体系，这个体系需要最简且完备，这个体系定义了”自动并行“的搜索空间。
            2，搜索空间中的任何一种构型，也就是任何一种并行策略，在数学上都是正确的，它们的区别仅仅是执行效率不同，我们目的是找到效率最高的并行策略。
            3，框架需要这样一种能力，给定任何一种构型，都能翻译和转换成一个物理图（执行计划），确保这个并行策略可以成功执行，即使它的效率不高。
            4，框架最好能够自动搜索到效率最高的那个构型。

    57. 盘点来自工业界的GPU共享方案 - 阎姝含
        https://zhuanlan.zhihu.com/p/398369404
        1. very good summary. key GPU virtualization competitors and their key bottlenecks
           authors are commenting in the article
        2. highlights
            1. Antman
                1. need to hook in framework, cannot accurately limit resource
            2. CUDA劫持: rCUDA, vCUDA, 腾讯 GaiaGPU, 百度 MPS+CUDA Hook的GPU隔离, 爱奇艺 vGPU, 第四范式 OpenAIOS vGPU, 趋动科技 OrionX
                1. CUDA lib upgrade breaks the hijack
                2. vCUDA通过劫持CUDA的显存申请和释放请求，为每个容器管理它的显存使用量，进而实现了显存隔离
                3. 和阿里Antman[18]相同地，第四范式vGPU通过Nvidia UVM实现了虚拟显存
                4. 趋动科技在AI算力资源池化解决方案OrionX中实现了GPU共享的能力[17]。在资源隔离方面，使用了CUDA劫持的方案，通过MPS以及其他方式限制算力。OrionX中也包含定制的device plugin和调度器方案，亦无开源
            3. CUDA聚合: Nvidia MPS, 百度 MPS+CUDA Hook的GPU隔离, AWS aws-virtual-gpu
                1. 错误相互影响 as sharing same kernel, no isolation
                2. AWS提供了一套非常简单的GPU共享方案[15]，该方案通过tensorflow框架的参数per_process_gpu_memory_fraction实现了显存隔离，通过MPS的CUDA_MPS_ACTIVE_THREAD_PERCENTAGE实现了算力的限制. 显然是个玩具之作
            4. 内核劫持: 阿里cGPU, 腾讯 qGPU
                1. OS dependency. cGPU实现了一个内核模块cgpu_km
                2. cGPU目前不能中止已经发送到GPU上的请求
                3. qGPU效仿Nvidia vGPU在必要时context switch，实现了强算力隔离
            5. Mdev框架
                1. no container
        3. related
            1. 陈飞: 同样的API劫持，rCUDA、vGPU、爱奇艺、趋动科技OrionX等 是不一样的。
                rCUDA和趋动科技的OrionX是一类，vGPU（包括腾讯、滴滴、爱奇艺、百度、第四范式）是另外一类。
                前者是跨进程、跨节点的思路，后者是同一个进程的内部API劫持。两者的难度、设计思路、产生的效果差异巨大。例如
                    （1）前者是虚拟化（共享仅仅是其中一个容易想到的case），而后者只能做共享。后者的思路由于必须是同一个进程，所以天生是不能跨OS（例如虚拟机、跨物理机），只能在容器这种本来就是进程级别的环境下共享。
                    （2）后者不能把一个GPU切分成多个虚拟GPU的。
                共享不等于切分，共享允许多个进程使用一个物理GPU，但是不允许一个进程把一个物理GPU当作几个虚拟GPU来用。 
                而前者是可以对GPU设备进行模拟，所以可以把一个物理GPU模拟成多个虚拟GPU，包括把多个跨物理节点的物理GPU进行聚合。
                在虚拟GPU的过程中可以对通讯、任务、多任务的行为进行优化。

    58. CockroachDB: The Resilient Geo-Distributed SQL Database - henry liang
        https://zhuanlan.zhihu.com/p/406235686
        1. similar content with CockroachDB paper
        2. highlights
            1. key features
                1. cross region transaction, serializable, highly optimized
                    1. Write Pipelining
                    2. Parallel Commit
                    3. 放弃了对SI的支持
                2. optimized query optimizer and execution engine
                    1. Cascades optimizer, transformation rules
                3. online schema change / backup and restore / fast import / JSON support
        3. related materials
            1. CockroachDB's Query Optimizer (Rebecca Taft, Cockroach Labs) - CMU Database Group
               https://www.youtube.com/watch?v=wHo-VtzTHx0

    59. Bookeeper:scalable,fault-tolerant and low latency storage service optimized for real-time workloads - KDF5000
        https://zhuanlan.zhihu.com/p/406707117
        1. writing log entries. initially for HDFS namenode. Now anything append-only.
        2. Ledgers, Bookies, Ensemble. 每个fragment包含了一组连续的entries
        3. related materials
            1. BookKeeper 原理浅谈 - Matt's Blog
               https://toutiao.io/posts/c4616n/preview

    60. Implementing Linearizability at Large Scale and Low Latency - 暗淡了乌云
        https://zhuanlan.zhihu.com/p/412627137
            1. Reusable Infrastructure for Linearizability（RIFL）
               Implementing linearizability at large scale and low latency

    61. 字节跳动是如何落地微前端的
        https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzI1MzYzMjE0MQ==&mid=2247490310&idx=1&sn=99ed45de3749cc8077bcebf4103f4a08
        1. 微前端 - 前端的微服务，i.e. 小程序？ Even Photoshop is web online now ..
            1. 能用 Web 技术实现的应用，最终都会通过 Web 来实现
            2. 在近几年涌现了一大批之前只能在传统 PC 软件中才能看到的优秀产品，例如：Photoshop、Web Office、Web IDE
            3. separated repo vs central repo
                1. Main App + 子系统间的开发、发布从空间上完成隔离
                2. not iframe => Garfish 在 Runtime 层: Loader, Sandbox, Router, Store
        2. related materals
            1. qiankun（乾坤）微前端 Micro Frontends
               https://github.com/umijs/qiankun
                1. Techniques, strategies and recipes for building a modern web app with multiple teams using different JavaScript frameworks
            2. 爱奇艺号微前端架构实践
               https://github.com/itgoyo/TelegramGroup
                1. 爱奇艺号技术团队基于Vue定制开发了微前端框架

    62. 国内稳定性领域知识库，降低知识获取门槛
        https://r.coding-space.cn/r/5861
        https://github.com/StabilityMan/StabilityGuide
        1. very good stuff. somehow really build the category of this

    63. 《解构领域驱动设计》第一章 - 我是张逸
        https://mp.weixin.qq.com/s?__biz=MzA4NTkwODkyMQ==&mid=2651257296&idx=1&sn=7273271d15bc7e2e41da58a155c6e4ab&chksm=84229506b3551c10f20437b06e0e2fb75c1cb0642d5571ea0b30f534a9000b7bb4f2946a393c
        https://mp.weixin.qq.com/s?__biz=MzA4NTkwODkyMQ==&mid=2651257414&idx=1&sn=cb00177be8aa338b5021d5bb87542088&chksm=84229690b3551f86f39f26f2276028bf379b248ebc9ca857900e09b7d1cfd60e92f7101e17e9
        0. compared to object-oriented design, OO makes an web, DDD requires connections to be encapsulated into domains
        1. 核心子领域，通用子领域，支撑子领域
           限界上下文和上下文映射
           问题空间，解空间
        2. 领域建模就是要从这些纷繁复杂的领域逻辑中寻找到能够表示项目管理领域的概念，对概念进行抽象，确定它们之间的关系
        n. related materials
            1. 领域驱动建模与面向对象建模的差异
               https://mp.weixin.qq.com/s?__biz=MzA4NTkwODkyMQ==&mid=2651257117&idx=1&sn=6fc27e8bc354a4c9bced0398820ce994&chksm=842295cbb3551cddb96245827f2c35f29d05efb65c9c8c43593bde7d31d57038c36959583215
                1. 限界上下文要求内部领域模型保持独立，避免出现跨限界上下文之间领域模型的直接引用
                2. 至于聚合之间的协作，社区的大多数声音认为：聚合之间需通过根实体的ID建立协作关系
            2. 验证限界上下文的原则
               https://mp.weixin.qq.com/s?__biz=MzA4NTkwODkyMQ==&mid=2651257651&idx=1&sn=e7199adb9cfeedfadb7a50c09ed437dc&chksm=842297e5b3551ef339cef0caacb677399a1034967c50ba8329f7287611e1390711ada7478517
                1. 限界上下文存在正交性
                2. 单一抽象层次原则： 保证一个方法中的所有操作都在同一个抽象层次
            3. 领域驱动设计对依赖的控制
               https://mp.weixin.qq.com/s?__biz=MzA4NTkwODkyMQ==&mid=2651257450&idx=1&sn=b8091f5234383c437d5c864edd1de66f&chksm=842296bcb3551faad220528697108ea930bd6b5b1d1ddbb392a581b7c369268331adb58afb09
                1. 聚合: 聚合内的实体组成树，根实体是聚合的唯一出入口
                2. 自治的限界上下文：最小完备，自我履行，稳定空间，独立进化
            4. 业务架构师原来是这样的！
               https://mp.weixin.qq.com/s?__biz=MzA4NTkwODkyMQ==&mid=2651257314&idx=1&sn=8b9fae578dbd4527569e2b948a0bdd28&chksm=84229534b3551c227ccead245c72598fd59b185ffa98a998d39867117c7a94cfdcca82c69f81
               1. 宏观思维、抽象思维、战略思维和前瞻思维
               2. 逻辑架构、数据架构、开发架构、运行架构和物理架构 - “5视图法”

    64. 什么是动态规划（Dynamic Programming）？动态规划的意义是什么？ - 阮行止
        https://www.zhihu.com/question/23995189/answer/613096905

    65. 一文详解t检验 - CoffeeCat
        https://zhuanlan.zhihu.com/p/138711532
        1. "t检验的前提是要求样本服从正态分布或近似正态分布，不然可以利用一些变换（取对数、开根号、倒数等等）试图将其转化为服从正态分布是数据，如若还是不满足正态分布，只能利用非参数检验方法。不过当样本量大于30的时候，可以认为数据近似正态分布。"
        2. 回归系数的显著性检验

    66. 如何连贯地理解香农三大定理？ - BeyondSelf
        https://www.zhihu.com/question/39296849/answer/1467262363

    67. CockroachDB's Query Optimizer (Rebecca Taft, Cockroach Labs) - CMU Database Group - Rebecca Taft
        https://www.youtube.com/watch?v=wHo-VtzTHx0
        1. useful, finally somewhere makes explain CockroachDB's Query Optimizer
           DSL Optgen, Locality-Aware SQL Optimization, Theory vs Practice
        2. highlights
            1. cost based, emit single value cost, join only needs physical node
            2. outline
                1. Parse: SQL to syntax tree
                2. Optbuild: Call functions to produce preliminary query plan, semantic analysis (syntax error)
                3. Normalize: Normalization rules. i.e. common sense transforms without cost
                    1. DSL: Optgen. That's how code like for rules. It compiles and generates go code
                        1. Can it generate C++ code? Should work but seems not implemented
                4. Explore: Memo and Group Expression
                    1. cost model: sketches, histograms
                5. DistSQL Planning
                    1. find number of rows processed
                        1. estimate how stats change as data flows through execution plan
                        2. collect from index columns?
                    2. Multi-column stats
                        1. using index, for index on (a,b,c), collect multi-column stat for (a,b) and (a,b,c)
                        2. multi-column histograms coming later
                    3. Samplers on multiple nodes, scanning
                       aggregate at SampleAggregator
                        1. Automatic Statistics when, create table, column/index change, 20% data change
            3. Locality-Aware SQL Optimization
                1. network latency and throughput are considered geo-distributed
                   duplicate read-most data to locality
                   plan queries to use data from same locality
                2. future: support geo-partitioned unique indexes
            4. Theory vs Practice
                1. optimizing for OLTP
                    1. spent lot of time to optimize OLTP, make sure optimizer is fast enough
                    2. took advantage of many logical properties: cardinality, functional dependency, non-null columns, 
                    3. 252 normalization rules, 29 explorartion rules
                    4. foreigh key checks and cascades optimized as "post queries"
                2. Join ordering
                    1. Initial: CommuteJoin and AssociateJoin, Reordered at most 4 tables by default
                    2. CockroachDB V20.2 uses DPSUBE
                       DPSUBE: On the Correct and Complete Enumeration of the Core Search Space
                       orders up to 8 tables by default
                3. Query cache
                    1. LRU cache keyed on SQL string
                    2. Stores optimized memo. For prepared statement, stores normalized memo
                4. Optimizer hints 
                    1. e.g. use hash join
                5. Debugging tools
                    1. explain analyze
        n. related materials
            1. Query Optimization at Snowflake (Jiaqi Yan, SnowflakeDB) - CMU Database Group
               https://www.youtube.com/watch?v=CPWn1SZUZqE
                1. Micro-partition design, and the fine-grain MP skipping when scan
                   Internal WebUI-based debugging and visualization tool for query debugging
                   Focus on optimize analytics queries
                2. highlights
                    1. Micro-partition pruning
                        1. the table is first separated into MP. MP keeps sketches e.g. min-max
                           skipping here seems a quite fit technique if MP are small
                            1. this is clever, compared traditionally using plain full table scan vs index selection 
                        2. MP are Immutable files, PAX format, column-oriented compressed, unit of DML
                           large table could contain many M of MP
                           automatic clustering re-arranging MPs
                    2. Join filters
                        1. using bloom filtering, Range pruning
                    3. Diagnosability
                        1. Internal WebUI-based debugging and visualization tool. Stepwise plans
                        2. Query Reproducer, to reproduce locally the customer query having issue
                    4. Automatic Statstics collection
                        1. Statistics are always up to date and always accurate
                            1. row count, size, min/max, null count, etc
                            2. Snowflake does not use indices
                            3. question: how to make it alwways up-to-date, most DB needs user to to explict run analyze to refresh statistics
                                1. probably because statistics is always collected upon data ingestion, this is OLAP, and Snowflake doesn't use index
                3. related
                    1. Paper: The Snowflake Elastic Data Warehouse
                       http://info.snowflake.net/rs/252-RFO-227/images/Snowflake_SIGMOD.pdf

    68. 浅谈数据湖的过去，现状和未来 - 你说得对
        https://zhuanlan.zhihu.com/p/450041140
        1. very good. the summaries defined the problem space, key challenges, and furture directions. the article compared product product, with technical strength and market landscape. the author is much experienced and knows underwater
        2. highlights
            1. 大数据领域的发展历程
                1. HDFS完成了分布式的文件存储，
                   MapReduce解决了分布式的批式计算，
                   Yarn解决了分布式计算的资源调度问题。
                   Hbase解决了基本的近线的KV类大数据存储和访问。
                   Hive及其生态完成了传统数据仓库从数据库到Hadoop生态的迁移。
                   Flink以相对用户友好的方式收敛了实时数据计算
                2. problems space
                    1. HDFS不支持完整的增删改，不支持事务。虽然现有离线数仓的范式非常契合HDFS的immutable特性，但是这一特性带来了流程的冗余和成本升高，并进一步block了这种分布式文件存储的更多发展
                    2. 实时计算和离线计算很难达成一致。由于实时计算所使用的存储和HDFS有特性上的区别，进而导致了架构，存储，建模等方方面面的不同，所以目前批流一体都处于非常割裂得状态，大家希望能用kappa架构替换掉已有的lambda架构
                    3. 大数据领域的元数据管理正在面临可扩展性问题，伴随着数据复杂性提升，不论是NN还是hive，都遭遇越加严重的单点瓶颈问题
                    4. 传统数仓建模范式只能针对结构数据，对于不能被建模为二维表的非结构化数据，基本无能为力
                    5. 对于非数仓的其他大数据领域，现有的体系仍未形成最佳实践。这里主要想说的是，机器学习
                    6. 大数据的serving目前还没有比较完整的解决方案。大数据量，非预设逻辑，高并发，低延时的OLAP还不存在
                3. problems the datalake trying to solve
                    1. 数据湖针对其中的1、3尝试给出解法，
                       并努力想要收敛其中的2和5。
                       对于4和6，其实是没有任何解决的迹象的;所以很多文章上来就说数据湖可以解决非结构化数据存储问题，非常误导人
                4. market adoption
                    1. 在市场选型上，在选择使用开源框架的大型互联网公司中，iceberg和hudi基本是对半分的。DeltaLake相对比较少。
                    2. 其中，对CDC比较看重的一般会选hudi。
                    3. 对和hive和已有数仓体系兼容或者使用flink写入的，一般会选iceberg。
                       deltaLake因为其背后商业公司运营方式的原因，一般比较少有大公司会参与投入。
        n. related materials
            1. Data Lake 三剑客——Delta、Hudi、Iceberg 对比分析 - 朝晖
               https://www.cnblogs.com/dhcn/p/15239194.html
                1. good article, in depth each egine and with summary table
                2. highlights
                    1. Hudi - Hadoop upsert, HoodieKey, COW vs MOR (MergeOnRead)
                    2. Iceberg - no primary key, more work on query, hidden partition, column statistics skipping
                    3. Delta - Databricks, Spark integration
            2. 字节跳动基于Apache Hudi构建EB级数据湖实践 - ApacheHudi
               https://zhuanlan.zhihu.com/p/404664274
                1. good useful. there are many optimizations to learn from
                2. highlights
                    1. key reasons to select Hudi
                        1. MOR better ingestion
                            1. question: why datalake needs ability to update existing records? in datawarehouse, typically append only, each update is tagged with a timestamp
                        2. 全局索引, HBase
                        3. 基于NN和HDFS文件来管理元数据
                        4. Write and read access granularity problems
                            1. HDFS的原子操作粒度是文件，其他粒度一改不支持。
                            2. 数仓修改原子操作粒度是文件夹。不支持细粒度的修改，改一行/一列就要重写整个分区
                            3. 读写任务需要额外的通信机制，否则表粒度读写数据有并发问题
                        5. SQL query is usually externally hooked in, concurrent user access support is usually bad 
                    2. scenario
                        1. the diagram is very useful for reference
                        2. what enters datalake? 
                            1. App layer: user logs, metrics, feedbacks - streaming realtime
                            2. Recommendation Engine layer: 自系统内部回流的Instance, 推荐系统Serving时获得的Feature, 来自端上埋点/多种复杂外部数据源的反馈，这类数据作为Label，和之前的feature共同组成了完整的机器学习样本
                            3. Database layer: CDC
                            3. 近线处理 (nearline): BigTable自研TBase. 状态变更、统计、特征生成、模型训练
                        3. what is stored in datalake? datalake stores offline data
                            1. 样本数据，用户日志，文章数据，离线挖掘
            3. What Is the Kappa Architecture?
               https://hazelcast.com/glossary/kappa-architecture/
               https://cloud.tencent.com/developer/article/1769585
            4. Data Lake vs Data Warehouse
               https://www.talend.com/resources/data-lake-vs-data-warehouse/
               https://blog.csdn.net/u010002184/article/details/114238372
                1. this is actually wrong, from the above article

    69. 15年技术老兵自述：创业5年后加入阿里有什么优势 - 崮德
        https://mp.weixin.qq.com/s?__biz=MzkwOTIxNDQ3OA==&mid=2247532560&idx=1&sn=c7fe95efa3aa864181134e69a522ed53
        1. 蓝牙BLE&mesh方面的资深专家。2017年加入阿里巴巴人工智能实验室，负责AIoT总体架构设计，是蓝牙mesh从0到1落地天猫精灵开放平台的负责人
        2. highlights
            1. 结构化思考
                1. 阿里巴巴的产品经理特别喜欢用 Xmind 来做脑图
                2. 自顶向下或者自底向上的思考，或者 MECE （ Mutually Exclusive Collectively Exhaustive ,中文意思是“相互独立,完全穷尽”）
                3. 推广一个产品有 4P 原则，即 Product，Price，Place，Promotion
                4. 分析一个具体问题可以有 4W1H 原则，即 What，Why，When，Where 以及 How
                   2W1H 原则：What，How 和 Why 
            2. 演讲力

    70. Gartner Solution Scorecard for Cloud Service IaaS+PaaS
        Alibaba: https://www.gartner.com/doc/reprints?id=1-288OG5JN&ct=211126&st=sb
        AWS: https://www.gartner.com/doc/reprints?id=1-27GFQN50&ct=210916&st=sb
        Oracle News: https://www.oracle.com/emea/news/announcement/blog/oci-scores-in-gartner-solution-scorecard-for-iaas-and-paas-2021-11-18/
        1. Very good. as you click open details toolstip, it shows global cloud landscape, and how each cloud vendor builds feature
        2. highlights
            1. Gartner ScoreCard (Very good as you go to scorecard details)
                1. Solution: required, preferred, optional
                2. Resilience
                    1. categories: Datacenter geo, AZs, monitoring & metrics, dashboards personalized, VM non-interrupt in ops, VM failure recovery.
                                  AZ isolations. Disaster recovery. Cross region consistency
                    2. AliCloud has SLO, in explict numbers, but Azure not
                    3. Azure lacks in AZ isolation, and multi-AZ availability.
                    4. Oracle provides "Full regional consistency"
                        0. OK .. this each region has same feature offered, not data in sync replication
                        1. Oracle async cross-region volume replication
                           https://blogs.oracle.com/cloud-infrastructure/post/cross-region-block-storage-volume-replication
                           https://docs.oracle.com/en-us/iaas/Content/Block/Concepts/volumereplication.htm
                        2. Oracle Cloud Maximum Availability Architecture
                           https://www.oracle.com/a/tech/docs/cloud-maa-overview.pdf
                            1. 两地三中心架构
                            2. some Data Guard level is selling zero RPO even cross geo regions?
                                1. some Oracle low latency interconnect backbone, can ensure sync replication cross region?
                                   https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm
                3. Compute
                    1. Categories: rapid launch, massive launch, launch large, VMs, migration; exclusive host, baremetal, private image catalog; containers / K8S; hooks, autoscaling, second level billing; trusted enclaves
                3.2. Storage
                    1. Categories: data migration appliance. block storage, object storage, file storage. snapshot, cross-region replication, permission, performance targets; large volume, archive storage, backup, encryption
                                   policy-driven approach to snapshot life cycle management; cross region file share; cloud storage gateway; 
                3.3. Network
                    1. Categorize: VPC, VPN gateway, Loadbalancer, static IP, DNS, perf SLO & monitor;
                                   VPC across region, traffic mirroring, 

                5. Security
                    1. Categories: Key/Certificate management, audits, retire sanitization, Trusted boost;
                                   federated identity, SSO, multifactor authentication (MFA), RBAC, resource groups; firewall, DDOS mitigation/scrubbin;
                                   thread monitoring, compliance, vulnerability assessment; Endpoint protection, encryption SDK, Sensitive data discovery
                6. Software Infa Services
                    1. Categories: Relational database, replication, Datawarehouse, FaaS, NoSQL;
                     DB migration, in-memory caching, API gateway, search indexing, messaging, CDN
                                   Micro-service Service Mesh, Globally distributed DB, GraphDB; end-user identity, emailing
                7. Digital Business Infrastructure
                    1. Categories: CI / CD, Bigdata analytics, Streaming, ML-optimized VM, ML training/inference, HPC, DB-optimized NVMe VMs
                                Edge Stack, Time-series DB, ETL, data catalog, Blockchain
                8. Operations and Governance
                    1. Categories: Self-service, cost, audit, templates, policies, metadata tagging
                                   Demo serivces, CMDB, Automation, Batch, Mobile App, AIOps
                9. Vendor Management and Audit
                    1. Categories: SLA, health dashoard, documentation, event management, support ticket, training & certification, managed service providers (MSPs), mitigation track record, global offering, Reference architectures, Marketplace (with > 500 ISVs)
                                    DC energy efficiency, FedRAMP, US DoD, HIPAA, CJIS, Law enforcement request/transparency report
            2. AWS strength and weakness
                1. Strengths
                    1. Large-scale capacity and scalability offerings
                    2. Extensive portfolio of flexible service offerings
                    3. Core focus on digital businesses
                    4. Proven suitability for the traditional enterprise
                    5. Broad and deep ecosystem
                2. Weakness
                    1. Building blocks, not solutions
                    2. Choice overload
                    3. Limited architectural transparency
                    4. Oriented toward distributed cloud, not hybrid cloud
                    5. Limited traditional disaster recovery (DR) capabilities
                        1. i.e. AWS has not many regions in some countries, that cannot offer distant but still in-country DR sites
                3. neutral
                    1. AWS is built around the assumption that organizations want to be agile and innovative
                    2. AWS’s release velocity is not only fast, but also unpredictable
            3. AliCloud
                1. Strong China top 1. Higher score than Google Cloud. Apsara Stack AI
                2. suffers from the lacking part is global offering, inconsistent china/global offering, limited ecosystem for multicloud customers
                3. Sometimes there are multiple services with what seem to be very similar feature sets, but each service has nuances that make it more optimal for particular use cases.
                4. Be mindful of the dearth of English-language documentation
            4. summarized key abilities of Azure
                1. Mission critical KPIs
                    1. run long time without failure
                    2. deterministic and consistent performance
                    3. high availability self and for customer apps
                2. dynamic and scale the workload
                3. Linux support, K8S support
                4. storage attached, e.g. SAN and NAS, NFS, HDFS
                5. Disaster recovery, Snapshot in time
                6. Migration tools into Azure, TCO cost management
                7. Run Azure on-premise customer datacenter, connect services to Azure
                8. Security, confidential, zero trust, enclave
                9. HPC, AI, Analytics workload
                10. working with 3rd party vendors
        n. related materials
            1. 云头条 News: https://mp.weixin.qq.com/s?__biz=MzI4OTc4MzI5OA==&mid=2247547807&idx=1&sn=4f8f9cd09a1eacbe7cab9188f2d17b64&chksm=ec2b90f2db5c19e4c59490cbb8e4864a497a486d546b330d29ace18963ff6f0cebc48b715b90
            2. 特大号 News: https://mp.weixin.qq.com/s?__biz=MzI3MzAzNDAyMQ==&mid=2657720192&idx=1&sn=6338af93cb7abdad96f82fcc04295294&chksm=f0b449cac7c3c0dc9bbc4fa83a0c5f2a784e392b81335b104a5fd086f44de04c66059c38b8f2
                1. 计算，存储，网络
                2. 弹性
                3. 安全
                4. 软件开发，数字化，运营
                5. 供应商
            3. Zhihu: https://www.zhihu.com/question/504904337

1. Readings: Comparing AWS S3 with Azure Storage and learn.
    1. Below articles reveal S3 is essentially Dynamo (which is published)
    2. key takeaways
        1. S3 is not append-only system. Blob objects can be updated. Updates are versioned.
        2. S3 is eventual consistent (though most time reads will return newest version). Until 2020 Dec.1, S3 released strong consistency feature (deep dive).
            1. According to deep dive, the primary source of S3 inconsistency is from the metadata cache layer. Reads may go to metadata cache nodes pointing to older version of data.
        3. S3 uses consistent hashing to manage data placement, which doesn't need metadata. Unlike we have metadata memory scalability issue. (Note consistent hashing is weaker at fine-grain placement and migration)
        4. S3 is a blob service. VHD is served by EBS, which seems another system. Unlike Azure Storage combine them all.
        5. S3 updates goes through quorum writes, e.g. writes need update 3 out of 5 replicas. It has a few implications
            1. Not all replicas are latest, thus stale reads are possible, i.e. eventual consistency.
            2. Version conflicts are possible. S3 resolving conflicts by simple "last write win".
            3. Maintaining 5 replica is expensive, unless multi-zone/region. Probably S3 built-in multi-zones and cross-region inside quorum write from day 1.
        6. There are interesting features in revealed in this article about S3 2006-2021 history 
            1. S3 Intelligent-Tiering
            2. S3 Replication Time Control
            3. S3 Object Lambda feature
    3. materials
        1. https://www.allthingsdistributed.com/2021/04/s3-strong-consistency.html
        2. https://aws.amazon.com/about-aws/whats-new/2020/12/amazon-s3-now-delivers-strong-read-after-write-consistency-automatically-for-all-applications/
        3. https://www.allthingsdistributed.com/2021/03/happy-15th-birthday-amazon-s3.html
        4. https://stackoverflow.com/questions/564223/amazon-s3-architecture
        5. https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html

```

More earlier results.

```
2. Readings: Recent Weichat articles   (1hrs)
    1. Sailfish: accelerating cloud-scale multi-tenant multi-service gateways with programmable switches [SIGCOMM, 2021, Alicloud, 0 refs]
       https://mp.weixin.qq.com/s?__biz=MzkxMDE3MDQxMA==&mid=2247485427&idx=1&sn=ad4ee2fbad0a1576f5c0d2cc1a074e56&chksm=c12ec7b6f6594ea0b9eef6ea0ae637fc46f0a464d37ea5ffa3cc4990eacf571bc76c15180001
        1. 可编程ASIC用于SBL

2. Misc: Reading: recent piled up WeiChat articles    (1hrs + 1hrs + 0.5hrs)
    1. CPU内部各个部件的时延大概是多少？（皮秒，纳秒）?
       https://www.zhihu.com/question/488790905/answer/2139603594
    2. 【会议解读】HOT CHIPS 33 Session 4
       https://zhuanlan.zhihu.com/p/421535584
    3. 分布式事务最经典的七种解决方案
       https://mp.weixin.qq.com/s?__biz=MzA5OTAyNzQ2OA==&mid=2649741845&idx=2&sn=8d8e5133747763cb43b78e532477ea95
    4. 现代中央处理器（CPU）是怎样进行分支预测的？
       https://www.zhihu.com/question/486239354/answer/2129757853
    5. All Things Distributed - Continuous Configuration - AWS AppConfig
       https://www.allthingsdistributed.com/2021/08/continuous-configuration-on-aws.html
    6. LSM-tree 的 Remote Compaction调度
       https://zhuanlan.zhihu.com/p/419766888
    7. 《Speedy Transactions in Multicore In-Memory Databases》
       https://zhuanlan.zhihu.com/p/419423367
    8. VLDB 2021 有哪些值得关注的论文？
       https://www.zhihu.com/question/480933862/answer/2094178256
    9. c++20协程入门
       https://zhuanlan.zhihu.com/p/59178345
    10. 推荐系统技术演进趋势：从召回到排序再到重排
        https://www.google.ca/advanced_search
        1. good summary overview

3. Misc: Reading: recent piled up WeiChat articles    (0.5hrs + 0.5hrs)
    1. AWS：存储新纪元已经到来！
       https://mp.weixin.qq.com/s?__biz=MzAwMDM4NTUyNw==&mid=2652254161&idx=1&sn=6b57d6eb7f1b827d5c41fa36aeb34a0b
        1. useful article to watch for recent updates
        2. highlights
            1. AWS和NetApp设计了一个解决方案，将完整的NetApp堆栈移植到AWS上，它将作为一个完全托管的服务交付
                1. question: Cloud vendor is the biggest competitor of NetApp/EMC traditional storage vendors
                   OK .. we can sell boxes in this way?
                2. "现在它可以变得有趣的地方是跨云。换句话说，如果NetApp可以从Snowflake Inc.中借鉴并构建一个抽象层，该抽象层不仅隐藏了AWS云的底层复杂性，还隐藏了 Google Cloud Platform 和 Microsoft Azure，您可以在其中登录NetApp 数据云，并优化了您的本地、AWS、Azure 和/或 GCP 文件存储，我们认为这是一个成功的策略"
            2. AWS还宣布了S3多区域访问点。这是一种考虑到延迟、网络拥塞和数据副本位置的优化存储性能的服务，通过最佳路径交付数据，以确保最佳性能
                1. S3 Multi-Region Access Points
                    1. What we have for multi-region?
                        1. remote migration
                        2. cross region EC
                        3. Exchange saves each of one replica (DB server) in a different region, 2-sync, 1-async
                            1. so if using Azure Storage, it's naturally using a multi-region replica
                    2. How AWS did it?
                        1. We know S3 has multi-zone design from very early.
                           but from "from global presence of AWS Global Accelerator", it should be by CDN / EdgeCloud architecture
                            1. object in buckets, buckets in different region
                        2. Azure: Integrate an Azure Storage account with Azure CDN
                           https://docs.microsoft.com/en-us/azure/cdn/cdn-create-a-storage-account-with-cdn
            3. AWS宣布了分层的改进，包括EFS智能分层，以优化文件存储的成本。它还宣布了S3分层特性，不再对低于128K的小对象收费
            4. AWS还发布了备份监控工具，以确保备份符合法规和公司规定

3. readings: WeiChat remaining articles & Zhihu
    1. 阿里云PolarDB及其存储PolarFS技术实现分析（上）(下)
       https://zhuanlan.zhihu.com/p/44874330
       https://zhuanlan.zhihu.com/p/44874809
        0. good interesting design.
           as a compare to AWS Aurora Mult-master, and to OceanBase
        1. highlights
            1. raft paxos data replication, not like 3-way replication
               raft paxos's return at 2 replica ready
                1. overhead: read may hit inconsistent data on the 3rd node
            2. parallelraft: allow holes in log
            3. userspace IO, userspace RDMA, userspace FS
            4. the testing showed they used CephFS before PolarFS
            5. section "与Aurora简单对比"
        2. questions
            1. abstraction: db->file->chunk->storage
               why not simply like Aurora: db->shared log?
                1. since we have paxos file, what's the meaning of journal, duplicated?
                   though currently we use paxos for locking, journal for metadata
                2. see section "与Aurora简单对比"
    2. 从R-CNN到RFBNet，目标检测架构5年演进全盘点
       https://zhuanlan.zhihu.com/p/45196320

3. readings: misc from weichat
    1. RocksDB事务实现TransactionDB分析
       https://zhuanlan.zhihu.com/p/31255678
        1. good
    2. 美团配送系统架构演进实践
       https://zhuanlan.zhihu.com/p/40681219
        1. good

3. readings: misc WeiChat
    1. Alibaba Open Channel SSD，阿里巴巴存储架构的重要里程碑
       http://www.ssdfans.com/blog/2018/07/24/alibaba-open-channel-ssd%EF%BC%8C%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E5%AD%98%E5%82%A8%E6%9E%B6%E6%9E%84%E7%9A%84%E9%87%8D%E8%A6%81%E9%87%8C%E7%A8%8B%E7%A2%91/
```

More results in the timeline

```
4. readings: remaining remaining articles
    1. B 站监控系统的框架、演进与展望
       http://mp.weixin.qq.com/s/bRm2bhpzUPRGrxg9lqlaOg
        1. they are using something similar to Goole Dapper too

5. readings: Machine Learning - random forest algorithm
    1. 机器之心: 从决策树到随机森林：树型算法的原理与实现
       https://www.jiqizhixin.com/articles/2017-07-31-3
        1. good
        2. （K-折）交叉验证（Cross Validation）简介
           https://blog.csdn.net/holybin/article/details/27185659
        3. 机器学习中的算法：决策树模型组合之随机森林（Random Forest）
           https://blog.csdn.net/holybin/article/details/25653597
    2. Bagging与随机森林算法原理小结
       https://www.cnblogs.com/pinard/p/6156009.html
        1. good.
        2. 机器学习中Bagging和Boosting的区别
           https://blog.csdn.net/u013709270/article/details/72553282
        3. Quora: What is the difference between boost, ensemble, bootstrap and bagging?
           https://www.quora.com/What-is-the-difference-between-boost-ensemble-bootstrap-and-bagging
    3. hangtwenty: Dive into Machine Learning
       https://github.com/hangtwenty/dive-into-machine-learning
        1. Quora: What are the best ways to pick up Deep Learning skills as an engineer?
           https://www.quora.com/What-are-the-best-ways-to-pick-up-Deep-Learning-skills-as-an-engineer
            1. CS231n Convolutional Neural Networks for Visual Recognition
               http://cs231n.github.io/
    4. 机器学习总结(四)——随机森林与GBDT(梯度提升决策树)
       https://blog.csdn.net/manong_wxd/article/details/78745728
        1. GBDT算法原理深入解析
           https://blog.csdn.net/yangxudong/article/details/53872141
            1. good
            2. 机器学习之GBDT(简单理解)
               https://juejin.im/post/5a9cdec1518825556533f8aa
        2. GBDT（MART） 迭代决策树入门教程 | 简介
           https://blog.csdn.net/w28971023/article/details/8240756
        3. 第四范式联合创始人陈雨强：机器学习在工业应用中的新思考
           https://www.jiqizhixin.com/articles/2016-12-22-7
            1. good
            2. 如何通俗的理解机器学习中的VC维、shatter和break point？
               https://www.zhihu.com/question/38607822
            3. 机器学习中常常提到的正则化到底是什么意思？
               https://www.zhihu.com/question/20924039

5. readings: TDA持续同调
    1. Cpp meta template partial-specialization programming, and for log formatting in compile time
       http://cpp.sh/8kljg
    2. PCA - Principal component analysis - Dimensionality reduction
       https://en.wikipedia.org/wiki/Principal_component_analysis
       http://www.cnblogs.com/zhangchaoyang/articles/2222048.html
       https://en.wikipedia.org/wiki/Covariance_matrix
       https://yoyoyohamapi.gitbooks.io/mit-ml/content/%E7%89%B9%E5%BE%81%E9%99%8D%E7%BB%B4/articles/PCA.html
       http://www.cnblogs.com/LeftNotEasy/archive/2011/01/19/svd-and-applications.html
    3. 拓扑数据分析－持续同调 - 知乎专栏 - 拜势科技
       https://zhuanlan.zhihu.com/p/31734839
       https://zhuanlan.zhihu.com/p/31946203
       https://zhuanlan.zhihu.com/p/33376520

4. readings: FLP impossibility
    1. 阿莱克西斯 - 评:Streaming System(简直炸裂,强势安利)
       https://zhuanlan.zhihu.com/p/43301661
    2. FLP Impossibility
       https://blog.csdn.net/chen77716/article/details/27963079
    3. FLP Impossibility paper: Impossibility of Distributed Consensus with One Faulty Process [1985, 4647 refs]
       https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf
    4. A Brief Tour of FLP Impossibility
       https://www.the-paper-trail.org/post/2008-08-13-a-brief-tour-of-flp-impossibility/
    5. FLP 不可能原理
       https://yeasy.gitbooks.io/blockchain_guide/content/distribute_system/flp.html

5. readings: Streaming Systems
    1. The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing    [2015, 211 refs]
       https://ai.google/research/pubs/pub43864
    2. 评:Streaming System(简直炸裂,强势安利)
       https://zhuanlan.zhihu.com/p/43301661
        1. Microsoft has booked as safari book: https://www.safaribooksonline.com/library/view/streaming-systems/9781491983867/
    3. (十)简单解释: 分布式数据流的异步快照(Flink的核心)
       https://zhuanlan.zhihu.com/p/43536305

4. readings: QCon 2018
   https://ppt.geekbang.org/list/qconsh2018
    1. 前隆微服务实践
       https://ppt.geekbang.org/slide/show?cid=33&pid=1722
    2. Tiger图数据库案例
       https://ppt.geekbang.org/slide/show?cid=33&pid=1726
        1. interesting
        2. related
            1. TigerGraph完成3100万美元A轮融资
               http://www.cctime.com/html/2017-11-9/1335209.htm
            2. GraphSQL 相比其它图数据库的优势?
               https://www.zhihu.com/question/41621125
            3. TigerGraph Docs : TigerGraph Platform Overview v2.1
               https://doc.tigergraph.com/TigerGraph-Platform-Overview.html
            4. TigerGraph: The parallel graph database explained
               https://www.infoworld.com/article/3269604/nosql/tigergraph-the-parallel-graph-database-explained.html
            5. Introducing TigerGraph, a Native Parallel Graph Database
               https://thenewstack.io/introducing-tigergraph-native-parallel-graph-database/
            6. TigerGraph, a graph database born to roar
               https://www.zdnet.com/article/tigergraph-a-graph-database-born-to-roar/
    3. 七牛云边缘存储服务架构分享
       https://ppt.geekbang.org/slide/show?cid=33&pid=1700
    4. 阿里巴巴统一调度系统SIGMA
       https://ppt.geekbang.org/slide/show?cid=33&pid=1720
        1. good
            1. 干扰分析
            2. 避免离线任务调度到在线任务相邻的HT上（规避HT，noise clean）
            3. Sigma调度核心与PouchContainer
        2. related
          1. CPI2: CPU performance isolation for shared compute clusters
             https://john.e-wilkes.com/papers/2013-EuroSys-CPI2.pdf
          2. Cluster Management at Google
             https://www.usenix.org/cluster-management-google
             https://www.usenix.org/sites/default/files/conference/protected-files/wilkes_lisa13_slides.pdf
    5. 蚂蚁金服端侧AI
       https://ppt.geekbang.org/slide/show?cid=33&pid=1729
    6. 微博深度学习在推荐系统中的应用
       https://ppt.geekbang.org/slide/show?cid=33&pid=1710
    7. 百度DStream3
       https://ppt.geekbang.org/slide/show?cid=33&pid=1818
    8. Pravega Streams
       https://ppt.geekbang.org/slide/show?cid=33&pid=1793

5. readings: Group Theory
   https://www.jmilne.org/math/CourseNotes/GT.pdf
    1. also, Computational Group theory
       https://www.jaapsch.net/puzzles/schreier.htm
    2. finally find the way to solve magic cube, by
       using my customized version of group action
         (actually should be from Jaapsch's article, but they didn't clarify the definition)
       and the stabilizer chain method
    3. materials
        1. The Schreier-Sims algorithm for finite permutation groups
           https://blogs.cs.st-andrews.ac.uk/codima/files/2015/11/CoDiMa2015_Holt.pdf
        2. Schreier-Sims Algorithm - Mathematics and Such
           https://mathstrek.blog/2018/06/12/schreier-sims-algorithm/

2. readings: Deep Learning
    1. ImageNet Classification with Deep Convolutional Neural Networks [2012, 31928 refs]
       https://www.nvidia.cn/content/tesla/pdf/machine-learning/imagenet-classification-with-deep-convolutional-nn.pdf
        1. AlexNet paper that first made CNN popular on ImagetNet recognition
           ILSVRC'12, AlexNet reduced top-5 error from 25.8% to 16.4, a leap
        2. highlights
            1. CNN is not new, but GPU training enabled it to be practical.
            2. Besides CNN, below technology is effective and became widely adopted
                1. ReLU Nonlinearity as the neuron activation function
                2. deep, more parameters can be more vulnerable to overfitting
                   to fight against overfitting
                    1. Data augmentation
                    2. Dropout
        n. related materials
            1. Deep Learning回顾#之LeNet、AlexNet、GoogLeNet、VGG、ResNet
               https://zhuanlan.zhihu.com/p/22094600
                1. good article

    2. ResNet: Deep Residual Learning for Image Recognition    [2016, 15636 refs]
       https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf
        1. deeper CNN expects higher accuracy. but experiemences shows that training is hard.
           Introducing the Residual shortcut connection, train F(x) := H(x) - x,
           however is much easier to train.
           In the end we got 157 layer ResNet ImageNet top-5 error rate to 3.57%
        2. highlights
            1. the chart of traing error & test error on iteration steps,
               is a good tool to study training optimization issue
            2. if the dimension of x and F are not equal,
               we can perform a linear projection Ws.

3. readings: general updates
    1. pravega
       https://www.infoq.cn/article/UuiP79pPP-IQbAr7dXo3
       https://www.infoq.cn/article/u8gDitPJ28mY-JL6izQT
       https://www.cnblogs.com/huxi2b/p/8459342.html
        1. work with Flink
        2. key feature: exactly-once (Consistency and durability, transaction)
            1. flink's separate messages into checkpoints, and two phase commit
               checkpoint: lamport's distributed snapshot algorithm, inject barriers/markers
    2. ceph conferences
        1. CEPHALOCON APAC 2018
           https://ceph.com/cephalocon/beijing-2018/
            1. Global Deduplication for Ceph - Myungwon Oh
               https://www.youtube.com/watch?v=diVmAdUme9Q&feature=youtu.be
               https://www.slideshare.net/Inktank_Ceph/global-deduplication-for-ceph-myoungwon-oh
            2. Everything You Wanted to Know About RadosGW - Orit Wassermann, Matt Benjamin
               https://www.youtube.com/watch?v=QDgWL1RyLmM&feature=youtu.be
                n. related
                    1. Why doesn't Amazon S3 allow the user to search by metadata?
                       https://www.quora.com/Why-doesnt-Amazon-S3-allow-the-user-to-search-by-metadata
                    2. Building and Maintaining an Amazon S3 Metadata Index without Servers
                       https://aws.amazon.com/blogs/big-data/building-and-maintaining-an-amazon-s3-metadata-index-without-servers/
            3. RADOS improvements and roadmap - Greg Farnum, Josh Durgin, Kefu Chai
               https://www.slideshare.net/Inktank_Ceph/rados-improvements-and-roadmap-greg-farnum-josh-durgin-kefu-chai
                1. ceph-mgr Balancer module to improve CRUSH placement balance
                   http://docs.ceph.com/docs/mimic/mgr/balancer/
                   https://www.xsky.com/tec/20171204/
                    1. upmap: OSDMap stores explicit PG mappings for individual OSDs as exception to CRUSH
                    2. crush-compat: balancer optimize the weight-set values
            4. Ceph Based Large Scale Application Case and Technology in Financial Industry - Wang Gang
               https://www.youtube.com/watch?v=kHg4bj1BqzM&feature=youtu.be
                1. massive amount of small files (e.g. small images)
                   multi-site replica distribution
                2. very good talk. no slides but the talk is very in detail
            5. CEPH DAY BERLIN - 5 REASONS TO USE ARM-BASED MICRO-SERVER ARCHITECTURE FOR CEPH CLUSTER
               https://www.slideshare.net/Inktank_Ceph/ceph-day-berlin-5-reasons-to-use-armbased-microserver-architecture-for-ceph-cluster
                1. the bechmark is much better ARM vs x86
            6. CEPH DAY BERLIN - DISK HEALTH PREDICTION AND RESOURCE ALLOCATION FOR CEPH BY USING MACHINE LEARNING
               https://www.slideshare.net/Inktank_Ceph/ceph-day-berlin-disk-health-prediction-and-resource-allocation-for-ceph-by-using-machine-learning
        2. CEPH DAY BERLIN
           https://ceph.com/cephdays/ceph-day-berlin/
    3. infoq
        1. 中台之上（二）：Zachman 模型，TOGAF
           https://www.infoq.cn/article/th-QkbHEr82MaxS9BMof
           中台之上（六）：如何为一个商业银行设计业务架构？
           https://www.infoq.cn/article/tcXcUq8-k4dxTZ19lmw9
    4. booked papers
        1. Datacenter PRCs can be General and Fast
           https://www.usenix.org/conference/nsdi19/presentation/kalia
        2. Exploiting commutativity for practical fast replication
           https://www.usenix.org/conference/nsdi19/presentation/park
        3. Design of Global Data Deduplication for A Scale-out Distributed Storage System
           https://ceph.com/wp-content/uploads/2018/07/ICDCS_2018_mwoh.pdf
        4. Understanding Lifecycle Management Complexity of Datacenter Topologies
           https://www.usenix.org/conference/nsdi19/presentation/zhang

3. readings: recent cloud storage articles piled up
    1. 「阿里云总监课」存储系统设计——NVMe SSD性能影响因素一探究竟
       https://zhuanlan.zhihu.com/p/48030385
        1. good
        2. Data Retention in MLC NAND Flash Memory: Characterization, Optimization, and Recovery
           https://people.inf.ethz.ch/omutlu/pub/flash-memory-data-retention_yixin_hpca15-talk.pdf
    2. 点云匹配 icp
       https://cloud.tencent.com/developer/information/%E7%82%B9%E4%BA%91%E5%8C%B9%E9%85%8D%20icp
    3. 十年磨一剑！OceanBase查询优化器的设计之道和工程实践哲学
       https://mp.weixin.qq.com/s/1UZeIvkJ32e2z3n6OSj1-g
    4. [译] 分布式系统中的一致性模型 - 陈Qiu凯
       https://zhuanlan.zhihu.com/p/48782892
        1. good. finally linearizability vs sequential consistency
    5. Small Cache, Big Effect - 陈Qiu凯
       https://zhuanlan.zhihu.com/p/66273612
    6. 360深度实践：Flink与Storm协议级对比
       https://mp.weixin.qq.com/s/iSnL8BDHv53cLEq4dpZWjw
    7. 通用矩阵乘（GEMM）优化与卷积计算
       https://zhuanlan.zhihu.com/p/66958390
    8. 神经架构搜索方法知多少 - 机器之心
       https://mp.weixin.qq.com/s/7BktpWWSbWe2DAaS9O0PcA
    9. MySQL Group Replication Paxos层不足和优化
       https://zhuanlan.zhihu.com/p/67485031
    10. Google 是如何做负载均衡的？       [year-2016]
        https://zhuanlan.zhihu.com/p/23826170

    11. MapD: Massive Throughput Database Queries with LLVM on GPUs
        https://devblogs.nvidia.com/mapd-massive-throughput-database-queries-llvm-gpus/
        http://www.smallake.kr/wp-content/uploads/2014/09/mapd_overview.pdf
        http://go.mapd.com/rs/116-GLR-105/images/MapD%20Technical%20Whitepaper%20Summer%202016.pdf
        1. GPU 数据库 MapD 性能超传统数据库 70 倍，数据库瓶颈不是 IO 吗？
           https://www.zhihu.com/question/21003317/answer/111549889
        2. 领先的开源内存数据库，早在2011年就在查询引擎中使用LLVM了
           HyPer: Hybrid OLTP&OLAP High-Performance Database System
           https://link.zhihu.com/?target=http%3A//hyper-db.de/index.html%23

    12. 【云吞铺子】性能抖动剖析
        https://zhuanlan.zhihu.com/p/62705793
        https://zhuanlan.zhihu.com/p/63540754
        https://zhuanlan.zhihu.com/p/65219936

1. readings: misc articles piled up
    1. 科普：分布式深度学习系统（二）
       https://zhuanlan.zhihu.com/p/30976469
       https://zhuanlan.zhihu.com/p/29032307
        1. very good
    2. 从300万行到50万行代码，遗留系统的微服务改造
       https://mp.weixin.qq.com/s/Z6Tk7FMLX9PIdbcL3iyIHA
        1. good
    3. 从 SGD 到 Adam —— 深度学习优化算法概览(一)
       https://zhuanlan.zhihu.com/p/32626442
    4. 浅析RocksDB的SSTable格式
       https://zhuanlan.zhihu.com/p/37633790
        1. highlights
            1. 排序存储，前缀压缩
    5. MySQL插入缓冲
       https://zhuanlan.zhihu.com/p/39812854
        1. highlights
            1. 因不排序，随机写入。使用插入缓冲，排序和批写入
               类似LSM-tree的compactin
    6. raft算法浅析
       https://zhuanlan.zhihu.com/p/38779730
       https://zhuanlan.zhihu.com/p/39105353
    7. 如何看待Google的Cloud Spanner?
       https://www.zhihu.com/question/55828060/answer/748777146
    8. Cascades Optimizer
       https://zhuanlan.zhihu.com/p/73545345
    9. 查询编译综述
       https://zhuanlan.zhihu.com/p/60965109

8. readings: recent learnings
    1. Hadoop Federation
        1. https://www.quora.com/What-is-HDFS-federation
            1. interesting design - Federation.
        2. https://www.infoq.cn/article/application-and-improve-of-hdfs-federation-in-meituan
        3. https://my.oschina.net/cloudcoder/blog/880812
        4. https://www.cnblogs.com/BYRans/p/5524780.html
    2. Gossip protocol convergence calculation
        1. Gossip Protocol Epidemiology convergence
           http://kaiyuan.me/2015/07/08/Gossip/
            1. good
        2. https://en.wikipedia.org/wiki/Gossip_protocol
        3. Service Fabric: A Distributed Platform for Building Microservices in the Cloud
        4. Gossip Protocols - Márk Jelasity
           http://www.inf.u-szeged.hu/~jelasity/ddm/gossip.pdf
            1. in detailed.
            2. total time to convergence
               vs. total messages sent
        5. Gossip Simulator
           https://flopezluis.github.io/gossip-simulator/
            1. good. You need to click a node first.
            2. convergence
               https://www.serf.io/docs/internals/simulator.html
        6. Using Gossip Protocols For Failure Detection, Monitoring, Messaging And Other Good Things
           http://highscalability.com/blog/2011/11/14/using-gossip-protocols-for-failure-detection-monitoring-mess.html
            1. useful. to maintain concensus
                1. use a central database
                2. paxos
                3. gossip protocol
            2. related
                1. GEMS: Gossip-Enabled Monitoring Service for Scalable Heterogeneous Distributed Systems
                    1. divide cluster into divisions and hierarchies, laters of aggregation
                       so we can reduce the total message counts
        7. https://www.quora.com/What-is-a-Gossip-protocol

9. readings
    1. MySQL group commit
        1. https://www.kancloud.cn/taobaomysql/monthly/67157
        2. https://my.oschina.net/u/3023401/blog/823333
        3. https://sq.163yun.com/blog/article/188020255134334976
           https://sq.163yun.com/blog/article/188020984930648064

8. readings: misc piled-up articles
    1. 等待的艺术：从Spin Lock到Token Bucket算法
       https://zhuanlan.zhihu.com/p/84617791
        n. related materials
            1. How to measure CPU cache misses
                1. on linux
                   https://stackoverflow.com/questions/10082517/simplest-tool-to-measure-c-program-cache-hit-miss-and-cpu-time-in-linux
                2. on windows
                   https://docs.microsoft.com/en-us/visualstudio/profiling/cpu-and-windows-counters?view=vs-2015&redirectedfrom=MSDN
                    1. Visual Studio Performance Explorer
                       L2 CPU cache misses
                        1. Need to disable Hyper-V first
                        2. need to launch VS in admin mode
                        3. Issue: even disabled Hyper-V and killed Hyper-V service, VS still reports VSP1478
                    2. Perfview tool
                        1. perfview tool for windows
                           https://blogs.msdn.microsoft.com/vancem/
                        2019/03/14/perfview-hard-core-cpu-investigations-using-cpu-counters-on-windows-10/
                            1. perfview github
                               https://github.com/microsoft/perfview
                        2. perfview cache misses
                           https://github.com/selagroup/diagnostics-courses/tree/master/perf-perfview-cache
                            1. good
                    3. others
                        1. https://randomascii.wordpress.com/2016/11/27/cpu-performance-counters-on-windows/

2. readings: misc piled up articles
    1. 多核时代与并行算法
       https://zhuanlan.zhihu.com/p/89863627
    2. 为什么需要知识图谱？什么是知识图谱？——KG的前世今生
       https://zhuanlan.zhihu.com/p/31726910
    3. PageRank算法与特征向量和特征值(eigenvector和eigenvalue)
       https://blog.csdn.net/sdgihshdv/article/details/77340966
       https://www.changhai.org/articles/technology/misc/google_math.php
        1. PageRank可以解释称Markov模型转移，eigenvector是稳定解
        2. (1-q/N)余项可化为ee^t*R，因为sum(R)是定值
           本质上因为特征值R*k也是特征值，所以限定sum(R)合理
    4. 超越"双十一"—— ebay百万TPS支付账务系统的设计与实现
       https://mp.weixin.qq.com/s/sbHPxzIqv_dRn555XzE5mw
        1. good
        2. why we need Raft/paxos to do 3-way replication?
            1. well, not us, but some system's 3-way replication chain is statically assinged to nodes
               that means, single node failure will interrupt the replication flow,
               it can happen frequently, and must be well taken care.
               so, raft/paxos allows majorty-out-of-all to return early, it helps.
               the the pay is less than 3-nodes persistence reliability.
        3. Event sourcing is well-match for the traceability of financing systems
    5. softmax和cross-entropy是什么关系？
       https://www.zhihu.com/question/294679135/answer/885285177
    6. MongoDB分布式事务原理
       https://zhuanlan.zhihu.com/p/90996685
        1. interesting
        2. Transaction: WiredTiger
            1. transaction - sharding - replication
                      distributed - avaialbility
                              consensus
            2. 2PC + replication set, snapshot isolation
               MVCC implemented by linked-list, conflict check by walking through list
               sounds like spanner's solution anyway
            n. materials
                https://www.slideshare.net/MyDBOPS/mongodb-wiredtiger-internals-journey-to-transactions
        n. related materials
            1. understanding external consistency
                1. transaction consistency:
                    T1, T2, T3 appears to be executed non-interleaved
                    we don't limit what's the appeared execution order of T1/T2/T3
                    we don't limit what the other readers can see
                        1) consistent results in different nodes
                        2) the newest value T1/T2/T3 execution appears
                2. linearizability
                    1. read write ordering and visibility
                    2. so, we can see, transaction consistency doesn't constraint the ordering required in the "linearizability".
                       so, we need to combine them too, call it "external consistency"
                3. related materials
                    1. 简单解释Spanner的TrueTime在分布式事务中的作用
                       https://zhuanlan.zhihu.com/p/44254954
                    2. 如何理解数据库的内部一致性和外部一致性？
                       https://www.zhihu.com/question/56073588/answer/519284998
        7. 正态分布上的期望之旅（一）
           https://zhuanlan.zhihu.com/p/87561292

9. readings: misc piled up articles
    1. 辉煌的中心极限定理
       https://zhuanlan.zhihu.com/p/85233692
        1. good
    2. 深度剖析阿里数据库内核：基于HLC的分布式事务实现
       https://mp.weixin.qq.com/s/CXoFMKtBz74ENVFMtIjVkQ
    3. 首次揭秘！字节跳动基础架构技术迭代演进之路
       https://mp.weixin.qq.com/s/1Pk0_3MG5CrriFZo4DtR0A
    4. 首度公开！OceanBase存储系统架构的演进历程及工程实践
       https://mp.weixin.qq.com/s/Z_i_QcaNMtYwUKC56WByyw
        1. interesting
        2. highlights
            1. 日志和数据分离， 日志三副本，数据量副本
            2. 在线分区分裂
            3. TableGroup绑定相近表:分布式事务关联，压缩关联
            4. 多租户
    5. Linux零拷贝技术
       https://zhuanlan.zhihu.com/p/76640160

3. readings: misc piled up articles
    1. SOSP19' Ceph 的十年经验总结：文件系统是否适合做分布式文件系统的后端
       https://mp.weixin.qq.com/s/cgPrpUo05LFU2Q3bQWSxOw
        1. good
```

More results in the timeline

```
3. readings: misc articles piled up
    1. Zipkin + Slueth tracing for Java by Bytecode interception
       https://mp.weixin.qq.com/s/TpeXPyfoUfQ5ktM0RCljDg
        1. Opensource implementation of Google Dapper
           Twitter opensourced Zipkin
        2. related materials
            1. Java分布式跟踪系统Zipkin（一）：初识Zipkin
               https://blog.csdn.net/apei830/article/details/78722168
            2. springcloud(十二)：使用Spring Cloud Sleuth和Zipkin进行分布式链路跟踪
               http://www.ityouknow.com/springcloud/2018/02/02/spring-cloud-sleuth-zipkin.html
    2. ZGC 原理是什么，它为什么能做到低延时？
       https://www.zhihu.com/question/287945354/answer/458761494
        1. paper: The Pauseless GC Algorithm - 2005
        2. related materials
            1. A FIRST LOOK INTO ZGC - DOMINIK INFÜHR
               http://dinfuehr.github.io/blog/a-first-look-into-zgc/
                1. good
                2. highlights
                    1. "page" groups objects, so that reduces metadata used to manage each
                    2. load barrier (i.e. read barrier) to mark, and relocate.
                        1. (GC thread also do relocate)
                        2. overhead of each reference read.
                            1. ZGC doesn't need write barrier
                    3. a forwarding table, basically a hashmap, to track where an object is relocated to
                        1. only need to forward for pages in relocation set
                    4. stop the world
                        1. still need, expect a few ms. when starting/ending marking, starting relocation.
                        2. stop time irrevalent to heap size

    3. Lindorm是阿里内部HBase分支的别称
       https://zhuanlan.zhihu.com/p/96489404
        1. interesting
        2. highlights
            1. Succinct Trie Tree as index. Higher compression, more index in memory, more cache hits
            2. ZGC, ~5ms pause for n*100 GB heap
            3. lockless
            4. context switch, coroutine for HBase handler
               SEDA, Dragonwell JDK Wips2.0
            5. Indexable Delta Encoding, for HFile randome seek
            6. TableService模型(SQL、二级索引)
               FeedStream模型
               全文索引模型
            7. Faster SkipListMap - CCSMap

    4. TCMalloc 是 Google 开发的内存分配器
       https://zhuanlan.zhihu.com/p/29216091
        1. intersting. This is a 2-years old article.
        2. highligths
            1. Golang用了TCMalloc
            2. basic structure
                1. n*16byte size buddy + linked freelist
                    1. less internal fragmentation than 2^n buddy
                2. page heap, and span heap = n*page size buddy + freelist
                    1. span can spilt into smaller spans and pages
                    2. how to handle external fragmentation?
                        1. merge to spans when page gets back
                        2. how to know page's head/tail span?
                            1. Use RadixTree - the PageMap
            3. CentralCache - now allocator does the object pool for you
                1. how to handle multi-thread racing?
                    1. ThreadCache - thread has local pool, only to fetch CentralCache when exhausted

    5. Flink SQL 如何实现数据流的 Join？
       https://zhuanlan.zhihu.com/p/98417209
        1. highlights. Streaming SQL
            1. Regular Join - needs to visiable full table? all stored, all in mem?
            2. Time-Windowed Join - data cleared out of time window
            3. Temporal Table Join - within time window build the time first, and then join

    6. taosdata/TDengine
       https://github.com/taosdata/TDengine
       https://mp.weixin.qq.com/s/YMcyeO4FO7Je88F85kdXig
        1. interesting
        2. related materials
            1. 浅谈时序数据库TDengine
               https://zhuanlan.zhihu.com/p/75243460
            2. TDengine 与 InfluxDB 对比测试
               https://juejin.im/post/5d80ae15e51d453c11684cff
            3. TDengine简单总结
               https://ifengkou.github.io/TDengine%E7%AE%80%E5%8D%95%E6%80%BB%E7%BB%93.html
            4. TDengine — 高效的时序空间大数据引擎
               https://www.slidestalk.com/u3507/TDengine_An_Efficient_Time_Series_Spatial_Large_Data_Engine
            5. 性能碾压 MySQL、ClickHouse 等，国产开源大数据平台 TDengine 全面剖析
               https://www.infoq.cn/article/ND*aqm6Zrxe8WXaz7j23
                1. 每个设备单独建表，百万个设备百万个表。
                   多表聚合用超级表，超级表限制tags数6
                    1. https://github.com/taosdata/TDengine/issues/173
                2. 超级表STable：多表聚合
                   https://www.bookstack.cn/read/TDengine/9d30aec0fe6774f9.md
            6. TDengine的技术设计
               https://www.bookstack.cn/read/TDengine/9fe77c557d639be9.md

6. Readings: misc articles piled up
    1. SkyWalking 毕业成为 Apache 顶级项目
       https://www.infoq.cn/article/lclYRGCBXTLaM82ue-7W
       https://skywalking.apache.org/zh/blog/2019-03-29-introduction-of-skywalking-and-simple-practice.html
    2. 基于 NVMe SSD 的分布式文件存储 UFS 性能提升技术解析
       https://zhuanlan.zhihu.com/p/102865122
        1. interesting. Similar to Azure Stoage, Stream + Table
           Name: Nebula, FileLayer
        2. questions
            1. what's the specific optimization for NVMe?
    3. 昆仑分布式数据库简介 - 赵伟
       https://zhuanlan.zhihu.com/p/99005057
    4. Kubernetes 疑难杂症排查分享：诡异的 No route to host
       https://mp.weixin.qq.com/s/1DltQsRWSW5pTTTDklzCyQ
    5. 开源史海钩沉系列 [1] Ray：分布式计算框架
       https://zhuanlan.zhihu.com/p/104022670
    6. 图说Cache - Cache的基本原理
       https://zhuanlan.zhihu.com/p/102293437
        1. useful
    7. 关于多核 CPU 自旋锁 （spinlock） 的优化
       https://yq.aliyun.com/articles/698642
        1. interesting
        2. 基于队列的锁:mcs lock简介
           https://www.ituring.com.cn/article/42394
    8. 经典Dual-pool 算法-高效Wear Leveling
       http://www.ssdfans.com/blog/2018/12/30/%e7%bb%8f%e5%85%b8dual-pool-%e7%ae%97%e6%b3%95-%e9%ab%98%e6%95%88wear-leveling/

    9. 分布式系统 in 2010s
        存储之数据库篇: https://zhuanlan.zhihu.com/p/99587904
            1. very good
            2. related materials
                1. 从大数据到数据库: https://zhuanlan.zhihu.com/p/97085692
                2. The Snowflake Elastic Data Warehouse    [2016, 41 refs]
                   http://pages.cs.wisc.edu/~remzi/Classes/739/Spring2004/Papers/p215-dageville-snowflake.pdf
                    1. good. key paper that DB to built native on cloud
                    2. highlights
                        1. virtual warehouse on cloud - 15hrs/4nodes vs 2hrs/32nodes, similar price but much faster
                        2. columnar, vectorized, push-based
        软件构建方式和演化: https://zhuanlan.zhihu.com/p/100325641
        测试和运维: https://zhuanlan.zhihu.com/p/102810526
            1. interesting
            2. related materials
                1. FoundationDB: "Testing Distributed Systems w/ Deterministic Simulation" by Will Wilson
                   https://www.youtube.com/watch?v=4fFDFbi3toc
                    1. good. deterministic flow abstract away OS threading, simulator 100% reproduce distributed bug
                2. eBPF - extented BPF
                    1. interesting. JIT in kernel
                    2. related materials
                        1. eBPF 简史
                           https://www.ibm.com/developerworks/cn/linux/l-lo-eBPF-history/index.html
                        2. BPF: A New Type of Software
                           http://www.brendangregg.com/blog/2019-12-02/bpf-a-new-type-of-software.html
                3. 你呼呼大睡，机器人却在找 bug？
                   https://pingcap.com/blog-cn/sqldebug-automatically/
                    1. good. genius. compare succ and fail commits, trace code and mark the diff by color
                    2. related
                        1. APOLLO: Automatic Detection and Diagnosis of Performance Regressions in Database Systems
                            1. interesting. SQLFuzz, SQLMin, SQLDebug
        硬件的进化: https://zhuanlan.zhihu.com/p/101888725
            1. SSD, Persistent memory / PMDK, 10/25GbE / DPDK, RDMA, SPDK, io_uring
            2. related materials
                1. Intel PMDK - persistent memory programing model
                   https://software.intel.com/en-us/articles/introduction-to-programming-with-persistent-memory-from-intel

    10. TiDB TiFlash
        https://zhuanlan.zhihu.com/p/104740409
    11. Shopee 的分布式数据库实践之路
        https://zhuanlan.zhihu.com/p/101609527

4. readings: misc articles piled up
    1. A Bite Of S3 Storage Arch - tom-sun
       https://zhuanlan.zhihu.com/p/103700905
        1. I wish there is S3 published info but actually not
        n. related materials
            1. HBase MOB
               https://issues.apache.org/jira/secure/attachment/12656011/HBase%2520MOB%2520Design.pdf
            2. 干货 | 如何优雅的通过Key与Value分离降低写放大难题？
               https://mp.weixin.qq.com/s/ClS1xfQsV7Shx0BcE9GJYg
                1. interesting.
                2. highlights
                    1. WiscKey => Hash KV
                        1. segmented GC
                        2. cold hot separation GC
                        3. avoid LSM lookup in GC
            3. How AWS Minimizes the Blast Radio of Failure
               https://www.youtube.com/watch?v=swQbA4zub20
                1. typical. can be used as a reference
                2. highlights
                    1. regions, availability zones
                    2. separating control plane and data plane
                    2. cell architecture
                    3. shuffle sharding
    2. A Bite of Random IO Storage Design-EBS如何设计 - tom-sun
       https://zhuanlan.zhihu.com/p/104726520
        1. 构建方案三: 同时支持随机写和append only的文件系统

2. readings: misc articles piled up
    1. "三高"产品设计的这些坑，你是不是也踩过？（上）- 许健 eBay技术荟
       https://mp.weixin.qq.com/s/bnhXGD7UhwTxL8fpddzAuw
    2. PostgreSQL并行hash join解读 - 北侠
       https://zhuanlan.zhihu.com/p/112003245
    3. 详解CockroachDB事务处理系统 - 吴镝
       https://zhuanlan.zhihu.com/p/26908120
    4. 矛与盾的永恒之战
       https://mp.weixin.qq.com/s/2SxOSMlZ00HPcWrVeBRZzw
       https://mp.weixin.qq.com/s/EUdh3R6ebhnjy8eBrfgpOA
       https://mp.weixin.qq.com/s/iOUe7TAaC7GWaf8xrT763A
    5. (译) io.latency I/O控制器
       https://mp.weixin.qq.com/s/XLnoLU1TM8tCA5kEATEUNQ
    6. FPGA20年最有影响力的25个研究成果 – 其他CAD算法篇
       https://mp.weixin.qq.com/s/nkffBj84qrUhQc6G5kr7vg
    7. 深入理解 Linux 内核--jemalloc 引起的 TLB shootdown 及优化
       https://mp.weixin.qq.com/s/GqJX_KdTeNlWbCIm9096oA
    8. 看了几篇FAST 2020 - 暗淡了乌云
       https://zhuanlan.zhihu.com/p/109774040
    9. 性能测试应该怎么做？ - 陈皓, 2016
       https://coolshell.cn/articles/17381.html
    10. 这多年来我一直在钻研的技术 - 陈皓, 2016
        https://coolshell.cn/articles/17446.html
    11. 与程序员相关的CPU缓存知识 - 陈浩，2020
        https://coolshell.cn/articles/20793.html
    12. 关于高可用的系统
        https://coolshell.cn/articles/17459.html
    13. 别让自己"墙"了自己
        https://coolshell.cn/articles/20276.html
    14. 与程序员相关的CPU缓存知识
        https://coolshell.cn/articles/20793.html
            1. good
    15. 分布式系统的事务处理
        https://coolshell.cn/articles/10910.html
    16. 字节跳动在 RocksDB 存储引擎上的改进实践
        https://mp.weixin.qq.com/s/9L_HOCfRwC_QxjzJyVjKXA
            1. interesting
    17. GeoDNS (Part 1)
        https://mp.weixin.qq.com/s/jDwy8za8V5YY-zhpRJdU3A

3. Readings: recent piled up articles
    1. 译：UE4是如何渲染一帧的
       https://zhuanlan.zhihu.com/p/33865743
       https://zhuanlan.zhihu.com/p/33868831
       https://zhuanlan.zhihu.com/p/118971518
    2. 分析著名游戏如何渲染一帧的文章
       http://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study/
       http://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study-part-2/
       http://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study-part-3/
    3. 一个秒杀系统的设计思考
       https://mp.weixin.qq.com/s/gF6oolXpyHroQE5moc159w
    4. Kernel trace tools（一）：中断和软中断关闭时间过长问题追踪
       https://mp.weixin.qq.com/s/myLa2QAYs-e0b6GURsOvrQ
        1. good innovation
    5. https://mp.weixin.qq.com/s/mtPQLSONUCWOC2HDPRwXNQ
       饿了么交易系统 5 年演化史
        1. very good
    6. 为什么越来越多企业正在往ARM平台迁移？
       https://zhuanlan.zhihu.com/p/134004699
    7. SIGMOD'18|Dostoevsky
       https://zhuanlan.zhihu.com/p/129355502
    8. 2020 存储技术热点与趋势总结
       https://zhuanlan.zhihu.com/p/135188922
        1. good
    9. Linux: AIO 的新归宿：io_uring
       https://zhuanlan.zhihu.com/p/62682475
    10. Socrates: The New SQL Server in the Cloud
        https://www.zhihu.com/people/xie-ti-36

15. Readings: papers about multi-dimensional resource scheduling
    1. readings
        1. Hadoop MapReduce Scheduling Algorithms – A Survey
           https://www.ijcsmc.com/docs/papers/December2015/V4I12201548.pdf
        2. Survey on MapReduce Scheduling Algorithms
           http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.673.4245&rep=rep1&type=pdf
        3. SLA-aware resource scheduling algorithm for cloud storage
           https://jwcn-eurasipjournals.springeropen.com/articles/10.1186/s13638-019-1604-0
        4. Optimal multi-dimensional dynamic resource allocation in mobile cloud computing
           https://www.researchgate.net/profile/Shahin_Vakilinia/publication/279290313_Optimal_multi-dimensional_dynamic_resource_allocation_in_mobile_cloud_computing/links/570d45d208aed31341cf75df/Optimal-multi-dimensional-dynamic-resource-allocation-in-mobile-cloud-computing.pdf
        5. Efficient Resource Scheduling in Data Centers using MRIS
           https://core.ac.uk/download/pdf/25878779.pdf
        6. How to Design a Job Scheduling Algorithm
           https://www.cse.huji.ac.il/~feit/parsched/jsspp14/p2-schwiegelshohn.pdf
    2. thinkings
        1. staging area - online staging, vs batched/queued staging (CSM GC round)
        2. filter step, weighted sort step, score
        3. one algorithm, multiple interfaces (initial placement, replication/migration, space/temperature balancing, deletion)

3. readings: recently piled up articles
    1. 不衰的经典: ARIES事务恢复 [数据库学习的成人试炼] - 阿莱克西斯
       https://zhuanlan.zhihu.com/p/143173278
        1. very good
        2. highlights
            1. non-force, steal
            2. redo log is page-level. undo log is logical; undo's physical is CLR log

2. readings: TiDB new release features
    1. Key Visualizer: Observe Distributed Databases to Discover the Unknowns
       https://pingcap.com/blog/observe-distributed-databases-to-discover-unknowns
        1. https://cloud.google.com/bigtable/docs/keyvis-overview
           https://www.youtube.com/watch?v=aKJlghIygQw

    2. How to Back Up and Restore a 10-TB Cluster at 1+ GB/s
       https://pingcap.com/blog/back-up-and-restore-a-10-tb-cluster-at-1-gb-per-second
        1. why LSM-tree memtable needs to checkpoint SSTables, when we know data is already in log?
            1. data lives in log shortly, eventually they will live in SSTables which are optimized for read (compared to log)
                1. so double-write is a problem, but capacity usable is not a problem
                2. if only metadata is in log, data not, then double-write is not a problem
            2. 华为TaurusDB技术解读（转载）
               https://zhuanlan.zhihu.com/p/64364775
                1. "日志即数据"?
                2. https://zhuanlan.zhihu.com/p/29182627
                    1. should be redo log replication to other nodes

            3. 华为Taurus云原生数据库论文分析
               https://zhuanlan.zhihu.com/p/151086982
                1. paper: "Taurus Database: How to be Fast, Available, and Frugal in the Cloud"
                2. very good. highlights
                    1. "POLARDB通过将Innodb的log和page存放到类POSIX接口的分布式文件系统（PolarFs）来实现计存分离。这种做法看似很美好、对Innodb的侵入非常小，但是却有一些严重的问题，Taurus论文中有提及。 具体来说，大量刷脏的时候，持久化page的网络流量对于计算层、存储层都是一个很大的挑战，因为page流量是单纯log流量的几倍到几十倍不等，具体取决于用户的工作负载。另外，page刷脏会抢占log的持久化需要的资源（网络带宽、IO带宽），增大log持久化的延时，继而增大事务提交的延时。另外，由于PolarFs的基于raft（准确说是ParallelRaft）的数据复制方式，导致事务提交的路径上至少需要两跳网络传输，这个架构导致其需要在计算节点、存储节点都需要引入RDMA来减少网络带来的rt。"
                    2. "计存分离的最优做法是采用“log is database”的理念，只需要把log写到存储层，由存储层负责重放log、回写page并尽量减少写放大。将刷脏这个操作从计算层剔除之后，可以降低计算节点的网络开销。Aurora首先采用这种做法，后续的Socrates、CynosDB、Taurus也均采用这个做法。"
                    3. "Aurora将db的数据（也即是所有page）分成若干个10GB大小的shard，相应的log也随data一起保存在shard中。每个shard有6个副本，采用N=6，W=4，R=3的策略，事务提交时需要等到log在至少4个副本持久化之后才能完成提交。Aurora的log持久化、page读取都只需要一跳网络传输。

                    Socrates也是采用“log is database”的理念，但是它单独了一个log层用于快速持久化log（具体实现不详），避免受到重放log、回写page的影响。另外，page svr层从log层拉取log进行重放、回写page，并向计算节点提供读取page的服务。但是page svr层只将部分page缓存在本地，全量的page在额外的冷备层。所以Socrates的读请求有可能在page svr层本地无法命中，进而从冷备层获取page。

                    CynosDB也是采用“log is database”的理念，从公开资料来看，存储层为计算节点提供了Log IO接口与Page IO接口，前者负责持久化log，后者负责page的读取。

                    Taurus也是采用“log is database”的理念，存储层分为Log Store、Page Store两个模块，前者负责持久化log，后者负责page的读取。log持久化、page读取都只需要一跳网络传输。"
                3. questions
                    1. why redo log (physical log) is smaller size of binlog (logical log)?
                        1. and if a pages is altered many times, sync a page be can smaller than redo log too
                    2. replication by logs rather than pages / full data?
                    3. compared to replicate by data, which can use different sets of nodes as replication chain
                       but logs replication need to lock to a fixed set of nodes? because log needs to know its previous logs to be able to replay
                    4. Storage node needs to rebuild pages from logs
                        which means it needs "history"
                        which means no easy to quickly failover to another storage node
                          to mitigate tail latency
                       So you see, instead of 3-replica 3-writes, Aurora uses quorum append
                        i.e. in 6 replicas, write 4 of them, and only require 3 succeeds.
                    5. LSM-tree seems less affected
                        it can just put data into logs. the memtable only for index
                        or memtable only saves changed data. read old data from cache/old-memtable
                        the flush/checkpoint only writes changed data. no flush unnecessary dirty "page" here

            4. how to do consistent snapshot?
                1. BR only needs to send a snapshot timestamp. TiKV supports timestamp multi-version

        2. how database do checkpoints? large database cannot load all data in memory
            1. https://docs.microsoft.com/en-us/sql/relational-databases/logs/database-checkpoints-sql-server?view=sql-server-ver15
                1. checkpoint only includes in-memory data
            2. https://www.sqlskills.com/blogs/paul/how-do-checkpoints-work-and-what-gets-logged/

    3. TiCDC: Replication Latency in Milliseconds for 100+ TB Clusters
       https://pingcap.com/blog/replication-latency-in-milliseconds-for-100-tb-clusters
        1. TiCDC Open Protocol. row-level data change notification
            for monitoring, caching, full-text indexing, analysis engines, and master-slave replication between different databases
            to third-party data medium such as MQ (Message Queue)
        2. Before version 4.0, TiDB provided TiDB Binlog, which collects binlog data from TiDB and provides near real-time replication to downstream platforms
            1. TiCDC pulls TiDB's data change logs from a TiKV cluster via the Google remote procedure call (gRPC) API and outputs data to downstream platforms

    4. Large Transactions in TiDB
       https://pingcap.com/blog/large-transactions-in-tidb
        1. "Large transactions caused problems for a few reasons:
                they take up a lot of memory in TiDB,
                they keep locks on many keys for a long time,
                which blocks other transactions from making progress,
                and they can exceed their time-to-live (TTL) and be rolled-back even though they are still working"

    5. Pessimistic Locking: Better MySQL Compatibility, Fewer Rollbacks Under High Load
       https://pingcap.com/blog/pessimistic-locking-better-mysql-compatibility-fewer-rollbacks-under-high-load
        1. TiDB now implements both pessimistic and optimistic concurrency control mechanisms
           MySQL supports pessimistic locking by default

    6. SQL Plan Management: Never Worry About Slow Queries Again
       https://pingcap.com/blog/sql-plan-management-never-worry-about-slow-queries-again
        1. old approach: SQL queries (optimizer hints)
        2. TiDB uses a cost-based optimizer that relies on statistics
            1. statistics can abruptly change becoming out of date as front-end application changes
            2. even with correct statistics, it's difficult to ensure that the optimizer chooses the best execution plan for all cases
            3. To avoid these issues, DBAs often try to find slow queries, rewrite SQL queries, or write comments in query statements (known as SQL hints)
                1. problems
                    1. SQL are generated by framework, unable to change directly
                    2. deploy new code introduces risk
                    3. SQL hints quickly become outdated when data distribution changes later
        3. SQL Plan Management
            1. manually bind an execution plan with a type of queries
            2. automatically create bindings for frequent SQL queries
            3. evolve binding: probe with alternative executino plans
                               perform experiments in a predefined period
            4. oracle: https://docs.oracle.com/en/database/oracle/oracle-database/12.2/tgsql/overview-of-sql-plan-management.html

7. readings: misc piled up articles
    1. YARN 在字节跳动的优化与实践
       https://mp.weixin.qq.com/s/9A0z0S9IthG6j8pZe6gCnw
        1. 利用率提升、多负载场景优化、稳定性提升、异地多活

4. readings: misc piled-up articles
    1. Yarn的DRF多维度公平调度算法
       https://lvsizhe.github.io/paper/2017/06/drf-paper-intro.html
       https://lvsizhe.github.io/paper/2017/07/drf-paper-properties.html
       https://lvsizhe.github.io/paper/2017/07/drf-paper-compare.html
        1. Sharing Incentive, Pareto efficient, Strategy proofness
        n. related materials
            1. YARN 在字节跳动的优化与实践
               https://mp.weixin.qq.com/s/9A0z0S9IthG6j8pZe6gCnw
                1. 单个生产集群达到了 2 万节点
                2. interesting. a lot of improvements
            2. Dominant Resource Fairness: Fair Allocation of Multiple Resource Types    [2011, 1056
            refs]
               https://cs.stanford.edu/~matei/papers/2011/nsdi_drf.pdf
                1. very good. the algorithm is ridiculously simple, but the properties are ridiculously good.
                   Sharing Incentive, Pareto efficient, Strategy proofness
                2. highlights
                    1. all properties
                        1. Sharing Incentive:
                        2. Strategy-proofness
                        3. Envy-freeness
                        4. Pareto efficiency
                        5. Single Resource Fairness
                        6. Bottleneck Fairness
                        7. Population Monotonicity
                        8. Resource Monotonicity
                    2. "在证明中将任务看作是可以连续可无限细分的1，即可以启动0.x个的task"
                       "所有用户的Dominant Resource share(后面记为s)同速率的上涨"
                        1. though multi-dimensional, but after normalized, every dimension is same
                           for user A, the diff is only its internal ratio
                            1. dominate share, normalized that different resources have different total amount
                            2. synced grow, keeping dominate share same, normalized that different user submits different sized tasks
                        2. because this synced grow, mostly all resources will be used up at same time
                        3. detailed walkthrough
                            ``
                            # Total resource and consumption of each user task
                            Resource    12      36      72
                            U1          2       6       36
                            U2          3       3       6
                            U3          2       2       8

                            # Normalize different resource amount
                            Resource    1       1       1
                            U1          1/6     1/6     1/2
                            U2          1/4     1/12    1/12
                            U3          1/6     1/18    1/9

                            # Dominate resource share grow in sync, normalize user task size
                            Resource    1       1       1
                            step_U1     1/6     1/6     1/2
                            step_U2     1/2     1/6     1/6
                            step_U3     1/2     1/6     1/3
                            ``
                    3. questions
                        1. "Strategy-proofness: user无法通过虚假声明自己的资源使用量，来获得有利于自己的分配。即，在DRF下，即便用户虚假声明自己的任务资源使用量，也无法让其启动更多的task。"
                            1. But ... a user can declare its task smaller to launch more tasks
                               hope the resource quota is battle proven
                        2. how to apply different weights per user?
                            1. weighted DRF (§4.3), see paper

2. readings: misc piled-up articles
    1. Redis源码中hyperloglog结构的实现原理是什么？
       https://www.zhihu.com/question/53416615/answer/1227317241
        1. very interesting.
           algorithm to count distinct elements. using space overhead log(log(distinct n))
        n. related materials
            1. Performance Tuning Basics 1 : Selectivity and Cardinality
               https://www.zhihu.com/question/53416615/answer/1227317241

1. readings: recent piled up articles (paper level almost)
    1. 字节跳动分布式表格存储系统的演进
       https://mp.weixin.qq.com/s/DvUBnWBqb0XGnicKUb-iqg
       https://mp.weixin.qq.com/s/oV5F_K2mmE_kK77uEZSjLg
        1. very good. understanding ByteDance version of BigTable and Spanner. And to compare with ours
        2. highlights
            1. interesting features
                1. multi-datacenter. replication location, sync/async, cross reads
                2. distributed transaction
                3. load balancing on multi-dimensional resources on heterogeneous + physical/VM machines
                4. global secondary index (not per-partition, but global secondary index)
                5. ByteSQL. Execution optimization, as Read-Write merged in one OP for Insert/Update/Delete
                6. online schema change
            2. looking into future
                1. Offload compaction / GC
                2. analytical columnar storage, HTAP
                3. multi-mode databse: combine Graph, Time-series, Geo data, SQL, non-structured API
                4. more consistency levels e.g. in cross datacenter sync
                5. cloud native, with Kubernetes
                6. distribution transaction cross region TSO, Percolator vs Spanner
        n. related
            1. DFR - Dominate Resource Fairness
                1. used in YARN.
                   https://www.usenix.org/legacy/events/nsdi11/tech/slides/ghodsi.pdf
                   https://people.eecs.berkeley.edu/~alig/papers/drf.pdf
                2. DFR seems can be used in multi-dimensional scheduling in heterogeneous resources in Bytable
                   but how ..?
                n. related materials
                    1. Quasar: Resource-Efficient and QoS-Aware Cluster Management
                       http://csl.stanford.edu/~christos/publications/2014.quasar.asplos.pdf
                        1. OK to be applicable?
                        2. classification for interference and scale-up.
                           Greedy scheduler Allocation and Assignment
            2. TiDB Percolator TLA+
               https://github.com/pingcap/tla-plus/blob/master/Percolator/Percolator.tla
                1. Percolator uses primary key's lock as the synchronization point of committed or not.
                     Read needs to follow up from secondary keys to primary keys to determine committed or not
                   Bytable uses a row in the transaction table as the sync point of committed or not

    2. 数据仓库、数据湖、流批一体，终于有大神讲清楚了！
       https://zhuanlan.zhihu.com/p/140867025
        1. good. very easy and fine explained HSAP, Data Lake, Lambda架构
        2. HASP
            1. Batch：离线计算
            2. Analytical：交互式分析
            3. Servering：高QPS的在线服务
            4. Transaction：与钱相关的传统数据库（绝大多数业务并不需要）

    3. 字节跳动在 Go 网络库上的实践
       https://mp.weixin.qq.com/s/wSaJYg-HqnYY4SdLA2Zzaw
        1. Nocopy Buffer

    4. Practical Fast Replication
       https://zhuanlan.zhihu.com/p/59991142
        1. paper: NSDI 2019 "Exploiting Commutativity For Practical Fast Replication"
        2. "witness" node to add additional "abilities" to existing replication facility

    5. Amazon Aurora 深度探索 - 腾讯技术工程
       https://zhuanlan.zhihu.com/p/33603518
        1. though written 2 years ago only for Aurora Single master, but still good worth reading
            author's comments are also interesting
        2. questions and thinkings
            1. Aurora Singe master
                1. the master node replicas logs to storage node, and in quorum commit way.
                   storage node in charge of everything else, e.g. redo to pages, conflict detection
                   storage node simply sequentially write logs to disk, and then sync back to master writer
                    1. this means even there is only one master, the master is very lightweighted, to support high throughput for transaction
                        1. design principle "minimizing master node write delay"
                    2. everything possible is offloaded to storage layer, which is a distributed layer
                2. "log is database"
                    1. replicating logs to storage rather than flush back pages is more efficient. because pages mix with unrelated data
                    2. LSM-tree if well-implemented should not have this problem, because only delta-data needs flush, not like flushing entire page
                    3. actually, you cannot store all logs forever. there is a VDL to point min log kept.
                       there is a concept that a "checkpoint" of pages need to present to keep the oldest snapshot of data
                        1. these "pages" are stored to AWS S3, smart. so, it's OK to call "log is database" as Aurora only stores pages
            2. Aurora multi-master
                1. Allow more master nodes to send logs to storage node.
                   for conflict resolving, the key is storage node, who is the sync point of conflicting pages
                2. How to guide user requests to different masters to avoid conflict? I didn't find any materials mentioning it
                    1. if related requests are send to different masters, it's easy to trigger conflicts, thus slow down overall throughput
                    2. thus you'll need a propoer partition strategy, who can do this partition for customers? I didn't see mentioning
                        1. secondly, with partition, you again introduced the need of cross master distributed transactions. how's that done?
                           the story of aurora multi-master isn't ending
                        2. thirdly, how a master is mapped to storage nodes? storage nodes must have certain partition policy to own pages
                            1. as the Author suggests, transaction data can be pushed to page level,
                               managed by storage nodes, and then be able to share acorss master nodes

4. readings: Alibaba 全图化引擎
    1. 从HA3到AI·OS -- 全图化引擎破茧之路
       https://developer.aliyun.com/article/674172
    2. 淘宝千人千面背后的秘密：搜索推荐广告三位一体的在线服务体系AI·OS
       https://zhuanlan.zhihu.com/p/208751474

3. Readings: misc articles piled up
    1. 卡尔曼滤波
       https://zhuanlan.zhihu.com/p/39912633
    2. 定点数优化：性能成倍提升 - 韦易笑
       Compiler Explorer - Analysis (llvm-mca (trunk))
       https://zhuanlan.zhihu.com/p/149517485
       https://quick-bench.com/q/FqOYuExcXoyHe_r6Bl1oSm0wUPE

4. Readings: recent piled up articles
    1. YougaByte DB vs CockroachDB
        0. https://zhuanlan.zhihu.com/p/285108593
        1. https://www.yugabyte.com/yugabytedb-vs-cockroachdb/
        2. https://blog.yugabyte.com/yugabytedb-vs-cockroachdb-bringing-truth-to-performance-benchmark-claims-part-2/
            1. "Yugabyte SQL is based on a reuse of PostgreSQL’s native query layer"
            2. "YugabyteDB’s DocDB (RocksDB-based storage layer) is engineered from the ground up"
            3. "Yugabyte SQL outperforms CockroachDB by delivering 3x higher throughput and 4.5x lower
            latency on average using YCSB tests"
                1. GO-JEK’s Performance Benchmarking of CockroachDB, TiDB & YugabyteDB on Kubernetes
                   https://medium.com/yugabyte/go-jeks-performance-benchmarking-of-cockroachdb-tidb-yugabyte-db-on-kubernetes-9fde0127b00
                    1. conforms with YugabyteDB has much better perf.
                    1. CockroachDB latency is ridiculous high/bad ..?

        3. https://db-engines.com/en/system/CockroachDB%3BYugabyteDB
            1. "CockroachCloud"
            2. CockroachDB is implemented with Go lang, while YogabyteDB in C++
            3. YogabytesDB supports Stored Procedure, Triggers
            4. YogabytesDB uses "Wide column store" / i.e. the document store
            5. YogabytesDB support NoSQL interface
                1. this is clever .. since underlyingly it is already built with DocDB / RocksDB
            6. all YogabytesDB and CockroachDB and TiDB use Raft replication for partitions
                1. YogabytesDB use 3-replica raft quorum.
                    1. my remark / question: we definitely don't want the quorum to be unavailable when 1 replica is dead. but as far as I read, this can happen in YogabytesDB.
                        1. a good solution would be to redirect to a new quorum when 1 replica failure.
                           Azure Storage does it .. by nature .. due to separation of storage vs table
                        2. coupling storage and table also makes partition migration, split/merge harder.
                           but good side is there is less metadata to keep for pure storage side.
            7. both YogabytesDB and CockroachDB are designed to be globally geo-distributed
            multi-datacenter
            8. CockroachDB doesn't support "follower read"?
                1. CockroachDB supports follower read, but enterprise-only, and relaxed consistency
                   https://www.cockroachlabs.com/docs/v19.2/follower-reads.html
                    1. "Currently, follower reads are available for any read operation at least 48 seconds in the past, though there is active work to reduce that window"
                    2. how it works?
                        1. the implementation relaxed consistency
                            1. "In CockroachDB's general architecture, all reads are served by a range's leaseholder, which is a replica elected to coordinate all write operations"
                            2. "However, if you were to lower the isolation requirements of an operation, it's possible to serve the read from any replica, not only the leaseholder"
                            3. "Each CockroachDB node tracks a property called its "closed timestamp", which means that no new writes can ever be introduced below that timestamp"
                               "With follower reads enabled, any replica on a node can serve a read for a key as long as the time at which the operation is performed (i.e. the AS OF SYSTEM TIME value) is less or equal to the node's closed timestamp"
        4. Hacker news: How does YugaByte compare to CockroachDB?
           https://news.ycombinator.com/item?id=20454053
            1. feature matrix: https://docs.yugabyte.com/latest/comparisons/
                1. useful. compare across CockroachDB, TiDB, Aurora, CosmosDB, Spanner, MongoDB, FoundationDB, Cassandra and Dynamo

        5. https://blog.yugabyte.com/ysql-architecture-implementing-distributed-postgresql-in-yugabyte-db/
            1. https://docs.yugabyte.com/latest/architecture/concepts/sharding/
                1. good hash sharding vs range sharding compare
                    1. cons of range sharding
                        1. "Firstly, when starting out with a single shard implies only a single node is taking all the user queries. This often results in a database “warming” problem"
                            1. my remark / question: foundamentally, this is sharding overloaded data balancing, query consecutiveness, hotness balancing roles
                        2. "Secondly, globally ordering keys across all the shards often generates hot spots: some shards will get much more activity than others"
                            1. "While these can be mitigated to some extent with active load balancing, this does not always work well in practice because by the time hot shards are redistributed across nodes, the workload could change and introduce new hot spots"
                            2. my remark / question: this is not always a drawback of range sharding. range sharding allows customize placement to balance hotspots, while hash sharding not as easy (unless using virtual nodes).
            2. https://docs.yugabyte.com/latest/architecture/concepts/replication/
            3. https://docs.yugabyte.com/latest/architecture/concepts/persistence/
            4. https://docs.yugabyte.com/latest/architecture/concepts/yql/
            5. https://docs.yugabyte.com/latest/architecture/transactions/distributed-txns/
                1. https://docs.yugabyte.com/latest/architecture/transactions/transactional-io-path/
                    1. question: read needs separated query to Txn status table? a penalty as not colocating Txn status/versioning with paxos primary.
                        1. "It makes sense to select a transaction status tablet in a way such that the transaction manager's tablet server is also the leader of its Raft group"
                           "But in the most general case, the transaction status tablet might not be hosted on the same tablet server that initiates the transaction"
                           "As each participating tablet reads from its local DocDB, it might encounter provisional records for which it does not yet know the final transaction status and commit time. In these cases, it would send a transaction status request to the transaction status tablet"
                2. "provisional records" the uncommited values are persistent in another RocksDB instance
                3. https://docs.yugabyte.com/latest/architecture/transactions/transactions-overview/
                    1. YugabyteDB uses Hybrid Logical Clocks (HLCs)
                    2. "lockless multi-version concurrency control (MVCC) in YugabyteDB"
                        1. also gets  similar "read wait" problem, as mentioned in Clock-SI paper
                            1. "The need to read from a tablet at a particular timestamp arises during transactional reads across multiple tablets. This condition becomes easier to satisfy due to the fact that the read timestamp is chosen as the current hybrid time on the YB-TServer processing the read request, so hybrid time on the leader of the tablet we're reading from immediately gets updated to a value that is at least as high as the read timestamp. Then the read request only has to wait for any relevant entries in the Raft queue with timestamps lower than the read timestamp to get replicated and applied to RocksDB, and it can proceed with processing the read request after that"
            6. highlights
                1. YogabyteDB reuses PostgreSQL layer for compatible
                2. YogabyteDB implments DocDB which is key for performance improvements
                    1. and also, YogabyteDB uses C++ rather than Go lang. No Go lang GC.
                    2.
                3. YogabyteDB also exposes NoSQL interface (Cassandra, Redis), leveraging the KV store underlying
                4. didn't see special addressing for OLAP
                    1. https://docs.yugabyte.com/latest/faq/general/
                       "YugabyteDB is not a good fit for traditional Online Analytical Processing (OLAP)"
                        1. use Druid or Snowflake instead
                5. How can YugabyteDB be both CP and ensure high availability (HA) at the same time?
                   https://docs.yugabyte.com/latest/faq/general/#how-can-yugabytedb-be-both-cp-and-ensure-high-availability-ha-at-the-same-time

        6. https://laptrinhx.com/follow-up-evaluating-cockroachdb-vs-yugabytedb-webinar-2251458949/
            1. Architectural takeaways
                1. "Use of RocksDB: CRDB unevenly uses multiple disks; whereas YugabyteDB has an even split of data across the two disks."
                2. "Compactions affect performance: CockroachDB’s lack of timely compactions have a huge negative impact on read performance; whereas compactions in YugabyteDB were able to keep pace with the data load thereby maintaining low SSTable file count and read amplification."
                3. "Backpressure vs no back pressure: CockroachDB was not able to throttle write requests, which impacted the read performance and the cluster had to be left idle for many hours to recover. By contrast, the load throughput graph of YugabyteDB shows that the database repeatedly applies backpressure on the loader to make sure the read queries would always perform well."

3. readings: CephFS MDS metadata tree operations and transaction
    1. Dynamic Metadata Management in CephFS
       https://www.bookstack.cn/read/ceph-en/bdc93f169737d2fd.md
        1. Distributed Locks in an MDS Cluster
           https://www.bookstack.cn/read/ceph-en/f86f8e1a8d1e7e8a.md
            1. metadata cache can be distributed among MDS
            2. within which, only one MDS is the authoritative MDS
            3. non-authoritative MDS can acuqire Read locks
        2. MExport message
        3. In CephFS, directories are fragmented when they become very largeor very busy
        4. Mantle: A Programmable Metadata Load Balancer for the Ceph File System
           https://www.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-15-10.pdf
            1.  CephFS's dynamic subtree partitioning
    5. cephfs: MDS处理mkdir
       https://zhuanlan.zhihu.com/p/100102030
       https://zhuanlan.zhihu.com/p/138086811
       https://zhuanlan.zhihu.com/p/143090219
    6. CephFS MDS内部锁介绍
       https://juejin.cn/post/6844903742450434056
    7. CEPH MDS lock mechanism implementation (unfinished)
       https://www.programmersought.com/article/1277796075/
    8. ceph作为一个分布式文件系统，整体架构是怎么样的
       https://www.zhihu.com/question/308282522/answer/568234592
        1. "客户端会发出caps消息请求锁，拿不到想要的caps会睡眠等待，这么属于业界经典的客户端行为设计了。服务端即mds进行中心化管理，要想切换lock，修改lock状态，必须在中心（或主）mds进行，其他mds只是保留副本，方便客户端读取，这样就通过消息传递把lock的中心化控制做在了元数据服务器mds。"
    9. 浅谈分布式系统元数据服务器设计
       https://zhuanlan.zhihu.com/p/85008536

5. readings: clear the weichat pending read
    1. good ones
        1. Ceph冷知识 | Cache Tier 的抉择与使用
           http://mp.weixin.qq.com/s/w39cEMBtV8bCI1k_2PR2vA
        2. 预算892万元的政务云项目，又0.01元中标了！
           https://mp.weixin.qq.com/s/70MHFCIqW9dl7tRHj46BeQ
        3. OpenStack：云之梯》连载三：搭建 OpenStack 团队
           http://mp.weixin.qq.com/s/8tPjTdEJFqRnC9v08TR3Hg
        4. 看云计算里的资源"超卖" (1)
           http://mp.weixin.qq.com/s/9GpVNTG_bNkqzPvX42dpsw
        5. 简单测试验证NUMA对内存带宽性能的影响
           http://mp.weixin.qq.com/s/s0o59e3gjYWaLTMI8rjqSQ
        6. Jupiter Rising -Google数据中心网络演进之路(1)
           http://mp.weixin.qq.com/s/hQHuv4Pjm4dutepjcPhKxA
            1. TCP incast and outcast problem
                1. https://pdfs.semanticscholar.org/bb38/6b1986cbef4d2d3aa833f6e3b273f757eeb1.pdf
                2. http://oversea.cnki.net/Kcms/detail/detail.aspx?filename=1013038128.nh&dbcode=CMFD&dbname=CMFD2014
                3. http://www.sciencedirect.com/science/article/pii/S1084804516300649
                4. TCP Incast and Cloud application performance
                   http://bradhedlund.com/2011/05/01/tcp-incast-and-cloud-application-performance/
                5. TCP incast: What is it? How can it affect Erlang applications?
                   http://www.snookles.com/slf-blog/2012/01/05/tcp-incast-what-is-it/
                6. The TCP Outcast Problem: Exposing Unfairness in Data Center Networks
                   https://www.usenix.org/node/165730
            2. the paper: Jupiter Rising: A Decade of Clos Topologies and Centralized Control in Google's Datacenter Network
               https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43837.pdf
                1. just did a quick read. http://mp.weixin.qq.com/s/hQHuv4Pjm4dutepjcPhKxA is usable start
                2. related readings
                    1. Data Center TCP (DCTCP) (Microsoft Research)    [2010, 909 refs]
                       https://www.microsoft.com/en-us/research/publication/data-center-tcp-dctcp/
                       https://habr.com/en/post/474282/
                        1. good paper. this is the classic TCP improvement, supported by commodity switches, to address TCP incast, queue buildup, buffer pressure problems
                           the results looks quite good: 10X background traffic, while 10X foreground traffic does not cause any timeouts
                            1. referenced as [3] in "Jupiter Rising: A Decade of Clos Topologies and Centralized Control in Google's Datacenter Network"
                        2. key points
                            1. DCTCP leverages Explicit Congestion Notification (ECN) in the network to provide multi-bit feedback to the end hosts
                                1. maintain queue length "should-be" less than K
                                2. essentially, DCTCP by reacting to congestion in proportion to the extent of congestion
                                    1. by using the marking bits, in the response get from ECN
                                    2. and the a and cwnd iteration formula
                            2. address to the TCP incast problem, and the aggregrate/partition application pattern
                                1. besides incast
                                    1. Query and delay-sensitive short messages experience long latencies due to long flows consuming some or all of the available buffer in the switches
                                    2. queue buildup impairment: even when no packets are lost, the short flows experience increased latency
                                                                 as they are in queue behind packets from the large flows
                                2. learnings
                                    1. switch buffer occupancies need to be persistently low, while maintaining high throughput for the long flows.
                                       DCTCP is designed to do exactly this
                            3. The TCP literature is vast, and there are two large families of congestion control protocols that attempt to control queue lengths
                                (i) Delay-based protocols use increases in RTT measurements as a sign of growing queuing delay, and hence of congestion.
                                    These protocols rely heavily on accurate RTT measurement, which is susceptible to noise in the very low latency environment of data centers.
                                    Small noisy fluctuations of latency become indistinguishable from congestion and the algorithm can over-react.
                                (ii) Active Queue Management (AQM) approaches use explicit feedback from congested switches.
                                     The algorithm we propose is in this family
                        n. related materials
                            1. DCTCP（背景和原理）
                               https://zhuanlan.zhihu.com/p/430215470
                                1. problems to solve
                                    1. Incast：对于查询流而言，mant-to-one的通信模式导致在聚集交换机处发生拥塞
                                    2. Queue buildup：长流对缓存区的占用，导致短流排队
                                    3. Buffer pressure：共享的缓存区，导致其他端口的长流影响本端口的短流的传输
                                2. Algorithms
                                    1. 交换机处简单标记
                                       我们在交换机处设置阈值K，如果数据包达到交换机时，其队列占用值大于，则在CE点标记该数据包。
                                        1. This is the same with DCQCN
                                    2. 接收者回传ECN信息
                                       接收端收到ECN标记的数据包后，回传带有ECE（ECN-echo）标记的ACK给发送端，发送端根据规则调节发送窗口，实现拥塞避免。
                                        1. DCQCN sends back CNP rather than ECN back to sender side. DCQCN ensures at most send one CNP in a given time window
                                        2. The RoCEv2 standard defines explicit Congestion Notification Packets (CNP) for this purpose. Processing a marked packet, and generating the CNP are expensive operations, so we minimize the activity for each marked packet
                                    3. 发送方拥塞控制
                                       发送方根据到达的标记的包的比例，来调整拥塞窗口的大小。DCTCP的核心是拥塞程度a的估计， 在每次发送完一个窗口后（一个RTT）更新
                                        1. DCQCN's version is more fine grained
                            2. HPCC和DCTCP的性能对比
                               https://zhuanlan.zhihu.com/p/368727972
                            3. Datacenter TCP, Incast Problem & Partition-agg timing | Network Traffic Analysis Ep. 17 | CS4558
                               https://www.youtube.com/watch?v=BoJrQ5mvLec
                                1. useful illustration.
                                   the key is to use a small switch buffer (queue length) so latency is low, but also maintain high throughput without easily cause congestion
                                   setting a large switch buffer is bad for latency

        7. 网络产品及硬件架构
           http://mp.weixin.qq.com/s/MC5sHlHdvVat0iNi7qpF2g
        8. 谈谈10G光模块(1)
           http://mp.weixin.qq.com/s/YpTaJhYjnf7zlTVGxdoGig
        9. 运营商网络简介
           http://mp.weixin.qq.com/s/wNkHD1c3_8VTN9Ila7_EqA
        10. GitLab想离弃云，但...
           http://mp.weixin.qq.com/s/YFSANJpAdyU538a6KjUe_A
            1. the comments are interesting. there are a lot of experience
            2. they got a lot of community support
```

Business visions.

```
1. Readings: Vision: Case Interview Secrets - Victor Cheng
   https://www.caseinterview.com/
    1. use proxy for estimation
        1. match you intuition and find proxy via
            1. relevance links
            2. history or similar peers
            3. population breakdown
        2. improving the proxy
            1. break the problem into different aspects and find multiple proxies
            2. finding different proxies from different layers for the same problem, and cross validate
            3. segmenting the proxy to confine the imperfect proxy issue
        3. comparing interview estimation problem vs real storage vision
            1. interview has limitted time, no google, no knowledge background, no calculator. the general questions are general product-sales-revenue
            2. but targeting for storage area, we can borrow many knowledge, no time limit and use complex model and simulation, shadow peer works. so a lot questions become easier
    2. Consultent Sense
        1. Independent Problem Solver
            1. Can I drop you off with a division of a Fortune 500 company by yourself, with little to no supervision? Can you handle the client, solve the problems, and in the process make teh firm looks good?
        2. Doing as Little as Possible vs Boiling the Ocean
            1. What is the "key information" to answer client's questions?
               How do the as little as possible to finish the quest?
        3. The Airplane Test (aka Don't Be an Asshole)
            1. Would I want to spend three hours sitting next to you on an airplane?
        4. Tooling
            1. Hypothesis
                1. Always Hypothesis first. Hypothesis dictate what customized Issue Tree you use
            2. Issue tree/framework/template
                1. Validated by
                    1. Always have Hypothesis first. Issue tree is dedicated to hypothesis, don't blindly borrow a framework for certain area
                    2. the MECE test
                    3. Victor Cheng's conclusiveness test: If all branches are true, you cannot reject the conclusion. To accept/reject the conclusion, you don't need less/more branches
            3. Drill-down analysis, goback and re-structure again
                1. process of elimination on false branches, until the final one left to point the true conclusion
            4. Synthesis: action-oriented, concise, big picture integrated with detailed analysis
    3. Issue tree frameworks
        1. Profitability framework: Revenue (price/#unit sold), (variable/fixed) cost
        2. Business situation framework: Customer, product, company, competition
        3. some tips
            1. Always do comparison, to historical data, to external competitors
            2. Company specifc issue, or industry wide issue?
            3. Combine both qualitive questions and quantitive questions 
            4. Segementation and process-of-elimination
            5. Linear thinker, rationalize each decision choice taken, as be thoughtful
            6. P173 the live case Frameworks in action. This chapter is very good
    4. more captures
        1. Record and replay, until you get every wording sythesis right
        2. Brainstorm ideas but with structured categories heuristics, MECE mining, comination iteration
        4. Presentation slides：each title should give the point (rather than description), the all titles together should tell a complete story - synthesis

4. readings: finish the recent WeiChat articles
    1. Facebook开源LogDevice：一种用于日志的分布式数据存储系统
       https://mp.weixin.qq.com/s/rJby2i4eUrY_qweOwp8XHQ
       https://code.facebook.com/posts/357056558062811/logdevice-a-distributed-data-store-for-logs/
        1. good to read
        2. highlights
            1. LogDevice record placement is different from HDFS (metadata approach) and Ceph (hash approach)。每个"R"或"G"（估计是不同的log stream或compent分类什么的）
               有固定的存储节点集。节点集实际上是允许log往这些节点里同时写入，最大限度地保证写入速度和写入tail latency tolerate（牺牲读效率）；这确实适合日志写这种场景。日志记录
               也在节点集中复制里2到3个副本。读取器联系节点集中的所有节点，自己做去重和排序。为了优化读效率，LogDevice保证每个log记录只有一个副本服务器从磁盘读取；这是通过把副本集（copy set）
               附加到每个log record的header实现的。
            2. 序号epoach:seq设计很巧妙，只有epoach递增（对应sequencer server crash）需要paxos保存，seq严格递增则只需要一台轻量的sequencer server即可。
               而不同的"R"和"G"（应该是对应不同log stream），可以分别用不同的log sequencer服务；"R"和"G"的epoach不同，对应关系由epoach paxos保存。这感觉是学了megastore。
               这种方式下，有了一个高效的全局sequencing方案。paxos的优化思路就是，把轻量的功能下放给SPOF的服务，自己管高层，同时还保证容忍层服务挂了不影响逻辑正确。
               这种多层代理的方式，确实增加了paxos的吞吐量；而paxos本身之管最顶上一层了。Ceph的paxos只管metadata，也有这个思路的影子。
    2. 深入浅出阿里云新一代关系型数据库 PolarDB
       https://mp.weixin.qq.com/s/Chqd-HSRQmSpuKcqJNnUwQ
        1. 跟进Amazon的Aurora，基于MySQL的云RDS服务。
           不同于原RDS，PolarDB的计算和存储分离，存储使用共享存储。
           类似Aurora，redolog和数据文件从在共享存储上。网络使用RDMA。
        2. others
            1. OceanBase
               https://www.zhihu.com/question/19841579
                1. transaction writes in memory, only journal to disk (SSD).
                   at night, data batch commit to disk (SSD). (all sequential write)
                   three zones in turn do night batch commit.
                2. 支撑蚂蚁双十一交易支付流量
                   http://velocity.oreilly.com.cn/2016/index.php?func=session&id=26
                   https://yq.aliyun.com/articles/217
                3. Questions
                    1. 基线数据在SSD，修改在内存。读怎么serve？
    3. 曹亚孟 - 中国云计算现状
        1. 成本篇： https://mp.weixin.qq.com/s?__biz=MzI3MzAzNDAyMQ==&mid=2657598340&idx=1&sn=0f417c8d04fd484bf0f4d2dbc331cd59
        2. 采购篇: https://mp.weixin.qq.com/s?__biz=MzA5MjA2MjgyNg==&mid=2649901141&idx=1&sn=d3107c14bebee710850a49d51de678f9
        3. 产品篇： https://mp.weixin.qq.com/s?__biz=MzI3MzAzNDAyMQ==&mid=2657598771&idx=1&sn=cf9ff35a396978074ab3739fb30f6a88
        4. 盈利篇： https://mp.weixin.qq.com/s?__biz=MzI3MzAzNDAyMQ==&mid=2657598340&idx=1&sn=0f417c8d04fd484bf0f4d2dbc331cd59
            1. 销售部分讲得很好好；good to read
    4. 史无前例开放！阿里内部集群管理系统Sigma混布数据
       https://mp.weixin.qq.com/s/4-7LLacEksMGfw6eZPz53w
       https://github.com/alibaba/clusterdata
    5. Mirantis: Is Kubernetes Repeating OpenStack's Mistakes?
       https://www.mirantis.com/blog/is-kubernetes-repeating-openstacks-mistakes/?from=timeline
    6. 没有绝对安全的系统：写在AES 256破解之后
       https://zhuanlan.zhihu.com/p/28089365?utm_medium=social&utm_source=wechat_timeline&from=timeline
        1. 使用专有的硬件来完成密码学操作(FPGA impl)，就可以很好地防御这类攻击了
    7. 同程容器云平台网络方案演进
       https://mp.weixin.qq.com/s/MqGI_l5bbWM1sdigDo65Bg
        1. 隧道方案：Weave，OVS，Flannel
            缺点：随着节点规模增长，复杂度上升，网络问题不好跟踪，性能损失严重
           路由方案：Cailco，Macvlan
            性能更好，但依赖BGP，侵入传统物理网络，频繁变更物理路由器的配置
           Vlan方案：Contiv netplugin，pipework
            Contiv由思科推出，支持ACI，性能到物理网卡95%，master挂了不影响网络，基于ovs可以灵活地做Policy/ACL/Qos监控
            最终选择使用Contiv netplugin
        2. 实现了container迁移后，容器IP不变（IP持久化）
        3. 网络监控使用ovs的sflow
        4. 深度解密京东登月平台基础架构
           https://mp.weixin.qq.com/s/uyhlp4oBV5VKc-eapKRsMw
    8. 深度解密京东登月平台基础架构
       https://mp.weixin.qq.com/s/uyhlp4oBV5VKc-eapKRsMw
    9. 分布式存储Ceph 架构及性能调优实践
       https://mp.weixin.qq.com/s/4mE5k6yfF-rinMHeBpe59w
    10. 万字长文 | 详解优维科技内部DevOps研发实践 | 演讲实录
        https://mp.weixin.qq.com/s/_moAftumbmxb4wBQfMO48Q
    11. 美团云《纠删码存储系统中的投机性部分写技术》在国际顶级技术大会USENIX ATC上发表
        https://mp.weixin.qq.com/s/2ku_PqzaSKh9rMVHeaKaqg
        1. good improvement. handles updates in EC fragments
        2. 在SSE、AVX等向量运算指令集的帮助下，现代CPU的1个核心每秒就能完成5~13GB数据量的编解码工作，
           远远大于同时期各种外部存储设备的吞吐率，所以编解码运算已不再成为EC存储系统的瓶颈
    12. Synthesizing Obama: Learning Lip Sync from Audio
        http://grail.cs.washington.edu/projects/AudioToObama/siggraph17_obama.pdf
        1. very interesting. good to take a look. video: https://www.youtube.com/watch?v=9Yq67CjDqvw
        2. using RNN. this technology can be used in Skype, Facebook, etc video chats
    13. 麦子迈 Ceph开发每周谈
        https://mp.weixin.qq.com/s/tm9uKZFZm-3ekbq5lTu8Sw
        https://mp.weixin.qq.com/s/GR6AnKqgnNBd_7K3WJf0sw
        false sharing: https://mp.weixin.qq.com/s/BKBwNb0JyuqOjgeHw4MkWA
        SPDK BlobStore: https://mp.weixin.qq.com/s/IfIie34YOxXtTbvsng3L0A
            1. think about MS LLAMA storage layer
        OpenStack 2017 用户调研: https://mp.weixin.qq.com/s/h-sMMm_ENQoDHmUHWU6ejA
        CRUSH 不均衡问题: https://mp.weixin.qq.com/s/7Djv7rgo-Lv0nlVMV0kLLA
        rbdcache CPU消耗: https://mp.weixin.qq.com/s/eZgg_gEr2GBZSqAyXfWBsQ
        Ceph 去重: https://mp.weixin.qq.com/s/z47TT8mfGHT61iL2312H0A
        https://mp.weixin.qq.com/s/8qPNt-9YdVjFtr4hcK3S3Q
        Ceph Day Beijing: https://mp.weixin.qq.com/s/e7rtVcF8CjnFsmWRQ6FqOg
            1. ceph day beijing agenda: https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-welcome-to-beijing-ceph-day
            2. slides
                1. Ceph Day Beijing - Ceph All-Flash Array Design Based on NUMA Architecture
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-ceph-allflash-array-design-based-on-numa-architecture?next_slideshow=1
                2. Ceph Day Beijing - Optimizing Ceph Performance by Leveraging Intel Optane and 3D NAND TLC SSDS
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-optimizing-ceph-performance-by-leveraging-intel-optane-and-3d-nand-tlc-ssds?qid=fe7dce42-8e43-49be-b5a3-96847182d5a2&v=&b=&from_search=3
                3. Ceph Day Beijing - Our journey to high performance large scale Ceph cluster at Alibaba
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-our-journey-to-high-performance-large-scale-ceph-cluster-at-alibaba?qid=fe7dce42-8e43-49be-b5a3-96847182d5a2&v=&b=&from_search=5
                4. Ceph Day Beijing - Ceph RDMA Update
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-ceph-rdma-update?qid=fe7dce42-8e43-49be-b5a3-96847182d5a2&v=&b=&from_search=6
                5. Ceph Day Beijing - Small Files & All Flash: Inspur's works on Ceph
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-small-files-all-flash-inspurs-works-on-ceph?qid=fe7dce42-8e43-49be-b5a3-96847182d5a2&v=&b=&from_search=7
                6. Ceph Day Beijing - SPDK for Ceph
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-spdk-for-ceph?qid=fe7dce42-8e43-49be-b5a3-96847182d5a2&v=&b=&from_search=8
                7. Ceph Day Beijing - Leverage Ceph for SDS in China Mobile
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-leverage-ceph-for-sds-in-china-mobile?qid=fe7dce42-8e43-49be-b5a3-96847182d5a2&v=&b=&from_search=10
                8. Ceph Day Beijing - BlueStore and Optimizations
                   https://www.slideshare.net/DanielleWomboldt/ceph-day-beijing-bluestore-and-optimizations?qid=fe7dce42-8e43-49be-b5a3-96847182d5a2&v=&b=&from_search=11
        LMDB: https://mp.weixin.qq.com/s/4cf6v4vLIq0Df0ZWmVH6NA
            1. PR: https://github.com/ceph/ceph/pull/4403
        https://mp.weixin.qq.com/s/Wo_yVNP5-KQXq_Rd8lsD_Q
        Open Channel SSD: https://mp.weixin.qq.com/s/gLRDRwwHChME7YFCKNaaWg
            1. LightNVM
        https://mp.weixin.qq.com/s/6vS5LzruoAoX8caYHW_7rA
        https://mp.weixin.qq.com/s/DoxO_PBcQ7fF8VjDwZx0Pw
        ObjectStore性能新数据: https://mp.weixin.qq.com/s/__xKjWi9y55di52QG1D19w
        Ceph新社区经理: https://mp.weixin.qq.com/s/jkE_a0jVfzT6TxyzCjtTgg
        Ceph Client Cache: https://mp.weixin.qq.com/s/DpmJ7C92Ke0IASZQIM7aZQ
        Rados Level Replication: https://mp.weixin.qq.com/s/6OryLe6m4vT-FFoHPQd8mQ
            1. from Qihoo 360: http://tracker.ceph.com/attachments/download/2903/ceph_rados-level_replication.pdf
        RocksDB Multi Column Family Performance: https://mp.weixin.qq.com/s/f1CctA8V492oAhCWqKd3Pg
            1. 很多用户问 CephFS 的多 Filesystem 特性是否安全，John 之前回应了这个特性并不是很好的测试覆盖，而且存在漏洞，
               用户在安全层面仍然能够访问所有 FS，而且不排除存在明显问题。
        Luminous 特性: https://mp.weixin.qq.com/s/co0GXRrtbrrMEC16sotu4A
            1. BlueStore:
                在 Luminous，BlueStore 大约经历了若干时间的稳定开发后，已经可以一用，特别是在对象存储场景，相信各方面性能和稳定性都能超越 FileStore。
                但是目前仍然有几个潜在风险，
                    第一个是内存消耗，BlueStore 虽然针对分配容量能够做控制，当时实际容量消耗仍然更大，大约在 1.5x 相较于默认 BlueStore cache memory 配置。
                    第二个是老生常谈的元数据缓存问题，在元数据大部分命中情况下，有较好的性能结果，但是当元数据超过 SSD 容量时，这个时候性能下降是非常大的，但是目前这个性能下降是无声的，对大量用户使用会有较大影响。
                    第三个是块存储性能上，基于目前的情况来看，在闪存下性能可以大致相当于 FileStore，但是延迟会更高，在 HDD 情况下性能会好一些，在大块场景下，可以完全超越 FileStore，目前主要是小块性能仍然不足。
                如果基于想尝试 Luminous 的生产用户，仍然推荐用 FileStore 先行，目前社区仍然太缺乏 BlueStore 的用例和实践，会存在较大运维困难和问题触发。
        https://mp.weixin.qq.com/s/0YZbm-w0shMJZnZtwj0SIg
```
