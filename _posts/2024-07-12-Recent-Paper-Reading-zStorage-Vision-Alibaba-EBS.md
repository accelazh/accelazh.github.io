---
layout: post
title: "Recent Paper Reading: zStorage Vision, Alibaba EBS"
tagline : "Recent Paper Reading: zStorage Vision, Alibaba EBS"
description: "Recent Paper Reading: zStorage Vision, Alibaba EBS"
category: "storage"
tags: [storage, paper, cloud]
---
{% include JB/setup %}

Search "very good", "good", "very interesting", "interesting", "very useful", "useful" for recommendation, and "my questions" for comments.

```
1. OpenAI Sora: Video generation models as world simulators
   https://openai.com/sora
   https://openai.com/research/video-generation-models-as-world-simulators
    1. Sora text-to-video model is able to generate 1 minute of high resolution and high fidelity video adhering to user prompt with accurate details, motions, and multiple characters. There is still weaknesses on accurately simulating the physics of a complex scene.
    2. highlights
        1. Key techniques
            1. patch-based representation
            2. Sora is a diffusion transformer
            3. re-captioning technique from DALLE3 applied to video
            4. Sora builds on past research in DALL·E and GPT models
        4. Usages
            1. text to image
            2. Animating images
            3. Extending videos, even backward or into a loop
            4. Connecting videos, even they are quite unrelated
            5. image generation
        5. Emerging simulation capabilities
            1. 3D consistency
            2. Long-range coherence and object permanence, Temporal consistency
            3. Interacting with the world
            4. Simulating digital worlds, game videos
        6. common failure modes
    3. my questions
        1. Why are all demo videos in slow motions? This is falsefully extending the generation length. 
    n. related materials
        1. Explaining OpenAI Sora's Spacetime Patches: The Key Ingredient
           https://towardsdatascience.com/explaining-openai-soras-spacetime-patches-the-key-ingredient-e14e0703ec5b
            1. Spacetime patches are at the heart of Sora's innovation
                1. without the need for pre-processing steps like resizing or padding

2. 分布式存储技术：总结2023，展望2024 - zStorage - 黄岩
   https://mp.weixin.qq.com/s/uXH8rkeJL_JMbKT3H9ZuCQ
    1. very good article for future vision
        1. "zStorage是针对数据库应用开发的高性能全闪分布式块。三节点zStorage集群可以达到200万IOPS随机读写性能，同时平均时延<300us、P99时延小于800us。zStorage支持多存储池、精简配置、快照/一致性组快照、链接克隆/完整克隆、NVMeoF/NVMeoTCP、iSCSI、CLI和API管理、快照差异位图（DCL）、慢盘检测、亚健康管理、16KB原子写、2副本、强一致3副本、Raft 3副本、IB和RoCE、TCP/IP、后台巡检、基于Merkle树的一致性校验、全流程TRIM、QoS、SCSI PR、SCSI CAW。"
    2. Highlights
        1. Leveraging NVMe
            1. 异步Event模型
                1. "zStorage达成相对比较 高性能的一个重要原因是，避免了pthread、mutex、condition的编程模式，使用 SPDK框架提倡的异步event模式。这就是要求代码中任何位置都不能阻塞，Raft流程中的写日志、发送消息、写元数据等等，都不能阻塞。"
            2. 用户态驱动、SPDK
            3. RDMA和NVMeoF
            4. 高性能定制化的本地文件系统
            5. 重删
            6. SSD vs HDD price converging
        2. EBOF, Share Everything架构
            1. "vastdata的 目标是让EBOF硬盘框变成像标准服务器一样的廉价硬件，这样围绕share everything 架构生态系统才能发展起来。"
            2. "这种架构可以在集群规模不大的情况下支持大比例EC，这样可以降低每TB存储成本。"
        3. 共识协议
            1. Multi-Raft
                1. Node level 对多个Raft组的心跳消息进行合并
                2. 多个Raft组的日志合并之后写盘
            2. Raft硬盘状态机，首先要解决的问题是，如何打快照
            3. "那么一片8TB的 SSD盘发生故障，需要耗时至少2小时。如果在这两个小时过程中，再发生一个SSD盘 故障，那么就会有部分Raft出现两个副本故障，只剩下一个正常副本，那么这个Raft 组就不可用了，不能再继续正常工作。
                整个系统中有几千个Raft组，只要有1个Raft组 不能正常工作，那么整个存储池就停摆了。 
                为了解决这个问题，zStorage给Raft增加 了一个logger角色。logger是一个可以在只有日志没有完整状态机数据的情况下工作 的Raft组成员，logger可以投票，但是不能被选为Leader。
                增加了Logger角色之后， zStorage的三副本可以在一个SSD故障的情况下，在10秒内恢复为三副本工作状态，只 要10秒内没有发生第二个SSD故障，那么就不会出现Raft组不可用的情况。"
            4. 实现基于Raft的EC
            5. "Raft中实现读的方法有两种：1、读操作其他操作相同，也要走Append Entry和 commit流程；2、不走Append Entry和commit流程，直接在Leader上读状态机；显然第2种方法性能更好，但是要保证新的Leader选出来之前，旧的Leader先退位，如果旧的Leader等待了一段时间，没有收集到足够的心跳消息，它自行退位。
                如果 这个旧Leader所在的服务器时钟不准，那么“等待一段时间”就不可靠，就可能出 现新旧两个Leader同时工作，Client从旧Leader读出了旧数据的情况，从而导致了 数据不一致问题。为了避免这种问题，zStorage会每隔一段时间，对所有服务器的 时钟频率做一次校对，并且让“等待一段时间”这个时长足够容忍不同服务器节点 之间的物理时钟频率的偏差。"
        4. 存储层接口
            1. 加密、压缩、块存储的逻辑卷、快照、克隆等等
            2. zStorage和Ceph的存储层对外提供原地更新接口。与Append-Only接口的架构对比， Write-in-place接口可以在存储层实现更多业务功能，也不需要跨越网络做compaction， 性能更好。
            3. 存算分离
                1. 节点之间不共享数据，如TiDB、OceanBase、ClickHouse等
                2. 底层存储在所有数据库节点之间共享，例如Oracle RAC、 PolarDB等
                3. 平衡OLTP和OLAP
                4. By reading the article, zStorage is probably going to use disaggregated architecture. It's selling storage not database anyway.
                    1. "所以，我认为“分布式存储”、“共享存储集群”、 “计算下推”同时具备这三个要素的架构，是理想的数据库架构。"

    n. related materials
        1. What is EBOF
            1. NVMe-oF存储扩展：EBOF、FBOF、EBOD生态详解 - 唐僧
               https://zhuanlan.zhihu.com/p/466820081
               https://www.snia.org/sites/default/files/ESF/Security-of-Data-on-NVMe-over-Fabrics-Final.pdf
            2. 数据中心Diskless架构化
               http://www.jifang360.com/news/20221227/n7563150914.html
        
        2. The Case for NFS-eSSDs    [2023, MSST]
           https://msstconference.org/MSST-history/2023/FlynnPresentation2.pdf
            1. Good redesign of storage architecture
            2. Highlights
                1. Today, NAS has 3 layers, Client->Filesystem Server->Storage Server, the last two each needs CPU, PCIe, NIC
                    1. Next, using NVMoF, Storage Server's CPU is offloaded, reads/writes directly go to flash
                    2. Next, using NFS4.2 e.g. Hammerspace, reads/writes don't need to go through Filesystem Server any more after first hand shake. Data path doesn't need NVMoF, doesn't even need an internal network.
                    3. Next, using NFS4.2 and NFS-eSSD, Storage Server is not needed, and NFS-eSSDs are directly attached to network. For rads/writes, Client directly accesses NFS-eSSD through network via protocol NFS3, nothing in middle.
                        1. NFS-eSSD along itself can translate File offset to block mapping, and Block to flash address mapping.

            n. Related materials
                1. Hammerspace: Standards-Based Parallel Global File Systems & Automated Data Orchestration with NFS    [MSST, 2023]
                   https://www.ddserv.com/DOCs/HS%20Technology%20Whitepaper_v.1.1_Aug22%20-1-.pdf
                    1. Hammerspace is a startup company now. It means the new technology has potential.
                       https://hammerspace.com/
                       The session is done by Hammerspace CTO.
                    2. Highlights
                        1. NFS 4.2 new protocol. Compatibility across cloud vendors. And parallel. Good improvement from NFSv3.
                            1. Elimination of excess protocol chatter using
                                1. This eliminates 80% of NFSv3's GETATTR traffic
                                2. Compound operations
                                3. Caching and delegations, no need to go to server twice
                            2. Multiple parallel network connections between client and server and optional RDMA
                            3. Ability to write to multiple storage nodes synchronously (striping, mirroring)
                            4. Ability to move data while it is live being accessed w/o interruption
                            5. Ability to serve SMB over NFS
                        2. Hammerspace architecture
                            1. Metadata plane (named Anvil)
                                1. Leverage NFS 4.2 FlexFiles in Linux
                                2. Seems leveraging NetApp ONTAP and EMC Isilon
                            2. Data plane (named DSX)
                                1. Directly mounting NFS storage from cloud vendors
                                   Or, use DSX store as the cache layer
                                   Or, use DSX to attach to block storage SAN and convert protocol to FS
                                3. DSX cloud mover function, no interrupt to file access
                                4. File to object
                                    1. S3, Azure Blob over HTTP
                                    2. Global dedup, compression, encryption

                2. Hammerspace Technology White Paper    [2022]
                   https://www.ddserv.com/DOCs/HS%20Technology%20Whitepaper_v.1.1_Aug22%20-1-.pdf
                    1. NAS/NFS at global scale.Hybrid across all cloud vendors. One instance of file metadata to get consistency. File migration is managed in transparency. Auto resource elasticity.
                    2. Filesystem metadata plane is the key component. Consistency across different cloud vendors. All users are sharing the same metadata.
                        1. Migrating data across cloud is done with consistency. This usecase cannot be walked around by existing systems.
                    m. My questions
                        1. How to maintain both consistency and latency at the global scale? Cross region region there is non-neglect-able networking latency

                3. What's New in NFS 4.2?    [2015, SNIA]
                   https://www.snia.org/sites/default/files/NFS_4.2_Final.pdf
                    1. Highlights
                        1. New features
                            1. Sparse File Support 
                            2. Space Reservation
                            3. Labeled NFS
                                1. Allows partial SELinux support
                            4. IO_ADVISE
                                1. App can tell server IO patterns. Sequential, random, read, write, etc.
                            5. Server Side Copy
                                1. Server to Server, Rather than Server->Client->Server 
                            6. Application Data Holes
                                1. Create sparse file
                        2. pNFS New Layouts; FlexFiles & SCSI
                            1. Aggregation of standalone NFS servers
                            2. per-file striping

                4. Hyperscale Storage Perspectives    [2023, MSST]
                   https://msstconference.org/MSST-history/2023/StenfortPresentation.pdf
                    1. SSD M.2 Challenges => E1.S Solution
                    2. 2022 Host provided data placement hints - Solution #3 Flexible Data Placement
                        1. FDP Use Case Example
                            1. Multi-user/ Multi-workload/ Disaggregated Storage

        3. CXL
            1. Compute Express Link (CXL): All you need to know
               https://www.rambus.com/blogs/compute-express-link/
                1. First generation will base on PCIe Gen5, which means 64GB/sec with 16x
        
        4. NVMe FDP - Flexible Data Placement
            1. Hyperscale Innovation: Flexible Data Placement Mode (FDP)    [2022, NVM Express]
               https://nvmexpress.org/wp-content/uploads/Hyperscale-Innovation-Flexible-Data-Placement-Mode-FDP.pdf
                1. Problem of today's SSD
                    1. Overprovisioning space ~28%
                    2. Random writes have worse performance than sequential writes
                    3. Media wear out due to WA
                2. History
                    1. Google & Meta merged their independent learnings into Flexible Data Placement (FDP) merging the best features of each proposal to enable best industry solution

            2. Flexible Data Placement FDP Overview    [2023, NVM Express]
               https://youtu.be/BENgm5a17ws?si=6PGLAaA_zfpkKXJc&t=880
                1. FDP interface
                    1. Reclaim Units (RU) -> flash block to erase
                       Reclaim Unit Handle (RUH)
                       Reclaim group (RG) -> a flash die
                    2. Endurance Group (EG) -> multiple RGs, to set different configuration, e.g. enable FDP or not
                    3. A host write can specify RG and RUH -> the placement
                       Placement handle
                2. Comparison of Streams, FDP, Zoned Namespaces
                   https://youtu.be/BENgm5a17ws?si=Gg-5qBt3z1cg1Ihk&t=1277
                    1. Useful chart
                    2. FDP can be seen as something in the middle of Streams vs ZNS

        5. HBM - High-Bandwidth Memory 
            1. High-Bandwidth Memory (HBM)
               https://semiengineering.com/knowledge_centers/memory/volatile-memory/dynamic-random-access-memory/high-bandwidth-memory/
            2. Wikipedia: High Bandwidth Memory
               https://en.wikipedia.org/wiki/High_Bandwidth_Memory
                1. 3D-stacked synchronous dynamic random-access memory (SDRAM)
                2. higher bandwidth than DDR4 or GDDR5 while using less power, achieved by stacking up to eight DRAM dies
                3. HBM memory bus is very wide in comparison to other DRAM memories such as DDR4 or GDDR5
                4. Mainly used for GPU

        6. DAOS
            2. A brief overview of Intel DAOS high performance storage    [2019]
               https://blocksandfiles.com/2019/11/28/intel-daos-high-performance-storage-file-system-explainer/
                1. DAOS is Intel's Optane-using file system for high performance computing
                2. Intel envisages DAOS as the successor to Lustre
                3. A scale-out object store optimised for Intel CPUs and Optane DIMMs and NVMe SSDs
                4. Operates in user space with full operating system bypass
                    1. Metadata, low-latency IO, and indexing/query -> PMDK to Intel Optane DC PMEM, using byte-addressable memory interface
                    2. Bulk data -> SPDK to Intel Optane DC SSD, via block-addressable NVMe interface
                5. "DAOS lacks the native POSIX file access that many HPC applications need. Instead, it gets its POSIX capability by using a foreign layout feature in Lustre, according to Glenn Lockwood, a storage architect at NERSC. DAOS is then an entity in the Lustre namespace that looks like a Lustre filesystem."
                    1. So, people are comparing DAOS with Lustre. But DAOS is an object storage, not POSIX not filesystem as commonly needed by HPC.
                    2. My questions
                        1. So, DAOS needs to add an additional translation layer. Isn't that adding latency again given Optane targets speed? 
                6. "In our view Intel is positioning DAOS as another Optane adoption hook. HPC folks are hooked on speed. Give them DAOS for free and Optane DIMM and SSD sales will follow. As a bonus, AMD gets locked out of DAOS-using installations since Optane persistent memory require Intel CPUs."
                    1. Interesting
                7. from zStorage article: "DAOS强绑定Intel Optane PM，由于Optane停产对DAOS的发展造成了不小的冲击。"
                
                n. Related materials
                    1. How Weka.io comapres with Vast Data?
                        1. VAST Data making its presence known in the HPC market
                           https://blocksandfiles.com/2023/08/29/vast-hpc-market/
                            1. Weka.io targets HPC market.
                               WEKA is a proper parallel file system, and VAST is enterprise storage.
                            2. US academic and government HPC survey
                               Lustre 54.2%, Vast Data 33.3%, Weka.io 2.1%
                        2. Reddit: Eli5 - Vast vs Weka, HPC & Deep Learning
                           https://www.reddit.com/r/HPC/comments/18mwvgq/eli5_vast_vs_weka_hpc_deep_learning/

                    2. Weka storage drill down
                        1. WEKA Architectural Whitepaper HTML
                           https://www.weka.io/resources/white-paper/wekaio-architectural-whitepaper/
                            1. Key goals of WekaFS
                                1. Optimized for NVMe
                                2. Multi-protocol ready
                                3. Built-in durability
                                4. Advanced security
                                5. Built for the cloud
                            2. Example use cases include:
                                1. Artificial Intelligence (AI) and Machine Learning (ML), including AIOps and MLOps
                                2. Life sciences including genomics, Cryo-EM, pharmacometrics (NONMEM, PsN)
                                3. Financial trading, including backtesting, time-series analysis, and risk management
                                4. Engineering DevOps
                                5. Electronic Design and Automation (EDA)
                                6. Media rendering and visual effects (VFX)
                                7. High-Performance Computing (HPC)
                                8. GPU pipeline acceleration
                            3. Highlights
                                1. WEKA runs in usespace in LXC Container, including NVMoF drivers.
                                   SSD access via SPDK. Networking access via DPDK. Kernel is bypassed
                                2. WEKA runs on RTOS inside the container
                                    1. Interesting
                                    2. Front End: Manages multiple protocols, POSIX, S3, NFS, SMB
                                       Compute: Manages placement, protection, metadata, tiering.
                                       Drive: also runs in userspace 
                                    3. Running in LXC container supports converged architecture
                                       application and storage software sharing the same server
                                3. Cloud-native design
                                    1. An optional S3-compatible object storage layer to tier longterm data
                                    2. Unified filesystem namespace across NVMe flash layer and S3
                                    3. Directly mounting to object store, ingested data skips flash tier
                                    4. Snap-to-object: committing all data of file snapshot and metadata to object store.
                                    5. Container Storage Interface (CSI) with K8S Kubernetes 
                                4. Proprietary networking - WekaIO L5 Protocol over IP
                                    1. Either InfiniBand (IB) HDR and EDR, or Ethernet.
                                    2. Not TCP/IP. It's proprietary stack.
                                    3. DPDK, no context switch, bypassing kernel
                                    4. Proprietary WEKA protocol over UDP - Interesting
                                        1. HA by allowing for failover and failback between network interfaces and switches
                                        2. Load balancing across both interfaces
                                        3. Support for Mixed Networking Environments, allowing both InfiniBand and Ethernet clients to access the same cluster
                                        4. Supports VMXNET3 networking from VMware to ensure seamless vMotion
                                        5. WEKA does not require a lossless network setting to support NVMoF. Unlike RoCE and PFC.
                                            1. In compare, Azure RDMA combines PFC and DCQCN
                                               https://www.microsoft.com/en-us/research/uploads/prod/2023/03/RDMA_Experience_Paper_TR-1.pdf
                                5. Adaptive Caching
                                    1. Leverage Linux page cache for data caching and dentry cache for metadata caching. WEKA supports maintaining data consistency/coherence across the shared storage cluster
                                        1. How to ensure cache coherence is alike CPU MESI protocol. A flag indicates whether a cache entry is exclusive. Once an entry is modified externally, WekaFS will invalidate the local entry.
                                        2. "No other file system provides the adaptive caching capability of WekaFS"
                                6. Data protection / Erasure Coding
                                    1. Stripe sizes can be set to any value from 4 to 16, while parity can be set to either +2 or +4.
                                7. Flexible deployment
                                    1. Bare metal, virtualized, containerized, cloud
                                    2. Converged 


                        2. WekaFS Architecture White Paper PDF 2023
                           https://www.weka.io/wp-content/uploads/resources/2023/03/weka-architecture-white-paper.pdf
                            1. Same content with the HTML version

            3. ChatGPT asking about DAOS
                1. DAOS comparing to Ceph
                    1. DAOS is designed ground up to leverage NVMe. Ceph is day-1 designed for HDD, then gets SSD.
                    2. Object storage model, targeting AI, HPC. Ceph is a unified storage, supporting file, object, block.
                    4. Intel led DAOS opensource. Redhat led Ceph opensource.
                2. Key technologies behind DAOS
                    1. to leverage NVMe
                        1. Intel Optane PMEM.
                        2. InfiniBand, Omni-Path, High-speed Ethernet
                        3. Zero-Copy I/O
                        4. Direct access to NVM
                    2. to optimize for AI, HPC
                        1. Distributed object model
                            1. object spanning multiple nodes
                            2. Flat object namespace
                            3. Object can carry attributes metadata for management and searching
                        2. Integrate seamlessly with popular AI frameworks and HPC software stacks
                    3. Others
                        1. Storage tiering and pooling
                        2. Distributed and hierarchical metadata management
                        3. Software-defined storage

            4. Zhihu about DAOS
                1. 下一代开源分布式存储(vs Ceph)系统 - DAOS - hongsongwu
                   https://zhuanlan.zhihu.com/p/672215338
                    1. SCM，PMEM，SPDK，RDMA
                    2. Run-to-Completition
                    3. 数据I/O端到端无内核调用开销
                    4. 普通SSD擦写次数是有限的，通过把小io聚合在SCM，合并下刷到SSD，进而减少io
                2. DAOS在后傲腾时代的演变 - 唐僧
                   https://zhuanlan.zhihu.com/p/676577025
                    1. Post-Optane: Metadata on NVMe (Checkpointing)
                        1. DRAM + SSD flush checkpoint
                3. 理解DAOS存储性能的扩展性 - edwu
                   https://zhuanlan.zhihu.com/p/655001654

            4. DAOS: A Scale-Out High Performance Storage Stack for Storage Class Memory    [2020, 51 refs, Supercomputing frontiers, Intel]
                1. The starting paper for DAOS.
                2. Highlights
                    1. Argobots User Level Thread (ULT)
                    2. object placement by pseudorandom based on object ID, similar but not using Ceph CRUSH
                    3. Replication, secondary data servers directly RDMA fetch data from client
                    4. Use 2PC protocol for replicated update
                    5. Server failure and membership decision is managed by a RAFT service
                    6. Per recovery, any server can find other replicas by calculating placement based on object ID
                        1. There is no central place to perform metadata scans
                    7. Per partial write to an EC stripe, read-modify-write is not needed. DAOS replicates partial write data to the parity server. Later lazily merge.
                        1. seems Parity Logging
                        2. 2PC is involved in EC updates too.
                    8. Array objects that allow an application to represent a multi-dimensional array
                    9.Objects have versioned data and supports rollback
                    10. Treating POSIX as a middleware IO library atop of DAOS object interface
                    11. IO500 benchmark suit on DAOS
                    12. end2end checksum for data integrity

            5. DAOS Github documentation
               https://github.com/daos-stack/daos/blob/master/docs/overview/architecture.md
               https://docs.daos.io/v2.4/
                1. Architecture doc
                   https://github.com/daos-stack/daos/blob/master/docs/overview/architecture.md
                    1. DAOS I/O operations are logged and then inserted into a persistent index maintained in SCM
                        1. The SCM storage is memory-mapped directly into the address space of the DAOS service that manages the persistent index via direct load/store.
                        2. My questions
                            1. Does it use DRAM as caching? How to efficiently do this is an interesting question.
                    2. No read-modify-write operations are performed internally. Write operations are non-destructive and not sensitive to alignment.
                        1. My questions
                            1. It's append-only now?
                
                2. Object model doc
                   https://github.com/daos-stack/daos/blob/master/src/object/README.md
                    1. KV store key=>value
                    2. Object byte array => several extents
                
                3. Algorithmic object placement doc
                   https://github.com/daos-stack/daos/blob/master/src/placement/README.md
                    1. consistent hash based algorithm. But not Ceph CRUSH
                    2. Topology of a pool map + Modular different placement maps of the pool
                        1. Jump Placement Map (default) - Jump Consistent Hashing algorithm
                            1. Jump Consistent Hash: A faster/leaner approach for scaling data storage
                               ttps://blog.techlanika.com/jump-consistent-hash-a-faster-leaner-approach-for-scaling-data-storage-3969a7dae3e4
                                1. paper "A Fast, Minimal Memory, Consistent Hash Algorithm" by Google
                                    1. Interesting
                                2. Highlights
                                    1. Removing an arbitrary server is not supported.
                                       Arbitrary server name is not supported.
                                       Client needs to know the list of all servers.
                                    2. Benefit:
                                        1. Even key distribution, a standard deviation of 0.00000000764 and a 99% confidence interval of bucket size
                                            1. Traditional consistent hashing: Even with 1000 virtual nodes per server, you get a standard deviation of ~3.2% in the number of keys assigned to different nodes
                                    3. Simple implementation. Figure 1 full code is less then 10 lines. 
                        2. Ring Placement Map
                
                4. Versioning Object Store doc
                   https://github.com/daos-stack/daos/blob/master/src/vos/README.md
                    1. VOS uses log-based architecture to manage index on SCM
                        1. PMDK for SCM, SPDK for NVMe SSDs.
                            1. From the EV-Tree design, we can see epoch is stored inside the tree. In another word, object version is stored as part of index inside the SCM.
                        2. Bulk data goes to NVMe SSD. Smaller data goes to SCM too.
                            1. My questions
                                1. It's similar with Ceph. If updates are small, they merge with RocksDB KV updates, rather than normally goes to BlueStore. 
                    2. VOS employs PMEM transaction (different from DAOS transaction), to ensure update atomicity and flush durability
                        1. VOS uses epoch to capture object update logs. The epoch is also used in DAOS transaction as commit timestamp. GC is needed to reclaim expired epochs. 
                        2. Object version is represented by the epoch here
                    3. Caching
                        1. Negative entry cache - To store timestamps for entries that do not exist in the VOS tree
                    4. Supporting Key Array Stores
                        1. A specialized R-Tree, called an Extent-Validity tree (EV-Tree) to store and query versioned array indices
                            1. Interesting
                            2. My questions
                                1. Comparing to traditionally tracking epochs by list, R-tree provides tree search for epochs too.
                    5. DTX - DAOS 2PC transaction
                        1. VSO handles the local transaction. Which is called DTX

                5. Blob I/O doc
                   https://github.com/daos-stack/daos/blob/master/src/bio/README.md
                    1. Blob IO - BIO - manages NVMe SSD
                    2. Per-Server Metadata Management (SMD)
                        1. Use SCM to manage NVMe Device Table and NVMe Pool Table
                    3. NVMe Threading Model
                    4. The DAOS data plane will monitor NVMe SSDs every 60 seconds for health monitoring
                        1. SSD Eviction
                        2. NVMe hot plug with Intel VMD devices is supported
                
                6. Storage Model
                   https://github.com/daos-stack/daos/blob/master/docs/overview/storage.md#daos-container
                    1. Pool. The actual space allocated to the pool on each target is called a pool shard.
                    2. A container represents an object address space inside a pool
                    3. VOS epoch is the object versioning
                        1. "A container is the basic unit of transaction and versioning. All object operations are implicitly tagged by the DAOS library with a timestamp called an epoch. The DAOS transaction API allows to combine multiple object updates into a single atomic transaction, with multi-version concurrency control based on epoch ordering."
                    4. A DAOS object can be accessed with
                        1. Multi-level key-array
                            1. Interesting
                            2. "Each DAOS object is a Key-Value store with locality feature. The key is split into a dkey (distribution key) and an akey (attribute key). All entries with the same dkey are guaranteed to be collocated on the same target."
                               https://github.com/daos-stack/daos/blob/master/src/object/README.md
                        2. Key-value
                        3. Array API
                
                7. Transaction Model
                   https://github.com/daos-stack/daos/blob/master/docs/overview/transaction.md#container-snapshot
                    1. Timestamp called epoch 64-bit integer generated by HLC
                       https://cse.buffalo.edu/tech-reports/2014-04.pdf
                        1. Same with CockroachDB's HLC 
                    2. Container snapshot feature, lightweight and are tagged with the epoch
                    3. Distributed Transactions
                        1. Single IO operations don't suffer from transaction overhead. They are tagged with a different epoch and applied in epoch order
                            1. Typical examples are collective MPI-IO operations, POSIX file read/write or HDF5 dataset read/write.
                        2. Distributed serializable transaction based on multi-version concurrency control
                            1. Examples are a SQL database over DAOS or a consistent POSIX namespace accessed concurrently by uncoordinated clients.
                            2. All operations in transaction use the same epoch
                            3. In the initial implementation, the transaction API does not support reading your own uncommitted changes. In other words, transactional object or key-value modifications are invisible to the subsequent operations executed in the context of the same transaction.
                                1. Oh .. that's bad.

                8. DAOS Container doc
                   https://github.com/daos-stack/daos/blob/master/src/container/README.md
                    1. Container properties graph
                
                9. Versioned Block Allocator (VEA)
                   https://github.com/daos-stack/daos/blob/master/src/vea/README.md
                    1. An extent based block allocator specially designed for DAOS
                    2. OS update is executed in a 'delayed atomicity' manner, which consists of three steps
                       1) Reserve space for update and track the reservation transiently in DRAM
                       2) Start RMDA transfer to land data from client to reserved space
                       3) Turn the reservation into a persistent allocation and update the allocated address in VOS index within single PMDK transaction
                    3. VEA assumes a predictable workload pattern: All the block allocate and free calls are from different 'IO streams', and the blocks allocated within the same IO stream are likely to be freed at the same time
                        1. a straightforward conclusion is that external fragmentations could be reduced by making the per IO stream allocations contiguous
                        2. there are two IO streams per VOS container, one is the regular updates from client or rebuild, the other one is the updates from background VOS aggregation
                        3. My questions
                            1. Sounds like this is an append-only model and VEA is optimized for it.
                
                7. Task Scheduler Engine (TSE)
                   https://github.com/daos-stack/daos/blob/master/src/common/README.md#task-scheduler-engine-tse
                    1. How is it implemented? Didn't find detailed doc
                
                8. Replicated Services
                   https://github.com/daos-stack/daos/blob/master/src/rsvc/README.md#architecture
                    1. Certain DAOS RPC services, such as Pool Service, and Container Service, are replicated using the state machine approach with Raft
                    2. My questions
                        1. Sounds like a Raft implemented Replicated State Machine
                
                9. Self-healing (aka Rebuild)
                   https://github.com/daos-stack/daos/blob/master/src/rebuild/README.md
                    1. The rebuild is divided into 2 phases, scan and pull.
                    2. Once the rebuild initiators get the object list from the scanning target, it will pull the data of these objects from other replicas and then write data locally.
                    3. A target in rebuild does not need to re-scan its objects or reset rebuild progress for the current failure if another failure has occurred.
                
                10. DAOS Pool
                    https://github.com/daos-stack/daos/blob/master/src/pool/README.md
                    1. Metadata Layout chart

                11. DAOS Server doc
                    https://github.com/daos-stack/daos/blob/master/src/control/server/README.md
                    1. SCM Format vs NVMe Format
                        1. Formatting SCM involves creating an ext4 filesystem on the nvdimm device. Mounting SCM results in an active mount using the DAX extension enabling direct access
                            1. My questions
                                1. Running ext4 filesystem on SCM? Why not a more customized FS tailored for PMEM accessed in byte-addressable fashion?

            6. DAOS and Friends: A Proposal for an Exascale Storage System    [2016, Intel]
               https://pages.cs.wisc.edu/~johnbent/Pubs/lofstead_sc16.pdf

            7. DAOS An Architecture for Extreme Scale Storage    [2015, SDC15]
               https://www.snia.org/sites/default/files/SDC15_presentations/dist_sys/EricBarton_DAOS_Architecture_Extreme_Scale.pdf

        7. Modern cloud infra filesystem (or storage system) is moving to the below directions:
            1. To match speed with RDMA and NVMe SSD, storage engine moves to userspace, filesystem moves to userspace. Kernel is bypassed. Leverage DPDK and SPDK.
                1. Besides, Filesystem becomes specialized, i.e. customized for the storage. Storage wants to access the raw interface of drives, e.g. ZNS SSD, and SMR.
                2. Besides, not only Kernel Bypassing. RDMA bypasses remote host CPU to access DRAM. NVMe-over-Fabric bypasses remote host CPU to access SSD.
    
            2. DPU becomes widely used: 1) Network offloading. 2) Storage offloading. 3) RDMA Smart NIC
                1. A typical DPU is composed of FPGA + CPU. The CPU can be an ARM core, or a processor on FPGA. FPGA can also be replaced with ASIC.
                   DPU also equips with extended chips like VPU (Vector Processor Unit), local DRAM, fast DPU inter-connect, fast DPU to GPU inter-connect.
                
                2. The concept of FastPath: A (packet) processing only involves the FPGA/ASIC part of DU (fast pass through). It doesn't involve the CPU or memory on DPU. It doesn't involve the host.
                   In the second level, The (packet) processing bypasses middle nodes in the distributed system. Client directly reads/writes from the end2end data node.
                   Besides, FastPath usually requires RDMA and NVMe-oF which bypasses the destination host CPU to access DRAM or SSD. 
                   The eventual goal is to offload the entire data path. The entire data path should be running on acceleration hardware, rather than CPU.
                
                3. Other typical hardware offloading usages
                    1) Offload compression/Encryption and CRC calculation. They can be offloaded to DPU, or RDMA smart NIC.
                    2) Smart SSD. Databases can pushdown filters or GC to on-SSD chip, which avoids PCIe bottleneck between SSD and CPU.
    
            3. Increasing adoption of zoned device to cut the storage cost, i.e. SMR drives and ZNS SSD. They expose similar Zoned Block Device (ZBD) interface.
                1. SMR drives allows higher HDD areal density. Writes subject to zone-level append-only, and open zone limit. Storage engine or filesystem need to be customized.
                2. ZNS SSD is essentially an SSD with a very simplified FTL. Cost is lower. And, it allows storage engine to highly customize GC and data placement.
    
            n. Related materials
                1. Pangu 2.0: More Than Capacity: Performance-oriented Evolution of Pangu in Alibaba
                   https://www.usenix.org/conference/fast23/presentation/li-qiang-deployed
                2. Pangu FS client: Fisc: A Large-scale Cloud-native-oriented File System
                   https://www.usenix.org/conference/fast23/presentation/li-qiang-fisc
                3. Pangu RDMA: When Cloud Storage Meets RDMA
                   https://www.usenix.org/conference/nsdi21/presentation/gao
                4. Pangu Networking: From Luna to Solar: The Evolutions of the Compute-to-Storage Networks in Alibaba Cloud
                   https://rmiao.github.io/assets/pdf/solar-sigcomm22.pdf
                5. Pangu DPU: X-Dragon: Hyperscale FPGA-as-a-Service Architecture for Large-Scale Distributed Graph Neural Network
                   https://dl.acm.org/doi/abs/10.1145/3470496.3527439
                6. Pangu SMR: Deployed System: SMRSTORE: A Storage Engine for Cloud Object Storage on HM-SMR Drives
                   https://www.usenix.org/conference/fast23/presentation/zhou


3. Alibaba EBS: What's the Story in EBS Glory: Evolutions and Lessons in Building Cloud Block Store    [2024, 0 refs, FAST24 Best Paper]
   https://www.usenix.org/conference/fast24/presentation/zhang-weidong
    1. Very good.
       LSM-tree append-only, Inline EC and compression with JournalFiles, FPGA and DPU, PMEM one-hop write and Solar networking, Federated BlockManager.
       Features in Write Amplification reduction with Inline EC and compression (Fusion Write Engine, SegmentCache, FPGA compression).
       EBS2 VD achieves 1M IOPS and 4,000 MiB/s throughput with 100us latency. Then EBS3 reduces storage overhead from 1.29 to 0.77 (w. compression) and traffic amplification from 4.69 to 1.59 (include 1 round of GC).
        1. Good chart the Figure 1 - chronological progression of Alibaba EBS since 2012
    2. Highlights
        1. VD, Segment Group, Segment, Data Sector, Pangu DataFile
            1. VD (Virtual Disk) is eventually partitioned into Data Sectors (2MiB to 128KiB). Data Sectors are mapped to Segments (32GB) in a round-robin fashion.
                1. Why need Segment Group (128GB)? A Segment can only take Data Sectors from one Segment Group.
                2. Reducing the Data Sector size allows scaling one SegmentGroup to more nodes. But, Data Sector is in the address space of VD. Not every bytes in the address space is actually written. The true data written to disk should be smaller blocks, per write request (usually 16KiB or smaller), and they map to the blocks in Pangu files.
                    n. My questions
                        1. How a smaller Data Sector size allows scaling one SegmentGroup to more nodes? I didn't see the paper explain that. As far as I can see, a Segment is the writing unit. The writes from a Segment can probably to sharded to multiple Pangu DataFiles appended in log-structured fashion. So, the parallel level is decided by how many Pangu DataFiles involved, rather than how small is the Data Sector size.
                            1. The paper mentioned "In the field, we further decrease Data Sector size to 128 KiB and EBS2 (and EBS3) are able to deliver 1,000 IOPS for every GiB subscribed". But no chart to show the change. Probably, Data Sector is somehow the smallest unit to be put to one node.

        2. AutoPL - "users can subscribe throughput and IOPS of VD on demand without altering the capacity"
            1. ESSD Auto PL Specifications, Leading A New Direction of I/O Performance Elasticity    [2022]
               https://www.alibabacloud.com/blog/essd-auto-pl-specifications-leading-a-new-direction-of-io-performance-elasticity_598859
                1. Traditional block storage products are designed with performance/capacity coupling
                2. PL is VD's performance level. Auto PL is alike AWS intelligent tiering. But
                    1. AutoPL allows scheduled reservation to target access peaks.
                    2. AutoPL allows instant elasticity expansion for bust access.
                    3. Auto reduce PL level to reduce cost, and in a fine-grain at per disk PL level, finer than tier movement
                3. The technologies behind AutoPL are
                    1. Sharding stripes to more nodes
                    2. Tenant isolation and IO priority management
                        1. Base+Burst IO. When overloaded, server prioritize to serve the base IO. (mentioned in EBS paper)
                    3. Load balancing across clusters by hot disk migration

        3. SegmentCache and FusionEngine - Very Good. Implementing Compression + Inline EC at Cloud Disk / Block Storage
            1. The initial problem is probably how to enable Inline EC to VD workload. A key problem is the writes are too small. We need to write the writes to disk with redundancy, but we want to reduce this write amplification.
               The solution is we merge small writes from different VDs (Segments), until reach 16KiB, compress them with DPU (Fusion Write Engine, FWE, FPGA), and write to disk in EC format (4+2), called JournalFiles. After JournalFiles written, user can be ACKed with IO complete.

            2. The second problem is, JournalFiles mixes different VD writes compressed together. It's bad for read. We designate JournalFiles as write-only.
               The solution is, we need a second round to write the true data, well-formatted, to elsewhere. The second round can happen in a delayed way, after writing JournalFiles. In the second round, there is no need to mix data from different VDs, and the buffer data can reach a bigger size (512KiB) before doing compression. The buffered data is being held in memory, per VD (Segment), called SegmentCache.
                1. Alternatively, it's possible to read JournalFiles from disks and recompress / reEC again. But this still means more IO amplifications. And yet more write amplification if we have to make JournalFiles easy to read from.

            3. Although the Double Write problem exists (JournalFile + SegmentCache writes), by applying compression + Inline EC, it can still reduce the overall write amplification even it's double writes. And, storage overhead can also be smaller because now compression is more effective by using larger blocks from SegmentCache. 
                1. The write amplification compare is: 3.0 vs (4+2)/4 * compression ratio + (8+3)/8 * compression ratio. Even compression ratio is 1.0, the new approach is still better. Not even counting the Offline EC potentially needed. This is the essence of the good part.
                
                2. Another potential trade off is read. If the compressed blocks are larger, though compression ratio is better, reading decompress is also slower. But it should be fine as the paper mentioned SegmentCache flush size is only 512KiB, and decompression is accelerated via FPGA
                
                3. Another good point is, a Pangu DataFile is exclusively occupied by one VD. A DataFile is NOT mixing data from different VDs. So compression should be more effective.
                    1. I didn't see the paper explicitly confirm DataFile is exclusive to VD, but it seems YES from 
                        1. Figure 7: Segment to DataFile is 1-on-1 mapping
                        
                        2. GC: Section 2.2. "performing GC by collecting valid data from the dirtiest DataFiles under the same segment"
                        
                        3. Disk segmentation: Section 2.2. "EBS2 associates one segment with multiple DataFiles (512 MiB by default) to support concurrent writes. DataFile is essentially a Pangu file designed to persist a portion of a segment's data."
                    
                    2. Another very good take away to think about is that "Stream" is no longer a necessary concept in the Pangu DataFile paradigm. Here the system partitioning happens at VD level, then to Segment Group and Segment (Note actually BlockManager still has partition concept which maps to a small subset of VDs).
                       How many open VD Segments, then how many open Pangu DataFiles to be appended to (multiplied by parallel count). VD exclusive Pangu DataFiles improve compression efficiency. And, because no mixing VDs to one DataFile, the VD throughput won't be limited by one DataFile throughput. Today, the trend is one VD must be shared to multiple DataFiles.  
                        
                        1. The concept of "Stream" initially comes from Azure Storage and Google Filesystem. But in the Pangu and Alibaba EBS paradigm, "Stream" no longer seems necessary. It even brings negative downsides.
                            
                            1. Pangu didn't come to the "Stream" path probably because it's initially based on HDFS, file based, and supports random write files. There is no "Stream" from day 1. And today Pangu converges to log-structure, append-only.

                            2. Quote, From Figure 7, Each EC.DataFile maps to one naming unit in Pangu Filesystem. This further shows "Stream" is not a concept being used in EBS/Pangu.
                        
                        2. However, Pangu should still support random write files today. It would making running things like RocksDB easy (mostly append-only, but still need random write file). RocksDB is useful in everywhere in system architecture e.g. to offload metadata storage, to assist Paxos replicated metadata cores.
                            1. Good. Need to think about "Stream" vs random write.
                        
                        n. Related materials
                            1. Windows Azure Storage: A Highly Available Cloud Storage Service with Strong Consistency
                               https://www.cs.purdue.edu/homes/csjgwang/CloudNativeDB/AzureStorageSOSP11.pdf
                                1. Stream Layer

                            2. Pangu – The High Performance Distributed File System by Alibaba Cloud
                               https://www.alibabacloud.com/blog/pangu-the-high-performance-distributed-file-system-by-alibaba-cloud_594059
                                1. "Indeed, if Pangu is only a simple copy of HDFS" (initially)
                            
                            3. Pangu - More Than Capacity: Performance-Oriented Evolution of Pangu in Alibaba
                               https://www.usenix.org/conference/fast23/presentation/li-qiang-deployed
                                1. "gradually added support to multiple file types (e.g., TempFile, LogFile, and random access file)"

            n. My questions
                1. SegmentCache is storing duplicate things in memory with Index Map (LSM-tree's memory table). But so far I didn't see the paper try to dedup them. Ideally, SegmentCache can be organized in a queryable format.
                    1. A second question, why SegmentCache's data compression is via host CPU? Unlike FWS which uses FPGA to compress?

                2. Bigger problem: PMEM (DRAM + super capacitor, NVDIMM-N), attached to EBS layer, should be able to totally eliminate the need of JournalFiles. Just write to PMEM, Use PMEM as SegmentCache, and compression is done in PMEM. The PMEM size needed should be small because SegmentCache flushes per 512KiB.
                    1. EBSX is experimenting with PMEM. PMEM is installed at EBS side (rather than Pangu side). But somehow looks like not trying the remove the JournalFiles? It's a typical approach in storage systems to use PMEM to coalescing data and do data reduction. 
                    2. I.e. Parity Logging technique + PMEM.

                3. In Azure Storage, EC is managed by Stream Layer. At Alibaba EBS, EC is managed by the EBS layer rather than the Pangu Filesystem. Pangu FS simply stores "EC.DataFiles".
                    1. Besides, In AliCloud, EBS (block storage) and OSS (object storage, see SMRSTORE paper) are separated systems, though they both persist on Pangu Filesystem.
                    2. Besides, Pangu Filesystem supports random write files.
                    3. PMEM is installed at EBS side rather than at the Pangu side to reduce the 2nd hop in net work to reduce the latency.
                    4. How EC conducts data repair if certain EC.DataFile is lost? It seems not mentioned in this paper.

                4. How does Inline EC cut blocks given the flush size from SegmentCache is only 512KiB? 512KiB/8 looks too small.
                    1. EC(8,3) has 8 data symbols and 3 parity symbols. 512KiB size maps to 64KiB size per EC chunk. From this paper, probably the typical block size in Pangu DataFile is only 4KiB. So 64KiB is totally fine.
                        1. Even a longer EC codec is fine, SegmentCache can accumulate more data before flush. Due to VD latency is very low, the accumulated data size is very small w.r.t. system memory.
                    2. Quote, Section 6. "EC(8,3) needs 32 KiB data for one stripe with 4 KiB stripe unit size"
                       Quote, Figure 5, The block size in Pangu DataFile is only 4KiB.
                       Quote, Section 6. "each segment represents an address space of a 32 GiB segment consisting of 4 KiB blocks"

                5. What if a VD is too small or the new writes are too small to form an EC stripe?
                    1. Maybe not so big a problem, the required size is only 512KiB. The tail length is fine to write as 3-replica.
                    2. But if VD is too small, it will be unwise to assign DataFile for each individually. Small Segments can be grouped, then it introduces the needs for Partition Layer.

                6. EBS (block storage) and OSS (object storage) are separated systems. Both run on the same Pangu Filesystem. AWS S3 and AWS EBS look separated but not seems using this approach.
                    1. If append-only is a necessity to EBS, then a stream filesystem or shared logging platform (CORFU) becomes a common need. Not mentioning AWS Aurora Multi-master is also advocating "log is database", similar with Apple FoundationDB.
                    2. This is good to think about.

        4. Log-structured storage is better than update in-place. Even it's disk storage. Even it's full SSD.
            1. Update in-place is hard for 
                1) Compression which changes the block size
                2) EC but the write requests are very small

        5. Persistent Memory / PMEM and one-hop Solar
            1. PMEM is installed at EBS side rather than at the Pangu side. User write can be ACKed directly after it hits PMEM. No need to go a 2nd hop network to reach Pangu write to Pangu SSD.
                1. good point. From Figure 11, this reduced write latency ~30%, and reduced read latency to ~20%.
        
            n. My questions
                1. As mentioned the above, not seeing in paper that uses PMEM to remove the JournalFiles double write.
                2. Which type of PMEM is being used? NVDIMM-N has the same latency with DRAM. NVDIMM-F, NVDIMM-P are different.
                3. Not seeing in this paper to optimize PMEM access with PMEM RDMA nor NVMoF.
                
                4. From Figure 11, why read latency at Pangu SSD is so much higher than write to Pangu SSD?
                    1. EBS is using LSM-tree. A key question is how reads are served if the data is not in memory table. I found this is NOT mentioned in paper. A guess is, in LSM-tree, reads to disk must scan the SSTable file.
                        1. Scanning SSTable file explains why in Figure 11, the read latency on Pangu SSD is much higher than write latency
                        2. Quote Figure 5, there is indeed "SSTable" file in the picture. 
                        3. This is Good to think about.

        6. Solar [36], a UDP-based transmission protocol. By leveraging the hardware offloading on our Data Processing Units (DPUs), Solar can pack each storage data block as a network packet, thereby achieving CPU/PCIe bypassing, easy receive-side buffer management and fast multi-path recovery. Good.
            1. Solar is installed in Ali-DPU. The Ali-DPU has an CPU and FPGA. CPU/PCIe bypassing is probably means NIC received packet can bypass the CPU/PCIe in Ali-DPU, and directly goes into the Host memory. The Host is running VMs. EBS is at the remote side. (See Figure 10, and Figure 12,13.)
            
            2. The FPGA in Ali-DPU can offload CRC, QoS, Encrypt/Decrypt, block data structure operation, and UDP protocol management, and multi-path.
               Skip packet reordering and packet assembly by leveraging that blocks are independent.

            3. Luna (pre Solar) networking, Kernel bypassing, run-to-completion thread model and zero-copy memory model
            
            n. My questions
                1. Compression, CRC and encryption need CPU offloading anyway. But should the chip be CPU aside or NIC aside? Solar gives the answer - NIC aside. By leveraging "storage block" as the unified transport unit flowing across the system, NIC aside chip can easily integrate Compression, CRC and encryption, and achieve CPU/PCIe bypassing.

                2. If Ali-DPU is installed at BlockClient side, why it doesn't offload compression too?

        7. Federated BlockManager and blast radius
            1. What are BlockManager and BlockServer
                1. By serving VD, BlockManager is the control plane which serves VD metadata (capacity, snapshot version), while BlockServer is the data plane (handle IO requests, LSM-tree). BlockManager assigns VDs to BlockServer and handles Segment migration. BlockManager is a Paxos quorum in the controller role, BlockServer is a group of nodes.
                2. Problem of BlockManager before Federated BlockManager
                    1. BlockManager still needs to serve VD metadata. It uses a single table. It's a single pointer of failure SPOF.
                    2. BlockManager has scalability issues as the VD to cluster density grows.
            
            2. Federated BLockManager - to solve the above problems of BlockManager
                1. BlockManager is partitioned. How VDs map to each partition is static hashing.
                   BlockManager is not longer Paxos, now one node is enough. 
                2. A new CentralManager (Paxos) is introduced to manage BlockManager. 
                   It manages how partition is assigned to BlockManager. 
                   CentralManager won't manage VD, won't affect VD read/write even dead.
                3. Upon BlockManager failure, partition is migrated.
                   Partition is small enough so reload is fast, in hundred milliseconds. From Pangu disk, no standby.

                n. My questions
                    1. Partitioning is common, but instead of failing a partition, partition migration can further increase the availability. However, in the case of consistent crashing, migration can propagate blast radius, so we need Logical Failure Domain here. It worth attention that migration is usually made fast to preserve availability, but it negatively makes propagating crashing also fast.
                        1. Good point to think about

            3. Logical Failure Domain
                1. A faulty Segment crashes its BlockServer (buggy code). Migration further kills more BlockServers. 
                2. Use a Leaky Bucket (3 max token, refilled per 30min) to limit Segment migration. If token used up, the Segment can only be migrated within 3 pre-designated BlockServers (Logical Failure Domain).
                    1. Does not limit the number of migrations but the range of migrations
                    2. Merge Logical Failure Domains if there are multiple failing Segments. At most uses 3 BlockServers.
                    n. My questions
                        1. Problem: A normal Segment may become a false positive just because it occasionally be migrated into the Logical Failure Domain.
                            1. This paper mentioned this problem. But the chance doesn't look like small. Any Segment initially lives in the Global Logical Failure Domain, or happen to migrated into the Global Logical Failure Domain, will crash altogether and very likely to become a false positive.
            
            4. More techniques to reduce blast radius
                1. deploy a smaller cluster, reduced from 700 nodes to 100 nodes

        8. FPGA, used in FWE compression, used in Solar networking DPU
            1. Figure 8: FPGA compression throughput is only 2x~3x of CPU-only. This looks too low. But latency is much lower.
                1. CPU compression, latency-optimized LZ4, 16KiB size. Compression takes 25us, 25.6% of total write latency.
                    1. Moreover, to achieve 4,000 MiB/s throughput, at least 8 CPU cores are required
                2. FPGA reduces latency by 78%, and with a maximum throughput of 7.3 GiB/s
           
            2. Optimizing compression algorithms tailored to data blocks with varying temperature profiles
                1. Using the ZSTD algorithm for separated cold data blocks can further achieve an average 17% space reduction
                    1. This is interesting
                    2. But FPGA unable to ship ZSTD due to resource constraints
           
            3. Future is for ASIC, but much longer development cycles.
                1. BlockClient is moving to ASIC-based offloading
                   BlockServer is moving to ARM with compression accelerator

            4. FPGA instability issue. - This is a good summary.
                1. BlockClient is running the Solar [36], i.e. the Ali-DPU part, to do offloading. FPGA targets BlockClient
                    1. Unlike BlockClient, we chose not to use ASIC for BlockServers
                        1. BlockServer can use full CPUs, unlike BlockClient needs to leave CPU for users
                        2. BlockServer functionalities (a.k.a., operators) are in an ever-changing fashion, e.g., the introduction of new compression and garbage collection algorithms.
                        3. The many-core ARM CPU becomes a proper choice for BlockServer.
                
                2. The major drawback of FPGA is the instability. Specifically, 37% of data corruption incidents, as identified by CRC mismatches, are directly caused by FPGA-induced errors such as overheating, signal interference, and timing issues. This is because FPGAs are sensitive to environmental conditions and require precise timing, which can be disrupted by various factors like temperature fluctuations and electrical noise.
                    1. FPGA-related issues account for 22% of BlockClient's operational downtime.
                
                3. The frequency of FPGA is rather limited (e.g., around 200 MHz to 500 MHz), thereby limiting its potential for adapting to high-speed networks.

                4. "BlockServer faces similar instability FPGA issues. Over the past year, out of every 10,000 deployed production BlockServers, we have documented on average around 150 instances of compression offload failures by FPGA exceptions".

                5. ZSTD unable - "However, the resource constraints inherent to FPGAs preclude the dynamic adaptation to various compression algorithms." 

        9. ARM processor for BlockServer offloading
            1. Kunpeng 920 ARM CPU [41], and Yitian 710 ARM CPU [9]
                1. all of which are equipped with dedicated units for compression acceleration, only slightly higher latency compared to FPGA

            2. "This shift is motivated by the advent of multi-core CPUs and specialized computational units integrated within them, which offer superior cost-efficiency while maintaining comparable performance metrics"
                1. Interesting.

        10. Other points
            1. IO throttling: Base+Burst strategy. 
                1. When a BlockServer is unable to meet all IO demands, it prioritizes processing the baseIO to ensure consistent latency.
            3. QLC flash, ARM with compression accelerator, ASIC, ZNS SSD
            4. GC: SepBIT: placement based on inferring the block invalidation time [39]
                1. An interesting trial
            5. Data scrubbing, traffic at 10 MiB/s, i.e., scanning all DataFiles every 15 days
            6. EC with 8+3
            7. Figure 11(b): Our analysis indicates that the principal driver of the tail latency is the contention between the IO and the background tasks (e.g., segment status statistics and index compaction)
                1. To address this, we segregate the IO flow from other tasks and execute it on independent threads. Figure 11(b) EBS3, the original top latency part from BlockServer is totally eliminated.
            8. We observe that EBS2 with the 2 × 25 Gbps network, throughput is constrained by network capabilities.
               For EBS3 with the 2x100G network, the bottleneck shifts to the PCIe bandwidth.
            9. Fast VD cloning. EBS uses the Hard Link of Pangu files
            10. "A segment needs to have a write throughput over 160 MiB/s—surpassing 90% of segments in production"
                1. VD targets 4000MiB/sec throughput. Segment size is 32GiB. So 160MiB/sec throughput per Segment maps to VD of 800GiB size.
            11. Pangu distributed lock service
            12. LZ4 compression (latency-optimized)
                1. the compression ratio of the LZ4 algorithm is between 43.3% ∼ 54.7%

    n. Related materials
        1. 阿里云EBS架构演进 - 黄岩gg
           https://zhuanlan.zhihu.com/p/684333453

        2. 阿里云高性能EBS的架构演进 - KDF5000
           https://zhuanlan.zhihu.com/p/686239323

        3. AWS Physalia: Millions of tiny databases    [2020, 27 refs, NSDI20]
           https://www.usenix.org/conference/nsdi20/presentation/brooker
            1. Introduction of "Blast Radius" and "Cell Architecture".
                1. Referenced in Alibaba EBS paper as "AWS Physalia [24] deploys small units called cells, each of which consists of seven nodes deploying Paxos algorithms and serves a group of VDs"

        4. 鲲鹏 Kunpeng 920: The first 7-nm chiplet-based 64-core ARM SoC for cloud services    [2021, 48 refs, IEEE Micro, Huawei]
           https://ieeexplore.ieee.org/abstract/document/9444893
            1. Referenced as "Kunpeng 920 ARM CPU [41]"
        
        5. 倚天 Yitian 710: Alibaba Cloud unveils new server chips to optimize cloud computing services
           https://www.alibabacloud.com/blog/598159?spm=a3c0i.23458820.2359477120.113.66117d3fm03t9b
            1. Referenced as "Yitian 710 ARM CPU [9]"

4. SquirrelFS: using the Rust compiler to check file-system crash consistency    [2024, 0 refs, OSDI24]
   https://www.usenix.org/conference/osdi24/presentation/leblanc
   https://arxiv.org/html/2406.09649v1
    1. There are quite a few papers that leverage Rust to reshape PMEM programming to make filesystem code safe. This is a good direction to further explore. Unlike Golang, Rust did change a lot of things.
    2. Highlights
        1. Rust typestate used in SuirrelFS can be thought as a common design pattern in system programming. The main advantages are it's practical, convenient to use, and fast to run verification. Note it's doesn't provide full coverage like formal verification Alloy. Formal verification however is expensive to use and very slow to run.
        
        2. Rust typestate is convenient and very useful tool for memory operating safety. By using PMEM with synchronous operations, this paper extends to reach to filesystems, to build crash consistency.
        
        3. Note the typestate is convenient programming tool but not a full protection to safety, unlike formal verification. A mistype, bad design, or some coding flaws can still let something miss out the protection.
        
        4. Soft updates gain favor on PMEM because it's update in place, doesn't incur extra copying. Because CPU is slower than PMEM, soft updates can be made simpler that each operation is made sychronious in function call, called Synchronous Soft Update (SSU). Then Rust typestate can easily be used here extending from memory safety techniques. All seem a good fit here. Also, in SquirrelFS Rust, compile is as fast as tens seconds to run all typestate checks.
        
        5. Typestate programming: https://docs.rust-embedded.org/book/static-guarantees/typestate-programming.html
        6. SquirrelFS at github: https://github.com/utsaslab/squirrelfs, 
           Alloy model checking: https://github.com/utsaslab/squirrelfs/blob/main/model_checking/model_auto.als 
        7. ShardStore is a Rust key-value store used in Amazon S3 that uses an asynchronous soft-updates-inspired crash-consistency mechanism.

        8. The original soft updates rules [43]:
            1. Never point to a structure before it has been initialized.
            2. Never re-use a resource before nullifying all previous pointers to it.
            3. Never reset the old pointer to a live resource before the new pointer has been set.
    3. Others
        1. This work is by Hayley LeBlanc etc at internship at Microsoft
    
    4. My questions
        1. How is compilation time made so fast?
            1. It should be due to SquirrelFS program is small and the Rust typestate checks are cheap enough to compile. Formal verification however takes a long time to convert program into Alloy code and needs to solve NP-hard problem and to iterate through many combinations states.
        2. Is SSU used in any other filesystems?
            1. Looks like SSU is coined in SquirrelFS paper, not used elsewhere.
        3. Using PMEM with synchronous operation (Synchronous Soft Updates)
            1. This greatly simplified implementation. It looks reasonable because PMEM is faster than CPU. But I didn't many papers prompting the same.
    
    n. Related materials
        1. Corundum: Statically-Enforced Persistent Memory Safety    [2021, 27 refs]
           https://cseweb.ucsd.edu/~mhoseinzadeh/hoseinzadeh-corundum-asplos21.pdf
            0. The parent paper is inspired by Corundum.
            1.
            2. Highlights
                1. PMEM smart pointers for dynamic allocation
                2. PMEM wrappers for interior mutability
                3. Corundum features
                    1. Mutable in transaction only
                    2. Transaction are atomic
                    3. No cross pool referencing
                    4. No acyclic memory leaks
                        1. Cyclic references may still leak, this is a common issue in reference counting memory management. See Section 3.9 Limitations.
                    5. Ease of use on Rust more than PMDK on C++
                4. Orthogonal Persistence
                    1. Interesting concept. It needs to:
                        1. Using the same code for transient and persistent data
                        2. Any data type can be persistent
                        3. Not expressing persistence in the type system
                    2. Not practical now. Even this paper is NOT doing it.

4. These Rows Are Made for Sorting and That's Just What We'll Do    [2023, 3 refs, DuckDB, ICDE23]
   https://hannes.muehleisen.org/publications/ICDE2023-sorting.pdf
    1. Optimizing sort into details. Row-wise vs columnar, cache misses, branch misses, biased data patterns.
    2. Highlights
        1. We implement a highly optimized row-based sorting approach in the DuckDB
            1. See Fig.9, DucksDB is a columnar OLAP, the sort pipeline needs to convert vectors to rows first.
            2. DucksDB is using a vectorized interpreted query engine, rather than JIT code generation engine.
        2. In systems with a vectorized interpreted engine, however, the efficiency of sorting rows is hindered by interpretation and function call overhead in the comparison function. To overcome this overhead
            1. key normalization, pre-compiled memcpy and memcmp, and radix sort. 
            2. Radix sort, however, is less effective when sorting strings. In this case, a comparison-based sorting algorithm like pdqsort is superior.
    n. Related materials
        1. 怎样把数据库排序做到全球第一？ - 红星闪闪
           https://zhuanlan.zhihu.com/p/664312966
            0. Good paper review.
            1. 决定数组排序性能的因素：
                1. 算法复杂度：O(NlogN)的排序性能通常远优于O(N^2)的排序。
                2. 减少CacheMiss：尽可能顺序访问，或者限定随机访问的范围。
                3. 避免分支预测失败：尽可能减少分支判断。
                4. 提升并行度：多线程排序。
                5. 特殊pattern检测：监测特殊的pattern（比如：基本有序、和目标排序刚好相反），针对不同的pattern采用不同的排序算法。pdqsort是这方面的典范。
            2. 数据库排序需要额外考虑的因素
                1. Compare和Move（Swap）原子操作：比较两个值大小和移动值是排序算法中的基本操作，这两个操作的性能需要精心优化。此外，数据库的比较操作更为复杂，因为SQL中的OrderBy子句可以写的很复杂，且包括各种类型。
                2. 执行引擎的影响：现在的OLAP数据库系统主要分为向量化（VectorWise）和代码生（HyPer）成两大流派。虽然针对这两种执行引擎已经有过较为详细的比较研究，但是在排序这个细分领域还没有一个确切的结论。
                3. 行存和列存：这篇论文给出一个结论：行式存储更有利于排序，即使在列存场景下也是这样。也就是说，行排序获得的收益大于额外进行列转换的开销。这个结论非常有用，因为现在的OLAP数据库系统通常是列式存储，这意味着基本上所有OLAP数据库都可以通过行列转换来提升排序性能。行列转换运用于排序如下图所示，先将列式数据转换成行式，对行式数据排序后再转换成列式输出。
            3. 数据分布，例子：
                1. Random：所有数据随机生成
                2. Unique128：只有128个数据，均匀分布
                3. PowerLay：只有128个数据，幂为5的幂率分布，和Unique128很像，但是倾斜严重
            4. 列存的逐行排序有三大性能问题：
                1. CacheMiss 1：如果第一列的数据相同，则需要比较第二列，这里会有一次随机访问，因为在列式存储下，第一列中的数据和第二列的数据在内存上不连续。频繁的随机访问会导致严重的CacheMiss进而影响性能。数据集中重复值越多，这个问题会越明显，所以Unique128和PowerLay较之于Random分布CacheMiss会更严重。
                2. CacheMiss 2：通常的排序算法会Swap真实的数据，随着排序的进行，数据的局部性会逐渐变好，进而降低CacheMiss。但是在列存逐行排序中，每次Swap交换的是row_id，而不是真实的数据，每次根据row_id获取真实值都是一次随机访问，CacheMiss严重
                3. BranchMiss：比较函数有较多的分支。由于具体走到哪个分支和排序的数据相关，所以CPU很难做到准确的分支预测。相同值较多的数据集会有更多的BranchMiss，因为第一列相等还需要比较第二列，会走到更多的分支，分支预测失败的可能性更大。
            5. 列存的逐列排序
                1. 列存数据排序都是对行号（row_id）排序，最后根据行号物化出最终的有序结果。逐列排序每次Swap同时交换原始数据和row_id。如果有相同值范围，使用对应的row_id取出下一列的数据，继续进行排序。
                2. 实验测试
                    1. 可以看出，无论是排序列多少，数据量多少，数据分布如何，在列存场景下，列存的逐列排序全面优于列村的逐行排序。
                    2. 和列存做横向对比，无论是CacheMiss还是BranchMiss，行存的两种排序方法都有量级上的提升。
            6. DuckDB的四板斧
                1. 数据结构角度：基于行存的排序全面优于基于列存的排序
                2. 排序方法角度：逐行排序和逐列排序各有千秋：
                    1. 逐行排序的应用面更广（比如Merge），CacheMiss更少，但是解释执行开销大
                    2. 逐列排序的解释执行开销较小
                3. 综合考量下，这篇论文选择了基于行存的逐行排序，但是需要解决前面发现的问题，消除劣势，扩大优势。
                4. 端到端测试
                    1. DuckDB is even faster than HyPer, ClickHouse. 1千万~1亿数据行。
            7. 高效Merge
                1. 如果直接对全量数据进行排序，会有较为严重的CacheMiss。更好的做法是多线程并发排序，如下图所示：每一个线程一次排Cache大小的数据，这样的CacheMiss会很少。最后需要一个Merge逻辑来将多个有序向量合并成一个全局有序的结果。
                2. DuckDB采用级联的两两归并来实现Merge，性能好好。两两归并，简化了比较逻辑，进而简化了判断分支，同时也从N路归并的每次访问N块不连续内存缩减为2块不连续内存，Cache更友好。级联归并可以尽可能利用多线程提速。
                3. 我们希望在两两归并时，每一个Merge处理的数据量相等（没有倾斜）。这需要对SortedVector进行合理的切分，让Merge完的结果刚好可以拼接成一个完整的有序结果，如下图所示。找到切分点的算法称为MergePath，MergePath算法会运用二分查找的思路快速定位分割点，详见《Merge Path - A Visually IntuitiveApproach to Parallel Merging》
            8. Others
                1. Normalized Keys
                    1. Normalized Keys就是将多个排序列，以某种编码方式，序列化成一个String列，之后直接对序列化后的String列进行排序。
                2. memcpy 动态调用 vs 静态调用
                    1. 在ARM架构上，当size小于16时，memcmp静态调用平均比动态调用快25%。其他情况静态调用性能更差
                    2. 在ARM架构上，memcpy静态调用平均比动态调用快55%，当size小于16时，平均快92%，当size小于8时，平均快121%
                3. RadixSort
                    1. 当key size <= 4 byte，使用LSD（Least Significant Digit）Radix Sort
                    2. 当key size > 4 byte，使用MSD（Most Significant Digit）Radix Sort

        2. Fastest table sort in the West - Redesigning DuckDB's sort    [2021, DuckDB]
           http://bit.ly/duckdb-sort
            1. Fig.9 "DuckDB's fully parallel sorting pipeline [28]" as referenced in the parent paper.
                1. "Full sorting pipeline in DuckDB. Incoming vectors from worker threads (illustrated as T1 and T2 in the figure) are converted to 8-byte aligned row formats. Key columns are normalized and stored separately from the payload. The normalized keys are sorted with radix sort or pdqsort, creating sorted runs. The sorted runs are then partitioned and merged in parallel until one run remains. Finally, the result is converted back to vectors."
            2. DuckDB uses Morsel-Driven Parallelism
            3. This article is mostly overlapping with the parent paper.
            4. Appendix A: Predication
                1. With this technique, we turn code with if/else branches into code without branches
            5. Appendix B: Zig-Zagging
                1. By zig-zagging through the blocks, we start an iteration by merging the last blocks that were merged in the previous iteration. Those blocks are likely still in memory, saving us some precious read/write operations.

        3. Why DuckDB?
           https://duckdb.org/why_duckdb.html
            1. Embedded database, in-memory, like SQLite but targeting OLAP.
            2. DuckDB contains a columnar-vectorized query execution engine, where queries are still interpreted, but a large batch of values (a "vector") are processed in one operation

        4. DuckDB: an Embeddable Analytical Database    [2019, 191 refs, SIGMOD]
           https://mytherin.github.io/papers/2019-duckdbdemo.pdf
            1. Introducing DuckDB, can be read with "Why DuckDB" article.
            2. Highlights
                1. Scenarios
                    1. edge computing
                    2. Database components
                        1. API
                        2. SQL Parser
                            1. derived from Postgres' SQL parser
                        3. Optimizer
                            1. Cost-Based
                            2. Join order optimization with dynamic programming
                            3. Cardinality estimation by samples and HyperLogLog
                        4. Execution Engine
                            1. Vectorized interpreted execution engine
                            2. JIT engines was not chosen because it depends on massive compiler libraries (e.g. LLVM)
                        5. Concurrency Control
                            1. ACID, MVCC
                            2. We implement HyPer's serializable variant of MVCC that is tailored specifically for hybrid OLAP/OLTP systems [10]. This variant updates data in-place immediately, and keeps previous states stored in a separate undo buffer for concurrent transactions and aborts.
                                1. HyPer: Fast Serializable Multi-Version Concurrency Control for Main-Memory Database Systems    [2015]
                            3. MVCC was chosen over simpler schemes such as Optimistic Concurrency Control because, even though DuckDB's main use case is analytics, modifying tables in parallel was still an often-requested feature in the past.
                        6. Storage
                            1. read-optimized DataBlocks storage layout
                            2. Logical tables are horizontally partitioned into chunks of columns which are compressed into physical blocks using light-weight compression methods.
                            3. Blocks carry min/max indexes for every column

5. We Ain't Afraid of No File Fragmentation: Causes and Prevention of Its Performance Impact on Modern Flash SSDs    [2024, 3 refs, FAST24 Best paper, Samsung]
   https://www.usenix.org/conference/fast24/presentation/jun
    1. Very good paper. It first time revealed SSD file fragmentation is due to read-related pages are undesirably put to the same die, which makes SSD unable to leverage die-level parallelism in reads. 
       SSD fragmentation read perf degradation happens when fragments size are < 128KB. In future, follow up papers can work in defragmentation improvements in many aspects.
       Page-to-die mapping solution NVMeVirt simulation shows 10%~20% improvement on SQLite and fileserver. 
    2. Highlights
        1. SSD file fragmentation today
            1. Where can it happen?
                1. Kernel IO path, storage device interface
                    1. Fragmentation causes more IO requests, which incurs more overhead in kernel operation and more commands sent to storage device
                        1. This is the prior arts of SSD fragmentation, as in Fragpicker [31]
                        2. This is identified as no the major impact in this paper, e.g., comparing Figure 3 vs Figure 4 (ramdisk) when Degree of Fragmentation (DoF) is larger than 128.
                2. Storage media
                    1. SSD reads need all dies to serve in the paralleled way. But a file's fragments can happen to be placed in the same die. Although an SSD stripe should choose dies in round-robin way for contiguous writes.
            2. What usage pattern causes fragmentation?
                1. Appends, but two files interleave their appends
                    1. See Figure 9 and Figure 10. I.e., die-level collision.
                2. Overwrite
                    1. I.e. Aging. The new rewritten page is put to other dies with has collision with existing pages.
                3. File is fragmented, due to (1) (2) above.
            3. What's the typical solutions against SSD fragmentation
                1. Delayed write - i.e. Filesystem plug and flush
                2. Extent based allocation, pre-allocation
                    1. Problem today: page-to-die mapping isn't determined in pre-allocation. When the write happens in a delayed way, it may write to another die that still causes die-level collision.
                    2. My questions
                        1. Looks like improving extent-based allocation should be the right way. But why this paper is heading for another page-to-die mapping solution?
                3. Page-to-die mapping, as is this paper proposed solution
                    1. For append, hint the NVMe command where's the immediate previous page. Per overwrite, write to the same die.
                4. Defragmentation, said to be expansive in this paper.
                    1. XFS's xfs_fsr sorts files by their number of extents and groups the top 10% of files into a unit called a pass, performing defragmentation for each pass [27]
                    2. F2FS defragmentation tool allows user-selected area. Btrfs's defragmentation tool only targets extents smaller than the specified size.
        2. Evaluation
            1. Analysis on fragmentation issue on commercial SSD disks.
                1. See Figure 8, interesting technique to probe die allocation granularity and stripe size.
                2. Specifically alter write size to make all fragments are placed in the same die, to get the worst performance.
                    1. See Figure 11 and it's explanation text in paper
            2. Page-to-die mapping is only implemented on simulator, in NVMeVirt.

    n. related materials
        1. 文件碎片造成SSD性能退化的根本原因真的如FAST 2024 Best Paper所说，是die-level collisions吗？ - 暗淡了乌云
           https://zhuanlan.zhihu.com/p/693732364
            1. Fragpicker[3]: 发现当frag size<128KB的时候，frag size越小，性能越差（Matching parent paper Figure 7）。
               在这个观察下，认为传统文件碎片整理的方法将文件从头到尾扫描整理一把，就没有必要了，其实只需要做适当的整理，保证连续文件的frag size >= 128K就好了。
            2. 其实文献[3]主体研究和方案没有问题，只是在解释frag size变小后，性能退化的原因描述的时候，它只分析到时因为request splitting这一层，就没有继续详细分析（如下图），它大概描述了request splitting造成性能退化的多个原因：（1）io number增加，造成小IO内核拆分合并开销；（2）Make IO smaller；（3）底层盘Channel conflict；。至于这3个原因那个占比更大，其实对文献[3]来说，它并不关心，并不影响它进行碎片整理的优化。

6. Amazon MemoryDB: A Fast and Durable Memory-First Cloud Database    [2024, SIGMOD24]
   https://www.amazon.science/publications/amazon-memorydb-a-fast-and-durable-memory-first-cloud-database
    1. Mounting Redis on an internal AWS shared-log service, it greatly simplifies building durability, strong consistency, snapshot, resharding, etc.
       This is another example that a shared-logging is extremely useful in building distributed storage service, as in AWS Aurora, Azure Storage, Apple FoundationDB - Log is the database.
    2. highlights
        1. The internal AWS transaction log service
            1. Cross Availability Zones (AZ)
            2. MemoryDB uses a Leadership Mechanism atop the transaction log
                1. This is the Good part. Use a shared-logging service to implement leadership election
                2. The transaction log service provides a Conditional Append API
                    1. Each append request must specify the identifier of the log entry it intends to follow as pre-condition. Leadership is granted to the only one participant that succeeded the append. The log entry registers the winner.
                    2. Only fully caught up instances can become the primary, because it needs to append to log tail.
                3. Lease by the transaction log service
                    1. Leader periodically renews its lease by appending an log entry
                4. Failure detection by a gossip protocol called Redis cluster bus
            3. Durability and availability
                1. Via the transaction log service. It's decoupled from the Amazon MemoryDB itself.
            4. Strong consistency
                1. The transaction log is synchronized replication.
                2. Sequential but eventual consistency - "Reading from multiple nodes, e.g., load balancing reads across multiple replicas, yields an eventually consistent view of the data set."
            5. Passive Replication
                1. Primary node writes updates to the transaction log. Replicas gets updates from the transaction log.
                    1. My questions
                        1. The design is so much similar with AWS Aurora multi-master
                2. Use write-behind logging rather than write-ahead logging.
                    1. It fits Redis replication model. It allows MemoryDB to support non-deterministic commands, such as SPOP
                    2. Response will be delayed until an update is persisted
            6. Snapshot
                1. Snapshot is taken periodically, it's like the checkpoint + log for recovery.
                    1. Non-snapshotted log length is monitored and limited. So as to bound recovery time.
                2. Snapshot is stored in AWS S3.
                3. Off-box snapshot using ephemeral VMs. Both user and DB instances are not spending extra resource.
                    1. This is an interesting design.
                4. Snapshot is verified for correctness
                    1. Compare with the equivalence to the original transaction log
                    2. Transaction log has a running checksum
                    3. Rehearsing restoring MemoryDB from an off-box cluster
            7. Resharding
                1. Changing the number of shards cause re-sharding, where data movement happens between replicas.
                2. Ownership transfer is by logging slot ownership in the transaction log.
                    1. It needs the transaction log from 2 shards, acting like a 2PC
                    2. Right before the ownership transfer, the source will block all incoming writes, and then perform a integrity handshake that transfers ownership to the dest.
                    3. Abandon the transfer is cheap and simple.
                3. Slot movement / data movement is used in N+1 rollout upgrade, re-sharding, machine scale-up, slot migration.
                    1. A slot is a unit of the key space used for horizontal scaling.
                       Redis, which MemoryDB is based on, splits its flat key space into 16,384 slots using the CRC16 algorithm
        
        2. Formal verification and consistency checker
            1. Formal Verification
                1. "MemoryDB uses P [23] as well for new feature development, which proved helpful in reasoning about the overall system and in catching bugs early in the development process"
            2. Consistency Testing Framework
                1. "We use porcupine [17], a linearizability checker, to test MemoryDB consistency"
                2. "We parse the API specification provided by the engine and generate commands based on the output"
                3. "Similarly to [19], we leverage argument biasing to improve our testing coverage, especially around edge-cases."
                    1. [19] Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3
                       https://assets.amazon.science/07/6c/81bfc2c243249a8b8b65cc2135e4/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3.pdf
                        1. "Argument bias. We apply biases in the property-based testharnesses when selecting arguments for operations in a test's alphabet. ... We also bias argument selection towards corner cases."
                            1. Interesting concept "Argument Biasing".

        3. Evaluation
            1. Figure 4. MemoryDB is slower at write-only workloads due to durability overhead.
            2. Figure 6. BGsave hits Redis performance significantly. Mainly due to extra memory usage and swap
                1. Redis extra memory usage is due to the fork system call which clones the entire memory page table
                    1. Section 4.2.2 "Redis creates snapshots of in-memory data by forking the database process"
                        1. My questions
                            1. How does the OS fork maintain crash consistency? It seems missing an operation of filesystem flush/quiescing.
                1. This is why off-box cluster snapshot is effective.

        4. Others
            1. Where Redis is being used? Real-time applications such as Finance, Advertising, and Internet-of-Things (IoT) applications
            2. How AWS uses Redis? "Amazon ElastiCache [1]. Many ElastiCache for Redis customers use Redis as their main data store"
            3. What's AWS MemoryDB's usecase scenario?
                1. Due to Redis lack durability, AWS customers traditionally uses Redis + DynamoDB, but which is complex.
                2. Redis's primary and replicas are not strongly consistent, customer must opt-in to avoid reading stale data from the replicas
    
    n. related materials
        1. [SIGMOD 2024] Amazon MemoryDB: A Fast and Durable Memory-First Cloud Database - 张建
           https://zhuanlan.zhihu.com/p/697669995

        2. 从一到无穷大 #27 从Amazon MemoryDB视角看稳定binlog带来的无限可能性 - 大家好大家吃了吗
           https://zhuanlan.zhihu.com/p/704955846

7. Is Garbage Collection Overhead Gone? Case study of F2FS on ZNS SSDs    [2023, 9 refs, HotStorage23]
   https://people.cs.vt.edu/huaicheng/p/hotstorage23-zgc.pdf
    1. F2FS has significant GC overhead on ZNS SSD unless taking significant amount of over-provisioning space.
       This paper proposes Parallel Garbage Collection (P-GC), to relieve GC overhead with multi-thread parallelism.
    2. Highlights
        1. F2FS on ZNS SSD
            1. Segment size is 2MB. Segment is the basic unit that F2FS manages. 
        2. GC overhead of F2FS on ZNS SSD
            1. Given 7%-28% over-provisioning space, F2FS does NOT show GC overhead on ZNS SSD even in high utilization.
                1. See Figure 4 for Ovp. vs throughput perf. Reserving 10 sections, 42% Ovp strikes a middle balance between Ovp. vs perf.
                    1. My questions
                        1. 42% Ovp is probably NOT acceptable in production. It's too much wastage in COGS. And ZNS SSD is expected to reduce Ovp overhead than the conventional SSD.
            2. Low over-provisioning space config, however, results in application crashes in high utilization.
                1. Parallel Garbage Collection (P-GC) is proposed for this scenario
        3. Parallel Garbage Collection (P-GC)
            1. Motivating problem: F2FS on ZNS SSD has high GC overhead, unless reserve a great amount of over-provisioning space.
            2. Reduce F2FS GC overhead by breaking GC process into multiple threads.
                1. GC with parallelism when the number of valid blocks exceeds half of the blocks per segment. The threshold is to justify the overhead of parallelizing in GC.
            3. Free segment-finding policy / Free segment search
                1. Added a retry that checks free sections. This reduces the risk of crash.

    n. Related materials
        1. ZNS+: Advanced Zoned Namespace Interface for Supporting In-Storage Zone Compaction    [2021, 65 refs, OSDI21]
           https://www.youtube.com/watch?v=QjrPiWrfM3k
            1. Logged elsewhere

        2. A New LSM-style Garbage Collection Scheme for ZNS SSDs    [2020, 42 refs, HotStorage20, SK Hynix]
           https://www.youtube.com/watch?v=csD-wsJfrDc&t=568s
            1. Track 2MB/4MB segment inside the 1GB zone size. So GC can separate hot/cold segments into different new zones. Besides, copying segments leverage the internal parallelism within a zone.
            2. Highlights
                1. How LSM ZGC work exactly?
                    1. It works in filesystem rather than in ZNS SSD
                    2. A segment in the context of ZNS SSDs is a smaller unit within a zone. Specifically, a segment is typically 2 MB or 4 MB in size, whereas a zone is much larger, often around 0.5 GB or 1 GB. This means a zone consists of multiple segments.
                        1. Track 2MB/4MB segment inside the 1GB zone size. This is an interesting design.
                            1. My questions
                                1. If the file size is 100MB, would the segment cold/hot segregation undesirably break the file sentimentality and introduces fragmentation? But maybe SSD can work with fragmentation well (with the "We Ain't Afraid of No File Fragmentation" paper).
                    3. LSM ZGC (Log-Structured Merge style Zone Garbage Collection) works by dividing a zone into multiple segments and managing their information individually, such as validity bitmap and utilization. It conducts garbage collection in an LSM style by reading all data from a candidate zone, identifying cold data, and merging them into a separate zone while merging the remaining data into another zone. This segment-based approach allows for fine-grained garbage collection, enabling effective hot/cold data segregation and reducing garbage collection overhead by exploiting internal parallelism within a zone.
                        1. Zone transitions through various states, including C0, C1C, C1H, and C2. This is how LSM concept come in. This manages and segregates cold data.
                4. Evaluation
                    1. SK Hynix prototype ZNS SSD - 1TB capacity, 1GB zone size
                        1. My questions
                            1. Why zone size is so large, given an flash block is only MBs?

        3. F2FS: A New File System for Flash Storage    [2015, 588 refs, FAST15]
           https://www.usenix.org/system/files/conference/fast15/fast15-paper-lee.pdf
```
