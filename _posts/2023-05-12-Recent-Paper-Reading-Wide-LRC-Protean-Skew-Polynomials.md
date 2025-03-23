---
layout: post
title: "Recent Paper Reading: Wide LRC, Protean, Skew Polynomials, etc"
tagline : "Recent Paper Reading: Wide LRC, Protean, Skew Polynomials, etc"
description: "Recent Paper Reading: Wide LRC, Protean, Skew Polynomials, etc"
category: "Paper Reading"
tags: [storage, paper, erasure-coding]
---
{% include JB/setup %}

Search keywords for recommended papers:

  * (as) (a) reference, reference (architecture).
  * very good, good, interesting.
  * very useful, useful.
  * my question(s).

## Papers

Custom Scheduling in Kubernetes, etc.

```
1. Compositional Model Checking of Consensus Protocols Specified in TLA+ via Interaction-Preserving Abstraction    [2022, 1 refs, SRDS22 Best Paper]
   https://zhuanlan.zhihu.com/p/580744043
   https://arxiv.org/abs/2202.11385
   https://github.com/Disalg-ICS-NJU/IPA
    1. "针对模型检验中面临的状态爆炸问题，提出了一种针对分布式系统 TLA+ 规约的组合模型检验技术 IPA（Interaction-Preserving Abstraction）。IPA 技术针对分布式系统 TLA+ 规约的特点，提出通过“模块划分”、“保交互抽象”和“模块组合”完成组合模型检验的方法，证明组合模型检验的正确性，有效降低了模型检验的复杂度
        将 IPA 技术应用到经典分布共识协议 Raft 和阿里巴巴云数据库 PolarDB 的分布共识协议 ParallelRaft 的正确性保障中，初步展示了 IPA 技术的可行性与有效性"
    2. highlights
        1. "Experimental evaluation shows that the cost for direct checking is up to about 300 times of the cost for compositional checking using our IPA framework"
        2. essentially, it first cut the original model into sub modules, then each module is refined to only include external facing variables and actions. the refinement makes sure new module is a truncated "sub-graph" of the original, so that the original module is being verified. External facing variables and actions are "transitive", i.e. to make sure new module includes all that are needed.

2. Cloudy with High Chance of DBMS: A 10-year Prediction for Enterprise-Grade ML    [2019, 27 refs, CIDR20]
   https://arxiv.org/pdf/1909.00084
    1. Enterprise Grade Machine Learning (EGML). The below Zhihu article already summarized key findings.
       I more wonder how this paper does collection, analysis, and to derive the Visions. 
    2. highlights
        1. key insights
            1. An ML model is software derived from data. Both software and ML model need CI/CD
            2. the actual model development represents less than 20% of most data science project lifecycle
        2. suggestions (not captured in the Zhihu article)
    
    n. related materials
        1. Cloudy with High Chance of DBMS: A 10-year Prediction for Enterprise-Grade ML - 约修亚
           https://zhuanlan.zhihu.com/p/446414853
            1. mentioned as a "visionary paper" that many points are validated in the recent 3 years.
            2. "不同于常见的 research paper，visionary paper 一般更强调对某一领域未来发展的前瞻。在这一篇论文中，来自微软的作者们发表了根据他们15+年行业经验和最近的观察实践等等总结出来的对未来10年的数据库和机器学习如何整合的展望"
            3. "文章中的观点主要由作者们的一手工程实践经验、企业访谈、GitHub 项目分析、行业竞品比较、机器学习社区科研五个维度总结形成
                工程实践经验（First-hand experience）
                    一个机器学习模型也是用数据发展来的软件 (An ML model is software derived from data)
                    模型的开发训练环节实际上只占据整个项目生命周期的20%
                企业访谈（Conversations with enterprise）
                    企业中机器学习应用实际上常由比较小规模的、缺乏经验的团队来开发
                GitHub 项目分析（GitHub analysis）
                    GitHub 上的机器学习项目有逐渐集中于几个大项目（numpy, pandas, sklearn 等等）的趋势，所以 EGML 尽管需要满足比较广泛的需求，但是可以优先适配这些比较核心常见的项目。
                行业竞品（Competitive landscape）（下图）
                    成熟的专有解决方案对数据管理有越来越好的支持
                    实现完整可用的第三方解决方案是不容易的
                机器学习社区科研"
            4. "作者们认为在接下来的10年主要有3个领域是 DBMS for EGML 整合的重点：
                    模型开发/训练（Model development/training）
                    模型评分（Model scoring）
                    模型管理/治理（Model management/governance）"
            5. "作者们对于未来模型推断的展望主要如下：
                    数据库中的模型推断（In-DBMS inference）
                    架设模型和应用之间的桥梁（Bridging the model-application divide）
                尤其对于第一点数据库中的模型推断，作者们认为不同于目前的单独容器化服务的模型推断的解决方案，数据库中model 可以作为首要的数据类型而对其进行支持，使得
                    数据库的事务可以用于模型的更新和部署
                    模型推断可以作为一种关系型查询的操作
                为了更好的支持数据库中的模型推断，未来还需要数据库中的 model pruning、model-projection pushdown、model clustering 等等方面的工作。"
            6. "未来数据库如何更好的支持机器学习的数据管理也是文章作者们着墨比较多的部分。这里，作者们总结了3点：
                    数据发现、访问和版本控制（Data discovery, access and versioning）
                    模型管理（Model management）
                        这里可以依赖关系型数据库来管理训练好的模型
                    模型追踪和溯源（Model tracking and provenance）"

3. Custom Scheduling in Kubernetes: A Survey on Common Problems and Solution Approaches    [2022, 0 refs]
   https://web.archive.org/web/20220703100532id_/https://dl.acm.org/doi/pdf/10.1145/3544788
    1. mentioned by Grissom Wang as "读完就可以建立起k8s完整的调度知识体系，现状以及优化方案".
       good paper as an overview summary about how and what to build about custom scheduler
    2. Highlights
        1. Customization/extension options
            1. Source code modiication
            2. Extender mechanism: calls an external process via HTTP/S in order to execute custom iltering and scoring functions
            3. Custom scheduler: workload owners can nominate their preferred scheduler in the pod definition
            4. Scheduling framework: turn the scheduler into a pluggable component, where multiple plugins could be enabled/disabled
            5. Input to the scheduler from another component
        2. Fig. 3. Classification of the surveyed contributions based on their objectives. This is interesting and useful. 
            1. Workload performance
                    Interference and colocation
                    Lack of support for network QoS
                    Topology-awareness
                    No support for co-scheduling
                    No support for batch scheduling
                    No support for data locality awareness
               Cluster resource usage
                    Lack of real load awareness
                    GPU sharing
               Environmental impact
        3. Fig. 4. Overall classification of the surveyed contributions. This is interesting and useful.
            1. Objective
                    Workload performance optimization
                    Cluster resource usage optimization
                    Reduction of environmental impact
               Target environment
                    Cloud ML/DL cluster
                    Edge/Fog
               Target workloads
                    AI/ML
                        Training
                        Inference
                    Analytics
                    Serverless
                    Stateful apps
                    VNFs
                    Network-intensive
                    Delay-sensitive
                    Heterogeneous
               Affected scheduling operation
                    Sorting
                    Filtering
                    Scoring
               Implementation approach
                    Source code modification
                    Scheduler extender
                    Custom scheduler
                    Scheduler framework
                    Input to the scheduler from another component
                    None
               Evaluation approach
                    Real cluster
                    Simulations
                    None
        4. the following aspects are missing or have not been studied much in the literature
            1. Small cluster sizes used in evaluations
            2. Limited number of contributions leveraging the new scheduling framework ([96] and Section 2.1.4)
            3. A common repository for hosting the scheduler plugins
            4. Leveraging historical scheduling data to improve scheduling decisions based on ML
            5. Cold start problem
            6. Decision making at the edge - Scheduling delay

4. Optimizing Hyperspace Hashing via Analytical Modelling and Adaptation    [2014, 6 refs]
   https://www.gsd.inesc-id.pt/~romanop/files/papers/ACR14.pdf
    1. As mentioned in HyperDex pdf, Hyperspace Hashing is a new better placement method compared to 1) consistent hashing 2) contiguous key space partitioning
       "By leveraging on hyperspace hashing, HyperDex can handle partial searches very efficiently. On the other hand, maintaining indexes does introduce additional costs on the execution of inserts and updates"

    2. highlights
        1. what is Hyperspace Hashing
            1. It's more like contiguous key space partition rather than hashing. multi-dimensional key spaces are cut into hypercubes. each hypercube is mapped to a server. the hypercube itself holds consecutive and ordered key ranges (which is not like hashing at all).
            2. Dedicated metadata server: "A directory keeps the mapping among regions and servers"
        2. Efficient partial searches
            1. Given key <city,price,stars>, a partial key <"city=Paris","price<=120"> can directly map to which hypercube to search, i.e. map to a server.
            2. My questions
                1. On a server node, how is parity key search done? which type of index is used for it? hypercube is not taking place at this level
                    1. See "HyperDisk"
                2. How does the Hyperspace Hashing compare to Z-Order?
                3. Given fixed total server count, Hyperspace Hashing has drawbacks compared to indexing by a single primary key, if the query is only asking for primary key.
                   Normal approach accessed server count: queried primary key range / total primary key range * total server count
                   Hyperspace Hashing: the hypercubes of the same primary key range can involve different secondary key ranges, they are hosted by more than one servers. In the end, more servers are needed to search from
        3. AUTO-CONFIGURING HYPERDEX
            1. generating all combinations, and use the Model to evaluate which is the best

    n. related materials
        1. An Introduction to HyperDex and the Brave New World of High Performance, Scalable, Consistent, Fault-tolerant Data Stores
           https://www.usenix.org/system/files/login/articles/escriva12-06.pdf
            1. Logged in article section
            2. Note HyperDex is a distributed KV store with strong consistency. It supports accessing by secondary keys

        2. HyperDex: A Distributed, Searchable Key-Value Store    [2012, 290 refs]
            1. Github - https://github.com/rescrv/HyperDex
               More information is available at http://hyperdex.org/
                1. But .. "The domain hyperdex.org is for sale" .. the company is already gone?
                2. Last commit 2016 Dec.1
            2. Hyperspace Hashing placement. Value-Dependent Chaining replication.
            3. highlights
                1. HyperDex partitions a high-dimensional hyperspace into multiple low-dimension subspaces
                    1. "In contrast, an alternative design choice is to store a full copy of each object in each subspace"
                       "The HyperDex implementation, however, relies upon the latter approach to implement the replication scheme"
                       I.e. Value Dependent Chaining
                    2. This is similar with C-Store. A subspace is a column set.
                2.  HyperDex recursively leverages the hyperspace hashing technique to organize the data stored internally on a server. Called HyperDisk
```

