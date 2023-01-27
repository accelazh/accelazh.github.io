这是长篇“分布式存储架构和设计空间”的第二篇。原文有5W多字词，受微信公众号限制长度，需要分P发出。“参考架构”是原文中间的一章，可以独立抽出。

## 存储领域的参考架构

软件架构具有共同的 __系统属性__（system properties），例如 [CAP]([52])。为了实现它们，不同的技术（technique）被发明，并演变成更通用的 __架构设计模式__（architecture design patterns）。将各种驱动因素（driving factors）绘制成地图，它们揭示了 __技术设计空间__（technology design space）的构造，我们在其中探索和航行以构建新系统。后文将专注于 __分布式存储__。

知名的开源和行业系统（industry systems）变成 __参考架构__（reference architectures），可以用来学习流行的技术或设计模式。下文列出了我能很快记起的参考架构（可能 __不完整__ ）。它们可以通过搜索流行产品、比较供应商备选方案、或从高引用论文中找到。

__按存储领域划分__

  * 缓存
  * 文件系统
    * 分布式文件系统
  * 对象/块存储
  * 数据去重
  * 档案存储
  * OLTP/OLAP 数据库
    * Shared logging
  * 内存数据库
    * Manycore
  * NoSQL 数据库
  * 图数据库
  * 数据湖
  * 流处理
  * 持久内存
  * 云原生
    * Cloud scheduling
    * Geo Migration
  * 二级索引
  * Query processing

### 缓存（Cache）

  * [Redis]([73])是大多数互联网公司使用的主流开源内存缓存。与Memcached相比，它支持丰富的数据结构。为实现持久性（durability），它添加了检查点（checkpoint）和操作日志（per operation logging）。数据可以集群分片并主从复制。 [Tendis]([74]) 进一步改进了冷热分层（Hot/cold tiering）和优化。

  * [Kangaroo 缓存]([75])（来自 Facebook 关于 [Scaling Memcached]([76])、[CacheLib]([77]) 和 [RAMP-TAO 缓存一致性]([78]) 的长期工作）在内存中缓存热数据，将冷数据存入闪存（Flash）。大对象（object）和小对象分离，小对象使用追加日志（append-only logging）和组关联缓存（set-associate cache），以实现最佳的内存索引体积与写放大（write amplification）。Kangaroo 还使用“分区索引”（partitioned index）来进一步减少 KLog 的内存索引体积。

  * [BCache]([79]) 是 [Ceph]([80]) 中使用的一种流行的 SSD 块缓存（block cahe）。数据在“Extents”（类似文件系统）中分配，然后组织到更大的桶（bucket）中。压缩以Extent为单位。桶内顺序追加（sequentially append）数据直到填满，桶是GC回收的单位。数据由 B+ 树索引（与 Kangaroo 中使用哈希表的 KLog 不同）。B+ 树使用 256KB 的大节点。节点内部通过追加日志进行修改。 B+-tree 结构变更（structural change）由 COW （copy-on-write）完成，并可能递归地重写每个节点直到树根。由于 COW，日志不是必需的，而是用作对小更新（small updates）的批处理（batching）和顺序化（sequentialize）。

### （分布式）文件系统（Distributed filesystems）

  * [BtrFS]([81]) 用于单机 Linux 文件系统。它使用 B-树 索引inodes，使用 COW 进行更新，使用影子分页（shadow paging）确保原子性（atomicity）。其它同时代系统的有 [XFS]([82])，它也通过 B-tree 建立索引，但通过覆写（overwrite）进行更新； [EXT4]([83])，这是默认的 Linux 文件系统，目录 inode 用树索引文件 inode ，并使用WAL (write-ahead logging) 来确保更新（覆写）原子性。

  * [CephFS]([84]) 引入 MDS 来管理文件系统元数据，例如目录、inode、缓存；而持久化由对象存储支持，例如数据池和元数据池。 CephFS 的特色有 [动态子树分区]([85])和 [Mantle负载平衡]([86])。跨分区事务由 [MDS 日志]([87]) 实现，MDS 在更新前获取 [锁]([88])。

  * [HopsFS]([89]) 在 HDFS 上构建分布式文件系统。 Namenode 变成一个 Quorum，无状态，元数据存储由另一个内存 NewSQL 数据库管理（Offload）。 Inode 被组织成实体关系表（entity-relation table），并进行分区（partition）且减少操作所涉及的服务器数量。跨分区事务（transaction），例如 rename、rmdir ，由 NewSQL 数据库和 Hierarchical locking 实现。子树操作经过优化以并行运行。

  * [HDFS]([90]) 是大数据的分布式文件系统。它放宽了 POSIX 协议的限制，倾向大文件，并运行主/从 Namenode 来序列化事务。 HDFS 最初是 [Google Filesystem]([91]) 的开源实现（Google以 [Big Table]([92])、[Chubby]([93]) 开启了云时代）。 HDFS 之后取得了巨大的成功，成为了大数据的共享协议，跨越文件系统、数据库（例如[HBase]([94])）、SQL（例如[Hive]([95])）、流处理（例如[Spark]([96])）、数据湖（例如[Hudi]([97])），包括开源和商业（例如 [Isilon]([98])）产品。

