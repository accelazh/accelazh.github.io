---
layout: post
title: "Haproxy HA by Keepalived VRRP"
tagline : " Haproxy HA by Keepalived VRRP"
description: "Make Haproxy HA by using keepalived VRRP"
category: "Loadbalance"
tags: [haproxy, HA, keepalived, VRRP]
---
{% include JB/setup %}

Keepalived can be used to achieve Haproxy HA using VRRP (Virtual Router Redundancy Protocol) protocol. Two Haproxies play master and backup and share a vip.

## Environment

*Host 1*

    10.224.147.166
    CentOS 7
    role: haproxy master

*Host 2*

    10.224.147.167
    CentOS 7
    role: haproxy backup

*Host 3*

    10.224.147.154
    CentOS 6.3
    role: httpd server

## Install and Configure Haproxy

On Host 1, install haproxy by

```
yum intall haproxy
```

Configure /etc/haproxy/haproxy.cfg

```
global
    log         127.0.0.1 local2

    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon
    
    stats socket /var/lib/haproxy/stats

defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    option http-server-close
    option forwardfor       except 127.0.0.0/8
    option                  redispatch
    retries                 3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout http-keep-alive 10s
    timeout check           10s
    maxconn                 3000

frontend  main *:5000
    acl url_static       path_beg       -i /static /images /javascript /stylesheets
    acl url_static       path_end       -i .jpg .gif .png .css .js

    use_backend static          if url_static
    default_backend             app

backend static
    balance     roundrobin
    server      static 10.224.147.154:80 check

backend app
    balance     roundrobin
    server      app1 10.224.147.154:80 check
```

On host 2, do the same.

## Install and Config Keepalived

First, make sure each host can login each other with passwordless ssh (public key).

On host 1 and host 2, both install keepalived

```
yum install keepalived
chkconfig keepalived on

# tell kernal to allow binding non-local IP
echo "net.ipv4.ip_nonlocal_bind = 1" >> /etc/sysctl.conf
sysctl -p
```

On host 1, config /etc/keepalived/keepalived.conf

```
vrrp_script chk_haproxy {
   script "pkill -0 haproxy"     # verify the pid existance
   interval 2                    # check every 2 seconds
   weight 2                      # add 2 points of prio if OK
}
 
vrrp_instance VI_1 {
   interface eth0                # interface to monitor
   state MASTER
   virtual_router_id 51          # Assign one ID for this route
   priority 101                  # 101 on master, 100 on backup
   virtual_ipaddress {
       10.224.147.208            # the virtual IP
   }
   track_script {
       chk_haproxy
   }
}
```

On host 2, config /etc/keepalived/keepalived.conf

```
vrrp_script chk_haproxy {
   script "pkill -0 haproxy"     # verify the pid existance
   interval 2                    # check every 2 seconds
   weight 2                      # add 2 points of prio if OK
}
 
vrrp_instance VI_1 {
   interface eth0                # interface to monitor
   state MASTER                  # both master and backup are set as MASTER
   virtual_router_id 51          # Assign one ID for this route
   priority 100                  # 101 on master, 100 on backup
   virtual_ipaddress {
       10.224.147.208            # the virtual IP
   }
   track_script {
       chk_haproxy
   }
}
```

On host 1 and host 2, start keepalived

```
service keepalived start
```

## To Verify

On host 1, to check who holds vip
```
$ ip a | grep -e inet.*eth0
inet 10.224.147.166/24 brd 10.224.147.255 scope global dynamic eth0
inet 10.224.147.208/32 scope global eth0
```

On host 2, 
```
$ ip a | grep -e inet.*eth0
inet 10.224.147.167/24 brd 10.224.147.255 scope global dynamic eth0
```

If you killed haproxy on host 1, host 2 should get the vip 10.224.147.208.

Keepalived logs in /var/log/messages, on host 1 you can see keepalived "Entering MASTER STATE".

```
...
Oct 29 13:53:38 host1 Keepalived_vrrp[2256]: VRRP_Script(chk_haproxy) succeeded
Oct 29 13:53:39 host1 Keepalived_vrrp[2256]: VRRP_Instance(VI_1) forcing a new MASTER election
Oct 29 13:53:39 host1 Keepalived_vrrp[2256]: VRRP_Instance(VI_1) forcing a new MASTER election
Oct 29 13:53:40 host1 Keepalived_vrrp[2256]: VRRP_Instance(VI_1) Transition to MASTER STATE
Oct 29 13:53:41 host1 Keepalived_vrrp[2256]: VRRP_Instance(VI_1) Entering MASTER STATE
...
```

## Neutron Allowed-address-pair

Neutron on default will drop all traffic who comes from a port, but has a different IP from the port's VM. By adding allowed-address-pair, we allow that kind of traffic from the port. In this way, a VM can use virtual ip.

On neutron controller
```
$ neutron port-update <port-id-of-host-1> --allowed-address-pairs type=dict list=true ip_address=10.224.147.208
$ neutron port-update <port-id-of-host-2> --allowed-address-pairs type=dict list=true ip_address=10.224.147.208
```

On host 3, ping vip will pass because of the allowed address pair.
```
$ ping 10.224.147.208
PING 10.224.147.208 (10.224.147.208) 56(84) bytes of data.
64 bytes from 10.224.147.208: icmp_seq=1 ttl=64 time=2.49 ms
64 bytes from 10.224.147.208: icmp_seq=2 ttl=64 time=0.399 ms
64 bytes from 10.224.147.208: icmp_seq=3 ttl=64 time=0.477 ms
```

Since we use fixed-ip to access public network. Enter http://10.224.147.208:5000/ in browser you should see apache welcome page behind haproxy.

## Further More

Not only haproxy, you can just boot several VM and use keepalived VRRP to create a redundant HA group.

Further, [conntrackd](http://conntrack-tools.netfilter.org/conntrackd.html) can be used to transfer tcp states between master and backup, so that connections are not interrupted. This is used in [Neutron L3 HA VRRP](https://wiki.openstack.org/wiki/Neutron/
L3_High_Availability_VRRP).

I'm thinking that keepalived VRRP only use one haproxy each time, wasting the others' capacity. Is there a way for both HA and share capacity between haproxies?

## References

* Install HAProxy and Keepalived (Virtual IP): <http://support.severalnines.com/entries/23612682-Install-HAProxy-and-Keepalived-Virtual-IP->
* 用HAProxy和KeepAlived构建高可用的反向代理系统: <http://weizhifeng.net/HA-with-HAProxy-and-KeepAlived.html>
