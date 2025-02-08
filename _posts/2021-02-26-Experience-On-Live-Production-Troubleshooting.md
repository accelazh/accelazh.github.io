---
layout: post
title: "Experience on Live Production Troubleshooting"
tagline : "Experience on Live Production Troubleshooting"
description: "Experience on Live Production Troubleshooting"
category: "Experience"
tags: [storage, reliability, engineering]
---
{% include JB/setup %}

Upon live production issue, before start, there are a few non-technical steps easy to neglect but proved very useful in practice

  * Search the victim cluster name in mail or history, to beware of any issues other people already investigated or on-going, and any operations other people just done. Highly possible they will reveal hints to the current issue.

    * The major sources of live production issues are usually new code deployment, new configuration changed, new features enabled, aggressive customer traffic (missed throttling).

  * Communicate with the people/customer who raised this live production issue. Make sure the true issues are understood. It is not uncommon to see misunderstanding after a few round of info passing and a chain of teams transferring issue ownership.

  * Besides the reported issue, review all monitoring metrics and alerting on the victim cluster. Make sure all issues are aware. And usually correlation in abnormal metrics reveal hints.

    * Besides correlation, comparing abnormal clusters and another healthy clusters also help locate the issue.

  * Better to have a dedicated online meeting room for all troubleshooting people present. Besides sharing clues, people who perform live mitigation changes must know each other.

  * Better to have a dedicated coordinator role. He/she knows and assigns what paths each other person is focusing, in parallel. He/she avoids chaos when live outage brings flood of communication and clues. Collaboration efficiency can be improved.

  * Better to have a dedicated customer communication role. He/she summarizes new findings from many pieces and share updates to customers, e.g. every 2 hrs. He/she shields the flood of customer asks to avoid distracting live troubleshooting people. Customer can be very anxious. He/she also periodically reminds priorities in case focus drifted away. 

There are a few common practices when start working on the live production issue

  * The priority is to mitigate customer impact first, rather than finding the root cause. Make sure the later one is not distracting. A typical mitigation is node/service restart, while root cause analysis (RCA) are much more time consuming.

  * Identify impact scope. E.g. how many customers and which accounts, e.g. which services and which clusters, e.g. are there more clusters affected but unknown? This helps understanding the issue and correct emergency prioritization, and well-formed customer communication.

    * Besides, when the impact started, is it continuously on-going or time-to-time? They are also common scope questions that customers may ask.

    * There can be other clusters having the same issue but just not triggered or noticed yet. Make sure they are discovered and proactively mitigated.

  * Stop the impact propagation. Are there deployment on-going in the victim cluster? Pause it. Are there deployment carrying suspicious changes in other clusters? Pause it. Are there auto node kill/restart tooling? Consider pause it to avoid snow avalanche. And beware restarted node may never come back, creating more failures. Are there auto analysis tooling? Consider pause some to avoid overload log searching. Note crashdumps have chance to fill disk up too. Cluster capacity may saturate if many nodes are dead. Repair/retry traffic spikes may cause overload failure avalanche. Think about temporary mitigation changes to relieve the situation.

  * Verify the mitigation steps or root causes found. Use two different methods or info sources to verify a hypothesis before conclude. Publish it in team channel so everyone can review. Use another test cluster to bake the mitigation steps before apply to production. Dial up the change, i.e. apply to few nodes than more, rather than directly apply to all nodes. 

    * Production logs/metrics are sources for investigation. But beware they can also have bugs (or less known pitfalls), thus lead to wrong path of investigation. Involving multiple people troubleshooting together helps avoid hanging in one dead tree, dipping into a local optimal rather than a global optimized.

    * A risky mitigation should first be baked on test, staging, canary clusters, before go to the real busy production clusters. Mitigation is also a change that should follow Safe Deployment Process. And beware not to introduce more failures in the mitigation steps, especially node restarting.

  * The mitigation steps should be shared and passed on to following teams. E.g. the next duty shift or other teams possible to hit the same issue again. It can become a team heads up or notice broadcast.

  * Continue the monitoring after mitigation is applied. Make sure things are truly fixed, especially for issues only happen time-to-time. The mitigation should be effective in different scenarios, e.g. when the victim cluster changes workload pattern, undergo an upgrading, enabled new feature, e.g. when it applies to other clusters with different setups.  The mitigation may need to cherry-pick to older codebases and involves patching too.

    * Verifying by scenarios involves having more complete understanding of what scenarios can happen. Rather than digging own parts, it requires team members to reach out wider scope, to understand what are the other moving parts in production, and what other people are doing, e.g. a parallel rollout of another feature by another team previously unknown. Scope yields more importance than depth sometime. 

