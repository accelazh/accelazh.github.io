---
layout: post
title: "Build Linux Kernel and Live Debugging"
tagline : "Build Linux Kernel and Live Debugging"
description: "Build Linux Kernel and Live Debugging"
category: "kernel"
tags: [linux, debug, kernel]
---
{% include JB/setup %}

### Build the Kernel

Install pre-requisites

```
yum groupinstall -y "Development Tools" && yum install -y ncurses-devel hmaccalc zlib-devel binutils-devel elfutils-libelf-devel git bc
```

Clone linux kernel source (this may take a long time). About how to [build kernel](http://kernelnewbies.org/KernelBuild).

```
mkdir -p ~/workspace/kernel
cd ~/workspace/kernel
wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.10.82.tar.xz
mkdir linux-3.10.82 && tar xvf linux-3.10.82.tar.xz -C $(pwd)/linux-3.10.82/
cd linux-3.10.82
```

To build the kernel, you need a `.config` file first. I copied it from my host OS, then modified it. About how to [enable kernel debugging](http://www.makelinux.net/ldd3/chp-4-sect-1).

```
# copy .config from the host linux
cp /boot/config-`uname -r`* .config

# make sure at least below options are enabled
vim .config
	CONFIG_DEBUG_KERNEL=y
	CONFIG_FRAME_POINTER=y
	CONFIG_KGDB=y
	CONFIG_KGDB_SERIAL_CONSOLE=y
	CONFIG_DEBUG_INFO=y

# modify the identifying string for my custom kernel
vim .config
	CONFIG_LOCALVERSION="test01"
```

You can also edit your `.config` via a gui menu (ssh is supported). The complete `.config` will be attached in the end.

```
make menuconfig
```

Start compiling. You may be asked a lot of choice, just press enter to select defaults.

```
make -j$(nproc)
```

If you hit error and want to start over

```
make clean
```

### Build the Root Filesystem Manually

First, create the rootfs file using `ext2` type. This part refers to this [guide](http://www.tldp.org/HOWTO/Bootdisk-HOWTO/buildroot.html). For what is rootfs, refer to [here](http://kernelnewbies.org/RootFileSystem) and [here](https://www.kernel.org/doc/Documentation/filesystems/ramfs-rootfs-initramfs.txt).

```
cd ~/workspace/linux-stable
mkdir my-build ; cd my-build
dd if=/dev/zero of=rootfs bs=1k count=20480
mke2fs -m 0 -N 2000 rootfs    # press Y
mkdir /mnt/rootfs
mount -t ext2 rootfs /mnt/rootfs
```

I need to create the necessary files on rootfs. Copy them from [cirros docker image](https://github.com/ewindisch/docker-cirros). Docker image such as cirros, ubuntu, centos, are actually tar.gz of linux filesystem.

```
wget https://github.com/ewindisch/docker-cirros/raw/master/cirros-0.3.3-x86_64-lxc.tar.gz
tar xzvf cirros-0.3.3-x86_64-lxc.tar.gz -C /mnt/rootfs/
```

### Debug the Kernel [FAILED]

I will use gdb + qemu to debug the kernel. First install qemu

```
yum install -y epel-release
yum install -y kvm virt-manager libvirt libvirt-python python-virtinst virt-install qemu-kvm
```

Launch the kernel with rootfs. Here's a [guide](http://www.linux-magazine.com/Online/Features/Qemu-and-the-Kernel). Connect it with a VNC client (on port 5901) to validate.

```
cd ~/workspace/linux-stable
qemu-system-x86_64 -kernel ./arch/x86/boot/bzImage -hda my-build/rootfs -append "root=/dev/sda rw" -vnc 0.0.0.0:1
```

If you encountered "Gtk-WARNING **: cannot open display", checkout [\[1\]](http://blog.csdn.net/Lux_Veritas/article/details/19244349)[\[2\]](https://wiki.gentoo.org/wiki/QEMU/Options).

Launch the kernel in debug mode. The `-S` does not start CPU at startup. The `-s` establish a gdb server on tcp::1234.

```
qemu-system-x86_64 -kernel ./arch/x86/boot/bzImage -hda my-build/rootfs -append "root=/dev/sda rw" -vnc 0.0.0.0:1 -s -S
```

Connect the debug session with GDB. Need to go to kernel source code folder so that GDB sees source.

```
cd ~/workspace/linux-stable
gdb
(gdb) file vmlinux
(gdb) target remote :1234
(gdb) continue
^C    # To interrupt execution anywhere you want
(gdb) break vfs_mknod
(gdb) continue
(gdb) bt
```

The kernel crashed in boot process. Guess there's something wrong in my rootfs. But I don't know.

Next I'll try building from the all-in-one tool [Buildroot](http://buildroot.uclibc.org/).

### Build Kernel & RootFS by Buildroot

Following [Qemu and the Kernel](http://www.linux-magazine.com/Online/Features/Qemu-and-the-Kernel) and the [Buildroot User Menual](http://buildroot.uclibc.org/downloads/manual/manual.html#_buildroot_quick_start). First, download Buildroot.

```
mkdir -p ~/workspace/buildroot/
cd ~/workspace/buildroot
wget http://buildroot.uclibc.org/downloads/buildroot-2015.05.tar.gz
tar xzvf buildroot-2015.05.tar.gz
cd buildroot-2015.05
```

Next, config Buildroot. You need to
  * In "Build options", toggle "build packages with debugging symbols".
  * In "Toolchain", change "linux version" to "3.10"
  * In "Toolchain", change "Custom kernel version headers series" to "3.10.x"
  * In "Kernel", change "Kernel version" to "3.10"

```
# Generate Buildroot preset config
make qemu_x86_defconfig
# Config Buildroot
make menuconfig
```

Config linux kernel. This will trigger Buildroot to download linux kernel source, which may take a long time. You need to
  * In "Kernel hacking", toggle "Kernel debugging"
  * In "Kernel hacking", toggle "Compile the kernel with debug info"
  * In "Kernel hacking", toggle "Compile the kernel with frame pointers"

```
make linux-menuconfig    # download kernel source and config it
```

Finally build the kernel. You wil find
  * In `output/build/linux-3.10` is the downloaded kernel source code
  * The `output/images/bzImage` is the built and compressed kernel image
  * The `output/images/rootfs.ext2` is the built root filesystem (rootfs)
  * The `output/build/linux-3.10/vmlinux` is the raw kernel image

```
make
```

Launch the kernel based on Buildbox built rootfs. Access it via VNC.

```
# Launch the kernel
qemu-system-x86_64 -kernel output/images/bzImage -hda output/images/rootfs.ext2 -append "root=/dev/sda rw" -s -S -vnc 0.0.0.0:1
```

In another ssh session, launch gdb. You should run gdb in linux source directory so that gdb can see source.

```
cd ~/workspace/buildroot/buildroot-2015.05/output/build/linux-3.10/
gdb
(gdb) file output/build/linux-3.10/vmlinux
(gdb) target remote :1234
(gdb) break vfs_mknod
(gdb) bt
(gdb) continue
```

In VNC, you should see it successfully enters linux login. Username `root`, no password. After login you can type shell commands.

### Cross Debug My Own Build vs Buildroot Ones [FAILED]

Try launch my own built kernel with Buildroot built rootfs. Access it with VNC

```
cd ~/workspace/buildroot/buildroot-2015.05
qemu-system-x86_64 -kernel ~/workspace/kernel/linux-3.10.82/arch/x86/boot/bzImage -hda output/images/rootfs.ext2 -append "root=/dev/sda rw" -s -S -vnc 0.0.0.0:1
```

Launch gdb in another ssh session

```
cd ~/workspace/buildroot/buildroot-2015.05
gdb
(gdb) file ~/workspace/kernel/linux-3.10.82/vmlinux
(gdb) target remote :1234
(gdb) continue
```

In VNC I see: Failed to enter login screen. Boot failed with call trace. Try the second way, launch Buildroot kernel with my own rootfs image.

```
qemu-system-x86_64 -kernel ~/workspace/kernel/linux-3.10.82/arch/x86/boot/bzImage -hda output/images/rootfs.ext2 -append "root=/dev/sda rw" -vnc 0.0.0.0:1 -s -S
```

In VNC I see another error, still failed. Anyway, by now only buildroot's kernel + rootfs works. I want to change how I face the problem. How about directly debug a live centos7 running in VM directly?

### Run Centos7 in Qemu and Debug with GDB

Create my working directory and download centos7 iso image.

```
$ mkdir ~/workspace/qemu-kernel
$ cd ~/workspace/qemu-kernel/
$ ll -h CentOS-7-x86_64-Minimal-1503-01.iso
-rw-r--r-- 1 root root 636M Jul 30 18:38 CentOS-7-x86_64-Minimal-1503-01.iso
```

Create an empty disk image to install centos7

```
qemu-img create CentOS-7-x86_64-Minimal-1503-01.qcow 5G
```

Boot centos7 installation iso on my 5G disk. Note that the process is quite slow.

```
qemu-system-x86_64 -cdrom CentOS-7-x86_64-Minimal-1503-01.iso -hda CentOS-7-x86_64-Minimal-1503-01.qcow -boot d -net nic -net user -m 1024 -localtime -vnc 0.0.0.0:1
```

After the installation finished, and you need a reboot. Relaunch the VM without cdrom. You should be able to enter the system successfully

```
qemu-system-x86_64 -net nic -net user -m 1024 -localtime -vnc 0.0.0.0:1 CentOS-7-x86_64-Minimal-1503-01.qcow
```

Next, we need the `vmlinux` (containing debug symbols) matched with kernel. The standard way is to 

    1) Compile linux kernel inside the VM with debug enabled
    2) Install the new kernel in VM. I.e. next time the VM will boot from the new kernel. (Better take a snapshot before that)
    3) Copy the vmlinux and kernel source out to your host
    4) Relaunch qemu with `-s -S`. On your host, use gdb, vmlinux and the kernel source to debug

Another way is, Centos7 provides debuginfo rpm for kernel, which will put the `vmlinux` file into `/usr/lib/debug/lib/modules/$(uname -r)/`. Also, to get kernel source code, follow [here](http://wiki.centos.org/zh/HowTos/I_need_the_Kernel_Source)

```
# In my VM, to get kernel vmlinux
dhclient    # To get an ip to access outside
debuginfo-install kernel     # Install kernel debuginfo
ls /usr/lib/debug/lib/modules/$(uname -r)/
```

But, both way would be really slow in my condition. Since this centos7 here uses kernel 3.10, and you remember that I have also compiled a 3.10 kernel on my host already. I decided to take a shortcut and use that kernel's vmlinux and source directly.

```
# First, reboot my VM with debug session
qemu-system-x86_64 -net nic -net user -m 1024 -localtime -vnc 0.0.0.0:1 -s -S CentOS-7-x86_64-Minimal-1503-01.qcow

# In another console, launch gdb
cd ~/workspace/kernel/linux-3.10.82/
gdb
(gdb) file vmlinux
(gdb) target remote :1234
(gdb) break vfs_mknod
(gdb) continue
(gdb) bt
```

Failed. This doesn't work, guess kernel minior version 3.10.xx makes difference. GDB reports target is running but my VM is stuck. Anyway, I don't wanna try build a kernel on such a slow VM, let's try the next way.

References: [\[1\]](https://tthtlc.wordpress.com/2014/01/14/how-to-do-kernel-debugging-via-gdb-over-serial-port-via-qemu/)[\[2\]](https://fedoraproject.org/wiki/How_to_use_qemu)[\[3\]](http://wiki.osdev.org/How_Do_I_Use_A_Debugger_With_My_OS)[\[4\]](https://bugs.centos.org/view.php?id=7497)[\[5\]](http://archive.openflow.org/wk/index.php/Kernel_Module_Debugging)

### Run Centos7 in Virtualbox and KGBD Debug via Serial Port

I'm using a Windows host. First, start my Centos7 VM in Virtualbox. In Centos7, First install the kernel debuginfo

```
# In Centos7 VM
sudo yum install -y epel-release
sudo debuginfo-install kernel     # Install kernel debuginfo

# Here's the vmlinux
ls /usr/lib/debug/lib/modules/$(uname -r)/
```

Next, get the Centos7 kernel source, follow this [guide](http://wiki.centos.org/zh/HowTos/I_need_the_Kernel_Source)

```
# Run below as root is NOT recommended
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros
yum install -y rpm-build redhat-rpm-config asciidoc hmaccalc perl-ExtUtils-Embed pesign xmlto audit-libs-devel binutils-devel elfutils-devel elfutils-libelf-devel ncurses-devel newt-devel numactl-devel pciutils-devel python-devel zlib-devel
rpm -i http://vault.centos.org/7.1.1503/updates/Source/SPackages/kernel-3.10.0-229.1.2.el7.src.rpm 2>&1 | grep -v exist    # Change to your matching package
cd ~/rpmbuild/SPECS
rpmbuild -bp --target=$(uname -m) kernel.spec

# Here's the kernel source
ls ~/rpmbuild/BUILD/kernel*/linux*/
```

Add a virtual serial port for my Centos7 VM in Virtualbox. Refer to [\[1\]](http://opensourceforu.efytimes.com/2011/03/kgdb-with-virtualbox-debug-live-kernel/)[\[2\]](https://techtooltip.wordpress.com/2008/09/12/using-host-serial-port-from-guest-in-virtual-box/)[\[3\]](https://www.haiku-os.org/guides/virtualizing/virtualbox-windows-debugging). Thanks to this [guide](https://forums.virtualbox.org/viewtopic.php?f=7&t=26860).

```
# On Virtualbox, add serial port wth below options
Port number: COM1; Port mode: Host device; Port path: COM4

# On my Windows host, add COM device in Device Manager (Win7)
  * From the Action menu select Add legacy hardware.
    * Select Next, ‘Install the hardware that I manually select from a list’ and Next
    * Select ‘Ports (COM & LPT)’ and Next
    * Select ‘Communication Port’ from Standard port types.
    * Continue with Next and Finish.
  * In the Device Manager you should now see the COM4 port with a yellow warning icon.
    * Open Properties for the COM3 port.
    * Select Advanced from Port Settings.
    * Choose COM4 from the 'COM Port Number' (Ignore possible 'In Use')
    * In the Resources tab select *Set Configuration Manually*
    * Uncheck 'Use automatic settings'
    * Select the configuration that corresponds to the VirtualBox settings as noted – likely configuration 0000.
    * Close the box and you should be asked to reboot.
    * After reboot the COM4 port should now be working.
```

Failed. My Centos7 VM in Virtualbox cannot start, complaining "Failed to open host device 'COM4'" anyway. If the debug host were Linux (but mine is Windows), it would be a lot easier.

I happen to have another fedora VM in Virtualbox, on my Windows host. I will try another way, debug my live centos7 VM (debug target) from my fedora VM (debug host). Following guide [\[1\]](https://forums.virtualbox.org/viewtopic.php?f=6&t=56897)[\[2\]](http://opensourceforu.efytimes.com/2011/03/kgdb-with-virtualbox-debug-live-kernel/). First copy the `vmlinux` and kernel source to fedora VM

```
# On my fedora, the debug host, after copied vmlinux and source
ls ~/workspace/kernel/linux-3.10.0-229.1.2.e17.centos.x86_64
ls ~/workspace/kernel/linux-3.10.0-229.1.2.e17.centos.x86_64/vmlinux

```

Next, config serial port in host pipe type on both fedora and centos. So that they are connected. Centos7 would see `/dev/ttyS0`, Fedora would see `/dev/ttyS3`. For COM* mapping to /dev/ttyS*, see [here](https://techtooltip.wordpress.com/2008/09/12/using-host-serial-port-from-guest-in-virtual-box/).

```
# On each of my fedora VM and my centos7 VM, add a serial port
  * Port number: COM1
  * Port mode: Host pipe
  * Port path: \\.\pipe\com1
  * Create pipe: centos7 side yes; fedora side no
```

Next on fedora VM do below to prepare

```
# On my fedora VM
cd ~/workspace/kernel/linux-3.10.0-229.1.2.e17.centos.x86_64

# Write the gdb command file
echo '
set serial baud 115200
target remote /dev/ttyS0
' > gdbinit

# To access /dev/ttyS*, a user should be in dialout group
sudo usermod $(whoami) -a -G dialout
# logout then login
groups
```

On my centos7 VM, also add user to dialout

```
sudo usermod $(whoami) -a -G dialout
```

Next we test the serial port connecting on both side is working

```
# On centos VM, you should see 'hello' later
cat /dev/ttyS0

# On fedora VM
echo hello > /dev/ttyS0

# test vice visa
...
```

The first way is to trigger debug session inside the linux (when login and already running). More kdb commands see [here](https://www.kernel.org/pub/linux/kernel/people/jwessel/kdb/usingKDB.html)

```
# On centos 7, after system is boot, login as root
echo ttyS0 > /sys/module/kgdboc/parameters/kgdboc

# trigger debug, which suspends the system
echo g > /proc/sysrq-trigger

# On my fedora VM launch gdb
cd ~/workspace/kernel/linux-3.10.0-229.1.2.e17.centos.x86_64
gdb -x gdbinit vmlinux
(gdb) ...    # Play as you like
```

The second way is to trigger debug when system boot. To do it, reboot the centos7 VM, on grub screen, press `e` to edit kernel boot parameters

```
# Append to kernel boot parameters
kgdboc=ttyS0,115200 kgdbwait
```

After continue booting (ctrl-x), you should see the centos7 VM suspend and wait for remote gdb connect in. Then, use fedora VM to gdb connect in

```
gdb -x gdbinit vmlinux
```

But this debug on boot way didn't work for me. My gdb keep stucking and timeout. I guess this is because of kgdb io driver staff, see [here](https://www.kernel.org/pub/linux/kernel/people/jwessel/kdb/kgdbwait.html).

### Debug VM using Virtualbox or VMware Debug Support

Both Virtualbox and VMware provide native debugging support, just like qemu provides `-s -S` for gdb.

  * Virtualbox: [http://sysprogs.com/VBoxGDB/tutorial/](http://sysprogs.com/VBoxGDB/tutorial/)
  * VMware Workstation: [http://stackframe.blogspot.com/2007/04/debugging-linux-kernels-with.html](http://stackframe.blogspot.com/2007/04/debugging-linux-kernels-with.html)

But note VBoxGDB is very inmature, and with a lot of limitations. VMware's only works on Workstation. I just post them here, not tried.

### Summary

To debug a live linux (e.g. CentOS7), you can choose one of below ways

  1. Launch target VM in qemu `-s -S`, then gdb debug
  2. Launch target VM in Virtualbox or VMware, add a serial port, then kgdb debug
  3. Use Virutalbox VBoxGDB or VMware Workstation debug support.

I recommend do (1) and (2) on Linux. If you have to do it on Windows, launch another Linux as the debug host, then connect debug target (VM) and debug host (VM) with virtual serial port (host pipe). For (3) it is either inmature or charged with a fee. Windows as the debug host, gdb debug to a Linux VM, never succeeds. Overall I think (1) is the best way as long as you have a baremetal Linux host (qemu on VM is so slow).
