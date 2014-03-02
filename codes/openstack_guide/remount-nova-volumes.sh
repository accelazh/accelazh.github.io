#! /bin/bash
loopid=`/sbin/losetup --show -f /srv/nova-volumes.img`
/sbin/vgcreate nova-volumes $loopid
