---
layout: post
title: "A Quick Summary of Energy-aware Cloud Computing"
tagline : "A Quick Summary of Energy-aware Cloud Computing"
description: "A Quick Summary of Energy-aware Cloud Computing"
category: "cloud"
tags: [cloud, energy, summary]
---
{% include JB/setup %}

A quick summary of current energy-aware cloud computing technologies here. 

### Cost of Energy Consumption

[\[5\]]() gives an overview of the energy cost in datacenters. The data comes from Amazon.com's estimates [9]. Servers cost 53%. Power related costs contribute 42% of the total, in which 19% for direct server power, and 23% for infrastructure cooling & power.

![Energy Costs in Datacenter](/images/energy-costs-in-datacenter.png "Energy Costs in Datacenter")

So, for cloud computing and datacenter operations, you save power, you save money. Besides, it protects the earth.

### Power Consumption Model

The first thing necessary about energy-awareness is the energy consumption model. They are usually seen in each paper when the author starts to discuss something. [\[3\]]() shows a popular energy consumption model, which is a linear sum of computer resource utilizations (Ux,y). The model needs the user to calibrate its coefficients (Cx,y) first. The model is basically the same with [\[1\]](), which has 280+ references. Though simple, [\[2\]]() gives an evaluation and shows that the model yields less than 9% error. See below

![Linear Model of Power Consumption](/images/linear-model-of-power-consumption.png "Linear Model of Power Consumption")

[\[7\]]() shows that in average an idle server consumes approximately 70% of the power consumed by the server running at full CPU speed; and compared to other system resources, CPU consumes larger amount of energy. [\[2\]]() shows that CPU is the dominate power consumer of the dynamic part of overall energy consumption, and CPU is usually considered a first-order proxy for dynamic power consumption.

Energy consumption per transaction, however, is not linear. [\[6\]]() shows that it reaches bottom when (CPU, disk) utilization is about (70%, 50%) in their experiment. See below picture

![Energy Consumption per Transaction](/images/energy-consumption-per-transaction.png "Energy Consumption per Transaction")

### The Overall Status

[\[5\]]() gives the perfect summary.

Energy-efficient hardware has been researched for long time. Processor can be powered down. Energy-aware scheduling contributes to a large part. With respect to wireless network, energy-saving routing protocols are studied.

The cloud part is mostly about server consolidation. The challenge is to achieve an "optimal balance between performance, QoS, and energy consumption and include self-aware runtime adaptation".

Besides, [\[1\]]() reveals some applications such that, dynamically control the fans according current energy consumption, predict the thermal map in a datacenter and allow the cooling system to cool much or less in different spot, calculate the power budget which may be used in scheduling or planning, etc.

### Cloud Consolidation

Energy-awareness related to Cloud is almost all about consolidation, AFAIK. Since an idle server needs up to even 70% of their maximum power consumption, server consolidation matters. However consolidation usually needs to cope well with SLA.

The Green Cloud [\[7\]]()[\[8\]]() is a highly referenced architecture (800+ references), which takes care of both energy consumption and application SLA. The basic idea is to set upper and lower CPU utilization thresholds for hosts, and keep the total utilization of the CPU (by all the VMs allocated to the host) between these thresholds.

  * VMs are migrated from host, if the utilization of CPU is too low. This to consolidate idle hosts.
  * VMs are migrated from host, if the CPU utilization are too high. This is to avoid SLA violation.

There are three different policies to select VMs for migration, when the CPU utilization exceeds the upper threshold.

  * The minimization of migrations policy. It tries to ensure the number of VMs selected is minimum, and upper CPU utilization threshold is maintained.
  * The highest potential growth policy. It tries to first select VMs who have the lowest CPU usage, because they have greater potential to grow.
  * The random choice policy. It select VMs randomly.

Besides, [\[6\]]() shows energy consumption per transaction reaches bottom, when (CPU, disk) utilization is about (70%, 50%) in their experiment. They propose the framework to schedule VMs and make servers close to their optimal utilization, where energy consumption per transaction is the lowest.

### Datacenter Design

The major operational expense of a datacenter is power. Energy efficiency is very important in datacenter design. Below is the fomula [\[10\]]() (page 67)

![Datacenter Energy Efficiency Fomula](/images/datacenter-energy-efficiency-formula.png "Datacenter Energy Efficiency Fomula")

