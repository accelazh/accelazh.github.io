

TODO architecture

https://blog.kghost.info/2013/03/01/linux-network-emulator/
https://blog.kghost.info/2014/11/19/openvswitch-internal/

ovs experiment
http://blog.scottlowe.org/2013/09/09/namespaces-vlans-open-vswitch-and-gre-tunnels/
http://blog.scottlowe.org/2013/05/07/using-gre-tunnels-with-open-vswitch/

in the past we have monolithic plugins. now introduc ML2, which is also a plugin. ML2 contains many drivers. agent side also have many implementations. currently there is a blueprint calls ML2-agnet: "A modular agent may be developed as a follow-on effort".

Modular Layer 2 In OpenStack Neutron
https://www.openstack.org/assets/presentation-media/ML2-Past-Present-and-Future.pptx
ML2 wiki
https://wiki.openstack.org/wiki/Neutron/ML2

neutron concepts
http://docs.openstack.org/juno/install-guide/install/apt/content/neutron-concepts.html


TODO add my picture on paper

--------

neutron中，不同的network可以使用不同的ethX，这样可以一个用gre，一个用vlan，一个vxlan，不同网口也可以让流量负载分开承担。

---------

Neutron LBaaS使用的是同样思路。在你想要做lb的physical node上，装agent。neutron controller会根据一个scheduler，选择node起haproxy。neutron controller怎么知道哪些node是被用来做lbaas的？根据你在哪里装了agent。

---------

add to nova-network + picture

hard_xmit来完成的，在这个hard_xmit中，打上相应的tag后，再调用eth0的hard_xmit将数据真正发出，如下图所示：
http://blog.csdn.net/dog250/article/details/7354590
以及router对vlan的支持
实际上就是一个薄层hard_xmit，打上tag，交给下一层

---------





## Environment

Continuing from my last post "play with openstack nova"

  * node 1: 10.224.147.166, CentOS 7, hostname openstack-01
    * nova-api
    * nova-scheduler
    * nova-novncproxy
    * nova-consoleauth
    * nova-conductor
    * glance (with filestore backend)
    * mysql
    * keystone
    * rabbitmq
  
  * node 2: 10.224.147.167, CentOS 7, hostname openstack-02
    * nova-compute
    * nova-network
    * nova-api-metadata

  * node 3: 10.224.147.168, CentOS 7, hostname openstack-03
    * nova-compute
    * nova-network
    * nova-api-metadata

  * node 4: 10.224.147.173, CentOS 7, hostname openstack-04
    * nova-compute
    * nova-network
    * nova-api-metadata

All nodes have each other's hostname in /etc/hosts. I will disable nova-network and install neutron on this environment.

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
service_plugins = router,lbaas
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
#service_provider=VPN:openswan:neutron.services.vpn.service_drivers.ipsec.IPsecVPNDriver:default

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
tenant_network_type = vxlan
network_vlan_ranges = 
enable_tunneling = True
tunnel_type = vxlan
tunnel_id_ranges = 32769:34000

# CHANGE according to host
local_ip = 10.224.147.166

bridge_mappings = external:br-ex

[agent]
tunnel_types = vxlan
root_helper=sudo neutron-rootwrap /etc/neutron/rootwrap.conf
' > /etc/neutron/plugins/ml2/ml2_conf.ini
```

On each node, config the plugin.ini

```
cp /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini.sample
echo '
[ovs]
tenant_network_type = vxlan
network_vlan_ranges = 
enable_tunneling = True
tunnel_type = vxlan
tunnel_id_ranges = 32769:34000

# CHANGE according to host
local_ip = 10.224.147.166

bridge_mappings = external:br-ex

[agent]
tunnel_types = vxlan
enable_distributed_routing = False
root_helper=sudo neutron-rootwrap /etc/neutron/rootwrap.conf

[securitygroup]
firewall_driver = neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver
enable_security_group = True
' > /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini
```

Create the plugin.ini. Note that scp copy with change symbolic link to concrete file.

```
ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
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
su -s /bin/bash neutron -c '/bin/neutron-server --config-file /etc/neutron/plugins/ml2/ml2_conf.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/server.log 2>&1' &

# on network nodes
su -s /bin/bash neutron -c '/bin/neutron-openvswitch-agent --config-file /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/openvswitch-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-l3-agent --config-file /etc/neutron/l3_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/l3-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-dhcp-agent --config-file /etc/neutron/dhcp_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/dhcp-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-metadata-agent --config-file /etc/neutron/metadata_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/metadata-agent.log 2>&1' &
su -s /bin/bash neutron -c '/bin/neutron-lbaas-agent --config-file /etc/neutron/lbaas_agent.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/lbaas-agent.log 2>&1' &

# on compute nodes (alread started in above)
#su -s /bin/bash neutron -c '/bin/neutron-openvswitch-agent --config-file /etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini --config-file /etc/neutron/neutron.conf >> /var/log/neutron/openvswitch-agent.log 2>&1' &

# check error in log
grep -ir -E "error|fail" /var/log/neutron

# to stop
#pkill dnsmasq; pkill neutron; ps -ef|grep neutron
#rm -rf /var/log/neutron/*
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
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | True                                 |
| id                        | c88ef4ed-973e-4fb5-97b4-3a329f032728 |
| name                      | ext-net                              |
| provider:network_type     | flat                                 |
| provider:physical_network | external                             |
| provider:segmentation_id  |                                      |
| router:external           | True                                 |
| shared                    | True                                 |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| tenant_id                 | c48611d23b754e909753d7ec2428819a     |
+---------------------------+--------------------------------------+

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
| id                | f20120e9-12be-461f-ab15-e1c24e9be2a1                 |
| ip_version        | 4                                                    |
| ipv6_address_mode |                                                      |
| ipv6_ra_mode      |                                                      |
| name              | ext-subnet                                           |
| network_id        | c88ef4ed-973e-4fb5-97b4-3a329f032728                 |
| tenant_id         | c48611d23b754e909753d7ec2428819a                     |
+-------------------+------------------------------------------------------+

# create tenant network
$ neutron net-create demo-net --provider:network_type vxlan
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | True                                 |
| id                        | 02320589-b038-493a-9106-c9c2c3ebdb42 |
| name                      | demo-net                             |
| provider:network_type     | vxlan                                |
| provider:physical_network |                                      |
| provider:segmentation_id  | 65537                                |
| router:external           | False                                |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| tenant_id                 | c48611d23b754e909753d7ec2428819a     |
+---------------------------+--------------------------------------+

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
| id                | 7b48f2da-62df-4a27-b2f8-f84cb8e13921                 |
| ip_version        | 4                                                    |
| ipv6_address_mode |                                                      |
| ipv6_ra_mode      |                                                      |
| name              | demo-subnet                                          |
| network_id        | 02320589-b038-493a-9106-c9c2c3ebdb42                 |
| tenant_id         | c48611d23b754e909753d7ec2428819a                     |
+-------------------+------------------------------------------------------+

