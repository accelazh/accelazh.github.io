

## Architecture

Cinder provides block storage service for openstack. Ceph, the popular block storage backend, is gaining popularity. Glance can also use Cinder as backend. Cinder consists of 

* Cinder-api
* Cinder-scheduler
* Cinder-volume
* Cinder-backup (api calls to backup/restore a volume)

They communicate by AMQP. Cinder uses the [taskflow](https://wiki.openstack.org/wiki/TaskFlow) framework, which is very interesting, in volume and scheduler components. Architecture picture borrowed from [kenhui](http://cloudarchitectmusings.com/2013/11/18/laying-cinder-block-volumes-in-openstack-part-1-the-basics/).

![Cinder architecture](/images/cinder-architecture.png "Cinder architecture")

Storage backend for Cinder varies, they can be

* Cheap and a decent way, LVM. Cinder LVM has no HA.
* Proprietary solutions like EMC, NetApp and Solidfire. They are expensive.
* Modern distributed storage clusters, e.g. Ceph & Sheepdog. Reliable, scalable and robust.

However, opensource cinder drivers are not that much. Refer to [here](http://www.sebastien-han.fr/blog/2014/06/02/start-considering-ceph-as-a-backend-for-openstack-cinder-replace-lvm/)

> Cinder has 27 storage drivers, and only 4 of them are open source, the rest are proprietary solutions: Ceph RBD, GlusterFS,
NFS, LVM(reference implementation).

Overall, Ceph is basically the best choice of Cinder backend. Not counting the "storage convergence" to unify image backend and block backend, and provide boot from volume and fast boot.

Cinder architecture references

* [Cinder System Architecture](http://docs.openstack.org/developer/cinder/devref/architecture.html)
* [Laying Cinder Block (Volumes) In Openstack, Part 1: The Basics](http://cloudarchitectmusings.com/2013/11/18/laying-cinder-block-volumes-in-openstack-part-1-the-basics/)
* [Laying Cinder Block (Volumes) In OpenStack, Part 2: Solutions Design](http://www.rackspace.com/blog/laying-cinder-block-volumes-in-openstack-part-2-solutions-design/)
* [Start Considering Ceph as a Backend for OpenStack Cinder (to Replace LVM)](http://www.sebastien-han.fr/blog/2014/06/02/start-considering-ceph-as-a-backend-for-openstack-cinder-replace-lvm/)
* [Mirantis reference architectures](http://docs.mirantis.com/fuel/fuel-3.2.1/reference-architecture.html#storage-nodes)

### About ISCSI

To understand iSCSI You can refer to here

* [NAS vs SAN, NFS vs iSCSI, file-based vs block-based](http://www.ecei.com/network-attached-storage.shtml)
* [iSCSI concepts](http://pubs.vmware.com/vsphere-51/index.jsp#com.vmware.vsphere.storage.doc/GUID-2219AF79-339F-4272-812C-5B48290E7DF1.html), [What is LUN](http://en.wikipedia.org/wiki/ISCSI#Logical_unit_number) and [What is IQN](http://pubs.vmware.com/vsphere-4-esxi-installable-vcenter/index.jsp?topic=/com.vmware.vsphere.esxi_server_config.doc_41/esx_server_config/introduction_to_storage/c_understanding_iscsi_naming_and_addressing.html)
* [Introduction to iSCSI](https://www.iol.unh.edu/sites/default/files/knowledgebase/iscsi/Introduction.ppt)
* [Setup software based iSCSI target - TGT](https://wiki.archlinux.org/index.php/TGT_iSCSI_Target)

To understand how to use LVM on iSCSI. Basically, LVM is used on target server, to create several lvm disks, then provided via iSCSI to initiators (client side / VM side). Also, to set up a software based iSCSI target on Linux

* [TGT iSCSI target arch wiki](https://wiki.archlinux.org/index.php/TGT_iSCSI_Target) and [TGT official site](http://stgt.sourceforge.net/)
* [Create Centralized Secure Storage using iSCSI Target on RHEL/CentOS/Fedora Part -I](http://www.tecmint.com/create-centralized-secure-storage-using-iscsi-targetin-linux/), [Part -II](http://www.tecmint.com/create-luns-using-lvm-in-iscsi-target/)

Note: RHEL 7, Fedora 21 and CentOS 7 now use targetcli (LIO) in place of tgtd.

## Environment

Cinder deployment architecture refer to [mirantis reference architectures](http://docs.mirantis.com/fuel/fuel-3.2.1/reference-architecture.html#storage-nodes). I would like to use LVM as storage backend (instead of ceph) for simplicity. Note that LVM is not HA

> Unlike Swift and Ceph, Cinder LVM doesn't implement data redundancy across nodes: if a Cinder node is lost, volumes stored on that node cannot be recovered from the data stored on other Cinder nodes. If you need your block storage to be resilient, use Ceph for volumes.

I will install cinder based on my prior neutron environment

  * node 1: 10.224.147.166, CentOS 7, hostname openstack-01, the cinder controller node
    * nova-api
    * nova-scheduler
    * nova-novncproxy
    * nova-consoleauth
    * nova-conductor
    * neutron-server
    * glance (with filestore backend)
    * mysql
    * keystone
    * rabbitmq
    * cinder-api
    * cinder-scheduler
  
  * node 2: 10.224.147.167, CentOS 7, hostname openstack-02, the cinder storage node
    * nova-compute
    * neutron-openvswitch-agent 
    * neutron-l3-agent
    * neutron-dhcp-agent
    * neutron-metadata-agent
    * neutron-lbaas-agent
    * cinder-volume

  * node 3: 10.224.147.168, CentOS 7, hostname openstack-03, the cinder storage node
    * nova-compute
    * neutron-openvswitch-agent 
    * neutron-l3-agent
    * neutron-dhcp-agent
    * neutron-metadata-agent
    * neutron-lbaas-agent
    * cinder-volume

  * node 4: 10.224.147.173, CentOS 7, hostname openstack-04, the cinder storage node
    * nova-compute
    * neutron-openvswitch-agent 
    * neutron-l3-agent
    * neutron-dhcp-agent
    * neutron-metadata-agent
    * neutron-lbaas-agent
    * cinder-volume

## Install Cinder

Following [developer guide](http://docs.openstack.org/developer/cinder/devref/development.environment.html#linux-systems) and [installation manual](http://docs.openstack.org/juno/install-guide/install/yum/content/ch_cinder.html). 

Install cinder code on each host.

```
yum install -y python-virtualenv openssl-devel python-pip git gcc libffi-devel libxslt-devel mysql-devel postgresql-devel 
yum install -y lvm2 targetcli
mkdir ~/workspace
cd ~/workspace
git clone https://github.com/openstack/cinder.git
cd cinder
git checkout stable/juno
pip install -r requirements.txt
python setup.py install
cd ~
```

Create user and directories, on each host.

```
useradd -r -s /sbin/nologin cinder
mkdir /var/lib/cinder
mkdir /var/log/cinder
mkdir /etc/cinder
cp -r ~/workspace/cinder/etc/cinder/* /etc/cinder/

chown -R cinder:cinder /var/lib/cinder
chown -R cinder:cinder /var/log/cinder
chown -R cinder:cinder /etc/cinder
chown -R root:root /etc/cinder/rootwrap.d
chown root:root /etc/cinder/rootwrap.conf
chmod -R a+r /etc/cinder/rootwrap.d
chmod a+r /etc/cinder/rootwrap.conf
```

Create the database for cinder. Run on one controller node

```
mysql -uroot -p
> create database cinder;
> exit;
```

Create the keystone user and service for cinder. Run on one controller node

```
keystone user-create --name cinder --pass 123work
keystone user-role-add --user cinder --tenant service --role admin
keystone service-create --name cinder --type volume --description "OpenStack Block Storage"
keystone service-create --name cinderv2 --type volumev2 --description "OpenStack Block Storage"
keystone endpoint-create --service-id $(keystone service-list | awk '/ volume / {print $2}') --publicurl http://10.224.147.166:8776/v1/%\(tenant_id\)s --internalurl http://10.224.147.166:8776/v1/%\(tenant_id\)s --adminurl http://10.224.147.166:8776/v1/%\(tenant_id\)s --region regionOne
keystone endpoint-create --service-id $(keystone service-list | awk '/ volumev2 / {print $2}') --publicurl http://10.224.147.166:8776/v2/%\(tenant_id\)s --internalurl http://10.224.147.166:8776/v2/%\(tenant_id\)s --adminurl http://10.224.147.166:8776/v2/%\(tenant_id\)s --region regionOne
```

## Config Cinder

First, ensure each node can ping each other with hostname. This requires you to modify /etc/hosts to add each node's host name.

Create the config file on each host

```
echo '
[DEFAULT]
verbose = True
debug = True
lock_path = $state_path/lock

rpc_backend = rabbit
rabbit_host=10.224.147.166
rabbit_userid=root
rabbit_password=123work

api_paste_config=/etc/cinder/api-paste.ini

# CHANGE according to host
my_ip=10.224.147.166
# CHANGE according to host
host=openstack-01.novalocal

glance_host=10.224.147.166
auth_strategy = keystone

iscsi_helper=lioadm
volume_group=cinder-volumes
volume_driver=cinder.volume.drivers.lvm.LVMISCSIDriver

[database]

connection=mysql://root:123work@10.224.147.166/cinder

[keystone_authtoken]
auth_uri = http://10.224.147.166:5000/v2.0
identity_uri = http://10.224.147.166:35357
admin_tenant_name = service
admin_user = cinder
admin_password = 123work
' > /etc/cinder/cinder.conf
```

Sync cinder db, run once

```
su -s /bin/sh -c "cinder-manage db sync" cinder
```

On each node, add sudoers for cinder

```
echo 'Defaults:cinder !requiretty

cinder ALL = (root) NOPASSWD: /usr/bin/cinder-rootwrap /etc/cinder/rootwrap.conf *
' > /etc/sudoers.d/cinder
```

On each storage node, create the storage disk for cinder lvm. I use loop device to do it

```
mkdir /srv
dd if=/dev/zero of=/srv/cinder-volumes.img bs=1 count=1 seek=4G
chown cinder:cinder /srv/cinder-volumes.img
losetup /dev/loop1 /srv/cinder-volumes.img
pvcreate /dev/loop1
vgcreate cinder-volumes /dev/loop1

# to prevent problems caused by lvm scanning on /dev
vim /etc/lvm/lvm.conf
devices {
  ...
  # modify this line
  filter = [ "a/loop1/", "r/.*/" ]
}
service lvm2-lvmetad restart
```

### Start Cinder

Let's start cinder services

```
# on controller node
su -s /bin/bash cinder -c '/usr/bin/cinder-api >> /var/log/cinder/api.log 2>&1' &
su -s /bin/bash cinder -c '/usr/bin/cinder-scheduler >> /var/log/cinder/scheduler.log 2>&1' &

# on storage node
service lvm2-lvmetad restart
service target restart
su -s /bin/bash cinder -c '/usr/bin/cinder-volume >> /var/log/cinder/volume.log 2>&1' &
```

### To Verify

```
$ source ~/openstack-admin.rc
$ cinder service-list
+------------------+--------------------------------+------+---------+-------+----------------------------+-----------------+
|      Binary      |              Host              | Zone |  Status | State |         Updated_at         | Disabled Reason |
+------------------+--------------------------------+------+---------+-------+----------------------------+-----------------+
| cinder-scheduler | openstack-01.novalocal | nova | enabled |   up  | 2014-12-23T16:32:00.000000 |       None      |
|  cinder-volume   | openstack-02.novalocal | nova | enabled |   up  | 2014-12-23T16:31:55.000000 |       None      |
|  cinder-volume   | openstack-03.novalocal | nova | enabled |   up  | 2014-12-23T16:31:58.000000 |       None      |
|  cinder-volume   | openstack-04.novalocal | nova | enabled |   up  | 2014-12-23T16:31:54.000000 |       None      |
+------------------+--------------------------------+------+---------+-------+----------------------------+-----------------+
$ cinder create --display-name demo-volume1 1
+---------------------+--------------------------------------+
|       Property      |                Value                 |
+---------------------+--------------------------------------+
|     attachments     |                  []                  |
|  availability_zone  |                 nova                 |
|       bootable      |                false                 |
|      created_at     |      2014-12-23T16:33:22.538902      |
| display_description |                 None                 |
|     display_name    |             demo-volume1             |
|      encrypted      |                False                 |
|          id         | 11fbce0b-c124-4a4d-a4b3-56564f614c19 |
|       metadata      |                  {}                  |
|         size        |                  1                   |
|     snapshot_id     |                 None                 |
|     source_volid    |                 None                 |
|        status       |               creating               |
|     volume_type     |                 None                 |
+---------------------+--------------------------------------+
$ cinder create --display-name demo-volume2 2
$ cinder create --display-name demo-volume3 3
$ cinder list
+--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
|                  ID                  |   Status  | Display Name | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
| 11fbce0b-c124-4a4d-a4b3-56564f614c19 | available | demo-volume1 |  1   |     None    |  false   |             |
| 7c4e578a-690b-47d3-a6da-66d976b1f823 | available | demo-volume3 |  3   |     None    |  false   |             |
| ae5ee8a6-fa12-4314-9f1c-438c773c5d58 | available | demo-volume2 |  2   |     None    |  false   |             |
+--------------------------------------+-----------+--------------+------+-------------+----------+-------------+

```

### Troubleshooting

If you encoutered below when starting cinder-api

```
2014-12-23 15:30:11.683 28602 CRITICAL cinder [-] ImportError: cannot import name reflection
2014-12-23 15:30:11.683 28602 TRACE cinder Traceback (most recent call last):
2014-12-23 15:30:11.683 28602 TRACE cinder   File "/usr/bin/cinder-api", line 60, in <module>
2014-12-23 15:30:11.683 28602 TRACE cinder     server = service.WSGIService('osapi_volume')
...
2014-12-23 15:30:11.683 28602 TRACE cinder   File "/usr/lib/python2.7/site-packages/cinder/volume/api.py", line 32, in <module>
2014-12-23 15:30:11.683 28602 TRACE cinder     from cinder import flow_utils
2014-12-23 15:30:11.683 28602 TRACE cinder   File "/usr/lib/python2.7/site-packages/cinder/flow_utils.py", line 16, in <module>
2014-12-23 15:30:11.683 28602 TRACE cinder     from taskflow.listeners import base as base_listener
2014-12-23 15:30:11.683 28602 TRACE cinder   File "/usr/lib/python2.7/site-packages/taskflow/listeners/base.py", line 26, in <module>
2014-12-23 15:30:11.683 28602 TRACE cinder     from taskflow.types import failure
2014-12-23 15:30:11.683 28602 TRACE cinder   File "/usr/lib/python2.7/site-packages/taskflow/types/failure.py", line 21, in <module>
2014-12-23 15:30:11.683 28602 TRACE cinder     from oslo.utils import reflection
2014-12-23 15:30:11.683 28602 TRACE cinder ImportError: cannot import name reflection
2014-12-23 15:30:11.683 28602 TRACE cinder 
```

Run this to install taskflow again

```
pip uninstall oslo.utils taskflow
pip install taskflow
```

If you encountered below in horizon. Or horizon dashboard cannot access volume on the web.

```
2014-12-23 16:50:40,427 5150 ERROR openstack_auth.user Unable to retrieve project list.
Traceback (most recent call last):
  File "/usr/lib/python2.7/site-packages/openstack_auth/user.py", line 280, in authorized_tenants
    debug=settings.DEBUG)
  File "/usr/lib/python2.7/site-packages/openstack_auth/utils.py", line 137, in wrapper
    result = func(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/openstack_auth/utils.py", line 188, in get_project_list
    client = get_keystone_client().Client(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/keystoneclient/v2_0/client.py", line 147, in __init__
    self.authenticate()
  File "/usr/lib/python2.7/site-packages/keystoneclient/utils.py", line 318, in inner
    return func(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/keystoneclient/httpclient.py", line 425, in authenticate
    resp = self.get_raw_token_from_identity_service(**kwargs)
  File "/usr/lib/python2.7/site-packages/keystoneclient/v2_0/client.py", line 181, in get_raw_token_from_identity_service
    return plugin.get_auth_ref(self.session)
  File "/usr/lib/python2.7/site-packages/keystoneclient/auth/identity/v2.py", line 79, in get_auth_ref
    authenticated=False, log=False)
  File "/usr/lib/python2.7/site-packages/keystoneclient/session.py", line 438, in post
    return self.request(url, 'POST', **kwargs)
  File "/usr/lib/python2.7/site-packages/keystoneclient/utils.py", line 318, in inner
    return func(*args, **kwargs)
  File "/usr/lib/python2.7/site-packages/keystoneclient/session.py", line 354, in request
    raise exceptions.from_response(resp, method, url)
Unauthorized: The request you have made requires authentication. (Disable debug mode to suppress these details.) (HTTP 401)
```

First check whether your keystone endpoint has correct ip for cinder. Second restart keystone, memcached and httpd on each side.




TODO boot from volume

TODO how does cinder use lvm iscsi initialize_connection result for VM?

## Dive into Cinder LVM

TODO cinder lvm driver basically use iscsi
     the initialize_connection() is invoked when attaching volume

TODO QoS support in ceph/lvm driver not found. Checkout how they are in libvirt side

TODO list the iscsi mapped in vm side
     [Provisioning KVM virtual machines on iSCSI the hard way](https://www.berrange.com/posts/2010/05/05/provisioning-kvm-virtual-machines-on-iscsi-the-hard-way-part-2-of-2/)
     
TODO what is volume type? what is retype?
     https://wiki.openstack.org/wiki/Cinder-multi-backend#Volume_Type


Cinder lvm driver doesn't support qos on cinder side (but libvirt can do it). Many proprietary drivers support qos in cinder driver. Just grep qos.

```
# in cinder/volume/drivers/lvm.py
QoS_support=False
```

No qos support found in ceph's cinder driver (cinder/volume/drivers/rbd.py). But ceph cinder support qos on libvirt side. See [here](http://ceph.com/planet/openstack-ceph-rbd-and-qos/). Libvirt qos and cinder driver qos can both be used, but share some difference (iops vs block io rate?). Related [article](http://www.wzxue.com/openstack-cinder%E7%9A%84qos%E7%89%B9%E6%80%A7%E9%A2%84%E8%A7%88/). 

QoS code api entrance at `cinder/api/contrib/qos_specs_manage.py`. Corresponding volume code at `cinder/volume/qos_specs.py`.



http://blog.csdn.net/gaoxingnengjisuan/article/details/18191943


