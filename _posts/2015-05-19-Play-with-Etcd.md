---
layout: post
title: "Play with Etcd"
tagline : "Play with Etcd"
description: "Play with Etcd"
category: "Cloud"
tags: [consensus, paxos, etcd]
---
{% include JB/setup %}

I'm going to setup a small etcd cluster using docker and learn basic API, in order to get familiar with etcd.

## Environment

3 node VM to explore etcd cluster

  * VM dev1 192.168.56.102 centos7
  * VM dev2 192.168.56.103 centos7
  * VM dev3 192.168.56.104 centos7

Docker is already installed.

## Cluster Installation

I will install etcd on 3 nodes using static cluster mode, following [official guide](https://github.com/coreos/etcd/blob/master/Documentation/clustering.md). Although I'm using the static one, the discovery modes are worth attention. For more [documentation](https://github.com/coreos/etcd/tree/master/Documentation).

First, on each node, pull etcd images

```
docker pull quay.io/coreos/etcd:v2.0.8
```

Launch the etcd container. I guess etcd docker file changed the default shell to etcd itself, so that I can pass in command options directly.

```
# On host dev1
docker run -d -v /etc/pki/ca-trust/source/anchors/:/etc/ssl/certs -p 4001:4001 -p 2380:2380 -p 2379:2379 \
 --name etcd1 quay.io/coreos/etcd:v2.0.8 \
 -name etcd1 \
 -advertise-client-urls http://192.168.56.102:2379,http://192.168.56.102:4001 \
 -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
 -initial-advertise-peer-urls http://192.168.56.102:2380 \
 -listen-peer-urls http://0.0.0.0:2380 \
 -initial-cluster-token etcd-cluster-1 \
 -initial-cluster etcd1=http://192.168.56.102:2380,etcd2=http://192.168.56.103:2380,etcd3=http://192.168.56.104:2380 \
 -initial-cluster-state new

# On host dev2
docker run -d -v /etc/pki/ca-trust/source/anchors/:/etc/ssl/certs -p 4001:4001 -p 2380:2380 -p 2379:2379 \
 --name etcd2 quay.io/coreos/etcd:v2.0.8 \
 -name etcd2 \
 -advertise-client-urls http://192.168.56.103:2379,http://192.168.56.103:4001 \
 -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
 -initial-advertise-peer-urls http://192.168.56.103:2380 \
 -listen-peer-urls http://0.0.0.0:2380 \
 -initial-cluster-token etcd-cluster-1 \
 -initial-cluster etcd1=http://192.168.56.102:2380,etcd2=http://192.168.56.103:2380,etcd3=http://192.168.56.104:2380 \
 -initial-cluster-state new

# On host dev3
docker run -d -v /etc/pki/ca-trust/source/anchors/:/etc/ssl/certs -p 4001:4001 -p 2380:2380 -p 2379:2379 \
 --name etcd3 quay.io/coreos/etcd:v2.0.8 \
 -name etcd3 \
 -advertise-client-urls http://192.168.56.104:2379,http://192.168.56.104:4001 \
 -listen-client-urls http://0.0.0.0:2379,http://0.0.0.0:4001 \
 -initial-advertise-peer-urls http://192.168.56.104:2380 \
 -listen-peer-urls http://0.0.0.0:2380 \
 -initial-cluster-token etcd-cluster-1 \
 -initial-cluster etcd1=http://192.168.56.102:2380,etcd2=http://192.168.56.103:2380,etcd3=http://192.168.56.104:2380 \
 -initial-cluster-state new
```

## Troubleshooting

### Exit status 2, tar cannot chdir

Symptom

``` 
$ docker run -it 3b3ecf8306ba    # Just run the etcd image
Timestamp: 2015-05-19 16:53:41.179947396 -0400 EDT
Code: System error

Message: [/usr/bin/tar -cf /var/lib/docker/tmp/168ac7c7ad4d8118b39a97ceaf691dad86eda47a26d31260e84928455cac272c758795987/_tmp.tar -C /var/lib/docker/devicemapper/mnt/168ac7c7ad4d8118b39a97ceaf691dad86eda47a26d31260e84928455cac272c/rootfs/tmp .] failed: /usr/bin/tar: /var/lib/docker/devicemapper/mnt/168ac7c7ad4d8118b39a97ceaf691dad86eda47a26d31260e84928455cac272c/rootfs/tmp: Cannot chdir: No such file or directory
/usr/bin/tar: Error is not recoverable: exiting now
: exit status 2

Frames:
---
0: setupRootfs
Package: github.com/docker/libcontainer
File: rootfs_linux.go@30
---
1: Init
Package: github.com/docker/libcontainer.(*linuxStandardInit)
File: standard_init_linux.go@52
---
2: StartInitialization
Package: github.com/docker/libcontainer.(*LinuxFactory)
File: factory_linux.go@223
---
3: initializer
Package: github.com/docker/docker/daemon/execdriver/native
File: init.go@35
---
4: Init
Package: github.com/docker/docker/pkg/reexec
File: reexec.go@26
---
5: main
Package: main
File: docker.go@29
---
6: main
Package: runtime
File: proc.go@63
---
7: goexit
Package: runtime
File: asm_amd64.s@2232
FATA[0000] Error response from daemon: : exit status 2
```

Solution, use docker 1.5.0 instead of 1.6. Related docker issue: [781](https://github.com/docker/swarm/issues/781).

## API

Just run a simple set and get. First, set a value on dev2 to dev1.

```
# On host dev2 (curl progress output removed)
$ curl 192.168.56.102:2379/v2/keys/hello -XPUT -d value="world" -vv | python -m json.tool
> PUT /v2/keys/hello HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 192.168.56.102:2379
> Accept: */*
> Content-Length: 11
> Content-Type: application/x-www-form-urlencoded
>
< HTTP/1.1 200 OK
< Content-Type: application/json
< X-Etcd-Cluster-Id: 630f24e186d7d175
< X-Etcd-Index: 10
< X-Raft-Index: 3036
< X-Raft-Term: 20
< Date: Tue, 19 May 2015 21:08:48 GMT
< Content-Length: 173
<
{
    "action": "set",
    "node": {
        "createdIndex": 10,
        "key": "/hello",
        "modifiedIndex": 10,
        "value": "world"
    },
    "prevNode": {
        "createdIndex": 9,
        "key": "/hello",
        "modifiedIndex": 9,
        "value": "world"
    }
}
```

Next, get the value from dev3

```
# On host dev3 (curl progress output removed)
$ curl 192.168.56.102:2379/v2/keys/hello -vv | python -m json.tool
> GET /v2/keys/hello HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 192.168.56.102:2379
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: application/json
< X-Etcd-Cluster-Id: 630f24e186d7d175
< X-Etcd-Index: 10
< X-Raft-Index: 3397
< X-Raft-Term: 20
< Date: Tue, 19 May 2015 21:11:49 GMT
< Content-Length: 94
<
{
    "action": "get",
    "node": {
        "createdIndex": 10,
        "key": "/hello",
        "modifiedIndex": 10,
        "value": "world"
    }
}
```

Etcd provides string based key-value http API, plus event notification. The index (`createdIndex` and `modifiedIndex`) fields are pretty handy. Atomic compare-and-swap is useful to implement cluster-wise concurrency control. Directory listing is also a powerful feature. Etcd provides statics so that you can monitor it or benchmark easily. Here is the [official API guide](https://github.com/coreos/etcd/blob/master/Documentation/api.md).

What if etcd provides bring basic data structures and data types, like redis vs memcached?

  * List, Tree, Map, Set
  * int, string, float, link/reference

About etcd vs zookeeper, [Juha's blog](http://devo.ps/blog/zookeeper-vs-doozer-vs-etcd/), provides a good comparison. I just quote the handy ones:

  * Zookeeper
    * Complex, mature, java, feature-rich
  * Etcd
    * Easy to deploy & use, better security, but young

