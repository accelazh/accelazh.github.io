---
layout: post
title: "Database Query Optimizer Volcano Cascades"
tagline : "Database Query Optimizer Volcano Cascades"
description: "Database Query Optimizer Volcano Cascades"
category: "database"
tags: [database, query-optimizer, search]
---
{% include JB/setup %}

Query optimizer is the database signature technology, and among those most complex and less understood ones. Here I wrote down the key concepts, design paradigm, and how it works, from my recent study. 

  * [Query Optimizer: Volcano/Cascades](https://mp.weixin.qq.com/s?__biz=MzI5Mjk3NDUyNA==&mid=2247483895&idx=1&sn=05b687a465f5e705dbebfdccaf478f4b&chksm=ec787b24db0ff) [PDF](/images/query-optimizer-volcano-cascades.pdf) [WeiChat](/images/query-optimizer-volcano-cascades-weichat.pdf)

Related paper reading

```
1. Access Path Selection in Main-Memory Optimized Data Systems: Should I Scan or Should I Probe?    [2017, 33 refs, CMU 15-721]
   https://www.eecs.harvard.edu/~kester/files/accesspathselection.pdf
    1. interesting paper and very useful modeling. Access Path Selection is a general Query Optimization problem..
       query concurrency should be considered choosing full scan vs B+tree index. Low selectivty is still key to use index (e.g. secondary index)
       the math model is linear (training possible) in a given hardware setup (varying selectivity / query concurrency), and logN/N on total DB data size.
       The math model is evaluated by math analysis, one physical machine + varying workload, and varying hardware setups (AWS VM)
    2. highlights
        1. scope
            1. study on in-memory analytical database read-only queries. column-oriented or column-group (hybrid row-column)
            2. these systems made full scan fast via many techniques (i.e. morden analytical systems)
                1. column-oriented only scan the attribute necessary
                2. vectorized execution passes a block of tuples to each operator, in a tight loop,  reducing interpretation logic overhead
                3. multiple queries can share one scan
                4. column-oriented compress more efficiently, and work directly over compressed data, 
                5. holding each attribute contiguously in a dense array allows tight for loop evaluation
                6. and lends itself well to single instruction multiple data (SIMD) processing, and in parallel across cores
            3. many modern analytical systems opt NOT to include secondary indexing
                1. this paper proved secondary indexing are still useful, compared to always full scan
            4. tradition database system uses a hardcode threshold selectivity to choose between use full scan vs index
                1. this paper proved there is better way
            5. since in-memory, there is limited time to devote to access path selection; optimization time has become the new bottleneck
            opt out secondary indexes
            6.  column-stores, the tuple-reconstruction is a heavy cost component
                1. it needs fetching an attribute/column based on a selection on another attribute
                2. having an unsorted result from a select operator will force a tuple reconstruction operator to operate with random access patterns
        2. access path selection
            1. full scan is more efficient due to below factors
                1. multiple queries sharing the same one scan (i.e. shared query, query concurrency)
                2. high selectivity
                3. Index scan (i.e. B+tree) needs ADDITIONALLY sort the read results by rowID
                    1. so, given low selectivity, but growing data size; we can see (Figure 9)
                        1. first, using index is bad, because there is few data
                        2. next, using index is favorable, because more data now, and index skips data effectively
                        3. last, using index is bad, because the sort cost dominates
                    2. question: is the extra sort really necessary? it affects key paper results?
                4. column-oriented is better than column-group (hybrid), because the latter one involves more data to scan through
        3. formulas. this part is very useful
            1. model of latency if we choose full scan. Formula (5)
                1. the base input is memory scan bandwidth, CPU cost to evaluate predict
                2. sharing query in one scan is key to improve latency performance
            2. model of latency if we choose index. Formula (13)
                1. the base input is memory bandwidth for tree traversal, leaf traversal, cache access/miss latency
                2. Appendix has how share query share sort cost, and how SIMD reduces sort cost
                3. question: why sort is necessary?
                    1. due to tuple-reconstruction, i.e. column-store needs to fetch other attributes in one row
                       with sort by rowID, the access to other attributes avoids random access
                    2. besides, to benefit subsequent operators, i.e. joins and aggregates
                    3. double-think, is the sort by rowID really and always necessary?
                4. question: unlike full scan path, index path didn't overlap time cost for tree traversal and predict evaluation
                    1. full scan path latency by max (scan, predict evalutation) .. this is another reason why index path can be slower
                    2. index path should be able to improve it
                5. B+tree needs to be traversal-ed multiple times if there are multiple query
                    1. leaf traversal does already combine the multiple shared queries
            3. APS score, which is Index path cost / full scan path cost, for Access Path Selection
                1. it is a simple formula, so very lightweight for runtime query optimization
                2. for a single machine, the formula is linear (except for total data size N)
                    1. question: since it's linear, we can forget the formula, and per machine uses a machine learning training process to build path selector
                    2. question: the paper has math fitting and experiment fitting, linear makes it seems must-be-able-to fit
                        1. and the paper introduced extra alpha/beta parameters for the fitting .. making fitting more fitting ..
                        2. anyway, the paper experimented with a physical machine + different workloads, and different hardware setup machines (AWS VMs)
                            1. the fitting results looks pretty well. so the model should be simple but very useful
                            2. the DB to evaluate is FastColumns
                    3. how to obtain the query's selectivity?
                        1. this is the typical query optimizer problem. it can be obtained with runtime statistics (e.g. histograms)
                        2. how other runtime info for query optimizer is collected?
                            1. selectivity & query concurrenct by DB scheduler
                            2. hardware specification collected by Intel's Memory Latency Checker tool
                            3. data size and physical organization is by storage engine
                3. key paper results
                    1. query concurrency needs to be considered when choosing full scan vs index
                    2. though full scan (no secondary index) is popular, index is still favorable usually when
                        1. low selectivity .. selectivity (i.e. sel%) is still the key dominator
                        2. few sharing queries
                        3. column-group size increases towards hybrid layouts
    n. related materials
        1. how to collect selectivity statistics in realtime?
            1. Oracle doc - Query Optimization
               https://docs.oracle.com/cd/B10500_01/appdev.920/a96595/dci08opt.htm

        2. what is cost based optimizer vs rule based optimizer
            1. http://its-all-about-oracle.blogspot.com/2015/03/cost-based-optimizer-vs-rule-based.html
                1. Rule Based Optimizer (RBO) is now obsolete in Oracle 10g
                2. Cost based optimizer takes into statistics and data distribution.
                   Rule-based optimizer may always use index even selectivity is high.
                   This doesn't rule out CBO to use hardcode selectivity value to switch on/off index
                3. CBO has more cost parsing & analyzing query. Cached query helps.
                   Prefer using parameterized query to improve cache hit, especially for Object-Relation mapping frameworks
                4. Database may allow users to explictly require update of selectivty statistics of a table
                   And custom associate functions to calculate selectivity, cost, statistics, or hook into any steps in query optimizer
                5. components in query optimiazation
                    1. Access method: how to access table, using index or full scan or hash table
                    2. Join order: permutations of which table join first
                    3. cost model: the algorithm to calculate the cost of each execution plan
                    4. mentioned in "AnalyticDB: Real-time OLAP Database System at Alibaba Cloud"
                        1. a rich set of relational algebra conversion rules
                            1. basic optimization rules, e.g., cropping, pushdown/merge, deduplication, constant folding/predicate derivation
                            2. probe optimization rules for different Joins, e.g., BroadcastHashJoin, RedistributedHashJoin, NestLoopIndexJoin
                            3. Aggregate, JoinReorder, GroupBy pushdown, Exchange pushdown, Sort
                            4. advanced optimization rules, e.g., Common Table Expression
                        2. sampling-based cardinality estimation framework
                    5. mentioned in "hellocode - Casecades Optimizer"
                       https://zhuanlan.zhihu.com/p/73545345
                        1. very good article. basically covered each key aspects in query optimizer
                        2. query optimizer components
                            1. statistics：维护统计信息，用于代价评估
                            2. cost model：基于统计信息，对具体的执行计划评估代价
                            3. plan enumeration：对可能的执行计划进行搜索，对其代价进行评估，选择最优执行计划
                            4. rules: match and replace, e.g. 谓词下推. E.g. CockroachDB DSL.
                            5. CochroachDB cost-based optimizer steps
                                1. Parse: SQL to AST tree
                                2. OptBuild: AST tree to relational expression tree (i.e. logical operator tree)
                                3. Normalize: apply static rewrite transformations (defined by DSL Optgen) to relational expression tree
                                              can be interleaved with OptBuild step
                                4. Explore: search cheapest query plan, estimate cost.
                                            Using Memo structure to organize expression trees
                                    1. 自底向上 vs. 自顶向下
                                    2. 广度优先搜索与启发式算法
                                5. ExecBuild: convert final expression to format understood by execution engine
                                              optimizer results can be cached
                            6. 此外，很重要的一点是: 实现关系代数的化简和优化，依赖于数据系统的物理性质，如
                               https://io-meter.com/2018/11/01/sql-query-optimization-volcano/
                                储存设备的特性(顺序读性能如何？随机读性能如何？吞吐量如何)
                                储存内容的格式和排列(列式储存？行式储存？是否以某列进行分片？)
                                包含的元数据和预计算结果(是否存在索引？是否存在物化视图？)
                                聚合和计算单元的特性(单线程？并发计算？分布式计算？特殊加速硬件？)
                               - Explains Logical Plan vs Physical Plan
                            7. SORT LIMIT - for Top N cases
                            8. search branch pruning
                                1. cost limit
                                2. use priority queue to order possible branches (children are weighted)
                                   Importance of matching
                            9. https://aaaaaaron.github.io/2020/02/08/Calcite-Volcano-Optimizer-%E9%83%A8%E5%88%86/
                                Logical Algebra 之间的转换使用 Transformation Rule；
                                Logical Algebra 到 Physical Algebra 之间的转换使用 Implementation Rule
                                Physical Property 可以从 Physical Algebra 中提取，表示算子所产生的数的具有的物理属性，比如按照某个 Key 排序、按照某个 Key 分布在集群中等
                            10. Query execution & processing, query scheduling

                6. CockroachDB query optimizer
                    1. How We Built a Cost-Based SQL Optimizer
                       https://www.cockroachlabs.com/blog/building-cost-based-sql-optimizer/
                        1. useful to explain key concepts
                        2. real example
                           https://forum.cockroachlabs.com/t/slow-join-query-performance-problems/2688
                        3. Query Plan Caching in CockroachDB
                           https://www.cockroachlabs.com/blog/query-plan-caching-in-cockroachdb/
                            1. optimization process steps - useful

                7. SQL 查询优化原理与 Volcano Optimizer 介绍
                   https://io-meter.com/2018/11/01/sql-query-optimization-volcano/
                    1. useful. illustrated all key aspects.
                    2. good, more details drilling into Calcite, e.g. Trait/Physical properties vector, explore终止条件
                8. The Volcano/Cascades Optimizer - Eric Fu
                   https://www.slideshare.net/ssuser9ebf46/the-volcanocascades-optimizer
                    1. useful.
                       history papers, operators, rules, properties, physical properties
                       very useful. page 51 step through
                    2. Calcite concepts are referenced in quite a few material
                       this, and https://io-meter.com/2018/11/01/sql-query-optimization-volcano/
                             and https://zhuanlan.zhihu.com/p/73545345
                9. 揭秘 TiDB 新优化器：Cascades Planner 原理解析
                   https://pingcap.com/blog-cn/tidb-cascades-planner/
                    1. good. useful, in-depth, and linked to the good source code drilling of TiDB
                       solved in-depth the puzzle how cascades optimizer compares to volcano optimizer
                    2. 十分钟成为 Contributor 系列 | 为 Cascades Planner 添加优化规则
                       https://pingcap.com/blog-cn/10mins-become-contributor-20191126/
                        1. TiDB version of Optgen like CockroachDB?
                        3. useful. concepts well-written
                        3. "目前所有的 Transformation Rule 的实现代码都放在 planner/cascades/transformation_rules.go 文件中"
                    3. "TiDB 中，一个 SQL 在进入到逻辑优化阶段之前，它的 AST（抽象语法树）已经转换成了对应的逻辑算子树，因此逻辑优化就是将一个逻辑算子树进行逻辑上等价变换的过程。逻辑优化是基于规则的优化（Rule-Based Optimization，RBO），这些规则背后的原理就是关系代数的等价变换，其中典型的规则包括：列剪裁，谓词下推等"
                    4. good useful summary on Volcano Optimizer
                        "Volcano Optimizer Generator 本身的定位是一个优化器的“生成器”，其核心贡献是提供了一个搜索引擎。作者提供了一个数据库查询优化器的基本框架，而数据库实现者要为自己的 Data Model 实现相应的接口后便可以生成一个查询优化器。我们下面抛开生成器的概念，只介绍其在“优化器”方向提出的一些方法：

                        1. Volcano Optimizer 使用两阶段的优化，使用 “Logical Algebra” 来表示各种关系代数算子，而使用 “Physical Algebra” 来表示各种关系代数算子的实现算法。Logical Algebra 之间使用 Transformation 来完成变换，而 Logical Algebra 到 Physical Algebra 之间的转换使用基于代价的（cost-based）选择。

                        2. Volcano Optimizer 中的变化都使用 Rule 来描述。例如 Logical Algebra 之间的变化使用 Transformation Rule；而 Logical Algebra 到 Physical Algebra 之间的转换使用 Implementation Rule。

                        3. Volcano Optimizer 中各个算子、表达式的结果使用 Property 来表示。Logical Propery 可以从 Logical Algebra 中提取，主要包括算子的 Schema、统计信息等；Physical Property 可以从 Physical Algebra 中提取，表示算子所产生的数的具有的物理属性，比如按照某个 Key 排序、按照某个 Key 分布在集群中等。

                        4. Volcano Optimizer 的搜索采用自顶向下的动态规划算法（记忆化搜索）。"
                    5. Cascades Optmizer. good useful compare with "Volcano Optimizer"
                        1. introduced Memo. Expression Group（下文简称 Group） 以及 Group Expression（对应关系代数算子）
                        2. 在 Volcano Optimizer 中，Rule 被分为了 Transformation Rule 和 Implementation Rule 两种 .. 而在 Cascades Optimizer 中，不再对这两类 Rule 做区分。
                        3. introduced Pattern
                            "Pattern 用于描述 Group Expression 的局部特征。每个 Rule 都有自己的 Pattern，只有满足了相应 Pattern 的 Group Expression 才能够应用该 Rule"
                        4. Searching Algorithm
                            1. 每个 Rule 都有 promise 和 condition 两个方法，其中 promise 用来表示 Rule 在当前搜索过程中的重要性，promise 值越高，则该规则越可能有用，当 promise 值小于等于 0 时，这个 Rule 就不会被执行；而 condition 直接通过返回一个布尔值决定一个 Rule 是否可以在当前过程中被应用。当一个 Rule 被成功应用之后，会计算下一步有可能会被应用的 Rule 的集合
                            2. Cascades Optimizer 的搜索算法与 Volcano Optimizer 有所不同，Volcano Optimizer 将搜索分为两个阶段，在第一个阶段枚举所有逻辑等价的 Logical Algebra，而在第二阶段运用动态规划的方法自顶向下地搜索代价最小的 Physical Algebra。Cascades Optimizer 则将这两个阶段融合在一起，通过提供一个 Guidance 来指导 Rule 的执行顺序，在枚举逻辑等价算子的同时也进行物理算子的生成，这样做可以避免枚举所有的逻辑执行计划，但是其弊端就是错误的 Guidance 会导致搜索在局部收敛，因而搜索不到最优的执行计划。
                            3. Volcano/Cascades Optimzier 都使用了 Branch-And-Bound 的方法对搜索空间进行剪枝。由于两者都采用了自顶向下的搜索，在搜索的过程中可以为算子设置其 Cost Upper Bound
                    6. interesting
                        1. "为 TiDB 的优化器能力分级，不同复杂程度的查询可以选用不同的优化等级。"
                    7. good useful, the optimizer algorithm of TiDB is in-detail and well-written. see the original article
                        1. Preprocessing phase，预处理阶段。
                        2. Exploration phase，逻辑搜索阶段。
                        3. Implementation phase，物理实现阶段

                10. The SQL Server Query Optimizer (2011) - Benjamin Nevarez
                    https://www.red-gate.com/simple-talk/sql/performance/the-sql-server-query-optimizer/
                    1. author of book "Inside the SQL Server Query Optimizer"
                    2. highlights
                        1. Hinting, user pass to direct optimizer use particular index/join algorithm 
                        2. Ongoing Query Optimizer Challenges
                            1. combinatorial explosion
                            2. accurate cost and cardinality estimation

            2. https://logicalread.com/reading-oracle-explain-plans-part-2-h01/#.YDTwUugzabg
            3. https://nirajrules.wordpress.com/2009/06/10/cost-based-optimization-cbo-vs-rule-based-optimization-rbo/
            4. SQL Server Query Optimization
               https://slidesplayer.com/slide/14265704/

        3. what is cascade query optimizer vs volcano query optimizer?
            1. hellocode - Cascades Optimizer
               https://zhuanlan.zhihu.com/p/73545345
                1. PostgreSQL自底向上 -> 局限. then
                   自顶向下-Cascades. Cascades继承Volcano Optimizer Generator，跳过Volcano来看Cascades
                2. 在工业界，Peleton、Orca、SQL Server、Calcite、Cockroach等都算是Cascades的实现
            2. Volcano and Cascades optimizers are basically replaciable namings to each other
               see, https://www.slideshare.net/ssuser9ebf46/the-volcanocascades-optimizer
                    https://io-meter.com/2018/11/01/sql-query-optimization-volcano/
                    https://zhuanlan.zhihu.com/p/73545345
               Cascades inherits and improves from Volcano. Nowadays it's almost all Cascades
            3. Calcite - Volcano Optimizer 部分
               https://aaaaaaron.github.io/2020/02/08/Calcite-Volcano-Optimizer-%E9%83%A8%E5%88%86/
                1. useful
                2. "Volcano Optimizer 将搜索分为两个阶段，在第一个阶段枚举所有逻辑等价的 Logical Algebra，而在第二阶段运用动态规划的方法自顶向下地搜索代价最小的 Physical Algebra
                    Cascades Optimizer 则将这两个阶段融合在一起，通过提供一个 Guidance 来指导 Rule 的执行顺序，在枚举逻辑等价算子的同时也进行物理算子的生成，这样做可以避免枚举所有的逻辑执行计划"
                2. The database redbook
                   http://www.redbook.io/ch7-queryoptimization.html
                    1. two architectures of query optimizer
                        1. System R optimizer
                        2. Goetz Graefe etc refined and summarized Volcano architecture
                           then Goetz Graefe etc again proposed Cascades architecture
                        3. Cascades is the latest and standard approach, addressed a number of detailed deficiencies in Volcano
                            1. two opensource projects: Orca and Calcite
                    2. 'This "top-down" vs "bottom-up" debate for query optimization has advocates on both sides, but no clear winner'
            4. The Volcano Optimizer Generator
               https://www.dazhuanlan.com/2019/12/05/5de8689665130
               original: https://nan01ab.github.io/2018/05/Valcano.html
                1. useful. in detail, in depth, good summary
                2. a summary by the article of what to implement
                    (1) a set of logical operators, 
                    (2) algebraic transformation rules, possibly with condition code, 
                    (3) a set of algorithms and enforcers, 
                    (4) implementation rules, possibly with condition code, 
                    (5) an ADT "cost" with functions for basic arithmetic and comparison, 
                    (6) an ADT "logical properties," 
                    (7) an ADT "physical property vector" including comparisons functions (equality and cover), 
                    (8) an applicability function for each algorithm and enforcer, 
                    (9) a cost function for each algorithm and enforcer, 
                    (10) a property function for each operator, algorithm, and enf
                3. pseudo code of FindBestPlan
                    ---
                    FindBestPlan (LogExpr, PhysProp, Limit)
                      // 记忆化优化
                      if the pair LogExpr and PhysProp is in the look-up table
                        if the cost in the look-up table < Limit return Plan and Cost
                      else
                        return failure
                      /* else: optimization required */
                      create the set of possible "moves" from
                        applicable transformations
                        algorithms that give the required PhysProp enforcers for required PhysProp
                        order the set of moves by promise 
                      for the most promising moves
                        if the move uses a transformation
                          // 转化为新的表达式，递归调用
                          apply the transformation creating NewLogExpr 
                          call FindBestPlan (NewLogExpr, PhysProp, Limit)
                        else if the move uses an algorithm 
                          TotalCost := cost of the algorithm
                          for each input I while TotalCost <= Limit
                            determine required physical properties PP for I 
                            Cost = FindBestPlan (I, PP, Limit - TotalCost) 
                            add Cost to TotalCost
                        else/* move uses an enforcer */
                          TotalCost := cost of the enforcer
                          // 通过enforcer来改变PhysProp，拓展可以使用的算法
                          modify PhysProp for enforced property
                          call FindBestPlan for LogExpr with new PhysProp
                      /* maintain the look-up table of explored facts */ 
                      if LogExpr is not in the look-up table
                        insert LogExpr into the look-up table
                      insert PhysProp and best plan found into look-up table 
                      return best Plan and Cost
                    ---
                4. "0x03 和EXODUS的区别
                        EXODUS是同一个作者在Volcano的一个优化器设计的版本，Volcano也是在EXODUS的基础之上优化而来。这里总结了一些Volvano在EXODUS上面的做的一些优化： 前者(EXODUS)没有区分逻辑表达式和物理表达式，也没有物理Properties的概念，没有一个通用的Cost函数等等。
                    0x04 The Cascades Framework for Query Optimization
                        Cascades是Volcano的一个优化设计的版本。在Cascades中，基于面向对象的设计。[3]这篇Paper是一个很抽象的描述，没有什么有意思的图。[4]这篇Thesis是一个Cascases风格的优化器的一个实现，更加具体一些。"
                    1. The Cascades Framework for Query Optimization, 1995.
                       Yongwen Xu, Efficiency in Columbia Database Query Optimizer, M.S. Thesis, Portland State University, 1998.
            5. Database Redbook - Chapter 7 Query Optimization
               http://www.redbook.io/ch7-queryoptimization.html
                    1. good. the text is short, but it is very more insightful than many other materials
                    2. highlights
                        1. Progressive Optimization
                            1. When executing, collect the statistics from real input, and reoptimize the query
                            2. adaptive for long running queries
                        2. Eddies
                            1. For query on continuous stream. Merge query optimizing and executing.
                               The operator can watch the stream, executing, collect statistics, and dynamically re-optimize
                            2 dataflow architectures, dataflow operators
            6. See 揭秘 TiDB 新优化器：Cascades Planner 原理解析 for good in-depth compare
               https://pingcap.com/blog-cn/tidb-cascades-planner/

        4. what is logical execution plan vs physical execution plan?
            1. SQL 查询优化原理与 Volcano Optimizer 介绍
               https://io-meter.com/2018/11/01/sql-query-optimization-volcano/
                1. "在最初的 Volcano Optimizer 论文中，算法存在逻辑优化和物理优化两个步骤， 在前者中会尽量将所有逻辑算子变换和展开。这一做法在后续的 Cascades 论文以及 Calcite 的实现中并没有体现。后两者当中，逻辑变换的规则和物理变换的规则没有本质的差别， 两者会在一轮优化当中同时使用，以期待快速从逻辑表示转换为物理执行方案。"
            2. https://pingcap.com/blog-cn/10mins-become-contributor-20191126/
                1. "业界设计出了 System R 优化器框架来处理越来越多的复杂 SQL 查询。它将查询优化分为逻辑优化和物理优化两个阶段，逻辑优化根据规则对执行计划做等价变形，物理优化则根据统计信息和代价计算将逻辑执行计划转化为能更快执行的物理计划。目前 TiDB 优化器采用的也是该优化器模型"
                2. https://www.dazhuanlan.com/2019/12/05/5de8689665130
                    1. "Group是Cascades中一个基本的概念，表示等效的逻辑和物理表达式的集合。在前面的Volcano中，优化的过程可以被分为两个阶段，一个是使用转化规则将给定的查询转化为所有可能的逻辑表达式，第二步是优化得到实际的执行计划。Volcano这样的做的缺点就是可以导致很多无用的搜索，因而Cascades中放弃这样的做法。Cascases中一个组只用在需要的时候才会应用转换规则"
                    2. I.e. Cascade should have merged logical plan and physical plan to reduce unnecessary transforms
                3. http://www.redbook.io/ch7-queryoptimization.html
                    1. "MySQL was the open source de facto reference for “database technology” for the preceding decade, with a naive heuristic optimizer" .. not even cost-based optimizer?

        5. how to test a query optimizer?
            1. 如何测试数据库查询优化器
               https://zhuanlan.zhihu.com/p/142982206
                1. OptMark: A Toolkit for Benchmarking Query Optimizers
                    1. Effectiveness: 优化器对于某条 Query 生成的 plan 的质量
                        1. random enumeration of plan space to compare.
                           the enumeration size is bound by reaching confidency % and accuracy %
                    2. Efficiency: Efficiency 则是衡量生成的 plan 的资源消耗

        6. relational algebra
            1. CockroachDB OptGen reflects possible transforms
                1. doc: https://github.com/cockroachdb/cockroach/blob/master/pkg/sql/opt/optgen/lang/doc.go
                2. transform definition: https://github.com/cockroachdb/cockroach/tree/master/pkg/sql/opt/norm/rules
            2. TiDB doc of relational algreba transforms
                https://pingcap.com/blog-cn/tidb-source-code-reading-7/
                https://pingcap.com/blog-cn/tidb-source-code-reading-21/
            3. Wikipedia Relational_algebra
               https://en.wikipedia.org/wiki/Relational_algebra
                1. as far, CockrochDB/TiDB transforms are still a useful place to learn
                2. Selectivity estimation

        7. collecting selectivity statistics
            1. Oracle doc: intro concepts
               https://docs.oracle.com/cd/B10500_01/appdev.920/a96595/dci08opt.htm
                1. online, and offline user-triggered "SQL ANALYZE"
            2. SITs: Exploiting Statistics on Query Expressions for Optimization     [2002, 171 refs, SQL Server 2000]
               https://www.seas.upenn.edu/~zives/03s/cis650/p263-bruno.pdf
                1. background: Cardinality Estimation using Histograms
                    1. bucket: range => frequency, distinct value count
                    2. base (non-true) assumption:
                        1. attribute distribution are independent
                           (so that seletivity of composed filters can be calculated via multiply)
                            1. Exponential BackOff [3] in SQL Server, to deal with AVI underestimates
                        2. buckets can be split into smaller ones, to align with query needs
                           (assuming value distribution are uniform?)
                        3. handling join expressions ..
            3. Selectivity Estimation for Range Predicates using Lightweight Models    [2019, 31 refs]
               http://www.vldb.org/pvldb/vol12/p1044-dutt.pdf
                1. neural networks and tree-based ensembles for selectivity estimation?
                2. The main method is using histogram, and ssuming AVI (attribute value independence)
                    1. some sampling also captures attribute correlations well
                       multi-dimensional histograms, random samples
                3. selectivity collection involves offline phases, also during query exectuion
                    1. A pay-as-you-go framework for query execution feedback [14]    [2008, 45 refs, SQL Server]
                       https://www.microsoft.com/en-us/research/publication/a-pay-as-you-go-framework-for-query-execution-feedback/
                        1. prior arts
                            1. passive monitoring: physical operators counting tuple outputs, i.e. feedback, store in feedback cache
                    2. proposing: proactive monitoring, a pay-as-you-go framework
            4. Synopses for Massive Data: Samples, Histograms, Wavelets, Sketches    [2012, 437 refs]
               https://dsf.berkeley.edu/cs286/papers/synopses-fntdb2012.pdf
                1. useful. covers typical methods: synopses: random samples, histograms, wavelets, and sketches
                    1. seems not dedicated for database selectivity / query optimization area
                    2. DBMS mainly uses histogram
                    3. Sketches can estimate COUNT DISTINCT queries
            5. Selectivity Estimation Without the Attribute Value Independence Assumption      [1997, 630 refs]
               http://www.vldb.org/conf/1997/P486.PDF
                1. approximate (multi-dimensional) joint data distributions
                    (a) Using a multi-dimensional histogram
                    (b) Using the Singular Value Decomposition (SVD) technique
                2. "joint data distribution" / multi-dimension histogram for query involving >=2 attributes
                    1. represented as a two or multi-dimensional matrix, each cell for a count/frequency value
                    2. the main problems turns into how to reduce multi-dimensional matrix size, how to approximate if with single-dimension histograms
                    3. MHIST: Multi-Dimensional Histograms technique
                       Hilbert-numbering method
                       SVD decomposition
            6. Selectivity Estimation using Probabilistic Models    [2001, 287 refs]
               http://robotics.stanford.edu/~btaskar/pubs/sigmod01.pdf
                1. common but inaccurate assumptions
                    1. AVI: attribute value independence
                    2. join uniformity
                        1. [23, 25] based on singular value decomposition
                        2. [21, 27, 6] new approaches using use of wavelets
                        3. randomly sample the two tables, and compute their join
                2. this paper's approach: probabilistic graphical models
                    1. Bayesian networks (BNs) [24] can be used to represent the interactions between attributes
                    2. PRM based algorithm
            7. An overview of methods for treating selectivity in big data sources   [2018, 13 refs]
               https://ec.europa.eu/eurostat/documents/3888793/9053568/KS-TC-18-004-EN-N.pdf/52940f9e-8e60-4bd6-a1fb-78dc80561943
                1. not related, not in database query optimizer area. "selectivity" means something else
            8. enterprise products
                1. Understanding Optimizer Statistics With Oracle Database 18c
                   https://www.oracle.com/technetwork/database/bi-datawarehousing/twp-stats-concepts-0218-4403739.pdf
                    1. periodical gather or refresh statistics, especially when data is highly volatile
                    n. related
                        1. Oracle 9i: Gathering Optimizer Statistics
                           https://docs.oracle.com/cd/A91202_01/901_doc/server.901/a87503/stats.htm
                        2. Oracle Dev: Using Extensible Optimize
                           https://docs.oracle.com/cd/B28359_01/appdev.111/b28425/ext_optimizer.htm
                            1. User-Defined Selectivity. system statistics may not work well with user-defined operators and predict containing funtions
                2. SQL Server statistics
                   https://docs.microsoft.com/en-us/sql/relational-databases/statistics/statistics?view=sql-server-2017
                    1. highlights
                        1. "Statistics objects on multiple columns also store statistical information about the correlation of values among the columns"
                        2. "Aggregates the column values into a maximum of 200 contiguous histogram steps"
                        3. sampled values can also be combinedly shown on Histogram
                        4. Filtered Statistics
                        5. AUTO_UPDATE_STATISTICS, AUTO_UPDATE_STATISTICS_ASYNC options
                            1. so .. the statistics are basically periodically gather/refreshed
                        6. Query Predicate contains multiple correlated columns
                            1. "Statistics on multiple columns contain cross-column correlation statistics, called densities"
                            2. "If the columns are not already in the same index, you can create multicolumn statistics by creating an index on the columns or by using the CREATE STATISTICS statement"
                    2. Cardinality Estimation for Correlated Columns in SQL Server 2016
                       https://docs.microsoft.com/en-us/archive/blogs/sql_server_team/cardinality-estimation-for-correlated-columns-in-sql-server-2016
                        1. Exponential Backoff method.
                4. PostgreSQL: Row Estimation Examp
                   https://www.postgresql.org/docs/current/row-estimation-examples.html
                    1. split a histogram bucket, is by assuming the values are in a linear distribution in each bucket
                        1. selectivity = (1 + (1000 - 993)/(1997 - 993))/10
                    2. Multivariate Statistics Examples
                       https://www.postgresql.org/docs/current/multivariate-statistics-examples.html
                        1. "fixed by creating a statistics object that directs ANALYZE to calculate functional-dependency multivariate statistics on the two columns"
                            1. so .. typical multi-column selectivity issue is solved by user explicitly creating a multi-column statistics object
                        2. MCV Lists - most common list
                    3. Planner Statistics and Security
                       https://www.postgresql.org/docs/current/planner-stats-security.html
                        1. Access to the table pg_statistic is restricted to superusers
                5. TiDB 源码阅读系列文章（十二）统计信息
                   https://pingcap.com/blog-cn/tidb-source-code-reading-12/
                   https://pingcap.com/blog-cn/tidb-source-code-reading-14/
                    1. very useful. good. well-written.
                    1. highlights
                        1. "等深直方图", Count-Min Sketch (for 等值查询)
                        2. 统计信息创建
                            1. 执行 analyze 语句, 下法请求到Region
                            2. 统计信息维护
                                1. 动态更新机制，根据查询的结果去动态调整统计信息
                                2. 如果最终估计的结果为 E，实际的结果为 R，adjust 桶高h = h * (R / E)
                                3. 桶边界更新：分裂与合并。更频繁查询的桶。使查询边界与桶边界靠近。
                                4. "为了不去假设所有桶贡献的误差都是均匀的，需要收集每一个桶的反馈信息"
                            3. 多列查询
                                1. Assume 不同列之间是相互独立的，因此我们只需要把不同列之间的过滤率乘起来
                                2. 如果有(a, b, c) 的索引，则(a = 1 and b = 1 and c < 5)可有配套的直方图
                                3. "Selectivity 的一个最重要的任务就是将所有的查询条件分成尽量少的组，使得每一组中的条件都可以用某一列或者某一索引上的统计信息进行估计，这样我们就可以做尽量少的独立性假设"
                6. Automatic Table Statistics in CockroachDB
                   https://www.cockroachlabs.com/blog/automatic-sql-statistics/
                    1. How CockroachDB Collects Table Statistics
                        1. CREATE STATISTICS performs a distributed, full table scan of the specified table
                        2. needed to refresh stats periodically
                            1. Automatic Statistics Collection
                            2. Deciding to Trigger a Refresh
                                1. P(refresh) = number of rows changed / (total row count * 0.20)
                    2. RFC: cockroach/docs/RFCS/20170908_sql_optimizer_statistics.md
                       https://github.com/cockroachdb/cockroach/blob/master/docs/RFCS/20170908_sql_optimizer_statistics.md
                        1. Sketch: HyperLogLog to estimate number of distinct values
                        2. this is the detailed design doc
                    3. CockroachDB's Query Optimizer (Rebecca Taft, Cockroach Labs)
                       https://www.youtube.com/watch?v=wHo-VtzTHx0

        8. query exectuion
            1. OLAP 任务的并发执行与调度 - IO Meter
               https://io-meter.com/2020/01/04/olap-distributed/
                1. Very useful article to summarize typical query exectuion
                2. highlights
                    1. MonetDB/X100: Hyper-Pipelining Query Execution
                       https://io-meter.com/2020/01/04/olap-distributed/
                        1. call-execute-return overhead per record.
                           using vectorization & SIMD to amortize
                        2. 算子内部并行和算子间并行
                            1. opertor on partitions introduces shuffle problem
                               EXCHANGE operator implements shuffle transparently to operators
                        3. Pipeline（处理管线）
                            1. Operator Fusion来合并算子
                            2. Plus query code compilation
                        4. data balancing / scheduling
                            1. 数据倾斜, 处理速度倾斜, Data Locality
                            2. Hyper: Morsel-Driven Parallelism: A NUMA-Aware Query Evaluation Framework for the Many-Core Age
                                1. 使用 Pipeline 技术组合算子
                                2. 使用自底向上的 Push 模型调度任务。
                                3. 既使用水平数据分区，也使用垂直数据分区，每个数据块的单位被称为 Morsel。一个Morsel 大约包含10000行数据。
                                4. NUMA-aware，一个内核上执行的任务，其产出结果都储存在当前内核的 Cache 或 Memory 里
                                    1. task "Affinity" to procesor
                                5. 使用 Work-stealing 实现弹性伸缩和任务负载均衡
                                6. 使用 Delay Scheduling 防止过于频繁的 Work stealing。
                                    1. 在内核空闲并可以偷取任务时，调度器并非立即满足空闲内核的要求，而是让它稍稍等待一段时间。在这段时间里，也许忙碌内核就可以完成自己的任务，而跨内核调度任务就可以被避免。
                                    2. 令人惊讶的是，这种简单的处理方式在实际应用中效果非常好。
                                    3. Delay Scheduling: A Simple Technique for Achieving Locality and Fairness in Cluster Scheduling
                            3. SAP HANA watchdog method to monitor & balance tasks scheduling
                                1. Adaptive NUMA-aware data placement and task scheduling for analytical workloads in main-memory column-stores
                            4. HyPer: RDMA network seen as NUMA, shuffle to broadcast, local Multiplexer
                                1. High-Speed Query Processing over High-Speed Networks
                            5. 慢任务异地重试机制
                                1. The tail at scale


        2. "Zonemaps" are commonly found in analytical systems
            1. oracle: Using Zone Maps
               https://docs.oracle.com/database/121/DWHSG/zone_maps.htm#DWHSG9358
                1. it's like a filter, it stores the min-max value of a disk unit. so that during scan the unit can be skipped by predict.

        3. Implications of Certain Assumptions in Database Performance Evaluation    [1984, 330 refs]
            1. referenced as "The problem of choosing the wrong access path and error propagation"
            // TODO
        4. The Vertica Query Optimizer: The Case for Specialized Query Optimizers    [2014, 7 refs]
           https://www.researchgate.net/profile/Nga-Tran-23/publication/269306314_The_Vertica_Query_Optimizer_The_case_for_specialized_query_optimizers/links/55aeb17208aed9b7dcdda55f/The-Vertica-Query-Optimizer-The-case-for-specialized-query-optimizers.pdf
            1. referenced as "cost-based optimization based on statistics used for select and join ordering"
            2. highligths
                1. from C-Store
                2. Figure 8 Join Order Enumeration process
        5.  An Efficient Cost-Driven Index Selection Tool for Microsoft SQL Server    [1997, 504 refs]
            1. referenced as "physical design tools use optimizers during offline analysis"
            // TODO
        6. Shared Workload Optimization    [2014, 48 refs]
            1. referenced as "work sharing across multiple queries .. sharing data movement also been considered"
            // TODO
        7. MonetDB: Two Decades of Research in Column-oriented Database Architectures    [2012, 358 refs]
           https://scholar.harvard.edu/files/MonetDebull2012.pdf
            1. multiple times referenced in above paper
            2. highlights
                1. speedup, first a few column-stores, BAT (Binary Association Table)
                2. the fine-grained flexible intermediate result caching technique “recycling” [12] 
                3. the adaptive incremental indexing technique “database cracking” [8]
                4. Research
                    1. good useful. This area lists many key technologies
        8. Smooth Scan: Statistics-Oblivious Access Paths    [2015, 21 refs]
            1. referenced as "has only been studied in row-stores .. delay access path decisions or provide hybrid access paths"
            // TODO
        9. A Comprehensive Study of Main-memory Partitioning and its Application to Large-scale Comparison- and Radix-sort    [2014, 87 refs]
           http://www.cs.columbia.edu/~orestis/sigmod14I.pdf
           http://www.cs.columbia.edu/~orestis/sigmod14Islides.pdf
            1. referenced as to show how SIMD can reduce sort cost
            2. highligths
                1. Categories of partitioning
                    Types of partitioning: Hash / radix / range
                    Memory usage: Non-in-place / in-place
                    Parallelization model: Shared / shared-nothing
                    Memory hierarchy layer: In-cache / out-of-cache / out-of-CPU
                    NUMA awareness: NUMA aware / NUMA oblivious

2. The Volcano Optimizer Generator: Extensibility and Efficient Search    [1993, 588 refs, Goetz Graefe]
   https://cs.uwaterloo.ca/~david/cs848/volcano.pdf
    1. The fundation paper proposed modern query optimizer. The next paper is Cascades from the same author.
       most features already covered in newer review articles, e.g.
         https://pingcap.com/blog-cn/tidb-cascades-planner/
         https://io-meter.com/2018/11/01/sql-query-optimization-volcano/
         https://zhuanlan.zhihu.com/p/73545345
    2. highlights
        1. Cascades are proposed after Volcano. But in recent literatures they can be used in place of each other, e.g.
             "An overview of query optimization in relational systems"
        2. Volcano makes query optimizer a modular and extensible architecture
        3. SQL text is first parsed into AST,
           converted into logical operator tree,
           then rewrite transform leveraging relation algreba (normalize)
           next use dynamica programming to search with optimal logical plan
            cost based, with pruning by cost cap
           next search for physical plan.
            Logical/Physical property limits allowed plans, e.g. sort by which key
            search priority is defined with "interesting"
        4. partial search results, of subquery trees, can be cached for reuse
        5. the paper provides "pseudo code of FindBestPlan". useful, see Figure 2.
        6. former works are System R, EXODUS, Starburst.

    n. related materials 
        1. The Cascades Framework for Query Optimization  (1995, 371 refs, Goetz Graefe)
           https://www.cse.iitb.ac.in/infolab/Data/Courses/CS632/Papers/Cascades-graefe.pdf
            1. This paper proposed Cascades. most key concepts already covered in Volcano paper
            2. the key difference from Cascades to Volcano are
                1. proposed Memo structure
                    1. exploit equivalent expressions groups
                2. Logical plan and physical plan are not separated in serach, unlike Volcano
                    1. why? "The first phase in Volcano must still be exhaustive"
                3. some new concepts/renaming
                    1. rules, patterns, promising

        2. An overview of query optimization in relational systems [1998, 896 refs, Microsoft]
           https://15721.courses.cs.cmu.edu/spring2020/papers/19-optimizer1/chaudhuri-pods1998.pdf
            1. useful summary to review history of volcano/cascades and key sql problems facing
            2. Highlights
                1. System-R: the use of cost-based optimization, dynamic programming and interesting orders strongly influenced subsequent developments in optimization
                2. linear join sequences and bushy join
                3. join/group-by commuting,
                   merge multi-block query into single block,
                   using semijoin like techniques for optimizing multi-block query
                4. statistics and cost estimation
                    1. given an operator and the statistics summary for each of its input data, determine the
                        1) statistics summary of the output data stream
                        2) estimate cost of executing the operation
                    2. statistical summary is a logical property but the cost of a plan is a physical property
                5. capture correlations among columns
                    1. joint distibution, 2-dimensional histograms
                    2. only summary info such as the number of distinct paris of values used
                    3. only use the selectivity of the most selective predict
                    4. the histogram may be "joined"
                5. volcano/cascades use dynamic programming in a top-down way
                    1. question: so current main stream is top-down search?
                6. open problems
                    1. cost model for UDF (user-defined function) is still open problem 
                    2. cost model for ADT
                    3. optimizer for object-oriented systems

        3. Query Evaluation Techniques for Large Databases    [1993, 1909 refs, Goetz Graefe]
           https://cgi.cse.unsw.edu.au/~cs9315/20T1/readings/query.pdf
            1. Runtime Filter: upon join, passes runtime built filter from one join pair to another, to reduce needed network transmition
                1. 查询性能优化之 Runtime Filter: https://zhuanlan.zhihu.com/p/354754979
                2. Runtime Filtering for Impala Queries: https://impala.apache.org/docs/build/html/topics/impala_runtime_filtering.html
                    1. in detail. Runtime Filter is a bit like broadcasting the join pair, but this time only filters, e.g. min-max filter.

        4. Database Redbook - Chapter 7 Query Optimization
           http://www.redbook.io/ch7-queryoptimization.html
            1. good. the text is short, but it is very more insightful than many other materials
            2. highlights
                1. Progressive Optimization
                    1. When executing, collect the statistics from real input, and reoptimize the query
                    2. adaptive for long running queries
                2. Eddies
                    1. For query on continuous stream. Merge query optimizing and executing.
                       The operator can watch the stream, executing, collect statistics, and dynamically re-optimize
                    2 dataflow architectures, dataflow operators

        5. How to Architect a Query Compiler    [2016, 59 refs, SIGMOD]
           https://15721.courses.cs.cmu.edu/spring2018/papers/03-compilation/shaikhha-sigmod2016.pdf
           https://io-meter.com/2020/02/24/how-to-architect-a-query-compiler/
            1. Query Compilation area rather than Query optimizer above
               logged before. "DSL 堆栈", Io-Meter blog is useful as a summary.
            n. related
                1. How to Architect a Query Compiler, revisted     [2018, 44 refs]
                   https://www.cs.purdue.edu/homes/rompf/papers/tahboub-sigmod18.pdf
                    1. Futamura Projections. System R, Volcano/Cacades are moving to query interpretation path.
                       however, query compilation is another way to build query optimizer
                    2. highlights
                        1. see Figure 1 to compare query interpretation vs compilation.
                        2. query compiler can be derived from query interpreters, to make the query compiler easier to build
                        3. useful Figure 12 to show the evolution of query compilation papers
                    n. related
                        1. fxjwind: How to Architect a Query Compiler
                           https://www.cnblogs.com/fxjwind/p/12560697.html
                            1. useful to understand paper
                        2. CMU 15-721 Query Compilation & Code Generation slides
                           https://15721.courses.cs.cmu.edu/spring2020/slides/14-compilation.pdf
                           // TODO

3. EFFICIENCY IN THE COLUMBIA DATABASE QUERY OPTIMIZER - Cascades Optimizer [1998, 14 refs]
   https://15721.courses.cs.cmu.edu/spring2018/papers/15-optimizer1/xu-columbia-thesis1998.pdf
   http://web.cecs.pdx.edu/~len/Columbia/
    1. very useful material to learn the implementation aspects of a query optimizer
       and to learn query optimizer concepts and history
       COLUMBIA improves from Cascades by many performance optimizations
    2. highlights
        1. key advantages from Cascades - abstraction
            1. the optimizer is designed as object-oriented
               rules, transforms, costs, operators, etc, can be implemented by deriving from the abstract class interface. extensible
            2. search algorithm is organized as tasks and scheduling
               promises, properties filters search branhes
               pattern binding and rules guides transforms to generate more search branches
        2. some architecture tips from Columbia
            1. a hash-based way to rule out duplicated expressions searched
            2. the new concept of expression group, widely useful
            3. succinct data structures in Columbia to save memory
            4. lower bound pruning, global epsilon pruning
        3. good part - the algorithm charts of each part of the query optimizer
            1. O_GROUP, E_GROUP, O_EXPR, APPLY_RULE< O_INPUTS
            2. very useful to understand the details of a query optimizer

4. Apache Calcite: A Foundational Framework for Optimized Query Processing Over Heterogeneous Data    [2018, 61 refs]
   https://arxiv.org/abs/1802.10233
    1. good paper, covers many key aspects of a query optimizer, and especially query different data sources and data types
       query different data sources, e.g. Hive, Cassandra, MongoDB. query differnet data types, e.g. JSON, Geo, ARRAY/MAP/SET, streams. Integrated with tons of open-source systems
       Calcite can even SQL query a directory of CSV files
    2. hightlights
        1. key features
            1. Calcite was quickly adopted by Hive, Drill [13], Storm
            2. Calcite enables cross-platform optimization, e.g., make decisions across different systems about materialized view selection
            3. Calcite provides support for query optimization and query languages using both streaming and conventional data processing paradigms
                1. Calcite treats streams as time-ordered sets of records or events
                2. and also semi-structured data e.g. JSON.
                    1. also adapter for MongoDB, JSON documents
                3. columns can be of type ARRAY, MAP, or MULTISET
                4. a set of streaming-specific extensions to standard SQL
                5. Geospatial support is preliminary in Calcite
                   It is expected that Calcite will be fully compliant with the OpenGIS Simple Feature Access [39]
                6. Calcite provides Language-Integrated Query for Java (or LINQ4J, in short)
            4. Calcite query optimizer architecture uses dynamic programming-based planning based on Volcano [20] with extensions for multi-stage optimizations as in Orca [45]
        2. key designs
            1. for stream processing, Calcite introduces a window operator that encapsulates the window definition
            2. Concept Traits instead of Physical operator.
               Relational operators can implement a converter interface that indicates how to convert traits of an expression from one value to another
            3. convention trait
                1. he trait represents the data processing system where the expression will be executed
                2. allows Calcite to meet its goal of optimizing transparently queries whose execution might span over different engines
                3. e.g. joining a Products table held in MySQL to an Orders table held in Splunk (see Figure 2)
            4. adaptor and adaptor convention
                1. Figure 3. Using adaptor to parse JSON as a table
            5. query optimization algorithm
                1. Calcite optimizes queries by repeatedly applying planner rules to a relational expression, A cost model guides the process
                2. a rule matches a given pattern in the tree and executes a transformation that preserves semantics of that expression
                    1. Calcite includes several hundred optimization rules
                3. push down query optimization to underlying data processing systems
                    1. e.g. push down Sort into Cassandra, LogicalSort/Filter => CassandraSort/Filter
                4. metadata providers
                    1. provide cost of executing a subexpression, the number of rows and the data size of the results 
                    2. the maximum degree of parallelism with which it can be executed
                    3. Calcite provides interfaces that allow data processing systems to plug their metadata information into the frameworks
                        1. or just enough to provide statistics about their input data, Calcite will do the rest
                        2. As the metadata providers are pluggable, they are compiled and instantiated at runtime using Janino [27], a Java lightweight compiler
                    4. cost-based planner engine: search algorithm is based on volcano
                        1. expression is registered with the planner, together with a digest based on attributes and its inputs. digest detects duplicates
                        2. the process stops when
                            1. exhaustively explore the search space
                            2. or, use a heuristicbased approach to stop the search when the plan cost has not improved by more than a given threshold 
                        3. The default cost function implementation combines estimations for CPU, IO, and memory resources
                        4. an alternative exhaustive planner
                            1. user may switch based on needs, and investigate and provide guides to optimzer
                            2. Multi-Stage Optimization (from Orca)
                                1. user can specify different terminate policies at different stages
                                2. the most expensive transformation rules can be configured to run in later stages to avoid increasing the optimization time
                    5. Materialized views: rewrite incoming queries to use views
                        1. view substitution: substitute part of the relational algebra tree with an equivalent expression which makes use of a materialized view
                        2. lattices: represents each of the materializations as a tile which in turn can be used by the optimizer to answer incoming queries
                            1. the rewriting algorithm is especially efficient in matching expressions over data sources organized in a star schema, which are common in OLAP applications
                            2. On the other hand, it is more restrictive than view substitution, as it imposes restrictions on the underlying schema

5. Orca: A Modular Query Optimizer Architecture for Big Data    [2014, 63 refs]
   https://15721.courses.cs.cmu.edu/spring2016/papers/p337-soliman.pdf
    1. Query optimizer used in Pivotal Greenplum and HAWQ, optimized for OLAP
       very good paper. covers full parts of query optimizer, well-explained, and with new improvements
    2. highlights
        1. key features
            1. the paper says existing commercial and opensource systems are still primarily based on technology dating back to early days,
            while Orca using state-of-art query optimization technology, less gaps between research and practical implementation
            2. Modularity
                1. Orca can be ported to other data management systems via plug-ins providing Metadata provider SDK
                2. run outside the database system as a stand-alone optimizer
                    1. Data eXchange Language (DXL)
                        1. Data eXchange Language (DXL), to exchange query, plan, metadata between Orca and Database system
            3. Multi-phase optimizer, but make it easier to extend
            4. Multi-core scheduler to distribute tasks across multiple cores
                1. Section 3: search includes both exploration and implementation steps; it's like volcano, but no cascades which merged the two
                    1. question: why separate explorartion vs implementation steps?
                2. Each transformation rule is a self-contained component that can be explicitly activated/deactivated in Orca configurations
            5. correctness and performance verification built-in for rapid development
        2. key designs
            1. During query execution, data can be distributed to segments in multiple ways including *hashed* distribution
                1. question: the distribution method seems hashign rather than range based? or range cut then hashing?
            2. Property Enforcements
                1. Properties have different types including logical properties (e.g., output columns),
                   physical properties (e.g., sort order and data distribution),
                   and scalar properties (e.g., columns used in join conditions)
                    1. An optimized child plan may either satisfy the required properties on its own (e.g., an IndexScan plan delivers sorted data), or an enforcer (e.g., a Sort operator) needs to be plugged in the plan to deliver the required property
                2. allows each operator to control enforcers placement based on child plans’ properties and operator’s local behavior
            3. Statistics are mainly histograms - "A statistics object in Orca is mainly a collection of column histograms used to derive estimates for cardinality and data skew."
                1. parent statistics are composed by single table statistics histograms. See Figure 5.
                   parent requirements are pushed down to children first, and then compose up
            4. Figure 6: Processing optimization requests in the Memo
                1. good useful to understanding how Memo works.
                2. Optimization is conducted by "requests". Requests carry logicial/physical properties.
                   Each requests are mapped to its best group expression.
                   requests are stored in hash table to dedup.
                   Expressions in upper Groups, generate requests passed/pointed to lower groups.
                3. Linkage structure in Memo - "Finally, the best plan is extracted from the Memo based on the linkage structure given by optimization requests"
            5. multi-stage optimization
                1. Stage: a complete optimization workflow using a subset of transformation rules and (optional) time-out and cost threshold
                    1. given by Orca's configuration
                2. This technique allows resource-constrained optimization where, for example
                    1. the most expensive transformation rules are configured to run in later stages to avoid increasing the optimization time
                    2. a foundation for obtaining a query plan as early as possible to cut-down search space for complex queries
            6. parallel job execution
                1. A query optimization is cut into small jobs, E.g. Exp(g), Imp(g), Opt(g), Xform(g)
                2. job dependency is tracked by dependency links. child complete notify parent. parent suspend waiting child
                3. A job scheduler abstraction do the scheduling work and completion notification
            7. Metadata exchange
                1. metadata providers are system specific plugins, across different database backends
                2. during optimization, related metadata objects are pined in-memory, until optimization done
                3. DXL file can provide metadata too, and a tool to harvest metadata into DXL file, save the needs to access live backend
            4. verifiability of Orca
                1. a cardinality estimation testing framework
                2. a number of benchmark tests at various scales
                3. a data generator that can generate data by reversing database statistics
                4. AMPERe tool to automatic capturing and replaying of optimizer’s anomalies
                    1. The dump captures the minimal amount of data needed to reproduce a problem, including the input query, optimizer configurations and metadata, serialized in DXL
                    2. dump can be replayed, and used a test cases
                5. TAQO tool automated method to measure the accuracy of optimizer’s cost mode
                    1. optimizer’s cost model to order any two given plans correctly
                    2. sampling plans uniformly from the search space, leveraging optimizer’s cost model to order any two given plans correctly
                    3. TAQO computes a correlation score between the ranking of sampled plans based on estimated costs and their ranking based on actual costs
                        1. TAQO computes a correlation score between the ranking of sampled plans based on estimated costs and their ranking based on actual costs
                        2. and also distance between plans
                            1. the score does not penalize optimizer for small differences in the estimated costs of plans that are actually close in execution time
                        3. The correlation score also allows benchmarking the optimizers of different database systems to evaluate their relative quality
            5. other designs

                2. Compact memo structure - "Derivation of statistics takes place on the compact Memo structure to avoid expanding the search space"
                3. Promise - "an InnerJoin expression with a small number of join conditions is more promising than another equivalent InnerJoin expression with a larger number of join conditions"
                4. "Property enforcement .. allows each operator to define the behavior of enforcing required properties based on the properties delivered by child plans and operator local behavior"
                    1. "For example, an order-preserving NL Join operator may not need to enforce a sort order on top of the join if the order is already delivered by outer child"

6. The MemSQL Query Optimizer: A modern optimizer for real-time analytics in a distributed database    [2016, 31 refs]
   http://www.vldb.org/pvldb/vol9/p1401-chen.pdf
    1. Very good paper. Covers many aspects of SQL query optimizer and with detailed SQL examples.
       The key improvements are how to consider distribution cost, and how to explore bushy join
    2. highlight
        1. MemSQL general
            1. in-memory row-oriented store and on-disk column-oriented
            2. OLAP workload in latency of seconds
                1. typical workload is star/snowflake schema with many joins, plus sorting, grouping, aggregation
                2. many query optimization effort are on joins
            3. distributed architecture is share-nothing, scheduler nodes and execution nodes (no specific data nodes vs SQL layer nodes?)
            4. distributed tables - hash partitioned, reference tables - replicated
            5. DQEP - distributed query execution plan
                1. SQL-like syntax used to pass query plan to executor nodes
                2. the REMOTE and RESULT table, SQL like, help executor nodes hide intra-node optimization 
            6. query optimizer - Rewriter, Enumerator, Planner
                1. Rewriter do transforms, in top-down fashion, invoke Enumerator to get costs
                2. Enumerator explore physical plan space, and maintain cost mode, consider data movement cost and accss path selection
                    1. Enumerator is bottom-up, adding annotations passed up.
                    2. intra-sql-block joins can be reordered, but inter-sql-block joins reorder are left to Rewriter top-down
                    3. interesting sharding, as a new property need consider in distributed context
                3. Planner translates execution plan to physical executable operation passed to executor nodes.
                    1. query plan can be cached for next use
        2. key designs
            1. distribution cost, i.e. those in data movement, e.g. early group by can reduce data move count, cannot be ignored.
                1. Example in Section 3.3
                2. This is a key improvement from "SQL Server PDW [14]"
            2. Bushy Joins
                1. most other query optimizer only explore left/right-deep join tree
                2. MemSQL explore joins combines heuristics and cost
                    1. heuristics allows repect user specified sub-query providing knowledged join structure
                    2. typical OLAP the table are organized as star/snowflake
                       the heuristics explore graphs, find seed tables and satelite tables, and cut bushy joins
                        1. the analyze is based only on graph connections, no involve cost
                        2. the heuristics probe new cuts, evaluate cost and decide whether to keep
                        3. better cut can leveraging pushing down filters
            3. in-memory DB needs to cut down query optimization time
                1. from paper, mostly pruning techniques

7. How Good Are Query Optimizers, Really?    [2015, 272 refs]
   https://www.vldb.org/pvldb/vol9/p204-leis.pdf
    1. very good paper. it proposed the methodology to study cost model and effects of cardinality estimation errors.
       it found cardinality estimate errors are way more affecting than cost models. and random samples help improve estimate quality.
    2. highlights
        1. key findings
            1. cardinality estimation errors
                1. database generally use single-column histograms and assuming
                   distributino uniformity, independence, principle of inclusion
                2. actual cardinality estimates for multi-join can be 10^2 to 10^4 orders of magnitude of wrong
                   and in absolute most cases are underestimates
                    1. the underestimate can lure DB optimizer to incorrectly choose nested-loop joins
                       which generates very slow query
                    2. query engines that mainly rely on hash joins and full table scans are more robust against large cardinality estimate errors
                        1. optimizer should take cardinality estimate error into consideration before select a plan
                           "hedging their bets" and not only choose the plan with the cheapest expected cost,
                           but take the probabilistic distribution of the estimate into account
                    3. more findings
                        1. queries with more indexes suffer more from cardinality estimate errors
                        2. "two wrongs that make a right" exist that can make a not-so-bad plan
                        3. query optimizer tends to systematically underestimate the result size of queries
                        4. swap the syntactic order of relations, joins, predicts, they can change estimates to the same query to 3,9,128,310. (bad)
                        5. join-crossing correlations
                            1. the effects of query optimization are always gated by the available options in terms of access paths
                    4. better methods for cardinality estimate
                        1. DBMS A and Hyper using random sample of 1000 rows per table, very effective
                        2. some commerical systems allow user configurable
                            1. sampling for base table estimation
                            2. multi-attribute hisograms ("column group statistics")
                            3. ex post feedback from previous query run [38]
            2. the difference of cost models are dwarfed by cardinality estimate errors
                1. see Figure 8
                    1. with true cardinalities, PostgreSQL cost model vs the simple cost model (only consider result tuple count), has little difference.
                        1. even the simple cost model can achieve linearity of cost vs runetime
                        2. i.e. even a trivial cost model is able to fairly accurately predict the query time, given true cardinalities
                            1. this means cardinality estimation worth more critical than better cost models
                    2. with PostgreSQL estimated cardinalities, both cost models are generating similar results
                        1. There are considerable amount of queries, that estimated as low cost, by the actual runtime are top high
                        2. PostgreSQL tuned cost model for main-memory sometime generate a plain of saying high cost, but actual execution time is extreme low (unknownly found well plan)
                2. Cost models need tunning
                    1. cost variables, i.e. the weight parameters of CPU, IO.
                        1. They are best treated as averages over the entire mix of queries that a particular installation will receive
                        2. main-memory DB can vary greatly from disk DB
                    2. tunning and calibrating cost models
                        1. baesd on sampling, various machine learning techniques
                        2. many papers [42] [25]
            3. Plan space enumeration
                1. importance of join order
                    1. the slowest or even median cost is generally multiple orders of magnitude more expensive than the cheapest plan
                    2. The percentage of plans that are at most 1.5× more expensive than the optimal plan is 44% without indexes, 39% with primary key indexes, but only 4% with foreign key indexes
                2. Are bushy tree necessary?
                    1. Tht zig-zag trees offer decent performance in most cases, with the worst case being 2.54× more expensive than the best bushy plan
                    2. The bad performance of right-deep trees is caused by the large intermediate hash tables that need to be created from each base relation and the fact that only the bottom-most join can be done via index lookup 
                    3. enumerating all bushy trees exhaustively offers moderate but not insignificant performance benefits in comparison with algorithms that enumerate only a sub set of the search space
                3. Are heuristics well enough?
                    1. using dynamic programming to explore full search space is more worthwhile than Quickpick-100 or Greedy Operator Ordering
                    2. given the existence of exhaustive enumeration algorithms that can find the optimal solution for queries with dozens of relations very quickly (e.g., [29, 12]), there are few cases where resorting to heuristics or disabling bushy trees should be necessary
        2. study methodologies - this is the good part
            1. JOB (Join Order Benchmark) based on IMDB dataset
            2. cardinality estimation
                1. obtain cardinality estimates from database intermediate results by using EXPLAIN commands
                2. inject these estimates of differente databses to PostSQL optimizer to obtain plans, compare and run
            3. cost models
                1. build the simple cost model only considering the result tuple count for baseline compare
                2. plot the linear plot of cost vs actual runtime
            4. plan space
                1. enumerate join orders, compute cost of each, and plot the distribution density plot
                   we can compare the space vs plan cost distribution
    n. related materials
        1. CMU 15-721 Cost model: https://15721.courses.cs.cmu.edu/spring2020/slides/22-costmodels.pdf
            1. Histograms are a type of "Sketches"
                1. Yahoo Sketching library
                   https://datasketches.apache.org/
                    1. interesting

        2. How cost-based optimizer dynamic programming search join order？
            1. PostgreSql cost-based optimizer
               https://www.postgresql.org/docs/9.5/planner-optimizer.html
                1. when join relation count < geqo_threshold, enumerate (near) all combinations
                2. otherwise, fallback to heuristics-based, to randomly generate join order and find low cost ones
                    1. retaining cost estimates for sub-joins, w.r.t. enough memory
                3. "explict join" to alow user specify join order
                   https://www.postgresql.org/docs/8.2/explicit-joins.html
            2. CockroachDB join ordering
               https://www.cockroachlabs.com/blog/join-ordering-pt1/
               https://www.cockroachlabs.com/blog/join-ordering-ii-the-ikkbz-algorithm/
                1. not solved? by saying a lot ..
            3. The MemSQL Query Optimizer
                1. exploit OLAP star/snowflake topology to explore most benefitial join orders first
            4. SQL Server join order
               http://www.benjaminnevarez.com/2010/06/optimizing-join-orders/
                1. "So how does the Query Optimizer analyze all these possible join orders? The answer is: it does not"
                2. probably heuristics
            5. oracle optimizer join order
                1. Choosing Execution Plans for Joins with the Rule-Based Approach
                   https://docs.oracle.com/cd/F49540_01/DOC/server.815/a67781/c20c_joi.htm
                    1. Fill order by choosing the table with the most highly ranked available access path
                    2. generally it's heuristics based. but comprehensive
                2. Choosing Execution Plans for Joins with the Cost-Based Approach
                   https://docs.oracle.com/cd/F49540_01/DOC/server.815/a67781/c20c_joi.htm
                    1. didn't mention how to enumerate all join orders
                3. About the optimizer's choice of join order
                   https://docs.oracle.com/javadb/10.8.3.0/tuning/ctunoptimz20327.html
                    1. When selecting a join order, the optimizer takes into account:
                        The size of each table
                        The indexes available on each table
                        Whether an index on a table is useful in a particular join order
                        The number of rows and pages to be scanned for each table in each join order
                2. The Importance of Table Join Order - Oracle Tips by Burleson Consulting
                   http://www.dba-oracle.com/oracle_tips_join_order.htm
                    1. "If the number of tables returning more than a single row in the query is less than optimizer_search_limit then the full factorial number of possible joins will be used in determining the path. If the number of tables returning more than a single row is greater than the optimizer_search_limit then Cartesian products are eliminated from the possible joins considered. Therefore the maximum number of joins considered for a given query with less than optimizer_search_limit+1 of involved tables can be expressed by either the value of optimizer_max_permutations or the optimizer_search_limit_factorial, whichever is larger."
                    2. it's like PostgreSQL, switching full search vs heuristics based on optimizer_max_permutations / optimizer_search_limit 


8. Morsel-driven parallelism: a NUMA-aware query evaluation framework for the many-core age     [2014, 200 refs]
   https://db.in.tum.de/~leis/papers/morsels.pdf
    1. Morsel-driven scheduling and pipeling are corner stones of nowaday execution engine, not only database.
       paper by HyPer team, targeting main-memory database.
    2. highlights
        1. key designs
            1. instead of static task partition, tasks are cut into "Morsel", dispatched to threads dynamically
                1. worker threads number is same with hardware threads
                    1. the dispatcher is implemented as a lock-free data structure only, instead of a separated thread
                2. operater is internally parallelized and inter- parallelized
                3. maximize locality, minimize synchronization
                    1. Option 2: build a global hash table on build relation, but parallellize both building and probing
                4. react to workload changes: priority-based scheduling of dynamic workloads possible
                5. NUMA Awareness at the morsel level
                    1. respect NUMA-local when scheduling new morsel
                    2. NUMA-Aware Table Partitioning
                        1. most join pairs should come from same CPU socket
                    3. threads may still steal morsels from a different socket, but try to avoid
                6. typical algorithms
                    1. parallel HashTable build
                    2. parallel hashtable aggregation
                    3. parallel merge-sort
                    4. parallel in-memory hash join
            2. Storage Implementation
                1. Use large virtual memory pages (2MB) both for the hash table and the tuple storage areas.
                    1. The number of TLB misses is reduced, the page table is guaranteed to fit into L1 cache,
                       and scalability problems from too many kernel page faults during the build phase are avoided.
            4. evaluation
                1. target architecture: Nehalem EX, 32 cores, 64 threads; Sandy Bridge EP
                2. TPC-H against PostgreSQL, HyPer, Vectorwise

    n. related materials
        1. IO Meter: OLAP 任务的并发执行与调度
           https://io-meter.com/2020/01/04/olap-distributed/
            1. good materials to summarize differnet technologies around database OLA query scheduling & execution
            2. Morsel-Driven Parallelism
                1. 使用 Pipeline 技术组合算子
                2. 使用自底向上的 Push 模型调度任务。当一个任务执行结束时，它会通知调度器将后序任务假如到任务队列中
                3. 既使用水平数据分区，也使用垂直数据分区，每个数据块的单位被称为 Morsel。一个Morsel 大约包含10000行数据。查询任务的执行单位是处理一个 Morsel
                4. NUMA-aware，为了实现 Data Locality，一个内核上执行的任务，由于其产出结果都储存在当前内核的 Cache 或 Memory 里，因此会优先将这个任务产生的后序任务调度在同一个内核上。这样就避免了在内核间进行数据通信的开销。
                5. 使用 Work-stealing 实现弹性伸缩和任务负载均衡，以缓解数据倾斜和处理速度倾斜带来的性能瓶颈。也就是说，当一个内核空闲时，它有能力从其他内核“偷取”一个任务来执行，这虽然有时会增加一个数据传输的开销，但是却缓解了忙碌内核上任务的堆积，总体来说将会加快任务的执行。
                6. 使用 Delay Scheduling 防止过于频繁的 Work stealing。在内核空闲并可以偷取任务时，调度器并非立即满足空闲内核的要求，而是让它稍稍等待一段时间。在这段时间里，也许忙碌内核就可以完成自己的任务，而跨内核调度任务就可以被避免。令人惊讶的是，这种简单的处理方式在实际应用中效果非常好。
        2. CMU 15-721 Query Scheduling & Execution
           https://15721.courses.cs.cmu.edu/spring2020/slides/12-scheduling.pdf
            1. static scheduling vs morsel-driven scheduling
            2. scheduling in different systems
                1. Hyper - no dispatcher, work threads cooperative schedule a query plan using a single task queue
                           use work stealing in the morsel-driven scheduling
                2. SAP HANA - use separate watchdog thread to check groups and assign tasks
                              worker threads are organized into groups, each group has a soft and hard priority task queue, soft is stealable
                3. SQL SERVER SQLOS - user-mode NUMA-aware OS layer that runs inside of the DBMS
                                      Non-preemptive thread scheduling through instrumented DBMS code

9. MonetDB/X100: Hyper-Pipelining Query Execution    [2005, 717 refs]
   http://cidrdb.org/cidr2005/papers/P19.pdf
    1. One of the founding paper of vectorized query processing.
       Useful to learn how to analyze CPU efficiency on query processing primitives
       and how to design the vectorized query primitives
    2. highlights
        1. MonetDB
            1. column-wise store, [oid, value] format (BAT), plus virtical fragmented into chunks
            2. vertical fragments are immutable, while new appends/delets into delta objects
                1. delta objects are NOT indexed, they are expected to be small and mostly in-memory
                2. "summary" indexes, similar with zone map
                3. overall, this is similar to PAX [2] format
        2. analyzing CPU perf
            1. most SQL processing are memory bound rather than CPU bound,
               CPU spent most time waiting memory load/store
            2. methodologies
                1. pipeline dependency
                    1. which leads to solution loop pipeling, the key to improve performance
                    2. vecto
                2. branch prediction and mismatch
                3. cache misses
                4. IPC measure
                    1. instruction per cycle reflect how much CPU is waiting pipeling, e.g. memory wait, branch mispredict
                    2. total instruction count of query primitives, core function
                        1. instruction count / IPC = how many cycles will use
                        2. IPC < 1 is bad, but common in DBs
                5. Figure 4, insert a UDF of Query 1 to reveal how DB performs on hardware
        3. X100 vector processing
            1. vectorized primitives
                1. the MIL SQL are purposely designed to be with fixed parameter, low degree of freedom,
                   thus to favor compilating them into efficient code, e.g. loop pipeling
                    1. also, operate without  having to know about table layout
                2. compound primitives to favor more loop pipeling
                    1. previous operator result are passed directly to next, with CPU register,
                       rather than through memory
                3. operator produce select arrays, it can ba a bit array of which column selectd
                    1. or select primitive fill a result array of selected vector positions
            2. vectorized blocks, to amortize loop in/out time into each record
                1. larger vector size is better, until they cannot fix into cache
                2. at the extreme vector size of 4M tuples, MonetDB/X100 behaves very similar to MonetDB/MIL
            4. general optimization guidelines
                1. cache-conscious data structure
                2. do the selection, computation, aggregation in a single pass, not materializing any data
                3. the "artificially" high bandwidths generated by MonetDB/MIL make it harder to scale the system to disk-based problems efficiently, simply because memory bandwidth tends to be much larger (and cheaper) than I/O bandwidth
                4. RAM
                    1. RAM access is carried out through explicit memory-to-cache and cache-to-memory routines (which contain platform-specific optimizations, sometimes including e.g. SSE prefetching and data movement assembly instructions).
                    2. The same vertically partitioned and even compressed disk data layout is used in RAM to save space and bandwidth.
                5. Cache
                    1. (de)compression happens on the boundary between RAM and cache
                    2. The X100 query processing operators should be cacheconscious and fragment huge datasets efficiently into cache-chunks and perform random data access only there
                6. CPU
                    1. that processing a tuple is independent of the previous and next tuples
                    2. compilers to produce efficient loop-pipelined code
                    3. reducing the number of load/stores in the instruction mix
                    4. Currently, this compilation is statically steered, but it may eventually become a run-time activity mandated by an optimizer


10. Query Optimization in Microsoft SQL Server PDW    [2012, 36 refs]
    http://cis.csuohio.edu/~sschung/cis611/MSPDWOptimization_PaperSIG2013.pdf
    http://cis.csuohio.edu/~sschung/CIS601/Heideloff_Presentation2_PDWQO.pdf
    1. 2-pass optimizer design to leverage single node SQL Server optimizer is clever
    2. highlights
        1. PDW engine distribute based on SQL Server nodes
        2. 2-pass optimization, to leverage SQL server optimization engine
            1. steps
                1. in Control node SQL Server instance, run single node optimization based on cascades
                2. rather than find the best plan, store *entire search space* in Memo
                3. pass Memo via serialize XML generator to PDW optimizer
                4. PDW optimizer do the second pass optimization, for distributed runs, considering data distribution, parallel execution, data dispatching
            2. PDW optimizer
                1. by extend DMS cost model, extend physical property considering distribution
                2. 对现有Cascades优化器的增强
                    1. "调整单机优化流程，在enumeration过程中，也会倾向对分布执行更有利的一些优化方式
                    2. 扩展更多的逻辑/物理算子，比如partial aggregation/final aggregation，以及每种operator分布式实现，join可以是local/directed/broadcast/repartition, aggregation可以是repartition/partial+final的形式。
                    3. 扩展出DMS enforcer，不同的分发方式形成不同物理operator"
            3. absence of pipelining
                1. "PDW的分布式plan可以用一系列的step来描述，每个step之间不构成pipelining，step直接顺序依次执行，中间结果数据要物化到temp table后，才能开始下一step，step内是并行"
            4. bottom-up + top-down
                1. top-down: single node SQL Server optimizer (control node)
                2. bottom-up: distribution optimization in PDW optimizer
    n. related materials
        1. Query Optimization in Microsoft SQL Server PDW
           https://zhuanlan.zhihu.com/p/366434087
            1. useful. covers may insights
```
