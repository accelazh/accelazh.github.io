---
layout: post
title: "Recent Paper Article Readings"
tagline : "Recent Paper Article Readings"
description: "Recent Paper Article Readings"
category: "storage"
tags: [storage, paper, database]
---
{% include JB/setup %}

Recent paper / articles reading. Search "very good", "good", "interesting", "useful" for recommendations. Search "question" for reviews.

```
1. readings: NVM databases
    1. Managing Non-Volatile Memory in Database Systems    [2018, 32 refs]
       https://www.cc.gatech.edu/~jarulraj/courses/8803-f18/papers/nvm.pdf
        1. DRAM-resident buffer manager that swaps cache-line-grained data objects between DRAM and NVM (leveraging byte-addressable)
           The paper summarized and gives the basic thoughts how DB to leverage NVDIMM. Useful as an example.
        2. highlights
            1. NVM <=> SSD page-grained swap
               DRAM <=> NVM cacheline-grained swap
                1. full-page and mini-page in DRAP to leverage space
                2. cacheline-grain to extract hot objects from cold pages
            2. how DBs uses NVDIMM
                1. single-level data storage 
                   using NVM as logging device for in-mem DB
                   DRAM NVDIMM SSD 3-tier hot-cold DB
        n. related materials
            1. CSDN blog: NIL_: Managing Non-Volatile Memory in Database Systems
               https://blog.csdn.net/u013129143/article/details/83829600
            2. How It Works (It Just Runs Faster): Non-Volatile Memory SQL Server Tail Of Log Caching on NVDIMM
               https://docs.microsoft.com/en-us/archive/blogs/bobsql/how-it-works-it-just-runs-faster-non-volatile-memory-sql-server-tail-of-log-caching-on-nvdimm
                1. interesting. instead of storing all logs to NVDIMM,
                   use NVDIMM to store the tail of log (actively writting logs)
            3. FOEDUS: OLTP Engine for a Thousand Cores and NVRAM    [2015, 139 refs]
               https://15721.courses.cs.cmu.edu/spring2016/papers/p691-kimura.pdf
               https://expolab.org/cs590-spring2017/slides/foedus.pdf
                1. in-memory DB offloading pages to NVRAM.
                   master-tree foster-twin algorithm to aviod OCC retry due to page split.
                   per-core logging, need log gleaner to merge
                   interesting paper. 
                2. highlights
                    1. leveraging NVRAM
                        1. DRAM pages offload to NVRAM.
                           concepts: volatile pages (DRAM), snapshot pages (NVRAM)
                        2. log buffered to DRAM, fsync to NVRAM
                    2. leveraging one thousand cores
                        1. OCC by page version compare
                        2. master-tree, foster-twin, to solve OCC retry due to page split
                            1. when split, don't delete old page, old page are marked "moved"
                               new pages are fostered as child of the old page
                            2. transactions need to check "moved" pages
                            3. in case page is "moved" after transaction check,
                               transaction used double-checked lock scheme
                            4. this algorithm is good, useful
                                1. alternatively, Bw-tree's page pool is another solution.
                                   tree points to page-id rather than page address.
                                   splited new page may hold the original page id.
                        3. per-core logging. fsync dump to NVRAM
                           then need map-reduce log cleaner to merge
                3. questions
                    1. the NVRAM devices is done by an emulator ..
                       this can vary way far from real 3DXpoint/Optane
                    2. opensource repo https://github.com/HewlettPackard/foedus
                       now only a readme.md left?
    
    2. How to Build a Non-Volatile Memory Database Management System    [2017, 59 refs]
       https://db.cs.cmu.edu/papers/2017/p1753-arulraj.pdf
        1. listing various aspects DB design diff in NVM: Allocator (non-volatile pointer), DAX interface, Logging & Recover (WBL),
           data placement (hot/cold migrating), etc. Useful paper.
        2. highlights
            1. write-behind logging (WBL)
            2. NVMe over Fabrics - replication
        n. related materials
            1. Write-Behind Logging     [2016, 72 refs]
               http://www.vldb.org/pvldb/vol10/p337-arulraj.pdf
               https://www.slideshare.net/PouyanRezazadeh/write-behind-logging
                1. good paper. WBL persist changes to DB instead of logging, to reduce the double-write overhead.
                   WBL requires MVCC and group commit to work. flushing to DB generates more sequential writes, WBL exploits NVM better random writes
                   Actually the same WBL algorithm can be used on tranditional DB even without NVM (but slower).
                   replication has a problem because there is no WAL logging available now.
                2. highlights
                    1. useful illustration for WAL (Write-ahead logging) as the compare base
                        1. steal and no force
                            1. steal: allow DBMS to flush changes of uncommitted transaction to disk. (thus need undo log)
                            2. no force: DBMS not required to ensure propagates changes to database when transaction commits (need redo logging)
                        2. in-memory DBMS doesn't need fuzzy checkpoints
                            1. i.e. checkpoint contains no uncommitted transactions, because
                               in-mem DB doesn't need buffer manager to access on-disk pages, things are simplified
                        3. group commit
                            1. to minimize the I/O overhead, batches the log records for a group of transactions
                               and then flushes them together with a single write to durable storage
                        4. analysis, redo, undo
                            1. MVCC DBMS obviates the need for an undo phase
                    2. WBL - Write-behind Logging
                        1. must work with MVCC DB
                            1. so that, update an tuple "in-place" is done by delete+insert. the old value is never lost
                        2. must work with group commit
                            1. so that, timestamp Cp and Cd. Before Cp are all commited.
                               Within Cp and Cd are dirty, which should be forgotten during failure restart
                            2. DB must determine visibility of tuples within Cp and Cd.
                               Garbage Collection cleans up dirty tuples, thus shrink Cp and Cd gap
                        3. undo and redo
                            1. WBL doesn't need undo like WAL. DBMS uses the information in the log to ignore the effects of uncommitted transactions
                            2. WBL doesn't need redo neither, because all modifications of committed transactions are already present in DB
                            3. WBL only needs the analyze phase. To retrieve the list of commit timestamp gaps and the commit timestamps of long running transactions
                        4. replicating
                            1. WAL can directly replicate logs
                            2. bug, WBL has problem. it requires overhead to construct WAL and then replicate
                        5. summary
                            1. there are two places to persist changes, database itself or logging
                                1. WAL chooses logging, WBL chooses database itself
                            2. MVCC makes sure old data is never overwritten, new data is appended with an increment version
                                1. so that WBL doesn't need undo, becuase old data is not lost
                               new data is made available by advance the version
                                1. this done by group commit. commit <=> version increment
                                   so there is no database states lagging behind, so WBL doesn't need redo
                            3. writting to logging vs writting to database itself
                                1. WBL chooses writting to database itself, this implies more random writes compared to logging
                                   it underlying relies on NVM's better random writes support, rather logging to exploit sequential writes
                                   the benefit is no duplicated writtings again in logging
                                2. actually, the whole stuff doesn't necessary need NVM, it works on traditional MVCC group commit DB too
                            4. questions
                                1. actually, WBL only writes metadata to logging. it doesn't exploit the fast writting of NVM w.r.t. logging
                                2. also, the byte-addresable property of NVM is not exploit
                3. questions
                    1. the NVRAM devices is done by an emulator ..
                       this can vary way far from real 3DXpoint/Optane
                n. related materials
                    1. Book: Non-Volatile Memory Database Management Systems
                       https://books.google.com/books?id=386HDwAAQBAJ&pg=PA55&lpg=PA55&dq=MVCC+DB+obviates+the+need+for+an+undo+phase&source=bl&ots=jlfJTft6sk&sig=ACfU3U2Iu0VUqBSx6dVe6JNkD-C-yuBkhA&hl=zh-CN&sa=X&ved=2ahUKEwi52dui2LfqAhWCeisKHfGcDCQQ6AEwAHoECA0QAQ#v=onepage&q=MVCC%20DB%20obviates%20the%20need%20for%20an%20undo%20phase&f=false
                        1. The author Joy Arulraj wrote many papers about NVM database and also this book

    3. Non-Volatile Memory File Systems: A Survey    [2019, 2 refs]
       http://repositorio.pucrs.br/dspace/bitstream/10923/15232/2/Non_Volatile_Memory_File_Systems_A_Survey.pdf
        1. RQ1: What are the differences between disk-based and NVM file systems?
           RQ2: What are the challenges and problems addressed by NVM file systems?
           RQ3: What techniques and methods have been proposed to improve NVM file systems?
           RQ4: What is the impact of new file system models on the overall architecture?
        2. Useful paper
            1. just note, the survey also included NVM SSD filesystems besides NVDIMM filesystems

    4. SLM-DB: Single-Level Key-Value Store with Persistent Memory    [2019, 15 refs]
       https://www.usenix.org/conference/fast19/presentation/kaiyrakhmet
        1. No DRAM, single-level KV store by pmem; disk only does L1 level. No journaling
           kv in SSTFile not sorted, instead uses global B+-tree for search
        2. highlights
            1. No journaling. Memtable is persistent in pmem. clfush() as consistent point
            2. Only L1 level, self-merging compaction. Selective compaction
               FAST-FAIR B+-tree Index in pmem
                1. KV pairs in disk file not in sorted order, use B+-tree for search
                   this significantly reduces compaction needs to write amplification
                2. SSTFile compaction candidate selection
                    1. live-key ratio
                    2. the leaf node scans
                    3. degree of sequentiality per range query

    5. An NVM-aware Storage Layout for Analytical Workloads    [2018, 3 refs]
       https://www.researchgate.net/profile/Philipp_Goetze2/publication/326215846_An_NVM-Aware_Storage_Layout_for_Analytical_Workloads/links/5c3c6f9ea6fdccd6b5ab54c5/An-NVM-Aware-Storage-Layout-for-Analytical-Workloads.pdf
        1. based on BDCC. NVM holds index, cache data nodes from disk.

2. readings: TiDB new release features
    1. Key Visualizer: Observe Distributed Databases to Discover the Unknowns
       https://pingcap.com/blog/observe-distributed-databases-to-discover-unknowns
        1. https://cloud.google.com/bigtable/docs/keyvis-overview
           https://www.youtube.com/watch?v=aKJlghIygQw
    
    2. How to Back Up and Restore a 10-TB Cluster at 1+ GB/s
       https://pingcap.com/blog/back-up-and-restore-a-10-tb-cluster-at-1-gb-per-second
        1. why LSM-tree memtable needs to checkpoint SSTables, when we know data is already in log?
            1. data lives in log shortly, eventually they will live in SSTables which are optimized for read (compared to log)
                1. so double-write is a problem, but capacity usable is not a problem
                2. if only metadata is in log, data not, then double-write is not a problem
            2. 华为TaurusDB技术解读（转载）
               https://zhuanlan.zhihu.com/p/64364775
                1. "日志即数据"?
                2. https://zhuanlan.zhihu.com/p/29182627
                    1. should be redo log replication to other nodes
            
            3. 华为Taurus云原生数据库论文分析
               https://zhuanlan.zhihu.com/p/151086982
                1. paper: "Taurus Database: How to be Fast, Available, and Frugal in the Cloud"
                2. very good. highlights
                    1. "POLARDB通过将Innodb的log和page存放到类POSIX接口的分布式文件系统（PolarFs）来实现计存分离。这种做法看似很美好、对Innodb的侵入非常小，但是却有一些严重的问题，Taurus论文中有提及。 具体来说，大量刷脏的时候，持久化page的网络流量对于计算层、存储层都是一个很大的挑战，因为page流量是单纯log流量的几倍到几十倍不等，具体取决于用户的工作负载。另外，page刷脏会抢占log的持久化需要的资源（网络带宽、IO带宽），增大log持久化的延时，继而增大事务提交的延时。另外，由于PolarFs的基于raft（准确说是ParallelRaft）的数据复制方式，导致事务提交的路径上至少需要两跳网络传输，这个架构导致其需要在计算节点、存储节点都需要引入RDMA来减少网络带来的rt。"
                    2. "计存分离的最优做法是采用"log is database"的理念，只需要把log写到存储层，由存储层负责重放log、回写page并尽量减少写放大。将刷脏这个操作从计算层剔除之后，可以降低计算节点的网络开销。Aurora首先采用这种做法，后续的Socrates、CynosDB、Taurus也均采用这个做法。"
                    3. "Aurora将db的数据（也即是所有page）分成若干个10GB大小的shard，相应的log也随data一起保存在shard中。每个shard有6个副本，采用N=6，W=4，R=3的策略，事务提交时需要等到log在至少4个副本持久化之后才能完成提交。Aurora的log持久化、page读取都只需要一跳网络传输。

                    Socrates也是采用"log is database"的理念，但是它单独了一个log层用于快速持久化log（具体实现不详），避免受到重放log、回写page的影响。另外，page svr层从log层拉取log进行重放、回写page，并向计算节点提供读取page的服务。但是page svr层只将部分page缓存在本地，全量的page在额外的冷备层。所以Socrates的读请求有可能在page svr层本地无法命中，进而从冷备层获取page。

                    CynosDB也是采用"log is database"的理念，从公开资料来看，存储层为计算节点提供了Log IO接口与Page IO接口，前者负责持久化log，后者负责page的读取。

                    Taurus也是采用"log is database"的理念，存储层分为Log Store、Page Store两个模块，前者负责持久化log，后者负责page的读取。log持久化、page读取都只需要一跳网络传输。"
                3. questions
                    1. why redo log (physical log) is smaller size of binlog (logical log)?
                        1. and if a pages is altered many times, sync a page be can smaller than redo log too
                    2. replication by logs rather than pages / full data?
                    3. compared to replicate by data, which can use different sets of nodes as replication chain
                       but logs replication need to lock to a fixed set of nodes? because log needs to know its previous logs to be able to replay
                    4. Storage node needs to rebuild pages from logs
                        which means it needs "history"
                        which means no easy to quickly failover to another storage node
                          to mitigate tail latency
                       So you see, instead of 3-replica 3-writes, Aurora uses quorum append
                        i.e. in 6 replicas, write 4 of them, and only require 3 succeeds.
                    5. LSM-tree seems less affected
                        it can just put data into logs. the memtable only for index
                        or memtable only saves changed data. read old data from cache/old-memtable
                        the flush/checkpoint only writes changed data. no flush unnecessary dirty "page" here

            4. how to do consistent snapshot?
                1. BR only needs to send a snapshot timestamp. TiKV supports timestamp multi-version

        2. how database do checkpoints? large database cannot load all data in memory
            1. https://docs.microsoft.com/en-us/sql/relational-databases/logs/database-checkpoints-sql-server?view=sql-server-ver15
                1. checkpoint only includes in-memory data
            2. https://www.sqlskills.com/blogs/paul/how-do-checkpoints-work-and-what-gets-logged/
        
    3. TiCDC: Replication Latency in Milliseconds for 100+ TB Clusters
       https://pingcap.com/blog/replication-latency-in-milliseconds-for-100-tb-clusters
        1. TiCDC Open Protocol. row-level data change notification
            for monitoring, caching, full-text indexing, analysis engines, and master-slave replication between different databases
            to third-party data medium such as MQ (Message Queue)
        2. Before version 4.0, TiDB provided TiDB Binlog, which collects binlog data from TiDB and provides near real-time replication to downstream platforms
            1. TiCDC pulls TiDB's data change logs from a TiKV cluster via the Google remote procedure call (gRPC) API and outputs data to downstream platforms

    4. Large Transactions in TiDB
       https://pingcap.com/blog/large-transactions-in-tidb
        1. "Large transactions caused problems for a few reasons:
                they take up a lot of memory in TiDB,
                they keep locks on many keys for a long time,
                which blocks other transactions from making progress,
                and they can exceed their time-to-live (TTL) and be rolled-back even though they are still working"

    5. Pessimistic Locking: Better MySQL Compatibility, Fewer Rollbacks Under High Load
       https://pingcap.com/blog/pessimistic-locking-better-mysql-compatibility-fewer-rollbacks-under-high-load
        1. TiDB now implements both pessimistic and optimistic concurrency control mechanisms
           MySQL supports pessimistic locking by default

    6. SQL Plan Management: Never Worry About Slow Queries Again
       https://pingcap.com/blog/sql-plan-management-never-worry-about-slow-queries-again
        1. old approach: SQL queries (optimizer hints)
        2. TiDB uses a cost-based optimizer that relies on statistics
            1. statistics can abruptly change becoming out of date as front-end application changes
            2. even with correct statistics, it's difficult to ensure that the optimizer chooses the best execution plan for all cases
            3. To avoid these issues, DBAs often try to find slow queries, rewrite SQL queries, or write comments in query statements (known as SQL hints)
                1. problems
                    1. SQL are generated by framework, unable to change directly
                    2. deploy new code introduces risk
                    3. SQL hints quickly become outdated when data distribution changes later
        3. SQL Plan Management
            1. manually bind an execution plan with a type of queries
            2. automatically create bindings for frequent SQL queries
            3. evolve binding: probe with alternative executino plans
                               perform experiments in a predefined period
            4. oracle: https://docs.oracle.com/en/database/oracle/oracle-database/12.2/tgsql/overview-of-sql-plan-management.html

3. readings: misc piled-up articles
    1. Yarn的DRF多维度公平调度算法
       https://lvsizhe.github.io/paper/2017/06/drf-paper-intro.html
       https://lvsizhe.github.io/paper/2017/07/drf-paper-properties.html
       https://lvsizhe.github.io/paper/2017/07/drf-paper-compare.html
        1. Sharing Incentive, Pareto efficient, Strategy proofness
        n. related materials
            1. YARN 在字节跳动的优化与实践
               https://mp.weixin.qq.com/s/9A0z0S9IthG6j8pZe6gCnw
                1. 单个生产集群达到了 2 万节点
                2. interesting. a lot of improvements
            2. Dominant Resource Fairness: Fair Allocation of Multiple Resource Types    [2011, 1056 
            refs]
               https://cs.stanford.edu/~matei/papers/2011/nsdi_drf.pdf
                1. very good. the algorithm is ridiculously simple, but the properties are ridiculously good.
                   Sharing Incentive, Pareto efficient, Strategy proofness
                2. highlights
                    1. all properties
                        1. Sharing Incentive: 
                        2. Strategy-proofness
                        3. Envy-freeness
                        4. Pareto efficiency
                        5. Single Resource Fairness
                        6. Bottleneck Fairness
                        7. Population Monotonicity
                        8. Resource Monotonicity
                    2. "在证明中将任务看作是可以连续可无限细分的1，即可以启动0.x个的task"
                       "所有用户的Dominant Resource share(后面记为s)同速率的上涨"
                        1. though multi-dimensional, but after normalized, every dimension is same
                           for user A, the diff is only its internal ratio
                            1. dominate share, normalized that different resources have different total amount
                            2. synced grow, keeping dominate share same, normalized that different user submits different sized tasks
                        2. because this synced grow, mostly all resources will be used up at same time
                        3. detailed walkthrough
                            ``
                            # Total resource and consumption of each user task
                            Resource    12      36      72
                            U1          2       6       36
                            U2          3       3       6
                            U3          2       2       8

                            # Normalize different resource amount
                            Resource    1       1       1
                            U1          1/6     1/6     1/2
                            U2          1/4     1/12    1/12
                            U3          1/6     1/18    1/9

                            # Dominate resource share grow in sync, normalize user task size
                            Resource    1       1       1
                            step_U1     1/6     1/6     1/2
                            step_U2     1/2     1/6     1/6
                            step_U3     1/2     1/6     1/3
                            ``
                    3. questions
                        1. "Strategy-proofness: user无法通过虚假声明自己的资源使用量，来获得有利于自己的分配。即，在DRF下，即便用户虚假声明自己的任务资源使用量，也无法让其启动更多的task。"
                            1. But ... a user can declare its task smaller to launch more tasks
                               hope the resource quota is battle proven
                        2. how to apply different weights per user?
                            1. weighted DRF (§4.3), see paper

4. readings: recent piled up articles (paper level almost)
    1. 字节跳动分布式表格存储系统的演进
       https://mp.weixin.qq.com/s/DvUBnWBqb0XGnicKUb-iqg
       https://mp.weixin.qq.com/s/oV5F_K2mmE_kK77uEZSjLg
        1. very good. understanding ByteDance version of BigTable and Spanner. And to compare with ours
        2. highlights
            1. interesting features
                1. multi-datacenter. replication location, sync/async, cross reads
                2. distributed transaction
                3. load balancing on multi-dimensional resources on heterogeneous + physical/VM machines
                4. global secondary index (not per-partition, but global secondary index)
                5. ByteSQL. Execution optimization, as Read-Write merged in one OP for Insert/Update/Delete
                6. online schema change
            2. looking into future
                1. Offload compaction / GC
                2. analytical columnar storage, HTAP
                3. multi-mode databse: combine Graph, Time-series, Geo data, SQL, non-structured API
                4. more consistency levels e.g. in cross datacenter sync
                5. cloud native, with Kubernetes
                6. distribution transaction cross region TSO, Percolator vs Spanner
        n. related
            1. DFR - Dominate Resource Fairness
                1. used in YARN. 
                   https://www.usenix.org/legacy/events/nsdi11/tech/slides/ghodsi.pdf
                   https://people.eecs.berkeley.edu/~alig/papers/drf.pdf
                2. DFR seems can be used in multi-dimensional scheduling in heterogeneous resources in Bytable
                   but how ..?
                n. related materials
                    1. Quasar: Resource-Efficient and QoS-Aware Cluster Management
                       http://csl.stanford.edu/~christos/publications/2014.quasar.asplos.pdf
                        1. OK to be applicable?
                        2. classification for interference and scale-up.
                           Greedy scheduler Allocation and Assignment 
            2. TiDB Percolator TLA+
               https://github.com/pingcap/tla-plus/blob/master/Percolator/Percolator.tla
                1. Percolator uses primary key's lock as the synchronization point of committed or not.
                     Read needs to follow up from secondary keys to primary keys to determine committed or not
                   Bytable uses a row in the transaction table as the sync point of committed or not

    2. 数据仓库、数据湖、流批一体，终于有大神讲清楚了！
       https://zhuanlan.zhihu.com/p/140867025
        1. good. very easy and fine explained HSAP, Data Lake, Lambda架构
        2. HASP
            1. Batch：离线计算
            2. Analytical：交互式分析
            3. Servering：高QPS的在线服务
            4. Transaction：与钱相关的传统数据库（绝大多数业务并不需要）

    3. 字节跳动在 Go 网络库上的实践
       https://mp.weixin.qq.com/s/wSaJYg-HqnYY4SdLA2Zzaw
        1. Nocopy Buffer

    4. Practical Fast Replication
       https://zhuanlan.zhihu.com/p/59991142
        1. paper: NSDI 2019 "Exploiting Commutativity For Practical Fast Replication"
        2. "witness" node to add additional "abilities" to existing replication facility

    5. Amazon Aurora 深度探索 - 腾讯技术工程
       https://zhuanlan.zhihu.com/p/33603518
        1. though written 2 years ago only for Aurora Single master, but still good worth reading
            author's comments are also interesting
        2. questions and thinkings
            1. Aurora Singe master
                1. the master node replicas logs to storage node, and in quorum commit way.
                   storage node in charge of everything else, e.g. redo to pages, conflict detection
                   storage node simply sequentially write logs to disk, and then sync back to master writer
                    1. this means even there is only one master, the master is very lightweighted, to support high throughput for transaction
                        1. design principle "minimizing master node write delay"
                    2. everything possible is offloaded to storage layer, which is a distributed layer
                2. "log is database"
                    1. replicating logs to storage rather than flush back pages is more efficient. because pages mix with unrelated data
                    2. LSM-tree if well-implemented should not have this problem, because only delta-data needs flush, not like flushing entire page
                    3. actually, you cannot store all logs forever. there is a VDL to point min log kept.
                       there is a concept that a "checkpoint" of pages need to present to keep the oldest snapshot of data
                        1. these "pages" are stored to AWS S3, smart. so, it's OK to call "log is database" as Aurora only stores pages
            2. Aurora multi-master
                1. Allow more master nodes to send logs to storage node.
                   for conflict resolving, the key is storage node, who is the sync point of conflicting pages
                2. How to guide user requests to different masters to avoid conflict? I didn't find any materials mentioning it
                    1. if related requests are send to different masters, it's easy to trigger conflicts, thus slow down overall throughput
                    2. thus you'll need a propoer partition strategy, who can do this partition for customers? I didn't see mentioning
                        1. secondly, with partition, you again introduced the need of cross master distributed transactions. how's that done?
                           the story of aurora multi-master isn't ending
                        2. thirdly, how a master is mapped to storage nodes? storage nodes must have certain partition policy to own pages
                            1. as the Author suggests, transaction data can be pushed to page level,
                               managed by storage nodes, and then be able to share acorss master nodes

5. readings: multi-dimensional resource placement / load balancing
    1. The power of two random choices - Marc's Blob
       https://brooker.co.za/blog/2012/01/17/two-random.html
        1. very good.
           randomly pick two nodes, and select the best one within them.
           this can yield surprisingly good load balancing result.
           and it is robust against delayed load info synced
        2. highlights
            1. Best of three is NOT better than best of two
                1. and when load refresh interval increases to > 10secs
                   Best of three getting worse, suffering from busy-quite-repeat issue

    2. Surprising Economics of Load-Balanced Systems
       https://brooker.co.za/blog/2020/08/06/erlang.html
        1. good. with c*0.8 req/sec, and c servers. the larger the c, avg response time decreases
           the result implies load balancing design architectures, breakdown big requests / servers

6. readings: TiDB papers and so on
    1. TiDB: A Raft-based HTAP Database    [2020, 0 refs, VLDB]
       http://www.vldb.org/pvldb/vol13/p3072-huang.pdf
        1. Very good. Now opensource hits the most challenging technologies in database.
           distributed scalable, SQL relational & distributed transactions, multi-raft replicating data,
           OLTP + OLAP in one cluster with TiFlash learner node
           Related Work part is good to understand HTAP landscape
        2. highlights
            1. HTAP (Hybrid Transactional and Analytical Processing), using extra replica in a different columnar format to support OLAP
                1. the replica is a learner node in the Multi-Raft replication group
                2. The TiFlash is using Delta Tree + B+ tree index
                    1. Delta Tree is a two-layer simplified LSM-tree.
                    2. compared to LSM-tree
                        1. Delta tree reads faster: each read accesses at most one level of delta files that are indexed in a B+ tree
                        2. the write amplification of DeltaTree (16.11) is greater than the LSM tree (4.74)
                3. paper summarized other approches to do HTAP, besides ETW to separated systems
                    1. MemSQL, Hyper have their different special ways, but the key lacking is isolation
                       TiDB uses a different replica, so that can grow resources
                4. more than simply Replica, a TiFlash node can host multiple regions from different groups
                5. To transform row-wise data into column-wise data for TiFlash
                    1. Raw logs => Compact Logs => Decode tuples removing redundant => Transforming to columnar
                    2. Log replication introduces asyc delay from TiKV to TiFlash, as tested usually < 1s
            2. Multi-raft to replicate data
                1. The good side is
                    1. metadata can be pushed down from central server to these small paxos groups to manage
                        1. PD (placement driver) has no persistent state, unlike Ceph etc using central Paxos group to persist metadata
                           PD gather metadata on startup from TiKV nodes mantaining paxos groups 
                    2. Paxos group can extend functionality by adding extra learner node, e.g. TiFlash
                2. The bad side is
                    1. it seems 3-replica is not enough for form a paxos group
                    2. many small paxos groups, massive heartbeats, need condense
                    3. Handling missing log entries and lagging paxos secondaries are tricky (e.g. reading secondary hits stale data)
            3. needs to implement SQL engine, including the Query optimizer
                1. TiDB supports rule-based and cost-based query optimization
                2. Storage operators are executed in TiKV, which is built atop RocksDB.
                    1. TiKV carries insight that SQL rows and indexes can be mapped to Key-Value pairs
            4. distributed transaction 
                1. implemented in Percolator, no need for central transaction table. Percolator.TLA github
                2. need datacenter centra timestamp oracle
                3. TiDB partitions data into small ranges called Region. Region supports split and merge
            5. TiSpark
                1. based on a Spark connector, but more improvements
                    1. push down computation natively to TiKV
                    2. simultaneously read multiple data regions
                    3. get index data from TiKB in parallel
                2. loading large data in transactions
                    1. need 2PC commit and lock tables
            6. Evaluation
                1. CH-benCHmark .. 100 warehouses take about 70 GB of memory
                    1. this is quite small amount of data, not reaching hundreds of TB
                2. Figure 7 (d). Latency of TiKV vs TiFlash is very small
                    1. TiFlash must be SSD. is it TiKV also SSD, or TiFlash too slow?
                3. Figure 9: TiSpark vs SparkSQL vs Greenplum vs PrestoDB
                    1. TiSpark is quite slow compared to others ..
                    2. SparkSQL usually outperforms TiSpark, because scanning compressed parquet files is cheaper
                4. Lay Replication Dalay to TiFlash
                    1. Table 4: under high load, more than 50% have longer delay than 100ms, more than 10% longer than 1s
                    2. delay time is related to data size
        3. questions
            1. TiFlash is a learner to paxos. Does it need to bound to one replication group?
                1. No, one TiFlash can host many regions from different groups
            2. Mananging massive heartbeat generated by the many raft replication groups?
                1. adjust heartbeat frequency according to how busy workload is a region
            3. Region couples storage ability and table management, compared to Azure Storage
                1. like BigTable, GFS manages storage partitions, i.e. regions of storage
                   and BigTable manages table partitions, not mapping / bound to storage partitions
            4. TiKV paxos replication group has different logs
                1. Paxos logs vs data trunk logs vs transaction logs.
                   How to consolidate them, and avoid double write issue?
                2. Efficient GC / Rearrange for data trunks mixed in paxos logs
            5. Multi-raft to replica data
                1. it's valid if you have 5 copies. but typical systems uses 3 replica, how to form a meaningful paxos group?
                2. if allow 2 out of 3 complete to ack in paxos, durability SLA is not met a 3-replica level
                3. extra overhead to handle holes in Raft group? some nodes may didn't catch up in a vote round
            6. Managing massive regions
                1. each region is 96MB max size by default, so small?
                2. whhat is the multi-dimensional resource scheduling / placement algorithms for regions?
                3. how to place regions to reduce cross node distributed transaction?
                4. how to reduce region down time when doing move/merge/split?
            7. TiFlash log replication
                1. How TiFlahs receives logs and replay to achieve transaction consistency?
            8. Delta tree
                1. so big .. the write amplification of DeltaTree (16.11) is greater than the LSM tree (4.74)

    2. Mesa: Geo-Replicated, Near Real-Time, Scalable Data Warehousing    [2014, 86 refs]
       https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42851.pdf
        1. interesting paper. Mesa serves Google advertising metrics. Features in Atomic update, incremental updates
           leverage exsiting Google infrasturctures to save implementation, Geo-replication, online schema change
           and interestingly using delta version diversity to mitigate data corruption issues
        2. highlights
            1. leveraging Google infrastructures to quickly build the distributed multi-regioin DB
                1. Colossus (next generation GFS) for persistency
                2. BigTable and Spanner to manage the metadata
                3. MapReduce to batch process metrics updates
                4. MySQL, F1, and Dremel for SQL query, while Mesa query server provides a limited primitives
            2. data organization
                1. example query
                    "How many ad clicks were there for a particular advertiser matching the keyword 'decaf' during the first week of
                    October between 8:00am and 11:00am that were displayed
                    on google.com for users in a specific geographic location using a mobile device?"
                2. dimensional attributes (keys) and measure attributes (values)
                3. production Mesa contains 1000+ tables, many of which have hundreds of columns
                4. each Mesa table has one or more table indexes
                5. row blocks, inside with transposed to columnar format and compressed
                    1. compression algorithm selection
                        1. "we emphasize the compression ratio and read/decompression times
                            over the cost of write/compression times when choosing the
                            compression algorithm"
            3. Atomic update - transaction update to multiple rows
               Incremental update - change value in existing rows
                1. Mesa applies updates in batches, frequency at every a few minutes
                2. to enforce atomic update, Mesa uses multi-version. updates applied in order of version.
                   ensuring always complete and update entirely before moving to the next update
                3. the ordering constraint allows Mesa to support inverse action to "fix" incorrect facts
                    1. e.g. Fraudulent clicks are offset by negative facts.
                4. versioned data are organized in two level delta compaction policy
                    1. Base version, update singletons version, cumulative versions small step merged
                    2. Once a delta is created, it is immutable
                5. Update / Maintenance subsystem
                    1. various background operations such as loading updates,
                       performing table compaction, applying schema changes,
                       and running table checksums, and GC
                    2. managed by a Conttroller / Worker framework
                        1. the Controller is the exclusive writer of the table metadata in BigTable
                        2. using MapReduce to parallelizing different workers
                        3. the Controller / Worker framework can restart without impacting user
                    3. to evenly distributed partitions across MapReduce
                        1. See "4.2 Parallelizing Worker Operation". Mesa worker samples every s-th row key
                    n. Questions
                        1. How does update maintenance control the delay deadline required by users?
                6. Query subsystem
                    1. Mesa provides limited primitives, using MySQL/F1/Dremel for full SQL query
                    2. Mesa ensures latency/throughput by labeling the workload and do isolation and prioritization
                    3. Query servers are organized into multiple sets, a set can upgrade, while another set keep serving
                    4. Mesa prefers to direct queries over similar data to a subset of query servers
                        1. to leverage in-memory prefetchinig and caching
                        2. on startup, each query server registers the list of tables it actively caches
                           i.e. the global locator service, also used by clients to discover query server
                        3. Mesa query server aggresively prefetch data form Colossus
                    5. scan-to-seek, using index to skip unnecessary (A = 1, B < 2)
                    6. resume key, if a query server becomes unresponsive, client and resume from another server
            4. Multiple geo location distribution
                1. only critical metadata is sync replicated, application data is async replicated
                    1. the version databse consistency is built atop Paxos
                2. the committer enforces all tables are update, using versioning
                    1. updates are applied in batches, Mesa does not require any locking between queries and updates
                3. mitigating data corruption problem
                    1. each Mesa instance in different datacenters manages delta versions independently, even they server same data
                        1. using this diversity to guard against faulty machines and human errors. interesting
                    2. global offline checks for index and data consistency 
                        1. each Mesa instance computes a strong row-order-dependent checksum and a weak row-order-independent checksum
                           for each index at a particular version,
                       2. and a global component verifies that the table data is consistent across all indexes and instances
                    3. if all instances are corrupted, Mesa can restore to an older version
                    4. a faulty component such as a floating-point unit on one machine can be extremely hard to diagnose
                        1. Overcoming such operational challenges remains an open problem
                4. datacenter has planned outage, without Geo-Repliication, Mesa has to perform laborious migration to another datacenter
            5. Online schema change for lage number of tables
                1. naive method: make a separated copy, replay any updates, switch the schema
                    1. linked schema change is not applicable to some cases, e.g. a schema change reorders key columns, or re-sorting data
                        1. then fallback to naive method
                2. linked schema change
                    1. treat old and new schema as one, handles conversion to new schema at query time on the fly
                3. The assumption is wrong the schema change is rare. Actually schema change is constant, due to application evolving

7. readings: CockroachDB paper
    1. CockroachDB: The Resilient Geo-Distributed SQL Database    [2020, 5 refs]
       https://dl.acm.org/doi/pdf/10.1145/3318464.3386134
        1. Very good paper.
           Opensource distributed relational database similar with TiDB. While TiDB features in HATP TiFlash,
           CockroachDB features in geo-distribution, serializable isolation, commit wait like Spanner.
           Both DBs use Raft to replicate data, and build storage layer upon RocksDB.
           The paper features more in detailed transaction implementation how it works
        2. highlights
            1. Geo-distributed data placement policies
                Replicas - partitioned into region, losing region losing data
                Leaseholders - paxos leader and secondaries at different regions, overhead on write cross region
                Duplicated Indexes - geo-replicate indexes across region to speed up queries
                1. the design is quite simple but as paper said very practical and useful
            2. Distributed transaction
                1. mainly see Parallel Commits. Using write intents as locking and staging value
                    1. after Tx committed, reader consider write intent as regular value, reader delete intent metadata to make it visible value
                    2. if Tx is found pending, reader blocks. If Tx is in STAGTING (parallel commit), reader attempts abort Tx
                2. unlike snapshot isolation whose read timestamp can drift older than write timestamp.
                   CRDB's serializable isolation ensures read timestamp and write timestamp are same
                    1. because CRDB uses serializable isolation, it more uses permissive locking
                    2. A write at Timestamp a cannot perform if already a read on high Timestamp b
                        1. The write Tx needs to advance timestamp past Timestamp b
                        2. Similarly, A write running into a committed value at higher Timestamp, the write Tx needs to advance Timestamp past it
                        3. Advaning Timestamp as above causes "Read Refreshes"
                            1. read timestamp must advance to match commit timestamp. to maintain serializable isolation
                            2. advacing read timestamp from Ta to Tb > Ta is possible, if can prove none data changed from Ta to Tb
                                1. otherwise transaction needs restart
                                2. to validate "not changed". Tx maintains read set, and it re-scan read keys again to determine change
                3. follow read constaints. to read from paxos secondaries
                    1. if a follower read at timestamp T is to be served, the leaseholder must no longer be accepting writes for timestamps T′ ≤ T
                        1. The "closed timestamp", aggregated as node level for efficiency
                    2. and the follower must have caught up on the prefix of the Raft log affecting the MVCC snapshot at T
            3. Hybrid-Logical Clock
                1. HLC is a combine of 500ms wall clock internal + self-incremental logical clock, causal-consistency
                    1. HLC provides self-stablization, by network gossiping, HLC should converges across nodes
                        1. paper didn't provide guarantees of converge
                    2. because the HLC is providing causal-consistency, which is weak
                        1. "Note that CRDB does not support strict serializability because there is no guarantee that the ordering of transactions
                            touching disjoint key sets will match their ordering in real time"
                2. commit wait - like Spanner.
                    1. called Uncertainty Intervals, max clock offset
                    2. CRDB maximum clock offset bounds must be respected
                        1. if violated, rnage leaseholders have extra safeguards. See section "4.2"
                        2. however, "clock skew outside of the configured clock offset bounds
                                    can result in violations of single-key linearizability between
                                    causally-dependent transactions"
                        3. to reduce likelihood of the above happen (only to reduce, not to guarantee safety?)
                            1. nodes periodically measure clock offset, and self-terminate if exceeds configured max offset by >80%
                                1. question: only self-terminate when *already* exceeds 80% max offset? how can this guarantee transaction safety ..
            4. Query exection, some interesting pieces
                1. "At the time of writing, only read-only queries can execute in distributed mode"
                    1. OK .. so bad ..
                2. "thus pushing down filters, joins, and aggregations as close to the physical data as possible"
                3. vectorized execution engine .. "data from disk is transposed from row to column format as it is being read from
                                                    CRDB’s KV layer, and transposed again from column to row
                                                    format"
                    1. vectorized execution was supposed to be very fast very lightweighted.
                       question: now the row->column->row transition seems wasted the benefit, so much overhead?
            5. Misc
                1. Ranges are ~64 MiB
                    1. reduce ranges can reduce the time moving across nodes doing load balancing
                2. Raft - Reducing the Chatter
                    1. similar with TiDB. Rafe replication for data ranges needs to reduce the heartbeats
                3. why not snapshot isolation along with serializability?
                    1. "we initially expected that offering just snapshot isolation by
                        removing the check for write skews would be simple. However, this proved not to be the case"
                4. "so we recommend that all production-grade Raft-based systems use Joint Consensus instead"
                5. "CRDB implements the solution used by F1", F1's famous online schema change.
            n. questions
                1. compared to TiDB, CRDB's SQL layer is coupled with KV storage on same node.
                   Though compared to Azure Storage, TiDB's table layer coupled with KV storage on same node already.
                2. "Replication is 3-ways", Raft replication .. how 3-replica paxos ack-back when 2 promises 3-replica durability?
                3. it's curious CRDB introduces Hybrid-Logical Clocks. It means CRDB wants to bring in clock uncertainty in design at Day 1?
                    1. and according to paper, CRDB requires configs a max clock offet.
                       Max clock offset must be repsected. CRDB cannot guarantee it safely well. And if violated, inconsistency can happen
                    2. and why also introduced the causal-consistency logical vector clock stuff ..
                       OK .. it must be Spanner a very large geo-distributed database that needs these stuff to reduce sync cost
                        1. compared to TiDB focusing on in-datacenter use, TiDB clocking is much more simplified
                4. when intra-datacenter deployment, it seems unwise to pay for commit wait each time ..
                    1. more customer cases are simple 1-DC. is the understanding correct?
                5. "3.3.3 Write-write conflicts" if two Tx trying to lock their set of keys (by write intents)
                   it seems quite easy Tx1 locked Key1 trying Key2, Tx2 locked Key2 trying Key1 => deadlock
                    1. the paper mentioned deadlock detection.
                       but Tx latency then depends on how efficient it can detect deadlock

        3. Parallel Commits: An Atomic Commit Protocol For Globally Distributed Transactions
           https://www.cockroachlabs.com/blog/parallel-commits/
            1. very good. major improvement on distributed transaction state of art
            2. highlights
                1. the two rounds of consensus mentioned
                    1. round 1: each write intent of the write key needs to be replicated
                    2. ruond 2: change transaction record in the transaction table to COMMITTED state, needs to be replicated too
                2. Parallel Commit
                    1. round 1: same. and additionally change transaction record to STAGING state
                        1. STAGING means
                            1. Tx has no more new write keys
                            2. writing data is in process or completed. transaction is either in process or committed
                    2. an other transaction, Tx2 or called Observer in article, needs additionally to
                        1. determine whether Tx in STAGTING state is truely committed
                        2. this involes verifying each of the Tx's write keys
                        3. Tx's write keys by design are tracked in its transaction record along with STAGTING state
                    3. about the cost of "verifying" each Tx's write key
                        1. it is called "Status Recovery Procedure"
                        2. expensive, but transaction coordinator will asynchronously mark transaction records as COMMITTED as soon as they can
                            1. also, CockroachDB periodically send heartbeats to their transaction record, to find the stuck ones
                        3. STAGING "verification" is very rare, only hapepns when transaction coordinator dies, so that why it is called "Status Recovery Procedure"
                3. Questions
                    1. Percolator looks a bit similar
                        1. round 1: write intent is written to each key in parallel.
                           round 2: Tx commits if key primary is updated to committed.
                        2. it's the next Tx2 that needs to do the extra "verification" about how previous Tx commits, Tx2 needs to poll the key secondaries and key primaries
                        3. Percolator has no central transaction table nor the transaction record
                            1. I didn't Percolator to merge round 1 and round 2 now, but the protocol should be able to update to Parallel Commit version
                    2. Overhead of observer polling each writing key in "Status Recovery Procedure"
                        1. this should be able to made faster but caching status in memory.
                           Recent Tx status is small

            n. related
                1. Pipelining Consensus Writes to Speed Up Distributed SQL Transactions
                   https://www.cockroachlabs.com/blog/transaction-pipelining/
                    1. issue write intents in parallel but no wait, manage async visibility with "pipeline dependency"
                    2. highlights
                        1. timestamp drifts in snapshot vs serializable isolation
                            1 snapshot isolation "allows a transaction's read timestamp and its write timestamp to drift apart"
                            2. but CockroachDB, "However, at a serializable isolation level, a transaction must read and write at the same timestamp to prevent anomalies like write skew"
                                1. Questions
                                    1. Serializable potentially creates more Tx aborts. I think that's why CockroachDB choose to permissive concurrency control
                        2. what is the change?
                            1. "we realized that we could begin writing intents immediately but don't actually need to wait for them to finish before returning a result to the client"
                            2. "we can push the entire consensus step out of the synchronous stage of statement execution"
                            3. Transaction commit finish requires
                                1. all write intents passed consensus replication
                                2. transaction record is updated and passed consensus replication
                        3. Read-Your-Writes
                            1. this Tx should see itself write intents
                                the next Tx2 should be able to see Tx's write intents when Tx succ
                            2. everything is async, so it is managed by "pipeline dependency"
                    3. look pretty related
                            Allow a Tx1 to speculatively read uncommitted versions of another Tx2.
                            this needs to track Tx1's read dependencies to Tx2
                       mentioned in  "An Empirical Evaluation of In-Memory Multi-Version Concurrency Control" Section 3.5
                        1. CRDB descripts it from the write perspective, but if you allow read to read write intents and track dependency, these techniques look pretty the similar

                2. Improvements on Percolator algorithm
                   http://oceanbase.org.cn/?p=195 - 两阶段提交的工程实践 - 郁白
                    1. good article. it's valuable to find improvement points on a well-famed transaction implementation Percolator
                    2. highlights
                        1. "而在事务执行过程中其他被修改的record里面记录primary record的key"
                            1. "这里我觉得priamry record保存单独的表中更优雅，否则priamry record被用户删除的话，并不好处理"
                        2. "对存储引擎的读写只能在一次RPC提交，使得加锁、修改、提交都必须是一次bigtable的提交操作，延迟代价是巨大的"
                            1. "commit时仍然要等待primary record持久化事务状态成功后，参与者才能进行commit，这一次延迟不可避免"
                                1. can be improved by Parallel Commit
                            2. so https://github.com/pingcap/tla-plus/blob/master/Percolator/Percolator.tla uses lock(c) for Prewrite(c)
                               it's essentially merging lock and change .. similar like Write-intent itself acts like a lock.
                            3. "行锁和数据修改为内存操作，避免持久化的代价" store in memory is OK
                                1. "简化协调者为无状态逻辑" not necessarily to persistent in BigTable everytime
                                2. "减少2PC执行关键路径上的持久化和RPC次数"
                        3. "Commit阶段：协调者收到所有参与者应答prepare成功的消息后，即向客户端返回事务提交成功；对于每个参与者，当它确认所有参与者都prepare成功后，将本地事务提交并释放行锁等资源，并异步的持久化一条commit日志，然后向其他参与者发送commit成功的消息。"
                            1. This is pretty much similar with Parallel Commit. article published on "2016年9月23日"
                            2. "因此协议全程只有 一次RPC交互延迟+一次日志持久化延迟"

8. readings: LegoOS paper and CMU 15-721 papers
    1. LegoOS: A Disseminated, Distributed OS for Hardware Resource Disaggregation    [2018, 78 refs, OSDI best paper]
       https://www.usenix.org/conference/osdi18/presentation/shan
       https://www.youtube.com/watch?v=KJqYHuL59_s
       https://blog.acolyer.org/2018/10/22/legoos-a-disseminated-distributed-os-for-hardware-resource-disaggregation/
       http://legoos.io
        1. interesting. disaggregate hardware including memory, GPU, disks, CPU, even cache into datacenter.
           decompose OS component into "monitors" running on these smart devices.
           This can be a future trend .. but need more large scale prototyping
        2. highlights.
            1. Disaggregation
                1. move hardware components out of machine box
                   now we have disks, soon we have memory, GPU, FPGA out of machine.
                    1. more smart and heterogeneous computing devices help the trend
                2. OS components are broken down into "monitors", running on disaggregated devices
                    1. smart devices can help
            2. Two-Level distributed resource management
                1. a key issue this paper targeting the resource utilization in datacenter
                2. other key challenges targeting in this paper
                    1. It is difficult to add, move, remove, or reconfigure hardware components after they have been installed in a server
                    2. It creates a coarse failure domain – when any hardware component within a server fails, the whole server is often unusable
            3. related technologies to support
                1. Rapidly growing networks speeds
                2. Network technologies such as Intel OmniPath, RDMA, and NVMe over Fabrics
                3. more smart devices suitable for pooling: GPGPUs, TPUs, DPUs, FGPAs, NVM, and NVMe-based SSDs
                4. smart devices: hardware devices are incorporating more processing power. offload OS functions
        n questions
            1. really needed and looking forward a prototype datacenter / OS / hardware link
            2. disaggregated hardware components and OS components will eventually need higher interconnect speed
               and the need for speed must trigger different layer of networking technology needed.
               because of the layered needs, the interconnect cannot be flat, it cannot be fully disaggregated
               but the resource pooling, scale-out of the machine box should be feasible and interesting

    2. Everything You Always Wanted to Know About Compiled and Vectorized Queries But Were Afraid to Ask    [2018, 34 refs]
       https://www.vldb.org/pvldb/vol11/p2209-kersten.pdf
        1. Explained how data-centric code generation vs SIDM vectorization work. thorough testing.
           more future hybrid code generation + vectorization approaches waiting explore.
           Useful. the evaluation methodology can be learned for evaluating any CPU centric workload
        2. highlights
            1. technologies
                1. old "Volcano-style iteration model": pull interface. "next" returns one tuple.
                    1. i.e. "a-tuple-at-a-time" model
                2. vectorization: pull interface. each "next" call fetches a block of tuples instead one. execute by SIMD.
                    1. VectorWise, now Actian Vector, previously the X100 project for MonetDB
                3. data-centric code generation
                    1. pioneered by HyPer
                    2. push-based interface (produce and consume)
                        1. "push" results in leaf-to-root traversal in query
                           while "pull" interface dose root-to-leaf traversal
                    3. generate code specialized for data types of the query
                       fuses all operators in a pipeline of non-blocking relational operators into a single (potentially nested) tight loop
                       This generated code can then be compiled to efficient machine code (e.g., using the LLVM)
                    4. has extra overhead to generate compiled machine code in runtime
                        1. or using C++ templates heavily to generate code - yielding exponential code size growth
            2. evaluations & methodologies
                1. we implemented a compilation-based relational engine and a vectorization-based engine in a single test system (available at [16])
                    1. https://github.com/TimoKersten/db-engine-paradigms
                    2. Typer - code generation
                       Tectorwise (TW) - vectorized engine
                2. what is evaluated
                    1. TPC-H benchmark: Q1, Q6, Q3, Q9, Q18
                    2. total runtime,
                       CPU cycles, instruction count, instructions per cycle,
                       L1 miss, LLC miss, branch miss, Memory stall cycles
                       Tectorwise Vector Size effects
                       Multi-threaded execution
                       Different hardware: e.g. Intel Skylake X vs AMD Threadripper
                    3. apply a small fix and see how sensitive the performance change to validate our findings
                3. interesting findings
                    1. Compilation-based engines have an advantage in calculation-heavy queries,
                       whereas vectorized engines are better at hiding cache miss latency, e.g., during hash joins
                    2. Q9: join (build: 320 K entries, probe: 1.5 M entries). Vectorize is 32% faster than Code generation
                        1. They have similar cache miss chances. But,
                            1. because Vectorize has simpler scan in hash probing loop,
                               CPU can do more out-of-order execution to hide the Memory stall latency
                            2. Code generation fused more operations resulting in the more complex loop.
                               Less out-of-order, and more expensive branch miss
            3. hybrid models combining vectorization and code generation
                1. Peloton: Relaxed operator fusion for in-memory databases: Making compilation, vectorization, and prefetching work together at last    [2017, 45 refs]
                   http://www.vldb.org/pvldb/vol11/p1-menon.pdf
                    1. "However, there are also cases where it would be better to explicitly break a single pipeline into multiple fragments
                          for example, in order to better utilize out-of-order execution and prefetching during a hash join. 
                       This is the key insight behind Peloton’s relaxed operator fusion [26] model,
                          which selectively introduces explicit materialization boundaries in the generated code.
                       By batching multiple tuples, Peloton can easily introduce SIMD and software prefetching instructions [26].
                          Consequently, Peloton’s pipelines are shorter and their structure resembles vectorized code (see Figure 13).
                       If the query optimizer’s decision about whether to break up a pipeline is correct (which is non-trivial [24]),
                          Peloton can be faster than both standard models"
                    2. highlights
                        1. Figure 5 and Figure 6 illustrated how the algorithm works
                            1. the processing pipeline is broken into Stages. each stage can do SIMD vectorization
                            2. across Stages, input and output passing are by TID vector ant bitmask vectors suitable for cache/register size
                                1. using SIMD compare and SIMD Permute, SIMD Masked Store instructions that work with bitmask vectors
                            3. the how it works look pretty similar with "AnalyticDB: Real-time OLAP Database System at Alibaba Cloud"
                               which is passing row id in a vector and do the filtering (e..g Figure 11)
                        2. key problems to solve in paper
                            1. "From the results shown in Fig. 4, we see that SIMD probes utilizing the vertical vectorization technique performs worse than tuple-ata-time probes with prefetching, even when the hash-table is cacheresident"
                            2. "What is needed is the ability for the DBMS to tactfully materialize tuples through prefetching at various points in the query plan — to enable vectorization and exploit inter-tuple parallelism — and otherwise fuse operators to ensure efficient pipelining"
                        3. others
                            1. combining SIMD vectorization, code geneation, memory prefetching.
                            2. concepts: pipeline breakers, operator fusion, Group prefetching
                            3. github project: https://github.com/cmu-db/peloton
                    n. related materials
                        1. In-Memory DBMS 『Peloton』技术简述 - 灰墙 - explaining the paper
                           https://zhuanlan.zhihu.com/p/51588155
                            1. "为了达到物化的目的 把pipeline分为多个阶段 每个阶段内有多个operation融合在一起
                                管道中各阶段通过缓存中的驻留向量进行通信
                                由于ROF只有一个活动阶段 则可以保证输入、输出向量都在CPU的高速缓存
                                  * ROF是a tuple a time 与SIMD之间的混合体
                                ROF与SIMD最大的区别：
                                  * ROF总是向下一个阶段提供完整的向量，而SIMD则是可选择限制输入向量的
                                  * 其次ROF支持跨多个序列operation的向量化，而SIMD则在单个operation中运行"
                            2. "DBMS必须提前足够多时间来预取，足够抵消内存延迟的时间(当然这部分时间与其他有效的计算相互重叠) 不可避免的是存在预取的开销
                                如果我们在单个元组中预取数据 这并没有效果
                                    因为单个元组中各个阶段 是相互依赖的 如果知道了这个元组中的下一个指令地址 那么就来不及获取内存延迟
                                    另一方面 积极预取也会认为高速缓存污染和浪费的指令而损失性能
                                在所有需要的数据大于缓存的input阶段加上stage
                                    这样可以确保启用预取的operation接收到完整的输入元组 使得其能重叠计算内存访问"
            4. others
                1. "One advantage of the push model is that it enables DAG-structured query plans (as opposed to trees), i.e., an operator may push its output to more than one consumer [27]
                   Push-based execution also has advantages in distributed query processing with Exchange operators,
                      which is one of the reasons it has been adopted by Virtuoso [8]"
                2. "One exception is Hekaton [12], which uses pull-based compilation.
                      An advantage of pull-based compilation is that it automatically avoids exponential code size growth for operators that call consume more than once"
            
            n. related materials: distributed hash join
                1. An evaluation of join-strategies in a distributed MySQL plugin architecture    [2019, 0 refs]
                   https://ntnuopen.ntnu.no/ntnu-xmlui/bitstream/handle/11250/2625827/no.ntnu%3Ainspera%3A2438786.pdf
                    1. summarizing distributed joins existing arts before designing the MySQL plugin
                    2. highlights
                        1. join methods
                            1. Distributed hash-join
                            2. Distributed sort-merge join
                            3. Semi- and Bloom-join
                        2. peer works
                            1. ClustrixDB
                                1. table column indexed by hash value. hash already present when hash-joining
                                2. table A whose primary key attends join do the filtering on node and send data to table B nodes
                            2. CockroachDB: The Resilient Geo-Distributed SQL Database - Figure 3
                               https://dl.acm.org/doi/pdf/10.1145/3318464.3386134
                                1. data is shuffled to each node and do filter locally and then send to a gateway node to merge
                            3. Google Spanner
                                1. data redistribution strategy to reduce inter-traffic
                                   only send to needed shards
                                2. retrieve only needed rows in batches, and do a distributed union
                                3. CockroachDB similar

                2. Track Join: Distributed Joins with Minimal Network Traffic    [2014, 73 refs]
                   http://www.cs.columbia.edu/~orestis/sigmod14II.pdf
                    1. Interesting paper. selective broadcast, tuple migration, if optimally scheduled destination and source,
                       can reduce the network transferred bytes than distributed hash join
                    2. highlights
                        1. Grace hash join - piror art
                           https://zhuanlan.zhihu.com/p/35040231
                            1. use hash partitioning into shared-nothing sub-problems that
                               can proceed locally per node and fully in memory (no spill to disk)
                            2. the data from two tables are partitioned by the same hash function
                               so jointable keys must be in the same parititon, sub-problem is localized
                            3. good zhihu article, it illustrated different hash joins
                               如何在分布式数据库中实现 Hash Join? - OceanBase: https://zhuanlan.zhihu.com/p/35040231
                                1. In-Memory Hash Join
                                2. Grace Hash Join
                                3. Hybrid Hash Join
                                    1. probe while doing the initial partition scan
                                       hit as much as it can in the memory
                                        1. i.e. hybrid in-memory and grace hash join

                        2. main algorithm
                            1. participants
                                1. node R, S holding the data partitions
                                2. node T collecting info, doing schedule, and sending key commands and node location info to R, S
                                    1. there can be many T nodes. R, S can send key corresponding hash(key) T node
                                       only need to make sure the same key sends to the same T node
                                        1. the algorithm evaluates each key independently,
                                           there is no cross-key information leveraged
                                    2. node T can colocate at node R, S. so this can reduce some transferred bytes
                            2. 4-phase track join
                                1. R, S: send all key in own partition to T
                                2. T: calculates optimal migration schedule, and whether R broadcast to S or vice versa
                                3. R, S: execute the migration commands send by T
                                4. R, S: execute the broadcast from R to S or vice versa
                                5. R, S: commit ack back to parent, if pieced together complete joined tuple for a key
                            3. optimal scheduling
                                1. T compares "migrate S & broadcast R" vs "migrate R & broadcast S"
                                2. per "migrate S & broadcast R", find which nodes to migrate
                                    1) migration dest doesn't affect network cost, so only care about source node
                                    2) exclude node with max |Ri|+ |Si| from source node (max tuple size on node)
                                    3) iterate though each node, evaluate gain. add to source node set if gain is positive
                                    4) Any S node not in migration source node set, can be used as destination ds.
                            4. other
                                1. the 4-phase track join is a hybrid of hash join + pure broadcast
                                   the hash join essentially is doing migration, by migrating to hash(key) node
                                    1. so, this paper algorithm can be thought as balancing hash join vs pure broadcast
                                       to obtain the optimal scheduling.
                                2. 4-phase track join degenerates to hash join in some cases. i.e.
                                   all tuples are migrated to the node of max |Ri|+ |Si|
                        3. hidden cost
                            1) partition nodes R, S need to send all key information to scheduler nodes T
                            2) T needs to send scheduled keys and node location information to R, S
                           besides
                            1) the algorithm mainly focus on reducing network transfer bytes
                               this may not be (the only) bottleneck of distributed hash join
                            2) as paper mentioned, T needs extra CPU to find optimal schedule
                        4. some possible further improvement can be
                            1) cross key information is not leveraged. currently R, S can send to any hash(key) T
                            2) migration phase and broadcase phase can execute in parallel

    3. An Empirical Evaluation of In-Memory Multi-Version Concurrency Control    [2017, 72 refs]
       http://www.vldb.org/pvldb/vol10/p781-Wu.pdf
        1. very good paper. the paper targets in-memory DB but is generally good for understanding each aspects MVCC
           implemented in Peloton: https://pelotondb.io/
        2. highlights
            1. Concurrency control protocol
                1. tuple fomrat: txn-id, begin-ts, end-ts, pointer, ..., columns
                2. MV2PL - Two-phase Locking
                    1. MV2PL records reads with its read lock for each version. Hence, a transaction performing a read/write on a tuple version will cause another transaction to abort if it attempts to do the same thing on that version
                3. MVTO - Timestamp Ordering
                    1. MVTO instead uses the read-ts field to record reads on each version
                    2. Transaction T creates a new version Bx+1 if (1) no active transaction holds Bx’s write lock and (2) Tid is larger than Bx's read-ts field
                4. MVOCC - Optimistic Concurrency Control
                    1. MVOCC requires the DBMS to examine a transaction’s read set to validate the correctness of that transaction’s read operations.
                    2. This can cause starvation of long-running read-only transactions
                5. Serialization Certifier
                    1. Examples
                        1. PostgreSQL SSI - serializable snapshot isolation
                        2. The serial safety net (SSN)
                    2. Certifier protocols reduce aborts because they do not validate reads, but their anti-dependency checking scheme may bring additional overheads
                        1. general principle: rw / ww dependency checking using locking or timestamps generate unnecessary false aborts, compared to the minimal aborts necessary for serializability dependency graph. so we reduce the false aborts here
                6. more optimizations
                    1. Allow a Tx1 to speculatively read uncommitted versions of another Tx2.
                       this needs to track Tx1's read dependencies to Tx2
                        1. related: CockroachDB - Write Pipelining. They look like the similar techniques but RDB describes it from write perspective
                           https://www.cockroachlabs.com/blog/transaction-pipelining/
            2. Version Stoarge
                1. from Evaluation results, see Section 8. Foremost is that the version storage scheme is one of the most important components to scaling an in-memory MVCC DBMS in a multicore environment.
                    1. This goes against the conventional wisdom in database research that has mostly focused on optimizing the concurrency control protocols
                2. DBMS uses the tuples’s pointer field to create a latch-free linked list called a version chain
                    1. "it is not possible to maintain a latch-free doubly linked list"
                3. Append-only Storage
                    1. link header ponts from Oldest-to-Newest (O2N), vs Newest-to-Oldest (N2O)
                        1. N2O favors fast lookup latest version
                        2. but index or header pointer changes everytime a newer version updates
                            1. usually DB employs "logical pointers", a middle layer that provides a fixed location, mapping to the changing physical address
                        3. GC Cooperative Cleaning (COOP) only works with O2N.
                            1. when read traverse old to new versions, it GC expired ones
                4. Time-travel Storage
                    1. DB maintains the master version in main table, and other versions in a separated time-travel table
                5. Delta Storage
                    1. DB maintains master version and a sequence of delta versions in a separated delta stroage
                    2. delta version contains only changed field, rather than the entire tuple
                6. more optimizations
                    1. to reduce multi-thread contention, DBMS can maintain separate memory spaces for each centralized structure (i.e., tables, delta storage) and expand them in fixed-size increments
            3. Garbage Collection - GC
                1. Tuple-level GC
                    1. Background Vacuuming (VAC)
                        1. Background GC threads periodically scan and reclaimexpired versions.
                        2. more optimized
                            1. transactions register invalidated versions in a latch-free data structure
                               GC threads then reclaim expired versions using the epoch-based scheme 
                    2. Cooperative Cleaning (COOP)
                        1. No GC threads needed. Reads scan from O2N versions to reclaim expired
                        2. used in Hekaton. there can be "dusty corners" if some versions never scanned
                            1. use a complete GC like VAC to full scan reclaim
                2. Transaction-level GC
                    1. DBMS considers a transaction as expired when the versions that it generated are not visible to any active transaction
                       After an epoch ends, all of the versions that were generated by the transactions belonging to that epoch can be safely
                    2. works well with the transaction-local storage optimization
                        1. because the DBMS reclaims a transaction’s storage space all at once
                    3. downsides
                        1. DBMS tracks the read/write sets of transactions for each epoch instead of just using the epoch's membership counter
                3. more optimizations
                    1. coarse-grained epoch-based memory reclaim
                        1. only one active epoch
                        2. epoch acts as the coarse-grained unit to hold transactions then to a transaction's versions
                        3. when epoch is not active, and it and all older epochs have zero reference counts, OK to clean up the versions
            4. Index Management
                1. All MVCC DBMSs keep the database's versioning information separate from its indexes
                2. N2O requires the DBMS to update the primary key index every time a new version is created
                    1. Using Logical Pointers, an indirection layer, to reudce changes propagating the the index tree
                    2. Primary Key vs Tuple Id used in index pointing
                        1. primary key can be very large depends on the customer table
                3. Physical Pointers
                    1. only applicable for append-only storage
                        1. "When updating any tuple in a table, the DBMS inserts the newly created version into all the secondary indexes"
                4. index-only scans are not possible in a MVCC DBMS unless the tuples’ versioning information is embedded in each index
                    1. NuoDB reduces the amount of data read to check versions by storing the header meta-data separately from the tuple data
        n. related materials
            1. CMU 15-721 MVCC Slides
               https://15721.courses.cs.cmu.edu/spring2020/slides/03-mvcc1.pdf
            2. 论文笔记 [VLDB '17] An Empirical Evaluation of In-Memory Multi-Version Concurrency Control
               https://www.codercto.com/a/56534.html
            3. 每周一论文：An Empirical Evaluation of In-Memory Multi-Version Concurrency Control
                https://zhewuzhou.github.io/2018/09/29/Weekly-Paper-An-Empirical-Evalution-of-In-Memory-MVCC/
            4. 翻译 《An Empirical Evaluation of In
               https://www.dazhuanlan.com/2019/10/01/5d92ff51db40f/

9. readings: summarizing recent years new storage technology trends
    1. 2018 存储技术热点与趋势总结: https://zhuanlan.zhihu.com/p/34455548
       2020 存储技术热点与趋势总结: https://zhuanlan.zhihu.com/p/135188922
    
    2. brief outline
        1. Persistent memory: Many change in Storage, Filesystem, Database. A good guide: https://www.usenix.org/system/files/login/articles/login_summer17_07_rudoff.pdf
        2. Open-Channel SSD: Cloud vendors always want to customize more the hardware. Alibaba invested in Computational SSD (https://www.youtube.com/watch?v=_8gEmK1L4EY) (ScaleFlux corp.) to pushdown OLAP row filtering down to SSD.
        3. LSM-tree improvements: Now everyone knows GC is a problem. Dostoevsky tells how to analyze: https://www.youtube.com/watch?v=fmXgXripmh0
        4. VirtIO without Virt: Still open gaps in virtualizing new generation hardware. Need faster, e.g. NVM. Need capability, e.g. GPU.

    3. NVDIMM / Persistent memory changing storage system designs
        1. What are the real performances? An Empirical Guide to the Behavior and Use of Scalable Persistent Memory: https://www.usenix.org/system/files/fast20-yang.pdf
            1. True "Byte-addressable" unit is 256 bytes (XPLine). Multi-threading contention is notable (XPBuffer)

        2. How to program applications? Persistent Memory Programming: https://www.usenix.org/system/files/login/articles/login_summer17_07_rudoff.pdf
            1. DAX, CLFLUSH/CLWB/SFENSE, libpmem

        3. Databases? Managing Non-Volatile Memory in Database Systems: https://www.cc.gatech.edu/~jarulraj/courses/8803-f18/papers/nvm.pdf
            1. Single-level system (No DRAM, just persistent memory), vs DRAM + persistent memory.
            2. Hot/cold switching, buffer manager, logging & recovery, etc.

        4. Filesystem? NOVA: A High-Performance, Hardened File System for Non-Volatile Main Memories: https://storageconference.us/2017/Presentations/Swanson.pdf
            1. Log-structured, copy-on-write, NVDIMM native

        5. KV store? Reaping the performance of fast NVM storage with uDepot: https://www.usenix.org/conference/fast19/presentation/kourtis
            1. Hash index in DRAM, log-structured to NVM, IO access with SPDK.

        6. Indexing? A Comparison of Adaptive Radix Trees and Hash Tables: https://bigdata.uni-saarland.de/publications/ARCD15.pdf
            1. Fast in-memory index, usually ART, hash table
```
