---
layout: post
title: "Experience on Live Production Troubleshooting"
tagline : "Experience on Live Production Troubleshooting"
description: "Experience on Live Production Troubleshooting"
category: "storage"
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

    * A risky mitigation should first be baked on test, staging, canary tenants, before go to the real busy production tenants. Mitigation is also a change that should follow Safe Deployment Process. And beware not to introduce more failures in the mitigation steps, especially node restarting.

  * The mitigation steps should be shared and passed on to following teams. E.g. the next duty shift or other teams possible to hit the same issue again. It can become a team heads up or notice broadcast.

  * Continue the monitoring after mitigation is applied. Make sure things are truely fixed, especially for issues only happen time-to-time. The mitigation should be effective in different scenarios, e.g. when the victim cluster changes workload pattern, undergo an upgrading, enabled new feature, e.g. when it applies to other clusters with different setups.  The mitigation may need to cherry-pick to older codebases and involves patching too.

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

      * Metrics involves customer facing metrics and system-side metrics. Customer facing metrics are helpful for locating the true customer issues, and to verify issues are truely mitigated. System-side metrics futher involves feature, service, OS, hardware levels.

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

Retrospective analysis, where for in-depth RCA, think thoroughly, and turn shortterm mitigation into longterm fix/improvements

  * Perform "5 Whys". E.g. why is the issue only discovered now, rather than captured by earlier monitoring, more upstream systems. E.g. why it passed test and canary clusters baking, why it is not captured by test cases. E.g. why it needs manual investigation and mitigation, rather than self-heal by the system itselves.

    * This is the first layer. After got answers, continue ask whys several more times to drill even deeper. They usually reveal core system gaps and future improvements, and key knowledge missing. Understand what is system bottleneck, prioritize and evolve. Be proactive.

  * Reuse. If the similar issue happens again, do we have systematic way to capture it? E.g. static code analysis, review, auto tooling, sanity checks, monitoring, etc. After written the fix code, do we have systematic methods to valid it? When seeing a similar issue, do we have a systematic way to investigate?

    * Learn the most from error and don't commit twice, and also defense for future. Many the needs can brew new advanced tooling frameworks.  Here comes innovation. Innovation is not optional. Enterprise needs innovation to evolve daily work, even they are small gradual improvements rather than paradigm shifts.

  * It is a feedback loop that continuously improve the system battle-tested, from new features, different live issues, various customer needs, etc. Time spent becomes value assets making the system more rubost.  The infrastructure and tooling, for live issues investigation, are like highway. They are not customer features, like buildings. But highway determines how fast you can evolve in the feedback loop, like how fast buildings built.

Grow.
