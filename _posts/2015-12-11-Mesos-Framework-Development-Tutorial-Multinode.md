---
layout: post
title: "Mesos Framework Development Tutorial Multinode"
tagline : "Mesos Framework Development Tutorial Multinode"
description: "Mesos Framework Development Tutorial Multinode"
category: "mesos"
tags: [mesos, scheduler, executor]
---
{% include JB/setup %}

### Introduction

Mesos is a popular resource scheduler. Applications on mesos are called "frameworks". They are indeed frameworks which launch tasks and consume resources. Here's the [existing frameworks that can run on Mesos](http://mesos.apache.org/documentation/latest/frameworks/). To allow your framework to run on mesos, here's the [framework developmemt guide](http://mesos.apache.org/documentation/latest/app-framework-development-guide/). Mesos tries to separate task management and resource management.

### Install Mesos Multinode

To install a multinode Mesos cluster, given you already have Openstack, you can use Heat. Openstack Magnum provides the necessary [heat template](https://github.com/openstack/magnum/tree/4b10436393b8d4315ae8e294a5bed92c2e04c298/magnum/templates/mesos). Here is the related [tutorial](http://docs.openstack.org/developer/magnum/dev/dev-heat-mesos.html). A little P.S. here

  * The template doesn't support [Mesos HA](http://mesos.apache.org/documentation/latest/high-availability/) yet. It will always launch only 1 Mesos master.
  * Mesos-master and mesos-slave processes are run as root. This is generally not a good security practice.
  * It requires you to build a dedicated ubuntu-mesos image before start the Heat template. I hope I can launch it directly on a plain Ubuntu 14.04 image.

### Develop Frameworks on Mesos

 A framework would need two parts: scheduler and executor. Besides the official very concise [framework developmemt guide](http://mesos.apache.org/documentation/latest/app-framework-development-guide/), personally I found this [video](https://www.youtube.com/watch?v=n5GT7OFSh58) helpful.

The greatest guide is the [offical mesos framework tutorial](https://github.com/mesosphere/mesos-framework-tutorial). It guides you to spin up a vagrant mesos all-in-one box, write the framework step by step, and run it to watch results. [This commit](https://github.com/mesosphere/mesos-framework-tutorial/tree/bc5da5bb52ad91871fb842e454133fe45d08d319) contains the very skeleton to accept resource offers and launch tasks. A little P.S. here

  * Quickly you will find you need to pool the resource offers received from mesos master, and select the best match of which offer to launch which task. Here's where [Fenzo](http://techblog.netflix.com/2015/08/fenzo-oss-scheduler-for-apache-mesos.html) comes in.

However, this [tutorial](https://github.com/mesosphere/mesos-framework-tutorial) only guides you how to develop framework on a single node all-in-one mesos. How to do that on a multinode mesos cluster?

### Develop Frameworks on Multinode Mesos

In the multinode mesos, mesos slave is not on the same node of mesos master. How does mesos slave gets the executor's executable file? The mesos slave expects to download it from a shared place, e.g. HDFS, HTTP server, etc. You need to pass it the [executor-uri](https://github.com/mesosphere/mesos-framework-tutorial/blob/bc5da5bb52ad91871fb842e454133fe45d08d319/main.go#L119). The downloading is done by [mesos fetcher](http://mesos.apache.org/documentation/latest/fetcher/).

In the [tutorial](https://github.com/mesosphere/mesos-framework-tutorial/tree/bc5da5bb52ad91871fb842e454133fe45d08d319), you will see [code here](https://github.com/mesosphere/mesos-framework-tutorial/blob/bc5da5bb52ad91871fb842e454133fe45d08d319/main.go#L59) launches an http artifact server. That's for mesos slave to download the executor's file. AFAIK, artifact server is a concept just in this tutorial. It is not a concept in mesos.

So what you need to do is

  * Launch a new VM, `test`, where scheduler should be running. It has to be able to connect to mesos master, and mesos master should be able to connect to it. Usually I launch it on the same network of mesos cluster.
  * Copy your scheduler exectuable file and executor executable file to VM `test`.
  * Launch the scheduler by below on VM `test`. (Executor should be launched and managed by mesos.)

```
./example_scheduler --master=<mesos-master-addr>:5050 --executor="<path/to/your/executor/executable/file>" --logtostderr=true --address=<VM-test-addr>
```

By now the scheduler should be running and reporting task running. Executor processes are running on mesos slaves. The key is `--address=<VM-test-addr>`, which the above [tutorial](https://github.com/mesosphere/mesos-framework-tutorial) doesn't tell you. The `--address=<VM-test-addr>` actually does three things, the code couples them together 

  * Which address the http artifact server binds to (and listens on)
  * Which address passed to mesos slave to download executor's executable file (executor-uri)
  * Which address the scheduler binds to and mesos master expects to connect the scheduler

That's all. The [offical mesos framework tutorial](https://github.com/mesosphere/mesos-framework-tutorial) is still very good, except that it should tell more about `--address`. (I once spent a lot of time troubleshooting it). A little more P.S.

  * In the [tutorial](https://github.com/mesosphere/mesos-framework-tutorial) above, the executor is not run in container.
    * You can `ps -ef | grep exec` on the mesos slave, to see the executor is launched by master-slave process with `sh -c`.
    * The executor keeps no matter how many new tasks received, rather than being restarted for every new task.
    * You can `ll /proc/<executor-pid>/ns` to see there is no namespace isolation applied.
    * You can `find /sys/fs/cgroup/ -name <executor-pid>` to see there is no cgroup applied.
    * In a word, there is nothing related to container or docker at all.
      * However, mesos does have containerizers: [mesos containerizer](http://mesos.apache.org/documentation/latest/containerizer/), [docker containerizer](http://mesos.apache.org/documentation/latest/docker-containerizer/), [external containerizer](http://mesos.apache.org/documentation/latest/external-containerizer/). But they are not the case now.

About debugging, you can run mesos-master/mesos-slave with `GLOG_v=2 MESOS_VERBOSE=1` to enable verbose and debug logging. (Never write `GLOG_V`.) For example

```
GLOG_v=2 MESOS_VERBOSE=1 /usr/sbin/mesos-slave --master=zk://10.0.1.12:2181/mesos --log_dir=/var/log/mesos --containerizers=docker,mesos --executor_registration_timeout=5mins --hostname=10.0.1.13 --ip=10.0.1.13
```

