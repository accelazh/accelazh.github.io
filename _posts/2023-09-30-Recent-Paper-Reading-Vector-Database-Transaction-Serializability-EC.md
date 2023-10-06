---
layout: post
title: "Recent Paper Reading: Vector Database, Transaction Serializability, EC"
tagline : "Recent Paper Reading: Vector Database, Transaction Serializability, EC"
description: "Recent Paper Reading: Vector Database, Transaction Serializability, EC"
category: "storage"
tags: [storage, paper, database]
---
{% include JB/setup %}


Vector database and vector index.

```
1. VBASE: Unifying Online Vector Similarity Search and Relational Queries via Relaxed Monotonicity    [2023, 0 refs, OSDI23]
   https://www.usenix.org/conference/osdi23/presentation/zhang-qianxi
    1. Background: VectorDB becomes a fundamental infrastructure for Machine Learning and LLM.
       Evaluation: VBASE offers up to three orders-of-magnitude higher performance than state-of-the-art vector systems e.g. Milvus, especially on complex online vector queries. See Table 4 compare with Milvus.
       Approach: By defining Relaxed Monotonicity (first inventor), which is a kind of "ordering", it enables traditional DB traversal "next->filter->OrderBy Limit 4", no need for Milvus multi-round trial-and-error to find optimal K which is slow. The approach returns approximate results, measured by "Recall", see Table 4 compare with Milvus. The paper targets ANNS and in compare with TopK-based DB. Traditional B+-tree scan is called "brute force table scan", and it's recall is 1.0 (max) but very slow.
       good paper.
    2. highlights
        1. The key diff in Vector DB and Relational DB is, Relational DB's data shows monotonicity, so that they can be indexed by B+-trees.
           But high-dimensional vectors cannot be sorted, while similarity search and approximate query are frequently needed.
           One of the most important query and key diff is TopK query
        2. Basic concept
            1. Vector Search: Finding K nearest vectors to a query vector
            2. ANNS: Approximate Nearest Neighbor Search
            3. ANNS query primitive: TopK
            4. Scope: Billion scope vector search, single machine
        3. Problem: ANNS is inefficient to support complex analytic queries 
            1. Current DB practices of using ANNS
                1. E.g. Find 4 top matches of clothes to ${input_image}, which are under $200
                    1. Building SQL directly on TopK interface: ANNS TopK -> K tuples -> Filter price < $200 -> N tuples -> N>=4? -> Enough results returned
                    2. Inefficient: 1) Optimal K is hard to predict, 2) try-and-error different K multiple rounds
                        1. In another word, the problem of PostgreSQL is it's not built for vector search, it's too slow
                           the problem of Milvus is it needs multiple try-and-error round, which made it slow. "It doubles K and re-executes the query if the previous results are insufficient."
        4. VBASE design
            1. See Figure 1, the common top K starts from a point far away from the target vector, and then uses vector index to go to the nearest neighbors. (Phase 1)
               Then it traversals within the neighbors. The observation is, as traversal goes, it starts to depart from the target vector.
               Start-to-depart is Phase 2. Departure is getting farther and farther is Relaxed Monotonicity (RM).
               RM is what is already happening in the existing Vector DBs. This paper made it a formal definition.
                1. My questions
                    1. RM, the paper's core idea, seems be built at the observation of the departure Monotonicity of Phase 2. But, is there a comprehensive study to show this actually works in large scale, different systems, and different patterns?
            2. RM established the "ordering" of vector traversal. So, as long as Top K is obtained, traversal can be stopped. It's one pass. It works when there is additional filters.
               See Figure 3. Compared to traditional TopK system, where it needs to determine K', VBASE doesn't.
            3. Multi-Column Scan Optimization
                1. Traversal each vector index, but traversal high quality index more times. Merge the results of each vector index.
        5. Implementation
            1. Based on PostgreSQL, 2000+ code change.
                1. My questions
                    1. OK .. the true origin problem maybe PostgreSQL can serve vectors (pgvector), but its search is way too slow.
                    2. In another sense, the paper also suggest we don't actually need a Vector DB. PostgreSQL is enough, with an extra vector index + VBASE.
            2. Integration with Vector Index: HNSW, IVFFlat, SPANN
        6. Evaluation
            1. Table 4: 8 Queries Results Overview
                1. What queries: Single vector (+ filter), Multi-column TopK, Vector range filter, Join
                2. PostgreSQL supports all operations. Milvus is even slower than PostgreSQL at Multi-Column TopK. VBASE is magnitudes faster.
                    1. "Milvus's performance is worse than PostgreSQL which uses sequential table scan, because it cannot finish after several rounds of TopK guesses"
                3. PostgreSQL has best recalls. VBase is better than Milvus, but 1% miss may still too high in large scale.
        7. Generality of Relaxed Monotonicity (at end of Section 3.1)
            1. Does RM apply to all systems and datasets? Yes.
               Graph-based Vector Index, Partition-based Vector Index.
    
    3. ChatGPT: https://chat.openai.com/c/9a4194a6-3400-4ff9-90a4-73c9e09fd179
        1. Vector DBs are specifically optimized to handle vector data by employing advanced indexing and search techniques. They leverage the concept of similarity search, which aims to find the most similar vectors to a given query vector. This is crucial for tasks like content-based recommendation systems, image recognition, natural language processing, and other applications that rely on measuring similarity between vectors.
        
           One popular approach used in Vector DBs is the use of vector indexes based on tree structures, such as k-d trees, VP trees, or ball trees. These indexes allow for efficient retrieval of vectors that are close to the query vector in terms of their similarity. They partition the vector space into smaller regions, enabling fast pruning of irrelevant vectors during search operations.
        
        2. Embedding Storage: Large language models, such as GPT-3, often generate word or sentence embeddings that represent the semantic meaning of the text. These embeddings are high-dimensional vectors. Vector DBs can be used to efficiently store and index these embeddings, allowing for fast retrieval and similarity search operations. This enables applications like finding similar documents, clustering similar texts, or generating recommendations based on semantic similarity.

           Semantic Search: Vector DBs can power semantic search engines that leverage the embeddings generated by large language models. By storing the embeddings in a Vector DB and using specialized indexing techniques, the search engine can quickly identify documents or passages that are semantically related to a given query. This enables more advanced search capabilities, such as finding relevant articles based on their meaning rather than just keyword matching.

           Content Recommendation: Large language models can generate embeddings not only for text but also for other types of content, such as images or audio. By storing these embeddings in a Vector DB, personalized content recommendation systems can be built. The system can identify similar or related content items based on their embeddings, allowing for personalized recommendations tailored to a user's preferences.

           Knowledge Graph Integration: Large language models can generate embeddings for entities and relationships in a knowledge graph. These embeddings can be stored in a Vector DB and used to perform advanced graph-based queries. For example, given a node in the knowledge graph, the Vector DB can quickly find similar or related nodes based on their embeddings, allowing for efficient traversal and exploration of the graph.

           Anomaly Detection: Large language models can be used for anomaly detection tasks, such as identifying fraudulent or unusual behavior in text data. By storing the embeddings of normal behavior in a Vector DB, incoming text can be compared against these embeddings to identify deviations or anomalies. This approach can be particularly useful when dealing with high-dimensional text data, where traditional anomaly detection methods may struggle.

        3. Vector DBs rely on several key technologies to efficiently store and process high-dimensional vector data. Here are some of the key technologies used in Vector DBs

           1. Vector Indexing: Vector indexing techniques play a crucial role in Vector DBs. They enable fast search and retrieval operations by organizing the vector space in a structured manner. Some popular vector indexing methods include:

                a. k-d Trees: k-d trees are binary trees that partition the vector space into axis-aligned regions. They recursively split the space based on the median value of a selected dimension at each level. This allows for efficient pruning and retrieval of vectors within a specific range or proximity to a query vector.

                b. VP Trees: VP (Vantage Point) trees are binary trees that recursively partition the vector space around selected vantage points. They use distance-based partitioning, where vectors closer to the vantage point are placed in the left subtree and those farther away are placed in the right subtree. VP trees are well-suited for approximate nearest neighbor search.

                c. Ball Trees: Ball trees are hierarchical data structures that partition the vector space into overlapping hyperspheres (balls). Each node of the tree represents a hypersphere enclosing a set of vectors. Ball trees are particularly effective for range queries and nearest neighbor searches.

            2. Distance Metrics: Vector DBs rely on distance metrics to measure the similarity or dissimilarity between vectors. The choice of distance metric depends on the application domain and the nature of the vector data. Some commonly used distance metrics include:

                a. Euclidean Distance: Euclidean distance calculates the straight-line distance between two points in a Euclidean space. It is suitable for vector data with continuous and numeric dimensions.

                b. Cosine Similarity: Cosine similarity measures the cosine of the angle between two vectors. It is commonly used to compare the similarity of textual or semantic embeddings, where the magnitude of the vectors is not as important as their direction.

                c. Jaccard Distance: Jaccard distance is used to compare the dissimilarity between sets. It is often employed for binary or categorical vector data, such as document feature vectors.

            3. Distributed Architectures: To handle large-scale vector datasets, Vector DBs often employ distributed architectures. These architectures distribute the data across multiple nodes or clusters, enabling horizontal scaling and parallel processing. Distributed Vector DBs may utilize technologies such as:

                a. Distributed File Systems: Distributed file systems like Hadoop Distributed File System (HDFS) or Apache HBase provide fault-tolerant storage and enable distributed data processing.

                b. Distributed Computing Frameworks: Distributed computing frameworks like Apache Spark or Apache Flink facilitate distributed computation and parallel processing of vector data across a cluster of machines.

                c. Load Balancing and Data Partitioning: Load balancing techniques and data partitioning strategies are employed to evenly distribute the vector data across the nodes in a cluster, ensuring efficient utilization of computational resources.

    4. Humata: https://app.humata.ai/context/ba5ef0d9-3b36-4b00-a4fc-892fbf0e816b
        1. According to [1], there is a division in the semantics between vector and conventional database indices, which makes it difficult to provide a unified system that efficiently runs various types of sophisticated online vector queries. While relational databases can express sophisticated queries through relational algebra, they use indices such as B-tree and B+-tree to expedite query executions, which demonstrate monotonicity. However, no existing systems can support all online similarity queries comprehensively and efficiently. Vector databases, on the other hand, support approximate query types that previous systems do not and show superior query performance and accuracy. They also model the cost of vector computation and rely on sampling-based methods to estimate selectivity. Overall, vector databases are better suited for vector-centric online applications and complex online queries that involve both approximate similarity search and relational operators on scalar and vector datasets.

        2. According to [4], VBASE has several advantages over other approximate vector index-based systems. Firstly, it can support both partition-based vector indices as well as graph-based ones. Secondly, it can integrate indices stored both in memory and on disk seamlessly. Thirdly, it supports all online similarity queries comprehensively and efficiently, including approximate query types that previous systems do not and shows superior query performance and accuracy. Fourthly, it models the cost of vector computation and relies on sampling-based methods to estimate selectivity. Finally, it has a unified engine that enables powerful complex queries leveraging both vector and scalar data indices, creating new optimization opportunities for vector queries. Overall, VBASE is better suited for vector-centric online applications and complex online queries that involve both approximate similarity search and relational operators on scalar and vector datasets.

        3. According to [4], VBASE achieves three orders-of-magnitude higher performance than state-of-the-art vector systems through several technical approaches. Firstly, it uses a unified engine that enables powerful complex queries leveraging both vector and scalar data indices, creating new optimization opportunities for vector queries. Secondly, it supports both partition-based vector indices as well as graph-based ones, and can integrate indices stored both in memory and on disk seamlessly. Thirdly, it models the cost of vector computation and relies on sampling-based methods to estimate selectivity. Fourthly, it supports all online similarity queries comprehensively and efficiently, including approximate query types that previous systems do not and shows superior query performance and accuracy. Finally, it uses a two-phase index traversal pattern that embodies effective data-structure design and relaxed monotonicity to identify if a vector index traversal has entered the second phase, allowing for early termination of TopK search queries. Overall, these technical approaches enable VBASE to achieve three orders-of-magnitude higher performance than state-of-the-art vector systems.

    5. More related materials
        1. What is a Vector Database? - Pinecone Vector Database
           https://www.pinecone.io/learn/vector-database/
            0. very useful article. Good for the introduction of VectorDB.
            1. Embeddings are generated by AI models (such as Large Language Models) and have a large number of attributes or features
            2. advanced features to our AIs, like semantic information retrieval, long-term memory, and more
            3. What's the difference between a vector index and a vector database?
                0. Standalone vector indices like FAISS (Facebook AI Similarity Search) can significantly improve search and retrieval of vector embeddings, but they lack capabilities that exist in any database
                1. Data management
                2. Metadata storage and filtering
                3. Scalability
                4. Real-time updates
                5. Backups and collections
                6. Ecosystem integration
                7. Data security and access control
            4. Since the vector database provides approximate results, the main trade-offs we consider are between accuracy and speed
            5. Algorithms
                1. Random Projection
                    1. The basic idea behind random projection is to project the high-dimensional vectors to a lower-dimensional space using a random projection matrix.
                    2. which results in a projected matrix that has fewer dimensions than our original vectors but still preserves their similarity
                2. Product Quantization
                    1. product quantization (PQ), which is a lossy compression technique for high-dimensional vectors (like vector embeddings)
                3. Locality-sensitive hashing
                    1. Locality-Sensitive Hashing (LSH) is a technique for indexing in the context of an approximate nearest-neighbor search. It is optimized for speed while still delivering an approximate, non-exhaustive result.
                4. Hierarchical Navigable Small World (HNSW)
                    1. HNSW creates a hierarchical, tree-like structure where each node of the tree represents a set of vectors. The edges between the nodes represent the similarity between the vectors
                    2. This could be done randomly or by clustering the vectors with algorithms like k-means, where each cluster becomes a node.
            6. Similarity Measures
                1. Cosine similarity
                2. Euclidean distance
                3. Dot product
            7. Filtering

        2. vector database
           https://zhuanlan.zhihu.com/p/510320750
            1. 整理了业界比较流行的7款vector database，如下
                1. 产品   Milvus  Pinecone    Vespa   Weaviate    Vald
            2. Not All Vector Databases Are Made Equal
               https://towardsdatascience.com/milvus-pinecone-vespa-weaviate-vald-gsi-what-unites-these-buzz-words-and-what-makes-each-9c65a3bd0696

        3. What is a vector database?
           https://learn.microsoft.com/en-us/semantic-kernel/memories/vector-db
            1. The main advantage of a vector database is that it allows for fast and accurate similarity search and retrieval of data based on their vector distance or similarity
            2. Vector databases have many use cases across different domains and applications that involve natural language processing (NLP), computer vision (CV), recommendation systems (RS), and other areas that require semantic understanding and matching of data.

               One use case for storing information in a vector database is to enable large language models (LLMs) to generate more relevant and coherent text based on an AI plugin.

        4. Milvus 开源向量数据库 - 你需要一个真正的向量数据库么
           https://zhuanlan.zhihu.com/p/634013251

            1. 自然语言数据同样可以通过Bert，GPT等模型完成嵌入向量的提取和映射。例如，在高维空间中，“东京”和“日本”的距离要比“东京”和“中国”的距离更近，因为在预训练的语料库中，“东京”和“日本”共同出现的频率更高。借助模型的先验知识，向量检索能轻易地回溯相关的文本，图片，音频，甚至是图文，文音等多模态数据查询。

               向量检索最近的流行与大模型能力的爆发是密切相关的。大模型通常能更有效地理解和生成更高维度、更复杂的数据表示，这为向量检索提供了更精确、更丰富的语义信息。反过来，向量检索也能为大模型提供信息的补全和长上下文的处理能力，从而进一步提升模型的表现。此外，向量检索在大模型的训练和应用中发挥着关键作用。虽然向量数据库并非进行向量检索的唯一途径，但它确实是所有方式中最高效、最便捷的一种。

               在接下来的文章中，我们将进一步探讨为何向量数据库在构建未来AI系统时是必不可少的关键环节。

            2. 相对的，如果你需要快速构建原型系统并对性能有一定要求，FAISS可能是一个好选择。FAISS是Meta开源的一个库，用于高效相似性搜索和密集向量聚类。它能处理任意大小的向量集合，甚至是无法全部装入内存的集合。

        5. Not All Vector Databases Are Made Equal - A detailed comparison of Milvus, Pinecone, Vespa, Weaviate, Vald, GSI and Qdrant
           https://towardsdatascience.com/milvus-pinecone-vespa-weaviate-vald-gsi-what-unites-these-buzz-words-and-what-makes-each-9c65a3bd0696
           https://news.ycombinator.com/item?id=28727816
            0. Good article in depth thinking. Thinking problems by searching multimodal vectors, is a fundamental revolution for how Database should design its search. For example
                1. Is full text search still valid? Should we generate AI embedding and search it instead?
                2. Should B+-tree key search still the first class citizen? Or what customer wants is instead to search similar objects. I.e. treat table row as a vector, search wants vector match, rather than a combo of per key range filters
                3. multimodal is an essential and naturally supported part of VectorDB. It' naturally needed in human scenarios. But it's far from a concept in Relational DB. I.e. Universal Data Representation.
            1. We have come close to involving machine learning on the fundamental level in the search engine experience: encoding objects in a multidimensional multimodal space
                1. Collection-level similarity on object level
                2. Have a notion of geometric similarity as a component in semantics, rather than only specific attributes of the raw object
                3. Multimodality: encode any object — audio, video, image, text, genome, software virus, some complex object (like code) for which you have an encoder and a similarity measure — and search seamlessly across such objects
            2. 7 Vector databases studied. Not including neural search frameworks like Jina.AI, FAISS or deepset's Haystack
                1. Milvus
                2. Pinecone
                3. Vespa
                4. Weaviate
                5. Vald
                6. GSI APU Board for Elasticsearch and OpenSearch
                7. Qdrant
            3. Why milvus need kafka? Why Pinecone also kafka?
                1. How Kafka Powers a Popular Vector Database System
                   https://www.slideshare.net/HostedbyConfluent/how-kafka-powers-the-worlds-most-popular-vector-database-system-with-charles-xie-and-frank-liu-current-2022
                    1. Log as data
                    2. Decoupling of read and write components
                    3. Support for both streaming and batched execution
                    4. All requests that change system state go through WAL

    6. Related papers
        1. Milvus: A Purpose-Built Vector Data Management System    [2021, 38 refs]
           https://www.cs.purdue.edu/homes/csjgwang/pubs/SIGMOD21_Milvus.pdf
            1. Milvus is the top opensource Vector DB.
               Query engine improved from Facebook Faiss on CPU cache, SIMD, GPU. Full fledged distributed system, LSM-structure, with Log Broker and backed with AWS S3.
               Vector Indexes quantization-based and graph-based. Attribute Filtering, Multi-vector Queries.

            2. as referenced in VBASE paper
                1. "Some TopK-based system [76] performs trial-and-error with many values of K 0 until K 0 × filter_selectivity ≥ K, which results in excessive duplicated data access and processing. In contrast, VBASE determines Ke × filter_selectivity = K on-the-fly, therefore achieving both high query accuracy and performance."
            3. highlights
                1. Additional architecture key diffs to SQL databases (e.g. TiDB, CockroachDB)
                    1. A new component "Log Broker" backed by Kafka
                    2. No persistent storage like file or page. Instead, working on AWS S3 + local cache
                        1. It's more like OLAP, that updates are batched and append-only. PAX files are in S3, middle results are persisted in Log Broker. 
                2. Key problems, usecases, and existing work compare
                    1. AI and embedding.
                    2. Table 1 system comparison
                        1. Dynamic data, attribute filtering, Multi-vector query
                            1. Attribute filtering: "Each entity is specified by a single vector and some attributes [65]. The system returns 𝑘 most similar vectors while adhering to the attributes constraints."
                            2. Multi-vector query: "Each entity is stored as multiple vectors [10]. The query returns top-𝑘 similar entities according to an aggregation function (e.g., weighted sum) between multiple vectors."
                        2. GPU support
                        3. Alibaba AnalyticDB-V [65] and Alibaba PASE (PostgreSQL) [68], they follow the one-size-fits-all approach to extend relational databases for supporting vector data by adding a table column called "vector column" to store vectors.
                        4. different types of indexes e.g., quantization-based indexes (including IVF_FLAT [3, 33, 35], IVF_SQ8 [3, 35], and IVF_PQ [3, 22, 33, 35]) and graph-based indexes (including HNSW [49] and RNSG [20])
                            1. The coarse quantizer applies the 𝐾-means algorithm (e.g., 𝐾 is 16384 in Milvus and Faiss [3]) to cluster vectors into 𝐾 buckets. And the fine quantizer encodes the vectors within each bucket. D
                    3. Milvus is adopted by hundreds of organizations and institutions worldwide in various fields such as image processing, computer vision, natural language processing, voice recognition, recommender systems, and drug discovery
                3. Key designs
                    1. Milvus manages dynamic vector data (e.g., insertions and deletions) via an LSM-based structure
                    2. In terms of implementation, Milvus is built on top of Facebook Faiss [3, 35]
                    3. CPU side SIMD and cache optimization.
                        1. Cache-aware design. Improved from Facebook Faiss. A query is run by all threads. Threads are sharded by data vectors, so to reuse them on L3 cache.
                        2. SIM optimization. Support AVX512. Automate SIMD selection.
                    4. GPU side hybrid index to work with CPU and scheduling strategy to work with more GPU devices
                        1. select any number of GPU devices during runtime instead of compilation time
                        2. assigns segment-based search tasks to the available GPU devices. Each segment can only be served by a single GPU device
                        3. From CPU to GPU, Milvus improves the I/O utilization by copying multiple buckets if possible
                        4. if the batch size is bigger than a threshold (e.g., 1000), Milvus executes all the queries in GPU
                    5. Storage Management
                        1. Vector storage
                            1. For single-vector entities, Milvus stores all the vectors continuously without explicitly storing the row IDs. In this way, all the vectors are sorted by row IDs
                            2. For multi-vector entities, Milvus stores the vectors of different entities in a columnar fashion.
                        2. Attribute storage.
                            1. The attributes are stored column by column.
                            2. In particular, each attribute column is stored as an array of ⟨key,value⟩ pairs where the key is the attribute value and value is the row ID, sorted by the key.
                            3. Besides that, we build skip pointers (i.e., min/max values) following Snowflake [16] as indexing for the data pages on disk.
                        3. Bufferpool. 
                            1. Milvus assumes that most (if not all) data and index are resident in memory for high performance. 
                            2. If not, it relies on an LRU-based buffer manager. 
                            3. In particular, the caching unit is a segment, which is the basic searching unit
                    6. Heterogeneous Computing / Distributed systems
                        1. It adopts modern design practices in distributed systems and cloud systems such as storage/compute separation, shared storage, read/write separation, and single-writer-multi-reader
                        2. Log + LSM segments. Segments are snapshot incremental versioned. 
                            1. The computing layer only sends logs (rather than the actual data) to the storage layer, similar to Aurora
                            2. Another optimization is that each computing instance has a significant amount of buffer memory and SSDs to reduce accesses to the shared storage.
                        3. "As a result, users may not immediately see the inserted data. To prevent this, Milvus provides an API flush() that blocks all the incoming requests"
                        4. There are no cross-shard transactions since there are no mixed reads and writes in the same request.
                        5. Looking forward, we plan to leverage FPGA to accelerate Milvus. We have implemented the IVF_PQ indexing on FPGA and the initial results are encouraging.
                    7. Attribute Filtering
                        1. Strategy E: Partitions the dataset based on the frequently searched attribute and applies the cost-based approach (i.e., the strategy D) for each partition
                        2. In particular, we maintain the frequency of each searched attribute in a hash table and increase the counter whenever a query refers to that attribute
                        3. In the current version of Milvus, we create the partitions offline based on historical data and serve query processing online. The number of partitions (denoted as 𝜌) is a parameter configured by users.
                    8. Multi-vector Queries
                        1. Vector fusion: then the aggregated query vector is: [𝑤0 ×𝑞.v0,𝑤1 ×𝑞.v1, ...,𝑤𝜇−1 ×𝑞.v𝜇−1]. Then it searches the aggregated query vector against the concatenated vectors in the dataset to obtain the final results
                            1. But it requires a decomposable similarity function such as inner product.
                        2. Iterative merging: If the underlying data is not normalized and the similarity function is not decomposable
                            1. Thus, iterative merging makes two optimizations over NRA .. Algorithm 2 shows iterative merging
                                1. "else 𝑘′ ← 𝑘′ × 2;"
                4. Applications
                    1. Large scale image search
                        1. 企查查：https://www.qcc.com/
                        2. 贝壳找房：https://www.ke.com/
                    2. Chemical Structure analysis
                        1. Apptech: https://www.wuxiapptec.com
                5. Others
                    1. Product Quantization
                        1. The main idea of vector quantization is to apply a quantizer 𝑧 to map a vector v to a codeword 𝑧(v) chosen from a codebook C [33]. The K-means clustering algorithm is commonly used to construct the codebook C where each codeword is the centroid and 𝑧(v) is the closest centroid to v. F

            n. related materials
                1. Milvus documentation overview introduction
                   https://milvus.io/docs/overview.md
                   https://milvus.io/docs/architecture_overview.md
                    1. highlights
                        1. Milvus uses MinIO as object storage and can be readily deployed on AWS S3 and Azure Blob
                            1. To improve its performance and lower the costs, Milvus plans to implement cold-hot data separation on a memory- or SSD-based cache pool. (like Snowflake)
                        2. Milvus standalone uses RocksDB as log broker. Besides, the log broker can be readily replaced with streaming data storage platforms such as Kafka and Pravega
                        3. Unlike indexing for scalar data, building vector index has to take full advantage of SIMD
                        4. When a search request arrives, it is broadcast to *all* query nodes for a concurrent search.
                        5. A collection in Milvus is split into multiple segments, and the query nodes loads indexes by segment.
                           There are two types of segments, growing segments (for incremental data), and sealed segments (for historical data).
                            1. Handoff: When a growing segment reaches a predefined threshold, data coord seals it and index building begins. 
                    n. My questions
                        1. Index is put to Coordinator Service, and stored in etcd? However in rational DB, index is treated as another table and stored in DB itself
                            1. OK .. it means "Index Coordinator". Index is served by Index Nodes.
                        2. Data is stored in object storage. But I didn't see file storage or page storage like the traditional DB. How transaction updates are managed?
                            1. This is also like Snowflake. The DB works on object storage + cache.
                               https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf
                                1. Table is split into several PAX files. Table files are immutable, due to the choice of S3.
                                   MVCC, write operations produce a newer version of the file.
                                    Snowflake also uses these snapshots to implement time travel and cloning
                                2. My question: I didn't see how logging is implemented in Snowflake, except 
                                    "It would certainly be possible to defer changes to table files through the introduction of a redo-undo log, perhaps in combination with a delta store [32], but we are currently not pursuing this idea for reasons of complexity and scalability."
                            2. So, Milvus write operations need to replace the S3 object into a new one. It should be done in batch to be efficient.
                               So middle results, i.e. logging, needs to be saved elsewhere. That is in the Log Broker, i.e. RocksDB or Kafka. logging needs to be persistent
                        3. Growing segments (for incremental data), and sealed segments (for historical data). Where stores the growing segments?
                            1. Probably, it's an S3 object and is still being appended.
                               Or, In-memory replica + persisted logging


        2. SPANN: Highly-efficient Billion-scale Approximate Nearest Neighbor Search    [2021, 7 refs]
           https://arxiv.org/abs/2111.08566
            1. Referenced as a popular Partition-based Vector Index in VBASE. Simple but efficient vector index building process to support ANNS similarity search with low latency and memory cost. 
            2. highlights
                1. Product Quantization (PQ) - to compress the vectors and save the in memory
                2. Key techniques
                    1. only stores the centroids of the posting lists in memory. a large posting list is stored on SSD. 
                    2. partition vectors into posting lists. goal: limit posting list length, balanced partitioning. 
                        1. Hierarchical balanced clustering: We cluster the vectors into a small number (i.e. k) of clusters iteratively until each posting list contains limit number of vectors
                        2. we replace the centroid with the vector that is closest to the centroid to represent each posting list
                        3. in order to quickly find a small number of nearest posting lists for a query, we create a memory SPTAG [12] (MIT license) index for all the vectors that represent the centorids of the posting lists
                    3. posting list expansion. problem see Figure 1, boundary points are easy to miss.
                        1. Closure clustering assignment: assign a vector to multiple closest clusters instead of only the closest one if the distance between the vector and these clusters are nearly the same 
                        2. Representative replication: use RNG[41] rule, skip assigning x to cluster ij if Dist(cij , x) > Dist(cij−1, cij)
                    4. Query-aware dynamic pruning
                        1. Instead of searching closest K posting lists for all queries, we dynamically decide a posting list to be searched only if the distance between its centroid and query is almost the same as the distance between query and the closest centroid

        3. Ultipa Graph: Designing Highly Scalable Graph Database Systems without Exponential Performance Degradation    [2023, 0 refs, Ricky Sun]
           https://dl.acm.org/doi/pdf/10.1145/3579142.3594293
            1. Ultipa Graph supports 3 cluster setups: HTAP, GRID, SHARD. Compare their PROs and CONs.
            2. highlights
                1. Key problems
                    1. K-hop traversal or finding all shortest paths, traversal large amount of data, led to BSP (Bulky Synchronous Processing) system to exchange heavily amongst its distributed instances
                2. Comparing with exiting graph DBs aiming to be scalable
                    1. Distributed Consensus with Graph HTAP
                        1. Cons: Vertical Scalability, Difficult to handle 10 billion plus nodes and edges
                        2. Example: Neo4j
                    2. Proxy/Nameserver/GRID or Federation. Nameservers act as proxy and aggregates data
                        1. Cons: Non-transparent graph partitioning (human-logic based). No data migration
                    3. Automated SHARD
                        1. Cons: Degraded graph query performance, Sophisticated Cluster Management, Large H/W footprint
                3. Ultipa approach
                    1. In HTAP cluster setup, multiple instances within the cluster can load-balance multiple K-hop queries concurrently.
                       In figure 4, K-hop on Twitter-2010 Dataset. Ultipa performances are magnitudes better
                    2. In GRID cluster setup, plus nameservers and metaservers. Need to partition graph manually with business logic 
                    3. Auto Shard setup. Horizontal scalability leveraging nameserver and metaserver, sharding use statistics rather than business logic directly.
                       Query is assigned with a group of compute node to process. A centralized computing note is used to avoid a large amount of network interaction overhead. 
                4. Related works
                    1. TigerGraph, Neo4j, JanusGraph, ArangoDB
```

