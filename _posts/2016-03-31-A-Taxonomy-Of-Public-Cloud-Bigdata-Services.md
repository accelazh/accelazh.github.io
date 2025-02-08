---
layout: post
title: "A Taxonomy of Public Cloud Bigdata Services"
tagline : "A Taxonomy of Public Cloud Bigdata Services"
description: "A Taxonomy of Public Cloud Bigdata Services"
category: "Database"
tags: [bigdata, public cloud, taxonomy, summary]
---
{% include JB/setup %}

We have been through an investigation on public cloud bigdata services. Public clouds, famous ones like Amazon AWS, Microsoft Azure, Google Cloud Platform, have been providing numerous bigdata services. Many of them are overlapped, some are differentiated. We select mainstream pubilc cloud vendors from Gartner 2015 Magic Quadrant [for Cloud Infrastructure as a Service](https://www.gartner.com/doc/3056019/magic-quadrant-cloud-infrastructure-service), and Magic Quadrant [for Enterprise Application Platform as a Service](https://www.gartner.com/doc/3013526/magic-quadrant-enterprise-application-platform).

![Gartner 2015 Magic Quadrants for Public IaaS and PaaS](/images/gartner-cloud-magic-quadrant-2015.png "Gartner 2015 Magic Quadrants for Public IaaS and PaaS")

Since bigdata services from public clouds are numerous, we try to create a categoration framework. The diversed bigdata services can be organized and understood, and we know what a complete set of bigdata services the public cloud should provide. Actually we found AWS' [data analytics flow slides](http://www.slideshare.net/AmazonWebServices/big-data-and-analytics-on-aws/4) suit our need quite well. We borrowed it here and use it as the model of bigdata lifecycle as below. We categorize bigdata services into each of the four stages.

![Bigdata Lifecycle](/images/bigdata-lifecycle.png "Bigdata Lifecycle")

  * Data Ingestion: How data is input into the cloud. The rate, volume, method, protocol of data ingestion may vary.

  * Data Store: How data is stored. The data storage is designed to cope with data characteristics and to help data analysis.

  * Data Analysis: Where data is analyzed iteratively in various of approaches.

  * Data Visualization: Show the data in graph, discover the potential pattern, and demonstrate the business value.

Another set of general principles to categorize bigdata services are [the extended 3Vs by AWS](http://www.slideshare.net/AmazonWebServices/big-data-and-analytics-on-aws/2). It is very effective if you apply them on storage product designs and their trade-offs.

![Bigdata Extended 3V General Principles](/images/bigdata-extended-3v.png "Bigdata Extended 3V General Principles")

  * Velocity: How fast data flow in. It differs for a time-series database/ingestion and an archiving store.

  * Change Rate: How much data is changing. Fast changing data may falls into OLTP databases, while append-only history data is usually seen in OLAP data warehouses.

  * Latency: How fast you access the data. It differs for memory storage/computing, streaming storage/processing, or offline batch computing systems.

  * Processing Requirements: How to compute. For example, realtime streaming processing, statistical analysis, offline machine learning, GPU accelerated deep learning, etc. Differet processing requirement needs different computing platforms and different storage designs.

  * Volume: How large the data is. High speed low volume or low speed high volume usually means different data services on cloud. Users need to balance the choice of price between memory computing, SSD, plain disks or low IOPS disks.

  * Durability: Not all data needs to be kept forever. The data may be droppable after analysis, archived, or keep less samples when it becomes older. Cloud storage usually provide configurable policies.

  * Variety: Structured data, unstructured data, half-structured data require different storage services. File, stream, transactions needs different kind of storage or processing.

  * Availability: How reliable you can access your data. The data can be stored locally, replicated to different city, or even globally distributed. Different storage services may offer different capability, some are always active-active, some are active-backup.

  * Item Size: Item size affects storage design. Large amount of small files brings more metadata, more random read/write, and high pressure for storage. Some storage services are designed efficient for large items, some are good at serving small items.

  * Growth Rate: Data size may grow quickly. The max capacity of different storage may be different. Some are good at scale-out, some may be designed to serve small amount of data but very fast.

  * Request Rate: Users may crowd in at a particular time, they may read large amount of scattered small files, or may have significant data locality, etc. Different access modes affect the choice of data services, how to balance hot and cold data, even data structure design. Cloud vendors usually services of high concurrency, CDN, and auto-scaling.

  * Views: How diverse the customer. Customers may vary in geo-distribution, access mode, hot time, bandwidth, etc. Cloud vendors need to provide variety in services and configurations. Variety of protocol support, multi-site replication, message bus (to share data between various applications and humans), various of visualization, APIs for different modes (e.g. single or batch), etc, are usually needed.

Above is useful. But for simplicty and handy use, in the following article we still choose to use **the bigdata lifecycle model: Ingest, Store, Analyze, Visualize**.

### Data Ingestion

Data ingestion deals with how to efficiently and reliably import large amount of data onto the cloud. Public clouds usually offer different services for different usecases. For example, 

  * Ingestion for streaming data or time-series data

  * Ingestion for database or data warehouse, by importing sql, binary data, or journal

  * Ingestion by (bulk) invoking web API, SQL or NoSQL operations

  * Ingestion by collecting logging messages

  * Ingesting by subscribing messages from a message bus

  * Ingestion by transfer physical storage appliance from site to site

Data ingestion is usually related with data migration, by which cloud vendors provide end-to-end tools to help user move data. Public clouds also provide many supplementary services along with data ingestion

  * Support different protocols. Data ingestion is a place where large amount of heterogeneous protocols can be seen.

  * Data cleaning services based on rules or machine learning, to filter noise, invalid data, or fill in the missing.

  * Data quality management, which should include data cleaning and proper ways to monitor data quality.

  * ETL (Extract Transform Load) services.

  * Workflow engine to orchestrate data operations.

  * Template library to reuse and share artifacts needed above.

  * Customizable web crawlers to collect dedicated information from internet.

### Data Stores

Numerous data store solutions are provided by cloud vendors. If categorized by data format, there can be

  * Structured data, i.e. relational tables. Cloud vendors usually provide relational SQL based databases.

  * Unstructured data, i.e. text, images, videos. Cloud vendors usually provide object storages, or filesystem services.

  * Half-structured data, i.e. key-value pair, json documents, sets, tree, mapping tables, graph. Cloud vendors usually provide NoSQL databases. AFAIK there are generaly 7 families of NoSQL schema:

      * Key-value pair based. It may also support data structures like list, set, tree, etc (e.g. Redis). Object storage can also be put in this category

      * Document based. It may be json document (e.g. MongoDB).

      * Big table (e.g. BigTable, HBase, Cassandra) based. Compared to SQL table, it allows adding much more columns freely.

      * Time-series databases (e.g. InfluxDB). They dedicate to store and query time-series data.

      * Graph databases (e.g. Neo4j). They dedicated to handle graph.

      * Search engines (e.g. ElasticSearch). They are data stores and indexing services that once you put data in, you can search them.

If categorized by OLTP and OLAP scenarios, cloud vendors usually provided different data stores for each of them

  * OLTP is used to support business applications. The data changes fast; the volume is usually smaller. Cloud vendors provide OLTP databases for both SQL (e.g. MySQL) and NoSQL (e.g. Redis). 

  * OLAP is used for data warehousing and analytics. The data is usually append-only; the volume is huge. Cloud vendors provide OLAP databases for both SQL (e.g. AWS Redshift) and NoSQL (e.g. Hadoop/HBase).

We can also categorize data stores by ACID and data consistency. ACID means they support full semantics of transaction (an ordered set of operations). Strong consistency means to once write data, always see the latest. There then can be

  * ACID and strong consistency. Relational SQL databases usually fall in this category (e.g. MySQL). NoSQL data stores hardly do this.

  * Not ACID and eventual consistency. Some NoSQL databases fall in this category (e.g. Cassandra). Note that even they don't support ACID transactions, they usually provide atomic operations. Though there are trade-offs, some databases allow config between eventual consistency and strong consistency (e.g. Cassandra again).

  * ACID and eventual consistency. It is impossible, because the "C" in ACID means consistency. But there are data stores that support atomic transactions but eventual consistency, for example [Google Cloud Datastore](https://cloud.google.com/datastore/docs/concepts/overview).

  * Not ACID and strong consistency. This means don't support transaction, but is stongly consistent. Some NoSQL databases can do this, for example [MongoDB if you always read from the primary node](https://www.mongodb.com/faq#consistency). [Ceph](http://docs.ceph.com/docs/master/architecture/#smart-daemons-enable-hyperscale) is another example.

If categorized by access latency, there can be

  * In-memory databases (e.g. Redis). They provide the lowest latency. They are usually used as cache. However when persistent memory become widely-used, things may change.

  * Common databases (e.g. MySQL). They are the common databases we usually. They work on persistent storages such as filesystem or raw block devices. The underlying store may be rotating disks or SSD.

  * Archiving Store (e.g. AWS Glacier). They are used to archive cold data. The data is usually highly compressed and deduplicated. The read latency can be very high. The price for storing large volume of data is much cheaper.

Besides the above, cloud vendors usually provide all sorts of supplementary services along with data stores

  * Backup services. It can be backup to the same site or backup to remote location for disaster recovery.

  * Remote replication. Synchronized or unsynchronized replicate data to remote location. It may be used for disaster recovery or for fast data access from the remote location.

  * Geo-distribution. Manage the data replication or distribution across multiple global locations. The data may be fully replicated, or each location stores pieces of the whole data.

  * CDN. Allows fast access to your web content from further locations or different internet service providers. CDN is vastly used in China.

### Data Analysis

Data analysis involves a lot of things. If categorized by latency, there can be

  * Offline processing. For example, offline batch MapReduce jobs, offline sql queries, offline machine learning jobs, etc.

  * Realtime processing. For example, realtime timer-series processing, stream processing, ad-hoc SQL queries, etc.

If categorized by different computation pattern, there can be

  * MapReduce. MapReduce interface are usually provided by cloud provider to their users. Spark is usually provided too. They basically follow the computation pattern of MapReduce, in-memory or on-disk.

  * SQL. Usually provided along with relational databases or data warehouses, SQL interface helps users to analyze data.
  * NoSQL. Usually provided along with NoSQL databases, users use NoSQL queries to analyze their data.

  * Statistics. Users can get statistics summaries of their data, and their can do statitics based analysis and learnings on it.

  * Time-series & stream processing. Dedicated time-series database, query interfaces and stream processing frameworks (e.g. Storm, Flint) are provided to user.

  * Serverless computing. AWS provides serverless computing platform, where users write event handlers to process incoming data. It is handy for time-series, stream, or event-based processing.

  * Machine Learning, graph learning, predictions. Machine learning are widely used to analysis data. Some cloud vendors provider platforms where user can implement their own machine learning jobs, some provide ready-to-use machine learning libraries, some provider ready-to-user machine learning models.

  * Deep Learning. Deep learning is a families of machine learning. It is more complex, quickly adopted, and usually involves GPU acceleration. Cloud vendors usually provide dedicated platforms, libraries, or integrate it on existing machine learning platforms (e.g. Spark).

  * High performance computing. HPC usually refers to the scenario of scientific computing, such as DNA computing, cosmos data processing, etc. Cloud vendors usually provide optimized virtual machines, SSD, GPU acceleration, high performance network, etc, for them. Some of HPC can use common bigdata platforms such as Hadoop & Spark, some requires specially desgined computation frameworks, which may be of more tightly coupled architecture.

  * Voice recognition, Nature language processing, etc. Some cloud vendors provide ready-to-use interface for voice recognition, nature language processing, etc. Although they are uderlyingly implemented by machine learning, a read-to-use interface is handy for users.

Besides the above computation patterns, there are many supplementary services provided all together

  * Data orchestration. Cloud vendors provide orchestration framework to manage operations on data. They may be called workflow system or data pipeline, too.

  * Messaging queue or bus. To allow analytics application to communicate with each other in a high performance and flexible way, cloud vendors usually provide messaging queue or messaging bus services. They can be used in publish-subscribe pattern, to exchange data or commands.

  * Service marketplace. Cloud vendors may provider a marketplace, where users can publish or exchange their trained meachine learning models, algorithms or other artifacts, with or without a price.

### Data Visualization

Data visualization is where the value of data is redeemed. It also helps discover potential patterns and value in data. Management layer relies heavily on data visualization. Different type of data visualization service can be categorized as below

  * API or SQL/NoSQL queries. The most direct way to see data is to query them by API or SQL/NoSQL queries.

  * Web-based tables and charts. They can be bind to user-defined queries statements linking to underlying data stores.

  * Dashboards. They are combinations of tables or charts in user-defined layout. The definitions of a dashboard can be exported/imported to templates in XML, Json, YMAL, etc, to be shared or reused later.

There are several aspects that matters to the quality and variety of data visualization services provided by cloud vendors. They are categorized as below

  * The refresh frequency of visualization tables and charts may vary between vendor implementation. They may need manual refresh, auto update in several seconds, or always synchronized with backend.

  * The variety of tables and charts for user to select may vary between cloud vendors. Usually more types and more themes are favorable.
  
  * The ability to gather multiple data sources, which may be heterogeneous, with numerous data formats and protocols. The gathered data are properly joined and visualized in user-end tables and charts.

### Others

  * Updated 2016-8-9: [onurakpolat/awesome-bigdata](https://github.com/onurakpolat/awesome-bigdata) gives an impressive list of popular bigdata frameworks and their categorizations. Worth reading.
