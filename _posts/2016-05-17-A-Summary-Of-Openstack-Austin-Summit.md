---
layout: post
title: "A Summary of Openstack Austin Summit"
tagline : "A Summary of Openstack Austin Summit"
description: "A Summary of Openstack Austin Summit"
category: "Openstack"
tags: [openstack, summit, summary]
---
{% include JB/setup %}

To give a summary of Openstack Austin Summit:

There are no much news on Cinder ([features](https://www.youtube.com/watch?v=pVvzn_bSDtY) are being developed but a bit routine). Manila becomes mature (and gets more exposure) now. Multi-site openstack is receiving increasing weight (from Cell V2, Ceph & Swift, backup/DR, to deployment practices).

Ceph [Jewel](http://ceph.com/releases/v10-2-0-jewel-released/) release is remarkable (CephFS [production-ready](http://thenewstack.io/converging-storage-cephfs-now-production-ready/), [RDB mirror](http://docs.ceph.com/docs/master/rbd/rbd-mirroring/) available for journal replication). NVM/SSD technologies are game-changing (NVMe Ceph journal, XtremIO, etc). DPDK are quickly getting adopted (in OVS, NFV, [monitoring](https://www.youtube.com/watch?v=BdebhsBFEJs)).

[Kuryr](https://github.com/openstack/kuryr) or container overlay network doesn't have much progress (looks like). Neutron keeps improving DNS, Baremetal support, IPAM, and NFV/VNF. For SDN part, OVN ([vs Dragonflow](https://www.ustack.com/blog/neutron-dragonflow/?print=yes)), Opendaylight integration, and Dragonflow are progressing. Service Function Chaining (SFC) (and Tacker) is coming to shape. Networking, NFV, SDN, service chaining, and various solutions & vendors, are still the most active part of Openstack.

IoT becomes hot (SAP, IBM, HPE, Pivotal, TCP Cloud, SmartCities). IBM is [betting](https://www.youtube.com/watch?v=ib3vsxc_wWk) on Openstack. [Mirantis](https://www.mirantis.com/) is gaining increasing weight (and respect) in community. [Ubuntu/Canonical](http://www.canonical.com/) is rising (they have so many presentations). Openstack Foundation is spending increasing effort on training activities, including the new Certificated Openstack Admin (COA) (99Cloud [supports](http://www.51ecs.com/3954.html) it in China), in preparation to become the true industry standard. Besides, this Summit has a new [Superuser TV](https://www.youtube.com/results?search_query=superuser+tv&page=1) series. 

Containers are of course hot, but most of them are supported via PaaS (rather than directly through Openstack) ([Murano vs Magnum](https://www.youtube.com/watch?v=Su4X2w-X-IE)), or used for containerized Openstack deployment (Kolla, Ansible + container, [run on Kubernetes](https://www.youtube.com/watch?v=e-j9FOO-i84), etc). OCI & CNCF are still working hard to get themselves known.

An interesting thing is that super user/developer companies have basically occupied most presentation slots on the Summit (market/committee consolidation?). In the [maillist](http://lists.openstack.org/pipermail/community/2016-May/001503.html) someone even proposed to remove voting process of speaker proposals.

Interesting new projects I met: [Romana](http://romana.io/try_romana/openstack/) for network and security automation; [Kingbird](https://wiki.openstack.org/wiki/Kingbird) for multi-site services; [Nation](https://www.youtube.com/watch?v=lddtWUP_IKQ) for compute node HA; [Convergence](https://specs.openstack.org/openstack/heat-specs/specs/juno/convergence.html) to make Heat execution more scalable and handle failures better; [Astara](https://www.youtube.com/watch?v=6pepWOwbmy4) for virtualize Neutron agents, VNF, and ease of management; [Tacker](https://www.youtube.com/watch?v=BQ2ZJWk2VNY) for network service function chaining orchestration.

### How to Select Videos to Watch

Each Openstack Summit releases hundreds of presentation videos. It is no easy work to select the most worthwhile ones to watch. Here's my guideline

  1. Checkout the officially featured videos ([link](https://www.openstack.org/videos/featured)).

  2. Checkout the officially summary/recap videos ([example](https://www.openstack.org/summit/tokyo-2015/videos/featured/openstack-summit-tokyo-2015-recap) of Tokyo Summit).

  3. Checkout the keynotes presentation ([link](https://www.openstack.org/summit/austin-2016/summit-schedule/#day=2016-04-25)). They are at the beginning of each summit day. They demonstrate key community events and directions.

  4. Checkout the Breakout Sessions. Openstack Summit is divided into Breakout Sessions and Workshops, Developer & Operator working sessions, Keynote presentations, Marketplace Expo Hall, Lounges, etc (see [summit timeline](https://www.openstack.org/summit/austin-2016/); it is clearer if you attend on-site). Note that this is not "track". Breakout Sessions are usually of more importance (of course you can watch other types too), to locate them:

      * Open the meeting room map ([link](https://www.openstack.org/summit/austin-2016/summit-map/)). Find the Breakout Session meeting room.

      * In presentation schedule page ([link](https://www.openstack.org/summit/austin-2016/summit-schedule/#day=2016-04-25)), find the talk by meeting room.

  5. Checkout the vidoes on Youtube of high view count ([link](https://www.youtube.com/user/OpenStackFoundation/videos?view=0&flow=list&live_view=500&sort=dd)). High view count video indicates bigger impact.

  6. Checkout the popular videos people liked through Twitter (effective if you followed the right group).

  7. Checkout how many attendees signed to watch a video ([example](https://openstacksummitmay2015vancouver.sched.org/event/05a6fe1fd957bfb74d6bdc8c21a5cdcd) of Vancouver Summit, see the "Attendees" part). It shows how many person said "I want to watch" this video.

  8. Checkout your interested videos by track ([link](https://www.openstack.org/summit/austin-2016/summit-schedule/#track=25)). Track means type of a presentation, for example, storage, operations, enterprise IT strategies, etc.

  9. Watch the presentation level ([example: beginner](https://www.openstack.org/summit/austin-2016/summit-schedule/events/7118)). Choose your fits.

  10. Don't forget #vBrownBag videos ([link](https://www.youtube.com/channel/UCaZf13iWhwnBdpIkrEmHLbA), search "austin"). They are 15min each, but usually very inspiring. #vBrownBag is not part of Openstack Foundation; AFAIK it is a horizontal organization that borrows slots in all sorts of summits.

  11. Checkout the Design Summit ([link](https://wiki.openstack.org/wiki/Design_Summit/Newton/Etherpads)). This is where the next version Openstack (Newton) features are being discussed and planned. Wish there was video. The Etherpads content are pretty condensed, while the best way to understand what core developers have said is to attend on-site.

Besides, if you can go on-site to an Openstack Summit, listen to the questions asked by audience (and answer), ask your questions, and talk with people, are usually more important.

### Featured Videos

After this Openstack Austin Summit, I found out that the official site provided us with a new lively [video page](https://www.openstack.org/videos/featured).

As far as I can see, Openstack Summit is high focusing on users, especially the big users. The most favored content are usecases, practices, experiences, etc. Technical details, black magic, design discussions are not the main theme, however, except that routinely core developers will come to stage and share the newest updates.

For real technical stuff, you may need to attend the [design summit](https://www.openstack.org/summit/austin-2016/summit-schedule/full/) (it spans the full week, with most events scheduled to the last summit day; search "contributors meetup"). The core developers summarize their discussions on [design summit etherpads](https://wiki.openstack.org/wiki/Design_Summit/Newton/Etherpads) (I wish there would be videos too). And remember that, the most cutting edge technical updates always appear on [developer maillist](https://wiki.openstack.org/wiki/Mailing_Lists#Future_Development), where the key is to learn how experts think and discuss upon a new problem.

**[AT&T's Cloud Journey with OpenStack](https://www.openstack.org/videos/video/at-and-ts-cloud-journey-with-openstack)**

AT&T is an elder and super user of Openstack. What they favor is common in the community: pen white box architecture, multi-site deploy with combined local and global controllers, no vendor lock-in, and the agility. But essentially I think it is cost-reduction, which is actually the most seen. I can see multi-site Openstack is getting mature and getting adoptted now. Checkout the differences between [zone vs region vs cell vs aggregates](http://docs.openstack.org/openstack-ops/content/scaling.html#segregate_cloud) (Note: Openstack zone is very different from AWS zone). Cell V1 is deprecated, while Cell V2 is still being actively developed ([link](http://docs.openstack.org/developer/nova/cells.html)). Murano is recommended by AT&T, for which I personally like its object-oriented orchestration language; Magnum, however, is not seen. And eventually Mirantis, and its Fuel, is becoming more and more the canonical production-level Openstack distribution.

**[Doubling Performance in Swift with No Code Changes](https://www.openstack.org/videos/video/doubling-performance-in-swift-with-no-code-changes)**

It is amazing that Swift, who uses Python as the data path language (with so many C++/C/Golang competitors), becomes such a success today. So tweaking Pythin interpretor is a must-do. I remember that Jython tries to run Python on JVM, leveraging JVM's GC, JIT & Hotspot and performance & maturity; not sure its stats, seems no much adoption. The default Python interpretor is CPython. [PyPy](http://pypy.org/), used in this video, however, features in the JIT, which is famous for interpertors. Using PyPy in Swift to improve performance is straightforward, which should have come out years before (since Swift is written in Python). Now it finally made progress, awesome progress, bravo!

**[Canonical - Carrier grade architecture with public cloud economics](https://www.openstack.org/videos/video/canonical-carrier-grade-architecture-with-public-cloud-economics-the-keys-to-successful-openstack-operations)**

NFV is hot and increasingly gaining heat in telecom area to adopt Openstack. But I think they are far from "[carrier grade](https://www.sdxcentral.com/articles/contributed/dont-confuse-high-availability-carrier-grade/2014/04/)" now, the latter demands HA, security, demanding throughput & latency, manageability, and smooth upgrading & patching. for jargon such as Openstack vs OpenDaylight vs Openflow vs Open vSwitch, see [here](https://www.quora.com/What-is-the-relation-between-OpenStack-OpenDaylight-OpenFlow-and-Open-vSwitch-Are-there-other-options-in-place-of-any-of-these). Generally this video gives introduction to Juju (integrated with Ubuntu) that eases Openstack development, and provide support to various aspects such as containers, hyper-converged architecture, software-defined storage, NFV & SDN, deep learning, ceph monitoring. The interesting trends is that, Ubuntu becomes increasingly the canonical platform for Openstack and various opensource software. Although people saying CentOS is more production stable, it seems systemd draws too much repell from the community.

**[Embracing Datacenter Diversity](https://www.openstack.org/videos/video/embracing-datacenter-diversity)**

This is a keynote. 7500 people attended Austin Summit on-site (slightly less than 9000 in Tokyo?). A key move from this summit is the [Certified Openstack Adminstrator (COA)](https://www.openstack.org/coa). We can see Openstack is preparing to become a mature industrial foundamental platform; increasingly more [training activities](https://www.openstack.org/summit/austin-2016/summit-schedule/#track=47) occur on the summit, and now we have official Openstack admin certification. In China, [99Cloud](http://www.99cloud.net/html/2016/gongsixinwen_0426/156.html) instantly established the COA training facility. The video released currently voted [Openstack Super Users](http://superuser.openstack.org/) winner: NTT (Tokyo), from nominated candidates: GMO INTERNET, Go Daddy, Overstock, University Federal de Campina Grande, Verzion.

**[AT&T's OpenStack Journey. Driving Enterprise Workloads Using OpenStack as the Unified Control Plane](https://www.openstack.org/videos/video/at-and-ts-openstack-journey-driving-enterprise-workloads-using-openstack-as-the-unified-control-plane)**

AT&T is elder. AT&T Integrated Cloud (AIC) starts from Juno, and moving to Mitaka in 2017. Agility, CI/CD, DevOps are the key enabler from Openstack; so like most adoptors, AT&T is using Openstack vastly in the development environment, but seems limitted in production. They use KVM and VMware (vCenter) in hybrid. They need to integrate Openstack with many other things, so writing Fuel plugins is priority, and also need to integrate Fuel with other management tools such as Ansible. Fuel upgradability is the key. There are things that AT&T needs but not present in upstream community, AT&T needs to close the gap itself (and contribute).

**[HPE - Lifecycle Management of OpenStack Using Ansible](https://www.openstack.org/videos/video/hpe-lifecycle-management-of-openstack-using-ansible)**

HP Openstack, Helion, is elder, but doesn't perform very successful. HP [shutdown its public cloud](http://www.businessinsider.com/hp-shutting-down-hp-helion-public-cloud-2015-10) in Oct 2015. This video demonstrate HPE's lifecycle management of OpenStack using Ansible. To be honest, this is a hotspot in the past Openstack but already out-dated now (and we have Fuel).

**[Fireside Chat: Mark Collier & Jim Curry](https://www.openstack.org/videos/video/fireside-chat-mark-collier-and-jim-curry)**

It is very interesting that this talk tries to dig into venture capitalists' key concerns related to startups based on opensource. For startups, how to evaluate the correct product and market is hard. Another problem is scaling (from small business to big), for example, how to do goto market, how to build the organization and leadership team, how to think about services vs product. Although they are not as familar with the technical part, Venture help beyond money. When enterprise wants technology, they want it standard and know where the support comes from, rather than free cost; the former is what Redhat is doing. Markey dynamics are changing; companies are invest more in opensource rather than proprietary. The speaker expressed concerns about a trend from building great technology to building for money. Opensource vs open-core is interesting; although the later is widely being employed today, but too many companies are burned by their open-core models. Customer expects their vendors to make money (they want healthy vendors), but don't like to be held hostage by them (no vendor lock-in is big concern). The open-core model is slowly dying today (according to the speaker). Next generation angel is a new creation, which requires entrepreneurs to be under age 40, and a commitment that investor spends enough time staying with startups.

**[Intel Sponsor Keynote](https://www.openstack.org/videos/video/intel-sponsor-keynote)**

Intel and IBM are radical investors in various opensource ecosystem. It is interesting to think how their strategies differ from other elder IT vendor companies. Recent breakthroughs, DPDK & SPDK, 3D XPoint NVM, Intel PCIe SSDs, and E5 v4 Cloud CPU, from Intel, are bringing great momentum in the storage and cloud world. Native [GPU access in virtual machines](http://www.cnblogs.com/sammyliu/p/5179414.htm) now relies on [Intel GVT](https://01.org/igvt-g); if you remember that [Intel VT](http://www.intel.com/content/www/us/en/virtualization/virtualization-technology/intel-virtualization-technology.html) is one of the beginning foundation of the virtualization age.

**[Mirantis Sponsor Keynote](https://www.openstack.org/videos/video/mirantis-sponsor-keynote)**

I can say that, Mirantis makes production-level Openstack distribution public accessable. Tales are that Mirantis before Openstack is nearly bankrupt. But Mirantis grabbed the big oppotunity, and became the canonical Openstack flagship (and gets a lot of financing investments). It doesn't own any single line of proprietary code; the value comes from their selection of bug fixing, patches, and security enhancements, they step further than community, their solid testing, and their good deployment designs ([link](https://www.mirantis.com/blog/mirantis-openstack-real-open-community-development/)). Mirantis is also the top rank [upstream contributor](http://stackalytics.com/?release=mitaka&metric=commits). This video tells an interesting opinion: Openstack is 1 part technology and 9 parts people and process.

**[DevOps At Betfair Using Openstack and SDN](https://www.openstack.org/videos/video/devops-at-betfair-using-openstack-and-sdn)**

This video is completely organized as a long and solid demo. Betfair shows how they use their tools and Openstack underlyingly to orchestrate package building, network creating, app deployment, setup loadbalancers, and rolling upgrade their app. It is curious that no one actually use Horizon; they build UI each of their own. In a word, the demo is killer usecase of Openstack in app lifecyle management.

### Keynotes

What, I can't find any Keynote video? Are they merged into featured videos? Or decomposed into a series of common videos? Weird ... (There are still Tokyo keynotes on Youtbe, but no Austin ...)

### Recaps

There is no official recaps of Austin Summit. But I've found one from Rackspace and one from HPE.

**Rackspace: [OpenStack Summit Austin 2016 - Racker Recap](https://www.youtube.com/watch?v=LwHj2AmUp5A)**

Talking about the Summit is exciting, in such a big scale, great experience, bla, bla, bla ... Nothing important.

**HPE: [OpenStack® Summit 2016 Austin Recap](https://www.youtube.com/watch?v=DMC03xQAbT4), [Day 2](https://www.youtube.com/watch?v=TGql1l2hofw), [Day 3](https://www.youtube.com/watch?v=Eog9mXDgxIg), [Day 4](https://www.youtube.com/watch?v=TuAiQj-AbC0)**

To short. A lot of big things are happening ... Video ends.

### Cinder, Ceph and Storage in Openstack 

I'm always interested in Ceph, Cinder and various storage technologies in Openstack, either data path or control path. Recent storage world are quickly evolving: DPDK & SPDK, PCIe SSD, NVMe, NVDIMM, RDMA adoption, smart NIC, Ceph BlueStore, hyper-converged architecture, software-defined storage (SDS), etc. Is an age that

  * Storage is again merging with computing. You can see Ceph (using commodity computing hardwares), and hyper-converged architectures.
  
  * Software-defined datacenter is the future. SDS is one of the pieces.
  
  * Flash is getting more and more adoptted. You can see from SAS/SATA SSD, PCIe SSD/Flash, NVMe SSD/Flash, NVDIMM SSD/Flash, persistent memory, etc, they are quickly climbing up the stack. Storage (and network) is too fast for CPU and memory, so people are finding ways to mitigate the memory bandwidth and PCIe bandwith limits, where you can see DPDK, SPDK, RDMA, etc. Many new technologies bypass the Linux Kernel to achieve lower latency. Also, Kernel page table (and the hardware-assistant MMU) now can be used to address filesystem metadata, see [SIMFS](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?reload=true&arnumber=7304365), interesting.
  
  * Scale-out architecture is the king. I have to say that one reason is Intel cannot build any more scaled-up CPU (and architecture) now, so vendors need the industry to buy-in scale-out strategy. And scale-out is more friendly to the cloud fashion and commodity white box trend.

**[How Stuff Works Cinder Replication and Live-Migration](https://www.youtube.com/watch?v=IZJpmxmvNpg)**

Cinder replication has been long under development, basically, get troubled because vendors have very different design requests. Replication V1.0 is in volume granularity, but given up. Replication V2.x is in fulll backend granularity. V2.1 hope fully will be available to use ([doc](https://specs.openstack.org/openstack/cinder-specs/specs/mitaka/cheesecake.html)). This [article](https://mp.weixin.qq.com/s?__biz=MzA3MjkwMDY5OA==&mid=2652565853&idx=1&sn=27ce74e11b831c133a1623d40ebd8dba) is a good introduction of how replication works; but it doesn't mention [thaw](https://github.com/openstack/cinder/blob/e950e23ca947bb755444db60ed90280f06ea0b86/cinder/volume/api.py#L1696). The video is by NetApp. Live migration and storage compability [chart](https://youtu.be/IZJpmxmvNpg?t=2m48s) is a bit useful.

**[Big Data Rapid Prototyping by Using Magnum with Cinder and Manila](https://www.youtube.com/watch?v=JlVdODLqshE)**

Joint video by NetApp and SolidFire. This video introduces using Magnum to orchestrate container PaaS, use Manila to deploy a share (filesystem), and mount to Docker. Where is the "big data"?

**[One Does Not Simply Use Multiple Backends in Cinder](https://www.youtube.com/watch?v=K7LQW85jkiM)**

Cinder volume-type and multi-backend have been available for long time. This video teaches you how to use.

**[Cinder and Docker, Like Peanut Butter and Chocolate](https://www.youtube.com/watch?v=CenWomQtQh8)**

Cinder and Manila are of coure volume solutions for Container/Docker, one as block and one as fileysystem. Docker now have volume-plugin. Kubernetes support Cinder ([doc](http://kubernetes.io/docs/user-guide/persistent-volumes/#types-of-persistent-volumes)). The talk is by IBM and Dell, but promote rackspace/gophercloud in the end.

**[Leverage the Advantage of Multiple Storage Backends in Glance](https://www.youtube.com/watch?v=eWajj-G9W5k)**

This video is by UnitedStack. "More and more users want to leverage the advantages of ceph and enterprise storage. But with the restriction of glance we could only get images in one place and copy to another storage if we boot virtual machines in different backends." Now we can use Glance Multi-location to solve the problem. It is also a usecase that we need more than one Ceph backends to be switched in Glance.

**[EMC - Enterprise Storage Management for Mixed Cloud Environments](https://www.youtube.com/watch?v=oRDyeBtzfcA)**

Promoting using CoprHD in Openstack. AFAIK CoprHD can be used to replace Cinder (CoprHD supports Cinder API), or to be used as a Cinder driver. CoprHD actually has a pretty cool [architecture](https://coprhd.atlassian.net/wiki/display/COP/A+Short+Guide+to+the+CoprHD+Architecture) and a much wider [feature range](https://coprhd.atlassian.net/wiki/display/COP/Storage+Controller+Overview#StorageControllerOverview-2.2APIService(apisvc)) covering block, object, filesystem, replication, and recovery.

**[Datera - OpenStack Cinder delivering Intent-Defined Infrastructu](https://www.youtube.com/watch?v=h5JpE2Asu1k)**

Datera introducts its orchestration tool product. Talks a lot about the template.

**[Persistent Storage for Containers Using Cinder](https://www.youtube.com/watch?v=ClKcMCDzueY)**

The [emccode/rexray](https://github.com/emccode/rexray) is software-defined storage controller for container platforms such as Docker and Mesos. Magnum uses Rexray to [provide persistent volumes](https://github.com/openstack/magnum/blob/f153d61c442053d335072d3dbf69113b678dd13c/magnum/templates/mesos/fragments/volume-service.sh#L23) for Mesos. Compared to Cinder, Rexray is more native to Docker, standalone, and simpler (also mentioned [here](http://www.openstack.cn/?p=5299)).

**[Cephfs as a Service with OpenStack Manila](https://www.youtube.com/watch?v=vt4XUQWetg0)**

CephFS has finally gone production-ready ([Jewell version](http://thenewstack.io/converging-storage-cephfs-now-production-ready/)). Integration of CephFS with Manila is OK but seems not mature yet.

**[Cinder Project Update](https://www.youtube.com/watch?v=pVvzn_bSDtY)**

Cinder core developers presents.

  *The Replication API: V2.0 is disabled, V2.1 (Cheesecake) fallover the whole backend; avaible to use now, but not mature; vendor support list see [here](https://youtu.be/pVvzn_bSDtY?t=4m24s).

  * Backup supports full and incremental and non-disruptive backup. Active-active HA is very awesome design, there are a lot of moving parts, still WIP. Checkout the [code](https://review.openstack.org/#/q/message:+blueprint+cinder-volume-active-active-support) if you like.

  * Multi-attach allows a volume to be attached to multiple hosts or VMs, not fully functional yet.

  * Rolling upgrade is OK now, but I guess it not very mature; it includes RPC versioning, versionedObjects, API microversions, and online DB schema upgrade. There are updates for Fibre Channel.

  * Some new backend drivers are added (now 53 in total); LVM, RBD, NFS are the reference architectures.

In Newtown (next release), we will have, Replication V2.x (Tiramisu); continuing of active-active HA, rolling upgrade, microversions, os-brick will help Cinder on ironic baremetal, and async operation and reporting. Cinder Replication Tiramisu gives tenants more control of the replication granularity, e.g. a volume or a group of volumes (using Replication Groups). 

**[The Performance Issues of Cinder Under High Concurrent Pressure](https://www.youtube.com/watch?v=n9TZDvwZffY)**

AWCloud (海云迅捷) presents. They deployed 200 nodes Openstack and test by Rally. Boot from volume often fail because of the low performance of Cinder. The problem resides on
  
  * HAProxy reports 504. It is too slow because the version is too old
  
  * Cinder-api database connection driver blocks the thread (eventlet monkey patch doesn't help). Solution is to increase worker count.

  * Cinder-volume is too slow to process large amount of requests: create volume, initialize connection, attach. Solution is to run more Cinder-volume workers (private code).

  * Cinder-volume race condition while running multiple works. Solution is to add lock (private code).

  * RDB rados call blocks the thread, because they are not patched by eventlet.

  * Download or clone image is too slow by Glance. Solution is to use RBD store.

  * The increase of database entries lead to sharp decline in performance. The hotspot is the reservation table. Solution is to add a combined index, and clean unecessary data.

  * Others: increase rpc_response_timeout, rpc_case_timeout, osapi_max_limt.

Results: boot_server_from_volume from failure in concurrency=200, to all success in concurrency=500; create_volume from failure in concurrency=1000, to all success in concurrency=2500. Good presentation!

**[Expanding DBaaS Workloads with OpenStack Trove and Manila](https://www.youtube.com/watch?v=VMrFL7jyTyY)**

Presentation by Tesora, NetApp and Redhat. On [5min22s](https://youtu.be/VMrFL7jyTyY?t=5m22s) there is a summary of why people want Openstack

  * 97% is to standardize one platform API
  * 92% to avoid vendor lock-in
  * 79% to accelerate innovation
  * 75% to operation efficiency
  * 66% to save money

"Until recently, the OpenStack Trove DBaaS project only used the Cinder block storage service for database storage. With joint development work from NetApp, Red Hat and Tesora, it is now possible to run database workloads on OpenStack using Manila-based file shares."

**[Red Hat - Making Ceph the powerhouse you know it can be!](https://www.youtube.com/watch?v=q7WOlte7hco)**

Introduce [Red Hat Ceph Storage](https://youtu.be/q7WOlte7hco?t=32m23s) to you.

**[VMware - Charter, PernixData, VMware A case study](https://www.youtube.com/watch?v=mw6fdkpvzoY)**

Cassandra deployment demo to introduce VMware Integrated OpenStack, VMware NSX, and [PernixData](http://pernixdata.com/press-release/pernixdata-fvp%E2%84%A2-added-vmware-partner-verified-and-supported-product-program). The case study is pretty detailed, with cluster layout design and benchmark results.

**[There and Back Again - Moving Data Across Your Clouds](https://www.youtube.com/watch?v=NrdIxKSvqcg)**

Presentation by Mirantis. Migrating data from one storage backend to another backend, or inter-cloud. Challenge is usually network limits, and how to avoid impact SLA. Approaches can be

  * DD from block to block. Simple, slow, and don't allow data udpates.
  * Rsync. It's file but [not block level](http://strugglers.net/~andy/blog/2011/03/13/copying-block-devices-between-machines/).
  * Use storage backend's replication. It is vendor dependent.
  * Just connect the storage backend to the other side.

They use [bbcp protocol](https://www.olcf.ornl.gov/kb_articles/transferring-data-with-bbcp/) to accelerate block migration. The command `dd | pv | dd` looks useful. For ceph, we have rbd export-diff and rbd import-diff; rbd export and rbd import; this is called [incremental snapshots transfer](http://ceph.com/dev-notes/incremental-snapshots-with-rbd/). [Sébastien's blog](http://www.sebastien-han.fr/blog/2013/01/28/ceph-geo-replication-sort-of/) is using DRBD and Pacemake. MOS/Fuel plugin helps deploy existing Ceph as primary storage, i.e. connect instread of move; it is still under development.

**[Scality - S3 and OpenStack, the best of both worlds](https://www.youtube.com/watch?v=zWbW1e_IpUI)**

Present by [Scality](http://www.scality.com/). Swift is [not fully compatible](https://youtu.be/zWbW1e_IpUI?t=12m28s) with AWS S3 API, for example container/object encryption. Scality Ring Storage product comes for you.

**[Amalgamating Manila And Swift for Unified Data Sharing Across Instances](https://www.youtube.com/watch?v=3MMrMUaA_Mg)**

Object storage has become more of a choice for many workloads. There are still traditional applications that need filesystem access. Swift and Manila solves the data sharing needs for VM. Presentation by IBM.

**[Ceph at Scale - Bloomberg Cloud Storage Platform](https://www.youtube.com/watch?v=gW084yAvoK0)**

Ceph RGW, the object storage, is actually pretty popular. Many people are deploying RGW. The [POD architecture](https://youtu.be/gW084yAvoK0?t=2m55s) of Ceph is interesting, even it may not be really necessary. VM use ephemeral storage vs Ceph, a [summary](https://youtu.be/gW084yAvoK0?t=3m37s). Ceph RGW stack configurations, see [here](https://youtu.be/gW084yAvoK0?t=6m53s). This video shares in detailed their Ceph and RGW config in both hardware and software. The orchestration of Ceph is by Chef. Their tools at [github](https://github.com/bloomberg/chef-bcs). The testing [tools](https://youtu.be/gW084yAvoK0?t=37m1s) for Ceph and RGW:

  * Ceph: RADOS Bench, COS Bench, FIO, Bonnie++
  * Ceph RGW: JMeter. Test load by requesting from a cloud.

**[Swift Object Encryption](https://www.youtube.com/watch?v=SBkvHYFhwjQ)**

Presentation by IBM and HPE. This talk is about future, so Swift object encryption is not ready. The encryption can be supported in hardware disk level, virtual block device level (LUKS, dm-crypt), or Swift encryption middleware level. BYOK (bring your own key) can be supported only in the last approach. Here is encryption [spec](http://specs.openstack.org/openstack/swift-specs/specs/in_progress/at_rest_encryption.html) and [code](https://github.com/openstack/swift/tree/feature/crypto).

**[OpenStack + Open Compute Project == Best of Breed Clouds](https://www.youtube.com/watch?v=rrzZ08jSPKE)**

Presented by Big Switch. This talk is about [OCP hardware](http://www.opencompute.org/). It is still early age, so this talk is pretty "soft".

**[Protecting the Galaxy - Multi-Region Disaster Recovery with OpenStack and Ceph](https://www.youtube.com/watch?v=VWFYC6W71tY)**

Talking about backup in Openstack, there is a project, [Freezer](https://www.openstack.org/summit/vancouver-2015/summit-videos/presentation/freezer-the-openstack-back-up-as-a-service-platform), focusing data level, and [Smaug](https://github.com/openstack/smaug) focusing on application-level. Besides, you can apply the common [standard backup practices](http://docs.openstack.org/openstack-ops/content/backup_and_recovery.html), for DB, filesystems, /var/lib/xxx, /etc/xxx, /var/log/xxx, etc.

This presentation focus on Ceph cross-site backup. [RDB mirroring](http://docs.ceph.com/docs/master/rbd/rbd-mirroring/) (finally, don't need to export-diff now) is used to replicate Ceph. The [architecture design](https://youtu.be/VWFYC6W71tY?t=14m33s) replications each level of Openstack. RBD mirror is available with Ceph Jewel, with the upcoming Redhat Ceph Storage 2.0. RBD mirror replicates journal underlyingly; it is asynchronized replication. It is supported in Cinder Replication V2.1. The current [gap](https://youtu.be/VWFYC6W71tY?t=25m34s) mainly resides on metadata replication. New project [Kingbird](https://wiki.openstack.org/wiki/Kingbird) provides centralized service for multi-site Openstack deployments.

**[A Close Look at the Behaviors of the Multi-Region Swift Clusters](https://www.youtube.com/watch?v=4y00OsFShng)**

Presented by Inspur (浪潮) & 99Cloud. The write & read affinity creatly improve multi-site performance of Swift. But due to eventual consistency, new data may not have to be replicated to appropriate location when site failure happens. Basically this talk tells about some practices about read & write affinity.

**[SanDisk - The Consequences of Infinite Storage Bandwidth](https://www.youtube.com/watch?v=-X9BuepxGko)**

SSD / CPU performances and bandwidth drop dramatically because the quick climbing of SSD speed. CPU / DRAM bandwidth bottleneck is another problem. SAN 2.0 - NVMe over Fabrics; this is an interesting idea:

  * NICs will forward NVMe operations to local PCIe decies
  * CPU removed from the software part of the data path
  * CPU is still need for the hardware part of the data path
  * IOPS improve, BW is unchanged
  * Significant CPU freed for application processing

To me, it looks like that the storage industry is evolving in spiral path. The rise of new NVM/SSD media, may bring back the past-style SAN architecture again. But this time, NVMe protocol is connected directly on PCIe bus, compared to the past-style expensive SCSI. Storage media access is bypassing kernel, bypassing CPU, bypassing memory, just direct RDMA; so it's kinda like a computer controller connecting to bunch of disk arrays, even through the disk array box is actually a computer, its CPU/memory/OS is not used or necessary. New technologies also bring in a lot of proprietary hardware configurations, but they are really much faster than what pure-software white box can do now. Finally rack-scale architecture is a lot heard related to the storage market.

**[OpenIO - OpenIO Object Storage Made Easy](https://www.youtube.com/watch?v=uOX5OimY_s4)**

Presented by [OpenIO](http://openio.io/). Commodity hardware + softwared-defined storage = hyper scalable storage and compute pool. Track containers rather than objects. Grid of nodes with no consistent hashing, never balance data. Dynamic loadbalancing by compute scores for each serivce in realtime. These designs are interesting. The OpenIO object storage is integrated at Swift Proxy server level.

**[Swift Middlewares - What Are They?](https://www.youtube.com/watch?v=GSmXyejbGQ0)**

The "middileware" here orients from Python's WSGI server design. It allows you to add customized feature to each part of Swift. Middleware can be added to the Swift WSGI servers by [modifying](http://docs.openstack.org/developer/swift/development_middleware.html) their [paste](http://pythonpaste.org/) configuration file. Anyway, middleware is the decorator design pattern introduced by Python WSGI to overlay server features; it's useful. Swift itself actually uses a lot of middleware, see its [config file](http://docs.openstack.org/developer/swift/development_middleware.html).

**[Optimizing Software-Defined Storage for OpenStack](https://www.youtube.com/watch?v=kQ9FJuUQYsE)**

Present by EMC. Promoting the idea of software-defined storage (SDS), and EMC ScaleIO. Shared [best practices](https://youtu.be/kQ9FJuUQYsE?t=34m4s) for work with SDS. Compared to Ceph, ScaleIO is purpose-built, native block, less trade-off on performance.

**[Swift 102 Beyond CRUD - More Real Demos](https://www.youtube.com/watch?v=4A9ypg2ASPE)**

Present by SwiftStack. A practical talk to introduce Swift advanced features. Concurrent gets to reduce first byte latency. To optimize multi-region, use read/write affinity, memcache pooling, aysnc account/container updats. Swift 2.7 now allows for 1 byte segment in Static Large Objects (previous it is 1MB).

**[Developing, Deploying, and Consuming L4-7 Network Services](https://www.youtube.com/watch?v=OXf40IdYASU)**

This is Hands-on Workshop, lasting 1h26m. The Youtube view count is 278, pretty high in average, looks welcome. There is a demo of network service chain: external -> firewall + lb -> lb -> app -> db. The demo is present on Redhat Enterprise Linux Openstack Platform (not Horizon, well).

**[Hey Storage Engineer Tell me About Backups in OpenStack!](https://www.youtube.com/watch?v=7jUDLdpIO9w)**

Present by NetApp & SolidFire. Backup the volume snapshots from Cinder, to Swift, to NetApp appliance (dedup & compression is good), or to cloud through a cloud gateway (cloud-integrated storage appliance). Demo 2 shows the backup workflow of SAP HANA on Manila. Next they introduced Manila Share Replication. Replication is used as non-disruptive backup.

**[How to Integrate OpenStack Swift to Your "Legacy" System](https://www.youtube.com/watch?v=sygqq9hDJzk)**

Present by NTT. Swift is good solution backup / disaster recovery. Swift uses HTTP REST API. But customer, as mentioned in this video, wants NFS or iSCSI to be compatible with their legacy application. The solution is to mount Swift as filesystem using Cloudfuse. But note that Swift is optimized for large files rather than lots of small files. There various issues while trying to use Swift as NFS/iSCSI to solve the backup problem. This talk has in detail discussion of them.

**[Scality - Open Networking and SDS, vendor-level integration amplifies Software Defined Convergence](https://www.youtube.com/watch?v=cK_pTNkeeW8)**

Introduction of Scality Ring Storage product. [Cumulus Linux](https://cumulusnetworks.com/cumulus-linux/overview/) is interesting: a networking-focused Linux distribution, deeply rooted in Debian. It is fully distributed P2P no-center-at-all architecture.

**[Scality - OpenStack Unified Storage One Platform to Rule them All](https://www.youtube.com/watch?v=8DIbF7zPoXU)**

Scality Ring Storage product is a unified storage platform, being able to support Swift, Glance, Cinder, Manila (each has the dirver). It is able to replication, erasure coding, geo-redundancy, self-healing, etc. On 9m50s there is an [Openstack Storage usecase diagram](https://youtu.be/8DIbF7zPoXU?t=9m50s) against storage type and size.

**[EMC - Accelerating OpenStack deployments with modern all-flash scale-out storage](https://www.youtube.com/watch?v=zbmN8NotZwE)**

Promoting EMC XtremIO. The problem to solve is: IO blender effect at large scale, VM provisioning & clone, dynamic policy-based operations. XtremIO is all-flash and sparkingly fast. The content-based addressing is a key design of XtremIO. Actually the best technical video to introduce XtremIO is the one from [Storage Field Day](https://www.youtube.com/watch?v=lIIwbd5J7bE) and the one from [SolidFire](https://www.youtube.com/watch?v=AeaGCeJfNBg). XtremIO is the #1 all-flash market leader with 34% share. On [11m51s](https://youtu.be/zbmN8NotZwE?t=11m48s) there is a comparison graph of scale-up vs scale-out on the rack shelf; scale-up is actually not able to survive shelf-level failure (e.g. power, switch). Per XtremIO controller provides 150K IPOS, scale-out to 16 boxes 2M IOPS. XtremIO has 100% metadata in memory, inter-connected with RDMA fabric. XtremIO integrates with Openstack Cinder to provide block storage.

**[Monitoring Swift ++ (incl Nagios, Elasticsearch, Zabbix, & more)](https://www.youtube.com/watch?v=YxDIz25nqAo)**

Presented by SwiftStack. [8m13s](https://youtu.be/YxDIz25nqAo?t=8m13s) is a nice summary of monitoring components: agent, aggregration engine, visualizer, alerting, and the popular solutions for each of them. [10m11s](https://youtu.be/YxDIz25nqAo?t=10m11s) categorizes the types of data to monitor, and the monitoring lifecycle: measurement, reporting, characterization, thresholds, alerting, root cause analysis, remediation (manual/automated). [19m49s](https://youtu.be/YxDIz25nqAo?t=19m49s) records the key point to monitor in Swift: cluster data full, networking including availability and saturation, proxy states such as CPU and /healthcheck, auditing cycles, replication cycle timing. The checks can be installed on load balancer. Later of this talk is demo.

**[Canonical - ZFS, Ceph and Swift for OpenStack and containers wi](https://www.youtube.com/watch?v=9tGE29hKJTk)**

Present by Ubuntu. [Canonical](http://www.canonical.com/) is the company behind Ubuntu. Ubuntu is quite active on this Summit. Compariing raw Disk (3-year refresh) vs AWS storage price:

  * SSD $12 TB/month
  * HDD $1.5 TB/month
  * EBS SSD $100 TB/month
  * EBS HDD $45 TB/month
  * S3 $30 TB/month
  * Glacier $7 TB/month
  * S3 $90/TB transfer out
  * Glacier $10/TB transfer out

[8m45s](https://youtu.be/9tGE29hKJTk?t=8m45s) is a summary of how recent new technologies save cost (is low-power archtecture ready to use now?). So how Ubuntu helps reduce storage cost? ZFS, Ceph, and Swift. [Deutsche Telekom] evaluated Manila, summarizing that Manila is [enterprise mature](https://youtu.be/9tGE29hKJTk?t=42m17s), and [something needs improve](https://youtu.be/9tGE29hKJTk?t=33m46s).

**[Cephfs in Jewel Stable at Last](https://www.youtube.com/watch?v=T8x1FGo60k4)**

Finally! CephFS is production-ready in Jewel release. For previous history, see [CephFS Development Update, Vault 2015](http://events.linuxfoundation.org/sites/events/files/slides/CephFS-Vault.pdf).

CephFS has "consistent caching". The client is allowed to cache, and server invalidates them before change, which means client will never see any stale data. Filesystem clients write directly to RADOS. Only active metadata is stored in memory. CephX security now applies to file path. Scrubbing is available on MDS. Repair tools are available: cephfs-data-scan, cephfs-journal-tool, cephfs-table-tool. MDS has standby servers; they replay MDS logs to warm up the cache for fast take-over. CephFS [sub-tree partitioning](http://ceph.com/papers/weil-mds-sc04.pdf) allows you to have multiple active MDSes. Directory fragmentation allows you to split a hot directory over many active MDSes; it is not well-tested. Snapshot is available now. You can create multiple filesystem, like pools or namespaces (not well tested). Still pain points: file deletion pins inode in memory, client trust problem (there is totally no control expcet separate them in namespaces/tenants), some tools to expose states are still missing (dump individual dirs/files, see why things are blocked, track access to file). 

**[Designing for High Performance Ceph at Scale](https://www.youtube.com/watch?v=P6SCdZXpM2Q)**

Presented by Comcast. The storage node is using NVMe for journal (but SATA HDD). To benchmark, FIO for block, Cosbench for object. Remember to test scaled-out performance. Issues encountered

  * [TCMalloc eats 50% CPU](https://youtu.be/P6SCdZXpM2Q?t=20m58s). Solution is to give it more memory
  * [Tune the NUMA](https://youtu.be/P6SCdZXpM2Q?t=25m49s). Map CPU cores to sockets; map PCIe devices to sockets; Map storage disks (and journals) to the associated HBA; pin all soft IRQs to its associated NUMA node. Align mount points so that OSD and journal are on the same NUMA node.

[General performance tips](https://youtu.be/P6SCdZXpM2Q?t=37m58s) below

  * Use latest vendor drivers (can be up to 30% performance increase)
  * OS tuning focus on increasing threads, file handles, etc
  * Jumbo frames help, particular on the cluster network
  * Flow [control issues](https://en.wikipedia.org/wiki/Ethernet_flow_control) with 40Gbe network adapters; watch out for dropping packets
  * Scan for failing disks (slow responding disks), take them out

### Popular Presentations

Next I will pick up the popular Openstack Austin Summit videos by Youtube view count that I'm interested to watch. It is 3 weeks after the Summity day, rough average view count is 100. So 200+ usually means the video is popular. There are a few videos which has over 1000+ views, such as [Why IBM is Betting on OpenStack](https://www.youtube.com/watch?v=ib3vsxc_wWk).

**[IBM - Why IBM is Betting on OpenStack](https://www.youtube.com/watch?v=ib3vsxc_wWk)**

Declare own move is a powerful strategy according to [Gaming Theory](http://v.163.com/special/gametheory/). IBM contributs a lot in Openstack community. Bluemix is based on CloudFoundry, and addes a well set of functionality including [CI/CD](https://www.youtube.com/watch?v=q3Kb3FEc9bE#t=9.339333), [Collaboration](https://www.youtube.com/watch?v=3OHMrr8iz5E), [IoT](http://www.ibm.com/internet-of-things/), [Serverless](http://www.ibm.com/cloud-computing/bluemix/openwhisk/). IBM identified customer needs Openstack distributor rather than direct community source. Openstack etc is also a good base from where IBM builds its cloud solution stack.

Besides, the bet may have relation with IBM's vast lay-off recently: \[[1](http://mp.weixin.qq.com/s?__biz=MjM5MzM3NjM4MA==&mid=2654675950&idx=3&sn=d1ce71e83bbd51f030e236867bce5056)\]\[[2](http://mp.weixin.qq.com/s?__biz=MjM5MzM3NjM4MA==&mid=507192360&idx=1&sn=b0e453db6c8eb6e87b00bc09b1c25731)\].

**[How SAP runs IoT on top of OpenStack](https://www.youtube.com/watch?v=UoREXLJNMcw)**

IoT Platform on SAP HANA Platform on CloudFoundry on Openstack, helps customer to transform their business. This is a pretty sales-oritented video, no much detail. SAP and CF (and also GE) are good pantners from early age. CF sells well in North America, however not even much known in China.

**[Nova Cells V2 What s Going On?](https://www.youtube.com/watch?v=Sieza5iMBXY)**

Openstack multi-site is receiving increasing attention. Cell is a unified API endpoint for multi-site. It is in use by large deployers such as Rackspace, CERN, GoDaddy. Checkout the differences between [zone vs region vs cell vs aggregates](http://docs.openstack.org/openstack-ops/content/scaling.html#segregate_cloud) (Note: Openstack zone is very different from AWS zone). Cell V1 is deprecated, while Cell V2 is still being actively developed ([link](http://docs.openstack.org/developer/nova/cells.html)).

Generally there are two ways to create a large cluster: 1) just creat a cluster with all nodes 2) create a lot of small clusters and combine them in some way. Cell works for (2). Note that many scale-out distributed system actually cannot scale much; if you use (1), the message queue, scheduler, DB, whatever, may start to malfunction when the cluster is large enough. The easier way is to use (2), where only exist small clusters, but combine them with either a unified API, or separated by let user select the region.

I remember that many online games let player select region, that is (2), which creatly lowers down the difficulty of creating large cluster (and server large amount of user). Internet companies also use [Cell architecture divided by user accounts](http://www.infoq.com/cn/presentations/high-performance-services-practice-based-on-cell-architecture), to reduce the difficulty of building a large cluster, and to achieve even [active-active multple datacenters located in different cities](http://www.infoq.com/cn/articles/interview-alibaba-bixuan). 

This is a pretty in-detail talk about how Cell V2 works. There are a lot of moving parts. Looking forward to it. [Cell V2, expected Fall 2016](https://youtu.be/Sieza5iMBXY?t=26m17s).

**[Building a SmartCity with IoT](https://www.youtube.com/watch?v=Ym_CZ8-crD8)**

Present by [TCP Cloud](http://www.tcpcloud.eu/). This video is very hot (and short), 2000+ views (the average presentation view count is only 100). IoT creates a lot of usecases for common user, and for the industry. Sensors -> IQRF -> gateway -> internet -> datacenter based on Openstack, with analyzing, big data, visualization, and API access; architecture at [5m24s](https://youtu.be/Ym_CZ8-crD8?t=5m24s). Container (in gateway) and virtual machines (in processing platform) are used together, connected with overlay network solutions. Note that, they can boost Kubernetes which starts various micro-services at the IO gateway directly located in the city, or in any remote location; this extends their platform. The final demo is pretty cool, see from [5m41s](https://youtu.be/Ym_CZ8-crD8?t=5m41s).

**[Automated Security Hardening with OpenStack-Ansible](https://www.youtube.com/watch?v=q_uDtdpLmpg)**

Present by Rackspace. A lot of attention on automated security. What they use: [Security Technical Implementation Guides](https://youtu.be/q_uDtdpLmpg?t=9m37s) (STIG) from the Defense Information System Agency (DISA). It covers a lot of [critical aspects](https://youtu.be/q_uDtdpLmpg?t=10m29s). They embed the security configurations in openstack-ansible-security, and with documentation. [How to get it](https://youtu.be/q_uDtdpLmpg?t=19m56s): apply_security_hardening to True.

**[OpenStack and Kubernetes: Inception](https://www.youtube.com/watch?v=e-j9FOO-i84)**

Google and CoreOS demo deploying containerized Openstack running on Kubernetes, including fast adding Nova compute node, auto failure recovery, and black-white publish of Horizon. The overall architecture is called GIFEE (Google Infrastructure for Everyone Else). There needs some modification on Kubernetes to allow Openstack components to invoke (privileged) hypervisor features. Pretty Google style.

**[Dreamhost - What s New with DreamHost DreamCompute](https://www.youtube.com/watch?v=nWJj7vOrirQ)**

DreamCompute price with predictive bill, i.e. cheaper. DreamCompute is Openstack-powered public cloud, general available at April 2016. Because Ceph all-SSD copy-on-write, DreamCompute can do fast VM creation. Note that Ceph was created on DreamHost. [Network setup](https://youtu.be/nWJj7vOrirQ?t=8m22s) uses VXLAN managed by Cumulus, encap/decap hardware & white box switch, L3+ serivces via Astara, dual-wired 10G TORs on each rack, TOP uplink at 40G to Spines, 20G effective between every node. [Storage setup](https://youtu.be/nWJj7vOrirQ?t=8m59s): hyper-converged architecture.

**[OVH Building a Public Cloud that Scales](https://www.youtube.com/watch?v=QjNFEzZQlWE)**

OVH is a company name. OVH doesn't use private network, every instance got a public IP. This is a high-level video, introducing how OVH uses their Openstack and how large is it. No much detail.

**[Magnum or Murano? OpenStack Options for Container Environment Creation and Management](https://www.youtube.com/watch?v=Su4X2w-X-IE)**

Present by Mirantis and Intel. The first part is introducting of [Mirantis and its design](https://youtu.be/Su4X2w-X-IE?t=6m12s). Murano is an App catelog. App interoperablity (because MuranoPL is objective language) is a good design. Magnum is a provision platform (plus scaling and management). Magnum vs Murano, the decision is to integrate them both, providing Magnum-based Kubernetes, Swarm, Mesos apps for Murano.

**[FutureCity App Hackathon Showcase](https://www.youtube.com/watch?v=ZyNqEr_EqAg)**

Taiwan Openstack Application Hackathon is launched at 2016 March. This video is basically a promotion of this event. In the end the winner team demo their creation (collect guitar hand motion data and analyze them in Openstack Sahara).

### Popular, But No Time to Watch

Note that several of the popular videos are moved to my "interested" sections.

**[Driving the Future of IT Infrastructure at Volkswagen Group](https://www.youtube.com/watch?v=HL_pzkDnal4)**

**[Cisco - Scaling Containers and OpenStack](https://www.youtube.com/watch?v=Q0G3p4MmRtg)**

**[VMware - IBM + VMware Everything you need to know](https://www.youtube.com/watch?v=4a3EeROQTxI)**

**[DevTest Cloud The Ultimate OpenStack UseCase](https://www.youtube.com/watch?v=co-YOEwBxnw)**

**[OpenShift and OpenStack Devlivering Applications Together](https://www.youtube.com/watch?v=FY--3Ce6isU)**

**[Canonical - Using containers to create the World s fastest OpenS](https://www.youtube.com/watch?v=lM2wwYDLB2M)**

**[OpenStack and the Power of Community-Developed Software](https://www.youtube.com/watch?v=xTM0kFwT6Y8)**

**[Integrate Active Directory with OpenStack Keystone](https://www.youtube.com/watch?v=Hx8Ic3XDi3c)**

**[Erisson - Changing the Context with OpenStack Orchestration to Support SDN/NFV](https://www.youtube.com/watch?v=ZHCMZb1Z7Nc)**

**[OpenStack and Opendaylight The Current Status and Future Direction](https://www.youtube.com/watch?v=HwUdbKdSVIo)**

**[Designing for NFV Lessons Learned from Deploying at Verizon](https://www.youtube.com/watch?v=1aVB3QvEYcI)**

**[Why Betfair Chose OpenStack - the Road to Their Production Private Cloud](https://www.youtube.com/watch?v=-Tmuph-vUWU)**

**[Windows and OpenStack - What s New in Windows Server 2016](https://www.youtube.com/watch?v=QApD3lpsFlQ)**

**[Achieving DevOps for NFV Continuous Delivery on Openstack - Verizon Case Study](https://www.youtube.com/watch?v=hMttg0mpqjM)**

**[A Deep Dive into Project Astara](https://www.youtube.com/watch?v=6pepWOwbmy4)**

**[Managing OpenStack in a Cloud-native Way](https://www.youtube.com/watch?v=EYjOu6ReL4E)**

**[Practical OVN Architecture, Deployment, and Scale of OpenStack](https://www.youtube.com/watch?v=okralc7LrZo)**

**[Tap-As-A-Service What You Need to Know Now](https://www.youtube.com/watch?v=rpIt9K2IsAc)**

**[Deploying Neutron Provider Networking on Top of a L3 Provider Network Using BGP-EVPN](https://www.youtube.com/watch?v=TpKVd0DgDwM)**

### Just Interesting

**[How to Become an Advanced Contributor](https://www.youtube.com/watch?v=LRMBXnYzcP4)**

By Errisson. Get familar with tools, do the dirty work, do code reviews, focus on project/feature, enter large project by code review or priority bugs/features. More advanced, to drive the agenda: know usecases, solutions, why, alternatives, and usability; find supporters via maillist, events; use the [Big Tent](https://www.openstack.org/summit/vancouver-2015/summit-videos/presentation/the-big-tent-a-look-at-the-new-openstack-projects-governance) (to create new project). Inter-project features and communication are becoming more impotant these days. Before start big features, talk with core devs to make sure they support (and align with the project design decisions). Focus, Be professional, Be collaborative.

**[Project Kuryr - Docker Delivered, Kubernetes Next!](https://www.youtube.com/watch?v=EGeTI-tvfqI)**

The problem to solve by Kuryr is the overlay^2 network of VM nested containers, which results in great performance penalty. According to video, I think there isn't much actual progress. Magnum has plan to [integrate](https://www.youtube.com/watch?v=00vo2FtY54Q) with Kuryr. Let's wait.

**[Service Function Chaining Technology Analysis and Perspective](https://www.youtube.com/watch?v=qTUtnosHles)**

Two technologies: NSH-based SFC and MPLS/BGP VPN-based SFC. Comparison at [30m28s](https://youtu.be/qTUtnosHles?t=30m28s). Related platforms: Openstack Tacker as orchestration platform, OpenDaylight SDN Controller, OPNFV Apex Installer Platform, and Custom OVS with NSH patch. There are quite a lot of diversity in the implementation (but not fragmentation, according to the video).

**[Tacker - Building an Open Platform for NFV Orchestration](https://www.youtube.com/watch?v=BQ2ZJWk2VNY)**

Tacker orchestrate VNFs. Tacker Multi-Site allows Operators to place, manage and monitor VNFs in multiple OpenStack sites. It closely works with OPNFV and standard bodies like ETSI NFV and OASIS TOSCA. 99Cloud is the [3rd top contributor](https://youtu.be/BQ2ZJWk2VNY?t=7m4s) of Tacker. The later slides introduces Tacker architecture, how it works, and various features. Multi-site VIM support is interesting.

**[Quantifying the Noisy Neighbor Problem in Openstack](https://www.youtube.com/watch?v=g27Pyz_43J4)**

Presented by ZeroStack. This talk presents how workloads interfere with each other in Openstack, from a several month long study of running workloads in different configurations on ZeroStack. They use micro-benchmarks as well as enterprise workloads such as Hadoop, Jenkins and Redis. The experiment setup is showed in great detail. SSD backends cope with random read/writes well, compared to HDD. Both VM perform well before storage is not saturated, but drop significantly after that. Lessons learned: use SSD, use local storage, don't need to use reliable storage for Hadoop, Cassandra who have in-built replication. Single VM is not able to saturate all 10Gbps NIC due to CPU saturation; throughput is OVS bound; GRE encap/decap consumes high CPU. Suggestions for network: leverage DPDK, explore VLAN-based solutions. Anyway, the overall observations and conclustions are a bit too plain ... I remember that [Google Heracles](http://csl.stanford.edu/~christos/publications/2015.heracles.isca.pdf) have done quite a lot of analysis in depth.

**[Nokia - Combining Neutron, DPDK, Ironic and SRIOV for seamless high-performance networking](https://www.youtube.com/watch?v=GPtgqTRU6gw)**

DPDK, (Ironic,) SR-IOV are new technologies that can significantly boost performance. To use them: SR-IOV VM driver, DPDK VM driver. There are however a lot of issues before make them work together. The later slides focus on them. (However I want to know how to enable DPDK and SR-IOV in compute host or VM: [this](http://dpdk.org/doc/guides/nics/e1000em.html)? [this](https://software.intel.com/en-us/blogs/2015/02/02/openstack-neutron-accelerated-by-dpdk)? ...).

**[Telco Cloud Requirements What VNF s Are Asking For](https://www.youtube.com/watch?v=pd5qoQUVdz8)**

Present by Juniper. Value moves up [The Value Stack](https://youtu.be/pd5qoQUVdz8?t=4m44s) and away from Telo's. The needs are to enable applications which is closer to customers, and ingration of DC existing technologies and network & operations. [Usecases](https://youtu.be/pd5qoQUVdz8?t=11m53s) span from L2-L7 networking, security services, 3GPP, to CDN, voice and video. The current gap of what is needed and what is available requires various of solutoins (or compromises or just wait). Generally this is a pretty good video with deep understanding to the Telco needs.

**[End-To-End Monitoring of OpenStack Cloud](https://www.youtube.com/watch?v=RxUyrOiv_KA)**

Zenoss promoting their monitoring solution: model, events, metrics. It uses no extra agents (use what is [already there](https://youtu.be/RxUyrOiv_KA?t=8m42s)). There is Ceilometer integration from Ceilometer collector; and integration with Neturon, etc. Impact analysis generate a dependency graph to show the risk of a failure. I remember that a new project, [Openstack Vitrage](https://www.youtube.com/watch?v=9Qw5coTLgMo) (invented from Nokia), is able to do root cause analysis; interesting but not receiving much attention yet. Not sure how many machine learning / detection / prediction are actually ready product use. As the slides illustrated, Zenoss monitoring solution is quite comprehensive; wish it is opensource.

### Interesting, But Watch When Have Time

**[DPDK, Collectd & Ceilometer The Missing Link](https://www.youtube.com/watch?v=BdebhsBFEJs)**

**[Deploying OpenStack Using Docker in Production](https://www.youtube.com/watch?v=3pc85InNR20)**

**[Ancestry.com in Production with OpenStack and Kubernetes](https://www.youtube.com/watch?v=UMXfKJL-pXc)**

**[Split Brain Overlays as Seen by Linux Vs. Networking Folks](https://www.youtube.com/watch?v=pb9zGIEeAPI)**

**[Troubleshooting oslo.messaging RabbitMQ issues](https://www.youtube.com/watch?v=WMLFeZG9_so)**

**[Troubleshoot Cloud Networking Like a Pro](https://www.youtube.com/watch?v=0qxgvWMRlBI)**

**[Tuning RabbitMQ at Large Scale Cloud](https://www.youtube.com/watch?v=9hVvlbIzonY)**

**[Achieving Five-Nine of VNF Reliability in Telco-Grade OpenStack](https://www.youtube.com/watch?v=KD9GIXrE-pM)**

**[Optimising NFV Service Chains on Openstack Using Docker](https://www.youtube.com/watch?v=KR1YGiEg3bI)**

**[Nokia - Nokia SDN & NFV: Bringing Dynamic Service Chaining to the Telco Cloud with Nuage Networks & CloudBand](https://www.youtube.com/watch?v=QbfjlNfLGxM)**

**[Neutron Quality of Service, New Features And Future Roadmap](https://www.youtube.com/watch?v=yLol_9BIP38)**

**[Installing, Configuring, and Managing a 300+ OpenStack Node Network In Under An Hour](https://www.youtube.com/watch?v=p1AOHLcSr5s)**

**[High Availability for Pets and Hypervisors - State of The Nation](https://www.youtube.com/watch?v=lddtWUP_IKQ)**

**[Scalable Heat Engine Using Convergence](https://www.youtube.com/watch?v=cz7Yguv_hDw)**

**[Horror Stories How we keep breaking the Scheduler at Scale!](https://www.youtube.com/watch?v=n3z19lk6Aes)**

**[Dive into Nova Scheduler Performance - Where is the Bottleneck](https://www.youtube.com/watch?v=BcHyiOdme2s)**

### vBrownBag

// TODO WIP

### Design Summit (Newton)

// TODO WIP

### Other Sources of Summaries

I like the Openstack Austin Summit observation written by [Sammy Liu](http://www.cnblogs.com/sammyliu/p/5473702.html): Openstack community is marching in the "tier II" area, bigdata, NFV, IoT, blockchain, finance & trading, e-commerce core web servers, etc; VMware is still basically "tier I" however, while in "tier II" its voice is hardly heard. The opinion is very inspiring; but as a comment, I know [CloudFoundry](https://blog.pivotal.io/tag/internet-of-things), which is usually deployed with VMware in commercial use, is an early starter in [IoT](https://www.predix.io/), with [GE](https://blog.pivotal.io/pivotal-cloud-foundry/features/ge-on-cloud-foundry-for-the-internet-of-really-important-things) the big partner; and [Pivotal CF](http://pivotal.io/big-data) is also veteran in bigdata area (while it is true that voice of commerical IaaS & PaaS is very small in Openstack summmit). "Tier II" area is usually done with PaaS, rather than VMware which is IaaS.

Another good summary & video recommendation for the network parts is [Neutron Community Weekly Notes](http://www.wtoutiao.com/p/10bMM1d.html). The official also released their summaries for [Day 1](http://www.openstack.cn/?p=5252), [Day 2](http://www.openstack.cn/?p=5293), [Day 3](http://www.openstack.cn/?p=5299), [Day 4](http://www.openstack.cn/?p=5313); good.

And, usually each release of Openstack will have a release note that summarize major changes (e.g. [Kilo's](https://wiki.openstack.org/wiki/ReleaseNotes/Kilo)). They are very useful. But on Mitaka, [release note](http://releases.openstack.org/mitaka/index.html) is re-organized by projects. They are not as informative as before, but I think still very useful to grasp the lastest updates.

Finally, if you are really interested in the feature & development progress of each Openstack component, I think however checkout the blueprint status on Launchpad is the best way (and checkout the dev maillist).
