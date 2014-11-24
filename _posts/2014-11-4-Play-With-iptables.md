---
layout: post
title: "Play with iptables"
tagline : "Play with iptables"
description: "Play with iptables"
category: "network"
tags: [network, routing, iptables]
---
{% include JB/setup %}

## Brief

Following 

* Manual: <http://drops.wooyun.org/tips/1424>
* Tutorial: <http://articles.slicehost.com/2011/2/21/introducing-iptables-part-1>

On default iptables consists raw->mangle->nat->filter, 4 tables. Each table contains several 'chains'. Each chain contains a sequence of 'rules'. Common use for 'iptables --list' below.

```
$ iptables -L -n --line-numbers # you can add -t <table-name> (default table is FILTER)
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
REJECT     all  --  0.0.0.0/0            127.0.0.0/8         reject-with icmp-port-unreachable 
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           
ACCEPT     icmp --  0.0.0.0/0            0.0.0.0/0           icmp type 8 
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:30000 
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:443 
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           tcp dpt:80 
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           state RELATED,ESTABLISHED 
LOG        all  --  0.0.0.0/0            0.0.0.0/0           limit: avg 5/min burst 5 LOG flags 0 level 7 prefix `iptables denied: ' 
REJECT     all  --  0.0.0.0/0            0.0.0.0/0           reject-with icmp-port-unreachable 

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
REJECT     all  --  0.0.0.0/0            0.0.0.0/0           reject-with icmp-port-unreachable 

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0  
```

The last field, which has no column name, is introduced by '-m' option. It can be seen as an argument for prior action. E.g

```
iptables -A INPUT -i eth0 -p tcp -m tcp --dport 30000 -j ACCEPT
```

For what '-m' options can be used and what can be filled in the last unamed field, refer to "隐士扩展" and "显示扩展" in <http://drops.wooyun.org/tips/1424>.

## Deeper iptables

Linux iptables is a very powerful tool which can be used to create routers and firewalls. If you dive into [netfilter](http://www.netfilter.org/) in kernel, which implements iptables, much more can be found. For example, how can the format and arrangement of rules impach kernel performance.

Iptables can create more tables and jump between them in rules. This feature is called [Linux advanced routing](http://www.lartc.org/LARTC-zh_CN.GB2312.pdf). It can be used, for example, to build a router that connects both to [China Telecom](http://baike.baidu.com/view/91684.htm) and [China Unicom](http://baike.baidu.com/view/2131714.htm) and use different routing strategy for each of their packets.

## V.S. Routing Table

Routing table and iptables are different, refer to [here](http://superuser.com/questions/419659/iptables-vs-route).

* Routing table, aka "Forwarding Information Base", can be displayed using `route`.  IP forwarding, i.e. routing, basically rewrites a packet with a different source address, and ships it out of a different network interface.
* The `iptables` manipulate on Netfilter, the Linux kernel's packet filtering and manipulating subsystem. It handles NAT.

Technically, one can do static routing with the proper iptables rules in the `mangle` table. But that would be generally slower.

There are many diagrams illustrate how a TCP/IP packet traverses the kernel. One example from [here](http://www.adminsehow.com/2011/09/iptables-packet-traverse-map/), including Netfilter and routing.

![iptables packet traverse map 1](/images/iptables-packet-traverse-map-1.jpg "iptables packet traverse map 1")

---

![iptables packet traverse map 2](/images/iptables-packet-traverse-map-2.png "iptables packet traverse map 1")

---

![iptables packet traverse map 3](/images/iptables-packet-traverse-map-3.png "iptables packet traverse map 1")

Also, there is an `ebtables` filtering on layer 2, compared with `iptables` working on layer 3.

