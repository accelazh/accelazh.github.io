---
layout: post
title: "Multi-paxos, Raft, Multi-Raft, Parallel Raft"
tagline : "Multi-paxos, Raft, Multi-Raft, Parallel Raft"
description: "Multi-paxos, Raft, Multi-Raft, Parallel Raft"
category: "Storage"
tags: [storage, paxos, consensus]
---
{% include JB/setup %}

Recent years emerging database products are coining new names for Paxos. Here to summarize the clarification

```
1. Multi-paxos: referred in OceanBase
   https://zhuanlan.zhihu.com/p/25664121
   http://oceanbase.org.cn/?p=111
    1. similar with Raft, both selects a Leader and only Leader can propose (Leader paxos)
    2. compared to Raft, multi-paxos allows holes in log entries, even new leader also allow holes
       while Raft makes sure no holes in the log entries
       as a result, multi-raft is more complex but more flexible for log/data replication
       the log entries must NOT require logs to be sequentially replayed. E.g. metadata replication usually not suitable
    3. Note, "Multi-paxos" is also a concept in common literature, e.g. in https://www.jianshu.com/p/b187abbb0fcb
        1. Compared with OceanBase's, both "Multi-paxos" pick a leader to simplify paxos rounds
        2. But OceanBase's "Multi-paxos" emphases allowing holes in the logs, while common literature "Multi-paxos" did't say about that.

2. Multi-Raft: coined in TiDB
   http://www.vldb.org/pvldb/vol13/p3072-huang.pdf
   https://tikv.org/deep-dive/scalability/multi-raft/
    1. TiDB and CockroachDB use Raft for data/log replication, compared to the traditional 3-way replication
    2. Multi-raft means, each partition (or region) forms an independent raft quorum (a replication set / a raft group).
       so overall in the cluster, there are many raft quorums working in parallel

3. Parallel Raft: coined in PolarFS
   https://www.vldb.org/pvldb/vol11/p1849-cao.pdf
   https://www.zhihu.com/question/278984902
    1. compared to Raft, Parallel Raft allows out-of-order log replication.
       i.e. to allow holes in the log entries of leader and followers
       that is to say, Parallel Raft is the Raft version of Multi-paxos
    2. Allowing holes is suitable for data replication or DB log replication
```

Comparing Paxos with 3-replica. Raft and 3-way replication are both widely used for data replication

```
1. Ack when 2 out 3 replica commits. Raft supports it naturally. 3-way replication needs customization.
2. Node failure and replace. Raft ring carries out membership change by itself. 3-way replication needs an external metadata ring (usually Paxos too) to replace node.
```
