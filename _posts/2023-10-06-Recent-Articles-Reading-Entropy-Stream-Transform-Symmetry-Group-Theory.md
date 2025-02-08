---
layout: post
title: "Recent Articles Reading: Entropy, Stream, Transform, Symmetry, Group Theory"
tagline : "Recent Articles Reading: Entropy, Stream, Transform, Symmetry, Group Theory"
description: "Recent Articles Reading: Entropy, Stream, Transform, Symmetry, Group Theory"
category: "Paper Reading"
tags: [storage, paper, database]
---
{% include JB/setup %}

The Entropy part.

```
1. 如何评价DuckDB?
   https://www.zhihu.com/question/438725169/answer/3143660836
    1. "初衷是提供一个AP版的SQLite，即： 一个面向数据分析场景的嵌入式数据库"
    n. related materials
        1. 万字解读 | A轮就融资￥3亿+的MotherDuck到底是个啥？
           https://www.rachellaw.xyz/2023/MotherDuck
            1. "MotherDuck的创始人Jordan是DuckDB的早期用户。 Jordan此前是Google BigQuery的创始工程师和产品经理"
        2. MotherDuck: BIG DATA IS DEAD
           https://motherduck.com/blog/big-data-is-dead/
            1. "I worked at SingleStore in 2020-2022"
            2. "DATA IS A LIABILITY" .. "regulations like GDPR and CCPA"
        3. MotherDuck: WHY DOES EVERYBODY HATE DATABASES?
           https://motherduck.com/blog/why-everybody-hates-databases/
        4. 数据库独角兽SingleStore：没有HTAP，机器学习和人工智能都是不切实际的
           https://zhuanlan.zhihu.com/p/583545188
            1. LoopJump: SingleStore - 云原生HTAP
               http://loopjump.com/singlestore-cloud-native-htap/
                1. vs SnowFlake

2. 桥水基金CEO瑞·达里奥的《原则Principles》读后感 - 图帕先生
   https://www.zhihu.com/tardis/zm/art/104876040

3. 南昌之星售票系统: Distributed Transaction in DynamoDB
   https://zhuanlan.zhihu.com/p/647873878
    1. "不用 MVCC，事务本地直接更新。作者觉得多版本开放在存储上太复杂了（感觉甚至包括用 write intent 这种形式），所以做了一个单版本的事务（我本人对这个不置可否，因为感觉它们没有 scan 负载，所以可以尽量做简单）"

4. TSA方法：基于线程时间分布分析性能瓶颈 -  Ash1n2
   https://zhuanlan.zhihu.com/p/649743048

5. [CIDR 2020] Umbra: A Disk-Based System with In-Memory Performance - 张建
   https://zhuanlan.zhihu.com/p/620731326
    1. "LeanStore 的 Buffer Manager 管理定长 page ... Umbra 的 Buffer Manager 管理变长 page，如图所示，page 按 size class 分类，每个 size class 的 page 大小是前一个的 2 倍。最小 64 KB"
    2. "Umbra 的关键实现包括：不定长 page 和专用 buffer manager，pointer swizzling 和 versioned latch 等多核优化，高效的 log 和 recover 算法，代码生成等。Umbra 是 LeanStore（基于 SSD 的定长 page 数据库）的演进"
    3. "物理内存释放：Umbra 用 pwrite 写 buffer frame 到磁盘文件，用 madvise 传 MADV_DONTNEED 标志，让操作系统回收物理内存。因为 mmap 没映射磁盘文件，madvise 开销很小。 
        Buffer Manager 跟踪物理内存使用情况，保证 buffer pool 不超配置容量。Umbra 和 LeanStore 的缓存替换策略相同，内存 page 先进 cooling stage 的 FIFO 队列头，到队列尾再驱逐。"
    4. "Umbra 用一个 64 位整数的原子变量实现了 versioned latch，支持 exclusive、shared 和 optimistic 三种上锁模式 ... Umbra 和 LeanStore 的区别在于，Umbra 支持 shared 模式上锁，而 LeanStore 只支持 optimistic 模式 ... 另外 Umbra 的 versioned latch 在后面演进成了 Hybrid-Latch"
    5. "Umbra 中支持的统计信息主要是每个表上的随机采样和每个列上可更新的 HyperLogLog。Umbra 实现了一个可扩展的在线蓄水池采样算法"
    6. "在生成的代码中，每个 step 对应一个单独的函数，可以由 Umbra 的 runtime system 调用。在查询执行时，通过这些 step 完成 pipeline 内的状态转换，step 的执行由 Umbra 的查询执行器协调。多线程 step 采用 morsel-driven 的方式执行。
        另一个和 HyPer 不同的地方是代码不是直接生成成 LLVM IR，而是在 Umbra 中实现了一个自定义的轻量级 IR，这使 Umbra 能在不依赖 LLVM 的情况下高效（省去一些额外开销，能够比 LLVM 更高效）地生成代码。
        Umbra 不会立即将 IR 编译为优化后的机器码。Umbra 采用了自适应编译策略，用来权衡每个 step 的编译和执行时间。step 的 IR 先被转换为高效的字节码，由 Umbra runtime system 解释执行。对于并行 step，自适应执行引擎会跟踪执行进展以决定编译是否有益，如果是，则将 Umbra IR 转换为 LLVM IR，然后交给 LLVM JIT 编译后执行。"
    n. related materials
        1. Morsel-Driven Parallelism: A NUMA-Aware Query Evaluation Framework for the Many-Core Age
           https://nan01ab.github.io/2018/05/Morsel-Driven-Parallelism.html

6. 亚马逊AWS有什么用呢？ - 李庆超
   https://www.zhihu.com/question/22314873/answer/2333079486

7. CEPH 4K小文件读写性能非常差? - 哈哈咩
   https://www.zhihu.com/question/268347739/answer/3166121803
    1. Ceph setup
        1. 存储协议走的nvmf
        2. 网络前后端分离，走RDMA，每台服务器使用双网口100GB IB * 2
        3. 存储后端使用的bluestore，spdk uio驱动，每个节点6块 Dell DC NVMe PE8010 RI U.2 3.84TB的硬盘
    n. related materials
        1. Ceph Days NYC 2023: NVMe-over-Fabrics support for Ceph
           https://www.youtube.com/watch?v=CWw689gcD7A
            1. Github: Ceph NVMe over Fabrics (NVMe-oF) Gateway
               https://github.com/ceph/ceph-nvmeof
                1. Essentially, it allows to export existing RBD images as NVMe-oF namespaces
            2. Related
                1. DPU with NVMe-oF offloading
        2. Accelerate Ceph via SPDK - XSKY’s BlueStore as a case study
           http://mysrc.cn-bj.ufileos.com/cephdaybeijing201608/04-SPDK%E5%8A%A0%E9%80%9FCeph-XSKY%20Bluestore%E6%A1%88%E4%BE%8B%E5%88%86%E4%BA%AB-%E6%89%AC%E5%AD%90%E5%A4%9C-%E7%8E%8B%E8%B1%AA%E8%BF%88.pdf
        3. SPDK - NVMf - NVMe over Fabrics Target
           https://spdk.io/doc/nvmf.html
        4. NVMe-oF with vSphere and Pure Storage: The Details - Pure Storage Cloud Solutions
           https://www.youtube.com/watch?v=Fvoat6PyEpg
            1. Key points of NVMe vs SATA
                1. NVMe exploits parallelism of SSD. While SATA is mostly serial
                2. NVMe shortens the processing path, make IO faster and need less CPU
            2. NVMe-oF vs SCSI
                1. SCSI queues have limits, 256 outstanding IO, need to tuning at many levels otherwise target for slow drives
                2. NVMe queue limits 64000+, parallelism. NVMe was designed for flash. 
            3. NVMe-oF components
                1. NVMe Adapter - the HBA
                2. Controller - the target manager, what the host connects to to see new storage
                3. NQN - NVMe Qualified Name, the address of a NVMe-oF initiator or target
                3. Namespace - an NVMe storage device attached to the host
        5. What are nvme namespaces? How do they work?
           https://unix.stackexchange.com/questions/520231/what-are-nvme-namespaces-how-do-they-work
            1. "thus a namespace can’t group multiple controllers (multiple controllers can provide access to a shared namespace)"
            2. "It’s better to think of namespaces as something akin to SCSI LUNs as used in enterprise storage (SANs etc.)."
            2. NVMe Namespace standard: https://nvmexpress.org/resource/nvme-namespaces/
        6. Keynote: Ceph: The Future of the Storage TODAY
           https://www.youtube.com/watch?v=FBCz0yXqdc8
            1. Ceph, IBM, opensource. OpenShift and Ceph.
            2. Ceph vision: be the Linux of storage. Ecosystem.
            3. NVMe fabric.
        7. Ceph Days NYC 2023: An Introduction to MicroCeph
           https://www.youtube.com/watch?v=H3msVyN5ac8&list=PLrBUGiINAakNlN2myemQaO5nSxKfbNFos&index=14
            1. Snap, Dqlite
        8. 分布式块存储性能调优之PGO - 哈哈咩
           https://zhuanlan.zhihu.com/p/644449363
            1. PGO - performance guided optimization
                1. Tune your program’s speed with profile guided optimizations
                   https://johnnysswlab.com/tune-your-programs-speed-with-profile-guided-optimizations/
                2. interesting
                3. Profile-Guided Optimization (PGO)
                   https://www.intel.com/content/www/us/en/docs/cpp-compiler/developer-guide-reference/2021-8/profile-guided-optimization-pgo.html

10. Rust and C++ Interoperability - TOBIAS HUNGER
   https://slint.dev/blog/rust-and-cpp
   https://github.com/hunger/reveal.js/blob/eurorust_2022_cxx_and_rust/Rust%20and%20C%2B%2B.pdf
    1. No C++ compatibility built into Rust. Challenges 
        1. Rust has no defined ABI, neither has C++ (compiler defined!).
        2. Language has different concepts like inheritance, lifetime, templates
        3. Data types do not match up. Even if they contain the "same" data, field names/sequence/types will be different
        5. utf-8 encoded strings in rust vs bytes in unknown encoding in C++
        6. Macros
    2. Existing approaches
        1. Binding Generation
            1. bindgen
            2. cbindgen
    3. Slint: No binding generation

11. 个人的选择与历史的进程 - 李博杰
    https://zhuanlan.zhihu.com/p/647970514
    1. very good
    2. 如何折纸将长方形纸的一条边三等份？五等份？
        1. 对折对角线，对折顶点到另一边中点线，交点即三分之一
            1. y=b/a*x, y=b-2b/a*x => x=a/3
            2. 同理，y=b-nb/a*x 即可得到 x=a/(n+1)，即得到任意奇数等分边的方法
            3. 群论推广
                1. 除了等分边以外，轻易还可以得到倍份边，称这种数为B数。B数满足1/n或者n的形式
                   因为折纸，B数还可以做到m/n和l+m/n的形式。
                2. 如果的到一条边的B数，同理也可以得到另一条边的B数，因此我们不区分是哪条边的
                3. 定义B数运算为与上面相仿的两条对角线的交点
                    y=B1*b/a*x, y=b-B2*b/a*x => x=a/(B1+B2)
                   因而，这种折纸方法实现的是B数上的加法运算，值域覆盖所有正有理数
                4. 即，理论上可以做出3/5等分一条边这种事情
                    y=b-2b/a*x, y=b/(2a)*x

    3. 用一个每次抛出正面朝上概率为 p 的硬币，允许多次抛出，实现一个等概率的 01 随机变量，要求尽可能减少抛出次数的期望. Toss Coin problem.
        1. General principles
            1. Every coin toss should be leveraged. If it cannot output in this round, continue to use it in the next round
            2. Key takeaways
                1. The "Running sequence layer deduction model" (Approach 2) sometime is much more simpler and useful than the "even tree model" (Approach 1)
                    1. RSLD to handle the infinite sequence generation problem.
                        1. I'm familiar with Tree Model for problem solving.
                           But here, let's call the new model STREAM MODEL - multi-layered stream model with reduce, 1:N stream model.
                    2. RSLD can leverage non-consecutive pieces of sequences. Tree model can hardly do it.
                    3. The LSM-tree compaction or GC right fits the RSLD model
                    4. In Approach 3, the layer model is extended to 1->2, each layer can map to 2 next layers
                2. Approach 1 finds consecutive sequences with equal numbers of H/T
                   Approach 2 additionally leverages non-consecutive sequences
                   Approach 3 additionally leverages overlapping sequences
                4. Verify whether an approach is optimal enough, by deriving A(p) average bit generate rate, and check whether A(1/2) == 1
                    1. Next, first derive the general requirement of A(p), and then prove that H(p) satisfies A(p)
                       So, in this way, we proved that Approach 3 Advanced Mult-Level Strategy reaches the optimal, and it's H(p)
                        H(p) = -plog2(p) - qlog2(q), and H(1/2) == 1.0
                    2. H(1.0/3) ~= 0.92, where 1/H(p) even < 2. This is because with Layer A,B, it can generate more than 1 bits per each coin toss
                5. A very good demo of how entropy works
                    1. the expected coin toss of a biased p coin, to compose into the random variable 0,1 of 0.5 probability, Entropy(0.5) / Entropy(p)
                        1. Even we don't know the optimal method, we can leverage Entropy function to "guess" to optimal bound, and to verify if an algorithm reached the optimal bound
                6. Biased coin toss is a fundamental model for many stochastic process. The zero-entropy lossing process is generally useful
                    1. A finite state Markov chain can be converted to several sequences of biased coin flips without losing entropy
                    2. A random variable with N possible values (e.g. a 6-face die), can be modeled with a single N-face coin toss
                        1. This is powerful

        2. Approach 1: Model coin toss as the probability event tree. Each toss maps to a tree layer. Any time we find two tree paths can be paired, we can assign them to A/B (i.e. output the 0/1 as in Approach 2)
            1. Source and example output data: https://gist.github.com/accelazh/b657e6c8ce8b70a9977e3dea06d54f71
            2. Which kind of two tree paths can we say they have equal probability?
                1. Two paths have equal length
                2. Two paths each has the same number of Hs
                    1. Two paths, within each, exactly 1/2 nodes are H
                        1. It can be proven that 2.1 can replace 2 entirely.
                3. Forget previous coin tosses, if the reminder paths are having equal probablity
                    1. Beware of how many coin tosses to forget.
            3. From the output, we can find captured paths are:
                1. New known patterns (2): 01 - A, 10 - B
                   New known patterns (4): 0011 - A, 1100 - B
                   New known patterns (8): 00001111 - A, 11110000 - B
                   New known patterns (16): 0000000011111111 - A, 1111111100000000 - B
                    1. This can be proven that only 2^n 0 + 2^n 1 patterns are possible
                2. Approach 1 captures the "known pattern" (tree path) in the beginning, middle, or end of a total tree path

        3. Approach 1.5: Resamping. Since a coin toss p != 1-p. We only needs to append a second layer of probability variable a, that p*(1-a) == (1-p)*a. Thus we will get equal output probability
            1. We can derive a == p. So, the second layer of resampling is equivalent to toss coin more times, so that the number of H and T are equal. Then, the method is equivalent to Approach 

        4. Approach 2: Model coin toss as a H,T sequence generator. We need to represent H/T into 0/1, so that the generation rate of 0,1 is a max
            1. Source: Tossing a Biased Coin and Binary Entropy Function
               https://www.eecs.harvard.edu/~michaelm/coinflipext.pdf
            2. Figure 1: the "Multi Layer Strategy", notes
                1. There are more than 3 layers. Note the output takes a unit of 2 symbols at each layer.
                2. Each N+1 layer consumes two coin tosses from the N layer. Layer 1 is the original coin toss sequence. 
                3. Each layer can output 0/1 by merging H/T. The layer can only merge with its self layer. This ensures 1 and 0 probability are equal
                4. As you can see, every coin toss is leveraged. The 0/1 output rate seems already at max.
            3. Proving that Approach 2 generates LESS tosses than Approach 1. Approach 2 is BETTER.
                1. From "New known patterns" in Approach 1, you can find what Approach 1 captures is exactly the same with what Approach captures per layer
                    1. Note there is position requirement. A "00001111" sequence must start from an even position.
                2. When does Approach 1 stops tossing coin? - the first A/B can be assigned
                   When does Appraoch 2 stops tossing coin? - the first 0/1 can be output
                   The proof is equivalent to - will both of Approach 1 and Approach 2 terminate tossing coin as exactly the same time?
                    1. Take HHHHTT as an example, Approach 2 can output 1 at Layer 2. But Approach 1 cannot generate anything.
                       The advantage of Approach 2 is it can leverage non-consecutive sequences, i.e. the HH and TT at start and end. But Approach 1 CANNOT
            4. At layer n (n starts from 0):
                Probability of meeting H: PH(n) = p^(2^n). Similarly, PT(n) = (1-p)^(2^n)
                Data ingestion speed: D(n) = D(n-1) - O(n-1)
                Output speed: O(n) = D(n) * 2 * PH(n) * PT(n) / (PH(n) * PH(n) + 2 * PH(n) * PT(n) + PT(n) * PT(n))
            5. How to calculate the expected time of coin tosses to generate 
                1. See the source paper. The solution method is very good.
                2. Step 1 - Obtain the probability of NOT outputing 0/1 at 2^k steps
                   Step 2 - Obtain the probability of NOT outputing 0/1 at l steps Q(l). l is a sum of 2^j
                   Step 3 - Obtain the probability of outputing 0/1 at exactly l step. By Q(l-2) - Q(l)
                   Step 4 - Sum the expectation. Sum((Q(l-2) - Q(l))*l), l>=2 and l is even.
                            This is can reduced into 2*Sum(Q(l)), l>=0 and l is even. t2 = 2 + Sum(Q(l)), l>=2 and l is even
                   Step 5 - Since l = Sum(2^ki), then Q(l) = Mul(Q(2^ki))
                       1. My questions: How does Page 6 the sum of Q(l) formula be reduced to p, q, k? No details in this paper
            
        5. Approach 3: A yet more efficient Advanced Mult-Level Strategy - Figure 7 - reached Entropy H(p) boundary
            1. Approach 1 finds consecutive sequences with equal numbers of H/T
               Approach 2 additionally leverages non-consecutive sequences
               Approach 3 additionally leverages overlapping sequences
            2. "The Multi-Level strategy does not take advantage of when each level provides us with a bit. For example, in the Multi-Level strategy, the sequences H H H T and H T H H produce the same single bit. However, since these two sequences occur with the same probability, we can pair up these two sequences to provide us with a second bit"
            3. Page 9, analysis to derive A(p) the average bits produced for each biased flip
                1. Level 0 + Level A + Level 1. But it's recursrive A(p) = A(Level 0) + A(Level A) + A(Level 1)
                   The math formula nicely walked around the multi-tail recursion complexity
                    1. The formula can derive A(1/2) = 1
                    2. good. By try calculating A(1/2), we can verify Approach 1 and Approach 2 that whether they are optimal enough 
            4. Approach 3 is the best? Paper "Iterating von Neumann’s Procedure" by Yuval Peres points out:
                1. The best average bit generation rate is the entropy function H(p) = -plog2(p) - qlog2(q), and H(1/2) == 1.0
                2. good. This paper's A(p) can be satisfied by H(p). See page 11
                    1. Since H(p) is the best already, we then proved that A(p) is H(p), and the Advanced Mult-Level Strategy achieves the optimal H(p)
            5. Paper "Iterating von Neumann’s Procedure" by Yuval Peres    [1992, 244 refs]
                1. This is what this paper does. The formula A(p) is right shown in Y.Peres's paper as r_v(p) in proposition 2. So the method is called "Iterating von Neumann"
                2. In more details, the method would require to work without knowing p, because the several A(p), A(p^2+p^2), are working on different biased coins.
                   It also assumes the coin toss sequence input into each layer are independent.
                3. To mathmatically prove A(p) = H(p), the paper leveraged that A(p) is monotonically increasing (by iterating A_(n+1)(p) = A_n(p) .. + A_n(p^2 + q^2) .. formula), and leveraged that H(p) is a fixed point of A(p)
                   Note, by iterating more times, i.e. constructing more layers, A(p) will eventually approach H(p). but before reaching the infinity limit, A(p) < H(p).  
                4. Interesting: "As in [2], the output of a finite state Markov chain can be converted to several sequences of biased coin flips without losing entropy, and then one may apply the extraction procedures discussed above"
            6. How the layers are constructed:
                    Full combinations: HH, HT, TH, TT. Layers capture by pair.
                    Layer N captures: HT, TH
                    Layer N+1 captures: HH=>H, TT=>T
                    Layer NA captures: Toss1 XOR Toss2
                1. My questions
                    1. It seems, AND + XOR composes certain kind of "Entropy completeness"?

        6. Generalization: Toss several biased coins in a row each with different bias probability
            1. Take 2 biased coins as an example
                1. Coin 1, Coin 2 probability are p1, p2
                2. The basic unit is 2-tosses: H1H2, H1T2, T1H2, T1T2
                3. The basic unit for reduction is a pair of 2-tosses:
                    Ideally, one toss generates 1 bit. But for biased coin
                        1. Layer 0 aims to generate 1 bit per 2 tosses
                        2. Layer 1 takes the reminder of Layer 0, and fold it by half
                        3. Layer 2 takes the XOR from Layer 0, and fold it by half 
                    Group 1 each coin is an HT/TH - generate 2 bits at Layer 0
                        H1H2, T1T2 -> 00
                        H1T2, T1H2 -> 01
                        T1H2, H1T2 -> 10
                        T1T2, H1H2 -> 11
                    Group 2 - only one coin is an HT/TH - generate 1 bit at Layer 0
                        Group 2.1
                            H1H2, H1T2 -> 0
                            H1T2, H1H2 -> 1

                        Group 2.2
                            H1H2, T1H2 -> 0
                            T1H2, H1H2 -> 1

                        Group 2.3
                            H1T2, T1T2 -> 0
                            T1T2, H1T2 -> 1

                        Group 2.4
                            T1H2, T1T2 -> 0
                            T1T2, T1H2 -> 1
                    Group 3 - no coin is HT/TH - fold and goto Layer 1
                        H1H2, H1H2 -> H1H2
                        H1T2, H1T2 -> H1T2
                        T1H2, T1H2 -> T1H2
                        T1T2, T1T2 -> T1T2
                    Duplicate Group - Layer A - Coin 1 XOR Coin 1, Coin 2 XOR Coin 2
                        H1H2, T1T2 -> H1 XOR T1, H2 XOR T2 = T1T2
                        H1T2, T1H2 -> 
                        T1H2, H1T2 -> 
                        T1T2, H1H2 -> 

                        H1H2, H1T2 -> H1 XOR H1, H2 XOR T2 = H1T2
                        H1T2, H1H2 -> 
                        H1H2, T1H2 -> 
                        T1H2, H1H2 -> 
                        H1T2, T1T2 -> 
                        T1T2, H1T2 -> 
                        T1H2, T1T2 -> 
                        T1T2, T1H2 -> 

                        H1H2, H1H2 -> H1 XOR H1, H2 XOR H2 = H1H2
                        H1T2, H1T2 -> 
                        T1H2, T1H2 -> 
                        T1T2, T1T2 -> 

            2. I didn't verify, but the optimal generator should reach the H(p1,p2) too, a random variable with 4 values.

        7. Generalization: Toss an N face coin - modeling a random variable with N different values
            1. Take a random variable with 3 values as an example. It generates 01 bit stream
                1. The basic unit is 1-toss: results represented by H T M
                2. The basic unit for reduction is a pair of 2-tosses
                    Group 1 - generate 1 bit per 2 tosses at Layer 0
                        HT -> 0
                        TH -> 1

                        HM -> 0
                        MH -> 1

                        MT -> 0
                        TM -> 1
                    Group 2 - fold and goto Layer 1
                        HH -> H
                        TT -> T
                        MM -> M
                    Group 3 - fold and goto Layer A - expand XOR to be the "distance" between two symbols 
                        HT -> T
                        TH -> T

                        HM -> M
                        MH -> M

                        MT -> T
                        TM -> T

                        HH -> H
                        TT -> H
                        MM -> H
            2. I didn't verify, but the optimal generator should reach the H(x) too, a random variable x with N values.

12. DPDK内存碎片优化，性能最高提升30+倍 - 字节跳动SYS Tech
    https://zhuanlan.zhihu.com/p/631499480
    1. Optimization on DPDK memory free list that improved performance by 30x in high fragmentation scenario.

13. Open challenges in LLM research - Chip Huyen
    https://huyenchip.com/2023/08/16/llm-research-open-challenges.html
    1. Reduce and measure hallucinations
    2. Optimize context length and context construction
    3. Incorporate other data modalities
    4. Make LLMs faster and cheaper
    5. Design a new model architecture
    6. Develop GPU alternatives
    7. Make agents usable
    8. Improve learning from human preference
    9. Improve the efficiency of the chat interface
    10. Build LLMs for non-English languages

14. 百度智能云块存储 EC 系统的构建 - DataFunSummit 2023
    https://www.zhihu.com/question/463802588/answer/3178773084
    1. Inline EC + Offline EC. Append-only. Cost, durability, performance triangle.
    n. related materials
        1. 面向百度网盘的大规模数据面存储架构思考与设计
           https://zhuanlan.zhihu.com/p/587758798
            1. ARIES, A Reliable and Integrated Exabytes Storage
            2. Table Space -> Volumelet -> Slice -> Shard
            3. 实时校验，后台周期性校验，跨系统校验（与网盘）
            4. 成本Trade-off
                1. EC最低可达1.2副本
                2. 引入磁带库
```

