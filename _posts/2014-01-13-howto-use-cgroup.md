---
layout: post
title: "how to use cgroup"
tagline : "Cgroup 用法"
description: "how to use cgroup"
category: "DevOps"
tags: ["cgroup"]
---
{% include JB/setup %}

介绍docker的的过程中，提到lxc利用cgroup来提供资源的限额和控制，本文主要介绍cgroup的用法和操作命令，主要内容来自

[1]<https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Resource_Management_Guide/ch01.html>

[2]<https://www.kernel.org/doc/Documentation/cgroups/cgroups.txt>

##cgroup

cgroup的功能在于将一台计算机上的资源(CPU,memory, network)进行分片，来防止*进程*间不利的资源抢占。

**Terminology**

* __cgroup__ - 关联一组task和一组subsystem的_配置参数_。一个task对应一个进程, cgroup是资源分片的最小单位。
* __subsystem__ - 资源管理器，一个subsystem对应一项资源的管理，如 cpu, cpuset, memory等
* __hierarchy__ - 关联一个到多个`subsystem`和一组树形结构的`cgroup`. 和`cgroup`不同，`hierarchy`包含的是可管理的`subsystem`而非具体参数

由此可见，cgroup对资源的管理是一个树形结构，类似进程。

相同点 - 分层结构，子进程/cgroup继承父进程/cgroup

不同点 - 进程是一个单根树状结构(pid=0为根)，而cgroup整体来看是一个多树的森林结构(hierarchy为根)。

一个典型的`hierarchy`挂载目录如下

    /cgroup/
    ├── blkio                           <--------------- hierarchy/root cgroup                   
    │   ├── blkio.io_merged             <--------------- subsystem parameter
    ... ...
    │   ├── blkio.weight
    │   ├── blkio.weight_device
    │   ├── cgroup.event_control
    │   ├── cgroup.procs
    │   ├── lxc                         <--------------- cgroup
    │   │   ├── blkio.io_merged         <--------------- subsystem parameter
    │   │   ├── blkio.io_queued
    ... ... ...
    │   │   └── tasks                   <--------------- task list
    │   ├── notify_on_release
    │   ├── release_agent
    │   └── tasks
    ...

**subsystem列表**

RHEL/centos支持的subsystem如下

  * blkio — 块存储配额 >> this subsystem sets limits on input/output access to and from block devices such as physical drives (disk, solid state, USB, etc.). 
  * cpu — CPU时间分配限制 >> this subsystem uses the scheduler to provide cgroup tasks access to the CPU.
  * cpuacct — CPU资源报告 >> this subsystem generates automatic reports on CPU resources used by tasks in a cgroup.
  * cpuset — CPU绑定限制 >> this subsystem assigns individual CPUs (on a multicore system) and memory nodes to tasks in a cgroup.
  * devices — 设备权限限制 >> this subsystem allows or denies access to devices by tasks in a cgroup.
  * freezer — cgroup停止/恢复 >> this subsystem suspends or resumes tasks in a cgroup.
  * memory — 内存限制 >> this subsystem sets limits on memory use by tasks in a cgroup, and generates automatic reports on memory resources used by those tasks.
  * net_cls — 配合tc进行网络限制 >> this subsystem tags network packets with a class identifier (classid) that allows the Linux traffic controller (tc) to identify packets originating from a particular cgroup task.
  * net_prio — 网络设备优先级 >> this subsystem provides a way to dynamically set the priority of network traffic per network interface.
  * ns — 资源命名空间限制 >> the namespace subsystem.

##cgroup操作准则与方法

### 操作准则

#### 1.一个hierarchy可以有多个 subsystem (mount 的时候hierarchy可以attach多个subsystem)

  > A single hierarchy can have one or more subsystems attached to it.

  eg.

      mount -t cgroup -o cpu,cpuset,memory cpu_and_mem /cgroup/cpu_and_mem

  ![cgroup-rule1](/images/cgroup-rule1.jpeg)

