---
layout: post
title: "A Summary of Openstack Barcelona Summit"
tagline : "A Summary of Openstack Barcelona Summit"
description: "A Summary of Openstack Barcelona Summit"
category: "Ceph"
tags: [openstack, summit, summary]
---
{% include JB/setup %}

Openstack adoption is growing. Interoperability, scaling, baremetal are receiving more attention. Real data heavy services often run on baremetal. Networking VNF/NFV/SDN is hot as always and quick evolving. Openstack competes AWS in cost. Many new projects appears using Ansible to automate Openstack. Sessions about experiences and tunings thrive at the Summit. Mirantis is embracing Kubernetes, on top of which to run Openstack (as upgraded in Fuel). Chinese influence is rising (Gold Members and Superuser Awards).

Besides, checking out blueprints, specs, and design summit etherpads are good ways to understand community direction.

__[OpenStack Newton Release Demo](https://www.youtube.com/watch?v=z6ftW7fUdp4)__    (High clicks)

Just a plain Horizon and commandline demo. Where are the new features?

__[OpenStack for the Work that Matters](https://www.youtube.com/watch?v=GGxzlLwt6WA)__    (Keynote)

China Mobile and 99cloud has enrolled the Gold Member. The Chinese community is winning growing influence. Research 451 reports 37.3% Openstack users are running 1,000+ cores, and 34.4% are running 10,000+ cores. Vlan-aware VMs, Kolla, are brought to stage.

__[Big Data at Banco Santander](https://www.youtube.com/watch?v=3FFTetNKBXg)__    (Keynote) (High clicks)

After good engineering work, big data was enabled in the Openstack cloud. Cloudera certified, Sahara not used. So you see the key issues of big data in Openstack ...

__[Why Sky UK Runs on OpenStack](https://www.youtube.com/watch?v=vW-KWx5RWkI)__    (Keynote)

Key reason to use Openstack: cost, software defined datacenter (and storage, networking), on stop shop for app delivery. Go to stage is also a good chance to ads company products.

__[Huawei Sponsor Keynote: Taking OpenStack to Industries](https://www.youtube.com/watch?v=oPnOTvKX8Ic)__    (Keynote)

Openstack to industry: telco transform via cloud, NFV, public cloud by telco (security, government, network access). Government cloud (江西政府), national enterprise cloud （东风汽车）, are examples.

__[Demo: OpenStack and OPNFV - Keeping Your Mobile Phone Calls Connected](https://www.youtube.com/watch?v=Dvh8q5m9Ahk)__    (Keynote) (High clicks)

Cell-phone network requires 5 nines. Opnfv doctor, initialized by NTT, is the fault management framework by collaborating with various Openstack components such as Aodh and Vitrage. Alarms are monitored and resolved automatically. They demoed by cutting a real server cable on the stage.

__[Deutsche Telekom Sponsor Keynote- DTAG- Unlocking the Public Cloud Potential of OpenStack](https://www.youtube.com/watch?v=qIvNgSiOJkQ)__    (Keynote)

I didn't realize what is being talked before this talk finished.

__[Superuser Award](https://www.youtube.com/watch?v=YrEkBa4aiyQ)__    (Keynote)

China Mobile: Release cycle has been shorten from half a year to a month.

__[Smashing Particles, Revolutionizing Medicine and Exploring Origins of the Galaxy]()__    (Keynote)

Openstack is useful in research centers for data analyzing. CERN is a well-known superuser from early years of Openstack. There are 4 keynote sessions in series. As I know, Tsinghua University is also using Openstack (enabled by EasyStack).

__[The Future is Multi-Cloud](https://www.youtube.com/watch?v=t8IiULAPKwo)__    (Keynote)

Openstack community is putting increasing effort on multi-cloud from recent cycles. I didn't realize what is being talked related to multi-cloud before this talk finished.

__[OpenStack Security Team Receives CII Badge](https://www.youtube.com/watch?v=bCb6E1QV7_s)__    (Keynote)

About the security best practice badges.

__[Containers on Bare Metal for Game Developer Crowdstar](https://www.youtube.com/watch?v=IUOWYxaLhQc)__    (Keynote)

By Crowdstar company. Baremetal: performance, cost effective, fast deployment. Container: simplicity and isolation safety.

__[IBM Sponsor Keynote: Why Enterprise Clients are Serious About OpenStack](https://www.youtube.com/watch?v=Z6kmgGHEyYs)__    (Keynote)

IBM are committed to demonstrate interoperability.

__[OpenStack Interoperability Challenge: Running Unmodified Apps in Any OpenStack Cloud](https://www.youtube.com/watch?v=CqNFcuJfZ_Y)__    (Keynote)

The demo brings tens of different companies, and shows that their Openstacks running on different environments (even on ARM) supports the same set of API and achieves the same deployment results. RefStack is the toolset for testing interoperability between OpenStack clouds. So, the essence of interoperability is sharing the same API, what about invoking each other cloud?

__[Demoing the World's Largest Multi-Cloud CI Application](https://www.youtube.com/watch?v=b5PRk69EMuA)__    (Keynote)

The OpenStack infra team manages the world's largest CI infrastructure, spinning up two thousand jobs per hour.

__[Scaling OpenStack to Support Large Scale Compute – 500 Computes and Beyond](https://www.youtube.com/watch?v=eLd3ZBhPbFk)__    (vBrownBag)

OpenStack has known scalability limitations and scaling beyond 100-200 compute nodes per single OpenStack instance (Region). Deploying multiple small OpenStack instances (region) instead of a single large one is more favorable. Neutron, MySQL, Nova Scheduler, RabbitMQ, Ceilometer are known to need increasing (left to right) tuning to support scale.

__[New in Swift: Object Encryption](https://www.youtube.com/watch?v=RB3uEPyYUe0)__

In the Newton cycle, Swift released the new feature of encryption at rest. Data is encrypted at proxy server by Swift encryption middleware. Key management is integrated into Barbican. The cipher is AES of 256-bit keys.

__[Beyond Object Storage - A Unified Storage Architecture for IoT](https://www.youtube.com/watch?v=yPnvMT_XMbI)__    (vBrownBag)

Object storage is suitable for IoT, but it fails for realtime processing. Another issue is the in-place analytics of object storage. IBM Spectrum Scale comes to help.

__[Chasing 1000 Nodes Scale](https://www.youtube.com/watch?v=XURkQ3biF6w)__

A new Openstack Performance Team work group from Mitaka. It is part of Large Deployment Team. Key tools: Rally, Shaker, os-faults, OSprofiler, sysbench, oslo.messaging simulator. Tested CPU and mem usage under load. But that's far from enough for the know Openstack scalability issues.

__[Deploying OpenStack with Neutron and Ceph- From Concept to Public Cloud (and Hell in the Middle)](https://www.youtube.com/watch?v=pKhZpBc9srA)__

By Dreamhost. Good sharing. Storage learnings: far over-provisioned storage; spinning disks are far too slow and failure prone; separate storage nodes drastically increase cost; Ceph wants RAW image for CoW, users prefer smaller formats, and Openstack has a poor image conversion experience for now. Network learnings: Cumulus Linux and whitebox switching are good; creating Astara requires an enormous effort; router VMs are SPOF and requires RAM; SDN/OVS platforms scale issues, proprietary, magical. Compute learnings: customer want faster cores, not more cores. Adjustments: hypervisors and storage are now colocated, moved from AMD to Intel processors, all-SSD storage, Neutron with DVR, SDN use VXLAN.

__[Perform Schema Rolling Upgrades in Just One Release Cycle](https://www.youtube.com/watch?v=juunf0u4cyo)__    (Upstream)

Oslo versioned objects, RPC messaging versioning. Expand-contract: write to new SQL column, read from both old and new column. Triggers: sync new to old when written. Summary of steps: download new code; run expand, installing triggers; roll out new version; run contract, removing triggers, old schemas and data.

__[I Found a Security Bug: What Happens Next?](https://www.youtube.com/watch?v=GJx3yBN9blY)__

The VMT process: implement the patch and send CVE, first embargoed disclusure early to critical users, next public disclusure.

__[Karbor - An Ecosystem for Data Protection Providers](https://www.youtube.com/watch?v=YFfcmGMn3M4)__

Karbor protects the deployment metadata of an app on Openstack by backup or replication. It provides the standard API fragment work the plugin system. Huawei and Smaug are active on this project.

__[OpenStack Scale and Performance Testing with Browbeat](https://www.youtube.com/watch?v=ch_rCyGQhYM)__

A set of Ansible playbooks to help check deployment for known issues, and to find out the optimal parameters, for example the number of database connections a given OpenStack deployment uses. Zero to performance testing. Check, stress test, analyze, tune, and iterate again.

__[Monasca: One Year Later](https://www.youtube.com/watch?v=9fo7WlCzqf8)__

New features that have been added: deterministic alarms; non-periodic notifications; alarms on logs, correlation of metrics and logs; OVS vSwitch monitoring. Major new areas of development: monasca log API; monasca transform and aggregation engine; monasca analytics.

__[Moving Large Workloads from a Public Cloud to an OpenStack Private Cloud- Is It Really Worth It?](https://www.youtube.com/watch?v=K4hoBOyCLF0)__

Good talk. Why not public cloud: the high volume and low latency traffic makes the proximity to some partners matter; huge datasets used for decisioning require high performance infrastruct, which costs a lot; instances' packet per second limitations leads to poor performance and excessively large instance size, especially for loadbalancers; network disruptions with no root causes. So, in general, it is the higher performance needs, performance stability, and location proximity. I wonder how AWS copes with these issues.

TCO analysis needs to decide plans for overcommit, availability trade-offs, changs of the test environment and R&D environment, datacenter locations and bandwidth, etc. The redeployment goes in 4 locations and 3 continents, in 3 years, using Openstack and baremetal, with 3 dedicated engineers (So few people. but I heard China Mobile only uses 2 dedicated engineers for the production Openstack, although they sometime "borrow" more people from other teams). In the resulting in-house production environment, they decreased instance sizes by 40% and loadbalancers by 95%; loadbalancers and core data services run on baremetal and leverage VLANs; 30% cost saving in total; the improved visibility for network traffic and full application stack helped for troubleshooting and performance improvements.

__[Project Independent Key Management](https://www.youtube.com/watch?v=9yQxE2yeBcM)__    (vBrownBag)

The key manager is useful for： as a centralized location to store your keys; to provide logging to show who is accessing your keys; to provide automation for accessing keys. Castellan provides a generic key manager interface, includes configurable backends, and developed by the Barbican team. Compared to Barbican, Castellan provides the abstraction layer that allow users to replace Barbican with other backends (e.g. to deploy your app on cloud without Barbican). Another backend is KMIP (work-in-progress).

__[Hiding in the Clouds: Secret Management with OpenStack Barbican](https://www.youtube.com/watch?v=_tAxATMXuxE)__    (vBrownBag)

A talk to introduce Barbican.

__[Building Large Scale Private Clouds with OpenStack and Ceph](https://www.youtube.com/watch?v=dO2LAklak74)__

By Walmart.

Current Ceph all-SSD node config: 128GB RAM, 24 physical cores (48 threads), dual 10Gb NIC, 10 SATA SSD, 1 NVMe device. Issues: dual CPU sockets cause NUMA issues; dual 10Gb networking is not enough bandwidth; dual disk controllers is not ideal (want to go with single controllers); want OEM to provide better tailored box for Ceph.

Future all-SSD Ceph node config: single CPU socket; all NVMe chassis; lower endurance flash (storage tiering for performance and endurance); single power supply; fail-in-place planned design; lower CPU core count?. Current challenges with Ceph block storage: low latency for small-queue-depth workloads; automation tooling for common ops; bugs not-solved.

Current spinning Ceph node config: 128GB RAM; 24 physical cores (48 threads); dual 10/25 Gb network; 12 SATA dense spinning disks; 1 NVMe/SSD device; bcache/LVM cache. Challenges serving big data: Ceph Jewel RGW bugs; scaling RGWs to meet number of concurrent connections; scaling RGWs bandwidth to over 30 Gbps; SwiftFS bugs with Ceph RGW.

__[Kerberos and Health Checks and Bare Metal, Oh My! Updates to OpenStack Sahara in Newton](https://www.youtube.com/watch?v=jesJCUOyD7M)__    (Upstream)

New features: event logs for cluster, health checks for cluster; more kerberos security features were implemented; some image generation improves; better ironic integration to improve baremetal experiences; Designate integration; API pagination; new plugin versions; Sahara tests framework to validate environment readiness.

__[VNF Managers - You Must Know](https://www.youtube.com/watch?v=FoImOGfiNSM)__

Virtual Network Function Managers (VNFM) are key components in NFV MANO framework. It works with Network Function Virtualization Orchestrator (NFVO) and Virtual Infrastructure Manager (VIM), for the lifecycle management of VNFs under the control of the NFVO, which it achieves by invoking to VIM. VNFM operations include: Instantiation of VNFs; Scaling of VNFs; Updating and/or upgrading VNFs; Termination of VNFs. See [\[1\]](https://www.sdxcentral.com/nfv/definitions/vnf-manager-vnfm-definition/)[\[2\]](https://www.sdxcentral.com/nfv/definitions/nfv-mano/).

__[Can OpenStack Beat Amazon AWS in Price?](https://www.youtube.com/watch?v=8bkeOg4tSW4)__

Good sharing. By Internap (and Catalyst IT). TCO model in detailed numbers, for both AWS and Openstack. The [spreadsheets](http://bit.ly/2dFGvfQ) are very useful. According to the minimum variable comparison, Openstack compute resource is 0.1x the cost of AWS, and storage resource is 0.4x. For a simple marketing webset, Openstack cost is 0.7x of AWS. For a large web application, Openstack costs 0.1x of AWS. For big data, Openstack costs 0.1x of AWS. The cost of developers are not counted in.

__[RabbitMQ at Scale, Lessons Learned](https://www.youtube.com/watch?v=bpmgxrPOrZw)__

Good sharing. A detailed configuration guide for RabbitMQ when your Openstack cluster grows larger. RabbitMQ is known to have issue for a large scale Openstack deployment. The talk also shares how to monitor RabbitMQ. Ceilomter and Heat should use a separated RabbitMQ cluster.

__[Ceph Performance on OpenStack (Over 50,000 Benchmarks!)](https://www.youtube.com/watch?v=iae9BPb1xrk)__    (vBrownBag)

It can be used as Ceph performance tuning baseline (but the performance results are too slow?). BlueStore still has data loss bug.

__[Trusted IoT (Internet of Things) on OpenStack Integrated Container Framework](https://www.youtube.com/watch?v=gAcGQq8w3O4)__    (vBrownBag)

Containerization of residential gateway. CI/CD on cloud end, and push to residential edge devices. Security: blockchain signed & encrypted, secure end2end IoT channel.

__[Toward 10,000 Containers on OpenStack](https://www.youtube.com/watch?v=hRCzj8Ds9K4)__

For CERN, 10,000 containers are too less. Benchmarking how well Magnum deploys Kubernetes. A 1000 nodes (4000 cores, 8000 GB RAM) kubernetes deployment took 23 minutes. It needs a series of scalability tuning. Next is the benchmark and tuning at CNCF. Existing issues: Openstack scaling and stability; linear scaling in Heat and Keystone; using UUID tokens and token validation in Keystone are too slow. Best practices: tune RabbitMQ and Heat; various trade-offs.

__[Holistic Security for OpenStack Clouds](https://www.youtube.com/watch?v=ehfSLZVCVLA)__

Good sharing. Few talks security with the big picture. This talk is at principle level. Build small security improvements at multiple layers.

Four layers, and the principles for each:

  * Outer perimeters

      * Security goal: Convince your attackers that it’s easier to attack someone else’s cloud

      * Key concpets
          * Make it expensive for attackers to breach your perimeter defense
          * When they do make it through, ensure that you know about it immediately
          * Perimeters usually have openings on the outside and inside -- secure both of them

      * Tactical objectives
          * Require a VPN for access from external networks
          * Segregate internal networks using a firewall or an internally-facing VPN
          * Monitor all logins (successful and unsuccessful) for unusual activity
          * Track bandwidth usage trends using netflow data

  * Control and data plane

      * Security goal: Keep the inner workings of your OpenStack cloud separated from tenant infrastructure

      * Key concpets
          * Tenant infrastructure should have extremely limited access to the control plane, and vice versa
          * A misconfigured tenant VM could open a wide hole in your secure network
          * Protect your cloud from VM exit exploits that allow attackers to gain hypervisor access

      * Tactical objectives
          * Separate control plane, hypervisors and tenant infrastructure with VLANs and strict firewall rules (and monitor dropped packets)
          * Use SELinux or AppArmor on hypervisors to reduce the impact of VM and container exit exploits
          * Hypervisor Linux Security Module refresher
              * Three popular implementations: SELinux, AppArmor, and TOMOYO.
              * sVirt (in libvirt) ensures that all processes are labeled properly (SELinux) or have profiles configured (AppArmor)

  * Control plan deep dive - the backend services (e.g. mysql, rabbitmq, memcached, syslog)

      * Security goal: Heavily restrict lateral movement and restrict access to the "crown jewels". "Crown jewels" are the databases and message queues in your OpenStack cloud.

      * Key concpets
          * Allow the least amount of access possible from the OpenStack services to backend services
          * Further restrict access to specific ports, sources, and destinations
          * Deploy services into containers to apply fine-tuned network and process restrictions

      * Tactical objectives
          * Use a load balancer or firewall to create a “choke point” between OpenStack and backend services
          * Monitor messaging and database performance closely to look for anomalies or unauthorized access
          * Use unique credentials for each MySQL database and RabbitMQ virtual host

  * Openstack services deep dive

      * Security goal: Know what valid communication looks like and alert on everything else. OpenStack has many (predictable) interactions.

      * Key concpets
          * OpenStack services are heavily interconnected, but the connections are predictable
          * Limit access between OpenStack services and monitor any invalid questions

      * Tactical objectives
          * Use iptables rules to limit access between OpenStack services; alert on any invalid connections
          * Give each service a different keystone service account (with different credentials)
          * Monitor closely for high bandwidth usage and high connection counts

Analyze. Isolate. Monitor. Repeat. Build small walls and eliminates the small holes. Small security changes add up to a strong defense.

__[Delivering High Performance OpenStack Storage Solutions with NVMe SSD and Intel® Optane™ Technology](https://www.youtube.com/watch?v=BPi0-pTNSmo)__    (vBrownBag)

Ceph on Intel 3D NAND: random write latency 5.94ms, 270K IOPS * 4K block. 1.5 performance improvement after various tunings; RocksDB has significant performance impact. Intel invests on Optane (3D XPoint) and 3D NAND.

__[Ceph OSD Hardware - A Pragmatic Guide](https://www.youtube.com/watch?v=kc7GIHyk57M)__

Good sharing. key points blow

  * Fat vs thin: more nodes with fewer disks each, or fewer nodes with more disks each?
      * Fat nodes: cheaper per PB but harder to manage. If one node goes down, you have more disks to recover. Good choice if you can afford many (6 to 10+) of them.
      * Thin nodes: faster recovery if node goes down. Typically 1 socket is enough (no NUMA). But need more rack space, and more power. Good choice to start out.

  * Networking for Openstack + Ceph
      * Single fabric: cheaper but lower throughput and high latency under pressure.
      * Multiple fabric (dedicated network fabric): each one set of fabric for VMs, for accessing Ceph, and for OSD data replication. Expensive.
      * Multiple IPs/NICs: Hypervisors: 10 GigE for VMs, 10 GigE for accessing Ceph, and optionally 1 GigE for management. Ceph OSDs: 10 GigE for accessing Ceph, 10 GigE for OSD data replication, and optionally 1 GigE for management.
      * Don't 1 GigE network.

  * Disks
      * What is the disk bandwidth to be saturated by network bandwidth?
      * 1 GigE (128MB/s) won't saturate a SATA SSD (~400 MB/s seq w.). 10 GigE (1280 MB/s) won't saturate a PCIe SSD (~2000 MB/s seq w.)

  * Cores and sockets
      * 1 socket is a safe choice, to avoid NUMA issues. For NUMA, pin OSD daemons to sockets; but, example: 10 GigE on socket A, OSD node on socket B, PCIe SSD journal on socket A.
      * 1 CPU core per daemon/disk. 1 SATA SSD journal per ~4-6 HDD disks. 1 PCIe SSD journal per ~6-20 HDD disks.
      * HT cores vs physical cores? Disable hyper-threads or not?

  * Memory size
      * 0.5 GB - 1 GB per TB per daemon. More is better (for Linux VFS caching).

So, network fabric determines number of disks, with fat vs thin, it then determines CPU and memory size. Network bandwidth and data amount together also majorly determines your reliability target (you need enough bandwidth to recover enough lost data).

__[From Neutron to Neutron- SDN-Driven Backbone Traffic Engineering](https://www.youtube.com/watch?v=7yctjjic0Kk)__

End-to-end traffic engineering today: DC and backbone have decoupled control planes; backbone conducts its own capapcity planning based on demand forcast. The model presented will enable seamless end-to-end service and traffic engineering from host to host and/or ToR to ToR across large National Service Provider backbones.

__[Sleep Better at Night- OpenStack Cloud Auto--Healing](https://www.youtube.com/watch?v=08eA2ShyFa4)__

Monitoring, metering, alerting: Zabbix, Nagios, Prometheus, PagerDuty; Volta (log monitoring) by Logstash, Kafka broker, ElasticSearch, InfluxDB (for metrics), Grafana/Kibana; synthetic transactions; health dashboards.

Auto-remediation: alert triggered -> is known problem -> yes -> auto-remediation workflow (e.g. Mistral) executed -> fixed? -> done. Other auto-remediation systems: Facebook FBAR, Linkedin Nurse, Netflix Winston, Google, Github, Paypal. StackStorm is an opensource event-driven auto-remediation framework.

__[Scaling Up OpenStack Networking with Routed Networks](https://www.youtube.com/watch?v=HwQFmzXdqZM)__    (Upstream)

Neutron's Routed Networks functionality which was added during the Newton cycle. Routed Networks rely on a layer 3 architecture that routes traffic to small segments of the network to achieve scale. This approach serves well deployments where large scale is a paramount requirement and users just need a set of VMs with IP addresses (just boot to public network).

__[Ceph, Now and Later- Our Plan for Open Unified Cloud Storage](https://www.youtube.com/watch?v=WgMabG5f9IM&t=17s)__    (Upstream) (High clicks)

Good sharing. Ceph the unified storage: single cluster to server all APIs (file, object, block), for the space efficiency, ease of management, simplicity of skillsets and staff.

Major new features at Kraken:

  * BlueStore: cut-off the entire layer and write directly to block device; ~2x faster than FileStore; better parallelism; plan to be stable at Kraken, and ready for broad at Luminous.

  * AsyncMessenger (XSKY): replaces aging SimpleMessenger; scales better; now the default!; pluggable backends (Linux sockets, DPDK, RDMA).

Major new features at Luminous:

  * Multi-MDS CephFS stable.

  * Erasure code overwrites: the current implementation only allows you to append erasure coded objects; EC overwrites will enable RBD and CephFS to consume EC pools directly (it's hard, but huge impact on TCO).

  * Ceph-MGR: ceph-mon daemons currently do a lot, which limits cluster scalability; ceph-mgr moves non-critical metrics into a separated daemon, which can be streamed to graphite and influxdb, and it a good host for Calamari REST API endpoint.

  * Quality of service: more ganularities; based on mClock paper from OSDI'10.

  * RDB ordered writeback cache: use VM local SSD reduces latency, but how to crash consistency?; with ordered writeback, the backend writes may be stale but is crash consistent; RBD image is always point-in-time consistent.

In the future, most bytes will be stored in objects. RADOSGW is increasingly important, and the key features are

  * Multisite federation
  * Tiering
  * Erasure coding
  * WORM (write once, read many)
  * S3, Swift
  * Compression
  * Deduplication
  * Encryption
  * Multisite replication

The new features of RADOSGW in this new release

  * RADOSGW indexing: RADOSGW gateways talking to each other to do asynchronized replication. And we extended it to add a cluster to only replicate metadata and push it to ElasticSearch.

__[Kuryr - Here Comes Advanced Services for Container Networking!](https://www.youtube.com/watch?v=ymDGG5oyVDM)__    (Upstream)

The overlay^2 for VM nested containers problem. Current status: supports Docker networking (CNM) - libnetwork. So is the overlay^2 problem solved or not? It seems the progress didn't change much from the last Summit.

__[Zuul v3- OpenStack and Ansible Native CICD](https://www.youtube.com/watch?v=R4EmE1QEvNU)__    (Upstream)

Openstack CI/CD is one of the worlds largest and the most successful ones.

__[Introducing OpenStack Omni: Using Horizon to Manage OpenStack and AWS](https://www.youtube.com/watch?v=upW0ufgVp5g)__    (Keynote)

Why do trade organizeations choose Openstack: 92% standardize on the same open platform & APIs; 92% avoid vendor lock-in; 87% deploying applications faster; 80% increase operational efficiency; 72% save money.

The Horizon panels can connect to AWS and manage clusters deployed on AWS. The demo showed how we can create all sorts of resources and map floating IPs at Horizon, and see them on AWS.

__[Magnum is Not the OpenStack Containers Service? How about Zun?](https://www.youtube.com/watch?v=Go8_G3iLyl4)__    (Upstream)

Renamed from Higgins, jointly created by former Nova-docker developers. Zun: map Magnum deployed COEs (Kubernetes, Swarm, etc) into Openstack API. The inter-connect architecture diagram at [5m59s](https://youtu.be/Go8_G3iLyl4?t=5m59s) is useful.

__[On Building an Auto-healing Resource Cluster using Senlin](https://www.youtube.com/watch?v=bmdU_m6vRZc)__    (Upstream)

Senlin: Profiles - a specification of objects to be managed, Policies - rules to be checked/enforced before/after actions are performed. Senlin engine helps you orchestrate HA procedure: Redundancy -> Monitor -> Failure -> Fencing -> Recovery. It seems Senlin is taking a very generic view, "Profile" and "Policy", to cluster management, which can be used in more wider areas. What's the difference from a workflow engine, such as Mistral.

__[Cinder Project Update](https://www.youtube.com/watch?v=6YeX2veJF9o)__    (Upstream)

New backend drivers. Added "unsupported drivers" check.

User Messages APIs that allow user to see error messages for asynchronous operations. Added stochastic weight handler for scheduler, and checks for extra specs "provisioning:type". Generic Volume Groups, a grouping construct that allows volumes used in the same application to be managed together.  Encrypted volumes and Castellan Key Manager interface.

Admin can modify quota for all projects. Active-Active HA (making progress). Multi-attach (making progress). Rolling upgrades (making progress). OS-brick added new connectors.

What's coming in Ocata? Improve test coverage. Continuation of rolling upgrades. Continuation of active-active HA. Continue to work with multiattach.

__[What's New in OpenStack File Share Services (Manila)](https://www.youtube.com/watch?v=Ek4oeQpWzsA)__    (Upstream)

Newton release: production ready with enhanced capabilities.

__[OpenStack and Ansible- Automation Born in the Cloud](https://www.youtube.com/watch?v=OaptTKpAfKQ)__    (High clicks)

A plain introduction to Ansible and Ansible Tower. Ansible is being used more and more in Openstack. It has interoperable integration with Heat templates.

__[Delivering Hybrid Bare-metal and Virtual Infrastructure Using Ironic and OpenStack](https://www.youtube.com/watch?v=mc1zN0xdDOs)__    (High clicks)

By Internap. Intermap is a big user for baremetal and Ironic; people are willing to hear. Hybrid infrastructure with baremetal (and VMs). Baremetal is gaining more heat in this Summit; it seems serious customers use more baremetal, although Openstack is born from virtual machines. Bifrost is a set of Ansible playbooks that automates baremetal provisioning. Internap built Netman to address the tenant isolation gap in Openstack Ironic.

__[Mirantis- Integrating NVMe over Fabric into OpenStack](https://www.youtube.com/watch?v=fTPe0sOHU0w)__

Create a Cinder driver for Intel SPDK as the reference implementation of NVMe-oF Target.

__[Cinder Always On - Reliability And Scalability Guide](https://www.youtube.com/watch?v=VjQ6D4IZMBk)__

Introduction to Cinder, and service-level and volume-level features related to reliability.

__[Datera- Reconciling Intent Defined Storage with Cinder's Volume-Centric Model](https://www.youtube.com/watch?v=4SigCCyJgsQ)__

Datera EDF templates.

__[Understanding Cinder Performance in an OpenStack Environment](https://www.youtube.com/watch?v=UvF1q1Qb0sI)__

Use Cinder LVM. It can be performant. It can do HA.

__[Mirantis- Evolve or Die- Enterprise Ready OpenStack Upgrades with Kubernetes](https://www.youtube.com/watch?v=ZIPe1XxShmI)__    (High clicks)

New Fuel architecture: baremetal, then Kubernetes, and then Openstack components running in container pods. Openstack compute: Libvirt & nova-compute in k8s pod; OpenContrail in host OS; Calico as network plugin for k8s. The Gerrit & Jekins CI is integrated, rolling upgrade of Openstack components can be done by Kubernetes.

The demoed use cases are powerful to show how Kubernetes helps Openstack operation

  * Deploy Openstack on Kubernetes
  * Scale up/out Openstack Components
  * Configuration Changes in Openstack Nova
  * Upgrade Openstack Cinder from Mitaka to Newton

But, if Openstack runs on top of Kubernetes, then what's the position of Openstack's container services, such as Magnum, Zun, Kuryr, etc?

__[Innovation at BBVA- Next Generation Overlay for Kubernetes and OpenStack](https://www.youtube.com/watch?v=QyGHZ2HCwqY)__    (High clicks)

Run Openstack on top of Kubernetes. Underlyingly it runs Rancher + K8s.

__[Public or Private Cloud, Amazon Web Services or OpenStack](https://www.youtube.com/watch?v=NtxmacNl9b0)__    (Vancouver Summit)

Comparing Openstack and AWS. What business is suitable for each. Plain comparison. Redhat Open Hybrid Cloud help you manage both Openstack and AWS in one platform.
