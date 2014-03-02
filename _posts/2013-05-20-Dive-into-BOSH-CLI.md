---
layout: post
category : BOSH
title : "Dive into BOSH - BOSH ClI"
tagline: "深入理解BOSH - BOSH CLI"
tags : [BOSH]
---

{% include JB/setup %}

BOSH CLI 是BOSH命令行的入口，所有对BOSH的操作都是通过BOSH CLI进行。本文中将介绍几个常用命令的执行过程。

## bosh micro deploy

`bosh micro deploy`用于部署micro bosh，该命令是扩展的bosh cli 命令，来自包`bosh_cli_plugin_micro`. 命令入口在`/bosh_cli_plugin_micro/lib/bosh/cli/commands/micro.rb`. `bosh micro deploy`的具体对应的方法为`Bosh::Cli::Command::Micro#perform`
代码片段如下，可查看[详细代码](https://github.com/cloudfoundry/bosh/blob/master/bosh_cli_plugin_micro/lib/bosh/cli/commands/micro.rb#L103)

    def perform(stemcell=nil)
      update = !!options[:update]

      manifest = load_yaml_file(deployment)
    		...
      if update
      	...
        method = :update_deployment
      else
        ...
        method = :create_deployment
      end

      confirm_deployment("#{confirmation} micro BOSH instance #{desc}")
      ...
      deployer.send(method, stemcell)
      ...
      update_target
      ...
    end

其中deployer方法返回的Bosh::Deployer::InstanceManager实例，根据IaaS类型有[openstack,aws,vcloud,vsphere]四种，详细代码在/lib/deployer/instance_manager/目录下。代码片段如下

    def deployer(manifest_filename=nil)
      ...
      if @deployer.nil?
        ...
        @deployer = Bosh::Deployer::InstanceManager.create(manifest)
      end

      @deployer
    end

以及Bosh::Deployer::InstanceManager.create方法

    class << self

      include Helpers

      def create(config)
        plugin = cloud_plugin(config)

        begin
          require "deployer/instance_manager/#{plugin}"
        rescue LoadError
          err "Could not find Provider Plugin: #{plugin}"
        end
        Bosh::Deployer::InstanceManager.const_get(plugin.capitalize).new(config)
      end

    end

`bosh micro deploy`基本过程就是加载deployment文件->新建Bosh::Deployer::InstanceManager::Openstack实例，然后执行其`update_deployment`或`create_deployment`方法。这里我们深入查看create方法。该方法核心在于Bosh::Deployer::InstanceManager#create方法，代码如下:

    def create(stemcell_tgz)
    	...
      state.stemcell_cid = create_stemcell(stemcell_tgz) //1
      state.stemcell_name = File.basename(stemcell_tgz, ".tgz")
      save_state

      step "Creating VM from #{state.stemcell_cid}" do
        state.vm_cid = create_vm(state.stemcell_cid)
        update_vm_metadata(state.vm_cid, {"Name" => state.name})
        discover_bosh_ip
      end
      save_state

      step "Waiting for the agent" do
        wait_until_agent_ready
      end

      step "Updating persistent disk" do
        update_persistent_disk
      end

      unless @apply_spec
        step "Fetching apply spec" do
          @apply_spec = Specification.new(agent.release_apply_spec)
        end
      end

      apply

      step "Waiting for the director" do
        wait_until_director_ready
      end
    end

由此可见，在create方法时，deployer的过程如下：

1. create\_stemcell : 验证并上传stemcell到openstack glance
2. create\_vm : 新建vm
3. update\_vm\_metadata : 通过openstack registry更新vm的metadata
4. discover\_bosh\_ip : 分配floating ip给vm
5. wait\_until\_agent\_ready : 等待vm的agent ready，通过agent_client发送请求
6. update\_persistent\_disk : 给vm添加volume
7. @apply\_spec = Specification.new(agent.release\_apply\_spec) : microbosh的stemcell与bosh不同，在/var/vcap/micro/apply_spec.yml目录下有基本的配置信息，此步骤取回该信息并调整其适合openstack的环境
8. apply : 上传spec给agent, 使agent根据spec执行操作。
9. wait\_until\_director\_ready : 等待vm的director进行成功响应


与此同时，在vm instance上的agent随着vm启动而启动，代码片段如下

    module Bosh::Agent

      BOSH_APP = BOSH_APP_USER = BOSH_APP_GROUP = "vcap"

      class << self
        def run(options = {})
          Runner.new(options).start
        end
      end

      class Runner < Struct.new(:config)

        def initialize(options)
          self.config = Bosh::Agent::Config.setup(options)
          @logger     = Bosh::Agent::Config.logger
        end

        def start
          $stdout.sync = true
          @logger.info("Starting agent #{Bosh::Agent::VERSION}...")

          if Config.configure
            @logger.info("Configuring agent...")
            Bosh::Agent::Bootstrap.new.configure

            Bosh::Agent::Monit.enable
            Bosh::Agent::Monit.start
            Bosh::Agent::Monit.start_services
          else
            @logger.info("Skipping configuration step (use '-c' argument to configure on start) ")
          end

          if Config.mbus.start_with?("https")
            @logger.info("Starting up https agent")
            require "bosh_agent/http_handler"
            Bosh::Agent::HTTPHandler.start
          else
            Bosh::Agent::Handler.start
          end
        end
      end

    end

其中Bosh::Agent::Bootstrap.new.configure代码如下

    def configure
          logger.info("Configuring instance")

          load_settings
          logger.info("Loaded settings: #{@settings.inspect}")

          if @settings
            update_iptables
            update_passwords
            update_agent_id
            update_credentials
            update_hostname
            update_mbus
            update_blobstore
            setup_networking
            update_time
            setup_data_disk
            setup_tmp

            Bosh::Agent::Monit.setup_monit_user
            Bosh::Agent::Monit.setup_alerts

            mount_persistent_disk
            harden_permissions
          end
          { "settings" => @settings }
        end

由此可见，当agent获取了configuration信息后，做了这么几个步骤

1. load\_settings : load setting from openstack\_registry
2. update_iptables 
3. update_passwords
4. update\_agent\_id 
5. update\_credentials
6. update\_hostname 
7. update\_mbus
8. update\_blobstore
9. setup\_networking
10. update\_time : ntp
11. setup\_data\_disk : mount Ephemeral disk
12. setup\_tmp
13. mount\_persistent\_disk : mount persistent disk (此时并没有设定persistent disk，在agent HTTP handler start之后会更新)
14. monit enable/start/startservice 
15. Bosh::Agent::HTTPHandler.start/Bosh::Agent::Handler.start

在deployer和agent交互的同时，一方面deployer利用agent\_client向agent发送命令，并等待执行结束，另一方面由openstack执行的操作，都是通过openstack\_cpi线程执行，并通知openstack registry，agent在执行时会从openstack registry获取配置信息，并执行deployer发来的指令。
