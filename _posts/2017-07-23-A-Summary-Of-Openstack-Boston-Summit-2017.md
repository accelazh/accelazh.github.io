---
layout: post
title: "A Summary of Openstack Boston Summit (2017.4)"
tagline : "A Summary of Openstack Boston Summit (2017.4)"
description: "A Summary of Openstack Boston Summit (2017.4)"
category: "Openstack"
tags: [openstack, summit, summary, ceph]
---
{% include JB/setup %}

Large amount of videos about running Openstack with Kubernetes. Networking is still hot, NFV, VNF, SDN, tuning, etc; VNF needs realtime KVM, and run isolated with noisy neighbors. There are hypervisor based containers. People are sharing experience about KVM tuning, DPDK, Baremetal, Ceph, Nova Scheduler, and other things. Teams from the world are sharing how they manage Openstack deployment and operations. There are also a series of "Project Update - XXX" videos to catch updates from upstream. We have CephFS, DPDK, Neutron integration with OpenDaylight, Kuberntes and Container, better Baremetal now. People are trying to run Ceph (and other storage systems) on ARM.

__[Keynote: Superuser Announcement](https://www.youtube.com/watch?v=2_IyVQUgLww)__

  * Citynetwork: 27 datacenters of, 30,000 customers, 100% openstack, [link](http://superuser.openstack.org/articles/boston-superuser-awards-nominee-city-network/)
  * Snapdeal: 100M cpu hours, 700,000 instances, [link](http://superuser.openstack.org/articles/boston-superuser-awards-nominee-snapdeal/)
  * Paddy Power Betfair: 500 deployments a week, 100,000 cores, [link](http://superuser.openstack.org/articles/boston-superuser-awards-nominee-paddy-power-betfair/)
  * UKCloud: public cloud, for govenment usecases, [link](http://superuser.openstack.org/articles/boston-superuser-awards-nominee-ukcloud/)

[More info](http://superuser.openstack.org/articles/superuser-award-winner-boston/)

__[Keynote: Red Hat Sponsor Keynote](https://www.youtube.com/watch?time_continue=133&v=ViJYVjOj2zk)__

  * 2/3 deployments of openstack are in production. This keeps growing every year.
  * Top one reason of choosing openstack is to avoid vendor-locking
  * Openstack MOC (The Massachusetts Open Cloud), non-profit public cloud for research universities (MIT, Harvard, BU, NE, and UMass) and private sector partners in Massachusetts. See more at [[1]](https://www.openstack.org/summit/openstack-summit-atlanta-2014/session-videos/presentation/the-massachusetts-open-cloud-moc-a-new-model-to-operate-and-innovate-in-a-vendor-neutral-cloud)[[2]](https://www.openstack.org/assets/presentation-media/MOC-OpenStack.pdf)
  * Ceph, future plans to increase capacity to 20PB
  * Containerized using Kubernetes. Openstack + Container.
  * GPU

[Openstack User Survey 2017 Boston](https://www.openstack.org/assets/survey/April2017SurveyReport.pdf)

  * Surveyed user dropped slightly from 1533 April 2016 to 1305 April 2017. But there are more deployments.

__[Keynote: Managing Kubernetes on OpenStack at Scale (eBay)](https://www.youtube.com/watch?v=3OuyLlPrpy0)__

eBay heavy user of openstack sharing experience here. There are Federation and GPU.

__[Keynote: Costs Less, Does More](https://www.youtube.com/watch?v=fY4nLcMuoJg)__

General keynotes and community status.

__[Keynote: Interop Challenge](https://www.youtube.com/watch?v=nBXXLNIwAoo)__

Interop by different vendors and from different geo-locations. Deploy kubernetes. A sql database horizontal scalable and self-healing, cockroach cluster.

More and more people are using CockroachDB now. And also TiDB, they are building something like an opensource Spanner. And nowadays DBs are moving from NoSql to Sql again.

This video is promoting CockroachDB too. No matter whether openstack is going to keep thriving or supressed by container, it is the big stage for new promising opensource softwares to get known and gather heat. Previously we see Ceph, now we see CockroachDB.

__[Keynote: Home of Open {Composable} Infrastructure](https://www.youtube.com/watch?v=_KIkp9pzToA)__

Composable and cloud native, key to build things thriving on openstack. Openstack problem: complexity.

__[Keynote: Taking OpenStack Out to the Network Edges](https://www.youtube.com/watch?v=Q-LukNfu2L0)__

Edge computing. We are collecting too much data to all be sent to central public/private clouds, so we compute at edge. Openstack in a hardware box (like a router), containerized and minimized the footprint. They can use the same management tools across the entire network, scale up to thousands/millions of nodes, deliver applications to any remote sits, and the virtual network services.

Good talk, very interesting. Openstack in a box or at central can be used as the unified central management tool for remote IoT + central cloud. Edge computing, a paradigm useful in big data, is also combined with this paradigm.

This video is mainly delivering VNFs. If they are wify routers, I wonder the overhead of running openstack in routers. And usually routers use specially designed hardware, while openstack usually runs in general purpose linux env (and needs python).

__[Keynote: Democratizing Robotics - Origami-Inspired Printed Robots](https://www.youtube.com/watch?v=3AmcRcogvgs)__

Everyone can made a robot, in future. Robot compiler. Robot spider. 3D printed parts. User specifiy key components, the compiler generates the remaining wire works.

__[Keynote: Mirantis Sponsor Keynote](https://www.youtube.com/watch?v=GM7l-M9WxeY)__

As Mirantis suggests: Managed Open Cloud must be built following the vertical design pattern of public clouds. NOT be stitched out of "enterprise software".

The addressed problem is: each opensource softwares at each layer are trying to enter other markets and promote their own end-to-end solution. So they don't work well when together. Public cloud, like AWS, however, ensure they build each layer vertically to work together. So customers are happy.

Also, public cloud continuously deliver each layers and components with locked version. Opensource cloud however deliver different versions on different components. They have version mismatch problem, need effort to smooth new verisons co-working, and more importantly, they cannot get the benefit of new version immediately when it comes out (because other components are still in old versions), compared to public cloud.

Mirantis have accumulated a lot of experience of composing and selling opensource software in enterprise market. Things are not instinctively simply what opensource community commonly speaks.

__[Keynote: The US Army Cyber School - Saving Millions & Achieving Educational Freedom Through OpenStack](https://www.youtube.com/watch?v=f5MRdaM-E0g)__

Use in education. Individuals don't need to buy their own devices again.

__[Keynote: Mark Collier Q&A with Edward Snowden](https://www.youtube.com/watch?v=DIxvFuKY0KM)__

You are sinking cost to a infrastructure that are not yours (online services like Facebook). Investing to openstack, the layers and knowledges are still in the control of you.

On public cloud or on the phone, user can never make sure their information are not leaked, e.g. to FBI, or GPS is not actually turned-off in flight mode. Snowden team are developing something that everybody can use and to inspect it from circuit electron level.

__[Keynote: Kubernetes and CockroachDB](https://www.youtube.com/watch?v=PIePIsskhrw)__

Scalable SQL with self-healing. In containers with Kubernetes.

__[Keynote: Deploying Cinder as a Stand-Alone Service Using Containers](https://www.youtube.com/watch?v=4yjhIoTRuXw)__

So, finally Cinder wants to get out of Openstack; like EMC ViPR, an independent storage controller. The large amount of vendor drivers which Cinder accumulated are great wealth.

This is a demo.

__[Keynote: Unified Platform VMs, Containers, Bare Metal](https://www.youtube.com/watch?v=o1RgIK1N4mo)__

Openstack, the unified control plain for VM, container, baremetal, is powerful. This is a demo. Why everyone doing a demo is using their own UI web portal rather than Horizon.

__[Keynote: Live Demo- Just Ironic and Neutron](https://www.youtube.com/watch?v=08JZZtFLZ3k)__

SDN for baremetal is useful. This is a demo.

__[The Design & Architecture of CockroachDB](https://www.youtube.com/watch?v=p8aJuk7TJJA)__

Simple introduction to CockroachDB. They use Raft paxos per table range. There are basically two ways to do write replication:

  * One primary secondary and thirdary, in which the ordering ensures replication consistency; the ordering info is stored in an external paxos system; examples is Ceph 
  * Write replication by paxos quorum; Amazon Dynamo is something like it, Google Metastore uses paxos for write replication, [AWS Aurora MySQL](http://www.allthingsdistributed.com/files/p1041-verbitski.pdf) is also using quorum based writting.

The essence of distributed system is replication, the essence of replication consistency is paxos. Paxos is everything in distributed systems. There is another video about running the team of CockroachDB, see [link](https://www.youtube.com/watch?v=pFKrRF_sflE).

__[Verizon Product Case Study - OpenStack at the Edge](https://www.youtube.com/watch?v=WbeLMhcrkz8)__

Linked from [Keynote: Taking OpenStack Out to the Network Edges](https://www.youtube.com/watch?v=Q-LukNfu2L0). Massively distributed Openstack in central and edge networks. (Edge Computing looks increasingly hot these days.) Unified management across the network, ability to move workload around, seamless customer experience, and deliver new services quickly. Cloud favors its agility and profitable by scale, but distant network latency is not something we can overcome, so we need edges.

__[Can OpenStack Beat Amazon AWS in Price? Augmented!](https://www.youtube.com/watch?v=0FXbeA-zI0M)__

The Openstack VMs don't include SSD. Openstack prices are significantly lower than AWS. (But Openstack doesn't provide you ready-to-use services like DB, hadoop.) The video is OVH. It is 20% ~ 30% cheaper than AWS. AWS also charges for API call request, besides the charges for bandwidth, compute, and storage.

__[Ceph Project Update](https://www.youtube.com/watch?v=NqOFWGUvA9A)__

New coming features in Luminous. Ceph releases by every 6 months. BlueStore is stable and default for OSD. BlueStore is fast on both HDD (~2x) and SSDs (~1.5x). RBD has EC 2+2, 4+2. Large writes faster than replication because of less IO to device. All writes update a full stripe. Ceph-mgr is adding more features. Ceph-mon now can scale to 10K OSDs. Ceph now have RDMA backend and DPDK backend.

Two imbalance problems are fixed, and Ceph finally has perfectly balanced OSDs. Long years after CRUSH paper, there are still issues can be fixed on production. Ceph can also explicitly map PGs to specific devices. There is a simple offline optimizer to balance PGs. Hash-basd approach, compared to metadata approach of data placement, imbalance and anomaly in weighted placement is practical a issue.

One big thing is the RGW metadata search, boosted by ElasticSearch. RGW is receiving more and more attention as Ceph grows. Same with the object storage market. RGW has more work on data tiering, deduplication, multi-site federation, etc. Erasure coding is important for RGW. It now has NFSv4 gateway, inline compression, and encrypytion. It has dynamic bucket index sharding finally now.

There are improvements on RBD mirroring, as cooperative HA daemons, and also integration with Cinder. Librbd now supports ISCI with full feature set.

CephFS supports multiple active MDS daemons now. Subtree can be pinned on specific daemon. There are a lot of bug fixes and tests.

What is after Luminous? OSD refactor, Peering Optimization, BlueStore, QoS (dmclock distributed QoS queuing), Tiering, Multi-site federation, Dedup, Self-management (auto CRUSH optimization, steer IO away from slow/busy devices), Metrics, Client-side caches, better performance, run on ARM, etc. Verison Mimic.

The community is quickly growing, more than 3x from 2015 to 2016. China is the major contributor behind it.

__[Project Update - Cinder](https://www.youtube.com/watch?v=EpxnsqIBkOI)__

Yet more new drivers are added to Cinder (the amount of drivers are great wealth). Consistency Groups (CG) are migrated to [generic volume groups](https://specs.openstack.org/openstack/cinder-specs/specs/newton/generic-volume-group.html) (GVG). Group replication is useful for database safety. Multiattach support is being improved. Active-Active HA is already in Cinder services; need to add driver support for it. Cinder uses tag "assert:supports-rolling-upgrade" to show the project supports minimal rolling upgrade capabilities. There are many more features and enhancements. Besides, Cinder is now an independent service which can run without Openstack. Cinder has more potential beyond. There are many discussions on [PTG](https://wiki.openstack.org/wiki/PTG/Pike/Etherpads) (Projects Team Gathering). Link to [Cinder PTG](https://etherpad.openstack.org/p/ATL-cinder-ptg-planning).

__[OpenStack Acceleration Service- Introduction of Cyborg Project](https://www.youtube.com/watch?v=sEBSL2sbeZk)__

To provide a management framework for dedicated devices (e.g. FPGA, GPU, NVMe SSD) as well as various accelerators (e.g iNIC, ip-sec card, dpdk) in OpenStack, in addition to Nova. The case Cyborg targets is vital for HPC cloud implementation which usually requires a lot of such devices/accelerators, especially FPGA and GPU cards. Public and NFV cloud implementation also has similar requirements. Good catch to the new hot trends.

GPU can be used in Openstack by KVM in PCI-passthrough mode. Cyborg attach drivers to Nova to provide placements for hardware accelerated hosts. It uses agents on compute nodes to collect data. There are more future works.

__[Nutanix - Cloud Builders Wanted - OpenStack on Nutanix Enterprise Cloud](https://www.youtube.com/watch?v=INA8Ha4H2qE)__

Hybrid private and public cloud. Offload to public. All features and deployment ready to use.

__[Discover All-Flash Ceph for High Performance Storage Pool](https://www.youtube.com/watch?v=fIf8c3Kez9M)__

By Intel and QCT. 4K random read 1.5M IOPS with 2ms latency. Tuning by software + NUMA CPU pinning.

__[Red Hat - Deterministic Storage Performance- 'The AWS Way' for Capacity-Based QoS with OpenStack and](https://www.youtube.com/watch?v=4V8ZTCBb2iE)__

Comparing AWS and Openstack Cinder volume models. Adding more volumes, after certain limit, will slow you down however. Instead, we can scale the "hight" of volumes instead of adding more. More small volumes with low iops, less large volumes with high iops. Even one volume per OSD.

__[Cloud Native Computing with Kubernetes and OpenStack](https://www.youtube.com/watch?v=C2kuaqcxrJ8)__

Google introducing Kubernetes and its philosophies.

__[Designing Cloud Native Applications - Deep dive](https://www.youtube.com/watch?v=aJq9KwVcMjc)__

Rest API + Micro Services + Message Queue. Sharing the patterns in cloud native application. Good to use as a reference.

__[Experience with DPDK Troubleshooting](https://www.youtube.com/watch?v=BEXwaf5IPhk)__

DPDK is quickly being adopted in the opensource world (as well as the industry). Now all kinds of stuff provide integration with DPDK. SSD requires more network performance. That's one of the reasons behind DPDK. Journey from VIRTO to DPDK: SR-IoV, PCI Passthrough. Hardware tuning. Troubleshooting. Etc.

__[OpenStack Ironic - features, scalability, performance, use cases and future with Intel's RSD](https://www.youtube.com/watch?v=ACr2Aq4dhyk)__

There are a bunch of improvement in Baremetal last year. The biggest ones are in network. Using Baremetal, there is no virtualization overhead, no noisy neighbor issue, direct access to low level hardware optimizations, and no issues with haredware not fully supported by virtualization. Baremetal has torrent based image delivery. Video by Intel RSD (Rack-scale Design).

__[Building and Operating an OpenStack Cloud with a Small Team](https://www.youtube.com/watch?v=2jjNdLAzWPU)__

Openstack is just a bunch of servers, with network services, and storage. Instead of call everything to opentack team, you can escalate them to other normal op teams for handling. E.e. if DB is going wrong, find a DB team member. There are other experiences shared.

__[Managing Local Storage with Kubernetes](https://www.youtube.com/watch?v=GAuWDeaVjng)__

Introducing how to use persistent volume in Kubnernetes.

__[Storage Capabilities in Cinder](https://www.youtube.com/watch?v=3Q5ChDYdlxI)__

Introducing what Cinder can do. More than 100+ volume drivers. Volume migration and Retype. Volume-backed image. Image volume cache. Replication. Generic volume groups. Backup and restore. 

__[OpenStack and OpenDaylight- An Integrated IaaS for SDN and NFV](https://www.youtube.com/watch?v=g5I7V5di--M)__

OpenDaylight is the general controller for many usecases, Edge Services, IP Routing, Optical Transport, DC Fabric, DC Overlay, vCPE & VAS Orchestration. OpenDaylight can be the SDN controller for Openstack. The later half of this talk introduces how OpenDaylight works. OpenDaylight NetVirt supports services like L2, L3, BGP, L3VPN, EVPN, ACL, DHCP, QoS, SFC, IPv6, L2GW. It supports OpenFlow and OVSDB based devices. There is plan to integrate with Kubernetes too. OpenDaylight is quick growing and being adopted in Openstack these days.

__[Cloud Wars! Public vs Private Cloud Economics](https://www.youtube.com/watch?v=oYK9y8rEhKI)__

From Ubuntu Canonical. Public cloud, you pay for the reservation, not how much you use.　Ｆｏｒ resource usage prediction, 1 VM is hard to predict, but many VMs together makes the curve smooth; so even private cloud with more VMs can predict usage. When started using, many peripheral services such as deployment, monitoring, tuning, load balancing, are also needed to buy. The gravity sucks money. And as grows the data, which also needs more and more money to host. The usecase is showing that after certain deployment scale, public cloud cost overruns on-premise.

__[OpenStack and Kubernetes- Combining the Best of Both Worlds](https://www.youtube.com/watch?v=NDOQMhIBWCw)__

A panel discusssion.

__[Cinder- It's Not Just for Secondary Attached Storage Any More!](https://www.youtube.com/watch?v=wgzkMLs2U_M)__

Besides for Nova instance, Cinder can be used as Glance backend (boot from volume), for container volumes, and outside Openstack. Cinder can now be run as an independent service beyond Openstack.

__[Being a Project Team Lead (PTL)- The Good, the Bad, and the Ugly](https://www.youtube.com/watch?v=2k6OSSca5zw)__

PTLs are moderators and liaisons. Besides code review, PTLs also ensure the gate isn't broken, nominate cores, organize PTGs, liaise with projects, triage bugs, run meetings, organize bug smashes, ensure stable isn't broken, release libraries, monitor mailling list, draft release notes, etc. The biggest requirment of PTL is having enough time to work upstream. PTL is the front-face of the project, and the go-to guy.

The bad side of PTL work can be many. Bureaucracy needs PTL to keep up the many threads of execution, like project govenance changes, interop working group, initiatives in other projects, release management, vulnerabilities, roadmaps, etc. The workload is high, as for PTL, disconnect is hard, put out fires, work like herding lots of cats, growing backlogs, and release crunch time. Things can go beyond scale of human proportions, like email inbox explosion, gate queue explosion, bug backlog explosion. It is hard to motivate people to care about bug triage, test coverage, team meatings.

The ugly sides can be, manageing expectations, contributors may repect PTL, and PTL also needs to justify upstream time to employer. Managing upstream releations is also hard, PTL needs to avoid disconnect with other PTLs, or with former/future PTLs. The team dynamics part, as PTL has to tackle with growing/contracting the core team, having to kick/ban people from IRC, can be PTL of a project of poor reputation.

As time grows, PTL work can make more of the good, keep level of the bad from growing, and reduce the amount of the ugly.

__[Unlocking the Performance Secrets of Ceph Object Storage](https://www.youtube.com/watch?v=BHGjvEo4dag)__

By QCT, to optimize the Ceph running. Architecture demensions: object size, object count, data protection, bucket indexes, caching, server density, client to rgw/osd ratio, price/performance.

Conclustions (12-Bay, 35-Bay are standard density and high density hosts, each with 12x or 35x HDDs per node)
  * #1 - optimizing small objects (OPS): 12-Bay OSD hosts, bucket indexes on SSD (improves the results a lot), 10GbE fabric.
  * #2 - optimizations for high objet density (100M objects: 210 OSDs): 35-Bay OSD hosts (prices/perf), Intel Cache Acceleration Software (Intel CAS) (just metadata caching), metadata is cached (many dentry and inodes taking kernel memory; CAS + metadata cache improves ~500% read perf, ~400% write perf), 40GbE farbric.
  * #3 - optimizing large object throughput (MBps): 12-Bay OSD hosts, 10GbE - Perf; 35-Bay OSD hosts, 40GbE - Price/Perf; Tune RGW chunk size to 4MB (so less small IOs); 40% performance boost. Higher performance could be achieved by adding more hosts.
  * #4 - optimizing RGW to OSD ratio: 1 RGW host per 100 OSDs (100% 32M write); 1 RGW host per 50 OSDs (100% 64K write). 

See this [page](https://youtu.be/BHGjvEo4dag?t=44m22s) for summarized optimizing takeaways. The most eye-taking part is Intel CAS + filesystem metadata cache achieves 400% ~ 500% IOPS improvement.

__[Optimized Workload Placement Using a New Batch Scheduling Algorithm](https://www.youtube.com/watch?v=rhw8e0itCRA)__

From Lenovo. By batch we can do better scheduling decision, instead short-sighted greedy come and place. The placement workload is multi-dimensional: RAM, CPU, Storage, NUMA, CPU-Pinning, SR-IoV VFs, SSD, Affinity, Anti-affinity, Cost (Energy saving), Thermal. Implementation options are: Heuristic algorithms (most-loaded first, least-loaded-first); Genetic algorithms; Simulated annealing algorithms. The ifnal choice is the Genetic alogrithm. Genetic algorithms perform better than others. Dynamic workload redistribution is planned to be integrated with the Watcher project.

__[Real Time KVM and How It Works](https://www.youtube.com/watch?v=x5Q6RXP6Kdk)__

Motivations: VNF applications require predictable and fast performance. On a 25 Gb/s interface, 48,000 64-byte packets take 1ms.

Hardware CPU & NIC considerations. By CPU E5-2600 v4 or after. So that Intel CAS can help allocate and protect L3 cache. Also OPNFV [KVM4NFV](http://artifacts.opnfv.org/kvmfornfv/docs/all/all.pdf) required BIOS setting, VT-d, interrupt [SMI](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_MRG/1.3/html/Realtime_Reference_Guide/sect-Realtime_Reference_Guide-Hardware_interrupts-System_management_interrupts.html) iLO sub-OS. More info at [video 8m9s](https://youtu.be/x5Q6RXP6Kdk?t=8m9s). Understanding [VMExits](https://software.intel.com/en-us/blogs/2009/06/25/virtualization-and-performance-understanding-vm-exits).

The main aim of [PREEMPT_RT](https://wiki.linuxfoundation.org/realtime/documentation/technical_details/start) patch for linux kernel is to minimize the amount of kernel code that is non-preemptible: High resolution timers, Sleeping spinlocks, Threaded interrupt handler, rt_mutex, RCU. Prority inversion problem of a high priority process is that, a low priority process blocks critical resource, such as a spinlock or RCU.

Cyclictest is a high resolution test program for realtime linux kernel. You set a time which fires every 10ms, and then the guy who is the process that gets woken every 10ms. You can do this in a VM to see whether it is like (bad case) 11ms, 9ms, 8ms, 10ms, 12ms, .. Also, you can run other high load VMs in Openstack to content with the realtime one. A perfect one should be 10ms, 10ms, 10ms, ..

Flavor settings: hw:cpu_realtime=yes. hw:cpu_realtime_mask=^0, which means vCPU0 is reseverved for non-RT usage. The flavor should have at least 2 CPUs. Besides, you should have VM tuned for NUMA, you have CPU isolation, you got [hugepages](http://dpdk.org/doc/guides/linux_gsg/sys_reqs.html) because you use DPDK. More tricks to optimize performance: CPU pinning, Passthrough, CPU isolation, [NoHZ](https://www.kernel.org/doc/Documentation/timers/NO_HZ.txt), [NoRCU callbacks](), etc.

"We did this exercise at the NFV meeting back in September at Red Hat and all the NFV SMEs agreed we need [RT-KVM](https://lwn.net/Articles/656807/) for [C-RAN](https://en.wikipedia.org/wiki/C-RAN) use case. However, we have discovered that using RT-KVM along with OVS-DPDK provides Zero-packet-loss."

Interesting talk.

__[Real Time KVM with DPDK - HOWTO and Results](https://www.youtube.com/watch?v=o-AFD7vbSWc)__

The howto guide of the above talk.

__[Facing The Public- What's Still Missing from OpenStack for Public Cloud Operators?](https://www.youtube.com/watch?v=CfQ0qEIuOQ4)__

A magic layer on top of openstack to enable it as a public cloud. Talk from people working at OpenStack cloud providers at Europe.

__[Lessons Learned from Running 1000 Application Deployments a Day on OpenStack at Paddy Power Betfair](https://www.youtube.com/watch?v=0PlPJG-xuHw)__

The talk covers experience from their openstack continuous delivery, how to run team, a series of design decision they did in running Openstack. (Besies, they are using Red Hat Openstack Director.) They also share the various issues fixed during running Openstack.

__[How Ceph Performance in an ARM-Base Microserver Cluster](https://www.youtube.com/watch?v=4rY3yrE2ysQ)__

People are trying to run Ceph (and other storage systems) on ARM. There is also a [Redis on ARM](https://redis.io/topics/ARM). Ambedded Technology offers storage servers on ARM. And the solution to Ceph.

Problems in Ceph

  * One server failure causes many OSD down
  * CPU utility is only 30%-40% when network is saturated. The bottleneck is network - not computing.
  * The power consumption and thermal/heat emitted. You pay much and you pay twice.

The solution

  * One board 8 servers, each one for one OSD (Micro server). (But you have more servers, so higher probably to fail any each?) 8 * SATA3 HDD/SSD + 8 * SATA journal SSD.
  * 2.5Gb * 8 links as the backend links across ARM servers. Two in-chassis switch each of 10Gb * 2. 8 the above single OSD ARM servers connected by on chassis.

I think the advantage is 8 OSD servers in one chasis, so interconnect network can be of high bandwidth.

Interesting talk.

__[CephFS Backed NFS Share Service for Multi-Tenant Clouds](https://www.youtube.com/watch?v=BmDv-iQLv8c)__

Using NFS Ganesha with CephFS in Manila. There are several solutions, each with likes and dislikes.

__[OpenStack + Kubernetes + HyperContainer = The Container Platform for NFV](https://www.youtube.com/watch?v=dATYAyVTdtU)__

From Harry Zhang, member of Hyper. Hypernetes (h8s) creates hypervisor-based containers (HyperContainer) directly on physical servers instead of wrapping containers inside VMs. Comparing to OS containers, kernel features of this HyperContainer is completely isolated from "noisy neighbors" but still have all benefits of cloud native deployment (e.g. Docker image, container api, sub-seconds spawn, etc).

Hypercontainer. Hypervisor runtime, [RunV](https://github.com/hyperhq/runv), ompatible with OCI. Interesting talk.

__[Accelerating Ceph Performance with High Speed Networks and Protocols](https://www.youtube.com/watch?v=anBMPY6iTIU)__

From Mellanox. High performance networks now able to reach 100Gb/s along with advanced protocols like RDMA. Also, Mellanox ConnectX-5 can do earsure coding offload for CPU.

__[Ceph Snapshots for Fun and Profit](https://www.youtube.com/watch?v=rY0OWtllkn8)__

Briefly overview how snapshots works and discuss their implications. Snap trim tunables: hammer.

__[OpenStack Virtual Machine Quickly Available in One Second](https://www.youtube.com/watch?v=C7VBHW2uaMs)__

From Chinac.com 华云数据. The OS boot in a new VM take time; to cope with it, we copy new VM from an existing one. Save Base VM as VM Stat; when creating new VM, we live upgrade cpu/mem/storage/NIC etc, upgrade guest info, including password, username NIC MAC etc. To cope with libvert, we also need to rewrite vm stat header to the new VM's. And a lot of other injections and rewrites for data consistency.

Interesting talk. Basically it implements fast VM boot in libvirt. See [16m34s](https://youtu.be/C7VBHW2uaMs?t=16m34s) for summary of overall workflow.

__[Turned Up to 11- Low-Latency Ceph Block Storage](https://www.youtube.com/watch?v=hFkPgKBqwvw)__

Client-side in-memeory caching. RBD cahcing. Persistent RBD cache. Flash-based read/write caching. PR#14629. This is practically very useful for Ceph.

__[Optimizing Ceph Performance by Leveraging Intel(R) Optane(TM) and 3D NAND TLC SSDs](https://www.youtube.com/watch?v=AFTsQAYyEiQ)__

38x improvement on Ceph 4KB random write on SSD, 71K IOPS in the end, see [9m36s](https://youtu.be/AFTsQAYyEiQ?t=9m36s). Intel sharing Ceph on 3D XPoint (device named Optane). 3D XPoint performance review [article](http://www.anandtech.com/show/11209/intel-optane-ssd-dc-p4800x-review-a-deep-dive-into-3d-xpoint-enterprise-performance), which says 500K 4KB IOPS. The test configuration has 8 ceph nodes, only 71K IOPS? Read is ~3M IOPS.

Tuning summary. There are a series of tuning on WAL, rocksdb compact, ceph cpu.

  * Good node scalability, bad disk scalability, for 4KB block workload. CPU throttled.
  * NUMA helps a lot on performance
  * Fine tune the number of OSD per node and driver per node.

Intel 3D NAND SSDs and Optane SSD have different products/configs for capacity-favoring and performance-favoring.

__[OpenStack on Kubernetes- One Year After](https://www.youtube.com/watch?v=hiepQrynsig)__

From Intel. Managing Openstack lifecycle with ease on Kubernetes. Nova-kubernetes-drain, making openstack aware of kubernetes deployment, implemented as lifecycle hooks. Talking about improvements in the Openstack deployment. 

__[Verizon Case Study- The Illusion of Infinite Capacity](https://www.youtube.com/watch?v=JsjO7KtTahU)__

The total cost of ownership for an OpenStack private cloud can be half of other infrastructure alternatives. The key to achieving such a goal is to capture relevant metrics and watch them closely. Such metrics become new word KPIs in the enterprise; it is these metrics that support the evolution for cloud services to becoming mission critical. Allowing such metrics to manifest as KPIs in pleasant and intuitive ways encourages good behavior of tenants and their supporting business unit as the business maximizes the potential of the investment.

At scale, this can be realized with real-time dashboards, self-service workflows, tools to assist in right-sizing resources, and reporting for operators, financial managers, and executives. Tenants need cost estimates for budget forecasts, while executives need chargeback data to justify additional investment in the OpenStack environment.

__[Security Hardening- PCI DSS and Security Compliance within Keystone](https://www.youtube.com/watch?v=dz7wRzxUBds)__

PCI DSS - Payment Card Industry Data Security Standard. There various detailed requirement lines for Keystone to meet. At begining, Keystone is simple, but now it becomes more and more comprehensive and satisfying more and more enterprise needs.

__[Multi-Site OpenStack- Deployment Options and Challenges for a Telco](https://www.youtube.com/watch?v=ozayFsofI1w)__

Telco needs openstack multi-site; they have many sites and edges to manage (detailes see [6m33s](https://youtu.be/ozayFsofI1w?t=6m33s)). Many usecases are shared in this talk. Useful to watch if interested. Indeed Telcos like Verizon, China Mobile, Huawei, etc are using multi-set a lot.

__[Terraforming OpenStack Landscape](https://www.youtube.com/watch?v=XaNUCGOpC00)__

From Mirantis. IaC (Infrastructure as Code) + Openstack. Using Terraform tool.

__[Advanced Tuning and Operation Guide for Block Storage Using Ceph](https://www.youtube.com/watch?v=gp6if858HUI)__

Tuning CRUSH, now ceph supports straw2. Cinder has active-active setup. Volume migration backed by Ceph. Volume replication by Ceph RBD mirroring. Tips & tricks.

__[Growing the Next Generation of OpenStack Contributors](https://www.youtube.com/watch?v=mCdUazLl0-4)__

A panel discussion.

__[The Past, the Present, and the Future of OpenStack Interoperability](https://www.youtube.com/watch?v=IrQnhnX38Js)__

Another panel discussion.

__[Manila on CephFS at CERN- The Short Way to Production](https://www.youtube.com/watch?v=6mbng-NPGAw)__

The OpenStack and Ceph teams at CERN have recently added Manila/CephFS to their service catalogues. CERN is running a 190K core OpenStack deployment and a 12 PB Ceph cluster.

__[Talk From The Trenches- Will Containers Save Us?](https://www.youtube.com/watch?v=n0OjuBxdg5c)__

Given the rate of adoption of container based infrastructure platforms, will there be a second renaissance for OpenStack? A panel discussion by two persons.

__Other summaries__

  * [2017 OpenStack Summit 网络性能篇](https://zhuanlan.zhihu.com/p/27126974)
      * Hybrid Messaging Solutions for Large Scale OpenStack Deployments. Interesting.
      * Saving up to 98% Time Updating Firewall Using Netlink. 98% saving.
      * Serverless Network Services in OpenStack and Data Centers. Mellox Smart NIC.
      * Maximizing Hardware - Server Simulator. Testing using few hardwares to sumilate large environment.
  * [2017 OpenStack Summit day Baremetal篇](https://zhuanlan.zhihu.com/p/27174508)
      * Ironic new features: RedFish, Driver Composition, VIF Interface Attachment, Rolling Upgrades, Boot From Volume.
  * [OpenStack波士顿峰会Day1](http://www.sdnlab.com/19184.html)
  * [OpenStack波士顿峰会Day2](http://www.sdnlab.com/19192.html)
  * [OpenStack@波士顿 Day3 风景这边独好](http://m.yopai.com/show-2-218938.html)
  * [OpenStack@波士顿 Day4 用优秀案例回馈社区](http://www.sohu.com/a/139949497_740446)
  * [OpenStack波士顿峰会：第二代私有云如何理解？](http://www.sohu.com/a/139332099_123058)

