---
layout: post
title: "A Holistic View of Distributed Storage Architecture and Design Space"
tagline : "A Holistic View of Distributed Storage Architecture and Design Space"
description: "A Holistic View of Distributed Storage Architecture and Design Space"
category: "technology"
tags: [cloud, storage, architecture]
---
{% include JB/setup %}


The article summarizes my (years of) experiences on software architecture. Architecture design is essentially driven by __philosophies__ as the generator engine that governs all knowledge. From the __organization view__, we can find why and how architecture design process and skills are required that way. Common __methodologies__ and __principles__, viewed from the philosophies, provide guidance to carry out architecture design with quality. An architect needs an armory of techniques for different __system properties__. I categorize __Reference architectures__ in each distributed storage area, summarize __architecture design patterns__ from them, and connect into __technology design spaces__.


# Software architecture - a philosophy perspective

Software architecture is a modeling of the reality world, a language, and a human mind creation that to assist human mind. Language, is an interesting topic. The three together are deeply inter-connected, pointing why, what and how to handle software architecture.

The next and following chapters tell about knowledge in software architecture. But this first chapter tells about the engine that generates the knowledge.

__Reality, language, and human mind__

Firstly, __the modeling of the world is human language__. Human language evolved for thousands of years, enriched by distinctive civil culture, polished by daily interaction among population, and tested by full industry use and creation. Grab a dictionary, you learn the world and mankind. 

Next, the modeling tool is also a model of the model-er itself. I.e. __human language is also the modeling of human mind__. Thinking is carried and organized by language. Language is structured in the way how human mind is capable to perceive the world, rather than how necessarily the world itself has to be. E.g. software designs by high cohesion low coupling, which is also the principle of how words are created in language. Like they are to reduce software complexity, they do because human thinks this way.

We can say __human language, mind, and the perceivable reality are isomorphic (of the same structure)__. The expedition into the outer world is the same way with exploring into the deep heart. Losing a culture, a language, is the same with losing a piece of reality. As the two sides of a coin, human language is both the greatest blessing how mankind outperforms other creature beings, and also the eternal cage how farthest human mind is capable to perceive.

__About software architecture__

Software architecture is a language, a modeling of the reality world, and a human mind creation to assist human mind. __The essence of software architecture__ is to [honestly reflect the outer world](https://www.zhihu.com/question/346067016), to introspect into the inner mind, and to conceptually light up where it is dark missing. The answer is already there, embedded in the structure, waiting to be perceived.

The question is not what software architecture itself is, nor to learn what software architecture has, but to understand the landscape of world and mind, where you see the hole that needs "software architecture" to fill. You __predict and design__ what "software architecture" should be, can be, and will be. There can be 3000 parallel worlds each with a different software architecture book; what we have here is just one.

Besides, __knowledge and experience are themselves good designs__. They are essentially a domain language, a reusable piece of world modeling, thus also explains why they are useful across daily work and even substitutes design skills. Knowledge is not to learn, but to observe the art of design tested by human act.

// TODO Add a pic about the triple mapping relation

__Side notes: explaining with examples__

For __"high cohesion low coupling" in human language__, imagine an apple on a disk. People name them with "apple" and "desk", rather than a "half apple + half desk" thing. Like selecting what to wrap into an object in Object-Oriented (OO) design, the naming "apple" and "desk" practices "high cohesion low coupling".

To drill deeper, "high cohesion" implies "going together". The __underlying axis is time__, during which the apple goes with itself as a whole. The edges of the apple and the desk intersect, but they have different curves, and they can be decoupled (separated if you move them). Another __underlying axis is space__. Human senses apple and desk with basic elements like shape and color. These __sense elements__ grow on axes of time and space, to be processed into human language. The processing principles look like those from software design, or to say, software design principles are crafted to suit human mind.

An imagined creature can have a totally different language system and thinking mind, if they do not rely on visual sights like human, or even not with time and space axes. They may not need "high cohesion low coupling" as a thinking principle neither. E.g. they can process information like how organic biology evolves. 

For __human language is also a cage__, remember language is a modeling of the reality. __Modeling__ implies "less important" information are dropped to ease the burden of human cognition. Are they really less important? Words are to __reuse__ the same concept for events happened at different time, which saves duplicates. But are they really duplicates? The necessity of language is itself a sign that human mind is unable to process "full" information. Relying on language, the ability is crippled, limited, caged.

More, human mind can hardly think without underlying __time and space__ axes. Human words, at the bottom layer of the abstraction tower, can hardly go without "human-organ-oriented" __sense elements__. People frequently need daily chats, to sync drifts on abstract concepts. Even language itself is becoming a bottleneck, between human-to-machine, population-to-population information exchange.

For __"software architecture" hole in the world and mind landscape__, you all see more in the following of the article. Though most associate "software architecture" with technology, it is also determined by organization and process needs. Various "needs" in different domains flow into the gap of "software architecture", crafted to be processed and expressed in a suitable language for human mind. Together they evolve into the internal meaning of "software architecture".

For __predict and design what "software architecture" should be__. It can be explained as the method of learning. The plain way is the learn what it is, the structure, the composition, cover the knowledge points, and practice using. The better way is to first understand the driving factors, landscape, and dynamics behind. You can see the source and direction of it, even to the end and final limitation. You can also see the many different alternatives, possible to happen, but eventually not chosen by the real world industry, due to certain reason in the back. You should be able to define your own methodology, given your local customized needs. You can forget the knowledge and create any on your own.


// TODO Add a picture about the apple/desk cut


# Why need software architecture

There are various aspects why software architecture is necessary, besides technology. These aspects together define what software architecture should be, and correspondingly the methodology and knowledge landscape developed.

Technology aspects

  * __Handling the complexity__. Software design are separated into architecture level, component level, and class level. Each level popularize with own techniques: 4+1 view, design patterns, refactoring. Any challenge can be solved by adding one layer of abstraction.

  * __Decide key technology stack__. Internet companies commonly build services atop opensource stacks across different domains, e.g. database, caching, service mesh. Which stack to use affects architecture, and are often evaluated with technology goals and organization resources.

  * __Cost of faults__. The cost of correcting a fault at early design is way lower than at full-fledged implementation, especially the architecture level faults that need to restructure component interconnects.

Capturing the big

  * __Non-functional requirements__. Typically, availability, scalability, consistency, performance, security, COGS. More importantly, possible worst cases, how to degrade, critical paths. Also, testability, usability, quality, extensibility, delivery & rollout. They are not explicit customer functional needs, but usually more important, and touches wide scope of components to finally implement.

  * __Capturing the changing and non-changing__. Architecture design identifies what changes quickly, and what can be stable. The former is usually localized and encapsulated with abstraction, or outsourced to plugin. The later is designed with an ask "can this architecture run 1/3/5 years without overhaul", which usually reflects to components and interconnections.

  * __Issue, strategy, and decision__. Architecture is where to capture key issues in system, technology, organization. Strategies are developed to cope with them. And a explicit track of design decisions are documented.

  * __Clarify the fuzziness__. At architecture step, not uncommonly the customer requirements are unclear, problems are complex and clouded, future is unstable, and system scope is unknown. The architect role analyzes, defines, designs solution/alternatives, and builds consensus across teams.

  * __Capture the big__. Architect role needs to define what system properties must be grasped in tight control throughput project lifecycle. They map to the __project goals__ of success and key safety criteria. More importantly, architect role needs to decide what to give up, which may not be as easy as it looks, and reach consensus across teams.  

Process & Organization

  * __Project management__. Architecture step is usually where the cost effort, touching scope, delivery artifact, development model; and resource, schedule, quality can be determined and evaluated. It is also where to closely work with customers to lock down requirements. Project management usually works with the architect role.

  * __Review and evaluation__. Architecture step is usually where the key designs are reviewed; the key benefit, cost, risk are evaluated; throughput capacity breakdown are verified; and all user scenarios and system scenarios are ensured to be addressed. This usually involves stakeholders from different backgrounds and engage with senior management.

  * __Cross team collaboration__. Architecture touches various external systems and stakeholders. It is when to __break barrier and build consensus__ cross teams or BUs. It is when to ensure support and get response from key stakeholders. It is where to drive collaboration. Unlike technology which only involves oneself, driving collaboration can be a larger challenge.

  * __Tracks and lanes__. The architect role usually builds the framework, and then the many team members quickly contribute code under given components. It sets tracks and lanes where the code can grow and where not, i.e. the basis of intra-team collaboration. Future, the tracks and lanes are visions for future roadmap, and standards for team to daily co-work.


// TODO Add a pic about architect role, that inter-connects project PM, dev teams, customer requirements, key technology decisions. and like Management (risk, critical path).



# Different architecture organization styles

What an architect role does and means in real world industry are somehow puzzled. From my experience, this is due to architecture step is organized differently at different companies. At some, architect is the next job position of every software developer. At some others, I didn't even see an explicit architect job position. 

  * __Architect the tech lead__. Usually seen at Internet companies. The architect role is taken by a senior guy in the team, who masters technology stacks and design principles. The architect makes decision on which technology stack to use, and builds the framework for the following team members to fill concrete code. The architect role is in high demand, because Internet companies quickly spin up App after App, each needs its architect, while the underlying opensource infrastructure is relatively stable. Both the business value and technology stack win traction. The API richness in upper App level implies more products and components to host new architects, while infra level generally has simpler API and honors vertical depth.

  * __Architecture BU (i.e. department)__. Seen at Telecom companies. Architects work with architects, software developers work with software developers; they reside at different BUs. The architecture results are handed off in middle, following a waterfall / CMMI model. The architecture designs on more stable, even standardized requirements, with very strict verification, and delivers completeness of documentation. Strong process, and expect more meetings bouncing across BUs. Employees tend to be separated into decision making layer and execution layer, where the later one expects long work, limited growth, and early retire. 

  * __Peer-to-peer architect__. Usually seen at teams building dedicated technology. Unlike Internet companies spinning up Apps horizontally atop many different technologies, such team vertically focuses on one, e.g. to build a database, a cloud storage, an infrastructure component, i.e. 2C (former) vs 2B (later) culture. No dedicated architect job position, but shared by everyone. Anyone can start a design proposal (incremental, new component, even new service). The design undergoes a few rounds of review from a group of senior guys, not fixed but selected by relevance and interest. Anyone can contribute to the design, and can join freely to set off with project development. Quite organic. Technology is the key traction here, where new architecture can be invented for it (e.g. new NVM media to storage design). 

  * __System analyst__. Usually seen at companies selling ERP, or outsourcing. The systems are heavily involved into customer side domain knowledge. And the domain knowledge is invalidated when selling to another customer from a different domain. Because of new background each time, comprehensive requirement analysis and architecture procedures are developed. When domain can be reused, domain experts are valued, where __knowledge and experience themselves are good designs__. Domain knowledge can win more traction than technology, where the later one more leans to stability and cost management.

  * __Borrow and improve__. Usually seen at follower companies. If not edge cutting into no man's land, __reference architecture__ (top product's architecture) can usually be found to borrow from, to customize and improve. This is also benefited by the wide variety of opensource. Reference architecture, standing on the shoulder of giants, are widely used in software architecture processes, e.g. comparing peer works, which is another example of knowledge and experience themselves are good designs. Market technology investigation survey are high demand skills.


# Key processes in software architecture

As preparation, architecture design requires below knowledge and skills

  * Downstream, __understand your customer__. The customer here also includes downstream systems that consume yours. Know customer to capture key aspects to prioritize in architecture, and more importantly what to de-prioritize (E.g. favor latency over cost? Is consistency and HA really needed?). It helps identify the risks (E.g. festival burst usage, backup traffic pattern). Besides, well defining customer space reveals future directions the architecture can evolve.  

  * Upstream, __understand what your system is built atop__. A web App can be built atop a range of server engines, service mesh, database, caching, monitoring, analytics, etc. Mastering the technology stacks is necessary for designing architecture that works with the practical world, and for choosing correct technology stacks that suit project goals and team capabilities. 

  * Externally, __understand the prior of art__. To design a good system, you need to know your position in the industry. Reference architecture can be discovered and borrowed from. Existing technology and experience should be leveraged. E.g. given the richness of opensource databases, designing a new data storage is even a selection and cropping of existing techniques. Participating in meetups helps exchange industry status, and to ensure your design is not drifting away into a pitfall. 

  * Internally, __understand your existing systems__. Understand the existing system to make designs that actually work, and to correctly prioritize what helps a lot and what helps little. Learn from past design history, experience, and pitfalls, to reuse and go the right path. 

  * Organizationally, __broaden your scope__. Architecture design involves interacting with multiple external systems and stakeholders. Be sure to broaden your scope and get familiar with them. Communicate with more people. Solid soft skills are needed for cross team / BU collaboration, to break barrier and build consensus, and to convey with action-oriented points, concise, big picture integrated with detailed analysis.

