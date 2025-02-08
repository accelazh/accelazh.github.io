---
layout: post
title: "A Summary of Distributed Transaction Implementation"
tagline : "A Summary of Distributed Transaction Implementation"
description: "A Summary of Distributed Transaction Implementation"
category: "Database"
tags: [cloud, transaction, summary, database, storage]
---
{% include JB/setup %}

Complex summary of distributed transaction & consistency, attached it below. I will tidy it up and translate it later when I have time.

```
1. reading & investigation & summary: 分布式事务、交易系统、互联网支付系统设计
    1. 保证分布式系统数据一致性的6种方案（实际上，是互联网交易系统的设计，还有最终一致性的分布式事务）
       https://mp.weixin.qq.com/s?__biz=MzAwMDU1MTE1OQ==&mid=2653546976&idx=1&sn=c3fb2338389a41e7ab998c0c21bd3e5d
        1. 消息可以是被发送一次或者多次的，但至少发送一次
            1. 消息发送不应该是动作，而应该是状态的传播。通常是对业务透明地，用中间件，根据本地数据库事务表的变化，自动发送消息，并保证一定发送
           幂等性：订单/买卖执行应该是幂等性的，同一个transaction id最多执行一次，可以利用DB的if语句或DB的compare and swap
                                                可以回滚，最多回滚一次 （上述，可以用一个专门的applied_transaction表实现）
        2. 满足1的话，多个子系统的transaction，可以叠加为一个分布式的大transaction。
           由一个中控结点反复监控transaction被全部执行或回滚    # 注意，这时是弱一致性，因为某个子系统可能未执行成功transaction
           基本思想类似于DB里放了一个WAL（Write-ahead Logging）表
        3. MVCC的话，版本比较->落盘日志（日志可能事先写好，直接swap in）->内存中写入新版本数据->增加版本号，这一系列需要原子完成
           单机可以尝试用compare_and_swap；如果用Paxos的话，本质上是可以用锁实现的。
        4. 电商的基本思路是，不使用分布式事务，它太重了。把一个大事务划分成N个子系统的各自的小事务，一部分立即执行（要求实时的），一部分通过消息队列异步执行。
           小事务执行的时间是不确定的，总体上是最终一致性。
           部分小事务的执行如果有顺序要求，如要求A->B->C->D，则可以A玩了再发给B消息，B完了在发给C消息。如果其中一部失败，那么发送全局废单消息，A、B、C、D各自回滚。
           所有子事务的执行、回滚都是幂等性的。
           ——总结而言，大分布式事务划分为多个子事务，子事务的执行是幂等性的，消息保证至少发送一次；那么订单状态一定会逐渐传播至整个系统，最终一致性。
        5. 如果有一个中心的coordinator来监控transaction各部分的执行的话，它自己的DB表，其实就相当于一个WAL
        6. NoSQL数据库没有事务支持，但应该可以用原子的conditional update来实现子事务同等语义
           例如，给数据加一个版本号字段
    2. Dubbo中的分布式事务
        1. http://javatar.iteye.com/blog/981787
           http://www.iteye.com/magazines/103#250
           http://www.dewen.net.cn/q/17502/Dubbo%E6%A1%86%E6%9E%B6%E4%B8%8D%E6%94%AF%E6%8C%81%E4%BA%8B%E5%8A%A1%EF%BC%8C%E9%82%A3%E9%9C%80%E8%A6%81%E6%80%8E%E4%B9%88%E6%A0%B7%E6%89%8D%E8%83%BD%E5%AE%9E%E7%8E%B0%E4%BA%8B%E5%8A%A1%E6%94%AF%E6%8C%81%E3%80%82%E8%A6%81%E6%80%8E%E4%B9%88%E6%89%A9%E5%B1%95%EF%BC%9F
           http://dubbo.io/User+Guide-zh.htm#UserGuide-zh-%E5%88%86%E5%B8%83%E5%BC%8F%E4%BA%8B%E5%8A%A1
           https://groups.google.com/forum/#!topic/dubbo/OCNBBzEQqzg
           http://my.oschina.net/alexgaoyh/blog/519237
           http://itindex.net/detail/52377-%E4%BB%A3%E7%90%86-spring-service
           https://github.com/dangdangdotcom/dubbox/issues/60
           http://www.cfanz.cn/index.php?c=uc/topic&a=read&id=15406
        2. 一些分布式事务处理的资料
            1. http://tech.dezai.cn/Detail.Aspx?AI=90001
            2. http://wenku.baidu.com/view/3e2a8ff79e31433239689358.html
        n. summary
            1. Dubbo不支持分布式事务，但可被Java TransactionManager管理，成为事务中的一部分。实用性不强
    3. write-ahead logging以及其幂等性idempotency的实现
        1. http://work.tinou.com/2012/09/write-ahead-log.html
        2. http://pages.cs.wisc.edu/~travitch/notes/cs764-notes-final.pdf
        3. https://courses.cs.washington.edu/courses/cse444/12sp/lectures/lecture18-19-transactions-aries.pdf
        4. https://parasol.tamu.edu/people/welch/teaching/310.f07/s22.ppt
        5. https://www.cs.columbia.edu/~du/ds/assets/lectures/lecture15.pdf
        n. summary
            1. 对db而言，log entry的执行是idempotent的，其中记录是final value（redo log）或original value（undo log），而不是做什么操作（不然无法idempotent）
               log entry中必须记录final value，那么生成时，read操作必须上lock，以保证final value是真实有效的
                    read (A, B) -> operate (A, B) -> commit log of (A, B) final value -> update (A, B) in memory，这期间（A，B）不会被其它transaction干扰
               对于MVCC，估计是
                    record version -> read (A, B) -> operate (A, B) -> prepare log of (A, B) final value -> prepare update of (A, B) in memory -> compare version and swap
                    compare and swap，或者某种原子性操作(double-checked-log?)，必须保证log和内存数据都是原子性地被swap in的
                        我猜可以是把transaction实现把log写进log流中，但只有compare version确定提交后，才把该log entry标记为有效的。因为有disk操作，估计还是得小范围上写锁。
            2. ARIES is the famous write-ahead logging algorithm
    4. Idempotency的实现，互联网支付和transaction系统中
        1. http://codebetter.com/gregyoung/2010/08/12/idempotency-vs-distibuted-transactions/
        2. http://hans-study.googlecode.com/svn/docs/%E5%B9%82%E7%AD%89_%E9%87%8D%E5%A4%8D%E6%8F%90%E4%BA%A4_%E4%B9%90%E8%A7%82%E9%94%81.pdf
        3. http://yongpoliu.com/idempotent/
        4. http://itindex.net/detail/40761-%E7%94%B5%E5%95%86-%E5%B9%82%E7%AD%89
        5. http://read01.com/0GENL.html
        6. http://www.cnblogs.com/weidagang2046/archive/2011/06/04/idempotence.html
        7. http://www.infoq.com/cn/news/2013/05/idempotent
        8. http://csrd.aliapp.com/?p=671
        n. summary
            1. 有DB的情况下，可以使用一个applied_transaction表，在事务中包含if not applied, do it and update applied。（另一个类似是排重表，可以是记transaction或消息）
            2. 有DB的情况下，可以使用conditional update或叫DB compare-and-update。类似上一个，只需不需要事务了，只需要原子性的conditional update的SQL语句。
            3. 无DB的情况下，使用lock：测试transaction状态->修改数据->更新transaction状态 （另外还得实现修改数据的原子性）
                             使用MVCC：记录版本->测试transaction状态->修改数据->更新transaction状态->测试版本->retry 或 atomic(测版本+提交数据+更新版本) （另外还得实现修改数据的原子性）
               目测略难，可用paxos实现，需要小范围上（写）锁
            4. API层设计，所有操作被改成创建一个transaction -> 执行一个transaction；transaction执行是幂等的（例子如取钱，用ticket号）
            5. 发送消息，可以保证至少发送一次（可能发送多次），方法是用一个message_sent表（或直接用业务表）跟踪状态和定期检查重发
    5. MVCC and transaction
        1. https://en.wikipedia.org/wiki/Multiversion_concurrency_control#Databases_with_MVCC
        2. https://devcenter.heroku.com/articles/postgresql-concurrency
        3. http://stackoverflow.com/questions/27499/database-what-is-multiversion-concurrency-control-mvcc-and-who-supports-it
        4. http://www.xaprb.com/blog/2013/12/28/immutability-mvcc-and-garbage-collection/
        5. http://coolshell.cn/articles/6790.html
        6. http://blog.notdot.net/2009/12/Damn-Cool-Algorithms-Log-structured-storage
        7. https://github.com/cmu-db/peloton/wiki/Write-Ahead-Logging
        8. http://www.enterprisedb.com/postgres-plus-edb-blog/amit-kapila/well-known-databases-use-different-approaches-mvcc
        n. summary
            1. the basic idea of MVCC: do first, compare the version, if someone else modified the data, then retry
            2. Write-ahead logging and ACID, caching, MVCC, and old-version-purge are often intertwined to some extent. there are entire books about it
               http://www.amazon.com/Transaction-Processing-Concepts-Techniques-Management/dp/1558601902/?tag=xaprb-20
               http://www.amazon.com/Transactional-Information-Systems-Algorithms-Concurrency/dp/1558605088/?tag=xaprb-20
            3. DB MVCC并未说一定是compare-and-swap，我估计，如上文分析，还是需要小范围的上写锁。搜索的资料中并未排除这种可能。
            4. 想到一个DB MVCC + Journal的方案，日志写可以放到version检查之后
               记录版本 -> 读数据 -> 操作 -> 写入内存数据 -> atomic（检查本版 -> 胜出：换入内存数据并更新版本 / 失败：回到开头） -> 日志写入磁盘 -> 返回用户提交成功
               有可能一个更新的写的日志项，排在旧写的日志项的前头，因此日志项需要带上版本号以识别旧写（旧写还是需要被apply，因为它不一定只改一处）
    6. MVCC and distributed transaction
        1. http://www.nuodb.com/techblog/mvcc-part-4-distributed-mvcc
        2. http://blog.csdn.net/zhang_shuai_2011/article/details/45673975
        3. http://www.yankay.com/google-spanner%E5%8E%9F%E7%90%86-%E5%85%A8%E7%90%83%E7%BA%A7%E7%9A%84%E5%88%86%E5%B8%83%E5%BC%8F%E6%95%B0%E6%8D%AE%E5%BA%93/
        4. http://stackoverflow.com/questions/18384883/why-is-googles-truetime-api-hard-to-duplicate
        5. http://www.leafonsword.org/google-spanner/
        n. summary
            1. 对于分布式事务，MVCC的思路也可以应用，集群需要一个consensus的version记录，和consensus的锁服务
                记录version -> 准备每一个node的内存更新 -> atomic（测试version -> 提交每一个node的内存更新，并递进version） 或 失败重试 -> 包含version号的日志落盘 -> 返回用户提交成功
            2. 或者更朴实的做法是，选出一个leader node做仲裁，写的node需要broadcast-before-commit（其实leader node也相当于MVCC的central consensus）
            3. spanner的TrueTime API，using GPS, atomic clocks？如何实现分布式事务的？
    7. cockroachdb - 支持MVCC的分布式事务的DB（和跨数据中心复制）
        1. http://www.infoq.com/cn/news/2014/08/CockroachDB
        2. http://thenewstack.io/cockroachdb-unkillable-distributed-sql-database/
        3. https://www.cockroachlabs.com/blog/how-cockroachdb-distributes-atomic-transactions/
        4. https://github.com/cockroachdb/cockroach/blob/master/docs/design.md#lock-free-distributed-transactions
        5. https://smazumder05.gitbooks.io/design-and-architecture-of-cockroachdb/content/architecture/lock-free_distributed_transactions.html
        6. https://www.cockroachlabs.com/blog/sql-in-cockroachdb-mapping-table-data-to-key-value-storage/
        7. https://news.ycombinator.com/item?id=10160797
        8. https://www.cockroachlabs.com/blog/living-without-atomic-clocks/
        n. summary
            1. cockroachdb is SQL, underlying it is a distributed sorted key-value store, it supports distributed transaction (MVCC, full ACID strong consistency)
               local store is RocksDB (which is based on LevelDB)
            2. cockroachdb is writen in Golang
            3. create switch -> stage -> filter -> flip -> unstage; accessing to switch itself is exclusive, switch direct read/write to data/staged
               it seems, version is by using timestamp, timestamp is from Hybrid Logical Clock; doesn't see explicit lock, other things not quite understand
               WHATEVER, WAIT TO EXPLORE ...: https://github.com/cockroachdb/cockroach/blob/master/docs/design.md#lock-free-distributed-transactions
            4. to map sql table to key-value store: in kv it stores like: tableID/primary/primaryKeyVal/columnID->columnVal (since kv is sorted, easy to fetch entire row)
               a secondary index stores like: tableID/indexID/indexColumnVals/primaryKeyVal/columnID->NULL (we need primaryKeyVal here also because index column may not be unique)
            5. 有分布式NoSQL store，其支持conditional update，那么可以实现MVCC分布式事务吗？
               可以认为，一个分布式事务，是由各个NoSQL结点的local transaction组合成。我们把事务信息记录到coordinator后，其实就相当于有了WAL。后面就等待状态传播到所有子节点即可。最终一致性经过等待，就可以变成强一致性。
               这个时候真正怕的问题，是casual related的事务不按顺序执行，发生冲突。互联网公司貌似库存加减场景，不同大事务的子事务的执行顺序貌似没要求。但分布式数据库需要考虑这点；用来检测事务冲突的timestamp，貌似就非常需要了。于是有了TrueTime或Cockroach的算法，以提高精度、绕过uncertainty。貌似是这样。
            6. 其它，blog中可以包含的内容
                1. background: 2PC 3PC
                   paxos, zookeeper: locking, distributed transaction
                   idempotent: how to do it in paxos, in db transaction
                   transactional messaging & kafka
                   eventual consistency, of transaction, BASE, ACID
                   transfer state rather than action
                   asynchronized, scalable,
                   对账系统，中控事务状态的跟踪和管理
                   支付系统、交易系统
                   WAL， redu/undo, ARIES, idempotent
                   MVCC, db, paxos
                   trading systems, internet company order/trading/payment system
                   DB table as the write-ahead log
                   the power of conditional update
    8. 更多理论
        1. Concurrency Control in Distributed Database Systems     [1272 references, 1981]
           http://www.cs.berkeley.edu/~brewer/cs262/concurrency-distributed-databases.pdf
            1. timestamp ordering的transaction思路完全不同，它通过给read/write分配好它们在未来什么时候执行的timestamp，来使transaction序列化
               加锁、重试都变得不再那么需要了
               参见4.1 Basic T/O Implementation
                1. 每个item有item.read_timestamp和item.write_timestamp，它们记录将要在其上执行的transaction的read/write的最大timestamp
                2. 对于发射过来的一个read，如果read.timestamp < item.write_timestamp，那么拒绝该read；否则允许其发射，并更新item.read_timestamp = read.timestamp
                3. 对于发射过来的一个write，如果write.timestamp < item.read_timestamp，那么拒绝该write；否则允许其发射，并更新item.write_timestamp = write.timestamp
            2. 另，见wiki: Timestamp-based concurrency control
               https://en.wikipedia.org/wiki/Timestamp-based_concurrency_control
            3. timestamp ordering: more materials
                1. Concurrency Control – Time Ordering
                   https://discovery.csc.ncsu.edu/Courses/csc742-S02/T14_CControl_TO_6.pdf
                2. DBMS - Concurrency Control
                   http://www.tutorialspoint.com/dbms/dbms_concurrency_control.htm
                    1. DB事务/并发控制有两类算法
                        1. Locked Based
                            1. Simplistic Lock Protocol: allow DB to obtain a lock on every object before a write
                            2. Pre-claiming Lock Protocol
                            3. Two-Phase Locking 2PL
                            4. Strict Two-Phase Locking
                        2. Timestamp Based
                            1. it is the most commonly used
                            2. Timestamp Ordering Protocol
                3. http://www.cs.virginia.edu/~son/662.pdffiles/662.to.pdf
                4. http://courses.cs.vt.edu/~cs5204/fall00/distributedSys/bto.html
                5. http://www-i4.informatik.rwth-aachen.de/content/teaching/lectures/sub/vs/vsSS06/08_Transactions2_1P.pdf
                6. https://www.youtube.com/watch?v=zzHjRWkL4_Y
                7. https://www.youtube.com/watch?v=ompcyEsxkoc
                8. https://www.quora.com/What-is-the-difference-between-timestamp-and-two-phase-locking-protocol-in-DBMS
                9. Commitment ordering (CO)
                   https://en.wikipedia.org/wiki/Commitment_ordering
                    1. The commitment ordering solution for global serializability
                    2. The Vote ordering strategy for Global CO Enforcing
        2. Snapshot Isolation and Serializable Snapshot Isolation
           http://cs.nyu.edu/courses/fall14/CSCI-GA.2434-001/p729-cahill.pdf
            1. good explanation of SI problems. SI reads from the snapshot of committed transaction, so
                tx1_r(a_v1) -> tx2_(a_v1) -> tx1_op(a_v2 = a_v1 + 1) -> tx2_op(a_v2 = a_v1 + 1) -> tx1_w(a) -> tx2_w(a)
               in the end, a++ twice results in a+1
        3. Calvin: Fast Distributed Transactions for Partitioned Database Systems
           http://cs.yale.edu/homes/thomson/publications/calvin-sigmod12.pdf
            1. layer Calvin on a non-transaction storage system, to provide ACID
            2. concurrency control is done by the sequencer layer
               the locking protocol resembles strict two-phase locking
        4. How Spanner manages distributed transaction with TrueTime API
            1. good explaination of how spanner works
               By Murat etc: http://www.cse.buffalo.edu/~demirbas/publications/augmentedTime.pdf
               By Murat: http://www.cs.cmu.edu/~pavlo/courses/fall2013/static/papers/murat-spanner.pdf
               Ref to Murat: http://www.cs.cmu.edu/~pavlo/courses/fall2013/static/slides/spanner.pdf
                1. Read-write transactions use 2-phase locking and 2-phase commit
        5. By Murat & his friend: Logical Physical Clocks and Consistent Snapshots in Globally Distributed Databases - The HLC time
           http://www.cse.buffalo.edu/tech-reports/2014-04.pdf
            1. combine physical time and logical time (similar to vector clock)
            2. to enable easy identify of consistent snapshots
            3. track the causality-related event ordering
            4. for more, see the conclusion part
    9. 其它类似的分布式事务实现
        1. DynamoDB
           https://github.com/awslabs/dynamodb-transactions/blob/master/DESIGN.md
        2. Percolator
           https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf
           Spanner
           http://www.cs.cmu.edu/~pavlo/courses/fall2013/static/slides/spanner.pdf
           http://research.google.com/archive/spanner-osdi2012.pdf
           http://www.yankay.com/google-spanner%E5%8E%9F%E7%90%86-%E5%85%A8%E7%90%83%E7%BA%A7%E7%9A%84%E5%88%86%E5%B8%83%E5%BC%8F%E6%95%B0%E6%8D%AE%E5%BA%93/
           http://www.cse.iitb.ac.in/infolab/Data/Courses/CS632/Talks/spanner-osdi2012.pptx
        3. Transactions in MongoDB, Cassandra, Zookeeper and others
           http://rystsov.info/2012/09/01/cas.html
        n. summary
            1. 基本上是2PC范畴（cockroachdb也可看作2PC），需要coordinator。coordinator是存在底层分布式NoSQL Store中的，所以状态不会丢。
               NoSQL存储需要提供atomic write功能
            2. 一个更简单的算法，甚至连version号都不需要。前提是底层NoSQL存储支持conditional update操作（CAS）
               每个kv item，都需要配一个tx字段，表示当前进行中的transaction，还需要配一个update字段，记录当前正在写，还没提交的value
               以下算法，适用于单机或分布式事务
                1. 类型1：这个算法相当于先依次给需要更新的item上了锁，后续transaction必须等待锁释放才能执行。
                   读有可能读到未完全提交的数据（银行就不能用这种；不过也不一定，因为银行转账可以不即时到帐）。
                    ```
                    新建transaction记录，后面用my_tx指代
                    for each item needs update    # 需要按全局一致的顺序遍历item，避免死锁，或反复抢断
                        atomic（if item.tx is null, then update item.tx = my_tx.id） else
                            abort & cleanup & retry    # 需要cleanup自己上的item.tx，类似于解锁
                        item.update = my_item_value
                    
                    my_tx.state = committing
                    for each item needs update
                        item.value = item.update    # 注意，读时可能读到transaction进行中的数据
                    
                    write journal to disk
                    my_tx.state = committed
                    return to user with transaction succ
                    
                    for each item needs update
                        item.tx = null
                    ```
                   transaction由一个或多个coordinator执行，NoSQL Store保证其数据不丢失，挂了之后重启即可。
                2. 类型2：后到的事务会抢断之前的事务。读有可能读到未完全提交的数据
                    ```
                    create my_tx in transaction table
                    for each item needs update    # 需要按全局一致的顺序遍历item，避免死锁，或反复抢断
                        loop1: 
                        atomic ( if item.tx is null, then update item.tx = my_tx.id) else
                            its_tx = item.tx
                            if ( its_tx == null
                                    || its_tx.state == aborted
                                    || (its_tx.state < committing    # 如果前者事务还没开始提交，那么就可以抢断
                                    && 抢断条件(its_tx)))    # 为了避免两个事务反复互相抢断，我们须有某种优先级比较，多次重试时自动跳到最大优先级（不能抢断最大优先级）
                                atomic ( if item.tx == its_tx && its_tx.state < committing, then item.tx.state = abort ) else
                                    goto loop1
                                atomic ( if item.tx == its_tx, then item.tx = my_tx) else    # 以防中途item.tx发生变化
                                    goto loop1
                                atomic ( if item.tx == my_tx, then item.update = my_item_update ) else
                                    goto loop1
                            else
                                abort & retry as a new transaction    # 不需要cleanup自己上的item.tx，因为可以被抢断；但应新建一个不同的transaction了
                    
                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # my_tx一旦进入committing，便不再可以抢断
                        abort & retry as a new transaction
                    for each item needs update
                        item.value = item.update    # 注意，读时可能读到transaction进行中的数据
                    
                    write journal to disk
                    my_tx.state = committed
                    return to user with transaction succ
                    
                    for each item needs update
                        item.tx = null
                    ```
                    transaction由一个或多个coordinator执行，NoSQL Store保证其数据不丢失，挂了之后重启即可。
                
                3. 我们现在有三个问题
                    0. 最初一个问题是，transaction是否可抢断，上面两个算法在干这个
                    1. read是可以看见transaction进行中部分提交的数据的，这不符合事务语义，例如银行就不能用
                       解决这个问题，八成需要引入version（或者timestamp）
                    2. 能否省去item.value = item.update / item.value = my_tx.item.update，由后续读操作自己处理？
                       CockroachDB应该是采用了上述方案（https://github.com/cockroachdb/cockroach/blob/10dfc9deb99bcde726dc3c45b03a9ef86ca56dd7/docs/design.md （"Transaction execution flow".2））
                    3. version应该是和timestamp能够相互替换的。之所以要把version换成timestamp，估计是为了去中心（待验证）。
                       但是，timestamp的draft误差问题就引来了Spanner的TrueTime API，或者CockroachDB的HLC time方案
                       Cockroach选用了timestamp替代version

                4. 类型3：不可抢断transaction；read可看见transaction部分提交的数据；不使用versoin；写事务不做item.value = item.update的更新
                    ```
                    create my_tx in transaction table
                    for each item needs update    # 需要按全局一致的顺序遍历item，避免死锁，或反复抢断
                        atomic（if item.tx is null, then update item.tx = my_tx.id） else
                            abort & cleanup & retry    # 需要cleanup自己上的item.tx，类似于解锁
                    
                    for each item needs update
                        item.value = my_item_value

                    write journal to disk
                    my_tx.state = committed    # 读时可能读到transaction进行中的数据
                    return to user with transaction succ

                    for each item needs update
                        item.tx = null
                    ```
                    对于读操作，因为允许读到transaction部分提交的数据，那么
                    ```
                    read item.value
                    ```
                    上述可以看出，如果允许read读到transaction部分提交的数据，其实根本就不需要item.update字段了
                    transaction的意义也被打破，实际上只保证了写操作组的隔离；读可以乱来，transaction实际上没用了，因为一个transaction可能是基于这种读做的操作；
                5. 类型4：和上一个算法相似，只是允许transaction抢断。注意因为能读到部分提交的数据，这其实还是一个无效的transaction实现
                    ```
                    create my_tx in transaction table
                    for each item needs update    # 需要按全局一致的顺序遍历item，避免死锁，或反复抢断
                        loop1: 
                        atomic ( if item.tx is null, then update item.tx = my_tx.id) else
                            its_tx = item.tx
                            if ( its_tx == null
                                    || its_tx.state == aborted
                                    || (its_tx.state < committing    # 一个已经进入committing阶段的transaction相当于已经胜出，不能再抢断
                                    && 抢断条件(its_tx)))    # 为了避免两个事务反复互相抢断，我们须有某种优先级比较，多次重试时自动跳到最大优先级（不能抢断最大优先级）
                                atomic ( if item.tx == its_tx && its_tx.state < committing, then item.tx.state = abort ) else
                                    goto loop1
                                atomic ( if item.tx == its_tx, then item.tx = my_tx) else    # 以防中途item.tx发生变化
                                    goto loop1
                                atomic ( if item.tx == my_tx, then item.update = my_item_update ) else
                                    goto loop1
                            else if (its_tx.state == committed)    # 懒惰地将已提交的transaction的item.update更新到item.value
                                atomic ( if item.tx == its_tx, then item.value = item.update ) else
                                    goto loop1
                                atomic ( if item.tx == its_tx, then item.tx = null) else
                                    goto loop1
                                goto loop1
                            else
                                abort & retry as a new transaction

                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # my_tx一旦进入committing，便不再可以抢断
                        abort & retry as a new transaction

                    write journal to disk
                    my_tx.state = committed
                    return to user with transaction succ
                    ```
                    对于读操作，如果允许读到部分提交的transaction
                    ```
                    read item.value
                    ```
                    对于读操作，如果不允许读到transaction部分提交的数据，那么应该根据item.tx的状态，来传递读，传递是单向的
                    ```
                    loop1:
                    its_tx = item.tx
                    if (its_tx != null && its_tx.state == committed) 
                        atomic ( if item.tx == its_tx, then read item.update ) else   # 要如何实现conditional read？倒是可以用atomic的item.value=item.update来代替
                            goto loop1
                    else
                        atomic ( if item.tx == its_tx, then read item.value) else
                            goto loop1
                    ```
                6. 上述大部分方法都不是完整的事务语义，因为读可能读到部分提交的事务。更完整的transaction语义应该是
                    1）两个事务的写操作组，不能互相穿插
                    2）一个事务可以看作是一系列读->内存运算->一系列写。事务过程中不允许穿插另一个事务的写操作
                    3）读操作不能读到部分提交的事务，即如果事务的写操作组没有全部完成，读应该是看不见的（Isolation）（例如，bank account A + B = 100，转账）
                   为了支持（3），还有（2），我估计是需要用version的了
                7. 类型5：为了满足（3），即对{item1=a_old, item2=b_old}，当一个transaction{item1=a, item2=b}提交后，要如何保证reader不能看见item1=a, item2=b_old？
                          用version版本号
                    ```
                    # transaction begin
                    create my_tx in transaction table
                    my_tx.version = generate_from_global_monotone_increasing_number()

                    # read in transaction
                    for each item to read
                        my_tx.item.version = item.version
                        loop1:
                        its_tx = item.tx
                        if (its_tx != null && its_tx.state == committed) 
                            atomic ( if item.tx == its_tx, then read item.update) else
                                goto loop1
                        else
                            atomic ( if item.tx == its_tx, then read item.value ) else
                                goto loop1

                    # write in transaction
                    for each item needs update or read    # 需要按全局一致的顺序遍历item，避免反复抢断    # write和read的item都要上锁item.tx=my_tx
                        loop2: 
                        its_tx = item.tx
                        if ( its_tx == null
                                || its_tx.state == aborted
                                || (its_tx.state < committing    # 一个已经进入committing阶段的transaction相当于已经胜出，不能再抢断
                                && 抢断条件(its_tx)))    # 为了避免两个事务反复互相抢断，我们须有某种优先级比较，多次重试时自动跳到最大优先级（不能抢断最大优先级）
                            atomic ( if item.tx == its_tx && its_tx.state < committing, then item.tx.state = abort ) else
                                goto loop2
                            atomic ( if item.tx == its_tx, then item.tx = my_tx) else    # 以防中途item.tx发生变化
                                goto loop2
                            if item needs update
                                atomic ( if item.tx == my_tx, then item.update = my_item_update ) else
                                    goto loop2
                        else if (its_tx.state == committed)    # 懒惰地将已提交的transaction的item.update更新到item.value
                            atomic ( if item.tx == its_tx, then item.value = item.update ) else
                                goto loop2
                            atomic ( if item.tx == its_tx, then item.tx = null) else
                                goto loop2
                            goto loop2
                        else
                            abort & retry as a new transaction
                                
                    # transaction commit
                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # my_tx一旦进入committing，便不再可以抢断
                        abort & retry as a new transaction

                    /* 可以把my_tx表示为read(C, A) -> write(A, B)，对于一个在my_tx读写之间完成提交的事务tx2
                    如果tx2是read(C)->write(C)，那么my_tx read item的版本号会变，但其实按照序列化要求，可以认为tx2发生于my_tx之后，my_tx可以无视版本号变化
                    如果tx2是read(C, A)->write(C, A)，那么只能序列化为tx2发生在my_tx之前，my_tx需要重启
                    如果tx2是read(C, B)->write(B)，那么只能序列化为tx2发生于my_tx之前，但my_tx可以继续执行
                    如果tx2是read(C)->write(C, A)，那么只能序列化为tx2发生于my_tx之前，my_tx需要重启
                    因此，我们可以看出，读和写的item都需要上锁（item.tx=my_tx），但只需要检查读item的版本号即可；只有读item被tx2写了的情况，才需要重启my_tx
                    */
                    for each item I read
                        if item.version != my_tx.item.version
                            abort & retry as a new transaction

                    for each item I update
                        item.version = my_tx.version

                    write journal to disk
                    my_tx.state = committed
                    return to user with transaction succ
                    ```
                8. 类型6：其实，使用抢断式的transaction，不用version号，也可以实现（3）和（2）。关键是写者会抢断读者。
                          原理是：reader不能读正在committing的item，writer进入committing状态后，abort所有reader
                    ```
                    # transaction begin
                    create my_tx in transaction table

                    # subroutine to read an item
                    def sub_read(item)
                        while (true)
                            its_tx = item.tx
                            if (its_tx.state == committing)    # reader不能去读committing的item
                                wait_for_a_short_time()
                                continue
                            if (its_tx != null && its_tx.state == committed) 
                                atomic ( if item.tx == its_tx, then read item.update) else
                                    continue
                            else
                                atomic ( if item.tx == its_tx, then read item.value ) else
                                    continue
                            atomic ( if item.tx == its_tx, then item.reader_txs.add(my_tx)) else
                                continue
                            break

                    # subroutine to write an item
                    def sub_write(item)
                        while (true)
                            its_tx = item.tx
                            if (its_tx == null || its_tx.state == aborted
                                    || (its_tx.state < committing && 抢断条件(its_tx) ))    # 事务有随机优先级，被多次抢断的事务优先级上升
                                atomic ( if item.tx == its_tx && its_tx.state < committing, then item.tx.state = abort ) else
                                    continue
                                atomic ( if item.tx == its_tx, then item.tx = my_tx) else
                                    continue
                                atomic ( if item.tx == my_tx, then item.update = my_item_update ) else
                                    continue
                            else if (its_tx.state == committed)
                                atomic ( if item.tx == its_tx, then item.value = item.update ) else
                                    continue
                                atomic ( if item.tx == its_tx, then item.tx = null) else
                                    continue
                                continue
                            else
                                abort & retry as a new transaction
                            break

                    # read in transaction
                    for each item needs read
                        sub_read(item)

                    # write in transaction
                    for each item needs update
                        sub_write(item)

                    # transaction commit
                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # 只有committing的transaction可以抢断committing的
                        abort & retry as a new transaction

                    for each item I write
                        for each r_tx in item.reader_txs    # my_tx到committing状态后，reader就不会再进入item.reader_txs了
                            if my_tx.state == abort
                                abort & retry as a new transaction
                            atomic ( if r_tx.state < committing, then r_tx.state = abort)
                            else atomic ( if r_tx.state == committing, then r_tx.state = abort)    # 可以保证，r_tx被抢断后会阻塞在read阶段
                            else atomic ( if r_tx.state == committed, then noop)
                            else noop        

                    atomic ( if my_tx.state = committing, then write journal to disk, my_tx.state = committed)
                    return to user with transaction succ 
                    ```
                9. 类型7：用timestamp代替version，且我们可以得到精确timestamp，且各节点都是一致（虽然现实上这不可能）
                         基本上，这个算法和类型5完全一样，只是把version换成了timestamp。
                    ```
                    # transaction begin
                    create my_tx in transaction table
                    my_tx.start_time = get_timestamp()

                    # subroutine to read
                    def sub_read(item)
                        atomic(    # 可以拆解成更小的atomic，以便CAS实现；此处和类型5其实没区别
                            if item.tx.state == committed
                                read item.update
                            else
                                read item.value
                        )

                    # subroutine to write & lock read
                    def sub_write_and_lock_read(item)
                        atomic ( if item.tx.state == committed, then item.value = item.update, item.tx = my_tx) else    # 此处和类型5其实没区别，只是重写了一下
                            atomic( 
                                if (item.tx == null || item.tx == aborted
                                        || (item.tx < committed && 抢断条件(item.tx)) )
                                    item.tx.state = abort; item.tx.abort_time = now()
                                    item.tx = my_tx
                                else if (item.tx.state = committed)
                                    item.value = item.update
                                    item.tx = null
                                    continue
                                else
                                    abort & retry as a new transaction
                            )
                        
                        if item need update
                            item.update = my_item_update    

                    # read in transaction
                    for each item needs read
                        sub_read(item)

                    # write & lock read in transaction
                    for each item needs update or read   # 需按顺序上锁以防死锁
                        sub_write_and_lock_read(item)
                        
                    # transaction commit
                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # committing状态后，transaction不可抢断，read和write item都不许别人写
                        abort & retry as a new transaction

                    for each item I read    # 根据类型5里的分析，只需要确保read item的version未变即可
                        if item.timestamp > my_tx.start_time
                            abort & retry as a new transaction

                    my_tx.commit_time = now()
                    for each item I write
                        item.timestamp = my_tx.commit_time

                    write journal to disk
                    my_tx.state = committed
                    return to user with transaction succ 
                    ```
                10. 类型8：用timestamp代替version，但clock有偏差skew；所以真是的time应该是在[timestamp-skew, timestamp+skew]间
                           算法和类型7基本一样，测试是否可提交时，加上skew偏差；但是这样误伤几率很大，一个在write之后skew时间内开始的transaction，很可能重启
                           不知道spanner和cockroachdb解决clock skew的方法应如何使用？
                    ```
                    # transaction begin
                    create my_tx in transaction table

                    # subroutine to read
                    def sub_read(item)
                        atomic( if my_tx.start_time == null, then my_tx.start_time = now())    # 记录first read时间作为开始时间
                        atomic(    # 可以拆解成更小的atomic，以便CAS实现；此处和类型5其实没区别
                            if item.tx.state == committed
                                read item.update
                            else
                                read item.value
                        )

                    # subroutine to write & lock lock
                    def sub_write_and_lock_read(item)
                        atomic ( if item.tx.state == committed, then item.value = item.update, item.tx = my_tx) else    # 此处和类型5其实没区别，只是重写了一下
                            atomic( 
                                if (item.tx == null || item.tx == aborted
                                        || (item.tx < committed && 抢断条件(item.tx)) )
                                    item.tx.state = abort; item.tx.abort_time = now()
                                    item.tx = my_tx
                                else if (item.tx.state = committed)
                                    item.value = item.update
                                    item.tx = null
                                    continue
                                else
                                    abort & retry as a new transaction
                            )
                        
                        if item need update
                            item.update = my_item_update    

                    # read in transaction
                    for each item needs read
                        sub_read(item)

                    # write & lock read in transaction
                    for each item needs update or read   # 需按顺序上锁以防死锁
                        sub_write_and_lock_read(item)
                        
                    # transaction commit
                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # committing状态后，transaction不可抢断，read和write item都不许别人写
                        abort & retry as a new transaction

                    for each item I read
                        if item.timestamp + skew > my_tx.start_time    # 必须确保不可能有另外的transaction发生在我的read和write之间，考虑skew误差；不过误伤范围较大，应该会经常重启
                            abort & wait(skew) & retry as a new transaction

                    my_tx.commit_time = now()
                    for each item I write
                        item.timestamp = my_tx.commit_time    # 这里有个问题，timestamp的更新和commit变可见，是不同步的

                    write journal to disk
                    my_tx.state = committed;
                    return to user with transaction succ
                    ```
                11. 类型9：当看到一个事件的timestamp，其真实时间可能是[timestsamp-skew, timestamp+skew]；Spanner采用在提交可见前等待skew的策略
                           Tx1会先完成所有修改并记录commit_time->等skew时间->使提交可见。如果tx2（有与tx1重合的读写item）开始于提交可见之后，那么必定tx2.start_time > tx1.commit_time
                           如果tx2开始于tx1提交可见之前，那么一定会因为重试，变成提交可见后开始执行，从而必定tx2.start_time > tx1.commit_time
                           下面的算法，可能大体上就是Spanner所采用的处理时钟skew的方法
                    ```
                    # transaction begin
                    create my_tx in transaction table

                    # subroutine to read
                    def sub_read(item)
                        atomic( if my_tx.start_time == null, then my_tx.start_time = now())
                        atomic(    # 如果上句到此句见，item.tx状态由committing变位了committed，那么start_time就稍有不准确；结果是可能误判稍多的transaction
                            if item.tx.state == committed
                                read item.update
                            if item.tx.state == committing    # 以保证发生在"等skew时间->使提交可见"之间transaction一定重试
                                abort & retry as a new transaction
                            else
                                read item.value
                        )

                    # subroutine to write & lock read
                    def sub_write_and_lock_read(item)
                        atomic ( if item.tx.state == committed, then item.value = item.update, item.timestamp = item.update_timestamp, item.tx = my_tx) else
                            atomic( 
                                if (item.tx == null || item.tx == aborted
                                        || (item.tx < committed && 抢断条件(item.tx)) )
                                    item.tx.state = abort
                                    item.tx = my_tx
                                else if (item.tx.state = committed)
                                    item.value = item.update
                                    item.timestamp = item.update_timestamp    # 此处也保证了，读timestamp时（只有committing阶段才需要读它）最新timestamp总是可见
                                    item.tx = null
                                    continue
                                else
                                    abort & retry as a new transaction
                            )
                        
                        if item need update
                            item.update = my_item_update 

                    # read in transaction
                    for each item needs read
                        sub_read(item)

                    # write & lock read in transaction
                    for each item needs update or read   # 需按顺序上锁以防死锁
                        sub_write_and_lock_read(item)

                    # transaction commit
                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # committing状态后，transaction不可抢断
                        abort & retry as a new transaction

                    for each item I read
                        if item.timestamp >= my_tx.start_time    # 已保证tx2.start_time > tx1.commit_time，所以能这么判断
                            abort & wait(skew) & retry as a new transaction

                    my_tx.commit_time = now()
                    for each item I write
                        item.update_timestamp = my_tx.commit_time    # 使用update_timestamp以使timestamp的更新不是立即可见

                    write journal to disk    # 如果crash重启，也得再等skew时间，以渡过时钟uncertain期

                    wait(skew)    # 使得提交后，至少经过skew时间，才变得可见；为了实现上述tx2.start_time > tx1.commit_time

                    my_tx.state = committed;
                    return to user with transaction succ
                    ```
                12. 类型10：和类型9完全一样，只是把commit前wait(skew)，变成了读之前wait(skew)，同样可以实现
                            如果tx2开始于tx1提交后，则一定有tx2.start_time > tx1.commit_time，即使clock有最大为skew的偏差
                            下面的算法，可能大体上就是CockroachDB所采用的处理时钟skew的方法
                    ```
                    # transaction begin
                    create my_tx in transaction table
                    wait(skew)    # 为了实现上述tx2.start_time > tx1.commit_time；不过此处应该先把item锁上，以清空[now()-skew, now()]时间段

                    # subroutine to read
                    def sub_read(item)
                        atomic( if my_tx.start_time == null, then my_tx.start_time = now())
                        atomic(
                            if item.tx.state == committed
                                read item.update
                            else
                                read item.value
                        )

                    # subroutine to write & lock read
                    def sub_write_and_lock_read(item)
                        atomic ( if item.tx.state == committed, then item.value = item.update, item.timestamp = item.update_timestamp, item.tx = my_tx) else
                            atomic( 
                                if (item.tx == null || item.tx == aborted
                                        || (item.tx < committed && 抢断条件(item.tx)) )
                                    item.tx.state = abort
                                    item.tx = my_tx
                                else if (item.tx.state = committed)
                                    item.value = item.update
                                    item.tx = null
                                    continue
                                else
                                    abort & retry as a new transaction
                            )
                        
                        if item need update
                            item.update = my_item_update 

                    # read in transaction
                    for each item needs read
                        sub_read(item)

                    # write & lock read in transaction
                    for each item needs update or read   # 需按顺序上锁以防死锁
                        sub_write_and_lock_read(item)

                    # transaction commit
                    atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # committing状态后，transaction不可抢断
                        abort & retry as a new transaction

                    for each item I read
                        if item.timestamp >= my_tx.start_time    # 已保证tx2.start_time > tx1.commit_time，所以能这么判断
                            abort & wait(skew) & retry as a new transaction

                    my_tx.commit_time = now()
                    for each item I write
                        item.timestamp = my_tx.commit_time

                    write journal to disk
                    my_tx.state = committed;
                    return to user with transaction succ
                    ```
                13. 类型11：这里我们使用完全不同的一种方式处理事务——timestamp ordering
                           给事务的读写分配它们该在什么时间执行的timestamp。通过合理地分配timestamp，保证事务的可序列化
                           我们假设所有获取的timestamp都是准确无误的，没有skew。
                           另外，原子操作/CAS可以使按timestamp执行的在一个item上的操作互相不会重叠
                    ```
                    item := {
                        value,
                        read_time,    # 该item上的所有read的最大timestamp（即最后什么时候读，不过这个read可能是计划在将来执行的）
                        write_time,    # 该item上的所有write的最大timestamp
                        commit_time,    # 该item上最后一次commit的timestamp
                        tx,    # 放着最后一次分派到item上write的transaction
                        update,
                    }

                    # transaction begin
                    create my_tx in transaction table

                    # subroutines to read
                    def schedule_read(item)
                        while (true)
                            read_time = max(now(), item.write_time, item.commit_time) + 1
                            atomic( if read_time > item.write_time && read_time > item.commit_time, then item.read_time = read_time) else
                                continue
                            break
                        schedule_read_at(item, read_time)
                        my_tx.first_read_time = min(my_tx.first_read_time, read_time)    # 记录第一次读的时间

                    def sub_read(item)
                         atomic(
                            if item.tx.state == committed
                                read item.update
                            else
                                read item.value
                        )

                    # subroutines to write
                    def schedule_write_and_lock_read(item)
                        while (true)
                            write_time = max(now(), item.read_time, item.write_time, item.commit_time) + 1
                            atomic(
                                if (write_time > item.read_time && write_time > item.write_time && write_time > item.commit_time)
                                    if ((item.tx == null || item.tx.state == abort
                                                || item.tx == my_tx)    # 为避免有别的事务的写插在了我的读和写之间，应重启
                                            && my_tx.first_read_time > item.commit_time)    # 不允许commit发生在事务的read和write之间
                                        item.tx = my_tx
                                        if item needs update
                                            item.write_time = write_time
                                    else if (item.tx < committing && 抢断条件(item.tx))    # 其实不推荐抢断；重启并重新schedule读写时间更便宜
                                        item.tx.state = abort
                                        continue
                                    else if (item.tx == committed)
                                        item.value = item.update
                                        item.tx = null
                                        continue
                                    else
                                        abort & retry as a new transaction
                                else
                                    continue
                            )
                            break
                        if item needs update
                            schedule_write_at(item, write_time)
                            my_tx.last_write_time = max(my_tx.last_write_time, write_time)    # 记录最后一次写的时间
                        
                    def sub_write(item)
                        /* 如果一个write已经被schedule了，那么它未来可能写了item.update，在将item.update放到item.value上的时候，又需要检查item.tx.state，然而item.tx可能已被后来schedule上去的tx write给替换。
                           事实上，上述情况永远不会发生。因为write的schedule，要求上一个write一定是commit或abort了，而commit的话就帮它item.value=item.update。也就是说，在上一个schedule上去的item实际执行完成并commit之前，或者abort之前，都无法schedule下一个write。注意schedule commit时并没有松开item.tx锁，只有commit完成才会。
                           一个更优雅的设计，大概是把item.tx分成item.last_schedule_write_tx和item.last_write_tx。之所以不这样做，是因为我希望整体算法和cockroachdb的更接近
                        */
                        atomic( if my_tx.state == in_process, then item.update = my_item_update)

                    # read in transaction
                    for each item needs read
                        sub_read(item)

                    # write & lock read in transaction
                    for each item needs update or read   # 需按顺序上锁以防死锁
                        sub_write_and_lock_read(item)
                        
                    # transaction commit
                    def schedule_commit()    # only after all writes & read locks are successfully scheduled
                        for each item I read
                            if item.commit_time >= my_tx.first_read_time
                                abort & retry as a new transaction
                        for each item I read or update
                            commit_time = max(commit_time, now(), item.write_time, item.commit_time)
                        for each item I write
                            atomic( if item.commit_time < commit_time, then item.commit_time = commit_time)
                        schedule_commit_at(commit_time)

                    def commit()
                        atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # committing状态后，transaction不可抢断
                            abort & retry as a new transaction

                        write journal to disk
                        my_tx.state = committed
                        return to user with transaction succ 
                    ```
                    加上item.commit_time纯粹是为了避免tx2的read发生在tx1的write和commit之间
                    其实，如果把item.update保存在tx各自的私有空间，就不再需要item.tx加锁，从而只需要留下item.read_time，item.commit_time即可；write在提交前完全不会互相影响；也不再需要抢断机制了。
                14. 类型12: 从类型11继续，为了是其更接近cockroachdb的样子，我们把Timestamp Ordering和不schedule直接读写的方式混和，即
                            先尝试直接读写，如果不行，则schedule到合适的timestamp。注意此似乎clock还是被认为是完全精确的。
                    ```
                    item := {
                        value,
                        read_time,    # 该item上的所有read的最大timestamp（即最后什么时候读，不过这个read可能是计划在将来执行的）
                        write_time,    # 该item上的所有write的最大timestamp
                        commit_time,    # 该item上最后一次commit的timestamp
                        tx,    # 放着最后一次分派到item上write的transaction
                        update,
                    }

                    # transaction begin
                    create my_tx in transaction table

                    # subroutines to read
                    def try_sub_read(item)
                        read_time = now()
                        atomic(
                            if item.tx == null || item.tx.state == abort
                                read item.value
                            else if item.tx.state == committed
                                read item.update
                        ) else
                            schedule_read(item)
                            return
                        
                        my_tx.first_read_time = min(my_tx.first_read_time, read_time)
                        atomic( if read_time > item.read_time, then item.read_time = read_time)

                    def schedule_read(item)
                        while (true)
                            read_time = max(now(), item.write_time, item.commit_time) + 1
                            atomic( if read_time > item.write_time && read_time > item.commit_time, then item.read_time = read_time) else
                                continue
                            break
                        schedule_read_at(item, read_time)
                        my_tx.first_read_time = min(my_tx.first_read_time, read_time)    # 记录第一次读的时间

                    def sub_read(item)
                         atomic(
                            if item.tx.state == committed
                                read item.update
                            else
                                read item.value
                        )

                    # subroutines to write
                    def try_schedule_write_and_lock_read(item)
                        write_time = now()
                        atomic(
                            if ((item.tx == null || item.tx.state == abort
                                        || item.tx == my_tx)
                                    && my_tx.first_read_time > item.commit_time)
                                item.tx = my_tx
                            else if (item.tx < committing && 抢断条件(item.tx))
                                item.tx.state = abort
                                item.tx = my_tx
                            else if (item.tx == committed)
                                item.value = item.update
                                item.tx = my_tx
                                continue
                        ) else
                            /* 上文已分析过，schedule write只有在上一个write tx执行完毕提交或abort时，才能成功
                               那么，干脆把它与write的实际执行合并
                            */
                            schedule_at(
                                try_schedule_write_and_lock_read,
                                max(now(), item.read_time, item.write_time, item.commit_time) + 1
                            )
                            return
                        
                        write_time = now()
                        if item needs update
                            item.update = my_item_value
                            my_tx.last_write_time = max(my_tx.last_write_time, write_time)
                            atomic(write_time > item.write_time, then item.write_time = write_time)

                    # read in transaction
                    for each item needs read
                        try_sub_read(item)

                    # write & lock read in transaction
                    for each item needs update or read   # 需按顺序上锁以防死锁
                        try_sub_write_and_lock_read(item)
                        
                    # transaction commit
                    def schedule_commit()    # only after all writes & read locks are successfully scheduled
                        for each item I read
                            if item.commit_time >= my_tx.first_read_time
                                abort & retry as a new transaction
                        for each item I read or update
                            commit_time = max(commit_time, now(), item.write_time, item.commit_time)    # 因为item.tx锁的缘故，十有八九commit会被立即执行
                        for each item I write
                            atomic( if item.commit_time < commit_time, then item.commit_time = commit_time)
                        schedule_commit_at(commit_time)

                    def commit()
                        atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # committing状态后，transaction不可抢断
                            abort & retry as a new transaction

                        write journal to disk
                        my_tx.state = committed
                        return to user with transaction succ 
                    ```
                15. 类型13：继续从类型12开始，为了更接近cockroachdb，我们认为clock有最大skew的偏差，真是事件发生在[timestamp-skew, timestamp+skew]内。
                            为了处理这种skew，读被约束为一定发生在commit之后至少skew时间后。如果是Spanner，则应该是commit前多等待skew。
                            https://www.cockroachlabs.com/blog/living-without-atomic-clocks/
                    ```
                    item := {
                        value,
                        read_time,    # 该item上的所有read的最大timestamp（即最后什么时候读，不过这个read可能是计划在将来执行的）
                        write_time,    # 该item上的所有write的最大timestamp
                        commit_time,    # 该item上最后一次commit的timestamp
                        tx,    # 放着最后一次分派到item上write的transaction
                        update,
                    }

                    # transaction begin
                    create my_tx in transaction table

                    # subroutines to read
                    def try_sub_read(item)
                        read_time = now()
                        atomic(
                            if read_time > item.commit_time + skew && read_time > item.write_time + skew    # read总是要开始于commit之后至少skew
                                if item.tx == null || item.tx.state == abort
                                    read item.value
                                else if item.tx.state == committed
                                    read item.update
                        ) else
                            schedule_read(item)
                            return
                        
                        my_tx.first_read_time = min(my_tx.first_read_time, read_time)
                        atomic( if read_time > item.read_time, then item.read_time = read_time )

                    def schedule_read(item)
                        while (true)
                            read_time = max(now(), item.write_time + skew, item.commit_time + skew) + 1    # read总是要开始于commit之后至少skew时间，以实现tx2.start_time > tx1.commit_time约束
                            atomic( if read_time > item.write_time && read_time > item.commit_time, then item.read_time = read_time) else
                                continue
                            break
                        schedule_read_at(item, read_time)
                        my_tx.first_read_time = min(my_tx.first_read_time, read_time)    # 记录第一次读的时间

                    def sub_read(item)
                         atomic(
                            if item.tx.state == committed
                                read item.update
                            else
                                read item.value
                        )

                    # subroutines to write
                    def try_schedule_write_and_lock_read(item)
                        write_time = now()
                        atomic(
                            if ((item.tx == null || item.tx.state == abort
                                        || item.tx == my_tx)
                                    && my_tx.first_read_time > item.commit_time)
                                item.tx = my_tx
                            else if (item.tx < committing && 抢断条件(item.tx))
                                item.tx.state = abort
                                item.tx = my_tx
                            else if (item.tx == committed)
                                item.value = item.update
                                item.tx = my_tx
                                continue
                        ) else
                            /* 上文已分析过，schedule write只有在上一个write tx执行完毕提交或abort时，才能成功
                               那么，干脆把它与write的实际执行合并
                            */
                            schedule_at(
                                try_schedule_write_and_lock_read,
                                max(now(), item.read_time, item.write_time, item.commit_time) + 1
                            )
                            return
                        
                        write_time = now()
                        if item needs update
                            item.update = my_item_value
                            my_tx.last_write_time = max(my_tx.last_write_time, write_time)
                            atomic(write_time > item.write_time, then item.write_time = write_time)

                    # read in transaction
                    for each item needs read
                        try_sub_read(item)

                    # write & lock read in transaction
                    for each item needs update or read   # 需按顺序上锁以防死锁
                        try_sub_write_and_lock_read(item)
                        
                    # transaction commit
                    def schedule_commit()    # only after all writes & read locks are successfully scheduled
                        for each item I read
                            if item.commit_time >= my_tx.first_read_time
                                abort & retry as a new transaction
                        for each item I read or update
                            commit_time = max(commit_time, now(), item.write_time, item.commit_time, item.read_time)    # 这里加上item.read_time以保证read总是发生在commit+skew之后，或一定被restart
                        for each item I write
                            atomic( if item.commit_time < commit_time, then item.commit_time = commit_time)
                        schedule_commit_at(commit_time)

                    def commit()
                        atomic ( if my_tx.state = in_process, then my_tx.state = committing ) else    # committing状态后，transaction不可抢断
                            abort & retry as a new transaction

                        write journal to disk
                        
                        # 如果是仿照Spanner，那应该是commit可见前，等待skew，以使tx2.start_time > tx1.commit_time
                        # 不过要注意，commit_time在提交前已经是可见的
                        # 并且read看committing状态需要abort，以保证等待skew->commit可见期间不穿插新transaction
                        # wait(skew)
                        
                        my_tx.state = committed
                        return to user with transaction succ 
                    ```
                    但和cockroachdb比较，HLC时钟在这里有什么用呢？估计是为了实现consistent的snapshot cut，为了SSI，大概。
```