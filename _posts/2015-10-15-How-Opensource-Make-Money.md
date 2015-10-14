---
layout: post
title: "How Opensource Make Money?"
tagline : "How Opensource Make Money?"
description: "How Opensource Make Money?"
category: "opensource"
tags: [opensource, business, startup]
---
{% include JB/setup %}

Opensource have dramatically reshaped how individuals play in the world the information technologies, how enterprises run their business internally and externally, and how startup companies can quickly grasp their technical stack on the fast train of internet.

The most interesting question related to opensource is how companies make money by it, i.e. the business model, since opensource are free to download. I want to have a list of them. But beware that there can always be new business models and new ways to make monkey by opensource, as long as more and more innovative startups emerge.

## Opensource Business Models

Here is the how-opensource-make-monkey list I've summarized.

### To Sell Complementary Products

Product A and product B are complementary if when people buy A, they would need B for it to work. This is very common when companies sell products. A strategy is to opensource A, making it free, but charge a fee for B. The growth of A gives more space for B. Also A has the chance to take the precedence in the market because it is free.

Examples are

  * Java vs IBM Weblogic
  * Openstack vs Intel x86 cores
  * Kubernetes (k8s) vs Google Cloud Engine (GCE)

### Publish the User Interface Layer

GCE uses k8s as their user interface layer. Google opensourced k8s, which is easy to use, free to get, powerful, and a new generation technology (dockerized PaaS). K8s tutorials always point to GCE. Quickly the benefits show up

  * With more and more people adopt k8s, k8s potentically become the canonical "how dockerize paas should look like". Then google defines dockerized PaaS.
  * More people become familiar with how to use GCE. K8s raises a very large potential user group and engineer labor for GCE.

### Opensource + Enterprise Version

A company can sell an opensource version + an enterprise version of its product. The former one is free but the latter one is charged. The enterprise one can add below to the opensource one

  * Ease of installation. More stable. Better deployment layout.
  * Professional support and warranty.
  * Integrated with enterprise-handy but community-less-care features like: auditing, monitoring, LDAP stuff enterprise user auth, configuration management, complex of dynamic XXX that only the complex company need, enterprise plugins, etc
  * Add some advanced component, only available for paied version

Many companies choose this business model. Examples are

  * Ceph vs Ceph Enterprise
  * Puppet vs Puppet Enterprise
  * Ansible vs Ansible Tower

This model also create a bridge from poor beginners to pay-money customers. A beginner startup may be poor, so it choose to use the free opensource version. When it grows up, it is very easy for the companies to become a paied customer.

### Distribution Vendor

Distribution vendor packages an opensource software, choose the right patch, right version, right deployment model, carry out a lot of testing, make it stable and easy to install. Complex opensource softwares, such as Openstack, which may consists of many components each of which need speciallized expertise, usually develop a market where a lot of distribution vendors live. Most of them, in the end, may be acquired by existing giant companies; some grow to be the new star.

Openstack market has quite a few distribution vendors selling packaged Openstack. Companies may choose to just sell a packaged Openstack, or integrate Openstack into their existing IT solutions for sale. For example

  * Mirantis
  * Piston cloud
  * Cloudscaling
  * Redhat Openstack
  * [IBM Cloud Manager](https://www.ibm.com/developerworks/servicemanagement/cvm/sce/)
  * [Intel Service Assurance](http://www.intel.com/content/www/us/en/software/intel-service-assurance-redapt-white-paper.html)
  * [Cisco Metapod](http://www.cisco.com/c/en/us/products/cloud-systems-management/metapod/index.html).

Mirantis is quite [special](https://www.mirantis.com/blog/mirantis-openstack-real-open-community-development/). It is pure opensource and owns no proprietary code. The value comes from their selection of more bug fixing, patches, security enhancements compared to community Openstack. They step further than the community, do real testing, and implement a good production-level deployment.

### To Offer Consulting & Management

Take Openstack market as an example. Openstack is complex to deploy and operate. The user also needs to following the community and upgrade. Given the difficulty of hosting an Openstack, companies step in and offer their consulting and management service. They can

  * Advise you what to choose and how to run it
  * Offer trainings
  * Outsource IT operation
  * Managed cloud: the asset is yours, I will manage the private cloud for you.

### Build My Public Cloud

Take Openstack as the example again. Companies such as [Cisco](https://www.telstra.com.au/business-enterprise/solutions/cloud-services/public-cloud/cisco-cloud-services) or [UnitedStack](https://www.ustack.com/) use Openstack to build their own public cloud. Openstack is free, but public cloud help them to earn money. However, it takes real effort to build from a free opensource version Openstack to an actual industry leading public cloud.

The public cloud can be sold in different ways

  * Complete open to all internet users, such as AWS
  * Only open to partner companies, so it'll has fewer but large customers. Such as Cisco's

### Advertising in Technology Peers

When we advertise a product, we use public media: TV, newpaper, video sites, printings, twitters, weibo, facebook, forums. But when we advertise a technology, we use opensource: github, papers, summits, blogs, meetups.

  * Technology people frequently look at opensource
  * Opensource stuff is definitely more attractive and persuasive to this group, i.e. the acceptance of the technology peer.
  * To opensource means to say, hey, everyone can sees my code, my code is bulletproof, you can trust the quality.
  * Public media is expensive. But opensource channels are almost free.

Examples are

  * OpenSSL: see how bulletproof I am
  * Ceph: use opensource to show the power and quality of a new emerging technology. Use opensource to promote. Frequently interactive with other opensource projects in the same ecosystem to build the integration. Frequently attend / host summits for more people to know.

### Stand in Alliance Against ...

Another perspective for Openstack is, traditional giant proprietary datacenter / IT vendors (IBM, Cisco, Intel, etc) try to stand in alliance against public cloud AWS, which quickly eats up the traditional IT market.

To stand in alliance, we need a platform to corporate, which should be transparent enough. Opensource is the best choice. When we want to build an industry standard, opensource is also the best choice. After years of developing, the standard emerges from global contribution and acceptance.

Examples

  * Openstack

### Disrupt the Industry and Take the Leadership

When a company gets a breaking-through technology, which is definitely more powerful, but is afraid of the conflict with the dominate existing one and the market acceptance. Opensource it. The market will be disrupted. Opensource can be proved and accepted by the technology peer first, then quickly explodes to market demand.

Opensource is a way for new technology to disrupt and prove itself. But to disrupt the industry is the first step. With market acceptance, the initial disruptor wins the de-factor industry leadership, which is highly advantageous and the biggest game.

Here are examples based on my understanding

  * Ceph: a new generation storage technology completely differs from traditonal proprietary storages. It takes opensource to promote.
  * Kubernetes: to make the industry quicker to accept containerized PaaS, google throw out kubernetes. When the market is convinced that contanierized PaaS is better, google already holds the leadership tight
  * Java: Sun, IBM, Oracle in aliance builds Java which reshapes the IT industry. Opensource helps Java to beat all the traditionals, win the world, and make Sun, IBM, Oracle the leaders. They define how company should build and run their IT.
  * Openstack: Companies like Redhat, Mirantis, HP, IBM are fighting for the leadship of Openstack community, by more contribution, more core developers and more PTL. When one leads how Openstack evolves, it ensures its own products always integrate better and step faster with Openstack than the competitors.
  * Google 3 papers: GFS, bigtable, MapReduce. Even if there are no selling products, and the community have adopted the design. The 3 papers totally reshaped our industry and the cloud technology, making everyone knows that google is the leader.









