---
layout: post
title: "Tail Latency Study"
tagline : "Tail Latency Study"
description: "Tail Latency Study"
category: "Storage"
tags: [storage, latency, cloud]
---
{% include JB/setup %}

Latency in real production is a (probability) distribution, practically described as percentiles. The latency can double at 75% percentile, and ridiculously 100x higher after 99%. 1% is a large portion of users for cloud services, and they get hurt every day. Slow operations, even transient, can cause customer VMs to restart (because OS write stalls), and online services to restart. [Performance availability](http://www.36dsj.com/archives/42599) is becoming another public cloud key factor besides plain accessible availability.

__What contributes to tail latency?__

  * Disk just get slowdown time to time for no reason. [The Tail at Store](https://www.usenix.org/conference/fast16/technical-sessions/presentation/hao) gives more in-depth analysis. Also, disks may degrade significantly when they get old.
  
  * Timeouts. Failure tolerance and retry is a common design pattern in distributed systems. But one retry is enough to send current request to latency tail. [Google SRE Book](http://shop.oreilly.com/product/0636920041528.do) chapter 21 to 22 discuss it in detail, such as,
    
      * Reduce remaining timeout quota and pass it down each layer of the request processing chain.
    
      * Be aware of the chained retry amplification (layer1 3 retries, layer2 3*3 retries, ...).

  * Background tasks. Almost every services, from software to even hardware/firmware, have backgroud tasks. Background task may temporarily slowdown the world. The most notorious one is GC (garbage collection).

  * Overload. The customer may be sending you too many/big requests, and upper layer throttling is not working well. Overprovisioned customer VMs may compete with each other resulting slow experience. Some small piece of data may be extremly hot, e.g. many OS images are forked from a small shared base. A large request may be pegging your CPU/network/disk, and make the others queuing up. Or something went wrong, as a dead loop stuck your cpu.

__Mitigating the tail latency__

The latency percentile has low, middle, and tail parts. [Controlling latency](http://474.cmpt.sfu.ca/public/Week4-Fri.html) has a good summary

  * To reduce the low, middle parts: Provisioning more resources, cut and parallelize the tasks, eliminate "head-of-line" blocking, and caching will help.

      * This is the common techniques that we apply for scale-out distributed systems.

  * To reduce the tail latency: The basic idea is hedging. Even we've parallelized the service, the slowest instance will determine when our request is done. You can use probability math to model the combined latency distribution.
    
      * Send more requests than necessary and only collect the fastest returned, helps reduce the tail. Send 2 instread of 1. Send 11 instead of 10 (e.g. in erasure-coding 10 fragment reconstruct read). Send backup requests at 95% percentile latency.
    
      * Canary request, i.e. send normal requests but fallback to sending hedged requests if the canary did't finish in reasonable time.
    
      * Usually, smaller task partitions (micro-partition) will help achieve smoother latency distribution percentiles.

      * Reducing head-of-line blocking. A small number of expensive queries may add up latencies to a large number of concurrent cheaper queries. Uniformly smaller tasks partitioning camn help.

      * To deal with timeout

          * Try a non-block try read at first (read but do not wait), then follow it by a best-effort read (read and wail till timeout).

          * When a timeout is found, mark related resource as known slow. Tell others to walk around it, and immediately timeout all pendings on it.

          * To set a proper timeout value, we can use the 99.9% percentile, and adjust it dynamically. Arbitrary timeout value can be harmful.

      * More fine-grained scheduling and even a management framework to balance latency and cost. (e.g. [Bing's Kwiken](http://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p219.pdf), also attached below.)

The famous [The Tail at Scale](http://web.stanford.edu/class/cs240/readings/tail-at-scale.pdf) from Google give more fine-grained techniques. More discussion around it: [\[1\]](http://research.google.com/people/jeff/latency.html)[\[2\]](http://highscalability.com/blog/2012/3/12/google-taming-the-long-latency-tail-when-more-machines-equal.html)[\[3\]](http://highscalability.com/blog/2011/2/1/google-strategy-tree-distribution-of-requests-and-responses.html)[\[4\]](http://highscalability.com/blog/2012/6/18/google-on-latency-tolerant-systems-making-a-predictable-whol.html)[\[5\]](http://www.bailis.org/blog/doing-redundant-work-to-speed-up-distributed-queries/)[\[6\]](http://static.googleusercontent.com/external_content/untrusted_dlcp/research.google.com/en/us/people/jeff/Stanford-DL-Nov-2010.pdf)[\[video\]](https://www.youtube.com/watch?v=modXC5IWTJI)[\[7\]](http://www.evanjones.ca/retries-considered-harmful.html)[\[8\]](http://research.google.com/people/jeff/latency.html)[\[9\]](https://news.ycombinator.com/item?id=5215884). Reading notes attached below

```
1. Google Jeff Dean's "the tail at scale" paper    [2013, 345 refs]
   https://web.stanford.edu/class/cs240/readings/tail-at-scale.pdf
   https://blog.acolyer.org/2015/01/15/the-tail-at-scale/
   https://plus.google.com/+JeffDean/posts/fRBupzPMREg
    1. good classic paper. read and logged before.
    2. realted materials
        0. Controlling latency: Basic approaches to reducing latency variability
           http://474.cmpt.sfu.ca/public/Week4-Fri.html
            1. read and logged before
        1. Google: Taming The Long Latency Tail - When More Machines Equals Worse Results    [Mar 12, 2012]
           http://highscalability.com/blog/2012/3/12/google-taming-the-long-latency-tail-when-more-machines-equal.html
            1. to reduce latency
                1. Tree Of Distribution Responses
                2. Focus On The 99%
                3. Latency Tied To Blocking Rather Then Queueing
                    1. head-of-line blocking
        2. Google Strategy: Tree Distribution Of Requests And Responses
           http://highscalability.com/blog/2011/2/1/google-strategy-tree-distribution-of-requests-and-responses.html
            1. the problems
                1. The CPU becomes a bottleneck, for either processing requests or sending replies, because it can't possibly deal with the flood of requests.
                2. The network interface becomes a bottleneck because a wide fan-in causes TCP drops and retransmissions, which causes latency.
                   Then clients start retrying requests which quickly causes a spiral of death in an undisciplined system
            2. Instead of having a root node connected to leaves in a flat topology, the idea is to create a tree of nodes.
                So a root node talks to a number of parent nodes
                and the parent nodes talk to a number of leaf nodes.
                Requests are pushed down the tree through the parents and only hit a subset of the leaf nodes.
                    1. can also co-locate parents on same rack as leaves
                    2. it's like NetAgg middlebox
                       https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/mai14netagg.pdf
            3. benefits
                1. Fan-in at each level of the tree is manageable
                2. Response filtering and data reduction (by parent)
                3. Collocation
            4. my questions
                1. the hops are increased, and some data are reduently sent-received multiple times? what it costs?
        3. Google On Latency Tolerant Systems: Making A Predictable Whole Out Of Unpredictable Parts    [June 18, 2012]
           http://highscalability.com/blog/2012/6/18/google-on-latency-tolerant-systems-making-a-predictable-whol.html
            1. Large fanout architectures are easy to suffer from tail latency
            2. Fault Tolerant Vs Latency Tolerant Systems
            3. to manage latency
                1. Prioritize request queues and network traffic
                2. Reduce head-of-line blocking
                3. Rate limit activity
                4. Defer expensive activity until load is lower
                5. Synchronize disruptions
            4. Cross Request Adaptation Strategies
               the idea is to examine recent behavior and take action to improve latency of future requests within tens of seconds or minutes
                1. Fine-grained dynamic partitioning
                2. Load balancing
                3. Selective partitioning
                4. Latency-induced probation
            5. Within-Request Adaptation Strategies
                1. Canary requests
                2. Backup requests with cross-server cancellation
                    1. use the fastest one, cancel the other requests
                3. Tainted results
                    1. drop out noncritical subcomponents, as tradeoff completeness for responsiveness
        4. Doing Redundant Work to Speed Up Distributed Queries
           http://www.bailis.org/blog/doing-redundant-work-to-speed-up-distributed-queries/
            1. "In distributed data stores, redundant operations can dramatically drop tail latency at the expense of increased system load;
                different Dynamo-style stores handle this trade-off differently, and there’s room for improvement."
            2. "at the 99.9th percentile,
                sending a single read request to two servers instead of one is 17x faster than sending to one
                —maybe worth the 2x load increase"
        5. Building Software Systems at Google and Lessons Learned, by Jeff Dean
           http://static.googleusercontent.com/external_content/untrusted_dlcp/research.google.com/en/us/people/jeff/Stanford-DL-Nov-2010.pdf
           https://www.youtube.com/watch?v=modXC5IWTJI
            1. good material, covery many aspects of google web search infra
            2. google web search status
                1. update latency: tens of secs
                2. avg. query latency: <0.2s 
                3. # docs: tens of billions
            3. Group Varint Encoding
                1. Pull out 4 2-bit binary lengths into single byte prefix
                2. Decode: Load prefix byte and use value to lookup in 256-entry table
                3. Much faster than alternatives, i.e. Varint encoding
            4. Numbers Everyone Should Know
                L1 cache reference 0.5 ns
                Branch mispredict 5 ns
                L2 cache reference 7 ns
                Mutex lock/unlock 25 ns
                Main memory reference 100 ns
                Compress 1K w/cheap compression algorithm 3,000 ns
                Send 2K bytes over 1 Gbps network 20,000 ns
                Read 1 MB sequentially from memory 250,000 ns
                Round trip within same datacenter 500,000 ns
                Disk seek 10,000,000 ns
                Read 1 MB sequentially from disk 20,000,000 ns
                Send packet CA->Netherlands->CA 150,000,000 ns
            5. Don’t design to scale infinitely:
                ~5X - 50X growth good to consider
                >100X probably requires rethink and rewrite
            6. design patterns
                1. Pattern: Backup Requests to Minimize Latency
                    1. useful when variance is unrelated to specifics of request
                    2. increases overall load by a tiny percentage
                    3. decreases latency tail significantly
                2. Pattern: Multiple Smaller Units per Machine
                    1. Having each machine manage 1 unit of work is inflexible
                       Have each machine manage many smaller units of work/data
                3. Pattern: Elastic Systems
                    1. Problem: Planning for exact peak load is hard
                    2. Design system to adapt:
                        – automatically shrink capacity during idle period
                        – automatically grow capacity as load grows
                    3. Make system resilient to overload:
                        - do something reasonable even up to 2X planned capacity
                          • e.g. shrink size of index searched, back off to less CPU
                          intensive algorithms, drop spelling correction tips, etc.
                        – more aggressive load balancing when imbalance more severe
                4. Pattern: Combine Multiple Implementations
                    1. Example: Google web search system wants all of these:
                        – freshness (update documents in ~1 second)
                        – massive capacity (10000s of requests per second)
                        – high quality retrieval (lots of information about each document)
                        – massive size (billions of documents)
                    2. Very difficult to accomplish in single implementation
                       Partition problem into several subproblems with different engineering tradeoffs.
                        – realtime system: few docs, ok to pay lots of $$$/doc
                        – base system: high # of docs, optimized for low $/doc
                        – realtime+base: high # of docs, fresh, low $/doc
        6. Naive Retries Considered Harmful
           http://www.evanjones.ca/retries-considered-harmful.html
            1. naively retry all requests as soon as a timeout expires
               This common mistake causes a feedback loop that
               makes every slightly overloaded service get swamped with a huge spike of requests
                1. Instead, you must "back off" to avoid overloading the destination during a failure
                2. a good policy is to send a "backup request" after the 95th percentile latency
                3. never retry more than 10% of requests within a 5 minute interval
                4. The problem is when the entire system is slow because it is overloaded, retries make things worse
                5. some thing to borrow from congestion control in networks to RPC systems?
        7. Achieving Rapid Response Times in Large Online Services, by Jeff Dean
           http://research.google.com/people/jeff/latency.html
            1. Basic Latency Reduction Techniques
                1. Differentiated service classes
                    1. prioritized request queues in servers
                    2. prioritized network traffic
                2. Reduce head-of-line blocking
                    1. break large requests into sequence of small requests
                3. Manage expensive background activities
                    1. e.g. log compaction in distributed storage systems
                    2. rate limit activity
                    3. defer expensive activity until load is lower
            2. Synchronized Disruption
                1. randomize background tasks time when each machine performs these tasks?
                2. no, better to synchronize the disruptions
            3. Latency Tolerating Techniques
                1. Cross request adaptation
                    –examine recent behavior
                    –take action to improve latency of future requests
                    –typically relate to balancing load across set of servers
                    –time scale: 10s of seconds to minutes
                2. Within request adaptation
                    - cope with slow subsystems in context of higher level request
                    –time scale: right now, while user is waiting
                3. Fine-Grained Dynamic Partitioning
                    - more than 1 partition per machine (often 10-100/machine)
                    - Speeds Failure Recovery
                4. Load Balancing
                    - Can shed load in few percent increments
                5. Selective Replication
                    - Find heavily used items and make more replicas
                6. Latency-Induced Probation
                    - Initiate corrective action
                7. Handling Within-Request Variability
                    - Canary Requests
                    - Backup Requests
            4. Backup Requests: efficient to reduce long tail percentile
                1. e.g. send a "backup request" after the 95th percentile latency
                2. with Cross-Server Cancellation
                3. Can handle Reed-Solomon reconstruction similarly
            5. Tainted Partial Results
                1. Many systems can tolerate inexact results 
                2. Design to proactively abandon slow subsystems
                    - important to mark such results as tainted in caches
            6. the summary: Collection of techniques
                –general good engineering practices
                    • prioritized server queues, careful management of background activities
                –cross-request adaptation
                    • load balancing, micro-partitioning
                –within-request adaptation
                    • backup requests, backup requests w/ cancellation, tainted results
        8. Heroku's Ugly Secret: The story of how the cloud-king turned its back on Rails
           https://news.ycombinator.com/item?id=5215884
            1. Jeff Dean tail at scale ... "this is an incredibly effective way to DoS yourself"
            2. "Just routing by least connections is one option"
```

The papers employing tail latency implies more detailed scheduling (and even a management framework) helps further: [\[1\]](https://www.usenix.org/system/files/conference/hotcloud16/hotcloud16_nguyen.pdf)[\[2\]](https://people.eecs.berkeley.edu/~dzats/detail.pdf)[\[3\]](https://www.usenix.org/system/files/conference/hotcloud14/hotcloud14-lu.pdf)[\[4\]](https://arxiv.org/pdf/1407.1239.pdf)[\[5\]](https://nsl.cs.usc.edu/~tobiasflach/publications/Flach_Latency.pdf)[\[6\]](http://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p219.pdf)[\[7\]](http://www.microarch.org/micro48/files/slides/F1-2.pdf). Reading notes attached below. You may select them by refs count.

```
1. the papers related to tail latency
    1. The Tail at Scale: How to Predict It?    [2016, 0 refs]
       https://www.usenix.org/system/files/conference/hotcloud16/hotcloud16_nguyen.pdf
        1. predict tail latency by a model, using only the mean and variance of the task response time
           prediction errors for 99th percentile request latency are consistently within 10%
        2. key designs & findings
            1. find that the tail behavior of a task mapped to a subsystem can be captured by
               a generalized exponential distribution function in the high load region,
               which uses the mean and variance of the task response time as input
        3. my comments
            1. I'm not sure whether tail latency in real systems can really be capture by such statistics model
            2. the evaluation workload looks unable to generalize
    2. DeTail: Reducing the Flow Completion Time Tail in Datacenter Networks (Facebook)    [2012, 185 refs]
       https://people.eecs.berkeley.edu/~dzats/detail.pdf
        1. older than Jeff Dean's "The Tail at Scale" paper.
           the approach focus on network stack
           it exploit cross-layer information, to reduce time tail by
            reduce packet drops,
            prioritize latency-sensitive flows,
            and evenly distribute network load
        2. key designs & findings
            1. by reducing the long flow completion tail, the app gains better worst-case performance from the network
            2. network latency varies
                1. congestion causes them to vary by 2 orders of magnitude
                2. because workflow uses many flows, long delay for lots of page creation is possible
                3. causes of long tails
                    1. packet loss and retransmissions
                    2. absence of prioritization
                    3. uneven load balancing
            3. DeTail solution
                1. At the link layer, DeTail uses port buffer occupancies to construct a lossless fabric
                   By responding quickly, lossless fabrics ensure that packets are never dropped due to flash congestion.
                2. At the network layer, DeTail performs per-packet adaptive load balancing of packet routes
                   At every hop, switches use the congestion information obtained from port buffer occupancies to dynamically pick a packet’s next hop
                3. Since packets are no longer lost due to congestion,
                   DeTail's transport protocol relies upon congestion notifications derived from port buffer occupancies
                4. DeTail allows applications to specify flow priorities
    3. Mechanisms and Architectures for Tail-Tolerant System Operations in Cloud    [2014, 7 refs]
       https://www.usenix.org/system/files/conference/hotcloud14/hotcloud14-lu.pdf
        1. wrap cloud provisioning APIs, to reduce their long tail (not app req's long tail?)
        2. key designs
            1. hedged requests
            2. retry, reallocate, force fail/completion
    4. RepNet: Cutting Tail Latency in Data Center Networks with Flow Replication    [2014, 0 refs]
       https://arxiv.org/pdf/1407.1239.pdf
        1. RetNet is an app layer transport. it replicate flows to avoid congestion path, so that tail latency is better
        2. key designs & findings
            1. the reason of long tail latency
                1. elephant flows and mice flows co-exist
                2. even in high bisection topologies, the core part of the network is still over-subscribed
                   this makes congestion likely to happen
            2. use flow replication to reap the path diversity gains
            3. ReSYN only replicates SYN packets
               ReFlow replicates the entire flow
            4. implemented on node.js
            5. efficient multipath routing in data center networks is worth further investigation
    5. Reducing Web Latency: the Virtue of Gentle Aggression (Google)    [2013, 86 refs]
       https://nsl.cs.usc.edu/~tobiasflach/publications/Flach_Latency.pdf
        1. a novel loss recovery mechanisms for TCP using redundant transmissions to minimize timeout-driven recovery
           evaluted on Google production network, yields a 23% decrease in the mean and 47% in 99th percentile latency over today’s TCP
        2. key designs & findings
            1. TCP’s current mechanisms fundamentally limit latency improvements
                1. while connections with no loss complete close to the ideal latency of one round-trip time
                   TCP’s timeoutdriven recovery causes transfers with loss to take five times longer on average
            2. multi-stage architecture, each involve increasing levels of aggression
                1. Reactive: transmits one additional packet per window for a small fraction of flows
                    1. requires only sender side changes
                    2. Reactive can be deployed on client-facing side of frontends to speed Web responses;
                    3. allows a sender to quickly detect tail losses without waiting for an RTO
                2. Corrective: transmits one additional packet per window for all flows
                    1. requires both sender and receiver changes
                    2. Corrective can apply equally to both client and backend connections
                    3. The sender transmits extra FEC packets so that the receiver can repair a small number of losses
                3. Proactive: duplicates the window for a small portion of flows
                    1. Proactive is applied selectively on certain transactions in the backend;
                    2. proactively transmitting copies of each TCP segment
            3. implemented in Linux Kernel
    6. Speeding up Distributed Request-Response Workflows (Microsoft)    [2013, 34 refs]
       http://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p219.pdf
        1. works on Bing, Kwiken manages the tail latency improvements and cost budges. Jeff Dean's "The Tail at Scale" is already considered. good to read
           the 99th percentile of latency improves by over 50% when just 0.1% of the responses are allowed to have partial results
           and by over 40% for 25% of the services when just 5% extra resources are used for reissues
        2. key designs
            1. improve tail latency by employing these core techniques
                1. reissuing laggards elsewhere in the cluster
                2. new policies to return incomplete results
                3.  speeding up laggards by giving them more resources
            2. Although Jeff Dean's "The Tail at Scale", applying them to reduce end-to-end latency is difficult
                1. different stages benefit differently from different techniques
                    1. also, Latencies in individual stages are uncorrelated
                             Latencies across stages are mostly uncorrelated
                        except when running on the same machine
                2. end-to-end effects of local actions depend on topology of the workflow
                   reducing latency of stages usually off the critical path does not improve end-to-end latency
                3. many techniques have overhead, such as increased resource usage when reissuing a request
            3. Kwiken, a framework that takes an end-to-end view of latency improvements and costs, by DAG
                1. the median workflow in production at Bing has 15 stages and 10% of the stages process the query in parallel on 1000s of servers
                   In all, we report results from thousands of stages and hundreds of thousands of servers
                2. casts each stage as a variance-response curve to apportion overall budget appropriately across stages
                3. At the stage/local level, it selects a policy that minimizes the variance of the stage latency.
                   At the workflow/global level, it combines these local policies to minimize the end-to-end latency
                4. burst losses in the network are responsible for a significant fraction of high latencies
    7. TimeTrader: Exploiting Latency Tail to Save Datacenter Energy for Online Search    [2015, 2 refs]
       https://arxiv.org/ftp/arxiv/papers/1503/1503.05338.pdf
       http://www.microarch.org/micro48/files/slides/F1-2.pdf
        1. TimeTrader to reduce energy by exploiting the latency slack in the subcritical replies which arrive before the deadline
           TimeTrader saves 15-19% and 41-49% energy at 90% and 30% loading
            1. it saves energy rather than reduce tail latency
        2. key designs
            1. the two core ideas
                1. TimeTrader trades time across system layers, borrowing from the network layer and lending to the compute layer
                    1. leverage the wellknown Explicit Congestion Notification (ECN) in IP [32] and TCP timeouts
                       to inform the leaves whether a request encountered timeout or congestion in the network and hence does not have slack
                    2. use power management schemes with response times of 1 ms
                2. leverage Earliest Deadline First (EDF) scheduling, to decouple critical requests from the queuing delays of subcritical requests
            2. to determine the slack and slowdown
                1. slowdown =(total slack – RAPLlatency)*scale/compute budget
                2. to set the core’s speed as per the slowdown factor, we employ RAPL  
```

__Monitoring__

There should be two types of monitoring

  * Single operation
  * Percentile statistics

The monitoring should be able to

  * Provide a trace id that can be followed from user request entrance to hardware operations
  * Cover the breakdown of each level
  * Point cover where it is easy to have problems

There are several aspects to be monitored

  * Errors that directly related to customer failure, e.g. VM stall/restart
  * Timeout error counts and auto throttles that directly impact customer experience
  * Operation slowdown
  * Typical hardware performance such as CPU, network, disks
  * Provide trace from user entrace, breakdown at each level, and eventually to hardware

__Other References__

  * [Latency Numbers Every Programmer Should Know](https://people.eecs.berkeley.edu/~rcs/research/interactive_latency.html): Give you the basic latency numbers of each level of a storage system
  * [Disks for Data Centers](http://research.google.com/pubs/pub44830.html): Google's disk experience, which covers some aspect of disk tail latency.
