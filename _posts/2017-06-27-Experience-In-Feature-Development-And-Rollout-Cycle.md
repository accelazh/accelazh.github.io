---
layout: post
title: "Experience in Feature Development and Rollout Cycle"
tagline : "Experience in Feature Development and Rollout Cycle"
description: "Experience in Feature Development and Rollout Cycle"
category: "storage"
tags: [engineering, development, rollout]
---
{% include JB/setup %}

Develop and rollout a production feature for large-scale online services, such as cloud, is like replacing wheels for a running train. How to online a serviecs without breaking the running code, and without impact customer reliability and performance SLA, needs to be coded in development and well throught while rollout.

New features come quick. Even the underlying systems, which are far from users, like storage, can be shipping with tens of new features each year. Cloud vendors such as AWS are publishing new services in rapid speed. Existing services are adding more options, usages, config setups, or performance/reliability selectables. In the meanwhile, services internally are evolving with new generation architectures, equipping with new technology (e.g. from new recent papers), improved internal algorithms of better profitibility, leverage new generation of hardware (better CPU, larger memory, disk; or FPGA, all in-memory), be larger scale (storage cluster has to support larger and larger dataset to make customer happy), better diagnostics or monitoring, performance or reliability improvements, etc.

On the other side, as more and more features are added, new bugs are brought in. Bug diagnostics and fixing are long-running effort. Some bugs happen only in race condition or under certain load or access pattern. Some bugs cause components to stall. Some bugs are performance regression. These bugs contribute to the main part of operation incidents which are not trival. They usually need to be discovered with a lot of investigation effort. Some bugs are related with upstream systems, for distributed storage it is usually the underlying filesystem. Semantics or logic bugs are however relatively rare. Even good architecture design is the foundation, the true killer of reallife reliability is bugs. A bug can kill (or just cause repeated restarting) the whole set of paxos, and thus stuck all your other services. 

As a result, usually we need devs take on operation incidents, several experienced devs for bug investigation, some for bug fixing, a lot of devs devoted to new feature development. There is no work partition, every dev takes every type of work. Operation incidents are important, as many system improvements/enhancements come from these investigations. There are many issues on-going, we never have to resource to implement all needs. They key is to determine priorities; what is the short-term mitigation, what is the long-term improvement/fix of the problem; we finish the core functions first, low-hanging fruits first, and give up the excessives for future, by which usually code are wrapped/evolved layer by layer; we implement, and then use A/B testing to measure the improvement we achieved; find out the gap, which in turn becomes the next cycle of critical things to fix; make a solid stepstone first, then next stepstone.

In this article I try to note down the experience of develop a new feature. There are usually many steps involved, design, analysis, evaluation, simulation, key algorithm, key config/parameter choosing, implementation, code review, all sorts of testing, evaluation for actual achievements, rollout steps, etc.

__Design__

