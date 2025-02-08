---
layout: post
title: "Config Postfix Mail Server"
tagline : "Config Postfix Mail Server"
description: "Config Postfix Mail Server"
category: "Linux"
tags: [mail, postfix]
---
{% include JB/setup %}

If an application wants to send mail out, besides you have to config your application correctly, you have to install mail server on localhost. The localhost mail server will finially send mails to and mail replay. 

We use postfix as localhost mail server here. First, change hostname to match the domain of the localhost SMTP server. Suppose domain is `testmail.com`

```
sudo su -
# change hostname to '*.testmail.com'. here we use 'hahaha.testmail.com'
hostname hahaha.testmail.com
vim /etc/hosts
append " hahaha.testmail.com" to line "127.0.0.1 ..."
vim /etc/sysconfig/network
change HOSTNAME to "HOSTNAME=hahaha.testmail.com"
```

Config postfix. To troubleshoot check /var/log/maillog

```
sudo su -
# config postfix
vim /etc/postfix/main.cf
change
  myorigin = $mydomain
  inet_interfaces = all
  mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
  relay_domains = $mydestination, mail.public.com
  relayhost = 10.224.123.223 # it is on domain "mail.public.com"
  debug_peer_level = 10
 
# optionally, to enable logging mail subjects
vim /etc/postfix/main.cf
change
  header_checks = regexp:/etc/postfix/header_checks
vim /etc/postfix/header_checks
append
  /^subject:/ WARN
```

Restart postfix

```
service postfix restart
```

Next, we need the next mail relay to accept our mails. Ask owner of 10.224.123.223 to allow our access.
