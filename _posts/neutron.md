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

