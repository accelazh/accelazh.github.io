---
layout: post
title: "Recent Paper Reading: EC, Storage"
tagline : "Recent Paper Reading: EC, Storage"
description: "Recent Paper Reading: EC, Storage"
category: "Paper Reading"
tags: [storage, paper, cloud, erasure-coding]
---
{% include JB/setup %}

```
1. A "Hitchhiker's" Guide to Fast and Efficient Data Reconstruction in Erasure-coded Data Centers    [2014, SIGMOD14, 308 refs, Facebook]
   https://www.cs.cmu.edu/~nihars/publications/Hitchhiker_SIGCOMM14.pdf
   Slides: https://www.camdemy.com/media/16288
    1. Related author "K. V. Rashmi". Apply Piggyback Framework on RS code, reduce both network by 25% and disk by 45%. Very good paper.
        1. The key argument is LRC saves reconstruct bandwidth by adding storage overhead, but regenerating code won't
        2. Hitchhiker regenerating applies only when 1 loss, more loss will fallback to plain RS reconstruction (batching the repairs is still favorable)
        2. Additionally, an Hitchhiker-XOR+ code to trade faster computation with less saving 
        3. Note Piggyback Framework is generally simpler than commonly Regenerating codes.
    2. Highlights
        1. Hitchhiker is implemented at HDFS.
        2. Face evaluation
            1. "We deployed Hitchhiker on a 60-machine test cluster in one of the data centers at Facebook, and evaluated the end to-end functionality of the system."
            2. "We consider the encoding parameters (k = 10 r = 4), a block size of 256MB (unless men tioned otherwise), and a bu er size of 1MB."
        3. "HOP-AND-COUPLE" FOR DISK EFFI CIENCY
            1. Unit is node. Stripe is what ECs together. Shaded blocks in Figure 7 are to be read. Hop distance should be unit size / sub-packet count. I.e, corresponding sub-packets from each stripe are put together.
            2. A finding in Figure 7 is nodes don't read the same amount of data.
            3. Another trade off is a reconstruct read reading a small block can split into 2X IOs.
        4. Hitchhiker XOR+
            1. Requiring one parity to be XOR of each data symbol
    3. My questions
        1. How it compares with Regenerating code / MSR code / Clay Code?
            1. OK ... year 2014, Clay Code (2018) hasn't be published yet, so as Product Matrix MSR Codes (2018)
        2. Upon more losses

    n. Related materials
        1. Saving capacity with HDFS RAID    [2014, Facebook]
           https://engineering.fb.com/2014/06/05/core-infra/saving-capacity-with-hdfs-raid/
            1. Facebook's erasure coding implementation at HDFS
            2. "small file" don't have enough blocks to RAID with. Solution: treat the entire leaf directory as a file to RAID with.
            3. Interesting
                1. Handling directory change
                    1. The problem of EC with changeable data
                2. When files are replicated across clusters, sometimes parity files are not moved together with their source files. This often leads to data loss.
                    1. The problem of EC doesn't happen within a single data unit

2. Fast Erasure Coding for Data Storage: A Comprehensive Study of the Acceleration Techniques    [2019, 64 refs, FAST19]
   https://www.usenix.org/conference/fast19/presentation/zhou
   https://www.usenix.org/sites/default/files/conference/protected-files/fast19_slides_zhou_update.pdf
    1. Good paper as a list of EC coding optimization methods.
    2. Highlights
        1. The background is a useful list of existing EC optimizing techniques
            1. Cauchy matrix instead of Vandermonde matrix
            2. Convert Parity Matrix to Bitmatrix
            3. Normalization of the Parity Coding Matrix / bitmatrix normalization
            4. Smart Scheduling - reuse an existing parity to generate the next parity
            5. Matching - any common parts of the XOR chain can be reused
            6. SIMD vectorization
            7. Reduce cache miss - each data chunk is accessed only once and to update all parities
            8. Table 1, good, a table to compare performance gain of each approaches
            9. Search for the optimal (X, Y) in Cauchy matrix
        2. Using simulated annealing, genetic algorithm to find the optimal (X, Y)-strategy

3. Azure SWAN: Achieving High Utilization with Software-Driven WAN    [2013, 1513 refs, SIGCOMM13, Microsoft]
   https://conferences.sigcomm.org/sigcomm/2013/papers/sigcomm/p15.pdf
    1. Azure WAN solution that coming to SDN approach.
    2. Highlights
        1. SDN primer
            1. Networks today
                1. Beefy routers
                2. Control plane: distributed, on-board
                3. Data plane: indirect configuration
            2. SDNs
                1. Streamlined switches
                    1. Typically OpenFlow switches
                2. Control plane: centralized, off-board
                3. Data plane: direct configuration
        2. Key design challenges
            1. Scalably computing BW allocations and network config
            2. Avoiding congestion during network updates
            3. Working with limited switch memory
    n. Related materials
        1. Azure SWAN: Platform for secure and traceable data exchange 
           https://azuremarketplace.microsoft.com/en-us/marketplace/apps/ssc-servicesgmbh1674730907970.swan_saas
        2. Azure SWAN: Software-driven wide area network
           https://www.microsoft.com/en-us/research/wp-content/uploads/2017/01/swan-msrc-jul2013.pdf

4. ClickHouse - Lightning Fast Analytics for Everyone    [2024, 7 refs, VLDB24, ClickHouse]
   https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf
    1. ClickHouse published this paper to describe its key technologies. Most are already well known for this famous product.
    2. Highlights
        1. Figure 2 the architecture
        2. MergeTree, but different from LSM-tree
            1. no tree hierarchy
            2. no constraint to merge the same level
            3. writes inserts directly to disk rather than WAL
            4. merge-time data transformation
            5. Idempotent Inserts
        3. On-disk format
            1. column clustering, granules (row group), block
            2. delta coding first, then heavy compression, then encryption
        4. pruning
            1. granules level min-max zoning
            2. table projection, which is sorted by a different primary key
            3. skipping index. small amount of metadata at the level of multiple granules
                1. min-max, set indices, bloom filters
        5. optimization for scenarios
            1. batch queries
            2. business telemetry
            3. time history
            4. analytics
        6. ACID
            1. Avoid using locks. operate on snapshots
            2. Most write-heavy ClickHouse instance in practice doesn't force fsync. It speeds up by tolerating small risk of losing recent data
                1. Interesting, most, in practice
        7. Query processing
            1. Parallelism  
                1. Table shards are processed in parallel by multiple nodes
                2. Data chunks are processed in parallel by a node's multiple CPU cores
                3. Data elements are processed in parallel by a CPU core's SIMD units
        8. Integration layer
            1. interesting
        9. Performance as a feature
            1. Built-in Performance Analysis Tools
                1. Server and query metrics
                2. Sampling profiler
                3. OpenTelemetry integration
                4. Explain query

5. Revisiting Network Coding for Warm Blob Storage    [2025, 0 refs, FAST25]
   https://www.usenix.org/system/files/fast25-gan.pdf
    1. NCBlob that optimizes EC on small blob with Split-merge-encode scheme (Figure 5) and Merge-split-encode scheme (Figure 6) and F-MSR (non-systematic). Large blobs can still use Clay Code.
    2. Highlights
        1. Design idea: Performing encoding on the group of data with access locality
        2. Split-merge-encode scheme
            1. my questions
                1. IO amplification is a small blob is future cut into sub-blobs?
        3. Hybrid MSR codes for all blobs
            1. determining the blob size threshold to switch between F-MSR vs Clay Code
                1. repair time is dominated by disk seek time when blob size decreases. NCBlob favors small blob because it reduces seek time by reducing sub-packetization. In generational, non-systematic MSR can reduce sub-packetization.

6. Fast, Transparent Filesystem Microkernel Recovery with Ananke    [2025, 0 refs, FAST25 best paper]
   https://www.usenix.org/conference/fast25/presentation/liu-jing
   https://www.usenix.org/system/files/fast25_slides-liu-jing.pdf
    1. Interesting new direction of microkernel FS. The key problem to solve is how to selectively reply the operation logs for fast process crash recovery
    2. Highlights
        1. Introduction
            1. Microkernel FS allows app and OS to continue after FS crash. But how should FS do recovery? The in-memory FS states are lost.
        2. P-Log and AIM (Act, Ignore, Modify)
            1. Figure 4: Intuition behind P-Log and AIM. The chart is useful as to list FS operations and their categories
            2. Figure 2: P-log by design survives after FS crash. New FS process uses P-log and only P-log to recover the state gap.
            3. The key challenges are, we must selectively replay P-Log.
                1. Some updates may have already been durable
                2. Some states can be affected by later states
                3. Operations that do no update state do no need to be replayed
                4. See Figure 3: P-log design

7. Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot    [2025, 0 refs, FAST25 best paper, Moonshot AI]
   https://www.usenix.org/conference/fast25/presentation/qin
   https://www.usenix.org/system/files/fast25_slides-qin.pdf
    1. Interesting paper as to re-illustrate Moonshot's key technology - P&D disaggregation for KVCache. By evaluation, the improvement is huge.
       KVCache is what the title said "trading more storage for less computation" 
    2. Highlights
        1. LLM Interference: Prefix Caching
            1. KVCache can be shared across requests with the same prefix, reducing computation during prefill
            2. Around 50% of the tokens’ KVCache in the real-world workloads can be reused
        2. P&D disaggregation - Mooncake Store
            1. Prefill instance
                1. Prefix KVCache
                2. Incremental KVCache
                3. Layer-wise load and store
                4. KVCache transfer
                5. chunked pipeline parallelism (CPP) 
            2. Decoding instance
                1. Full KVCache
                2. Async load
            3. Mooncake store
                1. Transfer engine
                    1. A key trade-off in P&D disaggregation is extra bandwidth requirement to transfer the cache
                    2. Key technologies: Zero-copy, multi-NIC up to 8*400Gbps aggregated bandwidth, topology aware, failure recovery, load balance, multi-transport support, etc
                2. Global caching pool
            4. Inference Engine
            5. Scheduling
                1. Swapping cold blocks, replicating hot blocks
                2. Algorithm 1: KVCache-centric Scheduling Algorithm
                    1. polynomial regression model fitted with offline data
                3. Load balancing
                4. local vs remote prefix cache entry
    n. Related works
        1. Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving
           https://yiyibooks.cn/arxiv/2407.00079v3/index.html
```
