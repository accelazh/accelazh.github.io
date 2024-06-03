---
layout: post
title: "Recent Articles Reading Chip Design Investment Valuation zStorage"
tagline : "Recent Articles Reading Chip Design Investment Valuation zStorage"
description: "Recent Articles Reading Chip Design Investment Valuation zStorage"
category: "storage"
tags: [storage, paper, cloud]
---
{% include JB/setup %}

Search "very good", "good", "very interesting", "interesting", "very useful", "useful" for recommendation.

```
1. 模型与算法在石油产业链的优化应用实践 - DataFunTalk
   https://zhuanlan.zhihu.com/p/680432343
2. 阿里云网络演进 - 木木女神经
   https://zhuanlan.zhihu.com/p/680367683
3. 智算中心网络架构白皮书 - 木木女神经
   https://zhuanlan.zhihu.com/p/680509531
4. LLM推理优化系统工程概述 - 进击的Killua
   https://zhuanlan.zhihu.com/p/680635901
7. 论文分享：利用对象存储进行高性能数据分析 - GreptimeDB
   https://zhuanlan.zhihu.com/p/681148414
8. 用「压缩即智能」评测各路开源大模型 - 九号
   https://zhuanlan.zhihu.com/p/681449063
9. 与MySQL相比，阿里云的PolarDB有哪些优势？它是否会对MySQL市场产生冲击？ - 沐风的回答
   https://www.zhihu.com/question/66598931/answer/3388971820
11. 火山引擎ByteHouse：“专用向量数据库”与“数据库+向量扩展”，怎么选？ - 科技哔哔的文章
    https://zhuanlan.zhihu.com/p/681469193
21. 「还是谷歌好」，离职创业一年，我才发现训练大模型有这么多坑 - Yi Tay 机器之心
    https://mp.weixin.qq.com/s/6UanZ_wxCe2OrRtu6L9ZKQ
23. 电信业务对数据库国产化的关键诉求 - bluesky
    https://zhuanlan.zhihu.com/p/685870579
31. 论文漫谈：CXL and the Return of Scale-up Database Engines - Dase314-ECNU的文章
    https://zhuanlan.zhihu.com/p/686586341
34. 六谈操作系统：构建商业模式 - 魏永明
    https://zhuanlan.zhihu.com/p/150541211
36. 微软37页论文逆向工程Sora，得到了哪些结论？ - 机器之心
    https://zhuanlan.zhihu.com/p/684754970
    1. Transformer除了语言模型，还可胜任图和视频生成
37. 螺蛳壳里做道场：实现一个256KB的迷你文件系统 - 木鸟杂记
    https://zhuanlan.zhihu.com/p/684289644
38. 探讨如何设计高性能IO软件栈 - SallyLeoqqdd
    https://zhuanlan.zhihu.com/p/684247143
39. 全网最细！列存高效更新技术介绍 - 黄金架构师
    https://zhuanlan.zhihu.com/p/665260177
41. DPDK内存管理引入 - 胡思乱想
    https://zhuanlan.zhihu.com/p/683819374
43. 生成引擎优化 - WF Research
    https://zhuanlan.zhihu.com/p/683956343
44. 中科院等万字详解：最前沿图像扩散模型综述 - 量子位
    https://zhuanlan.zhihu.com/p/685779235
46. 懂车帝数据指标体系建设和应用实践 - DataFunTalk
    https://zhuanlan.zhihu.com/p/686644975
48. 万字：对账系统从入门到精通 - 陈天宇宙 技术琐话
    https://mp.weixin.qq.com/s/f8DOQadT7rHMf3l1WZFycQ


5. 分布式存储全共享架构(Shared-Everything)分析与研究
   https://mp.weixin.qq.com/s/NVR-pj9Int0nVYG8TVUlTg
    1. XSKY.
    2. Interesting.

6. Problem: 寻找两个正序数列（长度M、N）合并的中位数，要求时间复杂度log(M+N)
   https://leetcode.cn/problems/median-of-two-sorted-arrays/
    1. Less optimal Solutions 1:
        1. Find S1's mid point S1m, locate S1m at S2 as S2_S1m. Get distance of S2_S1m vs S2m as D.
           The problem recursively becomes getting the merged mid point of S1[0, S1m] merging S2[S2m, S2_S1m]=D
           So, each round paying log(len(S2)/2), problem scale reduces to len(S1)/2 + D <= len(S1)/2 + len(S2)/2.
           So, total time complexity is sum(log(2^k)), 2^k from 1 .. len(S2)/2. => O(log(len(S2))^2)
    2. 合并二分查找
       https://leetcode-solution-leetcode-pp.gitbook.io/leetcode-solution/hard/4.median-of-two-sorted-arrays
        1. Translate the problem into a Partition Problem that is 1-dimensional:
            1) S1 is partitioned at index i, S2 is partitioned at index j. i+1 + j+1 = len(S1)+len(S2)/2. Freedom degree is 1.
            2) Every element in the left partition is smaller than every element in the right partition.
               I.e., S1[i] <= S2[j+1], S2[j] <= S1[j+1]
        2. Search for the right partition point index i inside S1, assuming len(S1)<len(S2).
           Use binary search. The time complexity is min(log(len(S1)), log(len(S2)))

10. SPDK之BlobStore设计特点体会 - 小川的文章
    https://zhuanlan.zhihu.com/p/675907424
    1. 云和恩墨 zStorage分布式存储系统
    2. "所以为了减少元数据的操作，我们在实际使用的时候，针对BS做了优化以减轻元数据操作慢的这个问题的"
       "尽量减少写盘，BS的位图信息，上述两个512KB的位图，并不会在每次修改以后就立即刷盘。 ... 如果异常掉电，这部分不下盘的元数据可以通过扫描分析其他持久化到盘上的元数据推导出来。"
    3. "最后由于BS没有采用日志来保障多步元数据操作的原子性，所以它采取了一些比较特别的方式。例如：持久化元数据链的时候，首页原地写，其他页面分配新的位置写入，然后删除旧的页面，最后将首页指向新的位置。采用了类似这样一些方法来保证元数据写入的原子性。"

    n. related materials
        1. 分布式存储系统-盘点zStorage分布式存储系统采用的那些基础技术 - 小川的文章
           https://zhuanlan.zhihu.com/p/681166641
            1. 分布式一致性协议，选择了Raft。
            2. 采用C语言、无锁化的SPDK存储性能开发框架。
            3. 采用SPDK BlobStore作为本地存储底层。
            4. 采用RDMA作为网络通信基础技术。
        2. 分布式存储系统性能调优-加法和减法思想 - 小川的文章
           https://zhuanlan.zhihu.com/p/681166166
            1. 计算机系统中，按照性能数量级，大概有以下几层：
                1. IO层。涉及到网络IO以及硬盘IO。
                2. 内存层。大量的内存拷贝会非常影响性能。
                3. CPU缓存层。CPU需要的数据是否可以命中CPU缓存。
                4. CPU层。局部代码的优化，是否可以命中寄存器。
                性能优化的顺序按照1，2，3，4层层推进的顺序。

12. 专家解读：新兴存储技术的扩展趋势（PPT） - Andy730
    https://mp.weixin.qq.com/s/LBwFHhnUAMEtP37j-n-BSQ
    1. Good. "No Shortage of Emerging Memory Technology Types"
    2. 在这次网络研讨会中，SNIA CMSI会员和领先专家Tom Coughlin（Coughlin Associates/IEEE主席）以及Jim Handy（Objective Analysis）将深入探讨MRAM、ReRAM、FRAM、PCM等新型存储技术的最新进展，详细解释这些技术的发展时间、方式和原因，以及它们的成功将如何影响半导体和资本设备市场。

13. 学习索引现有研究评述 - Nempt
    https://zhuanlan.zhihu.com/p/649563211
    1. Sun Z, Zhou X, Li G. Learned Index: A Comprehensive Experimental Evaluation[J]. Proceedings of the VLDB Endowment, 2023, 16(8)
    2. 通过评估得到如下结论：
        Existing learned indexes have no advantages for complicated data distributions and write-heavy workloads
        Learned indexes have no significant advantage against traditional indexes for range queries
        Learned indexes have no advantage on string keys
        Learned indexes have no advantage on bulk loading
        Non-linear models take more training overhead
        Learned indexes like XIndex and FINEdex gain both large index size and high insert/lookup latency, as the search involves both the index and buffers
        The micro-architectural metrics can reveal the read/write performances of learned indexes
        Learned indexes cannot outperform traditional indexes for concurrent lookups/writes

14. Groq公司推出的全球最快的大模型推理服务达到每秒输出500个token，如何看待这一技术？ - mackler的回答
    https://www.zhihu.com/question/645010090/answer/3403413472
    1. good insights
    2. related materials
        1. sram vs hbm
            1. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
               https://ahmdtaha.medium.com/flashattention-fast-and-memory-efficient-exact-attention-with-io-awareness-2a0aec52ed3d

        2. 24年对于大模型演进方向的一些思考 | - 霸王手枪腿的文章
           https://zhuanlan.zhihu.com/p/682434451
            1. good insights

        3. Groq公司推出的全球最快的大模型推理服务达到每秒输出500个token，如何看待这一技术？ - 陈巍的回答
           https://www.zhihu.com/question/645010090/answer/3402883628
            1. good insights

15. BlobDB简介 - 贺大伟
    https://zhuanlan.zhihu.com/p/682561835
    1. BlobDB 使用了一种称为键值分离的技术：它不是将大value（blob）存储在 SST 文件中，而是将它们写入一组专用的 blob 文件，并在 SST 中仅存储指向它们的小指针文件。
    2. blobDB的设计带来了两个核心优势：
        1. value的GC不再需要回查SST，也不需要回写SST。
        2. blob file中的value存储是跟SST中的key的字典序保持一致，可以很好的借助预读来提升读取性能，降低随机IO对读取性能的影响。

16. Roadmap to Learn AI in 2024 - Benedict Neo
    https://medium.com/bitgrit-data-science-publication/a-roadmap-to-learn-ai-in-2024-cc30c6aa6e16
    1. good

17. 数据库的下一场革命：S3 延迟已降至原先的 10%，云数据库架构该进化了 - 曹伟（鸣嵩）
    https://zhuanlan.zhihu.com/p/674018787
    1. good

18. HN 论坛里网友吵翻了 ｜ SSD硬件速度飙升，唯独云存储未能跟上 - 小猿姐
    https://mp.weixin.qq.com/s/hsh0y4eyPD2Rq1fjGK8jkg
    1. good insight

19. 传说OpenAI工程师必背的经典：苦涩的教训
    https://mp.weixin.qq.com/s/fX9Lmkg4b0bNx5igLuznpQ
    1. "那些能够发挥计算力的通用方法终将大获成功。"
       "绝大多数AI研究都是在这样一种假设下进行的：智能体可使用的计算资源是不变的（在这种情况下，发挥人类知识将是提升性能的主要手段）。然而，随着时间的推移，超出一般科研项目周期后，庞大的计算资源终将成为现实。虽然研究人员希望在短期内依靠人类的领域知识取得突破，但长远来看，真正重要的是计算能力的发挥。这两种方法不必是对立的，但实践中它们往往相悖。在一个上的投入就意味着牺牲另一个。"

20. 又一 SaaS 巨头：与（云）渐行渐远、转向数据中心，为节省成本 - 云头条
    https://mp.weixin.qq.com/s/GHmEAFHGFg_unjTm5c2EAg
    1. 视频会议公司 Zoom 正在削弱对云服务的依赖。
    n. related materials
        1. Hacker News: Zoom taps Oracle for cloud deal, passing over Amazon, Microsoft    [2020]
           https://news.ycombinator.com/item?id=23010868
            1. AWS charts GB transferred, while renting datacenter charts GBps. Zoom may have a constant transfer needs. If network keeps 100% util at full month, it can be 100x cost saving. 
                1. Good point

22. 一些已成为LLM InferEngine中事实标准的方法 - 进击的Killua
    https://zhuanlan.zhihu.com/p/685706549
    1. Multi-Query Attention
    2. Grouped-Query Attention
    3. Sliding Window Attention
        1. Mistral sliding window attention
        2. Longformer sliding window attention
    4. ALiBi
    5. Flash Attention
       https://zhuanlan.zhihu.com/p/682441154

24. zStorage是如何保持性能稳步上升的? - 张洋 zstorage
    https://mp.weixin.qq.com/s/UMk0UEN0-di48fTsltRU0g
    1. 最近一年以来，zStorage三节点集群的4KB随机读写 性能从120万IOPS稳步提升到了210万IOPS。
    2. Highlights
        1. zStorage数据面代码 全部采用标准C语言编写。
        2. zStorage在MR合入之后，对每个MR做了性能测试。
            1. 性能走势 by time
            2. 多次测试求取平均值
            3. 误判问题
                1. 硬件状态，如IB网卡
                2. 软件环境配置
        3. zStorage内置了点位时延分析工具(ztrace)，能够详细分析出一个IO请求在某个模块中的 耗时情况。

25. 苹果极致LLM端侧方案：LLM in a flash - Civ
    https://zhuanlan.zhihu.com/p/673775476
    1. 一个7B半精度LLM，存储空间超过14GB。手机DRAM一般不超过16GB。因而，使用Flash加载完整LLM，DRAM仅装载必要部分。Not using specialized chips.
    2. Highlights
        1. 如何快速识别出哪些模型参数是必要的
            1. Sparsity
        2. 考虑到由Flash memory到DRAM的带宽较低，如何加快由Flash memory到DRAM的传输效率
        3. Optimized Data Management in DRAM
    m. My questions
        1. Another group of people is even complaining that DRAM is too slow, everything must be put into GPU memory. So the whole thing can even run on flash?
        2. The Flash in LLAM is essentially using DRAM as cache (or pin parts in DRAM). How is the locality?

26. 单机文件系统笔记 - Trafalgar的文章
    https://zhuanlan.zhihu.com/p/601469798
    1. Storage become a system
    2. FFS 1984, LFS 1992, NFS WAFL 1994, XFS 1996, ZFS 2002

27. 龙芯的频率为什么提升不上去，是工艺还是设计问题？ - Matterhorn
    https://zhuanlan.zhihu.com/p/684810781
    1. CPU性能 = CPU频率 * IPC
    2. 更深长的流水线有利于提升CPU频率，但不利IPC提升
    3. 其它提升频率：后端优化如重排算子，工艺优化
    n. related materials
        1. 从电路底层来了解CPU中断机制 - 翛翾
           https://zhuanlan.zhihu.com/p/611038805
            1. 组合电路中各元件输出波幅的微小不对齐（毛刺），造成了频率的上限
        2. （译）现代微处理器：90分钟速成指南！ - 马克刘
            https://zhuanlan.zhihu.com/p/645343994
            1. very good. explained key technologies to recent years, and most importantly the rationales and trade-offs
            2. On the path of parallelism
                1. 频率、流水线、IPL
                2. 超流水线，多发射与超标量
                3. 乱序执行（OOO），分支预测，寄存器重命名
                    1. 近代处理器实现多种分支预测器，并根据实际表现动态选择， 以适配不同的代码场景
                    2. 头脑家与速度魔的争论
                        1. 功耗与指令并行性的双重壁垒
                4. 微指令μops，读作"micro-ops"
                5. SMT、超线程
                6. 多核、multi-core、manycore，大小核
                7. SIMD向量指令
            3. 功耗与集成
                1. 大小核
                2. SoC设计
                3. 内存控制器直接集成到处理器芯片，以减少访存延迟的周期数
            4. 内存与内存壁垒
                1. SDRAM（CAS延迟为11），访问延迟通常为内存总线的24个周期 * 数据块数，再加CPU的20个周期
                    1. "一个2.8 GHz的处理器将需要104个周期，一个3.2 GHz的处理器需要116个周期，一个3.6 GHz的处理器需要128个周期，一个4.0 GHz的处理器将等待惊人的140个周期来访问内存！"
                2. 缓存
                    1. "且大多数软件在这种缓存中的命中率约为90%"
                    2. 缓存冲突，多路关联缓存
                    3. SDRAM使用与内存总线相同的时钟，SDRAM芯片操作的内部时序方面和交错结构都暴露给了系统，因而可以被利用，这减少了有效的延迟
                        1. SDRAM内存系统中，多个内存请求可以在任何时候都是未解决的，而且都以高度有效的、完全流水线的方式进行处理。一个SDRAM内存系统通常提供了与同一时代的异步内存系统相比双倍或三倍的持续内存带宽，即使SDRAM系统的延迟只是稍微低一些，而且使用的是相同的基础存储单元技术（并且仍然是如此）。

28. 阿里云高性能EBS的架构演进 - KDF5000的文章
    https://zhuanlan.zhihu.com/p/686239323
    1. After the Pangu 2.0 paper. This table for the EBS layer
    2. Before 2019
        1. Inline EC
        2. Append-only
        3. Segment management (Partition movement)
        4. LZ4 compression inline
    3. 2019 to now
        1. Fusion staging writes and inline compress, SegmentCache, FPGA compression
            1. 基于FPAG的压缩可以实现7.3GiB/s的吞吐
        2. Networking: UDB protocol, DPU-offloading
        3. 数据冗余度从1.29降到了0.77；流量放大从4.69降低到了1.59
        4. VD is partitioned, CentralManager for partition management on cluster
        5. PMem staging

29. 拆解一下字节的烧钱工作，MegaScale！ - 蛋糕店的蜡烛
    https://zhuanlan.zhihu.com/p/684712727
    1. MFU利用率，并行、优化，容灾、日志、快速重训练

30. HALO: 动态堆内存布局优化技术 - 左沙
    https://zhuanlan.zhihu.com/p/687463484
    1. HALO: Post-Link Heap-Layout Optimisation
    2. Interesting. Using runtime profiling to optimize heap layout. Allocations accessed together are grouped. So to reduce cache miss.

32. 交叉熵、相对熵（KL散度）、JS散度和Wasserstein距离（推土机距离） - 麦茬茬的文章 - 知乎
    https://zhuanlan.zhihu.com/p/74075915
    1. Very useful. 
    2. 相对熵（KL散度） = 熵（信息量） - 交叉熵
    3. 解决KL散度的非对称性：JS散度
    4. 解决KL散度，JS散度在两个分布距离较远时变发散：Wasserstein距离
        1. 推土机距离：直观上可以把E(x,y)∼γ[||x−y||]理解为在γ这个路径规划下把土堆P1挪到土堆P2所需要的消耗

33. 为什么说腾讯22年前的这份神级PPT是立项汇报的天花板？ - 卫夕
    https://zhuanlan.zhihu.com/p/684222828
    1. Very good for vision and department BU level planning

35. GPU基础知识 - 陆淳
    https://zhuanlan.zhihu.com/p/683016265
    1. useful

40. Redis: 美团大规模KV存储挑战与架构实践 - 美团技术团队
    https://zhuanlan.zhihu.com/p/687147571
    0. Code name: Squirrel, Cellar
    1. 跨地域容灾 - 双向同步冲突自动解决
        1. 基于数据写入本地时间的 last write win 冲突自动解决功能
        2. 保存最近一段时间删除掉的 Key 及删除时间戳
        3. Cellar不同，它使用HLC
        m. My questions
            1. Looks a bit related to Facebook's memcache paper
               https://research.facebook.com/publications/scaling-memcache-at-facebook/
               Or the Facebook RAMP-TAO paper's RefllLibrary
               https://www.vldb.org/pvldb/vol14/p3014-cheng.pdf
    2. Run-to-Completion (RTC) 线程模型
        1. 内存引擎无锁化
        n. Related materials
            1. The word Run-to-Completion should came from Seastar and DPDK.
            2. DPDK supports Run-to-Completion mode vs Pipeline mode
               https://zhuanlan.zhihu.com/p/537984740
            3. RTC：run-to-completion 指从开始处理报文起到报文发出去在一个核上终结。
               https://zhuanlan.zhihu.com/p/98346451
            4. RTC(Run to Completion)运行模式 - 设计线程独占CPU核运行，减少CPU cache missing，减少CPU之间的缓存同步，保证IO在线程上RTC，同时，设计上需要考虑避免线程跨numa访问系统资源，内存、磁盘、网卡等。
               https://zhuanlan.zhihu.com/p/684247143
    3. 发展规划和业界趋势
        1. Squirrel && Cellar 去 ZK 依赖
        2. KV 存储支持向量引擎
        3. 云原生部署，自动化
        4. Kernel Bypass 技术，DPDK，SPDK，io_uring
        5. 硬件：配备了压缩卡的 SSD，RDMA 网络
    n. related materials
        1. TGW: 下一代 Tencent Gateway - 腾讯技术工程
           https://zhuanlan.zhihu.com/p/98346451
            1. RX core + TX core => Run-to-Completion 
               It almost doubled the throughput
                1. Good
            2. 显式预取 Hash 查表时的第一个 bucket 内存到 CPU 缓存
               关闭超线程时优化至 50Mpps
            3. 总结
                1. 转发架构优化：PipeLine 优化为 RTC；
                2. 关闭超线程：增强单核转发能力；
                3. 批量发送：显著提升零丢包性能；
                4. 解除伪共享；充分发挥 CPU 并发能力；
                5. 批量处理：降低每包平均花费的 CPU 指令数；
                6. 内存预取：降低 Cachemiss 及跨 NUMA 带来的影响；
                7. 去除无关逻辑；

        2. io_uring
            1. 一篇文章带你读懂 io_uring 的接口与实现 - 迟策的文章 - 知乎
               https://zhuanlan.zhihu.com/p/380726590
                1. API list: Submission Queue 
            2. 如何通俗易懂的讲解 io_uring? - 柠檬酸菜鱼的回答 - 知乎
               https://www.zhihu.com/question/637486626/answer/3359561338
                1. 在传统的 I/O 模型中，我们通常使用系统调用（例如 read、write）来进行 I/O 操作。而在 io_uring 中，我们可以将多个 I/O 操作组织成一个队列（ring），然后通过一个系统调用（io_uring_enter）将这个队列提交给内核进行批量处理。这样一来，我们可以减少系统调用的次数，从而提高性能。
                2. io_uring 还支持多种类型的 I/O 操作，包括文件读写、网络套接字操作、定时器等。它可以在一个请求中同时处理多个不同类型的操作，从而进一步提高效率。
                3. 另一个重要的特性是 io_uring 提供了零拷贝（zero-copy）的能力。在传统的 I/O 模型中，数据通常需要在用户态和内核态之间进行多次拷贝，而 io_uring 可以直接在内核态中操作数据，避免了不必要的数据拷贝，提高了效率。

42. Removing Double-Logging with Passive Data Persistence in LSM-tree based Relational Databases——论文泛读 - 妙BOOK言
    https://zhuanlan.zhihu.com/p/684332583
    1. 在基于LSM树的RDB中，上层RDB层和下层存储引擎层都实现了冗余日志记录设施，RDB中使用binlog记录所有处理的SQL语句， LSM使用预写日志（WAL）记录所有KV更新操作，而且这些操作都是同步执行且在关键路径上。

45. 【综述论文】UC Berkeley：Transformer推理全栈优化研究进展综述 - eyesighting的文章 - 知乎
    https://zhuanlan.zhihu.com/p/663879289
    1. very good paper

47. 大模型推理百倍加速之KV cache篇 - zhang
    https://zhuanlan.zhihu.com/p/685853516
    1. 对不断增长的 LLM 的窗口长度的需要与有限的 GPU 显存之间的矛盾。因此优化 KV cache 非常必要。
    2. KV cache主要分成5个方向的优化，即Sparse、Quantization、Allocator、Window、share
    3. Good summary table at the end of the article.

48. Understanding LLM RAG - Retrieval Augmented Generation
    1. AWS: Back to Basics: Understanding Retrieval Augmented Generation (RAG)
       https://www.youtube.com/watch?v=_sq3ixXMQTc

    2. LangChain: RAG From Scratch: Part 1 (Overview)
       https://www.youtube.com/watch?v=wd7TZ4w1mSw&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x
        1. Indexing
        2. Retrieval
        3. Generation
        4. Query
    
    3. Pankaj Pandey: Introduction to Retrieval-Augmented Generation (RAG)
       https://medium.com/@pankaj_pandey/introduction-to-retrieval-augmented-generation-rag-9209bf8a076d
        1. "RAG systems aim to address the drawbacks of Large Language Models by incorporating factual information during response generation, mitigating issues such as knowledge cutoff and response hallucination."
        2. Phase 2: Content Generation
            1. The retrieved information is appended to the user's prompt and fed to the LLM.
            2. The LLM generates a personalized answer based on the augmented prompt and its internal knowledge base.
        3. Open-Book Approach
            1. Model's response involves browsing through external content.

    4. Tejpal Kumawat: Retrieval-Augmented Generation (RAG) from basics to advanced
       https://medium.com/@tejpal.abhyuday/retrieval-augmented-generation-rag-from-basics-to-advanced-a2b068fd576c
        1. The Retrieval Augmented Generation (RAG) Pipeline
            1. Vector database, Graph database, Regular SQL database
            2. Retrieved information is represented as embedding vector. Index works on embedding vectors. Retrieve goes to Index.
               Information retrieval is achieved by providing the nearest neighbors to the questions as context to the LLM.

    5. SuperAnnotate: Retrieval augmented generation (RAG) explained [examples included]
       https://www.superannotate.com/blog/rag-explained
        1. RAG vs fine-tuning
        2. Retrieval augmented generation vs semantic search
        3. "When the user sends a query(question) to the retriever, we use vector embeddings(numerical representations) to retrieve the requested document. Once the needed information is found from the vector databases"

49. Leetcode Algorithm Problem: 给定一个字符串 (s) 和一个字符模式 (p)。实现支持 '.' 和 '*' 的正则表达式匹配。匹配应该覆盖整个字符串 (s)。
    1. Answers
        1. https://biaodigit.github.io/LeetCode/0010/#%E9%A2%98%E7%9B%AE%EF%BC%9A%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E5%8C%B9%E9%85%8D
        2. https://www.cnblogs.com/mfrank/p/10472663.html
    2. My solution
        1. Break the search pattern string into match tokens. Each match token can generate a list of individual token matches. An individual token match is represented as (start index, end index). We extra individual token match first, so that they can be repeatedly used in the later search process.
        2. Use recursive search to find full string match. Start from the first token, goes to the last token, iterate each individual token match. If two individual token match can connect to each other, the search can move to the next token.
        3. Optimizations
            1. concrete chars or "." on the start and end of pattern string can directly match with the input string. Stripe them off, then the problem recursively becomes a smaller problem, until both start and end of the pattern string are tokens with "*".
            2. In the list of individual token matches, merge them into several matching regions, each itself is consecutive. In another word, if (a1, b1), (a1, b2) are in list, then any substring between a1, max(b1,b2) are matches.
            3. A token of ".*" can be jumped through in the search process, because it's individual token matches are (0, infinity).
            4. The list of individual token matches can be represented as an bool array. The array is the same length of the full input string.
        4. Converting recursive search into DP
            1. SYSTEMATICALLY, almost every tree-style recursive search, can be converted into DP. The difference is a tree-style search scans through choices in each step. DP uses a 2D matrix to track states in this case. The 2D matrix tracks RESULTS rather than choices. DP searches through RESULT SPACE rather than choice space. The next result can be derived from the previous GROUP of results.
            2. Define the iteration direction and state representation.
                1. One-dimensional, only iterate through the pattern string. Suppose we know if the current pattern matches. If add a new token to the pattern string, can we know if it matches or not? No, we cannot. The matching is not greedy. We need to go back more steps. And, if we go back with the pattern string, we need to shorten the input string too.
                2. So this lead us to 2D iteration, by iterating both the pattern string and the input string. We need a 2D matrix to track the states. The state in the matrix tells whether the corresponding pattern substring (0, j) matches with the corresponding input substring (0, i).
            3. Drive the next state
                1. If the current token is "A*", it needs to go back to see m[i-1, j-1]
                    1. if m[i-1, j-1] is 1, and input[i] is A, then m[i,j] is matching
                    2. if m[i-1, j-1] is 0, go further back to the first m[i-k, j-1], where m[i-k, j-1] is 1. The question then comes to m[i-k+1, j] to m[i,j], their matching pattern must be 0,0,.., or 1,1,0,.., or 1,1,1,.. . In another word, match <=> input[i]==A && m[i-1,j]==1.
                    3. In another word, a next "A*" can match implies either
                        1) The last pattern substring matches the last input substring.
                           And, the next "A*" right matches the next char in the input substring.
                        2) Or, the last pattern substring doesn't match the last input substring.
                           But, the last pattern substring can match a more previous part of the input substring, and the remaining part of the input string matches "A*".
                    4. Example
                        1. aabbbbbbb (vertical), a*b* (horizontal)
                           1 1
                           1 1
                           0 1
                           0 1 
                2. The derive process would start from the left up corner, and then derive line by line to the right bottom.
            4. In recursive search, we exploit that a token's individual match can be repeated looked up. In DP how is the equivalent being leveraged?
                1. In DP, it doesn't repeatedly look up a token's individual match. Instead, the results are forwarded through the state matrix. So that, past match won't be looked up again. The implication is, a state is an overlapping of choices. It can hardly find combination of of choices now. The best is to keep a trace of the last top choice. The state then is tracking RESULT rather than choice.
    3. Typical DP solution
        1. That's the above.

50. RDMA这十年的反思1：从协议演进的视角 - zarbot
    https://mp.weixin.qq.com/s/G-1LAW8VNpTZAGvlbBOIgg
    RDMA这十年的反思2：从应用和芯片架构的视角
    https://mp.weixin.qq.com/s/JG29nOsCbC-eK8ZqDj9gwg
    RDMA这十年的反思3：AWS HPC为什么不用Infiniband
    https://mp.weixin.qq.com/s/iQjiDSHzY0CrA3xDt5E6fg
    1. Very good. with years of experience from the author
    2. highlights
        1. The RoCE including RoCEv2 started from an sub-optimal path. It requires lossless transport. It's using PFC. Indeed, this caused a lot of problems.
            1. 网络，无非就是三块内容：拓扑，路由和流控。
                1. 第一性原理只有很简单一句话：Smart Edge, Dumb Core。
            2. The source problem of RoCE is it tries to translate semantics and desgin patterns in intra-host PCIe communication into Host-to-host Ethernet domain. It's fine to assume intra-host network is stable, lossless, and fast. But Host-to-host networking is way different. Infiniband is expensive and can replicate properties from PCIe to Host-to-host networking, but Ethernet is different, then RocE hits trouble.
                1. It seems, CXL is heading into a similar pitfall path. Unless CXL is replicating Infiniband.
        2. Different vendors chose different path. Mellanox, AWS SRD, Google Falcon, Microsoft FaRM, DCQCN
        3. AI requirements: Multipathing, Adaptive routing, Packet spraying.

    n. related materials
        1. DPU及网络处理器的历史 - zartbot   [2021]
           https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247486914&idx=1&sn=37d779d3ab6abf8b2460a826f32d0abb
            0. Very good article. 网卡和交换机上已经发生过一轮 软件（服务器）-> 硬件（ASIC卡）-> 硬件微码编程 -> 软件（SDN）-> DPU & P4 的转换。如今也正在存储、云计算、DPU上上演。
            1. 其实网络一开始就是软件定义的，一开始的路由器其实是叫服务器的
                1. 这一时代的很多产品都是基于MIPS处理器实现的
            2. 从软件到硬件转发，技术上还是有一些区别，一方面就是线卡的ASIC如何设计，另一方面就是Fabric的ASIC如何设计
                1. 提出Crossbar架构的路由器 Nick Mckeown
                2. CLOS架构，解决扩展性问题，使用交换单元组成多级交换结构。路由器就这样进入了集群的年代
                3. 硬件转发之Linecard, TCAM, Run-To-Compile（RTC)
            3. 由硬到软：软件定义时代 / SDN
                1. openflow和openvswtich诞生了, VDC/VPC的发展, DPDK, VXLAN和Overlay的兴起
                2. 多核通用处理器性能越来越强，SR-IOV的出现
            4. 又硬了, 网卡也智能~网络也编程
                1. 等大家全软件了，发现CPU资源的50%以上都被网络占用了 .. 于是轰轰烈烈的Offload运动开始了
                2. Segment Routing & P4
                    1. 一方面，通过SR对网络设备进行编码有了SID，然后再编码一个Function和Args， 这样传统的网络设备在执行包头的Destination Lookup的时候， 就可以有更灵活的一个函数Callback栈来实现更多灵活的功能了。
                    2. 另一方面，我们对网络处理器的抽像可以表示成为大量的连续的Match-Action操作，可以弄成pipeline，于是P4也就顺理成章的诞生了。
                    3. SmartNIC
                3. 智能网卡-AWS
                    1. 主要功能就是：承担了原本物理机内虚拟交换机的路由、contrack匹配、ACL过滤、VTEP查表、MAC代答、tunnel建立等工作负载。同时硬件实现了虚拟机粒度的、严格的带宽以及五元组流的QoS
                4. 智能网卡-Azure
                    1. Large-Scale Reconfigurable Computing in a Microsoft Datacenter
                    2. A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services
                5. 拆分->虚拟化，组合->DPU
                    1. 而组合则是将多个CPU socket连接，并attach相应的内存和存储按需构建，也就是Fungible一直强调的DPU概念
            5. Future looking
                1. 软件编码逐渐开始以应用为中心，通信协议本身兼顾软硬件一体。另一方面随着云的资源广泛部署，在边缘云或者更进一步的元宇宙中
                2. 硬件功耗墙决定了在高密度的地方已经无法再添加新的东西了，而Tofino-3或者说Cisco Silicon One或者BRCM这些可编程的交换机基本上也开始碰到物理瓶颈了，将他们的可编程能力释放出来赋予终端，才是未来。
                3. 容器本身也带来了大量的挑战，网络协议栈消耗大，智能网卡PCIe SRIOV配置速度慢，直接的容器内存交付便成为未来的趋势，而Serverless的也将从概念走向商用。多云间的RPC和多云分布式数据库和存储
            6. summary of history
                1986~1995 软件实现为主
                    报文编码 基于目的IP地址的最长匹配做查询
                    软件结构 在软件算法上优化，使用Tree查找和Cache优化
                    硬件结构 大量基于MIPS指令集的CPU进行软件转发，后期逐渐出现了基于总线的分布式转发架构，例如Cisco的7500系列路由器
                1995~2010 由软向硬的过渡
                    报文编码 MPLS简化核心路由表条目数
                    软件结构 软件结构相对稳定没有太大变化
                    硬件结构 专用处理器繁荣的十年，各种专用芯片来做Offload，加密芯片，TCAM查表，各种基于微码的网络处理器，Fabric逐渐采用CLOS架构构建多机集群.
                2010~2015 由硬到软：软件定义时代
                    报文编码 VXLAN和Overlay的兴起
                    软件结构 软件转发的回归，DPDK/VPP等开源软件的出现
                    硬件结构 多核通用处理器性能越来越强，SR-IOV的出现，核心交换芯片越来越强并支持虚拟化
                2015~2019 由软到硬：可编程的智能网卡时代
                    报文编码 SegmentRouting，数据包即指令
                    软件结构 容器技术的出现，CNI触发Host Overlay，尽量采用协处理器或者网络设备卸载负担, P4等通用网络编程语言的出现
                    硬件结构 可编程交换芯片的出现，各种SmartNIC方案盛行，低延迟通信的需求日益增加，特别是AI带来的快速I/O响应

        n. Related materials
            1. NetDAM: DPU新范式: 网络大坝和可编程存内计算 - Zartbot
               https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247486644&idx=1&sn=a2a18f661c18bfb96a37d5ac0d1a9653
                1. Referenced by parent by "而这些技术也成了我们设计NetDAM的雏形，所有的I/O和CPU核之间有一块内存，而不是简简单单的一个Buffer，精髓就在于此"
                2. MPI Allreduce应用
                    1. Ring Reduce-Scatter
                    2. Ring All-Gather

            2. 洞见：下一个十年的云计算架构 - Zartbot
               https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247486799&idx=2&sn=fbaa307df3c39dcc7417d94b37605d1b
                1. 对于终端接入云,我们实现了基于Internet 200ms全球零丢包可达的实时音视频传输RTN的关键技术创新
                   在接入访问控制和流量调度中,我们实现了基于人工智能的ZaDNS优选路径和零信任接入访问能力(已开源)
                   在数据中心我们实现了新一代大规模数据中分布式路由协议及SDN控制技术的研发，并和广域网RTN及用户态传输融合实现了端到端的可控转发
                   同时针对数据中心拥塞实现了基于强化学习的自动驾驶网络技术
                2. 通过自研DPU在计算机体系架构中取得了革命性的创新，实现了一种以数据为中心的可编程计算指令体系架构，
                   并且整体通信延迟比广泛使用的RoCE技术低了20%抖动下降两个数量级，
                   并针对下一代云计算AI关键应用实现了存内计算和在网计算的关键加速能力。
                   同时构建了大规模内存池化和异构计算池化技术,也为片上网络和先进封装等DSA需求预留了接口
                3. 在Google swift拥塞控制基础上实现了关键性创新，隔离I/O域和计算域，在主机拥塞控制上实现了确定性延迟和更直观的缓存深度感知， 
                   并实现了用户态内存直达和多路径访问，配合自动驾驶网络实现了确定性转发，同时针对大象流实现了网内缓存和按包拆分的能力。
                   最后，由于我们的用户态内存直达，实现了零损耗的计算能力，计算资源直接通过用户态内存访问，实现了整个通信栈的卸载，也方便了异构计算器件的调用。

            3. 智能网卡的智障需求 - Zartbot
               https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247485976&idx=1&sn=ad0f06d5ea4acde5f79658f4c69dc871
                1. 所以智能网卡的最智障需求就是：
                        PCIe和以太网传输协议的互通及互相Overlay
                        符合资源拆分场景：实现裸金属虚拟化
                        符合资源组合场景: 实现多池化设备动态组网
                        拥塞控制: QoS和swift一类的拥塞算法，满足SLA需求.
                   基于这样的解释，你也就会不难理解一张智能网卡什么是刚需了
                2. "在DMA和Ethernet上配置P4处理矩阵)就很容的构建了FastPath和SlowPath的架构了。"
            
            4. 包处理的艺术(4)-低延迟智能网卡设计 - Zartbot - [2021]
               https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247485370&idx=1&sn=3b5590ccf58909f2d390df00bfb5d853
                0. very good article
                1. 低延迟网卡的常见解决方案
                    1. Kernel bypass
                        1. Solarflare NIC
                    2. UDP market data parser
                        1. 行情硬件解码机制
                    3. TCP Offload Engine(TOE)
                        1. 通常行情是UDP的但是报盘是TCP的
                2. 常见的高频交易业务模式
                    1. 我们来看传统的通信模式，通常为了降低延迟抖动我们会把航企和交易的接口分开，传统的做法需要经过两次PCIe，这样贡献的延迟大概为2us以上，因此大量早期的低延迟智能网卡的做法便是Bypass PCIE和CPU，直接把算法弄在网卡上。
                    2. 参考一下Pensando和Fungible的处理方式
                3. 传统CPU报文处理的缺陷
                    1. 在CPU处理数据报文中，主要的延迟来自于报文解析(Packet Parser)
                    2. P4硬件parse
                        1. Match-Action Unit (MAU) 流水线
                    3. Pensando报文处理方式
                        1. 最特别的设计就是和SOC域的DRAM构建了一个Cache coherent的本地缓存，然后增加了一些访存的DMA指令，这样的好处在于NetPath和SoCPath的编程更加简单
                    4. Fungible报文处理方式
                        1. 将各种Offload engine和处理器整合的方式构成一个DataCluster，单个Data Cluster采用6核4线程的结构，并且配合专门的加速协处理器，例如Lookup engine、Security engine等
                        2. HotChip 2020: https://www.hc32.hotchips.org/assets/program/conference/day2/HotChips2020_Networking_Fungible_v04.pdf

                        n. related materials
                            1. Fungible F1 DPU Powered Storage Hands-on at Fungible HQ
                               https://www.youtube.com/watch?v=NjhTTMNGBBw
                                1. Disaggregated servers: x86 servers + GPU servers + SSD servers + HDD servers
                                2. Before: SmartNIC is just a bunch of ARM processors + PCIe + Ethernet
                                   After - Fungible: Node + DPU + TrueFabric
                                3. Highlights
                                    1. Network engine - P4, TrueFabric endpoint
                                    2. HBM - on-chip memory (think CPU cache)
                                    3. 8 Data Clusters: 6 Cores * 4 threads each.
                                       1 Control Cluster: Security boot, key, true random number generator
                                        1. Separate two data/control engines. This is borrowed from networking area.
                                            1. Good point. Fungible founder Pradeep Sindhu actually came from Juniper Networks, he was the chief scientist.
                                            2. Data-centric: Agility, Security, Performance, Reliability, Cost 
                                        2. MIPS-64, it's not even ARM core. 
                                            1. 
                                    4. Host Unit can plug x86 or ARM CPU, supports SR-IOV
                                    5. "因为是RTC的所以完全兼容C代码程序"
                                       https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247485370&idx=3&sn=b942ece597aaed0023b730dcb0a91a00
                                    6. Worker Scheduler
                                        1. Note, this is hardware backed scheduler, rather than typically thread scheduler by OS that is software
                                        2. NanoPU
                                           https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247485370&idx=3&sn=b942ece597aaed0023b730dcb0a91a00
                                            1. "在超过100个核心的ManyCore处理上，片上网络和通信延迟时一个必须要考虑的问题。这篇文章的解决方法就是"Replacing the software thread scheduler and core-selector with hardware, by bypassing PCIe，main Memory and cache hierarchy completely""

                            2. MIPS, ARM, X86, NPU, What’s the Best Hardware Platform for Your IoT Gateway?
                               https://www.dusuniot.com/blog/mips-vs-arm-vs-x86-vs-npu-the-best-hardware-platform-for-iot-gateways/
                                1. Today, chips based on MIPS architecture are widely used in many electronic products, network equipment, personal entertainment devices and commercial devices. 

                            3. SDC2022 – Next-Generation Storage will Use DPUs instead of CPUs
                               https://www.youtube.com/watch?v=nml5ha84ZzQ&t=2s

            5. 包处理的艺术(3)-RTC vs Pipeline - Zartbot
               https://mp.weixin.qq.com/s?__biz=MzUxNzQ5MTExNw==&mid=2247485370&idx=3&sn=b942ece597aaed0023b730dcb0a91a00
                0. very good article.
                1. 正如这本书中所描述的计算机体系结构的8个伟大想法
                    1. 面向摩尔定律的设计, 架构师必须在设计之初预测其设计完成时的工艺水平。而以太网速度最近几年的爆炸式增长已经超越了摩尔定律，新的器件工艺的诞生(例如：Serdes/RAM/Optics/Packaging)也为处理能力提升奠定了基础。
                    2. 使用抽象简化设计，通常的做法是隐藏低层细节以提供给高层一个更简单的模型，网络的分层是一种做法，另一种做法就是包处理艺术<2>中讲到的同构，例如用一堆CPU构造成一个大路由器(多线卡分布式转发），然后一系列大路由器构造成一个集群(CRS/JNPR-TX/NE5000)，然后随着硅工艺的进步，又把多个CPU核心弄到一个硅芯片上，从而诞生了片上网络，更进一步直接把多个路由器放置在一个芯片上(Cisco Silicon One)。
                    3.加速经常性事件，例如早期对查表算法的优化，到后期offload或者出现FastPath的做法都是这种思维的体现。
                    4.通过并行提高性能，典型的做法就是多核CPU执行并行转发。
                    5.通过流水线提高性能，这也就是本文重点，流水线和RTC的区别。
                    6.通过预测提高性能，DPDK中有大量的分支预测的帮助函数，您会经常的看到likely/unlikely的处理
                    7.储存层次，cacheline对齐，zero copy等处理方式，或者以VPP为代表的优化I-cache的处理方式，以及核上对于Cache size的调优(例如思科针对企业多业务路由器QuantumFlow 和针对运营商的nxPower的区别)
                    8.通过冗余提高可靠性，单机双引擎，双机双引擎各种热备冷备技术都在用，还有SDWAN中的packet duplication，以及Tofu-D中针对误码率高了以后的双链路同时发送bypass RS-FEC都是这类思维的代表。
                2. 流水线和RTC的区别
                    1. RTC
                        1. 报文进入后通常会有一个调度分发器(Packet Distributor)，然后调度到相应的报文处理引擎(Packet Processing Engine,PPE)处理，调度算法可以有基于包的，也有基于流的，具体在包处理的艺术(4)中分析。
                        2. 而PPE的结构基本上都是标准的冯诺依曼架构处理器，有相应的指令内存，数据内存，寄存器，ALU，程序计数器(PC)等结构
                        3. 通常在RTC的处理结构中，我们可以灵活的使用C等多种高级语言编程，然后编译成一系列指令执行，有更高的灵活度，而每个报文在处理器内部的处理时间会有不同，例如很多简单的软件功能可能几个条指令就处理完，然后就可以转发。这也是Silicon One功耗低的本质原因
                    2. Pipeline
                        1. 最早期的流水线结构是通过多个ASIC实现的，典型的就是以Juniper M系列为代表
                        2. 最终单芯片多流水线架构就出现了
                    3. RTC vs pipeline
                        1. 通常我们对于流水线的定义为傻和快，傻是缺少灵活性的意思，当芯片设计好它支持的处理能力就固定了。而RTC架构通常是灵活但相对较慢的代名词，后期您可以通过软件代码的方式加入新的功能，这是RTC架构的优势。
                        2. Pipeline in RTC
                        3. 流水线空转问题
                        4. 可编程流水线的发展
                        5. 既然UADP验证了可编程ASIC的成功，那么就再进一步在工具链和底层结构上各自向中间靠拢一步，这就是P4.
                        6. 可以通过pipeline固化加速，也可以通过RTC获得灵活的业务。
                3. 每一块芯片设计的过程中取舍是什么？
                    1. Memory以何种形态出现，要多大，放在片上还是片外，这些内存墙的因素直接决定了包处理的架构。客户在不同的场合下需要不同的内存访问模型
                    2. ChatGPT: Factors to consider in chip design
                       https://chatgpt.com/c/4abc3238-3a5f-4a95-ac9e-992e7de76726
                        1. Performance Requirements:
                                Throughput and Latency
                                Parallelism

                            Power Efficiency:
                                Power Consumption
                                Thermal Management

                            Memory Architecture:
                                Memory Bandwidth
                                On-Chip Memory
                                Memory Hierarchy

                            Data Flow and Interconnects:
                                Data Movement
                                Interconnects

                            Scalability:
                                Modularity
                                Fabrication Technology

                            AI-Specific Features:
                                Accelerators
                                Support for AI Frameworks

                            Flexibility and Programmability:
                                Reconfigurability
                                Programmable Logic

                            Reliability and Fault Tolerance:
                                Error Correction
                                Redundancy

                            Cost Considerations:
                                Manufacturing Cost
                                Market Demand

                            Security:
                                Data Security
                                Secure Boot and Encryption
                
                4. Smart Edge & Dummy Core
                    1. "网络界通常针对分布式系统复杂性的另一种思路就是边缘智能和简单的核心。所以你会看到云计算发展到一定程度后也逐渐开始往边缘计算靠拢"
                        1. Good comment

            6. 包处理的艺术(2)-控制面协议设计 - Zarbot    [2021]
               https://mp.weixin.qq.com/s/m0QCtKskB7WZQrVRZyx_Fg
                1. 深度优先的设计思维 - bad
                    1. 通常在设计协议时回溯自己走过的光辉历程并将自己的职业生涯和已有项目经验复用便成了最佳实践。这样的思维方式解决小规模的问题非常棒，毕竟可以很快速的通过类比理解需求和最小的工程代价实现。
                    2. 通常这个时候解决问题还是按照一线研发的思路，定义好一个很小的问题，然后逐渐细化到差不多代码层级能工作了，也就认为协议设计做完了，但最后却成了一个工程灾难。 ... 实际上这种以深度优先寻找解决方案的设计思维变成了自底而上的设计方法。
                2. 广度优先的设计思维 - well
                    1. 我在处理这样的问题的时候，通常会进一步的去抽象问题，找到各个场景的共同点，类似于合并问题分支，另一方面是从原理上出发去找到一些理论上不可行的解决方案，通过剪支来降低问题的规模。最后适当的约束问题的规模，然后尽力的去找到相对约束条件下的可行解，并且清楚的明白自己取了什么，舍弃了什么。

            7. 包处理的艺术(1)-从大自然中学习 - Zarbot    [2021]
               https://mp.weixin.qq.com/s/FapDC_1HmVu5isZ6P562nA

            8. RFC: The Twelve Networking Truths
               https://datatracker.ietf.org/doc/html/rfc1925
                1. good.
                2. (1)  It Has To Work.

                   (2)  No matter how hard you push and no matter what the priority,
                        you can't increase the speed of light.

                        (2a) (corollary). No matter how hard you try, you can't make a
                             baby in much less than 9 months. Trying to speed this up
                             *might* make it slower, but it won't make it happen any
                             quicker.

                   (3)  With sufficient thrust, pigs fly just fine. However, this is
                        not necessarily a good idea. It is hard to be sure where they
                        are going to land, and it could be dangerous sitting under them
                        as they fly overhead.

                   (4)  Some things in life can never be fully appreciated nor
                        understood unless experienced firsthand. Some things in
                        networking can never be fully understood by someone who neither
                        builds commercial networking equipment nor runs an operational
                        network.

                   (5)  It is always possible to aglutenate multiple separate problems
                        into a single complex interdependent solution. In most cases
                        this is a bad idea.

                   (6)  It is easier to move a problem around (for example, by moving
                        the problem to a different part of the overall network
                        architecture) than it is to solve it.

                        (6a) (corollary). It is always possible to add another level of
                             indirection.

                   (7)  It is always something

                        (7a) (corollary). Good, Fast, Cheap: Pick any two (you can't
                            have all three).

                   (8)  It is more complicated than you think.

                   (9)  For all resources, whatever it is, you need more.

                       (9a) (corollary) Every networking problem always takes longer to
                            solve than it seems like it should.

                   (10) One size never fits all.

                   (11) Every old idea will be proposed again with a different name and
                        a different presentation, regardless of whether it works.

                        (11a) (corollary). See rule 6a.

                   (12) In protocol design, perfection has been reached not when there
                        is nothing left to add, but when there is nothing left to take
                        away.

51. Problem: 在二叉树中寻找两个节点的最近公共父节点
    1. Observation:
        1. If depth search, the common parent can be N levels away. Probably needs a tracing array of size N.
        2. The common parent of A and B is the same common parent of ancestor A and B.
        3. The A and B in question must be leaves.
        4. The distance of sibling link would directly tell the common ancestor.
        5. Root is the first ancestor
        6. If a node has reverse link, or a node has sibling link, the problem becomes trivial.
        7. The full reverse track of a node is log(N)

    2. Assumption:
        1. You would need at least one full node search to get the result.

    3. Possible exploration:
        1. You would need at least one full node search to get the result.
          1. Solution 1:
            1. A full search to give leave nodes numbers. Use the number id to derive their common parent.
                1. Problem 1: What if the depth of A and B are different?
                    1. Use the level of A (assume smaller). When searching B, track it's level(B)-level(A) ancestor.
                2. Problem 2: How to use the number id to derive common parent?
                    1. Distance 1
                        1. 0+2N -> 1+2N, common parent is immediate ancestor
                    2. Distance 2
                        1. Go up one level by divide by 2
                    3. Distance N
                        1. Go up one level by divide by 2, until the number id of A and B are equal
                3. Problem 3: How to mark numbers?
                    1. Use breadth search to reach level(A), and then switch to depth search to level(B).
                       It's remarkable that this algorithm problem tests both breadth search and depth search.

        2. Depth search 
            1. Solution 4: Search node A, save the path. Search node B, save the path. Intersect.

        2.5. Use two single search for single node and combine
            1. Same Solution 4.

        3. Breadth search
        4. Bottom up

        5. The binary tree is represented by an array, where each node uniquely maps to an array index
           https://www.prepbytes.com/blog/tree/array-representation-of-binary-tree/
            1. Observation
                1. The number id of any node maps to its order in a breadth search.
                2. Marking such number id is equivalent to that each node has reverse link and sibling link
                3. (number id - 1)/2 goes to a node's immediate ancestor
                4. [2^l - 1, 2^l-1+ 2^l-1] can derive a node's level

                       level l: 2^l nodes
                       level l sum = 2^0 + ... + 2^l = 2^(l+1) - 1
                       level l start = 2^l - 1
            
            2. Solution 2: Getting the common parent is trivial.
                1. Calculate level of A, B
                2. Repeat tracing parent by (number id - 1)/2

        6. Assuming NO need a full node search
            1. Looks like there isn't such an algorithm. Then all possible solutions map to full tree search + pruning + optimization + write nicer recursion code.

        7. Recursive divide and concur
            1. Observation
                1. If a node is the common parent node, it must have node A presents in one branch, node B presents in the other branch.
            2. Solution 3: by ChatGPT - Lowest common ancestor (LCA): https://chatgpt.com/share/cee90273-6791-4dd8-9679-35e57d513c36
            3. Potential problems
                1. What if there are 3 nodes to find the common parent?
                    1. It should still work in ChatGPT's algorithm to up propagate the last LCA

        8. Engineering solution
            1. Just add reverse links and sibling links to the binary tree. Or add the node number id to each node. Everything is simple and trivial then.


52. 万字长文讲透低代码 - 风轻扬    [2021]
    https://mp.weixin.qq.com/s/OXCBORheAx99o3fS-ZfUdg
    1. OutSystems就是专业低代码平台的代表
    2. 六项区分度最高的判断标准：模型驱动、可视化开发、表达式语言、软件工程、开放集成和脚本语言
    3. 把企业应用的复杂性分解为数据、权限、流程、算法、集成、报表等六个维度

    n. related materials
        1. APaaS搞不定复杂的应用，是这样吗？
           https://blog.mingdao.com/16803.html
            1. Interesting

53. 腾讯云 4.8 故障原因曝光：因 API 新版本兼容性不够和配置数据灰度机制不足
    https://mp.weixin.qq.com/s/IsSOksLOCZqyX-X8_xsyWw
    1. 转载：腾讯云4月8日故障复盘及情况说明
       https://mp.weixin.qq.com/s/Y1Rt2C0jD80GuVCIUTJH2w
    2. 中立分析腾讯云故障相关的事件
       https://mp.weixin.qq.com/s/yu2IUIiTfv017w7kO0HP8Q

54. XSKY CTO 在英特尔存储技术峰会的演讲：LLM 存储，架构至关重要
    https://mp.weixin.qq.com/s/t4C9IQpAViOSyn8lsd6PKg
    1. 高带宽存储（HBM）成为解决存储瓶颈的关键技术之一，它能够显著提升存储系统的性能
        n. Related materials
            1. 探究NVMe SSD HMB应用场景与影响 - 古猫先生
               https://mp.weixin.qq.com/s/Uvheog_Ih6hm-nxFg1VAxg

    2. 在大模型训练中，存储系统需要处理的大量数据写入，这使得存储写带宽成为决定性能竞争力的关键因素
        1. 特别是在多模态场景中，大量小文件
    3. 星辰天合最新发布的 XSEA（eXtreme Shared-Everything Architecture，极速全共享架构）
        1. 亚健康网络问题时，能在 100 毫秒内快速切换
        2. 采用了单层 SSD 架构，可以借助 QAT 加速数据压缩/解压缩的强大能力，采用大规模的 EC+压缩
        3. 采用了端到端的 NVME，因此能够实现 100 微秒的低延迟
        4. 通过全局 EC 和数据压缩技术，实现写放大的 100%降低，提升存储效率

55. 为什么每个数据科学家都要读一读Judea Pearl的《The Book of Why》 - 机器之心
    https://mp.weixin.qq.com/s/9g77_Igy6SHwOBLhKqYv3w
    1. 我应该把这个变量添加到模型里面吗？
        为什么这个反直觉的变量会作为一个预测结果出现？
        为什么当我增加另一个变量的时候这个变量就会突然变得没有意义？
        为什么相关性的方向与我所认为的会相反呢？
        为什么我所认为的一个很高的相关性结果却是零相关呢？
        当我将数据分解成几个子部分的时候，为什么关系的方向会反过来？
    2. 因果关系比关联更加鲁棒，在迁移后，因果仍然成立，而关联关系可能消失
       因果关系中，可以通过干预因而影响果，而关联关系中不能

56. 华为昇腾芯片跟英伟达的芯片相比，差在哪里？ - llk
    https://www.zhihu.com/question/651132283/answer/3459186418
    1. Ascend提供的片间互联HCCS和NVIDIA的NVLINK相比有显著的差异
       Ascend提供的系统扩展方案有限，相反，NVIDIA可以提供从NVlink，NVSwitch到Infiniband，Ethernet完整的互联扩展方案
       Ascend支持的软件生态也需要兼容CUDA才能更好被用户接受，这一点和NVIDIA差距也很大
    2. Useful as how to analyze chips

57. Data Layout的进化史：从Partition到Z-Order再到Liquid - 红星闪闪
    https://zhuanlan.zhihu.com/p/696053812
    1. DeltaLake
    2. Partitioning, Order Clustering, Z-Order Clustering, Liquid Clustering, Stable Cube

56. 全网最细！LSM-tree delete 性能优化(RocksDB,Lethe) - 黄金架构师
    https://zhuanlan.zhihu.com/p/647180030
    1. 介绍 LSM-tree 在 delete 上面临的一些性能问题。
       介绍 RocksDB 和 Lethe 提供的一些优化方案。
    2. RocksDB 优化
        1. 优化 delete tombstone
        2. 优化 range delete
    3. Lethe 的 KiWi 和 FADE
        1. KiWi 优化 non-sort key 的 range delete 问题
        2. FADE 解决 time-bounded delete 问题
    n. related materials
        1. Lethe 如何优化 LSM-Tree delete 难题 - DataWonder
           https://zhuanlan.zhihu.com/p/291135599

57. TPFS: A High-Performance Tiered File System for Persistent Memories and Disks——论文泛读 - 妙BOOK言
    1. 根据同步性、写入大小和读取频率，将传入I/O引导到PM、DRAM或磁盘。包括三个预测器，分析文件I/O序列，预测：传入的写入是否既大又稳定；对文件的更新是否是同步的；文件是否频繁读取。根据预测将I/O请求引导到最合适的层：对同步更新的I/O传入PM层，减少同步开销；小的随机写入传入PM层，以避免对磁盘的随机写入；异步更新和大型顺序写入传入磁盘；经常读取的文件迁移到磁盘，并缓存在DRAM中。
    2. 在线评测应用程序的访问流，估计文件数据的温度，选择要迁移的冷写和热读的文件数据块，将相邻数据块合并迁移到磁盘。根据应用程序访问模式调整迁移策略。

58. 为什么现在的LLM都是Decoder only的架构 - 成诚
    https://www.zhihu.com/question/588325646/answer/3422090041
    0. good
    1. Fig 1. The evolutionary tree of modern LLMs
        1. good
    2. 个人觉得 Decoder-Only 的架构最核心的优势是非常方便于 Scale Up，基于 Scaling Laws 的实际训练成本最低
        1. 在 LLM 时代，如果你提出的新的算法结构可能有 5% 的效果提升，但是引入了额外 50% 的训练成本（计算时间 or 通信量） 的话，那这个新的算法一定是一个负优化
        2. 比较 Encoder-Only、Encoder-Decoder、Decoder-Only 三者架构： 
            相同参数量的训练效率上：Decoder-Only > Encoder-Only > Encoder-Decoder
            现行分布式并行策略下，可以扩展的 参数量上限 和 分布式集群规模的上限：Decoder-Only  Encoder-Only >> Encoder-Decoder
    3. NVIDIA 在 3076 张 A100 集群上训练的 1T 参数量 LLM 使用的并行方式是
        1. Data Parallel Size = 6
            Tensor Parallel Size = 8
            Pipeline Parallel Size = 64
        2. 为什么在三千卡集群上最主要的并行方式是流水并行？
            1. 流水并行的核心优势就是用比较少的 Pipeline Bubble 代价 （当 gradient accumulation step 很大时可以忽略不计），较少的 Tensor Buffer 显存代价，以及非常低的通信开销，将大模型分割在不同的 Group 中。 大幅减少了单张 GPU 上的 weight tensor 大小（数量） 和 Activation tensor 大小（数量）。
            2. 同时，跟 Tensor Parallel 相比， Pipeline Parallel 的通信代价很低且可以被 overlap， Tensor Parallel 虽然也能切分模型大小，但是需要全量的数据（没有减少 Activation tensor 大小），另外极高的通信频率和通信量使得 Tensor Parallel 只能在机器内 8 张卡用 NVLink 等高速互联来实现，跨机的 TP 会严重拖慢速度。
            3. 然而流水并行有很重要的约束条件：  需要一个 规整对称的、线性顺序的网络结构。GPT 就是这样一个典型的网络结构： 完全一样的 Transformer Layer 顺序堆叠，没有分叉和不对称情况，当均匀切分 Layer 时，各个 Stage 的前向/反向计算时间均一致。

    n. related materials
        1. Current Best Practices for Training LLMs from Scratch - Rebecca Li, Andrea Parker, Justin Tenuto
           https://www.scribd.com/document/654166672/Current-Best-Practices-for-Training-LLMs-from-Scratch-Final
           1. good

59. 如何分析一个系统的架构？ - 蒙的解析
    https://www.zhihu.com/question/23800004/answer/3455840197
    1. Interesting topic on Google Map
    n. related materials
        1. DDD在大众点评交易系统演进中的应用
           https://zhuanlan.zhihu.com/p/696918026
            1. Good example to understand DDD
            2. Highlights
                1. 用例分析阶段
                    1. 参与方, 行为
                    2. 流程时序图
                    3. 坚持使用统一语言
                2. 问题域分析阶段
                    1. 在统一语言上，通过用例分析我们提炼了商家、买家、商品等统一语言
                    2. 在子域划分上，我们最终识别出了如图所示的这样几个子域
                    3. 核心域、支持域、子域
                3. 识别限界上下文
                    1. 限界上下文的识别是对问题域拆分和求解，同时限界上下文也是应用的边界和技术的边界
                    2. 我们从质量属性、服务集成和功能复用三个方面对限界上下文做进一步的划分。限界上下文封装了按照纵向切分的业务能力，多个限界上下文协作来完成一个完整的业务场景。
                    3. 通信集成模式和团队协作模式来映射限界上下文，用到最多的是通过防腐层、开放主机服务和发布语言三者联动来隔离上下游的变化、维护整个领域模型的稳定性。
                    4. 自治单元：最小完备，稳定空间，自我履行，独立进化
                4. 领域建模
                    1. 领域分析建模
                        1. 对用例以及用例规约和用户故事进行详细的分析，从中通过名词法和动词法寻找领域概念来构建我们的领域分析模型
                    2. 领域设计建模
                        1. 定义领域行为，定义聚合，添加领域服务和领域事件
                5. 模型实现
                    1. 代码实现阶段
                    2. 按照限界上下文划分微服务，服务内部按照分层架构进行实现
                    3. 分为接入层、应用层、领域层和基础设施层。最终需要维护领域层的稳定性
                6. 平台化阶段
                    1. 平台领域模型和各业务的扩展模型
                    2. 将平台领域模型拆解为基础领域模型，以及预订业务模型、团购业务模型等按照业务形态划分的领域模型
                    3. 基于插件化的集成开发模式。通过扩展点的定义，由各业务线在各自的插件包里基于业务扩展模型进行业务定制化实现，再集成平台领域模型和业务扩展模型，最后实现完整的业务流程和业务场景。

60. 数据库大事务优化方法 - bluesky
    https://zhuanlan.zhihu.com/p/691601859?utm_id=0
    1. 拆分大事务, 使用批处理, 使用乐观锁
    2. 优化事务日志写入性能
    3. 使用分布式事务
    4. 缓存数据

61. Meta如何将缓存一致性提高到99.99999999% - Mayank Sharma
    https://mp.weixin.qq.com/s/21fXm7Bv9DOREGOqytXNTA
    1. Polaris
        1. Polaris接收到x=4版本4的失效事件, 检查所有缓存副本, 以验证是否发生其他违规情况
        2. 下一个问题：但当Polaris检查缓存时，却找不到x的条目，可能是缓存有旧数据，可能是缓存有新版本删除了数据
            1. 为了验证这两种情况Polaris需要通过查询数据库进行检查。Polaris的解决方案是，延迟执行此类检查并调用数据库，直到不一致的样本超过设定的阈值（例如1分钟或5分钟）。目前Polaris提供了一个指标：表示在五分钟的时间尺度内，99.99999999%的缓存是一致的。
        3. 日志和troubleshooting
            1. 记录每个缓存数据更改几乎是不可能的，但如果我们只记录那些有可能导致不一致性的更改
            2. Potential Racing Window

62. QR分解就是这么简单 - mashuangwe
    https://zhuanlan.zhihu.com/p/624905041?utm_id=0
    1. 利用矩阵分解来简化计算机矩阵求逆。将待求逆矩阵A分解为BC，其中C为上三角矩阵（易求逆），且B为正交矩阵（易求逆）
    2. Good article to understand QR decomposition
    3. Highlights
        1. 如何变上三角矩阵？
            1. 高斯变换
            2. 旋转矩阵
            3. 镜像变换 - Household变换
        1. 旋转矩阵, 正交矩阵
        2. Household变换, 高维空间
            1. Household矩阵的性质 - 它也是正交矩阵（良好对称性、可逆性，犹如镜像）
        3. 矩阵的QR分解
            1. 利用Household变换，求逆过程只需乘法。随QR分解进行，矩阵维度逐渐减小

63. Jacob：从3年后的EPS看，现在的微软是否值得介入 - 雅格布
    https://mp.weixin.qq.com/s/IU03qeV53bcK75U-sfRMGg
    1. Good. 使用市场规模，营收增长率，EPS，市盈率(P/E)，计算股价。
    2. P/E = per stock price / EPS
            = per stock price / ((net income - preferred dividends) / common shares)
            = per stock price * common shares / net income'
            = years that the stock will pay off its price with net income

        30年美债的P/E = per stock price * common shares / net income
                 = 1000 * 100 / (1000 * 100 * 4.6%)
                 = 1 / 4.6%
                 = 1 / 年利率

        因此，P/E高于美债，那么必须预期股价上涨。 P/E反映市场对股价上涨的期望。

    3. How much stock price growth can compensate the high P/E than baseline?
        1. Assume P/E is constant. Suppose net income grows by X% per year
           Then we can see "per stock price" would grow by X% per year

        2. P/E = 1 / 年利率。 那么，
              股票的虚拟年利率 = 1 / P/E
           Then
              X% = 1 / (P/E baseline) - 1 / P/E
           Take MSFT as an example
              X% = 4.6% - 1/37.32 = 4.6% - 2.68% = 1.92%

        3. Net income 并不能直接回报普通股民，因此可认为
              X% = 4.6% - 0 = 4.6%
           即，持有公司股票则预期股价增长超过国债

        4. 实际回报给股民的是Dividend（股息）, Dividend Per Share - DPS. Yield% = DPS / stock price. 
           EPS Payout Ratio 显示公司收入有多少比例用于支付股民的股息
           https://in.investing.com/equities/microsoft-corp-historical-data-dividends 

           因此，上述公式应该为
            X% = Baseline interest rate - Yield%
               = 4.6% - 0.72%    // MSFT
               = 3.88%
           即，股价增长率以补偿股票回报的不足

        5. DPS 如何受股价影响？以及P/E如何影响股价？
            1. EPS Payout Ratio = Dividend per share / EPS 
                    = Dividend per share / (net income' / common shares)
               可以看到，EPS Payout Ratio 一般不受股价影响

               Then,
                Yield% = DPS / stock price 
                    = EPS * EPS Payout Ratio / stock price
                    = 11.53 * 26% / 420    // MSFT
                    = 0.71%

            2. DPS 和 P/E 关系如何？
                1. DPS = EPS Payout Ratio * EPS
                   P/E = Stock price / EPS

                   So,
                    DPS = EPS Payout Ratio * stock price / P/E

                   Then,
                    X% = Baseline interest rate - Yield%
                       = Baseline interest rate - EPS Payout Ratio * EPS / stock price
                       = Baseline interest rate - EPS Payout Ratio / P/E
                       = 4.6% - 26% / 37.32    // MSFT
                       = 3.9%

                    即，当前P/E意味着股民期望MSFT的股价有3.9%的年增长率

            3. 由上式可见
                1. 为维持当前P/E，股价必须与EPS（由营收反映）有同样的增长率。
                   如果股价增长慢于营收增长，则X%增大，更多股民买入，导致股价增长。
                   如果股价增长快于营收增长，或营收增长降低，则X%减小，股民卖出，导致股价下跌。
                   P/E有自身稳定性，可以假定其不变。

                   P/E的变化？其反映股民对公司股价增长的信念变化。
                   例如，股价增长将快于营收增长，则P/E增大，而股价投资回报X%同步增大。

                   也可以看到，股价维持来自于营收增长。如果营收不涨，或者维持不变则，股价很可能大幅下降。
                   在营收不变的情形下，股价会下降到DPS能够满足X%。X%由股息支撑，而不是股价增长。
                   也可以看出，股价的崩溃有可能快速发生， 只在营收增长跨过X%线、财报发布的一瞬间。

        6. 假设为维持当前P/E，
                P/E = stock price / EPS
            则公司EPS应维持X%的增长率，either营收有X%的增长，或者成本有下降。
            假定成本不变，则要求营收有X%的增长。

            假设公司某部门的营收占比为Y%，则可能要求部门营收有更高增长率以拖动全局

            1. 以MSFT为例，Cloud部门营收占比38%。假设其它部门无增长，则为达成3.9%的年增长率，Cloud部门营收需增长10.26%。
               事实上MSFT的Cloud部门营收增长有21%，这还没包括规模效益导致的COGS下降。此外，MSFT整体增长率也有6.9%。

                https://news.microsoft.com/2024/04/25/microsoft-cloud-strength-fuels-third-quarter-results-3/
                https://stockanalysis.com/stocks/msft/revenue/
                https://www.statista.com/statistics/273482/segment-revenue-of-microsoft/
                https://www.visualcapitalist.com/microsofts-revenue-by-product-line/
                https://www.kamilfranek.com/microsoft-revenue-breakdown/

            2. 对于公司部门而言，为维持股价，则需追上维持P/E所需的X%
                 X% = Baseline interest rate - EPS Payout Ratio / P/E
               EPS增长率需要达到X%，either从营收增长角度，或者成本下降角度。

                1. "Cost - Y%" maps to net income beccomes 1 + Cost * Y% / (Revenue - Cost). 在Cost占大头的业务（多数），从Cost下手更容易满足X%。
                2. Cost可分为人力成本、服务器成本、营销成本等。可见裁员能够在短期内迅速提高股价，尤其是人力占大头的业务。而服务器占大头的业务，技术类降COGS非常有用。

                3. Very good analysis.

        7. 上述分析未考虑风险溢价。可以由beta系数计算风险溢价，修改后的公式为

            X% = Baseline interest rate + beta * ERP - Yield%
                // X% 为期望的stock price增长，也是维持P/E所需的EPS增长。

            其中，
                1. beta, 贝塔系数，反映股价相对市场均价的波动幅度
                   https://zh.wikipedia.org/wiki/Beta%E7%B3%BB%E6%95%B0

                2. ERP = Equity Risk Premium = 风险溢价
                   计算方式是 
                        Equity Risk Premium (ERP) = Expected Market Return (rm) – Risk Free Rate (rf)
                        rm = Market Rate of Return (S&P 500)
                        rf = 10-Year Treasury Note Yield
                   https://www.wallstreetprep.com/knowledge/equity-risk-premium/

                3. CAPM模型：Expected Return (Ke) = rf + β (rm – rf)
                   https://www.wallstreetprep.com/knowledge/capm-capital-asset-pricing-model/

            代入MSFT 和 S&P500 5年增长率 和 10-year treasure note (10年期国债)
                https://in.investing.com/equities/microsoft-corp
                https://in.investing.com/indices/us-spx-500
                https://www.cnbc.com/quotes/US10Y

                X% = 4.6% + 0.893 * ((5320 - 2952)/2952/5 - 4.582%)
                   = 14.8%

                MSFT在2018.6 - 2022.6财年，Revenue增长仍在14%-17%，但2023年只有6.88%。
                https://stockanalysis.com/stocks/msft/revenue/
                https://stockanalysis.com/stocks/amzn/revenue/
                https://stockanalysis.com/stocks/aapl/revenue/
                https://stockanalysis.com/stocks/goog/revenue/
                https://stockanalysis.com/stocks/meta/
                https://stockanalysis.com/stocks/nvda/

                MSFT云Cloud部门 Revenue 增长仍强劲。2024 - 17%，2023 - 22%，2022 - 25%。
                https://news.microsoft.com/2024/04/25/microsoft-cloud-strength-fuels-third-quarter-results-3/
                https://news.microsoft.com/2024/01/30/microsoft-cloud-strength-drives-second-quarter-results-4/
                https://www.microsoft.com/investor/reports/ar23/index.html
                https://www.microsoft.com/en-us/Investor/earnings/FY-2022-Q4/intelligent-cloud-performance

                2023年S&P 500的增长有26%，主要由Nivdia等芯片半导体商驱动
                https://www.investors.com/etfs-and-funds/sectors/sp500-stocks-insane-growth-is-about-to-blow-the-doors-off/
                https://in.investing.com/indices/us-spx-500    // US
                https://in.investing.com/indices/sensex    // India
                https://www.investing.com/indices/vn-30    // Vietnam
                https://www.spglobal.com/spdji/en/indices/equity/sp-asx-200/    // Australia
                https://www.spglobal.com/spdji/en/indices/equity/sp-japan-500/    // Japan
                https://www.investing.com/indices/singapore-straits-time    // Singapore
                https://in.investing.com/indices/kosdaq    // Korea
                https://www.investing.com/indices/s-p-citic300    // China

            1. 可以看到，US S&P 500历年都有极高的增长速度，风险溢价推高股价增长要求。
               MSFT 2023年 Revenue增长 不足以支撑 X%，虽然其它Flag也不佳。
               either 股民持有乐观预期并推高P/E，或者有股价下跌预期。织梦、开疆、内务，都是维持股价的方向。
               Cloud部门 Revenue增长 历来强劲，但按年趋势，增长率可能跌破14%。headroom更小，如果需要考虑平摊其它部门较低的增长率。

        8. 本文不构成投资建议。

    n. related materials
        1. Jacob：从Office的营收看，没有人比微软更懂企业客户 - 雅格布
           https://mp.weixin.qq.com/s/A6yNSWAzS2ROGZxV-LwnBA

        2. 最近的一些启发与感悟 - 雅格布
           https://mp.weixin.qq.com/s/EImYuoHMqw3DW7WNSauLQA
            1. 不要陷入优化细节体验的陶醉感中，一个行业一个产品如果常常需要优化细节体验，这就证明解决方案已经成熟，后续不存在大机会了，或者说增长停滞，陷入同质化的竞争。长期在这种环境里面久了，你会发现自己很喜欢对一些雕花的小事情过度关注，实际上产出的社会价值非常少，慢慢你会把细节体验作为比选项加入你的决策系统中，以致于当有大机会来临的时候，你会嫌弃它细节不够好而错过。
            
            2. 如果观察一个企业，我习惯先看收入占比区分主营业务，再看收入毛利率和营业利润率，看看是否具备行业和供应链上的一些优势，其次再看看主营业务的所处领域的市场份额，然后再看看近十年收入、盈利水平和市场份额的变化情况和变化原因，最后再思考收入的持续性问题。
            
            3. 对于企业来说，什么是最关键的因素？不是收入暴涨也不是利润虚高，而是具备一定程度的垄断能力，投资企业的关键就在于想方设法通过各种渠道信息数据去查证这家企业是否具备垄断性，如果具备那就找到了好的标的。

        3. Jacob：避免竞争的最佳案例，论张忠谋的一剑封喉（上）（下）
           https://mp.weixin.qq.com/s?__biz=MzI1MjE4MDgxMg==&mid=2650796485&idx=1&sn=e0819b88cba45f702585cd615ff76013
           https://mp.weixin.qq.com/s?__biz=MzI1MjE4MDgxMg==&mid=2650796489&idx=1&sn=aca9500f5cdaad6c316a1c84ba004bc9
            1. 本文尝试回答三个问题：半导体行业的底层运作机制是什么？台积电有什么结构性优势？为什么张忠谋能在这里面胜出？
                1. 半导体行业的商业模式，属于重资本、中周期的行业，在前期出货阶段，良品率较低、单位成本却很高，所以在相同工艺水平之下，谁能更快地占领市场，谁就可以利用规模优势降低成本，反哺工艺水平，这也让竞争者望而生畏。

                    再加上制造业本身就具备十分明显的学习曲线特征，也就是随着经验的增加，效率提高和成本减少是必然的，随着规模的不断增加，学习曲线提升的速度也就越来越快。

                    如果要在行业里面做出名堂，确保良品率的同时保证有竞争力的价格是关键，这有助于逐步提升市场份额，份额一旦被拉开，竞争格局才有利于形成垄断，加上学习曲线的加持，相同良品率的产品又能再进一步降低价格，形成良性循环。

        4. Jacob：论企业的股价由什么决定？
           https://mp.weixin.qq.com/s/pzUqH4BJ5bs0mXSkznxBsg
            1. 企业的股价由2个因素决定：较高确定性的盈利增长、偏低的市盈率水平。
                1. 如果你的判断正确，一段时期内，EPS会向着东北方向走出一条漂亮的曲线，而股价会像一只极度情绪化的疯狗一样上蹿下跳，你只需要在高估的时候放手卖出即可，卖出不是不看好，而是静待疯狗回到合理区间，赚一波情绪的钱。
            2. -企业的创造的利润是真的吗？
                -企业创造利润的能力持续吗？
                -企业维持创造利润的能力，还需要额外的资本投入吗？
                利润真实性的问题好解决，换句话说，就是不断拷问自己：
                -企业的产品/服务，在未来几年里能否继续被客户所需要？
                -这些产品/服务的盈利能力，是否需要企业不断投入大量新资本去维持？

        5. 在赚钱的路上，我自己踩过的坑 -  雅格布
           https://mp.weixin.qq.com/s/yII_AMVeU42aEL21vZMl4w
            1. 第一个需要注意的地方，就是在验证产品的环节，最重要的是验证需求和市场的契合程度（PMF）。你可以从草根的调研方法去获知，也可以通过全面的供求关系来得知，无论是用什么方法，你得确定这个被证实了，才能继续去做其他事，否则都是徒劳。
                1. https://ahrefs.com/blog/zh/product-market-fit/
            2. 另外一个需要注意的地方，就是要以终为始，你需要用来赚钱的方式，要在开始做的时候就确定下来，尽管它以后会改变。
                1. 一个好的业务，用户基于你解决了他的某个问题而选择留存下来，他所希望的，只会是当这个问题的量级变得更大时，或者这个问题衍生出来的高关联的问题，你仍能更好地帮助他去解决，所以你的正确发展路径必然是围绕着核心路线在走，如果你不在核心解决方案上收费，请问用户为什么要给你付费？

        6. Jacob：沉迷推荐算法，犹如陷入死亡螺旋 - 雅格布
           https://mp.weixin.qq.com/s/6vtSRYzbE-NDlUI5kHUyOw
            1. 高质量的信息，不仅会引导你走向正确和真实，还会在一些关键环节的描述上，让人觉得特别有实操性，获知后能让人豁然开朗，因为心有成竹，对后面的生活也充满了信心。最重要的是，提供高质量信息的人，也会传递正向的价值观，在思维模式层面一通百通。
                1. 高质量的信息是稀缺的，是奢侈的，可遇不可求，如果有机会碰到，我一般会不断溯源，溯的是作者的源，因为信息都是跟着人走的，这个人人又是跟着另外一个你认可的人走的，有一种像偶然发现明星聚会，从花园后门翻墙进来看热闹的感觉。
            2. 相反，低质量的信息除了能把你带进沟里，还能让你上瘾，因为低质量的信息一般易于传播，经常是一些事实逻辑层面的描述压缩，掐头去尾，让人管中窥豹。如果你看完一条信息，没有觉得有启发，相反它还能让你变得义愤填膺，那就实属低质量信息无疑了。
                1. 推荐算法的出现，彻底打破了这一切，如果你原本就有很多高质量信源，推荐算法可能能帮助你找到更优质、更值得关注的人，但这还是不够直接，不够个性化，毕竟探索的过程也是学习筛选的过程。
                2. 但如果你本来就是个容易受影响的人，系统默认给新用户推的都是些易于传播，流量大的爽文，那就彻底跌入了万劫不复的时间黑洞了。

        7. Jacob：其实，谷歌还是在靠搜索撑着 - 雅格布
           https://mp.weixin.qq.com/s/CtIcFavmGNBAd-IVs4AsOw

        8. Jacob：特斯拉的车卖不过比亚迪？我有另外一个角度 - 雅格布
           https://mp.weixin.qq.com/s/xZA5GraNn_VQVaR7CMQeCA
            1. regulatory credits的出售业务

        9. 最近的一些交易思考 - 雅格布
           https://mp.weixin.qq.com/s/QlVDmI2hd5WSWEXNIrLEcQ
            1. 外资和我们的角度不一样，在全球视野寻求投资标的的时候，除了标的的估值、周期、趋势这些要关注之外，还会关注汇兑风险和各国经济周期。

        10. 那些交易里经常混淆的概念 - 雅格布
            https://mp.weixin.qq.com/s/jyPCTUp6BxWBQU-FjWvlBA

        11. 20条积累财富的建议，通透且真实 - 《纳瓦尔宝典》 - 雅格布 
            https://mp.weixin.qq.com/s/MN0bT_ByCQzaz-6VDB1Z8g
            0. Very good.
            1. 财富，不是金钱地位，是指在你睡觉时仍能为你赚钱的资产。财富与努力工作没有必然联系。依靠出租时间不可能致富，你必须拥有股权。无论是财富、人际关系，还是知识，都来自复利。
            2. 获得财富的一个途径，就是为社会提供其有需要但无从获得的东西，并实现规模化，而提供这些东西对你来说又是轻松自然的事情，在你的技术和能力范围内。专长指的是无法通过培训获得的知识，如果社会可以培训你，也可以培训他人来取代你，要有所专长，就要追求真正的兴趣和热爱，而不是盲目追求热点。累积专长的过程，对你而言就像玩耍，对他人来说则很吃力。人生大部分时间都在寻找，寻找那些最需要你的人，寻找那些最需要你的事。
            3. 要想获得财富，就必须充分利用杠杆效应，给自己的专长加杠杆，商业杠杆来自资本、劳动力和复制边际成本为零的产品。人生的一大目标应该是掌控自己的时间，理想的工作是利用了杠杆效应的工作。投入和产出之所以会脱节，是因为工具和杠杆的存在，一个职业的创造性越高，其投入和产出的不匹配就越高。
            4. 最好的工作与学位无关，最好的工作是终身学习者在自由市场中的创造性表达。致富最重要的技能是成为终身学习者，以前赚钱的模式是读4年大学，拿到学位在专业领域干上30年。现在不一样了，必须在9个月内掌握一门新专业，而这门专业4年后就过时了，但在专业存在的这3年里，你可以变得非常富有。
            5. 于我而言，我希望单纯靠判断力来获得报酬，而不是靠劳作，我想让机器人、资本或者计算机完成实际工作，而我只靠判断力赚钱。真正聪明的人是思路清晰的思考者。事实上，留出空闲时间非常重要，如果每一天都被各种会议室占满，都是忙忙碌碌的，你就无法进行思考。几乎所有的偏见，都是为了帮助人们在信息不完整的情况下迅速做出判断，对于重要的决策，要抛开记忆和身份，专注于问题本身。
            6. 很多时候，我们会沉迷于对外物的“欲望”，我对外部事物会带给我幸福和快乐的执念其实是一种痴念，从根本上来看，从自身以外的事物中寻求幸福，本身就是缘木求鱼。年轻的时候有时间、有健康，但没钱。中年的时候有钱、有健康，但没时间。老年的时候有钱、有时间，但没了健康。人生最大的赢家就是同时拥有健康、时间和钱，乍一看就是现在。成功并不一定会带来幸福，成功源于对现状的不满，对现状的改造，但幸福就是满足现状，某种程度上，两者是对立，只能选其一。


64. 谷歌流量整形技术Carousel解读 - 蔡伸 - sigcomm17
    https://mp.weixin.qq.com/s/5Z1IFK6S0aSkDxvH0OH2Mw
    1. 流量整形 (traffic shaping)
        1. 于是发送端需要通过一种主动调整流量输出速率的措施，其作用是限制流量与突发，使报文以比较均匀的速率向外发送
        2. 当前，流量整形通常通过 device output queue（设备发送队列）实现
            1. 最快发送速率就是队列的流速(drain rate)
            2. 传输中的最大数据量（inflight data）由接收窗口大小或队列长度决定
        3. Leaky bucket queue - the basic technique
        4. HTB和FQ/pacing (Hierarchical Token Bucket, flow pacing)
            1. HTB（分层令牌桶技术）
                1. 将leaky bucket串成tree，叶节点token溢出后，留存在parent节点。这解决了原来burst耗尽的问题。
            2. FQ/pacing（公平队列和节奏控制）
                1. Hierarchical leaky bucket. 然后通过使用：数据包大小/pacing rate，为数据包分配发送时间
        5. Carousel设计
            1. 整体设计思想
                1. 与更高级的拥塞控制机制（如TCP）兼容工作。
                2. 正确进行数据包节奏控制（pacing）：避免突发和不必要的延迟。
                3. 提供反压力并避免数据包丢失：由于速率限制而延迟数据包应该迅速导致终端应用程序变慢。否则，应用程序生成的每个额外数据包都需要在整形器中进行缓冲或丢弃，浪费内存和CPU资源来排队或重新生成数据包。此外，基于丢包的拥塞控制算法常常通过显著降低相应流的速率来对数据包丢失做出反应，这需要更长的时间才能恢复到原始带宽。
                4. 避免头部阻塞：整形属于一个流量聚合的数据包不应该延迟其他聚合的数据包。
                5. 高效使用CPU和内存资源。
            2. 三个技术
                1. 单队列整形（single queue shaping）：通过依赖一个单一队列来进行数据包整形，可以减轻多队列系统（使用令牌桶）的低效和开销，因为这些系统需要每个速率限制一个队列。
                    1. 时间戳, Timing Wheel 减少消耗以及队列
                2. 延迟完成（deferred completions）：发送方必须限制每个流的在途数据包数量，可使用现有机制（如TSQ或拥塞窗口）。
                    1. 只有在数据包离开网卡、进入网络后才给transport程序发送completion。而不是driver发送后就通知completion
                    2. Software NIC
                3. 单核独立整形器（silos of one shaper per-core)：将单队列整形器隔离到一个核心中可以减轻由于锁定和同步导致的CPU效率低下的问题。
```