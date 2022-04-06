---
layout: post
title: "Summary on Software Architecture Design"
tagline : "Summary on Software Architecture Design"
description: "Summary on Software Architecture Design"
category: "technology"
tags: [cloud, engineering, architecture]
---
{% include JB/setup %}


The article summarizes my experience on software architecture.

## Software architecture - a philosophy perspective

Software architecture is a modeling of the reality world, a language, and a human mind creation that to assist human mind. Language, is an interesting topic. The three together are deeply inter-connected, pointing why, what and how to handle software architecture.

The next and following chapters tell about knowledge in software architecture. But this first chapter tells about the engine that generates the knowledge.

__Reality, language, human mind__

Firstly, __the modeling of the world is human language__. Human language evolved for thousands of years, enriched by distinctive civil culture, polished by daily interaction among population, and tested by full industry use and creation. Grab a dictionary, you learn the world and mankind. 

Next, the modeling tool is also a model of the model-er itself. I.e. __human language is also the modeling of human mind__. Thinking is carried and organized by language. Language is structured in the way how human mind is capable to perceive the world, rather than how necessarily the world itself has to be. E.g. software designs by high cohesion low coupling, which is also the principle of how words are created in language. Like they are to reduce software complexity, they do because human thinks this way.

We can say __human language, mind, and the perceivable reality are isomorphic (of the same structure)__. The expedition into the outer world is the same way with exploring into the deep heart. Losing a culture, a language, is the same with losing a piece of reality. As the two sides of a coin, human language is both the greatest blessing how mankind outperforms other creature beings, and also the eternal cage how farthest human mind is capable to perceive.

__About software architecture__

