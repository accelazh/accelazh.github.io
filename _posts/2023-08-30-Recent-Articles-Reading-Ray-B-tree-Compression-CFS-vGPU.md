---
layout: post
title: "Recent Articles Reading: Ray, B-tree Compression, CFS, vGPU"
tagline : "Recent Articles Reading: Ray, B-tree Compression, CFS, vGPU"
description: "Recent Articles Reading: Ray, B-tree Compression, CFS, vGPU"
category: "storage"
tags: [storage, paper, database]
---
{% include JB/setup %}


```
1. 学术研究中，有了一个不错的研究创意后该怎么办？ - 赵山
   https://www.zhihu.com/question/315289489/answer/618549697

2. SQLite的文艺复兴 - Dawei Ma
   https://zhuanlan.zhihu.com/p/601510076
    1. How the SQLite Virtual Machine Works - Ben Johnson
       https://fly.io/blog/sqlite-virtual-machine/

3. Ray分布式计算框架详解 - liadrinz
   https://zhuanlan.zhihu.com/p/460600694
    1. 字节跳动基于 Ray 的大规模离线推理
       https://zhuanlan.zhihu.com/p/636971612
        1. 大模型离线推理（Batch 推理），是指在具有数十亿或数千亿参数的大规模模型上进行分布式推理的过程。相较于常规模型推理，它在模型切分、数据处理和数据流、提升 GPU 利用率方面面临着很大的挑战。
        2. 需求
            1. GPU Memory Wall，进行模型切分具有以下几点优势
            2. 异构资源调度, 弹性资源调度
            3. 性能
                1. 吞吐和 GPU 的利用率能够越高越好
                2. 数据在 Stage 之间能够方便且高效的传输，应当尽量避免数据落盘带来的序列化开销，纯内存的传输方式是比较好的方式
                3. 在推理侧，应当尽量减少数据 IO 等待，避免 IO 导致 GPU 空闲，最大化提高 GPU 使用率
                4. 结合资源弹性，释放掉利用率较低的 GPU，从而提高整理利用率
        5. Ray
            1. 目前 Ray在 GitHub 上已有两万多的 star，字节跳动、Uber、 OpenAI、蚂蚁等公司都有基于 Ray 的相关应用实践和开源合作。ChatGPT is powered by Ray
            2. 为了解决以上问题，我们开发了第二版推理框架。深入到 Ray Datasets Pipeline 的内部实现中添加了 Streaming 执行语义。
            3. 部署，KubeRay
    2. 如何看UCBerkeley RISELab即将问世的Ray，replacement of Spark？ - Milo
       https://www.zhihu.com/question/265485941/answer/294770578
        1. 为什么我们需要新的计算框架？
            "2015年前后，大量AI计算任务崛起，其中增强学习（Reinforcement Learning）和自动驾驶AI训练等等作为一个重大的计算需求，一直很难在MapReduce得到很好的表达。MapReduce本质上是一个大规模的数据聚合（data aggregation）的模型。另一方面，许多AI的任务的核心诉求是在大规模仿真（Simulation）的环境下优化AI的行为。这种诉求和Spark当时的设计初衷完全不同。

            首先，仿真的规模能够轻易轻易到达Billions的级别。这种级别难以在Spark集群得到良好支持。Spark的Task本质上对于基于CPU的操作系统线程抽象。因此Spark并没有非常自然的方式能够将数十亿个仿真实体（AlphaGo的仿真级别）能够合理的同时调度到几千个CPU上面。另外，MapReduce范式难以表达复杂的计算状态和同步。上亿个仿真实体不仅仅运行的时间不同（有些游戏只要几秒就结束，有些游戏可能十几分钟那个还在运行）。让他们在统一的Bulk Synchronization Processing(BSP)模型频繁的同步，不仅仅系统开销很大，而且很难实现。另外，仿真实体往往需要实现复杂的计算行为，伴随计算中间状态的抽象，而这在Spark下难以实现。

            最后，资源调度层的压力。Spark的设计初衷是解决大数据处理问题。那么数据已经静态的存储在文件系统中，Spark只需要依照资源可用性，启动一定的大小的计算图做静态计算即可。可是在大规模仿真中，这上亿个计算实体可能在计算中间大量产生和消失（例如，分布式优化算法的剪枝行为）。这些庞大的对于计算图在线修改的行为在Spark中很难有效支持。"
        2. Ray
            1. "首先在抽象层次，Ray专门给RL的几大类经典仿真问题提供了专用算法框架。RL用户现在难以得到满足的计算需求得到迅速满足。另外牺牲普适性后，Ray可以为几大类的RL算法专门设计同步算法，从而高效推进算法的执行和资源利用率。"
            2. "然后在计算效率上，Ray的底层使用了actor框架来实现。这么做有两大优势。第一，actor可以认为是用户级的线程。其可以轻易在16核的服务器上，同时调度上百万的actor。这使得我们可以轻易实现Billion级别的大规模仿真。第二，actor之间本身是松耦合的，在运行时大量创建和删除actor都可以在server本地完成（毫秒级别的调度延迟），并不会严重影响整个集群的运行效率"
            3. "另一方面，actor相对于Spark系统线程实现存在三大挑战。第一，缺少了系统隔离能力，一个有害的actor实现可以轻易独占当前的cpu资源从而影响他人的使用（依赖于cooperative scheduling）。第二，由于频繁的需要在cpu上切换不同的actor，其调度以及context switch的开销理论上更大。第三，允许python来实现，以及进行大规模仿真的巨大中间计算状态的更新和存储可能成为Ray一个可能的技术债。首先，python在支持function的序列化（函数闭包，有名类，依赖注入）以及远端部署的方面不及Java和C#这类语言成熟。"


4. 黑客 George Hotz 爆料 GPT-4 由 8 个 MoE 模型组成，真的吗？ - SIY.Z
   https://www.zhihu.com/question/607812079/answer/3084718231
    1. 混合专家系统（Mixture of Experts）
       https://github.com/danielgy/TensorFlow_toturial/blob/master/MoE/MoE.md

5. RisingWave: 让我们聊聊实时数据库与流数据库
   https://zhuanlan.zhihu.com/p/617350829
6. 模型优化漫谈：BERT的初始标准差为什么是0.02？ - 苏剑林
   https://zhuanlan.zhihu.com/p/433535832
7. 在机器人工业圈跌摸滚打的第一年——暨2020年终小结
   https://zhuanlan.zhihu.com/p/336575953
8. 浅谈学术论文rebuttal - 魏秀参
   https://zhuanlan.zhihu.com/p/104298923

9. 用 Trading System Lab 自动生成的交易策略，怎么保证它不是遗传算法过度优化的产物？ - 杨博理
   https://www.zhihu.com/question/35753613/answer/64336815
10. 内存数据库 (in-memory database) 的发展现状和前景如何？ - 吴垚
    https://www.zhihu.com/question/19883454/answer/2537385842
11. 陈天奇等人新作引爆AI界：手机原生跑大模型，算力不是问题了
    https://zhuanlan.zhihu.com/p/626274040

12. 为什么各大 VC 最近都在投向量数据库？ - 张文亮
    https://www.zhihu.com/question/603117242/answer/3047534915
    1. 不要投资向量数据库？！ - Yingjun Wu， RisingWave
        https://zhuanlan.zhihu.com/p/634388122

13. 如何评价CVPR 2023的best paper？
    https://www.zhihu.com/question/607381076/answer/3086062716
    1. 如何评价CVPR 2023的best paper？ - huybery
       https://www.zhihu.com/question/607381076/answer/3090802007
14. 揭秘光波导核心原理，了解AR眼镜背后的挑战（上）
    https://zhuanlan.zhihu.com/p/67633782

15. DuckDB 整体介绍 - 谭巍
    https://zhuanlan.zhihu.com/p/626311150
    1. Why DuckDB come out
        1. 下面是 DuckDB 团队发现对于嵌入式 In-Process OLAP 的一些要求
            1. 组合 OLAP 和 ETL 的 workload：能够处理 AP workload 的同时不完全牺牲 OLTP 的性能，同时有效支持批量 append 和批量 update
            2. 传输效率：需要很方便的在 application 和 DBMS 之间传递数据，因为不是所有任务都能在嵌入式数据库中完成，例如机器学习、画图等，所以需要很方便的在 DBMS 和 application 之间传递数据。而由于 In-Process OLAP 的好处是在同一地址空间内，可以非常方便的来传递数据。
            3. 弹性（Resilience）：边缘计算的 OLAP 所在的硬件和服务器级别的硬件差别非常大而且各异，更容易出现硬件问题，嵌入式DBMS要能够检测这些问题并防止数据损坏
            4. Cooperation：系统需要优雅地适应资源争用（CPU or RAM），由于嵌入式数据库不再是机器的唯一使用者，因此它不能像以前那样持续使用所有硬件，否则会导致底层应用程序资源匮乏
    2. DuckDB：高性能并行分组聚合
       https://zhuanlan.zhihu.com/p/636078578

16. 月活 12.8 亿的微信如何防止崩溃？| 后台过载保护策略 - 腾讯技术工程
    https://zhuanlan.zhihu.com/p/520699351

17. B-tree 压缩技术介绍(Oracle,MySQL,PG...
    https://zhuanlan.zhihu.com/p/623531853
    1. Oracle 支持的压缩算法就比较全面了。包括：
        1. Duplicate Key Removal。这就是 Postgres 中的 Deduplication。
        2. Index Key Compression(Prefix compression)。这是基于 B-tree 的 key 是排序的，相邻的 key 往往高概率有公共前缀的特点。
        3. Length Byte Compression。变长的字符串类型编码方式是长度 + 字符串内容。
        4. ROWID List Compression is an independent transformation that takes the set of ROWIDs for each unique index key and represents them in a compressed form, ensuring that the compressed ROWID representation is logically maintained in the ROWID order to allow for efficient ROWID based lookup。
        5. Row Directory Compression。我们知道 B-tree page 的布局用的都是 slotted-array(indirection vector) 结构。一个个 KV 在 page 内从尾部往前存放，它们的间接指针 「offset」（两个字节）在 page 内从头部往后存放。Oracle 把一个 page 按 256 bytes 切分成很多个 region，把一个 KV 的 offset 表示为 base(region 起始地址) + region 内的 offset。由于同一个 region 内的所有 KV 共享一个 base，只需为这些 KV 存一个共享的 1 byte 的 base，再为它们每个 KV 单独存 1 byte 的 offset 就可以了。
        6. Flag and Lock Byte Compression。Generally speaking, the index rows are not locked and the flags are similar for all the rows in the index block. These lock and flag bytes on disk can be represented more efficiently provided it is possible to access and modify them. Any modification to the flag or lock bytes requires these to be uncompressed.
    2. SQL Server 支持三种压缩算法
        1. Row compression。包括 a. 对 key 中 column 的 length 和 offset 进行压缩。(没看到具体说怎么干的) b. 对数值类型（e.g., int, numeric）进行 varint 编码（不了解 varint 的同学可以自行 google 一下，限于篇幅这里不详细介绍）。
        2. Prefix Compression。类似于 Oracle 的 Intra-column prefix compression。
        3. Dictionary Encoding。 Dictionary compression searches for repeated values anywhere on the page, and stores them in the CI area. Unlike prefix compression, dictionary compression is not restricted to one column. Dictionary compression can replace repeated values that occur anywhere on a page.
    3. DB2 支持的压缩算法有：
        1. RID List Compression。相当于 Postgres 的 Deduplication。
        2. Prefix Compression。原理和 Oracle 以及 SQL Server 是一样的，只是 page 内布局稍有不同，单独出来了一个「slots using common prefix」结构，存储着一个个区间，每个区间对应一个公共 prefix。

18. Neon Database介绍
    https://zhuanlan.zhihu.com/p/624075600
    1. Neon Database是由PostgreSQL黑客Heikki Linnakangas和Stas Kelvich共同创立，22年拿了3000w美金的A轮融资，提供基于PostgreSQL的Serverless云服务，此外与Google的alloydb差异化在于，它还实现了类似git的branch、timetravel的能力，Developer/DBA可以把数据库像代码一样来管理，想象一下Developer A和B在同一个业务模块基础上，即基础数据库实例上，分别创建不同的branch数据库，之后独立并行开发。
    2. Read path: Page servers - Replay WAL to reconstruct pages, on demand. Can reconstruct any page ay any point in time.

19. 2023年中国创业独角兽分析报告 - 吴建明wujianming
    https://zhuanlan.zhihu.com/p/635762397
    1. 深度：中美数据库行业，差距究竟在哪里？ - Yingjun Wu
       https://zhuanlan.zhihu.com/p/638474484

20. 将 paxos 和 raft 统一为一个协议: abstract-paxos - drdr xp
    https://zhuanlan.zhihu.com/p/488629044
    1. 因此, 我们就得到了在一个多副本的存储系统中 commit 完成的条件:
        1. commit-写quorum: 以保证任何 reader 都可读到.
        2. commit-唯一: 以保证多个 reader 返回相同的结果.
        3. commit后不能修改: 以保证多次读返回同样的结果.
    2. 两个 State 的顺序关系: 通过 commit_index和 log 长度确定
        1. 两个 State 的顺序关系: 通过 commit_index和 log 长度确定
        2. 而 raft 中, 与 commit_index 对应的概念是 [term, Option<NodeId>], 它是一个偏序关系的值, 也是它造成了 raft 中选举容易出现冲突.
    3. Phase-1.1 阻止更小的 State 被 commit
        1. 因为不同的 writer 不会产生同样的 commit_index . 所以整个系统只需阻止更小的 commit_index 的 State 被 commit
        2. Phase-1.2 读已完成 commit 的 State
    4. Phase-2
        1. 最后, 保证了 s₁ 当前最大, 和 commit后不能修改 这两个条件后, 第2阶段, writer 就可以安全的写入一个 s₁ 完成 commit.

21. Ceph peering流程14问
    https://aspirer.wang/?p=1387
    1. VisionStack-3.2.0版本研发历程
       https://aspirer.wang/?p=1062
    2. 私有云计费服务重构设计思路
       https://aspirer.wang/?p=752
    3. 对私有云一些问题的思考
       https://aspirer.wang/?p=591
    4. Nova-scheduler浅析
       https://aspirer.wang/?p=147

22. 虚拟化技术的过去现在和未来 - 2015
    https://aspirer.wang/?p=492
23. 左耳朵耗子：Amazon转单体架构，是微服务不香还是云不香？ - 陈皓
    https://mp.weixin.qq.com/s/IXCY37p1FHN5ycvXM2IqKA

24. 首个跨云元数据KV存储Xline正式进入CNCF沙箱
    https://mp.weixin.qq.com/s/wW5qGIV3QkDmHjeFC-Z7Gg
    1. interesting

25. 什么情况下需要考虑内存屏障？ - 南帝McKenney（RCU作者）
    https://www.zhihu.com/question/583090138/answer/2887780955
    https://preshing.com/20120515/memory-reordering-caught-in-the-act/
26. 谷歌首席工程师：未来Kubernetes应该消失 - Google Cloud 首席开发者倡导者 Kelsey Hightower
    https://mp.weixin.qq.com/s/SSnHDu2cF6DdHRt5Mo55cg
    https://github.blog/2023-05-24-kelsey-hightower-on-leadership-in-open-source-and-the-future-of-kubernetes/
27. 亚马逊AWS有什么用呢？ - 李庆超
    https://www.zhihu.com/question/22314873/answer/2333079486
28. 百度对象存储架构学习笔记
    https://zhuanlan.zhihu.com/p/636960529
29. 20世纪的乱序超标量处理器-MIPS R10000
    https://zhuanlan.zhihu.com/p/632137830
30. 记录工作中的一个crisis以及我是怎么解决的
    https://zhuanlan.zhihu.com/p/632374163

31. Jemalloc内存分配与优化实践
    https://zhuanlan.zhihu.com/p/632536851
    https://mp.weixin.qq.com/s/U3uylVKZ-FsMjdeX3lymog
    1. Jemalloc核心算法与数据结构
        1. 隔离了大 Size 和小 Size 的内存分配(区分默认阈值为 3.5 个 Pagesize)，可以有效地减少内存碎片
        2. 在内存重用时默认使用低地址，并将内存控制在尽量少的内存页上
        3. 制定 size class 和 slab class，以便减少内存碎片
        4. 严格限制 Jemalloc 自身的元数据大小
        5. 用一定数量的 arena 来管理内存的单元，每个 arena 管理相当数量的线程，arena 之间独立，尽量减少多线程时锁竞争
            1. Jemalloc 引入 extent 的概念，extent 是 arena 管理的内存对象，在 large size 的 allocation 中充当 buddy 算法中的 chunk，small size allocation 中，充当 slab

32. 数据闭环的核心 - Auto-labeling 方案分享 V2.0
    https://zhuanlan.zhihu.com/p/636622001
    1. 参考Chatgpt的训练方式， 大规模无监督的预训练 + 高质量数据集做具体任务的微调， 可能也会成为量产感知算法下一阶段需要发力的方向。

33. 宕机 12 小时，损失超亿元，唯品会技术总监被免职（重点：技术干货深入分析）
    https://zhuanlan.zhihu.com/p/635193879
34. 影响 2023 年的十大科技应用趋势 | 腾讯研究院万字报告
    https://mp.weixin.qq.com/s/QW0V6dN1ykqJIupWaz8Meg
35. 网易对象存储NOS十周年：为什么能不被取代？（文末有福利） - 王盼
    https://mp.weixin.qq.com/s/A_9BAb5xuI-yNxb_RUPMkw
36. 英伟达GH200解读 & 国内外AI芯片发展情况
    https://mp.weixin.qq.com/s/wAoV4wZSs58jeAGhhn0W5w

37. 如何将千亿文件放进一个文件系统，EuroSys'23 CFS 论文背后的故事 - 百度智能云技术站
    https://mp.weixin.qq.com/s/1uQ1yRq0letKDVTaFDtXTA
    1. 发表于 EuroSys 2023 的论文《CFS: Scaling Metadata Service for Distributed File System via Pruned Scope of Critical Sections》。论文披露了百度智能云文件存储 CFS 的元数据系统的核心设计
    2. "这个体系的元数据底座 TafDB 是一个类 Spanner 的系统，几乎和 CFS 同时启动研发。综合这些因素，由 TafDB 提供海量数据存储能力和分布式事务，CFS 自己实现文件语义层这条技术路线在原理上确定了下来。"
    3. "Namepace 2.0 的指导思路是不断缩小写操作的临界区范围并最终实现无锁化。上图给了一个简单的示意图，在 Namespace 1.0 中通过锁保护的关联变更，在 Namespace 2.0 仅通过原子操作就满足，并发的操作不再需要串行执行。"
    4. "通过调整数据布局，将整个关联变更涉及的数据耦合到一个分片上，可以起到让事务冲突聚焦到单个分片的效果。这个调整其实意味着 “属性分开存储” 这一规则扩展到了包括文件在内的所有类型的目录项。"
        1. Split metadata into id and attr
           对于 inode id record，<kID, kStr> 中的 kID 部分代表父目录的 inode .. inode_table 整体上按 <kID, kStr> 有序存储所有数据，分片规则是按照 kID 来的。TafDB 做了一个特殊的保证，即分片无论如何分裂和合并，同一个 kID 的数据始终存储在同一个分片上。
    5. "最后，我们将原来事务保护的整个操作，拆解成两个 TafDB 单分片操作的组合（目录的情况），或一个 FileStore 操作 + 一个 TafDB 单分片操作的组合（文件的情况），配合通过精心排列的顺序，使得这两个操作只需要满足分别满足原子性即可保证执行效果，不再需要一把大锁来保护整个范围。"
        1. 除了非常复杂的 rename 操作 .. Rename 服务（Renamer）：Multi-Raft 架构，每个文件系统由一个 Raft 复制组提供对复杂 rename，即所谓 Normal Path rename 的支持；
        2. 单分片原语
    6. related referenced works: HopsFS, ADLS, InifiniFS 

38. 国际顶会 ICDE入选 | OceanBase 死锁检测实现了哪些技术突破？
    https://zhuanlan.zhihu.com/p/624847601
    1. OceanBase: LCL: A Lock Chain Length-based Distributed Algorithm for Deadlock Detection and Resolution
    2. "LCL算法的死锁检测既不需要WFG全局视图，也不需要本地视图，只需要事务向持有它正在等待的资源的事务进程发送几十字节的信息，从而引入很小的内存开销和通信开销。最重要的是，LCL 可以检测并解决系统中所有真正的死锁，而不会引入冗余的中止操作。"
    3. 已知死锁检测算法
        1. 中心化死锁检测，E.g. TiDB
        2. 死锁预防策略, Wound-Wait或Wait-Die等策略, e.g. Google Spanner
        3. 路径推动算法, 节点之间传输并收集局部WFG关系，死锁的产生能够被部分节点检测到, e.g. CockroachDB - Path-Pushing Algorithms
        4. 边追逐算法, 依据事务依赖关系向下游节点发送消息，死锁产生的环将通过这些消息被推断出来, e.g. Oracle RAC, OceanBase
    4. "Mitchell 和 Merritt (M&M) 的算法[6]是一种简单且完全分布式的边追踪算法，它提供了检测和解决死锁的方法。OceanBase LCL 算法的灵感来自于M&M算法。M&M 和 LCL 主要差异在于: M&M 假设事务等待单一资源，LCL 对事务可以等待的资源数量没有任何限制。"
    n. related materials
        1. CockroachDB死锁处理
           https://zhuanlan.zhihu.com/p/449151313

39. 大模型微调总结
    https://zhuanlan.zhihu.com/p/627642632
    1. Parameter-Efficient Fine-Tuning (PEFT) 技术
    2. 今天介绍下另外几种常用的方法，包括 Adapter Tuning、Prompt Tuning、Prefix Tuning、P-Tuning、P-Tuning v2 和 AdaLoRA

40. 红黑树下岗，内核新数据结构上场：maple tree！
    https://zhuanlan.zhihu.com/p/628868025
    1. "比如，其中一个问题就是用来保护内存管理里的重要结构的锁的竞争问题 ... Liam Howlett 和 Matthew Wilcox 一直在开发一种新的数据结构，称为 "maple tree"，希望能取代目前用于 VMA 管理的数据结构。"
    2. "maple tree（取这个名字可能是借用了枫叶的形状，意指能走向多个方向）与 rbtrees 有根本性的差异。它们属于 B-tree 类型 ... maple tree 对搜索过程也有改进，同样是来自于 B-tree 结构特点 ... maple tree 的设计中也是按照 lockless 方式的要求来的，使用 read-copy-update (RCU) 方式"

41. 聊一聊分布式系统中的租约 - 罗一鑫
    https://zhuanlan.zhihu.com/p/268370901

42. Common arguments regarding emergent abilities
    https://www.jasonwei.net/blog/common-arguments-regarding-emergent-abilities
    1. "I showed that emergent abilities are widely prevalent, and that they are notable for several reasons:
        1. Emergence is not easily predicted by extrapolating scaling curves from smaller models.
        2. Emergent abilities are not explicitly specified by the trainer of the language model (next word prediction "only").
        3. Since we haven't tested all possible tasks that exist, we don't know the full range of abilities that have emerged.
        4. Further scaling can be expected to elicit more emergent abilities."

43. 从 Bluesky 到内容协议 - 李奇
    https://thequibbler.zhubai.love/posts/2133851511351164928
44. 《证券公司网络和信息安全三年提升计划》分析之一：“加强系统上下线管理”
    https://mp.weixin.qq.com/s/MOpql-_33v5c_UBNNSjqMw        

45. 惊人的算力成本背后，自动驾驶公司如何加速研发创新 - 趋动科技
    https://mp.weixin.qq.com/s/cFDxAsjO9S4TsBCETJlq6Q
    1. 当前业界在GPU虚拟化和池化方面的实践主要集中在三个层次：（1）硬件层；（2）内核层；（3）运行时层。
        1. 在硬件层实现GPU虚拟化的主要代表是英伟达的MIG，它的优点是性能损失小，缺点是只支持固定比例的GPU切分，只支持部分英伟达高端GPU。
        2. 在内核层实现GPU虚拟化的主要代表是英伟达的vGPU，腾讯的qGPU，以及阿里的cGPU。
            1. 英伟达的vGPU的优点是支持全部企业级GPU，支持虚拟机（如KVM，VMware）和容器环境，缺点是只支持固定比例的GPU切分。因为英伟达并未开放其GPU驱动（内核态和用户态）的所有接口，
            2. 腾讯的qGPU和阿里的cGPU只能支持容器环境，不能支持虚拟机环境。此外，英伟达的MIG和vGPU，腾讯的qGPU和阿里的cGPU都不支持基于远程GPU的GPU池化，不支持动态分配和自动释放GPU资源，不支持GPU资源的超分超售。
            3. 本质上，英伟达的MIG和vGPU，腾讯的qGPU和阿里的cGPU都是站在单张GPU卡的角度来实现GPU切分，而不是站在整个数据中心的角度来实现对所有GPU资源的池化管理，因此并非完整的GPU池化方案。
    2. 在运行时层实现GPU虚拟化和池化的主要代表是趋动科技的OrionX GPU池化软件。
        1. OrionX的优点是
            （1）兼容性好，支持市面上所有型号的英伟达GPU；
            （2）功能完备，支持虚拟机和容器环境；
            （3）性能优异，即便是远程GPU也只引入了非常小的性能损失；
            （4）使用灵活，支持基于远程GPU的GPU池化，支持动态分配和自动释放GPU资源，支持GPU资源超分超售；
            （5）管理简单，具有完整的控制面，支持通过GUI，命令行以及RESTFUL API来管理整个数据中心中的所有物理和虚拟GPU资源，提供GUI界面来可视化所有物理和虚拟GPU的监控和告警信息等；
            （6）企业级功能完备，支持故障卡自动隔离，GPU任务热迁移，软件自动灰度升级等。
        2. OrionX的主要缺点是，由于需要支持已公开的英伟达用户态驱动和库接口，同时还要实现整个数据中心GPU池化所需的管理平面，自身的研发工作量非常巨大，同时远程GPU的性能优化难度很高。
            1. 作为自动驾驶领域的深耕者，文远知行通过对当前主要技术路线和产品的仔细分析，认为运行时虚拟化是GPU池化技术的基础，并选择了趋动科技OrionX GPU池化软件来建设弹性GPU资源池，更从容地开展自动驾驶技术的研发工作，加快在该领域内开拓创新的步伐。
```