About monitoring & alerting systems, and logging systems, there are some common concepts

  * Though easy to neglect, they actually deserve more reliability 9s than the customer facing services itself. When customer facing services are down, they must still be up and working so live investigating & mitigation can proceed.

    * Also, make sure cluster A's monitoring & alerting & logging are still working when cluster A is completed down.

  * A common monitoring & alerting & logging system involve many parts

    * Realtime and detailed: Logging. Finer-grain per request is more costly but very helpful for troubleshooting.

      * Logs should be properly tagged with trace id so that any log entry can follow up the entire processing tree. Values in logs should be properly formated so easy to parse statistics.

      * Logs should be properly leveled, dense vs sparse, full detail vs key info, normal vs error, etc. So that non-dense logs can be quickly searched and choose various retention policies.

    * Realtime: Nodes and services provide webpages to show their status. They are is also portals to perform live operations.

    * Minutes to realtime: live traces, e.g. perf flamegraph, function call traces, crashdump analysis, etc. With less sample rate, they minimally impact live services, but good to see when started live issue investigation.

    * Minutes to realtime: Time-series metrics that capture status and vital, and are used for alerting. 

      * Metrics involves customer facing metrics and system-side metrics. Customer facing metrics are helpful for locating the true customer issues, and to verify issues are truely mitigated. System-side metrics further involves feature, service, OS, hardware levels.

    * Minutes to realtime: Auto analysis tooling can generate reports for newly detected live issues. The process aggregates many info sources and make low-level decisions to help people troubleshooting.

    * Tens of minutes to realtime: Captured, summarized, or sampled key logs and key status. Higher delay but richer formats, e.g. a table which supports queries.

    * Hours to realtime: OLAP data warehouse that ingests everything, e.g. (aggregated) time-series metrics, key info, cluster setup, change history, etc. It is used for comprehensive investigation, and all sorts of data-driven analysis.

      * More, there can be BI mining jobs generating periodical reports, running on these data, and for more specific team/feature needs.

Techniques and methodologies for live issue investigation vary

  * In common level, narrowing down the issue always helps. Constraint component, time range, specific behavior; follow suspicious abnormality, and decompose.  Comparing with healthy contemporaries help identify what's abnormal

    * Sampling the specific victim requests, with good sense for what's abnormal, and then follow them bottom up. This is usually enough to reveal functional issues.

    * Latency issues may require statistics level analysis. A common method is to sample the outlier requests and follow up the decomposed time spent.

    * More comprehensively, impacted requests' latency can be seen as a tree of statistics properties. The biased latency, i.e. tree root, is driven by the bias of lower level properties. E.g. they all come from same TOR, e.g. they all run certain code path. The decomposition and correlated bias reveal culprits.

    * For statistics, beware of production metrics can be noisy. The results from collected statistics should be reproducible in another capture. Besides, the percentiles, especially P99 or P9999, can be easily affected by outliers.

  * Investigation experiences and understanding to codebases and key logs always help. In more advanced level, it's good to build up the knowledge framework, sufficient enough that

    * Image a request is decomposed into a tree of more detailed components and processing operations to bottom hardware. In anywhere of the tree, a source of abnormal pattern can be injected. In this thought experiment, we should always have tooling and methods to isolate and locate any possible source. We should always have a way for mitigation.

    * With experience and even better logging/tooling, we should be able to build and leverage shortcuts and do tree branch pruning. They can be applied to the most frequent possible issues.

    * The thought experiment tree should be complete. If every part is healthy, the tree root should be healthy. If every part has healthy latency, the tree root has healthy latency.

      * Failure injection, or Chaos Monkey stuff, can help here. It also requires the codebase is well-written, able to handle, reveal, and trace all sorts of abnormalities.

  * If the investigation is hard, it usually reflects the system is missing necessary logging or tooling (in the above thought experiment tree). Spending long time in investigation is a good thing, that it reveals new gaps and new improvement directions. Investigation isn't supposed to be hard.

    * The tier 1 is to use experience and talented skillset to narrow down, generate good guesses, and trace down what is the culprit.

    * The tier 2 is to have systematic tooling, providing various automations, decision making, and hint information in troubleshooting.

    * The tier 3 is infrastructure. When a live issue happens, every pieces are already ready for you to look at, e.g. the targeted traces, logging, crashdump analysis, history events. E.g. with constant perf collecting framework, the flamegraph of victim time range is already present, when latency reported unhealthy.

    * The investigation time spent is not wasted. It should be condensed into auto tooling and infrastructure, be used to fill system gaps, and also become shared knowledge. Management is needed here: Time spent should become value assets, and value assets should be reused with growing scope (rather than forget and throw).

  * Specially, tools for dumping and safely modifying persistent data or metadata, should be ready before live issue happens. E.g. the on-disk data format is usually dense and not human readable, good tooling here is critical to safely and quickly mitigate related production issues.

  * A shortcut is to compare the config changes and new code deployments around the impact window. This proved very effective to quickly locate what's wrong in the system. If otherwise, it's usually customer workload or usage pattern changes. Overall, find what's changed.

