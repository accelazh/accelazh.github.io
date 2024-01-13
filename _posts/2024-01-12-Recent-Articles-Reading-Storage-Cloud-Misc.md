---
layout: post
title: "Recent Articles Reading: Storage, Cloud"
tagline : "Recent Articles Reading: Storage, Cloud"
description: "Recent Articles Reading: Storage, Cloud"
category: "storage"
tags: [storage, paper, cloud]
---
{% include JB/setup %}

Misc articles.

```
1. AWS Fault Isolation Boundaries - AWS Whitepaper
   https://docs.aws.amazon.com/pdfs/whitepapers/latest/aws-fault-isolation-boundaries/aws-fault-isolation-boundaries.pdf#abstract-and-introduction
    1. AZ, Region
    2. AWS Local Zone - Edge location deployment
    3. AWS Outpost - On-premises deployment
    4. Static stability - interesting
    	1. AWS data planes statically-stable to an impairment in the control plane
    5. Global services
    	1. useful listing

2. 云原生数据库 GaiaDB 的核心技术演进和解析 - 百度智能云
   https://zhuanlan.zhihu.com/p/661835478
    1. "对 I/O 的时延的要求进一步提升，GaiaDB 舍弃 Raft 协议，采用 Quorum 读写方案"
    2. 网络优化
        1. "采取了 BackupRequest 机制"
        2. "GaiaDB 引入了百度内部研发的智能网络"
            1. "智能网络能够根据硬件设备的性能和网络状态，自动选择最优的网络协议和参数"
            2. "用户态网卡驱动程序"
    3. 存储优化
        1. "提供统一的资源均衡策略"
    4. 多地多活技术
        1. "数据库多 AZ 的部署 .. 物理同步协议 .. AZ 热活"
        2. "采用了就近访问的策略"
        3. "在多地域部署时，GaiaDB 的自研同步组件 Replicator 通过同步 Redo 流来支持 DDL 操作等高级功能"

3. LLM大模型推理部署优化技术综述 - 上天界医神
   https://zhuanlan.zhihu.com/p/655557420
    1. good. very useful
    2. Highlights
        1. 计算优化
            1. 算子融合
            2. 高性能算子优化
        2. 显存优化
            1. kv cache
            2. pageattention
        3. 分布式优化
            1. 模型并行和流水型并行
        4. 模型低精度加速
            1. 这部分内容比较多，且属于高速发展期
        5. 服务化scheduler
            1. continuous batching

4. MySQL热点优化实践 - 贺大伟
    1. useful summary
    2. Highlights
        1. 事务组提交大概可以提升几十倍的性能
        2. 热点优化-OpC: 把对同一行Update的并发事务的算子进行聚合
    3. 高灵敏的热点识别算法
       https://zhuanlan.zhihu.com/p/612903909

5. 偏向引用计数(Biased Reference Counting) - sean
   https://zhuanlan.zhihu.com/p/668786189
6. 从一致性 hash 到 ceph crush - 暗淡了乌云
   https://zhuanlan.zhihu.com/p/60963885
7. 基于B-tree以及Shadow paging实现存储系统的快照功能 - sean
   https://zhuanlan.zhihu.com/p/666411114
8. 什么是数据库的“缓存池”？（万字长文，绝对干货） - 程序员小灰
   https://zhuanlan.zhihu.com/p/348100477
16. 超越POSIX：一个时代的终结？ -  Andy730
    https://mp.weixin.qq.com/s/D1mF4tJdtAubr9Ykh49fYQ
18. 记一次深入内核的数据库高并发性能优化实践 - DolphinDB
    https://zhuanlan.zhihu.com/p/669173594
22. 分布式和集中式存储的讨论 - tao.cheng
    https://zhuanlan.zhihu.com/p/505122541
23. 值得关注的开源分布式存储系统 - tao.cheng
    https://zhuanlan.zhihu.com/p/490969861
24. Ceph 数据复制算法和Raft数据一致性算法对比分析 - tao.cheng
    https://zhuanlan.z


9. 开源分布式存储系统PureFlash介绍
   https://mp.weixin.qq.com/s/Ssh5IjmFqkVeJ0Sj1hzOsg
    1. Highlights
        1. storage challenges
            1. CXL, pmem, 内存池化, RDMA, EC
        2. PureFlash - SAN
            1. 极简
            2. 硬件加速设备
            3. BlockDirectly架构
                1. 直接管理设备，不适用文件或对象存储为中间格式
                2. 提供虚拟化、池化、快照、加密等服务
                3. 最简化关键路径
                    1. 控制路径与IO路径分离, No calculation in IO path
                    2. No copy
                    3. No cache
                    4. No journal
            4. 元数据
                1. MariaDB Galera
    2. NetBRIC S5：“另类”设计的全闪存阵列
       https://mp.weixin.qq.com/s?__biz=MzAwODExNjI3NA==&mid=204765794&idx=1&sn=c210c414522e309ea4c30aaf0d28ed93
        1. NetBRIC S5却严重淡化了CPU，而是大量使用FPGA
        2. 利用PCIe MultiCast（多播）来将CPU从数据流中释放出来
        3. NIC <-> SWITCH+DRAM <-> FLASH
        4. 整个系统的IO路径完全由硬件实现

10. 中国有哪些AI芯片初创公司？ - 吃果冻不吐果冻皮
    https://www.zhihu.com/question/263418616/answer/3297463887
    1. useful summary

11. 联手体系结构专业委员会：“分离式内存”术语发布 | CCF术语快线 - disaggregated memory
    https://zhuanlan.zhihu.com/p/488712338
    1. CPU和DRAM资源可以像储存设备一样，实现低开销的池化管理

12. CubeFS EC的实现 - tao.chang
    https://zhuanlan.zhihu.com/p/635614999
    https://www.cubefs.io/docs/master/design/blobstore.html
    1. Blob -> stripe into multiple blocks -> Each block is called a shard -> One shard goes to one chunk
    2. EC works on chunk level. 6 chunks + 3 chunks form an EC group as example.
    3. Inline EC write to N shards
    4. Optimizing EC for Small File
        1. "Our optimization solution is to write smaller files to fewer data blocks as much as possible to reduce network requests during reading"
            1. 128K data originally generates 4*32K data + 4*32K parity.
               In optimized way, it generates 1*128K data + 4*128K parity
    5. Efficient Garbage Collection
        1. "First, delete the index entry of the data in the LSM."
        2. "Then, use the system call fallocate to create a "hole" of the corresponding size at the specified position in the Chunk File."
    6. Append Writing
        1. Overwriting is always written in Append mode
    7. Block EC/Stripe EC Strategy
        1. Block EC
            1. Distribute user data fixed length blocks. EC works cross blocks
        2. Stripe EC
            1. A piece of user data is itself sliced into N+M blocks for EC
        3. "CubeFS uses the simpler and more universal Stripe EC method."

13. MySQL运行在Docker容器中会损失多少性能 -  Rainux
    https://mp.weixin.qq.com/s/uvbe7b0PU4d3P7Z1gCQNgw
    1. "单表百万级以下时，非容器和容器的性能差异并不多。单表千万级时，容器 MySQL 大概会损耗 10% ~ 20%的性能。"

14. 数据密集型HPC产业趋势分析 - 智能计算芯世界
    https://mp.weixin.qq.com/s/nit9HIe0hNjAho2JLLLspQ
    1. HPC vs HPDA, AI
    2. HPDA - High Performance Data Analytics

15. 开源全闪存存储系统：Intel DAOS架构介绍 - tao.chang
    1. DAOS可以是完全实现在用户态的高性能分布式存储系统
        1. By OS kernel：直接使用PMDK，SPDK等用户态库绕过操作系统直接访问SCM和NVME SSD等高性能设备。
        2. RDMA：实现用户空间数据端到端的数据拷贝。
        3. UTL（user level thread）用户态线程或者称为协程的概念。
    2. Highlights
        1. 数据分布Placement
            1. Jump consistent hash
        2. 副本一致性
            1. 改进的两阶段提交算法DTX（DAOS Two Phase Commit）
        3. 故障检测和数据修复
            1. 分层的故障域（Hierarchical Fault Domains）
            2. gossip-based的称为SWIM的协议来完成节点的故障检测
                1. SWIM: scalable weakly-consistent infection-style process group membership protocol    [2002, 227 refs]
                    0. Referenced in
                        1. Service fabric: a distributed platform for building microservices in the cloud    [2018, 58 refs]
                            1. "Without the arbitrators, distributed membership will have inconsistencies (e.g., gossip, SWIM/Serf [32]), or one needs a heavyweight central group (e.g., Zookeeper [45], Chubby [24]) which has its own issues."
                    1. Heartbeat based membership has scalability limitation. SWIM solution imposes constant overhead no matter of group size. Effective to WAN / VPN  netwroking.
                    2. highlights
                        1. Scalability: Both the expected time to first detection of each process failure, and the expected message load per member, do not vary with group size.
                            1. Challenges
                                1. limitations of traditional heartbeat-based protocols, which struggle to scale in groups with more than a few dozen processes due to increased false failure detections and message load
                            2. SWIM solutions
                                1. SWIM uses a non-heartbeat based strategy, specifically a random peer-to-peer probing of processes
                                    1. See Figure 1
                                2. Membership updates are propagated efficiently and reliably using an infection-style (epidemic-style) mechanism
                                    1. SWIM's design separates the failure detection and membership update dissemination components
                                    2. dissemination is gossip based. Piggybacked.
                                4. SWIM introduces a suspicion mechanism with virtual incarnation numbers to reduce the frequency of false positives, trading off some failure detection time to improve accuracy
                                    1. Suspicion mechanism: a temporary non-responsive node is marked as Suspected. Suspect state is propagated to other nodes. After say 5min, if the suspected node won't respond to ping, it's marked as faulty.
                                    2. Figure 4, Suspicion mechanism vs 10% packet loss rate
                                    3.  Effective to WAN / VPN  netwroking, e.g. the replica groups in distributed hash table (DHT) systems such as Chord, Pastry, Opus [15]

        4. 本地存储VOS - versioning Object Store
            1. 小块IO在SCM，大块IO直接落盘NVMe SSD上。同时支持后台小块IO的合并成大块IO并迁移到NVMe SSD上
            2. 基于日志型的多版本机制。所有的写操作都带有epoch，并且都是追加写操作。方便实现事务机制，snapshot，数据恢复等
            3. 基于SCM的multi-version，concurrent Key-Value Store
                1. 在对比了红黑树和B+树的优缺点后，VOS使用了B+树做为存储结构
            4. 对象元数据保存了多版本的信息，通过R-Tree实现空间查找
            5. PMDK, SPKD技术

17. 分布式目录树管理 - 爱分享的码农
    https://zhuanlan.zhihu.com/p/501098927
    1. Facebook Tectonic针对文件目录树结构做了如下KV转换
        1. tectonic将子目录的inode信息与父目录放到了同一个shard里
    2. InfiniFS目录树管理
        1. 为了加快lookup的检索效率，InfiniFS采用了与LocoFS类似的处理思路，通过并行检索路径上的每个中间节点来加快目标文件的查找效率。但是与LocoFS采用全路径的处理方式不同，InfiniFS采用的是路径名推测(Speculative Path)的执行方式，即通过相应的hash函数推测出每个中间路径的key值，然后基于这些key值去做并行的get检索
    3. CephFS目录树管理
        1. CephFS则基于动态子树的方式来对目录树结构做分布式管理(以子树为粒度)
        2. 这里需要注意的是CephFS的负载均衡器并没有采用全局的方式进行设计，而是在每个MDS内部独立维护一套，MDS之间需要维持心跳逻辑来交换彼此的负载信息，以便于后续做迁移方面的决策。这种部署方式虽然满足了去中心化的使用需求，但是不同的MDS之间也很容易造成决策冲突，进而引发相关目录的频繁迁移，对上层业务使用造成一定的冲击影响。


19. 高性能计算的存储特点和解决思路 - tao.cheng
    https://zhuanlan.zhihu.com/p/575189905
    1. interesting 

20. 对象存储的发展脉络和特点 - tao.cheng
    https://zhuanlan.zhihu.com/p/572660698
    1. interesting

21. 分布式系统中的 IO fencing问题 - tao.cheng
    https://zhuanlan.zhihu.com/p/543168561
    1. my methods
        1. old primary kill itself immediately, while new primary wait a grace period before proceeding
        2. or, new primary take the lock or clear the old fencing token at the resource nodes
        3. or, eventual consistency, sync based, and make deletion slow enough to give the old primary enough time to exit race condition 

22. 聊聊日志即数据库 - CatKang
    https://zhuanlan.zhihu.com/p/669765317
    1. good

23. A Tale of Two Architectures — Engineering for the 99.999% versus the 0.001%
    https://volumes.blog/2013/12/30/a-tale-of-two-architectures-engineering-for-the-99-999-versus-the-0-001/
    1. interesting. useful.

------

1. RocketMQ 中冷热分离的随机索引模块详解 - 阿里云云栖号
   https://zhuanlan.zhihu.com/p/673200413?utm_id=0
2. 无需专有硬件 XDcache 大幅提升文件写性能 - XSKY
   https://mp.weixin.qq.com/s/u1uCynsh2qbSq14QumwJhg
3. AI 集群基础设施 NVMe SSD 详解（万字长文） - 吃果冻不吐果冻皮
   https://zhuanlan.zhihu.com/p/672098336?utm_id=0
4. OLAP技术的选择，进化和思考 - DataFunTalk
   https://zhuanlan.zhihu.com/p/672079607?utm_id=0
6. Linux实时补丁终于迎来最终结尾 - Hello小崔
   https://zhuanlan.zhihu.com/p/672773951?utm_id=0
7. 基于 CXL 的大内存池化 - Macan
   https://zhuanlan.zhihu.com/p/538689902
8. AI芯片设计--能效分析框架 - Damon的文章
   https://zhuanlan.zhihu.com/p/672951427
9. AMD CDNA 3计算架构 - AI 产品经理
   https://zhuanlan.zhihu.com/p/672817452
10. SSD入门全攻略——看这篇就够了 - gallopwei
    https://zhuanlan.zhihu.com/p/453516926

5. 下一代开源分布式存储(vs Ceph)系统 - DAOS
   https://zhuanlan.zhihu.com/p/672215338?utm_id=0
    1. Highlights
        1. Key points
            1. 持久化内存SCM，PMEM，SPDK，RDMA
            2. Run-to-Completition
                1. Benchmarks show that one execution stream can create millions of ULTs per second
            3. 数据I/O端到端无内核调用开销
            4. 有趣的I/O复制流 - Client通知主副本有写io，然后主通知两个从副本(到这里都只是控制流)，然后这3个副本通过RDMA直接从Client内存中读取数据
                1. Interesting
                2. read/encode/write process - "DAOS can avoid this expensive process by replicating only the partial write data to the parity server"
                    1. Parity Logging
                        1. PARIX: Speculative Partial Writes in Erasure-Coded Systems
                           https://www.usenix.org/conference/atc17/technical-sessions/presentation/li-huiba
            5 Service crash - captured by gossip-like protocol SWIM
            6. DAOS 数据模型
                1. Array objects, 允许应用程序表示多维数组
   n. related materials
       1. DAOS: A Scale-Out High Performance Storage Stack for Storage Class Memory    [2020, 48 refs]
          https://dlib.hust.edu.vn/bitstream/HUST/19785/3/OER000001255.pdf#page=48

6. 数据库的下一场革命：S3 延迟已降至原先的 10%，云数据库架构该进化了 - 曹伟 InfoQ
   https://mp.weixin.qq.com/s/HJ-D1OSoe2CjAHbQT39vZw 
    1. The article didn't mention S3 Express Zone. Not about the opinions but the article has very good visions on cloud storage future
    2. Key points
        1. "对象存储的价格是最低的，1TB 一个月的存储成本约为 120 元。低定价得益于其软硬件的协同优化。在软件
            层面，采用更激进的 EC 和压缩算法来提高存储密度；而在硬件方面，通过使用高密度盘和专用服务器，进而
            降低服务器、机架及电力的均摊成本。对象存储系统还利用定制的 FPGA 硬件来减轻 CPU 处理网络和数据的
            压力。在资源调度上，对象存储一般会采用大集群的部署方案，这有利于降低碎片率，提高系统的整体水位
            线。得益于其分布式大资源池的设计，对象存储能够支持 10Gb 乃至 100Gb 的访问带宽。此外，对象存储通
            常还具备跨可用区域（AZ）的灾难恢复能力。"
        2. 解法：持久性与延迟的解耦
            1. 持久性、延迟、成本
                1. 延迟、持久性：云盘、NAS
                2. 延迟、成本：实例存储
                3. 持久性、成本：对象存储
            2. My questions
                1. Should non-functional requirements and functional requirements be orthogonal? I.e., an object storage that takes 延迟、持久性.

8. 小红书应对万亿社交网络关系的图存储实践 - 卢亚德
   https://mp.weixin.qq.com/s/lWb-xbLmnCuInVr_2YRHzw
    1. Backed by MySQL, serving in-memory cache. Strong consistency reads/writes are routed back to primary MySQL。
        1. Mostly following Facebook TAO.
        2. Alternatives
            1. Facebook TAO - graph cache + MySQL
            2. Pinterest Zen - graph cache + HBase
            3. ByteDance ByteGraph - graph cache + KV (Abase or ByteKV)
            4. LinkedIn Voldemort - KV store
    2. 满足 2 跳以及 2 跳以上的查询。
        1. 三级嵌套HashTable设计: from_id => REDTaoGraph (HashTable) => edges by type (HashTable) => type_id => AssocType => to_id => REDTaoAssoc (HashTable) => recent edges

9. 卡在政企客户门口的阿里云 -  瑞典马工
   https://mp.weixin.qq.com/s/gPdeaWqFDRe131c78UBkSA
    1. very good.
    2. 门内的国企如何看门外的云厂商 - 思维南人
       https://mp.weixin.qq.com/s/FOdRF3zYxWBNkVxgHvHZrQ
    
    3. A Conversation with Werner Vogels (Amazon CTO)    [2006]
       https://queue.acm.org/detail.cfm?id=1142065
        1. The big architectural change that Amazon went through in the past five years was to move from a two-tier monolith to a fully-distributed, decentralized, services platform serving many different applications
            1. The first and foremost lesson is a meta-lesson: If applied, strict service orientation is an excellent technique to achieve isolation; you come to a level of ownership and control that was not seen before. 
            2. A second lesson is probably that by prohibiting direct database access by clients, you can make scaling and reliability improvements to your service state without involving your clients. 
            3. Another lesson we’ve learned is that it’s not only the technology side that was improved by using services. The development and operational process has greatly benefited from it as well. 
        2. But then there is the second category of large enterprise retail partners, such as Target, Bebe, or Sears Canada, to which we provide a large collection of platform services

9. 年度总结｜存储随笔2023年度最受欢迎文章榜单TOP15 - 古猫先生 存储随笔
   https://mp.weixin.qq.com/s/_ysmszIfQ22YB7pq7qh3qw
    0. very good.
    1. HDD最后的冲刺：大容量硬盘的奋力一搏
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247487899&idx=1&sn=99bb6538888ad63f61d6f1e77d1c819c
        1. HAMR, MAMR
        2. 微软Azure云数据中心工作负载分享：SSD与HDD，何去何从？
           https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247487876&idx=1&sn=04c7c6ce4724a8ff2278c220490c2ed1
        3. HDD与QLC SSD深度对比：功耗与存储密度的终极较量
           https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247487789&idx=1&sn=e2b142215c427cfad40921b9ee059e06
    2. 开啥玩笑？一个SSD硬盘可以使用100多年？
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247487301&idx=1&sn=fb00258c185ccfb94cb63b0e0c6bfc4b
    3. PCIe 6.0/7.0相对PCIe 5.0的变化有哪些？
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247486536&idx=1&sn=1bcee125c6ebccff1ab282a4cb403319
    4. 全景解析SSD IO QoS性能优化
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247486234&idx=1&sn=d759ab116860e2b24f29b97d7f88bd40
    5. 字节跳动ZNS SSD应用案例解析
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247488494&idx=1&sn=3894e2915c1265127e899bd368d65215
        1. Interesting
    6. 存储系统性能优化中IOMMU的作用是什么？
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247486314&idx=1&sn=d928b63724c43e75c5dfb259cc623660
    7. 3D DRAM：突破内存瓶颈的新希望
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247486557&idx=1&sn=aed9ab254fe21c272e5303439bf0dfee
    8. 《存储IO路径》专题：四种IO栈全能大比武
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247486706&idx=1&sn=b77c0e499c5932d2474fe06331f34089
    9. 独家揭秘｜小米14魔改存储芯片多出8GB空间背后的秘诀
       https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247487744&idx=1&sn=288afccf08a40a227a6db115528619d5
    10. CXL崛起：2024启航，2025年开启新时代
        https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247488182&idx=1&sn=699bfa8905fbf0438e9843549c2af9c4
    11. PCIe在狂飙，SAS存储之路还有多远？
        https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247488318&idx=1&sn=13b1281a7609ac1a56f4c63b4f6a2087&
    12. SSD数据在写入NAND之前为何要随机化？
        https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247488448&idx=1&sn=e969b687e71c045b3f22cb17a4e6bb1f
    13. SSD基础架构与NAND IO并发问题探讨
        https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247488520&idx=1&sn=85160549df0b37533ec11ccf691c44c2
    14. 过度加大SSD内部并发何尝不是一种伤害
        https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247488770&idx=1&sn=4414612cfaa7eb7b3852cc96ceb88242
    15. 浅析LDPC软解码对SSD延迟的影响
        https://mp.weixin.qq.com/s?__biz=MzIwNTUxNDgwNg==&mid=2247488674&idx=1&sn=820376c72419aa3eaaeeb2fcebc24a92

10. Danzero+：用掼蛋为例讲解如何处理大规模动作空间的强化学习问题 - 赵鉴
    https://zhuanlan.zhihu.com/p/673715817

11. Proportion integration differentiation - PID
    1. PID Controller Explained
       https://www.youtube.com/watch?v=fv6dLTEvl74
    2. ChatGPT
       https://chat.openai.com/share/72f24f58-79f3-48c5-86b4-84a32670fa6f
    3. PID Balance+Ball | full explanation & tuning
       https://www.youtube.com/watch?v=JFTJ2SS4xyA
        1. P controls by error distance, but you need D to handle remaining velocity/momentum,
           then you need I to make sure ball stops at zero distance rather than elsewhere,
           especially when P is small when distance is small, too small to fight the noise.

12. 2023年存储行业并购交易 - edwu
    https://zhuanlan.zhihu.com/p/676664448
14. 2024年Top 4数据存储趋势 - edwu
    https://zhuanlan.zhihu.com/p/674055673

13. VM大规模在线迁移 - edwu
    https://zhuanlan.zhihu.com/p/660302695
    1. Google VM migration paper. Interesting
    2. Highlights
        1. 源端阶段（Source brownout） -> 停机阶段（Blackout） -> 目标端阶段（Target brownout）
        2. 预复制 vs 后复制
            1. 一小部分工作负载具有足够高的写入速率，导致黑屏时间非常长
            2. 后复制[8]，虚拟机可以在所有脏内存迁移完成之前在目标上恢复。我们使用后台获取机制来继续从源迁移内存内容。如果虚拟机的虚拟CPU尝试访问尚未获取的页面，就会从源请求该页面，直到复制到虚拟机之前，该虚拟CPU将被阻塞。

14. 数据中心的温度管理：为何有些人可能倾向于较高温度 - edwu
    https://zhuanlan.zhihu.com/p/661048105
    1. 观察2: 温度的变异性对LSE率的影响往往比单纯的平均温度更显著且一致。
    2. 令人惊讶的是，这项研究发现随着温度的升高，硬盘故障率呈现出明显下降的趋势，除非温度非常高（超过45℃）。
    3. Many more observations. Interesting

15. 再谈Ceph - edwu
    https://zhuanlan.zhihu.com/p/654271922
    1. 以深信服、华三为例，两家均在前端自研了一套全用户态的基于NVMe的缓存加速层
    2. 其他方向
        1. RBD客户端缓存，如Intel贡献的基于客户侧PMEM/NVMe的缓存加速；
        2. PG锁的优化；
        3. 基于Open-Channel SSD的优化；
        4. 基于NVDIMM的优化；
        5. 基于F2FS-split的优化；
        6. 基于各种优化Rocksdb存取元数据的优化；
        7. 基于机器学习动态调整配置的优化；

16. 为什么现在的LLM都是Decoder only的架构？ - Sam多吃青菜
    https://www.zhihu.com/question/588325646/answer/3357252612
    1. good
```