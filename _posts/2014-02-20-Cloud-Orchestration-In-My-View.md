---
layout: post
title: "Cloud Orchestration In My View "
tagline : "Cloud Orchestration 个人见解"
description: "Cloud Orchestration In My View"
category: "DevOps"
tags: [cloud, orchestration, BOSH, HEAT]
---
{% include JB/setup %}

随着 IaaS产品的日趋成熟和完善，围绕整个 IaaS平台的周边工具也日益丰富起来。作为 AWS的最有力的竞争者， Openstack日趋丰富的生态系统进一步拉近与AWS的距离。然而 IaaS平台归根结底是为了简化运维工作，方便运维和开发人员管理硬件资源，共同实现 APP的快速上线。这里包含了笔者认为 IaaS平台能够提供的最核心的价值 ——

**硬件资源池化** : 利用虚拟化的方法将异构的计算/网络/存储资源抽象成统一的上层模型，利用内在的调度方法管理内部的物理资源

**操作手段标准化** ：提供标准API能够对由 IaaS平台管理的物理资源进行操作，使通过软件定义计算/网络/存储成为可能，从而快速生成所需要的运行环境。

这两点作为 IaaS平台的核心价值，改变了软件开发人员的思维模式，同时也使得 Cloud Orchestration成为可能。本文的主要内容分成以下三个部分：

1. 介绍 Cloud Orchestration的概念和来源
2. 现有 Cloud Orchestration的工具
3. 个人的一些看法

## Cloud Orchestration的概念和来源

