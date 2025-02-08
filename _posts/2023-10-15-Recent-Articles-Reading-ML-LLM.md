---
layout: post
title: "Recent Articles Reading: Machine Learning and LLM"
tagline : "Recent Articles Reading: Machine Learning and LLM"
description: "Recent Articles Reading: Machine Learning and LLM"
category: "Paper Reading"
tags: [ML, paper, LLM, AI]
---
{% include JB/setup %}

Large Language Model / LLM. Training in distributed framework and parallel models. GPT-4V.

````
8. ChatGPT 为什么不用 Reward-Model 的数据直接 fine-tune，而用 RL？ - Andy Yang
   https://www.zhihu.com/question/596230048/answer/3002469682
    1. 多样性角度：不仅仅生成SL指定的“正确答案”, "rather than trying to replicate the human responses directly"
       负反馈角度
       自我知识感知角度：不要编造
    n. related materials
        1. Reinforcement Learning for Language Models
           https://gist.github.com/yoavg/6bff0fecd65950898eba1bb321cfbd81
            1. The core argument
                1. There are (at least) three modes of interaction with a language model
                    1. (a) text-grounded: we provide the model with a text and an instruction ("summarize this text", "based on this text, what is the population of Israel", "what are the chemical names mentioned in this text", "translate this text to spanish", etc), and expect the answer to be fully grounded in the provided text.
                    2. (b) knowledge-seeking: we provide the model with a question or instruction, and expect a (truthful) answer based on the model's internal knowledge ("What are common causes of flu").
                    3. (c) creative: we provide the model with a question or instruction, and expect some creative output. ("Write a story about...")
                2. The argument for RL is based on interaction type (b): knowledge-seeking queries in which we expect a truthful (or confident) answer, and the ability of the model to say "I don't know" or refuse to answer in situations in which it is uncertain.
                3. We cannot use pure supervised learning to push the model for producing truthful answers, and we thus must use RL for this
        2. ChatGPT SL vs RL
            1. Supervised Learning: Learns from labeled data to make predictions or classifications.
            2. Reinforcement Learning: Learns by interacting with an environment to optimize a long-term reward.