$ grep -ir -E 'error|fail' /var/log/neutron
```

In neutron, a network which is mapped to a physical network is called '[provider network](https://developer.rackspace.com/blog/beginning-to-understand-neutron-provider-and-tenant-networks-in-openstack/)'. Above external network is a provider network. You can use it to boot VMs directly on provider network, as the example setup below

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
| id                    | ab22e15f-9d41-4d69-afa8-0b6c6820c296 |
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
| external_gateway_info | {"network_id": "c88ef4ed-973e-4fb5-97b4-3a329f032728", "enable_snat": true, "external_fixed_ips": [{"subnet_id": "f20120e9-12be-461f-ab15-e1c24e9be2a1", "ip_address": "10.224.147.230"}]} |
| ha                    | False                                                                                                                                                                                      |
| id                    | ab22e15f-9d41-4d69-afa8-0b6c6820c296                                                                                                                                                       |
| name                  | demo-router                                                                                                                                                                                |
| routes                |                                                                                                                                                                                            |
| status                | ACTIVE                                                                                                                                                                                     |
| tenant_id             | c48611d23b754e909753d7ec2428819a                                                                                                                                                           |
+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

I have checked the security group to allow all ingress and egress. Now let's try boot a VM.

```
nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64_swift --nic net-id=02320589-b038-493a-9106-c9c2c3ebdb42 --security-group default demo-instance1

# to boot on specific host
#nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64_swift --nic net-id=02320589-b038-493a-9106-c9c2c3ebdb42 --security-group default demo-instance1 --availability-zone nova:openstack-03.novalocal
```

Boot another instance.

```
nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64_swift --nic net-id=02320589-b038-493a-9106-c9c2c3ebdb42 --security-group default demo-instance2
```

Boot the third instance.

```
nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64_swift --nic net-id=02320589-b038-493a-9106-c9c2c3ebdb42 --security-group default demo-instance3
```

Create and associate floating ip to VMs

```
$ neutron floatingip-create ext-net
$ neutron floatingip-create ext-net
$ neutron floatingip-create ext-net
$ neutron floatingip-list
+--------------------------------------+------------------+---------------------+---------+
| id                                   | fixed_ip_address | floating_ip_address | port_id |
+--------------------------------------+------------------+---------------------+---------+
| 6f91ae8f-61d7-40b0-b3bc-a72029e24d9e |                  | 10.224.147.234      |         |
| b932efc6-3ffd-4625-b0e8-0ebed0f52a2e |                  | 10.224.147.236      |         |
| d3405d21-88a4-4bbd-886d-ac8d60d77c00 |                  | 10.224.147.235      |         |
+--------------------------------------+------------------+---------------------+---------+
$ neutron floatingip-associate 6f91ae8f-61d7-40b0-b3bc-a72029e24d9e 11d4dec5-4471-4fd4-a809-15356997cc21
$ neutron floatingip-associate d3405d21-88a4-4bbd-886d-ac8d60d77c00 eca4315f-384b-4efc-86c7-2e43fa5777b9
$ neutron floatingip-associate b932efc6-3ffd-4625-b0e8-0ebed0f52a2e 4f6c85ef-0e53-4685-800a-5b1ceeb0c879
```

Instances setup as below

```
   name              host             ip                          port                     floating-ip
demo-instance1   openstack-03    192.168.124.2    11d4dec5-4471-4fd4-a809-15356997cc21    10.224.147.234
demo-instance2   openstack-02    192.168.124.4    eca4315f-384b-4efc-86c7-2e43fa5777b9    10.224.147.235
demo-instance3   openstack-03    192.168.124.5    4f6c85ef-0e53-4685-800a-5b1ceeb0c879    10.224.147.236
```

## Verify Neutron

Verify the console is accessible from horizon - OK.

Try login using cirros@ip from compute host - FAIL. Dump the ip gateway on compute host

```
# on host openstack-03, 10.224.147.168
$ ip route
default via 10.224.147.1 dev eth0 
10.224.147.0/24 dev eth0  proto kernel  scope link  src 10.224.147.168 
169.254.169.254 via 10.224.147.151 dev eth0  proto static 
192.168.122.0/24 dev virbr0  proto kernel  scope link  src 192.168.122.1 
```

No route to 192.168.124.0/24. Possible this is supposed by neutron.

`iptables --list` shows that neutron and openvswitch-agent has modifications on it (incuding nat table). Dump openvswitch bridges

```
# on host openstack-03, 10.224.147.168
$ ovs-vsctl show
2e68b536-3378-4717-9088-9ba1d96dbf68
    Bridge br-tun
        Port "vxlan-0ae093a7"
            Interface "vxlan-0ae093a7"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="10.224.147.168", out_key=flow, remote_ip="10.224.147.167"}
        Port br-tun
            Interface br-tun
                type: internal
        Port "vxlan-0ae093a6"
            Interface "vxlan-0ae093a6"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="10.224.147.168", out_key=flow, remote_ip="10.224.147.166"}
        Port patch-int
            Interface patch-int
                type: patch
                options: {peer=patch-tun}
        Port "vxlan-0ae093ad"
            Interface "vxlan-0ae093ad"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="10.224.147.168", out_key=flow, remote_ip="10.224.147.173"}
    Bridge br-int
        fail_mode: secure
        Port patch-tun
            Interface patch-tun
                type: patch
                options: {peer=patch-int}
        Port br-int
            Interface br-int
                type: internal
        Port "qvo4f6c85ef-0e"
            tag: 2
            Interface "qvo4f6c85ef-0e"
        Port int-br-ex
            Interface int-br-ex
                type: patch
                options: {peer=phy-br-ex}
        Port "qr-5c4fee91-c1"
            tag: 2
            Interface "qr-5c4fee91-c1"
                type: internal
        Port "qvo11d4dec5-44"
            tag: 2
            Interface "qvo11d4dec5-44"
    Bridge br-ex
        Port br-ex
            Interface br-ex
                type: internal
        Port "eth2"
            Interface "eth2"
        Port "qg-6eff0712-2b"
            Interface "qg-6eff0712-2b"
                type: internal
        Port phy-br-ex
            Interface phy-br-ex
                type: patch
                options: {peer=int-br-ex}
    ovs_version: "2.1.3"

$ ovs-ofctl dump-flows br-int
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=54744.465s, table=0, n_packets=777, n_bytes=90232, idle_age=163, priority=1 actions=NORMAL
 cookie=0x0, duration=54743.519s, table=0, n_packets=10, n_bytes=864, idle_age=639, priority=2,in_port=30 actions=drop
 cookie=0x0, duration=54744.393s, table=23, n_packets=0, n_bytes=0, idle_age=54744, priority=0 actions=drop