wikipedia给出的[定义](http://en.wikipedia.org/wiki/Orchestration_\(computing\)) :

>>Cloud service orchestration therefore is the:

>>* Composing of architecture, tools and processes by humans to deliver a defined service

>>* Stitching of software and hardware components together to deliver a defined Service

>>* Connecting and automating of work flows when applicable to deliver a defined service

Orchestration就是将服务中涉及的工具、流程、结构描述成一个可执行的流程，结合软硬件的接口，使之可以按照描述自动化、可重复地交付。具体到Cloud Orchestration，主要就是通过定义一系列的元数据来描述交付过程中涉及的环境管理(OS. network, storage ..)、软件包管理、配置管理以及监控和升级操作，以便自动化和标准化地完成从申请资源到交付/升级服务的整个生命周期。

## 为什么需要Cloud Orchestration？

简单来说就是降低管理大规模集群和服务所需的人力和时间消耗，保证服务环境的一致性和可靠性。具体来说主要是面对以下三个现象：

**将IaaS当作单纯的VM生成器** 
- 这个现象非常普遍，因为IaaS最基本的功能就是提供VM，然而其提供资源标准操作手段的价值被忽略了，API才是云服务的入口。

**多种角色贯穿整个环境管理过程**
- OS由安全人员指定，网络/存储归运维人员，数据库等管理归中间件人员配置。多种角色之间如果沟通不畅，很可能导致环境发生不可预知的错误。

**多种环境管理不一致**
- 开发/QA/产品环境由不同的团队采用不同的方法维护，多种环境管理不一致可能会导致服务运行环境不可预期，出现错误难以复现等问题。

针对以上三个现象，所以我们需要一个统一的手段去管理从VM生成到服务交付中的各个环节，控制服务的运行环境。

## 如何实现Cloud Orchestration

正是由于IaaS提供了标准的操作计算、网络、存储资源的手段，才使得我们可以利用其资源池中的资源来 build所需要的服务。
主要有两个部分的工作

1. 定义DSL 
定义一个DSL来描述服务发布整个过程中的各个数据和操作。目前常用标准的有 _"AWS Cloud Formation"_ 和 _"TOSCA"_ ，当然也可以自己定义DSL，只有具有足够能力描述整个过程即可

2. 实现执行引擎(Execution Engine)
为DSL实现的一个标准执行引擎，用于执行由DSL描述的脚本。

## 现有工具介绍

_Cloud Orchestration_ 工具在2012年开始出现，影响较大的包括 _"AWS Cloud Formation"_ ,  _"Ubuntu Juju"_ ,  _"Openstack HEAT"_ 
以及 _"Pivotal BOSH"_ 。相比puppet/chef等配置管理工具，这些工具同IaaS平台结合起来，涵盖了软件交付的整个生命周期。

下图介绍了这些主流工具的功能图谱，如有纰漏请指出。

![orchestration-tools-overview](/images/orchestration-tools-overview.jpg)


不同于单纯的配置管理工具(puppet/chef), previsioning工具(cobbler)，以及DA和其他运维工具，Orchestration工具更倾向于流程和过程的管理，
试图提供一个方便快捷的手段来控制整个过程。

下面介绍围绕这个问题，已有的一些工具

### BOSH

>>Cloud Foundry BOSH is an open source tool chain for release engineering, deployment and lifecycle management of large scale distributed services

BOSH 是为 Cloud Foundry 量身定制的发布管理工具，设计之初就是为了解决复杂的分布式系统难于管理和部署的问题。其主要有 package, job, release 和 deployment 四个概念，
其中 package 是 app 等需要部署的软件的包的集合， job 包含了部署该 app 的所需要的配置文件(erb)和启动停止命令的集合, release是一组 packge 和 job 的集合可以复用，
deployment 就是一次发布，通过在一个mainifest文件中定义所需要的 job 和使用的 release，并且附带平台的网络/存储设置，以及一些配置的具体参数(与 job 的 erb 对应)，
来完成一次完整发布的信息。在执行过程中，利用 IaaS 的API(主要是Fog库)来管理虚拟机、和网络/存储，具体的 app 安装和配置都是通过自定义的跑在vm上的bosh agent
监听 NATS 的消息队列中的命令来完成的。

优点

- 可以持续发布和部署，其 canary fly 的方式能够完成并行部署，更新时保证服务可用
- 分布式的结构决定了其可以方便的横向扩展
- 支持多平台
- job 通过 erb 来描述，非常方便理解
- 可以用git工具管理 package 和 job

缺点

- 利用 package + job 这种方式部署较为复杂的软件功能有限
- 进行调试的时候(重建release)需要将 packege 同步到本地，不能完全远程运行
- 需要定制的 cloud image，目前只支持 ubuntu
- 需要在 target vm 上运行 agent 且一直通信

### HEAT

>>HEAT implements an orchestration engine to launch multiple composite cloud applications based on templates in the form of text files that can be treated like code

HEAT是openstack的官方项目，其思想来自于 AWS 的 Cloud Formation，甚至 template 的 schema 都有兼容版本。对于Openstack而言， HEAT是其通向为客户创造价值而非只是温床(平台)
的入口， United Stack 的工程师甚至将其定位在 Devops2.0 工具。因为其能利用在 openstack 上的存储、计算、网络等所有资源，根据客户的需要定义一个完全的运行环境，形成了从VM到APP的闭环。

优点

- Openstack 官方推荐，社区活跃度非常高，能够第一时间使用 openstack 的最新功能，且与 openstack 其他项目协调十分方便
- 有与 cloud formation 一直的template schema, 如果从 AWS 迁移变的非常方便
- 可以和 puppet/chef 集成，在配置管理方面只做一个 invoker
- 没有任何一个工具能把自定义网络做的这么方便的

缺点

- 几乎和 Openstack 完全绑定在一起了，和 M$ 的绑定差不多
- 不涉足 app 级别的管理，既是优点也是缺点

### 其他

* vagrant + packer

这是一个天才作者的两个项目。vagrant侧重开发环境而非生产环境的搭建， packer则是 app image 的 mainifest， 能够在 AWS, DigitalOcean, Openstack等平台上建立安装好应用的image。
vagrant 用 ruby 编写实现了一套完整DSL， packer 用 go 编写，手段其实没有什么新颖的地方，但 plugable 的结构使其能够在很多场景适用。

* ansible

作者是cobbler的开发者之一，ansible 能够做的是Application Deployment，Configuration Management，Cloud & Amazon (AWS, EC2) Automation，Continuous Delivery (with Jenkins, etc.)。
这个项目最初是为了成为第三个 puppet 而存在的。可以看出他有很多配置管理的代码和DSL。 这个项目是python实现的，而且完全不通过agent来访问VM，侵入性非常小，交付起来更灵活。个人认为目前是
这个市场最具竞争力的一家了。

## 个人理解 

在IaaS大张旗鼓的推进下，越来越多的企业考虑将自己的业务运行的 cloud 上，然而如何迁移到 cloud 上是十分困难的问题。
Cloud 不提供API就是耍流氓，Orchestration 工具就是利用 cloud 的API的特点能够将从资源申请到应用运行管理的一系列工作，
通过一份配置文件，将业务和cloud关联起来。

另外一个思路是利用现有的PaaS平台来屏蔽 cloud 的细节，专注为用户提供服务，用户只需提供 app 的编译包。
然而笔者之前的 blog 对 PaaS 的缺点也描述了许多，对能部署在其上的应用要求很高:

* 运行环境要简单 - buildpack虽然用于解决类似问题，但仍然不是很理想
* 要尽可能的使用service - 常用的mysql, apache倒能理解，但是类似log之类的如果也要用service就让用户接入PaaS平台, 让用户难以维护
* 要尽可能的使用"平台" - 单机环境构建出目标PaaS上运行的实际环境比较困难，开发测试工作都离不开"平台"
* 缺少可定制性 - 可选的中间件有限，难于调优和debug。

而且 PaaS 对网络功能的订制几乎没有，大多使用 container 技术对关键业务的SLA也隔离有限，所以更多地适合一些互联网的快速试错类应用。

所以，从企业的需要出发，更需要的是一个强大的 orchestration 工具来解决问题，国内外已有许多家 startup 瞄准此处市场。