---
layout: post
title: "Play with RabbitMQ"
tagline : "Config Postfix Mail Server"
description: "Config Postfix Mail Server"
category: "mail"
tags: [mail, postfix]
---
{% include JB/setup %}

Overall, RabbitMQ and the AMQP protocol is easy to understand and config. RabbitMQ official site provides helpful guide and examples. Below is a quick script notes of how I played. Format it to a better article if had time.

```
1. tryout rabbitmq for openstack
    1. rabbitmq HA
        single node, durable queue (write on disk, but no fsync, so still can lose)
        cluster mode, no mirror message, but two rabbitmqs 
                      mirror the messages

        openstack nova:
            rabbit_ha_queues=True/False – to turn queue mirroring on.

    2. following rabbitmq guide on openstack ha manual:
       http://docs.openstack.org/high-availability-guide/high-availability-guide.pdf

       following https://www.rabbitmq.com/clustering.html:

        1. when joining a cluster, must use hostname

            [root@bigzhao-openstack-03 ~]# rabbitmqctl join_cluster rabbit@10.224.147.166
            Clustering node 'rabbit@bigzhao-openstack-03' with 'rabbit@10.224.147.166' ...
            Error: {cannot_discover_cluster,"The nodes provided are either offline or not running"}
            [root@bigzhao-openstack-03 ~]# rabbitmqctl join_cluster rabbit@bigzhao-openstack-01
            Clustering node 'rabbit@bigzhao-openstack-03' with 'rabbit@bigzhao-openstack-01' ...
            ...done.
            [root@bigzhao-openstack-03 ~]# 

        n. try out
            0. user and permission
               http://www.rabbitmq.com/man/rabbitmqctl.1.man.html#Access%20control
               rabbitmqctl add_user ...
               rabbitmqctl set_permissions ...
               rabbitmqctl set_user_tags ...
            0.5. connections
               import pika
               connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.224.147.166', credentials=pika.PlainCredentials('test', 'password')))
               channel = connection.channel()
            1. create and list queues
                queue_declare(), exchange_declare()
            2. mirror & kill on rabbit
                done by kill -9 ...
            3. topics & message topic
               http://www.rabbitmq.com/tutorials/tutorial-five-python.html
            4. the web ui management plugin
               https://www.rabbitmq.com/management.html
                  browser open: 
                      http://10.224.147.166:15672/
                  why I don't have rabbitmq-plugins
                    http://stackoverflow.com/questions/8548983/how-to-install-rabbitmq-management-plugin-rabbitmq-plugins
                      ls /usr/lib/rabbitmq/lib/rabbitmq_server-3.1.5/sbin/rabbitmq-plugins
                      /usr/lib/rabbitmq/lib/rabbitmq_server-3.1.5/sbin/rabbitmq-plugins enable rabbitmq_management
                      # to restart
                      rabbitmqctl stop
                      rabbitmq-server -detached
                      rabbitmqctl start_app
                      rabbitmqctl cluster_status
                  how to see rabbitmq version: rabbitmqctl status
                    http://stackoverflow.com/questions/7593269/verify-version-of-rabbitmq
    
    3. rabbitmq concepts
       http://abhishek-tiwari.com/post/amqp-rabbitmq-and-celery-a-visual-guide-for-dummies
       https://www.rabbitmq.com/tutorials/amqp-concepts.html
       what is virtualhost
         http://blog.163.com/sky20081816@126/blog/static/16476102320107173226920/

    4. from mirantis: ha for mysql, rabbitmq
       https://www.mirantis.com/blog/ha-platform-components-mysql-rabbitmq/

    5. play with official examples: http://www.rabbitmq.com/tutorials/tutorial-one-python.html
        "hello world"
        "work queues"
        "publish/subscribe"
        "topics"
        After all, `bind` and `routing_key` is the key
```