9. MLsys各方向综述 - Pentium PRO
   https://zhuanlan.zhihu.com/p/104444471
    1. very good, USB CS294 is the key course for MLsys
    1. directions
        1. 分布式机器学习（Distributed DNN Training）
            1. 分布式ML系统设计
            2. Edge Computing
            3. 大量计算资源的Scheduling / device placement
            4. communication相关
            5. 其他sys for ML可做的坑
                1. 存储 / Data Management
        2. 深度学习模型压缩/加速
            1. 通过Quantized（量化）降低计算精度要求
            2. 新硬件 / DL Acclerator
            3. 矩阵算子优化
            4. AutoML
        3. 深度学习框架/系统设计
            1. Deep Learning Framework
            2. Inference / Model Serving
            3. 深度学习编译器
        4. 用ML优化传统的system问题
            1. 数据库参数、操作系统页表、数据库索引
            2. 同样的scenario，使用更合适的ML算法
            3. 寻找system界更多可以ML化的场景
    n. related materials
        1. AI-Systems Distributed Training - Joseph E. Gonzalez
           https://ucbrise.github.io/cs294-ai-sys-fa19/assets/lectures/lec06/06_distributed_training.pdf
            1. optimized for iteration and multi-stage computation
            2. Spark, DistBelief, Parameter Server, Ring All-Reduce, Double Binary Tree All-Reduce
            3. With more machines added, batch size is becoming larger, larger batch size isn't always well
                1. Scale the learning rate linearly with the batch size
            4. Dimensions of Parallelism
                1. Data Parallelism
                    1. Synchronous Execution (Most Common)
                    2. Asynchronous Execution (Popular in Research)
                2. Model Parallelism
                    1. Divide the model across machines and replicate the data
                    2. How to best divide a model
                        1. Split individual layers
                        2. Split across layers
                
                3. Pipeline Parallelism
                    1. Combine model and data parallelism to concurrently process multiple layers and batches
                    2. GPipe: Easy Scaling with Micro-Batch Pipeline Parallelism
                    n. related materials
                        1. PipeDream: Generalized Pipeline Parallelism for DNN Training    [2019, SOSP, 510 refs]
                           https://arxiv.org/abs/1806.03377
                            1. Pipeline model parallelism, cut model layers
                            2. PipeDream: 数据并行+流水线
                               https://zhuanlan.zhihu.com/p/336849279
                                1. "简单的说就是一个动态规划模型：把M层的网络分给N个节点算"
                                2. "实际上目前最主流的分布式深度学习框架用的都是sync SGD" .. "虽然有很多人提出了async SGD的训练，但是经过无数研究者的检验，发现它带来的精度损失所造成的负面影响远远大于应用它提升的性能。"

                4. Operator Level Parallelism
                    1. Exploiting the parallelism within linear algebra and convolution operations
            n. related materials
                1. How Does Ray, a Distributed AI System, Powers OpenAI's ChatGPT?
                   https://www.analyticsinsight.net/how-does-ray-a-distributed-ai-system-powers-openais-chatgpt/
                    1. ChatGPT背后的开源AI框架Ray，现在值10亿美元
                       https://www.51cto.com/article/743834.html
                2. Deep Learning: A Primer on Distributed Training — Part 1 - Shivam Bharuka
                   https://shivambharuka.medium.com/deep-learning-a-primer-on-distributed-training-part-1-d0ae0054bb1c
                    1. Activation Checkpointing
                    2. Networking
                        1. Backward pass can be overlapped with optimizer pass
                        2. Gradient bucketing
                        3. Synchronization Frequency
                        4. Hybrid PS — All-reduce
                            1. Herring. Use parameter server based data parallelism for aggregating gradients globally across nodes. Use reduce-scatter and all-reduce operation for gradient averaging locally amongst GPUs in a single node.
                3. Parameter Servers and AllReduce
                   https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/parameter-servers 
                    1. Parameter Servers
                        1. Bounded Delay or Stale Synchronous Parallel(SSP)
                    2. Gaia: Geo-Distributed Machine Learning Approaching LAN Speeds
                        1. It is infeasible to move the geo-distributed(or geo-generated) data to a centralized data center before running an ML algorithm over it
                        2. Approximate Synchronous Parallelism (ASP) is based on a key finding that the vast majority of updates to the global ML model parameters from each ML worker machine are insignificant.
                            1. With ASP, these insignificant updates to the same parameter within a data center are aggregated (and thus not communicated to other data centers) until the aggregated updates are significant enough.
                    3. Ring AllReduce
                        1. The main issue with the parameter server's communication strategy(e.g. one parameter server and multiple workers) was that the communication cost grew linearly with the number of GPUs in the system.
                        2. In contrast, a ring allreduce is an algorithm for which the communication cost is constant and independent of the number of GPUs in the system
                        n. related materials
                            1. 浅谈Tensorflow分布式架构：ring all-reduce算法
                               https://zhuanlan.zhihu.com/p/69797852

        2. UCB的CS294 19spring/fall
           https://ucbrise.github.io/cs294-ai-sys-sp19/
           https://ucbrise.github.io/cs294-ai-sys-fa19
           https://ucbrise.github.io/cs294-ai-sys-sp22/
           https://berkeley-deep-learning.github.io/cs294-131-s19/
            1. good
            2. CS 294-131: Trustworthy Deep Learning (Special Topics in Deep Learning)
                1. https://berkeley-deep-learning.github.io/cs294-131-s19/
                    1. security/privacy
                    2. adversarial examples
                    3. causality
                    4. fake news defense
                    5. explainability
                    6. uncertainty

        3. CS294: Scheduling Deep Learning Workloads
           https://ucbrise.github.io/cs294-ai-sys-sp19/assets/lectures/lec27/dl-scheduling.pdf
            1. key aspects
                1. Maximize throughput
                2. Fairness
            2. related: Dominant Resource Fairness (DRF) presentation 
        
        4. Model Compression - Joseph E. Gonzalez
           https://ucbrise.github.io/cs294-ai-sys-sp19/assets/lectures/lec22/network_compression.pdf
            1. Approaches to “Compressing” Models
                1. Architectural Compression
                    1. Layer Design - Typically using factorization techniques to reduce storage and computation
                        1. MobileNet Paper
                        2. ShuffleNet paper
                    2. Pruning - Eliminating weights, layers, or channels to reduce storage and computation from large pre-trained models
                2. Weight Compression 
                    1. Low Bit Precision Arithmetic - Weights and activations are stored and computed using low bit precision
                    2. Quantized Weight Encoding - Weights are quantized and stored using dictionary encodings
            
            n. related materials
                1. Efficient Processing of Deep Neural Networks: from Algorithms to Hardware Architectures - Vivienne Sze [2019, NIPS]
                   http://eyeriss.mit.edu/2019_neurips_tutorial.pdf?ich_args2=526-06113205060278_e0b61138dc2d908aa0766d50302e6d8a_10001002_9c896324d5cbf0d49239518939a83798_92e0a859ed6aa28355c3deea32562911
                   https://www.youtube.com/watch?v=geLeDFFl8UQ
                    1. 10:00 - 20:00, Very useful charts to understand how DNN works in the networking structure and how to calculate dimensions
                    2. Key metrics and design objectives in DNN, and DNN processor
                        1. Accuracy, latency, throughput.
                        2. Energy of power, hardware cost, range of DNN tasks (flexibility), scalability
                        3. MAC/data, MAC/cycle (PE count) matching issue
                        4. Data movement with DRAM dominates energy consumption
                    3. CPU & GPU Platforms
                        1. Matrix multiplication
                            1. reduce number of multiply, replace with addition
                            2. Fast Fourier Transform
                        2. More MAC per cycle
                            1. SIMT/SIMD
                            2. reduce precision
                        3. Memory access is the bottleneck
                            1. Input data reuse
                        4. High parallelism
                        5. Energy vs Accuracy
                            1. Energy ~ Exp(Accuracy)
                2. The Ultimate Guide to Deep Learning Model Quantization and Quantization-Aware Training - opensource SuperGradients by Deci 
                    https://deci.ai/quantization-and-quantization-aware-training/
                    1. edge devices are resource-constrained
                    2. The model size can typically be reduced by two to four times
                    3. post-training quantization (PTQ) and quantization-aware training (QAT)
                    4. scale quantization: Max, Entropy, Percentile
                    5. Types of Quantization: Naive, Hybrid, and Selective
                    6. selecting the appropriate quantization method, identifying sensitive layers, and fine-tuning your models using quantization-aware training
                    7. Useful Best Practices
                        1. Tips for Post Training Quantization
                            1. Use per-channel granularity for weights and per-tensor for activation
                            2. Quantize residual connections separately by replacing blocks
                            3. Identify sensitive layers and skip them from quantization
                        2. Tips for Quantization-Aware Training
                            1. Start with the best-performing calibrated PTQ model
                            2. Fine-tune for around 10% of the original training schedule
                            3. Use cosine annealing LR schedule starting at 1% of the initial training LR
                            4. Use SGD optimizer with momentum instead of ADAM or RMSProp

        5. ModelDB: An open-source system for Machine Learning model versioning, metadata, and experiment management
           https://github.com/VertaAI/modeldb
            1. Referenced in parent article as "训练数据的规模是很大的。如何为ML设计一个专用的文件系统（类似大数据界的HDFS）或者数据库来加速读数据呢？ 类似的工作有管理ML model的ModelDB."
            2. key features
                1. Make your ML models reproducible
                    1. model version control
                    2. model metadata
                2. Manage your ML experiments, build performance dashboards, and share reports
                3. Track models across their lifecycle including development, deployment, and live monitoring
            3. Verta Enterprise MLOps Platform
               https://docs.verta.ai/verta/
                1. Experiment Management
                2. Model Catalog
                3. Model Deployment
            4. related materials
                1. Versioning Your ML Models using ModelDB
                   https://songrcs.medium.com/versioning-your-dataset-and-models-using-modeldb-10b0ee3873ed
                2. Model Versioning Done Right: A ModelDB 2.0 Walkthrough - Verta AI
                   https://www.youtube.com/watch?v=U0lyF_lHngo
                    1. why not GIT
                        1. not for large file
                        2. not working with DBMS nor libraries
        
        6. AI-Systems Machine Learning Lifecycle
           https://ucbrise.github.io/cs294-ai-sys-fa19/assets/lectures/lec03/03_ml-lifecycle.pdf
            1. key concepts
                1. Hyperparameters
                2. Model Pipelines, Features, and Feature Engineering
                3. Warm Starting and Fine Tuning
                4. Feedback Loops, Retraining and Continuous Training
            2. model development, training, inference
                1. 80% time spent in data preparation
                2. model composition
                3. inference with Model updates, Feature updates

        7. 深度学习加速：算法、编译器、体系结构与硬件设计 - meton
           https://zhuanlan.zhihu.com/p/101544149
            1. very good article. summarizing wide ranges of aspects with inter-connection
            2. highlights
                1.算法顶层
                    1. 大规模分布式机器学习（并行模式、调度模式、更新策略）
                    2. 优化算法
                    3. 轻量级网络设计
                    4. 神经网络架构搜索
                    5. 量化与剪枝
                    6. 卷积运算的优化、
                2. 深度学习编译器
                    1. 需求与痛点
                    2. TVM
                    3. Pytorch Glow
                    4. Tensorflow XLA
                3. 体系结构与硬件设计
                    1. 关注指标
                    2. CPU和GPU平台与其设计考量
                    3. Domain-Specific 硬件设计
                    4. 设计关注点
                    5. 深度学习应用数据重用机会
                    6. 两类设计范式：Temporal Arch. 与 Spatial Arch.
                    7. 加速器设计可以利用的特性（稀疏、低精度、压缩）

            n. related materials
                1. Parameter Servers vs AllReduce
                   https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/parameter-servers
                    1. Parameter Server是中心式存储参数，All Reduce是无中心分发参数

                2. PuDianNao: A Polyvalent Machine Learning Accelerator
                   https://www.zhihu.com/question/41216802/answer/124409366
                   https://dl.acm.org/doi/10.1145/2786763.2694358
                    1. 文章先是对七种机器学习算法的计算及访存范式进行了分析 .. 论文中花了大量篇幅，仔细分析了各类机器学习算法在访存行为、计算模式上的异同
                        1. Identify time-consuming step, next identify locality property of the time-consuming step
                            1. analyze memory bandwidth. divide-and-conquer
                            2. Tiled code
                        2. interesting
                            1. k-Nearest Neighbors
                            2. k-Means
                            3. Deep Neural Network
                            4. Linear Regression
                            5. Support Vector Machine
                            6. Naive Bayes
                            7.  Classification Tree


        8. 深度学习算法优化系列三 | Google CVPR2018 int8量化算法
           https://zhuanlan.zhihu.com/p/99424468
            1. Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference
                1. 入门量化最经典的论文之一
            2. 训练后量化(post-training-quantizated)
                1. 以int8的形式保存，但在实际推理时，还需要反量化为浮点数类型进行计算
               训练时量化(quantization-aware-training)
                1. 在反向传播的时候仍然对float类型的权重进行梯度下降，前向推理时全部使用int8的方式进行计算
            3. 这篇论文提出了一种将float32量化为int8的方法，并给出了一个训练和推理框架，推理框架使得模型可以在能执行整型运算的计算设备上高效运行，训练框架和推理框架相辅相成，可以显著降低量化过程中的精度损失。
                1. r = S(q - Z), q就是8-bit整数
                2. 纯整数算术矩阵乘法
                    1. 零点的有效处理
                    2. int32中间结果
                3. 模拟量化训练
                    1. 在前向传播阶段模拟量化的方法，反向传播和平常一样
                    2. 学习量化范围
                    3. Batch normalization层

        9. 一文看懂深度学习新王者「AutoML」：是什么、怎么用？
           https://zhuanlan.zhihu.com/p/42924585
            1. AutoML和神经架构搜索（NAS） - 搜索最优神经网络架构，你只需要提供数据
                1. "Neural Architecture Search"

        10. AI-Systems Prediction Serving - Joseph E. Gonzalez
            https://ucbrise.github.io/cs294-ai-sys-fa19/assets/lectures/lec07/07_prediction-serving.pdf
            1. Serving Pre-materialized Predictions
            2. Hybrid Offline + Online Learning
            3. VELOX Architecture
            4. Clipper
                1. Selection Policy: Estimate confidence
            5. KUNA
            6. Pretzel: Opening the Black Box of Machine Learning Prediction Serving Systems

        11. 手把手带你遨游TVM
            https://zhuanlan.zhihu.com/p/50529704
            1. "而对于Inference来说，以我之所见，其实是“群雄逐鹿”"
               "会跑到的设备可能会是多种多样的，如Intel CPU / Intel GPU / ARM CPU / ARM GPU / NV GPU / FPGA / AI芯片等"
               "我们能不能做一个基于编译优化思想的推理框架呢？答案就是：TVM"

        12. Learning Key-Value Store Design    [2019, 9 refs]
            https://arxiv.org/pdf/1907.05443.pdf
            1. Referenced in the parent article "它提出了Design Continuum的概念：存储系统中的很多数据结构本质上是很像的（arise from the very same set of fundamental design principles），例如B+tree, LSM-tree, LSH-table等，但它们却有不同的应用场景（比如KV Store中用LSM就比B+ Tree更合适），很难有一个十全十美的设计。这说明它们有相互替换的空间。这样我们可以将不同数据结构的选择也作为存储系统的一个knob，根据具体workload和硬件的情况来自动选择一个合适的底层数据结构（find a close to optimal data structure design for a key-value store given a target workload and hardware environment）。"

    2. Federated Learning at Scale - xzhu0027
       https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/towards-federated-learning-at-scale-system-design
       https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/federated-learning-at-scale-part-i
        1. Federated learning (FL) is a machine learning setting where many clients (e.g. mobile devices or whole organizations) collaboratively train a model under the orchestration of a central server (e.g. service provider), while keeping the training data decentralized.   FL allows for smarter models, lower latency, less bandwidth usage, and less power consumption, all while ensuring privacy and user experiences.
        2. applications
            1. Healthcare
            2. enterprise collaboration
            3. privacy matters
        3. security and privacy
            1. homomorphic encryption and secure aggregation
                1. encrypting the model updates such that the server can still perform the algebraic operations necessary to combine them, but updates not sent in plaintext
            2. differential privacy.
                1. The basic idea is to add random noise to the individual updates. These updates are going to be accumulated, and thus your noise should cancel with all the noise other people have added
        4. Advances and Open Problems in Federated Learning by Kairouz et al.

    3. 大模型推理框架概述 - 吃果冻不吐果冻皮
       https://zhuanlan.zhihu.com/p/659792625?utm_id=0
        1. vLLM
        2. HuggingFace TGI
        3. FasterTransformer
        4. FlexFlow Server
        5. LMDeploy

    4. 大语言模型推理性能优化综述 - Young
       https://zhuanlan.zhihu.com/p/656485997?utm_id=0
        1. very good article. The top chart summarize all directions
        2. highlights
            1. LLM推理优化
                1. 显存相关优化
                    1. KV Cache
                    2. Paged Attention
                2. 计算相关优化
                    1. 算子融合
                    2. 高性能算子
                3. 服务相关优化
                    1. Continuous Batching
                    2. Dynamic Batching
                    3. 异步 Tokenize / Detokenize
                4. 分布式相关优化
                    1. 模型并行
                        1. Column Parallel,  Row Parallel
                        2. Megatron-LM
                5. 低比特量化
                    1. 权重量化
                    2. 权重和激活同时量化
                    3. KV Cache量化
                    4. 基于硬件特点的量化：英伟达 Hopper 架构下的 FP8
                6. 其他新技术
                    1. 投机采样（Speculative decoding）
                    2. 美杜莎头（Medusa head）

