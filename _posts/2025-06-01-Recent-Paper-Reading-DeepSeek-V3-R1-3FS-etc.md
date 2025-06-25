---
layout: post
title: "Recent Paper Reading: DeepSeek-V3, R1, 3FS, etc"
tagline : "Recent Paper Reading: DeepSeek-V3, R1, 3FS, etc"
description: "Recent Paper Reading: DeepSeek-V3, R1, 3FS, etc"
category: "Paper Reading"
tags: [paper, cloud, LLM, AI, ML]
---
{% include JB/setup %}


```
1. DeepSeek 3FS: https://github.com/deepseek-ai/3FS/tree/main
    0. 3FS release highlights
        1. Performance: 6TiB/s sustained throughput with 180 storage nodes => 300Gbps per node
        2. Architecture: FoundationDB for cluster metadata, RocksDB for storage node metadata, CRAQ for consistent replication supported parallel reads
        3. Rigor: both storage node and network (RDMA) protocol are formally modeled in thousands of lines of P specification language
        4. Very good.
    
    1. DeepSeek 3FS GitHub Design Notes
       https://github.com/deepseek-ai/3FS/blob/main/docs/design_notes.md
       https://github.com/deepseek-ai/3FS
        1. Apple FoundationDB, FUSE, Chain replication & CRAQ, P Specification.
        2. Highlights
            1. Chain replication with CRAQ (Data replication)
                1. Write requests are sent to the head target and propagated along a chain. Read requests can be sent to any of the storage target
                2. Per File interface, 3FS is update-in-place. But per storage node chunk engine, it's COW updates.
                    1. See https://github.com/deepseek-ai/3FS/blob/main/docs/design_notes.md#chunks-and-the-metadata
                3. Interesting. "Utilizing read bandwidth of all replicas is critical to achieve highest read throughput in an all-flash storage system"
                4. Write workflow
                    1. Storage only accepts a rewrite request carrying the latest known version
                    2. Storage uses RDMA read operation to pull write data from client
                    3. Acquire a lock for the chunk being updated, block concurrent updates
                    4. Version management - strictly increment per version per chunk
                        1. A storage target can store two versions: committed vs pending, version is n vs n+1.
                    5. A storage node only replaces commit version with pending version after its successor acked. So unlock & replace starts from the tail node.
                    n. My questions
                        1. Looks like the protocol doesn't require any write to fail, as long as it is written to the head node.
                5. Read workflow
                    1. When the service only has a committed version of the chunk, this version is returned to the client.
                    2. When there are both committed and pending versions
                        1. Unlike CRAQ, our implementation does not issue version query to the tail target
                        2. the service replies a special status code to notify the client. The client may wait for a short interval and retry. Or the client can issue a relaxed read request to get the pending version.
            
            2. Apple FoundationDB
                1. My questions
                    1. Suppose I'm looking for an opensource scaleout KV DB, looks like FoundationDB is the only choice. It also supports ACID transaction.
                        1. RocksDB is commonly used for metadata management, but it is single-noded.
                        2. Facebook Tectonic is using ZippyDB, but ZippyDB is not opensourced
                            1. https://github.com/SpanDB/SpanDB/blob/master/USERS.md (SpanDB is not from Facebook)
                        3. Apple FoundationDB on Github is highly recognized
                             https://github.com/apple/foundationdb
                           And with nice documentation
                             https://apple.github.io/foundationdb/getting-started-linux.html
                        4. TiKV, CockroachDB are full-feature database, too heavy to use as a sub-component in FS, and probably with licensing problem 
                        5. FoundationDB supports distributed transaction. This is a good feature for KV DB.
                2. FoundationDB provides a key-value store interface and supports transactions with Serializable Snapshot Isolation (SSI)
                3. FoundationDB supports fast restart without disruption, see its paper, this is nice for admin and upgrade
                4. Distributed transactions for atomic directory operation
                    1. Use FoundationDB's transaction support for atomic create, link, unlink, rename et
            
            3. Distributed transactions for atomic directory operation
                1. Just leverage FoundationDB's transaction. 
                    1. Good. This so simply solved the the core problem of distributed FS.
                    2. Facebook Tectonic only implemented per shared transaction.
                    3. HopsFS [2017] implements its own complex transaction protocol
            
            4. Interfaces
                1. File system interfaces
                    1. Atomic directory manipulation
                        1. Frequent usecase: creating a temporary directory, writing files to it, and then moving the directory to its final location
                        2. This is a key difference with Object Storage - atomic directory operation
                            1. Good remarks. File and Object storage are converging. We should see transactional object storage soon.
                    2. Symbolic and hard links
                        1. Frequent usecase:  create lightweight snapshots of dynamically updated datasets
                    3. Familiar interface
                       1. Frequent usecases: Many datasets are stored as CSV/Parquet files
                2. Limitations of FUSE - Performance limitation
                    1. Memory copy overhead
                        1. Data transfer between kernel and user spaces
                    2. Primitive multi-threading support
                        1. FUSE places these requests into a multi-threaded shared queue, protected by a spin lock
                        2. Our benchmark results indicate that FUSE only handles approximately 400K 4KiB reads per second
                    3. Others
                        1. FUSE on Linux 5.x does not support concurrent writes to the same file
                        2. Read operations insufficient to support random read
                            1. Some training jobs require random access to dataset samples, with read sizes varying from a few kilobytes to several megabytes per sample. And samples are typically not 4K-aligned in files
                            2. Data loaders are specifically designed to fetch batches of samples. But they perform poorly when handling small random reads on FUSE-mounted 3FS
                    4. Why choose FUSE instead of kernel VFS?
                        1. Kernel development is more challenging than userspace, e.g. debugging in production environment
                        2. Need upgrade without interrupting user processes nor restart machine
                3. Out FUSE implementation - a native client within the FUSE daemon
                    1. asynchronous zero-copy I/O operations - inspired by io_uring
                        1. USRBIO API Reference
                           https://github.com/deepseek-ai/3FS/blob/main/src/lib/api/UsrbIo.md
                        2. Good. This can be generalized per using FUSE. It has broken the limit as previously mentioned for FUSE
                    2. requests are batched to reduce RPC overhead caused by small read requests

            5. Data placement
                1. File -> equally sized chunks -> striped across multiple replication chains
                    1. Users can specify the chain table, chunk size, and stripe size for files on a per-directory basis
                        1. Interesting interface design
                2. When creating new file, select consecutive replication chains from chain table (round-robin), and then shuffle
                    1. Chain is composed by "target" rather than node nor SSD. Each SSD creates multiple targets.
                3. Each chain has a version number. The version number is incremented if the chain is changed
                    1. Managed by primary cluster manager
                4. Chain tables can be constructed to support different data placement requirements
                    1. Two chain tables can be created, one for batch/offline jobs and another for online services. 
                        1. The two tables consist of storage targets on mutually exclusive nodes and SSDs.
                5. To balance traffic during node recovery, each chain needs to cover a different set of nodes.
                    1. the load balance problem can be formulated as a balanced incomplete block design. The optimal solution is obtained by using integer programming solver.
                    2. My questions
                        1. Interesting. Note, chain table need to be updated on the fly upon node failure.
                        2. Note chain table needs to be generated upon deploy
                           https://github.com/deepseek-ai/3FS/tree/main/deploy/data_placement

            6. Metadata management
                1. Dynamic file attributes
                    1. 3FS maintains a file session for each file descriptor (fd) opened in write mode
                        1. Omit read-only fd. Training jobs can open a lot of files for read
                        2. Defer file deletion until all fd released
                            1. 3FS meta service periodically checks client liveness
                    2. Concurrent update on file length
                        1. To avoid transaction conflicts, "meta service distributes file length update tasks across multiple meta services using inode IDs and the rendezvous hash algorithm"
                        2. File length is eventual consistency. Meta service obtains it by querying the the last chunk
                    3. Track potentially used chains in file inode, to avoid scanning through up to 200 chains. Initial value 200
                2. The metadata services are stateless. - Interesting design from FoundationDB
                    1. The list of online meta services provided by cluster manager is a simple service discovery mechanism that helps clients create connections to metadata services. 
                    2. If one meta service is down, the clients may switch to any other metadata service.
                3. Cluster manager is different from metadata service
                    1. Cluster manager is in charge of detecting failure node and to update chain table
                    2. Metadata service is responsible to store and operate inode, dentry.
                    3. Cluster manager also uses FoundationDB, like Metadata service, this is to reduce dependency. Otherwise Cluster manager typically uses ZooKeeper or etcd.

            7. Failure detection
                1. Heartbeat + fail-stop
                    1. A service stops processing requests and exits if it cannot communicate with cluster manager for T/2 seconds
                        1. My questions
                            1. Self-kill after losing heartbeat. This is an interesting design
                2. Public state vs local state
                    1. Public state is known by public and indicates whether a node can serve requests: serving, syncing, waiting, lastsrv, offline
                    2. Local state is only known by storage service and cluster manager. It is used to trigger transition of public state: update-to-date, online, offline
                    3. Public/local state are associated to storage targets, node storage node

            8. Data recovery
                1. Once the service restarts, each target on the service enters into the recovery process independently. 
                2. recovery process overlaps with normal activity.
                3. recovery workflow
                    1. Replicate by full-chunk-replace write
                    2. The recovering node sends a dump-chunkmeta to its predecessor, so that predecessor can decide which chunks to send

            9. Storage node - Chunks and the metadata
                1. Components
                    1. Chunk Engine - fixed number of data files to store chunk data
                    2. RocksDB - managing chunk metadata
                    3. In-memory cache to speedup chunk metadata query
                    4. A chunk allocator for fast allocation of new chunks
                2. Key designs
                    1. update Implements copy-on-write (COW) semantics 
                        1. By allocating new chunks before modifying data. Old chunks remain readable until all handles are released.
                    2. Commit the updated chunk metadata to RocksDB via write batches to ensure atomic updates
                    3. The chunk data will ultimately be stored on physical blocks. 
                        1. Physical block sizes range from 64KiB to 64MiB in increments of powers of two, totaling 11 distinct sizes. 
                        2. Bitmap allocation management. 
                            1. A resource pool for each physical block size. 
                            2. Each pool maintains 256 physical files.
                            3. Each file contains multiple blocks.
                    4. COW - Copy-on-Write
                        1. When performing write operations on a chunk, the allocator first assigns a new physical block. The system then reads existing chunk data into a buffer, applies the update, and writes the updated buffer to the newly allocated block.
                        2. An optimized process is implemented for appends, where data is directly added in-place at the end of the existing block.
                        3. A new copy of metadata is constructed from the new block's location and existing chunk metadata. Subsequently, both the new chunk metadata and statuses of new and old physical blocks are atomically updated in RocksDB.
                        n. My questions
                            1. This COW write seem a natural match to the committed/pending versions in write workflow

            10. P specifications
                https://github.com/deepseek-ai/3FS/blob/main/specs/README.md
                1. Intro
                   https://p-org.github.io/P/whatisP/
                    1. Compared to TLA+, P Specification is much more friendly to programmer. P Specification works on state machines.
                        1. Currently P checker doesn't do proof on correctness. But P can do codec generation.
                    2. The P checker employs search prioritization heuristics to drive the exploration
                        1. Systematic Testing of Asynchronous Reactive Systems    [2015, 41 refs]
                           https://ankushdesai.github.io/assets/papers/fse-desai.pdf
                            1. Ankush Desai, Shaz Qadeer, Sanjit Seshia. They are the authors of P Specification
                2. Industry adoption
                    1. P Specification
                        1. Microsoft (used in USB3, IoT, and Async Event Handling)
                            1. https://www.microsoft.com/en-us/research/blog/p-programming-language-asynchrony/
                            2. https://en.wikipedia.org/wiki/P_(programming_language)
                            3. https://www.microsoft.com/en-us/research/project/safe-asynchronous-programming-p-p/
                        2. DeepSeek (used in 3FS)
                    2. TLA+
                        1. AWS (used in DynamoDB, S3, EBS)
                            1. 
                            2. https://www.amazon.science/publications/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3
                        2. MongoDB (used in Replication Protocols)


            11. Others
                1. ClickHouse is used for monitoring metrics in 3FS
                   https://github.com/deepseek-ai/3FS/tree/main/deploy
                2. 3FS local node is using XFS
                   https://github.com/deepseek-ai/3FS/blob/main/deploy/README.md
                    1. "Format the attached 16 SSDs as XFS and mount at ..."

            12. Write throughput of 3FS
                1. https://arxiv.org/html/2408.14158v2
                    1. "Parameters and optimization states are divided into chunks and written to 3FS using the 3FS batch write API, which is significantly faster than normal writes, achieving over 10 GiB/s per node"
                2. https://github.com/deepseek-ai/3FS?tab=readme-ov-file#2-graysort
                    1. Sorting 110.5 TiB of data across 8,192 partitions completed in 30 minutes and 14 seconds


    2. 幻方：萤火高速读写文件系统（3FS）概述 - Andy730
       https://mp.weixin.qq.com/s/qKRioV45IbOq91XDsUEIcg
        1. Key designs
            1. Direct IO：绕过内核的Page Cache
            2. AIO（异步IO）
            3. RDMA read
            4. 客户端数据对齐：3FS客户端负责处理Direct IO对齐的要求（buffer地址、读取size和offset需要对齐），避免用户进行额外的内存拷贝操作，简化了接口的使用。
            5. FFRecord格式
                1. 合并小文件：将多个小文件合并成一个或多个大文件，减少了训练时打开大量小文件的开销，对存储后端更加友好。
                2. 支持随机批量读取：存储每条样本的文件偏移量和校验和，方便进行随机批量读取。
                3. 数据校验：包含数据校验，保证读取的数据完整可靠。
            6. 3FS通过Infiniband技术构建高速网络，并采用虚拟通道机制隔离不同类型的流量
            7. 用户态文件系统（FUSE）支持：3FS vNext提供了特殊的用户态文件系统FUSE，在用户空间提供3FS vNext的POSIX接口
                1. Interesting point. If it's a distributed filesystem where server is at the remote end, the FUSE becomes an advantage at the client side.
            7. “萤火二号”超算的3FS存储系统配置（2024年）： 
                l. 存储节点：180个，每节点包含：
                    1. 16个PCIe 4.0 NVMe SSD。
                    2. 2个Mellanox CX6 200Gbps InfiniBand HCA。
                    3. 1个AMD EPYC 7742 CPU（64核）。
                    4. 512GB DDR4-3200MHz内存。
                2. 总带宽：9TB/s出站带宽。
                3. 总存储容量：2880个NVMe SSD提供超过20PiB的镜像冗余存储空间。
                4 实际性能：实现了总读取吞吐量8TB/s。
            8. 3FS-KV - 构建于3FS之上的共享存储分布式数据处理系统
                1. 支持三种模型：键值存储（key-value）、消息队列和对象存储。
                    1. Good point. 深度学习需要三种接口融合
                    2. 键值存储（key-value）模型
                        1. 这种存储方式具有高效的查找性能，对于简单的数据存储和快速检索场景非常适用
                        2. 例如，在一些实时数据处理应用中，需要快速根据某个唯一标识（键）获取相应的数据（值），键值存储模型可以在极短的时间内完成操作。
                    3. 对象存储模型
                        1. 主要用于存储非结构化的数据，如图片、视频、文档等。
                        2. 每个对象都有唯一的标识符，并且可以附带元数据信息，如对象的大小、创建时间、修改时间等
                        3. 3FS-KV的对象存储模型还支持数据的版本控制
                    4. 消息队列模型
                        1. 异步通信提供了可靠的支持 ... 确保消息在分布式系统中的有序传递
                        2. 例如在一个复杂的深度学习训练系统中，不同的模块（如数据预处理模块、模型训练模块、结果评估模块等）之间需要进行数据和指令的传递。通过消息队列，这些模块可以异步地发送和接收消息
                2. 3FS-KV支持DeepSeek的磁盘KV上下文缓存技术（KV Context Caching on Disk），这可以将LLM服务的成本降低一个数量级
                    1. Good improvement. Worth drilling down
            9. 3FS vNext
                1. 提供了更好的元数据（meta）性能和更高的小块读取吞吐量，能够显著提升训练效率
                    1. Good point. This is highlighting a key direction for AI storage
                2. 提升系统可用性，减少了服务端和客户端升级时对用户的影响
                    1. Interesting point. "升级时对用户的影响" considering a portion of nodes are down to upgrade
                3. 灵活的配置： 功能和参数配置更加灵活，可以根据实际需求进行定制化配置， 满足不同深度学习场景的需求
                4. 3FS vNext支持用户空间下的文件系统（FUSE）
                    1. 相比内核模块插拔，3FS vNext支持用户空间下的文件系统（FUSE）
                    2. 丰富的调试工具：用户空间下调试工具丰富，出现问题不会导致系统崩溃，提高了系统的稳定性
                    3. 性能限制：由于FUSE的性能受到一定限制，因此这种使用方式一般只推荐用于日常的文件管理，不适合作为深度学习训练过程中的主要数据访问方式
        2. Highlights: 
          1. AI 场景需要基于 NVMe SSD 的对象存储、消息队列、KV 存储。
          2. 更好的元数据性能和更高的小块读取吞吐量，能够显著提升训练效率。
          3. 磁盘 KV 上下文缓存技术（KV Context Caching on Disk），将 LLM 服务的成本降低一个数量级。
          4. Good article for insights
        3. Notes
            1. 注：本文基于论文《Fire-Flyer AI-HPC: A Cost-Effective Software-Hardware Co-Design for Deep Learning》和幻方官方文档（2019-2022）整理，内容未必体现其最新状态，并且存在不同时期的信息和数据，稍显混乱，仅作参考。

    3. DeepSeek 3FS：端到端无缓存的存储新范式 - XSKY
       https://zhuanlan.zhihu.com/p/27355706799
       https://mp.weixin.qq.com/s/bSvs3BPePYVgObZZMC32Nw
        1. Good article for insights
            1. 从 Delta、Azure 借鉴链式复制的可靠性模型，从 WekaFS、Vast Data 全闪存直写的简洁路径，从 Alibaba、FAST 论文的 FUSE 提速的思路
            2. 过去几年业内对无缓存、用户态 IO、RDMA、分布式事务元数据等理念多有探讨，3FS 将它们付诸实践并取得成功案例
            3. 3FS 项目开篇就讲到了整个项目是面向 AI 相关场景设计，完全面向大文件优化，放弃对于传统文件系统小文件问题的掣肘。
            4. 端到端无缓存
        2. Highlights
            1. 3FS 项目开篇就讲到了整个项目是面向 AI 相关场景设计，完全面向大文件优化，放弃对于传统文件系统小文件问题的掣肘
                1. 3FS 的元数据性能扩展性受限于 FoundationDB 的能力，在高并发场景下可能面临瓶颈
                2. 3FS 的小文件答案：FFRecord，特别适用于深度学习（DL）训练样本
                    1. 随机访问：支持直接访问特定记录，无需扫描整个文件。
                    2. 异步 I/O（AIO）：基于 Linux AIO，提供非阻塞数据读取，提升数据加载效率。
                    3. 高效批量读取：能够快速读取数据批次，适合深度学习中批量处理的需求。
                    4. 压缩支持：可选的记录级压缩，节省存储空间，同时保持高效访问。
            2. 端到端无缓存
                1. VastData 在 5.1 版本开始，在其两层的 DASE 架构上，进一步加强了 QLC SSD 直写，减少 SCM 层带来的写入带宽瓶颈
                FUSE 继承一系列优化
                2. HammerSpace 在去年年底，创新性提出了 Tier-0 存储概念，即在计算节点侧直接利用本地 NVMe SSD 作为读写，纳入到文件系统的全局里，并且不改变应用的使用方式。其核心是在利用 Linux Kernel 6.12 的 NFS Bypass 特性，绕开整个 VFS 栈进行读写，让 NVMe SSD 在单文件并发上发挥接近块存储的性能。
                3. https://mp.weixin.qq.com/s/yiy4hfXQE6k4FaQNBR7ilg
                    1. 读取文件时，程序通常会经过一个中间人——内核，它提供文件缓存等功能。（文件缓存也会导致不可预测的内存使用量/延迟峰值） DeepSeek 的文件系统完全消除了它，客户端直接访问驱动器（直接 IO）
                4. 幻方力量 | 高速文件系统 3FS    [2019]
                   https://www.high-flyer.cn/blog/3fs/
                    1. 3FS 是一个比较特殊的文件系统，因为它几乎只用在AI训练时计算节点中的模型批量读取样本数据这个场景上
                    2. 这是一个大规模的随机读取任务，而且读上来的数据不会在短时间内再次被用到，因此我们无法使用“读取缓存”这一最重要的工具来优化文件读取，即使是超前读取也是毫无用武之地
                    3. 因此，3FS的实现也和其他文件系统有着比较大的区别

            3. FUSE 继承一系列优化
                1. 3FS 客户端采用了主流 FUSE 框架，对于 FUSE 每个文件系统从业者都是爱恨交加，一方面 FUSE 给 Linux Kernel FS 带来了用户态实现的可能性，另一方面糟糕的性能实现以及坎坷的演进使得每个 FUSE 使用者都无力吐槽。
                2. 但也不得不说，FUSE 在过去 3 年里，随着文件系统在 AI 场景的使用，大量的 FUSE 改进项目和内核优化都在进行中，其中包括以下：
                    1. XFUSE: An Infrastructure for Running Filesystem Services in User Space 
                        1. 在 2021 的 ATC，阿里云就提出了 FUSE 存在的若干性能问题，对 FUSE 进行了多方面优化，包括路径直通、批处理请求、多线程处理等。论文结果表明，XFUSE 能将用户态文件系统请求处理延迟压缩到 4 微秒级，吞吐达到 8GB/s，同时，XFUSE 保持了对 FUSE API 的兼容，方便现有 FUSE 文件系统迁移。
                    2. ByteFUSE：ByteFUSE分布式文件系统的演进与落地
                        1. 字节跳动文件系统团队在 2021 年开始也在逐步优化 FUSE 性能，在《ByteFUSE分布式文件系统的演进与落地》可以看到其创新性的提出了利用 VirtQueue 来优化队列性能，并且可以统一虚拟机和容器场景。VirtQueue 作为 QEMU/KVM 成熟的高性能队列框架，非常适合去解决 FUSE 的队列问题。
                    2. RFUSE: Modernizing Userspace Filesystem Framework through Scalable Kernel-Userspace Communication 
                        1. 这篇 FAST 24 的论文进一步对 FUSE 通道进行性能优化，它的核心思路是使用每核独立的环形缓冲区在内核和用户态之间传递消息，从而避免传统 FUSE 中集中队列和锁带来的瓶颈。每个 CPU 核心都有自己的请求通道，用户态文件系统可以多线程并行处理不同核心的请求，无需在内核模块中进行序列化。更重要的是，RFUSE 设计为与现有 FUSE 文件系统兼容，不需要修改现有用户态代码。
                    3. Fuse over io-uring
                        1. 由 DDN Bernd Schubert 在 2023 年提出，在 2024 年经过近 10 个版本的迭代，由于代码涉及 CPU 调度和跨模块的影响，被迫砍掉了若干性能优化点，在 2025 年合并进了主线。Fuse over io-uring
                        2. 特性原理是用 io_uring 取代传统 FUSE 的 /dev/fuse 通道，这样用户态文件系统可以直接从 io_uring 队列读取请求和提交响应，避免了每次请求的系统调用和上下文切换。
                3. 3FS 是选择完全绕开 FUSE 的数据读写通道，如同 DeepSeek 过去开源的算子优化类似，通过借鉴 io uring 的零拷贝和共享内存设计，直接在应用侧跟文件客户端建立了共享内存通道，实现从应用侧内存数据到 RDMA 传输的零拷贝，更是彻底避免了 VFS 系统调用的 Context Switch 和内存拷贝
    
    4. Deepseek 3FS（ Fire-Flyer File System）设计笔记 - GrissomF
       https://mp.weixin.qq.com/s/B_5xdV2gl9APcJyBuBuUgQ
        1. A Chinese translation (well-formatted) to https://github.com/deepseek-ai/3FS/blob/main/docs/design_notes.md

    5. Paper: DeepSeek 3FS: Fire-Flyer AI-HPC: A Cost-Effective Software-Hardware Co-Design for Deep Learning    [2024, 1 refs, DeepSeek-AI]
       https://arxiv.org/html/2408.14158v1
       https://arxiv.org/abs/2408.14158
        1. Very good paper. Key contribution: HFReduce, HaiScale, 3FS, Network optimization, HAI scheduling platform. Key outcome, similar perf with DGX-A100 while reducing 50% costs.
            1. Note, many contents are stale compare to the release highlights.
        2. Highlights
            1. Achievements
                1. 3FS + PCIe A100 GPU, achieve similar perf with DGX-A100 while reducing 50% costs and 40% energy
                2. HFReduce on CPU/PCIe, outperforms NCCL
            2. Architecture
                1. 10K PCIe A100 GPUs
                    1. "Our cluster, consisting of 10,000 A100 GPUs, includes approximately 1,250 GPU compute nodes and nearly 200 storage servers"
                        1. Note, the compute and storage nodes are disaggregated
                2. Cost effectiveness
                    1. Comparing to DGX
                        1. See table "Table II: A100 PCIe Compared to DGX-A100.", "Table III:Relative Cost Comparison"
                    2. Cloud Service Providers
                        1. Despite their convenience and easy accessibility, the costs can accumulate significantly over time. For long-term projects spanning around two years, these costs could amount to purchasing an entire dedicated cluster.
                    3. Table I:Our Arch and DGX-A100 Server Hardware Details
                        1. Our 512GB DDR4 vs DGX 2048GB DDR4
                        2. Our 1* InfiniBand 200Gbps NIC vs DGX 9* InfiniteBand 200Gbps NIC
                        3. GPU and NVLink are the same
                        4. Additional points
                            1. 8 NVIDIA A100 PCIe GPUs and 1 Mellanox CX6 200Gbps IB NIC: directly connect to the CPU, without using a PCIe switch
                            2. IB NIC occupies a separate PCIe root complex, thus avoiding performance interference with the GPU.
                            3. Reserved the possibility of NVLink Bridge addition in design: As expected, when the LLM era arrived, we indeed added an NVLink Bridge between PCIe cards.
                3. Figure 3:Size of Model Parameter and Accelerator Memory
                    1. Transfomer size: 410x / 2yrs
                       AI HW Memory: 2x / 2yrs
                4. Challenges and Solutions in Models Training
                    0. Good summaries in this chapter
                    1. Overall
                        1. Model FLOPs Utilization (MFU)
                        2. Extensive communicate due to dividing models among GPUs
                        3. Operation optimization, data pre-processing, and GPU memory consumption significantly influence MFU
                    2. Parallel strategies
                        1. Data Parallelism (DP):
                            1. Models and optimizer states are replicated across devices. Note ZeRO optimizes it by sharding (see FSDP)
                        2. Pipeline Parallelism (PP)
                            1. Each device holds a portion of the model layers with each training batch divided into micro-batches for pipeline execution. 
                            2. Reduce pipeline bubbles. GPipe, PipeDream 1F1B, ZBPP
                        3. Tensor Parallelism (TP)
                            1. Placing a model layer on multiple GPUs that perform computations in parallel. Megatron-LM
                        4. Expert Parallelism (EP)
                            1. MoE Models’ different expert models are distributed on different GPUs during MoE training
                            2. The gate model selects tokens for allocation during input, with corresponding tokens sent to experts model via all2all communication.
                    3. Fully Sharded Data Parallel (FSDP)
                        1. based on the ZeRO Stage 3 algorithm
                        2. FSDP partitions the model’s parameters, optimizer states, and gradients, distributing them across different GPUs, with each GPU retaining only 1/n of the total
                        3. Forward pass: allgather
                        3. Backward pass: allgather, reduce-scatter
                           https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html
                5. Challenges in AI Infrastructure
                    1. This paper. How to be cost effective and high performance.
            3. Key technologies
                1. Network Co-Design
                    1. Two-Layer Fat-Tree Network
                        1. Fat-tree is a specific type of CLOS network architecture, it is being compared with Dragonfly topology
                            1. As in this paper, they need high bisection bandwidth which is featured by Fat-tree.
                            2. Also, InifiniBand comes with Fat-tree.
                    2. zoned
                        1. two-zone network configuration
                        2. Each zone consists of an 800-port Fat-Tree connected to approximately 600 GPU compute nodes
                        3. Each storage server equipped with two IB NICs, respectively connected to different zones, hence all GPU compute nodes could share a set of storage services
                        4. two zones are interconnected with a limited number of links
                        5. Our scheduler ensures that in this topology, only one pair of nodes communicates across zones
                            1. Interesting .. HFReduce with a double binary tree (DBT) algorithm
                            2. Double binary tree algorithm
                                1. Two-Tree Algorithms for Full Bandwidth Broadcast, Reduction and Scan    [2009, 132 refs]
                                   https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=daa542b84703c0a9faf321619acb5ad6c679ebeb
                                2. 万卡集群通信优化算法双二叉树 - ZOMI酱
                                   https://www.youtube.com/watch?v=wsXsuldYOKo
                                    1. NCCL 2.4 double binary tree. It is an effective way to do Reduce. The prior work is Ring Reduce.
                                        1. Ring Reduction has a problem that the allreduce latency increases linearly with node count
                                    2. Nice illustration.
                    3. various tunning to avoid congestion
                        1. VI-A Ensuring Minimal Congestion in Our Computation-Storage Integrated Network
                            1. Traffic classes
                                1. HFReduce communication, NCCL communication, 3FS storage traffic, and other traffic
                            2. Traffic QoS
                                1. by InfiniBand’s Service Level (SL) technology
                                2. map SL to IB physical queues Virtual Lanes
                                3. configured their proportions
                            3. Topology Adjustment and Route Optimization
                                1. we observed that enabling adaptive routing would lead to more severe congestion spread in the network. Therefore, we opted for a static routing strategy
                                    1. Related to Google B4 and Google Orion SDN. They use central controller to resolve and pass routing map to downstream switches.
                            4. NCCL Optimization
                                1. We adjusted the NCCL topology to route through the IB NIC and GPUs within the same NUMA node
                                2. using PCIe Relaxed Ordering, we further reduced congestion and increased bandwidth
                            5. Network Tuning in 3FS
                                1. 3FS implements a request-to-send control mechanism to mitigate the congestion
                                    1. After receiving a read request from a client, the service reads data from SSD and asks the client’s permission to transfer the data. The client limits the number of concurrent senders
                    4. Future look
                        1. LLM MoE, All-to-all performance is crucial. The next-gen nodes feature a 1:1 GPU to NIC ratio, comparable to DGX-H100/B100 systems, as illustrated in Figure 12.
                        2. Implementing a multi-plane network to reduce costs while maintaining performance, Figure 12.
                        3. Exploring the use of RoCE switches instead of IB switches, which can significantly lower network expenses
                            1. With a 128-port 400 Gbps RoCE switch, a 4-Plane Two-Layer Fat-Trees network can support up to 32,768 GPUs
                2. HFReduce - Custom AllReduce DBT implementation in compare with NCCL
                    1. Computation-communication overlap via asynchronous allreduce on the CPU
                    2. Advantages of HFReduce over NCCL (Ring Reduction)
                        1. Reduced PCIe Bandwidth Consumption
                        2. No GPU Kernel Overhead
                            1. HFReduce utilizes the GPU’s Copy Engine (CE) for PCIe asynchronous transfers. 
                            2. In contrast, NCCL’s allreduce operation requires GPU kernel execution
                        3. HFReduce Overcomes Limitations of EPYC Rome CPU
                            1. Our tests indicate that the maximum bandwidth between the GPU and IB NIC on Rome CPUs is approximately 9 GiB/s, making the observed 4GB/s all-reduce bandwidth for NCCL understandable. HFReduce circumvents this limitation by utilizing the CPU for reduction and transferring data through IB and host memory.
                            2. See more in "IV-D3 Bottlenecks of HFReduce"
                3. HaiScale - DDP that utilizes HFReduce as its communication backend
                    1. optimizes parallelism methods for our PCIe architecture
                        1. Data Parallelism (DP)
                        2. Pipeline Parallelism (PP)
                        3. Tensor Parallelism (TP) 
                        4. Experts Parallelism (EP) 
                        5. Fully Sharded Data Parallel (FSDP)
                        6. Zero Redundancy Optimizer (ZeRO)
                    2. custom optimizations
                        1. HFReduce does not depend on GPU Streaming Multiprocessors (SM) for reduction computation, enabling completely asynchronous allreduce without impacting performance
                            1. PyTorch’s DDP which employs NCCL as its backend
                        2. Both HaiScale’s FSDP and PyTorch’s FSDP are implementations based on the ZeRO Stage-3 algorithm
                            1. HaiScale’s FSDP offers better engineering implementation, optimizing memory management to reduce fragmentation specific to model adjustments
                            2. And we overlap allgather and reduce-scatter communication with forward and backward computation
                4. 3FS distributed filesystem
                    1. Big data AI tasks, reduces congestion in storage and computation integrated network topology
                    2. One sided RDMA operation like RDMA WRITE, RDMA READ.
                5. HAI Platform
                    1. task scheduling, fault handling, and disaster recovery, enhancing utilization and reducing costs
                    2. Tasks can be python or bash code. delivered in containers.
                    3. Tasks support checkpointing and recover from checkpoints
            4. Stability and Robustness
                1. These are crucial topics in HPC.
                    1. Robust mechanisms to handle hardware failures, minimizing downtime and impact on operations
                2. Disaster recovery through our checkpoint manager
                3. A validator utility for detecting hardware failures
                4. An overview of real hardware failure data from our cluster over the past year
                5. Numbers
                    1. Parameters and optimization states - write in 10GB/s per node
                    2. Checkpoint performed per 5 minutes, checkpoint write takes a few seconds
                6. Hardware Validator
                    1. Checking hardware frequency, link speed, and link status.
                    2. Testing CPU stress and memory bandwidth.
                    3. GPU Memory test: This involves checking each byte of GPU memory to ensure no data corruption has occurred.
                    4. Running GEMM with full GPU memory occupancy, which can simultaneously check whether there are any operational logic faults in the GPU chip.
                    5. Intra-node allreduce test: checking NVLink bandwidth through upper-level applications.
                    6. Storage bandwidth stress test to make sure storage is functioning normally.
                9. Hardware Failures Characterization - Good experience
                    1. Indeed, in our practice, we have encountered computational errors and GPU memory errors not detected by Error Correction Code (ECC), which led to models’ gradnorm spikes, loss explosions and even non-convergence. How to tackle these hardware failures, promptly identify and categorize them, is a key issue to improve the online rate and overall utilization of cluster nodes.
                    2. It is evident that the number of GPU ECC faults considerably surpasses those from the CPU
                    3. In our PCIe-based system, Xid74, also known as NVLink errors, account for a significant proportion, comprising 42.57% of the total
                        1. Table VI:Raw Data of GPU Xid Errors in Our Cluster Over the Past Year, as Mentioned in Section
                        2. Related to Network Flash Cut - 网络闪断
            5. Discussion and future works
                1. PCIe congestion control
                2. maintenance cost
                3. stability compared with other architectures
                4. propose the next generation of PCIe architecture
                    1. aimed at Mixture-of-Experts Large Language Models training and primarily utilizes multi-NICs and a Multi-Plane network
        3. My questions
            1. Is the 2 zone networking architecture used to support Prefill Decode Separation?
            

    6. Fat-tree network vs Dragonfly topology
        1. Demystifying DCN Topologies: Clos/Fat Trees
           https://packetpushers.net/blog/demystifying-dcn-topologies-clos-fat-trees-part1/
           https://packetpushers.net/blog/demystifying-dcn-topologies-clos-fat-trees-part2/
            1. Part 2 tells what is Fat-Tree. It's a tree networking that more bandwidth in links closer to root.
                1. 3FS uses a 2-layer Fat-Tree, that is to say they are using the simplest version of fat-tree.
                2. From Figure 5 in 3FS paper, they also have 2 zones, and each zone is a 2-layer Fat-tree.

        2. A Cost and Scalability Comparison of the Dragonfly vs. the Fat Tree
           https://www.youtube.com/watch?v=e5prPoqxx8o

        3. Dragonfly vs. Fat-tree -- the Future of Cluster Topologies
           https://www.youtube.com/watch?v=cLSn7Q0QXG4
            1. "The fat-tree is the dominating topology for InfiniBand". 3FS is using InfiniBand. It explains why they use Fat-tree.
            2. Fat-tree: "Full bisection bandwidth for arbitrary permutations"
            3. Both Fat-tree and Dragonfly are in HPC community. 
            4. Dragonfly
                1. Intra-group: can be any topology
                2. Inter-group: each group has at least one link directly to each other group
                3. Focus on reducing the number of long links and network diameter
                4. Requires non-minimal global adaptive routing and advanced congestion look ahead for efficient operation.
            5. Fat-tree
                1. Most common topology for InfiniBand
                2. Can be routed deadlock free without additional resources such as virtual lanes
                3. Fault-tolerant through its path diversity
                4. Full bisection bandwidth for arbitrary permutations
                5. Scalable, also with respect to cost
                6. Performance suffers slightly due to static routing

    7. DeepSeek 3FS 架构分析和思考（上篇）- ByteDance
       https://mp.weixin.qq.com/s/X60PsEPeFsb-ZPKATMrWrA
        1. Good illustration, chart, tables. Much more than the original 3FS papers and design notes.
        n. related materials
            1. DeepSeek 3FS 架构分析和思考（下篇）
               https://mp.weixin.qq.com/s/tlQ208NDss2VV4pCA4WW6Q
                1. 

    8. DeepSeek SmallPond
       https://github.com/deepseek-ai/smallpond
        1. Understanding smallpond and 3FS: A Clear Guide
           https://www.definite.app/blog/smallpond
            1. features
                1. Distributed Analytics: Allows DuckDB to handle larger-than-memory datasets by partitioning data and running
                2. Manual Partitioning: Data is manually partitioned by users, and smallpond distributes these partitions across nodes for parallel processing.
                3. Over 1PB (Petabyte-Scale): smallpond and 3FS were explicitly designed to handle massive datasets
            2. How Smallpond Works
                1. Lazy DAG Execution
                2. From Logical to Execution Plan
                3. Ray Core and Distribution
        
        2. 陈巍：DeepSeek 开源Day（5）3FS&smallpond深入分析
           https://zhuanlan.zhihu.com/p/26958884790

    9. Understanding MoE
        1. DeepSeek MoE把价格打下来核心原因？看MoE架构剖析！ - ZOMI酱
           https://www.youtube.com/watch?v=667J9Nh8zG8
            1. Good illustration. Finally demystified MoE.
        2. MOE终于迎来可视化解读！傻瓜都能看懂MoE核心原理！ - ZOMI酱
           https://b23.tv/YXZlxnb
            1. The more detailed version of the above
        3. DeepSeek-R1深度解读，如何做到 RL+LLM 训练的？
           https://youtu.be/B9El-kGj_vY?si=VR23tAzU_t6RtUNk
            1. DeepSeek-R1-Zero 训练流程 
               https://youtu.be/B9El-kGj_vY?si=_6Dc4XQZSGpgyDui&t=1050
                1. GRPO
                2. Distillation to Qwen/LLAMA
        4. DeepSeek开源一周大串烧，对行业和大模型带来哪些变化和冲击？ - ZOMI酱
           https://www.bilibili.com/video/BV11W9hYKEGj

    10. DeepSeek-V3/R1推理效率分析 - zartbot
        https://mp.weixin.qq.com/s/WXrgxV3LgYYvRLPTVzLkjw
        1. Very good. Worth thinking. It includes code and detailed model dimension parameters.
        n. Related materials
            1. DeepSeek V3/R1 推理效率分析（2）: DeepSeek 满血版逆向工程分析
               https://zhuanlan.zhihu.com/p/29841050824

    11. 3Blue1Brown
        1. Attention in transformers, step-by-step | DL6
           https://www.youtube.com/watch?v=eMlx5fFNoYc
        2. How might LLMs store facts | DL7
           https://www.youtube.com/watch?v=9-Jl0dxWQs8
            1. It has the parameter count calculation for GPT Transformer, for each of Attention and FF layers
            2. Good.

    12. DeepSeek 3FS解读与源码分析（2）：网络通信模块分析 - Zartbot
        https://mp.weixin.qq.com/s/RARAWVF8OpgnKJeXKmbNMQ
            1. "链式写速度受磁盘写盘速度限制，如果能在本地读写 NVMe 的时候将 libaio 替换成用户态存储栈 SPDK，能进一步大幅度提升 I/O 性能，甚至可以考虑引入 NVMeoF，将数据直接通过 RDMA 写到远端 NVMe 上。"
                1. "NVMeoF 的设计更适合于 1-to-N 的星形写，而对类似 HDFS 的 chain-replicate 或者 CRAQ 这种链式复制的架构不是很友好。"
                2. "而虽然 SPDK NVMe 层采用 polling mode driver 模式能带来高性能，但是对容器部署不友好带来的隐形成本，以及 RTC 模式与 folly 协程的协同带来的性能抵消可能是另一个考虑的因素。"
            2. Highlights
                1. 设计细节层面追求极致性能，包括 I/O 链路全栈引入 folly 协程将 I/O bounded 操作异步化，数据处理使用 C++20 新特性等
                2. 设计上考虑了通用性，例如 Client 和 Server 独立成型，不对某种应用场景有强依赖和强定制化，不依附于特定的 RPC 框架，不依赖元数据中心等
                3. 在工程实现上充分挖掘了多网卡并行的能力，并且在流控实现，自研消息编解码 Serde 服务等细节上有工业级打磨

    13. DeepSeek 3FS 源码解读——协程&RDMA篇 - howard
        https://zhuanlan.zhihu.com/p/27331176252
        1. "3FS 并没有选择自行编写协程库，甚至也没有使用 await_suspend 的方式来封装 IO（在代码库里是搜索不到这个关键词的），而是使用了 Facebook 开源的 folly 库，调用了其中实现的 Executor 等执行调度器驱动。"
    
    14. DeepSeek 3FS 源码解读——磁盘 IO 篇 - howard
        https://zhuanlan.zhihu.com/p/27497578911
        1. "和网络 IO 充分协程化不太一样，磁盘 IO 基本是由线程池来完成同步 IO 操作，而且读 Chunk 实际数据使用了 AIO 来异步读取，但是写数据则调用了同步 IO。这也就意味着 3FS 没有采用目前高性能存储系统使用的 Run To Completion 模型。"
        2. "用 Rust 编写的 Chunk 存储引擎"

    15. MHA vs MQA vs GQA vs MLA - Zain ul Abideen
        https://medium.com/@zaiinn440/mha-vs-mqa-vs-gqa-vs-mla-c6cf8285bbec
        1. Code implementation of MHA, MQA, and GQA based on nn.Module
        2. Code for MLA (not quite clear)
            1. "Instead of caching both the Key and Value matrices, MLA jointly compresses them in a low-rank vector which allows caching fewer items since the compression dimension is much less compared to the output projection matrix dimension in MHA."

    16. deepseek技术解读(1)-彻底理解MLA（Multi-Head Latent Attention） - 姜富春
        https://zhuanlan.zhihu.com/p/16730036197
        0. good article
        1. 一个token就要 2.62MB 的 KV 缓存 
        2. 减小KV cache的方法
            1. 共享KV：多个Head共享使用1组KV，将原来每个Head一个KV，变成1组Head一个KV，来压缩KV的存储。代表方法：GQA，MQA等
            2. 窗口KV：针对长序列控制一个计算KV的窗口，KV cache只保存窗口内的结果（窗口长度远小于序列长度），超出窗口的KV会被丢弃，通过这种方法能减少KV的存储，当然也会损失一定的长文推理效果。代表方法：Longformer等
            3. 
量化压缩：基于量化的方法，通过更低的Bit位来保存KV，将单KV结果进一步压缩，代表方法：INT8等
            4. 计算优化：通过优化计算过程，减少访存换入换出的次数，让更多计算在片上存储SRAM进行，以提升推理性能，代表方法：flashAttention等
        3. MLA原理解读
            1. 低秩变换矩阵
            2. 矩阵吸收计算 - 为什么q（或k）分成两个矩阵拼接，其中一个矩阵计算RoPE
                1. Good part

        n. Related
            1. 缓存与效果的极限拉扯：从MHA、MQA、GQA到MLA - 苏剑林
               https://spaces.ac.cn/archives/10091

    17. DeepSeek comments from WeiChat circles
        转：刚才花2小时看完了DeepSeek V3 的 Technical Report，下面说下我的感想：
        1. 首先，文章贡献主要来自系统（Training Infra），而非模型本身。模型本身依然基于传统的Transformer：
            1）他们世界首创在大规模LLM训练中系统性部署fp8（8位浮点）量化技术，这大大降低训练对显卡内存的需求，也加快了训练过程；
            2）为了正确使用fp8的矩阵乘法，他们优化并改进了CUDA Kernal的调用方式，甚至给NVDA提出了诸多Tensor Core方面的设计建议
            3）他们开发了自己的训练框架DualPipe，实现了16/64通道的流水线和专家（MOE）并行，极大改善了并行训练中的通信和计算冲突问题，解决了调度瓶颈。
            最终，DeepSeek实现了在2048个H800上的集群训练。
        2. 其次，文章中大部分改进是渐进式的，而非革命性的：
            1）对Context 扩展的技术实际上来自2023年文章YaRN，而且最终DeepSeek V3只实现了N=1的MTP，也即比传统的GPT多预测一个词；
            2）MOE所引入的Aux-Loss-Free Load Balancing技术，其实仅仅是在传统Expert的分配算法面前加入了一个bias term b_{i}；
            3）DeepSeek MOE上的另一个革新是加入了“共享Expert”，并保证训练时对于每个Token，这些Expert最多分布在4个node上，以减少通信瓶颈。
            4）其独创的Multihead Latent Attention 本质上是将QKV通过线性变换降维到一个Latent Space存入Cache，提高存储速度；这有利于推理任务加速。
            5）利用自己在量化交易中的经验，创造性地将某些移动平均值（如Adam参数状态）存在CPU中，减少并行开销，等等
            当然，能够将如此多新的细节整合在一起，并获得一个几乎没有任何Loss Spike的平滑的训练框架，这不得不说是一个奇迹。
        3. 最后，DeepSeek 在RL和蒸馏方面确实得到了极其宝贵的经验。Deep Seek证明了：
            1）推理能力可以通过RL获得，
            2）推理能力可有效的被蒸馏到更小的模型上去。
            虽然他们也同时观察到，蒸馏可能让小模型的输出变得更长，语言效率降低。此外，如果RL的Reward Model过于简单，这可能会让模型推理仅限于数学和代码任务
        4. 总的来说，确实是一个非常好的Paper，证明了在极限的精度和优化条件下，训练一个600B大模型成本能走到多低。
        但不至于颠覆硅谷，是一个非常好的阶段性进展
        恭喜全世界的AI研究者们！

    18. AI时代的高端文件存储系统：IBM、DDN、Weka 和 VAST - 企业存储技术
        https://mp.weixin.qq.com/s/z2rYfthS_7F-jsBoz-lb0Q
        n. Related materials
            1. AI的存储需求：训练和Checkpoint
               https://mp.weixin.qq.com/s/zYNubjEpRrUyw0TC9-HwDg
                1. "如上面图表，Checkpoint的大小（GB数）为模型参数（Billion数）的14倍"

    19. 陈巍：DeepSeek 开源Day（6）推理系统概览解读
        https://zhuanlan.zhihu.com/p/27264662709
        n. Related materials
            1. 陈巍：DeepSeek 开源Day（1）-FlashMLA 深入分析（收录于：DeepSeek技术详解系列）
               https://zhuanlan.zhihu.com/p/26031898869
            2. 陈巍：DeepSeek V3/R1的架构与训练技术2万字长文分析（上）（收录于：DeepSeek技术详解系列）
               https://zhuanlan.zhihu.com/p/21208287743
                1. "增加共享专家+无辅助损耗负载平衡"
            3. 陈巍：DeepSeek V3/R1的架构与训练技术2万字长文分析（下）（收录于：DeepSeek技术详解系列）
               https://zhuanlan.zhihu.com/p/21755758234
                1. Useful summary for the training process and main technologies in DeepSeek

            4. Rejection sampling - Lars Hernández Nielsen
               https://www.linkedin.com/pulse/rejection-sampling-lars-hern%C3%A1ndez-nielsen/

    20. 大模型推理加速：看图学KV Cache - 看图学
        https://zhuanlan.zhihu.com/p/662498827
        1. Useful. The chart illustration helps to understand how KV cache works
            1. K_i and V_i are per token calculated, same token, same result. They are reused per each attention(N+1) calculation
            2. Q_i cannot be reused, attention(N+1) needs Q_n+1
            3. Same token, same K,V cache entry. No context related, and it's per token.

    21. How to define a storage infrastructure for AI and analytical workloads - Google Cloud Tech
        https://www.youtube.com/watch?v=A4daQj9tnWk
        1. Key storage requirements for AI workload
            1. Performance & Scale
            2. Data management
            3. Ecosystem
            4. Data Governance
        2. Vision
            1. Storage data once, access anywhere, with any performance, any interface and any scale
                1. Very good. This is really great vision.

    22. Storage Architecture Optimized for AI Workloads - SNIA SuperMicro
        https://www.youtube.com/watch?v=FvVytHgXzd8

    23. StorageScale - 3FS / DeepSeek drilldown
        1. DeepSeek 3FS解读与源码分析（5）：客户端解读 - StorageScale
           https://mp.weixin.qq.com/s/sPkqOdVA3qBAUiMQltveoQ
            1. Useful. Very detailed. With thoughts
        2. DeepSeek 3FS解读与源码分析（4）：Meta Service解读
           https://mp.weixin.qq.com/s/urzArREaN7wj8UZ9Tx3FKA
        3. DeepSeek 3FS解读与源码分析（3）：Storage模块解读
           https://mp.weixin.qq.com/s/K8Wn0cop742sxfSdWB5wPg
        4. Deepseek 3FS解读与源码分析（2）：网络通信模块分析
           https://mp.weixin.qq.com/s/qzeUL4tqXOBctOOllFqL7A
        5. DeepSeek 3FS解读与源码分析（1）：高效训练之道
           https://mp.weixin.qq.com/s/JbC4YiEj1u1BrBejmiytsA


2. LoRA: Low-Rank Adaptation of Large Language Models
   https://arxiv.org/abs/2106.09685
   https://yiyibooks.cn/arxiv/2106.09685v2/index.html
    1. Applied to pre-trained model (W0 is fixed), typically for Fine-tuning. Also widely used in training of LLM attention.
    2. Highlights
        1. Q = (Wq + ΔWq) · X = Wq · X + Bq · Aq · X, Wq is fixed. Bq and Aq can choose a low middle dimension, so that parameter count is much lower than Wq.
        2. Key benefits: Reduced 2/3 memory usage in training. No overhead to inference.
        3. What is the Optimal Rank r for LoRA?
            1. See Table 6: Validation accuracy
    n. Related
        1. DeepSeek MLA is using LoRA, see kv_lora_rank in MLA chart
           https://mp.weixin.qq.com/s/WXrgxV3LgYYvRLPTVzLkjw
           https://blog.csdn.net/u013701860/article/details/146063967

        2. In attention formula, why Q and K are not merged into just a product?
           https://www.reddit.com/r/MachineLearning/comments/184m63q/din_transformer_models_why_is_there_a_query_and/
            1. To clarify the question, you can see "WeightMatrix_Q * WeightMatrix_K^T" is a whole in calculation

                Q = InputMatrix * WeightMatrix_Q  // Each row of InputMatrix is the embedding vector of an input token
                K = InputMatrix * WeightMatrix_K
                V = InputMatrix * WeightMatrix_V
                Attention = softmax((InputMatrix * WeightMatrix_Q * WeightMatrix_K^T * InputMatrix^T) / sqrt(d_k)) * InputMatrix * WeightMatrix_V

            2. The answer is LoRA. WeightMatrix_Q and WeightMatrix_K are 768 * 2304 sized. But "WeightMatrix_Q * WeightMatrix_K^T" is 
               https://poloclub.github.io/transformer-explainer/

3. When and Why Are Deep Networks Better than Shallow Ones?    [2017, 280 refs]
   https://ojs.aaai.org/index.php/AAAI/article/view/10913/10772
    1. DeepSeek model consists of 60+ transformer blocks. The question is why stack many transformer blocks rather than using one big transformer block?
    2. Highlights
        1. Both hierarchical and shallow networks support universal approximation. 
           Deep networks can approximate compositional functions, but shallow networks need exponentially more parameters.
        2. See Figure 2.

    n. Related materials
        1. Why are deeper networks better than wider networks?
           https://www.reddit.com/r/MachineLearning/comments/h0g83p/d_why_are_deeper_networks_better_than_wider/
           1. "The intuitive idea is that deep networks can exploit compositions. Every time a shallow network needs to compute something, then it essentially has to do it from scratch. A deep network can re-use the computations that have already been done by the intermediate layers. This makes them much more efficient."

        2. Topology of deep neural networks    [2020, 185 refs]
           https://arxiv.org/abs/2004.06093
           https://yiyibooks.cn/arxiv/2004.06093v1/index.html
            1. Looks unrelated. The paper is studying data geometric topology.

        3. ChatGPT: Why use more transformer blocks rather than one big layer
           https://chatgpt.com/share/683534eb-368c-800f-aa7b-d85b9b1aa781
            1. Depth Enables Hierarchical Representation
                1. Stacking many layers allows the model to learn progressively higher-level abstractions, 
                    1. Just like CNN Edges → textures → objects
                    2. progressively higher-level abstractions:
                        1. Lower layers learn local and syntactic patterns (e.g., word order)
                        2. Mid layers learn grammar, phrases, dependencies
                        3. Higher layers learn semantics, reasoning, and abstract context
            2. One Huge Block = No Composition = Poor Generalization
            3. Gradient Flow and Optimization Stability
            4. Parallelism and Memory Reuse
            5. Empirical Results
                1. deep, narrow layers consistently outperform shallow, wide ones at the same parameter count

4. On the Optimal Memorization Power of ReLU Neural Networks    [2021, 32 refs]
   https://yiyibooks.cn/arxiv/2110.03187v1/index.html
   https://arxiv.org/abs/2110.03187
    1. The question is MLP/FFN layer in LLM is said to be able to memorize world knowledge (3Blue1Brown). How does that happen?
    2. Highlights
        1. Key contribution: Use O(sqrt(N)) parameters to memorize N samples.
            1. My questions
                1. Sqrt is much less efficient than what I thought. I should be at least log level in LLM?
        2. In this work we show that deep networks have significantly more memorization power

5. How LLM can take embedding as input in RAG
    1. LLMs are Also Effective Embedding Models: An In-depth Overview    [2024, 4 refs]
       https://arxiv.org/html/2412.12591v1
    2. Passing Vector Embeddings as Input to LLMs?
       https://www.reddit.com/r/LocalLLaMA/comments/1gqztfb/passing_vector_embeddings_as_input_to_llms/
    3. GhatGPT: Embedding LLAM RAG
       https://chatgpt.com/share/683af47e-5b90-800f-944f-14955ac7d3b0
        1. Embedding isn't directly fed into LLM, it is used to search for relevant docs. Then the doc text and query text are input into LLM
        2. The embedding used in search and in LLM are different. They cannot be used interchangably.
        3. LLM uses per token embedding vector, sentence is a stack of vectors. Doc retrieval converts the whole sentence into a fixed length vector.
            1. Doc retrieval internally uses per token embedding, but they aggregate them into one vector
            2. "document embedding" vs "token embedding"
    4. Information Retrieval with Document Embeddings
       https://la.mathworks.com/help/textanalytics/ug/information-retrieval-with-document-embeddings.html
        1. Keyword search can be thought as retrieval upon bagOfWords embedding
    5. How Vector Embeddings work in LLM | LLM Embedding model | LLM Embedding explained
       https://www.youtube.com/watch?v=mtf8wbkj03M
        1. Mean Pooling
            1. Just take the average or sum of all token embedding to generate the document embedding
        2. Use PCA
            1. Reduce token vector dimensions
    6. LLM Embeddings Explained: A Visual and Intuitive Guide
       https://huggingface.co/spaces/hesamation/primer-llm-embedding?section=word2vec

6. DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning    [2025, 1397 refs]
   https://arxiv.org/abs/2501.12948
   https://yiyibooks.cn/arxiv/2501.12948v1/index.html
    1. Good founding paper of DeepSeek. Key contribution: GRPO no SFT. CoT <think> tags. Distill 14B models. DeepSeek-V3 trains DeepSeek-R1.
    2. Highlights
        1. DeepSeek-R1 achieves performance comparable to OpenAI-o1-1217 on reasoning tasks
        2. Model training process
            1. DeepSeek-V3-Base -> GRPO -> DeepSeek-V3-Zero
                1. No supervised data, no SFT
            2. DeepSeek-V3-Base -> Cold start Fine Tuning -> GRPO -> SFT rejection sampling, DeepSeek-V3 supervised -> full scenario learning -> DeepSeek-R1
            3. DeepSeek-R1 -> distill on Qwen2.5-32B -> 14B model
                1. significantly outperform peers
                2. DeepSeek-R1-Distill-Qwen-1.5B outperforms GPT-4o and Claude-3.5-Sonnet on math benchmarks with 28.9% on AIME and 83.9% on MATH
        3. Reword modeling
            1. Format reward: ‘<think>’ and ‘</think>’ tags
            2. Do not use reward on outcome or process
        4. Self-evolution process
            1. Figure 3, as training goes on, it generates longer and longer output (<thinking> tags)
                1. aha moment: DeepSeek-R1-Zero learned to allocate more thinking time to reevaluating its initial approach. this is not taught.
            2. DeepSeek-R1-Zero spontaneously arise behaviors like reflection and exploration
                1. reflection: where the model revisits and reevaluates its previous steps
                2. and the exploration of alternative approaches
        5. Reinforcement Learning for all Scenarios
            1. This is the secondary RL training stage
            2. using a combination of reward signals and diverse prompt distributions
        6. Future works
            1. Currently, the capabilities of DeepSeek-R1 fall short of DeepSeek-V3 in tasks such as function calling, multi-turn, complex role-playing, and JSON output
            2. When evaluating DeepSeek-R1, we observe that it is sensitive to prompts. Few-shot prompting consistently degrades its performance. Therefore, we recommend users directly describe the problem and specify the output format using a zero-shot setting for optimal results.
            3. Software Engineering Tasks. large-scale RL has not been applied extensively in software engineering tasks. DeepSeek-R1 has not demonstrated a huge improvement over DeepSeek-V3 on software engineering benchmarks
                1. rejection sampling on software engineering data
                2. asynchronous evaluations
        n. My questions
            1. Why not mentioning MoE? But it is in DeepSeek-V3 paper

7. DeepSeek-V3 Technical Report    [2024, 745 refs]
   https://arxiv.org/abs/2412.19437
   https://yiyibooks.cn/arxiv/2412.19437v2/index.html
    1. Very good paper. Founding paper of DeepSeek. Generously revealed every detail in the industry pioneering MoE LLM. Outperforms all opensource models and matches with leading closed-source models such as GPT-4o, Claude-Sonnet-3.5.

    2. Highlights
        1. Training framework
            1. FP8 mixed precision training
                1. compared with BF16, the relative loss error of FP8-training model remains consistently below 0.25%
                2. we adopt the strategy of promotion to CUDA Cores for higher precision, Figure 7
                3. quantization tile, group
            2. 16-way Pipeline Parallelism (PP), 64-way Expert Parallelism (EP) spanning 8 nodes, and ZeRO-1 Data Parallelism (DP)
            3. DualPipe algorithm for efficient pipeline
                1. overlap the computation and communication within a pair of individual forward and backward chunks
                2. DualPipe requires keeping two copies of the model parameters
            4. Customized cross-node all-to-all communication kernels to reduce SMs dedicated to communication
            5. Extremely Memory Saving 
                1. Recomputation of RMSNorm and MLA Up-Projection
                2. Exponential Moving Average in CPU memory
                3. Shared Embedding and Output Head for Multi-Token Prediction
            6. Suggestions on Hardware Design - good part
                1. hardware that offloads these communication tasks from the valuable computation unit SM
                2. Higher FP8 GEMM Accumulation Precision in Tensor Cores
                3. Support for Tile- and Block-Wise Quantization
                4. Support for Online Quantization
                    1. reducing off-chip memory access by roughly 50%
                5. Support for Transposed GEMM Operations

        2. Model architecture
            1. Multi-head Latent Attention (MLA)
                1. Compress the KV input (W^DKV * h_t) into much smaller dimensions (c_t^KV)
                2. Down-projection first, into KV cache, then up-projection into true KV
                    1. My questions
                        1. This implies MLA has overhead in computation, then it saves KV cache
                3. To sum up, MLA is simply installing a down-projection/up-projection step in front of MHA.
                4. My questions
                    1. Why RoPE is a separated vector concated into K, Q? Unlike a standard transformer that position encoding directly applies to K, Q.
                        1. deepseek技术解读(1)-彻底理解MLA（Multi-Head Latent Attention）
                           https://zhuanlan.zhihu.com/p/16730036197
                            1. DeepSeek-V2 paper has an explanation
                               https://arxiv.org/html/2405.04434v5
                                1. Section "2.1.3 Decoupled Rotary Position Embedding"
                                    1. RoPE is incompatible with low-rank KV compression ... W^UK cannot be absorbed into W^UQ during inference.
            2. DeepSeekMoE architecture
                1. Introducing shared experts, compared to GShard
                    1. the shared expert is regarded as a heavy-load one that will always be selected
                2. auxiliary-loss-free load balancing
                    1. Introduce bias term into affinity scores. Note bias term is used in routing only.
                    2. Complementary Sequence-Wise Auxiliary Loss
                    3. DeepSeek-V2 paper has more details
                    4. token-to-expert affinity is calculated by softmax(u * e), u is expert output, e is expert centroid. 
                        1. Centroid Vector (of an expert) 可通过聚合历史上路由到该专家的所有输入 token 计算得到
                           https://zhuanlan.zhihu.com/p/31729594502
            3. Multi-token prediction
                1. This is newly introduced in DeepSeek-V3 (not in V2). 
                2. Figure 3 shows everything. 
                    1. Sequentially predict tokens
                    2. Preserve causal chain
                3. Training objective: cross entropy loss of predicting the correct token
                4. Note that during inference, we directly discard the MTP module
                5. See section 4.2, the MTP prediction depth is set to 1.
        
        5. Training process
            1. DeepSeek-V3 requires only 2.788M H800 GPU hours for its full training.
            2. The training process is stable. Not experienced any irrecoverable loss spikes or perform any rollbacks.
            3. the training corpus for DeepSeek-V3 consists of 14.8T high-quality and diverse tokens
            4. Adjusting training Hyper-Parameters
                1. AdamW optimizer
                2. dialing down learning rate
                3. dialing up batch size (from 3072 to 15360)
            5. Long Context Extension
                1. DeepSeek-V3 is capable of handling inputs up to 128K
                2. The methodology is the same with DeepSeek-V2
                   https://arxiv.org/html/2405.04434v5
                    1. Yarn: Efficient context window extension of large language models    [2023, 365 refs]
                       https://arxiv.org/abs/2309.00071
                       https://yiyibooks.cn/arxiv/2309.00071v2/index.html
                        1. 
            6. Post-Training
                1. Supervised Fine-Tuning

    n. Related
        1. How KV cache works exactly
           https://medium.com/@joaolages/kv-caching-explained-276520203249
        
        2. ChatGPT: Understanding attention formula - scaling factor, softmax
           https://chatgpt.com/share/683af47e-5b90-800f-944f-14955ac7d3b0

        3. Deploy the DeepSeek 3FS cluster quickly by using M3FS
           https://blog.open3fs.com/2025/03/28/deploy-3fs-with-m3fs.html

8. Insights into DeepSeek-V3: Scaling Challenges and Reflections on Hardware for AI Architectures    [2025, 0 refs]
   https://arxiv.org/pdf/2505.09343
   https://yiyibooks.cn/arxiv/2505.09343v1/index.html
    1. Very good paper. The value suggestions to hardware design are future innovation directions for AI chips. 
       They need DeepSeek's large scale experience to draw and are illustrated in quite details.
       This paper also recapped key technologies in DeepSeek and also gave accurate numbers of DeepSeek performance and cost.
       So, overall DeepSeek is truly contributing to the industry
        1. Revealed the full details about how to train a large-scale industry pioneering LLM.
        2. Innovated and opensourced full stack key technologies in training LLM, and the filesystem. 
           The LLM industry has full load of what-to-do in the next a few years.
        3. The DeepSeek model itself is industry pioneering in cost-effectiveness.
        4. Now this paper revealed in detail what can be the future AI hardware directions.
           The AI hardware industry has full load of what-to-do in the next a few years.
    2. Highlights
        1. Recap the key technologies in DeepSeek-V3
            1. DeepSeek-V3, trained on 2,048 NVIDIA H800 GPUs
            2. Multi-head latent attention - MLA
            3. Mixture of experts - MoE
            4. Multi-Token Prediction - MTP
        2. Key design principles in DeepSeek-V3
            1. Memory Efficiency - HBM needs grows by 10x, by supply grows by 1.5x YoY
                1. By adopting MLA, DeepSeek-V3 achieves a significant reduction in KV cache size, requiring only 70 KB per token, substantially less than LLaMA-3.1 405B’s 516 KB and Qwen-2.5 72B’s 327 KB (Table 1)
            2. Cost-Effectiveness of MoE Models
                1. DeepSeek-V3 expands to 671B parameters, while keeping the activation per token at just 37B
                2. the total computational cost for DeepSeek-V3 is approximately 250 GFLOPS per token, whereas the 72B dense model requires 394 GFLOPS and the 405B dense model requires 2448 GFLOPS (Table 2)
            3. Increasing Inference Speed
                1. Test-Time Scaling
                    1. dynamically adjusting computational resources during inference
            4. Technique Validation Methodology
                1. a hierarchical and resource-efficient validation pipeline
                    1. first validated extensively on small-scale models, followed by minimal large-scale tuning, and finally integrated in a single, comprehensive training run
        3. Low-Precision Driven Design
            1. suggestions for future hardware designs
                1. Increased Accumulation Precision
                2. Native Support for Fine-Grained Quantization
            2. LogFMT: Communication Compression
                1. Logarithmic Floating-Point Formats (LogFMT-nBit)
                    1. interesting, this is new in this paper
                2. Hardware design suggestion
                    1. native support for compression and decompression units tailored to FP8 or custom precision formats
        4. Interconnection Driven Design
            1. Avoid TP, Enhance PP with DualPipe, Enhance EP with DeepEP 
            2. TopK expert routing, at most 4 nodes per token.
        5. Scale-Up and Scale-Out Convergence
            1. future hardware should integrate intra-node (scale-up) and inter-node (scale-out) communication into a unified framework
            2. Suggested to hardware
                1. Unified Network Adapter for scale-up and scale-out networks
                2. Dedicated Communication Co-Processor to offload GPU SM
                3. Flexible Forwarding, Broadcast and Reduce Mechanisms
                4. Hardware Synchronization Primitives to handle memory consistency issues or out-of-order packet arrivals at the hardware level
            3. Bandwidth Contention and Latency
                1. current hardware lacks the flexibility to dynamically allocate bandwidth between different types of traffic on NVLink and PCIe
                2. Suggestion
                    1. Dynamic NVLink/PCIe Traffic Prioritization
                    2. Integrating NICs directly into the I/O die and connecting them to the compute die in the same package
                    3. CPUs and GPUs should be interconnected using NVLink or similar dedicated high-bandwidth fabrics, rather than relying solely on PCIe
        6. Large Scale Network Driven Design
            1. Figure 3 Multi-Plane Fat-Tree (MPFT) scale-out network
                1. Figure 4, ideally the MPFT should: Each NIC is equipped with multiple physical ports, each connected to a distinct network plane
            2. Recommendations for RoCE Improvements
                1. Ethernet vendors develop RoCE switches specifically optimized for RDMA workloads by removing unnecessary Ethernet features
                2. ECMP in RoCE LLM training has bad performance. Adaptive Routing (AR) significantly enhance net perf, matching static manual configured routing. (Figure 8)
                3. Current RoCE switches support only a limited number of priority queues, not enough for EP/DP all-to-all
                4. InfiniBand GPUDirect Async (IBGDA): Built in DeepEP and yields substantial performance gains 
        7. Discussions
            1. Robustness Challenges
                1. Suggestions for Advanced Error Detection and Correction
            2. CPU Bottlenecks and Interconnects
                1. CPUs and GPUs often becomes a bandwidth bottleneck
                2. Suggest direct CPU–GPU interconnects, such as NVLinkd and IB
                3. Demand for high DRAM bandwidth - 1TB/s
            3. Toward Intelligent Networks for AI
                1. Incorporating silicon photonics enables scalable higher bandwidth scalability and enhanced energy efficiency
                2. Lossless Network
                3. Adaptive Routing
                4. Efficient Fault-Tolerant Protocols
                5. Dynamic Resource Management
            4. Discussion on Memory-Semantic Communication and Ordering Issue
                1. Inter-node communication using load/store memory semantics is efficient and programmer-friendly, but current implementations are hampered by memory ordering challenges
                2. Interesting topic. Section 6.4
            5. In-Network Computation and Compression
                1. A hardware-level protocol enabling automatic packet replication and forwarding to multiple destinations could drastically reduce communication overhead and improve efficiency
                    1. My questions
                        1. Transactional memory?
                2. Incorporating LogFMT natively within network hardware could further optimize communication by increasing entropy density and reducing bandwidth usage
            6. Memory-Centric Innovations
                1. Memory bottleneck: The exponential growth in model sizes has outpaced advancements in high-bandwidth memory (HBM) technology
                2. Suggestions
                    1. DRAM-Stacked Accelerators: Leveraging advanced 3D stacking technologies, DRAM dies can be vertically integrated atop a logic die, thereby enabling exceptionally high memory bandwidth, ultra-low latency, and a practical memory capacity (though stack-limited)
                        1. Interesting 
                    2. System-on-Wafer (SoW)

    n. Related materials
        1. DeepSeek-V3再发论文，梁文锋署名，低成本训练大模型的秘密揭开了 - 机器之心
           https://mp.weixin.qq.com/s/nTZH03aIIG1tQa7uiRc__A

        2. 谈谈DeepSeek对AI架构硬件的思考 - Zartbot
           https://mp.weixin.qq.com/s/6U6L_vACHU2LYRvkMWvyXw
            1. ScaleUp和ScaleOut融合
            2. NetDAM
```