### 对象/块存储（Object/block storage）

  * [Ceph]([99]) 用于分布式块存储（block storage）和对象存储（object storage），以及CephFS用于分布式文件系统。 Ceph 曾使开源的横向扩展（Scaleout）的存储成为可能，并在 OpenStack 生态系统中占据主导地位（[Ubuntu Openstack 存储调查]([100])）。它在 CRUSH map 中通过基于哈希的放置（Placement）算法来减小元数据体积。它在一个系统中实现对象/块/文件服务
   （converged）。元数据由一个 Paxos quorum（Consistent Core）管理，以实现所有 CAP 属性。 Ceph 条带化（striping）对象并就地更新（update in-place），后者需要单节点事务。 Ceph 后来构建了 [BlueStore]([101])，它是定制化（customized）的文件系统（[Ceph 10 年课程]([102])），针对 SSD 进行了优化，并解决了 [双写问题]([101])。双写（double-write）问题通过分离元数据（委托给 RocksDB），分离键/值数据（如 [Wisckey]([103])）来解决；大块的写（big writes）变为仅追加，小的覆写（small overwrites）合并到 WAL。

  * [Azure 存储]([104]) 用于行业级公有云存储基础设施。它建立在 Stream 层上，这是一个分布式的追加文件系统； 并使用 Table 层，它实现了横向扩展的大表格，以支持 VM （virtual machine，虚拟机）磁盘、对象存储、消息队列。“追加”（Append-only）简化了更新操作，但在垃圾回收 (GC) 方面有更多挑战。 [AWS S3]([105]) 似乎反而遵循 Dynamo，就地更新（猜的），使用一致性哈希来数据分片。对于融合（converging）对象/块/文件存储，[Nutanix]([106]) 类似地，在同一个节点上运行存储和 VM，这与远程连接（remotely attached）的 SAN/NAS 不同。

  * [Tectonic]([107]) 与 Azure 存储类似。它哈希分区元数据以进行横向扩展，采用了 [Copyset Placement]([108])，整合了 Facebook Haystack/F4（对象存储）和数据仓库（data warehouse），并引入了多租户（multitenancy）和资源限流（resource throttling）。 Tectonic 的另一个特性是解耦（decouple）常见的后台任务（background jobs），例如数据修复、迁移（migration）、GC、节点健康检查；它们从元数据节点搬出，变成了后台服务。 [TiDB]([109]) 也有类似的思路，如果将 Placement Driver 移出元数据服务器。

  * [XtremIO]([110]) 使用新颖的基于内容的寻址（content-based addressing）来构建全闪存的块存储阵列。数据放置由其内容的哈希决定，自带支持去重。尽管访问是随机的，但它们在闪存上运行。写入保存到内存中的两个副本后被确认（ack）。其它同期产品包括 [SolidFire]([111])，它也是横向扩展的； 和 [Pure Storage]([112])，它纵向扩展（scale-up），并使用双控制器共享磁盘。

### 数据去重（Data deduplication）

  * [Data Domain]([113]) 是最有名的数据去重存储设备（appliance）之一。它通过 [rolling hash]([114]) 可变长度分块，来识别文件中间的插入。 Locality Preserved Caching 使指纹缓存变得高效，它与备份（backup）工作负载（workload）完美配合。

  * [Ceph dedup]([115]) 在 Ceph 上构建可横向扩展的去重引擎。 去重后的块存储在 Ceph 中，以哈希指纹为键。它引入了一个新的元数据池，来查找对象 ID 到块的映射。去重操作离线（offline）进行，并受到限流。类似的二级间指（indirection）模式，也可用于将小文件合并为大块。

