---
layout: post
title: "Recent Paper Reading: Erasure Coding on SMR zones and ZNS SSD, etc"
tagline : "Recent Paper Reading: Erasure Coding on SMR zones and ZNS SSD, etc"
description: "Recent Paper Reading: Erasure Coding on SMR zones and ZNS SSD, etc"
category: "storage"
tags: [storage, paper, erasure-coding]
---
{% include JB/setup %}


EC on SMR drives.

```
1. SMORE: A Cold Data Object Store for SMR Drives (Extended Version)    [2017, 12 refs]
   https://arxiv.org/abs/1705.09701
    1. Append-only. Cross SMR zone EC. Input data is stripped to fill zone.
    2. GC needs to migrate live data out of zone. The EC pattern is essentially stripe/cut object to EC symbols. So no need to rewrite parity.
    3. PMEM in front of HDD to coalescing writes (DRAM backed with battery)
    4. Base EC stripe is called "Segment" (tens MBs), Segment is cut into fragments and written to a "zone set" (placement group). A zone set can pack multiple ECed Segments. GC cleans at the unit of Zone Set.
        1. My questions
            1. Amplification: A deletion of an object -> GC rewrite of Segment -> touches all zones in the Zone Set -> GC rewrite entire Zone Set
    5. What's the GC overhead?
        1. Figure 6 write amplification
        2. But I didn't see a compare to without SMR?

2. Facebook's Tectonic Filesystem: Efficiency from Exascale
   https://www.usenix.org/system/files/fast21-pan.pdf
    1. RS(9,6) intra 72MB block.
    2. Probably: Tectonic stores metadata in KV store ZippyDB. It is not fully in memory. It's sharded.
       So solved the metadata size issue. And metadata services are decoupled into different components.
    3. Bad EN/disk callback to metadata to process data repair, rather than using a GC scan, so solved the GC scan long time issue.
    4. ZippyDB: Data @Scale Seattle- Muthu Annamalai (2015)
       https://www.youtube.com/watch?v=DfiN7pG0D0k
        1. RocksDB and support primary-secondary replication,
        2. sharded. kV store is even easier for doing this.
           I also remember Facebook memcached has rich experience on sharding and replication 

3. Reference-counter Aware Deduplication in Erasure-coded Distributed Storage System    [2018, 3 refs]
   https://par.nsf.gov/servlets/purl/10100342
    1. Variable length chunking would pack chunks in "container". Actually we can split a large container and do intra container EC.
       But this paper does cross chunk EC, so it gets "more" GC problem. And it's not even cross container EC. And this paper thus forces chunk to be fixed sized.
    2. Key solution
        1. Separate chunks with high/low reference count to different EC stripes. It reduces GC.
        2. Pack chunks from the same file to the same EC stripe.
    3. If GC deleted a chunk in one EC stripe, need to regenerate parities. (Broken Stripe)
        No optimization here.

4. Shingled Magnetic Recording (SMR) Drives and Swift Object Storage [2015]
   https://www.openstack.org/videos/summits/tokio-2015/shingled-magnetic-recording-smr-drives-and-swift-object-storage
   https://docs.openstack.org/swift/latest/overview_erasure_code.html
    1. Introducing SMR, but not related to EC.

5. HDFS Erasure Coding
   https://hadoop.apache.org/docs/r3.1.1/hadoop-project-dist/hadoop-hdfs/HDFSErasureCoding.html
    1. Inline EC. Stripe a file into EC fragments.

6. MinIO
   https://resources.min.io/erasure-coding/erasure-coding-primer
    1. MinIO is an object storage. An object is cut into EC fragments

7. AWS S3
   https://assets.amazon.science/07/6c/81bfc2c243249a8b8b65cc2135e4/using-lightweight-formal-methods-to-validate-a-key-value-storage-node-in-amazon-s3.pdf
    1. Didn't find details. The system is append-only. Probably like Azure Storage.
    2. GC rewrite an extent to move out valid data
    3. S3 scans extent to find valid data by reverse lookup index.

8. Google Cloud Storage
   https://docs.cloudera.com/runtime/7.2.10/scaling-namespaces/topics/hdfs-ec-understanding-erasure-coding-policies.html
    1. Plain Reed-Solomon EC. No GC mentioned.

9. StripeFinder: Erasure Coding of Small Objects Over Key-Value Storage Devices    [2020, HotStorage, 4 refs]
   https://www.usenix.org/conference/hotstorage20/presentation/maheshwari
    1. KV SSD.
    2. Packing objects with similar sizes for EC.
    3. But didn't mention GC due to individual object deleted. The goal is instead to reduce metadata byte amplification.

10. Erasure Coding for Small Objects in In-Memory KV Storage    [2017, 39 refs]
    https://arxiv.org/abs/1701.08084
    1. Pack small objects in chunk. Cross chunk EC. Focus on in-memory EC.
    2. GC is by removing an object, and marking it to zero in parity.

11. Ceph
    https://docs.ceph.com/en/latest/rados/operations/erasure-code/#erasure-coding-with-overwrites
    1. Understanding System Characteristics of Online Erasure Coding on Scalable, Distributed and Large-Scale SSD Array Systems    [2017, 7 refs]
       https://arxiv.org/pdf/1709.05365.pdf
        1. The system being evaluated is Ceph. So Ceph is writing in-place, and EC inline on write path. There won't be garbage problem.
    2. Even BlueFS mixes append-only in each OSD, parity can still EC on matched data position. This is because ceph object stripe input address. EC is inline with write.

12. OneFS/Isilon
    https://www.delltechnologies.com/asset/en-us/products/storage/industry-market/h10719-wp-powerscale-onefs-technical-overview.pdf
    https://en.wikipedia.org/wiki/OneFS_distributed_file_system
    1. EC at intra file level. Seems update in-place, cached with NVRAM.

13. Modern Erasure Codes for Distributed Storage Systems
    https://www.snia.org/sites/default/files/SDC/2016/presentations/erasure_coding/Srinivasan_Modern_Erasure_Codes.pdf
    1. Useful if you want to understand major EC players.
    2. Not related to SMR, nor GC with EC.

14. Hierarchical Erasure Coding: Making Erasure Coding Usable
    https://www.snia.org/sites/default/files/SNIA_Hierarchical_Erasure_Coding_Final.pdf
    1. Similar with multi-level LRC. DC zoned.

15. GearDB: A GC-free Key-Value Store on HM-SMR Drives with Gear Compaction    [2019, 40 refs, FAST19]
    https://www.usenix.org/conference/fast19/presentation/yao
    1. not mentioning erasure coding.
       LSM-tree levels same level put to one zone. compaction participants are taken from one zone to ensure clean up one zone.
       SSTables in a zone share similar age and same compaction frequency
       Merge GC and compaction in one run: Out L1, Out L2. Gear: A compaction at L1, will trigger compaction at L2, then cascadingly trigger compaction at L3, ..
    2. redundant cleaning processes on both LSM-trees and HM-SMR drives that harm performance
        1. I.e. LSM-tree GC, LSM-tree compaction, SMR GC. They should be unified
    3. Key designs
        1. Compact Window = 1/k zones of that level
    n. related works
        1. SEALDB: A Set-Aware Key-Value Store on Shingled Magnetic Recording Drives with Dynamic Band    [2018, 5 refs]
           https://ieeexplore.ieee.org/document/8425184
            1. Same first author of "Ting Yao". Not mentioning Erasure Coding
            2. Set - related SSTables are grouped into set. Intra set they share key range. Cross set the key range is disjoint. Each SSTable in Level 1 have its sets in Level 2, each SSTable in Level 2 has its set in Level 3. Set is the compaction unit.
                1. "Multiple random accesses on scattered SSTables are turned into a large sequential one by sets"
                2. My questions
                    1. Similar with "SSTable Guard" concepts?
            2. "Dynamic Band" - In a dynamic band, multiple sets are settled sequentially.
                1. "Dynamic bands deliver a suitable data layout, where a set is always stored in a continuous physical space within a dynamic band. Hence, random write and corresponding auxiliary write amplification is eliminated."

16. Huawei Object Store: Implement Object Storage with SMR based Key-Value Store    [2015, 7 refs, SDC15]
    https://www.snia.org/educational-library/implement-object-storage-smr-based-key-value-store-2015
    1. Object storage based on Swift. 256MB SMR zone. Log-structured. 
    2. How to GC on SMR is future work. Not mentioned EC.
    n. related materials
        1. Huawei plans 20TB SMR drive for OceanStor Pacific storage array [2020]
           https://blocksandfiles.com/2020/06/01/huawei-0ceanstor-pacific-array20tb-smr-drive/
            1. 20TB SMR drives. erasure coding (EC) rather than RAID. Huawei Kunpeng 920 CPUs, 4-core, 64-bit ARM processors. 
            2. Reddit discussion: https://www.reddit.com/r/DataHoarder/comments/gvbc55/huawei_plans_20tb_smr_drive_for_oceanstor_pacific/
                1. "DM-SMR (device mananged-SMR) is bad for RAID, HM-SMR (Host Mangaged-SMR) and HA-SMR (Host aware SMR) can be used in RAID as long as the RAID is aware of the SMR"
                2. It uses Erasure Coding rather than RAID, with a 22+2 EC codec. I didn't find it's HM-SMR, DM-SMR, or HA-SMR
        2. ClusterStor A200: Seagate serves up three layer ClusterStor sandwich - The Register    [2015]
           https://www.theregister.com/2015/11/17/seagates_3layer_clusterstor_sandwich/
           https://www.seagate.com/files/www-content/product-content/xyratex-branded/clustered-file-systems/_shared/datasheets/seagate-clusterstor-a200-datasheet.pdf
            1. single tier, active archive, object store for the ClusterStor product line. The SSUs have SATA shingled magnetic recording (SMR) disk drives
            2. the default supported CS A200 erasure coding schema is 8+2
            3. Mentioned SMR and EC, but not telling how they are combined to work
        3. RAID 4SMR: Shingled Magnetic Recording disks for Mass Storage Systems    [2019, 2 refs, PHD Thesis]
           https://scholarcommons.scu.edu/cgi/viewcontent.cgi?article=1020&context=eng_phd_theses
            1. Building SMR-Aware Disk Arrays
                1. 3+1 EC. Data stores in SMR drives. Parity stores in CMR drives which need overwrite.
                    1. My questions
                        1. It would dedicate disks to store parity. Would it cause load imbalance?
                2. Garbage collection is needed. Which SMR zone has high number of invalid blocks will be tracked.
                3. Data updates are redirected to a dedicated CMR drive D2' (See Figure 6.2). And, parity updates in-place.
                    1. My questions
                        1. So, the D2' serves as a write coalescing cache? Mostly a system will use SSD or PMEM for it
            2. My questions
                1. It's interesting. System compares of cloud storage with RAID on SMR and how to maintain EC stripe updates. 
            n. related materials
                1. RAID 4SMR: RAID Array with Shingled Magnetic Recording Disk for Mass Storage Systems    [2019, 2 refs]
                   https://jcst.ict.ac.cn/fileup/1000-9000/PDF/2019-4-10-9124.pdf
                    1. the shorter version paper. Interesting work.
        4. Spectra Logic's ArcticBlue Storage Promises Longevity, Price of Tape With the Power of Disk    [2015]
           https://www.sportsvideo.org/2015/10/15/spectra-logics-arcticblue-storage-promises-longevity-price-of-tape-with-the-power-of-disk/
            1. Mentioned SMR and EC, both how both is combined to work?
        5. ArcticBlue: BRIDGING NAS AND TAPE WITH NEARLINE OBJECT STORE    [2016]
           https://www.nextplatform.com/2015/10/16/bridging-nas-and-tape-with-nearline-object-store/
            1. "ArcticBlue are interesting in that they make use of disk drives that employ Shingled Magnetic Recording (SMR) techniques to cram about 25 percent more data onto a disk drive and also use a customized variant of the Zettabyte File System (ZFS) to organize data and the triple parity RAID Z3 encoding to distribute data across bands of drives inside of the array. "

17. HiSMRfs: a High Performance File System for Shingled Storage Array    [2014, 72 refs, MSST14]
    https://storageconference.us/2014/Papers/06.HiSMRfs.pdf
    https://storageconference.us/2014/Presentations/Xi.pdf
    1. EC: file split into blocks, a block split into sub-blocks, each sub-block written to one SMR drive, EC cross sub-blocks. I.e. a block is a parity stripe.
        1. Block level EC avoided the need to rewrite a block's parity. But a deleted block pollutes multiple zones due to sub-block.
    2. SMR is supposed to host cold data. Metadata + hot file data are put to SSD.
    3. Write is append only.
    4. Garbage Collection
        1. Deleted file or overwritten blocks cause garbage. 
        2. EC is within a file block, so invalidating a block won't introduce the need to rewrite parity 
        3. My questions
            1. Suppose a file block is deleted. To reclaim the SMR zone, the need rewrite still amplifies from sub-block level to zone level?  

18. ZenFS: ZNS: Avoiding the Block Interface Tax for Flash-based SSDs    [2021, 35 refs, ATC21]
    https://www.usenix.org/conference/atc21/presentation/bjorling
    1. ZenFS
        1. Select zone for RocksDB by SST levels, and separate WAL zones. Write-lifetime hint
        2. limit concurrent compactions due to active zone count limit
        3. Didn't mention erasure coding

19. Pangu SMR: Deployed System: SMRSTORE: A Storage Engine for Cloud Object Storage on HM-SMR Drives    [2023, 2 refs, FAST23, Alibaba]
    https://www.usenix.org/conference/fast23/presentation/zhou
    https://www.youtube.com/watch?v=b_iW94OQmbY
    1. Logged elsewhere. Rewrote storage engine to fit SMR drives, append-only. Didn't mentioned EC.
    2. Related works
        1. GearDB [32], ZenFs [11], SMORE [19], SMRDB [26]
        2. archival-class object storage systems such as Alibaba Archive Storage Service [1] and Huawei Object Store [18].

20. SMRDB: Key-Value Data Store for Shingled Magnetic Recording Disks    [2015, 46 refs, SYSTOR15 Best Paper Award]
    https://www.ssrc.ucsc.edu/pub/pitchumani-systor15.html
    1. No filesystem. LSM-tree based. Fit SSTable and memtable to one SMR zone ("band").
    2. Not mentioned EC

21. Magic Pocket: Dropbox's Exabyte-Scale Blob Storage System
    https://www.infoq.com/articles/dropbox-magic-pocket-exabyte-storage/
    1. Mentioned SMR and EC, but not telling how two are combined
    n. related
        1. How we optimized Magic Pocket for cold storage - Dropbox
           https://dropbox.tech/infrastructure/how-we-optimized-magic-pocket-for-cold-storage
            1. "Magic Pocket's independent region model" .. "a single software bug could wipe out everything no matter how many copies we store"
        2. Hackathon discussion: https://news.ycombinator.com/item?id=19841887

21. Baoquan Zhang: Storage System Designs with Emerging Storage Technologies    [2021, Graduate thesis]
    https://conservancy.umn.edu/bitstream/handle/11299/219314/Zhang_umn_0130E_22072.pdf?sequence=1
    1. Went into details about HM-SMR, HA-SMR, DM-SMR. Not mentioning EC
    n. related works
        1. Ceph BlueFS & RocksDB: The Case for Custom Storage Backends in Distributed Storage Systems    [2020, 9 refs, SAGE WEIL]
           https://www.pdl.cmu.edu/PDL-FTP/Storage/TOS1602-09.pdf
            1. Challenges and Solutions of Running RocksDB on HM-SMR Drives
            2. Overwriting Erasure-coded Data
                1. My questions
                    1. I read the paper, but where it tells how this overwriting EC is handled on SMR? Seems only RocksDB (metadata) on SMR is evaluated 
            3. Standalone RocksDB on HM-SMR Drive Evaluation
                1. Ceph with RocksDB Running on HM-SMR Drive Evaluation
                    1. "we always store data on a CMR drive and alternate storing metadata on a CMR drive, on a DM-SMR drive, and on an HM-SMR drive"
        2. HORISON: Storage Outlook: A Look Ahead at the Opportunities and Challenges Facing the Data Storage Industry    [2016]
           https://horison.com/cache/uploads/2016/08/storage-outlook-horison-information-strategies-2016.pdf
            1. Mentioned SMR and EC, but not telling how they are combined

22. Michael Tsai Blog: How Is Amazon Glacier Implemented?    [2014]
    https://mjtsai.com/blog/2014/04/27/how-is-amazon-glacier-implemented/
    1. No much details revealed

23. Getting In The Zone: btrfs on SMR HDDs and NVMe ZNS SSDs - Damien Le Moal & Johannes Thumshirn    [2021]
    https://www.youtube.com/watch?v=6s7BJrT00pg
    1. Btrfs is copy-on-write, uses append-only to support SMR or Zoned Block Devices (including ZNS SSD)
    2. Not mentioning EC. OK .. if it's a local FS then EC shouldn't be mentioned here

```

