

TODO architecture

## Environment

Continuing from my last post "play with openstack nova"

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

I will disable nova-network and install neutron on this environment.

## Preparation

First, let's check whether network namespace is supported in kernel

```
# should raise no error if supported
$ ip netns lis
$ ip netns add spredzy
$ ip netns list
spredzy
```

Shutdown nova-network

```
# on each node
pkill nova-network; ps -ef|grep nova-network
# nova-api-meta is harder to kill, it seems ...
for i in $(ps -ef|grep nova-api-metadata | awk '{print $2}'); do kill $i; done; ps -ef|grep nova-api-metadata
```

Kill all dnsmasq processes

```
pkill dnsmasq; ps -ef|grep dnsmasq
```

Delete all VMs. There should be a migration from nova-network to neutron but for now I just keep it simple.

```
# run below for 3 times to make sure vm is deleted from virsh
for i in 1 2 3 4; do nova reset-state demo-instance${i}; nova force-delete demo-instance${i}; done;
... # wail until deleting finishes

# if vm in error state, don't worry. I just want it removed from libvirt 
nova list

# on compute node, check vm removed from libvirt
virsh list --all
```

Clean nova database

```
mysql -uroot -p
mysql> drop database nova;
mysql> create database nova;
mysql> exit;

nova-manage db sync
nova --debug list
```

On each node, clean network tables.

```
# clean iptables
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables --list

# clean ebtables
ebtables --flush
ebtables --list

# clean route
ip route del 192.168.123.0/24 dev br100  proto kernel  scope link  src 192.168.123.1
ip route

# delete br100
ifconfig br100 down
brctl delbr br100
brctl show
```

On each node, config kernel networking parameters for neutron

```
echo '
net.ipv4.ip_forward=1
net.ipv4.conf.all.rp_filter=0
net.ipv4.conf.default.rp_filter=0
' >> /etc/sysctl.conf

# make the settings to take effect
sysctl -p
```

On each node, enable `ipsets`

```
yum install -y ipset
# should raise no error
ipset list
```

On each node install haproxy

```
yum install -y haproxy
```

On each node, install openvswitch. There is no official rpm from openvswitch, so I have to strip it from RDO repo

```
cd ~
wget https://repos.fedorapeople.org/repos/openstack/openstack-juno/rdo-release-juno-1.noarch.rpm
yum install -y rdo-release-juno-1.noarch.rpm
yum install -y openvswitch openvswitch-devel python-openvswitch
yum remove -y rdo-release-juno-1.noarch

# to start
#service openvswitch start
```

## Install Neutron