#### 2.一个已经被挂载的 subsystem 只能被再次挂载在一个空的 hierarchy 上 (已经mount一个subsystem的hierarchy不能挂载一个已经被其它hierarchy挂载的subsystem)

  > Any single subsystem (such as cpu) cannot be attached to more than one hierarchy if one of those hierarchies has a different subsystem attached to it already.

  ![cgroup-rule2](/images/cgroup-rule2.jpeg)

#### 3.每个task只能在一同个hierarchy的唯一一个cgroup里(不能在同一个hierarchy下有超过一个cgroup的tasks里同时有这个进程的pid)

  > Each time a new hierarchy is created on the systems, all tasks on the system are initially members of the default cgroup of that hierarchy, which is known as the root cgroup. For any single hierarchy you create, each task on the system can be a member of exactly onecgroup in that hierarchy. A single task may be in multiple cgroups, as long as each of those cgroups is in a different hierarchy. As soon as a task becomes a member of a second cgroup in the same hierarchy, it is removed from the first cgroup in that hierarchy. At no time is a task ever in two different cgroups in the same hierarchy.

  ![cgroup-rule3](/images/cgroup-rule3.jpeg)

#### 4.子进程在被fork出时自动继承父进程所在cgroup，但是fork之后就可以按需调整到其他cgroup

  > Any process (task) on the system which forks itself creates a child task. A child task automatically inherits the cgroup membership of its parent but can be moved to different cgroups as needed. Once forked, the parent and child processes are completely independent.

  ![cgroup-rule4](/images/cgroup-rule4.jpeg)

#### 5.其它

  * 限制一个task的唯一方法就是将其加入到一个cgroup的task里
  * 多个subsystem可以挂载到一个hierarchy里, 然后通过不同的cgroup中的subsystem参数来对不同的task进行限额
  * 如果一个hierarchy有太多subsystem，可以考虑重构 - 将subsystem挂到独立的hierarchy; 相应的, 可以将多个hierarchy合并成一个hierarchy
  * 因为可以只挂载少量subsystem, 可以实现只对task单个方面的限额; 同时一个task可以被加到多个hierarchy中，从而实现对多个资源的控制

### 操作方法

#### 1.挂载subsystem
 
  * 利用cgconfig服务及其配置文件 `/etc/cgconfig.conf` - 服务启动时自动挂载

        subsystem = /cgroup/hierarchy;
  
  * 命令行操作

        mount -t cgroup -o subsystems name /cgroup/name

    取消挂载

        umount /cgroup/name

  eg. 挂载 cpuset, cpu, cpuacct, memory 4个subsystem到`/cgroup/cpu_and_mem` 目录(hierarchy)

      mount {
          cpuset  = /cgroup/cpu_and_mem;
          cpu    = /cgroup/cpu_and_mem;
          cpuacct = /cgroup/cpu_and_mem;
          memory  = /cgroup/cpu_and_mem;
      }

  or 

      mount -t cgroup -o remount,cpu,cpuset,memory cpu_and_mem /cgroup/cpu_and_mem

#### 2. 新建/删除 cgroup

  * 利用cgconfig服务及其配置文件 `/etc/cgconfig.conf` - 服务启动时自动挂载

        group <name> {
            [<permissions>]    <controller> {  <param name> = <param value>;
                …
            }
            …
        }

  * 命令行操作

     + 新建1 `cgcreate -t uid:gid -a uid:gid -g subsystems:path `
     + 新建2 `mkdir /cgroup/hierarchy/name/child_name`
     + 删除1 `cgdelete subsystems:path` (使用 -r 递归删除)
     + 删除2 `rm -rf /cgroup/hierarchy/name/child_name` (cgconfig service not running)

