---
layout: post
title: "Ceph All-in-one Scripts"
tagline : "Single node ceph build and installation scripts"
description: "Ceph All-in-one Scripts"
category: "ceph"
tags: [cloud, storage, filesystem, ceph]
---
{% include JB/setup %}

While learning manual deployment of ceph on single node, I wrote these scripts to automate the process. After modifing ceph source and re-make install, these scripts could make it easy to cleanup and re-deploy monitor and OSD, then see the result. 

Currently I've been using it on Ubuntu Server 12.04. To use it on redhat based systems you need to modifiy `inst-ceph-dep.ubuntu.sh`, which installs ceph dependencies. Hope it has some use for you :-)

## [Ceph-all-in-one](https://github.com/accelazh/ceph-allinone)

Link: [https://github.com/accelazh/ceph-allinone](https://github.com/accelazh/ceph-allinone)

Shell scripts to build ceph from source and install monitor & OSD services on single node (i.e. ceph storage cluster). Made easy to do quick and fresh-clean re-install. 

Although these scripts help you quickly build a single node ceph storage cluster. The purpose of these scripts is, you want to git download a copy of ceph source code, then repeatly modify it & re-build it & re-deploy it to see the result. I.e. to develop on ceph code.

Installation process follows [Ceph Manual Deploy](http://ceph.com/docs/master/install/manual-deployment/). `ceph-deploy` tool is not used. Because it is inconvenient to install from your own modified copy of source code using ceph-deploy. 

## Usage

Prepare Ubuntu Server 12.04 system. It is recommended to use a clean system and not to login as root account. ssh to the host and clone [ceph-allinone](https://github.com/accelazh/ceph-allinone).

```bash
git clone https://github.com/accelazh/ceph-allinone.git
cd ceph-allinone
```

First, use below command. It will git download ceph code, install dependency, build it and make install. The ceph git folder is `./workspace/ceph`. Git branch is 'firefly'. You can change the branch in `config.sh` (it is the configuration file). 

NO SUDO is needed for any of these scripts. When they actually need permission for a specific command, you will be prompted. 

```bash
./install-ceph.sh
```

Second, modify the config file for these scripts (although mostly you don't need to modify anything). `config.sh` contains all the configuration.

```bash
vim ./config.sh
```

At last, config and start services. No sudo is needed to run this command. You will get prompt if need permission. At any time you can run this command again, even after error occurred, to re-install again.

```bash
./config-all.sh
```

If `config-all.sh` says success in the end and printed out how-to-use, it means installation successfully completed and you get the ceph storage cluster functional and working. If you `ps -ef | grep ceph`, you should see ceph-mon and ceph-osd processes running.

Note that no service are installed into /etc/init.d or system service. You will have to use start-*/stop-* scripts to manage them.

## Optional Usage

Use connect.sh to enter ceph command line and check status and health.

```bash
./connect.sh
ceph> status
...
ceph> health
...
ceph> health detail
...
```

Check log file `/var/log/ceph` to troubleshoot.
```bash
grep -ir error /var/log/ceph
```

Manage services by start-*/stop-* scripts.

```bash
# stop all services
./stop-all.sh
# start all services
./start-all.sh
# restart all services
./restart-all.sh
# stop monitor services
./stop-mon.sh
# start monitor services
./start-mon.sh
# stop OSD services
./stop-osd.sh
# start OSD services
./start-osd.sh
```

You can test whether the services are working. During above installation, tests are already performed to check whether it works fine. 

```bash
# test all services
./test-all.sh
# test monitor services
./test-mon.sh
# test OSD services
./test-osd.sh
```

At anytime, even when installation totally corrupted and failed, you can use this command to remove all the config and data files of ceph to restore to a fresh clean start. 

```bash
./purge-all.sh
```

Git downloaded source code, make & make install generated library files and executable files will not be removed. Because they don't need to and you can manage them using `make`. It is the configuration and data files of ceph services that are cleaned. After this command you will get a fresh clean environment, ready to re-install.

At anytime, even when installation totally corrupted and failed, you can re-install ceph services using below command. No need to stop service or run `purge-all.sh`, because they are already included.

```bash
./config-all.sh
```

Like `purge-all.sh`, `config-all.sh` won't touch git download source code, make & make install generated library files and executable files. It is the configuration and data files of ceph services are re-installed. Usually it is them that should be re-installed.

If you have modified ceph code, of course before `config.sh` you need to make and make install.

## Limitations

Thess scripts have only been tested on Ubuntu Server 12.04. 

All scripts are assumed Linux platform independent except `inst-ceph-dep.ubuntu.sh`. This script apt-get install all the dependencies to build ceph. You may need to write another version for your platform.
