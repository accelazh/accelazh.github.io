---
layout: post
title: "First Impression on Salt and Ansible"
tagline : " First impression on salt and ansible"
description: "First impression on salt and ansible, with a basic comparasion"
category: "orchestration"
tags: [cloud, deploy, orechestration]
---
{% include JB/setup %}

## Overall Impression

**Commons between Salt & Ansible**

    * Both are considered next generation replacement for puppet
    
    * They are considered mature enough. [Here](http://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html) gives comments.
    
    * Both provide connectors to cloud (Openstack, AWS, Rackspace, ...).
    
    * Both provide orchestration templates.

**Outstanding difference between Salt & Ansible**

    * Salt and ansible both provide remote command execution, which is in procedural language style. However, salt can also declare and apply states (salt state), which is in declarative language style. I.e. "maintain by state" rather than write command procedure, which is also the core of puppet. Ansible doesn't have it.

    * Salt works in master/slave (called master/minion) and requires both agent installed on both side, which may be prohibited by application developers. Salt provide another mode to do masterless local apply (salt-call), like puppet local apply, but still need to install agent on local machine.

    * Salt is definitely more complex than ansible. Ansible uses very straight forward approach, ssh, while salt has many more components.

## References

    * Saltstack walkthrough: <http://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html>
    * Salt vs Ansible vs Puppet: <http://ryandlane.com/blog/2014/08/04/moving-away-from-puppet-saltstack-or-ansible/>
        * This is definitely a very good and complete compare between them.