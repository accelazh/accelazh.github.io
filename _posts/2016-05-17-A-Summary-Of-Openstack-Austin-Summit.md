---
layout: post
title: "A Summary of Openstack Austin Summit"
tagline : "A Summary of Openstack Austin Summit"
description: "A Summary of Openstack Austin Summit"
category: "Openstack"
tags: [openstack, summit, summary]
---
{% include JB/setup %}

// TODO Work in process, add the key summary for the overall summit

## How to Select Videos to Watch

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

  9. Don't forget #vBrownBag videos ([link](https://www.youtube.com/channel/UCaZf13iWhwnBdpIkrEmHLbA), search "austin"). They are 15min each, but usually very inspiring. #vBrownBag is not part of Openstack Foundation; AFAIK it is a horizontal organization that borrows slots in all sorts of summits.

  10. Checkout the Design Summit ([link](https://wiki.openstack.org/wiki/Design_Summit/Newton/Etherpads)). This is where the next version Openstack (Newton) features are being discussed and planned. Wish there was video. The Etherpads content are pretty condensed, while the best way to understand what core developers have said is to attend on-site.

## Featured Video

After this Openstack Austin Summit, I found out that the official site provided us with a new lively [video page](https://www.openstack.org/videos/featured).

As far as I can see, Openstack Summit is high focusing on users, especially the big users. The most favored content are usecases, practices, experiences, etc. Technical details, black magic, design discussions are not the main theme, however, except that routinely core developers will come to stage and share the newest updates.

For real technical stuff, you may need to attend the [design summit](https://www.openstack.org/summit/austin-2016/summit-schedule/full/) (it spans the full week, with most events scheduled to the last summit day; search "contributors meetup"). The core developers summarize their discussions on [design summit etherpads](https://wiki.openstack.org/wiki/Design_Summit/Newton/Etherpads) (I wish there would be videos too). And remember that, the most cutting edge technical updates always appear on [developer maillist](https://wiki.openstack.org/wiki/Mailing_Lists#Future_Development), where the key is to learn how experts think and discuss upon a new problem.

### [AT&T's Cloud Journey with OpenStack](https://www.openstack.org/videos/video/at-and-ts-cloud-journey-with-openstack)

AT&T is an elder and super user of Openstack. What they favor is common in the community: pen white box architecture, multi-site deploy with combined local and global controllers, no vendor lock-in, and the agility. But essentially I think it is cost-reduction, which is actually the most seen. I can see multi-site Openstack is getting mature and getting adoptted now. Checkout the differences between [zone vs region vs cell vs aggregates](http://docs.openstack.org/openstack-ops/content/scaling.html#segregate_cloud) (Note: Openstack zone is very different from AWS zone). Cell V1 is deprecated, while Cell V2 is still being actively developed ([link](http://docs.openstack.org/developer/nova/cells.html)). Murano is recommended by AT&T, for which I personally like its object-oriented orchestration language; Magnum, however, is not seen. And eventually Mirantis, and its Fuel, is becoming more and more the canonical production-level Openstack distribution.

### [Doubling Performance in Swift with No Code Changes](https://www.openstack.org/videos/video/doubling-performance-in-swift-with-no-code-changes)

It is amazing that Swift, who uses Python as the data path language (with so many C++/C/Golang competitors), becomes such a success today. So tweaking Pythin interpretor is a must-do. I remember that Jython tries to run Python on JVM, leveraging JVM's GC, JIT & Hotspot and performance & maturity; not sure its stats, seems no much adoption. The default Python interpretor is CPython. [PyPy](http://pypy.org/), used in this video, however, features in the JIT, which is famous for interpertors. Using PyPy in Swift to improve performance is straightforward, which should have come out years before (since Swift is written in Python). Now it finally made progress, awesome progress, bravo!

### [Canonical - Carrier grade architecture with public cloud economics](https://www.openstack.org/videos/video/canonical-carrier-grade-architecture-with-public-cloud-economics-the-keys-to-successful-openstack-operations)

NFV is hot and increasingly gaining heat in telecom area to adopt Openstack. But I think they are far from "[carrier grade](https://www.sdxcentral.com/articles/contributed/dont-confuse-high-availability-carrier-grade/2014/04/)" now, the latter demands HA, security, demanding throughput & latency, manageability, and smooth upgrading & patching. for jargon such as Openstack vs OpenDaylight vs Openflow vs Open vSwitch, see [here](https://www.quora.com/What-is-the-relation-between-OpenStack-OpenDaylight-OpenFlow-and-Open-vSwitch-Are-there-other-options-in-place-of-any-of-these). Generally this video gives introduction to Juju (integrated with Ubuntu) that eases Openstack development, and provide support to various aspects such as containers, hyper-converged architecture, software-defined storage, NFV & SDN, deep learning, ceph monitoring. The interesting trends is that, Ubuntu becomes increasingly the canonical platform for Openstack and various opensource software. Although people saying CentOS is more production stable, it seems systemd draws too much repell from the community.

### [Embracing Datacenter Diversity](https://www.openstack.org/videos/video/embracing-datacenter-diversity)

This is a keynote. 7500 people attended Austin Summit on-site (slightly less than 9000 in Tokyo?). A key move from this summit is the [Certified Openstack Adminstrator (COA)](https://www.openstack.org/coa). We can see Openstack is preparing to become a mature industrial foundamental platform; increasingly more [training activities](https://www.openstack.org/summit/austin-2016/summit-schedule/#track=47) occur on the summit, and now we have official Openstack admin certification. In China, [99Cloud](http://www.99cloud.net/html/2016/gongsixinwen_0426/156.html) instantly established the COA training facility. The video released currently voted [Openstack Super Users](http://superuser.openstack.org/) winner: NTT (Tokyo), from nominated candidates: GMO INTERNET, Go Daddy, Overstock, University Federal de Campina Grande, Verzion.

### [AT&T's OpenStack Journey. Driving Enterprise Workloads Using OpenStack as the Unified Control Plane](https://www.openstack.org/videos/video/at-and-ts-openstack-journey-driving-enterprise-workloads-using-openstack-as-the-unified-control-plane)

AT&T is elder. AT&T Integrated Cloud (AIC) starts from Juno, and moving to Mitaka in 2017. Agility, CI/CD, DevOps are the key enabler from Openstack; so like most adoptors, AT&T is using Openstack vastly in the development environment, but seems limitted in production. They use KVM and VMware (vCenter) in hybrid. They need to integrate Openstack with many other things, so writing Fuel plugins is priority, and also need to integrate Fuel with other management tools such as Ansible. Fuel upgradability is the key. There are things that AT&T needs but not present in upstream community, AT&T needs to close the gap itself (and contribute).

### [HPE - Lifecycle Management of OpenStack Using Ansible](https://www.openstack.org/videos/video/hpe-lifecycle-management-of-openstack-using-ansible)

HP Openstack, Helion, is elder, but doesn't perform very successful. HP [shutdown its public cloud](http://www.businessinsider.com/hp-shutting-down-hp-helion-public-cloud-2015-10) in Oct 2015. This video demonstrate HPE's lifecycle management of OpenStack using Ansible. To be honest, this is a hotspot in the past Openstack but already out-dated now (and we have Fuel).

### [Fireside Chat: Mark Collier & Jim Curry](https://www.openstack.org/videos/video/fireside-chat-mark-collier-and-jim-curry)

It is very interesting that this talk tries to dig into venture capitalists' key concerns related to startups based on opensource. For startups, how to evaluate the correct product and market is hard. Another problem is scaling (from small business to big), for example, how to do goto market, how to build the organization and leadership team, how to think about services vs product. Although they are not as familar with the technical part, Venture help beyond money. When enterprise wants technology, they want it standard and know where the support comes from, rather than free cost; the former is what Redhat is doing. Markey dynamics are changing; companies are invest more in opensource rather than proprietary. The speaker expressed concerns about a trend from building great technology to building for money. Opensource vs open-core is interesting; although the later is widely being employed today, but too many companies are burned by their open-core models. Customer expects their vendors to make money (they want healthy vendors), but don't like to be held hostage by them (no vendor lock-in is big concern). The open-core model is slowly dying today (according to the speaker). Next generation angel is a new creation, which requires entrepreneurs to be under age 40, and a commitment that investor spends enough time staying with startups.

### [Intel Sponsor Keynote](https://www.openstack.org/videos/video/intel-sponsor-keynote)

Intel and IBM are radical investors in various opensource ecosystem. It is interesting to think how their strategies differ from other elder IT vendor companies. Recent breakthroughs, DPDK & SPDK, 3D XPoint NVM, Intel PCIe SSDs, and E5 v4 Cloud CPU, from Intel, are bringing great momentum in the storage and cloud world. Native [GPU access in virtual machines](http://www.cnblogs.com/sammyliu/p/5179414.htm) now relies on [Intel GVT](https://01.org/igvt-g); if you remember that [Intel VT](http://www.intel.com/content/www/us/en/virtualization/virtualization-technology/intel-virtualization-technology.html) is one of the beginning foundation of the virtualization age.

### [Mirantis Sponsor Keynote](https://www.openstack.org/videos/video/mirantis-sponsor-keynote)

I can say that, Mirantis makes production-level Openstack distribution public accessable. Tales are that Mirantis before Openstack is nearly bankrupt. But Mirantis grabbed the big oppotunity, and became the canonical Openstack flagship (and gets a lot of financing investments). It doesn't own any single line of proprietary code; the value comes from their selection of bug fixing, patches, and security enhancements, they step further than community, their solid testing, and their good deployment designs ([link](https://www.mirantis.com/blog/mirantis-openstack-real-open-community-development/)). Mirantis is also the top rank [upstream contributor](http://stackalytics.com/?release=mitaka&metric=commits). This video tells an interesting opinion: Openstack is 1 part technology and 9 parts people and process.

### [DevOps At Betfair Using Openstack and SDN](https://www.openstack.org/videos/video/devops-at-betfair-using-openstack-and-sdn)

This video is completely organized as a long and solid demo. Betfair shows how they use their tools and Openstack underlyingly to orchestrate package building, network creating, app deployment, setup loadbalancers, and rolling upgrade their app. It is curious that no one actually use Horizon; they build UI each of their own. In a word, the demo is killer usecase of Openstack in app lifecyle management.

## Keynotes

// TODO Work in process

## Cinder, Ceph and Storage in Openstack 

I'm always interested in Ceph, Cinder and various storage technologies in Openstack, either data path or control path. Recent storage world are quickly evolving: DPDK & SPDK, PCIe SSD, NVMe, NVDIMM, RDMA adoption, smart NIC, Ceph BlueStore, hyper-converged architecture, software-defined storage (SDS), etc. Is an age that

  * Storage is again merging with computing. You can see Ceph (using commodity computing hardwares), and hyper-converged architectures.
  
  * Software-defined datacenter is the future. SDS is one of the pieces.
  
  * Flash is getting more and more adoptted. You can see from SAS/SATA SSD, PCIe SSD/Flash, NVMe SSD/Flash, NVDIMM SSD/Flash, persistent memory, etc, they are quickly climbing up the stack. Storage (and network) is too fast for CPU and memory, so people are finding ways to mitigate the memory bandwidth and PCIe bandwith limits, where you can see DPDK, SPDK, RDMA, etc. Many new technologies bypass the Linux Kernel to achieve lower latency. Also, Kernel page table (and the hardware-assistant MMU) now can be used to address filesystem metadata, see [SIMFS](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?reload=true&arnumber=7304365), interesting.
  
  * Scale-out architecture is the king. I have to say that one reason is Intel cannot build any more scaled-up CPU (and architecture) now, so vendors need the industry to buy-in scale-out strategy. And scale-out is more friendly to the cloud fashion and commodity white box trend.

// TODO Work in process

## Popular Presentations

// TODO Work in process

## vBrownBag

// TODO Work in process

## Design Summit

// TODO Work in process

## Others

I like the Openstack Austin Summit observation written by [Sammy Liu](http://www.cnblogs.com/sammyliu/p/5473702.html): Openstack community is marching in the "tier II" area, bigdata, NFV, IoT, blockchain, finance & trading, e-commerce core web servers, etc; VMware is still basically "tier I" however, while in "tier II" its voice is hardly heard. The opinion is very inspiring; but as a comment, I know [CloudFoundry](https://blog.pivotal.io/tag/internet-of-things), which is usually deployed with VMware in commercial use, is an early starter in [IoT](https://www.predix.io/), with [GE](https://blog.pivotal.io/pivotal-cloud-foundry/features/ge-on-cloud-foundry-for-the-internet-of-really-important-things) the big partner; and [Pivotal CF](http://pivotal.io/big-data) is also veteran in bigdata area (while it is true that voice of commerical IaaS & PaaS is very small in Openstack summmit). "Tier II" area is usually done with PaaS, rather than VMware which is IaaS.
