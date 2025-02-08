---
layout: post
title: "Install Devstack Master Branch on CentOS 7"
tagline : "Install Devstack Master Branch on CentOS 7"
description: "Install Devstack Master Branch on CentOS 7"
category: "Openstack"
tags: [openstack, devstack, centos]
---
{% include JB/setup %}

## Environment

Single host with ip 10.224.147.162 and hostname devstack-cinder.novalocal. Install devstack on CentOS 7. 

Using __master branch__ for devstack and all openstack components. Current is 2014-12-5, after stable/juno, before kilo release.

## Installation

First go through my prior post "centos 7 preparation", but don't install pip.

Add local ip and hostname to `/etc/hosts` so devstack can use `hostname -f`

```
echo "
10.224.147.162    $(hostname)
" >> /etc/hosts
```

Download devstack

```
mkdir -p /opt/stack/workspace
cd /opt/stack/workspace
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack
```

Create the user `stack` for devstack

```
cd /opt/stack/workspace/devstack
tools/create-stack-user.sh
chown -R stack:stack /opt/stack
```

Run it again to bypass the empty user in sudoer file [bug](https://bugs.launchpad.net/devstack/+bug/1316326).

```
tools/create-stack-user.sh
cat /etc/sudoers.d/50_stack_sh
```

Create the config file for devstack

```
echo '
[[local|localrc]]
ADMIN_PASSWORD=secrete
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=secrete
RECLONE=no

FIXED_RANGE=192.168.120.0/24
NETWORK_GATEWAY=192.168.120.1
FLOATING_RANGE=10.224.147.224/27
PUBLIC_NETWORK_GATEWAY=10.224.147.225
HOST_IP=10.224.147.162

# misc
API_RATE_LIMIT=False

# log
DEBUG=True
VERBOSE=True
DEST=/opt/stack
LOGFILE=$DEST/logs/stack.sh.log
SCREEN_LOGDIR=$DEST/logs/screen

SYSLOG=False
LOG_COLOR=False
LOGDAYS=7

# enable pre-requisite
enable_service rabbit
enable_service mysql
enable_service key

# keystone
KEYSTONE_CATALOG_BACKEND=sql

# enable ceph (rhel7 doesnt have ceph)
#enable_service ceph
#CEPH_LOOPBACK_DISK_SIZE=10G
#CEPH_CONF=/etc/ceph/ceph.conf
#CEPH_REPLICAS=3
#GLANCE_CEPH_USER=glance
#GLANCE_CEPH_POOL=glance
#CINDER_DRIVER=ceph
#CINDER_CEPH_USER=cinder
#CINDER_CEPH_POOL=cinder
#CINDER_CEPH_UUID=65B06887-B0EA-427F-B8BD-829AC2E18FF6
#CINDER_BAK_CEPH_POOL=cinder_bak
#CINDER_BAK_CEPH_USER=cind_bak
#CINDER_ENABLED_BACKENDS=ceph,lvm
#NOVA_CEPH_POOL=nova

# enable swift
enable_service s-proxy s-object s-container s-account
SWIFT_HASH=E75834B828A54832B8AF2294FD8F5C5D
SWIFT_REPLICAS=3
SWIFT_DATA_DIR=$DEST/data/swift

# cinder
enable_service cinder
enable_service c-api
enable_service c-vol
enable_service c-sch
enable_service c-bak

VOLUME_GROUP="stack-volumes"
VOLUME_NAME_PREFIX="volume-"
VOLUME_BACKING_FILE_SIZE=10250M

# enable neutron
disable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service q-fwaas
enable_service q-lbaas
#enable_service q-vpn
enable_service neutron

# VLAN configuration
Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True

# GRE tunnel configuration
Q_PLUGIN=ml2
ENABLE_TENANT_TUNNELS=True

# VXLAN tunnel configuration
Q_PLUGIN=ml2
Q_ML2_TENANT_NETWORK_TYPE=vxlan   

# enable ceilometer
enable_service ceilometer-acompute
enable_service ceilometer-acentral
enable_service ceilometer-collector
enable_service ceilometer-alarm-singleton
enable_service ceilometer-alarm-notifier
enable_service ceilometer-alarm-evaluator
enable_service ceilometer-api
CEILOMETER_BACKEND=mongodb

# enable heat
enable_service heat
enable_service h-api
enable_service h-api-cfn
enable_service h-api-cw
enable_service h-eng

# enable horizon
enable_service horizon

# enable tempest
enable_service tempest
' > /opt/stack/workspace/devstack/local.conf
chown stack:stack /opt/stack/workspace/devstack/local.conf
```

Start devstack installation

```
su stack
cd /opt/stack/workspace/devstack
./stack.sh
```

To restart devstack, run this beforehand

```
sudo su -
pkill -f python
pkill -f devstack

# to kill devstack screen session
su stack
screen -r
ctrl-a
:quit
```

After devstack intallation succeeded, you will see

```
...
2014-12-15 06:06:08.653 | + SCREEN_NAME=stack
2014-12-15 06:06:08.653 | + SERVICE_DIR=/opt/stack/status
2014-12-15 06:06:08.653 | + [[ ! -d /opt/stack/status/stack ]]
2014-12-15 06:06:08.653 | ++ ls '/opt/stack/status/stack/*.failure'
2014-12-15 06:06:08.655 | ++ /bin/true
2014-12-15 06:06:08.657 | + failures=
2014-12-15 06:06:08.657 | + '[' -n '' ']'



Horizon is now available at http://10.224.147.162/
Keystone is serving at http://10.224.147.162:5000/v2.0/
Examples on using novaclient command line is in exercise.sh
The default users are: admin and demo
The password: secrete
This is your host ip: 10.224.147.162

```

## Verification

Everything seems OK, except VM cannot access outside with associated floating ip. The router is created but with one port to 10.224.147.226. Looks like 10.224.147.226 comes from the external network (named 'public').

```
# neutron net-list
+--------------------------------------+---------+--------------------------------------------------------+
| id                                   | name    | subnets                                                |
+--------------------------------------+---------+--------------------------------------------------------+
| 34f84b53-72a7-46a9-80f3-297933663667 | private | 586e2451-97a4-4c32-839a-e7c4159104a3 192.168.120.0/24  |
| 871fdda5-edd7-42a9-92a1-61947490dd62 | public  | 19ae746c-5c71-467d-bdad-6bb7d924ee2f 10.224.147.224/27 |
+--------------------------------------+---------+--------------------------------------------------------+
$ neutron subnet-list
+--------------------------------------+----------------+-------------------+------------------------------------------------------+
| id                                   | name           | cidr              | allocation_pools                                     |
+--------------------------------------+----------------+-------------------+------------------------------------------------------+
| 586e2451-97a4-4c32-839a-e7c4159104a3 | private-subnet | 192.168.120.0/24  | {"start": "192.168.120.2", "end": "192.168.120.254"} |
| 19ae746c-5c71-467d-bdad-6bb7d924ee2f | public-subnet  | 10.224.147.224/27 | {"start": "10.224.147.226", "end": "10.224.147.254"} |
+--------------------------------------+----------------+-------------------+------------------------------------------------------+
$ neutron net-show public
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | True                                 |
| id                        | 871fdda5-edd7-42a9-92a1-61947490dd62 |
| name                      | public                               |
| provider:network_type     | vxlan                                |
| provider:physical_network |                                      |
| provider:segmentation_id  | 1002                                 |
| router:external           | True                                 |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   | 19ae746c-5c71-467d-bdad-6bb7d924ee2f |
| tenant_id                 | 072105901efc45149cb1b29f468621ff     |
+---------------------------+--------------------------------------+
$ neutron subnet-show public-subnet
+-------------------+------------------------------------------------------+
| Field             | Value                                                |
+-------------------+------------------------------------------------------+
| allocation_pools  | {"start": "10.224.147.226", "end": "10.224.147.254"} |
| cidr              | 10.224.147.224/27                                    |
| dns_nameservers   |                                                      |
| enable_dhcp       | False                                                |
| gateway_ip        | 10.224.147.225                                       |
| host_routes       |                                                      |
| id                | 19ae746c-5c71-467d-bdad-6bb7d924ee2f                 |
| ip_version        | 4                                                    |
| ipv6_address_mode |                                                      |
| ipv6_ra_mode      |                                                      |
| name              | public-subnet                                        |
| network_id        | 871fdda5-edd7-42a9-92a1-61947490dd62                 |
| tenant_id         | 072105901efc45149cb1b29f468621ff                     |
+-------------------+------------------------------------------------------+
```

The speed is really slow. My host 10.224.147.162 is a VM of 'm1.large | 8GB RAM | 4 VCPU | 80.0GB Disk'. Looks like I have launched too much services.

## Troubleshooting

Below I record my troubleshootings. Quite a __lot__ of error when installing devstack.

### Error `yum install -y openvswitch` no package found. 

The log trace

```
Loading mirror speeds from cached hostfile
2014-12-10 01:19:03.427 |  * base: mirror.lax.hugeserver.com
2014-12-10 01:19:03.427 |  * epel: mirror.premi.st
2014-12-10 01:19:03.427 |  * extras: mirror.fdcservers.net
2014-12-10 01:19:03.427 |  * updates: mirror.lax.hugeserver.com
2014-12-10 01:19:03.427 | No package openvswitch available.
2014-12-10 01:19:03.427 | Error: Nothing to do
2014-12-10 01:19:03.427 | + die 1195 'Missing packages detected'
2014-12-10 01:19:03.427 | + local exitcode=1
2014-12-10 01:19:03.427 | [Call Trace]
2014-12-10 01:19:03.427 | ./stack.sh:728:install_neutron_agent_packages
2014-12-10 01:19:03.427 | /opt/stack/workspace/devstack/lib/neutron:636:neutron_plugin_install_agent_packages
2014-12-10 01:19:03.427 | /opt/stack/workspace/devstack/lib/neutron_plugins/openvswitch_agent:21:_neutron_ovs_base_install_agent_packages
2014-12-10 01:19:03.427 | /opt/stack/workspace/devstack/lib/neutron_plugins/ovs_base:51:install_package
2014-12-10 01:19:03.427 | /opt/stack/workspace/devstack/functions-common:1139:real_install_package
2014-12-10 01:19:03.427 | /opt/stack/workspace/devstack/functions-common:1127:yum_install
2014-12-10 01:19:03.427 | /opt/stack/workspace/devstack/functions-common:1195:die
2014-12-10 01:19:03.430 | [ERROR] /opt/stack/workspace/devstack/functions-common:1195 Missing packages detected
2014-12-10 01:19:04.432 | Error on exit
```

Try borrow the  openvswitch from RDO repo. Then reinstall devstack

```
cd ~
wget https://repos.fedorapeople.org/repos/openstack/openstack-juno/rdo-release-juno-1.noarch.rpm
yum install -y rdo-release-juno-1.noarch.rpm
yum install -y openvswitch openvswitch-devel python-openvswitch
yum remove -y rdo-release-juno-1.noarch
```

### Error `keystone token-get` fail

Try below on my machine

```
$ export OS_USERNAME=admin
$ export OS_PASSWORD=secrete
$ export OS_TENANT_NAME=admin
$ export OS_AUTH_URL=http://10.224.147.162:35357/v2.0
$ keystone user-list
Expecting a token provided via either --os-token or env[OS_SERVICE_TOKEN]
```

This is weird. About should succeed and output user list, the correct user credential given.

After I logout and login back user `stack`, above fixed itself and printed the output. Maybe it is because last time I run devstack in `screen`. Let's run devstack without it.

### Error Neutron lbaas plugin fail to load

Neutron log by devstack

```
2014-12-10 07:50:34.678 20655 INFO neutron.manager [-] Loading Plugin: neutron.services.loadbalancer.plugin.LoadBalancerPlugin
2014-12-10 07:50:34.678 20655 ERROR neutron.manager [-] Error loading plugin by name, No 'neutron.service_plugins' driver found, looking for 'neutron.services.loadbalancer.plugin.LoadBalancerPlugin'
2014-12-10 07:50:34.678 20655 TRACE neutron.manager Traceback (most recent call last):
2014-12-10 07:50:34.678 20655 TRACE neutron.manager   File "/opt/stack/neutron/neutron/manager.py", line 135, in _get_plugin_instance
2014-12-10 07:50:34.678 20655 TRACE neutron.manager     plugin_class = importutils.import_class(plugin_provider)
2014-12-10 07:50:34.678 20655 TRACE neutron.manager   File "/usr/lib/python2.7/site-packages/oslo/utils/importutils.py", line 27, in import_class
2014-12-10 07:50:34.678 20655 TRACE neutron.manager     __import__(mod_str)
2014-12-10 07:50:34.678 20655 TRACE neutron.manager ImportError: No module named plugin
```

I login to github neutron and find that neutron/services/loadbalancer/plugin.py is gone on master branch. It is still there in stable/juno. Check commit history, it is delete by [Split services code out of Neutron, pass 1](https://github.com/openstack/neutron/commit/407ee801e3f4a9f489062c1446ba128d25da6db5), __2 days ago__. Core developers are doing big refactor on neutron services. Let's use stable/juno branch instead.

```
cd /opt/stack/neutron
git checkout stable/juno
```

Restart devstack now.

### Error yum repo timeout

Error log here

```
http://mirror.nexcess.net/epel/7/x86_64/repodata/repomd.xml: [Errno 12] Timeout on http://mirror.nexcess.net/epel/7/x86_64/repodata/repomd.xml: (28, 'Operation too slow. Less than 1000 bytes/sec transferred the last 30 seconds')
Trying other mirror.
```

This is because my local network become slow sometime. Modify /etc/yum.conf and restart devstack.

```
echo '
# default is 30
timeout=300
# default is 1000
minrate=100' >> /etc/yum.conf
```

### Error neutron subnet create: Gateway is not valid on subnet

Error log of devstack

```
2014-12-10 10:22:09.902 | ++ _neutron_create_private_subnet_v4
2014-12-10 10:22:09.902 | ++ local 'subnet_params=--tenant-id 31ec33077d7744728af49b2748145dc1 '
2014-12-10 10:22:09.902 | ++ subnet_params+='--ip_version 4 '
2014-12-10 10:22:09.902 | ++ subnet_params+='--gateway 10.0.0.1 '
2014-12-10 10:22:09.902 | ++ subnet_params+='--name private-subnet '
2014-12-10 10:22:09.902 | ++ subnet_params+='93cd58ec-99ca-490f-ade4-b44c100344f9 192.168.120.0/24'
2014-12-10 10:22:09.903 | +++ neutron subnet-create --tenant-id 31ec33077d7744728af49b2748145dc1 --ip_version 4 --gateway 10.0.0.1 --name private-subnet 93cd58ec-99ca-490f-ade4-b44c100344f9 192.168.120.0/24
2014-12-10 10:22:09.903 | +++ grep ' id '
2014-12-10 10:22:09.903 | +++ get_field 2
2014-12-10 10:22:09.904 | +++ local data field
2014-12-10 10:22:09.904 | +++ read data
2014-12-10 10:22:10.921 | Bad Request (HTTP 400) (Request-ID: req-45b0cf8b-1c2c-440f-bd70-2db2b3775f92)
2014-12-10 10:22:10.957 | ++ local subnet_id=
2014-12-10 10:22:10.957 | ++ die_if_not_set 1074 subnet_id 'Failure creating private IPv4 subnet for 31ec33077d7744728af49b2748145dc1'
2014-12-10 10:22:10.957 | ++ local exitcode=0
2014-12-10 10:22:10.963 | [ERROR] /opt/stack/workspace/devstack/functions-common:1074 Failure creating private IPv4 subnet for 31ec33077d7744728af49b2748145dc1
```

The command that raised error 

```
neutron subnet-create --tenant-id 31ec33077d7744728af49b2748145dc1 --ip_version 4 --gateway 10.0.0.1 --name private-subnet 93cd58ec-99ca-490f-ade4-b44c100344f9 192.168.120.0/24
```

Log from neutron server

```
2014-12-10 10:48:20.212 9042 DEBUG neutron.policy [req-0a16f579-ceec-4c5a-a03a-0e21683cac00 None] Enforcing rules: ['create_subnet'] _build_match_rule /opt/stack/neutron/neutron/policy.py:221
2014-12-10 10:48:20.223 9042 INFO neutron.api.v2.resource [req-0a16f579-ceec-4c5a-a03a-0e21683cac00 None] create failed (client error): Invalid input for operation: Gateway is not valid on subnet.
2014-12-10 10:48:20.226 9042 INFO neutron.wsgi [req-0a16f579-ceec-4c5a-a03a-0e21683cac00 None] 10.224.147.162 - - [10/Dec/2014 10:48:20] "POST /v2.0/subnets.json HTTP/1.1" 400 354 0.025684
2014-12-10 10:48:26.790 9042 DEBUG neutron.context [req-39f06a35-b58a-4523-984d-78dc92647eb7 None] Arguments dropped when creating context: {u'project_name': None, u'tenant': None} __init__ /opt/stack/neutron/neutron/context.py:83
```

Seems the gateway ip `10.0.0.1` is improper for subnet range `192.168.120.0/24`. Solution is to set `NETWORK_GATEWAY` option in local.conf. (Fixed in prior local.conf section.)

### Error neutron router-gateway-set: No IPs available for external network

Related devstack log

```
2014-12-10 11:56:20.938 | + neutron router-gateway-set 4d27233b-0e0e-4b63-b0ab-c7716f7caac7 85ce5945-7139-4b4d-a6f7-1f7a1dd68f5c
2014-12-10 11:56:22.118 | Bad Request (HTTP 400) (Request-ID: req-d7afa05b-4108-465f-a0f9-4801700237ce)
```

Related neutron server log

```
2014-12-10 13:06:41.512 19938 INFO neutron.api.v2.resource [req-d97f26ef-598d-4030-879e-8cecc0a6ab2e None] update failed (client error): Bad router request: No IPs available for external network 85ce5945-7139-4b4d-a6f7-1f7a1dd68f5c
```

Using `neutron net-show 85ce5945-7139-4b4d-a6f7-1f7a1dd68f5c`, looks like our external network doesn't have subnet. So cannot allocate ip. Found below in prior place of devstack log

```
2014-12-10 11:56:18.873 | ++ _neutron_create_public_subnet_v4 85ce5945-7139-4b4d-a6f7-1f7a1dd68f5c
2014-12-10 11:56:18.873 | ++ local 'subnet_params+=--ip_version 4 '
2014-12-10 11:56:18.873 | ++ subnet_params+=' '
2014-12-10 11:56:18.873 | ++ subnet_params+='--gateway 172.24.4.1 '
2014-12-10 11:56:18.873 | ++ subnet_params+='--name public-subnet '
2014-12-10 11:56:18.873 | ++ subnet_params+='85ce5945-7139-4b4d-a6f7-1f7a1dd68f5c 10.224.147.224/27 '
2014-12-10 11:56:18.874 | ++ subnet_params+='-- --enable_dhcp=False'
2014-12-10 11:56:18.875 | +++ neutron subnet-create --ip_version 4 --gateway 172.24.4.1 --name public-subnet 85ce5945-7139-4b4d-a6f7-1f7a1dd68f5c 10.224.147.224/27 -- --enable_dhcp=False
2014-12-10 11:56:18.875 | +++ grep -e gateway_ip -e ' id '
2014-12-10 11:56:19.882 | Bad Request (HTTP 400) (Request-ID: req-2d84c78d-c6c8-4ef1-9237-478476abc983)
```

Corresponding neutron server log

```
2014-12-10 13:11:17.595 19938 DEBUG neutron.policy [req-edb49181-f6d6-4f12-8ef6-e0a1372d1588 None] Enforcing rules: ['create_subnet'] _build_match_rule /opt/stack/neutron/neutron/policy.py:221
2014-12-10 13:11:17.607 19938 INFO neutron.api.v2.resource [req-edb49181-f6d6-4f12-8ef6-e0a1372d1588 None] create failed (client error): Invalid input for operation: Gateway is not valid on subnet.
2014-12-10 13:11:17.610 19938 INFO neutron.wsgi [req-edb49181-f6d6-4f12-8ef6-e0a1372d1588 None] 10.224.147.162 - - [10/Dec/2014 13:11:17] "POST /v2.0/subnets.json HTTP/1.1" 400 354 0.026341
```

Where does the ip `172.24.4.1` come? And the `subnet_params+='--gateway 172.24.4.1 '`. Trace in devstack source code, found

```
function _neutron_create_public_subnet_v4 {
    local subnet_params+="--ip_version 4 "
    subnet_params+="${Q_FLOATING_ALLOCATION_POOL:+--allocation-pool $Q_FLOATING_ALLOCATION_POOL} "
    subnet_params+="--gateway $PUBLIC_NETWORK_GATEWAY "
    subnet_params+="--name $PUBLIC_SUBNET_NAME "
    subnet_params+="$EXT_NET_ID $FLOATING_RANGE "
    subnet_params+="-- --enable_dhcp=False"
    local id_and_ext_gw_ip=$(neutron subnet-create $subnet_params | grep -e 'gateway_ip' -e ' id ')
    die_if_not_set $LINENO id_and_ext_gw_ip "Failure creating public IPv4 subnet"
    echo $id_and_ext_gw_ip
}
```

Let's add `PUBLIC_NETWORK_GATEWAY` to local.conf.

### Error openstack image create bad request: Client disconnected before sending all data to backend

Devstack log trace

```
2014-12-13 16:55:50.094 | + local kernel_id= ramdisk_id=
2014-12-13 16:55:50.094 | + '[' -n /opt/stack/workspace/devstack/files/images/cirros-0.3.2-x86_64-uec/cirros-0.3.2-x86_64-vmlinuz ']'
2014-12-13 16:55:50.095 | ++ openstack --os-token edb5e9cab3e1427d8e8def0cccdf546f --os-url http://10.224.147.162:9292 image create cirros-0.3.2-x86_64-uec-kernel --public --container-format aki --disk-
format aki
2014-12-13 16:55:50.095 | ++ grep ' id '
2014-12-13 16:55:50.095 | ++ get_field 2
2014-12-13 16:55:50.095 | ++ local data field
2014-12-13 16:55:50.095 | ++ read data
2014-12-13 16:56:25.482 | ERROR: openstack <html>
2014-12-13 16:56:25.483 |  <head>
2014-12-13 16:56:25.483 |   <title>400 Bad Request</title>
2014-12-13 16:56:25.483 |  </head>
2014-12-13 16:56:25.483 |  <body>
2014-12-13 16:56:25.483 |   <h1>400 Bad Request</h1>
2014-12-13 16:56:25.483 |   Client disconnected before sending all data to backend<br /><br />
2014-12-13 16:56:25.483 | 
2014-12-13 16:56:25.483 |  </body>
2014-12-13 16:56:25.483 | </html> (HTTP 400)
```

Independent run of the error command under user `stack`

```
$ openstack --os-token edb5e9cab3e1427d8e8def0cccdf546f --os-url http://10.224.147.162:9292 image create cirros-0.3.2-x86_64-uec-kernel --public --container-format aki --disk-format aki < /opt/stack/workspace/devstack/files/images/cirros-0.3.2-x86_64-uec/cirros-0.3.2-x86_64-vmlinuz
ERROR: openstack <html>
 <head>
  <title>400 Bad Request</title>
 </head>
 <body>
  <h1>400 Bad Request</h1>
  Client disconnected before sending all data to backend<br /><br />

 </body>
</html> (HTTP 400)
```

The glance-api log

```
2014-12-13 17:11:52.014 15136 DEBUG glance.common.client [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Constructed URL: http://0.0.0.0:91
91/images/79224872-4fe9-4a16-a519-416e6f82138a _construct_url /opt/stack/glance/glance/common/client.py:400
2014-12-13 17:11:52.154 15136 DEBUG glance.registry.client.v1.client [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Registry request PUT /
images/79224872-4fe9-4a16-a519-416e6f82138a HTTP 200 request id req-5461c041-428a-4052-bf13-387936ebf62c do_request /opt/stack/glance/glance/registry/client/v1/client.py:124
2014-12-13 17:11:52.155 15136 DEBUG glance.api.v1.images [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Uploading image data for image 792
24872-4fe9-4a16-a519-416e6f82138a to swift store _upload /opt/stack/glance/glance/api/v1/images.py:630
2014-12-13 17:11:52.160 15136 DEBUG keystoneclient.auth.identity.v2 [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Making authentication r
equest to http://10.224.147.162:5000/v2.0/tokens get_auth_ref /usr/lib/python2.7/site-packages/keystoneclient/auth/identity/v2.py:77
2014-12-13 17:12:23.317 15136 ERROR swiftclient [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] ('Connection aborted.', error(111, 'ECONNRE
FUSED'))
2014-12-13 17:12:23.317 15136 TRACE swiftclient Traceback (most recent call last):
2014-12-13 17:12:23.317 15136 TRACE swiftclient   File "/usr/lib/python2.7/site-packages/swiftclient/client.py", line 1243, in _retry
2014-12-13 17:12:23.317 15136 TRACE swiftclient     rv = func(self.url, self.token, *args, **kwargs)
2014-12-13 17:12:23.317 15136 TRACE swiftclient   File "/usr/lib/python2.7/site-packages/swiftclient/client.py", line 674, in head_container
2014-12-13 17:12:23.317 15136 TRACE swiftclient     conn.request(method, path, '', req_headers)
2014-12-13 17:12:23.317 15136 TRACE swiftclient   File "/usr/lib/python2.7/site-packages/swiftclient/client.py", line 217, in request
2014-12-13 17:12:23.317 15136 TRACE swiftclient     files=files, **self.requests_args)
2014-12-13 17:12:23.317 15136 TRACE swiftclient   File "/usr/lib/python2.7/site-packages/swiftclient/client.py", line 185, in _request
2014-12-13 17:12:23.317 15136 TRACE swiftclient     return self.request_session.request(*arg, **kwarg)
2014-12-13 17:12:23.317 15136 TRACE swiftclient   File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 461, in request
2014-12-13 17:12:23.317 15136 TRACE swiftclient     resp = self.send(prep, **send_kwargs)
2014-12-13 17:12:23.317 15136 TRACE swiftclient   File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 573, in send
2014-12-13 17:12:23.317 15136 TRACE swiftclient     r = adapter.send(request, **kwargs)
2014-12-13 17:12:23.317 15136 TRACE swiftclient   File "/usr/lib/python2.7/site-packages/requests/adapters.py", line 415, in send
2014-12-13 17:12:23.317 15136 TRACE swiftclient     raise ConnectionError(err, request=request)
2014-12-13 17:12:23.317 15136 TRACE swiftclient ConnectionError: ('Connection aborted.', error(111, 'ECONNREFUSED'))
2014-12-13 17:12:23.317 15136 TRACE swiftclient
2014-12-13 17:12:23.317 15136 WARNING glance.api.v1.upload_utils [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Client disconnected before sending all data to backend
2014-12-13 17:12:23.318 15136 DEBUG glance.registry.client.v1.api [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Updating image metadata for image 79224872-4fe9-4a16-a519-416e6f82138a... update_image_metadata /opt/stack/glance/glance/registry/client/v1/api.py:168
2014-12-13 17:12:23.318 15136 DEBUG glance.common.client [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Constructed URL: http://0.0.0.0:9191/images/79224872-4fe9-4a16-a519-416e6f82138a _construct_url /opt/stack/glance/glance/common/client.py:400
2014-12-13 17:12:23.410 15136 DEBUG glance.registry.client.v1.client [7f95a712-d24a-4412-8f16-10545fd0c22e 70f9aa2374644424a3ba33f83c25d594 43dd1d1beb1e40959a051d9b827bcaa8 - - -] Registry request PUT /images/79224872-4fe9-4a16-a519-416e6f82138a HTTP 200 request id req-baf1b5fb-c97b-4279-9fdd-580de3e5522e do_request /opt/stack/glance/glance/registry/client/v1/client.py:124
2014-12-13 17:12:23.435 15136 INFO eventlet.wsgi.server [-] 10.224.147.162 - - [13/Dec/2014 17:12:23] "POST /v1/images HTTP/1.1" 400 396 31.553426
10.224.147.162 - - [13/Dec/2014 17:12:23] code 400, message Bad request syntax ('0')
10.224.147.162 - - [13/Dec/2014 17:12:23] "0" 400 -
Traceback (most recent call last):
  File "/usr/lib/python2.7/site-packages/eventlet/greenpool.py", line 82, in _spawn_n_impl
    func(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/eventlet/wsgi.py", line 661, in process_request
    proto.__init__(sock, address, self)
  File "/usr/lib64/python2.7/SocketServer.py", line 649, in __init__
    self.handle()
  File "/usr/lib64/python2.7/BaseHTTPServer.py", line 342, in handle
    self.handle_one_request()
  File "/usr/lib/python2.7/site-packages/eventlet/wsgi.py", line 288, in handle_one_request
    if not self.parse_request():
  File "/usr/lib64/python2.7/BaseHTTPServer.py", line 286, in parse_request
    self.send_error(400, "Bad request syntax (%r)" % requestline)
  File "/usr/lib64/python2.7/BaseHTTPServer.py", line 368, in send_error
    self.send_response(code, message)
  File "/usr/lib64/python2.7/BaseHTTPServer.py", line 395, in send_response
    self.send_header('Server', self.version_string())
  File "/usr/lib64/python2.7/BaseHTTPServer.py", line 401, in send_header
    self.wfile.write("%s: %s\r\n" % (keyword, value))
  File "/usr/lib64/python2.7/socket.py", line 324, in write
    self.flush()
  File "/usr/lib64/python2.7/socket.py", line 303, in flush
    self._sock.sendall(view[write_offset:write_offset+buffer_size])
  File "/usr/lib/python2.7/site-packages/eventlet/greenio.py", line 359, in sendall
    tail = self.send(data, flags)
  File "/usr/lib/python2.7/site-packages/eventlet/greenio.py", line 342, in send
    total_sent += fd.send(data[total_sent:], flags)
error: [Errno 32] Broken pipe
```

Swiftclient reports error 'Connection aborted'. Swift proxy is not running. Check log in s-proxy of devstack's screen

```
 /opt/stack/swift/bin/swift-proxy-server /etc/swift/proxy-server.conf -v & echo $! >/opt/stack/status/stack/s-proxy.pid; fg || echo "s-proxy failed to start" | tee "/opt/stack/status/stack/s-proxy.failure"
[1] 15058
/opt/stack/swift/bin/swift-proxy-server /etc/swift/proxy-server.conf -v
Traceback (most recent call last):
  File "/opt/stack/swift/bin/swift-proxy-server", line 23, in <module>
    sys.exit(run_wsgi(conf_file, 'proxy-server', **options))
  File "/opt/stack/swift/swift/common/wsgi.py", line 445, in run_wsgi
    loadapp(conf_path, global_conf=global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 354, in loadapp
    ctx = loadcontext(loadwsgi.APP, conf_file, global_conf=global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 338, in loadcontext
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 296, in loadcontext
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 320, in _loadconfig
    return loader.get_context(object_type, name, global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 61, in get_context
    object_type, name=name, global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 450, in get_context
    global_additions=global_additions)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 562, in _pipeline_app_context
    for name in pipeline[:-1]]
  File "/opt/stack/swift/swift/common/wsgi.py", line 61, in get_context
    object_type, name=name, global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 454, in get_context
    section)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 476, in _context_from_use
    object_type, name=use, global_conf=global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 61, in get_context
    object_type, name=name, global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 406, in get_context
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 296, in loadcontext
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 328, in _loadegg
    return loader.get_context(object_type, name, global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 620, in get_context
    object_type, name=name)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 640, in find_egg_entry_point
    pkg_resources.require(self.spec)
  File "/usr/lib/python2.7/site-packages/pkg_resources.py", line 750, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/usr/lib/python2.7/site-packages/pkg_resources.py", line 641, in resolve
    raise VersionConflict(tmpl % args)
pkg_resources.VersionConflict: SQLAlchemy 0.9.7 is installed but SQLAlchemy<=0.8.99,<=0.9.99,>=0.8.4,>=0.9.7 is required by ['oslo.db']
s-proxy failed to start
```

Strange version conflict exists in oslo.db: `SQLAlchemy>=0.8.4,<=0.8.99,>=0.9.7,<=0.9.99`. Also [neutron stable/juno requirements.txt](https://github.com/openstack/neutron/blob/stable/juno/requirements.txt) and [oslo.db stable/juno requirements.txt] have this problem. Master branch doesn't have this.

```
$ grep -ir SQLAlchemy /usr/lib/python2.7/site-packages/oslo.db*
...
/usr/lib/python2.7/site-packages/oslo.db-1.2.0.dist-info/METADATA:Requires-Dist: SQLAlchemy (>=0.8.4,<=0.8.99,>=0.9.7,<=0.9.99)
...
```

I'm afraid this is caused by that neutron stable/juno other openstack components in master branch requires different version of oslo.db

```
vim /usr/lib/python2.7/site-packages/oslo.db-1.2.0.dist-info/METADATA
# change SQLAlchemy version requirements line
Requires-Dist: SQLAlchemy (>=0.9.7,<=0.9.99)
```

Similar error exists in other places

```
$ /opt/stack/swift/bin/swift-proxy-server /etc/swift/proxy-server.conf -v & echo $! >/opt/stack/status/stack/s-proxy.pid; fg || echo "s-proxy failed to start" | tee "/opt/stack/status/stack/s-proxy.failure"
[1] 3194
/opt/stack/swift/bin/swift-proxy-server /etc/swift/proxy-server.conf -v
Traceback (most recent call last):
  File "/opt/stack/swift/bin/swift-proxy-server", line 23, in <module>
    sys.exit(run_wsgi(conf_file, 'proxy-server', **options))
  File "/opt/stack/swift/swift/common/wsgi.py", line 445, in run_wsgi
    loadapp(conf_path, global_conf=global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 354, in loadapp
    ctx = loadcontext(loadwsgi.APP, conf_file, global_conf=global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 338, in loadcontext
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 296, in loadcontext
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 320, in _loadconfig
    return loader.get_context(object_type, name, global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 61, in get_context
    object_type, name=name, global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 450, in get_context
    global_additions=global_additions)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 562, in _pipeline_app_context
    for name in pipeline[:-1]]
  File "/opt/stack/swift/swift/common/wsgi.py", line 61, in get_context
    object_type, name=name, global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 454, in get_context
    section)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 476, in _context_from_use
    object_type, name=use, global_conf=global_conf)
  File "/opt/stack/swift/swift/common/wsgi.py", line 61, in get_context
    object_type, name=name, global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 406, in get_context
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 296, in loadcontext
    global_conf=global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 328, in _loadegg
    return loader.get_context(object_type, name, global_conf)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 620, in get_context
    object_type, name=name)
  File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 640, in find_egg_entry_point
    pkg_resources.require(self.spec)
  File "/usr/lib/python2.7/site-packages/pkg_resources.py", line 817, in require
    needed = self.resolve(parse_requirements(requirements))
  File "/usr/lib/python2.7/site-packages/pkg_resources.py", line 708, in resolve
    raise VersionConflict(tmpl % args)
pkg_resources.VersionConflict: SQLAlchemy 0.9.8 is installed but SQLAlchemy<=0.8.99,<=0.9.99,>=0.8.4,>=0.9.7 is required by ['ceilometer']
s-proxy failed to start
```

Change the version conflict of ceilometer

```
$ grep -r SQLAlchemy /opt/stack/ceilometer
...
/opt/stack/ceilometer/ceilometer.egg-info/requires.txt:SQLAlchemy>=0.8.4,<=0.8.99,>=0.9.7,<=0.9.99
...

vim /opt/stack/ceilometer/ceilometer.egg-info/requires.txt 
# change SQLAlchemy version requirements line
SQLAlchemy>=0.9.7,<=0.9.99

vim /opt/stack/ceilometer/requirements.txt 
# change SQLAlchemy version requirements line
SQLAlchemy>=0.9.7,<=0.9.99
```

Re-run `/opt/stack/swift/bin/swift-proxy-server /etc/swift/proxy-server.conf -v` under user 'stack', it works now. Re-install devstack.

### Error neutron create public subnet: Gateway is not valid on subnet

```
2014-12-13 18:16:51.827 | ++ _neutron_create_public_subnet_v4 cc8748ce-699d-46f6-b620-5db634a98b73
2014-12-13 18:16:51.827 | ++ local 'subnet_params+=--ip_version 4 '
2014-12-13 18:16:51.827 | ++ subnet_params+=' '
2014-12-13 18:16:51.827 | ++ subnet_params+='--gateway 10.224.147.1 '
2014-12-13 18:16:51.827 | ++ subnet_params+='--name public-subnet '
2014-12-13 18:16:51.828 | ++ subnet_params+='cc8748ce-699d-46f6-b620-5db634a98b73 10.224.147.224/27 '
2014-12-13 18:16:51.828 | ++ subnet_params+='-- --enable_dhcp=False'
2014-12-13 18:16:51.829 | +++ neutron subnet-create --ip_version 4 --gateway 10.224.147.1 --name public-subnet cc8748ce-699d-46f6-b620-5db634a98b73 10.224.147.224/27 -- --enable_dhcp=False
2014-12-13 18:16:51.829 | +++ grep -e gateway_ip -e ' id '
2014-12-13 18:16:52.970 | Bad Request (HTTP 400) (Request-ID: req-df5fd12c-8944-4093-a9dc-0dabca351108)
2014-12-13 18:16:53.018 | ++ local id_and_ext_gw_ip=
2014-12-13 18:16:53.018 | ++ die_if_not_set 1102 id_and_ext_gw_ip 'Failure creating public IPv4 subnet'
2014-12-13 18:16:53.018 | ++ local exitcode=0
2014-12-13 18:16:53.023 | [ERROR] /opt/stack/workspace/devstack/functions-common:1102 Failure creating public IPv4 subnet
```

Run this command indenpendently

```
$ neutron subnet-create --ip_version 4 --gateway 10.224.147.1 --name public-subnet cc8748ce-699d-46f6-b620-5db634a98b73 10.224.147.224/27 -- --enable_dhcp=False
Bad Request (HTTP 400) (Request-ID: req-274d8b4b-8aeb-4a26-bce9-5d6e3f53ab1e)
```

Relevant neutron server log

```
2014-12-14 02:38:20.760 539 INFO neutron.api.v2.resource [req-fd3d5092-c21c-470b-9087-9299dff1917e None] create failed (client error): Invalid input for operation: Gateway is not valid on subnet.
```

This is because I'm using 10.224.147.1 as gateway address, which is out of range on 10.224.147.224/27. Change `PUBLIC_NETWORK_GATEWAY` in local.conf. Reinstall devstasck.

### Error ceilometer-api failed to start

Devstack log trace

```
2014-12-14 03:12:31.118 | + echo 'Waiting for ceilometer-api to start...'
2014-12-14 03:12:31.118 | Waiting for ceilometer-api to start...
2014-12-14 03:12:31.119 | + timeout 60 sh -c 'while ! curl --noproxy '\''*'\'' -s http://localhost:8777/v2/ >/dev/null; do sleep 1; done'
2014-12-14 03:13:31.120 | + die 331 'ceilometer-api did not start'
2014-12-14 03:13:31.120 | + local exitcode=0
2014-12-14 03:13:31.120 | [Call Trace]
2014-12-14 03:13:31.121 | ./stack.sh:1268:start_ceilometer
2014-12-14 03:13:31.121 | /opt/stack/workspace/devstack/lib/ceilometer:331:die
2014-12-14 03:13:31.124 | [ERROR] /opt/stack/workspace/devstack/lib/ceilometer:331 ceilometer-api did not start
```

Ceilometer api log

```
2014-12-14 03:13:59.603 9644 DEBUG ceilometer.storage [-] looking for 'mongodb' driver in 'ceilometer.metering.storage' get_connection /opt/stack/ceilometer/ceilometer/storage/__init__.py:112
2014-12-14 03:13:59.604 9644 INFO ceilometer.storage.mongo.utils [-] Connecting to mongodb on [('localhost', 27017)]
2014-12-14 03:13:59.605 9644 WARNING ceilometer.storage.mongo.utils [-] Unable to connect to the database server: could not connect to localhost:27017: [Errno -9] Address family for hostname not support
ed.
2014-12-14 03:13:59.605 9644 CRITICAL ceilometer [-] ConnectionFailure: could not connect to localhost:27017: [Errno -9] Address family for hostname not supported
2014-12-14 03:13:59.605 9644 TRACE ceilometer Traceback (most recent call last):
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/bin/ceilometer-api", line 10, in <module>
2014-12-14 03:13:59.605 9644 TRACE ceilometer     sys.exit(main())
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/cmd/api.py", line 23, in main
2014-12-14 03:13:59.605 9644 TRACE ceilometer     srv = app.build_server()
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/api/app.py", line 160, in build_server
2014-12-14 03:13:59.605 9644 TRACE ceilometer     app = load_app()
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/api/app.py", line 156, in load_app
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return deploy.loadapp("config:" + cfg_file)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 247, in loadapp
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return loadobj(APP, uri, name=name, **kw)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 272, in loadobj
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return context.create()
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 710, in create
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return self.object_type.invoke(self)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 203, in invoke
2014-12-14 03:13:59.605 9644 TRACE ceilometer     app = context.app_context.create()
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 710, in create
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return self.object_type.invoke(self)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py", line 146, in invoke
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return fix_call(context.object, context.global_conf, **context.local_conf)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/paste/deploy/util.py", line 56, in fix_call
2014-12-14 03:13:59.605 9644 TRACE ceilometer     val = callable(*args, **kw)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/api/app.py", line 184, in app_factory
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return VersionSelectorApplication()
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/api/app.py", line 106, in __init__
2014-12-14 03:13:59.605 9644 TRACE ceilometer     self.v2 = setup_app(pecan_config=pc)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/api/app.py", line 69, in setup_app
2014-12-14 03:13:59.605 9644 TRACE ceilometer     storage.get_connection_from_config(cfg.CONF, 'metering'),
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/retrying.py", line 49, in wrapped_f
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return Retrying(*dargs, **dkw).call(f, *args, **kw)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/retrying.py", line 212, in call
2014-12-14 03:13:59.605 9644 TRACE ceilometer     raise attempt.get()
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/retrying.py", line 247, in get
2014-12-14 03:13:59.605 9644 TRACE ceilometer     six.reraise(self.value[0], self.value[1], self.value[2])
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib/python2.7/site-packages/retrying.py", line 200, in call
2014-12-14 03:13:59.605 9644 TRACE ceilometer     attempt = Attempt(fn(*args, **kwargs), attempt_number, False)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/storage/__init__.py", line 102, in get_connection_from_config
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return get_connection(url, namespace)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/storage/__init__.py", line 114, in get_connection
2014-12-14 03:13:59.605 9644 TRACE ceilometer     return mgr.driver(url)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/storage/impl_mongodb.py", line 396, in __init__
2014-12-14 03:13:59.605 9644 TRACE ceilometer     self.conn = self.CONNECTION_POOL.connect(url)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/storage/mongo/utils.py", line 247, in connect
2014-12-14 03:13:59.605 9644 TRACE ceilometer     client = self._mongo_connect(url)
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/opt/stack/ceilometer/ceilometer/storage/mongo/utils.py", line 261, in _mongo_connect
2014-12-14 03:13:59.605 9644 TRACE ceilometer     pymongo.MongoClient(url, safe=True))
2014-12-14 03:13:59.605 9644 TRACE ceilometer   File "/usr/lib64/python2.7/site-packages/pymongo/mongo_client.py", line 337, in __init__
2014-12-14 03:13:59.605 9644 TRACE ceilometer     raise ConnectionFailure(str(e))
2014-12-14 03:13:59.605 9644 TRACE ceilometer ConnectionFailure: could not connect to localhost:27017: [Errno -9] Address family for hostname not supported
2014-12-14 03:13:59.605 9644 TRACE ceilometer
ceilometer-api failed to start
```

Run ceilometer api command independently under user `stack`

```
$ ceilometer-api -d -v --log-dir=/var/log/ceilometer-api --config-file /etc/ceilometer/ceilometer.conf
2014-12-14 06:08:40.769 15283 INFO ceilometer.api.app [-] Full WSGI config used: /etc/ceilometer/api_paste.ini
2014-12-14 06:08:40.927 15283 DEBUG ceilometer.storage [-] looking for 'mongodb' driver in 'ceilometer.metering.storage' get_connection /opt/stack/ceilometer/ceilometer/storage/__init__.py:112
2014-12-14 06:08:41.008 15283 INFO ceilometer.storage.mongo.utils [-] Connecting to mongodb on [('localhost', 27017)]
2014-12-14 06:08:41.010 15283 WARNING ceilometer.storage.mongo.utils [-] Unable to connect to the database server: could not connect to localhost:27017: [Errno -9] Address family for hostname not supported.

# mongo can be connected succesfuly
$ mongo localhost:27017
MongoDB shell version: 2.6.5
connecting to: localhost:27017/test
> 
```

Run mongo connect in pymongo, which ceilometer is using

```
python
>>> import pymongo
>>> url = 'mongodb://localhost:27017/ceilometer'
>>> client = pymongo.MongoClient(url, safe=True)
/usr/lib64/python2.7/site-packages/pymongo/mongo_client.py:343: UserWarning: database name or authSource in URI is being ignored. If you wish to authenticate to ceilometer, you must provide a username and password.
  "must provide a username and password." % (db_name,))
>>> client
MongoClient('localhost', 27017)
```

PDB in ceilometer.stroage.mongo.utils, cannot connect to mongodb

```
> /opt/stack/ceilometer/ceilometer/storage/mongo/utils.py(262)_mongo_connect()
-> pymongo.MongoClient(url, safe=True))
(Pdb) l
257                         pymongo.MongoReplicaSetClient(
258                             url,
259                             replicaSet=cfg.CONF.database.mongodb_replica_set))
260                 else:
261                     client = MongoProxy(
262  ->                     pymongo.MongoClient(url, safe=True))
263                 return client
264             except pymongo.errors.ConnectionFailure as e:
265                 LOG.warn(_('Unable to connect to the database server: '
266                            '%(errmsg)s.') % {'errmsg': e})
267                 raise
(Pdb) pymongo.MongoClient(url, safe=True)
*** ConnectionFailure: could not connect to localhost:27017: [Errno -9] Address family for hostname not supported
(Pdb) n
ConnectionFailure: Connecti...ported',)
> /opt/stack/ceilometer/ceilometer/storage/mongo/utils.py(262)_mongo_connect()
-> pymongo.MongoClient(url, safe=True))
```

This because mongodb doesn't have db `ceilomter` yet. Relevant [bug](https://bugs.launchpad.net/openstack-cisco/+bug/1301577).

```
$ mongo
MongoDB shell version: 2.6.5
connecting to: test
> show dbs
admin  (empty)
local  0.031GB
```

If we use `127.0.0.1` rather than `localhost` in connection string, pymongo will pass.

```
(Pdb) url
'mongodb://localhost:27017/ceilometer'
(Pdb) pymongo.MongoClient(url, safe=True)
*** ConnectionFailure: could not connect to localhost:27017: [Errno -9] Address family for hostname not supported
(Pdb) pymongo.MongoClient('mongodb://127.0.0.1:27017/ceilometer', safe=True)
/usr/lib64/python2.7/site-packages/pymongo/mongo_client.py:343: UserWarning: database name or authSource in URI is being ignored. If you wish to authenticate to ceilometer, you must provide a username and password.
  "must provide a username and password." % (db_name,))
MongoClient('127.0.0.1', 27017)
```

I can create `ceilometer` db in mongo beforehand ([tutorial](http://www.tutorialspoint.com/mongodb/mongodb_create_database.htm). But devstack will clean it when reinstall.

```
$ mongo
> use ceilometer
> db.nothing.insert({"name":"nothing"})
> show dbs
db.nothing.drop()
> show dbs
admin       (empty)
ceilometer  0.031GB
local       0.031GB
test        0.031GB
```

I decided to modify devstack code at `/opt/stack/workspace/devstack/lib/ceilometer`, change it to use 127.0.0.1 instead of localhost.

```
$ grep -r 'mongodb://localhost:27017/ceilometer' /opt/stack/workspace/devstack/lib/ceilometer 
        iniset $CEILOMETER_CONF database alarm_connection mongodb://localhost:27017/ceilometer
        iniset $CEILOMETER_CONF database event_connection mongodb://localhost:27017/ceilometer
        iniset $CEILOMETER_CONF database metering_connection mongodb://localhost:27017/ceilometer
$ vim vim /opt/stack/workspace/devstack/lib/ceilometer 
# change above lines to
        iniset $CEILOMETER_CONF database alarm_connection mongodb://127.0.0.1:27017/ceilometer
        iniset $CEILOMETER_CONF database event_connection mongodb://127.0.0.1:27017/ceilometer
        iniset $CEILOMETER_CONF database metering_connection mongodb://127.0.0.1:27017/ceilometer
```

## References

Devstack config examples:

  * [My devstack configuration](http://www.cberendt.net/2013/09/my-devstack-configuration/)
  * [Best localrc for devstack](http://www.sebastien-han.fr/blog/2013/08/16/best-localrc-for-devstack/)
  * [Devstack installation and testing](http://www.chenshake.com/devstack-installation-and-testing/)