Google LRC.

```
1. Practical Design Considerations for Wide Locally Recoverable Codes (LRCs) [2023, 0 refs, FAST23, Google]
   https://www.usenix.org/conference/fast23/presentation/kadekodi
    1. Very good paper. "Figure 4" is the best chart to understand all code construction.

       "Optimal Cauchy LRC" seems the best we can do with a Folded LRC, which is symmetric. It reaches Distance Optimal. But it's still worse than Azure LRC, and sometime it has fewer recoverable cases than Azure LRC, when losses is beyond of distance. 
    
       "Uniform Cauchy LRC" seems a nice trick, that jumped out of it when "Optimal Cauchy LRC" hits the dead end. It creates a balance between Azure LRC and Folded LRC, and exploit that local groups are no longer symmetric. "Azure LRC +1" doesn't perform well, but it's a bridge to goto Uniform Cauchy LRC.
    
       But the concerns for Folded LRC should still apply to "Uniform Cauchy LRC":

         1) Some loss combinations that are beyond distance, is recoverable by Azure LRC (which is non Folded), but not an Folded LRC. Though Figure 5 tries to prove "Uniform Cauchy LRC" recovers more patterns, but are there more strict math proofs?

         2) When loss hits folded local group and need rec-read or recover, Folded LRC incurs larger local rec-read width. This issue is hidden in Table 2, because Azure LRC is averaging its global parities. user reads data symbol but not global parity. 
       
         3) Note, "Uniform Cauchy LRC" is NOT "Distance Optimal", though "Optimal Cauchy LRC" is Distance Optimal. Although the only usable codec on production is "Uniform Cauchy LRC", the paper still talked much about "Distance Optimal". Really good at packaging papers :-D

         4) But reading more carefully, I didn't find "Uniform Cauchy LRC" actually used on Google Production (it's other LRCs). What's the blocker here that are not mentioned in this paper?
    
         5) Uniform Cauchy LRC is not Distance Optimal. There should be a ratio of non recoverable combo within loss < r+1. But this is not shown in Figure 5 neither.

         6) Azure LRC can achieve both Distance Optimal and MR. But MR needs careful matrix construction. Is the compare in this paper using MR Azure LRC? If not, it's not a fair compare.

         7) Another missing point in the paper is, how "Uniform Cauchy LRC" compares to a general Folded LRC? Folded LRC folds globals to different local groups, while "Uniform Cauchy LRC" folds all globals to one local group.

         8) Losing 1 global + 1 data at the last local group, Uniform Cauchy LRC needs global rec-read, while Azure LRC not. ADRC2 of Uniform Cauchy LRC should be worse than Azure LRC. ARC2 is better due to have included rebuilding globals.

       So, "Uniform Cauchy LRC" sacrifice local rec-read a bit, may or may not sacrifice combo recoverability, but the key advantage is it hugely reduces the cost of repairing 1 failure by folding all globals to one local group. Repairing faster is also a key factor to improve durability.

       The next challenge is to find MR coding matrix for Wide EC. It's much harder than shorter EC codecs. And we must restrict the field length.

    2. highlights
        1. "the data blocks and the global parities together form an MDS code, and the local parities are added on top of this code"
            1. So, this is referring to Folded LRC. Local reconstruction needs to take global parities, which has high rec-read width
                1. Usually, we need to split global parities and assign to different local parities
                2. Optimal Cauchy LRC is a Folded LRC that each global parity is folded to each local group 
            2. MR property (Maximally Recoverable) is defined as (1) AND (2)
                (1) If failure is inside the local group, it should recover like MDS
                (2) Each local group losses all local parities, and then lose any N = # global parity. All such pattern is still recoverable

                1. my questions
                    1. No no no. It misses a property for Azure LRC. Call it "Local group MR"
                        (3) In each local group, loss symbols N = # local parity. Plus loss more symbols N = # global parity. All such pattern is recoverable
                            I.e. "arbitrary r + 1 symbol failures can be decoded" See Theorem 1 in Azure LRC paper.
                            OK .. this is the "Distance Optimal" property
                       The missing of MR is, it assumes losing local parities first. This is too ideal.

        2. Useful concepts
            1. MR-LRC, (Coding matrix) construction
               generator matrix := Gx=y message x to codeword y
            2. n := code length, k := data symbol count, l := local group data symbol count.
               d := distance of code, i.e. An error correcting code with distance d can always correct d −1 erasure
               r := global parity count, p := total local parity count
               t := k/p, which is l which is the data symbol count in a local group (suppose each local group has only 1 local parity, data symbols are evenly assigned)
            3. "Distance Optimal LRC" (Definition 5.4): d <= (n - k) - local group count + 2 = global parity count + (1 local parity) + 1
                1. i.e. there must be 1 local parity per local group. there other parity fragments contribute to global parities
            4. Cauchy matrix - any sub-matrix is invertible
            5. Instead random simulation, say "Monte-Carlo experiment"
        
        3. Concerns of wide LRC
            1. "the wider LRC has a significantly higher number of stripes with at least 4 failures compared to the relatively narrower LRC"
            2. Constructing MR-LRCs is hard
                1. This paper's setup: field size is 2^8, code length is 25-150, storage overhead is <= 1.17x
        
        4. MTTDL evaluation
            1. "The most popular deployed LRCs we came across are the Xorbas-LRC [42], AzureLRC [27] and Azure-LRC+1 [33] constructions"
            2. "using exponential distributions representing repair time" - i.e. transition probability = 1 / repair time
            3. "In our work, replace the modeled transition probabilities with observed ones, in order to get a better estimate of the MTTDL of our codes"
                1. Interesting. "empirical measures"
                2. so, one Markov state is a mix of which local/global symbol failed.
                   the paper mentioned random failure experiment, probably how to mix them
            4. my question: It's NOT MR-LRC, so how the miss-to-recover cases map to the Markov model?
        
        5. Insights of Optimal Cauchy LRCs - Distance Optimal, MR-LRC (ideal coding matrix, but not this paper)
            1. "Indeed, this provides some intuition as to why Uniform Cauchy LRCs perform the best against random erasures. It is because the evenly sized local repair groups maximize the probability that each local repair group will see at least one failure"
            2. "the p local parities in our code are uniformly distributed across the k data, and they are all XOR-ed with the r global parity checks (this helps with proving the Distance Optimality of the code"
                1. Note it's a simple XOR. See "r˜i = ri + gk+1 + gk+2 +···+ gk+r"
            3. "we restrict ourselves to the case where each of the data symbols of the code is covered by exactly one local parity"
            4. "For simplicity of exposition we assume that p is even (we will mention how this condition can be removed"
            5. "The locality parameter l ... is k/p + r" i.e. each local group has k/p data symbols + r all global symbols, the local group has 1 local parity (folded).
            6. Distance of Optimal Cauchy LRC is r + 2, this is exactly the same setup with Azure LRC (i.e. LRC with 1 local parity per group + r globals)
        
        6. Insights of Uniform Cauchy LRC - NOT Distance Optimal, MR-LRC (ideal coding matrix, but not this paper)
            1. "For example, a code that has the same locality and distance can have different durability (as measured by mean-time-to-data-loss) and robustness against random patterns of erasures. Distance-optimality simply indicates the best distance for fixed values of n, k and `"
               "These codes are constructed in much the same way as Optimal Cauchy LRCs, except that each local parity check covers k+r p of the data blocks and global parity blocks"
                1. it should be the Folded LRC has some > distance failure cases that cannot recover, but non Folded LRC can recover
                   especially, unlike Optimal Cauchy LRC, such a (bad) codec split globals and fold to local parities
            2. compared to Optimal Cauchy LRCs, Uniform Cauchy LRC simply let the last local parity (instead of each local parity) to fold all the global parities with XOR.
               thus, proving the matrix construction has the Distance Optimal is trivial
                
                1. my question: but, proving that every loss combo recoverable by Azure LRC is also recoverable by Uniform Cauchy LRC, is missing in this paper though Figure 5 suggests YES, but we need better math analysis. Interesting 
                    
                    1. Uniform Cauchy LRC is a Folded LRC. The weakness should be losing globals to make local group recovery harder.
                       "Figure 6" is simulating losing each local parity first. But what if we force it to lose (all) global parities first?
                    
                    2. But "Uniform Cauchy LRC" seems NOT "Distance Optimal". In Figure 4d, suppose lost all global parities first, and then lost any 1 of d39 - d48, it's data unavailable.
                        
                        1. So .. being one step shorter to data unavailable, can greatly reduce the MTTDL. So how "Uniform Cauchy LRC" gets better MTTDL than "Optimal Cauchy LRC" or "Azure LRC" .. Interesting and we need testing again.
                        
                        2. Also, the worst case MTTDL of "Uniform Cauchy LRC" worth attention too. Suppose it starts from one maintenance zone failure, and right bring down a global parity.
                            1. It should add another round of MTTDL simulation supposing such upgrade scenario. Interesting.
                            2. Besides, It should add another round of MTTDL simulation / loss combo recoverability simulation, that starts from losing globals, i.e. starts from the worst case. Interesting.

                        3. Wait .. the case of losing all globals plus any 1 of d39-d48 is RECOVERABLE. C4 can cancel out the lost globals, by deducting the survived data symbols. Or, just use the coding matrix to construct the small recovery sub-matrix. It's obvious recoverable.

                        4. WHAT ARE THE ANTI- DISTANCE OPTIMAL CASES for "Uniform Cauchy LRC"? I.e. cannot recover from r+1 losses, even the coding matrix is ideal
                            
                            1. With ideal coding matrix, the Code Topology of Uniform Cauchy LRC should be ABLE TO ACHIEVE Distance Optimal
                                
                                1. Proof: Map it to Azure LRC. Any reversible sub-matrix can map back to Uniform Cauchy LRC's sub-matrix. The only difference is the later one's sub-matrix can include the last row. Divide the case by how many global parity rows are included too in the sub-matrix. Each case should be invertible, suppose matrix coefficient is well selected.

                                2. similarly, with ideal coding matrix, the Code Topology of Uniform Cauchy LRC should be ABLE TO ACHIEVE MR (Maximal Recoverability)

                            2. With this paper's Cauchy Matrix construction, is the 

                                1. I didn't verify, but since Optimal Cauchy LRC's matrix is not MR, neither should be the Uniform Cauchy LRC
                    
                    3. Compared to "Azure LRC", "Uniform Cauchy LRC" also doesn't satisfy "Local group MR"
            
            3. maintenance robust deployment - no maintenance zone upgrade would render an EC stripe unrecoverable
               maintenance robust efficient - maintenance zone upgrade only lead to local repair 
                1. MRE requires "Data symbol count + 1 < MZ count", I.e. the 

            4. So the properties of LRC drill down to
                1) Locality: If the local group size is reduced to small enough. Folding the global will (negatively) increase the local group size
                    1. And note the locality of data symbols vs locality of global parities
                2) Distance: Recoverability if all losses concentrate to one local group
                3) MR: Recoverability if losses are distributed evenly across all local groups
                    1. There is actually two fold of Distance Optimal and MR property
                        1) Code Topology level: Suppose coding matrix is idea, whether it can achieve Distance Optimal and MR
                        2) Coding matrix construction: Whether there is method to find the idea matrix
                            1. The challenge is, even Code Topology allows MR, finding such real coding matrix for Wide EC is non trivial

            5. "The later experimental analysis of these codes highlights the point that distance optimal (i.e. on the generalized Singleton bound) does not mean most-durable or most cost-efficient from a practical perspective."
                1. Interesting .. Uniform Cauchy LRC gave up Distance Optimal. But this choice opens the gate for new opportunities of EC codecs.
                   The "fair" measurement of durability goes from shortest steps to data unavailable, to unrecoverable loss count / total combo count.

        7. Azure LRC: Distance Optimal, MR-LRC (but it needs non trivial effort and math of find the optimal coding matrix)
            1. my question: Is the Azure LRC used in this paper using MR coding matrix?
                1. Azure LRC should support MR coding matrix. But finding such matrix is non trivial. If the paper is not using MR Azure LRC, then it's NOT a fair compare.

        8. Folded LRC
            1. Another missing point in the paper is, how "Uniform Cauchy LRC" compares to a general Folded LRC? Folded LRC folds globals to different local groups, while "Uniform Cauchy LRC" folds all globals to one local group.
            2. Suppose ideal matrix, can the Code Topology of Folded LRC achieve Distance Optimal and MR?
                1. Yes. Both. Same approach as how Uniform Cauchy LRC to prove Code Topology Distance Optimal and MR
                2. The problem of Folded LRC is, if global parity is lost, frequently it needs to do global rec-read for a local group repair
                3. But, if all globals are lost, Azure LRC is very vulnerable to data unavailable.
                   Folded LRC is more likely to recover, because local parity encodes global parity coefficients
                   Uniform Cauchy LRC acts similar with Folded LRC in this sense, but only the last local parity encodes global parity coefficients
                    1. Suppose all global parities are lost, and local group 2 lost 2 additional parities. Azure LRC Code Topology can never recover, but Uniform Cauchy LRC or Folded LRC still have chance, suppose coding matrix is ideal
                    2. Interesting .. In this sense, Folded LRC or Uniform Cauchy LRC are a mix of Azure LRC with CRS. If you see the coding matrix 

    3. my questions
        1. What is the hardware SKUs used in this paper?
            1. As much as I can find
                1. "Figure 1 shows data unavailability events from a deployed wide LRC of width ≈ 50 blocks along with their erasure patterns captured from four large storage clusters at Google with a total disk population of over 1.7 million disks, over a period of one year."
                2. "storage administrators have informed us that the total number of maintenance zones in a single cluster are typically restricted to below 20"
            
            2. It's critical that how Wide EC to fit into maintenance zones. If EC codec is longer, but each maintenance zone is put yet more symbols to fail together, it's then not helping to leverage Wide EC to reduce COGS while maintaining durability
                1. So, here's the problem. Though the paper evaluated MTTDL, it missed to evaluate durability/availability when an maintenance zone is down, plus random failures.
            
            3. "Thus, with z ≈20, all schemes except 96-of-105 can be deployed in a maintenance-robust-efficient manner for Uniform Cauchy LRCs"
                1. So, Google cluster should using 20 maintenance zones. This is a common setup actually. But interesting that this is already viable to run Wide EC.

        2. From the paper, it should be using Folded LRC, with 1 local parity per group, and local groups are of equal size.
        
        3. Figure 3, Azure-LRC+1, Non-folded LRC, and giving globals also a local parity. Anyway, Azure-LRC+1 performs worst in Table 2 evaluation 
        
        4. ADRC and ARC1, ARC2. They only measure the losing of first 1 or two symbols. In real, we should weighted sum up the cost by each of the losing count. In case, in high losing count there is sharp cost increase.
        
        5. Optimal Cauchy LRC is maximizing the distance (section 6.2). Suppose it's MR. But compared to Azure LRC, we don't know if there is any pattern the is beyond the distance, but NOT recoverable by Optimal Cauchy LRC, and DOES recoverable by Azure LRC
            1. OK .. Figure 5 explained the doubt. Optimal Cauchy LRC can be a little bit worse than Azure LRC, but Uniform Cauchy LRC appears better.
        
        6. In Table 2, Locality table, Azure-LRC's locality should be k/p == 12, but why the table writes 24,48,72,96? 
            1. It seems incorrect
            2. If Azure-LRC uses 12, "Uniform Cauchy LRC" does NOT have the smallest locality (section 8)
            3. OK .. papers explains the definition trick: "Since Azure-LRC requires reading all data blocks to reconstruct any failed global parity, ..."
        
        7. Solely a Figure 4 + Cauchy matrix tricky can summarize the entire paper content. But Google guys still managed to write a whole paper. Interesting. Worth learning.
        
        8. In Table 2 ARC1, Azure LRC performs worse, because repair global parity is counted in. But in real production, we only care data, and global repair can be pushed off.
            1. In this sense, Azure LRC still has a "better" ARC1 compared to Uniform Cauchy LRC
            2. ARC2 losing 2 symbols are also tricky. The paper didn't give the formula. But Azure LRC shouldn't be that bad, because losing 2 data symbols frequently need global reconstruction, which is also the case of Uniform Cauchy LRC.
                1. In ARC2, Azure LRC can still be worse than Uniform Cauchy LRC. Thinking losing 1 global and losing 1 data in local group 1. Azure LRC still needs global rec-read to repair the global fragment

        9. Figure 4d, how are local group sizes divided?
            1. Trivial: "In the event that p - (k +r), we may simply divide the k +r data and global parities as evenly as possible amongst the p local checks."

        10. Coding matrix construction for Optimal Cauchy LRCs. The paper explains why it's Distance Optimal, but NOT why it's MR
            1. First, let's understand why the construction is Distance Optimal, i.e. to recover any r+1 failures.
                1. First, let's prove the coding matrix before folding is Distance Optimal. I.e. Cauchy Matrix with the last row cut into each local parities
                    1. Suppose lost s data symbols, and t global symbols.
                        Case 1: s+t = r+1
                            Then s = r-t+1, and sub-matrix size is s*s, and no local parity lost
                            So we pick r-t survived global parities, and one local parity row.
                            This will build the invertible Cauchy sub-matrix s*s, to decode lost data symbols
                        Case 2: s+t < r+1
                            Then r-t >= s. Then we pick s survived global parities.
                            This will build the invertible Cauchy sub-matrix s*s, to decode lost data symbols
                2. Now we come to Optimal Cauchy LRC, that each local parity has folded an XOR of each global parity
                    1. Suppose lost s data symbols, and t global symbols.
                        Case 1: s+t = r+1
                            Then s = r-t+1, and sub-matrix size is s*s, and no local parity lost
                            So we pick r-t survived global parities, and one local parity row.
                            Then we have a matrix like [g1, g2, g3, l1 + g1 + g2 + g3], g* is global party row, l* is local parity row. Suppose t=0.
                              Or we have [g2, g3, l1 + g1 + g2 + g3], suppose t=1. It maps to [g2, g3, l1 + g1]. It maps to [g2, g3, g4 + g1] sub-matrix
                              Or we have [g3, l1 + g1 + g2 + g3], suppose t=2. It maps to [g3, l1 + g1 + g2]. It maps to [g3, g4 + g1 + g2] sub-matrix
                            Will these sub-matrix be still invertible?
                                1. We don't know if a Cauchy Matrix + Row wise elementary operation, is still Any Sub-matrix invertible.
                                   If YES, this property can be used to verify the above. Interesting. Need to verify.
                            How the paper proved invertible? It's totally a different way
                                1. "Now consider the case when the r +1 deleted rows do not contain any of the rows r˜1,r˜2,...,r˜p. In this case, we can compute gk+r+1 = r˜1 + r˜2 + ··· + r˜p, which reduces to the case when r +1 rows are deleted from G(k+r+1),k ."
                                2. I.e. g4 is restored by XORing all local parities. Here Optimal Cauchy LRC requires the number of local groups are even.
                                   Then with g4, we have enough global parities to decode all lost data symbols.
                                    1. So, this also implies, if Optimal Cauchy LRC lost all globals, and 1 data, then it needs global rec-read to repair
                                        1. this also implies if lost globals, the global rec-read width would be longer than Azure LRC, because it needs to XOR each local parity.
                                    2. Similarly, Uniform Cauchy LRC, if losing >=1 global and 1 data at the last local group, it would need global rec-read to repair
                                       but Azure LRC only needs local rec-read.
                                3. So, this trick is NOT applicable to Uniform Cauchy LRC. So, Uniform Cauchy LRC by this coding construction is NOT Distance Optimal. 
                                4. Also, for Folding LRC, this trick is NOT applicable. We CANNOT naively say Folding LRC is Distance Optimal
                        Case 2: s+t < r+1
                            Then r-t >= s. Then we pick s survived global parities. This will build the invertible Cauchy sub-matrix s*s, to decode lost data symbols
                            Same. We only need to pick global parities.

        11. Wait .. Uniform Cauchy LRC isn't actually deployed on Google production? There must be problems are not mentioned in this paper. Google is using LRC indeed.
            "The deployed code had total width n ≈ 50, and always succeeded in recovering data when there were ≤ 6 failures. We then test these failure scenarios with the Uniform Cauchy LRC of the same width and overhead. The deployed code could not recover any of the 278 stripes before restoration, whereas Uniform Cauchy LRC simulation was successful in recovering 92 stripes prior to restoration; a success ratio of 33%."

        12. Wait .. Uniform Cauchy LRC is NOT Distance Optimal. Figure 5 should have given the Recovery Ratio within distance d, e.g. "4 failures" in "48-of-55 code"
            1. It should add such simulation analysis. Interesting

        13. At 2-failure of 1 global and 1 local at the last local group, Uniform Cauchy LRC needs global rec-read, but Azure LRC only needs local rec-read
            1. Interesting. So we need to drill down Table 2's ARC2, and analyze how many cases in 2 failure need global rec-read, and how many only need local rec-read.
            2. Are there 2-failure cases that Uniform Cauchy LRC only needs local rec-read, but Azure LRC needs global rec-read?
                1. Goto the coding matrix, Uniform Cauchy LRC strictly have more coefficients at each row, compared to Azure LRC. I.e. the last row. So
                   Case 1: Losing 2 data symbols. No such case
                   Case 2: Losing 1 data + 1 local. No such case
                   Case 2: Losing any global. Here's the catch. Azure LRC needs global rec-read to reconstruct global parity. Uniform Cauchy LRC may doesn't need it
                2. So, this explains why ARC2 of Uniform Cauchy LRC is better than Azure LRC
                3. But, In ADRC2, Uniform Cauchy LRC should be worse than Azure LRC. Think losing 1 global + 1 data in the last local group of Uniform Cauchy LRC

    n. related materials
        1. Improved Maximally Recoverable LRCs using Skew Polynomials    [2022, 16 refs]
           https://www.usenix.org/system/files/fast23-kadekodi.pdf
           https://arxiv.org/abs/2012.07804
            1. As referenced in the parent paper: "To the best of our knowledge, the current state of the art constructions are in [18]"
        
        2. VAST: Providing Resilience, Efficiently: https://vastdata.com/blog/providing-resilience-efficiently-part-ii/    [2019]
            1. As referneced in the parent paper: "Wide codes are known to be deployed in two commercial settings, VAST [50] and Backblaze [3]"
            2. VAST is also mentioned in paper "Exploiting Combined Locality for Wide-Stripe Erasure Coding in Distributed Storage"
            3. From the picture, VAST is using 10+4 on 20 racks
        
        3. Erasure coding used by Backblaze: https://www.backblaze.com/blog/reed-solomon/    [20150616]
            1. As referneced in the parent paper: "Wide codes are known to be deployed in two commercial settings, VAST [50] and Backblaze [3]"
            2. Also, the AFR report: https://www.backblaze.com/blog/hard-drive-stats-q2-2019/
            3. Backblaze is a cloud storage vendor (Backblaze B2), that deployed Wide codes
                1. Comparing with AWS S3/Azure/Google Cloud: https://www.backblaze.com/b2/cloud-storage-pricing.html
                2. Why do people use Amazon S3 when Backblaze B2 is 1/4 the cost of S3 and also includes a CDN for free.
                   You also get way faster access speeds with Backblaze vs Amazon since they tier their IO speeds.
                   https://news.ycombinator.com/item?id=22299954
                    1. Backblaze storage is not regional replicated, unless you explicitly pay twice
                    2. "any file is "sharded" across 20 different servers in 20 different racks in 20 different locations inside that datacenter"
            4. Cloud Backup Showdown: Azure vs Amazon S3 vs Google Cloud vs Backblaze B2 (2022/12)
               https://www.cloudwards.net/azure-vs-amazon-s3-vs-google-vs-backblaze-b2/
                1. "Backblaze B2 does not encrypt your files at rest"
                2. AWS S3 KMS: https://docs.aws.amazon.com/kms/latest/developerguide/services-s3.html
            5. BackBlaze should be using CRS 17+3: "When a file is stored in a Vault, it is broken into 17 pieces, all the same size. Then three additional pieces are created that hold parity, resulting in a total of 20 pieces. The original file can then be reconstructed from any 17 of the 20 pieces."
               EC lib should be by Java: "We needed a simple, reliable, and efficient Java library to do Reed-Solomon coding, but didn’t find any. So we built our own. " 
                1. But note, the article date is pretty old

        4. Tiger: {Disk-Adaptive} redundancy without placement restrictions    [2022, OSDI, 2 refs]
            1. mentioned in Google LRC paper as a study of Placement restrictions
            2. logged later

        5. Tamo Barg LRCs: A family of optimal locally recoverable codes    [2013, 516 refs]
           https://arxiv.org/abs/1311.3284
            1. As referenced in the parent paper: "Tamo and Barg [47] were among the first to provide a general construction of distance-optimal LRCs (with small field sizes), but with some constraints on the allowable parameters."
