---
layout: post
title: "Workflow of Push App in Cloud Foundry v1"
tagline : "Cloud Foundry V1版本中部署应用的工作流程"
description: "Workflow of Push App in Cloud Foundry v1"
category: cloudfoundry
tags: [Cloudfoundry, cloud_controller, stager, dea]
---
{% include JB/setup %}

本文介绍在Cloud Foundry v1版本中，Cloud Controller、Stager、DEA 是如何协同工作，实现app正常运行的。在Cloud Foundry V2版本中引入了dea\_next和cc\_next，并且Stager操作将在dea中进行，在处理流程中存在一些不同，将专门写blog介绍。

Cloud Foundry作为开源PaaS平台，对外提供的核心功能主要有两种 —— 为用户代码提供运行环境(runtime/framework)和为用户代码提供常用服务(数据库/消息队列等)。前者加上用户代码在Cloud Foundry的术语中称作一个Droplet，后者称为Service。本文介绍前者的主要工作流程，后者将写专文介绍。

>> 提醒 - 本文篇幅较长，代码较多，第三节细节较多

---

## Cloud Foundry APP 相关组件

当用户push一个app给Cloud Foundry，到最终app能够正常运行，主要由以下7个组件协同工作：

1. **vmc** :
v1版客户端，这里主要的操作就是利用`vmc push`将用户程序代码上传给Cloud Foundry，以及利用`vmc apps`获取app运行状态。代码见<https://github.com/cloudfoundry/vmc>， 本文所采用版本为0.5.1

2. **nats** :
核心组件，Cloud Foundry内部的消息队列服务，cloud\_controller, stager, dea, health\_manager\_next之间的消息请求都是在消息队列中发送的。在Cloud Foundry中是一个存在单点失败(single points of failure - SPOF)的节点，如何避免SPOF的问题已经有一些讨论，见<https://github.com/cloudfoundry/cf-release/issues/32>

3. **cloud\_controller** (下简称cc):
核心组件，Cloud Foundry响应用户请求的节点，可以很好的横向扩展，是一个ROR项目。在部署应用的过程中主要是响应用户请求，管理用户代码，请求stager和dea进行app的部署，并订阅health\_manager\_next的消息，响应用户查看app状态的请求。该节点在Cloud Foundry中可以很方便地横向扩展，代码见<https://github.com/cloudfoundry/cloud_controller>.

4. **stager** :
核心组件，Cloud Foundry中将用户代码和runtime/framework结合起来生成droplet的关键节点。目前提供java, ruby, python等rumtime，以及node.js,play, rake, rails, sinatra, java\_web等很多framework(java\_web就是提供了tomcat容器)。可扩展，代码见<https://github.com/cloudfoundry/stager>

5. **dea** :
核心组件，Cloud Foundry中运行droplet的节点，droplet包含用户app以及所需runtime和framework，以及所需的依赖包和start/stop脚本，dea只是提供运行用户代码的容器，提供最基本的隔离功能(v2版本的dea_next利用warden实现的LXC子集能够实现更好的隔离)。可扩展，代码见<https://github.com/cloudfoundry/dea>

6. **debian\_nfs\_server** :
可选组件，cloud\_controller保管用户代码的后台NFS存储服务，如果没有部署，则在cloud\_controller本地文件系统存储

7. **health\_manager\_next** :
可选组件，监控Cloud Foundry中app和各个组件的运行状态。这里主要是利用health\_manager\_next监控用户app的状态，如果没有部署，在用`vmc apps`查看app状态时，status信息会为n/a，不可扩展，代码见<https://github.com/cloudfoundry/health_manager>

8. **router**:
必须组件，当APP部署完成后，dea向router注册app的url，未来向该app发送的访问请求(url=xxx.cf.com)都会被转发至对应的dea处理，而操作请求(url=api.cf.com/apps/xxx)仍然转发至cc处理

---

## PUSH APP时组件操作概述

![Cloud Foundry v1 Push App](/images/CF-v1-push-app.png "cloud-foundry-v1-push-app")

