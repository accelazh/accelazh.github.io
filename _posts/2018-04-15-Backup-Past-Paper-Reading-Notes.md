---
layout: post
title: "Backup Past Paper Reading Notes"
tagline : "Backup Past Paper Reading Notes"
description: "Backup Past Paper Reading Notes"
category: "storage"
tags: [storage, fast, paper]
---
{% include JB/setup %}

```
1. readings: FAST16 papers
    1. NOVA: A Log-structured File System for Hybrid Volatile/Non-volatile Main Memories [2016, 3 refs]
       https://www.usenix.org/conference/fast16/technical-sessions/presentation/xu
        1. insteresting materials referenced by this paper
            1. Consistency Without Ordering    [2012, 52 refs]
               http://research.cs.wisc.edu/adsl/Publications/nofs-fast12.pdf
                0. referenced in FAST16: NOVA: it proposed backpointer for journaling (to build atomic operations)
                1. use backpointer, a piece of redudent in-place data associated (atomically written) with each data blocks, to ease write ordering
                2. key designs
                    1. "backpointer": to add a pointer in data block, inode, etc to point its "should be" parent
                       backpointer is atomically write (use disk atomic sector write) with data block
                        1. so that, when inconsistency, we have the backpointer as the single source of truth
                        2. so that, we don't need write ordering now
                    2. the general idea: associate each object with its logical identify
                3. drawbacks / doubts
                    1. no solution for atomicity yet, this is just for write ordering
                    2. the paper said "involves modifications to the Linux page cache". this can hardly be practical in real use
                    3. backpointer takes some space in data block, it must be write atomically in a sector
                    4. the overhead of checking / verifying the backpointer everytime?

            2. Optimistic Crash Consistency    [2013, 55 refs]
               http://research.cs.wisc.edu/adsl/Publications/optfs-sosp13.pdf
                0. referenced in FAST16: NOVA: to optimize journaling (for atomic operations), it decoupse ordering from durability
                1. good paper to read. the analysis to crash consistency are good.
                   same author with Consistency Without Ordering
                2. optimistic crash consistency
                    1. the motivations are
                        1. flushing / fsync() couples write ordering and durability. we don't always need both
                            1. ordering and durability should be separatedly addressed, and the fsync()/flush penalties too much for just ordering
                           flushing also jam disk out-of-order write completion, performance impact
                           flushing writes out all data, but actually we only need the target write to be persistent and tell us
                            1. 5x performance impact as tested on EXT4
                        2. disable flushes doesn't necessarily lead to inconsistency; call it probabilistic crash consistency
                            1. inconsistency factor Pinc is only high when a lot of random read writes
                            2. disk scheduler is not always trying to reorder writes
                               put data and journal farther to each other gives less reordering
                    2. the core ideas
                        1. transactional checksumming can remove the need of ordering writes
                            1. this is very clever
                        2. asynchronous durability notifications, which is newly added by authors to disk interface, can be used to delay metadata writeout
                            1. I thinks this is more general applicable and hits the essential pain point of flush
                        3. overall, less write ordering, more parallel write out of each component, async delayed background writes without fsync() blocking app
                3. We need to ensure: D, JM, JC -> M (data (M), metadata journal (JM), journal commit (JC) are entirely persistent before metadata (M) are written out)
                    1. the key is transactional checksumming, i.e. JC contains checksum of D and JM.
                       D, JM, JC can be submitted in parallel; if checksum matches, it equals to D, JM -> JC
                    2. M must happens after D, JM; it needs D to avoid pointing to garbage data, needs JM to ensure able to redo/undo
                       the author introduces a disk interface change "asynchronous durability notification" for that
                       M writing out / waiting happens in background, it doesn't pause app execution
                    3. when allocator tries to reuse data blocks, always find durably-free ones
                    4. selective data journaling journals data together with metadata in journal, so that M doesn't need to wait for D
                4. drawbacks
                    1. need to modify disk interface to allow asynchronous durability notification, that's hardly possbile for real use now

            3. BTRFS: The Linux B-Tree Filesystem [2012, 106 refs]
               http://domino.research.ibm.com/library/cyberdig.nsf/papers/6E1C5B6A1B6EDD9885257A38006B6130/$File/rj10501.pdf
                0. referenced in FAST16: NOVA: it uses shadow paging / copy-on-write instead of journaling to build atomic operations, how?
                1. copy-on-write b-tree with defragmentation considered snapshots
                   the performance is a little lower than EXT4, but is greatly superior for random writes
                   there is still need of "logging/journaling", i.e. the "log-tree", but COW b-tree ease the burden of journaling and makes atomicity easer
                2. key designs & findings
                    1. about the COW b-tree
                        1. each tree node takes up exactly one page
                        2. small files that occupy less than one leaf block may be packed into b-tree inside
                        3. btrfs allocation is based on extents, extent can be splited into several smaller extent if written in the middle
                        4. the COW tree makes atomicity is relatily simple, just a pointer change in root pointer
                        5. the downside is performance relies on the ability to maintain large extents of free contiguous disk areas
                           and, random updates to a file tend to fragment it
                    2. COW b-tree issue: all updates have to ripple up to the root of the filesystem
                        1. all these tree modifications are accumulated in memory, and after a timeout (30s) or enough page changed, batch write to new disk locations, forming a checkpoint
                        2. on fsync() durability is taken care of, data batch write to disk
                        3. since most user operations have locality into several hot file/dir, the tree modification is organized that only normally modify a single path
                        4. modified data and metadata related to the particular file are written to a special log-tree, to be later used in crash recovery
                    4. defragmentation
                        1. one is to read & COW it and write sequentially to a new place
                            1. it is simple and usually sufficient
                            2. but snapshots sharing the same chunk will results into being copied; sharing becomes full data clone
                        2. another is complex, with snapshot sharing in concern; basically to copy it and write sequentially to new place
                            1. to don't violate the snapshot sharing relation

1. read the Azure Storage related literature
    1. LSM trees (used in BigTable etc.) and Fractal Trees (used in TokuDB)
       https://www.quora.com/What-are-the-major-differences-between-LSM-trees-used-in-BigTable-etc-and-Fractal-Trees-used-in-TokuDB
        1. Write Optimization: Myths, Comparison, Clarifications
           https://www.percona.com/blog/2011/09/22/write-optimization-myths-comparison-clarifications/
           https://www.percona.com/blog/2011/10/04/write-optimization-myths-comparison-clarifications-part-2/
            1. "write optimization in B-trees involves maximizing the useful work we accomplish each time we touch a leaf"
            2. good article. LSM uses an array of b-trees from memory to disk, COLA uses fractional cascading to speed up searches for the previous
               COLA inserts as fast as LSM, and quesies as fast as b-tree; i.e. COLA is better than LSM
            4. COLA trees improved "the optimal insert/query trade-off curve", while LSM tree is not on the curve
        2. Fractional cascading
           https://en.wikipedia.org/wiki/Fractional_cascading
            1. good algorithm design structure.
               "by embedding within each component forward pointers to the next component to be searched"
        3. Versioned external-memory dictionaries with optimal query/update tradeoffs
           https://arxiv.org/pdf/1103.2566.pdf
        4. Cache-Oblivious Streaming B-trees
           http://people.seas.harvard.edu/~minilek/papers/sbtree.pdf
        5. The Log-Structured Merge-Tree (LSM-Tree)
           http://www.inf.ufpr.br/eduardo/ensino/ci763/papers/lsmtree.pdf

    2. B-Tree foundamentals
        1. The Ubiquitous B-Tree    [1979, 2256 refs]
           https://wwwold.cs.umd.edu/class/fall2002/cmsc818s/Readings/b-tree.pdf
        2. Performance of B + Tree Concurrency Control Algorithms    [1993, 75 refs]
           http://www.vldb.org/journal/VLDBJ2/P361.pdf
        3. A survey of B-tree locking techniques
           http://www.hpl.hp.com/techreports/2010/HPL-2010-9.pdf

    3. Flat Datacenter
        1. Flat Datacenter Storage    [2012, 88 refs]
           https://www.usenix.org/system/files/conference/osdi12/osdi12-final-75.pdf
            1. problems to solve
                1. network over-subscribed at datacenter scale. traditionally they are tree structure
                    1. programmers are forced to think "rack locality", moving computation to data, etc
                2. locality constraint sometime are not appropriate and even hinder efficient resource utilization
                    1. straggler task: a task is not complete untile its slowest worker is complete
                    2. retasking nodes
            2. FDS key designs
                0. large numbers of small commodity switches with redundant interconnections, has made it economical to
                   build non-oversubscribed full bisection bandwidth networks at the scale of a datacenter
                    1. FDS' main goal is to expose all of a cluster's disk bandwidth to applications
                    2. Even when computation is co-located with storage, all storage is treated as remote; in FDS, there are no "local" disks
                    3. FDS returns to the flat storage model: all compute nodes can access all storage with equal throughput
                    4. give each storage node network bandwidth equal to its disk bandwidth
                    5. The TORs load-balance traffic to the spine using ECMP (equal-cost multipath routing)
                        1. but, Long-lived, high-bandwidth flows are known to be problematic with ECMP
                    6. node NIC uses large-send offload, receive-side scaling (RSS), and 9 kB (jumbo) Ethernet frames
                       also, TCP stack is configured with a reduced MinRTO
                        1. need 5 flows per 10 Gbps port to reliably saturate the NIC?
                        2. At 20Gbps, a zero-copy architecture is mandatory
                    7. By design, at peak load, all FDS nodes simultaneously saturate their NICs with short, bursty flows.
                       A disadvantage of short flows is that TCP's bandwidth allocation algorithms perform poorly.
                       Under the high degree of fan-in seen during reads, high packet loss can occur as queues fill during bursts.
                       The reaction of standard TCP to such losses can have a devastating effect on performance. This is sometimes called incast
                        1. collisions mostly occur at the receiver.
                           to prevent it happend in application layer, FDS uses a request-to-send/clear-to-send (RTS/CTS) flows cheduling system
                            1. Large sends are queued at the sender, and the receiver is notified with an RTS.
                               The receiver limits the number of CTSs outstanding
                            2. RTS/CTS adds an RTT to each large message
                               However, the FDS API encourages deep read-ahead and write-ahead
                1. FDS guarantees atomicity but no ordering (of tracts)
                2. metadata server is off the critical path, data distrbution is by deterministic hash
                3. work allocation: mainly to avoid straggler
                   give small units of work to each worker as it nears completion of its previous unit (by callback notification)
                4. the primary replica doesn't commit until all other replicas complete
                   aslo support per-blob variable replication count (per-blob metadata is stored on tractserver)
                5. TLT may be too large, with O(n^2) entries
            3. lecture notes from UTAH
               http://www.cs.utah.edu/~stutsman/cs6963/lecture/03/
                1. see the networking graph, the key is TOR<->Spine bisection
            4. Binospace blog: Flat DataCenter Storage之系统分析
               http://www.binospace.com/index.php/flat-datacenter-storage-system-analysis/
                1. the paper is interesting when it compares to Hadoop's core ideas: computation to data locality, rack locality
                   when it is at the age of Hadoop, MS thinks something else
        2. VL2: A Scalable and Flexible Data Center Network
           https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/vl2-sigcomm09-final.pdf
            1. VL2 solves datacenter network oversubscribtion with affordable cost
            2. key designs
                1. built from low-cost switch ASICs arranged into a Clos topology
                    1. CLOS network: https://en.wikipedia.org/wiki/Clos_network
                2. adopt Valiant Load Balancing (VLB) to spread traffic across all available paths
                    1. Valiant Load Balancing: http://www.springer.com/cda/content/document/cda_downloaddocument/9781848827646-c2.pdf?SGWID=0-0-45-1123938-p173911520
                    2. We implement VLB by causing the traffic between any pair of servers
                       to bounce off a randomly chosen switch in the top level of the Clos topology
                       and leverage the features of layer-3 routers, such as EqualCost MultiPath (ECMP),
                       to spread the traffic along multiple subpaths for these two path segments
                3. the switches operate L3 using OSPF
                   L2 use IP addresses that act as name alone, shim-layer invokes a dictionary system and tunnel to destination
                    1. the shim-layer at L2 also elimates ARP scalability issue (like Neutron's ARP?)
                    2. directory system is implemented by Paxos

    4. Google Megastore
        1. Megastore: Providing Scalable, Highly Available Storage for Interactive Services    [2011, 535 refs]
           http://cidrdb.org/cidr2011/Papers/CIDR11_Paper32.pdf
            1. Metastore is built on top of Bigtable
                1. try to blend RDBMS and NoSQL
                2. proivdes strong consistency
                3. fully serializable ACID semantics within fine-grained partitions of data
                4. synchronously replicate each write across WAN with reasonable latency, and seamless failover between datacenters
                    1. based on Paxos, use Paxos to replicate log append
                    2. use user cells to partition global database space
            2. key designs
                1. most Internet services can be suitably partitioned (e.g., by user), called entity groups
                    1. partition the datastore and replicate each partition separately
                        1. give applications fine-grained control over how to partition
                    2. provide full ACID semantics within partition, but only limitted cosistency guarantees across them
                        1. application needs read-modify-write so much
                        2. inside entity group use single phase transaction, cross entity group use two phase commit for transaction
                    3. each partition (small) database has its own replicated log
                2. use Paxos as the way to replicate primary user data across datacenter
                    1. without distinguished master
                       replicate a write-ahead log over a group of symmetric peers
                       any node active-active read write
                    2. use multiple replicated log, each governing its own partition of the data set
                3. a tour of metastore
                    1. API designs
                        1. cost-transparent APIs with runtime costs that match application developers' intuitions
                        2. joins are not recommended. it is implemented in app code instead.
                        3. the data model / language offers fine-grained control over physical locality
                    2. data model
                        1. declared in a schema and is strongly typed
                            1. data model consists of tables consists of entities consists of properties, properties can be list
                            2. a sequence of properties is used as the primary key
                            3. child table needs a single distinguished foreigin key referenced to its partent table
                        2. each entity is mapped into single Bigtable row
                            1. Megastore tends to pre-join entities by seeing foreign keys, put into adjacent in the same Bigtable
                               this can recursive and be used to force hierachical layout by manipulating the key order
                        3. indexes
                            1. a global index spans entity groups, to find entities without knowing which entity group it's in
                               but are not guaranteed to reflect all recent updates
                            2. by adding STORING clause, data can be stored inline in index
                            3. index support list / repeated properties
                            4. inline indexes can extract info from child entities and store them at parent for fast access
                            5. allows map more than one table rows to one Bigtable row
                    3. transactions and concurrency control
                        1. entity group functions as a mini-databse
                           a transaction first write to WAL, then the actual data
                        2. Bigtable allows store multiple value with different timestamp
                           it is used to implement MVCC in entity group
                            1. Megastore provides current, snapshot, and inconsistent reads
                            2. optimistic concurrency by watch the log position not changed
                        3. queues provide transactional messaging between entity groups
                            1. can batch multiple updates into a single transaction
                            2. queues offer a way to perform operations that affact many entity groups
                            3. declaring a queue automatically creates an inbox on each entity group, giving us millions of endpoints
                            4. Megastore supports two-phase commit for atomic updates across entity groups
                               but it has higher latency and risk of contention, it is generally discouraged
                    4. other features
                        1. full-text index, backup, encryption at rest
                4. replication: a low-latency implementation of Paxos
                    1. fast read: local reads
                        1. A coordinator server tracks a set of entity groups for which its replica has observed all Paxos writes
                           For entity groups in that set, the replica has sufficient state to serve local reads
                            1. reads need to query local coordinator first, before actually read from replica
                            2. Before a write is considered committed and ready to apply,
                               all full replicas must have accepted or had their coordinator invalidated for that entity group
                    2. fast write: single roundtrip
                        1. run an independent instance of Paxos for each log position
                           the leader for each log position arbitrates who wins, all other writers must fall back on two-phase Paxos
                            1. select leader by which app writes most in its region
                    3. replica types (besides the normal ones)
                        1. witness replicas vote but only maintains WAL, no actual data
                            1. they are effective tie breakers and are used when there are not enough full replicas to form quorum
                        2. read-only replicas don't vote, but contains full snapshot of data
                            1. reflecting a consistent view of a point in recent past
                            2. help disseminate data over a wide geographic area without impacting write latency
                    4. architectures
                        1. each app server has a designed local replica
                        2. client library makes Paxos operations on that replica durable
                           by submitting transactions directly to the local Bigtable
                        3. the library submits remote Paxos operations to stateless intermediary replication servers
                           which communicating with their local Bigtables
                        4. the coordinator
                            1. the coordinator is a simple process with no external dependencies and no persistent storage
                               it can server fast, usually stable
                            2. coordinator relies on Chubby to acquire the majority lock
                            3. when coordinator is unavailable
                               reads need to query the majority of replicas
                            4. writer knows it by testing whether coordinator has lost its locks, if then
                               write wait for coordinator to ragain locks; it's a small rare outage
                            5. coordinator liveness protocol is vulnerable to asymmetric network partitions
                                1. needs manual steps to recover

        2. Binospace blog: Google-MegaStore的解读
           http://www.binospace.com/index.php/google-megastore-interpretation/
            1. "Google的这个模型，个人感觉是以应用为中心的，不是以服务为中心的架构。
                例如，MegaStore服务的GMail应用，会以这个应用构建一套ReplicationServer、Coord，以及对应BigTable，
                而不是通过这个架构对外提供统一的服务"

    4. COLA tree, Fractal tree, TokuDB, Cache-Oblivious Streaming B-trees
        1. TokuDB中的COLA-Tree
           http://blog.csdn.net/jwh_bupt/article/details/7901269
           http://www.kryptosx.info/archives/931.html
           https://read01.com/5Qe62K.html
           How TokuDB Fractal TreeTM Indexes Work
           http://www.kryptosx.info/wp-content/uploads/2015/04/How-TokuDB-Fractal-Tree-Databases-Work-Presentation.pdf
            1. COLA tree is levels of arrays, each level double the size. inserts cause merges (sequential writes)
               average insert cost is O(logN/B)
            2. to improve worst case insertion, add a assistance array by side of each level
               worst cose is improved from O(N/B) to O(log(N)/B)
            3. TokuDB Fractal tree adds forward pointer (fractional cascading) to COLA tree, to improve query speed
               query/search is the same as b-tree, O(logN)
            4. TokuDB license is too expensive, and propotional to data size. under 50GB is free
               recommended to store data at NoSQL, but use TokuDB as the index
        2. wiki: fractal tree index
           https://en.wikipedia.org/wiki/Fractal_tree_index
            1. LSM tree insert matches fractional tree, but query time is slower by a logarithmic factor
            2. although B-trees and Fractal Tree indexes are both on the optimal tradeoff curve between insertions and queries
               LSMs are not
            3. there are ways to make LSM tree queries faster, for example
                1. use bloom filter
            4. the current fractal tree implementation is an extension of the Bε tree
            5. Fractal Tree index is a refinement of the Bε tree, with several improvements and performance optimizations
                1. ACID semantics and locking
                2. buffers are themselves indexed in order to speed up searches
                3. Fractal tree leaves are much larger, thus compression is effective
                4. Fractal Tree indexes is to have large leaves that can be fetched as a whole for fast range queries
                   but are broken into smaller pieces called basement nodes which can be fetched individually (for small / point queries)
        3. what is Bε-trees?
            1. An Introduction to Bε-trees and Write-Optimization    [2015, no refs]
               http://supertech.csail.mit.edu/papers/BenderFaJa15.pdf
                1. B-tree is designed to be read-optimzied on the insert/query trade-off curve
                   but B^e-tree is used to stand in the middle ground
                2. in B^e-tree, each node is roughly of size B, data stored in leaves
                   ε controls how much of an internal node's space is used for pivots (Bε)
                   and how much is used for buffering pending updates (B − Bε)
                3. insertions are encoded as "insert messages", addressed to a particular key, and added to the buffer of the root node of the tree
                   when enough messages have been added to a node to fill the node's buffer, a batch of messages are flushed to one of the node's children
                4. in order to make searching and inserting into buffers efficient,
                   the message buffers within each node are typically organized into a balanced binary search tree,
                   such as a red-black tree
                5. the ε was originally designed to show the optimal insert/query trade-off curve
                6. when ε = 1 it matches the performance of a B-tree,
                   and when ε = 0, it matches the performance of a buffered-repository tree (BRT)
                7. mentioned Betrfs, the FAST16 best paper
        4. Percona TokuDB
           https://www.percona.com/software/mysql-database/percona-tokudb
           https://github.com/percona/tokudb-engine
           https://github.com/Percona/tokudb-engine/wiki
            1. TokuDB and Percona, both for MysqlDB, are merged
            2. fractal tree engine seems opensourced
               https://github.com/percona/tokudb-engine
               https://github.com/Percona/tokudb-engine/wiki
        5. what is buffered-repository tree
            1. On External Memory Graph Traversal    [2000, 117 refs]
               http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.31.128&rep=rep1&type=pdf
                1. for Bε-tree, when ε = 1 it matches the performance of a B-tree,
                   and when ε = 0, it matches the performance of a buffered-repository tree (BRT)
                2. an (a, b)-tree, each node has a buffer, overflow to children. only root is held in memory
                   buffered-repository tree is called buffer-tree too
                3. other materials: http://homes.soic.indiana.edu/qzhangcs/papers/EM_overview_CTW2010.pdf
                                    http://www.cc.gatech.edu/~bader/COURSES/GATECH/CSE-Algs-Fall2013/papers/Arg03.pdf
        6. Cache-Oblivious Streaming B-trees    [2007, 89 refs]
           http://people.seas.harvard.edu/~minilek/papers/sbtree.pdf
            1. shuttle tree
                1. a SWBST balanced search tree (split ancestor by weight)
                2. differs from buffered-repository tree (BRT) in that it has a linked-list of buffers for each child
                   the buffers have doubly-exponentially increasing size
                3. lay out the shuttle tree in "van Emde Boas (vEB) layout", with buffer size on Fibonacci numbers
                4. we maintain this layout dynamically by embedding the shuttle tree in a packed-memory array (PMA)
                    1. The PMA is simply an array
                       that allows for efficient insertions (amortized O(log2N/B) block transfers)
                       by leaving gaps between elements
            2. cache-oblivious lookahead array (COLA)
                1. It consists of roof(log2(N)) arrays, or levels, each of which is either completely full or completely empty
                   The kth array is of size 2^k and the arrays are stored contiguously in memory
                2. speed up searches by fractional cascading
                    1. Every eighth element in the (k + 1)st array also appears in the kth array, with a real lookahead pointer to its location in the (k + 1)st array.
                    2. Each fourth cell in the kth array is reserved for a duplicate lookahead pointer, which holds pointers to the nearest real lookahead pointer to its left and right.
                    3. Thus, every level uses half its space for actual items and half for lookahead pointers.
                3. we improve the worst-case bound from O(N/B) to O(logN)
                    1. In level k of the lookahead array we maintain two arrays each of size 2k.
                    2. Whenever a level contains items in both of its arrays, we begin merging those two arrays into an empty array in the next level
                    3. stop when there is no unsafe levels, or have moved m items in total
                       If a lookahead array contains k levels, setting m =2k+2 guarantees that two adjacent levels are never simultaneously unsafe
            3. the experiment results
                1. B-tree performs faster for searches than COLA, but they are on the same O
                2. B-tree performs much faster than COLA for sorted inserts when N is large
                    1. authors believe b-tree is faster because only uses the leftmost root-to-leaf path, which can stay in memory
                3. COLA tree performs much better than B-tree for random inserts
                   but sorted and random inserts performs the same speed in COLA (not like B-tree is faster for sorted inserts)

1. readings: FAST16 papers
    1. Optimizing Every Operation in a Write-optimized File System    [2016, 1 refs]
       https://www.usenix.org/conference/fast16/technical-sessions/presentation/yuan
        1. fast 16 best paper. very good to read
            1. Using three techniques, late-binding journaling, zoning, and range deletion,
               BetrFS 0.2 shows that there is no fundamental trade-off in write-optimization
                1. insert/query trade-off was previously a well-known concept in LSM-tree/Fractal-tree/B-tree debates
                   now things keep changing
                2. improve on random writes, metadata updates, and directory traversals by orders of magnitude,
                   without sacrificing performance on other file-system operations
            2. BetrFS 0.1 is a port of TokuDB (already opensourced) into the Linux kernel
               the core of BetrFS 0.1 is the Bε-tree / B^e-tree (Bε-tree = B^e-tree)
                1. it has journal double writes, resulting in at most half of disk bandwidth write problem
                2. it has slow file deletions, renames, and sequential file writes
                3. this paper solves them
            3. the evaluation part looks really good. the paper brings fractal tree / B^e-tree ready to filesystem world
               following the trends in DB
        2. background analysis
            1. although WODs such as fractal tree, LSM-tree accelerates random writes,
               but journaling the data (especially large data chunk) needs write twice
                1. TokuDB logs all inserted keys and values to support transactions,
                   limiting the write bandwidth to at most half of disk bandwidth
                2. the same problem of BetrFS 0.1
            2. BetrFS 0.1 uses two Bε-trees: a metadata index and a data index
                0. BetrFS 0.1 has slow file deletions, renames, and sequential file writes, the same with TokuFS
                1. The metadata index maps full paths to the corresponding struct stat information
                    1. so, the traditional dir inode stuff doesn't exist, name mapping are global
                       recursive directory traversals are WOD's range query, at nearly disk bandwidth
                        1. while traditional dir inode path-pointer traversal is on-disk scattered and slow
                    2. but, the problem is, rename needs to move move every file, dir on the Bε-tree
                       it is slow
                2. The data index maps (path, block-number) pairs to the contents of the specified file block
                3. BetrFS 0.1 caches dirty data (due to VFS). crash lose at most 6 seconds
                   has to use fsync(), which writes entire log buffer to disk
                    1. compared to Ceph, Azure Storage, etc,
                       I have to say that POSIX filesystem's cache dirty data until you fsync() semantics looks a bit out-dated
                       modern storage systems usually: write is persistented/consistent once user receives ack (function returns)
                    2. the second problem is, relying on fsync() for persistency/consistenct is too costly
                       the user wants "this" write to be ack-ed as persistent, by fsync() force flush the entire buffer
                       and also clear the cache, which is unnecessary
                    3. another question, if BetrFS 0.1 already choose to journal data with metadata,
                       why doesn't it achieve write-ack persistency/consistency/recovery-semantics altogether?
                       (without relying on fsync())
        3. key designs
            1. avoid journal double write problem (the main reason why BetrFS 0.1 large seq write is slow)
                1. prior-arts
                    1. existing update-in-place filesystems, such as ext4, handle this problem
                       by metadata-only journaling as a result
                    2. popular no-overwrite file systems address journal write amplification with indirection
                        1. for small values, zfs embeds data directly in a log entry
                        2. for large values, it writes data to disk redirect-on-write, and stores a pointer in the log
                    3. copy-on-write filesystems
                        1. btrfs uses indirection for all writes, regardless of size
                           it writes data to newly-allocated blocks
                           and records those writes with pointers in its journal
                2. BetrFS 0.2's solution: late-binding journal (actually no much innovative)
                   like ZFS, for large write, indirect data outside, then record a pointer in log
                    1. step 1: write an unbound log entry in journal memory buffer (not on disk),
                               with op & key, but no value. it is used to record operations' order
                       step 2: insert unbound entry into Bε-tree, which contains value
                       step 3: after entry in Bε-tree are written on disk,
                               a binding log entry is appended to journal memory buffer
                       step 4: once all entries are bound, journal memory buffer are flushed to disk
                    2. unbound entires only exist in memory, on disk structure & format doesn't change
                    3. late-binding journal forces tree node to be flushed to disk,
                       lost oppotunities to batch more small modifications
                        1. so only applicable for large write
            2. balancing search and rename
                1. as mentioned in background analysis, BetrFS 0.1 indexes all file, dir in the metadata Bε-tree
                   dir traversal is naturally fast but rename is slow.
                    1. on the contrary to traditional filesystems which put dir-file mapping in each dir inode
                    2. the authors consider it the trade-off of dir traversal vs rename
                2. BetrFS 0.2's solution: partition metadata index into zones,
                                          which makes the trade-off parameterizable and tunnable
                    1. each zone has and zone-id
                    2. dir & files of a zone are stored together, so traversal is fast
                       cross a zone boundary requires an extra seek
                    3. renaming file / dir inside a zone requires move data
                       renaming a zone (usually a large stuff), needs only to move pointer
                    4. if zone size is limitted to 1, BetrFS 0.2 becomes a dir inode based FS
                       if zone size is infinit, BetrFS 0.2 fallbacks to 0.1
                    5. so, when zone is smaller, moving/renaming small file / dir is less expensive
                       especially when it is renaming/moving a zone, just need pointer change
                        1. zone max size limits the upper bound of renaming/moving cost
                           zone min size indicates dir traversal speed
                3. from the evaluation part, zoning yields great results,
                   although it looks like doesn't improve anything
            3. efficient range deletion
                1. BetrFS 0.1 deletion time is linear in the amount of data being deleted
                    1. because of the sheer volume of delete messages that must be inserted into the B^e-tree
                       and B^e-tree cannot infer that two keys are adjacent in the keyspace
                2. to support delete a key range in a single message, authors added a rangecast message type
                    1. specifying the beginning and ending key, the range can be sparse
                    2. when a rangecast message is flushed to a child,
                       the propagation must check whether it spans multiple children
                       split the message and apply to each child
                    3. the message is defering in buffer, so that there may be enough message to obviate them
                        1. a key is inserted then deleted
                        2. delete an unbound inserts
                        3. prune an leaf entirely directly
                    4. the query involved in deletion is efficient because
                        1. all relevant messages will be in a node's buffer on the root-to-leaf search path
                        2. we can store rangecast messages in each node using an interval tree (log(n) then)
            4. optimized stacking
                1. BetrFS 0.1 is implemented on top of ext4
                   BetrFS 0.2 still use ext4 underlyingly but use it better
                    1. what, why use ext4 underlying? in kernel?
                       originally want to build like a DB on top of a common FS?
        4. evaluation
            1. rename, with proper zone size, is constant with file size, but slower than other filesystems
                1. the idea of zoning is effective.
                   zoning make rename time constant to file system now
            2. sequential IO is near (a little bit worse) dominate FS such as ext4, xfs, zfs
            3. `find` is 10x faster, `grep` is 2-10x faster, `mv`, `rm` is basically the same,
                random small write is 100x faster than ext4, xfs, zfs
                1. awesome results
                2. range deletion make unlink time constant to file system now
            4. generally, BetrFS 0.2 beats every filesystem
                1. the best cases are 10x - 100x better
                2. the worse cases are a little slower
        5. pre-readings
            1. add my pre-reading papers

1. readings: FAST16 papers
    1. Spinning Disks and Their Cloudy Future (by Google)
       https://www.usenix.org/conference/fast16/technical-sessions/presentation/brewer
        1. great emphase on the Tail Layency problem
            1. send the same request to multiple disks
            2. cancel pending requets
        2. collection view: many layers
            1. disk
            2. server
            3. data center
            4. geo replication
        3. fine-grain scheduling
            1. leave the detail of what to do to disks
               but when to do to host
            2. fine-grain labeling for all IOs: low latency, throughput, best effort
        4. aggregate mix of different disks (GB/$ vs IOPS/GB trade-off)
            1. find the optimal top edges of convex hull
        5. about the SSDs
            1. google don't use it as the core now in the datacenter
               most of their storage will be disks for at least 5-10 years
               but SSD is good to absorb high-performance workloads
            2. SSDs and HDDs both have good capacity growth rates
                1. Hard for SSDs to catch up soon
        6. others
            1. taller drives?
            2. multi-disk packages?
        7. related readings
            1. whitepaper: Disks for Data Centers
               http://research.google.com/pubs/pub44830.html
                1. covers this above material in more depth
                   the physical design options part are very good
                2. the five key metrics:
                    1. Higher I/Os per second (IOPS), typically limited by seeks,
                    2. Higher capacity, in GB
                    3. Lower tail latency, covered below,
                    4. Meet security requirements, and
                    5. Lower total cost of ownership (TCO).
                        1. At the data center level, the TCO of a disk­based storage solution is dominated by
                            the disk acquisition cost,
                            the disk power cost,
                            the disk connection overhead (disk slot, compute, and network),
                            and the repairs and maintenance overhead
                3. at the collection view, we optimize overall IOPS and capicty, by
                    1. using a carefully chosen mix of drives
                       the marginal IOPS and capacity added closer to our goals
                       workload changes, such as better use of SSDs or RAM, can shift the aggregate targets
                4. why talking about spinning disks at all, rather than SSD?
                    1. The root reason is that the cost per GB remains too high,
                       and more importantly that the growth rates in capacity/$ between disks and SSDs are relatively close
                       (at least for SSDs that have sufficient numbers of program­erase cycles to use in data centers),
                       so that cost will not change enough in the coming decade
                5. tail latency for reads (writes latency are easier to hide)
                    1. e.g. if one disk (or system) has it cached, but the others have queued up real reads
                6. security
                    1. firmware: Hard disk firmware attacks are not only possible, but appear to have been used
                    2. ensure the data is "encrypted at rest"
                    3. Fine grained access control, using different keys for different areas of the disk
                7. Physical Design Options
                    1. Alternative Form Factors [TCO, IOPS, capacity]
                        1. Parallel Accesses [IOPS]
                        2. Multi‐Disk Packages [TCO]
                        3. Power Delivery [TCO]
                    2. Cache Memory [TCO, tail latency]
                    3. Optimized SMR Implementation [capacity]
                        1. Firmware Directions
                    4. Profiling Data [IOPS, tail latency]
                    5. Host‐Managed Read Retries [tail latency]
                    6. Target Error Rate [capacity, tail latency]
                    7. Background Tasks and Background Management APIs [tail latency]
                        1. Background scanning [tail latency]
                    8. Flexible Capacity [TCO, capacity]
                    9.  Larger Sector Sizes [capacit
                    10. Optimized Queuing Management [IOPS]
            2. study on tail latencies / long timeout tails
                1. add my parts, also Hsytrix

2. readings: misc
    1. Netflix Hsytrix
       https://github.com/Netflix/Hystrix/wiki
        1. what does it do
            micro-service / API governance
            controls latency and resilient to dependency compoennt slow/failure
            handle recovery, quota control, failure isolation\
            1. the dashboard is really good. I guess people love it
        2. how it works
           https://github.com/Netflix/Hystrix/wiki/How-it-Works
            1. the flowchart and code examples are helpful
            2. the client libraries vs thread pools
                1. app uses it own client lib provided by each service, vs.
                   use the managed thread pool
            3. use semaphors instead of threads to limit the number of concurrent calls
                1. This allows Hystrix to shed load without using thread pools
                   but it does not allow for timing out and walking away
            3. request collapsing
                1. without request collapsing: request == thread == network connection
                   with requets collapsing: window == 1, thread == 1
                2. to reduce the number of threads
            4. request caching, with a cache key

        3. Netflix blogging
            1. Making the Netflix API More Resilient    [Dec 8, 2011]
               http://techblog.netflix.com/2011/12/making-netflix-api-more-resilient.html
                1. API Resiliency
                    failure should not break user experience
                    auto corrective action
                    show what's happening now and a momnet ago
                2. the CircuitBreaker pattern
                    1. custom fallback, fail silent, fail fast
                3. Real-time Stats Drive Software and Diagnostics
            2. Fault Tolerance in a High Volume, Distributed System    [Feb 29. 2012]
               http://techblog.netflix.com/2012/02/fault-tolerance-in-high-volume.html
                1. "When a single API dependency fails at high volume with increased latency (causing blocked request threads)
                    it can rapidly (seconds or sub-second) saturate all available Tomcat (or other container such as Jetty) request threads
                    and take down the entire API."
                2. use a combination of fault tolerance approaches
                    1. network timeouts and retries
                    2. separate threads on per-dependency thread pools
                    3. semaphores (via a tryAcquire, not a blocking call)
                    4. circuit breakers
                3. "If a dependency becomes latent (the worst-case type of failure for a subsystem)
                    it can saturate all of the threads in its own thread pool,
                    but Tomcat request threads will timeout or be rejected immediately rather than blocking"
                4. some approaches used as fallbacks
                    1. Cache: Retrieve data from local or remote caches if the realtime dependency is unavailable, even if the data ends up being stale
                    2. Eventual Consistency: Queue writes (such as in SQS) to be persisted once the dependency is available again
                    3. Stubbed Data: Revert to default values when personalized options can't be retrieved
                    4. Empty Response ("Fail Silent"): Return a null or empty list which UIs can then ignore
            3. Performance and Fault Tolerance for the Netflix API - August 2012    [Aug 22, 2012]
               https://speakerdeck.com/benjchristensen/performance-and-fault-tolerance-for-the-netflix-api-august-2012
                1. fault tolerance techniques
                    1. tryable semaphores for "trusted" clients and fallbacks
                    2. separate threads for "untrusted" clients
                    3. aggressive timeouts on threads and network calls (to "give up and move on")
                    4. circuit breakers as the "release value"
                2. a series of ppts illustrating the cost of threads
                    1. the cost of a separated thread can be too high, then we choose to use a tryable semaphores
                    2. if the cost in general is acceptable, we prefer the isolation benefits of a separated thread
                3. some page requires a lot of API requests
                    1. if this is done in client, because client limits connection number, and the latency, page load can be slow
                    2. push that call pattern to server and eliminate redundant calls is preferred
            4. Application Resilience in a Service-oriented Architecture    [Jun 10, 2013]
               http://radar.oreilly.com/2013/06/application-resilience-in-a-service-oriented-architecture.html
                1. the API status dashboard is good. I guess people love it
            5. Application Resilience Engineering & Operations at Netflix    [Jun 19, 2013]
               https://speakerdeck.com/benjchristensen/application-resilience-engineering-and-operations-at-netflix
                1. "Common resilience patterns used by Netflix in production will be shared including:
                    - Bulkhead isolation using threads and semaphores
                    - Circuit breaker
                    - Fail Fast
                    - Fail Silent
                    - Static Fallback
                    - Stubbed Fallback
                    - Fallback via Network Cache"

6. reading: Deep Storage: CMPT 474 by Ted Kirkpatrick from Simon Fraser Univeristy
   http://474.cmpt.sfu.ca/public/schedule.html
    1. Latency Numbers Every Programmer Should Know (By Year)
       https://people.eecs.berkeley.edu/~rcs/research/interactive_latency.html
        1. good reference

    2. The Tail at Scale    [2013, 345 refs]
       https://web.stanford.edu/class/cs240/readings/tail-at-scale.pdf
       lecture notes: http://474.cmpt.sfu.ca/public/Week4-Wed.html
        1. the famous google's tail latency paper. very good to read.
        2. We can get extreme latencies multiple ways
            Garbage collection (languages, file systems, SSDs, …)
            Network contention
            Storage contention
            Over-coordination between components
            Shifting to and from hardware low-power mode
            Multi-tenancy: Other programs running on same hardware

    3. Controlling latency: Basic approaches to reducing latency variability
       http://474.cmpt.sfu.ca/public/Week4-Fri.html
        1. The following methods reduce latency __on average__ and make it __more consistent__
            Overprovisioning
                Add more resources to ensure lower utilization
            Parallelization
                Break the key space into shards
                    Operate on each shard in parallel
                Do the computation near the data
                    Which typically means closer to the disks/SSDs
                    Eliminate longer network latencies
                        especially between-data-centre latencies
            Eliminate "head-of-line" blocking
                Imagine a grocery line for only one teller
                10 people in line have only two items in their basket
                But the person at front (the "head" of the line) is buying a month's worth of food for a family of 10 …
                That person with the big purchase is a "head-of-line blocker"

                Break large request into sequence of smaller ones
                    Intersperse these subrequests with other, shorter requests
                    In the grocery case, it's as though the person buying the big order has to step aside after every 10 purchases and let someone else go through
                    Each subrequest doesn't block the line for long
                    Note that this slows down the one big request (increasing the 99.x %ile of latency)
            Caching can improve the middle percentiles (50 %ile, 75 %ile)
                But not the higher percentiles (99 %ile and up)
        2. Reducing the higher percentiles requires different methods
            Hedged requests
                Source of problem: Once we've parallelized the service (see above), the slowest instance will determine when our request is done
                    And we can't predict in advance which instance will be the slowest
            Solution: Duplicate request
                But if we duplicate every request, we are overprovisioning
                    Require twice the resources
                Better solution: Duplicate only the slow requests
                    Measure our service's current latency
                    Set a threshold at the 95 %ile
                    After the 95 %ile has elapsed since the start of a request, duplicate the (few) lingering incomplete subrequests
                    Use the first answer to be returned (whether the original or the later duplicate)
                    Results in a Google benchmark (p. 77)
                        A BigTable query for 1000 values across 100 servers
                        Wait 10 ms
                        99.9 %ile from 1,800 ms to 74 ms
                        Just 2% more requests
                    Can improve even further by "tying" the duplicate requests (see pp. 77–78)
                        The Tail at Scale: https://blog.acolyer.org/2015/01/15/the-tail-at-scale/
                            7 patterns to enhance tail tolerance
                                Hedged requests
                                Tied requests
                                Micro-partition
                                Selectively increase replication factors
                                Put slow machines on probation
                                Consider 'good enough' responses
                                Use canary requests

    4. On Designing and Deploying Internet-Scale Services
       https://www.usenix.org/legacy/event/lisa07/tech/full_papers/hamilton/hamilton_html/
        1. the list of best practices is helpful. good as a reference
            Overall Application Design
                Design for failure
                Redundancy and fault recovery
                Commodity hardware slice
                Single-version software
                Multi-tenancy
            designing operations-friendly services
                Quick service health check
                Develop in the full environment
                Zero trust of underlying components
                Do not build the same functionality in multiple components
                One pod or cluster should not affect another pod or cluster
                Allow (rare) emergency human intervention
                Keep things simple and robust
                Enforce admission control at all levels
                Partition the service
                Understand the network design
                Analyze throughput and latency
                Treat operations utilities as part of the service
                Understand access patterns
                Version everything
                Keep the unit/functional tests from the previous release
                Avoid single points of failure
            Automatic Management and Provisioning
                Be restartable and redundant
                Support geo-distribution
                Automatic provisioning and installation
                Configuration and code as a unit
                Manage server roles or personalities rather than servers
                Multi-system failures are common
                Recover at the service level
                Never rely on local storage for non-recoverable information
                Keep deployment simple
                Fail services regularly
            Dependency Management
                Expect latency
                Isolate failures
                Use shipping and proven components
                Implement inter-service monitoring and alerting
                Dependent services require the same design point
                Decouple components
            Release Cycle and Testing
                Ship often
                Use production data to find problems
                    Measurable release criteria
                    Tune goals in real time
                    Always collect the actual numbers
                    Minimize false positives
                    Analyze trends
                    Make the system health highly visible
                    Monitor continuously
                Invest in engineering
                Support version roll-back
                Maintain forward and backward compatibility
                Single-server deployment
                Stress test for load
                Perform capacity and performance testing prior to new releases
                Build and deploy shallowly and iteratively
                Test with real data
                Run system-level acceptance tests
                Test and develop in full environments
            Hardware Selection and Standardization
                Use only standard SKUs
                Purchase full racks
                Write to a hardware abstraction
                Abstract the network and naming
            Operations and Capacity Planning
                Make the development team responsible
                Soft delete only
                Track resource allocation
                Make one change at a time
                Make everything configurable
            Auditing, Monitoring and Alerting
                Instrument everything
                Data is the most valuable asset
                Have a customer view of service
                Instrument for production testing
                Latencies are the toughest problem
                Have sufficient production data
                    Use performance counters for all operations
                    Audit all operations
                    Track all fault tolerance mechanisms
                    Track operations against important entities
                    Asserts
                    Keep historical data
                Configurable logging
                Expose health information for monitoring
                Make all reported errors actionable
                Enable quick diagnosis of production problems
                    Give enough information to diagnose
                    Chain of evidence
                    Debugging in production
                    Record all significant actions
            Graceful Degradation and Admission Control
                Support a "big red switch."
                Control admission
                Meter admission
            Customer and Press Communication Plan
                available through multiple channels
                make users feel reasonable and satisfactory
                have communication plan for each type of disaster
            Customer Self-Provisioning and Self-Help
                reduces costs and also increases customer satisfaction

    5. Optimal Logging by Google
       http://googletesting.blogspot.ca/2013/06/optimal-logging.html
        1. a guide and principles of what to log. very good.
           logging should be as much as explain cause of a bug, and whether a certain transaction took place
        2. Good things to log:
                Important startup configuration
                Errors
                Warnings
                Changes to persistent data
                Requests and responses between major system components
                Significant state changes
                User interactions
                Calls with a known risk of failure
                Waits on conditions that could take measurable time to satisfy
                Periodic progress during long-running tasks
                Significant branch points of logic and conditions that led to the branch
                Summaries of processing steps or events from high level functions - Avoid logging every step of a complex process in low-level functions.
            Bad things to log:
                Function entry - Don't log a function entry unless it is significant or logged at the debug level.
                Data within a loop - Avoid logging from many iterations of a loop. It is OK to log from iterations of small loops or to log periodically from large loops.
                Content of large messages or files - Truncate or summarize the data in some way that will be useful to debugging.
                Benign errors - Errors that are not really errors can confuse the log reader. This sometimes happens when exception handling is part of successful execution flow.
                Repetitive errors - Do not repetitively log the same or similar error. This can quickly fill a log and hide the actual cause. Frequency of error types is best handled by monitoring. Logs only need to capture detail for some of those errors.
        3. log levels
            Debug, Info, Warning,
            Error - something went wrong, but the process can recover.
            Critical - the process cannot recover, and it will shutdown or restart.
        4. Conditional Verbosity With Temporary Log Queues
            1. the log is first buffered in memory queues.
               if transaction succeeded, log is ignored; otherwise, print the log
        5. Using failures to improve logging should be used throughout the development process
            1. debug by adding more log
            2. While writing new code, try to refrain from using debuggers and only use the logs
               Do the logs describe what is going on?
        6. request id, activity id
            1. You should create unique identifiers for transactions that involve processing across many threads and/or processes
        7. Monitoring and Logging Complement Each Other
            1. Monitoring provides a real-time statistical summary of the system state
            2. Logs provide details and state on individual transactions

7. readings: investigating on tail latency / long timeout tail, and the problems on azure storage table layer & stream layer
    1. Google Jeff Dean's "the tail at scale" paper    [2013, 345 refs]
       https://web.stanford.edu/class/cs240/readings/tail-at-scale.pdf
       https://blog.acolyer.org/2015/01/15/the-tail-at-scale/
       https://plus.google.com/+JeffDean/posts/fRBupzPMREg
        1. good classic paper. read and logged before.
        2. realted materials
            0. Controlling latency: Basic approaches to reducing latency variability
               http://474.cmpt.sfu.ca/public/Week4-Fri.html
                1. read and logged before
            1. Google: Taming The Long Latency Tail - When More Machines Equals Worse Results    [Mar 12, 2012]
               http://highscalability.com/blog/2012/3/12/google-taming-the-long-latency-tail-when-more-machines-equal.html
                1. to reduce latency
                    1. Tree Of Distribution Responses
                    2. Focus On The 99%
                    3. Latency Tied To Blocking Rather Then Queueing
                        1. head-of-line blocking
            2. Google Strategy: Tree Distribution Of Requests And Responses
               http://highscalability.com/blog/2011/2/1/google-strategy-tree-distribution-of-requests-and-responses.html
                1. the problems
                    1. The CPU becomes a bottleneck, for either processing requests or sending replies, because it can't possibly deal with the flood of requests.
                    2. The network interface becomes a bottleneck because a wide fan-in causes TCP drops and retransmissions, which causes latency.
                       Then clients start retrying requests which quickly causes a spiral of death in an undisciplined system
                2. Instead of having a root node connected to leaves in a flat topology, the idea is to create a tree of nodes.
                    So a root node talks to a number of parent nodes
                    and the parent nodes talk to a number of leaf nodes.
                    Requests are pushed down the tree through the parents and only hit a subset of the leaf nodes.
                        1. can also co-locate parents on same rack as leaves
                        2. it's like NetAgg middlebox
                           https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/mai14netagg.pdf
                3. benefits
                    1. Fan-in at each level of the tree is manageable
                    2. Response filtering and data reduction (by parent)
                    3. Collocation
                4. my questions
                    1. the hops are increased, and some data are reduently sent-received multiple times? what it costs?
            3. Google On Latency Tolerant Systems: Making A Predictable Whole Out Of Unpredictable Parts    [June 18, 2012]
               http://highscalability.com/blog/2012/6/18/google-on-latency-tolerant-systems-making-a-predictable-whol.html
                1. Large fanout architectures are easy to suffer from tail latency
                2. Fault Tolerant Vs Latency Tolerant Systems
                3. to manage latency
                    1. Prioritize request queues and network traffic
                    2. Reduce head-of-line blocking
                    3. Rate limit activity
                    4. Defer expensive activity until load is lower
                    5. Synchronize disruptions
                4. Cross Request Adaptation Strategies
                   the idea is to examine recent behavior and take action to improve latency of future requests within tens of seconds or minutes
                    1. Fine-grained dynamic partitioning
                    2. Load balancing
                    3. Selective partitioning
                    4. Latency-induced probation
                5. Within-Request Adaptation Strategies
                    1. Canary requests
                    2. Backup requests with cross-server cancellation
                        1. use the fastest one, cancel the other requests
                    3. Tainted results
                        1. drop out noncritical subcomponents, as tradeoff completeness for responsiveness
            4. Doing Redundant Work to Speed Up Distributed Queries
               http://www.bailis.org/blog/doing-redundant-work-to-speed-up-distributed-queries/
                1. "In distributed data stores, redundant operations can dramatically drop tail latency at the expense of increased system load;
                    different Dynamo-style stores handle this trade-off differently, and there's room for improvement."
                2. "at the 99.9th percentile,
                    sending a single read request to two servers instead of one is 17x faster than sending to one
                    —maybe worth the 2x load increase"
            5. Building Software Systems at Google and Lessons Learned, by Jeff Dean
               http://static.googleusercontent.com/external_content/untrusted_dlcp/research.google.com/en/us/people/jeff/Stanford-DL-Nov-2010.pdf
               https://www.youtube.com/watch?v=modXC5IWTJI
                1. good material, covery many aspects of google web search infra
                2. google web search status
                    1. update latency: tens of secs
                    2. avg. query latency: <0.2s
                    3. # docs: tens of billions
                3. Group Varint Encoding
                    1. Pull out 4 2-bit binary lengths into single byte prefix
                    2. Decode: Load prefix byte and use value to lookup in 256-entry table
                    3. Much faster than alternatives, i.e. Varint encoding
                4. Numbers Everyone Should Know
                    L1 cache reference 0.5 ns
                    Branch mispredict 5 ns
                    L2 cache reference 7 ns
                    Mutex lock/unlock 25 ns
                    Main memory reference 100 ns
                    Compress 1K w/cheap compression algorithm 3,000 ns
                    Send 2K bytes over 1 Gbps network 20,000 ns
                    Read 1 MB sequentially from memory 250,000 ns
                    Round trip within same datacenter 500,000 ns
                    Disk seek 10,000,000 ns
                    Read 1 MB sequentially from disk 20,000,000 ns
                    Send packet CA->Netherlands->CA 150,000,000 ns
                5. Don't design to scale infinitely:
                    ~5X - 50X growth good to consider
                    >100X probably requires rethink and rewrite
                6. design patterns
                    1. Pattern: Backup Requests to Minimize Latency
                        1. useful when variance is unrelated to specifics of request
                        2. increases overall load by a tiny percentage
                        3. decreases latency tail significantly
                    2. Pattern: Multiple Smaller Units per Machine
                        1. Having each machine manage 1 unit of work is inflexible
                           Have each machine manage many smaller units of work/data
                    3. Pattern: Elastic Systems
                        1. Problem: Planning for exact peak load is hard
                        2. Design system to adapt:
                            – automatically shrink capacity during idle period
                            – automatically grow capacity as load grows
                        3. Make system resilient to overload:
                            - do something reasonable even up to 2X planned capacity
                              • e.g. shrink size of index searched, back off to less CPU
                              intensive algorithms, drop spelling correction tips, etc.
                            – more aggressive load balancing when imbalance more severe
                    4. Pattern: Combine Multiple Implementations
                        1. Example: Google web search system wants all of these:
                            – freshness (update documents in ~1 second)
                            – massive capacity (10000s of requests per second)
                            – high quality retrieval (lots of information about each document)
                            – massive size (billions of documents)
                        2. Very difficult to accomplish in single implementation
                           Partition problem into several subproblems with different engineering tradeoffs.
                            – realtime system: few docs, ok to pay lots of $$$/doc
                            – base system: high # of docs, optimized for low $/doc
                            – realtime+base: high # of docs, fresh, low $/doc
            6. Naive Retries Considered Harmful
               http://www.evanjones.ca/retries-considered-harmful.html
                1. naively retry all requests as soon as a timeout expires
                   This common mistake causes a feedback loop that
                   makes every slightly overloaded service get swamped with a huge spike of requests
                    1. Instead, you must "back off" to avoid overloading the destination during a failure
                    2. a good policy is to send a "backup request" after the 95th percentile latency
                    3. never retry more than 10% of requests within a 5 minute interval
                    4. The problem is when the entire system is slow because it is overloaded, retries make things worse
                    5. some thing to borrow from congestion control in networks to RPC systems?
            7. Achieving Rapid Response Times in Large Online Services, by Jeff Dean
               http://research.google.com/people/jeff/latency.html
                1. Basic Latency Reduction Techniques
                    1. Differentiated service classes
                        1. prioritized request queues in servers
                        2. prioritized network traffic
                    2. Reduce head-of-line blocking
                        1. break large requests into sequence of small requests
                    3. Manage expensive background activities
                        1. e.g. log compaction in distributed storage systems
                        2. rate limit activity
                        3. defer expensive activity until load is lower
                2. Synchronized Disruption
                    1. randomize background tasks time when each machine performs these tasks?
                    2. no, better to synchronize the disruptions
                3. Latency Tolerating Techniques
                    1. Cross request adaptation
                        –examine recent behavior
                        –take action to improve latency of future requests
                        –typically relate to balancing load across set of servers
                        –time scale: 10s of seconds to minutes
                    2. Within request adaptation
                        - cope with slow subsystems in context of higher level request
                        –time scale: right now, while user is waiting
                    3. Fine-Grained Dynamic Partitioning
                        - more than 1 partition per machine (often 10-100/machine)
                        - Speeds Failure Recovery
                    4. Load Balancing
                        - Can shed load in few percent increments
                    5. Selective Replication
                        - Find heavily used items and make more replicas
                    6. Latency-Induced Probation
                        - Initiate corrective action
                    7. Handling Within-Request Variability
                        - Canary Requests
                        - Backup Requests
                4. Backup Requests: efficient to reduce long tail percentile
                    1. e.g. send a "backup request" after the 95th percentile latency
                    2. with Cross-Server Cancellation
                    3. Can handle Reed-Solomon reconstruction similarly
                5. Tainted Partial Results
                    1. Many systems can tolerate inexact results
                    2. Design to proactively abandon slow subsystems
                        - important to mark such results as tainted in caches
                6. the summary: Collection of techniques
                    –general good engineering practices
                        • prioritized server queues, careful management of background activities
                    –cross-request adaptation
                        • load balancing, micro-partitioning
                    –within-request adaptation
                        • backup requests, backup requests w/ cancellation, tainted results
            8. Heroku's Ugly Secret: The story of how the cloud-king turned its back on Rails
               https://news.ycombinator.com/item?id=5215884
                1. Jeff Dean tail at scale ... "this is an incredibly effective way to DoS yourself"
                2. "Just routing by least connections is one option"

    2. FAST16 Spinning Disks and Their Cloudy Future about tail latency
       https://www.usenix.org/conference/fast16/technical-sessions/presentation/brewer
       and the white paper: http://research.google.com/pubs/pub44830.html
        1. read and logged before

    4. the papers related
        1. The Tail at Scale: How to Predict It?    [2016, 0 refs]
           https://www.usenix.org/system/files/conference/hotcloud16/hotcloud16_nguyen.pdf
            1. predict tail latency by a model, using only the mean and variance of the task response time
               prediction errors for 99th percentile request latency are consistently within 10%
            2. key designs & findings
                1. find that the tail behavior of a task mapped to a subsystem can be captured by
                   a generalized exponential distribution function in the high load region,
                   which uses the mean and variance of the task response time as input
            3. my comments
                1. I'm not sure whether tail latency in real systems can really be capture by such statistics model
                2. the evaluation workload looks unable to generalize
        2. DeTail: Reducing the Flow Completion Time Tail in Datacenter Networks (Facebook)    [2012, 185 refs]
           https://people.eecs.berkeley.edu/~dzats/detail.pdf
            1. older than Jeff Dean's "The Tail at Scale" paper.
               the approach focus on network stack
               it exploit cross-layer information, to reduce time tail by
                reduce packet drops,
                prioritize latency-sensitive flows,
                and evenly distribute network load
            2. key designs & findings
                1. by reducing the long flow completion tail, the app gains better worst-case performance from the network
                2. network latency varies
                    1. congestion causes them to vary by 2 orders of magnitude
                    2. because workflow uses many flows, long delay for lots of page creation is possible
                    3. causes of long tails
                        1. packet loss and retransmissions
                        2. absence of prioritization
                        3. uneven load balancing
                3. DeTail solution
                    1. At the link layer, DeTail uses port buffer occupancies to construct a lossless fabric
                       By responding quickly, lossless fabrics ensure that packets are never dropped due to flash congestion.
                    2. At the network layer, DeTail performs per-packet adaptive load balancing of packet routes
                       At every hop, switches use the congestion information obtained from port buffer occupancies to dynamically pick a packet's next hop
                    3. Since packets are no longer lost due to congestion,
                       DeTail's transport protocol relies upon congestion notifications derived from port buffer occupancies
                    4. DeTail allows applications to specify flow priorities
        3. Mechanisms and Architectures for Tail-Tolerant System Operations in Cloud    [2014, 7 refs]
           https://www.usenix.org/system/files/conference/hotcloud14/hotcloud14-lu.pdf
            1. wrap cloud provisioning APIs, to reduce their long tail (not app req's long tail?)
            2. key designs
                1. hedged requests
                2. retry, reallocate, force fail/completion
        4. RepNet: Cutting Tail Latency in Data Center Networks with Flow Replication    [2014, 0 refs]
           https://arxiv.org/pdf/1407.1239.pdf
            1. RetNet is an app layer transport. it replicate flows to avoid congestion path, so that tail latency is better
            2. key designs & findings
                1. the reason of long tail latency
                    1. elephant flows and mice flows co-exist
                    2. even in high bisection topologies, the core part of the network is still over-subscribed
                       this makes congestion likely to happen
                2. use flow replication to reap the path diversity gains
                3. ReSYN only replicates SYN packets
                   ReFlow replicates the entire flow
                4. implemented on node.js
                5. efficient multipath routing in data center networks is worth further investigation
        5. Reducing Web Latency: the Virtue of Gentle Aggression (Google)    [2013, 86 refs]
           https://nsl.cs.usc.edu/~tobiasflach/publications/Flach_Latency.pdf
            1. a novel loss recovery mechanisms for TCP using redundant transmissions to minimize timeout-driven recovery
               evaluted on Google production network, yields a 23% decrease in the mean and 47% in 99th percentile latency over today's TCP
            2. key designs & findings
                1. TCP's current mechanisms fundamentally limit latency improvements
                    1. while connections with no loss complete close to the ideal latency of one round-trip time
                       TCP's timeoutdriven recovery causes transfers with loss to take five times longer on average
                2. multi-stage architecture, each involve increasing levels of aggression
                    1. Reactive: transmits one additional packet per window for a small fraction of flows
                        1. requires only sender side changes
                        2. Reactive can be deployed on client-facing side of frontends to speed Web responses;
                        3. allows a sender to quickly detect tail losses without waiting for an RTO
                    2. Corrective: transmits one additional packet per window for all flows
                        1. requires both sender and receiver changes
                        2. Corrective can apply equally to both client and backend connections
                        3. The sender transmits extra FEC packets so that the receiver can repair a small number of losses
                    3. Proactive: duplicates the window for a small portion of flows
                        1. Proactive is applied selectively on certain transactions in the backend;
                        2. proactively transmitting copies of each TCP segment
                3. implemented in Linux Kernel
        6. Speeding up Distributed Request-Response Workflows (Microsoft)    [2013, 34 refs]
           http://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p219.pdf
            1. works on Bing, Kwiken manages the tail latency improvements and cost budges. Jeff Dean's "The Tail at Scale" is already considered. good to read
               the 99th percentile of latency improves by over 50% when just 0.1% of the responses are allowed to have partial results
               and by over 40% for 25% of the services when just 5% extra resources are used for reissues
            2. key designs
                1. improve tail latency by employing these core techniques
                    1. reissuing laggards elsewhere in the cluster
                    2. new policies to return incomplete results
                    3.  speeding up laggards by giving them more resources
                2. Although Jeff Dean's "The Tail at Scale", applying them to reduce end-to-end latency is difficult
                    1. different stages benefit differently from different techniques
                        1. also, Latencies in individual stages are uncorrelated
                                 Latencies across stages are mostly uncorrelated
                            except when running on the same machine
                    2. end-to-end effects of local actions depend on topology of the workflow
                       reducing latency of stages usually off the critical path does not improve end-to-end latency
                    3. many techniques have overhead, such as increased resource usage when reissuing a request
                3. Kwiken, a framework that takes an end-to-end view of latency improvements and costs, by DAG
                    1. the median workflow in production at Bing has 15 stages and 10% of the stages process the query in parallel on 1000s of servers
                       In all, we report results from thousands of stages and hundreds of thousands of servers
                    2. casts each stage as a variance-response curve to apportion overall budget appropriately across stages
                    3. At the stage/local level, it selects a policy that minimizes the variance of the stage latency.
                       At the workflow/global level, it combines these local policies to minimize the end-to-end latency
                    4. burst losses in the network are responsible for a significant fraction of high latencies
        7. TimeTrader: Exploiting Latency Tail to Save Datacenter Energy for Online Search    [2015, 2 refs]
           https://arxiv.org/ftp/arxiv/papers/1503/1503.05338.pdf
           http://www.microarch.org/micro48/files/slides/F1-2.pdf
            1. TimeTrader to reduce energy by exploiting the latency slack in the subcritical replies which arrive before the deadline
               TimeTrader saves 15-19% and 41-49% energy at 90% and 30% loading
                1. it saves energy rather than reduce tail latency
            2. key designs
                1. the two core ideas
                    1. TimeTrader trades time across system layers, borrowing from the network layer and lending to the compute layer
                        1. leverage the wellknown Explicit Congestion Notification (ECN) in IP [32] and TCP timeouts
                           to inform the leaves whether a request encountered timeout or congestion in the network and hence does not have slack
                        2. use power management schemes with response times of 1 ms
                    2. leverage Earliest Deadline First (EDF) scheduling, to decouple critical requests from the queuing delays of subcritical requests
                2. to determine the slack and slowdown
                    1. slowdown =(total slack – RAPLlatency)*scale/compute budget
                    2. to set the core's speed as per the slowdown factor, we employ RAPL

3. readings: FAST16 papers
    1. Flash Reliability in Production: The Expected and the Unexpected (Google)    [2016, 6 refs]
       https://www.usenix.org/node/194415
        1. field study over 6 years of production use at google datacenters
           those type of trace/measures/access/workload/failure/pattern/reliability study papers occurs every a few years
           good to use as a reference material
        2. designs
            1. differnet error types
                1. transparent errors
                    1. correctable error: During a read operation an error is detected and corrected
                    2. read error: A read operation experiences a (non-ECC) error, but after retrying it succeeds
                    3. write error: A write operation experiences an error, but after retrying the operation succeeds
                    4. erase error: An erase operation on a block fails
                2. non-transparent errors:
                    1. Uncorrectable error (UE): A read operation encounters more corrupted bits than the ECC can correct
                    2. Final read error: A read operation experiences an error, and even after retries the error persists
                    3. Final write error: A write operation experiences an error that persists even after retries
                    4. Meta error: An error accessing drive-internal metadata
                    5. Timeout error: An operation timed out after 3 seconds
        3. key findings
            0. some summaries
                1. RBER is not a good reliability predictor
                   UEs has no relation with number of reads, or RBER
                2. SLC drives, though market-considered highend, are not more reliable than MLC drivers
                3. a drive with a large number of factory bad blocks has a higher chance of developing more bad blocks in the field
                4. age (independent of PE cycles / wear-out) and prior errors are good predictors for impending failures
                5. flash drives offer lower field replacement rates than HDD, but have significantly higher UE rates
            1. raw bit error rates (RBER) grow at a much slower rate with wear-out,
               rather than the exponential rate commonly assumed
                1. RBER rates under wear-out vary greatly across driver models, even when they are similar at low PE cycles
                   so, wear-out is not predictive of uncorrectable errors or other error modes
                2. the RBER rates under wear-out increase smoothly near linear, and rapid increase at 3X the vendor PE cycle limit
                3. RBER has significant correlation with device age (independent of PE cycles / cell wear-out)
                    1. also, RBER experienced in the previous month is very predictive of future RBER
                    2. but, there is no significant correlation between uncorrectable errors and RBER
                    3. read, write, erase count, timeout error, etc, has very low or in-consistent correlation with RBER
                4. smaller lithography might explain the higher RBER for the eMLC drives compared to the MLC drives
            2. The widely used metric UBER (uncorrectable bit error rate) is not a meaningful metric
                1. because UEs are not correlated with the number of reads
                2. also, we see no correlation between RBER and UE incidence
                3. how does UE correlate?
                    1. UE probability continuously increases with age, slow and linear
                    2. final write errors, meta errors, erase errors, and UEs in the prior month increase UE probability significantly
                    3. the authors said:
                        "In fact, we have work in progress showing that
                        standard machine learning techniques can predict uncorrectable errors
                        based on age and prior errors
                        with an interesting accuracy"
            3. We see no evidence that higher-end SLC drives are more reliable than MLC drives within typical drive lifetimes
                    1. RBER rates for the MLC models are orders of magnitudes higher than for the SLC models
                       but will it translate to different user-visible, non-transparent errors?
                        1. RBER doesn't have correlation with UEs
                    2. Tables 2 and 5 show that SLC drives do not perform better for more visible reliability measurements
                        1. SLC drives don't have lower repair or replacement rates,
                           and don't typically have lower rates of non-transparent errors
            4. Comparing with traditional hard disk drives, flash drives have a significantly lower replacement rate in the field,
               however, they have a higher rate of uncorrectable errors
                1. The annual replacement rates of hard disk drives have previously been reported to be 2-9%
                   which is high compared to the 4-10% of flash drives we see being replaced in a 4 year period
                    1. However, flash drives are less attractive when it comes to their error rates
                        1. More than 20% of flash drives develop uncorrectable errors in a four year period,
                           30-80% develop bad blocks and 2-7% of them develop bad chips
                        2. previous work on HDDs reports that only 3.5% of disks in a large population developed bad sectors in a 32 months period
                            1. considering the number of sectors on a hard disk is orders of magnitudes
                               larger than the number of either blocks or chips on a solid state drive
            5. more findings
                1. transparent and non-transparent errors
                    1. final read errors are almost exclusively due to bit corruption byond what ECC can correct
                       final read errors are around two orders of magnitude more frequent than other non-transparent errors
                    2. correctable errors are the most common type of transparent errors, the next is write errors and erase errors
                2. RBER (raw bit error rate)
                    1. vendors doens't consistently out-perform others in RBER (MLC vs MLC, SLC vs SLC)
                    2. the field RBER rates are higher than in-house projections based on accelerated life tests
                3. Bad blocks
                    1. The drives in our study declare a block bad
                       after a final read error, a write error, or an erase error,
                       and consequently remap it
                    2. the median number of bad blocks for drives with bad blocks is 2-4, depending on the model.
                       However, if drives develop more than that they typically develop many more
                    3. most bad blocks are discovered in a non-transparent way, in a read operation
                    4. Bad blocks are common: 30-80% of drives develop at least one in the field
                    5. nearly all drives (> 99% for most models) are shipped with factory bad blocks
                        1. the number of factory bad blocks shows a correlation with the number of bad blocks the drive will develop in the field,
                           as well as a few other errors that occur in the field
                4. Bad chips
                    1. around 2-7% of drives develop bad chips during the first four years of their life
                        1. if without mechanisms for mapping out bad chips,
                           would require repairs or be returned to the vendor
                    2. across all models,
                       around two thirds of bad chips are declared bad after reaching the 5% threshold on bad blocks,
                       the other third  fter exceeding the threshold on the number of days with errors
                5. Drive repair and replacement
                    1. A drive is being swapped and enters repairs if it develops issues that require manual intervention by a technician
                    2. most models see around 5% of their drives permanently removed from the field within 4 years after being deployed,
                       while the worst models (MLC-B and SLC-B) see around 10% of their drives replaced
        n. related readings
            1. MLC vs eMLC vs SLC
                1. Flash Memory Explained: MLC vs. eMLC vs. SLC vs. TLC
                   http://www.tomsitpro.com/articles/flash-data-center-advantages,2-744-2.html
                    1. The cells are usually grouped into sections called "erase blocks."
                    2. One term frequently used to categorize "lifetime" is P/E
                       P/E refers to a Program/Erase cycle
                    3. There are four types of NAND flash: MLC vs. eMLC vs. SLC vs. TLC
                        1. SLC -- Single Level Cell: the most expensive, longest lived (high P/E), and generally fastest
                            1. bits are stored only as 2 voltage levels, or a "1" or "0.", less data is stored per cell
                        2. MLC -- Multi-Level Cell: is consumer grade and used in phones, cameras, and USB sticks
                            1. The stored charge in MLC may be interpreted as a variety of values, 0 to 3, or 4 possible states
                               and may store 2 bits
                            2. With shorter lifetimes, usually 10x less than SLC
                            3. the cost is 2- 4x less than SLC
                            4. but with lower write speeds
                            5. MLC typically uses some form of error correction code per block
                        3. eMLC -- Enterprise (grade) Multi-Level Cell: is MLC with longer life
                            1. usually because of an advanced controller operating the cell
                               and error recovery techniques, construction density,
                               or some combination of the two
                            3. TLC -- Triple Level Cell: championed by Samsung
                                1. TLC has higher power and error correction requirements, and higher wear levels
                                2. TLC is targeted at environments with predominant read uses
                                3. and has not been commonly used
                    4. NOR vs. NAND Architectures: memory cells of both an EEPROM memory array and a flash memory array
                                                   are typically arranged into either a "NOR" or "NAND" architecture
                        1. NOR architecture -- each cell directly coupled to a bit line, allows true random access
                        2. NAND architecture -- cells coupled into "strings" of cells,
                            1. such that each cell is coupled indirectly to a bit line
                               and requires activating the other cells of the string for access
                            2. Most solid-state drives, USB flash, and memory cards use NAND flash
                                1. Erasing, usually a slow process, is much faster in flash than non-flash EEPROM,
                                   because of the large block sizes used in flash
            1. what is "accelerated life tests"
                1. wiki: Accelerated life testing
                   https://en.wikipedia.org/wiki/Accelerated_life_testing
                    1. to derive projections for device reliability in the field, by
                       testing a product by subjecting it to conditions (stress, strain, temperatures, voltage, vibration rate, pressure etc.)
                       in excess of its normal service parameters

    2. Environmental Conditions and Disk Reliability in Free-cooled Datacenters (Microsoft)    [2016, 1 refs]
       https://www.usenix.org/node/194413
        1. Best Paper Award.
           data from 9 hyperscale datacenters for 1.5 to 4 years.
            1. but are they free-colling datacenters?
        2. designs
            1. key findings/learnings
                1. relative humidity seems to have a dominant impact on component failures
                    1. high relative humidity may cause significant temporal clustering of disk failures
                    2. the disks are exposed to high humidity in the first summer, but may fail at the second
                    3. high internal temperature does not directly correlate to the high range of AFRs (greater than 3%)
                    4. higher temperature leads to lower relative humidity, given a constant amount of moisture in the air
                        1. server designs that place disks in the back of enclosures can reduce the disk failure rate significantly
                        2. may consider running datacenters somewhere hotter in summer
                2. disk failures increase signifi-cantly when operating at high relative humidity, due to controller/adaptor malfunction
                3. software availability techniques can mask them and overweight the cost
            2. other findings
                1. disk drive failures dominate with 76%–95% (89% on average) of all hardware component failures
            3. a new model of disk lifetime as a function of both temperature and humidity
                1. by extending the Arrhenius model to calculate the disk lifetime acceleration factor
                2. see "Modeling Lifetime in Modern DCs" for detailed equations
            4. strike the right tradeoff between energy consumption, hardware reliability, cost, and quality of service
                1. but how? ... cost models?

1. readings: FAST16 papers
    1. Isotope: Transactional Isolation for Block Storage (Google)    [2016, 0 refs]
       https://www.usenix.org/node/194397
        1. implement ACID transaction & MVCC & concurrency control at block-level store is easier (100s line of code),
           and ease the implementation of upper-level KV/DB/B-tree/FS/etc store
           need to wait (perhaps many years) to see whether this can drive a design shift into the industry
            P.S. Ceph does provide block-level transaction, embedded inside the code.
                 Is that something to leverage?
            P.S. WinAzure Storage stream layer (append-only) looks easy to implement transaction
                 is that something to leverage?
            1. this paper's MVCC transaction implementation is easy to understand, can be borrowed as a reference
               also, there are a lot of detailed optimizations in later sections
        2. key designs
            1. Isotope is implemented as a kernel module, beginTX/endTX expose the transaction API
            2. storage structure & transaction implementation
                1. log-structured, store persistent log,
                   use a in-memory multiversion index to provide consistent point-in-time snapshots
                    1. the index is persistent by metadata log + checkpoints
                    2. The index is a hashtable that maps each logical address to a linked list of its existing versions, in timestamp order
                        1. authors plan to apply compact, concurrent maps [28] in future
                2. read execute against this snapshot
                3. writes are buffered in RAM, flush to log on commit
                4. transactions are ordered by timestamp counter
                    1. navie MVCC implementations: for MVCC, the in-memory index is consulted
                       to check whether any block previously read by the transaction
                       now has a greater timestamp than the transaction's start timestamp
                        1. problem: to fine-grained conflict detection, the in-memory index has to be very large
                    2. by conflict window
                        1. For strict serializability, the transaction T aborts if any committed transaction in its conflict window
                           modified an address that T read; else, T commits.
                        2. For snapshot isolation, the transaction T aborts if any committed transaction in its conflict window
                           modified an address that T wrote; else, T commits
                        3. timestamp counter increase without holes, so it can be used as an array of slots to hold transaction actions
                           for later conflict checks
            3. limitations
                1. upper-level see some information lost due to transaction is done in lower-level
                   lower-level see some information lost due to cannot leverage knowledge of upper-level
                2. the paper provides some mitigations
            4. API designs
                1. mark_accessed() allow app's to mark intra-block modified range, so that conflict detection is easier
                2. please_cache() lets app request Isotope to cache specific blocks in RAM
                3. takeoverTX() to pass transaction handle ownership from one process to another
        3. evaluations
            1. the disk and SSD benchmarks have similar throughput? what SSD benefits ...
            2. IsoHT and IsoBT outperform LevelDB for random fill, random read, YCSB workload-A, while providing strong consistency
               but LevelDB delete is much faster than them

    2. Uncovering Bugs in Distributed Storage Systems during Testing (Not in Production!) (Microsoft)    [2016, 0 refs]
       https://www.usenix.org/node/194443
        1. a new methodology for testing distributed systems, successful use in Azure Storage (and many other Azure's)
           the method is testing based, use P# runtime to inject & track nondeterminism to test the system
           a bit huge effort and invasion to the original system is needed to use this methodology
            1. generally, many testing system works by injecting nondeterminism, e.g. network messaging
               schedule the test case combination, and trace what happened when bug is triggered.
            2. a bit similar: Netflix Molly: https://people.eecs.berkeley.edu/~palvaro/molly.pdf
        2. key designs
            1. in general
                1. the methodology is based on P#, and supports C#/.NET programming
                    1. during test, P# runtime is aware of all sources of nondeterminism that were declared during modeling
                    2. P# generates a trace when bug discovered, to capture bug reproduce (and its environment)
                       the P# trace also provides a global order of all communication events
                2. to test, programmer needs add to the original system
                    1. a model of the nondeterministic execution environment of the system
                        1. the developer needs to modify the original system to send message via P#
                    2. a test harness that drives the system towards interesting behaviors
                        1. the harness is essentially a model of the environment of the system, like stub class in testing
                           to explicitly declare all sources of nondeterminism in the system using P#
                    3. safety or liveness specifications
            2. the effort is a bit huge to use this method
                1. need to invade into the original code
                2. need to write stub class
                3. need to model environment nondeterminism
                3. need to write the safety and liveness checks
            4. cost analysis
                1. the effort is non-trivial, but acceptable given the serious bugs found
        n. related readings
            1. Heisenbugs
               https://en.wikipedia.org/wiki/Heisenbug
                1. a heisenbug is a software bug that seems to disappear or alter its behavior when one attempts to study it
            2. What Bugs Live in the Cloud? A Study of 3000+ Issues in Cloud Systems    [2014, 20 refs]
               http://ucare.cs.uchicago.edu/pdf/socc14-cbs.pdf
                1. a study from bug repositories of Hadoop MapReduce, HDFS, HBase, Cassandra, ZooKeeper and Flume, from 2011 to 2014
                   more focus on "vital" issues
                2. the conslusion/summaries are a bit too trivial
                   what did we learn from those bug statitics?
            3. TaxDC: A Taxonomy of Non-Deterministic Concurrency Bugs in Datacenter Distributed Systems    [2016, 2 refs]
               http://ucare.cs.uchicago.edu/pdf/asplos16-TaxDC.pdf
                1. published by the same colleges, share some authors with the above paper
                   "What Bugs Live in the Cloud? A Study of 3000+ Issues in Cloud Systems"
                2. studied 104 distributed concurrency bugs, from Cassandra, Hadoop MapReduce, HBase and ZooKeeper
                3. key findings
                    1. 63% of  distributed concurrency (DC) bugs surface
                       in the presence of hardware faults such as machine crashes (and reboots),
                       network delay and partition (timeouts), and disk errors
                    2. 53% of the DC bugs generate explicit first errors, including local exceptions and global wrong messages,
                       and the remaining 47% DC bugs lead to silent errors
                        1. implying that sanity checks already in software can be harnessed, for the 53%
                    3. More than 60% of DC bugs are triggered by a single untimely message delivery that
                       commits order violation or atomicity violation, with regard to other messages or computation
                    4. Most DC bugs are fixed by better handling the triggering timing,
                       most of which do not introduce new computation logic
                       — they ignore or delay messages, re-use existing handlers, and cancel computation (40%)
                    5. The timing conditions of most DC bugs only involve one to three messages, nodes, and protocols (>90%).
                       Most DC bugs are mostly triggered by only one untimely event (92%)

3. readings: FAST16 papers
    1. Flash Reliability in Production: The Expected and the Unexpected (Google)    [2016, 6 refs]
       https://www.usenix.org/node/194415
        1. field study over 6 years of production use at google datacenters
           those type of trace/measures/access/workload/failure/pattern/reliability study papers occurs every a few years
           good to use as a reference material
        2. designs
            1. differnet error types
                1. transparent errors
                    1. correctable error: During a read operation an error is detected and corrected
                    2. read error: A read operation experiences a (non-ECC) error, but after retrying it succeeds
                    3. write error: A write operation experiences an error, but after retrying the operation succeeds
                    4. erase error: An erase operation on a block fails
                2. non-transparent errors:
                    1. Uncorrectable error (UE): A read operation encounters more corrupted bits than the ECC can correct
                    2. Final read error: A read operation experiences an error, and even after retries the error persists
                    3. Final write error: A write operation experiences an error that persists even after retries
                    4. Meta error: An error accessing drive-internal metadata
                    5. Timeout error: An operation timed out after 3 seconds
        3. key findings
            0. some summaries
                1. RBER is not a good reliability predictor
                   UEs has no relation with number of reads, or RBER
                2. SLC drives, though market-considered highend, are not more reliable than MLC drivers
                3. a drive with a large number of factory bad blocks has a higher chance of developing more bad blocks in the field
                4. age (independent of PE cycles / wear-out) and prior errors are good predictors for impending failures
                5. flash drives offer lower field replacement rates than HDD, but have significantly higher UE rates
            1. raw bit error rates (RBER) grow at a much slower rate with wear-out,
               rather than the exponential rate commonly assumed
                1. RBER rates under wear-out vary greatly across driver models, even when they are similar at low PE cycles
                   so, wear-out is not predictive of uncorrectable errors or other error modes
                2. the RBER rates under wear-out increase smoothly near linear, and rapid increase at 3X the vendor PE cycle limit
                3. RBER has significant correlation with device age (independent of PE cycles / cell wear-out)
                    1. also, RBER experienced in the previous month is very predictive of future RBER
                    2. but, there is no significant correlation between uncorrectable errors and RBER
                    3. read, write, erase count, timeout error, etc, has very low or in-consistent correlation with RBER
                4. smaller lithography might explain the higher RBER for the eMLC drives compared to the MLC drives
            2. The widely used metric UBER (uncorrectable bit error rate) is not a meaningful metric
                1. because UEs are not correlated with the number of reads
                2. also, we see no correlation between RBER and UE incidence
                3. how does UE correlate?
                    1. UE probability continuously increases with age, slow and linear
                    2. final write errors, meta errors, erase errors, and UEs in the prior month increase UE probability significantly
                    3. the authors said:
                        "In fact, we have work in progress showing that
                        standard machine learning techniques can predict uncorrectable errors
                        based on age and prior errors
                        with an interesting accuracy"
            3. We see no evidence that higher-end SLC drives are more reliable than MLC drives within typical drive lifetimes
                    1. RBER rates for the MLC models are orders of magnitudes higher than for the SLC models
                       but will it translate to different user-visible, non-transparent errors?
                        1. RBER doesn't have correlation with UEs
                    2. Tables 2 and 5 show that SLC drives do not perform better for more visible reliability measurements
                        1. SLC drives don't have lower repair or replacement rates,
                           and don't typically have lower rates of non-transparent errors
            4. Comparing with traditional hard disk drives, flash drives have a significantly lower replacement rate in the field,
               however, they have a higher rate of uncorrectable errors
                1. The annual replacement rates of hard disk drives have previously been reported to be 2-9%
                   which is high compared to the 4-10% of flash drives we see being replaced in a 4 year period
                    1. However, flash drives are less attractive when it comes to their error rates
                        1. More than 20% of flash drives develop uncorrectable errors in a four year period,
                           30-80% develop bad blocks and 2-7% of them develop bad chips
                        2. previous work on HDDs reports that only 3.5% of disks in a large population developed bad sectors in a 32 months period
                            1. considering the number of sectors on a hard disk is orders of magnitudes
                               larger than the number of either blocks or chips on a solid state drive
            5. more findings
                1. transparent and non-transparent errors
                    1. final read errors are almost exclusively due to bit corruption byond what ECC can correct
                       final read errors are around two orders of magnitude more frequent than other non-transparent errors
                    2. correctable errors are the most common type of transparent errors, the next is write errors and erase errors
                2. RBER (raw bit error rate)
                    1. vendors doens't consistently out-perform others in RBER (MLC vs MLC, SLC vs SLC)
                    2. the field RBER rates are higher than in-house projections based on accelerated life tests
                3. Bad blocks
                    1. The drives in our study declare a block bad
                       after a final read error, a write error, or an erase error,
                       and consequently remap it
                    2. the median number of bad blocks for drives with bad blocks is 2-4, depending on the model.
                       However, if drives develop more than that they typically develop many more
                    3. most bad blocks are discovered in a non-transparent way, in a read operation
                    4. Bad blocks are common: 30-80% of drives develop at least one in the field
                    5. nearly all drives (> 99% for most models) are shipped with factory bad blocks
                        1. the number of factory bad blocks shows a correlation with the number of bad blocks the drive will develop in the field,
                           as well as a few other errors that occur in the field
                4. Bad chips
                    1. around 2-7% of drives develop bad chips during the first four years of their life
                        1. if without mechanisms for mapping out bad chips,
                           would require repairs or be returned to the vendor
                    2. across all models,
                       around two thirds of bad chips are declared bad after reaching the 5% threshold on bad blocks,
                       the other third  fter exceeding the threshold on the number of days with errors
                5. Drive repair and replacement
                    1. A drive is being swapped and enters repairs if it develops issues that require manual intervention by a technician
                    2. most models see around 5% of their drives permanently removed from the field within 4 years after being deployed,
                       while the worst models (MLC-B and SLC-B) see around 10% of their drives replaced
        n. related readings
            1. MLC vs eMLC vs SLC
                1. Flash Memory Explained: MLC vs. eMLC vs. SLC vs. TLC
                   http://www.tomsitpro.com/articles/flash-data-center-advantages,2-744-2.html
                    1. The cells are usually grouped into sections called "erase blocks."
                    2. One term frequently used to categorize "lifetime" is P/E
                       P/E refers to a Program/Erase cycle
                    3. There are four types of NAND flash: MLC vs. eMLC vs. SLC vs. TLC
                        1. SLC -- Single Level Cell: the most expensive, longest lived (high P/E), and generally fastest
                            1. bits are stored only as 2 voltage levels, or a "1" or "0.", less data is stored per cell
                        2. MLC -- Multi-Level Cell: is consumer grade and used in phones, cameras, and USB sticks
                            1. The stored charge in MLC may be interpreted as a variety of values, 0 to 3, or 4 possible states
                               and may store 2 bits
                            2. With shorter lifetimes, usually 10x less than SLC
                            3. the cost is 2- 4x less than SLC
                            4. but with lower write speeds
                            5. MLC typically uses some form of error correction code per block
                        3. eMLC -- Enterprise (grade) Multi-Level Cell: is MLC with longer life
                            1. usually because of an advanced controller operating the cell
                               and error recovery techniques, construction density,
                               or some combination of the two
                            3. TLC -- Triple Level Cell: championed by Samsung
                                1. TLC has higher power and error correction requirements, and higher wear levels
                                2. TLC is targeted at environments with predominant read uses
                                3. and has not been commonly used
                    4. NOR vs. NAND Architectures: memory cells of both an EEPROM memory array and a flash memory array
                                                   are typically arranged into either a "NOR" or "NAND" architecture
                        1. NOR architecture -- each cell directly coupled to a bit line, allows true random access
                        2. NAND architecture -- cells coupled into "strings" of cells,
                            1. such that each cell is coupled indirectly to a bit line
                               and requires activating the other cells of the string for access
                            2. Most solid-state drives, USB flash, and memory cards use NAND flash
                                1. Erasing, usually a slow process, is much faster in flash than non-flash EEPROM,
                                   because of the large block sizes used in flash
            1. what is "accelerated life tests"
                1. wiki: Accelerated life testing
                   https://en.wikipedia.org/wiki/Accelerated_life_testing
                    1. to derive projections for device reliability in the field, by
                       testing a product by subjecting it to conditions (stress, strain, temperatures, voltage, vibration rate, pressure etc.)
                       in excess of its normal service parameters

    2. Environmental Conditions and Disk Reliability in Free-cooled Datacenters (Microsoft)    [2016, 1 refs]
       https://www.usenix.org/node/194413
        1. Best Paper Award.
           data from 9 hyperscale datacenters for 1.5 to 4 years.
            1. but are they free-colling datacenters?
        2. designs
            1. key findings/learnings
                1. relative humidity seems to have a dominant impact on component failures
                    1. high relative humidity may cause significant temporal clustering of disk failures
                    2. the disks are exposed to high humidity in the first summer, but may fail at the second
                    3. high internal temperature does not directly correlate to the high range of AFRs (greater than 3%)
                    4. higher temperature leads to lower relative humidity, given a constant amount of moisture in the air
                        1. server designs that place disks in the back of enclosures can reduce the disk failure rate significantly
                        2. may consider running datacenters somewhere hotter in summer
                2. disk failures increase signifi-cantly when operating at high relative humidity, due to controller/adaptor malfunction
                3. software availability techniques can mask them and overweight the cost
            2. other findings
                1. disk drive failures dominate with 76%–95% (89% on average) of all hardware component failures
            3. a new model of disk lifetime as a function of both temperature and humidity
                1. by extending the Arrhenius model to calculate the disk lifetime acceleration factor
                2. see "Modeling Lifetime in Modern DCs" for detailed equations
            4. strike the right tradeoff between energy consumption, hardware reliability, cost, and quality of service
                1. but how? ... cost models?

1. readings: FAST16 papers
    1. Isotope: Transactional Isolation for Block Storage (Google)    [2016, 0 refs]
       https://www.usenix.org/node/194397
        1. implement ACID transaction & MVCC & concurrency control at block-level store is easier (100s line of code),
           and ease the implementation of upper-level KV/DB/B-tree/FS/etc store
           need to wait (perhaps many years) to see whether this can drive a design shift into the industry
            P.S. Ceph does provide block-level transaction, embedded inside the code.
                 Is that something to leverage?
            P.S. WinAzure Storage stream layer (append-only) looks easy to implement transaction
                 is that something to leverage?
            1. this paper's MVCC transaction implementation is easy to understand, can be borrowed as a reference
               also, there are a lot of detailed optimizations in later sections
        2. key designs
            1. Isotope is implemented as a kernel module, beginTX/endTX expose the transaction API
            2. storage structure & transaction implementation
                1. log-structured, store persistent log,
                   use a in-memory multiversion index to provide consistent point-in-time snapshots
                    1. the index is persistent by metadata log + checkpoints
                    2. The index is a hashtable that maps each logical address to a linked list of its existing versions, in timestamp order
                        1. authors plan to apply compact, concurrent maps [28] in future
                2. read execute against this snapshot
                3. writes are buffered in RAM, flush to log on commit
                4. transactions are ordered by timestamp counter
                    1. navie MVCC implementations: for MVCC, the in-memory index is consulted
                       to check whether any block previously read by the transaction
                       now has a greater timestamp than the transaction's start timestamp
                        1. problem: to fine-grained conflict detection, the in-memory index has to be very large
                    2. by conflict window
                        1. For strict serializability, the transaction T aborts if any committed transaction in its conflict window
                           modified an address that T read; else, T commits.
                        2. For snapshot isolation, the transaction T aborts if any committed transaction in its conflict window
                           modified an address that T wrote; else, T commits
                        3. timestamp counter increase without holes, so it can be used as an array of slots to hold transaction actions
                           for later conflict checks
            3. limitations
                1. upper-level see some information lost due to transaction is done in lower-level
                   lower-level see some information lost due to cannot leverage knowledge of upper-level
                2. the paper provides some mitigations
            4. API designs
                1. mark_accessed() allow app's to mark intra-block modified range, so that conflict detection is easier
                2. please_cache() lets app request Isotope to cache specific blocks in RAM
                3. takeoverTX() to pass transaction handle ownership from one process to another
        3. evaluations
            1. the disk and SSD benchmarks have similar throughput? what SSD benefits ...
            2. IsoHT and IsoBT outperform LevelDB for random fill, random read, YCSB workload-A, while providing strong consistency
               but LevelDB delete is much faster than them

    2. Uncovering Bugs in Distributed Storage Systems during Testing (Not in Production!) (Microsoft)    [2016, 0 refs]
       https://www.usenix.org/node/194443
        1. a new methodology for testing distributed systems, successful use in Azure Storage (and many other Azure's)
           the method is testing based, use P# runtime to inject & track nondeterminism to test the system
           a bit huge effort and invasion to the original system is needed to use this methodology
            1. generally, many testing system works by injecting nondeterminism, e.g. network messaging
               schedule the test case combination, and trace what happened when bug is triggered.
            2. a bit similar: Netflix Molly: https://people.eecs.berkeley.edu/~palvaro/molly.pdf
        2. key designs
            1. in general
                1. the methodology is based on P#, and supports C#/.NET programming
                    1. during test, P# runtime is aware of all sources of nondeterminism that were declared during modeling
                    2. P# generates a trace when bug discovered, to capture bug reproduce (and its environment)
                       the P# trace also provides a global order of all communication events
                2. to test, programmer needs add to the original system
                    1. a model of the nondeterministic execution environment of the system
                        1. the developer needs to modify the original system to send message via P#
                    2. a test harness that drives the system towards interesting behaviors
                        1. the harness is essentially a model of the environment of the system, like stub class in testing
                           to explicitly declare all sources of nondeterminism in the system using P#
                    3. safety or liveness specifications
            2. the effort is a bit huge to use this method
                1. need to invade into the original code
                2. need to write stub class
                3. need to model environment nondeterminism
                3. need to write the safety and liveness checks
            3. Azure Storage vNext case study
                1. looks detailed, may worth reference later
            4. cost analysis
                1. the effort is non-trivial, but acceptable given the serious bugs found
        n. related readings
            1. Heisenbugs
               https://en.wikipedia.org/wiki/Heisenbug
                1. a heisenbug is a software bug that seems to disappear or alter its behavior when one attempts to study it
            2. What Bugs Live in the Cloud? A Study of 3000+ Issues in Cloud Systems    [2014, 20 refs]
               http://ucare.cs.uchicago.edu/pdf/socc14-cbs.pdf
                1. a study from bug repositories of Hadoop MapReduce, HDFS, HBase, Cassandra, ZooKeeper and Flume, from 2011 to 2014
                   more focus on "vital" issues
                2. the conslusion/summaries are a bit too trivial
                   what did we learn from those bug statitics?
            3. TaxDC: A Taxonomy of Non-Deterministic Concurrency Bugs in Datacenter Distributed Systems    [2016, 2 refs]
               http://ucare.cs.uchicago.edu/pdf/asplos16-TaxDC.pdf
                1. published by the same colleges, share some authors with the above paper
                   "What Bugs Live in the Cloud? A Study of 3000+ Issues in Cloud Systems"
                2. studied 104 distributed concurrency bugs, from Cassandra, Hadoop MapReduce, HBase and ZooKeeper
                3. key findings
                    1. 63% of  distributed concurrency (DC) bugs surface
                       in the presence of hardware faults such as machine crashes (and reboots),
                       network delay and partition (timeouts), and disk errors
                    2. 53% of the DC bugs generate explicit first errors, including local exceptions and global wrong messages,
                       and the remaining 47% DC bugs lead to silent errors
                        1. implying that sanity checks already in software can be harnessed, for the 53%
                    3. More than 60% of DC bugs are triggered by a single untimely message delivery that
                       commits order violation or atomicity violation, with regard to other messages or computation
                    4. Most DC bugs are fixed by better handling the triggering timing,
                       most of which do not introduce new computation logic
                       — they ignore or delay messages, re-use existing handlers, and cancel computation (40%)
                    5. The timing conditions of most DC bugs only involve one to three messages, nodes, and protocols (>90%).
                       Most DC bugs are mostly triggered by only one untimely event (92%)

3. readings: the papers around these days
    1. Peclian, which was a candidate for xarchive underlying storage media (though now we choose IBM tape library)
       Pelican: A Building Block for Exascale Cold Data Storage    [2014, 16 refs]
       https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-balakrishnan.pdf
        1. archival storage is becoming a necessarity for enterprise compliance. is there any opensource equivalent?
           Pelican designs with disk spin/not-spin (only 8% of total disks are spinning), more aggresive than disk/cpu power saving
           use disk groups to abstract away the computation complexity of scheduling disks with conflicting resource domains
        2. key designs
            1. into to Pelican
                1. Pelican is a rackscale unit for cold storage, with the mechanical, hardware and storage software stack being co-designed
                   over 5 PB of storage in a single rack, 1 GB/PB/s the entire contents of a Pelican could be transferred out every 13 days
                2. Resource right-provisioning in Pelican means only 8% of the drives can be concurrently spinning
                    1. In Pelican there is sufficient cooling to allow only 96 drives to be spun up. sufficient power for 144.
                       All disks which are not spun up are in standby mode. (1152 disks in total)
                    2. a regime where spin up latency is the modern day equivalent of disk seek latency
                    3. right-provisioning of the hardware, as sufficient to satisfy workloads
                3. key-value interface, data are immutable. first written until target utilization, then rarely read.
                   mainly servicing reads. has internal repair traffic.
            4. resource domains
                1. resource domains: a disk is using resources from several resource domains
                                     e.g. power domain, cooling domain, network bandwidth domain, PIC bus bandwidth domain
                2. hard vs soft: power and cooling are hard constraints
                                 bandwidths are soft constraints
                3. domain-conflicting: two disks are in the same resource domain
                   domain-disjoint: two disks can move independently
                4. Pelican storage stack uses the following constraints
                    (i) one disk spinning or spinning up per cooling domain;
                    (ii) two disks spinning or spinning up per power domain;
                    (iii) shared links in the PCIe interconnect hierarchy; and
                    (iv) disks located back-to-back in a tray share a vibration domain
            5. data layout
                1. use erasure coding 15 + 3; try to ensure all k+r drivers for a blob can be concurrently spun up
                2. objective: maximize the number of requests that can be concurrently served
                   i.e. lower the probability that two requets' disk set are in conflicting domains
                    1. to reduce the computional complexity, use logical groups rather than individual disks
                        1. A blob is written to k + r disks in a single randomly selected group
                        2. current group size g = 24, l = 48, l * g = 1152;
                           48 groups divide into 4 classes of 12 groups, each class is independent from each other
                    2. an off-rack metadata service, catalog, holds the mapping from a blog key to the 18 disks chosen
                3. IO scheduler
                    1. reordering: to　batch sets of operations for the same group to amortize the group spin up latency
                    2. from the evaluation part: spin up delay dominate service time when less requests/second

    2. Journaling versus Soft Updates: Asynchronous Meta-data Protection in File    [2000, 363 refs]
       https://www.ece.cmu.edu/~ganger/papers/usenix2000.pdf
        1. good paper to further understanding soft updates.
           compared to journaling, soft updates lacks metadata durability and atomicity guarantee
        2. key findings
            1. from introduction section
                1. Many of the obstacles to high performance file service have been solved in the past decade
                    1. clustering of sequential reads and writes removes the need for disk seeks between adjacent files [25][26][28]
                    2. The Co-locating FFS [13] solves the inter-file access problem for small files in the same directory are accessed together
                    3. The synchronous metadata update problem has been addressed through journaling [5][16] and Soft Updates [11]
            2. intro to Soft Updates
                1. how solve metadata update problem
                    1. by guarante blcoks are written to disk in their required order without using synchronous disk IOs
                    2. need to maintain dependency information in memory
                    3. to delay writes, soft updates uses writeback caching
                2. soft updates guarantees metdata integrity/consistency, but
                    1. it does not guarantee (as FFS does) that all meta-data operations are durable upon completion of the system call
                       Create, delete, and rename operations typically reach disk within 45 seconds of the corresponding system call,
                       but can be delayed up to 90 seconds in certain boundary cases
                    2. it does not guarantee atomicity
                    3. restarted filesystem from failure, although integrity/consistency can be ensured,
                       freed blocks and inodes may not yet be marked as free and, as such,
                       the file system may report less than the actual amount of free space
                        1. A background process, similar to fsck, restores the file system to an accurate state
                           with respect to free blocks and inodes
            3. intro to Journaling Systems
                1. write-ahead-logging.
                   it requires log and data buffers are synchronized.
                   it needs aditional (sequential) IO.
                2. journaling provides atomicity and durability
            4. other approaches
                1. Network Appliance [18] uses NVRAM to not only avoid synchronous meta-data writes, but can cache data indefinitely
                2. The Rio system [3] uses UPS power to protect a memory region, where metadata is stored
                3. Log-structured filesystem (LFS) write all modified data (both data blocks and meta-data) in a segmented log
        3. bencmarking
            1. soft updates, the async method, is almost twice the throughput on metadata intensive operations, compared to other sync methods
            2. LFFS-file, which use sync write-ahead-logging, is slower in file creating, but almost as fast as soft updates in other cases

    3. ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging    [1992, 1054 refs]
       http://cs.stanford.edu/people/chrismre/cs345/rl/aries.pdf
        1. the original paper of ARIES.
           for industrial strength, ARIES supports fuzzy checkpoints, selective and deferred restart,
                                    fuzzy image copies, media recovery, and high concurrency lock modes
        2. key designs
            1. algorithm outline is summarized in following materials
               detailed key points are in paper ppt
            2. this paper writes many more detailed optimizations
               hardly seen such long paper nowadays
        3. more materials
            1. paper ppt: http://homepages.cwi.nl/~manegold/teaching/DBtech/slides/Aries-8.pdf
                1. good to read for detailed key points.
            2. Introduction to Aries algorithm (uploaded by Akshay Kadam)
               https://www.youtube.com/watch?v=H57OtQioQgA
                1. good material
                2. key designs
                    1. log record
                        1. log record contains LSN; each page also contains pageLSN,
                           of the latest log record that updates the page
                    2. the recovery workflow
                        Analysis: scan down from most recent begin_checkpoint to last record
                                  find which pages were dirty in buffer pool
                                  find transactions that were active at crash time
                        Redo: start at smallest recLSN in dirty page table at end of Analysis.
                              redo all changes to any page that might have been dirty at crash
                              at the end of redo, DB is in same state as it was at crash
                        Undo: starting at end of log, in reverse order, undo changes of all transactions at time of crash
            3. wiki: https://en.wikipedia.org/wiki/Algorithms_for_Recovery_and_Isolation_Exploiting_Semantics
                1. ARIES (Algorithms for Recovery and Isolation Exploiting Semantics)
                   is a recovery algorithm designed to work with a no-force, steal database approach
                   was used by IBM DB2, Microsoft SQL Server and many other database systems
                2. main principles
                    1. Write-ahead logging:
                        log must be persistent before data changes are written
                    2. Repeating history during Redo:
                        when restart from crash, ARIES brings DB back to the exact state at crash
                    3. Logging changes during Undo:
                        Changes made to the database while undoing transactions are logged (CLR records)
                        to ensure such an action isn't repeated in the event of repeated restarts

5. readings: ceph related papers
    1. mClock: Handling Throughput Variability for Hypervisor IO Scheduling    [2010 OSDI VMWare, 155 refs]
       https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Gulati.pdf
        1. mClock supports proportional-share fairness subject to minimum reservations and maximum limits on the IO allocations for VMs
           dmclock in this paper is the cluster version
           dmClock is used in Ceph as the distributed QoS solution
        2. key designs
            1. mClock
                1. all requests are assigned tags and scheduled in order of their tag values
                1. each VM IO request is assigned a reservation tag R, a limit tag L, and a proportional share tag P, to track the 3 types of controls.
                2. the clocks corresponding to the tag are dynamically chosen.
                3. When new VM joins, existing tags need to be adjusted.
                4. handle bursting by idle credits
                5. handle large IO size by treating it as multiple IO requests
            2. dmClock
                1. the aggregated service received needs to be piggybacked
                2. dmClock algorithm does not require complex synchronization between the servers
        3. highlights - updated 20230403
            1. Each VM IO request is assigned three tags, one for each clock: a reservation tag R, a limit tag L, and a proportional share tag P for weight-based allocation

            2. How 2DFQ compares to mClock?
               Storage and I/O pClock [26], mClock [25], and Pisces [52] propose queue schedulers for physical storage, where several I/O requests execute concurrently. I/O request costs are much less variable than in the cloud setting, and dynamic workloads remain an open challenge [61]

            3. Table 1: Comparison of mClock with existing scheduling techniques
                1. Proportional allocation, Latency support, Reservation Support, Limit Support, Handle Capacity fluctuation

            4. the core of mClock algorithm is in equation (1) & (2).
               Satisfy R (reservation-clamped) and L (limit-clamped) VMs first, then goes to P (proportional sharing) VMs.
               P allocation is based on realtime throughput observed. That's where "clock" comes in.
                   1. Reservation - low bound. Limit - high bound.
                   2. the key advantage of mClock algorithm is, it covers all R, L, P types of throttling, i.e. Table 1

            5. Interesting paper. The true algorithm is formula (3) and Algorithm 1
                1. The core thought is to think each request has a virtual clock, and we have a physical clock.
                   Each new request sent will advance the request virtual clock by 1/limit_count.
                   Throttling is done by NOT allowing the request virtual clock to exceed the physical clock. 
                   Each IO request has all three tags, R, L, P
                2. So, a simpler solution would be simply track the past request count per second bucket using a sliding window or leaky bucket. We can then perform any R, L, P scheduling respectively
                   But compared to mClock, we would need to spend memory for tracking the buckets. mClock is instead using per request tag to incrementally track the past request count.
                3. it's then more tricky for mClock to handle
                    1) burst - allow request virtual clock to fall behind physical clock in a limited threshold
                    2) different request types - reads/writes FCFS
                    3) different request sizes - map large IO to multiple smaller standard IOs
                    3) sequential requests - detect and batch typically 8 IO requests
                4. dmClock. There shouldn't be any gap.
                    1. Simply, run mClock algorithm on each storage server.
                    2. Instead of R = R + 1/r, it should R + p/r. p is for a new request seen by the server, how many requests are also served by other servers.
                        1. typically, p is the serving server count, assume requests are evenly distributed.
                           or, we use a global aggregation service.
                        2. if without a global aggregation service, this is like evenly partition the resource quota across each shard server.
                           it'll hit problem is shard partitions are asymmetric
                5. So the revised key advantage of mClock/dmClock are
                    1. No tracking memory needed for sliding window, leaky bucket, or past request count
                    2. All three types of Reservation, Limit, Proportional Sharing are implemented. The algorithm is simple enough
                    3. dmClock doesn't require synchronization between each storage server. But if shard partitions are asymmetric, a global aggregation service is still necessary.

    
    2. Mantle: A Programmable Metadata Load Balancer for the Ceph File System    [2015, 2 refs]
       https://engineering.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-15-10.pdf
        1. decouple policies from mechanism in the metadata load balancer, expose Lua for programmers
           good paper when analyzing distributed metadata challenges
        2. key findings
            1. introduction part has good summary about techniques for distributed metadata service
               section 2 is good for understanding ceph dynamic subtree partitioning
            2. File system workloads have a great deal of locality because the namespace has semantic meaning;
               data stored in directories is related and is usually accessed together
            3. We find that the cost of migration can sometimes outweigh the benefits of parallelism,
               resulting in a 40% degradation in performance
                1. in Ceph dynamic subtree partitioning, MDS decides and migrates directories ("fragments")
            4. Many metadata balancers distribute metadata for complete balance by hashing a unique identi-fier, like the inode or filename;
               unfortunately, with such fine grain distribution, locality is completely lost
                1. Distributing for locality keeps related metadata on one MDS.
                   This can improve performance by reducing the amount of migrating inodes and the number of requests in the metadata cluster
                2. Distributing metadata to multiple MDS nodes hurts performance (left)
                   by reducing locality and increasing the number of "forwarded" requests (right)
                3. (Subtree partitioning also gets) good locality, making multi-object operations and transactions more efficient
        2. key designs
            1. Mantle: decoupling the policies from the mechanisms, we can dynamically select different techniques for distributing metadata
            2. Mantle decouples policy from mechanism by letting the designer inject code to control 4 policies:
                load calculation, "when" to move load, "where" to send load, and the accuracy of the decisions
                the language is Lua

7. readings: FAST16 papers
    1. The Tail at Store: A Revelation from Millions of Hours of Disk and SSD Deployments (NetApp) [2016, 3 refs]
       https://www.usenix.org/conference/fast16/technical-sessions/presentation/hao
        1. a paper to analyze disk/ssd performance instability in field and in large-scale
           google's tail latency and tail tolerance are highly regarded
           performance instability can be more prevalent in the future, and the findings are just beginning
           root cause analysis looks still not deep enough
            1. data is collected from performance logs at customer deployments
            2. no previous systematic large-scale studies of performance instability in storage devices, this paper is the first
            3. P.S. disk (periodically) slow down is one of the major source of OP's customer complain (e.g. why my latency raises)
               I expect this paper to tell some root cause analysis or some hint in prediction of disk slow down.
               but, it only concludes "... are the internal characteristics and idiosyncrasies of modern disk and SSD drives". so it's random?
        2. key findings
            1. storage performance instability in the field
                1. 0.2% of the time, a disk is more than 2x slower than its peer drives in the same RAID group (and 0.6% for SSD)
                   As a consequence, disk and SSD-based RAIDs experience at least one slow drive (i.e., storage tail) 1.5% and 2.2% of the time
                2. slowdown often persists; 40% and 35% of slow disks and SSDs respectively remain unstable for more than one hour
                3. more than 95% of slowdown periods cannot be attributed to I/O size or rate imbalance
                   this is the major finding
                4. older disks exhibit more slowdowns
                5. Slowdown has a high temporal locality. 90% and 85% of disk and SSD slowdown occurrences from the same drive
                   happen within the same day of the previous occurrence respectively
                6. 26% and 29% of disk and SSD drives have exhibited ≥2x slowdowns at least one time in their lifetimes
                    6% and 5% of slow disks and SSDs exhibit at least 100 slowdown occurrences
                7. A slow driver can often make an entire RAID perform poorly (as like in Ceph? and make customer complain as I see?)
                   tail tolerance storage system design is necessary
            2. root cause analysis
                1. what may slow down the magnetic disks?
                    1. the problems can be as performance "faults"
                       all these problems can reduce disk bandwidth by 10-80% and increase latency by seconds
                        1. mechanical wearout (e.g., weak head [1]),
                        2. sector re-reads due to media failures such as corruptions and sector errors [2],
                        3. overheat from broken cooling fans [3],
                        4. gunk spilling from actuator assembly and accumulating on disk head [4],
                        5. firmware bugs [41],
                        6. RAID controller defects [16, 47],
                        7. and vibration from bad disk drive packaging, missing screws, earthquakes, and constant "noise" in data centers [17, 29]
                    2. current generation of disks begin to induce performance instability "by default"
                        1. e.g., with adaptive zoning and Shingled-Magnetic Recording technologies
                2. what may slow down the SSDs
                    1. SSD garbage collection
                    2. Programming MLC cells to different states (e.g., 0 vs. 3) may require different numbers of iterations
                       due to different voltage thresholds [51]
                    3. The notion of "fast" and "slow" pages exists within an SSD
                       programming a slow page can be 5-8x slower compared to programming fast page [23]
                    4. As device wears out, breakdown of gate oxide will allow charge moves across gate easily,
                       resulting in faster programming (10-50%), but also higher chance of corruption [22]
                    5. ECC correction, read disturb, and read retry are also factors of instability [19]
                    6. SSD firmware bugs can cause significant performance faults
                       (e.g., 300% bandwidth degradation in a Samsung firmware problem [49])
            3. tail-tolerant RAID
                1. some backgrounds
                    1. When a request is striped across many drives, the request cannot finish until all the individual I/Os complete
                       the request latency will follow the tail latency
                    2. As request throughput degrades, stable drives become under-utilized
                2. advantanges
                    1. First, slow drives are masked
                    2. Second, tail-tolerant RAID is a cheaper solution than drive replacements
                3. solution
                    1. ToleRAID can cut "read tails"
                        1. in normal reads, the two parity drives are unused
                        2. if one data drive is slow, ToleRAID can issue an extra read to one parity drive and rebuild the "late" data
                    2. reactive approach
                        1. If a drive (or two) has not returned the data for ST x (slowdown threshold) longer than the median latency
                           extra read will be sent
                    3. proactive approach
                        1. always performs extra reads to the parity drives concurrently with the original I/Os
                    4. adaptive approach
                        1. by default runs the reactive approach
                           when the reactive policy is triggered repeatedly for SR times (slowdown repeats) on the same drive,
                           then ToleRAID becomes proactive until the slowdown of the offending drive is less than ST

2. readings: random paper
    1. A Common Database Approach for OLTP and OLAP Using an In-Memory Column Database    [2009, 315 refs]
       http://www.sigmod09.org/images/sigmod1ktp-plattner.pdf
       1. the is the founding paper of SAP HANA, almost the most successful in-memory database today

5. readings: random
    1. Regenerating coding
       https://www.youtube.com/watch?v=obXTLCTBGuU
        2. MDS code
           http://storagewiki.ece.utexas.edu/doku.php?id=wiki:definitions:mds_codes
            1. recovery by only tranfering 1.0x
               erasure coding needs 2.0x

    2. A Common Database Approach for OLTP and OLAP Using an In-Memory Column Database    [2009, 315 refs]
       http://www.sigmod09.org/images/sigmod1ktp-plattner.pdf
        1. logged before. today I read the most part
        2. done reading. generally saying column database is suitable for OLAP in many aspects. it also works for OLTP.
           the content is some basic orientation but not in depth.

1. readings: random
    1. Mantle: A Programmable Metadata Load Balancer for the Ceph File System    [2015, 2 refs]
        1. review the distributed metadata management challenges here
           to get more feelings about distribtued metadata management

5. readings: related to LRC
    1. Copysets: Reducing the Frequency of Data Loss in Cloud Storage
       http://www.stanford.edu/~skatti/pubs/usenix13-copysets.pdf
        1. what is the method of placement?
            1. step 1: generate P number of full node permutations
            2. step 2: divide P into non-overlappying copysets
            3. step 3: repeat 1 and 2, for Scatter-width / copyset-length times
            4. step 4: all copysets generated in 2 are the only allowed copysets

1. readings: related to LRC
    2. Local Reconstruction Code by Microsoft Research
       http://research.microsoft.com/en-us/um/people/chengh/slides/erasure_coding_tutorial_part2_FAST_2013.pdf
    3. Tutorial on Erasure Coding for Storage Applications, Part 1
       http://web.eecs.utk.edu/~plank/plank/papers/2013-02-11-FAST-Tutorial.pdf
       https://web.eecs.utk.edu/~plank/plank/papers/FAST-2005.pdf
    4. Coding for Modern Distributed Storage Systems IV
       https://www.youtube.com/watch?v=9Y3uWLgKPkU
    5. New Problems in Coding Theory with Applications to Modern Data Storage and Memories
       https://www.youtube.com/watch?v=FXOBZ1hi4J4

2. readings: FAST16 papers
    1. Flamingo: Enabling Evolvable HDD-based Near-Line Storage (Microsoft Research)    [2016, 0 refs]
       https://www.usenix.org/node/194437
        1. MS research continuing from Pelican.
           Flamingo automatically generates the best data layout and IO scheduler configuration for Pelican per environment setup.
           near-line storage is being researched (vs cold/archival storage, vs online storage)
        2. key findings/designs
            1. it has good summaries of what Pelican fails in section 2
            2. due to ambient temperature etc, per data center data layout and IO scheduler is required
            3. data layout and IO scheduler requires great effort to be tuned optimal and well-designed
               Flamingo takes rack spec, resource containts, perf targes, then automatically

7. readings: finding good papers in recent year conferences
    1. A Study of Linux File System Evolution    [2013, 54 refs]
        1. FAST13 best paper award. study from linux filesytem code bugs and patches.
           another bug study.
        2. key findings
            1. 45% patches are maintaince patches (e.g. simplify the code)
               35% are bug patches
            2. so, even experts make 500 bugs when writing a filesystem
            3. data corruption bugs account for 40%

1. readings: FAST16 papers
    1. Estimating Unseen Deduplication—from Theory to Practice (IBM Research)   [2016, 1 refs]
       https://www.usenix.org/conference/fast16/technical-sessions/presentation/harnik
        1. estimate dedup/compress ratio without reading entire dataset, output a estimated range
           15% sample is sufficient, fast sample by large super-chunks; run with 10MB less memory
           this paper is based on works of Valiant's "Estimating the unseen" [17][18]

    2. Using Hints to Improve Inline Block-layer Deduplication (IBM Research)    [2016, 1 refs]
        1. modify VFS interface to allow application pass dedup hints
           actually, app-aware/context-aware dedup should be a topic. passing hints is one way.
           more generally, storage strategies should employ more context flexibility
        2. key designs
            1. block dedup know only read/write, size, offset, nothing about context
                1. dedup metadata harms reliability (the data may intend to duplicate) and waste resouce
                2. undesirable to dedup on data that does not worth it
            2. possible hints
                1. NODEDUP - don't dedup on unecessary/worthy data
                2. PREFETCH - prefetch hashes when dedup knows data context
                3. more in paper ...

    3. CloudCache: On-demand Flash Cache Management for Cloud Computing (VMware)   [2016, 2 refs]
       https://www.usenix.org/node/194459
        1. VMware vSAN 6.5 uses server-side PCIe SSD to accelerate write ack, batch them, dedup, and exploit locality
           the SSD-in-middle can be used everywhere. in cluster-wide they consist the resource pool and employ distribution and migration
           besides flash cache wear-out is a serious problem.
        2. key designs
            1. for multi-tenancy/on-demand, use Reuse Working Set (RWS) to manage VM's cache size. like the working set for memory
                1. each new device added to the computer need to be virtualized.
                   for cache, RWS is a way. we don't need to lock up entire cache card for a VM.
                2. on-demand cache management: RWS - data blocks reused at least N times during a time interval window
                    1. select window size by test simulation
                    2. predict cache size in next window by expotional smoothing
                    3. use a staging area in main memory (LRU), before block has not yet been admitted
                        1. in main memory, how to ensure data persistency?
                            - only keep the data returned by read
                            - for writes only their addresses
                            1. so, this is a no-cache write through
            2. when cache size is not enough for VM, we do dynamic cache migration
                1. VMs can be live migrated to other hosts, to migrate the cache
                    1. when the migrated VM accesses a dirty block on source host's cache, we forward request
                        1. the metadata of the dirty blocks (8B per 4KB data), need to be transfered along with VM migration
                    2. the source host also proactively transfer VM's cache data
                2. migration rate limiting by max number of blocks per time interval (e.g. 100ms)
        3. evaluation
            1. cache usages of 12 concurrent VMs should provide more results, e.g. latency impact, or more use-facing metrics.

    4. Access Characteristic Guided Read and Write Cost Regulation for Performance Improvement on Flash Memory (Edwin Sha)    [2016, 1 refs]
       https://www.usenix.org/conference/fast16/technical-sessions/presentation/li-qiao
        1. this paper is on storage-media/hardware level
           flash memory write operation cost 10-20 times more than read.
        2. key designs/findings
            1. base observation: most accesses are "read-only" (read>95%) or "write-only" (write>95%)
                1. A write-only page will be written with a low-cost write to improve write performance (although retention is relaxed)
            2. the work is based on
                1. Pan et al. [9] and Liu et al. [10] proposed to reduce write costs by relaxing the retention time requirement of the programmed pages
                2. Wu et al. [12] proposed to apply a high-cost write to reduce the cost of read requests performed on the same page
                3. Li et al. [13] proposed to apply low-cost writes when there are queued requests to reduce the queueing delay
                4. and add workload access characteristics based cost regulation

4. readings: crash consistency and point-in-time consistency
    1. point-in-time consistency
       https://en.wikipedia.org/wiki/Data_consistency#Point-in-time_consistency
        2. filesystem relies on write ordering to ensure recoverability (e.g. journaling). but write cache may change the order of writes.
        3. point-in-time consistency, means to, write in order when an unexpected shutdown: 1-2-3-4 committed, write nothing or 1 or 1-2 or 1-2-3 or 1-2-3-4
           it can be truely write in order, or the equvalent effect (e.g. backup battery)
        4. high-end hardware disk controllers in servers may include a small battery backup unit.
           the controller may lies to the operation system about what order it writes.
           but on power loss, the battery ensures all writes are written.

    2. about write ordering
        1. Controlling File System Write Ordering
           https://www.usenix.org/legacy/events/fast05/wips/slides/burnett.pdf
           https://www.usenix.org/legacy/events/fast05/wips/burnett.pdf

    3. Principles of creating a consistent (point-in-time) backup
       http://serverfault.com/questions/520514/principles-of-creating-a-consistent-point-in-time-backup
        1. the standard approach is to shutdown the service, do a snapshot, and then backup it
        2. another approach is to export a point-in-time set of data from the application, and then backup the exported data
        3. an alternative approach, is to mark files as being backed up while they are copied. this may defer updates while the backup is running
        4. How to create a consistent (starting) point-in-time backup of a MongoDB replica set?
           http://serverfault.com/questions/639039/how-to-create-a-consistent-starting-point-in-time-backup-of-a-mongodb-replica

    4. atomic filesystem operation
       http://cseweb.ucsd.edu/~swanson/papers/FAST2016NOVA.pdf
        1. this can also be achieved by journaling, and eventually by write ordering
           so are Shadow paging and Log-structuring.
        2. write ordering on filesystem is usually by fsync/fdatasync
           in NVMM, it is by some memory barrier/flush instruction

    5. what is crash consistency
        1. http://www.altaro.com/hyper-v/vss-crash-consistent-vs-application-consistent-vss-backups-post-1-of-2/
            1. all data within a crash-consistent backup set is captured at exactly the same time
        2. Crash Consistency: Rethinking the Fundamental Abstractions of the File System
           http://queue.acm.org/detail.cfm?id=2801719
            1. reorder of filesystem calls is the source of problem
            2. ALICE: All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications    [2014, 38 refs]
               https://www.usenix.org/node/186195
                1. crash consistency: maintain data invariants across a system crash
                2. "The diagram shows the modularized update protocol for all applications ..."
                 good stuff
            3. Torturing Databases for Fun and Profit    [2014, 25 refs]
               https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-zheng_mai.pdf
                2. By recording SCSI commands, we can inject faults with high fidelity

    6. VM quiesce and consistency
       http://www.altaro.com/hyper-v/vss-crash-consistent-vs-application-consistent-vss-backups-post-1-of-2/
       https://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1015180

    7. Write ordering data and durability: why does it matter?
       https://boostgsoc13.github.io/boost.afio/doc/html/afio/design/acid_write_ordering/write_ordering_data.html
        1. good material
        2. performant Durability essentially reduces down to answering two questions
            (i) how long does it take to restore a consistent state after an unexpected power loss
            (ii) how much of your most recent data are you willing to lose?
        3. the normal and last-commit-durable way of writing data
            (i) writes one's data to the filing system,
            (ii) ensure it has reached non-volatile storage,
            (iii) appends the knowledge it definitely is on non-volatile storage to the intent log, and then
            (iv) ensure one's append also has reached non-volatile storage
        4. using the transactional checksum (similar to what mentioned in "Optimistic Crash Consistency" paper)
           it is possible to lose recent commits. but there is no need for fsync/fdatasync completely
           the problem is, checksum computing takes time. and recovery is longer because it needs to verify checksums.
            write all your data, but keep a hash like a SHA of its contents as you write it.
            When you write your intent log, atomically append all the SHAs of the items you just wrote.
        5. ZFS transaction group. so less fsync/fdatasync is necessary
           but to-disk writes need to be batched for 5 seconds to fill the group
            writes are grouped into transaction groups.
            intra-group there is no ordering, inter-group it is guaratneed of write ordering

5. readings: crash consistency
    1. ALICE: All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications    [2014, 38 refs]
       https://www.usenix.org/node/186195
        1. test consistency problems by reordering block commands or system calls
           reveal classic storage softwares' underlying update protocol (commit protocol)
           very good paper. especially the figure 4 update protocols
            1. a bunch of filesystems and DBs are found to have consistency bugs
            2. famous softwares have crash consistency vulnerabilities, even levelDB
            3. this paper designed the general approach that how can we test a software for its crash consistency
                1. this is generally known to be subtle. but this paper use reordering of low-level operations
                   to have solved this problem
                2. similarly, we can apply intelligent reordering to test application's concurrency handling
        2. highlights
            1. BOB - Block Order Breaker
                1. collects block-level traces and reorder them to explore possible inconsistent crash states
                2. Table 1 shows the how current filesystems support the atomicity and ordering, as tested
            2. ALICE - Application-Level Intelligent Crash Explorer
                1. collect filesystem related system call traces, reoder them to find out inconsistent crash states
                2. it also reveals the underlying update protocol for those applications (mostly DBs)
                3. Table 3 shows the vulnerabilities findings of famous storage softwares, as tested
                    1. LevelDB has append atomicity vulnerability,
                       i.e. the append may enlarge file size first, then crash, then (should have) fill content
                            but because of crash, the new file space contains garbage
                        1. this is mentioned in "Atomic Commit In SQLite"

    2. Torturing Databases for Fun and Profit    [2014, 25 refs]
       https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-zheng_mai.pdf
        1. record, reorder/inject power faults, and replay the underlying ISCSI commands.
           verifies whether the databse ACID properties suvive crash
           as discovered, all 8 databases exhibit erroneous behavior
            1. Table 1 shows the discovered ACID violation results

    3. Atomic Commit In SQLite
       https://www.sqlite.org/atomiccommit.html
        1. the famous document to explain how underlying DB atomic transactions are done
           e.g. is disk sector write atomic?
           very good article to illustrate journal commiting into details
        2. The best part is the hardware assumptions
            1. disk atomic sector write
                - we cannot assume it, but most modern disk should support it
            2. disk sector write is linear, i.e. write from left to right, or right to left
                - we assume it
            3. fsync only flush to disk controller, disk controller may cache it
                - we assume disk controller should guaratnee it has backup battery if it caches writse
            4. file growth in length may first increase file size, at this time the new file space is filled with garbage
                - we didn't assume an append, i.e. file size increase + fill in new content, is atomic
                  except VFS says it support "safe append"
            5. file deletion is atomic
                - we assume it
            6. write to a range of bytes will not damage or alter any bytes outside that range
                - we assume it
        3. SQLite is using a redo log on default
           it also support another way, the WAL
            1. comparisons at
               https://www.sqlite.org/wal.html
                1. WAL is significantly faster in most scenarios.
                   it seems most current implementations use WAL instead

2. readings: (SMR) disks
    1. picked materials
        Brief introduction by Wikipedia: https://en.wikipedia.org/wiki/Shingled_magnetic_recording
        Data management for SMR: https://www.cs.cmu.edu/~garth/papers/05_feldman_022-030_final.pdf
        SMR disk characteristics shared on Openstack Tokyo Summit (2015): https://www.openstack.org/zh_CN/videos/tokio-2015/tokyo-3219
        Google's experience with SMR disks: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44830.pdf (See the "Optimized SMR Implementation" section)
        Reverse engineer the SMR drives: https://www.usenix.org/system/files/conference/fast15/fast15-paper-aghayev.pdf

    2. the summary
        "Shingled Magnetic Recording (SMR) is a new hard drive technology that allows the magnetic tracks on a platter to be overlapped with each other, i.e. shingled. The technology has the potential to greatly improve storage density. The challenges are, the overlapping-tracks architecture may slow down the writing process, and the rewriting becomes more complicated. There are two major solutions to manage data on SMR disks. Drive-managed SMR uses a disk shipped firmware, similar to what we see in SSD. Host-managed SMR, in contrast, shifts data management responsibility to the host. In general, SMR drives reveal a bias towards GB/$ improvements over IOPS/GB improvements."

    3. Skylight—A Window on Shingled Disk Operation
       https://www.usenix.org/system/files/conference/fast15/fast15-paper-aghayev.pdf
        1. a reverse engineer to the SMR disk, revealing some of its key properties

4. readings: Flash Memory Summit 2016
    1. Managing Multi-Tiered Non-Volatile Memory Systems for Cost and Performance
       https://www.youtube.com/watch?v=nOaEY93ViKg
        1. Average access time = t1 + Hit Rate * SSD access time + Miss Rate * (t2 + HDD access time)
           t1 = Addr lookup time to read from SSD cache
           t2 = Addr lookup time to read from HDD, and data replacement time for the SSD cache
        2. the MARVELL cache engine to address the challenge of cache requirements
           low missrate vs low lookup overhead
            1. for hierarchical storage system design, the better the cache, the
               better the overall performance it can achieve. or, the cache is
               the bottleneck of how flexible the design can be
            2. for cache to be fast enough, hardware is necessary
        3. we don't develop two chips, we connect two chips together to become a
           doubled box. by this way, we reduce cost.

6. readings: misc materials collected when I prepare the SSD & FTL share
    1. ceph bluestore工作流程
       http://www.sysnote.org/2016/08/25/bluestore-work-flow/
        1. the picture style is what I can learn to diagram storage systems
        2. aio will be submitted to linux kernel to handle.
           we can use either epoll or polling io_getevents to receive the completion.
           in bluestore, we use the second way.
        3. "bluestore里通过OpSequencer来保证kv事务的顺序性"
        4. "然后db->submit_transaction将kv提交到rocksdb，但是没有落盘 ... 然后都会调用db->submit_transaction_sync来进行提交并刷盘的动作"
        5. "从上面的流程分析可以知晓，一个I/O在bluestore里经历了多个线程和队列才最终完成，
                对于非WAL的写，比如对齐写、写到新的blob里等，I/O先写到块设备上，然后元数据提交到rocksdb并sync了，才返回客户端写完成（在STATE_KV_QUEUED状态的处理）；
                对于WAL（即覆盖写），没有先把数据写块设备，而是将数据和元数据作为wal一起提交到rocksdb并sync后，这样就可以返回客户端写成功了，然后在后面的动作就是将wal里的数据再写到块设备的过程，
                    对这个object的读请求要等到把数据写到块设备完成整个wal写I/O的流程后才行，代码里对应的是_do_read里先o->flush()的操作，
                    所以bluestore里的wal就类似filestore里的journal的作用。"
            1. here's the magic how Ceph reduced the need for double writes
    2. ceph中对象读写的顺序性及并发性保证
       http://www.sysnote.org/2016/08/29/ceph-io-sequence/
        1. 不同对象的并发控制: "不同的对象有可能落到同一个pg里，ceph实现里，在OSD的处理线程中就会给PG加锁，一直到queue_transactions里把事务放到journal的队列里（以filestore为例）才释放PG的锁。"
        2. 同一个对象的并发顺序控制
            1. 一个client情况: 串行的，因为加了锁
            2. 对于多client的场景: 不知道
        3. ceph消息层的顺序性保证
            1. ceph的消息里有个seq序号； reader->seq, in_msg->seq, resp_msg->in_seq_acked
            2. pg层顺序保证及对象锁机制:
                1. "对某个对象进行写时会在对象上进行加锁操作ondisk_write_lock()" (在do_op()之内)
                2. "在进入do_op之前就已经加了PG的的锁" (在do_op()之前)
                3. "那么问题来了，同一个对象的2次写请求到了store层处理的时候也是有顺序上的保证吗？"
            3. store层保证顺序:
                1. "写请求到达filestore后（入口是queue_transactions），会生成OpSequencer"
                    1. 如果这个pg之前已经生成过了，就直接获取，每个pg有一个osr，类型为ObjectStore::Sequencer，osr->p就是指向OpSequencer
                    2. "在write_thread中使用aio异步将事务写到journal里，并将I/O信息放到aio_queue"
                       "在write_finish_thread里对于已经完成的I/O，会根据完成的op的seq序号按序放到journal的finisher队列里
                        （因为aio并不保证顺序，因此采用op的seq序号来保证完成后处理的顺序）"
                       "如果某个op之前的op还未完成，那么这个op会等到它之前的op都完成后才一起放到finisher队列里"
                    3. "FileStore::OpWQ线程池调用FileStore::_do_op，先osr->apply_lock.Lock()进行加锁操作"
                       "然后进行写数据到filesystem的操作完成后，在FileStore::_finish_op里才会osr->dequeue，并osr->apply_lock.Unlock()"
                       "即通过OpSequencer来控制同一个pg内写I/O到filesystem的并发，但是对于不同pg的写I/O是可以在OpWQ的线程池里并发处理的"
                    4. "FileStore里先通过op的seq来控制持久化写到journal的顺序性，然后再通过OpSequencer来保证写数据到文件系统的顺序性"
            4. primary发到replica的请求顺序
                1. "有了消息层的顺序性，以及primary处理上的顺序性，再将请求发给replica的时候也是有序的"
    3. The Lies That Flash Storage Companies Tell with Dave Wright of NetApp/SolidFire
       https://www.youtube.com/watch?v=35KNCOYguBU
        1. solidfire acquired by netapp. this video is still by Dave Wright. good video
           link to a previous video: Comparing Modern All-Flash Architectures - Dave Wright, SolidFire
                                     https://www.youtube.com/watch?v=AeaGCeJfNBg
        2. key points
            1. challenges of adopting a disk structure to flash
                1. Add data reduction & complex metadata handling
                    1. truth: we already have robust data reduction systems built. it's not that hard actually
                2. dealing with flash wear and write amplification
                    1. truth: just rely on (more expensive) SSD FTL, or just build ground-up. it's not that hard actually
            2. what's different between cMLC and eMLC
                1. endurance, performance, power loss protection, amount of overprovisioning
                   mostly just look at DWPD (ranges from 0.3 -> 10)
            3. you need overprovisioning to efficiently erase flash
                1. use 28% over-provisioned drivers (AFF, XtremIO)
                   use 7%, but carve out additional "reserved" capacity (Pure)
                   use 7%, but use failure rebuild space for efficient erasure (SolidFire Helix, 3par Adaptive Sparing)
                2. related reading: why SSD need over-provisioning
                    1. SSD Over-Provisioning And Its Benefits
                       http://www.seagate.com/sg/en/tech-insights/ssd-over-provisioning-benefits-master-ti/
                        1. used as log buffer
                        2. hidden by GiB (2^30) - GB (10^3) = 7.37%
                    2. "In practice, an SSD's performance begins to decline after it reaches about 50% full"
                    3. "However, once garbage collection begins, the method by which the data is written
                        – sequentially vs. randomly – begins to affect the performance."
                    4. for SSD with data reduction, data entrophy has effects
            4. long code path designed for disk can't deliver flash latency
                1. Dave Hitz's example
                    1. the old model was message passing, and before the disk replies, the OS put requests in queue
                       the queuing model was no big deal, if you just wait for 10 milliseconds for disk to come back
                       but for microseconds delay, queue consumes way more time than what flash has done
                    2. Netapp rewrite the underlying handler to take it off the interrupt handler, all the way through
                       the network, and reply the request
                    3. it radically changes the benchmark results
            5. flash is too fast for a traditional dual-controller architecture
                1. yes - performance can scale, but moore's low has increased these limits over time
                2. Dave Hitz's comments
                    1. all flash, the engineer can do some tunine underlyingly, that won't work if there were any devices that
                       are slower than 10-20 ms in the cluster.
                    2. so, hybrid systems can be different
            6. one flash architecture can cover all use cases
                1. use cases: traditional (data services), speed (application-centric), cloud (service-oriented, scale-out)
                   netapp's portfilo for all the three. solidfire is the cloud one.
                n. question
                    1. what about the public cloud?
            7. about flash startups and incumbents
                1. truth: disk architectures can be adaptedt to flash
                          ground-up flash architectures are still behind the full range of data services needed by traditional enterprise datacenters
                          no single architecutre can address the full range of environments that all flash array are being used today
                          all flash array are becoming the de-facto option for primary data at a faster speed than many predicted
        3. related readings
            1. "Queue depth refers to the number of outstanding access operations"
               http://www.tomshardware.com/reviews/ssd-gaming-performance,2991-3.html

5. readings: misc
    1. SMR disk data management
       https://www.cs.cmu.edu/~garth/papers/05_feldman_022-030_final.pdf
        1. hard to modify data after the writes shringle "overlapped"
        2. host managed, cooperatively managed, drive managed.
           many things similar to FTL
        3. Log-structed and copy-on-write application can be good match
        4. Exposed SMR. Caveat Scriptor and Coop are two proposals for SMR interfaces.

6. readings: gRPC
    1. key points
        1. gRPC is in CNCF (which put Kubernetes at head. So Google seems influcing in it)
        2. gRPC uses protocol buffers by default as the definition language and message format
        3. 目前版本来说实测性能肯定是差thrift一截的(实测grpc0.8版本).应该就是缺点吧,虽然用了netty和protobuf
        4. GRPC uses HTTP2 at the transport layer which is a multiplexing wire protocol
    2. material
        1. https://microsoft.github.io/bond/why_bond.html
           http://blog.csdn.net/dazheng/article/details/48830511
           https://news.ycombinator.com/item?id=9665204
           https://groups.google.com/forum/#!topic/grpc-io/JeGybvbz8nc
           http://www.andrewconnell.com/blog/grpc-and-protocol-buffers-an-alternative-to-rest-apis-and-json
           https://www.zhihu.com/question/30027669
           http://colobu.com/2016/09/05/benchmarks-of-popular-rpc-frameworks/
           https://www.quora.com/Is-GRPC-better-than-Thrift

6. readings: reading related papers
    1. Jupiter Rising: A Decade of Clos Topologies and Centralized Control in Google's Datacenter Network (Google)    [2015, 90 refs]
       https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43837.pdf
        1. google's intra/inter datacenter switch design.
            1. "scaling in capacity by 100x over ten years to more than 1Pbps of bisection bandwidth"
            2. related article: http://mp.weixin.qq.com/s/hQHuv4Pjm4dutepjcPhKxA
        2. key findings
            1. we would expect 11/12 of the traffic (92%) to be destined for other blocks.
            2. Packet drops associated with incast [8] and outcast [21] were severe pain points
        3. highlights
            1. reference to "VL2: a scalable and flexible data center network"
            2. Cable bundling helped reduce fiber cost (capex + opex) by nearly 40%
            3. support depopulated deployment, where we initially deployed only 50% of the maximum bisection bandwidth
            4. As a rule of thumb, we allocated 10% of aggregate intra-cluster bandwidth for external connectivity using one to three aggregation blocks
               These aggregation blocks were physically and topologically identical to those used for ToR connectivity
            5. we developed Neighbor Discovery (ND), an online liveness and peer correctness checking protocol.

7. readings: Read the DocumentDB Bw-tree
    1. The Bw-Tree: A B-tree for New Hardware Platforms (Microsoft Research)    [2013, 110 refs]
       https://www.microsoft.com/en-us/research/publication/the-bw-tree-a-b-tree-for-new-hardware/
        1. the foundamental data structure used in DocumentDB. SqlServer also tries to use it once heard.
           key improvements: latch-free, elastic pages, delta updates (avoids cache line invalidations), log structured storage
           good paper. one of the concurrent b-tree reference implementation
            1. so, the entire Bw-tree is put in memory, while the disk is managed by log structured store
               compared to traditional b-tree, the latter's disk part is still update-in-place, and memory part is also update-in-place
            2. generally, this is a better structure instead of directly use log-structured tree
               at least, the on-disk data is organized as pages and still indexed by the b-tree
            3. a lot of effort (and benefit) is put on the latch-free design
               latch free b-tree design is a big contribution of this paper
            3. I wish the evaluation part includes comparison with LSM based DBs, such as LevelDB
        2. backgounds
            1. b-tree is the classic method for DB indexing, e.g. MondoDBs
               http://zhangliyong.github.io/posts/2014/02/19/mongodb-index-internals.html
               even we have LSM-tree, we still need read indexing
        3. highlights
            1. we believe that latch free techniques and state changes that avoid update-inplace are the keys to high performance on modern processors
                1. note that this is talking about memory
            2. mapping table
                1. We use PIDs in the Bw-tree to link the nodes of the tree (rather than physical pointers)
                2. The mapping table severs the connection between physical location and inter-node links
                   This enables the physical location of a Bw-tree node to change on every update and every time a page is written to stable storage,
                   without requiring that the location change be propagated to the root of the tree
                3. the page is logical, doesn't have fixed size, it can be big, and do page split
                   managed by page id (PID) in the mapping table
                    1. i.e. the elastic pages
            3. Delta Updating
                0. the Bw-tree performs node updates via "delta updates" (attaching the update to an existing page), not via update-in-place (updating the existing page memory).
                   Avoiding update-in-place reduces CPU cache invalidation, resulting in higher cache hit ratios
                1. Page state changes are done by creating a delta record (describing the change) and prepending it to an existing page state.
                   We install the (new) memory address of the  elta record into the page's physical address slot in the mapping table
                   using the atomic compare and swap (CAS) instruction
                   If successful, the delta record address becomes the new physical address for the page.
                2. Occasionally, we consolidate pages (create a new page that applies all delta changes)
                   A consolidated form of the page is also installed with a CAS, and the prior page structure is garbage collected (i.e., its memory reclaimed)
            4. Bw-tree Structure Modifications (SMO)
                1. a page split introduces changes to more than one page
                2. We use a B-link design [11] to make this easier.
                   With a side link in each page, we can decompose a node split into two "half split" atomic actions
                    1. [11] Efficient Locking for Concurrent Operations on B-Trees    [1981, 615 refs]
                3. this is a innovative point and crucial point of this paper
                    1. described in detail at section IV. child spit -> parent update
                    2. our epoch mechanism guarantees that we will see the appropriate deleted state
                    3. ... One way to think about this is that if a thread stumbles upon an incomplete SMO, it is like seeing uncommitted state
                       Being latch-free, the Bw-tree cannot prevent this from happening
                       Our response is to require that such a thread must complete and commit the SMO it encounters before it can either
                        (1) post its update or (2) continue with its own  MO
            5. Log Structured Store
                1. Pages are written sequentially in a large batch
                2. When flushing a page, the LSS need only flush the deltas
                   There is a penalty on reads, however, as the discontinuous parts of pages all must be read to return a page to the main memory cache.
                3. During cleaning, LSS makes pages and their deltas contiguous for improved access performance
                4. Incremental Flushing
                   When flushing a page, the cache manager only marshals those delta records
                   which have an LSN between the previously flushed largest LSN on that page and the current ESL value
            6. Managing Transactional Logs
                1. We tag each update operation with a unique identifier that is typically the log sequence number (LSN)
                2. Like conventional systems, pages are flushed lazily while honoring the write-ahead log protocol (WAL)
                3. Unconventionally, however, we do not block page flushes to enforce WAL
                    1. DC (data component) not make durable any operation with an LSN greater than the latest ESL (End of Stable Log)
                       To enforce this rule, records on a page that have LSNs larger than the ESL are not included in a page when flushed to the LSS
        2. more materials
            1. The Bw-Tree key-value store and its application to server/cloud data management in production
               https://www.snia.org/sites/default/files/SDC15_presentations/database/SudiptaSengupta_Bw-Tree-Key_Value.pdf
            2. Bw树：新硬件平台的B树
               http://www.cnblogs.com/Amaranthus/p/4375331.html
            3. 如何分析bw-tree在8超线程机器上测试1000万OPS的结果？
               https://www.zhihu.com/question/52953257
            4. Comparison of the State-of-the-art B-Trees Designs on Modern Hardware
               http://dias.epfl.ch/files/content/sites/dias/files/groups/DIAS-unit/public/studentProjects/BtreeComparison.pdf
                1. keywords: B+Tree, Bw-Tree, MassTree, Multi-Rooted B+Tree, Shore-MT, OLTP, latch-free Btree, multicores, multisockets
            5. 数据库管理系统(二): Lock-free, high-performance Bw Tree
               https://zhuanlan.zhihu.com/p/20569606
            6. C++ 的无锁数据结构在工业界有真正的应用吗？
               https://www.zhihu.com/question/52629893
                1. 内存数据库领域用的很多
                    1. MemSQL用Lock Free Skip List做索引：The Story Behind MemSQL's Skiplist Indexes
                    2. SQL SERVER内存存储引擎Hekaton用Lock Free Bw-Tree做索引：https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/bw-tree-icde2013-final.pdf
                       https://www.microsoft.com/en-us/research/blog/hekaton-breaks-through/
                    3. HyPer的并行查询引擎大量的应用了Lock Free数据结构，如使用Lock Free的Hash Table实现Hash Join：http://db.in.tum.de/~leis/papers/morsels.pdf
                    4. DB2 BLU的并行查询引擎：http://db.disi.unitn.eu/pages/VLDBProgram/pdf/industry/p773-barber.pdf5. OceanBase也大量的使用Lock Free
            7. Masstree: Cache Craftiness for Fast Multicore Key-Value Storage    [2012, 131 refs]
               https://pdos.csail.mit.edu/papers/masstree:eurosys12.pdf
                1. besides the bw-tree, another reference concurrent b-tree implementation
                   the performance is said to be good
                2. highlights
                    1. the summary
                        1. Masstree uses a combination of old and new techniques to achieve high performance [8, 11, 13, 20, 27–29].
                        2. Query time is dominated by the total DRAM fetch time of successive nodes during tree descent
                           to reduce this cost, Masstree uses
                            1. a wide-fanout tree to reduce the tree depth
                            2. prefetches nodes from DRAM to overlap fetch latencies
                            3.  and carefully lays out data in cache lines to reduce the amount of data needed per node
                        3. A Masstree is a trie with fanout 264 where each trie node is a B+-tree
                            1. The trie structure efficiently supports long keys with shared prefixes;
                            2. the B+-tree structures efficiently support short keys and fine-grained concurrency
                    2. concurrency overview
                        1. Optimistic concurrency control
                        2. The key communication channel between read & write is a per-node version counter
                        3. Writer–writer coordination
                            1. Masstree writers coordinate using per-node spinlocks.
                               A node's lock is stored in a single bit in its version counter
                            2. As with Blink-trees [27], lock ordering prevents deadlock
                               locks are always acquired up the tree
                        4. Writer–reader coordination
                            1. Before making any change to a node n, a writer operation must mark n.version as "dirty."
                            2. Every reader operation first snapshots every node's version.
                        5. Updates
                            1. writers must not delete old values until all concurrent readers are done examining them
                            2. We solve this garbage collection problem with read-copy update techniques, namely a form of epoch-based reclamation [19].
                    3. persistency
                        1. A put operation appends to the query thread's log buffer and responds to the client without forcing that buffer to storage
                           Logging threads batch updates to take advantage of higher bulk sequential throughput, but force logs to storage at least every 200 ms for safety
                            1. so it may lose some writes if crash
                        2. Masstree periodically writes out a checkpoint containing all keys and values
                    4. evaluation
                        1. Factor analysis
                            1. Binary：　start with a lock-free binary tree. throughput ~1x
                               -> +Flow, +Superpage, +IntCmp: Memory allocation often bottlenecks multicore performance
                               -> 4-tree:　fanout 4, and, We aim to reduce and overlap those latencies and to pack more useful information into cache lines that must be fetched
                               -> B-tree: lockless balanced wide fanout (15) b-tree
                               -> +Prefetch: enable DRAM prefetch, allowing a single address request to result in multiple data words
                               -> +Permuter: Leaf-node permutations (§4.6.2)
                               -> Masstree: throughput ~3x

4. readings: ceph community updates
    1. ceph blog
        1. We've released the kraken!
           http://ceph.com/releases/v11-2-0-kraken-released/
        2. RGW Metadata Search
           http://ceph.com/geen-categorie/rgw-metadata-search/
    2. ceph blueprints
        1. ADD IOHINT IN CEPHFS
           http://tracker.ceph.com/projects/ceph/wiki/Add_IOhint_in_CephFS#Add-IOhint-in-CephFS
            1. because cephfs can mount subidr, so different subdir can have different usage, like some subdir don't need cache
        2. CACHE TIERING - IMPROVE EFFICIENCY OF READ-MISS OPERATIONS
           http://tracker.ceph.com/projects/ceph/wiki/Cache_Tiering_-_Improve_efficiency_of_read-miss_operations
        3. CEPH ON APACHE MESOS
           http://tracker.ceph.com/projects/ceph/wiki/Ceph-mesos
            1. ceph on mesos, and hadoop over ceph RGW .. looks interesting
        4. HADOOP OVER CEPH RGW STATUS UPDATE
           http://tracker.ceph.com/projects/ceph/wiki/Hadoop_over_Ceph_RGW_status_update
        5. IMPROVEMENT ON THE CACHE TIERING EVICTION
           http://tracker.ceph.com/projects/ceph/wiki/Improvement_on_the_cache_tiering_eviction
        6. OPTIMIZE NEWSTORE FOR MASSIVE SMALL OBJECTS STORAGE
           http://tracker.ceph.com/projects/ceph/wiki/Optimize_Newstore_for_massive_small_object_storage
            1. LOSF leads to many small files, which overwhelm the FS.
            2. Newstore introduced fragement_list, we now change it to object:fragment N:M
        7. MULTI-OBJECT TRANSACTION SUPPORT
           http://tracker.ceph.com/projects/ceph/wiki/Rados_-_multi-object_transaction_support
            1. two-phase commit
        8. RADOS - METADATA-ONLY JOURNAL MODE
           http://tracker.ceph.com/projects/ceph/wiki/Rados_-_metadata-only_journal_mode
            1. use cases: 1) cloud disk doesn't need data in journal
                          2) cache tiering base pool doesn't need to journal data since cache pool provides durability
        9. TIERING-ENHACEMENT
           http://tracker.ceph.com/projects/ceph/wiki/Tiering-enhacement
            1. At the implementation level, each RADOS object has associated with it a policy that provides specific action hints for that object.
               RADOS uses that policy to assist it in optimizing the movement of objects between the pools
        10. Improve tail latency
            http://tracker.ceph.com/projects/ceph/wiki/Tail_latency_improvements
            1. Tail latency (e.g. 99.99%) is important for some online serving scenarios, this blueprint summarizes some tail latency issues we observed on our production cluster.
                1. OSD ungraceful shutdown. When the OSD might crash due to broken disk, software bug, etc.
                   Currently the crash/down of OSD is detected by its peers and it could take tens of seconds to trigger a osdmap change (20 seconds by default),
                   which further lead client to retry the in flight requests associated with this OSD.
                    1. We could preemptively tell MON that the OSD is going down (crash) when there is assertion failures, as with a graceful shutdown
                2. Peering speed improvements
                3. Slow OSDs. OSD could become slow for various reasons, and currently the client latency is determined by the slowest OSD in the PG serving the request.
                    1. For EC pool, we tested the patch to read k + m chunks and used the first returned k chunks to serve the client,
                       it turned out to significantly (30%) improved the latency, especially for tail.
                       However, there is still a couple of problems:
                        If the primary is stucked, the patch would not help.
                        the patch does not bring benefit for WRITE (maybe only in a negative way as it brought more load).
                        It does not benefit replication pool.
        11. osd: Faster Peering
            http://tracker.ceph.com/projects/ceph/wiki/Peering_speed_improvements
        12. SLOPPY READS
            http://tracker.ceph.com/projects/ceph/wiki/Sloppy_reads
            1. Currently, when an osd gets a read on a pg for which it is not the primary, it drops it since the client will resend
            2. it might be interesting to allow a read to be serviced on an osd with a non-backfill copy of the pg, even if the osd is not primary or the pg is not active
        13. PASSIVE MONITORS
            http://tracker.ceph.com/projects/ceph/wiki/Passive_monitors
            1. passive monitors in paxos quorum only watch, but not vote. they can quickly go active when the quorum needs more nodes, or simply act as a backup
        14. CEPHFS FSCK PROGRESS/ONGOING DESIGN
            http://tracker.ceph.com/projects/ceph/wiki/CephFS_fsck_Progress_&#38-Design
            1. This tool (landing soon) is capable of reconstructing the metadata pool even if everything in it is deleted

        15. PMSTORE - NEW OSD BACKEND
            http://tracker.ceph.com/projects/ceph/wiki/PMStore_-_new_OSD_backend
            1. Goals:
                SSD/NVMe/NVM optimized,
                In-memory collection/object index, data on block device,
                Minimize write amplification factor to the block device,
                Leverage userspace PMBackend library optimized for Ceph's workload.

        16. RGW NEW MULTISITE SYNC
            http://tracker.ceph.com/projects/ceph/wiki/Rgw_new_multisite_sync
    3. ceph dev maillist
        1. crush multipick anomaly (61 mails)
           related: http://tracker.ceph.com/issues/15653
                    https://github.com/ceph/ceph/pull/10218
            1. the math problem
        2. explicitly mapping pgs in OSDMap
            1. The basic idea is to have the ability to explicitly map individual PGs to certain OSDs so that we can move PGs from overfull to underfull devices
            2. link: http://pad.ceph.com/p/osdmap-explicit-mapping
            3. the metdata + hash hybrid placement
    4. WeiChat: Ceph开发每周谈: haomai wang's articles
        1. openfabrics
           https://www.openfabrics.org/index.php/abstracts-agenda.html
            1. The OpenFabrics Enterprise Distribution (OFED™)/OpenFabrics Software is open-source software for RDMA and kernel bypass applications.
            2. Ceph RDMA Support (Haomai Wang, XSKY)
               https://www.openfabrics.org/images/eventpresos/2017presentations/103_Ceph_HWang.pdf
        2. linux vaults
           http://events.linuxfoundation.org/events/vault/program/slides
            1. the linux storage and filesystem conference
            2. Hyper Converged Cache for Distributed Storage
               http://events.linuxfoundation.org/sites/events/files/slides/2017_02_Vault_hyperstash_r4.pdf
                1. Local read cache and distributed write cache
                   Two hosts are required in order to provide physical redundancy
                2. good idea
        3. CDM Mar 2017: explicitly mapping pgs in OSDMap
            1. proposed by Sage. looks like there is a need to metadata + hash mixed placement approach
        4. Ceph GsoC 2017 (Ceph Google Summit of Code)
           http://ceph.com/gsoc2017-ideas/
            1. RGW: Local File Backend for RGW
        5. LibCrush项目成立
           http://libcrush.org/main/libcrush
            1. libcrush is a C library to control placement in a hierarchy
            2. 主要是ceph crush的拷贝，但是增加的API document
               http://doc.libcrush.org/master/group___a_p_i.html
        6. ZLog - a distributed shared log for ceph
           https://github.com/noahdesu/zlog
            1. ZLog: http://noahdesu.github.io/2014/10/26/corfu-on-ceph.html
               CORFU protocol: https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/balakrishnan
               why log: http://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying
               ZLog Transaction Key-Value Store: http://noahdesu.github.io/2016/08/02/zlog-kvstore-intro.html
            2. the shared log can be a foundamental building block for strong consistency distributed applications
                1. paxos can be one way of it
                   from paxos to CORFU: https://www.microsoft.com/en-us/research/publication/from-paxos-to-corfu-a-flash-speed-shared-log/
            3. postgresql can use zlog or paxos to build cluster
                1. different from the paxos, zlog replace postgresql log to enable the cluster
            4. related readings
                1. ZLog, CORFU: A Shared Log Design for Flash Clusters (Microsoft Research)    [2012, 52 refs]
                   https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/balakrishnan
                    1. a paxos cluster has the write throughput of only one node (the leader node).
                       can CORFU get aggregrate cluster write thoughput, why hold strong consistency?
                        1. no, CORFU cannot replace paxos.
                            1. CORFU only solved the consistency of find the latest tail (by a dedicated sequencer node)
                            2. but paxos needs the read-determine-write consistency across the contention of multiple node
                            3. even with a shared log, multiple node do read-determine-write and compete the log tail, invalid when found it doesn't hold the log tail
                               then, one node write, the other node all invalidate. in the end, the write throughput is still one node
                        2. something we can learn for paxos
                            1. shrink what paxos nodes control. instead of control the whole metadata logic, just arbitrate the simple log tail
                               smaller paxos responsibility should be faster
                                1. but the metadata server now needs to read-determine-write and invalidate when findout it didn't hold the latest read
                            2. client write to the paxos storage, instead let the paxos server do the write
                               this can also be seen in MegaStore where client writes to paxos data in big table
                            3. another way is to partition what paxos controls into multiple indepdent paxos group
                        3. a problem
                            1. if the flash pages a only mapped for writting logs, where can we store user data along side?
                    2. key designs
                        1. in a summary
                            1. In CORFU, each position in the shared log is mapped to a set of flash pages on different flash units
                            2. This map is maintained – consistently and compactly – at the clients
                            3. To read a particular position in the shared log, a client uses its local copy of this map to determine a corresponding physical flash page
                               and then directly issues a read to the flash unit storing that page
                            4. To append data, a client first determines the next available position in the shared log
                               – using a sequencer node as an optimization for avoiding contention with other appending clients –
                               and then writes data directly to the set of physical flash pages mapped to that position
                            5. function breakdown
                                1. A mapping function from logical positions in the log to flash pages on the cluster of flash units
                                2. A tail-finding mechanism for finding the next available logical position on the log for new data
                                3. A replication protocol to write a log entry consistently on multiple flash pages
                        2. CORFU's client-centric design
                            1. as we frequently see in modern distributed systems
                        3. Finding the tail in CORFU
                            1. use a dedicated sequencer node to obtain the log tail
                            2. flash page can only write once before erasure,
                               even without the sequencer,
                               so only one client can win
                2. From Paxos to CORFU: A Flash-Speed Shared Log (Microsoft Research)    [2012, 12 refs]
                   https://www.microsoft.com/en-us/research/publication/from-paxos-to-corfu-a-flash-speed-shared-log/
                    1. "How far is CORFU from Paxos?"
                        1. the paper doens't hit the pain point, I think ..
        7. Ceph dedup
            1. "double crush": use data's hash as the new oid
            2. "cache tier": hash the data in cache tier as a new oid
            3. online dedup: use lookup table and metadata cache when writting to the cache pool
        8. what's new in ceph Kraken
            1. RGW + ElasticSearch will be a hot feature
        9. Quantum's libcephd, i.e. rook
            1. it can use embedded ceph, as in coreos, etc.
               coreos native ceph
        10. xsky async recovery
            1. pg recovery vs backfill
            2. iops reduce 1%-2% when a node went down then up
            3. xsky's async recovery: pg recovery (based on log), don't block io
        11. gitlab因为cephfs放弃公有云
            1. 因为跑在公有云上无法保证稳定的IOPS，使用Ceph这种CP系统存在严重的性能问题
            2. "At a small scale, the cloud is cheaper and sufficient for many projects. However, if you need to scale, it's not so easy. It's often sold as, "If you need to scale and add more machines, you can spawn them because the cloud is 'infinite'". What we discovered is that yes, you can keep spawning more machines but there is a threshold in time, particulary when you're adding heavy IOPS, where it becomes less effective and very expensive. You'll still have to pay for bigger machines. The nature of the cloud is time sharing so you still will not get the best performance. When it comes down to it, you're paying a lot of money to get a subpar level of service while still needing more performance."
    5. ceph blogs
        1. Ceph冷知识 | RBD stripe_unit 与 stripe_count 大小对性能影响
           https://www.ustack.com/blog/ceph%E5%86%B7%E7%9F%A5%E8%AF%86-rbd-stripe_unit-%E4%B8%8E-stripe_count-%E5%A4%A7%E5%B0%8F%E5%AF%B9%E6%80%A7%E8%83%BD%E5%BD%B1%E5%93%8D/
        2. Predicting Ceph PG placement
           http://dachary.org/?p=4020
        3. How many objects will move when changing a crushmap ?
           http://dachary.org/?p=4003

10. readings: openstack community updates
    1. OpenStack Developer Mailing List Digest March 18-24
       https://www.openstack.org/blog/2017/03/openstack-developer-mailing-list-digest-20170324/
        1. Moving Gnocchi out: The project Gnocchi which has been tagged independent since it's inception has potential outside of OpenStack
    2. DPDK vRouter, Intelligent NFV performance with OpenContrail
       https://www.mirantis.com/blog/intelligent-nfv-performance-with-opencontrail/
    3. Kolla 2017年3月份月报
       http://www.chenshake.com/
    4. cinder blueprints
       https://blueprints.launchpad.net/cinder/+specs?direction=backwards&memo=75
    5. magnum blueprints
       https://blueprints.launchpad.net/magnum
        1. magnum-baremetal-full-support
    6. kolla blueprints
    7. dev maillist
        1. [openstack-dev] [neutron] Risk prediction model for OpenStack
        2. [openstack-dev] [Cinder] [Nova] Extend attached volume
        3. [openstack-dev] [nova] [placement] experimenting with extracting placement
    8. OpenSDS
       https://www.opensds.io/
       https://github.com/opensds/opensds

4. readings: google TPU paper published
    1. misc sources
        1. https://news.ycombinator.com/item?id=14043059
        2. https://www.nextplatform.com/2017/04/05/first-depth-look-googles-tpu-architecture/
        3. https://cloudplatform.googleblog.com/2017/04/quantifying-the-performance-of-the-TPU-our-first-machine-learning-chip.html
        4. https://plus.google.com/+JeffDean/posts/4n3rBF5utFQ
        5. from Weichat summarizing the google TPU
           http://mp.weixin.qq.com/s/3ZYrhN_rmHvjvkIU3Ifr9A
            1. "面向机器学习专用的处理器是芯片行业的发展趋势"
            2. "两年前谷歌就意识到 GPU 更适合训练，而不善于做训练后的分析决策。由此可知，谷歌打造 TPU 的动机只是想要一款更适合做分析决策的芯片"
            3. "TPU 是一款推理芯片" .. "考虑到能耗和效率的前提下，具有极高推理性能的芯片"
    2. In-Datacenter Performance Analysis of a Tensor Processing Unit​ (Google)    [2017, 0 refs]
       https://drive.google.com/file/d/0Bx4hafXDDq2EMzRNcy1vSUxtcEk/view
        1. key advantages
            1. On our production AI workloads that utilize neural network inference, the TPU is 15x to 30x faster than contemporary GPUs and CPUs.
            2. The TPU also achieves much better energy efficiency than conventional chips
            3. The neural networks powering these applications require a surprisingly small amount of code: just 100 to 1500 lines. The code is based on TensorFlow
            4. memory. The TPU's deterministic execution model is a better match to the 99th-percentile response-time requirement of our NN applications
        2. highlights
            1. custom ASIC, rather than FPGA
            2. the discussion part
                1. NN inference applications in datacenters value response time more than throughput
                2. CNNs attracts more paper (than MLPs, and prominent in NN), but they only account 5% of NN workload
            3. the conclusion part gives a summary of how TPU succeeds

5. readings: the pending papers
    1. Data Center TCP (DCTCP) (Microsoft Research)    [2010, 909 refs]
       https://www.microsoft.com/en-us/research/publication/data-center-tcp-dctcp/
        1. continued from yesterday

3. readings: Data @Scale 2017 Recap, as recommended
    1. FPGA (Doug Burger) – highly recommended - Architectures for the New Era of Cloud Specialization
        1. continued from yesterday
    2. Spanner DB (Sergey Melnik) – likely will become a huge competitive advantage for GCP - Spanner's SQL Evolution
        1. colocation of data: rows from different table but linked to the same id can be colocated on disk in the same shard
        2. Everyone wants SQL again now?
    3. Cosmos DB (Rimma Nehme) – a bit overloaded with marketing, but the capability of the system is very impressive - Next Generation of Globally-Distributed Databases in Azure
        1. Previously known as DocumentDB
        2. Cloud oriented DB (compared to SqlServer?). global distribution turn key
        3. database engine: Bw-tree, LLAMA++
    4. Cadence (Maxim Fateev) – I missed this one, but heard Georgi recommending it - Cadence: Micro-service Architecture Beyond Request/Reply
        1. like AWS serverless, inspired by AWS simple workflow service, eventhandlers

3. readings: misc papers and coding theory
    1. LLAMA: A Cache/Storage Subsystem for Modern Hardware (2013, 19 refs)
       http://db.disi.unitn.eu/pages/VLDBProgram/pdf/research/p853-levandoski.pdf
        1. good paper. it implements an general purpose page management engine, it can be
           used as the bottom part of DB implementation, or Bw-tree; like we use kv-store
           as bottom part of many distributed DBs or storage systems. the pages are mostly
           in-memory, and to disk are log-structured. it supports transactions (not complete
           but right for the needs of Bw-tree index manipulation).
        2. highlights
            1. what makes LLAMA superior performance
                1. Latch-free. Bw-tree the LLAMA are totally latch-free, even in transactions.
                   This is the best part of LLAMA. BerkeleyDB however requires page-level latches.
                2. Delta updates. In memory LLAMA appends page delta rather than write in-place.
                   BerkeleyDB however updates in-memory pages in place.
                3. Log structuring. LLAMA only writes sequentially to flash. BerkeleyDB updates
                   whole pages in place on secondary storage

    2. Horus: Fine-Grained Encryption-Based Security for Large-Scale Storage (2013, 11 refs)
       https://www.usenix.org/system/files/conference/fast13/fast13-final142.pdf
        1. Use keyed hash trees (KHTs) to generate a tree of keys and encrypt user data by access
           ranges. leaking one key of part of data won't make others vulnerable
            1. the issues are:
                1. maybe giving each user their own different key is easier? we can implement it
                   in user client or a front-end layer
                2. if data from different users are mixed, we may still be using one key to encrypt
                   data from different users.

    3. Dynamic Metadata Management for Petabyte-scale File Systems (2004, 243 refs)
       http://ceph.com/wp-content/uploads/2016/08/weil-mds-sc04.pdf
        1. dynamic sub-tree partitioning is useful to partition linux filesystem metadata. this paper
           compared it with many alternatives. but the implementation are not finished (CephFS release
           comes years after this paper). so this paper has more issue discussions than design structures.
        2. related: Mantle: A Programmable Metadata Load Balancer for the Ceph File System (2015, 8 refs)
           https://www.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-15-10.pdf
            1. it is hard to decide when to migrate sub-trees and where to cut trees.
               so, we are exposing an API framework and shift the configuration to user?

    4. Coding Techniques for Repairability in Networked Distributed Storage Systems (Fr´ed´erique Oggier)
       http://phdopen.mimuw.edu.pl/lato12/longsurvey.pdf
        1. Coding Preliminaries chapter is helpful. Finally I understand what is MDS code.

2. readings: regenerating code
    1. Network Coding for Distributed Storage Systems    [2010, 1353 refs]
       http://users.ece.utexas.edu/~dimakis/RC_Journal.pdf
        1. very good to read. this is the founding paper of regenerating code
           finally I understand what this paper is saying
        2. highlights
            1. by representing erasure code as a network information flow,
               and inspecting min-cut should allow at least M data to flow through
               the paper calculates the minimum bounds of repair bandwidth
                1. and using the network information flow multicasting theories
                2. the appendix part is good. it is the proof of how the bound is obtained
                    1. the bound is obtained by Fig. 7. G*, which is a sub-graph which can be extracted from any condition of graph G
                    2. if we could find a larger G* bound (14), we can even calculate a smaller α and β
            2. in first case, we don't expand storage data per node, and try minimize
               the repair bandwidth. this gives us the MSR code
                1. MSR code can almost easily use 0.55x bandwith than plain Reed-Solomn code
                   or even less if d is increased.
            3. in second case, we allow to expand storage data size per node, and this
               gives us even lower bound of repair bandwidth. the lowest one is MBR code
            4. this paper has been comparing itself with other code schemas
                1. replication, ideal erasure codes, hybrid, MSR, MBR
                2. hybrid: use 1 full replica and EC codes together. as long as the full replica
                   is here, we can reduce EC storage repair bandwidth by just copying from the
                   full replica.
        3. others
            1. the related works part has good introduction on what works and directions are
               in stoarge coding part. and the evaluation and analysis works on it.

4. readings: regenerating code
    1. Optimal Exact-Regenerating Codes for Distributed Storage at the MSR and MBR Points via a Product-Matrix Construction    [2011, 434 refs]
       https://people.eecs.berkeley.edu/~rashmikv/papers/product_matrix_codes.pdf
        1. key highlights
            1. This paper shows the way to construct MBR regenerating code matrix, for any [n, k, d]. good to read, it's not complex
            2. it is impossible to construct linear MSR codes for the case d < 2k - 3 of β = 1 when (see [6], [14])
               This paper also gives the method
            3. compared to "Explicit constructions of high-rate MDS array codes with optimal repair bandwidth [2016, 18 refs]"
               the later one gives a practical way to construct row-wise MDS regenerating code to cut bandwidth to 55% without storage overhead increased.
        2. for detailed math, see the paper.

7. readings: regenerating code
    1. Explicit constructions of high-rate MDS array codes with optimal repair bandwidth    [2016, 18 refs]
       https://arxiv.org/pdf/1604.00454.pdf
        1. very good paper. it is the row-wise MDS code able to regenerating 1 node failure, with 1/paritiy_count bandwidth per node
        2. highlights
            1. limitations:
                1. regenerating 1 node failure. access all n-1 surviving nodes
                2. on theory it supports any number of parity fragments. this paper gives 3
                3. row count must be parity_count^(data_frag_count + parity_count). it can be very high for long codes
            2. advantages
                1. row-wise MDS.
                2. the computation complexity for regenerating is low
                    1. sender side do an extra add for 1/parity_count of the data size
                    2. receiver side do matrix inversion for 1/parity_count of data size
                3. if we set block size of plain EC the same as the per row size here,
                   I think this coding schema can be very useful
                4. update complexity is low because it is row-wise
                5. the coding matrix is very easy to construct
            3. disadvantages
                1. need r^n rows on each node, this can be too large for long codes, such as 9+9
            4. referenced other papers who allow all parameters
                1. Minimum Storage Regenerating Codes For All Parameters    [2016, 14 refs]
                   https://arxiv.org/pdf/1602.04496.pdf
                    1. said to allow all parameters
                2. Optimal Rebuilding of Multiple Erasures in MDS Codes    [2016, 8 refs]
                   https://arxiv.org/pdf/1603.01213.pdf
                    1. allow regenerating multiple node failures
                3. these papers have their limitations: rely on existential lemmas in large finite fields,
                   e.g., the Schwartz-Zippel lemma or Combinatorial Nullstellensatz

8. readings: regenerating code papers
    1. Simple Regenerating Codes: Network Coding for Cloud Storage [2011, 140 refs]
       https://arxiv.org/pdf/1109.0264.pdf
        1. good to read. it use first Reed-Solomn code and then a 3-row XOR array code.
           but cross placing chunks, it can do regenerating. If you are willing to give
           off 1/3 storage space, the code is very good to implement a regenerating code.
           it is being tried on Hadoop.
        2. referred by "HDFS-RAID使用Erasure Code来实现HDFS的数据冗余"
           http://blog.csdn.net/wk022/article/details/49506643
            1. As hadoop is trying to use simple regenerating code to improve EC
               https://issues.apache.org/jira/browse/HDFS-3544
            2. another for hadoop: Locally Repairable Codes, (LRC)
               http://smahesh.com/HadoopUSC/ - XORing Elephants: Novel Erasure Codes for Big Data
        3. highlights
            1. advantages
                1. super simple
                2. only needs XOR for regenerating repair, which is much faster than matrix inversion decode
                3. regenerating node repair needs constant d==4 other nodes. needs constant 6 chunks (each size M/2/k).
                   when k is large, the bandwidth saving is significant
            2. disadvantages
                1. need extra 1/3 storage space

    2. Minimum Storage Regenerating Codes For All Parameters    [2016, 14 refs]
       https://arxiv.org/abs/1602.04496
        1. using interference alignment, allow MSR code for all (n, k, d) parameters, which is know to be
           impossible previously. but this papper did it by limit to systematic-repair only, need large row count
           on each node, and need large galois field size
        2. highlights
            1. disadvantages
                1. limited to systematic-repair, i.e. only repair failed data fragments
                2. need a=n^k rows on each node. for long codes like 9+9, row_count=18^9 which can be impossible
                3. need very large galois field size, which is unfavorable for real implementation
            2. advantages
                1. MSR code for all (n, k, d), which is previously known to be impossible in some case.
                   but systematic-repair only and large galois fields size made it possible

    3. Optimal Rebuilding of Multiple Erasures in MDS Codes    [2016, 8 refs]
       https://arxiv.org/abs/1603.01213
        1. improved from Zigzag code to be able to regenerating multiple erasures.
           very few regenerating code can do this
        2. highlights
            1. using previous work Zigzag codes by same authors
            2. advantages
                1. besides recover erasured nodes, this code is able to correct errors together
                   but, isn't checksum the cheaper way to do it? (unless we want to save the space)
                2. regenerating code to rebuild multiple erasures simultaneously, this is the main feature.
                   but for a single node, what's the purpose to obtain all the erasured fragments?
            3. disadvantages
                1. limited to systematic-repair only
                2. need r^(k-1) rows on each node, which is relatively too big
                3. need large enough galois finite field

4. readings: erasure coding survey
    1. Erasure Codes for Storage Systems: A Brief Primer
       https://www.usenix.org/system/files/login/articles/10_plank-online.pdf
        1. very good survey on erasure-coding status. there are a few categories of codes
            1. RAID-4 and RAID-5, Linux RAID-6
            2. Reed-Solomon Codes
            3. Array Codes. Examples are RDP code, EVENODD, etc
            4. Recent works
                1. Reduced disk IO for recovery. e.g. RDP code
                2. Regenerating codes
                3. Non-MDS codes
                    1. Flag XOR codes
                    2. local reconstruct codes
                    3. sector-disk (SD) codes
        2. besides
            1. Intel SSE2 and AVX instructions are important for implementing efficient galois operations
    2. 柯西编解码过程优化
       http://alanwu.blog.51cto.com/3652632/1410132
    3. EC编码优化
       https://web.eecs.utk.edu/~plank/plank/papers/CS-05-570.html

2. readings: write notes for papers read

    ---- Misc papers ----

    1. Malacology: A Programmable Storage System    [2017, 0 refs (not published yet)]
       https://www.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-17-04.pdf
        1. Initially Ceph invented the dynamic subtree partitioning to manage CephFS metadata
             Dynamic Metadata Management for Petabyte-scale File Systems
             http://ceph.com/wp-content/uploads/2016/08/weil-mds-sc04.pdf
           After CephFS implementation ready, authors found allowing endusers to customize metadata partition/migration/balancing strategy is necessary. Thus Mantle API came out
             Mantle: A Programmable Metadata Load Balancer for the Ceph File System
             https://www.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-15-10.pdf
           Now, in this paper, authors combine all Ceph originated enduser customizable APIs, as Malacology, the programmable stoage system. Also, the ZLog stuff is put in
           Interesting paper. Worth read
        2. Highlights
            1. Service Metadata Interface: the MON paxos is exposed as API
               Data I/O Interface: Ceph originally has the dynamic object interface by Lua
               Distributed Metadata Interface: CephFS metadata allows policies
               File Type Interface: Allows customize inode types
               Load Balancing Interface: CephFS metadata load balancing allows policies; policies can be stored in MON or OSD
               Durability Interface: Ceph OSD
            2. Services built on Malacology
                Mantle: Programmbale load balancer for CephFS metadata. policies are stored in MON or OSD. use Lua to program
                ZLog: A fast distributed shared log. sequencer uses File Type interface, to make itself a shared file
                      the sequencer implementation is interesting and crucial for ZLog performance

    ---- Coding theory ----

    2. Optimizing Cauchy Reed-Solomon Codes for Fault-Tolerant Storage Applications    [2006, 208 refs]
       http://web.eecs.utk.edu/~plank/plank/papers/CS-05-569.pdf
        1. very good paper. after all these EC code study, though there are many fancy ones,
           RS code (or those based on RS code) is still the most suitable one for practical use.
           this paper gives the important computational optimization for RS code encoding/decoding
        2. highlights
            1. many codes use only XOR, this is fast, but won't achieve best recoverability against storage overhead.
               RS code needs galois multiplication more than XOR.
            2. how RS code get fast to compute today
                1. Intel SSE/AVX instructions (vector instruction sets) allow GF (galois field) multiply operations to be much faster
                   Erasure Codes for Storage Systems A Brief Primer: http://web.eecs.utk.edu/~plank/plank/papers/Login-2013.pdf
                    1. there are techniques such as make all matrix coefficients as power of 2 (Linux RAID-6)
                2. CRS code - Cauchy Reed Solomon code use Cauchy matrix instead of Vandermonde maxtrix
                    1. with CRS, word size w can be selected as small as possible, rather than limited by 4, 8, 16
                    2. ((n + m) * n) cauchy code matrix, all n*n submatrices may be inverted in O(n^2) GF operations [Rab89]
                    3. use projects to covert operations over GF into XORs. this is genius. see paper for graphic illustration
                        1. every element e in GF(2^w) can be represented by a 1 × w column vector of bits, V (e), or a w × w matrix of bits, M(e)
                        2. the i-th column of M(e) is equal to the column vector V (e^(2^(i−1)))
                        3. M(e1) * V (e2) = V (e1e2), M(e1) * M(e2) = M(e1e2)
                        4. So, GF(2^w) is projected onto GF(2), where multiply is also XOR.
                           the computation now take place on plain bits, so w doesn't need to be multiply of 8
                           and, the number of 1's in cauchy matrix corresponds to XOR count
                        4.5. encoding: O(nlog(n+m)), decoding O(n^2)
                        5. another material: 基于柯西矩阵的Erasure Code技术详解
                           http://alanwu.blog.51cto.com/3652632/1410132
                4. Cauchy with less 1's has less XOR count in encoding
                   So, find optimal cauchy matrix with minimal 1's after projected to GF(2)
                    1. some general experience: larger w has more 1's in general. small w is favorable
                       (but there are some exceptions, detail in paper)
                    2. the author spent much effort on enumerating matrices to find optimal ones with different (n, m, w)
        3. related materials
            1. Optimizing Galois Field Arithmetic for Diverse Processor Architectures and Applications
               http://www.kaymgee.com/Kevin_Greenan/Publications_files/greenan-mascots08.pdf
                1. multiplication requires a variety of implementation techniques that depend on hardware, memory, co-processing elements and word size w

    3. Coding Techniques for Repairability in Networked Distributed Storage Systems (Fr´ed´erique Oggier)
       http://phdopen.mimuw.edu.pl/lato12/longsurvey.pdf
        1. very good reading. this part I start to read Part II to end of paper.
           this paper here provides the general framework of what categories of EC codes we have
        2. highlights
            1. beyond of RS code. there are many directions of current EC code study
               (another paper has similar summary is: Erasure Codes for Storage Systems A Brief Primer
                http://web.eecs.utk.edu/~plank/plank/papers/Login-2013.pdf)
                1. reduction in overall data transfer over the network
                    1. the example is regenerating codes. they reduce total network traffic,
                       but likely to increase number of network IOs, and usually cannot repair multiple faults
                2. reduction in the number of nodes contacted, i.e. repair fan-in
                    1. Simple regenerating codes, Flat XOR codes
                3. reduction in the amount of data that needs to be read from the live nodes, i.e. disk I/O
                    1. RDP codes
                4. possibility to repair multiple faults
                    1. LDPC codes can do it. and RS based codes, such as LRC. and some specially designed regenerating codes.
                5. possibility to distribute the repair load and parallelize the repair process and
                    1. Ceph PG scattered around OSDs
                6. reduction in the time to complete repairs
                    1. first, it is Codes on Codes. a simple example "Product Codes"
                    2. next Hierarchical Codes [11], Pyramid Codes [19] and Local Reconstruction Codes [18], they two are famous
                    3. others, Cross-object Coding
                    4. Locally Repairable Codes
                        1. Self-Repairing Codes (most paper published by this author F. Oggier)
                        2. Punctured Reed-Mueller Codes
            2. Besides, we have many XOR based codes: LDPC code, RDP code, Flat-XOR codes, X-Code, etc

    4. Optimal Recovery of Single Disk Failure in RDP Code Storage Systems    [2010, 98 refs]
       http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.439.9023&rep=rep1&type=pdf
        1. RAID-6 uses double XOR parities. The clever way is one parity for row and another for diagonal, i.e. RDP.
           RDP tolerates 2 disk failures at most. RDP uses only XOR operation. RDP needs n+2 storage overhead.
           This paper RDOR improves how to recover with 1 disk failure. It uses two parties together,
           and the algorithm achieves minimal disk read IO, and balance read against all disks.
           there is extensive math analysis to find the optimal disk reads and load balance point.
        2. RDP is a very classic XOR based code, besides this paper, there are many improvements on it.
           It is frequently used in RAID.
        3. EMC XtremIO is using XDP, which is similar to RDP.
           https://www.emc.com/collateral/white-paper/h13036-wp-xtremio-data-protection.pdf

    5. Flat XOR-based erasure codes in storage systems: Constructions, efficient recovery, and tradeoffs    [2010, 74 refs]
       https://pdfs.semanticscholar.org/09be/d5a75cbdba4b930cdca6bd2499d61121e030.pdf
        1. If you want a "small" LDPC code, that's Flat XOR. It is a much faster code than RS/MDS codes, with bigger storage overhead compared to recoverability
           Generally, the storage overhead is ~1.5, tolerage fragment falure is 2~3, recovery fan-in is ~5-10, read load can be ~0.2-0.5
           this papers propose the code construction and recovery schedule methods.
           but compared to usually used MDS code, flat XOR needs k=5 to 30, this is still relatively long. long codes are bigger probability to fail for all fragments
        2. related works
            1. compared to LRC code, LRC uses less storage overhead, when provide similar or smaller local recovery cost
               https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/LRC12-cheng20webpage.pdf

    6. X-Code: MDS Array Codes with Optimal Encoding    [1999, 354 refs]
       http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.30.9205&rep=rep1&type=pdf
        1. It's array code, the 2 parity row it attached at bottom. Each parity encodes left or right diagonal with only XOR. So, it looks like a big X.
           the update is optimal, with complexity 2. the code recovers at most 2 failures, with n+2 storage overhead, it's MDS.
        2. thinkings
            1. the optimal update complexity 2 is not uncommon. this is by nature for array code.
               if not array code, e.g. just plain RS, we can use 2 parities, and each encode packet is small.
               the update complexity is the same, i.e. 2 parity packets

    7. LDPC Codes: An Introduction
       https://www.ics.uci.edu/~welling/teaching/ICS279/LPCD.pdf
        1. LDPC codes usually have many data/parity fragments, i.e. the code is large. Parities only use XOR. Each parity covers some data fragments.
           The code matrix is a sparse matrix containing only 1's. LDPC can be ~2 storage overhead, low computation cost, and able to recover from large amount of fragment erasures.
           The code matrix can even be randomly generated. Using iterative belief propagation techniques, LDPC codes can be decoded in time linear to their block length
           There are extensive researches on LDPC. LDPC code is rarely used in storage, but much in network communication (10GBase-T Ethernet, Wi-Fi 802.11)
        2. other LDPC introductions
            1. Low-density parity-check code
               https://en.wikipedia.org/wiki/Low-density_parity-check_code
               https://zh.wikipedia.org/wiki/%E4%BD%8E%E5%AF%86%E5%BA%A6%E5%A5%87%E5%81%B6%E6%AA%A2%E6%9F%A5%E7%A2%BC
            2. Introduction to LDPC Codes
               http://circuit.ucsd.edu/~yhk/ece154c-spr15/ErrorCorrectionIII.pdf
            3. A Practical Analysis of Low-Density Parity-Check Erasure Codes for Wide-Area Storage Applications
               http://loci.cs.utk.edu/lors/files/DSN-2004.pdf
        3. some comments
            1. "When the ratio of networking performance to CPU speed is high enough, LDPC codes outperform their MDS alternatives.
                However, when that ratio is lower, MDS codes perform better [PT04, CP05]."
                -- [Optimizing Cauchy Reed-Solomon Codes for Fault-Tolerant Storage Applications](http://web.eecs.utk.edu/~plank/plank/papers/CS-05-569.pdf)
            2. "LDPC ... had a significant impact in networked and communication systems ... The appeal of LDPC is that, for large such codes,
                a small amount of space-efficiency can be sacrificed to significantly reduce the computation costs required to encode and decode data over lossy channels"
                -- [Flat XOR-based erasure codes in storage systems: Constructions, efficient recovery, and tradeoffs](https://pdfs.semanticscholar.org/09be/d5a75cbdba4b930cdca6bd2499d61121e030.pdf)

    8. Pyramid Codes: Flexible Schemes to Trade Space for Access Efficiency in Reliable Data Storage Systems    [2007, 283 refs]
       https://staff.ie.cuhk.edu.hk/~mhchen/papers/nca.07.pyramid.codes.pdf
        1. good paper. one of the founding paper of locality codes. basic pyramid code is to break a parity in RS code into two, each covering half of data fragments
           generalized pyramid code has parities each cover a group of data fragments, groups may overlap, and code matrix should achieve "Maximally Recoverable"
           the paper also gives an interesting algorithm to construct optimal matrix, by using null space vector, see III.C.3.
           Besides, the pyramid code can be applied in other code, including those XOR codes, such as RDP, X-Code, EVENODD, B-Code, CPM
           It can also be optimized by the Cauchy Reed-Solomon code optimization techniques
        2. founding papers of locality codes
            1. "Code locality was identified as a good metric for repair cost independently by Gopalan et al. [14], Oggier et al. [6], and Papailiopoulos et al. [15]"
               ---- as in [Locally Repairable Codes](http://www-scf.usc.edu/~papailio/repair_locality_ISIT_short.pdf)
                [14] P. Gopalan, C. Huang, H. Simitci, and S. Yekhanin, "On the Locality of Codeword Symbols," Preprint available at http://arxiv.org/abs/1106.3625.
                [6] F. Oggier and A. Datta, "Self-repairing homomorphic codes for distributed storage systems," in Proc. IEEE Infocom 2011, Shanghai, China, Apr. 2011.
                [15] D. S. Papailiopoulos, Jianqiang Luo, Alexandros G. Dimakis, C. Huang, and J. Li,
                     "Simple Regenerating Codes: Network Coding for Cloud Storage", accepted in IEEE International Conference on Computer Communications (Infocom) 2012, Miniconference
        3. related papers
            1. On the Locality of Codeword Symbols
               https://arxiv.org/abs/1106.3625
                1. gives the math analysis of lower/upper bounds of locality with other codec parameters, such as
                   disk/network IO count, transmitted bandwidth, recoverability, update cost, storage overhead, etc
            2. Erasure Coding in Windows Azure Storage
               https://www.usenix.org/system/files/conference/atc12/atc12-final181_0.pdf
                1. this paper proposed the LRC code used in Azure. it is a generalized pyramid code
        3. algorithm to construct optimal coding matrix
            1. the algorithm finds the next row one by one. each row needs to be linear independent with previous each (n-1) row selection, i.e. the recovery submatrix
            2. for each recovery submatrix, find the null space vector uj, then next_row * uj != 0 is required. if it == 0,
               make next_row <- next_row + e * uj. this guarantees next_row * uj != 0.
            3. to maintain the previous each recovery submatrix still have the != 0 property, we filter out bad e's.
               a bad e is the e to make ui * (next_row + e * uj) == 0

    9. On the Locality of Codeword Symbols    [2011, 328 refs]
       https://arxiv.org/pdf/1106.3625.pdf
        1. this paper analysis with extensive math the locality tight lower/upper bounds for parity codes against hamming distance d recoverability and a broad class of parameter settings
           it outlines the complete picture of the tradeoffs between codewords length, worst-case distance and locality of information symbols
           interesting paper to read. need to fully understand the math. key conclusion: n − k >= roof(k/r) + d - 2, and equality can be achieved (Canonical Codes).

    ---- Reliability in storage ----

    10. Availability in Globally Distributed Storage Systems    [2010, 387 refs]
        https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Ford.pdf
        1. Good paper. based on 1-year study in Google on live operations. it reveals the importance of modeling correlated failures when predicting availability.
           and introduced multi-cell replication schemes in the reliablity Markov model. Findings show correlated failure makes recovery rate ineffective to improve MTTF.
        2. highlights
            1. works done in google
                1. Compare mean time to failure for system components at different granularities, including disks, machines and racks of machines. (Section 3)
                2. Classify the failure causes for storage nodes, their characteristics and contribution to overall unavailability. (Section 3)
                3. Apply a clustering heuristic for grouping failures which occurs almost simultaneously and
                   show that a large fraction of failures happen in bursts. (Section 4)
                4. Quantify how likely a failure burst is associated with a given failure domain.
                   We find that most large bursts of failures are associated with rack- or multirack level events. (Section 4)
            2. Nodes can become unavailable for a large number of reasons
                1. For example, a storage node or networking switch can be overloaded;
                   a node binary or operating system may crash or restart;
                   a machine may experience a hardware error;
                   automated repair processes may temporarily remove disks or machines;
                   or the whole cluster could be brought down for maintenance
                2. The vast majority of such unavailability events are transient
                    1. less than 10% of events last longer than 15 minutes
                    2. data is gathered from tens of Google storage cells, each with 1000 to 7000 nodes
                    3. GFS typically waits 15 minutes before commencing recovery of data
                3. ARR is between 2% and 4% as reported in study [29]
                     Disk failures in the real world: what does an MTTF of 1,000,000 hours mean to you?
                     http://www.cs.toronto.edu/~bianca/papers/fast07.pdf
                   [19] also find 2% ~ 4%, but for some it can be 3.9% ~ 8.3%
            3. Correlated failures is critical for availability
                1. observed 37% of failures are part of a burst of at least 2 nodes
                2. Two broad classes of failure bursts can be seen in the plot
                    1. a large number of failures in quick succession, e.g. a DC power outage
                    2. a smaller number of nodes failing at a slower rate at evenly spaced intervals, e.g. rolling upgrade
                3. the paper defines a score, sum(ki * (ki - 1) / 2), ki is failure in i-th rack, to compare the rack concentration
                   and also the rack affinity score, 0.5 for random busrt, close to 1 for rack-correlated, close to 0 for anti-correlated
                    1. the finding is, larger failure bursts have higher rack affinity
                       all failures of 20+ nodes have rack affinity > 0.7, and 40+ nodes failure with > 0.9
                4. for placement
                    1. rack-aware placemnet policy is better than uniform random placement
                    2. in general
                        1. placement deals with burst failure
                        2. network speed deals with long term reliability (repair needs to be faster than failures)
            4. Markov model for stripe availability
                1. Weibull has better fit for disk MTTF. but the exponential distribution is enough
                2. correlated burst failures are added into the model,
                   i.e. failure events are independent of each other, but each event may involve multiple chunks
                3. MTTF is calculated in standard method in [27] Adventures in stochastic processes
                4. extend model to multi-cell (multi-DC)
                    1. treat each cell as a ‘chunk' in the multi-cell ‘stripe'
                5. findings
                    1. importance of recovery rate
                        1. with no correlated failures reducing recovery times by a factor of µ will increase stripe MTTF by a factor of µ^2 for R=3 and by µ^4 for RS(9, 4)
                           Reducing recovery times is effective when correlated failures are few
                        2. However, when correlated failures are taken into account, even a 90% reduction in recovery time results in only a 6% reduction in unavailability
                    2. failing to account for correlation of node failures typically results in overestimating availability by
                       at least two orders of magnitude and eight in the case of RS(8,4)
                    3. hardware failure rate
                        1. find that improvements below the node (server) layer of the storage stack do not significantly improve data availability
                           (latent disk error rate, disk failure rate)
                        2. On the other hand, cutting node failure rates by 10% can increase data availability by 18%
                    4. multi-cell
                        1. Replicating data across multiple cells (data centers) greatly improves availability because it protects against correlated failures
                        2. This introduces a tradeoff between higher replication in a single cell and the cost of inter-cell bandwidth
            5. Some recommendations made by this framework in google
                1. Determining the acceptable rate of successful transfers to battery power for individual machines upon a power outage
                2. Focusing on reducing reboot times, because planned kernel upgrades are a major source of correlated failures
                3. Moving towards a dynamic delay before initiating recoveries, based on failure classification and recent history of failures in the cell

    11. Efficient Replica Maintenance for Distributed Storage Systems    [2006, 295 refs]
        http://www.cis.upenn.edu/~ahae/papers/carbonite.pdf
        1. highlights
            1. key ideas
                1. durability algorithm must create replicas faster than permanent disk failures destroy it
                2. increasing the number of replicas doesn't help a system tolerate a higher disk failure probability,
                   but does help tolerate bursts of failures
                3. the equilibrium number of replicas: θ=µ/λf, i.e. replica creation rate / replica failure rate
                   if the system has more replicas, it cannot catch up to recover them. when
            2. others
                1. how to choose replica count, should 1) <= θ 2) tolerate large enough burst for acceptable MTTF
                2. improve repair time: large node scope, i.e. how wide the node's replica are scattered.
                                        however large scope increase monitoring load, and increase data loss possibility (more node-loss combinations turn into data loss)
                3. reduce transient costs: reintegrate object replicas stored on nodes after transient failures
                                           create replicas as needed, in batch
                                           use timeouts, failures are consider transient before timeout

    12. Reliability Mechanisms for Very Large Storage Systems    [2003, 220 refs]
        https://www.crss.ucsc.edu/Papers/xin-mss03.pdf
        1. analyzing what reliability mechanism is enough for PB-level system.
           2-way mirroring should be enough. 3-way mirroring or mirroring combined with RAID for high reliability.
            1. this is not what today has. today its EB-level system 3-way mirroring and EC coding
            2. there are fast recovery mechanisms proposed, they are already common today

    13. When MTTDLs Are Not Good Enough: Providing Better Estimates of Disk Array Reliability     [2008, 12 refs]
        https://www.ssrc.ucsc.edu/Papers/paris-i2ts08.pdf
        1. conventional MTTDL approach generally provides good estimates of the long-term reliability of repairable disk arrays,
           but significantly underestimates their short-term reliability
        2. proposed a technique reducing the margin of error by assuming that the disk array was replaced at frequent intervals
           found same MTTDL approach provided fairly good estimates of the reliability of repairable redundant disk arrays as long as
           the individual disk repair rate remained well above one thousand times the individual disk failure rate
        3. how to evaluate the reliability of complex redundant disk arrays that are not promptly repaired within hours of a disk failure
           The best alternative will be to turn to discrete simulation techniques

    14. Reliability Challenges for Storing Exabytes
        https://pdfs.semanticscholar.org/17e7/c943d15d9cc808393d0541f4c087bb18cefc.pdf
        1. we consider only two causes for dataloss, namely full disk failure and latent disk errors
           future also add losses due to operational errors, physical brick failure, losses due to networking outages, and generic catastrophes such as flooding
        2. LSE (Latent Sector Errors) seem to be highly correlated
        3. rather than a blind insistence on building using ever more reliable individual components,
           we advocate the building f more reliable architectures that can inform reliable data placement based on the physical nature of the underlying infrastructure
        4. Simply building exascale storage systems as a conglomeration of more reliable individual nodes will not scale

    15. Mean time to meaningless: MTTDL, Markov models, and storage system reliability    [2010, 61 refs]
        https://www.usenix.org/legacy/event/hotstorage10/tech/full_papers/Greenan.pdf
        1. MTTDL is meaningless
            1. MTTDL literally measures the expected time to failure over an infinite interval.
               This may make the MTTDL useful for quick, relative comparisons, but the absolute measurements are essentially meaningless
               E.g. probablity of data loss for every year for the first 10 years of a system
            2. Weibull distributions are more successful in modeling observed disk failure behavior, but we are using exponential distribution
            3. Latent sector failures exhibit significant correlation both temporally and spatially within a device
               Pareto distributions can best capture the burstiness of latent sector errors, as well as spatial and temporal correlations [11]
            4. Disk repair activities such as rebuild and scrubbing tend to require some fixed minimal amount of time to complete
            5. Memorylessness, Failure & Repair. aging is not considered.
               and previous rebuilding is discarded after transited to new state
        2. better matric, NOMDL: expected amount of data lost (in bytes) in a target system within mission time t
            1. recommend to use Monte Carlo simulation to calculate NOMDLt
            2. Many iterations of the simulator are required to get statistically meaningful results

    ---- Archival storage ----

    16. Understanding Data Survivability in Archival Storage Systems    [2012, 8 refs]
        http://alumni.soe.ucsc.edu/~yanli/res/li-systor12.pdf
        1. In most archival storage systems, data are replicated across several systems, sites, and backup media,
           so the survivability of the data is based on the combined reliability of these storage
        2. using Weibull reliability model
        3. it's not using markov model, but Psurvival = 1 - Ploss1 * Ploss2 * ..
        4. disk scrubbing is agreed to be an important feature for archival systems
        5. leverage the S.M.A.R.T events: [23] found that a group of drives with Scan Errors are ten times more likely to fail

    17. Disk Scrubbing in Large Archival Storage Systems    [2004, 160 refs]
        https://www.ssrc.ucsc.edu/Papers/schwarz-mascots04.pdf
        1. it looks like very beginning paper of archival storge. it says to have proposed "data scrubbing"
        2. disk MTTF uses 1.5E6 hours is AFR=8766/1.5E6=~0.5%, this is too low, should be AFR 2~4%
        3. scrubbing disk techniques
            1. scrub only when they are powered on
            2. scrub by read data and compare with stored signature
            3. power-on a disk lowers its reliability

    16. Pergamum: Replacing Tape with Energy Efficient, Reliable, Disk-Based Archival Storage    [2008, 176 refs]
        https://www.usenix.org/legacy/event/fast08/tech/full_papers/storer/storer_html/
        1. good reference as an archival storage.
        2. highlights
            1. compared to MAID (Massive Arrays of Idle Disks) who uses centralized controller,
               Pergamum uses CPU per storage node. it relies on each CPU to be slow and power cheap.
               it brings operational convenience that each storage node can be directly replaced.
            2. Pergamum add NVRAM to each node, so that disk don't need to be powered up, and they can
               do store signatures or compare them, defer writes, metadata requests.
               the foundamental truth is NVRAM is more power cheap than power-on disks
            3. Pergamum is able to keep 95% disks power-off in all time. This is the key to save energy.
                1. I does worry about its sustaining write ingesting throughput,
                   which is important if we want to use it in cloud for customers along side blob/object storage
            4. rebuild and data scrubbing are lazy, they try to only take place on powered on disks.
               as author suggests, with intra-disk and inter-disk redundancy (e.g. (n+2)+2),
               scrubbing once per year is enough for reliablity
            5. data scrubbing use hash-tree signature to do comparison, thus save reads and data transmitted
            6. deferred write, pass write delta, surrogate writes, needs only 2 disk active in same time per update.
            7. data scrubbing also checks disk SMART status to choose target disks

    ---- Misc ----

    17. Improving Disk Array Reliability Through Expedited Scrubbing    [2010, 11 refs]
        https://www.ssrc.ucsc.edu/Papers/paris-nas10.pdf
        1. on RAID-6, we propose to start an urgent scrubbing scan whenever we detect a failure of one of the array disks

    18. Efficiently Identifying Working Sets in Block I/O Streams    [2011, 21 refs]
        https://www.ssrc.ucsc.edu/Papers/wildani-systor11.pdf
        1. place physical protocol analyzer on storage bus, group by calculating distance, support multiple application accessing.
           distance is computed from time diff and file offset diff. next use kNN clustering or graph clique covering to determine groups.

    ---- Erasure coding ----

    19. In Search of I/O-Optimal Recovery from Disk Failures     [2011, 45 refs]
        https://www.usenix.org/conference/hotstorage11/search-io-optimal-recovery-disk-failures
        1. good, this paper finds the code to minimize recovery IO at given fault tolerance sacrificing storage overhead
           propose a new code, using only XOR, each paritiy covers two data symbols.
           in each failure case how to recovery needs to be calcuated a priori
           the recovery strategy calculating is an NP-hard problem,
           the paper uses a tree graph for it, graph depth equals to number of failures.
           basically it is enumeration search of using all recovery equation combinations, and use Dijkstra's algorithm to find shortest path
        2. the code is based on Flat XOR code
           "We solve the problem of determining how to recalculate the lost data
            while minimizing the total number of surviving bits that are read"
        3. there is a fundamental trade-off between recovery IO vs storage overhead at a given fault tolerance
            1. MDS minimize storage overhead
            2. this code gives mimize IO cost
            3. In between these extrema, lie codes that increase storage overhead and reduce recovery I/O,
               such as GRID/Weaver code
        4. it's like an extreme LRC with only overlaping local parities, and don't need GF multiply coefficients
            1. not sure how it compares with MBR regenerating code, though the latter tends to increase IO count but has less network traffic.
               and MBR regenerating code also does brings more storage overhead

    -- 20171011 --

    20. Rethinking Erasure Codes for Cloud File Systems: Minimizing I/O for Recovery and Degraded Reads    [2012, 235 refs]
        https://www.usenix.org/conference/fast12/rethinking-erasure-codes-cloud-file-systems-minimizing-io-recovery-and-degraded
        0. good paper to read. first part of the paper is the algorithm to find optimal recovery scheduling for less symbols
           next the method is used for degraded read, to reduce io, by merge user-read symbols into recovery-needed symbols
           next it proposed rotated reed solomon code, like the RDP, rotation makes recovery equations easier to be lucky to cover user-read symbols,
           and for disk rebuild, like RDP optimal recovery, we can use two parities for one disk failure to reduce IO
           however, in later LRC papers such as Pyramid Codes, authors think rotated RS code saving 20-30% is inferior than LRC
        1. highlights
            1. the paper follows "In Search of I/O-Optimal Recovery from Disk Failures" with same authors
            2. the related works and backgrond introduction is good. it covers most codec works and tells their core features
        2. related work
            1. previous simpler work: "In Search of I/O-Optimal Recovery from Disk Failures"
            2. as referenced in LRC paper later, they said LRC is better in saving IOs
                1. "The savings of these schemes are typically around 20%-30% [Khan et al. 2011, 2012; Xiang et al. 2010], much less than pyramid codes."
                   Pyramid codes: https://staff.ie.cuhk.edu.hk/~mhchen/papers/pyramid.ToS.13.pdf

    21. The RAID-6 Liber8tion Codes    [2008, 182 refs]
        https://www.usenix.org/legacy/event/fast08/tech/full_papers/plank/plank_html/
        1. Liber8tion is frequently referenced in other papers for compare. It has good recovery properties as reducing 30% IO (said in "Rethinking .." paper).
           The name is for the freedom of constructing RAID-6 codes. Liber8tion code is defined on Coding Distribution Matrix (CDM), see 3.3.
           It uses only XOR. It achieves lower bound of number of 1's in matrix. It is MDS code. It even outperforms RDP codes in some parameters.
           The paper uses "bit matrix scheduling" to find the optimal recover equations for a failure, thus reduce XOR count.
           the schedules can be precalculated and cached (since it tolerates 2 disk failure at most)
        2. highlights
            1. the related works & background part is good, as it summarized typical codes for RAID-6
                 RS code -> Parity Array: EVENODD -> RDP. X-Code however doesn't fit RAID-6 specification;
                 STAR code is for than two failures, it boils down to EVENODD still

    22. STAR: An Efficient Coding Scheme for Correcting Triple Storage Node Failures    [2005, 233 refs]
        https://www.usenix.org/legacy/event/fast05/tech/full_papers/huang/huang.pdf
        1. STAR is modified EVENODD code that tolerate 3 disk failures. it is MDS.
           Recovery achieves lower bound of 3 XORs per symbol. (EVENODD up to 10 XORs)
        2. highlights
            1. STAR uses p+3 columns, first 2 parity columns are same with EVENODD.
               the 3rd parity column is slop -1 rather than slop 1 of EVENODD 2nd parity
            2. decoding steps are illustrated in section 4.
               after finding a start point, there can be multiple crosses choosen

    ---- Coding theory ----

    23. Optimizing Galois Field Arithmetic for Diverse Processor Architectures and Applications    [2008, 53 refs]
        http://www.kaymgee.com/Kevin_Greenan/Publications_files/greenan-mascots08.pdf
        1. composite field technique, agnostic to hardware. GF(2^l) => GF(2^n = 2^l^k), so that large field 2^32 is reducted to 2^8 or smaller
           pinning entire lookup table in cache help improve performance. and there are many evaluation and observation experiences
           and, application-specific optimizations for composite fields can further improve performance (figure 4(d))
           the related works section tells more about GF operation implementation works and status
        2. existing table lookup methods for GF mul and optimizations
            1. log/antilog lookup table needs O(n) space. but needs to 3 table lookup for a multiply
            2. left-right table, breaks multiplier into left & right part, and lookup in two smaller tables, left-table and right-table
            3. more table lookup optimizations, see table 1

    24. Jerasure: A Library in C/C++ Facilitating Erasure Coding for Storage Applications - Version 1.2    [2007, 271 refs]
        https://web.eecs.utk.edu/~plank/plank/papers/CS-08-627.pdf
        1. the famous EC library that Ceph is using. For Jerasure 1.2, it adds Blaum-Roth and Liber8tion codes.
           it has many codec implementations, can be used for the RAID ones and cloud storage CauchyRS/MDS codes
           the code word w is typically 8, 16, 32

    ---- Erasure coding ----

    25. EVENODD: An Efficient Scheme for Tolerating Double Disk Failures in RAID Architectures     [1995, 682 refs]
        https://authors.library.caltech.edu/29320/1/BLAieeetc95a.pdf
        1. very classic, very old. many new codes are based on EVENODD. like STAR, RDP, liber8tion, etc.
           basically it gave us the first different and good code from RS.
           EVENODD tolerates 2 disk failures, uses only XOR, achieves MDS, and has good encode/recovery performance.
           The two parity column of it provides horizontal redundancy and diagonal redundancy
        2. related materials
            1. "The RAID-6 Liber8tion Codes" has introduction to EVENODD code

    26. Rebuilding for Array Codes in Distributed Storage Systems    [2010, 73 refs]
        https://arxiv.org/abs/1009.3291
        1. improved version of EVENODD code to minimize recovery IO. To build one data node erasure, only 3/4 information symbols need to be transimitted.
           it borrowed some idea from regenerating code [8], to calculate middle block and transimit it instead of transimit whole data
        2. materials
            1. referenced in "In Search of I/O-Optimal Recovery from Disk Failures" as the EVENODD code

    27. Self-repairing Homomorphic Codes for Distributed Storage Systems    [2010, 190 refs]
        https://arxiv.org/pdf/1008.0064.pdf
        1. interesting paper. together with "On the locality of codeword symbols", "Simple Regenerating Code", this paper first introduced "locality" to codecs.
           self-repairing codes: not systematic, not MDS, lost parities can reconstruct from a subset of fixed number-ed other parities.
           the code construction is Homomorphic SRC: encode needs mul but recover only needs XOR;
             it uses interesting polynominal operations and p(a+b) = p(a) + p(b). an parity can be obtained as a linear combination of other parities
        2. related materials
            1. Coding Techniques for Distributed Storage Systems (by Fr´ed´erique Oggier)
               http://phdopen.mimuw.edu.pl/lato12/LectPoland.pdf
                1. this is almost the same material of content with F.Oggier's long survey "Coding Techniques for Repairability in Networked Distributed Storage Systems"
                   but it tells more detail about Self-repairing Homomorphic Codes
                2. in chapter 1, there is actually very good intro to Galois Field

    28. Locally Repairable Codes    [2012, 280 refs]
        https://arxiv.org/abs/1206.3804
        1. very good paper. authored by D. S. Papailiopoulos, together with F.Oragger, P. Gopalan, ChengH, they proposed the "locality" in EC codecs
           "On the Locality of Codeword Symbols" prooves that, when each node has entropy a=M/k (or say data size), recoverability bound d<=n-k-roof(n/r)+2
           this paper allows a=(1+e)M/k, allow sacrificing storage ovhead, to maximize reliability, for given locality r: d<=n-roof(k/(1+e))-roof(k/(r(1+e)))+2
           the analysis method is based on network information flow graph and entropy.
           the paper then popose explict code constructs, it is actually the "Simple Regenerating Code", it is MDS and has great local repair ability
           locality can be set to sub-linear of k, r=log(k), r=sqrt(k), to vanish the storage space penalty as k grows large
        2. so, to summarize
            1. LRC code achieves locality lower bound with best recoverability without sacrificing space overhead
            2. Simple Regenerating Code achieves locality lower bound with best recoverability when allow sacrificing space overhead
            3. r can be configured to other sub-linear functions of k, e.g. r=log(k), r=sqrt(k),
               to construct non-trival locality codes for large k with small storage overhead penalty

    29. A Practical Analysis of Low-Density Parity-Check Erasure Codes for Wide-Area Storage Applications    [2004, 110 refs]
        http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.133.5556&rep=rep1&type=pdf
        1. good papers that tell many LDPC characteristics. it walkthrough all LDPC code constructs and generation method and measure their characteristics.
        2. highlights
            1. performance panelty is determined by overhead factor f. only when code length almost > 50, LDPC starts to vastly outperform RS code
               the f decreases as code length grows, dropping to nearly 1.00 as n grows to 100,000+
            2. the storage space overhead can be 1/3, 1/2, 2/3. it's not need to be ~2x.
            3. the bipartite graph edges are generated by probability distribution, this is basically how different LDPC varies
               regular graphs, i.e. nodes have constant in/out degree, cannot achieve "channel capacity" asymptotically
            4. the performance in theory is asymptotic value, in real case, you need to run generation methods multiple times to get one good construction
               some generation method may require long time to find a good construction

5. readings: recent papers and technology shares
    1. KV-Direct: High-performance in-memory key-value store with programmable NIC
       https://blog.acolyer.org/2017/11/23/kv-direct-high-performance-in-memory-key-value-store-with-programmable-nic/
       https://lrita.github.io/images/blog/kv-direct.pdf
        1. use the FPGA in RDMA NIC to carry out KV-Store CRUD operations
           KV-Direct is much faster and 3x power-efficient then other solutions (including RAMCloud, FaRM) which are based on commodity servers
            1. Accelators (FPGA, GPU, ASIC, Smart NIC, RDMA NIC, etc) are more and more widely used. Besides deep learning, machine learning, it keep penetrating into the storage pool and in-memory processing
           the key is use programmable NIC to offload. Besides RDMA, we can build primitive kv operations into FPGA. this part can be used in more systems
            1. Previously the FPGA was mostly used for calculation, like networking, compression, encryption, or Bing web page ranking.
               But now it can be used for storage, doing kv operations offloading from CPU
            2. But, KV-Direct looks like didn't include transaction, on-disk logging, distributed management. So comparing it with RAMCloud and FaRM is not fair.
               And, it's talking about saturating DMA bandwidth and network bandwidth get max perf. Real workload cannot be that easy.
               And, to achieve the best performance, the paper is using ~10B tiny KV
            3. part of the speed comes from, FPGA NIC stores things in its DRAM, so PCIe is not involved
        2. highlights
            1. versatile API
                1. High batch throughput for small key-value pairs (e.g., model parameters, graph node neighbours).
                2. Predictable low-latency (e.g., for data-parallel computation,where tail latency matters)
                3. High efficiency under write-intensive workloads (e.g., graph computations, and parameter servers)
                4. Fast atomic operations (e.g., for centralized schedulers, sequencers , counters and so on).
                5. Vector-type operations (for machine learning and graph computing workloads that often require operating on every element in a vector).
            2. key fronts
                1. Minimising DMA (direct memory access) requests per KV operation. The two major components that drive random memory access are hash tables and memory allocation.
                2. Hiding PCIe latency while maintaining consistency, which entails pipelining requests. Care must be taken to respect causal dependencies here though.
                3. Balancing load between NIC DRAM and host memory. The NIC itself has a small amount of DRAM available, but it turns out not to be much faster than going over PCIe. So the trick turns out to be to use both in order to utilise the joint bandwidth.
            3. How high frequency CPU -> multi-core CPU -> domain-specific architecture evolves
                   Ten years ago, processor frequency scaling slowed down and people turned to multi-core and concurrency [69].
                   Nowadays, power ceiling implies that multi-core scaling has also met difficulties [22].
                   People are now turning to domain-specific architectures (DSAs) for better performance
            4. The performance gain is astonishing
                   A single NIC KV-Direct is able to achieve up to 180 M KV operations per second (Ops), equivalent to the throughput of 36 CPU cores [47].
                   Compared with state-of-art CPU KVS implementations, KV-Direct reduces tail latency to as low as 10 µs
                   while achieving a 3x improvement on power efficiency.
            5. Micsosoft is actually investing a lot of the FPGA/Accelerator cloud architecture
                1. see related materials
            6. PCIe is a packet switched network with ~500 ns round-trip latency and 7.87 GB/s theoretical bandwidth per Gen3 x8 endpoint
               the cached PCIe DMA read latency is 800 ns due to additional processing delay in FPGA.
            7. issues & questions
                1. reservation station uses hash to decide which slot to hold an key operation, there can be collisions
                   but reservation station also cache latest values, what happens if key collision, can latest value be mistakenly overwritten?
                   (or we still compare keys)
                2. does the power efficiency (table 3) includes the power consumed by FPGA? Especially when a server is attached with many programmable NICs
                   for CPU it should be low because KV-Direct is bypassing CPU.
                    1. yes, FPGA included
            8. "related works" part is good to understand KV-store approaches
        n. related materials
            1. smart nic, reconfigurable nic, programmable nic
               http://www.mellanox.com/related-docs/prod_adapter_cards/PB_BlueField_Smart_NIC.pdf
               https://www.netronome.com/blog/what-makes-a-nic-a-smartnic-and-why-is-it-needed/
            2. A Cloud-Scale Acceleration Architecture    [2016, 50 refs]
               ftp://ftp.cs.utexas.edu/pub/dburger/papers/MICRO16.pdf
                1.  direct FPGA-to-FPGA messages
                    previous: placing FPGAs as a network-side "bump-in-the-wire" (network -> FPGA -> TOR)
                    add: treat remote FPGAs as available resources for global acceleration pools, using protocol LTL (Lightweight Transport Layer)
                n. related materials
                    1. "Our recent publication described a medium-scale FPGA deployment in a production datacenter to accelerate Bing web search ranking using multiple directly-connected accelerators [4]"
                       A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services    [2014, 451 refs]
                       https://www.microsoft.com/en-us/research/publication/a-reconfigurable-fabric-for-accelerating-large-scale-datacenter-services/
            3. Down to the TLP: How PCI express devices talk
               http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-1
               http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-2
               http://xillybus.com/tutorials/pci-express-dma-requests-completions

4. readings: paper reading
    1. The Invertible Bloom Filter (IBF)
       http://www.i-programmer.info/programming/theory/4641-the-invertible-bloom-filter.html
       http://www.i-programmer.info/programming/theory/4641-the-invertible-bloom-filter.html?start=1
        1. From team share
        2. highlights
            1. Issue: why not just use a plain hash table?
                IBF is like a hash table storing a key multiple times with different hash functions.
                Each slot now stores key, value, count; space is big. However, the original BF needs 1 bit for each slot.
                What about the space bloat. Why not just use a plain hash table?
            2. We can retrieve value. We can list values (iteratively remove values with count == 1). We can delete values.
            3 But what if I delete an element that is not previously stored in IBF?
                Issue 1: An element is in IBF, but all count >= 2, cannot determine whether it's there.
                Issue 2: If count == 2, I force delete a wrong value, then this slot has count == 1 and indicate a wrong remaining value was once added into IBF.
        n. related materials
            1. hacker news: Invertible Bloom Lookup Tables (2011)
               https://news.ycombinator.com/item?id=8244086
                1. "The usage scenario of IBLTs is quite different from the usual scenario of storing key-value mappings: it is useful when you have an algorithm that adds and delete keys, and at any time during the execution of the algorithm the number of distinct keys can be arbitrarily large, but you know that at the end of the algorithm the number of distinct keys is "small"."
                   "they use a standard trick in Bloom-like data structures (and perfect hashes, etc.): the property that there is always a cell with exactly one element; this property is preserved when you remove that one element, so there will be another cell with exactly one element, and so on, until you can retrieve all of them"
            2. paper: Invertible Bloom Lookup Tables    [2011, 80 refs]
               https://arxiv.org/pdf/1101.2245v2.pdf
    2. When RSL Meets Log Corruption

3. readings: cloud FPGA related readings
    1. Down to the TLP (Transaction layer packet): How PCI express devices talk
       http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-1
       http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-2
        1. good to read. PCI works like a network switching with physical layer, data link layer, and transaction layer; rather than "bus"
    2. Considerations for host-to-FPGA PCIe traffic
       http://xillybus.com/tutorials/pci-express-dma-requests-completions

    3. A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services    [469 refs, 2014]
       https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Catapult_ISCA_2014.pdf
        1. good to read. but now new better design is the follow-up paper "A Cloud-Scale Acceleration Architecture"
           Bing's FPGA cloud design, PCIe attach, homogenous single FPGA per server, SAS cable interconnect with routing.
           run Bing's ranking engine. 95% ranking throughput improvements
        2. highlights
            1. Catapult: middle-scale (1632 servers) datacenter FPGA architecture design
                1. hardware design
                    1. single highend FPGA per server, attach to PCIe, equaipped with DRAM on FPGA chip
                        1. though there are central FPGA rack/host alternatives, server homogeneity is a concern
                        2. select PCIe to minimize distruption to next generation server design.
                            1. not GPU due to concern for power requirement
                            2. not attach to memory bus or CPU QPI due to occupies CPU socket
                            3. not ASIC, due to we need reconfigurable (fast app develop iteration)
                        3. DIMMs with ECC to add resilience
                    2. FPGA interconnection: 10Gb SAS cable, 2D-mesh connection (each 1 to 4)
                        1. FPGA implements routing internally
                        2. FPGA link supports 20Gb/s peak bidirectional bandwidth, at sub-microsecond latency
                        3. Support ECC for network resilience
                        4. drawbacks: one FPGA issue may crash/stall 4 neighbor nodes
                                      scale is limited, due to SAS compared to ethernet network
                    3. TCO: FPGA architecture increase TCO < 30%, power budget < 10%
                2. software design
                    1. FPGA to host CPU interface
                        1. low latency achieved by avoiding system calls
                        2. thread safety achieved by statically divide buffer and assign exclusively to each thread
                        3. fairness achieved by taking snapshot of full bits periodically and DMAing them at priority
                        4. user-level app may initiate FPGA reconfiguration and partial-reconfiguration by calling to low-level lib
                    2. Shell/Role architecture
                        1. Shell: reusable common portion of program logic, pre-built into FPGA
                            1. Including: DMA engine, PCIe core, DDR core (with ECC), inter-FPGA router, SL3 serial link protocol (with ECC), etc
                            2. routing by static software-configured routing table
                                1. transport protocol has no retransmission or source buffering.
                                   simple as to reduce consumed FPGA capacity, and performance overhead
                                   double-bit error dectection, single-bit error correction, ECC, CRC are used to improve packet reliability (on SAS cable)
                                   packet loss is few, rely on high-level app to do retransmit
                            3. SEU scrubber runs continously to scrub FPGA configuration errors
                            4. in all, Shell consumes 23% of each FPGA capacity
                        2. Role: the application logic, which can be partial-reconfigured
                    3. Infrastructure
                        1. Mapping Manager manages FPGA configurations and correction
                           Health Monitor monitors failure and corrects them
                        2. Correct operation
                            1. to avoid FPGA crash/crashed-by neightbors through SAS link, need "TX/RX Halt" to mask in/out traffic when reconfiguring
                            2. to recover from failure: soft reboot, hard reboot, mark out-of-service
                        3. debugging support
                            1. lightweight Flight Data Recorder. I.e. keep important events in on-chip memory to be later dumped out for investigation
                3. application cases
                    1. Bing's ranking engine
                        0. the section 4 has good description for how Bing search & ranking works.
                        1. Most features are implemented on FPGA.
                        2. One ranking service is partitioned in to a ring of 8 FPGAs, whose pipeline managed by Queue Manager
                           Different language (Spanish, English, Chinese, etc) requires different Models, each model consists a differet set of ring
                           Model reload is expensive and needs FPGA reconfiguration
            2. related works
                1. good part to read. and follow-up paper "A Cloud-Scale Acceleration Architecture" has better taxonomy
        n. related materials
            1. An FPGA-based In-line Accelerator for Memcached    [2014, 49 refs]
               https://www.hotchips.org/wp-content/uploads/hc_archives/hc25/HC25.50-FPGA-epub/HC25.27.530-Memcached-Lavasani-UTexas.pdf
                1. build Memcached logic into FPGA chip
            2. What is an LUT in FPGA?
               https://electronics.stackexchange.com/questions/169532/what-is-an-lut-in-fpga
            3. FPGA Architecture - Altera
               https://www.altera.com/content/dam/altera-www/global/en_US/pdfs/literature/wp/wp-01003.pdf

    4. A Cloud-Scale Acceleration Architecture
       ftp://ftp.cs.utexas.edu/pub/dburger/papers/MICRO16.pdf
        1. good to read.
           Catapult v2 use ethernet instead of SAS for FPGA interconnection as compared to v1. FPGA is connected "bump-in-the-wire" to NIC.
           It achieves 2x throughput while meeting latency target, which means only half servers are needed.
           It has been deploying in production of 5,760 servers, accelerating Bing search ranking and Azure software-defined networks and network crypto
        2. highlights
            1. compared the previous "Catapult v1: A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services",
               use ethernet networking for FPGA interconnect, instead of SAS cable, to achive much larger scale
                0. previous SAS interconnection suffers from: scale limitation, one FPGA crashes neighbors
                1. FPGA is connected "bump-in-the-wire" to NIC. it can do network acceleration
                    1. CPU frequency scaling and Moore's Law is ending.
                       40Gb/s network requries ~5 cores of 2.4GHz CPU to process encryption/decryption (1.2 cycles per byte)
                       scale-out can hardly help in this case. only FPGA can help
                    2. network protocol and routing - LTL: lightweight transport layer
                        0. previous SAS has sub-microsecond latency, and ethernet has ~10 us latency. slower but ok
                        1. remote FPGA appears even closer to the local FPGA, than host access to local SSD, or host network stack
                        2. partial-reconfiguration allows NIC traffic through FPGA not interrupted
                        3. LTL has buffer, flow control, retransmission, packet ordering.
                        4. connections are statically allocated and persistent in table
                        5. datacenter networks have traffic class that differentiate FPGA routing traffic
                        6. Elastic Router handles ports: PCIe DMA, Role, DRAM, Remote (to LTL)
                2. local acceleration
                    1. app access local FPGA, and FPGA also have function built in Shell to access remote FPGAs, the global pool
                    2. the NIC pass through traffic in FPGA and search ranking acceleration has no performance intervention
                    3. throughput increases by 2.25x with no latency penalty, which means only half servers are needed
                3. remote acceleration
                    1. one server can consume more than one FPGA in remote pool
                    2. the latency overhead of remote compared to local FPGA is minimal
                    3. the hardware-as-a-service model
            2. deployment and evaluation
                1. mirror live traffic from Bing to the test bed for one month
            3. related works
                1. taxonomy of how FPGA/GPU/ASIC acceleration interfaces with CPU, and intercommunication
                   this part is very good to read
                    1. alternatives
                        1. CPU-Accelerator memory integration
                            1. (C) - Coherent accelerators, where data movement is handled by a memory coherence protocol
                            2. (I) - I/O level, where data movement is done via DMA transfers, and
                            3. (N) - Network level, where data movement is done via Ethernet (or other) packet
                        2. Accelerator connectivity scale
                            1. (S) Single server / single appliance
                            2. (R) Rack level
                            3. (D) Datacenter scale
                        3. Accelerator type
                            1. (F) FPGAs
                            2. (G) GPUs
                            3. (A) ASICs
                    2. categories
                        1. NSF: Network/Single/FPGA
                        2. IRF: IO/Rack/FPGA: Catapult v1, etc
                        3. ISF: IO/Single/FPGA: this paper is both ISF and NDF
                        4. ISFG: IO/Zero/FPGA+GPU
                        5. CSF: Coherent/Single/FPGA
                        6. ISG: IO/Single/GPU
                        7. ISA: IO/Single/ASIC
                        8. NDF: Network/Datacenter/FPGA: only this paper, Catapult v2.
                2. promising programmable accelerator architectures, but not yet reached level of business production: MPPAs, CGRAs
            4. questions
                1. the high-level distributed task scheduling framework, like what Hadoop Mapreduce does, is still absent in this paper
                    1. several ideas I can think about
                        0. one server can consume more than one FPGA in remote pool. how to manage that?
                        1. task splitting, and scheduling to different nodes, and how many FPGA, who's FPGA to use
                        2. lagger node, failure node, rescheduling, or issue two tasks to cut tail latency
                        3. proper scheduling of FPGA reconfiguration
                        4. heterogeneous FPGA nodes, e.g. CPU/mem/PCIe/NIC attached FPGAs, FPGA-dedicated rack, one server has few/many FPGA, high/low-end FPGA, etc
                           heterogeneous app workload type
                           and like Mesos to mix workload from different frameworks
                        5. like Spark, RDD snapshot of computed workload
                        6. auto-detect what kind of programs should be mapped to FPGA, and what not.
                           e.g. expose API libs to app, and underlying record load and intelligent migrate
                           like Tensorflow decides which to run on CPU or GPU
                        7. the storage replication handled by FPGA and integrated with NIC.
                           another question, how should the storage system uses FPGA cloud?
                        8. cloud-level FPGA virtualization, sharing & isolation, multitenant
                        9. power-efficient scheduling
                        10. budget sensitive dynamic scheduling across CPU vs FPGA
                        ----
                        11. in datacenter, each FPGA on host, may have been programmed with multiple service functions, to occupy the entire FPGA capacity.
                            e.g. the storage system. there can have multiple serivce function in total needed on the local FPGA chip.
                            But, in a given one time, some of the service functions may not be needed right now. though in some other times, all service functions can be needed all.
                            so, we can do a dynamic service function migration across chips. When this SF not needed for now, we replace it with a needed one.
                                1. migration: what storage function applies to it? E.g. EC process, scrubbing,
                            more needed SF on chip, more thoughput. the assumption is
                                when we have two instance of the same SF on FPGA, we parallelly use both of them, thus double the throughput.
                            a storage system can be viewed as a chain of necessary/optional service functions, as ported on FPGA
                        12. in the same way, serverless services can also be seen as a chain of service functions, which can be ported to FPGA and scheduled/allocated
                        13. a service function, if too big to fit into an FPGA region, we can futher cut the service function into smaller ones, and do the placement
                              ---- as told in "Virtualized Execution Runtime for FPGA Accelerators in the Cloud" referencing to [13]
                            this separation has performance panelties, so we give execuse for app dev to specify where to cut, the policy, and we do the scheduling/placement
                        14. also, virtual FPGA cores is able to be portable to different FPGA device. pre-programmed and share to use. and built into image.
                            then, again, we have the image sharing system and distribution system in datacenter. plus p2p and security verification.
                                1. taking about FPGA image distribution, "Amazon FPGA Image (AFI)" see https://aws.amazon.com/ec2/instance-types/f1/
                            fpga shell/role architrcture image distribution, and invent some special property for it
                                1. also, the tailing of shell/role as necessary or not, is even more useful to save FPGA capacity, as to put in more storage service functions
                        15. how to tackle with inter-task dependencies, as like spark workflow
        n. related materials
            1. How does FPGA works?    [2007, 438 refs]
                1. FPGA Architecture: Survey and Challenges
                   http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.153.3122&rep=rep1&type=pdf
                    1. Altera - FPGA logic block
                       https://www.altera.com/en_US/pdfs/literature/wp/wp-01003.pdf
                2. How does an FPGA work?
                   https://embeddedmicro.com/tutorials/mojo-fpga-beginners-guide/how-does-an-fpga-work
                    1. "The Routing Matrix .. These connections are again defined in RAM which is why the FPGA must be reconfigured every time the power is cycled"
                    2. "This is why you will never be able to clock an FPGA at speeds comparable to a dedicated chip.
                        An ASIC design can reach speeds faster than 4GHz, while an FPGA is very fast if it's running at 450MHz"
                        "This is also why FPGAs consume considerably more power than their ASIC counterparts."
                3. FPGA How do they work?
                   http://www.eit.lth.se/fileadmin/eit/courses/eti135/slides/FPGA_Anders_Stedan.pdf
                4. Computer Hardware: How do field-programmable gate arrays (FPGAs) work?
                   https://www.quora.com/Computer-Hardware-How-do-field-programmable-gate-arrays-FPGAs-work
                5. FPGAs - How do they work?
                   http://www.fpga4fun.com/FPGAinfo2.html
                    1. hardware graphs
                6. How FPGAs work, and why you'll buy one
                   https://www.embeddedrelated.com/showarticle/195.php
                    1. "true" FPGA vs real modern FPGA
                    2. visualized FPGA chip view
                7. What are FPGAs and how do they work
                   https://indico.cern.ch/event/283113/contributions/1632265/attachments/522019/720041/Zibell_How_FPGAs_work.pdf
                8. Field-programmable gate array
                   https://en.wikipedia.org/wiki/Field-programmable_gate_array
                    1. Introduction: the FPGA-ASIC Gap
                        1. chip area: ~18x larger
                           dynamic power: ~14x more
                           clock speed: ~3-5x slower
                    2. "Full initial configuration ~ 1-2 seconds in practice"
                    3. "Partial reconfiguration is also referred as context switching"

            2. How long does FPGA reconfigures, and what about partitial reconfiguration?
                1. How to take advantage of partial reconfiguration in FPGA designs
                   https://www.eetimes.com/document.asp?doc_id=1274489
                    1. there are bunch of requirements and guidelines for use of partial reconfiguration
                2. Partial FPGA reconfiguration and performance
                   https://stackoverflow.com/questions/17226631/partial-fpga-reconfiguration-and-performance
                    1. "Big FPGAs can be many 10s to 100s of milliseconds to completely reconfigure."
                       "A small configuration can be achieved within the PCI express startup time (100ms IIRC)"
                3. Reconfiguration time?
                   https://forums.xilinx.com/t5/7-Series-FPGAs/Reconfiguration-time/td-p/484046
                    1. "... requires ~28 ms to receive its 3.6 Mb of configuration data"
                    2. PartialReconfiguration User Guide, "Configuration Time" section
                       https://www.xilinx.com/support/documentation/sw_manuals/xilinx12_3/ug702.pdf
                        1. configuration port bandwidth: 66Mb/s ~ 3.2Gb/s
                4. Partial Reconfiguration on FPGAs
                   http://www.uio.no/studier/emner/matnat/ifi/INF5430/v11/undervisningsmateriale/lecture_slides_dirk/lecture_RC.pdf

            3. How to virtualize FPGA on cloud, i.e. multitenant, pooling, sharing, isolation, etc?
                1. Catapult v2 usage on Azure SDN - Azure Smart NIC
                   https://www.slideshare.net/insideHPC/inside-microsofts-fpgabased-configurable-cloud
                    1. indeed SDN witnesses performance issues, which need to be handled by introducing acceleration hardware such as FPGA on NIC

                2. Virtualized FPGA Accelerators for Efficient Cloud Computing    [2015, 24 refs]
                   https://warwick.ac.uk/fac/sci/eng/staff/saf/publications/cloudcom2015-fahmy.pdf
                    1. virtual FPGAs (vFPGAs): physical FPGA is divided into multiple partially reconfigurable regions (PRRs);
                       A vFPGA can be partial-configured to implement multiple virtual FPGA accelerators (vFAs)
                    2. An interface switch ensures each vFPGA is served in a fair manner with round robin arbitration for access to the PCIe and DRAM data streams
                    3. FPGA Driver, client API SDK, Hypervisor, FPGA allocation, Resource Manager
                    4. app case study: mapreduce accelerator for word counting

                3. How Microsoft uses FPGA in Bing, ASIC Holographic Processing Unit (in HoloLens), Azure network,
                   https://arstechnica.com/information-technology/2016/09/programmable-chips-turning-azure-into-a-supercomputing-powerhouse/
                    0. good to read, tells how MS using the FPGA from start to Bing and Azure clouds; help understand the above two papers
                    1. instead of highend NIC's SR-IOV (limitation, e.g. only assign to 4-VMs at max), MS uses FPGA+shared NIC across VMs.
                       Also, network SDN functionalities equivalents of tunneling/VLAN/VxLAN/GRE and routing are implemented in the FPGA
                    n. related materials
                        1. Virtualizing PCI and PCIe
                           https://arstechnica.com/information-technology/2010/02/io-virtualization/
                            0. enumerating, paravirtualization, PCI pass-through
                            1. for PCI pass through, Intel's VT-d and AMD's AMD IOMMU/AMD-Vi solves the VM virtual to host physical memory mapping issue
                            2. next, PCIe needs to extended, so that one physical device's multiple VFs can be mapped to multiple VMs.
                               i.e. PCIe Single Root I/O Virtualization specification (SR-IOV)

                4. Virtualized Execution Runtime for FPGA Accelerators in the Cloud    [2017, 1 refs]
                   http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7840018
                    1. good paper to read, tells the end-to-end framework from app dev toolchain, to scheduling virtualization on FPGA cloud, to protection and security
                       further work on "Virtualized FPGA Accelerators for Efficient Cloud Computing", sharing one same author
                    2. highlights
                        1. a complete end-to-end framework to allow apps run on cloud with FPGA, including dev tool chain.
                            enables developers to view FPGAs asa computational resource similar to CPUs,
                                providing facilities such as memory management,
                                virtualisation and a hardware abstraction layer
                            We also provide a design flow that enables developers to write FPGA-accelerated applications at different levels of abstraction,
                                up to high-level DSLs where CPU-FPGA partitioning and interaction are done seamlessly
                        2. designs
                            1. FPGA includes,
                                runtime: Local processor, runtime system, user threads.
                                PR regions: for app to write accelerators.
                                Memory: on FPGA chip, app accelerator accesses it by Local processor
                            2. toolchain generates an FPGA application package,
                                which includes the specifications of the hardware accelerators
                                and code to be run on the local processor
                            3. features required for the cloud
                                Memory management
                                    — Virtual memory
                                    — Dynamic memory allocation and deallocation
                                • Shared execution
                                    — Multi-process
                                    — Multi-user
                                    — Workload-dependent resource allocation
                                • Protection
                                    — Memory and hardware protection
                                    — Protection rings
                                • Application execution
                                    — Loader
                                    — Scheduler
                                • Code portability
                                    — Hardware abstraction layer
                            4. "a local processor, which can interact with the accelerators and access FPGA resources with lower latency than the host CPU"
                                1. the local processor is not for processing the application task, but to help accelerator access FPGA peripherals
                            5. "Even when the PR regions all have the same size, it is still possible to scale the area and performance of an application
                                by partitioning accelerators into multiple smaller replicas that operate in parallel [13]"
                        3. related materials
                            1. A platform-independent runtime methodology for mapping multiple applications onto FPGAs through resource virtualization    [2013, 4 refs]
                               https://pdfs.semanticscholar.org/3a7a/53a5530aa5b07e9e051dfd0433f9928eecca.pdf
                                1. virtual FPGA cores
                                    1. Portability across different FPGA devices
                                    2. CoreManager decides which FPGA's which region should be placed with the vFPGA core requested by application
                                    3. "CoreFusion" allows to merge adjacent cores
                                    4. FPGA capacity fragmentation issue
                            2. Enabling FPGAs in the Cloud    [2014, 42 refs]
                               http://nics.ee.tsinghua.edu.cn/people/wangyu/Enabling%20FPGAs%20in%20the%20Cloud.pdf
                                0. as referenced in "Virtualized Execution Runtime for FPGA Accelerators in the Cloud": "does not perform any dynamic management of accelerator slots"
                                   good to read. the paper proposed abstract pooling concepts PRP vs AP, acceleration slots. and many details in the FPGA-Hypervisor co-design.
                                   It uses KVM and Openstack
                                1. prototype implemented based on OpenStack, Linux-KVM and Xilinx FPGAs
                                2. highlights
                                    1. core features mentioned in abstract
                                        1. isolation between multiple processes in multiple VMs
                                            1. FPGA partial partition, regions / acceleration slots, GPA-HPA (Guest/host physical address) translation (VM-nocopy)
                                                1. the  slot layout cannot be changed unless whole FPGA is reconfigured
                                            2. DMA parameter checking, (alternative is IOMMU but not used), FPGA internal bandwidth control.
                                               in FPGA SL (service logic) governs them
                                        2. precise quantitative acceleration resource allocation
                                            1. Openstack is the cloud provider
                                        3. priority-based workload scheduling
                                            1. SL facilitates accelerator bandwidth and priority management.
                                            2. Openstack Nova scheduler for acceleration & slots scheduling
                                               accelerators are scheduled considering their various requirements for computation and I/O resources
                                    2. resource abstraction
                                        1. instead of abstracting PRP (programmable resource pool), we abstract AP (accelerator pool)
                                           "An accelerator design following standards can be mapped into standard slots"

                5. High Performance in the Cloud with FPGA Groups    [2016, 3 refs]
                   http://www.globule.org/publi/HPCFV_ucc2016.pdf
                    1. good, interesting to read. Note that the paper is on HPC
                       proposed FPGA group to aggregrate multiple physical FPGAs to one big virtual
                       and API remoting as another way to vritaulize FPGA access
                    2. highlights
                        1. abstract
                            1. "FPGA groups, which are seen by their clients as a single virtual FPGA"
                                1. FPGAs in group are configured with exact same circuit design
                                   load-balancing incoming execution requests to them
                            2. "an autoscaling algorithm to maximize FPGA groups' resource utilization"
                        2. challenges
                            1. "maximizing utilization", "capacities ranging"
                            2. the lack of satisfactory techniques for virtualizing FPGAs
                                1. current solutions
                                    1. based either on statically partitioning the gate array between ultiple applications (i.e., sharing in space)
                                        1. sharing in space implies that each application must use a smaller number of digital gates, thereby negatively impacting performance
                                        2. However, space sharing reduces the area that is made available to host an FPGA design, which can have a considerable performance impact because it limits the number of functional units that can work in parallel
                                        3. Sharing in space also requires some switching logic in the FPGA to route incoming requests to the appropriate design, which can add additional overhead
                                    2. on naive context switching (i.e., sharing in time)
                                        1. incurs prohibitive context switching costs, as reconfiguring an  PGA from one circuit design to another takes in the order of a couple of seconds
                                        2. actually this approach is usually overlooked
                                        3. AWS EC2 GPGPU is shared by PCI passthrough
                                2. another view
                                    1. existing: I/O passthrough, Paravirtualization
                                    2. this paper proposed: API remoting
                                        1. like OpenCL or CUDA, calls to the API are intercepted in the VM and passed through to the host OS on which the accelerator is accessible.
                                            1. It's more like mutiple clients sharing access to a web server
                                            2. A number of technologies employ API remoting over a network including rCUDA [10], DS-CUDA [20], dOpenCL [17] and VirtualCL [5]. Additional studies with Infiniband networks show that this is a practical solution for rCUDA [24] and DS-CUDA [16]
                        m. questions
                            1. if accelerator is partitioned across multiple physical FPGAs, how to deal with the communication management and overhead?
                                1. the paper assumes infiniband network
                                   the paper is using "MPC-X" appliance
                                   Note that the paper is a HPC paper

                    6. Overlay Architectures For FPGA Resource Virtualization    [2016, 1 refs]
                       https://hal.archives-ouvertes.fr/hal-01405912/document
                        1. "Adding special features to the overlay implementations such as dynamic clock control
                            and a state snapshot mechanism allows performing hardware task preemptive scheduling and live migration"
                        2. related materials
                            1. ZUMA: An Open FPGA Overlay Architecture    [2012, 66 refs]
                               http://www1.cse.wustl.edu/~roger/565M.f12/4699a093.pdf
                                1. "ZUMA reduces this penalty to as low as 40x"
                                2. highlights
                                    1. "Previous attempts to map an FPGA architecture into a commercial FPGA have had an area penalty of 100x at best [4]"
                                       "ZUMA reduces this penalty to as low as 40x"

                    7. FPGA Virtualization for Enabling General Purpose Reconfigurable Computing
                       http://cc.doc.ic.ac.uk/fresh16/Dirk.pdf
                        1. good material. tells industry status
                        2. highlights
                            1. FPGAs in Datacenters: Where are we?
                                1. Intel took over the second biggest FPGA vendor (Altera) one year ago for US$ 16.7B
                                2. Microsoft: 1632 servers with FPGAs for Bing Search -> 2x throughput, 29% less latency, ~2x energy efficiency
                                3. Baidu: search algorithm acceleration using FPGAs -> 3.5x more throughput than a GPU at 10% power
                            2. FPGAs Virtualization: Where are we?
                                1. Two main directions
                                    1. Overlays: a programmable architecture on top of an FPGA
                                        1. software like instead of RTL coding, portability, and reuse funcional blocks
                                        2. VectorBlox, Dragon processor (bioinformatics)
                                    2. Dynamic FPGA modules: temporal partitioning
                                        1. Maximize resource utilization, Runtime adaptability, Fault tolerance, Saving energy
                                        2. Move modules around for masking faults
                            3. FPGA Database Accelerator
                        3. related materials
                            1. An Efficient FPGA Overlay for Portable Custom Instruction Set Extensions    [2013, 22 refs]
                               https://pdfs.semanticscholar.org/2d04/22cc490db8b2069134f27bde85c9458af8e8.pdf
                                1. FPGA Overlay to virtualize FPGA is more like an effort from FPGA community,
                                   while the partition/region/accelerator-slot is more like from the cloud community
                                2. highlights
                                    1. challenges
                                        1. for FPGAs, there is no direct path to use identical configuration bitstreams from different vendors. not like binary-compatible CPU
                                    2. beyond partition/region/accelerator-slot, API remoting (interception);
                                       here's a new way to virtualize FPGA: FPGA overlay
                                        1. the concept is like JVM, shipping bytecode
                                        2. custom instruction set extensions
                                        3. physical:virtual LUT ratio
                                        2. looks like the Overlay is done by manipulating FPGA logic resources, circuit-level stuff ..
                                3. questions
                                    1. now the market of FPGA is dominated by Altera and Xillix, so we don't actually have too many incompatible binarystreams, right?
                                       If I only buy FPGA from one Vendor, like we only buy CPU from Intel, then we don't need the overlay bytecode and "JVM".

                    8. FPGAs in the Cloud: Booting Virtualized Hardware Accelerators with OpenStack    [2014, 74 refs]
                       http://ieeexplore.ieee.org/document/6861604/
                        1. no original paper. only reading from abstract.
                           treat booting accelerators as booting VMs; good thought.
                           virtualization is done by "Partially reconfigurable regions"
                        2. highlkghts
                            1. Partially reconfigurable regions across multiple FPGAs are offered as generic cloud resources through OpenStack (opensource cloud software),
                               thereby allowing users to "boot" custom designed or predefined network-connected hardware accelerators with the same commands they would use to boot a regular Virtual Machine
                            2. Our system can set up and tear down virtual accelerators in approximately 2.6 seconds on average
                            3. The static virtualization hardware on the physical FPGAs causes only a three cycle latency increase and a one cycle pipeline stall per packet
                               in accelerators when compared to a non-virtualized system
                            4. Our study shows that FPGA cloud compute resources can easily outperform virtual machines

                6. Virtualized FPGA Accelerators in Cloud Computing Systems    [2015, 24 refs]
                   http://www.eecg.utoronto.ca/~jayar/FPGAseminar/2013/high-scale-routers-for.html
                    1. FPGAs as OpenStack Cloud Resources. We want a way to make FPGAs analogous to VMs. using "Partial Reconfigurable Regions".
                       The idea soundslooks like "FPGAs in the Cloud: Booting Virtualized Hardware Accelerators with OpenStack"
                       The whole work is based on Openstack
                    2. the material is informative.

                7. OpenStack Acceleration Service: Introduction of Cyborg Project
                   https://www.openstack.org/videos/boston-2017/openstack-acceleration-service-introduction-of-cyborg-project
                   https://wiki.openstack.org/wiki/Cyborg
                   https://github.com/openstack/cyborg
                    1. Formerly known as project Nomad. Openstack Scientific Work Group. HPC.
                       GPU hosts vs VM resource scheduling. Cyborg agents communicating to Nova. OpenCL.

            3.4. how public cloud provide FPGA?
                1. Why Public Cloud is Embracing FPGAs and You Should Too
                   https://f5.com/about-us/blog/articles/why-public-cloud-is-embracing-fpgas-and-you-should-too-24883
                2. AWS Details FPGA Rationale and Market Trajectory
                   https://www.nextplatform.com/2017/01/22/aws-details-fpga-rationale-market-trajectory/
                3. Baidu Deploys Xilinx FPGAs in New Public Cloud Acceleration Services
                   https://www.xilinx.com/news/press/2017/baidu-deploys-xilinx-fpgas-in-new-public-cloud-acceleration-services.html
                4. Baidu Public Cloud FPGA
                   https://cloud.baidu.com/product/fpga.html
                    1. "每个FPGA实例独享一个FPGA加速平台，不会在实例、用户之间共享"
                5. FPGA as Service in Public Cloud: Why and How
                   http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7929179
                6. AWS FPGA instance
                   https://aws.amazon.com/ec2/instance-types/f1/
                    1. "Once your FPGA design is complete, you can register it as an Amazon FPGA Image (AFI)"
                    2. "Each FPGA includes local 64 GiB DDR4 ECC protected memory, with a dedicated PCIe x16 connection"
                    3. "you pay for F1 compute capacity by the hour with no long-term commitments or upfront payments."
                    4. 手把手教你在FPGA实例上运行"Hello World"
                       https://aws.amazon.com/cn/blogs/china/running-hello-world-on-fpga/
                    5. Developer Preview – EC2 Instances (F1) with Programmable Hardware
                       https://aws.amazon.com/blogs/aws/developer-preview-ec2-instances-f1-with-programmable-hardware/
                        1. "The FPGAs are dedicated to the instance and are isolated for use in multi-tenant environments"
                    6. Amazon EC2 F1 Instances, Customizable FPGAs for Hardware Acceleration Are Now Generally Available
                       https://aws.amazon.com/about-aws/whats-new/2017/04/amazon-ec2-f1-instances-customizable-fpgas-for-hardware-acceleration-are-now-generally-available/
                    7. EC2 F1 Instances with FPGAs – Now Generally Available
                       https://aws.amazon.com/blogs/aws/ec2-f1-instances-with-fpgas-now-generally-available/
                7. Azure FPGA VM instance?
                    1. I didn't find any news. Why are they all about Catapult and Azure SDN?
                8. Intel FPGAs Power Acceleration-as-a-Service for Alibaba Cloud
                   https://insidehpc.com/2017/10/intel-fpgas-power-acceleration-service-alibaba-cloud/
                    1. Alibaba Cloud's F1 Instance
                        1. tool: OpenCL or RTL
                        2. will .. a rich ecosystem of IP for ..
                9. summary
                    1. so overall, I think public cloud VM instance FPGA is done by PCI pass through
                       Baidu and AWS saying the FPGA is isolated, not shared, or dedicated.
                    2. the competivity comes from
                        1. provide FPGA VM instances, with big and more FPGA cards
                        2. develop tool chain support
                        3. rich ecosystem of IPs (reusable accelerator designs on FPGA)

            3.5. how GPU is virtualized on cloud?
                1. GPU CPU is connected via PCIe. PCIe (v2) bandwith typically 5GB/s ~ 8GB/s
                   https://devtalk.nvidia.com/default/topic/506821/data-transfer-between-cpu-and-gpu/
                   https://en.wikipedia.org/wiki/PCI_Express
                   https://www.xilinx.com/support/documentation/white_papers/wp350.pdf
                    1. PCIe bandwidth generally is much smaller than Ethernet
                       1 byte is transmitted every 4 ns (2.5Gb/s bandwidth)
                2. NVIDIA, AMD, and Intel: How they do their GPU virtualization
                   http://www.brianmadden.com/opinion/NVIDIA-AMD-and-Intel-How-they-do-their-GPU-virtualization
                    0. good to read
                    1. "In general the largest portion of the GPU is dedicated to shaders"
                    2. Approaches to virtualized GPUs
                        1. API Intercept
                            1. "The oldest of these, API Intercept, works at the OpenGL and DirectX level"
                        2. Virtualized GPU
                            1. "users get direct access to a part of the GPU"
                        3. Pass-through
                            1. "If you have two cards in your server, then you get to connect two VMs to GPUs while everyone else gets nothing"
                    3. types of GPUs
                        1.  There are three different companies making virtual GPUs: Intel (GVT-g), AMD (MxGPU), and NVIDIA (vGPU)
                        2. Virtualization
                            1. Video RAM
                                1. physical slice
                            2. Shader Engine
                                1. physical slice (AMD MxGPU; hardware); time slice (Intel GVT-g, NVIDIA vGPR; software, cannot interrupt)
                            3. GPU Compute
                                1. OpenCL; Passthrough only
                            3. Hypervisor Requirements and Hypervisor Support
                                1. SR-IOV (physical, AMD MxGPU); Software Manager (Intel, NVIDIA)
                            4. AMD is currently only certified on ESX
                               Intel supports KVM and XenServer
                               NVIDIA supports both ESX and XenServer
                               Hyper-V isn't supported at all
                3. Enable GPU Virtualization in OpenStack
                   https://www.openstack.org/assets/presentation-media/Enable-GPU-virtualization-in-OpenStack.pdf
                4. Everything you need to know about GPU virtualization
                   http://searchvirtualdesktop.techtarget.com/essentialguide/Everything-you-need-to-know-about-GPU-virtualization
                    1. "GPU virtualization is a great way to improve application and VDI performance"

            4. What is the current challenge / technology edge of FPGA circle?
                1. HPC Cloud for Scientific and Business Applications: Taxonomy, Vision, and Research Challenges    [2017, 0 refs]
                   https://arxiv.org/pdf/1710.08731.pdf
                    1. good paper to read. it's for HPC. highlights
                    2. highlighs
                        1. HPC Cloud Efforts: Viability
                            1. compared to traditional HP cluster, cloud features in "elastic"
                            2. latency-limited applications, where numerous small point-to-point messages are exchanged, are most penalized in cloud
                               bandwidth-limited applications, where exchanging few large messages, or perform collective communication, are less penalized
                            3. network virtualization and hardware heterogenety are main causes of poor performance of HPC in cloud
                        2. HPC Cloud Efforts: Performnace optimization
                            1. HPC-aware scheduler
                                1. topology requirements
                                2. benchmarking information which classifies the type of network requirements of app,
                                   and how it performance is affected when resources are shared
                            2. Platform selectors
                                1. environment selection impacts job performance.
                                   users may be overloaded with many infrastructure configuration choices
                                2. selection based on pre-populated information, use historical information on resource usage
                            3. Spot instance handlers.
                                1. use novel pricing models in public clouds to reduce cost
                            4. Elasticty
                                1. combines static reservation and dynamic allocation of VMs
                                2. VMs placed on same host improve performance (reminds me of pod/cell concpets)
                            5. Predictors
                                1. prediction of expected run time and wait time helps job placement and resource match
                        3. HPC Cloud Efforts: Usability
                            1. web portals; parameter sweep; workflow management; deploy; legacy-to-saas
                        4. version and challenges
                            1. see Figure 5. very good.
                               layered architecutre, with interaction roles, and modules of gap and existing
                            2. gaps
                                1. HPC-aware Modules
                                    1. Resource manager
                                    2. Cost advisor
                                    3. Large contract handler
                                    4. DevOps
                                    5. Automation APIs
                                2. General cloud modules
                                    1. Visualization and data management
                                    2. Flexible software licensing models
                                    3. Value-add cloud services

                    2. ClickNP: Highly Flexible and High Performance Network Processing with Reconfigurable Hardware    [2016, 31 refs]
                       https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/main-4.pdf
                       https://www.youtube.com/watch?v=f02IFrmQSFc
                        1. The author Bojie Li's anwser on zhihu "https://www.zhihu.com/question/24174597/answer/138717507" is good & interesting to read.
                           FPGA Network function (NF) processor. high performance.
                           Allows C-like language programmability. Modular architecture.
                           Use the PCIe channel instead of FPGA on-board DRAM to communicate with CPU
                        2. highlights
                            1. "The main challenge to use FPGA as an accelerator is programmability"
                            2. using Catapult shell + ClickNP role
                            3. c-like language is achieved by
                                1. many existing HLS tools support C
                                2. we extend C language to support element declaration
                                3. ClickNP tool-chain
                            4. PCIe IO Channel
                                1. "We extend the OpenCL runtime and add a new I/O channel, which is connected to a PCIe switch in the shell"
                                2. as mentioned by author's answer on Zhihu "https://www.zhihu.com/question/24174597/answer/138717507"
                                    1. For CPU to communicate with FPGA, we don't need to go through the DRAM on FPGA board.
                                       PCIe DMA of FPGA communicate directly with CPU reduce latency greatly, as opposed to OpenCL original
                                3. "We extend the OpenCL runtime and add a new I/O channel, which is connected to a PCIe switch in the shell.
                                    The PCIe switch will arbitrate the access between the newly added I/  channel and other components in the shell, e.g., DDR memory controller."
                                    "We leverage the PCIe slot DMA engine in Catapult shell [40], which divides a PCIe Gen2 x8 link into 64 logical subchannels, i.e., slots"
                                    "Among 64 slots, 33 are reserved by Shell and the runtime library to control kernels and access on-board DDR,
                                     one slot is used for passing signals to ClickNP elements"
                                    "The remaining 30 slots, however, are used for data communications among FPGA and CPU elements."
                                    "To amortize DMA overhead, we aggressively use batching. The maximum message size is limited at 64KB"
                            5. the pipeline parallelism, and duplicate pipeline to leverage data parallelism
                               and parallelism inside element: and minimize memory dependency in pipeline => use delayed write

                    3. Five Challenges to FPGA-Based Prototyping
                       https://www.eetimes.com/author.asp?doc_id=1324000
                        1. Design partitioning; Long time mapping design to FPGA prototype;
                           Difficult debug; Performance may not perform as expected;
                           Reusability of components and vs SoC size growth as to fit into one FPGA board

                    4. FPGA Architecture: Survey and Challenges    [2008, 438 refs]
                       http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.153.3122&rep=rep1&type=pdf
                        1. good to read. informative and complete material covers many sides of FPGA
                        2. highlights
                            1. FPGA features
                                1. flexible
                                2. significant cost in area, delay, and power consumption comapred to ASIC
                                    1. but ASIC is costly: CAD tools, mask cost of device, engineering team cost to develop ASIC taking years
                            2. history of FPGA evolve and today's main technology approach
                            3. Routing Architecture
                                1. very good section as to understand FPGA routing switches. See paper for details
                            4. FPGA gaps and alternative technologies
                                1. Technology issues: Soft Errors, Configuration Memory, User-Visible Memory, IC Process Variation, Manufacturing Defects
                                2. Emerging Architectures: Coarse-Grained FPGAs, Asynchronous FPGAs, Nanotechnology Architectures

                    5. Beyond Physical: Solving High-end FPGA Design Challenges
                       file:///D:/Chrome_Downloads/BeyondPhysical-SolvingHigh-endFPGADesignChallenges.pdf
                        1. highlights
                            1. FPGA challenges
                                1. Physical Synthesis
                                2. Managing Design Size and Complexity
                                    1. "The other big trend in FPGA design is an increasing amount of DSP content, as well as the use of embedded cores and IP blocks"
                                    2. DSP Optimization Techniques Used in FPGAs
                                        1. Pipelining, Folding, Multi-channelization, Multi-rate Folding
                                3. Addressing Low Power Consumption Demands
                                4. Debug in RTL, Not Gates
                                5. Debugging and Visibility Enhancement

                    6. Challenges of virtualization FPGA in a cloud context    [2017, 0 refs]
                       http://ieeexplore.ieee.org/abstract/document/7995321/
                        1. no original paper yet. abstract: "sensor network application"?

                    7. Cloud perspective on reconfigurable hardware    [2013, 0 refs]
                       http://www.afahc.ro/ro/revista/Nr_2_2013/23_Octavian_Mihai_MACHIDON.pdf
                        1. er ..

            5. Hadoop like job scheduler framework targeting the FPGA cloud?
                1. An FPGA-based Distributed Computing System with Power and Thermal Management Capabilities    [2011, 15 refs]
                   https://pdfs.semanticscholar.org/a36c/6991627e65d119926867c4f31c3acfb78d89.pdf
                    1. We created a multi-core distributed computing platform using "Altera Nios II Embedded Evaluation Kit (NEEK)"

                2. Distributed FPGA Solution for High-Performance Computing in the Cloud (LDA Technologies)
                   http://www.ldatech.com/2017/wp-content/uploads/2016/11/ldawhitepaper_fpga_for_cloud.pdf
                    1. N FPGAs connected by serial links to CrossPoint Fabric. So it's selling server solutions.

                3. Task Scheduling in Large-scale Distributed Systems Utilizing Partial Reconfigurable Processing Elements    [2012, 4 refs]
                   https://ce-publications.et.tudelft.nl/publications/140_task_scheduling_in_largescale_distributed_systems_utilizing.pdf
                    1. "we propose the design of a simulation framework to investigate the performance of reconfigurable processors in distributed systems"
                       "Results suggest that the average wasted area per task is less as (with partial reconfiguration) compared to the full configuration"

                4. Effective Utilization and Reconfiguration of Distributed Hardware Resources Using Job Management Systems     [2003, 10 refs]
                   ftp://cs.umanitoba.ca/pub/IPDPS03/DATA/W08_RAW_16.PDF
                    1. too old.

                5. FPGA-Accelerated Hadoop Cluster for Deep Learning Computations    [2015, 2 refs]
                   http://ieeexplore.ieee.org/document/7395718/
                    1. no original paper. abstract: exploits deep learning data parallelism in 2 ways:
                        1) by distributing deep computation into a Hadoop cluster or cloud of computing nodes, and
                        2) by using field programmable gate arrays (FPGA) hardware acceleration to speed up computationally intensive deep learning kernels
                       ... on a 6-node FPGA accelerated Hadoop cluster

                6. 如何评价微软在数据中心使用 FPGA 代替传统 CPU 的做法？ - 李博杰的回答 - 知乎
                   https://www.zhihu.com/question/24174597/answer/138717507
                    1. very good to read. sharing many insights as the author is intern from MSR
                    2. highlights
                        1. "我们即将用上的下一代 FPGA，Stratix 10，将配备更多的乘法器和硬件浮点运算部件，从而理论上可达到与现在的顶级 GPU 计算卡旗鼓相当的计算能力"
                        2. "在数据中心，FPGA 相比 GPU 的核心优势在于延迟"
                           "像 Bing 搜索排序这样的任务 ... 如果使用 GPU 来加速，要想充分利用 GPU 的计算能力，batch size 就不能太小，延迟将高达毫秒量级"
                        3. "FPGA 为什么比 GPU 的延迟低这么多？这本质上是体系结构的区别。FPGA 同时拥有流水线并行和数据并行，而 GPU 几乎只有数据并行（流水线深度受限）。"
                           "因此对流式计算的任务，FPGA 比 GPU 天生有延迟方面的优势"
                        4. "FPGA 的灵活性可以保护投资，事实上，微软现在的 FPGA 玩法与最初的设想大不相同"
                           "使用 FPGA 可以保持数据中心的同构性"
                        5. "从延迟上讲，网卡把数据包收到 CPU，CPU 再发给网卡，即使使用 DPDK 这样高性能的数据包处理框架，延迟也有 4~5 微秒"
                        6. "虽然 GPU 也可以高性能处理数据包，但 GPU 是没有网口的，意味着需要首先把数据包由网卡收上来，再让 GPU 去做处理。
                            这样吞吐量受到 CPU 和/或网卡的限制。GPU 本身的延迟就更不必说了。"
                        7. "综上，在数据中心里 FPGA 的主要优势是稳定又极低的延迟，适用于流式的计算密集型任务和通信密集型任务"
                        8. "只要规模足够大，对 FPGA 价格过高的担心将是不必要的。"
                        9. 过去的方案：专用的 FPGA 集群，里面插满了 FPGA
                            1. 不同机器的 FPGA 之间无法通信，FPGA 所能处理问题的规模受限于单台服务器上 FPGA 的数量
                            2. 数据中心里的其他机器要把任务集中发到这个机柜，构成了 in-cast，网络延迟很难做到稳定。
                            3. FPGA 专用机柜构成了单点故障，只要它一坏，谁都别想加速了；
                            4. 装 FPGA 的服务器是定制的，冷却、运维都增加了麻烦。
                        10. "FPGA 在 Bing 的部署取得了成功，Catapult 项目继续在公司内扩张"
                        11. "随着网络和存储速度越来越快，网络上了 40 Gbps，一块 SSD 的吞吐量也能到 1 GB/s，CPU 渐渐变得力不从心了"
                        12. "为了加速网络功能和存储虚拟化，微软把 FPGA 部署在网卡和交换机之间"
                            "FPGA（SmartNIC）对每个虚拟机虚拟出一块网卡，虚拟机通过 SR-IOV 直接访问这块虚拟网卡"
                            "虚拟机收发网络数据包均不需要 CPU 参与，也不需要经过物理网卡（NIC）"
                            "这样不仅节约了可用于出售的 CPU 资源，还提高了虚拟机的网络性能（25 Gbps），把同数据中心虚拟机之间的网络延迟降低了 10 倍"
                            "FPGA 复用主机网络的初心是加速网络和存储，更深远的影响则是把 FPGA 之间的网络连接扩展到了整个数据中心的规模，做成真正 cloud-scale 的「超级计算机"
                            "第三代架构中的 LTL 还支持 PFC 流控协议和 DCQCN 拥塞控制协议"
                        13. "对很多类型的应用，随着分布式 FPGA 加速器的规模扩大，其性能提升是超线性的"
                            "例如 CNN inference，当只用一块 FPGA 的时候，由于片上内存不足以放下整个模型，需要不断访问 DRAM 中的模型权重，性能瓶颈在 DRAM；
                             如果 FPGA 的数量足够多，每块 FPGA 负责模型中的一层或者一层中的若干个特征，使得模型权重完全载入片上内存，就消除了 DRAM 的性能瓶颈，完全发挥出 FPGA 计算单元的性能。"
                            "当然，拆得过细也会导致通信开销的增加。把任务拆分到分布式 FPGA 集群的关键在于平衡计算和通信。"
                        14. "在 MICRO'16 会议上，微软提出了 Hardware as a Service (HaaS) 的概念，即把硬件作为一种可调度的云服务，使得 FPGA 服务的集中调度、管理和大规模部署成为可能"
                        15. "CPU 和 FPGA 之间本来可以通过 PCIe 高效通信，为什么要到板上的 DRAM 绕一圈？也许是工程实现的问题，
                             我们发现通过 OpenCL 写 DRAM、启动 kernel、读 DRAM 一个来回，需要 1.8 毫秒。而通过 PCIe DMA 来通信，却只要 1~2 微秒。"
                            "因此我们提出了 ClickNP 网络编程框架 [5]，使用管道（channel）而非共享内存来在执行单元（element/kernel）间、执行单元和主机软件间进行通信。"
                        16. "低延迟的流式处理，需要最多的地方就是通信。然而 CPU 由于并行性的限制和操作系统的调度，做通信效率不高，延迟也不稳定。此外，通信就必然涉及到调度和仲裁"
                            "CPU 由于单核性能的局限和核间通信的低效，调度、仲裁性能受限，硬件则很适合做这种重复工作。"
                            "因此我的博士研究把 FPGA 定义为通信的「大管家」，不管是服务器跟服务器之间的通信，虚拟机跟虚拟机之间的通信，进程跟进程之间的通信，CPU 跟存储设备之间的通信，都可以用 FPGA 来加速。"
                        17. "成也萧何，败也萧何。缺少指令同时是 FPGA 的优势和软肋。每做一点不同的事情，就要占用一定的 FPGA 逻辑资源。
                             如果要做的事情复杂、重复性不强，就会占用大量的逻辑资源，其中的大部分处于闲置状态。"
                             "数据中心里的很多任务有很强的局部性和重复性：一部分是虚拟化平台需要做的网络和存储，这些都属于通信；另一部分是客户计算任务里的，比如机器学习、加密解密。"
                    3. as for challenges of FPGA
                        1. programming on FPGA is hard. transform RTL to real circuit design is hard. software developers to work on FPGA is hard, where needs hardware programming
                        2. mostly we are comparing FPGA with GPU/CPU/ASIC. But actually FPGA is more suitable to low latency (~ 1us) stream processing
                           while GPU is more suitable for higher latency (> 1ms) batch data processing.
                           FPGA has both data parallel and command pipeline, while GPU has only data parallel.
                           and, since logic occupies circuit area on FPGA, FPGA is not suitable to program very complex commands
                    4. questions
                        1. looks like, though FPGA is vastly used in MS Bing search & rank and Azure SDN, providing public cloud FPGA VM instance is not addressed yet.
                           and even more, how to allow public cloud users to use the cloud-scale FPGA acceleration infrastructure?
                    n. related materials
                        1. Communicating sequential processes
                           https://en.wikipedia.org/wiki/Communicating_sequential_processes
                            1. "CSP was highly influential in the design of the occam programming language"
                        2. ClickNP: Highly Flexible and High Performance Network Processing with Reconfigurable Hardware    [2016, 31 refs]
                           https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/main-4.pdf
                            1. logged before

                        3. Can FPGAs Beat GPUs in Accelerating Next-Generation Deep Learning?
                           https://www.nextplatform.com/2017/03/21/can-fpgas-beat-gpus-accelerating-next-generation-deep-learning/
                            1. highlights
                                1. Changes making FPGA a viable future
                                    1. While FPGAs provide superior energy efficiency (Performance/Watt) compared to high-end GPUs,
                                       they are not known for offering top peak floating-point performance
                                    2. Intel FPGAs offer a comprehensive software ecosystem that ranges from low level Hardware Description languages
                                       to higher level software development environments with OpenCL, C, and C++
                                    3. DNN Algorithms: the trends have shifted towards more efficient DNNs
                                        1. An emerging trend is adoption of compact low precision data types, much less than 32-bits. 16-bit and 8-bit data types are becoming the new norm
                                        2. continued accuracy improvements for extremely low precision 2-bit ternary and 1-bit binary DNNs, where values are constraints to (0,+1,-1) or (+1,-1)
                                        3. Another emerging trend introduces sparsity (the presence of zeros) in DNN neurons and weights
                                           by techniques such as pruning, ReLU, and ternarization, which can lead to DNNs with ~50% to ~90% zeros
                                2. case studies and FPGA vs GPU performance number charts

                        4. CUDA vs FPGA? - asked on Stackoverflow
                           https://stackoverflow.com/questions/317731/cuda-vs-fpga
                            1. answer 1
                                1. "FPGAs are great for realtime systems, where even 1ms of delay might be too long"
                                2. "FPGAs can be very fast, espeically for well-defined digital signal processing usages (e.g. radar data)
                                    but the good ones are much more expensive and specialised than even professional GPGPUs"
                                3. "FPGAs are quite cumbersome to programme. Since there is a hardware configuration component to compiling, it could take hours"
                            2. answer 2
                                1. "One thing where CUDA shines if you can realy formulate your problem in a SIMD fashion AND can access the memory coalesced"
                                2. "If the memory accesses are not coalesced(1) or if you have different control flow in different threads
                                    the GPU can lose drastically its performance and the FPGA can outperform it"
                                3. if you have huge amount of small operations, but you cannot wrap them in a loop in one kernel,
                                   then your invocation times for the GPU kernel exceeds the computation time
                                4. "Also the power of the FPGA could be better (depends on your application scenarion,
                                    ie. the GPU is only cheaper (in terms of Watts/Flop) when its computing all the time)"
                                5. "Offcourse the FPGA has also some drawbacks:
                                        IO can be one (we had here an application were we needed 70 GB/s, no problem for GPU,
                                        but to get this amount of data into a FPGA you need for conventional design more pins than available).
                                        Another drawback is the time and money. A FPGA is much more expensive than the best GPU and the development times are very high."

                        5. FPGA or GPU? - The evolution continues
                           http://mil-embedded.com/articles/fpga-gpu-evolution-continues/
                            1. "GPUs historically have been power hogs", "but the latest GPU products have reduced that liability"
                            2. "Unlike FPGAs, GPUs run software, and executing an algorithm in software takes time"
                               "GPUs' massively parallel construction enables them to run a software algorithm much faster than a conventional processor could"
                            3. "Unlike FPGAs, GPUs excel in floating-point operations"
                            4. "In fact, many newer signal-processing algorithms are aimed at GPUs.
                                Moreover, GPUs are designed with very fast memory,
                                and new direct memory access (DMA) techniques allow high-volume sensor data to be streamed to the GPU without consuming GPU clock cycles."
                            5. "GPUs also offer good backward compatibility"
                               "It's no small matter to upgrade the algorithm on an FPGA or to move an algorithm to a newer FPGA"
                               "GPUs, furthermore, are supported with a wide array of open development tools and free math function libraries."
                            6. "GPUs are increasingly found in radar processing"

            6. FPGA cloud usage on DNN, deep learning area?
                1. DLAU: A Scalable Deep Learning Accelerator Unit on FPGA
                   https://arxiv.org/pdf/1605.06894.pdf
                    1. mostly FPGA chip designs

            7. FPGA usage on key-value stores and stoarge and in-memory storage?
                1. Impact of Cache Architecture on FPGA-Based Processor/Parallel-Accelerator Systems    [2012, 43 refs]
                   https://www.youtube.com/watch?v=vfuPD0WWmSs
                    1. it's about the "Cache Architecture" on a "Processor/Parallel-Accelerator Systems"
                       i.e. multiple FPGAs connected with CPU, with an on-chip data cache, the designs

                2. An FPGA-based In-line Accelerator for Memcached    [2014, 50 refs]
                   http://www.cs.princeton.edu/courses/archive/spring16/cos598F/06560058.pdf
                   https://www.hotchips.org/wp-content/uploads/hc_archives/hc25/HC25.50-FPGA-epub/HC25.27.530-Memcached-Lavasani-UTexas.pdf
                    1. highlights
                        1. FPGA process network packets bypassing CPU
                           The CPU cores and FPGA all connects to the same shared memory (coherent memory system)
                            1. evaluation is done by simulation (the gem5 simulator)
                        2. profile the application to determine the hottest code paths, and extract them to FPGA
                           if execution cannot be fully satisfied on FPGA, we rollback to CPU
                        3. achieves ~2x energy efficiency compared to CPU only in the same throughput

                3. devicepros: HW Acceleration of Memcached
                   https://www.flashmemorysummit.com/English/Collaterals/Proceedings/2014/20140805_B12_Sturgeon.pdf
                    1. highlights
                        1. "Network not saturated for small Object sizes"
                        2. FPGA and KV store resides on NIC end. Access DRAM through PCIe.
                           Memcached logic is entirely built in FPGA
                        3. results
                            1. 7K queries / Watt vs. 100-200 queries / Watt
                            2. Significantly better max latency and distribution

                4. Achieving 10Gbps line-rate key-value stores with FPGAs    [2013, 51 refs]
                   https://www.usenix.org/system/files/conference/hotcloud13/hotcloud13-blott.pdf
                   https://www.usenix.org/sites/default/files/conference/protected-files/blott_hotcloud13_slides.pdf
                    1. highlights
                        1. "fully pipelined dataflow architecture"
                        2. "Scalability in throughput is achieved by widening or duplication of the data path"
                        3. modular design: each stage in the pipeline provides identical input and output interface formats, based on AXI-4 streaming protocol,
                                           and standardize how key, value, and meta-data, are conveyed between macro-level pipeline stages
                        4. "Collision handling is in software solutions typically solved by chaining a flexible number of keys to a single hash table index.
                           In hardware, collision handling is often supported  hrough a parallel lookup [3] of a fixed number of keys that map to the same hash table index"
                            1. [9] Hash Table for Large Key-Value Stores on FPGAs

                5. question: the FPGA are mostly handling in-memory storage. can FPGA offload disk/SSD access?
                             if we cannot use FPGA to accelerate disk/SSD access, then the usage on persistent storage would be limited to compression/crypto/etc, non-architecture shifting
                             NVDIMM with PCIe DMA by FPGA may be another way to use FPGA with Persistent Flash.
                             But disk handling and journaling usually consists of the majority of storage logic code and error handling, which is complex and favors CPU I think
                    1. FPGA Drive
                       https://fpgadrive.com/
                    2. FPGA to SSD via PCIe
                       https://forums.xilinx.com/t5/Zynq-All-Programmable-SoC/FPGA-to-SSD-via-PCIe/td-p/686622
                    3. Interfacing FPGA and a storage device
                       https://electronics.stackexchange.com/questions/129708/interfacing-fpga-and-a-storage-device
                    4. SSD SATA 3.0 Host Controller 1.5/3/6Gbit/s for Xilinx FPGA
                       http://chevintechnology.com/wp-content/uploads/2015/11/ProductBrief_SATA-HC_xilinx_v1.0.pdf

6. readings: Ceph BlueStore
    0. ceph bluestore git code
    1. checking github explore
    2. checking ceph blueprint
    3. checking ceph maillists
    4. ceph release notes
    5. ceph bluestore analysis
    6. ceph document in codebase
        1. BlueStore Internals
           https://github.com/ceph/ceph/blob/master/doc/dev/bluestore.rst
            1. very good. after checking so many materials, actually this is the most complete bluestore write strategies. including WAL or double write issue
    7. ceph bluestore codebase
        1. a philosophy is, the hot happy IO path must be short, because this is what 99.99% customer traffic goes through.
           the exception handling can be complex, and that's ok
        2. BlueStore codebase is actually much simpler than FileStore.
           Also, don't need to implement the FileJouranl.cc, that saves a lot of work and maintenance. Though BlueStore does use RocksDB transaction to commit metadata.
           BlueFS is a ~3000 LOC very simple FS. The allocator is ~3000 LOC, simple actually.
            1. so overall these simpleness saves a lot of maintenance work,
               bug potential, inconsistency, adopt to different FS and hack/walkarounds to their glitches,
               and shorter path performance gain
    8. ceph write path paper
        1. Understanding Write Behaviors of Storage Backends in Ceph Object Store    [2017, 2 refs]
           http://storageconference.us/2017/Papers/CephObjectStore.pdf
            1. very good paper to explain ceph write path and characteristics of each filestore/bluestore
            2. captured my interested points
                1. filestore
                    1. "FileStore first writes incoming transactions to its own journal
                        disk in an append-only manner. After writing to the journal,
                        worker threads in FileStore perform actual write operations to
                        the file system with the writev() system call. In every a
                        few seconds up to filestore_max_sync_interval (5
                        seconds by default), FileStore calls syncfs() to the disk and
                        then drops the journal entries"
                    2. "Having the external journal also brings a performance
                        benefit as the write speed is improved due to the appendonly
                        logging mechanism"
                    3. "due to some issues related to extended attributes (xattr),
                        XFS is the only file system officially recommended by Ceph
                        developers"
                    4. "journaling of journal [7] problem when
                        implementing distributed storage services on top of a local
                        file system"
                2. bluestore
                    1. "One problem in FileStore is a doublewrite
                        penalty caused by the external journaling"
                    2. "Since BlueStore
                        bypasses the local file system layer, file system overheads such
                        as journaling of journal can be avoided"
                    3. "POSIX
                        does not provide any efficient way to retrieve the objects from
                        multiple directories. Another benefit of using RocksDB is that
                        Ceph can simply retrieve and enumerate all objects stored in
                        the system"
    9. ceph bluefs/bluestore materials
        1. BlueStore, A New Storage Backend for Ceph, One Year In (2017.Mar)
           https://www.slideshare.net/sageweil1/bluestore-a-new-storage-backend-for-ceph-one-year-in?qid=154392c8-791a-4fcc-b584-40a72a0696e7
            0. very good material
                1. video: ceph developer monthly: 2016-JUN-21 -- Ceph Tech Talks: Bluestore
                   https://www.youtube.com/watch?v=kuacS4jw5pM
                2. SDC 2017 - Goodbye, XFS: Building a new, faster storage backend for Ceph - Sage Weil (2017.Sep)
                   https://www.youtube.com/watch?v=e9UPmVcq2jU
            2. logged before
            1. included the posix motivation of using bluestore and bluefs
            2. included the bluefs main design strategies
            3. three ways to write
                1. new allocation - directly goes to disk extent - commit transaction
                    1. after that, we have the metadata pointing to it, and we commit the rocksdb transaction, and we are done.
                    2. any write larger than "min_alloc_size" goes to new block
                        1. so, only small overwrites exist, which can be handled by deffered write
                        2. large overwrite goes to new block, and we need GC to handle holes
                2. deferred writes - any overwrite, which needs transaction, goes to rocksdb first, then async overwrite, and then cleanup the temporary kv pair. is that right?
                    1. this is the effective journal we do for filestore and newstore.
                       we only do it when the write is relatively small
                    2. the idea is, if writting to logging is faster, write to logging, or otherwise
                       we write them to disk somewhere, and commit the transactions in rocksdb
            4. the "Transaction State Machine"
                1. the CDM video made it more clear, we write to disk first (to AIO_WAIT),
                   after it's done, we write and commit transaction to rocksdb
                    1. so it's still double write?
            5. BlueStore using directIO, no kernel buffering
            6. FileStore issues about transactions
                1. first serialize and journal every transaction
                   then, write to the filesystem
                    1. the issue is we have full data journal, we write everything twice, so half of throughput
                    2. in BlueStore, we sometime need to write twice too, but we don't need to write data twice

        3. The new Ceph 12.2 Luminous and its BlueStore storage backend
           https://www.virtualtothecore.com/en/the-new-ceph-12-2-luminous-and-its-bluestore-storage-backend/
        4. Understanding BlueStore, Ceph's New Storage Backend: Tim Serong, SUSE (2017.July)
           https://www.youtube.com/watch?v=zpIsxz3qVLs

        5. Ceph BlueFS分析
           http://www.bijishequ.com/detail/271710
            1. good article. mostly explained the major design decisions of bluefs
            2. "BlueFS是个小型文件系统，小体现在功能简单，没有实现Posix接口，不支持对文件的覆盖写操作只支持追加写，没有本地文件系统的树形层次结构，只有扁平的目录到文件的映射关系。和BlueStore一样，BlueFS也依赖底层BlockDevice模块，使用它来管理磁盘空间的分配释放，将IO通过Libaio写到裸盘。和BlueStore不一样的是元数据的管理，BlueStore将元数据全权交给RocksDB，BlueFS存在的目的就是为了支持RocksDB，因此不能反过来依赖RocksDB，只能靠自己来解决元数据管理问题。"
        6. Introducing BlueStore - SUSE whitepaper
           https://www.suse.com/docrep/documents/qn1loi7fwf/suse_introducing_bluestore.pdf
            1. "Separating the metadata from the object data leads to interesting scenarios for multi-disk configurations"

        7. ceph存储引擎bluestore解析
           http://www.sysnote.org/2016/08/19/ceph-bluestore/
            1. good. one of the earliest article deep dive in bluestore in depth.
               now the write path can be
            2. bluestore元数据.
                1. Onode is always in memory, persistent as kv in rocksdb
                2. onode -> lextent (logical extent) -> blob (many:many) -> pextent (physical extent)
            3. I/O读写映射逻辑
                1. very good part. combined with the 3 ways to write in Sage's slideshare
                   now we can understand it in depth.
        8. ceph bluestore工作流程
           http://www.sysnote.org/2016/08/25/bluestore-work-flow/
            1. good doc. very in-depth io workflow
            2. "对于非WAL的写，比如对齐写、写到新的blob里等，I/O先写到块设备上，然后元数据提交到rocksdb并sync了，才返回客户端写完成（在STATE_KV_QUEUED状态的处理）；对于WAL（即覆盖写），没有先把数据写块设备，而是将数据和元数据作为wal一起提交到rocksdb并sync后，这样就可以返回客户端写成功了，然后在后面的动作就是将wal里的数据再写到块设备的过程，对这个object的读请求要等到把数据写到块设备完成整个wal写I/O的流程后才行"
        9. ceph中对象读写的顺序性及并发性保证
           http://www.sysnote.org/2016/08/29/ceph-io-sequence/
            1. in-depth
                1. 不同对象的并发控制 - "对于同一个PG里的不同对象，是通过PG锁来进行并发的控制"
                2. 同一个对象的并发顺序控制
                    1. "一个client情况，客户端对同一个对象的更新处理逻辑是串行的，要等前一次写请求完成，再进行后一次的读取或者写更新"
                        1. tcp消息的顺序性保证
                        2. ceph消息层的顺序性保证 - 消息序号m->seq
                        3. pg层顺序保证及对象锁机制 - "限制的是同一个对象上的读和写的并发"
                        4. store层保证顺序 - OpSequencer
                        5. primary发到replica的请求顺序 - "再将请求发给replica的时候也是有序的"
                    2. 多个client对同一个对象的并发访问
                        1. "ceph的rbd也是不能保证的"。一般都不能做到，需要集群文件系统

        10. Ceph Bluestore首测
            http://www.zphj1987.com/2016/03/24/Ceph-Bluestore%E9%A6%96%E6%B5%8B/
        11. New in Luminous: BlueStore
            https://ceph.com/community/new-luminous-bluestore/

        12. Ceph BlueStore解析：Object IO到磁盘的映射
            http://www.bijishequ.com/detail/208117
            1. good in depth
        13. 拆开Ceph看队列和线程
            http://www.bijishequ.com/detail/252606
            1. interesting angle to study the problem
        14. 聊聊dmclock 算法
            http://www.bijishequ.com/detail/252461?p=
            Ceph QoS初探（下）
            http://www.bijishequ.com/detail/251768?p=
            1. good materials

7. readings: ScanDisk opensource ZetaScale
   https://github.com/SanDisk-Open-Source/zetascale
    1. Ceph开发每周谈Vol 21 | ZetaScale | CMP/WriteSame
       https://www.xsky.com/tec/ceph-weekly-vol-21/
        1. "ZetaScale 是 SanDisk 为高速 Flash 设备研发的 KV 库，能够充分并行化并且利用好物理设备的特性"
        2. "在上次的 Linux Vault 上 SanDisk 介绍了他们利用 ZetaScale 结合 BlueStore 来替换 RocksDB 的方案。通过展示的性能报告来看，能够至少提高 50% 的基准性能"
    2. ZetaScale™ Software - Key Features
       http://cdn-docs.av-iq.com/dataSheet//ZetaScale%E2%84%A2_Datasheet.pdf
        1. key features
            1. Intelligent DRAM caching
            2. Optimized threading to maximize concurrency and minimize response time
            3. Support for atomic operations, snapshots, transactions,

8. readings: 王豪迈 - Ceph开发每周谈
    1. Vol 103 | Async OSD
        1. "为了实现高速 NVRAM 这类性能设备的支持，同时重构代码来得到更简约的代码，在十二月的 CDM(Ceph Developer Meeting)上讨论了希望重构 OSD 实现异步化的目标。实际上这个话题已经持续了一年多，只是在现在这个关口，这个事情的优先级上升，成为社区团队重要的优先事项。"
        2. "这个任务是长期的，同时也是艰巨的，主要期望达到以下状态:
            1. 实现每个 CPU Core 独立工作，减少共享资源以及锁维护。
            2. 最小化内存分配
            3. 每个服务器一个进程
            4. 不同的网络后段对应不同的介质类型"
    2. Vol 97 | PebblesDB From SOSP 2017
       http://chuansong.me/n/2019552051733
        1. "Pebbles 是一个面向写优化的键值数据库，类似于 RocksDB 但极大的增大了写带宽和减少写放大，同时带来了10-30% 在小范围查询的负担，在 SOSP 17 发表了关于 PebblesDB 的文章（ http://www.cs.utexas.edu/~vijay/papers/sosp17-pebblesdb.pdf ）。同时，PebblesDB 也在 Github（ https://github.com/utsaslab/pebblesdb ）上开源。"
        2. "这个数据结构成为 FLSM(Fragmented Log Structured Merge Tree)"
    3. Vol 96 | dmClock(Ceph QoS) Update
       http://chuansong.me/n/2010436051633
        1. how to dmclock QoS is broken down and constructed the design
        2. slideshare: Implementing distributed mclock in ceph
           https://www.slideshare.net/ssusercee823/implementing-distributed-mclock-in-ceph
    4. Vol 93 | Key Value SSD
       http://chuansong.me/n/2010436351122
        1. "三星在 SSD 这块一直有比较前沿的技术研究，在早些时候就主要针对 SSD Key Value 接口有过样品，因为 SSD 本质上是一个类似 Key Value 寻址的模式访问，现在主流的块访问都是模拟出的接口。因此，SSD 厂商寻求直接提供 Key Value 来避免损耗，同时，对于很多应用来说，Key Value 反而是想要的模式，因为如果应用需要 KV 接口模型，最后到设备层需要经过 Key Value 到文件的组织，文件到块设备的组织，块设备在 SSD 重新寻址的多层逻辑，实际上通过 Key Value 原生接口可以绕过所有。"
        2. "目前 Key Value API 的标准已经提交给 SNIA Object Drive 组审阅"
    5. Vol92 | New Key Value Store For Heterogeneous Storage From Intel
        1. "主要将利用高性能 Persistent Memory 来做聚合，将 Optane 和其他 SSD 作为主存使用。"
    6. Vol 91 | NVME Over Fibre Channel(SNIA SDC 2017)
       http://chuansong.me/n/2010436551047
        1. "闪存优化是前两年的技术热点，从今年起，在块存储上基本都是 NVME Over Fabric 的话题。"
        2. "NVME Over Fabric 从去年开始在 Linux 内核上进了第一个版本后，一直都是 RDMA 的方案，不管是 RoCE 还是 Infiniband 后端。今年 NVME Over FC 也已经进入内核，大量存储厂商其实更青睐于 FC 方式。"
        3. "用户在使用 NVME Over FC 上反过来其实可以极大推动 NVME 的普及，现实是 NVME 和 RDMA 在传统存储都是新东西，很难普及，而如果使用 FC 可以极大降低用户的使用门槛。"

9. readings: remaining piled up papers
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
                4. In Table 1 it's said Clay Code has polynomial sub-packetization level.
                   But in the "(n = qt, k, d) (α = q^t ,β = q^(t−1))" given later in paper, α is exponential to n. It's confusing.
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

            4. notations

              n := total codec length
              k := data fragment count
              d := number of helper nodes, ranging from k to (n-1)
              rec-read ampl = dβ/(kα) = d / (k * (d - k + 1)) * k    // normal RS is k
              α := sub-packetization level, see section "Clay code parameters"

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

10. readings: remaining piled up papers
    1. Protocol-Aware Recovery for Consensus-Based Storage    [2018, 0 refs, FAST18 best paper]
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

7. readings: remaining piled up papers
    1. Protocol-Aware Recovery for Consensus-Based Storage    [2018, 0 refs, FAST18 best paper]
       https://www.usenix.org/conference/fast18/presentation/alagappan
        1. logged before
    2. LightNVM: The Linux Open-Channel SSD Subsystem    [2017, 22 refs]
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

8. readings: remaining piled up papers
    1. Book: Designing Distributed Systems - Patterns and Paradigms for Scalable, Reliable Services by Brendan Burns
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

12. readings: remaining piled up papers
    1. Redundancy Does Not Imply Fault Tolerance: Analysis of Distributed Storage Reactions to Single Errors and Corruptions [2017, 9 refs]
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
    2. Evolving Ext4 for Shingled Disks    [2017, 9 refs]
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

11. readings: remaining piled up papers
    1. Application Crash Consistency and Performance with CCFS    [2017, 12 refs]
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

5. readings: remaining piled up papers
    1. I Can't Believe It's Not Causal! Scalable Causal Consistency with No Slowdown Cascades  [2017, 6 refs]
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

    2. FlashBlox: Achieving Both Performance Isolation and Uniform Lifetime for Virtualized SSDs  [2017, 9 refs]
       https://www.usenix.org/system/files/conference/fast17/fast17_huang.pdf
        1. SSD virtualization is an interesting approach.
           This paper pin app workload to channel/die to provide different levels of isolation.
           periodic inter-channel swap and block-mapping migration are used to balance the different wear-out level from different app workloads.
        2. highlights
            1. SSD virtualization - interesting as this paper thinks from hardware perspective
                1. by pin app workload to dedicated channels, or dedicated dies
                    1. question: if other channels are idle, can the app temporarily expand out of its pined to use others?
                                 I think that's the foundamental weakness of this approach. software virtualization may do better.
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

2. readings
    1. The TLA+ Book: Part II
       https://lamport.azurewebsites.net/tla/book.html
        1. WIP. Finished the Chapter 8 Liveness and Fairness. It's big.
        2. more TLA related case study
            1. A SUCCESS OF TLA+ IN AZURE STORAGE
            2. How Amazon Web Services Uses Formal Methods  [2015, 123 refs]
            3. Who Builds a Skyscraper Without Drawing Blueprints? by Leslie Lamport
               https://resnet.microsoft.com/video/31835
                n. related materials
                    1. Use of Formal Methods at Amazon Web Services
                       http://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf
                    2. Why Amazon Chose TLA+
                       https://groups.google.com/forum/#!topic/tlaplus/UwYW6XqyDvE
                        1. people shared a lot of materials,
                           e.g. TLA+ spec for snapshot isolation
                    3. TLA+ 3-Day Training
                       Day 2 PM http://resnet/fullVideo.aspx?id=37325 - Liveness
                       Day 3 AM http://resnet/fullVideo.aspx?id=37326 - Refinement mapping
                        1. this is useful to be used with book
                    4. tlaplus/DrTLAPlus
                       https://github.com/tlaplus/DrTLAPlus
                        1. there are many tutorials here
                        2. the TiDB percolator spec
                           https://github.com/tlaplus/DrTLAPlus/tree/master/TiDB
                           https://github.com/pingcap/tla-plus/blob/master/Percolator/Percolator.tla
                        3. Paxos
                           https://github.com/tlaplus/DrTLAPlus/blob/master/Paxos/Paxos.tla

3. readings: The TLA+ Book
    1. The TLA+ Book: Part III: The tools
       https://lamport.azurewebsites.net/tla/book.html
        1. I wonder to what extent TLC can check liveness & fairness
           so reading the how TLC works and limitations and walkarounds
        2. finished reading the Part III
    2. The TLA+ Book: Part II: Real Time
        1. I think, using math in TLA+ to express these time constraints, is making simple things complicated
           maybe a practical programming language assist can be more suitable.
            1. anyway, with the limit of TLC, the only workable part of TLA+ is just plain state transition, constraints, ENABLE, simple liveness,
               and in "nice" form (Init, Next, Temporal, Invariant, ImpliedInit, ImpliedAction, ImpliedTemporal, Constraint, ActionConstraint).
               this is what programming language and common test cases can do, easier to understand and with better flexibility
            2. realtime properties can be considered as a strong form of liveness,
               specifying not just that something must eventually happen, but when it must happen
    3. TiDB TLA+ Percolator code
       https://github.com/pingcap/tla-plus/blob/master/Percolator/Percolator.tla
        1. highlights
            1. reading the code.
            2. checked, CockroachDB doesn't have the similar TLA+ spec posted for its transaction design
            3. general steps
                1. start: assign start_ts. state: init => working
                2. get: first cleanup stale lock and data (key_data), then read key. state: working => prewriting
                3. prewrite: lock key and place data (key_data), assign commit_ts. state: prewriting => committing
                4. commit: write data (key_write), unlock key. state: committing => committed
                n. questions:
                    1. what is a stale lock? lock.ts <= client.start_ts. why is it reasonable, can a second reader clear the first locker?
                    2. I don't see how T2_read -> T1_commit -> T2_commit case is stopped
                    3. I don't see how T1, T2 both commit write to same key stopped
        2. running the code
            1. download tla2tools.jar from
                https://tla.msr-inria.inria.fr/tlatoolbox/dist/tla2tools.jar
               use java 1.8+. run with
                ---
                java -cp ./tla2tools.jar tlc2.TLC -deadlock -workers 4 Test1
                ---
            2. continue to install the TLA+ toolbox, TLAPS
        n. related materials
            1. TiDB transaction model
               https://github.com/pingcap/blog-cn/blob/master/tidb-transaction-model.md
                1. explains the design corresponds to Percolator.tla
            2. TiDB Spanner Truetime transaction
               https://github.com/pingcap/blog-cn/blob/master/Spanner-cap-truetime-transaction.md
                n. related materials
                    1. 学习 TLA+ - Percolator Transaction
                       https://www.jianshu.com/p/721df5b4454b
                        1. looks like the author of Percolator.tla
                        2. mentioned "Hybrid Logic Clock" from CockroachDB
                    2. 分布式系统的时间
                       https://www.jianshu.com/p/8500882ab38c
            3. others recorded in separated notes

4. readings: TLA+ and Snapshot Isolation and Serializable
    1. Serializable Isolation for Snapshot Databases    [2008, 201 refs]
       https://courses.cs.washington.edu/courses/cse444/08au/544M/READING-LIST/fekete-sigmod2008.pdf
        1. logged in separated notes
    2. A Critique of Snapshot Isolation    [2012, 37 refs]
       https://www.slideshare.net/MaysamYabandeh/wsi-eurosys
        1. logged in separated place
    3. A Critique of ANSI SQL Isolation Levels
        1. logged in separated place
    4. Calvin: Fast Distributed Transactions for Partitioned Database Systems
        1. logged in separated place
    5. Serializable Snapshot Isolation in PostgreSQL
        1. logged in separated place
    6. How Amazon Web Services Uses Formal Methods
        1. logged in separated place

4. readings: remaining distributed transaction study paper
    1. Spanner, TrueTime & The CAP Theorem    [2017, 11 refs]
       https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45855.pdf
        1. logged in separated notes
    2. Hyder - A Transactional Record Manager for Shared Flash    [2011, 130 refs]
       http://web.eecs.umich.edu/~michjc/eecs584/Papers/cidr11_hyder.pdf
        1. logged in separated notes

5. readings: misc remaining papers piled up
    1. Service Fabric: A Distributed Platform for Building Microservices in the Cloud    [2018, 0 refs]
       https://dl.acm.org/ft_gateway.cfm?id=3190546&ftid=1957693
        1. interesting paper as how Microsoft Azure implement its service fabric to support micro-service management.
           strong membership consistency, SF-Ring, Reliable Collections are interesting features and baked by production customer needs
        2. highlights
            1. Service Fabric is being widely used in production, includes MS Azure SQL DB, and several
                1. highly-available, fault-tolerant, agile, scalable. optimize resource usage
            2. key features
                1. strong consistency
                    1. actually as I read, it's the strong consistency of ring membership.
                        1. see later. ring membership did spent a lot of effort to make it stable
                2. support for stateful services
                    1. i.e. the on local node, replicated, data structures (dictionaries, queues) - Reliable Collections
                        1. some customer services does rely on that. local acess is faster than backend storage
            3. Failover Manager (FM) and Placement & Load Balancer (PLB)
                1. FM by replica set
                2. Unlike DHTs, PLB explicitly assigns each service replica to nodes in SF-Ring
                3. PLB uses Simulated Annealing to fast find close to optimal placement, of complex multi-dimensional constraints
                    1. 10s timer value, and 120s timer value
            4. SF-Ring
                1. Membership - which nodes are alive or not
                    1. each node keep track of its multiple immediate successor nodes and predecessor nodes, called neighborhood set
                    2. node gossip with neighborhood set with leases.
                    3. but final node alive/dead is arbitrated by the centralized lightweight arbitrator
                        1. critical to make the alive/dead thing stable.
                            1. nodes may tell unstable or conflicting truth of alive/dead upon each other
                        2. need majority confirm to mark a node alive/dead
                    4. many other details. and cascading detection problem (which is interesting) is avoided.
                       to make the ring membership of strong consistency
                2. Consistent Routing
                    1. if less nodes, a node stores full table and send message directly to the destination node
                       if too many nodes to allow memory to store full table, use SF-Ring routing
                        1. today, most time we use direct communication. except
                            1) node starts up and discover routings
                            2) routing to virtual addresses
                    2. SF-Routing
                        1. exponential expand: the i-th route table entry contains node id of n+i^i
                        2. routing table is symmetric/bidirectional, i.e. stores entries both forward and backward
                        3. essentally, the routing is a binary search
                    3. nearby nodes on the ring are selected preferably from different failure domains
                    4. leader election: any key k has and always a unique node corresponds to it. that node is the primary.
            5. lessions learned
                1. the absence of a functional disk renders app unhealthy, need optional disk heartbeat to detect
                2. automatic rollback mechanism (for customer app I think) to relieve customer from fear to upgrade
                3. "invisible" external dependencies need care
            6. future directions
                1. serverless
                2. geo-distributed Reliable Collections
            7. questions
                1. how is isolation implemented? by windows container? HyperV VM?
                    1. the paper didn't describe it clearly through
                2. since PLB explicitly assign service replicas to nodes, then why we need the Ring,
                   which maps key to node using something like consistent hashing?
                3. placement metadata can take memory space / disk space to store.
                   how does PLB store these states?

    2. Store, Forget, and Check: Using Algebraic Signatures to Check Remotely Administered Storage    [2006, 406 refs]
       ftp://ftp.cse.ucsc.edu/pub/darrell/schwarz-icdcs06.pdf
        1. we can fetch the signature from parity nodes, rather than fetch data and then calculate signature,
           to verify data integrity, because "calculating parity and taking a signature commute"
```