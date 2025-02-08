---
layout: post
title: "Evaluate ChatGPT Usage in Daily Work Scenarios"
tagline : "Evaluate ChatGPT Usage in Daily Work Scenarios"
description: "Evaluate ChatGPT Usage in Daily Work Scenarios"
category: "AI/ML"
tags: [NLP, GPT, LLM]
---
{% include JB/setup %}

Evaluate ChatGPT at different aspects in my daily work.

```
1. ChatGPT to read a paper and I ask questions
    1. Try Facebook Tectonic
       https://chat.openai.com/chat/3c27228a-1e5e-4cf8-b2c5-9b9feda343fb
        1. OK to answer basic questions
        2. When I drill down to more detailed questions that need knowledge background, logic deduction, or deeper thinking .. ChatGPT starts to FAKE
    2. Try "Improved Maximally Recoverable LRCs using Skew Polynomials"
        1. I asked what is "Skew Polynomial". ChatGPT does better than ChatPDF I think
           It did give explanation with examples, rather than saying not found in paper
        2. But .. I really doubt ChatGPT (and related products) is doing logic .. especially on papers that does need math and logic

2. ChatPDF to analyze any PDF, and answer question
   https://www.chatpdf.com/
    1. I tried Facebook Tectonic
        1. basically not working.
    2. Try "Improved Maximally Recoverable LRCs using Skew Polynomials"
        1. It's basically replicating the the content strictly in the paper
           nice part it's it provides the source page number
        2. OK .. I guess ChatPDF chooses to restrict answer strictly to the scope of paper, to ensure correctness, to avoid FAKEing problem of ChatGPT
        3. Nice .. it can give correct referencing books or article names links.
           I didn't verify they truly include the topic I asked, or there are other references missed

3. NewBing to analyze paper PDFs
    1. I tried Facebook Tectonic
        1. Only allow 15 questions .. not usable
        2. The nice part is NewBing prints what it's searching and the sources.
        3. Not working .. cannot answer simple answers
    2. Try "Improved Maximally Recoverable LRCs using Skew Polynomials"
        1. It can give answer and examples about what are "Skew Polynomials" with examples
           Results are similar with compared to ChatGPT
        2. The answer is quite similar with ChatGPT
    n. A summary
        1. I guess the proper usage is to let ChatGPT (families) give paper abstractions, and summarize things that can easily find on paper. I.e. search and summary
        2. For basic knowledge I'm missing, I can ask them. Basic knowledge is not limited to the paper scope 
        3. Ask how XX is used in YY areas. Similar "Scope" & "Survey" questions. Here are where ChatGPT families generally do good. Scope questions.

4. HUMATA - like ChatPDF
   https://app.humata.ai/context/6223f779-32b8-4123-9bcf-9884001d8a4a
    1. Nice. It has a side bar of the paper itself. It can locate to paper pdf.
       I think the answer has better quality then ChatPDF. Not ask FAKEed as ChatGPT/NewBing.
    2. The response is slower than ChatPDF
        1. WTF .. page freeze, saying high demand not responsive
    3. 
       1. When I ask to give examples of "Skew Polynomials", HUMATA gave formulas and texts extracted from the original paper. ChatGPT give external answers
       2. I asked to give concrete examples but not math. HUMATA still gives math formulas from the paper. OK .. better nothing than FAKE

5. Edge Dev - side bar for NewBing
    1. Button is on the top right corner. Ask NewBing.
    2. It's not limited by the 15 answers of NewBing.
    3. It can open my code repo pages and teach code for me?
        1. Now working .. It's a NewBing sidebar but no integration with my code repo

6. ChatGPT to help me learn the The Art of Computer Programming (TAOCP)
    1. ChatGPT
        1. Sometime the service will be interrupted. Refresh page will mitigate it.
        2. Good. ChatGPT families show remarkable value when helping me read long books, enter the scope of new areas
           https://chat.openai.com/chat/92585ea7-81d6-4c55-b128-ee464c212d04
    2. NewBing Edge Dev sidebar
        1. Responses are similar to ChatGPT. But more summarized, and faster 
        2. ChatGPT gives richer responses. This is more helpful than Edge Dev bar
        3. It looks like the NewBing Edge Dev sidebar is still limited to 15 questions ..
           it asks me to ask another topic
    3. Very good for entering new areas
        1. For example, tell ChatGPT to teach you key points in ML model design.
           Let ChatGPT to write code on Ray framework that to run your model.
        2. Robotics, Let ChatGPT tell you key points in certain area, e.g. flight control
           Let ChatGPT write example code in certain flight control algorithm
        3. Especially, ChatGPT is very good at writing code.
           And, to tell you the framework when you don't know something. And to summarize key points.
           Search engine however require you to know something first. This is unfriendly for new areas.

2. ChatGPT to generate the verbose serialization code for my classes
   https://chat.openai.com/chat/fb3f6586-3e71-4fd2-9aae-2f4ac0eacc22
    1. GhatGPT however defaults to use C++ std/boost lib for serialization. not what I wanted.
        1. also, the response is truncated by length
    2. Good, ChatGPT can do this well, if I supply it a few examples.
        1. To my surprise, it knows to use Getters and Setters
        2. the tricky thing is, for every fine detail, I need to train the ChatGPT to be able to write that code correctly
            1. The process is less than ideal. I hope ChatGPT can directly learn our code base.
               That all be a lot simpler. I don't need to teach it about everything
    3. finding more guides online
        1. https://typefully.com/svpino/11-ways-you-can-use-chatgpt-to-write-code-YnkOEF4
        2. Translate code between different languages is a KILLER APP
        3. Another usage is to write a draft version of code, and let ChatGPT polish it to the optimized version
        4. https://medium.com/geekculture/5-chatgpt-features-to-boost-your-daily-work-404478fd70ca

3. ChatGPT to write algorithms the ability
   https://chat.openai.com/chat/13de4e5e-6428-4783-ab8f-df214df59674
    1. NewBing and Edge dev sidebar NewBing cannot output code somehow. ChatGPT is the only choice
    2. Algorithms
        1. write a python neural network with backward propagation 
        2. red-back tree
        3. Partition a set into two subsets such that the difference of subset sums is minimum
            1. OK .. ChatGPT beats most of my interviewees ..
            2. But it says the problem is NP-hard, while it also gives a DP optimal solution? (INCORRECT)

4. ChatGPT to rephrase with a better writing style
    1. ChatGPT cannot preserve bullets in Outlook mail formats. But it's good at synthesizing points, and make it to fluent flat English.

5. Connect Windows Speech Recognition with ChatGPT
    1. Win+H to wake up Speech. Hope I don't need to type at all. This would make a true secretary

6. ChatGPT to teach about GitHub code repo
    1. Ceph BlueStore's bitmap allocator
        1. It can tell the high level structure. But it starts to fake when I ask the specific piece of code.
        2. The source to train ChatGPT is mainly from published articles in English or source code
           But ChatGPT hits problem if it needs to derive high level meaning from low level, which needs strong logic. And when there is public articles to directly answer what you asked
        3. So, the reliable task to ask for ChatGPT is survey and synthesis, requiring little logic, but many reading materials
    2. Not quite reliable, I cannot stop ChatGPT from faking everything ..

7. ChatGPT to answer questions that needs to read length documentation
    1. I asked what does `fsutil query extentinfo <filename>` means and pasted to output to explain. ChatGPT gives very good answer to it. In compare, Google only search a raw documentation, that to answer it I need to combine multiple and may hard to find materials.
       This is a KILLER APP compared to Google

8. Use ChatGPT to ask questions to revise my rollout and rollback plan
    1. surprisingly, ChatGPT can ask good questions. Need special prompt craft to ask ChatGPT to be critique
        1. In theory, we can do PCA analysis on large scale text corpus to extract key axis-es. Now it looks like, ChatGPT can do this and use it point out key points in your questions
        2. Prompt Engineering - A summary
            1. A prompt composes of
                1. Instructions
                2. Context
                3. Input data
                4. Output indicator
            2. To further refine the output (interactively)
                1. Ask to output step-by-step reasoning
                2. Supply apriori knowledge
                3. Give examples
    2. Revise rollout plan: https://chat.openai.com/chat/7448a727-dc08-4864-9c01-f79558c0f5b1
    3. Revise test plan: https://chat.openai.com/chat/27e44020-df96-4cc2-8add-cf9925bad5c1

N. ChatGPT useful prompt collection
    1. "I want you to act as an academic journal editor. Please rephrase the paragraph from an academic angle based on the writing style of the Natural Journal: (接要改写的论文段落)"

    2. "I am an undergraduate student. I want to write an email to a Professor in MIT working on large language models to sell my experience and ask him if he is willing to recruit me as a PhD student in next year."

    3. "Prompt: I am writing a scientific paper. Can you help me think a good acronym of the following topic: A New low power Implantable Wireless Brain Machine Interface."

    4. "Let's think step by step"
```
