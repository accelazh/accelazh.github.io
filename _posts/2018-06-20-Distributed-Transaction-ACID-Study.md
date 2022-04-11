---
layout: post
title: "Distributed Transaction ACID Study"
tagline : "Distributed Transaction ACID Study"
description: "Distributed Transaction ACID Study"
category: "transaction"
tags: [transaction, acid, storage]
---
{% include JB/setup %}

How is distributed transaction implemented with ACID semantics is a wonder. Percolator TLA+ mostly solved the myths. My summarized notes here.

WeiChart articles published to re-summarize

  * [Distributed Transaction in Distributed Systems (P1)](https://mp.weixin.qq.com/s/oNhTUoqE4Jj7GBSaE-hX0g) [PDF](/images/Accela-distributed-transaction-in-distributed-systems-P1.pdf)
  * [Distributed Transaction in Distributed Systems (P2)](https://mp.weixin.qq.com/s/K-VLqNkFH5047bTIJsTRzw) [PDF](/images/Accela-distributed-transaction-in-distributed-systems-P2.pdf)
  * [Distributed Transaction in Distributed Systems (P3)](https://mp.weixin.qq.com/s/FvQO_ZfHbdXKlmRnrt1O7Q) [PDF](/images/Accela-distributed-transaction-in-distributed-systems-P3.pdf)

For TLA+ study how & why, you may read the [TLA+ book](https://lamport.azurewebsites.net/tla/tla.html), or see attached slides for materials. 

![TLA+ My Cheatsheet](/images/tla-plus-my-cheatsheet.png "TLA+ My Cheatsheet")

```
1. How Amazon Web Services Uses Formal Methods    [2015, 123 refs]
    http://www.cslab.pepperdine.edu/warford/math221/How-Amazon-Web-Services-Uses-Formal-Methods.pdf
    1. this paper shows how AWS is using TLA+, it proves that, finally we have a formal language, TLA+
       to be able to use in industry production level.
    2. highlights
      1. Benefits of using TLA+: correctness, help thinking, pass shared knowledge
      2. "What Formal Specifcation Is Not Good For"
        1. prolonged severe slowdowns are considered errors. but TLA+ realtime specs cannot model that well
        2. “How do we know that the executable code correctly implements he verifed design?” The answer is we do not know
      3. How one of the AWS author C.N. finds TLA+ and determines to adopt it
        1. author C.N. (paper author CHRIS NEWCOMBE?) found TLA+ in appendix of a paper of Paxos. This gives confidence
             they learned engineers in DEC/Compaq had been using TLA+ to verify some intricate cache-coherency protocols. read and found TL+ is comprehensive enough
             C.N. evaulated TLA+ by writing a spec and compare with Alloy.
          2. C.N. tried to persuade colleagues at Amazon to adopt TLA+. but engineers usually have no spare time
            1. author T.R. chose TLA+ to verify DynamoDB replication and Fault-tolerance. Verified by TLC and found serious but subtle bugs that could lose data
            2. Persuading More Engineers. Author F.Z., author B.M., and more
    n. related materials
      1. Use of Formal Methods at Amazon Web Services    [2014, 10 refs]
         http://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf
          1. it's basically the same authors and same paper but 1 year before.
      2. Why Amazon Chose TLA+
         https://pdfs.semanticscholar.org/311c/5538d00421623ec73e14ef93ae0fbdae2392.pdf
        1. as mentioned in parent paper, "listing the requirements we think are important for a formal method to be successful in our industry segment"
        2. What we wanted in a formal method
          1. Handle very large, complex or subtle problems
          2. Minimize cognitive burden. And must be easy to remember
          3. High return on investment
```

As reading the [Percolator.tla](https://github.com/pingcap/tla-plus/tree/master/Percolator), here I try to generalize the detailed rules for Snapshot Isolation (SI).

```
Snapshot Isolation:
    
    1. on a key, if read2 happens after read1, then start_ts2 > read_ts1. i.e. for any transaction, start_ts > k's last_read_ts
        1. this ensures if a transaction sees a version of value, it must be started after corresponding timestamp
        2. this is enforced by `readKey(c): key_last_read_ts[k] < start_ts` in Percolator.tla
    2. SI 1: snapshot read: on a key, for any transaction, commit_ts must > k's last_read_ts.
        1. this is to ensure a version of read, which has already been seen in history, won't be changed.
           i.e. snapshot. this is what a snapshot isolation rule.
        2. this is verified by `checkSnapshotIsolation(k, commit_ts): key_last_read_ts[k] < commit_ts`
           enforced by, in Percolator.tla, `readKey(c): ~hasStaleLock(k, start_ts)`,
           i.e. the T2 reader will cleanup all locks before read, making T1 unable to commit
            T1_read -> T1_obtain_write_ts -> T2_clean_lock_before_read -> T2_read -> T1_commit_with_old_ts
    3. SI 2: detects write-write conflict: if both T1 and T2 writes to a key, only one of them can success, the other needs aborts
        1. this prevents the so-called Lost Update anomalies. it is one of snapshot isolation rule
        2. enforced by, `Prewrite(c): lock(c)`. i.e. before write to a key, must hold the lock, in Percolator.tla
    
Serializable:

    4. read-write conflict: T2 writes to what T1 reads, and T1_read -> T2_commit -> T1_commit must be prevented
        1. this is actually NOT a snapshot isolation rule. it is the famous Write Skew anomaly of snapshot isolation
            1. paper: "Serializable Isolation for Snapshot Databases" gives the anti-example of SI in intro
               https://drive.google.com/file/d/0B9GCVTp_FHJIcEVyZVdDWEpYYXVVbFVDWElrYUV0NHFhU2Fv/edit
        2. enforeced by, in Percolator.tla, `Prewrite(c): lock(c): canLockKey(k, ts): writes = {}`, i.e. new any newer writes.
            1. this should have made it Serializable Snapshot Isolation, i.e. it's serializable
               I.e. with both WW and RW (write-skew) conflicts detected, it's serializable
        3. this rule only, no need for rule 3, is sufficient for serializable
            1. as backed in paper "A Critique of Snapshot Isolation".
            2. and, even this rule only, will unecessarily abort some transactions that are serializable
               i.e. sufficient but not necessary for serializable

(Note that Percolator.tla actually enforeced 1-4, which is sufficient for serializable.
    It may remove some lock steps to work as SI only.
    Rule 5 is not in scope of Percolator.tla)

Serializable Snapshot Isolation:

    5. SSI: detect adjacent 2 rw-conflict in serialization graph, and abort
        1. this rule only, is sufficient for serializable.
        2. as backed in paper "Serializable Snapshot Isolation in PostgreSQL"
           which refers to "Serializable Isolation for Snapshot Databases"
        3. compared to rule 4 read-write conflict abort, or strict 2-phase locking, or snapshot isolation + rw-conflict abort
           SSI aborts less false positives, i.e. transactions that are allowed by serializable, but aborted or lock delayed
        4. also SSI can be built on SI implementation, and provides the way to implement serializable with feasible performance

--

For how to understand serialization graph,
    See notes in paper "Serializable Snapshot Isolation in PostgreSQL"
```

My [Attached slides](/images/distributed_transaction_explained_through_tla_plus.pdf). And the [Amazon serializable snapshot isolation TLA+](/images/amazon-snapshot-spec-master.zip) shared from [google group](https://groups.google.com/forum/#!topic/tlaplus/UwYW6XqyDvE).

Studying Percolator vs TiDB vs CockroachDB

```
1. 学习 TLA+ - Percolator Transaction
   https://www.jianshu.com/p/721df5b4454b
    1. Spanner-cap-truetime-transaction.md
       https://github.com/pingcap/blog-cn/blob/master/Spanner-cap-truetime-transaction.md
        1. the transaction part comes mainly from "Life of Cloud Spanner Reads & Writes"
        n. related materials
        1. 分布式系统的时间
             https://www.jianshu.com/p/8500882ab38c
        2. Life of Cloud Spanner Reads & Writes
           https://cloud.google.com/spanner/docs/whitepapers/life-of-reads-and-writes
    2. tidb-transaction-model.md
       https://github.com/pingcap/blog-cn/blob/master/tidb-transaction-model.md
        1. useful to read to understand how TiDB distributed transaction works
    3. tidb transaction-isolation.md
       https://github.com/pingcap/docs-cn/blob/master/sql/transaction-isolation.md
      1. TiKV 的 MVCC（Multi-Version Concurrency Control）机制
         https://pingcap.com/blog-cn/mvcc-in-tikv/
          1. "段提交（2-Phase Commit，2PC）是在 MVCC 中实现的"
            1. MVCC doesn't exclude this use of locks.
            2. MVCC usually works with snapshot isolation, so that read lock is not necessary
               but write locks are still needed, for snapshot isolation write-write conflict
            3. "MVCC is an extension of optimistic concurrency (or a version of it)"
               https://stackoverflow.com/questions/5751271/optimistic-vs-multi-version-concurrency-control-differences
                1. but, people usually say 2PC is pessimistic concurrency control/locking.
                   but actually TiDB/Percolator are showing that 2PC can be used with MVCC, in a Optimistic Concurrency Control/Locking way
                    1. in 2PC, TiDB/Percolator allows transaction to proceed read without locking, but write needs lock, and they may fail in between
                       read -> lock -> (cannot lock, abort) -> write
      2. Percolator 和 TiDB 事务算法
         https://pingcap.com/blog-cn/percolator-and-txn/

2. cockroachdb vs percolator
   https://github.com/cockroachdb/cockroach/blob/master/docs/design.md
   hackernews: How CockroachDB Does Distributed, Atomic Transactions
   https://news.ycombinator.com/item?id=10160797
    1. Lock-Free Distributed Transactions
       https://github.com/cockroachdb/cockroach/blob/master/docs/design.md#lock-free-distributed-transactions
       https://www.cockroachlabs.com/blog/how-cockroachdb-distributes-atomic-transactions/#comment-2232720938
        1. even Percolator & Spanner needs lock, in the prewrite phase
        2. I think the "switch" is acting as a lock. switch to new (staged) data or original data
           or say, the staged data is acting as the lock. anyway that's a record in database
          1. so, here we understand why in Percolator.tla, lockKey(k, start_ts, primary) also updates key_date[k]
        3. questions
          1. the article "How CockroachDB Does Distributed, Atomic Transactions" is they key to understand cockroachdb transaction
             but, it assumes there is only one transaction. and it promises to have later blog post to explain concurrent transaction case
             the original article was published at 2015. however, there is no follow up blogs ever. so ..
        n. related materials
          1. Serializable Isolation for Snapshot Databases  [2008, 201 refs]
             https://drive.google.com/file/d/0B9GCVTp_FHJIcEVyZVdDWEpYYXVVbFVDWElrYUV0NHFhU2Fv/edit
              1. this paper, given in cockroachdb doc, explains the problems in snapshot isolation (SI)
                 and proposed the serializable snapshot isolation (SSI).
                 SSI is serializable, and not like serializable by snapshot isolation + abort RW conflicts; SSI avoids some false positives
              2. For serializable snapshot isolation (SSI)
                1. the theory is to detect the "generalized dangerous structure" in multi-version serialization graph testing (MVSG).
                  1. I.e. a consecutive pair of RW-dependency, TN->T0->T1
                2. Use T.inConflict and T.outConflict to mark the RW dependencies.
                   in implementation, it's by using SIREAD locks along with WRITE locks
                3. there are some false positive detections to abort transactions. see details in paper
                4. the proposed SSI is serializable. see "Correctness"
              n. related materials
                1. A Critique of ANSI SQL Isolation Levels  [1995, 1056 refs]
                   https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf
                    1. this is the fundamental paper. as said to have formalized SI. the paper is done mainly by Microsoft.
                       the paper analyzed in detail the different anomalies in ANSI SQL isolation levels,
                       using the mostly formal transaction dependency graph, the transaction history representation, etc
                       most importantly, it proposed "Snapshot Isolation", which is being used till today
                2. Serializable Snapshot Isolation in PostgreSQL  [2012, 84 refs]
                   https://drkp.net/papers/ssi-vldb12.pdf
                    1. so, the SSI proposed in parent paper, has been adopted widely.
                       very good paper. SSI is aborts less false positives than SI + rw conflict, as to achieve serializable.
                       and, SSI finally made it possible to use a fast way to implement serializable, rather than tranditionally the strict two-phase locking (S2PL)
                       this paper illustrate how it comes, and how PostgreSQL implements it.
                       the SSI is referred to paper "Serializable Isolation for Snapshot Databases"
                    2. highlights
                      1. the theory of SSI
                        1. Serializable and Serializable Graphs
                          1. Serializable Graphs
                            1. See Example 2, this paper serves how to understand and use the Serializable Graphs. And see 3.1
                            2. If T2 *appears* to be executed after T1, e.g. T1 reads old value before T2 updates, then there is an arrow arc from T1 to T2
                              1. the arrow arc reflects *appear* before/after relationship
                              2. the arrow arc, i.e. transaction dependency, has different types
                                1. wr-dependency: T1 writes, and then T2 reads the updated value
                                2. ww-denpendency: this is what SI aborts, both T1 and T2 writes to same object
                                3. rw-anitdependency: T1 reads, T2 updates value and commits, T1 writes. this is the rw-conflict, or write-skew
                              3. Serializable <=> there is no cycle in the Serialization Graph
                                1. I.e. it appears that, each transaction exeutes before/after other transactions one-by-one
                                2. if there is cycles, there is no appear-to-be state of all transactions executes one-by-one
                              4. The Serializable Graph acts as the way for us to understand how an Isolation Level performs compared to Serializable
                                1. Snapshot Isolation, allows the Write-Skew abnormaly, compared to Serializable
                                2. Snapshot Isolation + Prevent RW-conflict, is Serializable, but it aborts some graphs that Serializable allows
                                  1. I.e. Snapshot Isolation + Prevent RW-conflict, aborts some false positives
                                3. Serializable Snapshot Isolation, is Serializable, and it aborts less false positives than Snapshot Isolation
                                  1. that's the fundamental "better" of why PostgreSQL is adopting SSI
                                  2. and, SSI can be but atop snapshot isolation which PostgreSQL already has
                                  3, and, most importantly, SSI provides a fast, or say feasible way, to implement serializatble,
                                     compared to traditional S2PL (strict two-phase locking) which is slow
                              5. As you can see how we understand different isolation levels
                                1. Serializable allows some serialization graph structures.
                                   SI, SI + avoid rw-conflict, SSI, each have their allowed serialization graph structures
                                   They may not fully overlap with Serializable's. They may be smaller, or excessively bigger, or else
                                   This is the way we discuss how these isolation levels be sufficient/necessary to Serializable
                          2. Serializable Snapshot Isolation
                            1. Theorem 1: Every cycle in the serialization history graph contains a sequence of edges T1 rw−→ T2 rw−→ T3 where each edge is a rw-antidependency.
                                          Furthermore, T3 must be the first transaction in the cycle to commit.
                            2. So, what SSI does to achive Serializable, is to detect any 2 adjacent RW-conflicts, and abort
                              1. Single RW-conflict won't make it not Serializable,
                                 but neither S2PL nor OCC (optimistic concurrency control) would permit this execution.
                                 While SSI allows it.
                      2. how PostgreSQL implements SSI
                        1. For longterm read-only transaction, use "safe snapshot", to avoid it or let other transactions keep holding SIREAD locks
                          1. Safe snapshot: see 4.2, I'm a read-only Tx, and no other concurrent read/write Txs with rw-conflict out to a Tx that comitted before my snapshot
                          2. That longterm read-only transaction, is delayed so it can use safe snapshot. That's called Deferrable Transactions
                        2. SSI generally uses more memory to track Transaction dependencies and locks.
                           See section 6 for how PostgreSQL mitigate memory uses. E.g. memory usage must be bounded, and there is graceful degrade.
                    n. related materilas
                      1. Why Amazon Chose TLA+
                           https://groups.google.com/forum/#!topic/tlaplus/UwYW6XqyDvE
                            1. Here people shared AWS's TLA+ spec for Serializable Snapshot Isolation. and other materials
                               https://groups.google.com/d/msg/tlaplus/UwYW6XqyDvE/t6xwd5jGPYwJ
                        2. CockroachDB may be using SSI
                           https://github.com/cockroachdb/cockroach/blob/master/docs/design.md#lock-free-distributed-transactions
                            1. since in the design doc they are highly recommended as inspiration
                3. wiki: Snapshot isolation
                   https://en.wikipedia.org/wiki/Snapshot_isolation
                    1. explains good for snapshot isolation, write skew, example, and ways of walkarounds,
                       and what does Oracle "SELECT FOR UPDATE" means
                        - upgrade reads to writes, so write skew now becomes write-write conflict and gets serialized

          2. A Critique of Snapshot Isolation  [2012, 36 refs]
             https://drive.google.com/file/d/0B9GCVTp_FHJIMjJ2U2t6aGpHLTFUVHFnMTRUbnBwc2pLa1RN/edit
             https://www.slideshare.net/MaysamYabandeh/wsi-eurosys
              1. this paper, given in cockroachdb doc, explains snapshot isolation good
                 the most good part is, it proves read-write conflict avoidance (write-snapshot isolation) is sufficient for serialization
                                        both read-write conflict avoidance and write-write conflict avoidance (read-snapshot isolation, i.e. normal snapshot isolation)
                                            may unecessarily abort some serializable transactions
              2. highlights
                1. snapshot isolation
                  1. it checks only write-write conflicts, which its lock-based implementation [24] is very straightforward:
                     a transaction locks a data item before modifying it and aborts if it is already locked
                  2. the read-only transactions, which comprise the majority of the transactional traffic, could run without any extra locking
                  3. The drawback is that serializability, which sometimes requires detecting read-write conflicts, is not pro- vided by snapshot isolation.
              2. as said, OMID implements lock-free snapshot isolation with both WW and RW conflict detected.
                 essentially it's using a centrallized scheme: Status Oracle (SO)
                 RW provides serializability
              3. lock-free: it's interesting here. this paper (link above) compared itself with Percolator [24], which need locks
                1. How to detect read-write conflict. See "Algorithm 1"
                  1. The centralized Status Oracle assigns timestamp. It ensures
                       If a Tx checks no newer writes and passed, the assigned commit timestamp to TS by Status Oracle must
                                   ensures, no other Tx' could violate previous passed check by Tx
                            2. I.e. I think what is shown on "Algorithm 1" is a single-thread flow, or locked block
                2. How to detect write-write conflict.
                  1. same in Algorithm 1
              4. the most useful part are actually these discussions and proofs
                1. Is Write-write Conflict Avoidance Sufficient for Serializability?
                  1. No. This is what SI does, but there are Write-Skew anomaly
                2. Is Read-write Conflict Avoidance Sufficient for Serializability?
                  1. Yes. Good. This shows the magic. Write-Write in SI is actually not necessary.
                  2. SI, which enforeces write-write abort, is called read-snapshot in this paper. it aborts some false positives, which are serializable however
                     write-snapshot isoaltion, which is coined in this paper, enfoce only read-write conflict abort. this is enough for serializable
                3. the next question is, Is Read-write Conflict Avoidance Necessary for Serializability?
                  1. "Both snapshot isolation and write-snapshot isolation unnecessarily abort some serializable transactions."
                    1. you see, serializable is actually not asking that much.
                       in "Serializable Snapshot Isolation in PostgreSQL" you will see how to SSI comes in
            n. materials
                1. Wiki: Non-lock concurrency control
                   https://en.wikipedia.org/wiki/Non-lock_concurrency_control
                    1. Wiki:Timestamp-based concurrency control
                       https://en.wikipedia.org/wiki/Timestamp-based_concurrency_control
                        1. there is formal definitations. interesting
                        2. I think it still needs lock to guarantee that a group of contraints hold while it's doing an action
                    2. Wiki: Optimistic concurrency control
                       https://en.wikipedia.org/wiki/Optimistic_concurrency_control
                    3. Wiki: Multiversion concurrency control
                       https://en.wikipedia.org/wiki/Multiversion_concurrency_control
                        1. "The most common isolation level implemented with MVCC is snapshot isolation"
          3. Calvin: Fast Distributed Transactions for Partitioned Database Systems  [2012, 277 refs]
             http://cs.yale.edu/homes/thomson/publications/calvin-sigmod12.pdf
              1. this paper, given in cockroachdb doc, as said a discussion of SSI implemented by preventing read-write conflicts
            2. this paper doesn't have much details about how to arrange transaction reads/writes and the locking procedures.
               it's mostly underlying KV store agnostic
            3. how it works for the distributed transaction
              1. there are multiple sequencer nodes. they somehow give each transaction a unique sequence
                 from one replica to another replica, they use paxos to replicate transaction requests. that's how geo-repilcate works
              2. the next layer is scheduler. each sequencer pass every transaction to every scheduler.
                 thus each scheduler has the global view of all transactions
                  1. this is different from Percolator, which every node works by only seeing its partition
                     since the scheduler needs to know globally everything, it may be bottleneck
                  2. like in paper "A Critique of Snapshot Isolation", the Scheduler global knows everyything,
                     so it can check rw dependencies and arrange the global ordering of how transaction should be executed.
                  3. to actually let those transactions reads/writes execute in order as we previously arranged, we use locks
                     that's the "deterministic locking mechanisms".
                     by implementation it uses a single thread to serialize all lockings.
                     that's like the Status Oracle in "A Critique of Snapshot Isolation" to centrally control, too
              3. Calvin needs transaction to declare full read/write set before hand.
                 "Dependent transactions", as called the name, may issue a probe read, and then know the full read/write set

3. MVCC distributed transaction
   1. python implementation of Distributed MVCC Based Cross-row Transaction
      https://gist.github.com/weidagang/1b001d0e55c4eff15ad34cc469fafb84
       1. originates from Percolator
```

Further, different approaches to implement distributed transaction

```
1. approaches to implement distributed transaction
    1. eventually, spanner & percolator are using 2PC. a variant is 3PC
        1. I think CockroachDB is using a variant of 2PC. They don't have much sensible doc to tell how they handle it.
           though CockroachDB refered to SSI papers, but how to implement it in distributed way (without locks?) is still in question.
    2. relax ACID, internet companies usually use eventual-consistent transactions, and compensating transactions
        1. think about how booking.com executes a distributed transaction to book hotels
            1. we can split the huge transaction into many small, single node ones.
               first, we log user intent into a DB. next, we eventually carry out it piece by piece.
                   the propagation of the "eventual" should have pre-defined fixed known order. that makes the "eventual" controllable.
                   it's eventual, in order, but not "weak" consistency. if well-designed, we can ensure the time threshold of full propagation
               there can be competitors, so these small transactions may fail in the middle
                   maybe because stock is sold out, which is a common case on hot hotel.
               next, we rollback. use "compensation" steps to restore the resources modifed by previous successful small transactions
                   that's the name of "compensation" transaction.
                   then general problem we are trying to solve here applies to all stock & sell management.
               after all that's done, we tell user that his/her booking failed in website.
                   the overall big transaction process should be quick enough, so no much issue for user.
               the overall ACID violation here is, middle result of the big transaction is visible
                   We don't care in practice.     
        2. lone lived transactions
          1. instead of fail the entire very long transaction if a small transaction fails, we can
                 choose an alternative path to forward to small transaction
                 rather than fail entirely, we fail back a part 
        n. materials
            1. Compensating Transactions: When ACID is too much
               https://developer.jboss.org/wiki/CompensatingTransactionsWhenACIDIsTooMuch
               https://developer.jboss.org/docs/DOC-48610
            2. smiliar
              https://zhuanlan.zhihu.com/p/25933039
              https://www.jianshu.com/p/716d3ec567c0
              http://www.cnblogs.com/soundcode/p/7146656.html
              https://github.com/QNJR-GROUP/EasyTransaction
                1. they usually rely on message queues
                  1. they may use or not a transactional message queue interface
    3. Serializable Snapshot Isolation, which implements Serilizable with feasible performance,
       abort less false positives than strict 2-phase locking or RW-conflict abort (write-snapshot isolation),
       and can be built based on Snapshot Isolation
        1. see paper "Serializable Snapshot Isolation in PostgreSQL" notes for detail
    4. The centralized Status Oracle
        1. as in paper "A Critique of Snapshot Isolation"
           and in paper "Calvin: Fast Distributed Transactions for Partitioned Database Systems", where the Scheduler knows every transaction
    5. POSIX filesystem metadata operation transaction
        1. usually filesystem doesn't need full semantics of transaction.
           so the implementation can be trimmed and optimized in specialized way.
           for large operations, strategies like eventual consistency + hide middle results, can be used
           as in paper "HopsFS: Scaling Hierarchical File System Metadata Using NewSQL Databases"
    6. multiple single-know-all DB servers + shared underlying distributed log system
        1. "Hyder - A Transactional Record Manager for Shared Flash" and AWS Aurora Multi-master are taking this approach
        2. single DB server is able to know all states from the log system, so is able to handle full transaction.
           there is actually not need for data partitioning and distributed transaction
           but, the underlying log system is distributed, so able to support scale-out write throughput
        3. to resolve conflicts due to multi-master DB servers, may use an external resolver
```

More paper readings

```
1. Percolator: Large-scale Incremental Processing Using Distributed Transactions and Notifications    [2010, 473 refs]
   https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36726.pdf
  1. good paper. the de-facto howto implement MVCC distributed snapshot isolation transaction for people to learn about
  2. highlights
    1. the purpose of Percolator
      1. to process large batches
      2. may have long-running transaction, such as reporting
      3. provides ACID snapshot isolation transactions
        1. actually, read-write conflict is also prevented
    2. key designs
      1. built on BigTable
        1. for each key row, adds a bal:data, bal:lock, bal:write columns to control the transaction
        2. Get() operation needs to read locks, locks are stored in special in-memory columns in BigTable
      2. rely on the Timestamp Oracle to obtain accurate timestamp
        1. not like Spanner which uses TrueTime
      3. lock cleanup
        1. stale/dead client may leave stale locks.
        2. the second transaction, if found stale locks, will do the cleanup
          1. only one of the second Tx who clean locks, and first Tx who lock and commit, will succeed
          2. to avoid Tx A cleans Tx B's lock when B is not failed
            1. Tx A will not clean lock unless it suspects B is dead or stuck
              1. the liveness is registed tokens in Chubby
              2. also, a lock of too-old wall time will be cleaned
                1. long-running works periodically update the wall time to avoid its lock being cleaned
      4. lock step
        1. when lock is acquired, data is added to bal:data. they are done in one step
        2. the bal:write is added a new record to point to new bal:data, that's the actual commit
      5. all the transaction protocol is in TiDB's Percolator.tla
         https://github.com/pingcap/tla-plus/tree/master/Percolator
        1. details logged elsewhere
        2. think it another way, what Percolator is trying to do is
          1. assign timestamps, use timestamp to arrange how transaction executes
          2. the locking & transaction protocol needs to enforce that the timestamps are respected
            1. if commit Ts1 < start Ts2, then Tx2 is guaranteed to see what Tx1 commits, or Tx1 aborted
              1. in anther word, if Tx2 sees commit of Tx1, then commit Ts1 < start Ts2
                1. this is ensured by the monotonical increase of Time Oracle
            2. if commit Ts2 > commit Ts1, then Tx1 cannot actually commit before Tx2
              1. this is guaranteed by the locking before acquire commit timestamp
            3. more .. you may find that commit-wait thinkings in Spanner looks like here
    3. notifications
      1. multiple threads distributed scan the dirty column
      2. the “bus clumping” issue
        1. multiple scanners (buses) overlaps, the first one runs slow, becauses it loads all dirty data (passengers)
           the following scanners (buses) are fast, because they don't have dirty data now
           eventually, all scanners clumping to the first one.
        2. how to solve it
          1. when a scanning thread discovers that it is scanning the same row as another thread,
             it chooses a new random location in the table to scan
    4. others
      1. Percolator performs around 50 individual Bigtable operations to process a single document
      2. Percolator attempts to predict, each time a column is read, what other columns in a row will be read later in the transaction
      3. We chose this thread-per-request model mainly to make application code easier to write
      4. we’ve seen that this costs a significant 30-fold overhead compared to traditional database architectures

2. Spanner: Google's globally distributed database    [2013, 1081 refs]
   https://research.google.com/archive/spanner.html
    1. good paper. for the TrueTime, for the global replicated SQL relational strong consistency DB
    2. highlights
      1. data structure and replication
        1. partitions
          1. 1 or more fragments <- directory (or call bucket)
             multiple directories <- a tablet
             tablet is the unit of replication
            1. put directories need to accessed together in one tablet
               this also eases distributed transaction
          2. each directoy typically corresponds to a customer app
        2. tablet is replicated by paxos, called a paxos group
          1. one replica is selected as a leader
            1. if a transaction involves mutiple paxos groups, the leader does coordination
          2. there are readonly replicas, non-voting, just readonly
        3. the underlying filesystem is Colossus, the successor of Google File System
        4. directory is the unit of data placement, migration moves directory by directory
        5. hierarchical table schema
          1. frequent child table is inline clustered into the partent table
      2. True Time
        1. TrueTime uses both GPS and atomic clock as time reference, they have different failure modes
          1. a set of time master machines per datacenter and a timeslave daemon per machine
            1. The majority of masters have GPS receivers with dedicated antennas
              1. GPS masters advertise uncertainty that is typically close to zero
              2. The remaining masters (called Armageddon masters) are equipped with atomic clocks
      2. Daemons apply a variant of Marzullo’s algorithm [27] to detect and reject liars
      3. Between synchronizations, a daemon advertises a slowly increasing time uncertainty, e
        1. e varying from about 1 to 7 ms
        2. the current applied drift rate is set at 200 microseconds/second
    3. transaction and consistency
      1. Spanner is using pessimistic, strict 2PC locking, transaction.
        1. a bit like Percolator, but actually more pessimistic
      2. paxos leader's disjointness invariant:
        1.for each Paxos group, each Paxos leader’s lease interval is disjoint from every other leader’s
      3. external consistency invarient:
        1. if the start of a transaction T2 occurs after the commit of a transaction T1,
           then the commit timestamp of T2 must be greater than the commit timestamp of T1
        2. There is proof in paper in section 4.1.2
          1. this is how 2e commit-wait comes, the wait time impact transaction latency, and introduces the need to use TrueTime
            ---
            s1 < tabs(e commit 1 )                   (commit wait)
            tabs(e commit 1 ) < tabs(e start 2 )     (assumption)
            tabs(e start 2 ) ≤ tabs(e server 2 )     (causality)
            tabs(e server 2 ) ≤ s2                   (start)
            s1 < s2                                  (transitivity)
            ---
      4. read-write transactions
        1. the client drives two-phase commit
        2. start timestamp -> prepare timestamp -> commit timestamp
        3. commit-wait (see previous): coordinator leader waits until TT.after(s commit) to obey the commit-wait rule
          1. the 2e wait time is typically overlapped with paxos communication
      5. read-only transaction
        1. Spanner requires client to tell scope of all read keys before transaction starts
        2. Spanner providers a global safe timestamp, below which no in-flight or future transaction can possibly commit
           the global safe commit typically lags current time by 5-10 seconds. reads are safe to run
      6. schema-change transaction
        1. schema-change is non-blocking.
        2. time t is registered, any dependent transaction may proceed if timestamp before t, but must block otherwise
      7. refinements
        1. When a read arrives, it only needs to be checked against the fine-grained safe time for key ranges with which the read conflicts
          1. like the "vector clock" per node, vs per object, vs per partition/group
    4. F1
      1. "as part of a rewrite of Google’s advertising backend called F1 [35]"
        1. when using MySQL, "The last resharding took over two years of intense effort"
      2. F1 chose spanner because
        1. Spanner removes the need to manually reshard
        2. Spanner provides synchronous replication and automatic failover
        3. but
          1. Spanner does not yet provide automatic support for secondary indexes
            1. F1 built it by themselves
    5. others
      1. related works
        1. "Calvin [40] eliminates concurrency control: it pre-assigns timestamps and then executes the transactions in timestamp order"
    n. related materials
      1. Spanner-cap-truetime-transaction.md
       https://github.com/pingcap/blog-cn/blob/master/Spanner-cap-truetime-transaction.md
       Life of Cloud Spanner Reads & Writes
       https://cloud.google.com/spanner/docs/whitepapers/life-of-reads-and-writes
      1. they illustrate more details of how Spanner handle shortcut reads
        1. Single Split Write
        2. Multi Split Write
        3. Strong Read
      2. TiDB is actively learning from Spanner & Percolator

3. F1: A Distributed SQL Database That Scales    [2013, 157 refs]
   https://www.cs.cmu.edu/~pavlo/courses/fall2013/static/slides/f1.pdf
   https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41344.pdf
    1. F1 is used by Google Ad Business, in effort to migrate from MySQL backends to Spanner.
    2. highlights
      1. F1 introduce new features atop Spanner
        1. Distributed SQL queries including Join
        2. secondary indexes
          1. Stored as separate tables in Spanner
          2. global secondary indexies, Consistently updated via 2PC
        3. Asynchronous schema changes
          1. interesting. this is borrowed in TiDB as in blog
             https://github.com/pingcap/blog-cn/blob/master/Spanner-cap-truetime-transaction.md
          2. full details in [20] Online, asynchronous schema change in F1
        4. Optimistic Transactions
          1. by re-read timestamps and check differ
          2. it's built on top of Spanner's strict 2PC locking transaction
      2. Data Models
        1. Clustered Hierarchical: Child table clustered/interleaved within the rows from its parent table
    n. related materials
        1. F1: the fault-tolerant distributed RDBMS supporting google's ad business    [2012, 65 refs]
           https://research.google.com/pubs/pub38125.html
            1. Co-develop with Spanner. Underlying Storage - Spanner. 
               F1 has, on-blocking schema changes. Secondary indexes.
               Performance, Very high commit latency - 50-100ms. 5-10ms reads, 50-150ms commits
               Hierarchical Schema
            2. highlights
              1. the "2.1 Spanner" summary is useful
        2. F1 vs Spanner
          1. F1 And Spanner Holistically Compared
             http://highscalability.com/blog/2013/10/8/f1-and-spanner-holistically-compared.html
            n. related materials
              1. Spanner vs. F1：谷歌两大数据管理利器的整体对比及关联
                  https://www.csdn.net/article/2013-10-10/2817138-f1-and-spanner-holistically-compared
          2. 谈谈Spanner和F1
             https://segmentfault.com/a/1190000009707788
          3. Google的分布式关系型数据库F1和Spanner
             http://www.cnblogs.com/foxmailed/p/4366692.html
          4. How is F1 different from Megastore?
             https://stackoverflow.com/questions/13852494/how-is-f1-different-from-megastore
        3. Online, asynchronous schema change in F1    [2013, 26 refs]
           https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41376.pdf
            1. good paper. online async distributed table schema change is a unique feature implemented. this paper also provided formal model.
            2. schema changes through a series of intermediate states.
               it's like a big transaction with weak consistency, propagating in single direction, and each step visible to outside,
               but restirct operations so it won't corrupt
                1. in openstack cinder, there were also practices in upgrade to upgrade DB schema while tolerating failure
                   create a shadow, column/index/etc, populate data but not visible, then put it out when ready
            4. if adding a new optional structure element: absent -> delete only -> public
               if adding a new required structure element: absent -> delete only -> write only -- [db reorg backfill all missing] --> public
                1. structural schema elements include table, column, and index.
                   index is also like a table, so appliable for the techniques on table
                2. adding or dropping a lock are equivalent to adding or dropping a required column
                3. figure 3 is useful. it shows overall states transition
            5. F1 represents the entire database schema as a protocol buffer-encoded file
               it is generated from source stored in version control system
               people use the verison control system to manage/update F1 schema
                1. this also allows them to batch several updates in one schema change operation. good design
            6. database reorganization is implemented by background with MapReduce framework

4. Spanner, TrueTime & The CAP Theorem    [2017, 11 refs]
   https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45855.pdf
    1. The newer article to explain the key design concepts in spanner
    2. highlights
        1. spanner claim to be a "CA" system. It is meaningful than "P" that
             1) the system already has high enough availability besides the cap of CAP
             2) network partition is low probability outage
        2. spanner employs 2PC for distributed transaction. 2PC is named "anti-availability" [Hel16], because each member has to be up and work.
           Spanner mitigates this by having each member be a Paxos group, thus ensuring each 2PC "member" is highly available
        3. what is external consistency: for any two transactions T1 and T2, if T2 starts to commit after T1 finishes committing,
           then the timestamp for T2 is greater than T1.
            1. more explanations - Cloud Spanner: TrueTime and External Consistency
               https://cloud.google.com/spanner/docs/true-time-external-consistency
                1. compared Percolator, I think, the diff from spanner is, each replica is getting timestamp from different sources.
                   so without external consistency, it's possible that replicas disagree with T1->T2 ordering
        4. TrueTime has bigger use than Spanner. E.g. TrueTime makes it possible to take snapshots across multiple independent systems

5. Hyder - A Transactional Record Manager for Shared Flash    [2011, 130 refs]
   http://web.eecs.umich.edu/~michjc/eecs584/Papers/cidr11_hyder.pdf
    1. paper from Microsoft. using shared log + multiple * single-know-all sql database server.
       transactions broadcast so each node knows everything and can resolve conflicts.
       has some similarity to AWS Aurora Multi-master
    2. highlights
        1. how Hyder works
            1. multiple active-active sql database, backed by one shared distributed log system.
            2. there is no data partitioning, like the otherwise approach took by Spanner. each sql database see single trueth from the backend log
            3. transaction is not distributed, it is done within one sql database. there is no need for two-phase commit. throughput is backed by the distributed backend log system
            4. to resolve transaction conflicts
                1. each transaction in a sql database server is broardcase to every other sql database server.
                2. each know all states. the use the "meld algorith" to merge tree index and resolve conflicts
                3. so generally it looks like a shared everything architecture, like Oracle's, but with log backend rather than shared SAN disks
            5. index data structure - using copy-on-write tree
                1. has the general issue of changes on leaf propagate to root, and need to change every node on path
                2. to mitigate it, works on batch, and use "meld algorithm" to merge changes and reduce the churn
            6. log system failure recovery: using Vertical Paxos to agree on sealing a stripe
        2. problems / questions
            1. since a transaction is handled by single sql database, there is no partition, so the transaction processing speed could be limited.
                1. the underlying distributed logging does improve write throughtput
            2. the transaction broadcast to every server can be expensive. and single server unavailable / lagging may hinder overall performance
                1. if the paper assume big memory high network interconnect environment, it could be acceptable
            3. every sql database server independently calculate their meld algorithm and conflict resolving. the duplicated computation wastes.
                1. so the paper mentioned many-core where we can dedicate several cores for it
            4. the copy-on-write tree index structure is subject to the common issue of, leaf change propagates to root and we need to COW each nodes on path
                1. the batched transaction handling and meld algorithm mitigate the issue
        3. looks similar to AWS Aurora Multi-master
           https://www.slideshare.net/AmazonWebServices/deep-dive-on-the-amazon-aurora-mysqlcompatible-edition-dat301-reinvent-2017#33
            1. multiple master sql database on a shared distributed log system
            2. how Aurora resolves multi-master conflict?
                1. both database server and storage nodes can resolve local conflicts.
                   so true conflicts only happen when changed at both multiple database servers AND multiple storage nodes
                2. there is a Regional resolver, which communicates with the two conflicting master database servers, to arbitrate the conflict
        4. others
            1. Dan et al. [11]: Modeling the Effects of Data and Resource Contention on the Performance of Optimistic Concurrency Control
               Dan et al. [12]: The Effect of Skewed Data Access on Buffer Hits and Data Contention in a Data Sharing Environment
                1. Dan et al. [11]: analytical model and simulation study of the effect of data and resource contention on transaction throughput for optimistic concurrency control
```

Other materials

```
1. "Multiversion Concurrency Control," [Online]. Available: https://en.wikipedia.org/wiki/Multiversion_concurrency_control.
    S. E. W. Z. Jiaqing Du, "Clock-SI: Snapshot Isolation for Partitioned Data Stores Using Loosely Synchronized Clocks".

2. Linearizability versus Serializability
   http://www.bailis.org/blog/linearizability-versus-serializability/
   from: https://stackoverflow.com/questions/40274040/what-is-the-truetime-api-in-googles-spanner

3. Consistency Models
   https://en.wikipedia.org/wiki/Consistency_model

4. vector clock, logical clock, optimizations; version vectors; MVCC, versions; write and read quorums; snapshot isolation
    https://vladmihalcea.com/how-does-mvcc-multi-version-concurrency-control-work/
    https://www.quora.com/NoSQL-What-is-the-difference-among-MVCC-vector-clocks-and-locks-How-they-will-affect-performance
    http://sergeiturukin.com/2017/06/26/hybrid-logical-clocks.html
    https://books.google.com.sg/books?id=YKMLCwAAQBAJ&pg=PA293&lpg=PA293&dq=MVCC+vs+logical+clock
    https://www.safaribooksonline.com/library/view/advanced-data-management/9783110433074/html/Chapter13.html
    1. the book advanced-data-management, snapshot isolation rules can be used as a reference
    2. Non-Monotonic Snapshot Isolation: scalable and strong consistency for geo-replicated transactional systems
       https://pages.lip6.fr/Marc.Shapiro/papers/NMSI-SRDS-2013.pdf

5. HopsFS: Scaling Hierarchical File System Metadata Using NewSQL Databases
    https://www.usenix.org/system/files/conference/fast17/fast17-niazi.pdf
      1. talked about how to build the distributed transaction layer for filesystem metadata operation

6. vCorfu: A Cloud-Scale Object Store on a Shared Log
    https://www.usenix.org/conference/nsdi17/technical-sessions/presentation/wei-michael
      1. check the distributed transaction implementation here

7. I Can’t Believe It’s Not Causal! Scalable Causal Consistency with No Slowdown Cascades
    https://www.usenix.org/system/files/conference/nsdi17/nsdi17-mehdi.pdf
      1. snapshot isolation transaction implemented based on casual consistency. interesting alternative approach.
```