### 归档存储（archival storage）

  * [Pelican]([116]) 是 rack-scale 的归档存储（或称为冷存储（cold storage），近线存储（near-line storage）），它与硬件协同设计（co-design），以减少磁盘/CPU/冷却功率，仅8%的磁盘处于旋转状态。数据经过擦除编码（erasure code）并跨磁盘组条带化。 [Flamingo]([117]) 继 Pelican 的研究，根据 Pelican 环境配置，生成最佳数据布局和 IO 调度配置。归档存储因政府合规（compliance）需求而广泛采用，例如 [AWS Glacier]([118]) 。

  * [Pergamum]([119]) 协同设计硬件，作为一个存储设备（appliance），始终保持 95% 的磁盘断电。每个节点都添加了 NVRAM，用于保存签名和元数据，以允许在不唤醒磁盘的情况下进行验证。数据在磁盘内和磁盘间进行纠删编码。 [磁带库]([120]) （tape library）由于容量成本、可靠性和吞吐量的改进，仍然是有吸引力的归档存储介质。

### OLTP/OLAP 数据库

  * [CockroachDB]([121]) 是支持 Serializable ACID 的跨区域（cross-region） SQL 数据库，可看作 [Google Spanner]([122]) 的开源实现。它通过 [Hybrid-Logical Clock]([123]) (HLC) 避免对 TrueTime 的依赖。 CockroachDB 将 SQL schema 映射到键值对 (key-value pair，KV) 并 [存储在 RocksDB 中]([124])。它使用 [Raft]([125]) 来复制分区数据。它构建了新颖的 [Write Pipelining]([126]) 和 [Parallel Commit]([127]) 来加速事务执行。另一个同期产品是 [YugabyteDB]([128])，它在查询层重用 PostgreSQL，用 DocDB 代替 RocksDB，它和 CockroachDB 有过一场有趣的辩论（[YugabyteDB挑战CockroachDB]([129])，[知乎YugabyteDB/CockroachDB辩论]([130])，[CockroachDB 反驳 YugabyteDB]([131])）。

  * [TiDB]([61]) 与 CockroachDB 类似。它倾向于单个地理区域，并使用时间戳 Oracle 服务器来序列化事务，基于 [Percolator]([132]) 实现事务。 TiDB 进一步结合了 OLTP/OLAP（即 HTAP），通过 Raft 从基线（baseline）行格式（row format）数据复制到一个额外的列式（columnar）副本（[TiFlash]([133])）。同期产品中（[Greenplum's related works]([134])），为了同时支持 OLTP/OLAP，除 HyPer/MemSQL/Greenplum 外，Oracle Exadata（OLTP）通过引入 NVMe flash 和 RDMA，并增加内存列式缓存来提升OLAP性能； AWS Aurora (OLTP) 将 OLAP 卸载（offload）到云端并行处理； [F1 Lightning]([135]) 从 OLTP 数据库（Spanner，F1 DB）复制数据并将它们转换为 OLAP 所需的列格式，支持快照一致性（snapshot consistency）。

  * [OceanBase]([136]) 是一个分布式 SQL 数据库，与 MySQL 兼容，支持 OLTP/OLAP 和 [混合行-列数据布局]([137])。它使用中央控制器（Paxos 复制）来序列化分布式事务。同期的 [X-Engine]([138]) 是一个与 MySQL 兼容的 LSM-tree 存储引擎，被 [PolarDB]([139]) 使用。 X-Engine 使用 FPGA 进行 compaction。读/写路径分离以应对流量激增。 X-Engine 还引入了多阶段流水线（multi-staged pipeline），任务被分解为小块，异步执行，并流水线化，类似于 [SeaStar]([140])。 PolarDB 的另一个特色是将查询下推（pushdown）到 Smart SSD（[Smart SSD 论文]([141])），它在磁盘盒内完成计算以减少过滤后的输出。后者 [PolarDB Serverless]([142]) 转向了像 Snowflake 这样的 disaggregated 云原生架构。

  * [AnalyticDB]([143]) 是阿里巴巴的 OLAP 数据库。它将数据存储在共享的 [Pangu]([144]) (HDFS++) 上，并通过 [Fuxi]([145]) ([YARN]([146])++) 调度任务。数据以混合行列数据布局（row groups）进行组织。写节点和读节点分离，独立扩展。更新首先作为增量追加，然后在写路径外合并，并在所有列上构建索引。基线+增量的思路类似于 [Lambda 架构]([147])。

  * [ClickHouse]([148]) 是最近迅速流行起来的 OLAP 数据库，因“非常快”知名（[为什么 ClickHouse 很快]([477])）。除了常见的列格式、矢量化查询执行（vectorized query execution）、数据压缩之外，ClickHouse 还通过“关注底层细节”进一步优化。 ClickHouse 支持各种索引（以及全扫描（full scan））。它通过 [MergeTree]([149])（类似于 LSM-tree）吸收更新。应用于 OLAP 场景，ClickHouse 不支持（完整的）事务。

  * [AWS Redshift]([150]) 是基于 PostgreSQL 的新一代云原生数据仓库。数据保存在 AWS S3，同时缓存在本地 SSD（类似于 Snowflake）。查询处理节点由 [AWS Nitro]([151]) ASIC 加速。它配备了现代数据库功能，例如代码生成（code generation）和矢量化 SIMD 扫描、external compilation cache、AZ64 编码、[Serial Safe Net]([152]) (SSN) 事务 MVCC、机器学习支持的 Auto tuning、半结构化查询（semi-structured query）。它可与 Datalake 和 OLTP 系统进行联邦查询（federated query）。

  * [Log is databse 1]([153]) / [日志是数据库 2]([154]) / [日志是数据库 3]([155])。该概念首次出现在 [AWS Aurora Multi-master]([156]) 上。日志被作为最终数据（single
   source of truth）来复制，而不是同步磁盘页面（disk page）。页面服务器被视为重放日志的缓存。同类中，[CORFU]([157])、[Delos]([158]) 将分布式共享日志构建为服务。 [Helios Indexing]([159])、[FoundationDB]([160])、[HyderDB]([161]) 在共享日志上构建数据库。

### 内存数据库（In-memory database）

  * [HyPer]([162]) 内存数据库发表了不少优秀论文。它领先于 [矢量化查询执行]([163])和代码生成，其中 [LLVM]([164]) 通常用于编译 IR（intermediate representation）。其它特色有 [Morsel-driven execution scheduling]([165])，用“fork()”从 OLTP 创建 OLAP 快照，等等。其它同期产品包括 [SAP HANA]([166])，它结合了 OLTP/OLAP（利用增量结构）并支持丰富的分析查询； [MemSQL]([167])，通过添加行/列格式来支持 OLTP/OLAP； 而[GreenPlum]([134])将PostgreSQL扩展为MPP，增加了GemFire（[12306.cn使用GemFire]([168])）进行内存处理，在OLAP之后增加了OLTP，并进行性能提升和资源隔离。

  * [Hekaton]([169]) 是 Microsoft SQL Server 的内存数据库引擎。它的无锁 [Bw-Tree]([170]) 具有特色，通过追加增量和合并（merge）来工作。 Bw-tree 需要 [Page Mapping Table]([171])（[LLAMA]([172])）用于原子页面更新，并避免将页面 ID 变更传播到父节点。 Bw-tree 的 SSD 组件也可以是仅追加的（append-only），在 [DocumentDB]([173]) 中有 “Blind Incremental Update” 。 Hekaton 也有 [Project Siberia]([174]) 来对冷热数据进行分层（tiering），它使用自适应过滤器（adaptive filters）来判断数据是否处于冷磁盘上；冷热分类（classification）是 [离线]([175]) 地对记录访问日志的采样进行的。

  * [ART 树]([176]) 是内存数据库（以及 PMEM）的流行索引之一（例如 HyPer）。它本质上是自适应节点大小的基数树（radix tree）。其它同期索引包括 [Masstree]([177])，它是由 B+树组成的的 trie树，以及各种优化的集大成者； [Bw树]([171])； 和 [Be-tree]([178])，它使用每个节点的缓冲区来吸收随机更新，在 [VMWare 文件复制]([179]) 中采用。查询过滤方面，除常用的 [BloomFilter]([180])外，[SuRF]([181]) 也支持范围查询，但更新代价较高。

  * [FaRM]([182]) 在 RDMA 和 UPS 保护的 PMEM 上构建可横向扩展的内存数据库，支持快速的 Serializable 的事务。它通过减少消息数量、One-sided RDMA 读/写，以及并行性，来克服 CPU 瓶颈。数据是分片的。分布式事务用2PC实现； 锁持久化在每个分区的主节点的日志中； 读是无锁的； 协调者（coordinator）没有持久状态。 Zookeeper 用于维护节点成员资格（node membership）。对象通过键（指针地址）来访问。后续工作 [A1]([183]) 在 FaRM 之上构建图数据库，并使用 [DCQCN]([184]) 缓解 RDMA 拥塞。

  * [Silo]([185]) 利用基于Epoch的组提交（group commit）来构建 OCC Serializable 事务协议，由 Masstree 索引。 [Manycore]([186])（40+ CPU 内核）显着改变了 HPC、内存、PMEM 系统中的并发设计； 例如 [Linux 内核 manycore]([187])，[文件系统 manycore]([188])。除了自定义latching和fencing，经常使用的技术如 [Epoch-based Reclamation]([189])（例如在 Masstree 中）、[Sloppy Counter]([187])、[Flat Combining]([190])、Shared Nothing。 Epoch-based Reclamation 将频繁的内存操作分组为更大的不频繁的 Epoch； 线程在本地内存上工作，除了 GC 在 Epoch不活动后访问所有线程内存。 [RCU]([70]) 类似，在所有事务超过低水位（low-watermark）的Epoch后，旧的 DB 记录版本可以被回收。 Sloppy Counter 将引用计数拆分为全局计数器和各个核的计数器，大多数操作发生在线程本地。在 Flat Combining 中，工作线程将请求发布到线程本地内存（thread-local），然后竞争全局 CAS（compare-and-set），最后的唯一赢家批量执行所有线程的请求。 Shared Nothing 是高并发的银弹，只要系统可以这样设计（例如 [NetApp Waffinity]([191])）。

### NoSQL 数据库

  * [RocksDB]([192]) 是基于 LSM-tree 的单节点键值存储的主流实现。它被用作 [许多系统的 KV 后端]([193])，例如 [MySQL MyRocks]([194])、[CockroachDB on RocksDB]([124])、[TiDB on RocksDB]([195])、[BlueStore RocksDB]([196])。它也经常在互联网公司中使用（[RocksDB FAQ]([197])）。RocksDB的特色有 [Universal Compaction]([198])、SSD 优化、和 [Remote Compaction]([199])（将 compaction 卸载到基于云的共享存储上）。在分层（tiering）方案中，[PebblesDB]([200]) 在每个 LSM-tree 层级中插入更多的 [SST "Guards"]([201])，其工作方式类似于用跳表（skip list）来约束和索引 SST 文件的键范围，从而减少读放大（read amplification）。

  * [FoundationDB]([160]) 实现分布式 KV 存储并支持 ACID 事务。事务实现由共享日志系统支持。控制面（control plane）、事务、共享日志（shared logging）、存储系统是解耦的。 FoundationDB 还利用共享日志构建快速恢复（fast recovery）能力。此外，FoundationDB 还基于 Flow 构建确定性模拟测试（Deterministic Simulation Testing）。

  * [MongoDB]([202]) 是流行的 JSON 文档数据库，是最成功的开源数据库之一，并进入了 [IPO]([203])。 MongoDB 的流行有赖于易用性。 水平扩展由分片（范围/哈希）实现，HA（高可用性，High availability）由副本集（replica set，1 个写 + N 个读副本）实现。

  * [HBase]([204])是 [Big Table]([92]) 的一个开源实现。表基于范围分区（range partitioning），元数据由 [ZooKeeper]([205])（Chubby 的开源实现，或曰 Paxos + [复制状态机]([206]) + 命名空间索引（namespace indexing））管理。分区服务器使用 LSM-tree 来管理更新，共有 MemTable、HFile、Compaction 等概念。 HBase 支持可变列（variable column schema），按时间戳版本检索，和行级原子操作，可以使用 [Percolator]([207]) 构建跨分区事务。 HBase 成为 HDFS 上的主流大表格数据库，并常用作 SQL、时间序列数据库、块存储等的后端。 ByteDance 将 Big Table 和 Spanner 定制化实现为 [ByteSQL]([208]) 和 [Bytable]([209])。阿里巴巴定制化 HBase 并发布了 [Lindorm]([210])。

  * [Cassandra]([211]) 遵循 [Dynamo]([212]) 的点对点 (P2P) 集群管理，而 [DynamoDB]([213])（[论文]([214])）由 AWS 商业运营，也遵循 Dynamo。它没有专用的元数据 Quorum，但在对等节点中携带元数据并使用 [Gossip]([215]) 协议传播。它支持需要主键的大表格。键由 [Consistent Hashing]([216]) 进行分区和放置（placement），以避免节点加入/离开时的额外数据迁移。 Cassandra 采用 quorum write/read（写入 N 个副本，读取 N/2+1 个副本）来确保持久性和版本一致性。类似的 P2P 集群管理可以在 [Service Fabric]([217]) 中找到，它托管微服务（microservice），为节点成员资格（node membership）的一致性做了很多工作。

  * [ElasticSearch][478] 起源于基于 Apache Lucene 的全文搜索引擎，非常受欢迎，然后演变为可横向扩展的，支持丰富搜索功能的数据库，可存储 JSON 文档、日志记录、时间序列、[地理空间数据]([218])。 [ElasticSearch scaleout]([219]) 通过主从复制和哈希分片来管理数据。曾经 ElasticSearch 也因 [ELK stack]([220]) 所熟知。

  * [InfluxDB]([221]) 是一个流行的时间序列数据库。与 SQL 数据库相比，时间序列数据库可以利用固定的数据组织和查询模式，可以聚合（aggregate）指标维度（metrics dimensions）以应对高速数据流入，并重新采样以冷热分层（tiering）数据。另一个产品是 [OpenTSDB]([222])，它基于 HBase 提供时间序列服务。时间序列数据库经常用于监控（例如 [Prometheus]([223])）和物联网（例如 [InfluxDB IoT]([224])）。

### 图数据库（Graph database）

  * [Graphene]([225]) 代表图数据库的典型实现，基于半外部内存（semi-external memory, 即 DRAM + 磁盘）。为加速查询，它协同放置（co-locating）常常一起访问的边（edges）和顶点（vertices），管理小对象和细粒度 IO 。更早的工作可以追溯到 [GraphLab]([226])。其它同时代产品的还有 [Neo4J]([227])，源于在数据库中保存对象图（Object-oriented）； [ArangoDB]([228])，支持 [JSON文档图]([229]) 和多模（multi-mode）； [OrientDB]([230]) 也是一个 [多模型数据库]([231])。图数据库经常用于社交网络挖掘（social network mining）和迭代机器学习（iterative machine learning）。

  * [Facebook TAO]([78]) 为社交图谱（social graph）的 OLTP 实现了精简的两级架构。持久性/容量层由 [MySQL]([232]) 提供，它使用 [RocksDB]([194]) 作为引擎。 QPS/缓存层由 Memcached 提供，有很多改进（例如 [CacheLib]([77])）。为了一致性，TAO 支持跨分片的2PC，并防止 fracture read（不是 ACID，不是快照隔离（snapshot isolation））。查询为获取关联数据而优化。

  * [FaRM A1]([233])。 Bing 用于知识图谱（knowledge graph）的通用图数据库，全部数据在内存中。顶点/边被组织在链接结构对象中，通过指针地址访问，并通过 FaRM 实现乐观并发控制 (OCC) 事务和 MVCC（multi-version concurrency control）读取。其它同期产品包括 [AWS Neptune]([234])； [CosmosDB]([235])，它从 [DocumentDB]([173]) 发展而来，是一个全球分布式（globally distributed）的强一致性的多模型数据库，使用 Bw-tree with "Blind Incremental Update" 而不是 LSM-tree 来吸收更新。

  * [ByteGraph]([236]) 在 RocksDB ([TerarkDB]([237])) 上构建图数据库，支持具有广泛兼容性的 [Gremlin API]([238])。加权的一致性哈希环将顶点和相邻边分片到同一个节点。 RocksDB 用 KV 轻松表示顶点和边，支持内存/磁盘分层和单节点事务。 Large edge list 由 edge-tree（B-tree）实现，并进一步支持二级索引。 ByteGraph 还支持地理复制（geo replication，最终一致性），分布式事务 (2PC) ，和基于成本的查询优化器（cost-based query optimizer）。

### 数据湖（Datalake）

  * [Apache Hudi]([239]) 在 HDFS、Kafka、Spark、Hive 上构建数据湖。与数据仓库相比，它允许通过 CopyOnWrite 或 MergeOnRead 更新数据。其它 [datalake contemporaries]([240]) 包括 [Delta Lake]([241])，它为 Spark 带来了 ACID； [Apache Iceberg]([242])，它支持高性能的查询。 Datalakes 一般强调跨系统的互操作性（interoperability）。结合数据湖和数据仓库，你会得到 [Lakehouse]([243]) 模式。

  * [F1 Query]([244]) 连接多个数据源，如 Spanner、BigTable、CSV、ColumnIO、Capacitor、ETL，以创建联邦查询引擎。之前的 [F1]([245]) 建立在 Spanner 上并服务于 Google AdWords。 F1 Query 支持包括 join 的交互式 SQL 查询（interactive SQL queries），批量查询，通过 UDF 服务器支持自定义的 UDF。查询作为 DAG 并行执行，其中 “dynamic range repartitioning” 减轻了数据倾斜（data skew）带来的影响。 F1 Query 在查询优化器中使用启发式规则（heuristic rules）。此外，[F1 Lightning]([135]) 通过复制额外的列式副本来增加对 HTAP 的支持，并通过跟踪时间戳水印（timestamp watermarks）来提供快照一致性（snapshot consistency）。

### 流处理（Stream processing）

  * [Kafka Transactional]([246]) 在消息队列中实现了 exactly-once 的事务级别的一致性。这使得流处理变得可靠，能成为比数据库表更好的一等公民。这进一步使结合 transactional spark 的 [Kappa 架构]([247]) 成为可能，以取代双重成本的 Lambda 架构。

  * [Spark]([248]) 是主流大数据计算框架之一。相比 MapReduce，Spark 支持基于内存的 RDD 和 micro-batch 处理。 Spark 之后扩展到 [Spark 流处理]([249])。 在 [Stream processing contemporaries]([250])中，[Flink]([251]) 使用 one-by-one 式的流处理（而不是 micro-batch），实现 [checkpointed 2PC exactly-once]([252])， 和 [ack by XOR of path nodes]([253])。

### 持久内存（Persistent memory）

  * [NOVA]([254]) 在持久内存 (PMEM) 上构建高并发的文件系统，有很多可借鉴的设计模式。 NOVA 通过 DRAM 基数树（radix tree）建立索引，并通过每个 inode 的日志、每个CPU核的 free-list 来提高并发性。 Nova 在（定制的）DAX-mmap 上使用日志、COW、`clwb` 指令构建原子文件操作。 [ART 和哈希表]([255]) 也是 PMEM 存储的常用索引。

  * [Level Hashing]([256])。尽管 NOVA 使用基于树的 PMEM 数据结构（文件系统 inode 树），但另一种方法尝试在 PMEM 上使用哈希表数据结构。后者有利于 O(1) 查找。 Level Hashing 不使用日志。调整大小是通过两级旋转完成的。崩溃一致性（crash consistency）通过小心操作标志位来保证。但是，基于哈希的 PMEM 数据结构不支持范围查询（range query）。

  * [Orion]([257]) 直接通过 RDMA 向客户端开放内存访问，进一步加速 PMEM 文件系统，类似的前作有 [Octopus]([258]) 。远端 PMEM 成为一个存储池，本地 PMEM 通过 [DAX]([259]) 访问。此外，这个 [PMEM guide]([260]) 对编程很有帮助。

  * [SplitFS]([261])。相比 Orion，SplitFS 将数据路径放在用户空间，将元数据放在内核并通过 Ext4-DAX 操作。数据路径借由绕过内核来加速，而内核仍然管理影响一致性和隔离的关键操作。在这类系统中，[Kuco]([262]) 引入了 Ulib、collaborative indexing、和two-level locking，以将更多细粒度操作卸载到用户空间。 [ZoFS]([263]) 使用 MMU 将文件系统与不同用户隔离开来，而每个用户都可以在用户空间（受 MPK 保护）中操作元数据/数据。

### 云原生（Cloud native）

  * [Snowflake]([43]) 是公有云上原生的 OLAP 数据库。内存缓存、查询处理、存储被解耦（disaggregated），重用公有云服务（例如 [AWS S3]([264])），并且可以独立扩展和计费。租户利用 VM（虚拟机）隔离，并将经典的资源利用不足问题卸载（offload）给公有云。为了避免每次都读取 AWS S3，Snowflake 添加了一个基于临时存储（ephemeral storage）的缓存层。节点可以预热（pre-warmed）以获得弹性（elastic）。 [Snowflake IPO]([265]) 非常成功。

  * [Service Mesh]([266]) 是一个容器化（containerized）的微服务（microservice）基础设施（infrastructure），其中 Sidecar 代理（例如 [Envoy]([267])）只需很少的代码变更，即可为应用程序添加流量路由（traffic routing）、服务注册（Service Registry）、负载平衡（Load Balancing）、断路器（Circuit Breaker）、健康检查、加密等功能。之前的 [Spring Cloud]([268])可以经过一些修改，迁移到 K8S 和 Service Mesh 环境。

  * [Dominant Resource Fairness]([269]) 是一种典型的 [Cloud Resource Scheduling]([270]) 算法，用于 [YARN]([271])。 DRF规范化（normalize）多维资源分配以保证支配资源（dominant resource）。此外，[2DFQ]([272]) 根据请求大小来将它们分配给线程，以确保公平性（fairness）； [Quasar]([273]) 通过机器学习在小型集群上采样工作负载的画像（profile），然后到整个集群运行； Container/[CGroup]([274]) 为每个用户任务执行配额（quota）/ 权重（weight），这个模式也被 [K8S scheduling]([275])使用； [Ceph QoS]([276]) 采用 d[mClock]([277])，它使用加权的预留资源的标签（reservation tags）。另外，[Leaky bucket]([278]) 是经典的节流算法； [Heracles]([279]) 为延迟敏感的作业与批处理隔离资源。一般来说，云引入了 [Multitenancy]([107]) 来描述一个由多个用户（租户）共享的系统，每个用户都分配了一组虚拟化、隔离、访问控制（access control）、优先级（priority）/ 配额的策略（policy）。对于成本估算，典型的方法是平滑窗口中的请求计数和大小，或者等待队列； [Cost Modeling]([280]) 在数据库查询优化器中提供了更多的 [comprehensive cost modeling methods]([281])； 示例可以在论文 [Access Path Selection]([72]) 和 [Optimal Column Layout]([71]) 中找到。

  * Facebook 中使用的 [Akkio]([282]) 跨地理区域数据中心（geo-regional datacenters）来迁移 u-shards，以保持访问局部性（access locality）。 U-shards（大小在 MBs 级别）代表了由 App 端知识决定的活跃访问的小数据集，远小于 Shards（大小在 GBs 级别），因此迁移成本更低。 [Taiji]([283]) 是另一个 Facebook 的系统，它基于 [SocialHash]([284]) 将用户负载均衡到数据中心，即好友群组可能会访问相似的内容。

### 二级索引（Secondary index）

  * [Helios]([159]) 构建全球规模的二级索引。更新被吸收到共享日志中，作为最终数据来源，然后以最终一致性异步地构建索引。 索引是自底向上逐级合并日志来构建的，并存储在兼容HDFS的数据湖中。 第三方查询引擎可以利用索引来排除不需要访问的块（pruning）。 [Hyperspace]([285]) 是数据湖上的另一个索引系统，用Spark任务建立； 它将细粒度的索引状态、元数据、数据、日志作为普通文件（with a spec）发布在数据湖上，以实现良好的互操作性。

  * [SLIK]([286]) 为 [RAMCloud]([287]) 构建全局二级索引。它对 B+树索引进行分区，后者表示为底层键值存储中的对象。 SLIK 通过在放宽（relaxed）索引一致性要求的情况下满足常见用例，来避免进行分布式事务的成本。

  * [HBase 二级索引]([288]) 比较全局索引和本地索引，在 [LSM-tree survey]([289]) 中有提到。全局索引只需要一次搜索，但在更新时会产生很高的一致性成本。本地索引 co-locates 于每个数据分区的节点，更新只需在本地维持一致性，但搜索需要查询所有分区。

### 内容分发网络（CDN）

  * [Facebook Owl]([290]) 运行一个去中心（decentralized）的点对点（P2P）数据层（如 BitTorrent），同时维护一个集中（centralized）的控制面（control plane）；每个区域运行有 Tracker，通过分片扩展。 P2P 架构能有效地横向扩展，在高流量增长下节约服务器资源。内容分发是逐块进行的，每个块沿着动态组成的临时（ephemeral）的分发树（distribution tree）传播。除了用于选择 Peer 和缓存的预设（preset）策略外，Owl使用仿真框架和 Random-restart Hill Climbing 算法来搜索最佳策略配置。CDN也可以看作是一种特殊的分布式缓存。

## 引用

// TODO insert

[477] Why ClickHouse is fast : https://clickhouse.tech/docs/en/faq/general/why-clickhouse-is-so-fast/

[478] ElasticSearch : https://en.wikipedia.org/wiki/Elasticsearch

(封面图片 by SBA73, CC BY-SA 2.0: https://99percentinvisible.org/episode/la-sagrada-familia/. 注：本文为个人观点总结，作者工作于微软)
