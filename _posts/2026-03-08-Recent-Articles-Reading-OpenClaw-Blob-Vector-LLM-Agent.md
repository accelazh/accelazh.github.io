---
layout: post
title: "Recent Articles Reading: OpenClaw, Blob Vector, LLM Agent"
tagline : "Recent Articles Reading: OpenClaw, Blob Vector, LLM Agent"
description: "Recent Articles Reading: OpenClaw, Blob Vector, LLM Agent"
category: "Paper Reading"
tags: [cloud, LLM]
---
{% include JB/setup %}

```
1. DeepTech深科技: 谷歌AI十年棋局：从猫识别到太空数据中心，Gemini如何统一生态
   https://zhuanlan.zhihu.com/p/1977401514071959136
    1. Useful reference as how Google organized its AI strategy company-wide that eventually led to success

2. 2025 AI 记忆系统大横评：从插件到操作系统，谁在定义下一代Agent Infra？ - 机器之心
   https://zhuanlan.zhihu.com/p/1978869876396413893
    1. Good.
    2. Highlights
        1. 我们梳理了2024–2025年全球开源社区出现的十几种完全不同的 Memory 技术路线和代表项目：
            自动抽取记忆（Mem0）
            企业级 Memory Server（Zep）
            结构化记忆树（MemU）
            神经张量记忆（MemOS）
            生物启发的Memory OS（EverMemOS）
            屏幕级多模态记忆（Mirix）
            Profile-based Memory（Memobase）
            文件系统式 Memory（Letta）
            视频级记忆 / LVMM（Memories.ai）
            知识图谱式超记忆（Supermemory）
            LangMem（LangChain 官方 Memory SDK）

3. LLM Agent System Development - 静水流深
   https://en.zhihu.com/article/29975037546
    1. Good and useful summary of key agent knowledge points

        """
        One, Core Fundamental Knowledge
        一、核心基础知识
        1. The underlying principles of large language models (LLM)
        1. 大型语言模型（LLM）的底层原理
        - Transformer Architecture: Self-Attention Mechanism, Positional Encoding, Multi-Head Attention
        - Transformer 架构：自注意力机制、位置编码、多头注意力
        - Pre-training Techniques: BERT (Masked Language Modeling), GPT (Autoregressive Modeling), and Mixed-Objective Models (e.g., T5)
        - 预训练技术：BERT（遮蔽语言模型）、GPT（自回归建模）以及混合目标模型（例如 T5）
        - Fine-tuning methods: Adapter, LoRA, Prompt Tuning, RLHF (Reinforcement Learning from Human Feedback)
        - 微调方法：Adapter、LoRA、提示调优、RLHF（来自人类反馈的强化学习）
        Model Compression and Inference Optimization: Quantization, Distillation, KV Cache, FlashAttention
        模型压缩与推理优化：量化、蒸馏、KV 缓存、FlashAttention

        2. Core Concepts of the Agent System
        2. 代理系统的核心概念
        - Agent Design Paradigms: ReAct, Toolformer, AutoGPT
        - 代理设计范式：ReAct、Toolformer、AutoGPT
        - Planning and Decision Making: Task Decomposition (Task Decomposition), Chain of Thought (CoT), Self-Refinement (Self-Refine)
        - 规划与决策：任务分解（Task Decomposition）、思维链（Chain of Thought，CoT）、自我改进（Self-Refine）
        - Memory Mechanisms: Short-term Memory (Context Window), Long-term Memory (Vector Database + Retrieval-Augmented Generation RAG)
        - 记忆机制：短期记忆（上下文窗口）、长期记忆（向量数据库 + 检索增强生成 RAG）
        - Tool Usage (Tool Use): API Integration, Code Execution, Multimodal Extension (e.g., Visual Model Calling)
        - 工具使用（Tool Use）：API 集成、代码执行、多模态扩展（例如，调用视觉模型）

        II. System Design and Engineering Implementation
        II. 系统设计与工程实现
        1. Agent architecture design
        1. Agent 架构设计
        - Modular Design: Planner, Executor, Memory Module, Tool Interface
        - 模块化设计：规划器、执行器、记忆模块、工具接口
        - State Management: Tracking of Conversation History, Task State Machine (State Machine)
        - 状态管理：对话历史追踪、任务状态机（State Machine）
        - Fault tolerance mechanism: Error recovery, exception handling (such as retrying API calls on failure)
        - 容错机制：错误恢复、异常处理（例如在失败时重试 API 调用）

        2. Performance Optimization
        2. 性能优化
        - Context Management: Sliding Window, Key Information Extraction
        - 上下文管理：滑动窗口、关键信息抽取
        - Delay Optimization: Asynchronous Processing, Batch Inference, Caching Strategies
        - 延迟优化：异步处理、批量推理、缓存策略
        - Cost Control: Model Routing (Mixed Invocation of Large/Small Models), On-demand Loading
        - 成本控制：模型路由（大/小模型混合调用）、按需加载

        3. Key Technology Stack
        3. 关键技术栈
        - Development Framework: LangChain, LlamaIndex, AutoGen, Semantic Kernel
        - 开发框架：LangChain、LlamaIndex、AutoGen、Semantic Kernel
        - Tool Ecosystem: OpenAI Functions, Google Toolset, Custom Tool Development
        - 工具生态系统：OpenAI Functions、Google Toolset、自定义工具开发
        - Vector Database: Pinecone, Milvus, FAISS
        - 向量数据库：Pinecone、Milvus、FAISS
        - Evaluation Tools: TruLens, LangSmith
        - 评估工具：TruLens、LangSmith

        III. Advanced Domain Knowledge
        III. 高级领域知识
        4. Multi-modal and Complex Tasks
        4. 多模态与复杂任务
        - Multimodal Agent: Text + Visual (e.g., GPT-4V), Cross-modal Alignment
        - 多模态代理：文本 + 视觉（如 GPT-4V），跨模态对齐
        Complex task handling: managing multi-round dialogues, analyzing long documents, and mathematical reasoning (such as Wolfram integration)
        复杂任务处理：管理多轮对话、分析长文档以及数学推理（例如 Wolfram 集成）

        5. Security and Controllability
        5. 安全性与可控性
        - Content Safety: Output Filtering (Moderation API), Sensitive Word Detection
        - 内容安全：输出过滤（Moderation API）、敏感词检测
        - Controlled Generation: Constrained Decoding, Guardrails
        - 可控生成：受限解码、护栏机制
        - Ethical Issues: Hallucination Suppression, Bias Mitigation
        - 伦理问题：幻觉抑制、偏见缓解

        6. Industry Solutions   6. 行业解决方案
        - Vertical Domain Agent: Customer Service (Intent Recognition + Work Order System), Programming Assistant (Code Interpreter), Data Analysis (SQL Generation + Visualization)
        - 垂直领域代理：客服（意图识别 + 工单系统）、编程助手（代码解释器）、数据分析（SQL 生成 + 可视化）
        - Enterprise Deployment: Privately Deployed Models (Llama2, Qwen), Permission Management, Audit Logs
        - 企业部署：私有部署模型（Llama2、Qwen）、权限管理、审计日志

        IV. Points for Practical Ability Assessment
        IV. 实操能力考核要点
        9. Coding and Debugging  9. 编码与调试
        - Required Algorithms: String Processing (e.g., text chunking), Recursive Task Decomposition, Prompt Template Engineering
        - 必要算法：字符串处理（例如文本分块）、递归任务分解、提示模板工程
        - Typical Issues:  - 典型问题：
        - Implement an API call tool with a retry mechanism
        - 实现带重试机制的 API 调用工具
        - Design of a Long-Term Memory Module Based on RAG
        - 基于 RAG 的长期记忆模块设计
        - Optimize the inference speed in long context scenarios
        - 在长上下文场景中优化推理速度

        10. **Scenario Design**   10. **场景设计**
        - Design a travel planning Agent (integrating weather APIs, mapping services, and recommendation systems)
        - 设计一个旅行规划代理（整合天气 API、地图服务和推荐系统）
        - Strategies for follow-up questions when handling user vague requests (Clarification Questions)
        - 在处理用户模糊请求时的后续提问策略（澄清问题）
        - Implementing multi-Agent collaboration (such as delegating tasks to expert models)
        - 实现多智能体协作（例如将任务委派给专家模型）

        V. Preparation for Trendy Dynamics
        V. 面向潮流动态的准备
        - Latest Technology: Real-time Interaction Capabilities of GPT-4, MoE Architecture of Mistral, and LPU Inference Chip of Groq
        - 最新技术：GPT-4 的实时交互能力、Mistral 的 MoE 架构，以及 Groq 的 LPU 推理芯片
        -Hotspot directions: AI Intelligent Agent Operating System (such as Microsoft AutoGen Studio), AI Society Simulation
        - 热点方向：AI 智能体操作系统（例如 Microsoft AutoGen Studio）、AI 社会模拟
        - Open Source Ecosystem: OpenAI Assistants API, Meta Llama 3 tool calling capability, HuggingFace Agent
        - 开源生态系统：OpenAI Assistants API、Meta Llama 3 的工具调用能力、HuggingFace Agent
        """

4. 为什么说大模型训练很难？ - bigpunch
   https://www.zhihu.com/question/498271491/answer/1981120245616906843
    1. Very good summary. Author in field in depth. 大模型训练的本质不是“堆显卡”，而是一个在“超大规模分布式系统 + 不稳定硬件 + 黑盒算法 + 海量脏数据 + 長反馈周期”五重不确定性之上的极限系统工程。
        1. ChatGPT summary: https://chatgpt.com/c/693603ea-8760-8324-a20a-33ef2a4abd01
    
    2. Highlights
        1. 大规模并行下的计算效率崩塌
            1. 核心问题
                几千张卡 ≠ 几千倍算力
                通信（AllReduce / 梯度同步）迅速吞噬算力
                实际：
                    监控：GPU 利用率看起来很高
                    实际：MFU 只有 30% 不到
                    结论：70% 的钱在等通信
            2. 关键技术对抗
                Megatron-LM
                    Tensor Parallelism
                    Pipeline Parallelism
                FlashAttention V2
                    本质是：把“显存 IO”这个瓶颈压榨到极限
                    不上 FlashAttention → 训练成本直接翻倍
        
        2. 硬件不可靠性 = “大规模集群是一个必然出错的系统”
            1. 在 3000 卡以上规模：“硬件出错不是异常，而是常态”
               大模型训练是“带物理故障概率的长时间连续精密实验”。
            2. 真实故障清单（非常真实）：
                    IB 网卡掉线
                    光模块烧毁
                    GPU ECC Error
                    PCIE 插槽松动
                    空调异常 → 局部过热 → 降频
                    单卡慢 → Straggler 拖慢全局
                后果：
                    一张卡异常 → 整个训练 卡死 / 降速
                    半夜报警 → 工程师爬起来查日志
                    最终发现：物理层问题
                工程应对核心：
                    容错机制
                    Checkpoint 策略
                    热替换节点
                    异步存盘
                但这里的矛盾是：
                    太频繁Checkpoint   IO 打爆 + 性能下降
                    太少Checkpoint    一次故障损失几十万

        3. 数据工程：不是“有几PB数据就能练”
            1. 原文这段是标准行业共识，非常重要：
                数据 ≠ 石油
                数据 = 含沙、含硫、含重金属的原油
                现在公认的结论是，模型效果好不好，一半看架构，一半看数据质量。
                数据工程不是“清洗”，是“工业级原料提纯”。
            2. 三个数据核心难点：
                极致去重（防止模型“背书”）
                    MinHash / SimHash, 分布式跑
                    目的：
                        防止复读
                        防止记忆污染
                        防止泛化能力崩塌
                ② 数据配比是“玄学 + 工程试错”
                        代码多 → 推理强，语言变死
                        小说多 → 文采好， hallucination 增加
                        论文多 → 知识性强，表达僵硬
                    LLaMA 3 报告的重点：
                        Up-sampling 策略
                        Eval 集严格剔除
                ③ 数据污染（最隐蔽、最致命）
                    测试集混进训练集
                    榜单虚高, 实际上线翻车
                    要从 几万亿 token 里剔除几千条 eval 数据

        4. 算法调参是“长反馈黑盒赌博”
            小模型：
                调个 LR、Batch
                半天知道效果
            大模型：
                改一个超参 → 两周后 才知道是对是错
            恐怖问题：Loss Spike
                Loss 突然心电图一样暴冲
                常见原因：
                    坏数据
                    梯度爆炸
                    BF16 精度溢出
                真实补救方式（非常血泪）：
                    人工回滚 Checkpoint
                    跳过坏数据
                    降低学习率
                    一点点“哄”模型走回来

        5. 评估难：Loss / 榜单 全都不靠谱
            评估方式    问题
            Loss    不等价于生成质量
            C-Eval / MMLU   被严重刷榜
            人工评估    准但贵、慢
            Model-as-Judge  有偏差

            行业真实现状：
                各家都有：
                    私有评估集
                    来自真实业务
                    严格保密
                  - 这才是真正的 护城河
                相对公开可研究的：
                    LMSYS Chatbot Arena
                    Elo 体系
                    盲测

        6. 最终难点：复合型人才极度稀缺
            会 PyTorch 的很多, 但真正稀缺的是懂：
                CUDA
                NCCL
                InfiniBand 拓扑
                分布式系统
                Transformer 架构
                Shell + Python 混合 Debug
                千卡级故障定位

5. Azure Storage innovations: Unlocking the future of data
   https://azure.microsoft.com/en-us/blog/azure-storage-innovations-unlocking-the-future-of-data/
    1. Very good. showcase what a strong performance product and AI vision-er should do
    2. Highlights
        1. OpenAI large scale account, EB capacity, 10s of Tbps, 50 Tbps read throughput 
        2. Azure Managed Lustre (AMLFS)
        3. Microsoft Foundry Agent Knowledge
        4. AI Search retrieval agents
        5. LangChain Azure Blob Loader
        6. Storage Discovery and Storage Actions
        7. Azure Elastic SAN
        8. Smart Tier on Azure Blob Storage
        9. Azure Ultra Disk
        10. Performance, cost, business continuity
            Azure Boost, Instant Access Snapshots
        11. Azure NetApp Files (ANF)
        12. Storage Migration Solution Advisor
            Azure Data Box and Storage Mover
        13. Azure Files
            ANF Migration Assistant 

6. Deep Research in ChatGPT
    1. Open‑Source “Deep Research” AI Assistants
       https://medium.com/@leucopsis/open-source-deep-research-ai-assistants-157462a59c14
        1. Open Deep Research
           https://github.com/langchain-ai/open_deep_research
            1. How it works
            """
            Open Deep Research uses a multi-agent architecture to break down tasks. There is a “research supervisor” agent that can split a complex query into subtopics and spawn multiple sub-agents in parallel, each focusing on a sub-question. These sub-agents perform the search and reading for their topic and then return findings with citations. The supervisor agent then decides if more digging is needed or if all subtopics are sufficiently covered, and finally orchestrates the writing of the comprehensive report. This design, described in the project’s documentation, mirrors how Google’s Gemini handles research - parallelizing work across subtopics - and it lets the system scale to really complex queries. The final output is a well-structured report (e.g. with an introduction, sections per subtopic, and a list of sources) that cites all the information used.
            """

    2. DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents
       https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard

7. 为什么几乎所有教科书上对微分的讲解都不明不白？ - bigpunch的回答
   https://www.zhihu.com/question/438795295/answer/1989001841367864615
    1. Very good insights. 
        1. NN is multi-dimensional => multi-dimensional function (vector to vector), differential is fundamental different from one dimensional.
        2. Jacobian matrix is the 导数 of vector to vector function
        3. 
    2. See https://chatgpt.com/c/695272b1-6738-8322-8dc7-85d9fdeadc8a

    n. Related materials
        1. 有哪些复杂度为O(1)的神奇算法？ - bigpunch
           https://www.zhihu.com/question/52968810/answer/1993650765001147880
           https://www.zhihu.com/people/bigpunch-46
            1. Very good . This author is extremely valuable

        2. Neural Ordinary Differential Equations    [2018, 8450 refs]
           https://arxiv.org/pdf/1806.07366

        3. Book: Deep Learning by Ian Goodfellow etc
           https://www.deeplearningbook.org/
            1. Highly recommended book, only need to read 
               第一部分数学基础 - 线性代数、概率论、数值计算的基础 - 流形学习

8. MiniMax-M1 技术报告解读
   https://zhuanlan.zhihu.com/p/1922752810816090506
    1. Lightning Attention
       https://zhuanlan.zhihu.com/p/1920800829725709333

9. Manus AI
    1. Official intro
       https://www.youtube.com/watch?v=K27diMbCsuw
        1. Very good. This is amazing
    2. 深度理解Manus AI Agent - 三白有话说
       https://zhuanlan.zhihu.com/p/28976348679
        1. Useful summary and deep dive
    3. Manus核心Context技术被人做成了Skills
       https://zhuanlan.zhihu.com/p/1993358891099111451
        1. planning-with-files
           https://github.com/OthmanAdi/planning-with-files
        2. Very good. This is break through of Agent building technology. Even it is not hard to copy.
        3. Highlights
            1. Key technologies
                1. 文件系统作为外部记忆 (Filesystem as External Memory)
                   原理：不要依赖易失的Context Window。将磁盘视为无限的“外挂内存”，只在Context中保留文件路径。
                2. 通过重复进行注意力操纵 (Attention Manipulation Through Repetition)
                   原理：对抗“Lost in the Middle”。在关键决策前反复读取计划文件，强行刷新模型的“注意力权重”。
                3. 保留失败痕迹 (Keep Failure Traces)
                   原理：错误是宝贵的资产。显式记录失败尝试，让模型通过“反思”避免死循环，而不是掩盖错误。
                4. 避免少样本过拟合 (Avoid Few-Shot Overfitting)
                   原理：在重复性任务中引入受控变体，防止模型陷入机械式的幻觉。
                5. 稳定前缀优化缓存 (Stable Prefixes for Cache Optimization)
                   原理：通过固定的文件结构和前置指令，最大化KV-Cache命中率，降低Token成本。
                6. 只增不改的上下文 (Append-Only Context)
                   原理：尽量以追加（Append）而非修改（Modify）的方式更新信息，维护上下文的连贯性。

        4. 三个file哪里够啊，试试我的，我弄了三层
           https://github.com/MasterGodzilla/Memory-System

    4. 让 AI 学会「专家级思考」的 Agent 开发框架 LoongFlow 开源发布 - 百度智能云
       https://zhuanlan.zhihu.com/p/1996151316955820602
        1. Interesting design that reveals an industry level agent
        2. Highlights
            1. Plan-Execute-Summarize
                1. planner agent, execute agent, summary agent
                2. Evaluator (evaluator function)
                3. Database (evolution memory)
            2. The evolution tree & global memory
                1. Interesting. Planner inspects history failure history before making the plan
                2.  Interesting. 多岛模型：它在内部建立多个独立的「探索特区」，允许不同的技术路线并行发展，相互隔离又定期交流，有效维持了探索的多样性，避免思维过早趋同。

    5. 破解二十亿美元的秘密：从 Manus 到 Planning-with-Files - 不亦乐乎
       https://zhuanlan.zhihu.com/p/1994868451479679799

    6. "Plan and Execute" AI agent
        1. LangGraph: Build a "Plan and Execute" AI Agent Workflow with LangGraph
           https://www.youtube.com/watch?v=8NYLEzJiDcQ
        2. LangChain blob: Plan-and-Execute Agents
           https://www.blog.langchain.com/planning-agents/

10. 为什么Claude的代码能力会这么强？ - 小雅的回答 - 知乎
    https://www.zhihu.com/question/1914086301076029991/answer/1951779221312627388
    https://minusx.ai/blog/decoding-claude-code/#appendix
    1. Very good. Thanks the original author.
    2. Highlights
        1. Not multi-agent. Fork itself. max-1-branch
        2. Maintain a todo list
        3. Use small model claude-3-5-haiku for as much as possible
        4. claude.md
            1. Always included: Entire claude.md contents sent with every request
            2. Auto generated, human tunnable 
        5. Special XML Tags, Markdown, and lots of examples
        6. Per code reading, LLM search is much better than RAG based search
        7. Write the Algorithm (with heuristics and examples)
        8. System prompt: ~2,800 tokens
           Tools descriptions: 9,400 tokens
           Context file (claude.md): 1,000-2,000 tokens per request
    
    n. Related
        1. What Makes Claude Code So Damn Good: A Deep Analysis
           https://cc.deeptoai.com/docs/en/advanced/decoding-claude-code-analysis

        2. Over 200 instructions, instruction-following quality decreases quickly
           https://www.humanlayer.dev/blog/writing-a-good-claude-md
            1. Useful finding. See the chart.

11. ClawdBot / MoltBot - Your private AI agent (like Manus but opensource local deploy)
    1. Clawdbot 如何记住一切 / 解析的记忆系统 - 段小草
       https://zhuanlan.zhihu.com/p/1999506236597637279
       https://manthanguptaa.in/posts/clawdbot_memory/
        1. Highlights
            1 .memory_search tool
        n. Related materials
            1. Manthan: I Reverse Engineered ChatGPT's Memory System, and Here's What I Found!
               https://manthanguptaa.in/posts/chatgpt_memory/
                1. Every message includes your stored memory facts (~33 items)
                2. User message snippets history
                3. Not using RAG nor vector database
            
            2. Manthan: I Reverse Engineered Claude's Memory System, and Here's What I Found!
               https://manthanguptaa.in/posts/claude_memory/
                1. Fundamentally different ChatGPT. 
                    1. Claude uses on-demand tools and selective retrieval
                    2. For conversation history, Claude doesn't use pre-computed summaries
                2. Approach to reverse engineer Claude's memory
                    1. Ask Claude to describe its own prompt structure.
                    2. Probe each section independently (memory, history, tools).
                    3. Cross-check answers by re-asking the same questions in different ways.
                    4. Look for consistency across responses.
                    5. Validate claims by testing behavior (e.g., storing and deleting memories).
                3. Highlights
                    1. Tools: 
                        1. memory_user_edits
                        2. conversation_search 
                        3. recent_chats 
    
    2. Clawdbot/moltbot Clearly Explained (and how to use it)
       https://www.youtube.com/watch?v=U8kXfk8enrY
        1. Key Points
            1. I get the most leverage when I treat the agent like a proactive teammate with clear expectations and rich context.
            2. Henry delivers compounding value by shipping work for review (pull requests) based on trend monitoring and conversation memory.
            3. I separate “brain” and “muscle” by delegating heavy coding to Codex while using Opus for reasoning and direction.
            4. I track autonomous work with a dedicated “Mission Control” board so progress stays visible over time.
            5. I keep risk contained by controlling environment and account access, especially around email and prompt injection.

        2. Alex's prompt: "I am a 1 man business. I work from the moment I wake up to the moment I go to sleep. I need an employee taking as much off my plate and being as proactive as possible. Please take everything you know about me and just do work you think would make my life easier or improve my business and make me money. I want to wake up every morning and be like "wow, you got a lot done while I was sleeping." Don't be afraid to monitor my business and build things that would help improve our workflow. Just create PRs for me to review, don't push anything live. I'll test and commit."

    3. 开源 AI 助理 Clawdbot 获 Karpathy 点赞，它究竟是什么，有何亮点？ - Tableau
       https://www.zhihu.com/question/1998931277835941056/answer/1999543975586075023
        1. Key technologies
            1. 大脑：Claude Opus 4.5 的“长程推理”
            2. 交互革命：A2UI (Agent to UI)
            3. 灵魂与记忆：SOUL.md 与 向量数据库
            4. 技能超市：ClawdHub

    4. Clawdbot: How Your Personal AI Assistant Actually Works - Prateek Kumar
       https://medium.com/@prateek.dbg/clawdbot-how-your-personal-ai-assistant-actually-works-919a454d2b5c

    5. How Clawdbot Remembers: A Deep Dive into AI Agent Memory Architecture - Avasdream
       https://avasdream.com/blog/clawdbot-memory-system-deep-dive
        1. ClawdBot memory system: Markdown + SQLite vector index + auto-flush
        2. Search "The Full Memory Lifecycle" in article

    --------

    6. Installing Clawdbot
        1. Deploying Clawdbot on Azure VM
           https://wilsonwu.me/en/blog/2026/clawdbot-on-azure/
        2. Deploying Clawdbot/Moltbot/OpenClaw Gateway Securely to Azure Container app with Azure Storage Fileshare
           https://suresh42326.medium.com/deploying-clawdbot-moltbot-openclaw-gateway-securely-to-azure-container-app-with-azure-storage-8e4f9ecdc209
        3. Clawdbot: the full setup in 30 minutes
           https://www.reddit.com/r/ClaudeCode/comments/1qnj0lz/clawdbot_the_full_setup_in_30_minutes/
        4. OpenClaw
           https://github.com/openclaw/openclaw
           https://docs.openclaw.ai/start/onboarding

        5. ClawdBot official
           https://openclaw.ai/
            1. One-liner: `curl -fsSL https://openclaw.ai/install.sh | bash`
            2. Must read: https://docs.openclaw.ai/gateway/security  

        6. Master OpenClaw/Clawdbot in 35 minutes
           https://www.youtube.com/watch?v=4evf5YqVzOM
            1. Useful in-depth usage

        7. Pay and get OpenClaw ready 
           https://myclaw.ai/
        8. How I Connected OpenClaw to Gmail (Beginner Step by Step Guide)
           https://www.reddit.com/r/SaaS/comments/1qz0nkw/how_i_connected_openclaw_to_gmail_beginner_step/

    ------

    7. Deep dive into OpenClaw
        1. Under the Hood: How Clawdbot Works
           https://o-mega.ai/articles/clawdbot-the-ultimate-guide-to-your-personalized-ai-agent-2026
        
        2. A Detailed Breakdown of Clawdbot's 4 Core Advantages
           https://help.apiyi.com/en/clawdbot-beginner-guide-personal-ai-assistant-2026-en.html#:~:text=Traditional%20AI%20chats%20usually%20start,Clawdbot%2C%20however

        3. 我扒开了OpenClaw(Clawdbot)的底层架构，发现它远比想象中简洁 - Draco
           https://mp.weixin.qq.com/s/naaoSKUaxUIzW4HafGoSwQ
           https://x.com/Hesamation/status/2017038553058857413
            1. Useful.
            2. Highlights
                1. Browser: Semantic Snapshots - from Playwright
                    1. Playwright -> Chrome CDP -> Accessibility Tree
                    2. Google search AI: https://share.google/aimode/MPErgzhUNjujVWor4

        4. OpenClaw技术原理 - 赛博味儿酒咖
           https://zhuanlan.zhihu.com/p/2001963895926044536

    8. My questions / summary
        1. I finished Clawdbot (now OpenClaw) study. Its system prompt is visible in code or you can just ask the agent.
            1. Core technologies:
                1. Agent loop: Reusing github.com/badlogic/pi-mono
                2. File read/write tool: Reusing github.com/badlogic/pi-mono
                3. Browser control: Reusing playwright which was invented for browser testing
                4. Vector embedding store: SQLite

            2. I don't think OpenClaw code base forms any moat. It is a typical Agent App. Today's AI coding can quickly replicate it (possibly 1 dev 3 months). Most components are standard and have reusable parts in github.

            3. A typical Agent App ships with:
                1. Agent loop (e.g. ReAct). Core tools (e.g. file access). 
                2. Memory with files, SQLite embedding store, RAG search.
                3. Multiple agents, each defined by its profile, and allow one agent to call another.
                4. Session management, persisted in files, and allow an agent to view/fork/start sessions.
                5. Install custom skills. Install custom tools. Access external MCP servers.
                6. Messaging/email with user, typically OpenClaw's Whatsapp/Telegram integration.
                7. Make plans and exuecte sub-tasks. Handle task errors and validation.
                8. A scheduler for longterm or periodical tasks, typically a cronjob.
                9. A UI portal for user interaction and management.
                10. Integration with your company wide database, knowledge base, documents, tooling, etc

        2. Future app development paradigm
            1. App development cost and available becomes much much more reachable to everyone.
               Probably not everyone would build their own customized app, but possible many will.
               AI coding will be your dev, you will have to be a good manager product manager.
               You should still need certain level of software developer knowledge, just like today's managers. 

    ------

    8. Setting up email for ClawdBot
        1. PSA: Gmail will nuke your Openclaw agent without warning. Here's what happened.
           https://www.reddit.com/r/AI_Agents/comments/1r1cf1j/psa_gmail_will_nuke_your_openclaw_agent_without/
            1. Google by design kills openclaw. Use AgentMail

