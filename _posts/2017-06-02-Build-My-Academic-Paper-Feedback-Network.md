---
layout: post
title: "Build My Academic Paper Feedback Network"
tagline : "Build My Academic Paper Feedback Network"
description: "Build My Academic Paper Feedback Network"
category: "storage"
tags: [storage, fast, osdi, paper]
---
{% include JB/setup %}

I sketch through each top-level storage conferences and try to build a framework to catch world storage technology updates and to quickly filter through large volume of papers and to select good ones. There are other sources though, like industrial summits, and opensource project commits/blueprints, leader company moves, etc. This article will focus on papers.

### Why read papers

Generally, papers are good sources to understand technology in depth.

  * The introduciton parts and related works parts are usually the best resource to grasp a new domain. There are papers that are very informative doing the introduction.
  
  * The analytical skills, where how the authors conduct the improvements and root cause digging, can be borrowed.
  
  * The design points and experiences can be applied into more places.
  
  * The evaluation part can be learned as how to evaluate systematically with quality.

Essentially, a peek to the top human minds is the most interesting.

### Research and industry

Some research works may need 5+ years (or even much more) to be wide-adopted into industry, like the erasure-coding, LSM-tree, Paxos, etc. Those who did the opening work and be the first to bring them into industry are remarkable. They may be the secret source to build a industry leading product. To select the really valuable research works (some may be rarely know) and apply to industrial system development (you need a lot of analysis, decision making, and adoption changes) is the top skill.

Some research papers took much less time. They can be quickly learned to industry. There are papers proposing various improvements to existing technology. Maybe 1-2 years they will be adopted in mang places.

Sometime research works follow the industry breakthrough, like MapReduce, scale-out storage, etc. They help to propose new improvements, experience, evaluations, which we can learn form. Research works may also co-walk with industry, like deeplearning, GPU computing, etc. 

Some research works are directly brought into industry. Usually, there is some college folk who did remarkable research, like Ceph, and they build startup company with it. These works may eventually affect industry trends.

There are papers written to expose industry system designs, like BigTable, Cassandra, etc. They are remarkable learning sources, and will usually start new projects improved from them.

Besides the above, papers are pool of sources to learn problem analyzing skills, to update with information and knowledges, and to share and borrow a lot of technology improvements.

### How to fast read

Papers are structured for fast reading.

  * Everything important in the paper will definitely be illustrated in the abstract. And, if the paper achieves good results in evaluation, it will add that.
  
  * Besides the informative background, contemporary work, motivations, challenges, the introduction/background/overview part will usually illustrate the main designs and key improvements/contributions of this paper; they can even be seen as a shorter version of this paper.
  
  * By common practice, for every paragraph, the first sentence clearly summarizes what this paragraph is going to say; following that are examples, detailed designs, and discussions on the details.
  
  * Abstract, introduction, related works, evaluation, conclusion, are the five key parts of the paper for fast read. They can define what place the paper stands.
  
  * Generally, most paper is based on one improvement/finding -> write a new protoype system to illustrate it -> digging the deeper layer of problems, analysis more -> add some secondary improvements/fixes. You can catch its head. Some other papers are whole system design; they will talk about every aspects of the system; So usually with more information.
  
  * The most helpful one is, actually, after you read 100+ papers in specific domain, fast reading is natually easy. You almost know what it is going to say.

Essentially, it is not the volume of words, but the volume of new information that defines the speed of read.

### How to select good papers

