---
layout: post
title: "Summarizing Production Server Failure Modes"
tagline : "Summarizing Production Server Failure Modes"
description: "Summarizing Production Server Failure Modes"
category: "failure"
tags: [failure, production, disk]
---
{% include JB/setup %}

Common server errors that I managed to find in [kubernetes maillist](https://groups.google.com/forum/#!forum/google-containers) (possible not very related to production OPs since many are asking beginner questions):

  * Misconfiguration or mis-setup; version mismatch; software bug
  * Service failed to start. service outputs error in log. service status fail. command outputs fail.
  * Network down. Network unable to connected. Firewall issue.
  * Process dies (especially the proxy process).
  * Network or something misconfiguration.
  * Process/service becomes non-responsive
  * Anybody reporting disk degradation/corruption error?

Kubernetes has a [HA doc](https://github.com/GoogleCloudPlatform/kubernetes/blob/37f0368ba26f5f503df2407f3241a3ad62cc8e59/docs/availability.md), which happens to have summarized some common failure modes:

  * VM(s) shutdown
  * Network partition within cluster, or between cluster and users.
  * Crashes in Kubernetes software
  * Data loss or unavailability of persistent storage (e.g. GCE PD or AWS EBS volume).
  * Operator error misconfigures kubernetes software or application software.

I also checked [openstack-operator maillist](https://wiki.openstack.org/wiki/Mailing_Lists#Operators) for more failure modes

  * Unexpected cpu/disk high usage.
  * Dhcp down / unable to acquire ip address
  * An operation (usually VM spawning) forever

Something in common linux failures

  * Read-only file system error (i.e. FS corrupt, or no free space)    
  * Kernel panic
  * Kernel softlockup / hardlockup

[This paper](http://www.pdl.cmu.edu/PDL-FTP/Failure/CMU-PDL-06-111.pdf) gives a relative frequency chart of hardware failures that need replacement. 1 high-performance computing cluster (HP1) and 2 internet service providers (COM1, COM2)

![LVM concept layout](/images/relative-frequency-of-hardware-failures-that-require-replacement.png "Relative frequency of hardware failures that require replacement")

[Disk failures in the real world: What does an MTTF of 1,000,000 hours mean to you?](http://www.pdl.cmu.edu/PDL-FTP/Failure/CMU-PDL-06-111.pdf) shows that 

  * Disk failures exhibit significant levels of autocorrelation in time (failures follow failures in time)

[RAIDShield: Characterizing, Monitoring, and Proactively Protecting Against Disk Failures](https://www.usenix.org/system/files/conference/fast15/fast15-paper-ma.pdf) reveals that

  * Reallocated sectors correlates strongly with impending disk failures
  * Many disks fail at a similar age
  * Accumulation of sector errors contributes to the whole-disk failure, causing disk reliability to deteriorate continuously, and eventually fail shortly or suffer a larger burst of sector errors. (RS can be observed)

We can download public computer failure datasets at

  * [Google - ClusterData2011](https://github.com/google/cluster-data/blob/master/ClusterData2011_2.md)
  * [The Computer Failure Data Repository (CFDR)](https://www.usenix.org/cfdr)

