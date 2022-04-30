---
layout: post
title: "Recent Paper Reading: DB, Storage"
tagline : "Recent Paper Reading: DB, Storage"
description: "Recent Paper Reading: DB, Storage"
category: "storage"
tags: [storage, paper, database]
---
{% include JB/setup %}

Search tags to find recommended papers: "(can be used as a) reference (architecture)", "very good", "good", "very interesting", "interesting", "very useful", "useful"

Papers about databases & storage

```
1. Casper: Optimal Column Layout for Hybrid Workloads    (2020 VLDB, 17 refs)
   https://www.youtube.com/watch?v=AsjqfidHNAQ
   https://stratos.seas.harvard.edu/files/stratos/files/caspervldb2020.pdf
    1. very good paper to model CRUD, point/range query, rand/seq read/write cost functions on how blocks are partitioned by partition size.
       innovative that by making partition size variable, and optimized upon workload, throughput can improve to 2x-4x
       the target scenario is in-memory DB, and hybrid reads/writes intensive but not very related to HTAP, updates are mostly in-place
       other interesting techniques are, ripple-insert, ghost values, and mapping partition problem into bit-vector optimization problem with off-shelf solver
    2. highlights
        1. column layout design space
            1. data organization: insertion order, sorted, partitioned
            2. update policy: in-place, out-of-place, hybrid
            3. buffering: none, global, per-partition
            4. questions
                1. I didn't see all aspects addressed in paper, e.g. out-of-place updating, buffering?
        2. insight into partitioning
            1. small partition size favors reads
            2. large partition size (i.e. few trailing partitions) favors updates
            3. ghost values (i.e. empty values in a partition to avoid ripple insert)
            4. ripple-insert algorithm: in-place update, rather than moving array, rippely shift last value in each partition to next
            5. questions
                1. large partition size is bad for reads? DB can have finer-grain index, rather than full scan
                2. HTAP is not much addressed in this paper? but partition sizes to hande read/write cost
                3. why a pointer read needs to scan entire partition size? DB can interchange pages
        3. modeling partition size and costs - this is the very good part
            1. the base variables
                1. the base tracking units are blocks, a vector 1/0 tracks if a block is the partition boundary
                2. access frequency is tracked by histogram, on blocks, for each read (point, range) and write (insert, delete, update) types
                3. rand/sed read/write cost are tracked as RR/SR/RW/SW, and measured by micro-banchmark
            2. modeling the cost
                1. see paper section 4.4 Cost Functions.
                   the bit vector can use II multiply to convert to partition size
                   each type of read/write operations are cost modeled
                2. the best partition size is viewed as a bit-vector optimization problem
                   solved with O^3 block count by off-shelf Mosek solver
                    1. how to handle scalble issue if too many blocks?
                        1. introducing column chunks, each chunk has fewer blocks
                        2. multi-core parallalism
                        3. larger block size
                3. ghost values
                    1. questions: too few talked about how ghost values are modeled and impacts
                4. SLA of update and read latency are also modeled and put into the bit-vector solver constraints
    n. related
        1. 《Optimal Column Layout for Hybrid Workloads》论文读后感 - 萌豆
           https://zhuanlan.zhihu.com/p/400225192
           1. the 2019 paper is ranked as a must read at CMU 15-721 2020

2. Taurus: Lightweight Parallel Logging for In-Memory Database Management Systems    [2021 VLDB, 0 refs]
   https://pages.cs.wisc.edu/~yxy/pubs/p189-xia.pdf
    1. good paper. simple but useful method to parallelize WAL, wich a vector clock to track dependency. vector clock can be further compressed.  
       opensourced at https://github.com/yuxiamit/DBx1000_logging
    2. highlights
        1. parallel WAL logging - a serial bottleneck for a parallel database
            1.tranditionally we can still parallel with
                1. partition the database, each partition runs an independent WAL.
                   Distributed transaction is needed and has overhead, e.g. Spanner
                2. log stripping, by running the DB on an comprehensive streaming system, e.g. CORFU logging
            2. But the technique is more needed for in-memory databases, which typically run a single instance on a powerful machine.
                1. The parallelism can further exploit one machine attached multiple disks to host log streams
        2. key design - LSN vector the vector clock
            1. the key challenge is to track Tx dependency across multiple log streams
            2. each log stream has an LSN, each Tx carries an LSN vector and writes to log entry
               the LSN vector is the LSN of each log stream. A Tx has LV means it is dependent on log entries smaller than LVi
                1. questions: what if Tx has no dependency on a log stream?
        3. key design - LSN vector compression
            1. old LV are not necessar,y only need to track active tuples in lock table
                1. maintain a global.PLV the global persisted LV, LV smaller than PSV-t can be removed
                2. in log entry, if LV's some component is too small, smaller than LPLV, we don't need to persist it 
                    1. "the anchor point"
    n. related
        1. VLDB 2021论文概述
           https://zhuanlan.zhihu.com/p/413463723
            1. "DBMS 通过写入一个持久性的 WAL 来实现故障恢复，这样的单一串行日志可能成为 in-memory 数据库的性能瓶颈。本文使用向量化的日志追踪事务之间的依赖关系，可以并行写入和回放日志。为了减少时间戳占用的空间，本文提出了时间戳压缩算法。可以与S2PL，OCC，MVCC等并发控制结合。"
        2. Silo-Speedy Transactions in Multicore In-Memory Databases阅读笔记
           https://zhuanlan.zhihu.com/p/448627690

3. Data Blocks: Hybrid OLTP and OLAP on Compressed Storage using both Vectorization and Compilation (2016 SIGMOD, 126 refs)
   https://event.cwi.nl/dbdbd2015/DBDBD-2015-slides-Harald-Lang.pdf
   https://db.in.tum.de/downloads/publications/datablocks.pdf
    1. HyPer in-memory DB. addressing the OLAP & OLAP impedance by introducing Data Block.
       Data Block further involves indexing, compression, query execution topics.
       This should be a different but very viable approach to solve HTAP problem, compared to TiDB's TiFlash, for in-memory DBs, - good paper
    2. highlights
        1. goals: HyPer in-memory DB, HTAP OLTP&OLAP, evicting cold data from memory to disk
            1. separating data into write optimized format (newer data, OLTP favor), and read optimized format (columnar, OLTP OK compressed, OLAP favor)
            2. not mention much whether cold Data Block is evicted to disk
                1. refer to LeanStore, also from HyPer team, to evict to disk
                2. this paper's main goal is to save memory via Data Block compression
            3. alternative approach is OLTP/OLAP separated, which however the merge operation O(n) is heavy. this is why HyPer is trying a different approach
                1. questions: is chunk hot data columnar or row-wise organized?
        2. key aspects
            1. hot/cold clustering: see the other paper below
            2. chunk - 64K tuples; data blocks - chunk after compression
                1. questions: can we leverage dynamic sized chunk size, from paper: "Casper: Optimal Column Layout for Hybrid Workloads"?
            3. novel PSMA lightweighted indexing, besides the SMA
                1. to further reduce range besides SMA's min/max
                2. PSMA consists of a lookup table that is computed when chunk is frozen to Data Block
            4. data block compression algorithms adaptive
                1. lightweighted, byte-addressable compression formats, point access compression, so OLTP can quickly access individual tuples
                2. adaptive
                    1. single value compression
                    2. ordered dictionary compression
                    3. truncation 
            5. SIMD, JIT, vectorized execution: Predicate Evaluation on data block
                1. avoid compile time bloat in JIT due to choosing different compression schemes
                   instead, use vectorized scans which remain interpreted and can be pre-compiled
                   i.e. scan Data Block uses pre-compiled vectorized scan. query processing still uses JIT-compiling
    n. related
        1. Data Blocks (HyPer) 论文阅读笔记
           https://zhuanlan.zhihu.com/p/449583289
            1. 为了减小内存占用，数据会被分为冷和热两部分，冷数据会被压缩以减少内存压力（且可以被 evicted 出内存），热数据不会压缩
               克制的使用了轻量级的压缩 (byte-addressable compression formats)。SARGable scan restrictions (i.e., =, is, <, ≤, >, ≥, between) 可以直接在这种轻量级压缩数据上进行比较
                1. 系统里数据先会被分为大小一致的 chunk，当一个 chunk 被认为是冷数据时，会被压缩成 read-optimized immutable Data Block (不可写)。如果这时候要 update 这个冷 Data Block 上的数据，会先把 Data Block 上的数据删掉 (mark with a flag)，再在热数据上插入一条新的。这样可以保证 OLTP 的性能。
            2. PSMA - Positional Small Materialized Aggregates
                1. 思考：PSMA 是不是只能用来加速 point query ？
            3. 然后是 Data Blocks 的压缩。其一大特点是每个 Data Block 内每一列的压缩算法可能都不同，它们会选用对自己数据最优的方式（最小化内存占用的方式）
        
        2. LeanStore 论文阅读笔记
           https://zhuanlan.zhihu.com/p/443809984
            1. LeanStore 是TUM 数据库组在 HyPer 纯内存数据库之后设计的一款 偏向大内存场景 但提供比纯内存数据库更好的 超物理内存数据量管理能力 的database
            2. 使用了改进的 BufferManager, 设计了一套更加轻量化的 page 替换机制
        
        3. Caching vs. Anti-Caching [缓存和反缓存]
           https://csruiliu.github.io/blog/20161218-cache-vs-anticache/
            1. "识别冷热数据并不是这篇文章的重点，有很多现成的算法解决了这个问题"
                1. HyPer's paper to categorize hot/cold data
                   Compacting Transactional Data in Hybrid OLTP&OLAP Databases    [2012, 72 refs]
                   http://vldb.org/pvldb/vol5/p1424_florianfunke_vldb2012.pdf
                    1. Hot/Cold Clustering
                        1. tracks temperature on virtual memory page granularity, attributes column-wise
                        2. update metrics via Access Observer component using a lightweight, hardware-assisted approach
                            1. exploiting Virtual Machine memory management tricks
                            2. In HyPer, we prevent memory pages from getting
                                paged out to the swap area by using the mlock system call.
                                Thus we can read and reset the young and dirty flags in
                                each observation cycle to monitor accesses to the database
                                with virtually no overhead
                        3. data is categorized as Hot->Cooling->Cold->Frozen
                            1. OLTP favors non-compressed data, while OLAP favors compressed data (no updates, full scans)
                            2. Cooling: Most entries remain untouched
                               Cold: Entries in a cold vector are not accessed
                               Frozen: Compressed, no in-place update

            2. Anti-Caching有两个优势，Fine-Grained Eviction和Non-Blocking Fetch
                1. Fine-Grained Eviction: 主要是可以提供更细粒度的evict机制，传统做法都是page-level，每次load和evict都是都是整个page，但是Anti-Caching可以提供tuple-level的load和evict就可以大大减低浪费
                2. Non-Blocking Fetch: 如果让操作系统的虚拟内存负责in-memory的页面调度，这个过程是对用户透明的，一旦放生页面确实，所有transcation就要停止，直到需要的page调度回memory才可以。Anti-Caching遇到页面确实会abort当前transaction，然后继续执行后续transactions直到，需要的数据调度从disk写会memory再restart已经abort的transaction
        
        4. fxjwind - Data Blocks: Hybrid OLTP and OLAP on Compressed Storage using both Vectorization and Compilation
           https://www.cnblogs.com/fxjwind/p/12576026.html
            1. Hybrid系统难点，在于AP和TP在很多方面，优化思路是矛盾的
                比如compression，对于ap可以提升查询性能因为降低带宽使用，但是对于TP反而降低了查询性能，因为查询的时候需要解压，而且影响索引
                所以大部分Hybrid系统的策略，都是提供read-optimized和write-optimized两部分
                但是这样明显不是很优雅，而且merge过程是个很重的操作
                所以这里提出的方案是，
                将关系表切分成固定大小的chunks，带轻量的压缩，不可变的datablocks
                最后再看下，如果使用向量化和JIT来提升hybrid查询的能力，

4. Mainlining Databases: Supporting Fast Transactional Workloads on Universal Columnar Data File Formats
   https://arxiv.org/abs/2004.14471
    1. Interesting direction. HATP tried using Columnar format (favors OLAP) to support OLTP
    2. Highlights
        1. // TODO
    n. related
        1. noisepage paper分享：基于column-storage实现的事务存储引擎
           https://zhuanlan.zhihu.com/p/351306672
            1. "这篇paper是CMU database group实现的self-driving database的系列paper的其中一篇，主要分享的是如何基于一个通用的列存格式来实现一个in-memory的HTAP系统"
            2. "HTAP从工业界目前的实现来看，除了HANA比较另类，基本都是一个行存用来服务TP，一个列存用来服务AP，更细分有2种策略，内部实现行转列，典型的代表是TiDB，用户自己做ETL来实现行列转换，例如Greenplum，TBase。noisepage的实现算是一种学术界的探索，在列存的引擎上同时实现AP和TP"
            3. "因为作者在这篇paper中，基于arrow的in-memory的列存做的实现" .. "这篇paper的核心是怎么基于arrow的列存格式，来实现一个TP的事务引擎"
               "但是从他对事务协议OCC的选择，并不是面向典型的TP：高并发，且冲突严重的场景"
               "典型的面向分析场景。综合来讲适合主要面向分析，但是具备完整事务能力的场景"

        2. VLDB 2021 论文推荐(续)
           https://zhuanlan.zhihu.com/p/424673206
            1. "本文是数据库网红 CMU database group 的 paper，介绍他们的 NoisePage（一个 self-driving database）如何快速将来自 OLTP 系统的数据转换成列存格式。其主要基于 Apache Arrow 来实现，Arrow 现在已经成了许多内存列存数据库的首选"

5. Scaling Replicated State Machines with Compartmentalization    [2021 VLDB, 3 refs]
   https://arxiv.org/abs/2012.15762
    1. very good paper as how to decouple the component responsibilities in paxos, scale out, and increase throughput
       Particularly, Acceptor Grid / Grid Quorum is interesting
    2. hightlights
        1. Compartmentalization is a general methodology to apply to protocols
            1. example is this paper
        2. Leader -> Proxy leader -> Acceptors - leader is bottleneck
            1. Leader couples log sequencing and message broadcasting. introduce proxy leader to take the later role
            2. Proxy leader needs f+1 to tolerate f node failures
        3. Acceptor grid - acceptor is bottleneck
            1. phase 1 - read quorum, phase 2 - write quorum. the correctness only needs read quorum (in every round) intersect with write quorum (in every round).
               read quorum don't need to interset with read qurum. so as write quorum
            2. form acceptors as a matrix. a row is a read quorum, a column is a write quorum.
            3. OK .. this is the [19] Flexible Paxos algorithm
            4. question
                1. what if r/w quorum has only 1 intersection, and the node went dead after accepted vote?
                    1. may be we can design to have more intersection nodes
                2. do leader needs all of the r or w nodes to all accept? I think yes
                3. how to maintain the availability, give nodes can fail, and we can left with a series of nodes with missing holes in log and each are inconsistent
        4. decouples read path from write path
            1. use Paxos Quorum Read, read doesn't need to involve leader.
            2. see Figure 7, this supports Grid Quorum / Acceptor Grid
            3. quorum read is necessary, as to implement linearizability
        5. Batcher and Unbatcher
            1. paxos can batch messages. Introduce Client -> Batcher -> Leader, the Batcher to decouple batch forming from leader
            2. Unbatcher, replica has to unbatch and send responses back to clients. introdce Unbatcher in middle for this
        6. related works
            1. PigPaxos substitutes direct leader-to-acceptor communication with a relay network
            2. Ring Paxos. Ring Paxos [32] is a MultiPaxos variant that decouples control flow from data flow (as in S-Paxos [10]) and that arranges nodes in a chain
            3. NoPaxos .. Each client sends commands to a centralized sequencer that is implemented on a network switch
            4. A Family of Leaderless Generalized Protocols. In [30] ..
            5. Sharding .. Every replica must execute every write. This creates a fundamental throughput limit
               However, if we are able to divide the state of the state machine into independent shards
        n. questions
            1. what if the bottleneck is at the replica executing writes? Paxos/Voting itself is light, but replicated state machine can be slow at executing
            2. after introduced so many roles .. probably we don't have as many machines. but if overlapping roles on same node, we go back to the beginning ..
    n. related
        1. VLDB 2021论文概述
           https://zhuanlan.zhihu.com/p/413463723
            1. 本文使用一系列的解耦操作提升MultiPaxos共识协议的可扩展性。
                1. Proxy Leader，解耦指令排序和广播，避免Leader成为瓶颈
                2. Acceptor Grid，解耦读写仲裁
                3. More Replicas，由于添加了Proxy Leader，增加更多的副本不会导致Leader成为瓶颈，同时每个副本负责的响应数量减少。
                4. Leaderless Read：解耦读写路径。写入像以前一样处理，但绕过领导者并使用 Paxos Quorum Reads (PQR)在单个副本上执行读取。 
                5. Batchers：批处理通过分摊处理命令的通信和计算成本来提高吞吐量，通过引入Batchers解耦指令排序和批处理。
                6. UnBatchers：在执行了n条命令后，副本（Replica）必须向n个客户端发送n条消息。因此，副本(就像没有批处理程序的leader)所遭受的通信开销在命令数量上是线性的，而不是在批处理数量上。通过引入一组至少f + 1的反批处理程序来解除这两个职责的耦合，副本负责执行批量命令，而反批处理程序负责将执行命令的结果发送回客户机。

        2. Columba M71 - Scaling Replicated State Machines with Compartmentalization
           https://nan01ab.github.io/2021/01/Compartmentalization-RSM.html
            1. useful summary

        3. Flexible Paxos: Quorum Intersection Revisited
           https://fpaxos.github.io/
           https://arxiv.org/pdf/1608.06696v1.pdf
           https://zhuanlan.zhihu.com/p/32757145
            1. very good paper. this is a theory breakthrough. The paper proves phase 1 quorum and phase 2 quorum only needs to intersect

6. Don't Hold My Data Hostage – A Case For Client Protocol Redesign    [2017, 20 refs, VLDB]
   https://www.vldb.org/pvldb/vol10/p1022-muehleisen.pdf
    1. From CMU 15-721 for database networking protocol. To improve speed of Result Set Serialization (RSS), or data export from DB.
       Compared to transfer CSV with netcat (`nc`), DBs are slower by > 10x.
       Solution for RSS: cut rows in chunk, then columnar compressed, based on PostgreSQL.
       Interesting paper. Looks like it found an optimization area that was previously missed by most DBs.
    2. highlights
        1. Problems with existing database Result Set Serialization
            1. PostgreSQL
                1. 每一行都是单独一条message，包含total length，每个field length
                   cons: 每一行的metadata数据量，大于实际存储的数据量。这些冗余的信息，也解释了为什么PG传输的数据较多
                   pros: 另一方面，这种简单的format，也减少了(de)serialization的cost，当网络不是瓶颈时，这种格式会降低传输时间，因为CPU消耗少
            2. MySQL
                1. metadata采用binary encoding，实际数据采用text encoding
                   行格式：3 byte数据长度 | 数据包序列号 | field长度 | field data
            3. Hive
                1. Hive和Spark SQL都使用thrift-based协议传输数据, Hive2开始使用columnar format形式
                   一个column中许多不必要的开销(stop/beign/mask)等，这些cost取决于结果集中的行数
                   每个field的开销是，length和NULL mask。其中NULL mask为每个值一个byte，浪费了很大空间
            4. MonetDB 
                1. MonetDB 是基于 text 的序列化格式, 虽然协议简单，但注意，二进制值转换为字符串返回开销不小
        2. Protocol Design Space
            1. Row vs Column Layout
                1. middle solution: cut rows in chunk, intra-chunk is columnar compressed
            2. Chunk Size
                1. large chunk size favors compression, but needs more client side memory to buffer
                    1. questions. OK, I think not that much buffer memory actually. 4MB compression ratio is already high enough
            3. Data Compression
                1. compression ratio vs CPU overhead
                2. transfer networking environment is depended
            4. Data Serialization
                1. customized vs protocolbuf
            5. String Handling
                1. Null-Termination：用一个0 byte标志字符串结尾
                     cons：client必须scan完当前整个字符串，才能知道下个字符串开始。
                   Length-Prefixing：字符串开头记录它的长度
                      pros：可以直接计算出下个字符串读取位置。
                      cons：需要额外空间存储长度，特别当大量小字符串时候。它可以通过varint prefix解决。
                   Fixed-Width：每个字符串都是对应SQL Type的固定长度
                      cons：理想情况下，字符串没有额外padding。但是对于varchar来说，大小不够长的字符串，也会引入额外padding。
        3. Proposed solution
            1. cut rows in chunk, then columnar compressed, based on PostgreSQL.
            2. NULL值处理：每个column数据之前都有bitmask来标志哪一行数据不存在。

    n. related materials
        1. Fedomn: Don't Hold My Data Hostage: A Case for Client Protocol Redesign
           https://zhuanlan.zhihu.com/p/451844958
            1. already summarized most of the paper.

        2. 卡比卡比: Don't Hold My Data Hostage: A Case for Client Protocol Redesign
           https://zhuanlan.zhihu.com/p/441979897

7. Integrating Compression and Execution in Column-Oriented Database Systems    [2006, 817 refs]
   https://web.stanford.edu/class/cs245/win2020/readings/c-store-compression.pdf
    1. From CMU 15-721 for database compression. Introduced "Late Materialization", by defining the operator interfaces to operate directly on compressed blocks.
       Also discussed and implemented typical compression/encoding algorithms for columnar DB. Extended C-Store.
       "Late Materialization" means to operate on compressed blocks, rather than decompress than operate. Now every columnar DB does this, and developed a spectrum of compression algorithms e.g. RLE - Run-length Encoding.
    2. highlights
        1. compression row-stores
            1. dictionary encoding, prefix-coding (e.g. Huffman encoding), frame of reference value
        2. different compression/encoding algorithms in choice for column-stores
            1. dictionary encoding - Cache-Conscious Optimization
                1. dictionary should be fit into CPU L2 cache, (and leave half space for other memory uses)
        3. 延迟物化 (Late Materialization): operators operate on compressed column data, rather than decompressed ones, and pass compressed blocks
            1. besides, "to the best of our knowledge, there has been no attempt to take advantage of some compression algorithms’ ability to represent multiple values in a single field to simultaneously apply an operation on these many values at once"
            2. minimizes operator code complexity while maximizing opportunities for direct operation on compressed data
                1. Table 1: Compressed Block API - this is the key contribution
                    1. isOneValue(), isValueSorted(), isPosContig();s getNext(), asArray(); getSize(), getStartValue(), getEndPosition()
                2. Figure 1 -> Figure 2: Reduce the coding complexity of joining N different compression algorithms
        4. Figure 10: Decision tree summarizing our results regarding the proper selection of compression scheme
            1. This is useful, and can be compared with "Column-Oriented Database Systems" below - no sort key requirement
            2. Are there moderate length runs?
                1. Yes - RLE
                2. No - Is the number of distinct value < ~50,000?
                    1. Yes - Is the column likely to be used in a position-contiguous manner?
                        1. Yes - Use Dictionary Encoding
                        2. No - Is the number of distinct values < ~50?
                            1. Yes - Use Bit-vector encoding
                            2. No - Use Dictionary encoding
                    2. No - Does the data exhibit locality?
                        1. Yes - LZ
                        2. No - Don't compress
                3. why "position-contiguous" diffs Dictionary encoding vs Bit-vector encoding above?
                    1. isPosContig(): returns whether the block contains a consecutive subset of a column (i.e. for a given position range within a column, the block contains all values located in that range)
                    2. a bit-vector (a non-position-contiguous list)
                    3. “Likely to be used in a position contiguous manner” means that that the column needs to be read in parallel with another column, so the column is not accessed out of order
                    4. questions: so .. still why? probably because bit-vector is for non-contiguous one, and thus everything left is put to dictionary encoding
        5. more key points
            1. it is generally beneficial to have low cardinality columns serve as the leftmost sort orders in the projection (to increase the average run-lengths of columns to the right)
            2. Sacrificing the compression ratio of heavy-weight schemes for the efficiency light-weight schemes in operating on compressed data
            3. optimizer needs to be aware of the performance implications of operating directly on compressed data in its cost models
    3. questions
        1. if we use RLE of one column, that means the column is maintained in sort order.
           other columns should be sorted in the same id order of the first column, otherwise we need an extra field to store row id mapping
           but how should other columns do compression? they are not in sort order of themselves, and cannot imply apply RLE.

    n. related materials
        1. [笔记] Integrating Compression and Execution in Column-Oriented Database Systems - Fu Zhe's Blog
           https://fuzhe1989.github.io/2021/01/08/integrating-compression-and-execution-in-column-oriented-database-systems/
            1. summarized most contents in the paper.

        2. Column-Oriented Database Systems - VLDB 2009 Tutorial - @ Stavros Harizopoulos, Daniel Abadi, Peter Boncz
           https://www.cs.umd.edu/~abadi/talks/Column_Store_Tutorial_VLDB09.pdf
            0. very useful course slides that summarize key papers in Columnar DB domain and the evolving history
            1. Integrating Compression and Execution in Column-Oriented Database Systems
                1. Bit-vector Encoding
                2. Dictionary Encoding
            2. other papers'
                1. Run-length Encoding (RLE)
                2. Frame Of Reference Encoding
                3. Differential Encoding
            3. What Compression Scheme To Use? - this is the good part, and the slides also demos each compression technique - Page 56
                1. Does column appear in the sort key?
                    1. Yes - Is the average run-length > 2
                        1. Yes - RLE
                        2. No - Differential Encoding
                    2. No - Are number of unique values < ~50000
                        1. Yes - Does this column appear frequently in selection predicates?
                            1. Yes - Bit-vector Compression
                            2. No - Dictionary Compression
                        2. No - Is the data numerical and exhibit good locality?
                            1. Yes - Frame of Reference Encoding
                            2. No - Leave data uncompressed,
                                1. Or, Heavyweight Compression, e.g. BZIP, ZLIB, LZO
            4. the Join algorithms for Columnar DBs
            5. vectorized execution

        3. 数据库学习资料（2022-03-18 更新） - 康凯森 - 编程小梦
           https://blog.bcmeng.com/post/database-learning.html

8. A1: A Distributed In-Memory Graph Database    [2020, 15 refs, Microsoft]
   https://www.microsoft.com/en-us/research/publication/a1-a-distributed-in-memory-graph-database/
    1. General purpose graph database built atop FaRM, used by Bing for knowledge graph. Good work compared to Facebook TAO for social graph.
       Vertices/edges are organized in linked structure objects, accessed with pointer addresses, and build OCC transaction and MVCC read via FaRM.
    2. highlights
        1. Leverages cheap DRAM, RDMA. Relies on FaRM for distributed transaction. 
            1. Coprocessor model: A1 is compiled into same address space of FaRM process, to reduce function call cost. Multi-threading is also cooperative
                1. question: how do you manage the user isolation and resource isolation ..
            2. data structure
                1. principles: use pointer linked data structure (linked lists, BTrees, graphs), frugal for memory cost, exploit locality, exploit concurrency 
                               FaRM object are access by pointer address, rather than str key. so all types are building with pointers
                               bond is widely used.
                2. data model is fixed schema types of Vertex/Edge, similar to entity relation model; but Vertex/Entity are first-class citizen
                   primary key is mandatory, secondary index on vertex attributes are supported
                3. APIS: CRUD on vertices/edges, types (vertex, edge can have a pointer to a data object), graphs. begin/commit transaction
                4. colocation: vertex are randomly sharded to nodes, as a plain object. query execution is pushed to colocated data nodes.
                    1. edge list is separated into two half-edges: incoming edge list and outgoing edge list. a vertex deletion must check their other pair
                    2. small edge list is stored unordered in a single object, can be colocated with vertex. large edge list is stored in BTree, distributed.
                5. query execution
                    1. async tasks span out cluster. first node that query arrives act as the coordinator.
                       coordinator aggregates replies, if result is too large, coordinator instead returns half results and a continuation token 
                    2. A1 doesn't have a true query optimizer (WIP), most queries are straightforward
                    3. A1QL for knowledge graph, but not talked much in this paper. See Table 2.
                       It looks like ElasticSearch JSON query: https://www.baeldung.com/elasticsearch-geo-spatial
            3. disaster recovery
                1. A1 async replicate all data to a durable KV store - ObjectStore used at Bing. ObjectStore supports Table schema. bond is widely used as schema.
                2. possible to lost recent updates
                    1. consistent recovery: recover the database to the most up to date transactionally consistent snapshot that exists in ObjectStore
                    2. best-effort recovery: do not guarantee that the recovered state of A1 will be transactionally consistent
                3. FaRM maps memory to another process (PyCo), so if itself crashes, FaRM won't lose its data in memory 
            4. RDMA
                1. RDMA protocol is RocEv2. A1 uses DCQCN for congestion control.
                2. Clock synchronization and lease is built by RDMA unreliable datagrams (UD)
            5. FaRMv2 vs FaRMv1, adding Opacity property
                1. no Opacity property: T1 read A and get pointer to B. T2 delete B and commits. T1 aborts, but app still deference B pointer and crash
                2. another issue of Optimistic concurrency control, Large queries are susceptible to conflict with updates and hence abort frequently
                3. both issues are solved in FaRMv2, by introducing a global clock that provides timestamp thus the global serialization of for all transactions
                   FaRMv2 also implements MVCC so read-only transaction can run conflict-free

        2. related works
            1. Facebook TAO: Two level architecture: Social graph persisted in MySQL, and use DRAM memcached to speedup.
                1. question: how does the capacity of A1 compares with TAO? FaRM in-memory doesn't have the cold tier
                2. question: per FaRM the UPS protected DRAM flush to PMEM. How does it survive datacenter power outage?
                             Also possible 3 nodes fail together with bad UPS?
                    1. Bing generates knowledge graph once a day by a large scale map-reduce job. So eventually, losing data in FaRM is not very unacceptable.
            
            2. AWS Neptune: https://aws.amazon.com/neptune/
               https://aws.amazon.com/blogs/architecture/category/database/amazon-neptune/
                1. I didn't find design details
            
            3. CosmosDB - A technical overview of Azure Cosmos DB
               https://azure.microsoft.com/en-us/blog/a-technical-overview-of-azure-cosmos-db/
                1. multi-model database is popular, that combines relational data (DocumentDB SQL), JSON documents (DocumentDB), graph (Gremlin API), geographical data
                2. globally distributed multi-model database with (optional) strong consistency
                3. CosmosDB is built from DocumentDB (greatly evolved now) and now also supports SQL.
                   CosmosDB also supports stored procedures, triggers and user-defined-functions (UDFs)

            4. Schema-Agnostic Indexing with Azure DocumentDB    [2015, 39 refs, Microsoft]
               https://www.vldb.org/pvldb/vol8/p1668-shukla.pdf
                1. DocumentDB is globally distributed, multi-tenancy. It supports strong consistency, supports  stored procedures, triggers, user defined functions (UDFs).
                   But this paper only talks about indexing subsystem. transaction is also skipped.
                   DocumentDB is using Bw-tree as the index to absorb writes. Compared to LSM-tree, Bw-tree can also use "blind incremental update" to flush deltas to disk, rather than full page sync in B+-tree. This is good part. This made Bw-tree not only for in-memory DB index, but also a possible replacement for LSM-tree.
                2. highlights
                    1. goals
                        1. atomically index all documents. 
                        2. configurable trade-off between index performance, storage overhead, query consistency
                        3. multi-tenancy 
                    2. schema
                        1. Documents as Trees
                    3. indexing
                        1. path segments are encoded. how many segments to cover is a trade-off between storage overhead and query performance
                        2. question: this part is written like a data structure spec rather than a paper ..
                        3. using Bw-Tree for DocumentDB, after several attempts and found B+-tree hopelessly inefficient
                        4. Bw-tree storage is organized in a log-structured manner. Bw-tree pages are flushed in an incremental manner
                            1. useful part to help understand the Bw-tree paper itself. Bw-tree page sync is NOT like B+-tree. See Figure 10.
                               Bw-tree on SSD appends page delta. Both in memory and in SSD, the Mapping Table points to the last delta, the delta points earlier delta to the base page
                            2. upon page flush but the page is not loaded to memory, Bw-tree only flush the delta, no read needed (blind incremental update).
                               Deltas can be batched in a large 4MB flush buffer
                               so B+-tree's read-modify-write on page sync can be totally avoided
                            3. unlike LSM-tree compaction, the merge happens when the page is read to memory.
                                1. merge callback needs to handle consistency issue. "the polarity based merge of the postings with the holdout"
                            4. note all steps happen as latch-free, as in Bw-tree.
                    4. others
                        1. DocumentDB follows a single master model for writes
                    n. questions
                        1. thinking comparing Bw-tree as a replacement of LSM-tree
                            1. the Bw-tree would still need page sync to persisted updates, while LSM-tree flush checkpoints (then later need compaction)
                            2. Thinking first we only need log. Then we change flush log to flush checkpoint (a big batch of logs), where log is only used to preserve recent data. Then we need compaction for flushed checkpoints.
                               Per traditional DB paging system. Instead of flush big checkpoint, we sync pages (which may contain both changed and untouched value, in efficient). Then Bw-tree can be used at this place.
                               This is also the argue of update-in-place vs append-only. The page sync introduces many random reads/writes. And random reads writes amplifies SSD too and HDD
    
    n. related materials
        1. FaRM: No compromises: distributed transactions with consistency, availability, and performance    [2015, 273 refs]
           https://www.microsoft.com/en-us/research/publication/no-compromises-distributed-transactions-with-consistency-availability-and-performance/
            1. FaRM publications: https://www.microsoft.com/en-us/research/project/farm/publications/


9. Secondary Indexing Techniques for Key-Value Stores: Two Rings To Rule Them All    [2017, 10 refs]
   http://ceur-ws.org/Vol-1810/DOLAP_paper_10.pdf
    1. HBase Secondary Index that compares global index and local index.
       Global index only needs one search but incurs high consistency cost upon updates.
       Local index colocates with each data partition, where consistency update is kept local, but a search needs to query all partitions
    2. highlights
        1. global index can be implemented with HBase table, low effort.
           While local index implementation effort is high, no HBase native support 
        2. Index Maintenance
            1. question: with global index, how to update with consistency?
                1. the paper didn't solve this part
                2. in general, the update needs distributed transaction that HBase didn't come out-of-box with
                   1. the second issue is, key->newValue needs also remove oldValue->key on the index
                   2. third issue, key1->newValue & key2->newValue with generate race condition on newValue->key1,key2 entry at secondary index
                3. the paper uses in-memory B-link tree for local index. But, it's not persisted. Upon failure it needs full rebuild.
    n. related materials
        1. LSM-based Storage Techniques: A Survey - Chen Luo
           https://arxiv.org/pdf/1812.07527.pdf
            1. Diff-Index: sync-full, sync insert, async-simple, and async-session.
            2. See "3.7.5 Summary" for the useful summary
            3. The parent paper is referenced in this paper. as [29].
```

