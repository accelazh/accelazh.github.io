Orchestrating Highly Available Load Balancers with OpenStack Heat
http://www.hastexo.com/blogs/syed/2014/08/05/orchestrating-highly-available-load-balancers-openstack-heat

Team wiki is useful
http://wikicentral.cisco.com/display/GROUP/Heat

Template guide
http://docs.openstack.org/developer/heat/template_guide/hot_guide.html
Template spec
http://docs.openstack.org/developer/heat/template_guide/hot_spec.html#hot-spec-outputs
Openstack & tosca
https://wiki.openstack.org/w/images/a/a1/TOSCA_in_Heat_-_20130415.pdf
Resource plugin guide
http://docs.openstack.org/developer/heat/pluginguide.html

http://docs.openstack.org/developer/heat/template_guide/openstack.html

cloudify: why orchestration and heat
http://www.slideshare.net/uri1803/deployment-automation-on-openstack-with-tosca-and-cloudify-30914199
heat template (hot) vs tosca
http://www.slideshare.net/openstackil/heat-tosca


ValueError: AES key must be either 16, 24, or 32 bytes long
http://fosshelp.blogspot.com/2014/07/openstack-valueerror-aes-key-must-be.html
Go to "/etc/heat/heat.conf" and set "auth_encryption_key" with 32 char string, like auth_encryption_key=12345678912345678912345678912345

--

get_attr & properties: see heat/engine/resource/random_string.py
  properties_schema
  attributes_schema
  input_schema # just in software_deployment.py
  output_schema # just in software_deployment.py

http://docs.openstack.org/developer/heat/glossary.html also gives an explaination

--

existing resource types: http://docs.openstack.org/developer/heat/template_guide/openstack.html
custom resource: http://docs.openstack.org/developer/heat/pluginguide.html

--

      5. topology and (autoscaling) group
          1. resource group
             http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Heat::ResourceGroup
             https://github.com/openstack/heat-templates/blob/master/hot/resource_group/resource_group.yaml
          2. autoscaling group
             http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Heat::AutoScalingGroup

      6. deploy sequence
          1. https://github.com/openstack/heat-templates/blob/master/hot/software-config/example-templates/example-deploy-sequence.yaml

--

nohup /usr/bin/heat-engine --logfile /var/log/heat/engine.log &
nohup /usr/bin/heat-api --logfile /var/log/heat/api.log &

--

heat-api and heat-engine is stateless, HA by lb proxy
http://behindtheracks.com/2014/05/openstack-high-availability-heat-orchestration-service/

architecture:
  http://docs.openstack.org/developer/heat/architecture.html
  http://openstack.prov12n.com/openstack-heat-concepts-architecture-and-workflow/

--

Heat tripleO templat: a good place to learn
https://github.com/openstack/tripleo-heat-templates master branch, controller

--

heat_template_version: 2013-05-23
 
description: HOT template to deploy two servers to an existing Neutron network.
 
parameters:
  image:
    default: 148b4d44-e56d-4be1-86ed-e5005ae48c0d
    type: strin
    description: Name of image to use for servers
  flavor:
    default: m1.tiny
    type: string
    description: Flavor to use for servers
  net_id:
    default: 48a5949f-eca5-420d-9205-79cb96891348
    type: string
    description: ID of Neutron network into which servers get deployed
  subnet_id:
    default: 3268b6c6-201d-4f1c-baa5-f69fa63ca5ac
    type: string
    description: ID of Neutron sub network into which servers get deployed
 
resources:
  server1:
    type: OS::Nova::Server
    properties:
      name: Server1
      image: { get_param: image }
      flavor: { get_param: flavor }
      networks:
        - port: { get_resource: server1_port }
 
  server1_port:
    type: OS::Neutron::Port
    properties:
      network_id: { get_param: net_id }
      fixed_ips:
        - subnet_id: { get_param: subnet_id }
 
  server2:
    type: OS::Nova::Server
    properties:
      name: Server2
      image: { get_param: image }
      flavor: { get_param: flavor }
      networks:
        - port: { get_resource: server2_port }
 
  server2_port:
    type: OS::Neutron::Port
    properties:
      network_id: { get_param: net_id }
      fixed_ips:
        - subnet_id: { get_param: subnet_id }
 
outputs:
  server1_provider_ip:
    description: IP address of server1 in provider network
    value: { get_attr: [ server1, first_address ] }
  server2_provider_ip:
    description: IP address of server2 in provider network
    value: { get_attr: [ server2, first_address ] }

--

let's experiment with autoscaling + lb example
