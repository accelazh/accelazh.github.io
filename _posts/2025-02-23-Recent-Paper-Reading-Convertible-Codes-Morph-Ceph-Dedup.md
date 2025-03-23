---
layout: post
title: "Recent Paper Reading: Convertible Codes, Morph, Ceph Dedup"
tagline : "Recent Paper Reading: Convertible Codes, Morph, Ceph Dedup"
description: "Recent Paper Reading: Convertible Codes, Morph, Ceph Dedup"
category: "Paper Reading"
tags: [storage, paper, cloud, erasure-coding, regenerating code]
---
{% include JB/setup %}

```
1. Convertible Codes: New Class of Codes for Efficient Conversion of Coded Data in Distributed Storage    [2020, 22 refs, ITCS]
   https://www.pdl.cmu.edu/PDL-FTP/BigLearning/LIPIcs-ITCS-2020-66_abs.shtml
    1. Convertible codes essentially work by merging multiple shorter codes into fewer longer codes. The 2020 paper focuses on MDS and "merge regime". Convertible codes have more follow up studies by this author and different authors.
    2. Highlights
        1. Background
            1. "For example, in [32], the authors show that an 11% to 44% reduction in storage space can be achieved by tailoring n and k to changes in observed device failure rates."
            2. "We focus on the access cost of code conversion, that is, the number of symbols that are affected by the conversion"
        2. Key challenges
            1. Convert MDS codeI to MDS codeF, where codeI and codeF have different length. Require to do the conversion with minimal number of nodes accessed.
        3. Key techniques
            1. Restrict to "merge regime", i.e., data symbol count of codeF is a multiple of data symbol count in codeI.
                1. Theorem 15: Conversion low bounds for MDS codes
                2. Theorem 22: Explicit construction of the code to achieve the optimal node access count
                    1. But, the field size is very large, it's exponential to codeF length
                3. Theorem 25: Hankel construction. Compared to Theorem 22, it has small field size, but has restricts codec parameters chosen
                    1. Two extreme points: Hankel-I and Hankel-II.
                        1. Hankel-I for small field size. 
                        2. Hankel-II for high parity symbol count in codecF.
                4. Definition 9: The concept of "stable" - all symbols are relabeling rather than being rewritten
            2. Section 3.1 Lower bounds on the access cost of code conversion
                1. Math to prove Theorem 15
            3. Section 4: Achievability: Explicit access-optimal convertible codes in the merge regime
                1. t-column block-constructible
                2. Math and construction to prove Theorem 22
            4. Section 5: Low field-size convertible codes based on superregular Hankel arrays
                1. Proving Theorem 25
        4. My questions
            1. There are quite a few limitations
                1. Codec must be MDS. LRC not discussed in paper.
                2. Data symbol count of codecF must be integer λ times of codecI. I.e., "merge regime". Non-merge regime not discussed in paper.
                3. Codec construction Hankel-I and Hankel-II both require codecF to be λ times longer, but with fewer parity symbols. It can raise durability issues.

    n. Related materials
        1. Convertible Codes: Efficient Conversion of Coded Data in Distributed Storage    [2019, 10 refs]
           https://arxiv.org/abs/1907.13119
            0. Exactly the same set of authors with the parent paper.
            1. Let's skip and look at the 2022 paper instead.

        2. Convertible Codes: Enabling Efficient Conversion of Coded Data in Distributed Storage    [2022, 10 refs, IEEE Transactions on Information Theory]
           https://par.nsf.gov/servlets/purl/10394403
            0. Same authors "K. V. Rashmi" and "Francisco Maturana".
            1. A better formatted version of the parent paper
            2. Highlights
                1. "Table I" is useful to see all parameter and cost setups
                2. Table III 
                    1. My questions
                        1. Table III shows several non-merge regime cases, but the paper only talked about merge regime cases. How to construct non-merge regime codecs?
                            1. Didn't find in the paper

        2. [32] Cluster storage systems gotta have HeART: improving storage efficiency by exploiting disk-reliability heterogeneity    [2019, 64 refs, FAST19]
           https://www.usenix.org/conference/fast19/presentation/kadekodi
            0. Same author "K. V. Rashmi" with the parent paper, and with Gregory R. Ganger. The parent paper references this paper a lot, as "a more detailed discussion on the practical benefits and constraints of adapting the erasure-code parameters with the variations in failure rates in a storage system".
            1. Save 11~33% disk space on production dataset.
            2. Highlights
                1. Key challenges
                    1. Different groups of disks have different durability level (AFR). By applying adaptive data replication or erasure coding level, we can save capacity, and we can also discover under-redundancy data. 
                2. Key techniques
                    1. Disk group
                        1. Even the same disk, it has different AFR at different age, see bathtub curve
                            1. This is a very interesting capture that potentially can be leveraged to save capacity COGS
                        2. Vendors and models
                        3. Section 2.2 has more detailed group info
                    2. Predicting and modeling disk failure stages
                        1. Using bathtub curve model: Infancy -> useful life -> Wearout
                            1. In compare with Figure 2
                        2. Challenges
                            1. Online and quick
                            2. Be accurate
                            3. filter out outliers
                        3. Online anomaly detection
                            1. Anomaly detector
                                1. Uses the RRCF algorithm [3] exposed by Amazon's data analytics service offering called Kinesis [2].
                                   On a reliability data stream exposed by disk health monitoring system (probably S.M.A.R.T.)
                            2. Online change point detection
                                1. See Figure 7, HeART excludes noise from bulk failure events
                                2. uses a standard window-based change point detection algorithm, which compares the discrepancy between adjacent sliding windows within the AFR curve to determine if a change point has been encountered.
                        4. Efficient redundancy schema transition
                            1. Not mentioned in this paper, but you can see "Convertible Codes".
                3. My questions
                    1. How can HeART accurately predict the current AFR of a disk group? Production disk will be used for ~5 years. To respond timely, HeART probably needs to predict on a per month basis. However, the failures within a 1 month window can be too few to make accurate predictions
                        1. "Figure 10: AFR of the S-4 disk group using a sliding window of 30 days. The determined useful life AFR value by HeART is conservative enough to subsume even the 30-day AFR values which vary more than the cumulative AFRs."
                        2. In particular, we employ the Ruptures library for online change point detection [39, 40].
                        3. We set the sliding window size to one month, because AFRs at a lower granularity than a month are jittery.

        3. StripeMerge: Efficient Wide-Stripe Generation for Large-Scale Erasure-Coded Storage    [2021, 17 refs]
           https://www.cse.cuhk.edu.hk/~pclee/www/pubs/icdcs21.pdf
            0. Quite similar work but not included in the parent paper. Seems not even in the author's newer papers. Focusing on "Global merge conversion" or "Global split conversion"
            1. Logged before

        4. LRCC: Locally Repairable Convertible Codes: Erasure Codes for Efficient Repair and Conversion    [2023, 6 refs]
           https://par.nsf.gov/servlets/purl/10467511Locally%20Repairable%20Convertible%20Codes:%20Erasure%20Codes%20for%20Efficient%20Repair%20and%20Conversion
            0. Same authors "K. V. Rashmi" and "Francisco Maturana". Compared to the parent paper, the authors start to look into LRC codecs.
            1. Sharing techniques, but not explicit construction, no optimal access. Parameters look flexible.
            2. Highlights
                1. global merge conversion (k I=6, gI=1, rI=3, ℓI=1) => (k F=12, gF=2, rF=3, ℓ F=1). Global parity count increased by merge.
                2. Seems the paper doesn't have explicit construction, it's just framework and techniques
                    1. Section B. Conversion techniques
                    2. It's not mentioning whether the conversion is access optimal, nor required field size
                    3. "Case g F ≤ g I : Conversion is carried out using only global parities, as in the MDS case [6]."
                        1. This is reasonable, to reuse local parities. But the problem is how to explicitly calculate the dest global parities.

            n. Related works
                1. The extended version of this paper
                    Locally Repairable Convertible Codes:  Erasure Codes for Efficient Repair and Conversion
                    http://www.cs.cmu.edu/~rvinayak/papers/LRC_conversion_ISIT2023_extension.pdf

        5. On Low Field Size Constructions of Access-Optimal Convertible Codes    [2024, 0 refs]
           https://arxiv.org/pdf/2405.09010
            0. Same authors "K. V. Rashmi" and "Francisco Maturana".
            1. Still focusing on MDS code and merge-regime. The construction is based on Vandermonde matrix. The contribution is more small field size, at the case of src/dest have equal parity symbol count.

            2. Highlights
                1. The thread of proof
                    1. The existence of Vandermonde matrix points to MDS access-optimal convertible codes with equal src/dest parity symbol count
                        1. "Thus, a proof of the existence of any k × r super-regular Vandermonde matrix yields (n I , kI ; n F, kF = λkI ) systematic MDS access-optimal convertible codes for any λ ≥ 2, k F ≤ k, and r I = r F ≤ r."
                        2. "In this paper, we study the setting of systematic MDS access-optimal convertible codes in the merge regime in the case where r I = r F"
                    2. Theorem 1~4, proving the existence of the special Vandermonde constructions.
                        1. Vandermonde matrix Vk(1, θ, σ(θ)) is super-regular
                    3. This paper is first to prove construction of MDS access-optimal convertible codes for merge regime and equal src/dest parity symbol count with practically usable small field size.
                        1. "This paper is also the first to provide, with proof, explicit constructions of systematic MDS access-optimal convertible codes for the merge regime where r F = r I over practically usable field sizes"

            n. Related materials
                1. [15] Locally repairable convertible codes with optimal access costs (X. Kong)
                    1. As referenced in the parent paper
                        1. "In addition to the access cost, previous works on convertible codes have also studied other costs of conversion such as bandwidth cost [8] and locality of repair [14], [15]."

                2. [14] Locally Repairable Convertible Codes: Erasure Codes for Efficient Repair and Conversion
                    1. As referenced in the parent paper
                        1. "In addition to the access cost, previous works on convertible codes have also studied other costs of conversion such as bandwidth cost [8] and locality of repair [14], [15]."

        6. Locally repairable convertible codes with optimal access costs (X. Kong)    [2024, 1 refs]
           https://arxiv.org/pdf/2308.06802
            0. Totally different authors
            1. Converting Optimal LRC codes in merge regime. But the required global parity symbol count is at least "local data symbol count + 1", which is too many (Example III.1).
               Interesting, the first LRC merge regime explicit construction as far as I can find.
            2. Highlights
                1. Definitions
                    1. Merge regime (and each source code is the same) LRC - LRCC (n I , k, r; n F , ζk, r)
                        1. It's a trick here. In the final codec, each local group is equivalent to their source. Then local parity symbols can be directly reused. The remaining problem is how to generate the dest global parity, which then map to the MDS merge regime
                        2. Note, see Definition I.3, the LRCC itself doesn't require merge regime
                    2. "we limit our focus on optimal LRCs" ... "In the following context, the term LRCs will always refer to optimal LRCs"
                2. Section II: CONSTRUCTIONS OF MDS CONVERTIBLE CODES
                    1. Theorem II.2: Constructing MDS merge regime with optimal access code with special parameters: (k + l I , k; ζk + l F , ζk)
                3. Section III. CONSTRUCTIONS OF LOCALLY REPAIRABLE CONVERTIBLE CODES
                    1. LRCCs construction with merge regime with optimal access cost. But requiring n=(k + l)(r + 1), i.e., k local groups with r data symbols each, each local group has 1 local parity symbol, and there are l*(r+1) global symbols.
                    2. Example III.1 (9, 4, 2)-LRC => (15, 8, 2)-LRC. I.e., 2 local groups * 2, 3 global parities, l=1 => 4 local groups * 2, 3 global parities, l=1.
                        1. Problem: Too many global parities. Even l=1, it needs "local data symbol count + 1" global parities.
                    3. Theorem III.1 .. optimal LRCC with write access cost l(r + 1) and read access cost ζlr
                        1. Write access cost is the same with global parity count. So, this is reusing local parities.
                    4. Theorem III.2
                        1. Doesn't require l from src/dest codes are the same.
                    5. My questions
                        1. What is the required field size to construct LRCC?
                            1. "Similarly, a family of (n I , k, r; n F , ζk, r) LRCCs over finite field of size linear in n I is obtained"
                            2. "Unlike MDS codes, for optimal locally repairable codes, it is known that the size of the field can be sub-linear in the code length (e.g., see [24], [25], [27], [28])."

        7. MDS Generalized Convertible Code    [2024, 0 refs]
           https://arxiv.org/pdf/2407.14304
            0. Totally different authors
            1. The key contribution is Extended GRS, see TABLE I. It allows merge N MDS codes into 1 MDS codes. - "MDS generalized merge-convertible codes". The N MDS codes are NOT required to have the same length. The field size is relatively small and related to how many source MDS codes are being merged. 
               The non-extended GRS is also practical, it requires all source codes have the same length, and the dest parity code has less parity symbols than source. The required field size is even smaller.
               But unfortunately this paper only explored the N to 1 merge case w.r.t. constructing an explicit MDS code.
               Good, best construction so far as I can find.
            2. Highlights
                1. Definitions
                    1. merge regime, split regime
                    2. Generalized Convertible Code (Definition 3)
                        1. Convert N codes to M codes. Only requiring their total data symbol count match. Not requiring each code have the same length. Data symbols must NOT after conversion.
                        2. Note, only part of source symbols remain unchanged. See Figure 1.
                    3. MDS generalized convertible code if all the initial and final codes are MDS codes
                    4. Stable Generalized Convertible Code, if it has the maximum number of unchanged symbols overall
                        1. My questions
                            1. Here the "stable" does NOT require all source data symbols keep unchanged. And, I didn't see the definition of convertible codes require preserving decode-ability of the source. So, why it is useful for such a "Stable Generalized Convertible Code" here?
                2. Lower bond on access cost
                    1. Theorem 1, Merge N MDS codes into 1 MDS code, it shows the lower bound of access cost
                        1. Corollary 1. All (t1, 1)q access-optimal MDS generalized merge-convertible codes are stable.
                    2. Theorem 3, explicit guidelines on how to construct access-optimal MDS N to 1 merge convertible codes
                3. Explicit code construction with Theorem 3
                    1. Construction 1
                        1. My questions
                            1. A sub-optimal problem is the MDS construction forces to use Vandermond-type matrix. However, we know only Cauchy Reed-Solomon matrices are optimal
                                1. Optimizing Cauchy Reed-Solomon Codes for Fault-Tolerant Storage Applications
                                   https://web.eecs.utk.edu/~jplank/plank/papers/CS-05-569.pdf
                            2. Is the Hankel construction stable, does it require changing source data symbols?
                                1. Found it. It's fine. 
                                    1. See Lemma 16: all access-optimal linear MDS convertible codes in the merge regime are stable
                                        1. Convertible Codes: Enabling Efficient Conversion of Coded Data in Distributed Storage
                                           https://par.nsf.gov/servlets/purl/10394403
                            3. Also, is the GRS constructions in this paper stable or require changing source data symbols?
                                1. The construction part of this paper didn't mention "stable"
                                    1. OK, found it, it's fine. See Corollary 1.

            n. Related works
                1. [5] Locally repairable convertible codes with optimal access costs (X. Kong)
                    0. As referenced in the parent paper
                        1. "Very recently, Kong [5] introduced a construction of MDS convertible codes with optimal access cost in the merge regime, which may have a linear field size compared with the final code length."
                        2. "Notably, our construction not only covers the known one by Kong [5] but also relaxes any restriction of other parameters compared to [3] and [5]"
                        3. "Maturana and Rashmi [3], Kong [5] respectively proposed some constructions of conventional access-optimal MDS merge-convertible codes corresponding to those in Corollary 2."

        8. Designing storage codes for heterogeneity: theory and practice - Francisco Maturana's Doctoral thesis    [2023]
           http://reports-archive.adm.cs.cmu.edu/anon/anon/home/ftp/usr0/ftp/2023/CMU-CS-23-134.pdf
            1. A summarize of all Francisco Maturana's papers
            2. Highlights
                1. Pudu for Geo-distributed storage system EC codecs.
                    1. See Figure 7.2
                    2. Pudu is not related to convertible codes
                2. Access-optimal convertible codes vs Bandwidth-optimal convertible codes
                3. Bandwidth-optimal convertible codes
                    1. Bandwidth cost of code conversions in distributed storage: fundamental limits and optimal constructions
                    2. Bandwidth cost of code conversions in the split regime

        9. Code Conversions in Storage Systems    [2024]
           https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10388233
            0. By same authors "Francisco Maturana and K. V. Rashmi"
            1. Re-iterating through Francisco Maturana papers. No mentioning LRC, LRC is categorized as open problem.
            2. Highlights
                1. General regime [21], Figure 5. MDS (6,5) => (13,12)
                    1. Still open problem: "For example, non-trivial lower bounds and constructions for minimizing conversion bandwidth in the general regime are still unknown"

        10. Access-optimal Linear MDS Convertible Codes for All Parameters    [2020, 19 refs]
            https://arxiv.org/pdf/2006.03042
            0. Same authors "Francisco Maturana, K. V. Rashmi" etc.
            1. Discussing the access bound of each of MDS merge regime, split regime, general regime. But a key finding is Theorem 1, see below.
            2. Highlights
                1. Theorem 1: In MDS merge regime, if dest code has more parities than src, then access cost is at least dest parity code + ς * src data symbol count
                    1. Good finding. I.e., "it is known [7] that one cannot do better than the default approach for a wide range of parameters (specifically, when (n I − k I ) < (n F − k F ), which we term Regime 1)" as in said paper "Bandwidth cost of code conversions in distributed storage: Fundamental limits and optimal constructions" ... "we show that (1) in Regime 1, where no reduction in access cost as compared to the default approach is possible"
                        1. In practical usage, the dest code parity count is usually "ς * src parity count - s > src parity count". Then from Theorem 1, this research direction is totally invalid, as it cannot reduce access to less than reading each src data and write each dest parity.
                        2. But the bandwidth cost paper said "We show that (1) in Regime 1, where no reduction in access cost as compared to the default approach is possible, a substantial reduction in bandwidth cost"
                            1. See Bandwidth cost of code conversions in distributed storage: Fundamental limits and optimal constructions
                2. Theorem 6: Similar for split regime.
                3. Section IV. GENERAL REGIME
                    1. Setting up access cost bounds

        10. Bandwidth cost of code conversions in distributed storage: Fundamental limits and optimal constructions    [2023, 11 refs]
            https://arxiv.org/pdf/2008.12707
            0. By same authors "Francisco Maturana and K. V. Rashmi". 
            1. MDS code merge regime. Mapping to the case where dest has more parities than src, although access cost cannot be reduced (how many symbols accessed), it can borrow techniques from Regenerating code (vector code) to reduce network bandwidth in conversion. Lower bounds are given and are achievable by the explicit construction in paper.
               Good paper, as it found out to introduce Regenerating code techniques into code conversion area.
            2. Highlights
                1. "We show that (1) in Regime 1, where no reduction in access cost as compared to the default approach is possible, a substantial reduction in bandwidth cost"
                    1. Regime 1 is MDS merge regime where src parity count < dest parity count
                    2. Analyze with Network information flow
                        1. Regenerating codes, paper "Network coding for distributed storage systems"
                        2. "Thus, some of the techniques used in this paper are inspired by the existing regenerating codes literature"
                    3. Using vector code and Piggyback framework to reduce bandwidth cost
                        1. Definition 2 conversion bandwidth γ
                            1. An [n, k, α] vector code, α is vector length
                        2. Theorem 4: conversion bandwidth lower bound if dest code has more parities
                            1. In Section V, the paper shows this bound is achievable. Thus call it "bandwidth-optimal"
                            2. Bound: "ςα min{k I , rF } + r F α", compared to default "ςα * k I + r F α"
                                1. the true network saving is "ςα * (k I - rF)". I.e., src code count * (src data size - dest parity size).
                                2. Divide it by src code count * src data size, you get "1 - dest parity size / src data size" 
                                    = "1 - dest parity size / src parity size * src data rate' "
                                3. See Figure 6, which plots the network saving per different src/dest code parameters
                            2. My questions
                                1. Why reducing the vector length α can even reduce the conversion bandwidth lower bound?
                                    1. It's assuming the chunk size is α, and unit 1 means an element in the vector.
                                2. How large is the vector length α to be required?
                                    1. Not found to be discussed in this paper, probably related to the Piggyback Framework, and can be high.
                                    2. "Therefore, the resulting code will have α = Qs i=1 ri ."
                        3. Section V: Explicit construction
                            1. Figure 4, Example 1, MDS bandwidth-optimal (5, 4; 10, 8) convertible code. And Example 2 to (11,8).

            n. Related materials
                1. Morph: Efficient File-Lifetime Redundancy Management for Cluster File Systems
                    1. In Figure 8. BWO-CC is able to save conversion bandwidth even when r^I < r^F.
                    2. Key contribution
                        1. MDS array code (Regime 2) that saves bandwidth when r^I < r^F, constructed using Piggybacking framework, and achieves bandwidth lower bound.
                        2. Use piggyback framework to construct BWO-CC to achieve bandwidth lower bound.
                        3. When rI < rF, the bandwidth lower bound:
                            1. Without BWO-CC, no array count: merge count * kI + rF
                            2. With BWO-CC, merge count * array count * (rI + kI * (1 - rI / rF)) + array count * rF
                            3. Bandwidth BWO-CC / non-BWO-CC = 1 - (rI/rF - rI/kI) / (1 + rF/kF)
                               So bandwidth saving is (rI/rF - rI/kI) / (1 + rF/kF)


        11. Piggyback Framework: A piggybacking design framework for read-and download-efficient distributed storage codes    [2017, 125 refs, IEEE Transactions on Information Theory]
            https://www.cs.cmu.edu/~nihars/publications/Piggybacking.pdf
            0. By author "K. V. Rashmi" etc. Being used a few times in different papers to construct codes to reduce IO. See Maturana's doctor thesis.
            1. An array Code like Regenerating Code to reduce network transfer, but usually requires fewer sub-packetization per node, and constructed with much easier to understand formulas. A powerful side is the code can be built atop any existing code, typically MDS, and then piggyback with a few formula calculated parities.
            2. Highlights
                1. Figure 1 and Figure 2 show example construction. Example 1 and Example 2 show the repair schedule.
                2. Piggybacking design 2
                    1. Less repair networking, in trade off with more substripes
                3. Piggybacking design 3
                    1. Locality of repair, to reduce number of nodes involved in repair
                4. Comparing with MSR code [5]
                    1. See Table at the tail of section "V. PIGGYBACKING DESIGN 3". Compared to MSR code, Piggyback allows fewer substripes, and applicable to any parity count.
                5. Piggyback Framework has 3 variants, page 14. They are in trade-off of substripe/sub-packetization level vs bandwidth saving. But overall, the sub-packetization level is much lower compared to usual Regenerating code.
            n. My questions
                1. How to piggyback LRC code?
                    1. Piggyback generally require the base code has >= 2 parities. The parity 2~r is piggybacked. But for LRC local group, there is only 1 local parity available.
                    2. Figure 5 shows the repair bandwidth saving. Piggyback 1~3 saving are always < 50%, for a small m, this is inferior then LRC.
                    3. But note, "PIGGYBACKING DESIGN 3" indeed considers repair locality.
                2. How to repair >= 2 node loss with bandwidth saving?
                    1. In piggyback design 1~3, the repair schedule only gives how to repair 1 loss.

        12. Screaming Fast Galois Field Arithmetic Using Intel SIMD Instructions    [2013, 204 refs, J.S. Plank]
            https://web.eecs.utk.edu/~jplank/plank/papers/FAST-2013-GF.pdf
            1. 2.7x to 12x speedup for GF mul with SIMD.
            2. Highlights
                1. See Figure 2 for how to use SIMD to calculate multiplication via left/right tables
                2. Applying to 8-bit GF
                3. Applying to 16-bit GF
                    1. My questions: The process should be able to get simplified because today we have much longer bit SIMD than 128 bit.
                4. My questions
                    1. With "Optimizing Cauchy Reed-Solomon Codes for Fault-Tolerant Storage Applications", high bit width GF is converted into GF(2), so that multiplication is never needed, only XOR is enough. In this way, the optimization in this paper becomes not applicable anymore?

        13. Optimizing Cauchy Reed-Solomon Codes for Fault-Tolerant Storage Applications    [2005, 328 refs, J.S. Plank]
            https://web.eecs.utk.edu/~jplank/plank/papers/CS-05-569.pdf
            1. Too famous. Good paper.

2. An Empirical Study of Rust-for-Linux: The Success, Dissatisfaction, and Compromise
   https://www.usenix.org/conference/atc24/presentation/li-hongyu
    1. The process is "a mixture of success, dissatisfaction, and compromise". Developer has to get safe abstractions merged first before being able to develop the driver. "Unsafe" is unavoidable e.g. in double linked list. Performance penalties happen due to cache misses caused by pointers to share object ownership, and runtime bound checks.
    2. Highlights
        1. RFL - Rust-For-Linux history: See the history in the Section 1 Introduction
            1. The process is "a mixture of success, dissatisfaction, and compromise"
            2. Rust only makes the kernel more "securable" but not fully secure due to unsafe usage is inevitable in driver development
                1. they prohibit complex data structures such as a doubly-linked list, where each node is simultaneously referenced (i.e., owned) by both its predecessor and successor
            3. as a side effect of generic Traits and smart pointers, Rust drivers incur a large number of icache misses and under-performs C drivers significantly in some cases
        2. Goals of RFL
            1. Memory-safe and thread-safe drivers
            2. Zero overhead on abstraction
        3. Insight 3: RFL is bottlenecked by code review but not by code development
            1. there is a deadlock of RFL development: the subsystem communities are unwilling to review the patches about safe abstractions without real Rust drivers as motivating examples; yet without such abstractions, the RFL community is not able to construct the drivers in Rust
        4. Performance penalty from Rust (section "Why Rust drivers may perform poorly?")
            1. runtime array access bound checks
            2. lacking advanced features such as prefetch
            3. more cache misses, due to massively using pointers to share object ownership
            4. Harnessing kernel memory ops with Rust safety rules often involves massive use of smart pointers and generic programming, which incurs large memory footprints and overhead (§ 4.2). In such cases, the developers may opt for unsafe implementation, as long as they have reviewed its safety carefully.
        5. Development overheads of using Rust to write Kernel drivers
            1. bindgen
            2. safe abstraction layer
            3. foreign function interface (FFI)

3. VAST Data: Breaking Resiliency Trade-offs With Locally Decodable Erasure Codes
   https://www.vastdata.com/blog/breaking-resiliency-trade-offs-with-locally-decodable-erasure-codes
    1. Guessing Vast Data EC is using RM LDC. LDC can easily reduce local reconstruct width (to even 2) on a long codec (>100 length), but the node failure recoverability is questionable. Seems it has low chance to lost data with 2 node failures.
    2. Highlights
        1. Text captures
            1. "Can reconstruct unreadable data from only a "local" fraction of the total number of data strips in a protection stripe. For our codes that fraction is 1/Xth of the data strips where X is the number of protection strips in the set."
            2. "We've determined that an example 150+4 encoded stripe has an MTTDL (Mean Time To Data Loss) of over 42 million years with just 2.66% overhead .. while the system can reconstruct the data by reading from just 1/4th of the remaining stripes in an encoded write stripe"
        2. Guessing possible codec schema
            1. The locally decodable erasure coding looks like "Reed-Muller locally decodable codes"
                """
                    def CalcParityCount_RmLdc(nData, readWidth):
                        nCode = math.exp(nData**(1/(readWidth-1)))
                        return math.ceil(nCode)
                """
                1. 150 data, 4 read groups, need 4 parities (read width 38+4)
                   40 data, 4 read groups, need 4 parities (read width 10+4)
                   146 data, 4 reads groups, need 4 parities (read width 38+4)
                2. (r, δ, ε)-locally correctable => (d + 1, δ, (d + 1)δ) in RM LDC
                        r := local read width
                        δ := ratio of tolerable lost symbols
                        ε := probability of cannot decode
                    1. Note "Similarly the exact value of ε < 1/2 is not important since one can easily amplify ε to be close to 0, by running the decoding procedure few times and taking a majority vote"
                    2. "Observe that codes given by proposition 2.4 can only tolerate δ < 1/(2(d + 1))"
                        1. Given data symbol count N, then tolerated failures are δ*N < 1/(2(d + 1)) * N = N/(2*readWidth)
                            1. (150+4)/(2*(38+4)) = 1.83
                               (40+4)/(2*(10+4)) = 1.57
                               (146+4)/(2*(38+4)) = 1.78
                3. "Section 2.3 Summary of parameters" lists RM LDC variables. But given k=150, only the first row N=exp(k^(1/(r-1))) gives a reasonably short N size. The first row maps to the construction at "Proposition 2.4". 
                    1. "Proposition 2.5" gives improved decoding. It can tolerate 1/4 fraction of errors. But it needs σ to be very small, then it requires a large q, which then results in a large N. Sees not feasible neither?
                    2. "Proposition 2.6" similarly require d < σ(q − 1), like Proposition 2.5

    n. Related materials
        1. Locally decodable codes by Sergey Yekhanin    [2012, 248 refs, Microsoft]
           https://www.microsoft.com/en-us/research/publication/locally-decodable-codes/
           https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/LDC_now.pdf 
            1. Good introduction to Locally Decodable Codes
        
        2. VAST DATA whitepaper
           https://www.vastdata.com/whitepaper/#VASTDataLocallyDecodableCodes

        3. VAST DATA blog: Introducing: Rack-Scale Resilience
           https://vastdata.com/blog/introducing-rack-scale-resilience
            1. Key designs
                1. Any VAST server and process data from any disk enclosure
                2. Any server or disk enclosure is connected to more than one switches
                3. Fabric modules provide N+1 redundancy
                4. Power supplies provide N+1 redundancy
                5. LDC code in wide stripe erasure coding


4. Ceph TiDedup: A New Distributed Deduplication Architecture for Ceph    [2023, 1 refs, ATC23]
   https://www.usenix.org/conference/atc23/presentation/oh
    1. Very good paper. Compared to Ceph Dedup 2018, it yields huge improvement on throughput and latency, to the level that dedup has almost no impact compared to no dedup (selective crawling, caching, cold object, IO isolation, dedup offline). Space saving is ~34% (CDC enabled).
    2. Highlights
        1. Key technologies
            1. OID shared reference management
                1. Instead of using ref count, use a list of source OID to track the references to a physical chunk. A false positive reference is possible due to failure, then an offline scrub process and verify the references by tracing back to the source.
                2. A good design pattern is eventual consistency re-execute. By which, a failure in middle of write dedup process can result in an inconsistent state, which is OK to expose. Later rerun will eventually fix it.
                3. Managing snapshot's references
                    1. Naively track the reference from each snapshot can generate excessive add/delete reference messages.
                    2. Instead, the solution is, TiDedup does not generate an add/delete reference message if a chunk is identical to a chunk in the adjacent snapshot.
                        1. Interesting technique.
            2. Selective crawling
                1. The crawler scan all objects to see if an object has enough dedup ratio. If not, the object won't be deduped.
                    1. chunk duplicate count => only a chunk in a object needs dedup => set_chunk
                       intra-object deduplication ratio => entire object should remove redundancy => tier_flush
                    2. The crawler maintains a running "fingerprint=>redundant count" store in memory. 
                        1. If memory usage exceeds threshold, the crawler deletes all entries in store except duplicate fingerprints
                2. Good technique. Selective crawling is probably the key to improve Ceph Dedup performance compared to the 2018 version. Because those objects having no dedup saving doesn't actually do dedup, with a small cost on total storage saving.
                    1. Another key technique to improve performance is caching. Hot objects are tier_promote to the base pool, or skipped dedup.
                    2. The third key technique is, isolate dedup IOs from foreground user IOs.
                    3. The fourth technique, see Section "Object Management"
                        1. Hot object won't be deduped. Cold object is deduped if they meet intra-object deduplication ratio. Otherwise, the cold object is moved to chunk tier without dedup.
            3. Event-driven tiering mechanism with CDC
                1. Standard operations are abstracted: set_chunk, tier_flush, Tier_evict, Tier_promote
                    1. The crawler is a separated application, which calls Ceph provided APIs. The crawler has multiple threads. More crawlers can be deployed if it needs scalability.
                2. Content Defined Chunking is supported.
                    1. A tricky case is writing a chunk can alter the previous range cut. This case is handled.
                    2. The crawler calls the standard operations to perform dedup. They are isolated from user IOs. It can process multiple requests concurrently.
                        1. In the 2018 version, it suffers from a background thread blocks foreground OSD I/Os due to locking
                3. My questions: How fast does crawler need to dedup enough amount of data? The paper focus on final dedup ratio and no impact to user IO. But what if the crawler is too slow to catch up with the ingestion?
        2. Evaluation
            1. Figure 12, YCSB benchmark, compared to 2018 version, huge improvement on performance. Now the throughput and latency has almost no impact to no-dedup mode.
                1. See above notes "technique".
            2. Figure 16 (B), "However, compared to Fixed, TiDedup-worst generates a higher number of messages because TiDedup needs to re duce the references due to the same adjacent snapshots"
        3. Discussion
            1. Additional space overhead for OID reference. "TiDedup forces OSD to stop performing deduplication on the chunk objects in case their number of references is over the threshold value".
                1. My questions: This looks bad.

    n. Related materials
        1. Ceph Dedup: Design of Global Data Deduplication for A Scale-out Distributed Storage System    [2018, 30 refs]
           https://ceph.com/assets/pdfs/ICDCS_2018_mwoh.pdf
            1. Logged before

5. Movie Gen: A Cast of Media Foundation Models    [2024, 0 refs, Facebook]
   https://ai.meta.com/research/movie-gen/
   https://ai.meta.com/research/publications/movie-gen-a-cast-of-media-foundation-models/
    1. Competing with OpenAI Soar, but with good amount of details revealed, based on LLaMa3 and FLow Matching.
    2. Highlights
        1. 30B parameter foundation model
        2. Joint Image and Video Generation
            1. Flow Matching
            2. temporal autoencoder model (TAE)
            3. temporal tiling
            4. Patchified with 3D convolutional layer
        3. Pre-training
            1. See section 3.2, many optimizations
        4. Finetuning
            1. both automated and manual filtering steps
        5. Inference
            1. Prompt rewrite: LLaMa3 teacher-student distillation, HITL finetuning
        6. Video personalization
        7. Instruction-Guided Precise Video Editing
        8. Joint Sound Effect and Music Generation
        8. Evaluation
            1. Evaluation Axes
            2. Table 6 MovieGenVideo vs. prior work
                1. MovieGen outperformed OpenAI Sora with significance
    n. Related works
        1. OpenAI Sora: https://openai.com/index/sora/
        2. moviegen 92页技术报告解读 + 细节全整理，如何复现sora？ - Ethereal
           https://zhuanlan.zhihu.com/p/835288682
            1. Good summary of key points in the paper
        3. 作为最优传输的连续正则化流，MovieGen时空压缩与流匹配推动AI视频时间关联更进一步 - 御坂美冰
           https://zhuanlan.zhihu.com/p/840275407
        4. Hacker News: Meta Movie Gen 元电影一代
           https://news.ycombinator.com/item?id=41740965
        5. Meta Movie Gen Guide: How It Works, Examples, Comparison
           https://www.datacamp.com/blog/movie-gen-meta
        6. Meta Movie Gen (model not released)
           https://www.reddit.com/r/StableDiffusion/comments/1fvyvy8/meta_movie_gen_model_not_released/

6. Morph: Efficient File-Lifetime Redundancy Management for Cluster File Systems    [2024, 0 refs, SOSP]
   https://www.pdl.cmu.edu/ftp/Storage/Morph_Final_abs.shtml
    1. Very good paper. Pointing the new industry direction for EC in cloud storage. A combination of techniques: EC+1 Inline EC, Convertible Codes, Wide Stripe EC. IO amplification is reduced throughput the data lifecycle.
    2. Highlights
        1. The authors are renowned
            1. Francisco Maturana - author of Convertible codes
                1. Designing storage codes for heterogeneity: theory and practice - Francisco Maturana's Doctoral thesis
                   http://reports-archive.adm.cs.cmu.edu/anon/anon/home/ftp/usr0/ftp/2023/CMU-CS-23-134.pdf
                2. These guys are ridiculously productive ...
            2. Saurabh Kadekodi - author of Google LRC
                1. Google LRC: Practical Design Considerations for Wide Locally Recoverable Codes (LRCs)
                   https://www.usenix.org/conference/fast23/presentation/kadekodi
            3. K. V. Rashmi - co-authored many Convertible codes papers with Francisco Maturana
                1. K. V. Rashmi is also the author of "Piggback Framework"
            4. Gregory R. Ganger - tutor of Francisco Maturana. Also, the interesting Declarative IO
                1. Declarative IO: Cluster Storage Systems Need Declarative I/O Interfaces
                   https://youtube.com/watch?v=TGWKZnJeNmA&si=AC6gaUtfnPjIt_vB
        
        2. Key takeaways
            1. Inline EC can have write latency impact. Instead, use an EC+1 with a shorter Inline EC format.
                1. EC+1 Inline EC is a middle group of traditional Inline EC and 3-replica.
                2. Section 4.2 Hybrid Writes has more optimization. It's using PMEM write buffer, even Inline EC would ack after 3-writes done. Section "Appendability Guarantee" - Parity Logging technique. True parity computation and disk writes are delayed.
            
            2. Use Convertible Code (CC) w. BWO-CC to reduce the bandwidth cost to convert shorter codecs into longer codecs when data gets cold
                1. BWO-CC uses regeneration code techniques to save conversion bandwidth when dest parity count > each src parity count 
                2. Figure 15, using CC also reduces the compute cost.
            
            3. Three levels of temperature, just write (hot) -> cold (medium codec length) -> frigid (wide stripe EC)
            
            4. Figure 5, Per-HDD capacity increases over the years at a faster rate than per HDD bandwidth: ≈11.8%/year vs. ≈5.1%/year. 
                1. Consequently, the available bandwidth-per-TB has been decreasing at an alarming ≈8.5%/year rate.
                2. the onset of new disk technologies like HAMR is expected to exacerbate the problem
            
            5. Figure 14e, by prioritizing striped reads, EC data yields better read throughput than 3-replica. Although Inline EC typically writes slower.
            
            6. Placement taking future merge into consideration. Data to merge placed to different nodes. Parity to merge placed at the same node.
            
            7. The specific part of the new parity chunk to pre-compute is strategically chosen such that the portion of data blocks to read during transcode is physically contiguous on disk, significantly improving IO efficiency. This approach is based on the "hop-and-couple" optimization for reconstruction-efficient vector codes introduced in [45].

            8. Use piggyback framework to reduce the repair cost of MDS code. But may be Regenerating Clay Code is even better.
        
        m. My questions
            1. Though CC can save bandwidth, it's not directly applied to Google's LRC. Instead, the author brings its own new sets of codecs narrow CC, med CC. Is it implying that CC has problem to apply to LRC?
                1. No no. The paper did gave LRCC. This should be a solution for LRC + CC. But the LRCC paper didn't give enough details, especially how to preserves maximum recoverability (MR) after conversion?
                2. "We implement both CC[37,39] and LRCC[42]."
            2. Figure 3. Inline EC RS(6,9) write latency Q50 is 4x of 3-replica? This looks too bad, how is the test data obtained? Hope it's not by a custom HDFS implementation.
            3. From Figure 1, Looks like Google Cloud is already running Wide Stripe LRC on production?
            4. Figure 6, it has problem, a node memory can hardly hold the entire replica if it's a real cloud storage. Instead, a typically way is to use PMEM (or battery/storage backed DRAM) to buffer writes, and use parity logging to write parities.
            5. Figure 12 D, 95% reduction in IO. How is it achieved? 
                1. This saving is remarkably high, looking for more details 
            6. How to CC convert MDS to LRC? As in Figure 2. Section 5.1 mentioned some, e.g. CC(6,9) to LRCC(24,4,2). This is an interesting direction to explore. Together with LRCC conversions.
                1. The typical solution mentioned in this paper is to, treat LRC as two separate groups of MDS codes, and apply MDS CC.
            7. What about split? A small amount of cold data can be come hot again.
                1. BWO for split regime: Bandwidth Cost of Code Conversions in the Split Regime
            8. How Morph overcomes the problem that merging CC would forcefully change EC stripe size?
                1. File is cut into chunks. EC works on chunks. An EC group of chunks forms a stripe.

    n. related works
        1. [41] BWO-CC: Bandwidth Cost of Code Conversions in Distributed Storage: Fundamental Limits and Optimal Constructions
           https://arxiv.org/pdf/2008.12707
            1. Figure 8 the magic to save bandwidth.

        2. StripeMerge: StripeMerge: Efficient Wide-Stripe Generation for Large-Scale Erasure-Coded Storage
           https://www.cse.cuhk.edu.hk/~pclee/www/pubs/icdcs21.pdf
            1. A compare work that reduces bandwidth when merging short codes into long.

        3. Google LRC: Practical Design Considerations for Wide Locally Recoverable Codes (LRCs)
           https://www.usenix.org/conference/fast23/presentation/kadekodi

        4. [42] LRCC: Locally repairable convertible codes: Erasure codes for efficient repair and conversion
           https://par.nsf.gov/servlets/purl/10467511Locally%20Repairable%20Convertible%20Codes:%20Erasure%20Codes%20for%20Efficient%20Repair%20and%20Conversion
        
        5. [32] ER-Store: ER-Store: A Hybrid Storage Mechanism with Erasure Coding and Replication in Distributed Database Systems
           https://onlinelibrary.wiley.com/doi/pdf/10.1155/2021/9910942
            // TODO

        6. [45] A hitchhiker’s guide to fast and efficient data reconstruction in erasure-coded data centers - 2014
            // TODO

        7. [39] Bandwidth Cost of Code Conversions in the Split Regime - 2022
           https://www.pdl.cmu.edu/PDL-FTP/Storage/ISIT22-Bandwidth.pdf


7. Codes With Local Regeneration and Erasure Correction    [2014, 201 refs]
   https://ieeexplore.ieee.org/document/6846301
    1. Combining LRC codec with Regenerating code. Apply regenerating property to the local group of LRC. The local code has minimum distance >2 (>2 local parities)
        1. See my questions .. "So .." for summary of this paper
    2. Extend LRC to allow more than one parities per local group. Derived the bounds of minimum distance, see Theorem 2.1
    3. Table II summary of constructions of locally regenerating codes appearing in the paper. Supports either MSR and MBR. Reaching maximum bound of minimum distance.
        1. δ means local minimum distance. 
        2. The constructed LRC code requires to be symmetric at each local group, and local code length divides the global code length. (parity-splitting, uniform (r, δ))
    4. My questions
        1. By Theorem 2.1, suppose 2 local groups and each ground has 2 parities. The distance of the new code can be d_min <= (k + k/r*(δ-1) + g) - k + 1 - (k/r - 1)(δ - 1) = g + (δ-1). This is just the common LRC's minimum distance if it has >=2 local parities per local group
        2. So, this paper is constructing LRC that supports local regenerating. It needs >= local parities per local group. The generated LRC code reaches the recoverability of a plain LRC. The underling code is a vector code. The code is named URC code. The paper didn't mention applying regenerating code global reconstruction.
            1. Use Pyramid-like Constr. 5.3
            2. Search "We next define the function" at section IV for what is P^(inv).
            3. It sounds like P^(inv)(K) needs to be pretty big, in the "Pyramid-Like MSR-Local Codes", Constr. 5.3
                1. Not sure the what vector size "α" needs to be, probably same with the MSR code used in local group
            4. So far, the "Pyramid-like Constr. 5.3" look like a good usage, few limitation. So the LRC local regeneration problem can be thought as solved.

    n. Related materials
        1. Partial MDS Codes with Regeneration (PMDS)
           https://arxiv.org/pdf/2009.07643.pdf
            1. Logged before. Global reconstruction with regenerating code is still the open problem.

        2. Codes with local regeneration    [2013, 187 refs]
           https://ieeexplore.ieee.org/document/6502947
            1. Same author "Govinda M. Kamath" with "Codes With Local Regeneration and Erasure Correction"
```