_图中router和nats之间的交互未标出_

1. **vmc -> cloud_controller** : vmc根据用户代码新建app -> 更新url/memery等信息(state=STOPPED) -> 上传用户app代码，此处通过REST API交互

2. **cloud_controller** : cc响应vmc请求，创建app，存储app代码

3. **cloud_controller -> stager** : cc将app相关消息发送至NAT，由stager接收。此操作是利用stager-client进行的，代码见<https://github.com/cloudfoundry/stager-client>

4. **stager  -> cloud_controller** : 接收到消息的stager根据消息中的download\_uri从cc下载app的代码包，并利用vcap-staging制作droplet，完成后将droplet上传至cc。vcap-staging完成了整个部署APP过程中其中最为关键的操作，包括下载/安装/上传依赖包，打包运行环境，编辑start/stop脚本等，代码见<https://github.com/cloudfoundry/vcap-staging>

5. **vmc -> cloud_controller** : vmc向cc发送启动命令(state=STARTED)，在等待启动过程中(step 6-7)，通过REST API `GET /apps/test/instances`获取启动状态

6. **cloud_controller -> dea** : cc在NAT上发布消息寻找合适的dea，dea接收消息后下载droplet，并根据设定的resources限额启动droplet，并在NAT上发布运行状态

7. **dea -> router** : dea根据app的url向router注册，注册信息通过NATS传递

---

## 代码分析

上一节简要介绍了工作流程，本节从代码内部，详细分析工作流程中的关键步骤。


### Step1: upload app code in cc 

由于create/update app的过程十分相似，因此，我们首先介绍上传app的过程。

vmc 将用户app的代码打包成zip，调用REST API上传zip包.这里上传的zip包中只包括更新部分的文件，如果文件的fingerprints在cc中已经存在，则在zip包中不会包含这些文件，并在HTTP HEAD中resources中标注这些已经在cc中的资源。

resources的元素是一个HASH `{ :size => size, :sha1 => Digest::SHA1.file(filename).hexdigest, :fn => ./path/filename}`

