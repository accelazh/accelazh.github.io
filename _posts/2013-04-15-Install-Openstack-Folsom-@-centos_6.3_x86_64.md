---
layout: post
category : "Cloud"
title : Openstack Install Guide @ centos 6.3
tagline: "在centos 6.3上安装openstack Folsom"
tags : [openstack]
---

{% include JB/setup %}

## Preparation

### Enable the EPEL repository


    $rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm


### Disable SELinux


    $vim /etc/sysconfig/selinux
    SELINUXTYPE=disabled


### Disable the firewall


    $vim /etc/sysconfig/system-config-firewall
    --disabled


### Install  openstack and all related packages 


    $yum  install -y openstack-utils openstack-keystone python-keystoneclient mysql mysql-server MySQL-python wget openstack-nova openstack-glance openstack-utils memcached qpid-cpp-server openstack-swift openstack-swift-proxy openstack-swift-account openstack-swift-container openstack-swift-object memcached xfsprogs  memcached mod-wsgi openstack-dashboard bridge-utils


## Configure Keystone

### Set up and start MySQL daemon 


    $chkconfig mysqld on
    $service mysqld start

Set mysql root password


    $/usr/bin/mysqladmin -u root password 'root'


### Configure the Keystone database

**The keystone configuration file is `/etc/keystone/keystone.conf`**

#### Check the admin_token in `keystone.conf`


    admin_token=ADMIN


#### Ininsual the keystone db with `openstack-db`

 
    $openstack-db --init --service keystone


*default user/password is keystone/keystone*
   
#### Restart the keystone service 


    $keystone-manage db_sync
    $service openstack-keystone start &&  chkconfig openstack-keystone on
			

### Setting up tenants, users, and roles


    $wget https://raw.github.com/TieWei/tiewei.github.io/master/codes/openstack_guide/sample_data.sh
    $chmod +x sample_data.sh;./sample_data.sh

**default setting is as list :**


    Tenant		User      Roles		Password
    -----------------------------------------
    demo   		admin     admin     secrete
    service		glance    admin 	glance
    service		nova      admin 	nova
    service		ec2       admin 	ec2
    service		swift     admin 	swift

### Verifying Keystone Installation
 
#### Create `adminrc` file 


    $vim adminrc
    export OS_USERNAME=admin
    export OS_PASSWORD=secrete
    export OS_TENANT_NAME=demo
    export OS_AUTH_URL=http://127.0.0.1:35357/v2.0
    $source adminrc


#### Do Verify


    $keystone user-list
    $keystone endpoint-list
    $keystone tenant-list


## Configure Swift

Swift is an object storage for openstack

### Edit Swift Configration Files 


#### edit `/etc/swift/swift.conf`


    [swift-hash]
    swift_hash_path_suffix = swifthashcode


#### setup XFS volume (Use a file to simulate)


    $dd if=/dev/zero of=/srv/swiftdisk bs=100MB count=50 //5G
    $mkfs.xfs -i size=1024  /srv/swiftdisk
    $mkdir -p /srv/node/sdb1
    $echo "/srv/swiftdisk /srv/node/sdb1 xfs loop,noatime,nodiratime,nobarrier,logbufs=8 0 0" >> /etc/fstab
    $mount /srv/node/sdb1
    $chown -R swift:swift /srv/node/ 
    $df -Th


#### edit `/etc/rsyncd.conf`


    uid = root
    gid = root
    log file = /var/log/rsyncd.log
    pid file = /var/run/rsyncd.pid
    address = 127.0.0.1

    [account]
    max connections = 2
    path = /srv/node/
    read only = false
    lock file = /var/lock/account.lock

    [container]
    max connections = 2
    path = /srv/node/
    read only = false
    lock file = /var/lock/container.lock

    [object]
    max connections = 2
    path = /srv/node/
    read only = false
    lock file = /var/lock/object.lock
    

#### edit `/etc/default/rsync`


    RSYNC_ENABLE = true


#### edit `/etc/rc.d/rc.local`


    rsync –daemon


#### create `/etc/swift/account-server.conf`


    [DEFAULT]
    bind_ip = 127.0.0.1
    bind_port = 6002
    workers = 2

    [pipeline:main]
    pipeline = account-server

    [app:account-server]
    use = egg:swift#account

    [account-replicator]

    [account-auditor]

    [account-reaper]


#### create `/etc/swift/container-server.conf`


    [DEFAULT]
    bind_ip = 127.0.0.1
    bind_port = 6001
    workers = 2

    [pipeline:main]
    pipeline = container-server

    [app:container-server]
    use = egg:swift#container

    [container-replicator]

    [container-updater]

    [container-auditor]


#### create `/etc/swift/object-server.conf`


    [DEFAULT]
    bind_ip = 127.0.0.1
    bind_port = 6000
    workers = 2

    [pipeline:main]
    pipeline = object-server

    [app:object-server]
    use = egg:swift#object

    [object-replicator]

    [object-updater]

    [object-auditor]

    [object-expirer]


