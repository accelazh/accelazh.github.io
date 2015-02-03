

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

Overall, Ceph is basically the best choice of Cinder backend. Not counting the "storage convergence" to unify image backend and block backend, and provide boot from volume and fast boot. Cinder, on the other side, can be separated from Openstack and be used as an independent unified enterprise storage management platform.

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

Create the config file on each host. I enable multi-backend following [tutorial](http://openstack-in-production.blogspot.com/2014/03/enable-cinder-multi-backend-with.html).

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
auth_strategy=keystone

enabled_backends=lvm
scheduler_driver=cinder.scheduler.filter_scheduler.FilterScheduler
default_volume_type=lvm

iscsi_helper=lioadm

[lvm]
volume_group=cinder-volumes
volume_backend_name=lvm
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

## Start Cinder

Let's start cinder services

```
# on controller node
su -s /bin/bash cinder -c '/usr/bin/cinder-api >> /var/log/cinder/api.log 2>&1' &
su -s /bin/bash cinder -c '/usr/bin/cinder-scheduler >> /var/log/cinder/scheduler.log 2>&1' &

# on storage node
service lvm2-lvmetad restart
service target restart
su -s /bin/bash cinder -c '/usr/bin/cinder-volume >> /var/log/cinder/volume.log 2>&1' &

# to stop cinder
#ps -ef|grep cinder|awk '{print $2}'|xargs kill
```

### To Verify

Acquire admin access and list services

```
$ source ~/openstack-admin.rc
```

List connected Cinder services

```
$ cinder service-list
+------------------+--------------------------------+------+---------+-------+----------------------------+-----------------+
|      Binary      |              Host              | Zone |  Status | State |         Updated_at         | Disabled Reason |
+------------------+--------------------------------+------+---------+-------+----------------------------+-----------------+
| cinder-scheduler | openstack-01.novalocal | nova | enabled |   up  | 2014-12-23T16:32:00.000000 |       None      |
|  cinder-volume   | openstack-02.novalocal | nova | enabled |   up  | 2014-12-23T16:31:55.000000 |       None      |
|  cinder-volume   | openstack-03.novalocal | nova | enabled |   up  | 2014-12-23T16:31:58.000000 |       None      |
|  cinder-volume   | openstack-04.novalocal | nova | enabled |   up  | 2014-12-23T16:31:54.000000 |       None      |
+------------------+--------------------------------+------+---------+-------+----------------------------+-----------------+
```

The above config already enabled Cinder [multi-backend](https://wiki.openstack.org/wiki/Cinder-multi-backend#Volume_Type). Now create the default backend. Following [tutorial](http://openstack-in-production.blogspot.com/2014/03/enable-cinder-multi-backend-with.html)

```
$ cinder type-create lvm
+--------------------------------------+------+
|                  ID                  | Name |
+--------------------------------------+------+
| 70e42295-8b2c-42b3-a0a3-f337136730f4 | lvm  |
+--------------------------------------+------+
$ cinder type-key lvm set volume_backend_name=lvm
$ cinder extra-specs-list
+--------------------------------------+------+----------------------------------+
|                  ID                  | Name |           extra_specs            |
+--------------------------------------+------+----------------------------------+
| 70e42295-8b2c-42b3-a0a3-f337136730f4 | lvm  | {u'volume_backend_name': u'lvm'} |
+--------------------------------------+------+----------------------------------+
```

Cinder provides QoS. See tutorials [1](http://openstack-in-production.blogspot.com/2014/03/enable-cinder-multi-backend-with.html), [2](http://www.wzxue.com/openstack-cinder%E7%9A%84qos%E7%89%B9%E6%80%A7%E9%A2%84%E8%A7%88/). QoS needs multi-backend enabled. The consumer can be "frontend", "backend" or "both", which means QoS can be done by frontend nova & libvirt, cinder driver & backend storage, or both sides.

```
$ cinder qos-create standard-iops consumer="both"
$ cinder qos-key dcaec566-9ef3-410c-bc88-8feef29ed685 set read_iops_sec=400 write_iops_sec=200
$ cinder qos-key dcaec566-9ef3-410c-bc88-8feef29ed685 set read_bytes_sec=80000000 write_bytes_sec=40000000
$ cinder qos-list
+--------------------------------------+---------------+----------+------------------------------------------------------------------------------------------------------------------------+
|                  ID                  |      Name     | Consumer |                                                         specs                                                          |
+--------------------------------------+---------------+----------+------------------------------------------------------------------------------------------------------------------------+
| dcaec566-9ef3-410c-bc88-8feef29ed685 | standard-iops |   both   | {u'read_bytes_sec': u'80000000', u'write_iops_sec': u'200', u'write_bytes_sec': u'40000000', u'read_iops_sec': u'400'} |
+--------------------------------------+---------------+----------+------------------------------------------------------------------------------------------------------------------------+
```

Associate Cinder QoS with backend type

```
$ cinder qos-associate dcaec566-9ef3-410c-bc88-8feef29ed685 70e42295-8b2c-42b3-a0a3-f337136730f4
```

Create the Cinder volumes. The volume created from image is bootable

```
# create a plain volume
$ cinder create --display-name demo-vol1 --volume-type lvm 1
# create volume from image, which is bootable
$ cinder create --display-name demo-vol2 --volume-type lvm --image-id 383de0c9-420d-4a03-b1c9-499bd8e681c7 1
# list the volumes
$ cinder list
+--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
|                  ID                  |   Status  | Display Name | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
| 6ea7cd9d-a8fb-4345-9e28-9c3a8b7653f1 | available |  demo-vol2   |  1   |     lvm     |   true   |             |
| 97f0cbb0-b661-4fbe-92ea-9ff15dab777e | available |  demo-vol1   |  1   |     lvm     |  false   |             |
+--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
```

Attach the volume to an VM instance. I have some previously created VMs demo-instance1 to 3.

```
$ nova list
+--------------------------------------+----------------+---------+------------+-------------+----------------------------------------+
| ID                                   | Name           | Status  | Task State | Power State | Networks                               |
+--------------------------------------+----------------+---------+------------+-------------+----------------------------------------+
| 66c94a8d-e56d-447b-8c4e-692c296d7550 | demo-instance1 | ACTIVE  | -          | Running     | demo-net=192.168.124.2, 10.224.147.234 |
| 718bad9d-0fe1-4939-8b40-76756bf7f074 | demo-instance2 | ACTIVE  | -          | Running     | demo-net=192.168.124.4, 10.224.147.235 |
| 871d21ce-f4ca-4242-bf63-f1659b42e60d | demo-instance3 | ACTIVE  | -          | Running     | demo-net=192.168.124.8                 |
+--------------------------------------+----------------+---------+------------+-------------+----------------------------------------+
$ nova volume-attach demo-instance1 97f0cbb0-b661-4fbe-92ea-9ff15dab777e
+----------+--------------------------------------+
| Property | Value                                |
+----------+--------------------------------------+
| device   | /dev/vdb                             |
| id       | 97f0cbb0-b661-4fbe-92ea-9ff15dab777e |
| serverId | 66c94a8d-e56d-447b-8c4e-692c296d7550 |
| volumeId | 97f0cbb0-b661-4fbe-92ea-9ff15dab777e |
+----------+--------------------------------------+
$ cinder show 97f0cbb0-b661-4fbe-92ea-9ff15dab777e
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                Property               |                                                                                                    Value                                                                                                     |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|              attachments              | [{u'device': u'/dev/vdb', u'server_id': u'66c94a8d-e56d-447b-8c4e-692c296d7550', u'id': u'97f0cbb0-b661-4fbe-92ea-9ff15dab777e', u'host_name': None, u'volume_id': u'97f0cbb0-b661-4fbe-92ea-9ff15dab777e'}] |
|           availability_zone           |                                                                                                     nova                                                                                                     |
|                bootable               |                                                                                                    false                                                                                                     |
|               created_at              |                                                                                          2015-01-27T14:12:15.000000                                                                                          |
|          display_description          |                                                                                                     None                                                                                                     |
|              display_name             |                                                                                                  demo-vol1                                                                                                   |
|               encrypted               |                                                                                                    False                                                                                                     |
|                   id                  |                                                                                     97f0cbb0-b661-4fbe-92ea-9ff15dab777e                                                                                     |
|                metadata               |                                                                               {u'readonly': u'False', u'attached_mode': u'rw'}                                                                               |
|         os-vol-host-attr:host         |                                                                                        openstack-04.novalocal@lvm#lvm                                                                                        |
|     os-vol-mig-status-attr:migstat    |                                                                                                     None                                                                                                     |
|     os-vol-mig-status-attr:name_id    |                                                                                                     None                                                                                                     |
|      os-vol-tenant-attr:tenant_id     |                                                                                       c48611d23b754e909753d7ec2428819a                                                                                       |
|   os-volume-replication:driver_data   |                                                                                                     None                                                                                                     |
| os-volume-replication:extended_status |                                                                                                     None                                                                                                     |
|                  size                 |                                                                                                      1                                                                                                       |
|              snapshot_id              |                                                                                                     None                                                                                                     |
|              source_volid             |                                                                                                     None                                                                                                     |
|                 status                |                                                                                                    in-use                                                                                                    |
|              volume_type              |                                                                                                     lvm                                                                                                      |
+---------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

On storage node, use `lvdisplay` to see created logic volumes

```
# on host openstsack-04
$ lvdisplay
  --- Logical volume ---
  LV Path                /dev/cinder-volumes/volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e
  LV Name                volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e
  VG Name                cinder-volumes
  LV UUID                Xq95Mb-0kXp-wUKG-AjQ6-5bal-g8cC-wcSdma
  LV Write Access        read/write
  LV Creation host, time openstack-04.novalocal, 2015-01-27 14:12:19 +0000
  LV Status              available
  # open                 1
  LV Size                1.00 GiB
  Current LE             256
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           252:0
$ ll /dev/cinder-volumes/
total 0
lrwxrwxrwx 1 root root 7 Jan 27 14:12 volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e -> ../dm-0
```

On the attacher VM instance, list the attached device `/dev/vdb`

```
# on demo-instance1
ls /dev/vd*
/dev/vda    /dev/vda1   /dev/vdb   
```

Let's see how the VM's libvirt domain changes in response to the attached volume

```
# on host openstack-03, instance-00000037 is demo-instance1's id in libvirt
$ virsh edit instance-00000037
...
  <devices>
    ...
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none'/>
      <source dev='/dev/disk/by-path/ip-10.224.147.173:3260-iscsi-iqn.2010-10.org.openstack:volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e-lun-0'/>
      <target dev='vdb' bus='virtio'/>
      <iotune>
        <read_bytes_sec>80000000</read_bytes_sec>
        <write_bytes_sec>40000000</write_bytes_sec>
        <read_iops_sec>400</read_iops_sec>
        <write_iops_sec>200</write_iops_sec>
      </iotune>
      <serial>97f0cbb0-b661-4fbe-92ea-9ff15dab777e</serial>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
    </disk>
    ...
  </devices>
...
```

Note that the `<iotune>` part provides qos by libvirt side (frontend QoS). Current Cinder LVM driver doesn't support QoS itself (backend QoS). Another example can be found [here](http://www.sebastien-han.fr/blog/2013/12/23/openstack-ceph-rbd-and-qos/).

To see how iscsi targets are setup on the volume node. About [lioadm](http://linux-iscsi.org/wiki/LIO). CentOS 7 use lioadm (targetcli) instead of tgtadm, see [1](https://bugzilla.redhat.com/show_bug.cgi?id=1071423), [2](https://www.centos.org/forums/viewtopic.php?f=47&t=48591). About set up tgtadm iscsi volumes and provision with libvirt pool, see article [1](https://www.berrange.com/posts/2010/05/05/provisioning-kvm-virtual-machines-on-iscsi-the-hard-way-part-1-of-2/), [2](https://www.berrange.com/posts/2010/05/05/provisioning-kvm-virtual-machines-on-iscsi-the-hard-way-part-2-of-2/).

```
# on host openstack-04
$ targetcli ls
o- / ......................................................................................................................... [...]
  o- backstores .............................................................................................................. [...]
  | o- block .................................................................................................. [Storage Objects: 1]
  | | o- iqn.2010-10.org.openstack:volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e  [/dev/cinder-volumes/volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e (1.0GiB) write-thru activated]
  | o- fileio ................................................................................................. [Storage Objects: 0]
  | o- pscsi .................................................................................................. [Storage Objects: 0]
  | o- ramdisk ................................................................................................ [Storage Objects: 0]
  o- iscsi ............................................................................................................ [Targets: 1]
  | o- iqn.2010-10.org.openstack:volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e ............................................. [TPGs: 1]
  |   o- tpg1 .......................................................................................... [no-gen-acls, auth per-acl]
  |     o- acls .......................................................................................................... [ACLs: 1]
  |     | o- iqn.1994-05.com.redhat:d1c48d5dbb6 ....................................................... [1-way auth, Mapped LUNs: 1]
  |     |   o- mapped_lun0 ................. [lun0 block/iqn.2010-10.org.openstack:volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e (rw)]
  |     o- luns .......................................................................................................... [LUNs: 1]
  |     | o- lun0  [block/iqn.2010-10.org.openstack:volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e (/dev/cinder-volumes/volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e)]
  |     o- portals .................................................................................................... [Portals: 1]
  |       o- 0.0.0.0:3260 ..................................................................................................... [OK]
  o- loopback ......................................................................................................... [Targets: 0]

```

Next Let's try boot from volume. Here I boot from Cinder volume. Another way is for nova to generate a bootable volume from you sepcified image, then boot from it, see [manual](http://docs.openstack.org/user-guide/content/create_volume_from_image_and_boot.html). About how to [create bootable volume](https://openstack.redhat.com/forum/discussion/197/booting-from-volume-or-snapshot).

```
$ nova boot --flavor m1.tiny --block-device source=volume,id=6ea7cd9d-a8fb-4345-9e28-9c3a8b7653f1,dest=volume,shutdown=preserve,bootindex=0 --nic net-id=02320589-b038-493a-9106-c9c2c3ebdb42 --security-group default demo-boot-vol
$ nova show 784a31c5-ac36-4bdf-af42-9c7b668d3868
+--------------------------------------+----------------------------------------------------------+
| Property                             | Value                                                    |
+--------------------------------------+----------------------------------------------------------+
| OS-DCF:diskConfig                    | MANUAL                                                   |
| OS-EXT-AZ:availability_zone          | nova                                                     |
| OS-EXT-SRV-ATTR:host                 | openstack-02.novalocal                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname  | openstack-02.novalocal                                   |
| OS-EXT-SRV-ATTR:instance_name        | instance-0000003e                                        |
| OS-EXT-STS:power_state               | 1                                                        |
| OS-EXT-STS:task_state                | -                                                        |
| OS-EXT-STS:vm_state                  | active                                                   |
| OS-SRV-USG:launched_at               | 2015-01-28T13:20:57.000000                               |
| OS-SRV-USG:terminated_at             | -                                                        |
| accessIPv4                           |                                                          |
| accessIPv6                           |                                                          |
| config_drive                         |                                                          |
| created                              | 2015-01-28T13:20:44Z                                     |
| demo-net network                     | 192.168.124.11                                           |
| flavor                               | m1.tiny (1)                                              |
| hostId                               | f679e241961b677f2a7ef572fc56bff74e1a8370c43448ae107dd0d5 |
| id                                   | 784a31c5-ac36-4bdf-af42-9c7b668d3868                     |
| image                                | Attempt to boot from volume - no image supplied          |
| key_name                             | -                                                        |
| metadata                             | {}                                                       |
| name                                 | demo-boot-vol                                            |
| os-extended-volumes:volumes_attached | [{"id": "6ea7cd9d-a8fb-4345-9e28-9c3a8b7653f1"}]         |
| progress                             | 0                                                        |
| security_groups                      | default                                                  |
| status                               | ACTIVE                                                   |
| tenant_id                            | c48611d23b754e909753d7ec2428819a                         |
| updated                              | 2015-01-28T13:20:58Z                                     |
| user_id                              | 6094daee26d9463e8b37e87dc8d8b33d                         |
+--------------------------------------+----------------------------------------------------------+
```

The VM 'demo-boot-vol' is running on volume 'demo-vol2', as its boot disk. Not that "Attempt to boot from volume - no image supplied". Login to this VM, let's check

```
# on VM demo-boot-vol
$ ls /dev/vd*
/dev/vda    /dev/vda1
```

/dev/vda is the volume booted from. Let's leave something

```
# on VM demo-boot-vol
$ pwd
/home/cirros
$ mkdir workspace
$ cd workspace
$ echo "hello world" "$(date)" > hello.txt
```

After than let's destory the VM and attach the volume to demo-instance1

```
$ nova delete demo-boot-vol
$ cinder list
+--------------------------------------+-----------+--------------+------+-------------+----------+--------------------------------------+
|                  ID                  |   Status  | Display Name | Size | Volume Type | Bootable |             Attached to              |
+--------------------------------------+-----------+--------------+------+-------------+----------+--------------------------------------+
| 6ea7cd9d-a8fb-4345-9e28-9c3a8b7653f1 | available |  demo-vol2   |  1   |     lvm     |   true   |                                      |
| 97f0cbb0-b661-4fbe-92ea-9ff15dab777e |   in-use  |  demo-vol1   |  1   |     lvm     |  false   | 66c94a8d-e56d-447b-8c4e-692c296d7550 |
+--------------------------------------+-----------+--------------+------+-------------+----------+--------------------------------------+
$ nova volume-attach demo-instance1 6ea7cd9d-a8fb-4345-9e28-9c3a8b7653f1
```

Let's login to demo-instance1 and check out the file left by demo-boot-vol

```
# on VM demo-instance1
$ ls /dev/vd*
/dev/vda    /dev/vda1   /dev/vdb    /dev/vdd    /dev/vdd1
$ sudo mkdir /mnt/demo-boot-vol
$ sudo mount /dev/vdd1 /mnt/demo-boot-vol
$ cd /mnt/demo-boot-vol
$ cat home/cirros/workspace/hello.txt
hello world Wed Jan 28 06:42:41 MST 2015
```

The file created by demo-boot-vol is still there. It can be shared with demo-instance1 who attached the volume. Note that it is '/dev/vdd' rather than '/dev/vdc' because I previously attached and detached an volume from demo-instance1 once.

## Troubleshooting

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

If you encounter that

```
2015-01-27 15:15:28.876 31039 WARNING cinder.brick.iscsi.iscsi [req-83b9d859-6279-45bf-aa54-38fbd8cb7105 6094daee26d9463e8b37e87dc8d8b33d c48611d23b754e909753d7ec2428819a - - -] Failed to create iscsi t
arget for volume id:volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e: Unexpected error while running command.
Command: None
Exit code: -
Stdout: u"Unexpected error while running command.\nCommand: sudo cinder-rootwrap /etc/cinder/rootwrap.conf tgt-admin --update iqn.2010-10.org.openstack:volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e\nExit 
code: 96\nStdout: u''\nStderr: u'/usr/bin/cinder-rootwrap: Executable not found: tgt-admin (filter match = tgt-admin)\\n'"
Stderr: None
2015-01-27 15:15:28.876 31039 ERROR oslo.messaging.rpc.dispatcher [req-83b9d859-6279-45bf-aa54-38fbd8cb7105 6094daee26d9463e8b37e87dc8d8b33d c48611d23b754e909753d7ec2428819a - - -] Exception during mess
age handling: Failed to create iscsi target for volume volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e.
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher Traceback (most recent call last):
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/oslo/messaging/rpc/dispatcher.py", line 134, in _dispatch_and_reply
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     incoming.message))
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/oslo/messaging/rpc/dispatcher.py", line 177, in _dispatch
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     return self._do_dispatch(endpoint, method, ctxt, args)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/oslo/messaging/rpc/dispatcher.py", line 123, in _do_dispatch
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     result = getattr(endpoint, method)(ctxt, **new_args)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/osprofiler/profiler.py", line 105, in wrapper
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     return f(*args, **kwargs)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/cinder/volume/manager.py", line 877, in initialize_connection
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     volume)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/osprofiler/profiler.py", line 105, in wrapper
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     return f(*args, **kwargs)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/cinder/volume/drivers/lvm.py", line 548, in create_export
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     return self._create_export(context, volume)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/cinder/volume/drivers/lvm.py", line 560, in _create_export
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     self.configuration)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/cinder/volume/iscsi.py", line 61, in create_export
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     conf.iscsi_write_cache)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher   File "/usr/lib/python2.7/site-packages/cinder/brick/iscsi/iscsi.py", line 249, in create_iscsi_target
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher     raise exception.ISCSITargetCreateFailed(volume_id=vol_id)
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher ISCSITargetCreateFailed: Failed to create iscsi target for volume volume-97f0cbb0-b661-4fbe-92ea-9ff15dab777e.
2015-01-27 15:15:28.876 31039 TRACE oslo.messaging.rpc.dispatcher 
```

Be sure that in cinder.conf, `iscsi_helper=lioadm` is put in global namespace, rather than inside any backend's section. If you search in the code you will find `iscsi_helper` is referenced this way

```
# cinder/volume/driver.py::initialize_connection
         if CONF.iscsi_helper == 'lioadm':
             self.target_helper.initialize_connection(volume, connector)
