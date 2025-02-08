---
layout: post
title: "ChatGPT papers and Prompt Engineering"
tagline : "ChatGPT papers and Prompt Engineering"
description: "ChatGPT papers and Prompt Engineering"
category: "Paper Reading"
tags: [NLP, GPT, LLM, AI]
---
{% include JB/setup %}

Foundation papers of ChatGPT.

```
1. Transformer: Attention Is All You Need    [2017, 69872 refs]
   https://arxiv.org/abs/1706.03762
    1. Revolutionized Machine Translation area. Founding cornerstone for ChatGPT
    2. highlights
        1. key technologies - Prior work Seq2Seq model
            1. Self-attention mechanism
                1. No recurrence, no RNN. This allows fast parallel training with GPU
            2. Multi-head attention
            3. Positional encoding
        2. How is attention vector calculated?
            1. HUMATA: The attention vector is calculated using the Scaled Dot-Product Attention mechanism, which is a type of attention function. The input to this attention function consists of queries and keys of dimension dk, and values of dimension dv. The dot products of the query with all keys are computed, divided by the square root of dk, and a softmax function is applied to obtain the weights on the values. In practice, the attention function is computed on a set of queries simultaneously, packed together into a matrix Q. The keys and values are also packed together into matrices K and V. The matrix of outputs is then computed using the formula: Attention(Q, K, V) = softmax(QKT / sqrt(dk))V This formula computes the attention weights for each query in Q, based on the dot product of the query with all keys in K, and then applies these weights to the corresponding values in V to obtain the final attention vector.
            2. How are Q, K, V calculated?
                1. HUMATA: In the Transformer model, the Q, K, and V matrices are calculated by linearly projecting the input embeddings into query, key, and value vectors. Specifically, for each input token, the embedding is multiplied by three learned weight matrices to obtain the query, key, and value vectors. These weight matrices are learned during training and have dimensions of (embedding size x attention dimension), where the attention dimension is a hyperparameter that determines the size of the query, key, and value vectors. Formally, given an input sequence of embeddings X with dimensions (sequence length x embedding size), the query matrix Q, key matrix K, and value matrix V are calculated as follows: Q = XW_Q K = XW_K V = XW_V where W_Q, W_K, and W_V are the learned weight matrices for the query, key, and value projections, respectively. The resulting Q, K, and V matrices have dimensions of (sequence length x attention dimension). These matrices are then used as inputs to the attention mechanism to compute the attention weights and the final output of the model.
    n. related materials
        1. Transformer Neural Networks - EXPLAINED! (Attention is all you need)
           https://www.youtube.com/watch?v=TQQlZhbC5ps
            1. very similar to "Transformer Neural Networks: A Step-by-Step Breakdown"
        2. Transformer Neural Networks: A Step-by-Step Breakdown
           https://builtin.com/artificial-intelligence/transformer-neural-network
            1. RNN: Feed the last model output and Xi to the next model input
            2. LSTM: Add a pass through branch to RNN
                1. Still have problems
                    1. Vanishing gradient after ~1000 words
                    2. Slow training
                2. Training of LSTM: Backpropagation Through Time (BPTT)
                    1. ChatGPT: "BPTT works by unfolding the LSTM network over time, treating it as a deep feedforward network with shared weights across time steps"
                       https://chat.openai.com/chat/3753b4da-4f94-4f0a-82f0-e9d1641b857d
                        1. So, LSTM/RNN is a DNN with as many layers as the time step. Each layer shares the parameter
                    2. Truncated Backpropagation Through Time
                       https://machinelearningmastery.com/gentle-introduction-backpropagation-time/
                        1. ChatGPT: "In truncated BPTT, the sequence is split into smaller subsequences, and BPTT is applied separately to each subsequence."
                    3. STAT 453: Intro to Deep Learning - L15.4 Backpropagation Through Time Overview - Sebastian Raschka
                       https://www.youtube.com/watch?v=0XdPIqi0qpg
                       https://sebastianraschka.com/pdf/lecture-notes/stat453ss21/L15_intro-rnn__slides.pdf
                    4. Werbos, Paul J. "Backpropagation through time: what it does and how to do it."
                       https://axon.cs.byu.edu/Dan/678/papers/Recurrent/Werbos.pdf 
                    5. Backpropagation Through Time - Technical Fridays
                       https://kharshit.github.io/blog/2019/02/22/backpropagation-through-time
                        1. with math formulas
            3. seq2seq-models: Visualizing A Neural Machine Translation Model (Mechanics of Seq2seq Models With Attention)
               https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/
                1. useful materials to learn how transformer works in animation
                2. An attention model differs from a classic sequence-to-sequence model
                    1. Instead of passing the last hidden state of the encoding stage, the encoder passes all the hidden states to the decoder
                    2. Multiply each hidden state by its softmaxed score, thus amplifying hidden states with high scores
                3. What are Word Embedding?
                   https://machinelearningmastery.com/what-are-word-embeddings/
                    1. A word embedding is a learned representation for text where words that have the same meaning have a similar representation.
                    2. capture a lot of the meaning/semantic information of the words (e.g. king - man + woman = queen)
                    3. Each word is represented by a real-valued vector, often tens or hundreds of dimensions. This is contrasted to the thousands or millions of dimensions required for sparse word representations, such as a one-hot encoding.
                    4. Word Embedding Algorithms
                        1. Embedding Layer - as part of a neural network model. trained together with the model
                4. seq2seq model vs Transformer
                    1. seq2seq model still uses RNN. But Transformer has zero recurrence, all needed is attention
                       https://medium.com/saarthi-ai/transformers-attention-based-seq2seq-machine-translation-a28940aaa4fe
                        1. seq2seq model still suffers from the problem that sentence increases the performance slumps  
                        2. Then what‘s wrong with RNNs?
                            1. The first flaw of RNN is its sequential nature
                            2. The second is the long-range dependencies
                        3. Note, seq2seq is already the attention model.
                           Transformer features instead in:
                            1. "Self-attention" - capture long range dependencies
                                1. "To handle this flaw, the transformer just allows the encoder and decoder to see the entire input sequence all at once, directly modelling these dependencies using attention."
                                2. "The basic attention mechanism is simply a dot product between the query and the key"
                                3. So .. Transformer instead all tokens all at once, but uses "self-attention" to map to a time step in RNN.
                            2. "Multi-head attention" -
                                1. "the Multi-Head Attention applies different linear transformations to the keys, values and queries for each “head” of attention" 
                            3. "Positional Encodings"
                                1. "The model easily learns to get the relative positions, as each dimension of the positional encoding is a wave with a different frequency."
                            4. "Masked" multi-head attention
                                1. hide the next future word. by transforming them into zeroes
            4. Transformer
                1. "One main difference is that the input sequence can be passed parallelly so that GPU can be used effectively and the speed of training can also be increased"
                   "It is also based on the multi-headed attention layer, so it easily overcomes the vanishing gradient issue"
            5. Google: Transformer: A Novel Neural Network Architecture for Language Understanding
               https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html
                1. a simple animation

2. InstructGPT: Training language models to follow instructions with human feedback    [2022, 388 refs]
   https://arxiv.org/pdf/2203.02155.pdf
    1. The paper of ChatGPT / GPT 3.5. The key is to use a Reward Model to train GPT. RM is first trained from human feedback.
       People train, people rank, than model trains model itself. Huge effort are spent to mitigate harms, toxic generations.
       Models: GPT-3 -> SFT -> RM -> RL. GPT-3 is public, RLHF & PPO are public, what are valuable is ChatGPT's carefully crafted representative training datasets. And RLHF & PPO enables fine-tuning with few manual feedback.
    2. highlights
        1. Problem: Avoid generating toxic results
        2. methods
            1. a dataset of labeler. fine tune GPT-3 with supervised learning. fine-tuning on a small curated dataset of human demonstrations
                1. See Figure 2. Labeler demonstrates the desired output.
                    1. A team of ~40 contractors on Upwork and through ScaleAI
                2. Human works on OpenAPI's API.
            2. RLHF - reinforcement learning from human feedback
                1. See Figure 2. Several model outputs are sampled and Labeler ranks the output from best to worst. It's used to train the reward model.
                   Finally, use this RM as a reward function and fine-tune our GPT-3 policy to maximize this reward using the PPO algorithm
                2. PPO - Proximal Policy Optimization
                3. minimizes this alignment tax
                    1. aligning the models only on customer tasks can make their performance worse on some other academic NLP tasks
                    2. solution: during RL fine-tuning we mix in a small fraction of the original data used to train GPT-3, and train on this data using the normal log likelihood maximization
        3. How ChatGPT handles multi-round conversation?
            1. HUMATA: "One of the key features of ChatGPT is its ability to handle multi-round conversations, which is achieved through the use of a prefix that signals to the model that it is in a conversational context. The prefix used by ChatGPT is "Q: {question}\nA: ", which indicates that the model is being asked a question and should respond accordingly. This prefix is used consistently throughout the conversation, allowing the model to maintain context and understand the flow of the conversation. In addition to the prefix, ChatGPT also uses a memory mechanism that allows it to store information from previous turns in the conversation. This memory is used to inform the model's responses and ensure that it maintains coherence and consistency throughout the conversation. The ability of ChatGPT to handle multi-round conversations is important because it allows the model to engage in more natural and human-like interactions with users. This is particularly useful in applications such as chatbots and virtual assistants, where users may have complex or multi-part requests that require multiple rounds of interaction. By using a conversational prefix and memory mechanism, ChatGPT is able to handle these interactions in a more natural and effective way."
        4. others
            1. "InstructGPT models show promising generalization to instructions outside of the RLHF fine-tuning distribution", while GPT-3 doesn't
            2. Table 1 shows usecase categorizes for prompt datasets: 
                Generation 45.6%
                Open QA 12.4%
                Brainstorming 11.2%
                Chat 8.4%
                Rewrite 6.6%
                Summarization 4.2%
                Classification 3.5%
                Other 3.5%
                Closed QA 2.6%
                Extract 1.9%
            3. Our dataset is 96% English
            4. Watch the APPENDIX
                1. OpenAI is really carefully crafting well-represented datasets
            5. we find that inter-annotator agreement rates are quite high: training labelers agree with each-other 72.6 ± 1.5% of the time, while for held-out labelers this number is 77.3 ± 1.3%. For comparison, in the summarization work of Stiennon et al. (2020) researcher-researcher agreement was 73 ± 4%
            6. We believe our InstructGPT model outperforms FLAN and T0 for two reasons
            7. training our 175B SFT model requires 4.9 petaflops/s-days and training our 175B PPO-ptx model requires 60 petaflops/s-days, compared to 3,640 petaflops/s-days for GPT-3
                1. At the same time, our results show that RLHF is very effective at making language models more helpful to users, more so than a 100x model size increase.
                2. This suggests that right now increasing investments in alignment of existing language models is more cost-effective than training larger models—at least for our customers’ natural language task distribution
                3. To this end, our results are good news for RLHF as a low-tax alignment technique
                4. Nvidia A100 is capable of  5 petaflops.
                   https://venturebeat.com/ai/nvidia-unveils-monstrous-a100-ai-chip-with-54-billion-transistors-and-5-petaflops-of-performance/
            8. We’ve seen some evidence that InstructGPT generalizes ‘following instructions’ to settings that we don’t supervise it in, for example on non-English language tasks and code-related tasks.
            9. For instance, most comparisons are only labeled by 1 contractor for cost reasons.
            10. While we mainly focus on RLHF, there are many other algorithms that could be used to train policies on our demonstration and comparison data to get even better results. For example, one could explore expert iteration (Anthony et al., 2017; Silver et al., 2017), or simpler behavior cloning methods that use a subset of the comparison data. One could also try constrained optimization approaches (Achiam et al., 2017) that maximize the score from a reward model conditioned on generating a small number of harmful behaviors
    n. related materials
        1. OpenAI's paper article: Aligning language models to follow instructions
           https://openai.com/research/instruction-following
            1. Article for the InstructGPT paper
        2. Improving language model behavior by training on a curated dataset
           https://openai.com/research/improving-language-model-behavior
           Process for Adapting Language Models to Society (PALMS) with Values-Targeted Datasets    [2021, 58 refs]
           https://cdn.openai.com/palms.pdf
            1. We’ve found we can improve language model behavior with respect to specific behavioral values by fine-tuning on a curated dataset of <100 examples of those values
            2. We also found that this process becomes more effective as models get larger
                1. See Figure 2 in paper ""
            3. OK .. this sound the key technology behind ChatGPT
            4. Steps
                1. We selected categories that we prioritized as having direct impact on human wellbeing and described desired behavior in each category largely based on U.S. and international human rights law and Western social movements for human equality
                2. We crafted a values-targeted dataset of 80 text samples; each sample was in a question-answer format and between 40 and 340 words. (For a sense of scale, our dataset was about 120KB, about 0.000000211% of GPT-3 training data.
                3. We used quantitative and qualitative metrics: human evaluations to rate adherence to predetermined values; toxicity scoring
        3. Proximal Policy Optimization
           https://openai.com/research/openai-baselines-ppo
           Proximal Policy Optimization Algorithms    [2017, 10960 refs]
           https://arxiv.org/abs/1707.06347#
            1. Prior works - TRPO and ACER
            2. From ChatGPT: https://chat.openai.com/chat/3753b4da-4f94-4f0a-82f0-e9d1641b857d
                1. Trust Region Policy Optimization (TRPO):
                    TRPO is a policy optimization algorithm that enforces a trust region constraint on the policy updates, ensuring that the updated policy does not deviate too far from the old policy. This is achieved using the KL divergence between the new and old policies as a constraint in the optimization problem. TRPO employs a natural policy gradient method with conjugate gradient descent and line search to solve the constrained optimization problem. This approach leads to more stable updates compared to vanilla policy gradient methods. However, TRPO can be computationally expensive and complex to implement.
                2. Proximal Policy Optimization (PPO):
                    PPO is a simplification of TRPO that aims to provide similar performance with less computational complexity. Instead of using a hard constraint on the KL divergence like TRPO, PPO uses a surrogate objective function with a soft constraint enforced by a clipping mechanism. This clipping mechanism prevents the updated policy from deviating too far from the old policy. PPO is easier to implement and generally more sample-efficient than TRPO, while still offering stable policy updates. PPO has become popular due to its simplicity, performance, and ease of use with various deep reinforcement learning problems.
        4. Learning from human preferences
           https://openai.com/research/learning-from-human-preferences
           Deep reinforcement learning from human preferences    [2017, 856 refs]
           https://arxiv.org/abs/1706.03741
            1. backflip video: 70hrs self-learning + 1000 bits of human feedback
            2. human feedback to reward predictor
            3. Ablation Studies - Figure 6: Performance of our algorithm on Atari tasks after removing various components
            n. related materials
                1. Illustrating Reinforcement Learning from Human Feedback (RLHF)
                   https://huggingface.co/blog/rlhf
                    1. "Next, with a language model, one needs to generate data to train a reward model, which is how human preferences are integrated into the system."
        5. Train ChatGPT on your own knowledge base
           https://beebom.com/how-train-ai-chatbot-custom-knowledge-base-chatgpt-api/
            1. Interesting. The OpenAPI python lib allows you to train the model again on your data
            2. The article is using langchain python lib.
                1. But is the underlying ChatGPT API should be the fine-tune API?
                   https://platform.openai.com/docs/guides/fine-tuning
        6. ChatGPT explained: A Guide to Conversational AI w/ InstructGPT, PPO, Markov, RLHF
           https://www.youtube.com/watch?v=GMkszGzFOgw
        7. Everything I understand about chatgpt - veekaybee/chatgpt.md
           https://gist.github.com/veekaybee/6f8885e9906aa9c5408ebe5c7e870698
            1. useful

4. GPT3 - Language Models are Few-Shot Learners    [2020, 8778 refs]
   https://arxiv.org/abs/2005.14165
    1. LLM. 175B parameters, unsupervised learning on internet (by predict next word). Transformer. Then achieved few-shot learning.
    2. highlights
        1. from ChatGPT to show what is GPT-3 and how GPT-1,2,3 compare: https://chat.openai.com/chat/3753b4da-4f94-4f0a-82f0-e9d1641b857d
            1. "GPT-3, or Generative Pre-trained Transformer 3, is a state-of-the-art language model developed by OpenAI. It's based on the Transformer architecture, a neural network architecture designed specifically for natural language processing tasks. GPT-3 has 175 billion parameters, making it one of the largest and most powerful language models at the time of its release in June 2020.

            Here's an overview of how GPT-3 works:

            Pre-training: GPT-3 is pre-trained on a large corpus of text from the internet, including books, articles, and websites. During this unsupervised learning phase, the model learns to generate text by predicting the next word in a sentence, given the previous words. It learns grammar, facts, reasoning abilities, and even some biases present in the training data.

            Fine-tuning: After the pre-training phase, GPT-3 is fine-tuned on specific tasks using smaller, supervised datasets. This allows the model to adapt its knowledge to specific domains and improve its performance on tasks such as question-answering, text summarization, translation, and more.

            Transformer architecture: GPT-3 uses the Transformer architecture, which relies on self-attention mechanisms to process input sequences. These mechanisms allow the model to capture long-range dependencies and context effectively. The architecture is composed of layers of multi-head self-attention and feedforward neural networks, organized into an encoder (for processing input) and a decoder (for generating output).

            Tokenization: Text input is tokenized into smaller units called tokens (words or subwords) and then converted into numerical vectors that can be processed by the neural network.

            Context windows: GPT-3 processes text in chunks called context windows, which have a limited number of tokens. The model reads and generates text within these windows, with its understanding of the text constrained by the window size.

            Autoregressive generation: GPT-3 generates text in an autoregressive manner, meaning it predicts one token at a time, conditioning each prediction on the previously generated tokens. This process continues until the desired text length is reached or a stop token is encountered.

            GPT-3 has demonstrated remarkable performance on various natural language processing tasks, showcasing its ability to generate coherent, contextually relevant, and often creative text. However, it can be sensitive to the input phrasing, and its performance can be inconsistent at times, producing plausible-sounding but incorrect or nonsensical answers."

                1. How does the model knows when to stop generation?
                    1. HUMATA: "the GPT-3 language model uses a special token, called the end-of-sequence (EOS) token, to indicate when the generation should stop. The model is trained to predict the EOS token after generating the final word in a sequence. When generating text, the model continues generating words until it predicts the EOS token or reaches a maximum length limit. The maximum length limit is typically set by the user or the application and is used to prevent the model from generating excessively long or nonsensical sequences."

            2. "GPT-1, GPT-2, and GPT-3 are all part of the Generative Pre-trained Transformer (GPT) series of language models developed by OpenAI. Each successive version is an improvement on the previous one in terms of model size, training data, and overall performance. Here's a comparison of the three models:

            GPT-1:

            Released in 2018, GPT-1 was the first model in the GPT series.
            It introduced the unsupervised pre-training followed by task-specific fine-tuning approach.
            GPT-1 used the Transformer architecture, which relies on self-attention mechanisms.
            The model contained 117 million parameters.

            GPT-2:
            
            Released in 2019, GPT-2 was a significant improvement over GPT-1.
            It increased the model size to 1.5 billion parameters, substantially improving its language understanding and generation capabilities.
            GPT-2 was pre-trained on a larger dataset called WebText, containing 45 million web pages.
            The model demonstrated strong zero-shot learning abilities, meaning it could perform well on tasks without any specific fine-tuning.
            GPT-2 gained attention for its ability to generate coherent, contextually relevant text but also raised concerns about its potential misuse in generating misleading or harmful content.
            
            GPT-3:
            
            Released in 2020, GPT-3 is a significant leap from GPT-2 in terms of model size and capabilities.
            It contains 175 billion parameters, making it one of the largest language models at the time of its release.
            GPT-3 was trained on an even larger dataset, which helped improve its performance on a wide range of tasks.
            It showed remarkable performance in few-shot learning, meaning it could generalize and perform well on tasks with just a few examples provided during inference.
            Despite its impressive capabilities, GPT-3 still has limitations, such as sensitivity to input phrasing and occasional generation of plausible-sounding but incorrect or nonsensical answers.
            In summary, GPT-1 laid the foundation for the GPT series with the introduction of the pre-training and fine-tuning approach using the Transformer architecture. GPT-2 improved upon GPT-1 by increasing the model size and training on a larger dataset, demonstrating strong zero-shot learning abilities. GPT-3 further expanded the model size and training data, showcasing impressive few-shot learning performance and setting a new benchmark in natural language understanding and generation."

        2. From HUMATA: What are zero-shot, one-shot, and few-shot learning
            1. HUMATA: "In the context of the paper "Language Models are Few-Shot Learners," zero-shot, one-shot, and few-shot refer to different settings for evaluating the performance of a language model on a given task. Zero-shot learning refers to the setting where the model is given a natural language instruction describing the task, but no demonstrations or examples are allowed. One-shot learning is similar to zero-shot learning, but only one demonstration is allowed in addition to the natural language description of the task. Few-shot learning is the term used in the paper to refer to the setting where the model is given a few demonstrations of the task at inference time as conditioning, but no weight updates are allowed. Few-shot learning works by giving K examples of context and completion, and then one final example of context, with the model expected to provide the completion. The authors typically present the model with a few dozen examples in the few-shot setting."

            2. Figure 1.2: Larger models make increasingly efficient use of in-context information. 175B Parms achieve one-shot.
            3. Few-shot (FS) - However, the difference here is that unlike a normal ML algorithm, the model does not do any weight updates
                1. My question: Is this potentially be able to build the multi-round conversation?
                2. Note, Fine-Tuning involves updating weights of the model, while Few-shot not.
                3. "The main disadvantage is that results from this method have so far been much worse than state-of-the-art fine-tuned models."
        
        3. What dataset is GPT-3 trained on?
            1. HUMATA: "GPT-3 language model is trained on a mixture of datasets, including a filtered version of the Common Crawl dataset, curated high-quality datasets such as WebText, Books1, and Books2, and English-language Wikipedia. The Common Crawl dataset is a large collection of web pages, while the curated datasets are designed to increase the diversity and quality of the training data. The authors also note that the Common Crawl dataset was filtered based on similarity to a range of high-quality reference corpora, and fuzzy deduplication was performed at the document level to prevent redundancy and preserve the integrity of the held-out validation set. The final mixture of datasets used in training is shown in Table 2.2 of the paper."

        4. From the evaluation part, OpenAI is really doing extensive evaluating
            1. 3.1 Language Modeling, Cloze, and Completion Tasks
                    3.1.2 LAMBADA
                    3.1.3 HellaSwag
                    3.1.4 StoryCloze
                3.2 Closed Book Question Answering
                3.3 Translation
                3.4 Winograd-Style Tasks
                3.5 Common Sense Reasoning
                3.6 Reading Comprehension
                3.7 SuperGLUE
                3.8 NLI
                3.9 Synthetic and Qualitative Tasks
                    3.9.1 Arithmetic
                    3.9.2 Word Scrambling and Manipulation Tasks
                    3.9.3 SAT Analogies
                    3.9.4 News Article Generation
                    3.9.5 Learning and Using Novel Words
                    3.9.6 Correcting English Grammar

        5. Measuring and Preventing Memorization Of Benchmarks
            1. Appendix C: Use number of words N to detect overlap
            2. Prevent the predict content to have already been seen by the model in training dataset, i.e. leaked, contaminated

        6. All models were trained on V100 GPU’s on part of a high-bandwidth cluster provided by Microsoft

        7. ChatGPT answer: How to understand emergence in GPT-3, InstructGPT, and ChatGPT?
           https://chat.openai.com/chat/3753b4da-4f94-4f0a-82f0-e9d1641b857d
            1. "Emergence in the context of GPT-3, InstructGPT, and ChatGPT refers to the appearance of complex or unexpected behaviors, capabilities, or properties in these models due to their large-scale architecture and pretraining methods. These emergent properties may not have been explicitly trained for but arise as a result of the models' ability to capture and generalize patterns and relationships from their extensive training data.

            Here's how emergence can be understood in each of these models:

            1. GPT-3: GPT-3's emergence comes from its ability to perform various tasks in a few-shot learning setting. GPT-3 can understand and generate human-like responses to a wide range of prompts without the need for task-specific training or fine-tuning. This ability emerges due to the model's massive scale (175 billion parameters) and its unsupervised pretraining on a large corpus of text, which helps it learn language structure, grammar, facts, and reasoning abilities.

            2. InstructGPT: InstructGPT is designed to follow instructions in natural language prompts and generate helpful responses. The model exhibits emergent behavior by understanding and answering complex questions or completing tasks it hasn't explicitly been trained for. InstructGPT's capabilities emerge from its training process, which combines Reinforcement Learning from Human Feedback (RLHF) with unsupervised pretraining. The model learns from human demonstrations and feedback, which helps it generalize and perform a variety of tasks.

            3. ChatGPT: ChatGPT is designed to engage in interactive conversations and provide informative responses. Emergence in ChatGPT can be observed through its ability to generate coherent and contextually relevant responses in a conversation, despite not being explicitly trained for every possible conversation scenario. Like GPT-3 and InstructGPT, ChatGPT's capabilities emerge from its large-scale architecture and unsupervised pretraining, which enable it to understand and generate human-like text.

            In summary, emergence in GPT-3, InstructGPT, and ChatGPT refers to the models' ability to display complex behaviors, understand various tasks, and generate human-like responses despite not being explicitly trained for those specific tasks. These emergent properties arise from the combination of their large-scale architecture, unsupervised pretraining, and other training techniques such as reinforcement learning from human feedback."

        8. Use Reddit votes to data cleaning Common Crawl, etc

    n. related materials
        1. Sciforce: What is GPT-3, How Does It Work, and What Does It Actually Do?
           https://medium.com/sciforce/what-is-gpt-3-how-does-it-work-and-what-does-it-actually-do-9f721d69e5c1
            1. "Pre-trained means that the language model has not been built with any special domain knowledge, but it can complete domain-specific tasks like translation"
        
        2. OpenAI GPT-3: Everything You Need to Know
           https://www.springboard.com/blog/data-science/machine-learning-gpt-3-open-ai/
           1. "A major issue in training models and in particular such large training models with so much data from the internet is that these models have the capacity to memorise the content and then contaminate downstream tasks like testing as they might have already seen the data. Though the creators of GPT-3 took some measures to avoid the training and test data overlaps but a bug in the filtering caused some of the data to leak. As mentioned in the paper, the team could not retrain the model due to the high cost associated with the training."
           2. To summarise:
                * GPT-3 is a very large language model (the largest till date) with about 175B parameters.
                * It is trained on about 45TB of text data from different datasets.
                * As such the model itself has no knowledge, it is just good at predicting the next word(s) in the sequence. It is not designed to store or retrieve facts.
                * It produces more fluent and human-like text outputs.
                * You don’t need task-specific datasets to accomplish a task using GPT-3. It is “Task-Agnostic”.
                * You cannot download or retrain the model. You need an API key (can get by joining the waitlist). It has “closed-API” access.
                * It is good mostly for English language tasks.
                * Longer outputs from the model tend to degrade.
                * The outputs can be biased and abusive.
                * There are known contaminations in the benchmark experiments which have been called out clearly in paper.

        3. How GPT3 Works - Easily Explained with Animations
           https://www.youtube.com/watch?v=MQnJZuBGmSQ

        4. All things: GPT-3 An Overview
           https://dzlab.github.io/ml/2020/07/25/gpt3-overview/
            1. See the model structure of GPT-3
               GPT-3 has the same attention-based architecture as GPT-2
               The main difference between the two models are the number of layers -layers 96 

            2. What are the "layers" in Transformer network?
               http://jalammar.github.io/illustrated-transformer/
                1. From Transformer paper: "The encoder is composed of a stack of N = 6 identical layers"
                2. HUMATA: "In the context of the Transformer model, layers refer to the repeated application of a set of operations that transform the input sequence into a higher-level representation. The Transformer model consists of multiple layers of encoders and decoders, each of which contains multiple sub-layers. The need for layers arises from the fact that natural language processing tasks often involve complex relationships between different parts of the input sequence. By applying multiple layers of transformations, the model can gradually learn to capture these relationships and build a more abstract representation of the input. Each layer can be thought of as a way to refine the representation learned in the previous layer, allowing the model to capture increasingly complex patterns in the data. In the Transformer model, the encoder layers apply a self-attention mechanism to capture dependencies between different parts of the input sequence, followed by a position-wise feed-forward network to further refine the representation. The decoder layers use a similar architecture, but also incorporate an attention mechanism over the encoder outputs to allow the decoder to attend to relevant parts of the input during generation. By stacking multiple layers of these operations, the Transformer model is able to learn complex relationships between different parts of the input sequence and generate high-quality outputs."
                3. useful article with chart illustration. the article also has nice useful explanations to Transformer and Attention.
                    1. So Encoders are stacked, this is called multiple layers. See http://jalammar.github.io/illustrated-transformer/ the second chart.
                       Multi-head attention is also having multiple instances, also called layers (Transformer paper Figure 2). so confusing 


5. GPT-1: Improving Language Understanding by Generative Pre-Training    [2018, 5117 refs]
   https://openai.com/research/language-unsupervised
   https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf
    1. unsupervised learning on large dataset, then fine-tuning supervised using a small dataset.
       GPT only uses the decoder part of the Transformer model. Prior work - Transformer.
       So the idea to train ChatGPT with unsupervised learning + supervised fine-tune is already embedded in GPT-1 paper
    2. highlights
        1. From ChatGPT - What are the key points in GPT-1 paper? - https://chat.openai.com/chat/3753b4da-4f94-4f0a-82f0-e9d1641b857d
            1. "introduces the key concepts and methods for the GPT model. Some of the main points in the paper are:

                Unsupervised pre-training: The paper proposes a two-step process for training the GPT model. The first step is unsupervised pre-training, where the model learns from a large corpus of text without any labeled data. This pre-training helps the model learn the structure of the language, grammar, and semantics.

                Supervised fine-tuning: After the unsupervised pre-training, the model is fine-tuned using supervised learning on a smaller dataset with labeled examples. This fine-tuning helps the model specialize in specific tasks and achieve better performance.

                Transformer architecture: GPT-1 is based on the Transformer architecture introduced by Vaswani et al. in the paper "Attention is All You Need." GPT-1 specifically uses the decoder part of the Transformer model, which consists of a stack of masked multi-head self-attention and feed-forward layers.

                Unidirectional context: Unlike the original Transformer model, which processes input tokens bidirectionally, GPT-1 processes input tokens unidirectionally from left to right. This unidirectional context is suitable for generative tasks where the model needs to predict the next token in the sequence.

                Transfer learning: The paper demonstrates the effectiveness of the GPT model in transfer learning, where the knowledge gained during pre-training is applied to various natural language processing tasks. GPT-1 shows competitive results on multiple tasks, such as document classification, question-answering, and language modeling, with minimal task-specific fine-tuning.

                The GPT-1 paper presents the foundational ideas and methods for the GPT series of models. These concepts and techniques were further developed and refined in subsequent models like GPT-2 and GPT-3."

        2. From ChatGPT- How does GPT-1 differ from Transformer?
            1. "Here are some key differences between GPT-1 and the original Transformer:

                1. Model architecture: The original Transformer consists of two main components: an encoder and a decoder. In contrast, GPT-1 is based on the decoder part of the Transformer architecture only. The decoder in GPT-1 consists of a stack of masked multi-head self-attention and feed-forward layers.

                2. Unidirectional context: The original Transformer model processes input tokens bidirectionally, meaning it considers both past and future tokens in the input sequence. On the other hand, GPT-1 processes input tokens unidirectionally from left to right, making it more suitable for generative tasks where the model needs to predict the next token in a sequence.

                3. Pretraining and fine-tuning: GPT-1 introduces a two-step training process consisting of unsupervised pretraining on a large corpus of text, followed by supervised fine-tuning on task-specific datasets. This approach allows GPT-1 to learn language structure, grammar, and semantics during pretraining and then specialize in specific tasks during fine-tuning. In comparison, the original Transformer model is usually trained using supervised learning on specific tasks like machine translation.

                4. Transfer learning: GPT-1 is designed for transfer learning across multiple natural language processing tasks. It demonstrates competitive results on various tasks, such as document classification, question-answering, and language modeling, with minimal task-specific fine-tuning. The original Transformer models are typically more specialized for tasks like machine translation and may require task-specific fine-tuning to achieve high performance on other tasks.

                In summary, while GPT-1 is based on the Transformer architecture, it differs in terms of its decoder-only structure, unidirectional context, pretraining and fine-tuning methods, and focus on transfer learning across multiple natural language processing tasks."

        3. "In our experiments, we use a multi-layer Transformer decoder [34] for the language model, which is a variant of the transformer [62]." - So GPT-1 is decoder only of the Transformer
            1. See Figure 1, the layer is 12x. Compared to GPT-3 96x
            2. "Our model largely follows the original transformer work [62]. We trained a 12-layer decoder-only transformer with masked self-attention heads (768 dimensional states and 12 attention heads)."
            3. StackExchange: Why does GPT-2 Exclude the Transformer Encoder?
               https://ai.stackexchange.com/questions/27038/why-does-gpt-2-exclude-the-transformer-encoder
                1. "GPT-2 does not require the encoder part of the original transformer architecture as it is decoder-only, and there are no encoder attention blocks, so the decoder is equivalent to the encoder, except for the MASKING in the multi-head attention block, the decoder is only allowed to glean information from the prior words in the sentence. It works just like a traditional language model as it takes word vectors as input and produces estimates for the probability of the next word as outputs but it is auto-regressive as each token in the sentence has the context of the previous words. Thus GPT-2 works one token at a time."
                
                2. HUMATA: "GPT-1 is only based on the decoder part of the Transformer because it is designed for language modeling, which is an autoregressive task where the model predicts the next word in a sequence given the previous words. The decoder part of the Transformer is responsible for generating the output sequence by attending to the input sequence and generating one token at a time. The encoder part of the Transformer is responsible for encoding the input sequence into a fixed-length representation, which is not necessary for language modeling. Therefore, GPT-1 only uses the decoder part of the Transformer, which is more suitable for autoregressive tasks like language modeling."
                
                3. What is the difference between Transformer encoder vs Transformer decoder vs Transformer encoder-decoder?
                   "I know that GPT uses Transformer decoder, BERT uses Transformer encoder, and T5 uses Transformer encoder-decoder. But can someone help me understand why GPT only uses the decoder, BERT only uses encoder, and T5 uses both?"
                    1. "Encoders are bidirectional while Decoders are Unidirectional. Encoders will look in both directions while encoding the data while the decoders will look either into the initial tokens or the tokens after it while vectorizing/predicting the current token"
                    2. "The GPT2 model discards the encoder part, so there is only one single input sentence rather than two separate source and target sequences. GPT is an autoregressive inference model.
                        Apart from that, at inference time BERT generates all its output at once, while GPT is autoregressive, so it need to iteratively generate one token at a time."

                4. DataScience: Why is the decoder not a part of BERT architecture?
                   https://datascience.stackexchange.com/questions/65241/why-is-the-decoder-not-a-part-of-bert-architecture
                    1. "In causal (traditional) language models (LMs), each token is predicted conditioning on the previous tokens. Given that the previous tokens are received by the decoder itself, you don't need an encoder."

                5. [34] Generating wikipedia by summarizing long sequences    [2018, 675 refs]
                   https://arxiv.org/abs/1801.10198
                    1. "For the abstractive model, we introduce a decoder-only architecture that can scalably attend to very long sequences, much longer than typical encoderdecoder architectures used in sequence transduction"

6. GPT-2: Language models are unsupervised multitask learners    [2019, 5573 refs]
   https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf
    1. GPT-3 reuses GPT-2's model, but add more layers (and larger). Compared to GPT-1, the key diff of GPT-2 is being larger
    2. highlights
        1. From ChatGPT - comparing GPT-2 vs GPT-1 - https://chat.openai.com/chat/3753b4da-4f94-4f0a-82f0-e9d1641b857d
            1. "The key differences between GPT-2 and GPT-1 can be summarized in terms of model size, architecture refinements, dataset, and performance. While both GPT-1 and GPT-2 are based on the Transformer architecture and share similar training methods (unsupervised pretraining followed by supervised fine-tuning), there are notable improvements in GPT-2:

                1. Model size: GPT-2 is significantly larger than GPT-1 in terms of the number of parameters. GPT-1 has 117 million parameters, while GPT-2 comes in several sizes, with the largest having 1.5 billion parameters. This increase in model size allows GPT-2 to capture more complex patterns and relationships in language, leading to better performance across a range of tasks.

                2. Architecture refinements: GPT-2 introduces several refinements to the model architecture. For example, GPT-2 uses modified initialization, weight scaling, and positional encoding schemes, which help stabilize training and improve performance.

                3. Dataset: GPT-2 is pretrained on a larger and more diverse dataset called WebText, which is a subset of the Common Crawl dataset. This dataset consists of around 45 million web pages, offering GPT-2 a more extensive and varied training corpus compared to GPT-1's BooksCorpus dataset. A larger dataset allows GPT-2 to learn a broader range of language patterns and facts, contributing to its improved performance.

                4. Performance: GPT-2 demonstrates significantly better performance across various natural language processing tasks compared to GPT-1. Due to its larger size, architecture refinements, and more extensive dataset, GPT-2 is capable of generating more coherent and contextually relevant text, with improved abilities in zero-shot and few-shot learning settings.

                In summary, the key differences between GPT-2 and GPT-1 include a substantial increase in model size, architectural refinements, a larger and more diverse training dataset, and overall improved performance across a range of natural language processing tasks."
        2. Multitask
            1. 
    n. related materials
        1. Day 1: Language Models are Unsupervised Multitask Learners
           https://medium.com/a-paper-a-day-will-have-you-screaming-hurray/day-1-language-models-are-unsupervised-multitask-learners-fdb7016d8aad
            1. "GPT2 is a basically a much larger version of GPT which achieved a step-wise increase in performance in zero-shot language modelling and promising results in zero-shot downstream tasks."
            2. OpenAI GPT 2 has some minor changes on the architecture compared with OpenAI GPT:
                1. Layer normalization was moved to the input of each sub-block (it used to be at the output of the sub-block) and an additional layer normalization was added after the final self-attention block.
                2. A modified initialization which accounts for the accumulation on the residual path with model depth is used.
                3. They scaled the weights of residual layers at initialization by a factor of1/√N where N is the number of residual layers.
                4. Vocabulary was expanded to 50,257.
                5. Context size was increased from 512 to 1024 tokens and a larger batchsize of 512 was used.

        2. Sebastian Raschka: L19.5.2.4 GPT-v2: Language Models are Unsupervised Multitask Learners
           https://www.youtube.com/watch?v=BXv1m9Asl7I

        3. Mu Li: GPT，GPT-2，GPT-3 论文精读【论文精读】
           https://www.youtube.com/watch?v=t70Bl3w7bxY
            1. Good. lengthy in-dpeth walkthrough in the paper text. I didn't find another blog/video that is comparable.

7. GPT-4 Technical Report
   https://openai.com/research/gpt-4
   https://arxiv.org/abs/2303.08774
   https://cdn.openai.com/papers/gpt-4-system-card.pdf
    1. multimodal (accepting image and text inputs, emitting text outputs). OpenAI became ClosedAI. GPT-4 can pass exams with well score.
       Compared to GPT-3, GPT-4's advancement is a big leap. very extensive study and work to enhance the safety and unbiased of the generated output
    2. highlights
        1. "Over the past two years, we rebuilt our entire deep learning stack and, together with Azure, co-designed a supercomputer from the ground up for our workload"
        2. "We proceeded by using the most recent publicly-available tests (in the case of the Olympiads and AP free response questions) or by purchasing 2022–2023 editions of practice exams. We did no specific training for these exams."
        3. "We also are using it to assist humans in evaluating AI outputs, starting the second phase in our alignment strategy."
        4. OpenAI Evals is a framework for evaluating OpenAI models and an open-source registry of benchmarks.
           https://github.com/openai/evals
        5. "GPT-4 is a Transformer-style model [39] pre-trained to predict the next token in a document, using both publicly available data (such as internet data) and data licensed from third-party providers. The model was then fine-tuned using Reinforcement Learning from Human Feedback (RLHF) [40]."
        6. "Finally, we demonstrate that while our mitigations and processes alter GPT-4’s behavior and prevent certain kinds of misuses, they are limited and remain brittle in some cases."
            1. "we engaged more than 50 experts to help us gain a more robust understanding of the GPT-4 model and potential deployment risks"
            2. Some of the specific risks we explored are:6
                • Hallucinations
                • Harmful content
                • Harms of representation, allocation, and quality of service
                • Disinformation and influence operations
                • Proliferation of conventional and unconventional weapons
                • Privacy
                • Cybersecurity
                • Potential for risky emergent behaviors
                • Interactions with other systems
                • Economic impacts
                • Acceleration
                • Overreliance
        
        7. A key tech - reliable scaling / Predictable scaling: reliably predict the training results on the large model
            1. usually this to verify parameter tuning on a small model first, and then apply to the large model. because re-train large model is too expensive
               but the problem is that smaller model results usually do not apply to large model, especially due to the emergence. wonder how OpenAI did that.
            2. this tech is especially important to make the model work evolve with high pace.
            3. see Figure 1 - OpenAI codebase next word prediction. Reliably predict the expected loss when full computation power is employed.

        8. Inverse Scaling Prize - anti-examples that a larger model will perform worse

        9. Is RLHF a kind of fine-tuning? Need to update model weights?
            1. YES - See the InstructGPT paper: "by incorporating pretraining data into RLHF fine-tuning"
            2. HUMATA: (I also asked a few follow up questions)
            "
            RLHF (Reward Learning from Human Feedback) is a kind of fine-tuning. It involves fine-tuning a pre-trained language model using human feedback as a reward signal to align the model's behavior with human intentions. However, RLHF fine-tuning is different from traditional fine-tuning in that it uses a reward signal instead of a loss function to update the model's parameters. This allows RLHF to learn from sparse and noisy feedback, making it more suitable for aligning language models with human intentions.

            RLHF (Reward Learning from Human Feedback) involves updating the model weights, not gradients. The reward signal is used to update the weights of the pre-trained language model, which is fine-tuned to align its behavior with human intentions. The reward signal is computed based on the human feedback, and the model's parameters are updated using an optimization algorithm such as Adam. The gradients are computed during the optimization process, but they are not used directly to update the model's parameters in RLHF. Instead, the reward signal is used to guide the optimization process and update the model's weights.

            Model weights and gradients are related but different concepts in machine learning. Model weights are the parameters of the model that are learned during training to make predictions on new data. Gradients, on the other hand, are the derivatives of the loss function with respect to the model weights. They indicate the direction and magnitude of the change needed to the model weights to improve the model's performance. Updating model weights involves changing the values of the model parameters based on the gradients computed during training. This is done using an optimization algorithm such as stochastic gradient descent (SGD) or Adam. The gradients are used to update the model weights in the direction that minimizes the loss function. Updating gradients, on the other hand, is not a common practice in machine learning. Gradients are computed during training and used to update the model weights, but they are not updated themselves. Instead, the optimization algorithm updates the model weights based on the gradients computed at each iteration of training. In summary, updating model weights involves changing the values of the model parameters to improve the model's performance, while updating gradients is not a common practice in machine learning.

            Fine-tuning and few-shot learning are related but different concepts in machine learning. Fine-tuning involves taking a pre-trained model and updating its parameters on a new task or dataset. The pre-trained model is typically trained on a large dataset and has learned general features that can be useful for a wide range of tasks. Fine-tuning allows the model to adapt to a specific task or dataset by updating its parameters based on the new data. Few-shot learning, on the other hand, involves learning from a small number of examples. The goal of few-shot learning is to learn a new task or concept with only a few examples, which is particularly useful in situations where collecting large amounts of labeled data is difficult or expensive. Few-shot learning algorithms typically use meta-learning or other techniques to learn how to learn from a small number of examples. In summary, fine-tuning involves updating a pre-trained model on a new task or dataset, while few-shot learning involves learning from a small number of examples. Fine-tuning can be used for few-shot learning, but few-shot learning is not limited to fine-tuning.

            Meta-learning, also known as "learning to learn," is a subfield of machine learning that focuses on developing algorithms that can learn how to learn. The goal of meta-learning is to enable models to learn new tasks quickly and efficiently with minimal training data. In meta-learning, a model is trained on a set of tasks, and the goal is to learn a general strategy or algorithm that can be applied to new tasks. This is achieved by optimizing the model's parameters to minimize the loss on a set of training tasks, while also optimizing the model's ability to learn new tasks quickly. Meta-learning has applications in a wide range of fields, including computer vision, natural language processing, and robotics. It has been used to develop algorithms for few-shot learning, where a model is trained to learn new concepts or tasks with only a few examples, as well as for reinforcement learning, where a model learns to make decisions based on feedback from its environment
            "

    n. related materials
        1. OpenAI Codex: Evaluating Large Language Models Trained on Code    [2021, 465 refs]
           https://openai.com/blog/openai-codex
           https://arxiv.org/abs/2107.03374
            1. Codex powers Github Copilot. Fine-tuned GPT model. HumanEval framework, solve 28.7%， while GPT-3 solves 0%.
               Repeated sampling is surprisingly effective. 100 samples per problem. We solve 70.2%.
               So, overall, Codex is still GPT but more weights on coding and with fine-tuning.
               Interesting paper. It can be used as an reference example about how to customize GPT for specific purpose use.
            2. highlights
                1. HumanEval. Different from NLP, eval part of generated coding can be done by machine, with unit tests.
                2. Generate 100 answers and use a heuristic ranking score to propose the best as the result. And need to pass unit test
                3. "We fine-tune GPT models containing up to 12B parameters on code to produce Codex"
                4. Data clean the whitespace chars in code, reduce unnecessary token count
                5. Bias the package usage rate. E.g. pytorch vs tensorflow.
            n. related materials
                1. Mu Li: OpenAI Codex 论文精读【论文精读】
                   https://www.youtube.com/watch?v=oZriUGkQSNM

        2. Sparks of Artificial General Intelligence - Early experiments with GPT-4    [2023, 2 refs]
           https://arxiv.org/abs/2303.12712
            1. An extensive evaluation set.
            2. highlights
                1. "我们证明了GPT-4不仅精通语言，而且可以解决涉及数学、编码、视觉、医学、法律、心理学等新颖而困难的任务，而不需要任何特殊提示。此外，在所有这些任务中，GPT-4的表现与人类水平的表现惊人地接近，通常远远超过了ChatGPT等以前的模型"
                2. Chapter 8: GPT-4突出的自回归架构的限制
                    1. "普通人不可能在没有计划其结构的时间内产生如此简洁的句子，并且可能需要“回溯”（进行编辑）几次才能达到最终形式。然而，GPT架构不允许这种回溯"
                    2. 8.2 算术/推理问题中缺乏规划, 8.3 文本生成中缺乏规划
                    3. Chapter 10: 通向更通用人工智能的道路
                        1. 持续学习
                        2. 长期记忆
                        3. 置信度校准
                    4. Appendix A: GPT-4具有常识基础
                        1. an interesting QA example of GPT-4 vs ChatGPT
                3. An extensive evaluation set
                    1. 2 多模态和跨学科的组成
                            2.1 综合能力
                            2.2 视觉
                                2.2.1 超越记忆的图像生成
                                2.2.2 根据详细说明生成图像（如 Dall-E）
                                2.2.3 可能在素描生成中应用
                            2.3 音乐
                        3 编码
                            3.1 从说明到代码
                                3.1.1 编码挑战
                                3.1.2 真实世界的情况
                            3.2 理解现有代码
                        4 数学能力
                            4.1 与 GPT-4 的数学对话
                                4.1.1 对原问题的第一次推广
                                4.1.2 原问题的第二个变体
                                4.1.3 对话中突显的限制分析
                            4.2 数学问题数据集的表现
                            4.3 不同领域的数学建模
                            4.4 高等数学
                        5 与世界的交互
                            5.1 工具使用
                                5.1.1 使用多种工具解决更复杂的任务
                                5.1.2 讨论
                            5.2 体现交互
                                5.2.1 热身：导航地图
                                5.2.2 文本游戏
                                5.2.3 真实世界问题
                                5.2.4 讨论
                        6 与人类的互动
                            6.1 理解人类：心理理论
                                6.1.1 测试心理理论的特定方面
                                6.1.2 在现实情境中测试心理理论
                                6.1.3 讨论
                            6.2 与人类交流：可解释性
                        7 区分能力
                            7.1 PII 检测
                            7.2 误解和事实核查
                                7.2.1 当前指标为何不足？
                                7.2.2 GPT-4 作为裁判
            n. related materials
                1. 《通用人工智能的火花：GPT-4的早期实验》 Sparks of Artificial General Intelligence: Early experiments with GPT-4
                   https://zhuanlan.zhihu.com/p/617566999
                    1. A Chinese translation
                2. 机器之心: 做完GPT-4完整测评，微软爆火论文称初版AGI就快来了
                   https://mp.weixin.qq.com/s/Al9Vojr3Or6s14gbiEq7sA

        3. Mu Li: GPT-4论文精读【论文精读·53】
           https://www.youtube.com/watch?v=K0SZ9mdygTw
           https://www.youtube.com/watch?v=p9IxoSkvZ-M&ab_channel=StanfordMLSysSeminars
            1. good useful for more in-depth understanding to GPT-4.
            2. highlights
                1. Video 35:21 - data contamination problem. GPT-4 uses training data before 2021. CodeForce problems before 2021 are answered correctly, after 2021 are all wrong.
                   Memorizing the solution rather than intelligently derive the solution.
                   But people also argue maybe change the prompt then it'll get the answer.
                2. DAN 2.0 - ChatGPT jailbreak
                    1. similar with "System Message" but used in the opposite way
                    2. "System Message" - define how ChatGPT should role play with
                3. adversary evaluation
                4. Model Calibration becomes worse after RLHF
                5. It's not easy to reduce the GPT-4 to provide harmful output, but with the output it's easier to classify whether it's harmful
                    1. In GPT-4, it's using RLHF to provide reward on harmful output. The reward is provided by a GPT-4 zero-shot classifier judging safety boundaries
                6. Current model is gpt-4-0314, Pricing is $0.03 per 1k prompt tokens and $0.06 per 1k completion tokens. Default rate limits are 40k tokens per minute and 200 requests per minute
                    1. gpt-4 has a context length of 8,192 tokens. We are also providing limited access to our 32,768–context (about 50 pages of text) version, gpt-4-32k

                7. My questions
                    1. If training a GPT-3/4 model is very expensive and it cannot retrain. We know even GPT-4 has the cut off date of 2021. How can OpenAI update the GPT-4 model for newer dates of contents?
                    2. GPT-4 can still answer some newer knowledge after 2021 cut off date. This should be due to some newer data are used for few-shot learning. So, we can probe knowledge after 2021 cut off date to know whether a question answered is due to generalization or due to they were used as training data.
                    3. GPT-3 is trained on Common Crawl, WebText2, Books1, Books2, and Wikipedia. So, it's basically public resources. It's not even touching the highest quality of human output - books. Training on full books look promising
                        1. https://gregoreite.com/drilling-down-details-on-the-ai-training-datasets/#Books1_Books2_15

                    4. AI like ChatGPT has a clear cut-off date at 2021, even GPT-4. Is this a general problem for large scale AI model? Can I say:
                        1) AI large model is generally hard to be good for areas with quickly upating information, and the insights are volatile.
                        2) AI large model can do well in areas that has relative stable insights, e.g. Management skills, stable industries.
                      
                        3) Areas in (1) are usually of high tech, where we believe they deserve high impact by AI, but actually not. The high pace of change becomes of its barrier.
                        4) Career track in areas in (2) generally benefit from growth of age, unlike (1). However, they are more vulnerable to the impact of AI. The barrier is however, hidden info that AI cannot directly access to train.

            n. related materials
                1. Toolformer: Language Models Can Teach Themselves to Use Tools
                2. Introducing LLaMA: A foundational, 65-billion-parameter large language model
                3. Visual ChatGPT: Talking, Drawing and Editing with Visual Foundation Models

                4. OPT-175B: Open Pretrained Transformers - Susan Zhang _ Stanford MLSys #77
                   https://www.bilibili.com/video/BV1XT411v7c9?t=1283.6
                    1. As referenced in parent. 斯坦福MLSYS课程请客座嘉宾 Susan Zhang 讲她们在MetaAI怎么用三个月的时间去做了跟GPT-3同等大小的语言模型 - OPT-175B，虽然模型性能一般，但干货非常多
                       OPT-175B survived 143K steps. Opt-175B在整个一个多月的训练过程中，因为机器崩了、loss跑飞了等原因，一共端~53次，从checkpoint重启训练。图中每个颜色代表重启的一段。
                        1. OK .. a lot of details. quite under water. what problems met in each run.
                    2. 33 days of continuous training. 175B LLM in ~3 months using 1024 80GB A100 GPUs
                    3. Small (125m) model failed to converge with tensor parallel code - bug found

                5. Google's PaLM model: Pathways Language Model (PaLM): Scaling to 540 Billion Parameters for Breakthrough Performance
                   https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html

        4. SIY.Z: ChatGPT在做什么...为什么它能够成功
           https://zhuanlan.zhihu.com/p/607601817?utm_id=0
           https://mp.weixin.qq.com/s/19sTGs_MKCn70CoX2-GKBw
            1. useful informative for beginners

        5. GPT-4的研究路径没有前途？Yann LeCun给自回归判了死刑
           https://mp.weixin.qq.com/s/m943KNGUzFqu62lAlyl5-A
            1. interesting. LeCun 提出了构建「世界」模型的想法, 联合嵌入预测架构（Joint-Embedding Predictive Architecture，JEPA）
            2. I don't think this PPT is to opposite GPT-4 .. title bait. The PPT is about World Model.

        6. 张俊林的答案: OpenAI 发布 GPT-4，有哪些技术上的优化或突破？
           https://www.zhihu.com/question/589639535/answer/2937928726?utm_id=0
            1. 第一，LLM最前沿研究的封闭化或小圈子化
            2. 第二，GPT 4技术报告里提到的LLM模型的“能力预测（Capability Prediction）”是个非常有价值的新研究方向（其实之前也有个别其它资料，我记得看过，但是具体哪篇记不起来了）。用小模型来预测某些参数组合下对应大模型的某种能力，如果预测足够精准，能够极大缩短炼丹周期，同时极大减少试错成本，所以无论理论价值还是实际价值巨大，这个绝对是非常值得认真研究具体技术方法的。
            3. 第三，GPT 4开源了一个LLM评测框架，这也是后面LLM技术快速发展非常重要的方向。尤其对于中文，构建实用的中文LLM评测数据和框架具备特别重要的意义
            4. 首先，斯坦福大学最近在Meta的7B 开源LLaMA基础上，加上Self Instruct技术构造的Alpaca，也代表了一个技术方向。如果归纳下，这个方向可以被称为“低成本复现ChatGPT”的方向

        7. Roger: Transformer模型优化及加速概览
           https://zhuanlan.zhihu.com/p/533797313?utm_id=0
            1. 目前有许多针对 Transformer 的优化，用于处理更长的序列，减少内存占用或加速推理。其中四种常见的方法有：
                1. Segment Level recurrence
                    1. Transformer-XL
                    2. Compressive Transformers

                2. Sparse Attention
                    1. Sparse Transformer
                    2. Longformer
                    3. Adaptive Transformer
                    4. Big Bird
                    5. Reformer
                    6. Routing Transformer
                
                3. Approximation
                    1. Linformer
                    2. Perceiver
                    3. Nyströmformer
                    4. Linear Transformer
                    5. RFA
                    6. Performer

                4. Inference Acceleration
                    1. Turbo Transformer
                    2. Faster Transformer

        8. Llama-X开源！呼吁每一位NLPer参与推动LLaMA成为最先进的LLM
           https://mp.weixin.qq.com/s/HrCg6vfqq7BxBo5ATEcLrA

        9. 【开源GPT】骆驼语言团队进一步开源“驼铃”，单张显卡1小时训练属于你自己的中文语言模型
           https://zhuanlan.zhihu.com/p/616784584?utm_id=0
            1. "自本周三发布Luotuo: Chinese-Alpaca-Lora，基于Meta公司开源的LLaMA模型，英文到中文跨语言训练的项目“骆驼”之后，项目在短短三天收获了超过400个Github的星星，并且还在持续快速上升中。"
            2. "骆驼模型的开发团队团队又进一步在清华唐杰团队开源的GLM-6B中文语言模型上，进行了LoRA的训练。因为GLM-6B本身就是中文语料的模型。骆驼团队尝试将80条左右的关键语料信息，通过LoRA训练的方式，编码到了GLM模型的记忆中。"
            3. 再复述一遍这些模型和项目之间的关系
                LLaMA，Meta（Facebook）开源的大模型，有很多不同的尺寸，13B及以上的模型达到了匹敌和超过GPT3的能力，但是不能chat
                Alpaca，斯坦福小哥使用178个问题生成62k标准数据（通过询问chatGPT），在LLaMA基础上finetune，得到了平替版本的英文ChatGPT
                Alpaca-LoRA，使用LowRank Adaption技术，可以用更少的时间（A100 6.5小时）来训练得到类似Alpaca性能的Chat模型
                山羊，因为使用了LoRA之后，可以用其他语言去训练 LLaMA，来获取跨语言的能力。简单来说，这好像是通过62k条语句，教一个英语的母语的人说一门新的语言，接着他就会说了。山羊是第一个验证LoRA可以实现这一点的。
                骆驼： 骆驼团队开发的开源项目，将山羊改成中文，验证了LoRA也可以使得LLaMA变为一个中文模型。

        10. zhijie的回答: ChatGPT 有什么新奇的使用方式？
            https://www.zhihu.com/question/582979328/answer/2899810576?utm_id=0
            1. 目录
                1. 人类解决问题的过程
                2. 增强GPT-3的实践
                3. 构造Prompt
                    1. 问题的层级结构
                    2. 问题分类器F
                    3. 问题解决器G

                4. 对G的提问
                    1. 生命的意义
                    2. 用GPT-3打造伟大的产品
                    3. 被困在计算机中的G
                    4. 自我改进的G
                    5. 抽象的问题M
                    6. 消消乐
                    7. 前后呼应
```