$ ovs-ofctl dump-flows br-tun
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=54755.065s, table=0, n_packets=0, n_bytes=0, idle_age=54755, priority=0 actions=drop
 cookie=0x0, duration=54753.912s, table=0, n_packets=160, n_bytes=16184, idle_age=175, priority=1,in_port=3 actions=resubmit(,4)
 cookie=0x0, duration=54755.135s, table=0, n_packets=211, n_bytes=25852, idle_age=175, priority=1,in_port=1 actions=resubmit(,2)
 cookie=0x0, duration=54753.682s, table=0, n_packets=0, n_bytes=0, idle_age=54753, priority=1,in_port=4 actions=resubmit(,4)
 cookie=0x0, duration=54754.137s, table=0, n_packets=0, n_bytes=0, idle_age=54754, priority=1,in_port=2 actions=resubmit(,4)
 cookie=0x0, duration=54754.928s, table=2, n_packets=115, n_bytes=12308, idle_age=180, priority=0,dl_dst=01:00:00:00:00:00/01:00:00:00:00:00 actions=resubmit(,22)
 cookie=0x0, duration=54754.997s, table=2, n_packets=96, n_bytes=13544, idle_age=175, priority=0,dl_dst=00:00:00:00:00:00/01:00:00:00:00:00 actions=resubmit(,20)
 cookie=0x0, duration=54754.859s, table=3, n_packets=0, n_bytes=0, idle_age=54754, priority=0 actions=drop
 cookie=0x0, duration=54754.788s, table=4, n_packets=0, n_bytes=0, idle_age=54754, priority=0 actions=drop
 cookie=0x0, duration=659.672s, table=4, n_packets=160, n_bytes=16184, idle_age=175, priority=1,tun_id=0x10001 actions=mod_vlan_vid:2,resubmit(,10)
 cookie=0x0, duration=54754.720s, table=10, n_packets=160, n_bytes=16184, idle_age=175, priority=1 actions=learn(table=20,hard_timeout=300,priority=1,NXM_OF_VLAN_TCI[0..11],NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[],load:0->NXM_OF_VLAN_TCI[],load:NXM_NX_TUN_ID[]->NXM_NX_TUN_ID[],output:NXM_OF_IN_PORT[]),output:1
 cookie=0x0, duration=54754.651s, table=20, n_packets=0, n_bytes=0, idle_age=54754, priority=0 actions=resubmit(,22)
 cookie=0x0, duration=254.578s, table=20, n_packets=82, n_bytes=12440, hard_timeout=300, idle_age=201, hard_age=201, priority=1,vlan_tci=0x0002/0x0fff,dl_dst=fa:16:3e:4f:37:67 actions=load:0->NXM_OF_VLAN_TCI[],load:0x10001->NXM_NX_TUN_ID[],output:3
 cookie=0x0, duration=265.622s, table=20, n_packets=0, n_bytes=0, hard_timeout=300, idle_age=265, hard_age=261, priority=1,vlan_tci=0x0002/0x0fff,dl_dst=de:13:53:23:04:91 actions=load:0->NXM_OF_VLAN_TCI[],load:0x10001->NXM_NX_TUN_ID[],output:3
 cookie=0x0, duration=308.202s, table=20, n_packets=14, n_bytes=1104, hard_timeout=300, idle_age=175, hard_age=175, priority=1,vlan_tci=0x0002/0x0fff,dl_dst=fa:16:3e:ad:c8:82 actions=load:0->NXM_OF_VLAN_TCI[],load:0x10001->NXM_NX_TUN_ID[],output:3
 cookie=0x0, duration=54754.582s, table=22, n_packets=81, n_bytes=8820, idle_age=247, priority=0 actions=drop
 cookie=0x0, duration=659.741s, table=22, n_packets=34, n_bytes=3488, idle_age=180, dl_vlan=2 actions=strip_vlan,set_tunnel:0x10001,output:2,output:3,output:4

$ ovs-ofctl dump-flows br-ex
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=54773.861s, table=0, n_packets=10, n_bytes=864, idle_age=668, priority=1 actions=NORMAL
 cookie=0x0, duration=54773.252s, table=0, n_packets=109, n_bytes=11534, idle_age=197, priority=2,in_port=4 actions=drop
