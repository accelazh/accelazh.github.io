---
layout: post
title: "Openstack Tokyo Summit Notes"
tagline : "Openstack Tokyo Summit Notes"
description: "Openstack Tokyo Summit Notes"
category: "openstack"
tags: [openstack, summit, tokyo]
---
{% include JB/setup %}

The Openstack Tokyo Summit, Oct.27 - Oct.30 2015, releases the Libery and designs the Mitaka. Schedule page at [here](http://openstack.org/summit/tokyo-2015/schedule/). Overall Keystone Federation (and multisite Openstack) was greatly enhanced and actively discussed. More integration remains underworking with Cinder, Nova, etc. Neutron added various new features, and we got Kuryr. NFV and NFV orchestration were hot topics whose rooms were always packed. Magnum positioned itself as the implementation of OCI (Open Containre Initiative) and CNCF (Cloud Native Computing Foundation). Ceph added PMstore (Persistent Memory store), RDMA (Remote DMA) support, XIO Messenger.

Below is my meeting notes. No warranty for my listening skills :-P

### Openstack Tokyo Summit Day 1 Oct.27

```
Openstack Summit Keynote:

    Jonathan Bryce Exec director @ Openstack Foundation: General Introduction
        Openstack now has Certificate for Openstack Administrator. You can attend the test.
        Introduction to Openstack development model vs common enterprise projects
        Introduction to Openstack sub-projects
        How to get involved in Def Core: 1) by providing data 2) participant in Def Core meeting
        Openstack adoption in market. The picture is each sub-project level, e.g. Magnum adoption rate.
        New Openstack project status page released. See each sub-project maturity status. Check it at: http://www.openstack.org/software/project-navigator
        Openstack is powerful vs docker/k8s because by one platform you have all models: VM, baremetal, container on VM, container on baremetal
        Federated Identity released in Kilo and keep being contributed in Liberty
        Super User awards: winner is NTT Group. See who is greatly using Openstack here.
        
    Lachlan Evenson Cloud Platform Engineering Team Lead @ Lithium Technologies: Use container on Openstack to quickly deploy infra with no engineering effort
        Be able to deploy container cloud on Openstack in less than 2 weeks. Awesome demo pages. All in pods ready for you.
        Kubot. A chat robot who you can ask to operate k8s, e.g. scale out.
        Demo the change code and quickly re-deploy the crocodile game
        
    Takuya Ito Sr. Manager of Infra Engineering and Openstack Blackbelt @ Openstack use case in Yahoo JP
        The scale: 61B page view per month. 20PB in data storage. 20+ clusters operating. 50000+ instances.
        The crazy workload spike (+300%) when a nature disaster happens. We have mission-critical applications on Openstack.
        Our mission is to make abstraction of the datacenter, with Openstack as the core. Common APIs are important.
        
Shingled Magnetic Recording (SMR) Drivers and Swift Object Storage

    Various tests are carried out on SMR. Use a Swift Simulator to understand how SMR performances.
        Increase the concurrency and workloads until the performance deteriorates to be unusable. 
        Drive managed vs Host managed
        Write vs Write-Heavy Read/Write vs Read.
        SMR Drive vs PMR Direct Access vs PMR No Direct Access
        Many other tests ... SMR is not performing well vs PMR
    
    Should we deploy SMR on Swift?
        You should not use SMR Driver on Swift. It brings performance drops, especially for small objects. It doesn't worth the storage density gained.
        Don't use SMR for general purpose. Use it for Swift with large object or very large bandwidth ingest.
        Good for use cases such as video surveillance cases, DNA analytics
    
    Future work
        Make it more configurable for the operator.
        SMR native filesystems. Teach Swift to speak SMR.
    
    Good questions audience asked
        Cache tiering with SMR? No such much related. We could use it if we implement tiering which supports SMR.
        Host aware drivers? Not quite available now. There are papers and academic discussions.
        
Full Stack Application Security in the Cloud

    The speaker didn't show up, the speech magically disappeared and jumped to the next one.

Running Openstack for Several Years and Live to Tell the Tale: by Redhat

    Undercloud
        RHEL + TripleO deployed via Kilo
        Ironic
            benchmarking you hardware is highly recommended
            Upload hardware profile to Swift
        Heat
            customize TripleO template to deploy Overcloud
            Configure Overcloud with PUppet

    Reference Architecture
        Controller 3+2n, Compute X, Storage X nodes
        Network isolation: provisioning/mgmt, internal API, tenant networks, storage, storage mgmt, external API & floating IP
    
    Logging
        Centralized logging by Fluentd + Kibana + Elasticsearch
         
    Monitoring
        Sensu with Uchiwa dashboard
        System checks + Openstack checks. A lot of them.
        
    Backup
        Run from external server.
        Only backup Ceph volumes
        Full and incremental
     
    Tips and Tricks
        Sync time with NTP across your servers
        Network MTU 9000 if hardware supports jumbo frame. Disable TSO, GSO. Disable rp_filter. Disable GRO, GSO, LRO.
        HAProxy increase maxconn. Increase Galera timeout. Increase RabbitMQ timeout.
        RabbitMQ limits: `rabbitmqctl status | grep file_descriptors -A4` increase it
        Set rabbit_durable_queue. Set rabbit_ha_quque. Set expire policy to avoid amount of orphans queue.
        MySQL increase open_files_limit, LimitNOFILE, max_connections. Monitor the number of active connections
        And more. Check the published video on Youtube
        
Hyperconverged for Openstack environments, does it make sense

    Convergence is the third wave of human evolving. Multi-vendor converged; single vendor converged; Hyper converged. 
    
    From software defined infra to webscale IT
    
    features of 3rd wave convergence.
        Efficient data management
        Infra convergence
        Scalability
        VM Centricity: primary focus on the virtualized workloads, no baremetal
        Unified management
    
    Customer space of where hyperconverged models emerge
        Hyperscalers / Web giants
        Service provider - Telecoms
        Managed Openstack
        Distros
        DIY
    
Multisite Openstack - Deep Dive

    Even the doorway is packed up with people. Highly recommend this session.
    When try to connect the network between two sites, the IPs, MACs and router tables may change after VM migration. They have implemented the cross-site router to handle it.
    Cross-site firewall is relatively easy to implement. They also implement the cross-site loadbalancer.
    Router peering creates a link between two sites. L2 and L3 network connectivity involves a lot work.

The Container Ecosystem, the Openstack Magnum Project, the Open Container Initiative, and You: by IBM

    Containers isolate the process resources, share host kernel and avoid hardware emulation, package app dependencies, easy to run and move. But there are cost
    Containers are not new, it starts from FreeBSD Jail, to Linux-VServer, to Solaries Zones.
    Existing container efforts in Openstack: Nova docker driver, a plugin for Heat to orchestrate docker resources, Kolla containerized Openstack services, Murano market place catelog, Magnum to manage CaaS

    Magnum implements OCI & CNCF.
        Introduction to Magnum team history, status and architecture
        Introduction Linux Foundation Open Container Initiative (OCI). OCI is lightweight. OCI is not bound to higher level constructs such as particular client or orchestration. OCI aims to meld Docker vs CoreOS Rocket. OCI specifies OCF (Open Container Format).
        Introduction of the Cloud Native Computing Foundation (CNCF). Container packaged, dynamically managed, micro-service focused. OCI specifies container format. CNCF specifies container platform common parts. OCI targets container image portability. CNCF targets container application portability.
        Magnum implements OCI & CNCF. You can see how Magnum positions itself now.
```

### Openstack Tokyo Summit Day 2 Oct.28

```
Openstack Summit Keynote

    Neutron is the most actively developed project in Openstack, about 30% growth of production adoption last year. SDN market grows fast.
    Neutron functional decomposed: virtual port, network, subnet, binding; LBaaS, VPNaaS, FWaaS; L2GW, SFC, BPG-MPLS VPN.
    Kuryr (sounds like 'career'): Container network by Neutron, leverging libnetwork. Key project this year. 
    
    Rackspace releases Carina (free beta), an instant-on container native environment, getcarina.com. Now we have container based public cloud :-)
    SK Telecom is demonstrating their 5G mobile network, 100x-1000x speed up than 4G. SDN & NFV are built on Openstack. Pilot release should be available at 2018.

Manila Work Sessions

    We have attended the Manila work sessions. It is a cosy small room on the ground floor with 10 - 15 core developers participating. A long table is put in the middle of the room, members sitting around two sides. The PTL sits in the head position and operates the screen. The conversation is led by PTL. There are many topics being discussed. The meeting is quite cold actually. For each topic only a few members who are related responses. I guess that Manila core developers are divided and each of them focus on different parts. The meeting results are recorded on Google share doc. It will be published after meeting.
    
    I guess this part of summit is seldom published on Youtube. Only results are shown on Etherpads. If not attend, you lose chance to decide future Openstack.
    
    The discussion is very detailed into Manila. There are common Manila operations listed on the doc. Network sharing issues are discussed. Then access list and rules and batch update or not are discussed. Manila holds the identity of the filesystems created. Ceph has its native authentication methods such as cephx or kerberos. They have some conflicts between each other and that's what is discussed later. How guest VM should access storage network is an problem. For Ceph, the two networks mon and osd are separated. Guest may not be able to access mon to get volume information, even if it has access to osd network.
    
    About how Cinder CI is used to test vendor storages. The vendor subscribes code patch notification. Once a code patch is submitted, the vendor system pulls it down, spin up devstacks to test it out. In most cases devstack single node is used. There may be a set of devstack env for each type of stroage being tested. Devstack often provokes problems because of its high pace of development and unstability.
    
Optimizing and Extending Overlay Network for Containers

    Experiments and the results (with numbers and graphs) to show container overlay network kills performance

        Env setup
            3 nova instances connected by eth0, one of which is kube-master. There is DNS service on the private subnet. Load balancers are connected to the subnet. There is also an router interface and router connected to the subnet. The router provides floating IP. The overlay network needed for k8s is provided by Flannel. 1 kube minion on the same host with kube master, another on the different one.
        
        Single overlay kills performance
            From server to vm-flat: bw (bandwidth) to 82%, latency to 350%
            From vm-flat to vm-vlan: bw to 96%, latency to 114%
            From vm-flat to vm-overlay: bw to 26%, latency to 108%
            Change MTU from 1450 to 1000, the bw decrease to 50%.
            
        Double overlay kills twice
            Throughput drops 41%, latency increase 34%
            
        Flannel UDP and VXLAN backend
            VXLAN obtains 3-5x throughput
            
    Pluggable libnetwork drivers: Null, Host, Bridge, Overlay, Remote. The 'Remote' one uses plugin to communicate with remote provide. It can be utilized by Neutron. Kuryr is a Docker network plugin that uses Neutron. Docker network concepts are mapped to Neutron (Docker IPAM is still under work). With Kuryr we can avoid overlay on top of overlay. Neutron VLAN-Aware VMs have initial patches under review; the trunk port on VM connects multiple containers in the VM.
    
Ceph Community Talk on High-Performance Solid State Ceph

    Ceph has been greatly improved from Dumpling, both performance and maturity. Reduce avg latency and spike. 95th+ percentile starts to exceeds 20ms. Venders are contributing and optimizing Ceph for their devices.
    
    Intel involves a lot in Ceph community contribution. The first Intel Ceph Hackathon focus on performance optimization. Intel also donated 8 high performance hardware nodes. Focus areas of Intel Ceph optimization includes PMStore (persistent memory store), client-side caching enhancement, lockless C++ wrapper classes, RBD & RADOS data-path optimization, cache tiering optimization.

    Samsung contributes to Ceph. For SSD interface improvements, existing read path is synchronized in OSD layer. It is extended to support async read. For messenger performance enhancements, the new XIO Messenger is still experimental. XIO is extended to support RDMA NIC ports.
    
    Sandisk contributes to Ceph. About OSD optimizations, in the SSD context, CPU becomes bottle neck again. It needs more parallel and less CPU/OPs. There are many iterative small improvements in OSD read path. The existing write path strategy is for HDD, Sandisk modified buffering/writing strategy for SSD. Future there are RDMA intra-cluster communications, NewStore that reduces write amplification, and improved memory allocation.
    
    WAL is widely used in Ceph, but in SSD context, writing everything twice is inefficient. Essentially we write WAL + actual data because we need to relocate data. But SSD FTL actually already manages data relocating. NewStore may achieve writing data only once (except metadata).

Kubernetes Cluster on Openstack
    
    This is an introduction level talk for k8s.
    
    Why Kubernetes?
        Abstract the application with Pods.
        Ability to group Pods using labels.
        Enable accessing to Pod group using service abstraction.
        Pod management, self-healing.
    
    Details
        K8s architecture.
        K8s network model.
        Issue of docker default networking model with k8s. To solve, opt1: routing for Pod networks; opt2, use overlay network.
    
    I asked
        K8s use flannel for underlying overlay network. How can I build complex network model like Neutron (seperated networks, routers)? No much idea yet. But be ware of overlay network performance hit.
        If I use multiple redis nodes and app uses consistent hashing to access, the k8s service model breaks the paradigm. How to solve? No much idea yet. A walkaround is to get IP of each pod and access them.
    
Building Clouds for the Financial Industry: Challenges and Solutions

    ShenZhen Securities Clearing Corporation .Ltd (SSCC) is building an IaaS, PaaS, and SaaS platform for their financial customers, new datacenter at 东莞. Cloud enables the user stories. Built by Mirantis + Openstack.
    
    User stories
        User case 1: Market data cloud
        Use Case 2: Fund Cloud
        Use Case 3: Face recognition cloud
        Independent software vendors: the partner companies.
    
    Why Openstack?
        No vendor lock-in
        Customization
        Independent control
        Openstack Merits: Scalability and performance, good API interface, quick update speed
    
    Mirantis Partner
        Using KVM.
        Using Ceph as Cinder backend.
        Mirantis provided SDN solution, Juniper Contrail.
        Use Murano to deploy. Murano is the financial application catalog.
        Use Sahara for big data. Special host aggregates for Hadoop related.
        LMA - Logging, Monitoring, Alerting. Elasticsearch, InfluxDB, Grafana.
    
    Juniper Contrail as the selected SDN
        HA in control and data planes.
        Horizontally scalable L3
        Service chaining to provide secure services (vDPI, vFW)
        No hardware lock-in
        Integrated with Fuel plugin with full automation
        
    Storage design
        Ceph SAS pool: most storage needs and Nova ephemeral storage
        Ceph SSD pool: high disk IO workloads
        SAN Storage pool: mission critical workload
        
    The Openstack is already online and real customers are using it, but only business financial institutes (主要是中小的金融机构系统)。Currently the cloud is provided via SaaS to its consumers. Later when it gets more mature, larger financial institutes may join and consume it by hybrid cloud model.
    
    How does the financial cloud differs from a common cloud? High priority for security and stability. The cost is not so much concerned. Service is provided by SaaS.
    
The state of Ceph, Manila, and Containers in Openstack: by Sage Weil

    Why file? Why not block? 
        Container volume are FS.
        App uses FS first.
        Ext4 etc FS are exclusive access.
        Block volume size expands without administrator control.
    Ceph has multiple clients: Linux kernel, ceph-fuse, libcephfs.so (Samba, Ganesha, Hadoop)
    The key feature of CephFS: dynamic metadata partitioning
    CephFS road to production: "Production-ready" Ceph FS at Jewel release (Q1 2016)
    FSCK and repair: a lot of tools. Tool must be available for CephFS to go production.
    
    Manila File Storage awkwards
        Manila also manages part of connectivity problems, manage "share networks" via Neutron.
        User must attach guest to share network, user must mount the shared.
    
    Genesha + libcphefs model for CephFS via Manila.
        Expensive: Extra hop. Extra VM.
        It is not HA.
    Native Ceph Driver for Manila
        Client needs modern kernel.
        Comming soon.
    cephfs-volume-manage.py -> libcephfs.py -> libcephfs.so -> CephFS
    Security issues
        Tenants have access to storage network. CephFS has to ensure tenant isolation.
        New CephFS path-based authentication.
        Ceph's security becomes the only barrier.
    
    KVM + 9P/VirtFS + libcephfs.so model for CephFS via Manila
        Tenants remain isolated from storage layer.
        More compact
        Prototyping by Jevon Qioa, Haomai Wang, etc
    
    KVM + NFS + NFSD/GANESHA + CephFS
        Tenants remain isolated from storage layer.
        More compact
        NFS to Host: Problems with TCP/IP. Slightly awkward network setup.
        Cons on the ppt. There are Cons.    
        AF_VSOCK
            VMware vSocket. Zero configuration.
        NFS to Host: VSock (Community learned from VMware AF_SOCK?)
            NFS 4.1 only.
            Various patches are under review.
    
    KVM + NFS (VSock) + NFSD + CephFS
        We like the VSock-based model
    
    I definitely want the ppt because a lot of detailed are written on the ppt but Sage goes too fast.
    
Storage Vendors are Killing Cinder: by Rackspace

    The title is bluffing. They showed Lunr & Lunrdriver, a Rackspace homebrew LVM backend for Cinder.
    
    Core conflicts between Cinder and its vendors are
        DefCore wants uniformity
        Vendors want differentiation
        Openstack wants it all
        How to make it inter-operable?
        
    One of the audience suggests we should add a do-nothing-driver for Cinder. Because some customer just want to disable Cinder, and manage volumes from outside.

My Quick Cap

    From the half year last cycle, Neutron added IPAM (IP address management), L2GW (first seen in Kilo), SFC (service function chaining), BPG-MPLS VPN, Kuryr (solve container overlay problem via libnetwork), Service Chaining (still blueprint but implemented in distributors. same stuff with SFC?). Ceph added PMStore (persistent memory store), RDMA (remote DMA) support, XIO Messenger, many OSD RW path optimize. I would say this year is a network year for Openstack.
    
    Materials I found to understand the new sparkling words
    
        Neutron IPAM (vs Docker IPAM)
                http://specs.openstack.org/openstack/neutron-specs/specs/kilo/neutron-ipam.html
                https://wiki.openstack.org/wiki/Blueprint-ipam-extensions-for-neutron
                https://blueprints.launchpad.net/neutron/+spec/neutron-ipam

        Neutron L2GW
            L2GW: https://wiki.openstack.org/wiki/Neutron/L2-GW
            http://docs.openstack.org/developer/networking-l2gw/usage.html
            what is service plugin?
                https://wiki.openstack.org/wiki/Neutron/ServiceTypeFramework
                https://github.com/openstack/neutron/blob/master/neutron/plugins/common/constants.py
        Neutron SFC
            https://wiki.openstack.org/wiki/Neutron/ServiceInsertionAndChaining
        Neutron BPG-MPLS VPN
            https://wiki.openstack.org/wiki/Neutron/MPLSVPNaaS
            https://wiki.openstack.org/wiki/Neutron/DynamicRouting/UseCases
            https://wiki.openstack.org/wiki/Neutron/DynamicRouting/TestingDynamicRouting
            what is Quagga?
                https://en.wikipedia.org/wiki/Quagga_(software)
                http://www.slideshare.net/KeithTobin1/architecting

        Kuryr arch. how it works
            https://github.com/openstack/kuryr/blob/master/doc/source/devref/goals_and_use_cases.rst or http://docs.openstack.org/developer/kuryr/devref/goals_and_use_cases.html
            https://etherpad.openstack.org/p/magnum-kuryr
            https://github.com/openstack/kuryr/blob/master/doc/source/devref/libnetwork_remote_driver_design.rst or http://docs.openstack.org/developer/kuryr/devref/libnetwork_remote_driver_design.html#libnetwork-user-workflow-with-kuryr-as-remove-driver-host-networking
            http://superuser.openstack.org/articles/project-kuryr-brings-container-networking-to-openstack-neutron
            https://wiki.openstack.org/wiki/Meetings/Kuryr
            http://www.slideshare.net/takufukushima79/container-orchestration-integration-openstack-kuryr
            http://blog.imaginea.com/cutting-edge-openstack-adding-container-support-to-iaas/

        ceph PMStore
            http://tracker.ceph.com/projects/ceph/wiki/PMStore_-_new_OSD_backend
            https://www.youtube.com/watch?v=Oy1xonZk20U
            http://tracker.ceph.com/projects/ceph/wiki/Hadoop_over_Ceph_RGW_status_update and https://www.youtube.com/watch?v=oqO_psxwJFk
            http://tracker.ceph.com/projects/ceph/wiki/Ceph_0_day_for_performance_regression and https://www.youtube.com/watch?v=t0A8syTfaY0 and https://lwn.net/Articles/514278/


        ceph RDMA NIC ports & ceph XIO Messenger
            http://tracker.ceph.com/projects/ceph/wiki/Accelio_xio_integration_with_kernel_RBD_client_for_RDMA_support
            http://tracker.ceph.com/projects/ceph/wiki/Accelio_RDMA_Messenger
            http://www.slideshare.net/mellanox/mellanox-high-performance-networks-for-ceph
                1. Mellanox networking + accelio RDMA
            http://www.slideshare.net/somnathroy7568/ceph-on-rdma
            https://community.mellanox.com/docs/DOC-2141
            http://www.snia.org/sites/default/files/JohnKim_CephWithHighPerformanceNetworks_V2.pdf
            about accelio: http://www.accelio.org/wp-content/themes/pyramid_child/pdf/WP_Accelio_OpenSource_IO_Message_and_RPC_Acceleration_Library.pdf

        SDN service chaining
            http://packetpushers.net/service-chaining/
            http://www.sdnzone.com/topics/software-defined-network/articles/362831-service-chaining-seems-important-but-what-it-aga.htm
            http://www.tail-f.com/service-chaining-with-sdn-and-openflow-controllers/
            https://blueprints.launchpad.net/neutron/+spec/openstack-service-chain-framework
            https://review.openstack.org/#/c/93524/13/specs/juno/service-chaining.rst
            https://blueprints.launchpad.net/neutron/+spec/neutron-api-extension-for-service-chaining

        libcephfs.so & hadoop
            http://noahdesu.github.io/2015/07/12/hadoop-ceph-diving-in.html
```

### Openstack Tokyo Summit Day 3 Oct.29

```
Why Reinvent the Wheel? Using Murano, Heat, Container Clusting & Ceilometer to Provide Auto-scaling & Enforce Self-healing Best Practices in Applications: by Mirantis

    If security is more important, run container in VM. If density is more important, run container in baremetal. K8s, Mesos, Docker Swarm & Compose are supported.
    How to make container infra reliable & scalable? Deploy & Scale by: Murano & Magnum. Mointoring by Ceilometer & Zabbix
    Self-healing capabilities are provided by Murano. Application workflow are callable by API (imperative workflow language). Workflow is used for removing failed node or create new node. I was thinking application deployment should be represented as an object language, with common operation exposed.

Leveraging Kubernetes to Scale Containers on Hybrid Multi-cloud Cluster: by Mirantis

    What? Mirantis Again? 标题党? This is only early work.
    Use Murano + K8s for auto-scaling.
    Where is the hybrid multi-cloud?

NFV Orchestration - Go Beyond Virtualization

    The room is totally. Even doorway is packed with people. I never managed to get in. Highly recommend we take a look later on Youtube.
    
Decomposing Lithium's Monolith with Kubernetes and Openstack

    Lithium is the company name. Monolith is the big monolith app.
    Some app is designed to work on VM. It is very hard to bring it on container.
    Container offered simplified packaging and deployment to the cloud. Need developer-led.
    Should you split the monolith? The monolith is long running, 50 years. It is hard to split it up. For deployment docker pipeline can be used. Be incremental.
    You can't containerize everything. Not just for "stateless" web front-ends.
    Why k8s? little engineering effort, docker primitives, openstack provides the platform and fill the gap (e.g. cinder storage). Cross-platform support, AWS CloudCoreo, k8s can be deployed on AWS in the same way as local.
    Containers force you to rethink everything: logging, monitoring, secret management, config management, try not to create container anti-patterns (e.g. ssh into container; multiple process in a container)
    
    The results
        Time spent on infra vs features
        single automatable pattern including CI/CD
        Infra tools cloud follow the same pattern
        AWS even acknowledged the problem
        
        Higher code coverage
        Smaller 
        Complex deployment options have been simplified
        Canary releases and rolling-upgrades and rollbacks
    
    I asked how app can access multiple ip of redis via service model on k8s. Answer: use endpoints api (http://kubernetes.io/v1.0/docs/user-guide/services.html). In the doc, I think headless service & service discovery is also the solution (http://kubernetes.io/v1.0/docs/user-guide/services.html#headless-services).

Turn Openstack into the Global InterCloud - Now!
    
    It's a bombastic title -_-o Talk is about future. The speaker looks like a scientist from Aerospace.
    IaaS-level federation, SaaS-level federation, App-level federation. Keystone federation is here already. Federation agent is the thing that manages local user & resource info.
    Federation deploy models: Pair federations, hierarchical federations, centralized 3rd-party federation, peer-to-peer federation, ..., interclouds.
    What does federation actually require?
        User Authentication
        Federation Discovery
        Interoperability
        Membership, governance and trust
        Federated identity management
        Federated resource access
    Trust federation - a precedent: www.igtf.net. Global grid enabled by trust protocol.
    A KeyVOMS for secure service discovery.
    Keystone is very close to what's needed for general federation management.
    
Scalable and Reliable Openstack Deployments on FlexPod with Red Hat Openstack Platform: by Cisco & NetApp

    The companies names are interesting.
    FlexPox is a physical box based on Cisco UCS, Cisco Fabric interconnect and NetApp storage, Nexus 1000V, Hypervisor of KVM or Microsoft or VMware. Redhat-OSP installer with NetApp integration. Local image caching by NetApp FlexVol. Nexus 1000v is configured once VM boot up.
    CVD Design: http://bit.lv/1LFCHEz
    
Storage is not Virtualized Enough: by Huawei Zhipeng Huang
    
    Inspired by NFS, Storage Function Virtualization (SFV).
    SFV in Openstack. Several BP submitted.    
    Google group 'sfv-dev'
    Difference from Ceph (SDS): SFV tries to run Ceph inside VM, with no performance penalty. Service Chaining can also be borrowed from SDN / NFV.
    
Unraveling Docker Security: Lessons Learned from a Production Cloud: by IBM Research & IBM Cloud
    
    Threat model
        Containers attack on other containers running on the same machine. E.g. see which process are running, which files are used, which network stack, what hostname, IPC other containers are using.
        Containers attach on host machine. E.g. Misconfigured containers, malicious containers, is root inside a container also root outside (they share the same kernel)? are cpu/mem/disk limit obeyed? can a container gain privileged capabilities? are other limits obeyed (e.g. fork())? can container mount of DoS host filesystem?
        Attacks launched from public internet. E.g. Scan open ports, ...
    
    Protections
        User namespaces, cgroups, Linux capabilities, Linux security modules AppArmor/SELinux, Seccomp, Restrict Docker API, Docker and storage engine configurations (TLS, nproc/fd limits, docker security checklist, make fs readonly, files quota), Docker Registry Security (V2 API: content is addressable cryptographic hash, signing & verification, digests & manifests, safe distribution over untrust channel, naming and content are separated)
        Use trust computing and TPM for host integration verification and VT-d for better isolation
        
    Possible attacks on Containers
        Forkbomb. DoS on host. Resource exhaustion on host storage. App level vulnerabilities (e.g. weak credential, password in dockerfile). 

    I recommend we get the ppt because many security checklists are listed there.

NFV Bakeoff Panel
    
    This room is packed with people, but not doorway this time. People love NFV this summit.
    
    Challenges why NFV has not been widely deployed in production
        mission critical app?, really cut down cost?, converge with openstack platform, poc after poc after poc,
        automation & orchestration beyond just virtualization, standard & vendor interoperable, standards are not mature and issue prone,
        interoperable with existing systems, need to talk with existing technologies, in openstack there are always more than one way to do anything and you have to decide which to use (Murano? Heat?)
        same level of performance and functionality (e.g. firewalls), initial steps in orchestration,
        
    What is the missing capabilities?
        orchestration, interoperate with nova compute, make features easy to consume for operators, plug'n'play,
        more works for securities, standardize how things communicate, Heat / Murano co-works, BGP & VPN projects,
        do move into an API driven system, steady env that operators need, more work in nova and neutron (e.g. scheduler),
        need SDN for NFV to work, need neutron support,
        
    Audience: Current docker adoption and openstack and five 9?
        Openstack needs to be HA. Protect the openstack. Neutron HA. More issues should be expected. Keep the pace in Openstack and OpenNFV.
    
    Tacker Project: https://wiki.openstack.org/wiki/Tacker
    OpenNFV Project: https://www.opnfv.org/
    
Block Storage Replication with Cinder: by John Griffith & Ed Balduf, both from Solidfire

    Purpose: DR for non-cloud apps (traditional app). NEVER - 2 different vendor backends. Use cases        
        2 backends, same cloud
        2 backends, different cloud
        2 backends, one not in a cloud
        Replication one to multiple backends
        Automated -vs- Non-automated failover; Consistency group recover
        Snapshot replication -vs- continuous replication
    Volume replication is admin only, and invisible to normal user.
    
    There are a lot of difficulties how we got there. Looks like dev progress Cinder replication is kind of stuck. 
        many voices lack agree, unique characteristics that don't translate all, lack of testability, rush at the end of release cycle, patch reviewed many many times, etc. (Vendors are killing Cinder? again? -_-o). Kind of stuck. 
        V1 lessons learned (V1 semantics are no longer used): Lack of community involvement, only worked for one vendor, the only 1 person who understand it in depth is no longer available now.
        The tests and CI tests are useful but they all go on 1 node openstack, so no way to actually test the replication. So the current status of community is zero testing.
        V2 lessons learned: heavy involvement from multiple vendors, reviews reviews reviews, everything stuck on spec review, DON'T RUSH!!!, we will sell no wine before it's time. There is a lot of talk in Cinder about replication, but no implementations in Liberty (really?).
        
    Demo (no live demo because not fully implemented). PPT walkthrough. Then there is a recording of demo.
        Config file: `replication_device=xxx`
        Volume-types: replication_enabled, replication_type, replication_count
        Terms: enabled/disabled, status active,error,inactive,disabled, tasks replication enable/disable/failover, list replication targets.
    
    Drivers in work (or done): solidfire, pure storage, HP, IBM. Drivers still in progress (under review): Dell, EMC (VNX), NTAP (pool level)
        
雲泥の差 'The Separation Between Clouds and Mud' - Operating OpenStack Private Clouds: by Rackspace

    Speakers are US/Euro. Where is the Japanese?

    Approach to Product Management: the key is to operate the cloud, not just build it for customer. The "customer" is a group of operators who provide cloud service to their customer.
    
    Design Principles
        Focus on what "Day 2" looks like, or Day 20, or Day 400
        "Opinionated Deployment" - design the deployment layout for customer needs
        iterate -> learn -> iterate -> learn -> iterate
    
    The Virtuous Cycle
        Openstack grows. The growth drives business.
        Look into the community to find what new features are enabled.
        Document and training.
        Feedback from customer builds up product.
        Community + Customer + Operators + PM & Engineers feedback adds to product cycle
    
    Net Promoter Score: NPS-R, NPS-T
        a. How are we doing?
        b. Would you recommend?
        c. Rating and free text
        
    Operations - Social Contract: Engage, Lead, Operate, Communicate

    Recognize the difference between deploying and operating a cloud: love the loop, create & define team identity & culture, balance process and empowerment

Trusted and Secure Containers for Enterprise Deployment: by Intel

    Trusted VMs and Trusted Containers.
    
    To define the container security problem
        Docker's host integrity
        Docker container integrity verification
        Runtime protection of container & enhanced isolation
        Intelligence orchestration - Openstack as singular control panel.

    To solve
        Ensure container are launched on Trusted Docker Hosts:
            Boot-time integrity: Measured Launch of Boot Process and components by Intel TXT
            Docker daemon and associated components are added to TCB and Measured
            Chain of trust: H/W -> FW -> BIOS -> OS -> Docker Engine
            Remote Attestation using Attestation Authority
        Ensure docker images are not tampered prior to launch
            Measure and verify docker images, chain of trust: H/W -> FW -> BIOS -> OS -> Docker Engine -> Docker images layers
            Sign and verify images with hardware supported security: Intel TXT + TPM. Can work with Notary* - Docker Content Trust Model
            Boundary Control/Geo-Tagging for docker runtime compliance
        Leveraging trusted VMs for asserting trust of the host and the VM. Include Docker daemon as part of VMs TCB.
        Who verifies the trust? Intelligent Orchestration (Openstack, Swarm, K8s, Mesos, Fleet). For Openstack
            Nova scheduler selects TPM. Use Trust filter, ImageProperties filter, etc.
            Docker daemon to intercept container launch and request to Measured agent
            Infra change to enable Intel TXT & TPM
    
    Looking ahead: hardware-based runtime integrity
        Intel KGT
        Extend launch time integrity to runtime integrity
        VT-x, xmon, de-privileged OS, monitor/control access to critical assets (CRs, MSRs, Memory Pages, ...)
        Policy describes assets to be monitored and action to be taken
        
    H/W assisted isolaiton: Intel Clear Containers
        use VT-x instead of namespace for isolation between containers (KVM?)
        Provides an extra, rooted-in-hardware security layer for containers
        Still support the advantages of container model
    
    So I think from the last time Intel released Clear Container, now it becomes a complete hardware-assisted container & integrity solution. Intel has done lots of work in hardware-assisted integrity.

```

### Openstack Tokyo Summit Day 4 Oct.30 (Design Summit Only)

```
Cinder Contributor Meetup (Morning)

    Mitaka Design Summit Etherpads: https://wiki.openstack.org/wiki/Design_Summit/Mitaka/Etherpads. Today's Cinder Etherpad: https://etherpad.openstack.org/p/mitaka-cinder-contributor-meetup. There is recording for this meeting, need to know where it is going to be published. Besides Cinder devs, many vendor representatives are also included in the meeting to be heard from. They also bring their customer use cases. There are also distributor guys here. The meeting is a bit exhausting and I know why everybody carries water now -_-o There are breaking times. People form in groups and discuss various topics. I guess that's another important time where people shape opinions and agreements, to decide the next step Cinder.
    
    Joash from keystone discuss how cinder should work with keystone federation. The volume is attached/detached from another site. VMs can be in this or another site. Keystone federation is working on networking. We want it to work for Nova and Cinder side. Two backends of CG (consistency group) should be the same. CG volumes may have interfere with federation. The datacenters need to be on a shared network for the storage, or at least IP routeable. As the distance increases, latency increases, there can be new race conditions need to tackle with.
    
    The next topic is CG interaction with volume replication. Currently the user can replicate one volume in a CG individually, which he should not be able to do. CG operation process and API should support replication. What's more is that replication is still not fully finished now. We need to inform driver vendors to take CG into consideration when they implement replication. We need to think ahead in case someone is implementing it but we found there is fundamental problem in replication design. Looks like replication is a headache for everyone. Replication can be used for volume, pool, CG, logical pool; that adds complexity. We've been working on Replication V1 (discarded), Replication V2. Now it's Replication V2.1. People keep arguing and just won't reach an agreement. Xing is very active and leading expert for CG & replication to push the progress (but shouldn't there be more persons to help?). Current Cinder implementation allows CG to span across pool, but some vendor may not agree; however replication should be able to span across pool. I found the Keystone guy of the last topic has already disappeared. The vendor can report its capabilities. People are finding ways to to avoid duplicity of CG x Replication x VG x ... Vendors CIs are also going to grow bigger and bigger because these combination scenarios. 
    
    To backup snapshot, currently we can backup volume but not snapshot. We can create an silent volume from the snapshot and reuse volume backup. That's a pattern we should follow.
    
    To improve config file organization, we need to clearly separate per-backend vs per-host vs default section. The default section cascades to driver sections. Maybe we can add warning for misconfigures. Maybe add a 'global' section. Upgrade should be taken into consideration. Which conf option the driver can override from the default section, e.g. oversubscription ratio?
    
    Next we discuss about minimum functions that a driver should support. manage/unmanage is under question because few people really use that. Retype is under questioned because not all vendor supports it and it is not supported in the same way.

    Then, how could Ironic attach a volume without Nova. We now have two source of truth for volume attachment, Nova and Ironic. That's a concern. Deleting a volume from a running instance is dangerous, just like press the power button. Ironic needs an API call that attaches/detaches a volume like Nova. Force-detach may have problems in this context.
    
    The default oversubscription value is 20%. We discuss whether we should change the default value. If changed, we should communicate to driver developers so they can make changes accordingly. Driver conf should be able to override the global oversubscription. Another problem is that if you want to change oversubscription rate, the only option is to change .conf file. You cannot change it on the fly. It is too risky to change the default. Look for <driver>_max_oversubscription_ratio generic option.
    
    Cinder functional tests for python-cinderclient. Reason http://lists.openstack.org/pipermail/openstack-dev/2015-July/068716.html. Neutron has a lot of functional tests implemented and can be used as a good reference. Example https://github.com/openstack/python-cinderclient/tree/master/cinderclient/tests/functional, https://github.com/openstack/neutron/tree/master/neutron/tests/functional.
    
Cinder Contributor Meetup (Afternoon)
    
    The `cinder create 1` the 'Gb' vs 'Gib'? You can change client but don't change underlying api because that will affect everyone. https://en.wikipedia.org/wiki/Gibibyte
    
    Cinder rpc and objects are versioned. An api can switch between new or old versions, so that rolling upgrade can be carried out per component. API needs to be backward compatible. We discuss the possible work items and the versioned api/objects workflow. This is key to enable rolling upgrade and we should make it ready at Mitaka release. Database compaction (compact the db migrations?) also need to be done. Need dedicated core dev to help review these patches because they get merged too slow.
    
    Volume migration improvement. A migration takes long time, we need to report the progress. We also need to be able to abort migration. The work is mostly done, patches are pending review. We are discussing the possible concerns related to them. E.g. to kill it or to wait until it finishes. If we use block copy `dd` with 32MB chunk size, we have abort points each chunk.
    
    RemoteFS driver refactoring. RemoteFS's hypervisor needs different volume/snapshot format, but nova first-class provides qcow2. Nova-assisted snapshots (when volume is in attached state) currently qcow2 only. It is hard to add support for a new volume type. Spec at https://review.openstack.org/#/c/237094/1/specs/mitaka/remotefs-volume-format-handlers.rst. It is proposed to add volume format base class and volume snapshot format base class and add volume format/snapshot handlers for each type. The other cores seem not very accepted with that. The work remains in question/re-work.
    
    LVM driver, the reference impl, needs love too but it is rarely cared; everyone doing presentation says don't use that. Is LVM still proper as the reference impl? How about Ceph? But ceph uses its own protocol rbd, rather than iscsi. DRBD status and how to support all the features. LVM thin provision should be enabled (rather than thick on default). We can prototypely implement CG in LVM driver for testing purpose. 
    
    Make rally job voting for new patch test? This adds performance verification for Cinder. The concern is John discussed with Rally team and they said Rally is not stable enough. The performance results are not stable enough. We don't want to add another block against patches being merged. http://logs.openstack.org/05/238505/1/check/gate-rally-dsvm-cinder/1c9ae79/. Another concern is that too few people in the community may be aware or interested in the rally part.
    
    Third party CI. We need to revise the status. Which works, which not, and how we want it to grow. Very need to improve devstack and tempest outputs to make finding bug easier. CI Watch http://ci-watch.tintri.com/project?project=cinder. You can find which test is totally useless here because it never succeeds.
    
    Priorities: H/A, rolling upgrade, microversions before M1
    
Other Thinkings

    I found there are too few in Openstack community who are fully aware of container technologies, even if we have Magnum for long time. That's too few people compared with such a disruptive technology.
    
    Both Murano and Magnum provides k8s, but the community looks diverged on them. Mirantis presentations provide both Murano and Magnum but doesn't mention the divergence or integration. "For those who don’t want to use Murano, the OpenStack Magnum project ..." in Mirantis article (https://www.mirantis.com/blog/yes-containers-need-openstack/) seems to have presumed the divergence. The Magnum presentations never mentioned Murano in my impression. So I guess those two are really diverged, but not publicly aware yet. Thanks for my colleague to think of this.
```