19. 大模型面试八股 - 花甘者浅狐
    https://zhuanlan.zhihu.com/p/643560888
    1. very good.
    n. related materials
        1. Understanding and Coding the Self-Attention Mechanism of Large Language Models From Scratch
           https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html
            1. useful
        2. Build Better Deep Learning Models with Batch and Layer Normalization
           https://www.pinecone.io/learn/batch-layer-normalization/
            n. related materials
                1. Different Normalization Layers in Deep Learning
                   https://towardsdatascience.com/different-normalization-layers-in-deep-learning-1a7214ff71d6
        3. Understanding Backpropagation Algorithm
           https://towardsdatascience.com/understanding-backpropagation-algorithm-7bb3aa2f95fd
            1. The Challenge of Vanishing/Exploding Gradients in Deep Neural Networks
               https://www.analyticsvidhya.com/blog/2021/06/the-challenge-of-vanishing-exploding-gradients-in-deep-neural-networks/
            2. The Vanishing/Exploding Gradient Problem in Deep Neural Networks
               https://towardsdatascience.com/the-vanishing-exploding-gradient-problem-in-deep-neural-networks-191358470c11
            3. Lecture 15: Exploding and Vanishing Gradients - Roger Grosse
               https://www.cs.toronto.edu/~rgrosse/courses/csc321_2017/readings/L15%20Exploding%20and%20Vanishing%20Gradients.pdf
        4. 梯度爆炸 (exploding gradients) vs 梯度消失 (gradient vanishing)
            1. Transformers Explained Visually (Part 3): Multi-head Attention, deep dive - Ketan Doshi
               https://towardsdatascience.com/transformers-explained-visually-part-3-multi-head-attention-deep-dive-1c1ff1024853
            2. 万字长文解读Transformer模型和Attention机制 - 潘小小
               https://zhuanlan.zhihu.com/p/104393915
            3. Transformer升级之路：1、Sinusoidal位置编码追根溯源 - 苏剑林
               https://kexue.fm/archives/8231
        5. 综述blog：Processing Data for LLM
           https://wandb.ai/wandb_gen/llm-data-processing/reports/Processing-Data-for-Large-Language-Models--VmlldzozMDg4MTM2
            1. Handling junk data
            2. De-duplication
            3. Decontamination
            4. Toxicity and Bias Control
            5. Personal Identifiable Information Control
            6. Prompt Control
        6. 红雨瓢泼：一文看懂：如何充分高效训练多轮对话大模型
           https://zhuanlan.zhihu.com/p/645517143
        7. Memory cost: Transformer Inference Arithmetic - kipply's blog
           https://kipp.ly/transformer-inference-arithmetic/
        8. 当红炸子鸡 LoRA，是当代微调 LLMs 的正确姿势？
           https://zhuanlan.zhihu.com/p/618894919
        9. Current Best Practices for Training LLMs from Scratch - Rebecca Li, Andrea Parker, Justin Tenuto
           https://uploads-ssl.webflow.com/5ac6b7f2924c656f2b13a88c/6435aabdc0a041194b243eef_Current%20Best%20Practices%20for%20Training%20LLMs%20from%20Scratch%20-%20Final.pdf
            1. Very useful for introduction. Good.
            2. main domains of LLMs
                1. use commercial API vs opensource vs pre-train by yourself
                2. choose model size, training data size
                3. hardware capabilities
                    1. memory efficiency
                    2. compute efficiency
                4. Parallelization
                    1. batch size
                    2. data parallelism - training data sharding 
                        1. problems
                            1. backward pass to pass all gradients to all GPUs
                            2. replicates model and optimizer to each GPU
                    3. Tensor parallelism - divide large matrix multiplications
                        1. problems
                            1. communication cost
                    4. pipeline parallelism and model parallelism - inter-layer parallelism
                        1. problems
                            1. cannot scale flexibly due to bound to model structure
                    5. examples
                        1. Megatron-LM PTD-P technology
                        2. Estimating 🌴PaLM's training cost
                           https://blog.heim.xyz/palm-training-cost/
                            1. good as to show COGS cost estimation method
                            2. public cloud prices act as the baseline building blocks
                5. data collection
                    1. dataset diversity for LLM
                    2. dataset pre-processing
                6. Tokenization methods
                    1. Word-based tokenization
                    2. Character-based tokenization
                    3. Subword-based tokenization
                7. Pre-training steps
                    1. Experiments and Hyperparameter Search
                        1. Experiments can involve any or all of the following: weight initialization, positional embeddings, optimizer, activation, learning rate, weight decay, loss function, sequence length, number of layers, number of attention heads, number of parameters, dense vs. sparse layers, batch size, and dropout.
                    2. Training instability
                        1. avoiding loss spikes
                8. Model evaluation
                    1. popular standard evaluation benchmarks
                    2. the listing is useful
                9. Bias andToxicity
                    1. bias and toxicity benchmarks
                10. Instruction Tuning
                    1. Instruction tuning tunes full model parameters as opposed to freezing a part of them in Parameter-efficient Fine Tuning
                    2. Instruction tuning is universally effective on tasks naturally verbalized as instructions (e.g., NLI, QA, translation), but it is a little trickier for tasks like reasoning.
                    To improve for these tasks, you'll want to include Chain-of-Thought examples during tuning
                    2. Reinforcement Learning Through Human Feedback (RLHF)
                        1. an extension of Instruction Tuning
                        n. related materials
                            1. 强化学习从零到RLHF（八）一图拆解RLHF中的PPO
                               https://zhuanlan.zhihu.com/p/635757674
                            2. ChatGPT explained: A Guide to Conversational AI w/ InstructGPT, PPO, Markov, RLHF
                               https://www.youtube.com/watch?v=GMkszGzFOgw
                                1. Policy Gradients in a Nutshell - Sanyam Kapoor
                                   https://towardsdatascience.com/policy-gradients-in-a-nutshell-8b72f9743c5d
                                    1. useful to understand RL training basics
                                2. Proximal Policy Optimization (PPO) Explained
                                   https://towardsdatascience.com/proximal-policy-optimization-ppo-explained-abed1952457b
                                    1. interesting. useful.
                                3. Understanding the Finite Element Method
                                   https://www.youtube.com/watch?v=GHjopp47vvQ
                                    1. interesting. useful.
                            3. 如何直观理解PPO算法?[理论篇] - 张斯俊
                               https://zhuanlan.zhihu.com/p/111049450

    n+1. related materials
        1. PTD-P: Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM    [2021, 257 refs, NVIDIA]
           https://arxiv.org/abs/2104.04473
            1. very good. state of art work to tell how parallelism should be organized in LLM.
               the recommended approach is running tensor + pipeline model parallelism.
               leverage intra server NVLink to fit the high communication cost of tensor parallelism
               the paper also provides detailed performance formulas and analysis, which can be used as a reference
            2. highlights
                0. Key paper problem
                    1. How should parallelism techniques be combined to maximize the training throughput of large models given a batch size while retaining strict optimizer semantics?
                    2. ensure strict optimizer semantics, need sync pipeline flush, thus introduces the pipeline bubble time
                        1. Not in this paper, but Pipeline parallelism can also be implemented with relaxed semantics
                            1. Asynchronous and bounded-staleness
                1. Selene supercomputer cluster setup
                    1. ~1T parameters.
                    2. NVIDIA DGX A100 servers
                        1. 8 * 80GB-A100 CPUs, with NVLink and NVSwitch
                        2. 8 * NVIDIA Mellanox 200GB HDR Infiniband HCAs
                    3. 3072 GPUs in cluster
                        1. bisection bandwidth
                           point-to-point 892 GB/s,
                           or all-reduce 12.9TB/s 
                    4. checkpoint of size 13.8 TB
                2. formula calculation - this is the good part
                    1. pipeline bubble time fraction
                    2. memory consumption
                    3. flops and throughput
                    4. microbatch size
                    5. model parameter size
                    6. end2end training time
                3. model parallelism
                    1. pipeline model parallelism - this is the good part
                        1. innovative PipeDream-Flush (same authors) schedule. Though pipeline bubble time is the same, but it reduces needed GPU memory by limiting the number of in-flight microbatches
                        2. more optimization, interleaved stages
                        3. Limitations
                            1. designed for LLM, that each device can assign an equal number of transformer blocks
                            2. the number of model layers limits the scalability
                    2. Tensor and pipeline model parallelism
                        1. This is the recommended approach by this paper
                        2. tensor model parallelism be used to degree g, given g GPUs per server.
                           pipeline model parallelism be used to distribute across servers.
                        3. GEMM matrix multiplication in parallel
                    3. data model parallelism
                        1. data and pipeline model parallelism doesn't show better performance vs tensor and pipeline model
                            1. Note, tensor parallelism needs all-reduce communication which is expensive, but it can be done within the server leveraging high speed NVLink
                        2. data and tensor model parallelism is even worse
                        3. my questions
                            1. how about data + tensor + pipeline parallelism?
                4. other optimizations
                    1. activation recomputation
                    2. communication scatter/gather
                    3. all-reduce, ring-reduce

        2. Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, the World’s Largest and Most Powerful Generative Language Model    [2022, 325 refs, Microsoft]
           https://github.com/microsoft/Megatron-DeepSpeed
           https://arxiv.org/abs/2201.11990
           https://www.microsoft.com/en-us/research/blog/using-deepspeed-and-megatron-to-train-megatron-turing-nlg-530b-the-worlds-largest-and-most-powerful-generative-language-model/
            1. Tensor parallel intra server with Megatron, pipeline parallelism across server with Deepspeed. Training and evaluation.
            2. highlights
                1. background
                    1. In isolation, existing parallelism strategies such as data, pipeline, or tensor-slicing have trade-offs in memory and compute efficiency and cannot be used to train models at this scale.
                        1. Data parallelism achieves good compute efficiency, but it replicates model states and cannot leverage aggregate distributed memory.
                        2. Tensor-slicing requires significant communication between GPUs that limits compute efficiency beyond a single node where high-bandwidth NVLink is not available.
                        3. Pipeline parallelism can scale efficiently across nodes. However, to be compute-efficient, it requires large batch sizes, coarse grain parallelism, and perfect load balancing, which is not possible at scale.
                2. solution
                    1. The system uses tensor-slicing from Megatron-LM to scale the model within a node and uses pipeline parallelism from DeepSpeed to scale the model across nodes
                    2. mixed precision on the NVIDIA DGX SuperPOD-based Selene(opens in new tab) supercomputer powered by 560 DGX A100 servers networked with HDR InfiniBand in a full fat tree configuration
                    3. We largely built our training dataset based on prior work, The Pile
                        1. The Pile: An 800GB Dataset of Diverse Text for Language Modeling
                           https://arxiv.org/abs/2101.00027
                3. different parallelism models - this is a good introduction
                    1. problems of data parallelism
                        1. data parallelism relies on scaling the batch size with the number of data-parallel workers, and cannot be made arbitrarily large without affecting model quality
                        2. Data parallelism replicates the model and optimizer across all workers, and therefore is not memory efficient
                        3. the communication cost of aggregating gradients increases with the model size and can limit compute efficiency on large models
                    2. Tensor Model Parallelism
                        1. Tensor parallelism reduces the memory footprint of the model proportional to the number of workers
                        2. tensor parallelism requires high communication bandwidth to be efficient and is best kept within a single DGX sever where high bandwidth NVLink is available
                    3. Pipeline Model Parallelism
                        1. Pipeline parallelism reduces memory proportionally to the number of pipeline stages, allowing model size to scale linearly with the number of workers.
                            1. However, pipeline parallelism does not reduce the memory footprint for the activations of each layer. 
                            2. Additionally, each worker must store the activations for all micro-batches in flight.
                        2. Pipeline parallelism has the smallest communication overhead of the three approaches, as it only communicates the activations between the pipeline stage boundaries
                        3. The degree of pipeline parallelism is bounded by the depth of the model, and increasing the pipeline dimension decreases the compute efficiency
                            1. pipeline bubble
                4. training dataset
                    1. many details here
                5. model evaluation
                    1. many details here
                6. others
                    1. gradient accumulation optimization

            n. related works
                1. ZeRO: DeepSpeed: Extreme-scale model training for everyone    [2020, Microsoft]
                   https://www.microsoft.com/en-us/research/blog/deepspeed-extreme-scale-model-training-for-everyone/
                   https://www.microsoft.com/en-us/research/project/deepspeed/publications/
                   https://github.com/xitu/gold-miner/blob/master/article/2020/deepspeed-extreme-scale-model-training-for-everyone.md
                    1. Topology aware 3D mapping (Figure 2)
                        1. ZeRO data parallel
                            1. ZeRO & DeepSpeed: New system optimizations enable training models with over 100 billion parameters
                               https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/
                                1. the animation sounds interesting. it's an algorithm with good potential, sharded with parallel, extra communication cost, but not adding extra memory to hold temporary data
                            2. This is just the usual DataParallel (DP), except, instead of replicating the full model params, gradients and optimizer states, each GPU stores only a slice of it. And then at run-time when the full layer params are needed just for the given layer, all GPUs synchronize to give each other parts that they miss - this is it.
                        2. Pipeline parallel
                        3. Model parallel
                            1. it seems the pipeline parallel and model parallel are just referring to the pipeline model parallel in Megatron-LM paper
                        n. related materials
                            1. Model Parallelism - huggingface.io
                               https://huggingface.co/docs/transformers/v4.15.0/parallelism
                                1. DataParallel (DP)
                                2. TensorParallel (TP)
                                3. PipelineParallel (PP)
                                4. Zero Redundancy Optimizer (ZeRO)
                                5. Sharded DDP

