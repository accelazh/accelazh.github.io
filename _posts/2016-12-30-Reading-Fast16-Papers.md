---
layout: post
title: "Reading FAST16 Papers"
tagline : "Reading FAST16 Papers"
description: "Reading FAST16 Papers"
category: "storage"
tags: [storage, fast16, fast]
---
{% include JB/setup %}

Reading notes of the FAST16 conference. Actually I've also read some related FAST15 papers.

__[NOVA](http://github.com/NVSL/NOVA): [A Log-structured File System for Hybrid Volatile/Non-volatile Main Memories](https://www.usenix.org/conference/fast16/technical-sessions/presentation/xu)__    [2016, 3 refs]

```
1. very good paper, helpful analysis on NVM backgrounds, good implementation detail
   NOVA is a log-structured FS designed for hybrid DRAM/NVMM, it outperforms existing NVMM FS by wide margin on a wide range of applications while providing strong consistency and atomicity guarantees
    1. essentially, the random access support of NVM allows sort of combining the goodiness of log-structured FS and write-in-place FS

2. backgrounds
    1. key challenges to design FS for NVMM
        1. since NVM is much faster, they need to minimize software overhead to fully exploit NVMM
        2. implement strong consistency guaratnees with frequently force flush
    2. what underlying devices provide for write atomicity and write ordering
       morden processors and their caching hierarchies may reorder store operations
        1. disk guaratnees sector write are atomic
        2. processors guaratnee only that 8-byte aligned stores are atomic
        3. modern processors support 64-bit atomic writes for volatile memory
        4. previous x86 processor support clflush: strictly ordered, needlessly invalidate the cache line
           modern x86 adds new instructions for NVM handling
            1. clflushopt: a more efficient verison of clflush
            2. clwb: explicitly write back cache line without invalidating it
            3. PCOMMIT: force stores out to NVMM
    3. existing ways to implement complex atomic operations
        1. journaling: first write journal, then write data, needs to write twice
        2. shadown paging: rely heavily on trees; copy-on-write, then update nodes between pages and root; suffer from cascade of updates
        3. log-structured: data is organized in log format, rely on log to implement atomicity;
           need to be able to always provide large contiguous regions to write log, need to be careful with GC

3. key designs
    1. keep logs in NVMM and indexes in DRAM
        1. use radix tree as the index, because kernel implements it mature
    2. give each inode its own log
        1. allows concurrent updates and recovery
    3. use logging and lightweight journaling for complex atomic updates
        1. logging works for single inode atomic updates
           journaling works for cross inode atomic updates; only save necessary data
           the most complex POSIX rename operation involves up to four inodes; journal are always no more than 64 bytes
        2. the code to enforce write ordering
            ```
            new_tail = append_to_log(inode->tail, entry);
            // writes back the log entry cachelines
            clwb(inode->tail, entry->length);
            sfence(); // orders subsequent PCOMMIT
            PCOMMIT(); // commits entry to NVMM
            sfence(); // orders subsequent store
            inode->tail = new_tail;
            ```
           if new instructions are not supported, NOVA fallbacks to movntq and uses a combination of clflush and sfense
    4. implement the log as a singly linked list
        1. since NVM allows fast random access, the log doesn't need to be sequential
        2. space allocation, space reclaim, GC are much easier and perform much better compared to the old LFS way
    5. do not log file data
        1. use copy-on-write for modified pages, then append pointer changes to the log
        2. a pointer to log tail indicates log commit
        3. but, radix tree -> log entries -> data pages, adds an interal layer of indirection overhead
    6. per-CPU free list, journal, inode table
        1. most metdata level structures are per-CPU each one, to ease locking and improve concurrency
        2. allows only one open transaction at a time on each core and per-CPU allows for concurrent transactions
    7. NVMM space management
        1. devide NVMM into pools, one per CPU, and keep lists of free NVMM pages in DRAM
        2. if no page are available in the current CPU's pool, NOVA allocates pages from the largest pool
        3. to reduce the allocator size, NOVA uses red-black tree to keep the free list sorted by address, allowing for efficient merging
        4. allocates log space aggressively; double the space each time until certail size, then add by constant number of pages
        5. on a normal shutdown, NOVA records the allocator state to the recovery inode's log, to allow fast recovery
           on power failure, NOVA recoveries by scanning all inodes' log
            1. power failure recovery is fast,
               because of per-inode log,
               log size is small (without file data),
               and log entry count is roughly the number of extents in the file
    8. directories
        1. log contains dentry CRUD and inode updates
        2. use a in DRAM radix tree to index dentry; dentry name is hashed before use
    9. atomic mmap
        1. kernel Direct Access (DAX) expose NVMM directly via load & store, bypass page cache
           by mapping physical NVMM file data pages into the app's address space
            1. DAX-mmap provides NVMM so the only atomicity mechanisms available to programmer are 64-bit writes, fences, cache flush
        2. NOVA atomic-mmap
            1. when app use atomic-mmap to map file into its address space,
               NOVA allocates replica pages from NVMM, copies the file data to the replica pages,
               and then maps the replicas into the address space
            2. when app use msync on the replica pages, NOVA handles it as a write request,
               uses movntq to copy data from replica pages to data pages directly, and commits the changes atomically
            3. it does not support DAX-mmap. atomic-mmap has higher overhead but provide strong consistency
               the normal DRAM mmap is not atomic, because OS may write back anytime
    10. garbage collection
        1. data pages are immediately reclaimed when copy-on-writing file data
        2. Fast GC reclaims invalid log pages by deleting them from the linked list
        3. Thorough GC reclaims by copy live log entries to a new page, i.e. to compact them
        4. it doesn't use checkpoint, but by detect and mark log entries as invalid and reclaim
            1. a log entry is dead if it is no longer useful
            2. a log page is dead, if all entries on it is dead
        5. NOVA resolves the issue that many LFSs suffer from,
           i.e. they have performance problems under heavy write loads, especially when the file system is nearly full.
            1. NOVA reduces the log cleaning overhead by
                reclaiming stale data pages immediately,
                keeping log sizes small,
                and making garbage collection of those logs efficient
    11. shutdown and recovery
        1. when NOVA mounts, it lasy (build at first access) rebuild structures in DRAM
        2. to recovery by log/journal
            1. first, check journal and rollback any uncommitted transactions
            2. scan log in parallel
            3. during the recovery scan, NOVA builds a bitmap of occupied pages, and rebuild the allocator base on it
    12. NVMM protection
        1. NOVA must make sure it is the only system software that accesses the NVMM
        2. upon mount, the whole NVMM region is mapped as read-only
           whenever NOVA needs write, it opens a write window by disabling processor's write protection control (CR0.WP)
        3. CR0.WP is not saved across interrupts, so NOVA disables local interrupts during the write window

4. insteresting materials referenced by this paper
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
```

__[Optimizing Every Operation in a Write-optimized File System](https://www.usenix.org/conference/fast16/technical-sessions/presentation/yuan)__    [2016, 1 refs]

```
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
                1. all relevant messages will be in a node’s buffer on the root-to-leaf search path
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

5. pre-readings, about LSM-tree, Fractal tree, COLA tree, and Bε-tree
    1. LSM trees (used in BigTable etc.) and Fractal Trees (used in TokuDB)
       https://www.quora.com/What-are-the-major-differences-between-LSM-trees-used-in-BigTable-etc-and-Fractal-Trees-used-in-TokuDB
        1. Write Optimization: Myths, Comparison, Clarifications
           https://www.percona.com/blog/2011/09/22/write-optimization-myths-comparison-clarifications/
           https://www.percona.com/blog/2011/10/04/write-optimization-myths-comparison-clarifications-part-2/
            1. “write optimization in B-trees involves maximizing the useful work we accomplish each time we touch a leaf”
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
                    1. FDS’ main goal is to expose all of a cluster’s disk bandwidth to applications
                    2. Even when computation is co-located with storage, all storage is treated as remote; in FDS, there are no “local” disks
                    3. FDS returns to the flat storage model: all compute nodes can access all storage with equal throughput
                    4. give each storage node network bandwidth equal to its disk bandwidth
                    5. The TORs load-balance traffic to the spine using ECMP (equal-cost multipath routing)
                        1. but, Long-lived, high-bandwidth flows are known to be problematic with ECMP
                    6. node NIC uses large-send offload, receive-side scaling (RSS), and 9 kB (jumbo) Ethernet frames
                       also, TCP stack is configured with a reduced MinRTO
                        1. need 5 flows per 10 Gbps port to reliably saturate the NIC?
                        2. At 20Gbps, a zero-copy architecture is mandatory
                    7. By design, at peak load, all FDS nodes simultaneously saturate their NICs with short, bursty flows.
                       A disadvantage of short flows is that TCP’s bandwidth allocation algorithms perform poorly.
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
                        1. cost-transparent APIs with runtime costs that match application developers’ intuitions
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
                   ε controls how much of an internal node’s space is used for pivots (Bε)
                   and how much is used for buffering pending updates (B − Bε)
                3. insertions are encoded as “insert messages”, addressed to a particular key, and added to the buffer of the root node of the tree
                   when enough messages have been added to a node to fill the node’s buffer, a batch of messages are flushed to one of the node’s children
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
```

__[Spinning Disks and Their Cloudy Future](https://www.usenix.org/conference/fast16/technical-sessions/presentation/brewer)__ (by Google)

```
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
            1. firmware: Hard­disk firmware attacks are not only possible, but appear to have been used
            2. ensure the data is “encrypted at rest”
            3. Fine­grained access control, using different keys for different areas of the disk
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
        (logged in the previous blog)
    
    3. study about Netflix Hsytrix
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
```

__[Flash Reliability in Production: The Expected and the Unexpected](https://www.usenix.org/node/194415)__ (Google)    [2016, 6 refs]

```
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
                1. SLC drives don’t have lower repair or replacement rates,
                   and don’t typically have lower rates of non-transparent errors
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

4. related readings
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
```

__[Environmental Conditions and Disk Reliability in Free-cooled Datacenters](https://www.usenix.org/node/194413)__ (Microsoft)    [2016, 1 refs]
       
```
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
```

__[Isotope: Transactional Isolation for Block Storage](https://www.usenix.org/node/194397)__ (Google)    [2016, 0 refs]

```
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
```

__[Uncovering Bugs in Distributed Storage Systems during Testing (Not in Production!)](https://www.usenix.org/node/194443)__ (Microsoft)    [2016, 0 refs]

```
1. a new methodology for testing distributed systems, successful use in Azure Storage vNext (and many other Azure's)
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

3. related readings
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
```

__[The Tail at Store: A Revelation from Millions of Hours of Disk and SSD Deployments](https://www.usenix.org/conference/fast16/technical-sessions/presentation/hao)__ (NetApp)    [2016, 3 refs]

```
1. a paper to analyze disk/ssd performance instability in field and in large-scale
   google's tail latency and tail tolerance are highly regarded
   performance instability can be more prevalent in the future, and the findings are just beginning
   root cause analysis looks still not deep enough
    1. data is collected from performance logs at customer deployments
    2. no previous systematic large-scale studies of performance instability in storage devices, this paper is the first
    3. P.S. disk (periodically) slow down is one of the major source of OP's customer incidents (e.g. why my latency raises)
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
        7. A slow driver can often make an entire RAID perform poorly (as like in Ceph? and make customer incidents as I see?)
           tail tolerance storage system design is necessary
    2. root cause analysis
        1. what may slow down the magnetic disks?
            1. the problems can be as performance “faults”
               all these problems can reduce disk bandwidth by 10-80% and increase latency by seconds
                1. mechanical wearout (e.g., weak head [1]),
                2. sector re-reads due to media failures such as corruptions and sector errors [2],
                3. overheat from broken cooling fans [3],
                4. gunk spilling from actuator assembly and accumulating on disk head [4],
                5. firmware bugs [41],
                6. RAID controller defects [16, 47],
                7. and vibration from bad disk drive packaging, missing screws, earthquakes, and constant “noise” in data centers [17, 29]
            2. current generation of disks begin to induce performance instability “by default”
                1. e.g., with adaptive zoning and Shingled-Magnetic Recording technologies
        2. what may slow down the SSDs
            1. SSD garbage collection
            2. Programming MLC cells to different states (e.g., 0 vs. 3) may require different numbers of iterations
               due to different voltage thresholds [51]
            3. The notion of “fast” and “slow” pages exists within an SSD
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
            1. ToleRAID can cut “read tails”
                1. in normal reads, the two parity drives are unused
                2. if one data drive is slow, ToleRAID can issue an extra read to one parity drive and rebuild the “late” data
            2. reactive approach
                1. If a drive (or two) has not returned the data for ST x (slowdown threshold) longer than the median latency
                   extra read will be sent
            3. proactive approach
                1. always performs extra reads to the parity drives concurrently with the original I/Os
            4. adaptive approach
                1. by default runs the reactive approach
                   when the reactive policy is triggered repeatedly for SR times (slowdown repeats) on the same drive,
                   then ToleRAID becomes proactive until the slowdown of the offending drive is less than ST
```

__[Flamingo: Enabling Evolvable HDD-based Near-Line Storage](https://www.usenix.org/node/194437)__ (Microsoft Research)    [2016, 0 refs]

```
1. MS research continuing from Pelican.
   Flamingo automatically generates the best data layout and IO scheduler configuration for Pelican per environment setup.
   near-line storage is being researched (vs cold/archival storage, vs online storage)

2. key findings/designs
    1. it has good summaries of what Pelican fails in section 2
    2. due to ambient temperature etc, per data center data layout and IO scheduler is required
    3. data layout and IO scheduler requires great effort to be tuned optimal and well-designed
       Flamingo takes rack spec, resource containts, perf targes, then automatically 
```

__[Estimating Unseen Deduplication—from Theory to Practice](https://www.usenix.org/conference/fast16/technical-sessions/presentation/harnik)__ (IBM Research)    [2016, 1 refs]

```
1. estimate dedup/compress ratio without reading entire dataset, output a estimated range
   15% sample is sufficient, fast sample by large super-chunks; run with 10MB less memory
   this paper is based on works of Valiant's "Estimating the unseen" [17][18]
```

__[Using Hints to Improve Inline Block-layer Deduplication](https://www.usenix.org/node/194453)__ (IBM Research)    [2016, 1 refs]

```
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
```

__[CloudCache: On-demand Flash Cache Management for Cloud Computing](https://www.usenix.org/node/194459)__ (VMware)    [2016, 2 refs]

```
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
```

__[Access Characteristic Guided Read and Write Cost Regulation for Performance Improvement on Flash Memory](https://www.usenix.org/conference/fast16/technical-sessions/presentation/li-qiao)__ (Edwin Sha)    [2016, 1 refs]

```
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
```

__[A Tale of Two Erasure Codes in HDFS](https://www.usenix.org/node/188447)__    [2015, 16 refs]

```
alternative link: https://www.usenix.org/system/files/conference/fast15/fast15-paper-xia.pdf

1. use two different erasure codes, dynamically converts between them, to trade-off between recovery speed and storage overhead
   essentially, fast code is the "adding more local groups" version of the compact code (slower but less storage)

2. highlights
    1. what two codes are used?
        1. fast code: product codes (three 2*5s), or LRC (12,6,2)
        2. compact code: product codes (one 6*5), or LRC (12,2,2)
    2. how to do the conversion (upcode, downcode)?
        1. showed in paper charts
        2. fast upcode/downcode from current coded fragments is worth more attention
    3. what condition triggers the conversion?
        1. if write cold, we starts to turn replicas into erasure-coded fragments
            next, if storage space is bounded, we use compact code
                  if read is hot, we use fast code
        2. the conversion condtion should have been worth more study
    4. how to insert this feature into HDFS?
        1. we implement HACFS as an extension to HDFS
    5. evluation (looks good)
        1. It reduces the degraded read latency by up to 46%,
           and the reconstruction time and disk/network traffic by up to 45%
```

__[Slacker: Fast Distribution with Lazy Docker Containers](https://www.usenix.org/system/files/conference/fast16/fast16-papers-harter.pdf)__    [2016, 5 refs]

```
1. large deployment using docker is slow, because the pulling image
   Slacker is a shared storage between image registry and docker worker nodes. so pull don't copy.
   It speeds up the median container development cycle by 20× and deployment cycle by 5×
    1. another approach is to p2p transfer image layers between worker nodes

2. key findings - HelloBench
    1. pulling packages accounts for 76% of container start time, but only 6.4% of that data is read
    2.  simple block-deduplication across images achieves better compression rates than gzip compression of individual images

3. key designs
    1. use snapshots and clones in shared storage for pull
       lazily fetching container data on startup
    2. docker storage driver is used as the feature insertion point
       make no changes to the docker registry or daemon
    3. as in related work, there are similar work for VMs
```

__[F2FS: A New File System for Flash Storage](https://www.usenix.org/system/files/conference/fast15/fast15-paper-lee.pdf)__    [2015, 66 refs]

```
1. designed for SSD (SATA/PCIe/NVMe SSD), but not for NVMM (what NOVA does)
   F2FS uses log-structured filesystem approach for flash. it uses multi-head logging.
   it fallbacks from normal logging to threaded logging at high disk utilization
   code public in Linux kernel 3.8.
    1. good to read

2. key findings
    1. in mobile smartphones, over 80% of total I/Os are random
       and more than 70% of the random writes are triggered with fsync
       by applications such as Facebook and Twitter
        1. This specific I/O pattern comes from the dominant use of SQLite in those applications
        2. frequent random writes and flush operations in modern workloads can seriously
           increase a flash device’s I/O latency and reduce the device lifetime

3. design highlights
    1. the inode structure looks like what the traditional EXT2 filesystem does
        1. dir tree is stored in dir inode as a hash table
            1. so directory size is limitted
        2. file inode has direct blocks, indirect blocks, inline data
    2. the "wandering tree" problem: because we append-only, if we update one block, we update its
       pointer in parent, then parent's parent ... the update propagates from tree leaf to root.
        1. to attack the "wandering tree" problem, we use NAT table
           all nodes address is stored in NAT table, NAT table entry does in-place update
            1. so, an block update, will only need to update its NAT table entry
               parent points to NAT table
            2. a node block is an inode, direct or indirect node
               NAT adds an extra layer of indirection
        2. the NAT table issues
            1. extra storage overhead
            2. efficient in-place update
            3. NAT table seems to be hot with a lot of updates, write-leveling?
            4. possible solution
                1. NAT table is stored in the Main Area, so it can be not a contiguous table, and dynamically allocate spaces
                   the index can be stored in memory
        3. NAT table is written to disk when checkpointing
            1. so, won't result in hot write in flush (except log update), because NAT entries are frequently updated
    3. Multi-head logging
        1. six major log areas, six logs open for writing
            1. node block - hot, warm, cold
               data block - hot, warm, cold
            2. what data is put into what area is completely static
        2. configuratble zones to be compatible with FTL
            1. FTL algoriths are largely classified into three groups: block-associative, set-associative, fully-associative
            2. map active logs to different zones to separate them in FTL, to avoid they are mixed into the same flash log blocks
                1. multi-head logging is also a natural match with the recent proposed "multi-streaming" interface [10]
                2. to me, separating warm/hot is also a match with what below paper does in FTL
                   "LAST: Locality-Aware Sector Translation for NAND Flash Memory-Based Storage Systems"
    4. Adaptive logging
        1. switch between normal logging and threaded logging
            1. normal logging: write log to consecutive blocks.
                      may suffer great performance degration when there is no free block
               threaded logging: write log to holes
                                 the write is random
            2. F2FS switch from normal logging to threaded logging
               when there are less than k (5% on default) of total sections are free
    5. checkpoint and recovery
        1. triggers a checkpoint when sync, umount and forground cleanning
        2. checkpoint does
            1. all dirty nodes and dentry blocks in the pagecache are flushed
            2. it suspends ordinary writing activities including system calls such as create, unlink, mkdir
            3. the filesystem metadata, NAT, SIT, SSA are written to disk
            4. F2FS writes a checkpoint pack, to the CP area
        3. after a sudden power-off, F2FS rollbacks to the latest checkpoint
            1. rather than what I wrote and ack-ed?
                1. fsync(fd) will ensure file is persistent
        4. roll-forward recovery
            1. for applications which frequently fsync (e.g. database), F2FS implements fsync to only flush specified written data
            2. direct node blocks have a special flag, to say it has changed after the last checkpointing
               when roll-forward recovery, those direct node blocks are collected and recovered

4. questions
    1. how does it do flash write-leveling?
        1. the data sections and metadata sections and other have different write patten
            1. but, anyway, flash FTL can take care of it
    2. the overhead of NAT
        1. it can use a lot of memory to cache the NAT for faster lookup
    3. how does log-structured flash fileysystem work with FTL?
        1. FTL also has log buffer, block re-mapping, and write-leveling stuff
        2. given we have FTL, flash in-place write is really slower than write in new block?
    4. checkpoint and recovery
        1. if not sync/fsync, everything written is lost, and restored back the lost checkpoint
           so, no write-ack -> ensure persistent guarantee

5. related readings
    1. A reconfigurable FTL (flash translation layer) architecture for NAND flash-based applications    [2008, 228 refs]
       http://idke.ruc.edu.cn/people/dazhou/Papers/a38-park.pdf
        1. this paper is referenced in F2FS to explain FTL zones and multi-head logging
           good paper to introduce flash structures and detailed concepts
        2. background introduction - this part is very good to read
            1. NAND flash structure
                1. each page has Spare Area, which can be used to store aux info, such as bad-block mark and ECC
                    1. in "A log buffer-based flash translation layer using fully-associative sector translation",
                       Spare Area is used to store mapping information between a logical page and a physical page
                2. operartion latency (year 2008)
                    1. page read: 20us
                       page program: 200us
                       block erause: 1.5ms
                       block program/erase cycle limit: 100,000
            2. FTL structure
                1. a typical FTL divide the NAND flash into a metadata area and a user data area
                    1. metadata area includes
                        1. Reserved blocks, for replacing initial or runtime bad blocks
                        2. Map blocks, for translating logical to physical addresses
                        3. write buffer blocks, for temporarily storing the incoming write data
                            1. or named as log buffer/log blocks? the main topic in below papers
                                "A Log Buffer-Based Flash Translation Layer Using Fully-Associative Sector Translation"
                                "LAST: Locality-Aware Sector Translation for NAND Flash Memory-Based Storage Systems"
                            2. write buffer block + data block => new data block (new data block is previously a free block, not the original data block)
                               this is the "merge operation"
                                1. in certain condition, if the log block holds the right data which should be stored in the data block
                                   we can do "switch operation" instead of merge, i.e. switch the log block and data block
                            3. the "merge operation" is time consuming. to reduce it is a main topic in FTL design
                    2. user area includes the other blocks
                2. mapping table designs
                    1. page mapping: map all blocks and all pages
                        1. advantage: always find free page for new writes
                           disadvantage: with more invalid pages scattered around, GC is consuming and tricky
                                         mapping table is very large, use a lot of memory
                        2. DFTL [7] dynamically load portion of page map into memory
                    2. block mapping: mapp all blocks, physical page offset is idential to logical's
                        1. advantage: smaller memory usage
                           disadvantage: every operation to the same logical page incurs a block copy
                    3. hybrid mapping [Kim et al. 2002]: compromise the block mapping and page mapping
                        1. maintain a small number of log blocks as the write buffer blocks for overwrite operations
                           the log block allows incoming data to be appended continuously as long as free pages are available in log blocks
                           when an overwrite operation occurs with the same logical page, the incoming data is written to a free page and invalid the previous page
                           when the log block has no additional free pages, the log block and the corresponding data block are merged into a free block
                    4. the fully associative sector mapping (FAST)
                       "A Log Buffer-Based Flash Translation Layer Using Fully-Associative Sector Translation"
                        1. a log block is shared by all data blocks
                        2. use a separated log block dedicated to handle sequential writes
                    5. [Chang and Kuo 2004] - utilize mapping units of variable sizes, for high-capacity flash
                        1. advantage: less memory usage, performance improvement, longer flash lifetime vs simple- or block-mapping schemas
                           disadvantage: the result is dependent on workload pattern, in worst case it becomes similar to page-mapping
                    6. [Kang et al. 2006] - the superblock-mapping schema
                       "A superblock-based flash translation layer for NAND flash memory"    [2006, 368 refs]
                        1. the flash is divided into superblocks, each superblock consist of N data block + M log block
                            1. in this way, set-associative is fully configurable, as from what FAST discussed
                            2. garbage collection overhead is reduced up to 40%
                            3. exploit "block-level temporal locality" by absorb writes to the same logical page into log block
                               exploit "block-level spatial locality" to increase storage utilization by that several adjacent logical blocks share a U-block
                            4. can we map sequantial writes and random writes into different superblocks?
                               and map hot and cold pages into different superblocks?
                        2. BTW, "LAST: Locality-Aware Sector Translation for NAND Flash Memory-Based Storage Systems" has reference to SUPERBLOCK
                            1. it further improves from SUPERBLOCK
                            2. the concept of separate sequantial writes and random writes in different log blocks
        3. key designs
            1. based on superblock. {N, K} parameter controls the N data block and K log block in a group
               the optimal {N, K} is infered from the access pattern of the target application, determined at design stage
            2. to find the {N, K} value, use the proposed analysis model

        4. related readings
            1. A SPACE-EFFICIENT FLASH TRANSLATION LAYER FOR COMPACTFLASH SYSTEMS    [2002, 989 refs]
               https://pdfs.semanticscholar.org/e0a1/546f56b68ebfcc5f7237c073d6186188f192.pdf
                1. the beginning paper that proposed the hybrid-mapping for FTL metadata
                   The key idea of the log scheme is to maintain a small number of log blocks in flash memory
                    to serve as write buffer blocks for overwrite operations

            2. A Log Buffer-Based Flash Translation Layer Using Fully-Associative Sector Translation    [2007, 778 refs]
               http://csl.skku.edu/uploads/ICE3028S11/fast-tecs07.pdf
                1. improved from "A SPACE-EFFICIENT FLASH TRANSLATION LAYER FOR COMPACTFLASH SYSTEMS"
                   In FAST, one log block can be shared by all the data blocks.
                   FAST also maintains a single log block, called sequential log block, to manipulate the sequential writes
                2. my notes are lost due to software bug. see the original paper then.

            3. LAST: Locality-Aware Sector Translation for NAND Flash Memory-Based Storage Systems    [2008, 298 refs]
               http://yourcmc.ru/wiki/images/d/d2/02-lee-last-usenix09.pdf
                1. improved from "A Log Buffer-Based Flash Translation Layer Using Fully-Associative Sector Translation"
                   LAST partitions the log buffer into two parts: random log buffer and sequential log buffer
                   The sequential log buffer consists of several sequential log blocks,
                    and one sequential log block is associated with only one data block
                   random log buffer is partitioned into hot and cold partitions.
                    By clustering the data with high temporal locality within the hot partition,
                    we can educe the merge cost of the full merge
                2. my notes are lost due to software bug. see the original paper then.

    2. compared with "NOVA: A Log-structured File System for Hybrid Volatile/Non-volatile Main Memories"    [2016, 10 refs]
       http://cseweb.ucsd.edu/~swanson/papers/FAST2016NOVA.pdf
        1. NOVA is designed for NVM as memory along with DRAM, i.e. NVMM
           F2FS is designed for SSD (SATA/PCIe/NVMe SSD)
        2. NOVA's major concern is write ordering, atomicity, consistency, because it is writting into a memory interface (with CPU and cache) of NVM
           F2FS is dealing with disk interface
        3. NOVA gives each inode its own log (F2FS has six logs at most, spearated by data/node warmness)
           NOVA use linked list as log (F2FS prefers sequential log, fallbacks to threaded log (i.e. linked-list log))
            1. so NOVA has a lot of random writes, but much better concurrency
        4. In NOVA's evulation cases, F2FS performs bad
```

__[Having Your Cake and Eating It Too: Jointly Optimal Erasure Codes for I/O, Storage, and Network-bandwidth](https://www.usenix.org/system/files/conference/fast15/fast15-paper-rashmi.pdf)__    [2015, 26 refs]

```
1. a new code based on product-matrix MSR code to minimize disk IO consumed, whie retain both storage, reliability, and network bandwidth optimality
   it can achievei 5X reducetion in IO. however, it requires parity fragment count >= data fragment count -1.

2. key findings
    1. MSR codes are optimal with respect to storage and network transfers
       But, MSR codes do not optimize with respect to I/Os
        1. reconstruction read during a lost fragment is higher, because "regenerating" needs to read, e.g. 2 block to generate 1 block then send 1 block.
           the same for reconstr

3. designs
    1. product-matrix MSR
    2. an algorithm to transform Product-Matrix-MSR codes into I/O optimal codes (termed as the PM-RBT codes)
        1. Product-Matrix-MSR is in
           "Optimal Exact-Regenerating Codes for Distributed Storage at the MSR and MBR Points via a Product-Matrix Construction"

4. references in other papers
    1. HashTag Erasure Codes: From Theory to Practice    [2016, 1 refs]
       https://arxiv.org/pdf/1609.02450.pdf
        1. "However, PM-RBT exist only for r ≥ k − 1, i.e., the codes have low rates" (r parities fragments, k data fragments, PM-RBT is the above cake eat paper)
        2. "Although several MSR code constructions exist, so far they have not been practically implemented.
           One of the main reasons for their practical abandonment is that existing MSR code constructions imply
           much bigger number of I/O operations than RS codes."
    2. Speeding up distributed storage and computing systems using codes    [2016, 0 refs]
       https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-59.pdf
        1. the cake eat paper is often mentioned together with
           "Optimal exact-regenerating codes for distributed storage at the MSR and MBR points via a product-matrix construction"
            1. they share same authors
```

__[Efficient MRC Construction with SHARDS](https://www.usenix.org/system/files/conference/fast15/fast15-paper-waldspurger.pdf)__    [2015, 15 refs]

```
1. MRC - miss-ratio curve; SHARDS - Spatially Hashed Approximate Reuse Distance Samping
   SHARDS generates MRC in a bounded 1 MB footprint, sampling rates lower than 1%,
   and exhibit approximate miss ratio errors averaging less than 0.01

2. highlights
    1. cache sizing management is important for production. effective cache sizing requires
       to use MRC. MRC is generated by reuse-distance analysis. The generation is is computational
       expensive.
    2. SHARDS is an algorithm to effectively generate the reuse-distance histogram, which is
       used to generate MRC. It works on approximate sampling, and uses spatial samping fiter
       and hash table to make it fast.
    3. these methods are useful for sophisticated cache study, e.g. ARC.
```

__[Opening the Chrysalis: On the Real Repair Performance of MSR Codes](https://www.usenix.org/system/files/conference/fast16/fast16-papers-pamies-juarez.pdf)__    [2016, 4 refs]

```
1. the implementation of MSR code is tricky. it is possible to get all the benefits, but it can also get no significant improvement.
   be careful with the increase of cpu usage. butterfly code is interesting.
    1. the introduction, background, and related works are good to read, also the discussion & conclusion part.

2. highlights
    1. implemented an MSR code in two mainstream distributed storage systems: HDFS and Ceph
        1. Ceph does online encoding while data is being introduced to the system
           Ceph applies erasure codes in a per-object basis
        2. HDFS performs encoding as a batch job
           HDFS does it on groups of objects of the same size
    2. Butterfly requires only XOR operations (galois muliply => log table lookup?)
    3. Several MSR codes constructions exist for rates smaller that 1/2 (i.e. r ≥ k) [26, 23, 29, 30]
    4. (to best knowledge) Butterfly codes [14] are the only codes that allow a two-parity erasure code (n−k = 2) over a small field (i.e. GF(2))
    5. evluation results
        1. In HDFS, MSR (Butterfly) yeilds about 2x effective repair throughput, but cpu util increases more than 2x, compared to Reed-solomon code
                    MSR gives about half the overall network trafific
                    MSR gives about half less overall disk read in GB, disk writes are almost the same with RS
        2. In Ceph, MSR (Butterfly) doesn't yeild signification improve
                    MSR gives about half the overall network traffic. but in certain case, MSR gives however 30% traffic than RS.
                    MSR gives about half less overall disk read in GB, disk writes are almost the same with RS
    6. communication vectorization
        1. what is it? it seems not clearly explained in paper.
```

__[Write Once, Get 50% Free: Saving SSD Erase Costs Using WOM Codes](https://www.usenix.org/system/files/conference/fast15/fast15-paper-yadgar.pdf)__    [2015, 16 refs]

```
1. WOM (write-once memory) code allows we write new page on flash without erasure operation.
   the basic idea is the bit value of each cell can only increase, not decrease, unless the entire block is erased.
   the approach is promising, as erasure is the major flash performance and lifespan killer.
   but these codes inflate the physically stored data by at least 29% (theory lower bound).

2. this paper propose "Reusable SSD", which reduces erasures by 33%, resulting in a 15% lifetime extension,
   and an overall reduction of up to 35% in I/O response time
```

__[The Devil Is in the Details: Implementing Flash Page Reuse with WOM Codes](https://www.usenix.org/system/files/conference/fast16/fast16-papers-margaglia.pdf)__    [2016, 4 refs]

```
1. the first end-to-end hardware to software implementation of a general-purpose FTL on MLC flash by WOM codes
   WOM - Flash page reuse

2. conclusions
    1. page reuse in MLC flash is possible, but can utilize only half of the pages and only if some of its capacity has been reserved in advance
    2. While reprogramming is safe for at least 40% of the lifetime of the chips we examined, it incurs additional long-term wear on their blocks
    3. even with an impressive 20% reduction in erasures, the increase in lifetime strongly depends on chip physical characteristics, and is fairly modest
    4. A reduction in erasures does not necessarily translate to a reduction in I/O response time or energy consumption
       These are determined by the overall amount of data moved during garbage collections, which strongly depends on the overprovisioning
    5. The reduction in physical flash page writes is limited by the storage overhead of WOM encoded data, and is mainly constrained by the limitation of reusing only half of the block’s pages
    6. This study exposed a considerable gap between theory and workable implementation
```

__[FlashGraph: Processing Billion-Node Graphs on an Array of Commodity SSDs](https://www.usenix.org/system/files/conference/fast15/fast15-paper-zheng.pdf)__    [2015, 36 refs]

```
1. graph engine built atop SAFS, for single multi-core machine attached with SSDs
   it has comparable performance (0.5x-0.8x) with in-memory graph engines
    1. good to read because this paper is concise and in detail to undertand what graph engine does

2. background
    1. Graph analysis performs many random reads and writes
    2. these workloads are typically performed in memory
    3. Graph processing engines have converged on a design that
        1. stores graph partitions in the aggregate memory of a cluster
        2. encodes algorithms as parallel programs against the vertices of the graph
        3. uses either distributed shared memory or message passing to communicate
       Recent work has turned back to processing graphs from disk drives on a single machine
        1. to achieve scalability without excessive hardware
    4. SAFS (set-associative file system)
        1. it refactors I/O scheduling, data placement, and data caching for the extreme parallelism of modern NUMA multiprocessors
        2. The lightweight SAFS cache enables FlashGraph to adapt to graph applications with different cache hit rates
        3. it has a scalable, lightweight page cache that organizes pages in a hashtable and places multiple pages in a hashtable slot
        4. Upon completion of a request, the associated user task executes inside the filesystem, accessing data in the page cache directly.
           Therefore, there is no memory allocation and copy for asynchronous I/O

3. highlights
    1. FlashGraph is a semi-external memory (memory + SSD) graph engine.
       It is built on top of a user-space SSD file system, SAFS.
       it works on a multicore server attached with commodity SSDs (compared to the traditional machine cluster setup)
    2. to optimize performance
        0. FlashGraph is built atop SAFS (same author), and leverage it heavily
        1. FlashGraph stores vertex state in memory and edge lists on SSDs
        2. It hides latency by overlapping computation with I/O
        3. To reduce IO, FlashGraph only accesses edge lists requested by applications from SSDs
           it conservatively merges I/O requests
           it uses compact external-memory data structures
        4. FlashGraph exposes a general and flexible vertex-centric programming interface
           which can express a wide variety of graph algorithms and their optimizations
        5. even though SSD, still perform sequential IO when never possible (from FTL design, this eases GC merge operations)
    3. execution model
        1. partition the graph and assign a worker thread to each
        2. each worker thread maintains a queue of active vertices
        3. the scheduler manages the execution order active vertices
           guarantees only a fixed number of running vertics in a thread
    4. programming model
        1. FlashGraph adopts the vertex-centric programming model commonly used by other graph engines such as Pregel [20] and PowerGraph [11]
        2. in this model, each vertex maintains vertex state and performs user-defined tasks based on its own state
        3. A vertex affects the state of others by sending messages to them as well as activating them
        4. FlashGraph further allow a vertex to read the edge list of any vertex from SSDs
        5. The rest of FlashGraph’s programming interface is event-driven to overlap computation and I/O,
           and receive notifications from the graph engine and other vertices
    5. in-memory data representation
        1. each vertex in the index uses slightly more than 1.25 bytes in an undirected graph and slightly more than 2.5 bytes in a directed graph
        2. we store the degree of large vertices (≥ 255) in a hash table
           Most realworld graphs follow the power-law distribution in vertex degree, so there are only a small number of vertices in the hash table
    6. on-SSD (external-memory) data representation
        1. the edge list of all vertex are stored as contiguous array on disk
           one edge list may be less than an page size. edge lists are compacted into pages with no holes.
        2. the graph index, which is a vertex list, whose each vertex links to its on-disk edge list, is maintained in memory
    7. edge list access on SSD
        0. Graph algorithms exhibit varying I/O access patterns
           The most prominent is that each vertex accesses only its own edge list
        1. FlashGraph globally sorts and merges I/O requests issued by all active state vertices within an iteration
        2.  the minimum I/O block size issued by FlashGraph is one flash page (4KB)
        3. The more requests FlashGraph observes, the more likely it is to merge them and generate cache hits
    8. graph partitioning
        1. When a thread processes vertices in its own partition, all memory accesses to the vertex state are localized to the processor
        2. With range partitioning, the edge lists of most vertices in the same partition are located adjacently on SSDs
    9. load balancing
        1. once a thread finishes all active vertices in its partition, it steals active vertices from other threads
        2. FlashGraph does not execute computation on a vertex simultaneously in multiple threads to avoid concurrent data access
        3. if only a few large vertices dominate the computation of the applications,
           vertical partitioning breaks these large vertices into parts
           so that FlashGraph’s load balancer can move computation of vertex parts to multiple threads
    10. evaluation
        1. what algorithms are selected?
            Breadth-first search (BFS), Betweenness centrality (BC), PageRank (PR),
            Weakly connected components (WCC), Triangle counting (TC), Scan statistics (SS)
        2. what datasets are selected?
            the Twitter graph, the subdomain Web graph

4. questions
    1. do we need to precompute the data layout of edge list on SSD? for example, who should be adjacent to whom?
       this has big impact on edge list access peroformance

5. referenced in other papers
    1. GridGraph: Large-Scale Graph Processing on a Single Machine Using 2-Level Hierarchical Partitioning    [2015, 29 refs]
       https://www.usenix.org/system/files/conference/atc15/atc15-paper-zhu.pdf
        1. "FlashGraph [34] implements a semiexternal memory graph engine which stores vertex states in memory and adjacency lists on SSDs,
            and presents impressive performance. Yet it lacks the ability to process extremely large graphs of which vertices can not be fit into memory"
    2. Active Community Detection in Massive Graphs    [2014, 4 refs]
       https://arxiv.org/pdf/1412.8576.pdf
        1. "In order to scale, FlashGraph requires the size of vertex state to be a small constant"
    3. ALGORITHMIC TECHNIQUES FOR THE MICRON AUTOMATA PROCESSOR    [2015, 5 refs]
       https://smartech.gatech.edu/bitstream/handle/1853/53845/ROY-DISSERTATION-2015.pdf
        1. "As a remedy, some recent research [77] have investigated the use of flash-based external memory coupled with smart middle-ware
            to provide near in-memory performance even for graph-applications which require random I/O access"
    4. An SSD-based eigensolver for spectral analysis on billion-node graphs    [2016, 3 refs]
       https://arxiv.org/pdf/1602.01421.pdf
        1. "This design prevents FlashGraph from performing some optimizations for sparse matrix multiplication as shown in this paper"
    5. Scaling Iterative Graph Computations with GraphMap    [2015, 5 refs]
       https://pdfs.semanticscholar.org/80d8/fe9fc7b965e1f6289677922a81cd03c54dd5.pdf
        1. "TurboGraph [9] and FlashGraph [30], based on SSDs, improve the performance by exploiting I/O parallelism and overlapping computations with I/O"
    6. Semi-External Memory Sparse Matrix Multiplication for Billion-Node Graphs    [2016, 1 refs]
       https://arxiv.org/pdf/1602.02864.pdf
        1. same author.
        2. "FlashGraph [12] adopted the concept and performs graph algorithms with vertex state in memory and edge lists on SSDs.
            This work extends the semi-external memory concept to matrix operations"
```

__[BTrDB: Optimizing Storage System Design for Timeseries Processing](https://www.usenix.org/system/files/conference/fast16/fast16-papers-andersen.pdf)__    [2016, 4 refs]

```
1. store time-series as a tree, which is partitioned by time, has fixed depth thus a lot of holes and fixed time range,
   copy-on-write and each version corresponds to a new root. each link in the tree is annotated with version. each internal
   nodes holds statistics summaries of its children

2. BtrDB achieves 53 million inserts and 119 million queries on a 4-node cluster, compared to most opensource systems such
   as OpenTSDB, KairosDB, Druid acheive less than 1 million per second (but they are designed for complex multi-dimensional data).
   BtrDB acheieves 2.9x compression ration.

3. the target use of BTrDB is extremely high sample rate, simple data structure, extremely high time precision
   BTrDB is designed to be simple and fast, with only 4709-line of GO code.
```

__[Design Tradeoffs for Data Deduplication Performance in Backup Workloads](http://stlab.wnlo.hust.edu.cn/csyhua/hua-fast2015.pdf)__    [2015, 17 refs]

```
1. to explore design tradeoffs in dedup, each combination of design parameters is seen as a N-dimensional point.
   the authors implement a general-purpose deduplication framework, DeFrame, to evaluate it.
    1. it is a useful paper to understand the taxonomy dedup systems

2. key findings
    1. While the fragmentation results in an ever-increasing lookup overhead in EDPL, EDLL achieves sustained performance.
       The sampling optimization performs an efficient tradeoff in EDLL
    2. In NDPL, the uniform sampling is better than the random sampling. The fingerprint cache has minimal impacts on deduplication ratio.
    3. The Base procedure underperforms in NDLL if self-reference is common.
       Reading a single most similar segment is insufficient due to self-reference and segment boundary changes.
    4. If self-reference is rare, the Base procedure is sufficient for a high deduplication ratio.
    5. If self-reference is common, the similarity detection is required. The segmenting prefetching is a great complement to Top-k
    6. The rewriting algorithm helps EDPL to achieve sustained backup performance.
       With a rewriting algorithm, EDPL is better due to its higher deduplication ratio than other index schemes.
    7. Without rewriting, the forward assembly area is recommended; but with an efficient rewriting algorithm, the optimal cache is better
    8. Although near-exact deduplication reduces the DRAM cost, it cannot reduce the total storage cost.
```

__[Reducing Solid-State Storage Device Write Stress through Opportunistic In-place Delta Compression](https://www.usenix.org/node/194421)__    [2016, 5 refs]

```
1. The paper works at FTL/SSD controler (firmware) level. It uses intra-page partial programming to improve delta compression,
   by packing deltas into the same page, while convential pratices put delta into other pages.
   evaluation shows, the programmed flash memory pages can be reduced to 0.2x-0.9x

2. highlights
    1. SSD controllers dynamically configure a small portion of MLC/TLC flash memory blocks to operate in SLC mode,
       to serve as write buffer/cache and/or store hot data. delta comnpression is appealing on those blocks, because
       reducing their write stress can directly reduce the flash memory wear-out.
    2. Although per-sector atomic write is essential in hard disk drives, per-page atomic write is not absolutely necessary in NAND flash
       experiments with 20nm MLC NAND flash memory chips, we observed that SLC-mode pages can support partial programming
    3. we propose a solution, the key idea is to
        1. When a 4kB sector is being written the first time, we always try to compress it before writing to an SLC-mode flash memory page
        2. The use of per-sector lossless compression leaves some memory cells unused in the flash memory page
        3. Taking advantage of the per-page partial-programming support of SLC-mode flash memory,
           we can directly use those unused memory cells to store subsequent deltas later on
```

__[OrderMergeDedup: Efficient, Failure-Consistent Deduplication on Flash](https://www.usenix.org/node/194449)__    [2016, 4 refs]

```
1. block-level dedup, fixed-sized chunking. built as linux kernel dm target.
   this solution uses soft-update similar metadata consistency approach; the dedup semantics allows resolve cyclic dependency issue.
    this approach brings reduces metadata IO on flash.
   this solution delays metadata IO, like the linux anticipatory scheduler, to benifit from metadata IO merging
    it can be used with soft-updates which delay metadata IOs.        
   Results show OrderMergeDedup realizes about 20% write reduction （the benchmark has about 30% duplicated content）,
    in a few cases to 50% more (the benchmark has about 60%-70% duplicated content)
    dmdedup performs really bad (and even increases the resulting content by 11x), it's not a good comparator
    the latency overheads is very small, less than 5%

2. highlights
    1. With failure-consistent I/O ordering and anticipatory merging, we name our deduplication approach OrderMergeDedup
    2. comparing metadata failure consistency techniques with atomic IO
        1. In journaling, an atomic I/O operation is recorded in a redo log before writing to the file system.
           A failure after a partial write can be recovered at system restart by running the redo log
        2. In shadowing, writes to existing files are handled in a copy-on-write fashion to temporary shadow blocks.
           The final commit is realized through one atomic I/O write to a file index block that points to updated shadow data/index blocks.
           Index blocks (potentially at multiple hierarchy levels) must be re-written to create a complete shadow
            1. Both journaling and shadowing require additional write I/O to achieve failure consistency of durable data
        3. The soft updates approach [6] carefully orders writes in file system operations such that
           any mid-operation failure always leaves the file system structure in a consistent state (except for possible space leaking on temporarily written blocks)
           While it requires no I/O overhead during normal operations, rollbacks may be necessary to resolve cyclic dependencies in the block commit order
            1. Seltzer et al. [18] showed that such rollbacks sometimes led to poor soft updates performance on the UNIX Fast File System
                1. Due to relatively simple semantics of a deduplicated storage (compared to a file system),
                   we show that a careful design of all deduplication I/O paths can efficiently resolve possible dependency cycles
                    1. We resolve this issue by delaying the non-critical metadata updates involved in the cyclic dependencies
            2. the ordering constraints (like soft-update's ordering constraint rules) are listed in 2.1
                1. For reference counters, the only possibly resulted inconsistency is higher-than-actual reference counters
                   it may produce garbage (that can be reclaimed asynchronously)
            3. question
                1. soft-update delay metadata IO, although it ensures failure consistency, but it doesn't guaratnee metadata durability, because it's delayed
                   how does OrderMergeDedup solve this?
    3. substantial I/O cost reduction may result from the merging of multiple metadata writes that fall into the same metadata block
        1. We may enhance the opportunities of metadata I/O merging by delaying metadata update I/O operations (Similar to Linux anticipatory scheduler)
        2. the opportunities of such delay are
            1. Weak persistence
            2. Non-critical I/O delay and merging
            3. Anticipatory I/O delay and merging
        3. In our implementation, we delay the non-critical metadata writes for 30 seconds after their failure-consistent dependencies are cleared
            1. 30 seconds
```

__[Converged Storage Technology](https://www.usenix.org/conference/fast16/technical-sessions/presentation/converged-storage-technology)__ (Huawei)    [2016]

```
alternative link: http://www.snia.org/sites/default/files/tutorials/FAST2016/FAST2016-LiangMing_Converged_Storage_Technology-Final.pdf

1. the Key Value Flash (KVF) architecture
    1. think about the "Isotope: Transactional Isolation for Block Storage" by google, KV flash may be something good

2. userspace network and IO stack (DPDK, SPDK)
   distributed hash table
```

__[Privacy vs. Data Protection: The Impact of EU Data Protection Legislation](https://www.usenix.org/conference/fast16/technical-sessions/presentation/rivera)__    [2016]

```
alternative link: http://www.snia.org/sites/default/files/DSS-Summit-2015/presentations/ThomasRivera_Privacy_vs_Data_Protection-Impact_EU_Legislation_v7.pdf

1. EU data protection legislation
    1. data breach includes data destruction
    2. the right to be forgotten
    3. the U.S. practice of breach notifications
```

__[Practical Online Cache Analysis and Optimization](https://www.usenix.org/conference/fast16/technical-sessions/presentation/waldspurger)__    [2016]

```
alternative link: http://www.snia.org/sites/default/files/tutorials/CarlWaldspurger_Practical_Online_Cache_Analysis.pdf

1. same author, Carl Waldspurger, with "Efficient MRC Construction with SHARDS"
   good research point to model and optimize cache management. if it works, this can be very useful

2. to analyze storage caches using lightweighted, continuous-updated miss ratio curves (MRCs)
    1. reuse distance

3. several examples

4. https://www.usenix.org/conference/fast16/technical-sessions/presentation/ault
```

__[Utilizing VDBench to Perform IDC AFA Testing](https://www.usenix.org/conference/fast16/technical-sessions/presentation/ault)__ (Oracle)    [2016]

```
alternative link: http://www.snia.org/sites/default/orig/FMS2015/MichaelAult_Using_Oracle_VDBench_%20Implement_IDC.pdf

1. AFA - All-flash-array. It is not SSD. AFA is a solid state storage array connected by redudant network protocols

2. VDBench - simulate multi-host load scenarios to benchmark AFA

3. difference between AFA and HDD
    1. flash-based array performance will differ significantly from FOB (fresh out of box) and after firt write on every flash cell
    2. read/write asymmetries: flash needs to erase before overwrite
    3. endurance: after a defined number of P/E cycles, flash will become readonly and eventually inoperable
    4. the mixed virtual workloads in 3rd platform computing are very different than traditioinal client/server workloads
        1. a variety of read/write ratios
        2. wide distribution of block sizes
        3. be skewed toward random IO
        4. have a high percentage of reducible data
```

__[Object Drives: A New Architectural Partitioning](https://www.usenix.org/conference/fast16/technical-sessions/presentation/carlson)__    [2016]

```
alternative link: http://www.snia.org/sites/default/orig/FMS2015/MarkCarlson_Object_Drives_V9.pdf

1. Ceph OSD node, if compared to an storage enclosures, the enclosure is a full computer node. power and space concerns.
   object drive allows storage to scale up and down by single drive increments
    1. the key-value example is Kinetic
       the higher-level example is CDMI

2. good and interesting idea.
   maybe after years, distributed storage will be standardized, and data nodes become replaciable drives
    1. think about "Converged Storage Technology"'s KVF,
       and "Isotope: Transactional Isolation for Block Storage" where we can put transaction support to lower layer
```

__[Towards Accurate and Fast Evaluation of Multi-Stage Log-structured Designs](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lim)__    [2016, 1 refs]

```
1. proposed new analytical primitives to estimate LSM-tree write amplification. it's more accurate than traditional worst-case analysis
   it can be used to find optimized system parameters, as evaluated, decrease LevelDB's insert cost by up to 9.4% - 26.2%

2. highlights
    1. Unique(p) := expected unique keys in p requests
       Unique^−1(u) := to accumulate to u unique keys, how many requests we need. then we know when memtable should be flushed
       Merge(u, v) := Unique(Unique^−1(u) + Unique^−1(v)), it's the size of the merged table
       DInterval(l) := expected interval between compaction of the same key in level-l
       then, we can model the write amplication of LSM-tree
    2. implemented a system parameter optimizer based on the analytical model

3. questions
    1. fX (k) have no spatial locality. but in reality this is not true
```

__[sRoute: Treating the Storage Stack Like a Network](https://www.usenix.org/conference/fast16/technical-sessions/presentation/stefanovici)__ (coop with microsoft research)    [2016, 2 refs]

```
1. route IO in (distributed) storage stack with a centralized control plane. built atop IOFlow (reminds me Openflow).
   it works with unmodified applications and VMs. it's like SDN in storage stack, or storage service chaining
    1. think of "Object Drives: A New Architectural Partitioning", when distributed storage stack can be standarized, these things may be useful

2. highlights
    1. example applications
        1. a load balancing service selectively routes write requests to go to less-loaded servers,
           while ensuring read requests are always routed to the latest version of the data (§5.1).
        2. a control application provides per-tenant throughput versus latency tradeoffs for replication update propagation,
           by using IO routing to set a tenant’s IO read- and writeset at runtime (§5.2).
        3. a control application can route requests to per-tenant caches to maintain cache isolation (§5.3)
    2. Consistent rule updates
        1. Per-IO consistency: each IO flows either an old set or a new set of rules, not the mixed
        2. Per-flow consistency
    3. implementation
        1. An sSwitch is implemented partly in kernel-level and partly in user-level
        2. Routing within a server’s IO stack. Our implementation makes use of the filter driver architecture in Windows
        3. Routing across remote servers. By TCP or RDMA (default) through SMB filesystem protocol
    4. tail latency control
       1. the control application attempts to balance queue sizes
```

__[CacheDedup: In-line Deduplication for Flash Caching](https://www.usenix.org/conference/fast16/technical-sessions/presentation/li-wenji)__    [2016, 2 refs]

```
1. flash is often used as cache. CacheDedup integrates fixed-size dedup to the flash cache, and designed D-LRU and D-ARC replacement algorithms
   it needs < 4% space of the flash cache to store dedup metadata. as evaluated by real world trace,
   CacheDedup achieves up to 20% reduction in miss ratio, 51% in latency, and 89% reduction in writes
    1. VMware vSAN 6.5 uses server-side PCIe SSD to as cache, it does dedup in the cache
    2. good to read as a typical dedup flash cache implementation

2. highlights
    1. cache replacement algorithms typically focus on maximizing the hit ratio.
       but for flash, CacheDedup needs to find the sweetspot, between keeping hit ratios close to the optimum and lowering the number of write operations
    2. metadata cache
        1. source addr index: source block address => fingerprint
           fingerprint store: fingerprint => cache block address
        2. source block addresses maps to fingerprints, this includes both current block and evicted history blocks in cache
           so, when evicted data are brought back to cache again, all pointing source block addresses are resurrected
        3. CacheDedup synchronously commits both the metadata and data to cache device
            1. pack metadata along with data blocks in the cache?
            2. it can also checkpoint metadata cache to flash, for faster startup
    3. deuplication-aware cache replacement algorithms
        1. D-LRU
            1. insert into matadata cache by LRU
               insert into flash cache by LRU
        2. D-ARC
            1. here the explanation of ARC is good
            2. use ARC to manage metadata cache, it cache data needs eviction, on select data blocks that have no mapping in T1UT2
               also, D-ARC allow size of T1+T2 to grow to C+X, to store X more source addresses whose data duplicates with others
               also, D-ARC uses an additional B3, to save source addresses evicited from B1 and B2. B3 uses the space left available by T1 and T2 to C+X
        3. as evaluated, D-LRU and D-ARC can have 20% less miss ratio than LRU and ARC
           and D-ARC has much less ratio than D-LRU in some test cases
    4. overhead
        1. fingerprinting overhead is considerable, but it can be overalpped with IOs

3. questions
    1. datadomain leverage the locality of backup workload to improve dedup
       does flash cache has similar characteristics that we can leverage?
    2. why not use content-based addresing? 
        1. but if content-based addressing, the cache space utilization is low, because we cannot determine which data block is put where
    3. what is the block size? this is important to metadata size
```

__[WiscKey: Separating Keys from Values in SSD-conscious Storage](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lu)__    [2016, 3 refs]

```
1. WiscKey is highly SSD optimized LSM-tree-based Key-value store, which separates keys from values to minimize I/O amplification2. 
   WiscKey is 2.5×–111× faster than LevelDB for loading a database and 1.6×–14× faster for random lookups.
   the write-amplification is 4x-14x lower. WiscKey outperforms LevelDB and RocksDB in all six YCSB workloads; but in some workloads, RocksDB is close.
   however, WiscKey can use 1.4x space than LevelDB when value is 4x size of key, but WiscKey use 0.75x space when value is 16Kx size of key
   however, WiscKey uses about 1.3x CPU than LevelDB, and 3x especially in range query
    1. good reading as to how to optimize LSM-tree for SSD

2. key findings
    1. LSM-tree, as a result, the same data is read and written multiple times throughout its life
       this is the IO amplification for SSD. in certain case, it can reach 50x or higher
        1. it looks like several papers are all attacking LSM's this problem on SSD
    2. when considering key-value storage system design, we believe the following three differences are of paramount importance
        1. the difference between random and sequential performance is not nearly as large as with HDDs;
           thus, an LSM-tree that performs a large number of sequential I/Os to reduce later random I/Os may be wasting bandwidth needlessly
        2. SSDs have a large degree of internal parallelism;
           an LSM built atop an SSD must be carefully designed to harness said parallelism
        3. SSDs can wear out through repeated writes;
           the high write amplification in LSMtrees can significantly reduce device lifetime

3. backgrounds
    1. LevelDB ensures that all files in a particular level, except L0, do not overlap in their keyranges
    2. many SSD-optimized key-value stores are based on LSM-trees [25, 50, 53, 54]
    3. when random reads are issued concurrently in an SSD, the aggregate throughput can match sequential throughput for some workloads

4. key designs
    1. central idea behind WiscKey
        1. only keys are kept sorted in the LSM-tree, while values are stored separately in a log
            1. challanges
                1. range query (scan) performance may be affected because values are not stored in sorted order
                    1. WiscKey solves this challenge by using the abundant internal parallelism of SSD devices
                2. WiscKey needs garbage collection to reclaim the free space used by invalid values
                    1. WiscKey proposes an online and lightweight garbage collector which only involves sequential I/Os and impacts the foreground workload minimally
                3. separating keys and values makes crash consistency challenging
                    1. WiscKey leverages an interesting property in modern filesystems, that appends never result in garbage data on a crash
    2. WiscKey includes four critical ideas
        1. WiscKey separates keys from values, keeping only keys in the LSM-tree and the values in a separate log file
        2. to deal with unsorted values, WiscKey uses the parallel random-read characteristic of SSD devices
        3. WiscKey utilizes unique crash-consistency and garbage collection techniques to efficiently manage the value log
        4. WiscKey optimizes performance by removing the LSM-tree log without sacrificing consistency, thus reducing system-call overhead from small writes
    3. garbage collection
        1. while storing values in the vLog, we also store the corresponding key along with the value
        2. when GC, it reads values from tail, check which are valid, then append them to head.
           finally, the tail is rolled forward
        3. To avoid losing any data if a crash happens, WiscKey has to make sure that the newly appended valid values
           and the new tail are persistent on the device before actually freeing space
    4. Crash Consistency
        1. values are sequentailly appended. if X lost, everything after X is lost
        2. if a key's associated value is lost, the key will be deleted
    5. removing the log of LSM-tree
        1. because vLog, where values are stored, contains keys too (see garbage collection)
           so, the we don't need the LSM-tree log any more
    6. implementations
        1. WiscKey is based on LevelDB 1.18
        2. use fallocate() to punch hole in a file for efficiently garbage collect the free space
           punching a hole in a file can free the physical space allocated
```

__[Efficient and Available In-memory KV-Store with Hybrid Erasure Coding and Replication](https://www.usenix.org/conference/fast16/technical-sessions/presentation/zhang-heng)__ (Haibo Chen)   [2016, 2 refs]

```
1. Cocytus, the first in-memory KV-store that adopt erasure coding (to same replicated memory size)
   built atop memcached, use online EC for data and primary-backup (no EC) for metadata
   evaluation shows about 20%-40% memory is saved compared to using only primary-backup
    1. can be read as an example to build sophisticated in-memory store atop memcached

2. highlights
    1. challanges
        1. an update may result in a number of small updates (we only need to update modified code words but not the entire code block)
            1. EC the data only, leave metadata and keys to be replicated by the primary-backup
    2. sharding
        1. Cocytus uses sharding to partition key/value tuples into different groups
            1. A coding group handles a key shard, which is further divided into P partitions in the group
            2. Each partition is handled by a particular data process, which performs coding at the level of virtual address spaces
               This makes the coding operation neutral to the changes of value sizes of a KV pair as long as the address space of a data process does not change
        2. for data layout, which is interleaved, to balance the load, to benefit the recovery
            1. see Figure 3
    3. consistency
        1. ack user after online EC and replication finishes
            1. one way to implement an atomic broadcast is 2PC, but it is not used
            2. Cocytus uses a piggybacking approach
                1. each request is assigned with an xid. when done, the data process update the latest stable xid
                   when sending a new parity update, it brings the latest stable xid with it
                   when parity process receives the piggybacked request, it mark all operations that have smaller xid as READY
    4. implementation
        1. determinstic allocator
            1. Each data process maintains a memory region for data with the mmap syscall 
            2. Cocytus uses two AVL trees, of which one records the free space and the other records the allocated space
            3. The trees manage the memory pieces in a way similar to the buddy memory allocation:
                large blocks might be split into small ones during alloc operations
                and consecutive pieces are merged into a larger one during free operations
            4. To make the splitting and merging fast, all memory blocks are linked by a list according to the address
```

__[Application-Managed Flash](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lee)__    [2016, 3 refs]

```
1. remove the FTL, let application manage the flash directly.
   AMF (application-managed flash) includes hardware device, based on an open FPGA-based flash platform.
   it exposes a block IO interface which requires erase before overwrite. it still has a simple FTL, the AFTL.
   evaluation shows, however, there is no significant performance improvement compared to EXT4 + normal SSD;
   except only for database, transactions/sec improves by about 50% (but is it because of AMF? or the log-structured ALFS absorbs random writes). 
    1. reminds me the open-channel SSD, and Baidu's "An Efficient Design and Implementation of LSM-Tree based Key-Value Store on Open-Channel SSD"
    2. there are always people who want to remove the FTL from SSD
       can some startup vendor sell these AMF (application-managed flash)?
    3. good to read, because the evaluation shows that open-channel SSD may not be a good approach

2. highlights
    1. in AMF, the device responsibility is reduced to
        1. provide error-free storage access
        2. efficient parallelism
        3. keep track of bad blocks and wear-leveling
            1. because they are simpler to implement at device-level
            2. it is done by using the segment-map table
    2. AFTL (AMF's FTL) design
        1. AFTL has a mapping table from logical (segment, block) to physical (segment, block) (called the segment-map table)
            1. the metadata size is the same with a block-level mapping table
            2. Table 2 lists the metadata size of FTL and AFTL
                1. 512GB SSD: block-level:4MB, hybrid-level:96MB, page-level:512MB, AFTL:4MB
                   1TB SSD: block-level:8MB, hybrid-level:186MB, page-level:1GB, AFTL:8MB
        2. AFTL does not need to run address remapping to avoid in-place updates
           AFTL does not need to perform garbage collection
        3. there are multiple channels, which can be writen in parallel
           each channel has its IO queue
    3. there is no reference to open-channel SSD,
       nor Baidu's "An Efficient Design and Implementation of LSM-Tree based Key-Value Store on Open-Channel SSD"
```

__[Mitigating Sync Amplification for Copy-on-write Virtual Disk](https://www.usenix.org/conference/fast16/technical-sessions/presentation/chen-qingshu)__ (Haibo Chen)    [2016, 2 refs]

```
1. use journal to replace the sync-per-metadata-update in CoW virtual disk image (e.g. qcow2)
   use preallocation to avoid host filesystem's extra metadata sync flush (because disk image size grows)
   evaluation shows about 40% performance speedup in many cases, but almost no change in other cases
    1. good to read, because it gains so much performance on qcow2, even though adding a journal is not a very innovative method
       it looks like people just didn't find that we can improve CoW virtual disk this way.

2. key findings
    1. qcow2, the copy-on-write virtual disk format is convenient for VM fork and deployment
       but the dramastic increase of disk sync operations (3x+) slowdown IO intensive workloads such as varmail
    2. this is because, CoW virtual disk image (e.g. qcow2) contains metadata, such as virtual to physical block number mapping
       the manager frequently use fdatasync to ensure the metadata persistency and ordering
    3. Figure 4 shows how the original qcow2 vs with journaling
        1. original: update ref table -> flush -> update L2 table -> flush -> update L1 table -> flush -> update data -> flush
        2. with journal: data -> journal -> commit block -> flush

3. highlights
    1. Per virtual disk journaling
        1. Qcow2 requires multiple syncs to enforce ordering, which is too strong according to our observation
        2. To address this issue, we implement an internal journal for each virtual disk,
           where metadata/data updates are first logged in a transaction,
           which needs only one sync operation to put them to disk consistently
    2. dual-mode journaling
        1. the above method, however, requires data to be written twice
        2. dual-mode journaling which monitors each modification to the virtual disk
           and only logs metadata (i.e., reference table, lookup table) when there is no data overwriting
    3. Adaptive preallocation
        1. allocates extra blocks for a virtual disk image when the disk is growing
        2. This saves the image manager from requesting the host file system for more free blocks,
           and thus avoids extra flush operations

4. related readings
    1. Rethink the Sync    [2008, 124 refs]
       https://www.usenix.org/legacy/event/osdi06/tech/nightingale/nightingale.pdf
        1. externally synchronous IO: a middle man does synchronous IO to the underlying filesystem, while the app can just do async IO to the middle man
           the overall semantics is still, user is doing a synchronous IO to the underlying filesystem. but app is released from the synchronous burden.
            1. for outline, see Figure 1
            2. the ack->durability may not be preserved, but ordering can be achieved in this way
```
