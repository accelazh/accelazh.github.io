


市场占有替代过程，商业功能替代
新技术、新场景催生的新可能
新市场的成熟化：数据收集->数据大量存储->数据查询。
市场中Efficiency的变更：一个人管理一台电脑，到一个人管理1PB数据，到一个人管理一个数据中心

9. 发展的另一驱动是市场需求
    Paradigm shift式的需求
        例如，苹果智能手机
                             例如，Cloud-native DB 取代机房部署DB，Scale-out DB取代固定机器数DB。
    安全、隐私、合规等的需要
        例如，GDPR合规，隐私数据删除
        例如，数据主权，跨区存储
        例如，Ransomware保护
    渐进式发展
        更丰富的功能
            例如，云数据库支持分钟级time travel
            例如，对象存储支持更多功能，与数据库接近
                                            例如，DynamoDB支持transaction，曾经式KV。
                                            例如，单节点数据库如今都向Scaleout SQL发展。NoSQL逐渐被NewSQL取代。Aurora Serverless.
                                            例如，数仓变得支持数据可变和版本。变得支持机器学习和特征工程
                                                // TODO Give a dimension decomposition to all possible feature sets.
                                             Many comes from finer and smaller and smaller customer profile. Then get more and more functionality support. It’s like a fraction tentacles, reaching to wider and finer, then




get you a more complex product and more market shares.
        多产品、多平台的融合
                                  例如，对象存储支持文件系统接口
                                  例如，产品跨界，扩展版图
        更快、更稳定、更大
         例如，云数据库支持Scale out
                                  E.g., I want OLAP to be realtime. I want metrics monitoring to support SQL query.
                                  Edge cloud, edge zone,
                                  Hardware path bypassing CPU.
            全球化
            数据迁移
            统一命名空间
            统一事务
            跨区容灾

                             Hardware plane
                                 Disaggregation the function unit -> No CPU / ASIC acceleration -> Commercial design vs Commodity design
        软件层的性能提升
                SSD placement, NVMe FDP, NVMe stream.
                Erasure coding
                DPDK, SPDK, kernel bypassing.








// TOOD 动力、驱动因素

// TODO 市场演变的动力：技术发展、需求发展，的两头凑；加上创新 disruptive  Innovation
// TODO 资产和关于资产的讨论

// TODO Evaluation matrix
// TODO 市场分析帮助vision和strategy认识我们在市场所处的位置
// TODO 什么是价值
// TODO 需求和驱动
// TODO 优势


// TODO 市场演变的动力：技术发展、需求发展，的两头凑；加上创新 disruptive  Innovation

externally, how we handle the scale. how we handle the competitors? how is the storage and cloud technology trends after 10 years?
think how we will be doing after 3 years 5 years 10 years.
what's the industry doing from 10 years past? compared to now to 10 years after?

Understand storage competitor & eco. Multiple lanes: 1) Cloud AWS/Google 2) Classic commercial SAN/NFS vendors 3) Data back/management vendors 4) Opensource community.
Externally, position of the world storage industry and academy

市场->产品->我们的位置->发展空间->什么是价值->需求变化->演化周期->驱动因素
文章-市场：分解为市场结构规律，创新，市场分区，政策问题，主要vendor，各分区主要产品和特点、Gartner比较，产品，什么是价值，需求驱动，发展空间，我们的位置

市场分析
    ….
Search “How come the gap of Azure vs AWS market share”
    关于市场发展规律，市场结构、创新突破的分析

产品
    ….
Distinctive advantage – Search “Distinctive advantage” see analysis
Search “什么是真正有价值的资产”

发展空间
    Search “发展的另一驱动是市场需求”
发展的驱动力是什么，什么驱动需求？
不同维度，分章节
        技术
        需求、消费者
        硬件
        市场老化、融合、换代

我们的位置
Where we are in the market
    Comparative tracks, vendor landscape
    Market, producer, consumer, us.

What's value
    The analysis of what's our key value other than tech
    What should be our invest
    各种反直觉结论的列表

创新和商业模式演化周期 -> 通过市场分析+竞争对手，定制5年业务发展天花板，和路线。

Driving factors behind -> market, customer, technology parts
Technology spectrum in storage industry landscape -> breakdown of the market and technology parts

Hardware price calculation
    Lanscape and growth strategy

市场    // Search “Breakdown storage product abilities into axes”。 Search “市场中Efficiency的变更”



2023年企业级存储主要发展趋势- https://mp.weixin.qq.com/s?__biz=Mzg3MDY0OTQ0NA==&mid=2247490328&idx=1&sn=c467bcc73b5308c43c1d4ce38ee7e6cb





