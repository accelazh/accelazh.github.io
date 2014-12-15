---
layout: post
title: "CentOS 7 Preparation"
tagline : "CentOS 7 Preparation"
description: "CentOS 7 Preparation"
category: "automation"
tags: [os, centos]
---
{% include JB/setup %}

After started a CentOS 7 VM instance, some common housekeeping are needed to prepare it

To disable SELinux

```
# disable selinux
vi /etc/sysconfig/selinux
 SELINUX=disabled
reboot
# to check selinux status
getenforce
```

To enable SSH password login

```
# enable password login
vi /etc/ssh/sshd_config
  PasswordAuthentication yes
service sshd restart
```

Install common tools

```
yum install -y vim yum-utils git curl wget
```

Config vim

```
echo '
set background=dark
"set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set hlsearch
set number
' >> /etc/vimrc
```

Install pip

```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

Install EPEL repo

```
cd /tmp
wget https://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-2.noarch.rpm
yum install -y epel-release-7-2.noarch.rpm
```

Generate ssh key pair, then each host contains each one's ssh public key.

```
ssh-keygen
ssh-copy-id user@password
```

## Optional

Some hardened image use umask 077 rather than 022. This mess up many software installation. Change it back to 022

```
for i in /root/.bashrc /root/.bash_profile /root/.cshrc /root/.tcshrc /etc/bashrc /etc/profile /etc/csh.cshrc; do
    sed -i 's/^\([ \t]*\)umask\([ \t]\+\)077\([ \t]*\)$/\1umask\2022\3/' $i;
done
```

Sometime SFTP is disabled (on defualt it shoud already be enabled). Sublime SFTP will be blocked. Enable it here

```
echo "Subsystem sftp /usr/libexec/openssh/sftp-server" >> /etc/ssh/sshd_config
/etc/init.d/sshd reload
```

