---
layout: post
title: "Storage College Course Study"
tagline : "Storage College Course Study"
description: "Storage College Course Study"
category: "storage"
tags: [storage, filesystem, cloud]
---
{% include JB/setup %}

I picked several the most helpful college storage couses I think. To grasp a solid foundation really helps understand new papers and think efficiently. Here's the notes I took

### [University of California, Santa Cruz - Prof. Scott A. Brandt - Advanced Topics in Computer Systems: Storage Systems](https://users.soe.ucsc.edu/~sbrandt/290S/)

The paper readings are basically orangized from history to modern, from basic foundamentals to complete filesystem design. It is helpful to understand the many historical motivations reflexed in today's storage designs. The instructor requires to answer below questions while reading a paper

  1. What is the problem the authors are trying to solve?
  2. What other approaches or solutions existed at the time that this work was done?
  3. What was wrong with the other approaches or solutions?
  4. What is the authors' approach or solution?
  5. Why is it better than the other approaches or solutions?
  6. How does it perform?
  7. Why is this work important?
  8. 3+ comments/questions

**[Computer Architecture: A Quantitative Approach](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.115.1881&rep=rep1&type=pdf) Chapter 6** \[4th-edition in 2007, 14823 refs\]

```
1. this is a pretty good and solid book, the problem is that it is too old
2. the case study part is good. correct, very good. if a student has done all of them, he/she is expert.
   mark
```

