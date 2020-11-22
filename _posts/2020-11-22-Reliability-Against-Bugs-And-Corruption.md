---
layout: post
title: "Reliability against Bugs and Corruption"
tagline : "Reliability against Bugs and Corruption"
description: "Reliability against Bugs and Corruption"
category: "storage"
tags: [storage, reliability, bug]
---
{% include JB/setup %}

Previously I wrote about data reliability in storage systems [[1]](/storage/Engineering-Reliability-Practices) [[2]](/storage/Storage-Reliability-Calculations) [[3]](/storage/Experience-In-Feature-Development-And-Rollout-Cycle). The main theme is to use replications (including erasure coding) to work against bad disks, node failures, disk corruptions, memory corruptions. However, replication is not as effective against bugs. Especially, bug corruption can be replicated, quickly, and compromise all replicas.

First, some typical __failure patterns__:

  * A programming bug that didn't write the persistent data right, and then that corrupted data block propagates to all relicas. Now customer reads cannot restore the original data.  The bug can be rare to happen, but does trigger when you have large amount of machines running on full variety of usecases.

  * Similarly, the bug can also happen on metadata.  E.g. During upgrade some messages got replayed but with incorrect old/new version format, and then the corrupted metadata quickly propagates through Paxos replication. Even the persistent data is healthy, the metadata corruption prevents them reading or repairing. And since metadata size is usually small and the processing is fast, the compromised area can grow quickly.

  * Data can be incorrectly deleted due to programming bugs. Deleting data quickly is a common usecase, where the storage system is append-only and ingesting fast with capacity reacing limit, especially on SSD clusters. However, if a bug incorrectly deleted customer data, all replicas can already be lost when the bug is finally discovered. What's worse, deleted data is even harder to recover than corrupted data, because filesystem may already overwrites them.

    * A delete decision typically involves 1) Seeing all replicas healthy and enough number of them; 2) Issuing deletes on excessive replicas.  However, they can break at 1) "seeing" is stale where true data already lost/deleted, and metadata can be cached but stale; 2) deletion request messages can be replayed; 3) data nodes can first tell you they have data, and next second executes deletes, now data gone; be careful with race conditions.

  * Sometime we also met bad hardware nodes that randomly calculate wrong results in memory (e.g. detected by CRC), and may or may not be catched by asserts. If not careful, i.e. the protection chain-of-trust has gaps or call it bugs, such corruption can go into persistent data or metadata. It recalls me of cosmic ray impacting hardare correctness.

We need a new systematic methodology for reliability against bugs. I think this is still an open industrial gap.

First, let's name __some small design tips__:

  * Metadata is critical for data reliability.  Store the metadata twice at two different places, in different format, and managed in separated flow.  E.g. The metadata about a file is stored at metadata servers, and also attached to the data files at data servers. A typical bug can corrupted all metadata replicas at metadata servers, but then it'll be lucky to recover from data server copies. Metadata at the two places are managed separatedly, so less likely to compromise by same bug.

  * Storage systems typically do data scrubbing to detect silent data corruption. This should also be designed to detect any corruption due to bugs, e.g. with end-to-end CRCs. Besides, make sure all necessary data and metadata are included in scrubbing, e.g. periodical compare those stored at metadata server and those on data nodes.

  * Incremental algorithms are usually clever, but full volume scan is still necessary. A bug can drift away incremental results unnoticed. Full volume scan can be less frequent, but necessary to detect such drift. E.g. Scan and compare all data between data nodes, v.s. the metadata tracked at metadata server.  The idea remotely resembles the CRC-verifiy-every-step (incremental) vs end-to-end CRC paradigm (end-to-end).

  * Make sure the delete decisions, typically scheduled by metadata server, is on linearizability algorithms. So that, it won't see a stale view and issue incorrect deletes.  A simple method is, only the writer can do read-decide-delete. And the writer should not trust metadata reported by someone else except the owner (i.e. to avoid cached metadata).

  * Storage systems typically manage data repairing against expected disk/node failures. Make sure if some data repair gets stuck, which implies potential bugs being hit, it gets alerted and checked.  To cope with stuck data repair, it may retry on *randomly* selected different nodes, where saying random here is to avoid unexpected bug pattern.
  
  * Code can be designed and implemented with more defensive thinking. And it can place sanity checks, alerts, asserts wisely. Checkings can be placed at each different layer, tooling, switch on/off, metadata server, data nodes. Related alerts printed should be captured and notify operation in first time.  Sanity checkings, e.g. on the replica count management, where if went wrong it can easily impact durability; e.g. detect suspicious deletion actions violating durability constraints.