Erasure coding.

```
1. StripeMerge: Efficient Wide-Stripe Generation for Large-Scale Erasure-Coded Storage    [2021, 7 refs]
   https://www.cse.cuhk.edu.hk/~pclee/www/pubs/icdcs21.pdf
   https://www.youtube.com/watch?v=lMYYQkv23r8
   https://github.com/YuchongHu/stripe-merge
    1. How to codec transition shorter codecs into longer codecs, by combing the existing data chunks, and generate new parity chunks by reusing existing parity chunks?
       If there is no bandwidth cost, it's called Perfect Merging.
       StripeMerge: Given a set of narrow stripes, how to optimally pair them to generate wide stripes, so that the cost is minimal?
       But somehow the paper only discussed merging two (k,m) code to one (2k,m) code. There can be other schemas.
    2. Highlights
        1. Fig. 1: Compared to prior work NCScale, introduced Perfect Merging
            1. Perfect Merging - wide-stripe generation bandwidth can be completed eliminated
                1. both of their data chunks reside in different nodes
                    1. migration cost
                2. both of their parity chunks have identical encoding coefficients and reside in the same nodes, so to calculate new parity purely by old parities
                    1. My questions
                        1. usually a placement won't put parities at the same node. but replacing node to rack, the paper still applies.
                    2. recalculation cost
            2. Formulate the Perfect Merging problem with Bipartite Graph Model
                1. complete chunk placement set - take all possible placement of a codec, and ignore the order of data chunks, but consider the order of parities chunks
                2. two sets X = Y, each set is a "complete chunk placement set". An edge from X to Y is a Perfect Merging
            3. Theorem 1 - we can always pair two (k,m) narrow stripes into a (2k,m) wide stripe by Perfect Merging
                1. My questions
                    1. The Bipartite Graph Model assumes full placement combinations. In actual deployment, real placement count is sparse w.r.t. it. So, the Theorem 1 may not really be useful. And, Algorithm-G/P isn't actually leveraging Theorem 1.
        2. StripeMerge
            1. Algorithm StripeMerge-G - just greedy
            2. Algorithm StripeMerge-P
                1. Perfect Merging requires "fully parity-aligned".
                   partially parity-aligned - some parities but not all are aligned.
                   i-partial parity aligned pair - a set that has i parities aligned
                2. StripeMerge-P uses i-partial parity-aligned pair set to speed up search.
                    1. and use hashtable to speed up in implementation
            3. OK .. the paper also refers itself StripeMerge-G/P as "two heuristics"
        3. Evaluation
            1. StripeMerge-P performs almost the same with StripeMerge-G
                1. My questions: So why introduce StripeMerge-P? Only to speed up?
                    1. But, See Fig. 6. When k is large (>=32), StripeMerge-P is only ~1/6 faster than StripeMerge-G.
            2. The merge cost is ~10x lower than NCScale.
        n. My questions
            1. But somehow the paper only discussed merging two (k,m) code to one (2k,m) code. There can be other schemas? But this is an interesting problem anyway.
            2. Can we leverage the initial placement to make the later merging easier?
    n. related materials
        1. ECWide: Exploiting Combined Locality for Wide-Stripe Erasure Coding in Distributed Storage [2021] 
           https://www.usenix.org/conference/fast21/presentation/hu
            1. By the same authors. same two universities
        2. OpenEC: Toward Unified and Configurable Erasure Coding Management in Distributed Storage Systems
           https://www.usenix.org/conference/fast19/presentation/li
            1. part of same authors, Patrick P. C. Lee
            2. same two universities
                1. The Chinese University of Hong Kong
                2. Huazhong University of Science and Technology
        3. ECPipe: Repair Pipelining for Erasure-Coded Storage    [2017]
           https://www.usenix.org/sites/default/files/conference/protected-files/atc17_slides_li_0.pdf
            1. One of same author - Patrick P. C. Lee
            2. One of same university - The Chinese University of Hong Kong
        4. NCScale: Toward Optimal Storage Scaling via Network Coding: From Theory to Practice    [2018, 21 refs]
           https://www.cse.cuhk.edu.hk/~pclee/www/pubs/infocom18.pdf
            1. One of same author - Patrick P. C. Lee
               same two universities
            2. We now formalize the scaling problem
                1. transform (n, k)-coded to (n + s, k + s)-coded
                   Remains MDS. Failure domain placement. No centralized role.
                2. reuse the previous code's parities to compute new parities
                3. need to reduce migration cost to fit placement.
        5. SepBIT: Separating Data via Block Invalidation Time Inference for Write Amplification Reduction in Log-Structured Storage
           https://www.usenix.org/conference/fast22/presentation/wang
            1. Same author Patrick P. C. Lee and The Chinese University of Hong Kong
        6. ParaRC: Embracing Sub-Packetization for Repair Parallelization in MSR-Coded Storage
           https://www.usenix.org/conference/fast23/presentation/li-xiaolu
            1. Same author Patrick P. C. Lee and
                The Chinese University of Hong Kong,
                and Huazhong University of Science and Technology
        
        7. ERS: Elastic Reed-Solomon Codes for Efficient Redundancy Transitioning in Distributed Key-Value Stores    [2020, 0 refs]
           https://www.cse.cuhk.edu.hk/~pclee/www/pubs/ton23ers.pdf
            1. Same author Patrick P. C. Lee. Referenced StripeMerge paper.
            2. Follow up work on StripeMerge. It extends to generally codec transition of one RS(k,m) to one RS(k',m). 
                1. Problem 1: How to calculate new parity based on old parities
                    1. Solution: Use k' matrix, but fill dummy zero data chunks to generate k.
                    2. Forward transitioning Algorithm 2
                    3. Backward transitioning Algorithm 4 
                2. Problem 2: How to fit the placement balance
                    1. ERS-aware data placement - Algorithm 3
                        1. Essentially, when placing RS(k,m), already left slots for RS(k',m). the reserved slots are filled with another EC stripe that to be broken apart.
                            1. i.e. row stripe vs cross row stripe
         
        8. Optimal Data Placement for Stripe Merging in Locally Repairable Codes    [2022, 3 refs]
           https://www.cse.cuhk.edu.hk/~pclee/www/pubs/infocom22lrc.pdf
            1. Same author Patrick P. C. Lee and The Chinese University of Hong Kong
            2. Follow up work on StripeMerge. It extends to generally merge of an arbitrary number of LRC stripes. The paper targets to how generate placement.
                1. Note this paper also couples with cross cluster placement of LRC
                2. concepts
                    1. migration cost, recalculation cost
                    2. pre-distributing the second stripe
                    3. pre-aggregating x small-size stripes
                3. Algorithm 4 - Multi-stripe data placement scheme
                    1. The key is AGGORDIS. clusters with id < β do aggregated placement, clusters with id > β do disperse placement (across x different clusters)
                n. My questions
                    1. The paper is missing a key picture to show how the optimal data placement for x small LRC stripes are done
                    2. ideally each of the x small stripes should be placed in the same way, but in Algorithm 4, we need first half small stripes to be placed in aggregated way, and the later half to be placed in disperse way. it violates the independence or symmetric intuitions.

        9. FlexRaft: Minimizing Network and Storage Costs for Consensus with Flexible Erasure Coding    [2023, 0 refs]
           https://www.cse.cuhk.edu.hk/~pclee/www/pubs/icpp23.pdf
            1. Same author Patrick P. C. Lee and The Chinese University of Hong Kong
            2. Follow up work on CRaft. FlexRaft switches to different EC codec schema according to number of server failures, measured by network costs and storage cost

        10. ZapRAID: Toward High-Performance RAID for ZNS SSDs via Zone Append    [2023, 0 refs]
            https://www.cse.cuhk.edu.hk/~pclee/www/pubs/apsys23.pdf
            1. Same author Patrick P. C. Lee and The Chinese University of Hong Kong
            2. Group-Based Data Layout
                1. to organize stripes with coarse-grained ordering for low stripe management overhead
                    1. So, group is to relax ordering of appending EC fragments at each SSD. And the group boundary acts as the barrier to sync ordering offsets.
                2. ZapRAID is an extended Log-RAID design for ZNS SSDs
```

