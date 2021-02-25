---
layout: post
title: "Searching and Evaluating EC Schemas"
tagline : "Searching and Evaluating EC Schemas"
description: "Searching and Evaluating EC Schemas"
category: "erasure-coding"
tags: [storage, erasure-coding, reliability]
---
{% include JB/setup %}

To design / evaluate / find optimal EC schema design, the general approach

### Understand the problem

Looking for a faster EC schema? To reduce tail latency? To save capacity? To improve throughput? Better reliability? Etc

Understand the scope and scenario: Cluster rack domain setup and placement constraints. Failure patterns, blast radius. Hardware replacement and software upgrading needs. Reconstruct read patterns and traffic volume. Data hot/cold temperature. Old existing EC data migration needs. Etc

Usually, the baseline is to compare with 3-replica.

### Different EC schema variations

How many instanecs per fragment has? Any local groups, or even overlaping groups? Code fragments all need to be replicated, long/short schema transition? Zone related support? Transition states and speed? SSD or HDD? Read patterns?

The basic EC schema is M fragments + N parities. 3-replica can also be seen as a 1 + 2 schema. But, more variations

  * EC can happen within a data object, across data objects, or even across datacenters

  * Replication unit can be a fragment instance, data ranges in fragment instance (e.g. only which are hot). And data ranges from different EC groups can form one same replica. I.e. __Caching__ hot instances in SSD/memory

  * Given data hot/cold, they can do different replication or schema policy.

  * The replica instances can be on different medias, migrated to some places. I.e. __Tiering__ HDD + SSD

  * The schema can determine to drop less important fragment instances or entire fragments, become __long or short__, given capacity needs, or for less important data types, and transition needs.

  * __Heterogenous instances__. Fragment instances & their replicas can be in different format, e.g. row-format OLTP vs columnar-format OLAP (TiDB TiFlash). (Also different media, count, placement, etc.)

  * The synchronization __quorum__ of different replicas can be different, e.g. plain replication, raft/paxos replication, private offloading to public cloud, eventual consistency, memory caching + dedup, witness nodes for tail latency, Dynamo read N+1 out of 2N+1, etc.

  * __Stripping__ layout can be different. Fragment hosts consecutive blocks, or blocks stripped to different fragments. Code parity can be plain mapping to data fragments, or with some stripping/translating strategies.

  * Replica / replication may not be simple copy. It can also have mapping / aggregating / stripping strategies.

In summary

  * Decouples the replica instances vs storing format, vs cold and hot, or different business needs

  * Decouples the replica instance counts, schema length, etc

  * Decouples the replica instance source and data size, from single object or many or across geo.

  * Managing the transition of different EC schemas. And we need good abstractions.

### Evaluating performance

Performance, Repliability, Storage overhead are a triangle to find optimal and to trade off.

__IO Amplification__

Compared to 3-replica, reconstruct reads amplify read IO count. Datacenter level IO amplification affects latency distribution.  Reconstruct reads usually come from reads fallback due to tail latency, upgrade temporary node unavailable, node/rack failures, throughput filled up / node busy, cluster-wide load saturation, aggressive repair traffic, etc.

There are two parts of amplification: IO count amplification, throughput amplication. Also, disk and network amplication can be of different patterns. CPU can also be stressed upon heavy requests. And IO count amplification can cause queue delays related to threading and throttling.

Besides reconstruct reads, initial EC needs extra traffic to do calculation and place fragment instances. Data repair needs more traffic than 3-replica. Append-only system do rewrite data, if off-line EC here, extra again new initial EC needed for rewritten data. Customer may also frequently create short-lived data to stress the EC amplification.

__Top throughput & under stress behavior__

Compared to 3-replica, which supports 3x max read throughput, EC fragments supports only 1x + 1 reconstruct read throughput, given there is no multiple instances per fragment. Secondly, 3-replica can balance read queue across replicas, to do tail reduction. EC fragments are harder due to less replicas.

This can result in lower top throughput per single data range supported reads, and higher tail latency. But note that compared to 3-replica, fragments do split reads to different ranges to different nodes. Besides, reads cross fragment boundary generates more IO count, which may raise cluster-wide IO stress.

Besides single object stress, cluster-wide under stress may worsen tail latency 3-replica vs EC fragments, and may also combine with reconstruct reads snow avalanche.

__Reconstruct behavior__

LRC EC schemas support local reconstruct vs global reconstruct. This helps reconstruct with less fragments thus improve tail latency. But this EC shema is not MDS anymore. It reduces "rebuild cost", but raises storage overhead given same reliability level; or call it less reliability if to maintain same storage overhead level.

__Degraded latency__

Scenarios that involves massive reconstruct reads, snow avalanche pattern. E.g. a rack is down for upgrade, a zone is down. Scope and scenarios, including both functional ones and failure scenario ones should be thoroughly included to evaluate.

Besides, cluster-wide or single node heavy reconstruct reads can also burst node memory usage, causing OOMs, or burst metadata memory usage, causing wider failure storm propagation. Verify under-stress behaviors.