**[An Introduction to Disk Drive Modelling](http://pages.cs.wisc.edu/~remzi/Classes/838/Fall2001/Papers/diskmodel-computer94.pdf)** \[1994, 1063 refs\]

```
1. good paper. spinning disk internally is complex, a lot designs and trade-offs
   although today the paper becomes old and SSD is taking over. the paper is good
2. it can be seen that this course provides a pretty solid foundation for their students
3. they did a very comprehensive disk simulator, 5800+ lines of commented C++ code
```

**[A Fast File System for UNIX](https://cs162.eecs.berkeley.edu/static/readings/FFS84.pdf)** \[1984, 1195 refs\]

```
1. use bitmap instead of linkedlist to allocated available blocks
   increase block size from 1024-byte to 4096-byte,
       and use smaller fragments to store small files more efficiently
   allocate sequential blocks for a file, or at least rotationally closest blocks
2. single fileysystem block is divided into fragments, to reduce space waste
   each file system block can be broken optionally into 2, 4, or 8 fragments, each of which is addressable
   bitmap is fragment level
3. referenced in
   http://pages.cs.wisc.edu/~swift/classes/cs736-fa06/papers/lfs.pdf
   http://www.ppgia.pucpr.br/~s.loest/bibliografia/osdi2002.pdf
   https://en.wikipedia.org/wiki/Unix_File_System
4. today, filesystems widely use extents
   this paper is pretty old though
```

**[MDS Functionality Analysis](https://users.soe.ucsc.edu/~sbrandt/290S/xue.pdf)** \[2001, 0 refs\]

```
1. the professor's student's work
2. use object store as the filesystem storage engine, need to address
    1. access control
    2. cache coherency
    3. scalability
    4. versioning
    5. data availability
    6. metadata allocation
    7. sharing mechanism
    8. encryption
3. the topics are very attractive, but the contents are too water-ed
```

**[A Trace-Driven Analysis of the UNIX 4.2 BSD File System](https://users.soe.ucsc.edu/~sbrandt/290S/trace.pdf)** \[1985, 748 refs\]

```
1. good paper, it answers to the foundamental accesss pattern problem
    1. How much network bandwidth is needed to support a diskless workstation?
    2. What are typical file access patterns (and what protocols will support those patterns best)?
    3. How should disk block caches be organized and managed?
2. the key patterns
    1. individual users make only occasional (though bursty) use of the file system, and they need very little bandwidth on average (only a few hundred bytes per second per active user)
    2. files are usually open only a short time, and they tend to be read or written sequentially in their entirety; non-sequential access is rare
    3. most of the files that are accessed are short; and most new files have short lifetimes (only a few minutes)
    4. most files accessed are short, though long files account for a large fraction of the data transferred; accesses tend to be highly sequential; and file system activity is bursty. 
3. the key patterns with data
    1. On average, about 300-600 bytes/second of file data are read or written by each active user.
    2. About 70% of all file accesses are whole-file transfers, and about 50% of all bytes are transferred in wholefile transfers.
    3. 75% of all files are open less than .5 second, and 90% are open less than 10 seconds.
    4. About 20-30% of all newly-written information is deleted within 30 seconds, and about 50% is deleted within 5 minutes.
    5. A 4-Mbyte cache of disk blocks eliminates between 65% and 90% of all disk accesses for file data (depending on the write policy).
    6. For a 400-kbyte disk cache, a block size of 8 kbytes results in the fewest number of disk accesses for filedata. For a 4-Mbyte cache, a 16-kbyte block size is optimal. 
4. how to collect data and meaure, and to avoid the large volume of metrics
    1. log file-level system calls: open/create, close, seek, unlink, truncate, execve
       rather than read/writes and accurate time boundary
       use the time interval between successive trace events to identify data transfer time
    2. the method is good, can be reused today
```

**[Measurements of a Distributed File System](https://www.eecs.harvard.edu/cs261/papers-a1/baker91.pdf)** \[1991, 767 refs\]

```
1. a re-measure of the above after six years
2. key findings
    1. Our general conclusions are that the basic access patterns are similar today to what they were six years ago
    2. see the tables for data
    3. paging accounts for 35% of server traffic
    4. shared access to mcdified data occurs often enough that a system should provide cache consistency
3. token-based algorithm for concurrent write-sharing
    1. is that still a valid modern method at nowaday?
    2. the write-sharing case which is rare, but worse
4. the summary part is good
```

**[UNIX disk access patterns](http://www.hpl.hp.com/techreports/92/HPL-92-152.pdf)** \[1993, 532 refs\]

```
0. still, good materials to reveal disk accesss patterns
1. key findings, very different from previous 2 papers
    1. the majority of all operations are writes (57%)
    2. only 8–12% of write accesses, but 18–33% of reads, are logically sequential at the disk level
       25– 50% of all accesses are asynchronous; 50–75% of all I/Os are synchronous
    3. only 13–41% of accesses are to user data; the majority (67–78%) of writes are to metadata; 
    4. 10–18% of all write requests are overwrites of the last block written out
    5. swap traffic is mostly reads (70–90%).
    6. I/O activity is very bursty: mean request queue lengths seen by an incoming request range from 1.7 to 8.9 (1.2–1.9 for reads, 2.0–14.8 for writes), while we saw 95th percentile queue lengths as large as 89 entries, and maxima of over 1000.
    7. there was almost no difference in the mean physical I/O times between the FCFS and SATF scheduling disciplines in the disk
2. trace method
    1. All of our data were obtained using a kernel-level trace facility built into HP-UX
3. the caching
    1. use NVRAM cache (in 1993? so early)
    2. read-ahead significantly reduces total read time
```

**[File System Aging—Increasing the Relevance of File System Benchmarks](https://www.eecs.harvard.edu/margo/papers/sigmetrics97-fs/paper.pdf)** \[1997, 130 refs\]

```
1. good starting point - test fileysystem based on aging
   the major results of aging is fragmentation
   algorithms may behave significantly only in aged case. the durable of performance against aging.
2. the method to replay aging
    1. the author has a series of fs snapshots in hand
       then they generate workload by comparing successive pairs of snapshots (and its inodes)
       the above cannot catch files that are created and deleted between the successive pair of snapshots, so
            they profile real fs and sample from it to simulate files create/delete in between
3. layout score: meansure fragmentation, i.e. whether blocks in file are contiguously allocated
4. SmartFrag allocation algorithm: always attempts to allocate the block immediately adjacent to the previous file block
    1. it looks like the extent-based allocation
5. misc
    1. three meanings of fragmentation
        1. fragmentation in FS: how un-contiguous are the file blocks allocated. fragmentation increase disk seek
        2. external fragmentation: for allocator, the space fragments that are too small to fit in a new task/file
           internal fragmentation: the space allocated to the task/file may be larger than what it asked. the leftover is fragmentation.
           http://stackoverflow.com/questions/1200694/internal-and-external-fragmentation
```

**[Scheduling Algorithms for Modern Disk Drives](https://users.soe.ucsc.edu/~sbrandt/290S/scheduling.pdf)** \[1994, 333 refs\]

```
1. disk scheduler (on hardware disk) scheduling algorithms
   FCFS vs SSTF vs Scan (elevator) vs C-SCAN vs Look vs C-Look vs VSCAN
    1. C-Look wins
2. key findings (disk is equipped with on-board prefetch cache, utilize it)
    1. Incorporating complex mapping information into the scheduler provides only a marginal (less than 2%) decrease in response times
        1. although features such rM zoned recording, track/cylinder skew, and defect reallocation complicate the translation of logical block numbers into physical media locations; the benifit of more knowledge results are little
            1. is disk againg problem tested?
    2. Algorithms which effectively utilize prefetching disk caches provide significant performance improvements for workloads with read sequentiality. (C-Look)
        1. good bias to serve sequential rw
```

**[Disk Scheduling Algorithms Based on Rotational Position](https://users.soe.ucsc.edu/~sbrandt/290S/scheduling2.pdf)** \[1991, 244 refs\]

```
1. Optimal Access Time (OAT) algorithm defines the theoretical bound of best scheduling, regardless of cost
   it can be used to hint improves for current algorithms
2. The Aged Shortest Access Time First(w) - ASATF(w) algorithm
   M = wTage – TA/τ
3. what is tested for evaluate?
    Service time distributions / mean by arrival rates
    Response time / mean / standard deviation / 95th percentile by arrival rates and parameter w
```

**[The LFS Storage Manager](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.104.1363&rep=rep1&type=pdf)** \[1990, 300 refs\]

```
1. good paper. the beginning of log-structured filesystem
2. designs
    1. write: buffered in file cache first, flush to disk append-only, all writes are sequential and asynchronous
        1. inodes are not in fixed location
        2. benefits from sequential and asynchronous IO
    2. read: use inode map to index inode location. inode map itself is partitioned into blocks and cached like regular files. modification to inode map is log append-only.
        1. it is said "LFS's read performance will match or exceed the performance of current read-optimized file systems in many cases."
        2. inode modification may be not flushed when crash. then, metadata lost?
    3. disk space management: by dividing the disk storage into large fixed-size pieces called segments. inside segments it is sequential. for deleted files, segment cleaning does a simple form of garbage collection. segment summary contains block live/dead etc info
        1. sync request will cause segment to flush, resulting in partial full segments written
           if a db/ceph likes to use a lot of fsync ... trouble
    4. recovery: examine the tail of log to find crash damage. speed recovery up by mark consistent points in log, i.e. checkpoints; it stores all memory-resident data structures in currnet states to the disk location checkpoint region.
        1. don't need to scan entire disk 
        2. so the fast recovery of inode map and segment usage array are enabled by checkpoint
        2. if data is not flushed when crash, all modification since last checkpoint is lost
        3. will the checkpoint action cause metadata structs to temporary locked? impact performance?
    3. performance
        1. mostly, 2x up vs SunFS. random write is also 2x.
        2. for small files, and deletes, 10x up
        3. don't forget the segment cleanning cost
3. referenced in
    1. File System Logging Versus Clustering: A Performance Comparison    [1995, 187 refs]
       https://www.eecs.harvard.edu/margo/papers/usenix95-lfs/paper.pdf
        1. LFS only does well in metadat intensive and a lot of small writes condition, other parts are comparable with FFS
        2. in transaction processing envrionment, cleaner overhead reduces LFS performance by more than 33% when the disk is 50% full
        3. aged LFS suffer from cleanning overhead, as FFS suffers from fragmentation
    2. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.70.8008&rep=rep1&type=pdf
        1. log-structed FS improved from on LFS
    2.5. https://www.usenix.org/legacy/publications/library/proceedings/sd93/seltzer.pdf
        1. LFS doesn't provide the same guarantees made by fsck, the verification of block pointers and directory structures
        2. the memory consumption of LFS is relatively large
        3. more details. good paper to see how LFS is improved.
    3. Scalable Performance of the Panasas Parallel File System
       https://www.usenix.org/legacy/events/fast08/tech/full_papers/welch/welch_html/
       https://www.nsc.liu.se/nsc08/pres/welch.pdf
       http://www.panasas.com/sites/default/files/uploads/docs/Whitepapers/Scalable%20Performance%20of%20the%20Panasas%20Parallel%20File%20System.pdf
        1. Per-file, object-based RAID gives scalable on-line performance
            1. Offloads the metadata server
            2. Parallel block allocation among the storage nodes
        2. Declustered parity group placement yields linear increase in rebuild rates with the size of the storage pool
            1. May become the only way to effectively handle large capacity drives
        3. Metadata is stored as attributes on objects
            1. File create is complex, but made fast with efficient journal implementation
            2. Coarse-grained metadata workload distribution is a simple way to scale
    4. Serverless Network File Systems (xFS)
       http://www.cs.cornell.edu/courses/cs6464/2009sp/papers/xfs.pdf
        1. Although log-based storage simplifies writes, it potentially complicates reads because any block could be located anywhere in the log, depending on when it was written.
        2. The overhead associated with log cleaning is the primary drawback of LFS
```

**[Today: Distributed File Systems NFS Architecture](http://lass.cs.umass.edu/~shenoy/courses/spring03/lectures/Lec20.pdf)** & **[Sun's Network File System (NFS) - Pages](http://pages.cs.wisc.edu/~remzi/OSTEP/dist-nfs.pdf)**

```
1. intro of NFS semantics
2. cache consistency is challenging
3. lock is not good compared as nowaday lockless, atomic, non-blocking, MVCC stuff
   session semantics: no changes are visible until file close, this is not good
   stateless design putting in NFS is all right suitable?
   NFSv4 receives a lot of attention
4. I think it would be good if I checkout CephFS designs
    session semtx no good，stateless ok?，nfsv4 recve gd attention
```

**[Extent-Like Performance from a Unix File System](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.55.2970&rep=rep1&type=pdf)** \[1991, 226 refs\]

```
1. basically now there two approaches of designing FS: log-structured FS (LFS) and update in-place ones (SunOS this paper (aslo called UFS), FFS)
2. good paper. finally people come to "extent", which dominates nowaday filesystem designs
3. key findings
    1. group IOs into extent, each involves 15-30 blocks, increase 50% - 100% sequential performance
    2. to introduce intent, only a small portion of filesystem code needs to be modified
    3. the efficiency of CPU cycles per byte is also a consideration
4. previous designs & problems
    1. read ahead: if current read one page greater than last, then we read ahead the next
    2. rotation delays: not necessary now, use track buffer. but it may not be equipped. rotation delay anyway should be obsoleted, they result in holes in track.
    3. the original extents let user decide size, it's hard, and it may vary on inner and outer tracks
    4. clustering: improved from extent, modify UFS to combine blocks adjacent to the requested blocks into a larger I/O request. this is the choosen way
5. designs
    1. transfer IO in units of clusters, which is simply a number of blocks.
       cluster size is variable, and transparent to users
    2. allocator tries to allocate in contiguous blocks. UFS doesn't need preallocation for that.
    3. maxcontig indicates largest cluster size; if less, use bmap to calculate
    4. read and read ahead by units of cluster
    4. write pretend to flush until pages form a full cluster and flushed (delay write impacts persistency semantics?)
6. new problems
    1. when large IOs go through the system, LRU page replacement may become inefficient.
       UFS compromise with new free behind policy
    2. write fairness
7. referenced in
    1. The Design and Implementation of a Log-Structured File System    [1992, 1835 refs]
       http://www.cs.cmu.edu/~dga/15-712/F13/papers/Rosenblum92.pdf
        1. Sprite LFS vs SunOS (paper Extent-Like ...). they are two directions of designing FS
        2. generally this the same paper from the last LFS, but provided more analysis
        3. segment cleanning process is a big headache
    2. Scalability in the XFS File System    [1996, 400 refs]
       http://www.cs.columbia.edu/~nieh/teaching/e6118_s00/papers/sweeney_xfs96.pdf
        1. XFS uses multiple read ahead buffers to increase the parallelism in accessing the underlying disk array. Traditional Unix systems have used only a single read ahead buffer at a time (paper Extent-like ...)
```

**[Deciding when to forget in the Elephant file system](https://cseweb.ucsd.edu/classes/fa01/cse221/papers/santry-efs-sosp99.pdf)** \[1999, 475 refs\]

```
1. good paper, as sees the beginning of versioned filesystem
2. retention of versions of file
    1. info is valuable, storage is becoming cheaper
    2. which file to keep version history?
       no read-only, derived, cached, temporary; only user-modified
    3. the combination of undo: allow a limited-length list of operations
       and long-term history: need to identify landmark versions
           firstly, user can tell the landmark version
           the updates can be short bursts and long seperate of silence. use the head as landmark version
           large delta to the subsequent version indicate a landmark version
3. designs
    0. policies: keep-one, keep-all, keep-safe, keep-landmarks, for differenet file categories
    1. for versions, inode is copy-on-write, block is copy-on-write
       inodes are put in inode log, which maintains the history; an imap holds them, and stores metadata
    2. directories store versioning information explicitly
       each dentry stores a name's inumber, creation time and deletion time
       directory can be a list of inodes, active to cold, by moving code deleted items to cold inodes
    3. cleanner: storage reclaimation, free obsoleted blocks
                 cleanner will lock file. to avoid deadlock, if cleanner encountered a file that is already locked, it will immediately release all of its locks and skip this group
```

**[Storage Management for Web Proxies](http://www.eecs.harvard.edu/~syrah/filesystems/papers/shriver_2001.pdf)** \[2001, 66 refs\]

```
1. good paper. filesystem design for caching web proxies, i.e. CDN nodes
   Hummingbird achieves 2.3-4.0x performance increase against Squid on UFS async, 5.4-13x against XFS
2. key findings
    1. web proxy doesn't need to ensure persistency, because everything can be retrieved again from backend
       espeically metadata, which accounts for large portion of sync IO overhead.
       web proxy can do metadata async and don't need to ensure correctness
    2. web proxy app can decide file naming, doesn't need to keep them the same with backend
       what is actually needed is a flat namespace; long names and directories slow down things
    3. reference locality. web client access has locality, the paper identifies it as locality set.
       and pack locality set into the same cluster/extent
    4. files are always access sequential and entirely on web proxy, different from general purpose fs
    5. most file size are small, 90% smaller than 8KB
    6. web proxy manages its own application-level cache. and filesystem cache things again. that's not necessary
3. designs
    0. Hummingbird manages a large memory cache
    1. flat namespace. use a hashtable to store pointers to files.
       URL names (which is long) is stored off memory in its cluster
    2. decide locality set by LRU of app access. locality set are packed into the same cluster/extent
       data access is organized as cluster
    3. web proxy app pass pointers to and from hummingbird FS. it use a special linked lib rather than POSIX.
       no extra memory copy. alleviate multiple buffering problem
    4. most metadata in memory, don't need to ensure strong persistency / consistency
    5. recovery: to warm the memory cache, use hotness recorded in file and cluster metadata.

```

**[RAID:High-Performance, Reliable Secondary Storage](https://web.eecs.umich.edu/~pmchen/papers/chen94_1.pdf)** \[1994, 1492 refs\]

```
1. good paper to summarize disk history trends
   a detailed introduction to RAID technology
   and a series of improvements
2. can be used as reference material
```

**[Scalability in the XFS File System](http://www.scs.stanford.edu/nyu/03sp/sched/sgixfs.pdf)** \[1996, 400 refs\]

```
1. the famous XFS paper. very good paper. breaking through designs.
2. designs
    1. the pervasive use of B+ trees
        1. B+ trees are used for tracking free extents in the file system rather than bitmaps.
            1. a pair of B+ tree for each AG, on indexed by starting block of free extents, another by length of free ext
        2. B+ trees are used to index directory entries rather than using linear lookup structures.
            1. dir names are hashed into 4-byte values to be stored in the B+ tree
        3. B+ trees are used to manage file extent maps that overflow the number of direct pointers kept in the inodes.
            1. XFS uses an extent map rather than a block map for each file
        4. B+ trees are used to keep track of dynamically allocated inodes scattered throughout the file system
            1. inodes are dynmaically allocated by B+ tree, rather than staticially preallocated
    2. uses an asynchronous write ahead logging scheme for protecting complex metadata updates
       and allowing fast file system recovery after a crash
    3. parallel file IO and use DMA to transfer data
    4. cut the fs into allocation groups
       allows relative block and inode pointers, reduces the size of those pointers from 64 to 32 bits
       also allows parallelism in the management of free spaces and inode allocation across multiple AG
    5. to allocate files contiguously
        1. delayed allocation, by build up virtual extent in memory for reserved blocks
           it benefits newly creating files, short-live files, randomly written files which have no wholes
    6. performing file IO
        1. XFS uses a combination of clustering, read ahead, write behind, and request parallelism
        2. instead of a single read ahead buffer, XFS uses multiple, and keep the drives in the array busy
        3. IO clustering for dirty data before actual write, and this works with delayed allocation
        4. direct IO DMA, between user program's buffer and the disk array
           database may need it to avoid mess with unix buffer cache
    7. access and update metadata
        1. use asynchronous write-ahead log for metadata update transaction
           modified data cannot be flushed to disk (unlock and pin in memory) until the log is committed to disk
        2. using NVM devices for transaction log can be very effective in high end OLTP systems
        3. reducing locking, rw lock, exploit parallelism
           XFS has only one centralized resource: the transaction log
           All other resources are made independent either across AGs or across individual inodes
```

**[An Empirical Study of a Wide-Area Distributed File System](http://www.cs.cmu.edu/~coda/docdir/spasojevic96.pdf)** \[1996, 95 refs\]

```
1. Andrew File System, now begins large-scale distributed filesystem, on WAN network
   as told in paper, 1000 servers in 10 countries, AFS uses trusted servers
2. designs
    1. cells: each is a completely autonomous environment, has own servers, clients, and admins
    2. RPC works well on both LANs and WAN
3. findings
    1. hazard rate: if a volume was accessed yesterday, there is 80% chance that it will be accessed again today
    2. more comprehensive statistics ...
4. an interesting comparasion with World Wide Web
```

**[Caching in the Sprite Network File System](http://www.scs.stanford.edu/nyu/01fa/sched/spritecaching.pdf)** \[1988, 689 refs\]

```
1. is it one of the beginning papers to introduce cache into storage systems?
2. deisgns
    0. Sprite network operating system uses large main-memory disk block caches
       both client and server have cache
    1. Sprite guarantees a consistent view of data, even accessing files simultaneously and one file is cached at multiple places
        1. This is done through a simple cache consistency mechanism that
            flushes portions of caches
            and disables caching for files undergoing read-write sharing.
    2. Sprite caches is that they vary dynamically in size
        1. by virtual memory system
           and file system of each workstation negotiate over the machine’s physical memory.
    3. cache structure: sprite cache is organized in 4kb blocks.
       write policy: use delayed-write back.
    4. cache consistency: each read returns the most up-to-date data
        1. sequential write-sharing: a file is shared but is never open simultaneously for reading and writing
            1. a version number for each file. client compare server's version and its own.
            2. server remembers the last writer, when a new reader opens it, server tells last writer to flush
        2. concurrent write sharing: read & write simultaneously
            1. tell clients to flush data and disable caching
    5. use virual memory and swap to handle to contention between cache and user program
        1. and a few possible page replacement policies
     6. crash recovery is not addressed, because many dirty data are cached not flushed
        1. well, nowaday fs only protect metadata, user data is still prone to loss
           or they use batteries & replicated cache; or they force fsync for every write    
3. referenced in
    1. Measurements of a Distributed File System    [1991, 767 refs]
       http://www.cs.rice.edu/~alc/old/comp520/papers/measurements-FS.pdf
        1. as a network file system
    2. OceanStore: An Architecture for Global-Scale Persistent Storage
       https://www.gnunet.org/sites/default/files/p190-kubi.pdf
        1. as Sprite also uses replication and caching to improve availability
```

**[Disconnected Operation in the Coda File System](http://www.cs.cmu.edu/~coda/docdir/s13.pdf)** \[1992, 1439 refs\]

```
0. good paper, it introduced a new area to think about, interesting
   as an extension from write-back caching
1. even client is disconnected from server, the cache (client's local disk) allows it to continue to work.
   cache can be used to improve availability
    1. once connected, propagating changes typically takes about a minute. (disconnection of 1-2 days)
    2. A local disk of 100MB has been adequate for caching during disconnection (disconnection of 1-2 days)
2. designs
    1. when disconnected, cache misses are still rendered as failure
    2. when connection restored, Venus propagate modifications and reverts to server replication
    3. scalability: putting functions on clients rather than servers
    4. the cache in client, and replica on servers, are uniformly seen as replications, see 3.4
    5. we choose optimistic strategy. when client disconnects, it can update, even it's possible to have conflicts
    6. Hoarding: which file to cache? predict which file the user may need, and the related file set
        1. prioritized cache management: recent reference history and per-workstation hoard database, implicit and explicit
        2. hierarchical cache management: to ensure directory ancestors are also cached
        3. hoard walking: cache is in equilibrium, if no uncached object has a higher priority than a cached object.
                          A hoard walk occurs every 10 minutes to help cache reach equilibrium
    7. Emulation: client is disconnected, pretend to have a pseudo-server.
        1. logging information to replay update activities, a replay log.
           log one store record only on file close, and discard previous if overwrite. the log only log pointers to cache rather actual file content
    8. put metadata in RVM (recoverable virtual memory), rather than UNIX file, to make synchronization simple
    9. Reintegration: replay. server will always validate client log again. if fail, save a replay file, and provide a tool for user to inspect
                      the complete replay is wrapped in one transaction, either succ or fail entirely
        1. conflict handling: to detect, use a storeid (version) attached on each object, which identifies the last update to it.
                              if conflict, abort entire reintegration, except that directory update can be auto merged
```

**[The Zebra Striped Network File System](https://users.soe.ucsc.edu/~sbrandt/290S/zebra.pdf)** \[1995, 327 refs\]

```
1. another Sprite operating system paper. it shows log-structured filesystem in distributed version
   many things are improves from LFS. good paper to read.
2. designs
    1. the style is log-structured append-only, in a distributed stripping manner
       the log is stripped and parity-ed by client, then stored in multiple servers
    2. each file has its metadata: an array of block pointers to its actual log data stripe.
       they are stored in the centralized file manager.
           1. when client/cleaner updates file, it add "deltas" in its log, and file manager gets the update
              (like LFS's inode map written into the log).  client will send "deltas" to file manager
           2. file manager also reject delta to solve conflicts
           3. the file manager also stores its data to Zebra storage servers, instead to its local disk
              so that the crash of file manager won't so easily destroy its data
    3. a centralized stripe cleaner server identifies strips with the most free space, and move live blocks to new strips
           1. "deltas" are used to compute utilization information. stripe status file is used to summarize for each stripe.
           2. compared with JVM garbage collection, can it be more clever, than just a merge compact?
           3. cleaner optimistically copy the block, then compare whether it is changed while copying
    4. first buffered in cache, flush when a stripe is full
        1. however, transaction process, which has a lot fsync, mess up the cache advantage and will result in poor performance
           generally this is the problem with log-structured approach
        2. another problem with log-structured approach. since write is sequentially batched as log, the read is not sequential now
           read ahead (or, clustering), which is highly regarded in "Extent-Like Performance from a Unix File System".
           overall, this is a question of "File system logging versus clustering".
    5. the cache consistency problem
        1. use what is in "Caching in the Sprite Network File System"
           overall I think this adds a bunch of communication delays
```

**[SWIFT/RAID: a distributed raid system](https://www.usenix.org/legacy/publications/compsystems/1994/sum_long.pdf)** \[1994, 152 refs\]

```
1. interesting way to construct storage fs: instructions, op-codes, plan executor, finite state machines, ...
   its like designing a hardware, to do a distributed RAID. may be realtime stuff can also borrow this approach.
2. designs
    1. transfer plan executor - a distributed finite state machine
        1. a plan set contains a local transfer plan (for client), and a remote transfer plan (for server)
           operations := a sequence of atomic primitives
           atomic primitives is called instructions := a C subroutine
        2. the local and remote instructions will cooperate in lock-step
           explicit synchronization programming is not required
    2. experience with network
        1. Avoid time-outs and retransmissions.
        2. congestion avoidance is better than congestion recovery.
           The use of stop-and-wait protocols provide congestion avoidance
```

**[Anticipatory Scheduling: A Disk Scheduling Framework to Overcome Deceptive Idleness in Synchronous I/O](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.29.1503&rep=rep1&type=pdf)** \[2001, 272 refs\]

```
1. it is the anticipatory IO scheduler used in Linux
   https://en.wikipedia.org/wiki/Anticipatory_scheduling
2. key findings
    1. deceptive idleness
        app may issue disk read requests in a synchronous manner, interspersing successive requests with short periods of computation
        but disk scheduler incorrectly assumes that the last request issuing process has no further requests,and becomes forced to switch to a request from another process.
            1. but, will programming-level buffered reader, like in Java, already copes with this problem? while loop read line won't actually issue read line by line.
    2. prefetching looks effective but may not be practical to eliminate deceptive idleness
3. designs
    1. Anticipatory scheduling overcomes deceptive idleness by pausing for a short time (a few milliseconds) after a read operation in anticipation of another close-by read requests
    2. how long to wait?
        1. anticipation heuristic
            benefit = (calculated_positioning_time(Candidate) - LP.expected_positioning_time)
            cost = max(0, LP.expected_median_thinktime - elapsed)
            waiting_duration = max(0, LP.expected_95percentile_thinktime - elapsed)
            return (benefit > cost ? waiting_duration : 0)
        2. online statistics need to be collected, and weighted with a decay factor
    3. architecture: the scheduler core wraps an existing scheduler, and asks anticipation heuristics how long to wait
    4. timer: choose i8254 Programmable Interval Timer (PIT) to generate interrupts every 500us
```

**[A Low-bandwidth Network File System](https://users.soe.ucsc.edu/~sbrandt/290S/lbfs.pdf)** \[2001, 1002 refs\]

```
1. now it comes using variable-length / rolling hash dedup in the filesystem transmission
   generally good paper to read about
2. designs
    1. LBFS provides close-to-open consistency
        1. flush on close
        2. use lease (like rw token) and version compare to determine whether local cache is valid
           when a client open write the file and not close yet, other clients see the stale version
    2. LBFS uses are large persistent file cache at client, to contain a user's entire working set
       when modifying a file, client must send the changes to server (for consistency?)
    3. to reduce bandwidth by exploiting similarities between files 
       when possible, LBFS reconstitutes files using chunks of existing data in server and client cache
       instead of transmitting them over network
        1. use rolling hash to determine chunk boundary (like the variable-length dedup today)
            0. 48-byte rolling region, 8KB average chunk size
            1. need to handle pathological cases, by impose minimum and maximum chunk size
        2. a chunk index database, by first 64bit of SHA-1 => <file, offset, count>
            1. doesn't rely on database correctness, always recompute SHA-1 for chunks
            2. implemented by B-tree
    4. NFS RPC handling
        1. use aggressive pipelining of RPC calls to tolerate network latency
        2. use asynchronous RPC library
        3. compress all RPC traffic using gzip
    5. file read and write
        1. client needs to communicate SHA-1 with server. it's an overhead
        2. when write, client first write tmp file on server, then atomic update
    6. security concerns
        1. since we use SHA-1 dedup, a client can probe whether a specific chunk exist in the backend fs,
           by measuring the time spent on saving that chunk. this leaks information
3. some questions
    1. the server side is still file-based. why not instead change it to chunk-based?
```

**[File Server Scaling with Network-Attached Secure Disks](https://users.soe.ucsc.edu/~sbrandt/290S/nasd.pdf)** \[1997, 313 refs\]

```
1. this paper discusses several NAS architecture, and gives detailed evaluation.
2. the comparison
    1. SAD (Sever-attached disks): client to/from disk communication must go through file manager server
    2. SID (Server integrated disks): the same with SAD, except the file manager server is a specialized server that's more efficiently
    3. NetSCSI: client to/from disk data transfer doesn't need to go through server. it exposes the disks to client network, thus less secure
    4. NASD (Network-attached secure disks): file open/close needs to go through server. data transfer is directly from client to disks. client needs to authenticate through server.
   client to disk connection uses encrypt link.
3. the evaluation
    1. generally NASD requires less server interleaving in client communication with disks. it's more efficient.
```

**[RAMA: An Easy-To-Use, High-Performance Parallel File System](https://users.soe.ucsc.edu/~sbrandt/290S/rama.pdf)** \[1997, 52 refs\]

```
1. people start to think about using data distribution algorithms to split data across disks
   closing to what today scale-out storage does
2. designs
    1. use hashing to pseudo-randomly distribute data to all of the disks
       allowing any node to determine any block's position without consulting the filesystem
        1. how to handle add/remove nodes?
    2. RAMA requires interconnection network link bandwidth to be an order of magnitude higher than disk bandwidth
    3. the file system acts as a set-associative cache of tertiary storage, in disk line
        1. how to map adjacent file blocks to the same disk line? by a hash function parameter s (set to 4 sequential blocks in a single file)
    4. self-identifying block on disk, so that when recovery a full disk scan can reconstruct everything
    5. tertiary storage is integrated into RAMA. using one migration manager for each disk.
```

**[Serverless network file systems](https://users.soe.ucsc.edu/~sbrandt/290S/xFS.pdf)** \[1995, 606 refs\]

```
1. the famous xFS paper. good to read.
   starting to look like Ceph; but Ceph are still much advanced then it
2. designs
    1. it (xFS) still has server, but "serverless" means distributed decentralized p2p storage architecture
       actually you can install per client and server on one node, so that serverless (client node are servers)
    2. xFS dynamically distributes control processing across the system on a per-file granularity
        1. use maps to hold metadata distribution: manager map, imap, file directories, stripe group
            1. each server has its manager, manager map tells client file no => which manager to find.
               manager map is replicated to each client. the prototype has not yet implemented this dynamic reconfiguration of manager maps
            2. imap are split and stored in each of its manager (by corresponding file no)
            3. file directories are stored as file, like in Linux
            4. instead of stripe each log segment across all storage servers, xFS uses stripe group that is a subset of storage servers
               one parity server per group, instead of one for entire cluster
    3. xFS distributes its data storage across storage server disks by implementing a software RAID using log-based network striping similar to Zebra's
        1. a lot learned from Zebra (or LFS)
    4. cooperative caching to harvest portions of client memory as a large, global file cache
        1. use a token-based cache consistency schema.
           when modify a file, client acquires write ownership first; manager invalidates any other copies of that block.
           when another client tries to read/write, manager revokes the previous ownership and force it to flush
    5. how to determine which file is assigned to which manager?
        1. First Writer: xFS chooses an index number that assigns the file’s management to the manager co-located with that client
    6. security: note that each client can access each server
        1.  a damaged xFS client can do wider harm by writing bad logs or by supplying incorrect data via cooperative caching
```

**[Frangipani: A Scalable Distributed File System](https://users.soe.ucsc.edu/~sbrandt/290S/frangipani.pdf)** \[1997, 590 refs\]

```
1. distributed filesystem by two layer design: first a distributed block layer, i.e. a big virtual disk; then this fs
   good to read
2. designs
    1. separated into two layers. the lower layer is Petal, a distributed storage service that provides virtual disks.
       the filesystem layer, Frangipani, focuses on filesystem itself
        1. this makes Frangipani internally much simpler
        2. what Frangipani sees in Petal is a big shared disk
    2. emphasize on adminstration ease
        1. all users are given consistnet view of the same set of file
        2. ease of adding in new servers, without interruption
        3. admin doesn't need worry about which server manage which piece of data
        4. can make a full and consistent backup of the entire filesystem without interruption
    3. distributed lock service: multi-reader/single-writer
        1. only one write is allowed to write file, write excludes write.
           when write lock is released, must flush cache.
        2. to avoid dead lock, it requires ordered locking
        3. use lease to deal with client failure.
        4. lock service implementation
            1. version 1: a single, centralized server that kept all its lock state in volatile memory
            2. version 2: stored the lock state on a Petal virtual disk, writing each lock state change through to Petal before returning to the client
                          If the primary lock server crashed, a backup server would read the current state from Petal and take over to provide continued service
            3. version 3: each lock server takes a partition of the lock table (a lock group)
                          Paxos is used to make consensus of which server is assigned which partition, and the recovery
                          lock states are written to underlying Petal
    4. Frangipani runs in the kernel, why? actually, Frangipani doesn't have an independent file server
        1. from the architecture diagram, each client uses its kernel's Frangipani fs model to access the Petal big virtual disk
           the lock service is used to manage concurrent file access, and tell servers some metadata, and manage lease
        2. this design makes Frangipani fs really simple
    5. logging sometimes occurs twice,once to the Frangipani log, and once again within Petal itself
       log protects metadata update; only metadata is logged, not user data.
       only after log is written, does the server modifies the actual metadata
    6. backup
        1. backup by first snapshot the disk (enabled by Petal), then backup the snapshot
            1. snapshot is based on copy-on-write, in Petal this is by bumping up the epoch number
               Petal: http://www.scs.stanford.edu/nyu/01fa/sched/petal.pdf
        2. it is possible that when doing snapshot, the fs is not in consistent state.
           Frangipani says this can be improved by that, the backup process first requires a write lock for the entire filesystem (force it to flush) and then do snapshot
```

**[File-Access Characteristics of Parallel Scientific Workloads](https://users.soe.ucsc.edu/~sbrandt/290S/pfw.pdf)** \[1996, 237 refs\]

```
1. the paper compares various of workload characteristics of CFS, CMS, CMMD
   "what to benchmark" can be reused when we study similar problems
2. trace methods
    1. record all the IO in the workload filesystem, rather than standard host IOs
       instrument the library calls from user to filesystem, the instrument is in user space
    2. the traced event records are first buffered on host, write to disk or send to network with large blocks
       the instrumentation increases overall application execution time by less than 5%
3. what is measured
    1. the number of jobs by fraction of time
       and the number of compute nodes by percent of jobs
    2. number of files opened by jobs
       and the portion of "temporary files"
    3. the density distribution of IO request size
        1. by request count
        2. by data amount
    4. sequentiality
        1. read, write, and read-write
    5. regularity: most access are actually regular (can be using of matrices)
        1. the variety of access intervals (the bytes interval between two accesses) to a file
        2. the variety of request sizes to a file
        3. strided-access: most access are simple-stride
           stride-segments: a group of requests that is in a single simple-strided pattern
           nested strided: indicates the use of multidimensional metrics
    6. synchronized access modes: most access are synchronized
    7. file sharing between and within jobs: mostly read-only files
        1. found large amounts of block-sharing, implies inter-process spatial locality, and suggestion of caching
4. some conclusions
    1. the current filesystem interface force users to break down large parallel IO activities into small, non-consecutive requests
       this should change. (related to strided IO requests)
```

**[The Vesta Parallel File System](https://users.soe.ucsc.edu/~sbrandt/290S/vesta.pdf)** \[1996, 307 refs\]

```
1. the paper of how to exploit strided-access and design the parallelism for scientific workload
2. key designs
    1. general
        1. for the author's text, scientific application heavily relies on operations of metrix
           so that many optimizations take matrix as the scenario
        2. the key of Vesta is to express the underlying parallel structure of files directly to application programmers
           (in 2-dimentional cell + BSU paradigm)
           access are paralleled into IO nodes, subfiles, and strided-access
        3. there is not client-side caching, the good is no cache consistency problem, the bad is data travsal network overheads
           client app should instead manage the cache by itself.
          (but cache is provided on IO nodes in Vesta, called buffer cache, and it has prefetch. buffer cache has priority management
        4. UNIX compatibility is sacrificed
    2. there is no central metadata. process accesses data directly to IO nodes where the required data or metadata reside
        1. file metadata are distributed among all IO nodes, and are found by hashing file path names
        2. Vesta objects resides in memory-mapped table, the entry containers its metadata, and points to its master node
    3. partitioning the file/data
        1. "cells" is the container of data. file is partitioned into cells.
           The number of cells defines the maximum level of parallelism to access that file
           cell is a sequence of "BSU", basic stripping unit, of that file.
           cell and BSU can be seen as an 2-dimensional array / metrix.
        2. "partition" / "subfile" corresponds to column, row, or block of that matrix (cell + BSU). it represents the access pattern.
           app can specify which "subfile" it opens. param Vbs, Vn, Hbs, Hn defines how the "subfile" is.
        3. the data cell/BSU/subfile partitioning are designed to work with matrix operation on various calculations
           matrix data is scattered across IO nodes and access in parallel
    4. concurrency control: a fast token-passing mechanism
            1. also, access to different cells, subfiles, can be paralleled
            2. there is a scheduler mechanism to govern the concurrency control
            3. the concurrency control can be fully turned off, i.e. the reckless access mode, if the app knows for sure it doesn't have concurrency control problem
    5. structures of storing data
        1. the block list of each cell is organized as a 16-ary tree
```

**[HFS: A Performance-Oriented Flexible File System Based on Building-Block Compositions](https://users.soe.ucsc.edu/~sbrandt/290S/hfs.pdf)** \[1997, 73 refs\]

```
1. compose building blocks to serve functional variety, a bit like storage service chaining.
   good paper to read
2. designs
    1. HFS is designed for (potentially large-scale) shared-memory multiprocessors
       they have been focusing on IO intensive parallel scientific applications
       they try to may the overhead of composing building blocks as low as negligible
    2. some pre-knownings
        1. most IO bandwidth goes to accessing temporary files
        2. the file structure can be optimized for the particular access pattern of the application
        3. application may have predictable access patterns that can be used to optimize IO performance
    3. architecture
        1. the Alloc Stream Facility (ASF) is an IO library that makes up the application layer of HFS
            1. type interface building blocks
                1. they import ASI interface but export a standard IO interface to the application
                   such as (emulated) standard Unix IO system call interface and stdio interface
            2. type Alloc Stream Interface (ASI) building blocks
                1. ASI building blocks expose ASI interfaces, thus can be composed in arbitrary ways
                2. ASI provides building blocks for latency hiding, compressing/decompression, advisory locking
                3. for multi-threading, each thread can use a different prefetching building block (per thread building block)
                   and then connect to the same locking building block for the advisory locking policy
            3. type service-specific building blocks
                1. they import the interface of a particular IO service: terminal, file, network connect
                   and exports the ASI interface
                2. there are also separated building blocks for read-only, write-only, read/write access for each IO service
                   direction-specific building blocks are more efficient than general ones
            4. application-layer building blocks are stateless thus can be changed at runtime
        2. the logical layer provides fs authentication, naming (directories), locking services
           they are system servers of HFS
            1. there are 4 basic types of building blocks: naming, open authentication, access authentication, locking
            2. logical layer building blocks are persistent and instantiated by the application when the file (or directory) is created
        3. the physical layer implements files and controls the system disks
            1. all building blocks in physical layer import and export the same interface
            2. per-disk building blocks have 3 types
               they provide the flexibility for all different types of filesystems
                1. extent-based: like the extent-based write-in-place filesystem
                2. random access: the log-structured filesystem
                3. sparse data: optimized for files with large un-populated areas
            3. physical-layer building blocks include interfaces below
                1. stripped data: strip in round-robin fashion
                2. distribution: partition a file into contiguous regions
                3. write-mostly: consider disk proximity or load
                4. replication: replicate data
                5. parity: computes and store parity information
                6. application specific distribution: maintains an application specified table that defines how to distribute data
                7. small data: store the data of a small file together with the file metadata
            4. physical-layer building blocks are persistent thus cannot be changed at runtime
            5. persistent building blocks are stored on disk as regular file
        4. the memory manager allows ASF to ensure most file IO occurs through mapped files
        5. compared to Vesta (Corbett and Feitelson 1996)
    4. evaluation
        1. why not compare with other filesystems to say building block overhead is low?
        2. too less data charts, they are not comprehensive enough.
        3. what has been done to optimize for shared-memory multiprocessor systems
           as opposed to distributed-memory multi-computer systems?
            1. mapped file IO? what about persistency constraints?
```

**[OceanStore: An Architecture for Global-scale Persistent Storage](https://users.soe.ucsc.edu/~sbrandt/290S/oceanstore.pdf)** \[2000, 2874 refs\] & [Web Portal](https://oceanstore.cs.berkeley.edu/info/overview.html)

```
1. good paper to read.
   oceanstore uses untrusted servers (vs AndrewFS which needs trusted servers) to build global-scale object storage (vs AWS S3, Azure Storage, Openstack Swift, EMC ECS, etc).
   nodes are connected by a routing network on top of IP.
   replicas are floating without fixed location (vs Ceph etc data distribution algorithms)
   objects are immutable, modified by appending (grouped) (predicate) updates, which creates new versions.
   the cluster maintains active version of objects and archive cold data by erasure code
   the overall cluster is continuously being optimized by introspection process.
   the API layer support sessions, (complex) conditional updates, callbacks, and facades (filesystem, transactional (DB), web)
    1. however, the system is work-in-process and no much evaluation (or implementation details) are provided
    2. and, written in Java (at least when the paper is being written)
2. designs
    1. some general points
        1. information must be divorced from location. data is nomadic.
        2. each user pay their fee to one particular "utility provider", although they could consume storage and bandwidth from many different providers.
        3. object (and almost any internal data) is identified by GUID
        4. applications
            1. groupware collaboration and personal information tools, such as calendars, emails, contact lists, and distribution design tools
            2. digital libraries and repositories for scientific data
    2. naming
        1. use GUID to identify objects (and most internal data objects), which is the secure hash of the owner's key and some human-readable name
        2. root node of the hierarchical hashing method for erasure coded data archival fragments, is used as GUID
    3. access control
        1. read is protected by encryption. to revoke reader permissions, need to re-encrypt with new key or delete it
        2. write is protected by ACL list
    4. data location and routing
        1. oceanstore is built on a node routing network overlay on top of IP.
           the routing network is used to support data nomadiness
           the routing process consists of a faster probabilistic algorithm, and then fallback to a slower deterministic algorithm
        2. the faster probabilistic algorithm: attenuated bloom filters
            1. use bloom filter combined with distance to show whether target object is through this path
            2. how to deal with circular paths?
        3. the slow global algorithm: a variation on Plaxton et. al.'s randomized hierarchical distributed data structure [40]
            1. it constructs a mesh of neighbor links, based on IP routing distance and node-ID bits
               we map each object to a single node whose node-ID matches the object's GUID in the most bits
               when object is moved elsewhere, we leave a pointer in the searching path
            2. to achieve fault tolerance, it hashes each GUID with a small number of different salt values
               the results map to several different root nodes, to gain redundancy
    5. update model
        1. changes to data is made by client-generated updates, which are lists of predicates associated with actions
           all messages here are addressed through GUID
        2. the model is able to work in ciphertext
            compareversion, compare-size, compare-block, and search
            replace-block, insert-block, delete-block, and append
        3. to serial updates, the cluster is separated into two tiers
            1. a primary tier of replicas, which cooperate in a Byzantine agreement protocol
                1. primary tier consists of a small number of replicas located in high-bandwidth, high-connectivity regions of the network
            2. and a secondary tier, which propagate decisions from primary tier by an epidemic algorithm
                1. secondary tier are organized into one or more application-level multicast trees, called dissemination trees
                2. secondary replicas container both tentative and committed data. they spread tentative commits and pick a tentative serialization order
                   to increase the chance that tentative order will matches what is selected by the primary tier, clients optimistically timestamp their updates
        4. while updates are being propagated through the dissemination tree, the server generates encode archival fragments and distribute them widely
    6. the deep archival storage
        1. cold data is archived by erasure code
        2. to ensure data fragments are retrieved correctly, it uses a hierarchical hashing method to verify
           generate a hash over each fragment, and recursively hash over the concatenation of pairs of hashes to form a binary tree
           top-most hash as the GUID to the immutable archival object
        3. it ranks administrative domains by their reliability and trustworthiness
           and avoid dispersing all of our fragments to locations that have a high correlated probability of failure
        4. there is processes that slowly sweep through all existing archival data, repairing or increasing the level of replication
    7. the oceanstore API
        1. the API layer support sessions, (complex) conditional updates, callbacks, and facades (filesystem, transactional (DB), web)
    6. introspection
        1. Introspection consists of observation and optimization
        2. observation: it process local events, forwarding summaries up a distributed hierarchy to form approximate global views of the system
           At the leaves of the hierarchy, this database may reside only in memory
            1. a level of fast event handlers summarizes local events
            2. A second level of more powerful algorithms periodically processes the information in the database
            3. a third level of each node forwards appropriate summaries to parent nodes for further processing
        3. use of introspection
            1. cluster Recognition: detects clusters of strongly-related objects, to help further optimizations
            2. replica Management: adjusts the number and location of floating replicas
            3. detect periodic migration of clusters from site to site and prefetch data
               e.g. put project files and emails on a local machine during work day, and move them to home machine at night
```

### [Stanford - Secure Computer Systems - David Mazières - Distributed Storage Systems](http://www.scs.stanford.edu/06wi-cs240d/notes/)

Covers most of the foundamental concepts. The lecture notes are very helpful, e.g. to understand what we should grasp in a paper.

**[Soft Updates - a method for metadata consistency](http://www.scs.stanford.edu/06wi-cs240d/notes/l8d.txt)**, **[Soft Updates: A Technique for Eliminating Most Synchronous Writes in the Fast Filesystem](https://www.usenix.org/legacy/event/usenix99/full_papers/mckusick/mckusick.pdf)** \[1999, 121 refs\]

```
1. soft update was first proposed at 1994.
   the general idea is to track update dependencies, and apply them in order, to ensure metadata consistency
   the lecture notes are good source of learning
2. designs
    1. previously, to ensure metadata consistency, there are basically two ways
        1. use synchronous writes to ensure dependent metadata updates are written out in sequence on disk, or
        2. use write ahead logging
    2. the update dependence can be summarized as
        1. never point to a structure before it has been initialized
        2. never re-use a resource before nullifying all previous pointers to it
        3. never reset the old pointer to a live resource before the new pointer has been set
    3. soft updates tracks dependent metadata updates on pointer basis
       any inodes that cannot be safely written yet are temporarily rolled back to their safe value
       after disk write completes, the IO system calls soft update, which then traverses the list of dependent updates to roll-forward
        1. internally, the worklist structure links different type of dependent updates together
           the tasklist structure contains background tasks for the work daemon
        2. throughout the paper there are in detail descriptions about the data structure
3. limitations (copied from the lecture notes)
    1. not as general as logging, e.g., no atomic rename
    2. metadata updates might proceed out of order
    3. crash in middle of mv may result in two names for the same dir
```

**[Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System](https://people.cs.umass.edu/~mcorner/courses/691M/papers/terry.pdf)** \[1995, 1112 refs\], **[lecture notes](http://www.scs.stanford.edu/06wi-cs240d/notes/l13d.txt)**, **[another lecture](http://www.cs.utah.edu/~stutsman/cs6963/lecture/17/)**

```
1. Bayou is highly referenced in oceanstore and also course http://www.scs.stanford.edu/06wi-cs240d/notes/
   like Paxos, but in eventual consistency, and works in weak connections (and perhaps applicable for larger group of servers).
   designed for mobile collaboration apps with no central server and in weak connection (mobile groupware).
   user apps each may hold a local copy (act as the server), and frequently switch between servers.
2. key designs
    1. Bayou is designed to be eventual consistency, work in weak connection, applicable for mobile collaboration apps (mobile groupware)
        1. there is no central server, each app may hold a replica locally and act as a server. user may frequently switch the server to connect to
    2. the storage server holds an ordered log of writes
        1. Bayou servers propagate writes among themselves during pair-wise contacts, the anti-entropy / epidemic / gossip algorithm
            1. the policies by which servers select anti-entropy partners, is tricky, and can affect how many rollbacks the server does
        2. a write consists of update, dependency_check, and merge_procedure
           all of them are specified by user
            1. dependency_check will be checked and ensure to be true before write
            2. otherwise, merge_procedure, a piece of executable/interpretable code, will be carried out
            3. this mechanism allows apps to specify their specific dependency_check: how to detect conflict
               and merge_procedures: how to solve conflict.
               it is a highlighted point in this paper
        3. automatic conflict resolution for all cases is not possible, for which it still needs manual resolution
           this paper provides tools for it
    3. replica management
        1. data is replicated in full at a number of servers
           replica is always available to client even when conflict happens
           data submitted can be tentative then to be committed.
        2. the global ordering of writes are by logical clock of the write's tentative timestamp and committed timestamp.
           writes are ordered on each server, as log. committed writes are always ahead of tentative writes in log
            1. if server receives a write (from client or another server), by whose ordering, should be inserted in the middle of its log
               it rollback, insert the new write, then roll forward / redo previous writes.
        3. a write is called stable when it is committed
           committed writes cannot be rolled back / redo
            1. a server determines a write is stable when the write has a lower timestamp than all servers' clocks.
            2. but the problem is, a server that remains disconnected can prevent writes from stabilizing
               which could cause a large number of Writes to be rolled back when the server reconnects
        4. one server in each replicated data collection is designated as the primary
           it takes responsible for committing writes.
            1. this alleviates the need to gather a majority quorum of servers, with respect to weak connection environment
            2. if primary server is down/unconnectable, writes accepted by other servers simple remain tentative until they eventually reaches the primary
    4. server storage implementation
        1. the tuple store is a in-memory relational database
        2. the committed writes in the write log can discarded (and saved/reflected in checkpoints)
        3. for crash recovery, it use checkpoint and write log
        4. there is a redo log for rolling back writes
        5. two timestamp vectors (logical clock)
           the "C vector" for write's committed timestamp, the "F vector" for tentative timestamp
    5. security
        1. it use public key authentication schema
        2. cert revocations are stored and propagated with the writes to that data collection
        3. the primary server checks access controls (as the second time), to ensure cert revocations are applied
            1. even when not all servers are aware of that revocation
```

**Other lectures I like**

```
1. Databases & Consistency: http://www.scs.stanford.edu/06wi-cs240d/notes/l6.pdf
2. XFS: http://www.scs.stanford.edu/06wi-cs240d/notes/l7d.txt
3. Kerberos and SFS: http://www.scs.stanford.edu/06wi-cs240d/notes/l9.pdf
4. Consistency (and Logical Clocks): http://www.scs.stanford.edu/06wi-cs240d/notes/l11.txt
```

### [The University of UTAH - Ryan Stutsman - Distributed Systems](http://www.cs.utah.edu/~stutsman/cs6963/lecture/)

Helpful lecture notes about key concepts in distribute systems and deep dive of modern famous system designs.

**[Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf)** \[2001, 12405 refs\], **[leture notes](http://www.cs.utah.edu/~stutsman/cs6963/lecture/16/)**

```
1. a famous DHT paper, peer-to-peer routing and location scheme, very highly referenced, good to read
   it uses routing instead of direct mapping (consistent hasing, CRUSH, metadata table, etc) to solve the data distribution/location problem
   generally, instead of store a full routing table (or a full consistent hash ring), Chord stores sparse 2-exp entries
   in steady state of an N-node network, each node stores O(logN) entry, key lookup takes O(logN), node join/leaves take O(logN*logN)
2. key designs
    1. Chord is simple. given a key, it maps the key onto a node.
    2. rather than use a direct key->node mapping (like consistent hashing or CRUSH map), chord use routing to locate key->node
       it's like Oceanstore's data location routing, but much simplers and handle concurrent node joins and failures well
    3. the routing protocol
        1. the only must-know to ensure correct routing: each node knows its successor on the ring
        2. to route more efficiently: the finger table
            1. each node has a finger table: node n.finger[i] := successor_node_of(n + 2^(i-1))
                1. the 2-exp ensures: 1) table size is O(logN)
                2. it can change 2-exp to (1+1/d)-exp, so that table is more dense with more entries, but lookup time is shorter
            2. to lookup k, node n finds the closest entry in its finger table and pass to it
                1. the 2-exp ensures total lookup/routing time is O(logN)
        3. basic node join protocol: for a new node n to join
            1. to populate n's finger table, just use the routing protocol to lookup each entry's position
            2. to update existing nodes' finger tables
                1. node n will become the i-th finger of node p iff. 1) p precedes n by at least 2^(i-1), and 2) the i-th finger of p succeeds n
                2. takes O(logN * logN) time, and it is the overall time complexity of joining a node
        4. stabilization: to handle concurrent node join/leave well, actually used instead of the above basic node join/leave protocol
            1. stabilization guarantees to add nodes to a Chord ring in a way that preserves reachability of existing nodes
            2. the stabilization algorithm is: 1) when n joins, fix related successor and predecessor links
                                               2) to fix finger table, periodically randomly select an index i, and lookup it
            3. the theory proves the eventual consistency
                1) once a node can successfully resolve a given query, it will always be able to do so in the future
                2) at some time after the last join all successor pointers will be correct
            4. the lookup time is not interrupted
                3) if we take a stable network with N nodes,
                   and another set of up to N nodes joins the network with no finger pointers (but with correct successor pointers),
                   then lookups will still take O(logN) time with high probability
        5. to handle failures and replication
            1. each Chord node maintains a "successor-list" of its r nearest successors on the Chord ring
            2. alternative nodes can also be finger table entries preceding that of the failed node
            3. for replication, the app may store replicas of key k at several nodes succeeding k
    4. the hashes
        1. use SHA-1 so that node distribution are even and robust
        2. hash the node identifier before use, so that an attacher cannot intentionally place node at a certain place of the ring
    5. how other papers evaluate Chord?
        1. Pastry: Scalable, decentralized object location and routing for large-scale peer-to-peer systems
           http://users.ece.utexas.edu/~garg/sp11/382n/resources/pastry.pdf
            1. Chord, along with others, is categorized as a peer-to-peer routing and location schemes
            2. Chord makes no explicit effort to achieve good network locality
        2. Bigtable: A Distributed Storage System for Structured Data
           http://pages.cs.wisc.edu/~remzi/Classes/739/Spring2003/Papers/bigtable-osdi06.pdf
            1. These systems address concerns that do not arise for Bigtable,
               such as highly variable bandwidth, untrusted participants, or frequent reconfiguration;
               decentralized control and Byzantine fault tolerance are not Bigtable goals
        3. Tapestry: A Resilient Global-Scale Overlay for Service Deployment
           http://homepage.cs.uiowa.edu/~ghosh/tapestry.pdf
            1. neither CAN nor Chord take network distances into account when constructing their routing overlay
        4. A Scalable Content-Addressable Network
           http://conferences.sigcomm.org/sigcomm/2001/p13-ratnasamy.pdf
            1. we envision applying CANs to very large systems with frequent topology changes.
               in such systems, it is important to keep the number of neighbors independent of the system size
               (compared to Chord's O(logN) table entry)
        5. Dynamo: Amazon’s Highly Available Key-value Store 
           http://docs.huihoo.com/amazon/Dynamo-Amazon-Highly-Available-Key-Value-Store.pdf
            1. to reduce the additional latency introduced by multi-hop routing,
               some P2P systems employ O(1) routing where each peer maintains enough routing information locally
               so that it can route requests to the appropriate peer within a constant number of hops. 
               Dynamo is built for latency sensitive applications, it was imperative for us to avoid routing requests through multiple nodes
```

**Other lectures I like**

```
1. Flat Datacenter Storage: http://www.cs.utah.edu/~stutsman/cs6963/lecture/03/
2. Leases: http://www.cs.utah.edu/~stutsman/cs6963/lecture/14/
3. Spanner: http://www.cs.utah.edu/~stutsman/cs6963/lecture/15/
```
