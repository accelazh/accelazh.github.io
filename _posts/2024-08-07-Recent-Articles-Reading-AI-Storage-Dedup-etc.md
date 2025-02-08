---
layout: post
title: "Recent Articles Reading: AI Storage, Dedup, etc"
tagline : "Recent Articles Reading: AI Storage, Dedup, etc"
description: "Recent Articles Reading: AI Storage, Dedup, etc"
category: "Paper Reading"
tags: [storage, paper, cloud]
---
{% include JB/setup %}

```
1. AI时代云厂商仓皇的文件存储 - 王太平 太平说存储    [2024]
   https://mp.weixin.qq.com/s/Ir0bi5KYvPUfAw-qYZNM_g
    1. Useful summary of filesystem landscape
    n. Related materials
        1. GTC 2024 英伟达的存储观点 - 王太平 太平说存储
           https://mp.weixin.qq.com/s/bCV1Efux_S8Ye7PunDlpqQ
            0. Good.
            1. Which storage to use? Local SSD => TOR NVMe => RDMA flash
            2. GPUDirect Storage (GDS): Data path bypass CPU, partner ecosystem vendors, 
            3. Big accelerator Memory (BaM): GDS need 32KB or larger IO size to saturate PCIe. BaM achieves the same by 4KB. Smaller IO size reduces IO amplification in transfer. Unlike GDS, BaM keeps both data path and metadata path in GPU.
            4. GTC 24 SCADA (scaled accelerated data access) : GPU + NVLink + NVMe, auto data scale out & partitioning & management. High level layout to solve data scale needs, where GPU memory is not large enough or cheap enough. CPU and PCIe are excluded from the picture. Big challenge to CXL.
            5. GDS生态的创新型供应商：创新型：vast、weka、hammerspace

        2. AIGC世界的IO特征研究 - 王太平 太平说存储
           https://mp.weixin.qq.com/s/cRfdnvCZtgKVLjUCdZK2oA
            0. Good.
            1. WEKA: IO Profiles in Generative AI Pipelines    [2023]
               https://www.weka.io/wp-content/uploads/files/resources/2023/09/io-profiles-gen-ai-pipelines.pdf
                1. Metadata Handling, Lots of small files (LOSF)
            
                2. Conclusions - Very good part
                    1. Challenges
                        1. Data stall from having to copy data between siloed platforms that are designed and/or tuned to only meet the IO needs of a single portion of the AI data pipeline.
                        2. Being able to handle the IO blender that occurs when data is consolidated from solving the siloed platform problem
            
                    2. Ongoing trends
                        1. Bursty IO at small time intervals. As a data pipeline continues to be run with multiple portions of the pipeline overlapping this burstiness increases with varying IO ratios and IO sizes.
                        
                        2. IO read/write ratios and IO sizes wildly vary. In individual segments of the data pipeline, they may be relatively consistent, but in others, they may be quite different, including between reads and writes.
                        
                        3. Latency is the leading indicator of overall performance within the GenAI environment. Because most operations in the AI environment must be immediately consistent, (i.e., retuning the foundational model or creating and embedding features), having low latency for all operations makes the consistency happen faster, and the AI process can move to the next iteration quicker.
                        
                        4. Metadata overhead. Regardless of the IO profile or use case, Metadata lookups and overhead can account for 25-75% of the operations in a system. File opens, stats, seeks, etc. account for this.

                    3. Many data platforms struggle with
                        1. Trying to create low latency transports by layering RDMA with older file protocols like NFS. While it works, it still cannot achieve the ultra-low latencies that newer technologies such as DPDK with NVMeoF-like transports can achieve.

                        2. Filesystem latency. If the filesystem itself is not designed for massive parallelization of both metadata and data operations, then it winds up serializing access, resulting in delays in responding to IO requests from clients. 

                        3. Tuning for individual workload profiles. Many platforms have made design choices resulting in optimizing for singular performance profiles. This results in having to copy data within the platform to specifically tuned sections, which creates data stalls.

                        4. Inability to scale against the Lots Of Small Files (LOSF) problem.. With foundational models and other large learning models ingesting millions and sometimes billions of files of training data, many platforms struggle with handling this unstructured data. The workaround is to concatenate the data into a smaller number of large files, but this creates other access problems and can increase latency.

                    4. WEKA for Generative AI technologies
                        1. WEKA's use of kernel bypass technologies such as DPDK and SPDK along with fast networking up to 400Gbit. creates a ultra-low latency transport layer similar to NVMeoF for data and metadata.

                        2. By having a completely distributed and parallelized architecture that looks to achieve the lowest queue depths for any operation in the system, WEKA can handle all types of workloads concurrently while maintaining consistent 100-200 microsecond latencies.

                        3. This same architecture and focus on low latency allows WEKA to handle high IOP, large streaming, or mixed workflows with aplomb. This allows for consolidation without performance tradeoffs, or having to constantly tune sections of the system to optimize for a single part of a workflow.

                        4. WEKA's architecture was designed upfront for multi-exabyte capacity scaling challenges. This translates into not having to worry about where your data lives in the WEKA platform. Billions of files in a single directory and trillions of files in a single namespace? With WEKA you aren't forced to concatenate files to make up for limits in the filesystem, simplifying your workflow and number of operations to make use of your data. WEKA easily handles the LOSF problem.
            
            2. Highlights
                1. DNN
                    1. 大量小文件，<100B or 10 KB-1 MB，对文件系统造成元数据密集负载。
                        1. 30%的读取是文件打开。
                        2. "Hidden IO" - Stat and Seeks from finding the files needed to pull into pre-processing, accounts 1/3 to total IOs.
                    2. 在Pre-processing阶段对总时间花费近1/3，涉及注释/标记、图像缩放、对比度平滑、索引等。
                    3. Inference阶段对文件系统的IOPS极小，相比预处理和训练阶段。
                2. AIGC / NLP
                    1. 负载剧烈波动，平均利用率约5%，最大利用率稳定在80-100%。
                    2. IO大小：读IO大（300-500K)，写IO小(100-200K)。小写来自append来自Checkpointing的增量。小读来自H5文件，预处理后使读能定位到较小range。
                    3. AI过程对于IO最敏感的是时延而不是吞吐。读写以及IO大小都是弹性多变的，并且还有大量元数据IO。
                    4. Filesystem vs Object Storage - think the metadata cost of small IO files, small IOs.
                3. AI存储的主要挑战：
                    (1)如果期望通过RDMA技术加速传统NFS等协议可能不一定是个好想法，还是要考虑另起炉灶，考虑新的实现方式。比如说自研客户端，做并行文件存储（pnfs也行），GDS适配等。
                    (2)低时延问题，文件存储本质上复杂度要高于块存储，所以在块存储场景的低时延在大规模小文件场景如何实现。
                    (3)混合IO,很多时候我们的存储系统内部的条带深度、块大小、缓存算法、qos策略等都是默认设置好的，在AI时代如何精细化的适配?
                    (4)海量小文件的元数据效率，假设10亿文件场景的海量小文件，如何保障批量元数据操作的效率以及数据随机遍历的性能？

        3. AI存储之VAST Data分析 上篇 - 王太平 太平说存储
           https://mp.weixin.qq.com/s/pVRL_vtt8jJbTckJBdS5Cg
            1. Vast data 与传统存储主要有以下个方面的区别
                1. 放弃HDD，全闪存+SCM。放弃全局缓存，用SCM代替。 通过QLC+SCM的模式优化成本。通过顺序大IO的异步写入来优化寿命。同时，提供146+4的EC。

                2. Share Everything: 集群中的所有 CNodes 都会在启动时通过 NVMe-oF 挂载集群中的所有 SCM 和flash SSD。每个 CNode 都可以直接访问集群中的所有数据和元数据。
                    1. 计算节点被称之为CNode,存储节点称之为DNode
                    
                    2. 对于Cnode来说，它是基于容器化运行的，无状态的，任何一个cnode失效，对于整个存储系统来说是无关的，不影响的。VASTOS 的升级过程实例化新的 VASTOS 容器，而无需重新启动底层操作系统，从而将 VAST 服务器的脱机时间缩短到几秒钟。（整个系统的升级效率非常高，传统存储每次升级都要选择业务低估，预留小时级的时间进行升级）

                    3. 计算节点的无状态，但是后端的存储节点可不行。因此需要提升存储节点的可靠性。在设计中，每个 HA Enclosure 都包含两个 DNode，它们负责通过每个 DNode 上的 PCIe 交换机芯片将 NVMe-oF 请求从端口路由到机箱的SSD。
                        1. 这意味着，从网络端口到SSD都是冗余设计的，这个在分布式存储中并不少见。但是Dnode并不承载过于复杂的业务，因此每个机箱中都是使用了ARM DPU作为DNode的处理器。每一组Enclosure 中的两个DNode采用全active-active的工作模式。
                            1. This is the very good part.

                    4. 元数据保存在DBbox的SCM中，构成全局共享池。一个范围的key归属两个特定的DNode（存双份）
                        1. CNode -> 加载 1GB 的 consistent hash table -> 定位到key归属的2个DBox -> V-tree保存每个元素（文件、对象、文件夹、表、卷等）元数据

                4. 软件订阅销售：21年开始推出了名为Gemini的软件订阅服务，打破了传统存储厂商软硬件一体化销售的方式，也打开了自己在头部厂商领域的机会窗。毕竟并行文件存储可没有几家厂商有。当然对于没有指定的情况下，VAST data的硬件由他自己的硬件供应商Avnet提供。后来又有新增的各种供应商。比如说：在Google cloud中、在CoreWeave的GPU云中，比如说和supermrico合作。
                
                5. 和NVIDIA结合：作为早早锚定的赛道，vast data在2019年就开始宣传自己针对AI场景设计的理念，当年可没有几个厂商在这里深耕或者重点挖掘。他通过和NVIDIA DPU构建存储节点、跟CoreWeave适配端到端NVIDIA的硬件。打造了自己最适合AI大模型场景的人设。

            2. AI存储之VAST Data分析 架构篇 - 王太平 太平说存储
               https://mp.weixin.qq.com/s/TXPtyjkfDrdY0r9YB1b-yg
                1. Server design - Canister - 与NVIDIA紧密结合
                    1. No CPU, use 2 NVIDIA BlueField DPUs
                        1. BF1600 has on chip SSD, what does it do?
                    2. DPU -> PCIe switch -> NIC -> GBE VLAN switch
                                          -> NVRAM, M.2 SSD, Capacity SSDs  
                    3. AI server -> 2x Storage Controller -> all-to-all Storage Enclosures
                        1. Storage Enclosures has no CPU, only 1x BF DPU + SSDs
                        2. Storage Controller and AI server has CPUs.
                    4. This is the good part.

            3. AI存储之VAST Data分析 下篇 - 王太平 太平说存储
               https://mp.weixin.qq.com/s/p027mz0NOzBLLzXoxAc0AQ
                1. 如何解决并发处理的问题 - in an all-to-all shared everything architecture
                    1. VAST V-Tree的元数据的更新需要通过transaction tokens，全局唯一、可从所有服务器访问。
                    2. 写操作创建一个元数据对象，元数据对象上附加了一个事务令牌并且表明事务正在进行的状态。
                    3. 数据首先写入两个SCM，然后创建事务元数据对象，最后修改V-Tree链接。冲突则事务重试，陈旧链接由GC清理。
                    4. Element Locking，由server id签名。
                        1. 当一个cnode发现需要访问的元数据对象被另一个cnode加锁，他会去主动联系对应的cnode，防止因为cnode离线而带来的死锁。如果所属服务器无响应，则请求服务器还将要求另一个未参与的服务器也轮询所属服务器，以确保请求服务器不会遇到误报。
                        2. 为了确保写性能，vast 在DNode的内存中缓存了Element Locks 的只读副本，cnode可以通过原子rdma操作就可以查看和更新只读锁的信息。
                        3. 由于没有全局缓存系统，因此锁机制更简单更高效
                        4. Interesting design
                2. 大条带的优势
                    1. Vast使用的lowest-cost hyperscale SSDs，大量的使用QLC介质，并且剔除了传统SSD中的缓存，所有数据直接到NAND Flash的page。因为，Vast的每次写入数据是非常大（都是异步批量写入，大小128KB+）
                        1. 可以看出，与许多企业存储系统中常见的 4KB 随机写入相比，QLC SSD 在大型连续条带写入时的耐用性提高了 20 倍。这是VAST确保SSD可靠性的关键手段。
                            1. 如果在业务上层，每次写入和擦除都以page甚至与Block对其，则整体的耐久性有极大的提升。
                            2. 并且由于可以在整个系统层面进行空间，减少SSD内部自己做的磨损平衡做的搬移，则会更好。
                            3. 大部分系统都期望跳过FTL层来直接优化闪存NAND。采用SCM+flash的架构有机会实现，因为SCM可以拦截大量的数据不需要下盘
                            4. Vast将FTL从单盘层面提升到了系统层面。VAST DataStore 管理所有超大规模 SSD 上的闪存，就像 SSD 中的 SSD 控制器管理其闪存芯片一样。
                            5. VAST DataStore 以 1 MB I/O 写入 SSD，这是底层闪存 64 KB-128 KB page size大小的很多倍，从而允许 SSD 控制器在 SSD 内的闪存芯片上并行化 I/O。
                            6. 管理 1 GB 条带中的数据会将每个擦除代码条带与 SSD 内的一组EC对齐。当VAST DataStore执行垃圾收集时，它会从每个SSD中擦除整个1 GB EC。SSD不需要在自己做垃圾回收
                            7. VAST Foresight - 根据数据的预期寿命将数据写入EC条带，从而最大限度地减少垃圾收集造成的写入放大。
                            8. 全局磨损均衡，leveraging a shared-everything architecture.
                        2. Good design
                        3. My questions
                            1. Be careful with DPWD of SCM or SSD. If NVRAM is used as cache, the write throughput is full but capacity is small. It means the flash wear out will be very high.
                    2. 数据EC
                        1. 146+4, GC a 150GB stripe, global shared-everything to improve durability, locally decodable codes for fast reconstruction.
                3. Global, Cross-Block Compression
                    1. Breaking Data Reduction Trade-offs with Global Compression
                       https://www.vastdata.com/blog/breaking-data-reduction-trade-offs-with-global-compression
                        1. Global Similarity Reduction, similarity compression, similarity hash
                        2. Plus traditional compression and deduplication
                4. 存储与 DPU
                    1. DPU（Data Processing Unit 数据处理器）最早由Fungible提出概念，随后Mellanox跟进打磨，随着Mellanox被NVIDIA收购并在之后的两年多内不断迭代产品演进增强，目前以BlueField和Fungible为代表的DPU产品在数据中心占据着C位角色，国内外众多厂商密切关注。
                5. 大容量SSD的使用
                    1. 在全闪存高性能的存储集群中大规模应用SCM+低成本SSD，达到替代现有SSD+内存架构的目的。
                    2. 全局FTL的构建
                    3. 大条带的优化，当前很多云厂商在EC优化上都有一定的经验
                6. 多协议融合
                    1. 当前VAST的数据可以被以块的方式直接访问
                    2. 数据库的数据可以用sql也可以用S3访问数据库文件
                    3. 单一数据块，可以同时被对象存储元数据和文件存储元数据访问，因此，可以轻松的实现多协议互访。
                7. 商业模式
                    1. Nimbus Data预测，Pure Storage将停止销售新闪存阵列，
                    2. VAST不销售硬件可能是明智的选择，2024年VAST将会支持三大云厂商

            n. Related materials
                1. AI存储厂商分析之Hammerspace - 王太平 太平说存储
                   https://mp.weixin.qq.com/s/B5YsCpeZRsUSOqk1l6GqBA
                    1. Meta的主存储部署通过用户空间中的本地 Linux 文件系统 (FUSE) API 来满足 AI 集群的数据和checkpoint需求，该 API 由针对 Flash优化的 Meta 的"Tectonic"分布式存储解决方案版本提供支持。
                       其次，Meta还与Hammerspace合作，共同开发并落地并行网络文件系统（NFS）部署，以满足该AI集群的开发者体验要求。除了其他优势之外，Hammerspace 还使工程师能够使用数千个 GPU 对作业执行交互式调试，因为环境中的所有节点都可以立即访问代码更改。    
                    2. Highlights
                        1. 传统存储系统由于分级存储、不同的数据协议、生命周期、站点、地域等多个维度的割裂，造就了跨越不同存储系统的割裂的存储系统分布。

                        而AI的流程更加漫长，有可能加剧这种割裂。这个问题对于AI/DL工作负载来说尤其严重，其中关键的第一步是整合来自多个来源的数据，以实现跨所有数据源的全局视图。人工智能工作负载必须能够访问完整的数据集，以便对文件进行分类和/或标记，这是确定哪些文件应该细化到流程的下一步的第一步。之后则是训练、精调推理等等。

                        Hammerspace想法时重新构想了一个基于标准的文件系统，它独立于专有的存储基础设施，但仍然与任何供应商的现有存储系统兼容，从而解决了这个问题。

                        Hammerspace是一种软件定义的解决方案，可与任何供应商的任何本地或基于云的存储平台兼容。Hammerspace创建了一个提升到存储系统基础设施层之上的高性能文件系统。通过这种方式，它创建了一个高性能的、并行的全局文件系统，可以跨越任何供应商在一个或多个位置(包括云)上的存储。
                        
                        2. Hammerspace从现有的存储系统先获取历史数据的元数据信息，然后通过NFS V4.2的并行文件存储视角呈现给客户。

                        在历史存储中不需要部署任何的代理设备，访问数据不需要在用户系统上安装客户端软件（默认使用Linux NFS client），对于用户和应用程序，Hammerspace并行全局文件系统提供与任何企业NAS完全相同的行业标准SMB或NFS挂载点。

                        3. NFSv4.2, pNFS, FedFS, Flex Files


        4. S3 Express One Zone的个人浅见 - 王太平 太平说存储
           https://mp.weixin.qq.com/s/2DWvWKyVY0Ws3kShctVThw
            0. Interesting
            1. S3 express one zone与Amazon File Cache有什么不同？ 
                1. 但是从技术上讲有什么差异，这个不是我们蒙昧以求的serverless file system吗？我们多想抛弃30年来的posix、nfs、smb对于我们云存储的束缚，已经2023年了，我们的计算框架、AI框架、包括可笑的云原生框架Kubernetes访问数据竟然是原始的posix，可笑不？在容器环境、ai环境访问云存储大家都是使用fuse客户端结合厂商提供的一个玩笑般的小玩具：S3fs，这不是对存储人最大的无声嘲讽吗？    
                2. 参考上图：S3 express one zone带来的冲击是我们看到serverless的存储服务将存储和计算耦合分解开来，带来更多的创新。
                3. 在S3之前构建一个复制层需要大量的工作，但许多系统都采用这种方法，因为它们希望从存储层获得所有三个核心价值：便宜，可靠性和稳定性，性能（低时延和高带宽）。
                    1. 我之前服务了一个AIGC的客户，为了在几千个可变的stable diffusion模型中快速的切换和启用对应pod并生成相关的文生图结果，期望能够每秒500-1000MB/s的数据加载速度，同时还要价格可控。最终他们选择了juicefs缓存层来解决这个问题。
                    2. 在S3 express one zone出现后可能的数据组织模式：
                        1. Fast Storage - S3 Express 1 Zone
                           Fast Storage + Cache - S3 Standard + Cache.
                           Standard - S3 Standard.
                           S3 Express 1Z -> S3 Standard
                        2. 但是可以看到第四种数据组织模式当前还有两个巨大的问题没有解决：
                            1，S3 Express One Zone到S3 standand的数据方式（还没有解决，但是预期是有很多方法可以解决）    
                            2，S3 Express One Zone的费用（这个预期也能解决）
                        3. Jack Vanlightly: S3 Express One Zone is it's the right technology, at the right time with the wrong price
                           https://jack-vanlightly.com/blog/2023/11/29/s3-express-one-zone-not-quite-what-i-hoped-for

            n. Related materials
                1. AWS reInvent 2023-存储更新解读 - 王太平 太平说存储
                   https://mp.weixin.qq.com/s/xt3uA6PuINay8pW6HMt6sQ
                    1. S3 Express one zone

        5. Google Cloud Next 2024存储看点-上篇 - 王太平 太平说存储
           https://mp.weixin.qq.com/s/knGUix-txc0qg5gteEqIsg
           Google Cloud Next 2024存储看点-下篇 - 王太平 太平说存储
           https://mp.weixin.qq.com/s/v-qOcAbhwnD1LqJxYhqdRA
            0. Good summary and analysis.
            1. 新一代基础设施AI Hypercomputer
                1. 优化的硬件
                    1. Cloud TPU v5p 和由 NVIDIA H100 Tensor Core GPU 提供支持的 A3 Mega VM 的正式发布
                
                2. 针对 AI 工作负载的存储产品组合优化
                    1. Cloud Storage FUSE（正式发布）是 Google Cloud Storage 的基于文件的界面，它通过提供对高性能、低成本云存储解决方案的文件访问，将 Cloud Storage 功能用于更复杂的 AI/ML 应用。今天，我们宣布新的缓存功能已正式发布。Cloud Storge FUSE 缓存将训练吞吐量提高了 2.9 倍，并将我们自己的基础模型之一的投放性能提高了 2.2 倍。

                    2. Parallelstore 现在还包括缓存（预览版）。Parallelstore 是针对 AI/ML 和 HPC 工作负载优化的高性能并行文件系统。与原生 ML 框架数据加载器相比，新的缓存功能可将训练时间缩短多达 3.9 倍，训练吞吐量提高多达 3.7 倍。

                    3. Filestore（正式发布）针对需要低延迟、基于文件的数据访问的 AI/ML 模型进行了优化。基于网络文件系统的方法允许集群中的所有 GPU 和 TPU 同时访问相同的数据，从而将训练时间缩短多达 56%，优化 AI 工作负载的性能并提升要求最苛刻的 AI 项目。

                    4. Hyperdisk ML 预览版，这是针对 AI 推理/服务工作负载进行优化的下一代块存储服务。与常见替代方案相比，Hyperdisk ML 将模型加载时间缩短了 12 倍，并通过只读、多连接和精简配置提供了成本效益。它支持多达 2500 个实例访问同一卷，每个卷的聚合吞吐量高达 1.2 TiB/s，性能比 Microsoft Azure Ultra SSD 和 Amazon EBS io2 BlockExpress 高 100 倍以上。
                
                3. 开放软件的进步
                    1. 包括引入 JetStream，一种用于大型语言模型的吞吐量和内存优化推理引擎 （LLMs），可在 Gemma 7B 等开放模型上提供更高的每美元性能，以及 JAX 和 PyTorch/XLA 版本，可提高云 TPU 和 NVIDIA GPU 的性能.

            2. 总结google的存储理念还是非常美好的，store once，access anywhere，any performance，any interface。要不是google下面贴了一张图，我都为这个理念沉醉。
                1. This is very good.
                2. Anywhere
                    1. Multi-region + Anywhere cache
                3. Any performance
                    1. 针对不同的业务场景提供了不同的块存储选择，分了四类：吞吐型的hyperdisk（离线分析，冷数据）,均衡型hyperdisk（日常），极速型hyperdisk（企业数据库），hyperdisk ML（机器学习）。    
                    2. Hyperdisk ML

            3. Hyperdisk ML
                1. 提供弹性扩展到1.2TBps的带宽（和容量解耦的），其次只需要$0.08 per GB(跟均衡型块存储价格一致），性能成本为$0.12 per MBps。Hyperdisk ML的性能和容量是独立扩展的
                2. Google提供了存储pool的概念，允许以总存储池的概念来申请hyperdisk。不同云盘之间性能可以共享
                3. Hyperdisk ML是一个多重挂载的块存储，最大支持2500个实例挂载。Hyperdisk ML是只读的。

            4. Parallelstore并行文件服务
                1. Parallelstore是Google基于Intel DAOS提供的托管并行文件服务
                2. Intel DAOS是intel开源的分布式对象存储，但是可以使用client进行通信，client是支持posix的。其次DAOS最初是为了傲腾适配而研发的，采用SCM做元数据管理，采用NVMe SSD做存储层，主打就是一个高性能。    

            5. 具有文件缓存功能的 Cloud Storage FUSE  
                1. Cloud Storage FUSE 允许您将 Cloud Storage 存储桶挂载为文件系统 - 类似 AWS S3 mounted filesystem, s3fs
                2. Google fuse的设计缓存更加精细，支持针对bucket以及单独的前缀设置缓存，还可以设置元数据缓存等，该功能看起来不出彩，但是很多场景很有用。Cloud Storage FUSE 提供三种类型的可选缓存来帮助提高数据检索的性能
                    1. Cloud Storage FUSE 文件缓存是基于客户端的读取缓存
                    2. Cloud Storage FUSE 统计信息缓存是用于对象元数据的缓存
                    3. Cloud Storage FUSE 类型缓存是元数据缓存

        6. 存储workload的演进1传统时代 - 王太平 太平说存储
           https://mp.weixin.qq.com/s/wXTd9ljkoqyGoXvDx31EzA
           存储workload的演进2-传统时代补充篇 - 王太平 太平说存储
           https://mp.weixin.qq.com/s?__biz=MzUzNzE1Njk3MQ==&mid=2247484689&idx=1&sn=de7b78e6750618ee11f2e26dbfc2ce8e
           存储WorkLoad的演进3-微软的早期研究 - 王太平 太平说存储
           https://mp.weixin.qq.com/s?__biz=MzUzNzE1Njk3MQ==&mid=2247484733&idx=1&sn=9bc3f3f8bdf9eeb01d711a35bbb9fa2f
           存储WorkLoad的演进4-Mapreduce的负载研究 - 王太平 太平说存储
           https://mp.weixin.qq.com/s?__biz=MzUzNzE1Njk3MQ==&mid=2247484737&idx=1&sn=8430b2a760334e6477975c2e979d93e1
           存储WorkLoad的演进5-Spark的负载研究 - 王太平 太平说存储    [2024]
           https://mp.weixin.qq.com/s/b3SxZZSdU_5lwRaFT40-eQ
            1. 商用存储
                1. Nimble storage发布了一个关于自己客户的IO特征分析
                   Mapping the Demands of Real-World Apps — One IO at a Time
                   https://ceo.digital/wp-content/uploads/2017/03/Nimble-Labs-Research-Report_Mapping-Real-World-Apps.pdf
                    1. Very useful.
                2. 场景：OLTP数据库、OLAP数据库、虚拟化、桌面云、运维日志
            2. 微软的早期研究
                1. 工作负载以读为主：读请求与写请求的比率为2.37
                2. 写卸载 - 本质是写缓存，来将写操作缓存起来，可以用内存、SSD或者HDD来做
                3. 最忙的一天硬盘能耗的下降（平均能耗下降接近50%）
            3. Mapreduce的负载研究 - Yahoo
                1. 高文件流失率(高创建/删除率)，导致80% - 90%的文件在6个月内最多被访问10次
                2. 有一小部分非常受欢迎的文件:不到3%的文件占访问(打开)的34% - 39%。热点很集中）
                3. 新文件占访问的百分比很高，但存储的容量百分比很小
                4. 观察到的请求间到达(打开、创建和删除)是突发的，并且表现出自相似的行为（突发的性能burst需要弹性）
                5. 文件寿命非常短:90%的文件删除目标是22.27分钟- 1.25小时的文件。（针对hdfs做读写cache非常有价值）
                6. 最常见的操作是open(55%−60%)，其次是listStatus (ls);它们加在一起占了绝大多数的操作(80% - 90%)
                7. 在向master server发出的操作中，open事件占一半以上;open+ listStatus，加起来占了绝大多数的操作(80% ~ 90%)
            4. Spark的负载研究
                1. 读取业务的特征分析
                    1，数据越近访问越多，数据越久访问越少
                    2，所有的访问特征（读size、单文件热度）都具有明显的长尾效应
                    3，读取操作发生是突然burst上去的
                    4，特征分布长时间内是平稳的
                        1. 赫斯特指数（Hurst exponent，记为 ）来刻画一个时间序列的长记忆性。
                           https://zhuanlan.zhihu.com/p/38282038
                    5. 大多数的读取的IO大小非常小，50%的io可能低于4bytes（中位数），90%的IO小于1KB，而P99分位的大io读取访问处理了超过80%的数据读取
                        1. 极小的读请求可能是来自于元数据操作，所以在数据湖存储场景元数据是一个典型优化点（又多又小，又最影响业务性能）
                            1. Very interesting
                        2. 在其他的研究中，我们可以看到，web缓存中90%的io小于1KB，HPC中90%的IO小于100Kb-1MB，而在消费者云中则小于4MB（主要是个人产生的数据）、在视频监控场景为10MB，在HBASE中为15MB。本次研究中的IO请求明显特别小。


        7. 存储沉思录之一 存储衰落之我见 - 王太平 太平说存储   [2018]
           https://mp.weixin.qq.com/s/CQeeFwbDlveoepHOm9xF6g
            1. 2013年之前，存储阵列还是高级玩意。2013年市场变化了，数据开始爆发式增长，数据从企业数据走向了用户数据市场。这个一切的诱因则是移动互联网的普及以及互联网公司的跨界。DELLEMC ... 不仅没有扩大战果，连自己的传统企业客户市场也开始纷纷向移动互联网公司开发的公有云倒戈，非关键业务市场在向超融合架构、分布式存储倒戈，一泻千里。
            2. 数据价值越来越低，欧洲运营商已经连年营收不增长，利润负增长，但是数据却在以每年50%左右的速度爆发式增长，那就意味着每TB的存储预算在每年20~30%的下降。
            3. 未来存储的死胡同
                1. 当集中式数据库无法满足移动互联网的百万、千万级并发需求，传统的IOE架构走向衰亡，企业存储这种针对IOE架构设计的产品也不可避免走向衰落。
                2. 大量的高可靠性诉求以及SLA诉求导致存储成本居高不下，未来爆发式增长的数据空间将全部存储在非企业存储上，何以为继？
                3. 大颗粒的数据将走向计算和存储的融合，同时功能走向定制化，专业存储设备为了普适性而做的开发的设计反而变成了鸡肋，成为拖垮存储的最后一根稻草？

            n. Related materials
                1. 存储沉思录2 企业存储架构之争 有什么好争？ - 王太平 太平说存储   [2018]
                   https://mp.weixin.qq.com/s/3d374bUe_mS_vbG04UyzPw
                    1. 在2012~2014年全球最火的是全闪存，这个时候国内厂商还在努力做高端存储
                       2016~2017年是分布式存储火起来的几年，从只认企业存储到分布式存储以及超融合大行其道就是这两天的时间
                    2. 高端存储和全闪存有什么区别？
                        1. "在我看来，高端、中端、低端存储甚至于全闪存存储没有什么区别，只是用料的差异而已，甚至于用料都没有差异，只是规格大小的差异。你的软件做的好可靠性好，那你就可以高中低端市场全部用一套软件，比如说HDS、HPE 3par、Netapp。如果你的软件做的不好就只能在入门级玩玩，比如说HPE的MSA。当你的软件灌装在一个低配的硬件上就是低端、高配的硬件上就是高端，但是是否客户认可你还是需要长期的客户关系和案例去积累。"
                    3. 其实分布式存储的未来大卖依赖几个前提，这几个前提正在消失：
                        1. 软硬件解耦（现在不但没有解耦，大多数分布式软件正在走向定制化）
                        2. 预期X86服务器性能每两年有大幅提升，同时价格不变
                        3. 分布式存储软件兼容不同型号不同类型的硬件，可以随着硬件生命周期更迭而软件不需要替换。
                    4. 为什么分布式在这个点火了，那是因为企业数据价值大幅下降，垃圾数据大大增加，而企业的预算和营收并没有大幅增加，所以存储的成本必须降，所以分布式就成了唯一的选择。

        8. 浅谈存储硬件（1）- 太平说存储    [2018]
           https://mp.weixin.qq.com/s/TaHo6ZzJ2jG45jzn6zTt_g
            1. 存储处理器的演进
                1. 早期的存储设备更多是一个计算密集的业务，大量的存储设备都采用专用的或者定制化的芯片来完成业务的处理。这个时候存储控制器芯片是一个百花齐放的年代。随着intel逐步的快速重金投入研发以及对存储市场的重视（推出ISA-L库），存储的主控制芯片渐渐又成为存储的主流。
                   比如说EMC在老的DMX4上还是用了大量的ASIC来进行加速，但是到了EMC VMAX时代，全部的操作交由intel cpu来实现，同时中端的Unity\XtremIO、分布式NAS 的islion全系列都是采用intel芯片。
            2. 未来的存储控制芯片预期
                1. 在2017年intel的摩尔定律已经开始失效，虽然当前看来intel的处理器市场份额已经占据极大优势，但是背后隐藏的问题多多。越往上多核带来的性能优势越小。同时，闪存介质的性能大幅提升，借助于NVMe技术的发展，单块SSD的性能接近10万IOPS（通用场景），相当于以前一台高端存储阵列的性能。
            3. Violin 和 EMC DSSD前车之鉴
                1. 我又想起来DELLEMC 砍掉DSSD时候所说的："These enterprise customers apparently told Dell that they loved the performance but wanted (needed) mainstream all-flash array data services, such as those we assume on VMAX and XtremIO products. The HPC customers said that mainstream all-flash arrays and bulk capacity storage met their requirements, so there was no general need for a separate D5-type product."
                   这一个让人无奈的情况，企业客户不仅仅要性能还要可靠性和数据服务能力，HPC的客户觉得当前性能已经够了。那么E8的路在何方？

        9. 浅谈重删压缩技术（一）- 太平说存储    [2017]
           https://mp.weixin.qq.com/s/dkYrf5tPq0mgI_b--FY1Ig
            1. 但是变长重删对性能和算法要求都比较高，同时对于CPU内存消耗也大，影响了数据的实时处理效率。毕竟存储主要还是处理主机的IO读写响应的。只有在备份归档领域用的比较多，因为这个场景节省空间比快速响应要求高的多。以下面这个图片为例，变长重删效率可能达到10:1，而定长重删只有3:1.
            2. 开启压缩，导致边长块，必须引入ROW（redirect on write）架构，带来性能开销
            
            n. Related materials
                1. 浅谈重删压缩技术（二）- 太平说存储    [2017]
                   https://mp.weixin.qq.com/s/yD4MPagUxHSFSuMZpipp_A
                    1. 从上述几个例子可以看出，实现重删压缩同时保障性能以及稳定性有多难。时至今日，我们看到HDS、HPE的重删性能冲击超过50%，EMC高端全闪存至今不具备重删能力。
                    2. 不用ROW，照样实现在线压缩，硬盘实现压缩，HDS独一家
                    3. 硬件加速减少性能损耗
                    4. EMC VMAX软件巧手设计
                        1. 将以前的一个盘切成16个hyper volume的模式做了改变，改成了切分为64个，然后针对每个hypervolume组设置不同的track size，16K、32K\48K一直到72K不等，每个不同的track size默认准备一个hypervolume的LUN组，64K默认准备2个，其他的都设置为128KB。
                           由于软件架构设计的下盘IO大小为128K,所以数据在压缩后只会比128k小，从8KB到128K不等，大多数都是在72K以下。按照压缩后的块大小挑选对应的hypervolume组进行下盘。如果某个规格的hypervolume用完了，就从默认的剩余hypervolume组里面取一个出来，将track size改成对应的块大小即可。
                           这个两个动作执行后，超级完美的避免了压缩后块大小不一致带来的数据拼接问题，因为数据拼接带来的性能损耗在容量增长以后非常可怕，可能会带来50%以上的额外cpu消耗和时延成倍的增加。
                        2. 到此还不算完，EMC更精巧的还在后面。由于VMAX主要承载客户关键业务，性能的稳定性是第一需要保障的，因此EMC推出了Activity Based Compression (ABC) 机制。简单来说就是热数据不压缩，直接下盘，直接读取，不用经过压缩和解压缩流程。这个思路我们大家都能想到，但是EMC不一样得是，将自己分层存储（FAST）的热点计算功能直接完完全全的继承了过来，根本不用添加额外的大的改动。
                        3. Good design. Very smart.

                2. 浅谈重删压缩之三netapp的优化 - 太平说存储    [2017]
                   https://mp.weixin.qq.com/s/Xr1rRNdCB2DfoPoTKC7tGg
                    1. 为了改善压缩率，netapp在该版本新增了一个功能，国内叫做压紧。将多个小块合并成一个4KB的块来存储。这个操作很有效，毕竟每个块的元数据只存储一个地址和偏移量，压紧不会增加任何元数据的开销，只是需要刷新一下原来的元数据即可。
                        1. Interesting. Can be compared with "EMC VMAX软件巧手设计"
                    2. 所有指纹数据仅仅在缓存中存储一份，不做持久化。在重启和升级过程中，指纹会被丢弃。或临时存到硬盘上一份。引用计数和指纹需要进行解耦才能更好的实现。
                    3. 很多人认为重删会导致数据丢失的风险。所以我们不可避免的都需要做逐字节比对，在这种情况下，netapp给我们做了一个很好的表率，那就是我们使用弱哈希，节省指纹表空间，扩大指纹数。使用强哈希不做比对的厂商未来根本没法在市场上被接受。
                    4. 在2015年之前在SAN领域netapp就是一个落后者，在全市场领域更完全是个失败者。但是通过2016/2017年的持续优化，竟然翻身了，非常让人不可思议。其实他只做对了一件事，将压缩重删实现了，同时开启后性能下降在可控范围内（5%~20%）。就这么一条，就让netapp如今在全闪存市场逆势上扬。

                3. 浅谈重删压缩技术之HPE Storserv - 太平说存储    [2017]
                   https://mp.weixin.qq.com/s/skVXps5GtApazYnh2vrZEQ
                    1. HPE最出名的就是他第一个提出精简配置这个概念（Thin Provisioning）
                    2. HPE重删架构的优化
                        1. 主要的方式是，新数据全部写入到LUN的私有空间，除非是发现了可以重删的数据才会从私有空间转移到DDS（shared space）,这样DDS里面的数据存储量就会非常少，所以DDS Table的元数据也会比较小。可以大幅提升重删数据量
                            1. 我理解到了一定程度存储厂商都是牺牲重删率来保性能，那么采用这种模式现在重删域就会大得多。
                            2. 相对于老版本来说重删率有小幅下降，但是下降不多。效率确提升了很多，因为元数据量大幅降低。原来99.999%以上的数据都是存储在DDS的，现在只有少量。
                            3. 按照HPE的分析，一般可以重删的数据仅占重删后数据空间的10%
                        2. 第二步就是做了一个查找性能的优化。
                            1. 用了一个两级hash的校验。前32-bit先查找，相对于完整的指纹查找要快的多。如果命中，则再进行一次hash比对，这次用的是一个64bit的hash。如果两次都命中，才会去后台读取数据。
                        3. 第三步是支持了DDS空间整理
                            1. 对于DDS里面的垃圾空间支持进行碎片整理，提升效率，整个整理过程对于上层的LUN来说是透明的。
                        4. Interesting optimizations
                    3. 压缩数据打包 - 解决变长块问题
                        1. HPE的压缩采用LZ4算法，和大多数厂商一致，不过他的处理机制是先重删后压缩。
                        2. 数据补齐成2KB的整数倍再打包，打包时添加额外元数据，放在包头。包头的元数据为一个256bit的数据包。
                            1. Good design, Can be compared with "EMC VMAX软件巧手设计".
                            2. 有元数据有一个非常好的方式就是可以支持数据的原位置的更新写

                4. 浅谈重删压缩技术之五 HDS软件重删压缩之路 - 太平说存储    [2017]
                   https://mp.weixin.qq.com/s/a4-9rBguDC9rbn5FWVnXkA
                    1. 在OLTP场景硬件压缩几乎没有任何性能损耗

                5. 浅谈存储重删压缩之厂商点评篇 - 太平说存储    [2018]
                   https://mp.weixin.qq.com/s/Y0WVNdjochIs2HupGC95Cg
                    1. 指标
                        1. 数据缩减比，性能损耗（IOPS、Throughput、Latency）
                        2. 场景：数据库、VDI、服务器虚拟化
                    2. 数据缩减比
                        1. EMC: EMC一般数据库按照2:1承诺，混合场景一般按照1.6~2.5这样一个范围进行承诺
                        2. HPE: 数据库2:1，虚拟化1.5:1，VDI 2.5:1
                        3. Netapp: 数据库2:1，服务器虚拟化 2:1，VDI 3~5:1
                        4. HDS: 我们看到市场项目中HDS其实是在1.6~2:1之间
                        5. IBM: IBM依然宣传的非常霸气：数据库场景他宣称4：1，VDI场景宣传48:1（全克隆场景其实并不高），对于服务器虚拟化场景也可以宣传2~9:1

                6. IBM存储重删压缩技术分析（一）-  太平说存储    [2018]
                   https://mp.weixin.qq.com/s/nd6N-A-T71bj_QyrcaBtLQ
                   IBM重删压缩技术之二 压缩性能 - 太平说存储    [2018]
                   https://mp.weixin.qq.com/s/vbFPVlN4qTaiaJGNptEhzA
                   IBM存储重删压缩技术之三 从落后到领先 - 太平说存储    [2018]
                   https://mp.weixin.qq.com/s/j1lf3xHUeAmWK5gzEB0Ueg
                   IBM存储重删压缩技术之四回归硬件 - 太平说存储    [2018]
                   https://mp.weixin.qq.com/s/2uhylHjL5oTKcof8cVCB7w
                    0. By article author, IBM compression/dedup is among the top in industry commercial storage.
                    1. IBM SVC的压缩实现 - Random Access Compression Engine (RACE)
                        1. 输入是不定长块，输出是定长块。数据读取、索引、垃圾回收大幅简化。
                            1. Good interesting design.
                                1. Can be compared with "EMC VMAX软件巧手设计". Search the keyword to get full collection of different dedup/compression approaches
                        2. 预判决机制（Predecide mechanism），如果压缩率不高则不压缩，避免浪费CPU。实现通过抽样。
                        3. 基于时间的压缩法（temporal compression）
                            1. 应用写入位置不能反映数据相关性，而相近的写入时间则可以。例如同样的数据在多个应用程序间同步。
                            2. 实现：将时间相同（一般按照Cache中的代次）的几个数据放在一个作用域，那么压缩率可能会带来明显的提升。
                            3. Good optimization
                    2. 压缩重删如何优化性能
                        1. IBM V840加速实现
                            1. 所以老一代的V系列闪存主要通过专核专用、压缩卡加速、内存独占来进行压缩性能的保障。
                        2. Flashsystem v840压缩性能
                            1. 场景
                                1. 大IO顺序写 - OLAP
                                2. 顺序小IO
                                3. 随机小IO - 全闪存应用的主要场景，主要用于生产业务数据库
                    3. IBM A系列的重删压缩实现
                        1. Pattern matching and removal（特征匹配重删）
                        2. 数据的hash指纹全部存储在内存中，分为段Segment。指纹匹配优先检索本地的段，然后才检索其它段。
                        3. 8KB的定长匹配，4KB的滑动窗口匹配。
                    4. IBM的硬件压缩实现
                        1. 采用ASIC而是使用FPGA，意味着它可以快速的开发上线。使用FPGA实现了关于颗粒的管理、垃圾回收、FTL等，在最新版本也实现数据的压缩和解压。


2. 搜索召回 | Facebook: 亿级向量相似度检索库Faiss原理+应用 - 魔法学院的Chilia
   https://zhuanlan.zhihu.com/p/432317877
    1. 倒排乘积量化(IVF-PQ). Interesting.

3. PolarDB 索引前缀压缩 - zeromean
   https://zhuanlan.zhihu.com/p/703425796
    1. MySQL 官方原生的两种压缩能力：表压缩和透明页压缩
       由 MySQL 向外扩展来看，针对:（1）动态（update-in-place）或静态（append-only）数据；（2）行存或列存组织组织（数据同质性不同）；（3）有序链或无序堆组织的数据（数据局部性不同）等不同情况，能适用的压缩方法也是不同的，并且压缩能获得的效果会有很大差异。
    2. PolarDB 前缀压缩（Index Prefix Compression）
        1. OLTP 中为了支持多种访问路径，比较常见的情况是在一个表上建立非常多的索引，这就导致索引在数据库整体存储空间中占了很大比例。索引存储占到 50% 以上的实例并不少见，这些实例通常在单表会有几十个二级索引。
        2. 由于索引的 key 部分数据存在有序性，因此对索引 key 部分进行前缀压缩往往可以取得不错的压缩效果。采用前缀压缩，可以有效减少 btree 索引的节点数量。
        3. 值得一提的是，部分商业数据库在实现 non-unique index 时，一般会将相同的二级索引对应的主键索引聚集存放, 这样二级索引 key 部分的数据只需要存一份（Duplicate Key Removal）。而在 InnoDB 中的实现较为简单, 每个二级索引 record 为重复的二级索引 key 字段加不同主键 key，这加剧了 InnoDB 索引数据膨胀的问题。
    3. 压缩元数据的设计
        1. 可以依赖前面的记录作为前缀压缩的 prefix base，...，但由于 InnoDB index 的 update-in-place 导致 record 是动态的，...，因此，PolarDB 这里采用的是半静态 prefix base 设计。...。一旦某个版本的 symbol table 确定之后，除非发生完整的 symbol table 更新，其内容是不会进行修改的，因此我们称之为半静态的。
    4. 场景
        1. IO Bound 场景
        2. CPU Bound 场景
        3. 压缩率
    5. My questions
        1. "注意，不同灌数据方式会导致不同的压缩率"
            1. Interesting possible optimization is pointed out on prefix compression

4. 一名数据库工程师的成长，写在Milvus 进入DB-Engines前一百之际 - 几点 James
   https://zhuanlan.zhihu.com/p/707469569
    1. 最近看了一篇文章，很是喜欢，姑且定义为一个数据库开发的自我修养吧：
        对细节的敏感性，颗粒度决定感知力
        培养从繁复的细节中找到关键的直觉
        过程主义而非结果主义，关注逻辑而非结论
        与不确定性共存，尝试定义问题
        勿忘初心
    2. 在这些方针的指导下，我们开始集中精力解决成本、扩展性和搜索质量等关键问题，并集中精力投入企业级功能，比如备份，安全，跨机房容灾，这些都是我们第一个在向量数据库中放出的能力。

5. Facilitating the Efficiency of Secure File Data and Metadata Deletion on SMR-based Ext4 File..——论文泛读 - 妙BOOK言
   https://zhuanlan.zhihu.com/p/708223818
    1. Interesting topic. Secure date deletion requires overwrite, but how should it work on SMR?

6. Don't Put a Cache in Front of Database - 大家好大家吃了吗
   https://zhuanlan.zhihu.com/p/704960840
    1. 原文：7 Reasons Not to Put an External Cache in Front of Your Database
       https://www.scylladb.com/2017/07/31/database-caches-not-good/
        1. We at ScyllaDB put a lot of effort into making our internal embedded cache rock.
        2. Key reasons
            1. An external cache adds latency.
            2. An external cache is an additional cost.
            3. External caching decreases availability.
            4、 Application complexity — your application needs to handle more cases.
            5. External caching ruins the database caching.
                1. Interesting
            6. External caching isn't secure.
            7. External caching ignores the database knowledge and database resources.
        3. My questions
            1. Why in today's Internet companies the main trend is MySQL + Redis? Rather than MySQL internal cache.
            2. There are different opinions
                1. Redis MySQL: 3 Reasons Why Your MySQL Database Needs Redis
                   https://redis.io/blog/3-reasons-your-mysql-db-needs-redis/
                    1. Key reasons
                        1. Maintenance cost of MySQL Query Cache
                        2. Forced to use the same data type of SQL statements. 
                        3. Forced to work with SQL statements. And optimizing SQL statements
                        4. MySQL performance on secondary indexes is infamously poor
                        5. The scaling pain of caching itself
                        6. Monitoring needs for the right size of caching resources.
                        7. Caching analytics, metering, and rate limiting.
    
    n. Related materials
        1. 2017双11技术揭秘—分布式缓存服务Tair的热点数据散列机制
           https://developer.aliyun.com/article/316466
            1. Tair的数据分片和路由算法采用了Amazon于2007年提出的一种改进的一致性哈希算法[4]。
                1. Then how to deal with hot data? This is a good topic right by this article to ask for consistent hashing based placement.
            2. Key solutions
                1. 热点识别
                    1. 支持用户预标记
                    2. 热点统计
                        1. DataServer收到客户端的请求后，由每个具体处理请求的工作线程（Worker Thread）进行请求的统计。
                        2. 工作线程用来统计热点的数据结构均为ThreadLocal模式的数据结构，完全无锁化设计。热点识别算法使用精心设计的多级加权LRU链和HashMap组合的数据结构，在保证服务端请求处理效率的前提下进行请求的全统计，支持QPS热点和流量热点（即请求的QPS不大但是数据本身过大而造成的大流量所形成的热点）的精准识别。
                        3. 每个采样周期结束时，工作线程会将统计的数据结构转交到后台的统计线程池进行分析处理。统计工作异步在后台进行，不抢占正常的数据请求的处理资源。
                2. 读热点方案 - 二级的Cache模型
                    1. Each DataServer adds a new HotZone. For a hot key, Tair Client will map it to a HotZone. The mapping is based on hash, 每个客户端只访问唯一的HotZone区域
                    2. A hot key will be effective for N seconds, and then expire from HotZone. Tair Client reads HotZone first, and then fallback to DataServer normal storage.
                    3. My questions
                        1. From Alibaba's analysis in this article, the hashing in vanilla consistent hashing placement doesn't well solve the hotness imbalance issue.
                        2. Consistent hashing supports replicas. Why not simply use more replicas for a hot key?
                            1. From ChatGPT: https://chatgpt.com/share/bc66136c-a2bc-4706-8cb0-14b9ab419b42
                                1. Replication:
                                    1. Replicating hot keys across multiple nodes can distribute the read load.
                                    2. Writes can be more challenging to handle with replication but can be managed with quorum-based approaches.
                        3. How can we introduce the live migration / load balancing into consistent hashing based placement?
                3. 写热点方案 - A write coalescing cache
                    1. DataServer runs a new 热点合并线程. The thread will batch the updates for hot keys, and then periodically flush to storage engine.
            3. Tair background
                1. Tair是阿里巴巴集团自研的弹性缓存/存储平台，在内部有着大量的部署和使用。Tair的核心组件是一个高性能、可扩展、高可靠的NoSQL存储系统。目前支持MDB、LDB、RDB等存储引擎。其中MDB是类似Memcached的内存存储引擎，LDB是使用LSM Tree的持久化磁盘KV存储引擎，RDB是支持Queue、Set、Maps等数据结构的内存及持久化存储引擎。

7. 转行只有0次和无数次 - Rand Xie
   https://zhuanlan.zhihu.com/p/701554123
    1. Good experience

8. 会议Rebuttal的一些整理和思考 - Liquidfrog
   https://zhuanlan.zhihu.com/p/696874676
    1. Useful

9. 国产数据库生态漫谈（上） - 赵伟
   https://zhuanlan.zhihu.com/p/706257240
    1. 如何理解国家的信创和新基建需求
    2. 首先，有不少是从各个大厂（包括Oracle，微软，IBM，EMC，Teradata等公司的中国研发团队，以及华为、阿里、腾讯、百度、蚂蚁、中兴、京东等IT和互联网大中厂商）出来创业的团队。
    3. 国内的基础软件初创厂商应该勇于靠自己的产品力和技术实力来在全世界获得客户和收入
    4. 这一切的技术进步及其应用都与数据紧密相关，都需要管理和利用越来越多的数据，因为本质上数据是人类认知的精确表达

10. MCN公司 — 很可能是未来的尖端量化投资公司 - DWill
    https://zhuanlan.zhihu.com/p/701127693
    1. good insight
    2. 可能让很多人吃惊的现实——传统的量化投资公司已经被MCN公司（你可以理解为就是做抖音短视频的公司）超越了。以下3点是MCN公司内容制作的事实：
        1. 很多MCN公司为了刺激关注度和内容热度，早已经在抖音、小红书等内容平台上以天、半天、小时为单位更新投放策略，2年前按季度、按年做策略的时代已经因为技术迭代而大大提高投放频率了。相对比，量化公司的投资配置方案基本是按月，最快按天更新。
        2. 内容投放策略频率大幅提升的根本是用AI全自动生成内容（文案、短视频）再多IP程序化分发。或者说是用量化投资模型的算法生成内容投放策略，同时AI优化模型并生成文案、图片、音频、配乐、视频内容等再自动化发布；
        3. 这一套内容输出的程序逻辑几乎和量化交易模型一模一样！他们用的是A100的80G显卡保证制作效率，跑的是量化策略，用的是ROA（资产回报率）模型生成投放策略。
        4. 用海量内容从流量平台换来钱，现金流充裕且算力牛B plus，完全可以满足用一套运营逻辑一边跑二级市场，一边跑公域流量平台。一边可能有风险，但一边几乎就是无风险套利，还是暴利！所以很多MCN公司已经成为很棒的量化基金公司了！
    3. 打败你的往往不是你的对手，颠覆你的也不是同行。
        1. 传统捧IP立人设拍剧集的MCN公司打死想不到AI＋ROA会抓取并copy我的各种元素甚至是节奏，１小时内用N个IP账号在N个平台上发布至少10个变种内容，然后１小时内被至少5000万人看到……我被量化对冲基金公司的模式搞死了……
        2. 量化基金公司也打死想不到，我们玩了命的做行情做局编故事弄报表，各种套利对冲，各种调研掉头发，就是为了得到投资人的青睐而和同行一起卷卷卷！结果搞死我们的是流量变现的MCN公司，而且人家搞死自己还是"捎带手"的事！还是人家单一广告投放部门就可以。

11. 深度粗排在天猫新品中的实践 - 沪漂城哥
    https://zhuanlan.zhihu.com/p/627107816
    1. 粗排与精排阶段的差异
        1. 待打分数量不同
            1. 粗排需要对上千上万个商品进行高效打分，模型一般不能过于复杂，推理耗时要求较低
            2. 精排仅需对上百个商品进行打分，模型一般相对较大，推理耗时可以相对较高
        2. 模型结构不同
            1. 由于待打分数量不同，导致粗排性能要求较高。在召回引擎BE的优化下， 粗排一般采用双塔结构，如DSSM，user tower和item tower在最终上层决策层进行高效交互计算，如内积等形式，且模型中user tower和item tower无法在底层进行直接的显式交叉
            2. 精排一般采用复杂模型的思路，超长序列建模、特征交叉与增强等，如 SIM[4]等，且已被验证有效的用户和商品交叉特征在模型底层即可进行
        3. 样本空间不同
            1. 粗排待打分候选集较大，主要结合用户历史兴趣点在业务商品总底池的多路召回的结果，理论上应远大于点击曝光日志中的样本空间
            2. 精排待打分候选集来自于粗排打分倒排截断后的结果，空间相对较小，且存在一定的选择偏差影响

12. 机器学习科研的十年 - 陈天奇
    https://zhuanlan.zhihu.com/p/74249758
    1. XGBoost, TVM, MXNet

13. 计算机视觉 | 哥大读博五年总结（全） - Mike Shou
    https://zhuanlan.zhihu.com/p/338193330
    1. 我觉得这段经历，对新手很有参考价值，很多时候光努力不够，方向更重要。新手如何选博士几年的topic，有两个问题值得思考：
        1. 能不能快速上手？有几个简单的评判标准：
            1. state-of-the-art的paper有没有开源的代码？目的是你能迅速复现baseline，熟悉整体pipeline（如怎样预处理，后处理），加深对实现和细节的理解
            2. 有没有对这个topic有hands-on经验的师兄，或者community里面approachable的前辈？目的是，当你遇到实现上的细节问题，可以及时咨询和得到反馈
            3. 这个topic有没有比赛，或者标准的benchmark？目的是，有大家已经定义好的数据，实验setup，评价标准；这样，你有可以直接比较的baseline，outperform baseline的时候也容易被人认可
        
        2. 能不能有大的impact？这里我指的是博士期间的大方向，由一系列单项的工作或者paper构成。单篇paper通常有三种类型：（1）First work：开创了一个topic，比如RCNN于object detection（2）Last work：基本解决了一个topic，比如Faster-RCNN，YoLo于object detection（3）Improve类型，介于First和Last之间的。
            1. Last很难，Improve常见但影响力不够深远，对于新手而言，博士的早期工作，在有能力做出来和有impact之间的trade-off比较好的，估计是First了，不一定非要是第一篇，只要是某个topic里面开创性工作的那一批之一，都是不错的。
            2. 这个早期工作之后，你会对这个问题哪里要改进，有很清楚的认识，因为improvement room大，也会有很多ideas。同样，早期的时候怎么选这样一个topic呢：相关的比赛是这一两年新开的吗，相关的benchmark是这一两年出来的吗，上面的结果提升空间大吗（现在是20%还是已经80%了）？

    2. 单篇Paper选题
        1. 著名的Heilmeier问题系列，是指导老师们申项目的
            1. What are you trying to do? Articulate your objectives using absolutely no jargon.
            2. How is it done today, and what are the limits of current practice?
            3. Who cares? [Support other's research? Shape research landscape? Power applications in industry?]
            4. What's new in your approach and why do you think it will be successful?
            5. If you're successful, what difference will it make? [e.g. Contributions in theory/modeling? Improve accuracy by 5% on dataset A, B, C…?]
            6. What are the risks and the payoffs? [Further, how would you mitigate the risks? If your proposed method does not work, what could be alternative design? These can end up as discussions such as ablation studies in your paper.]
            7. How much will it cost? [e.g. How many GPUs do your experiments require? How long is each training process? How about data storage?]
            8. How long will it take? [How many hours are you going to work on this per week? When is the submission DDL? Can you make it?]
            9. What are the midterm and final "exams" to check for success?

    3. 之后几年，从导师身上学到了很多presentation的技巧：
        1. 如果可能的话，事先了解你的听众背景，是跟你做同一个topic的，还是同一个大领域但不同topic的，还是完全其他专业背景的。需要根据听众背景，定制和调整：比如，需不需要多介绍些背景？需不需要更深入技术细节？等等
        2. 一页slide尽可能focus在一个点上，不要信息量过大，否则听众很容易lost
        3. 尽可能多用图片表达，不要大段大段的列文字，A picture is worth a thousand words
        4. 上面这两点，其实principle都是尽量让要讲的内容简单明了，因为很多时候我们在听talk，这样被动接受的时候，接受新知识的能力是比主动接受时候（比如看paper）低的。
        5. 当听众问问题的时候，If you don't know the answer, just say don't know.
        6. 如果是跟mentor日常讨论的slides，因为会讨论到很细节的东西，有些图PPT画起来，很花时间，而且通常这样细节的图还挺多，所以可以就ipad上面手画一画，截个图放到PPT里就好了；如果是正式一点的presentation，写slides跟写paper的principle有点像，不要太focus在细节上，更重要的是讲清楚motivation，为什么这样设计，细枝末节的不关键的内容，放在backup slides里面。

    4. 谈谈写paper
        1. 先给一个Talk。写paper最难的是构思storyline，而最好的完成这一步的方法就是先对你的工作做一个slides，给周围的人present一遍。这个过程中，你会梳理好自己的思路，画好文中的figure，准备好实验结果的table，周围的人还可以给你提意见，帮助你完善，等这个talk给完了，后面写paper就会顺畅自然了。其实我现在，如果准备投一个paper，当做了一段时间后，就会按照最终presentation的思路，准备slides，用在每周给老板们report时。开头先快速review一下做的task和提出的方法，remind一下context，然后重点focus在那周做的新东西上，所以每周汇报的slides可能80%都是跟上一周一样的，然后新的方法和实验结果的那几页slides是新的，有比较多的细节。
        2. 用Google doc做语法检查。刚写好的paper有typo和语法错误是很难避免的，但常常会被reviewer揪着不放。大家写paper如今大都在overleaf上，但overleaf的查错还是不够好，建议可以写完paper后，贴到Google doc里面。几年前开始，估计是由于deep learning对Google NLP的改进很大，感觉Google自动改的质量已经非常高了。
        3. Rationale很重要。不光是要讲清楚你怎么做的，更要justify你问什么这么做；不光要讲你的结果比baseline好，更要解释为什么好；读者看到的不应是一个"使用手册"。有时候我们写paper，花了很多篇幅写了很多实现细节，但是更重要的是，解释"为什么"，这个背后的逻辑和insights。
        4. 大部分paper都是提出一个新的方法，这类方法型paper似乎都可以套下面这个框架：
            Introduction：可以分为以下几个部分：
                Problem definition
                Previous methods and their limits
                简单描述你是提出了什么技术来overcome上面的limits
                一个图，非常high-level的解释前人工作的limits和你的工作怎么解决了这些limits，最好让人30秒内完全看懂
                最后一段如今大都是，In summary, this paper makes three contributions:
                    First work to解决什么limits
                    提出了什么novel的技术
                    outperform了state-of-the-art多少
            Related Work：一般三五个subsection，分别review下相关的topics，同样不光讲previous work做了啥，更要讲自己的方法跟前人工作有啥不同
            Method
                这是文章的主体，按照你觉得最容易让别人看懂的方式来讲
                可以第一个subsection是overview，formulate一下你的problem给出notation，配一个整体framework的图，图里面的字体不能太大或者太小看不清，要有些细节，让人光看图就能明白你的方法是怎么回事，但不要过于复杂，让人在不超过2分钟的时间看完这张图
                然后几个subsection具体介绍你的方法或者模型；如果testing跟training不太一样，最后一个subsection介绍inference时候的不同，通常是一些post-processing操作
            Experiment
                Datasets
                Implementation details such as pre-processing process, training recipe
                Evaluation metrics
                Comparisons with state-of-the-art
                Detailed analysis
                    Alternative design choice exploration
                    Ablation studies
                    Visualization examples
            Conclusion (and Future Work)
            Abstract：是全文的精简版，建议在paper写完第一稿差不多成型了，有定下来的成熟的storyline了，再去写abstract；大概就是用一两句话分别概括paper里面每个section，然后串起来

        5. 另外paper提交时候，可以交supplementary materials，虽然reviewer并不被要求强制看这个，但其实给我们机会，去include更多文章技术细节、实验结果的好地方；在后面rebuttal阶段，通常篇幅有限制，但如果你已经在supp里面未雨绸缪，可以省很多空间，refer reviewer去看你supp里面的内容就好了。

        6. 怎么样才能做的尽量完善，减少迭代次数呢？我的一个经验是，这种项目，尽可能involve多的experienced experts参与讨论，及时跟大家沟通，collect不同人的想法。

    5. 找教职的话，qu qing学长写了个总结，非常全面，强推
       https://qingqu06.github.io/pdf/Job_Search.pdf

    6. Change topic every 5 years
        1. 毕业那会儿，导师说他刚毕业来哥大时，师爷跟他说，you need to change topic every 5 years。感觉很有道理。
        2. 如果在博士开始那会儿，开始做一个topic，做了5年，基本这个topic就会饱和了，很难再有大的impact。
        3. 如果是转production，转business，那本身就是很不一样的topic了。

    7. Principles For Success by Ray Dalio
       https://www.youtube.com/watch?v=B9XGUpQZY38

14. 博士第五年 - YY硕
    https://zhuanlan.zhihu.com/p/631748171
    1. 我在大疆工作时形成了一些固定的思维方式，认为开发机器人的目的是为了让它更快更高更强，所有的科研应该为大幅提升机器人的性能、或者增加全新的功能来服务；如果机器人的一个功能可以用简单的方法实现，就不需要用复杂的数学理论来重新实现。
       后来我发现科研其实是反过来——开发新的数学理论和工具，用某一种机器人证明这种新的理论和工具有用，即使机器人只是重新实现了一些已经被别人实现出来的功能。

15. 工作五年反思 - 李沐
    https://zhuanlan.zhihu.com/p/374777591
    0. MXNet
    1. 决定优先级应该是根据事情的价值。我现在评估一件事的价值是它对社会的价值，用公式来写就是
        1. 受益人数 x 人均时间 x 单位时间价值差
    2. 领导者是带路者，需要有好眼光。管理者是后勤官，让团队执行高效。
        1. 放眼在三年以后
            1. 领导者最重要的是在带着团队探索未知领域时找出正确的方向。也就是说保证你们做的产品或技术是有价值的。
            2. 只有在快速变化的赛道上，新入局者才更容易通过更准确的预测未来的价值来弯道超车。也就是乱世出英雄。
            3. 好的眼光需要一个长期的训练。你需要不断的去做深入思考，获得自己独特的观点，而不是靠朋友圈里大家的高见。所以你需要时不时放下手头的事情，给自己空出时间做深入思考。
        2. 管理的核心是诚心待人
            1. 如果你有一个明确的团队目标，和一个高质量的团队，高效执行是水到渠成的事情。所以管理者有三个核心事情：招人、留住厉害的成员、和帮助落后的。
            2. 招人最理想是招比自己厉害的人。另外是每次招的人都比同级别的一半人厉害，这样能保证团队扩张时能不断提升团队质量。
            3. 能力突出的成员在哪里都会受欢迎。你的一个任务是让他们能尽可能长的留在团队里（虽然最终是要走的）。
                1. 一个办法是把自己放在他们的位置，想象你想你的领导如何待你。例如我自己最希望的是不断做有更大价值的事情（成就感），并从中学到新东西（个人提升）。在我困难时候老板能给与支持（经常发生）。
                2. 其他的都可以换算成当前待遇，例如可以多少时间做不喜欢的事情（不赞同一件事的价值，但又没能说服别人不做）、上下班路上很堵、食堂没中餐。
                3. 所以大方向上是创造轻松的环境、每年能新立项有价值的项目、和尽量给大家争取待遇。
            3. 对于绩效不理想的队员，你需要经常性的指出问题并给予建议，如果一段时间没改进则需要讨论是不是当前项目不合适。如果仍然无进展的话，那只能帮助他们换组，或者要求他们离开。
                1. 同样，你需要把自己代入对方的位置，明白想得到什么样的帮助和尊重。绝大部分时候，不是他们人不行，只是你们不合适。
                2. 愉快的分手能让前成员更快的找到更合适的职位（从而避免他们给你寄刀片）。
        3. 专注！专注！
            1. 有人说创业公司一个常见死因是在有了一定成绩后盲目扩张。这个在哪里都成立。
            2. 不管你是一个人，带一个团队，还是领导一家公司，资源总是有限。集中资源在最有价值的事情才能保证成功。
                1. 例如苹果好几十万人，但对于产品线的扩张上非常谨慎。从而能保证每一款产品都砸上足够多资源来颠覆市场。
                2. 因为同时把做几件类似的事情最好，不如只把一件事情做到极致、做到市面上最好。这样你总是可以得到正的价值差。一个第一比十个第二好，第三通常都活不长。同样的道理也可以用在生活、社交、和学习上。
            3. 在初期你也许可以广撒网多捕鱼，一旦事情的价值慢慢清晰，我们需要逐步集中资源。
        4. 升职
            1. 我因为运气不错升到了一个比较高的职位，从而有机会经常参加公司的从高级工程师、科学家到总监的升职评定。
            2. 虽然公司、职位、级别不同带来差异性，但总体来说，一个人能否升职成功取决于她做的最大项目对公司的价值是不是达到这个职位的要求。这里有三个要点：
                1. 一是项目对公司的价值。意味着针对的人群和价值差都是公司关心的，而不是你个人或者社会关心的。这里价值通常就是给公司赚了多少钱，或者3-5年后可能会赚多少钱。
                2. 二是看的是你最大的项目要够"档次"。累积很多项目，想通过不看功劳看苦劳升职可能是行不通的。
                3. 三是你在项目中的贡献，例如你负责多大一块，是贡献了代码、团队协调、宣传、制定计划、还是申请到了资源。
                4. 一个常见误解是跟人合作会降低我的贡献。如果你和合作者配合不好，导致1+1远小于2，那么你的贡献确实降低了。但如果通过合作把项目价值做大了，那么你分到的贡献是不会少的。特别是如果项目价值上了一个档次，那就更好了。

            3. 升职有一个经常被忽略的"潜规则"是影响力。随着职位的升高，公司对你的影响力的期望也越高。从能影响一个小团队，包括制定技术路线、帮助队员上手、解答疑惑、甚至是帮助别人来完成工作，到影响隔壁组（经理），影响隔壁部门（高级经理），影响隔壁集团（总监），最后到影响整个公司战略（副总裁）。
                1. 除非你是天生的领导者，不然你得花力气去培养自己的影响力。简单来说是在管好自己的事情外，积极的去帮助别人。当别人信你、咨询你意见、愿意找你合作时，那你就有了对他们的影响力。
                2. 你可能会觉得帮别人会耽误自己的活。但从公司角度来看，是需要鼓励这种奉献精神，而且要予以奖励。此外，你从中赢下的信任给你带来名声和人脉，长远来看是很有用的。

            4. 不同级别的薪酬中值通常是个等比序列，而不是等差。例如比你高一级的人可能工资比你多一半，但高三级的人不是比你多150%，而是多238%。
                1. 在这个模型里，你需要优化你的五年后，或者十年后能到达的高度。所以在比较offer时，你不要太关心它们之间的数字差价，而是关心去你去了之后的发展

16. MSRA 读博五年（一）从小白到第一篇 SIGCOMM - 李博杰
    https://zhuanlan.zhihu.com/p/647940948
    MSRA 读博五年（二）自己主导的第一篇 SOSP
    https://zhuanlan.zhihu.com/p/647942394
    1. MSR, KV-Direct, Catapult FPGA

17. 真的假的！有个物联网公司通过自建数据库省了 98% 的云成本？！ - 小猿姐
    https://zhuanlan.zhihu.com/p/691495959
    1. Sources: 
        1. How we've saved 98% in cloud costs by writing our own database
           https://www.reddit.com/r/programming/comments/1bvzfhr/how_weve_saved_98_in_cloud_costs_by_writing_our/
        2. hivekit.io: How we've saved 98% in cloud costs by writing our own database
           https://hivekit.io/blog/how-weve-saved-5000-percent-in-cloud-costs-by-writing-our-own-database/
        3. Saving cloud costs by writing our own database (hivekit.io)
           https://news.ycombinator.com/item?id=39929185
    2. Replaced $10K/month AWS Aurora to $200/month AWS EBS + custom data structure

18. 数据库公司究竟能赚多少钱？是怎么赚的？
    https://zhuanlan.zhihu.com/p/706406979
    1. 数据库公司究竟是怎么赚钱的？这些企业的收入大部分来自前两项。
        出售软件许可，让客户能在云上或者自己的硬件上运行软件（Snowflake例外，因为他们只提供云服务）
        提供云服务的订阅
        推出高级套餐，包括特殊支持、培训、课程和提前使用某些功能
        提供专业服务，比如咨询服务
        建立合作伙伴关系和其他收入来源
    2. 此外，MongoDB目前60-70%的收入来自其托管服务Atlas，这也是增长最快的部分。Elastic的Elastic Cloud占他们收入的35-45%，增长速度也不慢。至于Snowflake，几乎所有的收入都来自云服务。
    3. 2022年，DBMS市场增长了14.4%，达到910亿美元。云数据库服务几乎包揽了所有增长，云支出（55.2%）超过了本地（44.8%）。非关系型数据库和关系型数据库分别增长 26.8%和 12.2%，而前关系型时代的数据库下降 10.1%。
        1. DBMS市场规模，Gartner估计为910亿美元，是企业软件领域最大的市场之一（甚至可能是最大的）。
        2. 云支出超过了本地支出，并且增长更快。

19. 公有云多云管理，食之无味，弃之可惜！ -  云原生Lab 
    https://mp.weixin.qq.com/s/pAqgTh0jhMV5lKXU9t6T_g
    1. Gartner对CMP给出的定义是：CMP（Cloud management platforms，云管理平台）是一种管理公有云、私有云和混合云环境的整合性产品，
        1. 其最小的功能范围应该包括自服务界面（self-service interfaces）、创建系统镜像（provision system images）、监控和账单（metering and billing），以及基于策略的一定程度的负载优化（workload optimization）等。
        2. 高阶功能也包括了整合外部已有的企业管理系统，包括服务目录（service catalogs）、存储和网络资源配置，更高级的资源管理和监控，比如客户机性能和可用性监控等。
    2. Gartner于2019年发布报告《Critical Capabilities for Cloud Management Platforms》中指出，
        1. CMP具备的7个关键能力包括：资源提供与调度、云资源配置与分类、服务管理、监控与分析、云成本管理与优化、云迁移和容灾备份、身份认证和安全合规性。这也成为了客户在采购CMP产品时作为参考性建议的主要来源。
    3. 公有云CMP的商业悖论
        1. 因此，市场上交付给客户的CMP产品，似乎变成了最小公约数与最大公倍数的取舍，前者客户满意度极低，后者却带来了极重的交付成本。
        2. 而想要让用户在体验上得到提升，在执行上就必须抛开所谓All in One的宏大概念，去解决真实场景中那些细枝末节的问题。
        3. 那么在云原生时代的多云管理最佳实践，也理应面向开发者，以应用为中心去建设。

20. HyperLogLog 算法详解 - Abser Ari
    https://zhuanlan.zhihu.com/p/77289303
    1. Redis new data structure: the HyperLogLog
       http://antirez.com/news/75
    2. HLL - Cardinality *estimation* (count distinct)
        1. 集合中每个元素的经过hash函数后可以表示成0和1构成的二进制数串，一个二进制串可以类比为一次抛硬币实验，1是抛到正面，0是反面。
            二进制串中从低位开始第一个1出现的位置可以理解为抛硬币试验中第一次出现正面的抛掷次数k，
            那么基于上面的结论，我们可以通过多次抛硬币实验的最大抛到正面的次数来预估总共进行了多少次实验，
            同样可以可以通过第一个1出现位置的最大值来预估总共有多少个不同的数字（整体基数）。

21. 游戏心理学研究汇总：适用于游戏设计中的72个心理学效应理论（5万字长文慎入！） - 法师猫不凡
    https://zhuanlan.zhihu.com/p/32907455
    0. Very good summary. It has examples for each.
    1. Catalog
        1. 首因效应&第一印象理论
        2. 马洛斯需求层次理论
        3. 斯金纳箱原理
        4. 审美疲劳理论
        5. 情绪心理理论
        6. 纳什均衡理论
        7. 零和博弈理论
        8. 多巴胺&精神分析学与游戏成瘾机制
        9. 边际效应
        10. 霍布森选择效应
        11. 沉浸感理论
        12. 狄德罗配套效应
        13. 门槛效应
        14. 棘轮效应
        15. 齐氏效应
        16. 目标效应
        17. 超限效应
        18. 鲶鱼效应
        19. 思维定势效应
        20. 阿伦森效应
        21. 暗示效应
        22. 贝勃定律
        23. 布里丹毛驴效应&三棱镜效应
        24. 重叠效应
        25. 等待效应
        26. 多看效应
        27. 禁果效应
        28. 凡勃伦效应
        29. 空白&留白效应
        30. 冷热水效应
        31. 鸟笼效应
        32. 心理防御机制
        33. 人际互动效应
        34. 波纹效应
        35. 近因效应
        36. 系列位置效应
        37. 逆向思维
        38. 紫格尼克记忆效应
        39. 恐怖谷效应理论
        40. 成败效应
        41. 色彩心理学
        42. 禀赋效应与沉没成本
        43. 达维多定律
        44. 热炉效应
        45. 反馈效应
        46. 赫洛克效应
        47. 巴图玩家类型分类
        48. 名人效应+权威效应
        49. 从众效应&羊群效应
        50. 韦伯-费希纳定律
        51. 帕累托定律&二八法则
        52. 破窗效应
        53. 出丑效应&仰巴脚效应
        54. 手表定律
        55. 蝴蝶效应&多米诺骨牌效应
        56. 弼马瘟效应
        57. 心理摆效应
        58. 弗洛伊德的人格结构理论
        59. 狮羊效应
        60. 性心理学
        61. 晕轮效应
        62. 同体效应
        63. 莫扎特效应
        64. 搭便车效应+社会惰化效应
        65. 竞争优势效应
        66. 古烈治效应
        67. 奖惩效应
        68. 长尾效应
        69. 路径依赖定律
        70. 人际交往五定律
        71. 投射效应
        72. 移情效应

22. clickhouse到底有哪些吊炸天的优化？ - 禹鼎侯
    https://www.zhihu.com/question/446288242/answer/3290601554
    1. MergeTree, part, partition
    2. 稀疏索引。e.g., 8192条数据才会创建一个索引项目
    3. 物化视图，创建projection
    4. 二级索引

23. 从一到无穷大 #30 从阿里云盘古的屠龙之术看使用blob storage作为统一存储层的优势 - 大家好大家吃了吗
    https://zhuanlan.zhihu.com/p/706218967
    1. 在[3]的评论区中张威大佬提到BG3的存储层已经从kv更换为类似盘古的append only blob系统
        1. 其本质原因是LSM类系统一般为了稳定运营需要预留cpu/内存/存储IO带宽，这会造成qps/gb非常有限，存储利用率无法提升，横向扩展成本较高；其次分布式kv系统并非对计算没有要求，公有链路编解码，一致性协议，wal（写文件系统），memtable，cache等对于磁盘之外的资源消耗也不能小觑。
        2. 这就导致使用持久化kv类系统作为其他系统的共有存储层存在成本问题。其次kv系统的优势在于接口的易用性和相对较优性能，并不是成本和吞吐量。
    2. AWS在kv模型提供三个产品ElastiCache，MemoryDB和DynamoDB，分别占据性能/可靠性/成本效益。而阿里云提供Redis社区版，Tair性能增强性和Tair容量存储型，聚焦性能。

    n. Related materials
        1. [3] 从一到无穷大 #29 ByteGraph的计算，内存，存储三级分离方案是否可以通用化为多模数据库 - 大家好大家吃了吗
           https://zhuanlan.zhihu.com/p/704956012
            1. Logged elsewhere

24. TCHouse-C 实时数据更新的技术选型与工程实践 - DataFunTalk
    https://zhuanlan.zhihu.com/p/710490606
    1. 实时数据更新场景
        1. 第一类是对数据进行高频的增删改查。
        2. 第二类是利用部分列更新能力构建大宽表。
    2. Existing solutions
        1. ClickHouse
            1. Mutation 机制
            2. lightweight-update/delete
        2. 数仓领域
            1. Copy-On-Write
            2. Merge-On-Read
            3. Dleta-Store
            4. Delete-Insert
    3. TCHouse-C 实时数据更新方案
        1. Delete-Insert

25. 现代中央处理器（CPU）是怎样进行分支预测的？ - lawliet
    https://www.zhihu.com/question/486239354/answer/3245281606
    0. 本篇文章主要参考Onur课程以及姚永斌老师的《超标量处理器设计》
    1. Random captures
        1. 当流水线级数增加的时候，分支预测失败的惩罚会越来越大
        2. 条件分支指令跳转的目标地址总是保持不变的
            1. 因此我们可以很自然而然的将某一个PC地址对应的分支指令，以及其相应将要跳转的地址，全部存储起来。当下一次再执行到此分支指令的时候，通过其PC进行索引，然后获取其将要跳转的地址即可。
            2. 存储于 BTB 即 Branch Target Buffer
    2. 分支预测器基础
        1. 基于1位计数器的分支预测
            1. 这种方法被称为 last-outcome prediction
            2. 典型例子，for 循环
        2. 基于2-bit饱和计数器的分支预测
            1. "饱和": Strongly taken -> Weakly taken -> Weakly not taken -> Strongly not taken
        3. 基于局部历史的分支预测器
            1. 分支历史寄存器（Branch History Register，BHR），自适应的两级分支预测（Adaptive Two-level Predictor）
                1. 第一级称为局部历史寄存器组合
                2. 第二级称为每个历史条目的饱和计数
            2. 我们将开始讲的BTB和BHR结合在一起，如下图所示，就形成了一个完整的分支预测器。
        4. 基于全局历史的分支预测器
            1. 将分支预测的结果和所有分支的T/NT历史结合起来。相应的我们就需要一个GHR寄存器
        5. 混合分支预测器
            1. 使用超过一种的分支预测器，来获得最好的分支预测结果
    3. 现代分支预测器
        1. 基于感知机的分支预测器
            1. 感知机（Perceptron）在处理线性函数的时候非常有效。可以简单的将其作为二元分类器进行使用
            2. 如果错误则需要使用梯度下降法进行更新w系数，最终趋于稳定。该过程和AI的训练过程是一样的。
            3. 基于感知机的分支预测器非常成功。典型代表是AMD的Zen和Zen2（TAGE加感知机）。
        2. 基于Tage的分支预测器
            1. 该预测器依赖于基础预测器以及由多个标签（Tag）的预测器组件组成的全局预测器。这些组件使用不同的分支历史信息长度进行索引计算，这些历史长度形成几何级数。
            2. 因为通过实际的研究发现，不同的分支依赖于不同的历史长度，从而可以获得最好的预测准确率。
            3. TAGE预测器非常成功，现在的高性能处理器有一大批都以TAGE预测器为雏形。
    4. Q & A
        1. 进程切换的时候, 预测器的上下文状态会保存和恢复吗?
            1. 当然是不会了。上下文的恢复保存需要做很多次访存，而分支预测的作用是避免流水线断流，在前者的巨大开销面前，流水线清空完全无所谓了。

26. Snowflake Auto-Clustering 调研 - 要进屋喝茶吗
    https://zhuanlan.zhihu.com/p/676637725
    1. Key challenges
        1. 在物理上，Snowflake 表结构是由多个数据文件构成，这个数据文件称为 micro-partition（下文简称为 partition）。同时，Snowflake 在 partition 中为每列存储了一种轻量级的索引 zonemap（null/value count, min/max 等统计信息），其中 min/max 统计信息用于在文件级别进行 data skipping，即在 scan 表时，过滤掉不需要读的 partition 以节省 I/O 开销，从而提升读取性能。

           可惜的是，一般情况下用户导入的数据是无序的（特殊：时序数据），导致 partition 之间 overlap 严重，则 data skipping 并不能起到很好的效果。

           所以增强 data skipping 效果最关键的就是减少 partition 之间的 overlap
    2. Snowflake auto-clustering
        1. Snowflake 提出了近似排序的策略，大致思路是：选出最影响整体 overlap 的部分 partition 进行排序重写，以降低平均 overlap 程度。
        2. Concepts: 所以得出真正影响 data skipping 的是 depth，clustering 的目标是尽可能降低整个表的 average depth
        3. Snowflake clustering 使用类似 LSM-tree 的概念，新 partition 的 level 默认为 0，在经过多次的 re-clustering 之后，level 逐渐增大，整个表的数据也更加 well-clustered - See Figure "Clustering Levels"
            1. Partition Selection，选出执行 re-clustering 的 partition 集合
                1. Snowflake 并没有公开 selection 算法，简单来说：level 越小，权重越大，平均深度越大，权重越大，最后结合两者选择出某个 level
                2. 选择出某个 level 后，需要选择该 level 内具体的 partitions。选择算法流程如下：
                    排序所有 micro-partitions 的端点（min & max）；
                    计算出 peak ranges 并计算 overlapping partition 的数量；
                    可以使用 stabbing count array 优化；
                    通过排序 depth 获得 partition list；
            2. Re-cluster execution，对选出的 partition 集合执行排序重写
                1. 将上个任务选出的 partitions 进行排序重写，并且需要将重写后的 partitions 汇入下个 level，整体 overlap 将逐渐减少

27. 自从flink成熟之后，spark是否慢慢成为鸡肋？ - 作者：myasuka
    https://www.zhihu.com/question/306432813/answer/2901618780
    1. 所以我进入工作之后，主要就是在Spark streaming上挣扎了。说是挣扎，主要有如下的原因：
        1. 没有很好的反压机制，当数据激增时，内存激增，Spark集群很容易crash，由于实时作业理论上是一直运行的，但是我印象中当时很难有作业可以稳定地运行超过一个月。
        2. 没有增量checkpoint机制，当数据规模一大时，整个分布式RDD需要持久化checkpoint时，系统很不稳定。
    2. 我觉得Flink可以强于Spark的流式计算引擎（包括后来重构的Spark structured streaming）的原因主要是如下几点：
        1. 进入阿里后，我第一震惊的就是当时阿里已经存在了稳定运行长达一年以上的Blink作业，相比于之前Spark streaming跑一个多月都够呛的情况，无疑是质的飞跃。
        2. 设计理念不同带来的延迟上限不同。Flink是streaming first，流式作业的算子是在获取到资源后，一直运行的，这样子可以在算子之间进行数据交换时，形成pipeline流水线的数据传输，自然就可以实现毫秒级别的延迟。而Spark则是在批引擎上构建流式计算，所谓micro-batch的架构，其算子在需要map-reduce时，仍然是切分stage的，只能前面一个stage执行完成后，才能执行下一个stage，自然是无法实现毫秒级别的延迟。当然，这也有点好处，就是在可以接受的延迟情况下，能够节省一些资源（毕竟算子不是一直在运行的）。
        3. 设计理念不同带来的shuffle实现不同。Spark的shuffle来自MapReduce的经典理论，数据传输被切割成了经典的两阶段：根据key划分的map端写磁盘以及reduce端从磁盘读，这个的好处就是实现简单且稳定。而Flink由于是streaming first，所以数据传输是通过上下游task的网络buffer直接连接的流水线模式，聚合的逻辑被主要在下游reduce端（在Flink中就是keyBy 算子之后）的状态中进行处理。这个的好处就是可以达到低延迟，坏处就是这个状态的实现比较复杂，尤其是为了达到低延迟，状态后端（state-backend）需要在性能和capacity上做一个trade off，这也是为什么大规模实时作业需要使用RocksDB state-backend来解决基于on-heap内存的state-backend的稳定性问题。
        4. Flink这种数据交换方式带来的另一个非常大的优点，就是天生实现了反压机制（backpressure），上下游task的网络数据buffer队列形成了一个经典的生产者-消费者模型，当下游的消费能力不足时，下游无法向buffer队列中放置数据，整个作业就形成了一个反压的状态，也就不会继续从source端消费数据，避免了数据激增时带来作业的不稳定。至今Spark也依然缺乏一套完善的反压机制来提升稳定性。
        4. 更轻量的checkpoint机制。重构后的spark structured streaming也引入了state，来规避旧版本spark streaming需要将整个RDD持久化带来的不稳定问题。但是因为micro-batch的机制，实际上这些state在开启checkpoint之后，不得不在每个batch结束时对数据进行commit持久化，而不像Flink借助于async checkpoint barrier，可以在任意时间轻量级地执行checkpoint，这也是Flink早期在学术圈的亮点之一[13]。
    3. 新篇章：为什么说现在是推动Flink流批一体的计算引擎大规模落地的时刻了
        1. 在流式计算上为了在低延迟的情况下实现在批处理上习以为常的聚合计算，引入了状态、changlog流、支持exactly-once的轻量异步checkpoint容错、watermark、反压、pipeline shuffle等等机制。

    n. Related materials
        1. 数据仓库、数据湖、流批一体，终于有大神讲清楚了！ - 阿里云Hologres
           https://zhuanlan.zhihu.com/p/140867025
            1. "数据仓库，数据湖，包括Flink社区提的流批一体，它们到底能解决什么问题 ..."

28. 解读PolarFS中的Parallel Raft共识算法 - 川流
    https://zhuanlan.zhihu.com/p/653252230
    1. 那么就意味着leader发送给follower的请求可能是乱序到达follower的
    2. 在有日志空洞的前提下应用日志(Apply with Holes in the Log)
        1. Parallel Raft引入了一个数据结构 反向检查缓冲区(Look Behind Buffer) 
        2. 延迟列表(Pending List)
        3. 极其特殊的情况：连续空洞的数量大于N
    3. leader candidate需要预先经过一个merge的阶段，因为它不一定具有所有的集群已提交的日志
        1. Parallel Raft中没有commit Index这样的概念
        2. 对于leader candidate自己的日志，需要分如下三种异常情况做处理
            1. 在其他follower candidate节点上已提交但是在本节点上没有执行提交的index
            2. 在本节点上没有提交，且其他follower candidate节点均不存在的index（空洞）
            3. 在其他follower candidate节点上均未提交且均不一致(term不相同)的index
        3. Parallel Raft的选举收尾阶段
            1. Catch Up
                1. 假如是Follower Newbie与新Leader有巨大的日志差异，则通过Catch up可以恢复同
                2. Fast Catch Up
                3. Streaming Catch Up

    n. Related materials
        1. ParallelRaft: PolarFS: An Ultra-low Latency and Failure Resilient Distributed File System for Shared Storage Cloud Database    [2018, 124 refs, VLDB18]
           https://www.vldb.org/pvldb/vol11/p1849-cao.pdf)_._
           https://www.vldb.org/pvldb/vol11/p1849-cao.pdf
            1. We developed ParallelRaft, which allows out-of-order log acknowledging, committing and applying.
            2. ParallelRaft is used to replicate data across ChunkServer, rather than typically using Paxos in metadata servers. See Figure 2
            3. See Figure 2. The "ChunkServer" also appears in Pangu Filesystem paper and Alibaba EBS paper. Looks like they eventually converged into Pangu filesystem after years
                1. More Than Capacity: Performance-oriented Evolution of Pangu in Alibaba    [2023]
                   https://www.usenix.org/system/files/fast23-li-qiang_more.pdf
                    1. "Pangu adopts the append-only chunks and uses a self-contained chunk layout to manage chunks on chunkservers"
                2. What's the Story in EBS Glory: Evolutions and Lessons in Building Cloud Block Store    [2024]
                   https://www.usenix.org/system/files/fast24-zhang-weidong.pdf
                    1. "What if Pangu and EBS were never separated?"
            4. My questions
                1. How does ParallelRaft compare to 3-way chained replication commonly used in storage systems?
                    1. Didn't find such comparison in paper

29. GPU 虚拟化 [二]
    https://zhuanlan.zhihu.com/p/637960629
    GPU 虚拟化 [一]
    https://zhuanlan.zhihu.com/p/610441011
    1. 虚拟化方案
        1. pass-through
            1. 整体 pass-through
            2. 部分 pass-through
                1. 如果一个 GPU 本身支持 SR-IOV 的话
        2. 硬件 - 空分
            1. 自 2020 年的 Ampere 微架构（比如 A100）开始支持一种叫做 MIG (Multi Instance GPU) 的技术
            2. 不过 MIG 的 partition 同普通 SR-IOV 一样，依然是静态的，不可在使用过程中动态调整。假设中途有 vGPU 被移除，那么空出来的资源也不能被重新分配。
        3. 软件 - 时分
            1. Time-Sliced vGPU（也有一定的 hardware-assistant）。这种虚拟化方式就和 CPU 虚拟化就比较像了。
                1. 目前的 A100 和 H100 等芯片，支持选择使用 MIG-Backed 或 Time-Sliced 模式，Nvidia 早期的一些型号，则只支持 Time-Sliced。
            2. 另一种相似的软件虚拟化方案是 vfio-mdev（其中 "m" 代表 mediate），大致是通过软件层的协调，向上呈现出一个类似 VF 的 mdev 设备。Intel 基于 mdev 的虚拟化技术叫做 GVT-g，被 i915 等芯片驱动所采用。
                1. 这里说的"软件"的功能（比如 scheduling），主要是由 KVM/Xen 这样的 hypervisor 来承担的，而硬件虚拟化是不需要 hypervisor 介入的。
            3. My questions
                1. In LLM scenarios, GPU usage is usually constraint by GPU memory size. How can time slicing be applicable in this case?

30. 并发程序分析介绍 - Yvan
    1. 锁的释放和获得构成了 Happened-before 关系
        1. 想要知道事件 c 是不是 happened-before 事件 e，我们只需要检查节 c 和 e 之间是不是连通的。
    2. 当然这里还可以继续优化 VR 和 VW 的数据结构，2009年的一篇 PLDI 的 paper[3] 将 VR 和 VW 的数据结构优化为了一个叫做 Epoch 的数据结构，把空间复杂度从 O(n) 降到了 O(1)。
    3. Golang Race Condition 检查工具 TSan
        1. TSan会在编译时对关键函数进行插桩，并在这些关键函数执行的前后更新相关的VectorClock并进行检查
    4.  Concurrency Analysis 相关 paper 

31. AI fabric is a bus or a network？ - Dio-晶
    https://zhuanlan.zhihu.com/p/708602042
    1. 在AI的互联里一直有一个谜题：节点之间到底应该是用什么方式交互。有说Direct Load/Store/Atomic的，也有说RDMA的Read/Write的，更有在Actor之间用某种间接Message的（Tenstorrent）。
        1. Nvdia的Nvlink包括GH200、NVL72，号称一个as a single GPU，都是基于内存语义Load/Store/Atomic的。但在Nvidia之外，周围大多数同学都对此是反面意见的。
    2. RDMA最大的困境，在于如何解决Lossy和Out-of-Order的主要问题（后者包括多路径和重传），以及上下文爆炸的次级问题。
    3. CPU/DMA的Load/Store/Atomic相比RDMA Send/Read/Write的独特价值是什么？
        1. Load/Store/Atomic相比Send/Read/Write的特征是Smaller Granularity & Higher IOPs 。
        2. Load/Store/Atomic是Fabric Stateless，并且提升带宽时端侧设计代价更低。
        3. Load/Store是Native Multi-Path & Load Balancing
        4. Load/Store具有亲和性，融合编程
        5. Load/Store管理简单，或者说和Network的出发点不一样
    4. CPU/DMA的Load/Store/Atomic相比RDMA Send/Read/Write的缺点是什么？
        1. Latency敏感
        2. Topology敏感
        3. 系统可维护测试性

    n. Related materials
        1. 再谈谈三万亿的破绽 - zarbot
           https://mp.weixin.qq.com/s/2ZrD-FqHeYy9zA7FM_bYXg

32. 专家论坛：AI基础设施的发展（GTC 2024） -  Andy730
    https://mp.weixin.qq.com/s/hFFI7tdMZ9J49W6QjPSxqw
    1. 核心观点
        1. AI的核心是快速高效地处理大量数据，这得益于如今更多的数据和强大的处理能力。NVIDIA过去十年通过利用GPU释放AI潜力，构建了以GPU为核心的基础设施，并注重网络、数据传输和存储。未来，AI基础设施将以整个数据中心为单位，形成"AI工厂"，实现全规模整合。
        2. AI领域的关键在于规模，模型越大越好。过去十年，AI通过扩大模型规模实现了显著的创新和突破。这一趋势由GPU驱动，更大内存、更快网络和存储的发展，使得AI基础设施不断改进，从而推动了这些创新。
        3. 许多客户在构建和生产模型方面已经做得很好，但在企业级规模推广时面临挑战，包括生命周期管理、资源优化和复杂再训练计划的高效管理。需要跨数据准备、AI工程和应用开发等多个团队的协作。
        4. 构建AI集群是一项复杂任务，涉及多个动态组件和共享平台，不同于传统的隔离方式。无论是在本地数据中心、托管数据中心还是云环境中，都需要可扩展的设计，以便在推出新模型时不需要重新开始。
        5. 民主化访问GPU对AI开发至关重要。快速实验和从研究到生产的转变都依赖于GPU的高效使用。构建开放、灵活的平台，以集成新工具和模型，并为团队提供所需的工具和自由。
        6. AI发展迅速，用户需要进行前瞻性投入，尝试可能不会长期使用的工具。目标是构建一个共享、一致的平台，实现民主化的GPU访问，并在云端和本地之间灵活切换。平台应具备可组合性，允许集成和替换组件，确保生产环境的需求。
        7. 从端到端的角度优化AI基础设施，不仅仅关注GPU，还需考虑网络、存储和软件，形成完整解决方案。资源共享，避免"影子AI"现象，通过建立AI卓越中心整合资源和最佳实践，全面服务于不同的应用场景。
        8. 云计算带来的安全漏洞和成本逐渐增加的问题使得企业寻找替代方案，保护知识产权并降低成本。混合环境逐渐流行，跨越本地数据中心、托管数据中心和公有云环境。虽然POC可能在云端启动，但在本地运行大规模GPU训练模型在成本上更具吸引力。
        9. 过去十年，AI基础设施的性能大幅提升，但充分利用这些性能仍是挑战，许多客户未能完全挖掘其潜力。HPC领域的经验表明，带有调度器的AI集群非常重要。
        10. AI将无处不在，尤其是推理，边缘推理在未来几年会变得重要。端到端的AI解决方案将不仅限于数据中心或云端，而是需要云端、本地和边缘的混合解决方案。关键在于整合这些元素，确保计算和存储能力到位，管理数据处理和存储，并保持低延迟。
        11. 未来，边缘将成为主要的AI生产场所，不再需要将数据带到数据中心。数据湖仓库解决方案，可以从不同位置创建数据集，用于训练和微调模型，并将模型部署回边缘进行推理。
        12. AI在投入生产之前并不会产生任何价值。无论是在私有数据中心、边缘位置还是云端运行模型，生产时的一致性都很重要。MLOps提供了模型构建、调整、性能以及生产部署方式的可重复性、可审计性和可追溯性。这使企业对将AI投入生产充满信心。企业越来越依赖AI来做决策，而他们对这些模型的信心源自于MLOps。
        13. 企业客户非常关注保护数据安全。混合模型为此提供了解决方案，使客户能够在安全的环境中执行AI流程，将AI带到自己的数据中心。
        14. 不仅数据科学家和工程师使用敏感数据训练模型，现在每个人都可以使用敏感数据提示LLM，这带来了新的安全挑战。在AI基础设施方面，保护敏感数据并防止未经授权的访问也是至关重要的。

33. AI Compilers Demystified AI - Luhui Hu
    https://medium.com/geekculture/ai-compilers-ae28afbc4907
    1. Then came a lot of ML compilers: 
        1. Apache TVM 
            1. compilation of deep learning models into minimum deployable modules; 
            2. infrastructure to automatically generate and optimize models on more backends with better performance
        2. NVIDIA TensorRT
            1. optimizer and runtime library for NVIDIA GPUs
        3. ONNX Runtime
            1. ONNX Runtime is a performance-focused engine for running ONNX models
        4. LLVM
            1. provide a modern, SSA-based compilation strategy supporting the static and dynamic compilation of arbitrary programming languages
        5. Google MLIR (Multi-Level Intermediate Representation)
            1.  a specification for intermediate representations (IR) and a coding toolkit to perform transformations
        6. TensorFlow XLA (Accelerated Linear Algebra)
            1. domain-specific compiler for linear algebra that can accelerate TensorFlow models with potentially no source code change
        7. Meta Glow
            1. accepts a computation graph from deep learning frameworks like PyTorch and generates highly optimized code for machine learning accelerators
        8. PyTorch nvFuser
            1. a DL compiler that just-in-time compiles fast and flexible GPU-specific code to reliably accelerate users' networks automatically
        9. Intel PlaidML
            1. With Intel's nGraph graph compiler, ... portability across various CPU, GPU, and other accelerator processor architectures
        10. OpenVINO 
            1. tailored for optimizing and accelerating deep learning inference on Intel hardware, while PlaidML is a more generic
    2. How AI Compilers Work AI
        1. Two layers architecture
            1. the framework-related upper layer and the hardware-related lower layer, with graph IR in middle
        2. Model Architecture-Related Optimizations
            1. constructing a computation graph. 
            2. It can be model architecture-specific (e.g., transformer domain). 
            3. And it can also be in the graph node and at the tensor, dataflow, and block levels
        3. Hardware-Specific Optimizations
            1. based on hardware architecture and attributes, such as intrinsic hardware mapping, memory allocation and fetching, memory latency hiding, loop-oriented optimizations, and parallelization. 
            2. Also, an auto-tuning mechanism leverages parameter tuning in hardware-specific optimizations
        4. AI Compiler Extensions

34. 那些年，字节跳动带给我的管理思考(一) - Funny David
    https://zhuanlan.zhihu.com/p/710097976
    那些年，字节跳动带给我的管理思考（二） - Funny David
    https://zhuanlan.zhihu.com/p/711182132
    那些年，字节跳动带给我的管理思考（三） - Funny David
    https://zhuanlan.zhihu.com/p/713967931
    1. Good article. The author summarized ByteDance management into details and backed with reasons and thinking.

35. 《宝贵的人生建议》读后感 - 黄金架构师 - 凯文·凯利（Kevin Kelly）
    https://zhuanlan.zhihu.com/p/713957729
    1. It looks like a common 鸡汤 article, but turns out the tips in it are very smart.

36. 新型OLAP引擎（Doris、StarRocks）调研与对比 - 温正湖
    https://zhuanlan.zhihu.com/p/714079192
    0. Good article. In-depth drilling.
    1. Doris或StarRocks用到业务场景中
        1. 一类是为了简化系统架构，希望单个OLAP引擎能够提供较全面的能力，即支持实时数据分析，又支持Hive表、MySQL表和数据湖表格式等多数据源的查询和Join能力。如下面为严选业务的分享内容：
            1. "离线数据大部分存储在 Hive 中，小部分存储在 Hbase（主要用于基础标签的查询）。实时数据一部分存储在 Hbase 中用于基础标签的查询，部分双写到 KUDU 和 ES 中，用于实时分组圈选和数据查询。离线圈选的数据通过 impala 计算出来缓存在 Redis 中。这一版本的缺点包括：存储引擎过多。双写有数据质量隐患，可能一方成功一方失败，导致数据不一致。项目复杂，可维护性较差。为了减少引擎和存储的使用量，提高项目可维护性，在版本一的基础上改进实现了版本二。"
        2. 另一类是为了降低存储成本、提高使用体验。比如通过冷热分离（冷数据转对象存储）或依靠列存的高压缩特点等降低存储成本，或者是通过标准的SQL来降低使用难度。
    2. Doris或StarRocks存在的价值
        1. 笔者认为Doris和StarRocks最大的价值在于其全面的分析能力，一个引擎能够解决大部分业务需求，不需要部署多个系统来分别满足不同的业务需求。
            1. "网易邮箱从 21 年开始接触 StarRocks，到现在一年多的时间里，作为一个刚刚崭露头角的 OLAP 系统，StarRocks 在各方面的表现都很不错，它在功能、性能以及覆盖的场景方面的表现，都让我们相当满意，甚至超出了我们当初的预期。"
            2. "存储架构版本二引入了 Apache Doris，离线数据主要存储在 Hive 中，同时将基础标签导入到 Doris，实时数据也存储在 Doris，基于 Spark 做 Hive 加 Doris 的联合查询，并将计算出来的结果存储在 Redis 中。经过此版改进后，实时离线引擎存储得到了统一，性能损失在可容忍范围内（Hbase 的查询性能比 Doris 好一些，能控制在 10ms 以内，Doris 目前是 1.0 版本，p99，查询性能能控制在 20ms 以内，p999，能控制在 50ms 以内）；项目简化，降低了运维成本。"
        2. 有一个专有名词来表示符合这样要求的系统，那就是LakeHouse，Doris和StarRocks是国内目前最接近LakeHouse要求的OLAP引擎。
    3. Apache Doris vs StarRocks
        1. See the tables in the article
        2. "总的来说，Doris和StarRocks在功能特性上没有太大差别，就算某些特性暂时领先，也不代表短期内不会发生变化。但相对来说，笔者认为在数据湖分析（多表Join等）和存算分离场景，StarRocks相对领先，其多表物化视图能力及使用愿景，很吸引人，更多内容详见智能的物化视图。在传统的OLAP查询分析场景，Doris具备一定的优势，包括高并发点查优化、倒排索引能力等，StarRocks虽然也宣传支持倒排索引，但看官方介绍是基于bitmap索引实现，能力不如Doris。"

    n. Related materials
        1. Doris vs Iceberg, Hudi, Delta-lake: Which one?
           https://www.reddit.com/r/dataengineering/comments/169rnpl/doris_vs_iceberg_hudi_deltalake_which_one/
            1. "What's the purpose of the open table format databases (iceberg, hudi, delta lake) if apache doris can achieve much faster query times?"

37. 啊我数据呢？ 一个分布式数据库中最严肃的问题 - Real
    https://zhuanlan.zhihu.com/p/687957959
    1. Good article. Example illustration how Spanner, CockroachDB, TiDB, CalvinDB solve consistency problem in DB transactions.
        1. Spanner: 2PC + Paxos replication per Tablet + Commit Wait & TrueTime.
        2. CockroachDB: 2PC + Raft replication per partition + Parallel Commit + HLC + Causal ordering on overlapping keys via ts max_offset
        3. TiDB: 2PC + Raft replication per partition + Time oracle backed by raft
        4. CalvinDB: Sequence layer + every node executes RW in exactly same order
            1. No More 2PC. Interesting analysis
            2. Calvin不仅在学术上是成功的，工业界也非常成功。Fauna DB是在Calvin基础上写的New SQL，这几年运营的非常成功。
            3. 但是除了Fauna DB采用了它的架构之外，Calvin在当今的商业数据库上算不上很流行。

    n. Related materials
        1. FaunaDB
            1. Spanner vs. Calvin: Distributed Consistency at Scale
               https://fauna.com/blog/distributed-consistency-at-scale-spanner-vs-calvin

            2. The conclusion of FaunaDB's evaluation is: a simple and fast database suitable for large-scale use.
               https://www.linkedin.com/pulse/conclusion-faunadbs-evaluation-simple-fast-database-use-rajasekaran/

```