#### create `/etc/swift/proxy-server.conf`


    [DEFAULT]
    bind_port = 8080
    workers = 8
    user = swift

    [pipeline:main]
    pipeline = healthcheck cache authtoken keystone proxy-server

    [app:proxy-server]
    use = egg:swift#proxy
    allow_account_management = true
    account_autocreate = true

    [filter:cache]
    use = egg:swift#memcache
    memcache_servers = 127.0.0.1:11211

    [filter:catch_errors]
    use = egg:swift#catch_errors

    [filter:healthcheck]
    use = egg:swift#healthcheck

    [filter:keystone]
    paste.filter_factory = keystone.middleware.swift_auth:filter_factory
    operator_roles = admin,SwiftOperator
    is_admin = true
    cache = swift.cache

    [filter:authtoken]
    paste.filter_factory = keystone.middleware.auth_token:filter_factory
    admin_tenant_name = service
    admin_user = swift
    admin_password = swift
    auth_host = 127.0.0.1
    auth_port = 35357
    auth_protocol = http
    signing_dir = /tmp/keystone-signing-swift


#### Add to auto-start 


    $echo "swift-init main start" >> /etc/rc.local
    $echo "swift-init rest start" >> /etc/rc.local


### Start swift services


    cd  /etc/swift 
    $swift-ring-builder account.builder create  10 1 1
    $swift-ring-builder container.builder create 10 1 1
    $swift-ring-builder object.builder create 10 1 1
    $swift-ring-builder account.builder add z1-127.0.0.1:6002/sdb1 100
    $swift-ring-builder container.builder add z1-127.0.0.1:6001/sdb1 100
    $swift-ring-builder object.builder add z1-127.0.0.1:6000/sdb1 100
    $swift-ring-builder account.builder
    $swift-ring-builder container.builder
    $swift-ring-builder object.builder
    $swift-ring-builder account.builder rebalance
    $swift-ring-builder container.builder rebalance
    $swift-ring-builder object.builder rebalance
    $swift-init all start
    $service memcached start


### Verify swift service


    $swift stat


## Configure Glance 

Configure Glance service and set swift as glance back-end storage

### Initialize glance db


    $openstack-db --init --service glance


*default user/password is glance/glance*

####  Edit the Glance configuration files 

##### edit `/etc/glance/glance-api.conf`
	

    [DEFAULT]
    default_store = swift
    swift_store_auth_version = 2
    swift_store_auth_address = http://127.0.0.1:35357/v2.0/
    swift_store_user = service:swift
    swift_store_key = swift
    swift_store_create_container_on_put = True
    [keystone_authtoken]
    #<keystone_server_ip>
    auth_host = 127.0.0.1 
    auth_port = 35357
    auth_protocol = http
    admin_tenant_name = service 
    admin_user = glance 
    admin_password = glance

    [paste_deploy]
    config_file = /etc/glance/glance-api-paste.ini

    flavor=keystone


##### edit `/etc/glance/glance-registry.conf`


    [keystone_authtoken]
    auth_host = 127.0.0.1
    auth_port = 35357
    auth_protocol = http
    admin_tenant_name = service
    admin_user = glance
    admin_password = glance

    [paste_deploy]
    config_file = /etc/glance/glance-registry-paste.ini

    flavor=keystone


### Start glance services


    $glance-manage db_sync
    $service openstack-glance-registry start
    $service openstack-glance-api start
    $chkconfig openstack-glance-registry on
    $chkconfig openstack-glance-api on


### Verify glance service


    $cd ~
    $mkdir stackimages
    $wget -c https://launchpad.net/cirros/trunk/0.3.0/+download/cirros-0.3.0-x86_64-disk.img -O stackimages/cirros.img
    $glance image-create --name=cirros-0.3.0-x86_64 --disk-format=qcow2 --container-format=bare < stackimages/cirros.img


## Configure Nova

### Check and enbale KVM
	

    $egrep '(vmx|svm)' --color=always /proc/cpuinfo


check kvm either kvm-intel is loaded
	

    $lsmod | grep kvm


*If NOT*


    $modprobe kvm
    $modprobe kvm-intel
    add /etc/modules: 
    	kvm
    	kvm-intel

		
### Configuring the SQL Database (MySQL) on the Cloud Controller

    $openstack-db --init --service nova

### Configuring OpenStack Compute