1. 必看：微软166页论文解读 GPT-4V 中文版（精校）《多模态的新时代》 -  李秉宇 AIhackathon
   https://mp.weixin.qq.com/s/a8Y_yU5XYgJhQ2xMuTK13w
    1. 来自这些样本的观察表明，GPT-4V 在处理任意交错的多模态输入（interleaved multimodal inputs）和其能力的通用性方面具有前所未有的能力，使 GPT-4V 成为一个强大的多模态通用系统。
        1. The Dawn of LMMs: Preliminary Explorations with GPT-4V(ision)
           https://arxiv.org/abs/2309.17421
            1. interesting
    2. Highlights
        1. 括开放世界视觉理解（open-world visual understanding）、视觉描述（visual description）、多模态知识（multimodal knowledge）、常识（commonsense）、场景文本理解（scene text understandin）、文档推理（document reasoning）、编码（coding）、时间推理（temporal reasonin）、抽象推理（abstract reasoning）、情感理解（emotion understanding） ， 还有很多
        2. GPT-4V 的不同工作模式，例如指令调整（instruction tuning）、上下文学习（in-context learning）和其他紧急用途（and other emergent usages）。

2. 国产AI芯片的大模型系统的研究 - 干一行AI一行 IT生活路漫漫 
   https://mp.weixin.qq.com/s/bc9tFaftT75RpWQ9SUjb6Q
    1. 国产GPU的生态系统的10大方面
        1. 编程框架：利用基本算子快速构建人工智能模型，以降低编写人工智能模型的复杂度。例如:PyTorch，TensorFlow
        2. 并行加速：为多机多卡环境提供人工智能模型并行训练的能力，确保能够支持数据并行、模型并行、流水线并行、张量并行等。例如：微软DeepSpeed，英伟达Megatron-LM
        3. 通信库：提供跨机跨卡的通信能力，支持人工智能模型训练所需的各种通信模式，能根据底层网络特点充分利用网络通信带宽。例如：英伟达NCCL库，超算的MPI通信库
        4. 算子库：算子库提供人工智能模型所需基本操作的高性能实现，要求尽可能覆盖典型人工智能模型所需的操作，要求算子库能充分发挥底层硬件的性能。例如：英伟达cuDNN,cuBLAS
        5. Al编译器：人工智能程序的目标代码依靠AI编译器生成。对于算子库不能提供的操作，通过Al编译器可以自动生成高效目标代码。例如：XLA，TVM
        6. 编程语言：能够编写人工智能模型的基本算子，覆盖底层硬件功能以充分发挥硬件性能，支持在异构处理器上编写并行程序。例如英伟达的CUDA，Intel的OneAPI
        7. 调度器：提供在大规模系统上高效调度人工智能任务的能力。通过设计高效调度算法，提高集群资源利用率。例如：k8s，华为的ModeArts
        8. 内存分配系统：针对人工智能应用特点提供高效的内存分配策略。
        9. 容错系统：提供在硬件发生故障后快速恢复模型训练的能力。
        10. 存储系统：支持训练过程中高效的数据读写(检查点、训练数据等)。

3. Book THE ART OF ASKING CHATGPT FOR HIGH-QUALITY ANSWERS - IBRAHIM JOHN
   https://www.amazon.com/Art-Asking-ChatGPT-High-Quality-Answers/dp/B0BT2JB67Y
    1. Task, instruction, role
    2. Self-consistency prompt - "ensure the summary is consistent with "
    3. Knowledge integration prompt - "Update the existing knowledge about XX with the following information YY"
    4. Specifying the template or style
    5. Adversary prompt - "Generate text that is difficult to classify as XX." "difficult to classify as having the statement of YY."
    6. Clustering prompt - "Group the following customer reviews into clusters based on sentiment"
    8. Let ChatGPT learn examples first. Give ChatGPT examples in prompt
    9. Text classification prompt - "Classify them into different categories such as XX, YY, ZZ"
    10. How to avoid & bypass AI content detectors
        1. using high Perplexity and Burstiness method
        2. let ChatGPT incorporate your own content
        3. remove commonly used connecting words used by ChatGPT
        4. give ChatGPT your own writing style and tone
    11. Generate by seed word.
```