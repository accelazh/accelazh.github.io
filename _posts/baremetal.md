1. pxe启动
   image由glance管，需要自己build，pxe格式
   开关机(power management)由IPMI做
   网络，vxlan由出口交换机做；中心式virtual router接上即可；DVR不支持
   存储volume？
        cinder boot from volume + ironic: https://blueprints.launchpad.net/ironic/+spec/cinder-integration -> not finished
        "we don't have baremetal Cinder": http://osdir.com/ml/openstack-dev/2014-11/msg00623.html
        attach volume to baremetal: https://blueprints.launchpad.net/nova/+spec/attach-volume-on-nova-bare-metal -> still drafting    
   ceilometer监测？
        discussion: https://bugs.launchpad.net/nova/+bug/1188218
        
        IPMI data to ceilometer (implemented): https://blueprints.launchpad.net/ironic/+spec/send-data-to-ceilometer
            "Adds periodic task to conductor which emits notification to Ceilometer by an interval." -> no agent on baremetal node. an periodic task on ironic-conductor, collect data via IPMI and emit to Ceilometer.
        
        Monitoring Physical Devices (implemented): https://blueprints.launchpad.net/ceilometer/+spec/monitoring-physical-devices
            "There is a new Ceilometer agent needed to achieve this. This agent should run on every physical OpenStack server" -> need agent. but this aims to collect physical Openstack nodes such as Glance, Cinder, Swift, ...

1.5. ironic & baremetal关系？
   最开始baremetal是在nova里做的，后来成为独立组件ironic

2. For agent: "Baremetal (and Ironic) instances do not, by definition, necessarily have an agent"
   https://bugs.launchpad.net/nova/+bug/1188218

3. for cobbler and pxe
    cobbler arch: https://www.redhat.com/archives/spacewalk-devel/2009-February/001446.html
    cobbler wiki: http://en.wikipedia.org/wiki/Cobbler_%28software%29
    ibm's: http://www.ibm.com/developerworks/library/l-cobbler/

    pxe, dhcp, tftp is enough to baremetal boot. cobbler is a management tool.

> Cobbler sets up a PXE boot environment (it also supports PowerPC by using yaboot) and controls all aspects that are related to installation, such as network boot services (DHCP and TFTP) and repository mirroring

4. official architecture
   http://docs.openstack.org/developer/ironic/deploy/user-guide.html

----------
mirantis: baremetal architecture (before ironic)
https://www.mirantis.com/blog/bare-metal-provisioning-with-openstack-cloud/
mirantis: baremetal switches (before ironic
https://www.mirantis.com/blog/configuring-baremetal-openstack-cloud/
    switch needs config vlan
mirantis: image preparation for baremetal
https://www.mirantis.com/blog/baremetal-provisioning-part3-images-preparation/
mirantis: placement control and multi-tenancy isolation 
https://www.mirantis.com/blog/baremetal-provisioning-multi-tenancy-placement-control-isolation/