In many cases, the feature to be implemented is not simple enough to allow let the design emerge from continous refactors. We need to take the impact to existing system into consideration, and the path of rollout. Also, there are usually several alternative designs we need to analysis and compare. Here I outline the perspectives to be considered in design phase

  * The performance factors we want to achieve: latency, tail latency, throughput, etc.
      * There can be different access patterns, customers scenarios.
      * We also need to consider the degrade performance when upgrade is on-goging, when zone failure happens, or when some data is lost and repair is on-going.
      * We need to consider what we should achieve when system is overloaded. And how to implement throttling
      * Sometime the performance can be related to the data placement. The placement is also a thing that needs well thought.
      * Besides latency, tail latency is also important for online internet services
      * We can combine different strategies, which form into a failover chain. Performance is more complex but more robust.
      * We shouldn't forget there can be background reads/writes (e.g. other services/customers are accessing), when we consider the performance of our systems.
      * Usually a feature means to improve from the existing one. So, how much improvements are we achieving. This should be analyzed.
      * Worst case analysis, in the (very) degrade case or very bad access pattern
      * If the hardware generation upgrades quickly, take that into consideration

  * The availability factors we want to achieve: how often data is offline
      * Usually, a (data storage) althorithm has inherit property of availability. This is something to compare
      * Analyze the failure patterns and how to deal with them is necessary.
      * And take the cluster system into consideration, such as TOR, failure domain, repair speed, etc; we can get another set of calculations for availability
          * Collecting the production metrics should be done prehand to know the reliability numbers for each hardware
      * Having replicas is not enough. We need real number data-driven calculations to known how well is something dong
      * Note that although more replica makes it harder to lose all, but one more replica adds one more frequency to lose something.
      * Worst case analysis, in the (very) degrade case or very bad failure pattern

  * The durability factors we want to achieve: how often data is lost from disk
      * Different from availability, durability calculates how easy is data lost from persistent disk rather than just offline
      * We may use markov state transition and calculate its MTTF. Or simpler, truncate it to a sigle direction condition tree and calculate it.
      * Usually durability is greatly larger than availability.
      * Other tips adoptable from the availability part

  * The overhead: storage overhead, memory bloat, extra IOs, CPU, network bandwidth, etc
      * Performance, availability/durability, overhead are usually conflicting. Make sure we know which one we should prioritize.
      * Online services need to have good profitibility. We need to consider COGS carefully.
      * The overhead part can blow up existing systems sometime. E.g. memory increase when our metadata size is already near system critical line; or space overhead when we are rolling out to a cluster that has used up nearly all storage.
      * Also, be aware with the read/write amplification introduced by the new feature
      * Another thing, an improved/better/complex algorithm to replace the older version, usually means it can introduce more performance overhead than the old. Be careful with the benchmarks.

  * The pressure on exsiting systems: extra IOs, memory bloat, metadata size, network bandwidth etc
      * An looks-like effective algorithm may however putting too much pressure on underlying existing systems. For example, it issues too many concurrnet IOs, it needs a lof of memory, etc.
      * We need to evaluate how much pressure we are giving out. Whether it is acceptable, especially in degraded cases, e.g. an upgrade is on-goging.

  * Co-work with upstream/downstream systems
      * E.g. storage system is usually at low-level. Many problems and performance optimizations are however easy to be achieved when we co-work with upper layer systems. Such as just change something simple in table services or DB. Make sure we don't waste unecessary effort implementing something. And, what can we leverage from the upper/lower systems?
      * On the other side, what we implement in underlying systems may negatively interfere with upper layer systems. We need to understand their access pattern, special case and do the design. Examples are GC process of upper layer systems, anti-virus scan, or they just easily create a lot of short-life entities which bloat our memory.
      * We usualy also need to co-work with upper layer systems to understand whether our new feature is solving their key needs, or not impacting their performance/reliability SLA or something.

  * Correctness vs Benefits
      * An implementation may approch the most accurate math model or probability model, etc. Or, it's a ball of many practical fixes each targeting to an actual problem.
          * The first one is nearer to academic way; it can be math elegant, but complex to implement; the actual benefit in production may however prove to be only a little improvement in the most common cases, and doing good in a few corner cases.
          * The later one is more practical; it can be simpler, flexible to implement; and most importantly, the actual benefit and problem solved are taken into design from start; it may perform better even.
          * The second way is the more favored way in engineering production. In summary, it's the benefits rather than correctness what we are pursuiing

Usually it needs to be data-driven, and do number calculates. Usually we extract the key KPIs, to reflect what we prioritize, what are the most direct to end result. We evaluation what we can achieve in design, and test/evaluate after implementation to find the gap. Explain the gap, find implementation bugs, or identify the next stepstone to go from the gap we see. In design phase we usually do analysis on the several design alternatives, compare, and make choice. There are several tips on math/simulation analysis

  * Math, combinations, probability, matrix, markov model, and even stochastic process are something necessary.
  * Put things on charts. The distribution chart or the cumulative distribution chart or the quantiles, etc, can be useful to see patterns and easier for readers to understand.
  * There can be many cases, branches, combinations. Using math to calculate it can be sometime difficult. Then, we can write a program to do simulation. This can solve a lot of hard problems. I.e. simulation + math is helpful.
      * In the end we can accumulate a bunch of tools to simulate each things. And helper programs to calculate performance/reliability things.
  * The input data can be obtained from production trace. Most time by crawl the logs and collect what we need. Synthesis inputs may not reflect the real problem.
  * Usually in design phase we can get the performance improvement estimated. After implementation, we compare and find out why it is not fast as expect, which usually help locate bugs.