1. possible direction to drill down vision. Breakdown storage product abilities into axes. Project how they can reach in market demand vs technology support, and what are the possible things we can do in the next years.
•	Project market demand
•	Project technology support
o	Hardware trends
o	Software abilities
•	Project competitors
•	Where are we
•	Where we will be in the next 3~5 years

1. market demand
    1. The best way is you have customers, you do market research, you buy analytics reports.
    2. I don't have that. I need to use the past and current status to project.

2. disruptive innovations
    1. I have to ignore that. Because all analysis are linear that based on projection from the past. disruptive innovations are hard to predict.
3. but disruptive innovations are important. we can study the seed investments, startups, new tech adoption/propagation trends, etc to find
4. A list of future promising technologies that we can take into picture and build another projection based on it.


Competitor analysis: our position, predict the missing feature, predict the gap of non-functional properties.

Internal software maintenance cost. Software is viewed as a middle layer to expose hardware ability to customer. So
•	The true value of software layer is to provide functionalities. To manage the hardware resources.
o	Functionality is a key competitor in 2B software.
	把企业应用的复杂性分解为数据、权限、流程、算法、集成、报表等六个维度 (https://mp.weixin.qq.com/s/OXCBORheAx99o3fS-ZfUdg)




6. Our storage product architecture designs are based on assumption like below. What if the assumptions changed?
1) Networking speed is much faster than storage and CPU.
2) HDD favors sequential access. SSD also mostly favors sequential access.
    3) Commodity hardware can scale out to match performance of commercial hardware.

7. How likely is cloud storage becoming a pipe provider, just like what happened to Telecom vs Apps.
    E.g. Snowflake, Hammerspace use Cloud to build their service from much lower cost than traditional vendors when entering the market.

8. Distinctive advantage, doesn’t show up at how disciplined your engineers are to be involution with each other. But at
1) Distinctive way to organize engineering pipeline. E.g. SpaceX vs traditional rocket manufacturing. E.g. Chrome updating model vs MS office/OS update. E.g. Chrome plugin store vs Edge.
2) Technology with large scale and complex engineering accumulation that made impossible possible. E.g. AWS cloud. E.g. Apple phone.
3) Quality control, delivery control. Just to run faster than other competitors.
4) Connections and trust with customers, partners, governments.
5) Business model that deems to have advantage and made possible eventually. E.g. Alibaba Taobao selling vs traditional retails.
    6) Large amount of production data, many heavy users already been using the system for core usecases for many years. Especially for storage, filesystem, database vendors





9. 发展的另一驱动是市场需求
    Paradigm shift式的需求
        例如，苹果智能手机
                             例如，Cloud-native DB 取代机房部署DB，Scale-out DB取代固定机器数DB。
    安全、隐私、合规等的需要
        例如，GDPR合规，隐私数据删除
        例如，数据主权，跨区存储
        例如，Ransomware保护
    渐进式发展
        更丰富的功能
            例如，云数据库支持分钟级time travel
            例如，对象存储支持更多功能，与数据库接近
                                            例如，DynamoDB支持transaction，曾经式KV。
                                            例如，单节点数据库如今都向Scaleout SQL发展。NoSQL逐渐被NewSQL取代。Aurora Serverless.
                                            例如，数仓变得支持数据可变和版本。变得支持机器学习和特征工程
                                                // TODO Give a dimension decomposition to all possible feature sets.
                                             Many comes from finer and smaller and smaller customer profile. Then get more and more functionality support. It’s like a fraction tentacles, reaching to wider and finer, then




get you a more complex product and more market shares.
        多产品、多平台的融合
                                  例如，对象存储支持文件系统接口
                                  例如，产品跨界，扩展版图
        更快、更稳定、更大
         例如，云数据库支持Scale out
                                  E.g., I want OLAP to be realtime. I want metrics monitoring to support SQL query.
                                  Edge cloud, edge zone,
                                  Hardware path bypassing CPU.
            全球化
            数据迁移
            统一命名空间
            统一事务
            跨区容灾

                             Hardware plane
                                 Disaggregation the function unit -> No CPU / ASIC acceleration -> Commercial design vs Commodity design
        软件层的性能提升
                SSD placement, NVMe FDP, NVMe stream.
                Erasure coding
                DPDK, SPDK, kernel bypassing.


个人发展、资产的评估纬度，列举矩阵    // 搜百科查资产评估。 - 所以Vision的分析框架主要是follow资本家视角来进行的？真资本主义…… 敢于献身不利资产的人、甚至是大部分人，是真的勇士。
    1. 是否支持复利，增长是线性，还是指数
    2. 是否可迁移，例如公司内人际关系不宜在跳槽时迁移
    3. 是否自然垄断，规模效应、政策、传播
    4. 是否需要持续维护成本
