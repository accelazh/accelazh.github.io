---
layout: post
title: "Intercept RabbitMQ Message In Openstack"
tagline : "Intercept RabbitMQ Message In Openstack"
description: "Intercept RabbitMQ Message In Openstack"
category: "messaging"
tags: [openstack, messaging, rabbitmq]
---
{% include JB/setup %}

Openstack components communicates by rabbitmq, which can be seen as vessel of openstack. It is very useful if we can examine what exchange and queues are in rabbitmq and what messages is transmitted.

## Use RabbitMQ Management Plugin

The easity way is to use [RabbitMQ Management Plugin](https://www.rabbitmq.com/management.html), a web monitor to inspect what is happening in rabbitmq. Messages can be dequeued from rabbitmq to see its content, then put back. Put-back message is not guaranteed not to broke openstack. 

## List Exchange & Queue

List exchanges of openstack.

```
$ rabbitmqctl list_exchanges name type durable arguments auto_delete internal policy
Listing exchanges ...
    direct  true    []  false   false   
amq.direct  direct  true    []  false   false   
amq.fanout  fanout  true    []  false   false   
amq.headers headers true    []  false   false   
amq.match   headers true    []  false   false   
amq.rabbitmq.log    topic   true    []  false   false   
amq.rabbitmq.trace  topic   true    []  false   false   
amq.topic   topic   true    []  false   false   
cert_fanout fanout  false   []  true    false   
compute_fanout  fanout  false   []  true    false   
conductor_fanout    fanout  false   []  true    false   
consoleauth_fanout  fanout  false   []  true    false   
dhcp_agent.openstack-02.novalocal_fanout    fanout  false   []  true    false   
dhcp_agent.openstack-03.novalocal_fanout    fanout  false   []  true    false   
dhcp_agent.openstack-04.novalocal_fanout    fanout  false   []  true    false   
dhcp_agent_fanout   fanout  false   []  true    false   
l3_agent.openstack-02.novalocal_fanout  fanout  false   []  true    false   
l3_agent.openstack-03.novalocal_fanout  fanout  false   []  true    false   
l3_agent.openstack-04.novalocal_fanout  fanout  false   []  true    false   
l3_agent_fanout fanout  false   []  true    false   
n-lbaas-plugin_fanout   fanout  false   []  true    false   
n-lbaas_agent.openstack-02.novalocal_fanout fanout  false   []  true    false   
n-lbaas_agent.openstack-03.novalocal_fanout fanout  false   []  true    false   
n-lbaas_agent.openstack-04.novalocal_fanout fanout  false   []  true    false   
n-lbaas_agent_fanout    fanout  false   []  true    false   
neutron topic   false   []  false   false   
nova    topic   false   []  false   false   
q-agent-notifier-dvr-update_fanout  fanout  false   []  true    false   
q-agent-notifier-network-delete_fanout  fanout  false   []  true    false   
q-agent-notifier-port-update_fanout fanout  false   []  true    false   
q-agent-notifier-security_group-update_fanout   fanout  false   []  true    false   
q-agent-notifier-tunnel-update_fanout   fanout  false   []  true    false   
q-l3-plugin_fanout  fanout  false   []  true    false   
q-plugin_fanout fanout  false   []  true    false   
reply_07adc5aef68b4e3db8a61ffb7a502c5c  direct  false   []  true    false   
reply_1d32023d7ca1451986a7a3534a818e2f  direct  false   []  true    false   
reply_241688a279c0414d90e3b76b162fdb33  direct  false   []  true    false   
reply_2a768322ee9b4c3ea355de73b0374f74  direct  false   []  true    false   
reply_2ceed19e376b4cf78373f8e1f98c1f39  direct  false   []  true    false   
reply_38b4c8d7d7aa4d03a6355ec8485e0258  direct  false   []  true    false   
reply_40bd0d232bad4b469772b1a6ae7b9266  direct  false   []  true    false   
reply_5050b471ac05454baf9e6145121ca7c7  direct  false   []  true    false   
reply_6bae0879fe5b413c9ac3595fa3cbfbbf  direct  false   []  true    false   
reply_7d304be0842a48c8b51268f7ec41b02f  direct  false   []  true    false   
reply_9f1867d6c7ce4051a377861412427191  direct  false   []  true    false   
reply_9f9bf21f51aa427990e5000aa4a2d0b7  direct  false   []  true    false   
reply_ab28f6fe778c48618d4602ea3c5ace73  direct  false   []  true    false   
reply_b02bff3bc22c444fab3ff258081430ba  direct  false   []  true    false   
reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  direct  false   []  true    false   
reply_ce584f808713423ca834d7b146c6c9e9  direct  false   []  true    false   
reply_e95a8b2de2814843bb6b83d28c7abeed  direct  false   []  true    false   
reply_e9885a8dcf214007934d0d8aa0a39ef5  direct  false   []  true    false   
reply_eaa8cf9d5520414688a8b29b9db20543  direct  false   []  true    false   
reply_f82f54130ee24b91a4be06a4cadc704d  direct  false   []  true    false   
scheduler_fanout    fanout  false   []  true    false   
...done.
$ rabbitmqctl list_exchanges |grep topic
amq.rabbitmq.log    topic
amq.rabbitmq.trace  topic
amq.topic   topic
neutron topic
nova    topic
```

List queues of openstack.

```
$ rabbitmqctl list_queues name arguments messages consumers
Listing queues ...
cert    []  0   1
cert.openstack-01.novalocal []  0   1
cert_fanout_c3b6a1047d024c4d82ed736cca37ab10    []  0   1
compute []  0   3
compute.openstack-02.novalocal  []  0   1
compute.openstack-03.novalocal  []  0   1
compute.openstack-04.novalocal  []  0   1
compute_fanout_37820ee8b52d4522929da71b8d2770e0 []  0   1
compute_fanout_937b04c6dc184e13a40da15139326c03 []  0   1
compute_fanout_dff4ed8e64f94ff29938ccb6925e6038 []  0   1
conductor   []  0   2
conductor.openstack-01.novalocal    []  0   2
conductor_fanout_059f02fd42484b1d81f20498999b682e   []  0   1
conductor_fanout_612817c15be24accbedec3f78a202546   []  0   1
consoleauth []  0   1
consoleauth.openstack-01.novalocal  []  0   1
consoleauth_fanout_f6d2d3de596c4eacb4e945ae52f7ee58 []  0   1
dhcp_agent  []  0   6
dhcp_agent.openstack-01.novalocal   []  0   0
dhcp_agent.openstack-01.novalocal.openstack-01.novalocal    []  0   0
dhcp_agent.openstack-02.novalocal   []  0   3
dhcp_agent.openstack-02.novalocal.openstack-02.novalocal    []  0   1
dhcp_agent.openstack-02.novalocal_fanout_368887e67308455d958607cdbd1cb3b1   []  0   1
dhcp_agent.openstack-03.novalocal   []  0   3
dhcp_agent.openstack-03.novalocal.openstack-03.novalocal    []  0   1
dhcp_agent.openstack-03.novalocal_fanout_fcaed4cc7a0d4e3e94f35bea3409cc4d   []  0   1
dhcp_agent.openstack-04.novalocal   []  0   3
dhcp_agent.openstack-04.novalocal.openstack-04.novalocal    []  0   1
dhcp_agent.openstack-04.novalocal_fanout_de1d20e7e5b647edbdabce231d8f1eac   []  0   1
dhcp_agent_fanout_6c820b6e9ca04299abc796ad6035e8cc  []  0   1
dhcp_agent_fanout_76442de216f34d16aa69d6f7c72eebb1  []  0   1
dhcp_agent_fanout_adbc15f5242e4b90be2e28d99f502b19  []  0   1
dhcp_agent_fanout_ba24b6438c8f4193823943acef87a93a  []  0   1
dhcp_agent_fanout_ec9d0243330a444abaaf71d2908121eb  []  0   1
dhcp_agent_fanout_f313396733f1490c86b66f93b53ea4fa  []  0   1
ipsec_driver    []  0   0
ipsec_driver.openstack-01.novalocal []  0   0
l3_agent    []  0   6
l3_agent.openstack-01.novalocal []  0   0
l3_agent.openstack-01.novalocal.openstack-01.novalocal  []  0   0
l3_agent.openstack-02.novalocal []  0   3
l3_agent.openstack-02.novalocal.openstack-02.novalocal  []  0   1
l3_agent.openstack-02.novalocal_fanout_abc9e58899d24dea9757c9b9de7ad084 []  0   1
l3_agent.openstack-03.novalocal []  0   3
l3_agent.openstack-03.novalocal.openstack-03.novalocal  []  0   1
l3_agent.openstack-03.novalocal_fanout_85c125f6cd8d4f67a8bda949b1b44367 []  0   1
l3_agent.openstack-04.novalocal []  0   3
l3_agent.openstack-04.novalocal.openstack-04.novalocal  []  0   1
l3_agent.openstack-04.novalocal_fanout_abd453ab374e460fa8dba368f475de50 []  0   1
l3_agent_fanout_22fe4369f9c94c6abdb157d967806ca7    []  0   1
l3_agent_fanout_2f5c74b89297454c9068f2681773c749    []  0   1
l3_agent_fanout_3824a31696274bba8e6fb0c92a49610e    []  0   1
l3_agent_fanout_4293729cb958437fb52c6cdd04c76726    []  0   1
l3_agent_fanout_5129fab6dcfe494287b5a1417afcdf91    []  0   1
l3_agent_fanout_af7a3f7127e74b7697bdd7be0f914baf    []  0   1
n-lbaas-plugin  []  0   1
n-lbaas-plugin.openstack-01.novalocal   []  0   1
n-lbaas-plugin_fanout_258b582e2a954e1c89daafc26a2fc193  []  0   1
n-lbaas_agent   []  0   6
n-lbaas_agent.openstack-01.novalocal    []  0   0
n-lbaas_agent.openstack-01.novalocal.openstack-01.novalocal []  0   0
n-lbaas_agent.openstack-02.novalocal    []  0   3
n-lbaas_agent.openstack-02.novalocal.openstack-02.novalocal []  0   1
n-lbaas_agent.openstack-02.novalocal_fanout_4bbd290480a541c0a0f410f0b5bbe949    []  0   1
n-lbaas_agent.openstack-03.novalocal    []  0   3
n-lbaas_agent.openstack-03.novalocal.openstack-03.novalocal []  0   1
n-lbaas_agent.openstack-03.novalocal_fanout_9f9e6aeeb5974eb79fdde505155d3541    []  0   1
n-lbaas_agent.openstack-04.novalocal    []  0   3
n-lbaas_agent.openstack-04.novalocal.openstack-04.novalocal []  0   1
n-lbaas_agent.openstack-04.novalocal_fanout_c22854c4edc844c68965a6635750d334    []  0   1
n-lbaas_agent_fanout_1ee61b4ea0b9430fa80b9d7a39aca0ac   []  0   1
n-lbaas_agent_fanout_45e2e46e7fea4703a11c070ece7857e8   []  0   1
n-lbaas_agent_fanout_7d6add7137f148dda3fed7042336c7ff   []  0   1
n-lbaas_agent_fanout_9eb1723673f24d54a1cce88d972b2e51   []  0   1
n-lbaas_agent_fanout_aedcd117d4164c3e8ce075fd2eedfa99   []  0   1
n-lbaas_agent_fanout_ebbfd590e4bf4dff826604c78c6ba3a6   []  0   1
q-agent-notifier-dvr-update []  0   3
q-agent-notifier-dvr-update.openstack-01.novalocal  []  0   0
q-agent-notifier-dvr-update.openstack-02.novalocal  []  0   1
q-agent-notifier-dvr-update.openstack-03.novalocal  []  0   1
q-agent-notifier-dvr-update.openstack-04.novalocal  []  0   1
q-agent-notifier-dvr-update_fanout_08a70af4b8484650bd1873bf30500f14 []  0   1
q-agent-notifier-dvr-update_fanout_5f4066e44705427eb8d417b2a23aec76 []  0   1
q-agent-notifier-dvr-update_fanout_db613360bc364ad4a05db1550b0b58dc []  0   1
q-agent-notifier-network-delete []  0   3
q-agent-notifier-network-delete.openstack-01.novalocal  []  0   0
q-agent-notifier-network-delete.openstack-02.novalocal  []  0   1
q-agent-notifier-network-delete.openstack-03.novalocal  []  0   1
q-agent-notifier-network-delete.openstack-04.novalocal  []  0   1
q-agent-notifier-network-delete_fanout_1965391112ec45ee82bf15f68a02936a []  0   1
q-agent-notifier-network-delete_fanout_42d77d86515c476b8bd0bc44732a40b3 []  0   1
q-agent-notifier-network-delete_fanout_da1e307bd54c49f88ec514011bbf6609 []  0   1
q-agent-notifier-port-update    []  0   3
q-agent-notifier-port-update.openstack-01.novalocal []  0   0
q-agent-notifier-port-update.openstack-02.novalocal []  0   1
q-agent-notifier-port-update.openstack-03.novalocal []  0   1
q-agent-notifier-port-update.openstack-04.novalocal []  0   1
q-agent-notifier-port-update_fanout_2a6755a1b1334554bc621755782e4fbf    []  0   1
q-agent-notifier-port-update_fanout_a6fd2e90877e49738a03b0c0518fce23    []  0   1
q-agent-notifier-port-update_fanout_b6726f033e4249e5903232bcdd691f40    []  0   1
q-agent-notifier-security_group-update  []  0   3
q-agent-notifier-security_group-update.openstack-01.novalocal   []  0   0
q-agent-notifier-security_group-update.openstack-02.novalocal   []  0   1
q-agent-notifier-security_group-update.openstack-03.novalocal   []  0   1
q-agent-notifier-security_group-update.openstack-04.novalocal   []  0   1
q-agent-notifier-security_group-update_fanout_080b030f39a849cf81796507aabe2369  []  0   1
q-agent-notifier-security_group-update_fanout_270078481bcd4422b8b91c035b170ecb  []  0   1
q-agent-notifier-security_group-update_fanout_a823ef30d8e54e648b7a670641ed04d6  []  0   1
q-agent-notifier-tunnel-update  []  0   3
q-agent-notifier-tunnel-update.openstack-01.novalocal   []  0   0
q-agent-notifier-tunnel-update.openstack-02.novalocal   []  0   1
q-agent-notifier-tunnel-update.openstack-03.novalocal   []  0   1
q-agent-notifier-tunnel-update.openstack-04.novalocal   []  0   1
q-agent-notifier-tunnel-update_fanout_101f9d61f2d341c380c6e1c10a22e572  []  0   1
q-agent-notifier-tunnel-update_fanout_5bf260a186ff4075818b13b5d8e58e62  []  0   1
q-agent-notifier-tunnel-update_fanout_edfb77bf0ae74c139909f6e21edb6f1c  []  0   1
q-firewall-plugin   []  0   0
q-firewall-plugin.openstack-01.novalocal    []  0   0
q-l3-plugin []  0   1
q-l3-plugin.openstack-01.novalocal  []  0   1
q-l3-plugin_fanout_d1d00128c98b42d4a7fb55b71a96ae97 []  0   1
q-metering-plugin   []  0   0
q-metering-plugin.openstack-01.novalocal    []  0   0
q-plugin    []  0   1
q-plugin.openstack-01.novalocal []  0   1
q-plugin_fanout_76adbea5524b4de99b158215fb1db56a    []  0   1
reply_07adc5aef68b4e3db8a61ffb7a502c5c  []  0   1
reply_1d32023d7ca1451986a7a3534a818e2f  []  0   1
reply_241688a279c0414d90e3b76b162fdb33  []  0   1
reply_2a768322ee9b4c3ea355de73b0374f74  []  0   1
reply_2ceed19e376b4cf78373f8e1f98c1f39  []  0   1
reply_38b4c8d7d7aa4d03a6355ec8485e0258  []  0   1
reply_40bd0d232bad4b469772b1a6ae7b9266  []  0   1
reply_5050b471ac05454baf9e6145121ca7c7  []  0   1
reply_6bae0879fe5b413c9ac3595fa3cbfbbf  []  0   1
reply_7d304be0842a48c8b51268f7ec41b02f  []  0   1
reply_9f1867d6c7ce4051a377861412427191  []  0   1
reply_9f9bf21f51aa427990e5000aa4a2d0b7  []  0   1
reply_ab28f6fe778c48618d4602ea3c5ace73  []  0   1
reply_b02bff3bc22c444fab3ff258081430ba  []  0   1
reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  []  0   1
reply_ce584f808713423ca834d7b146c6c9e9  []  0   1
reply_e95a8b2de2814843bb6b83d28c7abeed  []  0   1
reply_e9885a8dcf214007934d0d8aa0a39ef5  []  0   1
reply_eaa8cf9d5520414688a8b29b9db20543  []  0   1
reply_f82f54130ee24b91a4be06a4cadc704d  []  0   1
scheduler   []  0   1
scheduler.openstack-01.novalocal    []  0   1
scheduler_fanout_318cb1685bac44b4bda11b12f967098d   []  0   1
...done.
```

To see which queue are bind to which exchange, use `list_bindings`. An example of binding is [rabbitmq routing](http://www.rabbitmq.com/tutorials/tutorial-four-python.html).

```
$ rabbitmqctl list_bindings source_name source_kind destination_name destination_kind routing_key arguments
Listing bindings ...
    exchange    cert    queue   cert    []
    exchange    cert.openstack-01.novalocal queue   cert.openstack-01.novalocal []
    exchange    cert_fanout_c3b6a1047d024c4d82ed736cca37ab10    queue   cert_fanout_c3b6a1047d024c4d82ed736cca37ab10    []
    exchange    compute queue   compute []
    exchange    compute.openstack-02.novalocal  queue   compute.openstack-02.novalocal  []
    exchange    compute.openstack-03.novalocal  queue   compute.openstack-03.novalocal  []
    exchange    compute.openstack-04.novalocal  queue   compute.openstack-04.novalocal  []
    exchange    compute_fanout_37820ee8b52d4522929da71b8d2770e0 queue   compute_fanout_37820ee8b52d4522929da71b8d2770e0 []
    exchange    compute_fanout_937b04c6dc184e13a40da15139326c03 queue   compute_fanout_937b04c6dc184e13a40da15139326c03 []
    exchange    compute_fanout_dff4ed8e64f94ff29938ccb6925e6038 queue   compute_fanout_dff4ed8e64f94ff29938ccb6925e6038 []
    exchange    conductor   queue   conductor   []
    exchange    conductor.openstack-01.novalocal    queue   conductor.openstack-01.novalocal    []
    exchange    conductor_fanout_059f02fd42484b1d81f20498999b682e   queue   conductor_fanout_059f02fd42484b1d81f20498999b682e   []
    exchange    conductor_fanout_612817c15be24accbedec3f78a202546   queue   conductor_fanout_612817c15be24accbedec3f78a202546   []
    exchange    consoleauth queue   consoleauth []
    exchange    consoleauth.openstack-01.novalocal  queue   consoleauth.openstack-01.novalocal  []
    exchange    consoleauth_fanout_f6d2d3de596c4eacb4e945ae52f7ee58 queue   consoleauth_fanout_f6d2d3de596c4eacb4e945ae52f7ee58 []
    exchange    dhcp_agent  queue   dhcp_agent  []
    exchange    dhcp_agent.openstack-01.novalocal   queue   dhcp_agent.openstack-01.novalocal   []
    exchange    dhcp_agent.openstack-01.novalocal.openstack-01.novalocal    queue   dhcp_agent.openstack-01.novalocal.openstack-01.novalocal    []
    exchange    dhcp_agent.openstack-02.novalocal   queue   dhcp_agent.openstack-02.novalocal   []
    exchange    dhcp_agent.openstack-02.novalocal.openstack-02.novalocal    queue   dhcp_agent.openstack-02.novalocal.openstack-02.novalocal    []
    exchange    dhcp_agent.openstack-02.novalocal_fanout_368887e67308455d958607cdbd1cb3b1   queue   dhcp_agent.openstack-02.novalocal_fanout_368887e67308455d958607cdbd1cb3b1[]
    exchange    dhcp_agent.openstack-03.novalocal   queue   dhcp_agent.openstack-03.novalocal   []
    exchange    dhcp_agent.openstack-03.novalocal.openstack-03.novalocal    queue   dhcp_agent.openstack-03.novalocal.openstack-03.novalocal    []
    exchange    dhcp_agent.openstack-03.novalocal_fanout_fcaed4cc7a0d4e3e94f35bea3409cc4d   queue   dhcp_agent.openstack-03.novalocal_fanout_fcaed4cc7a0d4e3e94f35bea3409cc4d[]
    exchange    dhcp_agent.openstack-04.novalocal   queue   dhcp_agent.openstack-04.novalocal   []
    exchange    dhcp_agent.openstack-04.novalocal.openstack-04.novalocal    queue   dhcp_agent.openstack-04.novalocal.openstack-04.novalocal    []
    exchange    dhcp_agent.openstack-04.novalocal_fanout_de1d20e7e5b647edbdabce231d8f1eac   queue   dhcp_agent.openstack-04.novalocal_fanout_de1d20e7e5b647edbdabce231d8f1eac[]
    exchange    dhcp_agent_fanout_6c820b6e9ca04299abc796ad6035e8cc  queue   dhcp_agent_fanout_6c820b6e9ca04299abc796ad6035e8cc  []
    exchange    dhcp_agent_fanout_76442de216f34d16aa69d6f7c72eebb1  queue   dhcp_agent_fanout_76442de216f34d16aa69d6f7c72eebb1  []
    exchange    dhcp_agent_fanout_adbc15f5242e4b90be2e28d99f502b19  queue   dhcp_agent_fanout_adbc15f5242e4b90be2e28d99f502b19  []
    exchange    dhcp_agent_fanout_ba24b6438c8f4193823943acef87a93a  queue   dhcp_agent_fanout_ba24b6438c8f4193823943acef87a93a  []
    exchange    dhcp_agent_fanout_ec9d0243330a444abaaf71d2908121eb  queue   dhcp_agent_fanout_ec9d0243330a444abaaf71d2908121eb  []
    exchange    dhcp_agent_fanout_f313396733f1490c86b66f93b53ea4fa  queue   dhcp_agent_fanout_f313396733f1490c86b66f93b53ea4fa  []
    exchange    ipsec_driver    queue   ipsec_driver    []
    exchange    ipsec_driver.openstack-01.novalocal queue   ipsec_driver.openstack-01.novalocal []
    exchange    l3_agent    queue   l3_agent    []
    exchange    l3_agent.openstack-01.novalocal queue   l3_agent.openstack-01.novalocal []
    exchange    l3_agent.openstack-01.novalocal.openstack-01.novalocal  queue   l3_agent.openstack-01.novalocal.openstack-01.novalocal  []
    exchange    l3_agent.openstack-02.novalocal queue   l3_agent.openstack-02.novalocal []
    exchange    l3_agent.openstack-02.novalocal.openstack-02.novalocal  queue   l3_agent.openstack-02.novalocal.openstack-02.novalocal  []
    exchange    l3_agent.openstack-02.novalocal_fanout_abc9e58899d24dea9757c9b9de7ad084 queue   l3_agent.openstack-02.novalocal_fanout_abc9e58899d24dea9757c9b9de7ad084 []
    exchange    l3_agent.openstack-03.novalocal queue   l3_agent.openstack-03.novalocal []
    exchange    l3_agent.openstack-03.novalocal.openstack-03.novalocal  queue   l3_agent.openstack-03.novalocal.openstack-03.novalocal  []
    exchange    l3_agent.openstack-03.novalocal_fanout_85c125f6cd8d4f67a8bda949b1b44367 queue   l3_agent.openstack-03.novalocal_fanout_85c125f6cd8d4f67a8bda949b1b44367 []
    exchange    l3_agent.openstack-04.novalocal queue   l3_agent.openstack-04.novalocal []
    exchange    l3_agent.openstack-04.novalocal.openstack-04.novalocal  queue   l3_agent.openstack-04.novalocal.openstack-04.novalocal  []
    exchange    l3_agent.openstack-04.novalocal_fanout_abd453ab374e460fa8dba368f475de50 queue   l3_agent.openstack-04.novalocal_fanout_abd453ab374e460fa8dba368f475de50 []
    exchange    l3_agent_fanout_22fe4369f9c94c6abdb157d967806ca7    queue   l3_agent_fanout_22fe4369f9c94c6abdb157d967806ca7    []
    exchange    l3_agent_fanout_2f5c74b89297454c9068f2681773c749    queue   l3_agent_fanout_2f5c74b89297454c9068f2681773c749    []
    exchange    l3_agent_fanout_3824a31696274bba8e6fb0c92a49610e    queue   l3_agent_fanout_3824a31696274bba8e6fb0c92a49610e    []
    exchange    l3_agent_fanout_4293729cb958437fb52c6cdd04c76726    queue   l3_agent_fanout_4293729cb958437fb52c6cdd04c76726    []
    exchange    l3_agent_fanout_5129fab6dcfe494287b5a1417afcdf91    queue   l3_agent_fanout_5129fab6dcfe494287b5a1417afcdf91    []
    exchange    l3_agent_fanout_af7a3f7127e74b7697bdd7be0f914baf    queue   l3_agent_fanout_af7a3f7127e74b7697bdd7be0f914baf    []
    exchange    n-lbaas-plugin  queue   n-lbaas-plugin  []
    exchange    n-lbaas-plugin.openstack-01.novalocal   queue   n-lbaas-plugin.openstack-01.novalocal   []
    exchange    n-lbaas-plugin_fanout_258b582e2a954e1c89daafc26a2fc193  queue   n-lbaas-plugin_fanout_258b582e2a954e1c89daafc26a2fc193  []
    exchange    n-lbaas_agent   queue   n-lbaas_agent   []
    exchange    n-lbaas_agent.openstack-01.novalocal    queue   n-lbaas_agent.openstack-01.novalocal    []
    exchange    n-lbaas_agent.openstack-01.novalocal.openstack-01.novalocal queue   n-lbaas_agent.openstack-01.novalocal.openstack-01.novalocal []
    exchange    n-lbaas_agent.openstack-02.novalocal    queue   n-lbaas_agent.openstack-02.novalocal    []
    exchange    n-lbaas_agent.openstack-02.novalocal.openstack-02.novalocal queue   n-lbaas_agent.openstack-02.novalocal.openstack-02.novalocal []
    exchange    n-lbaas_agent.openstack-02.novalocal_fanout_4bbd290480a541c0a0f410f0b5bbe949    queue   n-lbaas_agent.openstack-02.novalocal_fanout_4bbd290480a541c0a0f410f0b5bbe949    []
    exchange    n-lbaas_agent.openstack-03.novalocal    queue   n-lbaas_agent.openstack-03.novalocal    []
    exchange    n-lbaas_agent.openstack-03.novalocal.openstack-03.novalocal queue   n-lbaas_agent.openstack-03.novalocal.openstack-03.novalocal []
    exchange    n-lbaas_agent.openstack-03.novalocal_fanout_9f9e6aeeb5974eb79fdde505155d3541    queue   n-lbaas_agent.openstack-03.novalocal_fanout_9f9e6aeeb5974eb79fdde505155d3541    []
    exchange    n-lbaas_agent.openstack-04.novalocal    queue   n-lbaas_agent.openstack-04.novalocal    []
    exchange    n-lbaas_agent.openstack-04.novalocal.openstack-04.novalocal queue   n-lbaas_agent.openstack-04.novalocal.openstack-04.novalocal []
    exchange    n-lbaas_agent.openstack-04.novalocal_fanout_c22854c4edc844c68965a6635750d334    queue   n-lbaas_agent.openstack-04.novalocal_fanout_c22854c4edc844c68965a6635750d334    []
    exchange    n-lbaas_agent_fanout_1ee61b4ea0b9430fa80b9d7a39aca0ac   queue   n-lbaas_agent_fanout_1ee61b4ea0b9430fa80b9d7a39aca0ac   []
    exchange    n-lbaas_agent_fanout_45e2e46e7fea4703a11c070ece7857e8   queue   n-lbaas_agent_fanout_45e2e46e7fea4703a11c070ece7857e8   []
    exchange    n-lbaas_agent_fanout_7d6add7137f148dda3fed7042336c7ff   queue   n-lbaas_agent_fanout_7d6add7137f148dda3fed7042336c7ff   []
    exchange    n-lbaas_agent_fanout_9eb1723673f24d54a1cce88d972b2e51   queue   n-lbaas_agent_fanout_9eb1723673f24d54a1cce88d972b2e51   []
    exchange    n-lbaas_agent_fanout_aedcd117d4164c3e8ce075fd2eedfa99   queue   n-lbaas_agent_fanout_aedcd117d4164c3e8ce075fd2eedfa99   []
    exchange    n-lbaas_agent_fanout_ebbfd590e4bf4dff826604c78c6ba3a6   queue   n-lbaas_agent_fanout_ebbfd590e4bf4dff826604c78c6ba3a6   []
    exchange    q-agent-notifier-dvr-update queue   q-agent-notifier-dvr-update []
    exchange    q-agent-notifier-dvr-update.openstack-01.novalocal  queue   q-agent-notifier-dvr-update.openstack-01.novalocal  []
    exchange    q-agent-notifier-dvr-update.openstack-02.novalocal  queue   q-agent-notifier-dvr-update.openstack-02.novalocal  []
    exchange    q-agent-notifier-dvr-update.openstack-03.novalocal  queue   q-agent-notifier-dvr-update.openstack-03.novalocal  []
    exchange    q-agent-notifier-dvr-update.openstack-04.novalocal  queue   q-agent-notifier-dvr-update.openstack-04.novalocal  []
    exchange    q-agent-notifier-dvr-update_fanout_08a70af4b8484650bd1873bf30500f14 queue   q-agent-notifier-dvr-update_fanout_08a70af4b8484650bd1873bf30500f14 []
    exchange    q-agent-notifier-dvr-update_fanout_5f4066e44705427eb8d417b2a23aec76 queue   q-agent-notifier-dvr-update_fanout_5f4066e44705427eb8d417b2a23aec76 []
    exchange    q-agent-notifier-dvr-update_fanout_db613360bc364ad4a05db1550b0b58dc queue   q-agent-notifier-dvr-update_fanout_db613360bc364ad4a05db1550b0b58dc []
    exchange    q-agent-notifier-network-delete queue   q-agent-notifier-network-delete []
    exchange    q-agent-notifier-network-delete.openstack-01.novalocal  queue   q-agent-notifier-network-delete.openstack-01.novalocal  []
    exchange    q-agent-notifier-network-delete.openstack-02.novalocal  queue   q-agent-notifier-network-delete.openstack-02.novalocal  []
    exchange    q-agent-notifier-network-delete.openstack-03.novalocal  queue   q-agent-notifier-network-delete.openstack-03.novalocal  []
    exchange    q-agent-notifier-network-delete.openstack-04.novalocal  queue   q-agent-notifier-network-delete.openstack-04.novalocal  []
    exchange    q-agent-notifier-network-delete_fanout_1965391112ec45ee82bf15f68a02936a queue   q-agent-notifier-network-delete_fanout_1965391112ec45ee82bf15f68a02936a []
    exchange    q-agent-notifier-network-delete_fanout_42d77d86515c476b8bd0bc44732a40b3 queue   q-agent-notifier-network-delete_fanout_42d77d86515c476b8bd0bc44732a40b3 []
    exchange    q-agent-notifier-network-delete_fanout_da1e307bd54c49f88ec514011bbf6609 queue   q-agent-notifier-network-delete_fanout_da1e307bd54c49f88ec514011bbf6609 []
    exchange    q-agent-notifier-port-update    queue   q-agent-notifier-port-update    []
    exchange    q-agent-notifier-port-update.openstack-01.novalocal queue   q-agent-notifier-port-update.openstack-01.novalocal []
    exchange    q-agent-notifier-port-update.openstack-02.novalocal queue   q-agent-notifier-port-update.openstack-02.novalocal []
    exchange    q-agent-notifier-port-update.openstack-03.novalocal queue   q-agent-notifier-port-update.openstack-03.novalocal []
    exchange    q-agent-notifier-port-update.openstack-04.novalocal queue   q-agent-notifier-port-update.openstack-04.novalocal []
    exchange    q-agent-notifier-port-update_fanout_2a6755a1b1334554bc621755782e4fbf    queue   q-agent-notifier-port-update_fanout_2a6755a1b1334554bc621755782e4fbf    []
    exchange    q-agent-notifier-port-update_fanout_a6fd2e90877e49738a03b0c0518fce23    queue   q-agent-notifier-port-update_fanout_a6fd2e90877e49738a03b0c0518fce23    []
    exchange    q-agent-notifier-port-update_fanout_b6726f033e4249e5903232bcdd691f40    queue   q-agent-notifier-port-update_fanout_b6726f033e4249e5903232bcdd691f40    []
    exchange    q-agent-notifier-security_group-update  queue   q-agent-notifier-security_group-update  []
    exchange    q-agent-notifier-security_group-update.openstack-01.novalocal   queue   q-agent-notifier-security_group-update.openstack-01.novalocal   []
    exchange    q-agent-notifier-security_group-update.openstack-02.novalocal   queue   q-agent-notifier-security_group-update.openstack-02.novalocal   []
    exchange    q-agent-notifier-security_group-update.openstack-03.novalocal   queue   q-agent-notifier-security_group-update.openstack-03.novalocal   []
    exchange    q-agent-notifier-security_group-update.openstack-04.novalocal   queue   q-agent-notifier-security_group-update.openstack-04.novalocal   []
    exchange    q-agent-notifier-security_group-update_fanout_080b030f39a849cf81796507aabe2369  queue   q-agent-notifier-security_group-update_fanout_080b030f39a849cf81796507aabe2369  []
    exchange    q-agent-notifier-security_group-update_fanout_270078481bcd4422b8b91c035b170ecb  queue   q-agent-notifier-security_group-update_fanout_270078481bcd4422b8b91c035b170ecb  []
    exchange    q-agent-notifier-security_group-update_fanout_a823ef30d8e54e648b7a670641ed04d6  queue   q-agent-notifier-security_group-update_fanout_a823ef30d8e54e648b7a670641ed04d6  []
    exchange    q-agent-notifier-tunnel-update  queue   q-agent-notifier-tunnel-update  []
    exchange    q-agent-notifier-tunnel-update.openstack-01.novalocal   queue   q-agent-notifier-tunnel-update.openstack-01.novalocal   []
    exchange    q-agent-notifier-tunnel-update.openstack-02.novalocal   queue   q-agent-notifier-tunnel-update.openstack-02.novalocal   []
    exchange    q-agent-notifier-tunnel-update.openstack-03.novalocal   queue   q-agent-notifier-tunnel-update.openstack-03.novalocal   []
    exchange    q-agent-notifier-tunnel-update.openstack-04.novalocal   queue   q-agent-notifier-tunnel-update.openstack-04.novalocal   []
    exchange    q-agent-notifier-tunnel-update_fanout_101f9d61f2d341c380c6e1c10a22e572  queue   q-agent-notifier-tunnel-update_fanout_101f9d61f2d341c380c6e1c10a22e572  []
    exchange    q-agent-notifier-tunnel-update_fanout_5bf260a186ff4075818b13b5d8e58e62  queue   q-agent-notifier-tunnel-update_fanout_5bf260a186ff4075818b13b5d8e58e62  []
    exchange    q-agent-notifier-tunnel-update_fanout_edfb77bf0ae74c139909f6e21edb6f1c  queue   q-agent-notifier-tunnel-update_fanout_edfb77bf0ae74c139909f6e21edb6f1c  []
    exchange    q-firewall-plugin   queue   q-firewall-plugin   []
    exchange    q-firewall-plugin.openstack-01.novalocal    queue   q-firewall-plugin.openstack-01.novalocal    []
    exchange    q-l3-plugin queue   q-l3-plugin []
    exchange    q-l3-plugin.openstack-01.novalocal  queue   q-l3-plugin.openstack-01.novalocal  []
    exchange    q-l3-plugin_fanout_d1d00128c98b42d4a7fb55b71a96ae97 queue   q-l3-plugin_fanout_d1d00128c98b42d4a7fb55b71a96ae97 []
    exchange    q-metering-plugin   queue   q-metering-plugin   []
    exchange    q-metering-plugin.openstack-01.novalocal    queue   q-metering-plugin.openstack-01.novalocal    []
    exchange    q-plugin    queue   q-plugin    []
    exchange    q-plugin.openstack-01.novalocal queue   q-plugin.openstack-01.novalocal []
    exchange    q-plugin_fanout_76adbea5524b4de99b158215fb1db56a    queue   q-plugin_fanout_76adbea5524b4de99b158215fb1db56a    []
    exchange    reply_07adc5aef68b4e3db8a61ffb7a502c5c  queue   reply_07adc5aef68b4e3db8a61ffb7a502c5c  []
    exchange    reply_1d32023d7ca1451986a7a3534a818e2f  queue   reply_1d32023d7ca1451986a7a3534a818e2f  []
    exchange    reply_241688a279c0414d90e3b76b162fdb33  queue   reply_241688a279c0414d90e3b76b162fdb33  []
    exchange    reply_2a768322ee9b4c3ea355de73b0374f74  queue   reply_2a768322ee9b4c3ea355de73b0374f74  []
    exchange    reply_2ceed19e376b4cf78373f8e1f98c1f39  queue   reply_2ceed19e376b4cf78373f8e1f98c1f39  []
    exchange    reply_38b4c8d7d7aa4d03a6355ec8485e0258  queue   reply_38b4c8d7d7aa4d03a6355ec8485e0258  []
    exchange    reply_40bd0d232bad4b469772b1a6ae7b9266  queue   reply_40bd0d232bad4b469772b1a6ae7b9266  []
    exchange    reply_5050b471ac05454baf9e6145121ca7c7  queue   reply_5050b471ac05454baf9e6145121ca7c7  []
    exchange    reply_6bae0879fe5b413c9ac3595fa3cbfbbf  queue   reply_6bae0879fe5b413c9ac3595fa3cbfbbf  []
    exchange    reply_7d304be0842a48c8b51268f7ec41b02f  queue   reply_7d304be0842a48c8b51268f7ec41b02f  []
    exchange    reply_9f1867d6c7ce4051a377861412427191  queue   reply_9f1867d6c7ce4051a377861412427191  []
    exchange    reply_9f9bf21f51aa427990e5000aa4a2d0b7  queue   reply_9f9bf21f51aa427990e5000aa4a2d0b7  []
    exchange    reply_ab28f6fe778c48618d4602ea3c5ace73  queue   reply_ab28f6fe778c48618d4602ea3c5ace73  []
    exchange    reply_b02bff3bc22c444fab3ff258081430ba  queue   reply_b02bff3bc22c444fab3ff258081430ba  []
    exchange    reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  queue   reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  []
    exchange    reply_ce584f808713423ca834d7b146c6c9e9  queue   reply_ce584f808713423ca834d7b146c6c9e9  []
    exchange    reply_e95a8b2de2814843bb6b83d28c7abeed  queue   reply_e95a8b2de2814843bb6b83d28c7abeed  []
    exchange    reply_e9885a8dcf214007934d0d8aa0a39ef5  queue   reply_e9885a8dcf214007934d0d8aa0a39ef5  []
    exchange    reply_eaa8cf9d5520414688a8b29b9db20543  queue   reply_eaa8cf9d5520414688a8b29b9db20543  []
    exchange    reply_f82f54130ee24b91a4be06a4cadc704d  queue   reply_f82f54130ee24b91a4be06a4cadc704d  []
    exchange    scheduler   queue   scheduler   []
    exchange    scheduler.openstack-01.novalocal    queue   scheduler.openstack-01.novalocal    []
    exchange    scheduler_fanout_318cb1685bac44b4bda11b12f967098d   queue   scheduler_fanout_318cb1685bac44b4bda11b12f967098d   []
cert_fanout exchange    cert_fanout_c3b6a1047d024c4d82ed736cca37ab10    queue   cert    []
compute_fanout  exchange    compute_fanout_37820ee8b52d4522929da71b8d2770e0 queue   compute []
compute_fanout  exchange    compute_fanout_937b04c6dc184e13a40da15139326c03 queue   compute []
compute_fanout  exchange    compute_fanout_dff4ed8e64f94ff29938ccb6925e6038 queue   compute []
conductor_fanout    exchange    conductor_fanout_059f02fd42484b1d81f20498999b682e   queue   conductor   []
conductor_fanout    exchange    conductor_fanout_612817c15be24accbedec3f78a202546   queue   conductor   []
consoleauth_fanout  exchange    consoleauth_fanout_f6d2d3de596c4eacb4e945ae52f7ee58 queue   consoleauth []
dhcp_agent.openstack-02.novalocal_fanout    exchange    dhcp_agent.openstack-02.novalocal_fanout_368887e67308455d958607cdbd1cb3b1   queue   dhcp_agent.openstack-02.novalocal   []
dhcp_agent.openstack-03.novalocal_fanout    exchange    dhcp_agent.openstack-03.novalocal_fanout_fcaed4cc7a0d4e3e94f35bea3409cc4d   queue   dhcp_agent.openstack-03.novalocal   []
dhcp_agent.openstack-04.novalocal_fanout    exchange    dhcp_agent.openstack-04.novalocal_fanout_de1d20e7e5b647edbdabce231d8f1eac   queue   dhcp_agent.openstack-04.novalocal   []
dhcp_agent_fanout   exchange    dhcp_agent_fanout_6c820b6e9ca04299abc796ad6035e8cc  queue   dhcp_agent  []
dhcp_agent_fanout   exchange    dhcp_agent_fanout_76442de216f34d16aa69d6f7c72eebb1  queue   dhcp_agent  []
dhcp_agent_fanout   exchange    dhcp_agent_fanout_adbc15f5242e4b90be2e28d99f502b19  queue   dhcp_agent  []
dhcp_agent_fanout   exchange    dhcp_agent_fanout_ba24b6438c8f4193823943acef87a93a  queue   dhcp_agent  []
dhcp_agent_fanout   exchange    dhcp_agent_fanout_ec9d0243330a444abaaf71d2908121eb  queue   dhcp_agent  []
dhcp_agent_fanout   exchange    dhcp_agent_fanout_f313396733f1490c86b66f93b53ea4fa  queue   dhcp_agent  []
l3_agent.openstack-02.novalocal_fanout  exchange    l3_agent.openstack-02.novalocal_fanout_abc9e58899d24dea9757c9b9de7ad084 queue   l3_agent.openstack-02.novalocal []
l3_agent.openstack-03.novalocal_fanout  exchange    l3_agent.openstack-03.novalocal_fanout_85c125f6cd8d4f67a8bda949b1b44367 queue   l3_agent.openstack-03.novalocal []
l3_agent.openstack-04.novalocal_fanout  exchange    l3_agent.openstack-04.novalocal_fanout_abd453ab374e460fa8dba368f475de50 queue   l3_agent.openstack-04.novalocal []
l3_agent_fanout exchange    l3_agent_fanout_22fe4369f9c94c6abdb157d967806ca7    queue   l3_agent    []
l3_agent_fanout exchange    l3_agent_fanout_2f5c74b89297454c9068f2681773c749    queue   l3_agent    []
l3_agent_fanout exchange    l3_agent_fanout_3824a31696274bba8e6fb0c92a49610e    queue   l3_agent    []
l3_agent_fanout exchange    l3_agent_fanout_4293729cb958437fb52c6cdd04c76726    queue   l3_agent    []
l3_agent_fanout exchange    l3_agent_fanout_5129fab6dcfe494287b5a1417afcdf91    queue   l3_agent    []
l3_agent_fanout exchange    l3_agent_fanout_af7a3f7127e74b7697bdd7be0f914baf    queue   l3_agent    []
n-lbaas-plugin_fanout   exchange    n-lbaas-plugin_fanout_258b582e2a954e1c89daafc26a2fc193  queue   n-lbaas-plugin  []
n-lbaas_agent.openstack-02.novalocal_fanout exchange    n-lbaas_agent.openstack-02.novalocal_fanout_4bbd290480a541c0a0f410f0b5bbe949    queue   n-lbaas_agent.openstack-02.novalocal    []
n-lbaas_agent.openstack-03.novalocal_fanout exchange    n-lbaas_agent.openstack-03.novalocal_fanout_9f9e6aeeb5974eb79fdde505155d3541    queue   n-lbaas_agent.openstack-03.novalocal    []
n-lbaas_agent.openstack-04.novalocal_fanout exchange    n-lbaas_agent.openstack-04.novalocal_fanout_c22854c4edc844c68965a6635750d334    queue   n-lbaas_agent.openstack-04.novalocal    []
n-lbaas_agent_fanout    exchange    n-lbaas_agent_fanout_1ee61b4ea0b9430fa80b9d7a39aca0ac   queue   n-lbaas_agent   []
n-lbaas_agent_fanout    exchange    n-lbaas_agent_fanout_45e2e46e7fea4703a11c070ece7857e8   queue   n-lbaas_agent   []
n-lbaas_agent_fanout    exchange    n-lbaas_agent_fanout_7d6add7137f148dda3fed7042336c7ff   queue   n-lbaas_agent   []
n-lbaas_agent_fanout    exchange    n-lbaas_agent_fanout_9eb1723673f24d54a1cce88d972b2e51   queue   n-lbaas_agent   []
n-lbaas_agent_fanout    exchange    n-lbaas_agent_fanout_aedcd117d4164c3e8ce075fd2eedfa99   queue   n-lbaas_agent   []
n-lbaas_agent_fanout    exchange    n-lbaas_agent_fanout_ebbfd590e4bf4dff826604c78c6ba3a6   queue   n-lbaas_agent   []
neutron exchange    dhcp_agent  queue   dhcp_agent  []
neutron exchange    dhcp_agent.openstack-01.novalocal   queue   dhcp_agent.openstack-01.novalocal   []
neutron exchange    dhcp_agent.openstack-01.novalocal.openstack-01.novalocal    queue   dhcp_agent.openstack-01.novalocal.openstack-01.novalocal    []
neutron exchange    dhcp_agent.openstack-02.novalocal   queue   dhcp_agent.openstack-02.novalocal   []
neutron exchange    dhcp_agent.openstack-02.novalocal.openstack-02.novalocal    queue   dhcp_agent.openstack-02.novalocal.openstack-02.novalocal    []
neutron exchange    dhcp_agent.openstack-03.novalocal   queue   dhcp_agent.openstack-03.novalocal   []
neutron exchange    dhcp_agent.openstack-03.novalocal.openstack-03.novalocal    queue   dhcp_agent.openstack-03.novalocal.openstack-03.novalocal    []
neutron exchange    dhcp_agent.openstack-04.novalocal   queue   dhcp_agent.openstack-04.novalocal   []
neutron exchange    dhcp_agent.openstack-04.novalocal.openstack-04.novalocal    queue   dhcp_agent.openstack-04.novalocal.openstack-04.novalocal    []
neutron exchange    ipsec_driver    queue   ipsec_driver    []
neutron exchange    ipsec_driver.openstack-01.novalocal queue   ipsec_driver.openstack-01.novalocal []
neutron exchange    l3_agent    queue   l3_agent    []
neutron exchange    l3_agent.openstack-01.novalocal queue   l3_agent.openstack-01.novalocal []
neutron exchange    l3_agent.openstack-01.novalocal.openstack-01.novalocal  queue   l3_agent.openstack-01.novalocal.openstack-01.novalocal  []
neutron exchange    l3_agent.openstack-02.novalocal queue   l3_agent.openstack-02.novalocal []
neutron exchange    l3_agent.openstack-02.novalocal.openstack-02.novalocal  queue   l3_agent.openstack-02.novalocal.openstack-02.novalocal  []
neutron exchange    l3_agent.openstack-03.novalocal queue   l3_agent.openstack-03.novalocal []
neutron exchange    l3_agent.openstack-03.novalocal.openstack-03.novalocal  queue   l3_agent.openstack-03.novalocal.openstack-03.novalocal  []
neutron exchange    l3_agent.openstack-04.novalocal queue   l3_agent.openstack-04.novalocal []
neutron exchange    l3_agent.openstack-04.novalocal.openstack-04.novalocal  queue   l3_agent.openstack-04.novalocal.openstack-04.novalocal  []
neutron exchange    n-lbaas-plugin  queue   n-lbaas-plugin  []
neutron exchange    n-lbaas-plugin.openstack-01.novalocal   queue   n-lbaas-plugin.openstack-01.novalocal   []
neutron exchange    n-lbaas_agent   queue   n-lbaas_agent   []
neutron exchange    n-lbaas_agent.openstack-01.novalocal    queue   n-lbaas_agent.openstack-01.novalocal    []
neutron exchange    n-lbaas_agent.openstack-01.novalocal.openstack-01.novalocal queue   n-lbaas_agent.openstack-01.novalocal.openstack-01.novalocal []
neutron exchange    n-lbaas_agent.openstack-02.novalocal    queue   n-lbaas_agent.openstack-02.novalocal    []
neutron exchange    n-lbaas_agent.openstack-02.novalocal.openstack-02.novalocal queue   n-lbaas_agent.openstack-02.novalocal.openstack-02.novalocal []
neutron exchange    n-lbaas_agent.openstack-03.novalocal    queue   n-lbaas_agent.openstack-03.novalocal    []
neutron exchange    n-lbaas_agent.openstack-03.novalocal.openstack-03.novalocal queue   n-lbaas_agent.openstack-03.novalocal.openstack-03.novalocal []
neutron exchange    n-lbaas_agent.openstack-04.novalocal    queue   n-lbaas_agent.openstack-04.novalocal    []
neutron exchange    n-lbaas_agent.openstack-04.novalocal.openstack-04.novalocal queue   n-lbaas_agent.openstack-04.novalocal.openstack-04.novalocal []
neutron exchange    q-agent-notifier-dvr-update queue   q-agent-notifier-dvr-update []
neutron exchange    q-agent-notifier-dvr-update.openstack-01.novalocal  queue   q-agent-notifier-dvr-update.openstack-01.novalocal  []
neutron exchange    q-agent-notifier-dvr-update.openstack-02.novalocal  queue   q-agent-notifier-dvr-update.openstack-02.novalocal  []
neutron exchange    q-agent-notifier-dvr-update.openstack-03.novalocal  queue   q-agent-notifier-dvr-update.openstack-03.novalocal  []
neutron exchange    q-agent-notifier-dvr-update.openstack-04.novalocal  queue   q-agent-notifier-dvr-update.openstack-04.novalocal  []
neutron exchange    q-agent-notifier-network-delete queue   q-agent-notifier-network-delete []
neutron exchange    q-agent-notifier-network-delete.openstack-01.novalocal  queue   q-agent-notifier-network-delete.openstack-01.novalocal  []
neutron exchange    q-agent-notifier-network-delete.openstack-02.novalocal  queue   q-agent-notifier-network-delete.openstack-02.novalocal  []
neutron exchange    q-agent-notifier-network-delete.openstack-03.novalocal  queue   q-agent-notifier-network-delete.openstack-03.novalocal  []
neutron exchange    q-agent-notifier-network-delete.openstack-04.novalocal  queue   q-agent-notifier-network-delete.openstack-04.novalocal  []
neutron exchange    q-agent-notifier-port-update    queue   q-agent-notifier-port-update    []
neutron exchange    q-agent-notifier-port-update.openstack-01.novalocal queue   q-agent-notifier-port-update.openstack-01.novalocal []
neutron exchange    q-agent-notifier-port-update.openstack-02.novalocal queue   q-agent-notifier-port-update.openstack-02.novalocal []
neutron exchange    q-agent-notifier-port-update.openstack-03.novalocal queue   q-agent-notifier-port-update.openstack-03.novalocal []
neutron exchange    q-agent-notifier-port-update.openstack-04.novalocal queue   q-agent-notifier-port-update.openstack-04.novalocal []
neutron exchange    q-agent-notifier-security_group-update  queue   q-agent-notifier-security_group-update  []
neutron exchange    q-agent-notifier-security_group-update.openstack-01.novalocal   queue   q-agent-notifier-security_group-update.openstack-01.novalocal   []
neutron exchange    q-agent-notifier-security_group-update.openstack-02.novalocal   queue   q-agent-notifier-security_group-update.openstack-02.novalocal   []
neutron exchange    q-agent-notifier-security_group-update.openstack-03.novalocal   queue   q-agent-notifier-security_group-update.openstack-03.novalocal   []
neutron exchange    q-agent-notifier-security_group-update.openstack-04.novalocal   queue   q-agent-notifier-security_group-update.openstack-04.novalocal   []
neutron exchange    q-agent-notifier-tunnel-update  queue   q-agent-notifier-tunnel-update  []
neutron exchange    q-agent-notifier-tunnel-update.openstack-01.novalocal   queue   q-agent-notifier-tunnel-update.openstack-01.novalocal   []
neutron exchange    q-agent-notifier-tunnel-update.openstack-02.novalocal   queue   q-agent-notifier-tunnel-update.openstack-02.novalocal   []
neutron exchange    q-agent-notifier-tunnel-update.openstack-03.novalocal   queue   q-agent-notifier-tunnel-update.openstack-03.novalocal   []
neutron exchange    q-agent-notifier-tunnel-update.openstack-04.novalocal   queue   q-agent-notifier-tunnel-update.openstack-04.novalocal   []
neutron exchange    q-firewall-plugin   queue   q-firewall-plugin   []
neutron exchange    q-firewall-plugin.openstack-01.novalocal    queue   q-firewall-plugin.openstack-01.novalocal    []
neutron exchange    q-l3-plugin queue   q-l3-plugin []
neutron exchange    q-l3-plugin.openstack-01.novalocal  queue   q-l3-plugin.openstack-01.novalocal  []
neutron exchange    q-metering-plugin   queue   q-metering-plugin   []
neutron exchange    q-metering-plugin.openstack-01.novalocal    queue   q-metering-plugin.openstack-01.novalocal    []
neutron exchange    q-plugin    queue   q-plugin    []
neutron exchange    q-plugin.openstack-01.novalocal queue   q-plugin.openstack-01.novalocal []
nova    exchange    cert    queue   cert    []
nova    exchange    cert.openstack-01.novalocal queue   cert.openstack-01.novalocal []
nova    exchange    compute queue   compute []
nova    exchange    compute.openstack-02.novalocal  queue   compute.openstack-02.novalocal  []
nova    exchange    compute.openstack-03.novalocal  queue   compute.openstack-03.novalocal  []
nova    exchange    compute.openstack-04.novalocal  queue   compute.openstack-04.novalocal  []
nova    exchange    conductor   queue   conductor   []
nova    exchange    conductor.openstack-01.novalocal    queue   conductor.openstack-01.novalocal    []
nova    exchange    consoleauth queue   consoleauth []
nova    exchange    consoleauth.openstack-01.novalocal  queue   consoleauth.openstack-01.novalocal  []
nova    exchange    scheduler   queue   scheduler   []
nova    exchange    scheduler.openstack-01.novalocal    queue   scheduler.openstack-01.novalocal    []
q-agent-notifier-dvr-update_fanout  exchange    q-agent-notifier-dvr-update_fanout_08a70af4b8484650bd1873bf30500f14 queue   q-agent-notifier-dvr-update []
q-agent-notifier-dvr-update_fanout  exchange    q-agent-notifier-dvr-update_fanout_5f4066e44705427eb8d417b2a23aec76 queue   q-agent-notifier-dvr-update []
q-agent-notifier-dvr-update_fanout  exchange    q-agent-notifier-dvr-update_fanout_db613360bc364ad4a05db1550b0b58dc queue   q-agent-notifier-dvr-update []
q-agent-notifier-network-delete_fanout  exchange    q-agent-notifier-network-delete_fanout_1965391112ec45ee82bf15f68a02936a queue   q-agent-notifier-network-delete []
q-agent-notifier-network-delete_fanout  exchange    q-agent-notifier-network-delete_fanout_42d77d86515c476b8bd0bc44732a40b3 queue   q-agent-notifier-network-delete []
q-agent-notifier-network-delete_fanout  exchange    q-agent-notifier-network-delete_fanout_da1e307bd54c49f88ec514011bbf6609 queue   q-agent-notifier-network-delete []
q-agent-notifier-port-update_fanout exchange    q-agent-notifier-port-update_fanout_2a6755a1b1334554bc621755782e4fbf    queue   q-agent-notifier-port-update    []
q-agent-notifier-port-update_fanout exchange    q-agent-notifier-port-update_fanout_a6fd2e90877e49738a03b0c0518fce23    queue   q-agent-notifier-port-update    []
q-agent-notifier-port-update_fanout exchange    q-agent-notifier-port-update_fanout_b6726f033e4249e5903232bcdd691f40    queue   q-agent-notifier-port-update    []
q-agent-notifier-security_group-update_fanout   exchange    q-agent-notifier-security_group-update_fanout_080b030f39a849cf81796507aabe2369  queue   q-agent-notifier-security_group-update  []
q-agent-notifier-security_group-update_fanout   exchange    q-agent-notifier-security_group-update_fanout_270078481bcd4422b8b91c035b170ecb  queue   q-agent-notifier-security_group-update  []
q-agent-notifier-security_group-update_fanout   exchange    q-agent-notifier-security_group-update_fanout_a823ef30d8e54e648b7a670641ed04d6  queue   q-agent-notifier-security_group-update  []
q-agent-notifier-tunnel-update_fanout   exchange    q-agent-notifier-tunnel-update_fanout_101f9d61f2d341c380c6e1c10a22e572  queue   q-agent-notifier-tunnel-update  []
q-agent-notifier-tunnel-update_fanout   exchange    q-agent-notifier-tunnel-update_fanout_5bf260a186ff4075818b13b5d8e58e62  queue   q-agent-notifier-tunnel-update  []
q-agent-notifier-tunnel-update_fanout   exchange    q-agent-notifier-tunnel-update_fanout_edfb77bf0ae74c139909f6e21edb6f1c  queue   q-agent-notifier-tunnel-update  []
q-l3-plugin_fanout  exchange    q-l3-plugin_fanout_d1d00128c98b42d4a7fb55b71a96ae97 queue   q-l3-plugin []
q-plugin_fanout exchange    q-plugin_fanout_76adbea5524b4de99b158215fb1db56a    queue   q-plugin    []
reply_07adc5aef68b4e3db8a61ffb7a502c5c  exchange    reply_07adc5aef68b4e3db8a61ffb7a502c5c  queue   reply_07adc5aef68b4e3db8a61ffb7a502c5c  []
reply_1d32023d7ca1451986a7a3534a818e2f  exchange    reply_1d32023d7ca1451986a7a3534a818e2f  queue   reply_1d32023d7ca1451986a7a3534a818e2f  []
reply_241688a279c0414d90e3b76b162fdb33  exchange    reply_241688a279c0414d90e3b76b162fdb33  queue   reply_241688a279c0414d90e3b76b162fdb33  []
reply_2a768322ee9b4c3ea355de73b0374f74  exchange    reply_2a768322ee9b4c3ea355de73b0374f74  queue   reply_2a768322ee9b4c3ea355de73b0374f74  []
reply_2ceed19e376b4cf78373f8e1f98c1f39  exchange    reply_2ceed19e376b4cf78373f8e1f98c1f39  queue   reply_2ceed19e376b4cf78373f8e1f98c1f39  []
reply_38b4c8d7d7aa4d03a6355ec8485e0258  exchange    reply_38b4c8d7d7aa4d03a6355ec8485e0258  queue   reply_38b4c8d7d7aa4d03a6355ec8485e0258  []
reply_40bd0d232bad4b469772b1a6ae7b9266  exchange    reply_40bd0d232bad4b469772b1a6ae7b9266  queue   reply_40bd0d232bad4b469772b1a6ae7b9266  []
reply_5050b471ac05454baf9e6145121ca7c7  exchange    reply_5050b471ac05454baf9e6145121ca7c7  queue   reply_5050b471ac05454baf9e6145121ca7c7  []
reply_6bae0879fe5b413c9ac3595fa3cbfbbf  exchange    reply_6bae0879fe5b413c9ac3595fa3cbfbbf  queue   reply_6bae0879fe5b413c9ac3595fa3cbfbbf  []
reply_7d304be0842a48c8b51268f7ec41b02f  exchange    reply_7d304be0842a48c8b51268f7ec41b02f  queue   reply_7d304be0842a48c8b51268f7ec41b02f  []
reply_9f1867d6c7ce4051a377861412427191  exchange    reply_9f1867d6c7ce4051a377861412427191  queue   reply_9f1867d6c7ce4051a377861412427191  []
reply_9f9bf21f51aa427990e5000aa4a2d0b7  exchange    reply_9f9bf21f51aa427990e5000aa4a2d0b7  queue   reply_9f9bf21f51aa427990e5000aa4a2d0b7  []
reply_ab28f6fe778c48618d4602ea3c5ace73  exchange    reply_ab28f6fe778c48618d4602ea3c5ace73  queue   reply_ab28f6fe778c48618d4602ea3c5ace73  []
reply_b02bff3bc22c444fab3ff258081430ba  exchange    reply_b02bff3bc22c444fab3ff258081430ba  queue   reply_b02bff3bc22c444fab3ff258081430ba  []
reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  exchange    reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  queue   reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  []
reply_ce584f808713423ca834d7b146c6c9e9  exchange    reply_ce584f808713423ca834d7b146c6c9e9  queue   reply_ce584f808713423ca834d7b146c6c9e9  []
reply_e95a8b2de2814843bb6b83d28c7abeed  exchange    reply_e95a8b2de2814843bb6b83d28c7abeed  queue   reply_e95a8b2de2814843bb6b83d28c7abeed  []
reply_e9885a8dcf214007934d0d8aa0a39ef5  exchange    reply_e9885a8dcf214007934d0d8aa0a39ef5  queue   reply_e9885a8dcf214007934d0d8aa0a39ef5  []
reply_eaa8cf9d5520414688a8b29b9db20543  exchange    reply_eaa8cf9d5520414688a8b29b9db20543  queue   reply_eaa8cf9d5520414688a8b29b9db20543  []
reply_f82f54130ee24b91a4be06a4cadc704d  exchange    reply_f82f54130ee24b91a4be06a4cadc704d  queue   reply_f82f54130ee24b91a4be06a4cadc704d  []
scheduler_fanout    exchange    scheduler_fanout_318cb1685bac44b4bda11b12f967098d   queue   scheduler   []
...done.
```

To see who is subscribing a queue

```
$ rabbitmqctl list_consumers
Listing consumers ...
cert    <'rabbit@openstack-01'.1.652.0> 1   true
cert.openstack-01.novalocal <'rabbit@openstack-01'.1.652.0> 2   true
cert_fanout_c3b6a1047d024c4d82ed736cca37ab10    <'rabbit@openstack-01'.1.652.0> 3   true
compute <'rabbit@openstack-01'.1.1107.0>    1   true
compute <'rabbit@openstack-01'.1.1813.0>    1   true
compute <'rabbit@openstack-01'.1.24489.11>  1   true
compute.openstack-02.novalocal  <'rabbit@openstack-01'.1.1107.0>    2   true
compute.openstack-03.novalocal  <'rabbit@openstack-01'.1.24489.11>  2   true
compute.openstack-04.novalocal  <'rabbit@openstack-01'.1.1813.0>    2   true
compute_fanout_37820ee8b52d4522929da71b8d2770e0 <'rabbit@openstack-01'.1.1107.0>    3   true
compute_fanout_937b04c6dc184e13a40da15139326c03 <'rabbit@openstack-01'.1.1813.0>    3   true
compute_fanout_dff4ed8e64f94ff29938ccb6925e6038 <'rabbit@openstack-01'.1.24489.11>  3   true
conductor   <'rabbit@openstack-01'.1.625.0> 1   true
conductor   <'rabbit@openstack-01'.1.637.0> 1   true
conductor.openstack-01.novalocal    <'rabbit@openstack-01'.1.625.0> 2   true
conductor.openstack-01.novalocal    <'rabbit@openstack-01'.1.637.0> 2   true
conductor_fanout_059f02fd42484b1d81f20498999b682e   <'rabbit@openstack-01'.1.637.0> 3   true
conductor_fanout_612817c15be24accbedec3f78a202546   <'rabbit@openstack-01'.1.625.0> 3   true
consoleauth <'rabbit@openstack-01'.1.656.0> 1   true
consoleauth.openstack-01.novalocal  <'rabbit@openstack-01'.1.656.0> 2   true
consoleauth_fanout_f6d2d3de596c4eacb4e945ae52f7ee58 <'rabbit@openstack-01'.1.656.0> 3   true
dhcp_agent  <'rabbit@openstack-01'.1.10023.35>  1   true
dhcp_agent  <'rabbit@openstack-01'.1.10055.35>  1   true
dhcp_agent  <'rabbit@openstack-01'.1.10313.35>  1   true
dhcp_agent  <'rabbit@openstack-01'.1.10464.35>  1   true
dhcp_agent  <'rabbit@openstack-01'.1.10768.35>  1   true
dhcp_agent  <'rabbit@openstack-01'.1.10903.35>  1   true
dhcp_agent.openstack-02.novalocal   <'rabbit@openstack-01'.1.9991.35>   1   true
dhcp_agent.openstack-02.novalocal   <'rabbit@openstack-01'.1.10023.35>  2   true
dhcp_agent.openstack-02.novalocal   <'rabbit@openstack-01'.1.10055.35>  2   true
dhcp_agent.openstack-02.novalocal.openstack-02.novalocal    <'rabbit@openstack-01'.1.9991.35>   2   true
dhcp_agent.openstack-02.novalocal_fanout_368887e67308455d958607cdbd1cb3b1   <'rabbit@openstack-01'.1.9991.35>   3   true
dhcp_agent.openstack-03.novalocal   <'rabbit@openstack-01'.1.10313.35>  2   true
dhcp_agent.openstack-03.novalocal   <'rabbit@openstack-01'.1.10464.35>  2   true
dhcp_agent.openstack-03.novalocal   <'rabbit@openstack-01'.1.10496.35>  1   true
dhcp_agent.openstack-03.novalocal.openstack-03.novalocal    <'rabbit@openstack-01'.1.10496.35>  2   true
dhcp_agent.openstack-03.novalocal_fanout_fcaed4cc7a0d4e3e94f35bea3409cc4d   <'rabbit@openstack-01'.1.10496.35>  3   true
dhcp_agent.openstack-04.novalocal   <'rabbit@openstack-01'.1.10659.35>  1   true
dhcp_agent.openstack-04.novalocal   <'rabbit@openstack-01'.1.10768.35>  2   true
dhcp_agent.openstack-04.novalocal   <'rabbit@openstack-01'.1.10903.35>  2   true
dhcp_agent.openstack-04.novalocal.openstack-04.novalocal    <'rabbit@openstack-01'.1.10659.35>  2   true
dhcp_agent.openstack-04.novalocal_fanout_de1d20e7e5b647edbdabce231d8f1eac   <'rabbit@openstack-01'.1.10659.35>  3   true
dhcp_agent_fanout_6c820b6e9ca04299abc796ad6035e8cc  <'rabbit@openstack-01'.1.10055.35>  3   true
dhcp_agent_fanout_76442de216f34d16aa69d6f7c72eebb1  <'rabbit@openstack-01'.1.10903.35>  3   true
dhcp_agent_fanout_adbc15f5242e4b90be2e28d99f502b19  <'rabbit@openstack-01'.1.10464.35>  3   true
dhcp_agent_fanout_ba24b6438c8f4193823943acef87a93a  <'rabbit@openstack-01'.1.10313.35>  3   true
dhcp_agent_fanout_ec9d0243330a444abaaf71d2908121eb  <'rabbit@openstack-01'.1.10023.35>  3   true
dhcp_agent_fanout_f313396733f1490c86b66f93b53ea4fa  <'rabbit@openstack-01'.1.10768.35>  3   true
l3_agent    <'rabbit@openstack-01'.1.9933.35>   1   true
l3_agent    <'rabbit@openstack-01'.1.10183.35>  1   true
l3_agent    <'rabbit@openstack-01'.1.10544.35>  1   true
l3_agent    <'rabbit@openstack-01'.1.10576.35>  1   true
l3_agent    <'rabbit@openstack-01'.1.11034.35>  1   true
l3_agent    <'rabbit@openstack-01'.1.11068.35>  1   true
l3_agent.openstack-02.novalocal <'rabbit@openstack-01'.1.9933.35>   2   true
l3_agent.openstack-02.novalocal <'rabbit@openstack-01'.1.10177.35>  1   true
l3_agent.openstack-02.novalocal <'rabbit@openstack-01'.1.10183.35>  2   true
l3_agent.openstack-02.novalocal.openstack-02.novalocal  <'rabbit@openstack-01'.1.10177.35>  2   true
l3_agent.openstack-02.novalocal_fanout_abc9e58899d24dea9757c9b9de7ad084 <'rabbit@openstack-01'.1.10177.35>  3   true
l3_agent.openstack-03.novalocal <'rabbit@openstack-01'.1.10372.35>  1   true
l3_agent.openstack-03.novalocal <'rabbit@openstack-01'.1.10544.35>  2   true
l3_agent.openstack-03.novalocal <'rabbit@openstack-01'.1.10576.35>  2   true
l3_agent.openstack-03.novalocal.openstack-03.novalocal  <'rabbit@openstack-01'.1.10372.35>  2   true
l3_agent.openstack-03.novalocal_fanout_85c125f6cd8d4f67a8bda949b1b44367 <'rabbit@openstack-01'.1.10372.35>  3   true
l3_agent.openstack-04.novalocal <'rabbit@openstack-01'.1.11034.35>  2   true
l3_agent.openstack-04.novalocal <'rabbit@openstack-01'.1.11047.35>  1   true
l3_agent.openstack-04.novalocal <'rabbit@openstack-01'.1.11068.35>  2   true
l3_agent.openstack-04.novalocal.openstack-04.novalocal  <'rabbit@openstack-01'.1.11047.35>  2   true
l3_agent.openstack-04.novalocal_fanout_abd453ab374e460fa8dba368f475de50 <'rabbit@openstack-01'.1.11047.35>  3   true
l3_agent_fanout_22fe4369f9c94c6abdb157d967806ca7    <'rabbit@openstack-01'.1.10576.35>  3   true
l3_agent_fanout_2f5c74b89297454c9068f2681773c749    <'rabbit@openstack-01'.1.10183.35>  3   true
l3_agent_fanout_3824a31696274bba8e6fb0c92a49610e    <'rabbit@openstack-01'.1.9933.35>   3   true
l3_agent_fanout_4293729cb958437fb52c6cdd04c76726    <'rabbit@openstack-01'.1.11068.35>  3   true
l3_agent_fanout_5129fab6dcfe494287b5a1417afcdf91    <'rabbit@openstack-01'.1.10544.35>  3   true
l3_agent_fanout_af7a3f7127e74b7697bdd7be0f914baf    <'rabbit@openstack-01'.1.11034.35>  3   true
n-lbaas-plugin  <'rabbit@openstack-01'.1.9375.35>   1   true
n-lbaas-plugin.openstack-01.novalocal   <'rabbit@openstack-01'.1.9375.35>   2   true
n-lbaas-plugin_fanout_258b582e2a954e1c89daafc26a2fc193  <'rabbit@openstack-01'.1.9375.35>   3   true
n-lbaas_agent   <'rabbit@openstack-01'.1.10231.35>  1   true
n-lbaas_agent   <'rabbit@openstack-01'.1.10243.35>  1   true
n-lbaas_agent   <'rabbit@openstack-01'.1.10696.35>  1   true
n-lbaas_agent   <'rabbit@openstack-01'.1.10726.35>  1   true
n-lbaas_agent   <'rabbit@openstack-01'.1.10941.35>  1   true
n-lbaas_agent   <'rabbit@openstack-01'.1.11003.35>  1   true
n-lbaas_agent.openstack-02.novalocal    <'rabbit@openstack-01'.1.10231.35>  2   true
n-lbaas_agent.openstack-02.novalocal    <'rabbit@openstack-01'.1.10237.35>  1   true
n-lbaas_agent.openstack-02.novalocal    <'rabbit@openstack-01'.1.10243.35>  2   true
n-lbaas_agent.openstack-02.novalocal.openstack-02.novalocal <'rabbit@openstack-01'.1.10237.35>  2   true
n-lbaas_agent.openstack-02.novalocal_fanout_4bbd290480a541c0a0f410f0b5bbe949    <'rabbit@openstack-01'.1.10237.35>  3   true
n-lbaas_agent.openstack-03.novalocal    <'rabbit@openstack-01'.1.10503.35>  1   true
n-lbaas_agent.openstack-03.novalocal    <'rabbit@openstack-01'.1.10696.35>  2   true
n-lbaas_agent.openstack-03.novalocal    <'rabbit@openstack-01'.1.10726.35>  2   true
n-lbaas_agent.openstack-03.novalocal.openstack-03.novalocal <'rabbit@openstack-01'.1.10503.35>  2   true
n-lbaas_agent.openstack-03.novalocal_fanout_9f9e6aeeb5974eb79fdde505155d3541    <'rabbit@openstack-01'.1.10503.35>  3   true
n-lbaas_agent.openstack-04.novalocal    <'rabbit@openstack-01'.1.10941.35>  2   true
n-lbaas_agent.openstack-04.novalocal    <'rabbit@openstack-01'.1.10987.35>  1   true
n-lbaas_agent.openstack-04.novalocal    <'rabbit@openstack-01'.1.11003.35>  2   true
n-lbaas_agent.openstack-04.novalocal.openstack-04.novalocal <'rabbit@openstack-01'.1.10987.35>  2   true
n-lbaas_agent.openstack-04.novalocal_fanout_c22854c4edc844c68965a6635750d334    <'rabbit@openstack-01'.1.10987.35>  3   true
n-lbaas_agent_fanout_1ee61b4ea0b9430fa80b9d7a39aca0ac   <'rabbit@openstack-01'.1.10726.35>  3   true
n-lbaas_agent_fanout_45e2e46e7fea4703a11c070ece7857e8   <'rabbit@openstack-01'.1.10696.35>  3   true
n-lbaas_agent_fanout_7d6add7137f148dda3fed7042336c7ff   <'rabbit@openstack-01'.1.11003.35>  3   true
n-lbaas_agent_fanout_9eb1723673f24d54a1cce88d972b2e51   <'rabbit@openstack-01'.1.10231.35>  3   true
n-lbaas_agent_fanout_aedcd117d4164c3e8ce075fd2eedfa99   <'rabbit@openstack-01'.1.10243.35>  3   true
n-lbaas_agent_fanout_ebbfd590e4bf4dff826604c78c6ba3a6   <'rabbit@openstack-01'.1.10941.35>  3   true
q-agent-notifier-dvr-update <'rabbit@openstack-01'.1.9477.35>   1   true
q-agent-notifier-dvr-update <'rabbit@openstack-01'.1.11131.35>  1   true
q-agent-notifier-dvr-update <'rabbit@openstack-01'.1.25095.254> 1   true
q-agent-notifier-dvr-update.openstack-02.novalocal  <'rabbit@openstack-01'.1.9477.35>   2   true
q-agent-notifier-dvr-update.openstack-03.novalocal  <'rabbit@openstack-01'.1.25095.254> 2   true
q-agent-notifier-dvr-update.openstack-04.novalocal  <'rabbit@openstack-01'.1.11131.35>  2   true
q-agent-notifier-dvr-update_fanout_08a70af4b8484650bd1873bf30500f14 <'rabbit@openstack-01'.1.25095.254> 3   true
q-agent-notifier-dvr-update_fanout_5f4066e44705427eb8d417b2a23aec76 <'rabbit@openstack-01'.1.9477.35>   3   true
q-agent-notifier-dvr-update_fanout_db613360bc364ad4a05db1550b0b58dc <'rabbit@openstack-01'.1.11131.35>  3   true
q-agent-notifier-network-delete <'rabbit@openstack-01'.1.9451.35>   1   true
q-agent-notifier-network-delete <'rabbit@openstack-01'.1.10889.35>  1   true
q-agent-notifier-network-delete <'rabbit@openstack-01'.1.24786.254> 1   true
q-agent-notifier-network-delete.openstack-02.novalocal  <'rabbit@openstack-01'.1.9451.35>   2   true
q-agent-notifier-network-delete.openstack-03.novalocal  <'rabbit@openstack-01'.1.24786.254> 2   true
q-agent-notifier-network-delete.openstack-04.novalocal  <'rabbit@openstack-01'.1.10889.35>  2   true
q-agent-notifier-network-delete_fanout_1965391112ec45ee82bf15f68a02936a <'rabbit@openstack-01'.1.24786.254> 3   true
q-agent-notifier-network-delete_fanout_42d77d86515c476b8bd0bc44732a40b3 <'rabbit@openstack-01'.1.10889.35>  3   true
q-agent-notifier-network-delete_fanout_da1e307bd54c49f88ec514011bbf6609 <'rabbit@openstack-01'.1.9451.35>   3   true
q-agent-notifier-port-update    <'rabbit@openstack-01'.1.9437.35>   1   true
q-agent-notifier-port-update    <'rabbit@openstack-01'.1.10993.35>  1   true
q-agent-notifier-port-update    <'rabbit@openstack-01'.1.24942.254> 1   true
q-agent-notifier-port-update.openstack-02.novalocal <'rabbit@openstack-01'.1.9437.35>   2   true
q-agent-notifier-port-update.openstack-03.novalocal <'rabbit@openstack-01'.1.24942.254> 2   true
q-agent-notifier-port-update.openstack-04.novalocal <'rabbit@openstack-01'.1.10993.35>  2   true
q-agent-notifier-port-update_fanout_2a6755a1b1334554bc621755782e4fbf    <'rabbit@openstack-01'.1.24942.254> 3   true
q-agent-notifier-port-update_fanout_a6fd2e90877e49738a03b0c0518fce23    <'rabbit@openstack-01'.1.9437.35>   3   true
q-agent-notifier-port-update_fanout_b6726f033e4249e5903232bcdd691f40    <'rabbit@openstack-01'.1.10993.35>  3   true
q-agent-notifier-security_group-update  <'rabbit@openstack-01'.1.9471.35>   1   true
q-agent-notifier-security_group-update  <'rabbit@openstack-01'.1.11116.35>  1   true
q-agent-notifier-security_group-update  <'rabbit@openstack-01'.1.24301.254> 1   true
q-agent-notifier-security_group-update.openstack-02.novalocal   <'rabbit@openstack-01'.1.9471.35>   2   true
q-agent-notifier-security_group-update.openstack-03.novalocal   <'rabbit@openstack-01'.1.24301.254> 2   true
q-agent-notifier-security_group-update.openstack-04.novalocal   <'rabbit@openstack-01'.1.11116.35>  2   true
q-agent-notifier-security_group-update_fanout_080b030f39a849cf81796507aabe2369  <'rabbit@openstack-01'.1.11116.35>  3   true
q-agent-notifier-security_group-update_fanout_270078481bcd4422b8b91c035b170ecb  <'rabbit@openstack-01'.1.9471.35>   3   true
q-agent-notifier-security_group-update_fanout_a823ef30d8e54e648b7a670641ed04d6  <'rabbit@openstack-01'.1.24301.254> 3   true
q-agent-notifier-tunnel-update  <'rabbit@openstack-01'.1.9664.35>   1   true
q-agent-notifier-tunnel-update  <'rabbit@openstack-01'.1.11110.35>  1   true
q-agent-notifier-tunnel-update  <'rabbit@openstack-01'.1.25015.254> 1   true
q-agent-notifier-tunnel-update.openstack-02.novalocal   <'rabbit@openstack-01'.1.9664.35>   2   true
q-agent-notifier-tunnel-update.openstack-03.novalocal   <'rabbit@openstack-01'.1.25015.254> 2   true
q-agent-notifier-tunnel-update.openstack-04.novalocal   <'rabbit@openstack-01'.1.11110.35>  2   true
q-agent-notifier-tunnel-update_fanout_101f9d61f2d341c380c6e1c10a22e572  <'rabbit@openstack-01'.1.9664.35>   3   true
q-agent-notifier-tunnel-update_fanout_5bf260a186ff4075818b13b5d8e58e62  <'rabbit@openstack-01'.1.25015.254> 3   true
q-agent-notifier-tunnel-update_fanout_edfb77bf0ae74c139909f6e21edb6f1c  <'rabbit@openstack-01'.1.11110.35>  3   true
q-l3-plugin <'rabbit@openstack-01'.1.9252.35>   1   true
q-l3-plugin.openstack-01.novalocal  <'rabbit@openstack-01'.1.9252.35>   2   true
q-l3-plugin_fanout_d1d00128c98b42d4a7fb55b71a96ae97 <'rabbit@openstack-01'.1.9252.35>   3   true
q-plugin    <'rabbit@openstack-01'.1.9280.35>   1   true
q-plugin.openstack-01.novalocal <'rabbit@openstack-01'.1.9280.35>   2   true
q-plugin_fanout_76adbea5524b4de99b158215fb1db56a    <'rabbit@openstack-01'.1.9280.35>   3   true
reply_07adc5aef68b4e3db8a61ffb7a502c5c  <'rabbit@openstack-01'.1.25500.254> 1   true
reply_1d32023d7ca1451986a7a3534a818e2f  <'rabbit@openstack-01'.1.6427.8>    1   true
reply_241688a279c0414d90e3b76b162fdb33  <'rabbit@openstack-01'.1.10538.35>  1   true
reply_2a768322ee9b4c3ea355de73b0374f74  <'rabbit@openstack-01'.1.24382.11>  1   true
reply_2ceed19e376b4cf78373f8e1f98c1f39  <'rabbit@openstack-01'.1.10057.35>  1   true
reply_38b4c8d7d7aa4d03a6355ec8485e0258  <'rabbit@openstack-01'.1.10469.35>  1   true
reply_40bd0d232bad4b469772b1a6ae7b9266  <'rabbit@openstack-01'.1.10875.35>  1   true
reply_5050b471ac05454baf9e6145121ca7c7  <'rabbit@openstack-01'.1.10075.35>  1   true
reply_6bae0879fe5b413c9ac3595fa3cbfbbf  <'rabbit@openstack-01'.1.10939.35>  1   true
reply_7d304be0842a48c8b51268f7ec41b02f  <'rabbit@openstack-01'.1.10024.35>  1   true
reply_9f1867d6c7ce4051a377861412427191  <'rabbit@openstack-01'.1.10101.35>  1   true
reply_9f9bf21f51aa427990e5000aa4a2d0b7  <'rabbit@openstack-01'.1.294.0> 1   true
reply_ab28f6fe778c48618d4602ea3c5ace73  <'rabbit@openstack-01'.1.10573.35>  1   true
reply_b02bff3bc22c444fab3ff258081430ba  <'rabbit@openstack-01'.1.10840.35>  1   true
reply_bf4c9dcbf4ed4ddea6a482c2db5e1e0e  <'rabbit@openstack-01'.1.10769.35>  1   true
reply_ce584f808713423ca834d7b146c6c9e9  <'rabbit@openstack-01'.1.988.0> 1   true
reply_e95a8b2de2814843bb6b83d28c7abeed  <'rabbit@openstack-01'.1.9723.35>   1   true
reply_e9885a8dcf214007934d0d8aa0a39ef5  <'rabbit@openstack-01'.1.5485.8>    1   true
reply_eaa8cf9d5520414688a8b29b9db20543  <'rabbit@openstack-01'.1.10476.35>  1   true
reply_f82f54130ee24b91a4be06a4cadc704d  <'rabbit@openstack-01'.1.10755.35>  1   true
scheduler   <'rabbit@openstack-01'.1.668.0> 1   true
scheduler.openstack-01.novalocal    <'rabbit@openstack-01'.1.668.0> 2   true
scheduler_fanout_318cb1685bac44b4bda11b12f967098d   <'rabbit@openstack-01'.1.668.0> 3   true
...done.
```

## Intercept Message

To intercept neutron exchange messages. Code based on [Intercept RabbitMQ messages in Openstack nova](http://prosuncsedu.wordpress.com/2013/11/09/intercept-rabbitmq-messages-in-openstack-nova/). The script will ignore 'report_state' messages of neutron. 

```
vim ~/intercept_rabbit.py

# == below is the script ==
#!/usr/bin/env python
import pika
import sys
import json

global message_count
message_count = 0

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.224.147.166',
                            credentials=pika.PlainCredentials('root', '123work')))

exchange_name="neutron"  # CHANGE according to your need
queue_name = "interept_rabbit"
binding_key = "#"

channel = connection.channel()
channel.exchange_declare(exchange = exchange_name, type='topic')

result = channel.queue_declare(queue=queue_name, exclusive=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

def callback(ch, method, properties, body):
  global message_count
  message_count = message_count + 1
  #import pdb; pdb.set_trace()
  body_obj = json.loads(body)
  if 'oslo.message' in body_obj and r'"method": "report_state"' in body_obj['oslo.message']:
    return

  if 'oslo.message' in body_obj:
    body_obj['oslo.message'] = json.loads(body_obj['oslo.message'])
  print "\n\n"
  print ("----------------{}th message -----------------\n".format(message_count))
  print " routing_key: %r" % method.routing_key
  print json.dumps(body_obj, indent=4, sort_keys=True)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

print 'Waiting for logs. To exit press CTRL+C'
channel.start_consuming()
```

The script dequeues message from rabbitmq, which is destructive to the original openstack functionality. In rabbitmq, peek message rather than dequeue it seems no easy way. Refer to [here](http://stackoverflow.com/questions/4700292/using-rabbitmq-is-there-a-way-to-look-at-the-queue-contents-without-a-dequeue).

## References

* [Intercept Rabbitmq Message In Openstack Nova](http://prosuncsedu.wordpress.com/2013/11/09/intercept-rabbitmq-messages-in-openstack-nova/)
* [Nova AMQP Model](http://docs.openstack.org/developer/nova/devref/rpc.html)