12. Storage & AI updates posted from Clawdbot
    1. Reducing TCO for AI inferencing with external KV Cache on Managed Lustre
       https://cloud.google.com/blog/products/storage-data-transfer/choosing-google-cloud-managed-lustre-for-your-external-kv-cache
        1. Good. Cloud Storage is entering new AI area.
           Previously, checkpoint, training data loading.
           New, KV cache external hosting.

    2. LMCache on Google Kubernetes Engine: Boosting LLM Inference Performance with KV Cache on Tiered Storage
       https://blog.lmcache.ai/en/2025/10/07/lmcache-on-google-kubernetes-engine-boosting-llm-inference-performance-with-kv-cache-on-tiered-storage/

        n. Related materials
            1. Boosting LLM Performance with Tiered KV Cache on Google Kubernetes Engine
               https://cloud.google.com/blog/topics/developers-practitioners/boosting-llm-performance-with-tiered-kv-cache-on-google-kubernetes-engine

13. 小团队，如何降低Google的Gemini 3 Pro, Nano Banana 消耗的TOKENS？ - 跑酱er
    https://www.zhihu.com/question/2000645307021689319/answer/2003061813013673399
    1. Useful
    2. Highlights
        1. 模型路由函数，由Nano先判断用户意图，标准任务不需复杂模型
        2. Context Caching, extremely useful in RAG
        3. Prompt Compression, 精简用语，Prompt去水
        4. Semantic Cache, 直接返回已有答案，无需发送Token给Google
           把那些重复的、低价值的请求拦截在云端之外

