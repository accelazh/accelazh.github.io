---
layout: post
title: "Paper Reading Notes for Datacenter Networking"
tagline : "Paper Reading Notes for Datacenter Networking"
description: "Paper Reading Notes for Datacenter Networking"
category: "storage"
tags: [storage, paper, networking]
---
{% include JB/setup %}

Networking is another pillar for distributed storage systems.

```
1. Congestion Control for Large-Scale RDMA Deployments    [2015, 452 refs]
   https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p523.pdf
    1. The recognized datacenter networking technology for RDMA RoCEv2, following up from the recognized DCTCP 
    2. highlights
        1. problems of prior arts
            1. Priority-based Flow Control (PFC) does not distinguish between flows. 
            2. DCTCP and iWarp include a slow start phase
            3. Head-of-line blocking problems, PAUSE unfair, parking-lot problem
        2. DCQCN solution
            1. based on QCN
            2. flow-level congestion control defined by src/dest MAC address and a flow id field
            3. CP Algorithm (switch side, congestion point) - same with DCTCP
               RP Algorithm (sender side, reaction point) - FastRecovery, HyperIncrease, AddictiveIncrease
               NP Algorithm (receiver side , notification point) - NIC generates at most one CNP every N us
        3. Buffer settings
            1. PFC is not triggered too early, and PFC not triggered too late to cause packet loss due to buffer overflow
    n. related materials
        1. DCQCN+QCN+DCTCP
           https://blog.csdn.net/hithj_cainiao/article/details/117292144
        2. DCQCN：Congestion Control for Large-Scale RDMA Deployments
           https://www.jianshu.com/p/44dd54142f46

2. Clos topology for data center networks (Part 1).
   https://www.youtube.com/watch?v=XrnATy3AvpA
   https://www.youtube.com/watch?v=7-qYILgg5js
    1. CLOS - LEAF to SPINE are full connection
              ECMP - Equal cost multi-path
    2. Low cost
        1. cheap fix form-factor boxes
           inexpensive offering
           expand by simply adding boxes and links
        2. So, CLOS is in compare to the old single cross bar solution
           CLOS is horizontal scalable with inexpensive devices 
    n. related materials
        1. What is Clos Architecture or Clos Network?
           https://ipwithease.com/clos-architecture/
        2. Clos Networks: What's Old Is New Again
           https://www.networkworld.com/article/2226122/clos-networks-what-s-old-is-new-again.html
            1. "In this Clos topology, every lower-tier switch is connected to each of the top-tier switches in a full-mesh topology"
            2. "The advantage of the Clos network is you can use a set of identical and inexpensive devices to create the tree and gain high performance and resilience that would otherwise cost must more to construct."
            3. "To prevent any one uplink path from being chosen, the path is randomly chosen so that the traffic load is evenly distributed between the top-tier switches. If one of the top tier switches were to fail, it only slightly degrades performance through the data center."
        3. Introduction to Clos Networks
           https://web.stanford.edu/class/ee384y/Handouts/clos_networks.pdf
            1. "The advantage of such network is that connection between a large number of input and output ports can be made by using only small-sized switches"
        4. What is a Clos network?
           https://www.quora.com/What-is-a-Clos-network
            1. "The key advantage of Clos networks is that the number of cross points required (which compose each crossbar switch) can be far fewer than would be the case if the entire switching system were implemented with one large crossbar switch."
            2. MLAG - "Multi-Chassis Link Aggregation Group (MLAG or MCLAG) is still available on the server side. Servers can be connected to two different leaf or TOR switches in order to have redundancy and load balancing capability."
        5. Demystifying DataCenter CLOS networks
           https://www.youtube.com/watch?v=GVT3KeAa9xw&t=1847s

3. Google Datacenter Network Design, How Google Datacenters scale 100s thousands of Servers!
   https://www.youtube.com/watch?v=kythGOICErQ&t=1244s
    1. Customer requests and responses need little bandwidth. DB queries and responses are larege. So, intra-datacenter network needs large bandwidth, but external internet bandwidth doesn't need that much
    2. Google starts with CLOS network, and later are all CLOS network, including Jupiter.
    3. Later the network architecture went to Flattened Butterfly. It uses Infinband + RDMA, and TCP RPCs on massive Ethernet. Never used RDMA on Ethernet.

4. Jupiter Evolving: Transforming Google's Datacenter Network via Optical Circuit (TS 1, SIGCOMM'22)
   https://www.youtube.com/watch?v=Hfl-i56hZUg
    1. very good. many revolutionary network architecture redesign.
       30% reduction in network CapEx and 40% in power consumption. 10x faster fabric-wide topology reconfiguration with OCS. 10% improvement in flow completion time (FC) and 30% in throughput
       direct-connect jupiter architecture, serving production for more than 5 years
    2. highlights
        1. OCS - Optical Circuit Switches - as the interconnection layer for Jupiter
            1. data rate agnostic, no need to upgrade when the rest of network transit from 40GB to 60GB etc
            2. no more Clos. removed spine layer. to direct connect jupiter architecture
                1. heterogeneous network bandwidth, because old and newly added hardware. old spine becomes performance bottleneck
                    1. the data link between 200G aggregation block immediately get to 200GB (though OCS, which is data rate agnostic), without needing spine layer to be upgraded
                2. spines are expensive, composes 40% of fabric cost and power consumption
                3. Clos is great when traffic pattern is unknown, 
                   but Jupiter block-level traffic is predictable (gravity model), traffic between A-B is ~ to A * B
                4. power efficiency doesn't decrease with hardware generation evolve now, so architectural/structural cost reduction becomes more important for COGS saving
        2. Use SDN to adapt topology and routing to traffic variation
            1. traffic engineering: dynamically adapting routing to traffic
                1. split traffic among multiple shortest and non-shortest paths while observing link capacity, realtime communication patterns
                   the traffic topology change reaction control loop operates at seconds to minutes
                2. variable hedging as a configurable strategy
                    1. reduce spikes due to prediction overfit
            2. Topology engineering adapts to slow-moving changes
                1. traffic-aware topology change for managing heterogeneous speed
                   operates on days and doesn't respond to short-lived conditions like failures and drains
                2. hitless topology reconfiguration - no application impact
                    1. Minimal Rewiring [NSDI'19]
                    2. incremental reconfiguration to minimize unavailable capacity and limit blast radius

    3. The article: Jupiter evolving: Reflecting on Google’s data center network transformation
       https://cloud.google.com/blog/topics/systems/the-evolution-of-googles-jupiter-data-center-network
        1. spent last 8 years to integrate optical circuit switching (OCS) and wave division multiplexing (WDM) into Jupiter, and combine OCS with SDN.
           key advantages: incremental network with heterogeneous speed switches, lower latency (10%) and higher throughput (30%), lower cost (30%) and power saving (40%), 50x less downtime and zero-downtime upgrade
        2. highlights
            1. review the last Jupiter paper at 2015. Key features are 1) SDN 2) Clos networking 3) commodity hardware
            2. About Optical Circuit Switch (OCS)
                1. On an OCS die, it's packaged with arrays of micro mirrors. these micro mirrors can be reprogrammed to map an input port X to different output ports
                   this creates a virtual circuit. they are just lights, and transit in light speed. different circuits are by different color of lights
                2. Google datacenter networking is probably already using optical fibers. By replacing electronic switches to OCS, it avoids transiting electric<=>light, which needed power hungry transceivers
                    1. My question: is optical fiber really used in links? the paper also says WDM transceiver is used for electro-optical conversion
                        1. See paper "Mission Apollo" Figure 12. WDM and Circulator are combined into one device, and put to the uplink of Aggregator Block electrical switch. after the conversion, the link is optical fiber to input directly to OCS. Circulator is used to combine one uplink + one downlink into one bi-directional link
                3. OCS simply reflects lights from input port to output port, no header parsing are involved. this is another reason that OCS is fast, and data rate agnostic.
                4. OCS needs frequent reprogramming, this is right where SDN (Google Orion) takes part in.
                5. Google's OCS paper: Apollo OCS: https://arxiv.org/abs/2208.10041
            3. dynamic pathing
                1. real-time web request serving and batching jobs need different bandwidth and latency. need to allocate bandwidth and pathing with App aware
                2. if 10% network capacity needs to be taken down during upgrade, the 10% traffic needs to be distributed, not evenly but according to App needs 

    4. The paper: Jupiter Evolving: Transforming Google's Datacenter Network via Optical Circuit Switches and Software-Defined Networking    [2022, 9 refs, SIGCOMM, Google]
       https://research.google/pubs/pub51587/
        1. most points already captured in previous bullets
        2. highlights
            1. multi-path traffic routing is by WCMP algorithm. The traffic matrix is refreshed every 30s.
               The optimization is formulated to minimize MLU (max link utilization).
               prediction can be bad when 1) high variation 2) churns shorter than 30s. To avoid overfitting, variable hedging is used.
                1. see more in Appendix "B VARIABLE HEDGING FORMULATION"

    5. The older 2015 version: Jupiter Rising: A Decade of Clos Topologies and Centralized Control in Google’s Datacenter Network    [2015, 793 refs, SIGCOMM, Google]
       Paper: https://storage.googleapis.com/pub-tools-public-publication-data/pdf/43837.pdf
       Brief version: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/7a2ef8424cdc3be32a4cb96bf3e3483eaf0b8949.pdf
        1. Key features are 1) SDN 2) Clos networking 3) commodity hardware
        2. highlights
            1. First, multi-stage Clos topologies built from commodity switch silicon can support cost-effective deployment of buildingscale networks.
                1. why introducing "Edge Aggregation Block"?
                    1. aggregation block was introduced in the first version, Firehose 1.0 with 1Gbps networking. See figure 3, AB separates interconnection into domains, so that cross AB it doesn't need the very many links. it makes scaleout easier. it's the domain unit that is being managed by Orion. it's also probably the unit of new hardware purchase and deployment
            2. Second, much of the general, but complex, decentralized network routing and management protocols supporting arbitrary deployment scenarios were overkill for single-operator, pre-planned datacenter networks. We built a centralized control mechanism based on a global configuration pushed to all datacenter switches.
            3. Third, modular hardware design coupled with simple, robust software allowed our design to also support inter-cluster and wide-area networks
                1. instead of traditional decentralized routing protocols such as OSPF/IS-IS/BGP, Our approach was A centralized solution where a route controller collected dynamic link state information and redistributed this link state to all switches over a reliable out-of-band Control Plane Network (CPN)
                    1. this is interesting. this is the prototype of Orion that, instead of running OSPF by routers, a central mind (SDN controller) periodically collect info and decide best routing (WCMP) and pushdown the layout to end switches/routers via reliable out-of-band networking CPN.
                        1. "Our design informed the control architecture for both Jupiter datacenter networks and Google’s B4 WAN,17 both of which are based on OpenFlow18 and custom SDN control stacks"
                        2. "a centralized Firepath master, which redistributes global link state to all switches. Switches locally calculate forwarding tables based on this current view of network topology"
                    2. it exploits the fact that datacenter networking topology is largely static. it doesn't need protocols like OSPF to periodically re-layout. SDN controller does have functions to handle temporary/permanent link/switch down. 
                1. What's the advantage of commodity hardware switches?
                    1. the paper didn't mention much about the reasoning. 
                       "Rather than use commercial switches targeting small-volume, large feature sets, and high reliability, we targeted general-purpose merchant switch silicon, commodity priced, off the shelf, switching components"
                       "To keep pace with server bandwidth demands which scale with cores per server and Moore’s Law, we emphasized bandwidth density and frequent refresh cycles. Regularly upgrading network fabrics with the latest generation of commodity switch silicon allows us to deliver exponential growth in bandwidth capacity in a cost-effective manner."
            4. Google networking evolution history
                1. Firehose 1.0, Firehose 1.1
                2. Watchtower and Saturn: Global deployment
                3. Jupiter: A 40G datacenter-scale fabric
            5. EXTERNAL CONNECTIVITY
                1. WCC: Decommissioning legacy routers
                    1. We chose to build separate aggregation blocks for external connectivity, physically and topologically identical to those used for ToR connectivity. However, we reallocated the ports normally employed for ToR connectivity to connect to external fabrics
                2. Freedome, the third step in the evolution of our network fabrics, involved replacing vendor-based inter cluster switching
                    1. See Figure 10. CBR to speak BGP at both inter cluster and intra campus layers. CBR => FDB => DFD => CFD => WAN
                       CBR: Cluster Border Routers
                       FDB: Freedome Block. 2-stage fabric: FER => FBR
                        FER: Freedome Edge Router
                        FBR: Freedome Border Router
                       DFD: Datacenter Freedome
                       CFD: Campus Freedome
            6. Others
                1. we set out to make switches essentially look like regular machines to the rest of fleet. Examples include large scale monitoring, image management and installation, and syslog collection and alerting
                2.  We found several factors contributed to congestion: 
                        i) inherent burstiness of flows led to inadmissible traffic in short time intervals typically seen as incast [8] or outcast [21]; 
                        ii) our commodity switches possessed limited buffering, which was sub optimal for our server TCP stack; 
                        iii) certain parts of the network were intentionally kept oversubscribed to save cost, e.g., the uplinks of a ToR; and 
                        iv) imperfect flow hashing especially during failures and in presence of variation in flow volume
                    We used several techniques to alleviate the congestion in our fabrics
                        First, we configured our switch hardware schedulers to drop packets based on QoS. Thus, on congestion we would discard lower priority traffic. 
                        Second, we tuned the hosts to bound their TCP congestion window for intra-cluster traffic to not overrun the small buffers in our switch chips. 
                        Third, for our early fabrics, we employed link-level pause at ToRs to keep servers from over-running oversubscribed uplinks. 
                        Fourth, we enabled Explicit Congestion Notification (ECN) on our switches and optimized the host stack response to ECN signals [3]. 
                        Fifth, we monitored application bandwidth requirements in the face of oversubscription ratios and could provision bandwidth by deploying Pluto ToRs with four or eight uplinks as required. 
                        Similarly, we could repopulate links to the spine if the depop mode of a fabric was causing congestion. 
                        Sixth, the merchant silicon had shared memory buffers used by all ports, and we tuned the buffer sharing scheme on these chips so as to dynamically allocate a disproportionate fraction of total chip buffer space to absorb temporary traffic bursts.
                        Finally, we carefully configured switch hashing functionality to support good ECMP load balancing across multiple fabric paths.

        n. related materials
            1. Understanding BGP - Border Gateway Protocol
                1. BGP Overview
                   https://www.youtube.com/watch?v=_Z29ZzKeZHc
                    1. AntonymousSystem (Local ISP, local company network) exposes routers at the border (edge routers).
                       Edge routers have policies what to advertise to peers and what advertisements to accept.
                       routing table inside an AS is small, but it can be large on edge routers which tracks ASes in the world
                    2. BGP selects best path across ASes. hops of ASes, AS policies, SLAs, business considerations, charging fees, etc. are taken into consideration
                2. What is BGP? | BGP routing explained
                   https://www.cloudflare.com/learning/security/glossary/what-is-bgp/
                    1. Each AS wishing to exchange routing information must have a registered autonomous system number (ASN)
                    2. BGP hijacking: An incorrect local config can propagate world-wide via BGP peering, it can block all access
            2. BGP vs OSPF
                1. EGP / IGP :: Distance Vector / Link State :: Dynamic Routing Protocols :: OSPF EIGRP BGP RIP IS-IS
                   https://www.youtube.com/watch?v=KjNYEzEBRD8
                    1. IGP protocols: RIP, EIGRP, OSPF, IS-IS. IGP is tuned for speed & responsiveness, it's pretty chatty
                        1. Distance Vector: RIP, EIGRP. Knowledge of only the next hop, less RAM/CPU, slower convergence
                        2. Link State: OSPF, IS-IS. More CPU/RAM spent to track knowledge of entire Topology, faster convergence
                    2. EGP protocols: BGP. EGP is tuned for stability, limit update frequency, harden security / reject malicious route advertisements. BGP also offer more control on inbound/outbound path selection

    n. related materials
        1. Ultrafast optical circuit switching for data centers using integrated soliton microcombs    [2021, 21 refs, microsoft]
           https://www.youtube.com/watch?v=UDCdDHJcaAU
           https://arxiv.org/pdf/2010.10984.pdf
            1. optical fiber connection + optical switch (inter virtual circuits) is much faster than optical fiber + electrical switch.
               besides, it's more power saving because no transceivers needed
               in comparing with Google Jupiter's MEMS-based OCS Palomar. Slow switching time (ms level) is MEMS-based OCS is a general problem, but this paper proposes sub-ns level fast switching
            2. highlights
                1. sub-nano second transmit, ~500ps
                2. existing arts: optical fiber => electric switch, the electric<=>optical transceivers are very power hungry.
                3. connections between servers is established by different color of lights. different lights can be overlapping, establishing virtual circuit
                4. in comparing with Google Jupiter's MEMS-based OCS Palomar. Slow switching time (ms level) is MEMS-based OCS is a general problem, but this paper proposes sub-ns level fast switching 
                    1. "MEMS-based OCS architectures suffer from slow switching time (∼ ms)"
                    2. Our proposal: uses photonic chip-based soliton microcombs as a multiwavelength source
                       We use a Si3N4 based soliton microcomb as a multiwavelength source to show ultrafast (< 550 ps) optical wavelength switching

        2. Orion: Google's Software-Defined Networking Control Plane    [2021, 33 refs, NSDI, Google]
           https://www.usenix.org/conference/nsdi21/presentation/ferguson 
            1. An evolution from OpenFlow. Supports Google Jupiter (datacenter networking) and B4 (WAN networking). 
            2. highlights
                1. control plane is decentralized micro-services, each application in a separated process
                    1. data plane is based on OpenFlow agent (OFA), Orion calls OpenFlow Front End (OFE) to control OFAs
                2. NIB centralized configuration database, KV based, with performance, scalability, reliability goals
                    1. central tables to organize states consumed by end SDN programs. similar with ONOS, Open-Daylight, Hyperflow
                    2. NIB also includes the publish-subscribe messaging. it implements a single arrow of time to propagating intents, it tracks the global event trace for troubleshooting
                    3. Orion app updating config uses 2PC protocol. config is first staged in shadow NIB tables
                3. Intent-based network management and control
                    1. I.e. to define the goal state to eventually move into, instead of action based e.g. input switch commands (thinking of puppet)
                       intent is propagated through the hierarchical networking architecture
                4. reliability related
                    1. alignment of SDN domain vs physical failure domain. i.e. a SDN controller failure shouldn't impact more than one physical domain (blast radius)
                        1. In Jupiter, we use a hierarchy of partitioned Orion domains; in B4, a flat partitioning of Orion domains communicating with non-Orion global services
                    2. handle optimistically when SDN controller is temporarily unreachable, which can be frequent - 'Failure Static'
                        1. controller aggregates health states from switches. if a failure is decided to be permanent, traffic can be re-programmed to route around the failed switches
                           but capacity degradation threshold is also taken into consideration. it shouldn't reroute more switches if traffic volume cannot be satisfied
                    3. dedicated CPN - control/management plane network. it's separated from the data plane network, so that SDN controller can configure data plane without worrying about CPN is broken and commands cannot be received
                        1.  a hybrid design where only the Top-of-Rack (ToR) switches were controlled in-band (i.e. no dedicated CPN)
                5. Routing engine (RE)
                    1. "It models a configured collection of switches within an Orion domain as an abstract routing node called a supernode [13] or middleblock [28]"
                       This should be the "aggregation block" mentioned in Jupiter Paper
                    2. RE .. computes SPF (Shortest Path First) for each prefix
                       "RE performs load balancing within a domain by spreading traffic across multiple viable paths, and through non-shortest-path forwarding, as requested by client apps"
                        1. The second line should be mentioned in Jupiter Paper as split path while observing heterogeneous link capacity
                            1. per implementation, Jupiter/Orion employs "WCMP-based (Weighted Cost Multi-Pathing) routing"
                        2. re-programming the routing is done by passing route config to OpenFlow agent
                            1. My questions: this paper didn't mention whether the agent is Open vSwitch / OVS
                               but it probably won't need OVS, because the being programmed agents are physical devices. OVS is used for VM layer, which is mentioned in paper Andromeda
                        3. note, in default CLOS networking, rather than using SPF, a lower level switch randomly split traffic to all paths
                    3. loss-free sequencing from the currently programmed pathing solution to a new pathing solution. In a legacy network, the eventually consistent nature of updates from distributed routing protocols (e.g. BGP) can result in transient loops and blackholes in the data plane
                        1. this should be mentioned in Jupiter Paper as the "traffic-aware topology change"
                6. Capability Readiness - Protocol. With this protocol, applications have a uniform way of specifying which data they require to resume operation, and which data they provide for other applications
                    1. Capability-based coordination keeps the Orion apps from becoming "coupled", in which a specific implementation of one app relies on implementation details or deployment configuration of another app (which is a Bad thing)
                7. About Jupiter
                    1. Jupiter network architecture ("Jupiter Rising" rather than "Jupiter Evolving" paper)
                        "a Clos-network topology: (i) aggregation blocks [28] connected to a set of hosts, (ii) FBRs (Fabric Border Routers, also called Cluster Border Routers in [28]) connected to the WAN/Campus network, and (iii) spine blocks that interconnect aggregation blocks and FBRs"
                    2. map physical Orion domains to the Jupiter building blocks - e.g. the "aggregation block", "FBR supernode"
                    3. Onix is Google's first generation SDN, built with (first generation of) Jupiter, and B4
                8. about B4
                    1. Orion solved B4’s availability and scale problems via a distributed architecture in which B4’s control logic is decoupled into micro-services with separate processes

            n. related materials
                1. OpenvSwitch and OpenFlow: What Are They, What’s Their Relationship?
                   https://medium.com/@fiberoptics/openvswitch-and-openflow-what-are-they-whats-their-relationship-d0ccd39b9a5c
                    1. "OpenvSwitch and OpenFlow are both used for SDN application. OpenFlow is one of the first SDN standards. OpenvSwitch is an OpenStack SDN component. As to their relationship, OpenvSwitch is one of the most popular implementations of OpenFlow. Apart from OpenFlow, OpenvSwitch also supports other switch management protocols such as OVSDB (Open vSwitch Database Management Protocol)"
                    2. ONF - Open Networking Foundation
                       https://opennetworking.org/
                       "The Open Networking Foundation (ONF) is a non-profit operator-led consortium.[1] It uses an open source business model aimed at promoting networking through software-defined networking (SDN) and standardizing the OpenFlow protocol and related technologies"
                       https://en.wikipedia.org/wiki/Open_Networking_Foundation
                    3. "OpenDaylight (ODL) is an open source project within the Linux Foundation. As an SDN controller, it provisions the network policies as specified and sends that information to the HYpervisor. It allows the users to programmably manage OpenFlow capable Gigabit Ethernet switches"
                       OpenStack vs OpenDaylight vs OpenFlow vs OpenvSwitch: What’re Their Relations?
                       https://www.fiber-optic-transceiver-module.com/openstack-vs-opendaylight-vs-openflow-vs-openvswitch-whatre-their-relations.html

        3. A look inside Google’s Data Center Networks
           https://cloud.google.com/blog/products/gcp/a-look-inside-googles-data-center-networks
            1. GCP’s SDN network virtualization stack, Andromeda
               Enter the Andromeda zone: Google Cloud Platform's latest networking stack
               https://cloud.google.com/blog/products/gcp/enter-andromeda-zone-google-cloud-platforms-latest-networking-stack
                1. See Google's Networking Infrastructure publication site: https://research.google/teams/network-systems/
                    1. Orion: Google’s Software-Defined Networking Control Plane
                    2. Andromeda: Performance, Isolation, and Velocity at Scale in Cloud Network Virtualization    [2018, 131 refs, NSDI, Google]
                       https://www.usenix.org/conference/nsdi18/presentation/dalton
                        1. VM Controller -> OpenFlow Front End (inspired by Onix)
                           Flow programming on a large scale for virtual machines
                        2. data plane is using Open vSwitch / OVS.
                        3. Hoverboards
                            1. Hoverboards are dedicated machines to route packets from VMx to VMz
                               but if a persistent flow is detected, the flow can be offloaded from Hoverboard. then VMx's host directly sends to VMz, which is done by inserting a new flow entry in control table.
                            2. today, more than 99.5% traffic is offloaded
                        4. Andromeda Fast Path - OS bypassing, busy polling, dedicated for high performance flows with priority
                            1. Co-processors per Guest VM for CPU intensive packets
                            2. Flow table cache
                            3. DPDK faster than TCP Busy Poll faster than Normal TCP
                            4. Andromeda 2.0+ use a single core per host for the dataplane Fast Path
                        5. Dataplane Hitless Upgrade
                            1. Old Dataplane state is transferred to New Dataplane at background. Old dataplane kees serving
                               Next, old dataplane stops serving, any delta/updates transferred to new dataplane
                               state transfer done, median blackout is 270ms, new dataplane takes over serving
                        6. My questions
                            1. How is FPGA employed compared to Microsoft Catapult
                                1. instead of FPGA, Andromeda is using co-processor / coprocessor, kernel bypassing, and flow offloading
            
            2. How Google Invented An Amazing Datacenter Network Only They Could Create    [2015]
               http://highscalability.com/blog/2015/8/10/how-google-invented-an-amazing-datacenter-network-only-they.html
                1. the article is quite comprehensive but too old - year 2015
            
            3. Google Cloud Networking overview    [2021]
               https://cloud.google.com/blog/topics/developers-practitioners/google-cloud-networking-overview
                1. "At the time of this writing, Google has more than 27 regions and more than 82 zones across 200+ countries. This includes 146 network edge locations and CDN to deliver the content. This is the same network that also powers Google Search, Maps, Gmail, and YouTube."
                2. a nice chart, an overview, and a production list of GCS networking

        4. Helios: A Hybrid Electrical/Optical Switch Architecture for Modular Data Centers    [2010, 1242 refs]
           https://cseweb.ucsd.edu/~vahdat/papers/helios-sigcomm10.pdf
            1. mentioned in Jupiter Evolving article as "While academic research investigated the benefits of optical switches, conventional wisdom suggested that OCS technology was not commercially viable"
               mentioned in Jupiter Evolving paper as "Helios [11] takes a similar approach to the OCS layer presented in this paper by leveraging hybrid electrical/optical switches for a dynamic topology, but lacks fine-grained, demand-based traffic engineering"
            2. useful paper to understand what is MEMS-based Optical Circuit Switching.
            3. highlights
                1. MEMS-based Optical Circuit Switches, which is used in Jupiter Evolving
                2. Hybrid approach. A few spine switch is replaced from electrical switch to OCS switch. TOR installs Transceiver. Two optical uplinks are merged into one via Mux. 
                3. OCS: A single optical port can carry many multiples of 10 Gb/s assuming that all traffic is traveling to the same destination.
                        The key limitation is switching time, which can take as long as tens of milliseconds
                        optical circuit needs periodical dynamic reconfiguration
                4. Key problem to solve: Oversubscription is always needed, we cannot provision network bandwidth for worst case.
                                         However, temporary burst needs to be handled. OCS comes in as a pool of available bandwidth to be dynamically allocated
                5. what is MEMS-based Optical Circuit Switching (MEMS - Micro-ElectroMechanical Systems)
                    1. The OCS is a Layer 0 switch — it operates directly on light beams without decoding any packets. 
                       An OCS uses an N×N crossbar of mirrors to direct a beam of light from any input port to any output port. 
                       The mirrors themselves are attached to tiny motors, each of which is approximately 1 mm2 [16]. 
                       An embedded control processor positions the mirrors to implement a particular connection matrix and accepts remote commands to reconfigure the mirrors into a new connection matrix.

        5. Mission Apollo: Landing Optical Circuit Switching at Datacenter Scale    [2022, 1 refs, Google]
           https://arxiv.org/abs/2208.10041
            1. mentioned in Jupiter Evolving article as "we designed and built Apollo OCS that now forms the basis for the vast majority of our data center networks"
            2. World's first large scale deployment of OCS for datacenter networking.
               Google internally developed OCS (Palomar), co-designed circulators, WDM (wavelength-division-multiplexed).
               the use of camera image processing for mirror controls
               Very useful paper to understand how OCS works and Google's Palomar OCS implementation
            3. highlights
                1. To enable the Apollo optical switching layer, we employ circulators to realize bidirectional links through the OCS, effectively doubling the OCS radix
                    1. we have created a highly reliable and manufacturable 136x136 OCS, with millisecond-scale switching time and worst-case insertion loss of 2dB and return loss of -38dB.
                    2. Palomar is lower in per port cost than equivalent throughput EPSes (electrical packet switch). Circulators further enhance this cost advantage by doubling the OCS effective port count.
                2. the critical co-design of WDM transceiver technology for these OCS plus circulator-based bidirectional links and their corresponding physical impairments
                    1. "This eventually led to after-the-fact creation of the CWDM4 MSA [35]." Figure 11 (c) "bidi CWDM4 optical transceiver with integrated circulator"
                    2. Figure 11: a) The optical circulator is a three-port non-reciprocal device that has a cyclic connectivity. Input into port 1 is directed to port 2, input into port 2 is directed to port 3. The circulator thus converts a traditional duplex optical transceiver into a bi-directional one.
                        1. it reduces both the number of OCS ports and fiber cables required by half
                    3. the Circulator is integrated into WDM. See Figure 11 (c) which shows the circulator transceiver integration
                3. very useful. Table 1: Cost, scale, performance, and reliability/availability comparison of various OCS technologies.
                    1. MEMS [25, 26], Robotic [27], Piezo [28], Guided Wave [29], Wavelength Switching [30]
                    2. MEMS-based OCS technology holds a number of benefits relative to EPSes
                        1. Data rate and wavelength agnostic
                        2. Low power consumption
                        3. Low latency
                    3. Figure 5 and Figure 6 show the internal of Palomar OCS. Very useful for understanding.
                    4. Image processing of a single camera image for Micro-Electro-Mechanical Systems (MEMS) mirror control greatly simplifies manufacturing
                       A servo (control hardware/firmware) utilizes the camera image feedback to optimize MEMS actuation for minimum loss of the optical signal path
                       the use of camera image processing for mirror controls and fulfilling datacenter volumes/requirements over a decade make the Palomar OCS unique from these other (OCS) solutions
                4. future work
                    1. future hardware evolution of optical technologies include the following: 
                        1) Larger port count OCS to enable further scale out with increased striping and to increase efficiency through more flexible topology engineering. 
                        2) Faster switching speed and/or smaller radix but lower cost OCS to allow adoption in lower layers of the datacenter network for shorter, more bursty traffic flows (i.e., TOR to AB traffic) or flexible bandwidth provisioning with adjustment of TOR oversub ratio. 
                        3) Further improvements in reliability and availability for larger OCS/failure domains and/or more uptime sensitive applications. 
                        4) Lower insertion and return loss for extensibility of the optical interconnect roadmap for continued low power consumption and cost of the transceivers.
                    2. In particular, the lack of efficient and simple buffering in the optical domain and need for high-speed burst mode receivers and/or clocking schemes that circumvent such requirements remain significant barriers to the adoption of OPS and OBS

        6. Dragonfly+: Low cost topology for scaling datacenters    [2017, 55 refs, Mellanox]
           https://www.researchgate.net/profile/Eitan-Zahavi/publication/313341364_Dragonfly_Low_Cost_Topology_for_Scaling_Datacenters/links/5a30c4baaca27271ec8a1201/Dragonfly-Low-Cost-Topology-for-Scaling-Datacenters.pdf
           https://hipineb.i3a.info/hipineb2017/wp-content/uploads/sites/6/2017/05/slides_alex.pdf
            1. mentioned in Jupiter Evolving paper as "The direct-connect Jupiter topology adopts a similar hybrid approach as in Dragonfly+ [32] where aggregation blocks with Clos-based topology are directly connected. Compared to hardware-based adaptive routing in Dragonfly+, Jupiter provides software-based traffic engineering that can work on legacy commodity silicon switches"
            2. Dragonfly+ differs from Dragonfly in that routers inside the group are connected in Clos-like topology. The area is HPC. We conclude our findings by simulations
            3. highlights
                1. HPC Common topologies: Fat Tree, Dragonfly, Hyper-cube, Torus, SlimFly
                    1. Keys to topology evaluation:
                    2. Network throughput - for various traffic patterns.
                    3. Network diameter – min/average/max latency between end-hosts.
                    4. Scalability – cost of adding new end-hosts
                    5. Cost per end host – number of network routers/ports per end-host. 
                2. see slides Page 5: Dragonfly vs Dragonfly+
                    1. in a subnet group, Dragonfly is full connection, while Dragonfly+ is bi-partite connection
                    2. Dragonfly+ subnet group is even more similar to Jupiter networking's Aggregation Block.
                       But group to group connection is different, Dragonfly+ uses full connection, Jupiter still uses bi-partite connection
                        1. in summary, Dragonfly+ differs from Dragonfly in that routers inside the group are connected in Clos-like topology
                           Dragonfly+ is superior to conventional Dragonfly due to the significantly larger number of hosts which it is able to support
                        2. Dragonfly+'s area is HPC, while Dragonfly didn't mention HPC in paper
                3. routing protocol
                    1. Multi-Path Non-Minimal Routing
                    2. Fully Progressive Adaptive Routing (FPAR) with Adaptive Routing Notification (ARN) messages
                    3. In comparison, Jupiter is simply for routing, it just uses a centralized SDN controller to determine routing and pushdown to end switches

            n. related materials
                1. Technology-Driven, Highly-Scalable Dragonfly Topology    [2008, 928 refs, Google]
                   https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/34926.pdf
                   https://www.cs.umd.edu/class/spring2021/cmsc714/student-slides/XW-1.pdf
                    1. this is the older version of Dragonfly topology. the topology in comparison is flattened butterfly, which is under the same authors
                    2. highlights
                        1. for large networking, very high radix router is needed by infeasible. instead, we use a subnet of routers and treat it as a virtual high radix router
                            1. this should be similar with Jupiter's "Aggregation Block". but unlike typical Clos connection, see Figure 5 Dragonfly router can directly connect to same level other routers
                        2. routing protocol is based on UGAL. but modification is needed to handle indirect or remote information
                            1. Apply Valiant's algorithm for load balancing - It splits traffic across all available paths (direct and transit) based on the path capacity
                            2. Indirect Adaptive Routing

        7. B4 and After: Managing Hierarchy, Partitioning, and Asymmetry for Availability and Scale in Google’s Software-Defined WAN    [2018, 111 refs, SIGCOMM, Google]
           https://research.google/pubs/pub47191/
           https://pages.cpsc.ucalgary.ca/~carey/CPSC641/slides/sdn/B4-2018-slides.pdf
           https://www.youtube.com/watch?v=nzNOWu6yOOc&t=18s
            1. hierarchical topology with supernodes and sidelinks. 100x more traffic 60x more tunnels, hierarchical topology, supernode-level TE (TSG)
            2. highlights
                1. Flat topology scales poorly and hurts availability
                    1. Jumpgate: Two-layer Topology - supernodes with sidelinks
                        1. Support horizontal scaling by adding more supernodes to a site
                        2. Support vertical scaling by upgrading a supernode in place to new generation
                    2. previous bad choice - add a new site at close location (see paper section 2.1)
                    3. My questions
                        1. we know supernode introduced is a two-layer Clos network. for site to site connection with supernode, which of the layer 1 or layer 2 are connecting to another site?
                            1. "Each supernode is a 2-stage folded-Clos network. Half the ports in the lower stage are external-facing and can be flexibly allocated toward peering B4 sites, cluster fabrics, or other supernodes in the same site"
                2. Solving capacity asymmetry problem in hierarchical topology is key to achieve high availability at scale
                    1. Solution = Sidelinks + Supernode-level TE
                    2. Tunnel Split Group (TSG)
                        1. key points
                            Supernode-level traffic splits;
                            No packet encapsulation;
                                1. traditionally TE algorithm needs tagging/encapsulation.
                                   tagging/encapsulation twice overall makes ECMP hashing hard, because switch chip can only process 1 wrap.
                                   this paper coined the intra-site TE algorithm that doesn't need it.)
                            Calculated per site-level link
                        2. How-to: Greedy Exhaustive Waterfill Algorithm
                            1. Iteratively allocate each flow on their direct path (w/o sidelinks) or alternatively on their indirect paths (w/ sidelinks on source site) until any flow cannot be allocated further
                            2. Provably forwarding loop, take less than 1 second to run, low abstraction capacity loss
                        3. TSG Sequencing Problems - Transient Forwarding loop, Blackhole
                            1. Solution: Dependency Graph based TSG Update
                                1. Map target TSGs to a supernode dependency graph
                                2. Apply TSG update in reverse topological ordering*
                                    1. Most cases only need one or two steps
                            2. Earlier work enables loop-free update with two-phase commit [31] and dependency tree/forest based approach [28]. 
                               More recently, Dionysus [21] models the network update as a resource scheduling problem and uses critical path scheduling to dynamically find a feasible update schedule.
                               However, these efforts assume tunneling/version tagging, leading to the previously described hashing problem for our hierarchical TE.
                3. Scalable switch forwarding rule management is essential to hierarchical TE
                    1. Multi-stage Hashing across Switches in Clos Supernode
                        1. Ingress traffic at edge switches: TSG site-level split
                           At spine switches: TSG supernote-level split
                           Egress traffic at edge switches: Port/trunk split
                        2. Enable hierarchical TE at scale: Overall throughput improved by >6%

            n. related materials
                1. B4: experience with a globally-deployed software defined wan    [2013, 2884 refs, SIGCOMM, Google]
                   https://dl.acm.org/doi/pdf/10.1145/2486001.2486019
                   https://homepages.dcc.ufmg.br/~mmvieira/cc/slides/Aula%2008%20-%20B4-google-simcomm13.pdf
                    1. Jupiter for datacenter networking, B4 for WAN networking in Google. More specifically Google's private WAN connecting global datacenter sites.
                       SDN with OpenFlow to control simpler edge switches built from commodity hardware.
                       Centralized traffic engineering service drives links to nearly 100% utilization. Split flow to multiple paths to balance capacity against application priority.
                       Overall, the backing design principles are consistent with Jupiter and Orion
                    2. highlights
                        1. architecture overview
                            1. From Jupiter, at S1/S2 there is one dedicated Aggregation Block used for external communication - the FBR, See "Jupiter Rising" Figure 15 option (iv)
                               Orion works as the SDN controller. Each site A,B,C (an autonomous system) has its own Orion domain of SDN controller. SDN uses OpenFlow protocol.
                               Site to Site communication uses iBGP, Site to public internet communication uses eBGP. Site A,B,C collectively composes the B4 WAN 
                            2. globally it runs the Central TE server for overall bandwidth allocation.
                               Each Orion domain runs a local TE App, which communicates with Central TE server and enforces bandwidth optimization locally
                               TE means Traffic Engineering
                        2. TE Optimization Algorithm
                            1. Target: Achieve max-min fairness.
                                Tunnel Selection: selects the tunnels to be considered for each FG (Flow Group).
                                Tunnel Group Generation: allocates bandwidth to FGs using bandwidth functions to prioritize at bottleneck links.
                                Tunnel Group Quantization: changes split ratios in each FG to match the granularity supported by switch hardware tables.
                            2. TE abstracts each site into a single node with a single edge of given capacity to each remote site
                               B4 routers employ a custom variant of ECMP hashing [37] to achieve the necessary load balancing

                2. Google, Subhasree Mandal — Lessons Learned from B4, Google's SDN WAN    [2016]
                   https://www.youtube.com/watch?v=tVNlXg0iN-g
                    1. Traffic Engineering vs Shortest Path
                    2. conclusion
                        1. SDN is beneficial in real-world
                            1. centralized TE delivered upto 30% additional throughput
                            2. decoupled software and hardware rollout
                        2. lessons to work in practice
                            1. System performance: Flow control between components
                            2. Availability: Robust reachability for master election
                            3. Scale: Hierarchical topology abstraction

        8. BBR: congestion-based congestion control    [2016, 779 refs, Google]
           https://research.google/pubs/pub45646/
           [译] [论文] BBR：基于拥塞（而非丢包）的拥塞控制（ACM, 2017）
           http://arthurchiao.art/blog/bbr-paper-zh/
            1. DCTCP/DCQCN are recognized datacenter networking congestion control protocols. What are counter techniques for WAN networking?
               TCP BBR is the congestion control protocol by Google B4. By 2016 all B4 TCP traffic goes through BBR. YouTube Edge also deployed BBR.
               "TCP BBR 不再使用丢包作为拥塞的信号，也不使用 “加性增，乘性减” 来维护发送窗口大小，而是分别估计极大带宽和极小延迟，把它们的乘积作为发送窗口大小。" "在有一定丢包率的网络链路上充分利用带宽"
            2. highlights
                1. key diff between datacenter networking vs WAN networking
                    1. WAN has more frequent packet loss. while datacenter usually only loss packet when switch buffer overflowed
                    2. WAN latency is much higher. there are more switches and buffers in middle. latency is affected by switch buffering.
            n. related materials
                1. Linux Kernel 4.9 中的 BBR 算法与之前的 TCP 拥塞控制相比有什么优势？ - 李博杰
                   https://www.zhihu.com/question/53559433
                    1. "网络内尚未被确认收到的数据包数量 = 网络链路上能容纳的数据包数量 = 链路带宽 × 往返延迟"
                       "TCP 维护一个发送窗口，估计当前网络链路上能容纳的数据包数量"
                       "标准 TCP 的这种做法有两个问题："
                            "“加性增，乘性减” 的拥塞控制算法要能正常工作，错误丢包率需要与发送窗口的平方成反比"
                            "标准 TCP 是通过 “灌满水管” 的方式来估算发送窗口的 .. 这个问题被称为 bufferbloat（缓冲区膨胀）"
                                "缓冲区膨胀有两个危害："
                                    "增加网络延迟。buffer 里面的东西越多，要等的时间就越长"
                                    "共享网络瓶颈的连接较多时，可能导致缓冲区被填满而丢包。很多人把这种丢包认为是发生了网络拥塞，实则不然"
                    2. "TCP BBR 是怎样解决以上两个问题的呢？"
                        1. "既然不容易区分拥塞丢包和错误丢包，TCP BBR 就干脆不考虑丢包。"
                        2. "既然灌满水管的方式容易造成缓冲区膨胀，TCP BBR 就分别估计带宽和延迟，而不是直接估计水管的容积。" "带宽和延迟的乘积就是发送窗口应有的大小"
                        3. "TCP BBR 解决带宽和延迟无法同时测准的方法是：交替测量带宽和延迟；用一段时间内的带宽极大值和延迟极小值作为估计值。"
                    3. "TCP BBR 采用类似标准 TCP 的慢启动"
                        1. "标准 TCP 遇到任何一个丢包就会立即进入拥塞避免阶段"
                        2. "TCP BBR 则是根据收到的确认包，发现有效带宽不再增长时，就进入拥塞避免阶段"
                        3. "慢启动结束后，为了把多占用的 2 倍带宽 × 延迟消耗掉，BBR 将进入排空（drain）阶段，指数降低发送速率，此时 buffer 里的包就被慢慢排空，直到往返延迟不再降低"
                    4. "TCP BBR 不再使用丢包作为拥塞的信号，也不使用 “加性增，乘性减” 来维护发送窗口大小，而是分别估计极大带宽和极小延迟，把它们的乘积作为发送窗口大小。"
                        "BBR 解决了两个问题："
                            1. "在有一定丢包率的网络链路上充分利用带宽。非常适合高延迟、高带宽的网络链路。"
                            2. "降低网络链路上的 buffer 占用率，从而降低延迟。非常适合慢速接入网络的用户。"
                            3. "TCP 拥塞控制算法是数据的发送端决定发送窗口，因此在哪边部署，就对哪边发出的数据有效。
                                如果是下载，就应在服务器部署；如果是上传，就应在客户端部署。"
                    5. "
                    这篇论文并没有讨论（仅有拥塞丢包情况下）TCP BBR 与标准 TCP 的公平性。
                    也没有讨论 BBR 与现有拥塞控制算法的比较，如基于往返延迟的（如 TCP Vegas）、综合丢包和延迟因素的（如 Compound TCP、TCP Westwood+）、基于网络设备提供拥塞信息的（如 ECN）、网络设备采用新调度策略的（如 CoDel）。"
                       "实测结果这么好，也是因为大多数人用的是 TCP Cubic (Linux) / Compound TCP (Windows)，在有一定丢包率的情况下，TCP BBR 更加激进，抢占了更多的公网带宽。因此也是有些不道德的感觉。）"
```