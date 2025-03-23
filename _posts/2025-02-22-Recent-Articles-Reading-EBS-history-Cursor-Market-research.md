---
layout: post
title: "Recent Articles Reading: EBS history, Cursor, Market research"
tagline : "Recent Articles Reading: EBS history, Cursor, Market research"
description: "Recent Articles Reading: EBS history, Cursor, Market research"
category: "Paper Reading"
tags: [storage, paper, cloud, AI]
---
{% include JB/setup %}

```
1. Run CUDA on other GPUs not from NVIDIA
    1. Use CUDA without an NVIDIA GPU? [duplicate]
       https://stackoverflow.com/questions/68470042/use-cuda-without-an-nvidia-gpu
    2. Can I use CUDA with a non-NVIDIA GPU? [duplicate]
       https://stackoverflow.com/questions/55320552/can-i-use-cuda-with-a-non-nvidia-gpu
    3. 初创公司硬刚英伟达：在AMD卡上模拟CUDA，原版程序直接编译运行
       https://zhuanlan.zhihu.com/p/709105635
    4. HackerNews: Run CUDA, unmodified, on AMD GPUs (scale-lang.com)
       https://news.ycombinator.com/item?id=40970560
    5. SCALE is a GPGPU programming toolkit that allows CUDA applications to be natively compiled for AMD GPUs
       https://docs.scale-lang.com/
    
    6. summary
        1. 通常XPU需要提供配套的编译器和基础库。Nvida GPU提供的是nvcc和CUDA。新GPU卡应该也能有它的配套编译器和基础库。
        
        2. 另一种思路是将CUDA重新编译到新GPU卡上。nvcc是基于LLVM开发的，LLVM可以改后端生成不同的代码。有人干过将CUDA适配到AMD GPU的工作。 Run CUDA, unmodified, on AMD GPUs: https://news.ycombinator.com/item?id=40970560

        3. 第三种选择是让新GPU卡放弃支持CUDA，转而支持来源框架，例如OpenCL、OpenACC。例如看AMD GPU是怎么做的。

        4. 第四种方法取巧，将CUDA的二进制码转译到新GPU执行。这样新GPU就可以支持CUDA了。不过有法律风险，这种方法被Nvida禁了：https://m.caixin.com/m/2024-03-07/102172775.html

2. Book: Irreplaceable - The Art of Standing Out in the Age of Artificial Intelligence - Pascal Bornet Wiley, 2024
   https://www.getabstract.com/en/summary/irreplaceable/49474
    1. 采用五项关键原则，确保您的业务"AI-ready"。
        1. "Efficiency over effort" — Don't push people to work harder and longer. Find ways for them to work smarter instead, using the time-saving benefits of AI to create space for more impactful human activities. 
           "效率优先于努力"——不要强迫人们更努力、更长时间地工作。想办法让他们更聪明地工作，利用人工智能的节省时间的好处，为更有意义的人类活动创造空间。
        
        2 . "Value over volume" — It's become relatively easy to mass-produce goods in large quantities inexpensively using AI tools. Stand out from your competition by focusing on creating higher-value goods and services. 
           "价值优先于数量"——使用人工智能工具，以相对低廉的成本大量生产商品已经变得相对容易。通过专注于创造更高价值的产品和服务，在竞争中脱颖而出。

        3 . "Collaboration over control" — Don't be afraid to surrender control sometimes, automating simple decision-making tasks, for example. 
            "合作优先于控制"——不要害怕有时放弃控制，例如自动化简单的决策任务。

        4 . "Balance over burnout" — It's time to stop glamorizing hustle culture and overworking. Take advantage of the fact that AI can perform some of your work for you, leaving you with free time to engage in self-care activities.
            "平衡优先于过度劳累"——是时候停止美化忙碌文化和过度工作了。利用人工智能可以为你完成一些工作的事实，让你有空闲时间从事自我保健活动。

        5. "Reflection over rush" — Rather than use AI in a frenzied, reckless manner (for example, blasting clients with thousands of unsolicited emails), aspire to take a more thoughtful, ethical, and intentional approach.

3. 持续重塑：AWS块存储的简史 - 常华Andy
   https://mp.weixin.qq.com/s/85sfZCQ9S42_gZzg5YCzTw
    1. Shared by Marc Olson who worked in EBS for over 10 years.
    2. Good. Key takeaways
        1. Queuing theory. Remove excessive queues in the system.
            1. "吵闹的邻居" "noisy neighbor" problem also happens in queues.
        2. 如果无法衡量，就无法管理
        3. Nitro card offload is a great success. It moves VPC network processing from Xen dom0 to dedicated hardware pipeline
        4. Onboard old servers to SSD: simply glue SSD to server panel that has free space

4. 从PB到EB：MinIO对象存储引领AI数据基础设施的未来 - 常华Andy
   https://mp.weixin.qq.com/s/vhyQqGgx90IlLGYyRUY6bw
    1. Highlights
        1. 元数据与数据整合存储：MinIO将元数据和数据存储在一起，且采用原子提交技术，避免独立元数据数据库导致的性能瓶颈，大幅提升响应速度。
            1. 
    n. Related materials
        1. Ceph vs MinIO
            1. https://www.reddit.com/r/kubernetes/comments/lvr8po/looking_for_thoughts_on_minio_vs_ceph/
            2. https://github.com/minio/minio/discussions/11390
            3. https://news.ycombinator.com/item?id=28131140
            4. https://news.ycombinator.com/item?id=32498332
            5. https://erfansahaf.medium.com/syncing-minio-with-ceph-object-storage-67a09fb5d01
        2. Does MinIO use local filesystem like Ceph
            1. "Use XFS-Formatting for Drives"
               https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html
               https://min.io/docs/minio/linux/operations/checklists/hardware.html
               https://www.reddit.com/r/minio/comments/oqxyic/need_advice_about_best_practices_zfs_pool_or_xfs/

5. 聊聊提升CXL内存性能的一种新思路 - 知返
   https://zhuanlan.zhihu.com/p/827253890
    1. 目前CXL Type-3内存扩展设备算是发展的比较快的方向，三星、海力士包括国内的澜起科技都推出了CXL内存扩展卡
    2. CXL接口接内存，相比传统的DDR接口（大家攒机的时候都买过内存条），有何优势呢？
        1. 串口的CXL相对并口的DDR有更高的面效比
        2. 实现了内存设备和CPU本身的解耦。这样可以允许我们在不更换CPU的情况下兼容多种内存设备
        3. 便于实现内存资源的池化
    3. 那么代价呢？
        1. 而CXL内存与之相比则有着更高的访问延迟
    4. NeoMem: 面向CXL原生的内存分层系统
        1. 把热页分析做成一个设备端的硬件功能？

    n. Related materials
        1. 微软：AI存储，SSD or HDD ? -  王知鱼
           https://mp.weixin.qq.com/s/4SqCRqiYFf92UHPOQqaHiA
            1. Interesting

        2. 云规模存储的颠覆性创新：微软探索新型存储技术 - Andy730
           https://mp.weixin.qq.com/s/Qt-2V_zJ3a3GCPGU_WcFgQ
            1. 磁介质的局限性
                1. 硬盘：虽然硬盘技术已通过增加盘片、氦气填充、叠瓦式磁记录（SMR）等方式提升容量，但容量提升速度放缓，接近了100TB的极限。更严重的是，容量增大带来的IOPS瓶颈，使得硬盘在高并发和低延迟需求的场景中劣势明显。  
                2. 闪存：闪存依赖工艺尺寸的缩减和堆叠层数的增加来提升密度（例如从SLC到MLC、TLC和QLC的多层单元技术）。然而，随着工艺进入纳米级，量子效应和电荷干扰等物理限制逐渐显现，密度增长已经低于预期，同时导致单元寿命缩短。
                3. 磁带：虽然磁带具有较高的初始存储密度，但其存在寿命有限、操作不便、访问速度慢的缺陷，特别是当数据归档规模庞大时，磁带的维护和管理成本抵消了其容量带来的部分成本优势。
            2. 微软的Pelican项目是一项基于HDD的归档存储优化尝试
            3. 微软的Silica项目则探索玻璃存储技术
        
        3. 几种开源存储系统概览与最新动态 - Andy730
           https://mp.weixin.qq.com/s/DC-LC29wOpn4wM-fkOQE_w
            1. Good. Summarized the particular 劣势 at Luster, TrueNAS, Gluster, BeeGFS, Ceph, OpenStack Swift, DAOS, MinIO, OpenZFS, HDFS
            2. 小文件处理、密集元数据操作的劣势出现在很多产品中

        4. Google Cloud双区域存储
           https://mp.weixin.qq.com/s/Zp-w83Wj5vC4A3wfqWpINg
            1. 恢复点目标（RPO）：提供两种选项：
                默认复制：99.9%的新写入对象提供一个小时的RPO目标，100%的新写入对象提供12小时的RPO目标。
                快速复制：提供15分钟的RPO，确保100%的新写入对象在15分钟内复制到双区域中。

        5. 高性能数据中心存储：基于DPU的解决方案（演讲） -  Andy730
           https://mp.weixin.qq.com/s/Svz5Pzp9-chxSSbS4Fq9nQ
            1. 为了应对这些挑战，Supermicro和NVIDIA合作开发了一种基于DPU的高性能数据中心存储解决方案，该方案将NVIDIA BlueField DPU集成到Supermicro的Gen5 NVMe JBOF中

        6. 深入探秘全球最大AI超级集群xAI Colossus - Andy730
           https://mp.weixin.qq.com/s/RyXgCeELa9iN-rEcx1WBdQ
            1. Colossus目前部署了10万个NVIDIA Hopper GPU，并计划扩展至20万个，其中包括5万个H100和5万个H200。所有GPU都集成在NVIDIA HGX H100平台上，每个平台包含8个GPU。

6. Cursor: Inference Characteristics of Llama-2 - Aman
   https://www.cursor.com/blog/llama-inference#a-primer-in-transformer-math
    1. Very good article. The main idea is model shape => FLOPS/Memory you need => Fit to A100 portfolio => compute/memory bound => prompt process vs token generation => compare cloud prices baseline.
    2.  "A Primer in Transformer Math"
        1. FLOPS per token=140⋅10^9 FLOPs
           Memory bandwidth / token =140 GB/s+320⋅N⋅B KB/s
        2. "So for our largest sequence of 8192, attention still only occupies 10.5 10.5 GFLOPs of the full 140 140 GFLOPs. It's small enough that we neglect it for simplicity."
        3. The memory path for generating tokens through a transformer
    3. Further improve price/latency/throughput
        1. Quantization, MoE, Speculative Sampling, prefilling, dedicated node for generating tokens.
    4. From this blog, Cursor is funded by OpenAI. The model seems default to GPT 3.5 and offer paid GPT4 etc.
        1. I guess the key differentiator behind Cursor is to reduce LLM cost via batching (see Figure 3). Only when a product has vast many users, can this be done efficiently. So the first comer to market offering free-to-use product wins. The winner reenforces itself by taking yet more users. Besides, Cursor did really well in optimizing inference latency.

    n. Related materials
        1. What is the Transformer KV Cache? - Peter Chng
           https://peterchng.com/blog/2024/06/11/what-is-the-transformer-kv-cache/
            1. Good illustration
        
        2. CoreWeave GPU Cloud Pricing
           https://www.coreweave.com/gpu-cloud-pricing
            1. Useful when calculating GPU LLAM COGS

        3. What is prefill stage, and flash attention
           https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/

        4. What Is Embedding and What Can You Do with It
           https://towardsdatascience.com/what-is-embedding-and-what-can-you-do-with-it-61ba7c05efd8

        5. Mastering LLM Techniques: Inference Optimization
           https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/
            1. Very good. It covers almost all LLM key techniques and illustrated easy to understand

        6. Decoder-only的LLM为什么需要位置编码？ - 苏剑林
           https://zhuanlan.zhihu.com/p/720926452

        7. 大模型推理优化技术-KV Cache量化 - 吃果冻不吐果冻皮
           https://zhuanlan.zhihu.com/p/4335176084

        8. llm 论文淘金 - ybq
           https://zhuanlan.zhihu.com/p/719626313
            1. good

7. 国内大厂GPU CUDA高频面试问题汇总（含部分答案） - Tim在路上
   https://zhuanlan.zhihu.com/p/678602674
    1. Useful
    n. related materials
        1. CUDA cores vs Tensor cores: Choosing the Right GPU for Machine Learning  
           https://acecloud.ai/resources/blog/cuda-cores-vs-tensor-cores/

8. 【AI系统】Tensor Core 架构演进 - ZOMI酱
   https://zhuanlan.zhihu.com/p/5274320227
    1. Related materials
        1. 【AI系统】GPU 架构回顾（从2010年-2017年） - ZOMI酱
           https://zhuanlan.zhihu.com/p/4979352189

        2. 【AI系统】GPU 架构回顾（从2018年-2024年） - ZOMI酱
           https://zhuanlan.zhihu.com/p/5184521866

        3. 【AI系统】GPU 架构回顾（从2018年-2024年） - ZOMI酱
           https://zhuanlan.zhihu.com/p/5184521866

9. PolarDB 的 BLOB 实现与性能优化 - 谢榕彪
   https://zhuanlan.zhihu.com/p/738561529
    1. Interesting. very detailed
    2. PolarDB Blob 的写入性能优化
        1. 此时不持有索引的任何锁，离线拷贝 blob 数据
        2 在高并发下能有接近 3 倍的性能提升

    n. Related materials

10. TafDB - 面向未来的分布式存储设计是怎样的？ - 百度智能云
    https://www.zhihu.com/question/549730016/answer/2742709643
    1. 挑战一：在保证元数据操作 ACID 的同时，降低分布式事务的高额开销
        1. 我们解决这个问题的主要思路就是将一个事务涉及的数据都集中在同一个分片，来消除系统中的跨分片事务
        2. 将目前业务场景中所有的两阶段提交都优化为了一阶段提交
    2. 挑战二：在提供高性能写操作的同时，保证范围查询的性能
        1. "标记删除 + 异步清理"的方式会产生垃圾数据
        2. 为了解决这个问题，即缩短连续垃圾数据区的长度。我们将数据删除的压力分散开，将垃圾数据区拆成多个小片；同时增强单点处理垃圾数据的能力，缓解其对范围查询的性能影响。
    3. 挑战三：消除数据流程的单点，提供极致的扩展性和可用性
        1. TafDB 通过基于 Range 分区的分片分裂、调度、回收机制提供了极致的扩展性
        2. 业界的时钟解决方案分为三大类：TSO（全局发号器）、HLC（混合逻辑时钟）和 TrueTime
        3. 最终我们设计了 TafDB 独特的分布式时钟方案（TafDB Clock）：每个存储节点维护本地时钟服务。对于单分片事务，直接使用本地时钟；而对于跨分片事务，通过广播确保整体的因果序。由于 TafDB 中绝大多数事务都被优化为了单分片事务，该方案并不会引入广播产生的显著性能开销。

    n. Related materials
        1. 计算不停歇，百度沧海数据湖存储加速方案 2.0 设计和实践
           https://zhuanlan.zhihu.com/p/2221270079

11. VLDB顶会论文Async-fork解读与Redis在得物的实践 - 阿里云瑶池数据库
    https://zhuanlan.zhihu.com/p/622752885
    1. good work. smart implementation. copy-on-write is promoted on level up to make initial fork faster for Redis.
    2. Highlights
        1. Async-fork设计的核心思想是将fork调用过程中最耗时的页表拷贝工作从父进程移动到子进程缩短父进程，调用fork时陷入内核态的时间，父进程因而可以快速返回用户态处理用户查询，子进程则在此期间完成页表拷贝。与Linux中的默认原生fork相比，Async-fork显著减少了Redis快照期间到达请求的尾延迟
        2. 如果在父进程返回用户态后，子进程复制内存页表期间，父进程需要修改还未完成复制的页表项，怎样避免上述提到的破坏快照一致性问题呢？
            1. 主动同步机制 - deferred copy on write at PTE
                1. 父进程返回用户态后，父进程的PTE可能被修改。如果在子进程复制内存页表期间，父进程检测到了PTE修改，则会触发主动同步机制，也就是父进程也加入页表复制工作，来主动完成被修改的相关页表复制，该机制用来确保PTE在修改前被复制到子进程。
                2. 怎么区分PTE是否已经复制过？Async-fork使用PMD项上的RW位来标记是否被复制。
                3. 同时，在复制PMD项和PTE时，父进程和子进程都锁定PTE表

12. SNIA SDC 2024
    https://www.sniadeveloper.org/events/sdc-2024/agenda/tracks
    1. Efficient Media Utilization Across Dissimilar Cloud Storage Systems    [Microsoft Azure Storage, 2024]
       https://www.sniadeveloper.org/events/agenda/session/681
        1. Good. Garret Buban, Garret Buban

13. S3 RDMA
    1. MinIO’s S3 over RDMA Initiative: Setting New Standards in Object Storage for High-Speed AI Data Infrastructure
       https://blog.min.io/s3-over-rdma/
    2. MinIO releases AIStor with GPUDirect-like S3 over RDMA
       https://blocksandfiles.com/2024/11/13/minio-releases-aistor-with-gpudirect-like-s3-over-rdma/
        1. AIStor
            1. PromptObject, 
            2. S3 over RDMA (w. GPUDirect)
            3. Private Hugging Face API-compatible AIHub repository
    3. S3/RDMA: A Synergy for AI Workloads
       https://www.linkedin.com/pulse/rise-s3rdma-modernizing-data-access-ai-vast-data-tyxrc/

14. Hitachi Vantara: Geo-distributed Erasure Coding
    https://docs.hitachivantara.com/r/en-us/content-platform/9.4.x/mk-95hcph001/replicating-tenants-and-namespaces/geographically-distributed-data-protection/about-geo-protection/geo-distributed-erasure-coding-service-processing
    n. Related materials
        1. NetApp StorageGRID - Object Storage for What's Next
           https://www.youtube.com/watch?v=uO3ZnyFpo6k&t=2031s
            1. Geo-distributed erasure coding. Layered. Logged before



----------------------------
[Book]

1. 程序员修炼之道——从小工到专家 by Andrew Hunt & David Thomas
   https://github.com/hongye612430/awesome-programming-books-1/blob/master/others/%E7%A8%8B%E5%BA%8F%E5%91%98%E4%BF%AE%E7%82%BC%E4%B9%8B%E9%81%93%EF%BC%9A%E4%BB%8E%E5%B0%8F%E5%B7%A5%E5%88%B0%E4%B8%93%E5%AE%B6.pdf
    1. Very good book
    2. Highlights
        1. Rather than "Code Complete", the book tells more about how to do project management
            1. 曳光弹
            2. 破窗效应
            2. 需求工程
                1. 区分需求和（可配置的）策略
                2. 图 7.1 Cockburn 的用例模板
            4. 石头汤与煮青蛙 - Be a Catalyst for Change
        2. Personal growth
            1.  程序员知识资产的管理
                1. 严肃的投资者定期投资，作为习惯
                2. 多元化投资，是长期成功的关键
                3. 保守投资，和高风险高回报投资，之间的平衡
                4. 投资者设法低买高卖，以获取最大回报
                5. 应周期性地重新评估和平衡资产
            2. 所有程序员都应加入至少一个Association for Computing Machinery (ACM) 或 IEEE Computer Society 协会



-----------------------------
[Market research]

1. 行业研究员分析一个公司的流程是什么？ - 乐为
   https://www.zhihu.com/question/21305398/answer/1250410326
    1. Good chart as a decomposition about how to analyze a company's business structure.
    2. The breakdown
        1. 基本面分析
            1. 公司简介
            2. 公司经济区位分析
                1. 区位内的自然条件和基础条件
                2. 区位内政府的产业政策
                3. 区位内的经济特征
            3. 产品竞争能力分析
                1. 波特五力模型
                    1. 同行业内现有竞争者的竞争能力
                    2. 潜在竞争者进入的能力
                    3. 替代品的替代能力
                    4. 供应商的讨价还价能力
                    5. 购买者的讨价还价能
                2. 要分析一个公司的竞争力，就要分析以下几方面
                    1. 成本优势
                    2. 技术优势
                    3. 质量优势
                    4. 产品市场占有情况
                    5. 品牌优势
            4. 股权结构和管理团队分析
        2. 公司所属行业分析
            1. 公司所属的行业周期属性
            2. 行业生命周期分析，这个行业处于哪个阶段？
                1. 幼稚期
                2. 成长期
                3. 成熟期
                4. 衰退期
            3. 行业规模和市场潜力多大？
            4. 影响行业变化的主要因素有哪些？
                1. 技术进度对行业的影响
                2. 监管政策对行业的影响
                3. 社会习惯对行业的影响
                4. 经济全球化对行业的影响
        3. 财务分析
            1. 变现能力分析
            2. 营运能力分析
            3. 偿债能力分析
            4. 盈利能力分析
            5. 投资收益分析
            6. 现金流量分析
        4. 公司重大事项分析
        5. 风险分析
            1. 像下游需求不及预期、行业竞争加剧、导致公司产品销量下降
            2. 出口型公司，汇率波动对公司经营业绩造成影响
            3. 应收账款不能及时收回或发生坏账、成本上升等风险
        6. 未来发展预测
            1. 几种常见的公司分析方法
                1. 比较分析法：分为横向比较和纵向比较，横向比较就是将公司的增长情况、市盈率与同行业其他公司进行对比；纵向比较就是将公司的历史数据和现在进行比较，并来预测公司的未来发展趋势，例如营业收入、净利润增长同比上年增长多少
                2. PEST分析法：企业所处宏观环境分析模型，即P是政治（Politics），E是经济（Economy），S是社会（Society），T是技术（Technology）
                3. SWOT分析法：也就是优劣势分析法，S （strengths）是优势、W （weaknesses）是劣势，O （opportunities）是机会、T （threats）是威胁
                4. 4P营销理论：4p是指：产品（product） 价格（price） 渠道（place） 促销（promotion），4p理论是营销策略的基础
                5. 4PS营销理论：在4P的基础上加上策略（Strategy)，所以简称为"4Ps"
                6. 5W2H分析法：WHAT+WHY+WHEN+WHERE+WHO+HOW+HOW MUCH， 又叫七问分析法

    n. Related materials
        1. 如何在一周内快速摸清一个行业？ - 飞行公路
           https://www.zhihu.com/question/21324385/answer/215888864

        2. 城投评级框架整理 - 灵均
           https://zhuanlan.zhihu.com/p/365880016

        3. 商业模式画布九要素及具体内容 - 啊猫猫
           https://zhuanlan.zhihu.com/p/367456486
            1. Useful summary
            2. 推荐一个叫"帛马"的工具网站，可以一键生成商业模式画布，即开即用，很方便
               https://boomar.cn/

        4. 如何解释产业链和价值链？及其分析方法？ - 付国良
           https://www.zhihu.com/question/26779517/answer/118984070

        5. 怎样做行业研究？ - 盐选推荐
           https://www.zhihu.com/question/21892952/answer/720758646

        6. 怎样进行SWOT分析？ - 萨缪尔
           https://www.zhihu.com/question/20904284/answer/1396501141

2. 知乎圆桌 - 商业研究所
   https://www.zhihu.com/roundtable/companies
    1. Good channel to watch Zhihu updates

3. 如何在一周内快速摸清一个行业？ - 伊娜AI实战笔记
   https://www.zhihu.com/question/21324385/answer/1156006133
   1. 作者：伊娜AI实战笔记
        1. 对于行业研究报告，推荐以下几个地方： 
            1. 证监会官网 在证监会官网上可以找到各个上市公司的上市时候的招股说明书，这是券商针对公司情况出具的一份翔实的报告，里面的行业部分通常是券商经过仔细的调研得出的情况，当然如果是太小的券商出具的报告，有可能深度不够。可以找一下中金、招商、中信证券等大投行出的IPO对应行业的某家公司的招股说明书。 
            2. 巨潮资讯证监会指定的上市公司公开披露信息的网站，在上面可以找到各个上市公司的定期报告和招股说明书等。
            3. 东方财富网 对于未付费用户，每天可以免费下三份报告，找报告的时候同样挑选一下出具报告的券商，还是建议看几个大投行的。 
            4. 万得 這個是要收费的，而且很贵，一般人都不会买，大部分情况下是公司买了給员工用。如果你有朋友在金融机构，可能他手里有公司发的账号，你可以麻烦他下几份。如果嫌麻烦，某宝上或者某鱼上搜一搜，便宜得很。 
            5. 网站：发现报告 这个网站上有"行业研究"、"宏观策略"、"公司研究"、"招股说明书"和"其他报告"四个板块，每天会新增几百到上千份报告，报告来源于其他各个网站，包括消费、互联网等，常见的行业一般能在这上面搜到。 
            6. 网站：并购家 这个网站关注的是行业内的并购事件，也能在上面找到各个行业的报告。 
            7. 网站：行行查上面有行业数据、法规、技术变革、竞争格局等，是我最近用得比较多的一个网站，上面还会根据关键字提取报告中的内容，譬如"商业模式""产业链"等。

    n. Related materials
        1. 哪里看最新行业研报？ - 吾知吖
           https://www.zhihu.com/question/438907767/answer/1688450162

        2. 在哪里能找到各行业的分析研究报告？ - 李启方
           https://www.zhihu.com/question/19766160/answer/1711406770

4. 三张报表之间的勾稽关系应该如果去加深理解？ - 帆软
   https://www.zhihu.com/question/319408428/answer/1771003839
    1. Finereport 领先的企业级Web报表工具
       https://www.fanruan.com/finereport/
    2. Useful guide for reading financial reports

    n. Related materials
        1. 如何才能看懂企业的财务报表？ - 阳光下的沈同学
           https://www.zhihu.com/question/27785329/answer/1730926707
            1. Good lists of what each item means in financial reports.
            2. Highlights
                1. 净资产收益率ROE=净利润÷净资产（所有权权益|股东权益）x100%
                    1. 净资产收益率还可以这样更加详细的拆分：
                        1. 净利润÷销售收入（就是产品的净利润率）
                        2. 销售收入÷平均总资产（就是总资产周转率）
                        3. 平均总资产÷净资产（就是杠杆系数）
                    2. 企业要赚钱肯定有一个特色，要不就是产品利润巨大，要不就是资产周转极快，要不就是杠杆撬动更多资源。 ... 企业要赚钱肯定有一个特色，要不就是产品利润巨大，要不就是资产周转极快，要不就是杠杆撬动更多资源
```