14. Vibe Coding 一年实践后的冷思考 - 小明
    https://zhuanlan.zhihu.com/p/2003390589538956495
    1. 最近一年我在 Google/Anthropic/OpenAI 三家烧了超过 1 万美金的 token 账单。
       所以本文内容基于 opus4.6 、codex-5.3-xhigh 、gemini3-pro 等最强模型不限量使用所表现出来的编码能力进行评价。
        1. Interesting
    2. Highlights
        1. 原因：验证手段的全面失效
        2. Agent 编程时代，更需要强类型，更需要严格可验证的语言，而不是放任 agent 去写 python/js/java/go ，还有 anyscript 。
        3. 实际上现在的 formal method 工具链和生态还是很贫瘠，基本上只支持一门语言很有限很小的一个子集。
        4. 更深的困境：Plan 与 Execute - 这不是代码写错了，而是路线选错了。

15. Google L4 Cache at Colossus, see algorithm at CacheSack
    https://mp.weixin.qq.com/s/U3d-xc7asmm3iW0deYIU_w
    https://cloud.google.com/blog/products/storage-data-transfer/how-colossus-optimizes-data-placement-for-performance
    https://www.usenix.org/system/files/atc22-yang-tzu-wei.pdf
    1. Good. This is right to point a direction of the new evolve direction of cloud storage.
    
    2. CacheSack: Admission Optimization for Google Datacenter Flash Caches    [2022, 29 refs, ATC22]
       https://www.usenix.org/conference/atc22/presentation/yang-tzu-wei
    
    3. Google Colossus文件系统技术详解 - 贺大伟
       https://zhuanlan.zhihu.com/p/1994723519326606184
        1. Good. The summary includes incredible completeness from fragments of disclose even Colossus never released a full apper

