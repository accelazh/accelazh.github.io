---
layout: post
title: "Submit Code to Openstack Gerrit Using Https"
tagline : "Submit Code to Openstack Gerrit Using Https"
description: "Submit Code to Openstack Gerrit Using Https"
category: "openstack"
tags: [openstack, gerrit, ssh]
---
{% include JB/setup %}

Openstack `git review` submits code to gerrit server. The default transport is ssh. But in some corporate network, ssh may be blocked by firewall. We need to use https. Even though there is [developer doc](http://docs.openstack.org/infra/manual/developers.html), it doesn't seem to always work.

Note that on windows, the https way won'y work either, because its curl implementation here doesn't respect `realm`. In http digest authentication the `realm` is lost. See http://curl.haxx.se/mail/tracker-2015-02/0045.html.

```
# on windows git bash, 'realm' is lost, fail
curl -v -k --anyauth https://<username>:<http_password>@review.openstack.org/openstack/magnum/info/refs?service=git-receive-pack
...
> Authorization: Digest username="xxxxxx",realm="",nonce="wkHY1tNXPEe9ldPmV4CqHH0S2GaDpURG2fAovg==$",uri="/openstack/magnum/info/refs?service=git-receive-pack",cnonce="f3e532b77c27155408e3cc218c249062",nc=00000001,response="4dea580b6f275308621d7864a2ae35c9",qop="auth"
...
 
# on ubuntu, realm is preserved, success
curl -v -k --anyauth https://<username>:<http_password>@review.openstack.org/openstack/magnum/info/refs?service=git-receive-pack
...
> Authorization: Digest username="xxxxxx", realm="Gerrit Code Review", nonce="nIr/lo2fGz8uoqRa/3LsfS72zb7zIuj3eczK+Q==$", uri="/openstack/magnum/info/refs?service=git-receive-pack", cnonce="K2DlZGExGWQ1NDg5NmEyODAwND7mYWY4MDA3Y2UzZmM=", nc=00000001, qop=auth, response="b940fd5254c0b0d3e55fbdb737b3fec0"
...
```
 
So, steps here:
 
  1. Find an Ubuntu or CentOS, don't use Wnidows
  2. Generate your http password at Openstack gerrit.
  3. Change directory (cd)  to your project folder
  4. Fill in <username>, <http_password> and <project_name> (e.g. magnum), run below commands
```
git config gitreview.scheme https
git config gitreview.port 443
git remote rm gerrit
git remote add gerrit https://<username>:<http_password>@review.openstack.org/openstack/<project_name>
git review -s
```
  5. If it complains `scp <username>:<http_password>@review.openstack.org:hooks/commit-msg .git/hooks/commit-msg` failed. The file is used to generate ChangeId in commit message. Copy it from https://review.openstack.org/tools/hooks/commit-msg
  6. Now you should be able to `git review` to submit code. Have fun!

### Wrap It Up 

To summarize things up, I pasted full command line here
 
```
# find a linux machine, don’t use windows (because curl realm bug)
# clone the repo
cd ~/workspace/openstack
git clone https://github.com/openstack/cinder.git
cd cinder
 
# setup your username & email
git config user.name "<Your Name>"
git config user.email "<email@account.com>"
 
# install git review
yum install git-review
 
# setup gerrit to use http rather than ssh
git config gitreview.scheme https
git config gitreview.port 443
git remote rm gerrit
git remote add gerrit https://<username>:<http_password>@review.openstack.org/openstack/cinder
git review -s
 
# if you see "Problems encountered installing commit-msg hook"
# the following command failed with exit code 255
# "GET https://<username>:<http_password>@review.openstack.org/tools/hooks/commit-msg"
# just download it manually
wget -O .git/hooks/commit-msg https://review.openstack.org/tools/hooks/commit-msg
 
# start fixing bug
git checkout -b bug/1485897
vim …    # modify a bunch of code
git add …    # add them
git commit    # commit them. you need to write well formatted commit message. example: https://review.openstack.org/#/c/158713/
git review    # now your code is submitted. see it on review.openstack.org
```