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
set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set hlsearch
set number
' >> /etc/vimrc
```

Generate ssh key pair

```
ssh-keygen
ssh-copy-id user@password
```

