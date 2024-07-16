---
layout: post
title: "Recent Notes for Paper Reading: Cloud, DB, Storage"
tagline : "Recent Notes for Paper Reading: Cloud, DB, Storage"
description: "Recent Notes for Paper Reading: Cloud, DB, Storage"
category: "storage"
tags: [storage, paper, database]
---
{% include JB/setup %}

Tracking recent paper reading notes. For a better view, paste the notes into a text editor with larger line width.

```
3. Reading: Recent piled up papers
    1. FAST'22 InfiniFS: An Efficient Metadata Service for Large-Scale Distributed Filesystems    [2022, 0 refs, Alibaba]
       https://zhuanlan.zhihu.com/p/492210459
       https://www.usenix.org/conference/fast22/presentation/lv
        1. Good. Can be used as a Refernece Architecture. Distributed filesystem metadata management.
           Metadata partitioning is hash-based, locality enhanced by Access-Content Decoupled Partitioning, access latency enhanced by Speculative Path Resolution.
           Consistency of two-server operation is done by 2PC and write-ahead logging. Consistency of rename is done by a centralized rename coordinator 
        2. Highlights
            1. Access-Content Decoupled Partitioning
                1. Consistent-hashing based placement.
                   dir inode metadata is separated into
                     access metadata: name, ID, and permissions
                     content metadata: timestamps, entry list (i.e., dirent), etc info related to child inodes
                   parent content metadata and children access metadata are grouped in partition
            2. Speculative Path Resolution
                1. inode id is by crypto hashing <parent id, directory name, name version>.
                   if no rename, inode id never changes
                   name version tell diff if a same directory name moved elsewhere, then another same directory name dir created
                2. speculative: client guess inode id, and parallel send requests
            3. Optimistic Access Metadata Cache
                1. rename, set_permission can expire many client cached entries
                   uses a broadcasted invalidation list (i.e. a queue) to lazily handle expire, refetch on requested
            4. Transaction
                1. two parallel renams can create loop dir structure
                   use one centralized rename server to serialize all and resolve conflict (i.e. God node) 
                2.  mkdir/rmdir/statdir distributed transaction uses one of the metadata server as the coordinatord
            5. Storage
                1. uses underlying KV store, which supports single node transaction
        3. More Highlights
            1. Previous works
                1. Facebook introduced the Tectonic distributed filesystem to consolidate small storage clusters into one single instance that contains billions of files
                2. Alibaba Cloud maintains nearly thousands of Pangu distributed filesystems to collectively support up to tens of billions of files in the datacenter
                3. Facebook also needs many HDFS clusters to store datasets in one single datacenter
                4. Mantle [34] provides a programmable interface to adjust CephFS’s balancing policy for various metadata workloads. However, they suffer from the high overhead of frequent metadata migrations, when workloads are diverse and vary frequently.
                5. NFS v4 [30] leverage the lease mechanism to cache both the directory entries and permissions on the clien side. However, the lease mechanism suffers from load imbalance caused by cache renewals at the near-root directories
            2. Key problem space
                1. Distributed filesystem metadata operation typically involve two critical steps: Path resolution and metadata processing
                    1. The concrete problem is, a deep path resolution involves many fetching for each middle path nodes
                       Subtree partitioning is the way to localize them into one node. But this paper takes approach of hash
                       So this paper has to do many enhancements, e.g. Speculative Path Resolution
                    2. Metadata hotness balance is another dimension, that favor in locality can easily hurt it
            3. Speculative Path Resolution
                1. the idea is to assign a predictable ID to each directory, so that clients can speculate on the IDs of all intermediate directories, then send lookups in parallel
            4. Interesting future directions / New area / My questions
                1. Global scale distributed filesystem
                    1. this paper is still mainly addressing datacenter scale. but how to compose a global-scale, geo-regional distributed filesystem, like Google Spanner?
                       It is able to serve a global company wide filesystem metadata
                    2. Besides, Global data sharing can eliminate duplicated data among separated clusters
                2. The one centralized rename server is NOT enough for a global scale filesystem

    2. CompressDB: Enabling Efficient Compressed Data Direct Processing for Various Databases    [2022, 1 refs, Tencent]
       https://zhuanlan.zhihu.com/p/539804815
       https://dl.acm.org/doi/pdf/10.1145/3514221.3526130
        1. Fixed size block dedup, by comparing block hash, tracked in block hashtable
           Block is compressed. Allow block holes by pointer tracking
           Direct read, update, search text in compressed blocks
        2. highlights
            1. Direct query, manipulate in compressed data
                1. CompressDB adopts rule-based compression and limits its rule generation depth. data manipulation without decompression
                    1. TADOC Rule-based compressino. This is a total new research direction. All 5 papers are under the same authors: Feng Zhang, Jidong Zhai, Xipeng Shen, Onur Mutlu, Wenguang Chen, Xiaoyong Du
                        1. Elements are atomic. Rule is a statement of elements. Rules form DAG relations.
                        2. The compression targets text documents with repeating words and word groups
                2. Validated CompressDB by supporting various including SQLite, LevelDB, MongoDB, and ClickHouse, using a five-node cluster in the cloud with MooseFS 
                3. evaluate our method using six real-world datasets with various lengths, structures, and content.
                    1. Datasets A, B, and C are collections of web documents downloaded from the. Wikipedia database[1]. Dataset D is a Wikipedia dataset composed
                    of four large files. Dataset E represents NSF Research Award Abstracts (NSFRAA) dataset downloaded from UCI Machine Learning
                    Repository [61]. Dataset E consists of a large number of small files,
                    and is used to evaluate performance on small files. Dataset F is a
                    real-world structured dataset from an Internet company, which is
                    used for traffic forecasting and intervention
                3. In compare with Succinct
                    1. Succinct [13] is a database supporting queries
                        over compressed data; the compression technique is based on index
                        and suffix array [13, 21, 26, 30, 43, 68] where compressed elements
                        are dependent on each other, making it extremely inefficient if a
                        small unit of data needs updates
                    2. CompressDB can provide 40.4× faster extract and 1.9× faster search, but 90% slower count
                    3. "CompressDB+Succinct" delivers 33%, 43%, and 3% performance improvements on extract, count, and search, along with 23.9% space savings, compared with Succinct


3. Readings: Recent papers piled up
    1. Nekara: Generalized Concurrency Testing    [2021, 0 refs]
       https://www.microsoft.com/en-us/research/uploads/prod/2021/09/nekara-ase2021.pdf
       https://www.youtube.com/watch?v=UTWaUjsqV8s
        1. ASE'21 paper on generalizing systematic concurrency testing
        2. Highlighs
            1. Testing needs
                1. Bug Replay
                2. Coverage of the interleaving space
                3. Controlling the interleaving space
            2. Case Memcached
                1. found 4 new concurrency bugs. even Memcached is so mature now
                    1. need work effort for code integration of Nekara API
            3. Nekara
                1. expressive API to model concurrency primitives
                2. search heuristics from prior work
                3. record scheduling decisions

    2. AMD SEV-SNP: Strengthening VM Isolation with Integrity Protection and More
       https://www.amd.com/system/files/TechDocs/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf
        1. Highlights
            1. SEV - Secure Encrypted Virtualization: Hypervisors cannot see guest VM memory except encrypted bytes
               SEV-ES - Encrypted State: Additional protection for CPU register states
               SEV-SNP - Secure Nested Paging: Protect agains integrity attacks, e.g. modify memory without decrypting, data replay, memory re-mapping
                1. 
            2. How SEV is able to protect guest VM from Hypervisor?
                1. VM DRAM is encrypted, key is generated by hardware and stored in dedicated hardware register where software cannot directly access
                   Additionally, identical plaintext at different memory locations wil encrypt differently

    3. FAST'22 InfiniFS: An Efficient Metadata Service for Large-Scale Distributed Filesystems
        1. logged before


1. Reading: Papers about compression
    1. LZ-End: LZ77-Like Compression with Fast Random Access [2010, 92 refs]
        https://users.dcc.uchile.cl/~gnavarro/ps/dcc10.1.pdf
        1. This paper proposed LZ-End.
            As summarized in "LZ-End Parsing in Compressed Space": The original LZ-End parsing needs O(n) space, too large.
                As summarized in "LZ-End Parsing in Linear Time"
                    1. LZ77 lies at the heart of many common compressors such as gzip, 7-zip, rar, and lz4
                    2. While "LZ-End Parsing in Compressed Space" optimizes memory space needed in construction, "LZ-End Parsing in Linear Time" optimizes for constructing time.
                    3. "Kreft and Navarro [24]: In its simplest form LZ77 greedily splits the input text into substrings (called phrases) such that each phrase is a first occurrence of a single letter or the longest substring that has an earlier occurrence. The index in [24] is built upon a small modification of LZ77 parsing called LZ-End (introduced in [22]) which assumes that the end of an earlier occurrence of each phrase aligns with the end of some previous phrase"
        2. Key trade-offs
            1. Decompressing LZ77 is expensive because it goes from start. Cutting the text into blocks allows point decompression, but ruins compression ratio to capture long-range repetitions
            2. LZ-End achieves similar to LZ77. "LZ-End forces the source of a phrase to finish where some previous phrase ends, and as a result it can guarantee that a substring finishing at a phrase boundary can be extracted in optimal time"
            3. See Definition 3. LZ77 cuts token when the token’s prefix is found in previous source. LZ-End cuts token when the token’s prefix can be found as a suffix of some previous tokens
                 See Lemma 1: LZ-End never generates two identical token.
            4. See Encoding section, for encoding result in bit representation: z(p) = (source[p], selectB(p + 1) − selectB(p) − 1, char[p])
                Theorem 3. Function Extract outputs a text substring T[start, end] ending at a phrase in time O(end − start + 1)
                This looks good and promising
                    1. How many random access do we need if the data is on disk?
            5. Decoding algorithm
                1. It sounds straightforward – See Figure 1. The magic is the char[], source[], B[] arrays built in encoding phrase.
                      If current pos is a token end, print the char[i].
                      If current pos spans tokens, split and handle.
                      If current pos is within in a token, recursively track back to source token.
                2. Questions
                    1. It seems, we don’t need LZ-end. We can directly do a similar point decompress instead on LZ77? So why LZ-End was introduced and requires matching previous suffix?
                    2. When doing decompression (start, len), we are jumping all over char[], source[], B[]. char[] would be accessed by O(len) times. This looks very bad for disk IO.
           

        n. knowledge related materials
            1. Learn in 5 Minutes: LZ77 Compression Algorithms
                https://www.youtube.com/watch?v=jVcTrBjI-eE
            
            2. LZ4 explained
                http://fastcompression.blogspot.com/2011/05/lz4-explained.html
                1. LZ77 is the base for all LZ* algorithms. LZ4 is a format standard, that backward lookup can use any implementation.
                    The backward lookup table is a dictionary constructed during compression scan.
                    But compression output won’t carry a dictionary. An dedupped entry carries a pointer to its last occurrence.
                    Decompression is simple, it just needs to translate dedup pointer to original data. It doesn’t even need to keep a dictionary

           3. LZ77+Huffman Compression Algorithm Details
                https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-xca/c0244bfe-fd96-4fe5-97dd-39b9fc99b801
                https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/fccm2014kim_cr.pdf
                1. LZ77 is called a dictionary based method. Huffman encoding is called a statistical coding scheme.
                    How: LZ77 outputs entries of <length, distances, [literal symbols]>. Some are more frequent. So encode twice with Huffman. Two steps are mostly decoupled.
                    Actually, DEFLATE, Zstandard, LZHAM, LZHUF, LZH, etc. use both Huffman and LZ77. Dedup coding + entropy coding is the common approach.
                2. Huffman coding: https://www.youtube.com/watch?v=NjhJJYHpYsg
                3. Why combine LZ77+Huffman? https://stackoverflow.com/questions/55547113/why-to-combine-huffman-and-lz77

            4. ZSTD using LZ77 first, then entropy coding next. I.e. Finite State Entropy for Sequences section, Huffman coding for Literal section: https://en.wikipedia.org/wiki/Zstd
                ZSTD is backed by a very fast entropy stage, provided by Huff0 and FSE lib: https://github.com/facebook/zstd, https://github.com/Cyan4973/FiniteStateEntropy
                  1. Finite State Entropy  - ANS - Asymmetric numeral systems: entropy coding combining speed of Huffman coding with compression rate of arithmetic coding: https://arxiv.org/abs/1311.2540
                  2. ANS is in the family of Arithmetic coding. Arithmetic coding: https://www.youtube.com/watch?v=-R2a2a1-2MM
                  3. The trade off between Arithmetic coding vs Huffman coding is better compression ratio vs better speed. ANS gets the best of the two.

            5. FM-index: https://www.youtube.com/watch?v=kvVGj5V65io (Ben Langmead)
                BWT: https://www.youtube.com/watch?v=4n7NPk5lwbI (Watch this first)
                1. Succinct data structure: data is compressed to near information-optimal bytes, and allow queries. Not specific to which implementation
                     FM-index is one popular implementation. Succinct Trie is another (https://nark.cc/p/?p=1720). Compressed suffix array is a third. FM-index is closely related to "Compressed suffix array" (via BWT).
                     SuRF is based on Fast Succinct Trie (FST): https://www.cs.cmu.edu/~pavlo/papers/mod601-zhangA-hm.pdf. (I.e. combines LOUDS-Dense & LOUDS-Sparse)
                         FM-index is very suitable for DNA sequence compressing and in-place searching a substring (prefix)
                2. FM-index is based on Burrows-Wheeler Transform (BWT). BWT is equivalent to Suffix Array (SA).
                    BWT preserves T-rank from F to L column of BWM. B-rank is a reverse of T-rank. BWT is reversible, constructed back to forth; it needs F column, L column, and both carrying B-rank.
                        Ranks don’t actually need to be stored, because F column is sorted, and L column preserves ranking. But scanning to calculate is too slow; use Tally array (sparse checkpoint) to speedup.
                    F column is compressed by Run-length Encoding (RLE). L column is compressible because same characters are frequently put in consecutive rows.
                        F, L use 2x size of the original string, and stores the char ordering by L->F mapping. However, F, L are much compressible and searchable than the original string.
                   Substring (prefix) searching is done because F, L stores the char ordering, and the first char can be located by RLE.
                        How to find the match’s offset in the original string? It needs a SA. Storing a full every slot SA is too much capacity, instead store a sparse one (SA sample).
                        How to access a char starting from specified offset? Using SA, it’s similar. It needs more jumps starting from slots of SA sample.
                   Problems / open questions
                       1. F & L column are always accessed in an interleaved way. It’s OK for in-memory index. But for on-disk lookup, this is too many random accesses

            6. Succinct Trie
                1. SuRF paper has an illustration of FST: https://www.cs.cmu.edu/~pavlo/papers/mod601-zhangA-hm.pdf
                    MIT: Succinct Structures I:  https://www.youtube.com/watch?v=3Y2weLDiUWw
                    More: http://stevehanov.ca/blog/?id=120, https://nark.cc/p/?p=1720 
                2. It’s a Trie tree. A node is represented like 1110, where number of 1 => number of children, 0 is the terminator. Nodes are scanned with breath first (LOUDS). Tree traversal is done by Select & Rank primitives. Value (pointers) is also embedded in tree’s bit sequence.
                    LOUDS-DS: To access values, given pos where D-HasChild[pos] = 0, D-ValuePos(pos) = rank1(D-Labels, pos) - rank1(D-HasChild, pos) + rank1(D-IsPrefixKey, ⌊pos/256⌋)-1 gives the lookup position
                    Position of the i-th node = select0 (i) + 1. Position of the k-th child of the node started at p = select0 (rank1 (p + k)) + 1. Position of the parent of the node started at p = select1 (rank0 (p))
                3. Features
                    1. Compressed. Support key lookup. Support range query. All in-place without decompression.
               4. Similar problems with Succinct data structures
                    1. Expensive to build. Cannot modify. Accessing a key needs several memory jumps.
                    2. Succinct Trie shouldn’t be slow at sequential key scan. What succinct data structure that can be slow at scan can be FM-index and Compressed Suffix Array.
                    3. No one is using a vanilla Succinct data structure. Everyone poses much optimizations on it.

            7. Compressed Suffix Array
                1. Succinct Store DB is using CSA: https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/agarwal
                    Text book: https://www.cs.cmu.edu/~dga/csa.pdf 
                2. Suffix array + Successor Array. Compression is done by Rank & Select too

            8. Wavelet tree
                1. Wavelet tree is a data structure that can be used to implement FM-Index, and also Compressed Suffix Array
                    https://www.sciencedirect.com/science/article/pii/S1570866717300205
                    https://en.wikipedia.org/wiki/FM-index
                    https://en.wikipedia.org/wiki/Compressed_suffix_array
                2. In FM-Index, the F and L columns (BWT) are stored as Wavelet Trees. For efficient reversal and matching
                    Wavelet tree extends the Select & Rank primitives to any character. This is right what FM-Index frequently needs
                    https://www.youtube.com/watch?v=UHGgpfxlaiE&t=183s
                3. Compressing storing Wavelet Tree
                    https://youtu.be/4aSv9PcecDw?t=1238

        n+1. Further works
            1. LZ-End Parsing in Compressed Space    [2017, 24 refs]: https://arxiv.org/pdf/1611.01769.pdf
                Github implementation: https://github.com/dominikkempa/lz-end-toolkit
                LZ-End Parsing in Linear Time    [2017, 5 refs] (Same authors): https://drops.dagstuhl.de/opus/volltexte/2017/7847/pdf/LIPIcs-ESA-2017-53.pdf
                1. Area: compressed indexing of highly repetitive data. Such as Wikipedia, genomes, logs. LZ-End was one of the most successful approach. Fast retrieval of substrings of compressed text without decompression.
                    Comparing alternatives: LZ77-based methods, e.g. LZ-End. FM-index, Compressed suffix array (Succinct)
                2. "[24] On Compressing and Indexing Repetitive Sequences" [2013, 143 refs] referenced as the most successful work.
                    https://users.dcc.uchile.cl/~gnavarro/ps/tcs12.pdf
                    1. Same authors of the original LZ-End paper and published 3 years later

    2. FSST: Fast Random Access String Compression [2020 8 refs]
    https://www.vldb.org/pvldb/vol13/p2649-boncz.pdf
        1. Random access decompression is done by fetching a byte and lookup from the symbol table (i.e dictionary)
            Constructing a well symbol table is challenging

    3. On Universal Compression with Constant Random Access [2018, 9 refs]
        https://ieeexplore.ieee.org/abstract/document/8437931/
        1. the typical usecase field is genomics. The proposed method achieves near LZ78 compression rate, and needs constant number of random access to decompress and point address.
            All math formulas and theory analysis. Any ready runnable implementation for use?
    2. Based on sparse bit vector compressor [7].
        3. Still need per block compression? "every random access query requires decoding the parameters and the entire block". Block size b is fixed.
            "Thus, one can expect the random access performace to be highly correlated and dominated by the block size b, with smaller block sizes being preferred. However, the compression rate R also depends on the block size"
        3. LZ78 vs LZ77: https://www.ijesit.com/Volume%204/Issue%203/IJESIT201503_06.pdf
            Theorem 3 has an illustration of using LZ78: Input -> cut into blocks -> First Lb bits stored in dense stream, remaining bits stored in sparse stream -> Encode dense stream as itself (identity map), encode sparse stream with expander graph.
            expander graph: See [5] or Lemma 1. How to select block size? Roughly, block size must be large enough to ensure sparsity of the sparse stream, and to ensure entropy diff is small enough. The paper only points out block size is bounded.

    4. Succinct: Enabling Queries on Compressed Data [2015, 93 refs]
        https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/agarwal 
        1. Data compressed + in-memory index => One succinct compressed data (flat file, no index)
            Interface: buffer = extract(f, offset, len), [offset1, ...] = search(f, str). extract is supported by CSA
            "Succinct" (project name) is based on Compressed Suffix Arrays (CSA), with optimizations.
        2. Usecase targets in-memory DB or in-memory indexing, secondary key indexing, and DNA search
            "SuccinctStore .. designed for memory efficiency .. Succinct will lose its advantages if input data is too large to fit in memory even after compression"
           Input2AoS and AoS2Input, NextCharIdx need to stored. Capacity is reduced by lower sampling rate.

    5. Dictionary-based Order-preserving String Compression for Main Memory Column Stores    [2009, 201 refs]
        https://15721.courses.cs.cmu.edu/spring2016/papers/p283-binnig.pdf 
        1. Problems to solve
            1. Columnar DB to compress string columns, like product data.
                How many strings are there (domain size) are not known a priori, and can change
                Order preserving dictionary
                Code integers have fixed-length to favor query processing
        2. Key solutions
            1. Encode index and decode index to have shared leaves
            2. Leaf structure itself is compressed
            3. Cache-conscious string index for encoding, CSS-tree for decoding

    6. Other papers tracked but I didn't read

        Enabling Efficient Random Access to Hierarchically-Compressed Data [2020, 8 refs]: https://fengzhangcs.github.io/papers/ICDE_Zhang.pdf
        FSST: Fast Random Access String Compression [2020 8 refs]: https://www.vldb.org/pvldb/vol13/p2649-boncz.pdf
        Compression with Fast Random Access [2001]: https://www.brics.dk/DS/01/9/

        Simple Random Access Compression [2009, 5 refs]: https://www.researchgate.net/profile/Kimmo-Fredriksson/publication/220444601_Simple_Random_Access_Compression/links/02bfe50ee95e214e9f000000/Simple-Random-Access-Compression.pdf
        Wavelet based 3D compression with fast random access for very large volume data [1999, 101 refs]: https://ieeexplore.ieee.org/abstract/document/803354/
        Simple Compression Code Supporting Random Access and Fast String Matching [2007, 29 refs]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.437.8442&rep=rep1&type=pdf
        Robust relative compression of genomes with random access [2011, 132 refs]: https://academic.oup.com/bioinformatics/article/27/21/2979/217176?view=extract

        Index compression is good, especially for random access [2007, 52 refs]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.75.2591&rep=rep1&type=pdf
        Enhanced Variable-Length Codes: Improved Compression with Efficient Random Access [2014, 22 refs]: https://www.researchgate.net/profile/M-Kuelekci/publication/262938266_Enhanced_Variable-Length_Codes_Improved_Compression_with_Efficient_Random_Access/links/00b7d5396b8b1862c4000000/Enhanced-Variable-Length-Codes-Improved-Compression-with-Efficient-Random-Access.pdf 
        CompressDB: Enabling Efficient Compressed Data Direct Processing for Various Databases[2022, 1 refs]: https://zhuanlan.zhihu.com/p/539804815


3. Reading: Recent papers piled up
    1. Amazon Redshift Re-invented     [2022, 0 refs, SIGMOD22]
       https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf
        1. Redshift is a column-oriented data warehouse (OLAP), based on PostgreSQL, data persisted in S3, cached to local SSD, accelerated with AWS Nitro
           Performance optimized, feature rich, scaling storage & compute, and near-zero touch serveless interface.
           very good paper, a bibliography of the mordern data warehouse.
        2. highlights
            1. What makes a good cloud data warehouse
                1. First, customers demand high-performance execution of increasingly complex analytical queries
                    1. performant query execution, code generation at each query fragment
                    2. State-of-the-art techniques like prefetching and vectorized execution
                2. Second, as our customers grow, they need to process more data and scale the number of users that derive insights from data
                    1. disaggregated its storage and compute layers
                    2. scales up by elastically changing the size of each cluster and scales out for increased throughput via multi-cluster autoscaling
                    3. automatically adds and removes compute clusters to handle spikes in customer workloads
                3. Third, customers want Redshift to be easier to use
                    1. machine learning based autonomics that finetune each cluster based on the unique needs of customer workloads
                    2. automated workload management, physical tuning
                    3. the refresh of materialized views (MVs), along with preprocessing that rewrites queries to use MVs
                    4. Web-based Data API access, besdies JDBC/ODBC
                4. Fourth, customers expect Redshift to integrate seamlessly with the AWS ecosystem and other AWS purpose built services
                    1. federated queries to transactional databases (e.g., DynamoDB [10] and Aurora [22]), Amazon S3 object storage, and the ML services of Amazon Sagemake
                    2. Glue Elastic Views, customers can create Materialized Views in Redshift that are incrementally refreshed on updates of base tables in DynamoDB or Amazon OpenSearch
                    3. ingestion and querying of semistructured data with the SUPER type and PartiQL [2]
                5. Others
                    1. AQUA, Redshift’s hardwarebased query acceleration layer and Redshift’s advanced query rewriting capabilities
                        1. FPGA based
                    2. Compilation-As-A-Serivce, a caching microsservice for optimimzed generated code for the various query fragments
            2. Performance that matters
                1. code generation, vectorized SIMD scans
                    1. much effort are paied to put columns on-fly in CPU register, put hash tables in cache, issue prefetch to avoid memory stalls
                2. external compilation service, external compilation cache
                3. AZ64 encoding (vs zstd, lzo)
                   https://docs.aws.amazon.com/redshift/latest/dg/az64-encoding.html
                    1. proprietary AWS. seems columnar compression optimized with SIMD, type-specifc to small/big int, decimal, date, timestamp
                    2. AZ64 Encoding - Max Ganz II @ Amazon Redshift Research Project     [2021]
                       https://www.reddit.com/r/aws/comments/t3nrrr/amazon_redshift_research_project_az64_encoding/
                       https://www.amazonredshiftresearchproject.org/white_papers/downloads/az64_encoding.pdf
                4. Adaptive execution: the engine monitors BloomFilter effectiveness at runtime and determine size and if to disable
                5. AQUA - Advanced Query Accelerator
                    1. AQUA caches hot data for cluters on local SSDs, instead of fetching from regional storage
                    2. AQUA provides a functional interface, rather than a storage interface. it's a computational storage that directly run queries against cached data
                    3. AQUA customize servers with AWS Nitro ASIC.
                       Also FPGA a custom multi-core VLIW processor that contains database types and operations as pipelined primitives
                        1. VLIW: https://sites.pitt.edu/~akjones/Alex-K-Jones/VLIW_FPGA.html
                                 https://en.wikipedia.org/wiki/Very_long_instruction_word
                6. DSL-based Query Rewriting Framework (like CockroachDB's?)
                    1. including rewriting to nested and semistructured data processing
            3. Scaling Storage
                1. Redshift Managed Storage (RMS) optimize performance and tiers, based on block temperature, age, workload pattern
                    1. Server accelerated by AWS Nitro System
                    2. Data one copy at S3, cached by local attached SSD, plus an in-memoy disk cache
                    3. Access tracking per block, two-level clock-based cache replacement policy
                        1. interesting point: drive rehydration (i.e. what data to cache on local SSD) after a cluster reconfiguration (Elastic Resize, cluster restores, hardware failures)
                    4. Log-based commit protocol to S3, instead of legacy redirect-on-write protocol
                        1. batch data writes, and group commit with sync barriers
                2. Decoupling metadata from data
                    1. Elastic resize, Cross-instance Restore are heavily used features
                3. Concucrrency Control
                    1. MVCC, and enfore serializable isolation
                    2. Instead of SSI, implmented by a more improved Serial Safe Net (SSN) algorithm [23]
                        1. plus custom optimziation: aborting certain trnasactions during execution, rather than performing SSN calculation
                           this significantly reduces resource utilization and reduces memory footprint
            4. Scaling Compute
                1. Elastic Resize. Scale data without reshuffle, decoupled from metadata
                2. Sharable work unites: invidiual processor can work on multiple partitions, individual partition can be worked by all processors on a node
                3. Share live data across different Reshift compute clusters and AWS accounts
                    1. Different compute clusters can operate on a single source of data. Avoid pipelining data
                    2. Data can be shared at different levels
            5. Automated Tuning and Operations
                1. Cluster maintenance, patching, monitoring, resize, backup and encryption
                    1. Smart Warmpools for prompt replacements of faulty nodes, rapid resumption of paused clusters, automatic concurrency scaling, failover
                        1. Warmpools are a group of EC2 instances that have been pre-installed with software and networking configurations
                        2. Maintained a distinct warmpool in each AS
                        3. Redshift built a machine learning model to forecast how many EC2 instances are required for a given warmpool at any time
                           This system dynamically adjusts warmpools in each region and availability zone
                    2. Grey Failure Detection
                        1. Redshift has developed outlier detection algorithms that identify with confidence sub-performing components (e.g., slow disks, NICs, etc.)
                           and automatically trigger the corresponding remediation actions
                2. Vacuum, analyze and refresh of materialized views in background
                    1. Materialized Views
                        1. reuse expensive query results. updates from base table are incremental, offline from transaction path, favoring batch
                        2. a priority queue of MVs based on utilization, refresh cost. Update in background, within 15min for 95% MVs
                        3. MV-based query rewriting, or directly query MV
                3. Auto selection and recommendation of distribution key and sort key
                    1. called "Automatica Table Optimization (ATO)"
                4. forecasting techniques for workload management scaling
                    1. AutoWLM - Automatic Workload Manager
                        1. query admission throttling, scheduling, resource allocation
                        2. clsuster elastic resize
                    2. Machine Learning, Queuing Theory <= IO/CPU saturation => increase/reduce concurrency
                        1. Weighted round-robin scheme for scheduling higher priority queries more often than low priority ones
                           Redshift divides CPU and I/O in exponentially decreasing chunks for decreasing priority level
                        2. If a higher priority query arrives after a lower priority query started executing, AutoWLM preempts the lower priority ones
                           To prevent starvation of lower priority queries, a query’s probability of being preempted is reduced with each preemption
                           AutoWLM prevents preemption if wasted work ratio (i.e., time lost due to preemption over total time) breaches a threshold
                        3. Redshift’s Query Predictor Framework
                            1. Having a predictor on the cluster itself helps to quickly react to changing workloads, which would not be possible if the model was trained off-cluster and only used on the cluster for inference
                5. Serverless Compute - run and scale analytics in seconds without the need to setup and manage
                    1. Serverless relies on algorithms for automated provisioning, sizing and scaling
                    2. Serverless offers a near-zero touch interface. Customsers pay only for the seconds they have queries running
                6. Tooling environment
                    1. Query Open File Format (Parquet, Text, ORC, AVRO) in Datalake via Spectrum[8], cost efficient 
                    2. Integration with AWS Sagemaker ML
                    3. Federated Query to OLTP DynamoDB, Aurora Postgres, Aurora MySQL
                    4. SUPER field type to store JSON string, PartiQL shred them to materialized view
                    5. UDF backed by AWS Lambda, allow migrating legacy code to C/C++/Java

        n. related materials
            1. Amazon Redshift: Ten years of continuous reinvention    [2022-05-18]
               https://www.amazon.science/latest-news/amazon-redshift-ten-years-of-continuous-reinvention
            2. Amazon Redshift is based on PostgreSQL
               https://docs.aws.amazon.com/redshift/latest/dg/c_redshift-and-postgres-sql.html
            
            3. SSN: Efficiently making (almost) any concurrency control mechanism serializable    [2016, 34 refs]
               https://arxiv.org/pdf/1605.04292.pdf
               PPT: https://event.cwi.nl/damon2015/slides/slides-wang.pptx
                1. SSI was previously known the most recent Serializable level CC algorithm, implemented in PostgreSQL, now we have a more advanced SSN. very good upgrade.
                   The typical usable is SI+SSN, while SSN acts as the second level filter to reject Tx causing abnormality loops
                   The validation is performed when Tx commit, only need to examine direct dependencies. Less false positives are rejected.
                2. highlights
                    1. Figure 1 CC algorithm compares
                        1. Fully precise serialization graph testing (SGT) [6] allows all (and only) cycle-free executions, but is impractical as every commit requires an expensive search for cycles over an ever-changing dependency graph
                        2. SSI offers full serializability but lowers concurrency
                           Figure 3: SSI always admits cases (a) and (b), always rejects (d), and often rejects (c) and (f).
                            1. SSI rejects cycle by detecting "dangerous structure", while SSN detects π, η timestamp watermarks
                               https://zhuanlan.zhihu.com/p/103553619
                            2. memory tracking cost: SSI needs T.inConflict + T.outConflict, the window size is propotional to on-going Tx count. which is simall
                               SSN tracks timestamp watermarks for active Tx, note SSN also needs to track timestamp per value item.
                            3. computation cost: SSI needs SIREAD lock that gets updated per Tx per locking read/write value item
                               SSN needs timestamp calculation per Tx per value item accessed too.
                               SSN doesn't need a SIREAD lock, less lock so probably higher concurrency allowed?
                    2. Reading Figure 2/3/4
                        1. follow right arrows (any hop reachable) to the vertically bottom -> that's timestamp π(T) -> mapping to t.sstamp in Algorithm 1, successors
                           follow left arrows (only the neighbor hop) to the vertically top -> mapping to t.pstamp in Algorithm 1
                    3. SSN Exhibits the safe retry property too, like SSI
                        1. if a transaction is aborted, immediately retrying the same transaction will not cause it to fail again with the same serialization failure
                           https://drkp.net/papers/ssi-vldb12.pdf
                    4. SSN supports a variant of the “safe snapshot” [42]
                        1. a transaction known to be read-only can avoid the overhead of SSN completely, by using a snapshot that the system guarantees will not participate in any serial anomalies

                    n. questions
                        1. how to implemented SSN in a distributed transaction system?
                        2. from the testing, OCC (replace locking with version check) is actually not bad
                        3. where's the proof that SSN rejects false positives less than SSN? Rather than case by case analysis
                        4. why SSI starves writers, OCC starves readers, and SSN is fair to both R & W?
                            1. found in PPT, but didn't find search of "starv" in paper
                n. related materials
                    1. serial safety net (SSN)论文笔记 - 风影s6
                       https://zhuanlan.zhihu.com/p/524580964
                        1. SSN为了在提交时验证是否有环，定义了两个时间参数，π(T)和η(T)
                            π(T)是事务T在依赖图中，从T发出的依赖关系所能达到的事务节点，最早的提交时间，当T准备提交时，π(T)已经确定
                            η(T)是事务T在依赖图中，入读节点集合中，最晚的提交时间
                            SSN通过验证exclusion window来判定事务是否可以提交，exclusion window指的是事务T的π(T)和η(T)构成的时间区间，正常情况下是[η(T),π(T)] (η(T)<π(T))，如果不符合则不可以提交。
                        2. SSN原文中规定的->是排序顺序，而不是我们在依赖图中提到的依赖关系（因此论文中的->要全部反过来）

            4. Gray Failure: The Achilles’ Heel of Cloud-Scale Systems    [2017, 121 refs, Microsoft]
               https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/paper-1.pdf
                1. Gray failure, intermittent failures, performance degradation, failures at high percentiles.
                   The paper proposed "Observational difference" as the root cause of gray failure
                   "The blame game" is also a typical behavior.
                   Solutions: Active probing, fan-out probing, gossip health status, quorum decision
                2. highlights
                    1. gray failure examples
                        1. if a system’s request handling module is stuck but its heartbeat module is not, then an error-handling module relying on heartbeats will perceive the system as healthy while a client seeking service will perceive it as failed
                            1. see Figure 3.
                        2. if a link is operating at significantly lower bandwidth than usual, a connectivity test will reveal no problems but an application using the link may obtain bad performance
                            1. we can aggregate observations of VM virtual disk failure events and map them to cluster and network topology information
                            2. Indeed, we have used this approach to pinpoint many gray failure cases due to storage overloading or unplanned top-of-rack (ToR) switch reboots
                        3. a certain data server was experiencing a severe capacity constraint, but a subtle resource-reporting bug caused the storage manager to not detect this gray failure condition. Thus, the storage manager continued routing write requests to this degraded server, causing it to crash and reboot. Of course, the reboot did nothing to fix the underlying problem, so the storage manager once again routed new write requests to it, causing it to crash and reboot again.
                    2. "The blame game": gray failure wasn't detected at the right component, as a result a more upper stream component was marked as repeated failure and retired, increasing the resource stress and making the gray failure more easy to happen
                    3. high fan-in fan-out pattern increases the chance for gray failure

            5. 从 SIGMOD 22 论文看 Redshift 的最新进展 - hhwyt
               https://zhuanlan.zhihu.com/p/545348145?utm_source=ZHShareTargetIDMore&utm_medium=social&utm_oi=30546549800960

            6. Data Warehousing in the Cloud: Amazon Redshift vs Microsoft Azure SQL    [2017, 2 refs]
               https://pdfs.semanticscholar.org/6549/c8e2305e1e34c985d9559625b6a9fa3efee7.pdf
                1. highlights
                  1. "All the data stored in Azure SQL Data Warehouse is stored in Azure Blob Storage"
                  2. "It also has a service called Data Movement Service" responsible for all data movements between nodes
                     "It is not an Azure service but a Windows service that runs alongside SQL Database on all the nodes and it is only visible on query plans because they include some DMS operations since data movement is necessary to run a query in parallel"
                  3. Redshift has local storage caching to get faster
                     Azure DW can only run 32 concurrent queries
                     No sure Azure DW is not column-oriented?
                  4. Azure SQL DW has the ability to pause compute when not in use so we only pay for storage, as opposed to Redshift in which we are billed 24/7 for all the virtual machines that make up the nodes

    2. Amazon DynamoDB: A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service
       https://www.usenix.org/conference/atc22/presentation/elhemali
        1. good paper. cloud-native NoSQL database OLTP battle proven in AWS.
           API is CURD of KV, storage engine by B+-tree and WAL, data replicas are managed by Multi-Paxos.
           The paper featured in how to ensure predictable latency, cloud native, read-write deployment, statically stable design, bi-modality elimination
        2. highlights
            1. predictable latency
                1. Q99 is less than 2x of Q50, within < 10ms.
                2. partition split, merge, scaleout, migration balancing
                    1. partition split key is by access distribution, rather than middle of key range
                3. traffic admission
                    1. the table level global admission control (GAC), that allows partitions to share the throttle of the table
                    2. per partition burst capacity. partition is tagged with (allocated, burst) token bucket. node is tagged with a total token bucket
                    3. provisioned capacity
                4. metadata access no bi-modality
                    1. hit cache or not hit cache is a bi-modal behavior.
                       adding new node with cold cache restart can cause cascading failure in the system
                    2. to remove the bi-modality, introduced MemDS, a distributed off heap memory store
                       all metadata are kept in memory, replicated, indexed with Radix tree + Merkle tree
                       MemDS also supports range queries, and floor/ceiling
                5. on demand table
                    1. instead of letting customer assign provisioned capacity, the table auto scales and charge by actual use 
                6. Quorum writes that reduces tail latency
                    1. eventual consistency vs strong consistency writes
                7. storage backed by SSD.
            2. cloud native
                1. customer don't need to deploy explicit database, no config where/how tables are stored
                2. multi-tenancy. a physical servers runs multiple customer, isolated by performance and security
                3. boundless scale for tables
                4. predictable performance, even a table grows from MB to TB
                5. more features
                    1. Secondary indexes
                    2. JSON documents
                    3. Streams
                    4. GAC, burst/adaptive capacity
                    5. transactions
                    6. on-demand tables
                    7. infrequent access tables
                6. Gray network failures
                    1. instead of re-select leader once heartbeat not heard, send requests to peers to confirm the leader is actually dead.
                7. Deployment
                    1. Read-Write deployment, to add new message type while supporting rollback.
                       The first deployment changes nothing but to support the new message type.
                       The second deployment starts writing the new messages, while allowing rollback
                8. Dependencies on external services
                    1. e.g. IAM and AWS KMS
                    2. solution: statically stable design. even lost connection to IAM, KMS, the cached results in routers can still serve requests.
                       though new requests not in cache cannot work, but in practice this is not a big problem
            3. point-in-time backup, snapshots
                1. storage backend is B+-tree + WAL logs
                2. WAL is also archived to S3, that can be replayed for point-in-time restore
                   snapshot is periodically take to speedup replay

    3. SQLite: Past, Present, and Future    [VLDB 2022, 0 refs]
       https://www.vldb.org/pvldb/vol15/p3535-gaffney.pdf
        1. SQLite traditionally is OLTP, row-oriented, B-tree storage. An embedded database. But Edge computing and data science growing need OLAP.
           DuckDB (Not this paper) targets OLAP "the SQLite for analytics".
           This paper identify SQLite bottlenecks for OLAP and weighing potential solutions
        2. highlights
            1. past sucessfactors of SQLite
                1. Cross-platform. stored in a single file 32-bit/64-bit. Run on any platform.
                2. Compact and self-contained. 150K LOC. Compiled to less than 750 KiB. No external dependency
                    1. not only library, SQLite can compile into hosting App
                3. Reliable. Tests cover 100% of branches. Diverse tests
                   fuzz tests, boundary value tests, regression tests, and tests that simulate operating system crashes, power losses, I/O errors, and out-of-memory errors
                4. Fast. several 10Ks of TPS.
                   In some cases, SQLite reads and writes blob data 35% faster and uses 20% less storage space than the filesystem [16]
            2. banchmarks used
                1. SSB - Star Schema Benchmark
                2. TATP - Telecom Application Transaction Processing Benchmark
            3. future works
                1.  SQLite3/HE [46], a query acceleration path for analytics in SQLite. SQLite3/HE achieves speedups of over 100X on SSB with no degradation in OLTP performance. However, the current implementation of SQLite3/HE does not persist columnar data to storage and is designed to be used in a single process
        n. related materials
            1. Hacker News: https://news.ycombinator.com/item?id=32675861
            2. Notes on the SQLite DuckDB paper - Simon Willison’s Weblog
               https://simonwillison.net/2022/Sep/1/sqlite-duckdb-paper/

    4. Owl: Scale and Flexibility in Distribution of Hot Content    [OSDI 2022, 0 refs, Facebook]
       https://www.usenix.org/conference/osdi22/presentation/flinn
       https://engineering.fb.com/2022/07/14/data-infrastructure/owl-distributing-content-at-meta-scale/
        1. Per region runs many peers and several Tracks (HA redundancy).
           All decisions are made by Tracker to provide a centralized control plain. Content distribution data flows through peers, in a decentralized way, like BT.
           200x 2021 Traffic Growth, only 4x server growth, due to peer-to-peer distribution.
           Good. It can be used as a reference architecture for CDN.
        2. highlights
            1. prior works in facebook
                1. Hierarchical caching
                    1. Problems
                        1. Need growing number of dedicated hosts with growing number of reading clients and workloads
                        2. Hot contents are bursting and causing load spikes, however we need to set quota to protect the central storage
                           provisioning for transient spikes caused by hot content and setting quotas appropriately were conflicting
                2. a location-aware BitTorrent implementation and a static peer-to-peer distribution tree based on consistent hashing
                    1. The decentralized systems scaled much better than hierarchical caching
                    2. New problems though
                        1. Each peer is making decision by only local information, caching decisions are independent across peers.
                           either more or fewer than necessary data copies can be retained, causing poor resource efficiency or tail latency
                        2. Operation with decentralized system is hard. Always need to aggregate large amount of peers.
                           Difficult to understand overall healthy, status, efficency and correctness.
            2. new solution
                1. In summary, highly decentralized systems turned out to be inefficient and difficult to operate, while highly centralized systems scaled poorly. 
                   As a result, we chose to create a new, split design with a decentralized data plane and a centralized control plane. 
                   The decentralized data plane streams data from sources to clients via a distribution tree built by the centralized control plane. 
                   However, these trees are ephemeral and per-data-chunk. Each edge in a tree persists only while a chunk is being transferred from a source to a peer.
                2. This fine-grained state allows the trackers to make optimal decisions about data placement and distribution that minimize network hops and maximize cache hit rate. 
                   Centralizing the control plane has also made distribution easy to operate and debug: Engineers can understand what decisions led to low availability, high latency, or poor cache hit rate because a tracker with a consistent view of the distribution state makes these decisions
                3. We therefore chose to make customization a first-class design priority
                    1. Trackers implement modular interfaces for specifying different policies for caching and fetching data
                    2. Flexibility. At Meta, clients have vastly different resources to spare for distribution. Some dedicated GB's of memory or disk for p2p caching, others little resource to spare
            3. overview of Owl
                1. Peer - clientlib, simple state machines
                    1. runs on the peer server that downloads and acts as data cache
                    2. Superpeer - Peers can load cache data from
                        1. Superpeer is a inheritance of Hierarchical cache. It can also be used to consolidate cache to improve cache hit
                        2. Virtual Superpeer is a good design. reserve a portition of memory of each client, to collectively form a virtual superuser
                            1. it reduces the duplicated fetching from the root external storage.
                               The usercase includes a group of clients that each only needs a small portion of data, but collectively they need all chunks
                               With virtual Superpeer, the first client can fetch what it needs, and also cache all chunks to Virtual Superpeer
                               Without virtual Superpeer, each client would fetch duplicate chunks, discard it, because they only need their own portion of data
                    3. Assign a bucket that uniquely identify the type of client binary
                        1. customize Owl behavior for each type of client
                        2. monitor usage, performance, and reliability for each Owl customer individually
                2. Trackers (borrowed from BT) - manages the download state
                    1. Typically, peers and trackers are grouped by region (a region is several colocated data centers), 
                    with 3-4 trackers per region providing scale and redundancy
                    2. In contrast with highly decentralized systems like BitTorrent, Owl trackers can maintain such detailed up-to-date states because trackers make all major decisions about caching and downloading chunks on behalf of peers
                    3. Each peer picks a random instance from the set of available trackers and registers by sending a remote procedure call (RPC)
                       One of Owl’s primary design principles is to keep peers as simple as possible
                        1. This is achieved via a mechanism-policy split. The peers provide the mechanism to perform simple actions.
                           These include downloading a chunk from a given source, caching or evicting a chunk from cache, or providing cached data in response to a request from another peer.
                        2. To download content, peers ask trackers to decide from where they should fetch content, how they should retry failed downloads, and even what chunks they should cache locally
                        3. This design principle has proven invaluable for operational simplicity
                    4. state is sharded if beyond one tracker capacity
            4. CDN Policy design 
                1. Selection policies
                    1. Decide how to retry, when to give up
                    2. Set max outflows, bandwidth constraints, etc
                    3. Examples
                        1. Location-aware, choose nearest machine peer/superpeer
                        2. holt-cold: leverage superpeers for hot data, bypass for cold
                2. Caching policies
                    1. Whether to cache data in memory, on disk, or both
                    2. Can allow cooperative read-only sharing
                    3. examples
                        1. Replacement: LRU, Least-Rare, TTL, Random, etc
                        2. Clients manage their own replacement
                3. Emulation: Finding good policies
                    1. Run actual track and emulated peers.
                        1. Event-driven, virtual clock.
                    2. Record and replay production traffic.
                        1. search space is large. we use random-restart hill climbing [10]
                    3. Multi-start hill climbing to search space of possible policies
                    4. In 1 month, improved 5 user cases by 70% on key metrics
                    6. total 106 unique types of clients, 55 customized policies for them
                    7. besides, a new client can rollout with shadow run that force half requests to directly go to external storage, so for A-B compare
                    n. my questions
                        1. good part. This is actually the most important how-to about policy design, the fundamental infrastructure. The answer is emulation with prod traces, simple, but practical.
            5. Diff to BitTorrent
                1. BT makes a decisions locally at peers, the localized decision can become less than optimal
            6. Future works
                1. Move from pulling data by peer to, pushing data to peer, in streaming application
                2. Incremental update capability for really gradually changing objects, like AI model 

            n. related materials
                1. Random-start Hill Climbing search algorithms
                    1. Random Restart Hill Climbing - Georgia Tech - Machine Learning
                       https://www.youtube.com/watch?v=lFjH05v3T54
                    2. Stochastic hill climbing vs random-restart hill climbing algorithms
                       https://stackoverflow.com/questions/49595577/stochastic-hill-climbing-vs-random-restart-hill-climbing-algorithms
                    3. Gradient descent is a specific kind of “hill climbing” algorithm
                       https://www.quora.com/Is-gradient-descent-algorithm-the-same-as-hill-climbing
                    4. Local Search: of Hill Climbing With random Walk & Random Restart Part-5
                       https://www.youtube.com/watch?v=66y70MhetSw

    5. AMD 安全加密虚拟化 - White Paper
       AMD SEV-SNP: Strengthening VM Isolation with Integrity Protection and More
       https://www.amd.com/zh-hans/processors/amd-secure-encrypted-virtualization
        1. VM在云上运行，但用户/VM可以不信任Cloud infra的hypervisor（如盗取VM内信息）。AMD SEV系列技术通过硬件保障VM仍能安全不泄密
           Useful doc as an example how to analyze security with threat modeling
        2. highlights
            1. SEV - hypervisor only sees VM's encrypted memory bytes
               SEV-ES - encrypt CPU registers too
               SEV-SNP - further from SEV and SEV-ES, add Secure Nested Paging
                1. SEV-SNP is designed to prevent software-based integrity attacks and reduce risk associated with  memory integrity.
                   The basic principle of SEV-SNP integrity is that if a VM is able to read private (encrypted) page of memory, it must always read the value it last wrote
                2. "Additional protection against certain fingerprinting attacks may be offered in future SEV technologies"
            2. Threat modeling
                1. SEV and SEV-ES use the threat model of a “benign but vulnerable” hypervisor
                   SEV-SNP addresses additional attack vectors and potential threats to VM security
            3. key mechanisms
                1. Reverse Map Table (RMP)
                2. Page Validation (relies on RMP)
        n. related materials
            1. 在数据中心领域 AMD究竟如何加速？
               https://zhuanlan.zhihu.com/p/378529176
                1. "具体来说，Zen3架构对SEV进行改进，限制中断的注入，限制恶意管理程序注入SEV-ES访客中断/异常类型，能够将调试寄存器添加到交换状态中。
                   另外，Zen3架构还新引入了SNP安全嵌套分页，在现有SEV-ES对虚机内存和虚机寄存器进行加密保密的基础上，增加了系统完整性保护，防止恶意管理程序通过重放、损坏、重新映射进行攻击。
                   Zen3架构还提供了CET Shadow Stack(CET影子栈)，以此来防止ROP编程攻击，更好地确保系统安全性。"
            2. One Glitch to Rule Them All: Fault Injection Attacks Against AMD’s Secure Encrypted Virtualization    [CCS 2021 best paper reward, 12 refs]
               https://zhuanlan.zhihu.com/p/494897106
                1. "AMD安全加密虚拟化(SEV)通过内存和寄存器加密为非信任环境中的虚拟机提供保护机制。SEV利用了AMD安全处理器(AMD- sp)，将安全敏感的操作与在主x86内核上执行的软件分开。
                    本文提出了一种针对AMD-SP攻击受sev保护的虚拟机的新方法。展示了一种电压故障攻击，允许攻击者在目前市场上所有支持SEV的微体系结构的AMD-SP中运行自定义负载，包括Zen1，Zen2， Zen3。
                    本文介绍的方法允许在AMD-SP上部署自定义SEV固件，这使得攻击者能够解密VM的内存。通过本文的方法，可以在支持SEV的CPU上提取密钥，这使得我们可以伪造认证证书，不需要对目标主机进行物理访问就可以充当VM迁移的有效目标。此外，作者还对由SEV安全嵌套分页(SEV-SNP)引入的版本芯片密钥机制进行和逆向工程。"

    6. PATHWAYS: ASYNCHRONOUS DISTRIBUTED DATAFLOW FOR ML    [2022, 11 refs, Google]
       https://arxiv.org/pdf/2203.12533.pdf
        1. HPC architecture with ICI inter-connected islands of TPU cores.
           Single controller. But to catch performance with Mutlti-controller with gang scheduling and parallel asynchronous dispatch
        2. highlights
            1. comparing systems
                1. Googles TensorFlow v1/v2 on TPU, JAX; PyTorch; Ray on GPU
            2. Pathways match multi-controller performance with single controller design
                1. single controller is nicer for programming. A single control plane.
                   better for novel and efficient ML optimization
                2. to catch the performance with multi-controller
                    1. gang scheduling. a centralized scheduler per island. a big computation graph is sharded into gangs
                    2. parallel asynchronous dispatch. remove the one-by-one sync step, issue tasks in parallel from beginning 
            3. Pathways architecture
                1. HPC computing. TPU cores are separated into islands. Intra island connects with ICI (comparing with NVLink), cross island connects with datacenter network (DCN)
                2. "The biggest difference between TPU and GPU is that far longer-running and more complex computations can be fused into a single TPU kernel, because the TPU supports rich control flow and communication primitives that must instead be executed by driver code on GPU systems. GPUs, by contrast, are more tightly integrated with host memory systems and DCNs"
            3. Appendix A: Accelerator design considerations
                1. High-bandwidth memory, much faster than PCIe, and leverage Batching to mitigate
                2. Asynchronous programming to overcome PCIe latency, kernel scheduling overheads, and interrupt delays
                3. High performance interconnects
                4. Single-tenancy: accelerators are not often shared by multiple programs simultaneously
                5. GPU vs TPU
                    1. GPU systems tend to have small islands of NVLink-connected devices
                    2. TPU systems have thousands of devices connected all-toall
                       TPUs are restricted to run a single program at a time, with no local pre-emption

        n. related materials
            1. https://zhuanlan.zhihu.com/p/497461172
            2. https://www.zhihu.com/question/524596983
                1. https://www.zhihu.com/question/524596983/answer/2411800437
                2. https://www.zhihu.com/question/524596983/answer/2413471036
                3. 如何评价 Google 在 2022 年 3 月公开的 Pathways 架构设计？ - SIY.Z的回答 - 知乎
                   https://www.zhihu.com/question/524596983/answer/2420225275
                    1. very good article. It explains the problems to solve by PATHWAYS in TensorFlow V1, PyTorch & TensorFlow v2, JAX
                        0. A single controller to optimize a big dataflow graph, seemly a promising approach by TensorFlow V1, but actually didn't turn well
                        1. Latency of dispatching control commands
                        2. The need of gang-scheduling
                        3. the dataflow graph can be very large, optimization by a single controller is hard
                4. 如何评价 Google 在 2022 年 3 月公开的 Pathways 架构设计？ - Hsword的回答
                   https://www.zhihu.com/question/524596983/answer/2411800437
                    1. "目前的深度学习系统主要是面向a single, smallish, exclusively-owned island of accelerators，足以处理大部分常规的深度学习任务。但最近几年诞生了很多新兴的计算需求，如预训练大模型、稀疏大模型、流水线并行、NAS、多任务、多模态、异构计算等等，使得传统的SPMD显得拙荆见肘。"
            3. 解读 Pathways （二）：向前一步是 OneFlow
               https://mp.weixin.qq.com/s/N99dRgFYC9zOOcGlg0Ulsw
            
            4. Pathways Language Model (PaLM): Scaling to 540 Billion Parameters for Breakthrough Performance
               https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html
                1. Training a 540-Billion Parameter Language Model with Pathways. PaLM demonstrates the first large-scale use of the Pathways system to scale training to 6144 chips

            5. PaLM: Scaling Language Modeling with Pathways    [2022, 100 refs, Google]
               https://arxiv.org/abs/2204.02311
                1. We trained PaLM on 6144 TPU v4 chips using Pathways

            6. Ray: A Distributed Framework for Emerging AI Applications    [2018, 676 refs]
               https://arxiv.org/abs/1712.05889
                1. good paper. funding work of AI computation framework.
                   combines both task-parallel scheduling and actor-based computation model.
                   lineage based fault tolerance like RDD. millisecond level two-level bottom-up scheduler
                   overall, the ML required storage and computation are full in-memory and accelerated with TPU, GPU customized chips
                2. highlights
                    1. the first distributed framework that unifies training, simulation, and serving. all necessary components for RL applications
                    2. task-parallel scheduling and actor-based computation model
                        1. most previous frameworks choose one of the above, but only Ray combines them two
                        2. Tasks and Actor have simple programming APIs. Task for stateless computation, Actor for stateful
                        3. dynamic task graph computation are implemented with stateful Actor, and track lineage
                    3. Global Control Store (GCS)
                        1. Key-value store, with pub-sub functionality, and chained replication.
                           implemented with Redis with periodically memory flushing to disk.
                           tracks lineage information and object metadata, task status
                            1. enable every other component in Ray to be stateless
                        2. in-memory object store with Apache Arrow (not for control data but for object data)
                           objects entirely in-memory
                    4. Bottom-up Two-level hierarchical scheduler - this is the good part, novel work
                        1. need millisecond level task scheduling, a single central scheduler is not enough
                           use local schedulers and a central scheduler.
                           task first schedule on local ones, if not satisfied, pop up to central scheduler
                        2. Similar with Google Omega.
                           the global central scheduler can run multiple replicas with shared information to scale out
                    5. History
                        1. Ray starts two years ago (2018 - 2) with a Spark library
                           Spark is the BSP model (Bulk synchronous parallel, e.g. MapReduce ), less flexibility for task-parallel and no actor model.
                           Then Ray developed their own
                    6. Ray vs Spark
                        1. Ray has lower level APIs, more flexible to build distributed frameworks. Spark is more specialized for data processing. Spark API is more high level.
                        2. Ray is more Python native.
                n. related materials
                    1. https://zhuanlan.zhihu.com/p/111340572

    7. FAST'22 - 25 Years of Storage Research and Education: A Retrospective - Remzi Arpaci-Dusseau, University of Wisconsin—Madison
       https://www.usenix.org/conference/fast22/presentation/keynote
        1. Semantically-Smart Disk Systems
        2. Technology-driven Research
            1. Fundamental techs are always being altered, what's the impact to storage systems?
            2. WiscKey
            3. An ideal caching device to deliver Bp performance while seemly have Cc capacity
                1. Performance Bp vs Bc. Net bandwidth vs Hit ratio
                2. Splitting model of cache, direct reads to capacity device to maximize bandwidth of both devices - Orthus
                    1. interesting thinking here
            4. FS Semi-microkernel here - uFS

    8. Scalable Garbage Collection for In-Memory MVCC Systems    [2019, 28 refs]
       http://www.vldb.org/pvldb/vol13/p128-bottcher.pdf
        1. Very good paper. HypPer's MVCC GC algorithm design - called Steam.
           Reveals the GC problem, a survey of existing GC design in in-memory databases, and HyPer's design
           present in CMU 15-721 course https://15721.courses.cs.cmu.edu/spring2020/schedule.html
           published at 2019 VLDB and has high ref count 28
        2. highlights
            1. GC is critical to MVCC transaction performance
                1. Figure 1: too many versions slows down read transaction, while write transaction will yet add more versions
                2. Figure 3: mixed running OLAP and OLTP, i.e. long running transactions, can keep very old versions and leave a long version chain
            2. Survey of the practical MVCC GC - Table 1 - very good part
                1. Tracking Level: Txn batch, Epoch, Tuple, Transaction
                2. Frequency (precision): Batch, threshold, 1/10s, 1 min, Commit, Threshold, Version Access
                3. Version Storage: Write Set, Hash Table, Logs, Relation, Undo Log
                4. Identification: Epoch Guard, Snapshot Tracker, Txn Map, Global Txn list, Local Txn List
                5. Removal: Interspersed, Background, On-the-fly+Inter, On-creation-Inter
            3. The choice of HyPer
                1. GC garbage versions on every write transaction commit
                   this is because by evaluation, HyPer found the frequency of GC should be as high as possible
                    1. "polluters" are responsible for removal of garbage
                    2. compared to a separated GC, HyPer's way piggybacked the cost while the chain is locked anyway
                    3. from evaluation, the more thorough and fine-granular we clean our system, the less time we spend cleaning
                2. HyPer uses Undo Log to store version chain. Thus saved duplicate space.
                   and only delta is saved to further reduce the space
                   in-memory DB needs to be compact for memory size
                3. Transaction lists are ordered for fast GC
                   two lists: active transaction and their referenced versions
                              committed transaction versions lists
                   Figure 6 shows pruning version is by merging middle versions to old ones if they are not referenced
                4. Per implementation, transaction lists are separated into thread local to reduce synchronization
                   A thread only shares its minimal startTs globally
                    1. Section 5.2. Using latch-free algorithm can show worse performance than HyPer's
                       HyPer's approach eliminates most synchronization needs

    9. Improving the Reliability of Next Generation SSDs using WOM-v Codes    [2022, 1 refs, Fast22 Best paper award]
       https://www.usenix.org/conference/fast22/presentation/jaffer
        1. good paper. novel coding technique that can improve QLC flash endurance, with a cost on capacity, but still better than MLC
        2. highlights
            1. WOM codes - Write once memory code, suitable for flash device programming
            2. WOM-v codes - Figure 2 - for 4-bit QLC
                1. reduce the info bit, but remap 4-bit QLC voltages to different rewrite generations
                    1. compared using MLC, SLC by capacity/endurance trade-off, QLC+WOM-v Codecs still beneficial - Figure 13
                2. exploit that QLC programming increase voltage without erasing
                3. overheads
                    1. need extra storage overhead, but compared to the endurance added, still benefits
                    2. reduce read performance due to remapping lookup
                    3. interfere with FTL GC
            3. further optimizations
                1. GC_OPT: In an ECC protected group of pages, if only a small number of pages reached max rewrite generation, we can rewrite other remaining pages and rely on ECC to pseudo-ly "rewrite" that small number of pages - this reduces the GC needed
                    1. questions: impact to ECC recoverability? but paper says only a small number of pages as few as not being impacted
                2. No-Read (NR) mode
                    1. store recently used generation pages in chunk metadata to avoid lookup cost 

    10. Closing the B+-tree vs. LSM-tree Write Amplification Gap on Modern Storage Hardware with Built-in Transparent Compression    [2022, 4 refs, FAST22]
        https://www.usenix.org/conference/fast22/presentation/qiao
        1. Use computational SSD with transparent compression to build the new generation sparse data structure. LSM-tree may not be the best now
           comparing to Facebook MyRocks to replace MySQL engine, and a B+-tree reference implementation - WiredTiger
        2. highlights
            1. sparse data structure as a new research direction, built on Computational SSD (CSD) drives which enabled transparent compression
                1. question: what's the overhead of transparent compression in CSD level?
            2. build B+-tree on CSD with less storage overhead compared to MyRocks LSM-tree
                1. techniques
                    1. deterministic page shadowing
                        1. reduce the degree of freedom of which disk address to write pages, so to avoid write amplification to track page mapping
                    2. localized page modification
                        1. write page delta instead of the original page. dedicated a second page to pack the deltas
                    3. sparse redo logging
                        1. each new log record go to a new page, so that page read-modify-rewrite amplification is avoided
                2. questions
                    1. what is the read/write amplification overhead? but they can be proxy-ed by storage space amplification
                    2. and internal/external fragmentation due to writing half-zero pages?

    11. Removing Double-Logging with Passive Data Persistence in LSM-tree based Relational Databases    [2022, 0 refs, FAST22]
        https://www.usenix.org/conference/fast22/presentation/huang
        1. good paper. It solved the MySQL double logging issue with a practical solution, and perf evaluation shows the gain is significant. 
        2. highlights
            1. the solution - PASV - Flush Flag
                1. When LSM-tree flushes memory buffer, it's tailed with Flush Flag - <CF, TSN, LSN_first, LSN_last>
                   each LSM-tree (a column family) maintains a Local Epoch to say when data is safely flushed
                   Binlogging layer maintains a Global Epoch which is the minimal of all Local Epochs
                2. Recovery can be fast, avoiding replay binlog from beginning, by only replay from Global Epoch.
                   LSM-tree locally can further uses Local Epoch to truncate necessary recovery.
                   Recovery is done by put back KVs in LSM-tree, and reply binlog.

            4. questions
                1. IO cost of two logging. suppose logging cost is small because of small size compared to data
                    1. double logging overhead is big enough, especially the flush sync cost. See Figure 2b
                    2. note Figure 2b is generated by LinkBench, 100GB UDB-style workload
                2. why not drop binlog layer, instead the paper drops MyRocks internal logging
                    1. See P3 last paragraph. only binlog has global information. each column family goes to a different MyRocks instance
                       besides, binlog is used for replication
                3. how to maintain LSM-tree itself integrity if logging in it is removed?

    12. NyxCache: Flexible and Efficient Multi-tenant Persistent Memory Caching    [2022, 10 refs, FAST22]
        https://www.usenix.org/conference/fast22/presentation/wu
        1. good paper. Novel area that provide multi-tenancy for PMEM. The core idea is incremental feedback control loop, runtime micro experiment to measure interference
           the current implementation is built on Pelikan - Twitter's in-memory KV cache
        2. highlights
            1. problems and how to solve
                1. regulate PM access, load admission, capacity allocation
                    1. same with traditional approach, by delaying PM accesses at user-level
                    2. Algorithm 3: Proportional Resource Allocation: 
                2. obtain a client's PM resource usage
                    1. Optane DC PMM internally requires 256B aligned read size, a smaller or unligned read can cost the same with 256B
                    2. Nyx determines it by a function of current IOPS of each operation type w.r.t. its max IOPS. It needs profiling to get numbers of each operation type
                       More intricate cost models for cache instance with spatial (e.g. scan) and temporal locality (e.g. burst retries) are left for future work
                3. unfair interference
                    1. co-running read can be asymmetrically impacted by a even low throughput write neighbor
                       due to 256B align needs, a smaller access (64B) can even cause more inference
                    2. See Algorithm 2 - getLargestInterference. each candidate is throttled by a "ExperimentStep", to measure the interference
                        1. ExperimentStep cannot be too small, otherwise it cannot be told from noise
                4. application slowdown
                    1. slowdown estimation - by calculating T_along / T_share for App
                5. Discussion
                    1. Security: Nyx policies is attackable, e.g. a bad client limits its access in first ticks but putting heavy load at last 

    13. New Directions in Cloud Programming [2021, 14 refs, CIDR]
        https://www.cidrdb.org/cidr2021/papers/cidr2021_paper16.pdf
        https://www.youtube.com/watch?v=FeRg-7Sr1L8
        1. HYDRO: A PACT Programming Stack
            1. Program Semantics: Lift and Support
            2. Availability Specification
            3. Consistency Guarantees
            4. Targets for Dynamic Optimization

    14. Pigasus: Achieving 100Gbps intrusion prevention on a single server    [2022, 40 refs, OSDI20]
        https://www.usenix.org/conference/osdi20/presentation/zhao-zhipeng
        https://blog.acolyer.org/2020/11/16/pigasus/
        1. FPGA is in charge (available on SmartNICs), CPU is in supportive role.
            1. And, regular expression matching will be offloaded from the FPGA to the CPU
            2. Pigasus manages to fit everything into just 2MB of BRAM
        2. Intrusion Detection / Prevention System (IDS/IPS), line rate 100Gbps, hundreds of thousands of concurrent flows, matching packets against tens of thousands of rules
        3. Pigasus is designed to be compatible with Snort rulesets
           evaluated using the Snort Registered Ruleset (about 10K signatures

    15. SepBIT: Separating Data via Block Invalidation Time Inference for Write Amplification Reduction in Log-Structured Storage    [2022, 11 refs, FAST22, Alibaba]
        https://www.usenix.org/conference/fast22/presentation/wang
        1. good paper. It shows some improvement for data grouping design to save LSM-tree GC traffic.
           For user written blocks, the indicator of block lifespan is its rewritten source block's lifespan
           For GC rewritten blocks, the indicator of block residual lifespan is the block's age till now
           Overall, temperature information is still embedded in the Classification above. A block will go from a period of regular user update, to the next period of cooling down. This should right be where to optimize GC (but not fully leveraged by the paper nor verified the modeling).
        2. highlights
            1. public block-level I/O traces from two cloud block storage systems, Alibaba Cloud [23] and Tencent Cloud [46]
                1. This is useful
            2. Observations
                1. User-written blocks generally have short lifespans
                    1. short-lived blocks (Class 1) written near the same time have similar BITs
                2. Frequently updated blocks have highly varying lifespans
                    1. frequently updated blocks with similar update frequencies have high variance in their lifespans
                3. Rarely updated blocks dominate and have highly varying lifespans
                    1. temperature-based data placement schemes cannot effectively group the rarely updated blocks with similar BITs
            2. SepBIT design
                1. key intuitions
                    1. Any user-written block that invalidates a short-lived block is also likely to be a short-lived block
                    2. Any GC-rewritten block with a smaller age is likely to have a short residual lifespan
                2. how to separate blocks with BIT
                    1. Class 1-2 maps to User-written blocks
                        1. Class 1 for short-lived blocks. Class 2 for long-lived blocks
                        2. If a new block is written, BIT assumes it has infinite lifespan
                           If it's an old block rewritten by user, the old block is invalidated, the new block is assigned the lifespan of the old block
                        3. NOTE: the lifespan is measured by # user bytes written, as normalized to how fast the user writes
                    2. Class 3-6 maps to GC-rewritten blocks
                        1. Blocks from Class 1 are GC rewritten to Class 3
                        2. "Age" defined as the timespan since the block's last user write time until the block is rewritten by GC (i.e. invalidation timespan + GC delay?)
                           Age infers "Residual lifespan" which determines the Class 4-6
                    3. In summary
                        1. Age of user-written blocks: user written time -> invalidation time due to user rewrite
                           Age of GC-written block: last USER written time -> current GC rewritten time
                        2. Time is measured by total # bytes written by the whole workload, rather than world clock
                        3. The next inferred invalidation time, i.e. BIT, is determined by Age
                           The classification is two level
                             1) User written vs GC rewritten
                             2) Inside (1), further cut by BIT
                3. tracking per block age metadata
                    1. stored last user rewrite time on disk along with per block metadata.
            n. my questions
                1. how much short-lived blocks are there in total?
                2. how much user written blocks vs GC rewritten blocks are there in total?
                   But this must be wrong, temperature info must be considered
                3. Grouping data by GC generation should also approach the same idea
                   in GC-rewrite blocks, temperature info is incorporated, that less updated blocks will have a higher Age and go to a higher bucket
                    1. it contradicts with Observation 3?
                       Or the "Rarely updated blocks" map to "GC rewrite blocks" in Figure 6, and the "highly varying lifespan" is further cut to Class 3-6
                       Then that's said then temperature is still a valid indicator to group data

        -------- Re-read 20230708 --------

        1. Targeting "Alibaba Cloud ESSDs", which runs on "Alibaba Cloud Pangu". ESSD is a block-level volume as an append-only log.
           SepBIT is deployed at Alibaba Cloud ESSD. Trace analysis shows reduced overall WA of existing schemes by 9.1-20.2%. Interesting paper.
            1. My questions
                1. If SepBIT is deployed on prod, why the evaluation is using trace analysis? It should show prod data.
        2. Observations
            1. O1: User-written blocks generally have short lifespans
            2. O2: Frequently updated blocks have highly varying lifespans
            3. O3: Rarely updated blocks dominate with highly varying lifespans
            4. Temperature-based placement (e.g., via access frequencies) are ineffective in BIT inference
            5. User written blocks
                1. Short-lived blocks (Class 1) written near the same time have similar BITs
                2. Remaining long-lived blocks (Class 2) span large BIT ranges
            6. GC-rewritten blocks
                1. Short-lived blocks (Class 3) identified in user-written blocks
                2. Blocks with similar BITs inferred are grouped to Classes 4-6
        3. SepBIT Design
            1. Intuition
                1. Any user-written block that invalidates a short-lived block is also likely to be a short-lived block
                2. Any GC-rewritten block with a smaller age is likely to have a short residual lifespan
            2. Implementation
                1. ℓ: average segment lifespan of collected segments in Class 1
                2. Classes 1 and 2: Use ℓ as lifespan threshold for user-written blocks based on the lifespans of their invalidated blocks
                3. Classes 4-6: Use 4ℓ and 16ℓ as age thresholds for GC-rewritten blocks according to their ages


    16. ByteGraph: A High-Performance Distributed Graph Database in ByteDance    [2022, 0 refs, VLDB22, ByteDance]
        1. very good paper. can be used as a reference architecture.
           Graph database by Gremlin API built atop RocksDB sharded by consistent hashing with geo replication and supports distributed transaction with 2PC
           Features in memory-disk tiered, super vertex edge-list B-tree and secondary index
           Today complex storage systems can easily be built from RocksDB at Internet Companies
           Facebook previously uses MySQL to build graph DB, now ByteDance moved to RocksDB and Gremlin API
           The comparing and analysis to related works are also good to look
        2. highlights
            1. key motivations of ByteDance and drawbacks of existing graphDBs
                1. ByteDance
                    1. Serving OLAP, OLTP, OLSP.
                        1. OLAP: multi-hop graph traversal queries, large intermediate results
                        2. OLTP: transaction, high write throughput
                        3. OLSP: realtime and data freshness, high concurrent writes
                    2. hot data in-memory, cold data on-disk
                        1. edge-tree: btree-like structure, persisted in KV store
                    3. super vertex: a vertex with many edges, and update very frequently
                        1. edge-tree
                    4. burst access
                        1. light/heavy thread pool isolation
                        2. weighted consistent hashing
                    5. scalability and resilience
                        1. geographic replication (eventual consistency)
                        2. decoupling computation and storage
                        3. partition graph by consistent hashing
                           ensures both vertex and its edge-tree are assigned to the same BGS instance
                    6. API
                        1. Gremlin APIs
            2. Data organization
                1. Vertex storage and Edge storage - backed by KV store
                    1. Vertex: KV: key => vertex property
                    2. Edge: adjacency list: KV: <vID, vType, eType, dir> => adjacency list => list of <dest vID, dest vType> + edge properties
                        1. edge-tree for super vertex, work like B-tree
                        2. edge properties are compressed to save storage footprint
                        3. WAL: edge tree as the flush granularity, tracked by Dirty List
                        n. my question
                            1. talking about B-tree, assume the KV is backed by RocksDB
                               the edge tree can be simply implemented as another RocksDB instance
                                1. WAL will be readily as the LSM-tree's WAL itself
                                2. By far as talked, the edge tree implementation is just like a B+-tree style LSM-tree
                                3. and RocksDB provides atomic local transaction to update vertex + its edge tree
                                4. secondary edge-tree is just the secondary index of RocksDB
                            2. the second level B+-tree design looks just like how Pangu uses HBase + second level B+-tree to run VM disks (probably)
                            3. ByteGraph should be using RocksDB/TerarkDB. TerarkDB is known also built by RocksDB
                               " Existing KV stores (e.g., RocksDB [12], TerarkDB [29]) can be used in this layer, which is treated as a black box in ByteGraph."
                            3. in future, a GraphDB should allow user to specify the vertex/edge organization format to favor user's traffic patterns
                               see the analysis on Related Works
            3. Query processing
                1. Both Rule-based optimizer and Cost-based optimizer
                2. Cache query results. Periodical update results to maintain an eventual consistency
                3. BGE distribute and aggregate a query to multiple BGS according to graph partitioning
            4. More optimizations
                1. dynamic heavy/light thread pool, with dynamic adjusting thread count
                2. Adaptive secondary edge tree, and dynamic deciding whether worth to build
                    1. it's the secondary index implemented by B+-tree
            5. Distributed transaction processing
                1. ByteGraph supports ACID  Read-Committed (RC) isolation level
                2. leverage the two-phase commit (2PC) for distributed transaction
                3. ByteGraph does not support MVCC, the write intent acts as write lock
            6. High availability
                1. All BGE maintains the same consistent hash ring, and monitors every BGS
                   redirect requests to the next BGS (weighted) if BGS down
                    1. my questions
                        1. seems the persistent data is ensured in underlying shared storage, so BGS no need for replication? 
            7. Geo replication
                1. ByteGraph uses HLC for clock synchronization
            8. Related works
                1. AWS Neptune [8] and Alibaba GDB [6] only use one (master) machine to handle write operations and thus cannot scale to handle high concurrent writes in our OLSP and OLTP workloads
                2. while Azure CosmosDB [9] stores graph data in a document store where super-vertices are managed as large JSON documents which leads to high latency in data access.
                3. Open source graph databases such as ArangoDB [4], AgensGraph [3], Neo4j [10] and JanusGraph [5] generally have poor scalability and cannot satisfy the high throughput and low latency required in handling ByteDance’s workloads.
                4. A1 [15] and TigerGraph [20] focus on inmemory architectures to provide low query latency, but in-memory systems are hard to be scaled to handle large graphs at ByteDance, while storing the entire graph data in memory is also a waste of the resource as not all graph data are needed for query processing at all times

        n. related materials
            1. 论文速读：ByteGraph: A High-Performance Distributed Graph Database in ByteDance
               https://zhuanlan.zhihu.com/p/563890069
                1. "字节内多个不同应用如抖音，TikTok，今日头条等都大量采用图数据进行内容推荐，风险管理等。"
                2. 为什么目前开源、商用的各种图数据库不能满足字节的需求
                    1. 必须采用secondary storage+cache的两层结构
                       提高cache缓存命中率和在有易失的cache层后满足OLTP的事务要求将是设计重点
                    2. a.读访问量大; b.写访问量大;c.会在某些特定时候有burst I/O
                       这三个特定就决定了byteGraph需要选择存算分离的架构
                    3. 存在一些超级顶点（一个顶点有超级多变）
                        1. byteGraph采用了edge-tree树状结构来动态存储每个节点对应边的信息
                        2. 采用LRU List缓存热点数据，提高访问命中率
                        3. 用WAL和Dirty List来处理写事务的相关操作
                        4. byteGraph提出了Secondary Edge tree的优化概念
                    4. 为了避免heavy scan I/O（比如一些超级用户的查询）占用过多的线程池资源，
                       byteGraph把线程池分为Light和Heavy两个，从而做到了heavy workload的线程资源隔离
                        1. bytegraph同时通过监控heavy和light线程池workload的强弱来动态调整两个线程池的线程比例，从而避免昂贵的retry过程

            2. A Gentle Introduction to Graph Neural Networks
               https://distill.pub/2021/gnn-intro/

            3. Bytedance Distributed Graph Database Based On Brpc In Practice
               https://www.youtube.com/watch?v=j18qQsV5pr4
                1. brpc is widely used

    17. Compaction-Aware Zone Allocation for LSM based Key-Value Store on ZNS SSDs    [2022, 0 refs, HotStorage22]
        https://discos.sogang.ac.kr/file/2022/intl_conf/HotStorage_2022_H_lee.pdf
        https://www.hotstorage.org/2022/slides/hotstorage22-paper12-presentation_slides.pdf
        1. SSTs with overlapping key ranges should be placed to the same zone.
        n. related materials
            1. HotStorage2022-Compaction-Aware Zone Allocation for LSM based Key-Value Store on ZNS SSDs
               https://zhuanlan.zhihu.com/p/563180541 

    18. ZNS+: Advanced Zoned Namespace Interface for Supporting In-Storage Zone Compaction    [2021, 17 refs, FAST21, Samsung]
        https://www.usenix.org/conference/osdi21/presentation/han
        https://www.youtube.com/watch?v=QjrPiWrfM3k
        1. Host GC needs to copy data, it has higher overhead than SSD doing GC, because is transferred through PCIe
            1. solution: zone_compact command to copy block inside of SSD. it offloads compaction from host to SSD device
        2. threaded logging writes blocks to holes (invalidated, obsolete space) in existing dirty segments
            https://www.usenix.org/system/files/conference/fast15/fast15-paper-lee.pdf
            1. how to apply this for ZNS SSD? TL_open command. It will transparently do copy-merge move the blocking being randomly written to a new block (internal plugging) See Figure 5
                1. my question: isn't this lost the benefit of threaded logging already? which assumes no new blocks being used to save storage space
        3. copyback-aware block allocation for segment compaction
            1. attempts to allocate the destination LBA of a data copy such that both the source LBA and destination LBA of the target data are mapped to the same flash chip
        4. Adapting F2FS to run on ZNS SSD

        -------- Updated 20240712 --------

        1. Good paper, 65 refs now at 2024.07. The key innovation is to introduce
            1. intra-SSD data movement - zone_compact command. It's like a middle land of traditional SSD where SSD does GC itself, and ZNS SSD where GC forces data transfer between host and SSD.
            2. TL_open command - open zones for threaded logging. to assist F2FS threaded logging. The TL_opened zones can be overwritten without reset, and the overwrite requests can be sparse sequential. 
                1. F2FS: "Threaded logging writes blocks to holes (invalidated, obsolete space) in existing dirty segments. This policy requires no cleaning operations, but triggers random writes and may degrade performance as a result."
                   https://www.usenix.org/system/files/conference/fast15/fast15-paper-lee.pdf
            3. Copyback-aware block allocation - moves data within a flash chip without off-chip data transfers
            4. hybrid segment recycling - selects either threaded logging or segment compaction based on their reclaiming costs

    19. ZNS: Avoiding the Block Interface Tax for Flash-based SSDs    [2021, 35 refs, ATC21]
        https://www.usenix.org/conference/atc21/presentation/bjorling
            1. useful paper to understand ZNS
            2. highlights
                1. introducing ZNS, and example implementation of F2FS and RocksDB
                2. the block interface tax
                    1. GC caused performance unpredictability
                    2. Space needed in capacity over-provisioning
                    3. compared to open-channel SSD
                        1. OCSSD forces host to directly manage media-specific characteristics like wear-leveling, specific media failure characteristics. hard to adopt
                        2. ZNS SSD only offload GC to host, media reliability still owned by SSD
                    4. zone storage model originally introduced from SMR
                    5. Stream SSD, SSD with Stream support
                3. details about ZNS SSD
                    1. active zone count is limited. it's limited by adding extra power capacitors.
                       each zone needs to track write pointer position, which is recoverable from failure
                4. ZenFS
                    1. Select zone for RocksDB by SST levels, and separate WAL zones. Write-lifetime hint
                    2. limit concurrent compactions due to active zone count limit

            n. related materials
                1. Ceph SeaStore has support for ZNS
                    1. Seastore: Next Generation Backing Store for Ceph
                       https://www.youtube.com/watch?v=JZ815DOcKZ4
                        1. Rewrite IO path with SeaStar
                            1. Preallocated cores, one thread per core, shard all data structure and work across cores, no locks and non blocking
                            2. Message passing between cores
                            3. Polling for all IO
                        2. DPDK, SPDK
                        3. Async coroutine continuation programming
                        3. Why
                            1. More about IOPS per CPU core. Context switching is too expensive. Reduce CPU usage processing IO
                    2. Seastore - ZNS
                        1. any work done for the append-only zone semantic?

                2. Ceph SeaStore dev doc
                   https://docs.ceph.com/en/quincy/dev/seastore/
                    1. Target NVMe devices, not primarily concerned with HDD
                    2. SPDK for user-space IO
                    3. SeaStore future programming model
                    4. Zero or minimal data copying on read and write path with SeaStar-based messenger using DPDK
                    5. GC: https://docs.ceph.com/en/quincy/dev/seastore/#gc
                3. Ceph Crimson/Seastore Meeting 2022-06-07
                   https://www.youtube.com/watch?v=r-G4mdDK3I0

    20. F2FS: A New File System for Flash Storage    [2015, 467 refs, FAST15]
        https://www.usenix.org/system/files/conference/fast15/fast15-paper-lee.pdf
        1. high reference count paper filesystem for flash storage. merged into linux kernel. used extensively for Android.
        2. highlights
            1. Flash with random writes
                1. Mobile phone using SQLite trigger many random writes due to fsync
            2. Multi-head logging
                1. six major log areas = Node logging / Data logging * Cold / Warm / Hot
                2. temperature classification
                    1. Hot: Direct node blocks and data blocks for directories
                    2. Warm: Direct node blocks and data blocks for regular files
                    3. Cold: Indirect node blocks, data block moved by cleaning, cold data blocks specified by user, multimedia file data
                3. GC cleaning
                    1. rather than explicitly migrate valid blocks, F2FS simply load them into page cache and mark dirty. kernel work thread will flush them reusing existing optimization like batching
                4. Threaded logging
                    1. in capacity pressure, threaded logging writes blocks into holes in existing dirty segments, involving random writes but no requiring prehand cleaning
            n. my questions
                1. so .. this is another paper suggesting SSD also needs sequential writes. like RocksDB's suggestion
        n. related materials
            1. Difference between F2FS and EXT4
               https://sparrowsnews.com/2019/08/13/difference-between-f2fs-and-ext4-file-system/
                1. F2FS is log-structured FS, optimized for mobile phones, fauthlash friendly. continuously developed and making stable now, included in linux kernel since V3.8
            2. FAST '15 - F2FS: A New File System for Flash Storage
               https://www.youtube.com/watch?v=HgCvcMQnJQ0
                1. random writes is bad for flash
                    1. free space fragmentation
                    2. sustained random write performance degrade
                    3. lifetime reduced
                2. Flash-friendly on-disk layout
                    1. data packed and cleaned in unit of FTL GC unit / zone
                    2. multi-head logging for hot/cold data separation
                3. cost effective index structure
                    1. today's problem
                        1. indirect inode extra jump
                        2. one big log
                        3. wandering tree modify propagation
                    2. indirect node => Node address table (NAT) lookup => Direct node => file data
                        1. like Bw-tree Page Table to solve Wandering tree issue
                4. multi-headed logging
                    1. data temperature classification
                    2. zone-aware log allocation
                    3. Multi-stream interface
                5. GC cleaning
                    1. section aligned with FTL GC unit
                    2. victim selection: Greedy, Cost-benefit
                6. Threaded logging
                    1. reuse invalid blocks in dirty segments, no need GC cleaning

    21. OceanBase: A 707 Million tpmC Distributed Relational Database System    [2022, 0 refs, VLDB22]
        1. OK.
        2. highlights
            1. Macroblock, 2GB, is the basic unit of GC.
                1. If modified, a Macroblock will be rewritten.
                   Otherwise, the Macroblock will be reused in the new baseline data without any IO cost
            2. Replica types
                1. Full replica: Baseline data, mutation increment, redo logs
                2. Data replica: Baseline data, redo logs. Copy minor compactions from a full replica on demand
                3. Log replica: Redo logs only. OB deploys 2 full replicas and 1 log replica to save storage capacity.
            3. Paxos-based 2PC
                1. A paxos group to provide timestamp.
                2. Like Spanner, use Paxos to ensure reliability of participants in 2PC
                3. Like CockroachDB, uses Parallel Commit and Write Pipelining
        n. related materials
            1. The Architecture Overview of OceanBase DataBase - Charlie Yang
               https://www.youtube.com/watch?v=rPPZF26x7Xs
            2. 国产数据库OceanBase，如今入选了国际顶会VLDB 2022
               OceanBase: A 707 Million tpmC Distributed Relational Database System
               https://mp.weixin.qq.com/s/MI5X1AdBiv05ScHJKbbFhA
                1. a nice chinese transalation of the paper

    22. Partial-Parallel-Repair (PPR): A Distributed Technique for Repairing Erasure Coded Storage    [2016, 91 refs]
        https://about.att.com/ecms/dam/sites/labs_research/content/publications/SDN_Partial-Parallel-Decoding_PPR.pdf
        1. Referenced in "Repair Pipelining" paper. See "Repair Pipelining" paper Figure 2b.
           PPR let helper nodes talk to helper nodes to add up partial rec-reads first. it distribute load across helper nodes
        2. "Repair Pipelining" paper further adds pipelining to PPR. Total repair time is reduced
        n. Related materials
            1. OpenEC: Toward Unified and Configurable Erasure Coding Management in Distributed Storage Systems
               https://www.usenix.org/conference/fast19/presentation/li
                1. referencing Partial-Parallel-Repair (PPR)
            2. Repair Pipelining for Erasure-Coded Storage
               https://www.usenix.org/conference/atc17/technical-sessions/presentation/li-runhui
                1. another work referenced by OpenEC paper

    23. Qumulo Distributed, Scale-Out File System On AWS - Reference Architecture
        https://qumulo.com/wp-content/uploads/2022/02/AWS-and-AWS-Outpost-Reference-Architecture-White-Paper-1.pdf
        1. A white paper about Qumulo AWS native file storage.
        2. Moving Data Between Qumulo and Amazon S3
        3. How to Implement Erasure Coding
           https://qumulo.com/blog/how-to-implement-erasure-coding/

    24. Online Encoding for Erasure-Coded Distributed Storage Systems    [2017, 0 refs]
        https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7979843
        1. inline EC. sequential append with technique similar to parity logging

    25. FaaSNet: Scalable and Fast Provisioning of Custom Serverless Container Runtimes at Alibaba Cloud Function Compute    [2021, 26 refs, ATC21]
        https://www.usenix.org/conference/atc21/presentation/wang-ao
        1. Fast container provisioning for custom-container-based FaaS
        2. highlights
            1. "Our FaaS infrastructure uses a dynamic pool of resourceconstrained VMs to host containerized cloud functions for strong isolation"
            2. Cold start issue: as it requires the FaaS provider to fetch the image data and start the container runtime before executing the function
            3. Function Trees
                1. Each function has a separated FT. Tree nodes are VMs. FT is balanced binary tree.
                   FT is used to distribute container image. It needs to limit parallel download, and needs to limit how far an image traverses from root to leaf
                n. questions
                    1. what's the point of FT? Suppose a leaf VM needs image, it can directly ask from any ancestor that is idle, rather than burden every middle VM at tree trunk and root
        n. related materials
            1. 2021年技术盘点-Serverless架构
               https://zhuanlan.zhihu.com/p/459994252
                1. "在加速镜像的分发速度方面，常见的业界成熟的 P2P 方案没有做到 function 级别的感知，并且集群内的拓扑逻辑大多为全连接的网络模式，对机器的性能提出了一定需求，这些前置设定不适配 FC ECS 的系统实现，为此设计并提出了一个具有高伸缩性的轻量级系统中间件FaaSNet，FaaSNet利用到镜像加速格式进行容器分发，目标作用场景是 FaaS 中突发流量下的大规模容器镜像启动（函数冷启动），FaaSNet 的核心组件包含 Function Tree (FT)，是一个去中心化的、自平衡的二叉树状拓扑结构，树状拓扑结构中的所有节点全部等价。FaaSNet 可以根据 workload 的动态性实现实时组网已达到 function-awareness，无须做预先的 workload分析与预处理，进而帮助Serverless平台解锁高伸缩性和快速的镜像分发速度技术瓶颈，赋能自定义容器镜像场景的更为深入和广泛的应用"


10. Reading: Recent papers piled up: Power saving erasure coding and storage systems
    1. A Spin-Up Saved is Energy Earned: Achieving Power-Efficient, Erasure-Coded Storage    [2008, 50 refs]
       https://www.usenix.org/legacy/event/hotdep08/tech/full_papers/greenan/greenan_html/
       https://www.usenix.org/legacy/events/hotdep08/tech/full_papers/greenan/greenan.pdf
        1. power-aware coding
          1. The crux of power-aware coding is to prevent spinning up inactive disks when servicing read requests by treating each inactive disk as an erasure.
            1. another point is MDS codecs are worse than less dense (but less durability) codecs, w.r.t. the former needs more active disks to do rec-reads
          2. write group is per code instance, to serve writes.
             Every disk in the system must be a member of at least one write group 
             Exactly one write group per code instance will be active at a time
          3. transient activation is to serve reads. it involves disks not in the current activate write group. it will be deactivated after fixed period
             There may be cases where a transient activation may be more power efficient than reconstructing the data from active disks
        n. related materials
          1. Reliability and Power-Efficiency in Erasure-Coded Storage Systems
            1. It's the technical report of the parent paper. It's the doctor thesis of Kevin M. Greenan. It's a follow up work based on Pergamum
          2. Power Consumption in Enterprise-Scale Backup Storage Systems    [2012, 52 refs]
             https://www.usenix.org/legacy/event/fast/tech/full_papers/Li.pdf
            1. another work of Kevin M. Greenan. to provide power consumption measurements from real-world, enterprise-scale backup systems
            2. key findings - Disk enclosure also needs attention in power saving
              1. Observation 1: The idle controller power consumption is still significant
              2. Observation 2: Whereas idle controller power consumption varies between models, normalized watts per byte goes down with newer generations.
              3. Observation 7: Disk power-down may be more effective than disk spin-down for both ES20 and ES30
              4. Observation 5: The idle power consumption varies greatly across enclosures with new ones being more power efficient.
              5. Observation 8: Disk enclosures may consume more power than the drives they house. As a result, effective power management of the storage subsystem may require more than just disk-based power-management.
            3. existing systems are not achieving energy proportionality [2, 4, 12, 29, 30], which states that systems should consume power proportional to the amount of work performed.

    2. A reliable and energy-efficient storage system with erasure coding cache    [2017, 0 refs]
       https://link.springer.com/article/10.1631/FITEE.1600972

    3. RELIABILITY AND POWER-EFFICIENCY IN ERASURE-CODED STORAGE SYSTEMS    [2009, 41 refs]
       https://www.crss.ucsc.edu/media/pubs/380cbcb0af45adb86d11a0b0325773ffba5d08f5.pdf
        1. power-aware coding. A follow up work of Pergamum
        2. Chapter 8: Trading Reliability and Power-Efficiency using Power-Aware Coding
          1. Storage accounts for roughly 27% of a data center’s power budget
          2. read requests to inactive disks can be handled with rec-reads, and compared with whether activating the disk is more saving
          3. write group to serve writes while managing disk inactive. Figure 8.4 two different architectures
        n. related materials
          1. Pergamum: Replacing Tape with Energy Efficient, Reliable, Disk-Based Archival Storage    [2008, 176 refs]
             https://www.usenix.org/legacy/event/fast08/tech/full_papers/storer/storer_html/
              1. also published at UC Santa Cruz

    4. An Energy-Saving Method for Erasure-Coded Distributed Storage System    [2015, 0 refs]
       https://www.researchgate.net/publication/314693667_An_Energy-Saving_Method_for_Erasure-Coded_Distributed_Storage_System
       https://link.springer.com/content/pdf/10.1007/978-3-319-11104-9.pdf#page=269
        1. Put nodes in queue to sleep. If the node has data needed for rec-read, migrate to another node

    5. Improving coding performance and energy efficiency of erasure coding process for storage systems-a parallel and scalable approach    [2016, 5 refs]
       https://ieeexplore.ieee.org/document/7820376
        1. concurrent and parallel erasure coding with MPI to leverage task parallelism property from a multicore computing system

    6. On the Latency and Energy Efficiency of Erasure-Coded Cloud Storage Systems    [2014, 4 refs]
       https://arxiv.org/abs/1405.2833
        1. model analysis
        2. Fig. 9: Energy efficiency increases and attains a maxima as number of servers is increased

    7. Efficient Erasure Correcting Codes    [2001, 1371 refs]
       https://www.cs.yale.edu/homes/spielman/PAPERS/eraseIT.pdf
        1. LDPC codec. 
        2. In [10] it is shown that for a random bipartite graph without message nodes of degree one or two there is a constant ε depending on the rate of the induced code and on the degrees of the message nodes such that the graph is an (ε, 1/2)-expander with high probability
           https://www.cs.cmu.edu/afs/cs/project/pscico-guyb/realworld/www/slidesS14/ldpc-amin.pdf

    8. Lazy Means Smart: Reducing Repair Bandwidth Costs in Erasure-coded Distributed Storage    [2014, 92 refs]
       http://www.cs.cornell.edu/lorenzo/papers/Silberstein14Lazy.pdf
        1. Reduce CRS(14,10) aggregated repair bandwidth to the same level of 3-replica, while increasing the amount of degraded stripes by 0.1 percentage points.
           Figure 1 is the key trade-off between durability vs repair bandwidth. The paper is designing a mechanism for the trade off
        2. mechanisms (Lazy Recovery)
            1. schema II
               for permanent disk/node failure, trigger repair immediately
               for others, delay repair until r fragment failed. no matter how long time waited 
            2. schema III
               a system-wide limit on the number of degraded stripes with permanently lost blocks
        3. exploits
            1. repair two fragments cost almost the same with repair one block
            2. dead node may be transient and can come back later
            3. Figure 1. At the edge, slightly reduce durability, may cut repair bandwidth by half
        4. questions
            1. given a node failure, how to distinguish it's permanent or not? a practical way is to wait tens of minutes. then the method degenerates to delay then repair  
        n. related materials
            
            1. Piggiback Code: A Solution to the Network Challenges of Data Recovery in Erasure-coded Distributed Storage Systems: A Study on the Facebook Warehouse Cluster    [2013, 300 refs, Facebook]
               https://www.usenix.org/conference/hotstorage13/workshop-program/presentation/rashmi
                1. Based on RS(10,4) but reduce 30% repair IO at both network and disk
                   simple hand crafted regenerating code but not aiming to the lower bounds
                   Same storage overhead, same fault tolerance with RS, does require exponential block count growing with codec length
                   PiggybackedRS codes (like RS codes) are MDS and are hence storage optimal, whereas LRCs are not
                   good paper, at that it's simple and with well illustrated
                2. highlights
                    1. Step 1: Take RS code with identical parameters  
                    2. Step 2: Add carefully designed functions from one byte stripe on to  another
                      – retains same fault-tolerance and storage overhead  
                      – piggyback functions designed to reduce amount of download and IO for recovery
                3. General theory and algorithms:
                  1. K.V. Rashmi, Nihar Shah, K. Ramchandran, “A Piggybacking Design Framework for Read-and Download-efficient Distributed Storage Codes”, in IEEE International Symposium on Information Theory (ISIT) 2013.
                     https://ieeexplore.ieee.org/ielaam/18/8011574/7949040-aam.pdf
                4. questions
                  1. does it work for LRC?

    9. Erasure Coding for Ultra-Low Power Wireless Networks    [2019, 0 refs]
       https://ieeexplore.ieee.org/abstract/document/8764455
        1. this paper proposes a solution that simultaneously reduces encoding-decoding computational complexities as well as reception redundancy, so that the total energy cost of the network can be kept low

    10. Linux on the Road: Prev Appendix E. Dealing with Limited Resources or Tuning the System Next: E.7. Power Saving Techniques
        https://tldp.org/LDP/Mobile-Guide/html/mobile-guide-p6a5s7-power-saving-techniques.html

    11. Seagate: Technology Paper: Reducing Storage Energy Consumption by up to 75%
        https://www.seagate.com/files/docs/pdf/whitepaper/tp608-powerchoice-tech-provides-us.pdf
        1. Now Seagate has taken hard drive power management to the next level with its new PowerChoice technology
           active power condition, idle A power condition, idle B, idle C, Standby Z power condition, Standby Y.

    12. Power consumption of CPU, memory, network, and disk for various computing processes
        https://www.researchgate.net/figure/Power-consumption-of-CPU-memory-network-and-disk-for-various-computing-processes-19_fig1_327203171
        1. disk only accounts for a tiny portion. NIC < Memory < CPU are the big parts
           it's a nice chart
        2. the nice chart comes from
            Full-System Power Analysis and Modeling for Server Environments
            https://d1wqtxts1xzle7.cloudfront.net/40084315/2006.mantis.mobs-libre.pdf?1447726044=&response-content-disposition=inline%3B+filename%3DFull_system_power_analysis_and_modeling.pdf&Expires=1669972043&Signature=DhnOQjZmkuXrlGxoiEQquK-Ar~~sfsItmrh8eH~6SO-PRUBxLCn-QJ6EfZ0y1dhbq1yVrC-oeufjjNWU246uARNvNqsRWyFUHGh7t0k0whC~v3d16BPIqMp3U4Xg2Bh8tMbgNu1CqnUpVvvqrmhSEvjNMYeGvyn2KbtU-vEwK1TdDLnL4R81X6JszU54vd6mPFn5~hiuJDx3IwHwWfEueV0dz83Bz3VVNZeuY6xQFK0jEIgDvy5IO1bESDKgz8D2Icl8TzD47bx39cmR3t8JzxgUMYGd1E4mmPrBsLAuKG-jtntTu5kJ2Nj5HjoLeVMd3bs4MiSI8TVwkTRxJDmPWA__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA

    13. The Problem of Power Consumption in Servers
        https://www.infoq.com/articles/power-consumption-servers/
        1. Overheated parts will generally have a shorter maximum life-span. Shorter component lifespan can produce sporadic problems, system freezes, or even system crashes
        2. useful guide that covers full aspects
        n. related materials
          1. Optimizing server energy efficiency
             https://www.techtarget.com/searchdatacenter/tip/Optimizing-server-energy-efficiency
              1. A 500W server costs less than 3000 USD to buy. In a datacenter with PUE = 2.0, it needs 1KW to run (including cooling). 1KW in 1 year adds up to 8760kWh. With 11.5 cent per kWh, it sums to 1000 USD per year. After 3 years, you pay more money in power than buying the server itself. 
              2. useful guide about server optimizing power consumption at each component
          2. 6 ways to increase energy efficiency in data centers
             https://www.techtarget.com/searchdatacenter/tip/Four-ways-to-reduce-data-center-power-consumption
              1. SSDs generally consume far less power than hard disks and deliver a greater number of IOPS
          3. How to design and build a data center
             https://www.techtarget.com/searchdatacenter/How-to-design-and-build-a-data-center

    14. A cloud server energy consumption measurement system for heterogeneous cloud environments    [2018, 37 refs]
        https://www.sciencedirect.com/science/article/abs/pii/S0020025518306364
        1. measure CPU/memory/DRAM/disk power usage. PowerModel (this paper) is more accurate than LinearModel.
           model inputs are cache misses, current system memory footprint, disk read/write bytes, disk idle/query/transmission time, disk seq/random portion, 
           results show they closely matched
        n. related materials
          1. How much power does a hard drive use?
             https://superuser.com/questions/565653/how-much-power-does-a-hard-drive-use
             https://www.quora.com/How-much-power-does-an-HDD-use
          2. Drives with low idle power consumption
             https://www.reddit.com/r/DataHoarder/comments/tuckil/drives_with_low_idle_power_consumption/
          3. Designed for your business – 1 Petabyte of Online Storage – 500 Watts
             https://www.toshiba-storage.com/trends-technology/designed-for-your-business-1-petabyte-of-online-storage-500-watts/
              1. A petabyte (1000TB) of online HDD storage can now be served with the latest 16TB enterprise capacity HDDs in a 4U-JBOD with less than 500W power consumption

          5. Modeling Hard-Disk Power Consumption    [2003, 305 refs]
             https://www.usenix.org/legacy/event/fast03/tech/full_papers/zedlewski/zedlewski_html/
              1. Dempsey, a disk simulation environment that includes accurate modeling of disk power consumption, validated for two mobile hard disks, such as MP3 players
              2. Disk Power Management
                1. the question is when the disk should be put to sleep to minimize power consumption with little impact on performance
                2. several approaches
                  1. the impact of aggressively spinning down disks when the time since last I/O request exceeds some threshold
                  2. Algorithms for dynamically varying the spin-down threshold in response to changing user behavior and priorities
                  3. two implicit assumptions.
                    1. One is that a disk has only two distinct power levels: active and idle.
                    2. The second is that an active disk always consumes power at the same rate.
                  4. the effect of various file system attributes, like data layout policy, burstiness, background data reorganization algorithms, etc., on disk energy consumption
              3. Dempsey uses the DiskSim software to model the execution of a given trace on a given disk
                1. in extreme detail, including modeling different stages of the execution, namely, seeking, rotation, data transfer and idle periods
                2. many disks have four modes of operation: active, idle, standby and sleep.

    15. Energy-Saving Techniques for Disk Storage Systems
        https://www.taylorfrancis.com/chapters/edit/10.1201/b11643-14/energy-saving-techniques-disk-storage-systems-jerry-chou-jinoh-kim-doron-rotem
        1. As prices of disks are getting cheaper in terms of dollars per gigabyte, the prediction is that the energy costs for operating and cooling these rotating disks will eventually outstrip the cost of the disks and the associated hardware needed to control them
        2. Currently it is estimated that disk storage systems consume about 25%–35% of the total power used in data centers

    16. Energy efficient and reliable storage disks    [2008, 1 refs]
        https://www.researchgate.net/publication/220996252_Energy_efficient_and_reliable_storage_disks
        1. we determine the safe utilization levels for the disks to operate with minimum probability failure rates while also conserving energy 
```