Software architecture is a language, a modeling of the reality world, and a human mind creation to assist human mind. __The essence of software architecture__ is to [honestly reflect the outer world](https://www.zhihu.com/question/346067016), to introspect into the inner mind, and to conceptually light up where it is dark missing. The answer is already there, embedded in the structure, waiting to be perceived.

The question is not what software architecture itself is, nor to learn what software architecture has, but to understand the landscape of world and mind, where you see the hole that needs "software architecture" to fill. You __predict and design__ what "software architecture" should be, can be, and will be. There can be 3000 parallel worlds each with a different software architecture book; what we have here is just one.

Besides, __knowledge and experience are themselves good designs__. They are essentially a domain language, a reusable piece of world modeling, thus also explains why they are useful across daily work and even substitutes design skills. Knowledge is not to learn, but to observe the art of design tested by human act.

__Side notes: explaining with examples__

For __"high cohesion low coupling" in human language__, imagine an apple on a disk. People name them with "apple" and "desk", rather than a "half apple + half desk" thing. Like selecting what to wrap into an object in Object-Oriented (OO) design, the naming "apple" and "desk" practices "high cohesion low coupling".

To drill deeper, "high cohesion" implies "going together". The __underlying axis is time__, during which the apple goes with itself as a whole. The edges of the apple and the desk intersect, but they have different curves, and they can be decoupled (separated if you move them). Another __underlying axis is space__. Human senses apple and desk with basic elements like shape and color. These __sense elements__ grow on axes of time and space, to be processed into human language. The processing principles look like those from software design, or to say, software design principles are crafted to suit human mind.

An imagined creature can have a totally different language system and thinking mind, if they do not rely on visual sights like human, or even not with time and space axes. They may not need "high cohesion low coupling" as a thinking principle neither. E.g. they can process information like how organic biology evolves. 

For __human language is also a cage__, remember language is a modeling of the reality. __Modeling__ implies "less important" information are dropped to ease the burden of human cognition. Are they really less important? Words are to __reuse__ the same concept for events happened at different time, which saves duplicates. But are they really duplicates? The necessity of language is itself a sign that human mind is unable to process "full" information. Relying on language, the ability is crippled, limited, caged.

More, human mind can hardly think without underlying __time and space__ axes. Human words, at the bottom layer of the abstraction tower, can hardly go without "human-organ-oriented" __sense elements__. People frequently need daily chats, to sync drifts on abstract concepts. Even language itself is becoming a bottleneck, between human-to-machine, population-to-population information exchange.

For __"software architecture" hole in the world and mind landscape__, you all see more in the following of the article. Though most associate "software architecture" with technology, it is also determined by organization and process needs. Various "needs" in different domains flow into the gap of "software architecture", crafted to be processed and expressed in a suitable language for human mind. Together they evolve into the internal meaning of "software architecture".

For __predict and design what "software architecture" should be__. It can be explained as the method of learning. The plain way is the learn what it is, the structure, the composition, cover the knowledge points, and practice using. The better way is to first understand the driving factors, landscape, and dynamics behind. You can see the source and direction of it, even to the end and final limitation. You can also see the many different alternatives, possible to happen, but eventually not chosen by the real world industry, due to certain reason in the back. You should be able to define your own methodology, given your local customized needs. You can forget the knowledge and create any on your own.


// TODO Add a picture about the apple/desk cut


## Why need software architecture

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

  * __Project management__. Architecture step is usually where the cost effort, touching scope, delivery artifact, development model; and resource, schedule, quality can be determined and evaluated. Project management usually works with the architect role.

  * __Review and evaluation__. Architecture step is usually where the key designs are reviewed; the key benefit, cost, risk are evaluated; throughput capacity breakdown are verified; and all user scenarios and system scenarios are ensured to be addressed.

  * __Cross team collaboration__. Architecture touches various external systems and stakeholders. It is when to break barrier and build consensus cross teams, BUs. It is when to ensure support and get response from key stakeholders. It is where to drive collaboration.

  * __Tracks and lanes__. The architect role usually builds the framework, and then the many team members quickly contribute code under given components. It sets tracks and lanes where the code can grow, and where not. I.e. the basis of intra-team collaboration.


// TODO Add a pic about architect role, that inter-connects project PM, dev teams, customer requirements, key technology decisions. and like Management (risk, critical path). Break the barrier and build consensus.



## Different architecture organization styles

What an architect role does and means in real world industry are somehow puzzled. From my experience, this is due to architecture step is organized differently at different companies. At some, architect is the next job position of every software developer; at some others, I didn't even see an explicit architect job position. 

  * __Architect the tech lead__. Usually seen at Internet companies. The architect role is taken by a senior guy in the team, who masters technology stacks and design principles. The architect makes decision on which technology stack to use, and builds the framework for the following team members to fill concrete code. The architect role is in high demand, because Internet companies quickly spin up Apps after Apps, each needs its architect, while the underlying opensource infrastructure is relatively stable. Both the business value and technology stack win traction.

  * __Architecture BU (i.e. department)__. Seen at Telecom companies. Architects work with architects, software developers work with software developers; they reside at different BUs. The architecture results are handed off in middle, following a waterfall / CMMI model. The architecture designs on more stable, even standardized requirements, with very strict verification, and delivers completeness of documentation. Strong process, and expect more meetings bouncing across BUs. Employees tend to be separated into decision making layer and execution layer, where the later one expects long work, limited growth, and early retire. 

  * __Peer-to-peer architect__. Usually seen at teams building dedicated technology. Unlike Internet companies spinning up Apps horizontally atop many different technologies, such team vertically focuses on one, e.g. to build a database, a cloud storage, an infrastructure component, i.e. 2C (former) vs 2B (later) culture. No dedicated architect job position, but shared by everyone. Anyone can start a design proposal (incremental, new component, even new service). The design undergoes a few rounds of review from a group of senior guys, not fixed but selected by relevance and interest. Anyone can contribute to the design, and can join freely to set off with project development. Quite organic. Technology is the key traction here, where new architecture can be invented for it (e.g. new NVM media to storage design).

  * __System analyst__. Usually seen at companies selling ERP, or outsourcing. The systems are heavily involved into customer side domain knowledge. And the domain knowledge is invalidated when selling to another customer from a different domain. Because of new background each time, comprehensive requirement analysis and architecture procedures are developed. When domain can be reused, domain experts are valued, where __knowledge and experience themselves are good designs__. Domain knowledge can win more traction than technology, where the later one more leans to stability and cost management.

  * __Borrow and improve__. Usually seen at follower companies. If not edge cutting into no man's land, __reference architecture__ (top product's architecture) can usually be found to borrow from, to customize and improve. This is also benefited by the wide variety of opensource. Reference architecture, standing on the shoulder of giants, are widely used in software architecture processes, e.g. comparing peer works, which is another example of knowledge and experience themselves are good designs. Market technology investigation survey are high demand skills.