In the end, different design alternatives may show different trade-offs, rather than simple who is all better than whom.

  * We can use the rank table or score table, by alternatives * KPIs, to show the difference. The key is to show the team and management levels the transparent information of trade-off. So that eventually we can discuss and make consistent choices.
  * Another way, is to provide different config setups for users to favor different trade-offs. E.g. allow users to select optimal storage space, or optimal performance. However this introduces more implementation effort

Besides the design, before implementation we also need to find the actual parameters/configs numbers for our design. Some algorithms may even need an carefully choosen matrix satisfying a lot of constraints. Or the EC codec needs well-choosen codec parameters and length. Here are some tips

  * For example, how large should it be, when should we fallover to another, how many concurrnet IOs to issue, etc. These parameters/configs need to be carefuly choosen; they may have great impact on the end results.
  * Still, we use math or simulations to tell which choice is optimal. And we can use charts to visualize results and help analysis.
  * When searching for an optimal parameter, we can just brutal force, or use anneal algorithm, or use math to reduce the problem to a smaller space before search.
  * When can also use mapreduce for searching.

There are other aspects we need to take into consideration in design phase

  * Growth: as we have more customers and they are storing more things, accessing more, can we handle the growth?
      * Data growth, memory growth, scale growth, etc
      * How do we handle the growth? Do we have enought capacity? What is the limit? What can be the next generation design? etc.

  * Key component protection
      * We also need to include risks into consideration. It can be reflect in our design, and in our rollout.
      * First, many services have central metadata management components (though it can be paoxes, but still easy to fall). Make sure we carefully handle the related risks, and we have proper preparation if we introduced something wrong
      * Data corruption. This can destroy the business. Be careful that we involved enough protection and caution in the design and rollout. Also, beware that data corruption can quickly propagate across replicas.

Next we need to consider migration. We need to be absolutely careful when migrating customer data

  * We absolutely need some ways to ensure customer durable data is not screwed up while migrating to new feature code. Otherwise, it can totally destroy the business. To ensure this, we may have to do the rollout very slow and very careful, gradually and with many checks, and may need to leave some backups in the middle
  * In the steps of migration, we need to check whether there can be more overhead that can burden our system. E.g. need to uncompress and then compress, unEC then to reEC. Make sure the metadata and storage overhead won't jam normal customer traffic.
  * Migration its own will use a portion of our cluster resource, besides those to serve normal customer traffic. We need to calculate how fast can we do migration, to not impact SLA. And we need to implement the mechanisms, such as throttling, to control how fast we migrate.
      * When we are rolling back, we need throttling too.
  * Besides the data part, how the code is rolled out, how the feature switch is enabled (in what order, who first, etc), how the serviecs are replaced or restarted, etc, need to be considered.
  * Usually the design must be able to handle half old half new cases. E.g. half nodes are old, half are new; or half data is old, and half data is in new version.
      * Also, nodes can be down and up, or an acient node just come back with super old data. Be careful they won't break the logic

__Implementation__

