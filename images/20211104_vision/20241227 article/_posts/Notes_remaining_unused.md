
为什么
方法论
股价
市场
市场的分析
硬件
Case Study

（P.S. 本文未把 Vision & Strategy 直译为中文，因为难免含义有些偏差。Vision 合并了洞察、远见两者的含义。Strategy 更接近商业策略，而没有“战略”中战的含义。其它名词都尽力维持中文。）

（P.S. Leader 和领导的含义并不相同。Leader 是平等的，领导是有等级的。这里没有将 Leadership 直译成中文。）

Gap analysis, what is a top storage system should be, to compare to what we have today?
data life cycle stream study and each with finer grain ec? what's a top world class ec should be?




(封面图片 by SBA73, CC BY-SA 2.0: https://99percentinvisible.org/episode/la-sagrada-familia/。注：本文为个人观点总结，作者工作于微软)

DeepL翻译器：https://www.deepl.com/translator

\[([^\[\]]+)\]\[(\d+)\] -> [_\1_](.)[\2]
Markdown preview: https://jbt.github.io/markdown-editor/
检查 __ABC__ 等正确渲染
Also, remember to add reference parts.
[](.) replace to weichat link to sections
[transaction]() replace to weichat link to article
插入图片
检查标题正确拼写
声明原创
段落左对齐
插入前文链接
更新文章摘要
排版：不需要增加bullet间空行，尽管编辑器上看着没有空间
排版：试图将消除bullet缩进，消除二级bullet





## Other parts to put into the article

Vision - Abiliity to Define - Making Standard they are linked
硬核分享云产品定义 - 曹亚孟  https://mp.weixin.qq.com/s/8sQINI40GZlXm8l9Wd6n-w

    [Won’t use but keep for track]
    my thinking: Define means capture the space: all possible future landscape space, to host any possibility. and must plot the landscape to give the measure and rules (i.e. 经纬度)
    Next, define the key bottleneck. I.e. to define the key conflicts that is driving the evolving the landscape. Or .. key problems, key challenges, key driving factors
        e.g. NetDAM: 传统的冯诺依曼架构中，计算单元和存储单元是分离的，因此大量的数据流动产生了内存墙和冯诺依曼瓶颈


[Won’t use but keep for track]
  定义的能力：阿里云吴翰清：从技术人转型做产品经理是一种什么样的体验（https://mp.weixin.qq.com/s/tB77Etwfq_h-x32vEcL9og）
  CTO领导力、组织、业务、决策：阿里巴巴CTO独家自述：CTO就是要给CEO扫清障碍和风险 - 程立（https://mp.weixin.qq.com/s/tR1-LCFzt_QDGCOxm8kGWQ）请忽略非常“Aggressive”的标题，很多文章为了流量营销而标题党，标题通常也不是演讲者写的，而是媒体号编辑写的，“标题党”问题。


## Possible new topics to drill down as case study

Some possible drill down topics
  Global database. Global filesystem. Global Windows that everyone can use.

  App商vertical的内容感知的存储

  不是管理blob，而是管理图片、backup、镜像，的内容感知，垂直管理

  根据内容的分类存储，tag标准，AI分类

  一切blob都可query，不是blob，而是AI感知的图片、视频，提供app级管理和内容

  存储媒介blob分裂为ssd基的和hdd/tape基，后者读写差异拉大，不再支持修改。dna存储。

  Still,手算Blob服务收益比: http://accelazh.github.io/storage/Cloud-Storage-Cost-Study

  The application of EBOD on capacity scale storage and on latency target storage.

  Rack scale architecture vs cloud datacenter scale out model. Give SSD is so fast today, even a single rack can serve great needs.

  Given future HDD pool is getting slower and slower, will adding a SSD staging pool be beneficial?

  云发展可能的危机：1）客户下云，成本更低。2）云被管道化    (VastData, Hammerspace)

  Distributed storage vs single host / few host storage. Today, single SSD or PC scaleup is getting more powerful, except CPU. Single host storage can reduce distributing overhead, and suitable for small users probably.

  对于大规模云运营、互联网服务，硬件选型、采购应该是一个和EC一样，需要很好的专业知识、能够大幅降低COGS的领域。未来会和芯片设计知识挂钩，并且服务器领域更加多地使用加速硬件，使这一领域的技能要求更高。技能也能和存储架构、云运营经验挂钩。未来国内可能会有大量机会，等芯片技术和硬件定制技术解锁后，机会更多。

6. Our storage product architecture designs are based on assumption like below. What if the assumptions changed?
  1) Networking speed is much faster than storage and CPU.
  2) HDD favors sequential access. SSD also mostly favors sequential access.
  3) Commodity hardware can scale out to match performance of commercial hardware.

7. How likely is cloud storage becoming a pipe provider, just like what happened to Telecom vs Apps.
    E.g. Snowflake, Hammerspace use Cloud to build their service from much lower cost than traditional vendors when entering the market.
    E.g. How to provided unified namespace for our product as cloud storage?
    E.g. Hybrid cloud, it keeps customer at our side. As a public cloud vendor, how can we do hybrid cloud?
    E.g. Can public cloud's customer support be more competitive and responsive than top heavy working companies?


## Drilling down analysis

1.a 专用NVMe SSD
专用意味着采用内置压缩等计算型存储SSD的方式。截至2026年，专用NVMe SSD将在本地化部署中占据超过30%的份额，相较于2023年中期不到5%的水平，呈现出明显的增长趋势。采用专用NVMe SSD带来了多项益处，包括优化存储操作、降低成本，以及构建更具弹性和智能性的数据存储服务环境。

2.a How does the customer look into our products and what’s the future?

3. AI AI AI – What’s the vision of storage in AI world?

Another big topic is, if we switch the resource cost ratio (e.g. memory cost vs disk cost, e.g. network cost vs disk cost), what kind of storage picture it would lead into?
      It’s challenging the assumptions. It’s challenging a future picture that if a hardware breakthrough that would totally re-shift the landscape.

4. Question: Is the cloud or database market in China majorly selling to Gov or its affiliates? Will it cap the ceil of companies, affect whether is gov background? How is the situation compare to US/EU/Large Asia markets?

5. Another investigation point: When will cloud storage market enter slower growth stage?


## Courses

商学院课程: https://www.zhihu.com/question/24024512/answer/134861659. May help review what's vision and how to analysis in advanced methods.


## Mindset tips

1. Deep thinking and industry reflection books. Get the habit to read them.

7.a However, to analytics it also means to do linear projects (vs disruptive innovation), which has the limitation to cannot foresee paradigm shift changes, which however is almost one of the most important technology evolve approach. (Won’t plan to use)
