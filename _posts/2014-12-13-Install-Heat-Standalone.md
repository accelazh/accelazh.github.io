---
layout: post
title: "Install Heat Standalone"
tagline : "Install Heat Standalone"
description: "Install Heat Standalone"
category: "Openstack"
tags: [openstack, orchestration, heat]
---
{% include JB/setup %}

Installing heat stable/juno on centos 7. I want to run heat in standalone mode, i.e., has least dependent Openstack components. AFAIK keystone is needed. Looking forward to make heat a fully independent orchestration engine which can be used even without Openstack.

## Preparation

First I use "CentOS 7 preparation" to prepare the centos 7.

```
yum install -y python-devel openssl-devel python-pip git gcc mysql-devel postgresql-devel libffi-devel libvirt-devel graphviz sqlite-devel libxslt-devel libxslt libxml2 libxml2-devel
```

For simplicity we just run heat under root.

```
yum install -y mariadb mariadb-server mariadb-devel
pip install mysql-python
service mariadb start
mysql_secure_installation

mysql -uroot -p
mysql> create schema 'heat';
```

If you encounter below error in `pip install MySQL-python`, try [comment these lines out](https://mariadb.atlassian.net/browse/MDEV-6862)

```
vim /usr/include/mysql/my_config_x86_64.h
#ifdef __GLIBC__
#error <my_config.h> MUST be included first!
#endif
```

Intall rabbitmq. On default we have user `guest` with full permissions on virtual host `/`

```
yum install -y erlang
wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.4.2/rabbitmq-server-3.4.2-1.noarch.rpm
rpm --import http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
yum install rabbitmq-server-3.4.2-1.noarch.rpm 
service rabbitmq-server start

# list permissions for user
rabbitmqctl list_permissions
```

Follow my prior keystone post, install keystone in local host using local database. Then start it.

```
# install keystone and start
...
```

Create the token rc file

```
cd ~
echo '
export OS_SERVICE_TOKEN=123abcdef
export OS_SERVICE_ENDPOINT=http://127.0.0.1:35357/v2.0/
' > token.rc
chmod a+x token.rc
source token.rc
```

Add keystone endpoint

```
keystone tenant-create --name admin
keystone tenant-create --name service
keystone user-create --name admin --pass 123work
keystone user-role-add --user admin --tenant admin --role admin
keystone service-create --name=keystone --type=identity --description="Keystone Identity Service"
keystone endpoint-create --service-id=$(keystone service-list | awk '/ identity / {print $2}') --publicurl=http://127.0.0.1:5000/v2.0 --internalurl=http://127.0.0.1:5000/v2.0 --adminurl=http://127.0.0.1:35357/v2.0
```

Add heat user in keystone

```
keystone user-create --name heat --pass 123work
keystone user-role-add --user heat --tenant service --role admin
keystone role-create --name heat_stack_user
keystone role-create --name heat_stack_owner
keystone service-create --name heat --type orchestration --description "Orchestration"
keystone service-create --name heat-cfn --type cloudformation --description "Orchestration"
keystone endpoint-create --service-id $(keystone service-list | awk '/ orchestration / {print $2}') --publicurl http://127.0.0.1:8004/v1/%\(tenant_id\)s --internalurl http://127.0.0.1:8004/v1/%\(tenant_id\)s --adminurl http://127.0.0.1:8004/v1/%\(tenant_id\)s --region regionOne
```

Create admin rc file

```
echo '
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=123work
export OS_AUTH_URL=http://10.224.147.166:35357/v2.0
' > ~/admin.rc
chmod a+x ~/admin.rc

# enable the rc file
unset OS_SERVICE_TOKEN
unset OS_SERVICE_ENDPOINT
source ~/admin.rc
```

## Install Heat

```
# install heat
mkdir -p ~/workspace
cd ~/workspace
git clone https://github.com/openstack/heat.git
cd heat
git checkout stable/juno
cd ..

# install heat client
git clone https://github.com/openstack/python-heatclient.git
cd python-heatclient
python setup.py install
```

```
mkdir /etc/heat
cp -r ~/workspace/heat/etc/heat/* /etc/heat
mkdir /var/lib/heat
mkdir /var/log/heat
```

## Config Heat

Create the heat config file

```
echo '
[DEFAULT]
verbose = True
debug = True
log_dir = /var/log/heat/

rpc_backend = rabbit
rabbit_host = 127.0.0.1
rabbit_userid = guest
rabbit_password = guest

heat_metadata_server_url = http://127.0.0.1:8000
heat_waitcondition_server_url = http://127.0.0.1:8000/v1/waitcondition
heat_watch_server_url = http://127.0.0.1:8003

auth_encryption_key = 123work

[database]
connection = mysql://root:123work@localhost/heat

[keystone_authtoken]
auth_uri = http://127.0.0.1:5000/v2.0
identity_uri = http://127.0.0.1:35357
admin_tenant_name = service
admin_user = heat
admin_password = 123work
' > /etc/heat/heat.conf
```

Synchronized heat database

```
~/workspace/heat/bin/heat-manage db_sync
```

## Start/Stop Heat

```
# to start
~/workspace/heat/bin/heat-api --config-file /etc/heat/heat.conf >> /var/log/heat/api.log 2>&1 &
~/workspace/heat/bin/heat-engine --config-dir /etc/heat/heat.conf >> /var/log/heat/engine.log 2>&1 &

# to stop
pkill -f 'python.+heat'; ps -ef|grep heat
```

## References

* [Heat Standalone Getting Started](http://docs.openstack.org/developer/heat/getting_started/standalone.html)
* [Install Heat Standalone](https://github.com/sushilkm/heat-standalone/blob/master/install-heat)