Now we come to writing the code. Here I list the tips

  * After the design, we usually plan out a list of proposed code changes. Send them out to team, review, and make sure we are modifying code right.
  * After that, we create tasks and estimate efforts for tracking. Scrum is not a necessary workflow.
  * For big features, we can set a few milestones in the middle, and where we can demo something. Or, an epic story can be broken down to more smaller features before we actually start.
  * For big featueres, instead of finish it all at once, we can break it into many small patches, and merge them continously. These smaller changes will also have time to be verified by running. Suppose you are upgrading the whole architecture to version two, changing to a totally different set of algorithms, and cannot break any customer SLA.
  * We can develop on a separated git branch, but be sure to periodically merge and test back to master on e.g. weekly basis. Otherwise other teams' meges can flood your branch far away.
  * Another important thing is, feature switch (enable/disable). When we are considering rollback, we need to make sure we have way to disable new features. Usually a big systems need the ability of dynamically applied configuration change.
      * But be careful to handle when new feature is disabled, but new data is still there
  * Writing code for distributed systems can be tricky that, nodes can go online and offline and repeat many times. They can do this quickly, or just offline for very long time can then come back with the old data.
      * Since many feature logics are async, and needs to be carried out step by step. These node up and down can easily break the steps and mess up the async logic.
      * Offline then online may even bring you older version of data/metadata when you think you have fully rolled out to new feature

Code review is very important.
  
  * Teammates eyes are much sharper that testing to find bugs.
  * In daily work, review others code should be of high priority than write own code. Because pending CR blocks others work.
  * For big patches, we can scheduling some meetings to give other teams background contexts before they start review.
  * Face-to-face talk are usually very handy to discuss code review problems. Software development is indeed communication dense work.

__Testing__

Usually after code component owners sign-off, new code is merged to master. Master code is usually far beyond the verison running on production. This gives us time to test them in the pipeline

  * Unit test. We write unit test to do method level test, which tests the fine-grain whitebox logic. Unit test is cheap to write and run.
  * Local simulation environment. Like openstack devstack. It runs one one node on dev box, simulating production environment as much as possible. We can test the message communication with component endpoints, or blackbox logic. The tricky thing is, states are hard to retrieve when given the blackbox, and simulation is very different from production when testing things need scale, such as placement, reliability, scheduling, etc.
  * Test environment. Usually we provide several test cluster for devs to test out their features. They are multi-node environment, same with production except samller. A test cluster is usually deployed with other people's code too. Because the crashes/bugs are not from your part but misleading.
      * There can be sets of tools to automate the feature testing, to create stress load, or to validate the results. They are handy for devs to use.
  * Staging environment. Staging environment is the same with production. There are simulated customer traffic running on it, and whole set of production monitoring. We can rely on them to find bugs in code.
  * Canary production environment. This is production clusters, but for customers willing to try out new features (may not be stable). So after new code is well-tested on testing environments, we move to the first production environment.
  * Production environments can be ordered from samller/less-used ones, to large and heavily used once. This is not testing. But we can rollout from less risky production to heavy-running ones. In the meanwhile, good monitoring and alerting is critical for us to know anything goes wrong, and before the user even noticed.
  * There are user end tests, which targets on product user-facing APIs. There can be dedicated team and framework that doing such testing in continous effort. And there are also stress/load tests that intentionally heavily pressure an environment until it is full, so that we can discover more problems.
  * If the hardware generation upgrades quickly, take that into consideration. The hardware you write code and the production may differ, especially the performance aspects.
  * Scenario-based testing is a way, though we will mostly focus on functional. Catch missed scenarios, e.g. what ops need but not customer.
  * Test the middle steps on rollout, the special flags to turn on, and able to fallback in worst cases. Test the extra verification used in middle or rollout won't crash itself. Carefully test the data migration, fallback, and old/new code facing new/old data structure.