__Tail latency reduction__

E.g. Reonstruct need 9 fragment but actually sent out 10 reads. Plain reads, second-instance reads, reconstruct reads, local vs global switching; and all them going in parallel with coordination of fallback timers. Latency is a distribution, tail at Q99 or more can be reduced by many techniques; 1% is many users' experiences.

But be sure the timer, deadline, shortcut cancellation, load estimation and balancing, etc are well working. Otherwise the extra reads above easily become a DDOS to data nodes and even create more failure avalanche, and more retries and more reads and then more failures .. Failure scenarios and actual gains should be tested. Bad cases should have cap throttling.

__Read scheduling__

Read a fragment instance, read another fragment instance, read fragment instance + extra 3-replica instance, fallback to local reconstruct read, fallback to global reconstruct read. Timeouts and load balancing, etc. Prefetching, data caching, metadata caching, freshness, etc. The policies and timer settings matter, and they need to be tuned, given different hardware setup, and tested

Besides, Data node caching, local SSD caching, may require to favor one reading instance rather than scatter to all instances. So that local caching can be maximally hit.

__Modeling and simulation__

Latency is a probability distribution. Use math probability model we can deduce performance, tail latency, and different tail reduction strategies.

Simulation builds by programing. It requires less math skills, and may given more reliable results. It may be the only way for very complex scenarios. It should build atop live production trace and distributions.

Too many production clusters can be categorized with ML clustering techniques, equivalenet class techniques, using representative proxy to simplify too many data points or dimensions.


### Evaluating reliability

__Concepts__

Recoverability: At each fragment loss count, ratio of combinations that are recoverable. This is static per EC schema irrelevant to node failure probability.

Reliability MTTDL: Probability walkthrough along failure, repair, exposure state changes. It's MTTL of Markov State Model; EC schema during repeated failure & repair till data unavailable or data un-durable.

Availability vs Durability: Node down causes data unavailable, but data are still intact on disk. Bad disks beyond repair causes data both unavailable and unable to recover even offline. The former one says availability, the later one says durability. Availability usually relates to TOR and node failure probability, and durability usually relates to disk failure probabiilty.

Single ECed object blast failure availability: Consider a single ECed object. Failure happens in burst short time to its fragments, no repair involved. Node faiulure have their probability. Here to answer its survive probability. Usually using math formula `Sum(C(N,K)*p^k(1-p)^(N-k)*Recoverability)`. Note the better/worse of this formula can flip reverse in different scale of node failure probability p.

Datacenter data unavailable (DU) probability: Given a datacenter has millions of data objects, what's the probability that we have DU happen. For simple, it's multiplying of per data object DU probability * data object count. The metric points to how frequent we will be involved in operation data recovery effort.

Coding matrix: Given the same EC schema, we need to search for the optimal coding matrix, i.e. a matrix of galois field numbers. They must satisfy all linear independence constraints to achieve the declared EC schema recoverability. The matrix better have all 1 rows, and overall has less 1 bits, to reduce encoding/decoding computation cost.  The matrix is harder to search for longer EC schemas. But using larger galois fields (increased encoding/decoding cost) can search easier.

__Implementation related__

EC schema placement: Placing fragments in isolated failure domains, and handle placement balancing and migration well; this improve the actual reliability after EC schema is deployed. But finding a proper placement is usually coupled with datacenter layout variations, and selecting a suitable EC schema long/short too.  We also need to ensure placement can work in upgrading / rack failure cases, or a longterm zone down.

Repair action scheduling: Timely and efficeint data repair, with optimal prioritization, can improve the runtime reliability and the EC schema. It needs to work with datacenter bandwidth planning, and also upgrading (node unavailable) needs. Different strategies also worth compare: read live data and then reconstruct a single fragment in one run, read live data and then reconstruct multiple failed fragments in one run, reconstruct 3-replica instance first, reconstruct to SSD caching, etc.  Repairing may work on multiple fragments in parallel, make sure their placement won't race.

__Modeling and simulation__

Math modeling: where all the above metrics can be calculated. It can use simple data sheets containing formulas, or a program to do MTTL matrix solving.

Iterative simulation: simulate day to day datacenter node failres and repair. The data center is filled with ECed objets. See how the data availability reacts. The model can input with production live traces (obtained from paper/publications).

Optimal EC schema searching: combine all the auto tools, may employ Machine Learning, or Gene, or other searching algorithms.


### Storage overhead

How much used capacity the EC schema can save, and this is usually traded off with Performance and Reliability characteristics. The design should also consider extra capacity used in transition states, data repairing, longterm rack/zone failures. And how fast the used capacity can be gained back, given temporary capacity bursts.

Not all data objects have time to finish EC. They may be too short-lived, quickly deleted or got rewritten. The overall EC percentage relates to data scheduling and how much bandwidth available to use set aside from higher priority user traffic.

A common knowledge, Reed-Solomon code MDS (i.e. plain M+N EC schema) already achieves the best recoverability given the same stoarge overhead level. But in actual design, we usually trade off and combine into more various needs.
