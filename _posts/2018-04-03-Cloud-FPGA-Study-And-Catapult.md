---
layout: post
title: "Cloud FPGA Study And Catapult"
tagline : "Cloud FPGA Study And Catapult"
description: "Cloud FPGA Study And Catapult"
category: "storage"
tags: [storage, accelerator, fpga]
---
{% include JB/setup %}

Summary of study, see respective WeiChat articles.

  * [Interesting Papar FPGA Catapult (P1)](https://mp.weixin.qq.com/s/JID96e0votEWvghAlN7UCw) [PDF](/images/weichat-fpga-catapult-p1.pdf)
  * [Interesting Papar FPGA Catapult (P2)](https://mp.weixin.qq.com/s/hcnB0tKJQfuUWEuI4ZWNGw) [PDF](/images/weichat-fpga-catapult-p2.pdf)
  * [Interesting Paper FPGA Catapult (P3)](https://mp.weixin.qq.com/s/0U_tIxOoOoKxfBl2A_XC0g) [pdf](/images/weichat-fpga-catapult-p3.pdf)

Raw notes, containing all the read list.

```
1. readings: cloud FPGA related readings
    1. Down to the TLP (Transaction layer packet): How PCI express devices talk
       http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-1
       http://xillybus.com/tutorials/pci-express-tlp-pcie-primer-tutorial-guide-2
        1. good to read. PCI works like a network switching with physical layer, data link layer, and transaction layer; rather than "bus"
    2. Considerations for host-to-FPGA PCIe traffic
       http://xillybus.com/tutorials/pci-express-dma-requests-completions
    
    3. A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services    [469 refs, 2014]
       https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Catapult_ISCA_2014.pdf
        1. good to read. but now new better design is the follow-up paper "A Cloud-Scale Acceleration Architecture"
           Bing's FPGA cloud design, PCIe attach, homogenous single FPGA per server, SAS cable interconnect with routing.
           run Bing's ranking engine. 95% ranking throughput improvements
        2. highlights
            1. Catapult: middle-scale (1632 servers) datacenter FPGA architecture design
                1. hardware design
                    1. single highend FPGA per server, attach to PCIe, equaipped with DRAM on FPGA chip
                        1. though there are central FPGA rack/host alternatives, server homogeneity is a concern
                        2. select PCIe to minimize distruption to next generation server design.
                            1. not GPU due to concern for power requirement
                            2. not attach to memory bus or CPU QPI due to occupies CPU socket
                            3. not ASIC, due to we need reconfigurable (fast app develop iteration)
                        3. DIMMs with ECC to add resilience
                    2. FPGA interconnection: 10Gb SAS cable, 2D-mesh connection (each 1 to 4)
                        1. FPGA implements routing internally
                        2. FPGA link supports 20Gb/s peak bidirectional bandwidth, at sub-microsecond latency
                        3. Support ECC for network resilience
                        4. drawbacks: one FPGA issue may crash/stall 4 neighbor nodes
                                      scale is limited, due to SAS compared to ethernet network
                    3. TCO: FPGA architecture increase TCO < 30%, power budget < 10%
                2. software design
                    1. FPGA to host CPU interface
                        1. low latency achieved by avoiding system calls
                        2. thread safety achieved by statically divide buffer and assign exclusively to each thread
                        3. fairness achieved by taking snapshot of full bits periodically and DMAing them at priority
                        4. user-level app may initiate FPGA reconfiguration and partial-reconfiguration by calling to low-level lib
                    2. Shell/Role architecture
                        1. Shell: reusable common portion of program logic, pre-built into FPGA
                            1. Including: DMA engine, PCIe core, DDR core (with ECC), inter-FPGA router, SL3 serial link protocol (with ECC), etc
                            2. routing by static software-configured routing table
                                1. transport protocol has no retransmission or source buffering.
                                   simple as to reduce consumed FPGA capacity, and performance overhead
                                   double-bit error dectection, single-bit error correction, ECC, CRC are used to improve packet reliability (on SAS cable)
                                   packet loss is few, rely on high-level app to do retransmit
                            3. SEU scrubber runs continously to scrub FPGA configuration errors
                            4. in all, Shell consumes 23% of each FPGA capacity
                        2. Role: the application logic, which can be partial-reconfigured
                    3. Infrastructure
                        1. Mapping Manager manages FPGA configurations and correction
                           Health Monitor monitors failure and corrects them
                        2. Correct operation
                            1. to avoid FPGA crash/crashed-by neightbors through SAS link, need "TX/RX Halt" to mask in/out traffic when reconfiguring
                            2. to recover from failure: soft reboot, hard reboot, mark out-of-service
                        3. debugging support
                            1. lightweight Flight Data Recorder. I.e. keep important events in on-chip memory to be later dumped out for investigation
                3. application cases
                    1. Bing's ranking engine
                        0. the section 4 has good description for how Bing search & ranking works.
                        1. Most features are implemented on FPGA.
                        2. One ranking service is partitioned in to a ring of 8 FPGAs, whose pipeline managed by Queue Manager
                           Different language (Spanish, English, Chinese, etc) requires different Models, each model consists a differet set of ring
                           Model reload is expensive and needs FPGA reconfiguration
            2. related works
                1. good part to read. and follow-up paper "A Cloud-Scale Acceleration Architecture" has better taxonomy
        n. related materials
            1. An FPGA-based In-line Accelerator for Memcached    [2014, 49 refs]
               https://www.hotchips.org/wp-content/uploads/hc_archives/hc25/HC25.50-FPGA-epub/HC25.27.530-Memcached-Lavasani-UTexas.pdf
                1. build Memcached logic into FPGA chip
            2. What is an LUT in FPGA?
               https://electronics.stackexchange.com/questions/169532/what-is-an-lut-in-fpga
            3. FPGA Architecture - Altera
               https://www.altera.com/content/dam/altera-www/global/en_US/pdfs/literature/wp/wp-01003.pdf
    
    4. A Cloud-Scale Acceleration Architecture
       ftp://ftp.cs.utexas.edu/pub/dburger/papers/MICRO16.pdf
        1. good to read.
           Catapult v2 use ethernet instead of SAS for FPGA interconnection as compared to v1. FPGA is connected "bump-in-the-wire" to NIC.
           It achieves 2x throughput while meeting latency target, which means only half servers are needed. 
           It has been deploying in production of 5,760 servers, accelerating Bing search ranking and Azure software-defined networks and network crypto
        2. highlights
            1. compared the previous "Catapult v1: A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services",
               use ethernet networking for FPGA interconnect, instead of SAS cable, to achive much larger scale
                0. previous SAS interconnection suffers from: scale limitation, one FPGA crashes neighbors
                1. FPGA is connected "bump-in-the-wire" to NIC. it can do network acceleration
                    1. CPU frequency scaling and Moore's Law is ending.
                       40Gb/s network requries ~5 cores of 2.4GHz CPU to process encryption/decryption (1.2 cycles per byte)
                       scale-out can hardly help in this case. only FPGA can help
                    2. network protocol and routing - LTL: lightweight transport layer
                        0. previous SAS has sub-microsecond latency, and ethernet has ~10 us latency. slower but ok
                        1. remote FPGA appears even closer to the local FPGA, than host access to local SSD, or host network stack
                        2. partial-reconfiguration allows NIC traffic through FPGA not interrupted
                        3. LTL has buffer, flow control, retransmission, packet ordering.
                        4. connections are statically allocated and persistent in table
                        5. datacenter networks have traffic class that differentiate FPGA routing traffic
                        6. Elastic Router handles ports: PCIe DMA, Role, DRAM, Remote (to LTL)
                2. local acceleration
                    1. app access local FPGA, and FPGA also have function built in Shell to access remote FPGAs, the global pool
                    2. the NIC pass through traffic in FPGA and search ranking acceleration has no performance intervention
                    3. throughput increases by 2.25x with no latency penalty, which means only half servers are needed
                3. remote acceleration
                    1. one server can consume more than one FPGA in remote pool
                    2. the latency overhead of remote compared to local FPGA is minimal
                    3. the hardware-as-a-service model
            2. deployment and evaluation
                1. mirror live traffic from Bing to the test bed for one month
            3. related works
                1. taxonomy of how FPGA/GPU/ASIC acceleration interfaces with CPU, and intercommunication
                   this part is very good to read
                    1. alternatives
                        1. CPU-Accelerator memory integration
                            1. (C) - Coherent accelerators, where data movement is handled by a memory coherence protocol
                            2. (I) - I/O level, where data movement is done via DMA transfers, and
                            3. (N) - Network level, where data movement is done via Ethernet (or other) packet
                        2. Accelerator connectivity scale
                            1. (S) Single server / single appliance
                            2. (R) Rack level
                            3. (D) Datacenter scale
                        3. Accelerator type
                            1. (F) FPGAs
                            2. (G) GPUs
                            3. (A) ASICs
                    2. categories
                        1. NSF: Network/Single/FPGA
                        2. IRF: IO/Rack/FPGA: Catapult v1, etc
                        3. ISF: IO/Single/FPGA: this paper is both ISF and NDF
                        4. ISFG: IO/Zero/FPGA+GPU
                        5. CSF: Coherent/Single/FPGA
                        6. ISG: IO/Single/GPU
                        7. ISA: IO/Single/ASIC
                        8. NDF: Network/Datacenter/FPGA: only this paper, Catapult v2.
                2. promising programmable accelerator architectures, but not yet reached level of business production: MPPAs, CGRAs
            4. questions
                1. the high-level distributed task scheduling framework, like what Hadoop Mapreduce does, is still absent in this paper
        n. related materials
            1. How does FPGA works?    [2007, 438 refs]
                1. FPGA Architecture: Survey and Challenges
                   http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.153.3122&rep=rep1&type=pdf
                    1. Altera - FPGA logic block
                       https://www.altera.com/en_US/pdfs/literature/wp/wp-01003.pdf
                2. How does an FPGA work?
                   https://embeddedmicro.com/tutorials/mojo-fpga-beginners-guide/how-does-an-fpga-work
                    1. "The Routing Matrix .. These connections are again defined in RAM which is why the FPGA must be reconfigured every time the power is cycled"
                    2. "This is why you will never be able to clock an FPGA at speeds comparable to a dedicated chip.
                        An ASIC design can reach speeds faster than 4GHz, while an FPGA is very fast if it's running at 450MHz"
                        "This is also why FPGAs consume considerably more power than their ASIC counterparts."
                3. FPGA How do they work?
                   http://www.eit.lth.se/fileadmin/eit/courses/eti135/slides/FPGA_Anders_Stedan.pdf
                4. Computer Hardware: How do field-programmable gate arrays (FPGAs) work?
                   https://www.quora.com/Computer-Hardware-How-do-field-programmable-gate-arrays-FPGAs-work
                5. FPGAs - How do they work?
                   http://www.fpga4fun.com/FPGAinfo2.html
                    1. hardware graphs
                6. How FPGAs work, and why you'll buy one
                   https://www.embeddedrelated.com/showarticle/195.php
                    1. "true" FPGA vs real modern FPGA
                    2. visualized FPGA chip view
                7. What are FPGAs and how do they work
                   https://indico.cern.ch/event/283113/contributions/1632265/attachments/522019/720041/Zibell_How_FPGAs_work.pdf
                8. Field-programmable gate array
                   https://en.wikipedia.org/wiki/Field-programmable_gate_array
                    1. Introduction: the FPGA-ASIC Gap
                        1. chip area: ~18x larger
                           dynamic power: ~14x more
                           clock speed: ~3-5x slower
                    2. "Full initial configuration ~ 1-2 seconds in practice"
                    3. "Partial reconfiguration is also referred as context switching"
            
            2. How long does FPGA reconfigures, and what about partitial reconfiguration?
                1. How to take advantage of partial reconfiguration in FPGA designs
                   https://www.eetimes.com/document.asp?doc_id=1274489
                    1. there are bunch of requirements and guidelines for use of partial reconfiguration
                2. Partial FPGA reconfiguration and performance
                   https://stackoverflow.com/questions/17226631/partial-fpga-reconfiguration-and-performance
                    1. "Big FPGAs can be many 10s to 100s of milliseconds to completely reconfigure."
                       "A small configuration can be achieved within the PCI express startup time (100ms IIRC)"
                3. Reconfiguration time?
                   https://forums.xilinx.com/t5/7-Series-FPGAs/Reconfiguration-time/td-p/484046
                    1. "... requires ~28 ms to receive its 3.6 Mb of configuration data"
                    2. PartialReconfiguration User Guide, "Configuration Time" section
                       https://www.xilinx.com/support/documentation/sw_manuals/xilinx12_3/ug702.pdf
                        1. configuration port bandwidth: 66Mb/s ~ 3.2Gb/s
                4. Partial Reconfiguration on FPGAs
                   http://www.uio.no/studier/emner/matnat/ifi/INF5430/v11/undervisningsmateriale/lecture_slides_dirk/lecture_RC.pdf
            
            3. How to virtualize FPGA on cloud, i.e. multitenant, pooling, sharing, isolation, etc?
                1. Catapult v2 usage on Azure SDN - Azure Smart NIC
                   https://www.slideshare.net/insideHPC/inside-microsofts-fpgabased-configurable-cloud
                    1. indeed SDN witnesses performance issues, which need to be handled by introducing acceleration hardware such as FPGA on NIC
                
                2. Virtualized FPGA Accelerators for Efficient Cloud Computing    [2015, 24 refs]
                   https://warwick.ac.uk/fac/sci/eng/staff/saf/publications/cloudcom2015-fahmy.pdf
                    1. virtual FPGAs (vFPGAs): physical FPGA is divided into multiple partially reconfigurable regions (PRRs);
                       A vFPGA can be partial-configured to implement multiple virtual FPGA accelerators (vFAs)
                    2. An interface switch ensures each vFPGA is served in a fair manner with round robin arbitration for access to the PCIe and DRAM data streams
                    3. FPGA Driver, client API SDK, Hypervisor, FPGA allocation, Resource Manager
                    4. app case study: mapreduce accelerator for word counting
                
                3. How Microsoft uses FPGA in Bing, ASIC Holographic Processing Unit (in HoloLens), Azure network, 
                   https://arstechnica.com/information-technology/2016/09/programmable-chips-turning-azure-into-a-supercomputing-powerhouse/
                    0. good to read, tells how MS using the FPGA from start to Bing and Azure clouds; help understand the above two papers
                    1. instead of highend NIC's SR-IOV (limitation, e.g. only assign to 4-VMs at max), MS uses FPGA+shared NIC across VMs.
                       Also, network SDN functionalities equivalents of tunneling/VLAN/VxLAN/GRE and routing are implemented in the FPGA
                    n. related materials
                        1. Virtualizing PCI and PCIe
                           https://arstechnica.com/information-technology/2010/02/io-virtualization/
                            0. enumerating, paravirtualization, PCI pass-through
                            1. for PCI pass through, Intel's VT-d and AMD's AMD IOMMU/AMD-Vi solves the VM virtual to host physical memory mapping issue
                            2. next, PCIe needs to extended, so that one physical device's multiple VFs can be mapped to multiple VMs.
                               i.e. PCIe Single Root I/O Virtualization specification (SR-IOV)
                
                4. Virtualized Execution Runtime for FPGA Accelerators in the Cloud    [2017, 1 refs]
                   http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7840018
                    1. good paper to read, tells the end-to-end framework from app dev toolchain, to scheduling virtualization on FPGA cloud, to protection and security
                       further work on "Virtualized FPGA Accelerators for Efficient Cloud Computing", sharing one same author
                    2. highlights
                        1. a complete end-to-end framework to allow apps run on cloud with FPGA, including dev tool chain.
                            enables developers to view FPGAs asa computational resource similar to CPUs,
                                providing facilities such as memory management,
                                virtualisation and a hardware abstraction layer
                            We also provide a design flow that enables developers to write FPGA-accelerated applications at different levels of abstraction,
                                up to high-level DSLs where CPU-FPGA partitioning and interaction are done seamlessly
                        2. designs
                            1. FPGA includes,
                                runtime: Local processor, runtime system, user threads.
                                PR regions: for app to write accelerators.
                                Memory: on FPGA chip, app accelerator accesses it by Local processor
                            2. toolchain generates an FPGA application package,
                                which includes the specifications of the hardware accelerators
                                and code to be run on the local processor
                            3. features required for the cloud
                                Memory management
                                    — Virtual memory
                                    — Dynamic memory allocation and deallocation
                                • Shared execution
                                    — Multi-process
                                    — Multi-user
                                    — Workload-dependent resource allocation
                                • Protection
                                    — Memory and hardware protection
                                    — Protection rings
                                • Application execution
                                    — Loader
                                    — Scheduler
                                • Code portability
                                    — Hardware abstraction layer
                            4. "a local processor, which can interact with the accelerators and access FPGA resources with lower latency than the host CPU"
                                1. the local processor is not for processing the application task, but to help accelerator access FPGA peripherals
                            5. "Even when the PR regions all have the same size, it is still possible to scale the area and performance of an application
                                by partitioning accelerators into multiple smaller replicas that operate in parallel [13]"
                        3. related materials
                            1. A platform-independent runtime methodology for mapping multiple applications onto FPGAs through resource virtualization    [2013, 4 refs]
                               https://pdfs.semanticscholar.org/3a7a/53a5530aa5b07e9e051dfd0433f9928eecca.pdf
                                1. virtual FPGA cores
                                    1. Portability across different FPGA devices
                                    2. CoreManager decides which FPGA's which region should be placed with the vFPGA core requested by application
                                    3. "CoreFusion" allows to merge adjacent cores
                                    4. FPGA capacity fragmentation issue
                            2. Enabling FPGAs in the Cloud    [2014, 42 refs]
                               http://nics.ee.tsinghua.edu.cn/people/wangyu/Enabling%20FPGAs%20in%20the%20Cloud.pdf
                                0. as referenced in "Virtualized Execution Runtime for FPGA Accelerators in the Cloud": "does not perform any dynamic management of accelerator slots"
                                   good to read. the paper proposed abstract pooling concepts PRP vs AP, acceleration slots. and many details in the FPGA-Hypervisor co-design.
                                   It uses KVM and Openstack
                                1. prototype implemented based on OpenStack, Linux-KVM and Xilinx FPGAs
                                2. highlights
                                    1. core features mentioned in abstract
                                        1. isolation between multiple processes in multiple VMs
                                            1. FPGA partial partition, regions / acceleration slots, GPA-HPA (Guest/host physical address) translation (VM-nocopy)
                                                1. the  slot layout cannot be changed unless whole FPGA is reconfigured
                                            2. DMA parameter checking, (alternative is IOMMU but not used), FPGA internal bandwidth control.
                                               in FPGA SL (service logic) governs them
                                        2. precise quantitative acceleration resource allocation
                                            1. Openstack is the cloud provider
                                        3. priority-based workload scheduling
                                            1. SL facilitates accelerator bandwidth and priority management.
                                            2. Openstack Nova scheduler for acceleration & slots scheduling
                                               accelerators are scheduled considering their various requirements for computation and I/O resources
                                    2. resource abstraction
                                        1. instead of abstracting PRP (programmable resource pool), we abstract AP (accelerator pool)
                                           "An accelerator design following standards can be mapped into standard slots"
                
                5. High Performance in the Cloud with FPGA Groups    [2016, 3 refs]
                   http://www.globule.org/publi/HPCFV_ucc2016.pdf
                    1. good, interesting to read. Note that the paper is on HPC
                       proposed FPGA group to aggregrate multiple physical FPGAs to one big virtual
                       and API remoting as another way to vritaulize FPGA access
                    2. highlights
                        1. abstract
                            1. "FPGA groups, which are seen by their clients as a single virtual FPGA"
                                1. FPGAs in group are configured with exact same circuit design
                                   load-balancing incoming execution requests to them
                            2. "an autoscaling algorithm to maximize FPGA groups’ resource utilization"
                        2. challenges
                            1. "maximizing utilization", "capacities ranging"
                            2. the lack of satisfactory techniques for virtualizing FPGAs
                                1. current solutions
                                    1. based either on statically partitioning the gate array between ultiple applications (i.e., sharing in space)
                                        1. sharing in space implies that each application must use a smaller number of digital gates, thereby negatively impacting performance
                                        2. However, space sharing reduces the area that is made available to host an FPGA design, which can have a considerable performance impact because it limits the number of functional units that can work in parallel
                                        3. Sharing in space also requires some switching logic in the FPGA to route incoming requests to the appropriate design, which can add additional overhead
                                    2. on naive context switching (i.e., sharing in time)
                                        1. incurs prohibitive context switching costs, as reconfiguring an  PGA from one circuit design to another takes in the order of a couple of seconds
                                        2. actually this approach is usually overlooked 
                                        3. AWS EC2 GPGPU is shared by PCI passthrough
                                2. another view
                                    1. existing: I/O passthrough, Paravirtualization
                                    2. this paper proposed: API remoting
                                        1. like OpenCL or CUDA, calls to the API are intercepted in the VM and passed through to the host OS on which the accelerator is accessible.
                                            1. It's more like mutiple clients sharing access to a web server
                                            2. A number of technologies employ API remoting over a network including rCUDA [10], DS-CUDA [20], dOpenCL [17] and VirtualCL [5]. Additional studies with Infiniband networks show that this is a practical solution for rCUDA [24] and DS-CUDA [16]
                        m. questions
                            1. if accelerator is partitioned across multiple physical FPGAs, how to deal with the communication management and overhead?
                                1. the paper assumes infiniband network
                                   the paper is using "MPC-X" appliance
                                   Note that the paper is a HPC paper
                    
                    6. Overlay Architectures For FPGA Resource Virtualization    [2016, 1 refs]
                       https://hal.archives-ouvertes.fr/hal-01405912/document
                        1. "Adding special features to the overlay implementations such as dynamic clock control
                            and a state snapshot mechanism allows performing hardware task preemptive scheduling and live migration"
                        2. related materials
                            1. ZUMA: An Open FPGA Overlay Architecture    [2012, 66 refs]
                               http://www1.cse.wustl.edu/~roger/565M.f12/4699a093.pdf
                                1. "ZUMA reduces this penalty to as low as 40x"
                                2. highlights
                                    1. "Previous attempts to map an FPGA architecture into a commercial FPGA have had an area penalty of 100x at best [4]"
                                       "ZUMA reduces this penalty to as low as 40x"

                    7. FPGA Virtualization for Enabling General Purpose Reconfigurable Computing
                       http://cc.doc.ic.ac.uk/fresh16/Dirk.pdf
                        1. good material. tells industry status
                        2. highlights
                            1. FPGAs in Datacenters: Where are we?
                                1. Intel took over the second biggest FPGA vendor (Altera) one year ago for US$ 16.7B
                                2. Microsoft: 1632 servers with FPGAs for Bing Search -> 2x throughput, 29% less latency, ~2x energy efficiency
                                3. Baidu: search algorithm acceleration using FPGAs -> 3.5x more throughput than a GPU at 10% power
                            2. FPGAs Virtualization: Where are we?
                                1. Two main directions
                                    1. Overlays: a programmable architecture on top of an FPGA
                                        1. software like instead of RTL coding, portability, and reuse funcional blocks
                                        2. VectorBlox, Dragon processor (bioinformatics)
                                    2. Dynamic FPGA modules: temporal partitioning
                                        1. Maximize resource utilization, Runtime adaptability, Fault tolerance, Saving energy
                                        2. Move modules around for masking faults
                            3. FPGA Database Accelerator
                        3. related materials
                            1. An Efficient FPGA Overlay for Portable Custom Instruction Set Extensions    [2013, 22 refs]
                               https://pdfs.semanticscholar.org/2d04/22cc490db8b2069134f27bde85c9458af8e8.pdf
                                1. FPGA Overlay to virtualize FPGA is more like an effort from FPGA community,
                                   while the partition/region/accelerator-slot is more like from the cloud community
                                2. highlights
                                    1. challenges
                                        1. for FPGAs, there is no direct path to use identical configuration bitstreams from different vendors. not like binary-compatible CPU
                                    2. beyond partition/region/accelerator-slot, API remoting (interception);
                                       here's a new way to virtualize FPGA: FPGA overlay
                                        1. the concept is like JVM, shipping bytecode 
                                        2. custom instruction set extensions
                                        3. physical:virtual LUT ratio
                                        2. looks like the Overlay is done by manipulating FPGA logic resources, circuit-level stuff ..
                                3. questions
                                    1. now the market of FPGA is dominated by Altera and Xillix, so we don't actually have too many incompatible binarystreams, right?
                                       If I only buy FPGA from one Vendor, like we only buy CPU from Intel, then we don't need the overlay bytecode and "JVM".

                    8. FPGAs in the Cloud: Booting Virtualized Hardware Accelerators with OpenStack    [2014, 74 refs]
                       http://ieeexplore.ieee.org/document/6861604/
                        1. no original paper. only reading from abstract.
                           treat booting accelerators as booting VMs; good thought.
                           virtualization is done by "Partially reconfigurable regions"
                        2. highlkghts
                            1. Partially reconfigurable regions across multiple FPGAs are offered as generic cloud resources through OpenStack (opensource cloud software),
                               thereby allowing users to “boot” custom designed or predefined network-connected hardware accelerators with the same commands they would use to boot a regular Virtual Machine
                            2. Our system can set up and tear down virtual accelerators in approximately 2.6 seconds on average
                            3. The static virtualization hardware on the physical FPGAs causes only a three cycle latency increase and a one cycle pipeline stall per packet
                               in accelerators when compared to a non-virtualized system
                            4. Our study shows that FPGA cloud compute resources can easily outperform virtual machines

                6. Virtualized FPGA Accelerators in Cloud Computing Systems    [2015, 24 refs]
                   http://www.eecg.utoronto.ca/~jayar/FPGAseminar/2013/high-scale-routers-for.html
                    1. FPGAs as OpenStack Cloud Resources. We want a way to make FPGAs analogous to VMs. using "Partial Reconfigurable Regions".
                       The idea soundslooks like "FPGAs in the Cloud: Booting Virtualized Hardware Accelerators with OpenStack"
                       The whole work is based on Openstack
                    2. the material is informative.

                7. OpenStack Acceleration Service: Introduction of Cyborg Project
                   https://www.openstack.org/videos/boston-2017/openstack-acceleration-service-introduction-of-cyborg-project
                   https://wiki.openstack.org/wiki/Cyborg
                   https://github.com/openstack/cyborg
                    1. Formerly known as project Nomad. Openstack Scientific Work Group. HPC.
                       GPU hosts vs VM resource scheduling. Cyborg agents communicating to Nova. OpenCL.

            3.4. how public cloud provide FPGA?
                1. Why Public Cloud is Embracing FPGAs and You Should Too
                   https://f5.com/about-us/blog/articles/why-public-cloud-is-embracing-fpgas-and-you-should-too-24883
                2. AWS Details FPGA Rationale and Market Trajectory
                   https://www.nextplatform.com/2017/01/22/aws-details-fpga-rationale-market-trajectory/
                3. Baidu Deploys Xilinx FPGAs in New Public Cloud Acceleration Services
                   https://www.xilinx.com/news/press/2017/baidu-deploys-xilinx-fpgas-in-new-public-cloud-acceleration-services.html
                4. Baidu Public Cloud FPGA
                   https://cloud.baidu.com/product/fpga.html
                    1. "每个FPGA实例独享一个FPGA加速平台，不会在实例、用户之间共享"
                5. FPGA as Service in Public Cloud: Why and How
                   http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7929179
                6. AWS FPGA instance
                   https://aws.amazon.com/ec2/instance-types/f1/
                    1. "Once your FPGA design is complete, you can register it as an Amazon FPGA Image (AFI)"
                    2. "Each FPGA includes local 64 GiB DDR4 ECC protected memory, with a dedicated PCIe x16 connection"
                    3. "you pay for F1 compute capacity by the hour with no long-term commitments or upfront payments."
                    4. 手把手教你在FPGA实例上运行“Hello World”
                       https://aws.amazon.com/cn/blogs/china/running-hello-world-on-fpga/
                    5. Developer Preview – EC2 Instances (F1) with Programmable Hardware
                       https://aws.amazon.com/blogs/aws/developer-preview-ec2-instances-f1-with-programmable-hardware/
                        1. "The FPGAs are dedicated to the instance and are isolated for use in multi-tenant environments"
                    6. Amazon EC2 F1 Instances, Customizable FPGAs for Hardware Acceleration Are Now Generally Available
                       https://aws.amazon.com/about-aws/whats-new/2017/04/amazon-ec2-f1-instances-customizable-fpgas-for-hardware-acceleration-are-now-generally-available/
                    7. EC2 F1 Instances with FPGAs – Now Generally Available
                       https://aws.amazon.com/blogs/aws/ec2-f1-instances-with-fpgas-now-generally-available/
                7. Azure FPGA VM instance?
                    1. I didn't find any news. Why are they all about Catapult and Azure SDN?
                8. Intel FPGAs Power Acceleration-as-a-Service for Alibaba Cloud
                   https://insidehpc.com/2017/10/intel-fpgas-power-acceleration-service-alibaba-cloud/
                    1. Alibaba Cloud’s F1 Instance
                        1. tool: OpenCL or RTL
                        2. will .. a rich ecosystem of IP for ..
                9. summary
                    1. so overall, I think public cloud VM instance FPGA is done by PCI pass through
                       Baidu and AWS saying the FPGA is isolated, not shared, or dedicated.
                    2. the competivity comes from
                        1. provide FPGA VM instances, with big and more FPGA cards
                        2. develop tool chain support
                        3. rich ecosystem of IPs (reusable accelerator designs on FPGA)

            3.5. how GPU is virtualized on cloud?
                1. GPU CPU is connected via PCIe. PCIe (v2) bandwith typically 5GB/s ~ 8GB/s
                   https://devtalk.nvidia.com/default/topic/506821/data-transfer-between-cpu-and-gpu/
                   https://en.wikipedia.org/wiki/PCI_Express
                   https://www.xilinx.com/support/documentation/white_papers/wp350.pdf
                    1. PCIe bandwidth generally is much smaller than Ethernet
                       1 byte is transmitted every 4 ns (2.5Gb/s bandwidth)
                2. NVIDIA, AMD, and Intel: How they do their GPU virtualization
                   http://www.brianmadden.com/opinion/NVIDIA-AMD-and-Intel-How-they-do-their-GPU-virtualization
                    0. good to read
                    1. "In general the largest portion of the GPU is dedicated to shaders"
                    2. Approaches to virtualized GPUs
                        1. API Intercept
                            1. "The oldest of these, API Intercept, works at the OpenGL and DirectX level"
                        2. Virtualized GPU
                            1. "users get direct access to a part of the GPU"
                        3. Pass-through
                            1. "If you have two cards in your server, then you get to connect two VMs to GPUs while everyone else gets nothing"
                    3. types of GPUs
                        1.  There are three different companies making virtual GPUs: Intel (GVT-g), AMD (MxGPU), and NVIDIA (vGPU)
                        2. Virtualization
                            1. Video RAM
                                1. physical slice
                            2. Shader Engine
                                1. physical slice (AMD MxGPU; hardware); time slice (Intel GVT-g, NVIDIA vGPR; software, cannot interrupt)
                            3. GPU Compute
                                1. OpenCL; Passthrough only
                            3. Hypervisor Requirements and Hypervisor Support
                                1. SR-IOV (physical, AMD MxGPU); Software Manager (Intel, NVIDIA)
                            4. AMD is currently only certified on ESX
                               Intel supports KVM and XenServer
                               NVIDIA supports both ESX and XenServer
                               Hyper-V isn’t supported at all
                3. Enable GPU Virtualization in OpenStack
                   https://www.openstack.org/assets/presentation-media/Enable-GPU-virtualization-in-OpenStack.pdf
                4. Everything you need to know about GPU virtualization
                   http://searchvirtualdesktop.techtarget.com/essentialguide/Everything-you-need-to-know-about-GPU-virtualization
                    1. "GPU virtualization is a great way to improve application and VDI performance"
            
            4. What is the current challenge / technology edge of FPGA circle?
                1. HPC Cloud for Scientific and Business Applications: Taxonomy, Vision, and Research Challenges    [2017, 0 refs]
                   https://arxiv.org/pdf/1710.08731.pdf
                    1. good paper to read. it's for HPC. highlights
                    2. highlighs
                        1. HPC Cloud Efforts: Viability
                            1. compared to traditional HP cluster, cloud features in "elastic"
                            2. latency-limited applications, where numerous small point-to-point messages are exchanged, are most penalized in cloud
                               bandwidth-limited applications, where exchanging few large messages, or perform collective communication, are less penalized
                            3. network virtualization and hardware heterogenety are main causes of poor performance of HPC in cloud
                        2. HPC Cloud Efforts: Performnace optimization
                            1. HPC-aware scheduler
                                1. topology requirements
                                2. benchmarking information which classifies the type of network requirements of app,
                                   and how it performance is affected when resources are shared
                            2. Platform selectors
                                1. environment selection impacts job performance.
                                   users may be overloaded with many infrastructure configuration choices
                                2. selection based on pre-populated information, use historical information on resource usage
                            3. Spot instance handlers.
                                1. use novel pricing models in public clouds to reduce cost
                            4. Elasticty
                                1. combines static reservation and dynamic allocation of VMs
                                2. VMs placed on same host improve performance (reminds me of pod/cell concpets)
                            5. Predictors
                                1. prediction of expected run time and wait time helps job placement and resource match
                        3. HPC Cloud Efforts: Usability
                            1. web portals; parameter sweep; workflow management; deploy; legacy-to-saas
                        4. version and challenges
                            1. see Figure 5. very good.
                               layered architecutre, with interaction roles, and modules of gap and existing
                            2. gaps
                                1. HPC-aware Modules
                                    1. Resource manager
                                    2. Cost advisor
                                    3. Large contract handler
                                    4. DevOps
                                    5. Automation APIs
                                2. General cloud modules
                                    1. Visualization and data management
                                    2. Flexible software licensing models
                                    3. Value-add cloud services

                    2. ClickNP: Highly Flexible and High Performance Network Processing with Reconfigurable Hardware    [2016, 31 refs]
                       https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/main-4.pdf
                       https://www.youtube.com/watch?v=f02IFrmQSFc
                        1. The author Bojie Li's anwser on zhihu "https://www.zhihu.com/question/24174597/answer/138717507" is good & interesting to read.
                           FPGA Network function (NF) processor. high performance.
                           Allows C-like language programmability. Modular architecture.
                           Use the PCIe channel instead of FPGA on-board DRAM to communicate with CPU
                        2. highlights
                            1. "The main challenge to use FPGA as an accelerator is programmability"
                            2. using Catapult shell + ClickNP role
                            3. c-like language is achieved by
                                1. many existing HLS tools support C
                                2. we extend C language to support element declaration
                                3. ClickNP tool-chain
                            4. PCIe IO Channel
                                1. "We extend the OpenCL runtime and add a new I/O channel, which is connected to a PCIe switch in the shell"
                                2. as mentioned by author's answer on Zhihu "https://www.zhihu.com/question/24174597/answer/138717507"
                                    1. For CPU to communicate with FPGA, we don't need to go through the DRAM on FPGA board.
                                       PCIe DMA of FPGA communicate directly with CPU reduce latency greatly, as opposed to OpenCL original
                                3. "We extend the OpenCL runtime and add a new I/O channel, which is connected to a PCIe switch in the shell.
                                    The PCIe switch will arbitrate the access between the newly added I/  channel and other components in the shell, e.g., DDR memory controller."
                                    "We leverage the PCIe slot DMA engine in Catapult shell [40], which divides a PCIe Gen2 x8 link into 64 logical subchannels, i.e., slots"
                                    "Among 64 slots, 33 are reserved by Shell and the runtime library to control kernels and access on-board DDR,
                                     one slot is used for passing signals to ClickNP elements"
                                    "The remaining 30 slots, however, are used for data communications among FPGA and CPU elements."
                                    "To amortize DMA overhead, we aggressively use batching. The maximum message size is limited at 64KB"
                            5. the pipeline parallelism, and duplicate pipeline to leverage data parallelism
                               and parallelism inside element: and minimize memory dependency in pipeline => use delayed write

                    3. Five Challenges to FPGA-Based Prototyping
                       https://www.eetimes.com/author.asp?doc_id=1324000
                        1. Design partitioning; Long time mapping design to FPGA prototype;
                           Difficult debug; Performance may not perform as expected;
                           Reusability of components and vs SoC size growth as to fit into one FPGA board

                    4. FPGA Architecture: Survey and Challenges    [2008, 438 refs]
                       http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.153.3122&rep=rep1&type=pdf
                        1. good to read. informative and complete material covers many sides of FPGA
                        2. highlights
                            1. FPGA features
                                1. flexible
                                2. significant cost in area, delay, and power consumption comapred to ASIC
                                    1. but ASIC is costly: CAD tools, mask cost of device, engineering team cost to develop ASIC taking years
                            2. history of FPGA evolve and today's main technology approach
                            3. Routing Architecture
                                1. very good section as to understand FPGA routing switches. See paper for details
                            4. FPGA gaps and alternative technologies
                                1. Technology issues: Soft Errors, Configuration Memory, User-Visible Memory, IC Process Variation, Manufacturing Defects
                                2. Emerging Architectures: Coarse-Grained FPGAs, Asynchronous FPGAs, Nanotechnology Architectures

                    5. Beyond Physical: Solving High-end FPGA Design Challenges
                       file:///D:/Chrome_Downloads/BeyondPhysical-SolvingHigh-endFPGADesignChallenges.pdf
                        1. highlights
                            1. FPGA challenges
                                1. Physical Synthesis
                                2. Managing Design Size and Complexity
                                    1. "The other big trend in FPGA design is an increasing amount of DSP content, as well as the use of embedded cores and IP blocks"
                                    2. DSP Optimization Techniques Used in FPGAs
                                        1. Pipelining, Folding, Multi-channelization, Multi-rate Folding
                                3. Addressing Low Power Consumption Demands
                                4. Debug in RTL, Not Gates
                                5. Debugging and Visibility Enhancement

                    6. Challenges of virtualization FPGA in a cloud context    [2017, 0 refs]
                       http://ieeexplore.ieee.org/abstract/document/7995321/
                        1. no original paper yet. abstract: "sensor network application"?

                    7. Cloud perspective on reconfigurable hardware    [2013, 0 refs]
                       http://www.afahc.ro/ro/revista/Nr_2_2013/23_Octavian_Mihai_MACHIDON.pdf
                        1. er ..

            5. Hadoop like job scheduler framework targeting the FPGA cloud?
                1. An FPGA-based Distributed Computing System with Power and Thermal Management Capabilities    [2011, 15 refs]
                   https://pdfs.semanticscholar.org/a36c/6991627e65d119926867c4f31c3acfb78d89.pdf
                    1. We created a multi-core distributed computing platform using "Altera Nios II Embedded Evaluation Kit (NEEK)"

                2. Distributed FPGA Solution for High-Performance Computing in the Cloud (LDA Technologies)
                   http://www.ldatech.com/2017/wp-content/uploads/2016/11/ldawhitepaper_fpga_for_cloud.pdf
                    1. N FPGAs connected by serial links to CrossPoint Fabric. So it's selling server solutions.

                3. Task Scheduling in Large-scale Distributed Systems Utilizing Partial Reconfigurable Processing Elements    [2012, 4 refs]
                   https://ce-publications.et.tudelft.nl/publications/140_task_scheduling_in_largescale_distributed_systems_utilizing.pdf
                    1. "we propose the design of a simulation framework to investigate the performance of reconfigurable processors in distributed systems"
                       "Results suggest that the average wasted area per task is less as (with partial reconfiguration) compared to the full configuration"

                4. Effective Utilization and Reconfiguration of Distributed Hardware Resources Using Job Management Systems     [2003, 10 refs]
                   ftp://cs.umanitoba.ca/pub/IPDPS03/DATA/W08_RAW_16.PDF
                    1. too old.

                5. FPGA-Accelerated Hadoop Cluster for Deep Learning Computations    [2015, 2 refs]
                   http://ieeexplore.ieee.org/document/7395718/
                    1. no original paper. abstract: exploits deep learning data parallelism in 2 ways:
                        1) by distributing deep computation into a Hadoop cluster or cloud of computing nodes, and
                        2) by using field programmable gate arrays (FPGA) hardware acceleration to speed up computationally intensive deep learning kernels
                       ... on a 6-node FPGA accelerated Hadoop cluster

                6. 如何评价微软在数据中心使用 FPGA 代替传统 CPU 的做法？ - 李博杰的回答 - 知乎
                   https://www.zhihu.com/question/24174597/answer/138717507
                    1. very good to read. sharing many insights as the author is intern from MSR
                    2. highlights
                        1. "我们即将用上的下一代 FPGA，Stratix 10，将配备更多的乘法器和硬件浮点运算部件，从而理论上可达到与现在的顶级 GPU 计算卡旗鼓相当的计算能力"
                        2. "在数据中心，FPGA 相比 GPU 的核心优势在于延迟"
                           "像 Bing 搜索排序这样的任务 ... 如果使用 GPU 来加速，要想充分利用 GPU 的计算能力，batch size 就不能太小，延迟将高达毫秒量级"
                        3. "FPGA 为什么比 GPU 的延迟低这么多？这本质上是体系结构的区别。FPGA 同时拥有流水线并行和数据并行，而 GPU 几乎只有数据并行（流水线深度受限）。"
                           "因此对流式计算的任务，FPGA 比 GPU 天生有延迟方面的优势"
                        4. "FPGA 的灵活性可以保护投资，事实上，微软现在的 FPGA 玩法与最初的设想大不相同"
                           "使用 FPGA 可以保持数据中心的同构性"
                        5. "从延迟上讲，网卡把数据包收到 CPU，CPU 再发给网卡，即使使用 DPDK 这样高性能的数据包处理框架，延迟也有 4~5 微秒"
                        6. "虽然 GPU 也可以高性能处理数据包，但 GPU 是没有网口的，意味着需要首先把数据包由网卡收上来，再让 GPU 去做处理。
                            这样吞吐量受到 CPU 和/或网卡的限制。GPU 本身的延迟就更不必说了。"
                        7. "综上，在数据中心里 FPGA 的主要优势是稳定又极低的延迟，适用于流式的计算密集型任务和通信密集型任务"
                        8. "只要规模足够大，对 FPGA 价格过高的担心将是不必要的。"
                        9. 过去的方案：专用的 FPGA 集群，里面插满了 FPGA
                            1. 不同机器的 FPGA 之间无法通信，FPGA 所能处理问题的规模受限于单台服务器上 FPGA 的数量
                            2. 数据中心里的其他机器要把任务集中发到这个机柜，构成了 in-cast，网络延迟很难做到稳定。
                            3. FPGA 专用机柜构成了单点故障，只要它一坏，谁都别想加速了；
                            4. 装 FPGA 的服务器是定制的，冷却、运维都增加了麻烦。
                        10. "FPGA 在 Bing 的部署取得了成功，Catapult 项目继续在公司内扩张"
                        11. "随着网络和存储速度越来越快，网络上了 40 Gbps，一块 SSD 的吞吐量也能到 1 GB/s，CPU 渐渐变得力不从心了"
                        12. "为了加速网络功能和存储虚拟化，微软把 FPGA 部署在网卡和交换机之间"
                            "FPGA（SmartNIC）对每个虚拟机虚拟出一块网卡，虚拟机通过 SR-IOV 直接访问这块虚拟网卡"
                            "虚拟机收发网络数据包均不需要 CPU 参与，也不需要经过物理网卡（NIC）"
                            "这样不仅节约了可用于出售的 CPU 资源，还提高了虚拟机的网络性能（25 Gbps），把同数据中心虚拟机之间的网络延迟降低了 10 倍"
                            "FPGA 复用主机网络的初心是加速网络和存储，更深远的影响则是把 FPGA 之间的网络连接扩展到了整个数据中心的规模，做成真正 cloud-scale 的「超级计算机"
                            "第三代架构中的 LTL 还支持 PFC 流控协议和 DCQCN 拥塞控制协议"
                        13. "对很多类型的应用，随着分布式 FPGA 加速器的规模扩大，其性能提升是超线性的"
                            "例如 CNN inference，当只用一块 FPGA 的时候，由于片上内存不足以放下整个模型，需要不断访问 DRAM 中的模型权重，性能瓶颈在 DRAM；
                             如果 FPGA 的数量足够多，每块 FPGA 负责模型中的一层或者一层中的若干个特征，使得模型权重完全载入片上内存，就消除了 DRAM 的性能瓶颈，完全发挥出 FPGA 计算单元的性能。"
                            "当然，拆得过细也会导致通信开销的增加。把任务拆分到分布式 FPGA 集群的关键在于平衡计算和通信。"
                        14. "在 MICRO'16 会议上，微软提出了 Hardware as a Service (HaaS) 的概念，即把硬件作为一种可调度的云服务，使得 FPGA 服务的集中调度、管理和大规模部署成为可能"
                        15. "CPU 和 FPGA 之间本来可以通过 PCIe 高效通信，为什么要到板上的 DRAM 绕一圈？也许是工程实现的问题，
                             我们发现通过 OpenCL 写 DRAM、启动 kernel、读 DRAM 一个来回，需要 1.8 毫秒。而通过 PCIe DMA 来通信，却只要 1~2 微秒。"
                            "因此我们提出了 ClickNP 网络编程框架 [5]，使用管道（channel）而非共享内存来在执行单元（element/kernel）间、执行单元和主机软件间进行通信。"
                        16. "低延迟的流式处理，需要最多的地方就是通信。然而 CPU 由于并行性的限制和操作系统的调度，做通信效率不高，延迟也不稳定。此外，通信就必然涉及到调度和仲裁"
                            "CPU 由于单核性能的局限和核间通信的低效，调度、仲裁性能受限，硬件则很适合做这种重复工作。"
                            "因此我的博士研究把 FPGA 定义为通信的「大管家」，不管是服务器跟服务器之间的通信，虚拟机跟虚拟机之间的通信，进程跟进程之间的通信，CPU 跟存储设备之间的通信，都可以用 FPGA 来加速。"
                        17. "成也萧何，败也萧何。缺少指令同时是 FPGA 的优势和软肋。每做一点不同的事情，就要占用一定的 FPGA 逻辑资源。
                             如果要做的事情复杂、重复性不强，就会占用大量的逻辑资源，其中的大部分处于闲置状态。"
                             "数据中心里的很多任务有很强的局部性和重复性：一部分是虚拟化平台需要做的网络和存储，这些都属于通信；另一部分是客户计算任务里的，比如机器学习、加密解密。"
                    3. as for challenges of FPGA
                        1. programming on FPGA is hard. transform RTL to real circuit design is hard. software developers to work on FPGA is hard, where needs hardware programming
                        2. mostly we are comparing FPGA with GPU/CPU/ASIC. But actually FPGA is more suitable to low latency (~ 1us) stream processing
                           while GPU is more suitable for higher latency (> 1ms) batch data processing.
                           FPGA has both data parallel and command pipeline, while GPU has only data parallel.
                           and, since logic occupies circuit area on FPGA, FPGA is not suitable to program very complex commands
                    4. questions
                        1. looks like, though FPGA is vastly used in MS Bing search & rank and Azure SDN, providing public cloud FPGA VM instance is not addressed yet.
                           and even more, how to allow public cloud users to use the cloud-scale FPGA acceleration infrastructure?
                    n. related materials
                        1. Communicating sequential processes
                           https://en.wikipedia.org/wiki/Communicating_sequential_processes
                            1. "CSP was highly influential in the design of the occam programming language"
                        2. ClickNP: Highly Flexible and High Performance Network Processing with Reconfigurable Hardware    [2016, 31 refs]
                           https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/main-4.pdf
                            1. logged before
                        
                        3. Can FPGAs Beat GPUs in Accelerating Next-Generation Deep Learning?
                           https://www.nextplatform.com/2017/03/21/can-fpgas-beat-gpus-accelerating-next-generation-deep-learning/
                            1. highlights
                                1. Changes making FPGA a viable future
                                    1. While FPGAs provide superior energy efficiency (Performance/Watt) compared to high-end GPUs,
                                       they are not known for offering top peak floating-point performance
                                    2. Intel FPGAs offer a comprehensive software ecosystem that ranges from low level Hardware Description languages
                                       to higher level software development environments with OpenCL, C, and C++
                                    3. DNN Algorithms: the trends have shifted towards more efficient DNNs
                                        1. An emerging trend is adoption of compact low precision data types, much less than 32-bits. 16-bit and 8-bit data types are becoming the new norm
                                        2. continued accuracy improvements for extremely low precision 2-bit ternary and 1-bit binary DNNs, where values are constraints to (0,+1,-1) or (+1,-1)
                                        3. Another emerging trend introduces sparsity (the presence of zeros) in DNN neurons and weights
                                           by techniques such as pruning, ReLU, and ternarization, which can lead to DNNs with ~50% to ~90% zeros
                                2. case studies and FPGA vs GPU performance number charts
                        
                        4. CUDA vs FPGA? - asked on Stackoverflow
                           https://stackoverflow.com/questions/317731/cuda-vs-fpga
                            1. answer 1
                                1. "FPGAs are great for realtime systems, where even 1ms of delay might be too long"
                                2. "FPGAs can be very fast, espeically for well-defined digital signal processing usages (e.g. radar data)
                                    but the good ones are much more expensive and specialised than even professional GPGPUs"
                                3. "FPGAs are quite cumbersome to programme. Since there is a hardware configuration component to compiling, it could take hours"
                            2. answer 2
                                1. "One thing where CUDA shines if you can realy formulate your problem in a SIMD fashion AND can access the memory coalesced"
                                2. "If the memory accesses are not coalesced(1) or if you have different control flow in different threads
                                    the GPU can lose drastically its performance and the FPGA can outperform it"
                                3. if you have huge amount of small operations, but you cannot wrap them in a loop in one kernel,
                                   then your invocation times for the GPU kernel exceeds the computation time
                                4. "Also the power of the FPGA could be better (depends on your application scenarion,
                                    ie. the GPU is only cheaper (in terms of Watts/Flop) when its computing all the time)"
                                5. "Offcourse the FPGA has also some drawbacks:
                                        IO can be one (we had here an application were we needed 70 GB/s, no problem for GPU,
                                        but to get this amount of data into a FPGA you need for conventional design more pins than available).
                                        Another drawback is the time and money. A FPGA is much more expensive than the best GPU and the development times are very high."

                        5. FPGA or GPU? - The evolution continues
                           http://mil-embedded.com/articles/fpga-gpu-evolution-continues/
                            1. "GPUs historically have been power hogs", "but the latest GPU products have reduced that liability"
                            2. "Unlike FPGAs, GPUs run software, and executing an algorithm in software takes time"
                               "GPUs’ massively parallel construction enables them to run a software algorithm much faster than a conventional processor could"
                            3. "Unlike FPGAs, GPUs excel in floating-point operations"
                            4. "In fact, many newer signal-processing algorithms are aimed at GPUs.
                                Moreover, GPUs are designed with very fast memory,
                                and new direct memory access (DMA) techniques allow high-volume sensor data to be streamed to the GPU without consuming GPU clock cycles."
                            5. "GPUs also offer good backward compatibility"
                               "It’s no small matter to upgrade the algorithm on an FPGA or to move an algorithm to a newer FPGA"
                               "GPUs, furthermore, are supported with a wide array of open development tools and free math function libraries."
                            6. "GPUs are increasingly found in radar processing"

            6. FPGA cloud usage on DNN, deep learning area?
                1. DLAU: A Scalable Deep Learning Accelerator Unit on FPGA
                   https://arxiv.org/pdf/1605.06894.pdf
                    1. mostly FPGA chip designs

            7. FPGA usage on key-value stores and stoarge and in-memory storage?
                1. Impact of Cache Architecture on FPGA-Based Processor/Parallel-Accelerator Systems    [2012, 43 refs]
                   https://www.youtube.com/watch?v=vfuPD0WWmSs
                    1. it's about the "Cache Architecture" on a "Processor/Parallel-Accelerator Systems"
                       i.e. multiple FPGAs connected with CPU, with an on-chip data cache, the designs

                2. An FPGA-based In-line Accelerator for Memcached    [2014, 50 refs]
                   http://www.cs.princeton.edu/courses/archive/spring16/cos598F/06560058.pdf
                   https://www.hotchips.org/wp-content/uploads/hc_archives/hc25/HC25.50-FPGA-epub/HC25.27.530-Memcached-Lavasani-UTexas.pdf
                    1. highlights
                        1. FPGA process network packets bypassing CPU
                           The CPU cores and FPGA all connects to the same shared memory (coherent memory system)
                            1. evaluation is done by simulation (the gem5 simulator)
                        2. profile the application to determine the hottest code paths, and extract them to FPGA
                           if execution cannot be fully satisfied on FPGA, we rollback to CPU
                        3. achieves ~2x energy efficiency compared to CPU only in the same throughput

                3. devicepros: HW Acceleration of Memcached
                   https://www.flashmemorysummit.com/English/Collaterals/Proceedings/2014/20140805_B12_Sturgeon.pdf
                    1. highlights
                        1. "Network not saturated for small Object sizes"
                        2. FPGA and KV store resides on NIC end. Access DRAM through PCIe.
                           Memcached logic is entirely built in FPGA
                        3. results
                            1. 7K queries / Watt vs. 100-200 queries / Watt
                            2. Significantly better max latency and distribution

                4. Achieving 10Gbps line-rate key-value stores with FPGAs    [2013, 51 refs]
                   https://www.usenix.org/system/files/conference/hotcloud13/hotcloud13-blott.pdf
                   https://www.usenix.org/sites/default/files/conference/protected-files/blott_hotcloud13_slides.pdf
                    1. highlights
                        1. "fully pipelined dataflow architecture"
                        2. "Scalability in throughput is achieved by widening or duplication of the data path"
                        3. modular design: each stage in the pipeline provides identical input and output interface formats, based on AXI-4 streaming protocol,
                                           and standardize how key, value, and meta-data, are conveyed between macro-level pipeline stages
                        4. "Collision handling is in software solutions typically solved by chaining a flexible number of keys to a single hash table index.
                           In hardware, collision handling is often supported  hrough a parallel lookup [3] of a fixed number of keys that map to the same hash table index"
                            1. [9] Hash Table for Large Key-Value Stores on FPGAs

                5. question: the FPGA are mostly handling in-memory storage. can FPGA offload disk/SSD access?
                             if we cannot use FPGA to accelerate disk/SSD access, then the usage on persistent storage would be limited to compression/crypto/etc, non-architecture shifting
                             NVDIMM with PCIe DMA by FPGA may be another way to use FPGA with Persistent Flash.
                             But disk handling and journaling usually consists of the majority of storage logic code and error handling, which is complex and favors CPU I think
                    1. FPGA Drive
                       https://fpgadrive.com/
                    2. FPGA to SSD via PCIe
                       https://forums.xilinx.com/t5/Zynq-All-Programmable-SoC/FPGA-to-SSD-via-PCIe/td-p/686622
                    3. Interfacing FPGA and a storage device
                       https://electronics.stackexchange.com/questions/129708/interfacing-fpga-and-a-storage-device
                    4. SSD SATA 3.0 Host Controller 1.5/3/6Gbit/s for Xilinx FPGA
                       http://chevintechnology.com/wp-content/uploads/2015/11/ProductBrief_SATA-HC_xilinx_v1.0.pdf
```