```

Protean, etc.

```
1. Protean: VM Allocation Service at Scale    [2020, 72 refs]
   https://www.usenix.org/conference/osdi20/presentation/hadary
   https://www.microsoft.com/en-us/research/publication/protean-vm-allocation-service-at-scale/
    1. Good, can be used as a reference architecture.
       Azure Compute layer VM allocation system. A single Protean serves 10-100K servers in an AZ. high throughput and utilization (85-90% on a key utilization metric)
    2. highlights
        1. key designs
            1. a clear separation between policy and mechanisms, a flexible rule-based Allocation Agent (AA)
                1. policy - rule based AA, mechanism - multi-layer caching infrastructure implementation
            2. a multi-layer caching mechanism expedites the allocation process
                1. including
                    a shared cache - frequently accessed data across all AAs
                    a rule cache - rule evaluation results
                    and a machine cache - previous VM placement results on each machine, to avoid placing on same machine again
                2. journal to keep track of changes, to ensure cache consistency
                    1. every cached object stores the revision number it has seen, global revision number is self-incremental
                    2. An object brings itself up to date by reading only the journal records with higher revision numbers
                3. efficient cache update mechanism
                    1. a background update mechanism that opportunistically updates the caches when an AA has no requests to process
            3. A slight compromise on allocation quality enables multiple AAs to run concurrently on the same inventory, resulting in increased throughput with negligible conflict rate 
                1. Each AA processes requests independently and makes placement decisions based on its own view of the inventory. A shared pub/sub service distribute incoming requests to all AAs
                2. verifies that the new placement decision does not over-commit the machine resources or violate other anti-colocation constraints
                   If the new placement decision violates any of these constraints, the mechanism merges the new placement decision with the current state of the machine as part of the commit
                3. Protean employs a hybrid strategy for selecting a machine in its final step to address the challenge of AAs identifying highly overlapping sets of best machines if their respective requests are similar
                    1. The AA selects from the set of best machines in periods with no conflicts. Otherwise, avoid conflict by randomly select a machine from top N0 machines.
                    2. N0 is dynamically tuned with past conflict failures in a sliding window. By observation, high-load and conflicting periods are infrequent
            4. adapted to handle capacity crunch conditions
                1 COVID-19, increase utilization limits in each cluster by 1%, identify fragmented machines by what-if analysis, migrate VMs to pack capacity
        2. Simulations
            1. High-fidelity simulator: Connect the prod allocator directly with simulation data.
                1. This is an interesting and practical solution when building algorithm heavy component. 
            2. Low-fidelity simulator: Write another dedicated simulator for study.
        3. others
            1. "reuse distance" - which for each request of VM type v, measures the number of unique VM types requested since the last time that v was requested
                1. a short and highly biased reuse distance is the base that allocator can benefit from cache
                2. "Locality in requests" - each VM request is characterized by a vector of trait values
            2. Validator rules vs Preference rules
            3. Changes and slow and usually known by AA
                1. "However, allocation-related events are the dominant reason for such changes. Hence the machines that change between consecutive executions of the AA are primarily the machines whose states were altered as a result of allocation decisions made by other AAs running in parallel. Since the number of parallel AAs is relatively small, there are typically not many such changes"
            4. Allocation quality - packing density
                1. we focus on CPU because it is typically the bottleneck resource
            4. Protean scheduling is online rather than batching
                1. "A subset of these schedulers, optimizes placement decisions by batch-processing multiple jobs together [19, 21, 24]. Our demanding latency and throughout requirements preclude using these approaches."

