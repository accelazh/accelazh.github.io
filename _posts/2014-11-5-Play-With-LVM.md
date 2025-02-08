---
layout: post
title: "Play with LVM"
tagline : "Play with LVM"
description: "Play with LVM"
category: "Linux"
tags: [storage, volume, lvm]
---
{% include JB/setup %}

I'm working on a CentOS 7 VM. First, check disk space usage

```
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        40G  1.9G   39G   5% /
devtmpfs        1.9G     0  1.9G   0% /dev
tmpfs           1.9G     0  1.9G   0% /dev/shm
tmpfs           1.9G   41M  1.9G   3% /run
tmpfs           1.9G     0  1.9G   0% /sys/fs/cgroup
```

LVM works this way (borrowed from [here](http://www.turnkeylinux.org/blog/extending-lvm)):

```
PV[s] (Physical Volumes) -> VG[s] (Volume Groups) -> LV[s] (Logical Volumes) -> Filesystems
```

LVM concept layout (borrowed from [here](http://www.linuxdevcenter.com/pub/a/linux/2006/04/27/managing-disk-space-with-lvm.html)):

![LVM concept layout](/images/lvm-layout.gif "LVM concept layout")

## Fake Several Disks

I have only one disk but to play with LVM I need more. Let's fake them using [loop device](http://blog.csdn.net/ustc_dylan/article/details/6878252).

```
# use dd to create some disk images
dd if=/dev/zero of=disk1.img bs=1 count=1 seek=1G
dd if=/dev/zero of=disk2.img bs=1 count=1 seek=1G

# fake the pseudo block device
losetup /dev/loop1 disk1.img
losetup /dev/loop1 disk2.img

# to uninstall
# losetup -d /dev/loop1
# losetup -d /dev/loop2
```

Now list block devices

```
$ ll -h
-rw-r--r--  1 root root 1.1G Nov  4 14:21 disk1.img
-rw-r--r--  1 root root 1.1G Nov  4 14:21 disk2.img
$ ll -h /dev/vd*
brw-rw---- 1 root disk 253, 0 Oct 29 12:16 /dev/vda
brw-rw---- 1 root disk 253, 1 Oct 29 12:16 /dev/vda1
$ ll -h /dev/loop*
brw-rw---- 1 root disk  7,   1 Nov  4 14:22 /dev/loop1
brw-rw---- 1 root disk  7,   2 Nov  4 14:23 /dev/loop2
crw------- 1 root root 10, 237 Nov  4 14:22 /dev/loop-control 
```

Leave disk2 as raw disk. Format disk1 with partitions. For how to use [fdisk](http://tldp.org/HOWTO/Partition/fdisk_partitioning.html).

```
$ fdisk /dev/loop1
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x6fba7944.

Command (m for help): p

Disk /dev/loop1: 1073 MB, 1073741824 bytes, 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x6fba7944

      Device Boot      Start         End      Blocks   Id  System

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-2097151, default 2048): 
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-2097151, default 2097151): +500M
Partition 1 of type Linux and of size 500 MiB is set

Command (m for help): n
Partition type:
   p   primary (1 primary, 0 extended, 3 free)
   e   extended
Select (default p): p
Partition number (2-4, default 2): 
First sector (1026048-2097151, default 1026048): 
Using default value 1026048
Last sector, +sectors or +size{K,M,G} (1026048-2097151, default 2097151): 
Using default value 2097151
Partition 2 of type Linux and of size 523 MiB is set

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 22: Invalid argument.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
Syncing disks.

# checkout the result
$ fdisk -l /dev/loop1

Disk /dev/loop1: 1073 MB, 1073741824 bytes, 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x6fba7944

      Device Boot      Start         End      Blocks   Id  System
/dev/loop1p1            2048     1026047      512000   83  Linux
/dev/loop1p2         1026048     2097151      535552   83  Linux
$ fdisk -l /dev/loop2

Disk /dev/loop2: 1073 MB, 1073741824 bytes, 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
$ fdisk -l disk1.img 

Disk disk1.img: 1073 MB, 1073741824 bytes, 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x6fba7944

    Device Boot      Start         End      Blocks   Id  System
disk1.img1            2048     1026047      512000   83  Linux
disk1.img2         1026048     2097151      535552   83  Linux
```

Next we need mount partitions of /dev/loop1. Refer to [here](http://madduck.net/blog/2006.10.20:loop-mounting-partitions-from-a-disk-image/).

```
$ fdisk -l /dev/loop1

Disk /dev/loop1: 1073 MB, 1073741824 bytes, 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0xc6df6cca

      Device Boot      Start         End      Blocks   Id  System
/dev/loop1p1            2048     1050623      524288   83  Linux
/dev/loop1p2         1050624     2097151      523264   83  Linux

# mount the partitions
$ losetup /dev/loop11 disk1.img -o $((2048 * 512)) --sizelimit $((1048575 * 512))
$ losetup /dev/loop12 disk1.img -o $((1050624 * 512)) --sizelimit $((1046527 * 512))
$ ll -h /dev/loop*
brw-rw---- 1 root disk  7,   1 Nov  4 15:10 /dev/loop1
brw-rw---- 1 root disk  7,  11 Nov  4 15:10 /dev/loop11
brw-rw---- 1 root disk  7,  12 Nov  4 15:11 /dev/loop12
brw-rw---- 1 root disk  7,   2 Nov  4 14:52 /dev/loop2
crw------- 1 root root 10, 237 Nov  4 14:22 /dev/loop-control
```

After that, let's test whether the two partitions can work (hope they won't overwrite each other by wrong settings)

```
$ mkfs.ext4 /dev/loop11
$ mkfs.ext4 /dev/loop12
$ mount /dev/loop11 /mnt/disk11
$ mount /dev/loop12 /mnt/disk12

$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        40G  2.6G   38G   7% /
devtmpfs        1.9G     0  1.9G   0% /dev
tmpfs           1.9G     0  1.9G   0% /dev/shm
tmpfs           1.9G   41M  1.9G   3% /run
tmpfs           1.9G     0  1.9G   0% /sys/fs/cgroup
/dev/loop11     488M  2.3M  456M   1% /mnt/disk11
/dev/loop12     487M  2.3M  456M   1% /mnt/disk12

$ echo "hello world! this is disk11" > /mnt/disk11/msg
$ echo "hello world! this is disk12" > /mnt/disk12/msg

$ umount /mnt/disk11
$ umount /mnt/disk12
$ mount /dev/loop11 /mnt/disk12
$ mount /dev/loop12 /mnt/disk11
$ cat /mnt/disk11/msg
hello world! this is disk12
$ cat /mnt/disk12/msg
hello world! this is disk11

$ umount /mnt/disk11
$ umount /mnt/disk12
```

## Play with LVM

If you are ecountering this error

```
$ pvdisplay
  /run/lvm/lvmetad.socket: connect failed: No such file or directory
  WARNING: Failed to connect to lvmetad: No such file or directory. Falling back to internal scanning.
  /run/lvm/lvmetad.socket: connect failed: No such file or directory
  /run/lvm/lvmetad.socket: connect failed: No such file or directory
  /run/lvm/lvmetad.socket: connect failed: No such file or directory
  /run/lvm/lvmetad.socket: connect failed: No such file or directory
```

You have to start lvm service. Refer to [here](https://bbs.archlinux.org/viewtopic.php?id=174996).

```
service lvm2-lvmetad start
chkconfig lvm2-lvmetad on
```

Following this [tutorial](http://www.linuxdevcenter.com/pub/a/linux/2006/04/27/managing-disk-space-with-lvm.html?page=1). First step, create physical volume. Either a partition or a disk can be added.

```
$ pvcreate /dev/loop12 /dev/loop2
WARNING: ext4 signature detected on /dev/loop12 at offset 1080. Wipe it? [y/n] y
  Wiping ext4 signature on /dev/loop12.
  Physical volume "/dev/loop12" successfully created
  Physical volume "/dev/loop2" successfully created
$ pvdisplay
  "/dev/loop12" is a new physical volume of "511.00 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/loop12
  VG Name               
  PV Size               511.00 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               EkFO3Y-CRQT-QrSy-07pK-i72g-zf9o-bwKLtY
   
  "/dev/loop2" is a new physical volume of "1.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/loop2
  VG Name               
  PV Size               1.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               mPF1vW-Ja2T-LKTP-N68T-S1jU-COue-kC4jZq
   
  "/dev/loop1" is a new physical volume of "1.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/loop1
  VG Name               
  PV Size               1.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               Yq8UUq-MVpl-wNST-kThs-eRoc-UKfq-Gg0xhY
```

Step two, create volume group. You can see the total VG size.

```
$ vgcreate test1 /dev/loop12 /dev/loop2
  /proc/devices: No entry for device-mapper found
  /proc/devices: No entry for device-mapper found
  Volume group "test1" successfully created
$ vgdisplay
  --- Volume group ---
  VG Name               test1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               1.49 GiB
  PE Size               4.00 MiB
  Total PE              382
  Alloc PE / Size       0 / 0   
  Free  PE / Size       382 / 1.49 GiB
  VG UUID               tQCjut-3BsW-fGY8-GtLD-27Nd-VFtF-T7MYCh
```

Step three, create the logic volumes

```
$ lvcreate --name test11 --size 256M test1
  Logical volume "test11" created
$ lvcreate --name test12 --size 256M test1
  Logical volume "test12" created
$ lvcreate --name test13 --size 256M test1
  Logical volume "test13" created
$ lvdisplay
  --- Logical volume ---
  LV Path                /dev/test1/test11
  LV Name                test11
  VG Name                test1
  LV UUID                elD2Ua-UAOm-6aIu-9zSd-FUQH-dhmu-0l72jj
  LV Write Access        read/write
  LV Creation host, time openstack-01.novalocal, 2014-11-04 15:32:28 +0000
  LV Status              available
  # open                 0
  LV Size                256.00 MiB
  Current LE             64
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           252:0
   
  --- Logical volume ---
  LV Path                /dev/test1/test12
  LV Name                test12
  VG Name                test1
  LV UUID                FhBVnx-Mooc-WW46-biCP-eJu7-XmyM-0Sgdoy
  LV Write Access        read/write
  LV Creation host, time openstack-01.novalocal, 2014-11-04 15:32:31 +0000
  LV Status              available
  # open                 0
  LV Size                256.00 MiB
  Current LE             64
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           252:1
   
  --- Logical volume ---
  LV Path                /dev/test1/test13
  LV Name                test13
  VG Name                test1
  LV UUID                LDz7ih-pKlp-1Fb3-e8dH-lEkI-lzQM-tZT7oM
  LV Write Access        read/write
  LV Creation host, time openstack-01.novalocal, 2014-11-04 15:32:34 +0000
  LV Status              available
  # open                 0
  LV Size                256.00 MiB
  Current LE             64
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           252:2
```

Now we have the volume devices under /dev

```
$ ll /dev/test1/
total 0
lrwxrwxrwx 1 root root 7 Nov  4 15:32 test11 -> ../dm-0
lrwxrwxrwx 1 root root 7 Nov  4 15:32 test12 -> ../dm-1
lrwxrwxrwx 1 root root 7 Nov  4 15:32 test13 -> ../dm-2
```

You can mkfs.* and mount them now.

