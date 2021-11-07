---
layout: post
title: "FAST17 Paper Reading"
tagline : "FAST17 Paper Reading"
description: "FAST17 Paper Reading"
category: "storage"
tags: [storage, fast, paper]
---
{% include JB/setup %}

Raw paper reading notes for last year papers from major storage summits. Try to cover FAST17, MSST17, NSDI17, SOSP17/OSDI17, ASPLOS17， ATC17, ISCA17, HPCA17. Eventually most I picked are from FAST17. There are several from 2018 too.

Waiting 1 year before finish reading 2017 papers, so that I can tell which are favorable ones from reference count, as mentioned in paper selecting guide from [Build My Academic Paper Feedback Network](/storage/Build-My-Academic-Paper-Feedback-Network).

Look for "very good" > "good" > "interesting" as the levels that I recommend paper.

```
1. Clay Codes: Moulding MDS Codes to Yield an MSR Code
   https://www.usenix.org/conference/fast18/presentation/vajha
    1. Very good paper. Awesome work.
       "Clay codes extend the theoretical construction presented by Ye & Barg with practical considerations from a coupled-layer perspective that leads directly to implementation"
       Clay Code solved almost every drawback in regenerating code existing for years. "Clay codes provide the first practical implementation of an MSR code"
        1. Clay Code is MSR regenerating code. And it allows low storage overhead. This is not like Product-Matrix code which requires n > 2k-2
        2. It's array code, and the sub-packetization level, i.e. array size, is small enough
        3. It can regenerate multiple node failure with reduced traffic. This is hardpoint for regenerating code for many years
            1. the MSR property illustrated is for 1 node failure. multi-node it's "reduced traffic", bound given by appendix
        4. The Clay Code is based on RS code, actually pretty simple and easy transform
    2. how the code works
        1. the author only gives an example construct of (4,2) code. it's a bit lazy, because
            0. how could you write so little for such an awesome code construct that solved almost every problem in regenerating code? 
            1. there is no generalized code construct, e.g. how to assign the x, y, z correctly
            2. there is no illustration of how to regenerate multiple node failure with reduced traffic
                1. yes, there is, see appendix. and there is repair algorithm listed. this answers the general code construct and decoding method
            3. there is no math proof of the code property and the theory bounds
            4. In Table 1 it’s said Clay Code has polynomial sub-packetization level.
               But in the "(n = qt, k, d) (α = q^t ,β = q^(t−1))" given later in paper, α is exponential to n. It’s confusing.
        2. The baseline plain RS code. multiple packets abstracted as layers
           Then we add in the "Pairs" across layers. Encode "pairs" again with a simple inversible matrix
           For decode, we start from intersection score from 1 to biggest. using the pair PRT -> MDS Decode -> PFT to decode layer by layer.
            1. there is no general code construct except the very simple example (4,2) code. I've been gussing the general construct
                1. Coordinates x is 0~q-1, y is 0~t-1, z is (0~q-1, 0~q-1, .., 0~q-1) {t times}.
                    1. Yes, this is it. See appendix. They are there
                2. The "pair" follows same way described in paper. In each fixed y, z, ranging through all x, there is one and only one unpaired point
                3. the decode and selecting correct layers are complicated ..
                    1. In appendix, there is repair algorithm listed. now we have all we need.
        3. in the evaluation part
            1. the charts mostly shows "d=n-1". for regenerating code to reduce total IO count, this is not enough
            2. the (14,10,11~13) network traffic and disk-read charts compared to RS are not reaching theory numbers
    3. other highlights
        1. Sub-chunking through interleaving: pack the bytes in same position in code array together, to form the subchunk
            1. in implementation part, the calculation is performed in unit of sub-chunk, rather than directly every byte
        2. "Locally repairable codes such as the Windows Azure Code [15] and Xorbas [28] trade the MDS property to allow efficient node-repair by accessing a smaller number of helper nodes"
        3. "Clay codes possess all of the desirable properties mentioned above, and also offer several additional advantages compared to the Ye-Barg code"
        4. "Clay codes can be constructed using any scalar MDS code as building blocks"
        5. "The savings in repair bandwidth of the Clay code arises from the fact that parity-check constraints are judiciously spread across layers of the C data cube"
        6. to extend Clay Code for any (n,k,d) where not q divide n, the paper uses the imaginary data node whose data is all zero
            1. "The technique used is called shortening in the coding theory literature"
        7. "The helper nodes are to be chosen in such a way that if a y-section contains a failed node, then all the surviving nodes in that y-section must act as helper nodes"
           "If no such choice of helper nodes is available then it is not a repairable failure pattern"
    n. related materials
        1. [29] XORing Elephants: Novel Erasure Codes for Big Data [2013, 418 refs]
           http://www.vldb.org/pvldb/vol6/p325-sathiamoorthy.pdf
            1. facebook datacenter has employed (10,4) RS code.
               this paper is also by facebook. Locally Repairable Codes (LRCs) based on RS (10,4). t HDFS-Xorbas
                1. achievements: a 2x reduction in disk I/O and repair network traffic.
                   the disadvantage of the new code is that it requires 14% more storage
                   compared to RS code
                2. geo-distribution is key futhure direction to improving latency and reliability
                   RS code is be impractical due to high bandwidth requirements
                   local repairs make it possible
            2. "Locally Repairable Codes", share the same authors with this paper: Dimitris S. Papailiopoulos, Alexandros G. Dimakis
               https://arxiv.org/abs/1206.3804
            3. the code construct here
                1. "The basic idea of LRCs is very simple: we make repair efficient by adding additional local parities"
                    1. I'd say this is exactly the same with Azure LRC code ..
                2.  HDFS-Xorbas computes two extra parities for a total of 16 blocks per stripe (10 data blocks, 4 RS parities and 2 Local XOR parities)
                    1. Note that it's XOR.
            4. the new local parities are calculated by MapReduce and in a incremental manner.
                1. the code design makes new code rollout well adopted
        2. [35] Explicit Constructions of Optimal-Access MDS Codes With Nearly Optimal Sub-Packetization [2017, 34 refs]
           https://pdfs.semanticscholar.org/75d9/fedfa0c13b983e315ec2460da0c2e6d85775.pdf
            1. the "optimal access" property and the "group optimal access" property

2. Protocol-Aware Recovery for Consensus-Based Storage    [2018, 0 refs, FAST18 best paper]
   https://www.usenix.org/conference/fast18/presentation/alagappan
    1. good paper.
       discovered and analyzed the issue in paxos handling disk corruption; all industry paxos implementation have issues.
       the solution CTRL fixed all these issues, perforance ~90% of original, code lines 1500 change.
    2. highlights
        1. remarkable taxonomies
            1. the taxonomy of RSM recovery failure cases: failure scenarios * recovery approach = safety, availability, etc + data loss
            2. the storage fault model: fault outcome + possible causes
            3. the test cases for targeted corruptions, random block corruptions & errors, down/lagging nodes
        2. how CTRL works
            1. crash-corruption disentanglement.
                1. if crash, ok to delete logs and after, because they are not committed. if corruption, should not
                    1. because, committed logs should never be deleted. they are promises made to paxos leaders.
                       however most paxos implementations has this problem. e.g. log truncates, log rebuild, etc
                2. how to tell whether it's crash or corruption?
                    1. append a tail record p to log entry: t1:write(ei), t2:write(pi), t3:fsync()
                    2. if pi not present, it's ei crash.
                       if pi present: if pi+1 present, it's corrupt. if it's last log entry, ok to always treat as corrupt
            2. the safe log recovery protocol
                1. princiles
                    1. don't need leader must have complete logs (which hurts availability)
                    2. never delete corrupted logs
                    3. even we only have one copy of committed log, we will be able to recover
                2. if leader hits a corrupted log entry and need to fix, it asks each follower
                    1. if leader gets a "have" reponse, fix it
                    2. if leader gets "dontHave" responses from majority of followers, treat it as not committed, then discard the log entry and following
                        1. question: what if we removed paxos node previously, or added empty nodes?
                    3. if leader gets a "haveFaulty" responses, need to wait until one of previous cases to happen
            3. snapshot recovery
                1. each RSM node do snapshot at the same log index. the target log index is agreed through quorum
                2. after leader learns majority of quorum have done snapshot, issue gc logs through replication
                3. faulty node just copy snapshot from healthy node
        3. CTRL addes about 1500 lines of code in ZooKeeper or LogCabin.
            1. it's not big effort

3. LightNVM: The Linux Open-Channel SSD Subsystem    [2017, 22 refs]
   https://www.usenix.org/system/files/conference/fast17/fast17-bjorling.pdf
    1. OCSSD is gaining attention. Linux kernel is building support.
       LightNVM support different application-specific policies as "targets",
       and abstract different types vendor flash media with its designed interfaces.
       pblk "target" is a host-based FTL implementation.
       Also, the background introduction is very useful to understand flash media architecuture and characteristics.
    2. highlights
        1. Who needs Open-channel SSD?
            1. Host managed FTL, as FusionIO, Violin Memory, the in the similar approach of Open-channel SSD
            2. Tier 1 cloud providers, e.g. Baidu, use open-channel SSD
        2. LightKVM design
            1. built in kernel, operate by physical page address (PPA) IO interface
                1. channel -> parallel unit (PU) -> block -> plane -> page -> sector
                2. storage media characteristics can be passed as hint
                3. geometry management, like how many channels/PU/planes per each, etc
                4. vectored IOs, compared to single LBA+span IOs
            2. provide interface, where application-specific abstractions, donated as targets, can be implemented
                1. implemented a host-based FTL as a target, called pblk
                    1. write buffering, GC, write-leveling are implemented here
                    2. mapping table recovery: power-down flush copy + periodically snapshot + metadata at page out-of-bound area
        3. the background introduction to Open-channel SSD, NAND flash characteristics, write constraints are useful
            1. Media architecture
                1. a hierarchy of die, plane, block, and page, etc
                2. page is decomposed into fixed-size sectors with an additional out-of-bound (OOB) area
                   e.g., a 16KB page contains four sectors of 4KB plus an OOB frequently used for ECC and user-specific data
            2. Write Constraints
                1.  (i) a write command must always contain enough data to program one (or several) full flash page(s), 
                        1. thus we need the "Write Buffering", because we write in sector unit
                    (ii) writes must be sequential within a block, and
                    (iii) an erase must be performed before a page within a block can be (re)written
                2. The number of program/erase (PE) cycles is limited.
                   The limit depends on the type of flash: 10^2 for TLC/QLC flash, 10^3 for MLC, or 10^5 for SLC
                3. Failure Modes
                    1. Bit Errors. While error rates of 2 bits per KB were common for SLC, this rate has increased four to eight times for MLC
                    2. Read and Write Disturb
                    3. Data Retention. To persist over time, data must be rewritten multiple times
                    4. Write/Erase Error
                    5. Die Failure

4. Book: Designing Distributed Systems - Patterns and Paradigms for Scalable, Reliable Services by Brendan Burns
   https://azure.microsoft.com/mediahandler/files/resourcefiles/baf44271-3870-454f-868c-23d48e7672cb/Designing_Distributed_Systems.pdf
    1. good book to introduce container-oriented and micro-service design patterns, and around kubernetes
        1. however mostly are what I already know, and are navie wrapper of exsiting concept.
           original container-oriented design patterns are only a few of them in this book
        2. the book does intro a lot of typical opensource components to be used with the microservice and kubernetes
    2. highlights
        1. the Kubeless FaaS framework native for Kubernetes - What's the architecture?
           http://kubeless.io/docs/architecture/
        2. use resource version (similar to paxos epoach+=1 after new election), to avoid ownership lost-reobtain issues
            1. Shard-1 obtains ownership to become master.
            2. Shard-1 sends a request R1 as master at time T1.
            3. The network hiccups and delivery of R1 is delayed.
            4. Shard-1 fails TTL because of the network and loses lock to Shard-2.
            5. Shard-2 becomes master and sends a request R2 at time T2.
            6. Request R2 is received and processed.
            7. Shard-2 crashes and loses ownership back to Shard-1.
            8. Request R1 finally arrives, and Shard-1 is the current master, so it is accepted, but this is bad because R2 has already been processed.

5. Redundancy Does Not Imply Fault Tolerance: Analysis of Distributed Storage Reactions to Single Errors and Corruptions [2017, 9 refs]
   https://www.usenix.org/system/files/conference/fast17/fast17-ganesan.pdf
    1. the same authors from "Protocol-Aware Recovery for Consensus-Based Storage", former work of it.
       built testing framework CORDS, tested common opensource filesystems & DB & paxos, various bugs found
       generally the paper is interesting work. this is a new research track revealed from well-studied area.
    2. highlights
        1. zookeeper leader node partial crash: leader only quorum thread alive, follower still think leader is alive
        2. check the findings, there are many more practical bugs that those systems may hit
            1. all faults are by injecting single error to single node, but many cases result into cluster unavailable or data loss
            2. corruption and crash are different and cannot be recovered the same way.
               "Protocol-Aware Recovery for Consensus-Based Storage" focus on this
        3. underlying storage stack is unreliable, should employ end-to-end integrity strategies
    
6. Evolving Ext4 for Shingled Disks    [2017, 9 refs]
   https://www.usenix.org/system/files/conference/fast17/fast17-aghayev.pdf
    1. ext4-lazy mainly optimize the journaling of ext4 FS for DM-SMR disk, achieves 1.7-5.4x in metadata-light benchmark
       good as the introduction to DM-SMR internals: bands, guard regions, RMW, persistent cache, etc
    2. highlights
        1. besides SMR, Heat Assisted Magnetic Recording (HAMR) [29], and Bit-Patterned Magnetic Recording (BPMR) [2, 13] are in research
        2. ext4-lazy writes metadata only once in one location in journal, rather than ext4 twice
           so this becomes sequential write, and modification to ext4 codebase is minimal
            1. also, ext4-lazy migrate cold metadata back to its static location during cleaning, leaving only hot metadata in journal
        3. DM-SMR internals - the introduction part is good
            1. For purely sequential write workloads, DM-SMR disks perform at full throughput and do not suffer performance degradation
            2. Under random writes, DMSMR disks offer high throughput for a short period followed by a precipitous drop
        4. Ext4 uses jbd2 to do journaling, rather than itself.
            1. the introduction to EXT4 is also good to read.
        5. also, the evaluation part can be used as a reference of how to evaluate a new FS design

7. Application Crash Consistency and Performance with CCFS    [2017, 12 refs]
   https://www.usenix.org/system/files/conference/fast17/fast17_pillai.pdf
    1. share some same author with "Protocol-Aware Recovery for Consensus-Based Storage" too. this is the same research track
       ordering and crash consistency are widely required, by each application implements their own protocol, and they are error-prone
       to solve the problem, we introduce a new level of abstraction, stream. stream works like a multi-stream journaling.
        1. also, the shared distributed logging, CORFU and following work, may share the similar idea
    2. highlights
        1. the introduction to journaling of Ext4 is useful
        2. stream are not attached to files. may bind operations to two files in one stream, to implement ordering and crash consistency
           each application may use separated streams, so they have ordering in their own, but won't have ordering side-effect crosswise
        3. the work is mainly built on Ext4, to solve Ext4's optimized journaling techniques,
           Hybrid-granularity journaling and Delta journaling are introduced
        4. the journal technique adopted is from paper "Optimistic Crash Consistency", named SDJ - selective data journaling

8. HopsFS: Scaling Hierarchical File System Metadata Using NewSQL Databases  [2017, 15 refs]
   https://www.usenix.org/conference/fast17/technical-sessions/presentation/niazi
    1. very good paper, to show how to build distributed filesystem metadata on NewSQL database. the papaer illustrate how distributed filesystem metadata is built in detail.
       the gain is 37x capacity scalable, 16x throughput increase, zero down time in primary failover. HDFS client is compatible with HopFS.
       but HopFS needs more memory, and individual operation latency is higher.
       previously, distributed filesystem metadata is an industry hardpoint. Few are doing it e.g. CephFS. Now, the implementations come realized. The paper is by Spotify.
    2. highlights
        1. the target filesystem is HDFS. active/secondary namenodes are replaced to a set of in-memory namenodes with one leader.
           persistent metadata is stored in the MySQL database, NDB. NDB only supports read-commit transaction isolation
        2. distributed metadata management, keypoints
            1. modeling the filesystem metadata
                1. inode and related stat is modeld into tables, i.e. entity-relation model
            2. metadata partitioning
                1. this is a key design. inode of same direct directory parent are partitioned into same metadata server
                2. the NDB supports application-aware transactions
                3. partition pruned index scans, the transaction and table scan can be started at the server node who contains most of the data involved.
                4. so, generally, the hardpoint to filesystem metadata distribution is, how can we reduce the number of servers involved in each FS operation?
                    1. the partition strategy here helps.
                    2. but, another question, why we must do this? distributed shard opertions is not ok?
                        1. possibly to reduce the needs of distributed transaction
                5. hotspot handling: certain directories can be very hot
                    1. allow manually configured random partition for specific directories
            3. Inode Hint Cache
                1. in a FS path, except the last component is what we need to operate on, all previous components only need to read.
                   we use a cache to quickly retrieve them, in parallel and batched, and only needs primary key lookup.
            4. transaction implementation
                1. concurency control
                    1. HopFS uses pessimistic concurrency, i.e. lock execute update, rather than MVCC.
                       this is because NDB supports only read-commit, and also row locks
                    2. locks are acquired using total order, to avoid deadlock
                       read is all done at beginning, lock is aquired with strongest lock needed, no later lock upgrade
                    3. HopFS uses hierarchical locking, i.e. if parent locked, all decendent directories/files are locked too
                2. in a file path, the parent components are retrieved from inode hint cache, in batch, without locking
                3. transaction writes are in per-transaction cache first, if done, transmitted to NDB to commit
                   because NDB supports read-commit isolation, this works like copy-on-write to ensure transaction isolation
                    1. question
                        1. I didn't find description about transaction journaling. possibly this is included in NDB,
                           but not need to be handled in HopFS
                4. the transaction pseudo-code. very good to see the overall transaction implementation. coped here.
                    \`\`\`
                        1. Get hints from the inodes hint cache
                        2. Set partition key hint for the transaction
                    BEGIN TRANSACTION
                    LOCK PHASE:
                        3. Using the inode hints, batch read all inodes
                           up to the penultimate inode in the path
                        4. If (cache miss || invalid path component) then
                              recursively resolve the path & update the cache
                        5. Lock and read the last inode
                        6. Read Lease, Quota, Blocks, Replica, URB, PRB, RUC,
                             CR, ER, Inv using partition pruned index scans
                    EXECUTE PHASE:
                        7. Process the data stored in the transaction cache
                    UPDATE PHASE:
                        8. Transfer the changes to database in batches
                    COMMIT/ABORT TRANSACTION
                    \`\`\`
                5. another thing is, because the distributed transaction is for filesystem metadata operation.
                   it's not a general distributed transaction need to be implemented. so there can be many
                   special optimizations or simplifications dedicated for filesystem metadata distributed transaction.
            5. Subtree operation transactions
                1. this is to handle large filesystem operations, e.g. mv, rm, set quota, chmod, chown
                2. a big subtree operation can be divided and executed in different times,
                   the internal state, organized as a tree in memory in namenode, is serialized in NDB too
                    1. the subtree transaction protocol ensures below invariants to ensure correctness
                        1. no new operations access the subtree until the operation completes
                        2. the subtree is quiesced before the subtree operation starts
                        3. no orphaned inodes or inconsistencies arise if failures occur
                3. the subtree transaction and normal FS operation transaction voluntary abort if see locked
        3. about evaluation
            1. it's not using production data, but synthetic workload from operaiton statistics of production workload
            2. "In our experiments we have observed 8 to 10 seconds of downtime during failover in HDFS", HopFS has zero down time
            3. about NDB
                1. it should be in each group 1-primary n-slave of MySQL servers, and then with a partition + distributed transaction layer
                   that's the typical distributed MySQL solution.
                2.  If all the NDB datanodes in a node group fail, then the HopsFS namenodes shutdown
        4. about "related works"
            1. useful as a solution overview of what industry/academy have for distributed filesystem metadata solution
            2. why missed compare with CephFS?
            3. IndexFS [52] uses a caching mechanism to improve the performance of hot directories/files,
               while HopsFS’ currently only load balances a user-configurable number of top-level directories
        5. Admins usually have tool to analyze HDFS namespace, by ad-hoc or external dump
            1. HopFS enables online ad-hoc analytics on the metadata. Anyway they are in MySQL NDB which supports SQL
            2. also, an eventually consistent replication protocol to replicate HopFS metadata to Elasticsearch for free-text search

9. Algorithms and Data Structures for Efficient Free Space Reclamation in WAFL    [2017, 8 refs, FAST17 best paper]
   https://www.usenix.org/system/files/conference/fast17/fast17-kesavan.pdf
    1. interesting paper. To handle the random free issue while providing continuous high throughput,
       WAFL delay deleting in batched logs, and try to break big deleting into multiple CPs.
       the freeing involves walking through bigmap chains, and interleaves with all WAFL features such as snapshot
    n. related materials
        1. High Performance Metadata Integrity Protection in the WAFL Copy-on-Write File System  [2017, 8 refs]
           https://www.usenix.org/system/files/conference/fast17/fast17-kumar.pdf
            1. interesting paper to read. three methods are used to verify memory metadata integration
                1) Block checksum. To reduce the computation overhead, Adler32Incr only calculates changed byte at each incremental change, and processors in parallel
                2) Transaction auditing by invarients, listed at Table 1. invarients calculation is digest-based and also borrows incremental checksum to reduce overhead.
                3) CPU-assisted Page Protection. keep pages read-only, unless disable protection globally when modifying them. Only enabled in diagnostic mode, due to 30% performance impact
            2. highlights
                1. memory scribbles can be caused by software bug, or hardware failures.
                    1. a scribble overwrites an arbitrary data element
                        1. also, scribble can be introduced by external attacks in a controlled way on a shared infrastructure [38, 48]
                    2. even scribble happen, data written shouldn't be impacted
                        1. by end-to-end block checksum, transaction auditing, etc
                        2. reboot ONTAP node on verification failure, instead of aborting individual transaction.
                           this protects potential memory scribble hurting other unknown data
                    3. telling whether the scribble is caused by software bug or random hardware failure saves engineering efforts
                        1. by enabling page protection.
                        2. also, other checksums/auditing, core dump, help narrow down the trace
                2. WAFL has a built-in command-line tool that injects corruptions into in-memory data structures

10. PebblesDB: Building Key-Value Stores using Fragmented Log-Structured Merge Trees    [2017, 0 refs]
    http://www.cs.utexas.edu/~vijay/papers/sosp17-pebblesdb.pdf
    1. Fragmented Log-Structured Merged Tree (FLSM) delays sstable merge, but add extra indexes, i.e. guards, borrowed from skip list, to mitigate read penalty.
       Write amplification is reduced, because of delayed sstable merged, thus improve write throughput. but range query is slower due to sstable now are not fully sorted
    2. highlights
        1. LSM-tree write amplification is a big problem. most approaches try improve concurrency, or do less merge, or move big values out from key-value pairs.
           indutry mature RocksDB has done a lot in improving LSM-tree on SSD and mitigate write-amplification.
           This paper does proposed new light on improving the LSM-tree data structure, and the results are even better than RocksDB which is highly optimized.
    3. questions
        1. if the paper wants to demonstrate FLSM, why need to build PebblesDB and mix into unrelated optimizations, to hinder the evaluation results?

11. Azure Data Lake Store: A Hyperscale Distributed File Service for Big Data Analytics [2017, 6 refs]
    http://www.cs.ucf.edu/~kienhua/classes/COP5711/Papers/MSazure2017.pdf
    1. general paper to introduce Azure Data Lake. There is no detail implementation, but covered full concepts in Azure data lake.
    2. highlights
        1. Previous Cosmos will be substitued by Azure Data Lake, we are using Scope Language there
        2. Azure Data Lake can hook in all types of storage provider, can support all sort of big data workloads, and paid special attention to security, and includes many micro-services
        3. RSL-HK (MS RSL lib paxos + in-memory SQL Hekaton Engine), is used to store the metadata, including file/directory naming hierarchy
            1. still, it's the single primary + multiple secondary architecture, so I think the primary server limits throughput scale

12. Memory-Driven Computing
    https://www.usenix.org/conference/fast17/technical-sessions/presentation/keeton
    0. good summary, especially the technology challenge part
    1. technology trends
        1. storage media Memory + storage hierarchy technologies
        2. Non-Volatile Memory (NVM)
        3. Interconnect advances, Photonic interconnects
        4. Gen-Z: open systems interconnect standard
        5. Heterogeneous compute, Task-specific accelerators augment CPU compute
    2. how it affects Applications
        1. etc
    3. Memory-Driven Computing challenges for the FAST community
        1. Traditional storage services
            1. Issue: keeping persistently stored data safe in fabric-attached NVM
            2. Revisit traditional storage services: redundancy, encryption, compression, deduplication
            3. New challenges:
                1. Need to operate at memory speeds, not storage speeds
                2. Space-efficient redundancy for NVM
                3. Traditional solutions (e.g., encryption, compression) complicate direct access
                4. Providing performant access to encrypted data
            4. Memory-side hardware acceleration
                1. Memory speeds may demand acceleration (e.g., DMA-style data movement, memset, encryption, compression)
                2. What memory-side acceleration functions strike good balance between application performance and generality?
        2. Traditional data access
            1. Performant file systems for fabric-attached NVM
                1. Applications favor familiar file API, but traditional implementations are inefficient and don’t handle disaggregation
                2. How to extend NVM file system work to support Memory-Driven Computing environment?
            2. Memory access control
                1. As access granularity gets smaller, access control enforcement needs to adjust
                2. What approaches (e.g., capabilities) provide fine-grained access control and protection for Memory-Driven Computing environment?
        3. Heterogeneity and tiering
            1. Managing multi-tiered memory/storage systems
                1. Load/store memory isn’t most cost-effective medium for cold data
                2. How to manage multi-tiered hierarchy, to ensure data is in “right” tier for performant access, long-term storage, etc.?
                3. What opportunities does Memory-Driven Computing provide for multi-site storage?
            2. Heterogeneous memory
                1. DRAM stores ephemeral data, NVM stores persistent data: different access patterns
                2. How to manage allocation, reclamation, naming, etc. for different memory technologies?
            3. Leveraging local memory
                1. Memory-Driven Computing includes both local and fabric-attached memory
                2. How should local memory be managed – system-managed inclusive cache? scratchpad? application-managed?
        4. Coping with failures
            1. Ensuring crash consistency in face of failures
                1. Crash consistency methods can degrade application performance
                2. What are strategies for performant persistence and crash consistency?
            2. New memory fabric error models
                1. Memory fabric errors may lead to load/store failures, which may be visible only after the originating instruction
                2. How to provide reasonable reporting and selective handling of memory errors?
        5. Programming models
            1. System organization: remote memory vs. disaggregated memory
                1. Memory disaggregation provides many benefits, but departs from popular scale-out programming model
                2. Should non-local memory be treated as disaggregated (unmediated) resource or remote (mediated) resource?
            2. Memory-driven coordination
                1. Shared persistent memory can provide global view of shared state that enables coordination
                2. What are “memory-driven” approaches for concurrency control, consensus, failure detection, etc.?
        6. Characterization opportunities
            1. Characterization of new NVM and interconnect technologies
                1. New technologies present new performance, endurance, and management opportunities and challenges
                2. How do these new technologies behave under expected typical usage patterns?
            2. Implications of “wider” API for persistent data
                1. “Narrow” storage APIs require explicit action for persistence, but “wider” memory APIs allow stores to persist data
                2. Does widening of API for persisting data lead to more errors or more data corruption?

13. On the Performance Variation in Modern Storage Stacks    [2017, 4 refs]
    https://www.usenix.org/conference/fast17/technical-sessions/presentation/cao
    1. interesting work, the first paper to show performance variations for Ext4/XFS/Btrfs * HDD/SSD on different configurations
       the configuration space is selected by domain expertise and Latin Hypercube Sampling 
        1. the slides have more charts than paper
        2. the study is on local storage only, people are looking for distributed systems
        3. aging is not included in current study, may in future work
    2. highlights
        1. SSD setup is stable according all configs
        2. EXT4 is more performance variating. see papaer for which config changes which, and how to reduce variation
            1. block allocation is a major cause of performance variation in Ext4-HDD configurations
        3. temporal variation

14. Graphene: Fine-Grained IO Management for Graph Computing    [2017, 11 refs]
    https://www.usenix.org/conference/fast17/technical-sessions/presentation/liu
    1. graph computing challenge 1: access vertex issues random IO. linux pluglist IO scheduling is inefficient.
        Use vertex <-> bitmap <-> find & join consecutive IOs.
       challenge 2: partition with balanced #edges
        row cut first, then column cut, to get the 2D partition.
       anyway, the evaluation results are very good. perf improve 3x-20x to state-of-art; IO util improve by 50%.
        1. the slides are illustrative. the questions asked at end of audio recording are interesting
        2. in recent years there are a series of graph computing frameworks. they accumulated a lot of optimization methods
    2. highlights
        1. four types of existing graph processing systems:
            (1) vertex-centric programming model, e.g., Pregel [36], GraphLab [35], PowerGraph [20], and Ligra [47];
            (2) edge-centric, e.g., Xstream [44] and Chaos [43];
            (3) embedding-centric, e.g., Arabesque [50]; and
            (4) domain-specific language, e.g., Galois [40], Green-Marl [27] and Trinity [46]
            1. In Graphene, IO request centric processing. The IOIterator
        2. Direct hugepage support (DHP)
            1. preallocates hugepages at boot time, to store and manage graph data and metadata structures, e.g., IO buffer and Bitmap
            2. motivated by our observation of high TLB misses, as the number of memory pages continues to grow for large-scale graph processing
            3. We choose this approach over transparent hugepage (THP) in Linux [39] for a couple of reasons
                1. THP introduces undesirable uncertainty at runtime, because such a hugepage could be swapped out from memory [42]
                2. THP does not always guarantee successful allocation and may incur high CPU overhead
            4. As a first attempt, we have investigated the use of page coloring [16, 60] to resolve cache contention
                1. that is, to avoid multiple vertices being mapped to the same cache line
                2. achieve around 5% improvement across various graphs.
                   However, this approach becomes incompatible when we use 2MB hugepages for metadata
        3. In Graphene, we choose to use a small IO size of 512 bytes as the basic block for graph data IOs
        4. Balancing IO and Processing
            1. Graphene pins IO and computing threads to the CPU socket that is close to the SSD they are working on
            2. Graphene utilizes a work stealing technique to mitigate computational imbalance issue
        5. The experiments show that Graphene is able to perform comparably against in-memory processing systems on large-scale graphs,
           and also runs several times faster than existing external memory processing systems

15. vCorfu: A Cloud-Scale Object Store on a Shared Log    [2017, 3 refs]
    https://www.usenix.org/conference/nsdi17/technical-sessions/presentation/wei-michael
    1. continous effort from distributed shared log, i.e. CORFU. the project is getting interesting. good work to read.
       the object is built from stream materialization, and each can be a small replicated state machine to compose a large one
        1. comparing to typical replicate state machine, vCorfu did a "scalable paxos"
            1. shared the logs, so overall throughput are scalable rather than limitted by primary paxos node
            2. rather than each replica to rebuild entire replicated states in memory, they can build smaller ones, only for for their interested objects
                1. to benefit reads, but with write panelty, stream materialization is employed
            3. the didicate sequencer node is used as central consensus of which append goes to which shard
               there is no HA, but consensus fast-recovery is by vertical paxos, the reconfiguration mechanism
        2. the paper compares itself to Tango [10] a lot
    2. highlights
        1. stream materialization.
            1. client interact with objects, rather than logs. log entries specific to the object are copied out and put into "stream"
               the approach is borrowed from Tango [10]
                1. client can read materialized stream from one replica
            2. panelty at writes. client must commit data to every log and stream replica
            3. the system leverage logs to provide support for transactions
            4. object writing is supported by java language on vCorfu, to simplify many things
        2.Composable SMR: very large replicate state machine, with client to replicate entire state machine
            1. state machine can be composable by many smaller state machine
            2. to reduce playback burden, divide big objects into smaller ones, and connect them by pointer
        3. challenges
            1. the log tail must be consistent shared knowledge to all clients.
                1. using the address by sequencer. CORFU has more detail
                    1. CORFU uses a dedicated sequencer node.
                    2. For fast recovery from sequencer failure, we store the identity of the current sequencer in the projection
                       and use reconfiguration to change sequencers. The counter of the new sequencer is determined using the highest page written on each flash unit,
                       which is returned by the flash unit in response to the seal command during reconfiguration
                    3. reconfiguration mechanism (patterned after Vertical Paxos [17]) 
                       apable of restoring availability within tens of milliseconds on drive failures
        4. performance vCorfu vs Cassandra YCSB
            1. ~30% - 50% improvement to Cassandra.
        5. lightweight transaction resolution
            1. vCorfu leverages atomic multi-stream appends, and global snapshots provided by the log
                1. question: how is atomic multi-stream appends done?
            2. sequencer checks whether read set is modified before issuing a token for commit
               so that, transaction to be aborted will never be written into logs.
               the saves overhead and simplify things

16. Black-box Concurrent Data Structures for NUMA Architectures    [2017, 5 refs,  ASPLOS17 Best Paper]
    https://cs.brown.edu/~irina/papers/asplos2017-final.pdf
    https://cs.brown.edu/~irina/slides/asplos2017_slides.pdf
    1. Very good innovation. Node Replication (NR) replicates a sequential data structure to each of the NUMA node;
       inter-node, use a shared log to sync states; intra-node, use flat-combining as synchronization pattern.
       It's black-box for the sequential data structure to becomre NUMA-aware. The performnace results are pretty good.
        1. the idea is borrowed from [6] CORFU
        2. evaluation
            1. skiplist priority queue
                1. NR performs better than lock-free only for high contention (> 30 threads) - 1.7x
                   NR performs much better for basically all other concurrency algorithms - 6x
            2. Redis - 2.6x compared to others, not including lock-free
            3. is the compare fair ..
               "NR has many low-level optimizations specific to each architecture and related to the details of the cache coherency protocol"
        3. limitations
            1. n replica * memory overhead + shared log memory overhead
            2. NR is blocking. non-responsive replica can stall all. non-blocking version is under research.
            3. compared to lock-free, more suitable for high contention case
        4. others
            1. overall 1500 lines of code
            2. also implemented a multi-threaded verison of windows port of Redis
            3. Lock-free data structures are considered state-of-the-art, but they were designed for UMA.
               Creating new lock-free algorithms for NUMA is a herculean effort
    2. highlights
        1. the related works are very comprehensive
           good to read to graspe current NUMA concurrent data structure solution
        2. flat combining [30]
            1. selects a leader thread, called the combiner, to batch all updates. other threads are reads
               the leader is short-lived, abdicates after finishes outstanding updates, up to a maximum number
                1. the user thread posts its operation in a reserved slot, then tries to become the combiner by acquiring the combiner lock
                   the combiner reads the slots, marks filled slots (batch size B), and then proceeds to update shared log with B entries
            2. ref: Flat combining and the synchronization-parallelism tradeoff [2010, 229 refs]
               https://people.csail.mit.edu/shanir/publications/Flat%20Combining%20SPAA%2010.pdf
            3. for NR, the leader threads help batches updates to be published to shared log
        3. NR algorithm
            1. linearizability. read always reads fresh data.
               but no guarantee for data can updated after read completes. i.e. cross operation locking
            2. combiner thread and reader thread use rwlock to coordinate
            3. combiner thread uses CAS to append shared log
            4. the shared log is a circular buffer
            5. NR also has many low-leveloptimizations specific to each architecture. see paper for detail.
            6. multi-thread, thread-local, fast memory allocator is necessary

17. The Logic of Physical Garbage Collection in Deduplicating Storage    [2017, 6 refs]
    https://www.usenix.org/conference/fast17/technical-sessions/presentation/douglis
    https://www.usenix.org/sites/default/files/conference/protected-files/fast17_slides_duggal.pdf
    1. the GC improvements in Data Domain Filesystem (DDFS).
       PGC is introduced because LGC performs bad in high Total Compression workload, and high file count workload.
       PGC+ is yet another improvement on PGC. PGC improves 10-60% execution time.
       Generally, DDFS GC uses mark-and-sweep approach rather than refrence counting.
        1. to summarized, PGC+ use PHV to replace bloom filter to reduce memory consumption so that to run GC faster
           and added various optimizations to improve parallel and memory lookup to compensate PH overhead
           compared to LGC, PGC scans on-disk containers, rather than files,
               so mitigated slowness on the large file count workload, high TC rate workload
               also, PGC turned large numbers of random IOs to a set of sequential scans
        2. eventually, the LGC to PGC/+ evolve is due to user workload change in recent years
    2. highlights
        1. why Logical GC is slow. LGC scans live files
            1. recent workload has increasing file count. LGC scans all live files, so slow
            2. some system workload has high TC. LGC repeated mark the same live chunk. so slow.
            3. the "Technology Trends and Enumeration" section has more detailed illustration for how user behavior changed
        2. the filesystem namespace. for each file, it's a Merkle Tree, each layer is a hash to covering chunks.
           the file/tree can be fastcopy-ed, thus creating the forest.
        3. LGC
            1. use bloom filter to track fingerprints of live files.
               GC to remove "most" but not necessarily all "all" dead blocks
                1. each GC run may use different hash functions, so likely "all" dead chunks will be detected
            2. which instance of a duplicated fingerprint to preserve? keep the most recently written one
            3. which container to claim? which has less live fingerprints than threshold
            4. to reduce bloom filter memory, scan by setting a sampling rate
        4. PGC differs from LGC
            1. perfect-hasing. it doesn't have false positive like bloom filter, and needs less memory
                1. quesiton: how is it constructed?
                2. PGC has an extra Analysis step, to analze fingerprints in the on-disk index, to construct the perfect-hasing
                    1. less than 4 bit per Lp fingerprint
            2. scans containers to walk through each layer of Lp
            3. also, level-by-level checksum is verified to find corruption
        5. PGC+ improves from PGC
            1. the key idea is to reduce memory consumption, so PGC/FGC don't need to run focus cleaning due to limited memory
                1. replace remaining bloom filters to PHV
                2. parallelization, memory lookup, etc optimizations to improve PHV performance
                3. dynamic duplicate estimation. which removed the Live Instance Vector to reduce 2x memory
                    1. like LGC/PGC, estimate the liveness of container in select phase, to focus cleaning those most space can be reclaimed with least effort
                    2. for PGC+, there is no Pre-Filter step
                    3. During the Select phase, we walk the container set in reverse, from the end to the beginning, to find the latest copy of any duplicate chunk
                       a Dead Vector of bloom filter, with small cost of memory, to help count container liveness
                        1. anyway, Live Instance Vector is saved from memory
                    4. dynamic duplicate removal
                        1. the copy forward happens in reverse order. Each time a live chunk is copied forward, subsequent chunks with the same fingerprint are treated as duplicates 
                            1. hence, Live Instance Vector is saved from memory. 
                               This reduces memory requirements by 2×
            6. online GC
                1. customer may write a new chunk which is a duplicated to a dead chunk. the dead chunk is resurrected.
                2. added a process to inform GC of incoming chunks
                3. also has control to limit resource usage by GC, configurable. called throttling

18. I Can’t Believe It’s Not Causal! Scalable Causal Consistency with No Slowdown Cascades  [2017, 6 refs]
    https://www.usenix.org/system/files/conference/nsdi17/nsdi17-mehdi.pdf
    1. interesting paper as it coined the first snapshot transaction implementation based on casual consistency.
        1. the read & verification design is good.
        2. but the write still needs to lock every object.
           and dead lock holder introduces another stall problem besides slow cascades.
    2. highlights
        1. slowdown cascades
            1. when propagate writes, the replica needs to receive them in order.
               if one of the writes is pending on a replica, the following writes are stuck
                1. question: is this a real case? why need to write that way?
                             even example as twitter feeds & comments.
        2. shift the casual consistency responsible to client
            1. server replica still propagate writes as the original
            2. each shard carries it's shard timestamp/write-version, i.e. shardstamp
               each client carries causal timestamp = [shardstamp1, shardstamp2, shardstamp3, ..]
            3. client cannot read a slave shard, if the shard has lower shardstamp than it from client's casual timestamp
               client either wait retry, or goes to master shard, or use a mixed strategy
        3. compression of causal timestamp
            1. we have N shards, each has master-shard, several slave-shard. slave shards may span multiple datacenters
            2. we want to compress the causal timestamp to n slots << N
            3. observation: the top n-1 shards most frequently modified affects most
               so, n-1 slots + 1 slots. the first n-1 tracks the most frequenty modified shards' shardstamp individually
                   the last 1 slot merges all remaining shards' shardstamp
        4. snapshot isolation transaction based on casual consistency
           the transaction commit doesn't need to be synchronized. (but you lock)
            1. read & verify:
                1. read all objects involved,
                2. verify pairwise consistent of reads, verify pairwise consistent of reads vs writes
                    1. pairwise consistent: obj i is at least as updated as obj j, in causal timestamp, and vice-visa
                3. else, read again
            2. prepare write causal timestamp
                1. the new causal timestamp is the max(read, write) for every shardstamp slot
                   i.e. to make all writes pairwise dependent
                    1. if another client reads one of the writes, to be read with valid timestamp,
                       it needs to read all other writes in the transaction too
                    2. so that, the transaction results are atomic visible
                       even though it's not atomic written
            3. lock every object to be written
                1. yes. it still needs a lock, an needs to lock up every object to be written.
                   this destorys the elegance of this causal consistency transaction protocol,
                   and even the plain MVCC which is based on strong consistency doesn't need such lock
                2. the lock should be to prevent multiple interleaved writes from different transaction
                3. death of lock holder will stall other transactions
                    1. so, what's the purpose of solving Slow Cascades issues, while introduce another stall problem

19. FlashBlox: Achieving Both Performance Isolation and Uniform Lifetime for Virtualized SSDs  [2017, 9 refs]
    https://www.usenix.org/system/files/conference/fast17/fast17_huang.pdf
    1. SSD virtualization is an interesting approach.
       This paper pin app workload to channel/die to provide different levels of isolation.
       periodic inter-channel swap and block-mapping migration are used to balance the different wear-out level from different app workloads.
    2. highlights
        1. SSD virtualization - interesting as this paper thinks from hardware perspective
            1. by pin app workload to dedicated channels, or dedicated dies
                1. question: if other channels are idle, can the app temporarily expand out of its pined to use others?
                             I think that's the fundamental weakness of this approach. software virtualization may do better.
                             however, strong quota/throttling/limit enforcement, may favor the hardware pin approach
            2. the design is based on Open-channel SSD.
               Open-channel SSD are getting popularity these years.
            2. to balance wear-leveling across different app workloads pinned
                1. intra-channel wear-leveling: use the pre-existing SSD wear-leveling mechanisms
                2. inter-channel wear-leveling
                    1. on periodic basis, swap one of the max wear pinned channel with another app
                    2. how to migrate the data within a channel?
                        1. use an erase-block granular mapping table, to gradually switch block-by-block
                        2. may further, since the migration creates block replica, to perform reads on other replica
        2. evaulation
            1. FlashBox has up to 6% higher total system CPU usage, compared to stock open-channel ssd.
            2. figure 11, the big performance fall in MapReduce. there are explanations, they are expected
        3. related works
            1. Open Architecture SSDs. Recent research has proposed exposing flash parallelism directly to the host [38, 49, 61, 76].
            2. SSD Interface .. Multi-streamed SSDs [33] addresses a similar problem with a stream tag

20. readings: MSST 2017 papers/speaks
    1. Parallel I/O at NERSC: Today and Tomorrow
       https://www.youtube.com/watch?v=E-U2anogvhw&feature=youtu.be
       http://storageconference.us/2017/Presentations/Lockwood.pdf
    2. Tiered Erasure - When Flat Doesn't Fit
       http://storageconference.us/2017/Presentations/Bonnie-2.pdf
       https://youtu.be/Mkk82tEYwu4
        1. “Multi-Component Repositories” in MarFS speak
    3. MarFS: A Scalable Near-POSIX File System over Cloud Objects Erasure
       https://www.snia.org/sites/default/files/DSI/2016/presentations/filesys/GaryGrider_MarFS_Scalable_File_Systems-rev.pdf
        1. interesting. people should have already been exploring this approach
        2. highlights
            1. doesn't allow update file in place for object data
            2. metadata scaling. one node holds all directory metadata in one project. other nodes holds file metadta in the project
            3. spread very large file across many objects
            4. packing many small files into one large object
    4. Persistent Memory Programming: The Current State of the Ecosystem
       http://storageconference.us/2017/Presentations/Rudoff.pdf
       https://www.youtube.com/watch?v=hz1nO7zEOYU&feature=youtu.be
        1. Intel
    5. NOVA: A High-Performance, Hardened File System for Non-Volatile Main Memories
       http://storageconference.us/2017/Presentations/Swanson.pdf
        1. highlights
            1. Defense Against Scribbles, Data Protection
            2. Latency breakdown on NVDIMM-N
        2. related paper
            1. NOVA-Fortis: A Fault-Tolerant Non-Volatile Main Memory File System  [2017, 0 refs]
                1. same group of authors
    6. A Sideband Database for HPC and Archival Storage Systems Supporting Billions of Files
       http://storageconference.us/2017/Presentations/Farmer.pdf
       https://www.youtube.com/watch?v=7MjXJ5Te31s&feature=youtu.be
        1. add tags or key-value pairs to the records that represent files and directories
        2. File System Catalog
    7. Stoarge Acceleration with ISA-L
        1. Intel
        2. related
            1. Ceph Erasure-coding and ISA-L
               http://storageconference.us/2017/Presentations/Tucker-2.pdf
       http://storageconference.us/2017/Presentations/Tucker-1.pdf
    8. Building High Speed Erasure Coding Libraries for ARM and x86 Processors
       http://storageconference.us/2017/Presentations/Simonsen.pdf
        1. MemoScale Erasure Coding Library - no detail
    9. The Benefits of Hardware-Software Co-Design/Convergence for Large- Scale Enterprise Workloads
       http://storageconference.us/2017/Presentations/Palmeter.pdf
       https://youtu.be/OwXYg-3ifWM
        1. Oracle selling boxes
    10. Design Decisions and Trade-offs in Apache Accumulo
        http://storageconference.us/2017/Presentations/Cordova.pdf
        https://www.youtube.com/watch?v=a9l8QpoFTD4&feature=youtu.be
        1. Accumulo - improved BigTable
    11. Unresolved Storage Issues in Linux Container Interfaces
        https://www.youtube.com/watch?v=57g9hNGGOuk&feature=youtu.be
    12. LaLDPC: Latency aware LDPC for Read Performance Improvement of Solid State Drives [2017, 3 refs]
        http://storageconference.us/2017/Papers/LatencyAwareLDPC.pdf
        http://storageconference.us/2017/Presentations/LatencyAwareLDPC-slides.pdf
        1. Higher-capability LDPC codes
```