## Key processes in software architecture

As preparation, architecture design requires below knowledge and skills

  * Downstream, __understand your customer__. The customer here also includes downstream systems that consume yours. Know customer to capture key aspects to prioritize in architecture, and more importantly what to de-prioritize (E.g. favor latency over cost? Is consistency and HA really needed?). It helps identify the risks (E.g. festival burst usage, backup traffic pattern). Besides, well defining customer space reveals future directions the architecture can evolve.  

  * Upstream, __understand what your system is built atop__. A web App can be built atop a range of server engines, service mesh, database, caching, monitoring, analytics, etc. Mastering the technology stacks is necessary for designing architecture that works with the practical world, and for choosing correct technology stacks that suit project goals and team capabilities. 

  * Externally, __understand the prior of art__. To design a good system, you need to know your position in the industry. Reference architecture can be discovered and borrowed from. Existing technology and experience should be leveraged. E.g. given the richness of opensource databases, designing a new data storage is even a selection and cropping of existing techniques. Participating in meetups helps exchange industry status, and to ensure your design is not drifting away into a pitfall. 

  * Internally, __understand your existing systems__. Understand the existing system to make designs that actually work, and to correctly prioritize what helps a lot and what helps little. Learn from past design history, experience, and pitfalls, to reuse and go the right path. 

  * Organizationally, __broaden your scope__. Architecture design involves interacting with multiple external systems and stakeholders. Besure to broaden your scope and get familiar with them. Communicate with more people. Solid soft skills are needed for cross team / BU collaboration, to break barrier and build consensus, and to convey with action-oriented points, concise, big picture integrated with detailed analysis.