2. ParaRC: Embracing Sub-Packetization for Repair Parallelization in MSR-Coded Storage    [2023, FAST23, 0 refs]
   https://www.usenix.org/conference/fast23/presentation/li-xiaolu
   Source code: http://adslab.cse.cuhk.edu.hk/software/pararc
    1. Interesting. EC repair pipelining for MSR regenerating codes. Optimal repair path schedule, MLP, needs a complex resolver, computational expensive.
       But note, ParaEC on Clay Code (4,2) incurs more total Repair bandwidth, while reduced the Maximum repair load.
       Built on HDFS and evaluated in Alibaba Cloud.
    2. highlights
        1. definitions
            1. Repair bandwidth: total network amount to repair a dead node.
               Maximum repair load: max amount of data to be transferred by a single node. (Including the destination node)
            2. MLP (min-max repair load point), which minimizes repair bandwidth given the minimum maximum repair load
        2. The initial idea is Can we apply Repair Pipelining for MSR codes?
            1. No. But key idea for MSR is: Repair of a sub-block requires a subset of available sub-blocks
               We can distribute repair of sub-blocks across multiple nodes for load balancing
        3. Modeling the parallel repair pipeline for MSR trade off between Repair bandwidth vs Maximum repair load
            1. Propose a heuristic to find approximate MLP
            2. Algorithm: vertex edge connection at sub-packet level is fixed, explore assigning different colors to vertices
                1. it's a bit like DB optimizer. DP with a shared queue.
        m. My questions
            1. If ParaRC is adding more hops in the repair path, will it increase the total network bandwidth cost?
                1. This is a general concern of EC repair pipelining. But no, since total Repair bandwidth has no change.
            2. If ParaRC is adding more hops in the repair path, will it increase the total repair delay?
                1. No. The delay is dominated by total Repair bandwidth. Extra hops only add delay to first/last packet.
            3. Problem: taking the Clay Code (4,2) example, more total Repair bandwidth
                1. Centralized repair costs Repair bandwidth 384MB, Maximum repair load 384MB
                   ParaRC repair schedule takes Repair bandwidth 448MB, Maximum repair load 320MB
            4. Is it able to find a MLP that won't increase total Repair bandwidth, but with a smaller Maximum repair load?
            5. For longer EC codecs ((16, 12)), the Heuristic searching time is tens of hours (~60)? That's really long
            6. Section 7.2 "Finding the Approximate MLP" - So, after such lengthy searching, it's still finding an approximate answer?
            7. ParaRC says it reduces the degraded read time for ~50%. But I didn't see how it happens from Figure 2 or the Motivating Example in slides?
            8. Though MLP has worse repair bandwidth, but how is degraded read time much better?
                1. See Figure 8. Both maximum repair load and repair bandwidth need to be reduced. Compared to raw Clay Code, ParaEC reduce maximum repair load, which makes a node less likely to become a bottleneck. But this doesn't work for a system already with many objects to distribute the load across nodes.
    n. related materials
        1. Clay Codes: Moulding MDS Codes to Yield an MSR Code
           https://www.usenix.org/system/files/conference/fast18/fast18-vajha.pdf
            1. State of art regenerating code. Implmemented in Ceph. MDS & MSR. Sub-packetization is (n−k)^⌈n/(n−k)⌉
        2. Bufferfly codes: Opening the chrysalis: On the real repair performance of MSR codes
           https://www.usenix.org/conference/fast16/technical-sessions/presentation/pamies-juarez
            1. State of art regenerating code. Implemented in Hadoop and Ceph. MDS & MSR. Require two-parities. Sub-packetization is 2^k - 1
        3. Repair pipelining for erasure-coded storage: Algorithms and evaluation
           https://arxiv.org/abs/1908.01527v1
            1. same author as this paper: Xiaolu Li
        4. ECDAG: OpenEC: Toward unified and configurable erasure coding management in distributed storage systems
           https://www.usenix.org/conference/fast19/presentation/li               
            1. same author as this paper: Xiaolu Li

