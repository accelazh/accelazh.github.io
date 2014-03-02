---
layout: post
title: "LOG : Cisco UCS Baremetal Dirver"
tagline : "日志：UCS裸机安装"
description: "LOG : Cisco UCS Baremetal Dirver"
category: "DevOps"
tags: ["DevOps"]
---
{% include JB/setup %}

前段时间给一个系统做裸机安装服务的功能，在此记录一二。

## 背景


1. 功能要求能够在以往用Cobbler部署并没有IPMI的 [UCS](http://en.wikipedia.org/wiki/Cisco_Unified_Computing_System) lab里实现服务的自动部署，涉及 [Cobbler](http://en.wikipedia.org/wiki/Cobbler_(software)), CIMC (Cisco Integrated Management Controller, 类似UCS 控制台)

2. Cobbler是客户环境，用户只提供一个用户名密码，以及需要安装的 distro

3. 批量安装，系统和服务的repo不在Cobbler的维护下，repo 的性能暂时不考虑

4. 需要支持并行安装

5. 本人以往经验基本都在OS以上做文章，第一次做装机这种『硬件』活动，文中可能透露种种愚昧，望谅解

## 一句话工具介绍

### CIMC

简单介绍一下CIMC， 这是C家为自己的UCS设备量身订做的一个管理平台，提供一个 web GUI 和 xml api来操作(和 cobbler一样， xml api的功能比较有限)。 另外CIMC是没有
资源池的概念的，一台CIMC对应一台物理设备，批量安装就需要一组CIMC信息

### Cobbler

Cobbler是一个 provisioning server， 通过提供 DNS, TFTP, DHCP服务， 利用 Python 模板库 [Cheetah](http://cheetahtemplate.org/learn.html) 编写可
复用 kickstart 文件， 实现基于 PXE 的批量机器安装功能 (现也支持虚拟机安装)。其API提供python api和 xml api，由于前者是GPL协议的，因此我们只考虑后者。

**Cobbler的优势** : 确实在PXE的基础上向前走了一大步，能够无人值守地批量安装机器

**Cobbler的缺点** : API的功能比较有限 - snippet 和 distro 文件大多只能识别本机上的路径，不能以 API 的方式传入。 利用PXE 安装的效率对于少量机器效率尚可，但对于大量机器，带宽和repo server的性能将影响装机时间。 并不能对装机过程中的进度状况进行监控。

概念：

distro: 发行版， 主要包含一个 initrd.img 和一个 kernel

profile: 相当于一类server的image，具有相同特性的一组server的属性，主要包含kickstart文件，可以包含 cheetah 语法的模板写法

system: 具体的一台机器，如果告诉了mac地址，目标机器在同一网络中的话可以全自动进行 kickstart 安装

snippet: 代码片段，用于复用的代码

## 问题

1. Cobbler xmlrpc 的API功能非常有限，不能假设对方 cobbler 环境已有哪些 snippet

2. CIMC xml api 不同版本的有差别， 1.3不支持 xml api， 1.4 和 1.5 的 API 有差别(如 1.4 不能获取MAC地址)

3. 除不同的 server 安装不同包之外，还需要支持为不同的 server 注入不同的用户信息

## 解决思路

因为所有需要的信息都有可以获取的源头 - 包列表和用户信息由用户提供，CIMC 能获取server 的 BIOS 和 网卡数据，并且能操作电源。 

1. CIMC 关闭目标机器

2. 对同一类型的服务，由于pakcage列表相同，因此创建共有的 profile。 在 `%post` 中包含变量 `$metadata`

3. CIMC 获取 server 的 mac 地址

4. 根据 mac 地址创建 system， 并在 system 的 `ks_meta` 信息中包含具体的数据

5. CIMC 调整 BIOS 启动顺序， 转为网络启动

6. CIMC 开机

7. 装机过程中 CIMC 启动项改为硬盘启动

8. 目标 server 自动完成装机过程后重启， 可通过 %post脚本或启动项或最简单的ping测试查看是否安装完成。

## 代码

由于代码量较大， 且流程较为清晰，这里只放出 driver 的源码地址

**CIMC Driver** <https://github.com/TieWei/baremetal_driver_for_ucs/blob/master/cimc_driver.py>

**Cobbler Driver** <https://github.com/TieWei/baremetal_driver_for_ucs/blob/master/cobbler_driver.py>

虽然说 Cobbler 早已不是什么新鲜的玩意，网上的教程也非常多，但是由于 UCS 并不是所有人都会接触到的 (接触到的人或许是甲方工程师)， 所以应该还是有参考价值的

## 思考

通过学习和实践 Cobbler， 对系统管理员物理机安装的手段第一次有了较为详细的认识 (包括kickstart文件的详情)。 

CIMC 1.5 之后才有比较像样的API，硬件公司终于开始放开硬件的管理API让 automation everything 能够从硬件开始了。

了解 openstack ironic 的玩家应该知道 ironic 的装机过程完全不是通过 PXE， 而是利用 server 暴露出的 ISCSI 直接将image写进去的，无论是效率还是速度都快很多。
介绍可参加 ironic 的 wiki， 国内这个[blog post](http://blog.jimflying.com/?p=103)写的也非常好。有时间我也会深入看看 ironic

起初用python写这一部分的代码是因为希望能为 openstack ironic 写 CIMC 的driver。实际上存在模板文件应该很自然的想到用 ruby 的 erb 功能快速实现，
而且代码会比较漂亮 (我会说我是 ruby 脑残粉吗？)

## END

写于2013-12-9 00:58

