---
layout: post
title: "Play with Kubernetes on CentOS 7"
tagline : "Play with Kubernetes on CentOS 7"
description: "Play with Kubernetes on CentOS 7"
category: "kubernetes"
tags: [kubernetes, container, paas]
---
{% include JB/setup %}

In this article I install a k8s cluster, try to setup all the services needed to host a real web service, then give a summarize.

## Install Kubernetes Master and Minions

To install Kubernetes, I followed [Severalnines' guide](http://www.severalnines.com/blog/installing-kubernetes-cluster-minions-centos7-manage-pods-services). Note that

  * The firewalld is turned off
  * Kubernetes package are installed by `yum`
  * I use Kubernetes release-1.0

I setup a 1 master 3 minion deployment. If you are using vmware/virtualbox, be sure to enable promiscuous mode on vswitch. I didn't implement HA. For HA deployment of Kubernetes, refer to [official HA guide](https://github.com/kubernetes/kubernetes/blob/release-1.0/docs/admin/high-availability.md). My k8s version below

```
$ kubectl version
Client Version: version.Info{Major:"1", Minor:"0+", GitVersion:"v1.0.0-290-gb2dafdaef5acea", GitCommit:"b2dafdaef5aceafad503ab56254b60f80da9e980", GitTreeState:"clean"}
Server Version: version.Info{Major:"1", Minor:"0+", GitVersion:"v1.0.0-290-gb2dafdaef5acea", GitCommit:"b2dafdaef5aceafad503ab56254b60f80da9e980", GitTreeState:"clean"}

$ uname -r
3.10.0-229.el7.x86_64
```

To start services on master node

```
$ for SERVICES in etcd kube-apiserver kube-controller-manager kube-scheduler; do 
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES 
done
```

To start services on minion nodes. Note that we need to launch `flanneld` earilier than `docker`, otherwise `docker` may not be using flannel network.

```
$ for SERVICES in kube-proxy kubelet flanneld docker; do     # Launch flannel earilier than docker
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES 
done
```

### Verify the Network

Basically, to let docker use flannel network, you need to add `--bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU}` to docker daemon startup options. But above installation will automatically do that for you.

```
source /var/run/flannel/subnet.env
docker -d --bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU}
```

Use `ps -ef|grep docker` to check docker daemon options. Systemd unit file you should be able to see docker requires flannel

```
ps -ef | grep docker
cat /etc/systemd/system/docker.service.requires/flanneld.service
```

Once flannel network is running, each container on each host should be using different IP. They should be able to ping each other ip address. Use below to launch temporary containers to test

```
docker run -d ubuntu:trusty /bin/bash -c "while true; do echo hello; sleep 10; done"
```

References: [\[1\]](http://www.slideshare.net/lorispack/using-coreos-flannel-for-docker-networking)[\[2\]](http://blog.shippable.com/docker-overlay-network-using-flannel)

### ServiceAccount Error

If you hit below error, take out `ServiceAccount` of `/etc/kubernetes/apiserver::KUBE_ADMISSION_CONTROL`. Just delete the `ServiceAccount`. ([issue 11222](https://github.com/kubernetes/kubernetes/issues/11222)). Then restart the master node.

```
$ kubectl create -f redis-master1.yaml
Error from server: error when creating "redis-master1.yaml": Pod "redis-master1" is forbidden: no API token found for service account default/default, retry after the token is automatically created and added to the service account
```

## Play with K8S

By setting up a series of common services on k8s, I try to figure out how to host a production level web site on k8s. There needs multinode databases, volumes, load balancing, caching (redis/memcached), dns and monitoring.

### Run Kubernetes Guestbook (Without GCE, without DNS)

I'm using kubernetes release-1.0. To run guestbook without GCE, without DNS, just on CentOS 7. Follow [official guide](https://github.com/kubernetes/kubernetes/tree/5adae4e4a35202abe1c130e32240d0461b3a1c36/examples/guestbook).

```
git clone https://github.com/kubernetes/kubernetes.git
cd kubernetes
git checkout 5adae4e4a35202abe1c130e32240d0461b3a1c36    # the version which I experimented with
```

Create redis master pods and services

```
kubectl create -f examples/guestbook/redis-master-controller.yaml
kubectl get pods -o wide --all-namespaces=true
kubectl create -f examples/guestbook/redis-master-service.yaml
```

Create redis slave

```
vim examples/guestbook/redis-slave-controller.yaml
...    # comment out 'value: dns', uncomment `value: env` under GET_HOSTS_FROM
kubectl create -f examples/guestbook/redis-slave-controller.yaml
kubectl create -f examples/guestbook/redis-slave-service.yaml
kubectl logs redis-slave-*    # should show successfully sync with master
```

Create frontend controller

```
vim examples/guestbook/frontend-controller.yaml
...    # comment out 'value: dns', uncomment `value: env` under GET_HOSTS_FROM
kubectl create -f examples/guestbook/frontend-controller.yaml
kubectl create -f examples/guestbook/frontend-service.yaml
```

To expose frontend-service externally, I use `NodePort`. See [publishing services](https://github.com/kubernetes/kubernetes/blob/5adae4e4a35202abe1c130e32240d0461b3a1c36/docs/user-guide/services.md#publishing-services---service-types)

```
vim examples/guestbook/frontend-services.yaml
...    # Write `type: NodePort` under `spec`.
kubectl delete service frontend
kubectl create -f examples/guestbook/frontend-service.yaml

# to see which port is mapped
kubectl describe service frontend | grep NodePort    # in my case the nodeport is 30363
```

After you [open firewall](https://github.com/kubernetes/kubernetes/blob/703130e8e4f3c704cfa598d70fbd2ea13e7bc14f/docs/user-guide/services-firewalls.md) or iptables, you should be able to access the web frontend from `http://<any-minion-ip>:<nodeport>`.

To checkout what have been saved in redis

```
# on a k8s minion
$ docker exec -it k8s_worker.8bef144a_redis-slave-usfge_default_88895109-57a2-11e5-9a9e-005056957d30_3156e0e8 /bin/bash
$ redis-cli keys \*
1) "messages"
$ redis-cli get messages
",hello world,123,456"
```

Or just get it from web browser by `http://<any-minion-ip>:<nodeport>/guestbook.php?cmd=get&key=messages`.

### Run Multinode Galera Mysql on Kubernetes

To run galera mysql on k8s, one solution is [Planet Mysql's](http://planet.mysql.com/entry/?id=5989823) (I think the blog content is a bit out-of-dated compared to its code repo). Checkout its [entrypoint.sh](https://github.com/CaptTofu/percona_xtradb_cluster_docker/blob/master/docker-entrypoint.sh). The key point is how each galera instance find the others' addresses. Planet Mysql's solution uses k8s service environment variable to locate the other hosts and write it to `gcomm://`. Each mysql galera instance comprise of a pod and a service.

Some solution that I can think of to help galera mysql instance to locate its peer, besides Planet Mysql's

  * Each mysql galera instance comprise of a pod and a service. We just hardcode the ip address in pod yaml. If one pod down, we manually fill in the latest ip adn launch a new instance.
  * We launch an etcd cluster on k8s, all galera mysql instance find peer info from etcd.

Anyway, I will use Planet Mysql's solution now. P.S. To host a mysql cluster, besides galera, there are also mysql sharding solutions on k8s, such as [Vitess Mysql](http://vitess.io/getting-started/) by youtube.

First, download the code base

```
git clone https://github.com/CaptTofu/mysql_replication_kubernetes.git
cd mysql_replication_kubernetes
git checkout f7c2bc4f411d6950ca575e804189114026b2ba69     # the version I experimented with
cd galera_sync_replication
```

I think we should set all `WSREP_CLUSTER_ADDRESS` to `gcomm://` in each pxc-nodeN, according to the container image's [entrypoint.sh](https://github.com/CaptTofu/percona_xtradb_cluster_docker/blob/master/docker-entrypoint.sh).

```
vim pxc-node1.yaml
...    # change variable WSREP_CLUSTER_ADDRESS to gcomm://
vim pxc-node2.yaml
...    # same as above
vim pxc-node3.yaml
...    # same as above
```

Next we launch galera mysql instances one by one

```
kubectl create -f pxc-node1.yaml
kubectl create -f pxc-node1-service.yaml
```

Wait the first galera mysql instance is running. Than launch below. This is because galera mysql needs at least one instance running to form the cluster.

```
kubectl create -f pxc-node2.yaml
kubectl create -f pxc-node2-service.yaml
kubectl create -f pxc-node3.yaml
kubectl create -f pxc-node3-service.yaml
```

To verify correctness. See [galera mysql status guide](http://galeracluster.com/documentation-webpages/monitoringthecluster.html).

```
# check the pod log
kubectl logs pxc-node3

# check galera mysql status
kubectl get pods -o wide
docker exec -it 98d568b88aac  /bin/bash
mysql -uroot -p
mysql> SHOW GLOBAL STATUS LIKE 'wsrep_%';    # You should be able to see cluster_size = 3

# write something to mysql and check the other node reading it
...
```

I think k8s service design may not be really appropriate for p2p clusters like galera mysql, redis, memcached etc. Because

  * In the cluster, e.g. galera mysql, why should I be forced to couple a service for each of the instance?
  * If an app wants to use service provided by those kind of cluster, e.g. memcached, it needs to know every ip/hostname of them, because the consistent hashing, load balancing and failover are performed on the app side. It is hard to just hide the cluster under one service, which exposes one ip.

So I think the more appropriate way is to provide those services, such as mysql, redis and memcached, from the outside of k8s. Stateless web apps, however, are more appropriate to run on k8s.

### Debugger Pod

Sometime I need a simple pod to debug and test network connectivity to other pods. Here's my pod yaml.

```
debugvm.yaml
apiVersion: v1
kind: Pod
metadata:
  name: debugvm
  labels:
    name: debugvm
spec:
  containers:
    - name: debugvm
      image: ubuntu:trusty
      command: [ "bin/bash", "-c", "while true; do echo 'hello world'; sleep 60; done" ]
```

Once launched in k8s, login to debugvm and use nc to test network connectivity to other pods

```
docker exec -it k8s_debugvm.* /bin/bash
nc <host> <port>
```

### Run Multinode Redis for Memory Caching on Kubernetes

It is popular for web apps to use a cluster of Redis or Memcached as in-memory caching. I launch a 3-node redis cluster. Each redis has no idea of its peer. Each redis instance comprises of a pod and a service. Here's redis instance 1

```
# the redis-master1.yaml
apiVersion: v1
kind: Pod
metadata:
  name: redis-master1
  labels:
    name: redis-master1
spec:
  containers:
  - name: redis-master1
    image: redis
    ports:
    - containerPort: 6379

# the redis-master1-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-master1
  labels:
    name: redis-master1
spec:
  ports:
  # the default redis serving port
  - port: 6379
    targetPort: 6379
  selector:
    name: redis-master1
  type: NodePort
```

For redis instance 2 and 3, just change the `1` to `2` or `3` above. The web app, to use the 3 redis instances as the caching cluster, needs to perform consistent hashing itself and select which redis instance to access. If you use PHP, lib [Predis](https://github.com/nrk/predis#cluster) can do this.

Why I need to attach a k8s service to each redis instance? The client needs to know each IP of redis instances and perform consistent hashing. However one k8s service just expose on IP. For a cluster which needs client-side sharding / load balancing / failover or whatever client-side staff, client-side needs to know more IPs. The default k8s service model doesn't fit that well.

### Setup DNS for Kubernetes

Kuberetes can use dns services for its service discovery. See [official doc](https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/dns). DNS is a k8s [addon](https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/dns). I followed this [guide](http://www.dasblinkenlichten.com/kubernetes-dns-config-on-bare-metal/) to setup dns. The `cluster_dns` address should be in range specified in /etc/kubernetes/apiserver KUBE_SERVICE_ADDRESSES.

```
# on each kubelet server

# add '--cluster_dns=10.254.0.10 --cluster_domain=cluster.local' to KUBELET_ARGS
vim /etc/kubernetes/kubelet

# restate kubelet
systemctl daemon-reload
systemctl restart kubelet
```

Launch the dns service, below is the manifest. Copied and edited from [k8s repo](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/dns/skydns-svc.yaml.in).

```
apiVersion: v1
kind: Service
metadata:
  name: kube-dns
  namespace: default
  labels:
    k8s-app: kube-dns
    kubernetes.io/cluster-service: "true"
    kubernetes.io/name: "KubeDNS"
spec:
  selector:
    k8s-app: kube-dns
  clusterIP: 10.254.0.10
  ports:
  - name: dns
    port: 53
    protocol: UDP
  - name: dns-tcp
    port: 53
    protocol: TCP
```

Launch the dns pods, below is the manifest. I have tried several different manifests before setting it up.

This one was copied and edited from [here](http://www.dasblinkenlichten.com/kubernetes-dns-config-on-bare-metal/). Don't use it. It has issue [12534](https://github.com/kubernetes/kubernetes/issues/12534).

```
apiVersion: v1
kind: ReplicationController
metadata:
    name: kube-dns
    namespace: default
    labels:
      k8s-app: kube-dns
      kubernetes.io/cluster-service: "true"
spec:
    replicas: 1
    selector:
        k8s-app: kube-dns
    template:
        metadata:
            labels:
                k8s-app: kube-dns
                kubernetes.io/cluster-service: "true"
        spec:
            dnsPolicy: "Default"  # Don't use cluster DNS.
            containers:
              - name: etcd
                image: quay.io/coreos/etcd:latest
                command: [
                        "/etcd",
                        "--listen-client-urls",
                        "http://127.0.0.1:2379,http://127.0.0.1:4001",
                        "--advertise-client-urls",
                        "http://127.0.0.1:2379,http://127.0.0.1:4001",
                ]
              - name: kube2sky
                image: gcr.io/google_containers/kube2sky:1.11
                args: [
                        # entrypoint = "/kube2sky",
                        "-domain=cluster.local",
                ]
              - name: skydns
                image: kubernetes/skydns:2014-12-23-001
                args: [
                        # entrypoint = "/skydns",
                        "-machines=http://localhost:4001",
                        "-addr=0.0.0.0:53",
                        "-domain=cluster.local",
                ]
                ports:
                  - name: dns
                    containerPort: 53
                    protocol: UDP
```

This one was copied and editted from [k8s repo](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/dns/skydns-rc.yaml.in) version. It has the same issue [12534](https://github.com/kubernetes/kubernetes/issues/12534).

```
apiVersion: v1
kind: ReplicationController
metadata:
  name: kube-dns-v9
  namespace: default
  labels:
    k8s-app: kube-dns
    version: v9
    kubernetes.io/cluster-service: "true"
spec:
  replicas: 1
  selector:
    k8s-app: kube-dns
    version: v9
  template:
    metadata:
      labels:
        k8s-app: kube-dns
        version: v9
        kubernetes.io/cluster-service: "true"
    spec:
      containers:
      - name: etcd
        image: gcr.io/google_containers/etcd:2.0.9
        resources:
          limits:
            cpu: 100m
            memory: 50Mi
        command:
        - /usr/local/bin/etcd
        - -data-dir
        - /var/etcd/data
        - -listen-client-urls
        - http://127.0.0.1:2379,http://127.0.0.1:4001
        - -advertise-client-urls
        - http://127.0.0.1:2379,http://127.0.0.1:4001
        - -initial-cluster-token
        - skydns-etcd
        volumeMounts:
        - name: etcd-storage
          mountPath: /var/etcd/data
      - name: kube2sky
        image: gcr.io/google_containers/kube2sky:1.11
        resources:
          limits:
            cpu: 100m
            memory: 50Mi
        args:
        # command = "/kube2sky"
        - -domain=cluster.local
      - name: skydns
        image: gcr.io/google_containers/skydns:2015-03-11-001
        resources:
          limits:
            cpu: 100m
            memory: 50Mi
        args:
        # command = "/skydns"
        - -machines=http://localhost:4001
        - -addr=0.0.0.0:53
        - -domain=cluster.local.
        ports:
        - containerPort: 53
          name: dns
          protocol: UDP
        - containerPort: 53
          name: dns-tcp
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 1
          timeoutSeconds: 5
      - name: healthz
        image: gcr.io/google_containers/exechealthz:1.0
        resources:
          limits:
            cpu: 10m
            memory: 20Mi
        args:
        - -cmd=nslookup kubernetes.default.svc.cluster.local localhost >/dev/null
        - -port=8080
        ports:
        - containerPort: 8080
          protocol: TCP
      volumes:
      - name: etcd-storage
        emptyDir: {}
      dnsPolicy: Default  # Don't use cluster DNS.
```

After studied the solution provide by [guybrush's](https://github.com/guybrush/kubernetes/commit/e6070a7179e7ef69387e4f9851b9648aa23f1518). I pieced together the one works. The key is the missing command option, `-kube_master_url=http://<your-master-host-ip>:8080`, which prevents kube2sky from accessing kubernetes master node, and raise errors in [12534](https://github.com/kubernetes/kubernetes/issues/12534). Simple.

```
apiVersion: v1
kind: ReplicationController
metadata:
  name: kube-dns-v9
  namespace: default
  labels:
    k8s-app: kube-dns
    version: v9
    kubernetes.io/cluster-service: "true"
spec:
  replicas: 1
  selector:
    k8s-app: kube-dns
    version: v9
  template:
    metadata:
      labels:
        k8s-app: kube-dns
        version: v9
        kubernetes.io/cluster-service: "true"
    spec:
      containers:
      - name: etcd
        image: gcr.io/google_containers/etcd:2.0.9
        resources:
          limits:
            cpu: 100m
            memory: 50Mi
        command:
        - /usr/local/bin/etcd
        - -data-dir
        - /var/etcd/data
        - -listen-client-urls
        - http://127.0.0.1:2379,http://127.0.0.1:4001
        - -advertise-client-urls
        - http://127.0.0.1:2379,http://127.0.0.1:4001
        - -initial-cluster-token
        - skydns-etcd
        volumeMounts:
        - name: etcd-storage
          mountPath: /var/etcd/data
      - name: kube2sky
        image: gcr.io/google_containers/kube2sky:1.11
        resources:
          limits:
            cpu: 100m
            memory: 50Mi
        args:
        # command = "/kube2sky"
        - -kube_master_url=http://10.62.98.245:8080
        - -domain=cluster.local
      - name: skydns
        image: gcr.io/google_containers/skydns:2015-03-11-001
        resources:
          limits:
            cpu: 100m
            memory: 50Mi
        args:
        # command = "/skydns"
        - -machines=http://localhost:4001
        - -addr=0.0.0.0:53
        - -domain=cluster.local.
        ports:
        - containerPort: 53
          name: dns
          protocol: UDP
        - containerPort: 53
          name: dns-tcp
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /healthz
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 1
          timeoutSeconds: 5
      - name: healthz
        image: gcr.io/google_containers/exechealthz:1.0
        resources:
          limits:
            cpu: 10m
            memory: 20Mi
        args:
        - -cmd=nslookup kubernetes.default.svc.cluster.local localhost >/dev/null
        - -port=8080
        ports:
        - containerPort: 8080
          protocol: TCP
      volumes:
      - name: etcd-storage
        emptyDir: {}
      dnsPolicy: Default  # Don't use cluster DNS.
```

To verify whether dns works, I followed this [guide](https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/dns#how-do-i-test-if-it-is-working). First you check each pod logs to verify. But if you can ignore this error

```
skydns: falling back to default configuration, could not read from etcd: 100: Key not found (/skydns) [2]
```

After that, create a busybox pod

```
# busybox.yaml
apiVersion: v1
kind: Pod
metadata:
  name: busybox
  namespace: default
spec:
  containers:
  - image: busybox
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
    name: busybox
  restartPolicy: Always
```

After the pod is running, run below command you should see

```
$ kubectl exec busybox -- nslookup kubernetes
Server:    10.254.0.10
Address 1: 10.254.0.10

Name:      kubernetes
Address 1: 10.254.0.1

$ kubectl exec busybox -- nslookup kubernetes.default.svc.cluster.local
Server:    10.254.0.10
Address 1: 10.254.0.10

Name:      kubernetes.default.svc.cluster.local
Address 1: 10.254.0.1
```

### Run Heapster to Monitor Kubernetes Pods

I follow [official guide](https://github.com/kubernetes/heapster/blob/master/docs/influxdb.md) to set Heapster up.

```
git clone https://github.com/kubernetes/heapster.git
kubectl create -f deploy/kube-config/influxdb/
```

If you hit below error

```
Error from server: error when creating "deploy/kube-config/influxdb/grafana-service.json": Service "monitoring-grafana" is forbidden: Namespace kube-system does not exist
Error from server: error when creating "deploy/kube-config/influxdb/heapster-controller.json": ReplicationController "heapster" is forbidden: Namespace kube-system does not exist
Error from server: error when creating "deploy/kube-config/influxdb/heapster-service.json": Service "heapster" is forbidden: Namespace kube-system does not exist
Error from server: error when creating "deploy/kube-config/influxdb/influxdb-grafana-controller.json": ReplicationController "infludb-grafana" is forbidden: Namespace kube-system does not exist
Error from server: error when creating "deploy/kube-config/influxdb/influxdb-service.json": Service "monitoring-influxdb" is forbidden: Namespace kube-system does not exist
```

This is because your k8s doesn't have `kube-system` namespace. [Solution](https://github.com/kubernetes/heapster/issues/452) is to change all `kube-system` to `default` in each manifests.

Heapster relies on k8s dns to work. You have to enable dns in k8s before start to install Heapster. Similar issue found [here](https://github.com/kubernetes/heapster/issues/277).

If you check heapster pod logs and found heapster keeps crash by below error

```
$ kubectl logs heapster-yrh5i
...
open /var/run/secrets/kubernetes.io/serviceaccount/token: no such file or directory
```

The issue is that heapster is missing serviceaccount to access apiserver. Refer to this [guide](https://github.com/kubernetes/heapster/blob/master/docs/source-configuration.md). My solution is to "use a heapster-only serviceaccount". First, run below to create the serviceaccount

```
cat <EOF | kubectl create -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: heapster
EOF
```

After that, need to add `serviceAccount: "heapster"` and `--source=kubernetes:http://kubernetes-ro?inClusterConfig=false&useServiceAccount=true&auth=` in spec.

```
"spec": {
    "serviceAccount": "heapster",
    "containers": [
        {
            "image": "kubernetes/heapster:v0.18.0",
            "name": "heapster",
            "command": [
                "/heapster",
                "--source=kubernetes:http://kubernetes-ro?inClusterConfig=false&useServiceAccount=true&auth=",
                "--sink=influxdb:http://monitoring-influxdb:8086"
            ]
        }
    ]
}
```

If you meet below error

```
$ kubectl logs heapster-yrh5i
...
Failed to list *api.Node: Get http://kubernetes-ro/api/v1/nodes: dial tcp: lookup kubernetes-ro: no such host
Failed to list *api.Namespace: Get http://kubernetes-ro/api/v1/namespaces: dial tcp: lookup kubernetes-ro: no such host
Failed to list *api.Pod: Get http://kubernetes-ro/api/v1/pods?fieldSelector=spec.nodeName%21%3D: dial tcp: lookup kubernetes-ro: no such host
```

This is because the above `kubernetes-ro` is not dns resolvable. try `kubectl exec busybox -- nslookup kubernetes-ro` to verify. This [thread](https://github.com/kubernetes/kubernetes/issues/4567) indicates that `kubernetes-ro` is deprecated. So change it to `<kubeneters-master-ip>:8080` (I wish I could avoid hardcoded ip).

```
{
    "apiVersion": "v1",
    "kind": "ReplicationController",
    "metadata": {
        "labels": {
            "k8s-app" : "heapster",
            "name": "heapster",
            "version": "v6"
        },
        "name": "heapster",
        "namespace": "default"
    },
    "spec": {
        "replicas": 1,
        "selector": {
            "k8s-app": "heapster",
            "version": "v6"
        },
        "template": {
            "metadata": {
                "labels": {
                    "k8s-app": "heapster",
                    "version": "v6"
                }
            },
            "spec": {
                "serviceAccount": "heapster",
                "containers": [
                    {
                        "image": "kubernetes/heapster:v0.18.0",
                        "name": "heapster",
                        "command": [
                            "/heapster",
                            "--source=kubernetes:http://10.62.98.245:8080?inClusterConfig=false&useServiceAccount=true&auth=",
                            "--sink=influxdb:http://monitoring-influxdb:8086",
                            "-v=20"
                        ]
                    }
                ]
            }
        }
    }
}
```

Next, I need to change each service manifest. Change the service type to 'NodePort'. So that without GCD load balancer, I can still access them from outside. Restart all services.

```
"spec": {
        "type": "NodePort",
```

Access Grafana by the external NodePort mapping. Username and password is admin:admin. After you login Grafana, add a data source of type `InfluxDB 0.8.x`, url `http://monitoring-influxdb:8086`, database name 'k8s', database user name and password is root:root.

If you meet below error, heapster cannot resolve monitoring-influxdb, but busybox still can. That's weird.

```
$ kubectl logs heapster -k30m4
...
failed to sync data to sinks - encountered the following errors: Post http://monitoring-influxdb:8086/db/k8s/series?u=root&p=root&time_precision=s: dial tcp: lookup monitoring-influxdb: no such host ;
Post http://monitoring-influxdb:8086/db/k8s/series?u=root&p=root&time_precision=m: dial tcp: lookup monitoring-influxdb: no such host

# try troubleshooting. why busybox can resolve dns, but heapster cannot?
$ kubectl exec heapster-k30m4 -- nslookup monitoring-influxdb
Server:    (null)
nslookup: can't resolve 'monitoring-influxdb': Try again
Address 1: ::1 localhost
Address 2: 127.0.0.1 localhost

$ kubectl exec busybox -- nslookup monitoring-influxdb
Server:    10.254.0.10
Address 1: 10.254.0.10

Name:      monitoring-influxdb
Address 1: 10.254.113.143

$ kubectl exec heapster-k30m4 -- nslookup monitoring-influxdb 10.254.0.10
Server:    10.254.0.10
Address 1: 10.254.0.10

nslookup: can't resolve 'monitoring-influxdb': Try again

$ kubectl exec busybox -- nslookup monitoring-influxdb 10.254.0.10
Server:    10.254.0.10
Address 1: 10.254.0.10

Name:      monitoring-influxdb
Address 1: 10.254.113.143

# check skydns log, found
$ kubectl logs kube-dns-v9-f9j9m skydns
...
skydns: can not forward, name too short (less than 2 labels): `monitoring-influxdb.'
```

I didn't found the cause and solution. But there is a walkaround, let's write hostname directly to /etc/hosts.

```
kubectl exec heapster-fk6xo -- /bin/sh -c 'echo ${MONITORING_INFLUXDB_SERVICE_HOST} monitoring-influxdb >> /etc/hosts'
kubectl exec infludb-grafana-9wosh -- /bin/sh -c 'echo ${MONITORING_INFLUXDB_SERVICE_HOST} monitoring-influxdb >> /etc/hosts'
```

Now if you check heapster log, it should be working. Let's get back to Grafana to setup the dashboard, following this [guide](http://wahlnetwork.com/2015/04/29/building-a-dashboard-with-grafana-influxdb-and-powercli/). Example queries [here](https://gowalker.org/github.com/arkadijs/heapster) but quite outdated. Some queries that can work on the influxdb are

```
select derivative(value/1000000) from "cpu/usage_ns_cumulative" where $timeFilter and container_name = 'pxc-node1' group by time($interval) order asc
select mean(value/1024/1024) from "memory/usage_bytes_gauge" where $timeFilter and container_name = 'pxc-node1' group by time($interval) order asc
```

Tips on how to use influxdb (on its web portal)
  * The root:root is cluster admin. Create a database user (admin permission) and login with it before you access database.
  * Don't set database user to be of the same name with cluster admin. Otherwise strange permission will occur. (Gosh this takes me greate time to troubleshoot)
  * User `list series` to see what tables we have
  * Series name with special chars, e.g. `cpu/limit_gauge`, should be wrapped in quotes, like `select * "cpu/limit_gauge" limit 10`
  * Field name in `where` clause should be wrapped in single quotes, e.g. `where container_name = 'pxc-node1'`

By the time I setup Heapster, container network io metrics cannot be collected (always zero)
  * Know [issue](https://github.com/kubernetes/heapster/issues/500) pending fix. On centos `docker stats <container-id>` can neither catch network io.

Disk io metrics cannot be collected in Heapster either
  * Know [issue](https://github.com/kubernetes/heapster/issues/95). Heapster currrently doesn't pull disk io.
  * Raw disk IO can be retrieved by querying kubelet stats api, e.g. `curl 'http://<kubelet-ip>:10255/stats/default/pxc-node2/e2cf51fc-586e-11e5-9a9e-005056957d30/pxc-node2' | python -m json.tool`. The id number in that url can be found in `docker ps` container name.
  * Another way is to query docker daemon socket, e.g. `echo -e "GET /containers/<container-id>/stats HTTP/1.1\r\n" | nc -U /var/run/docker.sock | grep -e "^[[:space:]]*{.*}"`. See this [article](http://blog.scoutapp.com/articles/2015/06/22/monitoring-docker-containers-from-scratch).
  * To understand what the diskio metrics mean, note that disk partition is named with Major:Minor number (`lsblk` to see). See [here](http://unix.stackexchange.com/questions/124225/are-the-major-minor-number-unique).

### Run Docker Registry

A docker registry is needed if you want to build your own images and run them on k8s. I launched the docker registry on my master node, just one line of code, refer to the [official guide](https://docs.docker.com/registry/).

```
docker run -d -p 5000:5000 --name registry registry:2
```

The docker registry should be running now. To allow `dockerd` to use our "insecure" docker registry, we need to add `--insecure-registry <docker-registry>:5000` to /etc/sysconfig/docker::OPTIONS on each node. Restart `dockerd` then.

### Enable Ceph for K8S Volume

Ceph provides persistent volume service for k8s. I will next enable k8s to use ceph as volume backend.

#### Install Ceph

I fetched a new centos7 VM to install a 1-node ceph on it. First, make sure 

  * Kubernetes master node and the ceph node can ssh each other without key
  * Kubernetes master node can resolve the hostname of the ceph node
  * The `ceph-deploy` tool should be run on a separate node from where you install ceph

Install the `ceph-deploy` tool

```
# on kube master node
yum install -y ceph-deploy
mkdir -p ~/workspace/ceph/
cd ~/workspace/ceph
```

Install and launch ceph on the ceph node. Following the [official tutorial](http://docs.ceph.com/docs/master/start/quick-ceph-deploy/)

```
# on kube master node
# clean old installation
ceph-deploy purgedata <ceph-node>
ceph-deploy forgetkeys
#ceph-deploy purge    # to purge the ceph packages too

# install ceph
ceph-deploy install <ceph-node>

# create the cluster
ceph-deploy new <ceph-node>

# change ceph config
vim ./ceph.conf
...    # add `osd pool default size = 1`

# launch monitor
ceph-deploy mon create-initial

# launch osd
ceph-deploy disk list <ceph-node>
ceph-deploy osd prepare <ceph-node>:sdb
ceph-deploy osd activate <ceph-node>:/dev/sdb1

# push admin keys to the ceph node so that I can login without specifying monitor address and key file
ceph-deploy admin <ceph-node>
```

Verify ceph healthy status.

```
# on the ceph node
# test ceph healthy status
ceph health
ceph pg dump

# test ceph read write
ceph osd pool create data 128
echo hello world $(date) > test.txt
rados put test test.txt --pool data
rados get test test.txt.out --pool data
cat test.txt.out
```

Next, on each k8s node enable ceph `rbd` client

```
# on kube master node
# install ceph so that `rbd` is installed
ceph-deploy install 127.0.0.1 <kubelet1-ip> <kubelet2-ip> <kubelet3-ip>

# copy ceph admin keys to each node
cd ~/workspace/ceph
ceph-deploy admin 127.0.0.1 <kubelet1-ip> <kubelet2-ip> <kubelet3-ip>
```

To verify rbd is working

```
# on a randomly picked up k8s node
rbd create foo --size 1024
modprobe rbd
rbd map foo

mkfs.ext4 -m0 /dev/rbd/rbd/foo
mkdir /mnt/test-ceph-block-device
mount /dev/rbd/rbd/foo /mnt/test-ceph-block-device
cd /mnt/test-ceph-block-device
echo hello world $(date) > test.txt
cd ..
umount /dev/rbd/rbd/foo

# on another k8s node
modprobe rbd
rbd map foo
mkdir /mnt/test-ceph-block-device
mount /dev/rbd/rbd/foo /mnt/test-ceph-block-device
cd /mnt/test-ceph-block-device
cat test.txt    # here should print what we `echo` before
cd ..
umount /dev/rbd/rbd/foo
```

#### Enable Ceph in K8S

Following the [official guide](http://kubernetes.io/v1.0/examples/rbd/README.html). First make sure you have `/etc/ceph/ceph.client.admin.keyring` on every k8s node, os that k8s can authenticate to ceph.

We need to create the volume `vol1` and mkfs it before k8s can use.

```
# on kube master node
rbd create vol1 --size 1024 --pool data
mkfs.ext4 -m0 /dev/rbd/data/vol1
rbd unmap /dev/rbd/data/vol1
```

Next, we create a busybox pod which mounts the volume. The pod manifest is as follows. Start it by `kubectl create -f busyboxv.yaml`

```
# busyboxv.yaml
apiVersion: v1
kind: Pod
metadata:
  name: busyboxv
  namespace: default
spec:
  containers:
  - image: busybox
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
    name: busyboxv
    volumeMounts: 
      - mountPath: /mnt/rbd
        name: rbdpd
  volumes:
      - name: rbdpd
        rbd: 
          monitors: 
            - <ceph-node>:6789
          pool: data
          image: vol1
          user: admin
          keyring: /etc/ceph/ceph.client.admin.keyring
          fsType: ext4
          readOnly: false
  restartPolicy: Always
```

We write some file inside the busyboxv pod volume

```
# on kube master node
kubectl exec busyboxv -- sh -c 'echo hello world $(date) > /mnt/rbd/hello.txt'
kubectl exec busyboxv -- sh -c 'cat /mnt/rbd/hello.txt'
```

Next, kill the pod. Test whether the data in the volume persists

```
# on kube master node
kubectl delete pod busyboxv
sleep 5
rbd map vol1 --pool data
mkdir -p /mnt/rbd/data/vol1
mount /dev/rbd/data/vol1 /mnt/rbd/data/vol1
cat /mnt/rbd/data/vol1/hello.txt
umount /dev/rbd/data/vol1
rbd unmap /dev/rbd/data/vol1
```

So the k8s pod can use ceph volumes this way. We have persistent data storage now.

## Thinking of K8S Drawbacks

Kubernetes looks fancy and easy at the first glance. But during my experience these days, I found there many key features missing on k8s if you want to setup a complete web service, especially when you don't run it on GCE (Google Cloud Engine):

  * What if I want to use an external or custom load balancer, such as HAProxy? Openstack has LBaaS. But I wish to see it in k8s. K8s service does something of load balancing but it is not a full-featured load balancer. When you run k8s on GCE, GCE gives you external load balancer. But if you run k8s yourself, you don't have it. By searching on google I found people already start to build their own LB for k8s.

  * Many people run k8s on virtual machines. The VM overlay network and flannel overlay network, overlay the actual traffic twice. This results in performance degradation. Openstack Kuryr is trying to solve this problem. By that time, running k8s on Magnum would definitely be an advantage.

  * Multi-tenancy requires network separation. By k8s network model, if you use flannel, it actually connects every container as if they are in the same network. This is not acceptable for enterprise security. Openstack Neutron, however, allows user to create multiple at least L3 separated networks and connect them by routers.

  * The classic k8s services model hides a group of pods behind a service, and expose one IP to its user. But many real-life services actually don't fit into that model. Examples below. A solution for this is to use headless service. See[\[1\]](http://kubernetes.io/v1.0/docs/user-guide/services.html#headless-services)[\[2\]](https://github.com/kubernetes/kubernetes/issues/1607). However, users still need to implement their own service discovery, and perform IP registration. It is not really automated.

    * Memcached or Redis as the caching cluster. The client performs consistent hashing and decide which Memcached or Redis instance to access. The client needs to know IP of each instance. If you hide the whole Memcached or Redis cluster under one service, it would be not possible. One walkaround is to attach each instance to a service.

    * Mysql Galera cluster. In a similar way, the client needs to know each IP of the mysql instance, so that it can failover when one instance is down. In the k8s service model, if you hide the whole Mysql Galera cluster under one service (also on IP), it would not be possible.