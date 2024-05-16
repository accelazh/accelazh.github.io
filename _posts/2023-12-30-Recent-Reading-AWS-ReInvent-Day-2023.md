---
layout: post
title: "Recent Reading AWS Re:Invent Day 2023"
tagline : "Recent Reading AWS Re:Invent Day 2023"
description: "Recent Reading AWS Re:Invent Day 2023"
category: "storage"
tags: [storage, paper, cloud]
---
{% include JB/setup %}

Picking my interested points.

```
1. AWS S3 Express One Zone
    0. Overview of AWS re:Invent 2023
        1. 芯片更大更强：服务器加速芯片Graviton4。AI推理训练芯片Trainum2。
        2. AI: Amazon Q - ChatGPT。 Bedrock大模型平台。更多产品，逐渐全栈。
        3. 云数据库：Aurora Limitless水平扩展，零RPO可用区切换，NVMe存储加速，Tiered缓存，Grover日志存储，Nitro芯片原子钟，Caspian热资源管理。
        4. 存储：S3 Express One Zone。Zero-ETL集成。

    1. What is S3 Express One Zone?
       https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-one-zone.html
        1. A new storage class.
           Request costs 50% lower than S3 standard.
           One AZ, 99.95 percent availability.
           Single digit ms level access. Million requests per second. 10x faster than S3 standard.
           Co-locate your data near your compute 
        2. My questions
            1. Looks like a CDN / Edge zone that puts data close to the consumer
    
    2. AWS re:Invent 2023 - [LAUNCH] Deep dive on Amazon S3 Express One Zone storage class (STG230)
       https://www.youtube.com/watch?v=TJp4ayDC8m0
        1. How does S3 express one zone achieve high performance?
            1. One zone architecture - co-locate storage with compute
                1. Durability model is different
                2. My questions
                    1. One zone should have lower availability to AWS S3's default 3-zone layout
            2. S3 directory buckets - enable high transaction workloads
                1. Dedicate to express on zone.
                2. Directory buckets scales by bucket rather than prefix, all at once, very quickly to high workload change
            3. Session-based access: faster authorization
                1. New S3:CreateSession
                2. Amortize auth latency over all requests
        2. Scenarios
            1. AWS Athena
            2. SageMaker, reduce GPU wait time for storage retrievals
    
    3. AWS re:Invent 2023 - What’s new with Amazon S3 (STG204)
       https://www.youtube.com/watch?v=idz2SvBHK-s
        1. AWS S3 Express One Zone
        2. Directory Buckets
            1. A new request scaling model
        3. Simplify access control - moving away from ACLs
            1. ACLs in S3 Inventory Reports
            2. Move to bucket policies and IAM policies
            3. S3 Access Grants
        4. Common Runtime (CRT) - Opensource SDK
            1. Automated multi-part uploads
            2. Parallelization of range GETs for downloads
            3. Built-in retry logic using multiple IPs
                1. 
                2. My questions
                    1. Multiple IPs, interesting
        5. Mountpoint for AWS S3
            1. Good. A trend that object storage and filesystem are being integrated
            2. Translate local filesystem API calls to REST API calls on S3 objects
                1. Relies on the CRT to achieve high single-instance transfer rate
                2. Designed for reliability, not POSIX compliance
            3. Also support S3 Express One Zone
            4. Automatic caching for Mountpoint for S3
                1. File read from S3, then retained on EC2 instance storage, EBS volumes, or memory
                2. First request at S3 latency, subsequent requests at local, sub-millisecond latency
                3. Training jobs up to 2x faster by retaining data for repeated requests on EC2 instance storage
            5. Mountpoint for S3 for containers
                1. Attach S3 as CSI driver to your EKS cluster 
                    CSI - Container Storage Interface
                    EKS - Elastic Kubernetes Service
            6. Object lock
    
    4. AWS re:Invent 2023 - Dive deep on Amazon S3 (STG314)
       https://www.youtube.com/watch?v=sYDJYqvNeXU
        1. S3 front end
            1. Spread requests across server IPs
        2. S3 index
            1. Prefix
        3. Storage
            1. 11 9s of durability
                1. End-to-end integratiy checking
                2. AZ loss
            2. Accidental delete, especially bulk operations
                1. S3 Versioning
                2. S3 Replication, copy data between buckets and regions
                3. S3 Object Lock
                4. Backups
                    1. Backup catalog
                    2. Restore engine
            3. Availability Zones
                1. My questions
                    1. Does AZ have extra cost? What if a customer doesn't want either AZ or the overhead?
            4. Defense
                1. Shadow mode
                2. Control plane limits

    5. AWS re:Invent 2023 - [LAUNCH] Achieving scale with Amazon Aurora Limitless Database (DAT344)
       https://www.youtube.com/watch?v=a9FfjuVJ9d8
        1. Aurora Limitless Database
            1. Sharding based scale out
                1. Challenges: Placement, Lookup, Consistency, Maintenance
            2. Sharded tables vs Reference tables
                1. Sharded, Collocated tables
                2. Reference - replicated to every shard
        2. Aurora Limitless Database Architecture - interesting
            1. Today: Writer instance -> multiple Reader instances
            2. Limitless introduced "shard group"
                1. Distributed transaction router
                    1. Scale vertically and horizontally based on load
                    2. Know schema and key range placement
                    3. Assign time for transaction snapshot and drive distributed commits
                    4. Perform initial planning of query and aggregate results from multi-shard queries
                2. Data access shards
                    1. Owning data shards
                    2. Scale vertically and split based on load
                    3. Perform local planning and execution of query fragments
                    4. execute local translation logic
                    5. Backed by Aurora distributed storage
                        1. Always 3-AZ durable
                3. Aurora distributed storage
            3. Hash-range partitioning
                1. Shard key is hashed to 64-bit. Ranges of 64-bit space are assigned to shards
                2. Shards own table fragments. Routers have table fragment references, but no data
                3. Table slicing
                    1. Table fragments are partitioned into sub-range slices
                    2. Not directly visible to user
                    3. Improve intra-shard parallelism
                    4. Relocate on horizontal scale out
                4. Horizontal scale out
                    1. Shard split due to utilization or storage size
                    2. Collocated table slices moved together
                    3. Leverages Aurora storage level cloning and replication
            4. Transaction consistency
                1. Goal: Maintain PostgreSQL transaction semantics
                    1. Read committed: See the latest committed data before your query begin
                    2. Repeatable read: See the latest committed data before your transaction begin
                    3. My questions
                        1. Not supporting Snapshot Isolation, nor Serializable?
                2. Transaction scope unknown until commit
                3. Bounded clocks
                    1. Based on EC2 TimeSync service: current time (approximate), earliest possible, latest possible, ms range
                        1. router gets time t100, then asks shard 619 to execute using snapshot@t100
                    2. One-phase & two-phase commit
                        1. 1PC, when only touching 1 shard
                            1. Acks commit when, write durable on disk, earliest possible > t100.
                                1. Commit Wait is in parallel with disk IO, so not adding much latency
                                    1. interesting
                                2. My questions
                                    1. So the algorithm is similar with Spanner commit wait
                        2. 2PC
                            1. Router assigns commit@120
                               Acks comment when, write durable on disk, earliest possible > t120
            5. Compatibility
                1. PostgreSQL wire compatible
                2. My questions
                    1. Aurora is built on PostgreSQL?

    6. AWS re:Invent 2023 - Deep dive into Amazon Aurora and its innovations (DAT408)
       https://www.youtube.com/watch?v=je6GCOZ22lI
        1. Aurora Global Database - Switchover
        2. Passing WAL rather than blocks, Writing less compared to PostgreSQL
            1. WAL archived to AWS S3
            2. Aurora storage doesn't do engine checkpoint
                1. continuous and parallel coalesce, recovery in seconds
            3. AWS RW passes logs to Aurora storage node, rather than passing pages
            4. Fast clone
        3. pgvector
            1. PostgreSQL opensource extension that supports storage, indexing, searching, metadata with choice of distance
                1. Storage: The vector data type
                2. Indexing: Supports IVFFLAT / HNSW indexing
                3. Searching: KNN, ANN
                4. Metadata: co-locate with embeddings
        4. Buffer pool resizing
            1. vs heap. 
            2. Dynamically resize based on demand
                1. A combination of LFU (least frequently used) and LRU algorithms
                2. When memory cool off, evict cold pages, shrink the memory, shrink the size
        5. Blue/Green deployments - MySQL/PostgreSQL
            1. Make a copy of your entire database and setup.
               Then upgrade on the new copy and bake.
               Catchup, sync, and switch over.
               Everything automated. Delete original is manual.
            2. Interesting
        6. Zero-ETL
            1. Integration with Aurora and Redshift
            2. Integration at the storage layer
                1. CDC streaming (enhanced binlog) to Redshift
        7. New Aurora Storage Type
            1. I/O-Optimized storage type
                1. Previous: 1*4K write vs 4*1K writes charge differently. Many IOs make the price unpredictable
        8. Optimized Reads
            1. Temporary objects
                1. PG spill over to disk on NVMe storage. Reserve 90% of the NVMe, 6x memory
            2. Tiered cache
                1. Temporary objects on NVMe storage, 4x memory.
                2. Random eviction
                    1. Fast, no maintaining LRU, but may wrong hit
                3. NVMe is slower than memory. But compared to without it, the avg latency of serving large database is greatly improved
                    1. 8x larger working set size, not having a real material latency change on latency 
            3. Working set size - Heat
                1. Even the workload is evenly random, heap to blocks won't be even, higher level index blocks are heater

    7. AWS re:Invent 2023 - Amazon Aurora HA and DR design patterns for global resilience (DAT324)
       https://www.youtube.com/watch?v=4NM9EB0IqEs
        1. Aurora Storage Deep Dive
            1. 3-AZ design
                1. DB instance at 1 AZ. Aurora volume across at 3 AZs. Volume max to 128TB.
                    1. AZ failure then DB instance can be provisioned at another AZ
            2. DB instances write to 6 copies
                1. 2 copies per AZ
                    1. Tolerate AZ+1 failure
                2. Writing full copy is expensive, so write WAL instead of pages
                    1. And, do coalescing
            3. Connection management
                1. More Apps, more connection
                2. Limit connection count. Reuse connections
            4. my questions
                1. Why Aurora is using its own storage rather than EBS? Aurora Volume. And log backup is sent to S3.
        2. Cross region
            1. backup
            2. managed RPO
            3. switchover

    8. AWS re:Invent 2023 - Building observability to increase resiliency (COP343)
       https://www.youtube.com/watch?v=MARiKxvrdmc
        1. Key points
            1. Separate health metrics into dimensions
            2. Combined multiple metrics to rule out false alarms
            3. Service map
            4. Alarm gray-failed instances
            5. CloudWatch
            6. Traffic spikes

    9. AWS re:Invent 2023 - Behind the scenes of Amazon EBS innovation and operational excellence (STG210)
       https://www.youtube.com/watch?v=1EWh2aDvHzY
        1. 3-AZ
        2. Minimizing blast radius as you scale
            1. Control plane is regional
            2. Data plane is per AZ
            3. Cells - interesting
                1. Physalia - Smaller than an AZ
                2. Small and simple to manage
                3. Cell can reside near clients
                4. Each cell is a 7-node Paxos cluster
        3. Nitro card for EBS
            1. NVMe controller
            2. NVMe to remote storage
            3. EBS optimized by default
        4. SRD: Multi-path through network - Interesting
            1. SRD - scalable reliable datagram
            2. Multi-pathing, retries in microseconds, runs on Nitro
            3. Get away tail latencies of TCP
            n. related materials
                
                1. SRD: A Cloud-Optimized Transport Protocol for Elastic and Scalable HPC    [2020, 39 refs]
                   https://assets.amazon.science/a6/34/41496f64421faafa1cbe301c007c/a-cloud-optimized-transport-protocol-for-elastic-and-scalable-hpc.pdf
                    1. Good. AWS EBS has chosen a different path, SRD+Nitro, compared to Azure Storage RoCEv2 RDMA.
                       Multi-path ECMP, low latency and jitter, no packet ordering, low queue congestion control, enabled by Nitro card.
                       SRD transport exposed interface resembles InfiniBand verbs.
                    2. Highlights
                        1. Why not RoCEv2?
                            1. RoCE, while a popular high-throughput, low-latency interconnect for HPC, was found to be unsuitable for AWS's scalability requirements. One of the key issues with RoCE is that it requires priority flow control (PFC), which is not feasible on large-scale networks due to the potential for head-of-the-line blocking, congestion spreading, and occasional deadlocks
                        2. Why not TCP?
                            1. TCP implementations are often constrained by the need to maintain high retransmission timeouts to account for operating system delays. This can lead to suboptimal performance, particularly under conditions of network congestion
                        3. What's good in SRD?
                            1. SRD is designed to utilize modern commodity datacenter networks, which have a large number of network paths, while overcoming their limitations, such as load imbalance and inconsistent latency when unrelated flows collide.
                            2. SRD does not preserve packet order, instead sending packets over as many network paths as possible and avoiding overloaded paths. This approach allows SRD to achieve close to optimal flow completion times with very low jitter, outperforming TCP in scenarios with high levels of network congestion.
                            3. AWS Nitro networking card
                                1. Low Latency and Jitter
                                2. Scalability - Multi-pathing
                                    1. Load balance across a large number of network paths
                                    2. ECMP Path Selection
                                    3. with-out waiting for network-wide routing updates convergence which takes 2–3 orders of magnitude longer
                                        1. My questions
                                            1. Switch level rerouting is slow
                                                1. this is why SRD does Nitro card level multi-pathing?
                                                2. And, switch level rerouting may not respond fast enough to load balancing overloaded path
                                3. Efficient Congestion Handling
                                    1. SRD sends packets over as many network paths as possible
                                    2. No packet order preserved - Out of Order Delivery
                                        1. The per-flow ordering or other kind of dependency tracking is done by the messaging layer above SRD; the messaging layer sequencing information is transferred with the packet to the other side, opaque to SRD.
                                        2. My questions
                                            1. Sorting the packets order need considerable memory and compute. Is it Nitro card doing it?
                                4. OS Bypass
                                    1. Nitro card's user-space driver 
                                5. SR-IOV enabled
                                6. HPC and ML optimized
                            4. Congestion Control
                                1. SRD employs a specialized congestion control algorithm that aims to keep queuing to a minimum, thereby decreasing the chance of packet drops and minimizing retransmit times.
                                    1. My questions
                                        1. Interesting. Incast problem can be solved by maintaining a minimum queuing.
                                           RoCEv2 DCQCN solves the incast problem in a similar way
                                            1. "DCQCN ... ensures low queue buildup, and low queue oscillations"
                                2. By controlling the aggregate queueing on all paths, SRD's congestion control mechanism helps to alleviate the incast congestion problem, which is common in many-to-one communication patterns in datacenters
                                3. The algorithm is similar with BBR, with additional datacenter multipath considerations
                            5. User interface: EFA
                                1. SRD transport on the Nitro card is exposed to AWS customers over EFA. EFA interface resembles InfiniBand verbs
                    3. My questions
                        1. Why not simply do RDMA?
                            1. I guess Nitro card is there so TCP can match with RoCE
                            2. Does Nitro card do DMA without CPU, just like RDMA NIC?
                    n. related materials
                        1. Pangu Networking: From Luna to Solar: The Evolutions of the Compute-to-Storage Networks in Alibaba Cloud
                            1. SOLAR multi-path transport, TCP multi-path transport
                        2. Jupiter Evolving: Transforming Google's Datacenter Network via Optical Circuit Switches and Software-Defined Networking
                            1. multi-path traffic routing is by WCMP algorithm

    10. AWS re:Invent 2023 - Deep dive into the AWS Nitro System (CMP306)
        https://www.youtube.com/watch?v=Cxie0FgLogg
        1. Silicon innovations at AWS
            1. Nitro system
                1. Hypervisor, Nitro cards, network, storage, SSD, and security
            2. Graviton
                1. Powerful and efficient compute
                2. AWS Graviton Processors
                   https://aws.amazon.com/ec2/graviton/
                    1. ARM processors
            3. Inferentia / Trainium
                1. Machine learning acceleration
                   one inference chip, one training chip
        2. Purposes
            1. Networking
                1. VPC networking
                2. Improve throughput
                3. Simplify hypervisor
                4. Reduce latency & jitter
            2. Hypervisor
                1. Bare-metal instances
                2. Nitro Hypervisor
                    1. Lightweight hypervisor
                    2. Memory and CPU allocation
                    3. Bare metal-like performance
            3. Security
                1. Transparent encryption
                2. Hardware root of trust
                3. No operator access
                4. Narrow & auditable APIs
                5. Features
                    1. Nitro Enclaves
                    2. NEFI Secure Boot
                    3. NitroTPM
            4. Storage
                1. NVMe controller
                2. Encryption support
                3. NVM to remote storage protocol
                4. Nitro SSDs
                    1. Integrated FTL into Nitro cards, 60% lower latencies, improved reliability, update for firmware
                        1. Good. But eventually SSD vendors supplied ZNS SSD. 
                    2. Traditional vendor FTLs have problems like GC kicked in at wrong time, requests stalled somehow
        3. Design
            1. Looks like a PCIe card
            2. ENA, EFA, SRD
                1. EFAv2 brings 200Gbps, 30% lower latency in Nitro cards
            3. Nitro Controller
                1. EC2 control plane => Nitro Controller (Auth, encryption)
                2. Nitro Controller => Nitro Hypervisor
                3. Nitro Controller => PCIe buses => Nitro Cards
                4. Nitro is nexus of the system, rather than CPU
            4. Graviton3 with Nitro System
            5. My questions
                1. Nitro is really a platform that many features developed in it
                2. It looks like CPU based function are in Nitro Controller, networking based functions are in Nitro cards

    11. AWS re:Invent 2023 - AWS Graviton: The best price performance for your AWS workloads (CMP334)
        https://www.youtube.com/watch?v=T_hMIjKtSr4
        1. Graviton3
            1. Up to 25% higher compute performance and 2x higher floating-point
            2. Supports DDR5 memory to provide 50% more memory bandwidth over DDR4 memory
            3. Consume 60% less power for the same performance compared to other CPUs
            4. Up to 3x higher perf for ML workloads, 2x vector wid and bfloat16 support, PyTorch and TensorFlow optimizations
        2. Graviton4
            1. Scale up
                1. Single socket 24xl (96 vCPUs)
                2. Support for coherent multi-socket
                3. 50% more cores-per-socket, 3x more cores, 3x more DRAM than Graviton3
        3. Design
            1. CPU microbenchmarks
               https://youtu.be/T_hMIjKtSr4?si=5lx8rWYDswXqQpgS&t=1225
                1. interesting
            2. Improvements guided by microbenchmarks
                1. L2 cache - 2x larger
                2. Front-end CPU
                    1. predict branch better
                3. Architecture
                    1. Adopted ARM V9, including SVE2
        4. Software ecosystem for Graviton
            1. Linux ones are mostly there
            2. Most AWS tools
            3. Databases
                1. SAP HANA Cloud with AWS Graviton
                2. AWS managed services on Graviton
            4. ARM64
                1. Software transition needed to run on ARM64, i.e, transitioning to Graviton
            5. Containers

    12. AWS re:Invent 2023 - Achieve high performance consistency using Amazon EBS (STG331)
        https://www.youtube.com/watch?v=nguQGNSJf3I
        1. Performance tips
            1. Align accessing size/address to filesystem block size

    13. AWS re:Invent 2023 - Smart savings: Amazon EC2 cost-optimization strategies (CMP211)
        https://www.youtube.com/watch?v=_AHPbxzIGV0
        1. How EC2 VMs save you customers money
        2. Automated recommendations
            1. AWS Trusted Advisor
            2. AWS Cost Management
            3. AWS Compute Optimizer

    14. AWS re:Invent 2023 - Implement proactive data protection using Amazon EBS snapshots (STG226)
        https://www.youtube.com/watch?v=d7C6XsUnmHc
        1. EBS Snapshots
            1. Point-in-time backups
            2. Incremental
            3. Crash consistent
                1. Can be take with 1 API call for a subset of volumes attached to an instance
        2. Data lifecycle Manager (DLM) support
            1. pre-script, post-script

    15. AWS re:Invent 2023 - What’s new with AWS file storage (STG219)
        https://www.youtube.com/watch?v=yXIeIKlTFV0
        1. Amazon FSx
            1. On-premises filesystems now moved to cloud and managed
            2. NetApp ONTAP
                1. SnapLock
                2. Multi-AZ filesystems
                3. Create, manage, backup FlexGroups
            3. Windows File Server
            4. FSx for Lustre
            5. FSx for OpenZFS
        2. Amazon EFS
            1. Serverless solution with full elasticity
            2. 3x Throughput, 3x IOPS
            3. Eliminates overprovisioning
                1. Pay as much as you use. Grow as you use.
            4. Move colder data to lower priced storage
                1. EFS lifecycle management
                2. Moved data from SSD standard storage class to EFS IA (infrequent-access) storage class
            5. Amazon EFS Archive
                1. archival storage class, up to 50% cost saving

    16. AWS re:Invent 2023 - AWS storage: The backbone for your data-driven business (STG227)
        https://www.youtube.com/watch?v=Alxig9GFIE4&t=1023s
        1. Very useful. The latency of each AWS storage
           https://youtu.be/Alxig9GFIE4?si=zdXGs0Td9DKYlT9i&t=1193
            1. ~100-200us - Instance storage
            2. ~500us-1ms - EBS io2
            3. ~1ms-2ms - EBS GP
            4. ~1ms-4ms - Amazon FSx for Lustre, FSx for OpenZFS
            5. ~2ms-5ms - Amazon EFS
            6. ~3ms-10ms - S3 Express Zone One
            7. ~10ms-200ms - S3 Standard, S3 Standard-infrequent access, S3 Glacier Instant Retrieval
            8. 1-5 minutes - S3 Glacier Flexible Retrivals expedited retrievals
            9. 3-5 hours - S3 Glacier Flexible Retrievals standard retrievals
            10. 12-48 hours - S3 Glacier Deep Archive

    17. AWS re:Invent 2023 - Network-attached storage in the cloud with Amazon FSx (STG209)
        https://www.youtube.com/watch?v=y442aGhtkxg
        1. customer usecases

2. AWS Local zones
   https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-availability-zones
   https://aws.amazon.com/about-aws/global-infrastructure/localzones/
    1. Local zone
        1. low latency, close to large population and industry centers.
    2. Wavelength Zones
        1. ultra low latency, to the edge of telecommunication carriers' 5G networks
    3. AWS Outposts
        1. fully managed AWS infra to customer premises
    4. Listing AWS available zones at each region
        1. The Complete Guide to AWS Regions & Availability Zones
           https://portworx.com/blog/aws-availability-zones/
            1. US East (N. Virginia)    us-east-1a, us-east-1b, us-east-1c, us-east-1d, us-east-1e, us-east-1f
            2. US East (Ohio)  us-east-2a, us-east-2b, us-east-2c
            3. US West (N. California)   us-west-1a, us-west-1b, us-west-1c
            4. US West (Oregon)    us-west-2a, us-west-2b, us-west-2c, us-west-2d
        2. https://www.aws-services.info/regions.html
        3. https://www.economize.cloud/resources/aws/regions-zones-map/
    5. Listing Azure available zones and regions
        1. https://cloudregions.io/azure/regions
    6. AWS failure outage history complete
        1. https://awsmaniac.com/aws-outages/
        2. Azure: https://azure.status.microsoft/en-us/status/history/
```
