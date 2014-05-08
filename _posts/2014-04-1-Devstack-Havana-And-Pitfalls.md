---
layout: post
title: "Devstack Havana & Pitfalls"
tagline : "Openstack allinone on Ubuntu with Ceilometer"
description: "Openstack allinone on Ubuntu with Ceilometer"
category: "openstack"
tags: [cloud, openstack, devstack]
---
{% include JB/setup %}

Using devstack to install openstack all-in-one on ubuntu should be simple and quick. But there are quite a few pitfalls while using this tool.

##Environment

I'm installaing openstack stable/havana branch on ubuntu server 12.04. Ceilometer is also installed. I'm using devstack stable/havana branch.

##Pitfalls

During stack.sh installation:

  1. Rabbitmq requires hostname, /etc/hosts and /etc/hostname in consist. Otherwise stack.sh complains on "rabbitmqctl status" command.
  2. Devstack/clean.sh can be use to clean all and re-install. But it won't remove git repos under /opt/stack/*.
  3. Devstack has havana branch. You must use it if you install openstack in havana branch.
  4. Ceilometer-dbsync raises "_init_\_() got an unexpected keyword argument 'match'" while stack.sh installing. This is because alembic has incorrect version (use pip list to see). alembic should >=0.4.1 and <= 0.6.3, even though ceilometer's requirements.txt only specifies >=0.4.1.
  5. /etc/nova/nova.conf logging_XXX_suffix/prefix, log_XXX_format_string options contain "%(color)s". It writes control characters into nova log, making reading hard.

After stack.sh completes:

  1. Ceilometer should use mongodb rather than mysql. Otherwise horizon /admin/metering raises HTTPInternalServerError. Devstack defaults to use mysql, so you have to add CEILOMETER_BACKEND=mongodb in local.conf.
  2. Devstack may install mongodb with lower version than required (>=2.2). Recommend you install 2.2.3.

##local.conf

This is the local.conf I have been using for devstack:

```bash
[[local|localrc]]
ADMIN_PASSWORD=my_passwd
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

SERVICE_TOKEN=b3822399-66f1-a1ef-c3e2-f726f0140d61

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
SWIFT_HASH=a4c2f6b06e147ade6b4e21ac5f2010a2

# Enable the ceilometer metering services
enable_service ceilometer-acompute ceilometer-acentral ceilometer-anotification ceilometer-collector
# Enable the ceilometer alarming services
enable_service ceilometer-alarm-evaluator,ceilometer-alarm-notifier
# Enable the ceilometer api services
enable_service ceilometer-api
# Don't use mysql or impl_sqlalchemy.py raises NotImplemetedError
CEILOMETER_BACKEND=mongodb
```