Retrospective analysis, where for in-depth RCA, think thoroughly, and turn shortterm mitigation into longterm fix/improvements

  * Perform "5 Whys". E.g. why is the issue only discovered now, rather than captured by earlier monitoring, more upstream systems. E.g. why it passed test and canary clusters baking, why it is not captured by test cases. E.g. why it needs manual investigation and mitigation, rather than self-heal by the system itself.

    * This is the first layer. After got answers, continue ask whys several more times to drill even deeper. They usually reveal core system gaps and future improvements, and key knowledge missing. Understand what is system bottleneck, prioritize and evolve. Be proactive.

  * Reuse. If the similar issue happens again, do we have systematic way to capture it? E.g. static code analysis, review, auto tooling, sanity checks, monitoring, etc. After written the fix code, do we have systematic methods to valid it? When seeing a similar issue, do we have a systematic way to investigate?

    * Learn the most from error and don't commit twice, and also defense for future. Many the needs can brew new advanced tooling frameworks.  Here comes innovation. Innovation is not optional. Enterprise needs innovation to evolve daily work, even they are small gradual improvements rather than paradigm shifts.

  * It is a feedback loop that continuously improve the system battle-tested, from new features, different live issues, various customer needs, etc. Time spent becomes value assets making the system more robust.  The infrastructure and tooling, for live issues investigation, are like highway. They are not customer features, like buildings. But highway determines how fast you can evolve in the feedback loop, like how fast buildings built.

Grow.

Additionally, experience on investigating production latency issues

```
1. Carefully review the results given by the monitoring system. narrow down the scope, the spikes.
   Examine whether some data are false data, possibly due to monitoring fluctuation, or data points reach in different time, etc
   
2. The top 1 time consuming thing in investigating latency issue, is no that issue is complex, but we mislead ourselves on a wrong path.
   So need to be careful to examine our logic chain is complete, not missing other paths, not missing other check items/possibilities etc.

3. Besides the alerting data we get from monitoring system, we usually need to go to actual production nodes,
   to compare and obtain the actual more detailed quantile data. And to examine whether there were patterns.

4. After forming our new hypothesis root cause, we should double verify. I.e. find data from a different source and verify in a second way that our hypothesis is correct.
   Many times we may find the look-obvious hypothesis may not be correct, or may not be consistency for all issue occurrences we are facing.
   This is also helpful to get us away from getting trapped in a wrong path.

5. As team work, we better find at least 2 persons to investigate the issue. 1 person is very easy to get trapped in one path (because his/her instinctive thinking habit etc).
   At least 2 persons, keep challenging & comparing & throwing light on each other results, will greatly help making progress in the investigating.
   And, a favorable model is 1 person do heavy dedicated investigation, the 2nd person just spend minimal time and do some quick time to time check, which is enough.

6. Some logging can be misleading. E.g. by tracing with a common trace id, but other unrelated stuff may be also packed on this tracing id as noise.
   By tracing by an object pointer address, but print with different type may give different value of the same object;
      and same object address may be reused due to memory allocation, or object reuse.
   The statistics of latency, load, queue depth, throughput printed in logs, may be aggregated in a different way than you thought,
      e.g. in too long a time window, so that it is useless for short burst spikes.
   The time printed in logging, may be calculating different thing if checking the details in code; need also be careful with it.

7. We may pick some common check items to check first. E.g. network congestion, disk slowdown, queue piled up, burst of requests, some other error or alerts, etc.
   Common check items help quickly identify same issue reoccurred from previous history we know.

8. Latency issue is usually the behavior of statistics. But logging and tracing works in per request level.
   Statistics vs single is a natural conflict. A usually useful practice is, during the issue period of statistics,
      we pick several single request that match the issue,
      we and follow them down to see if they reveal the true underlying issue and cross validate with each other.

9. Latency issue is usually the behavior of statistics. Decomposition the request handling into each phase, and get statistics of each phase component
   and compare is also a approach to find issue. It took more time usually. And hope our logging can be easy to use enough for we to extract the data

10. It can be very helpful to find another healthy period or cluster, and compare side-by-side with our issue one.
    Comparing healthy vs having-issue, can usually help to find out what's going wrong.

12. Besides the server side, also check the client side. the client side may be behaving in unusual way, may be receiving different errors,
      and may be sending more data count, more bigger data size, and from monitoring charts we may find more issues.
    Also, there can be read size amplification issue, e.g. block alignment layer by layer, prefetching / readahead, read more than needed, etc.

13. The speed of investigation usually depends on how quick you can "guess" the right culprit, from a bunch of other symptoms or noises.
      If we have more experience on the system, we can guess more accurately.
    The counter-side is to have guessed a lot and be wrong a lot and need to check a lot, and eventually discovered the true culprit by systematic decompose and search.
      It's like cache hit vs cache miss, where your caching experience is valuable.

14. Usually, as a complete investigation, we need to drill down to the bottom root cause (RCA), and next propose improvement items,
      and use statistics data to prove the two. The statistics data proof should be complete covering branches/corners and linked in a chain from start to final cause/proposal.
```