The physics, symmetry, and group theory part.

```
15. 现代数学的基石—李理论，这就是你彻底理解它的方式，一定让你茅塞顿开 - 康托的天堂
    https://zhuanlan.zhihu.com/p/652585224
    1. good

16. 2的多少次方能包含所有6位数组？ - Haoqiang Fan
    https://www.zhihu.com/question/613498303/answer/3179547932
    1. good

17. 为什么纤维丛理论如此重要？ - 返朴
    https://www.zhihu.com/question/39293640/answer/3181597494
    1. good
    n. related materials
        1. A Quick Intro to Fiber Bundles (Hopf Fibration)
           https://www.youtube.com/watch?v=dkyvZo68IoM

18. 几何学中最伟大的发明之一——流形，其背后的几何直觉与数学方法 - 康托的天堂
    https://zhuanlan.zhihu.com/p/622263134
    1. useful

19. From Nother Theorm to General Relativity Theory.
    Very good. I skipped the detailed notes.
    0. marked materials
        1. 诺特定理，最美妙的数学思想之一，把对称的概念推广到了极致 - 康托的天堂
           https://zhuanlan.zhihu.com/p/481658443
        2. 最小作用量原理 - Y.Galbort
           https://zhuanlan.zhihu.com/p/168781828
        3. General Relativity Explained simply & visually - Arvin Ash
           https://www.youtube.com/watch?v=tzQC3uYL67U
        4. The Maths of General Relativity (1/8) - Spacetime and Worldlines - ScienceClic English
           https://www.youtube.com/watch?v=xodtfM1r9FA
        5. 20分钟带你从牛顿力学到拉格朗日力学再到哈密顿力学！-从宏观力学到微观力学，你只需关注我！！
           https://www.bilibili.com/video/BV1za41167an
           	1. Physics with Elliot
        6. 简单明了，广义相对论的新可视化解释方法
           https://www.bilibili.com/video/BV13X4y1V7WP
        8. The Most Important Math Formula For Understanding Physics - Physics with Elliot
           https://www.youtube.com/watch?v=HQsZG8Yxb7w
        9. Field Theory Fundamentals in 20 Minutes! - Physics with Elliot
           https://www.youtube.com/watch?v=13hCkUiu_mI
        10. Physics Students Need to Know These 5 Methods for Differential Equations - Physics with Elliot
            https://www.youtube.com/watch?v=0kY3Wpvutfs
        11. The Road to Reality: A Complete Guide to the Laws of the Universe - Roger Penrose
            https://www.amazon.com/Road-Reality-Complete-Guide-Universe/dp/0679776311
        12. Einstein Field Equations: A Step-By-Step Derivation (Two Ways) - Profound Physics
            https://profoundphysics.com/derivation-of-einstein-field-equations/
        13. The Maths of General Relativity (4/8) - Metric tensor - ScienceClic English
            https://youtu.be/sEDFHMLPaW8?si=y6tkChGCvxLVzSPS
        14. What is the difference between a metric tensor and a Riemann curvature tensor in mathematics?
            https://www.quora.com/What-is-the-difference-between-a-metric-tensor-and-a-Riemann-curvature-tensor-in-mathematics
        15. How Einstein Got His Field Equations - S. Walters
            https://browse.arxiv.org/pdf/1608.05752.pdf
        16. ChatGPT4 notes: Geodesics in General Relativity
            https://chat.openai.com/share/0f72b633-c2a3-46f8-9854-afa062f01ec6
        17. Tensor Calculus 22: Riemann Curvature Tensor Geometric Meaning (Holonomy + Geodesic Deviation)
            https://www.youtube.com/watch?v=-Il2FrmJtcQ&list=RDCMUCN8wTUlSAroLslWyf87E2pw&start_radio=1
    1. 诺特定理，参考系变换不变性，守恒、对称、群论
    2. 拉格朗日量（力到“场”），欧拉-拉格朗日方程，最小作用量原理
    3. 参考系变换不变性，守恒、对称、群论
    4. 哈密顿量、相空间，测不准原理
    5. 微分方程级数解法、拉普拉斯变换、哈密顿变换（力场互换）
    6. 场论，参考系、场与力的变换
    7. 狭义相对论，闵可夫斯基时空，度规
    8. 洛伦兹变换、变换群，庞加莱群
    9. 广义相对论、微分流形、黎曼曲率, Einstein field equation.
    10. 光速限制、力的locality局限、到场论
    11. 测地线, Spacetime curvature, metric tensor, Minkowski metric,
    12. christoffel symbols, Riemann curvature tensor, Ricci tensor, 
	13. Worldline, 固有时间
	14. Schwarzschild metric, Ricci tensor
```
