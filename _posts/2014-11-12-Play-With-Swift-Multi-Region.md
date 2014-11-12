---
layout: post
title: "Play with Swift Multi-region"
tagline : "Play with Swift Multi-region"
description: "Play with Swift Multi-region"
category: "openstack"
tags: [openstack, swift, storage, multi-region]
---
{% include JB/setup %}

Deploy one Swift cluster in multiple datacenters (i.e. regions, I will mix use the two words.), this is called multi-region, or global cluster. All datacenters gets a unified interface with eventual consistency. Objects are replicated and distrubuted across datacenters.

## Architecture

After Swift 1.9.0, global cluster is supported. All regions share the same ring file. Once you have added different regions into the ring file, the global cluster takes effect. This is the least config, by which global cluster is ready to work.

However, usually global cluster is combined with "Dedicated Replication Network" and "Read/Write Affinity".

### Dedicated Replication Network

Dedicated Replication Network use seperated network for replication, to make replication more efficient and reliable. WAN between datacenters usually has higher latency and lower reliability, and need VPN protection.

So, for now there are 3 networks

* Public network. Clients connects to proxy nodes
* Storage local network. Proxy node read and write to storage nodes. Replication requests don't run here. It should be VPN connected across datacenters, for cross regional read/write.
* Storage replication network. Region internal replication requests run on this network. Cross regioinal replication also run on this network. It should be VPN connected across all datacenters.

You should carefully choose which service binds to which network, including rsync. On each node there will launch 2 sets of object/container/account services
    
* Non-replication services. Don't do any replication work. Use /etc/swift/object-server/1.conf, /etc/swift/container-server/1.conf, or /etc/swift/account-server/1.conf. There is no `[<*>-replicator]` section in config file. Bind to storage local network.
* Replication services. Only do replication work. Use /etc/swift/object-server/2.conf, /etc/swift/container-server/2.conf, or /etc/swift/account-server/2.conf. Only has `[<*>-replicator]` section (and mandatory sections) in config file. Bind to storage replication network.

Also rsync should be bind to storage replication network. Proxy nodes needs 2 NICs each. Storage nodes need 2 NICs each. There are no longer any /etc/swift/object-server.conf, /etc/swift/container-server.conf, nor /etc/swift/account-server.conf.

### Read/Write Affinity

Replicas of a partition will be distributed to different regions, according to ring file. Without r/w affinity, one read/write from a proxy server will access always access different region, which is too slow.

After added r/w affinity, the proxy servers become region aware. They will first read/write to affinity locations, usually configured to be the local one. After that replicators will eventually distribute replicas across datacenters.

### Not So Useful References