3. Tiger: {Disk-Adaptive} redundancy without placement restrictions    [2022, OSDI, 2 refs]
   https://www.usenix.org/conference/osdi22/presentation/kadekodi
    1. Traditional EC stripe MTTDL design assumes worst disk AFR. Tiger Eclectic Stripe becomes aware of underlying disk AFR and fit reliability targets with different EC schemas
    2. Highlights
        1. Key designs
            1. Tiger - tailor stripe redundancy according to different disk AFR
                1. Eclectic stripe - an EC stripe that is aware of its underlying disk AFR and can reason about the reliability
                    1. research topic - "disk-adaptive redundancy system"
                2. Assuming disks are modeled with different AFR
            2. A novel approximation technique to speedup MTTDL calculation
                1. The base Markov model is tracking a state vector of each disk. The state space is large and (of course) expensive to calculate
                2. Eclectic Stripe uses the single chained Markov model, each state is N disk failed.
                    1. no, no, the paper's model is even simpler. It directly calculates the probability of >k disks are failing. This is not even Markov model
                    2. How to calculate the bias of the simple MTTDL model vs the base model? The paper is by sampling several EC codecs and do testing
                        1. "numerical experiments"
            3. Handling disk AFR change according to time
                1. Checking is a EC stripe is safe - by comparing with a MTTDL threshold
                2. If AFR doesn't meet requirement, do redundancy transition. look EC stripes from changed disks
                3. disk failure triggered data repair also choose the right disks that satisfy AFR needs
                4. See Figure 11. How much transition IOs are needed for redundancy transition
            4. How does Tiger handle transition overhead?
                1. HUMATA: "Tiger handles transition overhead by proactively issuing redundancy transitions to avoid transition overload. Tiger's mechanism of coalescing space-inefficient (high-redundancy) eclectic stripes into new space-efficient (low-redundancy) eclectic stripes in response to AFR reduction by moving all chunks leads to more data movement compared to moving just the chunks of the high-AFR disks (as is the case when AFR rises). However, this is a conscious design choice made in Tiger in order to maximize space-savings for non-urgent redundancy transitions at the expense of a minor increase in the IO overhead. Despite this, Tiger's average IO overhead is still at most 0.5% of the overall cluster’s IO bandwidth, which is much lower than existing background tasks such as scrubbing, that require approximately 7% IO bandwidth. Tiger also avoids urgent IO bursts during redundancy transitions by using eclectic stripes that provide much higher risk-diversity compared to other disk-adaptive redundancy systems. Tiger adapts to the changing failure rates of disks in a storage cluster and spreads out the transition overload over time, such that it can be completed within tolerable IO limits without compromising data safety."
    n. Related works
        1. Pacemaker: Avoiding heart attacks in storage clusters with disk-adaptive redundancy [2020]
            1. same authors, Saurabh Kadekodi, etc
            2. Compared with Tiger, the problem of Pacemaker is the placement constraints w.r.t. AFR subclusters of disks (Rgroups)
            3. Tiger requires less transition IO than Pacemaker due to its eclectic stripes
        2. Google LRC: Practical Design Considerations for Wide Locally Recoverable Codes (LRCs) [2023]
            1. same author, Saurabh Kadekodi
        3. HeART: improving storage efficiency by exploiting disk-reliability heterogeneity [2019]
            1. same author, Saurabh Kadekodi
            2. HUMATA: "However, HeART does not address the issue of transition overload, which can occur when thousands of disks require simultaneous redundancy transitions. This is addressed by Pacemaker, which makes conservative predictions of the rise in AFR and proactively issues redundancy transitions to avoid transition overload."