Database transactions.

```
1. Making Snapshot Isolation Serializable    [2005, 458 refs]
   https://dsf.berkeley.edu/cs286/papers/ssi-tods2005.pdf
    1. Referenced in PostgreSQL SSI paper to back Theorem 1: each cycle in serialization history must contains two consecutive rw dependency edges.
       Very good paper.
        1) Illustrated different SI anomalies
        2) Transaction serialization graph representations
            1. Serialization history
            2. DSG(H)
            3. SI-RW diagram.
        3) Categorized dependency types
        4) Proved Theorem 2.1
            1) Two concurrent transactions must have rw dependency
            2) Non serializable SI must have at least two consecutive rw edges
        5) Give the method to verify when SI is serializable
            1) COROLLARY 3.2
    2. highlights
        1. concepts
            1. transaction schedule.
                1. named as transaction history H in paper.
            2. serialization history graph. cycles <=> non-serializable transaction schedule
                1. See PostgreSQL SSI paper
            3. section 1.1 serialization history and version graphs
            4. concurrent transactions - transaction time overlap
            5. section 1.2 Predict Read (no such thing Predict Write)
        2. Snapshot Isolation abnormalities
            1. Example 1.2 SI Write Skew
                1. H2: R1(X0, 70) R2(X0, 70) R1(Y0, 80) R2(Y0, 80) W1(X1, −30) C1 W2(Y2, −20) C2
                   constraint that X + Y > 0
                    1. To fix the write skew, use Select For Update in Tx1 on Y.
                2. SI does not guarantee serializability in all cases,
                    but the TPC-C benchmark application, for example, executes under SI without serialization anomalies
                    1. My questions
                        1. OK .. remarkable. TPC-C CANNOT detect SI write skew
            2. Example 1.3 SI Read-Only Transaction Anomaly
                1. H3: R2(X0, 0) R2(Y0, 0) R1(Y0, 0) W1(Y1, 20) C1 R3(X0, 0) R3(Y1, 20) C3 W2(X2, −11) C2
                    1. Problem: T3 sees T1 happens before T3. T3 sees T2 happens after T3. But T2 sees T1 happens after T2.
                    2. T1,T2 itself are serializable. But even T3 is read-only, adding a T3 makes the whole violate serializability.
            3. Example 1.4 Predicte-based Write Skew
                1. H4 : PR1(P, empty) W1(Y1, eid = ‘e1234’, projid = 2, workdate = ‘09/22/02’, hours = 5)
                    PR2(P, empty) W2(Z2, eid = ‘e1234’, projid = 3, workdate = ‘09/22/02’, hours = 5) C1 C2.
                2. Similar with Example 1.2, but involves Predict Read. And Select For Update won't fix it.
                   Can be fixed by creating a tal_work_hours table
        5. Transactional history theory
            1. Definition 2.1 Transactional Dependencies
                1. i-wr
                2. i-ww
                3. i-rw
                4. pr-wr
                5. pr-rw
                6. wr is either i-wr or pr-wr
                7. rw is either i-rw or pr-rw
                    1. this is the "famous" rw anti-dependency in PostgreSQL SSI paper
                    2. and, a "dependency" must be operating the same or overlapping set of items
                8. Others
                    1. Note the dependency doesn't exclude T1 can completely precede T2 or vice visa
            2. DSG(H), the Dependency Serialization Graph for a history H
                1. See Fig. 1. Note two transactions can have more than one edges and more than one types of dependency 
            3. THEOREM 2.1 - an SI transaction that is NOT serializable, in every cycle there are three consecutive transactions T1, T2, T3 that T1 and T2 are concurrent, T2 and T3 are concurrent. (T1 and T3 can be the same transaction)
                1. Remark 2.1
                    1. If Tm -> wr -> Tn, then Tm must completely precede Tn, that Tm and Tn CANNOT be concurrent
                    2. If Tm -> ww -> Tn, then due to First Committer Wins rule, Tm and Tn CANNOT be concurrent, and Tm must commit before Tn starts
                    3. If Tm -> rw -> Tn, then Tm and Tn are concurrent, or Tm completely precede Tn.
                        1. But, Tn CANNOT completely precede Tm.
                            1. Because SI requires Tm the most recent version whose commit precedes the start of Tm
                            2. It introduces the thinking that Tm should bump its reads when some other transaction committed in middle
                        2. Only rw dependency implies concurrent T1, T2. This implies that rw dependency cannot co-exist with ww and wr dependencies. It makes COROLLARY 3.2 useful to test SI serializability with entering/leaving edge types.
                2. Lemma 2.2 and 2.3
                    1. In a history executed under SI, if we know that there is some Tm -> Tn dependency, and that Tm and Tn are concurrent, we can conclude that
                        1) Tm starts before Tn commits
                        2) Tm -> rw -> Tn
                    2. I.e. concurrent transactions must have rw dependency
                3. From the Theorem proof, and as mentioned in PostgreSQL SSI paper: 
                    1. Furthermore, T3 must be the first transaction in the ENTIRE cycle to commit
                        1. I.e. you can select the earliest commit transaction in the cycle as T3.
                    2. I.e. you can extend the proof of THEOREM 2.1: Select the earliest committed transaction in the cycle as T3. Then follow the dependency -> backwards. It can prove that
                        1) Any Tx -> Ty in the cycle are concurrent
                            1. THIS IS WRONG. See Fig. 6 and COROLLARY 2.4 
                        2) T3 is the earliest committed transaction
                 4. COROLLARY 2.4 - completing the cycle
                    1. Ti.1 ->rw-> Ti.2 ->rw-> Ti.3 ->wx-> Tm.1 ->wx-> Tm.2 ->wx-> · · · Tm.n ->wx-> Ti.1
                       Then each Tm.i runs fully within the lifetime of Ti.2
                        1. COROLLARY 2.4 is NOT saying Tm.1 to Tm.n must be using wx dependency. It still possible to have rw dependencies
                            1. My questions
                                1. But why wx dependency is possible here? From the Proof of Theorem 2.1, all Tm.* pointing to Ti.1 should be concurrent and thus using rw dependency only.
                                    1. Question solved: See Fig. 6, COROLLARY 2.4 is still assuming Ti.3 is the earliest committed transaction. But we cannot a transaction the precedes Ti.1 is also precedes Ti.3  
                        2. the corollary is very important because it outlined the full picture of what a cycle looks like
                            1. very good
                        3. "Of course, there is no implicit limitation in an SI history that there be only one sequence of three successive transactions with rw dependencies that goes back in time.
                            There might be multiple such rw dependencies in sequence or several separated sequences of two or more rw dependencies."
            4. SI-RW diagram
                1. Fig. 3 to illustrate the rw dependency cycle
                2. "any cycle among transactions must somehow 'go back in time' at some point"
                3. This is very useful chart to illustrate SI abnormalities by presenting all of 1) time 2) RW operations 3) dependency type
        6. SDG(H) and Dangerous Structure
            1. Definition 3.5 for Dangerous Structures by SDG(A)
                1. The key is still two consecutive rw dependencies
            2. THEOREM 3.1 If an application A has a static dependency graph SDG(A) with no dangerous structure, then A is serializable under SI
                1. Note, dangerous structure is a sufficient condition but not necessary
                2. COROLLARY 3.2. Suppose an application A has a static dependency graph SDG(A) where, for every vertex v, either there is no vulnerable anti-dependency edge leaving v, or else there is no vulnerable anti-dependency edge entering v. Then A is serializable under SI
                    1. This is the foundation of PostgreSQL SSI
                3. TPC-C is used as the evaluation
                    1. Fig. 13 shows the SDG(TPC-C). Use COROLLARY 3.2 to prove that TPC-C has no SI anomalies
    n. related materials
        1. Serializable Snapshot Isolation in PostgreSQL
           https://drkp.net/papers/ssi-vldb12.pdf
            1. the famous PostgreSQL SSI. Theorem 1 referenced the parent paper.
        2. Conflict Serializability in DBMS
           https://www.geeksforgeeks.org/conflict-serializability-in-dbms/
            1. Defining Conflicting operations. Non-conflicting operations can swap order.
            2. A transaction schedule is called conflict serializable if it can be transformed into a serial schedule by swapping non-conflicting operations
        3. Conflict Serializable is a subset of Serializability
           https://stackoverflow.com/questions/20529800/whats-the-difference-between-conflict-serializable-and-serializable
            1. A serializable but not conflict serializable schedule is
                    T1 : R(A)       W(A) C
                    T2 :     W(A) C
                    T3 :                   W(A) C
               This is not conflict serializable (by precedence graph) but is equivalent to serializable schedule
                    T1 T2 T3
               because T3 blind writes the output in both schedule.
```
