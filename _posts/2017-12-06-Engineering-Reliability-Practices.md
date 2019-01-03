---
layout: post
title: "Engineering Reliability Practices"
tagline : "Engineering Reliability Practices"
description: "Engineering Reliability Practices"
category: "storage"
tags: [reliability, engineering, development]
---
{% include JB/setup %}

One of the core drive of storage system development is reliability; the reliability vs rapid growing scale, the reliability under performance and cost constraints. Enterprise storage carries tons of features. Cloud storage grows new ones fast (thanks to AWS). And online service means to replace hot wheels on speed vehicle. Hardware upgrades fast, even outperforms the performance gain by improving software; storage systems need to shift from generating of generation; Flash, NVM, big memory, bigger disk, FPGA, GPU, RDMA, ... Reliability engineering is a complex of storage theory, feature delivery management, infrastructure and operation practices.

__Feature delivery__

Now matter how storage design in papers is said to improve reliability, bugs are actually the top killer; and it kills redundancy, replication, and backup altogether.

Code development worth careful design and evaluation. Code review is core way to find out logic bugs. Peer review and find senior review (may as sign-off gate); they have more experience on what can get the system into trouble. Code quality and readability affacts how fast we inject new bugs. And with logging and other facilities it affacts how fast we diagnose issues in production to mitigate customer impact.

Testing. Unit, integrated, build verification, smoke, release; functional, performance; failure; stress, capacity; on devbox, test env, staging env, canary, production - testing. They are what we need to do. Smoke tests periodically run in production are extremely important to detect issues. Rollout gate tests, and rollback testing, are important for big new features, especially those affact persistent data. Scenario-based testing and thinking is a way to find out missed tests, e.g. not only customer scenarios, but how ops necessarily uses the feature (e.g. rolling upgrade); compared to just test combinations, scenario is better to catch bugs. Also customer API part worth dedicated team seperate testing; and also cluster-based stress/capacity testing from customer API.

Rollout, i.e. replacing hot wheel in speed vehicle, worth attention. In practice, there are many teams pushing features to production. There are quick changes, hot fixes, and big new features; stateless or will change persistent data. Feature should have switches to enable/disable; and we should always have ways to go back. Like code, include peer review for the rollout plans. Invovle senior reviews for risky features; use their experience to find incompleteness and potential issues. Rollback plan needs to be rehearsed, and make sure in each rollout state we always are able to go back. When changing persistent data, better keep old data for some time in case we need recover. We may build controller/watcher services to monitor the rollout, do automated gate and smoke tests, and do circuit breaker in the rollout process. From test env, staging env, canary env, to production;  before go to all production envs, we can choose those pilot ones; and we can choose a small sample set of production envs which cover hardware/config/capacity/load etc varieties as the first rollout. In middle of rollout a certain cluster, we need middle stages to test/validate feature workable correct in controllable fashion, e.g. dial up the data involved, e.g. generate some data and test, e.g. use target EC schema plus an extra copy instance.

If you are reviewing evaluation results, you need to be careful. Find unexpected resutls in this step is much eaiser than locate RCA from unexpected issues on production. Grasp the interacting parts in the project from global, think about what key improvements and what overhead you need to control and visiualize. Make sure each can see results in evaluation, the separate charts/data are chained to support results with completeness. When looking at charts/data, think about whether this is expected or unexpected, need to work with experience, attention, and the sensitive to discover hidden issue in charts/data. Principles and workflows are impactful. To say high technology of high reliability, is essentially to say to work with high quality.

See previous [Experience in Feature Development and Rollout Cycle](/Experience-In-Feature-Development-And-Rollout-Cycle) for real stuff.

__Storage design__

Too many papers and studies on this area. Classic distributed storage design papers are good reference. Also those MTTF papers (see [Study on Erasure Coding Technology Spectrum](/erasure-coding/Study-On-Erasure-Coding-Technology-Spectrum)) uses Markov models to tell which part affects reliability most. Note that higher redundency level improves reliability but is constrainted by cost, replication or repair speed affects the vulnerable exposure time window, faster detection means shorter exposure, cross-site replicate breaks the chain of correlation.