5. 是否持续折旧
    6. 广泛的联系类型的资产具有稳定性，最好是N对1的垄断型



什么是真正有价值的资产    // TODO 使用矩阵分析
    技术
    技术体系
    工程
    执行力
客户关系
        声望 Reputation
        信任，长期的客户积累，成功案例
    政府关系
    企业文化
    品牌
    人员组合
工作场所评价
              实体联结数、稳定性
    Scale 规模效应
垄断
        平台聚集客户，更多客户更聚集
        能源产业、规模效益
        关系、trust，独占客户的新人空间，
        金融信任
        占有大量渠道
        社交聚集
        政策性垄断
        独有专利技术，如ChatGPT
  不幸的是，社会仇恨、冲突和对抗思潮，也是也满足良好资产的特性
        基于仇恨和国际冲突，在达到门槛后，有巨大的获利空间。战争是可持续的和可profitable的。人们为了保卫他人生命而激发的灼烈情感带来的杀戮方面的消费，远超基于生存需要、欲望、娱乐而来的消费。
粉丝群也是资产
      这解释类为什么宁可直播，也不愿进厂



    元素分解
        企业层面
            市场
            对手
            企业
               产品
               员工
               组织
        个人层面
               技术
               关系

    价值资产需要
        难替代性
            技术 vs 关系
        溢价
            即使对手有同样强大的产品，我们仍可以卖出更高价格
            即使被对手完全泄密，我们仍可以卖出更高价格
        时间稳定
            不应迅速过时，不应迅速被取代

当众多市场实体，企业、个人，将组合向价值资产靠拢
    资产粘性上升，垄断价值高端，编织关系
    流动性下降
    市场老化
     新入场者将处于劣势，选择
         卷
         开辟新的，不成熟的市场
         在旧市场进行革命
         退出躺平
        新人倾向进入未老化市场，高流动

      老人
                   If assuming the industry evolving is following a climbing cycles model, then learning from the past history is extremely important. For example, from scaleout storage, we are even going to back to multi-head box design or even fully connected super-computer. That’s going back from scaleout commodity hardware to old commercial hardware history, in a ~20 year cycle. The old people are extremely important when we try to learn from past experience. We don’t even need the old people to have competent skills, just copying from the history is extremely valuable.


程序员修炼之道 – 1.5 管理你的知识资产
https://awesome-programming-books.github.io/others/%E7%A8%8B%E5%BA%8F%E5%91%98%E4%BF%AE%E7%82%BC%E4%B9%8B%E9%81%93%EF%BC%9A%E4%BB%8E%E5%B0%8F%E5%B7%A5%E5%88%B0%E4%B8%93%E5%AE%B6.pdf
•	知识工作者回报较体力劳动者高，因为知识是资产，而不是消耗品。知识可以积累，有乘法效应。但对程序员行业来说，知识资产有一些特性：随时效递减（expiring asset）。资产投资的准则之一是多元化，而程序员专精技术可以说是背道而驰。