5. An In-depth Look at the Intel IPU E2000    [2023, Intel, 0 refs]
   https://ieeexplore.ieee.org/abstract/document/10067333
    1. Key capabilities: network offloading, storage offloading, Lookaside Crypto & Compression (LCE)
    2. highlights
        1. HUMATA: The Intel IPU E2000 is Intel's first ASIC IPU device, a 200G product co-designed with Google and in production as of 2022. It is a high-performance chip designed for use in cloud data centers, and it features a rich packet processing pipeline, RDMA and storage capability including NVMe offload, and an ARM Neoverse based compute complex
        2. How ARM N1 compares to ARM A53
            1. The ARM Neoverse N1 core used in the Intel IPU E2000 is a high-performance core designed for server and infrastructure applications, while the ARM A53 core used in the system management engine is a low-power core designed for mobile and embedded applications. The N1 core has a higher maximum frequency of 3GHz compared to the A53's maximum frequency of 1.2GHz, and it has a larger L2 cache size of 512KB per core compared to the A53's 128KB per core. The N1 core also supports more advanced features such as out-of-order execution, larger instruction and data TLBs, and hardware virtualization support, which are important for server workloads. In contrast, the A53 core is designed for low-power and cost-sensitive applications, and it has a simpler pipeline and lower power consumption.
    n. related materials
        1. IPU / DPU 双雄对决：英特尔 vs 英伟达
           https://mp.weixin.qq.com/s/r9isEMhycsCrYKTYTyQ3rQ
            0. Useful article.
            1. 今年二月份的2023 IEEE International Solid-State Circuits Conference (ISSCC)大会上，Intel发布了“An In-depth Look at the Intel IPU E2000”[1]
               https://ieeexplore.ieee.org/abstract/document/10067333
                1. Intel这次公开承认这个是co-designed with Google，产品已经在2022年量产了。
                2. 在ISSCC 2023的论文中，英特尔介绍了更进一步的内部设计细节。在hotchips资料中没有公开的管理单元，是由2个ARM A53的核完成。另外包括了一个32MB的系统cache。
                    1. My questions: WTF? Intel is selling ARM chips in IPU?
            2. 刚刚过去的三月份，英伟达的GTC 2023大会上，黄教主大谈了2个小时的AI，ChatGPT和GPU，当然也没有忘记DPU产品。只给了不到2分钟的时间，宣布Bluefield3量产了
                1. 大家整体的设计思路还是比较一致，都是包括计算子系统和网络包处理器子系统。
                   计算子系统大家都是基于ARM的IP，应该就是基于各自对于计算能力需求的理解，成本，产品发布时间和制造工艺来选择。
                   Intel还单独提供了A53的核来做管理平面，这个就体现出了两家对于IPU和DPU的应用场景理解的差别。
                    1. Intel的IPU全称是Infrastructure Processor Unit，有一个很大的需求是提供服务器的独立管理功能，需要和业务平面进行隔离提供更高的安全性。
                    2. Nvidia的DPU全称是Data Process Unit，定位是对Host CPU进行加速和卸载，更加注重对服务器上Host CPU的卸载和加速，独立的管理功能的考虑不够。
                    3. 各家的计算子系统技术上的差异化不大，IPU/DPU硬件上核心差异化的应该是网络子系统部分
                        1. 上面介绍了Intel是通过可编程流水线和P4来提供灵活的编程能力。
                           Nvidia是在数据通道上提供了DPA这种RSIC-V核来进行灵活编程，进一步卸载ARM核上的操作。