SSD flash internally has has "erasure coding" alike thing to protect data. GC or overwrite happens at page/block level, so flash shares the similar problem of EC on SMR.

```

1. Erasure Coding for Flash Devices and Systems    [2015, 0 refs, FlashSummit15]
   https://www.flashmemorysummit.com/English/Collaterals/Proceedings/2015/20150810_PreconfA_Hetzler.pdf
    1. Flash NRRE and parity unit
    2. PMDS Codes
    3. GC and EC again amplification not mentioned

2. What are the "redundant bytes" added to every page of this NAND flash?
   https://electronics.stackexchange.com/questions/637358/what-are-the-redundant-bytes-added-to-every-page-of-this-nand-flash
    1. A 2048 page has an additional 128 byte for ECC, metadata (logical section number, count of page writes, timestamp, etc)

3. NAND Flash Media Management Algorithms    [2019, FlashSummit]
   https://www.flashmemorysummit.com/Proceedings2019/08-05-Monday/20190805_PreConfG_Pletka.pdf
    1. Hard decision ECC decoding
       Plus, RAID-like parity among different dies (cross block parity)
    2. But didn't mention how to update the cross block parity

4. Write Amplification due to ECC on Flash Memory or Leave those Bit Errors Alone    [2012, FlashSummit]
   https://www.flashmemorysummit.com/English/Collaterals/Proceedings/2012/20120823_S301C_Moon.pdf
    1. Flash Memory Protection Scheme
        1. Error Correcting Code (ECC)
        2. Parity protection (RAID)
    2. Main sources of W.A.
        1. Writing corrected data back in ECC recovery
        2. Parity update of RAID
    3. The slides only address WA to ECC, not Parity update

5. DON'T LET RAID RAID THE LIFETIME OF YOUR SSD ARRAY    [2013, FlashSummit]
   https://www.usenix.org/sites/default/files/conference/protected-files/moon_hotstorage13_slides.pdf
    1. Write Amplification due to Parity Protection (RAID5)
    2. An analysis comparing parity protection vs striping (RAID0)

6. Building Flexible, Fault-Tolerant Flash-based Storage Systems    [90 refs, 2009]
   https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=85487ca09999d24c4f3d5c7148a8e1686d922147
    1. Erasure Coding Across Devices
        1. An EC stripe (block group) has a parity map, which tells each block in the EC group
        2. We erase the block in it before the first write is applied to the group
        3. parity updates are staged in cache, until dependent data is written to flash.
            1. My questions
                1. So, it looks like RAID but works on flash pages. Overwriting a block is allowed but redirected by block group tracking.

7. Improving the Reliability of Next Generation SSDs using WOM-v Codes    [2022, 4 refs, FAST22]
   https://www.usenix.org/conference/fast22/presentation/jaffer
    1. This code enables the recording of two bits of information in three cells twice, ensuring that in both writes the cells change their value only from 0 to 1

8. LightOS GFTL: A Global FTL Architecture to Drive Multiple SSDs    [2019, FlashSumit19]
   https://www.flashmemorysummit.com/Proceedings2019/08-06-Tuesday/20190806_ARCH-101-1_Shertman.pdf
    1. Erasure Coding: Default: RAID5 -like parity with append-only (no RMW)

n. Summary
    1. It seems the erasure coding inside flash doesn't need to be cross block. Unlike distributed storage, the EC doesn't need to be cross failure domain.
       Inside flash, it can be simply an ECC attached to each page. Extra bits is needed by the storage overhead is comparable with supposed cross block parity.
    2. There are cross block protection in flash, it's usually called "parity", and it's in the context of RAID. If RAID, then it's in the topic of distributed storage that we are familiar with.
    3. ChatGPT: As I mentioned earlier, erasure coding isn't typically applied at the SSD device level; instead, it's used in larger distributed storage systems. However, techniques like error correction codes (ECC) and garbage collection are crucial for SSDs.
       https://chat.openai.com/share/e39ca3c4-2a95-484c-8343-e59ff5b100fe
    4. Note, RAID is different. RAID can be adapted to work on SMR. If we take EC at block level, and allows overwriting, then "EC again after GC" seems no longer a problem. The problem degenerates to the classic partial write on an EC stripe.
       See RAID 4SMR: RAID Array with Shingled Magnetic Recording Disk for Mass Storage Systems: https://jcst.ict.ac.cn/fileup/1000-9000/PDF/2019-4-10-9124.pdf

```

