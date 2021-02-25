---
layout: post
title: "A Summary on SSD & FTL"
tagline : "A Summary on SSD & FTL"
description: "A Summary on SSD & FTL"
category: "SSD"
tags: [SSD, FTL, summary]
---
{% include JB/setup %}

Summary of study, also put to respective WeiChat articles.

  * [SSD & FTL Bottom-up (P1)](https://mp.weixin.qq.com/s/2iM-Q63jvtPYCSL-N-AX-w) [PDF](/images/ssd-ftl-bottom-up-p1.pdf)
  * [SSD & FTL Bottom-up (P1)](https://mp.weixin.qq.com/s/RrefVitT--BIb49yax_Hvw) [PDF](/images/ssd-ftl-bottom-up-p2.pdf)
  * [SSD & FTL Bottom-up (P1)](https://mp.weixin.qq.com/s/Y37GLELxtaUxoUBKW0EmLQ) [PDF](/images/ssd-ftl-bottom-up-p3.pdf)

The brief summary to book my SSD and FTL knowledge collected.

__SSD Market Growth__

The almost 100% growth speed is why everybody is looking at SSD.

  * Source: [TMR Analysis \(August 2015\)](http://www.legitreviews.com/market-research-shows-ssds-sales-are-going-to-greatly-increase_172791)

![SSD Market TMR Analysis](/images/ssd-market-tmr.png "SSD Market TMR Analysis")

  * Source: [TrendFocus \(2016\)](http://www.anandtech.com/show/10706/market-trends-q2-2016-ssd-shipments-up-41-percent-yoy)

![SSD Market TrendFocus](/images/ssd-market-trendfocus.png "SSD Market TrendFocus")

__SSD Chip Structure__

Flash chip

  * 1 Chip/Device -> multiple DIEs
  * 1 DIE -> several Planes
  * 1 Plane -> thousands of Blocks
      * Planes can be parallelly accessed
  * 1 Block -> hundreds of Pages
      * Block is the unit of erasing
  * 1 Page -> usually 4 or 8 KB + hundred bytes of hidden space
      * Page is the unit of read and write
  * Cells: SLC, MLC, TLC: basic bit storage unit
      * Max P/E cycles: MLC from 1500 to 10,000; SLC up to 100,000

References

  * Alanwu's blog: [\[1668609\]](http://alanwu.blog.51cto.com/3652632/1668609) [\[1544227\]](http://alanwu.blog.51cto.com/3652632/1544227)
  * [Storage architecture](http://meseec.ce.rit.edu/551-projects/fall2010/1-4.pdf)

__MLC vs eMLC vs SLC__

Cell comparison

  * SLC - Expensive. Fast, reliable, high P/E
  * MLC - Consumer grade. cost 2- 4x less than SLC, 10x less P/E than SLC, lower write speed, less reliable
  * eMLC - Enterprise (grade) MLC. Better controller to manage wear-out and error-correction.
  * TLC - Championed by Samsung

[Flash Reliability in Production: The Expected and the Unexpected \(Google\)](https://www.usenix.org/node/194415) [2016, 14 refs]

  * "We see no evidence that higher-end SLC drives are more reliable than MLC drives within typical drive lifetimes" (not cells)

References

  * [MLC vs. eMLC vs. SLC vs. TLC](http://www.tomsitpro.com/articles/flash-data-center-advantages,2-744-2.html)

__Latency Numbers__

[Latency Numbers Every Programmer Should Know](https://people.eecs.berkeley.edu/~rcs/research/interactive_latency.html)

  * Cache access: ~1ns
  * Memory access: ~100ns
  * SSD access: ~10μs
  * Disk access: ~10ms
  * Datacenter net RTT: ~500μs

![Latency Numbers Every Programmer Should Know 2016](/images/latency-numbers-2016.png "Latency Numbers Every Programmer Should Know 2016")

__SSD Interfaces__

SSD Interfaces (not including NVRAM's)
 
  * SATA/SAS
      * Traditional HDD interface, now mapped to SSD
  * PCIe
      * SSD is so fast, SATA/SAS bus speed is not enough.
      * Attach SSD directly to PCI bus. Much faster.
  * NVMe
      * Improved from the PCIe. The native interface for flash media.

References
  
  * [What’s the difference between SATA, PCIe and NVMe](http://www.userbenchmark.com/Faq/What-s-the-difference-between-SATA-PCIe-and-NVMe/105)
  * [Clarification of terminology: SSD vs M.2, vs PCIe vs. NVMe](http://www.tomshardware.com/answers/id-2776112/clarification-terminology-ssd-pcie-nvme.html)

__FTL - Flash Translation Layer__

FTL functionalities
  
  * Interface Adaptor
      * Map flash interface to SCSI/SATA/PCIe/NVMe interface
  * Bad Block Management
      * SSD records its bad blocks at first run
  * Logical Block Mapping
      * Map logical addresses with physical addresses
  * Wear-levelling
      * Save the P/E cycles
  * Garbage Collection
      * Manage garbage collection because of the NAND P/E logic
  * Write Amplification
      * Avoid writing more actual data than the user input

References
  
  * [Understanding FTL](https://flashdba.com/2014/09/17/understanding-flash-the-flash-translation-layer/)
  * Alanwu's blog: [\[1427101\]](http://alanwu.blog.51cto.com/3652632/1427101)

__FTL - Hybrid-level Mapping__

Logical to physical address mapping
  
  * Block-level mapping: too coarse
  * Page-level mapping: too much matadata
  * Hybrid-level mapping: what is used today

[A Space-efficient Flash Translate Layer for Compactflash Systems](https://pdfs.semanticscholar.org/e0a1/546f56b68ebfcc5f7237c073d6186188f192.pdf) [2002, 988 refs]
  
  * The beginning paper of hybrid-level mapping FTL
  * The key idea is to maintain a small number of log blocks in the flash memory to serve as write buffer blocks for overwrite operations

References
  
  * Alanwu's blog: [\[1427101\]](http://alanwu.blog.51cto.com/3652632/1427101)

![FTL Hybrid-level mapping](/images/ftl-hybrid-mapping-alanwu.jpg "FTL Hybrid-level mapping")

__FTL - Hybrid-level Mapping (More 1)__

[A reconfigurable FTL (flash translation layer) architecture for NAND flash-based applications](http://csl.skku.edu/papers/tecs08.pdf) [2008, 232 refs]
  
  * Good paper to introduce flash structures and detailed concepts
      * "As an approach that compromises between page mapping and block mapping, ... A hybrid mapping scheme ... was first presented by Kim et al. [2002]. The key idea ...
      * To solve this problem of the log block scheme, the fully associative sector translation (FAST) scheme has been proposed [Lee et al. 2006] ...
      * Chang and Kuo [2004] proposed a flexible management scheme for largescale flash-memory storage systems ...
      * Kang et al. [2006] proposed a superblock-mapping scheme termed “N to N + M mapping.” ... In this scheme, a superblock consists of ..."

__FTL - Hybrid-level Mapping (More 2)__

[A Log Buffer-Based Flash Translation Layer Using Fully-Associative Sector Translation](http://csl.skku.edu/uploads/ICE3028S11/fast-tecs07.pdf) [2007, 778 refs]
  
  * Usually called as FAST. Improved from "A Space-efficient Flash Translate Layer for Compactflash Systems"
  * Key ideas
      * In FAST, one log block can be shared by all the data blocks.
      * FAST also maintains a single log block, called sequential log block, to manipulate the sequential writes

![Flash FTL using FAST](/images/flash-ftl-fast.png "Flash FTL using FAST")

__FTL - Hybrid-level Mapping (More 3)__

[A Superblock-based Flash Translation Layer for NAND Flash Memory](http://csl.skku.edu/papers/emsoft06.pdf) [2006, 368 refs]
  
  * The flash is divided into superblocks, each superblock consist of N data block + M log block
      * In this way, set-associative is fully configurable, as from what FAST discussed
      * Garbage collection overhead is reduced up to 40%
      * Exploit "block-level temporal locality" by absorb writes to the same logical page into log block
      * Exploit "block-level spatial locality" to increase storage utilization by that several adjacent logical blocks share a U-block

__FTL - Hybrid-level Mapping (More 4)__

[LAST: Locality-Aware Sector Translation for NAND Flash Memory-Based Storage Systems](http://yourcmc.ru/wiki/images/d/d2/02-lee-last-usenix09.pdf) [2008, 298 refs]
  
  * Improved from "A Log Buffer-Based Flash Translation Layer Using Fully-Associative Sector Translation" and "A Superblock-based Flash Translation Layer for NAND Flash Memory"
  * Key ideas
    * LAST partitions the log buffer into two parts: sequential log buffer and random log buffer
    * The sequential log buffer consists of several sequential log blocks, and one sequential log block is associated with only one data block
    * Random log buffer is partitioned into hot and cold partitions. By clustering the data with high temporal locality within the hot partition, we can educe the merge cost of the full merge

__FTL - Hybrid-level Mapping (More 5)__

Implications
  
  * Although FTL does remapping, sequential writes still benefits SSD because it reliefs GC (more switch merges)

Image from: [FTL LAST](http://yourcmc.ru/wiki/images/d/d2/02-lee-last-usenix09.pdf)

![FTL GC Merge Operations](/images/ftl-gc-merge.png "FTL GC Merge Operations")

__Bypassing FTL - Open-channel SSD__

Though FTL is powerful and __dominatedly__ adopted, there are people who try to get rid of it
  
  * No nondeterministic slowdowns by background tasks of FTL
  * Reduce the latency introduced by FTL
  * Application customized optimization for flash operation

Open-channel SSD
  
  * SSD hardware exposes its internal channels directly to application. No remapping by FTL
  * [An Efficient Design and Implementation of LSM-Tree based Key-Value Store on Open-Channel SSD](http://www.ece.eng.wayne.edu/~sjiang/pubs/papers/wang14-LSM-SDF.pdf) (Baidu) [2014, 25 refs]
      * Optimize the LSM-tree-based KV store (based on LevelDB) on Open-channel SSD. 2x+ throughput improvement.
      * [SDF: Software-Defined Flash for Web-Scale Internet Storage Systems](https://pdfs.semanticscholar.org/6197/7858b3eea4f5a6d81393301e7298ade7a2d8.pdf) (Baidu) [2014, 67 refs]
          * SSD (with FTL) bandwidths ranges from 73% to 81% for read, and 41% to 51% for write, of the raw NAND bandwidths
  * [Optimizing RocksDB for Open-Channel SSDs](http://www.slideshare.net/JavierGonzlez49/optimizing-rocksdb-for-openchannel-ssds)
      * Control placement, exploit parallelism, schedule GC and minimize over-provisioning, control IO scheduling
  * Linux kernel integration
	  * [LightNVM](https://en.wikipedia.org/wiki/Open-channel_SSD)

[Application-Managed Flash](http://people.csail.mit.edu/ml/pubs/fast2016.pdf) [2016, 6 refs]
  
  * Expose the block IO interface and the erase-before-overwrite to applications

__Design Shifts - Seastar__

ScyllaDB Seastar
  
  * Original designed to build ScyllaDB, a 10x faster Cassandra. Now opensourced
  * FCP async programming: future, promise, completion. Sharded application design.
  * User-space TCP/IP stack, bypassing the kernel. By Intel DPDK
  * User-space storage stack, bypassing the kernel. By Intel SPDK (WIP)

Rationales Behind
  
  * SSD is so fast, that storage software stack needs to be improved. 
      * - Better async programming. FCP. Lockless. Cpu utilization.
  * SSD is so fast, that Linux kernel is too slow.
      * - Bypass it.
  * The same ideas are borrowed for NVM too

Image: [Tradition NoSQL vs ScyllaDB architecture](https://adtmag.com/articles/2015/09/23/scylladb-cassandra.aspx)

![Tradition NoSQL vs ScyllaDB Architecture](/images/traditional-vs-scylladb.png "Tradition NoSQL vs ScyllaDB Architecture")

References
  
  * [Seastar / ScyllaDB, or how we implemented a 10-times faster Cassandra](http://www.slideshare.net/TzachLivyatan/seastar-scylladb-or-how-we-implemented-a-10times-faster-cassandra)
  * [Linux Kernel IO Stack](https://www.thomas-krenn.com/en/wiki/Linux_Storage_Stack_Diagram)

__Design Shifts - DSSD__

DSSD - EMC Rack-scale Flash Appliance
  
  * Kernel bypass, directly connect to DSSD appliance
      * Similar idea to Seastar

References
  
  * [DSSD D5 Data Access Methods](https://www.emc.com/collateral/data-sheet/h14868-ds-dssd-d5-data-access-tech-brief.pdf)
  * [Software Aspects of the EMC DSSD D5](https://www.emc.com/collateral/white-papers/h14907-wp-dssd-d5-software-aspects.pdf)
  * [DSSD bridges access latency gap with NVMe fabric flash magic](https://www.theregister.co.uk/2015/08/18/dssd_nvme_fabric_flash_magic/)

__Design Shifts - Content-based Addressing__

Content-based Addressing
  
  * Data placement is determined by data content rather than address.
  * Leverage SSD random-write ability. Natural support for dedup.
  * Adopted in EMC XtremIO and SolidFire

Image: [SSD storage array tradeoffs by SolidFire](https://www.eigenmagic.com/2014/06/13/solidfire/)

![SSD Storage Array Tradeoffs by SolidFile](/images/solidfire-product-tradeoff.png "SSD Storage Array Tradeoffs by SolidFile")

References
  
  * [XtremIO Architecture](https://www.youtube.com/watch?v=lIIwbd5J7bE) (The debate is famous)
  * [Comparing Modern All-Flash Architectures](https://www.youtube.com/watch?v=AeaGCeJfNBg) - Dave Wright, SolidFire
  * [Coming Clean: The Lies That Flash Storage Companies Tell with Dave Wright of NetApp/SolidFire](https://www.youtube.com/watch?v=35KNCOYguBU)

__Design Shifts - LSM-tree Write Amplification__

[WiscKey: Separating Keys from Values in SSD-conscious Storage](https://www.usenix.org/conference/fast16/technical-sessions/presentation/lu) [2016, 7 refs]
  
  * In LSM-tree, the same data is read and written multiple times throughout its life, because of the compaction process
      * Write amplification can be over 50x. Read amplification can be over 300x.
      * Many SSD-optimized key-value stores are based on LSM-trees
  * WiscKey improvements
      * Separates keys from values to minimize I/O amplification. Only keys are in LSM-tree.
      * WiscKey write amplification  decreases quickly to nearly 1 when the value size reaches 1 KB. WiscKey is faster than both LevelDB and RocksDB in all six YCSB.

__Design Shifts - RocksDB__

RocksDB is well-known to be an SSD optimized KV store
  
  * It is developed based on LevelDB, opensourced by Facebook. Optimized in many aspects for SSD.
  * [RocksDB: Key-Value Store Optimized for Flash-Based SSD](https://www.percona.com/live/data-performance-conference-2016/sessions/rocksdb-key-value-store-optimized-flash-based-ssd)
      * Why is it flash-friendly? 
          * Space, Read And Write Amplification Trade-offs. Optimize compaction process.
          * Low Space Amplification
          * High Read QPS: Reduced Mutex Locking
          * High Write Throughput: Parallel Compaction; Concurrent Memtable Insert
  * [Universal compaction](https://github.com/facebook/rocksdb/issues/1014): "It makes write amp much better while increasing read amp and space amp"
      * This is RocksDB's famous feature

__Design Shifts - Ceph BlueStore__

Ceph BlueStore
   
   * Develop the single purpose filesystem, BlueFS, to manage data directly on raw block devices
   * Use RocksDB to store the object metadata and WAL. Better management for SSD.
   * Faster software layer to exploit the high performance of SSD. Similar thoughts from Seastar

References
   
   * [Ceph存储引擎bluestore解析](http://www.sysnote.org/2016/08/19/ceph-bluestore/)
   * [Ceph Jewel Preview](https://www.sebastien-han.fr/blog/2016/03/21/ceph-a-new-store-is-coming/)
   * ["System Notes" blog](http://www.sysnote.org/)
   * [BlueStore slideshare](http://www.slideshare.net/sageweil1/bluestore-a-new-faster-storage-backend-for-ceph-63311181)

__Design Shifts - RAID 2.0, FlashRAID__

Many design points to adapt for SSD
  
  * Failure model, write amplification, random writes, RISL (Random Input Stream Layout), zero-fill, trim, partial-stripe writes, ...

References
  
  * Alanwu's blog: [\[1876942\]](http://alanwu.blog.51cto.com/3652632/1876942) [\[1859361\]](http://alanwu.blog.51cto.com/3652632/1859361) [\[1722581\]](http://alanwu.blog.51cto.com/3652632/1722581) [\[1683079\]](http://alanwu.blog.51cto.com/3652632/1683079) [\[1682091\]](http://alanwu.blog.51cto.com/3652632/1682091) [\[1430288\]](http://alanwu.blog.51cto.com/3652632/1430288)
  * [SSD failure model](http://www.storagesearch.com/ssd-data-art.html)

Image from: [SSD failure model](http://www.storagesearch.com/ssd-data-art.html)

![SSD Failure Bathtub](/images/ssd-reliability-bathtub.png "SSD Failure Bathtub")

__Incoming New Generation__

Intel 3D XPoint
  
  * Announced in mid-2015 with claims of ten times reduced latency compared to flash
  * [References](http://www.userbenchmark.com/Faq/What-is-3D-XPoint-and-how-fast-is-it/106)

NVMe over Fabrics
  
  * A bit like the flash version of SCSI over SAN
  * DSSD's bus is like a customized verion of NVMe over Fabrics
  * [References](https://www.snia.org/sites/default/files/SDC15_presentations/networking/WaelNoureddine_Implementing_%20NVMe_revision.pdf)

NVDIMM
  
  * Attach flash to the memory bus. Even faster.
  * References
      * [Wiki NVDIMM](https://en.wikipedia.org/wiki/NVDIMM)
      * [NOVA paper](https://www.usenix.org/conference/fast16/technical-sessions/presentation/xu)

__Paper & Material Summary__

References
  
  * [Reading Fast16 Papers](http://accelazh.github.io/storage/Reading-Fast16-Papers)
  * FAST summits: [FAST16](https://www.usenix.org/conference/fast16)
  * [Flash Memory Summit](http://www.flashmemorysummit.com/)
  * [Storage Tech Field Day](http://techfieldday.com/)
  * [Alanwu's blog](http://alanwu.blog.51cto.com/)
  * [MSST](http://storageconference.us/) - Massive Storage Systems and Technology
  * OSDI - Google likes to publish new systems here: [OSDI16](https://www.usenix.org/conference/osdi16)

__Hints for Reading Papers__

Check the "Best Paper Award" on each conferences
  
  * On top-level conferences, they are best of the best

Search for papers with very high reference counts
  
  * E.g. 1800+ for industry reformer, 900+ for breakthrough tech, 200+ for big improvement tech.
  * 10+ refs on the first year indicates very good paper

Search for papers backed by industry leaders
  
  * E.g. Authored by/with Google, Microsoft, etc

Some papers have extensive background introduction
  
  * It is very good for understanding a new technology

You may even hunt on college curriculums. They help grow solid understanding.
  
  * E.g. From [where Ceph's author graduates](https://users.soe.ucsc.edu/~sbrandt/290S/)