* [SAIO dedicated replication network](http://docs.openstack.org/developer/swift/replication_network.html)
* [Swift network planning](http://docs.openstack.org/juno/install-guide/install/yum/content/object-storage-network-planning.html)
* [Swift 1.9.0 released: global clusters](http://lists.openstack.org/pipermail/openstack-dev/2013-July/011221.html)

They looks like but different from what I need.

## Environment

I will install Swift under multi-region, or called global cluster mode here. In real world each region corresponds to a seperated datacenter. Each zone corresponds to a rack.

* Region 1
    * Zone 1: node 10.224.147.166
    * Zone 2: node 10.224.147.167
    * Zone 3: node 10.224.147.168
* Region 2
    * Zone 1: node 10.224.147.173
    * Zone 2: node 10.224.147.174

A zone can include multiple nodes (or called machines), but I will use only 1 here. All nodes is VM with CentOS 7. Continuing from my last post "Play with Openstack Keystone". All machines should have already passed through

1. "CentOS 7 Preparation" in my prior post
2. Install and Configuration -> Prerequisites
3. Install and Configuration -> Installation
4. Install and Configuration -> Configuration -> Rsync for Swift
5. Install and Configuration -> Configuration -> Memcached for Swift

Leave behind Swift config and ring files. Delete all original existing config file, ring file and original data file

```
rm -rf /etc/swift/*
rm -rf /srv/node/sdb1/*
```

## Installtion and Configuration

### Config Rsync

Compared rsync config in last swift post, need to add module for replicators. And, bind address to storage replication network.

```
echo '
uid = nobody
gid = nobody
log file = /var/log/rsyncd.log
pid file = /var/run/rsyncd.pid
address = <storage-replication-network-ip>

use chroot = true
timeout = 300
log format = %t %a %m %f %b

[account]
max connections = 20
path = /srv/node/
read only = false
write only = false
list = yes
uid = swift
gid = swift
incoming chmod = 0644
outgoing chmod = 0644
lock file = /var/lock/account.lock
 
[container]
max connections = 20
path = /srv/node/
read only = false
write only = false
list = yes
uid = swift
gid = swift
incoming chmod = 0644
outgoing chmod = 0644
lock file = /var/lock/container.lock
 
[object]
max connections = 20
path = /srv/node/
read only = false
write only = false
list = yes
uid = swift
gid = swift
incoming chmod = 0644
outgoing chmod = 0644
lock file = /var/lock/object.lock

[account6002]
max connections = 20
path = /srv/node/
read only = false
write only = false
list = yes
uid = swift
gid = swift
incoming chmod = 0644
outgoing chmod = 0644
lock file = /var/lock/account6002.lock
 
[container6001]
max connections = 20
path = /srv/node/
read only = false
write only = false
list = yes
uid = swift
gid = swift
incoming chmod = 0644
outgoing chmod = 0644
lock file = /var/lock/container6001.lock
 
[object6000]
max connections = 20
path = /srv/node/
read only = false
write only = false
list = yes
uid = swift
gid = swift
incoming chmod = 0644
outgoing chmod = 0644
lock file = /var/lock/object6000.lock
' > /etc/rsyncd.conf
```

For xinetd, need to bind rsync to storage replication network.

```
echo '
service rsync
{
    disable         = no
    port            = 873
    socket_type     = stream
    protocol        = tcp
    wait            = no
    user            = root
    group           = root
    groups          = yes
    server          = /usr/bin/rsync
    bind            = <storage-replication-network-ip>
    server_args     = --daemon
}
' > /etc/xinetd.d/rsync
```

Don't forget to replace proper ip address in config files (quick script in later section). Now start rsync

```
service xinetd restart
```

To test rsync connectivity. Same as the last swift post.

### Ring File

Create ring file and add devices. All regions share the same one ring file. The format is aware of storage local network and storage replication network.

```
swift-ring-builder object.builder add r<region>z<zone>-<storage-local-network-ip>:<storage-local-network-port>R<storage-replication-network-ip>:<storage-replication-network-port>/DEVICE <weight>
```

I only have one IP on each node, so you cannot see the difference.

```
cd /etc/swift
rm -f *.builder *.ring.gz backups/*.builder backups/*.ring.gz

swift-ring-builder object.builder create 9 3 1
swift-ring-builder object.builder add r1z1-10.224.147.166:6010R10.224.147.166:6000/sdb1 1
swift-ring-builder object.builder add r1z2-10.224.147.167:6010R10.224.147.167:6000/sdb1 1
swift-ring-builder object.builder add r1z3-10.224.147.168:6010R10.224.147.168:6000/sdb1 1
swift-ring-builder object.builder add r2z1-10.224.147.173:6010R10.224.147.173:6000/sdb1 1
swift-ring-builder object.builder add r2z2-10.224.147.174:6010R10.224.147.174:6000/sdb1 1

swift-ring-builder container.builder create 9 3 1
swift-ring-builder container.builder add r1z1-10.224.147.166:6011R10.224.147.166:6001/sdb1 1
swift-ring-builder container.builder add r1z2-10.224.147.167:6011R10.224.147.167:6001/sdb1 1
swift-ring-builder container.builder add r1z3-10.224.147.168:6011R10.224.147.168:6001/sdb1 1
swift-ring-builder container.builder add r2z1-10.224.147.173:6011R10.224.147.173:6001/sdb1 1
swift-ring-builder container.builder add r2z2-10.224.147.174:6011R10.224.147.174:6001/sdb1 1

swift-ring-builder account.builder create 9 3 1
swift-ring-builder account.builder add r1z1-10.224.147.166:6012R10.224.147.166:6002/sdb1 1
swift-ring-builder account.builder add r1z2-10.224.147.167:6012R10.224.147.167:6002/sdb1 1
swift-ring-builder account.builder add r1z3-10.224.147.168:6012R10.224.147.168:6002/sdb1 1
swift-ring-builder account.builder add r2z1-10.224.147.173:6012R10.224.147.173:6002/sdb1 1
swift-ring-builder account.builder add r2z2-10.224.147.174:6012R10.224.147.174:6002/sdb1 1

swift-ring-builder object.builder rebalance
swift-ring-builder container.builder rebalance
swift-ring-builder account.builder rebalance
```

### Swift Config

Swift global config remains the same.

```
echo '
# random unique strings that can never change (DO NOT LOSE). should remain secret and MUST NOT change
[swift-hash]
swift_hash_path_prefix = d567525c1f822093
swift_hash_path_suffix = 72103971ef596e63

# recommended set policy 0, even you dont use it
[storage-policy:0]
name = Policy-0
default = yes
' > /etc/swift/swift.conf
```

The proxy server config is here. Modifications are: added affinity setting which is different in regions, change memcached server list according to different regions.

You need to make sure users and tenants are equal between regions. I'm using tempauth here, which defines them in config file. But if you are using keystone, consider `mysqldump` dumping tables: project, user, role, and user_project_metadata.

```
echo '
[DEFAULT]
#bind_ip = 0.0.0.0   # listen to both storage local network and public network
bind_port = 8080
user = swift
worker = 32
log_facility = LOG_LOCAL1
eventlet_debug = true

#conn_timeout=3
 
[pipeline:main]
# for monitoring you can more add informant and recon. note that I dont use keystone here
pipeline = catch_errors gatekeeper healthcheck proxy-logging cache bulk tempurl slo dlo ratelimit crossdomain tempauth staticweb container-quotas account-quotas proxy-logging proxy-server

[filter:catch_errors]
use = egg:swift#catch_errors

[filter:healthcheck]
use = egg:swift#healthcheck

[filter:proxy-logging]
use = egg:swift#proxy_logging

[filter:bulk]
use = egg:swift#bulk

[filter:ratelimit]
use = egg:swift#ratelimit

[filter:crossdomain]
use = egg:swift#crossdomain

[filter:dlo]
use = egg:swift#dlo

[filter:slo]
use = egg:swift#slo

[filter:tempurl]
use = egg:swift#tempurl

[filter:tempauth]
use = egg:swift#tempauth
user_admin_admin = admin .admin .reseller_admin
user_test_tester = testing .admin
user_test2_tester2 = testing2 .admin
user_test_tester3 = testing3

[filter:staticweb]
use = egg:swift#staticweb

[filter:account-quotas]
use = egg:swift#account_quotas

[filter:container-quotas]
use = egg:swift#container_quotas

[filter:cache]
use = egg:swift#memcache
memcache_servers = <memcached-server-list>

[filter:gatekeeper]
use = egg:swift#gatekeeper

[app:proxy-server]
use = egg:swift#proxy
allow_account_management = true
account_autocreate = true

sorting_method = affinity
write_affinity_node_count = 2 * replicas
<affinity-settings>

' > /etc/swift/proxy-server.conf
```

Memcached server list in Region 1 and Region 2 are different. You should fill in the correct one in `<memcached-server-list>` in following config files.

```
# in Region 1
10.224.147.166:11211,10.224.147.167:11211,10.224.147.168:11211

# in Region 2
10.224.147.173:11211,10.224.147.174:11211
```

Different proxy server in different region has different affinity. Usually proxy loves the closer one. Choose correct one to fill into `<affinity-settings>`, according to your region. See doc: [here](https://github.com/openstack/swift/blob/master/etc/proxy-server.conf-sample) and [here](http://docs.openstack.org/developer/swift/admin_guide.html#write-affinity-and-write-affinity-node-count).

```
# in Region 1
read_affinity = r1=100
write_affinity= r1        # write to Region 1 but note that replicator will later carry objects across datacenters

# in Region 2
read_affinity = r2=100
write_affinity= r2
```

The object expirer config remains the same, except that you have to specify memcached server list according to region.

```
echo '
[DEFAULT]
# swift_dir = /etc/swift
user = swift
# You can specify default log routing here if you want:
log_name = object-expirer
log_facility = LOG_LOCAL6
log_level = INFO

[object-expirer]
interval = 300
# auto_create_account_prefix = .

[pipeline:main]
pipeline = catch_errors cache proxy-server

[app:proxy-server]
use = egg:swift#proxy

[filter:cache]
use = egg:swift#memcache
memcache_servers = <memcached-server-list>

[filter:catch_errors]
use = egg:swift#catch_errors
' > /etc/swift/object-expirer.conf
```

Configuration for non-replicator object/container/account services. Modifications include: delete all `[<*>-replicator]` sections.

```
mkdir /etc/swift/object-server
mkdir /etc/swift/container-server
mkdir /etc/swift/account-server

# the object server
echo '
[DEFAULT]
devices = /srv/node
mount_check = false
bind_ip = <storage-local-network-ip>
bind_port = 6010
workers = 1
user = swift
log_facility = LOG_LOCAL2
recon_cache_path = /var/cache/swift
eventlet_debug = true

[pipeline:main]
pipeline = recon healthcheck object-server

[app:object-server]
use = egg:swift#object

[filter:recon]
use = egg:swift#recon

[filter:healthcheck]
use = egg:swift#healthcheck

[object-updater]
concurrency = 2

[object-auditor]

' > /etc/swift/object-server/1.conf

# the container server
echo '
[DEFAULT]
devices = /srv/node
mount_check = false
disable_fallocate = true
bind_ip = <storage-local-network-ip>
bind_port = 6011
workers = 1
user = swift
log_facility = LOG_LOCAL2
recon_cache_path = /var/cache/swift
eventlet_debug = true
allow_versions = true

[pipeline:main]
pipeline = recon healthcheck container-server

[app:container-server]
use = egg:swift#container

[filter:recon]
use = egg:swift#recon

[filter:healthcheck]
use = egg:swift#healthcheck

[container-updater]
concurrency = 2

[container-auditor]

[container-sync]

' > /etc/swift/container-server/1.conf

# the account server
echo '
[DEFAULT]
devices = /srv/node/
mount_check = false
bind_ip = <storage-local-network-ip>
bind_port = 6012
workers = 1
user = swift
log_facility = LOG_LOCAL2
recon_cache_path = /var/cache/swift
eventlet_debug = true

[pipeline:main]
pipeline = recon healthcheck account-server

[app:account-server]
use = egg:swift#account

[filter:recon]
use = egg:swift#recon

[filter:healthcheck]
use = egg:swift#healthcheck

[account-auditor]

[account-reaper]

' > /etc/swift/account-server/1.conf
```

Configuration for replicator object/container/account services. Modifications include: bind to storage replication network, add "replication_server = true" in section `[app:<*>-server]`, delete all `[<*>-reaper]`, `[<*>-auditor]`, `[<*>-updater]`, `[container-sync]` sections.

```
mkdir /etc/swift/object-server
mkdir /etc/swift/container-server
mkdir /etc/swift/account-server

# the object server
echo '
[DEFAULT]
devices = /srv/node
mount_check = false
bind_ip = <storage-replication-network-ip>
bind_port = 6000
workers = 1
user = swift
log_facility = LOG_LOCAL2
recon_cache_path = /var/cache/swift
eventlet_debug = true

[pipeline:main]
pipeline = recon healthcheck object-server

[app:object-server]
use = egg:swift#object
replication_server = true

[filter:recon]
use = egg:swift#recon

[filter:healthcheck]
use = egg:swift#healthcheck

[object-replicator]
concurrency = 2
' > /etc/swift/object-server/2.conf

# the container server
echo '
[DEFAULT]
devices = /srv/node
mount_check = false
disable_fallocate = true
bind_ip = <storage-replication-network-ip>
bind_port = 6001
workers = 1
user = swift
log_facility = LOG_LOCAL2
recon_cache_path = /var/cache/swift
eventlet_debug = true
allow_versions = true

[pipeline:main]
pipeline = recon healthcheck container-server

[app:container-server]
use = egg:swift#container
replication_server = true

[filter:recon]
use = egg:swift#recon

[filter:healthcheck]
use = egg:swift#healthcheck

[container-replicator]
concurrency = 2
' > /etc/swift/container-server/2.conf

# the account server
echo '
[DEFAULT]
devices = /srv/node/
mount_check = false
bind_ip = <storage-replication-network-ip>
bind_port = 6002
workers = 1
user = swift
log_facility = LOG_LOCAL2
recon_cache_path = /var/cache/swift
eventlet_debug = true

[pipeline:main]
pipeline = recon healthcheck account-server

[app:account-server]
use = egg:swift#account
replication_server = true

[filter:recon]
use = egg:swift#recon

[filter:healthcheck]
use = egg:swift#healthcheck

[account-replicator]
concurrency = 2
' > /etc/swift/account-server/2.conf
```

### Synchronize Config

Copy config files and ring files to each node.

```
scp -r /etc/swift/* root@10.224.147.167:/etc/swift/
scp -r /etc/swift/* root@10.224.147.168:/etc/swift/

scp -r /etc/swift/* root@10.224.147.173:/etc/swift/
scp -r /etc/swift/* root@10.224.147.174:/etc/swift/
```

Set the permissions on each host

```
# on each host
chown -R swift:swift /etc/swift
chmod 640 /etc/swift/swift.conf
```

### Replace Placeholders In Config File

You need to replace `<storage-replication-network-ip>` and `<storage-local-network-ip>` placeholders in config files. Since I only have 1 ip addresses on each node, so I can replace them all as the host ip. Also, don't forget to replace memcached ip and port addresses, since we have 2 regions so 2 memcached clusters. Also the affinity settings in each region. Here is a quick script

```
# for rsync config. run below on each host
export IP_ADDR=$(ifconfig eth0 | grep -E "inet\s" | awk '{print $2}')

sed -i "s/<storage-replication-network-ip>/$IP_ADDR/" /etc/rsyncd.conf
sed -i "s/<storage-replication-network-ip>/$IP_ADDR/" /etc/xinetd.d/rsync
```

```
# for swift config. run below on each host
export IP_ADDR=$(ifconfig eth0 | grep -E "inet\s" | awk '{print $2}')

# in Region 1
export MEMCACHED_LIST='10.224.147.166:11211,10.224.147.167:11211,10.224.147.168:11211'
export AFFINITY_SETTINGS="read_affinity = r1=100\nwrite_affinity= r1"
# in Region 2
#export MEMCACHED_LIST='10.224.147.173:11211,10.224.147.174:11211'
#export AFFINITY_SETTINGS="read_affinity = r2=100\nwrite_affinity= r2"

# for swift config
for f in $(find /etc/swift -regex '.*\.conf'); do 
  sed -i "s/<storage-local-network-ip>/$IP_ADDR/" $f
done

for f in $(find /etc/swift -regex '.*\.conf'); do 
  sed -i "s/<storage-replication-network-ip>/$IP_ADDR/" $f
done

for f in $(find /etc/swift -regex '.*\.conf'); do 
  sed -i "s/<memcached-server-list>/$MEMCACHED_LIST/" $f
done

for f in $(find /etc/swift -regex '.*\.conf'); do 
  sed -i "s/<affinity-settings>/$AFFINITY_SETTINGS/" $f
done
```

## Swift Startup

On every host.

```
$ swift-init all start
swift-init all start
Starting container-updater...(/etc/swift/container-server/1.conf)
Starting container-updater...(/etc/swift/container-server/2.conf)
Starting account-auditor...(/etc/swift/account-server/1.conf)
Starting account-auditor...(/etc/swift/account-server/2.conf)
Starting object-replicator...(/etc/swift/object-server/1.conf)
Starting object-replicator...(/etc/swift/object-server/2.conf)
Starting container-sync...(/etc/swift/container-server/1.conf)
Starting container-sync...(/etc/swift/container-server/2.conf)
Starting container-replicator...(/etc/swift/container-server/1.conf)
Starting container-replicator...(/etc/swift/container-server/2.conf)
Starting object-auditor...(/etc/swift/object-server/1.conf)
Starting object-auditor...(/etc/swift/object-server/2.conf)
Starting object-expirer...(/etc/swift/object-expirer.conf)
Starting container-auditor...(/etc/swift/container-server/1.conf)
Starting container-auditor...(/etc/swift/container-server/2.conf)
Starting container-server...(/etc/swift/container-server/1.conf)
Starting container-server...(/etc/swift/container-server/2.conf)
Starting object-server...(/etc/swift/object-server/1.conf)
Starting object-server...(/etc/swift/object-server/2.conf)
Starting account-reaper...(/etc/swift/account-server/1.conf)
Starting account-reaper...(/etc/swift/account-server/2.conf)
Starting proxy-server...(/etc/swift/proxy-server.conf)
Starting account-replicator...(/etc/swift/account-server/1.conf)
Starting account-replicator...(/etc/swift/account-server/2.conf)
Starting object-updater...(/etc/swift/object-server/1.conf)
Starting object-updater...(/etc/swift/object-server/2.conf)
Unable to locate config for container-reconciler
Starting account-server...(/etc/swift/account-server/1.conf)
Starting account-server...(/etc/swift/account-server/2.conf)
```

You can see both 1.conf and 2.conf are used.

```
$ ps -ef|grep swift
swift    25801     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-updater /etc/swift/container-server/1.conf
swift    25803     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-account-auditor /etc/swift/account-server/1.conf
swift    25806     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-replicator /etc/swift/object-server/2.conf
swift    25807     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-sync /etc/swift/container-server/1.conf
swift    25811     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-replicator /etc/swift/container-server/2.conf
swift    25814     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-auditor /etc/swift/object-server/1.conf
swift    25822     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-expirer /etc/swift/object-expirer.conf
swift    25827     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-auditor /etc/swift/container-server/1.conf
swift    25832     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-server /etc/swift/container-server/1.conf
swift    25836     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-server /etc/swift/container-server/2.conf
swift    25840     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-server /etc/swift/object-server/1.conf
swift    25847     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-server /etc/swift/object-server/2.conf
swift    25851     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-account-reaper /etc/swift/account-server/1.conf
swift    25858     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-proxy-server /etc/swift/proxy-server.conf
swift    25869     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-account-replicator /etc/swift/account-server/2.conf
swift    25898     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-updater /etc/swift/object-server/1.conf
swift    25908     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-account-server /etc/swift/account-server/1.conf
swift    25914     1  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-account-server /etc/swift/account-server/2.conf
swift    25942 25832  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-server /etc/swift/container-server/1.conf
swift    25951 25847  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-server /etc/swift/object-server/2.conf
swift    25959 25836  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-container-server /etc/swift/container-server/2.conf
swift    25977 25840  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-object-server /etc/swift/object-server/1.conf
swift    25983 25858  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-proxy-server /etc/swift/proxy-server.conf
swift    25984 25858  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-proxy-server /etc/swift/proxy-server.conf
swift    25991 25908  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-account-server /etc/swift/account-server/1.conf
swift    25992 25914  0 04:40 ?        00:00:00 /usr/bin/python /usr/bin/swift-account-server /etc/swift/account-server/2.conf
root     26219 14315  0 04:43 pts/1    00:00:00 grep --color=auto swift
```

Both the 600* ports and 601* ports are being listened. It means non-replication and replicaiton services are both running. 

```
$ netstat -nlp | grep python
tcp        0      0 10.224.147.166:6010     0.0.0.0:*               LISTEN      25840/python        
tcp        0      0 10.224.147.166:6011     0.0.0.0:*               LISTEN      25832/python        
tcp        0      0 10.224.147.166:6012     0.0.0.0:*               LISTEN      25908/python        
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN      25858/python        
tcp        0      0 10.224.147.166:6000     0.0.0.0:*               LISTEN      25847/python        
tcp        0      0 10.224.147.166:6001     0.0.0.0:*               LISTEN      25836/python        
tcp        0      0 10.224.147.166:6002     0.0.0.0:*               LISTEN      25914/python
```

## Verify Operation

Let's first upload some objects.

```
# execute on 10.224.147.166
cd ~

# show swift status 
swift -A http://10.224.147.168:8080/auth/v1.0 -U admin:admin -K admin stat

# create random object file
dd if=/dev/urandom of=./obj1.dat bs=512 count=2048
dd if=/dev/urandom of=./obj2.dat bs=512 count=2048

# update objects from different proxy
swift -A http://10.224.147.168:8080/auth/v1.0 -U admin:admin -K admin upload container1 obj1.dat 
swift -A http://10.224.147.167:8080/auth/v1.0 -U admin:admin -K admin upload container1 obj2.dat 
swift -A http://10.224.147.168:8080/auth/v1.0 -U admin:admin -K admin upload container2 obj1.dat 
```

Print the md5 sum.

```
# execute on 10.224.147.166
$ echo obj1.dat | md5sum
072964ee04eb1f26cd5e6496d862fdb2  -
$ echo obj2.dat | md5sum
b194d835311f2868ce4065b00def6204  -
```

Verify object access in local region and other regions

```
# execute on 10.224.147.167
$ swift -A http://10.224.147.166:8080/auth/v1.0 -U admin:admin -K admin download container1 obj2.dat
$ swift -A http://10.224.147.168:8080/auth/v1.0 -U admin:admin -K admin download container2 obj1.dat

# execute on 10.224.147.174
$ swift -A http://10.224.147.166:8080/auth/v1.0 -U admin:admin -K admin download container1 obj2.dat
$ swift -A http://10.224.147.168:8080/auth/v1.0 -U admin:admin -K admin download container2 obj1.dat
$ echo obj1.dat | md5sum
072964ee04eb1f26cd5e6496d862fdb2  -
$ echo obj2.dat | md5sum
b194d835311f2868ce4065b00def6204  -
```

To see object replica distribution

```
# on region 1, 10.224.147.166
$ ls /srv/node/sdb1/objects/
34
# on region 1, 10.224.147.167
$ ls /srv/node/sdb1/objects/
143  374
# on region 1, 10.224.147.168
$ ls /srv/node/sdb1/objects/
143  34  374

# on region 2, 10.224.147.173
$ ls /srv/node/sdb1/objects/
34
# on region 2, 10.224.147.174
$ ls /srv/node/sdb1/objects/
143  374
```

You can see objects replicas are distributed across regions (datacenters).