Even only in top-level storage conferences, there are too many papers each year. Here I share some experience to select good ones to read. Only appliable to storage.

  * The (nominated) best paper award, and invited paper, in each top-level conferences, are usually of high value. For example, [Paragon](https://pdfs.semanticscholar.org/ec16/af98929e9da143dcbee01023718013e01d22.pdf) is nominated for Best Paper Award at ASPLOS, selected as Invited Paper in the ACM Transactions on Computer Systems (TOCS), and selected in IEEE Micro's Top Picks for 2013. Here's a link to [the collection of all best papers](http://jeffhuang.com/best_paper_awards.html).
      
  * Good papers have quick growing reference count in 1-2 years. 10 refs in the first year can be a sign of good paper. No matter time, if a paper has 1000+ or 2000+ refs, it is a breakthrough paper, very worth reading. If a paper has 200+ to 300+ refs, it is usually a big improvement paper. 100+ means the paper is influencing. You can also use Google Scholar to search, which ranks by reference count and recentness.

  * See the paper's abstract. Good paper usually show significant performance improvements. Better if it is evaluated solidly on real production workloads. And the important thing is, every true highlights should be listed in abstract. So you should find what you need. Also, papers done by industrial leading companies on prduction systems, like Google, Facebook, Microsoft, etc, are usually good.

  * Dig into the paper's reference list. Usually, only papers will be notable achievements will be referenced by others. Famous paper's reference list is also worth digging. And you may also find some famous authors and their trail of publishing paper, like the beginning of [log-structed FS](https://people.eecs.berkeley.edu/~brewer/cs262/LFS.pdf).

  * If the paper's author starts a startup or opensource project with it, that usually means it is a really good paper. For example, Ceph, Paragon & Quasar, RAMCloud.

  * Some paper has extensive background introduction, they are very helpful to understand a new technology domain in depth. These papers may even illustrate the history of how the technology evolves through each breakthrough and the corresponding papers, very helpful.

  * Good storage papers may resides in multiple conferences, not only just storage. For example, OSDI is named as operation system architecture, but it is also a top place for storage papers. NSDI is named as networking conference, but it also has good storage papers because distributed storage is a network system. Also, top-level conferences usually features in the amount of work, and depth of analysis, or good performance results; but not necessarily the smartest ideas, while ATC does have some smart but simpler papers.

  * You may even hunt on college curriculums. They help grow solid understanding. For example, from [where Ceph's author Sage graduated](https://users.soe.ucsc.edu/~sbrandt/290S/).

### Storage top-level conferences

Here I list the top-level conferences related to storage. (The "others" part is not top-level, but ATC is worth reading.)

  * Architecture： ISCA, HPCA, ASPLOS
  * Storage: FAST, MSST
  * Operation Systems： SOSP, OSDI
  * Networking： NSDI, SIGCOMM
  * Database: SIGMOD, VLDB
  * Others: ATC, ACM TOCS, ACM TOS, hotCloud

Each of them probably publish ~50 papers each year.

### Ranking good papers

I want to index the recent year papers and rank them by reference counts, so that I can find out which are good papers and whose reference counts are quickly growing. In the end I found Google Scholar is the handy tool. Here I list each conference, their home page of year 2016, and google scholar search links for their papers. In the search results page, the top ones are usually good papers.

  * FAST: top-level storage conference; favor in filesystem, reliability, SSD, kvstore papers; lack distributed architecture design (I guess they are supposed to goto OSDI/SOSP)
      * [Home 2016](https://www.usenix.org/conference/fast16/technical-sessions)
      * Searches 2016: [part-1](https://scholar.google.com/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=FAST&as_ylo=2014&as_yhi=2017&btnG=&hl=en&as_sdt=0%2C5), [part-2](https://scholar.google.com/scholar?hl=en&as_publication=USENIX+Conference+on+File+and+Storage&as_sdt=0%2C5&as_vis=1&as_ylo=2014&as_yhi=2017)

  * MSST: top-level, more industry oriented; also includes panels and talks; Ceph once occupied the headline.
      * [Home 2016](http://storageconference.us/2016/)
      * [Searches 2016](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=MSST&as_sdt=0%2C5&as_vis=1&as_ylo=2014&as_yhi=2017)

  * USENIX ATC: much more papers; contains smart ideas; Copyset paper was published in it
      * [Home 2016](https://www.usenix.org/conference/atc16/technical-sessions)
      * [Searches 2016](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=USENIX+Annual+Technical+Conference&as_sdt=0%2C5&as_vis=1&as_ylo=2014&as_yhi=2016)

  * OSDI: top-level, storage architecture, paxos, scheduling, big data, OS components, etc. A place to publish new distributed storage system architectures. Google likes to publish here, e.g. Bigtable, MapReduce, Spanner.
      * [Home 2016](https://www.usenix.org/conference/osdi16/program)
      * Searches 2016: [part-1](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=OSDI&as_sdt=0%2C5&as_ylo=2014&as_yhi=2017), [part-2](https://scholar.google.com.sg/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=Operating+Systems+Design+and+Implementation&as_ylo=2014&as_yhi=2016&hl=zh-CN)

  * SOSP: top-level, storage architecture, paxos, big data, OS components, etc. A place to publish new distributed storage system architectures, e.g. Google File System
      * [Home 2015 (per 2 years)](http://sigops.org/sosp/sosp15/archive/index.html)
      * [Searches 2015](https://scholar.google.com.sg/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=Symposium+on+Operating+Systems+Principles&as_ylo=2015&as_yhi=2017&hl=zh-CN)

  * ASPLOS: top-level, storage architecture, scheduling, OS, etc. The Quasar & Paragon scheduler was published here. Most paper published into sigarch, sigops, sigplan.
      * [Home 2016](https://www.ece.cmu.edu/calcm/asplos2016/program.html)
      * Searches 2016: [asplos part-1](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=Architectural+Support+for+Programming+Languages+and+Operating+Systems&as_sdt=0%2C5&as_vis=1&as_ylo=2014&as_yhi=2017), [asplos part-2](https://scholar.google.com.sg/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=ASPLOS&as_ylo=2014&as_yhi=2017&btnG=&hl=zh-CN), [sigarch](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=SIGARCH&as_sdt=0%2C5&as_vis=1&as_ylo=2015&as_yhi=2017), [sigops](https://scholar.google.com/scholar?hl=en&as_publication=SIGOPS&as_sdt=0%2C5&as_vis=1&as_ylo=2015&as_yhi=2017), [sigplan](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=SIGPLAN&as_sdt=0%2C5&as_vis=1&as_ylo=2015&as_yhi=2017)

  * ISCA: top-level, computer architecture, cache, resource utilization, etc. Google Heracles was published in it.
      * [Home 2016](http://isca2016.eecs.umich.edu/index.php/main-program/)
      * [Searches 2016](https://scholar.google.com/scholar?hl=en&as_publication=%22Computer+Architecture+(ISCA)%22&as_sdt=0,5&as_ylo=2015&as_yhi=2017)

  * HPCA: high-performance computing.
      * [Home 2016](http://hpca22.site.ac.upc.edu/index.php/program/conference-program/)
      * [Searches 2016](https://scholar.google.com.sg/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=HPCA&as_ylo=2016&as_yhi=2016&hl=zh-CN)

  * NSDI: top-level network, also include some distributed storage systems. The ZLog CORFU paper was published here.
      * [Home 2016](https://www.usenix.org/conference/nsdi16)
      * [Searches 2016](https://scholar.google.com.sg/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=NSDI&as_ylo=2016&as_yhi=2016&hl=zh-CN)

  * SIGCOMM: top-level network, include big player papers such as Google, Facebook. DCTCP, Jupiter Rising, were published here.
      * [Home 2016](http://conferences.sigcomm.org/sigcomm/2016/program.php)
      * [Searches 2016](https://scholar.google.com.sg/scholar?as_q=&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=&as_publication=SIGCOMM&as_ylo=2016&as_yhi=2016&hl=zh-CN)

  * SIGMOD/PODS: top-level database
      * Home 2016: [SIGMOD](http://sigmod2016.org/program_sigmod.shtml) / [PODS](http://sigmod2016.org/program_pods.shtml)
      * Searches 2016: [SIGMOD](https://scholar.google.com.sg/scholar?q=&btnG=&hl=zh-CN&as_publication=International+Conference+on+Management+of+Data&as_sdt=0%2C5&as_ylo=2016&as_yhi=2016), [PODS](https://scholar.google.com.sg/scholar?q=&btnG=&hl=zh-CN&as_publication=Symposium+on+Principles+of+Database+Systems&as_sdt=0%2C5&as_ylo=2016&as_yhi=2016&as_vis=1)

  * VLDB: top-level database
      * Home 2016: [research track](http://www.vldb.org/pvldb/vol10.html), [industrial track](http://vldb2016.persistent.com/industrial_track_papers.php)
      * [Searches 2016](https://scholar.google.com.sg/scholar?q=&btnG=&hl=zh-CN&as_publication=VLDB&as_sdt=0%2C5&as_ylo=2016&as_yhi=2016)

  * hotCloud: hot topics in cloud computing
      * [Home 2016](https://www.usenix.org/conference/hotcloud16/workshop-program)
      * [Searches 2016](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=hotCloud&as_sdt=0%2C5&as_vis=1&as_ylo=2016&as_yhi=2016)

  * ACM TOCS: ACM transactions on Compute Systems. the old and classic place; The beginning of log structured filessytem, "The design and implementation of a log-structured file system", was published here; also the Bigtable paper.
      * [Home](http://tocs.acm.org/)
      * [Searches 2016](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=ACM+Transactions+on+Computer+Systems&as_sdt=0,5&as_ylo=2016&as_yhi=2016)

  * ACM TOS: ACM transactions on Storage. Archival journal that deals with storage.
      * [Home](http://tos.acm.org/)
      * [Searches 2016](https://scholar.google.com.sg/scholar?hl=zh-CN&as_publication=ACM+Transactions+on+Storage&as_sdt=0%2C5&as_vis=1&as_ylo=2015&as_yhi=2017)

Additionally, for all the best papers in the above conferences

  * The [collection of all best papers](http://jeffhuang.com/best_paper_awards.html)

### Tour across conferences

To grasp how the world storage technology evolves, I sketch through papers in each conferences at year 2016 and extracts what are everyone talking about.

__MSST 2016___

```
    1. the panels, talks, invited tracks, are very helpful.
    2. compared to FAST, MSST is more close to industry, and FAST is more academic (but also have Google, Microsoft industrial papers)
    3. the topics covered: flash, dedup, archival,
                           Storage Performance Enhancements
                           File Systems for Non-Volatile Memory
                           Store More, Longer, and for Less: Deduplication and Archival Systems
                           Spotlight on Flash memory and Solid-State Drives
                           Understanding Storage Systems through Measurements and Analysis
                           On-the-Go Storage
```

__ATC 2016__

```
    1. there is a section, "Best of the Rest", that lists all the Best Paper in other conferences, e.g. FAST, NDSI, SOSP, Usenix Security, etc.
    2. ATC gives Best Student Paper. A lot of ATC papers are smart.
    3. ATC covers almost every hot topics in storage: KV Store, Security, Cloud, Consensus, Caching, Indexing, Network, Big Data, OS.
```

__OSDI 2016__

```
    1. topics: filesystem crash verification, compiler, libraries on multi-core, OS context & processes;
               cloud scheduling, including the CARBYNE, Firmament which were once recommended, all sort of;
               storage transaction, replicate protocol, in-memory, RDM, RPC;
               networking NFV, reachability analysis, datacenter networking, disaggregated interconnect
               graph processing, Tensorflow, RDF graphs
               software engineering, programming languages, GC, code re-randomization (security), JVM,
               EC Cache, evolution of the multiprocessor software architecture, geo-distributed analytics, Dynamic information flow tracking (DIFT)
               Paxos, Consensus, crash fault-tolerance, state-machine replication (SMR), concurrency control
               security, sandbox, private/secure communication, analytics over encrypted data
               Troubleshooting, performance profiling, config error detection, live traffic tests
               formal verification, certified OS, per-application library OS, container security, Intel SGX, huge page
               reactive data management service, general purpose sharding, co-locate & resource utilization, data quality
    2. reading the abstracts of each paper is a good way to know the domains. also watch for the best papers
```

__SOSP 2015__

```
    1. topics: Formal Systems, Crash Hoare Logic, provably correct distributed systems
               Distributed transactions, in-memory, RDMA, RPC exactly-once semantics, RAMCloud
               Distributed Systems, Paxos, private messaging,
               Concurrency and Performance, MapReduce, read-log-update, synchronization mechanism, performance Profiling
               Energy Aware Systems, mobile, tablet, Software Defined Batteries, Power Management
               More Distributed Transactions, scalable SQL, replication protocol, consistency, ACID concurrency control,
               Experience and Practice, anomalies in consistency, CPU validation,
               Bugs and Analysis, Root Cause Diagnosis, filesystem semantic bugs,
               Big Data, memory pressure, programming model, graph processing, mining,
               Storage Systems, filesystem directory cache, maintenance (backup, layout optimization, etc), Split-Level I/O Scheduling
    2. SOSP and OSDI are both 2-year each, OSDI in even years, SOSP in odd years. They provide high quality storage papers.
```

__ASPLOS 2016__

```
    1. topics: Multicore, on-chip wireless communication, market-based chip shared resource allocation, performance-management runtime QoS
               IO, sidecores, network DMA interface, crash-consistency models
               Memory Management, memory allocator,  Cache Management, tail latency prediction & correction
               Debugging, static bug checking, Detecting data races, formal verify high-assurance file-system
                          Causality inference, Non-Deterministic Concurrency Bugs, Reference counts bugs
               Heterogeneous Architectures and Accelerators, OS design for Heterogeneous Manycores, Energy Efficient, offloading to a low-power processor, Manycore, verifying memory ordering
                                                             FPGAs, kernel-based data parallel programming models, interference, PCI-e bandwidth contention, GPU, Behavioral Specialized Accelerators,
               Security, IOMMU Protection, encrypt NVM, Verified Untrusted System Services, SGX, trusted
                         Information-Flow Tracking, Program State Relocation, “rowhammer” attack,
               Code Generation and Synthesis, code optimizer, Assembly, compilers, binary analysis, Code variants
               Energy and Thermal Management, Power management, Energy-autonomous, sprinting architecture
               Emerging Memory Technologies, NVRAM Write-Ahead Logging, Transactions on NVRAM, image encoding on storage cell, Persistent Memory Logging
               Cloud Computing, Interference Management, language runtime, Resource-Efficient Provisioning, Workflow Monitoring
               OS Optimizations, Kernel TCP Design, Short-Lived Connections, Virtual Address Spaces, heterogeneous memories
               Non-traditional Computer Systems, non-Von Neumann architecture, Pattern-Recognition Processors, controlling approximation, Approximate Computing, DNA-based archival storage
               Transactional Memory, recovery from unexpected permanent processor faults, Lock-Free Multicore Synchronization, breaks the serialization of hardware queues
    2. ASPLOS is somewhat more close to hardware (processors, cores, interfaces, IO, memory) and thus involves more disciplines, as said in its description
       ASPLOS also has more papers about debugging/languages/compilers, and OS low levels that interfacing to hardware
    3. ASPLOS have many invited talks/speeches besides the papers, also the
       "Synopsis of the ASPLOS ’16 Wild and Crazy Ideas (WACI) Invited-Speakers Session"
```

__ISCA 2016__

```
    1. topics: Neural Networks, DNN, Processing-in-memory (PIM), NN acceleration
                                DNN compression, mobile vision, image sensor, CNN, accelerator, Low-Power
                                energy consumption, minimal data movement, dataflow, High-Density 3D Memory, neuromorphic architecture, domain-specific ISA
               Heterogeneous Architecture / Approximate Computing, Work stealing, Work-mugging, object deserialization , co-processor, Approximate Acceleration
               Caches, Cache Replacement, TLB, virtual caching, LLC energy-efficient,
               Hardware Design, Reconfigurable Hardware, FPGA, neural networks, RTL designs, On-core microarchitectural, HW/SW co-designed
               Accelerators, Near-Data Processing, big data, Data-intensive, Graph Analytics Accelerators, ASIC accelerators, Bitcoin mining ASIC Clouds
               GPUs, Cache Efficiency, Transparent Offloading, Near-Data Processing in GPU, 3D-stacked memory, memory-intensive, multiprogramming GPUs,
                     Locality Aware thread block (TB) Scheduler, Address Translation on GPUs, Thread-Level Parallelism,
               NoC / Virtualization, NoC-based CMP, VM Interpreters, ARM Virtualization,
               Cache / Memory Compression, cache compression vs replacement, Compression in Many-core,
               Reliability, high reliability memory systems, On-Die ECC, Production-Run Software Failure Diagnosis, neural hardware
                            end-to-end ECC, on-chip ECC, error pattern transformation, memory reliability, memory faults, Memory Repair,
               Microarchitecture, ISA extension, data-level parallelism (DLP), SIMD, Simultaneous multithreading (SMT) out-of-order cores, enhanced Memory Controller,
               Datacenters, Tail Latency, Precise Load Testing, Power Management, Scheduling, Energy Proportional Servers, Power Virus, power attack defense
               Memory, FPGA, DRAM-Based Reconfigurable Acceleration Fabric, DRAM subarrays, Lifetime in Resistive Memories, PCRAM and ReRAM Wear leveling / wear limiting, Memory Inter-arrival Time Traffic Shaping
                       Phase Change Memory (PCM),  re-constructing data, Nested paging, shadow paging, virtual machine monitor (VMM), DRAM data bus energy-efficiency, encoding
               Emerging Architectures, Approximate computing, Markov Chain Monte Carlo (MCMC) sampling, Molecular Optical Gibbs Sampling Units, Analog Accelerator
               Energy-efficient Computing, Resource Efficiency, MIMO (multiple input, multiple output) controller, Ultra-Low-Power processors, Sub-core Configurable Architecture
    2. ISCA talks a lot about cache, memory, accelerator, GPU, software/hardware co-design architecture changes, also neural networks,
```

__HPCA 2016__

```
    1. topics: Hardware Accelerators, Boltzmann machine, deep learning, FPGA, resistive RAM (RRAM), memory-centric, compute in memory, machine learning, generate accelerators, general-purpose programmability, domain-specific
               Mobile/IoT, mobile CPU design, smartphone, energy control, QoS, Software Defined Radio (SDR)
               NVM, non-intrusive memory controller, Compression-expansion coding, reconfigurable architecture, resistive RAM, Access-transistor-free memristive crossbars
               Reconfigurable Architectures, FPGA, OpenCL, Near-Data Processing, coarse-grain reconfigurable architectures (CGRA), dynamic binary translation,
               GPUs, Voltage noise, manufacturing process variation,  core tunneling, GPU pre-execution, Warps, Compression,
               Cache, cache placement, Virtual caches, cache synonyms, Modeling Cache Performance, LRU, cache tag management, Tagless DRAM Caches (TDCs),
               Coherence and Consistency, Sequential Consistency Violations, Contention for shared memory, true sharing / false sharing, hardware transactional memory (HTM),
               Interconnects, network on chip (NoC), dynamic voltage/frequency scaling (DVFS), chip multiprocessors (CMPs), Photonic interconnects, laser gating technique, power efficiency
               GPGPUs, page memory, Simultaneous Multikernel GPU, dynamic sharing, warp scheduling,
               Security, timing-channel protection, secure memory scheduling, key recovery timing attack on a GPU, side-channel vulnerability on GPU, last-level cache side channel attacks,
               Large-Scale Systems, NUMA, core allocation, Power oversubscription, power capping, Power Surges, Fuel cells power source, datacenters, energy storage devices,
               Potpourri, mathematical computing architecture, power efficiency, Hardware prefetching, memory page migration, asymmetric regions memory architecture
               Industry Session, Cache coherence between CPUs and GPUs, consolidated server racks, datacenter server architectures, Soft-Errors on GPUs, mobile storage architecture,
               Memory Technology, significant variations and degraded timings, restore cell data, die-stacked DRAMs, 3D DRAM, memory faults, bulk data movement in DRAM, DRAM latency
               Best of IEEE Computer Architecture Letters, Associative Processor (AP), resistive memory, Stochastic and Deterministic Computing, heterogeneous architectures, specialized hardware, Heterogeneous Power, power mismatching,
               Modeling and Testing, heterogeneous multicore processors, thermal estimation, Microarchitecture, simulation, memory consistency model (MCM),
               Caches and TLB, Address Translation, Energy-Efficient, LLCs, dead-block management, Cache QoS, Cache Monitoring Technology (CMT), Cache Allocation Technology (CAT),
               Microarchitecture, Simultaneous multithreading (SMT) processors, IBM POWER8, symbiotic job scheduling, Voltage Scalability, energy efficiency, sharing physical register,
    2. HPCA talks a lot about high-end / accelerating hardwares, and in-depth. there are accelerators, NVM, Resistive RAM, GPUs, caches (hardware), interconnects, large NUMA, processsors. there are also many evaluation papers on new approaches/technology.
```

__NSDI 2016__

```
    1. topics: Network Architectures and Protocols, Software-Defined Internet Exchange Points (SDXes), Rack-scale computers, rack-scale network, SDN,  load balancing, blockchain, bitcoin, mobile cellular devices, cellular traffic,
               Content Delivery, user delays, media delivery, cryptographic, private information retrieval (PIR), page load latency, Dependency Tracking, video Quality of Experience (QoE),
               Wireless I, low power, hardware, Localization, indoor positioning, AP, uplink, human blockage,
               Flexible Networks, Measuring the flow of traffic, traffic engineering, SDN optimization, Middlebox, NFV, outsource network processing to the cloud, middlebox outsourcing,
               Dependability and Monitoring, Checking whether a network correctly implements intended policies, minimized bug executions, netflow, Internet routes, Network forensics and incident response,
               Resource Sharing, predict performance, Web Memory Cache allocation, fair allocation of memory cachem, Resource Fairness (DRF), isolation,
               Distributed Systems, Consensus, atomic broadcast, FPGA, stream processing, assignments, Social Networks, file slicing API, zero-copy, Storage-Performance Tradeoff,
               In-Network Processing, packet scheduling, Least Slack Time First (LSTF), Explicit Congestion Notification (ECN), load balancer, ECMP, Middlebox, inspect packet payloads,
               Security and Privacy, Delegations, Community Repositories, Anonymous Reputation, Tracking-Resistant, Tor, latency-based congestion control, expose user data to web services, Mobile, access control,
               Wireless II, Cellular Network,  data center networks (DCN), 3D Ring Reflection Spaces (RRSs), Physical Vibration, vibratory radio, privacy threat, sensor obfuscation technique,
    2. Although NSDI is named as network, it does provide good storage system papers. There are also SDN, web sites (and CDN, latency, memory cache), mobile (and wireless), protocols, middleboxes, packet processing, etc.
```

__SIGCOMM 2016__

```
    1. topics: SDN & NFV I, reconfigurable hardware, packet processing, FPGA, data-plane algorithms, OpenFlow, line rate,
               Wide Area Networks, high-available, network infrastructure, optical WAN, bulk transfer, inter-datacenter transfer, traffic engineering,
               Monitoring and Diagnostics, network flow monitoring, "one-big-switch" abstraction, event monitoring, differential provenance,
               Scheduling, fair queuing, multi-tenant, coflows, mix-flows with/without deadlines, bandwidth allocation control,
               Datacenters I, Datacenter Time Protocol (DTP), network managment, RDMA, flow-control mechanism, datacenter interconnects,
               Verification, control plane analysis, network static analysis, symbolic execution, BGP,
               Networked Applications, page load time, end-to-end latency, video quality-of-experience (QoE), Telephony Call Quality,
               Wireless, inter-technology backscatter, FPGA, ultra-low power, on-body sensor, energy budget, power-proportional, distributed MIMO, cellular network,
               Datacenters II, congestion control, virtualized, DCTCP, vSwitch, root cause analysis,
               Censorship and Choice, ISP, traffic policing, policing and pacing and shaping, net neutrality, L2 STP and L3, convergence,
               SDN & NFV II, network-wide deployment, network functions (NF), software switch, P4, OVS, OpenFlow,
               Best of CCR, transparency, privacy, social interactions, human rights,
    2. SIGCOMM talks about packet processing, datacenter networking, WAN, BGP, wireless, SDN/NFV. not as close to distributed storage systems as NSDI does.
```

__SIGMOD 2016__

```
    1. topics: (too many. only picking 3 papers each)
               Scalable Analytics and Machine Learning, join, machine learning (ML), batch gradient descent, video recommendation,
               Privacy and Security, social graph, Differential privacy,
               Logical and Physical Database Design, Data Warehouse, NoSQL, Oracle, JSON data management, Couchbase,
               New Storage and Network Architectures, OLTP and OLAP, Vectorization, JIT, flash translation layer (FTL), PVB, Flash,
               Graphs 1: Infrastructure and Processing on Modern Hardware, Breadth-First Search (BFS), GPU, joint traversal, Iterative Analysis, Relational,
               Streaming 1: Systems and Outlier Detection, Complex Event Processing (CEP), shared patterns, incremental View Maintenance, outlier detection,
               Approximate Query Processing, relational algebra (RA), bounded RA queries, join, complex ad-hoc queries,
               Networks and the Web, sampling, Viral Marketing, social network, continuous influence maximization problem,
               Data Discovery and Extraction, metadata, datasets, entity resolution project, Functional dependencies,
               Data Integration / Cleaning, Integrity constraints, repair data, data cleaning,
               Spatio / Temporal Databases, spatial and temporal, mining, temporal aggregation, Many-Many Relationships
               Distributed Data Processing, Realtime, Spark, R, SQL-on-Hadoop,
               Graphs 2: Subgraph-based Optimization Techniques, Subgraph querying, Graph Indexing, Subgraph Matching,
               Main Memory Analytics, Multi-Column Sorting, pipelining, Columnar Access, HANA, In-memory columnar databases,
               Interactive Analytics, OLAP, incremental query processing, Prefetching,
               Streaming 2: Sketches, Adaptiveness, sampling, Accurate,
               Transaction Processing, B+-tree, In-Memory Indexing, CPU-GPU, Checkpointing, Main-Memory Database, Deterministic database systems,
               Transactions and Consistency, Weak Consistency, Optimistic Concurrency Control, OLTP, Multicore, contention,
               Query Optimization, Adaptive techniques, cost-based optimizer, Sampling-Based, Multi-Objective,
               Graphs 3: Potpourri, heterogeneous entity graphs, Graph Ordering, In-Memory, scale-free graphs,
               Hardware Acceleration and Query Compilation, Co-Processor, Query Compiler, auto-scale,
               Nearest Neighbors and Similarity Search, Place Retrieval, Unstructured Text, local similarity search, Similarity Join,
    2. SIGMOD has tutorial sessions, which may be good papers for learners. There are also demo sessions. It talks about DB design, data processing, graph, stream, spatio-temopral, mining, analytics, in-memory DB, transaction processing, etc. Less NoSQL or distributed engines.
```

__VLDB 2016__

```
    1. topics: (no explicit category, just sampling)
               research track: query processing, event patterns, main-memory column-stores, concurrency control, stream processing,
                               graph processing, query optimization, indexing, in-memory, transactional memory, privacy, distributed join,
                               similarity search, differential privacy, distributed transaction, tensor analytics, big data, Approximate,
                               Spark, RDMA,
               industrial track: Hadoop, Spark, domain-specific languages (DSLs), in-memory, Set queries, bloom filter, RDMA,
                                 distributed in-memory DBMS, Cloud over-booking, Materialized Views, distributed machine learning,
                                 Indexing, Graph Analysis, Query Optimizer, company DB designs, In-Memory,
    2. VLDB talks a lot of in-memory, DB designs, spark, graph, etc
```

__hotCloud 2016__

```
    1. topics: cloud bidding, QoS, interactive debugging, software-defined, serverless, multicast in datacenter,
               coflows, KV-cache, Spark, FPGA, Unikernel, Cross-Cloud systems, public cloud Neutrality, VM Introspection,
               deduplication, container design patterns, baremetal big data, tail at scale,
    2. hotCloud, though the general reference count is low, but it does catch the cloud hot topics. worth to checkout the topics.
```

__ACM TOCS__

```
    1. topics: controlplane OS, network server OS, virtualization, microkernels, kernel, KV store, GPU, Multicore Architectures,
               HW/SW codesigned, SSD, reliability, scheduling, power-efficient, cache, dataplane OS, flash, big data, analytics,
               Voice Personal Asisant,
    2. ACM TOCS talks about topics in computer system designs, or OS designs
```

__ACM TOS__

```
    1. topics: flash, virtualization, manycores, data possession, SMR disk, transaction, persistent memory,
               garbage collecting, RAID, SSD, secure-deletion, memory-mapped IO, NAND, write skew, disk arrays,
               deduplication, sequential and temporal localities, workload, reliability, wear-leveling, predictive,
    2. ACM TOS, the paper comes from different places. It's more like an archive place. We can find a few archived good papers.
```

### Good papers selected to read

During the tour through each top-level conferences 2016, I selected some good papers to read. Here are the reading notes

__ATC 2016__

```
    4. good paper selected to read
        1. Design guidelines for high performance RDMA systems (ATC Best Student Paper)    [2016, 9 refs]
           https://www.usenix.org/sites/default/files/atc16_full_proceedings_interior.pdf#page=445
            1. this paper improve RDMA performance step by step based on sequencer case
               good to read. useful when implementing RDMA based systems. this paper illustrates a lot of backgrounds about RDMA
                1. related to "mises: distributed transactions with consistency, availability, and performance"
                   which uses RDMA heavily and did many optimization
                2. improved performance by 50x
            2. highlights
                1. Large RDMA design space
                    1. operations
                        1. read, wirte, atomic (one-sided)
                        2. send, recv (two-sided)
                    2. transports
                        1. reliable, unreliable
                        2. connected, datagram
                    3. optimizations
                        1. inline, unsignaled, doorbell batching
                        2. WQE shrinking, 0B-RECVs
                2. guidelines
                    1. NICs have multiple processing units (PUs)
                       - Avoid contention, Exploit parallelism
                    2. PCI Express messages are expensive
                       - Reduce CPU-to-NIC messages (MMIOs)
                       - Reduce NIC-to-CPU messages (DMAs)
                3. the sequencer case and its improvments
                    1. very helpful
                    2. Atomics
                       RPC (1 C)
                       +4 Queues, Dbell batching
                       +6 cores
                       +Header-only
                    3. Doorbell batching looks a useful technique
            3. related materials
                1. watching slides and audio recording is helpful to understand the key points
                   https://www.usenix.org/node/196244
        2. SLIK: Scalable Low-Latency Indexes for a Key-Value Store    [2016, 7 refs]
           https://www.usenix.org/system/files/conference/atc16/atc16_paper-kejriwal.pdf
            1. The secondary index design in RAMCloud. It can be used as a reference. The peer system compares can be used as a reference.
               The design is not very impressive. But generally good/ok to read.
                1. this is from the RAMCloud. now they are building the secondary index for the in-memory KV-store
                2. performance: indexed reads in 11 μs and writes in 30 μs. (refer to: memory access ~100ns, SSD random read ~16us)
                                durable updates of indexed objects in 30-36us, ~2x of non-indexed objects
                   index is distributed and throughput linearly scalable
                3. one of the authors, "John Ousterhout", is the author of "The Design and Implementation of a Log-Structured File System", a famous FS fundamental paper
            2. highlights
                1. SLIK secondary index features
                    1. an object can have multiple secondary keys
                    2. distribute index entries independently from their objects rather than colocating them
                        1. it is said for scalability. this design is different from the commonly colocating design.
                        2. Independent partitioning
                            1. index servers (indexlet) can run in separated place, scale independently, and use dedicated servers
                            2. the authors surveyed a lot of DB/store designs to choose the independent partition design
                                1. only index data on the same server: Cassandra [20] and H-Store [19], and the local indexes in Espresso [26] and Megastore [11]
                                2. independent partitioning, but replicate part/all data with each index: the global indexes in DynamoDB [3] and Phoenix [7] on HBase [4]
                            3. metadata & coordination: a place off data path to record which indexlet maps to which server
                                1. so, I think a range query would be to first use consitent-hashing to locate which indexlets hold the start and end key
                                   indexlet should have some sort to link to the next indexlet
                                   next, client queries the metadata server to locate which servers hold the indexlets in the range.
                        3. the queried objects are returned in a streaming approach, instead of collects and return all at once
                            1. this allows query a large set of objects which may not fit into memory
                    3. for consistency (because index and data is not colocated), SLIK avoids distributed transaction
                        1. the authors surveyed a lot of DB/stores to compare consistency design
                            1. some simply permit inconsistencies: CouchDB [2], PNUTS [13], the global indexes for Espresso [26] and Megastore [11], and Tao [12]
                            2. wrap updates in transactions: no example given
                        2. SLIK ensures consistency of
                            1. If an object contains a given secondary key, then an index lookup with that key will return the object
                                1. SLIK uses an ordered write approach.
                                    1. when a data server receives a write request, it first issues requests (to the server(s) with relevant indexlets) for creating index entries corresponding to each of the secondary keys in the new object’s data
                                    2. Then it writes the object and replicates it durably
                                    3. Finally, it asynchronously issues requests (again, to the server(s) with relevant indexlets) for removing old index entries, if this was an overwrite
                                2. However, now it is possible for a client to find index entries that refer to objects that have not yet been written or no longer exist
                                    1. To solve this, we observe that the information in an object is the truth and index entries pointing to it can be viewed as hints
                                        1. The client will fetch each object, and verify whether they matches with the index
                            2. If an object is returned by an index lookup, then this object contains a secondary key for that index within the specified range
                                1. by treating index entries as hints and using objects as ground truth to determine the liveness of index entries
                    3.5. index durable storage
                        1. approaches
                            1. not used: rebuild indexlet from objects. the crash recovery takes too long time
                            2. backup approach: SLIK represents each indexlet B+ tree with a backing table like any other table.
                                                esthe recovery is the same with other tables, which are backed by the KV store.
                                1. traversing a pointer from a node to one of its children requires a lookup in the key-value store
                                   this is slower than just dereferencing a virtual memory address
                                2. the backup approach requires an object to be written durably during each index update
                                   This durable write affects the performance of index updates
                    4. SLIK performs long-running bulk index creation/deletion/migration without blocking normal operations
                        1. Index Creation
                            1. To populate the new index with entries corresponding to the objects already in the underlying table,
                               client level code scans this table, reading each object and then rewriting it
                                1. this looks expensive ..
                            2. Live Index Split and Migration
                                1. SLIK keeps track of the mutations that have occured since the copying started (in a log), and transfers these over as well
                                   A lock is then required only for a short duration of time, while copying over the last mutation
                    5. SLIK uses B+ tree to implement the secondary index
                        1. the nodes hold secondary key => hash of primary key
            3. questions
                1. KV-store is usually used as object store or DB build units. where's the position of RAMCloud?
                    1. for object store, which is usually for high volume video/image data, RAM is not economical
                    2. for in-memory store, most use cases are in-memory analytical DB or high transaction rate DB. but RAMCloud is KV.
                2. bulk create index needs to rewrite all objects.
                    1. this looks expensive ..
                3. "soft update" is a method to ensure consistency constraints, write ordering, but not durability. it runs in memory.
                    1. can "soft update" be used here for RAMCloud's in-memory secondary index systems?

        3. Blockstack: A Global Naming and Storage System Secured by Blockchains    [2016, 12 refs]
           https://www.usenix.org/system/files/conference/atc16/atc16_paper-ali.pdf
            1. analyze the blockchain security and reliability issues, build the naming system based on blockchain
                1. blockstack has 600+ starts on github. this is no easy
                2. the experience shared is worth read
            2. highlights
                1. mentioned a decentralized PKI service built on top of the Namecoin blockchain
                    1. so, PKI can leverage blockchain?
                2. motivation: the needs to binds names with arbitrary values
                    1. alternative DNS-like system
                    2. PKI system
                3. challenges
                    1. Individual blockchain records are typically on the order of kilobytes and cannot hold much data
                    2. Latency of creating and updating records is capped by the blockchain’s write propagation and leader election protocol,
                       and it is typically on the order of 10-40 minutes
                    3. Further, new nodes need to independently audit the global log from the beginning:
                       as the system makes forward progress, the time to bootstrap new nodes increases linearly
                4. this paper is based on authors' experiences from operating this PKI system on the Namecoin network
                    1. they discovered a single miner consistently had more than 51% compute power
                    2. chronic networking issues wiht broadcasting transactions on Namecoin
                    3. merged mining, a popular method to secure smaller blockchains, is currently failing in practice
                       The total compute power dedicated to blockchains is currently insufficient to support multiple secure blockchains
                5. Blockstack designs
                    1. Blockstack separates its control and data plane considerations
                        1. keeps minimal metadata at blockchain
                        2. use external datastores for bulk storage
                    2. Agnostic of the Underlying Blockchain
                    3. virtualchain
                        1. a replicated state machine globally based on the input from the blockchain
                    4. routing layer
                        1. use zone files to store routing information
                        2. user do not need to trust the routing layer, because they can verify hashes in the blockchain
                    5. storage layer
                        1. verify hashes
                    6. pricing
                        1. new names need to pay blockchain money
                6. the analysis of blockchain current problems
                    1. Lesson #1: There is a fundamental tradeoff between blockchain security and introducing new functionality to blockchains.
                    2. Lesson #2: There is currently a significant difference between the network reliability of the largest public blockchain network (Bitcoin) and network reliability of the long tail of alternate blockchains
                    3. Lesson #3: Selfish-mining is not just a theoretical attack, but selfish-mining like behavior can already be observed in production blockchains.
                    4. Lesson #4: Other than the engineering problems, consensus-breaking changes are complicated because of fundamental incentive structures of the parties involved.
                                  System designers have never dealt with consensus-breaking changes before cryptocurrencies; it’s a novel challenge.
                    5. Lesson #5: At the current stage in the evolution of blockchains, there are not enough compute cycles dedicated to mining to support multiple secure blockchains.
            3. questions
                1. if the trust is from verifying hashes from the blockchain, who can be trusted to write the hashes?
                   what if a hijack write?
                2. if new names needs to pay the underlying blockchains,
                   what if you changed the underlying blockchain, and users are forced to change the currency?
```

__OSDI 2016__

```
    3. good papers selected to read
        1. Push-Button Verification of File Systems via Crash Refinement (OSDI Best Paper)    [2016, 2 refs]
           http://homes.cs.washington.edu/~bornholt/papers/yggdrasil-osdi16.pdf
            1. Yggdrasil is a toolkit to verify filesystem correctness by crash refinement. it generates a counterexample if there is a bug.
            2. designs
                1. Yggdrasil input
                    1. a specification of the expected behavior
                    2. an implementation
                    3. consistency invariants indicating whether a file system image is in a consistent state
                2. Yggdrasil provides fully automated reasoning
                    1. To free programmers from such a proof burden
                    2. by novel crash refinement
                        1. any disk state produced by a correct implementation must also be producible by the specification
                        2. Yggdrasil formulates file system verification as an SMT (satisfiability modulo theories) problem
                           and invokes a state-of-the-art SMT solver
                        3. Crash refinement enables programmers to implement file systems by stacking layers of abstraction
                            1. The higher layers can use lower specifications without reasoning about the implementation
                3. discussions/problems
                    1. Yggdrasil reasons about single-threaded code, so file systems written using Yggdrasil do not support concurrency

        2. To Waffinity and Beyond: A Scalable Architecture for Incremental Parallelization of File System Code (NetApp)    [2016, 2 refs]
           https://www.usenix.org/system/files/conference/osdi16/osdi16-curtis-maury.pdf
            1. very good to read. First, data partitioning allows parallel without explicit locks. Second
               The lock-by-scheduling assign threads to (hierarchical) data partitions, and there is no explicit lock.
               The design is also a very clever way to allow minimum engineering effort, continuous evolve a complex codebase,
               and cross-department cowork to update WAFL FS from old to new parallelism.
                1. this paper made a lot of compares with other manycore/multicore parallel designs.
                   it can be used as a study entrance of how to design multicore parallelism in storage systems.
                   it is important to design good parallelism for per node system
                2. the "lock" is done by lock by scheduling, rather than using explicit locks
                    1. see [3] Synchronization via scheduling
                    2. lock-by-scheduling can also be used in database transaction implementation
                       it was told in an old database transaction paper (very famous), although not widely used today.
                        1. "Calvin：一个为分区数据库设计的快速分布式事务框架" is similar to the lock-by-scheduling
                           http://www.jianshu.com/p/43909447728f
            2. key designs
                1. background
                    1. as highend server has more cores, need to modify WAFL filesystem to exploit the parallelism
                    2. the production WAFL filesystem is very complex, need to minimize engineer effort
                       also, if use fine-grained locks, there are too many core changes to handle
                        1. what is achieved in this paper is a minimum effort, continuous evolvable, and efficient
                           design to enable WAFL FS to use multicore parallelism
                2. Classical Waffinity
                    1. user files are partitioned into file stripes.
                       and assigned to affinities, which is the message (request)'s working context
                    2. the message scheduler assign affinities to different threads
                       the scheduler ensure one affinity won't be assigned to two threads
                        1. when an message needs to access more than one affinity
                           it locks the "Serial", i.e. the entire storage
                    3. the general idea is
                        1. use data partitioning, each partition is dynamically assigned (by scheduler) to threads
                        2. when thread is accessing a data partition, it "locks" the affinity, i.e. all related data partitions
                            1. here it is "lock" by scheduling, rather than "lock" by locks
                3. Hierarchical Waffinity
                    1. it has more hierarchies than classical waffinity, so that
                       when a message needs to access multiple affinities, it only needs to lock the ancestors
                    2. another key benefit is, engineering can update code message by message,
                       and continuously optimize messages from bigger affinities to smaller affinities
                        1. this is also favorable for cross department cowork, because they can work on
                           their own messages separately, don't need much interaction
                    3. the scheduler design is also clever. it can be used as a good reference.
                4. Hybrid Waffinity
                    1. fine-grained locking still has much performance improvement from the hierarchical waffinity
                       hybrid waffinity is the way to hybrid fine-grained locking with the previous hierarchical waffinity
                        1. engineering can continuously updated some components to use fine-grained lock
                           and the remaining still use the hierarchical waffinity way
                        2. here the lock-by-scheduling and lock by explicit locking are mixed
            3. related readings
                1. [30] Read copy update, which is widely used in Linux
                   https://www.ibm.com/developerworks/cn/linux/l-rcu/
                    1. better than rwlock and spinlock in the kernel usecases
                
                2. The Multikernel: A new OS architecture for scalable multicore systems    [2009, 772 refs]
                   https://www.sigops.org/sosp/sosp09/papers/baumann-sosp09.pdf
                    1. as referenced in "Waffinity", Recent work has emphasized minimizing the use of shared memory
                       in the operating system in favor of message passing between cores that are dedicated to specific functionality
                    2. highlights (merged other papers, only key points)
                        1. most of these manycore issues come from OS design. may be storage systems won't suffer so much?
                        2. the CPU core count needs to reach 40+ to make the problem significant
                        3. spin lock is a classical case, which one core unlock, incr the ticket, will cache invalid many other cores
                        4. the cache coherent cost is the key reason why message passing is better than memory sharing in manycore condidition
                        5. another pattern is to dedicate certain core to certain service/function, examples are "kernel core" in Corey paper and, the fos paper
                        6. how to implement efficient cross core message passing? The multikernel paper is using URPC[10],
                             a region of shared memory is used as a channel to transfer cache-line-sized messages point-to-point between single writer and reader cores
                           to receive message, a dispatcher is waken up by monitor when message arrives, and it use spin polling on the message cache line, after pre-determined time, it blocks. This can be further improved by [37]
                        7. the essence of understanding concurrency, is to understand cache coherence protocol
                        8. generally, for manycores, per-core data structure, per-core OS kernel, per-core service/function, is the solution. these per-cores communicate by messaging, or copy-on-read.
                           i.e. use space sharing to replace time sharing, as coined in the fos paper
                        9. what does many core mean? from the multikernel paper: 1) systems have more diversity (heterogeneity) 2) cores have more diversity (heterogeneity)
                                                                                 3) core count increase (40+ ~ 1000+) 4) core interconnects matters
                                                                                 5) message passing style costs less than shared memory because of cache coherence cost
                        10. if current filesystems have so many scalability issues (with 40+ cores),
                            how does it affect distributed storage layering on top of it, such as Ceph?

                3. Corey: An Operating System for Many Cores    [2008, 383 refs]
                   https://www.usenix.org/legacy/event/osdi08/tech/full_papers/boyd-wickizer/boyd_wickizer.pdf
                    1. merged to "The Multikernel: A new OS architecture for scalable multicore systems"
                
                4. Factored Operating Systems (fos): The Case for a Scalable Operating System for Multicores    [2009, 321 refs]
                   http://groups.csail.mit.edu/carbon/docs/Wentzlaff.2009.OSR.fos.pdf
                    1. merged to "The Multikernel: A new OS architecture for scalable multicore systems"
                       fos is addressing a 1000+ core model.
                
                5. An Analysis of Linux Scalability to Many Cores    [2010, 325 refs]
                   https://people.csail.mit.edu/nickolai/papers/boyd-wickizer-scaling.pdf
                    1. good to read. merged to "The Multikernel: A new OS architecture for scalable multicore systems"
                    2. video is good: https://www.usenix.org/conference/osdi10/analysis-linux-scalability-many-cores
                    3. the linux scalability problem list summarized is good
                
                6. The Linux Scheduler: a Decade of Wasted Cores    [2016, 19 refs]
                   https://hal.archives-ouvertes.fr/hal-01295194/document
                    1. merged to "The Multikernel: A new OS architecture for scalable multicore systems". interesting paper
                    2. video at: https://www.youtube.com/watch?v=yJcZsSxg4Jo
               
                7. Understanding Manycore Scalability of File Systems    [2016, 1 ref]
                   https://taesoo.gtisc.gatech.edu/pubs/2016/min:fxmark.pdf
                    1. like "The Linux Scheduler: a Decade of Wasted Cores" which is talking about linux kernel
                       linux filesystem is also facing manycore problems. very good to read
                    2. merged to "The Multikernel: A new OS architecture for scalable multicore systems".
                       video at: https://www.usenix.org/node/196193
                    3. the way to test filesystem is interesting. good to read
                    4. the findings are good to read
                    5. related references
                        1. Parallel log-structured writing on NVRAM
                            1. NOVA [FAST16]
                                1. per-CPU inode tables and per-inode logs
                                2. parallel recovery on each CPU and scans the inode tables in parallel
                        2. Scalable file system journaling
                            1. ScaleFS [MIT:MSThesis'14]
                                1. communte interface is the key. and then decouple in-memory and on-disk, and then lock-free.
                                   seqlocks, per-core oplogs. about multiheaded logging, see F2FS.
                                2. related readings
                                    1. The Scalable Commutativity Rule: Designing Scalable Software for Multicore Processors    [2015, 95 refs]
                                       https://people.csail.mit.edu/nickolai/papers/clements-sc.pdf
                                        1. "In any situation where several operations commute—meaning
                                            there’s no way to distinguish their execution
                                            order using the interface—they have an implementation
                                            whose memory accesses are conflict-free during
                                            those operations"
                                                1. good insights
                                        2. "On such processors, a core can
                                            scalably read and write data it has cached exclusively, and
                                            scalably read data it has cached in shared mode. Writing
                                            a cache line that was last read or written by another core
                                            is not scalable"
                                    2. Effective Synchronization on Linux/NUMA Systems
                                       https://www.kernel.org/pub/linux/kernel/people/christoph/gelato/gelato2005-paper.pdf
                                        1. very good material. to the cpu instruction and cacheline level of concurrency details and various lock implementation
                                        2. Intel Itanium CPU guarantees that operations up to 64-bit to aligned memory (8-byte boundary) locations are atomic
                                        3. related readings
                                            1. The Lost Art of C Structure Packing
                                               http://www.catb.org/esr/structure-packing/
                                                1. atomic load/store needs 8-byte alignment variable
                            2. SpanFS [ATC'15]
                                1. based on EXT4, contention on JBD2 and related journal data structures is the hotspot.
                                   the solution is to separate filesystem into more domains, each has independent instance of services.
                
                8. Synchronization via Scheduling: Techniques For Efficiently Managing Shared State    [2011, 38 refs]
                   http://www.ece.ubc.ca/~sasha/papers/pldi-2011.pdf
                    1. static analysis to find task share memory dependencies, and use scheduler to avoid
                       conflicting memory access. the performance is better than STM some sort.
                       target for video games.

        3. Ryoan: A Distributed Sandbox for Untrusted Computation on Secret Data (OSDI Best Paper)    [2016, 2 refs]
           https://www.usenix.org/system/files/conference/osdi16/osdi16-hunt.pdf
            1. protect user secret data while the app is running on cloud provider. both the app and the cloud provider are untrusted.
               Ryoan prevents covert channels. An untrusted application is confined by a sandbox.
               Machine learning on publich cloud and ensure user secret data not leaked is a topic
                1. a good paper and a very thorough confinement from side-channel/convert leaks
            2. highlights
                1. SGX makes sure memory are encrypted.
                   NaCl prevents app to use system calls to encode information.
                2. Ryoan provides a restricted IO model that prevents data leaks
                   (e.g., the output size is a fixed function of input size)
                3. Table 1 summarizes the properties Ryoan imposes on untrusted code
                4. Label-based model for communication
                    1. Modules with confining labels are disallowed to persist data
                5. Data oblivious communication
                6. many more ..
                7. Implementation based on NaCI
            3. related readings
                1. 萨凡纳小镇上的OSDI-2016——SJTU-IPADS的集体见闻（五）
                   http://ipads.se.sjtu.edu.cn/osdi2016/5.html
                    1. good summary
            n. questions
                1. the sandbox relies on Intel SGX, but on the cloud provider's hardware?
```

__SOSP 2015__

```
    3. good papers selected to read
        1. No compromises: distributed transactions with consistency, availability, and performance    [2015, 44 refs]
           http://dl.acm.org/ft_gateway.cfm?id=2815425&type=pdf
            1. very good to read. this can be used as a reference implementation for in-memory distributed transaction database. very fast.
                1. peak throughput of 140M TATP transaction by 90 machines, recover from failure in less than 50ms
                    1. 140M/90 = ~1.6M/sec => 0.625us per transaction.
                        1. how many cores each machine has? 8-core intel E5-2650 CPUs
                        2. and how durability are achieved giving the performance? only write to DRAM, backed by UPS.
                2. the systems that are compared with this paper (FaRM)
                    RAMCloud, Spanner, HERD, Silo
            2. highlights
                1. overview
                    1. FaRM, in-memory distributed system, using RDMA, and NVDRAM (batteried DRAM)
                       transaction with high availability and strict serializability
                        1. These trends eliminate storage and network bottlenecks, but they also expose CPU bottlenecks
                            1. FaRM’s protocols follow three principles for CPU bottleneck
                                1. reducing message counts
                                    1. FaRM reduces message counts by using vertical Paxos [25] with primary-backup replication
                                       and unreplicated coordinators that communicate directly with primaries and backups
                                    2. FaRM uses optimistic concurrency control with a four phase commit protocol
                                       (lock, validation, commit backup, and commit primary)
                                        1. we improved the original protocol by eliminating the messages to backups in the lock phase
                                    3. by piggyback messages with other messages
                                2. using one-sided RDMA reads and writes instead of messages
                                    1. One-sided RDMA uses no remote CPU and it avoids most local CPU overhead
                                    2. FaRM transactions use one-sided RDMA reads during transaction execution and validation
                                    3. coordinators use one-sided RDMA when logging records to non-volatile write-ahead logs at the replicas of objects modified in a transaction
                                    4. Using one-sided RDMA requires new failure-recovery protocols
                                        1. FaRM cannot rely on servers to reject incoming requests when their leases [18] expire because requests are served by the NICs
                                            1. We solve this problem by using precise membership [10] to ensure that machines agree on the current configuration membership
                                               and send one-sided operations only to machines that are members
                                        2. FaRM also cannot rely on traditional mechanisms that ensure participants have the resources necessary to commit a transaction during the prepare phase
                                           because transaction records are written to participant logs without involving the remote CPU
                                            1. Instead, FaRM uses reservations to ensure there is space in the logs for all the records needed to commit
                                               and truncate a transaction before starting the commit
                                            2. In addition, it uses two optimizations to allow transaction execution to proceed in parallel with recovery
                                                1. First, transactions begin accessing data affected by a failure after a lock recovery phase that takes only tens of milliseconds to complete
                                                   rather than wait several seconds for the rest of recovery
                                                2. Second, transactions that are unaffected by a failure continue executing without blocking
                                        3. Besides
                                            1. FaRM also provides fast failure detection by leveraging the fast network to exchange frequent heart-beats
                                            2. and it uses priorities and pre-allocation to avoid false positives
                                3. and exploiting parallelism effectively
                                    1. The failure recovery protocol in FaRM is fast because it leverages parallelism effectively
                                        1. It distributes recovery of every bit of state evenly across the cluster and it parallelizes recovery across cores in each machine
                2. hardwares
                    1. Non-volatile DRAM
                        1. Li-ion batteries are overprovisioned with multiple independent cells,
                           and any battery failure impacts only a portion of a rack
                            1.  using clusters of UPS rather than on-chip supercapacitor to back the DRAM
                        2.  it also preserves the lifetime of the SSD by writing to it only when failures occur
                            1. FaRM stores all data in memory, and considers it durable
                               when it has been written to NVRAM on multiple replicas
                        3. An alternative approach is to use non-volatile DIMMs (NVDIMMs),
                           which contain their own private flash, controller and supercapacitor (e.g., [2]).
                           Unfortunately, these devices are specialized, expensive, and bulky
                        4. The combined additional cost is less than 15% of the base DRAM cost,
                           which is a significant improvement over NVDIMMs that cost 3–5x as much as DRAM
                    2. RDMA networking
                        1. The bottleneck was the NIC message rate
                            1. we showed that on a 20-machine RoCE [22] cluster,
                               RDMA reads performed 2x better than a reliable RPC over RDMA
                               when all machines read randomly chosen small objects from the other machines in the cluster
                3. programming models and architecture
                    1. FaRM provides applications with the abstraction of a global address space that spans machines in a cluster
                        1. The FaRM API [16] provides transparent access to local and remote objects within transactions
                    2. FaRM transactions use optimistic concurrency control.
                       Updates are buffered locally during execution and only made visible to other transactions on a successful commit
                    3. FaRM provides strict serializability [35] of all successfully committed transactions
                    4. The FaRM API also provides lock-free reads, which are optimized single-object read only transactions, and locality hint
                    5. architecture
                        1. Each machine runs FaRM in a user process with a kernel thread pinned to each hardware thread
                        2. FaRM uses a Zookeeper [21] coordination service to ensure machines agree on the current configuration and to store it
                           as in Vertical Paxos [25]
                        3. The global address space in FaRM consists of 2 GB regions, each replicated on one primary and f backups
                            1. Each machine stores several regions
                            2. Objects are always read from the primary copy of the containing region
                            3. Each object has a 64-bit version that is used for concurrency control and replication
                            4. The mapping of a region identifier to its primary and backups is maintained by the CM and replicated with the region
                                1. This centralized approach provides more flexibility to satisfy failure independence and locality constraints
                                   than our previous approach based on consistent hashing [16]
                                    1. It also makes it easier to balance load across machines and to operate close to capacity
                            5. Each machine also stores ring buffers that implement FIFO queues [16]
                            They are used either as transaction logs or message queues
                                1. Each sender-receiver pair has its own log and message queue, which are physically located on the receiver
                                2. The sender appends records to the log using one-sided RDMA writes to its tail
                                3. These writes are acknowledged by the NIC without involving the receiver’s CPU
                4. Distributed transactions and replication
                    1. FaRM integrates the transaction and replication protocols to improve performance
                       FaRM uses primary-backup replication in non-volatile DRAM for both data and transaction logs
                       and uses unreplicated transaction coordinators that communicate directly with primaries and backups
                        1. it still needs a central coordinator for distributed transaction, but the coordinator only holds
                           volatile states, and are looked after by Zookeeper
                        2. because the distributed partial-commit concerns, distributed transaction looks still need central coordinator anyway
                    2. key points
                        1. the fully serializable transaction is done by the central coordinator,
                           coordinating the primaries and backups involved in the transaction
                        2. sending messages are merged with remote writing the logs directly
                        3. lock - lock the object to specific version, if version is changed in the middle, transaction abort
                           validate - read validation on all objects that are read but not written by the transaction
                            1. the validation step should be the difference with snapshot isolation, which only verify written data
                        4. to reduce message count
                            1. piggybacking log truncate messages to other messages
                    3. correctness
                        1. Committed read-write transactions are serializable at the point where all the write locks were acquired,
                           and committed read-only transactions at the point of their last read
                        2. Serializability in FaRM is also strict:
                           the serialization point is always between the start of execution and the completion being reported to the application
                5. failure recovery
                    1. FaRM uses leases [18] to detect failures
                        1. FaRM leases are extremely short
                           Under heavy load, FaRM can use 5 ms leases for a 90-machine cluster with no false positives
                            1. Significantly larger clusters may require a two-level hierarchy
                        2. FaRM uses dedicated queue pairs for leases to avoid having lease messages delayed in a shared queue
                            1. lease manager uses Infiniband send and receive verbs with the connectionless unreliable datagram transport
                        4. Lease renewal must also be scheduled on the CPU in a timely way
                            1. FaRM uses a dedicated lease manager thread that runs at the highest user-space priority
                            5. In addition, we do not assign FaRM threads to two hardware threads on each machine, leaving them for the lease manager
                        5. Finally, we preallocate all memory used by the lease manager during initialization and we page in and pin all the code it uses
                           to avoid delays due to memory management
                6. reconfiguration
                    1. precise membership
                    2. steps:
                        1. Suspect
                        2. Probe: These read probes allow handling of correlated failures that affect several machines
                        3. Update configuration. Remap regions. Send new configuration.
                           Apply new configuration. Commit new configuration.
                7. transaction recovery
                    1.
            3. related materials
                1. watching the video is helpful
                   https://www.youtube.com/watch?v=fYrDPK_t6J8
            4. questions
                1. how to handle the partial-commit problem? If two primaries need to be committed, only one succeeded?
                    1. basically, the primary, and the coordinator, gives the center of decision
                2. what if the primary/backup has committed, but the coordinator doesn't know? message lost
                3. would the central coordinator limit the transaction speed when the cluster gets larger and larger?
                    1. FaRM uses consistent hashing to determine the coordinator for a transaction
                4. data is all in memory. is there any chekcpoint to durable disks?
```

__ASPLOS 2016__

```
    4. good papers selected to read
        1. Sego: Pervasive Trusted Metadata for Efficiently Verified Untrusted System Services    [2016, 4 refs]
           https://www.cs.utexas.edu/~yjkwon/pdf/kwon16asplos-sego.pdf
            1. Securely run app on trusted hypervisor but untrusted guest OS, by using hypercalls to bypass OS and do verification
                1. the paper compare it with heavily with InkTag, and etc. they can be checked out as alternative security solution
                    1. See Table 9 the comparison of techniques: Sego vs InkTag, Overshadow, Haven, Virtual Ghost, MiniBox/TrustVisor, TLR
            2. backgrounds
                1. threat model
                    1. Sego assumes the guest OS can (try to) read or modify any area of a user application’s memory, and intercept or manipulate data en route to an IO device
                       It can modify control flow when a user application returns from a system call or interrupt
                        1. when a user application updates its security settings (stored in a file), the attacker can crash the OS before the changes are made persistent and pretend as if the updates were persisted
                        2. when a user application deletes a file and writes a new version of the file with the same name, the attacker can modify OS file metadata to point to the old version of file, rolling back the file’s state
                2. removing trust from the (guest) operating system
                    1. Sego allow trusted applications to continue to function with a compromised and even overly hostile operating system

            3. designs
                1. In Sego, high-assurance processes (HAPs) make hypercalls to the virtual machine hypervisor to verify the runtime behavior of the operating system
                    1. The HAP, libsego, Sego hypervisor, the block device/hardware, are trusted; the OS is not trusted.
                    2. HAP can verify its own initial code and data by trusted execution / TPM / SGX
                    3. The Sego hypervisor uses hardware nested page tables to ensure privacy and integrity for the HAP’s address space
                    4. Sego uses paraverification, where the hypervisor protects important guest data structures,
                       and the guest clearly communicates its actions and intent to the hypervisor
                        1. the workflow example is at 2.3 libsego section
                        2. when a HAP calls a systemcall, libsego first hypercalls to the hypervisor
                           after allowed, libcall tells trampoline to call the OS.
                           when the systemcall returns, libsego verifies the results, by comparing hypervisor returns and OS returns.
                2. secure pages
                    1. Sego is implemented in a hypervisor,
                       and it protects S-pages in RAM using hardware memory protection (nested page tables)
                       to ensure the untrusted guest OS cannot access them
                    2. There are advantages and disadvantages to the Sego model for secure data.
                        1. See 3.5 Discussion
                        2. Sego’s elimination of encryption and hashing, vs  CPU vendors are improving the performance of cryptographic operations
                            1. whether hardware support for encryption and hashing will erase Sego’s performance gains over an approach like InkTag
                            2. Currently, IO bandwidth is growing faster than encryption/hashing performance
                3. secure files
                    1. The Sego hypervisor and the virtualized block device collaborate to verify access to S-files, and to efficiently recover them
                    2. The Sego hypervisor must track S-file length because it cannot rely on the OS
                    3. recover from OS crashes to prevent data loss
                    4. secure deletion: preventing file rollback attack
                    5. questions
                        1. Sego performance impact on the file operations?
                           Model no-sparsity, no-shrinking, sync-required looks slow
                            1. See 6.4 IO benchmarks
                            2. Sego’s S-file write performance is 17% and 26% slower on disk and SSD respectively

        2. High-Performance Transactions for Persistent Memories    [2016, 10 refs]
           http://ai2-s2-pdfs.s3.amazonaws.com/f4f9/e8d681bdace87c988732d44b61ca163f351f.pdf
            1. This paper analyzed the minimal persist critical path for conflicting transactions on NVRAM,
               compare the existing transaction implementations, and proposed the new way to implement the transaction with less ordering dependencies
                1. in comparison, to enforce write ordering, NOVA is built with Intel's new consistency memory commands,
                   clflushopt, clwb, PCOMMIT, in mind
                2. besides the transaction design, this paper is also a gate to see contemporary works. very good to read.
                3. besides, the formal analysis also showed how to truly verify the correctness of a concurrency program.
                   by ordering constraints. this solved a many year question for me
                    1. besides, this paper also showed how to analyze the reordered performance, i.e.
                        persist critical path vs min persist critical path
            2. highlights
                1. backgrounds
                    1. Implementing transactions on NVRAM requires the ability to constrain the order of NVRAM writes
                    2. Since NVRAM write latencies are expected to be high, minimizing these ordering constraints is critical for achieving high performance
                    3. Recent work has proposed programming interfaces to express NVRAM write ordering constraints to hardware
                    4. For compatibility, some software will continue to access persistent data in NVRAM through a block-based, file system interface
                       However, we expect many programs to access persistent data structures directly in NVRAM using processor loads and stores
                        1. Doing so eliminates the need to maintain separate on-disk and in-memory copies of persistent data,
                           and eliminates the overhead of traversing the file system each time persistent data is read or written
                    5. for NVRAM, minimizing persist dependencies is likely to be essential for performance
                       because NVRAM is slower than DRAM, and to catch up with CPU, it can only relies on
                       techniques such as parallelism, batching, and re-ordering
                2. There are many ways to implement transactions [12],
                   with one basic design choice being which version to log of the data being modified in a transaction:
                    the data before the modification (undo logging [8, 11, 21]),
                    the data after the modification (redo logging [33]),
                    or both (e.g., ARIES [24])
                3. transaction design
                    0. use undo-logging. use lock-basd transaction. it is not MVCC
                    1. Use checksum-based log entry validation [28], to eliminates one persist ordering constraint
                        1. [28] "IRON File Systems"
                    2. Requiring a transaction to hold all locks before executing implies that
                       all the data that can possibly be modified by the transaction is known a priori
                    3. We implement per-thread, distributed logs [32, 33], to avoid the scalability constraints of a centralized log
                4. minimal persist dependencies
                    1. recovery correctness requires the following order relationships
                        prepareLogEntrym ≤p mutateDSm           (1)
                        mutateDSm ≤p commitTransactionm         (2)
                        ∀(m, n) : (unlockDSm ≤v lockDSn) ∧ (Locksm ∩ Locksn 6= φ)
                            prepareLogEntrym ≤p prepareLogEntryn                (3)
                            mutateDSm ≤p mutateDSn                              (4)
                            commitT ransactionm ≤p commitT ransactionn          (5)
                    2. so, the essence of the correctness of a concurrent program resides in the write-ordering
                        1. both in the on-disk case and the in the in-memory case
                        2. the implementation fundamentals then become how to ensure the ordering
                            1. A - The ordering of commit block, data part, journal part
                               C - The ordering of reads and writes of two inter-leaved transactions
                               I - The ordering of reads and writes of two inter-leaved transactions
                               D - The ordering of ack after persist commit
                        3. how to verify the correctness of a concurrent program?
                           testing cannot truly ensure the verify of all cases
                            1. the answer is the formal verification, based on ordering, shown in this paper
                5. Memory persistency models
                    1. Industry has already begun following this course [14]:
                       "Intel Architecture Instruction Set Extensions Programming Reference (319433-023)"
                    2. In currently shipping processor architectures, persist dependencies must be enforced either by using a write-through cache
                       or by explicitly flushing individual cache lines (e.g., using the clflush instruction on x86)
                       Moreover, these flush operations must be carefully annotated with fences to prevent hardware and compiler reorderings
                    3. We briefly summarize four persistency models, on which we build our transaction implementations
                        1. Strict persistency
                            Mia ≤v Mjb ↔ Mia ≤p Mjb    (6)
                        2. Epoch persistency
                            Mia ≤v P Bi ≤v Mib → Mia ≤p Mib    (7)
                        3. Strand persistency
                            1.  each strand behave as if it were a separate thread
                        4. Eager sync
                            1. intel's ISA extension
                            2. st A; CLWB A; SFENCE; PCOMMIT; SFENCE; st B;
                               -> SiA ≤p SiB
                6. transaction implementation
                    1. Synchronous commit transactions (SCT): intuitive but enforces unnecessary persist dependencies
                        1. analyze SCT under epoch, eager sync, and strand persistency (see Figure 2)
                        2. Unfortunately, these four persist barriers create a persist critical path longer than
                           the path that would be possible had the software been able to specify the precise dependencies between all persists (Section 3)
                            1. commitT ransactionm ≤p prepareLogEntryn
                            2. i.e. under epoch persistency, conflicting transactions are serialized
                            3. Moreover, transactions on the same thread are always serialized, even if they do not conflict
                            4. persist critical path under epoch persistency
                                3x for conflicting transactions
                                and 3(x/t) for non-conflicting transactions
                        5. SCT under Eager Sync.
                            1. Eager sync enforces both intra-thread and inter-thread (for conflicting transactions) persist dependencies via sync barriers
                        6. SCT under Strand Persistency
                            1. Strand persistency makes it possible to remove unnecessary persist dependencies between transactions on the same thread
                            2. To achieve high concurrency, our SCT implementation uses per-thread (distributed) logs
                                1. transactions that share no locks may nonetheless conflict if they reuse the same log space
                    2. Deferred commit transaction (DCT): release locks after mutating the data structure to defer commit
                        1. DCT under Epoch Persistency
                            1. spinOnConflicts
                               At commit, a transaction must verify that preceding conflicting transactions have committed
                        2. DCT under Eager Sync
                            1. SB1, ensures that log entries are prepared in order, satisfying Eq. 3
                            2. Cache coherence ensures that at any given time, only the latest values of any conflicting regions of the data structure persist,
                               satisfying Eq. 4
                            3. commitP ersisted bit, spinOnConflict, ensures the commit order, Eq. 5
                            4. We instead rely on sync barriers from a subsequent transaction,
                               implying that both mutateDS and commitT ransaction are persisted concurrently with later transactions
                        3. DCT under Strand persistency
                        4. conclusion
                            1. DCT transaction design reduces the persist critical path and improves performance by up to 50% under epoch and strand persistency
                               and up to 150% under eager sync
            3. questions
                1. is the minimal persist critical path and the corresponding ordering actually correct?
                   it looks like the transaction are all interleaved
                    1. the snapshot isolation, T1’s RS <= T2’s CS <= T1’s CS, actually prohibits this ordering
                    2. is it only recovery correctness? if so, this paper's ordering technique is not very useful, and Intel's may be widely adopted in the end

        3. HCloud: Resource-Efficient Provisioning in Shared Cloud Systems    [2016, 9 refs]
           https://web.stanford.edu/group/mast/cgi-bin/drupal/system/files/2016.asplos.hcloud.pdf
            1. resource provisioning between "reserved" and "on-demand"? HCloud proposes hybrid approach,
               mapping between batch jobs (e.g. hadoop) and latency-critical jobs (e.g. memcached)
               to optimize performance over cost
                1. how to use resources efficiently on cloud, considering the cost and performance and performance stability, is a hot topic
                   the pricing strategies on cloud is not a simple thing
                2. the study on public cloud provisioning strategies, pricing, and performance variability is good
                3. the dynamic policy strategy is good to be used as a reference
                4. this is the same author from Quasar/Paragon scheduling
                    1. the provisioning overheads include job profiling and classification (Quasar)
                5. results: improve performance by 2.1x compared to fully on-demand provisioning,
                            and reduce cost by 46% compared to fully reserved systems
            2. highlights
                1. performance unpredictability on Amazon EC2 and Google Cloud Engine
                2. the challenge: determining how many/what resources to obtain
                                  and how to schedule jobs between reserved and on-demand resources
                3. Provisioning Strategies
                    1. Statically Reserved Resources (SR)
                    2. Dynamic On-Demand Resources (OdF, OdM)
                    3. The Importance of Resource Preferences
                        1. SR may colocate jobs that interfere negatively on the same instance
                4. Hybrid Provisioning Strategies
                    1. Provisioning Strategies
                        1. The first strategy (HF) only uses large instances for on-demand resources, to constrain unpredictability
                        2. The second strategy (HM), uses a mix of on-demand instance types to reduce cost,
                           including smaller instances that experience interference from external load
                        3. the names HF, HM come from OdF, OdM
                    2. Application Mapping Policies
                        1. the findings, P1 - P8
                        2. the dynamic policy
                            1. First, it utilizes reserved resources before resorting to on-demand resources
                            2. Second, applications that can be accommodated by on-demand resources should not delay the scheduling of jobs sensitive to interference
                            3. Third, the system must adjust the utilization limits of reserved instances to respond to performance degradations due to excessive queueing
                            4. Figure 8
                                1. First, a soft limit (experimentally set at 60-65% utilization), below which all incoming jobs are allocated reserved resources
                                    1. Once utilization exceeds this limit, the policy differentiates between jobs that are sensitive to performance unpredictability and insensitive ones
                                        1. The differentiation is done based on the resource quality Q a job needs to satisfy its QoS constraints
                                           and the knowledge on the quality of previously-obtained on-demand instances
                                    2. Once we determine the instance size a job needs (number of cores, memory and storage),
                                       we compare the 90th percentile of quality of that instance type (monitored over time) against the target quality (QT ) the job needs
                                        1. If Q90 > QT the job is scheduled on the on-demand instance
                                        2. otherwise it is scheduled on the reserved instances
                                2. Second, we set a hard limit for utilization, when jobs need to be queued before reserved resources become available
                                    1. At this point, any jobs for which on-demand resources are satisfactory are scheduled in on-demand instances
                                       and all remaining jobs are locally queued
                                    2. An exception occurs for jobs whose queueing time would exceed the instantiation overhead of a large on-demand instance
                                        1. these jobs are instead assigned to on-demand instances
                                3. Third, we adjust the soft utilization limit based on the rate at which jobs get queued
                                    1. If the queued jobs increase sharply, the reserved instances should become more selective in the workloads they accept
                5. the evaluation
                    1. Figure 18 shows why this paper works
                    2. the provisioning overheads include job profiling and classification (Quasar)
                    3. the on-demand instanciation time overhead should be considered

        4. TaxDC: A Taxonomy of Non-Deterministic Concurrency Bugs in Datacenter Distributed Systems    [2016, 9 refs]
           http://people.cs.uchicago.edu/~shanlu/preprint/asplos16-TaxDC.pdf
            1. good taxonomy, findings, and summary of distributed system validation. this paper can be used as reference.
            2. key findings
                1. More than 60% of DC bugs are triggered by a single untimely message delivery that commits order violation or atomicity violation
                2. 53% of DC bugs lead to explicit local or global errors
            3. highlights
                1. the methodology
                    1. Triggering (§3)
                            What is the triggering timing condition?
                            Message arrives unexpectedly late/early
                            Message arrives unexpectedly in the middle
                            Fault (component failures) at an unexpected state
                            Reboot at an unexpected state
                            What are the triggering inputs preconditions?
                            Fault, reboot, timeout, background protocols, and others
                            What is the triggering scope?
                            How many nodes/messages/protocols are involved?
                       Errors & Failures (§4)
                            What is the error symptom?
                            Local memory exceptions
                            Local semantic error messages & exceptions
                            Local hang
                            Local silent errors (inconsistent local states)
                            Global missing messages
                            Global unexpected messages
                            Global silent errors (inconsistent global states)
                            What is the failure symptom?
                            Node downtimes, data loss/corruption, operation failures, slowdowns
                       Fixing (§5)
                            What is the fix strategy?
                            Fix Timing: add global synchronization
                            Fix Timing: add local synchronization
                            Fix Handling: retry message handling at a later time
                            Fix Handling: ignore a message
                            Fix Handling: accepting a message without new computation logics
                            Fix Handling: others
                2. lessons learned
                    1. all types of verification, testing, and analysis approaches must consider fault injections and multiple protocols as input conditions
                    2. Distributed system model checkers (dmck) works by intercepting distributed events and permuting their ordering

        5. ProteusTM: Abstraction Meets Performance in Transactional Memory    [2016, 5 refs]
           https://www.researchgate.net/profile/Diego_Didona2/publication/295135196_ProteusTM_Abstraction_Meets_Performance_in_Transactional_Memory/links/5733b77f08aea45ee838fb3e.pdf
            1. Ease the tuning TM implementations to specific workloads by Collaborative Filtering and Bayesian Optimization.
               This paper can be used as an information entrance for understanding TM backgrounds
            2. highlights
                1. TM problem
                    1. the efficiency of existing TM implementations is strongly dependent on the workloads they face
                    2. the complexity associated with tuning TM contradicts the motivation at its basis
                2. TM background
                    1. TM programming model relies on the abstraction of atomic blocks
                       to demarcate which portions of code of a concurrent application must execute as atomic transactions
                    2. TM abstraction has been implemented in software (STM), hardware (HTM), or combinations thereof (Hybrid TM)
                    3. The number of concurrently active threads is another parameter with a potentially strong impact on TM performance
                    4. A TM contention manager is in charge of arbitrating conflicts
```

__ISCA 2016__

```
    3. good papers selected to read
        1. Dynamo: Facebook's Data Center-Wide Power Management System    [2016, 2 refs]
           http://web.eecs.umich.edu/~hsuch/downloads/papers/pdfs/wu2016dynamo.pdf
            1. datacenter-wide power management. production at Facebook. with power variation characteristics, and background info.
            2. highlights
                1. The design has been used in Facebook production at large scale
                2. backgrounds
                    1. over-provisioning datacenter power problem
                    2. power over-subscription to mitigate the over-provisioning issue, but expose to risks of
                       tripping power breakers due to highly unpredictable power spikes
                    3. the datacenter power delivery graph: servers, racks, RPPs, SBs, and MSBs
                        1. the breaker sustains the overdrawn power for a period of time inversely proportional to the overdraw amount
                        2. they sustain low amounts of overdrawn power for long periods of time
                    4.
                3. contributions
                    1. a characterization of power variation in datacenters
                        1. the higher the power hierarchy level, the smaller the relative power variation, due to load multiplexing
                        2. power variations also depend on the application
                        3. design implications
                            1. Sub-minute power sampling
                            2. 2-minute power capping time
                    2. the design of a datacenter-wide power management system
                        1. scalable communication between controller and controllee
                            1. Dynamo agent on every server. It reads power, executes power capping/uncapping commands
                            2. Dynamo controllers. For every physical power device in the hierarchy that needs protection there is a matching controller instance
                            3. We use the Thrift remote procedure call (RPC)
                        2. application- and service-aware capping actions
                            1. The leaf power controller uses a three-band algorithm to make capping or uncapping decisions
                            2. categorizing Facebook services into predefined priority groups. leaf power controller allocate total-power-cut to servers.
                        3. coordination of multiple controller instances with heterogeneous workload and data dependence
                            1. Power reading and aggregation
                            2. Capping and uncapping decisions
```

__HPCA 2016__

```
    3. good papers selected to read
        1. CATalyst: Defeating Last-Level Cache Side Channel Attacks in Cloud Computing    [2016, 20 refs]
           http://ai2-s2-pdfs.s3.amazonaws.com/96ba/6f5c06850c009e5b77094c0d4532744dedc2.pdf
            1.
            2. backgrounds
                1. LLC is one of the most dangerous shared resources since it is shared by all of the cores in a processor package
                   it allows fine-grained, high-bandwidth, low-noise cross-core attacks
                2. the side channel is to probe the cache line eviction and reload
            3. design
                1. use Intel CAT. pin the sensitive pages on cache line. those cache lines are locked to the VM to be protected
                2. thus, it creates two cache partitions: non-secure partition, managed by hardware; secured partition, managed by VMM software
                3. The guest kernel exposes two system calls to the process, for mapping and unmapping the secure pages
            4. implementation
                1. the basic idea is straightforward but the implementation has many points
                2. at VM-side, the implmentation takes advantage of EPT and implements as a kernel module
```

__NSDI 2016__

```
    3. good papers selected to read
        1. Bitcoin-NG: A Scalable Blockchain Protocol    [2016, 55 refs]
           https://www.usenix.org/conference/nsdi16/technical-sessions/presentation/eyal
            1. use key block (like originally blockchain), and microblocks in-between key blocks. selecting a leader, and make the microblock issuing faster.
               good improvement to the blockchain.
                1. comparably, many current implementation batch multiple user transactions in block blockchain block.
            2. highlights
                1. in abstract
                    1. Bitcoin-NG is a Byzantine fault tolerant blockchain protocol that is robust to extreme churn and shares the same trust model as Bitcoin
                    2. perform large-scale experiments at 15% the size of the operational Bitcoin system
                        1. it looks like bitcoin dev/research never needs to worry about where to test on production
                    3. bitcoin-ng scales
                2. backgrounds
                    1. Bitcoin currently targets a conservative 10 minutes between blocks
                       yielding 10-minute expected latencies for transactions to be encoded in the blockchain
                    2. Bitcoin, fairness suffers, giving large miners an advantage over small miners
                    3. Bitcoin-NG included, are vulnerable to selfish mining by attackers larger than 1/4 of the network
                    4. a good introduction to bitcoin and blockchain
                3. designs
                    1. the key block is like what the blockchain block originally be, but it carries the leader's public key
                       so that only the leader can issue microblocks in its epoch
                    2. the microblocks are issued by leader, and not limitted by the 10min transaction time like the key block
                4. security
                    1. Censorship Resistance: a leader’s absolute power is limited to his epoch of leadership
                    2. Resilience to Mining Power drop: this only happens to key block, only censorship resistance is reduced.
                    3. Double-spending attacks remain a vulnerability in Bitcoin-NG, though to a lesser extent than in Bitcoin.
```

__VLDB 2016__

```
    3. selected good papers to read
        1. Husky: Towards a More Efficient and Expressive Distributed Computing Framework    [2016, 20 refs]
           http://www.vldb.org/pvldb/vol9/p420-yang.pdf
            1. Husky is a unified data mining programming model for in-memory system, a merged compatible to MapReduce, Spark, MPI, Graph, Pregel, Parameter Server
               Husky outperforms Spark 10x in TF-IDF, great performance gain in other cases too.
                1. Husky is an opensource project
                2. this paper has decent programming model design and the detaied implementations.
                   good to read.
                    1. but the problem is, they built another new "MapReduce/Spark/Graph" system.
                       how to merge these systems? how to broad the mature accumulations to the new system?
            2. design
                1. programming model
                    1. objects, object list, global and local objects
                    2. workers, execution,
                    3. message pull, push
                    4. synchronous and asynchronous computation
                2. system design
                    1. Composing Object Interaction Patterns with Husky
                        1. compatible with Pregel, Paramter Server, MapReduce Chain
                    2. Master-Worker Architecture
                        1. synchronous and asynchronous mode
                    3. Consistent Hashing-based Object Management
                        1. use consistent hash to manage the partition between works and objects
                    4. Implementation of primitives
                        1. Compressed Pull
                            1. pass compressed bloom filter rather than individual messages to the requested worker
                        2. Shuffle Combiner
                            1. on the same machine, shuffle messages by going-to which destination
                               then each work only needs to send to one destination with merged messages
                        3. Cache-Aware Optimization
                            1. object list + bitmap and hashmap
                            2. object list: We store the list of objects in contiguous memory spaces for better spatial locality
                               bitmap: to facilitate lazy deletion; object deletion is done by marking the bit
                               hashmap: for dynamic object creation; new objects are appended to the object list and indexed by the hashmap
                            3. Thus, the object list consists of two parts, where the first part is ordered by object ids and the second part indexed by the hashmap
                                1. object lookup consists of a binary search over the ordered part and then a hashmap lookup
                                2. consecutive searches access similar locations exploit cache temporal locality
                                   this brings around 20% than a standard hashmap lookup for app heavily depend on messaging
                    5. fault tolerance
                        1. checkpoint-based recovery
                    6. load balancing
                        1. stragglers
                            1. due to skewed data distribution
                                1. solved by better data partitioning at application layer
                            2. due to heterogeneous machine configurations
                                1. Hadoop approach: config machine capacity factor each
                                2. Husky approach: dynamic load balancing. if > (1 + p) · tavg, reassign partitions
                            3. due to local tasks running in parallel contending for resources
            3. evaluation
                1. there are many cases. covering bulk workload, graph analysis, machine learning, pipeline jobs
```

__ACM TOS__

```
    3. selected good papers to read
        1. Improving Flash-based Disk Cache with Lazy Adaptive Replacement    [2016, 49 refs]
           http://storageconference.us/2013/Papers/2013.Paper.28.pdf
```