请求信息实例如下

	POST http://api.cf.com/apps/:app/application
	{:_method=>"put", :resources=>"[]", :application=>#<UploadIO:0x0000000180d788 @content_type="application/zip", @original_filename="test.zip", @local_path="/tmp/test.zip", @io=#<File:/tmp/test.zip>, @opts={}>}

其中test为app的name

根据cc的`routes.rb`([github](https://github.com/cloudfoundry/cloud_controller/blob/master/cloud_controller/config/routes.rb#L20))，处理代码如下：

`AppsController#upload`-[github](https://github.com/cloudfoundry/cloud_controller/blob/master/cloud_controller/app/controllers/apps_controller.rb#L79)


    def upload
       ...
          file = get_uploaded_file
          resources = json_param(:resources)
          package = AppPackage.new(@app, file, resources)
          @app.latest_bits_from(package)
       ...
    end


这里将上传对应的app与上传的文件关联新建一个AppPackage对象。

`latest_bits_from(app_package)`-[github](https://github.com/cloudfoundry/cloud_controller/blob/master/cloud_controller/models/app.rb#L326)
	

    def latest_bits_from(app_package)
      sha1 = app_package.to_zip 
      unless self.package_hash == sha1
        ...
        unless self.package_hash.nil?
          FileUtils.rm_f(self.legacy_unstaged_package_path)
        end
        self.package_state = 'PENDING'
        self.package_hash = sha1
        save!
      end
    end


将对上传的文件利用`to_zip`方法进行处理，得出sha的值，并根据该值与数据库中app关联的package进行比较，如果不同，则更新sha值并将package_state设为PENDING状态

`AppPackage#to_zip`-[github](https://github.com/cloudfoundry/cloud_controller/blob/master/cloud_controller/models/app_package.rb#L7)

    def to_zip
      tmpdir = Dir.mktmpdir
      dir = path = nil
      check_package_size
      timed_section(CloudController.logger, 'app_to_zip') do
        dir = unpack_upload
        synchronize_pool_with(dir)
        path = AppPackage.repack_app_in(dir, tmpdir, :zip)
        sha1 = save_package(path) if path
      end
    ensure
      FileUtils.rm_rf(tmpdir)
      FileUtils.rm_rf(dir) if dir
      FileUtils.rm_rf(File.dirname(path)) if path
    end

此处在`check_package_size`检查package的大小是否超过限制(config中的`max_droplet_size`，默认512M)，`unpack_upload`将zip包解压到tmp文件夹，`synchronize_pool_with`将其同步到resource pool(这是resource pool是基于文件系统的实现即`FilesystemPool`，跟根目录是`AppConfig[:directories][:resources]`，可扩展至其他存储，只需继承`ResourcePool`)

    def synchronize_pool_with(working_dir)
      timed_section(CloudController.logger, 'process_app_resources') do
        AppPackage.blocking_defer do
          pool = CloudController.resource_pool
          pool.add_directory(working_dir)
          @resource_descriptors.each do |descriptor|
            create_dir_skeleton(working_dir, descriptor[:fn])
            path = resolve_path(working_dir, descriptor[:fn])
            pool.copy(descriptor, path)
          end
        end
      end
      ...
    end


由代码可见其将解压后的zip包文件夹`working_dir`同resource pool进行了同步。有两个操作，`add_directory`将`workdir`中的文件(非文件夹)路径计算出sha1值(`Digest::SHA1.file(path).hexdigest`与vmc计算方法一致)，然后根据sha1值进行计算(`FilesystemPool#path_from_sha1`)出一个形如`/resources_pool_root/MOD#1/MOD#2/SHA1`的文件路径`resource_path`，然后复制该文件到`resource_path`。另外一个操作就是恢复没有上传的已经存在`resources_pool`中的文件：`create_dir_skeleton`创建其所在文件夹`resolve_path`获得该文件应该在package中的文件路径，然后复制到package中，将解压后的文件夹package恢复成拥有全部应有文件的状态.之后重新打包成zip文件，将此zip文件计算出sha1值，保存为`package_dir/app_#{@app.id}`文件(`package_dir`为`AppConfig[:directories][:droplets]`)，并在数据库中更新`package_hash`为最新的sha1值。最后删除所有的临时文件(夹)。

至此，更新/新建的app package经过解压-同步-压缩-移动几个步骤，完整地保存在`package_dir/app_#{@app.id}"`中了。这里可以看出resources pool的功能主要就是保存已经上传的代码，防止重复的文件上传，然而这个处理方法显然不如openshift的使用git进行版本控制的方法方便，不知在cc\_ng中是否改善，待分析完cc\_ng代码后再做评论。


### Step2: create/update app in cc

新建/更新app的请求示例如下

  	POST http://api.cf.com/apps 
  	request {"name":"{:app}","instances":1,"staging":{"model":"sinatra","stack":"ruby19"},"resources":{"memory":64}

  	PUT http://api.cf.com/apps/{:app}
  	{"name":"test","instances":1,"state":"STARTED","staging":{"model":"sinatra","stack":"ruby18"},"resources":{"memory":64,"disk":2048,"fds":256},"env":[],"uris":["test.cf.com"],"services":[],"console":null,"debug":null}

根据cc的`routes.rb`， 请求将由`AppsController#create`和`AppsController#update`处理，其核心部分是`AppsController#update_app_from_params(app)`，代码如下

    # Checks to make sure the update can proceed, then updates the given
    # App from the request params and makes the necessary AppManager calls.
    def update_app_from_params(app)
      CloudController.logger.debug "app: #{app.id || "nil"} update_from_parms"
      error_on_lock_mismatch(app)
      app.lock_version += 1

      previous_state = app.state
      update_app_state(app)
      # State needs to be changed from above before capacity check.
      check_has_capacity_for?(app, previous_state)
      check_app_uris(app)
      update_app_mem(app)
      update_app_env(app)
      update_app_staging(app)
      delta_instances = update_app_instances(app)

      changed = app.changed
      CloudController.logger.debug "app: #{app.id} Updating #{changed.inspect}"

      # reject attempts to start in debug mode if debugging is disabled
      if body_params[:debug] and app.state == 'STARTED' and !AppConfig[:allow_debug]
        raise CloudError.new(CloudError::APP_DEBUG_DISALLOWED)
      end

      app.metadata[:debug] = body_params[:debug] if body_params
      app.metadata[:console] = body_params[:console] if body_params

      # 'app.save' can actually raise an exception, if whatever is
      # invalid happens all the way down at the DB layer.
      begin
        app.save!
      rescue Exception => e
        CloudController.logger.error "app: #{app.id} Failed to save new app errors: #{app.errors}.  Exception: #{e}"
        raise CloudError.new(CloudError::APP_INVALID)
      end

      # This needs to be called after the app is saved, but before staging.
      update_app_services(app)
      app.save if app.changed?

      # Process any changes that require action on out part here.
      manager = AppManager.new(app)

      stage_app(app) if app.needs_staging?

      if changed.include?('state')
        if app.stopped?
          manager.stopped
        elsif app.started?
          manager.started
        end
        manager.updated
      elsif app.started?
        # Instances (up or down) and uris we will handle in place, since it does not
        # involve staging changes.
        if changed.include?('instances')
          manager.change_running_instances(delta_instances)
          manager.updated

          user_email = user ? user.email : 'N/A'
          CloudController.events.user_event(user_email, app.name, "Changing instances to #{app.instances}", :SUCCEEDED)

        end
      end

      # Now add in URLs
      manager.update_uris if update_app_uris(app)

      yield(app) if block_given?
    end

前40行的逻辑非常简单，根据request中的参数，更新db中app对象的url,mem,env,runtime,framework,services信息，并更新到数据库中，接下来分为几个详细的步骤

1. **stage_app** 将app打包成droplet，可以供dea执行。作为cc只是将此消息在NAT上通知stager
2. **stager** 将实际处理打包任务，下载app->打包->上传
3. **start/stop app instance** 启动/停止dea中的app的instance或调整instance数量符合用户需求

最终`AppManager#update_uris`会将更新的url在NAT上通知dea，dea接收新的url后将droplet注册到routers，后续对该url的请求都会路由到对应的dea中执行。


### Step3: publish message to stage in cc

`AppsController#stage_app`的逻辑非常简单，就是利用`StagingController`生成download url 和upload url以便stager下载app code以及上传droplet，当stager完成后，将droplet移动到`package_dir/droplet_#{@app.id}`，并更新`package_state`为`STAGED`(如果打包失败，则为`FAILED`)

这里代码比较简单，就不详细介绍，但是我们需要介绍一下cc发送到NAT的消息，topic=`AppConfig[:staging][:queue]`。内容说明如下：


    {
      "app_id"       => app.id,
      "properties"   => app.staging_task_properties,
      "download_uri" => dl_uri, # /staging/app/#{app.id}
      "upload_uri"   => ul_hdl.upload_uri, # /staging/droplet/#{app.id}/#{VCAP.secure_uuid}
    }


其中 `app.staging_task_properties` 如下


    {    
    	"services"       => services,
      "framework"      => framework,
      "framework_info" => Framework.find(framework).options,
      "runtime"        => runtime,
      "runtime_info"   => Runtime.find(runtime).options,
      "resources"      => resource_requirements,
      "environment"    => environment,
      "meta" => metadata 
    }


这里暂时不讨论包含services的情况，所以services={}
framework和runtime对应request中的`model`和`stack`；
resources = `{"memory" => memory, "disk" => disk_quota, "fds" => file_descriptors}`，指明资源的限制;
environment和meta分别对应request中的`env`和`meta`，后者默认为[]。

`Framework.find(framework).options`的值来自于`AppConfig[:directories][:staging_manifests]/{framework_name}.yml`。

`Runtime.find(runtime).options`的值来自于`AppConfig[:runtimes_file]`，值为对应runtime下的HASH


### Step4: stage app in stager

stager节点主要包含两个项目`stager`和`vcap-staging`，前者接收cc的消息，启动后者进行实际的打包工作。

处理`AppConfig[:staging][:queue]`topic 的方法为`VCAP::Stager::Server#execute_request(encoded_request, reply_to)`，会根据message建立一个`VCAP::Stager::Task`实例，并执行其`preform`方法。


    def perform
      @logger.info("Starting task for request: #{@request}")

      @task_logger.info("Setting up temporary directories")
      workspace = VCAP::Stager::Workspace.create

      @task_logger.info("Downloading application")
      app_path = File.join(workspace.root_dir, "app.zip")
      download_app(app_path)

      @task_logger.info("Unpacking application")
      unpack_app(app_path, workspace.unstaged_dir)

      @task_logger.info("Staging application")
      stage_app(workspace.unstaged_dir, workspace.staged_dir, @task_logger)

      @task_logger.info("Creating droplet")
      droplet_path = File.join(workspace.root_dir, "droplet.tgz")
      create_droplet(workspace.staged_dir, droplet_path)

      @task_logger.info("Uploading droplet")
      upload_droplet(droplet_path)

      @task_logger.info("Done!")

      nil

    ensure
      workspace.destroy if workspace
    end


 经过了6步处理

 1. `VCAP::Stager::Workspace.create`会创建用于处理stage任务的文件夹，形如：

     	    root_dir=	  .
    	unstaged_dir=	  ├── unstaged/
    	  staged_dir=	  └── staged/
 
 2. `download_app`根据message中的`download_uri`利用curl下载app的code zip包，保存至`root_dir/app.zip`

 3. `unpack_app`利用`unzip`解压app的代码包到unstaged_dir中

 4. `stage_app(workspace.unstaged_dir, workspace.staged_dir, @task_logger)`将unstaged\_dir中的代码进行调整，安装需要的包和添加开始/停止脚本等，并将未压缩的droplet保存到staged\_dir

 5. `create_droplet`将staged\_dir中的文件打包成droplet.tgz保存在root\_dir中

 6. `upload_droplet`根据message中的`upload_uri`上传生成的droplet.zip

 可见核心部分在`stage_app`方法上，如果分析代码会发现，实际上执行的就是一条shell命令

 `cmd = [@ruby_path, @run_plugin_path, @request["properties"]["framework_info"]["name"], plugin_config_file.path].join(" ")`
 
 即执行 `ruby path_to_stager/bin/run_plugin framework_name file_of_opinion`.其中`file_of_opinion`包含的信息如下


   {
      "source_dir"   => unstaged_dir,
      "dest_dir"     => staged_dir,
      "environment"  => @request["properties"]
      "secure_user"  => {"uid" => secure_user[:uid],
  				      "gid" => secure_user[:gid], }
   }


其中`run_plugin`关键内容如下


    plugin_name, config_path = ARGV

    klass  = StagingPlugin.load_plugin_for(plugin_name)
    plugin = klass.from_file(config_path)
    plugin.stage_application


这里我们举sinatra/ruby18为例子说明制作droplet的过程，如果需要扩展支持更多的runtime/framework，扩展工作在此处进行。则对应的对应plugin的执行方法为`SinatraPlugin#stage_application`.如果是其他framework，根据`StagingPlugin#load_plugin_for`会加载`vcap-staging/lib/vcap/staging/plugin/<framework_name>/plugin.rb`中的`<Framework>Plugin`，其中加载ruby文件的framework名一般遵从下划线命名法(java_web.rb)，而对象遵从帕斯卡命名法(JavaWebPlugin)


    def stage_application
      Dir.chdir(destination_directory) do
        create_app_directories
        copy_source_files
        compile_gems
        install_autoconfig_gem if autoconfig_enabled?
        create_startup_script
        create_stop_script
      end
    end


**1. `create_app_directories` 创建一些标准的文件夹**

        root_dir=   .
    unstaged_dir=   ├── unstaged/
      staged_dir=   └── staged/
         *app_dir=          ├── app/
         *log_dir=          ├── log/
         *tmp_dir=          └── tmp/
    (*为新创建的文件夹)

**2. `copy_source_files` 将app代码从`unstaged_dir`复制到`app_dir`**

**3. `compile_gems` 根据runtime的ruby版本，安装gems.**
  
      def compile_gems
        return unless uses_bundler?
        return if packaged_with_bundler_in_deployment_mode?

        gem_task.install
        gem_task.install_bundler
        gem_task.remove_gems_cached_in_app

        write_bundle_config
      end
 
  `GemfileSupport#compile_gems`的注释说明了工作过程，这里采用ruby bundle工具进行依赖管理。

   + 如果没有`Gemfile.lock`文件，说明包管理使用其他的方法，则直接return，不进行处理
   + 如果有`:unstaged_dir/vendor/bundle/{ruby_version}`说明用户使用`bundle install --local --deployment`的方式已经将需要的gem放在正确的位置下，因此也不需要进行额外的stage工作
   + 接下来通过`GemfileTask`安装gem
     - `install`会安装`Gemfile.lock`文件里的gem，如果local cache中没有，则从git-repo/rubygems下载并保存在cache中, 然后使用`gem install`命令安装.
        (主要代码分布于`gemfile_parser` `gemspec_builder` `git_cache` `gem_cache` )
        1. 这里的过程是利用`gemfile_parser.rb`将`Gemfile.lock`中的gem和版本信息(包括来自github的gem)进行分析，将所需要的所有gem写入到`specs`文件中，然后根据`specs`文件安装gem。
        `specs`文件主要标识了gem的 name, version 和 source，如果source是git方式[即`spec.source.class.name = Bundler::Source::Git`]，则会包含额外的 git_scope, url, revision, submodules信息
        2. 安装时会区分source。如果是普通的gem，则首先尝试从`@app_dir/vendor/cache/`目录中查找用户上传文件中包含的gem，如果没有则从`<package_cache>/blessed_gems/`目录中查找该gem(<package_cache>为stager server配置文件platform.yml中cache的值)，最后用户既没提供，本地缓存的也没有，则会从rubygems中下载该gem并保存至`<package_cache>/blessed_gems/`目录下缓存。如果是git gems，则先检查缓存gem，如果没有，则从git-repo下载，根据其中的*.gemspec文件build出gem，然后根据该gem安装
        3. 安装gem的命令是`gem install #{staged_gemfile} --local --no-rdoc --no-ri -E -w -f --ignore-dependencies --install-dir #{gem_install_dir}`，将gem安装(解压)到一个临时文件夹中，然后复制到`<package_cache>`下的一个散列后的文件夹中缓存，最后将解压后的gem包复制到`@app_dir/rubygems/ruby/@library_version/`中去，git的gem则存到该目录的`bundler/gems/:git_scope`中。

        综上，安装gem的过程其实和运行`bundle install --local --deployment`的结果相同，但是stager安装的过程中会大量缓存gem和gem_package，因此在多次安装的场景中会大大降低网络请求的数据量

     - `install_bundler`即安装bundler-1.2.1
     - `remove_gems_cached_in_app`删除`@app_dir/rubygems/ruby/@library_version/cache`目录用户可能保存的gem
   + `write_bundle_config`主要作用是写入`BUNDLE_PATH: rubygems ;BUNDLE_DISABLE_SHARED_GEMS: "1"; BUNDLE_WITHOUT`以便在DEA中运行bundle

**4. `install_autoconfig_gem` 如果存在`staged_dir/app/config/cloudfoundry.yml`且其中`autoconfig`的值安装gem `cf-runtime 0.0.2`和`cf-autoconfig 0.0.4`, 如果不为false都会安装, 这个gem可以帮助用户在代码中调用cf的API连接service(mysql, redis)** gem doc的介绍如下

> A library for interacting with Cloud Foundry services. Provides methods for obtaining pre-configured connection objects and connection properties.

**5. `create_startup_script`和`create_stop_script`创建 app的启动/停止脚本，无非就是设置一些环境变量和启动/停止命令代码分布于`staging_plugin`和`plugin/xx/plugin`中，由于不同runtime/framework的脚本差异较大，不作详细介绍**

至此，用户上传的app的源代码经过了stager-server的打包，将完整的依赖包都安装之后压缩上传给cc，已经具有start/stop脚本，可以直接执行了


### Step5: Start/stop instance

cc收到stager打包后的app之后，开始准备根据用户提供的`resources`更新/启动在DEA中app，调整DEA中运行的app的数量，主要操作也就是start/stop instance.

启动dea中的app分成两个步骤，首先cc寻找可以接收此app的dea，其次dea根据消息下载staged app (即 droplet)并启动droplet。

**1. cc寻找dea** 

  代码如下

    def find_dea_for(message)
      if AppConfig[:new_initial_placement]
       DEAPool.find_dea(message)
      else
        find_dea_message = {
          :droplet => message[:droplet],
          :limits => message[:limits],
          :name => message[:name],
          :runtime_info => message[:runtime_info],
          :runtime => message[:runtime],
          :prod => message[:prod],
          :sha => message[:sha1]
        }
        json_msg = Yajl::Encoder.encode(find_dea_message)
        result = NATS.timed_request('dea.discover', json_msg, :timeout => 2).first
        return nil if result.nil?
        CloudController.logger.debug "Received #{result.inspect} in response to dea.discover request"
        Yajl::Parser.parse(result, :symbolize_keys => true)[:id]
      end
    end

    #message is init here
    def new_message
      data = {:droplet => app.id, :name => app.name, :uris => app.mapped_urls}
      data[:runtime] = app.runtime
      data[:runtime_info] = Runtime.find(app.runtime).options
      data[:framework] = app.framework
      data[:prod] = app.prod
      data[:sha1] = app.staged_package_hash
      data[:executableFile] = app.resolve_staged_package_path
      data[:executableUri] = "/staged_droplets/#{app.id}/#{app.staged_package_hash}"
      data[:version] = app.generate_version
      data[:services] = app.service_bindings.map {|sb| sb.for_dea }
      data[:limits] = app.limits
      data[:env] = app.environment_variables
      data[:users] = [app.owner.email] 
      data[:cc_partition] = AppConfig[:cc_partition]
      data
    end

  如果cc的配置文件中`new_initial_placement`为true，则会从DEAPool中取得一个满足resource要求的DEA，否则在NAT中发送广播消息等待DEA回应。 前者的方式是根据DEA定期发送的`dea.advertise`消息获得当前全局DEA的资源状态，并从中取得一个合适的DEA。后者则是立刻发送一个`dea.discover`消息等待满足的条件的DEA回复自己包含`{ :id => uuid, :ip => @local_ip, :port => @file_viewer_port, :version => VERSION }`的消息。有了这些消息，接下来cc就可以发送启动命令给DEA要求DEA启动droplet了

  DEA响应的方法为`DEA::Agent#process_dea_discover(message, reply)`, 代码比较简单

**2. dea启动droplet**

      def start_instances(start_message, index, max_to_start)
        EM.next_tick do
          f = Fiber.new do
            message = start_message.dup
            message[:executableUri] = download_app_uri(message[:executableUri])
            message[:debug] = @app.metadata[:debug]
            message[:console] = @app.metadata[:console]
            (index...max_to_start).each do |i|
              message[:index] = i
              dea_id = find_dea_for(message)
              json = Yajl::Encoder.encode(message)
              if dea_id
                CloudController.logger.debug("Sending start message #{json} to DEA #{dea_id}")
                NATS.publish("dea.#{dea_id}.start", json)
              else
                CloudController.logger.warn("No resources available to start instance #{json}")
              end
            end
          end
          f.resume
        end
      end

  在这里cc通过在NATS上发送`topic=dea.#{dea_id}.start`的消息，告知dea_id对应的DEA下载droplet的URL, resource limit等等一切所需要的消息，等待DEA启动droplet.

  DEA这边处理该请求的方法是`DEA::Agent#process_dea_start(message)`([github](https://github.com/cloudfoundry/dea/blob/master/lib/dea/agent.rb#L554))，代码比较多就不贴出来了。值的注意的是占巨大行数的`start_operation`是一个lambda表达式，所以执行的过程是进行了一通json解析和验证之后，执行`stage_app_dir`来从cc下载和解压droplet，然后才会调用`start_operation.call`来执行启动流程。在`start_operation`中有两个proc - `exec_operation`和`exit_operation`分别对应启动droplet的方法和停止后的回调方法.启动是通过EventMachine.system启动的 - `EM.system("#{@dea_ruby} -- #{prepare_script} true #{sh_command}", exec_operation, exit_operation)`
  其中`prepare_script`即为dea/bin/close_fds, 关闭`/proc/self/fd/`下除了stdin stdout stderr外的其他文件句柄。

  从`exec_operation`的代码可以看出，v1版本的dea实现的隔离性非常有限，仅仅是通过`ulimit`进行一些基本的限制，隔离水平远远达不到商用的水平(所以v1版本的cc和dea一直都是免费在用)，尤其是缺少cpu和网络的隔离，在v2版本推出带来基于cgroups的warden才能解决此问题。

**3. dea停止droplet**

  停止dea中的app非常简单，cc在nats中发送消息 topic = "dea.stop" msg = { :droplet => app.id, :version => app.generate\_version, :indices => indices } 即可，如果停止有限个instance, indices即为停止的index的集合，否则只包含`:droplet`将停止全部该app的droplet。停止过程就是执行droplet中的停止脚本并删除droplet所在文件夹；同时发送topic = 'droplet.exited' 和 'router.unregister'向health\_manager和router通知droplet已经停止。代码非常简单, 有兴趣的可以跟踪`DEA::Agent#stop_droplet(instance)`

---

## 结语

本文从代码级别对cf v1版本中部署app的过程进行了简要介绍，重点解释了关键函数和流程。然而更多的内容需要深入代码理解才行，希望本文能给希望一窥cf如何部署执行app的
朋友带来帮助。

本文重点介绍过程，并没对cloud_controller, stager和dea的代码结构和框架进行详细介绍，仅仅对关键方法进行说明。然而由于这3个项目都是ruby项目，代码阅读起来比较清爽，所以有兴趣了解全貌的朋友可以花些时间读读代码。

由于本人写作能力有限，本文又臭又长，非常感激有人能读到此处。最后抱怨一下vmware的工程师喜欢把一个文件里写太多功能而非通过module分开然后include的方法，dea中agent.rb有1868行...Xp

---

## Troube Shooting

1. create manifest failed - NoMethodError: undefined method "buildpack" for #<CFoundry::V1::App 'test'>

造成此问题的原因在于manifests-vmc-plugin-0.6.3.rc2的一个bug。此包会根据用户设定生成部署的manifest以便在日后部署能够自动进行大多数步骤。然而，由于V1版App对象没有buildpack属性(见cfoundry-0.5.3.rc7/lib/cfoundry/v1/app.rb)，而在manifests-vmc-plugin中会根据此属性生成manifest文件(代码见<https://github.com/cloudfoundry/manifests-vmc-plugin/blob/master/lib/manifests-vmc-plugin.rb#L189>).解决此问题的方法是将此行改为

`if app.respond_to?("buildpack") and buildpack = app.buildpack`

本人已经将此bug fix提交给repo的owner，pull request见此<https://github.com/cloudfoundry/manifests-vmc-plugin/pull/4>。
