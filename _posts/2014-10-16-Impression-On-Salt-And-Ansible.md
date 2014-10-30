---
layout: post
title: "Impression on Salt and Ansible"
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
    
    * Salt state, the SLS file, stands in the role of Ansible's playbook. SLS file is originally declarative and executed in lexicographical order like puppet. But from salt 0.17, [state-auto-order](http://docs.saltstack.com/en/latest/topics/releases/0.17.0.html?highlight=auto%20order#state-auto-order) feature is added, and now SLS file is executed in declared order in file.

    * I once want to use SLS as a set of commends, like Ansible's playbook. When I want to invoke another SLS file, I have to use "include".  But "include" can only be used once in each SLS file, because it is originally designed to declare states.

* Salt works in master/slave (called master/minion) and requires both agent installed on both side, which may be prohibited by application developers. Salt provide another mode to do masterless local apply (salt-call), like puppet local apply, but still need to install agent on local machine.

    * Salt provides "[salt-ssh](http://docs.saltstack.com/en/latest/topics/ssh/)", which is the agentless solution. However, salt-ssh does lack certain supports to salt functions, refer to [issue-9851](https://github.com/saltstack/salt/issues/9851). It is said to be still alpha. 


* Salt is definitely more complex than ansible. Ansible uses very straight forward approach, ssh, while salt has many more components.

* Ansible stream outputs while executing, while Salt prints them out only after all finished. The command results are printed in random order from when they are executed. Here is a [discussion](https://groups.google.com/forum/#!topic/salt-users/ikAVtZnuB30).

## References

* Saltstack walkthrough: <http://docs.saltstack.com/en/latest/topics/tutorials/walkthrough.html>
* Salt vs Ansible vs Puppet: <http://ryandlane.com/blog/2014/08/04/moving-away-from-puppet-saltstack-or-ansible/>
