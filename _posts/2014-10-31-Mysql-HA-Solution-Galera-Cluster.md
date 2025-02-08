---
layout: post
title: "Mysql HA Solution Galera Cluster"
tagline : "Mysql HA Solution Galera Cluster"
description: "Mysql HA Solution Galera Cluster"
category: "Database"
tags: [mysql, HA, mariadb, galera]
---
{% include JB/setup %}

In past time we use [Mysql-MMM](http://mysql-mmm.org/mysql-mmm.html) (Master-Master Replication Manager). Masters and slaves are separated for write and read. VIP for master active/active, proxy for slave loadbalance.

Guides: 
  
  * <http://blog.csdn.net/yongcto/article/details/12528423>
  * <http://navyaijm.blog.51cto.com/4647068/1230674>

New emerging solution is [MariaDB Galera Cluster](https://mariadb.com/kb/en/mariadb/documentation/replication/galera/what-is-mariadb-galera-cluster/). Mirantis is using it in Openstack Fuel. 

Mysql servers forms a cluster where all servers are synchronized. Each node can be used to write or read. Transaction returns only after others is synchronized with the writer. It uses wsrep to replicate transaction on row level. A good practice is to use haproxy and desinate only one node as writer, leaving others as reader (all node writeable is prone to deadlock). To avoid brain split, minimum of 3 nodes is recommended. If you have *even number* of nodes, consider installing [Galera Arbitrator](http://galeracluster.com/documentation-webpages/arbitrator.html) (refer to [this](http://nouvellesidees.info/blog/mysql-cluster-with-galera/)).

Advantages over MMM:
  
  * <http://www.oschina.net/translate/from-mysql-mmm-to-mariadb-galera-cluster-a-high-availability-makeover?print>
  * <http://634871.blog.51cto.com/624871/1350082>

Guides: 

  * <http://matthewcasperson.blogspot.com/2013/07/setting-up-galera-cluster-in-centos-6.html>
  * <https://mariadb.com/kb/en/mariadb/documentation/replication/galera/getting-started-with-mariadb-galera-cluster/>
  * <http://www.percona.com/live/mysql-conference-2012/sessions/galera-synchronous-multi-master-replication-mysql>

## Troubleshooting

__1. Can't grep find local ip address__

The second MariaDB server failed to start:

```
mysqld --wsrep_cluster_address=gcomm://10.224.147.166 --user=mysql --wsrep_provider=/usr/lib64/galera/libgalera_smm.so --wsrep_sst_auth=root:password
```

The error output is

```
141031  7:12:13 [ERROR] WSREP: Failed to read output of: '/sbin/ifconfig | grep -E '^[[:space:]]+inet addr:' | grep -m1 -v 'inet addr:127' | sed 's/:/ /' | awk '{ print $3 }''
```

Reason is "localization problem", refer to <https://mariadb.atlassian.net/browse/MDEV-4163>. I have to provide local ip address in above command:

```
mysqld --wsrep_cluster_address=gcomm://10.224.147.166 --wsrep_sst_receive_address=10.224.147.167 --user=mysql --wsrep_provider=/usr/lib64/galera/libgalera_smm.so --wsrep_sst_auth=root:password
```

__2. Full restart of the cluster__

If one node is down and you want to restart it (cluster is still alive), connect it to any other node. E.g host 1

```
mysqld --wsrep_cluster_address=gcomm://10.224.147.167 --user=mysql --wsrep_provider=/usr/lib64/galera/libgalera_smm.so --wsrep_sst_auth=root:password
```

Actually you can write config in /etc/my.cnf.

```
[mariadb]
wsrep_cluster_address=gcomm://10.224.147.167
wsrep_provider=/usr/lib64/galera/libgalera_smm.so
wsrep_sst_auth=root:password
wsrep_node_address=10.224.147.166
log-error=/var/log/mysql.log
```

And use `service mysql restart`.

If the whole cluster is down, given you have the above /etc/my.cnf, restart by

```
mysqld --wsrep_cluster_address=gcomm:// --user=mysql
```

This will create a new cluster.