Here are some tips about writting test cases. They key is covering all combinations are simply not possible, we need other ways, the engineering ways, with reasonable effort corresponding to what work has true value. Below are my tips combined reallife experience and something from textbook

  * The techniques about testing large test case combination.
      * Equivalent class: what is proper to be selected as a class?
    * Merge some for loops to others. E.g. for (a) { for (b) {..}} => for (b) { a = rand() }. But this loses some coverage. 
    * Sampling. For example, for (a = 1..100) => for (i = 1..10) {a = rand (1, 100)}. We can also add some edge cases as complementary.
    * Focus on critical cases first. Some case are more critical to system reliability, or more frequently used.
        * We make sure the most critical cases / low-hanging fruits work fine first, and then as the stepstone, we continuouly improve/involve more.
        * We can use A/B testing. A is the original code, B is the new code but only do logging.
            * We compare the logs and identify the ciritcal issues to fix, and (quantitively) verify how much actual improvements B is gaining over A.
    * Smaller model. For example, use a smaller matrix or less replicas instead of full. The correctness of tests can be preserved.
    * Only full cover the critical cases, and use random select for the remaining. So that we still have chance to cover the remaining.
    * In the end, we can add an overall case skip ratio, to equally skip all cases.

  * If there are too many test cases even after we only include the critical ones
    * Select the most critical ones. we first add the test cases for the most critical ones.
    * Next, when we have extra test time, we just add more, and add more, layer by layer
    * The contrary way is to write all at once. this is not favorable when we have limitted resources.

  * For complex combinations beyond test effort, we can write test cases this way
      * A core test case to cover the most critical functionalities. It may be using random tests.
      * A random tests to cover the full wide range. It just use one for-loop, and randomly generate each setup options.
          * We can give different options different probabilities to reflect importance
      * A group of static predefined testcases to cover what we care else

Besides the tests to ensure functional correctness, we need to evaluation the performance results of our implementation. We compare it with 1) our analysis in design 2) the existing old feature, like A/B testing, to find out how well we are doing. The gaps may indicate bugs in our implementation which causes performance regression, or it can become something we can improve in the next cycle, or something that we missed in our analysis model.

  * We can outline a list of what KPIs we are going to track. Like the latency, throughput, tails, etc. Make sure we don't just forget something in the middle
  * It's good to use a spare production environment, or a staging one, because they approach real performance closer. Otherwise we can use test environment.
  * We can use simulated traffic and collect results from monitoring or logging. Charts are good to reflect the combined results.
  * When simulating, we should be aware that in reallife, there should be background reads/writes. We can choose to add them or not.
  * When digging the latency issue, we can compare the latency distribution. We can break them down into step-wise latency distributions, and find out where is going wrong.
  * When running on production, we can collect real performance numbers to analysis the gaps.
  * Also, for existing functionalities, test to find whether we have introduced performance regression

Also, we need tests for reliability and failure scenarios

  * We identify the key failure patterns need to cover, and inject them to the system
      * Having APIs for failure injection in the system is handy for tests and automation
  * We need to test how the system can recover from failures. It needs to recover in expected time and in expected cases.
  * Also, the customer-facing performance and SLA shouldn't be impacted during failures. We also need to measure how is the actual performance when failure exists.
  * When testing in test environment or staging, an automated chaos monkey like something can be useful. We can run unmanned long-term testing combined with monitoring and alert systems to tell us when it goes wrong.

Also, we need to test the overhead and pressure we give, such as memory bloat, cpu, disk bloat, etc

  * This is easy to forget. But we need to evaluate that we are not giving our more overhead or pressure than we expect.
  * Test to make sure that critical system resources won't blow up. Such as metadata memory overhead, or use up the disk space.
  * Also, how much more CPU we are using. Using too much CPU may indicate bugs or can heavily affact other functionalities.
  * Also, check we are not writting too much log unexpectedly, which uses up the disk quota.
  * If a new (more complex) alogrithm is replacing the older one. Besides A/B compare how well it performs functionally, we also need to A/B test the performance overhead it introduces more than the older algorithm.

__Rollout__