6. SNIA SDC 2022 storage systems
    1. Next-Generation Storage will be built with DPUs instead of CPUs    [2022, SNIA]
       https://www.snia.org/educational-library/next-generation-storage-will-be-built-dpus-instead-cpus-2022
        1. Full storage on chip DPU, no CPU. DBS - DPU-based storage. high performance, power saving, high rack density
```

LRC coding matrix construction.

```
1. Improved Maximally Recoverable LRCs using Skew Polynomials    [2022, 16 refs, IEEE Transactions on Information Theory]
   https://arxiv.org/abs/2012.07804
   https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9779224
    1. As mentioned in the Google LRC paper, the state of art construction for large LRC coding matrix with Maximally Recoverability (MR) Property.
       In general, finding MR matrix on a very large field is easy. The problem is how to find that on a practically small field size.
    2. highlights
        1. Existing works: Note GYBS17, GJX20, MK19. Note some call LRC as PMDS - Partial MDS codes.
           Most works are published on IEEE Transactions on Information theory, IEEE International Symposium on Information Theory.
           Most papers on start will tell you its results like field size.
           The topic is called "Construction of ... codes"
        2. Convenient representations
            n - code length
            r - local group size, including local parity
            a - local group's local parity count
            h - global parity count
            g - number of local groups
            q - the field size q=q0^m
            m - the field size can be F_q0 or F_(q0^m)
        3. Reed-Solomon codes are constructed using the fact that a degree d polynomial can have at most d roots
            1. A LITTLE BIT ABOUT REED-SOLOMON CODES
               https://math.columbia.edu/~dejong/courses/RS.pdf
        4. Definition 2.3: Skew polynomial ring - K[t;σ,δ≡0]
            1. ChatGPT: "Non-commutative polynomials, also known as skew polynomials, are a generalization of the usual (commutative) polynomials where the coefficients do not necessarily commute with the indeterminate"
               https://chat.openai.com/c/2e880215-4dc7-4e2b-bdb3-4d974097b3b4
            2. "and in fact the constructions in this paper only use skew polynomials with δ ≡ 0" OK .. much simplified
        5. Definition 2.9:Conjugation. Note this is not the common conjugation, it's the conjugation for skewed polynomials
        6. Example 2.13: "Therefore the centralizer of every non-zero element is F_q". This creates a mapping from F_q^m to F_q, bridged by conjugacy class 
        7. Theorem 2.17: A Skewed Polynomial can have many roots, but it can have roots in at most d distinct conjugacy classes, and the sum of dimension of the subspace of roots is no larger than d
            1. See more in Appendix C Roots of Skew Polynomials
        8. Definition 2.18: Vandermonde matrix for Skewed Polynomials version. A key property is formula (10)
        9. Corollary 2.21: This is the base matrix that is used to construct MR LRC coding matrix
            1. Construction: Proof of Theorem 1.3. It's quite straightforward, to build A_l and B_l. Then come back to the matrix of H in formula (1)
                1. My question: The the paper says H in (1) is a parity check matrix, it more looks like a generator matrix? If you see the "Proposition 1.2"
                   "Coding Techniques for Repairability in Networked Distributed Storage Systems" by Frederique Oggier better explains parity check matrix vs generator matrix
                    1. OK .. the H is still the correct parity check matrix. Note it folds global parities into local groups. And each local group includes its parities multiplying with A_l
                2. "Intuitively, in the construction each local group corresponds to one conjugacy class"
                   "The stabilizer subfield of each conjugacy class is F_q0 as shown in Example 2.13"
                   "B_i will be chosen carefully to combine well with the Vandermonde matrix A" This is the improvement from [MK19]
                    1. In 1.3 "Our Techniques" section has more explanation
                3. The "A1(S1 ∪T1)", "B1(S1 ∪T1)" matrix analysis on H(E) is actually the general applicable for all LRC codecs. This is very useful.
                4. The final proof of full rank resides at "This implies that D1,D2,...,Dt are full rank", it's actually leveraging Skewed Polynomial Vandermonde matrix
        10. Appendix D Constructions of MR LRCs where global parities are outside local groups