```

If you encounter below in compute log when booting VM from volume

```
2015-01-28 13:01:11.166 19710 ERROR nova.virt.libvirt.driver [-] Error launching a defined domain with XML: <domain type='qemu'>
  <name>instance-0000003d</name>
  <uuid>aa2e1571-1d65-4171-9cad-6f6308ed2983</uuid>
  ...
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' cache='none'/>
      <source file='/var/lib/nova/instances/aa2e1571-1d65-4171-9cad-6f6308ed2983/disk'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
    </disk>
  ...
```

And this one

```
2015-01-28 13:01:11.167 19710 ERROR nova.compute.manager [-] [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983] Instance failed to spawn
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983] Traceback (most recent call last):
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/nova/compute/manager.py", line 2242, in _build_resources
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     yield resources
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/nova/compute/manager.py", line 2112, in _build_and_run_instance
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     block_device_info=block_device_info)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py", line 2621, in spawn
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     block_device_info, disk_info=disk_info)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py", line 4414, in _create_domain_and_network
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     power_on=power_on)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py", line 4338, in _create_domain
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     LOG.error(err)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/nova/openstack/common/excutils.py", line 82, in __exit__
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     six.reraise(self.type_, self.value, self.tb)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/nova/virt/libvirt/driver.py", line 4329, in _create_domain
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     domain.createWithFlags(launch_flags)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/eventlet/tpool.py", line 183, in doit
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     result = proxy_call(self._autowrap, f, *args, **kwargs)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/eventlet/tpool.py", line 141, in proxy_call
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     rv = execute(f, *args, **kwargs)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/eventlet/tpool.py", line 122, in execute
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     six.reraise(c, e, tb)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib/python2.7/site-packages/eventlet/tpool.py", line 80, in tworker
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     rv = meth(*args, **kwargs)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]   File "/usr/lib64/python2.7/site-packages/libvirt.py", line 728, in createWithFlags
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983]     if ret == -1: raise libvirtError ('virDomainCreateWithFlags() failed', dom=self)
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983] libvirtError: Failed to open file '/var/lib/nova/instances/aa2e1571-1d65-4171-9cad-6f6308ed2983/disk': No such file or directory
2015-01-28 13:01:11.167 19710 TRACE nova.compute.manager [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983] 
2015-01-28 13:01:11.168 19710 AUDIT nova.compute.manager [req-2f72b190-4247-4fd7-89a2-14827a92aa4e None] [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983] Terminating instance
2015-01-28 13:01:11.168 19710 AUDIT nova.compute.manager [req-2f72b190-4247-4fd7-89a2-14827a92aa4e None] [instance: aa2e1571-1d65-4171-9cad-6f6308ed2983] Terminating instance
```

Follow [nova-bug-1358624](https://bugs.launchpad.net/nova/+bug/1358624), Sergey's answer. When using the command `nova boot ...`, you need to add `dest=volume` to `--block-device` to tell nova to generate the correct XML for libvirt.

## Dive into Cinder LVM

After tracing the code, I found that when an volume is attached, it follows

```
# nova side
compute/manager.py::attach_volume -> ...