Papers about Runtime Verification

```
1. Circuit ORAM: On Tightness of the Goldreich-Ostrovsky Lower Bound    [2016, 246 refs]
   https://eprint.iacr.org/2014/672.pdf
    1. Circuit ORAM is used in MPC. It is based on tree-based ORAM framework, significantly reduced circuit size, and asymptotically reaches the Goldreich and Ostrovsky lower bound
    2. highlights
        1. 隐私计算，cloud outsourcing, multi-party computation (MPC), 
        2. Circuit ORAM 58.4X improvement, Theoretical near-optimality lower bound
        3. Table 1: Circuit size of various ORAM schemes
    n. related
        1. ORAM 和多方安全计算
           https://zhuanlan.zhihu.com/p/42729085
        2. Garbled Circuits介绍 - 5&6 Yao协议的实现 & 总结
           https://zhuanlan.zhihu.com/p/400422769
        3. Circuit ORAM
           https://cloud.tencent.com/developer/article/1747284
        4. ORAM slideshare P114/136 - Circuit ORAM
           https://www.slideshare.net/AshutoshSatapathy4/oram

2. A Tutorial on Runtime Verification    [2012, 161 refs]
   https://www.havelund.com/Publications/rv-tutorial-ios-2012.pdf
    1. dynamic runtime verification with Java, AspectJ, and the Rover system example
    2. highlights
        1. Classifying Runtime Verification Approaches
            1. When monitoring occurs
            2. Where the monitor is placed
            3. When are verdicts returned
        2. A Rover System and its Requirements
            1. requirements
                1. Exactly One Success
                2. Respect Conflicts
                3. Respect Priorities
                4. Release Resource
            2. Instrumentation with ASPECTJ
               Designing Monitors with pointcut
               TRACEMATCHES language, extension of AspectJ
               JAVAMOP specification language
               RULER expressive rule-based runtime verification
    n. related
        1. Morpheus: A Vulnerability-Tolerant Secure Architecture Based on Ensembles of Moving Target Defenses with Churn
           Zhihu: https://www.zhihu.com/question/337913506/answer/774842152 - Gh0u1L5's answer
            1. good to explain the field

3. Enclage: Building Enclave-Native Storage Engines for Practical Encrypted Databases    [2021 VLDB, 3 refs]
   http://vldb.org/pvldb/vol14/p1019-sun.pdf
   https://www.bilibili.com/video/BV1Pb4y1674E/
    1. Enclage, an encrypted storage engine that makes practical trade-offs.
       page-level encryption, reduced enclave interaction, hierarchical memory bufer.
       To make better use of the limited enclave memory,
        we derive the optimal page size in enclave
        and adopt delta decryption to access large data pages with low cost
    2. highlights
        1. challanges from Intel SGX hardware enclaves (thread of trusted execution environment (TEE))
            1. limited memory ~94MB
            2. huge cost from systemcalls interaction with enclave
            3. Section 1 Introduction to peer works
                1. EnclaveDB [50] puts all data in enclave-protected memory
                2. ObliDB [25] adopts oblivious data access to untrusted memory
                3. Always-encrypted [5] and StealthDB [61] ofer a few enclave-based functions for computation over ciphertext with marginal modifcations to SQL Server and PostgreSQL
                    1. leads to severe information leakage and performance degradation
        2. design space of exiting works - Table 1, interesting useful part
            1. encryption granularity, execution logic in enclave, memory access granularity, enclave memory usage, record identity protection
            2. security (information leakage), vs performance, vs functionality
        3. enclage design
            1. enclage index in enclave, B+tree like, buffering tier 1 EBuffer, teir 2 MBuffer
                1. reducue page swapping, reduce unnecessary OCalls
            2. enclage store heap-file-like table store, append-only
                1. AES-CTR model: allow a small block within a large cipher be solely decrypted. only decrypts record, rather than load entire page to enclave and decrypt
    n. related
        1. VLDB 2021 论文推荐(续)
           https://zhuanlan.zhihu.com/p/424673206
            1. "达摩院孙园园博士等人发表的论文，探讨如何在云端构建安全数据库。本文讨论了加密数据库存储引擎，并提出了 Enclage 存储引擎，包括两个组件：一个类 B+-tree 索引的 Enclage 索引；一个类堆文件的表存储 Enclage store"
        2. 在工业界和学术界中数据库的研究热点是什么？
           https://www.zhihu.com/question/318554064/answer/2092699648
```

