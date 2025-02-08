---
layout: post
title: "HA of Haproxy - Using Keepalived VRRP"
tagline : "HA of Haproxy - Using Keepalived VRRP"
description: "Make Haproxy HA by using keepalived VRRP"
category: "Cloud"
tags: [haproxy, HA, keepalived, VRRP]
---
{% include JB/setup %}

Haproxy can be used to create HA of backend servers. But how to HA for Haproxy itself?

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

Not only haproxy, you can just boot several VM and use keepalived VRRP to create a redundant HA group. See [this](http://blog.aaronorosen.com/implementing-high-availability-instances-with-neutron-using-vrrp/).

Further, [conntrackd](http://conntrack-tools.netfilter.org/conntrackd.html) can be used to transfer tcp states between master and backup, so that connections are not interrupted. This is used in [Neutron L3 HA VRRP](https://wiki.openstack.org/wiki/Neutron/
L3_High_Availability_VRRP).

I'm thinking that keepalived VRRP only use one haproxy each time, wasting the others' capacity. Is there a way for both HA and share capacity between haproxies?

## Haproxy in Openstack

Share-nothing services in Openstasck can use Haproxy for HA, including swift-proxy, glance, nova-api, keystone and other controller services. Check [Openstack HA Manual](http://docs.openstack.org/high-availability-guide/content/ha-aa-haproxy.html). Different services can share one Haproxy node/pair.

Example config for openstack.

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
        log             global
        mode            http
        option          httplog
        option          dontlognull
        retries         3
        option          redispatch
        maxconn         20000
        contimeout      5000
        clitimeout      50000
        srvtimeout      50000

# haproxy web
listen stats 0.0.0.0:9000       #Listen on all IP's on port 9000
    mode http
    balance
    timeout client 5000
    timeout connect 4000
    timeout server 30000

    stats uri /haproxy
    stats realm HAProxy\ Statistics
    stats auth admin:password
    stats admin if TRUE

# horizon
frontend horizon_frontend
    bind horizon.app.com:443 ssl crt /home/app/cert/appcert/app.crt
    mode http
    option httpclose
    option forwardfor
    reqadd X-Forwarded-Protocol:\ https
    default_backend horizon_server
 
backend horizon_server
    mode http
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server horizon1 10.224.155.xx:8088 check cookie horizon1
    server horizon2 10.224.155.xx:8088 check cookie horizon2

# keystone api
frontend keystone_frontend
    bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt 
    mode http
    option httpclose
    option forwardfor
    reqadd X-Forwarded-Protocol:\ https
    default_backend keystone_server

backend keystone_server
    mode http
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server keystone1 10.224.155.xx:5000 check cookie keystone1
    server keystone2 10.224.155.xx:5000 check cookie keystone2

# keystone admin
frontend keystone_admin_frontend
    bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
    mode http
    option httpclose
    option forwardfor
    reqadd X-Forwarded-Protocol:\ https
    default_backend keystone_admin_server

backend keystone_admin_server
    mode http
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server keystoneadmin1 10.224.155.xx:35357 check cookie keystoneadmin1
    server keystoneadmin2 10.224.155.xx:35357 check cookie keystoneadmin2

# nova api
frontend novaapi_frontend
        bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
        mode http
        option httpclose
        option forwardfor
        reqadd X-Forwarded-Protocol:\ https
        default_backend novaapi_server

backend novaapi_server
        mode http
        balance roundrobin
        cookie SERVERID insert indirect nocache
        server novaapi1 10.224.155.xx:8774 check cookie novaapi1
        server novaapi2 10.224.155.xx:8774 check cookie novaapi2

# nova novnc
frontend novanovnc_frontend
        bind 10.224.155.xx:444 ssl crt /home/app/cert/appcert/app.crt
        mode http
        option httpclose
        option forwardfor
        reqadd X-Forwarded-Protocol:\ https
        default_backend novanovnc_server

backend novanovnc_server
        mode http
        balance roundrobin
        cookie SERVERID insert indirect nocache
        server novanovnc1 10.224.155.xx:6080 check cookie novanovnc1
        server novanovnc2 10.224.155.xx:6080 check cookie novanovnc2

# glance api
frontend glanceapi_frontend
    bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
    mode http
    option httpclose
    option forwardfor
    reqadd X-Forwarded-Protocol:\ https
    default_backend glanceapi_server

backend glanceapi_server
    mode http
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server glanceapi1 10.224.155.xx:9292 check cookie glanceapi1
    server glanceapi2 10.224.155.xx:9292 check cookie glanceapi2

# glance registry
frontend glanceregistry_frontend
    bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
    mode http
    option httpclose
    option forwardfor
    reqadd X-Forwarded-Protocol:\ https
    default_backend glanceregistry_server

backend glanceregistry_server
    mode http
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server glanceregistry1 10.224.155.xx:9191 check cookie glanceregistry1
    server glanceregistry2 10.224.155.xx:9191 check cookie glanceregistry2

# swift api
frontend swift_frontend
    bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
    mode http
    option httpclose
    option forwardfor
    reqadd X-Forwarded-Protocol:\ https
    default_backend swift_server

backend swift_server
    mode http
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server swift1 10.224.155.xx:8080 check cookie swift1
    server swift2 10.224.155.xx:8080 check cookie swift2

# neutron
frontend neutron_frontend
        bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
        mode http
        option httpclose
        option forwardfor
        reqadd X-Forwarded-Protocol:\ https
        default_backend neutron_server

backend neutron_server
        mode http
        balance roundrobin
        cookie SERVERID insert indirect nocache
        server neutron1 10.224.155.xx:9696 check cookie neutron1
        server neutron2 10.224.155.xx:9696 check cookie neutron2

# heat api 
frontend heat_api_frontend
        bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
        mode http
        option httpclose
        option forwardfor
        reqadd X-Forwarded-Proto:\ https
        default_backend heat_api_server

backend heat_api_server
        mode http
        balance roundrobin
        cookie SERVERID insert indirect nocache
        server heat_api_1 10.224.155.xx:8004 check cookie heat_api_1
        server heat_api_2 10.224.155.xx:8004 check cookie heat_api_2

# heat api cfn
frontend heat_api_cfn_frontend
        bind 10.224.155.xx:443 ssl crt /home/app/cert/appcert/app.crt
        mode http
        option httpclose
        option forwardfor
        reqadd X-Forwarded-Proto:\ https
        default_backend heat_api_cfn_server

backend heat_api_cfn_server
        mode http
        balance roundrobin
        cookie SERVERID insert indirect nocache
        server heat_api_cfn_1 10.224.155.xx:8000 check cookie heat_api_cfn_1
        server heat_api_cfn_2 10.224.155.xx:8000 check cookie heat_api_cfn_2
```

In config line `server web01 127.0.0.1:9000 check cookie xxxxxx`, `check` enables healthcheck. `cookie` enables sticky-session. The `xxxxxx` specifies cooked value -- `SERVERID = xxxxxx`. Refer to [here](https://serversforhackers.com/editions/2014/07/15/haproxy/).

The Haproxy node only has one IP for himself. The frontend has been bind to many different IPs, i.e. VIPs.

## References

* Install HAProxy and Keepalived (Virtual IP): <http://support.severalnines.com/entries/23612682-Install-HAProxy-and-Keepalived-Virtual-IP->
* 用HAProxy和KeepAlived构建高可用的反向代理系统: <http://weizhifeng.net/HA-with-HAProxy-and-KeepAlived.html>
