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

Provider network example in lab

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




