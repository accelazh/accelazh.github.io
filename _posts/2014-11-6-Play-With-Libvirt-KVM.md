---
layout: post
title: "Play with Libvirt/KVM"
tagline : "Play with Libvirt/KVM"
description: "Play with Libvirt/KVM"
category: "virtualization"
tags: [virtualization, kvm, libvirt, compute]
---
{% include JB/setup %}

## Create the VMs

Following [IBM KVM installation guide](http://www-01.ibm.com/support/knowledgecenter/linuxonibm/liaai/kvminstall/liaaikvminstallstart.htm) to install kvm and libvirt. Play on a virtual CentOS 7. (There is also a [developer version guide](http://www-01.ibm.com/support/knowledgecenter/linuxonibm/liaai/kvmadv/kvmadvstart.htm))

```
# check Intel-VT and AMD-V, the hardware-assisted virtualization is supported
grep -E 'vmx|svm' /proc/cpuinfo

# ensure you are not running Xen kernel
uname -a # see '2.6.18-164.el5Xen' means Xen kernel is running

# install packages
yum install -y kvm virt-manager libvirt libvirt-python python-virtinst virt-install qemu-kvm

# start libvirt
service libvirtd start
chkconfig libvirtd on
```

Download a cirros image to use. [qemu-img](http://smilejay.com/2012/08/qemu-img-details/) is versatile.

```
wget --no-check-certificate https://download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img
qemu-img info cirros-0.3.2-x86_64-disk.img # show image format (qcow2)
```

Create the cirros guest. Note that the ~/cirros-0.3.2-x86_64-disk.img will be modified and used as VM's disk file. The owner is changed to qemu:qemu.

```
# install seabios to prevent "qemu: could not load PC BIOS 'bios-256k.bin'" error
yum install seabios-bin
# create and start cirros
virt-install --connect=qemu:///system --name=cirros --ram=512 --vcpus=1 --disk path=cirros-0.3.2-x86_64-disk.img,format=qcow2 --import --network network:default --vnc
```

The configuration locates at /etc/libvirt/qemu/cirros.xml. Change it using

```
ls /etc/libvirt/qemu/cirros.xml
virsh edit cirros
```

To find out process and command arguments to kvm/qemu

```
$ ps -ef|grep -E "kvm|qemu"
qemu     13354     1  8 05:26 ?        00:01:06 /usr/bin/qemu-system-x86_64 -name cirros -S -machine pc-i440fx-2.0,accel=tcg,usb=off -m 512 -realtime mlock=off -smp 1,sockets=1,cores=1,threads=1 -uuid ffd5da2b-61fc-49ad-8007-95e6f6ea9fc0 -no-user-config -nodefaults -chardev socket,id=charmonitor,path=/var/lib/libvirt/qemu/cirros.monitor,server,nowait -mon chardev=charmonitor,id=monitor,mode=control -rtc base=utc -no-shutdown -boot strict=on -device piix3-usb-uhci,id=usb,bus=pci.0,addr=0x1.0x2 -drive file=/root/cirros-0.3.2-x86_64-disk.img,if=none,id=drive-ide0-0-0,format=qcow2,cache=none -device ide-hd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=1 -netdev tap,fd=23,id=hostnet0 -device rtl8139,netdev=hostnet0,id=net0,mac=52:54:00:3c:f7:ba,bus=pci.0,addr=0x3 -chardev pty,id=charserial0 -device isa-serial,chardev=charserial0,id=serial0 -vnc 127.0.0.1:0 -device cirrus-vga,id=video0,bus=pci.0,addr=0x2 -device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x4
root     14341 27909  0 05:39 pts/0    00:00:00 grep --color=auto -E kvm|qemu
```

To find vnc port
```
$ virsh vncdisplay cirros
127.0.0.1:0
```

Repeating the above steps, I have create another VM 'cirros2', using ~/irros-0.3.2-x86_64-disk.img.1 as disk file
```
$ virsh list
 Id    Name                           State
----------------------------------------------------
 8     cirros                         running
 13    cirros2                        running
```

## Create VM, the XML way

Libvirt KVM VM is purely defined by the XML under /etc/libvirt/qemu/, including the disk file path. Format in [here](http://libvirt.org/formatdomain.html). To create a new VM using the XML file,

```
# get cirros-0.3.2-x86_64-disk.img.2
wget --no-check-certificate https://download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img
cp /etc/libvirt/qemu/cirros2.xml cirros3.xml
vim cirros3.xml
... # change name.cirros2, delete uuid, change device.disk.source[file], replace last 3 bytes of 'mac address', 
virsh define cirros3.xml
ll /etc/libvirt/qemu/cirros3.xml
virsh start cirros3
```

After this, cirros3 is successfully started.

```
$ virsh list
 Id    Name                           State
----------------------------------------------------
 8     cirros                         running
 13    cirros2                        running
 14    cirros3                        running
```

## Libvirt in Openstack

If you use boot VM from image (rather than boot from volume) in Openstack. When you boot a VM in nova, image file will be 'GET' from glance and put in local file system '/var/lib/nova/instances/_base' of the compute node. Refer to <https://lists.launchpad.net/openstack/msg08074.html>.

```
# on a openstack compute node
$ ll -h /var/lib/nova/instances/_base
total 16G
-rw-r--r-- 1 nova qemu  40G Nov  3 08:38 5dca4e25ea2410ac6c0615581e875f62a294b8db 
-rw-r--r-- 1 nova qemu  20G Nov  3 08:38 68f3e3d4d52bf185741ec5dc374ed664e3f93797
-rwxr-xr-x 1 nova qemu 2.2G Nov  3 08:38 7a2c028dc0908c780fb56ad35527cd50ac1ad661
...
```

The disk of an VM is stored on compute's local file system under '/var/lib/nova/instances/'. Each of the folder corresponds to a VM, with its openstack id as folder name.

```
# on the compute node
$ ll -h /var/lib/nova/instances/
032588cd-cbfa-4fe6-b627-f1e6d1fe6ddc  9042822a-d3f9-44cd-9694-4f45e5259257
1419c8c0-0d86-4b19-84b2-cdf9136d3aa6  _base
```

List one of the folder content.

```
# on the compute node
$ ll -h /var/lib/nova/instances/032588cd-cbfa-4fe6-b627-f1e6d1fe6ddc/
total 207M
-rw-rw---- 1 qemu qemu  21K Sep  9 04:04 console.log
-rw-r--r-- 1 qemu qemu 207M Nov  3 08:55 disk
-rw-r--r-- 1 nova nova 1.6K Sep  9 04:03 libvirt.xml
```

The libvirt definition xml file as below. The instance has id '032588cd-cbfa-4fe6-b627-f1e6d1fe6ddc' in openstack, and id 'instance-0002a893' in libvirt. Access the VM through 'https://<horizon-ip>/dashboard/admin/instances/03e588cd-cbfa-4fe6-b626-f1e6d2fe6ddc/detail' in browser.

```
# on the compute node
$ less /var/lib/nova/instances/032588cd-cbfa-4fe6-b627-f1e6d1fe6ddc/libvirt.xml
<domain type="kvm">
  <uuid>032588cd-cbfa-4fe6-b627-f1e6d1fe6ddc</uuid>
  <name>instance-0002a893</name>
  <memory>4194304</memory>
  <vcpu>2</vcpu>
  <sysinfo type="smbios">
    <system>
      <entry name="manufacturer">Red Hat Inc.</entry>
      <entry name="product">OpenStack Nova</entry>
      <entry name="version">2013.2.3-140612233026_ocp</entry>
      <entry name="serial">8de7977e-195d-47ba-8ed2-19f5ddb728fc</entry>
      <entry name="uuid">03e588cd-cbfa-4fe6-b626-f1e6d2fe6ddc</entry>
    </system>
  ...
```

There is also a VM definition file in libvirt's /etc/libvirt/qemu/. They look alike but with a little difference.

```
# on the compute node
$ less /etc/libvirt/qemu/instance-0002a893.xml
<domain type='kvm'>
  <name>instance-0002a893</name>
  <uuid>03e588cd-cbfa-4fe6-b626-f1e6d2fe6ddc</uuid>
  <memory unit='KiB'>4194304</memory>
  <currentMemory unit='KiB'>4194304</currentMemory>
  <vcpu placement='static'>2</vcpu>
  <sysinfo type='smbios'>
    <system>
      <entry name='manufacturer'>Red Hat Inc.</entry>
      <entry name='product'>OpenStack Nova</entry>
      <entry name='version'>2013.2.3-140612233026_ocp</entry>
      <entry name='serial'>8de7977e-195d-47ba-8ed2-19f5ddb728fc</entry>
      <entry name='uuid'>03e588cd-cbfa-4fe6-b626-f1e6d2fe6ddc</entry>
    </system>
  ...
$ diff /var/lib/nova/instances/032588cd-cbfa-4fe6-b627-f1e6d1fe6ddc/libvirt.xml /etc/libvirt/qemu/instance-0002a893.xml
```

## Play with Network

Usually a hypervisor gives you two network options to connect VMs to outside: the NAT mode and the Bridge mode.

### The NAT Mode

In NAT mode we connect VM to a bridge (yes, it also uses bridge), and use SNAT to translate VM IPs to host ports. A DHCP runs on the bridge, by which the VMs get IP addresses. I.e., VM gets private IP. The bridge consumes one private IP address itself.

On default, libvirt kvm is using the NAT mode. Now let's dive.

First, ifconfig on the host

```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.224.147.166  netmask 255.255.255.0  broadcast 10.224.147.255
        inet6 fe80::f816:3eff:fe98:559f  prefixlen 64  scopeid 0x20<link>
        ether fa:16:3e:98:55:9f  txqueuelen 1000  (Ethernet)
        RX packets 1925933  bytes 400908368 (382.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 967162  bytes 269767657 (257.2 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 0  (Local Loopback)
        RX packets 1666  bytes 129707 (126.6 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1666  bytes 129707 (126.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

virbr0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
        ether fe:54:00:17:1e:56  txqueuelen 0  (Ethernet)
        RX packets 944  bytes 88204 (86.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1008  bytes 110279 (107.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vnet0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc54:ff:fe3c:f7ba  prefixlen 64  scopeid 0x20<link>
        ether fe:54:00:3c:f7:ba  txqueuelen 500  (Ethernet)
        RX packets 548  bytes 63284 (61.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10604  bytes 596604 (582.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vnet1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc54:ff:fedb:4c6c  prefixlen 64  scopeid 0x20<link>
        ether fe:54:00:db:4c:6c  txqueuelen 500  (Ethernet)
        RX packets 137  bytes 13561 (13.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 8358  bytes 441239 (430.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

vnet2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::fc54:ff:fe17:1e56  prefixlen 64  scopeid 0x20<link>
        ether fe:54:00:17:1e:56  txqueuelen 500  (Ethernet)
        RX packets 133  bytes 12731 (12.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 6061  bytes 320596 (313.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

The 'virbr0' is the bridge. From vnet0 to vnet1 corresponds to our 3 cirros VM's nic. To see the bridge setup:

```
$ brctl show
bridge name     bridge id           STP enabled     interfaces
virbr0          8000.fe5400171e56       yes             vnet0
                                                        vnet1
                                                        vnet2
```

You can see vnet0-2 are attached on virbr0. Bridge virbr0 has IP 192.168.122.1. But how is the DHCP running on virbr0? It is done by dnsmasq (it is capable of both DNS and DHCP).

```
$ ps -ef|grep libvirt
...
nobody    4618     1  0 Nov02 ?        00:00:00 /sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf
...
```

Check out the configure file dnsmasq is using. So you know dnsmasq is listening on virbr0 and allocate IP address to VMs. The range is 192.168.122.2 - 192.168.122.254.

```
$ less /var/lib/libvirt/dnsmasq/default.conf
strict-order
pid-file=/var/run/libvirt/network/default.pid
except-interface=lo
bind-dynamic
interface=virbr0
dhcp-range=192.168.122.2,192.168.122.254
dhcp-no-override
dhcp-leasefile=/var/lib/libvirt/dnsmasq/default.leases
dhcp-lease-max=253
dhcp-hostsfile=/var/lib/libvirt/dnsmasq/default.hostsfile
addn-hosts=/var/lib/libvirt/dnsmasq/default.addnhosts
```

To [find out IP address of VM](https://rwmj.wordpress.com/2010/10/26/tip-find-the-ip-address-of-a-virtual-machine/), we first use arp to get IP and its map to MAC address. You can find a VM's MAC address in libvirt xml at /etc/libvirt/qemu/. So you know a VM's IP.

```
$ arp -an
? (10.224.147.167) at fa:16:3e:65:b5:95 [ether] on eth0
? (169.254.169.254) at fa:16:3e:96:a5:41 [ether] on eth0
? (10.224.147.154) at fa:16:3e:99:41:fa [ether] on eth0
? (192.168.122.102) at 52:54:00:db:4c:6c [ether] on virbr0
? (192.168.122.182) at 52:54:00:17:1e:56 [ether] on virbr0
? (10.224.147.152) at fa:16:3e:96:a5:41 [ether] on eth0
? (10.224.147.1) at 00:00:0c:07:ac:00 [ether] on eth0
? (10.224.147.203) at fa:16:3e:c8:17:5e [ether] on eth0
? (10.224.147.204) at fa:16:3e:10:16:a0 [ether] on eth0
? (10.224.147.168) at fa:16:3e:a8:4f:41 [ether] on eth0
? (192.168.122.56) at 52:54:00:3c:f7:ba [ether] on virbr0
? (10.224.147.2) at 40:f4:ec:1d:6e:48 [ether] on eth0
? (10.224.147.205) at fa:16:3e:2f:da:d3 [ether] on eth0
```

Now we can login guest VM. The ifconfig inside it looks perfectly normal.

```
$ ssh cirros@192.168.122.56
cirros@192.168.122.56's password: 
$ ifconfig
eth0      Link encap:Ethernet  HWaddr 52:54:00:3C:F7:BA  
          inet addr:192.168.122.56  Bcast:192.168.122.255  Mask:255.255.255.0
          inet6 addr: fe80::5054:ff:fe3c:f7ba/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:792 errors:0 dropped:0 overruns:0 frame:0
          TX packets:576 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:80117 (78.2 KiB)  TX bytes:66950 (65.3 KiB)
          Interrupt:10 Base address:0xc000 

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
$ ping 192.168.122.182
PING 192.168.122.182 (192.168.122.182): 56 data bytes
64 bytes from 192.168.122.182: seq=0 ttl=64 time=4.302 ms
64 bytes from 192.168.122.182: seq=1 ttl=64 time=1.383 ms
$ ping www.baidu.com
PING www.baidu.com (180.76.3.151): 56 data bytes
64 bytes from 180.76.3.151: seq=0 ttl=37 time=43.311 ms
64 bytes from 180.76.3.151: seq=1 ttl=37 time=42.429 ms
$ ping 169.254.169.254     # the magic address of cloud-init
PING 169.254.169.254 (169.254.169.254): 56 data bytes
64 bytes from 169.254.169.254: seq=0 ttl=63 time=5.598 ms
64 bytes from 169.254.169.254: seq=1 ttl=63 time=1.454 ms
```

The next question is, how does the packet from a VM, comes to the out side into www.baidu.com? Open the four default tables in iptables,

```
$ iptables -t raw -nL
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         

$ iptables -t mangle -nL
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
CHECKSUM   udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:68 CHECKSUM fill

$ iptables -t nat -nL
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination         

Chain INPUT (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination         
MASQUERADE  tcp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  udp  --  192.168.122.0/24    !192.168.122.0/24     masq ports: 1024-65535
MASQUERADE  all  --  192.168.122.0/24    !192.168.122.0/24    

$ iptables -t filter -nL
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:53
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:53
ACCEPT     udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:67
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:67

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            192.168.122.0/24     ctstate RELATED,ESTABLISHED
ACCEPT     all  --  192.168.122.0/24     0.0.0.0/0           
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           
REJECT     all  --  0.0.0.0/0            0.0.0.0/0            reject-with icmp-port-unreachable
REJECT     all  --  0.0.0.0/0            0.0.0.0/0            reject-with icmp-port-unreachable

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination  
```

You can see in the 'nat' table, all traffic from 192.168.122.* and not to 192.168.122.* (! means not) is applied action '[MASQUERADE](http://server.zdnet.com.cn/server/2008/0317/772069.shtml)', the SNAT transaltion. This is how traffic from inside VM can come outside.

### The Bridge Mode

In bridge mode use connect VM to a bridge, and direct connect the bridge to public network. VMs get IP addresses from public DHCP service, which DHCP the host is also using. I.e., VMs get public IP. The bridge consumes one public IP address. Usually you take the IP address from eth0 and give it to the bridge. (By connecting the bridge's IP, client can also login to the host.)

Follow this guide: <http://www-01.ibm.com/support/knowledgecenter/linuxonibm/liaai.kvminstall/liaaikvminstallbridge.htm>

## Access by VNC

On another laptop with graphic desktop, I'm using chicken VNC. The host on which I run guest VM is 10.224.147.166. First you need to modify VM's libvirt xml. The default config, `<graphics type='vnc' port='-1' autoport='yes'/>`, can only be connected vir host's loopback address. Refer to [here](http://blog.scottlowe.org/2013/09/10/adjusting-vnc-console-access-via-libvirt-xml/). 

```
$ virsh edit cirros
... # change <graphics type='vnc' port='-1' autoport='yes'/> to <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'/>
$ virsh shutdown cirros
... # wait some time until fully shutdown
$ virsh start cirros
```

Do the same for cirros2 and cirros3. Now list VNC ports

```
$ virsh vncdisplay cirros
:0

$ virsh vncdisplay cirros2
:1

$ virsh vncdisplay cirros3
:2
```

On default, for a VM with VNC port N, VNC server listens on port 5900+N. VNC uses TCP, no UDP. To test connectivity, use telnet. Be careful whether there is firewall blocking these ports.

```
$ telnet 10.224.147.166 5900
Trying 10.224.147.166...
Connected to 10.224.147.166.
Escape character is '^]'.
RFB 003.008

```

Now on my laptop, I use chicken VNC to connect with Host: 10.224.147.166, Display: 0. Things worked!

## About File Injection into VM

In Openstack you can inject a file to VM's file system prior to boot. This feature is not originally shipped with Libvirt, it is implemented by Nova. Here is a [code dive](http://www.cnblogs.com/popsuper1982/p/3835409.html). 

[Libguestfs](http://libguestfs.org/guestfs.3.html) is a library for accessing and modifying VM's disk image. You can mount VM's virtual filesystem onto host's VFS, where you access it as a common filesystem. This is where we can "inject a file".

There are several ways to bring user data into VM. Here I copied from [Liping's blog](http://blog.csdn.net/matt_mao/article/details/11600115):

1) File injection prior to VM boost

```
[root@compute1 ~]# nova boot --image 2401a752-fbda-482e-98f6-281656758b7f --file /home/test=./matt.test --flavor=1 test6  
[root@compute2 ~]# ssh cirros@100.100.100.10  
The authenticity of host '100.100.100.10 (100.100.100.10)' can't be established.  
RSA key fingerprint is xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.  
Are you sure you want to continue connecting (yes/no)? yes  
Warning: Permanently added '100.100.100.10' (RSA) to the list of known hosts.  
cirros@100.100.100.10's password:   
$ sudo su -  
# cd /home/  
# ls  
cirros ftp test
```

2) Inject metadata.

```
[root@compute1 ~]# nova boot --image 2401a752-fbda-482e-98f6-281656758b7f --meta matt1=test1 --meta matt2=test2 --flavor=1 test2  
[root@compute1 ~]# nova show test2  
+-------------------------------------+--------------------------------------------------------------+  
| Property | Value |  
+-------------------------------------+--------------------------------------------------------------+  
| status | ACTIVE |  
| updated | 2013-09-12T02:39:43Z |  
| OS-EXT-STS:task_state | None |  
| OS-EXT-SRV-ATTR:host | compute2.webex.com |  
| key_name | None |  
| image | cirros-0.3.0-x86_64_2 (2401a752-fbda-482e-98f6-281656758b7f) |  
| private-net network | 100.100.100.7 |  
| hostId | 9f9ff1519a8807f08ae0798af159cbaa8c96912da9beacfd8b6ca134 |  
| OS-EXT-STS:vm_state | active |  
| OS-EXT-SRV-ATTR:instance_name | instance-000001b9 |  
| OS-EXT-SRV-ATTR:hypervisor_hostname | compute2.webex.com |  
| flavor | m1.tiny (1) |  
| id | 6c6cf452-0763-486d-a94c-acdf30c69304 |  
| security_groups | [{u'name': u'default'}] |  
| user_id | 2a167be1e83c477e9dd57033c2eaaec9 |  
| name | test2 |  
| created | 2013-09-12T02:38:25Z |  
| tenant_id | 0b337e1ad59d43428b77c8bb2f84ce32 |  
| OS-DCF:diskConfig | MANUAL |  
| metadata | {u'matt2': u'test2', u'matt1': u'test1'} |  
| accessIPv4 | |  
| accessIPv6 | |  
| progress | 0 |  
| OS-EXT-STS:power_state | 1 |  
| OS-EXT-AZ:availability_zone | nova |  
| config_drive | |  
+-------------------------------------+--------------------------------------------------------------+  
[root@compute2 ~]# ssh cirros@100.100.100.7  
cirros@100.100.100.7's password:   
$ cd /  
$ cat meta.js   
{"matt2": "test2", "matt1": "test1"}
```

3) The user-data way. Note 169.254.169.254. This is used by [cloud-init](http://cloudinit.readthedocs.org/en/latest/topics/datasources.html).

```
[root@compute1 ~]# cat matt.test   
This is test for user-data  
[root@compute1 ~]# nova boot --image 2401a752-fbda-482e-98f6-281656758b7f --user-data ./matt.test --flavor=1 test4  
[root@compute1 ~]# ssh cirros@100.100.100.8  
The authenticity of host '100.100.100.8 (100.100.100.8)' can't be established.  
RSA key fingerprint is 31:7f:b6:5f:ea:b8:5a:b4:f5:97:35:27:7c:3c:8e:3a.  
Are you sure you want to continue connecting (yes/no)? yes  
Warning: Permanently added '100.100.100.8' (RSA) to the list of known hosts.  
cirros@100.100.100.8's password:   
$ sudo su -  
# telnet 169.254.169.254 80  
GET /latest/user-data
  
HTTP/1.1 200 OK  
Content-Type: text/html; charset=UTF-8  
Content-Length: 27  
Date: Thu, 12 Sep 2013 03:54:12 GMT  
Connection: close  
  
This is test for user-data  
Connection closed by foreign host 
```

Here is an [example](http://my.oschina.net/chape/blog/119980) using metadata and 169.254.169.254 to fetch public key and hostname for new VM.

## Libvirt Remote

You can access libvirt from another host. Refer to <http://libvirt.org/remote.html#Remote_certificates>. On default this needs certificate on server and client. By using ssh we can bypass this.

```
# on host 10.224.147.167
$ virsh --connect qemu:///10.224.147.166:/system
error: failed to connect to the hypervisor
error: internal error: unexpected QEMU URI path '/10.224.147.166:/system', try qemu:///system
$ virsh --connect qemu+ssh://10.224.147.166/system list
 Id    Name                           State
----------------------------------------------------
 15    cirros                         running
 16    cirros2                        running
 17    cirros3                        running

```

## Attach Volumes to VM

Libvirt/KVM supports all kinds of volume type: raw, iso, qcow2, vmdk, etc, See [here](http://libvirt.org/storage.html). The official site usually guides you to use [storage pools](http://libvirt.org/storage.html). But I found you can also [attach a disk directly](http://koumm.blog.51cto.com/703525/1292146).

### Attach A Disk Directly

To directly attach a new disk to VM, you have to modify the libvirt VM xml (refer to [here](http://koumm.blog.51cto.com/703525/1292146)). In this way, file based disk can be attached.

```
virsh edit cirros

# in <device>...</device>, following <disk>...</disk>, add
# this points to the new disk file. you have to replace target dev name as 'hdb' or others.
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' cache='none'/>
  <source file='/root/vm_direct_disk1.qcow2'/>
  <target dev='hdb' bus='ide'/>
</disk>

virsh shutdown cirros
... # wait untile fully shutdown
virsh start cirros
```

You can find the kvm parameters have added the new disk.

```
$ ps -ef|grep -E 'qemu|kvm'
qemu     26915     1 90 12:18 ?        00:06:40 /usr/bin/qemu-system-x86_64 -name cirros ... -drive file=/root/vm_direct_disk1.qcow2,if=none,id=drive-ide0-0-1,format=qcow2,cache=none -device ide-hd,bus=ide.0,unit=1,drive=drive-ide0-0-1,id=ide0-0-1 ...
```

Wait until the VM fully starts SSH. Login and check out the new disk

```
# login VM cirros
$ ssh cirros@192.168.122.56

# originally there is only /dev/sda
$ ls /dev/sd*
/dev/sda   /dev/sda1  /dev/sdb

$ sudo su -
$ mkfs.ext4 /dev/sdb
$ mkdir /mnt/disk1
$ mount /dev/sdb /mnt/disk1
$ echo "hello world this is vm_direct_disk1.qcow2" > /mnt/disk1/hello.txt
$ umount /mnt/disk1
```

Let's mount the disk to another VM, then checkout files on it. 

```
virsh edit cirros
... # remove the disk configuration segment we have added
virsh edit cirros2
... # add the same disk configuration segment
virsh shutdown cirros2
... # wait until fully shutdown, use 'virsh list' to see
virsh start cirros2
... # wait until SSH service starts

# login to VM cirros2
ssh cirros@192.168.122.102 
$ ls /dev/sd*
/dev/sda   /dev/sda1  /dev/sdb
$ sudo su -
$ mkdir /mnt/disk1
$ mount /dev/sdb /mnt/disk1
$ cat /mnt/disk1/hello.txt
hello world this is vm_direct_disk1.qcow2
$ umount /mnt/disk1
```

Files on the volume can be seen by VM cirros2.

### Attach Logical Volume as Disk

Not only files can be attached as disks, logical volumes can do it too. I followed the config [here](https://www.redhat.com/archives/libvirt-users/2010-April/msg00064.html). First, let's create logical volumes using LVM (disk is faked by dd)

```
# create the disk image
dd if=/dev/zero of=vm_disk.img bs=1 count=1 seek=1G

# mount as disk device
losetup /dev/loop3 vm_disk.img

# use lvm to create logic volumes
pvcreate /dev/loop3
vgcreate vm_vg /dev/loop3
lvcreate --name vm_lv1 --size 256M vm_vg
lvcreate --name vm_lv2 --size 256M vm_vg
lvcreate --name vm_lv3 --size 256M vm_vg
```

You need to edit the libvirt VM xml.

```
virsh edit cirros

# in <device>...</device>, following <disk>...</disk>, add
# target dev name can be changed. bus supports scsi, ide and virtio
<disk type='block' device='disk'>
  <source dev='/dev/vm_vg/vm_lv1' />
  <target dev='sdb' bus='scsi' />
</disk>
<disk type='block' device='disk'>
  <source dev='/dev/vm_vg/vm_lv2' />
  <target dev='sdc' bus='scsi' />
</disk>
<disk type='block' device='disk'>
  <source dev='/dev/vm_vg/vm_lv3' />
  <target dev='sdd' bus='scsi' />
</disk>

virsh shutdown cirros
... # wait untile fully shutdown
virsh start cirros
```

After rebooting the VM, let's see the new disks.

```
$ ssh cirros@192.168.122.56
$ ls
$ ls /dev/sd*
/dev/sda   /dev/sdb   /dev/sdc   /dev/sdd   /dev/sdd1
$ sudo su -
$ mkfs.ext4 /dev/sdb
$ mount /dev/sdb /mnt/disk1
$ echo hello world this is logical volume /dev/vm_vg/vm_lv1 > /mnt/disk1/hello.txt
$ umount /mnt/disk1

... # reboot the VM and find the hello.txt is still here
```

Check out the kvm process and its parameters.

```
$ ps -ef|grep -E 'kvm|qemu'
qemu      1921     1  7 13:57 ?        00:00:57 /usr/bin/qemu-system-x86_64 -name cirros ... -drive file=/dev/vm_vg/vm_lv1,if=none,id=drive-scsi0-0-1,format=raw -device scsi-hd,bus=scsi0.0,scsi-id=1,drive=drive-scsi0-0-1,id=scsi0-0-1 -drive file=/dev/vm_vg/vm_lv2,if=none,id=drive-scsi0-0-2,format=raw -device scsi-hd,bus=scsi0.0,scsi-id=2,drive=drive-scsi0-0-2,id=scsi0-0-2 -drive file=/dev/vm_vg/vm_lv3,if=none,id=drive-scsi0-0-3,format=raw -device scsi-hd,bus=scsi0.0,scsi-id=3,drive=drive-scsi0-0-3,id=scsi0-0-3 ...
```

### Use Storage Pool [FAILED]

Before approaching to this section, Let's unload all the attached disks in VM cirros and cirros2, by removing the added xml fragment

```
virsh edit cirros
... # remove the added config for new disks
virsh edit cirros2
... # remove the added config for new disks
... # restart cirros and cirros2
```

Libvirt supports many type of [storage pools](http://libvirt.org/storage.html#StorageBackendLogical): directory based, filesystem based, NFS based, iSCSI based, RBD based, etc. I will follow the official guide and use Filesystem pool.

```
mkdir -p /var/lib/virt/images
virsh edit cirros

# in <device>...</device>, following <disk>...</disk>, add
<pool type="fs">
  <name>virtimages</name>
  <source>
    <device path="/dev/vm_vg/vm_lv1"/>
  </source>
  <target>
    <path>/var/lib/virt/images</path>
  </target>
</pool>
```

__\[FAILURE\]__ After I wq the virsh edit, then open it again, I found my edits disappeared. The xml config is restored to the original. It seems I can't add <pool> tag in /etc/libvirt/qemu/cirros.xml.

### Use Storage Pool, the Right Way

After googling I figured out my understanding is WRONG. Storage pools are defined in /etc/libvirt/storage, not in VM's xml config. They are separated and not like "disks to attach". This is a [mail ask](https://www.redhat.com/archives/libvirt-users/2010-August/msg00042.html). This is a [tutorial](http://koumm.blog.51cto.com/703525/1304196).

```
mkdir -p /var/lib/virt/images
$ virsh pool-define-as virtimages --type fs --source-dev /dev/vm_vg/vm_lv1 --target /var/lib/virt/images # --print-xml to dry-run

# here is where pools are defined
$ cat /etc/libvirt/storage/virtimages.xml 
<pool type='fs'>
  <name>virtimages</name>
  <uuid>b8343798-f0fe-4ae5-bc40-6c94b0b15993</uuid>
  <capacity unit='bytes'>0</capacity>
  <allocation unit='bytes'>0</allocation>
  <available unit='bytes'>0</available>
  <source>
    <device path='/dev/vm_vg/vm_lv1'/>
    <format type='auto'/>
  </source>
  <target>
    <path>/var/lib/virt/images</path>
    <permissions>
      <mode>0755</mode>
      <owner>-1</owner>
      <group>-1</group>
    </permissions>
  </target>
</pool>

# now truely create and start the pool
$ virsh pool-build virtimages
$ virsh pool-autostart virtimages
$ virsh pool-list --all
$ virsh pool-info virtimages

# if not mkfs, pool-start reports mount error
$ mkfs.ext4 /dev/vm_vg/vm_lv1
$ virsh pool-start virtimages

# you can see, pool.source in xml is mounted to pool.target
$ df -h
Filesystem                Size  Used Avail Use% Mounted on
/dev/vda1                  40G  2.6G   38G   7% /
devtmpfs                  1.9G     0  1.9G   0% /dev
tmpfs                     1.9G     0  1.9G   0% /dev/shm
tmpfs                     1.9G   41M  1.9G   3% /run
tmpfs                     1.9G     0  1.9G   0% /sys/fs/cgroup
/dev/mapper/vm_vg-vm_lv1  240M  2.1M  222M   1% /var/lib/virt/images
```

Next, we can create volumes from the pool

```
$ virsh vol-create-as virtimages disk_in_pool.qcow2 128M --format qcow2
$ virsh vol-list virtimages
$ ll -h /var/lib/virt/images/
total 205K
-rw------- 1 root root 193K Nov  5 15:19 disk_in_pool.qcow2
drwx------ 2 root root  12K Nov  5 15:14 lost+found
```

You can find the corresponding disk file in /var/lib/virt/images now. I've seen tutorials telling me to use the disk file in virt-install, 

```
# refer to http://koumm.blog.51cto.com/703525/1304196, /data/oeltest03.qcow2 is the volume's disk file
virt-install --name=oeltest03 --os-variant=RHEL6 --ram 1024 --vcpus=1 --disk path=/data/oeltest03.qcow2,format=qcow2,size=20,bus=virtio --accelerate --cdrom /data/iso/oel63x64.iso --vnc --vncport=5910 --vnclisten=0.0.0.0 --network bridge=br0,model=virtio –noautoconsole
```

Or attach it to VM by modifying xml (what the above two sections do). But after searching out 'man virsh', I can't find a command to just attach volume to VM (although there is a set of command for pool, and a set for volume).

## Boot VM From Volume

In Openstack we often talk about [boot from image](http://docs.openstack.org/user-guide/content/launch_from_image.html) and [boot from volume](http://docs.openstack.org/user-guide/content/boot_from_volume.html). I want to do "boot from volume" in libvirt/kvm.

There is an excellent [summit talk](https://www.openstack.org/assets/presentation-media/OSSummitAtlanta2014-NovaLibvirtKVM2.pdf) about how Openstack nova work with kvm and libvirt. Below is a VM's libvirt xml, booted from IMAGE (not volume), found in a compute node:

```
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' cache='none'/>
  <source file='/var/lib/nova/instances/ef77b0bc-a5ef-4012-b21b-41f53d9abfc1/disk'/>
  <target dev='vda' bus='virtio'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
</disk>
```

No direct article telling "libvirt, boot from volume" or "kvm, boot from volume" found. From what I see I want to conclude that "boot from volue" is no difference from attaching disks in libvirt/kvm. Just use a bootable disk image and set it into the xml config of VM.

Other not so related materials: 

* Boot from iSCSI: [\[1\]](http://blog.hirudinean.org/blog/2013/11/05/booting-virtual-machines-using-iscsi-part-1/)[\[2\]](http://blog.hirudinean.org/blog/2013/11/05/booting-virtual-machines-using-iscsi-part-2/)
* Boot from Ceph: [here](http://davespano.wordpress.com/2012/09/09/boot-from-volume-with-openstack-and-ceph/)

### Boot from LVM Volume [FAILED]

Next I will try to create a logical volume, make it bootable and launch VM from it. BTW, actually the more practical is to first create an empty volume, then install a dummy VM (can use cdrom to install OS), by which way the volume becomes naturally bootable.

Following this [guide](http://www.howtoforge.com/xen-how-to-convert-an-image-based-guest-to-an-lvm-based-guest). First let's create the logical volume

```
# still, we use dd and loop device to create volume
dd if=/dev/zero of=boot_vg.img bs=1 count=1 seek=1G
losetup /dev/loop4 boot_vg.img
pvcreate /dev/loop4
vgcreate boot_vg /dev/loop4
lvcreate --name boot_lv1 --size 512M boot_vg
```

Use dd to copy the image to the logical volume. The dd can preserve all data including boot sector.

```
dd if=cirros-0.3.2-x86_64-disk.img of=/dev/boot_vg/boot_lv1
```

Create the VM cirros4 and boot.

```
cp /etc/libvirt/qemu/cirros3.xml cirros4.xml
vim cirros4.xml
... # change name, delete uuid, replace last 3 bytes of 'mac address'
# and, change the disk section as 
<disk type='block' device='disk'>
  <driver name='qemu' type='qcow2'/>  # note that the original cirros image is qcow2
  <source dev='/dev/boot_vg/boot_lv1' />
  <target dev='sda' bus='scsi' />
</disk>

virsh define cirros4.xml
ll /etc/libvirt/qemu/cirros4.xml
virsh start cirros4
```

OH, NO! Don't work. Don't know why. Use VNC and see that VM boots with error meesage "No bootable device".

### Boot from LVM Volume, Way 2

Now I follow this [guide](http://www.westernwillow.com/cms/blog/franco/migrate-vm-qcow2-disk-image-logical-volume), which converts cirros image to raw format beforehand.

```
qemu-img convert -f qcow2 -O raw cirros-0.3.2-x86_64-disk.img cirros-0.3.2-x86_64-disk.raw.img
dd if=cirros-0.3.2-x86_64-disk.raw.img of=/dev/boot_vg/boot_lv1

virsh edit cirros4
# change disk section to
<disk type='block' device='disk'>
  <driver name='qemu' type='raw'/>
  <source dev='/dev/boot_vg/boot_lv1' />
  # I found that if use <target dev='sda' bus='scsi' />, still error with "No bootable device"
  <target dev='hda' bus='ide' /> 
</disk>

virsh destroy cirros4   # virsh shutdown cannot stop a boot failed VM
virsh start cirros4
```

Succeeded! I can now see the VM boot up successfuly from VNC. But I found that if I use `<target dev='sda' bus='scsi' />` in disk section, still error boot up with "No bootable device". So I want to try way 1 again.

### Boot from LVM Volume, Back to Way 1

I want to try way 1 with `<target dev='hda' bus='ide' />` instead of `<target dev='sda' bus='scsi' />` again, will it fail?

```
dd if=cirros-0.3.2-x86_64-disk.img of=/dev/boot_vg/boot_lv1

vim cirros4.xml
# change the disk section to
<disk type='block' device='disk'>
  <driver name='qemu' type='qcow2'/>  # note that the original cirros image is qcow2
  <source dev='/dev/boot_vg/boot_lv1' />
  <target dev='hda' bus='ide' />    # use 'hda' this time
</disk>

virsh destroy cirros4
virsh start cirros4
```

Good, it worked! So in conclusion no need to convert qcow2 to raw. We can use qcow2 on LVM. Boot from volume is no difference with attaching a (bootable) disk to VM.

## Virtio

To enable virtio, follow libvirt [wiki](http://wiki.libvirt.org/page/Virtio). Virtio can be used in network and disk. There are 3 parts: virtio_net, virtio_blk, and virtio_balloon. 

To enable virtio it requires 

* KVM version support virtio (recent version is ok)
* Guest VM supports has installed virtio drivers. Any Linux OS with kernel >= 2.6.25 should be OK.
* Libvirt >= 0.4.4

I will try virtio in disk.

```
virsh edit cirros
# add a new disk like what prior section does. but choose bus='virtio'
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' cache='none'/>
  <source file='/root/vm_direct_disk1.qcow2'/>
  <target dev='vda' bus='virtio'/>
</disk>

virsh shutdown cirros
... # wail until fully shutdown
virsh start cirros
```

Next, let's check out the virtio on Guest VM.

```
$ ssh cirros@192.168.122.56
$ sudo su -

# check whether virtio started
$ lsmod | grep virtio
$ ls /sys/devices/virtio*
ls: /sys/devices/virtio*: No such file or directory

$ ls /dev/vd*
/dev/vda
$ mount /dev/vda /mnt/disk1
$ cat /mnt/disk1/hello.txt 
hello world this is vm_direct_disk1.qcow2  # the message left before
```

We can see virtio is not started. I think, cirros image doesn't support virtio. But after all I can access the attached disk `/dev/vda`.

## KVM Tuning

There are many aritcles published about KVM tunning: [\[1\]](http://www.slideshare.net/meituan/kvmopt-osforce-27669119)[\[2\]](https://www.redhat.com/summit/2011/presentations/summit/decoding_the_code/wednesday/wagner_w_420_kvm_performance_improvements_and_optimizations.pdf). This usually include setting a lot of config on kvm/libvirt. Below I will play with vcpupin and transparent huge page.

### VCPUPin

Following this [article](https://www.berrange.com/posts/2010/02/12/controlling-guest-cpu-numa-affinity-in-libvirt-with-qemu-kvm-xen/) for vcpu pin. Main things to consider are

* How to see NUMA node info
* Check the host capabilities
* Know which cpu is free
* How to pin vcpu
* List vcpu status

Here I play with vcpupin.

```
$ virsh vcpuinfo cirros
VCPU:           0
CPU:            1
State:          running
CPU time:       430.3s
CPU Affinity:   -y

# check which cpu the VM is running, 8611 is the pid of VM 
$ ps  -eLo pid,psr,comm | grep 8611
 8611   1 qemu-system-x86
 8611   1 qemu-system-x86
 8611   0 qemu-system-x86

# pin the cpu: vcpupin name <vcpu> <cpu>
$ virsh vcpupin cirros 0 0

$ virsh vcpuinfo cirros
VCPU:           0
CPU:            0
State:          running
CPU time:       430.3s
CPU Affinity:   y-

$ ps  -eLo pid,psr,comm | grep 8611
 8611   0 qemu-system-x86
 8611   0 qemu-system-x86
 8611   0 qemu-system-x86

$ check the runtime status
$ grep pid /var/run/libvirt/qemu/cirros.xml
<domstatus state='running' reason='booted' pid='8611'>
    <vcpu pid='8615'/>
```

In VM's libvirt xml you can find [this config](http://libvirt.org/formatdomain.html#elementsCPUAllocation) to pin cpu

```
<domain>
  ...
  <vcpu placement='static' cpuset="1-4,^3,6" current="1">2</vcpu>
  ...
</domain>
```

How to unpin vcpu? In libvirt you have to re-pin a vcpu to all cpus, refer to [here](https://bugzilla.redhat.com/show_bug.cgi?id=584684)

```
virsh vcpupin cirros 0 0-1  # 0-N, N is your max physical cpu id.
```

The `vcpupin` doesn't reflex in `ps -ef|grep cirros`. I.e. it is not set by kvm parameters. If using kvm only, you need to use command `taskset` to set cpu affinity, refer to [this book](http://item.jd.com/11325760.html) P60.

### Transparent Hugepage

First, the host needs to enable transparent hugepage. View the status by

```
# usually transparent hugepage is enabled by default
$ cat /sys/kernel/mm/transparent_hugepage/enabled
[always] madvise never    # in the 3 options, 'always' is selected
```

To check hugepage status

```
$ cat /proc/meminfo | grep -i AnonHugePages
AnonHugePages:    323584 kB
```

To enable or disable.

```
# to disable
echo never > /sys/kernel/mm/transparent_hugepage/enabled

# to enable
echo always > /sys/kernel/mm/transparent_hugepage/enabled 
```

Cool, transparent, so that's all. No need to config libvirt/kvm. Let's play with VM.

```
$ grep AnonHugePages /proc/meminfo 
AnonHugePages:    323584 kB
$ virsh destroy cirros

# the page used by VM is released
$ grep AnonHugePages /proc/meminfo 
AnonHugePages:     45056 kB
```

## Other References

* A Chinese KVM book: <http://item.jd.com/11325760.html>
* A good KVM guide: <http://koumm.blog.51cto.com/703525/1292146>
* Ceph rbd and libvirt: <http://ceph.com/docs/master/rbd/libvirt/>