Rollout needs to be carefully planned, especially the rollback part. Otherwise we can easily screw ourselves out of business. Stateless services are easier to rollout, but services owning data, such as storage, needs to be careful. Here are some tips

  * In the rollout plan, usually we need to list the binaries, configuration, feature switch changes. We need to detail what to operate in each step. And we need to outline the many phases from beginning to end. We also give an time schedule plan.
      * The detailed rollout step worth careful design. We usually need to implement something in it, so that it is easy to operate and rollback, and in the middle we still have backup of data.
  * It is practical to review the rollout plan with team, and necessarily, involve some very experienced seniors. Make sure that we won't mess up something, miss something. Also, make sure we won't impact the upstream/downstream systems as we rollout. And the upstream/downstream know that we are doing the rollout.
  * Also, we should work with upstream/downstream systems to help our rollout. And, can we depend on some of their behavior/functionality to make rollout easier?
  * The rollout phases starts from testing. In each rollout step, we all execute some tests to ensure correctness. And we set gate conditions about wether we should enter the next step. Also, monitoring and alerting systems should be running, so that they help find issues. We also need to determine how long time we should watch on each phase.
      * Full testing on test environments
          * Usually we also need to prepare a testing plan for here and later use.
      * Full testing on staging environments
      * Rollout and test on canary production environments.
      * We choose a small sample set of all production environments. The sample should cover full range of scenarios, from easy to hard, from light to heavy. After we rolled out the sample set, we should have confidence to rollout any environments left.
      * Rollout the remaining production environments. Start from the less important ones, such as backup cluster, then less used onces, and then to the heavily used hot ones in the end.
  * Rollback. Rollout have many steps, we need to make sure at every step at any time, we all have rollback plan prepared.
  * Rollback. Rollback needs to be tested. It should be added in the test plan and executed/rehearsed at every rollout phase.
  * When rollout is changing persistent data, better keep old data for some time in case we need some recover.
  * Make sure that in every state of rollout, we all have the rollback plan to go back
  * Next we need some automation. Like a controller to govern the phase/state change in the rollout process.
      * It should automate the testing, watch gate conditions, and determine when to forward to the next step.
      * It should keep watch key metrics, logs. and report abnormals or incorrectness. It should do some integrity checks.
      * Also, it should also it should watch latency or other performance degrades.
      * It is good to be able to handle rollback. And should give chance for human to come in for manual operate
      * It should have proper visualization of current status, at least a periodically report sending through mail.
      * Also, sign-off mechanisms can be used for human to determine whether the auto controller should enter the next phase.
  * In the end, data related rollout can take very long time. Because it needs to gradually transform all data formats, in the reliable way.
  * Some mechansim to help rollout and baking
      * Shadow feature. The new feature only prints log, but don't carry out actual action. The old feature is still running. So that we can compare the actual benefit. Besides logs, we may also need aggregrate metrics or counters to reveal overall benefits, rather than human read logs one by one.
      * Baking time and rollout flow. The new feature is not one-off thing.
          * New fixes/improvements keep adding to it. It's a flow. The binary rollout is a flow too. The feature enabling along staging->canary->production with order, is also a flow.
          * We may set free the binary flow, bug keep the enabling flow sit to staging/canary for a long baking time, and while we are adding new fixes/improvements to the feature flow.

  * Core feature catch rollout timeline should have metrics monitoring, incident alerting, log scanning, and even Jupyter Notebook processed scanning, to run daily.
    * Periodically to sample vicitim clusters and scale-out to team members to co-review
    * Auto marking healthy and unhealthy can be tricky. Filtering out noise is a long-term and non-trival task
    * For tight schedule, we need to allocate more resource on daily scanning and more people for co-review. For important incidents, we need to establish prioritized collaboration process - keep focus, cancel all meeting, push off all dev work.

  * Core feature catch rollout timeline should have testing pipeline continuously running
     * This is to catch that new changes may break existing feature, and we need to know before code deploy on production. Otherwise we have to do hotfixing which delays feature rollout.
     * If we see the testing break, don't wait. need first time high priority act to fix.
     * Proactive act in mind. E.g. to review code changes from other tracks that may impact the core feature rollout.
     * Or when people ask us to review, don't wait or ignore. otherwise when the PR merged we have more work to fix.