Industry papers about data and storage

```
1. Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3    (2021 SOSP, 1 refs, AWS)
   https://www.amazon.science/publications/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3
   https://www.youtube.com/watch?v=YdxvOPenjWI
    1. interesting "reference model" method, executable code, engineer dev-able.
       compared to TLA+, the later is less direct to check crash consistency and concurrency correctness which relate to implementation
    2. highlights
        1. S3 deploying new ShardStore written in Rust.
            1. ShardStore is a KV store, single node, hosting hundreds PB customer data
            2. ShardStore comprises LSM-tree and shard data stored outside
            3. ShardStore writes sequentially chunks in extents. extents can reset write pointer and then allow overwrites from start
                1. the lacking of single log makes crash consistency more complex
                2. soft write pointer for each extent is persisted in a superblock and flushed on a regular cadence
            4. ShardStore implements "soft update", rather than WAL
                1. Soft update ensures crash consistency by ensuring ordering of writes to disk, i.e. data->index->metadata.
                   It saves the cost of redirecting writes in write-ahead log, and allows flexible placement of data on disk
                2. Soft update doesn't guarantee persistence like WAL. ShardStore tracks writes ordering via "Dependency" object, and use a is_persistent field to track persistence
        2. lightweight formal methods goals
            1. executable reference models as specifications
            2. decompose aspects, automated tools
            3. coverage tools to track effectiveness over time
                1. engineers are encouraged to write their own reference models to change with code
            4. not full formal verification
        3. reference models
            1. a simple hashmap is a reference model for LSM tree, interface is same
                1. reference model can fail in limited ways
                    1. we choose to omit other implementation failures (IO errors, resource exhaustion, etc.)
                2. reference models can also be used at unittesting mocks
            2. correctness properties decomposed
                1. sequential correctness
                2. crash consistency
                    1. sequential crash-free operations
                    2. sequential crashing execution, reference model defines which data can lose
                    3. concurrent crash-free execution, use a separated reference model
                    4. NO checking concurrent crashing execution because not found an effective automated approach
                        1. question: more details? 
                    5. persistence, and foward progress
                        1. forward progress: after a non-crashing shutdown, every operation's dependency should indicate it is persistent
                3. concurrency and linearizability
                    1. tools
                        1. We check such fine-grained concurrency properties using the Loom stateless model checker for Rust [28], which implements the CDSChecker [39] algorithm
                        2. we developed and open-sourced the stateless model checker Shuttle [47]
                        3. Miri interpreter [50], a dynamic analysis tool built into the Rust compiler that can detect certain classes of undefined behavior
                        4. We worked with the developers of Crux [51], a bounded symbolic evaluation engine
            3. argument biasing with domain knowledge
                1. copying customer traffic pattern into testing is little effective, rather we should break any assumption
                2. get from what puts, reads/writes close to page size
            4. failure steps minimization
                1. upon a bug found, automation try to reduce op list to find the minimal list to reprodce failure
                2. ShardStore is designed to be deterministic as much as possible across runs
            5. failure injection
                1. failure types
                    1. fail-stop crashes
                    2. transient or permanent disk IO failures
                    3. resource exhaustion
            6. engineer dev-able low cost executable reference models
                1. We focused heavily on lowering the marginal cost of future validation: we would not have considered this work
                    successful if future code changes by engineers required kicking off new formal methods engagements
                2. Early in our work,
                    we wrote reference models using modeling languages we
                    were familiar with (Alloy [23], SPIN [22], and Yggdrasil-style
                    Python [49]) and imagined developing tooling to check the
                    Rust code against them. It was only when we discussed
                    long-term maintenance implications with the team that we
                    realized writing the models themselves in Rust was a much
                    better choice
                3. and even later when we realized the reference
                    models could serve double duty as mocks for unit testing
        4. practices
            1. random sequences
            2. "pay-as-you-go": test small scale locally, larger scale before deployment
            3. continuous validation
            4. get into a world that future change doesn't involve formal method experts at all
        5. questions
            1. where addresses "formal" in paper title?
                1. so .. this is actually a pragmatic approach
    
2. Facebook 十年集群管理系统简述 Twine: a Unified Cluster Management System for Shared Infrastructure [2020 OSDI, 16 refs, Facebook]
   https://www.usenix.org/conference/osdi20/presentation/tang
    1. Facebook's shared infra for job hosting and scheduling. One control plan for entire region, span jobs wider to reduce fault tolerant "resoure buffer", small machine lowers TCO then big machine, host profile customization, are interesting
    2. highlights
        1. Control plan across entire region (Ms of machines)
            1. make machine assignment dynamic
            2. allow jobs to migrate cross clusters in region
            3. spanning jobs wider in clusters, reduce the "resource buffer" needed for fault tolerant
            3. too many K8S clusters if were using K8S
            4. "entitlement" to manage quota
                1. follows the "resource offer" from Mesos
        2. Allow app users to do customization
            1. hook into shard restart timing, for rolling upgrade, avoid all shards offline
            2. host profile customization: huge page, kernel version, etc
               able to switch host profiles 
        3. small machines is better than big machines
            1. deploy small machines on a rack give more CPUs less memory
            2. small machine approach is more power efficient, lower TCO
                1. questions: is this because small machines can be shutdown, but big underutilized machines is wasting power?
            3. small machine also provides a resource isolation boundary, than sharing big machines
        1. questions
            1. how Twine if compared to a public cloud
    n. related
        1. Facebook 十年集群管理系统简述
           https://zhuanlan.zhihu.com/p/359071322
            1. control plan across entire region
            2. host profile customized by apps
            3. 小机器（而非大机器）
        2. 如何评价Facebook在OSDI20发表的Twine和Delos论文？
           https://www.zhihu.com/question/429682314/answer/1574581196
            1. "Twine作为FB的IaaS层，应用已经普及到各大产品线，可以说绝大部分的脸书服务器都运行在这个系统下面。其实Twine本身并没有太多学术上的创新，而可以说是一个工程上的成功 .. 在单一系统规模这个方向，我的理解Twine是工业界领先的"
            2. "当然Twine本身有很多问题，stacking也好，resource isolation也好，可以说落后业界尤其是公有云很多年，这个基本上amazon/microsoft/google相关背景过来的员工都有同感"
        3. Dynamo: Facebook’s Data Center Wide Power Management System    [2016, 135 refs]
            1. "On the other hand, we overcommit power by default [41]"

3. Dynamo: Facebook's Data Center Wide Power Management System    [2016, 135 refs]
   https://research.facebook.com/publications/dynamo-facebooks-data-center-wide-power-management-system/
    1. To show how Facebook manages the datacenter power provisioning.
       The conflict is to get higher power efficiency, vs power failure can easily cause datacenter wide outage.
       Facebook managed to bring power over-provisioning to over-committing. interesting impactful for COGS.
       Besides, few previous works on datacenter wide. 
    2. highlights
        0. background for DC power supply, see Figure 2
        1. 6-months of fine-grain production power data
        2. Dynamoc design: agent and controller
        3. evaluation on facebook's large scale datacenters
    n. related
        1. 简书：Dynamo: Facebook’s Data Center-Wide Power Management System
           https://www.jianshu.com/p/e7fdbb456d5f
        2. Facebook数据中心电能管理系统Dynamo
           https://zhuanlan.zhihu.com/p/65897620
            1. "考虑到断电器跳闸的严重性，数据中心操作员采取了over-provisioning过度供应数据中心电源的方法"
            2. "提出了power capping搭配over-subscription技术"
                1）持续监控服务器功耗。
                   不同聚合级别（从机架到MSB）和不同时间尺度（从几秒到几十分钟）的功率变化特征
                   发现控制器功率读取周期应该快到几秒钟
                2）在接近其功率限制是使用处理器和存储器动态电压和频率调整（DVFS - dynamic voltage and frequency scaling）来抑制服务器功耗
                   controller与controllee间的可扩展通信，应用和服务间感知上限动作
            3. Performance-Aware Power Capping
                1. “首先将Facebook服务分类为一组预先定义的priority groups”，SLA
                   然后尝试以优先级从低到高的顺序在优先级组的服务中进行功率削减
                   ”对于属于相同优先级组的服务的服务器内，控制器使用high-bucket-first算法来确定每个服务器应该削减多少功率。算法首先根据服务器当前的功耗将服务器分成不同的桶，然后在最高桶中的服务器之间分配总功率削减，理由是惩罚先消耗更多功率的服务器。如果最大的桶不足以满足功率削减，则扩展到下一个桶中的服务器等，直到总功率减少可以满足SLA下限，在桶内所有服务器将获得均匀的功率削减
                2. 控制器使用three-band算法进行capping或uncapping决定
                   即在capping threshold，capping target与uncapping threshold这3个阈值间触发不同capping策略。
                   three-band算法效地消除了控制振荡，同时使上限响应时间足够快以处理突然的功率浪涌
        3. Introduction to Facebook's data center fabric    [2014, Youtube]
           https://www.youtube.com/watch?v=mLEawo6OzFM
            1. each "Server Pod" is a small cluster

4. Alibaba Hologres: A Cloud-Native Service for Hybrid Serving/Analytical Processing    [2020 VLDB, 3 refs]
   http://www.vldb.org/pvldb/vol13/p3272-jiang.pdf
   https://www.youtube.com/watch?v=YttNq3ixxtQ
    1. HSAP cloud native disaggregated database
       compared to HTAP, Hologres HSAP is more customized for Internet Company online recommendation system + BI system use.
    2. highlights
        1. usecase scenario
            1. Alibaba recommendation system, knowledge serving will generate results, to feed into the DB analytics system, and yet fine tune the knowledge
               OLTP - serving users, generating new metrics
               OLAP - knowledge ML background jobs
            2. existing systems - Figure 1 is an interesting useful reference
                1. Greenplum for interactive analytics -> BI system
                   Hive for batch aggregates -> Update derived features and dimension tables
                   Cassandra/HBase for serving -> Recommendation system
                2. need unified DB for all
            3. HSAP compared to HTAP
                1. high throughput ingestion on realtime data
                    1. sync-ing much data from separate OLTP to OLAP can be expensive
                2. transaction may not be supported
                3. serving highly concurrent user accesses, and OLAP workloads
        2. key designs
            1. disaggregated compute and storage.
                1. DB is separated into FE, Coordinator, Worker Node, Storage manager, Resource manager, Cache, and shared Pangu Distributed Filesystem.
                   Each layer can scale independently
                2. a tablet can be either row or columnar format, both managed by LSM-tree
                    1. row format memory table as Masstree
                    2. columnar format memory table uses format Apache Arrow
                3. Hierarchical Cache
                    1. local disk cache, block cache, row cache
            2. Highly Parallel Query Execution
                1. fragment分为 read/write/query fragments, they are operators DAG
                2. fragment被水平切分为fragment instances，而fragment instances被映射到本地的一个work units上
                3. Execution Context, to avoid frequent context switching
        3. questions
            1. I didn't see explicit large scale production use in paper?
                1. though always Double-11 Festival ..
            2. compared to HyPer, less found about JIT and vectorized query execution
            3. how Hologres compares to Snowflake?
            4. how is the row and columnar format organized across data?
    n. related
        1. Alibaba Hologres: A Cloud-Native Service for Hybrid Serving/Analytical Processing
           https://zhuanlan.zhihu.com/p/449695265
            1. HSAP（hybrid serving and analytical processing）的云原生数仓（可能不支持事务，但又支持类似于TP的服务查询）
            2. 计算存储解耦，每一层可以弹性伸缩
            3. 架构
                1. FE主要接收查询并返回结果，并且将query经优化器生成一个fragment instances组成的DAG plan，由Coordinator将fragment分发到对应的worker Node
                2. Worker Node是一个CPU 内存资源的集合，并且管理多个table group shareds
                3. worker_units实际上是通过EC（Execution context）来执行，EC可以认为是一个user-defined thread的资源抽象，多个EC构成EC Pools
                4. 底层共享存储是阿里的盘古文件系统
            4. query processing
                1. fragment分为 read/write/query fragments。 read/write fragment只能访问一个TGS，
                   而query fragment不含read/write operator，uery fragment会根据load balance被分发到任意worker node上

5. RAMP-TAO: Layering Atomic Transactions on Facebook's Online TAO Data Store    [2021 VLDB best industry paper award, 1 refs]
   https://www.vldb.org/pvldb/vol14/p3014-cheng.pdf
    1. very good for how eventual consistency system can upgrade for transaction support
       Read atomic is < snapshot isolation, it needs timestamp metadata, and Tx failure atomic prebuilt, it also needs recent versions preserved
       the protocal can be implemented fast - most are one round communication, and opt-in - only pay when you need, and built atop - minimal change to existing system 
       Facebook does have a long track record to build global scale caching system (a serias of papers). it reached the day transaction consistency is needed
    2. highlights
        1. key advantage - good practical for eventual consistency system to upgrade to
            1. Minimal change to TAO, only layer on top to provide transaction
            2. Minimal impact to performance, and low memory usage. and only those need transaction pay for overhead
        2. fracture reads problem
            1. read expects to read all or none what a write transaction updates
               but in reality TAO encounter 1 anomalies out of 1500 read batches
               due to writes not fully replicated
            2. Facebook uses MySQL to host social graph data
                1) Two sets of associated links, one part can be missing
                2) One set of associate link, half side can be missing
        3. TAO's existing work of failure-atomic transaction API - very good part for how eventual consistency system can upgrade for transaction support
            1. TAO ready exist write atomic. read can still fracture because different shards are independently and async replilcated to TAO cache replicas
            2. single-shard MultiWrites - using MySQL transaction ACID to support
                1. this is not enough for customers, because forcing them to colocate data to one shard, and may exceed capacity, and data may not owned to one team
            3. cross-shard transactions - use 2PC and 2 phase locking implemented.
               the protocol is layed atop TAO, and opt-in pay only when you need
            4. special case - bidirectional associates. That's the A->B and B->A link, they are special because they are very ubiquitous.
               TAO try best beffort, most transaction can complete one round without first phase of 2PC, and a background fixer to ensure failure atomic
               when need more strict invariant to hold, customers can use cross-shard transactions
        4. RAMP-TAO protocol - very good part
            1. problems and solutions
                1. from the paper, I can sense existing TAO is
                    1. OK to read uncommitted. E.g. to see a middle value during 2PC (recovery)
                        "If Tr reads from x and y while T2 is writing, it could read
                        {x = x1, y = y2} or {x = x2, y = y1} on its second round, both of
                        which violate RA"
                    2. no need to support snapshot isolation, e.g.
                        a1,b1,c1,d1 is read
                        RA found violation as another Tx wrote c2,d2
                        RA needs to fetch a1,b1,c2,d2 and return
                       though in middle a1,b1 may have been updated to a2,b2 of timestamp 2, there is no need to return a point-in-time snapshot of timestamp 2
                    3. TAO lacking of multi-version support, compared to RAMP original
                        1. if a fracture read is found RAMP-TAO switch to fetch newer versions of value. e.g. c1,d1 -> c2,d2
                           how ever it's possible c,d keeps being overwritten by newer transactions. RAMP-TAO may never has chance to find a non-factured c,d.
                           In original RAMP, RAMP instead fetches older versions of c,d, which are stable
                           but TAO original doesn't have a multi-version support
                        2. the solution is to, leverage RefillLibrary, to store recent version of values
                            1. but what low watermark and high watermark of versions to keep?
                            2. low watermark issue: RefillLibrary keeps as old as 3 min of old versions, this is longer than TAO replication time, so most time no issue
                                1. if customer is requesting older than 3 min version, that means replication has must already been done, no fracture
                            3. The most recent values may not yet have been saved in RefillLibrary, i.e. high watermark issue
                                1. RAMP-TAO will go to DB to fetch the newest value
                                2. it's possible to RA violation again, RAMP-TAO will then fallback to older version of value, they should exist in RefillLibrary
                            4. My questions: what if customer sees a <x2, y999>? it seems RAMP-TAO RA allows this situation.
                               the backing Tx writes are <x2, y2> <y999,z999>
                    4. read termination
                        1. This is same with 3, TAO needs fast read termination, to achieve low read latency.
                           the main gap is no multi-version support
                        2. worst case, fail the transaction and let user do retry
                    5. RAMP needs a metastore to tell timestamp version => corresponding Tx's write set
                        1. this is tracked in txn_info DB table, to point to shards and key,data,timestamp
                        2. RefillLibrary also has the metadata
            4. actual workflow
                1. See Algorithm 2, my questions
                    1. ts_lastest[K_txn] <- max(ts_latest[K_txn], r.ts)
                       but compared to Algorithm 1, here is ts_lastest <- max(ts_latest[K_txn], r.ts), a glitch?
                    2. the algorithm always try to fetch the newest value and timestamp, this is not MVCC, which is OK to return an older version
                       but in paper detail, 
                       "we can ask the system to return slightly older ones to satisfy atomic
                        visibility (note that we omit the details of this optimization for 
                        clarity in Algorithm 2)"
                2. See "End to end protocol description"
                    1. RAMP-TAO, clients first directly goes to RefillLibrary.
                       They fetch data, and a bit to tell whether newer Tx modified value.
                       In most case, no RA violation found - the fast path
                    2. if RA (read-atomic) violation is found, collect the keys need newer version, and then fetch again from DB, remote region cache
                       if yet a new RA violation is found, we can fallback to a slightly older version to sure to present in RefillLibrary.
                3. Optimization for bidirectional association
                    1. since the association always write in pair, client after read uses the newer version pair to overrride the older version pair, purely local

    n. related
        1. VLDB 2021 论文推荐(续)
           https://zhuanlan.zhihu.com/p/424673206
            1. "RAMP-TAO 灵感来自于 Read Atomic Multi-Partition (RAMP) 协议，RAMP 协议的原论文提出了一个新的隔离级别——Read Atomic（RA），RA 隔离级别不允许出现 fractured reads，即每个事务的更新都应该对其他事务可见，例如，如果一个事务 T1 写了 x = 1 和 y = 1，事务 T2 不应该读到 x = 1 和 y = null 的旧版本数据。RA 隔离级别对一个最终一致性的存储系统来说非常有用"
        
        2. TAO: Facebook’s Distributed Data Store for the Social Graph    [2013 ATC, 490 refs]
           https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf
           https://www.youtube.com/watch?v=sNIvHttFjdI
            1. Memcache for QPS, >99% are reads; MySQL for capacity, saving graph links while contents e.g. photos in other store.
               optimized for cross region, scaleout, heavily using cache. async eventual consistency 
            2. highlights
                1. Social graph: users, posts, comments, etc
                    1. large scale, high frequency ingrest, and low latency feed to user
                    2. hard to predict to traffic pattern, burst, from user uncertainty
                2. TAO
                    1. system include: databases, caches
                        1. mysql: objects = nodes, associations = edges
                        2. memcache: nodes, edges, edge list
                    2. single system across all Facebook datacenters to provide access to all graph data
                    3. dynamic resolution of data dependencies
                    4. data structures and queries
                        1. every association list has a timestamp list, can be queried by position or time
                        2. reads - 99.8%, object/assoc gets/range, count
                    5. how to scale out
                        1. web server - stateless
                        2. Cache - objects, assoc lists, assoc counts - sharded by id
                            1. read QPS is bound to cache layer
                            2. Follower cache (web server side)
                               Leader cache (DB side)
                                1. leader cache maintains distributed write logic and to avoid thunderherd issue
                                2. follow cache can serve as a failover after another failed
                            3. cache is write through, (as we should have seen a lot in Facebook memcache paper, Facebook CacheLib paper)
                        3. Database - sharded by id
                            1. capacity bytes is bound to database
                            2. async DB replication
                            3. we are not storing the contents, but storing the links.
                               Facebook has another system for photo contents
                    n. questions
                        1. cache for QPS, DB for capacity. so it means the graph is not serving OLAP complex queries (simple cache interface cannot do), but mainly for Facebook website displaying contents? 
                        2. the consistency level should be eventual consistency, user is OK to toerlate minutes of delay. and that's why later came paper RAMP-TAO
                        3. though mysql seems not a very proper graph DB, but since cache serves QPS, the main system design focus now moves to cache, and seems much simplified 
                        4. why not using a native graph database? rather using MySQL
                            1. MySQL has the backup system we already has experience
                               we already has the data model in MySQL, optimized locality
                               ... it should be the engineer practices and history path

        3. MyRocks: LSM-Tree Database Storage Engine Serving Facebook's Social Graph    [2020, 5 refs]
           https://vldb.org/pvldb/vol13/p3217-matsunobu.pdf
            1. logged before

        4. FlightTracker: Consistency across Read-Optimized Online Stores at Facebook    [2020 OSDI, 6 refs]
           https://research.facebook.com/publications/flighttracker-consistency-across-read-optimized-online-stores-at-facebook/
           https://www.youtube.com/watch?v=noyH8x7VkyU
            1. (checked video only.) FlightTracker - RYW (read your write) consistency API to access social graph TAO
            2. FlightTrack stores 60sec metadata, since replication should finish after that
                1. writer attach ticket, ticket is a metadata that identifies a set of writes
                2. ticket-inclusive read: use ticket to fix inconsistent reads, fetch missing data elsewhere, attach ticket on read to ensure freshness

6. Hyperspace: The Indexing Subsystem of Azure Synapse    [2021 VLDB, 0 refs]
   https://www.microsoft.com/en-us/research/publication/hyperspace-the-indexing-subsystem-of-azure-synapse/
    1. the paper is mostly user facing, talking about high level architectures. The overall system is huge for a single paper.
       featured in Interoperability and automated index lifecycle management. and Hybrid Scan is interesting useful technique
       related Datalake systems: Linux Foundation's Delta Lake [30], Apache Hudi [27], and Apache Iceberg
    2. highlights
        1. key features
            1. building the index (secondary index)
                1. build index with Spark with serverless Spark batch jobs, incremental refresh
                2. metadata in WAL in datalake
                    1. lineage that allows seamless incremental index refresh
                    2. statistics allowing fast pruning
                3. data format agnostic, CSV/JSON/Parquet/DeltaLake/Iceberg, min-max/zonemap filters
            2. using the index - automated index lifecycle management
                1. multi-engine index
                2. query optimizer integration
                3. history tracking through transaction logs, and audit logging
                4. allow exploit stale indexes, hybrid scan mechanism
                5. index as a derived dataset to simplify data
                6. index recommendation, tell users whether and which to have index
            4. managing the index
                1. index is a derived dataset, i.e. same with other data in datalake, inter-operatable
        2. usecases
            1. Business analytics, OLAP, Needle-in-haystack exploratory queries
            2. GDPR compliance, query user data
            3. IoT, time-series, streaming
        3. architecture
            1. columnar
            2. hash-partitioned, intra-partition sorted
                1. allow skip shuffle stage in shuffle-based join
            3. lineage tracking
                1. index contains a pointer to the original data. located by handle URI
            4. log management API
            5. index specs
            6. concurrency model
                1. multi-user access, index state has exclusive compatibility table, Operatoin log can track access and states
                2. relies on the atomicity of renaming a file in a cloud file system
                3. timestamp is used to generate signature of an index, like a snapshot, index of different versions can be queried simultaneously
        4. incremental refresh
            1. compare new appends vs lineage source, e.g. filename, last modified timestamp, file size
            2. quick refresh
                1. if user data is updating too quick, incremental refresh only scans file level metadata
                hybrid scan layer at query time will derive the latest index
            3. optimize
                1. after incremental updating too many times, the index can become fragmented
                   compact the index into more efficient format 
        5. Hybrid scan
            1. use existing index (may be stale), and apply the changes diff from data source
            2. query plan is changed to 1) excluded deleted rows in index 2) merge new rows from source file change
            3. Support of “Time Travel”, Hyperspace supports ACID data formats such as DeltaLake
                1. index has versions
                2. query optimizer selects best index version from Hyperspace, and apply scan diffs from DeltaLake
        n. questions
            1. Is index updated in sync with data update (ACID), or a eventual consistency?
                1. strong consistency requires exposing transaction manager service, which hinders interoperability.
                2. "We decided to trade-off metadata consistency for easier operational maintenance"
                3. hybrid scan can query a not-refreshed index, and with latest data, in same time
            2. Is it a global index, or an index per data partition?
                1. should be global index. the index is totally decoupled with source data
            3. Exactly, what is the data structure of this index?

    n. related
        1. VLDB 2021 论文推荐(续)
           https://zhuanlan.zhihu.com/p/424673206
            1. "本文介绍微软 Azure 团队开源的 Hyperspace 的设计与实现经验。Hyperspace 脱胎于 Azure Synapse，后者是一个基于 Spark 和 T-SQL 的数据湖。而 Hyperspace 是 Spark 的索引子系统，微软宣称无需修改应用程序代码即可加速 Spark 查询和工作负载"

        2. Hyperspace: An Indexing Sub-system for Spark in Azure Synapse
           https://www.youtube.com/watch?v=IaqjBPNS_0M
            1. mostly introducing for end users, no much paper details

        3. Apache Hudi comparing to Hadoop
           https://hudi.apache.org/docs/comparison/
           https://hudi.apache.org/docs/concepts/
            1. A key differentiator is that Kudu also attempts to serve as a datastore for OLTP workloads, something that Hudi does not aspire to be
               Hudi, on the other hand, is designed to work with an underlying Hadoop compatible filesystem (HDFS,S3 or Ceph) and does not have its own fleet of storage servers
            2. Hive transactions does not offer the read-optimized storage option or the incremental pulling, that Hudi does
               Hudi leverages the full power of a processing framework like Spark, while Hive transactions feature is implemented underneath by Hive tasks/queries
            3. Given HBase is heavily write-optimized, it supports sub-second upserts out-of-box and Hive-on-HBase lets users query that data
               However, in terms of actual performance for analytical workloads, hybrid columnar storage formats like Parquet/ORC handily beat HBase,  since these workloads are predominantly read-heavy
               Hudi bridges this gap between faster data and having analytical storage formats
            4. Streaming: Hudi can integrate with batch (copy-on-write table) and streaming (merge-on-read table) jobs of today

7. TMO: Transparent Memory Offloading in Datacenters    [2022, 0 refs, ASPLOS Best Paper, Facebook]
   https://www.cs.cmu.edu/~dskarlat/publications/tmo_asplos22.pdf
   https://www.cs.cmu.edu/~dskarlat/slides/tmo_asplos22_slides.pdf
   https://ms-my.facebook.com/atscaleevents/videos/transparent-memory-offloading-meta-niket-agarwal-dan-schatzberg-johannes-weiner/2559594047504927/
   https://github.com/facebookincubator/senpai
    1. Scaling data pane is common, scaling metadata (consistently) can be done, but compared to disk dropping price, DRAM is increasingly expensive that accounts 1/3 of infra cost
       TMO deployed in Facebook fleet-wide that saves 20%-30% memory without impact TPS. The thought of PSI is generally useful to introduce COGS features that comes with a cost
       This work introduced PSI measure, and modified Kernel swap algorithm to balance file cache vs Heap, and userspace Sanpai to feedback control memory reclaim (swap out) vs PSI pressure level. The use of Reuse Distance is also interesting.
       Good work. Besides, the many details and production experiences are useful. Compared to related works, PSI is the distinguishing part. Except Google ZSWAP (G-SWAP), there are no comparable work (mentioned in paper) in such scale and includes offloading to SSD. And it saves 20%~30% memory fleet wide on the microservice containerized architecture.
       Another key benefit is TMO doesn't need to change application. We can think about our systems, where indeed memory can be saved by a lot of complex code changing, where TMO can do this transparently.
    2. highlights
        1. SWAP
            1. why SWAP doesn't work on Linux
                1. bad for perf, programmed for HDD but not SSD
            2. the new SWAP algorithm
                1. we simply reuse Linux Kernel's reclaim algorithm (SWAP out). it internally maintains active/inactive page LRU lists.
                2. Linux App memory (majorly) consists of Heap memory and File-backed memory by page cache. 
                   The Kernel algorithm skewed to reclaim file cache more than swap out Heap memory
                    1. we augmented kernel tracking: reuse distance[7] : the diff of page fault count between the page swapped out and in again 
                       If the reuse distance is smaller than the size of resident memory, the fault is considered a refault
                        1. question: why? reuse distance < the size of resident memory. how come the threshold?
                            1. probably think the app is scanning through the working set mem. if reclaim happens within the working set.
                            2. Johannes Weiner: The reuse distance of page P is the number of unique other pages accessed until P is accessed again. If this distance exceeds the amount of available RAM, then P doesn't belong to the cacheable set. Trying to displace other pages to make it fit is futile, so we don't: the page stays on the short list for eviction, ahead of active file cache and swapbacked memory.
                            Resident memory is used as opposed to total RAM to exclude things like static kernel reservations and unreclaimable memory from what we consider potential cache capacity.
                            If you're curious, there is a more in-depth explanation of how reuse distance is approximated in the comments at the top of this file here:
                            https://github.com/torvalds/linux/blob/master/mm/workingset.c
                        2. Refault is used for PSI to exclude stalls from first time accessed file page cache
                        3. we modify the kernel reclaim algorithm to exclusively reclaim from file cache so long as no refaults occur
                           As soon as refaults begin to occur, the kernel now balances reclamation of file cache and swap based on the refault rate and swap-in rate respectively
                           With this new reclaim algorithm, swap occurs as soon as the file cache’s workingset begins to be reclaimed
                           This approach more equally offloads file-backed and swap-backed cold memory, and minimizes the aggregate amount of paging
                           Our changes to the Linux kernel reclaim algorithm have been upstreamed
        2. PSI + SANPAI
            1. Pressure Stall Information (PSI) measures impact of lack resource, i.e. tracking blocks at page faults
                1. Expressed as a percentage of wasted compute potential
                2. scales with storage speed, faster SSD lower impact
                3. in more detail, PSI include below occasions
                    1. when a process triggers reclaiming pages when memory is full and the process tries to allocate new pages
                    2. when a process needs to wait for IO for a refault, i.e., a major fault against a page which was recently evicted from the file cache
                    3. when a process blocks on reading a page in from the swap device
                4. usecases
                    1. CPU stall are part of processes are stalled, CPU full is when all processes are stalled 
                       full pressure can be used to detect unacceptable losses of productivity that require immediate remediation
                        Userspace out-of-memory killers can monitor full metrics and apply killing policies. Kernel OOM killer is too slow
                    2. Before PSI, operators relied on correlating indirect metrics such as kernel time, variations in application throughput, event counters for reclaim activity, file re-reads, and swap-ins, in order to estimate the resource health of workloads
            2. Userspace agent Senpai maintains constant low but non-zero PSI pressure, in feedback control style
               if PSI is lower than threshold, reclaim memory (offload to disk); if PSI is higher than threshold, no reclaim.
                1. user can also measure how much actual memory the app needs
                2. formula: 𝑟𝑒𝑐𝑙𝑎𝑖𝑚_𝑚𝑒𝑚 = 𝑐𝑢𝑟𝑟𝑒𝑛𝑡_𝑚𝑒𝑚 × 𝑟𝑒𝑐𝑙𝑎𝑖𝑚_𝑟𝑎𝑡𝑖𝑜 × 𝑚𝑎𝑥 (0, 1 − 𝑃𝑆𝐼𝑠𝑜𝑚𝑒 / 𝑃𝑆𝐼𝑡ℎ𝑟𝑒𝑠ℎ𝑜𝑙𝑑)
                    1. the reclaim_mem step size is at most 1%,  reclaim is performed every six seconds. 
                       Adaptation to workload expansion, on the other hand, is immediate
                3. instead of set cgroup limit, Senpai uses a new memory.reclaim cgroup control file, ask Kernel to reclaim exactly the calculated memory amount
                   so when app needs quick mem growth due to workload change, cgroup limit won't block it
                4. Previous measurements of tax memories were ad hoc, reliant on measuring how much memory was used before hitting out-of-memory or unreliable per-process metrics such as RSS. With TMO, we were able to measure and attribute memory consumption to specific processes and proactively act on regressions

        3. ZSWAP memory compression
            1. hot memory, warm memory, cold memory. swap out cold memory, compress warm memory.
               actually, app needs to config to choose only one as offloading target.
               Kernel supporting a hierarchy of offload backend is future work
            2. experimented with many compression algorithms, including lzo, lz4, and zstd [42], then finally chosen zstd for ZSWAP
               experimented with various zswap memory pool allocators, including Z3fold, Zbud, and Zsmalloc [43], and finally chose Zsmalloc

        4. rollout to production
            1. instead of a perfect solution, we wrap up ship to get an immediate solution
            2. let services to choose ZSWAP or disk swap
            3. SSD write endurance becomes an issue (Similar issue also mentioned in Kangaroo/CacheLib papers, common for SSD cache)
                1. regulate SWAP out MB/sec from ~4MB/sec to 1MB/sec
            4. onboard, this part is interesting
                1. first deploy for the datacenter memory tax, as they had more relaxed perf constraints.
                   and the new measurements are proven useful
                2. then deployed TMO in file-only mode, no touching Heap memory.
                    1. TMO helped detect that an application unexpectedly consumed a large amount of file cache due to its repeated execution of a self-extracting binary (70% memory savings)
                    2. Most methods for memory-usage accounting would not detect this as they discount file cache as negligible or reclaimable
                3. switched TMO from file-only mode to include swapping for several of the largest applications, with stringent performance SLO
                    1. As PSI works well to capture the impact of memory offloading on diverse applications, we were able to use a single globally-optimal Senpai configuration to support all applications 
        5. future work
            1. Memory Offloading to CXL Memory
                1. as said the promising new technology that many people are working on. See slides page 46 for chart. Good
                   A pool of CXL-Mem NUMA nodes can be connected to CPU via CXL ASIC chip.
                   CXL - Compute Express Link - is an cache-coherent interconnect for Processors, Memory Expansion and Accelerators
                2. related materials
                    1. https://www.computeexpresslink.org/about-cxl
                    2. Rambus: Compute Express Link (CXL): All you need to know
                       https://www.rambus.com/blogs/compute-express-link/
        6. related works
            1. the only known large-scale adoption of kernel-driven swapping for latency-sensitive datacenter applications, is Google’s deployment [18] of zswap [43] 
        7. others
            1. Memory tax - microservice infra needs significant amount of memory to maintain infra-level functions. total as 20% many - this is interesting
                1. datacenter memory tax - for infra needs
                2. microservice memory tax - for app needs to disaggregation into microservices, routing and proxy
    3. questions
        1. with TMO if we are already serving more memory than hardware, how to handle hot memory usages spikes?
           E.g. zone down, many ENs failure, network or memory caused rec-read spikes
           E.g. frequent ENs down that may touch entire memory in a few days. E.g. a fault down down that will touch huge, if not all data memory, especially with long EC
        2. only saving memory cannot directly reduce the hardware cost of ownership. how exactly TMO saves money? buy less hardware, save more power?
           by co-running other apps consuming the memory (but how do isolation?)? by replacing hardware to use smaller memory? by change new Gen hardware planned size? 
            1. it should be the container microservice infra. less memory used, more containers can be scheduled
        3. how does ZSWAP select which piece of warm memory is chosen to compress? ideally we should choose the one that is more compressible
        4. "Regulate SWAP out MB/sec from ~4MB/sec to 1MB/sec" - how it impacts when app needs more memory to be freed up?
            1. potentially, it seems the rollout has been letting the App to serve more memory than hardware size. so this not yet becomes a problem.
               or probably the 1MB/sec only accounts for PSI reclaim, but not aggressive memory swapping
        5. PSI is an overall throughput measure, but not a Q99 latency measure. Here's a missing part
        6. so .. using SSD as cache does introduce the worse endurance problem. are there study on them? mainly I can think of is to reduce write amplification
        7. 20%-30% offloaded, is that to SSD or to compressed memory? If to compressed memory, that's not really 20%-30% reduced

        8. ZSWAP compression is based on pages. However, we know metadata store is like a DB. If we can compress in columnar format, it will be more efficient.
            1. but if we offload to SSD, compressing the metadata is not necessary, and should not; since SSD is much bigger and compression cost extra time

    n. related materials
        1. Software-Defined Far Memory in Warehouse-Scale Computers    [2019, 55 refs, Google]
           https://research.google/pubs/pub48551/
           https://blog.acolyer.org/2019/05/22/sw-far-memory/
            1. mentioned in TMO paper. G-swap improves accessed bit accuracy by additionally tracking page age histograms and feeding them to machine learning.
               besides TMO, G-swap is the only known large-scale adoption of kernel-driven swapping for latency-sensitive datacenter applications

8. Software-Defined Far Memory in Warehouse-Scale Computers    [2019, 55 refs, Google]
   https://research.google/pubs/pub48551/
   https://blog.acolyer.org/2019/05/22/sw-far-memory/
    1. DRAM is expensive in datacenter. Far Memory sits between DRAM and SSD, actually compressed memory with Linux Kernel ZSWAP.
       Cold memory is classified by not accessed by T seconds - cold age threshold. performance impact is measured by rate of access on cold pages - promotion rate.
       Cold age threshold are updated per minute via a histogram algorithm, with feedback from promotion rate. The threshold tunes based on percentile, so histogram is implemented to capture statistics
       Offline ML-based auto-tuning are also used. GP Bandit algorithm treats it as a optimization problem and learns the search space shape. Like Hekaton Siberia, here's another example of using Machine Learning in Storage/Infra systems.
       Google WSC top 10% jobs have > 43% cold memory, majority having ~30%.
       Good paper as TMO as the reference architecture for how offload DRAM into compression or SSD, in industry large scale.
       This paper is also a good example of paper writing to separate Design and Implementation
    2. highlights
        1. ZSWAP default control plane did not meet Googles strict performance slowdown and CPU overhead budgets
           Google built a new one to identify cold pages and proactively migrate them to far memory
        2. identification of cold pages: the cold age threshold determines how many seconds we can go without a page being accessed before it is declared cold
        3. A good proxy metric for the overhead introduce by the system is the promotion rate: the rate of swapping pages from far memory to near memory
            1. P% promotion rate threshold set to 0.2%/minute
            2. Google maintain a promotion histogram for each job in the kernel, which records the total promotion rate of pages colder than the threshold T. This gives an indication of past performance
            3. we also want to be responsive to spikes
                1. The best cold age threshold is tracked for each 1 minute period, and the K-th percentile is used as the threshold for the next one
                   so we’ll violate approximately 100-K% of the times under steady state conditions
                2. If jobs access more cold memory during the minute than the chosen K-th percentile then the best cold age threshold from the previous minute is used instead
                3. Zswap is disabled for the first S seconds of job execution to avoid making decisions based on insufficient information
        4. ML-based auto-tuning - this is the good part
            1. The system also collects per-job cold-page histograms for a given set of predefined cold age thresholds. These are used to perform offline analysis for potential memory savings under different cold-age thresholds
            2. To find optimal values for K and S, Google built a model for offline what-if explorations based on collected far-memory traces, 
               that can model one week of an *entire WSCs* far memory behaviour in less than an hour. 
               This model is used by a Gaussian Process (GP) Bandit machine learning model to guide the parameter search towards an optimal point with a minimal number of trials. 
               The best parameter configuration found by this process is periodically deployed to the WSC with a carefully monitored phased rollout
            3. kstaled - a kernel daemon to periodically scan page access bit to determine cold age
                         accessed bit is set by the MMU whenever a physical page is accessed and it is up to the software to clear it
                1. Whenever kstaled updates the age of a page, it also updates two per-job histograms
                    1. cold age histogram, a histogram over page ages that tracks time T for which pages have not been accessed and
                    2. promotion histogram, a histogram recording the age of the page when it is accessed
        5. evaluation
            1. Q50 decompression latency is ~6us, all < 10us. Q50 compression ratio is 3x. the compression algorithm is lzo.
            2. CPU overhead is < 0.10%. well .. this is actually not bad at all.
    3. questions
        1. "Our system exposes K and S," - what are they exactly? the paper didn't mention 
        2. per Figure 9 for page decompress latency, what is the page size?
```

