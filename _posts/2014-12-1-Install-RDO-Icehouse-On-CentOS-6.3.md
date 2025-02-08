---
layout: post
title: "Install RDO Icehouse on CentOS 6.3"
tagline : "Install RDO Icehouse on CentOS 6.3"
description: "Install Icehouse RDO on CentOS 6.3"
category: "Openstack"
tags: [openstack, rdo, centos]
---
{% include JB/setup %}


As the first step I will try to install RDO Icehouse on CentOS 6.3, with heat in it. After trying out template orchestration in heat, I will try to seperate heat as an independent component and extend resource plugin to support vmware and ansible. Heat becomes a pure orchestration engine (partially support [TOSCA](http://docs.oasis-open.org/tosca/TOSCA/v1.0/os/TOSCA-v1.0-os.html)).

## Environment

[RDO](https://openstack.redhat.com/Quickstart) all-in-one deploy.

  * Node: 10.224.147.150 
  * OS: CentOS 6.3 (hardened)
  * Openstack Version: stable/icehourse 
  * Python: 2.6.3

Python 2.6 is [supported](http://osdir.com/ml/openstack-dev/2014-10/msg00033.html) by stable/juno until kilo. But RDO juno only [supports](https://openstack.redhat.com/forum/discussion/992/rdo-juno-packages-available/p1) CentOS 7 / RHEL7. So we choose stable/icehouse.

Overall, my conclusion is CentOS 6.3 + RDO Icehouse is a bad choice which is problematic to install, better use CentOS 6.5 or 7. I have reinstalled RDO 32 times before success.

## Preparation

First, get root

```
sudo su -
```

Install repo file

```
rm -rf /etc/yum.repos.d/*
cd /etc/yum.repos.d/
wget https://github.com/accelazh/Centos-6.3-default-repo/archive/master.zip
unzip master
cp Centos-6.3-default-repo-master/* ./
rm -rf master Centos-6.3-default-repo-master
cd ~
yum clean all
```

Change umasks. Then *logout, then login again*.

```
for i in /root/.bashrc /root/.bash_profile /root/.cshrc /root/.tcshrc /etc/bashrc /etc/profile /etc/csh.cshrc; do
    sed -i 's/^\([ \t]*\)umask\([ \t]\+\)077\([ \t]*\)$/\1umask\2022\3/' $i;
done
```

Make yum mirro timeout waiting longer in case slow network.

```
echo '
timeout = 300
' >> /etc/yum.conf
```

Install common dependencies

```
yum groupinstall -y "Development tools"
yum install -y curl vim git gcc yum-utils zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel python-devel openssl-devel python-pip git gcc mysql-devel postgresql-devel libffi-devel libvirt-devel graphviz sqlite-devel libxslt-devel libxslt libxml2 libxml2-devel

# install pip
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python get-pip.py

# add easy-to-use vim config
echo '
set background=dark
" set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set hlsearch
" set number
' >> /etc/vimrc
```

## Install RDO Icehouse

Install the RDO Icehouse release repo. Find it at [rdo repo list](https://openstack.redhat.com/Repositories#Browsing).

```
# install rdo repo files in /etc/yum.repo.d/
wget https://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-4.noarch.rpm
wget https://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-4.src.rpm
yum install -y rdo-release-icehouse-4.noarch.rpm rdo-release-icehouse-4.src.rpm
```

Install packstack, aka RDO, the installer to openstack.

```
yum install -y openstack-packstack
```

If above command fails, and you use curl to get repomd.xml and also fail. Refer to [here](https://www.redhat.com/archives/rdo-list/2014-October/msg00111.html) and [here](https://bugzilla.redhat.com/show_bug.cgi?id=527771). Below is the fix.

```
# fail: NSS error -8092
curl -v https://repos.fedorapeople.org/repos/openstack/openstack-icehouse/epel-6/repodata/repomd.xml

# but this can pass
curl -LIv --ciphers rsa_aes_128_sha https://repos.fedorapeople.org/repos/openstack/openstack-icehouse/epel-6/repodata/repomd.xml

# so it is the ssl negotiation problem, update the nss packages. nss is the underlying lib used by ssl.
yum install -y nss
```

Packstack requires root ssh login

```
vim /etc/ssh/sshd_config
# replace below line
PermitRootLogin yes
```

Run packstack

```
packstack --allinone
```

If you encounter `Error: /Stage[main]/Neutron::Keystone::Auth/Keystone_user[neutron]: Could not evaluate: Execution of '/usr/bin/keystone --os-auth-url http://127.0.0.1:35357/v2.0/ token-get' returned 1: The request you have made requires authentication. (HTTP 401)`. Try below to reinstall. Refer to [here](https://ask.openstack.org/en/question/9620/how-to-resolve-keystone-error/).

```
# delete mysql so it wont prevent RDO to setup mysql password
#mysqladmin -u root  password ''
#yum remove -y mysql mariadb-galera-server mysql-devel mysql-libs mariadb-galera-common

# delete keystone tables
mysql -uroot
mysql> use keystone;
mysql> delete from token;
mysql> delete from user;

# reinstall with specified answier file
packstack --answer-file=<your-answer-file>
#packstack --answer-file=packstack-answers-20141124-125008.txt    # example
```

If you encountered `Error: Could not find a suitable provider for cron`. Refer to [this solution](http://stackoverflow.com/questions/21802223/how-to-install-crontab)

```
yum install -y vixie-cron
service crond start
chkconfig crond on
```

If the first time you run RDO and it passed, things will be easy. But if the first time it failed, and you have tu re-run RDO, problem may raise. You can first try reinstall using the same last answer file. If not work, uninstall RDO and try again. Here is [how to uninstal RDO](https://openstack.redhat.com/Uninstalling_RDO).

```
# remove RDO totally
for x in $(virsh list --all | grep instance- | awk '{print $2}') ; do virsh destroy $x ; virsh undefine $x ; done ; yum remove -y nrpe "*nagios*" puppet ntp "ntp-*" ntpdate "rdo-release" "*openstack*" "*nova*" "*keystone*" "*glance*" "*cinder*" "*swift*" mysql mysql-server httpd "*memcache*" scsi-target-utils iscsi-initiator-utils perl-DBI perl-DBD-MySQL ; ps -ef | grep -i repli | grep swift | awk '{print $2}' | xargs kill ; rm -rf /etc/nagios /etc/yum.repos.d/packstack_* /root/.my.cnf /var/lib/mysql/ /var/lib/glance /var/lib/nova /etc/nova /etc/swift /srv/node/device*/* /var/lib/cinder/ /etc/rsync.d/frag* /var/cache/swift /var/log/keystone /tmp/keystone-signing-nova ; find /etc | grep rpmsave | xargs rm -vf ; umount /srv/node/device* ; killall -9 dnsmasq tgtd httpd ; setenforce 1 ; vgremove -f cinder-volumes ; losetup -a | sed -e 's/:.*//g' | xargs losetup -d ; find /etc/pki/tls -name "ssl_ps*" | xargs rm -rf ; for x in $(df | grep "/lib/" | sed -e 's/.* //g') ; do umount $x ; done

# reinstall rdo, better using last answer file
packstack --answer-file=<your-last-answer-file>
```

Usually packstack `testing if puppet apply is finished` takes 30min. But if your packstack stucks at `testing if puppet apply is finished: <your-ip>_neutron.pp` for hours, check whether your kernel enables `network namespace`. Here is the [complain](https://openstack.redhat.com/forum/discussion/527/testing-if-puppet-apply-is-finished-stuck-for-hours/p1). I found solution at [here](https://openstack.redhat.com/forum/discussion/777/openstack-neutron-stuck-at-installation/p1). This is a [guide](http://spredzy.wordpress.com/2013/11/22/enable-network-namespaces-in-centos-6-4/) to enable network namespace in kernel for RDO.

```
# add network namespace this should raise no error
ip netns add spredzy
ip netns list

# otherwise, upgrade your kernel
yum install kernel iproute

# you should have one of below kernel or iproute package installed
kernel-2.6.32-358.123.2.openstack.el6.x86_64
kernel-firmware-2.6.32-358.123.2.openstack.el6.noarch
iproute-2.6.32-130.el6ost.netns.2.x86_64

# must reboot because either your or packstack has upgraded the kernel
reboot

# reinstall
packstack --answer-file=<your-last-answer-file>
```

If you encountered `Error: Unable to connect to mongodb server! (<your-ip>:27017)`. A walkaround found at [here](http://blog.csdn.net/oneinmore/article/details/38423569).

```
# reinstall mongodb
yum remove -y mongodb-server python-pymongo mongodb
yum install -y mongodb-server python-pymongo mongodb

service mongod start
chkconfig mongod on
# check possible errors here
less /var/log/mongodb/mongodb.log 
# try connect to mongo server
mongo

# reinstall packstack
packstack --answer-file=<your-last-answer-file>
```

If you still see `Error: Unable to connect to mongodb server` and found `/usr/bin/mongod: symbol lookup error: /usr/bin/mongod: undefined symbol: _ZN7pcrecpp2RE4InitEPKcPKNS_10RE_OptionsE` in log file. This is because RDO repo's mongodb-server breaks with CentOS 6.3.

```
# the mongodb-server, which is causing error, is installed from RDO repo
$ yum provides mongodb-server
Loaded plugins: fastestmirror, priorities
Loading mirror speeds from cached hostfile
119 packages excluded due to repository priority protections
mongodb-server-2.4.6-1.el6.x86_64 : MongoDB server, sharding server and support scripts
Repo        : openstack-icehouse
Matched from:

```

Follow this [walkaround](http://blog.csdn.net/oneinmore/article/details/38423569). Download mongod binary and replace the RDO one.

```
yum install -y mongodb-server python-pymongo mongodb

# download binary from monodb official site, and replace current installed one
wget http://downloads.mongodb.org/linux/mongodb-linux-x86_64-2.4.6.tgz
tar -xzvf mongodb-linux-x86_64-2.4.6.tgz 
cp mongodb-linux-x86_64-2.4.6/bin/mongod /usr/bin/mongod
chmod a+x /usr/bin/mongod
chown -R mongodb:mongodb /var/log/mongodb
chown -R mongodb:mongodb /var/lib/mongodb

# test whether mongodb can work
service mongod restart
mongo

# reinstall RDO
packstack --answer-file=<your-last-answer-file>
```

If you mongodb still can not work, raising `Error: couldn't connect to server 127.0.0.1:27017 at src/mongo/shell/mongo.js:145` after command `mongo`. Try modify the `bind_ip`.

```
vim /etc/mongodb.conf
# replace this line
bind_ip = 0.0.0.0

# test whether mongodb can work
service mongod restart
mongo

# reinstall RDO
packstack --answer-file=<your-last-answer-file>
```

If you encountered `ERROR : Error appeared during Puppet run: 10.224.147.150_nagios.pp` with `/Stage[main]/Main/Exec[nagios-plugins-ping]/returns: Error: Nothing to do`. Try below then reinstall packstack with the same answer file.

```
yum install -y nagios nagios-plugins-ping monitoring-plugins-ping

```

If after installation, you login horizon and find no heat. You need to enable heat in answer file and reinstall.

```
vim <your-last-answer-file>
# change this line
CONFIG_HEAT_INSTALL=y
```

Finally, installation complete! Here is the execution output.

```
$ packstack --answer-file packstack-answers-XXXX-XXXX.txt 
Welcome to Installer setup utility

Installing:
Clean Up                                             [ DONE ]
Setting up ssh keys                                  [ DONE ]
Discovering hosts' details                           [ DONE ]
Adding pre install manifest entries                  [ DONE ]
Preparing servers                                    [ DONE ]
Adding AMQP manifest entries                         [ DONE ]
Adding MariaDB manifest entries                      [ DONE ]
Adding Keystone manifest entries                     [ DONE ]
Adding Glance Keystone manifest entries              [ DONE ]
Adding Glance manifest entries                       [ DONE ]
Adding Cinder Keystone manifest entries              [ DONE ]
Adding Cinder manifest entries                       [ DONE ]
Checking if the Cinder server has a cinder-volumes vg[ DONE ]
Adding Nova API manifest entries                     [ DONE ]
Adding Nova Keystone manifest entries                [ DONE ]
Adding Nova Cert manifest entries                    [ DONE ]
Adding Nova Conductor manifest entries               [ DONE ]
Creating ssh keys for Nova migration                 [ DONE ]
Gathering ssh host keys for Nova migration           [ DONE ]
Adding Nova Compute manifest entries                 [ DONE ]
Adding Nova Scheduler manifest entries               [ DONE ]
Adding Nova VNC Proxy manifest entries               [ DONE ]
Adding Openstack Network-related Nova manifest entries[ DONE ]
Adding Nova Common manifest entries                  [ DONE ]
Adding Neutron API manifest entries                  [ DONE ]
Adding Neutron Keystone manifest entries             [ DONE ]
Adding Neutron L3 manifest entries                   [ DONE ]
Adding Neutron L2 Agent manifest entries             [ DONE ]
Adding Neutron DHCP Agent manifest entries           [ DONE ]
Adding Neutron LBaaS Agent manifest entries          [ DONE ]
Adding Neutron Metering Agent manifest entries       [ DONE ]
Adding Neutron Metadata Agent manifest entries       [ DONE ]
Checking if NetworkManager is enabled and running    [ DONE ]
Adding OpenStack Client manifest entries             [ DONE ]
Adding Horizon manifest entries                      [ DONE ]
Adding Swift Keystone manifest entries               [ DONE ]
Adding Swift builder manifest entries                [ DONE ]
Adding Swift proxy manifest entries                  [ DONE ]
Adding Swift storage manifest entries                [ DONE ]
Adding Swift common manifest entries                 [ DONE ]
Adding Provisioning Demo manifest entries            [ DONE ]
Adding Provisioning Glance manifest entries          [ DONE ]
Adding MongoDB manifest entries                      [ DONE ]
Adding Ceilometer manifest entries                   [ DONE ]
Adding Ceilometer Keystone manifest entries          [ DONE ]
Adding Nagios server manifest entries                [ DONE ]
Adding Nagios host manifest entries                  [ DONE ]
Adding post install manifest entries                 [ DONE ]
Installing Dependencies                              [ DONE ]
Copying Puppet modules and manifests                 [ DONE ]
Applying 10.224.147.150_prescript.pp
10.224.147.150_prescript.pp:                         [ DONE ]          
Applying 10.224.147.150_amqp.pp
Applying 10.224.147.150_mariadb.pp
10.224.147.150_amqp.pp:                              [ DONE ]        
10.224.147.150_mariadb.pp:                           [ DONE ]        
Applying 10.224.147.150_keystone.pp
Applying 10.224.147.150_glance.pp
Applying 10.224.147.150_cinder.pp
10.224.147.150_keystone.pp:                          [ DONE ]         
10.224.147.150_cinder.pp:                            [ DONE ]         
10.224.147.150_glance.pp:                            [ DONE ]         
Applying 10.224.147.150_api_nova.pp
10.224.147.150_api_nova.pp:                          [ DONE ]         
Applying 10.224.147.150_nova.pp
10.224.147.150_nova.pp:                              [ DONE ]     
Applying 10.224.147.150_neutron.pp
10.224.147.150_neutron.pp:                           [ DONE ]        
Applying 10.224.147.150_neutron_fwaas.pp
Applying 10.224.147.150_osclient.pp
Applying 10.224.147.150_horizon.pp
10.224.147.150_neutron_fwaas.pp:                     [ DONE ]              
10.224.147.150_osclient.pp:                          [ DONE ]              
10.224.147.150_horizon.pp:                           [ DONE ]              
Applying 10.224.147.150_ring_swift.pp
10.224.147.150_ring_swift.pp:                        [ DONE ]           
Applying 10.224.147.150_swift.pp
Applying 10.224.147.150_provision_demo.pp
Applying 10.224.147.150_provision_glance.pp
10.224.147.150_swift.pp:                             [ DONE ]                 
10.224.147.150_provision_demo.pp:                    [ DONE ]                 
10.224.147.150_provision_glance.pp:                  [ DONE ]                 
Applying 10.224.147.150_mongodb.pp
10.224.147.150_mongodb.pp:                           [ DONE ]        
Applying 10.224.147.150_ceilometer.pp
Applying 10.224.147.150_nagios.pp
Applying 10.224.147.150_nagios_nrpe.pp
10.224.147.150_ceilometer.pp:                        [ DONE ]            
10.224.147.150_nagios.pp:                            [ DONE ]            
10.224.147.150_nagios_nrpe.pp:                       [ DONE ]            
Applying 10.224.147.150_postscript.pp
10.224.147.150_postscript.pp:                        [ DONE ]           
Applying Puppet manifests                            [ DONE ]
Finalizing                                           [ DONE ]

 **** Installation completed successfully ******
```

Login horizon and checkout the orchestration panel.
