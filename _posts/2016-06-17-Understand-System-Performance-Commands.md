---
layout: post
title: "Understand System Performance Commands"
tagline : "Understand System Performance Commands"
description: "Understand System Performance Commands"
category: "Linux"
tags: [Linux, shell, performance]
---
{% include JB/setup %}

There are tons of system monitoring commands in Linux which are handy for collecting system statistics and performance troubleshooting. Here are the most impressive tutorials I found

  * [Linux Performance Analysis in 60,000 Milliseconds](http://techblog.netflix.com/2015/11/linux-performance-analysis-in-60s.html) by Netflix.
  * [Netflix at Velocity 2015: Linux Performance Tools](http://techblog.netflix.com/2015/08/netflix-at-velocity-2015-linux.html). Check the part-1 & part-2 talk on Youtube. They are inspiring.        

**Understand `top`**

Type `top` show CPU monitoring per second. Type `1` to show per core.

  * us: user cpu time (or) % CPU time spent in user space
  * sy: system cpu time (or) % CPU time spent in kernel space
  * ni: user nice cpu time (or) % CPU time spent on low priority processes
  * id: idle cpu time (or) % CPU time spent idle
  * wa: io wait cpu time (or) % CPU time spent in wait (on disk)
  * hi: hardware irq (or) % CPU time spent servicing/handling hardware interrupts
  * si: software irq (or) % CPU time spent servicing/handling software interrupts
  * st: steal time - - % CPU time in involuntary wait by virtual cpu while hypervisor is servicing another processor (or) % CPU time stolen from a virtual machine

Extracted from [its_me's ask on stackexchange](http://unix.stackexchange.com/questions/18918/in-linux-top-command-what-are-us-sy-ni-id-wa-hi-si-and-st-for-cpu-usage).

**Understand `iostat`**

Type `iostat -x -d 1` to disk IO monitoring. It rolling print to shell per second.

CPU status

  * %user: The percentage of CPU utilization that occurred while executing at the user level (this is the application usage).
  * %nice: The percentage of CPU utilization that occurred while executing at the user level with nice priority.
  * %system: The percentage of CPU utilization that occurred while executing at the system level (kernel).
  * %iowait: The percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request.
  * %steal: The percentage of time spent in involuntary wait by the virtual CPU or CPUs while the hypervisor was servicing another virtual processor.
  * %idle: The percentage of time that the CPU or CPUs were idle and the systems did not have an outstanding disk I/O request.

Device status

  * rrqm/s: The number of read requests merged per second queued to the device.
  * wrqm/s: The number of write requests merged per second queued to the device.
  * r/s: The number of read requests issued to the device per second.
  * w/s: The number of write requests issued to the device per second.
  * rMB/s: The number of megabytes read from the device per second. (I chose to used MB/s for the output.)
  * wMB/s: The number of megabytes written to the device per second. (I chose to use MB/s for the output.)
  * avgrq-sz: The average size (in sectors) of the requests issued to the device.
  * avgqu-sz: The average queue length of the requests issued to the device.
  * await: The average time (milliseconds) for I/O requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them.
  * r_await: The average time (in milliseconds) for read requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them.
  * w_await: The average time (in milliseconds) for write requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them.
  * svctm: The average service time (in milliseconds) for I/O requests issued to the device. Warning! Do not trust this field; it will be removed in a future version of sysstat.
  * %util: Percentage of CPU time during which I/O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs when this values is close to 100%.

Extracted from [Jeff Layton's Monitoring Storage Devices with iostat](http://www.admin-magazine.com/HPC/Articles/Monitoring-Storage-with-iostat).

**Other commands**

  * Type `mpstat -P ALL 1` to show CPU per core statistics rolling print per second
  * Type `sar -d 1` to show disk IO statistics rolling print per second. It uses "major:minor" number rather than device name.