#### edit `/etc/nova/nova.conf`


    [DEFAULT]

    # LOGS/STATE
    logdir=/var/log/nova
    state_path=/var/lib/nova
    lock_path = /var/lib/nova/tmp
    rootwrap_config=/etc/nova/rootwrap.conf

    # SCHEDULER
    compute_scheduler_driver=nova.scheduler.filter_scheduler.FilterScheduler

    # VOLUMES
    volume_driver=nova.volume.driver.ISCSIDriver
    volume_group=nova-volumes
    volume_name_template=volume-%08x
    iscsi_helper=tgtadm

    # DATABASE
    sql_connection=mysql://nova:nova@127.0.0.1/nova

    # COMPUTE
    libvirt_type=kvm
    compute_driver=libvirt.LibvirtDriver
    #instance_name_template=instance-%08x
    api_paste_config=/etc/nova/api-paste.ini

    # COMPUTE/APIS: if you have separate configs for separate services
    # this flag is required for both nova-api and nova-compute
    allow_resize_to_same_host=True

    # APIS
    osapi_compute_extension=nova.api.openstack.compute.contrib.standard_extensions
    ec2_dmz_host=127.0.0.1
    s3_host=127.0.0.1

    #QPRD
    rpc_backend = nova.openstack.common.rpc.impl_qpid
    qpid_hostname=127.0.0.1

    # GLANCE
    image_service=nova.image.glance.GlanceImageService
    glance_api_servers=127.0.0.1:9292

    # NETWORK
    network_manager=nova.network.manager.VlanManager
    force_dhcp_release=False
    dhcpbridge_flagfile=/etc/nova/nova.conf
    firewall_driver=nova.virt.libvirt.firewall.IptablesFirewallDriver
    dhcpbridge = /usr/bin/nova-dhcpbridge
    public_interface=eth0
    vlan_interface=eth0
    injected_network_template = /usr/share/nova/interfaces.template

    # NOVNC CONSOLE
    novncproxy_base_url=http://127.0.0.1:6080/vnc_auto.html
    vncserver_proxyclient_address=127.0.0.1
    vncserver_listen=127.0.0.1

    # AUTHENTICATION
    auth_strategy=keystone
    [keystone_authtoken]
    auth_host = 127.0.0.1
    auth_port = 35357
    auth_protocol = http
    admin_tenant_name = service
    admin_user = nova
    admin_password = nova
    signing_dirname = /tmp/keystone-signing-nova


edit `/etc/libvirt/qemu.conf `


    # The user ID for QEMU processes run by the system instance.
    user = "nova"

    # The group ID for QEMU processes run by the system instance.
    group = "nova"


#### creat nova-volumes (20G)


    $dd if=/dev/zero of=/srv/nova-volumes.img bs=100M count=200 && /sbin/vgcreate nova-volumes `/sbin/losetup --show -f /srv/nova-volumes.img`


edit `/etc/tgt/targets.conf `


    include /var/lib/nova/volumes/*
    $service tgtd restart && chkconfig tgtd on


#### Restart nova services


    $service qpidd restart && chkconfig qpidd on
    $service libvirtd restart && chkconfig libvirtd on
    $nova-manage db sync
    $for svc in api objectstore compute network volume scheduler cert; do  service openstack-nova-$svc start ;  chkconfig openstack-nova-$svc on ;  done


### Verify nova service

Check images from glance


    $nova-manage service list
    $nova image-list 


Creating the Network for Compute VMs


    $nova-manage network create --label=private --fixed_range_v4=192.168.20.0/24 --vlan=250 --bridge=br250 --num_networks=1 --network_size=256
    $nova-manage network list


### Running Virtual Machine Instances

#### disable qpid auth, edit `/etc/qpidd.conf`


    auth=no


#### enable ssh and icmp


    $nova secgroup-list
    $nova secgroup-add-rule default tcp 22 22 0.0.0.0/0
    $nova secgroup-add-rule default icmp -1 -1 0.0.0.0/0


#### adding a keypair (for ssh)


    $mkdir ~/.ssh && ssh-keygen
    $nova keypair-add --pub_key ~/.ssh/id_rsa.pub mykey
    $nova keypair-list


#### starting an instance


    $nova flavor-list //you will get [flavor_id]
    $nova image-list //you will get [image_id]
    $nova boot --flavor [flavor_id] --image  [image_id] --key_name mykey --security_group default cirros
    $nova list //you will get [instance_id]
    $virsh list
    $nova console-log cirros
    //now you can ping the ip of instance or do ssh
    //login as 'cirros' user. default password: 'cubswin:)'. use 'sudo' for root.


#### delete the instance


    $nova delete [instance_id]


## Installing the OpenStack Dashboard

### configure

edit `/etc/openstack-dashboard/local_settings`


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dash',
            'USER': 'dash',
            'PASSWORD': 'dash',
            'HOST': '127.0.0.1',
            'default-character-set': 'utf8'
        },
    }
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

    OPENSTACK_HOST = "127.0.0.1"
    OPENSTACK_KEYSTONE_URL = "http://%s:5000/v2.0" % OPENSTACK_HOST
    OPENSTACK_KEYSTONE_DEFAULT_ROLE = "Member"
    OPENSTACK_KEYSTONE_ADMIN_URL = "http://%s:35357/v2.0" % OPENSTACK_HOST


### Initialize db


    CREATE DATABASE dash;
    GRANT ALL ON dash.* TO 'dash'@'%' IDENTIFIED BY 'dash';
    GRANT ALL ON dash.* TO 'dash'@'localhost' IDENTIFIED BY 'dash';
    $/usr/share/openstack-dashboard/manage.py syncdb
    $service httpd restart


### Verify

login http://127.0.0.1/dashboard  user:admin pass:secrete


##END


