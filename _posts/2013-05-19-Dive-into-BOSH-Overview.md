---
layout: post
category : BOSH
title : "Dive into BOSH - Overview"
tagline: "深入理解BOSH - 概述"
tags : [BOSH]
---

{% include JB/setup %}

近期研究用BOSH部署cloud foundry，苦于BOSH的参考文献非常有限，为了实现知其然且知其所以然的目的，深入研究了BOSH的代码，希望能对更好的利用BOSH部署更多的系统，提供帮助。

## BOSH 介绍

BOSH是VMware公司公司为了持续部署和运维Cloud foundry而开发的一款基于cloud的持续部署工具集，有许多令人振奋的功能。由于PaaS大多是建立在IaaS的基础之上，通过抽象和封装，对外界用户暴露基本的运行环境和服务，同时对用户屏蔽复杂的环境配置和中间件管理、虚拟机运维等IaaS需要面对的问题，进一步使用户的专注于业务。因此cloud foundry通常建立在IaaS环境之上，然而为了实现与IaaS的解耦，cloud foundry 并不直接与IaaS平台交互，而是通过扩展运行的集群环境中的service和DEA组件，实现动态扩展和管理。然而由于cloud foundry的组件众多，当出现需要底层扩容、版本更新、开发/产品环境管理等问题时，部署和运维开发难度较大，因此BOSH工具应运而生，具有以下特性。

* __cloud aware__ 
 
 个人认为是相比于puppet和chef等工具最大的特性。对于在云平台上部署产品，BOSH支持同IaaS API进行交互，从而管理虚拟机状态，在需要时能够启动/删除虚拟机，而对于用户将不再需要从IaaS平台准备虚拟机的繁琐步骤。并且由于BOSH是和IaaS平台交互，因此当IaaS平台/VM出现不稳定的状况时，在部署时能够快速反应。

* __compile__

 对于需要编译才能运行的产品/包，BOSH通过和IaaS层交互实现对源代码的编译/管理。由于BOSH的虚拟机都是从同一个标准虚拟机镜像进行部署，支持编译可以保证代码和包可以正确地运行在目标环境中。

* __版本控制__
 
 对于大多数的管理工具，都可以方便地保存历史部署和当前部署之间的版本，以及所依赖的包的管理，可以通过git等版本控制工具进行管理

* __包管理__
 
 BOSH的packages可以支持存放在文件系统，S3，swift等多种方式

* __持续部署__
 
 能够比较部署版本之间的差别，进行持续增量部署

* __环境切换__
 
 在开发环境和生产环境直接的切换可以简单地通过`bosh target`进行切换

下图更好地描述了BOSH与先有的一些配置管理工具和任务编排工具的比较

![bosh features](/images/bosh_features.png)

## BOSH Codes Overview

BOSH的代码保存在[github上](https://github.com/cloudfoundry/bosh), 可以clone到本地进行学习。主要代码可以分成几个部分

* __CLI相关__ BOSH命令行相关的包，主要是在安装BOSH CLI本地进行操作，响应用户命令，并请求BOSH director在BOSH集群中按照命令进行操作。
	
	+ bosh\_cli : 所有`bosh`命令行操作的入口，支持扩展，扩展的方法见另一篇博客[Ruby 元编程在BOSH中的运用][1]

	+ bosh\_cli\_plugin\_aws : 扩展自bosh\_cli，所有`bosh aws`命令行操作的入口，用户和aws交互

	+ bosh\_cli\_plugin\_micro : 扩展自bosh\_cli，所有`bosh micro`命令行操作的入口，用于部署micro bosh


* __Agent相关__ 主要是安装在stemcell中的agent组件和BOSH中发送请求操作Agent的组件两部分，前者随stemcell嵌入在标准IMAGE中，后者由需要和agent交互的组件包含。

	+ agent\_client : 用于同agent进行交互的包，提供一系列agent操作的基本方法

	+ bosh\_agent : 响应对agent的各种操作的包，消息根据mbus设定可以来自nats或者HTTP API

* __BOSH core__ 是BOSH的核心组件，负责BOSH中部署工作，通过CPI组件和底层IaaS交互，通过registry以及agent_client控制部署流程和状态。
	
	+ director : BOSH的核心组件，控制所有部署操作，响应来自BOSH CLI的请求。

	+ bosh\_registry : BOSH保持和IaaS交互的入口，BOSH部署过程中利用多线程操作IaaS平台，执行结果和状态都是通过bosh\_registry进行控制，可以扩展

	+ bosh\_common : BOSH基本操作

	+ health\_monitor : BOSH部署过程中的监控组件，能够从nats消息中间件和director交互，监控BOSH状态

	+ monit\_api : 操作monit的API，用于监控VM的状态
 
	+ blobstore\_client : 同存储交互的模块

	+ simple\_blobstore\_server ： 一个简单的对象存储服务器，不推荐用于产品环境

* __BOSH cpi__ BOSH扩展底层IaaS的接口，目前支持Openstack, aws, vcloud和vSphere, 其中Openstack 和AWS是通过fog进行。
	
	+ bosh\_cpi : bosh IaaS 操作接口，抽象底层具体平台的基本操作，用于扩展
	
	+ bosh\_openstack\_cpi ： openstack操作接口

	+ bosh\_vcloud\_cpi ： vcloud操作接口

	+ bosh\_vsphere\_cpi ： vsphere操作接口

	+ bosh\_aws\_cpi ： aws操作接口

* __基本工具__ 提供在BOSH部署过程中的一系列基本工具
	
	+ bosh_encryption ： 加密相关

	+ ruby\_vcloud\_sdk ： vcloud sdk

	+ ruby\_vim\_sdk ：vsphere sdk

	+ stemcell\_builder ： 制作stemcell的帮助工具

* __其他__ 
 
	+ package\_compiler : 编译micro bosh用到的编译工具包

	+ aws ： aws相关的一些工具，制作AMI等脚本

	+ bat ： BOSH Acceptance Tests

	+ rake ： rake工具

	+ release ： bosh示例release

	+ spec ： 测试相关

	+ vendor ：工程中相关的lib

## BOSH 部署过程中的一些概念术语和部署步骤

详见本人另外一篇博客[《BOSH Terms and Working Steps》][2]

[1]: http://tiewei.github.io/bosh/Ruby-Magic-in-BOSH/ "ruby元编程在BOSH中的应用"
[2]: http://tiewei.github.io/bosh/BOSH-Terms-and-Working-Steps/ "BOSH中的概念和工作流程"