And, the most important but very easy to ignore, hardware. The hardware AFR is the foundation of what resulting MTTF you can get from software services. In practice, many operation issues, including those perf issues, can be traced back to hardware, e.g. slow API performance by underlying NIC slowdown. Another thing is vendor hardware may have issues in batch, firmware bugs, or need updates; which can cause hot production issues need to track. There can be OS rebooting randomly and repeatedly. Another thing is the the hardware upgrade, especially those to supply power. A datacenter may have double power sources, but one is being replaced; then when another one goes down, Datacenter outgate. The datacenter can have cooling issue, humidity issue, noise and viberation which affects disk performance & reliability, inproper installation, overheat, or cable loose up, etc. Think how many operation issues they can create. In the end, we should collect the hardware history like AFR and other paremeters, as the way to know our system performance, and as the base to analysis storage designs. There are failure patterns. When transforming paper designs to actual implementions, customizing them to what actual production env is is important, and needs to choose the best config and parameters; all those need the foundamental numbers collected from hardware observation. Also, know the history, know the improvement.

Data placement, balance and migration, replication speed, data failure detection, repair priorities, repair speed, scrubbing; and the EC schema. All those aspects in storage design affects the final reliability. There are too many details and too many optimizations we can do. All those need to be trade-off-ed with cost, perforance, overhead, energy, release cycle, etc. E.g. Markov-MTTF probability based repair scheduling theoretically is the most fine-grained; but the actual complexity and computation overhead to implement it may be far from worth it. On the other hand, when we have good knowledge of the businesses and apps on top of storage, specially use different strategies towards different workflows is easy and effective. E.g. internal housekeeping data vs customer; old data vs new data in append-only workload.

__Infrastructure__

