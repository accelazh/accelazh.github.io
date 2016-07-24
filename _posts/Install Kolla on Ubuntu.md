

1. using ubuntu 14.04
2. on machine 192.168.88.130 as ansible master

Enable sshd password auth on each machine

```
vim /etc/ssh/sshd_config
...	# set "PasswordAuthentication yes"
service ssh restart
```


=====
On ansible master machine

```
yum install -y ansible
```

Generate ssh key pair

```
ssh-keygen
... # Keep pressing Enter
```

```
# For each machine as ansible's slaves
ssh-copy-id labadmin@10.13.182.120
...
```

====


After diving Kolla code on github. I found not clue related to Kubernetes. They use a lot of docker-compose. Ansible is newly brought in. Kolla can also use heat to deploy its nodes.
       Found below mail threads
            https://openstack.nimeyo.com/39170/openstack-dev-kolla-why-we-didnt-use-k8s-in-kolla says 
                1. Kubernetes doesn’t offer a control or integration point. We have that now with docker-compose.
                2. Kubernetes doesn’t offer super privileged containers. We need that in order to operate an OpenStack environment.
            http://osdir.com/ml/openstack-dev/2015-03/msg02140.html says
                 Kubernetes has been deprecated because it doesn’t provide super privileged containers.




To execute

ansible-playbook -i usa-dev.inventory -K ./site.yml --check


=====
Another thread:
  
```
cd ~/workspace
git clone https://github.com/stackforge/kolla.git
cd kolla
chmod a+x tools/
tools/genenv
sudo tools/kolla start
```