# cinder side
-> ... -> driver.initialize_connection
```

The initialize_connection() is invoked when attaching volume, to return connection parameters that libvirt can put into VM instance's domain XML to connect. Take cidner/volume/drivers/rbd.py as an example.

TODO need a detailed code dive, and verify

Another things is Cinder LVM driver doesn't support qos itself. But many proprietary drivers does support qos in their cinder drivers. Just grep 'qos'.

```
# in cinder/volume/drivers/lvm.py
QoS_support=False
```

It looks like no QoS support found in Ceph's Cinder driver (cinder/volume/drivers/rbd.py). But we can use QoS on the libvirt side, i.e. "frontend" QoS, see [here](http://ceph.com/planet/openstack-ceph-rbd-and-qos/). Libvirt QoS and Cinder driver QoS can both be used,i.e. "frontend" and "backend" QoS. Related [article](http://www.wzxue.com/openstack-cinder%E7%9A%84qos%E7%89%B9%E6%80%A7%E9%A2%84%E8%A7%88/). QoS api code entrance at `cinder/api/contrib/qos_specs_manage.py`. Corresponding volume code at `cinder/volume/qos_specs.py`.

BTW, found a Cinder code analysis [article](http://blog.csdn.net/gaoxingnengjisuan/article/details/18191943).
