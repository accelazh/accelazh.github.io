#! /bin/bash

service qpidd restart
service libvirtd restart
for services in `ls /etc/init.d/openstack*` ;
 do $services restart;
done
nova-manage service list
nova-manage network list