Papers about machine learning

```
1. Embedding-based Retrieval in Facebook Search    [2020, 63 refs]
   https://arxiv.org/abs/2006.11632
    1. very good paper. the recall step in search/recommendation system. reference architecture full stack and facebook engineering practices. including both training and serving.
       "Training Data Mining" negative samples are the key, "Hard Negative Mining"
    2. highlights
        1. "模型采用了点击样本为正样本，负样本则是由两部分组成一部分是曝光但是未点击的样本，另一部分则是随机从document 库中选择"
            1. "如果说排序是特征的艺术，那么召回就是样本的艺术，特别是负样本的艺术 "
            2. "为什么Youtube不用“曝光未点击”做负样本，而是拿抽样结果做负样本。而且这样做的还不仅仅Youtube一家，Microsoft的DSSM中的负样本也是随机抽取来的"
        2. "一个是text features，text embedding 采用了Character n-gram 的形式" .. "第二个是Location features。位置特征对于社交网络还是比较重要"  .. social embedding feature
            1. "paper 中通过实验证明了采用 character n-gram 比起 word n-gram 效果要更优"
        3. "线上serving" .. "facebook也是采用了自家的Faiss 库进行线上的ANN的查询" .. "且通过 quantization 来进一步缩短向量间相似性的计算时间"
           "离线通过spark构建document的索引，query的embedding在线进行计算，进行top-K召回"
           "全量的document进行索引是非常耗存储和费时的，所以facebook在构建索引的时候，只选择了月活用户，近期事件，热门的事件，以及热门group"
        4. "可以将召回的分数（也就是向量的相似度）作为ranking阶段的一个特征"
        5. "由于语义召回的结果召回高但是精度低，所以他们就采用了人工的方式对语义召回的结果进行标注，对每个query召回的结果进行标注"
        6. Hard negative mining (HNM).
            1. "把那些和positive sample很近的样本作为负样本去训练"
            2. "因为模型是采用mini-batch的方式进行更新的，所以对每个batch中的positive pairs，都随机一些非常相似的负样本作为训练集，模型效果提升非常明显"
            3. Hard positive Mainlining
                1. "模型采用了用户点击的样本为正样本，但是还有一些用户为点击但是也能被认为是正样本的样本。这块他们从用户的session日志中挖掘到潜在的正样本"
        7. Embedding Ensemble - "如何将多个模型融合的问题，采用不同正负样本比例训练出来的模型在不同的方面具有不同的优势，如何对这些模型进行融合"
            1. "第一种方案是采用加权求和的方式" .. "采用融合的当时对于单模型而言有4.39%的提升"
            2. Cascade Model "第二种是串行的方式，第二个模型在第一个模型的基础上训练。感觉就像bagging和boosting的区别" .. "模型也有3.4%的提升" .. "其实就是粗排"
            3. "为了能够使用FAISS，必须将多个模型产出的embedding融合成一个向量。做法也非常简单，将权重乘在user embedding或item embedding一侧，然后将各个模型产出的embedding拼接起来，再喂入FAISS"
        8. "简单的pytorch实现unified embedding model，帮助理解模型结构" - Query, Document 双塔结构
            1. https://github.com/liyinxiao/UnifiedEmbeddingModel
    n. related
        1. 负样本为王：评Facebook的向量化召回算法
           https://zhuanlan.zhihu.com/p/165064102
            1. 总之，我感觉，排序更受关注，很多问题被研究得更透彻。而召回，尽管"召回不存，排序焉附"，地位相当重要，但是受关注少，有好多基本问题还没有研究清楚。比如接下来，我们要谈到的， 诸如“拿什么样的样本训练召回模型”这样的基本问题，很多人还存在误区，习惯性照搬排序的方法，适得其反 。
            2. 在这种情况下， 2020年Facebook最新的论文《Embedding-based Retrieval in Facebook Search》（EBR） 更显难能可贵，值得每个做召回算法的同行仔细阅读。正所谓“实践出真知”，文中涉及的部分问题，哪怕你有推荐算法经验但只做过排序（比如一年前的我），都压根不会意识到，更不能给出解决方案。而在你实践过召回算法，特别是向量化召回之后，方能感觉到这篇文章切中召回工作中的痛点，“对症下药”
            3. good in-depth summary with broad knowledge compares

        2. Embedding-based Retrieval in Facebook Search：解读Facebook搜索中的召回技术
           https://blog.csdn.net/weixin_41089007/article/details/108292704

        3. Embedding-based Retrieval in Facebook Search
           https://zhuanlan.zhihu.com/p/152570715
            1. "在一个通常的搜索算法而言，一般分为两个步骤一个是召回一个是排序。基于embedding的语义召回主要在第一阶段，它要解决的问题是如何从千万个文本中找到相关的top-K个。难点有如下两个方面一个是如何构建千万级别的索引以及如何在线上进行服务。第二个难点在于如何在召回是同时考虑语义信息和关键词匹配的信息。

                facebook这篇文章从三个方面去阐述了他们应对的挑战--modeling, serving, and full-stack optimization.。所谓modelling其实就是如何建模的问题。在这个地方facebook提出了一种统一的embedding方式，也采用了经典的双塔结构，一侧是query，搜索者，上下文，另一侧则是document。"

        4. 《Embedding-based Retrieval in Facebook Search》阅读笔记
           https://wulc.me/2020/08/30/%E3%80%8AEmbedding-based%20Retrieval%20in%20Facebook%20Search%E3%80%8B%E9%98%85%E8%AF%BB%E7%AC%94%E8%AE%B0/
            1. 笔者认为这篇 paper 值得关注的点如下
                1. 召回模型的负样本的选取（为什么不能只选取曝光未点击的样本作为负样本，easy negative 与 hard negative）
                2. 新的召回策略如何克服当前 ranking system 的 bias
                3. 构建一个召回系统的常规流程及每个流程中的一些经验
```

