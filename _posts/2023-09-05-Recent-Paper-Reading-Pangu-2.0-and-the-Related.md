---
layout: post
title: "Recent Paper Reading: Pangu 2.0 Filesystem and the Related"
tagline : "Recent Paper Reading: Pangu 2.0 Filesystem and the Related"
description: "Recent Paper Reading: Pangu 2.0 Filesystem and the Related"
category: "storage"
tags: [storage, paper, filesystem]
---
{% include JB/setup %}


Pangu 2.0 filesystem.

```
2. Pangu 2.0: More Than Capacity: Performance-oriented Evolution of Pangu in Alibaba    [2023, 1 refs, FAST23, Alibaba]
   https://www.usenix.org/conference/fast23/presentation/li-qiang-deployed
    1. Good paper. Comprehensive industry implementation for a cloud storage backend.
       Key point: Userspace filesystem USSOS driven by SSD and RDMA, leveraging DPDK and SPDK. 
       Results: Figure 10, 6.10x throughput.
    2. highlights
        1. Key points
            1. Userspace filesystem USSOS driven by SSD and RDMA, leveraging DPDK and SPDK.
                1. also need to design userspace memory management, CPU scheduling, and hardware failure handling
                2. Handling correctable machine check exceptions (MCE) in the USSOS to improve availability
                    1. "Initially, USSOS (§3.2) can monitor such hardware failures, but it cannot perceive how the kernel migrates the physical memory for exception isolation. As such, errors would happen when USSOS tries to access the already migrated physical memory based on its outdated virtual-physical memory address mapping"
                    2. "To this end, we add a handler to the MCE monitor daemon in USSOS. Once the number of found correctable MCEs exceeds a threshold, the user-space process related to them will pause and let the handler notify the kernel to migrate the memory. After the migration, the process resumes and updates its mapping table before accessing memory pages."
            2. Hardware offloading (e.g. compression) improved the service provision capability by ~50%
                1. At ~3GB/s throughput, Hardware-based FPGA compression can save about 10 physical cores (Intel Xeon 2.5Ghz)
                2. CRC is offloaded to RDMA capable NICs, CRC per block.
                   CPU then aggregates these CRC and performs a lightweighted check.
        2. Optimization with SSD and RDMA
            1. Add small capacity DRAM module to increase memory bandwidth with NIC
            2. Leverage Intel's DDIO to implement RDCA (Remote Direct Cache Access).
                1. The motivation observation is data is extremely short-lived in memory.
                2. RDCA consumes 12MB LLC (20% of total per server), "平均内存带宽消耗减少了89%，网络吞吐量提高了9%"
                3. My questions
                    1. Why ~89% memory bandwidth reduced, but only ~9% network throughput improvement?
            3. Hybrid RPC: Optimize CPU bottleneck with FlatBuffer for data path and ProtoBuf on control path.
            4. Synchronizing CPU hyper-threading (HT) with specialized `CPU wait` instruction.
                1. HT problems: Interference when two tasks running simultaneously, e.g. a network idle-polling thread vs a compression thread
                2. Solution
                    1. "Pangu introduces the CPU wait instruction. It consists of monitor and mwait. Pangu needs less than 5 ms to call them."
                    2. "the network idle-polling thread will mwait at the monitored memory address and does not wake up until the memory address is written by other threads."
                3. My questions
                    1. 5ms call time, is it very bad?
            5. Improve HDD write efficiency by the differences between internal and external tracks of disks.
                1. My questions: The paper didn't add any details?
            6. More
                1. run-to-completion thread model, to reduce thread context-switch.
                2. huge-page shared memory zero-copy from network stack to processing to SPDK
                3. As such, Pangu upgrades to lossy RDMA, in which pause frames are disabled, to avoid these problems and improve performance.
        3. Self-contained chunk layout to reduce IO latency of file writes
            1. See Figure 3. Section 3.1.3
            2. Append with one file write (no extra metadata write).
            3. footer per block carries CRC, and chunk metadata
        4. My questions
            1. What's the status of "NVMe-Over-Fabric"?
            2. It seems, Pangu 1.0 was to match HDFS, then Pangu 2.0 eventually moved to the paradigm of Azure Storage or GFS (Colossus). 
            3. Pangu files can be variable size, they can be large or small. If all files are large enough, can we say the overhead of Kernel filesystem is low enough, so USSFS is no longer necessary?
                1. Probably not, the power of SPDK is still there, and need to avoid Kernel's
                    1) System call context switch
                    2) Copying user space data to kernel space
                    3) Kernel interruption handling
                2. The way to avoid frequent Kernel interrupt is "Polling and event-driven switching (NAPI)". Would this already be supported by Windows Completion Port that you can poll the status?
            4. Is userspace filesystem or Filesystem bypassing really necessary?
                1. The assumption is, if file size is large enough, filesystem overhead is low
                2. We can avoid userspace to kernel space data copy via O_DIRECT
                   See https://chat.openai.com/share/8bb2c074-8d9a-45a9-a6d0-718da5f2f2be
                3. Polling instead of the interruption can be implemented with Windows completion port.
                4. But, what about networking stack / DPDK? Or similarly the SPDK for storage stack? Or SMR drives?
                   Maybe it's still right that Kernel and common Filesystems are too large and too complex.
                   We only need a simplified specialized storage engine that customizes every layer.
            5. Is FPGA or DPU in the network path really necessary?
                1. In network processing, ASIC is definitely faster than FPGA. Then, buy a better vendor NIC should solve the problem
                2. Compression/encryption/CRC should have dedicated acceleration card. And Smart NIC is there anyway.
                3. Vector Processing has GPU is there. No need for another DPU.
                4. FPGA inter-connect is not needed if we don't need FPGA. Instead, DRAM+CPU inter-connect can be done with RDMA, storage inter-connect can be done with NVMe-oF.
                5. Maybe a lightweighted low power CPU is still desirable? ARM, FPGA core?

    n. related materials
        1. Pangu 2.0: 如何打造一个高性能的分布式存储系统 - Pangu paper on FAST23 - KDF5000
           https://zhuanlan.zhihu.com/p/611583679?utm_id=0
            0. useful article. already covered most key points in paper
            1. "Pangu存储系统是阿里云存储服务的底层存储系统，大家熟知的OSS/NAS/EBS等服务都是基于Pangu系统开发"
            2. "100us级I/O延迟". "Pangu的进化包括两个阶段：
                1. 第一阶段，Pangu利用新的SSD硬件和RDMA网络技术重新设计了一套用户空间存储系统，降低了其I/O延迟，同时提高了吞吐和IOPS；
                2. 第二阶段，Pangu从面向容量的存储服务转变为面向性能的存储服务。为了适应这种业务模型的变化，Pangu将服务器升级为拥有更高容量的SSD和RDMA带宽的存储服务器，网络从25 Gbps升级到100 Gbps。同时还引入了一系列关键设计，包括减少网络流量放大、远程直接缓存访问和CPU计算卸载，以确保Pangu充分利用硬件升级带来的性能提升"
            3. Pangu 1.0 (2009 - 2015)
                1. "Pangu 1.0存储引擎使用的是Linux自带的ext4内核文件系统，网络使用TCP网络，可以认为当时对标的主要是HDFS，从业务视角来看当时面临的主要问题是如何存储大规模的数据，对性能的要求并不是很高。Pangu 1.0时期为了适应业务需求，也提供了多种文件类型，比如Append-only的LogFile，支持随机读写的Random Access File和类似文件系统的临时文件需求的TempFile，"
            4. Pangu 2.0 (2015 ~ now)
                1. "Pangu团队总结了1..0版本中的一些洞察和思考：
                    1. 1.0提供了各种文件类型，尤其是支持随机读写的文件类型，随机读写相比顺序读写并不能发挥SSD硬件的性能，提供极致的吞吐和IOPS
                    2. 1.0单机存储使用的是内核文件系统，IO链路上存在大量的数据复制和中断，这些都影响了IO性能，相比SSD和RDMA消耗的延迟，已经成为了大头
                    数据中心架构已经由服务器为中心演变为了资源为中心，如何适配这种数据中心架构的演进从而提供低IO延迟的服务带来了新的挑战"
                2. 2.0 第一阶段：用户态文件系统
                    1. "重新设计了文件系统，提供了一个用户态的文件系统(USSOS），提供了append-only的语义，并重新设计了一种自包含的Chunk Layout避免了文件系统一次io产生两次IO的情况(一次数据io和一次meta io)。"
                    2. "2.0在线程模型上使用run-to-completion的模型，避免了额外的线程切换开销，实现了用户态存储栈和用户态网络栈的高效协同，同时也提供了一个用户态的CPU/MEM资源调度机制。"
                    3. "该阶段实施效果也是相当显著的，2018年双十一期间，Pangu 2.0为阿里巴巴数据库服务提供了280us的优异延迟性能；对于写敏感的EBS/Drive服务，其PCT999延迟低于1ms；对于读敏感的如在线搜索业务，其PCT999延迟低于11ms"
                3. 2.0 第二阶段：升级基础设施适应面向性能的业务模型和打破CPU/Mem的瓶颈
                    1. "阿里巴巴开始自研存储服务器，提供了单机97TB SSD和100Gpbs网卡的高性能服务器"
                    2. "硬件升级了，软件栈同样也要进行适配，从而打破CPU/MEM的瓶颈，软件栈主要做了如下优化"
                        1. "通过技术手段减少网络写放大，并且提供动态调整流量优先级的策略"
                        2. "提供远端缓存访问技术(RDCA)"
                        3. "降低序列化反序列化开销，减少CPU消耗"
                        4. "引入了CPU wait指令同步超线程"
                    3. "通过使用自研的存储服务器，先比之前网络从2x25Gbps升级到2x100Gbps，并且解决了硬件升级造成软件层面存在的CPU/MEM瓶颈，Pangu 2.0的吞吐提升了6.1倍"
            4. Pangu架构
                1. "Pangu Service：这一部分严格说不算是Pangu系统的范畴，指的Pangu系统的用户，有OSS/NAS/EBS等面向普通用户的产品服务。"
                    1. "这里值得一提的是，除了传统的存储服务（OSS/EBS/NAS等），Pangu Service提供一个一个面向云原生的文件系统服务Fisc[1]，这也是现在云原生大潮下比较重要的一个服务，也发表在今年的FAST上。"
                    2. "Pangu Core: 该部分是本文关注的Pangu系统部分，包含了Client、Masters和ChunkServers。对外提供了Append-Only的持久化文件系统。其中Client是提供给Pangu Service的SDK，负责接收调用方的文件读写请求，然后和Maters和Chunkservers交互完成数据的读写，Client是一个重SDK，其在整个系统中扮演着重要的角色，诸如多副本的写入，数据的一致性等都由其负责"
                    3. "Pangu Mornitor: 整个系统的监控系统，对于任何系统都是必备组件，提供了实时的监控和基于AI的根因分析服务"
                2. "Pangu Core里的Masters和ChunkServer，也是Pangu系统里最重要的两个组件。"
                    1. "Masters主要负责管理所有元数据，使用Raft的协议维护元数据一致性。为了更好的水平扩展性和可扩展性（例如数百亿个文件），Pangu主节点将元数据服务分解为两个独立的服务：命名空间服务和Stream元数据服务。"
                    2. "命名空间服务提供有关文件的信息，例如目录树和命名空间"
                    3. "Stream是Pangu中文件的代称由一系列的Chunk组成，一个Stream可以认为是可以无限append写入的大文件，Stream元数据服务提供文件到块的映射(即块的位置)，这个和微软的Azure Storage系统是相似的(传闻Pangu早期的操刀者也是由微软过来的同学完成)"
                    4. "ChunkServer则负责将数据的单机存储，其组织形式也是由一个一个的Chunk组成，并且使用用户态文件系统(USSFS)对Chunk进行管理。USSFS为不同硬件提供高性能的追加式存储引擎。"
                        1. "在Pangu 2.0的第一阶段中，每个文件都存储在具有三个副本的块服务器中，后来垃圾回收工作程序（GCWorker）执行垃圾回收并使用纠删码（EC）存储文件。"
                        2. "在Pangu 2.0的第二阶段中，逐渐将3倍复制替换为EC在关键业务（例如EBS）中，以减少Pangu中的流量放大"
            5. Pangu 2.0
                1. 设计目标：
                    1. "低延迟：2.0旨在利用高性能的的SSD和RDMA硬件在存算分离架构下提供100us级别的IO延迟，并且能够提供ms级别的SLA保证，即便是存在网络抖动和服务器故障"
                    2. "高吞吐：充分发挥存储服务器的吞吐能力，提供极限吞吐"
                    3. "一致的高性能：为所有使用Pangu的服务，如在线搜索、数据分析、EBS、OSS和数据库，都能够提供一致的高性能服务"
                2. 第一阶段：拥抱SSD和RDMA
                    1. Append-only文件系统
                        1. "所以在2.0的设计了简化了该设计只提供一个统一的Append-only的FlatLogFile类型"
                        2. "传统的文件系统，如Ext4，存储文件是以Block为单元，一个文件的数据和元数据分两次IO写入到存储介质，这样不仅增加了写入的延迟也缩短了SSD的使用寿命，"
                            1. "因此Pangu 2.0设计了图3所示的一种自包含的Chunk Layout，每个Chunk自己保存了数据和元数据，这样在写入的时候只需要一次IO即可，
                            2. 这种设计还有一个好处是在故障的时候，可以自行恢复，因为元数据包含了ChunkID、Length和CRC等。
                            3. 同时，ChunkServer在内存还保留一份所有Chunks的元数据，并且周期性的进行Checkpoint到持久化存储，当故障发生的时候，Chunkserver可以对比Checkpoint中的元数据和Chunk Layout里保存的元数据，通过比对CRC从而恢复到一个正确的状态。"
                        3. 
                        4. "通过使用自包含的Chunk Layout可以减少数据操作的次数，也去除传统文件系统Page Cache和Journal等开销"
                    2. Heavyweight client
                        1. "Pangu Client是一个很重的SDK，负责了从Maters获取元数据信息，然后从ChunkServer读写数据。从Masters获取到元数据后，就得到了Chunkserver的位置信息，
                        2. 然后还要负责复制协议，比如将用户数据通过EC的方式写入到多个ChunkServer上，除此之外还提供了重试的机制以及backup read的能力。
                        3. Client还提供了后台探测机制，周期性的探测Chunkserver的状态，这样在写入和读取的时候就可以有选择地规避有故障的ChunkServer。"
                3. Metadata Operation Optimization
                    1. "两层元数据服务使用不同的分片策略（比如目录树通过子目录划分，然后stream则通过哈希划分）划分为不同的分片，
                        每个分片由raft协议保证一致性的元数据服务管理，这样保证了元数据服务的扩展性。"
                    2. 两层元数据服务使用不同的分片策略（比如目录树通过子目录划分，然后stream则通过哈希划分）划分为不同的分片，每个分片由raft协议保证一致性的元数据服务管理，这样保证了元数据服务的扩展性。
                        1. 元数据并行处理。除此之外，Pangu 2.0还是用了 一种可预测的目录ID的数据结构使其能够支持高效的并行处理路径解析
                        2. 长度可变的Chunk大小
                        3. 在Client端缓存Chunk的信息
                        4. Chunk请求批处理
                        5. Chunk信息预取
                        6. Data Piggybacking减少一次RTT: 合并Create Chunk和Write Chunk请求
                4. ChunkServer 用户态文件系统(USSOS)
                    1. "Pangu 2.0使用了高性能的SSD和RDMA网络，1.0使用的内核文件系统成为了短板，因为会带来大量的中断以及内核用户态的数据复制，因此利用kernel-bypass技术设计实现了一套用户态的文件系统，在线程模型上也使用了Run-to-Completion模型。"
                    2. "Chunkserver的用户态文件系统基于RDMA的网络栈(DPDK)和SPDK的存储栈。在两种协议的基础上进行了如下的优化：
                        1. 使用Run-to-Completion线程模型，减少上下文的切换和线程间的通信以及同步
                        2. 通过用户态的共享内存减少内存拷贝。一个线程请求一块大内存后，这个共享内存会在网络栈和存储栈共享。比如用RDMA协议从网络收到数据后会放到一块共享大页内存中，然后发送内存的地址和大小后，数据就可以通过SPDK直接写入到存储媒介中。通过这种方式可以减少数据的拷贝，同时一些后台的任务比如GC一样可以共享这块内存实现数据的零拷贝"
                    3. "Pangu 2.0引入了一个用户态的调度机制去进一步提高性能
                        1. 防止一个任务阻塞后续的任务。 
                            1. 每个chunkserver只有固定数量的工作线程，
                            2. 新的请求根据请求中文件的哈希值分配到工作线程。
                            3. 对于一些长任务，引入心跳机制监控任务的执行时间并设置警报
                        2. 优先级调度保证QoS。
                        3. Polling和evnt-drivent切换(NAPI)。
                            1. 具体讲就是应用默认是event-driven模式，当收到一个通知后就会切换到polling模式，polling一段时间没有新的IO请求后会再次切换到event模式"
                    4. Append-Only USSFS
                        1. "这样可以充分利用SSD的顺序写优势"
                        2. "通过使用自包含的Chunk Layout可以减少数据操作的次数，也去除传统文件系统Page Cache和Journal等开销"
                        3. "使用polling模式替代ext4使用的中断模式，最大化ssd的性能"
                5. 高性能SLA保证
                    1. "Chasing机制。 这个机制可以减少系统抖动对写延迟的影响", similar with "Non-stop write"
                        1. "在写入数据副本的时候设置MinCopy和MaxCopy，通常2xMinCopy > MaxCopy（不如MaxCopy为3，MinCopy为2），假设其中一个副本发生了异常，那么写入只需要写入MinCopy就返回用户成功。
                        2. 假设两个正常副本写入成功时的时间为T，Client已经返回用户写入成功，但是依然会将该Chunk保存在内存中，等待时间t(ms级别），如果异常的副本在T+t前返回成功，那么Client就会从内存中将该chunk释放。
                        3. 如果没有，但是没有写入成功的数据大小小于k，那么client就会重试写入，如果没有写入成功的数据大于k，那么Client就会将失败的副本Seal掉(禁止后续写入)，然后通知masters修复该副本。
                        4. 通过他们分析发现小心的选择t和k可以额在减少写入尾延迟的同时不带来任何数据丢失的风险。"
                    2. Backup Read
                        1. "一个chunk有多个副本，当下发读请求到一个副本时，等待一段时间t，如果请求还没有成功，那么会马上发送n个请求到其他副本，哪个请求先回来就返回给用户"
                    3. Backlisting
                        1. "如果一个chunkserver可以提供服务，但其延迟超过一定阈值，它将被添加到非确定性黑名单中"
                6. 第二阶段：适应面向性能的业务模型
                    1. "Pangu 2.0阶段转向了性能的优化，为了适应业务对性能的需求，自研了名为泰山的存储服务器，每台泰山服务器配备了2x24C的Skylake CPU，12x8TB的商用SSD，128GB的DDR内存以及2x 100Gbps网卡。并且通过SSD制造的优化(缓存和channel等)，单台泰山服务器的SSD吞吐能够达到20GB/s。"
                    2. "升级了硬件后，CPU、Memory和网络成为了新的瓶颈，因此2.0阶段主要是进行软件栈的优化打破这些瓶颈。"
                        1. 网络瓶颈
                            1. "硬件上： 采用高性能的NIC/RNIC、光模块（QSFP28 DAC、QSFP28 AOC、QSFP28等），单模/多模光纤和高性能交换机
                            2. 网络软件栈： 早期为了大规模部署RDMA，采用了关闭NIC端口或在RDMA网络上有太多暂停帧时（例如几秒钟）临时切换到TCP等各种机制，但是这些机制不能处理基于暂停帧的流量控制的其他问题（例如死锁和头部阻塞，因此又升级到有损RDMA，禁用暂停帧，以避免这些问题并提高性能"
                            3. 流量优化，减少网络流量的放大
                                1. 使用EC替代3副本：用EC(4,2)替代第(b)步的三副本
                                2. 压缩FlatLogFile：在GC和Client写入数据的时候使用LZ4对数据进行压缩
                                3. 动态为前端和后台流量分配网络带宽
                        2. 内存瓶颈
                            1. Problem: "内存瓶颈发生在网络进程和应用进程对内存带宽的竞争，如网卡不能够申请到足够的内存带宽，就会对PCIe产生严重的反压，最终导致网卡buffer积压网络包，最终丢弃溢出的包，进而触发拥塞控制机制导致系统整体性能恶化，如吞吐降低30%，延迟增加5~10%，IOPS也会降低10%。"
                            2. "增加小容量的DRAM扩充内存带宽。 因为内存容量不是瓶颈，因此可以增加小容量的DRAM去充分利用内存通道增加单台机器的内存带宽"
                            3. 后台流量从TCP切换到RDMA
                            4. 远端缓存直接访问
                                1. "Pangu团队发现数据离开网卡后在内存中时间非常短（平均几百微秒）。
                                2. 假设在内存中停留的时间平均为200微秒的，对于双端口100 Gbps的网卡，只需要5 MB的临时存储来存储离开NIC的数据，
                                3. 因此他们使用英特尔的DDIO在商用硬件上实现了RDCA (Remote Direct Cache Access)
                                4. 使得发送这可以绕过接受者的内存直接访问Cache。
                                5. 在盘古的一些集群上的广泛评估结果表明，对于典型的存储工作负载，RDCA每台服务器消耗12MB LLC缓存(占总缓存的20%)，平均内存带宽消耗减少了89%，网络吞吐量提高了9%。
                                6. RDCA在非存储工作负载中也很有效，例如，在延迟敏感的HPC应用程序中，它将集合通信的平均延迟降低了多达35.1%
                        3. CPU瓶颈
                            1. "对网络和内存优化后，100Gbps网卡下吞吐依然只达到了理论值的80%。主要是因为序列化/反序列化、数据压缩和CRC计算都消耗了大量的CPU资源，使得CPU称为了瓶颈。"
                            2. "混合RPC。 Pangu团队发现RPC请求中序列化/反序列化消耗了30%的CPU，
                                1. 因此他们对数据链路使用类似FlatBuffer替代Protobuf，但是在控制链路依然使用ProtoBuf，最终优化后单核CPU网络吞吐增加了59%"
                            3. "使用CPU wait指令支持超线程。 引入cpu wait指令解决超线程存在的同一个物理核线程切换的开销以及两个线程同时执行相互干扰带来的性能退化，最终单核CPU网络吞吐增加了31.6%"
                            4. "软硬件系统设计。 引入可编程FPGA硬件，将数据压缩和CRC计算卸载到FPGA进行，同样的网络吞吐下，可以节省30%的CPU开销[3]"
                                1. [3] POLARDB Meets Computational Storage: Efficiently Support Analytical Workloads in Cloud-Native Relational Database
                    3. 其他优化案例
                        1. 进行大量的数据完整性校验
                        2. "处理一些影响SLA的异常抖动。比如TCMalloc在申请内存时候如果触发了从全局内存申请则会产生延迟抖动，
                            1. 因此他们引入了用户空间的内存分配池，优化RDMA驱动使用匿名页。
                            2. 其次一些周期性的任务放到后台执行，比如打印日志，
                            3. 还有比如内存占用过高时候进行内存回收会导致很高的CPU使用率，因此调整了内存回收阈值减少回收的机会"
                        3. "处理USSOS中的可纠正机器检查异常(MCE)以提高可用性。
                            1. 增加后台守护进程去检测和处理MCE错误，一旦发现就会通知内核迁移故障的内存"
                        4. "处理USSOS中的可纠正机器检查异常(MCE)以提高可用性。增加后台守护进程去检测和处理MCE错误，一旦发现就会通知内核迁移故障的内存"
            6. 经验教训
                1. 用户态系统
                    1. 用户态系统的开发和运营比内核空间系统更简单。
                    2. 开发用户空间系统应该借鉴内核空间的设计。不仅需要统一存储和网络堆栈，还需要设计用户空间模块来管理内存、CPU调度和硬件故障处理
                    3. 用户空间系统的性能提升不仅适用于高速存储设备，如SSD。
                        1. Pangu的USSFS中提供了一系列机制来加速HDD的性能
                            1. 例如利用自包含的块布局来减少元数据操作次数，
                            2. 利用磁盘内部和外部轨道的差异来提高写入效率
                2. 性能和成本
                    1. "为了满足新的业务需求，Pangu通常首选添加更多硬件来提高性能，基于总拥有成本（TCO）平衡考虑（例如，将网络从25 Gbps升级到100 Gbps，通过增加更多小容量DRAM和升级更强大的CPU来增加内存通道数量）
                    2. 硬件扩展有效地提高了Pangu的性能，但由于产生的成本不可持续，因此Pangu还花费了大量精力，例如流量优化，提高其资源利用率和效率
                    3. 在性能和成本之间进行权衡是必要的，Pangu通过定期评估业务需求和硬件资源的使用情况来确保平衡"
                3. PMem
                    1. "Pme确实有很多优点，Pangu基于Pmem也开发了30us的EBS服务，但是PMem最终还是被Intel砍掉了，所以在开发新服务时，需要更加深入地考虑替代性、可持续性和成本权衡等因素"

                4. 硬件卸载
                    1. "硬件卸载的成本与收益权衡。Pangu硬件卸载压缩的整个开发过程用了20人团队两年时间，期间也解决了许多问题，如FPGA硬件成本、压缩数据的完整性以及与硬件中的其他功能共存等问题
                    2. 硬件卸载的结果收益大大超过了成本。硬件卸载显著降低了压缩的平均延迟和尾延迟，有效降低了低延迟内的网络流量，服务的整体能力提高了约50%
                    3. 内部先使用，然后逐步扩展到核心服务，整个过程中为了防止可能存在的硬件错误损害数据完整性，在硬件上执行数据解压缩和CRC检查，定期地进行软件CRC检查
                    4. Pangu的所有200 Gbps集群默认启用硬件压缩，事故发生的次数越来越少"

        2. Pangu FS client: Fisc: A Large-scale Cloud-native-oriented File System    [2023, 3 refs, FAST23, Alibaba]
           https://www.usenix.org/conference/fast23/presentation/li-qiang-fisc
            1. Same top author "Qiang Li" as the Pangu 2.0 paper. Referenced as
                1. "On top of the Pangu Core, the Pangu Service provides traditional cloud storage services (e.g., EBS, OSS, and NAS) and cloud-native storage services through a cloud-native-oriented file system (i.e., Fisc [15])."
                2. "Pangu Service提供一个一个面向云原生的文件系统服务Fisc[1]"
            2. Key takeaway: Not only offloading but also aggregates resources in Fisc Client to Fisc Agent. Fisc Agent runs on DPU and FPGA.
               Common optimization: Storage gateway routes per file ranges, and can be bypassed once Fisc Client cached metadata. And score based LB.
               16% CPU and 57% lower memory than traditional file client. ~500us E2E latency while LB cost ~ms.
            3. Highlights
                1. Traditional file client has problems
                    1. Thousands containers running in one server, a heavy file client per container uses too much resource
                        1. And, The CPU/memory/network resources among containers cannot be multiplexed 
                    2. RDMA and NVMe requires yet lower latency for the file client. The high bandwidth uses too much CPU
                    3. Network load balancer is unsuitable, yields poor performance, imbalance due to not aware of file. It needs pass-through
                2. Key designs
                    1. Reducing and multiplexing resources among lots of file clients
                        1. Lightweighted client passes virtual RPC to underlay Fisc Agent (Virtio-Fisc Device)
                        2. Fisc Agent aggregates other functionalities passed down from client.
                            1. not only offloading, but also aggregates resources
                        3. Fisc Agent leverages FPGA and DPU to hardware offload
                            1. Fastpath: On Fisc Agent, FPGA packet process bypasses the CPU of DPU by cached route table
                        4. My question
                            1. "CPU of DPU". From the chart, it seems the Fisc Agent is entirely running at the DPU chip? And, it seems FPGA is also on the DPU chip.
                            2. "69% CPU resource compared to traditional file client". 69% still seems too high? It's using DPU now.
                    2. Building a storage-aware gateway to provide performance and SLA
                        1. Storage-aware distributed gateway. vRPC held by client, vRPC Server is here.
                            1. File range based route table
                            2. Score based retry / blacklist / reopen
                            3. Locality aware read
                                1. Fisc client remembers file replica, and then bypasses the gateway (direct communicate)
                                2. ~500us E2E latency while LB cost ~ms
                        2. No extra middle load balancer. Deploy Luna / Solar / RDMA
                            1. [1] From Luna to Solar: The Evolutions of the Compute-to-Storage Networks in Alibaba Cloud
                        3. My question
                            1. Would an extra gateway uses more network bandwidth, and more serialization/deserialization cost
                    3. X-Dragon DPU: [33] Hyperscale FPGA-as-aService Architecture for Large-scale Distributed Graph Neural Network

        3. Pangu Networking: From Luna to Solar: The Evolutions of the Compute-to-Storage Networks in Alibaba Cloud    [2022, 8 refs, SIGCOMM22, Alibaba]
           https://rmiao.github.io/assets/pdf/solar-sigcomm22.pdf
           https://www.youtube.com/watch?v=tLvefIU8QWg
            1. As referenced by the Pangu 2.0 paper and Fisc paper. Reveals Alibaba Cloud the networking architecture.
               Core idea: each network packet is a self-contained storage data block. and no need to maintain packet ordering because blocks are independent
               Technology: hardware offloading the entire EBS data path, as much as possible. Ali-DPU. Packet processing zero-touch to CPU or memory
               SOLAR/LUNA was originally designed for TCP/UDP, but can also work on RDMA. SOLAR is to replace LUNA. 
            2. Highlights
                1. Problem to solve, Problems from Luna
                    1. Context: The compute-storage separation of EBS.
                    2. LUNA is a user-space TCP stack that needs to match speed of SSD and RDMA
                        1. LUNA was to replace the kernel networking stack
                2. Solar solutions - SOLAR: OFFLOAD EPS' DATA PATH
                    1. SOLAR is a storage-oriented UDP stack. with hardware acceleration
                        1. My question: Why not just switch to RDMA?
                    2. Core ideas / insights
                        1. unifying the concepts of network packet and storage data block – each network packet is a self-contained storage data block
                            1. Good. This captures the insight
                        2. storage packets are independent.
                            1. So the storage (in hardware) does not need to maintain receiving buffers for assembling packets into blocks or handling packet reordering
                    3. Key technologies
                        1. merges the packet processing and storage virtualization pipelines to bypass the CPU and PCIe
                            1. Ali-DPU and Bare-metal Clouds.
                                1. Problem: PCIe to host is the bottleneck
                                2. FPGA is error prone to random hardware failures
                            2. See Figure 10 (c). The entire data path is offloaded to FPGA, no CPU (on DPU) involved (zero-touch to CPU or memory) 
                                1. Interesting design here. The idea is also shared by Pangu Fisc Fastpath.
                        2. the storage (in hardware) does not need to maintain receiving buffers for assembling packets into blocks or handling packet reordering
                        3. SOLAR multi-path transport for fast failure recovery
                            1. easier to implement because no need to track packet ordering.
                                1. Compared to before, no need to maintain the complex state machine
                            2. TCP multi-path transport
                               https://network-insight.net/2016/12/10/multipath-tcp/
                        4. DPU: formalize the storage virtualization procedure into a P4-compatible packet processing pipeline
                            1. Data path of SA can be expressed with the P4 language and executed on the P4-compatible pipeline
                            2. About Ali-DPU
                                1. "As our early version of DPU, ALI-DPU, which integrates FPGA for the progammable data plane with interconnection options, has some critical resource limitations by that time. First, the FPGA's resource is minimal due to the hardware cost and power consumption concerns (e.g., DPU is typically limited to 100⇠300 Watt), and the infrastructure CPU on ALI-DPU only has six cores. I"
                                2. Commodity DPU is an alternative from Ali-DPU
                                    1. "it was clear that ASIC will finally replace FPGA after the solution of hypervisor offloading converges because DPU needs to optimize the cost and the power consumption; 
                                    2. it was also predictable that DPU would have a programmable packet processing pipeline (and use languages like P4) for offloading networking functions"
                3. Working with RDMA?
                    1. "With LUNA and RDMA deployed in FN and BN, respectively", "The BN of LUNA and SOLAR is RDMA"
                        1. So LUNA and SOLAR can run with RDMA. See paper for BN "When Cloud Storage Meets RDMA"
                    2. "RoCE uses PFC for flow control, which is a reachability risk because PFC storms or deadlocks in large-scale networks like FN can be disasters [26]"
                        1. "Instead, our design choice is that FN should be loss-tolerant, and shallow buffer switches are used within the region to save cost"
                4. My questions
                    1. Kernel bypassing is the first step, as in Pangu 2.0 USSOS/USSFS. Will offloading to DPU also be the future of storage systems?

            n. related materials
                1. Pangu RDMA: When Cloud Storage Meets RDMA    [2021, 32 refs, NSDI21, Alibaba]
                   https://www.usenix.org/conference/nsdi21/presentation/gao
                    1. As referenced by [17] "When Cloud Storage Meets RDMA" in Pangu 2.0 paper. "As such, Pangu upgrades to lossy RDMA, in which pause frames are disabled, to avoid these problems and improve performance"
                       "Luna to Solar" paper is for networking stack, while this paper is for RDMA.
                       Key technologies: PFC storm handling "escaping as fast as possible", RDMA fallback to TCP, UMR CRC offloading. HPCC vs DCQCN
                    2. Highlights
                        1. Pangu 2.0's userspace storage is already here in this paper (https://youtu.be/8zziI7UPGmQ?t=157)
                            1. Userspace Storage Operation System - USSOS
                            2. Userspace Storage File System & Driver - USSFS
                        2. Zero data copy from NIC to SSD, and add CRC to per block 
                            1. UMR CRC offloading. Let NIC add CRC to per block (Zero-Copy & CRC Offloading)
                                1. User-Mode Memory Registration (UMR) feature of RNICs
                                2. We use UMR to remap the continuous data from the sender into an I/O buffer at the receiver, which contains 4KB data, a 4B footer, and a 44B gap in each unit. 
                                   Following the CRC calculation, the filled I/O buffer can be directly applied for disk writing. 
                                   Besides, the CRC calculation is able to be offloaded to capable RNICs (e.g., Mellanox CX-5), thus lowering CPU and memory usage. 
                                   The 4KB data are posted to the RNIC and the 4B CRC checksum is then generated.
                        3. Queue Pair number explosion in 100Gbps Network
                            1. Don't use Full Mesh. Each thread connects to another thread (RDMA specific problem?)
                            2. Instead, Shared QP. Only do QP in correspondent threads
                        4. Improve availability with RDMA/TCP hybrid traffic
                            1. RDMA fallback to TCP.
                            2. Disable LRO. NUMA
                            3. Escape-as-fast-as-possible design principle to handle PFC (Priority Flow Control) pause frame storms 
                                1. RDMA-enabled Pangu clusters do encounter such problems, including PFC deadlocks [13], PFC pause frame storms, and head-of-line blocking [27, 44].
                                2. We determined several PFC storms to be attributed to a previously unexplored source that consequently invalidates an earlier solution [13]
                                    1. "We investigated this problem together with Mellanox and determined that the processing of TCP in the Linux kernel is highly I/O intensive. Kernel TCP initiates too many partial writes on NICs' PCIe bus. As the PCIe bandwidth is consumed, the receiving pipeline of a NIC is slowed down. The buffer overflows and the NIC subsequently begins to transmit PFC pause frames."
                                        1. Problem: PCIe bandwidth exhausted 
                                    2. Problem: PFC frame polluting server->ToR->Leaf, PFC storm
                                        1. Fig. 9(a) depicts the phases of this PFC storm: 
                                            (1) The bug slows down the NIC receive processing, filling its buffer; 
                                            (2) the NIC transmits the PFC pauses to its ToR switch in order to prevent packet drop; 
                                            (3) the ToR switch pauses the transmission; 
                                            (4) the ToR switch's buffer becomes full and starts to transmit the PFC pauses; and 
                                            (5) the victim ports are paused and are unable to transmit
                                3. We bring up a fine-grained switching mechanism between RDMA/TCP traffic in Pangu and it handles PFC storms regardless of their causes
                                    1. State of art solution: "Guo et al. [13] built a NICbased watchdog to continuously monitor transmitted pause frames, disabling the PFC mechanism if necessary. In addition, watchdogs were also deployed on the switches for disabling the PFC mechanism when switches receive continuous pause frames and are unable to drain the queuing packets. The switches can subsequently re-enable PFC in the absence of pause frames over a specific period of time."
                                        1. "However, this solution is unable to completely solve the PFC storms originating from switches. 
                                                In particular, the TX pause watchdogs on the NICs will not work since the NIC only receives PFC storms from the switches. 
                                                Furthermore, current switch hardware does not support the monitoring of pause frame transmissions."
                                    2. This paper's solution - "escaping as fast as possible"
                                        1. Workaround 1: shuts down NIC ports affected by PFC storms for several seconds. It's simple and effective
                                        2. Workaround 2: the affected RDMA links in a PFC storm are switched to TCP links
                        5. Dual-ToR topology and podset-level RDMA
                            1. A server connects to two ToRs
                            2. "we deploy Mellanox CX series dual-port RNICs to connect a host with two distinct ToR switches. In particular, two physical ports are bonded to a single IP address."
                        6. Others
                            1. Lossy RDMA in Storage
                                1. "We tested lossy RDMA with Pangu over an extensive period and will deploy it for new clusters"
                                2. "However, enabling the lossy feature with early generation RNICs (e.g., CX-4) that have limited hardware resources and do not support SR is hard"
                            2. NVMe-Over-Fabric
                                1. "The ChunkServer data flow in Pangu is processed by CPUs. However, with NVMe-Over-Fabric, NICs can directly write the received data into NVMe SSDs. This CPU-bypass solution can save CPU costs and reduce latency."
                            3. working with DCQCN
                                1. DCQCN [52] is integrated in Mellanox RNICs. "In Pangu, we tune several parameters in DCQCN to improve its performance in fail-over scenarios"
                                2. "When removing the Fast Recovery stage in DCQCN, the pause can be eliminated yet the flow tail latency increases due to the slow recovery of the flow rate. 
                                   In contrast, extending the duration of the rate-increase can result in a sharp reduction in the pause but only slightly increases the flow tail latency. 
                                   In our experience, extending the rateincrease duration in DCQCN is effective for storage traffic patterns."
                                3. "In 2019, Alibaba designed HPCC [30], a novel congestion control algorithm for the RDMA network."

        4. X-Dragon: Hyperscale FPGA-as-a-Service Architecture for Large-Scale Distributed Graph Neural Network    [2022, refs, ISCA22, Alibaba]
           https://dl.acm.org/doi/abs/10.1145/3470496.3527439
           https://www.iscaconf.org/isca2022/slides/isca22-li-lsd-gnn.pdf
           https://youtu.be/3unWgKS4Ews?t=2647
            1. As referenced in the Pangu Fisc paper as the DPU solution of Fisc Agent
               4-card FPGA as a proof-of-concept (PoC) system
               A single FPGA can provide up to 894 vCPU's sampling capability. FaaS.mem-opt with FPGA local DRAM and high-speed links to GPU further unleash the benefit to 12.58×
               analysis on dollar cost and comparing with ASIC
            2. Highlights
                1. Problem to solve
                    1. Targeting at LSD-GNN, Bottleneck is Graph Sampling on Distributed System
                2. Key designs
                    1. FPGA chip * 4, nRISC-V programmable processor / controller. 
                    2. Access Engine (AxE)'s goal is to support an order of magnitude more sampling requests in flight in the memory system
                        1. Share-nothing multi-core processing.
                        2. Decoder, Encoder, Scheduler. Output to memory buffer
                        3. Fine-grained (deep) FIFO pipelining
                            1. deeper pipeline, better performance
                        4. Streaming sampling algorithm
                        5. Out-of-order support improve the throughput by 30x
                            1. massive memory level parallelism
                            2. use a 128-bit tag to track request dependency context
                            3. OoO by maintaining order and synchronization with score-board hardware.
                                1. Scoreboard hardware
                                   https://en.wikipedia.org/wiki/Scoreboarding
                                   https://www.icsa.inf.ed.ac.uk/cgi-bin/hase/dlx-scb-m.pl?/depend-t.html
                                    1. Interesting.
                        6. 8K cache dedicated for coalescing of LSD-GNN
                    3. Memory Over Fabric (MoF) is a customized lightweight interconnection between FPGAs
                        1. multi-request in single package, to amortize header size
                        2. address compression for small requests
                    4. RISC-V based central Controller
                        1. Seems, the processor is implemented on FPGA, rather than using ARM.
                        2. queue-based RISC-V coprocessor communication hub (QRCH)
                3. Motivation and Architecture Taxonomy
                    1. "Although customized ASIC could provide better performance, its significant non-recurring engineering (NRE) cost cost makes the ROI less attractive than the off-the-shelf FaaS solutions."
                    2. FaaS.mem-opt (See Table 8)
                        1. MoF for FPGA-FPGA connection
                        2. FPGA local DRAM
                        3. FPGA-GPU connection via in-server fast link
                        4. VPU, See Figure 13
                4. Comparing with ASIC
                    1. "ASIC solution: We see weak motivation for a standalone customized ASIC chip solution to replace the FPGA solution. Performance wise, all standalone sampling chip solutions have a performance upper-bound (i.e., the GPU data input bandwidth). Although an ASIC can provide larger throughput than the FPGA solution, both of them will hit the upper-bound. Cost-wise, ASIC requires a significant NRE cost, but there is not enough volume and demand to even it out. Therefore, FPGA is a more reasonable solution after ROI is calculated."
                4. My questions
                    1. In Pangu Fisc paper, the DPU consists of CPU + FPGA (Figure 5). But I cannot find the CPU in X-Dragon paper?

        5. Pangu SMR: Deployed System: SMRSTORE: A Storage Engine for Cloud Object Storage on HM-SMR Drives    [2023, 2 refs, FAST23, Alibaba]
           https://www.usenix.org/conference/fast23/presentation/zhou
           https://www.youtube.com/watch?v=b_iW94OQmbY
            1. As referenced in Pangu 2.0 paper, "The USSFS provides high-performance, append-only storage engines for different hardware (e.g., SMRSTORE for HM-SMR drives [14])."
               Instead of SMR-aware filesystem (F2FS), Pangu implemented SMRStore Engine to manage SMR drives and NO local filesystem.
               Prod deployed, comparable performance with prior CMR drives
               Key technologies: Pangu file is append-only. Separate streams by types to different pools of zones (workload-aware data placement). Fit chunk to zone size.
               Interesting paper. Pioneering SMR deployment on large cloud production. Didn't mention Erasure Coding / EC, though.
               Vision: "Cloud storage systems [18] and distributed file systems [31]) tend to evolve towards to user space, special purposed [9], and end-to-end integration [11, 32]"
            2. Highlights
                1. Problems to solve
                    1. Replace CMR drives with SMR, no compromise to performance
                    2. Pangu file is append-only, but
                        1. need to fit Chunk size to SMR zone
                        2. IO failures can happen (switch to new chunk)
                    3. SMR-aware filesystem doesn't satisfy needs
                        1. F2FS supports SMR, but suffers 70% throughput drop with random deletion workload
                            1. Problem: F2FS mixes OSS GC/Data/Meta chunks in one zone
                               When OSS GC kicks in, all zones have garbage, and then F2FS GC kicks in
                2. Production deployment
                    1. "Currently, we have deployed SMRSTORE in standard-class Alibaba Cloud Object Storage Service (OSS)
                        1. to store hundreds of PBs of data.
                        2. We plan to use SMR drives for all classes of OSS in the near future"
                        3. up to 2.16x faster than F2FS on SMR drives
                    2. HM-SMR drives
                        1. ~25% higher areal density
                        2. decrease the total cost by up to 15%
                        3. comparable performance with CMR drives prior systems
                    3. HM-ZMR drives limits
                        1. Zone model (Zone size 256MB)
                        2. Sequential write constraint
                        3. Open zone limit (128)
                3. Existing OSS architecture
                    1. OSS FrontEnd Layer
                    2. OSS Service Layer
                        1. KV server
                        2. Object Index
                            1. Object Foo, Pangu File A, Offset, Length
                    3. Apsara Pangu
                        1. Chunks sealed/unsealed
                        2. HDD Storage Engine
                            1. EXT4 file system
                            2. CMR drive
                    4. OSS workload
                        1. OSS Data Write Streams
                            1. usually live < 7 days
                            2. Data is first written to SSD and then moved to HDD
                        2. OSS Metadata Write Streams
                            1. Chunks are usually small (<16MB)
                        3. OSS GC Streams
                            1. Most chunks are large (>90%)
                            2. Stream concurrency is low (~100 per chunkserver)
                                1. I.e. number of open streams
                        4. All streams do random deletions
                4. Key designs for SMR
                    1. Pangu file is append-only.
                        1. Everything is log
                            1. SMRStone does NOT journal write operations, it's not necessary to maintain a second journaling. Only metadata changes are journaled, which are used in Recovery
                        2. SMR GC is still necessary even with SMRStore. Due to small sized chunks. Note OSS GC works on another level.
                            1. SMRStore runs the "SMR GC"
                            2. My questions
                                1. Can the SMR GC and OSS GC be merged, or co-work coordinated? For example, SMR GC to a file may become unnecessary, if OSS GC already decided to rewrite it.
                    2. SMRStore - the new storage engine for SMR
                        1. HDD Engine operates CMR HDD on EXT4. While SMR Store Engine operates SMR HDD
                            1. My question
                                1. So, SMR Store Engine bypasses the local filesystem?
                                    1. Yes. See on-disk layout.
                        2. Zoned block layer, zoned block interface
                    3. SMRStore components
                        1. On-disk layout
                            1. Everything is a record. Log-structured design
                                1. record payload is of variable size. A zone packs many records
                            2. Superzone, metazone list, datazone list
                        2. Data index
                            1. In-memory data index
                                1. Chunk ID => Index Group List => Index Group => Record Index List
                            2. Workload-aware data placement
                                1. Strategy 1: Separating streams by types.
                                    1. GC is organized into pools: OSS GC pool, OSS Data pool, OSS Meta pool
                                2. Strategy 2: Adapting chunk size limit for datazone. Most chunks can be large.
                                    1. Set chunk size to zone size. Fill datazone only one chunk. GC delete a zone at once
                                    2. OSS GC pool and OSS Data pool account for ~78% traffic
                                        1. Most chunks are of zone size. But some chunks are small, interleaved with other chunks. Need SMR GC
                                3. Strategy 3: Zone pool & round-robin allocation. Lower stream concurrency
                                    1. Strategy 3 has ~50% through impact, see Figure 19. It implies stream concurrency is important.
                                       Probably due to active zone exhaustion 
                        3. Garbage collection
                            1. Zones are organized into Pools. GC happens per Pool.
                            2. Best effort to pack a zone with records from the same stream type.
                                1. Set chunk size to zone size. Fill datazone only one chunk. GC delete a zone at once
                        4. Zone management
                        5. Recovery 
                5. Related works
                    1. GearDB [32], ZenFs [11], SMORE [19], SMRDB [26]
                    2. archival-class object storage systems such as Alibaba Archive Storage Service [1] and Huawei Object Store [18].
                6. My questions
                    1. Didn't mention Erasure Coding at all?
                    2. Combine CMR drives and SMR drives running together?
                        1. Seems NO. "We plan to use SMR drives for all classes of OSS in the near future"
                    3. Strategy 3 has ~50% through impact, see Figure 19. It implies stream concurrency is important.
                       SMRStore introduce the concept records, which breaks a Pangu file into records. Is it due to SMR disk active zone count is smaller than stream concurrency, so it has to mix multiple Pangu File in one zone, then it needs to break Pangu File into a smaller concept?
                    4. With SMRStore, is the cluster only using SMR drives, or mixing SMR and CMR drives?
                        1. A chunkserver uses both HDD and SSD. It looks like HDD are replaced to SMR drives.
                           There should be no point to equip CMR drives, because chunkserver is using SSDs anyway.
                    5. How did SMRStore test GC behaviors?
                        1. High Concurrency Microbenchmark
                            1. High Concurrency Write (HC-W) and High Concurrency Rand Read (HC-RR)
                        2. Multi-Stream Microbenchmark (OSS simulation macro benchmark)
                            1. a more realistic setup with multiple data streams, random deletion, and subsequent F2FS/SMR GC
                            2. test high capacity utilization
                        3. How does the GC traffic compare before/after running with SMR drives?
                            1. Figure 17 compares CS-Ext4 vs CS-SMRStore, but it's comparing write throughput
                            2. Figure 22 is comparing GC throughput, but will SMRStore incurs more GC? It added an extra zone level GC.
                            3. There should be a section called "Garbage collection performance", and to evaluate "SMR GC overhead"
                                1. E.g. Figure 19. Somehow I didn't find an individual chart to tell "SMR GC overhead", all the compares are merged with total write throughput. 
                    6. unifying zone level GC (SMR GC) and OSS GC
                        1. 

        6. Pangu – The High Performance Distributed File System by Alibaba Cloud
           https://www.alibabacloud.com/blog/pangu-the-high-performance-distributed-file-system-by-alibaba-cloud_594059
            1. "deduplication technologies" this is interesting in cloud storage area. But didn't mention how

        7. SelectiveEC: Selective Reconstruction in Erasure-coded Storage Systems    [2020, 4 refs]
           https://www.usenix.org/system/files/hotstorage20_paper_xu.pdf
            1. Interesting. Node failure and then reconstruct repair. Repair is carried out in batch. Within a batch, node level load may be imbalanced
            2. SelectiveEC: 1) select repair tasks so chunk nodes are balanced 2) select replacement nodes so they are also balanced
            n. related materials
              1. Dayu: Fast and Low-interference Data Recovery in Very-large Storage Systems    [2019, 12 refs, ATC19, Alibaba]
                 http://web.cse.ohio-state.edu/~wang.7564/papers/atc19-wang_0.pdf
                  1. Targeting Pangu but seems not prod deployed. Evaluated in a 1,000-node real cluster and in a 25,000-node simulation.
                  2. Existing problems
                    1. "Our simulation of existing scheduling algorithms shows that, on the one hand, simple and decentralized algorithms like random selection or best-of-two-random [9] can finish scheduling quickly (i.e., high speed), but they often cause a small number of nodes to be overloaded, increasing the recovery time and impairing the performance of foreground traffic (i.e., low quality)"
                    2. "On the other hand, sophisticated and centralized algorithms, such as Mixed-Integer Linear Programming [10–12], can effectively utilize available bandwidth and avoid overloading a node (i.e., high quality), but they can take prohibitively long to compute a plan given the scale of our target system (i.e., low speed)."
                  2. Dayu solutions
                    1. periodically monitor the dynamic foreground traffic and adjust the recovery plan
                    2. divide timeslot. schedule a subset of chunks so that they can be re-replicated within the current timeslot
                    3. scheduling algorithms
                       1. Greedy algorithm with bucket convex-hull optimization to schedule tasks
                       2. Prioritizing nodes with high idle bandwidth but few available chunks
                       3. Iterative WSS (weighted shuffle scheduling) to allocate bandwidth for each task
                       4. Re-scheduling stragglers

        8. SepBIT: Separating Data via Block Invalidation Time Inference for Write Amplification Reduction in Log-Structured Storage    [2022, 11 refs, FAST22, Alibaba]
           https://www.usenix.org/conference/fast22/presentation/wang
              1. Logged before
```
