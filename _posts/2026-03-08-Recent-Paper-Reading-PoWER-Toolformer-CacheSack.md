---
layout: post
title: "Recent Paper Reading: PoWER, Toolformer, CacheSack"
tagline : "Recent Paper Reading: PoWER, Toolformer, CacheSack"
description: "Recent Paper Reading: PoWER, Toolformer, CacheSack"
category: "Paper Reading"
tags: [paper, cloud, LLM, storage]
---
{% include JB/setup %}


```
1. PoWER Never Corrupts: Tool-Agnostic Verification of Crash Consistency and Corruption Detection    [OSDI 2025 Best paper, 6 refs, Azure Storage, Hayley LeBlanc]
   https://www.microsoft.com/en-us/research/publication/power-never-corrupts-tool-agnostic-verification-of-crash-consistency-and-corruption-detection/
   https://people.csail.mit.edu/nickolai/papers/leblanc-power.pdf
   https://www.usenix.org/system/files/osdi25-leblanc.pdf
   https://yiyibooks.cn/boywithoutname2/PoWER_Never_Corrupts-_Tool-Agnostic_Verification_of_Crash_Consistency_and_Corruption_Detection/index.html
    1. PoWER - Preconditions on Writes Enforcing Recoverability. Though AI is grabbing all research focus, storage world still have advancement at formal verification proof.
        1. Search "Good" below to find out the (real) key contribution
    2. My reading outs
        1. What it can do?
            1. PoWER APIs. precondition. 
            2. No performance cost, only compile time.
            3. developer cannot introduce crash-consistency bugs
        2. How does it do it?
            1. require, ensure, Verus Rust
            2. ghost state, completion object
            3. Hoare logic and quantifier, which are supported by most verification tools
        3. Comparable works
            1. vs TLA+, vs PSpec
                1. TLA is not required, use preconditions are simpler
        4. Limitations
            1. The storage model we use is based on the prophecy-based asynchronous disk model [62]
            2. Concurrency, PoWER cannot reason about writes executing concurrently with other reads/writes to the same storage region
        5. How it helps PMEM exactly
            1. Listing 6
            2. Corruption Detection Boolean (CDB)
            3. CAPYBARAKV and CAPYBARANS
        6. Why exactly PoWER needs Rust?
            1. Memory Reasoning needs Rust. Also, as mentioned in VeriBetrKV, Rust is needed for heap memory reasoning, much simplified Dafny dynamic frames
            2. Verus can verify a subset of unsafe Rust features [10], and it rejects usage of features outside that subset
            3. Related to "Verus: Verifying Rust programs using linear ghost types"
                1. Linear Ghost Types: This is a central innovation. "Ghost types" are auxiliary types and data structures used solely for verification, without affecting the runtime behavior of the program. "Linear" refers to the property that these ghost types, like regular Rust types, adhere to linearity and borrow checking rules, allowing proofs to manipulate "permissions" that correspond to memory, pointers, and concurrent resources.
                2. OK .. this also explains the linear types in VeriBetrKV

    2. Highlights
        1. Difference to VeriBetrKV
            1. VeriBetrKV adds TLA-styel reasoning to Dafny, needs state machine. However, steep learning curve.

        2. What exactly does PoWER do compared to VeriBetrKV?
            0. From: https://chatgpt.com/share/690b69d8-1dec-800f-8dd6-04005473bca8 
                     https://chatgpt.com/c/690b691f-d774-8323-8499-669d3887d583
            1. The key idea: instead of relying on exotic logics (e.g., Crash Hoare Logic, or TLA refinement), you stay within standard Hoare logic + ghost variables + quantifiers (which most verifiers support) and add preconditions on each durable write API call saying: “all crash states that result from this write must be permitted/legal.”
            2. PoWER also includes a set of proof/implementation strategies (tentative writes, committing writes, recovery writes, in-place writes) backed by libraries, to help users discharge the preconditions without having to manually enumerate all weird crash branches.
            3. On the corruption detection side, the paper improves over VeriBetrKV by offering a more flexible model of media corruption: it does not require data + checksum to be in the same block or atomically updated together. Instead, it models media corruption as “some bit-mask flips up to a bounded count c” and uses CRC semantics to reason about detection.

        3. How does PoWER know if a crash write state is legal?
            1. Instead of modelling the OS or NVM hardware explicitly, PoWER attaches a quantified precondition to every durable write operation in the code.
                1. fn write(addr: Ptr<T>, val: T)
                     requires ∀crash_state ∈ possible_crash_states(addr, val):
                        recover(crash_state) ∈ GoodStates
            2. My questions
                1. Implementation of "possible_crash_states" is not disclosed by the paper

        4. Strategies for satisfying preconditions - Good part
            1. Tentative write - modify data at unreachable address
                1. Example: Write metadata/log first
            2. Committing writes - An atomic write to change system state
                1. Example: Flip commit bit last
            3. Recover writes - Writes done in recovery
                1. Example: Fix corruption during recovery
                2. Must be idempotent (crash in recovery) and only modify bytes that will be written to by a completed recovery 
            4. In-place writes - Non-atomic modify user visible states
                1. Example: Update stable structure directly
                2. Bad for crash consistency

        5. Extending PoWER to concurrent contexts, VerusSync
            1. My questions
                1. This is the real work, because the "pre/post condition" approach is by nature weak to handle multi-threading, as mentioned in VeriBetrKV "Floyd-Hoare reasoning".
                2. The solution in this chapter is good.
            2. From: https://chatgpt.com/share/690b69d8-1dec-800f-8dd6-04005473bca8
                1. This is NOT mentioned in the original paper. But I think it is even doing better.
                2. The new idea: Thread-local crash consistency specifications
                    1. Each thread can be verified locally (modularly)
                    2. Yet the composition of all threads is still crash-consistent globally.
                3. Core concept
                    1. a rely condition: what crash behavior it can assume about other threads, and
                    2. a guarantee condition: what crash behavior it must ensure for others
                4. Each memory region (say, a key/value entry, or a metadata block) is treated as a resource R
                    1. exclusive persistent permission (full ownership): they can modify R and are responsible for ensuring PoWER’s precondition on their writes to R, or
                    2. shared read permission: they can read R, but must assume others’ writes satisfy their PoWER preconditions.
                5. The concurrency extension rule
                    1. ∀ interleaving of writes W1, W2, ...
                        if each thread’s writes satisfy its PoWER precondition
                        and threads respect ownership of persistent regions,
                        then ∀ crash_state S, recover(S) ∈ GoodStates
                    2. That’s PoWER’s concurrency theorem
                        1. crash-safety is compositional under non-interfering PoWER-verified threads

        6. CDB - corruption-detecting Boolean
            1. CDB is a bool value atomically written to PM. It is a atomic pointer to switch which data version is valid.

        7. CapybaraKV
            1. Github: https://github.com/microsoft/verified-storage
            2. PMEM KV store built on Rust and verified by Verus
            3. Let's use it as the example to learn Verus

    n. Related materials
        1. VeriBetrKV Storage systems are distributed systems (so verify them that way!)    [2020, 69 refs, OSDI 20]
           https://www.usenix.org/conference/osdi20/presentation/hance
            1. State machine Dafny for disk crash consistency. 
                1. Referenced by PoWER as TLA-style reasoning, prove properties related to asynchrony, crash consistency, and liveness, but with steep learning curve
                    1. While Verus is the Floyd-Hoare pre-/post-conditions approach
            2. My reading outs
                1. What is it exactly?
                    1. VeriBεtrKV crash-safe kv store based on Be-tree, written in Dafny, compared via C++
                    2. Modeling Asynchronous Systems
                        1. We demonstrate that we can use this approach for other asynchronous systems, like our disk system
                    3. Modeling disk system
                        1. System<Host> state machines is a convenient and flexible way to encode environmental assumptions
                    4. Dafny dynamic frame - Memory Aliasing
                    5. Linear type systems
            
            3. Highlights
                1. Floyd-Hoare reasoning ... pre-/post-conditions ... popular for single-threaded imperative programs ... do not consider asynchronous interaction
                    1. That's the Verus approach. VerusAsync did enhance multi-threading condition

                2. Linear type system
                    1. What problem it solves?
                        1. Heap memory usage reasoning
                        2. Dafny rely on an SMT solver to reason about aliasing and ownership, e.g. Dafny uses dynamic frames [32], where programmers annotate methods with modifies clauses to specify which objects each method may modify
                            1. which provides programmers with great flexibility, but painfully slows verification
                    
                    2. What is it exactly?
                        1. Rust point to an alternate strategy, where the language’s type checker quickly takes care of memory safety and ensures non-aliasing
                        2. See "Linear Ghost Types" in Verus. Linear means 

                    3. What does "linear" mean? From humata.ai
                        1. Non-Aliasing and Mutable
                        2. No Duplication or Silent Discarding 
                        3. Explicit Deallocation
                        4. Enabling Efficient In-Place Updates
                        5. Simplified Reasoning

        2. Verus: A practical foundation for systems verification    [2024, 54 refs, Hayley LeBlanc]
           https://www.andrew.cmu.edu/user/bparno/papers/verus-sys.pdf
           https://github.com/verus-lang/verus
            1. Base technology that supports PoWER and well integrated with Rust. Quite popular on Github, with well written documents
                1. Good, based on reputation, website, documentation, this is the outcome that worth invest. A long climb from Dafny. Rust solved the tricky memory aliasing problem as mentioned in VeriBetrKV
            2. My reading outs
                1. What is Verus exactly?
                    1. Rust, with keywords spec, requires, ensures (pre/post sconditions)
                2. How does Verus work?
                    1. underlying SMT solver
                    2. standard Floyd-Hoare logic to convert proof obligations
                    3. The net effect is that Verus sends queries that are simpler and smaller by orders of magnitude to the SMT solver
                    4. Selective Use of EPR for Full Automation
                    5. Automated Reasoning for Multi-Threading
                        1. Resource Algebras 
                        2. ghost resources
                        3. VerusSync
                3. Innovative techniques
                    1. See how does it work
                4. Runtime overhead
                    1. Unanswered. But Figure 7 has veriifation time compare

            3. Highlights
                1. None

        3. Dafny: An automatic program verifier for functional correctness    [2010, 1664 refs, Microsoft Research]
           https://www.microsoft.com/en-us/research/wp-content/uploads/2008/12/dafny_krml203.pdf
           https://dafny.org/
           https://github.com/dafny-lang/dafny
            1. The root technology backing Verus and VeriBetrKV. If you check https://dafny.org/, the language look similar
                1. Dafny running in "Visual Studio Code"
            2. My readings out
                1. What are the key features of Dafny?
                    1. Pre- and Postconditions - requires, ensures
                    2. Ghost State
                        1. the variables are used in the verification of the program but are not needed at run time
                    3. Dafny is language that supports function, data types, set, sequence, etc
                        1. and, algebraic datatype
                2. How does it work exactly?
                    1. Dafny program -> Dafny verifier -> translate to Boogie language -> applied tby many automatic program verifiers -> generate first-order verification conditions -> passed to a theorem prover, SMT solver Z3.

2. CloudBuild: Microsoft's Distributed and Caching Build Service    [2016, 118 refs]
   https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/q_signed-2.pdf
   https://eng.ms/docs/cloud-ai-platform/devdiv/one-engineering-system-1es/1es-build/cloudbuild/intro
    1. CloudlBuild is currently being used by more than 4000 developers in Bing, Exchange, SQL,OneDrive, Azure and Office. Build speedup ~3x or more, always compatible to old tooling. 
        1. The system looks straightforward but actually not trivial. See "my reading outs" and search for "good" keywords.
    2. My reading outs
        1. What does CloudBuild do exactly?
            1. Distributed build. Maven, Ant etc cannot do it.
        2. How does CloudBuild work?
            1. Backed by AutoPilot cluster management, 
                1. cluster manager - worker, zookeeper
        3. How does CloudBuild speed up building?
        4. How does CloudBuild manage artifacts and versions?
            1. Artifact Repository built on top of Azure Blob Storage
            2. Integrated into Visual Studio
            3. Progressive upload during build, and incremental download
        5. How is cache being used?
            1. cache key is content hash + path hash + inputs settings + global settings + rand session id
            2. cache mapping is managed by Azure Tables. Build worker caches partial local copies.
            3. upon cache hit, copy the cache replica to requester node.
            4. cache removal is by time based expire.
        6. How to shard a build into smaller parallel reusable parts?
            1. DAG scheduling
        7. How to manage availability of build system?
            1. AutoPilot, Zookeeper
        8. How is build dependency managed?
            1. Use nmake and msbuild
            2. Problem: under-specified, see example in Figure 3
                1. infer hidden dependency, but a large set of rules to apply against the build specification ASTs
                    1. Even robocopy.exe invoke are parsed
                    2. Good. This is the technology that solves a "hard" problem, with much manual efforts
                2. Let user add annotation
        9. How to onboard existing tools with minimal effort?
            1. CloudBuild Commitment to compatibility
        10. How to handle the caching of non-deterministic tool invoking?
            1. See 4.3 "Non-Deterministic Build Outputs". It exposes bugs and app owners are happen to fix
        11. How to manage sandbox and security of build?
            1. See section 3.4. It is a directory with symbolic links to resource files
                1. My questions
                    1. What a pity that Microsoft didn't invent container like Google did. What is being used here is like a beggar version.
                    2. And previously Windows doesn't have Container
            2. CloudBuild uses Detour binary injection to observe which files are accessed
        12. How are symbolic linking handled?
            1. See sandbox
        13. Build scheduling
            1. DAG, actionable task, critical path, resource profile estimate, blocked tasks
            2. overlap fetching delay
            3. retry, retriable, and retry on different nodes
            4. input locality, cache aware scheduling
            5. My questions
                1. why not schedule jobs with Yarn, Mesos
    3. Highlights
        1. history
            1. CloudBuild was started to enable Bing's fast delivery cadence
        2. Figure 1: CDF of tools by usage
            1. My questions
                1. There is no head concentration nor long tail pattern, no 20/80 rule. Interesting, this is an example that 20/80 rule won't apply, but which have many scenarios in devops

3. Toolformer: Language Models Can Teach Themselves to Use Tools    [2023, 2595 refs, Facebook]
   https://arxiv.org/abs/2302.04761
   https://yiyibooks.cn/arxiv/2302.04761v1/index.html
    1. Founding paper that demonstrates the great potential for LLM to call external tools.
        1. There are previous works, but the key contribution of this paper is self-supervised with few human intervention
    2. My readings out
        1. What exactly is Toolformer?
            1. Training Toolformer with GPT-J. Key steps are in Figure 2: Filter to keep only calls that reduce next-token loss
            2. Train with self-supervised without requiring large amounts of human annotations.
                1. Given just a handful of human-written examples of how an API can be used, we let a LM annotate a huge language modeling dataset with potential API calls. We then use a self-supervised loss to determine which of these API calls actually help the model in predicting future tokens
                    1. Good approach. This is generic that LLM can train itself.
                2. Prompts are listed in Appendix A.2
            3. Model finetuning
                1. See chapter 2
            4. No degradation when API calls are disabled
        2. What is beyond just let LLM select tools and call?
            1. Not in paper scope. 
        3. What does it mean to let LLM team themselves in this context?
            1. See training
        4. How to resolve the problem that there are too many tools to select?
            1. Not in paper scope. 
        5. A big example that LLM uses tools to do fancy job?
            1. No such example. But the paper gives evaluation on different datasets
        6. What are the best practices to write tools?
            1. Not in paper scope. 
        7. How to integrate the Toolformer into commercial models like ChatGPT?
            1. Not in paper scope. 
    3. Highlights
        1. ChatGPT summaries
           https://chatgpt.com/share/690ffce4-4140-800f-8aeb-c851647278c0

    n. Related articles
        1. LLM Agent System Development - 静水流深
           https://en.zhihu.com/article/29975037546
            1. Logged elsewhere. Good. It constructs the knowledge framework for LLM agent
            2. Core: Toolformer, ReAct, and AutoGPT
        
        2. ReAct: Synergizing Reasoning and Acting in Language Models    [2022, 5771 refs, Google]
           https://arxiv.org/abs/2210.03629
            1. Good paper. It brought LLM agent design into the new stage. "thoughts -> action -> observation" and loop.
            2. My readings out
                1. What is the baseline of ReAct?
                    1. Chain of Thought
                        1. Problem: Missing group truth from external response, results in Hallucination
                    2. Action plan generation
                        1. Problem: Missing reasoning and abstracting about high-level goals, nor maintaining working memory
                2. What exactly does ReAct do and how it works?
                    1. The key source is "thoughts -> action -> observation" loop.
                3. How should ReAct be used in LLM agent?
                    1. 
                4. The performance of ReAct?
                    1. Absolute improve 34% and 10%, only need two or even one-shot prompting. Over ALFWord and Webshop, which used imitation or reinforcement learning with 10^3~10^5 task instances.
                5. What are the test dataset and evaluation method of ReAct?
                    1. Using well established test sets. HotpotQA and Fever

        3. AutoGPT - ReAct agent framework
           https://github.com/Significant-Gravitas/AutoGPT
           https://agpt.co/
            1. From chatgpt: https://chatgpt.com/c/693516b1-cbb8-8322-9e2a-2d0597bc117a

            n. Related materials
                1. Multi-modal agent
                   https://chatgpt.com/c/693417c0-9c28-8321-bd16-13458840e43a


        4. LlamaIndex - Agent's data framework
           https://github.com/run-llama/llama_index
           https://developers.llamaindex.ai/python/framework/
           https://www.llamaindex.ai/
            1. From chatgpt: https://chatgpt.com/c/693417c0-9c28-8321-bd16-13458840e43a

        5. AutoGen - multi-agent orchestration 
           https://github.com/microsoft/autogen
            1. Microsoft Agent Framework
               https://github.com/microsoft/agent-framework
            2. Related
                1. Semantic Kernel
                   https://github.com/microsoft/semantic-kernel
                    1. From MS and for single agent. Semantic Kernel is the earlier work of AutoGen

                2. timeline
                    1. LLM-Driven Agentic AI
                        1. ReAct framework (2022): interleaving reasoning and actions in LLMs
                        2. AutoGPT & BabyAGI (2023): open-source multi-step planning/discovery agents
                        3. LangChain, AutoGen, and function-calling APIs (2024–25): turnkey agent toolkits

        6. LangGraph
           https://docs.langchain.com/oss/python/langgraph/overview
           https://chatgpt.com/c/693417c0-9c28-8321-bd16-13458840e43a

        7. Multi-modal agent
           https://chatgpt.com/c/693417c0-9c28-8321-bd16-13458840e43a

4. Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot    [FAST 2025 Best paper, 81 refs, Moonshot AI Kimi]
   https://www.usenix.org/conference/fast25/presentation/qin
   https://arxiv.org/abs/2407.00079
    1. Unified caching tiering VRAM, DRAM, SSD. Compute/storage co-design. User chat aware cache scheduling. Prefix vs Incremental KVCache. Chunked pipeline parallelism (CPP). Targeting vLLM KVcaching's problems.
    2. My readings out
        1. What is unique in the Mooncake KV cache architecture?
            1. a global scheduler named Conductor
            2. KVCache transfer
                1. Topology-aware path selection
            3. multi-tier spanning VRAM, DRAM, and SSD
            4. Prefix vs Incremental KVCache
            5. a unified address space for all KV tensors, abstracting away their physical location
            6. Chat-Session–Aware Scheduling
                1. Detecting session idleness
            7. Chunked pipeline parallelism (CPP)
        2. Any KVCache disaggregation?
            1. This is the prior work
        3. What is special for the LLM Chatbot scenario?
            1. See bullet 1
        4. What makes Mooncake better than vLLM KVCaching?
            1. vLLM's problems
                1. VRAM-only caching
                2. No session awareness
                3. Compute recomputation trade-off ignored, 
                    1. vLLM doesn’t distinguish prefix/incremental KV
                    2. Once VRAM is full, vLLM either drops old sessions or recomputes past tokens from scratch (high compute cost)

    3. Highlights
        1. Prefix KVCache vs Incremental KVCache
            1. Keep incremental cache resident in VRAM
            2. Gradually merge and demote it into prefix cache stored in DRAM/SSD when session is idle
            3. Prefetches prefix blocks before next generation

5. How to Copy Memory? Coordinated Asynchronous Copy as a First-Class OS Service    [2025, 0 refs]
   https://ipads.se.sjtu.edu.cn/_media/pub/sosp25-copier-preprint.pdf
    1. Good idea, to embed coping into as a system level service in Linux . The idea is borrowed from GPUs which provides hardware primitives for async copy.
        1. See Table 1. Overview of systems with copy optimizations
    2. My readings out
        1. What is the API definition
            1. See figure 4 programming model
            2. See table 2, high level interface and low level interface
        2. What are today's copy technologies and what are their shortcomings?
            1. Memory sharing, remapping, Zero copy
            2. on-chip DMA, SIMD instructions
        3. What are the key technologies in this paper?
            1. dynamically switching DMA vs CPU AVX copy according to task size, and parallel executing both
            2. ATCache
            3.  cross-privilege copy, cross-address-space copy. intra-boundary and inter-boundary copy.
            4. Section 4.5.4 Proactive fault handling, need to lock VA's physical mapping
        4. What are the unique optimizations that are only possible by this design?
            1. lazy copy, but prioritize queued request if caller requests read, and deprioritize head of queue blocking ones
                1. out-of-order execution
            2. cgroup resource constraints by copy length
            3. overlapping copy and consume, allow (segment-ed) consume before copying finished. bitmap tracking segment completion. 
            4. Figure 8, layered absorption of unnecessary copies
        5. What are the usage scenario?
            1. Huawei Smartphone HarmonyOS
        6. Limitations
            1. Copier costs more CPU cycles
            2. 
    2. Highlights
        1. None

    n. Related materials
        1. zIO: Accelerating IO-Intensive Applications with Transparent Zero-Copy IO    [OSDI 2022, 26 refs]
           https://www.usenix.org/conference/osdi22/presentation/stamler
            1. Intercept kernel calls to avoid user/kernel copy, and plus copy-on-write protection. 1x~2x throughput improvement and cpu reduction. 17% improvement compared to zero-copy IO stack APIs
                1. See section 2.4 summary for limitations of zero-copy IO stacks    
            2. My readings out
                1. What is zIO exactly? And how it works?
                    1. Unified buffer mapping: Instead of separate user-space and kernel-space buffers, zIO allows the kernel’s page cache pages to be directly mapped into the process’s address space. This lets user code read or write data in place without copying
                    2. Copy-on-write protection: Because the same physical page may be shared between kernel and user, zIO enforces memory protection rules (using page faults and ref-count tracking) to prevent corruption. If the user modifies a shared page that must stay immutable, zIO automatically falls back to making a private copy.
                    3. Transparent interception: zIO intercepts read()/write() syscalls and redirects them through its fast path when safe; otherwise, it reverts to the normal kernel path.
                    4. Cross-stack unification: It coordinates across filesystem cache, network stack, and block I/O layers to maintain correctness and cache coherence
            3. Highlights


6. RoPE: RoFormer: Enhanced Transformer with Rotary Position Embedding    [2021, 4362 refs]
   https://arxiv.org/abs/2104.09864
    1. Good paper. Relative positional encoding widely adopted in 
    2. My readouts
        1. What is the path that led authors invented RoPE?
            1. Observation 1, only relative position matters.
               Observation 2, if decompose the q^t*k matrix with absolute position sinusoidal encoding , it is multiply q^t and k with a rotation matrix
               Observation 3, relative position information is not useful beyond a certain distance
            2. Formula 16, rotation from Q and K are "transfer-able". 
               Rotation depends only on distance not position not token vectors

        2. What is the intuition behind RoPE?
            1. Rotation with sin/cos matrix, this is from the earliest Absolute Positional Encoding

        3. What is the math behind RoPE?
            1. See paper. Pretty elegant

        4. How is RoPE evaluated?
            1. Transformer by RoPE - RoFormer.
            2. English-to-German translation
            3. GLUE: MRPC, SST-2, QNLI, STS-B, QQP, MNLI(m/mm)

        5. What are other comparable methods to RoPE?
            1. Absolute position embedding, see section 2.2
            2. Relative position embedding, see section 2.3

        6. What makes a well positional encoding?
            1. Depend on relative position diff
               Composes naturally with dot-product attention
               Bounded to max value 1
               Capture prev/next word, also capture long distance
               Preserves token semantics
               Workable with super long context length

        7. Why RoPE is needed to apply to K, Q at each attention layer?
            1. This is specified in paper. 
                1. RoPE is applied on Q, K, so much be on each attention layer
                2. RoPe is NOT applied to q, k. It must be applied after WQ, WK applied.
                3. RoPE is NOT applied to v nor V. 
    
    3. Highlights
        1. Chapter 2.1 Preliminary, very useful attention formula in compact and professional form
        2. the hypothesis that precise relative position information is not useful beyond a certain distance

    n. Related materials
        1. Positional Encoding Explained: A Deep Dive into Transformer PE
           https://medium.com/thedeephub/positional-encoding-explained-a-deep-dive-into-transformer-pe-65cfe8cfe10b
            1. Useful explanation for how Sinusoidal Encoding and RoPE works.

        2. Is RoPE applied in each attention layer?
           https://www.reddit.com/r/LocalLLaMA/comments/1apn1dy/is_rope_applied_in_each_attention_layer/
            1. Yes. Absolute Position Encoding (Sinusoidal Encoding) is applied at the beginning of Transformer (at the embedding layer). But ABE is for older architectures.
               Llama, Mistral archs use RoPE embeddings on Q and K just before the attention mechanism. RoPE is applied to every attention layer.


7. GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding    [2020, 1841 refs, Google]
   https://arxiv.org/abs/2006.16668
   https://yiyibooks.cn/arxiv/2006.16668v1/index.html
    1. Good. GShard is the founding paper of MoE. MoE is the founding technology to expand super large model.
       Besides, GShard uses annotations and simple APIs to automatically do partitioning, backed with compiler extension in XLA.
    2. My readouts
        1. What is the MoE in GShard?
            1. GShard, which only requires the user to annotate a few critical tensors in the model with partitioning policies. It consists of a set of simple APIs for annotations, and a compiler extension in XLA [28] for automatic parallelization.
            2. The other parts are similar with what described in DeepSeek-V3 paper
               https://arxiv.org/pdf/2412.19437

        2. What leads to building MoE?
            1. Super large model, 600B parameters
            2. Need Sub-linear Scaling
            3. Expert level parallelism

        4. What properties are necessary to make MoE work well?
            1. Gate function is critical
            2. Balanced the load
            3. Efficiency at scale
            4. Auxiliary loss for LB bias
            5. Sparse activation

        5. Why MoE targets FFE layer rather than attention?
            1. Not mentioned in this paper, but ChatGPT has reply
               https://chatgpt.com/c/693f44ab-c7ac-8324-954a-b5c0e6487619
                1. FFN is token-wise; attention is token-pair-wise.
                2. FFN dominates majority of parameters
                   https://mp.weixin.qq.com/s/WXrgxV3LgYYvRLPTVzLkjw

        6. How effective is the evaluation?
            1. 600B model with GShard, able to be trained on 2048 TPU v3 accelerators in 4 days

        7. Does MoE reduce the GPU memory needed?
            1. No. It won't reduce memory, because all experts need to be loaded. But it can reduce the Activation memory used in training.

    n. Related materials
        1. Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity    [2021, 3524 refs, Google]
           https://arxiv.org/abs/2101.03961
            1. High referenced MoE implementation paper.
            2. My readouts
                1. What does Switch Transformer do?
                    1. A Differentiable Load Balancing Loss
                        1. This is the formulas in DeepSeek-V3 paper
                    2. Designing expert-parallelism

                2. What is the difference compared to GShard?
                    1. GShard is categorized to extend XLA compiler for MoE

            2. Highlights
                1. "We observe a clear trend: when keeping the FLOPS per token fixed, having more parameters (experts) speeds up training." (Figure 4)
                2. "Do sparse models outperform dense models on the speed-accuracy Pareto curve? Yes."

        2. DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models    [2024, 686 refs]
           https://arxiv.org/pdf/2401.06066
           https://yiyibooks.cn/arxiv/2401.06066v1/index.html
            1. Expanding "DeepSeek-V3 Technical Report" on the MoE part
            2. My readouts
                1. What is the problem and challenges?
                    1. Existing MoE architectures potentially suffer from issues of knowledge hybridity and knowledge redundancy
                2. What does DeepSeekMoE do differently?
                    1. Fine-Grained Expert Segmentation
                    2. Shared Expert Isolation

        4. Nvidia Megatron-LM - Mixture of Experts package - Megatron Core MoE
           https://docs.nvidia.com/megatron-core/developer-guide/latest/api-guide/moe.html

        5. 一文搞懂DeepSeek的技术演进之路：大语言模型、视觉语言理解、多模态统一模型 - 魔方 AI 空间
           https://mp.weixin.qq.com/s/xYD4eprGvr2aS7lXzGHIuQ?token=1471301116&lang=zh_CN
            1. Useful summary of what each does from DeepSeek LLM, DeepSeek V2, DeepSeek V3, DeepSeek R1

8. RedPajama: an Open Dataset for Training Large Language Models
   https://arxiv.org/pdf/2411.12372
   https://github.com/togethercomputer/RedPajama-Data
    1. Replication of Llama training dataset and data processing pipeline
    2. My readouts
        1. What kind of data cleaning is used?
            1. See "4.1 Data Processing Steps"
                1. How much natural language it is
                2. Repetitiveness
                3. Harmful content blocking

        3. What are the key properties that make well datasets?
            1. quality signals accompanying each document

        4. What is in the dataset?
            1. RedPajama-V1 dataset, an open reproduction of the dataset used to train LLaMA-1
            2. RedPajama-V2 dataset, the largest open pretraining dataset consisting of raw, unfiltered data scraped from the web, together with 46 measures of quality computed for each document

        5. Evaluation?
            1. Table 5 evaluating how effective is dataset filters
               For each dataset, we train 468M llama-2 on 100B tokens and the 1.6B model on 350B tokens.
               Evaluate the model on metrics at Table 4

    n. Related materials
        1. 为什么说大模型训练很难？ - bigpunch的回答
           https://www.zhihu.com/question/498271491/answer/1981120245616906843
            1. "这里推荐大家关注一下RedPajama或者The Pile这些开源数据集的处理流程。特别是RedPajama，他们详细披露了如何复刻LLaMA的数据配方，里面关于数据清洗、质量过滤的细节非常有参考价值。"

        2. Understanding Perplexity
            1. ChatGPT
               https://chatgpt.com/c/693f44ab-c7ac-8324-954a-b5c0e6487619
                1. L =− 1/3 * ( ln0.5 + ln0.25 + ln0.25) ≈ 1.155
                   PPL = e^1.155 ≈ 3.17

                   L = - 1/T * sum t=1..T (log P(x_t | x_<t))
                   PPL = e^L

                2. Perplexity is exponential(cross-entropy loss (sum of all tokens output))
                3. smaller PPL is better
                4. Transformer model outputs the logits of the vocabulary, apply softmax to it. this is how P(x_t | x_<t) is obtained.

            2. 困惑度(perplexity)的基本概念及多种模型下的计算（N-gram, 主题模型, 神经网络）
               https://zhuanlan.zhihu.com/p/114432097


9. CacheSack: Admission Optimization for Google Datacenter Flash Caches    [2022, 29 refs, ATC22]
   https://www.usenix.org/conference/atc22/presentation/yang-tzu-wei
    1. Different categories of workload share the flash cache on the server. How to assign cache policy to each category?
       
       Forget the "high-tech" buzz wording and formulas from the google paper. It is simply
        1. Given an imaginary cache retention time D, and past metrics (ghost cache), we can calculate the cost/saving per each category and cache policy.
        2. Greedily assign policy to category one by one for who has the best cost/saving ratio
        3. The last category may not have enough cache size left, just assign a % of cache policy, here comes "fractional"
        4. We don't know true D priori, just try all possible D values and find the best.
        5. 
           The whole problem is just a simple greedy problem, to assign policies to categories.
           But nice paper writing to make it look "high-tech" buzzing.

       Real time run cache optimization per every 5min. Collect real time metrics in ghost cache. Each cache server do its optimization and history collection independently.
        
        1. Good methods of formulating the problem and solve it. Except the buzz high-tech wording formulas. Good to understand Google Colossus architecture and Colossus Flash Cache.
        
        2. Category is predefined by human, rather than recognized by ML. 
           Instead, policy assignment is an optimization problem.
           This is nice simplification that bypassed pitfalls
    
    2. My readings out
        1. How is index service done, and especially HA?
            1. Not a key topic in paper. Just partition cache by key space, and in each server do ghost cache and algorithm
        2. How to solve Write Amplification / Wear Out issue with flash
            1. Not a key topic in paper. Just reduce the flash writes. Modeled as cost in knapsack problem.
        3. Colossus workload cache admission/ejection algorithm
            1. prior work
                1. LARC: >60% data is only accessed once. Only admit in second access.
                    1. Problem: misses all first cache hits.
                2. Colossus buffer cache
            2. Traffic by category (e.g. Spanner column family)
               Admission cache policy by category
                1. AdmitOnWrite (most aggressive)
                2. AdmitOnMiss (LRU)
                3. AdmitOnSecondMiss (LARC)
                4. NeverAdmit
            3. Formulate a fractional knapsack problem
                1. Solution: find the optimal fraction per policy per category (e.g. 30% LARC, 10% NeverAdmit, to same category)
                2. Run entire optimization every 5 minutes in real time (automatic cache optimization)
                3. CacheSack uses a ghost cache, the lookup table for all last access times to compute inter-arrival times
        
        4. Caveats in the cache policy assignment algorithm
            1. See summary from https://chatgpt.com/c/699abfa2-bc20-83a0-ae53-067d2bfc74aa
            2. Step 1: Given a predefined cache retention time D, the observed access history in ghost cache can be used to compute the cost (disk reads, cache usage by byte-seconds, bytes written) of each cache policy (AdmitOnWrite, AdmitOnMiss, AdmitOnSecondMiss, NeverAdmit)
            3. Step 2: Formulating the optimization problem
                1. The base problem can be formulated as a fractional knapsack problem - given fixed cache size, take in as many blocks to cache as possible, so as to maximize the total saving (or to reduce the total cost). 
                    1. Different categories are sharing the cache. % of blocks of a category is what to be put into the "pack".
                2. fractional knapsack problem can be solved by simple greedy solution (unlike 0/1 knapsack). 
                   But there is a problem, a category maps into 4 items to pack, one item per each cache policy. However, the 4 items are inter-coupled, their sum % must equal to 1. How to solve this "variant" of "fractional knapsack problem"?
                3. For each category, construct function F(cache usage). More cache usage assigned to that category, lower total cost. The function is a piecewise‑linear function, each viable cache policy maps to a linear segment.
                    1. In each line segment of F, it connects two cache policies. Fully taken one linear segment means to 100% go to a policy. Partially take a middle point of a linear segment means to take say 70% of a policy, then 30% of another.
                    2. My questions
                        1. Instead of saying "convex hull" etc buzz word, it is simply a cost/saving plot on bi-policy transition. It is a simple a greedy problem. 
                            1. Figure 16 shows why "lower convex hull" is needed
                4. Greedy cache policy assignment. Gradually assign cache usage to each category. Per each assignment step, pick a category whose linear segment is steepest, i.e. best saving ratio to per unit cache usage.
                   The last segment may be partially used, resulting in one category getting a mixture of two policies; all other categories end up with a single policy
            4. Step 3: Repeat over retention times. 
                1. The true retention time 𝐷 is not known a priori. CacheSack try 127 predefined D_i values, in a geometry distribution space.
                2. Finally, it then selects the configuration with minimal cost across all D values.
                3. My questions
                    1. D maps a policy to the cache size used. Likely this step is to resolve it.
                    2. Selecting the D_i giving best saving, doesn't mean you can actually enforce D_i in the real running?
            5. Each cache‑index server performs this optimization independently, using its own collected metrics in 5min window.
                1. Note, different categories of workload share the flash cache on the server.

    n. Related materials
        1. Kangaroo: Caching Billions of Tiny Objects on Flash
        2. The CacheLib Caching Engine: Design and Experiences at Scale
        3. Facebook CacheLib
```
