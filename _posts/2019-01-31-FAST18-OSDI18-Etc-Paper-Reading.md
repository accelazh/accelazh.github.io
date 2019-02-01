---
layout: post
title: "FAST18 OSDI18 Etc Paper Reading"
tagline : "FAST18 OSDI18 Etc Paper Reading"
description: "FAST18 OSDI18 Etc Paper Reading"
category: "storage"
tags: [storage, fast, paper]
---
{% include JB/setup %}


Summary of paper reading notes. Papers collected from FAST18, OSDI18, and etc from [Build My Academic Paper Feedback Network](/storage/Build-My-Academic-Paper-Feedback-Network), and Deep Learning related papers from [CS231n](http://cs231n.stanford.edu/syllabus.html). Search "very good" > "good" > "interesting" for recommendations.

Service Fabric: A Distributed Platform for Building Microservices in the Cloud

```
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
```

Store, Forget, and Check: Using Algebraic Signatures to Check Remotely Administered Storage

```
2. Store, Forget, and Check: Using Algebraic Signatures to Check Remotely Administered Storage    [2006, 406 refs]
   ftp://ftp.cse.ucsc.edu/pub/darrell/schwarz-icdcs06.pdf
    1. we can fetch the signature from parity nodes, rather than fetch data and then calculate signature,
       to verify data integrity, because "calculating parity and taking a signature commute"
```

The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing

```
1. The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing    [2015, 211 refs]
   https://ai.google/research/pubs/pub43864
    1. interesting paper. semantics & primitives framework for stream processing
    2. highlights
        1. windowing, etc, are put into data points flowing to next node
           rather than saved as states in nodes
            1. so that, the workflow looks similar to mapreduce
               i.e. +window=>key&split, agg=>merging&reduce
    3. related
        1. 阿莱克西斯 - (十)简单解释: 分布式数据流的异步快照(Flink的核心)
           https://zhuanlan.zhihu.com/p/43536305
        2. 阿莱克西斯 - 评:Streaming System(简直炸裂,强势安利)
           https://zhuanlan.zhihu.com/p/43301661
```

Beyond TrueTime: Using AugmentedTime for Improving Spanner

```
2. Beyond TrueTime: Using AugmentedTime for Improving Spanner   [2013, 11 refs]
   https://cse.buffalo.edu/~demirbas/publications/augmentedTime.pdf
    1. good paper. as recommended in 简单解释Augmented Time(前篇)
       https://zhuanlan.zhihu.com/p/44319138
       it proposed a way to use TrueTime but without commit-wait
    2. how it works
        1. perspectives: different ends of tracking asyc distributed systems
            1. Spanner's TrueTime, using strick clock to ensure external consistency
            2. Causal consistency using Vector Clock, totaly ignoring wall clock
        2. We try to combine the good of two worlds
            1. within commit-wait time, Spanner TT cannot tell Tx ordering,
               but Causal consistency still can
            2. if two Tx has overlapped keys, they has Causal consistency
        3. Vector clock compression
            1. if Server A didn't receive Server B for e time, where e is the
               TrueTime max time drift. Sever A can omit B's vector clock.
    3. questions
        1. need to make sure the compressed vector clock size is reliable
           in all production cases.
    4. related
        1. what is Spanner's extenal consistency?
            1. if Tx1 commits before Tx2, then Tx1's commit timestamp < Tx2's
               otherwise, it may happen that
                1) Tx2 committed after Tx1. but Tx2 has a smaller timestamp then Tx1
                2) a client lookup value by timestamp, and got Tx1's value.
                   Although Tx2 is expected to have already overridden Tx1's
            2. why need commit-wait to ensure external consistency?
                1. Suppose Tx2 commits after Tx1
                     Tx2 obtains commit timestamp by max(server B, server C)
                     Tx1 obtains commit timestamp by max(server A, server B)
                   if timestamp C < timestamp A, and timestamp B is very small.
                   it's possible Tx2 got a smaller commit timestamp than Tx1.
                     By commit-wait, Tx1 locks blocking Tx2, until
                       timestamp B,C become bigger than
                         prev Tx1's commit timestamp obtained from A.
                2. see: 简单解释Spanner的TrueTime在分布式事务中的作用
               https://zhuanlan.zhihu.com/p/44254954
                    1. very good
            3. Google cloud doc - external consistency
               https://cloud.google.com/spanner/docs/true-time-external-consistency?hl=zh-cn
```

SuRF: Practical Range Query Filtering with Fast Succinct Tries

```
1. SuRF: Practical Range Query Filtering with Fast Succinct Tries    [2018, 6 refs]
   https://db.cs.cmu.edu/papers/2018/mod601-zhangA-hm.pdf
    1. SIGMOD 2018 best paper. SuRF against BloomFilter to support range query, but higher false positive, and high update cost. FST as index has high compression rate, but same high update cost issue.
    2. highlights
        1. Fast Succinct Trie (FST)
            1. compressed index of compression ratio near information-theoretic lower bound.
               accurate. support range query. query speed comparable with pointer based index.
               high update cost. built with one scan.
            2. Built by fast bitmap-based LOUDS-Dense for top level nodes which are frequently accessed,
               plus space-efficient LOUDS-Sparse for other lower-level nodes
            3. Query by rank & select bit operation, modern ones can be optimized to O(1)
                1. Modern rank & select implementations [30, 43, 53, 58]
                2. paper optimizations
                    1. all bit-sequences in LOUDS-DS require either rank or select, but not both
                    2. Rank/Select, use sampled precomputed LUT
                    3. Label search, use 128-bit SIMD
        2. SuRF
            1. Trimmed by FST. Has FalsePositives. Compared against BloomFilter.
               Can use hash(key) or key suffix to tweak. Suppose range query
            2. problems compared to BloomFilter
                1. from Evaluation, Figure 8, false positive rate is higher
                    1. RocksDB case 40% slower SuRF than BF if none query key exists in dataset
                2. same with FST, e.g. high cost of update.
                3. effectiveness depends on the distribution of keys
        3. Others
            1. RUM Conjecture [16]: for read, update, and memory, one can only optimize two at the cost of the third
            2. There are three ways to define “close” [10].
               Suppose the information-theoretic lower bound is L bits.
               A representation that uses L+O (1), L+o(L), and O (L) bits is called implicit, succinct, and compact, respectively.
               All are considered succinct, in general.
    n. related articles
        1. SuRF: 一个优化的 Fast Succinct Tries
           https://zhuanlan.zhihu.com/p/38385054
           Succinct Data Structure
           https://zhuanlan.zhihu.com/p/38194127
        2. TerarkDB - 我们发布了一款划时代的存储引擎
           https://zhuanlan.zhihu.com/p/21493877, https://github.com/simongog/sdsl-lite 
           如何评价国产高性能存储引擎 TerarkDB
           https://www.zhihu.com/question/46787984/answer/103359271
        3. 大数据时代的压缩表现形式
           https://www.oreilly.com.cn/ideas/?p=168
        4. Succinct: Enabling Queries on Compressed Data
           https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/agarwal
```

Taming Performance Variability

```
2. Taming Performance Variability    [1 refs, 2018]
   https://www.usenix.org/system/files/osdi18-maricq.pdf
    1. Use foundamental statistics methods to tell performance results that:
        1) don't follow normal distribution
        2) is stationary
        3) how many samples needed to reach desired confidence level (CONFIRM)
        4) Steering Clear of Pitfalls - practical tips
    2. highlights
        1. Using Shapiro-Wilk test [55], we reject the test result distribution follows normal distributions. so we use nonparametric analysis
        2. Using Augmented Dickey-Fuller (ADF) [15] test, we find all test results are stationary (median, variance, etc don't change over time)
        3. massive amount of data collected on CloudLab public available
        4. methods to calculate confidence interval (CI) with confidence level
        5. Steering Clear of Pitfalls - defensive practices
            1. Randomize experiment orderings to expose effects that they might have on each other
            2. Perform sensitivity analyses with respect to the hardware configuration
            3. carefully consider whether they need features like NUMA, hyperthreading, complex memory hierarchies, etc. before selecting servers that have them
            4. It is tempting to treat repeated experiments as independent. Test for independence
            5. Be careful on shared infrastructure
                1. Studies have found high CoVs in commercial clouds [18, 29]—particularly for network and disk operations—and the long performance tails in clouds are well-known [14]
    3. related works
        1. Scientific Benchmarking of Parallel Computing Systems - Twelve ways to tell the masses when reporting performance results    [2015, 77 refs]
            1. test 120 papers HPC performance improvements are statistics reproducible
            2. Common Best/Worst Practices
```

Write-Optimized and High-Performance Hashing Index Scheme for Persistent Memory

```
3. Write-Optimized and High-Performance Hashing Index Scheme for Persistent Memory    [2018m 0 refs]
   https://www.usenix.org/conference/osdi18/presentation/zuo
    1. interesting paper. consistency data structures optimized for PM is a big topic.
       this paper is for hash table state-of-art. good for the hash table index design.
    2. highlights
        1. Tree-based vs Hashing Index Structures
            1. data structures in PM should avoid inconsistency when system failure occurs
        2. Challenges of Hashing Indexes for PM
            1. High Overhead for Consistency Guarantee
            2. Cost Inefficiency for Resizing Hash Table
        3. To avoid hash collision
            1. table structure
                1. each hash bucket has multiple slots, thus small key-value packs into CPU cacheline
                2. one key has two hash function and thus two hash locations.
               this greatly increase "load balance" and reduce collision
                3. top-level + bottom-level of half size. if top full, put to bottom
            2. at most one kv item movement for each insertion
                1. try each bucket slot alternatives above,
                   if all full, insertion fail
                2. anyway this avoids generate more writes or cascading writes to PM
            3. problems
                1. more memory consumption.
                    1. but two-hash scheme increase balance however, so higher load-factor is allowed.
                2. fail if inseration find not slots even in alternatives
                   thus need hashtable resizing
        4. hashtable resizing - interesting design
            1. 2x size enlarge. 2x TL allocated; old TL => BL; old BL => delete
               old BL data needs to put into table again, thus at max 1/3 data rehashed.
        5. Low-overhead Consistency Guarantee
            1. NVM consistency general techniques
                1. To achieve data consistency in NVM, it is essential to ensure the ordering of memory writes to NVM [17, 35, 64]
                2. We need to use the cache line flush instruction (CLFLUSH for short), e.g., clflush, clflushopt and clwb, and memory fence instruction (MFENCE for short), e.g., mfence and sfence, to ensure the ordering of memory writes
            2. howto: a bit token per each slot at the header of a bucket
                1. delete, insertion, by atomic switch token bit
                2. update
                    1. if has empty slot in same key location, use shadow write
                    2. otherwise, using logging
                3. problem
                    1. looks like here the operations assume single-threaded
                       otherwrite the token bit operation can conflict
            3. Concurrent Level Hashing
                1. we allocate a fine-grained locking for each slot.
                   When reading/writing a slot, the thread first locks it.
```

RobinHood: Tail Latency-Aware Caching — Dynamically Reallocating from Cache-Rich to Cache-Poor


```
4. RobinHood: Tail Latency-Aware Caching — Dynamically Reallocating from Cache-Rich to Cache-Poor    [2018, 3 refs]
   https://www.usenix.org/conference/osdi18/presentation/berger
    1. good paper. can we use cache to reduce P99? - Yes
       dynamic cache partition in aggregation cache against tail latency.
        the paper is unique because it thinks we can use cache to reduce tail latency
        rather than as traditionally to improve hit rate or reduce average latency
    2. highlights
        1. The RobinHood tradeoff
            1. Sacrifice performance of some backends - up to 2.5x higher latency
            2. Reduce latency of bottleneck backends - typically 4x lower latency
        2. how it works
            1. design cache to improve tail rather than improve average
                1. e.g. issue, backends with higher query rates have more opportunities for their objects to be admitted into the cache
            2. By reallocate cache space.
                1. RobinHood repeatedly taxes every backend by reclaiming 1% of its cache space,
                   identifies which backends are cache-poor,
                   and redistributes wealth to these cache-poor backends
                2. RobinHood use RBC as the measure of how cache-poor a backend is
                   RBC is reuqest blocking count, the counts of times a backend produce slow queries
                3. RBC threshold is determined by set S, i.e. request set that are around P99
        3. from test evaluations, the RobinHood results are crazily good
    3. problems
        1. actually the paper missed one point.
           tail latency can come from long queue, so more cache or replica you have,
           less queue length hits backend, so lower tail latency
```

Fault-Tolerance, Fast and Slow: Exploiting Failure Asynchrony in Distributed Systems

```
5. Fault-Tolerance, Fast and Slow: Exploiting Failure Asynchrony in Distributed Systems    [2018, 0 refs]
   https://www.usenix.org/conference/osdi18/presentation/alagappan
    1. SAUCR - replication by buffer in-memory updates, trade availability for performance.
       react to Simultaneity of Failures, by switch in-memory mode to disk flush mode.
    2. highlights
        1. Replication Protocols: Paxos, Viewstamped, Raft
            1. Disk-durable approach, vs Memory-durable approach
        2. Situation-Aware Updates and Recovery
            1. dynamically (based on the situation) decide how to commit updates
        3. state charts "Figure 5: SAUCR Summary and Guarantees"
    3. problems
        1. 3 node failure which holds a complete replication set is possible in large-scale cloud.
           also, site power outage is also possible.
           So, the in-memory only replication looks not reliable enough nowadays seems
        2. when memory is full, we still need to flush to disk
           so the memory performance gain is not sustainable
```

Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems

```
8. Fail-Slow at Scale: Evidence of Hardware Performance Faults in Large Production Systems    [2018, 6 refs]
   https://www.usenix.org/node/210509
    1. Fail-slow hardware is not rare. Let's write a paper for evidence
       interesting paper. we architect to tolerate node failure, but what about fail-slow?
    2. highlights
        1. Important Findings and Observations
            §3.1 Varying root causes: Fail-slow hardware can be induced by internal causes such as firmware bugs or device errors/wear outs as well as external factors such as configuration, environment, temperature, and power issues.
            §3.2 Faults convert from one form to another: Fail-stop, -partial, and -transient faults can convert to fail-slow faults (e.g., the overhead of frequent error masking of corrupt data can lead to performance degradation).
            §3.3 Varying symptoms: Fail-slow behavior can exhibit a permanent slowdown, transient slowdown (up-and-down performance), partial slowdown (degradation of sub-components), and transient stop (e.g., occasional reboots).
            §3.4 A long chain of root causes: Fail-slow hardware can be induced by a long chain of causes (e.g., a fan stopped working, making other fans run at maximal speeds, causing heavy vibration that degraded the disk performance).
            §3.4 Cascading impacts: A fail-slow hardware can collapse the entire cluster performance; for example, a degraded NIC made many jobs lock task slots/containers in healthy machines, hence new jobs cannot find enough free slots.
            §3.5 Rare but deadly (long time to detect): It can take hours to months to pinpoint and isolate a fail-slow hardware due to many reasons (e.g., no full-stack visibility, environment conditions, cascading root causes and impacts).
        2. Suggestions
            §6.1 To vendors: When error masking becomes more frequent (e.g., due to increasing internal faults), more explicit signals should be thrown, rather than running with a high overhead. Device-level performance statistics should be collected and reported (e.g., via S.M.A.R.T) to facilitate further studies.
            §6.2 To operators: 39% root causes are external factors, thus troubleshooting fail-slow hardware must be done online. Due to the cascading root causes and impacts, full-stack monitoring is needed. Fail-slow root causes and impacts exhibit some correlation, thus statistical correlation techniques may be useful (with full-stack monitoring).
            §6.3 To systems designers: While software systems are effective in handling fail-stop (binary) model, more research is needed to tolerate fail-slow (non-binary) behavior. System architects, designers and developers can fault-inject their systems with all the root causes reported in this paper to evaluate the robustness of their systems
        3. many detailed error info and stories
           the paper is very informative
```

Maelstrom: Mitigating Datacenter-level Disasters by Draining Interdependent Traffic Safely and Efficiently


```
9. Maelstrom: Mitigating Datacenter-level Disasters by Draining Interdependent Traffic Safely and Efficiently    [2018, 0 refs]
   https://www.usenix.org/conference/osdi18/presentation/veeraraghavan
    1. interesting paper.
       Maelstrom to auto, safely, efficiently, drain traffic from one datacenter to another
       in production at Facebook for 4+ years, successfully recovered from 100+ datacenter outage
    2. highlights
        1. usecase:
             microservice running in datacenter.
             we know datancener is going to be taken down (e.g. hurricane)
             we want to safely transfer traffic to another datacenter
        2. challenges
            1. manage the dependency of traffic during draining
            2. parallel draining, as fast as possible to mitigation
        3. design
            1. primitives:
                shifting traffic, reallocating containers, changing configuration, moving data shards
                Inter-system dependencies, resource constraints, runbook
            2. validation: maintaining health and SLAs
               closed feedback loop to execute step by step
            3. scheduler: critical path analysis, parallelism
            4. testing: drain test on internal traffic, per weekly basis
               and driven the evolution of Maelstrom
               and find missed dependencies
        3. infrastructure
            1. PoP: public IP points to one of the tens of edge locations, i.e. PoP.
               A PoP consists of a small number of servers, typically co-located with a peering network [43,54]
               A PoP server terminates the user's SSL session and then forwards the request on to an L4 load balancer (Edge LB)
                which forwards the request on to a particular datacenter
        4. more
            1. Preventing Resource Contention
                1. Verifying capacity, Prioritizing important traffic, Graceful degradation
            2. Fault tolerance
                1. save data in DB (a highly available, multi-homed DB)
```

Deconstructing RDMA-enabled Distributed Transactions: Hybrid is Better!

```
10. Deconstructing RDMA-enabled Distributed Transactions: Hybrid is Better!    [2018, 0 refs]
    https://www.usenix.org/conference/osdi18/presentation/wei
    1. compare one-sided vs two-sided (RPC implementions) RDMA w.r.t. transaction performance, and various optimizations.
    2. highlights
        1. backgrounds
            1. One-sided primitive provides higher performance and lower CPU utilization
            2. two-sided primitive simplifies application programming and is less affected by hardware restrictions
        2. main findings
            1. One-sided primitive has better performance than two-sided with the same round trips
            2. Two-sided primitive has better scalability with small payloads in large clusters
            3. Two-sided primitive can be faster than one-sided when receiving ACK is done off the critical path
        3. Passive ACK
            1. introduced in this paper. ACK is done off critical path.
            2. passive ACK can save half of the messages (replies) when
               piggybacking the reply message with the requests
        4. optimizations
            1. Coroutine
            2. Issue reads/writes in transaction in parallel
            3. Doorbell batching
    3. problems
        1. how to ensure the atomicity between step Verification to Commit?
```

Computation Reuse in Analytics Job Service at Microsoft

```
11. Computation Reuse in Analytics Job Service at Microsoft    [2018, 2 refs]
    https://www.microsoft.com/en-us/research/uploads/prod/2018/03/cloudviews-sigmod2018.pdf
    1. interesting paper. The computation subgraph overlapping, materialization, reuse in SCOPE, by CloudView, related to Azure ADLS.
       40%+ jobs overlap, with CloudView improved latency by 40%+ and CPU hour by 30%+
    2. highlights
        1. Overlap analysis (which is good)
            How wide in space: percentage of overlap
                1. 45%+ jobs overlapping
            How wide in time: frequency of overlap
            How deep: overlap is consumed how many times
            What structure: overlap in cluster unit and in business unit
                            operator and overlap
            Impact: frequency, runtime, output size, and relative costs
            1. Useful observations
                1. Users tend to start analytics scripts from other people's
                2. There is a data producer/consuder, with multiple consumers process same input, and often end up duplicating post-processing
        2. How to reuse overlaps
            Use online updating materialized view.
            Computation in subgraph are identified/tracked by signatures
            1. Debuggability
                1. users can trace what materialized view are created/used,
                   drill down, control reuse, and replay a job
        3. CloudView Analyzer - the Feedback Loop
            1. Rather than pick materialized views by cost estimates,
               which may have low confidence of actual cost vs future benefits
            2. How to get the correct cost
                1. enumerating all possible subgraphs of all jobs seen within a time window
                   the subgraphs have actually been used and provide runtime statistics
                2. query operators to executed operators are linked,
                   runtime statistics are collected as fine-grain to individual operator
            3. others
                1. phsical design of view.
                   same view of different physical designs can even be treated as different views
                2. expiry and purging.
                   track the lineage of the inputs of the view
        4. CloudView Runtime
            1. metadata pull:
                one request per-job to fetch all overlaps relevant
                done creating an inverted index
                1. metadata service is backed by AzureSQL, providing exclusive locks
            2. online materialization
                1. materialized view are created as part of query processing with minimal overhead. instead of create them long priori
            3. synchronization
                1. build-build synchronization
                    1. metadata service of Azure SQL, and exclusive locks
                2. build-use synchronization
                    1. early materialization: available even before it finishes
                    2. early materiaization also acts as a checkpoint
```

F1 Query: Declarative Querying at Scale

```
1. F1 Query: Declarative Querying at Scale [2018, 0 refs]
   http://www.vldb.org/pvldb/vol11/p1835-samwel.pdf
    1. very good paper. dense. like spanner paper, tells the next division of DB evolution.
       unifies query, data source, and SQL and its extensions. proposed new concept "Robust Performance"
    2. highlights
        1. foundamentals
            1. Decouples storage from query processing.
               F1 Query only in chart of query processing.
               Storage connects Spanner, BigTable, CSV, ColumnIO, Capacitor, ETL, etc
                1. I would say F1 Query did find the best usecase and avoided compete work with Spanner again
            2. F1 Query is feasible because of Google Jupiter [56] datacenter networking,
               which allows any server to server in cluster communicates with sustainable bandwidth of 10Gb/s
                1. e.g. the repartition operator
        2. unify of query workload
            1. interactive query
                1. centralized mode
                2. distributed execution
                    1. fully compatible with SQL, with left/right/full join, lookup/hash joins, fully supported, plus ARRAY typed, protocol buffer, etc
                    2. DAG, query fragments
                       exchange operator, repartition; with flow control
                       dynamic assign fragments to avoid tail latency
                       big aggragation by earilier smaller secondary aggregations
                3. performance concerns
                    1. primary causes for query performance issue is skew and sub-optimal data source access patterns
                    1. DAG forks are sensitive to different data consumption speeds, and distributed deadlocks
                    2. the choice of partitioning function has strong impact on performance
                       F1 query "dynamic range repartition"
                        1. observation: distribution observed at one input plan fragment partition
                                        often closely approximates the overall data distribution
            2. batch query
                1. Using MapReduce, future may leverage FlumeJava
                    1. Fault tolerance are handled by MapReduce
                2. Use SQL as the pipeline language
                3. metadata saved in Spanner database
                4. performance concerns
                    1. batch mode can materialize teh smaller inputs into disk-based lookup tables called SSTable, for lookup join
                        1. leverage distributed caching layer, e.g. TableCache
        3. query optimizer
            1. query optimizer development is notoriously complex.
               F1 Query use same query optimizer for interactive and batch.
               F1 Query use mainly heuristic rules for query optimizer,
                future to ehance distributed statitics, and use cost-based optimization rules
            2. more
                1. all plan tree structures are immutable
                2. generated code enables a DSL language for query planning and contains methods
                   saves engineers considerable time
                3. logical query plan optimization
                    1. Rules applied include filter pushdown, constant folding, attribute pruning,
                       constraint propagation, outer join narrowing, sort elimination,
                       common subplan deduplication, and materialized view rewrites
                4. physical query plan construction
                    1. Each resulting physical operator is represented as a class that tracks multiple data properties,
                       including distribution, ordering, uniqueness, estimated cardinality, and volatility
                    2. The optimizer also uses the physical plan properties to decide whether
                       to run a query in central or distributed mode
        4. unify of extension
            1. supports custom data sources as well as
               user defined scalar functions (UDFs),
               aggregation functions (UDAs),
               and table-valued functions (TVFs)
                1. group multiple SQL UDFs, UDAs, TVFs into modules
            2. supports Lua scripts, managed Java, and compile un-managed C++
               they remain in separated process to isolate failures
            3. TVF example
                1. machine-learning steps like modle training
                2. other company teams can add new TVF data source without involve F1 devs
            4. RPC for TVF evaluation uses persistent bidirectional streaming network connection
               to send input rows to the UDF server and receive output rows back
        5. Robust Performance
            1. this is new concept. performance gracefully degrades in the presence of
               unexpected input sizes, unexpected selectivities, and other factors
                1. otherwise, "performance cliff"
            2. Performance cliffs create several problems
                1. unpredictable performance and a poor experience for the user
                2. optimizer choices become error-prone because a small cardinality estimation error
                   may be amplified into a large cost calculation error
                3. in parallel query execution, small load imbalances between compute nodes may turn
                   into large disparities in elapsed runtimes
            3. the principle idea is, instead of using a binary switch at optimization time or execution,
               the execution operator incrementally transitions between modes of operations
                1. Related: SmoothScan [16] and dynamic destaging in hash joins [52]
        6. others
            1. protocol buffer are statically typed, and integer field identifier, thus gain performance optimize than JSON
               some data source even vertical shredding the messages into columnar format [51]
            2. production metrics:
                Interactive mode: 450K query/sec, easily handle peak of 2x. Q99 latency in 1s to 10s.
                Batch mode: 55K query/day, 8 to 16 PB data processed per day. Q50 latency at 500s
                growth: query throughput doubled in four quarters
            3. analysis in related works. this is interesting informative
            4. related technologies in Google. this is useful for understand how these teams compete
                1. PowerDrill, interesting
            5. future work & improvements
                1. F1 Query achieves significant synergy benefits compared to the situation
                   where many separate systems exist for different use cases
                2. F1 Query does not yet match the performance of vectorized, columnar execution engines
                   (e.g. Vectorwise [63]) because of its row-oriented execution kernel.
                   A transition to a vectorized execution kernel is future work
                3. F1 Query also does not support local caches for data in the query engine’s native format
                   Currently, F1 Query relies on existing caches in the data sources, or remote caching layers such as TableCache [50]
                    1. To support in-memory or nearly-in-memory analytics, such as offered by PowerDrill [39],
                       F1 Query would need to support local caching on individual workers and locality-aware work scheduling
                       that directs work to servers where data is likely to be cached
                4. The use of remote data sources also makes it harder to collect statistics for use in query optimization,
                   but we are working to make them available so that F1 Query can use cost based optimization rules
                5.  we are working on techniques to improve how F1 scales in, for example,
                    by running medium-sized distributed queries on only a few servers,
                    thereby reducing the cost and latency of exchange operations
```

BrainWave: A Configurable Cloud-Scale DNN Processor for Real-Time AI

```
1. BrainWave: A Configurable Cloud-Scale DNN Processor for Real-Time AI (Microsoft)    [2018, 1 refs]
   https://www.microsoft.com/en-us/research/uploads/prod/2018/06/ISCA18-Brainwave-CameraReady.pdf
    1 interesting. Microsoft's datacenter-level NPU architecture, in compare with Google's TPU [10]
    2. highlights
        1. how production-level is BrainWave project
            1. on FPGA chip. datacenter-level.
               runs multiple FPGA models in >10K nodes production
        2. Training is primarily a throughput-bound workload
           Inference, can be much more latency sensitive
            1. BrainWave "real-time AI" DNN inference with no minibatching
               much lower with equivalents such as GPGPU on a watt-for-watt basis
        3. designs
            1. single-threaded SIMD ISA
            2. on-chip SRAM memories TB/sec bandwidth
            3. hierarchical decode and dispatch (HDD)
            4. vector-level parallelism (VLP)
            5. maps these parallelized vector operations to a flat,
               one-dimensional network of vector functional units
        4. latency-centric metrics based on critical-path analysis
            1. cycles on Unconstrained Dataflow Machine (UDM)
            2. cycles on Structurally-constrained Dataflow Machine (SDM)
            3. BW NPU
```

E2FS: an elastic storage system for cloud computing

```
1. E2FS: an elastic storage system for cloud computing    [2018, 12 refs]
   https://link.springer.com/content/pdf/10.1007%2Fs11227-016-1827-3.pdf
    1. interesting work. not to say this paper study is abundant enough, but the area of thinking is worthwhile.
       dynamic replication/EC schema in fine-grain of per extent/object or even data block level.
    2. highlights
        1. data classification - by VPT visit time per period
        2. replication scheme - 3x to 0~3+n replica
            1. problem: less than 3x ignores reliability SLA
        3. distribution rate - how many nodes to include all M data blocks - N node / M
        4. copyset paper
    3. my thinkings
        1. Dynamic fine-grain data replication and EC schema.
            Previous: whole cluster use same replication schema (e.g. 3x), or same EC schema (e.g. RS 4+2)
                      we must be able to read from any replicated instances, instead of only master. This is important for tail reduction.
            Now: Fine-grain: per extent/object, per group of extent/object, per data classification, can use different schemas
                             replication unit can be data block level, rather than per whole extent/object
                 Multi-layer Hot/Cold: for hot and cold data, we can apply different stages for different schemas, e.g. hot/cold EC
                 Burst instances: Replicate extra instance for hot traffic, e.g. an extra extent/object instance, an extra EC fragment instance.
                               More, we can replicate only extra data blocks, and group extra blocks from multiple different extents/objects as a new instance.
            About data classification: peak, throughput, frequency
                High peak, low general throughput, low frequency: cold spike
                high general throughput, high frequency, high or few spikes: high workload
                low general throughput, high frequency, low spike: really?
                low general throughput, low frequency, low spike: real cold
```

Improving Docker Registry Design Based on Production Workload Analysis

```
2. Improving Docker Registry Design Based on Production Workload Analysis    [2018, 6 refs]
   https://www.usenix.org/conference/fast18/presentation/anwar
    1. docker registry workload trace analysis based on IBM Cloud Container Registry
    2. highlights
        1. what to think/analyze about the collected data?
            1. What is the general workload the registry serves? What are request type and size distributions? (§4.1)
            2. Do response times vary between production, staging, pre-staging, and development deployments? (§4.2)
            3. Is there spatial locality in registry requests? (§4.3)
            4. Do any correlations exist among subsequent requests? Can future requests be predicted? (§4.4)
            5. What are the workload’s temporal properties? Are there bursts and is there any temporal locality? (§4.5)
        2. main findings (but most are trival)
            1. GET requests dominates
            2. 65% and 80% of all layers are smaller than 1 MB and 10MB
            3. yonger and non-production registries experience lower load
            4. response times correlate with registry load and hence also depend on age
            5. Registry accesses to layers, manifests, repositories, and by users are heavily
                1. can be leveraged by caching
            6. There is a strong correlation between PUT requests and subsequent GET manifest and GET layer requests
                1. can be leveraged for prefetch
            7. While there are weak declines in request rates during weekends,
               we did not find pronounced repeated spikes that can be used to improve resource provisioning
        3. Two-level Cache
            1. We do not have to deal with possible cache invalidation as layers are content addressable
               and any change in a layer also changes its digest
```

Towards Web-based Delta Synchronization for Cloud Storage Services

```
3. Towards Web-based Delta Synchronization for Cloud Storage Services    [2018, 6 refs]
   https://www.usenix.org/conference/fast18/presentation/xiao
    1. web-based delta sync for net drive apps. innovative reverse sync protocol
    2. highlights
        0. why web-based delta sync?
            1. Dropbox, SugarSync, Google Drive, iCloud Drive, and Microsoft OneDrive
               a lot of efforts have been made to improve their network-level efficiency,
               such as batched sync, deferred sync, delta sync, compression and deduplication [24, 25, 27, 37, 38, 46]
            2. delta sync is not available for web
               the most pervasive and OS-independent access method
            3. WebRsync, access file using HTML5 File APIs
        1. Server-side Overhead Profiling
           Checksum searching and block comparison occupy 80% of the computing time
            1. Replacing MD5 with SipHash in Chunk Comparison 
            2. Reduce Checksum Searching by Exploiting Locality of File Edits
            3. A Series of attempts of other techs
                1. Native Extension: leverage the native client for web browsers.
                2. WebRsync-Parallel: using HTML5 web workers to avoid stagnations
        2. Core improvements
            1. WebRsync: web-based delta sync using JavaScript and Html5
                1. server tells client what's new by passing checksum listing
            2. WebR2sync: Reverse the rsync process by moving computation-intensive operations from client with JavaScript to server
                1. client tells server what it has by passing checksum listing (should-be?)
                   thus costly search & compare are shifted to server-side
            3. WebR2sync+: By exploiting the edit locality and trading off hash algorithms
        3. related
            1. CDC - Change Data Capture
               https://en.wikipedia.org/wiki/Change_data_capture
            2. CDC - Content defined chunking (CDC) [35]
```

FStream: Managing Flash Streams in the File System

```
1. FStream: Managing Flash Streams in the File System    [2018, 7 refs]
   https://www.usenix.org/conference/fast18/presentation/rho
    1. interesting work. SSD/NVMe "streams" are entering standard now. How should we leverage it?
       application tells stream vs FTL tells stream vs this paper filesystem tells stream.
       FStream robustly achieves a near-optimal WAF (close to 1).
    2. highlights
        1. related works
            1. The first strategy would map application data to disparate streams based on an understanding of the expected lifetime of those data
               For example, files in different levels of a log-structured merge tree could be assigned to a separate stream
            2. The other strategy aimed to “automate” the process of mapping write I/O operations to an SSD stream with no application changes
               For example, the recently proposed AutoStream scheme assigns a stream to each write request based on estimated lifetime from past LBA access patterns
            3. The above sketched strategies capture the two extremes in the design space—application level customization vs. block level full automation
               In this work, we take another strategy, where we separate streams at the file system layer
        2. Essentially, FStream separates streams for filesystem metadata, journal data.
           For database it separates streams of redo/undo logs.
        3. Ext4Streams: journal-stream, inode-stream, dir-stream, misc-stream, fname-stream, extn-stream
        4. evaluations
            1. Fstream achieved 5~35% performance improvements
            2. Fstream achieved WAF of close to one (vs ~1.3 or 2)
        5. As future work, we consider applying FStream to log-structured file systems, like f2fs, and copy-on-write file systems, e.g., btrfs
```

High-Performance Transaction Processing in Journaling File Systems

```
1. High-Performance Transaction Processing in Journaling File Systems    [2018, 5 refs]
   https://www.usenix.org/conference/fast18/presentation/son
    1. interesting. manycore & IO-intensive & SSD scenario, EXT4 lock contention took ~46% of total transaction time.
       found heavy contention at transaction buffer list, checkpoint list.
       solution: lock-free linked-list. improved performance by ~2x,
       but only ~1.1x for data-intensive but not journal-intensive workload (anyway, this paper focus on journal).
       the lock-free linked-list design is good, using GC is clever, solved my years of puzzle
       besides, instead of multi-core shared lock-free data structured, a different approach would be per-core data structure, e.g. ScaleFS
    2. highlights
        1. usecase scenario
            1. 72-core machine, with a high-performance NVMe SSD
               so, that's when shared data structure contention and IO underutilization matters
               the manycore & IO-intensie & SSD scenario
        2. background
            1. journaling filesystem, crash-consistency
            2. performance bottleneck
                1. data structures for transaction processing protected by non-scalable locks
                2. serialized IO operations by a single thread
        3. related works
            1. SpanFS: separated a collection of micro FS called domains, to distribute IOs so that parallelism
            2. Understanding Manycore Scalability of File Systems
               to observe and analyze and benchmark that FS are hidden scalability bottlenecks in many IO-intensive applications
            3. this part, at paper tail, is good
        4. key transaction processing schemes
            1. Use lock-free data structures and operations to reduce lock contention
               Allows multiple threads to access e.g. linked list concurrently
            2. A parallel IO scheme that performs IO operations by multiple threads in a parallel and cooperative manner
                1. i.e. since the journal head list is parallel, we can now parallel the buffer head list too
                   i.e. the IO operations in parallel. that to leverage SSD internal parallelism.
        5. evaluation
            1. improves performance by up to ~2.2x. ~1.5x compared to SpanFS when optimized.
            2. Tokubench, Sysbench, Varmail, Fileserver
            3. Sysbench/Fileserver show less improvement, because it is data-intensive rather than journal IO metadata intensive
        6. thinkings
            1. how the paper benchmarks the lock contension issue
                1. chart of app bandwidth vs core number
                2. lock time on transaction processing (~46% total)
            2. what's the key contention problem the paper targets
                1. transaction buffer list, the multi-thread contention
                2. checkpoint list, the multi-thread contention
            3. how is the concurrent linked list implemented?
                0. this part is good.
                1. basic, the atomic_set: jh->prev=atomic_set(tail,jh)
                2. problem: compareAndSet compares address change, but two allocation happen to use same addresses is not uncommon
                    1. but, if addresses are same, then no issue then, even there were a bunch of operations in middle.
                3. how to handle two inserts at same position in parallel?
                    1. only allow insert to tail. atomic_set(tail, jh)
                       variable "tail" atomically tracks the last tail
                4. how to handle insert and remove conflict in parallel?
                    1. lazy remove, only mark flag, add to GC list
                       a subsequent traversal do GC for logically deleted nodes
                    2. this follows the "Zhang et all" method according to wikipedia
            4. generally
                1. I think this is a typical benchmark -> bottlenect -> optimization work
                   then the small topic is written as a high-level and published paper
                2. so future work, more optimization on contention resources
                   such as file, page cache, etc
    n. related materials
        1. SpanFS: A Scalable File System on Fast Storage Devices    [2015, 24 refs]
           https://www.usenix.org/system/files/conference/atc15/atc15-paper-kang.pdf
            1. in compare with this paper. separated a collection of micro FS called domains, to distribute IOs so that parallelism
               the slides have a summary of parallelism techniques and why they don't apply to EXT4 well.
        2. Understanding Manycore Scalability of File Systems
        3. Lock-free linked-list
            1. wikipedia: https://en.wikipedia.org/wiki/Non-blocking_linked_list
                1. Concurrent insert and delete. Harris, Zhang et all, Valois
            2. Valois [33] Lock-Free Linked Lists Using Compare-and-Swap    [1995, 365 refs]
               Zhang et al. [35] Practical non-blocking unordered lists    [2016, 15 refs]
        4. Silo: Speedy Transactions in Multicore In-Memory Databases
        5. Cerberus: A Case for Scaling Applications to Many-core with OS Clustering
        6. An Analysis of Linux Scalability to Many Cores
        7. RadixVM: Scalable address spaces for multithreaded applications
        8. iJournaling: Fine-Grained Journaling for Improving the Latency of Fsync System Call
```

Understanding Manycore Scalability of File Systems

```
2. Understanding Manycore Scalability of File Systems    [2016, 33 refs]
    1. FxMARK benchmark methods to observe and analyze the morden Fileystems hidden scalability bottlenecks in many IO-intensive applications.
       They key is to stress each individual building block, so we reveal each part of core# scalability. good methodology
       The "Summary of results" in slides, and the bottlenect "Table 3" in paper are very informative.
       The fndings are very good. See details. We never thought of classic FS have so many bottlenecks
    2. highlights
        1. what's the method to study filesystem scalability issue in manycores
            1. FxMARK benchmark suite consisting of 19 microbenchmarks stress each building block of a FS
                1. why stress earch building block?
                   apps usually stuck with a few bottlenecks, cannot see next before resolve previous ones
                    1. path name resolution
                    2. page cache for buffered I/O
                    3. inode management
                    4. disk block management
                    5. file offset to disk block mapping
                    6. directory management
                    7. consistency guarantee mechanism
                2. different sharing levels
                    1. private file (low)
                    2. private data block in shared file (medium)
                    3. same data block in shared file (high)
            2. three application benchmarks representing popular IO-intensive tasks
               (mail server, NoSQK key/value store, and file server)
            3. five popular FS: ext4, XFS, btrfs, F2FS, tmpfs
               on three storage medias: RAMDISK, SSD, HDD
               (each FS selected represented a typical class)
                1. EXT4: popular journaling FS
                2. XFS: support very large file system
                3. Btrfs: copy-on-write COW
                4. F2FS: flash-optimized log-structured LFS
                5. Tmpfs: memory-based
            4. research questions to drill down
                1. What file system operations are not scalable?
                2. Why they are not scalable?
                3. Is it the problem of implementation or design?
        2. what's the scalability issue findings
            1. all operations on a directory are sequential regardless of read or write
            2. a file cannot be concurrently updated even if there is no overlap in each update
            3. the consistency mechanisms are not scalable: like journaling (ext4), copy-on-write (btrfs), and log-structured writing (F2FS)
            4. The "Summary of results" in slides are informative
               And the bottlenect "Table 3" in paper
            5. page cache's reference counting, which uses atomic_inc/dec,
               suffers performance penalty when high core# (up to 80 cores)
                1. reference counting is a commonly know scalability bottleneck in manycore
                2. High locality can cause performance collapse
                   Cache hit should be scalable
            6. Btrfs CoW triggers disk block allocation for every write
               disk block allocation beocmes a bottleneck
                1. similarly, EXT4 -> bottleneck journaling
                   F2FS -> bottleneck checkpointing
                2. Overwriting could be as expensive as appending
                   Consistency guarantee mechanisms should be scalable
            7. Entire file is locked regardless of update range even non-overlap
                1. All tested file systems hold an inode mutex for write operations
                   mutex_lock(&inode->i_mutex)
                2. the issue is Critical for VM and DBMS, which manage large files
            8. many more ... see paper details
                1. fine-grained locks often impede scalability
                    1. e.g. btrfs executes at least 10 atomic insttructions to acquire a singel B-tree node lock
                       under heavy contention, it typically retries a few hundred times to lock a single node
                2. subtile contention matters
                    1. e.g. EXT4 is OK but EXT4nj interleaves a spin lock for journaling and a mutex for directory update.
                       the contending directory mutex in EXT4nj results in expensive side-effects,
                       such as sleeping on a waiting queue after a short period of opportunistic spinning
```

Silo: Speedy Transactions in Multicore In-Memory Databases

```
4. Silo: Speedy Transactions in Multicore In-Memory Databases    [2013, 226 refs]
   http://people.eecs.berkeley.edu/~stephentu/papers/silo.pdf
   https://www.youtube.com/watch?v=5g66rBmUKOw
    1. significant work in manycore scalable in-memory database.
       implement a variant of optimistic concurrency control in which transaction write their updates to shared memory only at commit time
       and uses a discentralized timestamp based technique to validate transactions at commit time
    2. highlights
        1. epoach-based group commit
            1. transaction ordering only exist across epoachs
               global epoach number updates per 40ms by a dedicated thread
            2. problem: client commit delay due to epoach.
            3. compared to another famous altnertive: data partitioning
               silo is based on shared memeory
            4. colocating locks with each record in the TID word
               so don't need centralized lock manager, a shared memory
            5. commit protocol
                1. read-set and write-set are thread-local
                2. commit phase 1: lock each write record in TID
                    if insert, not record to lock, insert a fake record with TID/version
                3. fences ensure epoach is newest, lock is known by others
                4. commit phase 2: use TID change, key version change to detect conflict
                5. commit phase 3: write (record, new-value, commit-TID), unlock
        2. architecture
            1. problem: one-short request, what if read-process-commit transaction?
            2. table implemented by a collection of index trees
               silo index is based on Masstree
            3. transaction needs on-disk logging
            4. GC is needed for deletion of B-tree nodes and records
            5. consistency snapshot based on epoach as consistency point
    n. related materials
        1. Silo: Fast Databases with Fast Durability and Recovery Through Multicore Parallelism    [2014, 65 refs]
           https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-zheng_wenting.pdf
           https://people.eecs.berkeley.edu/~wzheng/osdi_presentation.pdf
            1. follow-up work of Silo, added additional features for logging, checkpointing, recovery, etc.
            2. highlights
                1. exploiting parallelism. fastest checkpointing can introduce undesired spikes
                   using engineering and pacing to reduce the variability
                2. even with frequent checkpointing, a high-throughput DB will have to recover from a very large log
                   parallel design allows replay logs at maximum IO
                3. logging
                    1. use value logging instead of operation logging
                       so recover of key can be in any order (compre), more parallelism
                    2. divides works into subsets and map to exactly one logger
                       to reduce memory remote writes or reads
```

Cerberus: A Case for Scaling Applications to Many-core with OS Clustering

```
5. Cerberus: A Case for Scaling Applications to Many-core with OS Clustering    [2011, 51 refs]
   https://ipads.se.sjtu.edu.cn/_media/publications/cerberus-eurosys11.pdf
    1. work in area of scalable kernels. interesting, very clever, innovative
       Cerberus mitigates contention on many shared data structures within OS kernels
       by clustering multiple commodity operating systems atop a virtual machine monitor
    2. highlights
        1. background: people argue for manycore design new OS from scratch,
           vs continue with traditional path of commodity kernels
            1. this paper takes a middle ground.
               commodity kernels can scale well in small number of kernels
        2. Figure 1. Use VMM to run multiple OSs, each controls a subset of CPU cores
           memory, networking, IO are shared, and managed by VMM
           atop them we provide a POSIX system call virtualization, routing requests to OS
           application runs in top on the POSIX virtualization layer
            1. prototye adds 1800 LOC to Xen VMM, 8800 LOC linux kernel module
            2. the thoughts work similar of partitioning hardware
```

An Analysis of Linux Scalability to Many Cores

```
6. An Analysis of Linux Scalability to Many Cores    [2010, 401 refs]
   https://pdos.csail.mit.edu/papers/linux:osdi10.pdf
    1. analyze the scalability of seven system applications trigger scalability bottlenecks inside linux kernel. MOSBENCH.
       introduced the well-known "sloppy counter".
    2. highlights
        1. method
            1. use in-memory FS to avoid disk bottleneck
               find bottlenecks
               fix bottlenecks and re-run
                1. "Understanding Manycore Scalability of File Systems" is cleverer
                2. stop when a non-trival fix is required, or bottleneck is DRAM
        2. findings
            1. more core#, less throughput. scaling collapse. e.g. Exim.
            2. lookup_mnt: high kernel cpu%, spin_lock may use more cycles than critical section
                1. shared ticket, cross core communication
                   the analysis visualized in slides are good
                2. solution, per-core mount caches
                   observation is mount table is rarely modified
            3. bottleneck: reference counting
                1. cross core communication, slow depending on congestion
                   atomic operation, hardware cacheline lock, delays other core reads
                                     and then needs update all other cores
                2. sloppy coutners: kernel rarely needs true value of ref count
                   central counter, per-core local counter. on a core, threads reuse the local before acquire/put-back from central.
                   memory usage: O(core#) space
                    1. generally, this is per-core data structure
            4. false sharing cache lines
```

RadixVM: Scalable address spaces for multithreaded applications

```
7. RadixVM: Scalable address spaces for multithreaded applications    [2013, 67 refs]
   http://www.cs.otago.ac.nz/cosc440/readings/radixvm-eurosys13-final-draft.pdf
    1. a scalable virtual memory address space for non-overlapping operations.
       it avoids cache line contention using three techniques, which are radix trees, Refcache, and targeted TLB shootdowns
    2. highlights
        1. "RadixVM removes this burden from application developers by ensuring that address space operations on non-overlapping memory regions scale perfectly"
            "Because operating systems serialize mmap and munmap calls .." parallel mmap/munmap matters
            1. it organizes metadata in a radix tree instead of a balanced tree to avoid unnecessary cache line movement
            2. it uses a novel memory-efficient distributed reference counting scheme
            3. it uses a new scheme to target remote TLB shootdowns and to often avoid them altogether
        2. Radix Tree
            1. balanced tree: memory efficient, balanced means unnecessary communication
               radix tree: a large array, but break into regions and indexed by layers
                           2-3x size of balanced region tree
        3. TLB shootdown
            1. when a thread removes region from its address space,
               OS sends shootdown interrupts to each core,
               so that the core flush the region from its TLB
            2. RadixVM implement precise TLB tracking per-core page table
               so that TLB shootdown only needs to send to necessary cores
        4. Refcache - distributed reference counting for manycore
            1. Refcache applies where the true value only needs to be known when it reaches zero
               it delays and batches zero detection to reduce cache contention
            2. structure: global count and per-core local deltas
                          sum them all is the true count
                1. per-core delta is periodically flushed to global count
                2. if global count drops to zero, it will remain zero
                   because no object would further use it
                    1. so if global count remains zero for a entire epoch
                       thus we can detect zero (so, not immediately)
                    2. not that per-core flush is not synced
                3. dirty zero problem: global count can be falsefully zero,
                   thus a wasted examine of whether to free object is scheduled in next epoach
        5. evaluation: the benchmark is very good, almost linearly scalable to core numbers
```

iJournaling: Fine-Grained Journaling for Improving the Latency of Fsync System Call

```
8. iJournaling: Fine-Grained Journaling for Improving the Latency of Fsync System Call   [2017, 6 refs]
   https://www.usenix.org/conference/atc17/technical-sessions/presentation/park
    1. iJournaling improves performance of fsync() call. It journals only the corresponding file-level transactions
       to the ijournal aread for an fsync call while exploiting the advantage of the compound transaction scheme.
    2. highlights
        1. compound journaling, i.e. a journal has both data and metadata
        2. ijournaling: normal periodic journaling operations for compound journaling
                        plus, on-demand journaling (fsync call) if invoked for only file-level metadata
        3. interesting: the idea that we can separate the "streams" in journaling
                          where "streams" are irrelvant application or data flows
                        into different journaling flows, is good.
                        anyway we don't need to mix all things into one journaling fsync,
                          because they don't need transaction semantics across each other
```

Eon Mode: Bringing the Vertica Columnar Database to the Cloud

```
1. Eon Mode: Bringing the Vertica Columnar Database to the Cloud    [2018, 0 refs]
   https://www.vertica.com/wp-content/uploads/2018/05/Vertica_EON_SIGMOD_Paper.pdf
    1. commercial Vertica DB move to cloud shared storage backend, data hash sharding
       originally it runs on directly attached disks.
    2. highlights
        1. column projection is the only physical data structure. it is totally sorted
           data is hash sharded, called segmented, and placed on nodes
        2. column-oriented and sorted gains IO performance due to better compression
        3. problem: if it's hash sharding, how to deal with range query that needs contiguous rows?
                    e.g. 2 <= sales_id <= 5
            1. idea: actually, since we also need replicas,
               in each replica, we can organize it differently, hash, range, etc
               to individually optimize for certain workload
        4. nodes shares one shared storage, not like VHDs.
           nodes each have local cache
        5. transaction. "When a transaction commits, any storage metadata associated with
           a shard must have been sent to every subscriber of the shard"
            1. i.e. the subscriber holding metadata is like a lock mechanism
        6. Crunch Scaling. There are two scalaing, data and computation.
           Crunch scalaing scales the copmputation instead of bound to data
        7. "By leveraging the UDFS API, Eon mode can support additional
            shared storage products such as Azure Blob storage [5], Google
            cloud storage [8], HDFS [14], Ceph [19], and so on"
```

Barrier-Enabled IO Stack for Flash Storage

```
2. Barrier-Enabled IO Stack for Flash Storage    [2018, 4 refs]
   https://www.usenix.org/conference/fast18/presentation/won
    1. interesting paper. evaluation results showed ~30% improvement or less in other cases.
       needs overhaul from flash device to filesystem to Linux IO stack layers.
       allows ordered / orderless IO requests, and barrier requests
    2. highlights
        1. background
            1. storage system use fsync, i.e. transfer-and-flush, to preserve ordering
               this paper overhaul from Flash side to support preserve ordering
               besides, layers in Linux IO stack are also overhauled to preserve ordering
                1. For Flash, the second pain point is Transfer-and-Flush conflicts with Flash internal parallelism
                2. problem: storage system use fsync, also to make sure data is on-disk
                            if this semantics is not addressed, we still have to fsync and wait
                    1. see slides page 42, durability still needed fsync() (but less calls)
            2. related works
                1. this part is informative. e.g. transactional checksum [56, 32, 64]
                   they all tried to solve the extra ordering cost
        2. how is the paper issue studied?
            1. mix ordered vs orderless writes, with fdatasync(), meansure performance on EXT4 w.r.t different flash storage media speeds
               Figure 1 plots the throughput ratio % of ordered vs orderless
            2. Issue Order, Dispatch Order, Transfer Order, Persist Order
        3. architecture: from flash hardware to linux IO stack layers to filesystem
            1. cache barrier-aware storage device
            2. order-preserving block device layer
                1. Order Preserving Dispatch
                2. Epoch Based IO scheduling
            3. barrier enabled filesystem
                1. new fbarrier(), fdatabarrier()
                   they don't have durability semantics compared to fsync(), fdatasync()
        4. evaluation
            1. SQLite performance increases by 270% and 75%, in server and in smartphone, respectively.
                1. the 270% is BarrierFS ordering guarantee vs EXT4 durability guarantee, not fair
                2. for 75%, I only see (BFS-DR - EXT4-DR)/EXT4-DR as ~30% improvement
                3. actually in other cases, the improvement is even smaller
            2. In a server storage, BarrierFS brings as much as by 43X and by 73X performance gain in MySQL and SQLite, respectively,
               against EXT4 via relaxing the durability of a transaction
                1. In Figure 14, the BFS-DR vs EXT4-DR showed ~60% in a case
                   but ~12% in other or even zero in MySQL's
```

Akkio: Sharding the Shards: Managing Datastore Locality at Scale with Akkio

```
3. Akkio: Sharding the Shards: Managing Datastore Locality at Scale with Akkio (Facekbook)   [2018, 2 refs]
   https://www.usenix.org/conference/osdi18/presentation/annamalai
    1. cross-datacenter geo-distributed u-shareds migration, DC access locality management
    2. highlights
        1. Akkio went into production at Facebook in 2014, and it currently manages ∼100PB of data
           Akkio reduces access latencies by up to 50%, cross-datacenter traffic by up to 50%
        2. compared alternatives
            1. distributed cache: cost extra cache memory, missed cache hit rate
            2. geo-replicated data: extra copy cost, many facebook data has low R vs W ratio
        3. u-shard
            1. shard by access locality, rather than using key range or key hashing
            2. other factors related to shard size are
                1. the amount of metadata needed to manage the shards with
                2. effectiveness in load balancing and failure recovery
        4. u-shared placement algorithm
            1. choose datacenter with highest score
                1. score 1: sum up u-share accessed from that datacenter in last X days
                2. score 2: resource usage, available resource in datacenter
```

UKSM: Swift Memory Deduplication via Hierarchical and Adaptive Memory Region Distilling

```
4. UKSM: Swift Memory Deduplication via Hierarchical and Adaptive Memory Region Distilling    [2018, 4 refs]
   https://www.usenix.org/conference/fast18/presentation/xia
    1. UKSM vs CBPS (Content Based Page Sharing) dedup memory for e.g. VM, container, public cloud.
       categorize memory region by page types, layers of levels and priority of scanning,
       plus adaptive in partial page hashing
    2. highlights
        1. Responsiveness of dedup process to newly generated pages. which CBPS lacks
        2. memory region types (by dominating page types)
            not favorable to dedup
                sparse pages
                COW-broken pages
                short-lived pages
            favorable to dedup
                statically-duplicated pages
            observations
                pages within the same memory region present similar duplication patterns
        3. how to detech memory region types?
            1. by sampling a portion of pages, monitoring its degree of dynamics and lifetime
            2. responsiveness: each time application mmap a new memory region,
               it is inserted into list of bottom-level
               hierarchy: bottom bubble from down to up levels
                          higher levels have higher scanning speed
        4. partial page hashing - XDE [18]
            1. hash a fixed number of bytes for each page
            2. adaptive: increase hashed byte number from increasing rounds
                probling, like TCP slow start: increase by delta, and compare gain vs cost
```

Pocket: Elastic Ephemeral Storage for Serverless Analytics

```
5. Pocket: Elastic Ephemeral Storage for Serverless Analytics    [2018, 2 refs]
   https://www.usenix.org/conference/osdi18/presentation/klimovic
    1. For serverless apps to share intermediate data, compared ElastiCache Redis,
       reduce cost by almost 60% while not bottleneck apps with IO. Tested on AWS
        1. For cost test, Pocket uses NVME, redis cache is probably in-memory?
           execution time are basically the same
        2. is the usecase related to Redis changing it's license?
    2. highlights
        1. automatic resource scaling (CPU cores, network bandwidth, storage capacity)
            1. Figure 2 execution time vs resource cost
            2. job gives impact hint.
                latency DRAM, spill over to other storage tiers
                number of concurrent lambdas
                data capacity
                peak aggregate bandwidth
               deduce impact on throughput, capacity, and storage media
        2. intelligent data placement across multiple storage tiers such as DRAM, Flash, and disk
```

Endurable Transient Inconsistency in Byte-Addressable Persistent B+-Tree

```
1. Endurable Transient Inconsistency in Byte-Addressable Persistent B+-Tree    [2018, 5 refs]
   https://www.usenix.org/conference/fast18/presentation/hwang
    1. good paper. For persisteny memory crash consistency of B+-tree, this paper invented
        Failure-Atomic ShifT (FAST) algorithm to shift array slots for B+-tree insert in tree node
          leveraging invariant: B+-tree nodes don't allow duplicate pointers.
          it doesn't need copy-on-write, logging, or tree construction techniques / overheads.
          and read can be non-blocking
        Failure-Atomic In-place Rebalancing (FAIR)
          For tree node split and merge, and modifying from child to parent
          Support of Lock-free search, read doesn't need lock to sync with write
       FAST+FAIR speeds up to 15X~20X compared with Skiplist
    2. highlights
        1. background
            1. the granularity mismatch issue
                1. With the emergence of byte-addressable persistent memory (PM), a cache line, instead of a page, is expected to be the unit of data transfer between volatile and nonvolatile devices
                2. the failure-atomicity of write operations is guaranteed in the granularity of 8 bytes rather than cache lines
            2. to cope with the crash inconsistency in persistence memeory,
                1. the previous works need to maintain consistent backup copy or expensive logging,
                   and memory fencing and cache flush,
                2. this paper work propose a different approach, to tolerating transient inconsistency
                   and made read operations non-blocking
            3. TSO - total store ordering. x86 prevents stores-after-stores from being reordered
               8-byte pointer can be atomically updated
        2. Failure-Atomic ShifT (FAST) algorithm
            1. it's easier to see from slides
            2. the key challenge in B+-tree node is to insert a new key with sort
               the key operation that needs to be failure-transient is to shift arrary slots
                1. the paper invented the Failure-Atomic ShifT (FAST) algorithm
                2. use the duplicated pointer as a marker of invalidate data, shift value slot by slot
                3. if crash in any step, the read operations can identify the duplicated opinter,
                   so as to know invalidate data, and to read correctly
                4. x86 TSO make it doesn't need mfence() to everytime change memory value
                5. FAST requires dirty cache lines must be flushed in order
                   cache line flush need mfence() to avoid reordered with store instruction
        3. Failure-Atomic In-place Rebalancing (FAIR)
            1. Split a node.
                1. A read transaction can detect transient inconsistency in new tree node
                   by checking keys are out of order
                2. while updating partent tree node slots,
                    reader can tolerate the transient inconsistency
                    also, reading can still access the transient inconsistent child tree node by sibling pointer
                3. so, there is no need of lock, for the reader to sync with tree writer
                   the reader needs to check the counter not change, otherwise need to start again
```

Designing a True Direct-Access File System with DevFS

```
2. Designing a True Direct-Access File System with DevFS    [2018, 4 refs]
   https://www.usenix.org/system/files/conference/fast18/fast18-kannan.pdf
    1. FS built in flash device, bypass OS overheads, reverse-caching at host to save device memory
    2. highlights
        1. design principles
            1. For crash consistency, DevFS exploits the power-loss-protection capacitors, instead of logging/journaling or log-structured FS.
            2. To reduce memory usage, in DevFS, only in-memory data structures (inodes, dentries, per-file structures) of active files are kept in device memory, spilling inactive data structures to host memory
            3. DevFS maps each fundamental data unit (i.e., a file) to an independent hardware resource. Each file has its own I/O queue and in-memory journal which enables concurrent I/O across different files
        2. How to implement DevFS in flash device, firmware? ASIC? FPGA? hardware code?
            Due to the current lack of programmable storage hardware,
            we implement DevFS as a driver in the
            Linux 4 kernel and reserve DRAM at boot time to emulate DevFS storage
```

The FuzzyLog: A Partially Ordered Shared Log

```
3. The FuzzyLog: A Partially Ordered Shared Log    [2018, 0 refs]
   https://www.usenix.org/conference/osdi18/presentation/lockerman
    1. Compared to CORFU, give up total ordering with an off-path sequencer.
       Partial ordering allows concurrency across shards, and with weeker consistency cross-region
    2. highlights
        1. shared log abstraction, facilities the simplified design of database, metadata and coordination services, key-value and object stores
            1. AWS Aurora Multi-master database is essentially a shared log abstraction
               this is a interesting approach of database design
               compared to TiDB's self managed per-node TiKV local store
                1. currently, we know distributed DB approaches
                    1. shared storage architecture: PolarDB, Oracle, etc many tranditional
                    2. table partitioned master-slave: mysql master-slave and partitioned table to a homebrew distributed database
                    3. shared log architecture: AWS Aurora Multi-master
                    4. shared nothing architecture: TiDB, Spanner
                    5. Built atop distributed FS: HBase, Percolator, Azure Storage Partition Layer, BigTable
        2. problem: actaully, a cheaper alternative would be like Windows Azure Stoarge,
                    use multiple "streams", in stream ordered, stream vs stream unrelated
        3. CORFU sequencer's scalability issues
            1. network diameter, e.g. cross geo region network delay
            2. network bandwidth. if many small log appends requiring high volume of seqs
            3. large cluster. if hundreds of servers all need high ops/sec
        4. FuzzyLog's partial ordering
            1. First, applications partition their state across logical data shards,
               such that updates against different shards are processed concurrently.
            2. Second, when deployed across geographical regions, applications weaken consistency
               to avoid synchronous cross-region coordination on the critical path of requests;
               as a result, updates across regions – even to the same logical data partition
               - can occur concurrently
```

__Deep Learning Related__


TVM: An Automated End-to-End Optimizing Compiler for Deep Learning

```
6. TVM: An Automated End-to-End Optimizing Compiler for Deep Learning    [2018, 16 refs]
   https://www.usenix.org/conference/osdi18/presentation/chen
    1. very good paper. end2end compiler to generate optimized code for each hardware-specific, from major DL framework graph languages.
       opensourced https://tvm.ai and production in several major companies
       interesting part to use ML-based cost-model (gradient tree boosting model) to optimize code generation
    2. highlights
        1. Current DL frameworks: TensorFlow, MXNet, Caffe, PyTorch, Keras, CNTK
           Graph-level optimizations, target-specific optimizations
           vendor-specific operator libraries
        2. Gap: high-level specification => TVM compiler =>
                low-level optimized code for a diverse set of hardware back-ends
        3. TVM
            1. tensor expression language
                1. middle language that can be generated from major DL frameworks
            2. hardware-specific optimized code generation by ML-based cost model
                1. we must support enough schedule primitives to cover
                   a diverse set of optimizations on different hardware back-ends
                2. nested parallelism, memory scopes;
                   Tensorization, tensorize
                   Explicit Memory Latency Hiding
                3. Automating Optimization
                    1. a schedule explorer that proposes promising new configurations,
                       and a ML cost model predicts performance of a given configuration
                       (billions of possible configurations)
                    2. schedule template specification
                       generic master template for each hardware backend
                    3. the ML-model is trained using runtime measurement data collected during exploration,
                       updated periodically while schedule exploring
                       we need not predict the absolute execution times directly. Instead, we use a rank objective
                        1. a gradient tree boosting model (based on XGBoost [8])
                            1. features extracted from the loop program: 
                                memory access count
                                reuse ratio of each memory buffer
                                one-hot encoding of loop annotations
                        2. a neural network model that uses TreeRNN
                            1. need not feature engineering
                            2. predict slower and took more time to train
                    4. Schedule Explorartion
                        1. In each iteration, the explorer uses the ML model’s predictions to select a batch of candidates on which to run the measurements.
                           The collected data is then used as training data to update the model.
                           If no initial training data exists, the explorer picks random candidates to measure
                        2. we run a parallel simulated annealing algorithm [22]
            3. graph rewriter for high- and operator-level optimizations
                1. Operator fusion combines multiple operators into a single kernel
                2. Data layout optimization converts graph to use better internal data layouts
```

Ray: A Distributed Framework for Emerging AI Applications

```
7. Ray: A Distributed Framework for Emerging AI Applications    [2017, 26 refs]
   https://www.usenix.org/conference/osdi18/presentation/moritz
   https://www.youtube.com/watch?v=CCL0ZkLl9ns
    1. No general-purpose system today can efficiently support the tight loop of training, serving, and simulation. Ray for it.
       Openource released 2017, the community is actively quickly growing
    2. highlights
        1. Ray - a general-purpose framework to enables simulation, training, and serving for RL applications
        2. Ray implements the actor and the task abstractions on top of a single dynamic xecution engine that is highly scalable and fault tolerant
        3. Ray provides lineage-based fault tolerance for tasks and actors, and replication-based fault tolerance for the metadata store
        4. others
            1. Parameter Server by actor
            2. Ray employs a dynamic task graph computation model [21]
            3. A scalable architecutre for high-throughput fine-grained tasks
            4. Driver, Worker, Actor
               Global Control Store (GCS)
                1. GCS enables every component in the system to be stateless
               A global scheduler and per-node local schedulers
                1. the tasks created at a node are submitted first to the node’s local scheduler.
                   A local scheduler schedules tasks locally unless the node is overloaded
               In-Memory Distributed Object Store
                1. On each node, we implement the object store via shared memory
                2. If a task’s inputs are not local, the inputs are replicated to the local object store before execution
                3. Global Storage, Lineage Storage
```

ImageNet Classification with Deep Convolutional Neural Networks

```
1. ImageNet Classification with Deep Convolutional Neural Networks [2012, 31928 refs]
   https://www.nvidia.cn/content/tesla/pdf/machine-learning/imagenet-classification-with-deep-convolutional-nn.pdf
    1. AlexNet paper that first made CNN popular on ImagetNet recognition
       ILSVRC'12, AlexNet reduced top-5 error from 25.8% to 16.4, a leap
    2. highlights
        1. CNN is not new, but GPU training enabled it to be practical.
        2. Besides CNN, below technology is effective and became widely adopted
            1. ReLU Nonlinearity as the neuron activation function
            2. deep, more parameters can be more vulnerable to overfitting
               to fight against overfitting
                1. Data augmentation
                2. Dropout
    n. related materials
        1. Deep Learning回顾#之LeNet、AlexNet、GoogLeNet、VGG、ResNet
           https://zhuanlan.zhihu.com/p/22094600
            1. good article
```

ResNet: Deep Residual Learning for Image Recognition

```
2. ResNet: Deep Residual Learning for Image Recognition    [2016, 15636 refs]
   https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf
    1. deeper CNN expects higher accuracy. but experiemences shows that training is hard.
       Introducing the Residual shortcut connection, train F(x) := H(x) - x,
       however is much easier to train.
       In the end we got 157 layer ResNet ImageNet top-5 error rate to 3.57%
    2. highlights
        1. the chart of traing error & test error on iteration steps,
           is a good tool to study training optimization issue
        2. if the dimension of x and F are not equal,
           we can perform a linear projection Ws.
```

CNN Features off-the-shelf: an Astounding Baseline for Recognition

```
1. CNN Features off-the-shelf: an Astounding Baseline for Recognition    [2014, 2510 refs]
   http://openaccess.thecvf.com/content_cvpr_workshops_2014/W15/papers/Razavian_CNN_Features_Off-the-Shelf_2014_CVPR_paper.pdf
    1. OverFeat. Paper tests over a series of DL tasks. Data augmentation.
       CNN features off-the-shelf. AP well-performs even CNN was not trained for new task.
    2. highlights
        1. in company with data augmentation techniques
            1. e.g. jittering
        2. the crucial thing is CNN features used are trained only using ImageNet,
           while simple classifiers are trained using image specific to task dataset
        3. the many visual classification tests and datasets, are very useful
            1. e.g. Image Classification: Pascal VOC, MIT-67 indoor scenes
        4. Figure 2. Train an SVM using output of each layer level and measure AP by level
        5. CNNaug-SVM data augmentation. Feature Augmentation
```

How transferable are features in deep neural networks

```
2. How transferable are features in deep neural networks    [2014, 2045 refs]
   https://papers.nips.cc/paper/5347-how-transferable-are-features-in-deep-neural-networks.pdf
    1. Experiment design on model transfer on datasets, and good explanation drill down at Figure 2. The base model is plain AlexNet.
       Explains why transfer learning work or not work.
       Transfer learning can even out-performs original model due to combined training set.
    2. highlights
        1. experiment design: separate dataset by A and B.
           AnB, BnB transfer by layer levels.
            1. the author gave explanation to many details
            2. Figure 2 is good, well-explains what happens during transfer by layer level w/wo fine-tuning
                1. Transfer + fine-tuning improves generalization
                2. Fine-tuning recovers co-adapted interactions
                3. Performance drops due to fragile co-adaption
                4. Performance drops due to representation specificity
        2. importance of fine-tuning: AnB+ >> AnB.
           even, AnB+ > BnB+ == B
        3. another experiment by spliting dataset w/wo similarity
            1. first 3-layers are usually transferrable
            2. compared to randomize weights, transfer-learning can be more accurate
    n. related materials
        1. 《小王爱迁移》系列之三：深度神经网络的可迁移性
           https://zhuanlan.zhihu.com/p/27450288
```

FCN: Fully Convolutional Networks for Semantic Segmentation

```
1. FCN: Fully Convolutional Networks for Semantic Segmentation    [2015, 7198 refs]
   https://people.eecs.berkeley.edu/~jonlong/long_shelhamer_fcn.pdf
    1. significant work that improved semantic segmentation score a lot (and inferences faster).
       convers CNN classifier to fully convolutional network output dense predictions.
       skip architecture to combine what and where. upsampling. code on github
    2. highlights
        1. skip architecture
            1. to combine deep coarse semantic information, and shallow fine appearance information.
               i.e. global information resolves what while local information resolves where
        2. "taking all of the final layer receptive fields as a minibatch"
        3. fast scanning [13]
           Shift-and-stitch is filter rarefaction
           Urr ... "we do not use it in our model" ... "We find upsampling ... more effective" ...
        4. Adapting classifiers for dense prediction. convolutionalized
        5. Transfer learning: "We cast ILSVRC classifiers into FCNs ... fine-tuning"
        6. "Experimental framework" lists many optimization and analysis. useful as reference.
            actually, in the paper's model. most yeild no improvement
    n. related materials
        1. FCN学习:Semantic Segmentation
           https://zhuanlan.zhihu.com/p/22976342
```

Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks

```
2. Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks    [2015, 5995 refs]
   https://arxiv.org/pdf/1506.01497.pdf
    1. introduced Region Proposal Networks (RPNs) to propose Region of Interest (RoI), as improved from Fast R-CNN.
       the fully convolutional network (FCN) method out-performs all existing RoI proposal methods
    2. highligths
        1. based on VGG-16 model. 5 FPS inference speed
        2. PASCAL VOC 2007 dataset, MS COCO dataset
        3. Region Proposal Networks (RPNs)
            1. shares the convolutional layers (feature map) with Fast R-CNN
            2. novel "anchor" boxes for images at multiple scales
                1. reg later outputs 4k outputs per point.
                   i.e. each point tells 4 corner coordinates of maximum k boxes
                2. cls layter outputs 2k scores that tells whether a point is in a box
                3. translation-invariant property on image transactions
            3. training method to unify RPNs with Fast R-CNN
                1. "Alternating training". as the convolutional layers are shared,
                   first train by PRN, then train by Fast R-CNN, and iterates
    n. related materials
        1. 【论文笔记】Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks
           https://blog.csdn.net/tmylzq187/article/details/51441553
        2. Fast R-CNN paper    [2015, 4290 refs]
           https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/Girshick_Fast_R-CNN_ICCV_2015_paper.pdf
            1. prior work of Faster R-CNN. The CNN feature map is shared by faster R-CNN
            2. highlights
                1. how is the convolutional layers (feature map) generated?
                    1. it's a pre-trained ImageNet network and then fine-tune
```

Speed/accuracy trade-offs for modern convolutional object detectors

```
3. Speed/accuracy trade-offs for modern convolutional object detectors    [2017, 461 refs]
   https://arxiv.org/pdf/1611.10012.pdf
    1. compares Faster R-CNN, R-FCN, Single Shot Detector (SSD) meta-architectures object detectors. useful.
    2. highligths
        1. "Faster R-CNN w/Inception Resnet, Hi Res, 300 Proposals, Stride 8" shows optimial results.
           See Figure 2. Through it's slower than R-FCN and SSD
        2. Faster R-CNN etc OK to deploy on consumer products, e.g. Google Photos
           and shown fast enough to run on mobile devices
        3. key findings
            1. using fewer proposals for Faster R-CNN can speed it up significantly without a big loss in accuracy, making it competitive with its faster cousins, SSD and RFCN
            2. SSD's performance is less sensitive to the quality of the feature extractor than Faster R-CNN and R-FCN
            3. we identify “sweet spots” on the accuracy/speed trade-off curve
        4. shared feature convolution layers
            1. typical convolution layers to extract feature map:
               VGG, MobileNet, Inception V2, Resnet 101, Inception Resnet V2
    n. related materials
        1. 论文笔记之---Speed and accuracy trade-offs for modern convolutional object detectors
           https://blog.csdn.net/He_is_all/article/details/56485921
        2. YOLOv3目标检测有了TensorFlow实现，可以用自己的数据来训练
           https://zhuanlan.zhihu.com/p/54795847
            1. it was categorized as SSD in above paper
            2. "YOLOv3比R-CNN快1000倍，比Fast R-CNN快100倍"
               YOLO features in speed I think.
            3. YOLOv3 paper: YOLOv3: An Incremental Improvement
               https://pjreddie.com/media/files/papers/YOLOv3.pdf
        3. YOLO（You Only Look Once）算法详解
           https://blog.csdn.net/u014380165/article/details/72616238#comments
```

DenseCap: Fully Convolutional Localization Networks for Dense Captioning

```
4. DenseCap: Fully Convolutional Localization Networks for Dense Captioning    [2015, 391 refs]
   https://cs.stanford.edu/people/karpathy/densecap.pdf
    1. image captioning when one image has multiple regions where each can be captioned.
       i.e. dense captitioning task. key contribution is the dense localization layer, FCLN.
    2. highlights
        1. Figure 2 Model Overvew. Localization Layer
        2. Fully Convolutional Localization Layer
            1. Based Faster R-CNN RPN, but replaced RoI pooling by bilinear interpolation
               so that we allow RoI of different sizes or transactions, instead of just bounding boxes
            2. Box Sampling, NMS algorithms. Select top 300 region proposals
            3. Bilinear Interpolation. RoIs are of different size, we make them same, so that to connect with RNN
               bilinear interpolation, sampling grid G
        3. Recognition Network
            1. fully connected layers. obtain region codes to input to RNN
        4. RNN Launguage Model
            1. LSTM. iterately send x-1 token to next iteration
        5. Preprocessing
            1. Remove "there is", "there seem to be" etc referring phrases
            2. Remove comments that have > 10 words
               Remove images that have < 20 or > 50 comments
            3. merge highly overlapped bounding boxes
    n. related materials
        1. 论文笔记之---DenseCap：Fully Convolutional Localization Networks for Dense Captioning
           https://blog.csdn.net/He_is_all/article/details/54973614
            1. well written
```

Deep Sliding Shapes for Amodal 3D Object Detection in RGB-D Images

```
5. Deep Sliding Shapes for Amodal 3D Object Detection in RGB-D Images    [2015, 194 refs]
   https://arxiv.org/abs/1511.02300
    1. Using deep ConvNet to proposal regions of small and big, and to recognize object types, from RGB + depth image
    2. highlights
        1. input: RGB image + Depth Map. i.e. 4-channel images
        2. Deep Sliding Shapes, Multi-scale 3D RPN
           3D Amodal Region Proposal Network
            1. Joint Object Recognition Network
               Extract both 3D and 2D region proposal
            2. Anchor boxes N = 19
            3. See Figure 1, there are two object size scales of proposal in the network architecture
        3. Encoding 3D Representation, Truncated Signed Distance Function (TSDF)
        4. Autonomous Driving dataset KITTI
    n. related materials
        1. 综述：3D目标检测于RGB-D（Object detection in RGB-D images）
           https://zhuanlan.zhihu.com/p/34887948 
```

Multi-View 3D Object Detection Network for Autonomous Driving

```
6. Multi-View 3D Object Detection Network for Autonomous Driving    [2016, 166 refs]
   http://openaccess.thecvf.com/content_cvpr_2017/papers/Chen_Multi-View_3D_Object_CVPR_2017_paper.pdf
   https://www.youtube.com/watch?v=ChkgSvxAvMg
    1. from Baidu, plan to be used in production. outperforms the state-of-the-art by around 25% and 30% AP. significant work
    2. highlights
        1. car equipment: LIDAR and cameras
            LIDAR / laser scanner depth information
            camera: semantic information
        2. MV3D: fusion of networks from multiple views, classify object proposals, 3D boxes
            1. the paper is somewhat dense
    n. related materials
        1. [论文解读]Multi-View 3D Object Detection Network for Autonomous Driving
           https://blog.csdn.net/williamyi96/article/details/78043014
```

Image style transfer using convolutional neural networks

```
1. Image style transfer using convolutional neural networks    [2016, 707 refs]
   https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf
    1. insight of image style features and content features.
       training method to fuse image style and image content, i.e. style transfer
    2. highligths
        0. pretrained VGG-19 in caffe. with normalization
        1. Figure 1. ConvNets each layer extracts style features or content features
           pass in a style image to obtain style feature, or a content image for content features.
           higher level layers is more about global info, which lower layers has more about detailed pixel information
            1. Content Reconstruction. reconstruct from lower layers is almost perfect
            2. Style Reconstruction. though higher layers matters more about global information.
               if we recontruct style but unifying all layers, then we obtain the style rather than global arrangement
        2. Figure 2. how the model is trainined.
            1. Obtain style feature across each layer on left
            2. Obtain content feature in one layer on right
            3. in middle, define the style loss and content less, weighted add
               use error back-propagation to train white noise image
                1. style feature of white noise image is calculated by Gram matrix,
                   i.e. Gij = SumFikFkj. So that texture info is irrelevant from position
                   See "2.2. Style Representation"
        3. The images presented in this paper were synthesised in a resolution of about 512 × 512 pixels
           and the synthesis procedure could take up to an hour on a Nvidia K40 GPU
    n. related materials
        1. 图像风格迁移-Image Style Transfer Using Convolutional Neural Networks
           https://blog.csdn.net/u014380165/article/details/76286047
```

Perceptual Losses for Real-Time Style Transfer and Super-Resolution

```
2. Perceptual Losses for Real-Time Style Transfer and Super-Resolution    [2016, 1087 refs]
   https://cs.stanford.edu/people/jcjohns/papers/eccv16/JohnsonECCV16.pdf
    1. train another neural network to style transfer faster. also works on super-resolution tasks.
    2. highlights
        1. "Image style transfer using convolutional neural networks"
           is slow since inference requires solving an optimization problem
            1. actually they look similar. though the "Perceptual loss .." paper
               uses a totally different set of concepts to perceive the image style transfer problem
            2. plug the "image transfer network" in front of "Image style transfer .." paper's network
               so that, the error back-propagation on image, now becomes a training on the image transform network
        2. perceptual loss functions, rather than per-pixel loss functions
            1. insights: ConvNets pretrained for image classification have already learned to encode the perceptual and semanticinformation
            2. we therefore use the ConvNet as the loss function
            3. VGG-16 network pretrained on ImageNet.
        3. image transform network is a ResNet
    n. related materials
        1. 感知损失(Perceptual Losses)
           https://blog.csdn.net/stdcoutzyx/article/details/54025243
```

Generative Adversarial Nets

```
1. Generative Adversarial Nets    [2015, 6621 refs]
   https://papers.nips.cc/paper/5423-generative-adversarial-nets.pdf
    1. initial paper of GAN. the foundamental theory is actually simple
    2. highlights
        1. "Instead, we alternate between k steps of optimizing D and one step of optimizing G"
        2. sounds hard to train. like training judge and athlete together
        3. what is the network of D and G using? see "5 Experiements"
    n. related materialis
        1. GAN — Why it is so hard to train Generative Adversarial Networks
           https://medium.com/@jonathan_hui/gan-why-it-is-so-hard-to-train-generative-advisory-networks-819a86b3750b
            1. in-depth
        2. 【深度学习】生成对抗网络Generative Adversarial Nets
           https://blog.csdn.net/shenxiaolu1984/article/details/52215983
        3. Yann LeCunn: What are some recent and potentially upcoming breakthroughs in deep learning?
            https://www.quora.com/What-are-some-recent-and-potentially-upcoming-breakthroughs-in-deep-learning/answer/Yann-LeCun
            1. the Discriminator can be used as a feature extractor for a classifier
            2. the generator can be seen as parameterizing the complicated surface of real data
                1. e.g. doing arithmetic on faces in the Z vector space:
                   [man with glasses] - [man without glasses] + [woman without glasses] = [woman with glasses]
```

Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks

```
2. Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks    [2016, 2736 refs]
   https://arxiv.org/pdf/1511.06434
    1. Architecture guidelines for stable deep convolutional GANs. GAN discriminator for image classification. Impressive vector arithmetic of GAN generator. good paper.
    2. highlights
        1. GAN as alternative to lack of a heuristic cost function
        2. Architecture guidelines for stable Deep Convolutional GANs
            1. Replace any pooling layers with strided convolutions (discriminator) and fractional-strided convolutions (generator).
            2. Use batchnorm in both the generator and the discriminator.
            3. Remove fully connected hidden layers for deeper architectures.
            4. Use ReLU activation in generator for all layers except for the output, which uses Tanh.
            5. Use LeakyReLU activation in the discriminator for all layers
        3. need to prevent Generator model memorize training examples
        4. CLASSIFYING CIFAR-10 USING GANS AS A FEATURE EXTRACTOR
        5. "We demonstrate that an unsupervised DCGAN trained on a large image dataset
           can also learn a hierarchy of features that are interesting"
            1. FORGETTING TO DRAW CERTAIN OBJECTS experiment. interesting
            2. VECTOR ARITHMETIC ON FACE SAMPLES. interesting impressive
                1. "Experiments working on only single samples per concept were unstable,
                   but averaging the Z vector for three examplars showed consistent and stable generations"
        6. "Further work is needed to tackle this from of instability"
    n. related materials
        1. http://cs231n.stanford.edu/slides/2018/cs231n_2018_lecture11.pdf
            1. Same name
                Upsampling
                Deconvolution (bad)
                Upconvolution
                Fractionally strided convolution
                Backward strided convolution
        2. 精读深度学习论文(26) DCGAN
           https://zhuanlan.zhihu.com/p/40126869
           https://github.com/zhangqianhui/AdversarialNetsPapers
        3. 生成对抗网络学习笔记3----论文unsupervised representation learning with deep convolutional generative adversarial
           https://blog.csdn.net/liuxiao214/article/details/73500737
        4. 论文笔记——UNSUPERVISED REPRESENTATION LEARNING WITH DEEP CONVOLUTIONAL GENERATIVE ADVERSARIAL NETWORKS
           https://blog.csdn.net/aidazheng/article/details/72401401
```

Recurrent Models of Visual Attention

```
1. Recurrent Models of Visual Attention    [2014, 900 refs]
 https://papers.nips.cc/paper/5542-recurrent-models-of-visual-attention.pdf
  1. by Google DeepMind. model, reward, training design of the attention network based on RNN.
     Attention patches reduce noise and computation (parameter number is controllable).
     Reinforcement training requires a series of math transforms
  2. highlights
      1. process on attention patches rather than complete image reduces computational cost, reduces noise
          1. the agent never observes entire image, expect the attention patch
      2. each step, the model choose next location to attend base on past information and task demand
      3. Figure 1: network architecture.
          1. Glimpse Sensor: extracts attention patches of multiple resolutions
          2. Glimpse network: taking attention patches and location, through several linear layers
          3. Model architecture: RNN.
              1. core network takes glimpse representation,
                 combining internal representation of previous step,
                 producing the nex internal state representation
              2. location network takes internal state representation to produce the next location
              3. action network takes internal state representation to produce the classification
          4. Reward: a reward signal is given at each step, the goal is to maximize the sum of reward signal
             reward = 1 if object is classified at T step, or 0 otherwise (POMDP)
      4. Training
          1. it's the key gradient approximate formula at CS231n Reinforcement Learning slides page 75. The "REINFORCE rule" in paper
              1. parameters led to high accumulative rewards are increased
          2. Variance Reduction. also same with CS231n Reinforcement Learning page 79.
              1. essentially, it's a weight of reward close or far from when the reward is obtained. and subtract to a common baseline
              2. how to choose the common baseline to be subtracted?
                  1. use the Value Function in Q-Learning
                  2. so that, the loss function is change to favor more when an action gets larger-than-expected reward
      5. Experiment. why are they mainly care hand written digits recognition? these problems recognition are already well accurate
          1. waiting for future extension
  n. related materials
      1. 论文笔记之： Recurrent Models of Visual Attention
         https://www.cnblogs.com/wangxiaocvpr/p/5537454.html
      2. Attention - CosmosShadow
         http://www.cosmosshadow.com/ml/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C/2016/03/08/Attention.html#_label2_3
          1. informative
      3. Show, Attend and Tell: Neural Image Caption Generation with Visual Attention    [2015, 2629 refs]
         https://arxiv.org/abs/1502.03044
          1. impressve results on image caption. LSTM, and models the "hard" and "soft" attention transition
          2. highlights
              1. based on LSTM
              2. "hard" attention: treat attention locations as stochastic by hidden variables
                  1. Monte Carlo based sampling to calculate the gradients.
                     plus moving average to reduce variance
              3. "soft" attention: "The whole model is smooth and differentiable under the deterministic attention, so .. by using standard back-propagation"
                  1. NWGM.
                  2. the loss function deduced
          n. related materials
              1. 论文笔记 - Show, Attend and Tell: Neural Image Caption Generation with Visual Attention
                 https://zhuanlan.zhihu.com/p/35703999

      4. Attention Is All You Need    [2017, 1097 refs]
         https://arxiv.org/pdf/1706.03762.pdf
          1. from Google. attention instead of CNN, RNN. more parallelizable.
          2. highlights
              1. Encoder and decoder stacks
                  1 "residual connection" .. 
              2. Dot-product attention
              3. Self-attention
              4. Multi-head attention
              5. Positional Encoding
              6. RNN needs many iterations thus can hardly be parallelized
          n. related materials
              1. 一文读懂「Attention is All You Need」| 附代码实现
                 https://www.jiqizhixin.com/articles/2018-01-10-20
                  1. "Attention 层的好处是能够一步到位捕捉到全局的联系 .. 相比之下，RNN 需要一步步递推才能捕捉到，而 CNN 则需要通过层叠来扩大感受野"
              2. 《attention is all you need》解读
                 https://zhuanlan.zhihu.com/p/34781297
              3. 论文笔记：Attention is all you need
                 https://www.jianshu.com/p/3f2d4bc126e6
```

DistBelief: Large Scale Distributed Deep Networks

```
1. DistBelief: Large Scale Distributed Deep Networks    [2012, 1727 refs]
   https://static.googleusercontent.com/media/research.google.com/en//archive/large_deep_networks_nips2012.pdf
    1. the paper published at 2012 that's a bit old. AlexNet came out at 2012.
       distributed platform to shard network and parameter server.
       async inconsistency in training is an issue of few study.
       and networking can be saturated to prevent the gain from sharding scale-out
    2. highlights
        1. target problem - distributed training
        2. architecture
            1. sharding the model. Figure 1.
               only nodes with edges cross partitions will need to transmit state across machine
                1. sounds the schema is not always applicable for a typical ConvNets
            2. upward and downward phases, i.e. feedforward and back-propagation 
            3. a typical cause of less-than-ideal speedup is variance in processing times across machines.
               leading many machines waiting for single slowest machine
            4. paramater server. in Downpour SGD or L-BFGS, replicas or coordinators pull and update parameters in Parameter Server. it can be asynchronous
                1. parameter server shards run independently of one another
        2. Downpour SGD
            1. still need to develop distributed version of SGD,
               so that means the common many SGDs used in many papers may have difficulty moved on distributed platform?
            2. per mini-batch, replica asks parameter server for updated parameters,
               then mini-batch, then send update the parameter server
            3. replica updates themselves totally async, so guarantee that they undergo same number of updates or order
                1. little theory ground for the impact of such inconsistency
                2. in practices, relax consistency can be remarkably effective
        3. Sandblaster L-BFGS
            1. actually seldom heard L-BFGS in newer DL papers ..
            2. batch optimization: a single coordinator sends small messages to replicas
               and the parameter server to orchestrate batch optimization
            3. coordinator load balancing. assign each replica a very small portion of work.
               assign new portion whennever they are free
                1. also, schedule multiple copies and use whichever finishes first
                2. prefetching, and assigning same sequential portions to same replica worker
    n. related materials
        1. 总结：Large Scale Distributed Deep Networks
           https://blog.csdn.net/u012648144/article/details/43084403
        2. 数值优化：理解L-BFGS算法
           http://www.hankcs.com/ml/l-bfgs.html
```

VGG: Very Deep Convolutional Networks for Large-Scale Image Recognition

```
1. VGG: Very Deep Convolutional Networks for Large-Scale Image Recognition    [2014, 18657 refs]
   https://arxiv.org/pdf/1409.1556.pdf
    1. VGG-19 layers deeper network yeilds better accuracy.
       the training details are useful. use 3*3 filter.
    2. highlights
        1. use very small 3*3 receptive fields rather than 7*7
        2. learn from the paper's training details
```

GoogleLeNet: Going Deeper with Convolutions

```
2. GoogleLeNet: Going Deeper with Convolutions    [2014, 11112 refs]
   https://www.cs.unc.edu/~wliu/papers/GoogLeNet.pdf
    1. 22-layers. 12x few parameters than AlexNet, no new data used than old ImageNet.
       usage in mobile. innovative Inception network. Auxiliary classifier in middle. no fully-connected layers
       Inception network is still evolving, v2, v3. Batch Normalization. Factorization of filters.
    2. highlights
        1. mobile. concepts of computational budget by multiply-adds at inference time
        2. 1*1 convolutions used as dimensionality reduction
           also see: https://stats.stackexchange.com/questions/194142/what-does-1x1-convolution-mean-in-a-neural-network
        3. Filter concatenation. H*W output sizes of the 1*1, 3*3, 5*5 etc convolutions are actually same.
           So these output layers can be stacked together simply.
           also see: https://blog.csdn.net/qq_28132591/article/details/64124491
        4. dropout. everyone uses it.
        5. no fully-connected layers
        6. key innovations
            1. Inception network, which uses 1*1 convolution to reduce dimensionality.
               So that, the network can easily be wider and deeper without getting into computational difficulties
            2. Auxiliary classifier connected to intermediate layers to propagate back gradient signals,
           On the assumption that features produced by layers in the middle should be very discriminative
               Their losses are added to total loss after weighted by 0.3
               At inference time, the auxiliary networks are discarded
        7. training methodology section is useful
    3. related works
        1. network-in-network approaches as the prior works
        2. sparsely connected architectures, to reduce parameter and computational needs
    n. related materials
        1. Lecture 7 Convolutional Neural Networks CMSC 35246: Deep Learning
           http://ttic.uchicago.edu/~shubhendu/Pages/Files/Lecture7_flat.pdf
```
