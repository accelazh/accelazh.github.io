---
layout: post
title: "Recent Articles Reading: MCP, MLA"
tagline : "Recent Articles Reading: MCP, MLA"
description: "Recent Articles Reading: MCP, MLA"
category: "Paper Reading"
tags: [storage, cloud, AI]
---
{% include JB/setup %}

```
1. UB-Mesh: 基于统一互联和高维直连拓扑的AI集群架构 - 知返
   https://zhuanlan.zhihu.com/p/32978184612

2. Bing 搜索核心技术 BitFunnel 原理
   https://zhuanlan.zhihu.com/p/92840881?utm_id=0
   1. Very good. This is generation technology breakthrough of search engine
       1. text match -> BitFunnel
       2. vector distance
   2. BitFunnel: Revisiting Signatures for Search
      https://www.youtube.com/watch?v=1-Xoy5w5ydM
        1. Higher rank rows
        2. Frequency conscious bloom filters
        3. Sharding across cluster
        4. Handling false positives

3. How OpenAI Deep Research works?
    1. Open Deep Research - Together.ai
       https://www.together.ai/blog/open-deep-research

4. Using meta tags in GPT prompt
    1. Cursor's prompt
        1. https://www.zhihu.com/pin/1898416105153863856
        2. https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/blob/main/Cursor%20Prompts/cursor%20agent.txt
    2. Reddit: Exploring Meta Tags for AI Prompts
       https://www.reddit.com/r/ChatGPTPro/comments/1ehx9zi/exploring_meta_tags_for_ai_prompts/
    3. A Complete Guide to Meta Prompting
       https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting
    4. Meta Prompting: A Practical Guide to Optimising Prompts Automatically
       https://cobusgreyling.medium.com/meta-prompting-a-practical-guide-to-optimising-prompts-automatically-c0a071f4b664

5. Windsurf: 160人卖了217亿，AI应用首个大额套现项目，CEO解密成功秘诀
   https://mp.weixin.qq.com/s/MgHOoIyU1oCEqeXXWU8jng
    n. Related materials
        1. 理解LLM智体的规划：综述 - 黄浴
           https://zhuanlan.zhihu.com/p/684281195
        
        2. Understanding the planning of LLM agents: A survey
           https://yiyibooks.cn/arxiv/2402.02716v1/index.html
           https://arxiv.org/abs/2402.02716
            1. Interesting. Today using LLM is evolved into let an Agent first use LLM to plan the task map first. Reflection and refinement can be done a second time on the outputs.

        3. A Survey on the Memory Mechanism of Large Language Model based Agents
           https://arxiv.org/html/2404.13501v1
            1. Memory Sources, Memory Forms, Memory Operations
            n. Related materials
                1. How LLM Memory works
                   https://www.reddit.com/r/OpenAI/comments/1aqksc3/how_llm_memory_works/
                    1. useful explanation
                    2. In another word, regular RAG retrieving vector embeddings of past user messages

                2. Generative Agents: Interactive Simulacra of Human Behavior    [2156 refs, 2023]
                   https://arxiv.org/pdf/2304.03442
                   https://yiyibooks.cn/arxiv/2304.03442v2/index.html
                   https://www.youtube.com/watch?v=ZdoU9vI2yCg
                    1. Memory Stream, Reflection, Planning, Feedback
                        1. Very good paper. The authors built power modern LLM agent but with super simple but innovative solutions.
                    2. How the Smallville is built upon LLM - very good
                        1. Per timeframe, an agent outputs a natural language statement. The statement drives the world.
                        2. Everything in the architecture is recorded and reasoned over as a natural language description.
                        3. Memory stream and RAG database
                            1. Figure 6 reveals the magic. Memory stream are simply text lines of history. Retrieval is evaluated by recency * importance * relevance.
                            2. Implementing importance: simply let LLM model to output an integer score. Prompt below.
                            3. Implementing relevance: 
                                1. Use LLM model to generate embedding vector for each memory text description. Relevance is a cosine similarity between embedding or memory vector and the query memory's embedding vector.
                            4. Weight of recency, importance, relevance are simply 1.
                        4. Building "reflection"
                            1. The agent's observations of the world, represented in the leaf nodes, are recursively synthesized to derive Klaus's self-notion
                            2. Reflection is also fed into Memory stream
                            3. Implementation
                                1. Reflections are generated periodically
                                2. Generate reflections when the sum of the importance scores for the latest events perceived by the agents exceeds a threshold
                                3. Prompt: "Given only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements", and then use the answers as query to memory stream, and then let LLM to extract insight
                        5. Planning
                            1. Plans are put to Memory stream too.
                            2. Plans are recursively broken down.
                            3. Dialogue
                                1. Interesting implementation. See section 4.3.2
                        6. Interaction to objects
                            1. Ask LLM what would be the state change of an object after interaction
                                1. Interesting tricky. Instead of programming states, pretend the object is an agent with memory, and interact with natural language
                    3. Evaluation
                        1. Criteria
                            1. Believable plans, reactions, thoughts
                            2. Information diffusion
                            3. Relation information
                            4. agent coordination
                        2. Procedure
                            1. "Interview" the agents with natural language
                                1. Interesting .. very interesting ..
                            2. Scoring: Human evaluator ranks the believability 
                                1. Also with human crowdworder-authored behaivors as baseline
                                2. TrueSkill ranking
                                3. Inductive analysis
                            3. Ablations tests
                            4. Results
                                1. Generative Agents Remember, but With Embellishments
                                2. Reflection Is Required for Synthesis
                                3. "Over time, the interests of others shaped her own interests" (Section 7.2)
                            5. End-to-end evaluation
                                1. Criteria
                                    1. Information diffusion
                                    2. People relation built
                                    3. Coordination
                                2. The remarkable part is the above criteria weren't directly built in the simulation system. Agents learned them with emergence.

6. GetAbstract: Good Team, Bad Team by Sarah Thurber and Blair Miller
   https://www.getabstract.com/en/summary/good-team-bad-team/50096
    1. Team members may have distinct thought preferences
        1. Clarifiers sometimes spend too much time trying to define an issue. That can lead to analysis paralysis.
        2. Idea generators may get swept away by their big concepts, forgetting or ignoring the pesky details. Thus, their more sweeping ideas may not be grounded in reality.
        3. Developers, in contrast, may spend too much time digging into the numerous details of a proposed solution, losing themselves in the intricacies as they pursue a perfect solution.
        4. Implementers often want to move as quickly as possible, often too quickly, to activate their solutions. Unsurprisingly, this often leads to flawed results.
    2. Team development phases
        1. "Forming" – This is the "honeymoon phase" when people come together to form a team. The members of a new team are naturally anxious. They will look to the leader to set the pace and provide guidance.  
        2. "Storming" – This is the fractious stage when members may maneuver for power and position or try to elbow other members out of the way. Conflict can cause havoc as feelings and egos arise.
        3. "Norming" – Members put aside their differences and begin to communicate easily and act as teammates. They negotiate instead of arguing. One way or another, troublemakers leave the team. The team gets to work.
        4. "Performing" – This is the magic phase when good things happen. Members readily collaborate as they become energized about achieving mutual goals. 
        5. "Re-forming" – When old members leave the team, when new members join, or when the team’s charter changes, re-forming occurs naturally. This period is always difficult. Seasoned members can help everyone get back on track.
        6. "Closure" – The team achieves its goals, wraps up its joint efforts, and celebrates its accomplishments.
    3. two pivotal problem-solving tools
        1. One proven tool is to state problems as questions, not facts. For example, instead of saying, “I can’t keep up with all this work,” ask, “How might I manage my growing workload?”  
        2. Offering praise before criticism is a second proven tool. This strengthens relationships and helps people refine their ideas. Instead of immediately seeking the weaknesses in new ideas, praise what you can and then raise your concerns. Remain open to the opportunities an idea may suggest.

7. Why Cline Doesn't Index Your Codebase (And Why That's a Good Thing)
   https://cline.bot/blog/why-cline-doesnt-index-your-codebase-and-why-thats-a-good-thing
    1. The article reveals key reflections of RAG and code agent
        1. RAG - chunk documents and big embedding index for each. The problem is code is different, code is interconnected, cannot be chunked
        2. Agent exploration of code - Explores, trace, and follows up the code. 
            1. You have to parse all the source code of all the files using something like tree-sitter or clang (etc) and ingest the code entities and relationships into a knowledge graph.
                1. Graph RAG
            2. Also should use an LLM to make english summaries of the various code entities so that you can make embeddings of those summaries to put on the graph nodes to search them up later.
            3. Need to also have file paths and line numbers on the graph nodes.
            4. it asks clarifying questions and makes sure it understands your goals
    n. related materials
        1. Does RAG work on large codebases? Or does chunking / embedding ruin an LLM’s ability to make sense of an app’s code, understand dependencies, etc?
           https://www.reddit.com/r/LocalLLaMA/comments/1gf2mg5/does_rag_work_on_large_codebases_or_does_chunking/

        2. My experience with Cursor vs Cline after 3 months of daily use
           https://www.reddit.com/r/ChatGPTCoding/comments/1inyt2s/my_experience_with_cursor_vs_cline_after_3_months/

8. Understanding MCP
    1. Github: modelcontextprotocol / python-sdk
       https://github.com/modelcontextprotocol/python-sdk
        1. "MCP Inspector" can show you the detailed request/response workflow
           `uv run mcp dev`
           http://127.0.0.1:6274

    2. model context protocol specification
       https://modelcontextprotocol.io/docs/concepts/prompts#python

    3. Model Context Protocol (MCP) Explained in 17 Minutes - Jan Marshal
       https://youtu.be/G5KyIzV-254?si=XPSryWebBOuNCTgt&t=795
        1. Reveals how MCP knows which tools to use
            1. MCP client sends ask to all MCP servers
            2. Each MCP server returns its capability (tools), compose into an array
            3. Question + tools array is sent to LLM, LLM tells which tool to use
                1. It's pretty like MoE routing
                2. It doesn't necessarily use context length in the user session
        n. related materials
            1. Model Context Protocol (MCP) - Explained - Marco Codes
               https://youtu.be/sahuZMMXNpI?si=KSpmMAzwbcZCmMo4&t=490
                1. Similarly shows the workflow that how LLM discovers which tool to use

    4. Relations with Plugin/MCP/Agent
        1. MCP is also by far the best current solution for “LLM plugins”
           https://jamiedubs.com/blog/llm-plugins-and-the-state-of-mcp/
            1. OK .. Plugin is replaced to MCP

        2. How to build an AI agent with ChatGPT: A step-by-step guide
           https://www.jotform.com/ai/agents/how-to-build-an-ai-agent-with-chatgpt/
            1. OK .. Agent is a customized wrapper (upper layer) to LLM API
                1. Agent integrates external data source, customized scenario, history tracking, Agent-to-Agent talks
            2. Typical platforms
                1. LangChain
                   https://www.langchain.com/

    5. ChatGPT: Questions to understand how MCP works
       https://chatgpt.com/share/683d79a3-e40c-800f-87c2-b191f4883371

9. Knowledge Graph RAG
    1. Knowledge Graph or Vector Database… Which is Better?
       https://www.youtube.com/watch?v=6vG_amAshTk
        1. Microsoft GraphRAG. Useful.
        2. Highlights
            1. Community detection and community reports
            2. Chunking text and building relations automatically
                1. Each chunk has 1200 tokens with 100 tokens overlaps
                2. The uploader has a long magic prompt to tell how to identify entities and relations

    2. Microsoft GraphRAG
       https://microsoft.github.io/graphrag/

    3. From Local to Global: A GraphRAG Approach to Query-Focused Summarization    [2024, 511 refs]
       https://arxiv.org/pdf/2404.16130
        1. Very good paper. GraphRAG is now widely used. This is a paradigm shift from vector RAG. Related category "Query-Focused Summarization".
           This paper has quite a few innovations like, hierarchical community summaries, mapreduce answer processing, evaluation by LLM to generate diverse questions.
           But note, GraphRAG is more computational heavy than vector RAG.
        2. Highlights
            1. How GraphRAG works
                1. First, GraphRAG uses LLM to construct the knowledge graph.
                    1. Self-reflection methods
                        1. After entities are extracted from a chunk, we provide the extracted entities back to the LLM, prompting it to “glean” any entities that it may have missed
                    2. Surprisingly, Small chunk size however discovers more entities
                    3. Appendix E example prompts are very useful. Prompts are the magic sauce 
                2. Next, it partitions graph into a hierarchy of communities
                3. Use LLM to generate community level summaries, bottom-up hierarchically
                4. Finally, GraphRAG answers queries with MapReduce processing of community summaries
                    1. in the map step, the summaries are used to provide partial answers to the query independently and in parallel, 
                    2. then in the reduce step, the partial answers are combined and used to generate a final global answer.
                    3. The LLM is also asked to generate a score between 0-100 indicating how helpful the generated answer is in answering the target question
            2. Evaluation to compare with vector RAG
                1. First uses one LLM to generate a diverse set of global sensemaking questions based on corpus-specific use cases, 
                2. using a second LLM to judge the answers of two different RAG systems using predefined criteria
                3. Algorithm 1: Description of a corpus, number of users K, number of tasks per user N, number of questions per (user, task) combination M
                4. Section 3.3 criteria for evaluating global sensemaking
                    1. And Appendix F. This is an very interesting section as how to effectively use LLM to evaluate generation.
                    2. My questions
                        1. It resembles DeepSeek-R1 to me, that it uses DeepSeek-V3 to generate SFT training samples for DeepSeek-R1. (See section 2.3.1 Cold Start, rejection sampling)
            3. Comparing with prior works
                1.  GraphRAG contrasts with these approaches by generating a graph index from the source data, then applying graph-based community detection to create a thematic partitioning of the data
            5. Appendix
                1. Context window selection
                    1. Surprisingly, small context size 8K performs better for all comparisons on comprehensiveness, diversity, empowerment.

        n. Related materials
            1. GraphRAG: Unlocking LLM discovery on narrative private data
               https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/

10. Google: AlphaEvolve: A Gemini-powered coding agent for designing advanced
    https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
    1. Designing better algorithms with large language models
    2. Highlights
        1. AlphaEvolve discovered a simple yet remarkably effective heuristic to help Borg orchestrate Google's vast data centers more efficiently. This solution, now in production for over a year, continuously recovers, on average, 0.7% of Google’s worldwide compute resources.
        2. AlphaEvolve proposed a Verilog rewrite that removed unnecessary bits in a key, highly optimized arithmetic circuit for matrix multiplication.
        3. By finding smarter ways to divide a large matrix multiplication operation into more manageable subproblems, it sped up this vital kernel in Gemini’s architecture by 23%, leading to a 1% reduction in Gemini's training time.
    n. Related materials
        1. Hackernews: AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms
           https://news.ycombinator.com/item?id=43985489
        2. Reddit: DeepMind introduces AlphaEvolve: a Gemini-powered coding agent for algorithm discovery
           https://www.reddit.com/r/singularity/comments/1kmhti8/deepmind_introduces_alphaevolve_a_geminipowered/

11. 一个大型网站需要多少服务器？ - Karminski-牙医
    https://www.zhihu.com/question/27641736/answer/814798641
    1. Good. 掘金前技术总监. Pretty hardcore DIY.

12. 十年再出发：回顾我与 TiDB 的成长之旅 - 唐刘
    https://zhuanlan.zhihu.com/p/1896834371740210342
    1. Very good. It is changing my impression to TiDB.
    2. TiKB, Chaos Mesh, TiDB Cloud, Global customers
    3. 单表导入100TB数据, TiDB支持100万张表

13. DanceNN：字节自研千亿级规模文件元数据存储系统概述 - 云朵儿
    https://zhuanlan.zhihu.com/p/1896340677115220912
    https://mp.weixin.qq.com/s/uJb6iplETFEaO2drL3YF_g
    0. Good. Clear solutions and quite a few interesting optimizations.
    1. 一般基于分布式存储的元数据格式有两种方案
        1. 方案一类似 Google Colossus，以全路径作为 key，元数据作为 value 存储
            1. 优点有：
                1. 路径解析非常高效，直接通过用户请求的 path 从底层的 KV 存储读取对应 inode 的元数据即可
                2. 扫描目录可以通过前缀对 KV 存储进行扫描
            2. 但是有下列缺点：
                1. 跨目录 Rename 代价大，需要对目录下的所有文件和目录进行移动
                2. Key 占用的空间相对比较大
        2. 另外一种类似 Facebook Tectonic 和开源的 HopsFS，以父目录 inode id + 目录或文件名作为 key，元数据作为 value 存储，
            1. 这种优点有：
                1. 跨目录 Rename 非常轻量，只需要修改源和目标节点以及它们的父节点
                2. 扫描目录同样可以用父目录 inode id 作为前缀进行扫描
            2. 缺点有：
                1. 路径解析网络延迟高，需要从 Root 依次递归读取相关节点元数据直到目标节点
                    1. 例如：MkDir /tmp/foo/bar.txt，有四次元数据网络访问：/、/tmp、/tmp/foo 和 /tmp/foo/bar.txt
                2. 层级越小，访问热点越明显，从而导致底层存储负载严重不均衡
                    1. 例如：每个请求都要读取一次根目录/的元数据
    2. 考虑到跨目录 Rename 请求在线上集群占比较高的比例，并且对于大目录 Rename 延迟不可控，DanceNN 主要采用第二种方案，
        1. 方案二的两个缺点通过下面的子树分区来解决。
            1. 子树分区: DanceNN 通过将全局 Namespace 进行子树分区，子树被指定一个 NameServer 实例维护子树缓存。
            2. 子树缓存: 维护这个子树下所有目录和文件元数据的强一致缓存
        2. 路径冻结
            1. 在子树迁移、跨子树 Rename 等操作过程中，为了避免请求读取过期的子树缓存，需要将相关的路径进行冻结，冻结期间该路径下的所有操作会被阻塞，由 SDK 负责重试，整个流程在亚秒级内完成
    3. 分布式锁管理
        1. 虽然 ByteKV 提供事务的 ACID 属性且支持 Snapshot 隔离级别，但是对于多个并发写操作如果涉及底层数据变更之间没有 Overlap 的话，仍然会有 Write Skew 异常，这可能导致元数据完整性被破坏。
            1. 其中一个例子是并发 Rename 异常，如下图
        2. 我们选择使用分布式锁机制来解决，对于可能导致异常的并发请求进行串行处理，基于底层 KV 存储设计了 Lock Table，支持对于元数据记录进行加锁，提供持久性、水平扩展、读写锁、锁超时清理和幂等功能。
        3. Latch 管理
            1. 为了支持对子树内部缓存的并发访问和更新，维护缓存的强一致，会对操作涉及的缓存项进行加锁(Latch)，
            2. 例如：Create /home/tiger/foobar.txt，会先对 tiger 和 foobar.txt 对应的缓存项加写 Latch，再进行更新操作;
            3. Stat /home/tiger 会对 tiger 缓存项加读 Latch，再进行读取。
    4. 为了提升服务的整体性能做了非常多的优化，下面列两个重要优化：
        1. 热点目录下大量创建和删除文件
            1. 例如：有些业务像大型 MapReduce 任务会在相同目录一下子创建几千个目录或文件。
            2. 一般来说根据文件系统语义创建文件或目录都会更新父目录相关的元数据(如 HDFS 协议更新父目录的 mtime，POSIX 要求更新父目录 mtime，nlink 等)，这就导致同目录下创建文件操作对父目录元数据的更新产生严重的事务冲突，另外底层 KV 存储系统是多机房部署，机房延迟更高，进一步降低了这些操作的并发度。
            3. DanceNN 对于热点目录下的创建删除等操作只加读 latch，之后放到一个 ExecutionQueue 中， 由一个的轻量 Bthread 协程进行后台异步串行处理，将这些请求组合成一定大小的 Batch 发送给底层的 KV 存储，这样避免了底层事务冲突，提升几十倍吞吐。
                1. Interesting technique. Use a queue/scheduler to optimize transaction conflicts from a high ingestion spike
        2. 请求间的相互阻塞
            1. 有些场景可能会导致目录的更新请求阻塞了这个目录下的其他请求，
                1. 例如：SetXAttr /home/tiger 和 Stat /home/tiger/foobar.txt 无法并发执行，
                    1. 因为第一个对 tiger 缓存项加写 Latch，后面请求读 tiger 元数据缓存项会被阻塞。
                2. DanceNN 使用类似 Read-Write-Commit Lock 实现对 Latch 进行管理，每个 Latch 有 Read、Write 和 Commit 三种类型，其中 Read-Read、Read-Write 请求可以并发，Write-Write、Any-Commit 请求互斥。
                    1. 基于这种实现，上述两个请求能够在保证数据一致性的情况下并发执行。
                    2. Interesting optimization, a "commit lock" to separate from write lock
        3. 请求幂等
            1. Problem: 当客户端因为超时或网络故障而失败时，进行重试会导致同一个请求到达 Server 多次。有些请求如 Create 或者 Unlink 是非幂等的请求，对于这样的操作，需要在 Server 端识别以保证只处理一次。
            2. Solution: 在单机场景中，我们通常使用一个内存的 Hash 表来处理重试请求，Hash 表的 key 为 {ClientId, CallId}，value 为 {State, Response}，当请求 A 到来之后，我们会插入 {Inprocess State} 到 Hash 表;这之后，如果重试请求 B 到来，会直接阻塞住请求 B，等待第请求 A 执行成功后唤醒 B。当 A 执行成功之后，我们会将 {Finished State, Response} 写到 Hash 表并唤醒 B，B 会看到更新的 Finished 状态后响应客户端。
                1. Interesting technique
            3. 类似的 DanceNN 写请求会在底层的 WriteBatch 请求里加一条 Request 记录，这样可以保证后续的重试请求操作一定会在底层出现事务 CAS 失败，上层发现后会读取该 Request 记录直接响应客户端。另外，何时删除 Request 记录呢，我们会给记录设置一个相对较长时间的 TTL，可以保证该记录在 TTL 结束之后一定已经处理完成了。

14. GetAbstract: Working with AI - Real Stories of Human-Machine Collaboration - Steven Miller and Thomas H. Davenport
    https://www.getabstract.com/en/summary/46179
    1. Highlights
        1. Many people in IT departments now have business backgrounds rather than technology ones

15. GetAbstract: The AI-Powered Enterprise - Harness the Power of Ontologies to Make Your Business Smarter, Faster, and More Profitable - Seth Earley
    https://www.getabstract.com/en/summary/39725
    1. Highlights
        1. AI algorithms help leaders guide business decisions because they detect irregular patterns

16. GetAbstract: Influence and Impact - Discover and Excel at What Your Organization Needs from You the Most - Bill Berman and George Bradt
    https://www.getabstract.com/en/summary/influence-and-impact/43568?u=microsoft&st=RELATED&si=46904
    1. Highlights
        1. What we have found, again and again, is that people tend to underperform because they do what is comfortable, what is familiar or what they desire, rather than what is most important to the organization.
        2. "Psychological contract with your organization" - Actually this "contract" lack definition and change frequently. It is very common that you will find your organization expects something different from you than what you think your job entails.
        3. Control, autonomy and the need for respect are major motivators for people. The higher you move in an organization, the more likely you are to find people who value independence and self-determination.
        4. Turn [your job’s] most relevant values into more specific guidelines for yourself in your role. If, for example, you say you value collaboration, your way of working might be, ‘Build alignment with all key stakeholders before making mission-critical decisions’.
        5. If you do something extraordinary, your colleagues may expect you to do it again. Instead, you may want to build your abilities by taking small, consistent steps that shape you as a person. Increasing your influence within your organization requires consistent work with that goal in mind.
        6. Change your tactics if you run into unforeseen obstacles. Seek support from your superiors, and ask them to evaluate your plans and provide their insights. If you steadily and successfully take on more responsibility, your colleagues will accept that you will do what you say. In time, these responsibilities will become part of your job.

17. LeetCode 776: Split BST
    https://leetcode.com/problems/split-bst/description/
    https://www.geeksforgeeks.org/dsa/split-a-bst-into-two-balanced-bsts-based-on-a-value-k/
    1. inorder traversal is sorted, it splits the original tree into sorted nodes for subtree1 and subtree2.
       next, construct subtree1 and subtree2 from the sorted nodes. note the constructed tree should be balanced.
    2. My analysis
        ``
        if (e < me)
        {
          // subtree1 and subtree2 only contain elements smaller than me
          search_and_build(me.left, subtree1, subtree2)
          connect_me_and_my_right_to_subtree2  // me.left = subtree2, subtree2 = me.
        }
        else if (e == me)
        {
          connect_my_left_to_subtree1
          connect_my_right_to_subtree2
        }
        else  // e > me
        {
          // subtree1 and subtree2 only contain elements bigger than me
          search_and_build(me.right, subtree1, subtree2)
          connect_my_left_and_me_to_subtree1  // me.right = subtree1, subtree1 = me.
        }
        ``
       1. So, subtree1 will only be inserted with a subtree_left, which is smaller than any existing node in subtree1.
          subtree2 will only be inserted with a subtree_right, which is bigger than any existing node in subtree2.
          1. How to efficiently insert such a subtree_left/right and maintain balance-tree property?
            1. We can know, subtree_left/right can be in any shape. Consider a huge AVL rotating operation
    3. Create a balanced BST with a sorted list as input
        1. https://www.geeksforgeeks.org/dsa/sorted-array-to-balanced-bst/ 
            1. The solution needs the array of sorted elements to be pre-existing. It will randomly access the array. Using binary recursive access.

18. LeetCode 1312: Minimum Insertion Steps to Make a String Palindrome
    https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/description/
    https://www.geeksforgeeks.org/dsa/minimum-insertions-to-form-a-palindrome-dp-28/
    1. My analysis
      1. Observations
        1. only need to insert a char pre-existing. this limits search space.
        2. max insert steps is n-1. n is strlen. this limits search step.
        3. if the input string has existing palindromic substr, starting from there will reduce the insertion steps. otherwise, we *probably* need insertion step n-1.
        4. suppose we found the center of a palindromic substr, its len-1 substr is also a palindromic substr.
      
    2. naive solutions
      1. O(n^3) brutal force trial
        1. loop 1: n steps. loop 2: insert position. loop 3: insert char. track with an n^3 table. test any is palindromic string.
      2. DP to scan through steps
        1. dp[i] is a hashset of string at step i. dp[i+1] is obtained by inserting any char at any position at strings from step i.
      3. start from center
        1. Scan each position i or i+0.5, test if its neighborhood is a palindromic string. obtain the max neighborhood radius.
        2. problems
          1. it may not be the best seed
          2. insert at left vs insert at right, or insert both?
            1. we must try each. otherwise we may miss the disconnect palindromic substr in further distance. See the example below.
              ``
              lgeekl
                lgkeekl
                  lglkeekl
                  lgkeekgl
                lgeegkl
                  lkgeegkl
                  lgeeglkl
              ``
          3. there may not existing a seed, but only existing a disconnected palindromic substr
      4. DP to scan through str len
        1. min step for str n-1 len.
             case 1: str at n is identical to str at 0
               recursion to min step for str 1..n-1
             case 2: str at n is not same with str at 0
               recursion to min step for str 0..n-1 + 1
    
    3. solutions
        1. use recursion
          1. if str[l] is equal to str[h] findMinInsertions(str[l+1…..h-1]) 
             otherwise, min(findMinInsertions(str[l…..h-1]), findMinInsertions(str[l+1…..h])) + 1 
            1. the assumption is, the palindromic insertion starts from a best seed, and then expand to edge
            2. There are shared structure in recursion search. It can be optimized.
              ``
              1 2 3 4 5 6 7 8
              1..8
                1..7
                  1..6
                  2..7
                2..8
                  3..8
                  2..7
              ``

          2. 问题：为什么n+1的递推，不去考虑字符串抽掉任何一个字符后得到的n？而是只递推了首尾移动
            1. // TODO

        2. DP
          1. d[start][end] = min insertion step for substr start..end.
          2. d[start-1][end] = 
               if str(start-1) == str(end) then d[start][end-1]
               else: min(d[start+1][end], d[start][end-1])+1
             d[start][end+1] = similar
          3. it needs O(n^2) calculation and O(n^2) space

        3. DP with optimized space
          1. Following DP in 2, calculate row by row, from left to right. Then it only needs O(n) space.

    4. 如何寻找最优子结构，并保证不遗漏任何递推联接？
      1. 探索从n+1到n，也探索从n到n+1。如果任何一方有多对多的关系，那对称地，另一方向递推也应该有。
      2. 完整性检测：任何n+1中的可能solution，都应该被某一个n的分支包含
      3. 有时需要问题转化，对dp值含义加限定条件，如LIS

    5. Related problems
      1. LCS problem - Longest Common Subsequence. s1, s2 are the two strings
        1. My analysis
          1. DP solution
            1. dp[s1_n, s2_n] := the LCS for s1.substr(0..s1_n) and s2.substr(0..s2_n) // a..b is inclusive
            2. dp[*, 0] = 0
               dp[s1_n, s2_n] = max( dp[s1_n, s2_n - 1], 1 + dp[s1_i-1, s2_n - 1] for s1_i in 1..s1_n if s1[s1_i] == s2[s2_n] )
            3. dp[s1_n, s2_n] = take max of
              1. dp[s1_n, s2_n - 1]
              2. for s1_i in s1_n..1:
                   if s1[s1_i] == s2[s2_n]:
                     return dp[s1_i - 1, s2_n - 1]
          2. Brute force for validation
            1. suppose LCS ends at s1[s1_n] and s2[s2_n]. then, we can do recursion
              ret = 0
              for s1_i in 0..len(s1):
                for s2_i in 0..len(s2):
                  if s1[s1_i] == s2[s2_i]:
                    ret = max(ret, func(s1_i-1, s2_i-1) + 1)
            2. OK .. this is the better solution

      2. Edit Distance problem
        1. Problem
          1. Given two strings s1 and s2, compute the minimum number of operations required to convert s1 into s2
          2. It can insert/delete/replace a char
        2. Example
          1. s1 = "ABCDEAG"
             s2 = "BAGCA"
        3. My analysis

          1. PLANNING THE SOLUTION
            1. Problem clarification
            2. Create my examples
              1. Collect counter and edge examples
            3. Observations
              1. Math properties
              2. Max possible steps
              3. Ordering of operations
              4. Space structure analysis
                1. 操作空间的大小是有限的吗？
                2. 操作空间与 Permutation 是同构的吗？
                3. 解空间是有限的吗？
            4. Substructure analysis
            5. Try DP
              1. step formula should has stable relation, i.e. if add 1 step, whether score increase or not is fixed. Otherwise, add constraints and conditions, or introduce more incremental legs/dimensions in DP.
              2. try different incremental legs in DP, e.g.
                1. end in s1 + end in s2
                2. start, end in s1
              3. How to know if the step branch is exhaustive?
                1. Cut conditions, make sure all covered  
              4. 解决的关键在于如何划分子问题。
                 子问题和下一级需要有稳定的关系，可以确定性地给出分数公式。
                  1. 子问题可以来自
                    1. partition the N elements, or reduce to N-1 elements
                    2. 为结果 score 添加限定关系，如 LIS 问题，限定为 score + end index
                    3. 为结果 score 扩展内容，如 Partition a set to minimize subset sum diff 问题，扩展为所有可能的 score
                    4. 追踪 score 空间，而不是操作空间，这是 DP 的基础
            6. Try brute force for validation
            7. Aux data structure
            8. Try recursion
            9. Math translate to another problem
            10. Decompose to sub-problems
            11. Fallback, if I didn't workout
              1. If it is too hard to solve the complete problem, solve a sub-problem under certain constraints. relaxation.
              2. If the accurate solution is not possible, solve an approximate solution. sketching.
        
          2. trying solution
            1. observation
              1. max step is strlen. so brute force is possible
            2. Brute force
              1. use a hashset for wip strings. each round try insert/delete/replace at any position. try at most strlen round.
            3. observation
              1. the shared hashset in brute force solution implies there are overlapping substructure. we can apply DP or recursion
              2. string tokens in hashset implies they are the sub-problems in DP
            4. DP
              1. dp[s1_n][s2_n] := edit distance between s1[0..s1_n] and s2[0..s2_n]
              2. if s1_n > s2_n, then dp[s1_n][s2_n] = dp[s2_n][s1_n]
                1. note, need to switch the string
              3. observation
                1. suppose len(s1) < len(s2), can delete help in s1? - Yes
                  1. s2 = ABCDEFG
                     s1 = AXBCDE
                2. suppose len(1) == len(s2), what is the edit distance?
                  1. first, strip away the identical chars on the left and right
                  2. edit distance(n) = edit distance(0..n-1) + 1
                  3. actually, only need to strip right
                  4. observation: we cannot recursion by delete both char at tail. example below
                     DEFGHIJKL
                     EFGHIJKLD
                3. replace = delete then add back. 
                   distance(n+1) = min(distance(n)) + 1. 
                    1. DEFGHIJKL
                        DEGHIJKL
                4. delete left, right, middle, can each possible to give you a better edit distance
                  1. Example
                       DEFGHIJKL
                      GDEFGHIJKL
                       DEFGHIJKLG
                       DEFGHGIJKL
                  2. Replace can be represented by delete then add back, so we only need to try n+1 -> n
                  3. Insert? it is not reducing to a simpler problem.
                6. delete/replace/insert operations can be reordered, always put delete first, so that short s never exceeds long s length.
                7. delete in middle, should be able to be replaced by just exploring strip head/tail.
                  1. example
                      CDEF
                      CXDEF
            5. DP2
              1. suppose s1 is longer than s2
              2. dp[i..j] := edit distance of s2[i..j] to s1
                 dp[i..i] = s1 contains s2[i] ? (strlen(s1) - 1, position of match) : (strlen(s1), -1)
                 dp[i..i+1] = s1[pom+1..len(s1)-1] contains s2[i+1] ? (dp[i..i]-1, new pom) : (dp[i..i], pom+1)
                 dp[i..j] = 
            6. DP3
              1. dp[i][j] := edit distance of s1[0..i] and s2[0..j]
              2. observation
                1. what does "+1" edit distance map to?
                  1. delete a char in a shorter s, can also reduce the edit distance
                    ABCDEFG
                    ABCXDEF
                  2. add a char in the longer s, can also reduce the edit distance 
                     BCDEFGH
                       DEFIGH
                2. An example of rotationg
                   ABCDEFGHIJKLM
                     C
            EFGHIJKLMC
                    1. This example shows, DP2 algorithm has problem with the pom. pom of the last round may not be correct in the next round
            7. Math translation
              1. Assuming the Edit Distance = 0 + Edit Distance(remove the LCS)
                  ..A..S..A.S..S..S....
                    .AS..S.AS..S..
            8. DP4
              1. Observation
                1. We know inserting a new char at head/tail, not necessarily increase the Edit Distance, it may reduce the Edit Distance, if the newly added char is matching something.
                   So, to make dp recursion formal at n+1 has a fixed relationship with dp at n, we need to introduce constraints.
                2. suppose s1 is longer than s2, we edit s2 to approach s1
                   dp[i][pom] := Edit Distance of s2[0..i], and s2[i] is matching s1 at position pom in the final string we edited. Future matching position is s1[pom+1..]
                   dp[i][-1] := The case that s2[i] isn't matching any s1 position. Future matching position is <need-to-maintain> 

                   starting:
                    dp[0][-1] = strlen(s1), Future matching position is s1[0..]
                    dp[0][pom] = strlen(i)-1 for any s2[0]==s1[pom], otherwise invalid. Future matching position is s1[pom+1..]

                   step formula:
                    dp[i][-1] = min(dp[i-1][*]) + 1, future matching position is the selected one's Future matching position.
                    dp[i][pom] = min(dp[i-1][*]), require pom > last future matching position, future matching position is pom+1
              2. this should work but it is a non-standard solution

            9. DP5
              1. Let dp[i][j] be the minimum edit distance to convert the first i characters of s2 to the first j characters of s1
              2. starting
                  dp[i][0] = i
                  dp[0][j] = j
              3. step formula
                  dp[i][j] =
                    if s2[i] == s1[j]: 
                      dp[i-1][j-1]   // Case 1: s2[i] match last token
                    else:
                      dp[i-1][j-1] + 1    // Case 2: s2[i] is replaced
                      for k in 1..j-1 where s2[i]==s1[k]:
                        dp[i-1][k-1] + j-k    // Case 3: s2[i] match prior token
                      dp[i-1][j] + 1    // Case 4: s2[i] is deleted
                      dp[i][j-1] + 1    // Case 5: insert s1[j]   // This may not be allowed, because we only operate s2

      3. Matrix Multiplication problem (MCM): given sequence of matrices, find the most effective way to multiply them.
         A1,A2,A3 matrix. Ai dimension is p[i-1] * p[i].
        1. cost of i * j multiply j * l = i * (j mul + j-1 sum) * i * l = j * i * l mul
           (i,j j,k) k,l => ijk mul + i,k k,l => ijk mul + ikl mul
           i,j (j,k k,l) => i,j j,l + jkl mul => ijl mul + jkl mul
        2. My analysis
          1. Brute force recursion
            1. Transform the p array into a bit mask, each mask maps to middle operating space. An "1" means the corresponding A has been cancelled out in matrix multiplication, by multiply with the matrix to its left.
            2. Transform the problem into a permutation of A[1..n].
              1. interesting. most such operation choice problem can be translated into permutation.
              2. in MCM, permutation represents which matrix should be cancelled out first.
              3. another way to map MCM to permutation is, insert a separator to the matrix chain, and require its left part and right part to multiply first respectively. Do this recursively, until places are inserted a separator.
            3. Recursion solution
              1. Cost(bitmask) = min(p[i-2]*p[i-1]*p[i] + Cost(bitmask clear i)) for i in 2..n
              2. Optimization: construct Cost of any bitmask from bottom to up.
              3. problem here, if we calculate cost for each bitmask, the space is too much. can we only calculate bitmask that has 1 consecutive sequence of bits? this transforms to the typical DP solution.
          2. DP
            1. analysis
              1. in the bitmask space, how should a lower level go to the higher next level?
                1. because a bit can be inserted in the middle of bitmask, the relation is not obvious
                2. take two lower level bitmask, which is shorter, you can combine them into one bigger higher level bitmask
            2. solution
              1. Partition the matrix chain into left and right part. Multiply left, right respectively, and then multiply the result.
                 Cost(1..n) = min (Cost(1..i) + Cost(i+1..n) + p[0]*p[i]*p[n] for i in 1..n-1)  // Split as A1..Ai, Ai+1..An
                 Cost(i..i) = 0
                 Cost(i..j) = min (Cost(i..k) + Cost(k+1..j) + p[i-1]*p[k]*p[j] for k in i..j-1)
              2. Compared to the Brute force Recursion solution, the DP solution found a much simpler path to go from bottom bitmask to top.

19. 这段时间搞大模型的血和泪 - 赵俊博 Jake
    https://zhuanlan.zhihu.com/p/716420396
    1. interesting

20. 带你从头发明MLA - 我是那谁
    https://zhuanlan.zhihu.com/p/1911795330434986569
    1. useful. with calculation steps and cost details
    2. 从MHA到MLA就两步
        1. 放弃缓存较大的KV，而缓存更小的输入Embedding X，代价是每次decoding step都重复地从X计算KV
        2. 简单粗暴地给X降维，从而使得缓存的X和重复计算KV的计算量都大幅减小。
    3. 对内存占用量（KV cache）和计算量比例的调和

21. lfyzjck 连载 AI 基础设施
    1. 大数据基础设施的演进：早期发展 - lfyzjck
       https://zhuanlan.zhihu.com/p/9879922408
    
    2. 大数据基础设施的演进：AI 时代--存储篇 - lfyzjck
       https://zhuanlan.zhihu.com/p/1918801610357862816
        0. Very good article. both with breadth, depth, and friendly-reading. Good problem analysis.
        1. 传统 DL 包括 NLP 后者图像领域的模型通常规模较小，训练耗时不算长，存储上面临的主要问题都是小文件问题（比如数亿小文件的存储），但是在性能没有太多需求。
            1. 但 LLM 带来了完全不同的需求，见下文
        2. LLM 动辄 100B 的参数量，使得我们不得不使用更昂贵的硬件比如 A100/H100 来训练模型，这使得我们对于 GPU 的利用率非常敏感
            1. 有过统计在一个 Epoch（将所有训练样本训练一次的过程）中，高达 70% 的时间都用在数据传送到 GPU 之前
            2. 一个 epoch 的训练时间为 21s；如果将 dataloader 替换为远端的 s3/hdfs 存储，每个 epoch 的训练时间下降到 40s，GPU 平均利用率不到 50%。可以看到 IO 性能其实对模型训练有很大的影响。
        3. AI Storage 的挑战
            1. 访问接口
                1. 目前深度学习领域经常使用的两种协议是基于 HTTP 的 S3 协议以及 POSIX
                2. POSIX 和我们使用本地磁盘没有区别，但是要求分布式文件系统基于 libfuse 实现一套了 VFS 的接口。
                    1. 实际上目前主流的分布式文件系统几乎都提供了 FUSE 接口的支持，但是功能和稳定性一言难尽，实际上能在产生环境稳定运行的并不多。
                    2. This explains why DeepSeek 3FS implements its own USRBIO API
                       https://github.com/deepseek-ai/3FS/blob/main/src/lib/api/UsrbIo.md
            2. 性能
                1. 延时对于提供 GPU 的利用率至关重要，因此分布式文件系统必须提供低延时的访问，并在整个集群并发读取时保证性能没有太大的下滑
                2. 扩展性. 这里主要说的还是元数据的扩展性
                    1. 在 CV 领域数据集通常都是图片和视频，小文件较多，轻松会超过亿级别，而分布式存储集群通常提供了元数据存储规模是严重受到架构限制的
                        1. 比如 HDFS 采用了中心化的元数据设计且所有元数据保存在内存中，元数据的规模受到单机内存的限制，大概每个 GB 能承载在元数据量在 1-2Million 左右
                        2. 而对象存储基本没有这类扩容，将元数据的扩展能力委托给 KV Store
                3. 数据管理问题
                    1. 这个本身不是一个很难的事情，但是实际操作起来会比较棘手
                    2. 因为专用的高性能文件系统比较贵，而训练使用的数据集通常比较多，所以会很明显的将存储分为昂贵的高性能训练文件系统和成本低廉的用于持久化的分布式文件系统
                    3. 我们需要不断的在两个 fs 之间进行数据同步，生命周期管理等操作。
                        1. 在这点上 Alluxio 这类主打 Cache 的系统就比较有优势
                        2. 云厂商提供的方案里比如 PFS 也会提供类似的 Bucket Link（通过并行文件系统直接读取对象存储的能力）的功能来解决这个问题
                4. 安全
                    1. 假设我们有行业领先的大模型，模型本身就具备相当的商业价值，保护模型本身不被攻击者非法获取也是非常重要
            3. 分布式文件系统
                1. 一类是传统从 HPC 领域做过来的全闪文件系统以及并行文件系统，由专门的存储提供商或者云厂商提供，这类方案的性能非常好，价格也十分昂贵，每PB/月的成本大概在千万 级别；
                    1. 而目前的 LLM 包括多模态主要的 io 模式是高并发的随机读，大规模的顺序 checkpoint 写入，和并行文件系统的设计略有差别，达不到最佳性能
                2. 另外一类方案是传统的分布式文件系统厂商，针对 AI 领域做了优化来提供对应的解决方案，性能比全闪文件系统慢，但是也大致满足需求，每PB/月的成本大概在百万级别。
                    1. 这里主要提及一下 JuiceFs 和 Alluxio，目前也是国内采用比较多的方案
                        1. JuiceFS 本质上是一个对象存储的 FUSE 代理，但是针对随机读写进行了大量的优化，在 AI 场景下更加适合。企业版的 JuiceFS 中支持分布式缓存，使得数据集可以被 Cache 在 FUSE 客户端组成的集群，避免反复从对象存储加载，这是高性能的关键。
                        2. Alluxio 严格来说不是一个文件系统，而是构建在其他分布式文件系统之上的分布式缓存系统，在大数据领域使用非常广泛。
                3. 还有定制硬件来提供加速的公司，比如 weka.io 的估值已经在 7亿刀左右了。
                    1. 全闪文件系统（All-Flash File System）
            4. CPU Offload
                1. 以 PyTorch 为例，DataLoader 在读取数据时并不是存粹的 IO ，而是混合了数据预处理，拷贝等操作的。一个数据集被加载到 GPU 之前，既有 IO 处理，也需要 CPU 参与对数据进行一些预处理来满足 GPU 的格式要求。整个 IO 的 Pattern 是并发的随机读，IO 和 CPU 的问题都可能导致数据无法及时送到 GPU 使得 GPU 空闲，利用率低。
                2. 要优化好 DataLoader 的性能，首先要做好数据并行（DP），常见的方案是 DDP 和 FSDP 
                3. 其次是需要尽可能的将 IO 从 CPU offload 到其他地方，提高数据传输带宽，降低 CPU 负载。这里有两种典型的解决方案：GDS 和 RDMA。
                    1. GDS（GPU Direct Storage）
                    2. RDMA
            5. 总结
                1. 首先，LLM 的 IO 特点是高并发的随机读以及高吞吐的顺序写入用于持久化 checkpoint，这需要底层的文件系统提供非常好的并发特性，并支持尽可能高的吞吐。
                2. 其次，训练用的数据集需要再内存、存储和 GPU 之间反复拷贝，存储访问的延时同时也会带来 GPU 的空闲，降低了 GPU 的资源利用率。我们需要优化存储，以及通过各种 CPU 侧载（cpu offload）的方式降低数据到 GPU 的延时，提供更好的 GPU 利用率。
                3. 最后，我们还需要关注数据的生命周期管理和安全问题。大部分时候，数据集并不是一开始就保存在高性能的存储上的，而是从其他更廉价的存储拷贝而来，我们需要一个系统来进行快速的数据复制并及时的从高性能存储上回收数据来降低整体的成本。缓存是一个不错的方案，其他存储可能也会内置类似的同步方案。
                4. 对于大部分的公司而言，虽然全闪文件系统（All-Flash FileSystem）是一个非常好的解决方案，在延时和并发能力上都会更适合 AI 训练的需求，但是高昂的价格让很多企业望而却步，在数据规模较小以及团队缺少 infra 能力的情况下可以考虑酌情购买。大部分时候我们应该考虑传统的分布式文件和并行文件系统，并尽量为模型的训练进行优化，在可控的成本下达到接近全闪文件系统的性能。相信不久的将来会看到更多的支持 RDMA 和 GDS 的分布式文件系统出现。

            n. Related materials
                1. 数据并行Deep-dive: 从DP 到 Fully Sharded Data Parallel （FSDP）完全分片数据并行 - YuxiangJohn
                   https://zhuanlan.zhihu.com/p/485208899

    3. 大数据基础设施的演进：云计算时代 - lfyzjck
       https://zhuanlan.zhihu.com/p/1916171182710944478

22. LeetCode 121: Best Time to Buy and Sell Stock
    https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
    1. Problem description
        1. An array of price[i]. Chose a single day to buy and sell stock to maximize the gain
    3. My analysis
        0. problem clarification
          1. can I sell the stock at the same day? assuming yes
          2. can I lose money after sold? assuming yes
          3. can I see full future prices? assuming yes
        1. Math structure
            1. reusable sub-structure: i-j and i2-j2 overlap
            2. not greedy - a drop in price then a large grow
            3. concat - dp[i][j] = dp[i][k] + dp[k][j]
            4. unlike common DP problem, calc dp[i][j] is a low const cost, no incremental calc needed
            5. greedy structured - give dp[i][*], the best answer is put j = the highest price within [i:]
        2. Brute force
            1. i, j to full scan array
        3. Looks like matching typical DP
            dp[i][j] :=  buy at day i and sell at day j, i <= j
            dp[i][i] = 0
            dp[i][i+1] = price[i+1] - price[i]

            dp[i+1][j] = dp[i][j] + price[i] - price[i+1] = dp[i][j] - dp[i][i+1]
            dp[i][j+1] = dp[i][j] - price[j] + price[j+1] = dp[i][j] + dp[j][j+1]
        4. problem: complexity is still i*j, no improvement to a simple for loop
        5. custom back scan algorithm
            1. best_day[i] := suppose buy at day i, then sell at best_day[i]
               best_day[i] = day | arg_max _day (price(day))

               highest_price_seen = price[max_day]
               highest_price_day = max_day
               for k in max_day..0:
                 if price[k] >= highest_price_seen:
                   highest_price_seen = price[k]
                   highest_price_day = k
                 best_day[k] = highest_price_day
        6. custom forward scan algorithm
            1. similar with bullet 5. suppose sold stock at day i, then the buy day should be the lowest within [:i+1]

23. Book: GetAbstract: You’re the Boss - Become the Manager You Want to Be (and Others Need) - Sabina Nawaz
    https://www.getabstract.com/en/summary/youre-the-boss/50036
    1. Follow the 5:1 rule: Offer five positive pieces of feedback for every corrective one.
    2. Create space for big ideas .. When you’re “mired in minutiae” — studying the details of a spreadsheet you don’t need to know, for example — you will have difficulty thinking clearly .. Busyness is a fabulous excuse to hide behind.
        1. Use the “Blank Space” tool to regain those capacities. Block out two hours per week in your calendar like any other commitment.
    3. Ask questions. Set aside the belief that you are always right
        1. For example, ask about one thing you can do more or less of; 
        2. use scaling questions, such as asking how your performance rates on a scale from one to ten; 
        3. or “externalize the ask,” by, for example, creating distance between the speaker and feedback by asking what a super critical person might say.
        4. Stay fully present and engaged by paraphrasing your team’s answers and asking follow-up questions.

24. Books about how to ask questions
    1. Stop, Ask, Explore - Learn to Navigate Change in Times of Uncertainty - Joan P. Ball
       https://www.getabstract.com/en/summary/45243
    
    2. Frank Sesno - Ask More - The Power of Questions to Open Doors, Uncover Solutions, and Spark Change
       https://www.getabstract.com/en/summary/28758

    3. Ask for More - 10 Questions to Negotiate Anything - Alexandra Carter
       https://www.getabstract.com/en/summary/40105

    4. What to Ask - How to Learn What Customers Need but Don’t Tell You - Andrea Olson
       https://www.getabstract.com/en/summary/46089

    5. QBQ! The Question Behind the Question - Practicing Personal Accountability at Work and in Life - John G. Miller
       https://www.getabstract.com/en/summary/44292

25. Book: GetAbstract: Emotionally Charged - How to Lead in the New World of Work - Dina Denham Smith and Alicia Grandey
    https://www.getabstract.com/en/summary/emotionally-charged/50368
    1. For too long, the workplace operated on the assumption that emotions were bad for business and bad for leadership. 
        1. This presumption stemmed from certain lines of reasoning. 
        2. The first, which puts rationality and hierarchy over collaboration, derives from outdated business models, such as command and control. 
        3. The second is the indeterminate cost of emotional labor, which renders it invisible and undervalued.
    2. Regulate your emotions by understanding where they come from and how they form, and by developing tools to deploy them with awareness and control
        1. Internal state awareness: You feeling are changeable, depending on your state of mind.
        2. Event appraisal: appraisal than explode
        3. Contextual assessment: Assess the people involved, the situation, the location, your role, and the timing to determine the context of your feelings
        4. Labeling emotions: Not "bad" / "stressful", but use for more specific vocabulary
    3. The DARE framework provides effective instructions on how to break the negative stress cycles that deplete leaders
        1. Detached – Try to stop ruminating. When the time comes, turn off your devices and step away from your office.
        2. Autonomous – Being autonomous means making active choices about what you do and don’t do.
        3. Relaxed – For your physical recovery, take time to relax and do nothing.
        4. Engaged – Pursue off-the-job activities that inspire and motivate you.
    4. In moments of intense emotional conflict, invoke the BRAVE process: Breathe, Recognize, Accept, Verbalize, and Engage to calibrate your responses.
        1. Process an emotional encounter by using “the three Rs”: 
            1. Reframe to consider your role. 
            2. Reflect to think about what you learned. 
            3. Restore yourself by replenishing your emotional resources.
    5. At their core, compassionate leaders recognize others’ distress while maintaining some distance between their emotions and those of the people they lead.
        1. Recognize common emotions – Acknowledge your anxiety, and remind your team members that you’re all in this together.
        2. Share socially – Tell a story your staff members can relate to that shows how you overcame a personal or professional challenge.
        3. Share with the team – Start meetings by checking in on how people are feeling, thus acknowledging that their anxieties matter.
        4. Narrate personal journeys – Sharing a life journey builds trust and compassion.
        5. Encourage candor – In stressful moments, let people express their anxieties without filters.
        6. Being genuine means not striving to be positive all the time.
            1. Unwarranted positivity can be toxic when leaders deploy it to placate people instead of recognizing and honoring their reactions.
            2. However, allowing strong negative feelings to take center stage will discourage your employees, so maintain a balance.

26. LeetCode 255: Verify Preorder Sequence in Binary Search Tree
    https://leetcode.com/problems/verify-preorder-sequence-in-binary-search-tree/
    1. Probing solutions
        1. construct tree while traversal
            1. how many different trees it can map to?
        2. stack traversal
            1. 
    2. use math properties to determine
        1. traversal a BST to find pattern
        2. neighbor relation
        3. jump element relation
    3. leverage certain recursion or loop to determine
        1. use node[0] to split list into smaller part and larger part
            1. there must be only 1 split cut
        2. recursively try on smaller part, and recursively try on larger part
            1. this should be the solution
    4. no recursion one scan - better solution
        1. what is the standard algorithm to construct tree from a preorder traversal list?
        2. Or standard algorithm to convert preorder traversal list into midorder traversal list?
            ``
            bool verifyPreorder(vector<int>& preorder) {
                stack<int> s;
                int lowerBound = INT_MIN;

                for (int v : preorder) {
                    if (v < lowerBound) return false;
                    while (!s.empty() && v > s.top()) {
                        lowerBound = s.top();
                        s.pop();
                    }
                    s.push(v);
                }

                return true;
            }
            ``
            1. Use a stack to simulate the path from root to current node.
            2. Use a lowerBound variable: the minimum allowed value for future nodes — because we've moved into a right subtree.

27. GetAbstract: Book: The New CEO - Lessons from CEOs on How to Start Well and Perform Quickly (Minus the Common Mistakes) - Ty Wiggins
    https://www.getabstract.com/en/summary/the-new-ceo/49968
    1. About the Author
        1. Ty Wiggins is the global head of the CEO and Executive Transition Practice at Russell Reynolds Associates.
    2. Highlights
        1. Communicate strategically. Communication matters more than action.
            1. For CEOs, no conversations are casual.
            2. Intertek CEO André Lacroix identified key messages to highlight for 30 days. He stresses the importance of repeating messages frequently to ensure that everyone hears and internalizes them.
        2. Prepare for a crisis of confidence
            1. In the past, the CEO played the role of a commander, with the company’s employees poised to carry out the leader’s directives. Today, CEOs embrace servant leadership: The leader provides guidance and vision, cultivating the conditions that allow employees to succeed.
        3. Assemble your leadership team
            1. During your first month, critically assess your senior leadership team and make necessary changes quickly.
        4. Devote a quarter of your time to interacting with your board
            1. Appreciate that the board outranks the CEO. Let your board members challenge your ideas and actions, and demonstrate to them that your activities are benefiting the company’s shareholders.
            2. It often happens that a new CEO who perceives the need for change will take charge of implementing it, often becoming too hands-on and enmeshed. Your board can help you avoid getting entangled in details so you can maintain your focus on strategic, long-term thinking.
            3. Your first year as CEO is arguably the most decisive period in your entire CEO journey. It is when you make your mark as a leader – signaling to your organization and the market that you were not only the right choice, but that you have what it takes to lead the business to even greater heights.
            4. The most important element in any CEO’s successful relationship with a board is a mutual embrace of transparency. When Mark Clouse took over as CEO at Campbell’s, for example, company performance was faltering, and trust between the board and management had collapsed. Clouse committed to sharing all the details of the business with the board and to reframing the relationship between the board and the CEO as a collaboration toward common goals.
        5. Shape your company’s culture through your principles and actions
            1. A business culture is a collective attitude toward fundamental values. Everything – from who joins the team to who gets rewarded or penalized – reflects your company’s culture.
            2. Employee morale is an important measure of a culture’s health. 
            3. As CEO, you are ultimately responsible for the culture of your organization.

    n. Related materials
        1. GetAbstract: How to Untie a Balloon - A Negotiator’s Guide to Avoid Popping Under Pressure - Kwame Christian
           https://www.getabstract.com/en/summary/how-to-untie-a-balloon/50618
            1. Highlights
                1. We don’t rise to the level of our expectations; we fall to the level of our training
                2. Pressure has a unique way of forcing us to get honest with ourselves about ourselves

        2. GetAbstract: Data Storytelling in Marketing - How to Tell Persuasive Stories Through Data - Caroline Florence
           https://www.getabstract.com/en/summary/data-storytelling-in-marketing/50235
            1. Highlights
                1. The best data stories adhere to the “5Rs.”
                    1. Your data stories must be “relevant” to your audience and “robust” enough to withstand scrutiny. They must feature “refined” messaging, be “relatable” on a human level, and strike listeners as “remarkable” — prompting them to take a desired action.
                2. Tailor your data story to your audience’s context and concerns to make it relevant
                3. A robust data story can withstand critical evaluation
                4. A refined data story has a clear, unambiguous message
                5. A relatable story moves beyond data intelligence to emotional intelligence
                6. To create a remarkable story, the storyteller must engage in creative thinking to deliver an original (原创性) insight
                    1. Socialization is a crucial step in making a data story remarkable.
                7. There are five mindsets that can transform you into a “data storytelling champion.”
                    1. Know your end goal — As Stephen Covey writes in The 7 Habits of Highly Effective People, effective data storytellers “begin with the end in mind,” meaning they start off with a clear vision of where they want to go.
                    2. Prioritize curiosity — Curiosity leads to great storytelling — after all, the curious analyst wants to learn new things and see the world in fresh ways. Curiosity isn’t efficient. In fact, asking questions can be inefficient. But data storytellers must devote time and effort to seeking answers, with the understanding that reaching new insights is rarely a linear process.
                    3. Think about the story all the time
                    4. Embrace the mess
                    5. Collaborate deliberately

        3. GetAbstract: You’re the Boss - Become the Manager You Want to Be (and Others Need) - Sabina Nawaz
           https://www.getabstract.com/en/summary/youre-the-boss/50036
            1. Highlights
                0. practical tools, such as the “Time Portfolio,” the “Delegation Dial,” the “Trigger Spotter,” and many more
                1. the skills that helped you climb to the top may not be the ones you need to stay there
                    1. Team performance — not personal excellence — now determines success, requiring a mindset shift from competition to collaboration
                    2. When you’re a leader, your team looks to you for protection, order, and direction. They will scrutinize your every word and action for hidden meanings. Your jokes will seem funnier, your ideas more brilliant, and your team will seek to connect with you on a personal level by learning details about your life. Instead of trying to avoid the spotlight, learn to manage it.
                2. Recognize how power can distort your perceptions
                    1. However, when the “Power Gap” grows too wide, your perception of yourself can become distorted. You might think you’re leading brilliantly when, in fact, you’re merely insulated from your missteps because your team withholds honest feedback for fear of negative repercussions.
                    2. A lack of honest input can keep you from knowing when to change how you manage your team.
                    3. Set aside the belief that you’re always right or above the rules.
                        1. Clinging to a “Singular Story” and pushing away any proposed alternative widens the gap between you and your team, which can lead them to engage in “quiet quitting” or other forms of resistance, such as taking more sick days than needed
                        2. Instead of clinging to one story — yours — consider at least three alternative perspectives — especially when you’re confident you’re absolutely right
                3. Change is hard; take small steps and track your progress.
                    1. “Cost vs. benefit analysis”
                    2. “Micro habits”
                        1. As a micro habit, at the end of each day, identify one thing you did well and one thing you’d like to improve.
                    3. “Yes list”
                4. Collaborate rather than compete
                    1. To narrow that power gap, solicit honest, specific feedback. 
                        1. For example, ask about one thing you can do more or less of; 
                        2. use scaling questions, such as asking how your performance rates on a scale from one to ten; 
                        3. or “externalize the ask,” by, for example, creating distance between the speaker and feedback by asking what a super critical person might say. 
                        4. Listen deeply to the feedback. Stay fully present and engaged by paraphrasing your team’s answers and asking follow-up questions.
                5. Be a clear communicator.
                    1. For example, if poorly communicated, your team members might interpret a simple suggestion to improve their presentation skills as a threat to their job security.
                    2. To prevent this problem, familiarize yourself with the most common communication fault lines
                        1. Uneven feedback: Don’t only give corrective feedback or simple praise. Follow the 5:1 rule: Offer five positive pieces of feedback for every corrective one. Ensure that your feedback highlights the action you praise and its impact.
                        2. Assuming cluelessness: Don’t assume your team lacks expertise in a given area or is entirely unaware of elements of their work that need improvement. Before trying to teach a team member how to do something, ascertain what they already know. Before giving feedback, first ask employees to rate their own performance. Note any misalignments between how you and your employees see their performance and work with them to set clear individual goals that tie into the overall team’s goals and desired outcomes.
                        3. Verbal overkill - Don’t dilute your key message by speaking too much or too soon. In group settings, aim to be the third person to speak at the earliest, take “margin notes” to capture your comments and questions about other people’s ideas, and start your remarks by paraphrasing what others have already said.
                        4. Sage speak: Don’t assume everyone understands your jargon. Verify that your audience understands the meaning of what you say.
                        5. The past experience divide: Don’t rely solely on your prior experiences. Focus on empathizing with and understanding your team’s current context and challenges.
                        6. Unspoken messaging: Don’t let nonverbal cues convey the wrong message. Create a map of your “personal operating system.” Map, for example, whether you’re an introvert or extrovert, prefer to think alone or brainstorm with others, or are a morning or night person. Then, communicate your operating system to your team.
                        7. The uncalibrated megaphone: Don’t let your requests and comments sound more important than you intend. Offer clarity and context by adding a rating system to your remarks — say, a one-to-ten scale — that indicates a task or a piece of corrective feedback’s importance.
                6. Manage pressure to avoid bad boss behaviors.
                    1. Overcome poor reactions to pressure with the “Trigger Spotter” tool
                    2. As a micro habit, spend 30 seconds at the end of each day reflecting on moments of high emotion and their causes.
                    3. As soon as pressure arises, our hungers take over. - 一旦压力出现，我们的欲望就会占据上风
                        1. To stop this behavior, use the “Hunger Tracker” tool
                7. Delegate effectively and take control of your time to avoid burnout
                    1. The belief that you must handle everything yourself depletes your energy and makes your team less competent. Escape that belief with the “Delegation Dial” (授权调节器)
                        1. Identify a team member’s competency on a scale from 
                            1. unconscious incompetence — no competency in a task — to unconscious competence — the ability to perform a task automatically. 
                            2. Based on a team member’s level, turn your delegation dial to one of five options
                                1. “Do” — Complete the task yourself while letting a team member assist or observe.
                                2. “Tell” — Outline clear expectations of what the team member needs to do. Offer specific examples.
                                3. “Teach” — Provide step-by-step guidance and feedback.
                                4. “Ask” — Act like a coach, asking what that person needs and what the team member is learning.
                                5. “Safety net” — Offer support while letting the team member take charge.
                        2. As a micro habit, ask someone on your team at least one coaching question daily rather than offering direct instructions.
                    2. We create portfolios to manage our money — why not create one for our time?
                        1. good thinking
                8. Create space for big ideas
                    1. When you’re “mired in minutiae” — studying the details of a spreadsheet you don’t need to know, for example — you will have difficulty thinking clearly, creatively, and strategically
                        1. Busyness is a fabulous excuse to hide behind.
                            1. Good. This is a hard, but an imminent challenge that I'm facing
                    2. “Blank Space” tool
                        1. Block out two hours per week in your calendar like any other commitment. During that time, focus on easy activities that let your mind wander, such as hiking, driving, or swimming. Choose a theme to loosely reflect on during these blank spaces, such as a work challenge or your team. Be patient with mental restlessness, and recognize that emotional resistance will try to pull you away from your commitment to maintaining this time each week.
                9. Realign your work with a deeper sense of purpose.
                    1. Whether it’s gaining financial security, supporting your family, or making an impact, your “why” drives you forward and gives you a sense of purpose. But under pressure, you may lose sight of that sense of purpose, impeding your motivation.
                    2. Regain your sense of meaning with the “Joyline” tool.
                        1. Start by listing 10–20 critical moments in your life. Include highs — such as a promotion — and lows — such as a personal loss. Plot these moments on a vertical line, placing highs on one side and lows on the other. Look for recurring themes, common factors and emotions, or influential people that reveal an overarching narrative. Your joyline can reignite your motivation, and you can use it as a compass to guide how you delegate, spend your time, and communicate with your team.

        4. GetAbstract: Strategic - The Skill to Set Direction, Create Advantage, and Achieve Executive Excellence - Rich Horwath
           https://www.getabstract.com/en/summary/strategic/49208
            2. Highlights
                1. imitating a competitor is not a strategy. Instead, Horwath urges you to differentiate your business by developing its distinctive qualities, not by lowering your prices
                2. To set your strategy, use the GOST Framework, which covers goals, objectives, strategy, and tactics
                    1. The Rule of Touch helps you discern between strategies and tactics. If you can physically touch a component of a planned action, it is a tactic, not a strategy
                3. Apple CEO Tim Cook acknowledges that while business schools extol diversification, not concentration, Apple rejects this philosophy. Instead, it focuses on a narrow range of specific offerings and opportunities
                4. Companies that compete only on price tend to underperform
                5. To replace multitasking with monotasking, batch your work, or work on similar tasks at the same time to sharply reduce transitions among different tasks. For example, during his leadership tenure at Twitter and Square, Jack Dorsey was a monotasker. He focused on management matters on Monday, products on Tuesday, marketing and growth on Wednesday, partnerships and developers on Thursday, and recruiting and corporate culture on Friday.
                6. To inspire your workforce, you need three kinds of written declarations of purpose: 
                    1. a mission statement that explains why your organization exists, 
                    2. a vision statement that sets out the company’s aspirations, 
                    3. and a values statement listing the core beliefs that guide your decision-making and actions.
                7. Companies tout their business models during the start-up phase, and then often ignore them. Yet ongoing updates to business models enable companies to attain total shareholder returns that are 7% greater than similar rivals’ returns. 
                    1. Update your business model by focusing on customers before and after they buy from you. 
                    2. An amended business model, for example, could include changes to the way customers purchase a product or service, or how the company delivers goods or services, as well as changes to product usage, retention, and disposal.
                8. Never treat different strategic options as mutually exclusive 
                9. Use meeting efficiently
                    1. Use meeting to make decision, rather than to share information
                        1. Interesting thinking
                    2. If one person does more than half of the talking, the event is a monologue, not a meeting

        5. GetAbstract: The Innovative Leader - Step-By-Step Lessons from Top Innovators for You and Your Organization - Stephen Wunker, Hari Nair and Jennifer Luo Law
           https://www.getabstract.com/en/summary/the-innovative-leader/50855
            1. Highlights
                1. An innovative leader gets their organization to act innovatively — and consistently
                    1. It is not about the individual person or any individual idea they may have, but about their ability to inspire others to become innovative in their thinking and actions
                        1. Collaboration is the key. The in productivity plane, collaboration is space that has far greater potential to grow. It does worth investment. In compare, in COGS saving, even a 5% saving YoY is hard. 
                            1. Good thinking
                    2. Innovative leaders help their organizations “CREATE” by demonstrating these behaviors
                        1. “Connected” — Leadership must personally understand customer needs
                        2. “Role model” — Demonstrate the innovative behaviors you wish to nurture within your organization
                            1. View challenges as opportunities. Stay curious, always ask questions, and seek new insights. Be willing to experiment and accept feedback
                        3. “Evolving” — Try different strategies as your market and competition change
                            1. For example, when Olam Food Ingredients began focusing on sustainability, it found markets for cascara — the husks of the coffee bean fruit — allowing them to turn a profit from a substance they once treated as waste
                        4. “Audacious” — Be bold and consider how you would run your business if you could do anything
                            1. For example, Ron Shaich noticed that his cookie store didn’t draw morning customers. So, he shifted his business to offer coffee, soup, and sandwiches in addition to baked goods, giving rise to the successful restaurant chain, Au Bon Pain. 
                        5. “Three-sixty thinker” — Don’t restrict innovation to only new products. Innovate in every aspect of your business.
                            1. For example, General Motors overtook automotive leader Ford by offering potential buyers financing. 
                            2. For example, Princess Cruises developed wearable Wi-Fi devices for customers that automatically tracked their locations, thus eliminating their need to wait in long lines when they boarded or departed the ship, or attended dinners and events.
                        6. “Enabler”  “推动者” — As film directors do, bring together a talented cast and crew who collaborate to produce great results.
                            1. Build teams with diverse mindsets, backgrounds, and perspectives, and keep teams small enough to make efficient decisions.
                    3. “Aspire” to define clear goals that prioritize innovation and drive results
                        1. Many organizations promote the need to innovate, but fail to clarify what they mean by “innovation.” 
                            1. To some stakeholders, innovation may mean investing in technology, developing new products, better serving current customers, or getting measurable results within a near-term period. 
                            2. Others may regard innovation as creating new markets, transforming the business, or pursuing projects that won’t see a return on investment for half a decade. 
                            3. Gain consensus on the kind of innovation that makes sense for your organization. Your company may be in a position to take on a considerable risk, or you may need to start smaller.
                        2. Set measurable goals that align with the innovation you want to generate.
                            1. One company might set a goal, for example, of establishing a new business line that brings in $5 million. 
                            2. DBS Bank viewed innovation as getting employees to try new approaches, so the company set a goal of completing one thousand experiments — of any kind and with any results — in the coming year.
                            3. Clothing giant Levi Strauss & Co., established a core innovation goal of incorporating advanced technology into manufacturing. In pursuing this goal, Levi’s developed a process for creating distressed jean finishes using lasers instead of environmentally harmful chemicals. 
                    4. “Build” consistent processes for developing, evaluating, and pursuing new ideas.
                        1. Examples
                            1. Some companies, such as Apple, depend on top leadership to direct innovation. 
                            2. Others, such as Google and Logitech, expect people throughout the company to develop ideas. 
                            3. Philips and Procter & Gamble rely on in-house innovation departments to develop marketable new concepts, 
                            4. while Meta and Colgate acquire start-ups or partner with outside organizations. 
                            5. Some innovators prefer to start new companies when they have novel ideas, thus keeping each company small and nimble.
                    5. “Cultivate” an organizational culture that equips and motivates people to innovate
                        1. the “Three As” - Action, Assurance, Accountability
                        2. the “Three Cs” - Capabilities, Carrots, Connections
                    6. Train yourself and your team to suggest bold ideas
                        1. In the world of innovation, ideas are cheap. Companies usually don’t suffer from a lack of ideas; the challenge is acting on those ideas
                    7. Spark innovation with inspiring and educational events
                        1. For example, Pharmaceutical and biotech company Bayer, encourages employees to form teams and seek executive support for their ideas, then receive three months of coaching from innovation consultants. A panel of top leaders then selects 10 ideas to develop fully. Since the program focuses on teamwork, new skills, and executive sponsorship, even teams that don’t win gain valuable innovation experience.
                    8. Sustain momentum by reminding people why innovation matters
                        1. Innovative leaders are constantly selling innovation
                            1. To make your message memorable, engage your audience with short, relatable stories that feature real-world models
                            2. For example, college football player Kevin Plank saw a need for moisture-wicking athletic wear. He sold apparel from his grandmother’s basement until contracts with the National Football League led him to grow his company, Under Armour.

28. Joe Magerramov: The New Calculus of AI-based Coding
    https://blog.joemag.dev/2025/10/the-new-calculus-of-ai-based-coding.html
    1. Good. Showing future path of agentic coding. The author has nice articles with deep insights in the dark corners of system engineering
    2. Highlights
        1. Agentic coding literally increase coding speed by 10x
            1. bottleneck shows up the whole CI/CD chain, other parts need speedup support too
            2. human coordination is another bottleneck
            3. Technologies (e.g. wind tunnel testing) that are previously has clear definition, but too expensive due to need to maintain large code base, are now possible because agentic coding reduces cost by 10x
        2. Practical usecase
            1. Let coding agent maintain mock external dependencies (wind tunnel)
    n. Related materials from the same author
        1. The Nuanced Reality of Throttling: It's Not Just About Preventing Abuse
           https://blog.joemag.dev/2025/06/the-nuanced-reality-of-throttling-its.html
            1. Interesting points
                1. Throttling protects customer from misuse cost
                2. Throttling should trigger auto scaling
                3. How to do "harm" properly when throttling starts to enforce
                4. Instead of hard limits, you admit new requests as long as your system has capacity. But as soon as congestion builds up, the traffic lights on the onramp activate and begin metering new cars
        2. The Trouble with Leader Elections (in distributed systems)
           https://blog.joemag.dev/2025/03/the-trouble-with-leader-elections-in.html
            1. Highlights
                1. Trade offs
                    1. Blast radius - big leader vs small localized leaders
                    2. Leases and liveness
                        1. short lease, expires before task done, new leader conflicts with old leader
                        2. long lease, liveness loss, and false live leaders
                    3. Idempotent co-leaders
                2. Different architectures
                    1. Using a queue (like SQS) to enqueue housekeeping items as they arise and then processing those using a small fleet of subscribers.
                    2. Using capabilities of the platform to perform housekeeping tasks (e.g. using AutoScaling Groups to replace unhealthy hosts or S3 lifecycles to delete expired objects).
                    3. Using event driven approaches (e.g. using a Lambda to trigger an action when S3 object changes, instead of centrally recomputing all files in the bucket).

        3. The mathematics of redundancy
           https://blog.joemag.dev/2024/01/the-mathematics-of-redundancy.html
            1. Highlights
                1. Failure formula: independent, correlated, cascaded
                    1. P_system_failure = (P_uncorrelated)^n + P_correlated + (1-(1-P_casading)^n)
                        1. Good. Exponential law isn't effective under cascading failure. If 4 engine replicas cause cascading failure, we would prefer only 1 engine.

        4. Batching: Efficiency under load
           https://blog.joemag.dev/2023/02/batching-throughput-and-latency.html
            1. Optimization technique
                1. In DPDK (or similar) queue polling, a small backlog can pile up in queue. The poller should dequeue a batch rather than a single request. 
                    1. In another word, batching can also be used in low latency scenario, this is the interesting part

        5. Performance and efficiency
           https://blog.joemag.dev/2022/12/performance-and-efficiency.html
            1. Highlights
                1. Performance optimization is usually put to lower priority in project management, but this is wrong. See below 
                2. Performance is a customer facing "feature", that can even dictate product roadmap
                3. Performance has direct mapping to COGS saving. E.g., reduce the number of hosts needed
                4. Reduce performance variability. It is needed by security, to fence against DoS and side channel attack.

29. Facebook Engineering: How do you test your tests?
    https://engineering.fb.com/2020/12/10/developer-tools/probabilistic-flakiness/
    1. Good. we've developed a measure of test flakiness: the probabilistic flakiness score (PFS)
    2. Highlights
        1. Bayes modeling
            1. Result_test(version of code, state of world, flakiness)
            2. P_b - the probability of bad state
               P_f - the probability of failure in good state
            3. P(P_b,P_f | history of a test) = P(history of a test | P_b,P_f) * P(P_b,P_f) / P(history of a test))
        2. Coordination between CI/CD and dev
            1. Metric is trust

21. Facebook: 10X Backbone: How Meta Is Scaling Backbone Connectivity for AI
    https://engineering.fb.com/2025/10/16/data-center-engineering/10x-backbone-how-meta-is-scaling-backbone-connectivity-for-ai/
    1. High performance
        1. Meta has architected Backbone in two different networks: Classic Backbone (CBB) and Express Backbone (EBB)
        2. BBB scaling
            1. pre-build DC metro architecture 
            2. IP platform scaling
                1. Introducing ZR technology
```