4. Partial MDS Codes with Regeneration (PMDS)    [2020, 5 refs, IEEE Transactions on Information Theory]
   https://arxiv.org/pdf/2009.07643.pdf
    1. Good. Combining LRC (Maximally Recoverable) with regenerating code. The regenerating parity be either as a local parity or a global parity.
       But note, regenerating code won't be effective if parity count is less than 2.
       Overall, the true limit of constructing such a versatile codec is field size.
       Local regenerating + LRC see construction 1, 1) in each row, it's an PMDS in [15], 2) and in each row's each local group, it's Ye-Barg Regenerating Codes. Note the explicit construction requires exactly 2 global parities.

     2. highlights
        1. backgrounds
            1. PMDS is LRC with Maximally Recoverable
                1. an (r, s)-PMDS code of length µn can be partitioned into µ local groups of size n, such that any erasure pattern with r erasures in each local group plus any s erasures in arbitrary positions can be recovered
            2. Locally Regenerating Code: Combining LRC and Regenerating Code
                1. Locally Repairable Code are the common LRC we mentioned
                2. When Locally Repairable Codes Meet Regenerating Codes — What If Some Helpers Are Unavailable
                   https://engineering.purdue.edu/~chihw/pub_pdf/15C_ISIT_dynamic_helpers.pdf
                    1. locally repairable regenerating codes (LRRCs)
            3. Rack-aware regenerating codes (RRCs):
                1. The distinction to regenerating codes is that the repair bandwidth is given measured in terms of the amount of data transmitted between the racks, while communication within each rack is ignored
                2. Double regenerating codes [26] refine this model by considering two levels of regeneration, a local one, i.e., within the racks, and a global one, i.e., across the racks
            4.  row-wise MDS
            5. Ye-Barg regenerating codes
            6. Gabidulin-code-based PMDS construction [4]
        2. First part: MSR PMDS codes with significantly smaller field size than the construction in [4] (which requires a field size exponential in the length of the code and the subpacketization of the local regenerating code (which may itself be exponential in the length of the local code))
        3. Second part: PMDS codes with global regeneration properties, i.e. when punctured in any r positions in each local group, becomes an MSR code
            1. Finally, for the globally MSR PMDS codes, it remains an open problem to utilize surviving local redundancy nodes, in particular in the extreme case where r + 1 nodes in a single local group fail while all other nodes survive.

    3. highlights - more detailed
        1. PMDS - Partial MDS is first an Maximally Recoverable LRC. But
            1. Locally MSR PDMS construction. Field size exponential by parity count as power. 
                1. The construction based on [33] is O(max{rn, u+1}^(n-r)), which is practical
                    1. Note, there are different constructions, See Table II field size comparison for each B, C, D construction
                2. Definition 5: Locally (h, d)-MSR PMDS array codes
                3. Subpacketization is b^n, exponential to code length, b=d+1-(n-r), see Construction 1. It's first an row-wise MDS code, each row is a PMDS in [15]
            2. Or, Globally MSR PDMS construction. Field size and subpacketization are exponential by code length
                1. Way too large to be feasible
        2. Definition 2 is a math formal way to declare Maximally Recoverable property. It's also the definition of PMDS code.
        3. Definition 3 is a math formal way to declare MSR regenerating code property
        4. Definition 4: Row-wise MDS regenerating code
            1. My questions: Is Clay Code is also a Row-wise MDS regenerating code?
               https://www.usenix.org/sites/default/files/conference/protected-files/fast18_slides_vajha.pdf
                1. Looks like not, it's initially row-wise MDS, but then applied Pairwise Forward Transform (PFT) to couple cross rows
        5. Definition 7: Ye-Barg d-MSR Codes. Which is a row-wise MDS d-MSR code
            1. Paper: "Explicit constructions of high-rate MDS array codes with optimal repair bandwidth"
        6. Definition 8: Gabidulin Codes are used repeatedly in the literature to construct LRCs and PMDS codes, can be seen as matrices in FM×n q by expanding elements of FqM into vectors in FM. It is well-known that the minimum rank distance of a Gabidulin code is n − k + 1
        7. Lemma 1: The paper extends the work of [15]: "Construction of partial MDS and sector-disk codes with two global parity symbols"
            1. The construction in [15] has two global parities. The H parity check matrix in (2) of each parities. H0 for each local parity. H1 to Hu are global parities. All representation are in array code format. The "code locator" is the β^x.
                The trick to prove MR property is by converting the punch matrix back to Vandermonde matrix. And also matrix F(..)
            2. Paper: Construction of Partial MDS and Sector-Disk Codes With Two Global Parity Symbols
                1. SD codes are a weaker form of PMDS code. SD codes tolerate the erasure of any m columns of elements, plus any additional s elements in the array. PMDS codes tolerate a broader class of erasures — any m elements per row may be erased, plus any additional s elements
        
        8. Construction 1: Locally d-MSR PMDS/SD array codes - It's a row-wise MDS code that each row is an PMDS in [15]
            1. Theorem 1: Prove this code is d-MSR. In each row, in each local group H0(a), it's a Ye-Barg Regenerating Codes.
                1. OK .. so the d-MSR PMDS is constructed by 1) in each row, it's an PMDS in [15], 2) and in each row's each local group, it's Ye-Barg Regenerating Codes.
            2. Corollary 2: Calculate field size requirements

        9. Definition 9: See Figure 2, expanding single row MDS to M-row MDS. The single row version (but with a larger field size) is the Universal Partial MDS Code Family.
        10. Construction 2: It makes the trick in Construction 1 generalized. Any PMDS and row-wise (h,d)-MSR code can be combined to make a (h,d)-MSR PMDS code
            1. Theorem 3 proves it. The 2 global parities should be constructed in the same way like before (see formula (5)), it's a trick that makes them always MR
            2. The remaining difficulty in Construction 2 is to find suitable constructions of universal PMDS code familiies
                1. B. Construction 2 using the Gabidulin-Code-Based PMDS Family. See the detailed steps. Global parity count s doesn't need to be 2
                    1. This finds the PMDS part. Then use Ye-Barg MSR codes as the MSR part.
                    2. Corollary 3: For all valid PMDS parameters µ, n, r, s
                2. C. Construction 2 using the Linearized-RS-Codes-Based PMDS Family
                    1. This is even simpler, just use RS code for PMDS, and Ya-Barg for MSR
                    2. My questions: But how to make sure local parity and global parity together satisfy MR property?
                3. D. Construction 2 using the PMDS Family in Gabrys et al.
                    1. See Table II field size comparison for each B, C, D construction
                        1. This is useful

        11. PMDS Global Regeneration
            1. Restriction: "MSR codes with that repair one position (h = 1) from all remaining positions (d = µ(n − r) − 1) of the MDS code"
            2. Construction 3: Globally MSR PMDS array codes
                1. using Gabidulin codes instead of RS codes. and, "performing linearly independent linear combinations of the symbols of a Gabidulin code yields another Gabidulin code with different code locators"
            3. Definition 10: Skew Ye–Barg d-MSR codes
            4. Definition 11: Skew Ye-Barg codes are MSR codes if they have following property: YB-Grouping Property
                1. "Therefore, for repair of node i, node j transmits the set of symbols ..<formula>.."
            6. Theorem 6: "the following theorem gives a sufficient condition on the matrix B for Construction 3 to give a globally-MSR PMDS code"
            7. Definition 12: To construct matrix B, we use slightly stronger property to simplify: scrambled YB grouping property
                1. Theorem 7: Let B be a matrix whose rows are exactly the entries of S, Then B has the scrambled YB grouping property
                2. Corollary 6: Calculate field size and subpacketization level for globally-MSR PMDS
                    1. "The resulting code has a field size in O(n^(µ(n+s))) and subpacketization in O((8n)^(µn(n+s)))"
                        1. This is way too large for practical use

        12. My questions
            1. The paper talked about either local or global is MSR. But is there a codec that both local and global are MSR?
                1. It's an open question. "Finally, for the globally MSR PMDS codes, it remains an open problem to utilize surviving local redundancy nodes, in particular in the extreme case where r + 1 nodes in a single local group fail while all other nodes survive."
```
