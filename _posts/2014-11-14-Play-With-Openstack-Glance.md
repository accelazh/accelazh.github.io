---
layout: post
title: "Play with Openstack Glance"
tagline : "Play with Openstack Glance"
description: "Play with Openstack Glance"
category: "Openstack"
tags: [openstack, glance, image, swift]
---
{% include JB/setup %}

## Architecture

Here is official [overview](http://docs.openstack.org/havana/install-guide/install/apt/content/image-service-overview.html).

![Glance architecture](/images/glance-architecture.png "Glance architecture")

What `registry` does? For [code api](https://github.com/openstack/glance/blob/master/glance/registry/api/v1/images.py), it providers CRUD access to images, communicating to DB. 

Storage adapter at [glance_store](https://github.com/openstack/glance_store) project. Cinder, filesystem, RBD, sheepdog, http are supported. There is general store interface at `glance_store.driver.py::Store`.

VM image: disk format vs container format, refer to [here](http://docs.openstack.org/developer/glance/formats.html):

  * Disk format is the format of the VM's disk image.
  * Container format is disk + metadata of actual virtual machine.

Glance does have a queuing system, also tasks and status. See [here](http://docs.openstack.org/developer/glance/statuses.html).

![Glance image status transition](/images/glance-image-status-transition.png "Glance image status transition")

P.S. Best ways to gather information for installation & deployment of Openstack components

  * How to install: check Openstack official manuals. This is the __BEST__ reference.
  * Config options: github source /etc/*.conf
  * Search config option name in source code.
  * Search in source code test cases for how to use example.

After play install and architecture diving, a complete review of config options will get you a good understanding on project status and problem to solve.

Nova use glance client to get image information for glance. Downloading image is handled by "download handlers". Glance is not used in downloading.

```
# stable/juno
# nova is using glanceclient to communicate to glance
nova.image.api.py::download()
    sesion.download()   # session = GlanceImageService(client=glance_client)
        image = self.show() # using glanceclient
        ... # download image chunks, not using glance
        data = open(dst_path, 'wb')
        for chunk in image_chunks:
            data.write(chunk)
```

Other references

  * [Nova workflow](https://www.openstack.org/assets/presentation-media/OSSummitAtlanta2014-NovaLibvirtKVM2.pdf)
  * [Vm boost with image workflow](https://lists.launchpad.net/openstack/msg08074.html)
  * [Glance introduction](http://blog.csdn.net/ganglia/article/details/11298261)
  * [Nova boot from volume](http://blog.csdn.net/juvxiao/article/details/22614663)

## Install and Config

I've tried using glance + swift without keystone. Later found out that glance can only get swift address from keystone endpoints. It doesn't even have a config option to fill in swift address alone. See [config](https://github.com/openstack/glance/blob/stable/juno/etc/glance-api.conf).

So in the end I decided to deploy glance alone using file stone. Following official developer [doc](http://docs.openstack.org/developer/glance/installing.html), and installation [manual](http://docs.openstack.org/icehouse/install-guide/install/apt/content/glance-install.html).

```
mkdir workspace
cd workspace/
git clone https://github.com/openstack/glance
cd glance
git checkout stable/juno
pip install -r requirements.txt
python setup.py install
cd ..
```

Create user for glance

```
useradd -r -s /sbin/nologin glance
```

Create necessary directories.

```
# remember to change to proper permission
mkdir /etc/glance
mkdir /var/lib/glance
mkdir /var/lib/glance/image-cache/
mkdir /var/lib/glance/images/
mkdir /var/lib/glance/scrubber
chown -R glance:glance /var/lib/glance
mkdir /var/log/glance
chown -R glance:glance /var/log/glance
mkdir /var/run/glance
chown -R glance:glance /var/run/glance

# copy config files
cp -r glance/etc/* /etc/glance/
```

For configuration files, refer to github source [etc](https://github.com/openstack/glance/tree/stable/juno/etc). Below is config file for `glance-api.conf`. Actually, I recommend copy the modify on official config files, rather than overwrite them like what I do now.

```
echo '
[DEFAULT]
debug = True
sql_connection = mysql://root:123work@localhost/glance
default_store = file
image_cache_dir = /var/lib/glance/image-cache/
log_file = /var/log/glance/api.log

[paste_deploy]
# here I dont use keystone
flavor =

[glance_store]
stores = glance.store.filesystem.Store
' > /etc/glance/glance-api.conf
```

Configuration file for `glance-registry.conf`

```
echo '
[DEFAULT]
debug = True
sql_connection = mysql://root:123work@localhost/glance 
default_store = file
log_file = /var/log/glance/registry.log

[paste_deploy]
# here I dont use keystone
flavor =
' > /etc/glance/glance-registry.conf
```

Need to create `glance` table in mysql

```
... # create table 'glance' in mysql, collation=utf8, and grant proper permission
glance-manage -v db_sync
```

## Start Service

```
su -s /bin/bash glance -c '/bin/glance-control glance-api start'
su -s /bin/bash glance -c '/bin/glance-control glance-registry start'

# to stop
#su -s /bin/bash glance -c '/bin/glance-control glance-registry stop'
#su -s /bin/bash glance -c '/bin/glance-control glance-api stop'
```

## Verify Operation

First, let's download the image.

```
mkdir /tmp/images
cd /tmp/images/
wget http://cdn.download.cirros-cloud.net/0.3.2/cirros-0.3.2-x86_64-disk.img
```

I have to avoid using glanceclient, becuase it force me to authenticate on keystone, which I don't have now. So I use curl.

```
# list images, I don't have auth on glance
curl -i -X GET http://127.0.0.1:9292/v1/images/detail

# send by base64 encode
base64 /root/cirros-0.3.2-x86_64-disk.img | curl http://127.0.0.1:9292/v1/images --trace - -i -X POST -H 'Content-Transfer-Encoding: base64' -H 'Content-Type: application/octet-stream' -H 'x-image-meta-name: cirros' -H 'x-image-meta-disk_format: qcow2' -H 'x-image-meta-container_format: bare' --data-binary @-

# using glance without keystone, I cannot create public image, nor can I list them detail. So, change image to public in db
mysql -uroot -p -e "use glance; update glance.images set is_public=1;"

# list images again
curl -i -X GET http://127.0.0.1:9292/v1/images/detail

# to retrieve image metadata
curl -i -X HEAD http://127.0.0.1:9292/v1/images/7253b5ab-00a1-4bac-9bd4-1c66364a4265

# to retrieve image metadata and image data
curl -i -X GET http://127.0.0.1:9292/v1/images/7253b5ab-00a1-4bac-9bd4-1c66364a4265
```

Show the image data stored. It is in different size of the original one, because of the encoding when upload.

```
# show glance stored image
$ ll /var/lib/glance/images/
-rw-r----- 1 glance glance 20450682 Nov 14 09:14 7253b5ab-00a1-4bac-9bd4-1c66364a4265

# show original image file
$ ll cirros-0.3.2-x86_64-disk.img
-rw-rw-rw- 1 root root 15138816 Nov  6 09:12 cirros-0.3.2-x86_64-disk.img
```

API References: 

  * [An example on maillist](https://lists.launchpad.net/openstack/msg17531.html)
  * [Glance API simle doc](http://docs.openstack.org/developer/glance/glanceapi.html)
  * [See usecase on testcases](https://github.com/openstack/glance/tree/master/glance/tests/functional)





