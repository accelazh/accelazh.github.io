---
layout: post
title: "Cloud Storage Cost Study"
tagline : "Cloud Storage Cost Study"
description: "Cloud Storage Cost Study"
category: "storage"
tags: [storage, cloud, cost]
---
{% include JB/setup %}

Raw notes only.

```
1. public cloud pricing study
    1. AWS pricing
        1. "There are four ways to pay for Amazon EC2 instances: On-Demand, Reserved Instances, and Spot Instances" "You can also pay for Dedicated Hosts"
        2. EC2 pricing: https://aws.amazon.com/ec2/pricing/
            1. on-demond: t2.xlarge 4core16GBmem $0.1856/hrs
            2. reserved: t2.xlarge $83.95/month
        3. EBS pricing: https://aws.amazon.com/ebs/pricing/
            1. Throughput optimized HDD: $0.045/GB/month
        4. S3 pricing: https://aws.amazon.com/s3/pricing/
            1. US East: First 50TB/month: standard storage: $0.023/GB/Month
            2. Request pricing: US East: GET 0.004/10,000req PUT 0.005/1,000req
    2. Azure pricing
        1. Blob storage pricing: https://azure.microsoft.com/en-us/pricing/details/storage/blobs/
            1. LRS: East US 2: First 50TB $0.0184/GB/month
            2. operations and data transfer: hot write $0.05/10,000op, hot read $0.004/10,000op
        2. Disks pricing: https://azure.microsoft.com/en-us/pricing/details/storage/
            1. Managed Disk: HDD: S30 1TB: $40.96.
            2. transactions: $0.0005/10,000tx
    3. Aliyun pricing
        1. ECS instances: https://cn.aliyun.com/price/product#/ecs/detail
            1. ecs.g5.xlarge 4core16GBmem 513CYN/month
        2. Block storage: https://cn.aliyun.com/price/product?spm=5176.8030368.333906.7.59075fee9YuhOC#/disk/detail
            1. data disk: 0.28CYN/GB/Month
        3. Object storage （OSS): https://cn.aliyun.com/price/product?spm=5176.8030368.333906.4.59075fee9YuhOC#/oss/detail
            1. standard: 0.148CYN/GB/month
            2. requests: 0.01CYN/10,000req
    4. P.S. I don't see cost advantage from Aliyun over Azure or AWS

2. hardware prices by CapEx and OpEx
    1. Amazon hardware prices
        1. 1TB HDD: $164
        2. 4 * 16GB DRAM: $715
        3. Intel CPU Xeon E5-2630: $764
        4. NVIDIA Tesla K40 GPU: $2799
           NVIDIA TITAN Xp: $1499
        5. FPGA: ~$100
        6. (RDMA) Mellanox ConnectX-4: $217
        7. Samsung 960 EVO Series - 250GB PCIe NVMe: $128
           Samsung 960 PRO Series - 512GB PCIe NVMe: $307
           Optane SSD 900P 280GB: $388
           Intel SSD 750 Series PCIe AIC 1.2TB Internal SSD: $1150
           Intel SSD 600p Series (1.0TB, M.2 80mm PCIe 3.0 x4, 3D1, TLC): $424
    2. server power consumption
        1. ~850watt/hrs: http://www.zdnet.com/article/toolkit-calculate-datacenter-server-power-usage/
        2. server power calculator: https://networking.ringofsaturn.com/Tools/serverpowerusage.php
            1. 300servers * $0.0808/kwh ~= $15040/month
    3. rough cost estimate: 300 servers each with 1TB disk
        1. $income/month: 500servers * 60disks * 1000GB * $0.0184/GB/month ~= $550k/month
           $power/month: 500servers * 850w * 0.001k * $0.2/kwh * 720hrs/month ~= $61k/month
           $hardware/month: 500servers * (60disks * 164 + 1dram * 715 + 2cpu * 764 + 100) * 3whatever / (3 * 12) ~= $510k
        2. looks like public cloud storage can make some money. the cost is close.
           that requires high density disks. high util efficiency. careful cost management.

3. costs analysis in papers/talks
    1. Pergamum: Replacing Tape with Energy Efficient, Reliable, Disk-Based Archival Storage
       https://www.usenix.org/legacy/events/fast08/tech/full_papers/storer/storer.pdf
        1. section "5.1 cost", and table 3 archival storage media prices
    2. No compromises: distributed transactions with consistency, availability, and performance
       http://dl.acm.org/ft_gateway.cfm?id=2815425&type=pdf
        1. dram cost / GB, UPS cost / Joule, energy cost / GB, capcity cost / GB
    3. A Quick Summary of Energy-aware Cloud Computing
       http://accelazh.github.io/cloud/A-Quick-Summary-of-Energy-Aware-Cloud-Computing
        1. power & cooling contributs > 70% to OpEx
    4. A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services
       http://www.nallatech.com/wp-content/uploads/ISCA14-Catapult.pdf
        1. section "2 catapult hardware" TCO increase < 30% including < 10% of power
    5. The Cost of Cloud Storage
       https://www.backblaze.com/blog/cost-of-cloud-storage/
       Cloud infrastructure Economics: Cogs and operating costs
       https://24x7x0.wordpress.com/2014/02/28/cloud-infrastructure-economics-cogs-and-operating-costs/
        1. profitability, sellable capacity, per GB COGS
        2. highend hardwares are more expensive, but provide more consolidated IOPS/latency/capacity to sell.
           and use more power usually, the total price may drop however we cannot say
    6. Ceph OSD Hardware - A Pragmatic Guide
       https://www.youtube.com/watch?v=kc7GIHyk57M&feature=youtu.be&t=34m49s
        1. price setup when choosing Ceph cluster setup
        2. under-utilized hardware wastes money
    7. AWS vs Azure vs Google Cloud vs IBM Cloud 全方位价格比较
       https://mp.weixin.qq.com/s/XNTEwvQljXkwzF0Df76HMA
    8. Ceph冷知识 | Cache Tier 的抉择与使用
       https://mp.weixin.qq.com/s/w39cEMBtV8bCI1k_2PR2vA
        1. For the same IOPS target, w./wo. SSD cache layer, hit rate, reduced HDD cluster size or not

4. OVH: Can OpenStack Beat Amazon AWS in Price? Series
   https://www.youtube.com/watch?v=To6iTnyb_fc
   https://www.youtube.com/watch?v=0FXbeA-zI0M
   https://www.youtube.com/watch?v=8bkeOg4tSW4
    0. compared to AWS, OVH openstack saves dev/software cost, large-scale XX cost
    1. the OpEx calculation datasheet: http://accelazh.github.io/images/can-openstack-beat-aws-in-price.zip (best resource)
    2. price decomposition
        1. hardware
            1. networking
                1. spine switches
                2. leaf switches
                3. management switches
            2. server nodes
                1. controller nodes
                2. network nodes
                3. compute nodes
                4. block storage nodes
                    1. Server platform (e.g. 1U Dual Xeon Intel Server Platform, 8 x 2.5" HDDs, Dual PSU)
                    2. Power supply unit (PSU) (e.g. 2nd 1000W PSU for R2312WTTYS server)
                    3. Premium Rail Kit
                    4. CPU (e.g. Intel Xeon E5-2620V4 2.10GHz 20MB LGA2011-3 8C/16T)
                    5. DIMM (e.g. Intel Certified 16GBDDR4 2133MHz ECC Reg DIMM)
                    6. RAID controller (e,g, LSI MegaRAID SAS 9361-8i SGL RAID Controller)
                    7. Flash cache (e.g. LSI CacheVault Flash Module LSICVM02)
                    8. PCI card (e.g. Intel 12Gb/s RES3FV288 RAID Expander LP PCI Card)
                    9. NIC (e.g. Intel Ethernet X540-T2 Dual 10-Gb PCIe x8 Card)
                    10. disks (e.g. 400GB Intel SSD DCP3700 series PCIe SATA HDD 2.5"
                                    1TB Seagate Constellation SATA 7200rpm HDD 2.5"
                                    4TB Seagate Constellation SATA 7200rpm HDD 3.5")
                5. object storage nodes
        2. rack units
            1. cost per month for a rack
            2. number of rack units available on a rack
        3. power
            1. raw cost for power per kW/h
            2. PUE ratio of the data center
        4. staff
            1. team size, FTE 8*5
            2. operation on-duty 24*7
```

![Example OpEx & CapEx Decomposition Sheet](/images/can-openstack-beat-aws-in-price-2017-cheetsheet.png "Example OpEx & CapEx Decomposition Sheet")
