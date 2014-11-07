---
layout: post
title: "Play with Openstack Keystone"
tagline : "Play with Openstack Keystone"
description: "Play with Openstack Keystone"
category: "openstack"
tags: [openstack, keystone, auth]
---
{% include JB/setup %}


I'm going to deploy [Keystone](http://docs.openstack.org/developer/keystone/) on one node (10.224.147.166). Also a single node mysql and memcached will be deploy on it. Yes, one node just play with. For HA and scaling, keystone is stateless.

## Install Keystone

Install from source. First git clone the source. Following the official [install](http://docs.openstack.org/developer/keystone/installing.html) and [config](http://docs.openstack.org/developer/keystone/configuration.html) manual.

```
git clone http://github.com/openstack/keystone.git
cd keystone
git checkout stable/juno
```

Next install keystone. I need to install dependencies fisrt (they are not in requirements.txt).

```
yum install -y gcc
yum install -y python-devel
pip install pbr
pip install python-memcached
```

`pip install MySQL-python` complains about `mysql_config`. Locate the pakcage I'm have a MariaDB-Galera-server on the host which prevents me from installing `mariadb-devel`, which contains `mysql_config`.

```
# show which package has mysql_config
$ yum whatprovides '*bin/mysql_config'
...
1:mariadb-devel-5.5.37-1.el7_0.x86_64 : Files for development of MariaDB/MySQL applications
Repo        : updates
Matched from:
Filename    : /usr/bin/mysql_config
```

But, I can't install `mariadb-devel` because dependency issue

```
$ yum install -y mariadb-devel
...
Transaction check error:
  file /etc/my.cnf from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-common-10.0.14-1.el6.x86_64
  file /usr/share/mysql/czech/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/danish/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/dutch/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/english/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/estonian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/french/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/german/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/greek/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/hungarian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/italian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/japanese/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/korean/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/norwegian-ny/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/norwegian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/polish/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/portuguese/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/romanian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/russian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/serbian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/slovak/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/spanish/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/swedish/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
  file /usr/share/mysql/ukrainian/errmsg.sys from install of mariadb-libs-1:5.5.37-1.el7_0.x86_64 conflicts with file from package MariaDB-Galera-server-10.0.14-1.el6.x86_64
```

I have to hack out 'mysql_config' by myself, to extract `mysql_config` and use.

```
$ cd ..
$ mkdir mariadb-devel
$ cd mariadb-devel
$ yumdownloader mariadb-devel
$ rpm2cpio mariadb-devel-*.x86_64.rpm | cpio -idmv
...
./usr/include/mysql/private/unireg.h
./usr/include/mysql/private/violite.h
./usr/include/mysql/private/waiting_threads.h
./usr/include/mysql/private/welcome_copyright_notice.h
./usr/include/mysql/private/winservice.h
./usr/include/mysql/private/wqueue.h
./usr/include/mysql/psi
./usr/include/mysql/psi/mysql_file.h
./usr/include/mysql/psi/mysql_thread.h
./usr/include/mysql/psi/psi.h
./usr/include/mysql/psi/psi_abi_v1.h
./usr/include/mysql/psi/psi_abi_v2.h
./usr/include/mysql/service_debug_sync.h
./usr/include/mysql/service_kill_statement.h
./usr/include/mysql/service_logger.h
./usr/include/mysql/service_my_snprintf.h
./usr/include/mysql/service_progress_report.h
./usr/include/mysql/service_thd_alloc.h
./usr/include/mysql/service_thd_wait.h
./usr/include/mysql/service_thread_scheduler.h
./usr/include/mysql/services.h
./usr/include/mysql/sql_common.h
./usr/include/mysql/sql_state.h
./usr/include/mysql/sslopt-case.h
./usr/include/mysql/sslopt-longopts.h
./usr/include/mysql/sslopt-vars.h
./usr/include/mysql/typelib.h
...
```

Oh, no! It is a *.c and *.h, I can't find `mysql_config` here. No way to extract the file. Now I will try force install.

```
mv /etc/my.cnf /etc/my.cnf.bk
mv /usr/share/mysql/czech/errmsg.sys /usr/share/mysql/czech/errmsg.sys.bk
mv /usr/share/mysql/danish/errmsg.sys /usr/share/mysql/danish/errmsg.sys.bk
mv /usr/share/mysql/dutch/errmsg.sys /usr/share/mysql/dutch/errmsg.sys.bk
mv /usr/share/mysql/english/errmsg.sys /usr/share/mysql/english/errmsg.sys.bk
mv /usr/share/mysql/estonian/errmsg.sys /usr/share/mysql/estonian/errmsg.sys.bk
mv /usr/share/mysql/french/errmsg.sys /usr/share/mysql/french/errmsg.sys.bk
mv /usr/share/mysql/german/errmsg.sys /usr/share/mysql/german/errmsg.sys.bk
mv /usr/share/mysql/greek/errmsg.sys /usr/share/mysql/greek/errmsg.sys.bk
mv /usr/share/mysql/hungarian/errmsg.sys /usr/share/mysql/hungarian/errmsg.sys.bk
mv /usr/share/mysql/italian/errmsg.sys /usr/share/mysql/italian/errmsg.sys.bk
mv /usr/share/mysql/japanese/errmsg.sys /usr/share/mysql/japanese/errmsg.sys.bk
mv /usr/share/mysql/korean/errmsg.sys /usr/share/mysql/korean/errmsg.sys.bk
mv /usr/share/mysql/norwegian-ny/errmsg.sys /usr/share/mysql/norwegian-ny/errmsg.sys.bk
mv /usr/share/mysql/norwegian/errmsg.sys /usr/share/mysql/norwegian/errmsg.sys.bk
mv /usr/share/mysql/polish/errmsg.sys /usr/share/mysql/polish/errmsg.sys.bk
mv /usr/share/mysql/portuguese/errmsg.sys /usr/share/mysql/portuguese/errmsg.sys.bk
mv /usr/share/mysql/romanian/errmsg.sys /usr/share/mysql/romanian/errmsg.sys.bk
mv /usr/share/mysql/russian/errmsg.sys /usr/share/mysql/russian/errmsg.sys.bk
mv /usr/share/mysql/serbian/errmsg.sys /usr/share/mysql/serbian/errmsg.sys.bk
mv /usr/share/mysql/slovak/errmsg.sys /usr/share/mysql/slovak/errmsg.sys.bk
mv /usr/share/mysql/spanish/errmsg.sys /usr/share/mysql/spanish/errmsg.sys.bk
mv /usr/share/mysql/swedish/errmsg.sys /usr/share/mysql/swedish/errmsg.sys.bk
mv /usr/share/mysql/ukrainian/errmsg.sys /usr/share/mysql/ukrainian/errmsg.sys.bk

yum install -y mariadb-devel
```

Fu*k still got 'Transaction check error'. OK, I give up. It seems that

```
Don't install MariaDB-Galera-server and python application who use mysql on one machine!
```

I will remove MariaDB-Galera-server and install a plain mariadb. Then install MySQL-python

```
yum remove -y MariaDB-Galera-server MariaDB-client galera MariaDB-common MariaDB-compat
yum install -y mariadb-server mariadb mariadb-devel
systemctl daemon-reload
service mariadb start
mysql_secure_installation
pip install MySQL-python

cd ../keystone
```

Finally, insall keystone.

```
python setup.py install
```

Install the user, log folder and config files.

```
mkdir /etc/keystone
cp -r etc/* /etc/keystone/

adduser keystone -s /sbin/nologin
mkdir /var/log/keystone
chown keystone:keystone /var/log/keystone
```

To start/stop keystone

```
# to start. this will continue after shell exits
su -s /bin/bash keystone -c '/bin/keystone-all >> /var/log/keystone/keystone.log 2>&1' &

# to stop
pkill keystone
```

## Install Memcached

Install from repo.

```
yum install -y memcached
service memcached start
```

Check version

```
$ memcached -h
memcached 1.4.15
$ ps -ef|grep memcache
memcach+   596     1  0 09:50 ?        00:00:00 /usr/bin/memcached -u memcached -p 11211 -m 64 -c 1024
```

So the port is `11211`.

We need to install the [python-openstackclient](https://github.com/openstack/python-openstackclient)

```
yum install -y libffi-devel
pip install cryptography
pip install python-openstackclient
```

To see contents in memcached, refer to [here](http://serverfault.com/questions/207356/view-content-of-memcached)

```
echo "stats items" | nc 127.0.0.1 11211
```

## Install Mysql

I already have a mysql installed in prior post. So, omit it.

## Configure Keystone

The first question is [PKI or UUID](http://docs.openstack.org/developer/keystone/configuration.html#pki-or-uuid). Follow the link but note this line

> The current architectural approaches for both UUID and PKI-based tokens have pain points exposed by environments under heavy load (search bugs and blueprints for the latest details and potential solutions).

Next, keystone is able to use a caching layer. Refer to [here](http://docs.openstack.org/developer/keystone/configuration.html#caching-layer)

Now let's config it. Write the config file `/etc/keystone/`

```
[DEFAULT]  # must uppercase
# this is the default "--os-token". need to remove in production: remove AdminTokenAuthMiddleware in keystone-paste.ini
admin_token = 123abcdef 

[identity]
driver = keystone.identity.backends.sql.Identity

[database]
# db connection string refer to http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls
connection = mysql+mysqldb://root:123work@localhost/keystone 
idle_timeout = 200

[memcache]
servers=localhost:11211

[token]
provider = keystone.token.providers.uuid.Provider
driver = keystone.token.persistence.backends.memcache_pool.Token

[cache]
enabled = true
backend = dogpile.cache.memcached

[catalog]
driver = keystone.catalog.backends.templated.Catalog
template_file = /etc/keystone/default_catalog.templates
```

Restart keystone each time config file is changed

```
pkill keystone
keystone-all
```

Synchronize database tables. First you need to create keystone table in mysql.

```
mysql -uroot -p
... # create the 'keystone' table
keystone-manage db_sync
```

Show keystone tables

```
MariaDB [keystone]> show tables;
+------------------------+
| Tables_in_keystone     |
+------------------------+
| assignment             |
| credential             |
| domain                 |
| endpoint               |
| group                  |
| group_domain_metadata  |
| group_project_metadata |
| migrate_version        |
| policy                 |
| project                |
| region                 |
| role                   |
| service                |
| token                  |
| trust                  |
| trust_role             |
| user                   |
| user_domain_metadata   |
| user_group_membership  |
| user_project_metadata  |
+------------------------+
```

Test keystone connectivity

```
openstack --debug --os-token 123abcdef --os-url http://127.0.0.1:35357/v2.0/ project list
keystone --debug --os-token 123abcdef --os-endpoint http://127.0.0.1:35357/v2.0/ user-list
```

On another host (10.224.147.167), try to connect to keystone

```
# on another host
pip install python-keystoneclient
keystone --debug --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ user-list
```

## Setting Up Projects, Users and Roles

Refer to the [guide](http://docs.openstack.org/user-guide-admin/content/admin_cli_manage_projects_users.html)

```
# executed on another host
# create service
$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ service-create --name test-service --type compute --description "service for test"
+-------------+----------------------------------+
|   Property  |              Value               |
+-------------+----------------------------------+
| description |         service for test         |
|   enabled   |               True               |
|      id     | c3c7463a6f6f4e3e847a8f8bdd7365f4 |
|     name    |           test-service           |
|     type    |             compute              |
+-------------+----------------------------------+
$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ service-get test-service
+-------------+----------------------------------+
|   Property  |              Value               |
+-------------+----------------------------------+
| description |         service for test         |
|   enabled   |               True               |
|      id     | 0257cb3029764eedbd074cfd7c9ec6b3 |
|     name    |           test-service           |
|     type    |             compute              |
+-------------+----------------------------------+

# create project
$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ tenant-create --name test-tenant --description "tenant for test"
+-------------+----------------------------------+
|   Property  |              Value               |
+-------------+----------------------------------+
| description |         tenant for test          |
|   enabled   |               True               |
|      id     | d114a213c3d749b19a442dc0d68de5a8 |
|     name    |           test-tenant            |
+-------------+----------------------------------+


# create user
$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ user-create --name test-user --tenant test-tenant --pass test
+----------+----------------------------------+
| Property |              Value               |
+----------+----------------------------------+
|  email   |                                  |
| enabled  |               True               |
|    id    | e595588b4e4c49b2878813df6481173d |
|   name   |            test-user             |
| tenantId | d114a213c3d749b19a442dc0d68de5a8 |
| username |            test-user             |
+----------+----------------------------------+

# assign roles
$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ user-role-list --user test-user --tenant test-tenant
+----------------------------------+----------+----------------------------------+----------------------------------+
|                id                |   name   |             user_id              |            tenant_id             |
+----------------------------------+----------+----------------------------------+----------------------------------+
| 9fe2ff9ee4384b1894a90878d3e92bab | _member_ | e595588b4e4c49b2878813df6481173d | d114a213c3d749b19a442dc0d68de5a8 |
+----------------------------------+----------+----------------------------------+----------------------------------+

$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ role-create --name test-role
+----------+----------------------------------+
| Property |              Value               |
+----------+----------------------------------+
|    id    | fe7417255ffe40c2935a56672973e864 |
|   name   |            test-role             |
+----------+----------------------------------+

$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ role-list
+----------------------------------+-----------+
|                id                |    name   |
+----------------------------------+-----------+
| 9fe2ff9ee4384b1894a90878d3e92bab |  _member_ |
| fe7417255ffe40c2935a56672973e864 | test-role |
+----------------------------------+-----------+

$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ user-role-add --user test-user --role test-role --tenant test-tenant

$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ user-role-list --user test-user --tenant test-tenant
+----------------------------------+-----------+----------------------------------+----------------------------------+
|                id                |    name   |             user_id              |            tenant_id             |
+----------------------------------+-----------+----------------------------------+----------------------------------+
| 9fe2ff9ee4384b1894a90878d3e92bab |  _member_ | e595588b4e4c49b2878813df6481173d | d114a213c3d749b19a442dc0d68de5a8 |
| fe7417255ffe40c2935a56672973e864 | test-role | e595588b4e4c49b2878813df6481173d | d114a213c3d749b19a442dc0d68de5a8 |
+----------------------------------+-----------+----------------------------------+----------------------------------+
```

So the points here are

    * Openstack compute, volume, swift, glance is called `service` in keystone.
    * The url is carried by `endpoint`, which has an associated `service` id. About endpoint config, see [here](http://lin-blog-1.blogspot.com/2013/12/keystone.html).
    * Keystone has `roles`, but they are just names to it. What they mean depends on each services' own policy.json.

Let's play with user authentication. Refer to [here](http://bodenr.blogspot.com/2014/03/openstack-keystone-workflow-token.html)

```
# authenticate user
$ curl -d '{"auth":{"tenantName":"test-tenant", "passwordCredentials":{"username": "test-user", "password": "test"}}}' -H "Content-type: application/json" -X POST http://10.224.147.166:35357/v2.0/tokens | python -m json.tool
... # get the user's token from access.token.id, mine is d114a213c3d749b19a442dc0d68de5a8
$ keystone --os-token d114a213c3d749b19a442dc0d68de5a8 --os-endpoint http://10.224.147.166:35357/v2.0/ user-list
Invalid OpenStack Identity credentials

# add admin role to user
$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ role-create --name admin
+----------+----------------------------------+
| Property |              Value               |
+----------+----------------------------------+
|    id    | 095a652351fe464aafe77bdc90039162 |
|   name   |              admin               |
+----------+----------------------------------+
$ keystone --os-token 123abcdef --os-endpoint http://10.224.147.166:35357/v2.0/ user-role-add --user test-user --tenant test-tenant --role admin

# need to re-login
$ curl -d '{"auth":{"tenantName":"test-tenant", "passwordCredentials":{"username": "test-user", "password": "test"}}}' -H "Content-type: application/json" -X POST http://10.224.147.166:35357/v2.0/tokens | python -m json.tool
... # get the user's token from access.token.id
$ keystone --os-token 1d6e4a386adb468a9f60e408401e1320 --os-endpoint http://10.224.147.166:35357/v2.0/ user-list
+----------------------------------+-----------+---------+-------+
|                id                |    name   | enabled | email |
+----------------------------------+-----------+---------+-------+
| e595588b4e4c49b2878813df6481173d | test-user |   True  |       |
+----------------------------------+-----------+---------+-------+
```

Below is an example result of user authentication


```
$ curl -d '{"auth":{"tenantName":"test-tenant", "passwordCredentials":{"username": "test-user", "password": "test"}}}' -H "Content-type: application/json" -X POST http://10.224.147.166:35357/v2.0/tokens | python -m json.tool
{
    "access": {
        "metadata": {
            "is_admin": 0,
            "roles": [
                "9fe2ff9ee4384b1894a90878d3e92bab",
                "fe7417255ffe40c2935a56672973e864",
                "095a652351fe464aafe77bdc90039162"
            ]
        },
        "serviceCatalog": [
            {
                "endpoints": [
                    {
                        "adminURL": "http://localhost:8776/v1/d114a213c3d749b19a442dc0d68de5a8",
                        "internalURL": "http://localhost:8776/v1/d114a213c3d749b19a442dc0d68de5a8",
                        "publicURL": "http://localhost:8776/v1/d114a213c3d749b19a442dc0d68de5a8",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "Volume Service",
                "type": "volume"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://localhost:9292/v1",
                        "internalURL": "http://localhost:9292/v1",
                        "publicURL": "http://localhost:9292/v1",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "Image Service",
                "type": "image"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://localhost:8774/v1.1/d114a213c3d749b19a442dc0d68de5a8",
                        "internalURL": "http://localhost:8774/v1.1/d114a213c3d749b19a442dc0d68de5a8",
                        "publicURL": "http://localhost:8774/v1.1/d114a213c3d749b19a442dc0d68de5a8",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "Compute Service",
                "type": "compute"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://localhost:8773/services/Admin",
                        "internalURL": "http://localhost:8773/services/Cloud",
                        "publicURL": "http://localhost:8773/services/Cloud",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "EC2 Service",
                "type": "ec2"
            },
            {
                "endpoints": [
                    {
                        "adminURL": "http://localhost:35357/v2.0",
                        "internalURL": "http://localhost:5000/v2.0",
                        "publicURL": "http://localhost:5000/v2.0",
                        "region": "RegionOne"
                    }
                ],
                "endpoints_links": [],
                "name": "Identity Service",
                "type": "identity"
            }
        ],
        "token": {
            "audit_ids": [
                "eG32kxyJS_KidPAihbH18w"
            ],
            "expires": "2014-11-07T16:52:40Z",
            "id": "1d6e4a386adb468a9f60e408401e1320",
            "issued_at": "2014-11-07T15:52:40.800544",
            "tenant": {
                "description": "tenant for test",
                "enabled": true,
                "id": "d114a213c3d749b19a442dc0d68de5a8",
                "name": "test-tenant"
            }
        },
        "user": {
            "id": "e595588b4e4c49b2878813df6481173d",
            "name": "test-user",
            "roles": [
                {
                    "name": "_member_"
                },
                {
                    "name": "test-role"
                },
                {
                    "name": "admin"
                }
            ],
            "roles_links": [],
            "username": "test-user"
        }
    }
}
```

## How Keystone work

The main workflow can be seen from blew picture. Borrowed from [here](https://www.ustack.com/blog/openstack_hacker/). Note that the endpoint server also needs to communicate with Keystone, to verify what the token can do.

![Keystone workflow](/images/keystone-workflow.png "Keystone workflow")

On the side of endpoint service, policy.json defines what role can do what. Here is the example nova's [policy.json](https://github.com/openstack/nova/blob/master/etc/nova/policy.json). Other components, e.g. neutron, also have [one](https://github.com/openstack/neutron/blob/master/etc/policy.json). Note that Keystone also has a policy.json, to control other users/endpoints' access.

```
{
    "context_is_admin":  "role:admin",
    "admin_or_owner":  "is_admin:True or project_id:%(project_id)s",
    "default": "rule:admin_or_owner",

    "cells_scheduler_filter:TargetCellFilter": "is_admin:True",

    "compute:create": "",
    ...
    "compute:unlock_override": "rule:admin_api",

    "compute:shelve": "",
    "compute:shelve_offload": "",
    "compute:unshelve": "",

    "compute:volume_snapshot_create": "",
    "compute:volume_snapshot_delete": "",

    "admin_api": "is_admin:True",
    "compute:v3:servers:start": "rule:admin_or_owner",
    "compute:v3:servers:stop": "rule:admin_or_owner",
    "compute_extension:admin_actions:resume": "rule:admin_or_owner",
    "compute_extension:admin_actions:lock": "rule:admin_or_owner",
    "compute_extension:admin_actions:unlock": "rule:admin_or_owner",
    "compute_extension:admin_actions:resetNetwork": "rule:admin_api",
    "compute_extension:admin_actions:injectNetworkInfo": "rule:admin_api",
    ....
    "compute_extension:migrations:index": "rule:admin_api",
    "compute_extension:v3:os-migrations:index": "rule:admin_api",
    "compute_extension:v3:os-migrations:discoverable": "",
    "compute_extension:os-assisted-volume-snapshots:create": "rule:admin_api",
    "compute_extension:os-assisted-volume-snapshots:delete": "rule:admin_api",
    "compute_extension:console_auth_tokens": "rule:admin_api",
    "compute_extension:v3:os-console-auth-tokens": "rule:admin_api",
    "compute_extension:os-server-external-events:create": "rule:admin_api",
    "compute_extension:v3:os-server-external-events:create": "rule:admin_api",

    "volume:create": "",
    "volume:get_all": "",
    ...
    "volume_extension:snapshot_admin_actions:reset_status": "rule:admin_api",
    "volume_extension:volume_admin_actions:force_delete": "rule:admin_api",

    "network:get_all": "",
    "network:get": "",
    "network:disassociate": "",
    "network:get_vifs_by_instance": "",
    ...
    "network:get_dns_entries_by_name": "",
    "network:attach_external_network": "rule:admin_api"
}
```

But, how does other openstack components interact with Keystone, to verify a user's token?

## Tracing Nova Extension Authorization

I'm using python IDE [liClipse](http://www.liclipse.com/) to dive nova stable/juno code. I want to see how nova extension use policy.json and communicate with Keystone to authorize user request.

```
git clone https://github.com/openstack/nova.git
cd nova
git checkout stable/juno
```

### Part 1

Let's begin from the `authorize(context)` method invoke.

```
nova/api/openstack/compute/contrib/floating_ips.py
    authorize = extensions.extension_authorizer('compute', 'floating_ips')
        core_authorizer(api_name, extension_name)
            def authorize(context, target=None, action=None)
                ...
            return authorize    # so authorize(context) below actually invokes here returned function

    class FloatingIPController(object):
        def show(self, req, id):
        authorize(context)
            nova.policy.enforce(context, act="compute:floating_ips", target={'project_id': xxx, 'user_id': xxx})   # the entry to policy authroize
```

What does `nova.policy.enforce()` do?

```
nova.policy.enforce(context, act="compute:floating_ips", target={'project_id': xxx, 'user_id': xxx})
    init()
        _ENFORCER = policy.Enforcer(policy_file=None, rules=None, default_rule=None, use_conf=None)  # here the _ENFORCE is created
    return _ENFORCER.enforce(act, target, credentials=context.to_dict(), do_raise=True, exc=exception.PolicyNotAuthorized, action=act)
```

What does _ENFORCER.enforce() do?

```
_ENFORCER.enforce(rule="compute:floating_ips", target={'project_id': xxx, 'user_id': xxx}, creds=context.to_dict(), do_raise=True, exc=exception.PolicyNotAuthorized, action=act)
    self.load_rules()
        rules = Rules.load_json(data, self.default_rule)   # loaded from /etc/keystone/policy.json
        self.set_rules(rules)
            self.rules = Rules(rules, self.default_rule)   # self.rules is changed

    if isinstance(rule, BaseCheck):    # false  # a rule can be "A string or BaseCheck"
        ...
    elif not self.rules:           # false
        ...
    else:
        result = self.rules[rule](target, creds, self)     # we execute here

    if do_raise and not result:
        raise PolicyNotAuthorized(rule)     # raise exception here if unauthroized
    return result
```

So what happens in self.rules[rule](target, creds, self)?

```
result = self.rules[rule="compute:floating_ips"](target={'project_id': xxx, 'user_id': xxx}, creds=context.to_dict(), self=<policy object>)
    class Rules(dict):     # Rules is child of dict, so it can []
        ...                # all it do is return the matching [key]

# so, the pesudo code of what happens here is
rules = Rules.load_json(data, self.default_rule)   # loaded from /etc/keystone/policy.json
rule = rules["compute:floating_ips"]
result = rule(target={'project_id': xxx, 'user_id': xxx}, creds=context.to_dict(), self=<policy object>)
return result
```

First question, what Rules.load_json(data, self.default_rule) returns?

```
Rules.load_json(data, self.default_rule)
    rules = dict((k, parse_rule(v)) for k, v in jsonutils.loads(data).items())   # please refer to one copy of policy.json
        # what's in parse_rules(v="rule:admin_api")?
        _parse_text_rule(rule)
            for tok, value in _parse_tokenize(rule):     # _parse_tokenize() returns 'original string token', 'BaseCheck child object'
                state.shift(tok, value)                  # basically, append them
            return state.result               # a crazy syntax analysis state machine. the result is a BaseCheck tree (And, Or, Not, ...)

# so, after the returned is a dick, key is the "compute:floating_ip" staff, value is a BaseCheck tree with And, Or, Not, ...
# the leaf node of BaseCheck should be doing the actual business 

# for example, RoleCheck
class RoleCheck(Check):
    def __call__(self, target, creds, enforcer):
        return self.match.lower() in [x.lower() for x in creds['roles']]

# for example IsAdminCheck
class IsAdminCheck(policy.Check):
    def __call__(self, target, creds, enforcer):
        return creds['is_admin'] == self.expected

In the end, the creds=context.to_dict() is checked for fields like 'is_admin' or 'roles'
```

Second question, what rule(target={'project_id': xxx, 'user_id': xxx}, creds=context.to_dict(), self=<policy object>) does?

```
rule(target={'project_id': xxx, 'user_id': xxx}, creds=context.to_dict(), self=<policy object>)
```

By now, the second question is automatically answered. Overall the authorized like following

    1. Given the `context` object, which contains all information of the user sending request
    2. The policy.json is loaded and translated into dict[str_key => BaseCheck_tree]
    3. Fields in `context` such as 'is_admin' & 'roles' are matched to decide authorization

### Part 2

The question here is: how does the `context` object get filled? Is the Keystone interaction happens when filling `context`?

```
nova/api/openstack/compute/contrib/floating_ips.py
    def index(self, req):
        context = req.environ['nova.context']
        authorize(context)
```

So where calls the index(self, req) with `req` parameter. Where it is filled?

```
/nova/api/openstack/__init__.py::class APIRouter(base_wsgi.Router):
    ... # this class set up nova extension, load them and connect them to URL path

/nova/api/openstack/compute/__init__.py::class APIRouter(nova.api.openstack.APIRouter):
    def _setup_routes(self, mapper, ext_mgr, init_only):
        ... # this is where URL path get actually connected

# Above two classes can be seen as the entry into nova extension. But no where to see the http request call

# the router base class
nova/wsgi.py::class Router(object):
    def __init__(self, mapper):
        self.map = mapper                                                               
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, self.map)     # the routes library
    @webob.dec.wsgify(RequestClass=Request)    # translate input request to wsgi object. so, where input comes?
    def __call__(self, req):
        return self._router
```

How APIRouter gets launched, see /etc/nova/api-paste.ini. About python [paste deploy](http://pythonpaste.org/deploy/).

```
[composite:openstack_compute_api_v2]
use = call:nova.api.auth:pipeline_factory      # define how to use paste
# this is a pipeline of filters, each of them is a WSGI app, the last one is nova api. They wrap around using decorator pattern.
noauth = compute_req_id faultwrap sizelimit noauth ratelimit osapi_compute_app_v2    # use this pipeline if you config auth_strategy=noauth
keystone = compute_req_id faultwrap sizelimit authtoken keystonecontext ratelimit osapi_compute_app_v2    # use this pipeline if you config auth_strategy=keystone. this is default
keystone_nolimit = compute_req_id faultwrap sizelimit authtoken keystonecontext osapi_compute_app_v2      # use this pipeline if you config auth_strategy=keystone_nolimit

[app:osapi_compute_app_v2]
paste.app_factory = nova.api.openstack.compute:APIRouter.factory

# about pipeline (at nova/api/auth.py)
def _load_pipeline(loader, pipeline):
    app = loader.get_app(pipeline[-1])
    for filter in filters:
        app = filter(app)
    return app

# all these filters and the finally osapi_compute_app_v2 are WSGI apps, wrapping layer by layer. So, decorator pattern.
```

Note the `authtoken` and `keystonecontext` here. In the last part of api-paste.ini

```
##########
# Shared #
##########

[filter:keystonecontext]
paste.filter_factory = nova.api.auth:NovaKeystoneContext.factory          # inside nova api

[filter:authtoken]
paste.filter_factory = keystonemiddleware.auth_token:filter_factory       # keystonemiddleware is another lib, see requirements.txt
```

Let's first see class NovaKeystoneContext.

```
nova/api/auth.py::class NovaKeystoneContext(wsgi.Middleware):
    def __call__(self, req):
        roles = self._get_roles(req)
            roles = req.headers.get('X_ROLES', '')
        auth_token = req.headers.get('X_AUTH_TOKEN', req.headers.get('X_STORAGE_TOKEN'))
        ctx = context.RequestContext(user_id,
                                     project_id,
                                     user_name=user_name,
                                     project_name=project_name,
                                     roles=roles,
                                     auth_token=auth_token,
                                     remote_address=remote_address,
                                     service_catalog=service_catalog,
                                     request_id=req_id)
        req.environ['nova.context'] = ctx          # remember the req.environ['nova.context'] here. this is where context object is filled
        return self.application                    # another thing is, no remote access to keystone here!
```

Haha, this is the right place where the `context` object get filled. Found it! Another thing is, this function DOESN'T do remote communite, nor Keystone. The communication with Keystone must happen before this step.

Now let's check out [keystonemiddleware.auth_token](https://github.com/openstack/keystonemiddleware/blob/master/keystonemiddleware/auth_token.py) on github.

```
git clone https://github.com/openstack/keystonemiddleware.git
cd keystonemiddleware
... # open the LiClipse IDE
```

Tracing the code

```
# the factory returns the actual keystonemiddleware.auth_token app - AuthProtocol
def filter_factory(global_conf, **local_conf):
    def auth_filter(app):
        return AuthProtocol(app, conf)
    return auth_filter

class AuthProtocol(object):
    def __call__(self, env, start_response):
        # get token field from header. no remote access
        user_token = self._get_user_token_from_header(env)
        # access memcached for caching. verify token remote on Keystone server. can see the url inside.
        token_info = self._validate_token(user_token, env)
            data = self._identity_server.verify_token(token, retry)
                path = '/tokens/%s' % user_token
                # this is where we communicate to Keystone, asking to verify incoming user token
                response, data = self._json_request('GET', path, authenticated=True, endpoint_filter={'version': version}, headers=headers)
            return data
        # everything above is added into env
        self._add_headers(env, user_headers)

        return self._call_app(env, start_response)
            return self._app(env, _fake_start_response)    # self._app = app, in def __init__(self, app, conf)
                ... # calling to next layer WSGI app
```

Finally, the things become clear now. The overall workflow is listed following

    1. WSGI app keystonemiddleware.auth_token access to keystone '/tokens/%s' % user_token to verify. Also returns detailed user information (e.g. roles, is_admin, etc).
    2. The nova.api.auth:NovaKeystoneContext fills in req.environ['nova.context'], which later be created as the `context` object.
    3. Finally, execution is passed to nova api, entering nova.api.openstack.compute:APIRouter. (See api-paste.ini)
        1. Given the `context` object, which contains all information of the user sending request
        2. The policy.json is loaded and translated into dict[str_key => BaseCheck_tree]
        3. Fields in `context` such as 'is_admin' & 'roles' are matched to decide authorization

## Useful Materials

* Keystone tutorial: <http://blog.flux7.com/blogs/openstack/tutorial-what-is-keystone-and-how-to-install-keystone-in-openstack>
* Another Keystone tutorial: <http://lin-blog-1.blogspot.com/2013/12/keystone.html>
* Shell Keystone example: <https://github.com/openstack/keystone/blob/master/tools/sample_data.sh>
* Workflow with token: <http://bodenr.blogspot.com/2014/03/openstack-keystone-workflow-token.html>