I lean more to peer-to-peer architect style mentioned above. Many can be sensed from [GXSC's answer](https://www.zhihu.com/question/24614033/answer/497338972). At each step, besure to engage __talk with different persons__ which significantly improves design robustness. Rather than the design results, it's problem analysis and alternative trade-off analysis that weight most.

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


## Key methodologies in software architecture

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

Software design is complex. To manage the complexity, we break it into different __levels and views__. Typical levels are: architecture level, component level, and class level. The abstraction level goes from high to low, scope from big to small, and uncertainty from fuzzy to clear. Each level yet has its own methodologies. Levels also map to first-and-next steps, which in practice can be simplified or mixed, to lean more to the real world bottleneck. 

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

Besides this section, I also found valuable experiences from Kenneth Lee's [blogs](https://gitee.com/Kenneth-Lee-2012/MySummary/tree/master/%E8%BD%AF%E4%BB%B6%E6%9E%84%E6%9E%B6%E8%AE%BE%E8%AE%A1)/[articles](https://www.zhihu.com/column/kls-software-arch-world)); and from eBay's [[1]](https://mp.weixin.qq.com/s/bnhXGD7UhwTxL8fpddzAuw)[[2]](https://mp.weixin.qq.com/s/Xyvfx9mLKqquulnrhFi42Q), [Alibaba's](https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzA5OTAyNzQ2OA==&mid=2649721202&idx=1&sn=97b3edaa344a1d901ee6ad4b8c4830e4), or [AWS's](https://mp.weixin.qq.com/s?__biz=MzI4OTc4MzI5OA==&mid=2247520243&idx=1&sn=dfce28433ff14ef188055dc5daf67bd7).


## Common architecture styles

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

  * __Cloud native__. The system is designed to run exclusively on cloud infrastructure (but to be hybrid cloud). The typical example is [Snowflake](https://www.usenix.org/conference/nsdi20/presentation/vuppalapati) database. Key designs are: 1) Disk file persistence are offloaded to __S3__. 2) Memory caching, query processing, storage are __disaggregated__ and can independently scale-out and be elastic for traffic surge. 3) Read path and write path can separately scale, where typical users generate write contents in steady throughput and read traffic in spikes. 4) Different tiers of resources, since fully disaggregated, can accurately charge billing for how much a customer actually uses.  __Serverless__ is another topic, where all the heavy parts like database and programming runtime are shifted to cloud. Programmers focus on writing functions to do what business values, lightweighted and elastic to traffic.

// TODO Add pic about Snowflake architecture

  * __DDD onion architecture__. The onion (or call it hexagon) architecture comes to shape in the context of DDD. Domain model is the central part. The next layer outside is applications. The outer layer are adapters that connects to external systems. Onion architecture is neutral to the actual technical architecture being implemented. Domain models can also be connected test cases to easily validate business logic (rather than the verbosity of preparing testbed with fake data in databases, fake REST interfaces, etc).

// TODO Add pic about DDD onion the classic architecture

  * __[React-Redux](https://medium.com/mofed/react-redux-architecture-overview-7b3e52004b6e)__. The architecture is a more advanced version of MVC. With data pulled from server-side, Javascripts at client-side runs MVC itself. Views are constructed by templates + input properties. User actions generate events, which trigger actions, e.g. call services. New updates are sent to reducer, which then map to store. Container uses selectors to fetch states from store, map them to properties, and then finally render the new view. The architecture is also frequently accompanied with Electron and NodeJS to develop rich client Apps with web technologies.

// TODO Add pic Reach-Redux architecture the workflow loop chart, which should find from the official site


## General architecture principles

Most principles are already reflected in the above sections. At __architecture level__, the most mentioned principles are below [three](https://xie.infoq.cn/article/5e899856e29017c1079b3be86)

  * __Keep it simple__. There are enough complexity; simple is precious. Related to [KISS](https://en.wikipedia.org/wiki/KISS_principle).

  * __Suitable__. Enough for the need, is better than "industrial leading". An architecture should be suitable, to steer it with your concrete requirement and team resources, rather than to vainly pursuit new technologies. Be frugal. The benefit of a design should be mapped to financial cost to evaluate.

  * __Designed for evolving__. Business needs are changing. Traffic scale are increasing. Team members may come and go. Technologies are updating. An architecture should be designed evolvable. The architecture process (and development) should be carried out with a [growth mindset](https://www.youtube.com/watch?v=M1CHPnZfFmU). An example is [Ele.me Payment System](https://mp.weixin.qq.com/s/mtPQLSONUCWOC2HDPRwXNQ), which is quite common for Internet companies.

More principles come to __component level__ design. [CoolShell has a very good post](https://coolshell.cn/articles/4535.html) to list all of them. Below lists what I think are useful

  * __Keep It Simple__, Stupid (KISS), You Ain't Gonna Need It (YAGNI), Don't Repeat Yourself (DRY), Principle of Least Knowledge, Separation of Concerns (SoC): That said, make everything simple. If you cannot, divide and conquer.

  * Object-oriented __S.O.L.I.D__. Single Responsibility Principle (SRP), Open/Closed Principle (OCP), Liskov substitution principle (LSP), Interface Segregation Principle (ISP), Dependency Inversion Principle (DIP). Note that though OO principles try to isolate concerns and make changes local, refactoring and maintaining the system in well such state however involves global knowledge of global dependency.

  * __Idempotent__. Not only API, the system operation should be idempotent when replayed, or reentrantable. A distributed system can commonly lost message and do retry. Idempotent examples can be doing sync (rather than update, sync a command to node, which is consistent after node fail-recovers and re-executes); propagating info in __eventual consistency and in one direction__; re-executing actions without side effect; __goal states__ commonly used in deployment and config change. 

  * __Orthogonality__. Component behavior is totally isolated from each other. They don't assume any hidden behaviors from another. They work, no matter what others output. Not only the code path, also the development process can be orthogonal, with a wise cut of components. Orthogonality greatly saves the mind burden, communication cost, and ripple impact of changes.

  * __Hollywood Principle__, don't call us, we'll call you. Component doesn't `new` components. It's however the Container who manages Component creation and initialization. It's inversion of control, or dependency injection. Examples are [Spring DOI](https://www.baeldung.com/spring-dependency-injection), [AspectJ AOP](https://docs.spring.io/spring-framework/docs/4.3.15.RELEASE/spring-framework-reference/html/aop.html). 

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







// TODO system property design patterns, integrate architecture design patterns in Mattflower's blog
  1. use 质素分布 to derive a continuous graph: metadata/data consistency, data layout, scaleout, availability, durability, 
                            components: metadata, data node, allocator, compression, memory, indexing
  2. for a continuous space cut, I first talk about component division, then goto workflow (read, write), then go to system properties division
       this should be able to cover all typical systems, e.g. storage, (distributed) filesystem, graphdb, OLAP/TP/HP databases, data lakes, etc
    1. next, system properties maps to design goals and usecase scenarios. this is where I should apply different technique spaces. Use technique spaces to achieve system goals and usecase scenarios.
       the applied technique space then affects on the component division and workflow division, thus affects the designs
    2. I should be able to plot a table then to summarize the above. to put each typical product onto one of the component division, and workflow division plot. and then predict new type by combining different combos

    3. Show the important source of such design patterns, and also mention the highly interleaved.
       papers, reference archs, books, mattflower design pattens, 

// TODO design space analysis




------------------------------











// TODO I should insert more pictures also in former parts to help reading. too many words 
// TODO Add my materials in OneDrive to a zip and link to this article




















-- Key system properties and their design patterns

let's use consultant thinking to handle this chapter. systematic breakdown, and probe with structure



e.g. concurrency of web services, concurrency of manycore
读写分离、CAP


-- key db.cache, etc systems and their design spaces


put the LSM tree paper here
  constructing and analyzing the lsm compact design space
  http://vldb.org/pvldb/vol14/p2216-sarkar.pdf
  LSM-based Storage Techniques: A Survey
  https://zhuanlan.zhihu.com/p/351241814
  https://arxiv.org/pdf/1812.07527.pdf

put disk data layout paper here
  // TODO OK .. this section is basically following database each layers?
  Check with CMU 15-721 courses, the structure is basically what I need

Another design space example: Optimal Column Layout for Hybrid Workloads (presented at VLDB 2020)
  https://www.youtube.com/watch?v=AsjqfidHNAQ
  https://stratos.seas.harvard.edu/files/stratos/files/caspervldb2020.pdf
 
  For design space, also remember the Dostoevsky LSM paper
    https://scholar.harvard.edu/files/stratos/files/dostoevskykv.pdf

another design space example: Building Enclave-Native Storage Engines for Practical Encrypted Databases - use the table 1 for plotting
  http://vldb.org/pvldb/vol14/p1019-sun.pdf


Reference to Book Designing Data-Intensive Applications
  https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/



------------

metadata size and degree of freedom, the very good insight theory

Patterns of Distributed Systems - martinfowler
https://martinfowler.com/articles/patterns-of-distributed-systems/
  Add service registry
  Add shared nothing, in web server, and concurrency design

Break the barrier and build consensus. Cross team collaboration
  What's the biggest challenge in architecturing?


-----------

Cost modeling involved in architecture design, examples
  Casper: Optimal Column Layout for Hybrid Workloads: section 4.4
    https://stratos.seas.harvard.edu/files/stratos/files/caspervldb2020.pdf
  Access Path Selection in Main-Memory Optimized Data Systems: Should I Scan or Should I Probe?    [2017, 33 refs, CMU 15-721]
    https://www.eecs.harvard.edu/~kester/files/accesspathselection.pdf