```

Dump ifconfig content

```
# on host openstack-03
$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.224.147.168  netmask 255.255.255.0  broadcast 10.224.147.255
        inet6 fe80::f816:3eff:fea8:4f41  prefixlen 64  scopeid 0x20<link>
        ether fa:16:3e:a8:4f:41  txqueuelen 1000  (Ethernet)
        RX packets 9990611  bytes 1111388015 (1.0 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 5559417  bytes 1203424066 (1.1 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 0  (Local Loopback)
        RX packets 1777838  bytes 103632532 (98.8 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1777838  bytes 103632532 (98.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

qbr11d4dec5-44: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::302d:bdff:fed5:15bb  prefixlen 64  scopeid 0x20<link>
        ether ee:a5:9e:9f:fa:dc  txqueuelen 0  (Ethernet)
        RX packets 48  bytes 4220 (4.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 8  bytes 648 (648.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

qbr4f6c85ef-0e: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::20bd:24ff:feba:c3dc  prefixlen 64  scopeid 0x20<link>
        ether 3a:19:20:f0:29:c5  txqueuelen 0  (Ethernet)
        RX packets 24  bytes 1772 (1.7 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 8  bytes 648 (648.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

qvb11d4dec5-44: flags=4419<UP,BROADCAST,RUNNING,PROMISC,MULTICAST>  mtu 1500
        inet6 fe80::eca5:9eff:fe9f:fadc  prefixlen 64  scopeid 0x20<link>
        ether ee:a5:9e:9f:fa:dc  txqueuelen 1000  (Ethernet)
        RX packets 140  bytes 18250 (17.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 161  bytes 15204 (14.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

qvb4f6c85ef-0e: flags=4419<UP,BROADCAST,RUNNING,PROMISC,MULTICAST>  mtu 1500
        inet6 fe80::3819:20ff:fef0:29c5  prefixlen 64  scopeid 0x20<link>
        ether 3a:19:20:f0:29:c5  txqueuelen 1000  (Ethernet)
        RX packets 119  bytes 15732 (15.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 167  bytes 15736 (15.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

qvo11d4dec5-44: flags=4419<UP,BROADCAST,RUNNING,PROMISC,MULTICAST>  mtu 1500
        inet6 fe80::88c9:16ff:fe2e:fc8a  prefixlen 64  scopeid 0x20<link>
        ether 8a:c9:16:2e:fc:8a  txqueuelen 1000  (Ethernet)
        RX packets 161  bytes 15204 (14.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 140  bytes 18250 (17.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

qvo4f6c85ef-0e: flags=4419<UP,BROADCAST,RUNNING,PROMISC,MULTICAST>  mtu 1500
        inet6 fe80::d4ec:8eff:fe5e:a45a  prefixlen 64  scopeid 0x20<link>
        ether d6:ec:8e:5e:a4:5a  txqueuelen 1000  (Ethernet)
        RX packets 167  bytes 15736 (15.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 119  bytes 15732 (15.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tap11d4dec5-44: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc16:3eff:fe64:41e4  prefixlen 64  scopeid 0x20<link>
        ether fe:16:3e:64:41:e4  txqueuelen 500  (Ethernet)
        RX packets 146  bytes 13998 (13.6 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 127  bytes 16276 (15.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tap4f6c85ef-0e: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc16:3eff:fe4e:5b9  prefixlen 64  scopeid 0x20<link>
        ether fe:16:3e:4e:05:b9  txqueuelen 500  (Ethernet)
        RX packets 152  bytes 14530 (14.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 127  bytes 16380 (15.9 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

virbr0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
        ether 22:b0:81:e2:54:4f  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

List the kernel namespace

```
# on host 10.224.147.168
$ ip netns list
qrouter-ab22e15f-9d41-4d69-afa8-0b6c6820c296
```

Dig things out from the router namespace

```
$ ip netns exec qrouter-ab22e15f-9d41-4d69-afa8-0b6c6820c296 ip route
default via 10.224.147.1 dev qg-6eff0712-2b 
10.224.147.0/24 dev qg-6eff0712-2b  proto kernel  scope link  src 10.224.147.230 
192.168.124.0/24 dev qr-5c4fee91-c1  proto kernel  scope link  src 192.168.124.1

$ ip netns exec qrouter-ab22e15f-9d41-4d69-afa8-0b6c6820c296 ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
40: qr-5c4fee91-c1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN 
    link/ether fa:16:3e:b7:0b:52 brd ff:ff:ff:ff:ff:ff
    inet 192.168.124.1/24 brd 192.168.124.255 scope global qr-5c4fee91-c1
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:feb7:b52/64 scope link 
       valid_lft forever preferred_lft forever
41: qg-6eff0712-2b: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN 
    link/ether fa:16:3e:c5:b8:4c brd ff:ff:ff:ff:ff:ff
    inet 10.224.147.230/24 brd 10.224.147.255 scope global qg-6eff0712-2b
       valid_lft forever preferred_lft forever
    inet 10.224.147.234/32 brd 10.224.147.234 scope global qg-6eff0712-2b
       valid_lft forever preferred_lft forever
    inet 10.224.147.235/32 brd 10.224.147.235 scope global qg-6eff0712-2b
       valid_lft forever preferred_lft forever
    inet 10.224.147.236/32 brd 10.224.147.236 scope global qg-6eff0712-2b
       valid_lft forever preferred_lft forever
    inet6 fe80::f816:3eff:fec5:b84c/64 scope link 
       valid_lft forever preferred_lft forever

$ ip netns exec qrouter-ab22e15f-9d41-4d69-afa8-0b6c6820c296 ip li
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
40: qr-5c4fee91-c1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT 
    link/ether fa:16:3e:b7:0b:52 brd ff:ff:ff:ff:ff:ff
41: qg-6eff0712-2b: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT 
    link/ether fa:16:3e:c5:b8:4c brd ff:ff:ff:ff:ff:ff
```

On each VM instance, ping each other with fixed ip (192.168.124.*) - OK

On each VM instance, `ipconfig` shows their ip addresses - OK

On each VM instance, `ip route` shows gateway 192.168.124.1 dev eth0 - OK. 

On each VM instance, `ping 169.254.169.254` to test metadata service - FAIL. Troubleshoot when I have time.

The port for floating ip is always `DOWN`. This is normal, according to this [bug](https://bugs.launchpad.net/neutron/+bug/1196851).

The VM cannot ping outside using floating ip. I guess this is because my controller and compute nodes are actually VMs running on another openstack, whose neutron blocks differnt ip from one port. And they runs on a vlan network. My ext-net is just flat.

Now I use demo-instace1 to ping demo-instance2. You can `ifconfig` and `ovs-vsctl show`. `qvo11d4dec5-44` can be seen in both of them, and has the id `11d4dec5` corresponding to port uuid in openstack.

```
# on host openstack-03
$ tcpdump -i qvo11d4dec5-44 -vvv -nnn
tcpdump: WARNING: qvo11d4dec5-44: no IPv4 address assigned
tcpdump: listening on qvo11d4dec5-44, link-type EN10MB (Ethernet), capture size 65535 bytes
13:24:02.964584 IP (tos 0x0, ttl 64, id 1615, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.124.2 > 192.168.124.4: ICMP echo request, id 26881, seq 241, length 64
13:24:02.965594 IP (tos 0x0, ttl 64, id 26241, offset 0, flags [none], proto ICMP (1), length 84)
    192.168.124.4 > 192.168.124.2: ICMP echo reply, id 26881, seq 241, length 64
13:24:03.965155 IP (tos 0x0, ttl 64, id 1616, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.124.2 > 192.168.124.4: ICMP echo request, id 26881, seq 242, length 64

# on host openstack-02
$ tcpdump -i qvoeca4315f-38 -vvv -nnn
tcpdump: WARNING: qvoeca4315f-38: no IPv4 address assigned
tcpdump: listening on qvoeca4315f-38, link-type EN10MB (Ethernet), capture size 65535 bytes
13:28:23.097584 IP (tos 0x0, ttl 64, id 1875, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.124.2 > 192.168.124.4: ICMP echo request, id 26881, seq 501, length 64
13:28:23.098160 IP (tos 0x0, ttl 64, id 26501, offset 0, flags [none], proto ICMP (1), length 84)
    192.168.124.4 > 192.168.124.2: ICMP echo reply, id 26881, seq 501, length 64
13:28:24.098034 IP (tos 0x0, ttl 64, id 1876, offset 0, flags [DF], proto ICMP (1), length 84)
    192.168.124.2 > 192.168.124.4: ICMP echo request, id 26881, seq 502, length 64
```

Essentially, neutron works like nova-network, but the linux bridge here is replace by openvswitch. iptables and route table are used to implement packet flow.

## Distrubuted Virtual Router (DVR)

[DVR](https://wiki.openstack.org/wiki/Neutron/DVR/HowTo) is an attractive feature. Wait to try when I have time.

## Load Balancer as s Service (LBaaS)

```
$ neutron lb-pool-create --lb-method ROUND_ROBIN --name lb_pool --protocol HTTP --subnet-id demo-subnet
Created a new pool:
+------------------------+--------------------------------------+
| Field                  | Value                                |
+------------------------+--------------------------------------+
| admin_state_up         | True                                 |
| description            |                                      |
| health_monitors        |                                      |
| health_monitors_status |                                      |
| id                     | 551f9962-1d69-4aef-be30-9ddc4254e4f3 |
| lb_method              | ROUND_ROBIN                          |
| members                |                                      |
| name                   | lb_pool                              |
| protocol               | HTTP                                 |
| provider               | haproxy                              |
| status                 | PENDING_CREATE                       |
| status_description     |                                      |
| subnet_id              | 7b48f2da-62df-4a27-b2f8-f84cb8e13921 |
| tenant_id              | c48611d23b754e909753d7ec2428819a     |
| vip_id                 |                                      |
+------------------------+--------------------------------------+
$ neutron lb-member-create --address 192.168.124.2 --protocol-port 80 lb_pool
Created a new member:
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| address            | 192.168.124.2                        |
| admin_state_up     | True                                 |
| id                 | 4425af29-078b-4f0d-a3a1-fe0a05f30098 |
| pool_id            | 551f9962-1d69-4aef-be30-9ddc4254e4f3 |
| protocol_port      | 80                                   |
| status             | PENDING_CREATE                       |
| status_description |                                      |
| tenant_id          | c48611d23b754e909753d7ec2428819a     |
| weight             | 1                                    |
+--------------------+--------------------------------------+
$ neutron lb-member-create --address 192.168.124.4 --protocol-port 80 lb_pool
Created a new member:
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| address            | 192.168.124.4                        |
| admin_state_up     | True                                 |
| id                 | 0f8edcd7-c344-47e7-a134-7cb9a3a15c1b |
| pool_id            | 551f9962-1d69-4aef-be30-9ddc4254e4f3 |
| protocol_port      | 80                                   |
| status             | PENDING_CREATE                       |
| status_description |                                      |
| tenant_id          | c48611d23b754e909753d7ec2428819a     |
| weight             | 1                                    |
+--------------------+--------------------------------------+
$ neutron lb-member-create --address 192.168.124.5 --protocol-port 80 lb_pool
Created a new member:
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| address            | 192.168.124.5                        |
| admin_state_up     | True                                 |
| id                 | 7bf3e8af-ebfe-442c-a717-274687234e6b |
| pool_id            | 551f9962-1d69-4aef-be30-9ddc4254e4f3 |
| protocol_port      | 80                                   |
| status             | PENDING_CREATE                       |
| status_description |                                      |
| tenant_id          | c48611d23b754e909753d7ec2428819a     |
| weight             | 1                                    |
+--------------------+--------------------------------------+
$ neutron lb-pool-show 551f9962-1d69-4aef-be30-9ddc4254e4f3
+------------------------+--------------------------------------+
| Field                  | Value                                |
+------------------------+--------------------------------------+
| admin_state_up         | True                                 |
| description            |                                      |
| health_monitors        |                                      |
| health_monitors_status |                                      |
| id                     | 551f9962-1d69-4aef-be30-9ddc4254e4f3 |
| lb_method              | ROUND_ROBIN                          |
| members                | 0f8edcd7-c344-47e7-a134-7cb9a3a15c1b |
|                        | 4425af29-078b-4f0d-a3a1-fe0a05f30098 |
|                        | 7bf3e8af-ebfe-442c-a717-274687234e6b |
| name                   | lb_pool                              |
| protocol               | HTTP                                 |
| provider               | haproxy                              |
| status                 | ACTIVE                               |
| status_description     |                                      |
| subnet_id              | 7b48f2da-62df-4a27-b2f8-f84cb8e13921 |
| tenant_id              | c48611d23b754e909753d7ec2428819a     |
| vip_id                 |                                      |
+------------------------+--------------------------------------+
$ neutron lb-healthmonitor-create --delay 3 --type HTTP --max-retries 3 --timeout 3
Created a new health_monitor:
+----------------+--------------------------------------+
| Field          | Value                                |
+----------------+--------------------------------------+
| admin_state_up | True                                 |
| delay          | 3                                    |
| expected_codes | 200                                  |
| http_method    | GET                                  |
| id             | 496db106-ccdc-4d9e-b5a2-3c9ecee7049b |
| max_retries    | 3                                    |
| pools          |                                      |
| tenant_id      | c48611d23b754e909753d7ec2428819a     |
| timeout        | 3                                    |
| type           | HTTP                                 |
| url_path       | /                                    |
+----------------+--------------------------------------+
$ neutron lb-healthmonitor-associate 496db106-ccdc-4d9e-b5a2-3c9ecee7049b lb_pool
Associated health monitor 496db106-ccdc-4d9e-b5a2-3c9ecee7049b
$ neutron lb-vip-create --name vip1 --protocol-port 80 --protocol HTTP --subnet-id demo-subnet lb_pool
Created a new vip:
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| address             | 192.168.124.6                        |
| admin_state_up      | True                                 |
| connection_limit    | -1                                   |
| description         |                                      |
| id                  | c95cd95d-f3e4-444d-98e6-3617cab3294f |
| name                | vip1                                 |
| pool_id             | 551f9962-1d69-4aef-be30-9ddc4254e4f3 |
| port_id             | 3bb0ebe2-7a14-48a0-af96-526a860ce697 |
| protocol            | HTTP                                 |
| protocol_port       | 80                                   |
| session_persistence |                                      |
| status              | PENDING_CREATE                       |
| status_description  |                                      |
| subnet_id           | 7b48f2da-62df-4a27-b2f8-f84cb8e13921 |
| tenant_id           | c48611d23b754e909753d7ec2428819a     |
+---------------------+--------------------------------------+
```

Found the create haproxy at openstack-03. `551f9962-1d69-4aef-be30-9ddc4254e4f3` is the id of `lb-pool`.

```
# on host openstack-03, 10.224.147.168
$ ps -ef|grep haproxy
nobody   12052     1  0 14:00 ?        00:00:00 haproxy -f /var/lib/neutron/lbaas/551f9962-1d69-4aef-be30-9ddc4254e4f3/conf -p /var/lib/neutron/lbaas/551f9962-1d69-4aef-be30-9ddc4254e4f3/pid

$ cat /var/lib/neutron/lbaas/551f9962-1d69-4aef-be30-9ddc4254e4f3/con
global
        daemon
        user nobody
        group haproxy
        log /dev/log local0
        log /dev/log local1 notice
        stats socket /var/lib/neutron/lbaas/551f9962-1d69-4aef-be30-9ddc4254e4f3/sock mode 0666 level user
defaults
        log global
        retries 3
        option redispatch
        timeout connect 5000
        timeout client 50000
        timeout server 50000
frontend c95cd95d-f3e4-444d-98e6-3617cab3294f
        option tcplog
        bind 192.168.124.6:80
        mode http
        default_backend 551f9962-1d69-4aef-be30-9ddc4254e4f3
        option forwardfor
backend 551f9962-1d69-4aef-be30-9ddc4254e4f3
        mode http
        balance roundrobin
        option forwardfor
        timeout check 3s
        option httpchk GET /
        http-check expect rstatus 200
        server 0f8edcd7-c344-47e7-a134-7cb9a3a15c1b 192.168.124.4:80 weight 1 check inter 3s fall 3
        server 4425af29-078b-4f0d-a3a1-fe0a05f30098 192.168.124.2:80 weight 1 check inter 3s fall 3
        server 7bf3e8af-ebfe-442c-a717-274687234e6b 192.168.124.5:80 weight 1 check inter 3s fall 3
```

On each VM start a fake http server

```
while true; do echo -e 'HTTP/1.0 200 OK\r\n\r\n<servername>' | sudo nc -l -p 80 ; done 
```

Start a new VM on demo-subnet to test lbaas

```
$ nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64_swift --nic net-id=02320589-b038-493a-9106-c9c2c3ebdb42 --security-group default lb-tester
$ nova show lb-tester
+--------------------------------------+------------------------------------------------------------------+
| Property                             | Value                                                            |
+--------------------------------------+------------------------------------------------------------------+
| OS-DCF:diskConfig                    | AUTO                                                             |
| OS-EXT-AZ:availability_zone          | nova                                                             |
| OS-EXT-SRV-ATTR:host                 | openstack-04.novalocal                                           |
| OS-EXT-SRV-ATTR:hypervisor_hostname  | openstack-04.novalocal                                           |
| OS-EXT-SRV-ATTR:instance_name        | instance-0000003a                                                |
| OS-EXT-STS:power_state               | 1                                                                |
| OS-EXT-STS:task_state                | -                                                                |
| OS-EXT-STS:vm_state                  | active                                                           |
| OS-SRV-USG:launched_at               | 2014-12-15T14:10:06.000000                                       |
| OS-SRV-USG:terminated_at             | -                                                                |
| accessIPv4                           |                                                                  |
| accessIPv6                           |                                                                  |
| config_drive                         |                                                                  |
| created                              | 2014-12-15T14:09:26Z                                             |
| demo-net network                     | 192.168.124.7                                                    |
| flavor                               | m1.tiny (1)                                                      |
| hostId                               | 777a91173e7d8a0f2b13e39727e64ec21c7035f679d0934f979617a6         |
| id                                   | f8295910-5b2f-437c-a1c2-8addfad2de07                             |
| image                                | cirros-0.3.3-x86_64_swift (383de0c9-420d-4a03-b1c9-499bd8e681c7) |
| key_name                             | -                                                                |
| metadata                             | {}                                                               |
| name                                 | lb-tester                                                        |
| os-extended-volumes:volumes_attached | []                                                               |
| progress                             | 0                                                                |
| security_groups                      | default                                                          |
| status                               | ACTIVE                                                           |
| tenant_id                            | c48611d23b754e909753d7ec2428819a                                 |
| updated                              | 2014-12-15T14:10:06Z                                             |
| user_id                              | 6094daee26d9463e8b37e87dc8d8b33d                                 |
+--------------------------------------+------------------------------------------------------------------+
```

Show what vip we have

```
$ neutron lb-vip-list
+--------------------------------------+------+---------------+----------+----------------+--------+
| id                                   | name | address       | protocol | admin_state_up | status |
+--------------------------------------+------+---------------+----------+----------------+--------+
| c95cd95d-f3e4-444d-98e6-3617cab3294f | vip1 | 192.168.124.6 | HTTP     | True           | ACTIVE |
+--------------------------------------+------+---------------+----------+----------------+--------+
```

On lb-tester, access vip1

```
# on VM lb-tester
wget -O - http://192.168.124.6
```

I can see response on each of the demo-instance1 to 3

```
HOST: 192.168.124.6
User-Agent: Wget
Connection: Close
X-Forwarded-For: 192.168.124.7
```

On lb-tester (192.168.124.7), the result

```
$ wget -O - http://192.168.124.6
Connecting to 192.168.124.6 (192.168.124.6:80)
            0 - stalled -demo-instance3
         100% |====================================|   15   0:00:00 ETA
$ wget -O - http://192.168.124.6
Connecting to 192.168.124.6 (192.168.124.6:80)
            0 - stalled -demo-instance1
         100% |====================================|   15   0:00:00 ETA
$ wget -O - http://192.168.124.6
Connecting to 192.168.124.6 (192.168.124.6:80)
            0 - stalled -demo-instance2
         100% |====================================|   15   0:00:00 ETA
```

## Troubleshooting

Good troubleshooting needs familiarity of technologies which neutron relies on, and neutron workflow. Ignore no abnormalities like a detective.

A tip in netron troubleshooting is always pay attention to port. Is port not created? Is port created physically? Is port down?

### Nova boot failed: vif_type=binding_failed

Nova boot instance. The instance failed with `virf_type=binding_failed`. The instance was boot on compute node openstack-03.novalocal.

First, check whether port in br-int is created. The result is no.

```
$ ovs-vsctl show
2e68b536-3378-4717-9088-9ba1d96dbf68
    Bridge br-tun
        Port br-tun
            Interface br-tun
                type: internal
        Port "vxlan-0ae093a6"
            Interface "vxlan-0ae093a6"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="10.224.147.168", out_key=flow, remote_ip="10.224.147.166"}
        Port patch-int
            Interface patch-int
                type: patch
                options: {peer=patch-tun}
        Port "vxlan-0ae093a7"
            Interface "vxlan-0ae093a7"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="10.224.147.168", out_key=flow, remote_ip="10.224.147.167"}
        Port "vxlan-0ae093ad"
            Interface "vxlan-0ae093ad"
                type: vxlan
                options: {df_default="true", in_key=flow, local_ip="10.224.147.168", out_key=flow, remote_ip="10.224.147.173"}
    Bridge br-int
        fail_mode: secure
        Port int-br-ex
            Interface int-br-ex
                type: patch
                options: {peer=phy-br-ex}
        Port br-int
            Interface br-int
                type: internal
        Port patch-tun
            Interface patch-tun
                type: patch
                options: {peer=patch-int}
    Bridge br-ex
        Port br-ex
            Interface br-ex
                type: internal
        Port "eth2"
            Interface "eth2"
        Port phy-br-ex
            Interface phy-br-ex
                type: patch
                options: {peer=int-br-ex}
    ovs_version: "2.1.3"
```

After that, on horizon, I can see the port of the new instance is creatd (in db), but status down. You can also see it by neutron client. The `device_id` is uuid of the VM bind to it.

```
$ neutron port-show --ID d7a198bc-0dfc-4bf8-9b83-ce338d740622
+-----------------------+---------------------------------------------------------------------------------------+
| Field                 | Value                                                                                 |
+-----------------------+---------------------------------------------------------------------------------------+
| admin_state_up        | True                                                                                  |
| allowed_address_pairs |                                                                                       |
| binding:host_id       | openstack-03.novalocal                                                                |
| binding:profile       | {}                                                                                    |
| binding:vif_details   | {}                                                                                    |
| binding:vif_type      | binding_failed                                                                        |
| binding:vnic_type     | normal                                                                                |
| device_id             | d71399f6-5b56-41ce-8aa2-5a02b487dba7                                                  |
| device_owner          | compute:nova                                                                          |
| extra_dhcp_opts       |                                                                                       |
| fixed_ips             | {"subnet_id": "239b2216-0006-4a96-8a41-27e405a05018", "ip_address": "192.168.124.29"} |
| id                    | d7a198bc-0dfc-4bf8-9b83-ce338d740622                                                  |
| mac_address           | fa:16:3e:d3:71:c6                                                                     |
| name                  |                                                                                       |
| network_id            | eaf3a591-fb39-433c-b01a-f74aaa814405                                                  |
| security_groups       | 0b04a0d6-1796-4881-b7f1-b859675148f4                                                  |
| status                | DOWN                                                                                  |
| tenant_id             | c48611d23b754e909753d7ec2428819a                                                      |
+-----------------------+---------------------------------------------------------------------------------------+
```

On either side of neutron-server and neutron-openvswitch-agent, log has no error. But later I found that neutron log failed request with `fail`.

```
# show no error
grep -ir ERROR /var/log/neutron

# search with 'fail'
grep -ri fail /var/log/neutron
```

I found that on neutron-openvswitch-agent (host openstack-03.novalocal), openvswitch agent is never invoked. This can be verified from log.

I doubt that it is because that rabbitmq message never reaches neutron-openvswitch-agent. So I started an experiment to intercept messages of rabbitmq. See my post "intercept rabbitmq message in openstack". 

The result seems like, both side of neutron has no problem connecting to rabbitmq. Exchanges and queues are created. But somehow the message to invoke neutron-openvswitch-agent is never sent.

```
# with instance being created
$ python intercept_rabbit.py

----------------16th message -----------------

 routing_key: 'dhcp_agent.openstack-02.novalocal'
{
    "oslo.message": {
        "_context_auth_token": "90034361b7c44f938fbdd59666b7d86a", 
        "_context_is_admin": true, 
        "_context_project_id": "c1eec4d4365f41d8b1fe47e71da00956", 
        "_context_project_name": "service", 
        "_context_read_deleted": "no", 
        "_context_request_id": "req-8c8442e4-d79a-4162-862c-87e8936114f2", 
        "_context_roles": [
            "admin"
        ], 
        "_context_tenant": "c1eec4d4365f41d8b1fe47e71da00956", 
        "_context_tenant_id": "c1eec4d4365f41d8b1fe47e71da00956", 
        "_context_tenant_name": "service", 
        "_context_timestamp": "2014-12-14 11:22:49.629200", 
        "_context_user": "724b2c99c6e54742b2d656ab7d76fa98", 
        "_context_user_id": "724b2c99c6e54742b2d656ab7d76fa98", 
        "_context_user_name": "neutron", 
        "_unique_id": "96f37927aca64b0483354fd93ce67f84", 
        "args": {
            "payload": {
                "port": {
                    "admin_state_up": true, 
                    "allowed_address_pairs": [], 
                    "binding:host_id": "openstack-03.novalocal", 
                    "binding:profile": {}, 
                    "binding:vif_details": {}, 
                    "binding:vif_type": "binding_failed", 
                    "binding:vnic_type": "normal", 
                    "device_id": "46f979f8-be01-4342-8b62-a358ab961c03", 
                    "device_owner": "compute:nova", 
                    "extra_dhcp_opts": [], 
                    "fixed_ips": [
                        {
                            "ip_address": "192.168.124.30", 
                            "subnet_id": "239b2216-0006-4a96-8a41-27e405a05018"
                        }
                    ], 
                    "id": "df1b289c-5f6f-4fa0-8637-55f1b60969c2", 
                    "mac_address": "fa:16:3e:eb:ec:2a", 
                    "name": "", 
                    "network_id": "eaf3a591-fb39-433c-b01a-f74aaa814405", 
                    "security_groups": [
                        "0b04a0d6-1796-4881-b7f1-b859675148f4"
                    ], 
                    "status": "DOWN", 
                    "tenant_id": "c48611d23b754e909753d7ec2428819a"
                }
            }
        }, 
        "method": "port_create_end", 
        "version": "1.0"
    }, 
    "oslo.version": "2.0"
}

----------------26th message -----------------

 routing_key: 'dhcp_agent.openstack-02.novalocal'
{
    "oslo.message": {
        "_context_auth_token": "58baf1775c4a45de93422046da29d305", 
        "_context_is_admin": true, 
        "_context_project_id": "c48611d23b754e909753d7ec2428819a", 
        "_context_project_name": "admin", 
        "_context_read_deleted": "no", 
        "_context_request_id": "req-f1663a70-3a64-4e0c-b87f-2a4a5a563ab1", 
        "_context_roles": [
            "admin"
        ], 
        "_context_tenant": "c48611d23b754e909753d7ec2428819a", 
        "_context_tenant_id": "c48611d23b754e909753d7ec2428819a", 
        "_context_tenant_name": "admin", 
        "_context_timestamp": "2014-12-14 11:23:20.800571", 
        "_context_user": "6094daee26d9463e8b37e87dc8d8b33d", 
        "_context_user_id": "6094daee26d9463e8b37e87dc8d8b33d", 
        "_context_user_name": "admin", 
        "_unique_id": "e7588d16fdbf407e8e20b31b5aa94728", 
        "args": {
            "payload": {
                "port_id": "df1b289c-5f6f-4fa0-8637-55f1b60969c2"
            }
        }, 
        "method": "port_delete_end", 
        "version": "1.0"
    }, 
    "oslo.version": "2.0"
}

----------------29th message -----------------

 routing_key: 'q-plugin'
{
    "oslo.message": {
        "_context_auth_token": null, 
        "_context_is_admin": true, 
        "_context_project_id": null, 
        "_context_project_name": null, 
        "_context_read_deleted": "no", 
        "_context_request_id": "req-a78b88df-bde6-48ee-89c7-d28b5f14c51a", 
        "_context_roles": [
            "admin"
        ], 
        "_context_tenant": null, 
        "_context_tenant_id": null, 
        "_context_tenant_name": null, 
        "_context_timestamp": "2014-12-02 17:10:20.018646", 
        "_context_user": null, 
        "_context_user_id": null, 
        "_context_user_name": null, 
        "_msg_id": "57954eea529347dcbb4061438bead661", 
        "_reply_q": "reply_7d304be0842a48c8b51268f7ec41b02f", 
        "_unique_id": "b94048931a7b4ee38d03e9322cd5b79d", 
        "args": {
            "host": "openstack-02.novalocal"
        }, 
        "method": "get_active_networks_info", 
        "version": "1.1"
    }, 
    "oslo.version": "2.0"
}
```

The 'binding_failed' comes from `portbindings.VIF_TYPE_BINDING_FAILED` in neutorn code. By grep `vif_type.*VIF_TYPE_BINDING_FAILED`, I found there is only one place assigned `VIF_TYPE_BINDING_FAILED` to vif_type.

```
neutron/plugins/ml2/managers.py::bind_port()
  597                                  "bind_port"),
  598                                driver.name)
  599:         binding.vif_type = portbindings.VIF_TYPE_BINDING_FAILED
  600          LOG.warning(_("Failed to bind port %(port)s on host %(host)s"),
  601                      {'port': context._port['id'],
```

PDB tracing shows the invocation flow. Neturon uses a different way to handle plugins and extensions from nova

```
(Pdb) where
  /usr/lib/python2.7/site-packages/eventlet/greenpool.py(80)_spawn_n_impl()
-> func(*args, **kwargs)
  /usr/lib/python2.7/site-packages/eventlet/wsgi.py(594)process_request()
-> proto.__init__(sock, address, self)
  /usr/lib64/python2.7/SocketServer.py(649)__init__()
-> self.handle()
  /usr/lib64/python2.7/BaseHTTPServer.py(340)handle()
-> self.handle_one_request()
  /usr/lib/python2.7/site-packages/eventlet/wsgi.py(285)handle_one_request()
-> self.handle_one_response()
  /usr/lib/python2.7/site-packages/eventlet/wsgi.py(389)handle_one_response()
-> result = self.application(self.environ, start_response)
  /usr/lib/python2.7/site-packages/paste/urlmap.py(203)__call__()
-> return app(environ, start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(130)__call__()
-> resp = self.call_func(req, *args, **self.kwargs)
  /usr/lib/python2.7/site-packages/webob/dec.py(195)call_func()
-> return self.func(req, *args, **kwargs)
  /usr/lib/python2.7/site-packages/neutron/openstack/common/middleware/request_id.py(38)__call__()
-> response = req.get_response(self.application)
  /usr/lib/python2.7/site-packages/webob/request.py(1320)send()
-> application, catch_exc_info=False)
  /usr/lib/python2.7/site-packages/webob/request.py(1284)call_application()
-> app_iter = application(self.environ, start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(130)__call__()
-> resp = self.call_func(req, *args, **self.kwargs)
  /usr/lib/python2.7/site-packages/webob/dec.py(195)call_func()
-> return self.func(req, *args, **kwargs)
  /usr/lib/python2.7/site-packages/neutron/openstack/common/middleware/catch_errors.py(38)__call__()
-> response = req.get_response(self.application)
  /usr/lib/python2.7/site-packages/webob/request.py(1320)send()
-> application, catch_exc_info=False)
  /usr/lib/python2.7/site-packages/webob/request.py(1284)call_application()
-> app_iter = application(self.environ, start_response)
  /usr/lib/python2.7/site-packages/keystonemiddleware/auth_token.py(750)__call__()
-> return self._call_app(env, start_response)
  /usr/lib/python2.7/site-packages/keystonemiddleware/auth_token.py(684)_call_app()
-> return self._app(env, _fake_start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(144)__call__()
-> return resp(environ, start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(144)__call__()
-> return resp(environ, start_response)
  /usr/lib/python2.7/site-packages/routes/middleware.py(131)__call__()
-> response = self.app(environ, start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(144)__call__()
-> return resp(environ, start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(144)__call__()
-> return resp(environ, start_response)
  /usr/lib/python2.7/site-packages/routes/middleware.py(131)__call__()
-> response = self.app(environ, start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(144)__call__()
-> return resp(environ, start_response)
  /usr/lib/python2.7/site-packages/webob/dec.py(130)__call__()
-> resp = self.call_func(req, *args, **self.kwargs)
  /usr/lib/python2.7/site-packages/webob/dec.py(195)call_func()
-> return self.func(req, *args, **kwargs)
  /usr/lib/python2.7/site-packages/neutron/api/v2/resource.py(87)resource()
-> result = method(request=request, **args)
  /usr/lib/python2.7/site-packages/neutron/api/v2/base.py(448)create()
-> obj = obj_creator(request.context, **kwargs)
  /usr/lib/python2.7/site-packages/neutron/plugins/ml2/plugin.py(815)create_port()
-> bound_context = self._bind_port_if_needed(mech_context)
  /usr/lib/python2.7/site-packages/neutron/plugins/ml2/plugin.py(273)_bind_port_if_needed()
-> bind_context = self._bind_port(context)
  /usr/lib/python2.7/site-packages/neutron/plugins/ml2/plugin.py(311)_bind_port()
-> self.mechanism_manager.bind_port(new_context)
> /usr/lib/python2.7/site-packages/neutron/plugins/ml2/managers.py(600)bind_port()
-> binding.vif_type = portbindings.VIF_TYPE_BINDING_FAILED
```

Combined with the log messages, I found that `self.ordered_mech_drivers` is empty. Mechanism drivers, such as openvswitch, is never invoked, in `bind_port()`

Further code dive found out that, `cfg.CONF.ml2.mechanism_drivers` is empty, too. WHAT? neutron-server never loaded my config files! It seems neutron-server needs explicitly specify config files. This is different from nova. Gosh it tooks me totally 2 weeks to find out, to find the right place that goes wrong.

```
# never use
#neutron-server

# specify conifg files for neutron-server
neutron-server --config-file /etc/neutron/plugins/ml2/ml2_conf.ini --config-file /etc/neutron/neutron.conf
```

__The fix is merged into prior setup steps.__ To fully fix this, you need to remove all VMs, networks (including the external network) and routers completely, and create them from the begining.

I'm curious how the workflow of port binding. Read the code now. The neutron-server doesn't send rpc call to neutron-openvswitch-agent, it just write states into db. 

```
ml2/managers.py::bind_port()
   LOG.debug("Attempting to bind port %(port)s on host %(host)s ", ...) # find this in neutron/server.log
```

neutron-openvswitch-agent loops on polling db, you can see in log the `Agent rpc_loop - iteration:7`

```
2014-12-14 12:27:05.512 13303 DEBUG neutron.plugins.openvswitch.agent.ovs_neutron_agent [req-6193f867-adeb-4a7c-8485-a5bcdfd76e89 None] Agent rpc_loop - iteration:7 started rpc_loop /usr/lib/python2.7/site-packages/neutron/plugins/openvswitch/agent/ovs_neutron_agent.py:1353
...
2014-12-14 08:54:20.672 22218 DEBUG neutron.plugins.openvswitch.agent.ovs_neutron_agent [req-04ed31b6-56df-4536-98ba-1d5504122ed3 None] Agent rpc_loop - iteration:7 completed.
```

Once port db state is changed, the invocation follows

```
ovs_neutron_agent.py::rpc_loop()
  self.process_network_ports(..)
    self.treat_devices_added_or_updated(..)
      self.treat_vif_port(..)
         self.port_bound(..)
           self.provision_local_vlan(..)
             self.int_br.add_flow(..)
                ovs_lib.py::add_flow(..)
```

The neutron-openvswitch-agents works by maintaining states rather than executing action.

### Error neutron-rootwrap ip netns exec unauthorized

Error log in /etc/neutron/dhcp-agent.log

```
Command: ['sudo', 'neutron-rootwrap', '/etc/neutron/rootwrap.conf', 'ip', 'netns', 'exec', 'qdhcp-eaf3a591-fb39-433c-b01a-f74aaa814405', 'dhcp_release', 'tap5291baff-f2', '192.168.124.44', 'fa:16:3e:f0:
d4:c5']
Exit code: 99
Stdout: ''
Stderr: '/usr/bin/neutron-rootwrap: Unauthorized command: ip netns exec qdhcp-eaf3a591-fb39-433c-b01a-f74aaa814405 dhcp_release tap5291baff-f2 192.168.124.44 fa:16:3e:f0:d4:c5 (no filter matched)\n'
2014-12-14 13:50:52.253 19412 ERROR neutron.agent.dhcp_agent [req-34611eff-f8dc-4562-8993-865c842fb515 None] Unable to reload_allocations dhcp for eaf3a591-fb39-433c-b01a-f74aaa814405.
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent Traceback (most recent call last):
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent   File "/usr/lib/python2.7/site-packages/neutron/agent/dhcp_agent.py", line 129, in call_driver
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent     getattr(driver, action)(**action_kwargs)
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent   File "/usr/lib/python2.7/site-packages/neutron/agent/linux/dhcp.py", line 438, in reload_allocations
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent     self._release_unused_leases()
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent   File "/usr/lib/python2.7/site-packages/neutron/agent/linux/dhcp.py", line 542, in _release_unused_leases
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent     self._release_lease(mac, ip)
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent   File "/usr/lib/python2.7/site-packages/neutron/agent/linux/dhcp.py", line 426, in _release_lease
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent     ip_wrapper.netns.execute(cmd)
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent   File "/usr/lib/python2.7/site-packages/neutron/agent/linux/ip_lib.py", line 550, in execute
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent     check_exit_code=check_exit_code, extra_ok_codes=extra_ok_codes)
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent   File "/usr/lib/python2.7/site-packages/neutron/agent/linux/utils.py", line 84, in execute
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent     raise RuntimeError(m)
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent RuntimeError: 
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent Command: ['sudo', 'neutron-rootwrap', '/etc/neutron/rootwrap.conf', 'ip', 'netns', 'exec', 'qdhcp-eaf3a591-fb39-433c-b01a-f74aaa814405', 'dhcp_release', 'tap5291baff-f2', '192.168.124.44', 'fa:16:3e:f0:d4:c5']
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent Exit code: 99
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent Stdout: ''
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent Stderr: '/usr/bin/neutron-rootwrap: Unauthorized command: ip netns exec qdhcp-eaf3a591-fb39-433c-b01a-f74aaa814405 dhcp_release tap5291baff-f2 192.168.124.44 fa:16:3e:f0:d4:c5 (no filter matched)\n'
2014-12-14 13:50:52.253 19412 TRACE neutron.agent.dhcp_agent 
2014-12-14 13:50:52.254 19412 DEBUG neutron.openstack.common.lockutils [req-34611eff-f8dc-4562-8993-865c842fb515 None] Semaphore / lock released "port_delete_end" inner /usr/lib/python2.7/site-packages/neutron/openstack/common/lockutils.py:252
2014-12-14 13:50:55.480 19412 DEBUG neutron
```

The command that raise error

```
$ su neutron
$ sudo neutron-rootwrap /etc/neutron/rootwrap.conf ip netns exec qdhcp-eaf3a591-fb39-433c-b01a-f74aaa814405 dhcp_release tap5291baff-f
2 192.168.124.44 fa:16:3e:f0:d4:c5
Unauthorized command: ...
```

The error doesn't appear again, after I set neutron user to be /sbin/nologin in /etc/passwd, on the host where dhcp-agent reports error.

### Remember to remove all the pdb.set_trace()

Remember to remove all the pdb.set_trace() after debugging. Otherwise after start service as daemon, things may go wrong unexpectedly.

## Other References

  * [Diving into OpenStack Network Architecture](https://blogs.oracle.com/ronen/entry/diving_into_openstack_network_architecture)
  * [Launching a Nova instance results in "NovaException: Unexpected vif_type=binding_failed"](https://www.redhat.com/archives/rdo-list/2014-May/msg00079.html)
  * [Identifying and Troubleshooting Neutron Namespaces](https://www.mirantis.com/blog/identifying-and-troubleshooting-neutron-namespaces/)
  * [Reference Architectures](http://docs.mirantis.com/fuel/fuel-3.2.1/reference-architecture.html)
  * [Neutron Network Namespaces and IPtables--A Technical Deep Dive](http://www.slideshare.net/mirantis/hk-openstack-namespaces1)