16. 如何有效地给 10 个 Claude Code 打工 - 胡渊鸣
    https://zhuanlan.zhihu.com/p/2007147036185744607
    1. Interesting. "CEO 支持软件"

17. 揭秘 GeminiFS (FAST 2025) 的论文诞生与作者成长之路 - 存储前沿技术评论
    https://mp.weixin.qq.com/s/pbeeogrsK1bKA8FfvAWl8A
    1. GPUDirect Storage (GDS) 在I/O数据面绕过CPU，BaM进一步在控制面绕过CPU，而GPU文件系统在此基础上提供文件抽象。这背后的核心驱动因素是减少I/O处理软件开销，包含CPU与GPU之间的同步开销和CPU软件栈开销。这些开销在小I/O负载下十分凸显。然而，GPU采用高并行的计算架构，只有输入大量数据才能发挥它的带宽优势，GPU应用的设计原则应该是尽可能生成大尺寸I/O请求。那么，哪些GPU应用场景包含大量小I/O请求？以及，大I/O负载下软件处理开销相对低，GDS的性能表现如何，bypass CPU是否必要？
        1. 现在AI场景下，GPU访存主要的需求可能有训练数据集，KV Cache/RAG，checkpoint。其中Checkpoint的I/O粒度通常比较大，且并发度并不大，GDS/GDR也可以有较好的性能，并不需要bypass CPU。训练数据集的大小一般是是几十KB到几百KB，已经算是比较小的I/O了。因此许多工作会将许多输入压缩成一个大文件传输。在训练这种可以预加载的场景还是比较有效的。

        而KV Cache是典型的小I/O负载，KV矩阵的大小受到模型设计、量化策略以及并行计算策略等策略影响比较大。而且，目前主流的LLM推理框架（如vLLM、Sglang）为提高计算效率和减少内存碎片，都会采用内存分页的方式将GPU内存分成固定大小的页。然而，在这种内存布局下，将一段逻辑上连续的KV换出到NVMe上时，内存碎片会转化为IO碎片。以一个64层的模型为例，如果要换出128K长度的KV，需要传输的内存对象的数量为2*64*128K。即使将多个token（比如16）合并成一个Block，就会造成上百万的离散小I/O。

        现在高效的传输放啊通常是利用GPU kernel进行数据聚合然后内存拷贝，最后再写回SSD，仍然会有一定的传输与操作开销，导致GPU阻塞。在较长的KV传输场景下，CPU控制开销是十分巨大的，在这种情况下就非常适合将控制路径卸载到GPU上。

        GDS有限的并行性肯定是完全无法适应这样的负载的，其GDS较大的控制开销以及有限的并行性反而会导致较差的性能。另外大家可以关注一下我们NICELAB最新的工作Phoenix SC'25，对现有的GDS框架进行了优化，实现了并发性能的大幅提升。

        除了AI，典型的应用是GNN，GPU对于边的访问一般也都是小I/O。

