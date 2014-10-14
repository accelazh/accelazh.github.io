---
layout: post
title: "Devstack Config & Troubleshooting"
tagline : "Openstack allinone on Ubuntu with Ceilometer"
description: "Openstack allinone on Ubuntu with Ceilometer"
category: "openstack"
tags: [cloud, openstack, devstack]
---
{% include JB/setup %}

*[The blog screwed up markdown format. See better formatted version here.](https://github.com/accelazh/accelazh.github.io/blob/master/_posts/2014-04-1-Devstack-Config-And-Troubleshooting.md)*

Using devstack to install openstack all-in-one on ubuntu should be simple and quick. But there are quite a few pitfalls while using this tool.

Versions
===

I'm installaing openstack stable/havana branch on ubuntu server 12.04. Ceilometer is also installed.

Installation Pitfalls
===

During stack.sh installation:

  * Rabbitmq requires hostname, /etc/hosts and /etc/hostname in consist. Otherwise stack.sh complains on "rabbitmqctl status" command.

  * Devstack/clean.sh can be use to clean all and re-install. But it won't remove git repos under /opt/stack/*.

  * Devstack has havana branch. You must use it if you install openstack in havana branch.

  * Ceilometer-dbsync raises "\_\_init\_\_() got an unexpected keyword argument 'match'" while stack.sh installing. This is because alembic has incorrect version (use pip list to see). alembic should >=0.4.1 and <= 0.6.3, even though ceilometer's requirements.txt only specifies >=0.4.1.

  * Ceilometer should use mongodb rather than mysql. Otherwise horizon /admin/metering raises HTTPInternalServerError. Devstack defaults to use mysql, so you have to add CEILOMETER_BACKEND=mongodb in local.conf.

  * Devstack may install mongodb with lower version than required (>=2.2). Recommend you install 2.2.3.

After stack.sh completes:

  * /etc/nova/nova.conf logging_XXX_suffix/prefix, log_XXX_format_string options contain "%(color)s". It writes control characters into nova log, making reading hard.  
```bash
logging_exception_prefix = %(asctime)s.%(msecs)03d TRACE %(name)s %(instance)s  
logging_debug_format_suffix = (pid=%(process)d) %(funcName)s %(pathname)s:%(lineno)d  
logging_default_format_string = %(asctime)s.%(msecs)03d %(levelname)s %(name)s %(instance)s%(message)s      
logging_context_format_string = %(asctime)s.%(msecs)03d %(levelname)s %(name)s %(request_id)s %(user_name)s %(project_name)s %(instance)s%(message)s  
```

  * Horizon logging, horizon/openstack_dashboard/local/local_settigns.py, set log level to INFO. Change it to DEBUG.

  * Change timezone, so that log has correct timestamp.  
```bash
sudo dpkg-reconfigure tzdata
```

  * Since our developing has added new mysql tables to nova, we need db sync.  
```bash
source ~/workspace/devstack/accrc/admin/admin
nova-manage db sync
sudo ~/stopnova.sh
sleep 2
sudo ~/startnova.sh
```

  * Install **brctl** command if missing. It is needed for set up vm networking. See  
    [http://openstack.redhat.com/forum/discussion/952/problem-creating-instances-no-valid-host/p1]

  * Devstack rejoin-stack.sh will enter "screen" shell. To exit, use ctrl-a-d. See  
    [http://www.ibm.com/developerworks/cn/linux/l-cn-screen/]

  * VM Fusion's VM, after restart, may change IP address. This corrupts Openstack installed on it. To set static IP for VM Fusion's VM, see  
    [http://andrewelkins.com/linux/vmware-fusion-5-set-static-ip-address/]

local.conf
===

This is the local.conf I have been using for devstack:

```bash
[[local|localrc]]
ADMIN_PASSWORD=secrete
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
 
SERVICE_TOKEN=a682f596-76f3-11e3-b3b2-e716f9080d50
 
FIXED_RANGE=172.31.1.0/24
FLOATING_RANGE=192.168.20.0/25
HOST_IP=192.168.255.176
 
DEST=/opt/stack
LOGFILE=$DEST/logs/stack.sh.log
VERBOSE=True
SCREEN_LOGDIR=$DEST/logs/screen
 
SYSLOG=False
RECLONE=yes
LOGDAYS=2
 
GLANCE_BRANCH=stable/havana
HORIZON_BRANCH=stable/havana
KEYSTONE_BRANCH=stable/havana
NOVA_BRANCH=stable/havana
NEUTRON_BRANCH=stable/havana
SWIFT_BRANCH=stable/havana
CEILOMETER_BRANCH=stable/havana
CINDER_BRANCH=stable/havana
 
disable_service cinder c-sch c-api c-vol tempest
 
# Enable swift
enable_service s-proxy s-object s-container s-account
SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
 
# Enable the ceilometer metering services
enable_service ceilometer-acompute ceilometer-acentral ceilometer-anotification ceilometer-collector
# Enable the ceilometer alarming services
enable_service ceilometer-alarm-evaluator,ceilometer-alarm-notifier
# Enable the ceilometer api services
enable_service ceilometer-api
# Don't use mysql or impl_sqlalchemy.py raises NotImplemetedError
CEILOMETER_BACKEND=mongodb
```

Scripts to Start/Stop Nova
===

On default, openstack services (by devstack) log to screen. Devstack write screen log down to /opt/stack/logs/screen/\*. But, by using these scripts, nova log is written to /var/log/nova/\* (**you have to assign the right permission**).

  * Start nova - startnova.sh  
```bash
#!/bin/bash
 
service rabbitmq-server start
sleep 5
 
glance-registry >> /var/log/nova/glance-registry.log 2>&1 &
glance-api >> /var/log/nova/glance-api.log 2>&1 &
keystone-all >> /var/log/keystone/keystone-all.log 2>&1 &
nova-api >> /var/log/nova/nova-api.log 2>&1 &
nova-scheduler >> /var/log/nova/nova-scheduler.log 2>&1 &
nova-wsproxy >> /var/log/nova/nova-wsproxy.log 2>&1 &
nova-network >> /var/log/nova/nova-network.log 2>&1 &
nova-volume >> /var/log/nova/nova-volume.log 2>&1 &
nova-compute >> /var/log/nova/nova-compute.log 2>&1 &
nova-conductor >> /var/log/nova/nova-conductor.log 2>&1 &
sleep 2
 
swift-init --run-dir=/opt/stack/data/swift/run all start
```

  * Stop nova - stopnova.sh  
```bash
#!/bin/bash

swift-init --run-dir=/opt/stack/data/swift/run all stop
sleep 2
kill -9 `ps aux | grep swift | awk '{print $2}'`

kill -9 `ps aux | grep nova-api | awk '{print $2}'`
kill -9 `ps aux | grep nova-scheduler | awk '{print $2}'`
kill -9 `ps aux | grep nova-wsproxy.py | awk '{print $2}'`
kill -9 `ps aux | grep 'nova-' | awk '{print $2}'`
kill -9 `ps aux | grep glance | awk '{print $2}'`
kill -9 `ps aux | grep keystone | awk '{print $2}'`

service rabbitmq-server stop
```

Others Issues
===

  * Horizon, which is django, runs on Apache. After editing code, if without restarting Apache, the code won't be reloaded.

  * Horizon log is at /opt/stack/logs/screen/screen-horizon\*.log and /var/log/apache/horizon\*.log

  * Openstack services log in specific format. Log type is written as "2014-05-16 10:10:30.259 **ERROR** ...". So to grep for errors, you only need to "grep **ERROR**"  
```bash
2014-05-16 10:10:30.259 ERROR nova.openstack.common.rpc.amqp req-2ccfcdc7-540c-4550-8e67-e4f175ceb865 admin demo Exception during message handling
2014-05-16 10:10:30.259 TRACE nova.openstack.common.rpc.amqp Traceback (most recent call last):
2014-05-16 10:10:30.259 TRACE nova.openstack.common.rpc.amqp   File "/opt/stack/nova/nova/openstack/common/rpc/amqp.py", line 461, in _process_data
2014-05-16 10:10:30.259 TRACE nova.openstack.common.rpc.amqp     **args)
...
```

  * If host doesn't have enough memory (free \-m), launch instance can raise ERROR. See  
    [http://openstack.redhat.com/forum/discussion/952/problem-creating-instances-no-valid-host/p1]

  * When VM launch failed in Horizon, few error info is given. However, using nova cli to launch VM usually show more hints.  
    [http://docs.openstack.org/grizzly/basic-install/yum/content/basic-install_operate.html]  
```bash
nova boot --flavor 1 --image <image_id> --key-name default_key my_instance
```

  * Even though my startnova.sh and devstack/rejoin-stack.sh both can launch openstack services. If you run both of them, some services such as nova-scheduler will be started twice, causing trouble.

  * When using startnova.sh, if you first ./startnova.sh, then rm \-rf /var/log/nova/\*. Then nova won't output any logs. So don't remove log files, while nova running.

  * A convenient code snap to restart service for debugging.  
```bash
sudo ~/stopnova.sh
rm -rf /var/log/nova/*
sleep 3
sudo ~/startnova.sh
sleep 5
grep -r ERROR /var/log/nova/*
```

  * Swift on defaut log to /dev/log, i.e. /var/log/syslog
  
  * Remember to open tcp and udp in security group.
  
  * All right, so after all the correct steps, log is the best place to find ERROR.

