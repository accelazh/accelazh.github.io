---
layout: post
title: "Play with Docker Network"
tagline : "Play with Docker Network"
description: "Play with Docker Network"
category: "docker"
tags: [docker, network, linux-bridge]
---
{% include JB/setup %}

## Environment

3 nodes VMs (or called hosts), each installed docker.

  * VM1/Host1: 10.32.171.202  centos7
  * VM2/Host2: 10.32.171.203  centos7
  * Vm3/Host3: 10.32.171.204  centos7

First, lets setup the experiment environment. On each node

```
docker pull centos:7
docker run -d --name test1 centos:7 /bin/bash -c "while true; do sleep 3600; done"  # name test2 on VM2, test3 on VM3

# to connect the container
docker exec -it test1 bash
```

Make sure kernel is willing to forward IP packets.

```
$ sysctl net.ipv4.conf.all.forwarding=1
$ sysctl net.ipv4.conf.all.forwarding
net.ipv4.conf.all.forwarding = 1
```

## Introduction

Docker, once installed, creates bridge docker0. When a container is created, a veth pair (veth2a6e52a) links it to docker0. Refer to [offical doc](https://docs.docker.com/articles/networking/). Note that `ens32` is my host's "eth0".

```
# VM1
$ ip li
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens32: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT qlen 1000
    link/ether 00:50:56:98:61:4c brd ff:ff:ff:ff:ff:ff
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT
    link/ether 56:84:7a:fe:97:99 brd ff:ff:ff:ff:ff:ff
25: veth2a6e52a: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT
    link/ether 56:7f:46:26:0d:cb brd ff:ff:ff:ff:ff:ff

$ brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.56847afe9799       no              veth2a6e52a

$ bridge li
25: veth2a6e52a state UP : <BROADCAST,UP,LOWER_UP> mtu 1500 master docker0 state forwarding priority 32 cost 2
```

Docker use route and iptables (note the `MASQUERADE`) to create NAT network for the container, so that it can access outside.

```
$ ip route
default via 10.32.171.1 dev ens32
10.32.171.0/24 dev ens32  proto kernel  scope link  src 10.32.171.202
169.254.0.0/16 dev ens32  scope link  metric 1002
172.17.0.0/16 dev docker0  proto kernel  scope link  src 172.17.42.1

$ iptables --list -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination
PREROUTING_direct  all  --  anywhere             anywhere
PREROUTING_ZONES_SOURCE  all  --  anywhere             anywhere
PREROUTING_ZONES  all  --  anywhere             anywhere
DOCKER     all  --  anywhere             anywhere             ADDRTYPE match dst-type LOCAL

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
OUTPUT_direct  all  --  anywhere             anywhere
DOCKER     all  --  anywhere            !loopback/8           ADDRTYPE match dst-type LOCAL

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  172.17.0.0/16        anywhere
POSTROUTING_direct  all  --  anywhere             anywhere
POSTROUTING_ZONES_SOURCE  all  --  anywhere             anywhere
POSTROUTING_ZONES  all  --  anywhere             anywhere
MASQUERADE  tcp  --  172.17.0.4           172.17.0.4           tcp dpt:https
MASQUERADE  tcp  --  172.17.0.4           172.17.0.4           tcp dpt:6611
MASQUERADE  tcp  --  172.17.0.4           172.17.0.4           tcp dpt:7072
MASQUERADE  tcp  --  172.17.0.4           172.17.0.4           tcp dpt:http
MASQUERADE  tcp  --  172.17.0.4           172.17.0.4           tcp dpt:9011

Chain DOCKER (2 references)
target     prot opt source               destination

Chain OUTPUT_direct (1 references)
target     prot opt source               destination

Chain POSTROUTING_ZONES (1 references)
target     prot opt source               destination
POST_public  all  --  anywhere             anywhere            [goto]
POST_public  all  --  anywhere             anywhere            [goto]

Chain POSTROUTING_ZONES_SOURCE (1 references)
target     prot opt source               destination

Chain POSTROUTING_direct (1 references)
target     prot opt source               destination

Chain POST_public (2 references)
target     prot opt source               destination
POST_public_log  all  --  anywhere             anywhere
POST_public_deny  all  --  anywhere             anywhere
POST_public_allow  all  --  anywhere             anywhere

Chain POST_public_allow (1 references)
target     prot opt source               destination

Chain POST_public_deny (1 references)
target     prot opt source               destination

Chain POST_public_log (1 references)
target     prot opt source               destination

Chain PREROUTING_ZONES (1 references)
target     prot opt source               destination
PRE_public  all  --  anywhere             anywhere            [goto]
PRE_public  all  --  anywhere             anywhere            [goto]

Chain PREROUTING_ZONES_SOURCE (1 references)
target     prot opt source               destination

Chain PREROUTING_direct (1 references)
target     prot opt source               destination

Chain PRE_public (2 references)
target     prot opt source               destination
PRE_public_log  all  --  anywhere             anywhere
PRE_public_deny  all  --  anywhere             anywhere
PRE_public_allow  all  --  anywhere             anywhere

Chain PRE_public_allow (1 references)
target     prot opt source               destination

Chain PRE_public_deny (1 references)
target     prot opt source               destination

Chain PRE_public_log (1 references)
target     prot opt source               destination
```

### About The Namespaces

The container is using different namespaces than other processes. To view it (namespace guide [1](http://lwn.net/Articles/531114/)[2](http://crosbymichael.com/creating-containers-part-1.html)):

```
# VM1
$ ll /proc/3378/ns  # docker process
total 0
lrwxrwxrwx 1 root root 0 May 11 14:32 ipc -> ipc:[4026531839]
lrwxrwxrwx 1 root root 0 May 11 14:32 mnt -> mnt:[4026532442]
lrwxrwxrwx 1 root root 0 May 11 14:32 net -> net:[4026531956]
lrwxrwxrwx 1 root root 0 May 11 14:32 pid -> pid:[4026531836]
lrwxrwxrwx 1 root root 0 May 11 14:32 uts -> uts:[4026531838]
$ ll /proc/1/ns     # systemd process
total 0
lrwxrwxrwx 1 root root 0 May 11 14:33 ipc -> ipc:[4026531839]
lrwxrwxrwx 1 root root 0 May 11 14:33 mnt -> mnt:[4026531840]
lrwxrwxrwx 1 root root 0 May 11 14:33 net -> net:[4026531956]
lrwxrwxrwx 1 root root 0 May 11 14:33 pid -> pid:[4026531836]
lrwxrwxrwx 1 root root 0 May 11 14:33 uts -> uts:[4026531838]
$ ll /proc/4718/ns/   # container test1, the ns is different
total 0
lrwxrwxrwx 1 root root 0 May  8 16:44 ipc -> ipc:[4026532453]
lrwxrwxrwx 1 root root 0 May  8 16:44 mnt -> mnt:[4026532451]
lrwxrwxrwx 1 root root 0 May  8 16:44 net -> net:[4026532456]
lrwxrwxrwx 1 root root 0 May  8 16:44 pid -> pid:[4026532454]
lrwxrwxrwx 1 root root 0 May  8 16:44 uts -> uts:[4026532452]
```

However, `ip netns` shows nothing. [Why?](https://github.com/DockerPool/dockerpool_website_res/blob/master/docs/%E8%AE%BF%E9%97%AE%20Docker%20%E5%AE%B9%E5%99%A8%E7%9A%84%E5%90%8D%E5%AD%97%E7%A9%BA%E9%97%B4.md) Docker deletes network namespace info on default.

```
# However, ip netns shows nothing (root). Why?
$ ip netns list
$

# New network namespaces should able to be seen in /var/run/netns. But docker deletes them on default
$ ip netns add blue
$ ls /var/run/netns/
blue
$ ip netns delete blue

# Let's restore these netns info
$ docker inspect --format='{{ .State.Pid }}' test1    # show pid of test1
4718
$ ln -s /proc/4718/ns/net /var/run/netns/4718

# View network info inside my test1 container
$ ip netns
4718
$ ip netns exec 4718 ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
32: eth0: <BROADCAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
    link/ether 02:42:ac:11:00:01 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe11:1/64 scope link
       valid_lft forever preferred_lft forever

# Show another pair of outside veth pair
$ ethtool -S veth523170f
NIC statistics:
     peer_ifindex: 32    # Note the 32 shown above

# Restore everything to default
$ rm -f /var/run/netns/4718
```

Question: how can I create my own namespaces in shell and launch/change process to it?

### About Veth Pair

Veth pair are usually used to communicate between different network spaces, see [1](http://www.opencloudblog.com/?p=66)[2](http://blog.scottlowe.org/2013/09/04/introducing-linux-network-namespaces/). Veth pair have know performance issue: [1](http://www.opencloudblog.com/?p=96)][2](https://bugs.launchpad.net/nova-docker/+bug/1418823). Some suggests using ovs patch ports, which [overperforms](http://www.opencloudblog.com/?p=386) veth pair.

## Build My Own Docker Network

Here's a series of experiment to build networks between host and container. Finally I will build a private network 192.168.7.0/24 for the containers, separated from the host network 10.32.171.0/24. A virtual router (by network namespace) connects two networks, which enables host and container to ssh each other.

### Milestone 1: Intra-host Ping

First, on each host, delete original docker bridge and iptables rules. Some of this section refers to [here](https://docs.docker.com/articles/networking/#docker0).

```
service docker stop
ip link set dev docker0 down
brctl delbr docker0
iptables -t nat -F POSTROUTING
```

Add my own bridges

```
brctl addbr bridge0
ip addr add 192.168.5.1/24 dev bridge0
ip link set dev bridge0 up

brctl addbr bridge1
ip addr add 192.168.6.1/24 dev bridge1
ip link set dev bridge1 up
```

Start the docker service with bridge0 and iptables untouched. About how to config docker start up options on CentOS, thanks to [Fabien](http://stackoverflow.com/questions/26166550/set-docker-opts-in-centos).

```
# Append below to /etc/sysconfig/docker::OPTIONS
-b=bridge0 --iptables=false    # actually, bridge0 can be whatever
# Start docker service
service docker start
```

Start my centos test container without network config, on each host.

```
$ docker run -d --name test1.1 --net=none centos:7 /bin/bash -c "while true; do sleep 3600; done"  # name test2.1 on VM2, test3.1 on VM3
$ docker exec -it test1.1 bash

# inside test1.1, no network at all
$ ip li
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
$ ip ro
$
```

Create 2 NICs for my test container, on each host

```
# Restore the network namespace info
export TEST_PID=$(docker inspect --format='{{ .State.Pid }}' test1.1)    # change to test2.1 on VM2, test3.1 on VM3
ip netns add blue && ip netns delete blue    # to ensure /var/run/netns folder exists
ln -s /proc/${TEST_PID}/ns/net /var/run/netns/${TEST_PID}

# Create veth pairs for container
ip link add ${TEST_PID}.eth0 type veth peer name veth0
ip link add ${TEST_PID}.eth1 type veth peer name veth1

# Assign veth pairs to container
ip li set veth0 netns ${TEST_PID}
ip li set veth1 netns ${TEST_PID}

# Add NIC to bridges
brctl addif bridge0 ${TEST_PID}.eth0
brctl addif bridge1 ${TEST_PID}.eth1
```

Inside the container you can see these new NICs

```
$ docker exec -it test1.1 bash
$ ip li
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
47: veth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT qlen 1000
    link/ether 6e:21:24:67:71:fd brd ff:ff:ff:ff:ff:ff
49: veth1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN mode DEFAULT qlen 1000
    link/ether 6e:14:8b:d3:de:a5 brd ff:ff:ff:ff:ff:ff
```

On each host, give each of my container NICs a new IP in the corresponding bridge network. (I'm just pseudoing a DHCP service.)

```
# Host 1
ip netns exec ${TEST_PID} ip addr add 192.168.5.2 dev veth0
ip netns exec ${TEST_PID} ip addr add 192.168.6.2 dev veth1

# Host 2
ip netns exec ${TEST_PID} ip addr add 192.168.5.3 dev veth0
ip netns exec ${TEST_PID} ip addr add 192.168.6.3 dev veth1

# Host 3
ip netns exec ${TEST_PID} ip addr add 192.168.5.4 dev veth0
ip netns exec ${TEST_PID} ip addr add 192.168.6.4 dev veth1
```

Bring up all interfaces on each host

```
ip netns exec ${TEST_PID} ip li set veth0 up
ip netns exec ${TEST_PID} ip li set veth1 up
ip li set ${TEST_PID}.eth0 up
ip li set ${TEST_PID}.eth1 up
```

On each host, config the route inside container

```
# Host 1
ip netns exec ${TEST_PID} ip route add 192.168.5.0/24 dev veth0
ip netns exec ${TEST_PID} ip route add 192.168.6.0/24 dev veth1
ip netns exec ${TEST_PID} ip route add default via 192.168.5.1

# Host 2
ip netns exec ${TEST_PID} ip route add 192.168.5.0/24 dev veth0
ip netns exec ${TEST_PID} ip route add 192.168.6.0/24 dev veth1
ip netns exec ${TEST_PID} ip route add default via 192.168.5.1

# Host 3
ip netns exec ${TEST_PID} ip route add 192.168.5.0/24 dev veth0
ip netns exec ${TEST_PID} ip route add 192.168.6.0/24 dev veth1
ip netns exec ${TEST_PID} ip route add default via 192.168.5.1
```

At this point, you should be above to ping a container from its own host. But you cannot ping it from an outside host.

```
# Host 1
$ ping 192.168.5.2
PING 192.168.5.2 (192.168.5.2) 56(84) bytes of data.
64 bytes from 192.168.5.2: icmp_seq=1 ttl=64 time=0.188 ms
...
$ ping 192.168.6.2
PING 192.168.6.2 (192.168.6.2) 56(84) bytes of data.
64 bytes from 192.168.6.2: icmp_seq=1 ttl=64 time=0.160 ms
...

# Host 3
$ ping 192.168.5.4
PING 192.168.5.4 (192.168.5.4) 56(84) bytes of data.
64 bytes from 192.168.5.4: icmp_seq=1 ttl=64 time=0.275 ms
...
$ ping 192.168.6.4
PING 192.168.6.4 (192.168.6.4) 56(84) bytes of data.
64 bytes from 192.168.6.4: icmp_seq=1 ttl=64 time=0.120 ms
...
```

### Milestone 2: Access Outside via Host NAT

Add host NAT on each host, so that test container can access outside via veth0. Related [guide](http://www.revsys.com/writings/quicktips/nat.html).

```
# Modify the nat table
iptables -t nat -A POSTROUTING -j MASQUERADE -s 192.168.5.0/24 -o ens32    # ens32 is my host's eth0
```

Add proper forward rules so that my container packets will be accepted, on each host.

```
# Modify the filter table. Note that if you want to use "!" or "any", read manula, don't just append them to device name
iptables -I FORWARD 1 -i bridge0 ! -o bridge0 -j ACCEPT
iptables -I FORWARD 2 ! -i bridge0 -o bridge0 -m state --state RELATED,ESTABLISHED -j ACCEPT

iptables -I FORWARD 3 -i bridge1 ! -o bridge1 -j ACCEPT
iptables -I FORWARD 4 ! -i bridge1 -o bridge1 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

Install the necessary tool on each of my centos container.

```
docker exec -it test1.1 bash    # name 2.1 on VM2, 3.1 on VM3
# inside container
yum install -y bind-utils traceroute telnet openssh openssh-server openssh-clients net-tools tcpdump
```

Let's enable sshd inside each container. Useful [doc](https://docs.docker.com/examples/running_ssh_service/) here.

```
docker exec -it test1.1 bash    # name 2.1 on VM2, 3.1 on VM3
# inside container
vi /etc/ssh/sshd_config
    # Change below config options
    PasswordAuthentication yes
    PermitRootLogin yes
/usr/bin/ssh-keygen -A
echo 'root:123work' | chpasswd
nohup /usr/sbin/sshd -D > /var/log/sshd.log 2>&1 &
exit
```

On each host, let's test sshd. By now we can ssh from a host to the container located on it, but not a container on other hosts.

```
# on host 1
$ ssh root@192.168.5.2 'cat /etc/hostname'
6e5898a7d4e4
$ ssh root@192.168.6.2 'cat /etc/hostname'
6e5898a7d4e4

# on host 3
$ ssh root@192.168.5.4 'cat /etc/hostname'
89c83ee77559
$ ssh root@192.168.6.4 'cat /etc/hostname'
89c83ee77559
```

### Milestone 3: SSH from A Host to A Remote Container

How to enable any host to connect to any container? Let's do it. On each host, delete the original routing to bridge1, because they are too broad.

```
ip route delete 192.168.6.0/24 dev bridge1
```

We connect only local container to local bridges. Other containers are gatewayed to their corresponding hosts.

```
# On host 1
ip route add 192.168.6.2 dev bridge1 src 192.168.6.1
ip route add 192.168.6.3 via 10.32.171.203 dev ens32
ip route add 192.168.6.4 via 10.32.171.204 dev ens32

# On host 2
ip route add 192.168.6.2 via 10.32.171.202 dev ens32
ip route add 192.168.6.3 dev bridge1 src 192.168.6.1
ip route add 192.168.6.4 via 10.32.171.204 dev ens32

# On host 3
ip route add 192.168.6.2 via 10.32.171.202 dev ens32
ip route add 192.168.6.3 via 10.32.171.203 dev ens32
ip route add 192.168.6.4 dev bridge1 src 192.168.6.1

# You should still be able to ssh to local container. For example on host 1
ssh root@192.168.5.2 'cat /etc/hostname'
ssh root@192.168.6.2 'cat /etc/hostname'
```

Next we need to make sure ping reply can be sent outside container

```
# On host 1
ip netns exec ${TEST_PID} ip route add 10.32.171.203 via 192.168.6.1 dev veth1
ip netns exec ${TEST_PID} ip route add 10.32.171.204 via 192.168.6.1 dev veth1

# On host 2
ip netns exec ${TEST_PID} ip route add 10.32.171.202 via 192.168.6.1 dev veth1
ip netns exec ${TEST_PID} ip route add 10.32.171.204 via 192.168.6.1 dev veth1

# On host 3
ip netns exec ${TEST_PID} ip route add 10.32.171.202 via 192.168.6.1 dev veth1
ip netns exec ${TEST_PID} ip route add 10.32.171.203 via 192.168.6.1 dev veth1
```

Make iptables allow the ssh traffic, on each host

```
iptables -I FORWARD 1 -o bridge1 -p tcp --dport 22 -j ACCEPT
```

Now you should be able to ssh from any host to any container, via 192.168.6.0/24, but not from container to container.

```
# On host 1
ssh root@192.168.6.4 'cat /etc/hostname'
ssh root@192.168.6.2 'cat /etc/hostname'

# On host 3
ssh root@192.168.6.2 'cat /etc/hostname'
ssh root@192.168.6.4 'cat /etc/hostname'
```

### Milestone 4: Flat Bridged Private Network for Containers

This setup needs 2 NICs on each host. I already have `ens32` in the above sections. Thank the operator who has given me a fresh new `ens34` on each host, with promisc mode enabled from the infra level (vCenter). Note that `ens32` and `ens34` are actually connected on the same vswitch, although logically in separated networks. First, bring all `ens34` up. They don't need ip.

```
# On each host
ip li set ens34 up
```

I will use a new bridge, `bridge2`, for this section. So that the former configuration won't be messed up. The bridge won't have ip. There will also a new NIC inside each container. Do below on each host

```
# Create new bridge. The bridge doesn't have ip
brctl addbr bridge2
ip link set dev bridge2 up

# Create new veth pair as the new NIC
ip link add ${TEST_PID}.eth2 type veth peer name veth2
ip li set veth2 netns ${TEST_PID}
brctl addif bridge2 ${TEST_PID}.eth2
ip netns exec ${TEST_PID} ip li set veth2 up
ip li set ${TEST_PID}.eth2 up

# Delete useless routes added by Milestone 3. It may mess up what we gonna do next
ip netns exec ${TEST_PID} ip route del 10.32.171.202
ip netns exec ${TEST_PID} ip route del 10.32.171.203
ip netns exec ${TEST_PID} ip route del 10.32.171.204

# Setup the route for each container
ip netns exec ${TEST_PID} ip route add 192.168.7.0/24 dev veth2

# Add new NIC of the host to bridge
brctl addif bridge2 ens34    # my second NIC on the host is ens34

# Enable promisc mode for NIC
ip li set ens34 promisc on
```

Setup the ip for each container

```
# On host 1
ip netns exec ${TEST_PID} ip addr add 192.168.7.2 dev veth2

# On host 2
ip netns exec ${TEST_PID} ip addr add 192.168.7.3 dev veth2

# On host 3
ip netns exec ${TEST_PID} ip addr add 192.168.7.4 dev veth2
```

Now you should be able to ssh each containers.

```
# On host 1
ip netns exec ${TEST_PID} ssh root@192.168.7.4 'cat /etc/hostname'
ip netns exec ${TEST_PID} ssh root@192.168.7.2 'cat /etc/hostname'

# On host 3
ip netns exec ${TEST_PID} ssh root@192.168.7.2 'cat /etc/hostname'
ip netns exec ${TEST_PID} ssh root@192.168.7.4 'cat /etc/hostname'
```

### Milestone 5: A Router Between Host and Container Network (FAILED)

I'm trying to build a router between host network 10.32.171.0/24 and container network 192.168.7.0/24. Since I don't have a new ip on 10.32.171.0/24, I will put the router inside host 1. The router is implemented by network namespace, don't even need a container. First, on host 1, Let's set up the router.

```
# On host 1
ip netns add testrt
ip li add testrt.eth0 type veth peer name veth0    # NIC for host network 10.32.171.0/24
ip li add testrt.eth1 type veth peer name veth1    # NIC for container network 192.168.7.0/24
ip li set veth0 netns testrt
ip li set veth1 netns testrt

brctl addif bridge2 testrt.eth1                    # connect veth1 to container network
ip netns exec testrt ip addr add 192.168.7.100 dev veth1

ip li set testrt.eth0 up
ip netns exec testrt ip li set veth0 up
ip li set testrt.eth1 up
ip netns exec testrt ip li set veth1 up

ip li set testrt.eth0 promisc on
ip netns exec testrt ip li set veth0 promisc on
ip li set testrt.eth1 promisc on
ip netns exec testrt ip li set veth1 promisc on
```

The router `testrt` is now connected to ens34, inside host 1. Let's install routes for testrt.

```
# On host 1
# make sure packet going container network are routed into testrt
ip route add 192.168.7.0/24 dev testrt.eth0

# Install testrt router table
ip netns exec testrt ip route add 192.168.7.0/24 dev veth1
ip netns exec testrt ip route add 10.32.171.0/24 dev veth0

# You should be able to ping or ping from testrt now
ping 192.168.7.100
ip netns exec testrt ping 192.168.7.2
ip netns exec testrt ping 192.168.7.4
ip netns exec testrt ping 10.32.171.202
```

Let's set each host and container to use testrt as gateway.

```
# On each host
ip netns exec ${TEST_PID} ip route add 10.32.171.0/24 via 192.168.7.100 dev veth2

# On each host except host 1 (host 1 already has route to testrt)
ip route add 192.168.7.0/24 via 10.32.171.202 dev ens32
```

You should be able to ssh from each host (network 10.32.171.0/24) to any container (network 192.168.7.0/24), or vice versa.

```
# On host 1
ssh root@192.168.7.2 'cat /etc/hostname'
ssh root@192.168.7.4 'cat /etc/hostname'
docker exec -it test1.1 ssh root@10.32.171.202 'cat /etc/hostname'
docker exec -it test1.1 ssh root@10.32.171.204 'cat /etc/hostname'

# On host 3
ssh root@192.168.7.2 'cat /etc/hostname'
ssh root@192.168.7.4 'cat /etc/hostname'
docker exec -it test3.1 ssh root@10.32.171.202 'cat /etc/hostname'
docker exec -it test3.1 ssh root@10.32.171.204 'cat /etc/hostname'
```

Failed here: host 1 ping 192.168.7.2, ICMP request can be seen on test1.1's veth0 (tcpdump), but never reaches veth1. I tried using container (testrt2) instead of network namespace to build testrt, stuck in the same place. Host 3 ping 192.168.7.101 (the container testrt2), arp request for 10.32.171.204 heard on testrt2.eth0, but not ens32. Another issue, testrt2 cannot even ping 10.32.171.202.

### Milestone 6: Just Use Host 1 & Container test1.1 as Router (FAILED)

Since I find it hard to use network namespace or container to create a virutal router inside host 1, I will use host 1 itself as a router by tweaking ip route. First, delete old gateway settings from Milestone 5.

```
# On each host
ip route del 192.168.7.0/24
ip netns exec ${TEST_PID} ip route del 10.32.171.0/24

# On host 1
brctl delif bridge2 testrt.eth1
```

My plan is to use host 1 as router/gateway for 10.32.171.0/24, use test1.1 as router/gateway for 192.168.7.0/24, and hook host 1 and test1.1 together by a new veth pair.

```
# On host 1
ip li add ${TEST_PID}.eth3 type veth peer name veth3
ip li set veth3 netns ${TEST_PID}

ip li set ${TEST_PID}.eth3 promisc on
ip netns exec ${TEST_PID} ip li set veth3 promisc on

ip li set ${TEST_PID}.eth3 up
ip netns exec ${TEST_PID} ip li set veth3 up

ip route add 192.168.7.0/24 dev ${TEST_PID}.eth3
ip netns exec ${TEST_PID} ip route add 10.32.171.0/24 dev veth3

# Now you should be able to ping test1.1
ping 192.168.7.2
```

Set gateway on other hosts and containers

```
# On host 2 and 3
ip route add 192.168.7.0/24 via 10.32.171.202 dev ens32
ip netns exec ${TEST_PID} ip route add 10.32.171.0/24 via 192.168.7.2 dev veth2
```

Failed: host 1 ping 192.168.7.4, inside test1.1, veth3 sees ICMP request, but veth2 never get forwarded. Same problem with Milestone 5. Another issue, test1.1 cannot even ping host 1. At least I can generate a few rules here

  * A NIC won't send packets out if it is not set IP, nor will it if IP is not in the same network range with the packet; even if ip route says packets is delivered to that NIC.
  * Create a container, then put a veth pair one into it and one in host. This won't make the container and the host connected.
  * Always test network connectivity, in 2 directions, between every hop.

### Milestone 7: Finally Made the Router Work

In this section I'm going to build a virtual router, using namework namespace, resides in host 1. Container network 192.168.7.0/24 and host network 10.32.171.205/24 will be able to communicate with each other via this router. First, let's clean up the mess left by above two failed sections.

```
# On host 1
ip netns exec ${TEST_PID} ip li del veth3
brctl delif bridge2 testrt.eth0
brctl delif bridge2 testrt.eth1
brctl delif bridge2 testrt2.eth0
brctl delif bridge2 testrt2.eth0

# On each host
ip route del 192.168.7.0/24
ip netns exec ${TEST_PID} ip route del 10.32.171.0/24
```

Still, I use network namespace to build a router, the `testrt3`

```
# On host 1
ip netns add testrt3
ip li add testrt3.eth0 type veth peer name veth0    # NIC for host network 10.32.171.0/24
ip li add testrt3.eth1 type veth peer name veth1    # NIC for container network 192.168.7.0/24
ip li set veth0 netns testrt3
ip li set veth1 netns testrt3

brctl addif bridge2 testrt3.eth1                    # connect veth1 to container network
ip netns exec testrt3 ip addr add 192.168.7.100 dev veth1

ip li set testrt3.eth0 up
ip netns exec testrt3 ip li set veth0 up
ip li set testrt3.eth1 up
ip netns exec testrt3 ip li set veth1 up

ip netns exec testrt3 ip route add 192.168.7.0/24 dev veth1
ip netns exec testrt3 ip route add 10.32.171.0/24 dev veth0
```

Let's set each container's gateway to testrt3.

```
# On each host
ip netns exec ${TEST_PID} ip route add 10.32.171.0/24 via 192.168.7.100 dev veth2

# You should be able to ping router from container
ip netns exec ${TEST_PID} ping 192.168.7.100
```

At this time, when I ping from a container to a host, I can see icmp or arp request on testrt3's veth1. But they cannot be forward to testrt3's veth0. Next, to connect testrt3's veth0 to host 1, let's create a bridge which connects to 10.32.171.0/24 instead of ens32.

```
# On host 1
brctl addbr br-ens32
ip li set br-ens32 promisc on

# Add ens32 to br-ens32, host 1 will be temporarily disconnected
ip addr del 10.32.171.202/24 dev ens32 && \
ip addr add 10.32.171.202/24 dev br-ens32 && \
brctl addif br-ens32 ens32 && \
ip route add default via 10.32.171.1 dev br-ens32 && \    # add default route. in my case it is 10.32.171.1
ip link set dev br-ens32 up

# Reconnect to host 1, restore the original routes
ip route add 169.254.0.0/16 dev br-ens32 metric 1002    # the cloud init address
ip route add 192.168.6.3 via 10.32.171.203 dev br-ens32
ip route add 192.168.6.4 via 10.32.171.204 dev br-ens32

# Restore the host NAT for 192.168.5.0/24
LINENO_MASQ=$(iptables -L POSTROUTING -v --line-numbers -t nat | grep 'MASQUERADE .* ens32 .* 192.168.5.0' | awk '{print $1}')
iptables -D POSTROUTING ${LINENO_MASQ} -t nat
iptables -t nat -A POSTROUTING -j MASQUERADE -s 192.168.5.0/24 -o br-ens32
```

Now we can connect testrt3's veth0 to 10.32.171.0/24.

```
# On host 1
brctl addif br-ens32 testrt3.eth0
```

Next, add an ip address to testrt's veth0, who's facing 10.32.171.0/24 side. I borrowed 10.32.171.205 from the network operator. Both side of the router NIC should have ip.

```
# On host 1
ip netns exec testrt3 ip addr add 10.32.171.205 dev veth0

# You should be able to ping router
ping 10.32.171.205
ip netns exec testrt3 ping 10.32.171.202
```

Set each host 's gateway to testrt3

```
# On host 1
ip route add 192.168.7.0/24 via 10.32.171.205 dev br-ens32

# On host 2 and 3
ip route add 192.168.7.0/24 via 10.32.171.205 dev ens32
```

By now, I can ssh from any host to any container, or vice versa.

```
# On host 1
ssh root@192.168.7.2 'cat /etc/hostname' && \
ssh root@192.168.7.4 'cat /etc/hostname' && \
docker exec -it test1.1 ssh root@10.32.171.202 'hostname' && \
docker exec -it test1.1 ssh root@10.32.171.204 'hostname' && \
docker exec -it test1.1 ssh root@192.168.7.2 'cat /etc/hostname' && \
docker exec -it test1.1 ssh root@192.168.7.4 'cat /etc/hostname'

# On host 3
ssh root@192.168.7.2 'cat /etc/hostname' && \
ssh root@192.168.7.4 'cat /etc/hostname' && \
docker exec -it test3.1 ssh root@10.32.171.202 'hostname' && \
docker exec -it test3.1 ssh root@10.32.171.204 'hostname' && \
docker exec -it test3.1 ssh root@192.168.7.2 'cat /etc/hostname' && \
docker exec -it test3.1 ssh root@192.168.7.4 'cat /etc/hostname'
```

Finally, I made the router work! The keypoint is, each side NIC of the router must have an IP, from the network range which it is facing. Other hosts or containers must set gateway to this router's IP in the corresponding side. In prior sections I always tried to avoid using extra IP for router, i.e. 10.32.171.205, which doesn't work anyway.

## Future

Use gre/vxlan to set up private tunnel network for containers. Add router to them.