ChatGPT Prompt Engineering

```
1. Prompt Engineering - A lecture by DAIR.AI
   https://github.com/dair-ai/Prompt-Engineering-Guide
   https://medium.com/dair-ai/prompt-engineering-lecture-71099d8cbb9e
   https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/lecture/Prompt-Engineering-Lecture-Elvis.pdf
    1. A summary
        1. A prompt composes of
            1. Instructions
            2. Context
            3. Input data
            4. Output indicator
        2. To further refine the output (interactively)
            1. Ask to output step-by-step reasoning
            2. Supply apriori knowledge
            3. Give examples

2. 卜寒兮的回答: ChatGPT最实用的提示（Prompts）写法有哪些
   https://www.zhihu.com/question/584402332/answer/2956335225?utm_id=0
    1. good useful. Put the below to ChatGPT first. It's also an example of advanced prompt engineering
        ---
        I want you to become my Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for ChatGPT. The process is as follows: 
        1. You will generate the following sections:

        Prompt:
        {provide the best possible prompt according to my request}

        Critique:
        {provide a concise paragraph on how to improve the prompt. Be very critical in your response}

        Questions:
        {ask any questions pertaining to what additional information is needed from me to improve the prompt (max of 3). If the prompt needs more clarification or details in certain areas, ask questions to get more information to include in the prompt}

        2. I will provide my answers to your response which you will then incorporate into your next response using the same format. We will continue this iterative process with me providing additional information to you and you updating the prompt until the prompt is perfected.
        Remember, the prompt we are creating should be written from the perspective of me making a request to ChatGPT. Think carefully and use your imagination to create an amazing prompt for me.

        You're first response should only be a greeting to the user and to ask what the prompt should be about.
        ---

3. Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing    [2021, 875 refs]
   https://arxiv.org/abs/2107.13586
    1. comprehensive for the area of prompt engineering and much more
    2. highlights
        1. Design Considerations for Prompting
            1. Pre-trained Model Choice
            2. Prompt Engineering
            3. Answer Engineering
            4. Expanding the Paradigm
            5. Prompt-based Training Strategies
        2. Figure 1: Typology of prompting methods
            1. GPT-1,2,3 are one branch in the tree. nice useful chart

    n. related materials
        1. 迷途小书僮: [综述]鹏飞大神的Pre-train, Prompt, and Predict [1]
           https://zhuanlan.zhihu.com/p/396098543

        2. 红叶红不红: Pre-train prompt and predict A systematic survey of prompting methods in natural language processing
           https://zhuanlan.zhihu.com/p/569355491
            1. A Chinese translation

4. ChatGPT提示的艺术：制作清晰有效提示的指南 - binsfan
   The Art of ChatGPT Prompting: A Guide to Crafting Clear and Effective Prompts - Fatih Kadir Akın
   https://zhuanlan.zhihu.com/p/619799922?utm_id=0
    1. good useful. Github: https://github.com/f/awesome-chatgpt-prompts
    2. highlights
        1. 什么是好的 ChatGPT 提示
            1. 清晰度：清晰明确的提示有助于确保 ChatGPT 理解手头的主题或任务，并能够生成适当的响应。避免使用过度复杂或含糊不清的语言，尽量在提示中具体。
            2. 焦点：明确定义的提示应具有清晰的目的和焦点，有助于引导对话并使其保持在轨道上。避免使用过于广泛或开放式的提示，否则会导致不连贯或不集中的对话。
            3. 相关性：确保您的提示与用户和对话相关。避免介绍无关的主题或旁支曲节，这可能会分散对话的主要焦点。
        2. 引导具有意义方向的对话最佳实践
        3. “扮演…”技巧
            1. "我要求你扮演 JavaScript 控制台。我会输入命令，你将根据这些命令回复 JavaScript 控制台应该显示的内容。我希望你只回复一个包含命令在终端输出的代码块，没有其他内容或解释。不要写解释。除非我指示你这样做，否则不要输入命令。当我需要用英语告诉你一些内容时，我会用花括号括起来 {就像这样}。我的第一个命令是 console.log("Hello World");。"

5. 段小草 - ChatGPT Prompt 逆向工程
   https://www.zhihu.com/question/570765297/answer/2956586737?utm_id=0
    1. Steps
        1. 输入原文
        2. Input: "现在，请分析以下文本的角色、风格、语气、长度、段落和emoji使用等特点，给出可以生成这个文本的 Prompt"
        3. 新建一个 ChatGPT，测试Prompt
        4. 让ChatGPT调整Prompt："这个Prompt的效果很棒！现在，请优化这个Prompt，使其适用于更通用的商品推荐场景。你可以在适当的地方插入占位符，以便用户在以后得使用中替换其中的内容。"
    2. Summary
        1. 把 ChatGPT 作为一个逆向工程师来培养，可以预置几个步骤来解锁能力/提升效果
            "Let's think step by step. Prompt 逆向工程是指通过分析给定的文本，返回可以由ChatGPT生成这些文本的 Prompt。现在，请你给出一个 Prompt 逆向工程的例子。好的，现在，我们一起思考一下，为了提高生成内容的质量，一个好的Prompt都需要考虑哪些内容？好的，现在，请给出3条你认为的高质量Prompt"
        2. 给出实际场景中的具体例子，要求 ChatGPT 反写出 Prompt
            "现在，请分析以下文本的角色、风格、语气、长度、段落和emoji使用等特点，给出可以生成这个文本的 Prompt"
        3. 新建 Chat，验证 Prompt 效果，如果效果不好，可以反复修改，直到满足效果为止
        4. 要求 ChatGPT 重写 Prompt 成为模板，使其更加通用（可以使用一定的占位符来做格式化）
            "这个Prompt的效果很棒！现在，请优化这个Prompt，使其适用于更通用的商品推荐场景。你可以在适当的地方插入占位符，以便用户在以后得使用中替换其中的内容。"
        5. 使用 Prompt 模板，提供另一个具体场景，测试其效果，效果不好可以继续修改；效果不错的话，我们就找到了一条适用于某个场景的更为通用的 Prompt

6. ChatGPT 有哪些神奇的使用方式？ - 老曾
   https://www.zhihu.com/question/570729170/answer/3007762683
    1. useful
    2. highlights
        1. 目录
        第一章：不要问漫无边际的问题，要问带目的的问题
        第二章：不要问大而模糊的问题，要问带场景的问题
        第三章：不要问太抽象的问题，要问具体的问题
        第四章：不要问无角色限定的问题，要问带角色扮演的问题
        第五章：不要问过于简洁的问题，要问带全方位要求的问题
        第六章：不要问逻辑混乱的问题，要问有条理性的问题
        第七章：不要问一次性的问题，要问连续性的问题
        第八章：不要问一成不变的问题，要问由浅入深的问题
        第九章：不要问一步到位的问题，要问持续优化的问题
        第十章：不要盲目相信ChatGPT答案，要较验结果的准确性

7. 你在用ChatGPT时有什么独特的prompt心得？ - 运营黑客
   https://www.zhihu.com/question/594837899/answer/2999260766
    1. good. Just add "Let's think step by step". You get 10x better answer

```
