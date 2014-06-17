---
layout: post
title: "Logstash Elasticsearch Kibana Investigation"
tagline : " Get to know LEK"
description: "Openstack allinone on Ubuntu with Ceilometer"
category: "elasticsearch"
tags: [cloud, openstack, search, logging]
---
{% include JB/setup %}

## Investigation Guideline

Logstash+ElasticSearch+Kibana (LEK) consists a popular and versatile log collecting and searching platform. During the investigation, I try to address below problems.

* **Design production-ready solution**
    * HA solution for each component
    * Clustering, sharding and scaling
    * Security, authentication & authorization (AA), encryption
    * Performance benchmarking
    * Small scale POC deployment

* **Find integration possibilities with Openstack**
    * Swift be used to store log or index?
    * Keystone be used for AA?
    * Ceilometer be for log collecting and storing?
    * Meniscus: Openstack logging as a Service (LAAS)?

* **Care for business integration needs**
    * Per tenant AA. View log/query by tenant permission
    * Multi-tenant support
        * Service \* Server Group (Server Type) \* Per Server \* Log Type 
    * Must we install an agent on each production server?    

## Architecture

LEK are lightweight and relatively free to architect. Various materials provide ways to do it.

* Basic Architectures
    * Shipper -> (Logstash Receiver ->) Redis -> Logstash Indexer -> Elasticsearch (cluster)
        * Shipper: run on production server. Read local log, send to remote. Can use Logstash, Lumberjack, beaver and so on.    
          \[<http://cookbook.logstash.net/recipes/log-shippers/>\]
        * Logstash Receiver: receive log from shipper and put into Redis. Most shipper can send directly to Redis, except Lumberjack.
        * Redis: acts as the queue. This role is also called broker. You can also use AMPQ.
        * Logstash Indexer: transform log format. Called 'indexer' but actually elasticsearch is who does indexing.
        * How Logstash transform log - grok - structure decompositable regex    
          \[<http://semicomplete.com/presentations/logstash-puppetconf-2012/#/38>\]
        * ElasticSearch: indexing and search. Mature for HA and scaling cluster.
    * Offical's very basic guide    
       \[<http://logstash.net/docs/1.1.0/tutorials/getting-started-centralized>\]
        * Logstash supports all kinds of input/filter/output.
        * Logstash support input from rsyslog/collectd/log4j. You can use server's default logging.    
          \[<http://logstash.net/docs/1.4.1/>\]
    * Collect & visualize your logs with Logstash, Elasticsearch & Redis    
      \[<http://michael.bouvy.net/blog/en/2013/11/19/collect-visualize-your-logs-logstash-elasticsearch-redis-kibana/>\]
        * Nice architecture picture
        * Suggested to use Lumberjack shipper
    * Centralizing Logs with Lumberjack, Logstash, and Elasticsearch    
      \[<http://www.vmdoh.com/blog/centralizing-logs-lumberjack-logstash-and-elasticsearch>\]
        * Shipping with Lumberjack (logstash-forwarder)
        * Another shipper option Rsyslog
    * Centralized logging system based on Logstash-forwarder+Logstash+RabbitMQ+ElasticSearch+Kibana    
       \[<http://jakege.blogspot.com/2014/04/centralized-logging-system-based-on.html>\]
        * Use RabbitMQ rather than Redis for queuing
        * Pull from Lumberjack port 5000

* A mail thread that has production Logstash setup to refer to    
  \[<https://groups.google.com/forum/#!topic/logstash-users/-392l9LHa8Q>\]
    * Provided with detail config file
    * 2 Redis server in failover mode
    * 5 Logstash indexers
    * Config exists ERRORs. Read through the thread to know it.

* LogStach HA Cluster Cookbook    
  \[<http://www.masteringthecloud.com/2014/01/logstash-cluster-cookbook.html>\]
    * HAProxy load balancing and fail-over
    * 3 Redis to do load balance
    * Issue: tied Redis, Logstash and Elasticsearch on one server.
    * Problem: Fail of one Redis server may lose log entries in it.

* My designed architecture
  * Use Lumberjack as log shipper. Reason see below shipper comparasion.
  * Use Lumberjack's load balancing and fail-over. So no dedicated load balancer device needed.
  * Multiple Logstash to demo scaling of it.
  * Redis acts as queue. Use master-slave mode for HA. Multiple Redis master-slave group to distributed load.
  * Elasticsearch cluster to store and index log and do searching. Kibana as front-end web server.

![My designed LEK architecture picture](/images/logstash-lek-demo-arch.png "My designed LEK architecture")

* Other concerns
    * In above architecture, we lack a persistent log storage location. Elasticsearch cares for searching but not recommended as permanent log storage.
    * Hadoop/HDFS is usually recommended for log storing.    
       \[<http://blog.mgm-tp.com/2010/04/hadoop-log-management-part2/>\]
    * We lack AA in above architecture. May need to add a proxy server on top of Kibana.
    * Meniscus - Openstack logging as a service. This is another log searching framework, using Elasticsarch and Kibana, but discarded Logstash.    
       \[<http://developer.rackspace.com/blog/project-meniscus-an-update.html>\]
        * Can we use/borrow from that?

Some materials to start learning LEK

* How to set up tutorial and some tips.    
  \[<http://www.cnblogs.com/buzzlight/p/logstash_elasticsearch_kibana_log.html>\]
* Logstash, ElasticSearch, Kibana Intro    
  \[<https://speakerdeck.com/elasticsearch/using-elasticsearch-logstash-and-kibana-to-create-realtime-dashboards>\]
* A comprehensive bibliography for ElasticSearch    
  \[<http://blog.csdn.net/gaoyingju/article/details/23750563#1536434-tsina-1-19369-66a1f5d8f89e9ad52626f6f40fdeadaa>\]

## Shipper Comparasion

Logstash provides many shippers to choose from. Commonly suggested shippers and comparasion are listed blow.

* Logstash-Forwarder (Lumberjack) \[**Recommended**\]
    * \[**good**\] Written in go, the fastest shipper, consume little resource    
       \[<http://www.vmdoh.com/blog/centralizing-logs-lumberjack-logstash-and-elasticsearch>\]
    * \[**good**\] Compressed transmitting    
       \[<https://github.com/elasticsearch/logstash-forwarder>\]
    * \[**good**\] OpenSSL to auth and encrypt transmission    
       \[<https://github.com/elasticsearch/logstash-forwarder>\]
    * \[**bad**\] Cannot send directly to Redis. Must use extra logstash to receive its output.    
       \[<https://github.com/elasticsearch/logstash-forwarder/issues/18>\]
    * \[**good**\] Output (push) to logstash, with load balancing and fail-over    
       \[<https://github.com/elasticsearch/logstash-forwarder>\]
    * \[**good**\] After restarted, will resume to last position in log file. Won't start-over.    
       \[<https://groups.google.com/forum/#!topic/logstash-users/Kqd8Wb5y-V8>\]    
       \[<https://github.com/elasticsearch/logstash-forwarder/blob/master/prospector.go>\]

* Logstash Shipper
    * \[**bad**\] Written in java, may consume too many resource.    
       \[<http://www.vmdoh.com/blog/centralizing-logs-lumberjack-logstash-and-elasticsearch>\]
    * \[**good**\] Can round-robin output to a list of Redis hosts, for load balancing and fail-over.    
       \[<http://serverfault.com/questions/459303/scaling-logstash-with-redis-elasticsearch>\]    
       \[<https://groups.google.com/forum/#!searchin/logstash-users/availability/logstash-users/8Km9VFqapig/w9WEaN2K3E8J>\]
    * \[**good**\] After restarted, will resume to last position in log file. Won't start-over.    
       \[<https://groups.google.com/forum/#!topic/logstash-users/Kqd8Wb5y-V8>\]

* Beaver Shipper
    * Written in python
    * \[**good**\] SSH tunneling to secure transmission.    
       \[<http://beaver.readthedocs.org/en/latest/user/usage.html#ssh-tunneling-support>\]
    * \[**good**\] Use push model. Push to Redis directly.    
       \[<https://github.com/josegonzalez/beaver/blob/master/docs/user/usage.rst>\]
    * \[**bad**\] Push model but seems cannot output a list of Redis hosts. So no load balancing and fail-over.    
       \[<https://github.com/josegonzalez/beaver/blob/master/docs/user/usage.rst>\]
        * Modify the code to add round-robin feature. Or
        * Add our own load balancing device to enhance this
    * \[**bad**\] After restarted, will beaver resume to last position in log file? Won't it start-over? Seems not implemented.    
       \[<https://groups.google.com/forum/#!topic/logstash-users/Kqd8Wb5y-V8>\]    
       \[<https://github.com/josegonzalez/beaver/issues/6>\]

Not only can you use Logstash related shipper. Logstash accepts input from syslog/rsyslog/collectd/log4j, 
    * This means you may not need to install a shipper on each server. Use syslog/log4j ...
    * For what input types are supported    
      \[<http://logstash.net/docs/1.4.1/>\]

## High Availability

Basics.

* Logstash pipeline and blocking.    
  \[<http://logstash.net/docs/1.4.0/life-of-an-event>\]
    * Logstash queue log entry in it, called pipeline.
    * If an output is failing, the output thread will wait until this output is healthy again. So won't lose data.    
       \[<https://groups.google.com/forum/#!topic/logstash-users/jwGHb00KfT8>\]
    * A full queue in pipeline will cause blocking. Thus finally blocks input end.
    * Most shipper remember last position in log file and resume on restart. See above shipper comparasion section.    
       \[<https://groups.google.com/forum/#!topic/logstash-users/Kqd8Wb5y-V8>\]

What if Logstash shipper crashed?

* Can use monitd to watch it and restart.
* Most shipper remember last position in log file and resume on restart. See above shipper comparasion section.    
  \[<https://groups.google.com/forum/#!topic/logstash-users/Kqd8Wb5y-V8>\]
    * But there is **edge condition**. If shipper crashed, then log rotated, then shipper restarted. This may lose log entries.
    * Shipper has queue inside. Crashing may **lose the queue**. How shipper handle queue loss may result in log lose or send-twice.

What if Logstash shipper, or one of Logstash, get stucking forever?

* May need to combined with "Monitoring Logstash itself"
* Suggesting check timestamp of last document to know 'loggign'    
  \[<https://groups.google.com/forum/#!topic/logstash-users/jwGHb00KfT8>\]

Monitoring Logstash itself?

* Few material relates to this issue
* A script for monitoring and use document's timestamp to know 'lagging'    
  \[<https://groups.google.com/forum/#!topic/logstash-users/Z9WR7CJ0KRw>\]
* Send heatbeat and metric of Logstash via JMX.    
  \[<https://groups.google.com/forum/#!topic/logstash-users/nBbQ-jXfjgI>\]
    * It's only prototype and murders performance

What if Logstash receiver, if we used it, crashed?

* Monitd to watch it restart
* Shipper can use load balancing and failover to send to other Logstash receiver. See above shipper comparasion section.

What if the Redis, acting as the queue, crashed?

* Use multiple Redis, event no master-slave replication, can ensure log keep flowing. But log entries in queue may lose.    
  \[<http://www.masteringthecloud.com/2014/01/logstash-cluster-cookbook.html>\]
* Use RabbitMQ instead of Reddis, as the queue. But many complains RabbitMQ is slow and awful to use.    
  \[<https://groups.google.com/forum/#!topic/logstash-users/aSAlAHmyuT8>\]    
  \[<https://groups.google.com/forum/#!topic/logstash-users/lvuG7UGZwVU>\]    
  \[<https://twitter.com/jordansissel/status/302294195945738240>\]
* Redis HA solutions
    * Redis Sentinel \[**Recommended**\]    
       \[<http://redis.io/topics/sentinel>\]
       * Master slave replication. Monitoring and auto failover.
       * If master crashed before replicates to slave, **may sill lose data**
    * Redis Cluster    
       \[<http://redis.io/topics/cluster-tutorial>\]
       * Shipped in Redis 3.0.0, still beta.
       * cluster = ( 1 master + n slave (replica) ) * m (hash sharding)
       * Master slave replication. Monitoring and auto failover.
       * Hash sharding to do load balancing.
       * If master crashed before replicates to slave, **may sill lose data**
    * Other earlier and simpler solutions    
       \[<http://afei2.sinaapp.com/?p=360>\]

What if Logstash indexer crashed?

* Monitd to watch it and restart.
* Log entries are queued in Redis, won't lose.

What if ElasticSearch crashed?

* ElasticSearch has mature clusting, HA and recovery mechanism.    
  \[<http://spinscale.github.io/elasticsearch/2012-03-jugm.html#/8>\]    
  \[<http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/_coping_with_failure.html>\]

## Performance & Scaling

Logstash is written in java and ruby, will there be performance problems?

* Many suggest Logstash jvm consume too much server resource. Use Lumberjack as shipper instead.    
  \[<http://michael.bouvy.net/blog/en/2013/11/19/collect-visualize-your-logs-logstash-elasticsearch-redis-kibana/>\]    
  \[<http://michael.bouvy.net/blog/en/2013/12/06/use-lumberjack-logstash-forwarder-to-forward-logs-logstash/>\]
* Openstack Logging as a Service - Meniscus, doesn't use LogStash    
  \[<http://developer.rackspace.com/blog/project-meniscus-an-update.html>\]
    * - "Internal testing by our operations team found that it didn’t handle certain loads"
    * - "Second, because the Project Meniscus team has a goal of producing a solution that can handle massive amounts of data (two terabytes per day) and be a project that OpenStack can use, "
* Issues that complaining about performance    
  \[<https://logstash.jira.com/browse/LOGSTASH-1771>\]
* More Issues that complaining about performance    
  \[<https://logstash.jira.com/browse/LOGSTASH-480?jql=text%20~%20%22performance%22>\]

But, what I have not mentioned above is that there are still a lot that use Logstash to handle greate load in production. 

* To see it, search the Logstash mail archive or see below Practice section.     
  \[<https://groups.google.com/forum/#!forum/logstash-users>\]
* Even if Logstash was slow, you can scale it. Usually the bottle neck is ElasticSearch.
* My suggestion is, Logstash is good but **replace shipper to, e.g. Lumberjack**.

Redis scaling solution.

* Redis Cluster. It has been mentioned above.
* Use multiple Redis server for load balancing. You can add a load balancer device before Redis:    
  \[<http://www.masteringthecloud.com/2014/01/logstash-cluster-cookbook.html>\]
  Or use Logstash shipper's load balancing feature (see shipper comparasion section):    
  \[<http://serverfault.com/questions/459303/scaling-logstash-with-redis-elasticsearch>\]
* You can use scaling with master-slave replication together for HA.

Scaling ElasticSearch

* ElasticSearch is designed distributed and super easy to scale.
* It can evey do auto node discover.    
  \[<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-discovery-zen.html>\]
* - "After 17 years in this industry I've never seen anything scale horizontally as easy as ElasticSearch"    
  \[<http://serverfault.com/questions/459303/scaling-logstash-with-redis-elasticsearch>\]

Performance benchmarks.

* Logstash 1.1.x transport performance    
  \[<https://twitter.com/jordansissel/status/302294195945738240>\]
  * Used Logstash 1.1.x, but now it is 1.4.x
  * Redis, in batch mode, yields very good results.
  * RabbitMQ is slow.
  * Lumberjack is really fast.
* Logstash performance testing    
  \[<https://gist.github.com/paulczar/4513552>\]
* Elasticsearch+logstash perf exploration    
  \[<https://github.com/jordansissel/experiments/tree/master/elasticsearch/perf#readme>\]
* ElasticSearch - How many shards?    
  \[<http://blog.trifork.com/2014/01/07/elasticsearch-how-many-shards/>\]
    * From graph: it is strange that, with more shards, elastisearch gets slower
    * Shards are not free, they add overheads.

Performance tuning tips.

* Use Lumberjack as log shipper, it is really fast, and has a lot of features.
* Change Logstash thread count. On default it may have only one thread.    
  \[<https://logstash.jira.com/browse/LOGSTASH-480>\]
* Tips in a LEK setup tutorial    
  \[<http://www.cnblogs.com/buzzlight/p/logstash_elasticsearch_kibana_log.html>\]
* Tips in an ElasticSearch material summary    
  \[<http://blog.csdn.net/gaoyingju/article/details/23750563#1536434-tsina-1-19369-66a1f5d8f89e9ad52626f6f40fdeadaa>\]
* ElasticSearch and Logstash Tuning    
  \[<http://jablonskis.org/2013/elasticsearch-and-logstash-tuning/index.html>\]

## Security

Protect log transimission 

* Lumberjack log shipper supports OpenSSL authentication and encrpytion    
  \[<https://github.com/elasticsearch/logstash-forwarder>\]
* Beaver log shipper supports ssh tunneling    
  \[<http://beaver.readthedocs.org/en/latest/user/usage.html#ssh-tunneling-support>\]

Kibana authentication & authorization

* Use authenticatioin for Kibana3 setup    
  \[<https://groups.google.com/forum/#!topic/logstash-users/XeDfZcVRdsA>\]
* One approach is to authenticate by web server (nginx, apache)    
  \[<https://github.com/elasticsearch/kibana/blob/master/sample/nginx.conf>\]
* Another approach is to use code addons
    * Add authentication to kibana3 and allow users to view only thier logs.    
       \[<https://github.com/christian-marie/kibana3_auth>\]
    * Another thread discussing about this    
       \[<http://stackoverflow.com/questions/19867663/how-and-where-to-implement-basic-authentication-in-kibana-3>\]
* The third approach is to use proxy to hide Kinaba
    * Kibana-authentication-proxy    
       \[<https://github.com/fangli/kibana-authentication-proxy>\]

ElastiSearch authentication & authorization

* The basic idea is - "After a number of discussions on the ElasticSearch mailing list, I've discovered that the current solution is to host ElasticSearch behind another application layer and then to secure that layer."    
  \[<http://stackoverflow.com/questions/4960298/how-to-secure-an-internet-facing-elastic-search-implementation-in-a-shared-hosti>\]
    * So, use Kibana or a proxy
* Use a proxy    
  \[<http://stackoverflow.com/questions/9956062/authentication-in-elasticsearch>\]
* Another approach, replace embedded http server to jetty, so that jetty can use SSL and authentication.    
  \[<http://stackoverflow.com/questions/4960298/how-to-secure-an-internet-facing-elastic-search-implementation-in-a-shared-hosti>\]
* Yet another approach, use 3rd pary plugin. E.g. Elasticsearch-security-plugin    
  \[<http://stackoverflow.com/questions/9956062/authentication-in-elasticsearch>\]    
  \[<https://github.com/salyh/elasticsearch-security-plugin>\]
* But the common way, authenticate through Kibana

Data encryption.

* Encrypting ElasticSearch index
    * Mail threads discussing about it    
       \[<http://elasticsearch-users.115913.n3.nabble.com/Enabling-encrypted-indexes-td4035771.html>\]
    * No feature in ElasticSearch. You may use full disk encryption.
    * ElasticSearch also transmits data unencrypted over the wire between nodes.
    * "Encrypting every piece of data within an ES cluster is way too expensive."

Others & Tutorials

* A More Secure LogStash Install    
  \[<http://sphughes.com/2012/01/01/a-more-secure-logstash-install/>\]
    * Focusing on how to securily install them, rather than AA or encryption.
* Securing Elasticsearch / Kibana with nginx    
  \[<http://www.ragingcomputer.com/2014/02/securing-elasticsearch-kibana-with-nginx>\]
* Securing Your Elasticsearch Cluster - A Brief Overview of Running Elasticsearch Securely    
  \[<https://www.found.no/foundation/elasticsearch-security/>\]

## Maintainability

ElasticSearch monitoring.

* ElasticSearch has a lot of monitoring plugins    
  \[<http://www.elasticsearch.org/guide/en/elasticsearch/client/community/current/health.html>\]
* ElasticHQ is one the most recommended    
  \[<http://www.elastichq.org>\]    
  \[<http://www.cnblogs.com/buzzlight/p/logstash_elasticsearch_kibana_log.html>\]
    * License: Apache 2.0
    * features: monitoring and operate, indices management, no install & run in browser    
       \[<http://www.elastichq.org/features.html>\]

Logstash monitoring.

* see section "Monitoring Logstash itself?"

Deployment automation.

* LogStash puppet    
  \[<http://cookbook.logstash.net/recipes/puppet-modules/>\]

## LEK Practices

See how other people are using LEK log searching platform.

* Using elasticsearch and logstash to serve billions of searchable events for customers    
  \[<http://www.elasticsearch.org/blog/using-elasticsearch-and-logstash-to-serve-billions-of-searchable-events-for-customers/>\]
    * Billions, but for mail
* Production env configurations    
  \[<https://groups.google.com/forum/#!topic/logstash-users/Yj397MdAD74>\]
* Enterprise logstash/broker/kibana3/ setup    
  \[<https://groups.google.com/forum/#!topic/logstash-users/p-rEw6XpucM>\]
* Logstash best practices and configuration for load distribution    
  \[<https://groups.google.com/forum/#!topic/logstash-users/hHXJz1upk9E>\]
* Logstash configuration best practices    
  \[<http://stackoverflow.com/questions/22257956/logstash-configuration-best-practices>\]
* Our Experience of Creating Large Scale Log Search System Using ElasticSearch    
  \[<http://architects.dzone.com/articles/our-experience-creating-large>\]
* Rsyslog + Logstash in failover scenario    
  \[<https://groups.google.com/forum/#!topic/logstash-users/P8mTZaFGGqE>\]
* How is the scalability of logstash    
  \[<https://groups.google.com/forum/#!topic/logstash-users/k9QxzDl7_6I>\]
* Implementation with High Availability/Load Balancing    
  \[<https://groups.google.com/forum/#!topic/logstash-users/aSAlAHmyuT8>\]
* Problems scaling logstash redis and elasticsearch for 3-4 million log events per hour    
  \[<https://groups.google.com/forum/#!topic/logstash-users/-392l9LHa8Q>\]

## Openstack Integration

Swift to store log or index?

* If used as queue, Swift seems not appropriate
* If used to store index, ElastiSearch only supports filesystem/memory to store index    
  \[<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/index-modules-store.html>\]
* If used as permanent log storage, Haddop/HDFS is somehow more popular.

Ceilometer for log collecting and storing?

* Its data is organized for metric and samples, seems not the most appropriate
* Ceilometer use MongoDB. Is it suite for queuing log (Reddis?) or storing log (Hadoop)? 
* Can collect from collectd, but what about syslog or log4j? If we use Logstash to ship log, then what becomes better?
* A Blueprint: using ceilometer as log storage + elasticsearch    
  \[<https://blueprints.launchpad.net/ceilometer/+spec/elasticsearch-driver>\]
    * More info about this BP (mail threads)    
       \[<https://www.mail-archive.com/openstack-dev@lists.openstack.org/msg04565.html>\]    
       \[<http://lists.openstack.org/pipermail/openstack-dev/2013-September/015657.html>\]
    * Meniscus also mentioned a design goal that: "Provide common sinks for already existing systems such as Ceilometer"    
       \[<https://github.com/ProjectMeniscus/meniscus>\]
    * In above mail threads Ceilometer event/notification system is also mentioned.    
       \[<http://docs.openstack.org/developer/ceilometer/events.html>\]
    * However, the BP and mail threads seem inactive nowadays.

Figuring out how to integrate Openstack is still a challenge now.

## Business Integration

Authentication & Authorization, with each user can only view log in his/her tenant/service group.

* Keystone and add proxy to Kinaba

Must we install an agent for each production server?

* Logstash can use default log shipper such as syslog, log4j. In this case we don't need to add new shipper to servers.
* If we need to install Lumberjack, for performance needs, then we need to install it on each server.

Multi-tenant support.

* Logstash multi-tenant support discussion on maillist.    
  \[<https://groups.google.com/forum/#!topic/logstash-users/qiptMyaMqWs>\]
    * Basically, we add tag in log entry to separate them. 
    * Each server installs a Logstash, where tag is acquired.
    * Use puppet for logstash's conf on each server.
* Meniscus decides to implement multi-tenant support. We can borrow from it.    
  \[<https://github.com/ProjectMeniscus/meniscus/wiki/Tenant-Identification-Flow>\]    
  \[<https://github.com/ProjectMeniscus/meniscus/wiki/Tenant-API>\]    
  \[<https://github.com/ProjectMeniscus/meniscus/wiki/Research-on-Elasticsearch-Templates>\]

There may need a unified log format.

* My draft log format
    * Identity part 
        * service name, group, component, code location, 
        * server, ip, process
        * level, timestamp, 
        * session id, (request id)
    * Content part
        * descriptive words
        * stack trace
    * Tenant info is taken as service name or group. User can only access server's log if has permission.