Following [neutron developer guide](http://docs.openstack.org/developer/neutron/devref/development.environment.html) and [installation manual](http://docs.openstack.org/juno/install-guide/install/apt/content/section_neutron-networking.html).

Neutron install things controller node, network node and compute node. I will keep using the environment from my last "play with openstack nova" post.

  * neutron controller
      * 10.224.147.166

  * neutron compute node (this means nova compute node)
      * 10.224.147.167
      * 10.224.147.168
      * 10.224.147.173

  * neutron network node (compute node also act as network node)
      * 10.224.147.167
      * 10.224.147.168
      * 10.224.147.173

On each node, install neutron

```
mkdir ~/workspace
cd ~/workspace
git clone git://git.openstack.org/openstack/neutron.git
cd neutron
git checkout stable/juno
pip install -r requirements.txt
python setup.py install
cd ~
```

On each node, create user and directories.

```
useradd -r -s /sbin/nologin neutron

mkdir /var/lib/neutron/
mkdir /var/lib/neutron/dhcp
mkdir /var/lib/neutron/external
mkdir /var/lib/neutron/keystone-signing
mkdir /var/lib/neutron/lbaas
mkdir /var/lib/neutron/lock
mkdir /var/log/neutron
mkdir /etc/neutron
cp -r ~/workspace/neutron/etc/* /etc/neutron/
cp -r ~/workspace/neutron/etc/neutron/* /etc/neutron/

chown -R neutron:neutron /var/lib/neutron
chown -R neutron:neutron /var/log/neutron
chown -R neutron:neutron /etc/neutron
```

Create database

```
mysql -uroot -p
mysql> create database neutron;
mysql> exit;
```

Create the keystone user, service and endpoint

```
source openstack-admin.rc
keystone user-create --name neutron --pass 123work
keystone user-role-add --user neutron --tenant service --role admin
keystone service-create --name neutron --type network --description "OpenStack Networking"
keystone endpoint-create --service-id $(keystone service-list | awk '/ network / {print $2}') --publicurl http://10.224.147.166:9696 --adminurl http://10.224.147.166:9696 --internalurl http://10.224.147.166:9696 --region regionOne
```

## Config Neutron

On each node, config neutron. Refer to [source code](https://github.com/openstack/neutron/tree/stable/juno/etc) on github for config options.

```
cp /etc/neutron/neutron.conf /etc/neutron/neutron.conf.sample
echo '
[DEFAULT]
verbose = True
debug = True
lock_path = $state_path/lock

notify_nova_on_port_status_changes = True
notify_nova_on_port_data_changes = True
nova_url = http://10.224.147.166:8774/v2
nova_admin_auth_url = http://10.224.147.166:35357/v2.0
nova_region_name = regionOne
nova_admin_username = nova
nova_admin_tenant_id = c1eec4d4365f41d8b1fe47e71da00956
nova_admin_password = 123work

rpc_backend = rabbit
rabbit_host = 10.224.147.166
rabbit_userid = root
rabbit_password = 123work

auth_strategy = keystone

core_plugin = ml2
service_plugins = router,firewall,lbaas,vpnaas,metering
allow_overlapping_ips = True

[keystone_authtoken]
auth_host = 10.224.147.166
auth_port = 35357
auth_protocol = http
admin_tenant_name = service
admin_user = neutron
admin_password = 123work

[database]
# if compute node, better comment this line out because compute node doesnt access database directly
connection = mysql://root:123work@10.224.147.166/neutron

[service_providers]
service_provider=LOADBALANCER:Haproxy:neutron.services.loadbalancer.drivers.haproxy.plugin_driver.HaproxyOnHostPluginDriver:default
service_provider=VPN:openswan:neutron.services.vpn.service_drivers.ipsec.IPsecVPNDriver:default

[agent]
root_helper=sudo neutron-rootwrap /etc/neutron/rootwrap.conf
' > /etc/neutron/neutron.conf
```

On each node, config the ML2 plugin. I want to use vxlan. A reference at [here](http://www.opencloudblog.com/?p=300).

```
cp /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugins/ml2/ml2_conf.ini.sample
echo '
[ml2]
type_drivers = local,flat,vlan,gre,vxlan
tenant_network_types = vlan,gre,vxlan
mechanism_drivers = openvswitch,linuxbridge

extension_drivers = anewextensiondriver

[ml2_type_flat]
flat_networks = external

[ml2_type_vlan]
network_vlan_ranges = external:1000:2999

[ml2_type_gre]
tunnel_id_ranges = 32769:34000

[ml2_type_vxlan]
vni_ranges = 65537:69999
vxlan_group = 239.1.1.1

[securitygroup]
enable_security_group = True
enable_ipset = True
firewall_driver = neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver

[ovs]
# CHANGE according to host
local_ip = 10.224.147.166
enable_tunneling = True
bridge_mappings = external:br-ex

[agent]
tunnel_types = vxlan
root_helper=sudo neutron-rootwrap /etc/neutron/rootwrap.conf
' > /etc/neutron/plugins/ml2/ml2_conf.ini
```

On each node, add sudoers for neutron

```
echo 'Defaults:neutron !requiretty

neutron ALL = (root) NOPASSWD: /usr/bin/neutron-rootwrap /etc/neutron/rootwrap.conf *
' > /etc/sudoers.d/neutron
```

On each node, edit the existing nova.conf to use neutron

```
vim /etc/nova/nova.conf
# replace below lines
network_api_class = nova.network.neutronv2.api.API
security_group_api = neutron
linuxnet_interface_driver = nova.network.linux_net.LinuxOVSInterfaceDriver
firewall_driver = nova.virt.firewall.NoopFirewallDriver

echo '
[neutron]
url = http://10.224.147.166:9696
auth_strategy = keystone
admin_auth_url = http://10.224.147.166:35357/v2.0
admin_tenant_name = service
admin_username = neutron
admin_password = 123work
neutron_metadata_proxy_shared_secret = 123work
service_metadata_proxy = True
' >> /etc/nova/nova.conf
```

On each node, config the L3 agent

```
cp /etc/neutron/l3_agent.ini /etc/neutron/l3_agent.ini.sample
echo '
[DEFAULT]
debug = True
verbose = True
interface_driver = neutron.agent.linux.interface.OVSInterfaceDriver
use_namespaces = True
external_network_bridge = br-ex
' > /etc/neutron/l3_agent.ini
```

On each node, config the dhcp agent

```
cp /etc/neutron/dhcp_agent.ini /etc/neutron/dhcp_agent.ini.sample
echo '
[DEFAULT]
debug = True
verbose = True

interface_driver = neutron.agent.linux.interface.OVSInterfaceDriver
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
' > /etc/neutron/dhcp_agent.ini
```

On each node, config the metadata agent

```
cp /etc/neutron/metadata_agent.ini /etc/neutron/metadata_agent.ini.sample
echo '
[DEFAULT]
debug = True
verbose = True

auth_url = http://10.224.147.166:5000/v2.0
auth_region = regionOne
admin_tenant_name = service
admin_user = neutron
admin_password = 123work

nova_metadata_ip = 10.224.147.166
metadata_proxy_shared_secret = 123work
' > /etc/neutron/metadata_agent.ini
```

On each node, config openvswitch

```
service openvswitch restart
ovs-vsctl add-br br-ex
ovs-vsctl add-port br-ex eth2
ovs-vsctl show
```

On each node, config the lbaas agent

```
cp /etc/neutron/lbaas_agent.ini /etc/neutron/lbaas_agent.ini.sample
echo '
[DEFAULT]
debug = True
verbose = True

interface_driver = neutron.agent.linux.interface.OVSInterfaceDriver
device_driver = neutron.services.loadbalancer.drivers.haproxy.namespace_driver.HaproxyNSDriver

[haproxy]
loadbalancer_state_path = $state_path/lbaas
user_group = haproxy
' > /etc/neutron/lbaas_agent.ini
```

Update the datbase

```
su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade juno" neutron
```

## Start Neutron

First, I need to restart nova completely

```
# run multiple times to ensure nova killed
pkill nova; ps -ef|grep nova

# start nova on controller nodes
su -s /bin/bash nova -c '/bin/nova-api >> /var/log/nova/nova-api.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-cert >> /var/log/nova/nova-cert.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-novncproxy >> /var/log/nova/nova-novncproxy.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-consoleauth >> /var/log/nova/nova-consoleauth.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-scheduler >> /var/log/nova/nova-scheduler.log 2>&1' &
su -s /bin/bash nova -c '/bin/nova-conductor >> /var/log/nova/nova-conductor.log 2>&1' &

# start nova on compute nodes
su -s /bin/bash nova -c '/bin/nova-compute >> /var/log/nova/nova-compute.log 2>&1' &

# check error in log
grep -ir error /var/log/nova/*
```

Let's start neutron

```
# on each node
service openvswitch restart

# on controller node
su -s /bin/bash neutron -c '/bin/neutron-server >> /var/log/neutron/server.log 2>&1' &

# on network nodes
su -s /bin/bash neutron -c '/bin/neutron-openvswitch-agent >> /var/log/neutron/openvswitch-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-l3-agent --config-file /etc/neutron/l3_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/l3-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-dhcp-agent --config-file /etc/neutron/dhcp_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/dhcp-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-metadata-agent --config-file /etc/neutron/metadata_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/metadata-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-lbaas-agent --config-file /etc/neutron/lbaas_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/lbaas-agent.log 2>&1' &

# on compute nodes
su -s /bin/bash neutron -c '/bin/neutron-openvswitch-agent >> /var/log/neutron/openvswitch-agent.log 2>&1' &

# check error in log
grep -ir error /var/log/neutron/*

# to stop
#pkill neutron; ps -ef|grep neutron
```

To verify

```
# on controller node
$ source openstack-admin.rc 
$ neutron ext-list
-----------------------+-----------------------------------------------+
| alias                 | name                                          |
+-----------------------+-----------------------------------------------+
| security-group        | security-group                                |
| l3_agent_scheduler    | L3 Agent Scheduler                            |
| ext-gw-mode           | Neutron L3 Configurable external gateway mode |
| binding               | Port Binding                                  |
| provider              | Provider Network                              |
| agent                 | agent                                         |
| quotas                | Quota management support                      |
| dhcp_agent_scheduler  | DHCP Agent Scheduler                          |
| l3-ha                 | HA Router extension                           |
| multi-provider        | Multi Provider Network                        |
| external-net          | Neutron external network                      |
| router                | Neutron L3 Router                             |
| allowed-address-pairs | Allowed Address Pairs                         |
| extraroute            | Neutron Extra Route                           |
| extra_dhcp_opt        | Neutron Extra DHCP opts                       |
| dvr                   | Distributed Virtual Router                    |
+-----------------------+-----------------------------------------------+
$ neutron agent-list
+--------------------------------------+--------------------+--------------------------------+-------+----------------+---------------------------+
| id                                   | agent_type         | host                           | alive | admin_state_up | binary                    |
+--------------------------------------+--------------------+--------------------------------+-------+----------------+---------------------------+
| 0a2f9089-6163-4681-8c36-7afbdbf84970 | Open vSwitch agent | openstack-03.novalocal | :-)   | True           | neutron-openvswitch-agent |
| 1ccce2dd-4b63-48cb-bd52-8e4ab88936b0 | L3 agent           | openstack-04.novalocal | :-)   | True           | neutron-l3-agent          |
| 1ea46637-dff2-4b64-8258-60cc584af330 | DHCP agent         | openstack-02.novalocal | :-)   | True           | neutron-dhcp-agent        |
| 23eb0927-37b1-4ce8-b9fd-f3cb40e0f53b | Open vSwitch agent | openstack-02.novalocal | :-)   | True           | neutron-openvswitch-agent |
| 544a9da4-4803-4f58-a823-83627e80417e | Metadata agent     | openstack-03.novalocal | :-)   | True           | neutron-metadata-agent    |
| 92dc9214-9b5a-4c23-89fb-ed71e657d2cd | DHCP agent         | openstack-04.novalocal | :-)   | True           | neutron-dhcp-agent        |
| a293d7c0-b1b6-482b-b585-c66b1c085bc3 | L3 agent           | openstack-02.novalocal | :-)   | True           | neutron-l3-agent          |
| ae341c8e-98d9-40a1-a64c-c7e8357a8d68 | L3 agent           | openstack-03.novalocal | :-)   | True           | neutron-l3-agent          |
| b4a14d16-b592-489f-a552-d72ab8f01049 | DHCP agent         | openstack-03.novalocal | :-)   | True           | neutron-dhcp-agent        |
| dbcc3b44-6f68-4f80-ac37-7beb3d1b5633 | Open vSwitch agent | openstack-04.novalocal | :-)   | True           | neutron-openvswitch-agent |
| f4c78a1b-a766-463c-985d-6752d46588e2 | Metadata agent     | openstack-02.novalocal | :-)   | True           | neutron-metadata-agent    |
| f6647411-8c34-4d5f-ace5-09562a541ca7 | Metadata agent     | openstack-04.novalocal | :-)   | True           | neutron-metadata-agent    |
+--------------------------------------+--------------------+--------------------------------+-------+----------------+---------------------------+
```

Next, I need to create [initial networks](http://docs.openstack.org/juno/install-guide/install/apt/content/neutron-initial-networks.html).

```
# on controller node, 10.224.147.166
source openstack-admin.rc

# create external network, with floating ip
$ neutron net-create ext-net --shared --router:external True --provider:physical_network external --provider:network_type flat
$ neutron subnet-create ext-net --name ext-subnet --allocation-pool start=10.224.147.230,end=10.224.147.250 --disable-dhcp --gateway 10.224.147.1 10.224.147.0/24
+-------------------+------------------------------------------------------+
| Field             | Value                                                |
+-------------------+------------------------------------------------------+
| allocation_pools  | {"start": "10.224.147.230", "end": "10.224.147.250"} |
| cidr              | 10.224.147.0/24                                      |
| dns_nameservers   |                                                      |
| enable_dhcp       | False                                                |
| gateway_ip        | 10.224.147.1                                         |
| host_routes       |                                                      |
| id                | 6bd2a08e-c133-4700-92e6-9415a9c5d764                 |
| ip_version        | 4                                                    |
| ipv6_address_mode |                                                      |
| ipv6_ra_mode      |                                                      |
| name              | ext-subnet                                           |
| network_id        | 0c8f1d57-cc5b-4903-b53e-9304581da01a                 |
| tenant_id         | c48611d23b754e909753d7ec2428819a                     |
+-------------------+------------------------------------------------------+

# create tenant network
$ neutron net-create demo-net
$ neutron subnet-create demo-net --name demo-subnet --gateway 192.168.124.1 192.168.124.0/24
+-------------------+------------------------------------------------------+
| Field             | Value                                                |
+-------------------+------------------------------------------------------+
| allocation_pools  | {"start": "192.168.124.2", "end": "192.168.124.254"} |
| cidr              | 192.168.124.0/24                                     |
| dns_nameservers   |                                                      |
| enable_dhcp       | True                                                 |
| gateway_ip        | 192.168.124.1                                        |
| host_routes       |                                                      |
| id                | 239b2216-0006-4a96-8a41-27e405a05018                 |
| ip_version        | 4                                                    |
| ipv6_address_mode |                                                      |
| ipv6_ra_mode      |                                                      |
| name              | demo-subnet                                          |
| network_id        | eaf3a591-fb39-433c-b01a-f74aaa814405                 |
| tenant_id         | c48611d23b754e909753d7ec2428819a                     |
+-------------------+------------------------------------------------------+
```

In neutron, a network which is mapped to a physical network is called '[provider network](https://developer.rackspace.com/blog/beginning-to-understand-neutron-provider-and-tenant-networks-in-openstack/)'. Above external network is also a provider network. You can use it to boot VMs directly on provider network, as the example setup below

```
$ neutron net-show abe6d002-1efc-4d34-b241-d880cf8dd5d8
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | True                                 |
| id                        | abe6d002-1efc-4d34-b241-d880cf8dd5d8 |
| name                      | QA_vlan_220                          |
| provider:network_type     | vlan                                 |
| provider:physical_network | physnet1                             |
| provider:segmentation_id  | 220                                  |
| router:external           | False                                |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   | 8b6b9df6-f208-4ad0-9ec8-07c4ca30d281 |
| tenant_id                 | c3df8eadad4145b1b0ea4bb23a537dc6     |
+---------------------------+--------------------------------------+

# the subnet of QA_vlan_220, where we boot VM
$ neutron subnet-show 8b6b9df6-f208-4ad0-9ec8-07c4ca30d281
+------------------+---------------------------------------------------------+
| Field            | Value                                                   |
+------------------+---------------------------------------------------------+
| allocation_pools | {"start": "10.224.147.150", "end": "10.224.147.254"}    |
| cidr             | 10.224.147.0/24                                         |
| dns_nameservers  | 10.224.96.228                                           |
|                  | 8.8.8.8                                                 |
| enable_dhcp      | True                                                    |
| gateway_ip       |                                                         |
| host_routes      | {"destination": "0.0.0.0/0", "nexthop": "10.224.147.1"} |
| id               | 8b6b9df6-f208-4ad0-9ec8-07c4ca30d281                    |
| ip_version       | 4                                                       |
| name             | QA_vlan220                                              |
| network_id       | abe6d002-1efc-4d34-b241-d880cf8dd5d8                    |
| tenant_id        | c3df8eadad4145b1b0ea4bb23a537dc6                        |
+------------------+---------------------------------------------------------+

$ neutron net-show 0ae66644-755c-4cd4-9667-a842c50f905c
+---------------------------+-------------------------------------------------------+
| Field                     | Value                                                 |
+---------------------------+-------------------------------------------------------+
| admin_state_up            | True                                                  |
| id                        | 0ae66644-755c-4cd4-9667-a842c50f905c                  |
| name                      | Shared_Provider_Network_Vlan850                       |
| provider:network_type     | vlan                                                  |
| provider:physical_network | physnet1                                              |
| provider:segmentation_id  | 850                                                   |
| router:external           | False                                                 |
| shared                    | True                                                  |
| status                    | ACTIVE                                                |
| subnets                   | 24a2d531-4987-4460-8d2d-a136b8ecee4d                  |
| tenant_id                 | 08a8d2afde8d40c49ad8aee4ac531aed                      |
+---------------------------+-------------------------------------------------------+

# the subnet of Shared_Provider_Network_Vlan850, where we boot VM
$ neutron subnet-show 24a2d531-4987-4460-8d2d-a136b8ecee4d
+------------------+----------------------------------------------------------+
| Field            | Value                                                    |
+------------------+----------------------------------------------------------+
| allocation_pools | {"start": "10.224.148.69", "end": "10.224.148.94"}       |
| cidr             | 10.224.148.64/27                                         |
| dns_nameservers  | 10.224.96.228                                            |
|                  | 8.8.8.8                                                  |
| enable_dhcp      | True                                                     |
| gateway_ip       |                                                          |
| host_routes      | {"destination": "0.0.0.0/0", "nexthop": "10.224.148.65"} |
| id               | 24a2d531-4987-4460-8d2d-a136b8ecee4d                     |
| ip_version       | 4                                                        |
| name             | sub_vlan_850                                             |
| network_id       | 0ae66644-755c-4cd4-9667-a842c50f905c                     |
| tenant_id        | 08a8d2afde8d40c49ad8aee4ac531aed                         |
+------------------+----------------------------------------------------------+
```

But, in the current experiment carrying out, we boot VM from tenant network and route it to external network.

```
$ neutron router-create demo-router
Created a new router:
+-----------------------+--------------------------------------+
| Field                 | Value                                |
+-----------------------+--------------------------------------+
| admin_state_up        | True                                 |
| distributed           | False                                |
| external_gateway_info |                                      |
| ha                    | False                                |
| id                    | 31742f37-d5fa-49a1-bb58-25cac0a93332 |
| name                  | demo-router                          |
| routes                |                                      |
| status                | ACTIVE                               |
| tenant_id             | c48611d23b754e909753d7ec2428819a     |
+-----------------------+--------------------------------------+

$ neutron router-interface-add demo-router demo-subnet
Added interface 4d03977a-8140-4c36-acfa-5163587668db to router demo-router.

$ neutron router-gateway-set demo-router ext-net
Set gateway for router demo-router

$ neutron router-show demo-router
+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field                 | Value                                                                                                                                                                                      |
+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| admin_state_up        | True                                                                                                                                                                                       |
| distributed           | False                                                                                                                                                                                      |
| external_gateway_info | {"network_id": "0c8f1d57-cc5b-4903-b53e-9304581da01a", "enable_snat": true, "external_fixed_ips": [{"subnet_id": "6bd2a08e-c133-4700-92e6-9415a9c5d764", "ip_address": "10.224.147.230"}]} |
| ha                    | False                                                                                                                                                                                      |
| id                    | 31742f37-d5fa-49a1-bb58-25cac0a93332                                                                                                                                                       |
| name                  | demo-router                                                                                                                                                                                |
| routes                |                                                                                                                                                                                            |
| status                | ACTIVE                                                                                                                                                                                     |
| tenant_id             | c48611d23b754e909753d7ec2428819a                                                                                                                                                           |
+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

I have checked the security group to allow all ingress and egress. Now let's try boot a VM.

```
nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64_swift --nic net-id=eaf3a591-fb39-433c-b01a-f74aaa814405 --security-group default demo-instance1
```



private: 10.0.0.0 - 10.255.255.255
ovs-ofctl dump-flows br-int


TODO launch vm
TODO ping vm eachother
TODO ping vm outside
TODO trace network traffic
TODO test lbaas service
TODO test metadata services
TODO restore /etc/passwd::neutron login

https://blogs.oracle.com/ronen/entry/diving_into_openstack_network_architecture