PUE = (Facility power) / (IT Equipment power). It reflects how efficient is the data center facility to transfer external energy to the IT devices. SPUE = server PUE. It is PUE inside the server, i.e. how efficient the server can transfer total input power to its useful electronic computation components.

General steps to improve PUE can be summarized as following [\[10\]]() (page 71).

  * Careful air flow handling:  segregate hot air exhausted by servers from cold air, and keep the path to the cooling coil short so that little energy is spent moving cold or hot air long distances.

  * Elevated temperatures: keep the cold aisle at 25-30°C rather than 18–20°C.

  * Free cooling: use cool air or water from external environment to make the cooling system economicized.

  * Better power system architecture: UPS and power distribution losses can often be greatly reduced by selecting higher-efficiency gear, and redesign the path. See pictures below [\[10\]]() (page 52). Power delivery architecture may greatly impact PUE.

![Datacenter Power Delivery Designs](/images/datacenter-ups-path-designs.png "Datacenter Power Delivery Designs")

PUE * SPUE = TPUE (True PUE). Based on the state of the art in 2013, an annual TPUE of 1.25 probably represents the upper limit of what is economically feasible in real-world settings [\[10\]]() (page 73).

With respect to the power efficiency of computing, a key feature is: under low levels of utilization, computing systems tend to be significantly more ineffcient than when they are exercised at maximum utilization [\[10\]]() (page 73). This is usually why we need cloud consolidation.

Energy-proportional computing is a different approach [\[10\]]() (page 76), where energy-consumption of computer hardware should be proportional to its utilization. Though some progress, it is still under-research now. But if it comes true, cloud consolidation is not really needed any more, since low utilization yields low energy consumption in proportion.

### Other Software Techniques

[\[3\]]() proposes a energy-saving network data transfer method, by tuning TCP parameters pipeling, parallelism, concurrency, to their best. [\[4\]]() gives algorithm to save energy in cache management. Basically in each component of the software path, you can find some energy-saving embodiments. Search more in Google Scholar.

### References

* \[1\] [Full-System Power Analysis and Modeling for Server Environments](http://www-mount.ece.umn.edu/~jjyi/MoBS/2006/program/3A-Economou.pdf) \[287 references, 2006\]
* \[2\] [A Comparison of High-Level Full-System Power Models](https://www.usenix.org/legacy/event/hotpower08/tech/full_papers/rivoire/rivoire_html/) \[209 references, 2008\]
* \[3\] [Energy-Aware Data Transfer Algorithms](http://www.cse.buffalo.edu/faculty/tkosar/papers/sc_2015.pdf) \[no reference yet, 2015\]
* \[4\] [Reducing Energy Consumption of Disk Storage Using Power-Aware Cache Management](http://opera.ucsd.edu/paper/HPCA04.pdf) \[246 references, 2004\]
* \[5\] [Energy-Efficient Cloud Computing](http://san.ee.imperial.ac.uk/publications/EfficientCloud.pdf) \[504 references, 2010\]
* \[6\] [Energy Aware Consolidation for Cloud Computing](https://www.usenix.org/legacy/events/hotpower08/tech/full_papers/srikantaiah/srikantaiah_html/main.html) \[551 references, 2008\]
* \[7\] [Energy-Efficient Management of Data Center Resources for Cloud Computing: A Vision, Architectural Elements, and Open Challenges](http://128.250.22.134/papers/GreenCloud2010.pdf) \[333 references, 2010\]
* \[8\] [Energy-aware resource allocation heuristics for efficient management of data centers for Cloud computing](http://www.cloudbus.org/papers/Energy-Aware-CloudResourceAllocation-FGCS2012.pdf) \[838 references, 2012\]
* \[9\] [Cooperative Expendable Micro-Slice Servers (CEMS): Low Cost, Low Power Servers for Internet-Scale Services](http://www-db.cs.wisc.edu/cidr/cidr2009/JamesHamilton_CEMS.pdf) \[195 references, 2009\]
* \[10\] [The Datacenter as a Computer: An Introduction to the Design of Warehouse-Scale Machines, Second Edition](https://cseweb.ucsd.edu/classes/wi14/cse141/pdf/10/18_Synthesis_Lecture_Data_Center_2.pdf) \[1184 references, 2013\]