EC on ZNS SSD

```
1. Adopting Zoned Storage in Distributed Storage Systems    [2020, 4 refs, Doctor Thesis]
   http://reports-archive.adm.cs.cmu.edu/anon/2020/CMU-CS-20-130.pdf
    1. Skylight: a novel technique to reverse engineer the translation layers of modern hard disk drives and demonstrate the high garbage collection overhead of the translation layers
    2. ext4-lazy: an extension of the popular ext4 file system, leveraging the insight from Skylight. DM-SMR.
    3. Ceph BlueStore extended: Make it work on zoned devices. zone interface eliminates in-device garbage collection when running RocksDB.
        1. Overwrite of Erasure Coded Data
            1. But seems didn't mention how EC is done on ZNS SSD exactly? Seems it mainly targets RocksDB on ZNS.

2. SSDFS: flash-friendly file system with highly optimized GC activity, diff-on-write, and deduplication    [2022, ByteDance]
   https://elinux.org/images/8/84/SSDFS_talk_v.3.pdf
   https://www.youtube.com/watch?v=x5gklnkvi_Q
   https://www.indiegogo.com/projects/ssdfs-zns-ssd-native-file-system#/
    1. Why yet another file system?
        1. NILFS2 vs F2FS vs bcachefs vs SSDFS
    2. SSDFS - ZNS SSD ready
        1. says "Erasure coding support", but how exactly?
        2. compression + delta-encoding + compaction scheme. What is "delta-encoding" exactly?

3. RAIZN: Redundant Array of Independent Zoned Namespaces    [2023, 1 refs]
   https://huaicheng.github.io/p/asplos23-razin.pdf
   https://www.youtube.com/watch?v=RQvqnWr4KdgASPLOS23
    1. RAIZN, a logical volume manager that exposes a ZNS interface and stripes data and parity across ZNS SSDs
        1. RAIZN behaves like software RAID. arranges data into parity coded stripes, and distributes it across the underlying devices
        2. RAIZN's novelty stems from exposing a logical ZNS volume operating atop physical ZNS devices that do not support overwrites
        3. garbage collection: only the metadata.
    2. My questions
        1. So, it's like an ZNS interfaced RAID. Then GC is still in the hand of upper layers

4. A new LSM-style garbage collection scheme for ZNS SSDs    [2020, 25 refs]
   https://www.usenix.org/conference/hotstorage20/presentation/choi
    1. LSM ZGC design
        1. GC based on a segment unit, rather than an entire zone. Finer gain benefits throttling, and do pipelining
            1. My questions
                1. it doesn't seem necessarily to GC by segment to implement throttling and pipelining.
        2. segregate hot and cold data into different zones while doing GC
        3. Instead of reading only invalid blocks, GC reads all blocks
            1. In implementation, GC only read full data when valid data ratio is high enough. Otherwise, it reads full data by sending 16 parallel requests over the full 2MB range
            2. The paper argues reading full data can benefit from the internal parallelism in SSD
```