Besides coding time, some protections can be added at __testing__ and __runtime__. E.g. Chaos Engineering, besides node failures

  * Let some nodes simulate the "corrupted guy", and the system should be able to protect itself against it. E.g. the node may randomly inject memory corruptions, or to write to disk flipped bits, or to send intentionally corrupted results to other nodes.

  * Simulate message delay and replay for deletion staleness. Try trigger some race conditions too in deletion process.

  * Sanity checks, alerts, asserts wisely. And monitoring & alerting timely. Defensive thinking, and wisely.

Now, more advanced topics. First, it's the __end-to-end (end2end, e2e) verification methodology__. The underlying thoughts are, even if the feature is totally implemented wrong and with bugs everywhere, end-to-end methods still detect the bug. Some examples:

  * The typical example is end-to-end checksum. The checksum is usually calculated at customer side or client side, and then passed through every layer and then persisted along with every data blocks.  Even the replication or erasure coding features are totally implemented wrong, end-to-end CRC can still detect the bug.

  * End-to-end methodology can be used in wider scope. E.g. SQL databases may use it to verify indexes match the actual data, independent with how the indexing algorithms are designed.

  * On erasure coding, the core ability to verify, is that the code parities can actually do reconstruct reads and data rebuilds as it declares, against different failure patterns and data contents in real production. Call it the "recoverability". The "recoverability" actually has no relation with how erasure coding feature is implemented; it's just the relation of bits. There are methods to end-to-end verify them too.

Compared to end-to-end verification, we can name the __chain-of-trust verification__ concept. In typical verification, every step of data transform needs to be verified, e.g. memory copy, message sending, writing to disk, transforming to other formats, calculating dependent results, etc.  Memory corruption is not uncommon to see on massive production scale.

  * A typical example is CRC is carried and verified at every step, carried with every data block. Bigger units also need CRC, because even per block is correct, blocks may come in wrong order. The step-by-step verification composes the chain-of-trust.

  * In the chain-of-trust, the root source must be carefully dealt with. Usually the root source is OK from direct customer.  However, A node may restart and resume work, where the root source implicitly becomes the remembered progress. The "remembered" thing in memory or disk can already be corrupted; it needs verify before resume.

  * The operation on CRC also needs to be verified. This is because CRC will usually be memorized in data blocks and metadata, as the source to determine whether the data is "correct". If the CRC is memorized wrong, it breaks data health management.  Failure patterns can be, CRC is copied in memory but bit flip, CRC is written to disk but bit flip, CRC can be concatenated or resued (to calcuate CRC on longer data) but yields an incorrect result.  Typical solutions can be, compute twice and compare, wait on disk scrubbing done before declare finish healthily.

Next, it brings me to think several different paradigms to maintain the chain-of-trust. By far, we can see a good verification method composes of 1) verify end-to-end, 2) implemented heterogeneously, 3) computational light. Let's coin the concept __heterogeneous end-to-end verification__.

  * Paradigm 1: CRC to verify data is identical. Or CRC to verify multiple pieces of data having certain relations, where the CRC here is more like a purposed content hash.  The CRC is the basic here.

  * Paradigm 2: Compute twice. Image there is a long chain of data transform, compute twice and compare results. Identical results implies trust worthy.  But if the compute algorithm is implemented with bugs, compute twice wrongs twice.  This is an end-to-end verification, but not heterogeneously implemented, and not computational light.

  * Paradigm 3: Instead of compute twice, verify at each step of the chain, i.e. the chain-of-trust. It's of lighter computational overhead, but not end-to-end. It's vulnerable if a single step, or the root source of trust chain, is corrupted by a bug.

  * Paradigm 4: Practical end-to-end verifications, e.g. end-to-end CRC.  It did compute twice, first it's the data itself, second it's the end-to-end verification part. The end-to-end verification part is usually computational light, and so implies implemented heterogeneously. The heterogeneousity ensures the two paths are less likely to hit the same bug. And if both paths have bugs, verification results are still less likely to match.  Besides, there is no chain here, so not vulnerable to bugs breaking a step in chain.  However, end-to-end methods need to be designed case by case, and may or may not exist.

So far here ..
