---
layout: post
title: "Recent Articles Reading: VAST DATA, KV Cache, Google Colossus, Claude Code"
tagline : "Recent Articles Reading: VAST DATA, KV Cache, Google Colossus, Claude Code"
description: "Recent Articles Reading: VAST DATA, KV Cache, Google Colossus, Claude Code"
category: "Paper Reading"
tags: [cloud, LLM, storage, AI]
---
{% include JB/setup %}


```
1. KV Cache管理架构演进：从连续分配到统一混合内存架构 - deephub
   https://zhuanlan.zhihu.com/p/2012270020915389042
2. 统一的AI媒体生产线 - wangleineo的
   https://zhuanlan.zhihu.com/p/1948887920762157033
3. Deepseek-v4 引入 MHC 架构实现性能稳健，如何理解其数学原理与大模型发展影响？ - PP19
   https://www.zhihu.com/question/1991253856454218680/answer/1992715126378349349
4. NVIDIA Fabric Manager 架构设计、工程实现与处理流程全解析 - 码夫祥子
   dhttps://zhuanlan.zhihu.com/p/1986153212257014264
5. Reddit上有个博主花了 1000 个小时研究 prompt 技巧，总结出 6 个方法 - 非著名程序员
   https://zhuanlan.zhihu.com/p/1969789332610090962
6. 2025年Memory最全综述！AI Agent记忆统一分类体系：超越RAG下一代架构 - 杨沐白
   https://zhuanlan.zhihu.com/p/1985435669187825983

7. 对象存储正在重塑数据库架构 - Cursor 
   https://zhuanlan.zhihu.com/p/1983280843783943628
   https://medium.com/@siddontang/object-storage-is-rewriting-the-database-playbook-9e2dd1a81a53
    1. Cursor experience: Yugabyte -> PostgreSQL -> Object Storage
    2. The future data architecture is object-storage first
    3. TiDB X: Next-gen TiDB for an object-storage world
        1. Object storage on S3, as well as cloud SQL

8. 腾讯太极团队实现DeepSeek模型业内H20最高性能15800+ tokens/s - 紫竹
    https://zhuanlan.zhihu.com/p/1981837979547870704
9. 非原创 转载X:我们失去的不只是知乎，而是中文互联网的精神高地 - 利维坦大战龙猫
    https://zhuanlan.zhihu.com/p/1979015454598141392
10. 分布式文件系统架构演进 - AwakeLjw
    https://zhuanlan.zhihu.com/p/1977446763762840860
11. 如何评价美团发布的新上下文级联压缩技术（C3）？ - deephub
    https://www.zhihu.com/question/1977413775251502148/answer/1977427688261174837
12. transformer架构的核心公式其实类似于数学期望，理解起来也不复杂，但为什么这个模型这么强呢？ - CodeCrafter
    https://www.zhihu.com/question/580810624/answer/1976600872675977173
13. 我在性能团队的这两年 - buuug
    https://zhuanlan.zhihu.com/p/16545147271

14. 高性能存储：软硬件协同优化 - panic
    https://zhuanlan.zhihu.com/p/1966538752521410180
    1. Good.

15. 万亿交易背后的代码：顶级做市商XTX开源EB级文件系统TernFS - QuantML
    https://zhuanlan.zhihu.com/p/1964743461254198760
16. DuckDB 的 MVCC 设计与 HyPer 模型 - 陈宗志
    https://zhuanlan.zhihu.com/p/80671035929
17. 分布式元数据论文阅读笔记整理（持续更新） - 妙BOOK言
    https://zhuanlan.zhihu.com/p/673282792
18. 2025年该使用ray、accelerate、trainer、lightning还是pytorch？ - CodeCrafter
    https://www.zhihu.com/question/1926849595331318550/answer/1939450608894608104
19. 国产芯片的三年 - 有了琦琦的棍子
    https://zhuanlan.zhihu.com/p/1933155604605698054
20. 有哪些算法惊艳到了你？ - 好地方bug
    https://www.zhihu.com/question/26934313/answer/32768976853
21. 腾讯开源的 libco 号称千万级协程支持，那个共享栈模式原理是什么? - xiaokang
    https://www.zhihu.com/question/52193579/answer/1996233732437337184w
22. AI for Coding：从 Vibe Coding 到规范驱动开发 - 王人书
    https://mp.weixin.qq.com/s/HaazAEMGqH1GBTmn9qI73g
23. 如何评价 Qwen 门控注意力Gated Attention获得 NeurIPS 最佳论文？ - 旷野
    https://www.zhihu.com/question/1977370700328166444/answer/1978179919344338830

    24. 大厂业务大模型微调实录 - strive
    https://zhuanlan.zhihu.com/p/1931389474501292248
        1. Interesting. Useful.

24. Shade BIOS：一种让BIOS常驻后台，绕过OS安全措施的天才攻击手段 - 老狼
    https://zhuanlan.zhihu.com/p/1936815218610143883
25. 百度商业超大规模KV存储实践d
    https://mp.weixin.qq.com/s/IPx4kpRzXRX8wf35s2SSOQ
26. 大模型推理与 AI Infra 软硬件栈协同优化 - ZOMI酱
    https://zhuanlan.zhihu.com/p/1950701604161446200
27. 从 RAG 到 Context：2025 年 RAG 技术年终总结 - InfiniFlow
    https://zhuanlan.zhihu.com/p/1984948557493592394
    1. Interesting
    2. Different RAG paradigms
        1. Search -> send to LLM as context
        2. Search -> Retrieve full doc / better synthesize -> send to LLM
        3. LLM -> plan -> search -> retrieve -> LLM think and search again -> loop -> LLM piece together results and present

28. 从Deepseek 3FS看AI存储 - 贺大伟
    https://zhuanlan.zhihu.com/p/2009674851913330830
29. FlashAttention进化史：从V1到V4的性能突破 - 章川
    https://zhuanlan.zhihu.com/p/1993815603383902344
30. 2025年数据库回顾 - 李明军
    https://zhuanlan.zhihu.com/p/1993683024462749905
    1. Interesting
31. bilibili技术总监毛剑：B站高可用架构实践 - 腾讯云开发者
    https://zhuanlan.zhihu.com/p/139258985

32. 微软研究：为何LLM会在多轮对话中迷失 - 木牛流码
    https://zhuanlan.zhihu.com/p/1971681801295619070
    1. Interesting research

33. 如何将一棵 LSM-Tree 塞进 NVM - 阿里云云栖号
    https://zhuanlan.zhihu.com/p/411283655
     1. Revisiting the Design of LSM-tree Based OLTP Storage Engine with Persistent Memory    [VLDB 2021, 37 refs]
     2. Key ideas
        1. Replace DRAM with PMEM, redesign data structure in PMEM
        2. Replace memtable with semi-persistent memtable (sp-m)
        3. ROR lock-free logging (Reorder Ring, ChainLog, lock-free ring)
        4. Global index and in-PMEM compact

34. LinkedIn 生成式 AI 技术栈的演进 - 段小草
    https://zhuanlan.zhihu.com/p/1968095125491135108

35. Neon Database适合什么，有哪些问题，给数据库创业者什么启示？ - 路云飞
    https://zhuanlan.zhihu.com/p/1903539433543796195
36. 日久见人心：论建模用户长期兴趣的几种姿势 - 石塔西
    https://zhuanlan.zhihu.com/p/494881660
37. From VecDB to MemOS, From Cloud to LLM - 吴垚
    https://zhuanlan.zhihu.com/p/1970084076183590583

38. 为什么人可以直观地看出函数局部最小值的大致位置，而计算机不能？ - V777
    https://www.zhihu.com/question/657302311/answer/1992562376210393062
    1. Very good. Look ChatGPT to help understand
       https://chatgpt.com/c/69aed597-c9e0-8321-8687-a18aafe71c45
    2. Key points
        1. Finding min is the top problem in NN, 
           the typical solution is using optimization,
           but this article tells you how to use "sampling" to solve it.
        2. Finding min is formulated into tweak θ so that ∫f(x)attention(θ)dx is minimal.
           It means to tweak θ so that attention(θ) is concentrated into the minimal point of f(x).
           It is particularly similar to how human eye finds a minimal point.
        3. To gradually approach to the optimal θ, the key is to step by 
           ∇∫f(x)attention(θ)dx = ∫∇f(x) * attention(θ)dx + ∫f(x) * ∇attention(θ)dx
             = E(∇f(x)) + ∫f(x) * ∇log(attention(θ)) attention(θ) dx
             = E(∇f(x)) + E(f(x)*∇log(attention(θ)))
           The problem is then transformed into finding the expectations on attention(θ) which is a probability density function (PDF).
           Expectations can be obtained by doing sampling, using Monte Carlo.

39. Claude Code auto mode: a safer way to skip permissions - Claude Code 的自动模式
    https://www.anthropic.com/engineering/claude-code-auto-mode?utm_source=chatgpt.com
     1. Good. The is the magic behind --autopilot mode. New breakthrough, finally the agent firewall
     2. Highlights
        1. Claude's internal incident log focused on agentic misbehaviors
        2. How permission decisions work
            1. Tier 1: Built-in safe-tool allowlist and user settings
            2. Tier 2: In-project file operations
            3. Tier 3: Transcript classifier
        3. Why the prompt-injection probe matters

40. Harness Engineering
    1. Harness Engineering 深度解析：AI Agent 时代的工程范式革命
       https://zhuanlan.zhihu.com/p/2014014859164026634
        1. Techniques
            1. Using specialized agents and sub-agents
            2. Json structured execution
                1. Plan → Execute → Verify → Fix → Repeat
            3. Persistent Memory, learn from where you made mistake
            4. Manage context, fill just enough
                1. AGENTS.md, docs, RAG
                2. layered progressive disclosure organization
                3. Be able to discover the right materials
            6. CI pipeline and testing for agents
            7. Autopilot firewall
                1. Claude Code auto mode: a safer way to skip permissions - Claude Code 的自动模式
                   https://www.anthropic.com/engineering/claude-code-auto-mode?utm_source=chatgpt.com
            8. enforcing invariants, not micromanaging implementations
                1. For example
                    1. code can only depend "forward" through a fixed set of layers (Types → Config → Repo → Service → Runtime → UI). 
                    2. Cross-cutting concerns (auth, connectors, telemetry, feature flags) enter through a single explicit interface: Providers. 
                    3. we statically enforce structured logging, naming conventions for schemas and types, file size limits, and platform-specific reliability requirements with custom lints
            9. Entropy and garbage collection
                1. Good. This is new discovery
                2. Agent coding generates garbage code over time, you need
                    1. Periodical garbage cleaning, usually human engineer driven
                    2. Human define golden rules, auto agents enforce and scan
                    3. "Human taste is captured once, then enforced continuously on every line of code"

    2. ChatGPT
       https://chatgpt.com/c/69e36b10-92e0-839d-8f22-6c2cfed6a35b

    3. OpenAI: Harness engineering: leveraging Codex in an agent-first world
       https://openai.com/index/harness-engineering/
        1. 3 dev, 5 months, 1M lines of code
        2. Interesting. This is the article that brings Harness Engineering to its hotness

    4. 2026 Harness Engineering 非常有启发性的论文：AutoHarness 深度解读 - JustBeClaw
       https://zhuanlan.zhihu.com/p/2016839356833341880

41. 浅析 Amazon S3 Files：工作机制、性能边界与 JuiceFS 对比 - Juicedata
    https://zhuanlan.zhihu.com/p/2027708477347312719
    1. S3 Files ：以 EFS 为高性能层的 S3 原生文件系统方案
        1. 可以把它理解为：AWS 在对象存储之上增加了一层基于 EFS 的文件系统访问面，使原本只能通过对象接口访问的数据，也能以目录、文件和挂载点的形式被计算节点直接使用；而文件系统与 S3 之间的数据变化，则由服务在后台自动同步。
        2. Only files smaller than 128KB will be cached in EFS, larger files directly go to S3

42. 震惊！Google Colossus 文件系统选择 1MiB Chunk 的原因竟然是…… - 李明
    https://zhuanlan.zhihu.com/p/2028454368735708026
    1. Very good. Cloud Filesystem design is changing now. 
       With 1MB chunk size. Colossus is append-only, and per chunk location is also in BigTable. 
       The earliest articles aren't new, they were in 2009, 2017, 2019.
    2. 64MB to 1MB chunk, here is the motivation
        1. Like 3FS or Parallel File System, shard files to all nodes to improve throughput
        2. Faster chunk recovery, to reduce the unavailable time to user access
    3. Backing techniques
        1. Backing tech: Colossus hosts metadata in BigTable, 1MB chunk's massive metadata is now scalable
        2. Pack small files into a 6MB or 8MB big file and EC into 1MB chunks
        3. The age of SSD

    4. ChatGPT: https://chatgpt.com/c/69e37da8-b72c-839c-b422-685933a21174
        1. Colossus simplified the GFS programming model to an append-only storage system
        2. Google Colossus reduced chunk size from GFS’s 64 MB to ~1 MB
        3. Colossus stores all metadata (including chunk/block metadata) in a distributed metadata service ("Curators") backed by Bigtable. Data nodes ("D servers") do NOT own authoritative chunk metadata.
           https://shambhavishandilya.medium.com/colossus-googles-file-system-baced846d9b7
           https://luminousmen.substack.com/p/bigquery-explained-what-really-happens

    n. Related materials
        1. Finding the sources of 64MB=>1MB
            1. The Google File System: What Every Distributed Systems Engineer Should Actually Understand About It
               https://www.linkedin.com/pulse/google-file-system-what-every-distributed-systems-engineer-pai-r7u6e/

            2. Google File System block size
               https://stackoverflow.com/questions/26397123/google-file-system-block-size
               It may worths to mention that the successor of GFS, called Colossus, reduce the data chunk size from 64MB to 1MB.

            3. Case Study: GFS: Evolution on Fast-forward
               https://queue.acm.org/detail.cfm?id=1594206

            4. What can be gleaned about GFS successor codenamed Colossus
               https://pierrezemb.fr/posts/colossus-google/

43. Anthropic Mythos model
    1. Assessing Claude Mythos Preview’s cybersecurity capabilities
       https://red.anthropic.com/2026/mythos-preview/
        1. Takeaways
            1. Good. Nowadays, leveraging the modern models well is a necessity to enhance system infra
        2. Highlights
            1. Performance improvement
                1. basic crashes (tier 1) to complete control flow hijack (tier 5)
                    1. Sonnet 4.6 and Opus 4.6 reached tier 1 in between 150 and 175 cases, and tier 2 about 100 times, but each achieved only a single crash at tier 3
                    2. Mythos Preview achieved 595 crashes at tiers 1 and 2, added a handful of crashes at tiers 3 and 4, and achieved full control flow hijack on 10 separate, fully patched targets (tier 5)
            2. For us, that means starting with Project Glasswing. And while we do not plan to make Claude Mythos Preview generally available
               https://www.anthropic.com/glasswing

    2. System Card: Claude Mythos Preview
       https://www-cdn.anthropic.com/08ab9158070959f88f296514c21b7facce6f52bc.pdf
        1. Bad ... 200+ pages PDF
        n. Related materials
            1. ChatGPT: https://chatgpt.com/c/69e98fa1-127c-83a0-ba9a-3ccaefaa7285
                1. cyber operator
                    1. Previous models
                        1. can write exploit code if you guide them
                    2. Mythos
                        1. finds vulnerabilities + builds exploits end-to-end
                        2. can chain multiple bugs into a full attack
                        3. works on real systems (OS, browsers, kernels)
            
            2. 如何评价 Anthropic 这个据称强到不敢直接发布的大模型 Mythos Preview?
               https://www.zhihu.com/question/2025124518817973047
               Anthropic最强大模型“Claude Mythos预览版”深度解析
               https://zhuanlan.zhihu.com/p/2025121628577625231

            3. Google search: 
                以下是知乎上关于Mythos的核心观点和信息：
                    1. 能力极强且危险： Mythos被称为Claude产品线中有史以来最强大的模型，在评估基准上大幅超越之前的模型。有观点认为其由于能力太强，“聪明到不敢公开”。
                    2. 非正常发布： 不同于常规的AI模型，Anthropic没有为Mythos提供公开API，也没有更新claude.ai的模型选项。
                    3. 潜在风险与担忧： Anthropic在测试中发现该模型具有极强的网络漏洞发现和攻击能力，因此因潜在滥用风险而未公开。
                    4. 技术架构（OpenMythos）： 有知乎用户提到，有人利用公开研究“逆推”并开源了名为“OpenMythos”的模型架构，该架构实现了循环深度Transformer（Recurrent-Depth Transformer, RDT）。
                    5. 引起业界恐慌： Mythos的发布在AI行业引发关注，甚至被认为逼迫Google等其他技术巨头紧急应对。 
                在知乎上，用户通常围绕该模型的“被封印”状态、极高的计算推理能力以及对“OpenMythos”开源实现展开深度技术分析和讨论。

44. FAST 2002–2026：AI 时代来了，存储系统的问题变了吗？ - 团子云技术
    https://zhuanlan.zhihu.com/p/2027130965617643713
45. 创业者思考：如何做 AI Agent 喜欢的基础软件？ - Founder Park
    https://zhuanlan.zhihu.com/p/1987033206663435327
46. Claude Code内部复盘：不再需要产品经理，揭开快速迭代的秘密 - 段小草
    https://zhuanlan.zhihu.com/p/2030815687707464658

48. Understanding VAST Data's Erasure Coding Architecture - Storage Math
    https://storagemath.com/posts/vast-data-erasure-coding/
    1. https://chatgpt.com/c/6a0f90d6-9df4-83ec-bb58-7580c48da7d5
-----
# VAST Data Erasure Coding Article Summary

## Core Summary

- **Protection tiers**
  - **What the article says:** VAST uses three different schemes:
    - Metadata replication
    - SCM write-buffer erasure coding
    - QLC capacity erasure coding
  - **Key numbers:**
    - Metadata: `3x` replication
    - Write buffer: `N+2`
    - Capacity tier: `146+4`
  - **Why it matters:** Different layers fail differently, so the system cannot be reasoned about as one simple EC model.

- **Capacity efficiency**
  - **What the article says:** VAST’s capacity tier is described as `146` data + `4` parity.
  - **Key numbers:**
    - Efficiency: `146 / 150 = 97.33%`
    - Parity overhead vs data: `4 / 146 = 2.74%`
  - **Why it matters:** Much better raw efficiency than common `12+4` Reed-Solomon.

- **Traditional comparison**
  - **What the article says:** `12+4` Reed-Solomon is used as the simple baseline.
  - **Key numbers:**
    - Efficiency: `12 / 16 = 75%`
    - Parity overhead vs data: `4 / 12 = 33.33%`
  - **Why it matters:** VAST saves a lot of flash capacity, but uses proprietary algorithms.

- **Write-buffer change**
  - **What the article says:** VAST 5.1 changed the SCM write buffer from mirroring to EC.
  - **Key numbers:**
    - StorageMath says write amplification changes from `3x` to `1.2x`.
    - VAST says SCM RAID gives `50%` faster writes.
    - One example moves from mirroring to `6+2` RAID.
  - **Why it matters:** The write path becomes much more space-efficient, but also more complex.

- **Metadata asymmetry**
  - **What the article says:** Metadata still uses triplication and waits for all three acknowledgements.
  - **Key numbers:**
    - Metadata write requires `3 / 3` acknowledgements.
    - It is not a majority-quorum scheme.
  - **Why it matters:** With two SCM-side failures, the write buffer may still survive, but metadata writes can stop.

- **Rebuild claim**
  - **What the article says:** VAST claims locality helps rebuild without reading all surviving data.
  - **Key numbers:**
    - For a device failure, rebuild may typically read around `1 / 4` of data.
  - **Why it matters:** The public material focuses mostly on single-failure rebuild behavior.

- **Algorithm transparency**
  - **What the article says:** StorageMath argues VAST is not simply Zigzag code.
  - **Key numbers:**
    - VAST capacity-tier rate: `146 / 150 = 0.973`
    - Zigzag optimal rebuild condition cited by the article: `k / n < 0.5`
  - **Why it matters:** The article concludes VAST must be using a proprietary LDEC-like construction, not standard Zigzag.

- **Failure-domain placement**
  - **What the article says:** Wide stripes need careful placement.
  - **Key numbers:**
    - VAST public material mentions stripe widths from `36+4` to `146+4`.
    - DBox-HA limits strips per DBox.
  - **Why it matters:** Poor placement can turn device-level resilience into rack-level or enclosure-level availability risk.

- **Operational tradeoff**
  - **What the article says:** VAST is attractive at large scale but harder to reason about.
  - **Key numbers:**
    - At `100 PB`, the article says `2.74%` overhead vs `33.33%` overhead can mean roughly `30 PB` of hardware difference.
  - **Why it matters:** The value depends on whether capacity savings justify vendor-specific operational complexity.

## Dedicated Erasure Coding Section

### SCM Write-Buffer Erasure Coding

- **Layer:** SCM write buffer
- **Scheme described:** Double-parity EC
- **Example parameters:**
  - `6+2`
  - `8+2`
  - `10+2`
- **Failure tolerance:**
  - Any `2` SCM, device, or failure-domain failures, depending on layout.
- **Main purpose:**
  - Lower write amplification than mirroring while keeping the write buffer protected.

### QLC Capacity-Tier Erasure Coding

- **Layer:** QLC capacity tier
- **Scheme described:** Proprietary LDEC
- **Example parameters:**
  - `146+4`
- **Failure tolerance:**
  - Claimed tolerance of `4` missing strips or device failures.
- **Main purpose:**
  - Extreme capacity efficiency with local rebuild optimization.

## Important EC Numbers

- **VAST capacity LDEC**
  - Data shards: `146`
  - Parity shards: `4`
  - Total shards: `150`
  - Efficiency: `146 / 150 = 97.33%`
  - Parity overhead vs data: `4 / 146 = 2.74%`
  - Comment: Very high efficiency; proprietary.

- **Reed-Solomon 12+4**
  - Data shards: `12`
  - Parity shards: `4`
  - Total shards: `16`
  - Efficiency: `12 / 16 = 75.00%`
  - Parity overhead vs data: `4 / 12 = 33.33%`
  - Comment: Lower efficiency, but standard and easy to reason about.

- **SCM 10+2**
  - Data shards: `10`
  - Parity shards: `2`
  - Total shards: `12`
  - Efficiency: `10 / 12 = 83.33%`
  - Parity overhead vs data: `2 / 10 = 20.00%`
  - Comment: VAST example says a `1 MB` write becomes `1.2 MB` into SCM.

- **SCM 6+2**
  - Data shards: `6`
  - Parity shards: `2`
  - Total shards: `8`
  - Efficiency: `6 / 8 = 75.00%`
  - Parity overhead vs data: `2 / 6 = 33.33%`
  - Comment: More overhead, but likely easier to fill stripes under smaller-scale or placement constraints.

- **Metadata 3x replication**
  - Logical data unit: `1`
  - Extra copies: `2`
  - Total copies: `3`
  - Efficiency: `1 / 3 = 33.33%`
  - Overhead vs data: `2 / 1 = 200%`
  - Comment: Simple for small random metadata writes, but asymmetric compared with EC-protected layers.

## Key Takeaway

VAST’s design is attractive because it pushes capacity efficiency very high, especially with a `146+4` capacity-tier code. However, this comes with tradeoffs:

- The EC algorithm is proprietary.
- The system uses multiple protection schemes at different layers.
- Metadata protection and data protection have different failure behavior.
- Wide-stripe EC requires careful failure-domain placement.
- Independent reasoning about multi-failure behavior is harder than with standard Reed-Solomon.

For storage system design, the most useful lesson is:

> Wide-stripe EC can provide huge storage-efficiency gains, but placement, rebuild, metadata protection, write-buffer protection, and degraded-mode semantics must be designed together.
-----

50. Magic Pocket 冷存储是怎么炼成的：跨区域分片擦除编码 (Erasure Coding) 实战
   https://zhuanlan.zhihu.com/p/2031680509953169388
   How we optimized Magic Pocket for cold storage - Dropbox
   https://dropbox.tech/infrastructure/how-we-optimized-magic-pocket-for-cold-storage
    1. 
    2. Highlights
        1. "读完你会理解：为什么真正大规模存储系统的最大风险不是磁盘故障，而是 software bug 同时擦掉两个区域的数据。"
           "如果整个 EC 是 一个全局软件实例 在执行，那么——这个实例上的 任何一个 software bug、任何一次 operator 误操作，理论上都能在所有区域同时擦掉数据。冗余度再高也救不了。
            反过来说，Magic Pocket 原本”两个区域各运行一套独立软件”的笨办法，恰恰利用了”区域独立”这一点提供了对人为错误的兜底——不同区域可能跑着不同版本的二进制，bug 不会同时触发。"
        2. Magic Pocket solution
            1. "每个 block 被切分为多片 (fragments)，分片用 EC 跨多个区域条带化分布。"
            2. 这套设计有几个非常优美的性质：
                1. 区域独立性回来了——三套软件可以独立部署、独立做 GC、跑不同版本的二进制。
                2. Delete 不需要全局协调——每区域自己删自己那片就行，软件 bug 不会同时擦三份。
                3. 写入可暂停——某区域不可用时，整体可以停写，等回来再补。
                4. 读”永远走最坏路径”——所以单区域故障时，剩下两个区域的流量不会突变（不会出现”灾备切换瞬间负载翻倍”的尾延迟尖峰）。
            3. 延迟：竟然还更好了？
                1. 冷层永远 hedged read（请求三发两收，取快的）
```