#### 3. 权限管理

  * 利用cgconfig服务及其配置文件 `/etc/cgconfig.conf` - 服务启动时自动挂载

        perm {
            task {
                uid = <task user>;
                gid = <task group>;
            }
            admin {
              uid = <admin name>;
              gid = <admin group>;
            }
        }

  * 命令行操作 `chown`

  eg.

      group daemons {
          cpuset {
              cpuset.mems = 0;
              cpuset.cpus = 0;
          }
      }
      group daemons/sql {
          perm {
              task {
                  uid = root;
                  gid = sqladmin;
              } admin {
                  uid = root;
                  gid = root;
              }
          }
          cpuset {
              cpuset.mems = 0;
              cpuset.cpus = 0;
          }
      }

  or

      ~]$ mkdir -p /cgroup/red/daemons/sql
      ~]$ chown root:root /cgroup/red/daemons/sql/*
      ~]$ chown root:sqladmin /cgroup/red/daemons/sql/tasks
      ~]$ echo 0 > /cgroup/red/daemons/cpuset.mems
      ~]$ echo 0 > /cgroup/red/daemons/cpuset.cpus
      ~]$ echo 0 > /cgroup/red/daemons/sql/cpuset.mems
      ~]$ echo 0 > /cgroup/red/daemons/sql/cpuset.cpus

#### 4. cgroup参数设定

  * 命令行1 `cgset -r parameter=value path_to_cgroup`
  * 命令行2 `cgset --copy-from path_to_source_cgroup path_to_target_cgroup`
  * 文件 `echo value > path_to_cgroup/parameter`

  eg.

      cgset -r cpuset.cpus=0-1 group1
      cgset --copy-from group1/ group2/
      echo 0-1 > /cgroup/cpuset/group1/cpuset.cpus

#### 5. 添加task

  * 命令行添加进程 `cgclassify -g subsystems:path_to_cgroup pidlist`
  * 文件添加进程  `echo pid > path_to_cgroup/tasks`
  * 在cgroup中启动进程 `cgexec -g subsystems:path_to_cgroup command arguments`
  * 在cgroup中启动服务 `echo 'CGROUP_DAEMON="subsystem:control_group"' >> /etc/sysconfig/<service>`
  * 利用cgrulesengd服务初始化，在配置文件`/etc/cgrules.conf`中

        user<:command> subsystems control_group

        其中:
        +用户user的所有进程的subsystems限制的group为control_group
        +<:command>是可选项，表示对特定命令实行限制
        +user可以用@group表示对特定的 usergroup 而非user
        +可以用*表示全部
        +%表示和前一行的该项相同

  eg.

      cgclassify -g cpu,memory:group1 1701 1138
      echo -e "1701\n1138" |tee -a /cgroup/cpu/group1/tasks /cgroup/memory/group1/tasks
      cgexec -g cpu:group1 lynx http://www.redhat.com
      sh -c "echo \$$ > /cgroup/lab1/group1/tasks && lynx http://www.redhat.com"

  通过/etc/cgrules.conf 对特定服务限制

      maria          devices        /usergroup/staff
      maria:ftp      devices        /usergroup/staff/ftp
      @student       cpu,memory     /usergroup/student/
      %              memory         /test2/

#### 6. 其他
  
  + cgsnapshot会根据当前cgroup情况生成/etc/cgconfig.conf文件内容

        gsnapshot  [-s] [-b FILE] [-w FILE] [-f FILE] [controller]
          -b, --blacklist=FILE  Set the blacklist configuration file (default /etc/cgsnapshot_blacklist.conf)
          -f, --file=FILE       Redirect the output to output_file
          -s, --silent          Ignore all warnings
          -t, --strict          Don't show the variables which are not on the whitelist
          -w, --whitelist=FILE  Set the whitelist configuration file (don't used by default)

  + 查看进程在哪个cgroup 

        ps -O cgroup
        或
        cat /proc/<PID>/cgroup

  + 查看subsystem mount情况

        cat /proc/cgroups

        lssubsys -m <subsystems>

  + 查看cgroup `lscgroup`
  + 查看cgroup参数值

        cgget -r parameter list_of_cgroups
        cgget -g <controllers>:<path>

  + cgclear删除hierarchy极其所有cgroup
  + 事件通知API - 目前只支持memory.oom_control
  + 更多
    - man 1 cgclassify — the cgclassify command is used to move running tasks to one or more cgroups.
    - man 1 cgclear — the cgclear command is used to delete all cgroups in a hierarchy.
    - man 5 cgconfig.conf — cgroups are defined in the cgconfig.conf file.
    - man 8 cgconfigparser — the cgconfigparser command parses the cgconfig.conf file and mounts hierarchies.
    - man 1 cgcreate — the cgcreate command creates new cgroups in hierarchies.
    - man 1 cgdelete — the cgdelete command removes specified cgroups.
    - man 1 cgexec — the cgexec command runs tasks in specified cgroups.
    - man 1 cgget — the cgget command displays cgroup parameters.
    - man 1 cgsnapshot — the cgsnapshot command generates a configuration file from existing subsystems.
    - man 5 cgred.conf — cgred.conf is the configuration file for the cgred service.
    - man 5 cgrules.conf — cgrules.conf contains the rules used for determining when tasks belong to certain cgroups.
    - man 8 cgrulesengd — the cgrulesengd service distributes tasks to cgroups.
    - man 1 cgset — the cgset command sets parameters for a cgroup.
    - man 1 lscgroup — the lscgroup command lists the cgroups in a hierarchy.
    - man 1 lssubsys — the lssubsys command lists the hierarchies containing the specified subsystems.

##subsystem配置

###1. blkio - BLOCK IO限额

  * common
    + blkio.reset_stats - 重置统计信息，写int到此文件
    + blkio.time - 统计cgroup对设备的访问时间 - `device_types:node_numbers milliseconds`
    + blkio.sectors - 统计cgroup对设备扇区访问数量 - `device_types:node_numbers sector_count`
    + blkio.avg\_queue\_size - 统计平均IO队列大小(需要`CONFIG_DEBUG_BLK_CGROUP=y`)
    + blkio.group\_wait\_time - 统计cgroup等待总时间(需要`CONFIG_DEBUG_BLK_CGROUP=y`, 单位ns)
    + blkio.empty\_time - 统计cgroup无等待io总时间(需要`CONFIG_DEBUG_BLK_CGROUP=y`, 单位ns)
    + blkio.idle\_time - reports the total time (in nanoseconds — ns) the scheduler spent idling for a cgroup in anticipation of a better request than those requests already in other queues or from other groups.
    + blkio.dequeue - 此cgroup IO操作被设备dequeue次数(需要`CONFIG_DEBUG_BLK_CGROUP=y`) - `device_types:node_numbers number`
    + blkio.io\_serviced - 报告CFQ scheduler统计的此cgroup对特定设备的IO操作(read, write, sync, or async)次数 - `device_types:node_numbers operation number`
    + blkio.io\_service\_bytes - 报告CFQ scheduler统计的此cgroup对特定设备的IO操作(read, write, sync, or async)数据量 - `device_types:node_numbers operation bytes`
    + blkio.io\_service\_time - 报告CFQ scheduler统计的此cgroup对特定设备的IO操作(read, write, sync, or async)时间(单位ns) - `device_types:node_numbers operation time`
    + blkio.io\_wait\_time - 此cgroup对特定设备的特定操作(read, write, sync, or async)的等待时间(单位ns) - `device_types:node_numbers operation time`
    + blkio.io\_merged - 此cgroup的BIOS requests merged into IO请求的操作(read, write, sync, or async)的次数 - `number operation`
    + blkio.io\_queued - 此cgroup的queued IO 操作(read, write, sync, or async)的请求次数 - `number operation`
  * Proportional weight division 策略 - 按比例分配block io资源
    + blkio.weight - 100-1000的相对权重，会被blkio.weight\_device的特定设备权重覆盖
    + blkio.weight\_device - 特定设备的权重 - device\_types:node_numbers weight 
  * I/O throttling (Upper limit) 策略 - 设定IO操作上限
    + 每秒读/写数据上限        
      blkio.throttle.read_bps_device  - `device_types:node_numbers bytes_per_second`
      blkio.throttle.write_bps_device  - `device_types:node_numbers bytes_per_second`
    + 每秒读/写操作次数上限      
      blkio.throttle.read_iops_device - `device_types:node_numbers operations_per_second`
      blkio.throttle.write_iops_device - `device_types:node_numbers operations_per_second`
    + 每秒具体操作(read, write, sync, or async)的控制
      blkio.throttle.io_serviced - `device_types:node_numbers operation operations_per_second`
      blkio.throttle.io_service_bytes -  `device_types:node_numbers operation bytes_per_second`

###2. cpu - CPU使用时间限额

  * CFS(Completely Fair Scheduler)策略 - CPU最大资源限制
    + cpu.cfs\_period\_us, cpu.cfs\_quota\_us - 必选 - 二者配合，前者规定时间周期(微秒)后者规定cgroup最多可使用时间(微秒)，实现task对单个cpu的使用上限(cfs\_quota\_us是cfs\_period_us的两倍即可限定在双核上完全使用)。
    + cpu.stat - 记录cpu统计信息，包含 nr\_periods（经历了几个cfs\_period\_us）, nr\_throttled (cgroup里的task被限制了几次), throttled\_time (cgroup里的task被限制了多少纳秒)
    + cpu.shares - 可选 - cpu轮转权重的相对值
  * RT(Real-Time scheduler)策略 - CPU最小资源限制
    + cpu.rt\_period\_us, cpu.rt\_runtime\_us

      二者配合使用规定cgroup里的task每cpu.rt\_period\_us(微秒)必然会执行cpu.rt\_runtime\_us(微秒)

###3. cpuacct - CPU资源报告

  * cpuacct.usage - cgroup中所有task的cpu使用时长(纳秒)
  * cpuacct.stat - cgroup中所有task的用户态和内核态分别使用cpu的时长
  * cpuacct.usage_percpu - cgroup中所有task使用每个cpu的时长

###4. cpuset -  CPU绑定

  * cpuset.cpus - 必选 - cgroup可使用的cpu，如0-2,16代表 0,1,2,16这4个cpu
  * cpuset.mems - 必选 - cgroup可使用的memory node
  * cpuset.memory\_migrate - 可选 - 当cpuset.mems变化时page上的数据是否迁移, default 0
  * cpuset.cpu\_exclusive - 可选 - 是否独占cpu， default 0
  * cpuset.mem\_exclusive - 可选 - 是否独占memory，default 0
  * cpuset.mem\_hardwall - 可选 - cgroup中task的内存是否隔离， default 0
  * cpuset.memory\_pressure - 可选 - a read-only file that contains a running average of the memory pressure created by the processes in this cpuset
  * cpuset.memory\_pressure\_enabled - 可选 - cpuset.memory_pressure开关，default 0
  * cpuset.memory\_spread\_page - 可选 - contains a flag (0 or 1) that specifies whether file system buffers should be spread evenly across the memory nodes allocated to this cpuset， default 0
  * cpuset.memory\_spread\_slab - 可选 - contains a flag (0 or 1) that specifies whether kernel slab caches for file input/output operations should be spread evenly across the cpuset， default 0
  * cpuset.sched\_load\_balance - 可选 - cgroup的cpu压力是否会被平均到cpu set中的多个cpu, default 1
  * cpuset.sched\_relax\_domain\_level - 可选 - cpuset.sched\_load\_balance的策略
    + -1 = Use the system default value for load balancing
    + 0 = Do not perform immediate load balancing; balance loads only periodically
    + 1 = Immediately balance loads across threads on the same core
    + 2 = Immediately balance loads across cores in the same package
    + 3 = Immediately balance loads across CPUs on the same node or blade
    + 4 = Immediately balance loads across several CPUs on architectures with non-uniform memory access (NUMA)
    + 5 = Immediately balance loads across all CPUs on architectures with NUMA

###5. device - cgoup的device限制

  * 设备黑/白名单
    + devices.allow - 允许名单
    + devices.deny - 禁止名单
    + 语法 - type device\_types:node\_numbers access
      type - b (块设备) c (字符设备) a (全部设备)
      access - r 读 w 写 m 创建
  * devices.list - 报告

###6. freezer - 暂停/恢复 cgroup的限制

  * 不能出现在root目录下
  * freezer.state - FROZEN 停止 FREEZING 正在停止 THAWED 恢复

###7. memory - 内存限制

  * memory.usage\_in\_bytes - 报告内存限制byte
  * memory.memsw.usage\_in\_bytes - 报告cgroup中进程当前所用内存+swap空间
  * memory.max\_usage\_in\_bytes - 报告cgoup中的最大内存使用
  * memory.memsw.max\_usage\_in\_bytes - 报告最大使用到的内存+swap
  * memory.limit\_in\_bytes - cgroup - 最大内存限制，单位k,m,g. -1代表取消限制
  * memory.memsw.limit\_in\_bytes - 最大内存+swap限制，单位k,m,g. -1代表取消限制
  * memory.failcnt - 报告达到最大允许内存的次数
  * memory.memsw.failcnt - 报告达到最大允许内存+swap的次数
  * memory.force_empty - 设为0且无task时，清除cgroup的内存页
  * memory.swappiness - 换页策略，60基准，小于60降低换出机率，大于60增加换出机率
  * memory.use_hierarchy - 是否影响子group
  * memory.oom_control - 0 enabled，当oom发生时kill掉进程
  * memory.stat - 报告cgroup限制状态
    + cache - page cache, including tmpfs (shmem), in bytes
    + rss - anonymous and swap cache, not including tmpfs (shmem), in bytes
    + mapped_file - size of memory-mapped mapped files, including tmpfs (shmem), in bytes
    + pgpgin - number of pages paged into memory
    + pgpgout - number of pages paged out of memory
    + swap - swap usage, in bytes
    + active_anon - anonymous and swap cache on active least-recently-used (LRU) list, including tmpfs (shmem), in bytes
    + inactive_anon - anonymous and swap cache on inactive LRU list, including tmpfs (shmem), in bytes
    + active_file - file-backed memory on active LRU list, in bytes
    + inactive\_file - file-backed memory on inactive LRU list, in bytes
    + unevictable - memory that cannot be reclaimed, in bytes
    + hierarchical\_memory\_limit - memory limit for the hierarchy that contains the memory cgroup, in bytes
    + hierarchical\_memsw\_limit - memory plus swap limit for the hierarchy that contains the memory cgroup, in bytes


###8. net_cls

  * net_cls.classid - 指定tc的handle，通过tc实现网络控制

###9.net_prio 指定task网络设备优先级

  * net_prio.prioidx - a read-only file which contains a unique integer value that the kernel uses as an internal representation of this cgroup.
  * net_prio.ifpriomap - 网络设备使用优先级 - `<network_interface> <priority>` 

###10.其他

  * tasks - 该cgroup的所有进程pid
  * cgroup.event_control - event api
  * cgroup.procs - thread group id 
  * release\_agent(present in the root cgroup only) - 根据notify\_on\_release是否在task为空时执行的脚本
  * notify\_on\_release - 当cgroup中没有task时是否执行release\_agent

##总结

  1. 本文总结了cgroup的操作方法和详细的可配置项，为对更好的控制系统中的资源分配打下基础
  2. 对于限制资源分配的两个场景，在针对特殊APP的场景中可进行非常细致的调优，而在通用的资源隔离的角度上看，可能更关注的是CPU和内存相关的主要属性