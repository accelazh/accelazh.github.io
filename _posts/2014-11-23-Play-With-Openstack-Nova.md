---
layout: post
title: "Play with Openstack Nova"
tagline : "Play with Openstack Nova"
description: "Play with Openstack Nova"
category: "openstack"
tags: [openstack, nova, compute]
---
{% include JB/setup %}


## Architecture

Nova services includes
  
  * Stateless, put on opensatck controller node
    * nova-api
    * nova-conductor: seperate nova-compute from accessing db directly. See [here](http://blog.csdn.net/lynn_kong/article/details/8606640).
    * nova-scheduler
    * nova-network: now there is neutron to replace it. But nova-network is much more robust and simpler, and neutron still not mature enough.
    * nova-novncproxy: change vnc access to browser web access to VM. Also, without a proxy user can not access compute node, which is in private network. See [here](http://docs.openstack.org/admin-guide-cloud/content/getting-started-with-vnc-proxy.html).
    * nova-consoleauth: for authentication of vnc access to VM.
  
  * Stateful, put on compute node
    * nova-compute

  * Others
    * nova-objectstore: only used by Nova for euca2ools, not a full-featured object store. See [here](https://answers.launchpad.net/nova/+question/156113) and [here](http://linux.die.net/man/1/nova-objectstore). Stateful. This service is rarely used.
    * nova-cert: used to generate certificates for euca-bundle-image. Only needed for EC2 API. See [here](http://docs.openstack.org/developer/nova/man/nova-cert.html). It is stateless.

Nova vnc workflow

![Nova vnc workflow](/images/nova-vnc-workflow.png "Nova vnc workflow")

Nova scheduler works by
  
  1. Use `filters` to filter out hosts that would attend selection,
  2. Get `weights` of each host, find the top one as the selected.

There is not much [code](https://github.com/openstack/nova/tree/stable/juno/nova/scheduler), easy to read. Both `filter` and `weight` are extendable, by adding more `filter`/`weigher` classes. You can use config file to specify custom classes (about [extending nova](http://lingxiankong.github.io/blog/2014/10/02/nova-extensions/)).

```
self.weight_classes = self.weight_handler.get_matching_classes(CONF.scheduler_weight_classes)

cfg.ListOpt('scheduler_weight_classes',
    default=['nova.scheduler.weights.all_weighers'],
    help='Which weight class names to use for weighing hosts')

cfg.MultiStrOpt('scheduler_available_filters',
    default=['nova.scheduler.filters.all_filters'],
    help='Filter classes available to the scheduler which may
```

"Avaibility zone", by which you specify VM boot on which compute node, is also implemented by nova-scheduler filters. For scheduler mechanism, see [here](http://lynnkong.iteye.com/blog/1776134). About which filter does what, see [here](http://blog.csdn.net/lynn_kong/article/details/9354455). 

Another thing is nova-cell, code in [nova/cell](https://github.com/openstack/nova/tree/master/nova/cells). The code looks extremely like nova-scheduler. For an introduction, see [here](http://blog.csdn.net/lynn_kong/article/details/8564558). For now nova-cell is rarely used and not being maintained well.

Many services are gradually moved out from Nova, even the nova-scheduler. Nova is becoming more of a connection point of all openstack services and a taskflow system. Openstack does have a python [`taskflow`](https://wiki.openstack.org/wiki/TaskFlow) library, which is being used in Cinder, going to be used in Neutron, not yet used in Nova (see [here](http://blog.csdn.net/epugv/article/details/17565759)). `Taskflow` targets on task flow chaining, transaction & rollback, sudden stop handling, metric & histroy and status tracking. This is for long time what I once want. 

Nova hard reboot (soft reboot is guest os level), or `nova reboot --hard`. What it does is

```
virsh destroy
Re-establish any and all volume connections
Regenerate the Libvirt XML
Regenerate establish network
```

Virsh correspondings is [here](http://virt-tools.org/learning/start-stop-vm-with-command-line/). Note that there is no `virsh stop`. "Pull the plug" maps to `virsh destroy`

In the end, an excellent [nova workflow](https://www.openstack.org/assets/presentation-media/OSSummitAtlanta2014-NovaLibvirtKVM2.pdf) explaination.

### Nova-network

Even though now there is neutron, nova-network is still a simple and stable solution for small openstack clusters (tenant count < 4094).

__Nova-network supports 3 modes__

  * Flat: use bridge to connect VMs out. It works like "the NAT mode" in my prior libvirt-kvm post.
  * FlatDHCP: add dhcp service (dnsmasq) to Flat mode. Launch a dnsmasq process for each tenant.
  * Vlan: add vlan to flatdhcp mode. Need switch support.

The `fixed ip` is what ip each VM got inside Openstack. It is a private ip address. The `floating ip` is a public ip address assigned to a VM (who also have a `fixed ip`). `Floating ip` is implemented by iptables NAT mapping.

Flat mode is useful if you want to handle dhcp by yourself. E.g offload to some central DHCP server.

Flatdhcp mode adds dhcp to Flat mode. FlatDHCPManager starts a dnsmasq on each compute host to DHCP fixed ip on VM. It creates a static lease file per compute node to guarantee the same IP address for VM. Only one network bridge is created on each compute node. All VMs in all tenants share the same network address pool, the same L2 broadcast domain. They can see each other regardless what tenant they belongs to. [Mirantis deep dive here](https://www.mirantis.com/blog/openstack-networking-flatmanager-and-flatdhcpmanager/).

![Flatdhcp networking diagram](/images/flat-dhcp-networking-diagram.png "Flatdhcp networking diagram")

Vlan mode brings VLAN to flatdhcp mode, so that we can have separation between tenants. Each tenant has its VLAN. On each compute node, one bridge will be created for each tenant. If VM in tenant 1 wants access to tenant 2, cross VLAN access needs L3 routing, which is done by the kernel of compute node. So no need for external router for this. On each compute node, for each tenant's VLAN id xx, eth0 will have a vlan interface eth0.xx (suppose eth0 carries VM traffic). So there will be many eth0.xxs. Vlan tagged packets are sent out compute nodes, so we need the switch to support vlan mode. The switch ports connecting to compute nodes must be configured as trunk port and allow tenant vlan ids. There will at most be 4094 vlan ids and tenants, as limitted by vlan tag length. 

[Mirantis deep dive here](https://www.mirantis.com/blog/vlanmanager-network-flow-analysis/). Note that in "Scenario 7", intertenant packets may be lost. Solution is

> The simplest way (and the best in my opinion) would be to place the intertenant communication on floating IPs rather than on fixed IPs.

![vlan mode networking diagram](/images/vlan-manager-networking-diagram.png "Vlan mode networking diagram")

Overall the issue is all about scalability and multitenancy. In neutron, we can use open-vswitch in place of the bridges in nova-network, and vxlan in place of the tenant seprartion brought by vlan.

References

  * [Nova-network architecture](http://blog.csdn.net/beginning1126/article/details/41172365)
  * [Openstack network modes and mechanism](http://blog.csdn.net/hilyoo/article/details/7721401)
  * [Nova-network introduction](http://www.cnblogs.com/yuxc/p/3426463.html)
  * [Nova-network in Openstack]s(http://blog.csdn.net/matt_mao/article/details/16918483)
  * [Linux bridge and VLAN](http://blog.csdn.net/dog250/article/details/7354590)
  * [VLAN in detail](http://blog.csdn.net/beginning1126/article/details/39371757)

__IP Alias__

Compute node usually requires at least 2 nics (1 given to bridge for vm traffic, another for management traffic). If you only have 1, [ip alias](http://en.wikipedia.org/wiki/IP_aliasing) can be used. It is capable to create numbers of ip addresses on only 1 eth0. Note that alias interfaces do not support DHCP.

CentOS guide refer to [here](http://geekpeek.net/ip-alias-centos-6/).

__What is TUN/TAP devices__

When kernel sends data to a tun or a tap device, instead of sending data "on the wire", a user space program can get the data (the user space program gets a special file descriptor from tun/tap device and read from it).

In a similar way, the program can write to the special file descriptor (with data properly formatted), and the data will appear as input to the tun ro the tap device. To the kernel, it would look like the tun/tap interface is receiving data "from the wire".

Vpn and tunneling can be implemented using tun/tap devices.

References: 

  * [A Q&A](http://askubuntu.com/questions/383082/whats-the-difference-between-tun-tap-vs-bridgevnet-vs-macvtap-for-virtualiza)
  * [Tun/Tap tutorial](http://backreference.org/2010/03/26/tuntap-interface-tutorial/)
  * [The wiki](http://en.wikipedia.org/wiki/TUN/TAP)

## Install and Config

Nova services on controller node are stateless, whose data in mysql. In production I can use haproxy and 2 copies of them for HA (see my prior haproxy post). But to play with, I'm gonna save the effort. I plann to 

  * node 1: 10.224.147.166, CentOS 7
    * nova-api
    * nova-scheduler
    * nova-novncproxy
    * nova-consoleauth
    * nova-conductor
    * glance (with filestore backend)
    * mysql
    * keystone
    * rabbitmq
  
  * node 2: 10.224.147.167, CentOS 7
    * nova-compute
    * nova-network
    * nova-api-metadata

  * node 3: 10.224.147.168, CentOS 7
    * nova-compute
    * nova-network
    * nova-api-metadata

  * node 4: 10.224.147.173, CentOS 7
    * nova-compute
    * nova-network
    * nova-api-metadata

For nova-network, I use the flatdhcp + multi-host deployment: on each compute host their is an nova-network. Here is the [example architecture](http://docs.openstack.org/openstack-ops/content/example_architecture.html).

### MySQL

I have installed MariaDB in prior post

```
service mariadb start
pip install mysql-python
```

### RabbitMQ

For rabbitmq installation and startup, check [tutorial](http://www.rabbitmq.com/install-rpm.html) and [cluster guide](https://www.rabbitmq.com/clustering.html). In prior post I have already installed a rabbitmq cluster.

On host 10.224.147.166, 

```
rabbitmq-server -detached
rabbitmqctl status

# break up my original rabbit cluster
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app
```

Add user for openstack to use.

```
rabbitmqctl add_user root 123work
rabbitmqctl set_user_tags root administrator
set_permissions -p / root ".*" ".*" ".*"
rabbitmqctl list_permissions
```

### Keystone

In my prior post already got keystone installed. To start it

```
service memcached start
su -s /bin/bash keystone -c '/bin/keystone-all >> /var/log/keystone/keystone.log 2>&1' &
keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ user-list
echo "stats items" | nc 127.0.0.1 11211
```

Now I need to create default users, tenants, and roles, following [openstack manual](http://docs.openstack.org/havana/install-guide/install/apt/content/keystone-users.html).

```
export OS_SERVICE_TOKEN=123abcdef
export OS_SERVICE_ENDPOINT=http://127.0.0.1:35357/v2.0

keystone tenant-create --name=admin --description="Admin Tenant"
keystone tenant-create --name=service --description="Service Tenant"
keystone user-create --name=admin --pass=123work --email=admin@example.com
keystone role-create --name=admin
keystone user-role-add --user=admin --tenant=admin --role=admin
```

Next define keystone service in keystone.

```
keystone service-create --name=keystone --type=identity --description="Keystone Identity Service"
keystone endpoint-create --service-id=<the_service_id_above> --publicurl=http://10.224.147.166:5000/v2.0 --internalurl=http://10.224.147.166:5000/v2.0 --adminurl=http://10.224.147.166:35357/v2.0
```

In above the `endpoint-create` may fail because unable to find service specified by the id. I have been encountering below, the service I created randomly appear or disapper.

```
# I cleared memcached before hand
$ echo "stats items" | nc 127.0.0.1 11211
END
$ keystone service-list
+----------------------------------+----------+----------+---------------------------+
|                id                |   name   |   type   |        description        |
+----------------------------------+----------+----------+---------------------------+
| 1dce5f94805241d388188ae29c678341 | keystone | identity | Keystone Identity Service |
+----------------------------------+----------+----------+---------------------------+
$ keystone service-list

$ keystone service-list

$ keystone service-list
+----------------------------------+----------+----------+---------------------------+
|                id                |   name   |   type   |        description        |
+----------------------------------+----------+----------+---------------------------+
| 1dce5f94805241d388188ae29c678341 | keystone | identity | Keystone Identity Service |
+----------------------------------+----------+----------+---------------------------+
$ echo "stats items" | nc 127.0.0.1 11211
END
```

In db table keystone.service, I found no record inserted. The newly created service is not entered into db. Troubleshooting with pdb ... I found I'm using template backended catalog

```
# this is wrong
[catalog]
driver = keystone.catalog.backends.templated.Catalog
template_file = /etc/keystone/default_catalog.templates
```

The default should be `keystone.catalog.backends.sql.Catalog`. Replace it with correct config file

```
echo '
[DEFAULT]
admin_token = 123abcdef
debug = true

[identity]
driver = keystone.identity.backends.sql.Identity

[database]
connection = mysql://root:123work@localhost/keystone
idle_timeout = 200

[token]
provider = keystone.token.providers.uuid.Provider
driver = keystone.token.persistence.backends.memcache_pool.Token

[cache]
enabled = true
backend = dogpile.cache.memcached
memcache_servers=localhost:11211

[auth]
methods = external,password,token
external = keystone.auth.plugins.external.DefaultDomain
password = keystone.auth.plugins.password.Password
token = keystone.auth.plugins.token.Token
' > /etc/keystone/keystone.conf
```

Now let's do things again and success

```
# db needs re-sync because template backend doesn't create correct service table
keystone-manager db_sync
su -s /bin/bash keystone -c '/bin/keystone-all >> /var/log/keystone/keystone.log 2>&1' &

keystone service-create --name=keystone --type=identity --description="Keystone Identity Service"
keystone endpoint-create --service-id=<the_service_id_above> --publicurl=http://10.224.147.166:5000/v2.0 --internalurl=http://10.224.147.166:5000/v2.0 --adminurl=http://10.224.147.166:35357/v2.0
```

Create openstack-admin.rc, by which to access keystone/openstack as admin

```
echo '
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=123work
export OS_AUTH_URL=http://10.224.147.166:35357/v2.0
' > ~/openstack-admin.rc
chmod a+x ~/openstack-admin.rc

# enable the rc file
unset OS_SERVICE_TOKEN
unset OS_SERVICE_ENDPOINT
source ~/openstack-admin.rc
```

### Glance

In my prior post I have already installed glance without keystone and file backend. Now I need to use glance + keystone.

Edit glance-api.conf to use keystone + cachemanagement. `cachemanagement` enables a series of REST API url path, where command `glance-cache-manage` can list cache/queue status or operate. See file /usr/lib/python2.7/site-packages/glance/api/middleware/cache_manage.py

```
echo '
[DEFAULT]
debug = True
verbose = True
log_file = /var/log/glance/api.log
image_cache_dir = /var/lib/glance/image-cache/

[database]
connection = mysql://root:123work@localhost/glance

[paste_deploy]
flavor = keystone+cachemanagement

[glance_store]
stores = glance.store.filesystem.Store
default_store = file
filesystem_store_datadir = /var/lib/glance/images/

[keystone_authtoken]
# once I forgot to write below, which cost me hours to troubleshoot
auth_uri = http://10.224.147.166:5000/v2.0
identity_uri = http://10.224.147.166:35357
admin_tenant_name = service
admin_user = glance
admin_password = 123work
' > /etc/glance/glance-api.conf
```

Edit glance-registry.conf to use keystone

```
echo '
[DEFAULT]
debug = True
verbose = True
log_file = /var/log/glance/registry.log

[database]
connection = mysql://root:123work@localhost/glance

[paste_deploy]
flavor = keystone

[keystone_authtoken]
auth_uri = http://10.224.147.166:5000/v2.0
identity_uri = http://10.224.147.166:35357
admin_tenant_name = service
admin_user = glance
admin_password = 123work
' > /etc/glance/glance-registry.conf
```

Start glance

```
su -s /bin/bash glance -c '/bin/glance-control glance-api start'
su -s /bin/bash glance -c '/bin/glance-control glance-registry start'

#su -s /bin/bash glance -c '/bin/glance-control glance-registry stop'
#su -s /bin/bash glance -c '/bin/glance-control glance-api stop'
```

Add glance to keystone, following [openstack manual](http://docs.openstack.org/juno/install-guide/install/apt/content/glance-install.html)

```
keystone user-create --name glance --pass 123work
keystone user-role-add --user glance --tenant service --role admin
keystone service-create --name glance --type image --description "OpenStack Image Service"
keystone endpoint-create --service-id $(keystone service-list | awk '/ image / {print $2}') --publicurl http://10.224.147.166:9292 --internalurl http://10.224.147.166:9292 --adminurl http://10.224.147.166:9292 --region regionOne
```

Verify glance working

```
mkdir /tmp/images
cd /tmp/images
wget http://cdn.download.cirros-cloud.net/0.3.3/cirros-0.3.3-x86_64-disk.img
glance image-create --name "cirros-0.3.3-x86_64" --file cirros-0.3.3-x86_64-disk.img --disk-format qcow2 --container-format bare --is-public True --progress
glance image-list
glance image-download cirros-0.3.3-x86_64 > cirros-0.3.3-x86_64.download
```

Compare the original image and downloaded image.

```
$ cat cirros-0.3.3-x86_64-disk.img | md5sum 
133eae9fb1c98f45894a4e60d8736619  -
$ cat cirros-0.3.3-x86_64.download | md5sum 
133eae9fb1c98f45894a4e60d8736619  -
```

### Libvirt

Compute nodes need to install libvirt first. See my prior post.

```
yum install -y kvm virt-manager libvirt libvirt-python python-virtinst virt-install
service libvirtd start
chkconfig libvirtd on
yum install -y seabios-bin
```

### Nova

You can use RDO repo to install RPMs for openstack components, as in [openstack manual](http://docs.openstack.org/juno/install-guide/install/apt/content/ch_basic_environment.html#basics-packages).

```
#yum install -y https://repos.fedorapeople.org/repos/openstack/openstack-juno/rdo-release-juno-1.noarch.rpm
```

But I will install from github source, following [developer guide](http://docs.openstack.org/developer/nova/devref/development.environment.html).

```
yum install -y python-devel openssl-devel python-pip git gcc mysql-devel postgresql-devel libffi-devel libvirt-devel graphviz sqlite-devel libxslt-devel libxslt libxml2 libxml2-devel
pip-python install tox
pip install mox
pip install fixtures
yum install -y novnc

mkdir ~/workspace
cd ~/workspace
git clone https://git.openstack.org/openstack/nova
cd nova
git checkout stable/juno
pip install -r requirements.txt
ldconfig
python setup.py install

cd ~/workspace
git clone https://github.com/openstack/python-novaclient.git
cd python-novaclient
python setup.py install
```

Create dependent directories and config files

```
# generate sample nova.conf. takes me hours, never works, commented out
cd ~/workspace/nova
./tools/config/generate_sample.sh -b ./ -p nova -o etc/nova

useradd -r -s /sbin/nologin nova
mkdir /var/lib/nova
mkdir /var/lib/nova/instances 
mkdir /var/lib/nova/buckets 
mkdir /var/lib/nova/CA 
mkdir /var/lib/nova/images 
mkdir /var/lib/nova/keys 
mkdir /var/lib/nova/networks 
mkdir /var/lib/nova/tmp
mkdir /var/log/nova
mkdir /etc/nova

cp -r ~/workspace/nova/etc/nova/* /etc/nova/
# better config /etc/nova/rootwrap* to be only visible to root
chown -R nova:nova /var/lib/nova /var/log/nova /etc/nova
```

Create database

```
mysql -uroot -p
CREATE DATABASE nova;
exit
```

Create the keystone user, service and endpoint

```
cd ~
source ~/openstack-admin.rc

keystone user-create --name nova --pass 123work
keystone user-role-add --user nova --tenant service --role admin
keystone service-create --name nova --type compute --description "OpenStack Compute"
keystone endpoint-create --service-id $(keystone service-list | awk '/ compute / {print $2}') --publicurl http://10.224.147.166:8774/v2/%\(tenant_id\)s --internalurl http://10.224.147.166:8774/v2/%\(tenant_id\)s --adminurl http://10.224.147.166:8774/v2/%\(tenant_id\)s --region regionOne
```

Config nova, following [openstack manual](http://docs.openstack.org/juno/install-guide/install/apt/content/ch_nova.html). The best reference should be [etc/nova.conf.sample](https://github.com/openstack/nova/tree/master/etc/nova) but it never generates successfully. Here for [example config files](http://docs.openstack.org/juno/config-reference/content/section_compute-config-samples.html).

Remember to modifiy ip according to host, and DON'T append '# xxx comment' after an option (nova parser will raise [error](https://lists.launchpad.net/openstack/msg04588.html)).

```
echo '
# DATABASE
[database]
connection = mysql://root:123work@10.224.147.166/nova

[DEFAULT]
# LOGS/STATE
verbose = True
debug = True
state_path=/var/lib/nova
logdir = /var/log/nova
lock_path=/var/lib/nova/tmp
rootwrap_config=/etc/nova/rootwrap.conf
bindir=/usr/bin

# SCHEDULER
compute_scheduler_driver=nova.scheduler.filter_scheduler.FilterScheduler
# avoid using most filters because my host has only one 1 core
scheduler_default_filters=RetryFilter

# COMPUTE
compute_driver=libvirt.LibvirtDriver
instance_name_template=instance-%08x
api_paste_config=/etc/nova/api-paste.ini

allow_resize_to_same_host=True

# RABBITMQ
rpc_backend = rabbit
rabbit_host = 10.224.147.166
rabbit_userid = root
rabbit_password = 123work

# GLANCE
image_service=nova.image.glance.GlanceImageService

# APIS
osapi_compute_extension=nova.api.openstack.compute.contrib.standard_extensions

# NETWORK
network_manager=nova.network.manager.FlatDHCPManager
dhcpbridge_flagfile=/etc/nova/nova.conf
firewall_driver=nova.virt.libvirt.firewall.IptablesFirewallDriver
network_size = 254
multi_host = True
send_arp_for_ha = True
share_dhcp_address = True
force_dhcp_release = True

# CHANGE according to host
my_ip = 10.224.147.166
public_interface=eth0
vlan_interface=eth0
flat_network_bridge=br100
flat_interface=eth0

network_api_class = nova.network.api.API
security_group_api = nova

# NOVNC CONSOLE
vnc_enabled = True
novncproxy_base_url=http://10.224.147.166:6080/vnc_auto.html
# CHANGE according to host
vncserver_listen = 10.224.147.166
# CHANGE according to host
vncserver_proxyclient_address = 10.224.147.166

# AUTHENTICATION
auth_strategy = keystone
[keystone_authtoken]
auth_uri = http://10.224.147.166:5000/v2.0
identity_uri = http://10.224.147.166:35357
admin_tenant_name = service
admin_user = glance
admin_password = 123work

[glance]
api_servers = 10.224.147.166:9292

# LIBVIRT
[libvirt]
# Im installing on VM, so use qemu instead of kvm
virt_type=qemu  
' > /etc/nova/nova.conf
```

Config sudoers for nova. Do it on both controller and compute nodes. Refer to [rootwrap](https://wiki.openstack.org/wiki/Rootwrap).

```
echo 'Defaults:nova !requiretty

nova ALL = (root) NOPASSWD: /usr/bin/nova-rootwrap /etc/nova/rootwrap.conf *
' > /etc/sudoers.d/nova
```

We need to config libvirt permissions so that nova-compute can access. On default libvirt uses `polkit` authentication. Do below on each controller and compute node.

```
echo '
[Allow nova libvirt management permissions]
Identity=unix-user:nova
Action=org.libvirt.unix.manage
ResultAny=yes
ResultInactive=yes
ResultActive=yes
' > /etc/polkit-1/localauthority/50-local.d/50-nova.pkla

# to test, first login as user 'nova' (need to temporarily change /etc/passwd)
sudo su nova
virsh --connect qemu:///system list
```

Synchronize nova database

```
nova-manage db sync
```

Next install nova on every host and copy the nova.conf accross. Remember to modify ip address on where I marked out.

Start nova services on controller and compute nodes.

```
# on controller node
su -s /bin/bash nova -c '/bin/nova-api >> /var/log/nova/nova-api.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-cert >> /var/log/nova/nova-cert.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-novncproxy >> /var/log/nova/nova-novncproxy.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-consoleauth >> /var/log/nova/nova-consoleauth.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-scheduler >> /var/log/nova/nova-scheduler.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-conductor >> /var/log/nova/nova-conductor.log 2>&1' &

# on each compute node
su -s /bin/bash nova -c '/bin/nova-compute >> /var/log/nova/nova-compute.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-network >> /var/log/nova/nova-network.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-api-metadata >> /var/log/nova/nova-api-metadata.log 2>&1' &

# to check error
grep -ir error /var/log/nova/*

# to stop
#pkill nova; ps -ef|grep nova
```

Create initial network (Don't use 192.168.22.x which is libvirt's default private net for VM).

```
nova --debug network-create demo-net --bridge br100 --multi-host T --fixed-range-v4 192.168.123.0/24
nova net-list
```

## Verify Operation

```
# on host 10.224.147.166
scp openstack-admin.rc root@10.224.147.167:~/

# on host 10.224.147.167
cd ~
nova service-list
nova list
```

The prior uploaded image (by glance) can be see now

```
$ nova image-list
+--------------------------------------+---------------------+--------+--------+
| ID                                   | Name                | Status | Server |
+--------------------------------------+---------------------+--------+--------+
| 0c953f24-e8f6-4d33-913c-1d06ee5dbf77 | cirros-0.3.3-x86_64 | ACTIVE |        |
+--------------------------------------+---------------------+--------+--------+
```

The prior created network below

```
nova net-list
+--------------------------------------+----------+------------------+
| ID                                   | Label    | CIDR             |
+--------------------------------------+----------+------------------+
| feb64647-f149-4322-bc58-c1d6c56e534a | demo-net | 192.168.123.0/24 |
+--------------------------------------+----------+------------------+
```

Now try to boot a VMs. For security group guide, refer to [here](http://docs.openstack.org/openstack-ops/content/security_groups.html)

```
# on host 10.224.147.167
nova keypair-add --pub-key ~/.ssh/id_rsa.pub demo-key
nova keypair-list
nova flavor-list
nova secgroup-list
nova secgroup-add-rule default icmp -1 255 0.0.0.0/0
nova secgroup-add-rule default tcp 1 65535 0.0.0.0/0
nova secgroup-add-rule default udp 1 65535 0.0.0.0/0
nova secgroup-list-rules default
```

Boot the VM

```
$ nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64 --nic net-id=feb64647-f149-4322-bc58-c1d6c56e534a --security-group default --key-name demo-key demo-instance1
+--------------------------------------+------------------------------------------------------------+
| Property                             | Value                                                      |
+--------------------------------------+------------------------------------------------------------+
| OS-DCF:diskConfig                    | MANUAL                                                     |
| OS-EXT-AZ:availability_zone          | nova                                                       |
| OS-EXT-SRV-ATTR:host                 | -                                                          |
| OS-EXT-SRV-ATTR:hypervisor_hostname  | -                                                          |
| OS-EXT-SRV-ATTR:instance_name        | instance-00000003                                          |
| OS-EXT-STS:power_state               | 0                                                          |
| OS-EXT-STS:task_state                | scheduling                                                 |
| OS-EXT-STS:vm_state                  | building                                                   |
| OS-SRV-USG:launched_at               | -                                                          |
| OS-SRV-USG:terminated_at             | -                                                          |
| accessIPv4                           |                                                            |
| accessIPv6                           |                                                            |
| adminPass                            | 5kWyxFNk7mn3                                               |
| config_drive                         |                                                            |
| created                              | 2014-11-21T11:27:06Z                                       |
| flavor                               | m1.tiny (1)                                                |
| hostId                               |                                                            |
| id                                   | d8aadfe5-b695-4b26-bc37-f4c4593b4c7a                       |
| image                                | cirros-0.3.3-x86_64 (0c953f24-e8f6-4d33-913c-1d06ee5dbf77) |
| key_name                             | demo-key                                                   |
| metadata                             | {}                                                         |
| name                                 | demo-instance1                                             |
| os-extended-volumes:volumes_attached | []                                                         |
| progress                             | 0                                                          |
| security_groups                      | default                                                    |
| status                               | BUILD                                                      |
| tenant_id                            | c48611d23b754e909753d7ec2428819a                           |
| updated                              | 2014-11-21T11:27:06Z                                       |
| user_id                              | 6094daee26d9463e8b37e87dc8d8b33d                           |
+--------------------------------------+------------------------------------------------------------+
```

Show vm state. For [VM state and transitions](http://docs.openstack.org/developer/nova/devref/vmstates.html), see link.

```
nova show d8aadfe5-b695-4b26-bc37-f4c4593b4c7a
```

If you see below error in nova-compute.log

> 2014-11-21 11:27:09.121 10279 ERROR nova.virt.disk.mount.nbd [-] nbd module not loaded

It means kernel module nbd is needed. Nbd is used by libvirt to inject file. See [here](https://bugs.launchpad.net/nova/+bug/755854) and [here](https://lists.launchpad.net/openstack/msg23244.html)

```
modprobe nbd
```

Check out VMs in libvirt

```
# on the host where VM boots
$ virsh list --all
 Id    Name                           State
----------------------------------------------------
 8     instance-00000003              running

$ ls /var/lib/nova/instances/_base/
58c4ff690623a24f84643a0d7f87649a0233a2d8
$ ls /var/lib/nova/instances/
_base  compute_nodes  d8aadfe5-b695-4b26-bc37-f4c4593b4c7a  locks
$ ll -h /var/lib/nova/instances/d8aadfe5-b695-4b26-bc37-f4c4593b4c7a/disk
-rw-r--r-- 1 qemu qemu 1.9M Nov 21 11:28 /var/lib/nova/instances/d8aadfe5-b695-4b26-bc37-f4c4593b4c7a/disk
$ ps -ef|grep instance-00000003
qemu     10659     1  6 11:27 ?        00:01:23 /usr/libexec/qemu-kvm -name instance-00000003 -S -machine pc-i440fx-rhel7.0.0,accel=tcg,usb=off -cpu Westmere,+hypervisor,+avx,+osxsave,+xsave,+tsc-deadline,+x2apic,+pcid,+pclmuldq,+ss,+vme -m 512 -realtime mlock=off -smp 1,sockets=1,cores=1,threads=1 -uuid d8aadfe5-b695-4b26-bc37-f4c4593b4c7a -smbios type=1,manufacturer=OpenStack Foundation,product=OpenStack Nova,version=2014.2.1,serial=464814b6-1cfc-f330-e1cd-d3ed2d316b8b,uuid=d8aadfe5-b695-4b26-bc37-f4c4593b4c7a -no-user-config -nodefaults -chardev socket,id=charmonitor,path=/var/lib/libvirt/qemu/instance-00000003.monitor,server,nowait -mon chardev=charmonitor,id=monitor,mode=control -rtc base=utc -no-shutdown -boot strict=on -device piix3-usb-uhci,id=usb,bus=pci.0,addr=0x1.0x2 -drive file=/var/lib/nova/instances/d8aadfe5-b695-4b26-bc37-f4c4593b4c7a/disk,if=none,id=drive-virtio-disk0,format=qcow2,cache=none -device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x4,drive=drive-virtio-disk0,id=virtio-disk0,bootindex=1 -netdev tap,fd=23,id=hostnet0 -device virtio-net-pci,netdev=hostnet0,id=net0,mac=fa:16:3e:5e:92:31,bus=pci.0,addr=0x3 -chardev file,id=charserial0,path=/var/lib/nova/instances/d8aadfe5-b695-4b26-bc37-f4c4593b4c7a/console.log -device isa-serial,chardev=charserial0,id=serial0 -chardev pty,id=charserial1 -device isa-serial,chardev=charserial1,id=serial1 -device usb-tablet,id=input0 -vnc 10.224.147.173:0 -k en-us -vga cirrus -device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x5
root     10827  3110  0 11:47 pts/0    00:00:00 grep --color=auto instance-00000003
$ virsh vncdisplay instance-00000003
10.224.147.173:0
```

Now I can use VNC client to access the VM on

```
... # vnc to 10.224.147.173:0

# on the host where VM lives
$ ssh cirros@192.168.123.2
$ ifconfig
eth0      Link encap:Ethernet  HWaddr FA:16:3E:5E:92:31  
          inet addr:192.168.123.2  Bcast:192.168.123.255  Mask:255.255.255.0
          inet6 addr: fe80::f816:3eff:fe5e:9231/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1025 errors:0 dropped:0 overruns:0 frame:0
          TX packets:141 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:69856 (68.2 KiB)  TX bytes:14658 (14.3 KiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
$ ls /dev/vd*
/dev/vda   /dev/vda1
# nova auto inject hostname
$ hostname
demo-instance1

# ping gateway br100
$ ping 192.168.123.1
PING 192.168.123.1 (192.168.123.1): 56 data bytes
64 bytes from 192.168.123.1: seq=0 ttl=64 time=2.301 ms
64 bytes from 192.168.123.1: seq=1 ttl=64 time=0.781 ms
64 bytes from 192.168.123.1: seq=2 ttl=64 time=0.753 ms
round-trip min/avg/max = 0.753/1.278/2.301 ms

# ping local compute host
$ ping 10.224.147.173
PING 10.224.147.173 (10.224.147.173): 56 data bytes
64 bytes from 10.224.147.173: seq=0 ttl=64 time=2.058 ms
64 bytes from 10.224.147.173: seq=1 ttl=64 time=0.970 ms
64 bytes from 10.224.147.173: seq=2 ttl=64 time=0.728 ms
```

To verify the vnc console from browser. Note that in the browser it shows "unencrypted".

```
$ nova get-vnc-console demo-instance1 novnc
+-------+-------------------------------------------------------------------------------------+
| Type  | Url                                                                                 |
+-------+-------------------------------------------------------------------------------------+
| novnc | http://10.224.147.166:6080/vnc_auto.html?token=645e0bc5-f90b-4d89-8ecd-2f739f49ec8e |
+-------+-------------------------------------------------------------------------------------+
... # open it from browser
```

Let's try metadata services on VM. It can be used to attach custom user data to VM, visible from inside. Nova-api-metadata is required for metadata services. [Manual](http://docs.openstack.org/admin-guide-cloud/content/section_metadata-service.html) here and see [materials](http://blog.csdn.net/matt_mao/article/details/11600115).

```
$ ssh cirros@192.168.123.2
$ curl http://169.254.169.254/openstack
2012-08-10
2013-04-04
2013-10-17
latest
$ curl http://169.254.169.254/openstack/2012-08-10/meta_data.json
{"uuid": "d8aadfe5-b695-4b26-bc37-f4c4593b4c7a", "availability_zone": "nova", "hostname": "demo-instance1.novalocal", "launch_index": 0, "public_keys": {"demo-key": "ssh-rsa xxx"}, "name": "demo-instance1"} 
```

Check out the host node who carries the new VM

```
$ ip route
default via 10.224.147.1 dev br100 
10.224.147.0/24 dev br100  proto kernel  scope link  src 10.224.147.173 
169.254.169.254 via 10.224.147.152 dev br100  proto static 
192.168.122.0/24 dev virbr0  proto kernel  scope link  src 192.168.122.1 
192.168.123.0/24 dev br100  proto kernel  scope link  src 192.168.123.1 
$ ifconfig
br100: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.123.1  netmask 255.255.255.0  broadcast 192.168.123.255
        inet6 fe80::b08b:eaff:feae:6941  prefixlen 64  scopeid 0x20<link>
        ether fa:16:3e:f4:45:a2  txqueuelen 0  (Ethernet)
        RX packets 34952  bytes 17998089 (17.1 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 26756  bytes 5392590 (5.1 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::f816:3eff:fef4:45a2  prefixlen 64  scopeid 0x20<link>
        ether fa:16:3e:f4:45:a2  txqueuelen 1000  (Ethernet)
        RX packets 1120119  bytes 336575244 (320.9 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 231734  bytes 24710843 (23.5 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 0  (Local Loopback)
        RX packets 10557  bytes 554458 (541.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10557  bytes 554458 (541.4 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

virbr0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
        ether 00:00:00:00:00:00  txqueuelen 0  (Ethernet)
        RX packets 344  bytes 30418 (29.7 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 231  bytes 31501 (30.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vnet0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc16:3eff:fe5e:9231  prefixlen 64  scopeid 0x20<link>
        ether fe:16:3e:5e:92:31  txqueuelen 500  (Ethernet)
        RX packets 135  bytes 14304 (13.9 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 648  bytes 45967 (44.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
$ iptables --list -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         
nova-compute-PREROUTING  all  --  anywhere             anywhere            
nova-network-PREROUTING  all  --  anywhere             anywhere            
nova-api-metadat-PREROUTING  all  --  anywhere             anywhere            

Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
nova-compute-OUTPUT  all  --  anywhere             anywhere            
nova-network-OUTPUT  all  --  anywhere             anywhere            
nova-api-metadat-OUTPUT  all  --  anywhere             anywhere            

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
nova-compute-POSTROUTING  all  --  anywhere             anywhere            
nova-network-POSTROUTING  all  --  anywhere             anywhere            
nova-api-metadat-POSTROUTING  all  --  anywhere             anywhere            
MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24    
nova-postrouting-bottom  all  --  anywhere             anywhere            

Chain nova-api-metadat-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-POSTROUTING (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-PREROUTING (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-float-snat (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-snat (1 references)
target     prot opt source               destination         
nova-api-metadat-float-snat  all  --  anywhere             anywhere            

Chain nova-compute-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-compute-POSTROUTING (1 references)
target     prot opt source               destination         

Chain nova-compute-PREROUTING (1 references)
target     prot opt source               destination         

Chain nova-compute-float-snat (1 references)
target     prot opt source               destination         

Chain nova-compute-snat (1 references)
target     prot opt source               destination         
nova-compute-float-snat  all  --  anywhere             anywhere            

Chain nova-network-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-network-POSTROUTING (1 references)
target     prot opt source               destination         
ACCEPT     all  --  192.168.123.0/24     10.224.147.173      
ACCEPT     all  --  192.168.123.0/24     192.168.123.0/24     ! ctstate DNAT

Chain nova-network-PREROUTING (1 references)
target     prot opt source               destination         
DNAT       tcp  --  anywhere             169.254.169.254      tcp dpt:http to:10.224.147.173:8775

Chain nova-network-float-snat (1 references)
target     prot opt source               destination         

Chain nova-network-snat (1 references)
target     prot opt source               destination         
nova-network-float-snat  all  --  anywhere             anywhere            
SNAT       all  --  192.168.123.0/24     anywhere             to:10.224.147.173

Chain nova-postrouting-bottom (1 references)
target     prot opt source               destination         
nova-compute-snat  all  --  anywhere             anywhere            
nova-network-snat  all  --  anywhere             anywhere            
nova-api-metadat-snat  all  --  anywhere             anywhere 
```

Try the most powerful trouble-fix combo for VM

```
nova reset-state –-active d8aadfe5-b695-4b26-bc37-f4c4593b4c7a
nova reboot --hard d8aadfe5-b695-4b26-bc37-f4c4593b4c7a
```

Launch another 2 VMs. Sometime the new VM doesn't get ip, `nova reboot --hard` fixes it.

```
$ nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64 --nic net-id=feb64647-f149-4322-bc58-c1d6c56e534a --security-group default --key-name demo-key demo-instance2
...
3297e53b-1e04-490f-9049-060728c1ac65    # on host 10.224.147.168
...
$ nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64 --nic net-id=feb64647-f149-4322-bc58-c1d6c56e534a --security-group default --key-name demo-key demo-instance3
...
0f519353-9394-4cc7-969f-dc8f89311045    # on host 10.224.147.173
...
```

Let's ping from demo-instance2 (192.168.123.3) on host 10.224.147.168, to demo-instance3 (192.168.123.4) on host 10.224.147.173

```
# on host 10.224.147.168
$ ssh cirros@192.168.123.3
$ hostname
demo-instance2
$ ping 192.168.123.4
PING 192.168.123.4 (192.168.123.4): 56 data bytes
... # get no response
```

Why I get no response when ping another VM? The ARP reply never comes into vnet0.

```
# on host 10.224.147.168
$ tcpdump -i vnet0 -vvv -nnn
tcpdump: WARNING: vnet0: no IPv4 address assigned
tcpdump: listening on vnet0, link-type EN10MB (Ethernet), capture size 65535 bytes
13:16:48.572175 IP (tos 0xc0, ttl 255, id 35914, offset 0, flags [none], proto VRRP (112), length 40)
    10.224.147.166 > 224.0.0.18: vrrp 10.224.147.166 > 224.0.0.18: VRRPv2, Advertisement, vrid 51, prio 101, authtype none, intvl 1s, length 20, addrs: 10.224.147.208
13:16:48.591710 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
13:16:48.591721 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
13:16:48.591857 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
... # the ARP packets never get its reply

$ tcpdump -i br100 arp
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on br100, link-type EN10MB (Ethernet), capture size 65535 bytes
13:49:46.176324 ARP, Request who-has 192.168.123.4 tell 192.168.123.3, length 28
13:49:46.176564 ARP, Request who-has 192.168.123.4 tell 192.168.123.3, length 28
13:49:46.177406 ARP, Reply 192.168.123.4 is-at fa:16:3e:6e:d8:92 (oui Unknown), length 42     # the arp reply
```

Check the `iptables --list -t filter` result. All bridge to interface traffic is supposed to pass iptables filter table, according to [here](http://serverfault.com/questions/162366/iptables-bridge-and-forward-chain). I found that filter table FORWARD chain `nova-filter-top`, this rule targets to `nova-compute-inst-6` and drops all packet.

```
$ iptables --list -t filter
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
nova-compute-INPUT  all  --  anywhere             anywhere            
nova-network-INPUT  all  --  anywhere             anywhere            
nova-api-metadat-INPUT  all  --  anywhere             anywhere            
ACCEPT     udp  --  anywhere             anywhere             udp dpt:domain
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:domain
ACCEPT     udp  --  anywhere             anywhere             udp dpt:bootps
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:bootps

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
nova-filter-top  all  --  anywhere             anywhere            
nova-compute-FORWARD  all  --  anywhere             anywhere            
nova-network-FORWARD  all  --  anywhere             anywhere            
nova-api-metadat-FORWARD  all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             192.168.122.0/24     ctstate RELATED,ESTABLISHED
ACCEPT     all  --  192.168.122.0/24     anywhere            
ACCEPT     all  --  anywhere             anywhere            
REJECT     all  --  anywhere             anywhere             reject-with icmp-port-unreachable
REJECT     all  --  anywhere             anywhere             reject-with icmp-port-unreachable

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
nova-filter-top  all  --  anywhere             anywhere            
nova-compute-OUTPUT  all  --  anywhere             anywhere            
nova-network-OUTPUT  all  --  anywhere             anywhere            
nova-api-metadat-OUTPUT  all  --  anywhere             anywhere            

Chain nova-api-metadat-FORWARD (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-INPUT (1 references)
target     prot opt source               destination         
ACCEPT     tcp  --  anywhere             openstack-03  tcp dpt:8775

Chain nova-api-metadat-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-local (1 references)
target     prot opt source               destination         

Chain nova-compute-FORWARD (1 references)
target     prot opt source               destination         
ACCEPT     udp  --  default              255.255.255.255      udp spt:bootpc dpt:bootps

Chain nova-compute-INPUT (1 references)
target     prot opt source               destination         
ACCEPT     udp  --  default              255.255.255.255      udp spt:bootpc dpt:bootps

Chain nova-compute-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-compute-inst-6 (1 references)
target     prot opt source               destination         
DROP       all  --  anywhere             anywhere             state INVALID
ACCEPT     all  --  anywhere             anywhere             state RELATED,ESTABLISHED
nova-compute-provider  all  --  anywhere             anywhere            
ACCEPT     udp  --  192.168.123.1        anywhere             udp spt:bootps dpt:bootpc
ACCEPT     all  --  192.168.123.0/24     anywhere            
ACCEPT     icmp --  anywhere             anywhere            
ACCEPT     tcp  --  anywhere             anywhere             multiport dports tcpmux:65535
ACCEPT     udp  --  anywhere             anywhere             multiport dports tcpmux:65535
nova-compute-sg-fallback  all  --  anywhere             anywhere            

Chain nova-compute-local (1 references)
target     prot opt source               destination         
nova-compute-inst-6  all  --  anywhere             192.168.123.3       

Chain nova-compute-provider (1 references)
target     prot opt source               destination         

Chain nova-compute-sg-fallback (1 references)
target     prot opt source               destination         
DROP       all  --  anywhere             anywhere            

Chain nova-filter-top (2 references)
target     prot opt source               destination         
nova-compute-local  all  --  anywhere             anywhere            
nova-network-local  all  --  anywhere             anywhere            
nova-api-metadat-local  all  --  anywhere             anywhere            

Chain nova-network-FORWARD (1 references)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            

Chain nova-network-INPUT (1 references)
target     prot opt source               destination         
ACCEPT     udp  --  anywhere             anywhere             udp dpt:bootps
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:bootps
ACCEPT     udp  --  anywhere             anywhere             udp dpt:domain
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:domain

Chain nova-network-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-network-local (1 references)
target     prot opt source               destination    
```

Useful commands in troubleshooting: `ip a`, `route -n`, `iptables --list`.

Found similar issue in [maillist](http://lists.openstack.org/pipermail/openstack/2014-July/008558.html) but no solution followed up. Some troubleshooting material: [\[1\]](http://docs.openstack.org/openstack-ops/content/network_troubleshooting.html)[\[2\]](https://www.mirantis.com/blog/openstack-networking-single-host-flatdhcpmanager/).

I have been using `tcpdump` to trace arp reply. On 10.224.147.168, the arp reply reaches br100, with destination mac address pointing vnet0. But vnet0 never receives it

```
$ tcpdump -i br100 -vvv -nnn -XX arp
tcpdump: listening on br100, link-type EN10MB (Ethernet), capture size 65535 bytes
05:00:28.384074 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
    0x0000:  ffff ffff ffff fa16 3eb5 e478 0806 0001  ........>..x....
    0x0010:  0800 0604 0001 fa16 3eb5 e478 c0a8 7b03  ........>..x..{.
    0x0020:  0000 0000 0000 c0a8 7b04                 ........{.
05:00:28.384194 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
    0x0000:  ffff ffff ffff fa16 3eb5 e478 0806 0001  ........>..x....
    0x0010:  0800 0604 0001 fa16 3eb5 e478 c0a8 7b03  ........>..x..{.
    0x0020:  0000 0000 0000 c0a8 7b04                 ........{.
05:00:28.384797 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.4 is-at fa:16:3e:6e:d8:92, length 42
    0x0000:  fa16 3eb5 e478 fa16 3e6e d892 0806 0001  ..>..x..>n......
    0x0010:  0800 0604 0002 fa16 3e6e d892 c0a8 7b04  ........>n....{.
    0x0020:  fa16 3eb5 e478 c0a8 7b03 0000 0000 0000  ..>..x..{.......
    0x0030:  0000 0000 0000 0000                      ........
...

6 packets captured
6 packets received by filter
0 packets dropped by kernel

$ ifconfig vnet0
vnet0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc16:3eff:feb5:e478  prefixlen 64  scopeid 0x20<link>
        ether fe:16:3e:b5:e4:78  txqueuelen 500  (Ethernet)
        RX packets 75807  bytes 5194181 (4.9 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 579235  bytes 32177463 (30.6 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ ifconfig br100
br100: flags=4419<UP,BROADCAST,RUNNING,PROMISC,MULTICAST>  mtu 1500
        inet 192.168.123.1  netmask 255.255.255.0  broadcast 192.168.123.255
        inet6 fe80::9c96:1ff:fe46:df67  prefixlen 64  scopeid 0x20<link>
        ether fa:16:3e:a8:4f:41  txqueuelen 0  (Ethernet)
        RX packets 3649642  bytes 582346877 (555.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3194510  bytes 484417499 (461.9 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ tcpdump -i vnet0 -vvv -nnn -XX arp
tcpdump: WARNING: vnet0: no IPv4 address assigned
tcpdump: listening on vnet0, link-type EN10MB (Ethernet), capture size 65535 bytes
05:03:33.479611 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
    0x0000:  ffff ffff ffff fa16 3eb5 e478 0806 0001  ........>..x....
    0x0010:  0800 0604 0001 fa16 3eb5 e478 c0a8 7b03  ........>..x..{.
    0x0020:  0000 0000 0000 c0a8 7b04                 ........{.
05:03:33.479634 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
    0x0000:  ffff ffff ffff fa16 3eb5 e478 0806 0001  ........>..x....
    0x0010:  0800 0604 0001 fa16 3eb5 e478 c0a8 7b03  ........>..x..{.
    0x0020:  0000 0000 0000 c0a8 7b04                 ........{.
...

6 packets captured
9 packets received by filter
0 packets dropped by kernel
```

__Found possible problem cause__

I have only 1 NIC eth0, and both eth0 and br100 have addresses

```
# on host 10.224.147.168
$ ip a
...
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast master br100 state UP qlen 1000
    link/ether fa:16:3e:a8:4f:41 brd ff:ff:ff:ff:ff:ff
    inet 10.224.147.168/24 brd 10.224.147.255 scope global dynamic eth0
       valid_lft 86176sec preferred_lft 86176sec
    inet6 fe80::f816:3eff:fea8:4f41/64 scope link 
       valid_lft forever preferred_lft forever
...
4: br100: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
    link/ether fa:16:3e:a8:4f:41 brd ff:ff:ff:ff:ff:ff
    inet 192.168.123.1/24 brd 192.168.123.255 scope global br100
       valid_lft forever preferred_lft forever
    inet 10.224.147.168/24 brd 10.224.147.255 scope global br100
       valid_lft forever preferred_lft forever
    inet6 fe80::9c96:1ff:fe46:df67/64 scope link 
       valid_lft forever preferred_lft forever
...
```

And nova-network has added eth0 to br100

```
# on host 10.224.147.168
$ brctl show br100
bridge name bridge id   STP enabled interfaces
br100   8000.fa163ea84f41 no    eth0
                                vnet0
```

The problem here is, I should NEVER add an interface to bridge and also give it an IP address, which will mess network up. Nova-network assumes I'm using 2 NICs eth0 and eth1, and it puts 1 of it into br100. But I fill nova.conf both with eth0.

Next I will leave the problem for some time and take care of swift and horizon first. After that I will jump back and get 2 NIC deploy on board.

## Enable Swift

To use swift in nova, first I need to change my prior deployed swift to use keystone, than I need to enable glance to use swift backend.

### Enable Swift to Use Keystone

In prior post I deployed swift on 10.224.147.166, 10.224.147.167, 10.224.147.168. I want to use swift as image backend, replacing glance file store.

Config swift to use keystone. Refering to openstack [installation guide](http://docs.openstack.org/juno/install-guide/install/yum/content/installing-openstack-object-storage.html).

First add swift user and service to keystone. The endpoint url is supposed to be a load balancer, which shields all swift proxy nodes. But for now I will just be simple, use one proxy node instead.

```
source openstack-admin.rc 
keystone user-create --name swift --pass 123work
keystone user-role-add --user swift --tenant service --role admin
keystone service-create --name swift --type object-store --description "OpenStack Object Storage"
keystone endpoint-create --service-id $(keystone service-list | awk '/ object-store / {print $2}') --publicurl 'http://10.224.147.166:8080/v1/AUTH_%(tenant_id)s' --internalurl 'http://10.224.147.166:8080/v1/AUTH_%(tenant_id)s' --adminurl http://10.224.147.166:8080 --region regionOne
```

Config swift proxy node, the config file needs to be modified on all nodes.

```
# replace below section proxy-server.conf
[pipeline:main]
pipeline = catch_errors gatekeeper healthcheck proxy-logging cache bulk tempurl slo dlo ratelimit crossdomain authtoken keystoneauth staticweb container-quotas account-quotas proxy-logging proxy-server

------------------------

# add these filters in proxy-server.conf
[filter:keystoneauth]
use = egg:swift#keystoneauth
operator_roles = _member_,admin,swiftoperator
 
[filter:authtoken]
paste.filter_factory = keystoneclient.middleware.auth_token:filter_factory
 
delay_auth_decision = true
 
auth_protocol = http
auth_host = 10.224.147.166
auth_uri = http://10.224.147.166:5000
 
admin_tenant_name = service
admin_user = swift
admin_password = 123work
```

Restart swift on each host.

```
# to stop
swift-init stop all

# start services, log in /var/log/message
service memcached start
service xinetd restart
swift-init main start
swift-init rest start
```

To verify swift

```
source openstack-admin.rc
swift stat
dd if=/dev/urandom of=./obj1.dat bs=512 count=2048
dd if=/dev/urandom of=./obj2.dat bs=512 count=2048
swift upload container1 obj1.dat obj2.dat
swift upload container2 obj2.dat
swift list
swift list container1
swift list container2
swift download container1 obj2.dat
mkdir test
cd test
swift download container1 obj2.dat
cd ..
cat obj2.dat | md5sum
cat test/obj2.dat | md5sum
```

### Enable Glance to Use Swift

First edit glance config to enable swift backend

```
# replace below section in glance-api.conf
[glance_store]
stores = glance.store.swift.Store
default_store = swift
swift_store_auth_address = http://10.224.147.166:5000/v2.0/
swift_store_user = service:glance
swift_store_key = 123work
swift_store_create_container_on_put = True
```

Restart glance

```
# to stop
killall glance-api
killall glance-registry
sleep 2
ps -ef|grep glance

# to start
su -s /bin/bash glance -c '/bin/glance-control glance-api start'
su -s /bin/bash glance -c '/bin/glance-control glance-registry start'
```

Verify glance

```
# download disk image
source openstack-admin.rc
mkdir /tmp/images
cd /tmp/images
wget http://cdn.download.cirros-cloud.net/0.3.3/cirros-0.3.3-x86_64-disk.img

# upload and download from glance
glance --debug image-create --name "cirros-0.3.3-x86_64_swift" --file cirros-0.3.3-x86_64-disk.img --disk-format qcow2 --container-format bare --is-public True --progress
glance image-list
rm -rf /var/lib/glance/images/*
glance image-download  cirros-0.3.3-x86_64_swift > ./verify_glance_swift
cat verify_glance_swift | md5sum
cat cirros-0.3.3-x86_64-disk.img | md5sum

# boot new vm in nova
nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64_swift --nic net-id=feb64647-f149-4322-bc58-c1d6c56e534a --security-group default --key-name demo-key demo-instance4
nova show demo-instance4
nova get-vnc-console demo-instance4 novnc
... # verify instance status on browser
```

Check the image files in swift

```
source openstack-admin.rc
export OS_TENANT_NAME=service
export OS_USERNAME=glance
swift list
swift list glance
```

## Enable Horizon Dashboard

I'm gonna add a horizon dashboard to my nova cluster. Horizon is a pure frontend web portal for openstack. Install horizon on 10.224.147.174. Following [openstack manual](http://docs.openstack.org/juno/install-guide/install/apt/content/install_dashboard.html) and [developer doc](http://docs.openstack.org/developer/horizon/quickstart.html).

First, install horizon.

```
yum install -y gcc git-core python-devel python-virtualenv openssl-devel libffi-devel memcached libxslt-devel libxslt libxml2 libxml2-devel httpd mod_wsgi
pip install python-memcached

mkdir ~/workspace
cd ~/workspace
git clone https://github.com/openstack/horizon.git
cd horizon
git checkout stable/juno
pip install -r requirements.txt
python setup.py install

mkdir /var/lib/openstack-dashboard/
mkdir /var/log/horizon/
mkdir /etc/openstack-dashboard/
cp ~/workspace/horizon/openstack_dashboard/local/local_settings.py.example /etc/openstack-dashboard/
cp /etc/openstack-dashboard/local_settings.py.example /etc/openstack-dashboard/local_settings.py
chown -R apache:apache /var/lib/openstack-dashboard /var/log/horizon /etc/openstack-dashboard
```

Config horizon. A good tutorial at [here](http://dev.cloudwatt.com/en/blog/deploy-horizon-from-source-with-apache-and-ssl.html).

```
# open /etc/openstack-dashboard/local_settings.py and replace these lines
CACHES = { 
  'default': {
    'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION' : '127.0.0.1:11211'
  }
}

# and replace this line
ALLOWED_HOSTS = ['*']

# and replace this line
OPENSTACK_HOST = "10.224.147.166"

# replace this line to avoid https://bugs.launchpad.net/ubuntu/+source/horizon/+bug/1216019
#SECRET_KEY = secret_key.generate_or_read_from_file(
#    os.path.join(LOCAL_PATH, '.secret_key_store'))
SECRET_KEY = 'horizonkey_123work'

# add below to LOGGING.handlers
'file': {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': '/var/log/horizon/horizon.log',
    'formatter': 'verbose',
},
# add blow to LOGGING
'formatters': {
    'verbose': {
        'format': '%(asctime)s %(process)d %(levelname)s %(name)s '
                  '%(message)s'
    },
},
# change LOGGING.loggers.*.handlers to file & console
'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'horizon': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_dashboard': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'novaclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'cinderclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'keystoneclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'glanceclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'neutronclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'heatclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ceilometerclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'troveclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'swiftclient': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack_auth': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'nose.plugins.manager': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'iso8601': {
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'scss': {
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    }
```

Next, move openstack dashboard to the right place. We also need the static file collected

```
mkdir /usr/share/opentack-dashboard
mv -v /usr/lib/python2.7/site-packages/openstack_dashboard /usr/share/openstack-dashboard/
ln -s /etc/openstack-dashboard/local_settings.py /usr/share/openstack-dashboard/openstack_dashboard/local/local_settings.py
cp ~/workspace/horizon/manage.py /usr/share/openstack-dashboard/

cd ~/workspace/horizon
python manage.py collectstatic    # answer 'yes' to override
python manage.py compress --force
cp -r static /usr/share/openstack-dashboard/
```

Config the apache for horizon.
```
echo '
WSGIDaemonProcess dashboard
WSGIProcessGroup dashboard
WSGISocketPrefix run/wsgi

WSGIScriptAlias /dashboard /usr/share/openstack-dashboard/openstack_dashboard/wsgi/django.wsgi
WSGIPythonPath /usr/share/openstack-dashboard
Alias /static /usr/share/openstack-dashboard/static

<Directory /usr/share/openstack-dashboard/openstack_dashboard>
  Require all granted
</Directory>

<Directory /usr/share/openstack-dashboard/static>
  Require all granted
</Directory>

RedirectMatch permanent ^/$ /dashboard/
' > /etc/httpd/conf.d/openstack-dashboard.conf
```

Start horizon service

```
service memcached start
service httpd restart
```

To verify, checkout things on browser and try the vnc console. View horizon log in `/var/log/httpd` and `/var/log/horizon`.  

## Nova-network (multi-host) with 2 NICs

My experiment nodes 10.224.147.* are VMs in an openstack environment. I will create a private network in openstack and add my compute nodes the second NIC. For [openstack nic hot plugging](http://blog.aaronorosen.com/openstack-interface-hot-plugging/).

To add nic to existing vm.

```
# on openstack host
nova interface-attach --net-id <network-id> <vm-instance-id>
```

On each of my compute nodes

```
# create eth1 network script
echo '
DEVICE="eth0"
BOOTPROTO="none"
ONBOOT="yes"
TYPE="Ethernet"
IPV6INIT="no"
' > /etc/sysconfig/network-scripts/ifcfg-eth1

# bring up eth1
ifconfig eth1 up
```

On all nodes, edit the nova.conf

```
# replace below lines
vlan_interface=eth1
flat_interface=eth1
```

`public_interface` is where floating ip traffic goes. `vlan_interface` and `flat_interface` is where internal VM traffic goes.

Now, restart all nova services on all nodes. `grep -ir error /var/log/nova` is a good practice. Let's check out which interface br100 is using

```
# on host 10.224.147.168
$ brctl show
bridge name bridge id   STP enabled interfaces
br100   8000.fa163ed51638 no    eth1
                                vnet0

$ virsh vncdisplay instance-00000006
10.224.147.168:0

# ssh is passed
$ ssh cirros@192.168.123.3
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether fa:16:3e:b5:e4:78 brd ff:ff:ff:ff:ff:ff
    inet 192.168.123.3/24 brd 192.168.123.255 scope global eth0
    inet6 fe80::f816:3eff:feb5:e478/64 scope link 
       valid_lft forever preferred_lft forever

$ route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         192.168.123.1   0.0.0.0         UG    0      0        0 eth0
192.168.123.0   *               255.255.255.0   U     0      0        0 eth0
```

Lets vnc to vm 192.168.123.3 (10.224.147.168:0) and ping other vms

```
# vnc 10.224.147.168:0
$ ping 192.168.123.4
... # sh*t still no response
```

Sh*t still no response. Trace arp flow at compute host. The arp reply reaches br100 but not vnet0

```
# on host 10.224.147.168
$ tcpdump -i br100 -vvv -nnn -X arp
tcpdump: listening on br100, link-type EN10MB (Ethernet), capture size 65535 bytes
08:12:11.638495 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
08:12:11.638640 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
08:12:11.640233 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.4 is-at fa:16:3e:6e:d8:92, length 42
  0x0000:  0001 0800 0604 0002 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 fa16 3eb5 e478 c0a8 7b03 0000 0000  {...>..x..{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
...

9 packets captured
9 packets received by filter
0 packets dropped by kernel

$ ifconfig vnet0
vnet0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc16:3eff:feb5:e478  prefixlen 64  scopeid 0x20<link>
        ether fe:16:3e:b5:e4:78  txqueuelen 500  (Ethernet)
        RX packets 2244  bytes 110644 (108.0 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4289  bytes 194865 (190.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ tcpdump -i vnet0 -vvv -nnn -X arp
tcpdump: WARNING: vnet0: no IPv4 address assigned
tcpdump: listening on vnet0, link-type EN10MB (Ethernet), capture size 65535 bytes
08:12:41.647424 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
08:12:41.647450 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.

$ tcpdump -i eth1 -vvv -nnn -X arp
tcpdump: WARNING: eth1: no IPv4 address assigned
tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
08:17:25.766466 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
08:17:25.766576 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
08:17:25.767228 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.4 is-at fa:16:3e:6e:d8:92, length 42
  0x0000:  0001 0800 0604 0002 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 fa16 3eb5 e478 c0a8 7b03 0000 0000  {...>..x..{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
...

12 packets captured
12 packets received by filter
0 packets dropped by kernel
```

The problem is still there. NOTHING SOLVED!

```
$ ebtables -L --Ln
Bridge table: filter

Bridge chain: INPUT, entries: 1, policy: ACCEPT
1. -p ARP -i eth1 --arp-ip-dst 192.168.123.1 -j DROP 

Bridge chain: FORWARD, entries: 2, policy: ACCEPT
1. -p IPv4 -o eth1 --ip-proto udp --ip-dport 67:68 -j DROP 
2. -p IPv4 -i eth1 --ip-proto udp --ip-dport 67:68 -j DROP 

Bridge chain: OUTPUT, entries: 1, policy: ACCEPT
1. -p ARP -o eth1 --arp-ip-src 192.168.123.1 -j DROP 

# after I cleared it
$ ebtables -L --Ln
Bridge table: filter

Bridge chain: INPUT, entries: 0, policy: ACCEPT

Bridge chain: FORWARD, entries: 0, policy: ACCEPT

Bridge chain: OUTPUT, entries: 0, policy: ACCEPT
```

After I cleared `ebtables`, the problem still persist. I'm gonna flush iptables next

```
# on host 10.224.147.168
# save iptables
$ iptables-save -c > iptables_save.dat

# delete all rules/chains
$ iptables -F
$ iptables -X
$ iptables -t nat -F
$ iptables -t nat -X
$ iptables -t mangle -F
$ iptables -t mangle -X
$ iptables -P INPUT ACCEPT
$ iptables -P FORWARD ACCEPT
$ iptables -P OUTPUT ACCEPT
$ iptables --list
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination 
```

The problem still persists. `tcpdump` tracing below

```
# on host 10.224.147.168
$ tcpdump -i br100 -vvv -nnn -X 
tcpdump: listening on br100, link-type EN10MB (Ethernet), capture size 65535 bytes
09:16:33.211987 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
09:16:33.212170 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
09:16:33.212771 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.4 is-at fa:16:3e:6e:d8:92, length 42
  0x0000:  0001 0800 0604 0002 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 fa16 3eb5 e478 c0a8 7b03 0000 0000  {...>..x..{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
...

$ tcpdump -i vnet0 -vvv -nnn -X 
tcpdump: WARNING: vnet0: no IPv4 address assigned
tcpdump: listening on vnet0, link-type EN10MB (Ethernet), capture size 65535 bytes
09:16:46.214483 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.
09:16:46.214512 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 28
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04            {.........{.

# on host 10.224.147.173, where vnet0 belongs to the VM being pinged
$ tcpdump -i vnet0 -vvv -nnn -X 
tcpdump: WARNING: vnet0: no IPv4 address assigned
tcpdump: listening on vnet0, link-type EN10MB (Ethernet), capture size 65535 bytes
09:20:54.301884 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 42
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04 0000 0000  {.........{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
09:20:54.305769 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.4 is-at fa:16:3e:6e:d8:92, length 28
  0x0000:  0001 0800 0604 0002 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 fa16 3eb5 e478 c0a8 7b03            {...>..x..{.
09:20:55.301808 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.4 tell 192.168.123.3, length 42
  0x0000:  0001 0800 0604 0001 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 0000 0000 0000 c0a8 7b04 0000 0000  {.........{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
09:20:55.302191 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.4 is-at fa:16:3e:6e:d8:92, length 28
  0x0000:  0001 0800 0604 0002 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 fa16 3eb5 e478 c0a8 7b03            {...>..x..{.
...
```

I tried ping in the reverse side: from 192.168.123.4 ping to 192.168.123.3

```
# on host 10.224.147.168, where vm 192.168.123.3 resides
$ tcpdump -i br100 -vvv -nnn -X arp
tcpdump: listening on br100, link-type EN10MB (Ethernet), capture size 65535 bytes
12:51:01.561041 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 42
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03 0000 0000  {.........{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
12:51:01.561362 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.3 is-at fa:16:3e:b5:e4:78, length 28
  0x0000:  0001 0800 0604 0002 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 fa16 3e6e d892 c0a8 7b04            {...>n....{.
...

4 packets captured
4 packets received by filter
0 packets dropped by kernel

$ tcpdump -i vnet0 -vvv -nnn -X arp
tcpdump: WARNING: vnet0: no IPv4 address assigned
tcpdump: listening on vnet0, link-type EN10MB (Ethernet), capture size 65535 bytes
12:51:11.565952 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 42
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03 0000 0000  {.........{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
12:51:11.566440 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.3 is-at fa:16:3e:b5:e4:78, length 28
  0x0000:  0001 0800 0604 0002 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 fa16 3e6e d892 c0a8 7b04            {...>n....{.
...

6 packets captured
6 packets received by filter
0 packets dropped by kernel

$ tcpdump -i eth1 -vvv -nnn -X arp
tcpdump: WARNING: eth1: no IPv4 address assigned
tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
12:53:45.687331 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 42
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03 0000 0000  {.........{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
12:53:45.687745 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.3 is-at fa:16:3e:b5:e4:78, length 28
  0x0000:  0001 0800 0604 0002 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 fa16 3e6e d892 c0a8 7b04            {...>n....{.
...

4 packets captured
6 packets received by filter
0 packets dropped by kernel

# on host 10.224.147.173, where vm 192.168.123.4 resides
$ tcpdump -i eth1 -vvv -nnn -X arp
tcpdump: WARNING: eth1: no IPv4 address assigned
tcpdump: listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
12:57:00.959244 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 28
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03            {.........{.
12:57:00.959488 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 28
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03            {.........{.
12:57:00.960050 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.3 is-at fa:16:3e:b5:e4:78, length 42
  0x0000:  0001 0800 0604 0002 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 fa16 3e6e d892 c0a8 7b04 0000 0000  {...>n....{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
...

3 packets captured
3 packets received by filter
0 packets dropped by kernel

$ tcpdump -i br100 -vvv -nnn -X arp
tcpdump: listening on br100, link-type EN10MB (Ethernet), capture size 65535 bytes
12:57:07.964117 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 28
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03            {.........{.
12:57:07.964298 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 28
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03            {.........{.
12:57:07.964942 ARP, Ethernet (len 6), IPv4 (len 4), Reply 192.168.123.3 is-at fa:16:3e:b5:e4:78, length 42
  0x0000:  0001 0800 0604 0002 fa16 3eb5 e478 c0a8  ..........>..x..
  0x0010:  7b03 fa16 3e6e d892 c0a8 7b04 0000 0000  {...>n....{.....
  0x0020:  0000 0000 0000 0000 0000                 ..........
...

3 packets captured
6 packets received by filter
0 packets dropped by kernel

$ tcpdump -i vnet0 -vvv -nnn -X arp
tcpdump: WARNING: vnet0: no IPv4 address assigned
tcpdump: listening on vnet0, link-type EN10MB (Ethernet), capture size 65535 bytes
12:57:27.003567 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 28
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03            {.........{.
12:57:27.003589 ARP, Ethernet (len 6), IPv4 (len 4), Request who-has 192.168.123.3 tell 192.168.123.4, length 28
  0x0000:  0001 0800 0604 0001 fa16 3e6e d892 c0a8  ..........>n....
  0x0010:  7b04 0000 0000 0000 c0a8 7b03            {.........{.
...

6 packets captured
9 packets received by filter
0 packets dropped by kernel

$ ifconfig vnet0
vnet0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc16:3eff:fe6e:d892  prefixlen 64  scopeid 0x20<link>
        ether fe:16:3e:6e:d8:92  txqueuelen 500  (Ethernet)
        RX packets 16551  bytes 705872 (689.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 24171  bytes 1149481 (1.0 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

You can see, on host 10.224.147.168, br100 forwards arp request to vnet0, and vnet0 sends arp reply to br100. br100 doesn't stop forwarding packets to vnet0. But why br100 eats my arp reply? This is fu*king crazy. I'm going nuts.

ANYWAY, I DECIDE TO LEAVE THE PROBLEM BEHIND. More staff needs carried out and I'm gonna moving forward.

## Play with Floating IP

Floating ip is implemented by iptables NAT and traffic through `nova.conf::public_interface`. To make it work you need to have a pool of real public ips await to use. This usually requires the 'network admin' to allocate you these ips beforehand.

I won't have really these ips. But I will use `tcpdump` to trace whether floating ips work. Configuration guide [here](http://docs.openstack.org/admin-guide-cloud/content/nova-associate-public-ip.html).

```
# on controller node 10.224.147.166
nova-manage floating create --pool nova --ip_range 10.42.0.32/27
nova-manage floating list
nova floating-ip-bulk-list

```

To associate floating ips, refer to [here](http://docs.openstack.org/user-guide/content/floating_ip_allocate.html)

```
$ nova floating-ip-associate demo-instance1 10.42.0.34
$ nova show demo-instance1
+--------------------------------------+------------------------------------------------------------+
| Property                             | Value                                                      |
+--------------------------------------+------------------------------------------------------------+
...
| OS-EXT-SRV-ATTR:instance_name        | instance-00000003                                          |
...
| OS-EXT-STS:vm_state                  | active                                                     |
...
| demo-net network                     | 192.168.123.2, 10.42.0.34                                  |
...
| id                                   | d8aadfe5-b695-4b26-bc37-f4c4593b4c7a                       |
| image                                | cirros-0.3.3-x86_64 (0c953f24-e8f6-4d33-913c-1d06ee5dbf77) |
...
| name                                 | demo-instance1                                             |
...
+--------------------------------------+------------------------------------------------------------+
```

Check out the iptables on compute node.

```
# on host 10.224.147.174, where demo-instance1 resides
$ iptables --list -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         
nova-network-PREROUTING  all  --  anywhere             anywhere            
nova-compute-PREROUTING  all  --  anywhere             anywhere            
nova-api-metadat-PREROUTING  all  --  anywhere             anywhere            

Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
nova-network-OUTPUT  all  --  anywhere             anywhere            
nova-compute-OUTPUT  all  --  anywhere             anywhere            
nova-api-metadat-OUTPUT  all  --  anywhere             anywhere            

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
nova-network-POSTROUTING  all  --  anywhere             anywhere            
nova-compute-POSTROUTING  all  --  anywhere             anywhere            
nova-api-metadat-POSTROUTING  all  --  anywhere             anywhere            
nova-postrouting-bottom  all  --  anywhere             anywhere            
MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24    

Chain nova-api-metadat-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-POSTROUTING (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-PREROUTING (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-float-snat (1 references)
target     prot opt source               destination         

Chain nova-api-metadat-snat (1 references)
target     prot opt source               destination         
nova-api-metadat-float-snat  all  --  anywhere             anywhere            

Chain nova-compute-OUTPUT (1 references)
target     prot opt source               destination         

Chain nova-compute-POSTROUTING (1 references)
target     prot opt source               destination         

Chain nova-compute-PREROUTING (1 references)
target     prot opt source               destination         

Chain nova-compute-float-snat (1 references)
target     prot opt source               destination         

Chain nova-compute-snat (1 references)
target     prot opt source               destination         
nova-compute-float-snat  all  --  anywhere             anywhere            

Chain nova-network-OUTPUT (1 references)
target     prot opt source               destination         
DNAT       all  --  anywhere             10.42.0.34           to:192.168.123.2

Chain nova-network-POSTROUTING (1 references)
target     prot opt source               destination         
ACCEPT     all  --  192.168.123.0/24     10.224.147.173      
ACCEPT     all  --  192.168.123.0/24     192.168.123.0/24     ! ctstate DNAT
SNAT       all  --  192.168.123.2        anywhere             ctstate DNAT to:10.42.0.34

Chain nova-network-PREROUTING (1 references)
target     prot opt source               destination         
DNAT       tcp  --  anywhere             169.254.169.254      tcp dpt:http to:10.224.147.173:8775
DNAT       all  --  anywhere             10.42.0.34           to:192.168.123.2

Chain nova-network-float-snat (1 references)
target     prot opt source               destination         
SNAT       all  --  192.168.123.2        192.168.123.2        to:10.42.0.34
SNAT       all  --  192.168.123.2        anywhere             to:10.42.0.34

Chain nova-network-snat (1 references)
target     prot opt source               destination         
nova-network-float-snat  all  --  anywhere             anywhere            
SNAT       all  --  192.168.123.0/24     anywhere             to:10.224.147.173

Chain nova-postrouting-bottom (1 references)
target     prot opt source               destination         
nova-network-snat  all  --  anywhere             anywhere            
nova-compute-snat  all  --  anywhere             anywhere            
nova-api-metadat-snat  all  --  anywhere             anywhere 
```

You can see the SNAT/DNAT above, who does floating ip translation. demo-instance1's address is `192.168.123.2`.

```
# vnc to demo-instance1
$ ping 8.8.8.8

# trace on host 10.224.147.174, where demo-instance1 resides
$ tcpdump -i eth0 -vvv -nnn icmp
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
14:19:15.971441 IP (tos 0x0, ttl 63, id 44386, offset 0, flags [DF], proto ICMP (1), length 84)
    10.42.0.34 > 8.8.8.8: ICMP echo request, id 10241, seq 428, length 64
14:19:16.971957 IP (tos 0x0, ttl 63, id 44387, offset 0, flags [DF], proto ICMP (1), length 84)
    10.42.0.34 > 8.8.8.8: ICMP echo request, id 10241, seq 429, length 64
...
```

So translated packets are sent out from VM demo-instance1 to public.