I lean more to peer-to-peer architect style mentioned above. Many can be sensed from [GXSC's answer](https://www.zhihu.com/question/24614033/answer/497338972). At each step, be sure to engage __talk with different persons__ which significantly improves design robustness. Rather than the design results, it's problem analysis and alternative trade-off analysis that weight most.

  * Firstly, __problem analysis__. Design proposal starts from [innovation](/technology/Notes-on-How-to-do-Innovation). Finding the correct problem to solve is half-way to success. The cost and benefit should be translated to the final __market money__ (Anti-example: we should do it because the technology is remarkable. Good-example: we adopt this design because it maps to $$$ annual COGS saving). The __problem scope__ should be complete, e.g. don't miss out upgrading and rollout scenarios, ripple effect to surrounding systems, or exotic traffic patterns that are rare but do happen in large scale deployment. __Risk__ should be identified; internally from technology stacks, externally from cross teams, market, and organization. __The key of management is to peace out risks__, same with managing the design.

  * One important aspect from problem analysis is __prioritization__. Architecture design, even the final system, cannot address each problem. You must decide __what to discard__, what to suppress, what to push down to lower level design, what choices to make now and what to defer, what to push into abstraction, what to rely on external systems, what to push off as future optimization; and to decide what are the __critical properties__ you must grasp tightly throughout the project lifetime and monitor end-to-end. I.e. __the other key of management is to identify the critical path__. Prioritization are usually determined by organization goals, key project benefits and costs, and the art to coordinate across teams.

  * Next, __find alternatives__. To solve one problem, at least two proposals should be developed. __Trade-off analysis__ is carried out to evaluate the Pros and Cons. Usually, Pros yet have special cases to make it worse, and Cons yet have compensations to make it not bad. The discussion is carried out across team members, up/downstream teams, stakeholders, which may in turn discover new alternatives. The process is __iterative__, where the effort is non-trivial, multiplied, because it's not developing one but a ripple tree of solutions. Eventually you explored the completeness of __design space__ and __technology space__, and reached consensus across team. Choosing the final alternative can be carried out with team voting, or with a [score matrix](https://www.productplan.com/learn/prioritization-matrix-example/) to compare.

  * __Review__ with more people. Firstly, find one or two local nearby guys for __early review__, to build a more solid proposal. Next, find __senior and experienced__ guys to review, to make sure no scenarios are missing, all can be reused are reused, and the solution is using the best approach. Then, involve key __upstream__ guys, to ensure required features, load level, and hidden constraints, are actually supported; and to ensure their own feature rollout won't impact yours. Involve key __downstream__ guys, to ensure the new system addresses what they actually want. It's important to involve key __stakeholders__ early; make sure you gain support from organization, you deliver visibility, and you align with high level prioritization.

  * Then __evaluation__ for the architecture design. Make sure the problem analysis, every customer __scenario__ and system scenario, and project goals, are well addressed. Make sure __non-functional__ requirements are addressed. Make sure the key project __benefit and cost__ are verified in a __data driven approach__, with actual production numbers as input, using a prototype, simulation tools, or math formulas to model. Make sure the system can support required __load level__, by breaking down throughput capacity into each component. Make sure the system handles the __worst case__ and supports graceful throttling and downgrade. Make sure the __logic has completeness__; e.g. when you handle a Yes path, you must also address No path; e.g. you start a workflow, you must also handle how it ends, go back, interleaved, looped. Make sure __development and deliver__ are addressed, e.g. how to infra is to support multi-team development, the branching policy, component start/online/maintenance/retire strategies, CI/CD and rollout safety. Also, make sure __hidden assumptions__ and constraints are explicitly pointed out and addressed.

  * Finally, it's the __documentation__. On practice, it involves a short "__one-pager__" document (actually can be < 20 pages), and slides for quick presentation, and spreadsheets for data evaluation. Nowadays culture lean more to lightweight document, central truth in codebase, and prioritize agile and peer-to-peer communication. Problem analysis and alternative trade-off analysis usually weight more in document than the design itself, where __defining the problem space__ is a key ability. Architecture design part usually includes key data structure, components, state machines, workflows, interfaces, key scenario walkthrough, and several detailed issue discussion. Importantly, the document should track the change history of design decision, i.e. how they reach today, and more specifically the __Issue, Strategy, Design Decision__ chain. 

  * Another output of architecture design are __interfaces__. Interface design does have principles (see later). They are the tracks and lanes where following development start. They reveal how components are cut and interactions to happen. They also propagate expectations of your system to external systems, such as how they should co-work, what should be passed.

__Architecture is designed to evolve__, and prioritized to make it evolve faster. [Ele.me payment system](https://mp.weixin.qq.com/s/mtPQLSONUCWOC2HDPRwXNQ) is a good example in a 5 year scope. Competency of nowadays software depend on the velocity it evolves, rather than a static function set. 

  * __[Simple is beauty](https://xie.infoq.cn/article/5e899856e29017c1079b3be86)__. Initial architecture usually only address key requirements. What changes and not changes in several year's scope are identified and addressed with abstraction. __[MVP](https://en.wikipedia.org/wiki/Minimum_viable_product)__ is a viable first deployment, after which it yet becomes challenging how to "replace wheels on a racing van". 

  * __Highway is important__. Functionalities in software resembles to tall buildings in a city, where highways and roads are key how they build fast. These architecture aspects are less visible, usually under prioritized, but are life critical. Inside the system, they can be the debugability, logging, visibility and monitoring. Have they defined quality standards? Do monitoring have more 9s when the system is to be reliable? From infrastructure, they can be the tooling, platform, config system, fast rollout, data obtaining convenience and analytics, scripting. At organization level, they can be the team process and culture to facilitate agile moves. Externally, they can be the ecosystem and plugin extensibility. E.g. [Chrome](https://developer.chrome.com/docs/apps/first_app/) with plugins designed as first-class. E.g. [Minecraft](http://gametyrant.com/news/5-best-modding-tools-for-minecraft) published tools to build 3rd-party mods. E.g. [Opensource Envoy](https://mattklein123.dev/2021/09/14/5-years-envoy-oss/) designs for community engagement from day 1.

  * Build the __feedback loop__. Eventually after project rollout and deploy, you should be able to collect data and evaluate the actual benefit and costs. New gaps can be found, and yet facilitate a new round of design and improve. How to construct such feedback loop with __data driven__ should be taken into consideration of architecture design. 

The last point is about __driving the project__. The architect role is usually accompanied with ownership, and be responsible to the progress and final results. Driving goes not only the architecture step, but also along with entire project execution. Many can be sensed from [Daoyan's article](https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzA5OTAyNzQ2OA==&mid=2649721202&idx=1&sn=97b3edaa344a1d901ee6ad4b8c4830e4).

  * There can be timeline schedule issues, new technical __challenges__, new blockers, more necessary communication with up/downstream; previous assumptions may not hold, circumstances can be __changed__, new risks will need engage; there can be many people joining and many needs to coordinate, and many items to follow up.  

  * Besides the knowledge and communication skills, driving involves the __long time perseverance__, attention, and care. The ability to find real problems, to prioritize and leverage resources, to push, the experiences, and the skillset of __project management__, are valued. To drive also means to __motivate__ team members to join and innovate. The design becomes more robust, completed, improved, with more people help; and with people from __different perspectives__ to look.

  * More, __driving is a mindset__. You are not who asks questions, people ask questions to you, and you are the final barrier to decide whether problem is solvable or not. The most difficult problems naturally routes to you. If solving the problem needs resource, you make the plan and lobby for the support. You make prioritization, you define, and you eat the dogfood. The team follow you to success (if not otherwise). 

// TODO add pic for the feedback loop of design->implement->evaluate


# Key methodologies in software architecture

Software architecture is a large topic that I didn't find a canonical structure. I divide it into process (above), methodologies (this chapter), principles, system properties and design patterns, technology design spaces. The article is organized as it.

  * __Process__. Already covered in the above chapters. It involves how real world organizations carry out architecture design, and conceptually what should be done for it. 

  * __Methodologies__. The analysis method, concept framework, and general structure, to carry out architecture design. They also interleave with principles and philosophies. Methodologies change with culture trends, organization styles, and technology paradigms. But throughout the years, there are still valuable points left.

  * __Principles__. Architecture level, component level, class level each has many principles, common or specific. Essentially they are designed to reduce mind burden, by letting the code space to mimic how human mind is organized.

  * __System properties and design patterns__. Distributed systems have non-functional properties like scaleout, consistency, HA (high availability). Various architectural design patterns are developed to address each. They are the reusable knowledge and domain language. Best practices can be learned from reference architecture, more market players, and historical systems; where __architecture archaeology__ systematically surveys though the past history of systems.

  * __Technology design spaces__. A technology, e.g. database, can evolve into different architectures after adapting to respective workload and scenarios, e.g. OLAP vs OLTP, in-memory of on disk. Exploring the choices and architectures, plotting them on the landscape, reveals the design space. With this global picture in mind, the design space landscape greatly helps navigating the new round of architecture design.

__Managing the complexity__

The first and ever biggest topic in architecture design (or software design) is to __handle complexity__. The essence is to __let the code space mimic human mind__, i.e. how the human language is organized (if you have read the philosophy chapter). Human language is itself the best model of the complex world, which is a "design" polished by human history, and yet shared by everyone. Domain knowledge is thus helpful, as it is the language itself. When code space is close to the language space (or use a good metaphor), it naturally saves everyone's mind burden.

Below are conceptual tools to handle complexity. 

  * __Abstraction__. Any challenge can be solved by adding one layer of abstraction. The tricky part is you must precisely capture, even predict, __what can change and what not__. It's non-trivial. E.g. for long years people tried to build abstract interface across Windows API and Linux API, but today what we have is "write once glitch somewhere". You still need to examine down the abstraction tower to the bottom. Because coding interface cannot constraint all __hidden assumptions__, and non-functional properties e.g. throughput and latency, compatibility. Information in the flow can become missing and distorted, after passing along the abstraction tower, resulting in incorrect implementation.

  * __Information flow__. Typical design captures how code objects flow around the system. But instead, you should capture how __information described in human language__ flow around the system. Language information is __symmetric__ at the sender and receiver components, but the implementation and representation varies (e.g. you pass "apple" across the system, rather than DB records, DAO, bean objects, etc). __Dependency is essentially a symmetry__, where there is possibly no code references, but semantics linked (e.g. apple has color "red", that's where everywhere of your system must handle correctly). Language information carries the __goal__, which the code should align to, i.e. the code should align to the __human language model__. Human language is consistent compared to the code objects passing in the system; the later one becomes the __source of bug__ when misalignment happens at different layers of system. The design principle eventually leads to "__programming by contract__", "__unbreakable class__" (a component should work, with no assumptions to the outside, regardless what the caller passes into), semantics analysis; but more to learn from. 

  * __High cohesion low coupling__. Human concepts, or say words in language, are all constructed following the rule of "high cohesion low coupling". This is __how human mind works__, and to follow which, the code design saves mind burden. The topic is related to __change and dependency__. High cohesion encapsulates changes, which localizes code modification impact. __Changes pass along the wire of dependency__, that's why low coupling works to reduce undesired propagation. Good encapsulation and delegation requires to predict future changes, which is usually not easy; instead of adding unnecessary OO complexity, it oppositely leads to another [KISS](https://en.wikipedia.org/wiki/KISS_principle) design. 

  * __Name and responsibility__. The most difficult thing in software design is giving names. It's not to say fancy names are hard to find, but to say, __being able to name something means you have already grouped the concept in a high cohesion way__ (e.g. you can name "apple", "desk", but cannot name "half apple + half desk"), which inherently leads to good design. Next, __a name defines__ what a thing is, is not, can do, and cannot do; that's the __responsibility__. Saying objects should call be their names, is to say objects should call by interfaces and responsibility. Finally, when you can __describe the system with fluent human language__, i.e. with __good names and information flows__, you are naturally doing the good design. To do it better, you can organize the talk with consistent abstraction levels, rather than jumping around; if so, it means the design abstraction levels are consistent and self-contained too. Remember __design is a modeling to human language__ (if you have read the philosophy chapter).

  * __Reuse__. If a component is easy to reuse, it naturally follows high cohesion and good naming responsibility. Design for reuse is recommended, but avoid introduce extra encapsulation and delegation, which results in high OO complexity. Refactor for reuse is recommended, but refactor usually requires global picture knowledge, which contradicts with the goal that changes should be localized. __Reference architecture__ is another reuse to reduce mind complexity. Find the top product and opensource to learn from. Find the popular framework which teaches good designs. The past experience here becomes its domain knowledge, shared by team members, and changing points are more predictable. 

  * __Separate of concerns__. Divide and concur, decomposition, are the popular concepts. Decouple on the boundary of minimal dependency links. Make components __orthogonal__ from each own space. Make API __idempotent__ from timeline of calls. To truly separate concerns, methodologies are naturally required such as encapsulation, knowledge hiding, minimal assumptions. In theory, any complexity can be broken down into handy small pieces, but beware of the information flow distorted in between, and the missing holes in responsibility delegating.

  * __Component boundary__. Separating components and sub-components eases mind memory usage. Component boundary should be cut at __what changes together__. If an upstream service change is frequently coupled with a downstream service change, they should have been put into the same component. Violating it is the common case where micro-service messes up the system. High organization collaboration cost is another place to cut component boundary, see [Convey's Law](https://en.wikipedia.org/wiki/Conway%27s_law).

Design complexity can be formulated and evaluated using scores on dependency. I found [D Score](https://book.douban.com/subject/26915970/) interesting. And this [article](https://thevaluable.dev/complexity-metrics-software/) lists other measures. These methods are less popular probably because domain knowledge is more effective to handle complexity. In general,

  * __"D Score"__ measures software complexity by the number of dependencies. Dependency links inside the component is adding to cohesion, otherwise adding to coupling if pointing to outside. The two types of dependency links are summed up, with a formula, as the final score.

  * __"Halstead Metrics"__ treat software as operators and operands. The total number of operators and operands, unique numbers, and operand count per operator, are summed up, with a formula, as the final score.

  * __"Cyclomatic Complexity"__ treat software as control flow graph. The number of edges, nodes, and branches, are summed up, with a formula, as the final score.

// TODO https://mp.weixin.qq.com/s?__biz=MzA4NTkwODkyMQ==&mid=2651257296&idx=1&sn=7273271d15bc7e2e41da58a155c6e4ab&chksm=84229506b3551c10f20437b06e0e2fb75c1cb0642d5571ea0b30f534a9000b7bb4f2946a393c
   表1-1　质量评估指标 This is a really nice picture to show how to measure code complexity

__Levels of architecture design__

Software design is complex. To manage the complexity, I break it into different __levels and views__. Typical levels are: architecture level, component level, and class level. The abstraction level goes from high to low, scope from big to small, and uncertainty from fuzzy to clear. Each level yet has its own methodologies. Levels also map to first-and-next steps, which in practice can be simplified or mixed, to lean more to the real world bottleneck. 

  * __Architecture level__ focuses on components and their __interconnections__. Interconnections are abstracted by ports and connectors. A component or connector can hide great complexity and to delay technical decision to lower levels. A component can be a metadata server, a storage pool, or with distributed caching. A connector can be a queue with throttling QoS, REST services, or an event-driven CQRS. System __scope__ is examined, e.g. input and output flows, how to interact with end users, and the up/down stream systems. The infrastructure and technology stack to build atop can be investigated and determined. __Non-functional requirements__, user __scenarios__, and system scenarios are captured and addressed in this level. The typical analysis method is __[4+1 View](https://zhuanlan.zhihu.com/p/112531852)__. When talking about __software architecture__, more are referring on this level. It is also what this article to cover.

  * __Component level__ follows the architecture level. It focuses on the design inside the component. The scope should also be defined, e.g. interface, input and output, execution model and resources needed. This level usually involves tens of classes, __[Design Patterns](https://en.wikipedia.org/wiki/Software_design_pattern#Creational_patterns)__ are the popular methodology, and component should be designed __Reusable__. Architecture can be built on existing systems, where __technical debt__ plays a role, e.g. to rewrite all with a better design (high cost), or to reuse by inserting new code (high coupling). 

  * __Class level__ next focuses on the more fine-grained level, i.e. how to implement one or several classes well. The definitions are clear and ready for coding. Typical methodologies are __[Coding Styles](https://google.github.io/styleguide/cppguide.html)__, __[Code Refactoring](https://m.douban.com/book/subject/1229923/)__, __[Code Complete](https://book.douban.com/subject/1477390/)__ (bad book name). You can also hear about defensive programming, contract based programming. __[UML diagrams](https://en.wikipedia.org/wiki/Unified_Modeling_Language)__ are vastly useful at this level and also component level, as a descriptive tool, and more importantly an analysis tool; e.g. use state machine diagram/table to ensure all possible system conditions are exhausted and cared about. (Similar methods are also shared in [PSP](https://www.geeksforgeeks.org/personal-software-process-psp/), which is a [subset](https://www.isixsigma.com/tools-templates/combining-cmmia-psp-tsp-and-six-sigma-software/) of [CMMI](https://en.wikipedia.org/wiki/Capability_Maturity_Model_Integration); real world today more lean to Agile, while CMMI essentially turns developers into screw nails with heavy documentation and tightly monitored statistics). 

__Views of architecture design__

Views help understand software design from different perspectives. The methodologies covered below act as the descriptive tools for design output, the analysis tools to verify correctness, the heuristic frameworks for mind flow, and the processes to carry out architecture design.

__[4+1 View](https://zhuanlan.zhihu.com/p/112531852)__ is one of the most popular software architecture methods. It captures the static structure, runtime parallelism, physical deployment, and development lifecycle.

  * __Logical View__: The components and their interconnections. The diagram captures what consists of the system and how it functions, the dependencies and scope, and the responsibility decomposition. It's the most commonly mentioned "what architecture is".

  * __Process View__: Logical View is static, while Process View captures the runtime. Performance and scalability are considered. Examples are how multi-node parallelism and multi-threading are organized, how control flow and data flow co-work in timeline.

  * __Deployment View__: E.g. which part of the system runs at datacenter, CDN, cloud, and client device. How should the rollout and upgrade be managed. What are the binary artifacts to deliver.

  * __Implementation View__: Managing the code, repo, modules, DLLs, etc. Logical View components are mapped to concrete code objects, that developers and project manager can readily work on. It also covers the branching policies and how different versions of the product should be maintained.

  * __Usecase View__: Last but the most __important__ view. It captures all user scenarios and system scenarios, functional and non-functional requirements. Each of them are walked through across the previous 4 views to verify truly addressed.

// TODO pic: 4+1 view chart from https://zhuanlan.zhihu.com/p/112531852

__[UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language)__ is the generic software modeling tool, but it can also be understood from the view's perspective.

  * __Structural diagrams__ capture the static view of the system. From higher abstraction level to lower, there are Component diagram, Class diagram, Object diagram, etc.

  * __Behavioral diagrams__ capture the runtime view of the system. E.g. Activity diagram for the logic workflow, sequence diagram for timeline, Communication diagram for multi-object interaction, and the state diagram everyone likes.

  * __Other diagrams__. There are Usecase diagram to capture user scenarios and more fine-grained cases; and deployment view to capture how the code and artifacts are grouped for code development.

[DDD](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) (Domain-Driven Design) views the system from the domain expert perspective. It applies to systems with complex business logic and domain knowledge, e.g. ERP, CRM, or Internet companies with rich business. Compared to traditional OO-design, which easily leads to a spider web of objects ("__Big Ball of Mud__"), DDD introduces "domains" to tide it up. Below lists key concepts:

  * __Domain__. A big complex system (enterprise scale) are cut into multiple domains (e.g. user account system, forum system, ecommerce system, etc), each with their specific domain knowledge, language wording, and domain experts.

  * __Bounded Context__. The boundary of the domain is called the bounded context. The same conceptual object is possible to exist in two different domains, but they map to different classes; e.g. an account in the context of banking is different from an account in book selling. The object __can only interact__ with objects from the same bounded context. And you should not directly operate on getters/setters, instead you use "business workflow calls". (Similarly in OO design, objects should interact with objects __at the same abstraction level__.) A domain's object cannot (directly) go outside of its bounded context. Bounded contexts are orthogonal to each other.

  * __Context Map__. But how two Bounded Contexts interact? A domain's object is mapped to another domain, via the Context Map. The Context Map can be as simple as "new an object" and "assign properties", or as complex as a REST service. __Anti-corruption layer__ (ACL) can be inserted in middle for isolation.

  * __[Drive DDD design by language](https://qiyu2580.gitbooks.io/iddd/content/Chapter2/making-sense-of-bounded-contexts.html)__. Domain knowledge is a language, and knowledge itself is a good design (if you see the philosophy part). However language has its fuzziness nature, that's why __context__ needs to be introduced to bound for certainty. Language is fluent when you organize talking at the same abstraction level; that explains objects should only interact with objects from the same bounded context. DDD is a methodology to __operate language into design__; it expresses domain knowledge __in reusable code__, where domain experts are (or close to) code developers.

  * __Company strategic view__. DDD is able to model company-wide. An executive needs to strategically decide what is core for business competency, what to support it, and what are the common parts. This introduces __[Core domains](https://cloud.tencent.com/developer/article/1709312)__, __Supporting domains__, and __Generic domains__. Priority resources are biased among them. In long term, the domain knowledge, and the DDD model implemented in running code, are accumulated to become valuable __company assets__. The DDD architecture focus on lasting domain modeling, where a good design is __neutral to the technical architecture__ being implemented.

// TODO DDD pic insert: https://qiyu2580.gitbooks.io/iddd/content/Chapter1/how-to-ddd.html. 表1.4 分析"注射流感疫苗"的最佳模型

There are more general architecture views more used for customer facing and sales scenarios. They provide alternative insights for what an architecture should include. 

  * The [Enterprise architecture](https://dev.to/dhruvesh_patel/software-architecture-five-common-design-principles-2il0) consists of Business architecture, Data architecture, Application architecture, Technology architecture. This is more viewed from enterprise business level and does a coarse decomposition 

  * The [四横三纵 architecture](https://mp.weixin.qq.com/s?__biz=MzI4OTc4MzI5OA==&mid=2247544948&idx=6&sn=e89031d33a1b7f753095164b022ae80d) or with more detailed in this [article](https://posts.careerengine.us/p/5f0db6acb5fef84f7de7203d). "四横" are IaaS, DaaS (data as a service), PaaS (platform services) and SaaS. "三纵" are Standard Definition & Documentation (准规范体系), Security Enforcing (安全保障体系), Operation Support & Safety (运维保障体系).

// TODO pic arch from: https://dev.to/dhruvesh_patel/software-architecture-five-common-design-principles-2il0

Besides this section, I also found valuable experiences from [Kenneth Lee's blogs](https://gitee.com/Kenneth-Lee-2012/MySummary/tree/master/%E8%BD%AF%E4%BB%B6%E6%9E%84%E6%9E%B6%E8%AE%BE%E8%AE%A1)/[articles](https://www.zhihu.com/column/kls-software-arch-world)), the remarkable [On Designing and Deploying Internet-Scale Services](https://www.usenix.org/legacy/event/lisa07/tech/full_papers/hamilton/hamilton_html/); and from eBay's [[1]](https://mp.weixin.qq.com/s/bnhXGD7UhwTxL8fpddzAuw)[[2]](https://mp.weixin.qq.com/s/Xyvfx9mLKqquulnrhFi42Q), [Alibaba's](https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzA5OTAyNzQ2OA==&mid=2649721202&idx=1&sn=97b3edaa344a1d901ee6ad4b8c4830e4), or [AWS's](https://mp.weixin.qq.com/s?__biz=MzI4OTc4MzI5OA==&mid=2247520243&idx=1&sn=dfce28433ff14ef188055dc5daf67bd7).


# Common architecture styles

This is the old topic, a generic design pattern on the scale of architecture. New recent technologies bring more paradigms, but the essence can be tracked back. Company-wide the architecture may eventually evolve to reflect the organization's communication structure ([Conway's Law](https://en.wikipedia.org/wiki/Conway%27s_law)), besides the technical aspects. 

  * __Layered architecture__. Now every architecture cannot totally discard this.

  * __Repository/blackboard architecture__. All components are built around the central database (the "Repository/blackboard"). They use pull model or get pushed by updates.

  * __Main program and subroutines__. Typical C-lang program architecture, __procedure-oriented__ programming, and can usually be seen at simple tools. The opposite side is object-oriented programming.

  * __Dataflow architecture__. Still procedure-oriented programming, it can typically be represented by dataflow diagram. The architecture is useful for data processing, especially chips/FPGA, and image processing. __Pipeline and filters__ are another architecture accompanied with.

  * __MVC (Model-view-controller)__. The fundamental architecture to build UI. It separates data, representation, and business logic. It gets richer variants in richer client UI, e.g. React.

  * __Client server__. The style that old fashion client device connects to server. Nowadays it's usually Web, REST API, or SOA instead. But the architecture is still useful in IoT, or as a host agent to report status / receive command to central server, or as a rich client lib to speedup system interactions.

  * __The mediator__. Suppose N components are connecting to M components, instead of N * M connections, a "mediator" component is introduced in middle to turn it to N + M connections.

  * __Event sourcing__. User sends command, and every system change is driven by an event. System stores the chain of events as the central truth. Realtime states can be derived from event replay, and speedup by checkpoints. The system naturally supports auditing, and is append-only and immutable.

  * __Functional programming__. This is more an ideal methodology rather than a concrete architecture. Variables are immutable; system states are instead defined by a chain of function calls. I.e. it's defined by math formula, or a bit like event sourcing. Functions are thus the first-class citizens.

// TODO pic: add charts for each major architecture. this is much easier to understand.

More recent architectures below. You can see architectures vary on: How to cut boundaries, e.g. fine-grain levels, offloading to cloud. Natural structures, e.g. layered, event & streaming, business logic, model-view UI. The gravity of complexity, e.g. complex structures, performance, consistency, managing data, security & auditing, loose communication channels.

  * __Micro-service__. Complex systems are broken into micro-services interacting with REST APIs. Typical examples are __Kubernetes and Service Mesh__. You yet need an even more complex container infrastructure to run micro-services: SDN controller and agents for virtual networking, HA load balancer to distribute traffic, circuit breaker to protect from traffic surge, service registry to manage REST endpoints, Paxos quorum to manage locking and consistent metadata, persistent storage to provide disk volumes and database services, ...

// TODO Add pick about K8S service mesh architecture

  * __Stream processing__. Upstream and downstream systems, across company-wide, are connected via messaging queue, or low latency streaming platforms. Nowadays enterprises are moving from __Lambda architecture__ (realtime approximate streaming and delayed accurate batching are separated) to __[Kappa architecture](https://towardsdatascience.com/a-brief-introduction-to-two-data-processing-architectures-lambda-and-kappa-for-big-data-4f35c28005bb)__ (combine both into streaming, with consistent transaction). A more complex system can comprise [online, nearline, offline](https://netflixtechblog.com/system-architectures-for-personalization-and-recommendation-e081aa94b5d8) parts.

// TODO pic: online,nearline,offline from Netflix chart: https://netflixtechblog.com/system-architectures-for-personalization-and-recommendation-e081aa94b5d8

  * __Cloud native__. The system is designed to run exclusively on cloud infrastructure (but to be hybrid cloud). The typical example is [Snowflake](https://www.usenix.org/conference/nsdi20/presentation/vuppalapati) database. Key designs are: 1) Disk file persistence are offloaded to __S3__. 2) Memory caching, query processing, storage are __disaggregated__ and can independently scaleout and be elastic for traffic surge. 3) Read path and write path can separately scale, where typical users generate write contents in steady throughput and read traffic in spikes. 4) Different tiers of resources, since fully disaggregated, can accurately charge billing for how much a customer actually uses.  __Serverless__ is another topic, where all the heavy parts like database and programming runtime are shifted to cloud. Programmers focus on writing functions to do what business values, lightweighted and elastic to traffic.

// TODO Add pic about Snowflake architecture

  * __DDD onion architecture__. The onion (or call it hexagon) architecture comes to shape in the context of DDD. Domain model is the central part. The next layer outside is applications. The outer layer are adapters that connects to external systems. Onion architecture is neutral to the actual technical architecture being implemented. Domain models can also be connected test cases to easily validate business logic (rather than the verbosity of preparing testbed with fake data in databases, fake REST interfaces, etc).

// TODO Add pic about DDD onion the classic architecture

  * __[React-Redux](https://medium.com/mofed/react-redux-architecture-overview-7b3e52004b6e)__. The architecture is a more advanced version of MVC. With data pulled from server-side, Javascripts at client-side runs MVC itself. Views are constructed by templates + input properties. User actions generate events, which trigger actions, e.g. call services. New updates are sent to reducer, which then map to store. Container uses selectors to fetch states from store, map them to properties, and then finally render the new view. The architecture is also frequently accompanied with Electron and NodeJS to develop rich client Apps with web technologies.

// TODO Add pic Reach-Redux architecture the workflow loop chart, which should find from the official site


# General architecture principles

Most principles are already reflected in the above sections. At __architecture level__, the most mentioned principles are below [three](https://xie.infoq.cn/article/5e899856e29017c1079b3be86)

  * __Keep it simple__. There are enough complexity; simple is precious. Related to [KISS](https://en.wikipedia.org/wiki/KISS_principle).

  * __Suitable__. Enough for the need, is better than "industrial leading". An architecture should be suitable, to steer it with your concrete requirement and team resources, rather than to vainly pursuit new technologies. Be frugal. The benefit of a design should be mapped to financial cost to evaluate.

  * __Designed for evolving__. Business needs are changing. Traffic scale are increasing. Team members may come and go. Technologies are updating. An architecture should be designed evolvable. The architecture process (and development) should be carried out with a [growth mindset](https://www.youtube.com/watch?v=M1CHPnZfFmU). An example is [Ele.me Payment System](https://mp.weixin.qq.com/s/mtPQLSONUCWOC2HDPRwXNQ), which is quite common for Internet companies.

More principles come to __component level__ design. [CoolShell has a very good post](https://coolshell.cn/articles/4535.html) to list all of them. Below lists what I think are useful

  * __Keep It Simple__, Stupid (KISS), You Ain't Gonna Need It (YAGNI), Don't Repeat Yourself (DRY), Principle of Least Knowledge, Separation of Concerns (SoC): That said, make everything simple. If you cannot, divide and conquer.

  * Object-oriented __S.O.L.I.D__. Single Responsibility Principle (SRP), Open/Closed Principle (OCP), Liskov substitution principle (LSP), Interface Segregation Principle (ISP), Dependency Inversion Principle (DIP). Note that though OO principles try to isolate concerns and make changes local, refactoring and maintaining the system in well such state however involves global knowledge of global dependency.

  * __Idempotent__. Not only API, the system operation should be idempotent when replayed, or reentrantable. A distributed system can commonly lost message and do retry. Idempotent examples can be doing sync (rather than update, sync a command to node, which is consistent after node fail-recovers and re-executes); propagating info in __eventual consistency and in one direction__; re-executing actions without side effect; __goal states__ commonly used in deployment and config change. 

  * __Orthogonality__. Component behavior is totally isolated from each other. They don't assume any hidden behaviors from another. They work, no matter what others output. Not only the code path, also the development process can be orthogonal, with a wise cut of components. Orthogonality greatly saves the mind burden, communication cost, and ripple impact of changes.

  * __Hollywood Principle__, don't call us, we'll call you. Component doesn't `new` components. It's however the Container who manages Component creation and initialization. It's inversion of control, or dependency injection. Examples are [Spring DOI](https://www.baeldung.com/spring-dependency-injection), [AspectJ AOP](https://docs.spring.io/spring-framework/docs/4.3.15.RELEASE/spring-framework-reference/html/aop.html). Dependency should be towards the more stable direction.

  * __Convention over Configuration（CoC)__. Properly set default values, save the caller's effort to always pass in comprehensive configurations. This principle is useful to design opensource libs, e.g. Rails. However, large scale production services may require explicit and tight control on configuration, and the ability to dynamic change. [Microsoft SDP](https://azure.microsoft.com/en-us/blog/advancing-safe-deployment-practices/) is an example. 

  * __Design by Contract (DbC)__. A component / class should work by its "naming", i.e. contract, rather than implementation. A caller should call a component by its "naming", instead of the effort to look into its internals. The principle maps to objects should work objects at the same abstraction level, and to respect responsibilities.

  * __Acyclic Dependencies Principle (ADP)__. Try not to create a cyclic dependency in your components. Ideally, yes. In fact, cyclic dependency still happens, when multiple sub-systems are broker-ed by a message queue. Essentially, components need interaction, just like people.  

Coming to __class level__ or lower component level, the principles can be found from __[Coding Styles](https://google.github.io/styleguide/cppguide.html)__, __[Code Refactoring](https://m.douban.com/book/subject/1229923/)__, __[Code Complete](https://book.douban.com/subject/1477390/)__; this article won't cover.  However, it's interesting to evaluate if a piece of code is __good design__, which people frequently argue for long time without an agreement. In fact, several distinct design philosophies all apply, which can be found from diverged opensource codebases and programming language designs. To end the arguing, practical principles are

  * Compare __concrete benefits/costs__ to team and daily work, rather than design philosophies.

  * Build the compare on __concrete real usecases__, rather than blindly forecasting future for design extensibility.

__About OO design and Simple & direct__

Continued from the above discussion about evaluating a piece of code is good design. The key concern should be whether it __saves mind burden__ across team. There are generally two paradigms: OO design and Simple & direct. They work in different ways.

  * __OO design__ reduces __mind burden__ because good OO design metaphors (e.g. patterns) are __shared language__ across team. The principle fails if they are actually __not shared__, which should be verified. E.g. one person's natural modeling may not be another person's. What code one person feels natural, can become another person's mind burden. One top team guy can quickly generate code in her natural OO design, but the new code becomes mind burden for others, and slows them down. The condition __self-enhances__ and makes the "top" guy topper.  __Consistency__ can be desired, because it extends what's shared to share.

  * __OO design__ does __increase complexity__. It introduces more parts from beginning. More interactions becomes __hidden and dynamic__. A change can rafactor more parts to maintain high cohesion low coupling.  Things become worse for __performance considerations__. Decoupling generally hurts performance; it thus needs to introduce more parts to compensate, e.g. caching. More moving parts touched, yet larger scope to maintain for production safety and correctness.  __Over-design__ is the next problem behind. OO design essentially works by __forecasting future__ to make changes extensible. However, the forecasting can be frequently wrong, and extra code yet becomes new burden. 

  * __Simple & direct__. Compared to OO design which frequently applies to App level programming, "simple and direct" is more used in system level and data plane programming. The __interfaces__ supported in programming languages, which are the core that OO design relies on, are frequently not capable to capture all information to pass. Examples are performance aspects (cache line, extra calls, memory management, etc), handling worst cases, safety & security concerns, fragile side effects that touch system data structure (if you are programming OS), etc.

  * Thus in __simple & direct__ paradigm, people frequently need to __read over all code__ in a workflow, grasp every detail, to make sure it can work correctly. People also need to read over the code to make sure each corner cases is handled, all scenarios are covered, and worst case and graceful degradation is cared.  Then, __less code less burden__ to people, everything __simple direct transparent__ is better. __Mind burden__ is reduced this way.  However, __OO design__ is making it harder, because subtle aspects to capture are hidden in layers of encapsulation, and linked in dynamic binding, and there are yet more code and more components to introduce.

  * What's the __gravity and traction__ of the project being developed? Apps with rich and varying logic are willing to adopt OO design. While system level and data plane usually have more stable interfaces and feature sets, but having more traction to performance and safety. Sometime the developer is willing to break every OO rule as long as COGS can be saved. Besides, encapsulation hinders developers from having __control__ on the overall perf numbers and calls.

  * __Prioritization__. Can the new code go production? Perf under goal, no. Production safty concerns, no. Bad OO design, OK. Thus, the design should first consider perf and safty, and then OO design. However, OO design naturally prioritizes design first, and __pushes off__ goals like performance, worst case handling, to future extension. Besides the priority inversion, extension may turn out hard after the interface is already running on production.


# Technology design spaces, architecture design patterns, and system properties

Software architecture has common __system properties__, e.g. [CAP](https://www.educative.io/blog/what-is-cap-theorem). To achieve them, different techniques are invented and evolve into more general __architecture design patterns__. Plotting them on the map of various driving factors, they reveal the landscape of __technology design space__, that we explore and navigate for building new systems. I'll focus on __distributed storage__. 

## Sources to learn from

Articles, books, and courses teach design patterns and outlines the design spaces

  * MartinFowler site [Patterns of Distributed Systems](https://martinfowler.com/articles/patterns-of-distributed-systems/). With the adoption of cloud, patterns like [Consistent Core](https://martinfowler.com/articles/patterns-of-distributed-systems/consistent-core.html) and [Replicated Log](https://martinfowler.com/articles/patterns-of-distributed-systems/replicated-log.html) are gaining popularity. Besides this article, Service Registry, Sidecar, Circuit Breaker, Share Nothing are also popular patterns.

  * [Cloud Design Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/) from Azure Doc also summarizes common cloud native App design patterns. They are explained in detail, and fill the missing ones from above.

  * Book [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) shows the challenges, solutions and techniques in distributed systems. They map to design patterns and combine into design space.

  * Courses [CMU 15-721](https://15721.courses.cs.cmu.edu/spring2020/schedule.html) outlines key components in database design, e.g. MVCC, data compression, query scheduling, join. The breakdown reveals the design space to explore. The attached papers future tours established design patterns in depth. Highly valuable.

  * [On Designing and Deploying Internet-Scale Services](https://www.usenix.org/legacy/event/lisa07/tech/full_papers/hamilton/hamilton_html/index.html). The article is comprehensive, in-depth, and covers every aspect of best practices for building Internet scale services. Highly valuable. It reminds me of [SteveY's](https://coolshell.cn/articles/5701.html)

Recognized opensource and industry systems become the Reference architectures, which to learn prevalent techniques or design patterns. I listed what I recall quickly (can be __incomplete__). Reference architectures can be found by searching top products, comparing vendor alternatives, or from cornerstone papers with high reference.

  * Due to the lengthy content, I list them in the next section [Reference architectures in storage areas](.).

Related works section in generous papers are useful to compare contemporary works and reveal the design space. For example,

  *  [TiDB](http://www.vldb.org/pvldb/vol13/p3072-huang.pdf) paper and [Greenplum](https://arxiv.org/pdf/2103.11080.pdf) paper related works show how competing market products support HTAP (Hybrid Transactional and Analytical Processing) from either prior OLTP or OLAP. They also reveal the techniques employed and the Pros/Cons.

Good papers and surveys can enlighten the technology landscape and reveal design space in remarkable depth and breadth

  * [LSM-based Storage Techniques: A Survey](https://arxiv.org/abs/1812.07527) ([Zhihu](https://zhuanlan.zhihu.com/p/351241814)) investigated full bibliography of techniques used to optimize LSM-trees, and organized the very useful taxonomy.

![LSM-based Storage Techniques: A Survey](/images/arch-design-space-lsm-survey.png "LSM-based Storage Techniques: A Survey")

  * [Scaling Replicated State Machines with Compartmentalization](https://arxiv.org/abs/2012.15762) shows a group of techniques to decouple Paxos components and optimize the throughput.

![Scaling Replicated State Machines with Compartmentalization](/images/arch-design-space-paxos-compartment.png "Scaling Replicated State Machines with Compartmentalization")

  * [An Empirical Evaluation of In-Memory Multi-Version Concurrency Control](http://www.vldb.org/pvldb/vol10/p781-Wu.pdf) compared how main-stream databases implement MVCC with varieties, extracted the common MVCC components, and discussed main techniques. It's also useful guide to understand MVCC.  

![An Empirical Evaluation of In-Memory Multi-Version Concurrency Control](/images/arch-design-space-in-mem-mvcc.png "An Empirical Evaluation of In-Memory Multi-Version Concurrency Control")

  * [In-Memory Big Data Management and Processing](https://www.comp.nus.edu.sg/~ooibc/TKDE-2015-inmemory.pdf) surveyed how main-stream in-memory databases and designed, compared their key techniques, that form the design space.

![In-Memory Big Data Management and Processing](/images/arch-design-space-in-mem-db.png "In-Memory Big Data Management and Processing")

  * [Constructing and Analyzing the LSM Compaction Design Space](http://vldb.org/pvldb/vol14/p2216-sarkar.pdf) compared different compaction strategies in LSM-tree based storage engines. THere are more fine-grained tables inside the paper. 

![Constructing and Analyzing the LSM Compaction Design Space](/images/arch-design-space-lsm-compaction.png "Constructing and Analyzing the LSM Compaction Design Space")

  * Another [Dostoevsky: Better Space-Time Trade-Offs for LSM-Tree](https://www.youtube.com/watch?v=fmXgXripmh0) also plots the design space for space-time trade-offs among updates, point lookups, range lookups.

![Dostoevsky: Better Space-Time Trade-Offs for LSM-Tree](/images/arch-design-space-dostoevsky.png "Dostoevsky: Better Space-Time Trade-Offs for LSM-Tree")
  
  * [Latch-free Synchronization in Database Systems](http://www.jmfaleiro.com/pubs/latch-free-cidr2017.pdf) compared common lock/lock-free techniques, e.g. CAS, TATAS, xchgq, pthread, MCS, against different concurrency levels. It reveals the choice space while implementing effective B+-tree locking techniques.

  * [Optimal Column Layout for Hybrid Workloads](https://stratos.seas.harvard.edu/files/stratos/files/caspervldb2020.pdf) models CRUD, point/range query, random/sequential read/write cost functions on how blocks are partitioned by partition size. It helps find the optimal block physical layout. 

  * [Access Path Selection in Main-Memory Optimized Data Systems](https://www.eecs.harvard.edu/~kester/files/accesspathselection.pdf) models query cost using full scan vs B+-tree at different result selectivity and query sharing concurrency. The cost model shows how query optimizer choose physical plans.

## Reference architectures in storage areas

(Continued from the previous section.)

__Cache__

  * [Redis](https://redis.io/) is the opensource de-factor in-memory cache used in most Internet companies. Compared to Memcached, it supports rich data structures. It adds checkpoint and per operation logging for durability. Data can be shared to a cluster of primary nodes, then replicated to secondary nodes. [Tendis](https://cloud.tencent.com/developer/article/1815554) further improves cold tiering, and optimizations.

  * [Kangaroo cache](https://www.pdl.cmu.edu/PDL-FTP/NVM/McAllister-SOSP21.pdf) (from long thread of Facebook work on [Memcached](https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala), [CacheLib](https://www.usenix.org/conference/osdi20/presentation/berg), and [RAMP-TAO cache consistency](https://www.vldb.org/pvldb/vol14/p3014-cheng.pdf)) features in in-memory cache with cold tier to flash. Big objects, small objects are separated. Small objects combines append-only logging and set-associative caching to achieve the optimal DRAM index size vs write amplification. Kangaroo also uses "partitioned index" to further reduce KLog's memory index size.

  * [BCache](https://bcache.evilpiepirate.org/BcacheGuide/) is a popular SSD block cache used in [Ceph](https://segmentfault.com/a/1190000038448569). Data is allocated in "extents" (like filesystem), and then organized to bigger buckets. Extent is the unit of compression. A bucket is sequentially appended to full and is the unit of GC reclaim. Values are indexed by B+-tree (unlike KLog in Kangaroo using hashtables). The B+-tree uses large 256KB nodes. Node internal is modified by appending log structured. B+-tree structural change is done by COW and may recursively rewrite every node up to the root. Journaling is not a necessity because of COW, but used as an optimization to batch and sequentialize small updates.

__(Distributed) Filesystem__

  * [BtrFS](https://dominoweb.draco.res.ibm.com/reports/rj10501.pdf) for Linux single node filesystem. It indexes inodes with B-tree, updates with copy-on-write (COW), ensures atomicity with shadow paging. Other contemporaries include [XFS](http://www.scs.stanford.edu/nyu/03sp/sched/sgixfs.pdf), which also indexes by B-tree buts updates with overwrite; and [EXT4](https://ext4.wiki.kernel.org/index.php/Ext4_Disk_Layout), which is the default Linux filesystem that directory inode is a tree index to file inodes, and employs write-ahead journaling (WAL) to ensure update (overwrite) atomicity.

  * [CephFS](https://docs.ceph.com/en/pacific/cephfs/index.html) introduces MDS to serve filesystem metadata, i.e. directories, inodes, caches; while persistence is backed by object storage data pool and metadata pool. It features in [dynamic subtree partitioning](https://ceph.io/assets/pdfs/weil-mds-sc04.pdf) and [Mantle load balancing](https://engineering.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-15-10.pdf). Cross-partition transaction is done by [MDS journaling](https://docs.ceph.com/en/pacific/cephfs/mds-journaling/) to the object store. MDS acquires [locks](https://docs.ceph.com/en/pacific/cephfs/mdcache/#distributed-locks-in-an-mds-cluster) before update.

  * [HopsFS](https://www.usenix.org/conference/fast17/technical-sessions/presentation/niazi) builds distributed filesystem on HDFS. Namenode becomes a quorum, stateless where metadata is offloaded to another in-memory NewSQL database. Inodes are organized into entity-relation table, and partitioned to reduce servers touched by an operation. Cross-partition transaction, e.g. rename, rmdir, are backed by the NewSQL database, with hierarchical locking. Subtree operations are optimized to run parallel.

  * [HDFS](https://storageconference.us/2010/Papers/MSST/Shvachko.pdf) is the distributed filesystem for big data. It relaxes POSIX protocol, favors large files, and runs primary/back Namenode to serialize transactions. HDFS was initially the opensource version of [Google Filesystem](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf) (which started the cloud age with [Big Table](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf), [Chubby](https://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf)), then went so successful, that becomes the de-facto shared protocol for big data filesystems, [databases](https://hbase.apache.org/), [SQL](https://hive.apache.org/), [stream processing](https://databricks.com/blog/2014/01/21/spark-and-hadoop.html), [datalakes](https://hudi.apache.org/docs/comparison/) for both opensource and [commercial](http://doc.isilon.com/onefs/hdfs/02-ifs-c-hdfs-conceptual-topics.htm) products.

__Object/Block Storage__

  * [Ceph](https://www.ssrc.ucsc.edu/pub/weil-osdi06.html) for distributed block storage and object storage (and CephFS for distributed filesystem). Ceph made opensource scaleout storage possible, and [dominated](https://ubuntu.com/blog/openstack-storage) in OpenStack ecosystem. It features in CRUSH map to save metadata by hash-based placement. It converges all object/block/file serving in one system. Node metadata is managed by a Paxos quorum (Consistent Core) to achieve all CAP. Ceph stripes objects and update in-place, which yet introduced single node transaction. Ceph later built [BlueStore](https://mp.weixin.qq.com/s/dT4mr5iKnQi9-NEvGhI7Pg) that [customized](https://www.pdl.cmu.edu/PDL-FTP/Storage/ceph-exp-sosp19.pdf) filesystem, optimized for SSD, and solved the [double-write problem](http://accelazh.github.io/ceph/Ceph-Blue-Store-And-Double-Write-Issues). The double-write issues is solved by separating metadata (delegated to RocksDB), and key/value data (like [Wisckey](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf)); and big writes become append-only, small overwrites are merged to WAL (write-ahead logging).

  * [Azure Storage](https://azure.microsoft.com/en-us/blog/sosp-paper-windows-azure-storage-a-highly-available-cloud-storage-service-with-strong-consistency/) for industry level public cloud storage infrastructure. It is built on Stream layer, which a distributed append-only filesystem; and uses Table layer, which implements scaleout table schema, to support VM disk pages, object storage, message queue. Append-only simplifies update management but gets more challenge in Garbage Collection (GC). The contemporary [AWS S3](https://stackoverflow.com/questions/564223/amazon-s3-architecture) seems instead follows Dynamo, that is update in-place and shards by consistent hashing. For converging object/block/file converged, [Nutanix](https://www.nutanix.com/hyperconverged-infrastructure) shares similar thought to run storage and VM on one node (unlike remotely attached SAN/NAS).

  * [Tectonic](https://www.usenix.org/conference/fast21/presentation/pan) is similar with Azure Storage. It hash partitions metadata to scaleout. It employs [Copyset Placement](http://www.stanford.edu/~skatti/pubs/usenix13-copysets.pdf). It consolidates Facebook Haystack/F4 (Object storage) and Data Warehouse, and introduced much multitenancy and resource throttling. Another feature of Tectonic is to decouple common background jobs, e.g. data repair, migration, GC, node health, from metadata store, into background services. [TiDB](https://docs.pingcap.com/tidb/dev/tidb-architecture) shares similar thought if would have moved Placement Driver out of metadata server.

  * [XtremIO](https://www.youtube.com/watch?v=lIIwbd5J7bE) to build full-flash block storage array with an innovative content-based addressing. The data placement is decided by content hash, thus deduplication is naturally supported. Though accesses are randomized, they run on flash. Write is acked after two copies in memory. Other contemporaries include [SolidFire](https://www.youtube.com/watch?v=AeaGCeJfNBg), which is also scaleout; and [Pure Storage](https://www.purestorage.com/products.html), which is scale-up and uses a dual-controller sharing disks.

__Data deduplication__

  * [Data Domain](https://www.usenix.org/legacy/events/fast08/tech/full_papers/zhu/zhu.pdf) builds one of the most famous data deduplication appliance. It recognizes middle-file inserts by [rolling hash](https://www.gluster.org/deduplication-part-1-rabin-karp-for-variable-chunking/) variable-length chunking. Fingerprint caching is made efficient via Locality Preserved Caching, which works perfectly with backup workload.

  * [Ceph dedup](https://ceph.io/assets/pdfs/ICDCS_2018_mwoh.pdf) builds the scalable dedup engine on Ceph. Ceph stores deduplicated chunks, keyed by hash fingerprint. A new metadata pool is introduced to look object id to chunk map. Dedup process is offline with throttling. The two level indirection pattern can also be used to implement merging small files to large chunk. 

__Archival storage__

  * [Pelican](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-balakrishnan.pdf) is the rack-scale archival storage (or called cold storage, near-line storage), co-designed with hardware, to reduce disk/cpu/cooling power by only 8% of total disks are spinning. Data is erasure coded and stripped across disk groups. [Flamingo](https://www.usenix.org/node/194437) continues research from Pelican. It generates best data layout and IO scheduler config per Pelican environment setup. Archival storage gains adoption from government compliance needs, and with [AWS Glacier](https://aws.amazon.com/s3/storage-classes/glacier/).

  * [Pergamum](https://www.usenix.org/legacy/event/fast08/tech/full_papers/storer/storer_html/) co-designs hardware, as an appliance, to keep 95% disks power-off all time. NVRAM is added per node, holding signatures and metadata, to allow verification without wake up disk. Data is erasure coded intra and inter disks.  Note [Tape Library](https://www.snia.org/sites/default/orig/DSI2015/presentations/ColdStorage/OasamuShimizu_Tape_storage_for_cold_data_archive.pdf) is still attractive archival storage media due to improvement on cost per capacity, reliability, and throughput. 

__OLTP/OLAP database__

  * [CockroachDB](https://dl.acm.org/doi/pdf/10.1145/3318464.3386134) builds the cross-regional SQL database that enables serializable ACID, an opensource version of [Google Spanner](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf). It overcomes TrueTime dependency by instead use [Hybrid-Logical Clock](https://www.cockroachlabs.com/docs/stable/architecture/transaction-layer.html) (HLC). It maps SQL schema to key-value and stores in [RocksDB](https://www.cockroachlabs.com/blog/cockroachdb-on-rocksd/). It uses [Raft](https://www.cockroachlabs.com/docs/stable/architecture/replication-layer.html#raft) to replicate partition data. It built novel [Write Pipelining](https://www.cockroachlabs.com/blog/transaction-pipelining/) and [Parallel Commit](https://www.cockroachlabs.com/blog/parallel-commits/) to speedup transactions. Another contemporary is [YugabyteDB](https://blog.yugabyte.com/ysql-architecture-implementing-distributed-postgresql-in-yugabyte-db/), which reuses PostgreSQL for query layer and replaced RocksDB with DocDB, and [had](https://blog.yugabyte.com/yugabytedb-vs-cockroachdb-bringing-truth-to-performance-benchmark-claims-part-2/) an interesting [debate](https://www.zhihu.com/question/449949351) with [CockroachDB](https://www.cockroachlabs.com/blog/unpacking-competitive-benchmarks/).

  * [TiDB](https://www.vldb.org/pvldb/vol13/p3072-huang.pdf) is similar with CockroachDB. It focus on single region and serializes with timestamp oracle server. It implements transaction following [Percolator](https://github.com/pingcap/tla-plus/blob/master/Percolator/Percolator.tla). TiDB moved a step further to combine OLTP/OLAP (i.e. HTAP) by Raft replicating an extra columnar replica ([TiFlash](https://docs.pingcap.com/zh/tidb/dev/tiflash-overview)) from the baseline row format data. In [contemporaries](https://arxiv.org/pdf/2103.11080) to support both OLTP/OLAP, besides HyPer/MemSQL/Greenplum, Oracle Exadata (OLTP) improves OLAP performance by introducing NVMe flash, RDMA, and added in-memory columnar cache; AWS Aurora (OLTP) offloads OLAP to parallel processing on cloud; [F1 Lightning](http://www.vldb.org/pvldb/vol13/p3313-yang.pdf) replicas data from OLTP database (Spanner, F1 DB) and converts them into columnar format for OLAP, with snapshot consistency.

  * [OceanBase](https://zhuanlan.zhihu.com/p/93721603) is a distributed SQL database, MySQL-compatible, and supports both OLTP/OLAP with [hybrid row-column data layout](https://dbdb.io/db/oceanbase). It uses a central controller (Paxos replicated) to serialize distributed transaction. The contemporary [X-Engine](https://www.cs.utah.edu/~lifeifei/papers/sigmod-xengine.pdf) is an MySQL-compatible LSM-tree storage engine, used by [PolarDB](https://www.usenix.org/conference/fast20/presentation/cao-wei). X-Engine uses FPGA to do compaction. Read/write paths are separated to tackle with traffic surge. X-Engine also introduced Multi-staged Pipeline where tasks are broken small, executed async, and pipelined, which resembles [SeaStar](https://www.scylladb.com/2016/03/18/generalist-engineer-cassandra-performance/). PolarDB features in pushing down queries to Smart SSD ([an example](https://cacm.acm.org/magazines/2019/6/237002-programmable-solid-state-storage-in-future-cloud-datacenters/fulltext)) which computes within disk box to reduce filter output. Later [PolarDB Serverless](http://www.cs.utah.edu/~lifeifei/papers/polardbserverless-sigmod21.pdf) moved to disaggregated cloud native architecture like Snowflake. 

  * [AnalyticDB](http://www.vldb.org/pvldb/vol12/p2059-zhan.pdf) is Alibaba's OLAP database. It stores data on shared [Pangu](https://www.alibabacloud.com/blog/pangu%E2%80%94the-highperformance-distributed-file-system-by-alibaba-cloud_594059) (HDFS++), and schedules jobs via [Fuxi](http://www.vldb.org/pvldb/vol7/p1393-zhang.pdf) ([YARN](https://www.cnblogs.com/liangzilx/p/14837562.html)++). Data is organized in hybrid row-column data layout (columnar in row groups). Write nodes and read nodes are separated to scale independently. Updates are first appended as incremental delta, and then merged and build index on all columns off the write path. The baseline + incremental resembles [Lambda architecture](https://www.cnblogs.com/listenfwind/p/13221236.html).

  * [ClickHouse](https://clickhouse.com/docs/en/development/architecture/) is a recent OLAP database quickly gaining popularity known as "[very fast](https://clickhouse.tech/docs/en/faq/general/why-clickhouse-is-so-fast/)". Besides common columnar format, vectorized query execution, data compression, ClickHouse made fast by "attention to low-level details". ClickHouse supports various indexes (besides full scan). It absorbs updates via [MergeTree](https://developer.aliyun.com/article/762092) (similar to LSM-tree). It doesn't support transaction due to OLAP scenario.

  * [AWS Redshift](https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf) is the new generation cloud native data warehouse based on PostgreSQL. Data is persisted at S3, while cached at local SSD (which is like Snowflake). Query processing nodes are accelerated by AWS Nitro ASIC. It is equipped with modern DB features like code generation and vectorized SIMD scan, external compilation cache, AZ64 encoding, [Serial Safe Net](https://arxiv.org/pdf/1605.04292.pdf) (SSN) transaction MVCC, Machine Learning backed auto tuning, semi-structure query, and federated query to datalake and OLTP systems, etc.

  * [Log is database](https://zhuanlan.zhihu.com/p/33603518) [[2]](https://zhuanlan.zhihu.com/p/338582762)[[3]](https://zhuanlan.zhihu.com/p/151086982). The philosophy was first seen on [AWS Aurora Multi-master](https://www.allthingsdistributed.com/2019/03/Amazon-Aurora-design-cloud-native-relational-database.html). Logs are replicated as the single source of truth, rather than sync pages. Page server is treated a cache that replays logs. In parallel, [CORFU](https://blog.acolyer.org/2017/05/02/corfu-a-distributed-shared-log/), [Delos](https://www.usenix.org/system/files/osdi20-balakrishnan.pdf) builds the distributed shared log as a service. [Helios Indexing](http://www.vldb.org/pvldb/vol13/p3231-potharaju.pdf), [FoundationDB](https://www.foundationdb.org/files/fdb-paper.pdf), [HyderDB](http://www.cs.cornell.edu/~blding/pub/hyder_sigmod_2015.pdf) build database atop shared logging.

__In-memory database__

  * [HyPer](https://hyper-db.de/) in-memory database has many recognized publications. It pioneers [vectorized query execution](https://www.vldb.org/pvldb/vol11/p2209-kersten.pdf) with code generation, where [LLVM](https://stackoverflow.com/questions/2354725/what-exactly-is-llvm) is commonly used to compile IR (intermediate representation); and features in [Morsel-driven execution scheduling](https://db.in.tum.de/~leis/papers/morsels.pdf), `fork()` to create OLAP snapshot from OLTP, and many other aspects. Other contemporaries include [SAP HANA](http://sites.computer.org/debull/A12mar/hana.pdf), which combines both OLTP/OLAP (with delta structure) and supports rich analytics; [MemSQL](https://www.singlestore.com/blog/revolution/), which supports OLTP/OLAP by adding both row/columnar format; and [GreenPlum](https://arxiv.org/pdf/2103.11080), which extended PostgreSQL to MPP, added GemFire (used by [12306.cn](https://blog.csdn.net/u014756827/article/details/102610104)) for in-memory processing, and added OLTP after OLAP with performance improvement and resource isolation.

  * [Hekaton](https://www.microsoft.com/en-us/research/publication/hekaton-sql-servers-memory-optimized-oltp-engine/) is the in-memory DB engine for Microsoft SQL Server. It features in the lock-free [Bw-Tree](https://www.cs.cmu.edu/~huanche1/publications/open_bwtree.pdf), which works by append deltas and merge. Bw-tree needs a [Page Mapping Table](https://www.microsoft.com/en-us/research/publication/the-bw-tree-a-b-tree-for-new-hardware/) ([LLAMA](https://db.disi.unitn.eu//pages/VLDBProgram/pdf/research/p853-levandoski.pdf)) for atomic page update, and avoid propagating page id change to parent nodes. Bw-tree's SSD component can also be append-only, with "Blind Incremental Update" in [DocumentDB](https://www.vldb.org/pvldb/vol8/p1668-shukla.pdf). Hekaton also has [Project Siberia](http://www.vldb.org/pvldb/vol6/p1714-kossmann.pdf) to tier cold data, which uses adaptive filters to tell whether data exists on cold disk, and cold classification is done [offline](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p1016-eldawy.pdf) on logged sampled record accesses.

  * [ART tree](https://db.in.tum.de/~leis/papers/ART.pdf) is one of the popular index (e.g. HyPer) for in-memory databases (and also PMEM). It's essentially a radix tree with adaptive node sizes. Other contemporaries include [Masstree](https://pdos.csail.mit.edu/papers/masstree:eurosys12.pdf), which is a trie of B+trees and collective optimizing techniques; [Bw-tree](https://www.microsoft.com/en-us/research/publication/the-bw-tree-a-b-tree-for-new-hardware/); and [Be-tree](https://www.usenix.org/conference/fast15/technical-sessions/presentation/jannen), which uses per node buffer to absorb random updates, and adopted in [VMWare copy files](https://www.usenix.org/conference/fast20/presentation/zhan). For filtering, besides commonly used [BloomFilter](http://oserror.com/backend/bloomfilter/), [SuRF](https://db.cs.cmu.edu/papers/2018/mod601-zhangA-hm.pdf) additionally supports range query but with high update cost.

  * [FaRM](https://www.microsoft.com/en-us/research/project/farm/) builds scaleout in-memory database with fast serializable transactions on RDMA and UPS protected PMEM. CPU bottleneck is overcome by reducing message count, one-sided RDMA reads/writes, and exploiting parallelism. Data is sharded. Distributed transaction is implemented with 2PC; lock is persisted in logs of primary nodes of each partition; read is lock-free; coordinator has no persistent state. Zookeeper is used to maintain node membership. Objects are accessed via keys (pointer address). Following work [A1](https://arxiv.org/abs/2004.05712) builds graph database atop FaRM, and handles RDMA congestion with [DCQCN](https://blog.csdn.net/hithj_cainiao/article/details/117292144).

  * [Silo](https://wzheng.github.io/silo.pdf) builds OCC serializable transaction commit protocol by epoch-based group commit, indexed by Masstree. [Manycore](https://taesoo.kim/pubs/2016/min:fxmark.pdf) (40+ CPU cores) significantly changes concurrency design in HPC, in-memory, PMEM systems; e.g. Linux [Kernel](https://pdos.csail.mit.edu/papers/linux:osdi10.pdf) and [Filesystems](https://taesoo.kim/pubs/2016/min:fxmark-slides.pdf). Besides custom latching & fencing, techniques are frequently used such as [Epoch-based Reclamation](https://aturon.github.io/blog/2015/08/27/epoch/#epoch-based-reclamation) (e.g. in Masstree), [Sloppy Counter](https://pdos.csail.mit.edu/papers/linux:osdi10.pdf), [Flat Combining](https://www.cs.bgu.ac.il/~hendlerd/papers/flat-combining.pdf), Share Nothing. Epoch-based Reclamation groups frequent memory operations into larger infrequent epochs; threads work on local memory, except the GC one touches all after epoch inactive. [RCU](http://www.jmfaleiro.com/pubs/latch-free-cidr2017.pdf) is similar, that after all transaction passed low-watermark epoch, older DB record versions can be reclaimed. Sloppy Counter splits reference counting to a global counter and per-core counters, where most operation happens at thread-local. In Flat Combining, worker threads publish requests to thread-local, then compete for a global CAS (compare-and-set), and the only winner batches and executes all requests. Shared Nothing is the silver bullet for high concurrency, as long as the system can be designed this way ([comprehensive example](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/curtis-maury)).

__NoSQL database__

  * [RocksDB](http://rocksdb.org/) is the de-factor LSM-tree implementation of single node key-value store. It is commonly used as the KV backend for [many](https://en.wikipedia.org/wiki/RocksDB) systems, e.g. [MySQL](https://vldb.org/pvldb/vol13/p3217-matsunobu.pdf), [CockroachDB](https://www.cockroachlabs.com/blog/cockroachdb-on-rocksd/), [TiDB](https://docs.pingcap.com/tidb/dev/rocksdb-overview/), [BlueStore](http://www.yangguanjun.com/2018/10/25/ceph-bluestore-rocksdb-analyse/). It is also frequently [used](http://rocksdb.org/docs/support/faq.html) at Internet companies. RocksDB features in [Universal Compaction](https://github.com/facebook/rocksdb/wiki/Universal-Compaction), SSD optimization, and [Remote Compaction](https://zhuanlan.zhihu.com/p/419766888) (offload compaction to cloud based on shared storage). In tiering approach, [PebblesDB](https://www.cs.utexas.edu/~vijay/papers/pebblesdb-sosp17-slides.pdf) inserts increasingly more ["Guards"](https://vigourtyy-zhg.blog.csdn.net/article/details/109005795) in each LSM-tree level, which works like a skip list to constraint and index SST files key ranges, thus to reduce read amplification. 

  * [FoundationDB](https://www.foundationdb.org/files/fdb-paper.pdf) to support ACID transaction in distributed KV store. The transaction implementation is backed by the shared logging system. Control Plane, Transaction, Shared Logging, Storage Systems are decoupled. FoundationDB also builds fast recovery leveraging the shared log. Besides, FoundationDB features in Deterministic Simulation Testing built by Flow.

  * [MongoDB](https://engineering.mongodb.com/papers) is the de-facto JSON document database, one of the most successful opensource databases and went [IPO](https://www.cnbc.com/2017/10/19/mongodb-mdb-ipo-stock-price-on-first-trading-day.html). MongoDB went popular because of ease to use. It scales out by sharding (range/hash partitioning) and HA (high availability) by replica set (1 write + N read replicas).

  * [HBase](https://segmentfault.com/a/1190000019959411) is the opensource version of [Big Table](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf). Table is range partitioned and metadata managed by [ZooKeeper](https://mikechen.cc/4657.html) (opensource version of Chubby, or Paxos + [Replicated State Machine](https://www.youtube.com/watch?v=TWp6H7mb09A) + Namespace indexing). Partition server employs LSM-tree to manage updates, with common parts like MemTable, HFile, Compaction. HBase features in variable column schema, retrieving values by timestamp versions, and per row atomic operations. Cross-partition transactions can be built atop with [Percolator](https://research.google/pubs/pub36726/). HBase becomes the de-factor big table schema database on HDFS, and serves as the backend for higher level systems serving SQL, time-series, block, etc. ByteDance has customized implementation of Big Table and Spanner [[1]](https://mp.weixin.qq.com/s/DvUBnWBqb0XGnicKUb-iqg)[[2]](https://mp.weixin.qq.com/s/oV5F_K2mmE_kK77uEZSjLg). Alibaba customized HBase and published [Lindorm](https://zhuanlan.zhihu.com/p/407175099).

  * [Cassandra](https://www.cs.cornell.edu/projects/ladis2009/papers/lakshman-ladis2009.pdf) follows the peer-to-peer (P2P) cluster management from [Dynamo](http://docs.huihoo.com/amazon/Dynamo-Amazon-Highly-Available-Key-Value-Store.pdf), while [DynamoDB](https://www.allthingsdistributed.com/2012/01/amazon-dynamodb.html) ([paper](https://www.usenix.org/conference/atc22/presentation/elhemali)) is AWS commercial that also follows Dynamo. It has no dedicated metadata quorum, but carries metadata in peer nodes and propagates with [Gossip](http://kaiyuan.me/2015/07/08/Gossip/) protocol. It supports big table schema where primary key is required. Keys are partitioned and placement-ed by [Consistent Hashing](https://www.toptal.com/big-data/consistent-hashing) to avoid data churn when node join/leaves. Cassandra employs quorum write/read (write N replicas, read N/2+1 replicas) to ensure durability and version consistency. Similar P2P cluster management can be found in [Service Fabric](https://dl.acm.org/doi/pdf/10.1145/3190508.3190546) which hosts micro-services and has extensive mechanisms for member node ring consistency.

  * [ElasticSearch] originates from full-text search engine based on Apache Lucene, so popular, then evolves into the scalable database of JSON documents, logging, time-series, [geospatial data](https://www.baeldung.com/elasticsearch-geo-spatial) with strong search support. ElasticSearch manages [scaleout](https://www.cnblogs.com/sgh1023/p/15691061.html) with primary-secondary replications, and hash sharding. Previously ElasticSearch was also known by [ELK stack](https://www.elastic.co/what-is/elk-stack). 

  * [InfluxDB](https://www.influxdata.com/_resources/techpapers-new/) is a popular time-series database. Compared to SQL databases, time-series database exploits fixed data organization and query patterns. Metric dimensions can be aggregated to tackle with high ingress volume, re-sampled to tier data. Another contemporary is [OpenTSDB](https://zhuanlan.zhihu.com/p/111511463), which supports time-series atop HBase. Time-series database is frequently used in [monitoring](https://logz.io/blog/prometheus-influxdb/) and [IoT](https://www.influxdata.com/blog/how-influxdb-iot-data/).

__Graph database__

  * [Graphene](https://www.usenix.org/conference/fast17/technical-sessions/presentation/liu) builds the typical patterns for a graph databases, semi-external memory. It speeds up queries by co-locating edges and vertices accessed together, managing small objects and fine-grained IOs. Former work traces back to [GraphLab](https://arxiv.org/ftp/arxiv/papers/1408/1408.2041.pdf). Other contemporaries include [Neo4J](https://neo4j.com/), which originates from saving OO graph in DB (database); [ArangoDB](https://www.arangodb.com/), which features in [JSON document graph](https://www.g2.com/categories/graph-databases) and multi-model; and [OrientDB](http://www.enotes.vip/index.php/tz_enotes/Article/showArticleReader.html?art_id=513) which is also a [multi-model](https://db-engines.com/en/system/ArangoDB%3BNeo4j%3BOrientDB) database. Graph databases are frequently used in Social Network mining and iterative Machine Learning.

  * [Facebook TAO](https://www.vldb.org/pvldb/vol14/p3014-cheng.pdf) the frugal two level architecture for social graph (OLTP). Persistence/capacity layer is by [MySQL](https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf), which instead uses [RocksDB](https://vldb.org/pvldb/vol13/p3217-matsunobu.pdf) as engine. QPS/cache layer is by Memcached, with a long thread of [works](https://www.usenix.org/conference/osdi20/presentation/berg) to improvement. For consistency, TAO supports 2PC cross shard write, and prevents fracture read (not ACID, not snapshot isolation). Query is optimized to fetch association.

  * [FaRM A1](https://ashamis.github.io/files/A1-A-Distributed-In-Memory-Graph-Database.pdf). General purpose graph database used by Bing for knowledge graph, all in-memory. Vertices/edges are organized in linked structure objects, accessed via pointer addresses, and build optimistic concurrency control (OCC) transaction and MVCC (multi-version concurrency control) read via FaRM. Other contemporaries include [AWS Neptune](https://aws.amazon.com/neptune/); and [CosmosDB](https://azure.microsoft.com/en-us/blog/a-technical-overview-of-azure-cosmos-db/), which developed from [DocumentDB](https://www.vldb.org/pvldb/vol8/p1668-shukla.pdf), is a globally distributed (optional) strong consistency multi-model database, and uses Bw-tree with "Blind Incremental Update" instead of LSM-tree to absorb writes.

  * [ByteGraph](https://www.vldb.org/pvldb/vol15/p3306-li.pdf) builds graph database atop RocksDB ([TerarkDB](https://www.zhihu.com/question/46787984)) with widely compatible [Gremlin API](https://tinkerpop.apache.org/gremlin.html). Weighted consistent hash ring shards vertex & adjacent edges to one node. RocksDB easily represents vertex and edges in KV, support in-memory/on-disk tiering, and single node transaction. Large edge list is implemented by edge-tree (B-tree), and further supports secondary index. ByteGraph also supports geo replication (eventual consistency), distributed transaction (2PC), and cost-based query optimizer.

__Datalake__

  * [Apache Hudi](https://zhuanlan.zhihu.com/p/450041140) to build datalake atop HDFS, Kafka, Spark, Hive. Compared to data warehouse, it allows update data via CopyOnWrite or MergeOnRead. Other [contemporaries](https://www.slideshare.net/databricks/a-thorough-comparison-of-delta-lake-iceberg-and-hudi) are [Delta Lake](https://databricks.com/wp-content/uploads/2020/08/p975-armbrust.pdf) which brings ACID with Spark, [Apache Iceberg](https://www.dremio.com/resources/guides/apache-iceberg-an-architectural-look-under-the-covers/) which features in high performance query. Datalakes generally emphasize in cross-system interoperability. Combing datalake and data warehouse, you get [Lakehouse](https://databricks.com/blog/2020/01/30/what-is-a-data-lakehouse.html) pattern.

  * [F1 Query](http://www.vldb.org/pvldb/vol11/p1835-samwel.pdf) connects multiple data sources like Spanner, BigTable, CSV, ColumnIO, Capacitor, ETL, to create the federated query engine. The former [F1](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41344.pdf) was built atop Spanner and serves Google AdWords. F1 Query supports interactive SQL queries with joins, batch queries, and custom UDFs via the UDF Server. Query is executed as a DAG in parallel, where "dynamic range repartitioning" alleviates data skew. F1 Query use heuristic rules in query optimizer. Besides [F1 Lightning](http://www.vldb.org/pvldb/vol13/p3313-yang.pdf) adds support to HTAP by replicating extra columnar replica, and ensures snapshot consistency by tracking timestamp watermarks.

__Stream processing__

  * [Kafka Transactional](https://assets.confluent.io/m/2aaa060edb367628/original/20210504-WP-Consistency_and_Completeness_Rethinking_Optimized_Distributed_Stream_Processing_in_Apache_Kafka-pdf.pdf) builds exactly-once transaction level consistency in messaging queue. This made stream processing reliable, to be the first-class citizen than database tables. This further enables [Kappa architecture](https://blog.twitter.com/engineering/en_us/topics/infrastructure/2021/processing-billions-of-events-in-real-time-at-twitter-) with transactional Spark, to replace the dual-cost Lambda architecture.

  * [Spark](https://spark.apache.org/docs/latest/rdd-programming-guide.html) outperforms MapReduce by in-memory RDD and micro-batch process, and then extends to [stream processing](https://spark.apache.org/docs/latest/streaming-programming-guide.html). It is the de-factor Big Data computation framework. Among [contemporaries](https://medium.com/@chandanbaranwal/spark-streaming-vs-flink-vs-storm-vs-kafka-streams-vs-samza-choose-your-stream-processing-91ea3f04675b), [Flink](https://flink.apache.org/) features in one-by-one streaming (rather than micro-batches), [checkpointed 2PC exactly-once](https://www.infoq.com/news/2021/11/exactly-once-uber-flink-kafka/), and [ack by XOR of path nodes](https://hps.vi4io.org/_media/teaching/wintersemester_2017_2018/bd1718-11-streams.pdf#20).

__Persistent memory__

  * [NOVA](https://www.usenix.org/conference/fast16/technical-sessions/presentation/xu) sets up the design patterns for how to build filesystem on persistent memory (PMEM) with high concurrency. NOVA indexes by DRAM radix tree, and improves concurrency by per inode logging, per core free-list. Nova builds atomic file operations with logging, COW, `clwb` instruction on (customized) DAX-mmap. [ART and hashtable](https://bigdata.uni-saarland.de/publications/ARCD15.pdf) are also frequently used index for PMEM storage.

  * [Level Hashing](https://www.usenix.org/conference/osdi18/presentation/zuo). Though NOVA uses tree-based PMEM data structure (filesystem inode tree), another approach explores hashtable data structures on PMEM. It favors O(1) lookup. Level Hashing uses no logs. Resizing is done by two-level rotates. Crash consistency is guaranteed by carefully operating flag bits. However, hash-based PMEM data structure doesn't support range query. 

  * [Orion](https://www.usenix.org/system/files/fast19-yang.pdf) further speeds up PMEM filesystem by directly exposing memory access via RDMA to client, continued from [Octopus](https://www.usenix.org/conference/atc17/technical-sessions/presentation/lu). Remote PMEM becomes a pool, local PMEM is accessed via DAX. Besides, this [guide](https://www.usenix.org/system/files/login/articles/login_summer17_07_rudoff.pdf) is useful for PMEM programming.

  * [SplitFS](https://arxiv.org/abs/1909.10123), continues from to Orion, puts data path at userspace and metadata operations at kernel by Ext4-DAX. Data path speeds up by bypassing Kernel, while Kernel still manages critical operations affecting consistency and isolation. In this thread, [Kuco](https://www.usenix.org/conference/fast21/presentation/chen-youmin) introduces Ulib, collaborative indexing, and two-level locking, to offload more fine-grain operations to userspace. [ZoFS](https://ipads.se.sjtu.edu.cn/_media/publications/dongsosp19-rev.pdf) instead use MMU to isolate filesystems from different users, while per single user can operate both metadata/data in userspace (protected by MPK).

__Cloud native__

  * [Snowflake](https://www.usenix.org/conference/nsdi20/presentation/vuppalapati) is the OLAP database native on public cloud. Memory caching, query processing, storage are disaggregated, reuse public cloud service (e.g. [S3](https://docs.snowflake.com/en/user-guide/data-load-s3.html)), and independently scalable and billable. Tenant isolation leverages VMs (virtual machines), and offloads the classic resource under-utilization problem to cloud. To avoid read S3 every time, Snowflake adds a caching layer based on ephemeral storage. Nodes can be pre-warmed for elasticity. Snowflake went [IPO](https://edition.cnn.com/2020/09/16/investing/snowflake-ipo/index.html) very successfully.

  * [Service Mesh](https://istio.io/latest/about/service-mesh/) is a containerized micro-service infrastructure, where Sidecar proxies (e.g. [Envoy](https://istio.io/latest/docs/ops/deployment/architecture/)) adds traffic routing, Service Registry, Load Balancing, Circuit Breaker, health Checks, encryption, etc to Apps with little code change. The former [Spring Cloud](https://xie.infoq.cn/article/2baee95d42ed7f8dd83cec170) can be migrated to K8S and Service Mesh environment with effort.

  * [Dominant Resource Fairness](https://cs.stanford.edu/~matei/papers/2011/nsdi_drf.pdf) is a typical [Cloud Resource Scheduling](https://www.researchgate.net/publication/293329163_A_Survey_on_Resource_Scheduling_in_Cloud_Computing_Issues_and_Challenges) algorithm, used in [YARN](https://mp.weixin.qq.com/s/9A0z0S9IthG6j8pZe6gCnw), that normalizes multi-dimensional resource allocation to follow the dominate resource. Alternatively, [2DFQ](https://cs.brown.edu/~jcmace/papers/mace162dfq.pdf) achieves fairness by separating requests to threads according to their sizes; [Quasar](http://csl.stanford.edu/~christos/publications/2014.quasar.asplos.pdf) samples workload profile on a small cluster via Machine Learning, than goto the full cluster; Container/[CGroup](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/using-cgroups-v2-to-control-distribution-of-cpu-time-for-applications_managing-monitoring-and-updating-the-kernel) specifies quota/weight per user job, and the pattern is shared by [K8S scheduling](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/); Ceph QoS [employs](https://docs.ceph.com/en/latest/rados/configuration/mclock-config-ref/) d[mClock](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Gulati.pdf) that uses weighted reservation tags. Besides, [Leaky bucket](https://blog.51cto.com/leyew/860302) is the classic algorithm for throttling; [Heracles](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43792.pdf) isolates resource for latency-sensitive jobs vs batch. In general, cloud introduced [Multitenancy](https://www.usenix.org/conference/fast21/presentation/pan) to depict a system shared by multiple users (tenants) and each assigned a group of virtualization, isolation, access control, and priority/quota policies. For cost estimation, a typical method is request count & size in smoothing window or outstanding queue; [Cost Modeling](https://github.com/pingcap/tidb/blob/master/planner/core/task.go#L260) in DB query optimizer provides more [comprehensive methods](https://15721.courses.cs.cmu.edu/spring2020/schedule.html#apr-15-2020); examples can be found at paper [Access Path Selection](https://www.eecs.harvard.edu/~kester/files/accesspathselection.pdf) and [Optimal Column Layout](https://stratos.seas.harvard.edu/files/stratos/files/caspervldb2020.pdf).

  * [Akkio](https://www.usenix.org/conference/osdi18/presentation/annamalai) used in Facebook migrates u-shards across geo-regional datacenters to maintain access locality. U-shards (in MBs), which represents the small actively access datasets determined by App-side knowledge, is way smaller than shards (GBs), thus incurs low migration cost. [Taiji](https://research.facebook.com/publications/taiji-managing-global-user-traffic-for-large-scale-internet-services-at-the-edge/) is another Facebook system that load balances users to datacenters based on [SocialHash](https://blog.acolyer.org/2016/05/25/socialhash-an-assignment-framework-for-optimizing-distributed-systems-operations-on-social-networks/), i.e. friendly groups are likely to access similar contents.

__Secondary Indexing__

  * [Helios](http://www.vldb.org/pvldb/vol13/p3231-potharaju.pdf) builds global scale secondary index. Updates are ingested into shared logging, the single source of truth, and then build indexes asynchronously with eventual consistency. Index is built bottom-up by merging logs and uproll level by level, and stores at HDFS-compatible datalake. 3rd-party query engine can leverage the indexes to prune blocks. [Hyperspace](https://www.microsoft.com/en-us/research/publication/hyperspace-the-indexing-subsystem-of-azure-synapse/) is another indexing system on datalake, building index with Spark jobs; but publishes fine-grain index states, metadata, data, logs as plain files (with a spec) on datalake to achieve good interoperability.

  * [SLIK](https://www.usenix.org/system/files/conference/atc16/atc16_paper-kejriwal.pdf) builds global secondary index for [RAMCloud](https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848671/RAMCloud+Papers). It partitions B+tree index that is represented as objects in underlying Key-value store. SLIK avoids the cost of distributed transaction by relax index consistency to satisfy common usecases.

  * [HBase Secondary Index](http://ceur-ws.org/Vol-1810/DOLAP_paper_10.pdf) compares global index and local index, mentioned in the [LSM-tree survey](https://arxiv.org/pdf/1812.07527.pdf). Global index only needs one search but incurs high consistency cost upon updates. Local index colocates with each data partition, where consistency update is kept local, but a search needs to query all partitions.

__Content distribution network (CDN)__

  * [Facebook Owl](https://www.facebook.com/atscaleevents/videos/2897218060568137/?t=739) runs a decentralized peer-to-peer data layer (like BitTorrent), while maintaining a centralized control plan with sharded Trackers per region. P2P architecture efficiently scales out and achieves a very high traffic growth v.s. server growth ratio. Content distribution is chunk by chunk, while each chunk follows a different ephemeral distribution tree composed dynamically. Besides preset policies for peer selection and caching, an Emulation framework uses Random-restart Hill Climbing to search for the best policy settings. CDN can also be seen as a special type of distributed cache.

## Storage components breakdown

To plot the architecture design space for distributed storage systems, we divide it by three different dimensions. They map to static/runtime views and non-functional goals of the architecture. Common components can be extracted from sources like section [Reference architectures in storage areas](.). They may overlap, while I strive to separate them concisely and clearly.

__Divide by storage areas__

  * Cache
  * Filesystem
    * Distributed filesystem 
  * Object/Block Storage
  * Data deduplication
  * Archival storage
  * OLTP/OLAP database
    * Shared logging
  * In-memory database
    * Manycore
  * NoSQL database
  * Graph database
  * Datalake
  * Stream processing
  * Persistent memory
  * Cloud native
    * Cloud scheduling
    * Geo Migration
  * Secondary indexing
  * Query processing

__Divide by static components__

  * Metadata nodes
  * Data nodes
  * Indexing
  * Logging & journaling
  * Transaction control
  * Allocator
  * Data layout
  * Data compression
  * Data deduplication
  * Caching layer
  * Cold/hot tiering
  * Client
  * Storage media
  * Networking & Messaging
  * Backup & disaster recovery
  * Upgrade/deployment and restart
  * Monitoring & alerting
  * Configuration management
  
__Divide by runtime workflows__

  * Read path
  * Write path - append/overwrite
  * Load balancing
  * Data replication/repair/migration
  * GC/compaction 
  * Data scrubbing
  * Failure recovery
  * Node membership & failure detection
  * Background jobs
  * Clock synchronization
  * Resource scheduling & quota/throttling 
  * Overload control
  * Offloading

__Divide by system properties__

  * Traffic pattern, query model
  * Data partitioning & placement
  * Consistency
  * Transaction & ACID
  * Scaleout
  * Scale-up
  * High availability
  * Data durability
  * Data integrity
  * Read/write amplification
  * Space amplification 
  * Concurrency & parallelism
  * Throughput & latency
  * Cross geo-regions
  * Operational ease
  * Interoperability

## Technology design spaces & design patterns

The following sections talk about technology design spaces (ordered by the importance). They root in "Reference architectures" listed above, and cover areas in "Storage components breakdown". Unlike breakdowns, techniques and design patterns usually interleave multiple components and require co-design. Architecture design patterns, also covered below, map to certain techniques to achieve desired system properties. When connected the dots, they expand to a consecutive design space that enlightens more choices. 

### Metadata

Key problems related to metadata are the size of metadata, how to scaleout, where to store, and consistency. Metadata size is closely related to data partitioning and placement. 

__Metadata size__

Essentially, the size of metadata is determined by __tracking granularity__ and __degree of freedom__ the per object. They are the key design space dimensions to consider

  * __Tracking granularity__. Smaller partition size generally yields better balance, though more memory consuming. The same also works for multi-thread task scheduling. Think randomly tossing balls into bins; the smaller/more balls, the balancer per bin ball count. Different hot/cold tiers can uses different tracking granularity, e.g. cache blocks but store files, e.g. Akkio u-shards. 

  * __Degree of freedom__. The fundamental reason that an object needs memory to track placement location is due to it has freedom to place at any slot. Limiting the possible slots generally reduces memory consumption, e.g. hash object id to map to a placement location. However, this makes placement inflexible and incurs cost on migration.

Generally techniques and design patterns range from minimal metadata or more metadata for fine-grain control 

  * __Hash-based placement__, the extreme of zero metadata. The typical example is Ceph CRUSH, or consistent hashing. A Ceph PG's placement calculated by a deterministic algorithm, which has no degree of freedom, thus, no metadata needed. The Pro is little metadata memory cost. The Con is excessive data migration when add/remove nodes; balanced placement for capacity but not for hotness; can hardly place when cluster near full. 

  * __Track full placement__, the extreme of full metadata. An object is able to place at any node, and the location is tracked at memory. The Pro is easy to implement extensive migration and balancing for capacity, temperature, in fine-grain. The Con is large metadata size; but there are ways to reduce it or offload.

  * __VNode__, the hybrid approach that put limits to the object side. 2-levels, an object is first deterministically mapped to a VNode, then VNode is placement on any node. VNode increased tracking granularity, thus less metadata to track, but still enjoys placement freedom. The examples are DB placing partitions, which groups rows mapped by hash; Ceph's PG and Dynamo's VNode, which groups small objects (though then still use hash placement); Azure Storage's "extent", which groups small blocks from table layer.

  * __Partitioned Index__, the hybrid approach that limits placement space. Used in Kangaroo KLog index. Rather than allowing an entry to place at any slot of a hashtable, hashtable is split into partitions and entry is allowed to place at a deterministic partition. Thus index space is reduce, and index/pointer memory is reduced. Another approach to limit placement space is [Copyset](https://www.usenix.org/conference/atc13/technical-sessions/presentation/cidon).

  * __Overlay__, the hybrid approach that overlays freedom placement level over hash-based placement layer. Existing objects keeps the old hash-based placement. New objects are tracked in metadata and place in a different algorithm. Adding nodes won't forcefully migrate existing objects. An example is [MAPX](https://www.usenix.org/conference/fast20/presentation/wang-li).

  * __Reduce object linkage__. Another source of metadata size is the mapping linkage used to lookup objects, e.g. a 16-byte UUID. It grows especially when objects are small, and components are disaggregated into different layers or nodes in the system. Techniques to reduce metadata size can be to piggyback child objects into its parent to save the lookup ID.  

__Metadata scaleout__

The de-facto way to handle scaleout is partitioning (or call it sharding). But there are also simpler methods

  * __Partitioning__. Metadata are cut by key ranges to serve at different Paxos rings, e.g. Tectonic. Objects can also hash the key to map. This approach solves scalability, requires implementation complexity, and incurs challenge on consistency.  

  * __Decoupling__. Not all metadata are necessary to be stored in the central store. Less important ones can be decoupled to other stores that scale differently, e.g. Tectonic. This approach increases complexity, and incurs cost on messaging, especially for the previous tight memory scans.

  * __Pushdown__. Metadata can be separated into two levels. The first level is still served in the central store. The second level is looked up on-demand, pushed down to many more data nodes, or pushed down to SSD. A typical example is to handle "Lots of small files" (LOSF): Small files are compacted into a big file, which also persists the index; [HDFS](https://vanducng.dev/2020/12/05/Compact-multiple-small-files-on-HDFS/) only knows the big file, and loads indexes on-demand.

  * __Levels of delegation__. Similar with Pushdown, the example is Big Table, think the cluster-wide B+-tree as the metadata. Metadata is essentially an index to lookup data, if in tree structure, it can be decomposed level by level, and naturally scaleout lower levels to whole cluster, where the top level is specially kept in a consistent Paxos quorum. 

__Metadata where to store__

Where to host metadata, a dedicated cluster, distributed on data nodes, generate on-fly, etc

  * __Paxos cluster__ is the popular approach, e.g. Ceph, FaRM, TiDB, CockroachDB. They use a dedicated Paxos (variant) cluster to host metadata, or Etcd, ZooKeeper that is backed by Paxos (variant).

  * __Peer-to-peer__. Systems originated from Dynamo doesn't use dedicated metadata cluster, but distribute the info across entire cluster. They use Gossip protocol to reach eventual consistency. Besides, Dynamo doesn't have much metadata to track because it uses consistent hashing placement.

  * __Primary/Secondary__. HDFS uses a single Namenode to host all metadata and process transactions. It's simpler. HDFS adds a secondary standby backup nodes for HA.

  * __God node__. You can see distributed DBs get transaction timestamp from one (Paxos quorum of) "timestamp oracle" node, or "sequencer" node, e.g. TiDB's PD, FoundationDB, CORFU. The sequencer node is stateless, can quickly recover by restart, and use epoch to separate old/new.

__Metadata offloading__

Metadata can be managed elsewhere to avoid managing the scaleout, consistency, and persistence.

  * __Consistent Core__. App can manage metadata in Micro-service framework provided ZooKeeper, Etcd. In this way, each dimension of problems are offloaded elsewhere. The approach is popular.

  * __In-memory DB__. Storage cluster-wide metadata management can be offloaded to in-memory database. Examples are HopsFS, or Hekaton. The databases manages metadata partitioning, consistency, scaleout, and tiering cold ones to SSD. At single data node level, Ceph BlueStore offloads metadata to RocksDB, and reuses the transaction. 

  * __Cold Tiering__. Cold metadata can be offloaded to SSD. Which/when to offload need careful management, to avoid slowdown maintenance scan loops, especially when correlated node failures and critical data repair. It's also possible to compress cold memory entries, but which is CPU consuming.

__Metadata consistency__

Different areas can favor their terms, such as DB, Storage, Filesystem, which sometime brings confusion

  * __Database__ area commonly use terms like strong consistency, external consistency, serializability, isolation levels, snapshot consistency. See [Distributed Transactions](http://accelazh.github.io/storage/Linearizability-Vs-Serializability-And-Distributed-Transactions).

  * __Storage__ area and __distributed systems__ may terms like Linearizability, sequential consistency (see above article); and weaker ones like eventual consistency, casual consistency. Eventual consistency (well implemented) guarantees updates finish propagation in a time window, won't revert, and in certain direction. Casual consistency is frequently used in client messaging requiring to see what-you-change.

  * __Filesystem__ area uses "journaling" for metadata logging, and "logging" for data logging. It talks about write atomicity, operation atomicity, and crash consistency. The example of write atomicity is, if a write changes both data and inode, they should either all succeed or all not. The example of operation atomicity is, `rmdir`, rename operations on a directory should never expose half state to user. Crash consistency means after node crash, the filesystem should restore a correct state, e.g. no half rmdir, rename exposed, e.g. no broken linked-list on PMEM.

  * __VM__ and __Backup__ systems use terms like consistent snapshot. A DB can use compute VMs, cache VMs, storage VMs. When Hypervisor takes a consistent snapshot, it means all VMs are taken snapshot at a consistent point-in-time. The anti-example is, compute VM thinks an update is committed, but storage VM's snapshot is taken earlier and says no such commit.

  * __Paxos__ algorithm use terms like consistent read, or quorum read. The issues comes that half of the voters can lag votes, or half of the replicas can lag execution, thus a client can read stale states from a replica. To overcome this issue, the client has to only read from Paxos leader (cannot distribute load, and may failover already), or use quorum read that touches more than half non-leader replicas, or switch to casual consistency instead.

Metadata consistency and data consistency share common techniques, and metadata needs to update in consistent with data. [Epoch](https://wongxingjun.github.io/2015/05/18/Paxos%E7%AE%97%E6%B3%95%E7%9A%84%E4%B8%80%E7%A7%8D%E7%AE%80%E5%8D%95%E7%90%86%E8%A7%A3/) and [fencing (token)](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) are common techniques to expire stale metadata/data (after crash restart) and to exclude stale leaders. I'll leave most to data consistency part. In general, metadata needs strong consistency, or weaker but versioned. 

  * __Single node__, strong consistency. Putting all metadata at a single node is the old way, but extremely simple to implement. HA can be achieved by a secondary standby node, or simply rely on faster restart. Modern CPU ensures sequential consistency per core, and cross-core can achieve linearizability via locking. 

  * __Paxos__, strong consistency, in quorum. Relying on Paxos quorum is the de-facto way to achieve string metadata consistency, e.g. Ceph, HBase. A popular variant is the [Raft](https://raft.github.io/) algorithm, originated from [RamCloud](https://ramcloud.atlassian.net/wiki/spaces/RAM/pages/6848671/RAMCloud+Papers), but becomes even more successful.

  * __Casual consistency__, weaker consistency, propagating. When strong consistency is prohibitive, usually due to performance consideration, metadata can switch to weaker consistency. The most frequently used one is casual consistency, which captures the propagating constraints. It can be implemented by adding version numbers (simplified from [vector clocks](https://newbiettn.github.io/2014/05/03/lamport-clock-vs-vector-clock/)) to messages.

  * __Snapshot consistency__, weaker consistency, versioning. Like causal consistency to constraint propagating, snapshot consistency constraints that within a version, all component states seen are at a consistent point-in-time. Usually both needs a version number, or a timestamp. In general, "weak" consistency is vague, while versioning provides instinctive way to measure and control.

  * __Gossip__. A common way to propagate metadata across nodes is gossiping, i.e. to piggyback metadata in common communications between nodes. An example is Ceph. The method is also commonly applied in heartbeats to detect node health and membership. __Eventual consistency__ can be achieved with version tracking. A node usually also needs periodically refresh with Consistent Core for suspected stale metadata.


### Consistency

Consistency interleaves the core spine of distributed storage system design. The techniques have high variety and touch most components. I choose __scale__ as the first level category to illustrate consistency design space: from single node level, datacenter level, to geo-regional level. In general, key design space dimensions to consider are below. See [Distributed Transactions](http://accelazh.github.io/storage/Linearizability-Vs-Serializability-And-Distributed-Transactions) for more. 

  * __Point of sync__. When a piece of data is changed, there must be a point of time after which the change is made visible to end user. Call it point of sync. It must be atomic, i.e. no half state in middle of invisible vs visible. It must keep promise, i.e. once passed point of sync, it cannot go back. It must reach consensus, i.e. components in the system will agree on the point of sync, according to which propagation it divides into strong consistency vs eventual consistency. For implementation, point of sync usually relies on [atomic disk sector write](https://www.sqlite.org/atomiccommit.html) (e.g. logging commit entry), [atomic memory pointer switch](https://stackoverflow.com/questions/78277/how-to-guarantee-64-bit-writes-are-atomic) (e.g. B+-tree), or another (group of) node that acts as the Consistent Core (e.g. leader participant).

  * __Ensure ordering__. The system must agree on what happens first or later. This is instinctive for append-only or WAL based systems, or where every operation can be serialized by a locking data structure. It becomes tricky when the system involve multiple nodes, or the logging has multiple parallel segments. Versioning (or timestamp) is introduced, where a total ordering maps to Serializable, partial ordering maps to Vector Clocks, and disjoint read/write versions map to Snapshot Isolation (Serializable requires same timestamp for read/write). The system resolved ordering may not be the same with realworld, requiring which it maps to External Consistency. How to handle ordering conflicts varies, where new comer wait maps to plain locking / pessimistic concurrency control, new comer retry maps to OCC, and preempting a lock maps to preemptive concurrency control or [wound-wait](https://cloud.google.com/spanner/docs/whitepapers/life-of-reads-and-writes). For implementation, usually CPU/memory level use locks/latches, and disk level uses flush or direct write.

  * __Separating ACID__. In transaction ACID, usually ACI is united with consistency, but D durability can potentially be separated. Majority of storage systems choose to implement them altogether, essentially because ordering on disk is done by flush or direct write that couples with persistence. We can see more techniques in the following that break the paradigm and improve performance (e.g. Soft Update, Journal Checksum).

__Single node level consistency__

At the __level of CPU/memory__, fundamentally single CPU core ensures sequential consistency (though both compiler and CPU reorder instructions). Multi-core programming involves instruction atomicity (e.g. Intel x64 arch guarantees [64-bit reads/writes are atomic](https://stackoverflow.com/questions/78277/how-to-guarantee-64-bit-writes-are-atomic)), memory operation ordering (e.g. load/store semantics), visibility of memory changes (e.g. volatile, cache invalidation); they can be summarized under [C++ memory model](https://www.youtube.com/watch?v=A_vAG6LIHwQ). CPU provides fine-grain instructions for locking/CAS (e.g. lock, xchg, cmpxchg), memory fencing (e.g. lfence, sfence, mfence), cache flush (e.g. CLFLUSH, CLWB). Going to higher level, they are used to build [programming locks](https://compas.cs.stonybrook.edu/~nhonarmand/courses/fa17/cse306/slides/11-locks.pdf), [lock-free algorithms](http://www.jmfaleiro.com/pubs/latch-free-cidr2017.pdf), and [PMEM commit protocols](https://www.usenix.org/system/files/login/articles/login_summer17_07_rudoff.pdf) (like O_DIRECT flushes to disk, CLFLUSH flushes cache to memory/PMEM). More advanced are developed for [B+-tree locking techniques](http://mysql.taobao.org/monthly/2018/09/01/) in database, and [Linux Kernel synchronization](https://mirrors.edge.kernel.org/pub/linux/kernel/people/christoph/gelato/gelato2005-paper.pdf). They are not a main topic for architecture design.

Coming to storage, more concerns add to __memory/disk level__ and __crash recovery__ (i.e. system integrity). Write-ahead logging (WAL) is the de-facto solution for consistency (as well as write atomicity and durability in ACID), which becomes more dominating with the trend of append-only storage systems (e.g. LSM-tree). WAL (redo/undo log) is also the necessity to implement [database transactions](https://zhuanlan.zhihu.com/p/143173278). But there are more ways for consistency. 

  * __Write-ahead logging__, consistency by sequential logging and commit entry. Metadata/data changes are made durable to disk by journaling/logging; where the journal/logging commit entry, sync flushed to disk, is the point of sync that changes are committed and visible. Logging is naturally totally-ordered, no excluding further use of versioning/timestamp. Database further employs redo logs and undo logs ([ARIES](https://zhuanlan.zhihu.com/p/143173278)), where redo logs is the common logging, and undo logs is introduced because of "No Force, Steal", i.e. a page can be flushed to disk even when a (large) transaction hasn't committed.

  * __Shadow paging__, consistency by COW and atomic pointer switch. The example is BtrFS. New updates are copy-on-write (COW) added to new B+-tree pages. Upon committing, the point of sync is to atomically switch the pointer at the parent node to new pages. The same paradigm is used both in memory and on disk, which CPU/memory controls ordering with locks. The technique is beneficial with built-in support for snapshot, improves parallelism with COW, and won't be bottlenecked at serialized journal committing. However, a change at leaf node incurs change at parent node, and propagating further upper to root, which is expensive (unless employs a Page Mapping Table).

  * __Soft update__, which tracks ordering in memory but without durability. The example is [FFS](https://www.ece.cmu.edu/~ganger/papers/usenix2000.pdf). Inodes tracks update dependency, and the system enforces it. Actual writes to disk can be delayed, and happen asynchronously, and improve parallelism. End user needs to wait notification for changes become durable. Soft update itself doesn't guarantee necessary metadata/data changes are durable upon crash, and careful implementation is needed to ensure crash consistency.

  * __Transactional checksumming__, which tracks ordering on disk but without durability. The system starts writing block A/B in parallel, but expects block A is committed only after block B. Block A carries B's checksum; if a crash happened in middle, leaving B on disk but not A, the checksum can tell block A is invalid. The technique breaks the sequential bottleneck of logging, however determining the point of sync during failure recovery becomes more expensive. See [Optimistic Crash Consistency](https://research.cs.wisc.edu/adsl/Publications/optfs-sosp13.pdf) for more.

Consistency between __metadata/data components__ also needs maintain (continued from the [Metadata section](.)). A typical storage system propagates visibility of new changes from disk data, to index, then to end user. The index here is metadata, which tells how to lookup data, e.g. inode trees. From system internal, the propagation is usually of __eventual consistency__, e.g. allocating disk space, write data, then after some time to commit the journal. From the view of end user, it's __made atomic__ by the interface (hiding system internals) and notification (async) exposed by the write request. This same design pattern applies when metadata and data are separated to different groups of nodes.

__Datacenter level consistency__

After single node level consistency, we come to the distributed multi-node level. From strong to weak, modern distributed database typical implements distributed transactions for ACID at Serializable or Snapshot Isolation level. Storage systems builds strong consistency with data replication. NoSQL, caching, cross systems interactions typically employ weaker consistency models to reduce complexity and overhead on performance.

  * __Distributed Transactions__. See the [article](http://accelazh.github.io/storage/Linearizability-Vs-Serializability-And-Distributed-Transactions) for more. Examples are Spanner, Percolator, CockroachDB, TiDB. The implementations vary at point of sync, how to enforce ordering, and lock conflict handling. Besides, database global secondary index, in strong consistency with user writes, also implements with distributed transaction.

![Distributed transaction spectrum of strategies](/images/dist-transaction-strategy-spectrum.png "Distributed transaction spectrum of strategies")

  * __Raft data replication__. Examples are CockroachDB, TiDB. Like running metadata in Paxos quorum, data partitions are replicated with Raft protocol (a Paxos variant). This ensures strong consistency, and reuses optimizations on Paxos e.g. [Out-of-order commit](https://www.zhihu.com/question/278984902). [Megastore](http://cidrdb.org/cidr2011/Papers/CIDR11_Paper32.pdf) provides comprehensive optimizations for Paxos replication.

  * __3-way replication__. Examples are Ceph, and similarly the [Chain Replication](https://sigops.org/s/conferences/sosp/2011/current/2011-Cascais/printable/11-calder.pdf) used in Azure Storage. It's simpler and came earlier than Raft. The classic implementation selects a leader node via the Consistent Core (e.g. the metadata cluster) to drive follower nodes with strong consistency. Throughput can be optimized with pipelining.

  * __Quorum read/write__. Examples are Dynamo, Cassandra. With N replicas in total, either read or write operations on > N/2 replicas, so they guarantee to intersect on the replica with the latest version. The implementation adds more complexity to handle read amplification (or simply return cached versions), version tracking, and node write failures.

  * __Log is database__. Like WAL simplifies single node consistency, distribute system can build atop a shared logging service. Examples are FoundationDB, Helios Indexing. The idea can be expanded to build system atop any shared storage service that provides strong consistency and act as a single node, e.g. a distributed filesystem, a page store. Examples are AWS Aurora Multi-master, Azure Storage. The idea also extends to propagate changes in a synchronous or eventually consistent way, which naturally works with database WAL. Examples are Helios Indexing, [MySQL BinLog Replication](https://hevodata.com/learn/mysql-binlog-based-replication/).

Above techniques build strong consistency. For weaker consistency

  * __Eventual consistency__. Typically if a system doesn't do anything about consistency, and let changes propagate, it's eventual consistency. Better implementation provides versioning to measure propagation, and guarantees deadline for propagation.

  * __Casual consistency__. Same with [Metadata section](.)'s. It's compatible with Eventual consistency, and a client must see what it already sees. For implementation, client tracks the low watermark version it wants server to return.

  * __Custom consistency level__. The example is RAMP-TAO, which checks local result set satisfies "read atomicity", and fetch missing versions from RefillLibrary. In general, wide spectrum of custom consistency model can be implemented by tracking versions with data, checking consistency constraints on the fly, and buffer necessary lookups in a cache.

  * __Compensation Transaction__. See this [article](https://developer.jboss.org/docs/DOC-48610). It unites multiple systems to build (a pseudo) ACID transaction. Each system internally supports ACID transaction and idempotent operation. The client drives transaction, propagating changes across the multiple systems in an eventual consistency way in single direction, with at-least-once semantics and a clear completion time. If one system fails in middle, which breaks atomicity, client rollbacks by replaying "Compensation Transaction" at each system in reverse order. Hiding all complexity, the client exposes a seemingly ACID transaction interface. The techniques is handy to build booking service in large scale Internet companies. Additionally, a "reservation" step can be added to makes a system less easy to fail, which renders it more like 2PC (except other client can read middle states).

__Geo-regional level consistency__ 

When coming to cross-regional multi-datacenter level, the techniques are similar with single datacenter level. But the scale makes strong consistency or synchronous replication hard due to the latency overhead. Most implementations are eventually consistent, where disaster recovery area defines measure concepts

  * __RTO (Recovery Time Objective)__. How long the system and application needs to recover at the second region, after a disaster happened at the first region. RTO can be long if the system startup, cache warm, DNS hand-off take time. 

  * __RPO (Recovery Point Objective)__. Because cross-region replication is async, there is a delay from replicated data to the latest data. RPO defines the delay window. It maps how much recent data will be lost after recovery in the second region.

Besides those duplicate with Datacenter level, common techniques are below. In compare, more optimization are for unstable links and low bandwidth in WAN. 

  * __Geo-replication__. Databases commonly support async replication (eventual consistency) used for backup cross regions, typically by replicating logs, e.g. MySQL BinLog Replication, and [Redis](https://redis.io/docs/manual/replication/) primary/secondary replication via command stream. Async Geo-replication doesn't exclude sync replicate a small piece of critical metadata; and doesn't exclude a client to query the primary region to determine the latest version.

  * __Incremental diff__. Ceph provides [RBD diff](https://ceph.io/en/news/blog/2013/incremental-snapshots-with-rbd/) that exports incremental snapshots, which can be used for geo-replication in a semi-automate way.

  * __Log is database__. Most is already summarized above. Use logs to replicate changes in eventual consistency way. Examples are Helios Indexing, MySQL BinLog Replication.

Above are eventual consistency replications. For strong consistency geo-replication, typically Paxos replication is employed (and optimized), while clock syncing for serializable transaction becomes a bigger problem.

  * __Megastore Paxos__. [Google Megastore](http://cidrdb.org/cidr2011/Papers/CIDR11_Paper32.pdf) synchronously replicates across WAN using optimized Paxos protocol. Compared to primary/secondary replication, any Paxos replica at a nearby or less utilized datacenter can lead transaction to balance load. Write only needs > N/2 replicas to ack, which reduces cross-datacenter latency. Local datacenter reads are favored, by using a Coordinator to track which replica has latest versions. Writes use [Leader Paxos](http://accelazh.github.io/storage/Multi-Paxos-Raft-Multi-Raft-Parallel-Raft), where leader selection favors nearby replica. Witness replicas, which vote and replicate logs but won't execute logs to serve DB data, are introduced to form a quorum when too few participants. Read-only replicas, which don't vote but replay logs to serve DB data, are introduces to serve snapshot reads. Per implementation, Paxos cross-datacenters is essentially replicating logs, similarly "Log is database".

  * __Spanner & TrueTime__. Like Megastore, [Google Spanner](https://cloud.google.com/spanner/docs/replication) stores replicas in different geo-regions, and employ Paxos replication. Distributed transaction is implemented by 2PC, whose liveness is guaranteed by HA of a participant's Paxos replicas. The special part is [TrueTime](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45855.pdf), used to synchronize clocks across datacenters, thus to implement External Consistency via Commit Wait ([article](http://accelazh.github.io/storage/Linearizability-Vs-Serializability-And-Distributed-Transactions)). TrueTime relies on customized hardware, i.e. GPS receivers and atomic clocks, as time master nodes in each datacenter, to guarantee [< 7 ms clock drifts globally](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf).

  * __CockroachDB & Hybrid-Logical clock (HLC)__. Like Spanner, [CockroachDB](https://www.cockroachlabs.com/blog/geo-partitioning-one/) employs Paxos (Raft) data replication across regions, and 2PC for distributed transaction. Reads favor nearby replicas, and writes can choose nearby replicas in same region first and leave others in async. Different from Spanner TrueTime, CockroachDB uses [HLC](https://dl.acm.org/doi/pdf/10.1145/3318464.3386134) for cross-datacenter clocks. HLC provides causality tracking at its logical components, and monotonic increasing epochs at its physical component, and employs NTP as the software-only clock syncing protocol.


### Write path

The next big component in a distributed storage system is write path, following which you characterize how a system works. Append-only or update in-place fundamentally divides system styles and next level techniques. Write path touches almost every other components in a system, e.g. metadata, index, data organization, logging, replication, and many system properties, e.g. consistency, durability, amplification.

__Append-only vs update in-place__

The first driving dimension is __append-only__ vs __update in-place__. Transitional single node filesystems usually update disk data in-place (except BtrFS). Later the quick adoption of LSM-tree leads the predominance of append-only systems, also known as log-structured systems. Not only HDD which benefits from sequential writes, SSD also favors append-only (e.g. RocksDB) due to internal FTL & GC. More, PMEM filesystems e.g. NOVA adopts append-only with per-inode logging; and in-memory systems e.g. Bw-tree adopts append-only with delta pages.

  * __Update in-place__. Examples are EXT4, Ceph. If a piece of data is to be updated, it's overwritten on the same address on the disk, rather than written to a new address. Compared to append-only, address tracking is simpler, without needing extra memory metadata to track new addresses; and without extra costly GC to reclaim old data. The drawbacks are: 1) the underlying HDD doesn't like random writes. 2) With a fixed block-size, storing compressed results are tricky. 3) Double-write problem, where overwrites need transaction to protect against crash, thus new data gets an extra write in journaling.

    * __Content-based addressing__. The example is XtremIO. Each piece of data has a fixed on-disk location (think about placement by data hash, but at disk block level). When the data block location is determined by data content hash, it can be used to auto dedup. Since data block location has zero degree of freedom, such system needs minimal metadata to track data location, and cannot be implemented by append-only.

    * __Set-associative cache__. The example is Kangaroo and [Flashcache](https://github.com/facebookarchive/flashcache/blob/master/doc/flashcache-doc.txt). Entire SSD is used to map a large HDD space, just like how CPU cache maps memory. An HDD data block can be stored on SSD, selecting from a small set of blocks. The set is determined by hashing, within which a block is found with linear probing. Similarly, by limiting the data location degree of freedom, minimal memory metadata is needed.

    * __Database paging__. A cleaner way to update in-place is to divide address space into pages, and use page as the atomic unit of transfer. The "page" here is like storage "blocks". However, the system additionally needs transaction logging to guarantee crash consistency. More, even only a few bytes updated, an entire page has to be switched, i.e. write amplification. A page can have internal fragmentation that margin bytes cannot be utilized, i.e. space amplification. If page doesn't need to be equal-sized, it becomes "chunks", or "micro-partitions".

  * __Append-only__. Examples are LSM-tree or RocksDB, Log is database, Azure Storage. The systems don't support modifying written data on-disk, thus updates need to append to new places, like a log. The main drawbacks of such systems are: 1) Constant GC (or compaction) is needed to reclaim old data, which can eat up even 50% of system bandwidth. 2) Data location has high degree of freedom, thus the system either needs huge memory metadata to lookup, or incurs read amplification when scanning through stale data. The benefits are: 1) Everything is simplified because written data is immutable. 2) Writes are sequential which HDD favors. 3) Transaction and crash consistency is built-in, because data is log. Over the years, after all, append-only proves successful.  

    * __Sequential structure or not__. The example is BtrFS. Not all append-only follows a sequential logging. In BtrFS, new data is copy-on-write to a new page, and then atomically linked to the B+-tree. Besides, optimization like parallel multi-segment logging also breaks the default one sequential logging.

    * __Cleanup inline or offline__. Append-only needs to cleanup stale data; should it be done on the write path, or offline? GC/compaction chooses offline. Apache Hudi copy-on-write chooses inline of the write path. Besides, the cleanup can even be delayed to the first user read, i.e. Apache Hudi merge-on-read.

    * __Delta data__. The idea of append-only can be expanded to indexing, on PMEM (e.g. NOVA) or in-memory (e.g. Bw-tree). They exploit that appending delta data benefits high concurrency, simplifies lock handling, and avoids amplification like COW. In another perspective, immutable data can either be implemented by COW or appending delta, while COW forces compaction on write path.

    * __Log is database__. We mentioned before already. Compared to database paging which incurs random writes, transferring logs across components writes sequentially. Syncing pages incurs write amplification if only partial page is modified, but repeated modification on same address can be absorbed; while logging carries delta, smaller than whole page, but can grow to a long list for repeated modification, thus need compaction. Though log can easily be used as a consistent truth for database state, replaying to the latest data incurs computation cost, and needs careful version aligning to leverage cached pages.

  * __Hybrid approach__. The example is Ceph BlueStore, where big writes are append-only, small writes overlapping no existing data is in-place, and small overwrites are merged to RocksDB WAL. This approach was invented to overcome Ceph double-write problem. It essentially bridges the old in-place update to append-only.

Thinking in higher level, the driving factor behind append-only vs update in-place is whether to delay __maintaining on-disk data organization__, to do it inline or offline, or a write-optimized data format vs a read-optimized data format.

  * __Write path__ is efficient if it doesn't need to maintain on-disk __data organization__ (see next [section](.)). Writes favor batching, sequential. This is what __append-only__ brings, except extra bandwidth spent for GC/compaction. Besides, writes favor less co-update components (in sync), e.g. fewer indexes, caching, less fragmented write locations.

  * __Read path__ is efficient either if data has an index, or the location can be derived from the key, or well-sorted to favor full scan. Data should be less fragmented, preserve locality, and with fewer stale entries. Though __append-only__ generates fragmented deltas, GC/compaction can rewrite them to optimized read formats. Though __update in-place__ saves GC/compaction traffic, more read-optimized formats may still need extra rewrites.

    * __Data index__ is usually needed for efficient read path. __Update in-place__ reduces index size by limiting data location degree of freedom, though not applicable to secondary indexes; and by preserving tracking granularity, i.e. unlike __append-only__ which redirects small updates to a new page. This also means less ripple updates to index.

  * __On-disk data organization__. The best read-optimized data format almost always require a full rewrite to generate, which explains why append-only is favorable, especially considering columnar compression (i.e. OLAP). More recent data, which can be separated by hot/cold tiering (or like the "levels" in LSM-tree), may still benefit from update in-place to reduce GC/compaction or churn to index (though in fact most also use append-only).  

__Co-updating neighbor components__

Besides on-disk data, write path touches a wide range of components to co-update together, e.g. metadata, index, checkpoint, logging, cache. 

  * __Metadata, index__. The main concern here is the propagation of visibility from disk data change to end user. This is mentioned before in [Consistency section](.).

  * __Checkpoint, logging__. New changes are first made atomically durable by WAL, where a typical technique is separating key/value (WiscKey). Durable changes can then be propagated to index and metadata to be made visible to user. Logging is a write-optimized format, while reads need structured data. The "structured data" is either periodically flushed from memory to disk, i.e. checkpointing, or by transferring database pages. Fragmented, overlapping checkpoints further need GC/compaction to rewrite to more read-optimized format (e.g. LSM-tree), and to reclaim deleted storage space.

  * __Cache__ updates are async, usually be offline from write path; unless the write wants to invalidate stale data or immediately load new data.

Besides writing locally, __data replication__ is also interleaved in write path. It achieves durability and many other purposes

  * __Durability__, e.g. Raft replication, 3-way replication, quorum writes, see [Consistency section](.). Durability replication is usually synchronous with strong consistency.

  * __Disaster-recovery__, e.g. backup, geo-replication__, see [Consistency section](.). They can async with an agreement on RPO.

  * __Locality__, e.g. geo-replication which moves data to user's local region, e.g. Akkio u-shards; and CDN that acts as static content cache and bridges across WAN provider.

  * __Data layout__. Examples are TiFlash and F1 Lightning. The databases maintain main data copy as row-format to serve OLTP, which replicate an extra columnar layout copy for OLAP use. Raft protocol or fine-grained version tracking can be used to maintain consistency between replicas.

  * __Hot/cold tiering__. Hot data can be copied cache. Cold data can be offloaded slow HDD or archival storage. Data formats between tiers can also be different, to favor access latency, storage efficiency, or compression. 

  * __Data balance__. Typically, data can be re-balanced to occupy empty new nodes, to spread out placement from correlated failure domains, or to balance hot/cold access on nodes.

  * __Log is database__. Instead of replicating data or pages, logs which carry delta are replicated and propagated as the source of truth. See [Consistency section](.).

  * __Separating write path and read path__. The example is AnalyticDB, MySql primary/secondaries replication. The design originates from database community that uses one server as write primary, and replicates to multiple replicas to scale reads. It exploits the pattern that social network generates content (writes) in a relatively constant rate, but user views (reads) can burst high.

Offline background jobs touching data can also be divided by purpose. They usually rewrite data copies, which is the main source of __write amplification__, but necessary to reduce __read amplification__ by generating a more optimized data layout.

  * __Durability__. Typically the data repair process, which comes when nodes or disks went bad. These background jobs require low detection time, and high priority bandwidth. Data repair efficiency can be improved by __involving more nodes__ to provide source data, e.g. Ceph which involves full cluster, Copyset which involves a partition of cluster, and primary/secondary replication however which only involves a few secondaries.

  * __Storage efficiency__. Data compression can be run off the write path to avoid increasing user seen latency. Erasure coding can then further reduce storage space needed. GC runs periodically to reclaim deleted storage space.

  * __Data layout__. E.g. RocksDB runs offline compaction, which removes stale data, sort out overlapping SST files, to make reads more efficient. E.g. AnalyticDB buffers new writes in incremental files, and then merge them to baseline data and build full index. Similar patterns of delta merging can also be found in Datalakes, e.g. Apache Hudi. W.r.t. data replication, the destination copy can be placed in another node or even another cloud service, while the computation can also be __offloaded to cloud__.

  * __Data integrity__. Storage systems typically employ offline data scrubbing to detect silent data corruption. End-to-end CRC can be stored along with data. Besides, invariant with different layers can be checked, e.g. index vs data, mapping constraints.

__Write to different storage media__

Write data flows through or eventually persists at one of the storage media: memory, PMEM, SSD, HDD, or archival tapes. Data structures and techniques vary according to the characteristics of storage media, and the workload access patterns. We will see more in [Data indexing section](.) and [Data organization section](.).

  * __Memory tier__ does well with random access and provides the lowest latency compared to other storage tiers. The major concern is to improve concurrency, cache efficiency, and to pack more data in memory. Typical data structures can be plain pointer links (e.g. FaRM), skiplists (e.g. RocksDB) and Bw-tree which favor concurrency, [B+-tree](https://www.zhihu.com/question/516912481/answer/2403713321) whose bigger node benefits cache line than red-back tree, and hashtables for quick lookup (e.g. Memcached). Memory compression and disk SWAP can be enabled (e.g. [TMO](https://www.cs.cmu.edu/~dskarlat/publications/tmo_asplos22.pdf)).

  * __PMEM tier__ is [2x~3x slower](https://www.usenix.org/conference/fast20/presentation/yang) than DRAM, and doesn't like small random writes. The major concern is to improve concurrency, compensate with slow CPU, and maintain crash consistency while avoiding expensive cache flush instructions. RDMA and Kernel bypassing are common techniques. Tree-based append-only data structures, e.g. per inode logging in NOVA, are still favorable. Another approach uses hashtable data structure, e.g. Level Hashing.

  * __SSD tier__. Except a few systems update in-place, most systems shift to append-only, e.g. RocksDB, and TiDB/Cockroach/MySQL which use RocksDB as engine, HBase/ClickHouse which employs LSM-tree (like) engine, or FoundationDB / Azure Storage which build atop shared logging. I.e. SST files and central logging are the common data structures on SSD. OLAP databases also favor append-only in batch and rewrite to compressed columnar layout. Some databases choose to build index for every column, while some others solely rely on full scan.

  * __HDD tier__. Since both favor append-only, the data structure are similar on HDD or SSD, where most systems can interchangeably run on both. The difference is SSD one needs more CPU and parallelism allocated per device. 

  * __Archival tapes tier__. Append-only is also the favored write style, e.g. Data Domain, thus no much diff from HDD or SSD ones. The data is usually deduplicated and appended in sequential structure, and relying on an index to lookup. Dedup fingerprints can be stored with data that preserves locality. Higher compression level and longer erasure coding codecs are used.

  * __Computation tier__. The above tiers sort by data size. Computation tier is special that, in certain cases there is no data needs to store, and all can be derived from calculation. In another word, "store" data in calculation.

__Tiering between different storage media__

In general, storage media tiers are chosen according to the price, scale, and performance targets of data. Each tier has their own optimization techniques. Data movement across tiers yet needs efficient temperature detection/prediction algorithms, which are usually LRU variants but more concerned in reducing tracking metadata size against the large data scale:

  * __Exponential smoothing__. This is the standard academy method that averages now and history hotness with a weight, where older history is exponentially forgotten. The method doesn't mention how to implement it efficiently. Hotness can be measured by data access IOs and bytes in a time window.

  * __LRU (least recent used)__. Like exponential smoothing, LRU is the typical method that stems most temperature tiering algorithms, but doesn't specify how to implement. 

  * __Bits per object__. The example is Kangaroo RRIParoo algorithm. Temperature is tracked by per object bits. A bit can be flipped when the object is accessed, or global eviction is needed (e.g. clock tick, cache full). If all bits match, the object can be evicted.

  * __Objects in list__. Examples are linked-list implemented LRU, or Linux Kernel [memory page swap](https://github.com/torvalds/linux/blob/master/mm/workingset.c). Temperature is tracked by object position in list. Objects are prompted to head when accessed, pushed to tail when cold, and evicted beyond tail. 

  * __Last accessed and expire__. Usually seen when App is operating cache aside. Simply, the last accessed item from DB is also put into cache. The oldest item is evicted if the cache is full. Cache items also expire by a timeout.

  * __Offline classification__. Examples are Hekaton Siberia, [Google G-SWAP](https://research.google/pubs/pub48551/). When temperature tracking metadata is too large, the system can dump traffic records (may be sampled) to disk, and employs an offline periodical classification job or __Machine Learning__ to categorize hot/cold data.

  * __User tagging__. Expose interface for end users to explicitly tag whether a piece of data is hot or cold. Simple, but users always know better.

__Write & read paths coalescing__

Though write/write and read/read coalescing are common techniques, write/read and read/write have interesting ways to combine and reuse each other's middle results.

  * __Writes coalescing__. Small writes can be combined into one big write to disk. The system can use a timeout plug to accumulate enough small writes to combine, or just scan and sort through the write queue. Small writes in neighbor addresses can be combined to favor big sequential writes. Repeated writes to the same address can be canceled out and leave the last write to disk. A fast staging memory, flash, or PMEM can be kept to absorb small writes.

  * __Reads coalescing__. Like writes, small reads can be combined to favor sequential disk accesses, or save repeated reads with caching. A read query typically needs to scan more physical data than what user requested, which means multiple queries can be batched and share one single disk scan.

  * __Read as a path for write__. When a read query is scanning data to lookup something, it's conceptually building the index. The read can leverage the scan and push the index parts to write path, while write path is responsible to build the index. E.g. [REMIX LSM-tree](https://zhuanlan.zhihu.com/p/357024916) leverages range query to build the index for SST files. Write path is also responsible to rewrite newly ingested data into read optimized formats. It can reuse what the read query just scanned and loaded into memory. It's more useful when the loading is expensive and involves remote network.

  * __Write as a path for read__. Newly written data is usually more likely to be read. Writes can leave them in memory or in staging area, directly populate cache, and organize them in read-optimized data structures. The following reads can be benefited. E.g. The memtable in a typical LSM-tree.

__Offloading__

Inline or offline from write path, FPGA and ASIC are commonly used in offloading from CPU, e.g. compression/encryption, and multi-tenant cloud virtual network processing. Offloading relieves CPU from growing IO hardware throughput, while pushdown shortens data transfer path.

  * FPGA features in reconfiguration, which favors flexibility and early experiments. ASIC are dedicated circuits, hard to change, but once shipped they are much more efficient than FPGA. FPGA had successful usecases like [Project Catapult](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Catapult_ISCA_2014.pdf). [SmartNICs](https://www.microsoft.com/en-us/research/project/azure-smartnic/) also went popular.

  * Compression/encryption are typical offload usecases because the logic is fixed, few exception handling, and data pipeline oriented. Network processing is similar. Besides, nowadays high speed RDMA is much more demanding for CPU, and cloud virtual networking involves more layers of redirections.

  * The more recent [IPU](https://www.forbes.com/sites/karlfreund/2021/08/02/nvidia-dpu--intel-ipu-game-changers-or-just-smart-nics/) (Infrastructure Processing Unit) was proposed following DPU, to offload common datacenter infrastructure functionalities to processing chips other than CPU.

  * [Smart SSD](https://www.youtube.com/watch?v=_8gEmK1L4EY) adds computation chips to SSD. Query filtering or GC/Compaction can be pushed down to SSD internal, without involving the longer data transfer path across PCIe.


### Data Organization

Traditionally "data organization" talks about physical columnar/row-wise data layouts in databases. I choose to view data organization from a broader perspective which is divided by purposes.

  * __Durability tier__. The basic need to organize data in a storage system is to make it durable. __Replication__ is common, on the cost of storage efficiency, yet vulnerable as corruption can be simultaneously replicated. Replication also couples with performance tier to balance reads with extra replicas. __Erasure Coding (EC)__ reduces storage space, improves durability, on the cost of data reconstruct. __Consistency__ is a common issue that accompanies replication. __End-to-end CRC__ and __periodical scrubbing__ are necessary to protect against corruption happens on write path, data transformation, or silent data at reset. __Backup__, __geo-replication__ are standard setups for disaster recovery, while __time travel__ is handy to recover manual errors by restoring an early version.

  * __Query tier__. Disk data needs to support reads and update. Common accesses are __sequential/random reads__, __appends__, __updates (or read-modify-write)__ talked in storage systems, and __point/range queries__, __scans__, __inserts__, __updates (or update-after-query)__ talked in databases. Traditionally, disk data serves both durability tier and query tier coupled, which incurs cost in write path to maintain read-optimized format. Separating read path and write path can help, or move read path entirely to __performance tier__, e.g. in-memory database. Query tier can further specialize for __OLTP__, __OLAP__ and __Datalake__ that share main techniques but vary at query patterns, consistency, data scale, and structured data. 

  * __Performance tier__. Commonly they are extra data copies to balance reads, an SSD tier for caching (or also serves part of durability), PMEM staging area to absorb and sequentialize repeated random writes, plain memory caching, or in-memory DB that moves all computation to memory. When used as cache, SSD or memory can target small blocks rather than entire chunks from disk, see [Data caching section](.). Data organized in memory is more attached to indexes, unlike on disk, see [Data indexing section](.).

  * __Scaleout tier__. To cope with increasing volume and high throughput targets, data is __partitioned__, __replicated__, and work with __placement__ to serve from more machines. __Resource scheduling__ for heterogeneous job sizes, __load balancing__, and __migration__ follow the needs. See [Data partitioning section](.). __Consistency__ is always a problem. On single node it easily relies on CPU cache coherence, but scale-up is bottlenecked by CPU power/heat and cache coherence cost between too many cores. Coming to distributed systems, consistency of distributed transaction still incurs high networking cost, unless relaxing it with App level agreement.

Essentially, query tier carries the most DB techniques when it wants to be performant, while durability/scaleout tiers are orthogonal from it and can be offloaded to a shared storage system, and performance tier is usually addressed by caching. We focus on query tier for data organization, and discuss performance/scaleout tiers in other sections.

__Durability tier__

We covered replication in [Consistency section](.). We will see more about CRC and scrubbing in [Data integrity section](.). Below we briefly expand the design space for Erasure Coding (EC).

  * __Storage overhead__. The main goal of EC is to store data with comparable durability but less storage space, compared to plain replication.

  * __Durability__. Data must be recoverable, if a set of disks went bad. Data must be available (with reconstruct) to user reads, if a set of nodes went offline. 

  * __Performance__. Compared to plain replication, reading (reconstruct) EC data incurs significant cost when part of data is offline, especially the tail latency. With less storage copies, total aggregated bandwidth to serve is capped. 

EC codecs have great richness in schema variety, especially combined with cluster layouts and user traffic patterns. Briefly, main schemas come from below classes

  * __Reed-Solomon Codes__. The standard textbook schemas where each data symbol is symmetrically involved in each parity symbol. The code is MDS, which means able to recover the most loss patterns given fixed storage overhead.

  * __Local-reconstruct Codes (LRC)__. To reduce bandwidth needed in reconstruct reads or data repair, part of parity symbols choose to involve less data symbols. In another word, the schema improves performance in the cost of recoverable loss patterns.

  * __Regenerating Codes__. Another approach to reduce bandwidth in reconstruction. MSR (Minimum Storage Regenerating) codes reach low bandwidth bound without penalty on storage overhead. The code construction is usually more complex and involves more computation.

__Data layout for query tier__

In high level, we first capture the desired __goals__ of a data layout. Ideally we want every goal to reach optimal, which by far is impossible. Trading off between goals composes the design space.

  * __Read amplification__. To return the desired value, how many extra data reads needed in count and size? Locating the data starts from index lookup. Without fine-grain index, reads need to scan through the entire chunk. More chunks containing stale data are involved, if chunks host overlapping ranges. Ideally, if any data can be located accurately, scan is not even needed. Read amplification is possible to be __amortized by batching queries__, at a cost of latency.

  * __Write amplification__. To write a piece of data, how many extra writes needed in count and size? In-place update in an array can kick off ripple data movements if the slot is too small. Append-only systems trigger background writes for GC/compaction. Background jobs also do rewrites. Write amplification is possible to be __pushed off to offline__ from write path, at a cost of space amplification. Deletes can be treated as a special type of writes. Note extra reads can also accompany write amplification in data movement. 

  * __Space amplification__. Compared to only user data, how much extra storage space is spent at query tier? This includes unclaimed stale (or deleted) values, empty slots pre-allocated for inserts, internal fragmentation inside pages/chunks, external fragmentation that skips allocation. Space amplification can naively be reduced by GC/compact more frequently, at a cost of read/write amplification. Storage space goals are critical to Cloud Storage COGS which sells by capacity.

  * __Sequentialize reads__. HDD favors sequential reads. We want the next read hits a previous prefetch, multiple reads to batch in one bigger, and range queries to map to sequential on-disk scans. We want __data locality__ to be preserved for access pattern. 

  * __Sequentialize writes__. HDD/SSD favor sequential writes. Append-only systems sequentialize all writes. In-place update systems are harder, but possible with pre-allocated empty slots, or filesystem extents.

  * __Compression__. Compression is critical to storage efficiency at query tier. It also reduces amplification by transferring less data in reads/writes. Compression needs to work with encryption, where CBC (chained block cipher) can randomize identical blocks. Packing similar data together makes compression more efficient (e.g. columnar layout). Transfer overhead can be reduced by directly querying and passing compressed blocks ([late materialization](https://web.stanford.edu/class/cs245/win2020/readings/c-store-compression.pdf)). Queries become even more efficient with [SIMD vectorization and JIT compile](https://15721.courses.cs.cmu.edu/spring2020/papers/16-vectorization2/p2209-kersten.pdf). 

  * __Index lookup__. An ideal data layout should be easy for index lookup to serve reads or find write locations. Index structure and traversal can embed into data units, or data clustered into index. Given limited index size and granularity, data chunks can have a second level min-max sketching, zone maps, or bloomfilters. Data can also be compressed, support range query, without a separated index; see [Succinct data structures](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2019/EECS-2019-141.pdf).

Next, we define the __data unit__, e.g. how big a block is, chunks, files. We need to think properties are enforced at which level of data unit, indexing happens at which granularity, data placement & migration unit size, etc. Listing data units from small to big:

  * __Individual key-value__, or only value if the key can be derived, e.g. incremental row id in columnar layout. This is the smallest data unit. Usually indexing every key-value at this layer is prohibitively expensive.

  * __Row group__. A file can have multiple row groups. It may still be too small for indexing, but carries itself min-max sketching and aggregation statistics. The example is [Parquet](https://github.com/apache/parquet-format), or AnalyticDB row-column layout. A row group contains all columns for a set of rows, while inside the row group data is organized columnar.

  * __Chunk__. I use "Chunk" to universally donate the smallest data unit to index. An example is the "SST file" in RocksDB, where reads first locates a chunk (think of a "shabby" index here) and then full scan it (can be optimized by per row group sketching). Another example is the "page" in B+-tree index (such systems usually don't have row groups), where we need to consider record layout inside. The next example is the "block" in filesystems, which is indexed by inode trees; or "extents", where allocator assigns a larger space than asked, to append future writes.

  * __Partition__. The smallest unit to choose which server to host. It's where data starts to participant in a distributed system, and as the unit for placement, replication and migration.

  * __Data unit for classification__. Storage systems need to decide a data unit as the level for __tracking and classification__. Classification is a common problem in storage systems for efficient GC/compaction, temperature tiering, and various background jobs. __Machine Learning__ can but not much used mainly due to the metadata size and computation cost for vast tracking units. The unit of classification can either be bigger or much smaller than a partition, given the tracking cost willing to pay. 

    * __Generation__. I.e. the "level" in LSM-tree or RocksDB. It marks how many GC/compaction rounds the data has went through. It __classifies__ how likely the data won't be deleted/overwritten in future. LSM-tree couples more properties with generation, e.g. chunk size, sort runs, compaction strategies; which is a design choice but not a necessity. 

    * __Temperature tiering__. A tag with statistics to __classify__ how likely the data will be accessed in future with certain traffic. Efficient ways to offload cold data to cheaper storage media is critical for storage space efficiency, while quick response on sudden user reads yet needs the (asymmetric) data unit of transfer. Separating GC/compaction strategies between cold/hot is also beneficial.

    * __Workload streams__. The storage system is serving mixed user workloads. "Stream" here means to separate out the data operations from a single workload (e.g. single App, single content, single user). The concept came from [NVMe protocol](https://www.seagate.com/files/www-content/product-content/ssd-fam/nvme-ssd/nytro-xf1440-ssd/_shared/docs/an-introduction-to-nvme-tp690-1-1605us.pdf), and an example is [FStream](https://www.usenix.org/conference/fast18/presentation/rho). Practically, "stream" groups similar data together to yield better compression, dedup, to share close lifecycle in GC/compaction, and temperature. 

In the next level, we abstract the __properties__ of a data layout. They constraint the physical data organization intra/inter data units, to which writes pay to maintain, and reads benefit from to speedup. Below lists properties from small to big data units. They map properties to high level goals. Applying properties and trade off between them compose the design space for various techniques.

  * At key-value level, common techniques are to __separate keys and values__ (WiscKey). Most compaction happen at keys, thus saved rewrite amplification on values (which are big). Another technique is to __dedup common key prefixes__ which saves storage space. Examples are "column family" in HBase, trie trees, and Masstree.

  * At row group level, a notable property is whether data is stored in __columnar or row format__. OLTP database favors row format, where data is organized as rows, and row piles in a page. OLAP database favors columnar format, where data is organized as columns, values from one column is stored consecutively in a row group, and then to the next column. 

    * __Columnar format__. Since column packs similar data, compression is more efficient thus reduces storage space, and less read data when scan. Common OLTP workloads can hardly generate columnar format on start, thus need to pay write amplification for batch and rewrite. Querying one column and then lookup another column in one row, however incurs extra IOs and non-sequential reads, because columns are stored at different locations. Common columnar format examples are Parquet, Apache ORC. 

    * __Row format__. Scans involve unnecessary columns, i.e. a read amplification. Compression are less efficient compared to columnar format, and also cost read transfers. But updating/inserting can directly operate in unit of rows. Looking up all columns in one row costs only one read.

Continue with data layout __properties__. __At chunk level__, many properties are covered such as whether data is __sorted__ (or partially sorted), __overlapping__ between chunks, __cross chunk linking__, allowing __in-place updates__. They further couple with intra chunk or inter chunk. Much of LSM-tree compaction optimization is talking about this level. 

  * __Sorted, intra chunk__. Examples are RocksDB SST files, or column values in columnar format, which stores records sorted. Sorting favors lookups to locate the record, allows sequential reads in range queries, ease building external index or embedding index inside file. However, since user writes in any order, sorted data cannot be obtained from start, unless either buffer in memory, or pay write amplification for rewrite. Besides, sorted data enables more efficient compression algorithm, e.g. Run-length Encoding (RLE).

    * __In-place updates__. Maintaining both intra chunk sorted and in-place update is hard. Giving up internal sorting, sort property can be __pushed off to inter chunk level__, so that read amplification is still capped, and index at chunk granularity can still be built. To absorb inserts, a chunk can pay storage space to pre-allocate empty slots, or pay extra writes to move records elsewhere.

    * __Index sort order vs data sort order__. Databases records can appear to be sorted by index (e.g. traverse B+-tree in order), but random on-disk. Though a range query saves lookup by leveraging index sort order, on-disk scan still suffers from random reads. To align on-disk data in sort order, it can pay amplification for a rewrite. Or, let index leaf level have larger chunks for sequential reads inside, and then jump to the next chunk. However, secondary indexes can hardly achieve data sort order on secondary keys, while this can be compensated by [Z-Order](https://zhuanlan.zhihu.com/p/491256487) at a cost of read amplification.

  * __Sorted, inter chunks__. The example is ["tiering" vs "leveling"](https://zhuanlan.zhihu.com/p/112574579) in RocksDB. "Leveling" requires chunks are __non-overlapping__, i.e. a sorted run, or chunks have a total sort order. It favors read to quickly locate only one chunk that needs scan. However, maintaining the inter chunk sort property requires more eagerly paying writes in compaction. In "tiering", chunks can have __overlapping__ key ranges. Breaking "sorted" property relaxes writes, but read may need to scan multiple chunks.  

    * __Overlapping__. Can chunks have overlapping key ranges? This is another way to say whether inter chunk sort property is enforced.

    * __Partially sorted, inter chunks__. The example is "Guards" in PebblesDB. A guard contains multiple chunks which can overlap, but cross guards there is no overlapping. It creates a tunable balance between read/write amplification.

    * __Key assignment to chunks__ matters when maintaining the sort/overlapping property inter chunks. By partitioning keys into non-overlapping ranges (or hashing) and assigning to different chunks, it ensures chunks non-overlapping. You can see __data partitioning__ is not only for scaleout, but also a method to __separate conflict spaces__ that eases algorithm handling. Besides, it also __separates addressing space__, which reduces metadata size, as you see in [Metadata section](.). 

    * __Fixed/variable sized blocks__. For example, chunks of SST files are variable sized, database pages are fixed size, and storage system may either use fixed sized or variable sized blocks. Fixed size blocks are commonly seen in traditional filesystems, updated in-place, where size variety is however handled by allocator (which can be tricky to be robust). Internal fragmentation can waste space inside blocks.  Variable sized blocks favor append-only systems and compression which outputs unpredictable size. Index metadata has to be larger, as no fixed size of tracking units.  In balance of the two: 1) The system can take a __minimal write size__ e.g. 4KB, so index metadata size is reduced even for variable sized blocks. 2) Allocate by a large "extent" rather than individual blocks, so that inside the extent it can append fixed size blocks and reduce external fragmentation.

    * __Compensation by index__. Having an index can ease chunk maintenance. If the chunk means B+-tree index pages, it needs to maintain both non-overlapping and fixed size block property. This is done by __key assignment to chunks__ guarded by the index itself. With overlapping chunks, instead of scanning all matched ones, a global tree/hash index can tell whether certain key exists in a chunk, so as bloomfilters (which is commonly used). In a word, __index compensates read amplification__.

  * __Cross chunk linking__. The example is __Forwarding pointers__ in LSM-tree that level L-1 chunks can embed pointers to level L chunks. When a read scanned level L-1 but didn't find matching records, it can follow forwarding pointers to level L, which saves scanning startover. E.g. [REMIX LSM-tree](https://zhuanlan.zhihu.com/p/357024916). Essentially, the method is to __embed an index__ at inter chunk level. Note we also mentioned __indexing at chunk internal__, or a separate __external index__. Conceptually, index leverages __connections between data__ to build, this right happens when chunks have overlapping key ranges across LSM-tree levels.

  * __Data locality__. Data to be accessed together should be located physically close, so that a read can fetch all. This can happen at node/partition level to save cross networking, within same chunk/block to be cached as one unit, or aligned in neighbor records to benefit prefetch. An example is graph databases, where edges and vertices are accessed one by one in traversal order.

    * __[Data clustering & data skipping](https://zhuanlan.zhihu.com/p/354334895)__ as we can also call it. Data clustering means data frequently accessed together should be physically packed together, so they can be prefetched or returned in one sequential scan. It becomes tricky when trying to pack different DB table fields. An example is Z-Order. Data skipping is an opposite of data clustering that, it tries to skip as much unnecessary data during disk scan. It leverages the embedded sketching filters or indexes, and avoid clustering too much unrelated data.

Other data layout __properties__ at data unit levels of partition and classification:

  * __Partition level__. It maps to chunk level to serve individual queries. There are few other "larger scale" properties

    * __Replication__ and __placement__ affects how queries are served at distributed system level, but more proper to discuss at [Data partitioning section](.). __Colocation__ places data used together on same node to benefit prefetching and saves networking coordination cost.

    * __Interoperability__. Datalake, e.g. Delta Lake, uses open formats (Parquet, Apache ORC, JSON, CSV) for both its internal data, metadata, and transaction logs. This allows any other app to interoperate, and allows launching a new server anywhere else at cloud to resume processing.

  * __Classification level__. It maps to individual or a group of similar chunks as the tracking unit. The grouping can either be physical to locate chunks together, or logical to track similar chunks with metadata. 

We can summarize data layout __properties__ by exploring two extremes, a write-optimized layout and a read-optimized layout. We can tune properties to watch the transition between the two.

  * __Write-optimized layout__. Newly updated/inserted data are sequentially appended to the end of log without any special handling. Write path has the lowest cost.

  * __Read-optimized layout__. Chunks are fully indexed at key-value granularity. Chunks are internally sorted, non-overlapping, and large enough to avoid fragmented IOs from a range query. Columnar layout if not too many cross-column lookups. Fields frequently accessed together are packed close.

  * __Transition from write-optimized to read-optimized layout__. Applying various properties, we can observe three trends: 1) introduce sort order, 2) reduce tracking granularity, 3) group similar data together

    * __Introduce sort order__. A query needs to exploit sort order to locate data more quickly and skips unrelated ones. On-disk access also benefits from sequential reads. Sorting also benefits compression such as RLE. Chunk internal sort is usually done by a rewrite. Inter chunk sort can dial from loose to tight, by directing records through guards or index.

    * __Reduce tracking granularity__. The benefits come to indexing and skipping. With smaller granularity located and more unrelated data filtered out, queries save more reads. Metadata overhead is a trade off, where low level index parts / sketching / statistics can be embedded in chunks, rather than pinned in memory. Chunks can be cut smaller, with size more balanced, and embed variety at row group level.

    * __Group similar data together__. Examples are, separating keys and values, columnar format that groups values from a single column, generation or LSM-tree levels that group data by lifecycle, temperature tiering that groups cold/hot data, workload streams that group similar data from a single workload. Such classification, either based on type rules, statistics, or Machine Learning, are effectively useful everywhere, e.g. compression, scanning, GC/compaction, lifecycle related data movements.

More about optimized layouts

  * __Space-optimized layout__. Space amplification is important to Cloud Storage COGS but less attended. Write-optimized layout hurts space efficiency due to unclaimed stale values. Read-optimized layout hurts space efficiency, if it keeps internal fragmentation in pages, blocks, or pre-allocated empty slots. Efficient compression is also required. Space-optimized layout can be a columnar layout with closely packed records, which seems can be achieved together with read-optimized layout. If we accept rewrites, we also absorb newly ingested data by write-optimized layout.

  * __Balanced-optimized layout__. Considering the cost of GC/compaction, we can hardly achieve both write/read-optimized simultaneously. A balanced layout is worthwhile, and it is only __optimized__ when tailored against the target App workload. This is essentially a __Machine Learning__ problem, where [Optimal Column Layout](https://stratos.seas.harvard.edu/files/stratos/files/caspervldb2020.pdf) explored for in-place updates (binary linear optimization).

// TODO add a pic chart to link how properties connect to goals, and each concrete design pattern techniques

__Garbage collection (GC) / Compaction__

GC/compaction are common in append-only or LSM-tree systems and quite bandwidth consuming. Update in-place systems can also use compaction to generate read-optimized layout, and need GC if some new values are temporarily written out-of-place. I choose to mix the notation of GC/compaction because both reclaim stale/deleted values. Compaction can replace GC in LSM-tree, and GC can go without compaction if index/bloomfilter/versioning tell which key is stale.

Typical design __goals__ for effective GC/compaction are below. They map to the goals of data layout.

  * Be timely enough to reduce __read amplification__ incurred on user reads.

  * Be timely enough to reduce __space amplification__.

  * Pay less for __write amplification__ either inline in write path or offline in background jobs.

  * Arrange __sequential reads__ and __sequential writes__ when possible.

  * Spend reasonable amount of __CPU/memory/disk__. Less compete with user traffic or stall them.

The design space of GC/compaction consists of a series of "knobs" choosing when and how to run

  * __Size granularity__. How big is the data unit selected for GC/compaction? It can be an individual chunk, a group of chunks, or compact with all chunks in a LSM-tree sorted run or level. A chunk can either be configured small or large. Essentially, enforcing sort order on a wider range implies correspondingly larger compaction granularity, which benefits reads but is more costly to maintain. A large granularity costs less tracking metadata but incurs more rewrite on unnecessary data.

  * __Selecting candidates__. Which chunk to GC/compact with which other chunks. A GC/compaction run is more efficient if it removes the most stale values, or when chunks having more possible overlapping. A new chunk can also be pushed off to accumulate more stale values. Proper indexing and statistics tracking can be spent here. Selecting best candidates optimizes GC/compaction.

  * __When to trigger__. When to start run GC/compaction? It can be when storage space is filled up, certain LSM-tree level reached max size, a chunk accumulated enough old stale keys, periodical timer triggered, recent read/write cost reached alarm or stalled due to pending work, or user traffic is low enough. They target to proactively maintain system properties while minimally impact user activity.

  * __Where to run__. Traditionally GC/compaction need to run in local node to save network/disk transfer. However in shared storage, chunks can be loaded by other nodes to scaleout the computation. They can also have extra replicated copies to balance reads, or smart SSDs to compute in hardware. More, GC/compaction can store data in cloud storage (e.g. S3), disaggregate storage components (e.g. Snowflake), and offload computation to cloud (e.g. Remote Compaction).

Base on data unit for classification (mentioned previously), e.g. generation, temperature, workload streams, different GC/compaction strategies (the above) can be applied.

  * __Generation__. I.e. the level 0, 1, 2, .. N in LSM-tree or RocksDB. Each level is typically configured with different max sizes, chunk size, GC/compaction frequency. They can also use different tiering vs leveling strategy. An example is Lazy Leveling in Dostoevsky. Roughly, lower levels incurs more write amplification because they compact more frequently, while higher levels incur more read amplification because of scanning large chunks.

  * __Temperature tiering__. It's beneficial to delay hot data, keep them in memory, which then accumulate more stale values to GC/compact in one run. Cold data should be separated from hot data, to avoid polluting and forced to rewrite altogether. GC/compaction can run more infrequently on cold data because they have less activity. An example is [TRIAD](https://github.com/epfl-labos/TRIAD).

  * __Workload streams__. It groups data which have similar temperature hot/cold level. The correlated data with similar lifecycle are more likely to be deleted/updated together, so to be reclaimed in one GC/compaction run. The example is files in Google Drive, where a file is deleted as a whole, but mixing blocks from different files in one chunk results in fragmented lifecycle.

HyPer [Scalable MVCC GC paper](http://www.vldb.org/pvldb/vol13/p128-bottcher.pdf) also gives another similar categorization of GC designs (for DB MVCC versions): Tracking Level, Trigger Frequency, Version Storage, Identification of obsolete versions, Removal of garbage versions.

__Compression__

Columnar format organizes data in compressed way. The compression algorithms yet allow reading records directly without decompression. The below [algorithm selection taxonomy](https://www.cs.umd.edu/~abadi/talks/Column_Store_Tutorial_VLDB09.pdf) not only reflects common properties in data, but also data organization in compression to query efficiently.

![What compression schema to use in columnar format](/images/arch-design-columnar-compress-taxonomy.png "What compression schema to use in columnar format")

The above is categorized as "Columnar compression". There are more compression algorithm families available for storage systems. They can be categorized as below

  * __Block based compression__. The classic daily used compression algorithm. [LZ77](https://www.youtube.com/watch?v=jVcTrBjI-eE) is the heart of most of them: ZIP, LZ4, LZ* family, GZIP, DEFLAT, 7-ZIP, RAR, Zstd. LZ77 does dedup, where text tokens pointing to each other virtually composes a dictionary. LZ77 is usually used with an [Anti-entropy stage](https://stackoverflow.com/questions/55547113/why-to-combine-huffman-and-lz77) to further shorten bit representation, see "Anti-entropy compression".

  * __Explicit dictionary based compression__. DB compressing string values can specialize to use algorithms like [FSST string symbol table](https://www.vldb.org/pvldb/vol13/p2649-boncz.pdf), whose core is a lookup dictionary. Zstd also provides a [dictionary mode](https://ayende.com/blog/189954-A/random-access-compression-and-zstd), where a pre-trained dictionary can be supplied to compress small documents.

  * __Succinct data structures__. We mentioned it before. Besides, [LZ-End](https://users.dcc.uchile.cl/~gnavarro/ps/dcc10.1.pdf) is an interesting algorithm recognized in research. It slightly modifies LZ77 to support random access without block decompression, but yet needs a few extra lookups with address jumps.

  * __Columnar compression__. Columnar DB uses it to compress columns. These family of algorithms are shown in the above taxonomy picture. Such compression assumes column data shares similarity. They typically support index point lookup, scan, query filtering, without decompression (Late Materialization). 

  * __Anti-entropy compression__. As used along with LZ77 family, the algorithms select bit representation for entries according to their frequency, so that the total bit length is shorter. E.g. Zstd uses LZ77 + [FiniteStateEntropy](https://github.com/Cyan4973/FiniteStateEntropy).


### Data indexing

Data indexes commonly reside in memory (i.e. DRAM) and forward links to data. Though residing in PMEM is possible but by far it's still slower than DRAM. Data indexes stem from standard textbook data structures, evolve into more complexity for industrial use, and scaleout in distributed systems. They serve read queries, point where to write, and carry a cost to maintain consistency with data.

__Data index properties__

We can summarize common properties in data indexes. They compose the design space and various techniques available

  * __Structure__. A data index typically has a base structure, i.e. trees, hashtable, lists.

  * __Sort order__. Examples are tree vs hashtable. Tree-based index commonly maintain the ordering between data, which enables range query. Hashtable is known by O(1) lookup time, but global ordering is lost. Though tree-based index can hardly simultaneously preserve the ordering on secondary keys, and hashtable can track ordering by maintaining a tree-index altogether. In another word, __combining multiple indexes__ together is a way to join read properties, at a cost on updates. 

  * __Point lookup__. All data indexes support point lookup, typically ranging time cost from O(1) to O(log(n)). Essentially, there is a trade off with memory size: 1) If entire key space can be put in memory, we simply need a huge array to map any key to its value. 2) Hashtable collapses the mapping space, with hash as the mapping kernel, thus smaller memory size needed. The new space has to be sparse enough, due to the unpredictable degree of balance in the mapping (unless [perfect hashing](https://en.wikipedia.org/wiki/Perfect_hash_function)). 3) Coming to trees, keys are indexed by inter connections, rather than address mapping, thus yet more smaller memory size needed. 

  * __Range query__. Data indexes that preserve sort order can support range query, typically trees. Otherwise it has to be a full scan, unless applying guard/segmentation to preserve partially sorted, where skiplist can be seen as an example. Another way to understand range query is that a data index must support looking up a key's neighbors, even the key itself doesn't exist.

  * __Update/insert/deletion cost__. An index is essentially a constraint on how data is organized, which implies cost must be spent in write path to maintain such constraint structure. Linked structures are easier to insert, while packed arrays have to move data if no empty slots left. Besides, a second extra cost can be spent in/off the write path to: 1) Rebalance data structure to reduce tail latency (E.g. Red-back tree rotates). 2) Handling addressing conflicts (e.g. hashtable). 3) Space expansion or shrink (e.g. expand 2x array size when hashtable is full, or shrink likewise). 4) Garbage Collection / GC (e.g. epoch-based memory reclamation) 5) Compact deltas (e.g. Bw-tree page deltas).

  * __Read-only__. Some data indexes, e.g. [SuRF](https://db.cs.cmu.edu/papers/2018/mod601-zhangA-hm.pdf), doesn't support updates except of a total rewrite or very expensive operations. Such indexes can be packed in consecutive arrays, highly compressed to favor memory size; and with delicate interleaving to speedup (range) queries. 

  * __Sequential reads__. Are the memory access more sequential when jumping to lookup keys, when neighbor keys are accessed next, and when scanning range queries? This affects CPU cache efficiency, where tree-based index commonly does better than hashtables. Another dimension is on-disk sequential reads, if the index has on-disk components.

  * __Sequential writes__. Are writing data on disk follow sequential access? A typical example is B+-tree vs Be-tree. Be-tree buffers small writes in middles nodes to flush to disk sequentially. Even append-only logs can be used to buffer updates for DRAM indexes to flush them in sequential batch. LSM-tree can be seen as another type of index to achieve append-only sequential writes to disk.

  * __Cache affinity__. How efficient to CPU cache when the data index is accessed? Common measures are cache miss, IPC (instruction per cycle), branch prediction misses, pipeline stall, memory waits, and memory writes (vs in CPU register). Typical techniques include: 1) Embed pointers in data struct, rather than using an explicit node struct. 2) Pack data structures to align with cache line. 3) Avoid false sharing. 4) Exploit sequential data structures. 

  * __Index memory size__. How much memory is need by the data index, or commonly the metadata size of a data storage. Tree-based indexes suffer from cross node pointer size, and intra node fragmentation. Hashtables however needs to leave empty slots to avoid conflicts. An example is ART tree that tailors smaller node size when less occupied. Other techniques are: 1) Pointer swizzling that packs data into tail bits of pointer. 2) Replace pointer to shorter bits IDs according to max record count. 3) Data partitioning to reduce address space thus reduces pointer size. More effective ways are decouple and scaleout, see [Metadata section](.).

  * __Concurrency__. Examples are [lock coupling](https://15721.courses.cs.cmu.edu/spring2016/papers/a16-graefe.pdf) in B+-tree, per inode logs in NOVA, and page deltas in Bw-tree. Common techniques are: 1) More efficient share/intent/exclusive locking protocol, smaller lock granularity and duration. 2) Data partitioning so multiple locks can work in parallel. 3) Lock-free data structures, but need careful design for high race conditions. 4) Symmetric parallel copies (同态多副本), i.e. to shard the space into non-interleaving but identical processing flows, e.g. one thread per disk doesn't even need locking, e.g. requests targeting different files.

  * __Compression__. Keys can dedup common prefixes to save memory size, e.g. trie tree or Masstree. Nodes having few children can be merged to one (path compression). Less occupied nodes can trim its container size (e.g. ART tree). Big B+-tree node can also compress its contents. Cold pages can even employ memory compression or offload to disk. Succinct data structures compress data, and provide same ability for search and range query, without needing a separated index.

  * __Fuzziness__. Data indexes may return false positives, e.g. Bloomfilter, SuRF. Allowing inaccurate results enables new family of highly memory-efficient indexes. They can also be seen as [sketch structures](https://dsf.berkeley.edu/cs286/papers/synopses-fntdb2012.pdf), e.g. min-max sketching, zone maps commonly used in DB data chunks. 

  * __Data clustering__. Like index can be embedded in data chunks as forward pointers, data can also be [clustered into index](https://docs.microsoft.com/en-us/sql/relational-databases/indexes/clustered-and-nonclustered-indexes-described?view=sql-server-ver15). This means data reads has one less fetch after traversed the index, and data is aligned with index physical order. "Clustered index" is a database term.

  * __Disk components__. There are two dimensions 1) Are the working parts of the index exclusively reside in memory? 2) How the index is recovered from disk to memory after node restart.

    * __Disk working parts__. A common hashtable, skiplist, ART tree resides only in memory. However, B+-tree has lower level pages resides on disk and load to memory on demand. Bw-tree can also flush page deltas to disk and track with linking pointers. In general, the disk transfer unit is page.  But the problem can be thought in another way: Which working part of the index resides in CPU cache, and which in memory? Because cache hardware hides most complexity, the discussion falls into CPU cache efficiency and multi-core concurrency. 

    * __Disk recovery__. A naive approach is to log every operation on the index to disk in append-only fashion. However, replaying (days of) full logs on restart is way too slow. The second approach is to keep a short term of log and periodically flush checkpoints to disk. This is what LSM-tree does. The approach also comes to B+-tree and databases, where pages are synced to disk on demand (also known as checkpointing but not requiring one full flush) and recovery follows more delicate ARIES protocol.    

__Popular data indexes__

There are quite a few well-encapsulated data indexes widely used in industry. Below briefly lists them. They are reference architectures and source of techniques. Optimization matters in data indexes.

  * __Hashtables__. Plain old hashtable is yet useful in DRAM indexing, PMEM, and database hash indexes. Hashtables vary when address conflicts, how to choose the next address, and how to add conflicting keys. The second level container for conflicting keys also worth optimization. Hashtable can simultaneously use one, two, or several different hash algorithms, and target them to App level knowledge. Smooth capacity expansion and shrink is another optimization point. Data partitioning helps reduce conflict space and shorten address pointers (e.g. Kangaroo).

    * Popular hashtables are [Cuckoo hashing](https://en.wikipedia.org/wiki/Cuckoo_hashing) that bounces between two hashtables, [HotRing](https://www.usenix.org/system/files/fast20-chen_jiqiang.pdf) that switches hot keys to front, [Consistent Hashing](https://medium.com/system-design-blog/consistent-hashing-b9134c8a9062) and Ceph CRUSH map, Level Hashing. 

    * Particularly, Consistent Hashing suffers from load imbalance if a server went offline, and its keys are assigned to the immediate next server on the ring. The issue can be relieved if each server has multiple points on the Consistent Hash ring.

  * __[Skiplist](https://en.wikipedia.org/wiki/Skip_list)__ is first a list structure that preserves data sort order. To speedup lookups, it adds several layers of new lists, each with increasing sparseness by skipping more keys. Essentially, it's like a tree but nodes linked horizontally. They data index is used in Redis and RocksDB, known for its simplicity and performance at high concurrency. In another way, a list packed in consecutive memory can also be useful to index small amounts of data, where sort order is preserved, and lookup uses binary search. An example is values packed in a B+-tree node.

  * __[Radix tree](https://en.wikipedia.org/wiki/Radix_tree)__ is used in Linux Kernel [memory management](https://lwn.net/Articles/175432/), and NFS and NOVA inode indexing. Radix tree is a trie tree that compressed paths to the most, so that each node's children count maps to the variety (i.e. radix) of the next level data. It can also be seen as a fragmented array, where the big consecutive array is broken into a few smaller segments, and these segments are indexed by another smaller array at the next level in the tree.

  * __[Red-back tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree)__ is the standard implementation of C++ ordered map. It's a binary search tree, self-balanced with efficient rotation, yet not too strict to hurt update performance (rather than [AVL tree](https://stackoverflow.com/questions/5288320/why-is-stdmap-implemented-as-a-red-black-tree)). 

    * Unlike C++, Rust instead implements ordered map [with B-tree](https://www.zhihu.com/question/516912481). This is because the binary structure of Red-back tree jumps too many times to hurt CPU cache efficiency, while B+-tree has less levels and a big node to favor CPU cache. B+-tree has another [discussion](https://github.com/rust-lang/rust/issues/27090).

  * __B+-tree__. The plain old database index, but still proven widely useful in storage, PMEM, caching. B+-tree balances itself, uses packed big nodes to limit tree height which maps to disk reads, and preserves sort order with traversal links. B+-tree works entirely in pages, which simplifies disk data transfer in DB and memory management. B+-tree shares various optimization for access efficiency, storage space, and locking concurrency.

    * __[Steal, no force]__. The terms came from [ARIES](https://cs.stanford.edu/people/chrismre/cs345/rl/aries.pdf) protocol for DB transaction recovery ([well explained here](https://zhuanlan.zhihu.com/p/143173278)). They work with DB page syncs between memory and disk. "Steal" allows DB to flush pages of uncommitted transaction to disk, thus introduced the need of undo log. "No force" allows DB to NOT flush pages of committed transaction to disk, thus needs redo log from failure recovery. Not only do "steal, no force" improve DB performance on large transactions, they enable DB buffer management to become a decoupled component from transaction and indexing. 

    * __[B+-tree locking techniques](https://15721.courses.cs.cmu.edu/spring2017/papers/06-latching/a16-graefe.pdf)__ separated DB concepts "latch" (for data structure) vs "lock" (for transaction). It introduced the widely used technique "lock coupling". The concurrency design space in B+-tree ranges from: 1) SIX locks which introduced intent locks that softly drain on-going writes, 2) lock coupling that steps through parent/child with limited lock span, 3) Blink/OLFIT tree that supports version-based OCC lock-free reads and locked writes, 4) Bw-tree that is lock-free and delta page append-only ([well explained here](http://mysql.taobao.org/monthly/2018/09/01/)).

  * Popular data indexes for in-memory databases and PMEM. They essentially stem from B+-tree, and are frequently found in papers and industry products. Since they are already covered in [Reference architectures in storage areas](.), here does a brief walkthrough.

    * __ART tree__. is used in HyPer in-memory database. It is built from a radix tree, dedup key prefix like trie tree, and made space efficient by adapting node sizes to several different record counts. The node is essentially a fixed length array. Leaf nodes can store values inline. Path compression is carried out to nodes with a single child. ART tree supports range queries.

    * __Masstree__ collectively applied many optimization techniques on B+-tree. Trie tree is employed to dedup common key prefixes. The next-to-access nodes are prefetched from DRAM to CPU cache in overlapped pipeline. Operations can carry out concurrently at tree nodes, while read is version-based OCC lock-free, and writes hold a lock. More fine-grain optimizations can be found in Masstree paper.

    * __Bw-tree__ is a lock-free B+-tree variant used in Hekaton and DocumentDB. It appends page delta, which then needs compaction and epoch-based memory reclamation. It employs a Page Mapping Table to avoid recursive propagating COW page updates up to root. The Page Mapping Table also enables many atomic operations that need to switch page pointers. The Bw-tree page deltas can be incrementally flushed to disk, which makes it comparable to the append-only LSM-tree that buffers and sequentialize writes.

    * __Be-tree__ is a B+-tree variant to reduce random writes compared to LSM-tree. Compared to B+-tree, small writes are buffered in nodes, and flushed to lower levels when full. In this way, small writes are batched and disk writes are mostly sequentialized. While compared to LSM-tree, Be-tree still maintains the B+-tree structure in data organization to supports optimal read performance.

  * Other types of indexes. Below a few are handy at special usecases. 

    * __[Bitmap index](https://www.oracle.com/technical-resources/articles/sharma-indexes.html)__ is used in databases. Compared to B+-tree, it becomes applicable when a column has low cardinality (count of distinct values). It works in the same way with [bit-vector compression](https://www.cs.umd.edu/~abadi/talks/Column_Store_Tutorial_VLDB09.pdf#page=52) in columnar layout.

    * __[Inverted index](https://codingexplained.com/coding/elasticsearch/understanding-the-inverted-index-in-elasticsearch)__ is used in full-text search engine, e.g. Lucene, ElasticSearch, to lookup documents by words. Weights of words can be evaluated via [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) score. Weights of pages or documents can be evaluated by [PageRank algorithm](https://en.wikipedia.org/wiki/PageRank), known from Google, while PageRank is the [eigenvector](https://blog.csdn.net/sdgihshdv/article/details/77340966) of the page link matrix. Inverted index becomes wider adopted in databases because more started to support full-text search. 

__Data indexes in distributed storage__

We discuss a few secondary topics here about data index

  * __How a data index can scaleout in a distributed system?__ Typically, a tree-based index can host top levels in a Consistent Core, and naturally scaleout bottom levels across cluster. Hashtables and list-based indexes can scaleout with data partitioning on value ranges.

  * __How to maintain index consistency with data updates?__ We already discussed this in [Consistency section](.). Essentially, it needs a distributed transaction interleaving data and index. If the index is partitioned and exclusively co-located with data on the same node, a local transaction is enough. The index can also receive data updates in an eventual consistent way, while versions can guide users about the propagating progress and snapshot isolation. A third alternative builds full index for old data, while new incremental delta data runs without index or a cheap index. Typically, the index can be implemented as another plain database table to reuse data structure and transaction.

  * __How to build secondary indexes?__ We mentioned a few secondary indexes in Reference architectures, which agree on eventual consistency. A typical database can support secondary indexes by paying transaction cost with data updates. On distributed storage, there are yet two categories of secondary indexes

    * __Global secondary index__ builds index on the global space of the secondary key. It needs a distributed transaction to update consistently. However, if treating it as a plain database table, reusing the code is easy.

    * __Local secondary index__ builds an index locally on each data node. Per index only covers the local space, while different data nodes can have overlapping secondary keys but not known by the index. The index only needs a local transaction to consistently update with local data. However, looking up a secondary key needs to query all data nodes. Running parallel queries may not be that bad, considering there are also databases who choose hash partitioning per row. A node can skip query if its bloomfilter tells the key doesn't exist.

__Succinct data structures__

Succinct represents a family of data compression algorithms with interesting "__self-indexing__" property. See below. I add a special section for it. They quite match the usecase for DNA indexing & searching. They can also be used for in-memory indexing, and compressing in-memory data while supporting DB queries.

  * The compressed size is [close to the entropy limit](https://en.wikipedia.org/wiki/Succinct_data_structure). I.e. the compression ratio is near the classic block-based compression.

  * Supports point/range query, and especially text search, __in-place__ on the compressed data. There is NO separated index, but the performance is close to using an index, much faster than a full scan. Supporting text search is handy for DNA sequencing.

    * I.e. Succinct can be used to replace in-memory index, especially a secondary index. Besides, succinct also compresses your data.

  * Querying/lookup in Succinct data structure usually involves several address jumps in its internal data structure (e.g. Compressed Suffix Array). This is OK for in-memory indexing/compression, but may not be as handy for on-disk data compression. Besides, sequential read throughput / reading a large block may also be a concern.

  * Succinct data structure is usually slow to build, compared to classic block-based compression. Once built, it is usually hard to modify. Though supporting various queries, succinct data structure can be slow for sequential scan.

    * In column-oriented DB, common columnar compression algorithms (e.g. RLE) make powerful alternatives to Succinct data structure. Columnar compression algorithms also support directly executing DB queries. They are also easier and faster to modify. They get much wider adopted in DB.

There are a few most commonly used Succinct data structures

  * [FM-index](https://www.youtube.com/watch?v=kvVGj5V65io) is one popular and versatile succinct data structure. It is based on [Burrows-Wheeler Transform](https://www.youtube.com/watch?v=4n7NPk5lwbI) (BWT). How it works is close to CSA.

  * [Compressed Suffix Array](https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/agarwal) (CSA) is built from a different knowledge set. But it eventually converges to a very similar data structure like FM-index and BWT. Essentially, it tracks the suffixes of the input string and sort them. Tail char and prev char are extracted from each suffix, and sufficient to rebuild the original input string. The chars extracted are sorted, thus can be efficiently compressed. Text search is based on matching these chars. When point lookup needs address offsets, CSA needs to store them, but uses sampling to reduce the storage overhead.

  * [Succinct Trie](https://www.cs.cmu.edu/~huanche1/publications/surf_paper.pdf) is a Trie Tree encoded in bits. Rank & Select primitives are used to traverse tree parents/children. The primitives can be optimized to execute faster. Succinct Trie is typically used as a compressed index.

There are several notable adoptions of Succinct data structures

  * Compressed index in [TerakaDB/ToplingDB](https://www.zhihu.com/question/46787984/answer/103639893). ToplingDB uses Succinct Trie (CO-Index) to index RocksDB keys, while on-disk data is compressed by PA-ZIP. PA-ZIP supports random access to compressed data, without decompressing the entire block. PA-ZIP is not using succinct. 

  * [Spark RDD](https://databricks.com/blog/2015/11/10/succinct-spark-from-amplab-queries-on-compressed-rdds.html) added an Succinct based implementation. It is compressed, and supports text search and text occurrence count. It published [GitHub AMPLab/Succinct](https://github.com/amplab/succinct) and a [SuccinctStore paper](https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/agarwal). 

  * [GitHub simongog/sdsl-lite](https://github.com/simongog/sdsl-lite) is an well-known opensource implementation for succinct data structures. The implementation is efficient and is mostly used for researching. 

  * DNA sequencing. Searching a sub-sequence in a huge compressed DNA database is handy, and right matches what Succinct does. See an [example paper](https://academic.oup.com/bioinformatics/article/27/21/2979/217176?view=extract). [LZ-End](https://drops.dagstuhl.de/opus/volltexte/2017/7847/pdf/LIPIcs-ESA-2017-53.pdf) is also a well-known algorithm.


### Data caching

Data caching resolves the performance tier in data organization. It exploits the skewness of data hotness and temporal access locality, to trade off expensive small capacity storage media with fast access. Internet services commonly heavily leverage cache (e.g. Redis) to serve most user data. We first plot the design space of data caching by categorizing its different properties.

  * __Storage media__. The dominating caching device is __DRAM__, e.g. Redis, Memcached, which layers atop slow disk accesses. Later, __SSD__ is integrated into caching device to exploit larger capacity, warm cache restart, and its speed compared to HDD. __PMEM__ is recent and mostly used for writing staging, offload cold memory, or as fast persistent storage of Filesystems and DBs. At cloud-native scenarios e.g. Snowflake, __Ephemeral HDD__ in local VM is used to cache computed results fetched from remote S3.

  * __Durability semantics__. Commonly, cache is a __duplicate of data__ persisted elsewhere, where losing cache has no impact to durability. __Cache tiering__ (e.g. in Ceph) however requires cache is persistent, that 1 replica of the 3-replica is migrated to cache, and leaves the other 2 replicas in slow storage (e.g. HDD, ECed). __Write staging__ also requires persistence, while it's used to absorb recent writes, dedup and sequentialize them, and to cache recent data for following reads. __Memory buffer__ is common in programming that data needs to load from disk into memory before processing. It is volatile. It's also used in Stream Processing to buffer and composing middle results (e.g. in an Redis server), where durability can be enhanced with [RDD](https://spark.apache.org/docs/latest/rdd-programming-guide.html).

  * __What to cache and the granularity__. From small units to bigger ones. Storage/DBs typically cache __blocks__ and __pages__. Memcached caches __key-value pairs__, while Redis caches __data structures__ e.g. lists, sets, maps. Tiering systems can move larger __chunks__ or __files__. DBs can also cache more semantically, i.e. __table rows__ which contains more density of user data than raw blocks, __query results__, or __materialized views__ which caches data as well as computation efforts. __Query optimizer results__ can also be cached, where parameterized query common. __In-memory DB__ can be seen as caching for an entire DB level.

  * __Where to host the cache__. To use a separated system, offload to another server node, run in another process, or embed into the local App.

__Memory caching__

Caching data in memory is essentially how to manage data with DRAM indexing. We mentioned that in [Data indexing](.) section. Typical data structures are hashtables and trees. Additionally, memory compression and cold offloading can be employed to enlarge the capacity. There are a few design properties to consider. We recap here while they are also valid for SSD caching.

  * __Cache partition & replication__. Scaleout cache via hashing partitioning is common. But it can be capped by IOPS if clients have to split requests. E.g. an originally large request has to split into two small requests, because the queried keys are hash mapped to two servers. Replication comes valid here to scatter load for small pieces of very hot data. It's also used to save cross-region lookup. __Load balancing__ can be done via partition/replicating, while hot/cold rebalancing migration is usually not necessary because cache is volatile.

  * __Cache warmup__. A newly restarted cache node needs to run a while to fill with warm data. A cold restart can impact performance of systems which heavily rely on caching. For a warm restart, a cache process can offload data to disk before exit, backfill from other cache nodes, or let a shared process to temporarily keep its memory while being restarted.

  * __Item eviction__. The methods are shared with storage temperature tiering, which have already been mentioned in [Write path section](.). Additionally, cache can be designed to never evict until a new item comes in full. __Cascaded expire or invalidation__ should be avoided that, a large swarm of cache item eviction can burst miss rate and impacts latency.

  * __Propagating updates and invalidation__. Updates and invalidation are necessary to keep cache consistent with the underlying persistent store. However, with N cache nodes and M App nodes, an N\*M connection count is unwise. An mediator module or a central coalescing messaging queue can be introduced. Cache can also subscribe DB change logs to update itself (shared logging system).

Managing consistency between cache and persistent store has several approaches. Facebook Memcached/TAO papers had rich discussion.

  * For __read consistency__, a typical method is __cache aside__. App first reads from DB and then puts item in cache. App is responsible to invalidate cache item when updating DB. A small period of stale reads from cache is tolerable. Cross region cache consistency can be achieved by primary secondary replication, and a sequential ordering of update and invalidation. Facing with cross region lag, a user can request to see its latest updates via casual consistency, which can be implemented with version tracking in cache items.

  * For __write consistency__, the same typical method is the above __cache aside__, or call it __[write through](https://www.zhihu.com/question/319817091)__. Cache can also totally hides the backing persistent store, that it will take all writes and guarantee durability (e.g. write staging, or proxy). When a staging cache writes back to the persistent store, __write ordering__ needs to be considered. An anti-example is, journal commit is flushed earlier than journal data.

  * For __multi-key consistency__, the problem decouples into atomic writes and atomic reads. Both can be enhanced by tagging versions with cache items, detect inconsistency and apply mitigation. A key difference to persistent storage is, cache is OK to be __inconsistent first then detect and fix__, while persistent storage must guarantee data consistency.

__SSD caching__

SSD cache also uses DRAM as the first level cache and offloads cold data to SSD. DRAM index is typically hashtable or B+-trees. New challenges come from managing larger index size brought by the larger capacity of SSD, handling SSD rewrites and garbage collection, managing item eviction on SSD, and managing SSD wearing out issue. They are a few design properties.

  * __SSD cache structure__. __Set-associative cache__ is one approach, e.g. Flashcache and KSet in Kangaroo. Set-associative cache limits the freedom of item location into a cache line, thus needs little memory to host index (same level as a hashtable). __Append-only storage__, e.g. BCache and KLog in Kangaroo. Cache items are sequentially appended to disk, and organized in a larger bucket as the unit of GC. __Key-value stores__, e.g. to use RocksDB to manage SSD data. However, RocksDB is not designed to use as cache, disk point lookup has no index, and deleted space is released too slow after many levels of compaction. Cache has a second key difference to persistent store that is, __deletion is much more frequent__.

  * __Managing index size__. While a plain method is to set __a larger page size__, cache items can be divided into __small objects and large objects__, e.g. Kangaroo. Large objects have fewer count thus can use full DRAM index. Small objects assign most SSD capacity to __set-associative cache__ which incurs little index memory. It overlays a more efficient __append-only storage__ to favor batching, which uses __limited SSD capacity__ thus small DRAM index size. Further __metadata size reduction__ techniques such as "Partitioned Index" can be applied. __Bloomfilter__ is another memory-efficient technique to tell whether an item exists on disk. 

  * __SSD garbage collection__. __Set-associative cache__ has huge write amplification. A cache line is set to be __aligned with the flash page__. Overwriting a cache item needs to rewrite the entire cache line (i.e. flash page). __Append-only storage__ generally follows the common GC techniques. Buckets composes the resource throttling unit, and high garbage buckets can be picked first. __Item eviction__ is same with what we mentioned before, where memory size needs compact. Note that a flash cache line can merge eviction and insert into one rewrite, i.e. __never evict without insert__.

  * __SSD wearing out__. When used as cache, SSD inherently suffers from more __severe wearing out__. It is the third key difference to persistent storage. This is because cache capacity is much smaller than the underlying persistent store, but cache has to flow through most new writes, and yet to flow more due to periodical data hot/cold shifts. Mitigations can be to prevent cold data from flowing through cache, and to avoid churn by using enough capacity to host a hot/cold cycle.

__Metadata caching__

This section focuses on caching data, but we also briefly mention metadata caching.

  * Metadata is usually served fully in-memory in a Consistent Core (or partitioned, or disaggregated nodes). A client can directly ask the Consistent Core rather than requiring another cache service. Besides, the size of metadata is usually much smaller than data.

  * The propagating of metadata usually leverages piggybacked requests, gossip protocol, and a direct refresh request to the Consistent Core. Client typically caches what it needs in the local memory, with an expire or version checking policy.

  * Secondary indexes of data can be seen as a type of metadata. Per implementation, they are usually treated as plain data or tables, that share the same caching facility as mentioned in prior sections. As index, they may set higher priority to pin in memory.


### Data partitioning & placement

Data partitioning is the fundamental paradigm to __scaleout__ data serving in a distributed system. It has more design properties, that many also resemble those in [Data organization section](.), where you can find partitioning across nodes is like co-locating data in chunks. Data sharding is mostly a synonym of data partitioning.

  * __Scaleout__. Data partition maps data space to partitions, so that each partition can be served on a different node to scaleout system capacity. The system is __dynamic__, that an individual partition will grow or shrink in size or hotness, which yet introduced the needs to __split or merge partitions__.

  * __Access locality__. Data accessed together should be put into a single partition. E.g. a partition includes consecutive data ranges and preserves __sort order__ to favor range query. E.g. different tables frequently grouped in one __transaction__ are co-located in one partition. E.g. A partition includes different objects or table columns that are __frequently accessed together__. E.g. a single object can be __broken into different components__, that each partitioned differently according to access patterns. Access patterns are __dynamic__, which means either partition or placement need to change by time. Finding the best partitioning can either act greedily on recent metrics, or by __Machine Learning__ optimizing on history behaviors. 

  * __Granularity of units__. Partition can be small for fine-grained scheduling, and still preserve locality by __co-locating__ multiple partitions on one node. However more metadata can be paid as growth of data volume. Existing partition granularity can also be __adaptive__ to future growth/shrink by employing merge/split. However, a hash-based partitioning needs careful deign to avoid excessive data migration. 

  * __Balance of capacity__. How to ensure each node receives similar data capacity? Either this is achieved by equalizing data partitioning, or to rely on balancing data placement. Partition growth/shrink in size further introduces needs to manage merge/split and migration.

  * __Balance of hot/cold__. How to ensure each node receives similar IOPS/throughput? Hotness is the second dimension other than capacity that requires balancing. The balancing is either embedded in data partitioning level, or rely on data placement. Adaptive data migration is needed to deal with future traffic pattern change.

  * __Shuffle__. Computation may need a different partition key compared to the existing one. This happens frequently in MapReduce/Spark pipeline that data needs to be aggregated by a different partition key, and in database join operating not on primary keys. Usually the solution is __reshuffle__ that sends data via new key, or sometime a small table can be completely replicated to each destination.

Data placement is the next step that decides which node to place a partition. Usually data partitioning and placement are joined together to solve the above design properties. Data placement has more design properties.

  * __Data migration__. The first source of migration is balancing, that comes from the asymmetric growth of capacity, change of hotness, change of access locality. Another source is nodes join or exit, that empty nodes need fill up and dead nodes need to place data elsewhere. Hash-based placement usually needs careful design to avoid excessive data migration. The topic is closely related to __load balancing__, while __resource scheduling__ more focuses on placing jobs with multiple dimensions of constraints such as CPU, memory, IO, latency.

  * __Metadata size__. It helps balancing and reduce migration to allow full freedom of object placement, and to have a fine-grained tracking unit. However, both requires spending more metadata size. Metadata itself can also be partitioned and scaleout, see [Metadata section](.).

  * __Failure domains__. Co-related data, e.g. 3-replica or EC symbols, needs to avoid placed into the same failure domain. Failure domain hierarchically consists of disk, node, TOR, datacenter row, T2 switch, and region DNS. Upgrading schedule adds another layer of failure domain. 

__Common techniques__

Common data partitioning techniques for key-value structures are hash and range based partitioning. It gets more flexibility for Filesystem inode trees, and graph vertices/edges. Data partition & placement techniques closely relate to [Metadata section](.).

  * __Ranges__. Frequently seen in DB to support range query, e.g. CockroachDB, HBase. A table is horizontally partitioned by consecutive row key ranges. Ranges are usually dynamically managed by split/merge. A table can additionally vertically partition by columns frequently accessed together.

  * __VNode__. Keys are hash mapped to buckets called "VNodes". VNodes are the input for further placement. Compared to directly placing each key, VNode reduces the granularity of tracking, and balances hot/cold. The number of VNodes in a system is usually pre-configured, hard to change. We mentioned VNode before.

    * __Hash partitioning__ Databases, e.g. YugabyteDB, can support hash partitioning. Each partition is like a VNode. Rows are assigned to them via row key hash mapping. A distributed Memcached can also scaleout by hash partitioning. While hashing automatically balances hotness across nodes, IOPS can be significantly increased as a range query involves all nodes.

  * __Filesystem inode trees__. Like range vs hash, trees can also be partitioned by sub-structure vs hash randomness.

    * __Subtree__ based. E.g. CephFS features in "dynamic subtree partitioning", that an entire subtree can be migrated to different MDS nodes according to hotness. Subtree based partitioning preserves access locality but is prune to hotness skew. When accessing a deep FS path, each middle node is subject to a metadata fetch, where Subtree partitioning helps localize all them in one node. 

    * __Hash__ based. E.g. HopsFS partitions inodes by parent inode ID to localize operations of `dir` commands. Hashing favors load balancing but breaks access locality.

    * __Break into different components__. E.g. [InfiniFS](https://zhuanlan.zhihu.com/p/492210459). Inode metadata is decoupled into access attributes and content attributes. Each has different access locality, thus each is partitioned differently. The method enhances locality for hash based partitioning.

  * __Graph partitioning__ is challenging because inter-connections between graph components are irregular. Besides, computation on graph usually can hardly be localized to partitions, e.g. Deep Learning needs Parameter Server.

    * __Hash/range partitioning__. E.g. FaRM A1 applies hash partitioning to favor randomness. E.g. Facebook TAO is backed by MySQL and assigned a shard_id for partitioning. Adjacent edges are packed to their vertices due to always accessed together.

    * __[Clique](https://en.wikipedia.org/wiki/Clique_(graph_theory))__ identifies a group of vertices that have dense internal communication but sparse outside. Facebook Taiji partitions data via [Social Hashing](https://blog.acolyer.org/2019/11/15/facebook-taiji/), i.e. to partition by groups of friends, geo domains, organization units, etc. Expensive partitioning can be calculated offline via Machine Learning.

    * __Replication__. E.g. Facebook TAO. Some partitions can be frequently needed by computations happened in other partitions. The traffic is expensive if cross region. Such partitions can be replicated to all consumer nodes to favor access locality. 

Techniques about data placement follows similar categories with data partitioning.

  * __Metadata tracking__. Use Consistent Core to track the placement of each partition. It costs metadata size. The placement of a partition have full degree of freedom. All sorts of algorithms can be explored for fine-grain arrangement on capacity/hotness. No excessive migration is needed for node join/exit. Examples are HDFS/HBase, Tectonic.

  * __Consistent hashing__. Hash methods save metadata size. Naively a partition can hash map its placement to a node, but a node join/exit can churn all existing placement thus cause excessive data migration. Consistent hashing is introduced to stabilize the churn that, only neighbor VNodes are touched. Examples are Cassandra, Dynamo. We mentioned consistent hashing before.

    * __CRUSH__. Ceph invented CRUSH algorithm which is a hash based placement algorithm. It generate random but deterministic placement, and limits excessive migration during node membership change. Compared to consistent hashing, CRUSH supports hierarchical failure domains organized as a tree, and different weights of devices.

  * __Content-based addressing__. Placement is determined by the hash of the data block content, so that dedup is automatic. The example is XtremeIO. We mentioned it before.


### Data integrity

Data integrity is critical. A storage system can be slow, feature less, non-scalable, but it should never lose data. There are several failure patterns affecting data integrity.

  * __Durability loss__. Enough disk is down that a piece of data cannot be recovered. In compare, __Availability loss__ means a serving node is down, but data is still recoverable offline from the disks. At hardware level, an entire disk failure usually maps to power unit or disk encapsulation, while corruption usually maps to individual sector failures. [RAIDShield](https://www.usenix.org/system/files/conference/fast15/fast15-paper-ma.pdf) points out that climbing reallocated sectors is a good predictor for incoming disk failures.

  * __Disk error on reads__. Disk read can generate transient or persistent read errors. It may or may not map to the underlying bad sector. The rate can be measured by bit error rate, or [UBER](https://www.jedec.org/standards-documents/dictionary/terms/uncorrectable-bit-error-rate-uber).

  * __Silent disk corruption__. A disk sector can go corrupted without notice. The disk hardware may not discover it until the first read. Or the disk read is successful but software level CRC verification finds a mismatch.

  * __Memory corruption__. Memory bits can corrupt time to time and generates incorrect calculation results. This includes ECC memory. What's worse is a corrupted pointer, that may tamper a wide range of memory unpredictably.

  * __Unexpected data deletion bugs__. A high ingress storage system needs to timely reclaim deleted space. But a programming bug can unexpectedly delete valid data. This can be infrequent with careful rollouts, but once happened, much more data can be impacted than plain disk failures.

  * __Incorrect metadata bugs__. Metadata needs to be frequently updated with data changes. A programming bug can easily incorrectly update metadata, thus loses the track of data location or states. It's more error prone to handle version incompatible upgrades.

  * __Bugs propagated through replication__. It's not uncommon to see a full sets of replica corrupted, due to a bug is replicated too. Replication is effective to protect against hardware corruptions, but not so helpful for software bugs.

Plain techniques are used to improve data integrity.

  * __Replication based__. Replicate the data or apply EC. Replicate the metadata too in case one copy is corrupted. Perform periodical backup, including to another geo location, and to an offline system to prevent bug propagation.  

  * __CRC__ is pervasively used to verify a piece of data matches verification, with a cost of computing polynomials on finite fields. Compared to cryptographic hash, CRC is reversible to recover wrong bits. CRC algorithm [satisfies linear function](https://en.wikipedia.org/wiki/Cyclic_redundancy_check), which can be used for optimization. A 32-bit CRC is [able to detect](https://www.cs.princeton.edu/courses/archive/spring18/cos463/lectures/L08-error-control.pdf) any 2 bit errors, burst errors of length <= 31, any double bit errors, or any odd number of errors.

The techniques should be used with thoughtful methodologies. See more in this [article](http://accelazh.github.io/storage/Reliability-Against-Bugs-And-Corruption).

  * __CRC should be end-to-end__. User client generates the CRC, and the CRC is persisted in the last level of system. Data is verified with CRC before returned to user. CRC calculated in the middle of processing is less reliable because the input data may already be corrupted. The more general principle is, __end-to-end verification is necessary__.

  * __Any data transform needs verify__. Replication, EC, buffer copy, compression, network send, format change, store/load from disk, etc. Any data transformation should compare CRC before/after, in case any memory corruption happens in middle. The more general principle is, __each incremental step needs verification__.

  * __Save metadata twice__. Metadata is too critical that, it can be saved one time in Consistent Core, and keeps another copy on data nodes. The two copies are updated with different workflows. If metadata corruption happens in Consistent Core, they are still recoverable from data nodes. The more general principle is, __heterogeneous verification__, that critical data or computation should be persisted or verified by two different workflows, so that corruption at one side can be recovered from the other side. 

  * __Data ordering needs verify__. Distributed system can receive packets in inconsistent order. When data is being appended, their overall ordering should be verified that no change happened in middle.

  * __Periodical disk scrubbing__. This is common on distributed storage, e.g. Ceph, that disk needs periodical scrub to prevent from silent corruptions. To finish scrubbing on schedule, it requires enough throughput and deadline scheduling.

  * __Verification pushdown__. A storage system can be organized by multiple layers. Verification computation can be pushed down to the bottom layer, to shorten the data transfer path. It is applicable because verification logic is usually fixed, few exception handling, and data pipeline oriented. They can also also be offloaded to hardware accelerators chips or smart hardware.

  * __Chaos engineering__. Periodically inject failures and corruptions in the system to test system ability of error detection and recovery. Periodically drill the engineering operations of data recovery. The more risky activities should be carried out more frequently.

__High availability__

I choose to combine HA in this section because it's related to durability, most contents already covered before, and the fundamental goal of integrity is to ensure the correct data is always available. Availability issue is usually transient and gone after node recovery, but durability issue means data lost availability in infinite future.

  * __Replication__. The fundamental technique for data/metadata HA is to persistent multiple copies. Once copy to recover another, and 2 in 3 copies can vote out 1 incorrect data. Synchronized replication acks client only after all copies done updating, while __geo-replication__ or backup can be employed with an RPO.

  * __Active-active__. The fundamental technique for computation/service HA is to run multiple instances of services and allow failover. __Active-standby__ saves computation resource at the standby machine, but suffers from an RTO delay for standby startup. __Paxos__ is the pervasively active-active algorithm where the majority quorum arbitrates a split-brain. Active-active can be extended to multi-datacenter or multi-region, either by Paxos/sync or async replication. 

    * __Cell architecture__ partitions data and encapsulates depended services into cells. Each cell specifies only one active primary datacenter, while all datacenters run active cells. So that all datacenters are active-active, no standby datacenter. Data can be sync/async/not-replicated across datacenters. Datacenter failover needs caution to avoid overloading alive ones.

    * __Multi-zone services__. [AWS](https://cloud.netapp.com/blog/aws-availability-using-single-or-multiple-availability-zones) and [Azure](https://docs.microsoft.com/en-us/azure/storage/common/storage-redundancy) divide disaster failure domains in a geo region into availability zones. A services can span multiple zones that a single datacenter disaster won't impact availability. Zones are active-active.   

  * __Two geo locations three datacenters__ are commonly used in banks. One city deploys two datacenter with synchronized replication, and a second city deploys the third datacenter with async replication for disaster recovery.

HA relies on robust detection of failures, where the major issue is [Observational difference](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/paper-1.pdf) caused gray failures. Examples are dead App but heartbeat thread still working, network link degradation only at a high percentile, inconsistently reported heathy status, intermittent failures. Common techniques to overcome such issues are stemmed from __Metadata consistency__:

  * __Synchronized locksteps__ between heartbeat and application progress, e.g. use request execution count as heartbeat, or use expiring fencing token / lease.

  * __Gossip protocol__ that multiple peers can participate in observing failures, and an ask request can go confirm with multiple peers.

  * __Quorum decision__ that important events such as node failure or node membership change should engage a consistency quorum to make the final decision.

__Durability__

Durability usually share similar techniques with HA, except more emphasis on disk failures/corruptions and integrity verification. They have already been covered before. Reliability modeling is commonly used, where [exponential distribution](http://web.stanford.edu/~lutian/coursepdf/unit1.pdf) satisfies most needs.


### Resource scheduling

Multi-dimensional resource scheduling on cloud is a big topic, see DRF/2DFQ etc mentioned in [Reference architectures](.). In this section I cover design properties in a typical storage system. 

  * __Priority__. A user/background job/request should be handled first or delayed, with maximum or minimal resources. Priority are also reflected as weights on different user jobs. Usually, critical system traffic e.g. data repair > user latency sensitive workloads > user batch workloads > background system jobs. 

  * __Throttling__. A user/background job/request should not use more resources than its __quota__. Throttling also means to isolation the propagation of impact from one user to another, where shared resources like CPU, network, IO bandwidth, latency can easily become the channel. Typical throttling algorithms are token-based Leaky bucket, or a simple queue limit on request count/size.

  * __Elastic__ has multiple meanings: 1) A service can timely expand to more resources in respond to the growing load. 2) A background job can borrow unused resource for faster processing, even temporarily exceeds its quota. 3) A low priority job can timely shrink itself, if a high priority job suddenly demands more resources. Elasticity involves quick startup or growing resources, predicting usage with Machine Learning, instantly enforced quota, and probing growth, that sometime resembles __congestion control__ in networking protocols.

    * __Resource utilization__ should eventually be improved, without impacting latency sensitive workloads. This also benefits __energy efficiency__, which is a main datacenter operating cost. CPU can dial down frequency. Vacant nodes can shutdown.

  * __Fairness__. Commonly mentioned in locking or resource allocating. User jobs should be given similar chances to get resources, proportional to their priorities/weights, rather than being biased or starved.

    * __Anti-starvation__ is the other side of coin. Low priority background jobs should not be delayed too much, e.g. GC/compaction to release capacity. It resembles important but non-urgent quadrant in time management. It requires detecting starved jobs and apply mitigation.

    * __Priority inversion__ is another issue. High priority can be waiting on the resource held by another low priority job, e.g. a lock. Dependency link should be traced to bump priority, or preemptively kill and retry.

    * __Preempting__. It defines the strategies whether higher priority jobs should stop/pause lower ones to take up its resources. Besides job scheduling, preempting is also seen in transaction scheduling and deadlock resolving. It varies whether younger jobs should preempt older ones, or vice visa. The cost to preempt a long live transaction can be high. OCC can also be seen as first win jobs preempts slower ones, where frequent retry can cost high.

There are a few system properties to consider when designing resource scheduling.

  * __Job granularity__. Small jobs generally benefits resource schedule balance. Think randomly tossing balls into bins: the smaller and more balls, the balancer per bin's final ball count. The method is widely used for multi-core processing, i.e. async multi-stage pipeline. While small job granularity is beneficial, it costs metadata, increases IOPS, and disks still favor batches.

  * __Overload control__. System overload and then cascaded failures are not uncommon, e.g. synced massive cache expire, retry count amplified across layers, node failure repair/retry than bringing down more nodes, CPU/memory/network exhausted and propagating the churn, crash failover then crash again, etc. Operation control knobs, graceful degradation, circuit breaker are necessary.

  * __Cost modeling__. Read/write size is the common practical cost modeling in storage systems. Together they compose queue count and queue size. The most comprehensive cost modeling as a reference can be found in DB [query optimizers](https://mp.weixin.qq.com/s?__biz=MzI5Mjk3NDUyNA==&mid=2247483895&idx=1&sn=05b687a465f5e705dbebfdccaf478f4b). The predicted IO cost can be combined with deadline to early cancel requests that cannot finish in time or resource limits.


### Performance

Though running the system fast is the most typical meaning of performance, performance maps to more system __properties__:

  * __Latency__ & __Throughput__. Latency measures how fast a request is served and returns. It matters more to small requests. Throughput measures how fast given size of data is processed and returns. It matters more to a single large request, or a batch of requests up to size.  Note requests in queue negatively affect latency, by adding arbitrary queuing latency to serving latency. But they generally benefit throughput, if the system is not overloaded, by exploiting batching and parallelism in request serving. __Queue depth__ (QD), or outstanding/active/on-going request count, measures such behavior.

    * __Tail latency__. Request latency is a probability distribution that usually P25/P50/P99 vary greatly, especially in cloud storage that is serving mixed workloads from many customers, with unpredictable burst patterns, and in a large scale. P99 matters because it still maps to many customers. P25 is usually achieved by cache hit, while P99 can point to bad cases in request execution. Typical techniques to reduce tail latency include sending extra requests, monitor lagging noes with proactive retry, and [the power of two random choices](https://brooker.co.za/blog/2012/01/17/two-random.html).

    * __[Queuing theory](https://lrita.github.io/images/posts/math/%E6%8E%92%E9%98%9F%E8%AE%BA%E5%8F%8A%E5%85%B6%E5%BA%94%E7%94%A8%E6%B5%85%E6%9E%90.pdf)__. The system is abstracted into components connected sequentially/in-parallel by queues. While stochastic math can be used in modeling, simulations with production samples are generally more practical. Though Queuing theory points out serving latency can grow to infinity with 100% resource utilization, the assumption is fully stochastic request ingestion. In a well scheduled system, where requests arrive at chosen time instead of stochastically, is still possible to achieve high resource utilization with low latency (for high priority jobs). Queuing theory is also used for __Capacity Planning__, where the queuing layout can point out the bottlenecks of data flow, while it also helps debugging/troubleshooting to narrow down which point injected the excessive latency. Queuing theory also guides __configuration tuning__, that only when the queue sizes and capacity at each component are well fitted, the overall system performance can reach its max.

    * __[Instruction per cycle]__ (IPC). While latency/throughput are useful to measure IO systems, what are the concepts extended to CPU-cache-memory area, or in-memory processing systems? The typical measures are IPC, __cache misses__, __memory stalls__, from CPU statistics. A well designed program increases IPC by reducing mis-predicted branch jumps, making efficient use of CPU cache, pipeline and prefetch memory; as well as to reduce the cache invalidation, cache line locking, process lock wait due to concurrency control algorithms.

  * __[Predictable performance](https://www.usenix.org/conference/atc22/presentation/elhemali)__. A higher requirement for latency/throughput is, they should be consistent among requests, among time, and among any scale. A typical anti-example is SSD performance varies time to time due to background GC is running, where the term "__Deterministic latency__" is often used. Another anti-example is SSD performance starts to drop after over-provisioned space is used up, where the term "__Sustainable performance__" is often used. People also expects Cloud storage to provide consistent latency from request to request, i.e. to shorten the __gap between P50 and P99__; and to ensure a stable performance during App/VM is running for days and being migrated.

    * __Factors affecting predictable performance__. Background maintenance job like GC/Compaction can easily block user requests with a large read/write request at the head of queue. Workloads have changing hotspots, while load balancing and migration may not kick in in time. Customer TPS/Capacity can grow rapidly, with bursts, while auto scaling is not responsive enough, and the switching is not smooth. Migrating itself also consumes resources. A VM can run with noisy neighbors, where co-locating is necessary for resource efficiency, but quota/throttling isn't perfect. Cache can miss, while cold restart or traffic churn can cause cascade failures. Switching between cache hit/miss, or anything similar, is a behavior of __[Bi-modality](https://www.usenix.org/conference/atc22/presentation/elhemali)__, that is a fundamental cause of performance variances. DBs may have schema changes at background. __Adaptive execution__ switches strategies, data structures, and indexes being used in middle according to traffic pattern, more efficient, but can create a non-smooth jump of performance. Networking can also have burps, congestion, and incast problems. Overall, achieving predictable performance is still one of the challenges in cloud storage. 

    * __Service-level Agreements__ (SLA) / __Service-level Objectives__ (SLO). Cloud storage offer customers with SLA, a money insured guarantee about performance and availability/durability, while SLO gives more rigid measured numbers. Offering a predicable performance is even more important to customers than simply saying we are fast. What may also overweight fast is to offer a rich feature set, trustworthy customer service, helpful troubleshooting and visualization, and extreme data safety & security.

    * __Graceful degradation__. When overloaded, or some components are offline (e.g. Auth service), or new feature disabled / rolled back, the system should have a graceful path to degrade the serving level. What should be avoided are cascaded failures, retry storms, or missing operation knob for recovery. Typical techniques include throttling with circuit breaker, cancel requests that cannot meet future deadline, avoid amplifying retry at each level, etc.

    * __Quota/throttling/admission control/deadline__. These words have overlapped meanings. Customer accounts or allocated objects are provisioned with quota, and these quotas are further used for job scheduling. Throttling is the common need in cloud storage with multi-tenancy, that enforces resources used by quota, protects from system overloading, and avoid affecting latency by noisy neighbors. Soft quota are usually allowed to share between customer objects, or between different customers, to temporarily absorb bursts. Longterm or periodical traffic changes can be learned by Machine Learning to proactively scale up/out on-demand. Throttle can be dialed with incremental feedback control loop, and interference measured with runtime micro experiments ([NyxCache paper](https://www.usenix.org/conference/fast22/presentation/wu)).

    * __Cold restart__ is a typical issue that if a cache node restarted, it cannot serve requests well until filled up again. This can easily introduce a churn during batch upgrade, overload the system, kill more nodes, and bring a cascaded failure. AWS Redshift introduced [Warmpools](https://assets.amazon.science/93/e0/a347021a4c6fbbccd5a056580d00/sigmod22-redshift-reinvented.pdf) to provision pre-warmed cache nodes.

  * __Scalability__. The fundamental way to concur a scale problem is to __divide and concur__. With the fast growth of modern hardware, being efficient in __Scale-up__ is also necessary, e.g. to work with __manycore__ CPU with efficiency concurrency, to handle large memory with NUMA, to respond fast with RDMA networking, PMEM, NVM SSD. __Scaleout__ is the classic cloud storage solution, with infinite scale (in theory), but every step in the distributed consistency and communication charges your COGS.

    * __Partitioning__ & __Replication__. Partitioning scales out the performance for the overall data space, while Replication scales out the performance for a specific data unit. They can work at different and non-symmetric fine-grain levels. Caching can also be seen as a case of replication, which leverage more expensive hardware to increase performance within space/temporal locality.

    * __Data tiering__. Caching replicates data across faster storage hardware, while data tiering migrates data across them. Another fundamental way to increase performance is to __run it on a better hardware__. The recent years of growth in hardware industry, e.g. memory, networking, SSD, disk density, are even faster than software, so that buying new generation hardware is even a better choice than human optimizing the software for cost and time-to-market.

  * __Resource efficiency__. Commonly better performance requires programming efficient code. The techniques vary at different system layers e.g. CPU-cache, in-memory computing, networking, and at different storage media e.g. HDD, SSD, PMEM, DRAM. The next fundamental way to increase performance is to __Do less things__. A typical example is a system runs faster if turned off all logging, and a new system with fewer features usually runs faster. The next key part for resource efficiency is load balancing. It's not too few resources, but problems at exchanging and fair assignment that cause starvation.

    * __Load balancing__. The first hop of load balancing is efficient __job scheduling__ and  __placement__ on servers, that best coordinates with resource utilization, fairness, and co-locating jobs with SLA guarantee. Customer jobs run with close monitoring at growth, bursts, and hotspots that involve __scaleout__ and __partition split/merge__. The cluster runs monitoring for over/under-utilized nodes that conducts __migration__ time to time. __Quota/throttling/admission control__ are the next part to protect SLA, ensure predictable performance, and as a trigger for migration. Node __failure detection__ is an infrastructure ability needed in between, where __gray failures__ can inject intermittent latency or report inconsistent healthy status, that need robust handling.

    * __COGS__. Overall, the cost of IOPS, storage space, and query TPS, should be measured and controlled to understand the end-to-end resource efficiency. It's also the Project/Product Management that incorporated into decision making whether an investment worths its cost. The COGS is essentially sellable earning compared to overall spending at datacenter purchase/operation, telecomm renting, R&D, etc. __Capacity Planning__ also takes part in COGS about what SKU and how many to purchase, usually in ahead of months to years.

    * __Kernel bypassing__. Intel __[DPDK](https://www.dpdk.org/)__ went popular with RDMA that require faster CPU processing, where Linux Kernel networking stack is relatively slower so they get bypassed. __RDMA__ can also be seen as a bypassing of server CPU. The approach then gets adopted at Intel __[SPDK](https://spdk.io/)__ that Kernel bypassing makes faster CPU processing for PMEM and NVM SSD. __DPU__ further bypasses host CPU to take over common storage infrastructure. Ceph also built BlueStore which underlyingly implements customized [BlueFS](https://zhuanlan.zhihu.com/p/46362124) that bypassed many functionalities compared to the original Linux Filesystems. Kernel bypassing is another example of __Do less things__: shorten call path, less jump nodes, direct access, direct return.

  * __Hardware acceleration/offloading__. While CPU is general purpose, the same (or less) money spent on specific purpose chips can yield even higher computation throughput at a low energy consumption. Besides, CPU itself is becoming harder to catch up with rapidly growing processing speed required by modern IO devices like PMEM, RDMA networking, and Deep Learning / Machine Learning.

    * __ASIC__ based compression/encryption cards are common. __AWS Nitro__ / __Microsoft Catapult__ are successful business cases that ASIC/FPGA boost virtual cloud networking, as well as compression/encryption, etc. 

    * __SmartNIC__ builds virtualization, RDMA, processor offloading in NIC. CPU work can be offloaded to NIC level, with shorter roundtrip path. While __SmartSSD__ (or [Computational SSD drives](https://www.usenix.org/system/files/fast22-qiao.pdf)) builds query processing at SSD level, bypassing PCIe for early filtering data.

    * __GPU__/__TPU__ are leading Machine Learning acceleration, dedicated for FLOPS in thirty Deep Learning training. __IPU__/__DPU__ try to consolidate datacenter infrastructure into more COGS efficient chips. More advanced GPU inter-connection like NVLink are being developed, composing an HPC cluster.

    * __HPC__ is another area that high-end hardware, usually with customized accelerators, and manycore, are used for scientific processing. The accelerators usually then gain maturity and enter the market of commodity servers, like RDMA.

  * __Debugging & Troubleshooting__. Performance is not only a matter of now, but also a good velocity to improve it. Only when there are metrics, there are insights to make the improvement. Well-designed monitoring system involves realtime time-series metrics, logging with exchangeable standards, and a data warehouse for retention and complex queries. [OpenTelemetry](https://opentelemetry.io/docs/concepts/), which is similar to [Google Dapper](https://research.google/pubs/pub36356/), is a typical micro-service tracing framework that can be used to debug performance issues.

    * __A typical analysis__ involves __top down breakdown__ of component calling hierarchy (or [queuing layout](https://zhuanlan.zhihu.com/p/22124514)), and to narrow down which component injected latency. The culprit requests are then correlated with recent system changes, certain SKU tags, source units generated traffic patterns, etc. After going to the server level, the narrow-down further branches to disk IO, network IO, or to CPU/caching inefficiency. At each branching point, there should be __supporting tools__ for investigation and visualization. In the end, the analysis should give estimated impact numbers that __matches with__ the observation, to __validate the hypothesis__. 

    * __Thought experiment__ starts from a __bottom up approach__. Suppose latency was injected at a bottom component, by a certain type of requests, at a specific percentile level. Does the system have enough metrics and troubleshooting tools to find it out? And then from the top down again, what is the main contributor that affects latency? Performance troubleshooting shouldn't be a hard problem. Instead, it should be a systematic approach that discovers what we can and where we miss metrics and tools, and then enhance the infrastructure step by step.

    * __Line speed, gap analysis__. Another approach to analyze performance is to first find out the raw hardware speed (line speed) of the underlying storage device or networking device, and then analyze what composes the gap from line speed to the actual performance of the storage system. This provides a systematic approach to dissect performance layer by layer, and guaranteed to reach its max given abundant dev resource invested. Anyway, optimization should __start from the bottleneck__, backed with metrics insight.

__Concurrency & parallelism__

Exploiting concurrency & parallelism is the key technique to improve performance. This section covers those techniques. We mainly focus optimizing a single node here with multi-core, while distributed scaleout systems are put to the later section. In general, parallel means happening at the same time (need hardware support), while concurrency means happening together but not necessarily at the same time (by interleaved scheduling). 

The fundamental ability of parallelism comes from __Hardware parallelism__. E.g. CPU cache chip can be designed to lookup every cache lines all at the same time, while software hashtable has to resort to various multi-threading techniques backed by CPU multi-core. The best performance comes from utilizing all parallel units, with minimal coordination/synchronization overheads.

  * __Typical hardware parallelism to exploit__ are listed here. First, the most commonly CPU socket -> CPU cores -> CPU hyper-threading. Next, NUMA and [DRAM banks](https://zhuanlan.zhihu.com/p/539717599). SSD built-in [parallelism at Plane level](https://blog.51cto.com/alanwu/1544227) (Chip -> Die -> Plane -> Block -> Page -> Cell). PMEM may have similar internal parallelism like SSD.

  * __SIMD, vectorized execution__ are common DB techniques to exploit the data parallelism per instruction. Column scan is treated as operating (bit) vectors. Further, Code Generation and JIT are used to produce more CPU efficient execution plans. AWS Redshift further looks up recent compilation in external caches.

  * __ASIC, FPGA, TPU, GPU__ Specialized hardware can further boost parallelism and efficiency for the target workload. For FPGA, how large the chip area is, how many computation units can be programmed, and thus how many can work in parallel. More chips can be interconnected with high bandwidth link (e.g. NVLink) to compose an HPC cluster.

__Load balancing__ is critical to achieve max efficiency among multiple hardware units being utilized in parallel. This is just like a scaleout distributed system.

  * Tasks cutting into smaller units are easier to balance, just like tossing smaller balls to bins. This explains why storage engines can benefit from __Multi-staged Pipeline__. It resembles to smaller partition size in a distributed system. Besides cutting tasks, __Pipelining__ overlaps task execution to improve utilization of the underlying resources. __Prefetching__ and __[Speculative execution](https://www.usenix.org/conference/fast22/presentation/lv)__ further overlap future with now.

  * __Work stealing__ is another common technique. Idle thread seize jobs from busy threads. The cost of scheduling tasks are automatically amortized to more idle threads. It resembles to job __migration__ in distributed systems.

__Reduce communication__ is the most important topic. Locking and synchronization are the top area in concurrency & parallelism. They are used to coordination communication. But the best system is designed to rather NOT requiring communication, thus the most simplified. This same applies both in a distributed scaleout system, or a single node scale-up system with manycore.

  * __Symmetric parallel copies__ (同态多副本). The data and tasks are sharded into multiple copies. Each copy processes in exactly the same way. Copies don't need any interaction. E.g. processing requests from different customers in a Cloud storage systems. E.g. Ceph OSD that each thread exclusively owns a disk. E.g. Networking switch that one core schedules tasks to all other cores doing plain packet processing.

  * __Communication density__. Locking/latching, reading another thread's thread local, and accessing shared memory/cache address are all communication. Plot the communication connections by each CPU core. How frequent are such communication done? What's the connection fan-out? What's the webbing density? A good algorithm should reduce all three.

    * __Lock/latch free algorithms__ usually have high communication cost in manycore condition, as pointed out by HyPer [Scalable MVCC GC paper](http://www.vldb.org/pvldb/vol13/p128-bottcher.pdf). The communication point is usually a CAS operation which underlyingly locks CPU cache line. All cores race on the lock, creating an N-to-N communication map, which is frequently triggered, high fan-out, and thus high webbing density.

    * __Flat Combining__, and also the __Thread Local__ technique used in the above HyPer paper. Each thread only works in its thread local, and a leader thread consults all other threads to do coordination work. This reduces communication to a fan-out of 1-N, and thus reduces webbing density.

    * __Epoch based reclamation__ further reduces the communication frequency. Only when epoch passed and each thread local is away from the shared resource, the leader thread will do the coordinated resource cleanup. Similar idea applies for techniques like Sloppy Counters, delayed batched async updates, etc.

  * __Reduce competing resources__. Avoid racing on resources when it's not necessary. A typical example is __False Sharing__ that CPU cores race on a cache line, whose dependency is not required by the App, but introduced by compiler packing memory objects.

    * __Partitioning and reducing lock granularity__. A typical technique is to partition the hashtable, and each lock only owns a shard. This partitions the communication web to reduce connection density. Also, typical programming courses teach about fine-grain locking. This reduces the duration of communication connection, similar with reducing frequency, and may also reduce the connection fan-out.

    * __B+-tree lock coupling__ steps lock through tree parent/child nodes with limited lock span, like a crab. Compared to locking the whole sub-tree, it also reduces the lock scope, thus reduced the competing resource. It's another example of fine-grained locks. Acquiring lock in the same order is related, that by pre-building coordination with fixed rules, deadlock can be avoided.

    * __Copy-on-write, immutable data objects, shadow paging, and delta updates__ are related techniques. Instead of working on the original data, updates work on a copy, or only write deltas. In this way, the updaters avoid racing on the original data. Besides, __Immutability__ can greatly simplify system design, but yet poses pressure on later GC.

    * __Concurrency by scheduling__. The example is [NetApp WAFL filesystem](https://www.usenix.org/system/files/conference/osdi16/osdi16-curtis-maury.pdf). Accesses to disjoint files and address partitions can be safely parallelized. Instead of programming low level locks, NetApp uses a top level scheduler to ensure racing accesses won't be scheduled.  

Here also to mention __Engineering aspects__ of concurrency & parallelism. I categorized coroutine in this part.

  * __Coroutine, thread, and process__. In theory, they should be able to achieve the same level of performance or parallelism, except coroutine allows bypassing the Kernel, and threads are more lightweighted to share resource/memory than processes. However, a nice programming API does matter, that by which coroutine quickly gains adoption. Threading are left to give developers root control on concurrency & parallelism, where the thread execution pool can be tricky; while processes are better at resource/fault isolation.

  * __Sync & Async__. In theory, they should be able to achieve the same level of performance or parallelism. But Async programming is easier to overlap CPU time with IO time to improve efficiency (e.g. epoll), and more easily cut long function into smaller tasks to benefit load balancing.

  * __Lock and preempting__. A simple lock let first comer win and blocks later comers. But it can be implemented differently to either let first/later comer win, either block/non-block, and with OCC retry. Such techniques can be used to optimize DB transactions, especially those mixed short live OLTP transactions with long running OLAP transactions.

  * __Testing the correctness__ of a complex concurrency program is not easy and important for Cloud storage. C# [Coyote] searches through the large execution ordering space to find potential bugs. FoundationDB also equips with Deterministic Simulation Testing built by Flow. Besides, TLA+ is used to model the state machine aside to verify liveness and invariants. 

__CPU-cache and in-memory__

Performance optimization can be broken into several aspects

  * __CPU, cache, and memory__. They usually overlap with __Scale-up__ topics and optimizing a single node, i.e. how to efficiently utilize them after stacked more CPU cores and large memory. We'll cover below.

  * __IO and networking__. They usually overlap with __Scaleout__ topics, where a distributed system interconnects many nodes. Also, disk IO and networking traditionally are slower than the CPU, cache, and memory plane. We'll cover in the next section.

Per optimizing __CPU, cache, and memory__ plane, there are a few aspects below

  * __Concurrency & parallelism__, as we covered in the previous section.

  * __Memory wall__. Today CPU is much faster than DRAM ([1ns vs 100ns](https://colin-scott.github.io/personal_website/research/interactive_latency.html)), which relies on Cache as the middle bridge. Efficiency can be measured by __IPC__ (instruction per cycle), __Memory stall__, and __Cache miss__ counters. A good algorithm needs to 1) exploit locality for caching 2) pipelining with cache prefetching 3) avoid racing on the same cache line 4) avoid extra memory writes while keeping most operations in CPU register and cache.

  * __Branch mis-predict__ is costly for CPU speculative execution. An efficient data processing program should avoid too many if branches which are not deterministic. Such principles become yet more important for GPU, who has minimal control units and most chip area is dedicated for synced data operations.

  * __Do less things__ will always make the program faster. DB query __Code Generation__ and __JIT__ can be seen as an example, where highly customized code is compiled for each specific query SQL to improve CPU efficiency. Though the code is either unfriendly for human programmer, or there are too many combinations for handcraft. 

__Scaleout systems__

In this section we focus on optimizing performance at the distributed scaleout system plane. The previous section already covered most topics, such as __Load balancing__, __Tail latency__, and __Pipelining__, etc. More former sections discussed about __Sequentialize IOs__. The majority of performance improvement comes from scaleout itself, and carefully optimizing single node performance. We add a few bullets not covered by the above

  * __Compression__ is a seemly separated topic but can significantly improve performance because fewer data are transferred across IO devices. We have talked much about it in previous sections.


### Networking

// TODO

__Datacenter networking architecture__


// TODO Also mention SDN, e.g. Google Orin, Openstack Neutron here 

__Load balancing__

Google maglevle
ECMP

https://cloud.google.com/load-balancing/docs/load-balancing-overview

nginx

Direct Response
https://docs.bluecatnetworks.com/r/DNS-Edge-Deployment-Guide/How-DSR-load-balancing-works


BGP reroute


__Application layer__

__TCP layer__

__IP layer__

__Data link layer__



### More topics 

Compared to section "Storage components breakdown", there are a few topics I didn't cover.

  * __Allocator__ It refers the to disk space allocator by a single node filesystem. There are mature and off-the-shelf solutions in production filesystems. A distributed storage usually directly leverage them by building atop the local node filesystems. On the other hand, "Allocator" in a multi-node case is the __Data placement__ we covered before.

  * __Upgrade/deployment__. Safe and incremental upgrading on a large scale distributed storage system with atomic rollback can be complex and with many engineering practices. But they are too much off the topic so I didn't cover in this article.

  * __Configuration management__. __[CMDB](https://en.wikipedia.org/wiki/Configuration_management_database)__ is an interesting topic. E.g. you need a database to manage the many baremetal nodes in a large scale cloud. However they are too much off the topic so I didn't cover in this article.

  * __Operational ease__. It's an interesting topic to design a system that makes daily operation smooth, safe, and to avoid human errors. However they are too much off the topic so I didn't cover in this article.






// TODO We should have a overall picture for all techniques. It can be a similar to: https://mapsontheweb.zoom-maps.com/post/143896346898/a-map-of-mathematics
        We should have a typical storage system picture with each components and data flow. At each components, we put the technique breakdown there.

// TODO Wrap and mapping to Reference architectures.

// TODO design space analysis
// TODO think in this aspect: 1) what is the driving factor and challenge, 2) what is the design space. 3) then boil down to discrete design patterns

// TODO Let's check each project mentioned in reference architecture, and generate a table to say how they did in Storage components breakdown, and how they did in design patterns. This should generate the nice table chart. -> <design pattern, touching components, examples systems>

------------------------------

// TODO I should insert more pictures also in former parts to help reading. too many words 
// TODO Add my materials to a zip and link to this article