Continuous delivery pipeline, as today in devops and in the ["Continuous Delivery book"](https://book.douban.com/subject/6862062/) by Jez Humble & David Farley. The orchestration automates deployment with the manifest files, which avoids human error injection. Frequent iteration "do the hard part often" to amortize big risk. Monitoring systems, which can cover the cold, warm, hot tier and path of data or metrics collection and retention, from logging archive, to realtime alerting; it should also allow devs to fast and easily add more and more checks and measures for new features. The alerting systems is important for us to know system abnormal early than outage is observed by customer; there can accumulate a lot of rules and configs. Alert rule settings should be continuously updated to filter noise out. Visualization is important work, and it can need a very comprehensive platform; watching the visualized cluster status can be the first step to troubleshooting; many hidden background issue can be found out there. Generally monitoring/alerting/auto-diagnostics will become foundamental of operation reliability, e.g. we want storage systems of reliability of A, the monitoring/alerting/auto-diagnostics needs reliability of >A.

Diagnosing toolset is important. The faster devs can locate issue, the faster customer impact can be mitigated. Logging and distributed search can be a main tool. Writting good logging code worth attention; it can reflect functional, performance, status change, and alerting; individual logs should dump sufficient background variables too. When new feature is being baked in test and staging envs, various debugging tools, stress, and perf or memory analyzers can be used to trace bugs. And customized debugging extensions can also be implemented for big projects. Automated diagnosing, issue triage, and root cause analysis platforms can be implemented to ease the operation work, reduce repeated work, and to provide instance status report for troubleshooting.

Besides the data plan of storage system to support customer traffic, the health team, i.e. the team to provide the above infrastructure, is very important. If you want the storage system to have five 9s, the health infrastructure should have even higher 9s, because it's the foundation that the storage can run reliable. In academic papers, storage reliability is a result of good technical solutions; but in reality, many life issues are affecting the final results. Papers won't tell you that good monitoring, log search, diagnostics, health services impact even more than advanced reliability technologies; and for complex technologies, a bug can break down all your data no matter how many replications or EC you have, and the error can propagate to remote backup/replication quickly.

__Operation practice__

The first is issue handling. Live issues are graded by severity, evaluated the impact and scope, and tagged as having customer impact or not. They are triaged to different teams, where neighbor teams often collaborate tight. Customer impact issues need great attention; issues having customer impact ususally require related dev war table online till solved. Another concept is mitigation vs fix; where mitigation is to relieve customer from impact, no require of knowing the cause, and fix needs to know the root cause. Repeated issue handling should be automated, as suggested in the ["Google SRE book"](https://book.douban.com/subject/26875239/) by Betsy Beyer. Standard steps and handling can be accumulated into documentation, continously updated, auto linked to issue tracking, and distributed to operation guys. There can be front-line operations, second-line operations, etc, eventually to the dev; to filter out the repeated and known works in issue handling.

Root cause needs to be located and documented in the issue tracking, for any customer impact issues. Postmortem meeting should be held periodically to review and discuss what we can learn. This is the important piece of how production systems can evolve; different from the innovations from papers, operation experience tells many small improvements. They may not be catchy, or using high-tech, but they solve real customer issue and perf issue; the accumulated improvements along time makes great difference; implementation matters. Talking about how storage systems evolves, besides the small accumulated improvements; another drive is the growing data scale, need for performance, and for high reliability; hardware keep upgrades with bigger disk and memory, and new hardwares like FPGA, GPU, RDMA, NVM are gradually being adopted; yet another drive is customer needs, the way of using storage may change, e.g. filesystem or object storage, HDFS, computation model, etc; and, in every a few years, there can be big architecture shift, just like when GFS/MapReduce/BigTable were published.

Some production issues can reoccuring for long time, or not be able to fix quickly. Tracking those issues is necessary. There can be a lot of issues going back and forth in devs. Prioritize them is a common way. Facing with immediate issue, there can be shortterm actions, like how to stop and mitigate it, and what should be more intensively watched; and longterm actions, like what feature should we improve, to stop the issue to reoccur, or to allow us to detect them earlier. The entire operation issue status should be evolving, i.e. old issues gradually stop reoccuring, because they are fixed or automated; new features are being added so there are new issues met. Besides, since now devs and operations are merged into one functional team, there are duty day rotation; we should watch the overall team efficency, i.e. make sure they are focusing on deliver things that have longterm value, rather than keep spending time on repeated shortterm things. I.e. as suggested in ["Google SRE book"](https://book.douban.com/subject/26875239/), only longterm value thing is what a team should be doing, others should be automated as much as possible. Shortterm fix & longterm fix are frequent concepts after operation issues RCA; and this continuous improvement is key to increasing reliability targets year by year.

As the internet trends, storage systems development iterations are going faster and faster. There can be a release to production in every a few months. Release management is necessary. Git branch can be tagged and checkout a release branch; while testing and master growing, put useful fixes and patches back to release branch. As release branch is baking, tests are walked through, and from staging to canary to production, many issues need to be found and tracked. When ready, the automated rolling upgrade system can quickly bring the binaries to each production env. And the feature teams can use config switches to enable new features gradually following the rollout plan. There can be hot fixes and blocker issues during release cycle; as we practice it frequent, experiences learned and the system and management grow robust.

For longterm planning, and strategic comparison with competitors, there are high-level views and metric indexes for storage reliability, especially what customer sees. Like VM availability, SLA satisfy status, customer impact issue count and resolution speed, customer asks and support speed and satisfactory, etc. They should be improving year by year, while following the market growing and maintaining the cost level. The high-level goals can be decomposed into various smaller measures, become the focus, priority, strategies and solution projects in each team, and evaluate the results.

Actually, when saying about high technology / high reliability stuff, it's essentially about work with high quality.

__Scratch Notes__

Notes 1

```
1. also include those in other notes, such as monitoring, and incidents continuous improving. and eventually the SRE engineering system. Also include those in the google SRE book.
2. besides technology, coding schema, engineering system/practice and continuous improvement is the key to reliability
3. EC schema, distributed techniques, hardware operation and design, datacenter design, monitoring and alerting, engineering and continous improvement
   storage device/media faliure pattern study
   and data scrubbing
4. trade-off with cost, performance, energy, overhead, etc
5. the release management, as the periodical release stage meeting notes. continuous delivery, fast iteration rollout, cherry-pick hot fixes, tracking issues. automated tests, unit, build verification, smoke, customer API, rollout test, 
   shortterm and longterm fixes.

-----
[notes on writting article]

1. starting with storage trends: scale, reliability, more feature (big data, distributed fs, deeplearning GPU), cost (ec, cross site ec, etc), hardware change (flash, NVM, bigger mem/disk, faster CPU, FPGA, etc). we may hit architecture new generation, but that is very rare
   then we come to reliability
```

Notes 2

```
reliability outline
1. monitoring & alerting, livesite, continuous improvement, engineering practice; google SRE book
1.5. operation steps standarization, frontline operation livesite, triage, DOTD practices, toolsets.
     RCA postmortem, RCA review, shortterm and longterm improvement (see other notes for more)
2. from hardware, datacenter design, bottom top to software layer
2.5. collect the history, and data and pattern from the hardware failure behavior, for later studies and improvements
3. EC schema; data placement, migration, continuous optimization; scrubbing
4. trade-off with cost, performance, energy, overhead
5. starting with storage trends: scale, reliability, more feature (big data, distributed fs, deeplearning GPU), cost (ec, cross site ec, etc), hardware change (flash, NVM, bigger mem/disk, faster CPU, FPGA, etc). we may hit architecture new generation, but that is very rare
   then we come to reliability
5.5 rollout, rollout, rollout, the rollout plan; the staging, canary, pilot, production. the binary rollout and runtime config enabling. always think about how to do roll back
5.6. code review, rollout plan review, etc. the peer review, get some seniors review it; they have experience to identiy potential bugs, or risks, or incompleteness in the plans. the rollout controller continuous monitoring & alerting & circuit breaker in the rollout process
5.7. scenario based testing. not only to catch all the functional correctness, but think about whether the behavior is proper in different scenarios.
5.7.5. separation of mitigation and root fix
5.8. identify the hot issues, keep tight control. e.g. the metadata server memory tight vs new code should avoid increase metadata memory otherwise need tight review; capacity pressure on stamps; rollout/new release hot issues tracking.
5.9. bug is killing reliability, no matter how well is the design. monotiring & alerting, log searching & debugging, diagnostics are playing key roles
6. check what I have on other notes
    1. shortterm and longterm fixes; prioritize; release blocking, cherry-pick or not
    2. customer focus, impact evaluation, serverity levels; stay online stay engaged
    3. software quality. code quality, readability, logging effectiveness (functional, status, performance tracing, background & variable printing), testing, dev decipline & CIT tests, 
    4. small improvements, doesn't need to new technology, new paper study; but a lot of small improvements continuously piled up. e.g. optimize repair/read priorities for GC vs customer reads, better timeout & throttling control, etc
       deliver new features, adoption of new technologies (FPGA, mem computing), architecture improvements, etc
6.5. the release management, as I can see on the release meeting notes. continuous delivery, fast iteration rollout, cherry-pick hot fixes, tracking issues. automated tests, unit, build verification, staging tests, simulated traffic, smoke, customer API, rollout test, buildout stress tests
     shortterm and longterm fixes.
7. high-level view of reliability
    1. customer facing issues
    2. the continous drop of customer impact incidents, customer complain incidents, the outage events, the VM restarts/glitches
8. from the google SRE book
    1. see the book
n. referenced materials
    1. other notes
    2. google SRE book
```

Notes 3

```
reliability outline
1. monitoring & alerting, livesite, continuous improvement, engineering practice; google SRE book
1.5. operation practice standarization, frontline / secondline / till dev livesite, triage, DOTD practices, toolsets.
     RCA postmortem, RCA review, shortterm and longterm improvement (see "other notes" for more)

5.7.5. separation of mitigation and root fix

5.8. identify the hot issues, keep tight control. e.g. the metadata memory tight vs new code should avoid increase metadata memory otherwise need tight review; capacity pressure on stamps; rollout/new release hot issues tracking.

6. check what I have on "other notes"
    1. shortterm and longterm fixes; prioritize; release blocking, cherry-pick or not
    2. customer focus, impact evaluation, Sev levels; stay online stay engaged
    3. software quality. code quality, readability, logging effectiveness (functional, status, performance tracing, background & variable printing), testing, dev decipline & CIT tests, 
    4. small improvements, doesn't need to new technology, new paper study; but a lot of small improvements continuously piled up. e.g. optimize repair/read priorities for GC vs customer reads, better timeout & throttling control, etc
       deliver new features, adoption of new technologies (FPGA, mem computing), architecture improvements, etc
6.5. the release management, as I can see on the periodical release meeting notes. continuous delivery, fast iteration rollout, cherry-pick hot fixes, tracking issues. automated tests, unit, build verification, staging tests, simulated traffic, smoke, customer API, rollout test, buildout stress tests
     shortterm and longterm fixes.
7. high-level view of reliability
    1. customer facing issues
    2. the continous drop of customer impact incidents, customer complain incidents, the outage events, the VM restarts/glitches
    3. the reliability related goals on each version release
8. from the google SRE book
    1. see the book
n. referenced materials
    1. "other notes"
    2. google SRE book

-----

5. starting with storage trends: scale, reliability, more feature (big data, distributed fs, deeplearning GPU), cost (ec, cross site ec, etc), hardware change (flash, NVM, bigger mem/disk, faster CPU, FPGA, etc). we may hit architecture new generation, but that is very rare
   then we come to reliability

5.7. scenario based testing. not only to catch all the functional correctness, but think about whether the behavior is proper in different scenarios.

5.6. code review, rollout plan review, etc. the peer review, get some seniors review it; they have experience to identiy potential bugs, or risks, or incompleteness in the plans. the rollout controller continuous monitoring & alerting & circuit breaker in the rollout process

5.5 rollout, rollout, rollout, the rollout plan; the staging, canary, pilot, production. the binary rollout and dynamic runtime config enabling. always think about how to do roll back

3. EC schema; data placement, migration, continuous optimization; scrubbing
4. trade-off with cost, performance, energy, overhead

2.5. collect the history, and data and pattern from the hardware failure behavior, for later studies and improvements

5.9. bug is killing reliability, no matter how well is the design. monitoring & alerting, log searching & debugging, diagnostics are playing key roles

2. from hardware, datacenter design, bottom top to software layer
```