17. rethinking the driving factors for storage evolving trends and dynamics, vision in 1 ~ 3 years
    1. hardware
                    1. new type of hardware, e.g. 3D-XPoint, SSD, SMR, ZNS, NVMoF
                    2. growing capacity of hardware, e.g. TB memory, 1 machine 100+ HDD, manycore, RDMA
                    3. changing propotion of hardware, e.g. colocating compute/storage vs disaggregated design Snowflake, faster networking / faster storage device vs not-catching up CPU
                    4. smart hardware, e.g. FPGA, Computational Storage, AWS Nitro, Azure Catapult
                    5. GPU, DPU, IPU

    2. growing scale of data capacity and IOPS
                    1. distributed scale-out storage, Ceph, now everything
                    2. distributed filesystem, CephFS, EMC Isilon, Azure HDFS/DataLake
                    3. cloud opening 1000+ datacenters worldwide, interconnect, geo-distribution
                    4. performance deterministic, SLA

    3. COGS saving
                    1. ErasureCoding, performance optimization, Kernel Passthrough
                    2. Data deduplication
                    3. Data tiering, migrating, caching, etc
                    4. underlying data representation, data format, physical layout

    4. Reliability
                    1. Data backup, Copy data management

    5. related technology
                    1. container, cloud
                    2. TLA+, formal verification
                    3. consistent hashing, distributed transactions, append-only LSM tree, ART / Mass-tree indexes

    6. User interface changing, new business models
                    1. SQL, no SQL, new SQL
                    2. OLAP, OLTP, HTAP
                    3. in-memory storage, all flash, NVMe storage
                    4. Cloud, Hybrid Cloud, Cloud offloading, Hyper-converged, IoT, Edge computing, Blockchain
                    5. many pushing from new changing consumer, e.g. the active Database community, VM & virtualization, NFS, page & block storage, archiving, data backup, AI & machine learning & deep learning, GPU, Datalake & enterprise data mgmt and analysis, software defined DC/stoage, containerization, etc
                    5. stream processing, transactional streaming, evolving table, RDD, XOR linage
                    6. video processing. online realtime podcasting

    6.5. Co-design with surrounding
                    1. Co-design with database some years, and then decouple design some years
                    2. Co-design the custom hardware some years, and then decouple with whitebox commodity hardware some years
                    3. Open-Channel SSD, ZNS GC, SMR GC

    7. security
                    1. Zero trust, confediential computing
                    2. Ransomware, Immutable Storage

    8. Data management
                    1. Operational model changing, Orchestration
                    2. on-premise and hybrid cloud management and COGS improvement, metrics and analytics COGS saving
                    3. data migration, shipping, Edge, caching, Tiering



    vision in 1 ~ 3 years
      1. in general, the vision is more a wording for startups, where leader needs insight in one or a few directions but with predictions, depth, and belief
         to understand overall trends, the wording "trends" already have a lot of study, which can be easily searched on google.
                    for the daily work, the vision is more like a breakdown, to more specifically know what our team should do in the following 1 ~ 3 years, and where are our SWOT - Weakness/bottleneck, Strength, Opportunities, Risks
      2. what are the bottlenecks/directions in our xstream team in the following 1~3 years
                      1. scale-out the metadata, the data, the operation management. balance and migration.
                      2. reduce COGS, improve performance, more sellable IOPS/capacity, less amplification.
                      3. deterministic performance, better request SLA. improving customer request resolving time and satisfaction.
                      4. data reliability and corruption. security hardening.
                     5. fitting working with new type of hardware layout, new generation, new SKU, Rack count, geo-distribution, etc
                      6. shipping new technology, e.g. storage device, e.g. CPU feature, into our system.
                      7. internal technical debts, better design and refactor, adding metrics, measures, making visible and systematic
    3. what is the storage at world industry position?
    4. what is the storage at our competitor position? AWS/Google, SAN/NFS vendors, Data backup vendors / Data management
    5. what kind of team, guys, and how we work and organize, will be, after 3~5 years?


-------------


Vision - Abiliity to Define - Making Standard they are linked
硬核分享云产品定义 - 曹亚孟  https://mp.weixin.qq.com/s/8sQINI40GZlXm8l9Wd6n-w
  my thinking: Define means capture the space: all possible future landscape space, to host any possibility. and must plot the landscape to give the measure and rules (i.e. 经纬度)
    Next, define the key bottleneck. I.e. to define the key conflicts that is driving the evolving the landscape. Or .. key problems, key challenges, key driving factors
        e.g. NetDAM: 传统的冯诺依曼架构中，计算单元和存储单元是分离的，因此大量的数据流动产生了内存墙和冯诺依曼瓶颈
    Categorize different alternatives, and think what if how to handle at each path. and use 柏拉图式提问 to think more and deeper. and use 5 Whys asks to drill deeper.
    What's the risk, can I foresee the risk?
    Another aspect of vision is knows what is under water. E.g. knows which team is doing what this year, before paper is published. which direction is actively being tried by which guys in industrial elsewhere. which lab/startup is trying which part, tried which and fail, or promising. what community is doing and the directions. E.g. 浅谈数据湖的过去，现状和未来 - 你说得对（https://zhuanlan.zhihu.com/p/450041140） This article can be used as reference for vision too

  定义的能力：阿里云吴翰清：从技术人转型做产品经理是一种什么样的体验（https://mp.weixin.qq.com/s/tB77Etwfq_h-x32vEcL9og）
  CTO领导力、组织、业务、决策：阿里巴巴CTO独家自述：CTO就是要给CEO扫清障碍和风险 - 程立（https://mp.weixin.qq.com/s/tR1-LCFzt_QDGCOxm8kGWQ）请忽略非常“Aggressive”的标题，很多文章为了流量营销而标题党，标题通常也不是演讲者写的，而是媒体号编辑写的，“标题党”问题。



--------------




// TODO 为什么说腾讯22年前的这份神级PPT是立项汇报的天花板？ - 卫夕的文章 - 知乎
https://zhuanlan.zhihu.com/p/684222828

// TODO 硬核分享云产品定义
https://mp.weixin.qq.com/s/8sQINI40GZlXm8l9Wd6n-w

// TODO 下篇：技术 Leader 的思考方式 - 阿里云云栖号的文章 - 知乎
https://zhuanlan.zhihu.com/p/526571851


颠覆性创新？存储界已有所耳闻 - Andy730
https://mp.weixin.qq.com/s/NFQYEwrYCwKvTjpQdLkcQA


