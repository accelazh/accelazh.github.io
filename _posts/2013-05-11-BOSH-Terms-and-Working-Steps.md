---
layout: post
category : BOSH
title : "BOSH Terms and Working Processes"
tagline: "BOSH相关的术语和工作流程"
tags : [BOSH]
---

{% include JB/setup %}

## Terms:

## Cloud Foundry

[Cloud Foundry](http://cloudfoundry.org) is a Open Source PaaS solution. It is available as a public cloud at [http://cloudfoundry.com](http://cloudfoundry.com) operated by VMWare, but it is also a solution you can bring in-house and install on your own servers, or even operate on Amazon like [AppFog](http://appfog.com) does.

* __Cloud Controller__ is the main component in Cloud Foundry and the server you point your vmc command to. It can be split up into separate VMs, but this bootstrap keeps it all on one instance.
* __DEA__ is the compute instance. In the initial setup the Cloud Controller is also a DEA. But you can basically view it as VMs that will handle and serve your applications.
* __Service__ is the concept Cloud Foundry uses to describe added functionality to your application like Postgres or MongoDB.

## BOSH 

[BOSH](https://github.com/cloudfoundry/bosh) is a cloud oriented tool chain for releasing, deployment and lifecycle management of applications. It abstracts away the underlying IaaS solution (AWS, OpenStack, VMWare) and performs requests for new virtual machines etc. It also handles the distribution of "Jobs" to the virtual machines in the BOSH setup. In some ways you can say that it eliminates the need for Puppet/Chef, but it uses some different concepts. It also covers more, like the provisioning of virtual machines.

* __Job__ is BOSH's concept of grouping functionality together. In the normal instance you can think of a Job as a composition of installed software and configuration that a virtual machine will have. So two virtual machines with the same Job attached will be identical.
* __Template__ is BOSH's concept for defining a software setup. CloudController is one such template, and dea is another one.
* __Stemcell__ is BOSH's concept for a virtual machine image. For Amazon it equals and AMI. It is a template that is booted and becoms an instance of an virtual machine.
* __Resource Pool__ is basically a collection of virtual machines, that you can reference/assign jobs to. The have the same stemcell and configuration (eg. AWS size).
* __Compilation instance__ is instances that BOSH uses when deploying a new part. At first it is used to compile everything that is needed for VCAP and DEA. If you add a template like Postgres you'll see that it compiles the components used for that. I think this is something that resembles rpm or deb packages, and that they get compiled on your Stemcells to ensure compatibility when running on your cloud.
* __Inception VM__ is a Virtual Machine used for bootstrapping BOSH.

## A BOSH deployment

### Stemcell - A VM image with bosh_agent installed

In a cloud platform, VMs are usually cloned from a template. A stemcell is a VM template containing a standard Ubuntu distribution.A BOSH agent is also embedded in the template so that BOSH can take control of VMs cloned from the stemcell. The name “stemcell” originated from biological term “stem cells”, which refers to the undifferentiated cells that are able to grow into diverse cell types later. Similarly, VMs created by a BOSH stemcell are identical at the beginning. After inception, VMs are configured with different CPU/memory/storage/network, and installed with different software packages. Hence, VMs built from the same stemcell template behavior differently.

### Deployments - From static release into runnable software on VMs.

A deployment is something that turns a static release into runnable software on VMs. A Deployment Manifest defines the actual values of parameters needed by a deployment. During a deployment process, BOSH substitutes the parameters in the release and makes the software run on the configuration as planned.

### Release - A collection of source code, configuration file and start-up scripts used to run services

    └── bosh-release                  //release name
      ├── config                      //release configuration file
      ├── git                         //use git to manage versions of the contained files
      ├── jobs                        //job definitions
      ├── blobs                       //large source code bundles
      ├── packages                    //package definitions
      ├── releases                    //final releases
      └── src                         //source code for packages

A release contains collections of software bits and configurations which will be installed onto the target system. Each VM is deployed with a collection of software, which is called a job. Configurations are usually templates which contain parameters such as IP address, port number, user name, password, domain name. These parameters will be replaced at deploy time by the properties defined in a deployment manifest file.

#### Job - Configuration of how to operate (start/stop) services installed from packages

Jobs are a realization of packages. A job contains the configuration files and startup scripts to run the binaries from a package.
     
There is a many-to-many mapping between jobs and VMs - one or more jobs can run in any given VM and many VMs can run the same job. E.g. there can be four VMs running the Cloud Controller job, the Cloud Controller job and the DEA job can also run on the same VM. If you need to run two different processes (from two different packages) on the same VM, you need to create a job which starts both processes.

    └── jobs    
        └── nats    
           ├── monit
           ├── spec
           └── templates
              ├── nats_ctl.erb
              └── nats.yml.erb

* __`templates`__

  The job templates are generalized configuration files and scripts for a job, which uses [ERB](http://ruby-doc.org/stdlib-1.9.3/libdoc/erb/rdoc/ERB.html) files to generate the final configuration files and scripts used when a Stemcell is turned into a job. When a configuration file is turned into a template, instance specific information is abstracted into a property which later is provided when the director starts the job on a VM
  
  The properties used for a job comes from the deployment manifest, which passes the instance specific information to the VM via the agent. 

* __`spec`__

  When a VM is first started, is a Stemcell, which can become any kind of job. It is first when the director instructs the VM to run a job as it will gets its personality.

* __`monit`__

BOSH uses monit to manage and monitor the process(es) for a job. The monit file describes how the BOSH agent will stop and start the job, and it contains at least three sections:

* `with pidfile` : Where the process keeps its pid file
* `start program` : How monit should start the process
* `stop program` : How monit should stop the process

Usually the monit file contain a script to invoke to start/stop the process, but it can invoke the binary directly.

#### packages - Configration of how to compile & install packages 

A package is a collection of source code along with a script that contains instruction how to compile it to binary format and install it, with optional dependencies on other pre-requisite packages.


    └── packages
        └── nats
            ├── packaging
            └── spec

* __`packaging`__

Packages are compiled on demand during the deployment. The director first checks to see if there already is a compiled version of the package for the stemcell version it is being deployed to, and if it doesn't already exist a compiled version, the director will instantiate a compile VM (using the same stemcell version it is going to be deployed to) which will get the package source from the blobstore, compile it, and then package the resulting binaries and store it in the blobstore.

`packaging` script that is responsible for the compilation, and is run on the compile VM. The script gets two environment variables set from the BOSH agent:

* `BOSH_INSTALL_TARGET` : Tells where to install the files the package generates. It is set to `/var/vcap/data/packages/<package name>/<package version>`.

* `BOSH_COMPILE_TARGET` : Tells the the directory containing the source (it is the current directory when the packaging script is invoked).

When the package is installed a symlink is created from `/var/vcap/packages/<package name>` which points to the latest version of the package. This link should be used when referring to another package in the packaging script.

There is an optional pre\_packaging script, which is run when the source of the package is assembled during the bosh create release. It can for instance be used to limit which parts of the source that get packages up and stored in the blobstore. It gets the environment variable BUILD_DIR set by the BOSH CLI which is the directory containing the source to be packaged.

*  __`spec`__

`spec` file contents package specification.which has three sections:

* `name` : The name of the package.

* `dependencies` : An optional list of other packages this package depends on. These dependencies are compile time dependencies, as opposed to the job dependencies which are runtime dependencies. When the director plans the compilation of a package during a deployment, it first makes sure all dependencies are compiled before it proceeds to compile the current package, and prior to commencing the compilation all dependent packages are installed on the compilation VM.

* `files` : A list of files this package contains, which can contain globs. A `*` matches any file and can be restricted by other values in the glob, e.g. `*.rb` only matches files ending with `.rb`. A `**` matches directories recursively.

#### config - The release configuration file



    └── config
        ├── blobs.yml
        └── final.yml

* __`blobs.yml` : The list of packages in blobs storage__

sample as :

    nats/vendor/cache/rack-1.3.5.gem:
      object_id: eyJvaWQiOiI0ZTRlNzhiY2EzMWUxMjIyMDRlNGU5ODYzYjFiNzQwNGZiZDRm%0AMTg5MDk3ZiIsInNpZyI6InFiZWN1SmMrZGRTeWdLYWV0MTl5c2kwaE5yND0i%0AfQ==%0A
      sha: 8ceed89e9a1d0039002eca26e579de8ad5883516
      size: 155648


* __`final.yml` : The configration file for the release__

sample as:

    --- 
    final_name: bosh
    min_cli_version: 1.0.3
    blobstore:
      provider: atmos
      options:
        tag: BOSH
        uid: 92b8944a45f24e94b4ad254d98ab1f25/bosh-release-uid
        url: https://blob.cfblob.com


#### releases - Configration of which `packages` and `jobs` are used in a final releases


    └── releases
        ├── bosh-1.yml
        ├── bosh-2.yml
        └── index.yml

The `releases` folder contains the `yml` file declaring the content of the release : `packages` and their dependencies.

* __`bosh-*.yml` : which `packages` and `jobs` in a final releases__

sample 

    ---
    packages: 
    - name: ruby
      version: 1
      sha1: cbab7b06a703e5b0a407ab20e0d1ef91fa6119cc
      dependencies: []
    - name: nats
      version: 1
      sha1: d5a042c08c70df1e32d9b75ee3872f04c2fd08c0
      dependencies:
       - ruby
    jobs:
    - name: nats
      version: 1
      sha1: 8e903b443185d657933b9f085b9db807c12177a4
    ...
    name: bosh
    version: 1

_here the dependencies are job dependencies_

* __`index.yml` : index of all releases__

sample as:

    --- 
    builds:
      c31b8fec04fdf27f8e7a3a361ae0019bf4d0c3b4:
        version: 1

#### src - The source folder from which the release is created

The source folder from which the release is created

#### blobs - large source code bundles (object storage)

To create final releases you need to configure your release repository with a blobstore. This is where BOSH will upload the final releases to, so that the release can later be retreived from another computer.

To prevent the release repository from becoming bloated with large binary files (source tar-balls), large files can be placed in the blobs directory, and then uploaded to the blobstore.

For production releases you should use either the Atmos or S3 blobstore and configure them as described below.trying out BOSH and don't have an Atmos or S3 account, you can use the local blobstore provider (which stored the files on disk instead of a remote server).

_NOTE: To config the blobs storage, the configration file is `config/blobs.yml`_

current support blobs storage are _[simple s3 swift atmos local]_

* s3 sample

in config/final.yml :

    ---
    blobstore:
      provider: s3
      options:
        access_key_id: KIAK876234KJASDIUH32
        bucket_name: 87623bdc
        encryption_key: sp$abcd123$foobar1234

in config/private.yml:

    ---
    blobstore_secret: ahye7dAS93kjWOIpqla9as8GBu1=


* local sample

in config/final.yml : 

    ---
    blobstore:
      provider: local
      options:
        blobstore_path: /path/to/blobstore/directory



## BOSH Working Steps:

![bosh working steps](/images/bosh_working_steps.png)

1. If some packages in the release require compilation, BOSH first creates a few temporal VMs (worker VMs) to compile them. After compiling the packages, BOSH destroys the worker VMs and stores the binaries to its internal blobstore.

2. BOSH creates a pool of the VMs which will be the nodes where the release to be deployed on. These VMs are cloned from the stemcell with a BOSH agent installed.

3. For each job of the release, BOSH picks a VM from the pool and updates its configuration according to the Deployment Manifest. The configuration may include IP address, persistent disk size etc.

4. When the reconfiguration of the VM is completed, BOSH sends commands to the agent inside each VM. The commands tell the agent to install software packages. During the installation, the agent may download packages from BOSH and installs them. When the installation finishes, the agent runs the starting script to launch the job of the VM.

5. BOSH repeats step 3-4 until all jobs are deployed and launched. The jobs can be deployed simultaneously or sequentially. The value `max_in_flight` in the manifest file controls this behavior. When it is 1, it means the jobs are deployed one by one. This value is useful for a slow system to avoid timeout caused by resource congestion. While it is greater than one, it means jobs are deployed in parallel.

## How BOSH do scaling

![BOSH-CF initial deploy](/images/BOSH-cf-initial-create.png)

1. The bosh-bootstrap gem on "My Computer" creates an Inception virtual machine from an Ubuntu image.
2. The Inception VM creates the BOSH controller
3. The BOSH controller creates virtual machines for Cloud Foundry
4. The BOSH controller deploys Jobs to the separate instances

One example of deployments is as below (one core and many dea and services)

![BOSH-CF scaled deploy](/images/BOSH-cf-scaled.png)

### How ?

1. Create/Update a new release
2. Upload the release
3. Edit deployment manifest.
4. `bosh deploy`


# BOSH Deployments 

## Steps of a Deployment 

When you do a deploy using BOSH the following sequence of steps occur:

1. Preparing deployment
    * binding deployment - Creates an entry in the Director's database for the deployment if it doesn't exist.
    * binding release - Makes sure the release specified in deployment configuration exists then locks it from being deleted.
    * binding existing deployment - Takes existing VMS and sets them up to be used for the deployment.
    * binding resource pools - Gives idle VMs network reservations.
    * binding stemcells - Makes sure the stemcell specified has been uploaded and then locks it from being deleted.
    * binding templates - Sets up internal data objects to track packages and their pre-reqs for installation.
    * binding unallocated VMs - For each job instance required it determines whether a VM running the instance already exists and assigns one if not.
    * binding instance networks - Reserves networks for each VM that doesn't have one.
1. Compiling packages - Calculates all packages and their dependencies that need to be compiled.  It then begins compiling the packages and storing their output in the blobstore.  The number of `workers` specified in the deployment configuration determines how many VMs can be created at once for compiling.
2. Preparing DNS - Creates DNS entry if it doesn't exist.
3. Creating bound missing VMs - Creates new VMs, deletes extra/oudated/idle VMs.
4. Binding instance VMs - Any unbound VMs are setup for the deployment.
5. Preparing configuration - Pulls in the configurations for each job to be run.
6. Updating/deleting jobs - Deletes unneeded instances, creates needed instances, updates existing instances if they are not already updated.  This is the step where things get pushed live.
7. Refilling resource pools - Creates missing VMs across resource pools after all instance updaters are finished to create additional VMs in order to balance resource pools.

## BOSH Deployment Manifest

The BOSH Deployment manifest is a YAML file defining the layout and properties of the deployment. When BOSH user initiates a new deployment using CLI, BOSH Director receives a version of deployment manifest and creates a new deployment plan using this manifest (see [Steps of a Deployment](#steps-of-a-deployment)). Manifest contains several sections:

* `name` [String, required] Deployment name. Single BOSH Director can manage multiple deployments and distinguishes them by name.
* `director_uuid` [String, required] Director UUID. Identifies BOSH Director that manages given deployment. A targeted Director UUID should match this property in order for BOSH CLI to allow any operations on the deployment.
* `release` [Hash, required] Release properties.
  * `name` [String, required] Release name. References a release name that wiill be used to resolve the components of the deployment (packages, jobs).
  * `version` [String, required] Release version. Points to the exact release version to use.
* `compilation` [Hash, required] Package compilation properties.
  * `workers` [Integer, required] How many compilation VMs will be created to compile packages.
  * `reuse_compilation_vms` [Boolean, optional] If set to true, compilation VMs will be re-used when compiling packages. If false, every time new package needs to be compiled (as a part of current deployment), a new worker VM will be created (up to a number of compilation workers) and it will be shut down after single package compilation is finished. Defaults to false. Recommended to set to true if IaaS takes a long time to create/delete VMs or to optimize package compilation cost (as compilation VMs are usually short-lived and some IaaS billing round up usage time to the hour).
  * `network` [String, required] Network name, references a valid network name defined in `networks` section. Compilation VMs will be assigned all their network properties according to the type and other properties of that network.
  * `cloud_properties` [Hash, required] Any IaaS-specific properties that will be used to create compilation VMs.
* `update` [Hash, required] Instance update properties. These control how job instances will be updated during the deployment.
  * `canaries` [Integer, required] Number of canary instances. Canary instances are being updated before other instances and any update error for canary instance means the deployment should stop. This prevents a buggy package or job from taking over all job instances, as only canaries will be affected by a problematic code. After canaries are done, other instances of this job will be updated in parallel (respecting `max_in_flight` setting).
  * `canary_watch_time` [Range<Integer>, Integer] How long to wait for canary update to declare job healthy or unhealthy. If Integer is given, director will sleep for that many seconds and check if job is healthy. If Range `lo..hi` is given it will wait for `lo` ms, see if job is healthy, and if it's not it will sleep some more, all up until `hi` ms have passed. If job is still unhealthy it will give up.
  * `update_watch_time` [Range<Integer> Integer]: Semantically no different from `canary_watch_time`, used for regular (non-canary) updates.
  * `max_in_flight` [Integer, required] Maximum number of non-canary instance updates that can happen in parallel.
* `networks` [Hash<Array>, required] Describes the networks used by deployment. See [nework_spec] for details.
* `resource_pools` [Hash<Array>, required] Describes resource pools used by deployment. See [resource_pool_spec] for details.
* `jobs` [Hash<Array>, required] Lists jobs included in into this deployment. See [job_spec] for details.
* `properties` [Hash, required] Global deployment properties. See [job_cloud_properties] for details.

### Network spec ###

Network spec specifies a network configuration that can be referenced by jobs. Different environments have very different networking capabilities, so there are several network types. Each type has a required `name` property that identifies the network within BOSH and has to be unique.

The more details network type description follows:

1. `dynamic` The network is not managed by Bosh. VMs using this network are expected to get their IP addresses and other network configuration from DHCP server or some other way, BOSH will trust each VM to report its current IP address as a part of its `get_state` response. The only extra property this network supports is `cloud_properties`, containing any IaaS-specific network details for CPI.
2. `manual` The network is completely managed by BOSH. Ranges are provided for dynamic, static and reserved IP pools, DNS servers. Manually managed networks can be further divided into subnets. When using this type of network BOSH takes care of assigning IP addresses, making network-related sanity checks and telling VMs which network configuration they are meant to use. This type of network has only one extra property `subnets`, an array of Hashes, where each hash is a subnet spec, containing the following properties):
  * `range` [String, required] Subnet IP range (as defined by Ruby NetAddr::CIDR.create semantics) that includes all IPs from this subnet.
  * `gateway` [String, optional] Subnet gateway IP.
  * `dns` [Array<String>, optional] DNS IP addresses for this subnet.
  * `cloud_properties` opaque IaaS-specific details passed on to CPI.
  * `reserved` [String, optional] Reserved IP range. IPs from that range will never be assigned to BOSH-managed VMs, these are supposed to be managed outside of BOSH completely.
  * `static` [String, optional] Static IP range. When jobs request static IPs, they all should be coming from some subnet static IP pool.
3. `vip` The network is just a collection of virtual IPs (e.g. EC2 elastic IPs) and each job spec will provide a range of IPs it supposed to have. Actual VMs are not aware of these IPs. The only extra property this network supports is `cloud_properties`, containing any IaaS-specific network details for CPI.

### Resource pool spec ###

Resource pool spec is essentially a blueprint for VMs created and managed by BOSH. There might be multiple resource pools within a deployment manifest, `name` is used to identify and reference them, so it needs to be unique. Resource pool VMs are created within a deployment and later jobs are applied to these VMs. Jobs might override some of the resource pool settings (i.e. networks) but in general resource pools are a good vehicle to partition jobs according to capacity and IaaS configuration needs. The resource pool spec properties are:

* `name`[String, required] Unique resource pool name.
* `network` [String, required] References a network name (see [network_spec] for details). Idle resource pool VMs will use this network configuration. Later, when the job is being applied to these resource pool VMs, networks might be reconfigured to meet job's needs.
* `size` [Integer, required] Number of VMs in the resource pool. Resource pool should be at least as big as the total number of job instances using it. There might be extra VMs as well, these will be idle until more jobs are added to fill them in.
* `stemcell` [Hash, required] Stemcell used to run resource pool VMs.
  * `name` [String, required] Stemcell name.
  * `version` [String, required] Stemcell version.
* `cloud_properties` [Hash, required] IaaS-specific resource pool properties (see [job_cloud_properties]).
* `env` [Hash, optional] VM environment. Used to provide specific VM environment to CPI `create_stemcell` call. This data will be available to BOSH Agent as VM settings. Default is {} (empty Hash).

### Job spec ###

Job is one or more VMs (called instances) running the same software and essentially representing some role. Job uses job template, which is a part of a release, to populate VM with packages, configuration files and control scripts that tell BOSH Agent what is to run on a particular VM. The most commonly used job properties are:

* `name` [String, required] Unique job name.
* `template` [String, required] Job template. Job templates are a part of a release and usually contained (in the raw form ) in release 'jobs' directory in release repo and get uploaded to BOSH Director as a part of a release bundle.
* `persistent_disk` [Integer, optional] Persistent disk size. If it's a positive integer, persistent disk will be created and attached to each job instance VM. Defaults to 0 (no persistent disk).
* `properties` [Hash, optional] Job properties. See [job_cloud_properties] for details.
* `resource_pool` [String, required] Resource pool to run job instances. References a valid resource pool name in `resource_pool` section.
* `update` [Hash, optional] Job-specific update settings. This allows overriding global job update settings on a per-job settings (similar to `properties`).
* `instances` [Integer, required] Number of job instances. Each instance is a VM running this particular job.
* `networks` [Array<Hash>] Networks required by this job. For each network the following properties can be specified:
  * `name` [String, required] Specifies network name in `networks` section.
  * `static_ips` [Range, optional] Specifies the range of IP addresses job supposed to reserve from that network.
  * `default` [Array, optional] Specifies which of default network components (dns, gateway) are populated from this network (this only makes sense if there are multiple networks).

### Job properties and cloud properties ###

There are two kinds of properties that can be featured in the deployment manifest.

1. cloud_properties: an opaque Hash that is being passed (usually "as-is") to CPI. Usually it controls some IaaS-specific properties (such as VM configuration parameters, network VLAN names etc). CPI is up to validate if these properties are correct.
2. job properties. Almost any non-trivial job needs some properties filled in, so it can understand how to talk to other jobs and what non-default settings to use. BOSH allows to list global deployment properties in a properties section of the deployment manifest. All this properties are recursively converted by director from Hash to a Ruby OpenStruct object, so they can be accessed by using original Hash key names as method names. The resulting OpenStruct is exposed under `properties` name and can be addressed in any job configuration template (using ERB syntax). Here's an example of de
fining and using a property:

File `deployment_manifest.yml`

    …
    properties:
      foo:
        bar:
          baz

File  `jobs/foobar_manager/templates/config.yml.erb`

    ---
    bar_value: <%= properties.foo.bar %>

Global properties are available to any job. In addition every job can define it's own `properties` section, these properties are only accessible within configuration templates of that job. Local job properties are being recursively merged into global job properties, so accessing them requires exactly the same syntax. Note that this can also be used to override global properties on per-job basis.

### Instance spec ###

Instance spec is a special object accessible to any job configuration file, similar to `properties` (actually `properties` is just a shortcut for `spec.properties`, so they are just a small part of spec). It contains a number of properties that can be used by job creator to access the details of a particular job instance environment and potentially make runtime-based decisions at the time of creating a job.

Two important parts of the instance spec are `job` and `index`. `job` contains job name and `index` contains 0-based instance index. This index is important if you want to only perform some actions (i.e. database migrations) on a particular job instance or want to test a new feature only on several instances but not all of them. Other things available through this spec are `networks` and  `resource_pool` which might be useful to get some data about job whereabouts.

## BOSH Property Store ##

Deployment manifest is a YAML file but it gets processed by ERB before being actually used, thus it might contain ERB expressions. This allows BOSH Director to substitute some properties saved in its database, so that sensitive or volatile data is only set at the time of deployment but not by manifest author at the time of creating the actual manifest.

BOSH CLI has several commands allowing property management:

  set property <name> <value>
  get property <name>
  unset property <name>
  properties

You can set the property using `bosh set property <name> <value>` and then reference it in the deployment manifest using `<%= property(name) %>` syntax.



## Reference

1. <http://www.think-foundry.com/cloud-foundry-bosh-introduction/>
2. <http://docs.cloudfoundry.com/docs/running/bosh/>
3. <https://github.com/StarkAndWayne/bosh-cloudfoundry/blob/master/docs/concept.md>
4. <https://github.com/TieWei/bosh-oss-docs/blob/master/bosh/documentation/bosh_deployments.md>