18. Leetcode 218: 城市天际线 - Given an array of building rectangles, output the city skyline
    https://leetcode.cn/problems/the-skyline-problem/description/
    1. My solution
        1. Observations
            1. Sorting the input building list helps, but it has cost
            2. A new building only changes the overlapping ones from the existing builds
            3. Insert a new building is equivalent to reverse: assume new building is there first, and then insert overlapping builds again
            4. We don't need to track existing builds, we only need to track the city skyline to handle new insert buildings
            5. Inserting a new building is localized, it only affect the the node that overlaps with it. This makes operating data structure simpler
            6. Inserting a new building can be handled recursively, just poke out of first overlapping part, then recursively handle the remaining.
            7. Each building's start/end point together are the max possible cardinality of city skyline, then next problem is just to merge them.
            8. Instead pixel, we only need to track as fine grain resolution as the cardinality of points, not really per pixel
        
        2. Solution 1: Simplest solution
            1. Maintain city skyline as an ordered linked list
            2. Find the city skyline segment that is overlapping with the left point of the new building
               Cut the new building line into two, part A that is within the segment, and part B that is out of the segment.
               Handle Part A below. And then recursively handle the part B.

                1. Case 1: Segment not found
                    1. Just insert Part A. 
                2. Case 2: Segment found
                    1. Part A is higher
                        1. Part A can break the segment up to 3 consecutive parts. Create them and reinsert.
                    2. Part A is lower
                        1. Ignore

            3. Optimization, track the last position to resume scan, when recursively handling part B.

        3. Solution 2: Use tree for ordering and quick insert
            1. Something similar to range tree, but we can simply index by the left point of each segment in the city skyline, because we know the segments are not overlapping
            2. We need an algorithm to, given a segment, find its next segment, and next next segment.
                1. if the segment has right child, it is the right child
                   if not, go upwards till the first time you come from a left child.
            3. Others are same with Solution 1

        4. Solution 3: Pixel solution
            1. The problem is pretty like a game. Formulate the X axis as pixel. Each pixel occupies a slot in array. When inserting a new building, directly go into each overlapping pixel and update. It is O(1)
            2. The problem is, one pixel is possible to have to hold two segments, each segment only partially occupy the pixel.
                1. In this case, fallback to solution 2 or solution 1 inside this pixel.
            3. Pixel is similar to using a hashmap. And using solution 2 or 1 to resolve collision.  

        5. Solution 4: Pixel slot + sub-level pixel
            1. Unlike solution 3, upon conflicts in a pixel slot, use another level of pixel solution to resolve the conflict.
            2. In the sub-level, the precision can result into a huge number of slots. Use lazy allocation, use a tree to index

        6. Public solution: https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0218.The%20Skyline%20Problem/README_EN.md
            1. Python solution
                1. Break apart each building's start/end point, put into a list and sort
                2. Per each start/end point, scan all builds that possibly overlap with this point
                3. sort buildings scanned from higher to lower. take its height
                4. merge into the city skyline, skip if the current height is equal to the last segment
            2. C++ solution
                1. Break apart each building's start/end point.
                   Sort point by its location at X axis. Dedup the points by set.
                   Given each point an index i (after sorted)
                2. Create a map highs[i] to track given a point, what is its max height
                3. Merge all points to create the city skyline

        7. Solution 5: Use point instead of Pixel
            1. You don't need to track height at each pixel. You only need to track height at each building left/right point.
                1. The max resolution needed is not pixel, but the each building point instead
            2. Then, the solution is super simple:
                1. Break apart a building's left/right point
                2. organize a linked list or tree to host the points and maintain sorted
                3. Gradually insert new building one by one, each insert should update all points height within building left/right
                4. In the end, scan points ordered left to right, merge and output city skyline

            3. Solution 2 is actually very close
                1. The tree only needs to track a point rather than a line segment
                2. Each new insert is inserting a new point if the point's height is higher
                   Then it goes to the immediate next tree node (std::map iterator)
                   and recursively update the height again

        n. My questions - My thinking on Leetcode
            1. A person with A) good problem analytics skill but B) slow to write code or syntax, can be filtered out in a leetcode test. 
               This is NOT reasonable. (A) is the skill extremely important in real work. (B) is a cheap skill even before the age of AI.
            
            2. In a Leetcode test, the code has to be short. It has to try best to leverage existing say C++ data structures like std::map, std::set, std::vector.
               But this is wrong in real project. We need deeper understanding and frequently customize the data structures to exploit the most.
               Solutions based on STL containers are not the best solutions. And a person who is too much trained to solve a problem by layering up STL containers may not write the best code in real project.
            
            3. The ability to A) clarify a fuzzy problem and to B) think at the scope boundary are extremely important in real work.
               But, Leetcode problems have to be defined without fuzziness. A person trained on it lost skill at (A). 
               Also, Leetcode frequently make simplification on the problem, inputs, and scale of data. A person trained on it lost skill at (B).

