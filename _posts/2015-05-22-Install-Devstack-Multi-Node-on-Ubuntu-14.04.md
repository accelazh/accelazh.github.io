---
layout: post
title: "Install Devstack Multi-node Kilo on Ubuntu 14.04"
tagline : "Install Devstack Multi-node Kilo on Ubuntu 14.04"
description: "Install Devstack Multi-node Kilo on Ubuntu 14.04"
category: "Openstack"
tags: [openstack, devstack, ubuntu]
---
{% include JB/setup %}

## Environment

Hosts (login user `labadmin`):

  * 10.12.181.120   controller  1 NIC
  * 10.32.182.121   compute     1 NIC
  * 10.32.182.122   compute     1 NIC
  * 10.32.182.123   compute     1 NIC
  * 10.32.182.124   compute     1 NIC

Devstack branch stable/kilo commit [24cc0023](https://github.com/openstack-dev/devstack/commit/24cc0023ddca09bbbf44b70f9b4f61b500a1c0fd). Openstack branch stable/kilo. Operating system Ubuntu 14.04.2 LTS.

## Preparation

First, make sure kernel is willing to forward packets

```
# Edit /etc/sysctl.conf file, make sure ip forwarding is enabled
vim /etc/sysctl.conf
  net.ipv4.ip_forward=1
  net.ipv4.conf.all.rp_filter=0
  net.ipv4.conf.default.rp_filter=0

# Make the changes take effect
sysctl -p
```

get the devstack code from git

```
cd ~/workspace/
git clone https://github.com/openstack-dev/devstack.git
cd devstack
git checkout stable/kilo
git checkout 24cc0023ddca09bbbf44b70f9b4f61b500a1c0fd
```

To install devstack multi-node (cluster), first run devstack on your controller node with its local.conf, then run devstack on each of the compute node. I use 1 controller node and leave other nodes to be compute nodes.

Controller node devstack/local.conf

```
[[local|localrc]]
GIT_BASE=${GIT_BASE:-https://git.openstack.org}

ADMIN_PASSWORD=secrete
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=secrete
RECLONE=no

# public interface eth0 will be added to ovs br-ex. eth0 loses its ip, br-ex gets the ip.
# if the process is not finished correctly, host is left ssh unconnectable.
PUBLIC_INTERFACE=eth0

FLAT_INTERFACE=eth0
FIXED_RANGE=192.168.120.0/24
NETWORK_GATEWAY=192.168.120.1
FLOATING_RANGE=10.12.181.224/27
PUBLIC_NETWORK_GATEWAY=10.12.181.225
HOST_IP=10.12.181.120

# misc
API_RATE_LIMIT=False
LIBS_FROM_GIT=python-openstackclient

# log
DEBUG=True
VERBOSE=True
DEST=/opt/stack
LOGFILE=$DEST/logs/stack.sh.log
SCREEN_LOGDIR=$DEST/logs/screen

SYSLOG=False
LOG_COLOR=False
LOGDAYS=7

# If don't set ENABLED_SERVICES, devstack will install its default set of services
ENABLED_SERVICES=key,dstat,rabbit,mysql,tempest

# keystone
KEYSTONE_CATALOG_BACKEND=sql

# enable ceph
enable_service ceph
CEPH_LOOPBACK_DISK_SIZE=10G
CEPH_CONF=/etc/ceph/ceph.conf
CEPH_REPLICAS=3
GLANCE_CEPH_USER=glance
GLANCE_CEPH_POOL=glance
CINDER_DRIVER=ceph
CINDER_CEPH_USER=cinder
CINDER_CEPH_POOL=cinder
CINDER_CEPH_UUID=65B06887-B0EA-427F-B8BD-829AC2E18FF6
CINDER_BAK_CEPH_POOL=cinder_bak
CINDER_BAK_CEPH_USER=cind_bak
CINDER_ENABLED_BACKENDS=ceph,lvm
NOVA_CEPH_POOL=nova

# adjust scheduler to balance VMs (followed devstack official doc, but nova doesn't actually have this SimpleScheduler)
#SCHEDULER=nova.scheduler.simple.SimpleScheduler

# enable nova
enable_service n-api
enable_service n-sch
enable_service n-cond
enable_service n-api-meta
enable_service n-novnc
enable_service n-crt
enable_service n-net
enable_service n-cauth

# enable glance
enable_service g-api
enable_service g-reg

# enable swift (I find no way to just install s-proxy on controller node)
enable_service swift3
enable_service s-proxy s-object s-container s-account
SWIFT_HASH=E75834B828A54832B8AF2294FD8F5C5D
SWIFT_REPLICAS=3
SWIFT_DATA_DIR=$DEST/data/swift

# cinder
enable_service c-api
enable_service c-sch
enable_service c-bak

VOLUME_GROUP="stack-volumes"
VOLUME_NAME_PREFIX="volume-"
VOLUME_BACKING_FILE_SIZE=10250M

# enable neutron
enable_service q-svc

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
```

Compute node devstack/local.conf. For multi-node guide, see [\[1\]](https://github.com/openstack-dev/devstack/tree/stable/kilo#multi-node-setup)[\[2\]](https://github.com/openstack-dev/devstack/blob/stable/kilo/doc/source/guides/multinode-lab.rst).

```
[[local|localrc]]
GIT_BASE=${GIT_BASE:-https://git.openstack.org}

SERVICE_HOST=10.12.181.120
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
Q_HOST=$SERVICE_HOST
MATCHMAKER_REDIS_HOST=$SERVICE_HOST
DATABASE_TYPE=mysql

ADMIN_PASSWORD=secrete
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
MYSQL_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=secrete
RECLONE=no

# public interface eth0 will be added to ovs br-ex. eth0 loses its ip, br-ex gets the ip.
# if the process is not finished correctly, host is left ssh unconnectable.
PUBLIC_INTERFACE=eth0

FLAT_INTERFACE=eth0
FIXED_RANGE=192.168.120.0/24
NETWORK_GATEWAY=192.168.120.1
FLOATING_RANGE=10.12.181.224/27
PUBLIC_NETWORK_GATEWAY=10.12.181.225

# NEED TO CHANGE
HOST_IP=10.12.181.121

# misc
API_RATE_LIMIT=False
LIBS_FROM_GIT=python-openstackclient

# log
DEBUG=True
VERBOSE=True
DEST=/opt/stack
LOGFILE=$DEST/logs/stack.sh.log
SCREEN_LOGDIR=$DEST/logs/screen

SYSLOG=False
LOG_COLOR=False
LOGDAYS=7

# If don't set ENABLED_SERVICES, devstack will install its default set of services
ENABLED_SERVICES=dstat,rabbit,tempest

# Nova
enable_service n-cpu
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://${SERVICE_HOST}:6080/vnc_auto.html"
VNCSERVER_LISTEN=$HOST_IP
VNCSERVER_PROXYCLIENT_ADDRESS=$VNCSERVER_LISTEN

# Cinder
enable_service c-vol
GLANCE_CEPH_USER=glance
GLANCE_CEPH_POOL=glance
CINDER_DRIVER=ceph
CINDER_CEPH_USER=cinder
CINDER_CEPH_POOL=cinder
CINDER_CEPH_UUID=65B06887-B0EA-427F-B8BD-829AC2E18FF6
CINDER_BAK_CEPH_POOL=cinder_bak
CINDER_BAK_CEPH_USER=cind_bak
CINDER_ENABLED_BACKENDS=ceph,lvm
NOVA_CEPH_POOL=nova

VOLUME_GROUP="stack-volumes"
VOLUME_NAME_PREFIX="volume-"
VOLUME_BACKING_FILE_SIZE=10250M

# Swift
# I find no way to install multi-node swift with devstack, so I just use standalone swift on controller node
#enable_service s-proxy s-object s-container s-account
SWIFT_HASH=E75834B828A54832B8AF2294FD8F5C5D
SWIFT_REPLICAS=3
SWIFT_DATA_DIR=$DEST/data/swift

# Neutron
enable_service q-metering
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service q-fwaas
enable_service q-lbaas
#enable_service q-vpn

# VLAN configuration
Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True

# GRE tunnel configuration
Q_PLUGIN=ml2
ENABLE_TENANT_TUNNELS=True

# VXLAN tunnel configuration
Q_PLUGIN=ml2
Q_ML2_TENANT_NETWORK_TYPE=vxlan

# Ceilometer
enable_service ceilometer-acompute
CEILOMETER_BACKEND=mongodb
```

To run devstack. PS4 usage thanks to [Charles](http://stackoverflow.com/questions/10813863/while-executing-shell-scripts-how-to-know-which-line-number-its-executing). This will output debug message with file name and line number

```
PS4=':${0}:${LINENO}+' ./stack.sh
```

After installation finished, grep the error using below command

```
#rm /opt/stack/logs/*2015*    # delete all the old logs (change the year 2015 if you need)
grep -ir 'error\|fail\|usage\|not found' /opt/stack/logs/stack.sh.log
grep -ir 'error\|fail\|usage\|not found' /opt/stack/logs/screen/
```

If you met error, before reinstall devstack, you need to cleanup. The `screen` part thanks to [Milind](http://stackoverflow.com/questions/14447131/kill-all-detached-screen-sessions). Here is my `myclean.sh` to cleanup devstack remainings to prevent some error.

```
set -x
# clean rabbitmq-server
sudo kill -9 $(ps aux | grep rabbit | awk '{print $2}')
sudo kill -9 $(ps aux | grep epmd | awk '{print $2}')
sudo kill -9 $(ps aux | grep erl | awk '{print $2}')
sudo apt-get remove -y rabbitmq-server

# clean up ceph
sudo kill $(ps -ef| grep ceph | awk '{print $2}')
sudo pkill ceph
sudo apt-get remove -y ceph
sudo umount /var/lib/ceph
sudo rm -rf /var/lib/ceph
sudo rm -rf /etc/ceph

# stop swift
sudo swift-init stop all

# stop devstack and openstack
sudo pkill -9 -f python
sudo pkill -9 -f devstack
screen -ls | grep stack | cut -d. -f1 | awk '{print $1}' | xargs kill

# remove swift data
sudo umount /opt/stack/data/swift/drives/sdb1
sudo rm -rf /opt/stack/data

# clean vm net route
sudo route delete -net 192.168.120.0/24 gw 10.12.181.226
```

I recommend run `myclean.sh` this way because some services may delay a few seconds before they truely stop

```
./myclean.sh; sleep 5; ./myclean.sh
```

## Installation

Step 1: Patch the devstack code on each node, according to "Troubleshooting: Misplaced `ceph` command"

Step 2: Patch the devstack code on each node, according to "Troubleshooting: Error: openstack role list raises unrecognized arguments: --group"

Step 3: Install dependencies, according to "Troubleshooting: Error: virsh: command not found"

Step 4: Install the controller node.

Step 5: On controller node, manually add swift user, service and endpoint. See "Troubleshooting: Cannot authenticate through swift client"

Step 6: Copy devstack/accrc folder from controller node to each compute node. See "Troubleshooting: Error: euca-bundle-image: error: certificate file does not exist"

Step 7: On compute node, source openstack login environment variables `source accrc/admin/admin`. See "Troubleshooting: ERROR: openstack Missing parameter(s)"

Step 8: Change `HOST_IP` in compute node local.conf to your real host ip. 

Step 9: Run stack.sh on each of the compute nodes. After it finishes, Openstack should be available.

Step 10: To be able to access external network. Login Horizon, manually config external network & router to have correct Gateway, DNS and Provider Network Type. (For example, the gateway should be 10.12.181.1. The PUBLIC\_NETWORK\_GATEWAY in local.conf is wrong. So as is FLOATING\_RANGE.) You might need to delete them and create new ones.

BTW, [Murano](https://github.com/openstack/murano) can be installed by devstack very easily. Checkout [here](https://github.com/openstack/murano/tree/master/contrib/devstack). Same works for [Magnum](https://github.com/openstack/magnum), checkout [here](https://github.com/openstack/magnum/tree/master/devstack).

## Troubleshooting

A useful tip: when you see "error", scroll the log up until you find the root one.

### Error install rabbitmq-server

If you meet this

```
Errors were encountered while processing:
  rabbitmq-server
```

Try manually install rabbitmq-server

```
$ sudo apt-get install rabbitmq-server
Setting up rabbitmq-server (3.2.4-1) ...
 * Starting message broker rabbitmq-server
 * FAILED - check /var/log/rabbitmq/startup_\{log, _err\}]

invoke-rc.d: initscript rabbitmq-server, action "start" failed.
dpkg: error processing package rabbitmq-server (--configure):
 subprocess installed post-installation script returned error exit status 1
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

Solve by my cleanup script. Thanks to [Jordan](http://stackoverflow.com/questions/8737754/node-with-name-rabbit-already-running-but-also-unable-to-connect-to-node).

If not solved, stop all docker containers. Finally I found it is the docker services who prevents me from killing rabbitmq. Docker is running Kolla, which contains privileged container running rabbitmq.

### Ceph file exists, Ceph connect PermissionError

Symptom

```
mkdir: cannot create directory '/var/lib/ceph/mon/ceph-sclg120': File exists
```

Cause: you need to clean ceph totally. Solution: run my cleanup script.

### Git clone openstack requirements fail

Symptom

```
git clone git://git.openstack.org/openstack/requirements.git /opt/stack/requirements
 Cloning into '/opt/stack/requirements'...
 fatal: unable to connect to git.openstack.org:
```

Solution: add below to local.conf. Thanks to [Jacek and Mark](http://stackoverflow.com/questions/20390267/installing-openstack-errors).

```
GIT_BASE=${GIT_BASE:-https://git.openstack.org}
```

### Misplaced `ceph` command

Symptom. It looks like `sudo (ceph) -c` missed the `ceph` command in between

```
sudo ceph -c /etc/ceph/ceph.conf osd pool set nova size 3
set pool 5 size to 3
[[ 3 -ne 1 ]]
sudo -c /etc/ceph/ceph.conf ceph osd pool set nova crush_ruleset 1
usage: sudo -h | -K | -k | -V
usage: sudo -v [-AknS] [-g group] [-h host] [-p prompt] [-u user]
usage: sudo -l [-AknS] [-g group] [-h host] [-p prompt] [-U user] [-u user]
```

Check the line of [code](https://github.com/openstack-dev/devstack/blob/stable/kilo/lib/ceph#L282) which triggers this error. There is a [bug report](https://bugs.launchpad.net/devstack/+bug/1453055) about this. You need to modify code to fix this error:

```
$ git diff
diff --git a/lib/ceph b/lib/ceph
index 76747cc..4068e26 100644
--- a/lib/ceph
+++ b/lib/ceph
@@ -279,7 +279,7 @@ function configure_ceph_embedded_nova {
     # configure Nova service options, ceph pool, ceph user and ceph key
     sudo ceph -c ${CEPH_CONF_FILE} osd pool set ${NOVA_CEPH_POOL} size ${CEPH_REPLICAS}
     if [[ $CEPH_REPLICAS -ne 1 ]]; then
-        sudo -c ${CEPH_CONF_FILE} ceph osd pool set ${NOVA_CEPH_POOL} crush_ruleset ${RULE_ID}
+        sudo ceph -c ${CEPH_CONF_FILE} osd pool set ${NOVA_CEPH_POOL} crush_ruleset ${RULE_ID}
     fi
 }
```

Related devstack bug: [#1453055](https://bugs.launchpad.net/devstack/+bug/1453055)

### openstack role list raises unrecognized arguments: --group

Symptom

```
::./stack.sh:780+openstack role list --group 3c65c1a8d12f40a2a9949d5b2922beae --project 18ab3a46314442b183db43bc13b175b4 --column ID --column Name
usage: openstack role list [-h] [-f {csv,html,json,table,yaml}] [-c COLUMN]
                           [--max-width <integer>]
                           [--quote {all,minimal,none,nonnumeric}]
                           [--project <project>] [--user <user>]
openstack role list: error: unrecognized arguments: --group 3c65c1a8d12f40a2a9949d5b2922beae
```

Code location at lib/keystone:[418](https://github.com/openstack-dev/devstack/blob/stable/kilo/lib/keystone#L418), invoked by functions-common:[773](https://github.com/openstack-dev/devstack/blob/stable/kilo/functions-common#L773).

The first reason is that the python-openstackclient version is too old (`openstack --version`), upgrade it

```
sudo pip install --upgrade python-openstackclient
```

You need to add python-openstackclient to LIBS_FROM_GIT in local.conf, to make sure devstack uses the newest version of python-openstackclient. Note that, devstack will use master branch of python-openstackclient instead of stable/kilo.

```
# Add python-openstackclient to your LIBS_FROM_GIT
LIBS_FROM_GIT=python-openstackclient
```

The next step, since keystone v2.0 doesn't even have the concept "group", you need to force here to use keystone V3 api.

```
$ git diff
diff --git a/functions-common b/functions-common
index d3e93ed..bd55d7e 100644
--- a/functions-common
+++ b/functions-common
@@ -773,12 +773,15 @@ function get_or_add_user_project_role {
 # Gets or adds group role to project
 # Usage: get_or_add_group_project_role <role> <group> <project>
 function get_or_add_group_project_role {
+    local os_url="$KEYSTONE_SERVICE_URI_V3"
     # Gets group role id
     local group_role_id=$(openstack role list \
         --group $2 \
         --project $3 \
         --column "ID" \
         --column "Name" \
+        --os-identity-api-version=3 \
+        --os-url=$os_url \
         | grep " $1 " | get_field 1)
     if [[ -z "$group_role_id" ]]; then
         # Adds role to group
@@ -786,6 +789,8 @@ function get_or_add_group_project_role {
             $1 \
             --group $2 \
             --project $3 \
+            --os-identity-api-version=3 \
+            --os-url=$os_url \
             | grep " id " | get_field 2)
     fi
     echo $group_role_id
```

Related devstack bug: [#1441010](https://bugs.launchpad.net/devstack/+bug/1441010)

### virsh: command not found

Symptom

```
sudo virsh secret-define --file secret.xml
sudo: virsh: command not found
```

Solution: install kvm and libvirt manually

```
sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils
sudo adduser `id -un` libvirtd
sudo adduser `id -un` kvm

# You should see kvm and libvirtd in your groups
groups

# logout and login so that groups take effect
exit

# to verify
virsh -c qemu:///system list
```

### Module version does not exist!

Symptom

```
:./stack.sh:68+sudo a2enmod version
ERROR: Module version does not exist!
```

The code location is in [lib/apache:68](https://github.com/openstack-dev/devstack/blob/stable/kilo/lib/apache#L68). See the comment

> Ensure mod_version enabled for <IfVersion ...>.  This is built-in statically on anything recent, but precise (2.2) doesn't have it enabled

So, feel free to ignore this error.

### ERROR: openstack No role with a name or ID of '...' exists

Symptom

```
::./stack.sh:378+get_or_create_role admin
:::./stack.sh:748+openstack role create admin --or-show -f value -c id
::./stack.sh:746+local role_id=40d9db7cef7840c1a85d4339e1f12979
::./stack.sh:747+echo 40d9db7cef7840c1a85d4339e1f12979
:./stack.sh:378+local admin_role=40d9db7cef7840c1a85d4339e1f12979
:./stack.sh:379+get_or_add_user_project_role 40d9db7cef7840c1a85d4339e1f12979 127f875b4cfb4cfea1d3bf4c55f21fca f4376e357c12439db40d01933ef648b2
::./stack.sh:760+get_field 1
::./stack.sh:760+grep ' 40d9db7cef7840c1a85d4339e1f12979 '
::./stack.sh:598+local data field
::./stack.sh:599+read data
::./stack.sh:760+openstack role list --user 127f875b4cfb4cfea1d3bf4c55f21fca --project f4376e357c12439db40d01933ef648b2 --column ID --column Name --os-identity-api-version=3
ERROR: openstack No project with a name or ID of 'f4376e357c12439db40d01933ef648b2' exists.
:./stack.sh:760+local user_role_id=
:./stack.sh:761+[[ -z '' ]]
::./stack.sh:768+get_field 2
::./stack.sh:598+local data field
::./stack.sh:768+grep ' id '
::./stack.sh:599+read data
::./stack.sh:768+openstack role add 40d9db7cef7840c1a85d4339e1f12979 --user 127f875b4cfb4cfea1d3bf4c55f21fca --project f4376e357c12439db40d01933ef648b2 --os-identity-api-version=3
ERROR: openstack No role with a name or ID of '40d9db7cef7840c1a85d4339e1f12979' exists.
```

Cause: The first "ERROR" is ok if you see the [code](https://github.com/openstack-dev/devstack/blob/stable/kilo/functions-common#L760). Looks like the newly create role `40d9db7cef7840c1a85d4339e1f12979` doesn't get enough time to write into db. But a manual role list says it is already added.

```
$ openstack role list --os-token=secrete --os-url=http://10.12.181.120:5000/v3 --os-identity-api-version=3
+----------------------------------+-----------------+
| ID                               | Name            |
+----------------------------------+-----------------+
| 122db501c75d467084c2569628257f77 | anotherrole     |
| 40d9db7cef7840c1a85d4339e1f12979 | admin           |
| 4e889676b5b245b99a2d613cf2332088 | ResellerAdmin   |
| 7c6f1796f0b744d4aecdb78fe18ed833 | Member          |
| 8cf25f2a9c034adf91677147fc438bef | heat_stack_user |
| df0d13a639f8437d827cf7fcc5e4e72d | service         |
+----------------------------------+-----------------+
```

Solution: re-install devstack again.

### n-sch fails to start: no module named simple

Symptom, in /opt/stack/logs/screen/screen-n-sch.log

```
/usr/local/bin/nova-scheduler --config-file /etc/nova/nova.conf
2015-05-08 00:44:04.648 4677 DEBUG nova.servicegroup.api [-] ServiceGroup driver defined as an instance of db __init__ /opt/stack/nova/nova/servicegroup/api.py:68
2015-05-08 00:44:04.863 4677 INFO nova.openstack.common.periodic_task [-] Skipping periodic task _periodic_update_dns because its interval is negative
2015-05-08 00:44:04.890 4677 CRITICAL nova [-] ImportError: No module named simple
2015-05-08 00:44:04.890 4677 TRACE nova Traceback (most recent call last):
2015-05-08 00:44:04.890 4677 TRACE nova   File "/usr/local/bin/nova-scheduler", line 10, in <module>
2015-05-08 00:44:04.890 4677 TRACE nova     sys.exit(main())
2015-05-08 00:44:04.890 4677 TRACE nova   File "/opt/stack/nova/nova/cmd/scheduler.py", line 44, in main
2015-05-08 00:44:04.890 4677 TRACE nova     topic=CONF.scheduler_topic)
2015-05-08 00:44:04.890 4677 TRACE nova   File "/opt/stack/nova/nova/service.py", line 277, in create
2015-05-08 00:44:04.890 4677 TRACE nova     db_allowed=db_allowed)
2015-05-08 00:44:04.890 4677 TRACE nova   File "/opt/stack/nova/nova/service.py", line 148, in __init__
2015-05-08 00:44:04.890 4677 TRACE nova     self.manager = manager_class(host=self.host, *args, **kwargs)
2015-05-08 00:44:04.890 4677 TRACE nova   File "/opt/stack/nova/nova/scheduler/manager.py", line 63, in __init__
2015-05-08 00:44:04.890 4677 TRACE nova     self.driver = importutils.import_object(scheduler_driver)
2015-05-08 00:44:04.890 4677 TRACE nova   File "/usr/local/lib/python2.7/dist-packages/oslo_utils/importutils.py", line 38, in import_object
2015-05-08 00:44:04.890 4677 TRACE nova     return import_class(import_str)(*args, **kwargs)
2015-05-08 00:44:04.890 4677 TRACE nova   File "/usr/local/lib/python2.7/dist-packages/oslo_utils/importutils.py", line 27, in import_class
2015-05-08 00:44:04.890 4677 TRACE nova     __import__(mod_str)
2015-05-08 00:44:04.890 4677 TRACE nova ImportError: No module named simple
2015-05-08 00:44:04.890 4677 TRACE nova
n-sch failed to start
```

Cause: you must be following the devstack official [guide](https://github.com/openstack-dev/devstack/tree/stable/kilo#multi-node-setup)

```
SCHEDULER=nova.scheduler.simple.SimpleScheduler
```

However, nova.scheduler.simple.SimpleScheduler doesn't [exist](https://github.com/openstack/nova/tree/stable/kilo/nova/scheduler) actually. Solution: don't add this SimpleScheduler line.

```
#SCHEDULER=nova.scheduler.simple.SimpleScheduler
```

### route add -net ... raises "SIOCADDRT: File exists"

Symptom

```
sudo route add -net 192.168.120.0/24 gw 10.12.181.226
SIOCADDRT: File exists
```

Cause: the route is added multiple times. Solution: remove the route 192.168.120.0 before reinstall devstack.

```
sudo route delete -net 192.168.120.0/24 gw 10.12.181.226
```

Added to my cleanup script.

### Warning: pvs: Ignoring duplicate config node: global_filter

Symptom

```
sudo pvs --noheadings -o name
WARNING: Ignoring duplicate config node: global_filter (seeking global_filter)
WARNING: Ignoring duplicate config node: global_filter (seeking global_filter)
WARNING: Ignoring duplicate config node: global_filter (seeking global_filter)
WARNING: Ignoring duplicate config node: global_filter (seeking global_filter)
```

Cause: you have multiple line of 'filter = ' in lvm config file. For example, here is what I found in my /etc/lvm/lvm.conf

```
 # global_filter = []
    global_filter = [ "a|loop2|", "a|loop3|", "a|loop4|", "r|.*|" ]
    global_filter = [ "a|loop2|", "a|loop3|", "a|loop4|", "r|.*|" ]
    global_filter = [ "a|loop2|", "a|loop3|", "a|loop4|", "r|.*|" ]
    global_filter = [ "a|loop2|", "a|loop3|", "a|loop4|", "r|.*|" ]
```

Solution: delete duplicated lines.

### ERROR: openstack No group with a name or ID of '425c537ceb8b4a5391692452ef2f64bb' exists

Symptom

```
openstack role list --group 425c537ceb8b4a5391692452ef2f64bb --project df5b59544ea84147addf09237a7fe0b0 --column ID --column Name --os-identity-api-version=3
ERROR: openstack No group with a name or ID of '425c537ceb8b4a5391692452ef2f64bb' exists.
```

Cause: use --verbose --debug to find out what's happening. Look at below

```
$ openstack role list --group 5bd604db63d34b158cec7ede42ff27a1 --project f636a88775b749d5aa71c7c585540d3e --column ID --column Name --os-identity-api-version=3 --verbose --debug
...
service_provider_endpoint='', timing=False, token='secrete', trust_id='', url='http://10.12.181.120:35357/v2.0', user_domain_id='', user_domain_name='', user_id='', username='', verbose_level=3, verify=False)
...
DEBUG: openstackclient.shell cloud cfg: {'auth_type': 'token_endpoint', 'compute_api_version': '2', 'region_name': '', 'volume_api_version': '1', 'insecure': False, 'auth': {'url': 'http://10.12.181.120:35357/v2.0', 'token': 'secrete'}, 'default_domain': 'default', 'timing': False, 'network_api_version': '2', 'object_api_version': '1', 'image_api_version': '1', 'verify': False, 'identity_api_version': '3', 'verbose_level': 3, 'deferred_help': False, 'debug': True}
...
DEBUG: keystoneclient.session REQ: curl -g -i -X GET http://10.12.181.120:35357/v2.0/groups/5bd604db63d34b158cec7ede42ff27a1 -H "User-Agent: python-keystoneclient" -H "Accept: application/json" -H "X-Auth-Token: {SHA1}e78608b0aa589f6a36e3e6fb9a720cece3163496"
...
CommandError: No group with a name or ID of '5bd604db63d34b158cec7ede42ff27a1' exists.
```

Note that I'm trying to force python-openstackclient to use keystone api V3, by `--os-identity-api-version=3`. However, the auth url `http://10.12.181.120:35357/v2.0` is still v2. This makes python-openstackclient throws a "No group ..." error.

Solution: when you want to use keystone V3 api, you should always one of the pair

```
# Switch to V3 by environment variable
export OS_URL=http://10.12.181.120:5000/v3
export OS_IDENTITY_API_VERSION=3

# Switch to V3 by command options
--os-url=http://10.12.181.120:5000/v3
--os-identity-api-version=3
```

### ERROR: openstack No group with a name or ID of 'XDG_SESSION_ID=54' exists

Symptom

```
get_or_add_group_project_role bdc3408336f647f5bf858e01ca2d4bd3 XDG_SESSION_ID=54 WHEELHOUSE=/opt/stack/.wheelhouse ...
...
openstack role list --group XDG_SESSION_ID=54 --project WHEELHOUSE=/opt/stack/.wheelhouse --column ID --column Name --os-identity-api-version=3 --os-url=http://10.12.181.120:5000/v3
ERROR: openstack No group with a name or ID of 'XDG_SESSION_ID=54' exists.
```

Cause: the `get_or_add_group_project_role` is taking don't know what argument. This is because I put `env` in functions to dump environment variables. But the output is treated as return value, then taken by `get_or_add_group_project_role` as arguments. For example:

```
function get_or_create_group {
    local domain=${2:+--domain ${2}}
    local desc="${3:-}"
    local os_url="$KEYSTONE_SERVICE_URI_V3"
    env    # debug
    # Gets group id
    local group_id=$(
        # Creates new group with --or-show
        openstack --os-token=$OS_TOKEN --os-url=$os_url \
            --os-identity-api-version=3 group create $1 \
            $domain --description "$desc" --or-show \
            -f value -c id
    )
    echo $group_id
}
```

Solution: remove the debug commands in function body.

### ERROR: openstack No service with a type, name or ID of 's3' exists

Symptom

```
2015-05-14 23:39:30.253 | ::~/devstack/tools/create_userrc.sh:137+openstack endpoint show -f value -c publicurl s3
2015-05-14 23:39:33.340 | ERROR: openstack No service with a type, name or ID of 's3' exists.
```

Cause: This is because S3 service is not enabled. Take a look at [lib/nova:375](https://github.com/openstack-dev/devstack/blob/stable/kilo/lib/nova#L375).

Solutoin: enable swift3 service.

```
enable_service swift3
```

Added to my local.conf.

### ERROR (EndpointNotFound): publicURL endpoint for compute service in RegionOne region not found

Symptom: my controller node installation succeeds. However compute node reports

```
:::./stack.sh:197+nova flavor-list
ERROR (EndpointNotFound): publicURL endpoint for compute service in RegionOne region not found
```

Just after controller is installed, and compute node not installed. Run `nova flavor-list` on controller node is OK. After compute node installs, both controller node and comupte node reports above error.

Cause: compute node installed keystone again. Note that devstack on default install a servies of default services, see devstack/stackrc line 48

```
# If you don't set ENABLED_SERVICES, devstack installs a series of default services
if ! isset ENABLED_SERVICES ; then
    # Keystone - nothing works without keystone
    ENABLED_SERVICES=key
    # Nova - services to support libvirt based openstack clouds
    ENABLED_SERVICES+=,n-api,n-cpu,n-net,n-cond,n-sch,n-novnc,n-crt
    # Glance services needed for Nova
    ENABLED_SERVICES+=,g-api,g-reg
    # Cinder
    ENABLED_SERVICES+=,c-sch,c-api,c-vol
    # Dashboard
    ENABLED_SERVICES+=,horizon
    # Additional services
    ENABLED_SERVICES+=,rabbit,tempest,mysql,dstat
fi
```

Usually I use `enable_service` to enable a service, what is its relation with ENABLED_SERVICES? The `enable_service` adds service to `ENABLED_SERVICES`. See devstack/functions-common line 1667

```
function enable_service {
    local tmpsvcs="${ENABLED_SERVICES}"
    local service
    for service in $@; do
        if ! is_service_enabled $service; then
            tmpsvcs+=",$service"
        fi
    done
    ENABLED_SERVICES=$(_cleanup_service_list "$tmpsvcs")
    disable_negated_services
}
```

So if you don't write `ENABLED_SERVICES` explicitly in local.conf, devstack will install default services.

Solution: explicitly specify `ENABLED_SERVICE`. Merged in my local.conf above.

### Cannot authenticate through swift client

Symptom: After controller node installed, cannot authenticate through swift client

```
$ source accrc/admin/admin
$ swift list
Endpoint for object-store not found - have you specified a region?
```

Cause: check swift config I find it uses user `swift` and tenant `service`

```
$ cat /etc/swift/proxy-server.conf
[filter:keystoneauth]
...
admin_user = swift
admin_tenant_name = service
admin_password = secrete
...
```

However, keystone doesn't has `swift` user. Keystone doesn't have object-store service, either.

```
$ source accrc/admin/admin
$ keystone user-list
+----------------------------------+----------------------------------+---------+----------------------------------------------+
|                id                |               name               | enabled |                    email                     |
+----------------------------------+----------------------------------+---------+----------------------------------------------+
| c40195e8f7bf4b96b6d96497b712f14e |              admin               |   True  |                                              |
| eaa5205fd7b54a23a73c0c71b5af01de |             alt_demo             |   True  |             alt_demo@example.com             |
| 93276360fe014b33b8d41fe6ed5bf7c6 |            ceilometer            |   True  |                                              |
| a7ae0298ed054d30a0e249837d053a3e |              cinder              |   True  |                                              |
| 5beb0900ae6e4d9b8bd8deb1976c3799 |               demo               |   True  |               demo@example.com               |
| 268dbc01b733425fb01bf0dc9bb8cc48 |              glance              |   True  |                                              |
| 914a2945c2604cf0a888af2c7ab75cf8 |           glance-swift           |   True  |           glance-swift@example.com           |
| 65fba8c2200b4bd597b4f5013a963641 |               heat               |   True  |                                              |
| 7b53803da68e42dbb1c3ca4b0c3ce8fd |             neutron              |   True  |                                              |
| 03de71cfaed24fefbba070c0fbdb42f8 |               nova               |   True  |                                              |
| cb0577eecfd14b30b865b09b89d48e01 | verify_tempest_config-1054526126 |   True  | verify_tempest_config-1100444792@example.com |
+----------------------------------+----------------------------------+---------+----------------------------------------------+
$ keystone service-list
+----------------------------------+------------+----------------+-----------------------------+
|                id                |    name    |      type      |         description         |
+----------------------------------+------------+----------------+-----------------------------+
| 6dba83f0ce15479b865d555856c2ae6b | ceilometer |    metering    | OpenStack Telemetry Service |
| d7065bd18b6a48ee93ded600ba46f24d |   cinder   |     volume     |    Cinder Volume Service    |
| 51e8c16252824f308057804fef5af887 |  cinderv2  |    volumev2    |   Cinder Volume Service V2  |
| 3f11529fb0664b9ea402c24357283c96 |    ec2     |      ec2       |   EC2 Compatibility Layer   |
| 6454affd1c7445eaaf24da37a0fbeb65 |   glance   |     image      |     Glance Image Service    |
| 1d95168b965540379a2052e8d87364f4 |    heat    | orchestration  |  Heat Orchestration Service |
| c0c77fc0e0334aeda4c0253f8dfede99 |  heat-cfn  | cloudformation | Heat CloudFormation Service |
| f66252ab764040aebb9845b020a342c6 |  keystone  |    identity    |  Keystone Identity Service  |
| c2dd7ae47c394d34b1e1a92fade588a9 |  neutron   |    network     |       Neutron Service       |
| 9f07331af66e4ba28bda3da908b2e6d2 |    nova    |    compute     |     Nova Compute Service    |
| 8cf19cea035f40df9c170c677b26ccef |  novav21   |   computev21   |  Nova Compute Service V2.1  |
| 64c4225d886b4e70aa2cee06f561db92 |     s3     |       s3       |              S3             |
+----------------------------------+------------+----------------+-----------------------------+
```

Solution: thanks to [Danlzack's answer](https://ask.openstack.org/en/question/28032/i-installed-openstack-using-devstack-then-i-discovered-that-the-swift-service-object-store-is-missed-how-i-can-add-it/), let's manually add swift endpoint and service.

```
# On controller node, after devstack installation finished, before you install compute node
source accrc/admin/admin
keystone user-create --name=swift --pass=secrete --email=swift@example.com
keystone user-role-add --user=swift --tenant=service --role=admin
keystone service-create --name=swift --type=object-store --description="Object Storage Service"
keystone endpoint-create \
  --service-id=$(keystone service-list | awk '/ object-store / {print $2}') \
  --publicurl='http://10.12.181.120:8080/v1/AUTH_%(tenant_id)s' \
  --internalurl='http://10.12.181.120:8080/v1/AUTH_%(tenant_id)s' \
  --adminurl=http://10.12.181.120:8080 \
  --region RegionOne
```

### ERROR: openstack Missing parameter(s)

Symptom: on compute node

```
2015-05-21 04:29:24.147 | ::./stack.sh:729+local os_cmd=openstack
2015-05-21 04:29:24.147 | ::./stack.sh:730+local domain=
2015-05-21 04:29:24.147 | ::./stack.sh:731+[[ ! -z '' ]]
2015-05-21 04:29:24.147 | :::./stack.sh:740+openstack project create alt_demo --or-show -f value -c id
2015-05-21 04:29:25.470 | ERROR: openstack Missing parameter(s):
2015-05-21 04:29:25.470 | Set a username with --os-username, OS_USERNAME, or auth.username
2015-05-21 04:29:25.470 | Set an authentication URL, with --os-auth-url, OS_AUTH_URL or auth.auth_url
2015-05-21 04:29:25.470 | Set a scope, such as a project or domain, with --os-project-name, OS_PROJECT_NAME or auth.project_name
2015-05-21 04:29:25.499 | ::./stack.sh:738+local project_id=
2015-05-21 04:29:25.500 | ::./stack.sh:739+echo
```

Cause: I dumped the environment variables when executing the `openstack project create`, found missing

```
OS_PASSWORD=secrete
OS_AUTH_URL=http://10.12.181.120:35357/v2.0
OS_TENANT_NAME=admin
OS_USERNAME=admin
```

Compare this compute node with controller node, I found these environment variables should be imported at stack.sh line 1010

```
if is_service_enabled keystone; then
    ...
    export OS_AUTH_URL=$SERVICE_ENDPOINT
    export OS_TENANT_NAME=admin
    export OS_USERNAME=admin
    export OS_PASSWORD=$ADMIN_PASSWORD
    export OS_REGION_NAME=$REGION_NAME
fi
```

So because I won't install keystone again on compute node, so devstack didn't export the necessary environment variables.

Solution: before install the compute node, `source accrc/admin/admin` which copied from controller node.

### euca-bundle-image: error: certificate file does not exist

Symptom: On compute node, devstack reports below error

```
2015-05-21 05:34:37.566 | ::./stack.sh:1062+real_install_package euca2ools
2015-05-21 05:34:37.567 | ::./stack.sh:1047+is_ubuntu
2015-05-21 05:34:37.567 | ::./stack.sh:380+[[ -z deb ]]
2015-05-21 05:34:37.567 | ::./stack.sh:383+'[' deb = deb ']'
2015-05-21 05:34:37.567 | ::./stack.sh:1048+apt_get install euca2ools
2015-05-21 05:34:37.572 | ::./stack.sh:877+sudo DEBIAN_FRONTEND=noninteractive http_proxy= https_proxy= no_proxy= apt-get --option Dpkg::Options::=--force-confold --assume-yes install
 euca2ools
2015-05-21 05:34:37.587 | Reading package lists...
2015-05-21 05:34:37.893 | Building dependency tree...
2015-05-21 05:34:37.894 | Reading state information...
2015-05-21 05:34:38.144 | euca2ools is already the newest version.
2015-05-21 05:34:38.145 | 0 upgraded, 0 newly installed, 0 to remove and 84 not upgraded.
2015-05-21 05:34:38.146 | ::./stack.sh:581+source /home/labadmin/workspace/devstack/accrc/demo/demo
2015-05-21 05:34:38.166 | :::./stack.sh:2+export EC2_ACCESS_KEY=b73139469b9e45c9bb7c51439ec59bf0
2015-05-21 05:34:38.166 | :::./stack.sh:2+EC2_ACCESS_KEY=b73139469b9e45c9bb7c51439ec59bf0
2015-05-21 05:34:38.166 | :::./stack.sh:3+export EC2_SECRET_KEY=03822bf48f0d4773a64f7d2d1c0a4f03
2015-05-21 05:34:38.167 | :::./stack.sh:3+EC2_SECRET_KEY=03822bf48f0d4773a64f7d2d1c0a4f03
2015-05-21 05:34:38.167 | :::./stack.sh:4+export EC2_URL=http://localhost:8773/
2015-05-21 05:34:38.167 | :::./stack.sh:4+EC2_URL=http://localhost:8773/
2015-05-21 05:34:38.167 | :::./stack.sh:5+export S3_URL=http://localhost:3333
2015-05-21 05:34:38.168 | :::./stack.sh:5+S3_URL=http://localhost:3333
2015-05-21 05:34:38.168 | :::./stack.sh:7+export OS_USERNAME=demo
2015-05-21 05:34:38.168 | :::./stack.sh:7+OS_USERNAME=demo
2015-05-21 05:34:38.168 | :::./stack.sh:9+export OS_TENANT_NAME=demo
2015-05-21 05:34:38.168 | :::./stack.sh:9+OS_TENANT_NAME=demo
2015-05-21 05:34:38.168 | :::./stack.sh:10+export OS_AUTH_URL=http://10.12.181.120:35357/v2.0
2015-05-21 05:34:38.168 | :::./stack.sh:10+OS_AUTH_URL=http://10.12.181.120:35357/v2.0
2015-05-21 05:34:38.169 | :::./stack.sh:11+export OS_CACERT=
2015-05-21 05:34:38.169 | :::./stack.sh:11+OS_CACERT=
2015-05-21 05:34:38.169 | :::./stack.sh:12+export EC2_CERT=/home/labadmin/workspace/devstack/accrc/demo/demo-cert.pem
2015-05-21 05:34:38.169 | :::./stack.sh:12+EC2_CERT=/home/labadmin/workspace/devstack/accrc/demo/demo-cert.pem
2015-05-21 05:34:38.170 | :::./stack.sh:13+export EC2_PRIVATE_KEY=/home/labadmin/workspace/devstack/accrc/demo/demo-pk.pem
2015-05-21 05:34:38.170 | :::./stack.sh:13+EC2_PRIVATE_KEY=/home/labadmin/workspace/devstack/accrc/demo/demo-pk.pem
2015-05-21 05:34:38.170 | :::./stack.sh:14+export EC2_USER_ID=42
2015-05-21 05:34:38.171 | :::./stack.sh:14+EC2_USER_ID=42
2015-05-21 05:34:38.171 | :::./stack.sh:15+export EUCALYPTUS_CERT=/home/labadmin/workspace/devstack/accrc/cacert.pem
2015-05-21 05:34:38.171 | :::./stack.sh:15+EUCALYPTUS_CERT=/home/labadmin/workspace/devstack/accrc/cacert.pem
2015-05-21 05:34:38.171 | :::./stack.sh:16+export NOVA_CERT=/home/labadmin/workspace/devstack/accrc/cacert.pem
2015-05-21 05:34:38.171 | :::./stack.sh:16+NOVA_CERT=/home/labadmin/workspace/devstack/accrc/cacert.pem
2015-05-21 05:34:38.171 | :::./stack.sh:17+export OS_PASSWORD=secrete
2015-05-21 05:34:38.171 | :::./stack.sh:17+OS_PASSWORD=secrete
2015-05-21 05:34:38.172 | ::./stack.sh:582+euca-bundle-image -r x86_64 -i /home/labadmin/workspace/devstack/files/images/cirros-0.3.2-x86_64-uec/cirros-0.3.2-x86_64-vmlinuz --kernel t
rue -d /home/labadmin/workspace/devstack/files/images/s3-materials/cirros-0.3.2
2015-05-21 05:34:38.460 | usage: euca-bundle-image -i FILE [-p PREFIX] -r {i386,x86_64,armhf} [-c FILE]
2015-05-21 05:34:38.460 |                          [-k FILE] [-u ACCOUNT] [--region USER@REGION]
2015-05-21 05:34:38.461 |                          [--ec2cert FILE] [--kernel IMAGE] [--ramdisk IMAGE]
2015-05-21 05:34:38.461 |                          [-B VIRTUAL1=DEVICE1,VIRTUAL2=DEVICE2,...] [-d DIR]
2015-05-21 05:34:38.461 |                          [--productcodes CODE1,CODE2,...] [--debug]
2015-05-21 05:34:38.461 |                          [--debugger] [--version] [-h]
2015-05-21 05:34:38.461 | euca-bundle-image: error: certificate file '/home/labadmin/workspace/devstack/accrc/demo/demo-cert.pem' does not exist
```

Cause: The controller node generates the certificate file, but compute didn't. Looks like it is because some services are not installed on compute node, so the generation is not triggered.

Solution: Manually copy `accrc` folder to each compute node.

### c-vol fails to start: ArgumentError: Could not parse rfc1738 URL from string ''

Symptom: On compute node, stach.sh reports "Service c-vol is not running", /opt/stack/logs/screen/screen-c-vol.log shows

```
/usr/local/bin/cinder-volume --config-file /etc/cinder/cinder.conf
/opt/stack/cinder/cinder/openstack/common/service.py:38: DeprecationWarning: The oslo namespace package is deprecated. Please use oslo_config instead.
  from oslo.config import cfg
2015-05-20 22:51:43.073 2849 DEBUG oslo_db.api [-] Loading backend 'sqlalchemy' from 'cinder.db.sqlalchemy.api' _load_backend /usr/local/lib/python2.7/dist-packages/oslo_db/api.py:214
2015-05-20 22:51:43.350 2849 CRITICAL cinder [-] ArgumentError: Could not parse rfc1738 URL from string ''
2015-05-20 22:51:43.350 2849 TRACE cinder Traceback (most recent call last):
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/usr/local/bin/cinder-volume", line 10, in <module>
2015-05-20 22:51:43.350 2849 TRACE cinder     sys.exit(main())
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/cmd/volume.py", line 72, in main
2015-05-20 22:51:43.350 2849 TRACE cinder     binary='cinder-volume')
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/service.py", line 249, in create
2015-05-20 22:51:43.350 2849 TRACE cinder     service_name=service_name)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/service.py", line 129, in __init__
2015-05-20 22:51:43.350 2849 TRACE cinder     *args, **kwargs)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/volume/manager.py", line 195, in __init__
2015-05-20 22:51:43.350 2849 TRACE cinder     *args, **kwargs)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/manager.py", line 130, in __init__
2015-05-20 22:51:43.350 2849 TRACE cinder     super(SchedulerDependentManager, self).__init__(host, db_driver)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/manager.py", line 80, in __init__
2015-05-20 22:51:43.350 2849 TRACE cinder     super(Manager, self).__init__(db_driver)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/db/base.py", line 42, in __init__
2015-05-20 22:51:43.350 2849 TRACE cinder     self.db.dispose_engine()
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/db/api.py", line 80, in dispose_engine
2015-05-20 22:51:43.350 2849 TRACE cinder     if 'sqlite' not in IMPL.get_engine().name:
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/db/sqlalchemy/api.py", line 85, in get_engine
2015-05-20 22:51:43.350 2849 TRACE cinder     facade = _create_facade_lazily()
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/opt/stack/cinder/cinder/db/sqlalchemy/api.py", line 72, in _create_facade_lazily
2015-05-20 22:51:43.350 2849 TRACE cinder     **dict(CONF.database.iteritems())
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/usr/local/lib/python2.7/dist-packages/oslo_db/sqlalchemy/session.py", line 796, in __init__
2015-05-20 22:51:43.350 2849 TRACE cinder     **engine_kwargs)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/usr/local/lib/python2.7/dist-packages/oslo_db/sqlalchemy/session.py", line 376, in create_engine
2015-05-20 22:51:43.350 2849 TRACE cinder     url = sqlalchemy.engine.url.make_url(sql_connection)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/url.py", line 176, in make_url
2015-05-20 22:51:43.350 2849 TRACE cinder     return _parse_rfc1738_args(name_or_url)
2015-05-20 22:51:43.350 2849 TRACE cinder   File "/usr/local/lib/python2.7/dist-packages/sqlalchemy/engine/url.py", line 225, in _parse_rfc1738_args
2015-05-20 22:51:43.350 2849 TRACE cinder     "Could not parse rfc1738 URL from string '%s'" % name)
2015-05-20 22:51:43.350 2849 TRACE cinder ArgumentError: Could not parse rfc1738 URL from string ''
2015-05-20 22:51:43.350 2849 TRACE cinder
c-vol failed to start
```

Check out the cinder conf file /etc/cinder/cinder.conf

```
...
[database]
connection =
...
```

The db connection string is empty. That's why cinder fails to start. Same issue found in nova.conf. The db connection string should be generated by 

```
# lib/cinder
iniset $CINDER_CONF database connection `database_connection_url cinder`

# lib/database
function database_connection_url {
    local db=$1
    database_connection_url_$DATABASE_TYPE $db
}
```

Looks like the DATABASE_TYPE is not assigned since compute node doesn't install mysql. Also found below in log.

```
2015-05-21 05:49:42.876 | ::./stack.sh:205+database_connection_url cinder
2015-05-21 05:49:42.876 | ::./stack.sh:125+local db=cinder
2015-05-21 05:49:42.876 | ::./stack.sh:126+database_connection_url_ cinder
2015-05-21 05:49:42.876 | /home/labadmin/workspace/devstack/lib/database: line 126: database_connection_url_: command not found
```

Solution: Add `DATABASE_TYPE=mysql` into local.conf. Merged to my local.conf above. There is a [doc](https://github.com/openstack-dev/devstack/blob/stable/kilo/doc/source/guides/multinode-lab.rst) mentioned adding DATABASE_TYPE into compute local.conf.

## Package List

After my whole cluster installation finished, I will list my installed packages and versions. Here is my OS kernel version

```
$ uname -a
Linux sclg120 3.16.0-30-generic #40~14.04.1-Ubuntu SMP Thu Jan 15 17:43:14 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
```

List my controller node installed packages and versions

```
accountsservice                          0.6.35-0ubuntu7.1
acl                                      2.2.52-1
acpid                                    1:2.0.21-1ubuntu2
adduser                                  3.113+nmu3ubuntu3
apache2                                  2.4.7-1ubuntu4.4
apache2-bin                              2.4.7-1ubuntu4.4
apache2-data                             2.4.7-1ubuntu4.4
apparmor                                 2.8.95~2430-0ubuntu5.1
apport                                   2.14.1-0ubuntu3.7
apport-symptoms                          0.20
apt                                      1.0.1ubuntu2.6
aptitude                                 0.6.8.2-1ubuntu4
aptitude-common                          0.6.8.2-1ubuntu4
apt-transport-https                      1.0.1ubuntu2.6
apt-utils                                1.0.1ubuntu2.6
apt-xapian-index                         0.45ubuntu4
at                                       3.1.14-1ubuntu1
aufs-tools                               1:3.2+20130722-1.1
augeas-lenses                            1.2.0-0ubuntu1.1
base-files                               7.2ubuntu5.2
base-passwd                              3.5.33
bash                                     4.3-7ubuntu1.5
bash-completion                          1:2.1-4
bc                                       1.06.95-8ubuntu1
bind9-host                               1:9.9.5.dfsg-3ubuntu0.1
binutils                                 2.24-5ubuntu3.1
biosdevname                              0.4.1-0ubuntu6.1
bridge-utils                             1.5-6ubuntu2
bsdmainutils                             9.0.5ubuntu1
bsdutils                                 1:2.20.1-5.1ubuntu20.4
build-essential                          11.6ubuntu6
busybox-initramfs                        1:1.21.0-1ubuntu1
busybox-static                           1:1.21.0-1ubuntu1
byobu                                    5.77-0ubuntu1.2
bzip2                                    1.0.6-5
ca-certificates                          20130906ubuntu2
ceph                                     0.80.9-0ubuntu0.14.04.2
ceph-common                              0.80.9-0ubuntu0.14.04.2
cgroup-lite                              1.9
comerr-dev                               2.1-1.42.9-3ubuntu1.2
command-not-found                        0.3ubuntu12
command-not-found-data                   0.3ubuntu12
conntrack                                1:1.4.1-1ubuntu1
conntrackd                               1:1.4.1-1ubuntu1
console-setup                            1.70ubuntu8
coreutils                                8.21-1ubuntu5.1
cpio                                     2.11+dfsg-1ubuntu1.1
cpp                                      4:4.8.2-1ubuntu6
cpp-4.8                                  4.8.2-19ubuntu1
cpu-checker                              0.7-0ubuntu4
crda                                     1.1.2-1ubuntu2
cron                                     3.0pl1-124ubuntu2
cryptsetup-bin                           2:1.6.1-1ubuntu1
curl                                     7.35.0-1ubuntu2.5
dash                                     0.5.7-4ubuntu1
dbus                                     1.6.18-0ubuntu4.3
dctrl-tools                              2.23ubuntu1
debconf                                  1.5.51ubuntu2
debconf-i18n                             1.5.51ubuntu2
debianutils                              4.4
debootstrap                              1.0.59ubuntu0.2
devscripts                               2.14.1
dh-python                                1.20140128-1ubuntu8
diffstat                                 1.58-1
diffutils                                1:3.3-1
distro-info-data                         0.18ubuntu0.2
dmidecode                                2.12-2
dmsetup                                  2:1.02.77-6ubuntu2
dnsmasq-base                             2.68-1ubuntu0.1
dnsmasq-utils                            2.68-1ubuntu0.1
dnsutils                                 1:9.9.5.dfsg-3ubuntu0.1
docutils-common                          0.11-3
docutils-doc                             0.11-3
dosfstools                               3.0.26-1
dpkg                                     1.17.5ubuntu5.3
dpkg-dev                                 1.17.5ubuntu5.4
dput                                     0.9.6.4ubuntu1.1
dstat                                    0.7.2-3build1
e2fslibs:amd64                           1.42.9-3ubuntu1
e2fsprogs                                1.42.9-3ubuntu1
ebtables                                 2.0.10.4-3ubuntu1
ed                                       1.9-2
eject                                    2.1.5+deb1+cvs20081104-13.1
erlang-asn1                              1:16.b.3-dfsg-1ubuntu2.1
erlang-base                              1:16.b.3-dfsg-1ubuntu2.1
erlang-corba                             1:16.b.3-dfsg-1ubuntu2.1
erlang-crypto                            1:16.b.3-dfsg-1ubuntu2.1
erlang-diameter                          1:16.b.3-dfsg-1ubuntu2.1
erlang-edoc                              1:16.b.3-dfsg-1ubuntu2.1
erlang-eldap                             1:16.b.3-dfsg-1ubuntu2.1
erlang-erl-docgen                        1:16.b.3-dfsg-1ubuntu2.1
erlang-eunit                             1:16.b.3-dfsg-1ubuntu2.1
erlang-ic                                1:16.b.3-dfsg-1ubuntu2.1
erlang-inets                             1:16.b.3-dfsg-1ubuntu2.1
erlang-mnesia                            1:16.b.3-dfsg-1ubuntu2.1
erlang-nox                               1:16.b.3-dfsg-1ubuntu2.1
erlang-odbc                              1:16.b.3-dfsg-1ubuntu2.1
erlang-os-mon                            1:16.b.3-dfsg-1ubuntu2.1
erlang-parsetools                        1:16.b.3-dfsg-1ubuntu2.1
erlang-percept                           1:16.b.3-dfsg-1ubuntu2.1
erlang-public-key                        1:16.b.3-dfsg-1ubuntu2.1
erlang-runtime-tools                     1:16.b.3-dfsg-1ubuntu2.1
erlang-snmp                              1:16.b.3-dfsg-1ubuntu2.1
erlang-ssh                               1:16.b.3-dfsg-1ubuntu2.1
erlang-ssl                               1:16.b.3-dfsg-1ubuntu2.1
erlang-syntax-tools                      1:16.b.3-dfsg-1ubuntu2.1
erlang-tools                             1:16.b.3-dfsg-1ubuntu2.1
erlang-webtool                           1:16.b.3-dfsg-1ubuntu2.1
erlang-xmerl                             1:16.b.3-dfsg-1ubuntu2.1
ethtool                                  1:3.13-1
euca2ools                                3.0.2-1ubuntu1
fakeroot                                 1.20-3ubuntu2
file                                     1:5.14-2ubuntu3.3
findutils                                4.4.2-7
fontconfig                               2.11.0-0ubuntu4.1
fontconfig-config                        2.11.0-0ubuntu4.1
fonts-dejavu-core                        2.34-1ubuntu1
fonts-liberation                         1.07.3-3
fonts-ubuntu-font-family-console         0.80-0ubuntu6
fping                                    3.8-1
friendly-recovery                        0.2.25
ftp                                      0.17-28
fuse                                     2.9.2-4ubuntu4
g++                                      4:4.8.2-1ubuntu6
g++-4.8                                  4.8.2-19ubuntu1
gawk                                     1:4.0.1+dfsg-2.1ubuntu2
gcc                                      4:4.8.2-1ubuntu6
gcc-4.8                                  4.8.2-19ubuntu1
gcc-4.8-base:amd64                       4.8.2-19ubuntu1
gcc-4.9-base:amd64                       4.9.1-0ubuntu1
gdisk                                    0.8.8-1build1
genisoimage                              9:1.1.11-2ubuntu3
geoip-database                           20140313-1
gettext                                  0.18.3.1-1ubuntu3
gettext-base                             0.18.3.1-1ubuntu3
gir1.2-glib-2.0                          1.40.0-1ubuntu0.2
git                                      1:1.9.1-1ubuntu0.1
git-man                                  1:1.9.1-1ubuntu0.1
gnupg                                    1.4.16-1ubuntu2.1
gpgv                                     1.4.16-1ubuntu2.1
graphviz                                 2.36.0-0ubuntu3.1
grep                                     2.16-1
groff-base                               1.22.2-5
grub2-common                             2.02~beta2-9ubuntu1
grub-common                              2.02~beta2-9ubuntu1
grub-gfxpayload-lists                    0.6
grub-pc                                  2.02~beta2-9ubuntu1
grub-pc-bin                              2.02~beta2-9ubuntu1
gzip                                     1.6-3ubuntu1
haproxy                                  1.4.24-2
hardening-includes                       2.5ubuntu2.1
hdparm                                   9.43-1ubuntu3
hostname                                 3.15ubuntu1
ifupdown                                 0.7.47.2ubuntu4.1
info                                     5.2.0.dfsg.1-2
initramfs-tools                          0.103ubuntu4.2
initramfs-tools-bin                      0.103ubuntu4.2
initscripts                              2.88dsf-41ubuntu6
init-system-helpers                      1.14
insserv                                  1.14.0-5ubuntu2
installation-report                      2.54ubuntu1
install-info                             5.2.0.dfsg.1-2
intltool-debian                          0.35.0+20060710.1
iproute                                  1:3.12.0-2
iproute2                                 3.12.0-2
ipset                                    6.20.1-1
iptables                                 1.4.21-1ubuntu1
iputils-arping                           3:20121221-4ubuntu1.1
iputils-ping                             3:20121221-4ubuntu1.1
iputils-tracepath                        3:20121221-4ubuntu1.1
ipvsadm                                  1:1.26-2ubuntu1
ipxe-qemu                                1.0.0+git-20131111.c3d1e78-2ubuntu1.1
irqbalance                               1.0.6-2ubuntu0.14.04.1
isc-dhcp-client                          4.2.4-7ubuntu12
isc-dhcp-common                          4.2.4-7ubuntu12
iso-codes                                3.52-1
javascript-common                        11
kbd                                      1.15.5-1ubuntu1
keepalived                               1:1.2.7-1ubuntu1
keyboard-configuration                   1.70ubuntu8
klibc-utils                              2.0.3-0ubuntu1
kmod                                     15-0ubuntu6
kpartx                                   0.4.9-3ubuntu7.2
krb5-locales                             1.12+dfsg-2ubuntu5.1
krb5-multidev                            1.12+dfsg-2ubuntu5.1
landscape-common                         14.12-0ubuntu0.14.04
language-pack-en                         1:14.04+20150219
language-pack-en-base                    1:14.04+20150219
language-selector-common                 0.129.3
laptop-detect                            0.13.7ubuntu2
less                                     458-2
libaccountsservice0:amd64                0.6.35-0ubuntu7.1
libacl1:amd64                            2.2.52-1
libaio1:amd64                            0.3.109-4
libalgorithm-diff-perl                   1.19.02-3
libalgorithm-diff-xs-perl                0.04-2build4
libalgorithm-merge-perl                  0.08-2
libapache2-mod-wsgi                      3.4-4ubuntu2.1.14.04.2
libapparmor1:amd64                       2.8.95~2430-0ubuntu5.1
libapparmor-perl                         2.8.95~2430-0ubuntu5.1
libapr1:amd64                            1.5.0-1
libaprutil1:amd64                        1.5.3-1
libaprutil1-dbd-sqlite3:amd64            1.5.3-1
libaprutil1-ldap:amd64                   1.5.3-1
libapt-inst1.5:amd64                     1.0.1ubuntu2.6
libapt-pkg4.12:amd64                     1.0.1ubuntu2.6
libapt-pkg-perl                          0.1.29build1
libarchive-extract-perl                  0.70-1
libarchive-zip-perl                      1.30-7
libasan0:amd64                           4.8.2-19ubuntu1
libasn1-8-heimdal:amd64                  1.6~git20131207+dfsg-1ubuntu1
libasound2:amd64                         1.0.27.2-3ubuntu7
libasound2-data                          1.0.27.2-3ubuntu7
libasprintf0c2:amd64                     0.18.3.1-1ubuntu3
libasprintf-dev:amd64                    0.18.3.1-1ubuntu3
libasyncns0:amd64                        0.8-4ubuntu2
libatomic1:amd64                         4.8.2-19ubuntu1
libattr1:amd64                           1:2.4.47-1ubuntu1
libaudit1:amd64                          1:2.3.2-2ubuntu1
libaudit-common                          1:2.3.2-2ubuntu1
libaugeas0                               1.2.0-0ubuntu1.1
libauthen-sasl-perl                      2.1500-1
libautodie-perl                          2.23-1
libavahi-client3:amd64                   0.6.31-4ubuntu1
libavahi-common3:amd64                   0.6.31-4ubuntu1
libavahi-common-data:amd64               0.6.31-4ubuntu1
libbind9-90                              1:9.9.5.dfsg-3ubuntu0.1
libblas3                                 1.2.20110419-7
libblkid1:amd64                          2.20.1-5.1ubuntu20.4
libbluetooth3:amd64                      4.101-0ubuntu13.1
libboost-filesystem1.54.0:amd64          1.54.0-4ubuntu3.1
libboost-iostreams1.54.0:amd64           1.54.0-4ubuntu3.1
libboost-program-options1.54.0:amd64     1.54.0-4ubuntu3.1
libboost-system1.54.0:amd64              1.54.0-4ubuntu3.1
libboost-thread1.54.0:amd64              1.54.0-4ubuntu3.1
libbrlapi0.6:amd64                       5.0-2ubuntu2
libbsd0:amd64                            0.6.0-2ubuntu1
libbz2-1.0:amd64                         1.0.6-5
libc6:amd64                              2.19-0ubuntu6.6
libc6-dev:amd64                          2.19-0ubuntu6.6
libcaca0:amd64                           0.99.beta18-1ubuntu5
libcairo2:amd64                          1.13.0~20140204-0ubuntu1.1
libcap2:amd64                            1:2.24-0ubuntu2
libcap2-bin                              1:2.24-0ubuntu2
libcap-ng0                               0.7.3-1ubuntu2
libc-bin                                 2.19-0ubuntu6.5
libc-dev-bin                             2.19-0ubuntu6.6
libcdt5                                  2.36.0-0ubuntu3.1
libcephfs1                               0.80.9-0ubuntu0.14.04.2
libcgmanager0:amd64                      0.24-0ubuntu7.3
libcgraph6                               2.36.0-0ubuntu3.1
libck-connector0:amd64                   0.4.5-3.1ubuntu2
libclass-accessor-perl                   0.34-1
libclone-perl                            0.36-1
libcloog-isl4:amd64                      0.18.2-1
libcomerr2:amd64                         1.42.9-3ubuntu1.2
libcommon-sense-perl                     3.72-2build1
libconfig-general-perl                   2.52-1
libcroco3:amd64                          0.6.8-2ubuntu1
libcryptsetup4                           2:1.6.1-1ubuntu1
libcurl3:amd64                           7.35.0-1ubuntu2.5
libcurl3-gnutls:amd64                    7.35.0-1ubuntu2.3
libcwidget3                              0.5.16-3.5ubuntu1
libdaemon0                               0.14-2ubuntu1
libdatrie1:amd64                         0.2.8-1
libdb5.3:amd64                           5.3.28-3ubuntu3
libdbd-mysql-perl                        4.025-1
libdbi-perl                              1.630-1
libdbus-1-3:amd64                        1.6.18-0ubuntu4.3
libdbus-glib-1-2:amd64                   0.100.2-1
libdebconfclient0:amd64                  0.187ubuntu1
libdevmapper1.02.1:amd64                 2:1.02.77-6ubuntu2
libdevmapper-event1.02.1:amd64           2:1.02.77-6ubuntu2
libdigest-hmac-perl                      1.03+dfsg-1
libdistro-info-perl                      0.12
libdns100                                1:9.9.5.dfsg-3ubuntu0.1
libdpkg-perl                             1.17.5ubuntu5.4
libdrm2:amd64                            2.4.56-1~ubuntu2
libedit2:amd64                           3.1-20130712-2
libelf1:amd64                            0.158-0ubuntu5.2
libemail-valid-perl                      1.192-1
libencode-locale-perl                    1.03-1
libept1.4.12:amd64                       1.0.12
liberror-perl                            0.17-1.1
libestr0                                 0.1.9-0ubuntu2
libevent-2.0-5:amd64                     2.0.21-stable-1ubuntu1.14.04.1
libexpat1:amd64                          2.1.0-4ubuntu1
libexpat1-dev:amd64                      2.1.0-4ubuntu1
libexporter-lite-perl                    0.02-2
libfakeroot:amd64                        1.20-3ubuntu2
libfdt1:amd64                            1.4.0+dfsg-1
libffi6:amd64                            3.1~rc1+r3.0.13-12
libffi-dev:amd64                         3.1~rc1+r3.0.13-12
libfile-basedir-perl                     0.03-1fakesync1
libfile-fcntllock-perl                   0.14-2build1
libfile-listing-perl                     6.04-1
libflac8:amd64                           1.3.0-2ubuntu0.14.04.1
libfont-afm-perl                         1.20-1
libfontconfig1:amd64                     2.11.0-0ubuntu4.1
libfreetype6:amd64                       2.5.2-1ubuntu2.4
libfribidi0:amd64                        0.19.6-1
libfuse2:amd64                           2.9.2-4ubuntu4
libgc1c2:amd64                           1:7.2d-5ubuntu2
libgcc1:amd64                            1:4.9.1-0ubuntu1
libgcc-4.8-dev:amd64                     4.8.2-19ubuntu1
libgck-1-0:amd64                         3.10.1-1
libgcr-3-common                          3.10.1-1
libgcr-base-3-1:amd64                    3.10.1-1
libgcrypt11:amd64                        1.5.3-2ubuntu4.1
libgd3:amd64                             2.1.0-3
libgdbm3:amd64                           1.8.3-12build1
libgeoip1:amd64                          1.6.0-1
libgettextpo0:amd64                      0.18.3.1-1ubuntu3
libgettextpo-dev:amd64                   0.18.3.1-1ubuntu3
libgfortran3:amd64                       4.8.2-19ubuntu1
libgirepository-1.0-1                    1.40.0-1ubuntu0.2
libglib2.0-0:amd64                       2.40.2-0ubuntu1
libglib2.0-data                          2.40.2-0ubuntu1
libgmp10:amd64                           2:5.1.3+dfsg-1ubuntu1
libgnutls26:amd64                        2.12.23-12ubuntu2.1
libgnutls-openssl27:amd64                2.12.23-12ubuntu2.1
libgomp1:amd64                           4.8.2-19ubuntu1
libgoogle-perftools4                     2.1-2ubuntu1
libgpg-error0:amd64                      1.12-0.2ubuntu1
libgpm2:amd64                            1.20.4-6.1
libgraphite2-3:amd64                     1.2.4-1ubuntu1
libgssapi3-heimdal:amd64                 1.6~git20131207+dfsg-1ubuntu1
libgssapi-krb5-2:amd64                   1.12+dfsg-2ubuntu5.1
libgssrpc4:amd64                         1.12+dfsg-2ubuntu5.1
libgvc6                                  2.36.0-0ubuntu3.1
libgvpr2                                 2.36.0-0ubuntu3.1
libharfbuzz0b:amd64                      0.9.27-1ubuntu1
libhcrypto4-heimdal:amd64                1.6~git20131207+dfsg-1ubuntu1
libheimbase1-heimdal:amd64               1.6~git20131207+dfsg-1ubuntu1
libheimntlm0-heimdal:amd64               1.6~git20131207+dfsg-1ubuntu1
libhtml-format-perl                      2.11-1
libhtml-form-perl                        6.03-1
libhtml-parser-perl                      3.71-1build1
libhtml-tagset-perl                      3.20-2
libhtml-template-perl                    2.95-1
libhtml-tree-perl                        5.03-1
libhttp-cookies-perl                     6.00-2
libhttp-daemon-perl                      6.01-1
libhttp-date-perl                        6.02-1
libhttp-message-perl                     6.06-1
libhttp-negotiate-perl                   6.00-2
libhx509-5-heimdal:amd64                 1.6~git20131207+dfsg-1ubuntu1
libibverbs1                              1.1.7-1ubuntu1
libice6:amd64                            2:1.0.8-2
libicu52:amd64                           52.1-3ubuntu0.2
libidn11:amd64                           1.28-1ubuntu2
libio-html-perl                          1.00-1
libio-pty-perl                           1:1.08-1build4
libio-socket-inet6-perl                  2.71-1
libio-socket-ssl-perl                    1.965-1ubuntu1
libio-string-perl                        1.08-3
libio-stringy-perl                       2.110-5
libipc-run-perl                          0.92-1
libipc-system-simple-perl                1.25-2
libipset3:amd64                          6.20.1-1
libisc95                                 1:9.9.5.dfsg-3ubuntu0.1
libisccc90                               1:9.9.5.dfsg-3ubuntu0.1
libisccfg90                              1:9.9.5.dfsg-3ubuntu0.1
libisl10:amd64                           0.12.2-1
libitm1:amd64                            4.8.2-19ubuntu1
libiw30:amd64                            30~pre9-8ubuntu1
libjbig0:amd64                           2.0-2ubuntu4.1
libjpeg8:amd64                           8c-2ubuntu8
libjpeg-turbo8:amd64                     1.3.0-0ubuntu2
libjs-jquery                             1.7.2+dfsg-2ubuntu1
libjs-jquery-hotkeys                     0~20130707+git2d51e3a9+dfsg-2ubuntu1
libjs-jquery-isonscreen                  1.2.0-1
libjs-jquery-metadata                    8-2
libjs-jquery-tablesorter                 8-2
libjson0:amd64                           0.11-3ubuntu1.2
libjson-c2:amd64                         0.11-3ubuntu1.2
libjson-perl                             2.61-1
libjson-xs-perl                          2.340-1build1
libjs-sphinxdoc                          1.2.2+dfsg-1ubuntu1.1
libjs-underscore                         1.4.4-2ubuntu1
libk5crypto3:amd64                       1.12+dfsg-2ubuntu5.1
libkadm5clnt-mit9:amd64                  1.12+dfsg-2ubuntu5.1
libkadm5srv-mit9:amd64                   1.12+dfsg-2ubuntu5.1
libkdb5-7:amd64                          1.12+dfsg-2ubuntu5.1
libkeyutils1:amd64                       1.5.6-1
libklibc                                 2.0.3-0ubuntu1
libkmod2:amd64                           15-0ubuntu6
libkrb5-26-heimdal:amd64                 1.6~git20131207+dfsg-1ubuntu1
libkrb5-3:amd64                          1.12+dfsg-2ubuntu5.1
libkrb5-dev                              1.12+dfsg-2ubuntu5.1
libkrb5support0:amd64                    1.12+dfsg-2ubuntu5.1
liblapack3                               3.5.0-2ubuntu1
liblcms2-2:amd64                         2.5-0ubuntu4
libldap-2.4-2:amd64                      2.4.31-1+nmu2ubuntu8
libldap2-dev:amd64                       2.4.31-1+nmu2ubuntu8
libleveldb1:amd64                        1.15.0-2
liblist-moreutils-perl                   0.33-1build3
liblocale-gettext-perl                   1.05-7build3
liblockfile1:amd64                       1.09-6ubuntu1
liblockfile-bin                          1.09-6ubuntu1
liblog-message-simple-perl               0.10-1
libltdl7:amd64                           2.4.2-1.7ubuntu1
liblwp-mediatypes-perl                   6.02-1
liblwp-protocol-https-perl               6.04-2ubuntu0.1
liblwres90                               1:9.9.5.dfsg-3ubuntu0.1
liblzma5:amd64                           5.1.1alpha+20120614-2ubuntu2
libmagic1:amd64                          1:5.14-2ubuntu3.3
libmailtools-perl                        2.12-1
libmnl0:amd64                            1.0.3-3ubuntu1
libmodule-pluggable-perl                 5.1-1
libmount1:amd64                          2.20.1-5.1ubuntu20.4
libmpc3:amd64                            1.0.1-1ubuntu1
libmpdec2:amd64                          2.4.0-6
libmpfr4:amd64                           3.1.2-1
libmysqlclient18:amd64                   5.5.43-0ubuntu0.14.04.1
libmysqlclient-dev                       5.5.43-0ubuntu0.14.04.1
libncurses5:amd64                        5.9+20140118-1ubuntu1
libncursesw5:amd64                       5.9+20140118-1ubuntu1
libnetcf1                                1:0.2.3-4ubuntu1
libnet-dns-perl                          0.68-1.2build1
libnet-domain-tld-perl                   1.70-1
libnetfilter-conntrack3:amd64            1.0.4-1
libnetfilter-cthelper0:amd64             1.0.0-1ubuntu1
libnetfilter-queue1                      1.0.2-1
libnet-http-perl                         6.06-1
libnet-ip-perl                           1.26-1
libnet-smtp-ssl-perl                     1.01-3
libnet-ssleay-perl                       1.58-1
libnewt0.52:amd64                        0.52.15-2ubuntu5
libnfnetlink0:amd64                      1.0.1-2
libnih1:amd64                            1.0.3-4ubuntu25
libnih-dbus1:amd64                       1.0.3-4ubuntu25
libnl-3-200:amd64                        3.2.21-1
libnl-genl-3-200:amd64                   3.2.21-1
libnl-route-3-200:amd64                  3.2.21-1
libnspr4:amd64                           2:4.10.7-0ubuntu0.14.04.1
libnspr4-dev                             2:4.10.7-0ubuntu0.14.04.1
libnss3:amd64                            2:3.17.4-0ubuntu0.14.04.1
libnss3-nssdb                            2:3.17.4-0ubuntu0.14.04.1
libnuma1:amd64                           2.0.9~rc5-1ubuntu2
libodbc1:amd64                           2.2.14p2-5ubuntu5
libogg0:amd64                            1.3.1-1ubuntu1
libp11-kit0:amd64                        0.20.2-2ubuntu2
libpam0g:amd64                           1.1.8-1ubuntu2
libpam-cap:amd64                         1:2.24-0ubuntu2
libpam-modules:amd64                     1.1.8-1ubuntu2
libpam-modules-bin                       1.1.8-1ubuntu2
libpam-runtime                           1.1.8-1ubuntu2
libpam-systemd:amd64                     204-5ubuntu20.10
libpango-1.0-0:amd64                     1.36.3-1ubuntu1.1
libpangocairo-1.0-0:amd64                1.36.3-1ubuntu1.1
libpangoft2-1.0-0:amd64                  1.36.3-1ubuntu1.1
libpaper1:amd64                          1.1.24+nmu2ubuntu3
libpaper-utils                           1.1.24+nmu2ubuntu3
libparse-debcontrol-perl                 2.005-4
libparse-debianchangelog-perl            1.2.0-1ubuntu1
libparted0debian1:amd64                  2.3-19ubuntu1
libpathplan4                             2.36.0-0ubuntu3.1
libpcap0.8:amd64                         1.5.3-2
libpci3:amd64                            1:3.2.1-1ubuntu5
libpciaccess0:amd64                      0.13.2-1
libpcre3:amd64                           1:8.31-2ubuntu2
libpcre3-dev:amd64                       1:8.31-2ubuntu2
libpcrecpp0:amd64                        1:8.31-2ubuntu2
libpcsclite1:amd64                       1.8.10-1ubuntu1
libperl5.18                              5.18.2-2ubuntu1
libperlio-gzip-perl                      0.18-1build3
libpipeline1:amd64                       1.3.0-1
libpixman-1-0:amd64                      0.30.2-2ubuntu1
libplymouth2:amd64                       0.8.8-0ubuntu17.1
libpng12-0:amd64                         1.2.50-1ubuntu2
libpod-latex-perl                        0.61-1
libpolkit-agent-1-0:amd64                0.105-4ubuntu2
libpolkit-backend-1-0:amd64              0.105-4ubuntu2
libpolkit-gobject-1-0:amd64              0.105-4ubuntu2
libpopt0:amd64                           1.16-8ubuntu1
libpq5                                   9.3.6-0ubuntu0.14.04
libpq-dev                                9.3.6-0ubuntu0.14.04
libprocps3:amd64                         1:3.3.9-1ubuntu2.2
libpulse0:amd64                          1:4.0-0ubuntu11.1
libpython2.7:amd64                       2.7.6-8
libpython2.7-dev:amd64                   2.7.6-8
libpython2.7-minimal:amd64               2.7.6-8
libpython2.7-stdlib:amd64                2.7.6-8
libpython3.4-minimal:amd64               3.4.0-2ubuntu1
libpython3.4-stdlib:amd64                3.4.0-2ubuntu1
libpython3-stdlib:amd64                  3.4.0-0ubuntu2
libpython-dev:amd64                      2.7.5-5ubuntu3
libpython-stdlib:amd64                   2.7.5-5ubuntu3
libquadmath0:amd64                       4.8.2-19ubuntu1
librados2                                0.80.9-0ubuntu0.14.04.2
librbd1                                  0.80.9-0ubuntu0.14.04.2
librdmacm1                               1.0.16-1
libreadline5:amd64                       5.2+dfsg-2
libreadline6:amd64                       6.3-4ubuntu2
libroken18-heimdal:amd64                 1.6~git20131207+dfsg-1ubuntu1
librtmp0:amd64                           2.4+20121230.gitdf6c518-1
libsasl2-2:amd64                         2.1.25.dfsg1-17build1
libsasl2-dev                             2.1.25.dfsg1-17build1
libsasl2-modules:amd64                   2.1.25.dfsg1-17build1
libsasl2-modules-db:amd64                2.1.25.dfsg1-17build1
libsctp1:amd64                           1.0.15+dfsg-1
libsdl1.2debian:amd64                    1.2.15-8ubuntu1.1
libseccomp2:amd64                        2.1.0+dfsg-1
libselinux1:amd64                        2.2.2-1ubuntu0.1
libsemanage1:amd64                       2.2-1
libsemanage-common                       2.2-1
libsensors4:amd64                        1:3.3.4-2ubuntu1
libsepol1:amd64                          2.2-1ubuntu0.1
libsgutils2-2                            1.36-1ubuntu1
libsigc++-2.0-0c2a:amd64                 2.2.10-0.2ubuntu2
libsigsegv2:amd64                        2.10-2
libslang2:amd64                          2.2.4-15ubuntu1
libsm6:amd64                             2:1.2.1-2
libsnappy1                               1.1.0-1ubuntu1
libsndfile1:amd64                        1.0.25-7ubuntu2
libsnmp30:amd64                          5.7.2~dfsg-8.1ubuntu3
libsnmp-base                             5.7.2~dfsg-8.1ubuntu3
libsocket6-perl                          0.25-1
libspice-server1:amd64                   0.12.4-0nocelt2
libsqlite3-0:amd64                       3.8.2-1ubuntu2
libss2:amd64                             1.42.9-3ubuntu1
libssl1.0.0:amd64                        1.0.1f-1ubuntu2.11
libssl-dev:amd64                         1.0.1f-1ubuntu2.11
libssl-doc                               1.0.1f-1ubuntu2.11
libstdc++-4.8-dev:amd64                  4.8.2-19ubuntu1
libstdc++6:amd64                         4.8.2-19ubuntu1
libsub-identify-perl                     0.04-1build3
libsub-name-perl                         0.05-1build4
libsysfs2:amd64                          2.1.0+repack-3ubuntu1
libsystemd-daemon0:amd64                 204-5ubuntu20.10
libsystemd-login0:amd64                  204-5ubuntu20.10
libtasn1-6:amd64                         3.4-3ubuntu0.1
libtcl8.6:amd64                          8.6.1-4ubuntu1
libtcmalloc-minimal4                     2.1-2ubuntu1
libterm-readkey-perl                     2.31-1
libterm-ui-perl                          0.42-1
libtext-charwidth-perl                   0.04-7build3
libtext-iconv-perl                       1.7-5build2
libtext-levenshtein-perl                 0.06~01-2
libtext-soundex-perl                     3.4-1build1
libtext-wrapi18n-perl                    0.06-7
libthai0:amd64                           0.1.20-3
libthai-data                             0.1.20-3
libtidy-0.99-0                           20091223cvs-1.2ubuntu1
libtie-ixhash-perl                       1.23-1
libtiff5:amd64                           4.0.3-7ubuntu0.3
libtimedate-perl                         2.3000-1
libtinfo5:amd64                          5.9+20140118-1ubuntu1
libtk8.6:amd64                           8.6.1-3ubuntu2
libtsan0:amd64                           4.8.2-19ubuntu1
libudev1:amd64                           204-5ubuntu20.10
libunistring0:amd64                      0.9.3-5ubuntu3
libunwind8                               1.1-2.2ubuntu3
liburi-perl                              1.60-1
libusb-0.1-4:amd64                       2:0.1.12-23.3ubuntu1
libusb-1.0-0:amd64                       2:1.0.17-1ubuntu2
libusbredirparser1:amd64                 0.6-2ubuntu1
libustr-1.0-1:amd64                      1.0.4-3ubuntu2
libuuid1:amd64                           2.20.1-5.1ubuntu20.4
libv8-3.14.5                             3.14.5.8-5ubuntu2
libvirt0                                 1.2.2-0ubuntu13.1.10
libvirt-bin                              1.2.2-0ubuntu13.1.10
libvorbis0a:amd64                        1.3.2-1.3ubuntu1
libvorbisenc2:amd64                      1.3.2-1.3ubuntu1
libvpx1:amd64                            1.3.0-2
libwebp5:amd64                           0.4.0-4
libwebpmux1:amd64                        0.4.0-4
libwind0-heimdal:amd64                   1.6~git20131207+dfsg-1ubuntu1
libwrap0:amd64                           7.6.q-25
libwww-perl                              6.05-2
libwww-robotrules-perl                   6.01-1
libx11-6:amd64                           2:1.6.2-1ubuntu2
libx11-data                              2:1.6.2-1ubuntu2
libx86-1:amd64                           1.1+ds1-10
libxapian22                              1.2.16-2ubuntu1
libxau6:amd64                            1:1.0.8-1
libxaw7:amd64                            2:1.0.12-1
libxcb1:amd64                            1.10-2ubuntu1
libxcb-render0:amd64                     1.10-2ubuntu1
libxcb-shm0:amd64                        1.10-2ubuntu1
libxdmcp6:amd64                          1:1.1.1-1
libxen-4.4                               4.4.1-0ubuntu0.14.04.5
libxenstore3.0                           4.4.1-0ubuntu0.14.04.5
libxext6:amd64                           2:1.3.2-1
libxft2:amd64                            2.3.1-2
libxml2:amd64                            2.9.1+dfsg1-3ubuntu4.4
libxml2-dev:amd64                        2.9.1+dfsg1-3ubuntu4.4
libxml2-utils                            2.9.1+dfsg1-3ubuntu4.4
libxmu6:amd64                            2:1.1.1-1
libxmuu1:amd64                           2:1.1.1-1
libxpm4:amd64                            1:3.5.10-1
libxrender1:amd64                        1:0.9.8-1build0.14.04.1
libxslt1.1:amd64                         1.1.28-2build1
libxslt1-dev:amd64                       1.1.28-2build1
libxss1:amd64                            1:1.2.2-1
libxt6:amd64                             1:1.1.4-1
libxtables10                             1.4.21-1ubuntu1
libyajl2:amd64                           2.0.4-4
libyaml-0-2:amd64                        0.1.4-3ubuntu3.1
libyaml-dev:amd64                        0.1.4-3ubuntu3.1
lintian                                  2.5.22ubuntu1
linux-firmware                           1.127.11
linux-generic-lts-utopic                 3.16.0.30.23
linux-headers-3.16.0-30                  3.16.0-30.40~14.04.1
linux-headers-3.16.0-30-generic          3.16.0-30.40~14.04.1
linux-headers-generic-lts-utopic         3.16.0.30.23
linux-image-3.16.0-30-generic            3.16.0-30.40~14.04.1
linux-image-extra-3.16.0-30-generic      3.16.0-30.40~14.04.1
linux-image-generic-lts-utopic           3.16.0.30.23
linux-libc-dev:amd64                     3.13.0-49.83
lksctp-tools                             1.0.15+dfsg-1
locales                                  2.13+git20120306-12.1
lockfile-progs                           0.1.17
login                                    1:4.1.5.1-1ubuntu9
logrotate                                3.8.7-1ubuntu1
lsb-base                                 4.1+Debian11ubuntu6
lsb-release                              4.1+Debian11ubuntu6
lshw                                     02.16-2ubuntu1.2
lsof                                     4.86+dfsg-1ubuntu2
ltrace                                   0.7.3-4ubuntu5.1
lvm2                                     2.02.98-6ubuntu2
lxc-docker                               1.6.0
lxc-docker-1.6.0                         1.6.0
make                                     3.81-8.2ubuntu3
makedev                                  2.3.1-93ubuntu1
man-db                                   2.6.7.1-1ubuntu1
manpages                                 3.54-1ubuntu1
manpages-dev                             3.54-1ubuntu1
mawk                                     1.3.3-17ubuntu2
memcached                                1.4.14-0ubuntu9
memtest86+                               4.20-1.1ubuntu8
mime-support                             3.54ubuntu1.1
mlocate                                  0.26-1ubuntu1
module-init-tools                        15-0ubuntu6
mongodb-clients                          1:2.4.9-1ubuntu2
mongodb-server                           1:2.4.9-1ubuntu2
mount                                    2.20.1-5.1ubuntu20.4
mountall                                 2.53
msr-tools                                1.3-2
mtr-tiny                                 0.85-2
multiarch-support                        2.19-0ubuntu6.5
mysql-client-5.5                         5.5.43-0ubuntu0.14.04.1
mysql-client-core-5.5                    5.5.43-0ubuntu0.14.04.1
mysql-common                             5.5.43-0ubuntu0.14.04.1
mysql-server                             5.5.43-0ubuntu0.14.04.1
mysql-server-5.5                         5.5.43-0ubuntu0.14.04.1
mysql-server-core-5.5                    5.5.43-0ubuntu0.14.04.1
nano                                     2.2.6-1ubuntu1
ncurses-base                             5.9+20140118-1ubuntu1
ncurses-bin                              5.9+20140118-1ubuntu1
ncurses-term                             5.9+20140118-1ubuntu1
netbase                                  5.2
netcat-openbsd                           1.105-7ubuntu1
net-tools                                1.60-25ubuntu2.1
ntfs-3g                                  1:2013.1.13AR.1-2ubuntu2
ntpdate                                  1:4.2.6.p5+dfsg-3ubuntu2.14.04.2
open-iscsi                               2.0.873-3ubuntu9
openssh-client                           1:6.6p1-2ubuntu2
openssh-server                           1:6.6p1-2ubuntu2
openssh-sftp-server                      1:6.6p1-2ubuntu2
openssl                                  1.0.1f-1ubuntu2.11
openvswitch-common                       2.0.2-0ubuntu0.14.04.1
openvswitch-switch                       2.0.2-0ubuntu0.14.04.1
os-prober                                1.63ubuntu1
parted                                   2.3-19ubuntu1
passwd                                   1:4.1.5.1-1ubuntu9
patch                                    2.7.1-4ubuntu1
patchutils                               0.3.2-3
pciutils                                 1:3.2.1-1ubuntu5
perl                                     5.18.2-2ubuntu1
perl-base                                5.18.2-2ubuntu1
perl-modules                             5.18.2-2ubuntu1
pkg-config                               0.26-1ubuntu4
plymouth                                 0.8.8-0ubuntu17.1
plymouth-theme-ubuntu-text               0.8.8-0ubuntu17.1
pm-utils                                 1.4.1-13ubuntu0.1
policykit-1                              0.105-4ubuntu2
popularity-contest                       1.57ubuntu1
postgresql-client-common                 154ubuntu1
postgresql-common                        154ubuntu1
postgresql-server-dev-9.3                9.3.6-0ubuntu0.14.04
postgresql-server-dev-all                154ubuntu1
powermgmt-base                           1.31build1
ppp                                      2.4.5-5.1ubuntu2.1
pppconfig                                2.3.19ubuntu1
pppoeconf                                1.20ubuntu1
procps                                   1:3.3.9-1ubuntu2.2
psmisc                                   22.20-1ubuntu2
pylint                                   1.1.0-1
python2.7                                2.7.6-8
python                                   2.7.5-5ubuntu3
python2.7-dev                            2.7.6-8
python2.7-minimal                        2.7.6-8
python3                                  3.4.0-0ubuntu2
python3.4                                3.4.0-2ubuntu1
python3.4-minimal                        3.4.0-2ubuntu1
python3-apport                           2.14.1-0ubuntu3.7
python3-apt                              0.9.3.5ubuntu1
python3-chardet                          2.2.1-2~ubuntu1
python3-commandnotfound                  0.3ubuntu12
python3-dbus                             1.2.0-2build2
python3-debian                           0.1.21+nmu2ubuntu2
python3-distupgrade                      1:0.220.7
python3-gdbm:amd64                       3.4.0-0ubuntu1
python3-gi                               3.12.0-1ubuntu1
python3-magic                            1:5.14-2ubuntu3.3
python3-minimal                          3.4.0-0ubuntu2
python3-newt                             0.52.15-2ubuntu5
python3-pkg-resources                    3.3-1ubuntu1
python3-problem-report                   2.14.1-0ubuntu3.7
python3-pycurl                           7.19.3-0ubuntu3
python3-six                              1.5.2-1
python3-software-properties              0.92.37.3
python3-update-manager                   1:0.196.12
python-anyjson                           0.3.3-1build1
python-apt                               0.9.3.5ubuntu1
python-apt-common                        0.9.3.5ubuntu1
python-astroid                           1.0.1-1
python-beautifulsoup                     3.2.1-1
python-blinker                           1.3.dfsg1-1ubuntu2
python-bson                              2.6.3-1build1
python-bson-ext                          2.6.3-1build1
python-ceph                              0.80.9-0ubuntu0.14.04.2
python-chardet                           2.0.1-2build2
python-cheetah                           2.4.4-3.fakesyncbuild1
python-cherrypy3                         3.2.2-4ubuntu5
python-colorama                          0.2.5-0.1ubuntu2
python-configobj                         4.7.2+ds-5build1
python-coverage                          3.7.1+dfsg.1-1ubuntu2
python-dateutil                          1.5+dfsg-1ubuntu1
python-debian                            0.1.21+nmu2ubuntu2
python-decorator                         3.4.0-2build1
python-dev                               2.7.5-5ubuntu3
python-distlib                           0.1.8-1ubuntu1
python-dns                               2.3.6-3
python-docutils                          0.11-3
python-egenix-mxdatetime                 3.2.7-1build1
python-egenix-mxtools                    3.2.7-1build1
python-eventlet                          0.13.0-1ubuntu2
python-feedparser                        5.1.3-2
python-flask                             0.10.1-2build1
python-formencode                        1.2.6-1ubuntu1
python-gdbm                              2.7.5-1ubuntu1
python-greenlet                          0.4.2-1build1
python-gridfs                            2.6.3-1build1
python-html5lib                          0.999-3~ubuntu1
python-iso8601                           0.1.10-0ubuntu1
python-itsdangerous                      0.22+dfsg1-1build1
python-jinja2                            2.7.2-2
python-libvirt                           1.2.2-0ubuntu2
python-libxml2                           2.9.1+dfsg1-3ubuntu4.4
python-lockfile                          1:0.8-2ubuntu2
python-logilab-common                    0.61.0-1
python-lxml                              3.3.3-1ubuntu0.1
python-m2crypto                          0.21.1-3ubuntu5
python-markupsafe                        0.18-1build2
python-migrate                           0.8.2-3ubuntu1
python-minimal                           2.7.5-5ubuntu3
python-mox                               0.5.3-3build1
python-msgpack                           0.3.0-1ubuntu3
python-mysql.connector                   1.1.6-1
python-mysqldb                           1.2.3-2ubuntu1
python-netifaces                         0.8-3build1
python-nose                              1.3.1-2
python-numpy                             1:1.8.2-0ubuntu0.1
python-openid                            2.2.5-3ubuntu1
python-openssl                           0.13-2ubuntu6
python-pam                               0.4.2-13.1ubuntu3
python-paste                             1.7.5.1-6ubuntu3
python-pastedeploy                       1.5.2-1
python-pastedeploy-tpl                   1.5.2-1
python-pastescript                       1.7.5-3build1
python-pbr                               0.7.0-0ubuntu2
python-pil                               2.3.0-1ubuntu3
python-pkg-resources                     3.3-1ubuntu1
python-pygments                          1.6+dfsg-1ubuntu1
python-pyinotify                         0.9.4-1build1
python-pymongo                           2.6.3-1build1
python-pymongo-ext                       2.6.3-1build1
python-pysqlite2                         2.6.3-3
python-pyudev                            0.16.1-2build1
python-repoze.lru                        0.6-4
python-requestbuilder                    0.1.0~beta2-1build1
python-requests                          2.2.1-1ubuntu0.1
python-roman                             2.0.0-1
python-routes                            2.0-1build1
python-scgi                              1.13-1.1build1
python-serial                            2.6-1build1
python-setuptools                        3.3-1ubuntu1
python-simplejson                        3.3.1-1ubuntu6
python-six                               1.5.2-1
python-sphinx                            1.2.2+dfsg-1ubuntu1.1
python-sqlalchemy                        0.8.4-1build1
python-sqlalchemy-ext                    0.8.4-1build1
python-suds                              0.4.1-11ubuntu0.1
python-tempita                           0.5.2-1build1
python-tk                                2.7.5-1ubuntu1
python-twisted-bin                       13.2.0-1ubuntu1
python-twisted-core                      13.2.0-1ubuntu1
python-urllib3                           1.7.1-1ubuntu0.1
python-utidylib                          0.2-9build1
python-vm-builder                        0.12.4+bzr489-0ubuntu2
python-webob                             1.3.1-1
python-werkzeug                          0.9.4+dfsg-1.1ubuntu2
python-wheel                             0.24.0-1~ubuntu1
python-xapian                            1.2.16-2ubuntu1
python-xattr                             0.6.4-2build1
python-zope.interface                    4.0.5-1ubuntu4
qemu-keymaps                             2.0.0+dfsg-2ubuntu1.10
qemu-kvm                                 2.0.0+dfsg-2ubuntu1.10
qemu-system-common                       2.0.0+dfsg-2ubuntu1.10
qemu-system-x86                          2.0.0+dfsg-2ubuntu1.10
qemu-utils                               2.0.0+dfsg-2ubuntu1.11
rabbitmq-server                          3.2.4-1
radvd                                    1:1.9.1-1.1ubuntu2
readline-common                          6.3-4ubuntu2
resolvconf                               1.69ubuntu1.1
rsync                                    3.1.0-2ubuntu0.1
rsyslog                                  7.4.4-1ubuntu2.5
run-one                                  1.17-0ubuntu1
screen                                   4.1.0~20120320gitdb59704-9
seabios                                  1.7.4-4
sed                                      4.2.2-4ubuntu1
sensible-utils                           0.0.9
sg3-utils                                1.36-1ubuntu1
sgml-base                                1.26+nmu4ubuntu1
shared-mime-info                         1.2-0ubuntu3
sharutils                                1:4.14-1ubuntu1
socat                                    1.7.2.3-1
software-properties-common               0.92.37.3
sphinx-common                            1.2.2+dfsg-1ubuntu1.1
sphinx-doc                               1.2.2+dfsg-1ubuntu1.1
sqlite3                                  3.8.2-1ubuntu2
ssh-import-id                            3.21-0ubuntu1
ssl-cert                                 1.0.33
strace                                   4.8-1ubuntu5
sudo                                     1.8.9p5-1ubuntu1.1
sysfsutils                               2.1.0+repack-3ubuntu1
systemd-services                         204-5ubuntu20.10
systemd-shim                             6-2bzr1
sysvinit-utils                           2.88dsf-41ubuntu6
sysv-rc                                  2.88dsf-41ubuntu6
t1utils                                  1.37-2ubuntu1
tar                                      1.27.1-1
tasksel                                  2.88ubuntu15
tasksel-data                             2.88ubuntu15
tcpd                                     7.6.q-25
tcpdump                                  4.5.1-2ubuntu1.2
telnet                                   0.17-36build2
tgt                                      1:1.0.43-0ubuntu4
time                                     1.7-24
tmux                                     1.8-5
tzdata                                   2015a-0ubuntu0.14.04
ubuntu-keyring                           2012.05.19
ubuntu-minimal                           1.325
ubuntu-release-upgrader-core             1:0.220.7
ubuntu-standard                          1.325
ubuntu-vm-builder                        0.12.4+bzr489-0ubuntu2
ucf                                      3.0027+nmu1
udev                                     204-5ubuntu20.10
ufw                                      0.34~rc-0ubuntu2
unattended-upgrades                      0.82.1ubuntu2
unzip                                    6.0-9ubuntu1.3
update-manager-core                      1:0.196.12
update-notifier-common                   0.154.1ubuntu1
upstart                                  1.12.1-0ubuntu4.2
ureadahead                               0.100.0-16
usbutils                                 1:007-2ubuntu1
util-linux                               2.20.1-5.1ubuntu20.4
uuid-runtime                             2.20.1-5.1ubuntu20.4
vbetool                                  1.1-3
vim                                      2:7.4.052-1ubuntu3
vim-common                               2:7.4.052-1ubuntu3
vim-runtime                              2:7.4.052-1ubuntu3
vim-tiny                                 2:7.4.052-1ubuntu3
vlan                                     1.9-3ubuntu10
w3m                                      0.5.3-15
watershed                                7
wdiff                                    1.2.1-2
wget                                     1.15-1ubuntu1.14.04.1
whiptail                                 0.52.15-2ubuntu5
wireless-regdb                           2013.02.13-1ubuntu1
wireless-tools                           30~pre9-8ubuntu1
wpasupplicant                            2.1-0ubuntu1.1
x11-common                               1:7.7+1ubuntu8.1
xauth                                    1:1.0.7-1ubuntu1
xfsprogs                                 3.1.9ubuntu2
xkb-data                                 2.10.1-1ubuntu1
xml-core                                 0.13+nmu2
xz-utils                                 5.1.1alpha+20120614-2ubuntu2
zlib1g:amd64                             1:1.2.8.dfsg-1ubuntu1
zlib1g-dev:amd64                         1:1.2.8.dfsg-1ubuntu1
```

Diff with my compute node 1 (10.12.181.121) installed packages

```
$ diff controller.dpkg.txt compute.dpkg.txt
30a31
> btrfs-tools                              3.12-1
37,38d37
< ceph                                     0.80.9-0ubuntu0.14.04.2
< ceph-common                              0.80.9-0ubuntu0.14.04.2
52a52
> cryptsetup                               2:1.6.1-1ubuntu1
61,62d60
< debootstrap                              1.0.59ubuntu0.2
< devscripts                               2.14.1
64d61
< diffstat                                 1.58-1
66d62
< distro-info-data                         0.18ubuntu0.2
72,73d67
< docutils-common                          0.11-3
< docutils-doc                             0.11-3
77d70
< dput                                     0.9.6.4ubuntu1.1
120d112
< fping                                    3.8-1
131d122
< gdisk                                    0.8.8-1build1
135a127
> ghostscript                              9.10~dfsg-0ubuntu10.2
148a141
> gsfonts                                  1:8.11+urwcyr1.0.7~pre44-4.2ubuntu1
151d143
< hardening-includes                       2.5ubuntu2.1
153a146
> icoutils                                 0.31.0-2
163d155
< intltool-debian                          0.35.0+20060710.1
177a170
> jfsutils                                 1.1.15-2.1
190a184
> ldmtool                                  0.2.3-2ubuntu1
207d200
< libapt-pkg-perl                          0.1.29build1
209d201
< libarchive-zip-perl                      1.30-7
223d214
< libautodie-perl                          2.23-1
249d239
< libcephfs1                               0.80.9-0ubuntu0.14.04.2
254d243
< libclone-perl                            0.36-1
257d245
< libcommon-sense-perl                     3.72-2build1
260a249,251
> libcups2:amd64                           1.7.2-0ubuntu1.5
> libcupsfilters1:amd64                    1.0.52-0ubuntu1.4
> libcupsimage2:amd64                      1.7.2-0ubuntu1.5
274,275d264
< libdigest-hmac-perl                      1.03+dfsg-1
< libdistro-info-perl                      0.12
281d269
< libemail-valid-perl                      1.192-1
289d276
< libexporter-lite-perl                    0.02-2
294d280
< libfile-basedir-perl                     0.03-1fakesync1
326a313,314
> libgs9                                   9.10~dfsg-0ubuntu10.2
> libgs9-common                            9.10~dfsg-0ubuntu10.2
329a318
> libguestfs0:amd64                        1:1.24.5-1
350d338
< libicu52:amd64                           52.1-3ubuntu0.2
351a340
> libijs-0.35                              0.35-8build1
353d341
< libio-pty-perl                           1:1.08-1build4
357,359d344
< libio-stringy-perl                       2.110-5
< libipc-run-perl                          0.92-1
< libipc-system-simple-perl                1.25-2
367a353
> libjbig2dec0                             0.11+20120125-1ubuntu1
371,372d356
< libjs-jquery-hotkeys                     0~20130707+git2d51e3a9+dfsg-2ubuntu1
< libjs-jquery-isonscreen                  1.2.0-1
377,380c361,362
< libjson-perl                             2.61-1
< libjson-xs-perl                          2.340-1build1
< libjs-sphinxdoc                          1.2.2+dfsg-1ubuntu1.1
< libjs-underscore                         1.4.4-2ubuntu1
---
> libjson-glib-1.0-0:amd64                 0.16.2-1ubuntu1
> libjson-glib-1.0-common                  0.16.2-1ubuntu1
396,397c378
< libleveldb1:amd64                        1.15.0-2
< liblist-moreutils-perl                   0.33-1build3
---
> libldm-1.0-0                             0.2.3-2ubuntu1
406a388
> liblzo2-2:amd64                          2.06-1.2ubuntu1.1
420,421d401
< libnet-dns-perl                          0.68-1.2build1
< libnet-domain-tld-perl                   1.70-1
426c406
< libnet-ip-perl                           1.26-1
---
> libnetpbm10                              2:10.0-15ubuntu2
437d416
< libnspr4-dev                             2:4.10.7-0ubuntu0.14.04.1
455d433
< libparse-debcontrol-perl                 2.005-4
467d444
< libperlio-gzip-perl                      0.18-1build3
528d504
< libsub-identify-perl                     0.04-1build3
534d509
< libtcl8.6:amd64                          8.6.1-4ubuntu1
540d514
< libtext-levenshtein-perl                 0.06~01-2
545,546d518
< libtidy-0.99-0                           20091223cvs-1.2ubuntu1
< libtie-ixhash-perl                       1.23-1
550d521
< libtk8.6:amd64                           8.6.1-3ubuntu2
563a535
> libvirt-dev                              1.2.2-0ubuntu13.1.10
567,568d538
< libwebp5:amd64                           0.4.0-4
< libwebpmux1:amd64                        0.4.0-4
583a554
> libxen-dev                               4.4.1-0ubuntu0.14.04.5
586d556
< libxft2:amd64                            2.3.1-2
596d565
< libxss1:amd64                            1:1.2.2-1
602d570
< lintian                                  2.5.22ubuntu1
654a623
> netpbm                                   2:10.0-15ubuntu2
669d637
< patchutils                               0.3.2-3
678a647
> poppler-data                             0.4.6-4
690d658
< pylint                                   1.1.0-1
700d667
< python3-chardet                          2.2.1-2~ubuntu1
703d669
< python3-debian                           0.1.21+nmu2ubuntu2
707d672
< python3-magic                            1:5.14-2ubuntu3.3
710d674
< python3-pkg-resources                    3.3-1ubuntu1
713d676
< python3-six                              1.5.2-1
716d678
< python-anyjson                           0.3.3-1build1
719,721d680
< python-astroid                           1.0.1-1
< python-beautifulsoup                     3.2.1-1
< python-blinker                           1.3.dfsg1-1ubuntu2
724d682
< python-ceph                              0.80.9-0ubuntu0.14.04.2
726,728d683
< python-cheetah                           2.4.4-3.fakesyncbuild1
< python-cherrypy3                         3.2.2-4ubuntu5
< python-colorama                          0.2.5-0.1ubuntu2
730,731d684
< python-coverage                          3.7.1+dfsg.1-1ubuntu2
< python-dateutil                          1.5+dfsg-1ubuntu1
733d685
< python-decorator                         3.4.0-2build1
735,743d686
< python-distlib                           0.1.8-1ubuntu1
< python-dns                               2.3.6-3
< python-docutils                          0.11-3
< python-egenix-mxdatetime                 3.2.7-1build1
< python-egenix-mxtools                    3.2.7-1build1
< python-eventlet                          0.13.0-1ubuntu2
< python-feedparser                        5.1.3-2
< python-flask                             0.10.1-2build1
< python-formencode                        1.2.6-1ubuntu1
745d687
< python-greenlet                          0.4.2-1build1
747,751c689
< python-html5lib                          0.999-3~ubuntu1
< python-iso8601                           0.1.10-0ubuntu1
< python-itsdangerous                      0.22+dfsg1-1build1
< python-jinja2                            2.7.2-2
< python-libvirt                           1.2.2-0ubuntu2
---
> python-guestfs                           1:1.24.5-1
753,754d690
< python-lockfile                          1:0.8-2ubuntu2
< python-logilab-common                    0.61.0-1
757,758d692
< python-markupsafe                        0.18-1build2
< python-migrate                           0.8.2-3ubuntu1
760,761d693
< python-mox                               0.5.3-3build1
< python-msgpack                           0.3.0-1ubuntu3
764d695
< python-netifaces                         0.8-3build1
767d697
< python-openid                            2.2.5-3ubuntu1
770,775d699
< python-paste                             1.7.5.1-6ubuntu3
< python-pastedeploy                       1.5.2-1
< python-pastedeploy-tpl                   1.5.2-1
< python-pastescript                       1.7.5-3build1
< python-pbr                               0.7.0-0ubuntu2
< python-pil                               2.3.0-1ubuntu3
777,778d700
< python-pygments                          1.6+dfsg-1ubuntu1
< python-pyinotify                         0.9.4-1build1
781,783d702
< python-pysqlite2                         2.6.3-3
< python-pyudev                            0.16.1-2build1
< python-repoze.lru                        0.6-4
786,788d704
< python-roman                             2.0.0-1
< python-routes                            2.0-1build1
< python-scgi                              1.13-1.1build1
791d706
< python-simplejson                        3.3.1-1ubuntu6
793,798d707
< python-sphinx                            1.2.2+dfsg-1ubuntu1.1
< python-sqlalchemy                        0.8.4-1build1
< python-sqlalchemy-ext                    0.8.4-1build1
< python-suds                              0.4.1-11ubuntu0.1
< python-tempita                           0.5.2-1build1
< python-tk                                2.7.5-1ubuntu1
802,806d710
< python-utidylib                          0.2-9build1
< python-vm-builder                        0.12.4+bzr489-0ubuntu2
< python-webob                             1.3.1-1
< python-werkzeug                          0.9.4+dfsg-1.1ubuntu2
< python-wheel                             0.24.0-1~ubuntu1
808d711
< python-xattr                             0.6.4-2build1
811c714
< qemu-kvm                                 2.0.0+dfsg-2ubuntu1.10
---
> qemu-kvm                                 2.0.0+dfsg-2ubuntu1.11
817a721
> reiserfsprogs                            1:3.6.24-1
822a727
> scrub                                    2.5.2-2
832,833d736
< sphinx-common                            1.2.2+dfsg-1ubuntu1.1
< sphinx-doc                               1.2.2+dfsg-1ubuntu1.1
838a742
> supermin                                 4.1.6-1
844d747
< t1utils                                  1.37-2ubuntu1
859d761
< ubuntu-vm-builder                        0.12.4+bzr489-0ubuntu2
880d781
< wdiff                                    1.2.1-2
891a793,794
> zerofree                                 1.0.2-1ubuntu1
> zfs-fuse                                 0.7.0-10.1
```

List my controller node installed pip packages.

```
aioeventlet (0.4)
alembic (0.7.4)
amqp (1.4.6)
anyjson (0.3.3)
apt-xapian-index (0.45)
astroid (1.0.1)
Babel (1.3)
BeautifulSoup (3.2.1)
beautifulsoup4 (4.3.2)
blinker (1.3)
boto (2.34.0)
ceilometer (2015.1.1.dev1, /opt/stack/ceilometer)
ceilometermiddleware (0.1.0)
cffi (0.9.2)
chardet (2.0.1)
Cheetah (2.4.4)
CherryPy (3.2.2)
cinder (2015.1.1.dev2, /opt/stack/cinder)
cliff (1.10.1)
cliff-tablib (1.1)
cmd2 (0.6.8)
colorama (0.2.5)
configobj (4.7.2)
coverage (3.7.1)
croniter (0.3.5)
cryptography (0.8.2)
decorator (3.4.0)
discover (0.4.0)
Django (1.6.11)
django-appconf (1.0.1)
django-compressor (1.4)
django-openstack-auth (1.1.9)
django-pyscss (1.0.6)
dnspython (1.12.0)
docutils (0.11)
dogpile.cache (0.5.6)
dogpile.core (0.4.1)
ecdsa (0.13)
enum34 (1.0.4)
euca2ools (3.0.1)
eventlet (0.17.3)
extras (0.0.3)
feedparser (5.1.3)
fixtures (1.2.0)
flake8 (2.2.4)
Flask (0.10.1)
FormEncode (1.2.6)
futures (2.2.0)
glance (2015.1.1.dev1, /opt/stack/glance)
glance-store (0.4.0)
greenlet (0.4.2)
hacking (0.10.1)
happybase (0.9)
heat (2015.1.1.dev1, /opt/stack/heat)
horizon (2015.1.1.dev2, /opt/stack/horizon)
html5lib (0.999)
httplib2 (0.9)
ipaddr (2.1.11)
iso8601 (0.1.10)
itsdangerous (0.22)
Jinja2 (2.7.2)
jsonpatch (1.10)
jsonpath-rw (1.4.0)
jsonpointer (1.9)
jsonrpclib (0.1.3)
jsonschema (2.4.0)
kafka-python (0.9.3)
kazoo (2.0)
keystone (2015.1.1.dev1, /opt/stack/keystone)
keystonemiddleware (1.5.1)
kombu (3.0.7)
Landscape-Client (14.12)
libvirt-python (1.2.2)
linecache2 (1.0.0)
lockfile (0.8)
logilab-common (0.61.0)
logutils (0.3.3)
lxml (3.3.3)
M2Crypto (0.21.1)
Mako (1.0.1)
MarkupSafe (0.18)
mccabe (0.2.1)
mock (1.0.1)
mox (0.5.3)
mox3 (0.7.0)
msgpack-python (0.4.6)
mysql-connector-python (1.1.6)
MySQL-python (1.2.3)
netaddr (0.7.14)
netifaces (0.10.4)
networkx (1.9.1)
neutron (2015.1.1.dev3, /opt/stack/neutron)
neutron-fwaas (2015.1.1.dev1, /opt/stack/neutron-fwaas)
neutron-lbaas (2015.1.1.dev1, /opt/stack/neutron-lbaas)
nose (1.3.1)
nova (2015.1.1.dev8, /opt/stack/nova)
numpy (1.8.2)
oauthlib (0.7.2)
ordereddict (1.1)
os-client-config (0.8.1)
oslo.concurrency (1.8.0)
oslo.config (1.9.3)
oslo.context (0.2.0)
oslo.db (1.7.1)
oslo.i18n (1.5.0)
oslo.log (1.0.0)
oslo.messaging (1.8.2)
oslo.middleware (1.0.0)
oslo.policy (0.3.2)
oslo.rootwrap (1.6.0)
oslo.serialization (1.4.0)
oslosphinx (2.5.0)
oslotest (1.5.1)
oslo.utils (1.4.0)
oslo.versionedobjects (0.1.1)
oslo.vmware (0.11.1)
osprofiler (0.3.0)
PAM (0.4.2)
paramiko (1.15.2)
passlib (1.6.2)
Paste (1.7.5.1)
PasteDeploy (1.5.2)
PasteScript (1.7.5)
pbr (0.11.0)
pecan (0.8.3)
pep8 (1.5.7)
Pillow (2.3.0)
Pint (0.6)
pip (7.0.0)
ply (3.6)
posix-ipc (0.9.9)
prettytable (0.7.2)
psutil (1.2.1)
py (1.4.26)
pyasn1 (0.1.7)
pyasn1-modules (0.0.5)
pycadf (0.8.0)
pycparser (2.12)
pycrypto (2.6.1)
pydns (2.3.6)
PyECLib (1.0.7)
pyflakes (0.8.1)
Pygments (1.6)
pyinotify (0.9.4)
pylint (1.1.0)
pymemcache (1.2.9)
pymongo (2.6.3)
pyOpenSSL (0.15.1)
pyparsing (2.0.3)
pysaml2 (2.4.0)
pyScss (1.2.1)
pyserial (2.6)
pysnmp (4.2.5)
pysqlite (2.6.3)
python-apt (0.9.3.5ubuntu1)
python-barbicanclient (3.0.1)
python-ceilometerclient (1.0.14)
python-cinderclient (1.1.1)
python-dateutil (1.5)
python-debian (0.1.21-nmu2ubuntu2)
python-glanceclient (0.17.1)
python-heatclient (0.4.0)
python-keystoneclient (1.3.1)
python-mimeparse (0.1.4)
python-neutronclient (2.4.0)
python-novaclient (2.23.0)
python-openid (2.2.5)
python-openstackclient (1.2.1.dev20, /opt/stack/python-openstackclient)
python-saharaclient (0.8.0)
python-subunit (1.1.0)
python-swiftclient (2.3.1)
python-troveclient (1.0.8)
pytz (2015.2)
pyudev (0.16.1)
PyYAML (3.11)
qpid-python (0.26)
redis (2.10.3)
repoze.lru (0.6)
repoze.who (2.2)
requestbuilder (0.1.0b1)
requests (2.7.0)
retrying (1.3.3)
rfc3986 (0.2.0)
roman (2.0.0)
Routes (2.1)
rtslib-fb (2.1.51)
scgi (1.13)
semantic-version (2.4.1)
setuptools (16.0)
simplegeneric (0.8.1)
simplejson (3.6.5)
singledispatch (3.4.0.3)
six (1.9.0)
Sphinx (1.2.2)
SQLAlchemy (0.9.9)
sqlalchemy-migrate (0.9.6)
sqlparse (0.1.15)
ssh-import-id (3.21)
stevedore (1.3.0)
suds (0.4)
swift (2.3.0, /opt/stack/swift)
swift3 (1.7.0.dev371, /opt/stack/swift3)
tablib (0.10.0)
taskflow (0.7.1)
tempest (4.0.1.dev23, /opt/stack/tempest)
tempest-lib (0.4.0)
Tempita (0.5.2)
testrepository (0.0.20)
testresources (0.2.7)
testscenarios (0.5.0)
testtools (1.8.0)
thrift (0.9.2)
tooz (0.13.2)
tox (1.9.2)
traceback2 (1.4.0)
trollius (1.0.4)
Twisted-Core (13.2.0)
unittest2 (1.0.1)
urllib3 (1.10.4)
uTidylib (0.2)
virtualenv (12.1.1)
waitress (0.8.9)
warlock (1.1.0)
WebOb (1.3.1)
websockify (0.6.0)
WebTest (2.0.18)
Werkzeug (0.9.4)
wheel (0.24.0)
WSME (0.6.4)
xattr (0.6.4)
XStatic (1.0.1)
XStatic-Angular (1.3.7.0)
XStatic-Angular-Bootstrap (0.11.0.2)
XStatic-Angular-Cookies (1.2.1.1)
XStatic-Angular-lrdragndrop (1.0.2.2)
XStatic-Angular-Mock (1.2.1.1)
XStatic-Bootstrap-Datepicker (1.3.1.0)
XStatic-Bootstrap-SCSS (3.2.0.0)
XStatic-D3 (3.1.6.2)
XStatic-Font-Awesome (4.3.0.0)
XStatic-Hogan (2.0.0.2)
XStatic-Jasmine (2.1.2.0)
XStatic-jQuery (1.10.2.1)
XStatic-JQuery-Migrate (1.2.1.1)
XStatic-JQuery.quicksearch (2.0.3.1)
XStatic-JQuery.TableSorter (2.14.5.1)
XStatic-jquery-ui (1.11.0.1)
XStatic-JSEncrypt (2.0.0.2)
XStatic-Magic-Search (0.2.0.1)
XStatic-QUnit (1.14.0.2)
XStatic-Rickshaw (1.5.0.0)
XStatic-smart-table (1.4.5.3)
XStatic-Spin (1.2.5.2)
XStatic-term.js (0.0.4.2)
zake (0.2.1)
zope.interface (4.0.5)
```

Diff with my compute node 1 (10.12.181.121) pip packages

```
$ diff controller.pip.txt compute.pip.txt
2c2
< alembic (0.7.4)
---
> alembic (0.7.6)
6d5
< astroid (1.0.1)
8d6
< BeautifulSoup (3.2.1)
10,11c8
< blinker (1.3)
< boto (2.34.0)
---
> boto (2.38.0)
16,18c13
< Cheetah (2.4.4)
< CherryPy (3.2.2)
< cinder (2015.1.1.dev2, /opt/stack/cinder)
---
> cinder (2015.1.1.dev7, /opt/stack/cinder)
22d16
< colorama (0.2.5)
24d17
< coverage (3.7.1)
27,29c20,21
< decorator (3.4.0)
< discover (0.4.0)
< Django (1.6.11)
---
> decorator (3.4.2)
> Django (1.7.8)
31,32c23,24
< django-compressor (1.4)
< django-openstack-auth (1.1.9)
---
> django-compressor (1.5)
> django-openstack-auth (1.2.0)
35d26
< docutils (0.11)
41c32
< eventlet (0.17.3)
---
> eventlet (0.17.4)
43d33
< feedparser (5.1.3)
45,48c35
< flake8 (2.2.4)
< Flask (0.10.1)
< FormEncode (1.2.6)
< futures (2.2.0)
---
> futures (3.0.2)
51,54c38
< greenlet (0.4.2)
< hacking (0.10.1)
< happybase (0.9)
< heat (2015.1.1.dev1, /opt/stack/heat)
---
> greenlet (0.4.6)
56,57c40
< html5lib (0.999)
< httplib2 (0.9)
---
> httplib2 (0.9.1)
60,62c43,44
< itsdangerous (0.22)
< Jinja2 (2.7.2)
< jsonpatch (1.10)
---
> Jinja2 (2.7.3)
> jsonpatch (1.11)
68c50
< kazoo (2.0)
---
> kazoo (2.1)
71c53
< kombu (3.0.7)
---
> kombu (3.0.26)
73c55
< libvirt-python (1.2.2)
---
> libvirt-python (1.2.15)
75,76d56
< lockfile (0.8)
< logilab-common (0.61.0)
81,85c61
< MarkupSafe (0.18)
< mccabe (0.2.1)
< mock (1.0.1)
< mox (0.5.3)
< mox3 (0.7.0)
---
> MarkupSafe (0.23)
100c76
< os-client-config (0.8.1)
---
> os-client-config (0.8.2)
112,113d87
< oslosphinx (2.5.0)
< oslotest (1.5.1)
115d88
< oslo.versionedobjects (0.1.1)
121c94
< Paste (1.7.5.1)
---
> Paste (2.0.2)
123d95
< PasteScript (1.7.5)
126,127d97
< pep8 (1.5.7)
< Pillow (2.3.0)
129c99,100
< pip (7.0.0)
---
> pip (6.1.1)
> pluggy (0.3.0)
131c102
< posix-ipc (0.9.9)
---
> posix-ipc (1.0.0)
134c105
< py (1.4.26)
---
> py (1.4.27)
138c109
< pycparser (2.12)
---
> pycparser (2.13)
140d110
< pydns (2.3.6)
142,145d111
< pyflakes (0.8.1)
< Pygments (1.6)
< pyinotify (0.9.4)
< pylint (1.1.0)
148c114
< pyOpenSSL (0.15.1)
---
> pyOpenSSL (0.13)
154d119
< pysqlite (2.6.3)
156c121
< python-barbicanclient (3.0.1)
---
> python-barbicanclient (3.0.3)
159c124
< python-dateutil (1.5)
---
> python-dateutil (2.4.2)
167d131
< python-openid (2.2.5)
171,172c135,136
< python-swiftclient (2.3.1)
< python-troveclient (1.0.8)
---
> python-swiftclient (2.4.0)
> python-troveclient (1.0.9)
174d137
< pyudev (0.16.1)
176d138
< qpid-python (0.26)
181c143
< requests (2.7.0)
---
> requests (2.2.1)
183,184c145
< rfc3986 (0.2.0)
< roman (2.0.0)
---
> rfc3986 (0.2.1)
187d147
< scgi (1.13)
194d153
< Sphinx (1.2.2)
202d160
< swift3 (1.7.0.dev371, /opt/stack/swift3)
205c163
< tempest (4.0.1.dev23, /opt/stack/tempest)
---
> tempest (4.0.1.dev54, /opt/stack/tempest)
212d169
< thrift (0.9.2)
214c171
< tox (1.9.2)
---
> tox (2.0.1)
220d176
< uTidylib (0.2)
224,225c180,181
< WebOb (1.3.1)
< websockify (0.6.0)
---
> WebOb (1.4.1)
> websockify (0.6.1)
227c183
< Werkzeug (0.9.4)
---
> Werkzeug (0.10.4)
230c186
< xattr (0.6.4)
---
> xattr (0.7.5)
234d189
< XStatic-Angular-Cookies (1.2.1.1)
236d190
< XStatic-Angular-Mock (1.2.1.1)
```