Papers about Erasure Coding (EC)

```
1. Erasure Coding for Distributed Storage: An Overview    [2018, 77 refs]
   https://arxiv.org/pdf/1806.04437.pdf
    1. very good paper. The summarization tables are very helpful to pick codecs. many new EC directions to think about
    2. highlights
        1. regenerating codes
            1. reported that 98.08% of the cases have exactly one block missing in a stripe
            2. Minimum Bandwidth Regenerating (MBR)
            3. Minimum Storage Regeneration (MSR)
        2. locally recoverable codes
        3. novel ways to repair the ubiquitous Reed-Solomon code
        4. LRC regenerating codes
            1. codes where local codes are MSR/MBR
                1. question: what about global parities?
        5. repairing RS codes
            1. downloading 15 bits instead of 32 bits from 15 our 16 survival nodes
        6. EC codes using in realworld production
            1. MS Azure LRC
            2. HDFS Xorbas LR code
            3. Ceph: Clay code is simultaneously optimal in terms of storage overhead, repair bandwidth, optimal access and sub-packetization level
```

Misc papers about Cloud scheduling, Data lake, ect.

```
1. Scaling Large Production Clusters with Partitioned Synchronization    [2021 ATC, Best paper award, AliCloud, 0 refs]
  https://www.usenix.org/conference/atc21/presentation/feng-yihui
    1. Shared-state scheduler following Google Omega. Omega OCC scheduling suffers high conflicts in
        1) large cluster small tasks high contention scenario
        2) and staleness of local states 
        3) high contention of high-quality resources
       This paper proposes partitioned synchronization (ParSync) to mitigate. ParSync is deployed in Fuxi 2.0 (but seems not yet in large scale prod?). Techniques
        1) cluster state is partitioned, each local scheduler charges 1/N distinct partitioned state, and can first schedule jobs in own partition
        2) balance scheduling latency vs quality based on how fresh the local scheduler state is
       It more sounds a common partition strategy applied to schedulers, with a sync master (a bit like Mesos), rather than Google Omega approach
    2. highlights
        1. Problem with YARN - a single master scheduler
            1. the size of some of our clusters is close to 100k machines and the average task submission rate is about 40k tasks/sec, absolutely most tasks are < 10s
        2. Google Omega - shared state scheduler
            1. a master maintains the cluster state, which indicates the availability of resources in each machine in the cluster.
               There are multiple schedulers, each of which maintains a local copy of the cluster state by synchronizing with the master copy periodically.
               Each scheduler schedules tasks optimistically based on the (possibly stale) local state and sends resource requests to the master
            2. As multiple schedulers may request the same piece of resource, this results in scheduling conflicts.
               The master grants the resource to the first scheduler that requested it, and the other schedulers will need to reschedule their task.
               The scheduling conflicts and rescheduling overheads lead to high latency when the task submission rate is high
               which we validate in §4 using both analytical models and simulations
            3. Our results show that the contention on high-quality resources and the staleness of local states
               are the two main contributors to high scheduling latency as they both substantially increase scheduling conflicts
        3. Our strategy
            1. partition the cluster, each scheduler in charges one non-overlapping partition
            2. Adaptive scheduling strategy
                1. Quality-first, Latency-first, Adaptive, StateSync
            3. Conflict modeling
                1. using binomial distribution to model slot conflict, and to derive model, this part is useful 
                    E(Yi) = NK/S_idle - 1 + (1 - K/S_idle)^N
    3. questions
        1. Finally, we evaluate our solution in a high-fidelity simulation cluster with workloads sampled from the production clusters as shown in Figure 1b
            1. so .. this is not running in large scale production?
    n. related
        1. 获国际架构顶会ATC2021最佳论文！Fuxi2.0去中心化的调度架构详解 - Scaling Large Production Clusters with Partitioned Synchronization
           https://zhuanlan.zhihu.com/p/396562588
        2. Borg, Omega, and Kubernetes (2016)
           https://mwhittaker.github.io/papers/html/burns2016borg.html

2. Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores    [2020, 30 refs, VLDB20]
   https://databricks.com/wp-content/uploads/2020/08/p975-armbrust.pdf
    1. Lakehouse combines Hadoop + SQL data warehouse. The infra is built atop, and tightly coupled with Spark.
       It features in performant, mutable tables, atomic writes, lots of small files, time travel, with ACID transaction implemented with open interoperable Parquet format logs
       The core idea is simple, maintain object metadata in Delta table in ACID manner with transaction log; objects are in Parquet, easy for connecting more engines. transactions are in OCC format, no servers need to maintain the table state; users only need to launch servers to run queries
       Delta Lake can be however understood as an Object Store with multi-object atomic writes, consistency, time travel; plus streaming, delta objects update; and table store with transactional SQL, but opens everything interoperable (even metadata), and disaggregated (like Snowflake, but don't even need a all-time-run server to own anything).
       With Delta Lake, users can avoid running a separated message bus altogether and use a low-cost cloud object store with Delta to implement streaming pipelines with latency on the order of seconds
       The cloud native approach that publish both metadata and data as plain files in Object Store for interoperability, looks pretty like Hyperspace in Azure Synapse
       Parquet/ORC, bond/protocolbuf, etc public binary format made possible for binary parts of a database to be interoperable, just like json/xml/yaml made text parts interoperable
       very good paper. breakthrough that opens a new product paradigm and market type. 
    2. highlights
        1. problems to solve
            1. compared to traditional OLAP data warehouse
                1. support UPSERT, write in serializable isolation ACID transaction, read in MVCC snapshot isolation.
                   The SQL table storage is expected to be mutable and performant upon write transactions
                    1. unlike traditional data warehouse which usually only supports append data (or update is very slow), and may not support transactions 
                    2. Schema evolution supported: besides, schema change history is kept, and allow reading older Parquet objects without rewrite 
                    3. how to implement transaction ACID
                        1. a transaction log compacted into Apache Parquet format, and for time travel
                        2. Exactly-Once Streaming Writes are implemented by requiring each record having a unique key, and atomically updating a last version written together with each write
                2. atomic update for those involving multiple objects. UPSERT, DELETE and MERGE
                    1. can be required for GDPR compliance
                3. time travel and rollback
                    1. Data objects and log objects are immutable.
                    2. support MVCC and retention of deltas
                4. Streaming ingestion and consumption, Exactly-Once Streaming Writes with Spark
                    1. Write compaction: Spark writes small objects in low latency, then async compact them into
                    2. Fast tailing reads of new data: so it can be used as a message bus
                5. Connectors: ETL, Spark SQL, Spark Streaming
                    1. and allow reads to delta tables from Apache Hive, Presto, AWS Athena, AWS Redshift, and Snowﬂake
                    2. ETL and Change Data Capture (CDC) tools including Fivetran, Informatica, Qlik and Talend can write to Delta Lake
                6. Compared to Snowfalke data warehouse - interoperability
                    1. Snowfalke manages metadata by themselves in a separated, strong consistency service.
                       however self-managing is expensive, and add overhead in queries with an external computing engine (interoperability), and vendor lock-in
                    2. Delta Lake publishes all data and metadata as plain files in Cloud Object Store
                7. Caching
                    1. because objects are in delta and logs are immutable, they can easily be cached
                8. Data layout optimization
                    1. automatically optimizes the size of objects in a table and the clustering of data records (e.g., storing records in Zorder to achieve locality along multiple dimensions) without impacting running queries
            2. Limitations
                1. Delta Lake currently only provides serializable transactions within a single table, because each table has its own transaction log
                    1. my questions
                        1. WTF? how can you say you support SQL transaction .. In theory this should be able to implement in future
                2. for streaming workloads, Delta Lake is limited by the latency of the underlying cloud object store
                    1. my questions
                        1. bad .. this is an architecture limitation that is prohibitive to replace the stream part in Lambda architecture
                3. Delta Lake does not currently support secondary indexes (other than the minmax statistics for each data object),
                   but we have started prototyping a Bloom ﬁlter based index
                    1. my questions
                        1. OK .. this is so bad for an OLAP system / data warehouse. running on Cloud Object Storage (probably HDD)
                           Though some data warehouse choose full scan approach with no index, those are full SSD or in-memory
            2. cloud native
                1. the system builds atop Google Cloud / Azure Storage / AWS S3 / HDFS / Spark,
                2. and leverage the cloud services for data storage, metadata storage, logging, and to maintain consistency
                3. file and log format are published interoperable plain files in Object Stores, and in json or parquet format
        n. my questions
            1. from the performance evaluation, if to replace Lambda architecture, the latency is still too high compared to stream processing
               example of stream processing requiring low latency is 1) monitoring metrics 2) realtime analytics to respond user requests e.g. fraud detection, queries, recommendations 
            2. compared to a plain data warehouse, Delta Lake features in ACID transactions, update existing data, and integrating data warehouse with Cloud Storage
               but, a datalake should also include semi-structured or blobs/files beside table & SQL. How are they managed in ACID, and to support query, and the metadata catalog?
                1. i.e. how the Object Storage, and SQL tables, are combined in one store, interoperable?
            3. if the metadata are opened in Parquet files, on-disk, how are they made fast enough to support DB operations? compared to traditional DB
    n. related materials
        1. yishanhe blog: [VLDB'20] Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores
           https://yishanhe.net/delta-lake-high-performance-acid-table-storage-over-cloud-object-stores/
            1. useful summary, it captured most key points and provided much insight

        2. Databricks: Beyond Lambda: Introducing Delta Architecture
           https://www.youtube.com/watch?v=FePv0lro0z8
            1. // TODO

        3. Hyperspace: The Indexing Subsystem of Azure Synapse
           https://www.microsoft.com/en-us/research/publication/hyperspace-the-indexing-subsystem-of-azure-synapse/

        4. 星环科技：我们需要怎样的湖仓一体架构？
           http://m.blog.itpub.net/69925873/viewspace-2889130/
            1. useful to explain Lakehouse and 湖仓一体, i.e. what Delta lake brings
            2. highlights
                1. "除Databricks外，Snowflake以及一些云大厂进行了相关布局"
                2. "在日前星环科技春季发布周，星环科技公共事业部系统架构负责人徐流明指出，2010年后，随着大数据技术的兴起，数据应用场景更加多元化，出现实时计算、全文检索、机器学习，以及其他数据科学类分析需求，数据湖概念也随之而来。在这个阶段，大家的关注点更多在于如何用不同的技术栈支撑不同的数据分析场景，很多企业采用“数据湖+数据仓库”的混合架构处理结构化和非结构化等问题，但是对数据平台架构的合理性、可维护性、易用性没有太多关注，导致很多企业建设的数据平台架构非常复杂，为后期的平台迭代和运维等造成了很大问题。

                徐流明介绍，“湖+仓”混合架构中，数据湖和数据仓库是两套独立的技术体系混合部署在一个数据平台上，数据湖是基于Hadoop技术来实现，主要用于支撑多元异构的数据存储，去执行批处理、流处理等工作负载。数据仓库主要是基于MPP或者关系型数据库来实现，主要支撑结构化数据在OLAP场景下的BI分析和查询需求，由于湖和仓之间是互相独立的，需要通过ETL实现数据交换。这种架构可以在一定程度上解决企业多场景的数据分析需求，但也有一些明显的弊端。

                一是混合部署架构较为复杂，导致架构设计和项目实施交付成本较高，且后期平台运维难度较大;二是数据冗余非常明显，Hadoop和MPP属于分布式系统，为了保障数据的高可靠性一般通过冗余备份的方式实现，本身两种技术都已经做了数据冗余备份，但是采用混合架构无法避免有部分数据既存在Hadoop平台，又存在MPP平台，进一步增加了数据冗余比例，增加存储成本;三是数据链路过长，通常数据处理要先入湖，进行批处理后再入仓，由湖入仓需要ETL加载，影响查询时效性;四是容易产生数据一致性问题，无论由湖入仓，还是由仓入湖，混合架构下实质都是在两种数据平台间进行数据迁移，迁移过程难免会出现数据一致性问题，增加额外的数据校验成本。

                “湖+仓的混合架构是在数据平台架构演进过程中技术向业务妥协的一个产物，它并不是真正意义上的湖仓一体平台。”徐流明强调，“从技术角度看，湖仓一体是以多模型数据平台技术为依托，打破传统Hadoop+MPP混合部署模式，实现湖仓技术架构统一。通过一站式的多模型数据平台支撑数据湖、数据仓库、数据科学等多样化的数据分析场景。未来，湖仓一体作为新一代大数据技术架构，将逐渐取代单一数据湖和数据仓库架构。”"

        5. 深入分析Z-Order - 陈峰
           https://zhuanlan.zhihu.com/p/491256487
            1. good technique. OLTP uses primary index for a and secondary index for b, filter b range needs random access disk anyway
               but in OLAP, we can develop a total order of dimensions <a,b,c>, so that each of a,b,c retains its order (roughly, actually it can have reverse in small scope) in the total order of <a,b,c>. This is Z-Order
               in this way, OLAP doesn't need secondary index, it just needs an index for Z-Order. On disk, the data is also organized in Z-Order. So that fetching data only needs sequential scans
               compared to primary index of a along and a-order on disk, the cost of Z-Order is the scan range in Z-Order is larger, probably several times larger.

3. Silent Data Corruptions at Scale    [2021, 15 refs, Facebook]
   https://arxiv.org/pdf/2102.11245.pdf
    1. highlights
        1. SDC can come at device level: faulty transistors, design fault at corner cases, early life failures, heavy use degradation, end-of-life wear-out
        2. FB Compression Application: live case of how CPU SDC caused missing row in outcome
        3. Assembly Level Test Case - started from 420K code and then narrow down to 60 lines code reproducer
        4. Fault Tolerant Libraries
    2. related
        1. Silent Data Corruption - Google Cloud Platform Console Help
           https://support.google.com/cloud/answer/10759085?hl=en
            1. highlights
                1. "an impacted CPU might miscalculate data (i.e., 1+1=3)"
                2. google's handling
                    1. "by adding software checksums"
                    2. "When a substantially better test becomes available, we re-screen the fleet."
                    3. "When a defect is detected, that CPU is replaced"
                4. Hardware: Memory ECC, CPU ECC, disk parity bits, network CRC
                   Software: Self-checking, end-to-end checksums, cross check, fail-stop
                   System: Cloud backup, disaster recovery, e2e checksum, replica of important data, Periodic Verification, Periodic Verification
                   Operation improvements
                        improve code coverage: code sanitizers: memory addressability, leak sanitizers, thread sanitizers race contidion, undefined behavior sanitizer
                        Triage. Exercising Backup and Restore Mechanisms:

                5. more techniques
                    1. "When a substantially better test becomes available, we re-screen the fleet. When a defect is detected, that CPU is replaced"
                    2. "encrypt on one CPU and decrypt on another CPU and see if the data is consistent"
                    3. encrypt on one CPU and decrypt on another CPU and see if the data is consistent

4. Database Systems Performance Evaluation Techniques    [2008, 7 refs]
   https://zhuanlan.zhihu.com/p/402415858
   https://www.cse.wustl.edu/~jain/cse567-08/ftp/db/index.html
    1. OK .. actually most DB papers use TPC benchmarks, e.g. TPC-H
       https://www.tpc.org/information/benchmarks5.asp
       A survey - Section "5. Database Systems: Performance Evaluation Benchmarks" lists useful DB benchmarks
    2. Reliability evaluation, Security evaluation seem more cared for DB, but not the focus of this paper
```