19. Leetcode 807: 保持城市天际线 - n*n 整数格上的建筑物高，东南西北观测天际线，问最大可能增高且不影响天际线
    https://leetcode.cn/problems/max-increase-to-keep-city-skyline/description/
    1. Simple. each building can grow by "min(row max, column max) - self height"

21. THE 2028 GLOBAL INTELLIGENCE CRISIS - Citrini Research.pdf
    https://www.citriniresearch.com/p/2028gic
    1. Very good, how AI can re-shift many industry
        1. SaaS companies are facing drastic change, which is already happening
        2. Companies that act as middle mediator layer or to handle trade frictions are facing replacement. Because AI agent doesn't care about friction, doesn't maintain lazy-habit like human.
        3. Banks and financial are facing impact, because AI agents trade bypassing them directly with cryptocurrency

22. Blob vector index at cloud scale storage
    1. AWS S3 vector
        1. Amazon S3 Vectors — Native Vector Storage in Amazon S3 for AI/ML Applications
           https://jtanruan.medium.com/amazon-s3-vectors-native-vector-storage-in-amazon-s3-for-ai-ml-applications-8e8be3840e41
            1. Store documents in S3, create vectors in S3 vector bucket, auto index
        
        2. AWS S3 Vectors | Cost-optimized AI-ready storage | query vectors at scale, reduce costs up to 90%
           https://www.youtube.com/watch?v=9a027daACJk

        3. Tutorial: Getting started with S3 Vectors
           https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-getting-started.html
            1. 用户可以创建特定的 bucket 以启用 vector 向量索引。
            2. 让用户自己插入插入向量，自己选择向量值。这样绕开了额外的 CPU/GPU 资源需求 (AWS S3)。
               除非用户用工作流使用专用的 ML 服务来生成向量。当然 ML 服务费另付。

        4. Will Amazon S3 Vectors Kill Vector Databases—or Save Them?
           https://zilliz.com/blog/will-amazon-s3-vectors-kill-vector-databases-or-save-them
            1. Blob source: Zilliz Cloud is a fully managed Milvus vector database service
                1. Good article with distinctive insights about vector index
            
            2. A Surprising Fact: Vector Storage Can Cost More Than LLM Calls
                1. Latency tolerance shifted: Since LLMs take time to generate responses anyway, users became more forgiving of slightly slower retrieval. The “sub-10ms recall at all costs” mindset suddenly mattered less.
                2. Cost sensitivity skyrocketed. Massive data explosion.
            
            3. I’ve seen vector databases go through three distinct stages: From Memory to Disk, and Now to Object Storage
                1. Phase I (2018–2022): The Pure Memory Era: In the early Milvus days, we leaned on memory indexes like HNSW and IVF. The performance and recall were fantastic—but the costs were brutal.
                2. Phase II (2022–2024): The Disk Index Revolution: To break the memory bottleneck, we pioneered a disk-based approach using DiskANN along with our proprietary Cardinal index (exclusive to Zilliz Cloud, the managed Milvus). With tricks like asynchronous I/O (AIO) and io_uring, we managed to squeeze real performance out of disks.
                3. Phase III (2024– ): The Tiered Storage Era: The next step was obvious: push vector indexes onto cheap object storage. New players like TurboPuffer went all-in on S3, dropping storage costs to ~$0.33/GB/month—a 10x reduction.
            
            4. hypothesis of how S3 Vectors works under the hood - This is very good
                1. SPFresh Dynamic Indexing
                2. Deep Quantization (4-bit PQ)
                3. Post-Filter Mechanism
                4. Multi-Tier Caching
                5. Large-Scale Distributed Scheduling
            
            n. My questions
                1. Why S3 vector "Write performance: Capped at under 2MB/s"? This is way too low to a blob storage. Is there a limitation to SPANN/SPFresh?
                    1. I guess vector insert is internally random writes, to different partitions
                    2. This means, a big future topic is how to introduce LSM-tree into the partition centroid level. Good, worth thinking.
                        1. OK .. LSM-tree vector index has recent researches
                            1. LSM-VEC: LSM-Tree Integrated Vector Index (2025)

    2. PostgreSQL pgvector
        1. pgvector实现分析 - 宋昭
           https://zhuanlan.zhihu.com/p/1928127841259745664
        
        2. 向量数据库与pgvector - xiongcc
           https://zhuanlan.zhihu.com/p/649779973
            1. Typical algorithm used -  HNSW
            2. HNSW - 向量组成neighbor图，图的"skip list"
            3. HNSW is a graph based algorithm. The vectors themselves don't have edge connection. HNSW adds edge connect according to distance.

        3. ChatGPT: https://chatgpt.com/c/69a45916-31ec-839c-8414-e9c0c25bc442
            1. pgvector uses HNSW algorithm. It is a postgresql plugin. 
               pgvector leverages pg to manage index pages. But what stores in the index page is defined by pgvector hnsw. 
            2. HNSW is an algorithm that structured as a graph. pgvector insert needs to update elements on disk and maintain graph links.
            3. The code is in https://github.com/pgvector/pgvector/blob/master/src/hnswinsert.c
               HnswUpdateConnection, AddElementOnDisk, UpdateNeighborOnDisk, ItemPointerSet
            4. pgvector stores the HNSW graph entirely within standard PostgreSQL 8KB pages, managed by the PostgreSQL buffer manager. There is no custom file I/O.

    3. CockroachDB 向量索引
       https://zhuanlan.zhihu.com/p/1996662932252156083
       https://www.cockroachlabs.com/blog/cspann-real-time-indexing-billions-vectors/
        1. C-SPANN (CockroachDB SPANN)
            1. SPANN: Highly-efficient Billion-scale Approximate Nearest Neighbor Search    [2021, 290 refs]
               https://www.microsoft.com/en-us/research/wp-content/uploads/2021/11/SPANN_finalversion1.pdf
                1. Problem to solve
                    1. Traditional ANN structures like HNSW or other graph/approx algorithms assume the entire index fits in RAM or large memory. But we need to handle billion-scale approximate nearest neighbor search (ANNS)
                2. Design
                    1. Hierarchical tree of K-means. Same with C-SPANN, except wording
                        1. posting lists -> cockroach C-SPANN partition
                           Hierarchical Balanced Clustering -> K-means with balancing
                        2. Store high level indexes in memory, store bottom partitions on SSD
                    2. Posting lists can be small, vectors inside are close and compact
            
            2. SPFresh: Incremental In-Place Update for Billion-Scale Vector Search    [2024, 87 refs]
               https://www.microsoft.com/en-us/research/publication/spfresh-incremental-in-place-update-for-billion-scale-vector-search/
                1. Problems to solve
                    1. Incremental update without full rebuild the index. At billion scale
                2. Design
                    1. LIRE Protocol — Lightweight Incremental Rebalancing
                        1. splits partition
                        2. reassigns a small number of boundary vectors (those near partition borders) to adjacent partitions to restore balance
            
            3. SPANN - 小分区的centroid组成的B+tree
        
        2. SIMD vector scan
        3. 分区的 split/merge, rebalance
            1. partition is internally done by "K-means tree", i.e. partition by distance
               In compare, KD-tree partitions the space recursively by axis-aligned hyperplanes, and KD-tree is a binary tree
            2. C-SPANN's core is the K-means tree
        4. 量化技术 quantization 减少索引规模
            1. RaBitQ - Random Bit Quantization
            2. RaBitQ: Quantizing High-Dimensional Vectors with a Theoretical Error Bound for Approximate Nearest Neighbor Search [SIGMOD 2024, 97 refs]
               https://arxiv.org/pdf/2405.12497
               https://github.com/gaoj0017/RaBitQ
               https://dev.to/gaoj0017/quantization-in-the-counterintuitive-high-dimensional-space-4feg
                // TODO

        n. ChatGPT: https://chatgpt.com/c/69a45916-31ec-839c-8414-e9c0c25bc442
            1. Very useful

        m. My questions
            1. Seems the CockroachDB C-SPANN article didn't mention transaction
            2. CockroachDB C-SPANN. looks very good. based on state of arts. the fundamental design is extremely simple, but quite adaptive to partition based distributed system. next, the SIMD speedup, quantization RabitQ pushes it to a new level. 

    4. Milvus Opensource Vector DB
        1. How is indexing done in a vector database?
           https://milvus.io/ai-quick-reference/how-is-indexing-done-in-a-vector-database
           https://milvus.io/ai-quick-reference/how-does-indexing-affect-the-speed-of-vector-search

        2. The Power of Vector Indexes in Milvus: Efficiency in High-Dimensional Data Search
           https://medium.com/@divya999/the-power-of-vector-indexes-in-milvus-efficiency-in-high-dimensional-data-search-5770ec91fd72

        3. ChatGPT: https://chatgpt.com/c/69a45916-31ec-839c-8414-e9c0c25bc442
            1. Milvus supported indexes: FLAT, IVF_FLAT, IVF_PQ, HNSW, DiskANN/SCANN/GPU
            2. DiskANN
                1. DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node    [2019, 542 refs]
                   https://www.microsoft.com/en-us/research/publication/diskann-fast-accurate-billion-point-nearest-neighbor-search-on-a-single-node/

            3. IVF_PQ / IVFPQ
                1. Product Quantization
                    1. Split a vector into sub-vectors by cutting dimensions. Replace sub-vectors by their nearest centroids, store only centroid index
                    2. Interesting, RoPE also works in sub-vectors by cutting dimensions. It rotates each 2D sub-vector
                       https://medium.com/thedeephub/positional-encoding-explained-a-deep-dive-into-transformer-pe-65cfe8cfe10b

    5. Faiss - Facebook AI Similarity Search
        1. an open-source C++ library with python bindings
        2. It includes a range of index structures (flat, IVF, HNSW, PQ variants), compression schemes, and GPU acceleration for high throughput
        3. Faiss’s IVFPQ index is widely used in billion-vector workloads because it balances memory efficiency, speed, and recall
        4. Faiss is Not designed for incremental updates, not a database
            1. Faiss indexes are static data structures with limited update semantics
            2. most Faiss indices don’t support removal or replacement of individual vectors without rebuildin
        5. Faiss itself was originally designed for in-memory indexes, but the project and ecosystem do offer techniques to scale beyond RAM
        6. GPU acceleration

    6. Turbopuffer
       https://turbopuffer.com/
        1. How Turbopuffer is Slashing Vector Search Costs by 90% with a Radical Architectural Shift
           https://www.linkedin.com/pulse/how-turbopuffer-slashing-vector-search-costs-90-radical-yadav-nqvlc/
            1. Top user - Cursor 
               https://turbopuffer.com/customers/cursor
            2. Turbopuffer's Solution: An Object-Storage-First Architecture
                1. Writes to Object Storage, typically AWS S3
                2. Smart Caching
                    1. A cache layer of NVMe SSDs and memory sits between the user and object storage
                    2. This layer holds the "hot" data, the indexes for vectors that are being actively queried.
                3. Intelligent Query Routing
            3. Key technologies of Turbopuffer
                1. inspired by SPFresh, Incremental Indexing 
                2. Syncing with Merkle Trees
                3. A Framework for Privacy by Design - Interesting
                    1. No Plaintext Storage: The service never needs to store the raw source code.
                    2. Client-Side Transformation: Code is transformed into numerical embeddings on the client or during a transient process.
                    3. Metadata Obfuscation: Sensitive metadata like file paths is obfuscated by the client before being stored in Turbopuffer.
        2. ChatGPT: https://chatgpt.com/c/69a45916-31ec-839c-8414-e9c0c25bc442
            1. Native Filtering for High Recall - Interesting
                1. Turbopuffer doesn’t just pre-filter or post-filter queries — it integrates attribute filtering with vector search by mapping attribute filters into cluster selection predicates.

    7. ChatGPT overall deep research
       https://chatgpt.com/c/69a4439f-b184-83a0-9d22-c5efadc01b84


    8. RaBitQ - Seems growing adopted in recent vector indexes
        1. RaBitQ: Quantizing High-Dimensional Vectors with a Theoretical Error Bound for Approximate Nearest Neighbor Search    [2024, 97 refs]
           https://arxiv.org/pdf/2405.12497
           https://www.ntu.edu.sg/innovates/tech-portal/tech-offers/detail/rabitq-estimating-unit-vector-positioning-ml-systems
           https://github.com/gaoj0017/RaBitQ
            1. A big improvement compared to PQ
            2. Highlights
                1. SIMD based batch vector scan
                2. Compared to PQ, advantages
                    1. Provides a theoretical error bound guaranteeing robust performance
                    2. Ensures accurate distance estimation compared to PQ
                    3. Utilises bitwise and SIMD-based operations for speed and efficiency
                    4. Demonstrates significant improvements on real-world datasets, including scenarios where PQ fails
                3. A random orthogonal rotation (via multiplicative random matrix) is applied to these basis vectors so that the binary basis covering is uniformly distributed across all directions.
                    1. Random rotation - remove bias from hyper cube axes (PQ has it)
                    2. orthogonal rotation - preserve inner product / geometric structure
                4. Computes distance estimates between query and database vectors using an unbiased estimator derived from the geometric relationship of the query, original vectors, and quantized codebook vectors.
                    1. I.e. the average of the estimates matches the true inner product exactly
                       it does not systematically over- or underestimate the true similarity
                       Unlike PQ
            3. ChatGPT: https://chatgpt.com/c/69a45916-31ec-839c-8414-e9c0c25bc442


23. 纠删码技术在vivo存储系统的演进【上篇】 - vivo互联网技术
    https://zhuanlan.zhihu.com/p/635624629
    1. Waiting for the 下篇

24. Copilot CLI and Claude Code
    1. Ralph Loop
       https://github.com/snarktank/ralph/blob/main/prd.json.example

    2. Git Worktree to enable parallel work
       https://www.reddit.com/r/ClaudeCode/comments/1pzczjn/git_worktrees_are_a_superpower_for_agentic_dev/
        1. An example of AI generated content that describes a simple thing in a faked complex way and pretend to be building something complex and pretend to be a well teacher. Caution here. 
       
    3. Git worktree is the biggest improvement
       https://stackoverflow.com/questions/31935776/what-would-i-use-git-worktree-for

    4. Claude Code supports for git worktree
       https://code.claude.com/docs/en/common-workflows

    5. OpenAI supports for git worktree
       https://developers.openai.com/codex/app/worktrees/
```
