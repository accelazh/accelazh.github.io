---
layout: post
title: "A Summary of Cloud Scheduling"
tagline : "A Summary of Cloud Scheduling"
description: "A Summary of Cloud Scheduling"
category: "Scheduling"
tags: [cloud, scheduling, energy]
---
{% include JB/setup %}

### Real World Resource Utilization

To provide some background, [Quasar](http://web.stanford.edu/~cdel/2014.asplos.quasar.pdf) summaried quite a few real world statistics on datacenter resource utilization (I copied most of the text)

  * A production cluster at Twitter with thousands of servers, managed by Mesos over one month.

      * The cluster mostly hosts user-facing services. The aggregate CPU utilization is consistently below 20%, even though reservations reach up to 80% of total capacity.

      * Even when looking at individual servers, their majority does not exceed 50% utilization on any week. Typical memory use is higher (40-50%) but still differs from the reserved capacity.

      * Very few workloads reserve the right amount of resources; most workloads (70%) overestimate reservations by up to 10x, while many (20%) underestimate reservations by up to 5x.

  * A 12,000-server Google cluster managed with the more mature Borg system consistently achieves aggregate CPU utilization of 25-35% and aggregate memory utilization of 40%. In contrast, reserved resources exceed 75% and 60% of available capacity for CPU and memory respectively.

Twitter and Google are in the high end of the utilization spectrum. Utilization estimates are even lower for cloud facilities that do not co-locate workloads the way Google and Twitter do with Borg and Mesos respectively.

  * Various analyses estimate industry-wide utilization between 6% and 12%.

  * A recent study estimated server utilization on Amazon EC2 in the 3% to 17% range.

So overall, I can assume real world resource utilization is under 20%. That's low.

### The Goals of Scheduling

As mentioned in the previous summary of [Energy-aware Cloud Computing](cloud/A-Quick-Summary-of-Energy-Aware-Cloud-Computing), the root motivation of scheduling is to save the energy cost (almost account for 50% total spending including purchasing new machines). To improve resource utilization (or energy efficiency), scheduling needs to consolidate applications in less hosts. But that raises new questions about performance and QoS (Quanlity of Service) / SLA (Service Level Agreements) / SLO (Service Level Objectives). Below I summary the goals of scheduling

  * Server consolidation. Less machines, higher apps density, increased resource utilization, better energy-efficieny. Eventually less cost.

  * Improve the resource utilization. Higher resource utilization is more power efficent, and less waste of idle resources.

  * Ensure the QoS / SLA / SLO of applications. There are similar names. I will call it SLA below for consistency.

  * Improve the performance of scheduled appliactions by better placement

Those goals are inter-related. Also, basically, consolidating more apps in one host, increase the resource utilization, are by nature against application SLA. It's a consistent battle in the scheduling area.

Still, there can be other goals for scheduler, for example below. So keep minds open

  * [Tail latency](http://home.cse.ust.hk/~weiwa/teaching/Fall15-COMP6611B/reading_list/TheTailAtScale.pdf). By clever placing or duplicate partitoned tasks, the largest latency (tail latency) amount all the partitions is limited. Also, as it sees, latency can be a goal for scheduling.

### Complementary Parts of Scheduling

I actually understand cloud scheduling as three complementary aspects

  * The common sense scheduling. When tasks starts, scheduler finds it the best placement to run.
      
      * Examples: [Green Cloud](http://www.cloudbus.org/papers/Energy-Aware-CloudResourceAllocation-FGCS2012.pdf), [Paragon](http://web.stanford.edu/~cdel/2013.asplos.paragon.pdf), [Quasar](http://web.stanford.edu/~cdel/2014.asplos.quasar.pdf). And the schedulers in [Openstack](https://github.com/openstack/nova/tree/master/nova/scheduler), [Kubernetes](https://github.com/kubernetes/kubernetes/tree/master/plugin/pkg/scheduler), [Mesos](http://mesos.apache.org/documentation/latest/app-framework-development-guide/), ...

  * Continuous optimization. While tasks are already running, we can optimize its placement. The most common technique is live migration. Task can be moved/re-scheduled/re-started on another host. Monitoring is necessary.
      
      * Examples: [Openstack Watcher](https://wiki.openstack.org/wiki/Watcher), [VMware DRS](https://www.vmware.com/products/vsphere/features/drs-dpm)
  
  * Resource container (I conied this name). It works on the locally one host level. Ihe needs are two-folds, AFAIK much beyond Docker
      
      * For co-located critical and best-efforst (low priority) apps, we need a way to isolate their resource size, isolate their resource bandwidth, isolate their resource interference, and eventually isolate their performance.
      
      * Another aspect is, since workload is time-varying, the resource container needs to dynamically respond to expand/shrink its bubble. So that all idle resource leftover by critical apps can be utilized by best-effort ones.
      
      * Examples: [Google Heracles](http://csl.stanford.edu/~christos/publications/2015.heracles.isca.pdf)

The ideal is they co-work together as the complete cloud scheduling solution. In real world usually the later two are missing.

### The Factors of Scheduling

I try to summarize all the factors that scheduling should take into consideration. AFAIK, more factors are taken into consideration, more efficient is the sceduling.

First, the resource. It includes resource size, and resource bandwidth. The later is easier to ignore. [Google Heracles](http://csl.stanford.edu/~christos/publications/2015.heracles.isca.pdf) is a good reference. Container namespace isolation is just a beginning; CGroups doesn't provide full functionality.

  * CPU: Cpu cores, time quota, weight

  * Cache: L1/L2/L3/Last-level cache (LLC) (Intel CAT), TLB

  * DRAM: Memory size, memory bandwidth; also, NUMA and memory nodes

  * Persistent Memory: size, bandwidth; if added to the system

  * Disk IO: IOPS, request per second, disk bandwith

  * NVM: NVM/NVMe/SSD disks if you take them as more precious resource

  * Network traffic: packets per second, bandwidth

  * PCI bus: PCI bus bandwidth is a limited resource

  * Power: [power virus](http://csl.stanford.edu/~christos/publications/2015.heracles.isca.pdf) may lower down CPU core frequencies
  
  * GPU: to limit the size (cores? internal memory?) used, the bandwidth used, etc
  
  * More hardware (virtual) functions: e.g. compression card, Fathom GPU stick, etc

Another thing that is easy to ignore is 

  * Time varying. The actually workload is actually time varying, so as the resource utlization. Specifying how much an app needs by a constant template/manifest (as in Openstack, Kubernetes, Mesos) will always result in some internal leftover wasted.

      * Serverless, which by nature partitions app into short-lived tasks, may have the potential to cope with this problem.

Overall, resource interference is the major problem. [Bubble-up](http://www.cs.virginia.edu/~skadron/Papers/mars_micro2011.pdf) proposed a good method to model and measure resource interference, as used in [Paragon](http://web.stanford.edu/~cdel/2013.asplos.paragon.pdf)

  * To model resource interference, for an app
      
      * Tolerated: single benchmark for each type of resource, see how much of its stress will break app from its SLA. It reveals the different sensity of the app against each type of resource interference.
      
      * Caused: when app running on its SLA leve, how much stress it generates for each type of resource. It will act as the resource inteference on other co-located apps.

  * To meansure resource intference, use bubble-up
      
      * Tolerated: for each type of resource, slowly increase its benchmark stress, until the point where app just fails its SLA. Record down this point as the score.

      * Caused: let the app run at its just SLA point. Record down the resource stress it generated on each type.

[Paragon](http://web.stanford.edu/~cdel/2013.asplos.paragon.pdf) & [Quasar](http://web.stanford.edu/~cdel/2014.asplos.quasar.pdf) reveals that app preference contributes to a big part of scheduling efficiency, especially server config (i.e. (VM) hardware setup). They quckly profile the staged tasks before they go online, and use collaborative filtering to fill the missing columns.

  * Preference to resource interference. Different apps have different sensitivities towards types of resources.

  * Preference to server config. Server config may affact app performance significantly

      * It includes: CPU clock frequency, sockets, cores, L1/L2/L3 cache/LLC, TLB, memory, and the ages of server hardware, etc.

  * Preference to scale-out and scale-up. App performance may have different sensitivities towards each of them.

The next factor is app dependency. Apps usually depend on other apps to work. Their frequency of interaction and amount of traffic are asymmetric. Uniform scheduling is not appropriate here. The varying affinity between application leads to

  * Schedule by the traffic affinity between apps: frequency, bandwidth.

  * App co-location. Put highly affinited apps in one host, in one rack, under the same switch, or anywhere to shorten their network distance.

      * Related: Kubernetes "[Pod](http://kubernetes.io/docs/user-guide/pods/)", Netflix [Fenzo](http://events.linuxfoundation.org/sites/events/files/slides/Prezo-at-MesosCon2015-Final.pdf) for Mesos.

  * Cell architecture. Instead of putting all things into a very large cluster, we partition them into multiple Cells which are smaller. Usually we can partition them by user. Underlyingly, highly dependent apps are partitioned into the same Cell, and deployed co-locatedly.

      * Cell architecture also performs a way to solve cluster-is-too-large problem. Cell can be small enough to design and manage. Practically, the advocated linear scalability won't always work with cluster size infinitely large.

      * Examples: Cell architectures (by user) in internet companies: [\[1\]](http://www.infoq.com/cn/articles/how-weibo-do-unit-architecture)[\[2\]](http://www.infoq.com/cn/articles/how-weibo-do-unit-architecture)[\[3\]](http://www.infoq.com/cn/presentations/high-performance-services-practice-based-on-cell-architecture)[\[4\]](http://www.infoq.com/cn/articles/interview-alibaba-bixuan); Azure Storage [Stamp](http://www-bcf.usc.edu/~minlanyu/teach/csci599-fall12/papers/11-calder.pdf); Openstack [Nova Cell](https://wiki.openstack.org/wiki/Nova-Cells-v2).
  
  * Data locality. Put app (computing) closer to the data (to be computed). The concept is popularized since Hadoop & MapReduce.

Also, the different workload/task types should be taken into consideration. Here's the dimensions. Google [Omega](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41684.pdf) and [Borg](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43438.pdf) showed some aspects.

  * Service vs batch. Service are usually user-facing, latency critical, and high priority. Batch are usually Hadoop/Spark/etc, low priority and more flexible on time.

  * Short tasks and long jobs. Usually short tasks ang long jobs receive different treatments. And their flood in volume can be very differnet.

  * The flood-in volume. How many tasks come in per second, is it heavy load or lighter. This may leads to different strategies.

Community efforts are huge, but AFAIK there are still many missing parts.

### Methods of Scheduling

This is the most flexible part. It dependes on how the scheduler uses the factors above and decide its strategy. I summarized the a few that I know

  * Greedy. Filter the inappropriate hosts, find most suited, then schedule app on it. It's the most common method used, and usually effective enough.

  * Constraint equation. Treat the scheduling problem as solving the constraint equation. It can be used to express complex business rules.

  * Use of predictions. Machine learning and intelligent analytics are highly involved.

      * The model used can be simple linear functions, statistics models (PDF), or other machines learning algorithms (e.g. Collaborative Filtering in [Paragon](http://web.stanford.edu/~cdel/2013.asplos.paragon.pdf)).

      * The predicted can be workload pattern (e.g. [Netflix Scryer](http://techblog.netflix.com/2013/12/scryer-netflixs-predictive-auto-scaling.html)), app preference (e.g. [Paragon](http://web.stanford.edu/~cdel/2013.asplos.paragon.pdf) & [Quasar](http://web.stanford.edu/~cdel/2014.asplos.quasar.pdf)), placement distribution, possibilities of SLA violation, ... It is unlimited.

      * Meta of strategies. One scheduling strategy may not be suitable for all conditions. The scheduler can be equipped with many strategies and decide when to switch to what.

  * Proactive and reactive. Decide whether to reactive upon change or proactive act upon it results in different strategies, usually to cope with varying workload. An examples is [Netflix Scryer](http://techblog.netflix.com/2013/12/scryer-netflixs-predictive-auto-scaling.html).
  
  * The optimization problem. Treat the optimal allocation of resource as an optimization problem, and use gradient decent (e.g. [Google Heracles](http://csl.stanford.edu/~christos/publications/2015.heracles.isca.pdf)).

  * On-stage profiling. Before the app is scheduled online, we can first profile it on a few dedicate machines. After we know more about its preference, we can do better scheduling. See [Paragon](http://web.stanford.edu/~cdel/2013.asplos.paragon.pdf).

  * Combined with dedicate problem / usecase. For example [Mobile Crowdsourcing](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/icde16task-1.pdf). This may derive different algorithms.

There must always be new and better method and better ones. Stay tuned.

### Architectures of Scheduling

There are various of scheduling architectures on-going. Here's the [good reference](http://www.firmament.io/blog/scheduler-architectures.html) (and its [Chinese translated version](http://dockone.io/article/1113)).

  * Monolithic scheduler. A centric scheduler does all the thing, or copies of stateless schedulers sharing the same database. It is a common approach, and cope engineer complexity well. Most schedulers, as seen in Openstack, Kubernetes are like this.

  * Two-level scheduler. The Example is [Mesos](http://mesos.apache.org/documentation/latest/app-framework-development-guide/). It separates resource allocation and task placement. Usually the central scheduler hands out resource offers, and each app hooks in its second-level scheduler to do task placement.

      * Good sides: apps are easier to hook in their dedicate logic in the second-level scheduler. Resource offer is a new concept.

          * Most importantly, Mesos solves the static partitioning problem: Hadoop, Spark, Storm, etc each occupies their own pool of resource, each of them have their own schedulers. But, since the pool partitioning is static, Hadoop cannot borrow Spark's idle resource, neither vice versa. With Mesos, they share the same resource pool; Mesos acts as the datacenter-level resource scheduler.

      * Bad sides: the views of second-level schedulers are split. They cannot see global status, but only what is offer to them. Without global understanding, it is easy to make sub-optimal decisions, especially for co-located tasks.

          * There are works try to solves this for Mesos, for example [Netflix Fenzo](http://techblog.netflix.com/2015/08/fenzo-oss-scheduler-for-apache-mesos.html).
  
  * Shared-state scheduler. The example is [Google Omega](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41684.pdf). Schedulers share the state of the cluster. Copies of cluster state are independently updated by schedulers; they may conflict, thus needs optimistically concurrent transaction. An individual scheduler may be working on stale information, and may experience degraded performance under high contention.

  * Fully-distributed scheduler. Schedulers are distributed, no coordination in-between. Jobs can be submitted to any scheduler, and each scheduler may place tasks anywhere in the cluster. It is still academic. The problem is it is too hard to design a full-functional comprehensive scheduler in this way.

  * Hybrid scheduler. It tries to combine monolithic and shared-state schedulers, to solve the problem of fully distributed schedulers. For example, there are two scheduling paths: a distributed one for very short tasks or low-priority batch workloads, and a centralized one for the rest. It is still academic.
