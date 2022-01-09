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

The next and following chapter tell about knowledge points in software architecture. But this first chapter tells about the engine that generates the knowledge.

__Reality, language, human mind__

Firstly, __the modeling of the world is human language__. Human language evolved for thousands of years, enriched by distinctive civil culture, polished by daily interaction among population, and tested by full industry use and creation. Grab a dictionary you learn the world and mankind. 

Next, the modeling tool is also a model of the model-er itself. I.e. __human language is also the modeling of human mind__. Thinking is carried and organized by language. Language is structured in the way how human mind is capable to perceive the world, rather than how necessarily the world itself has to be. E.g. software designs by high cohesion low coupling, which is also the principle of how words are created in language. Like they are to reduce software complexity, they do because human thinks this way.

We can say __human language, mind, and the perceivable reality are isomorphic (of the same structure)__. The expedition into the outer world is the same way with exploring into the deep heart. Losing a culture, a language, is the same with losing a piece of reality. As the two sides of a coin, human language is both the greatest blessing how mankind outperforms other creature beings, and also the eternal cage how farthest human mind is capable to perceive.

__About software architecture__

Software architecture is a language, a modeling of the reality world, and a human mind creation that to assist human mind. __The essence of software architecture__ is to [honestly reflect the outer world](https://www.zhihu.com/question/346067016), to introspect into the inner mind, and to conceptually light up where it is dark missing. The answer is already there, embedded in the structure, waiting to be perceived.

The question is not what software architecture itself is, nor to learn what software architecture has, but to understand the landscape of world and mind, where you see the hole that needs "software architecture" to fill. You __predict and design__ what "software architecture" should be, can be, and will be. There can be 3000 different parallel worlds each with a different software architecture, what we have now is just one.

Besides, __knowledge and experience are themselves good designs__. They are essentially a domain language, a reusable piece of world modeling, thus also explains why they are useful across work and even make substitution of design skills. Knowledge is not about to learn, but to observe the art of design tested by human act.

__Side notes: explaining with examples__

For __"high cohesion low coupling" in human language__, imagine an apple on a disk. People name them with "apple" and "desk", rather than a "half apple + half desk" thing. Like selecting what to put into an object in Object-Oriented (OO) design, the naming "apple" and "desk" practices "high cohesion low coupling".

To drill deeper, "high cohesion" implies going together. The __underlying axis is time__, during which the apple goes with itself as a whole. The edges of the apple and the desk intersect, but they have different curves, and they can be decoupled (separated if you move them). The __underlying axis is space__. Human senses apple and desk with basic elements like shape and color. These __sense elements__ grow on axes of time and space, to be processed into human language. The processing principles look like those from software design, or to say, software design principles are crafted to suit human mind.

An imagined creature can have a totally different language system and thinking mind, if they do not rely on visual sights like human, or even not with time and space axes. They may not need "high cohesion low coupling" as a thinking principle neither, if they process information like how organic biology evolve. 

For __human language is also a cage__, remember language is a modeling of the reality. __Modeling__ implies "less important" information are dropped to ease the burden of human cognition. Are they really less important? Words are to __reuse__ the same concept for events happened at different time, which saves duplicates. But are they really duplicate? The necessity of language is itself a sign that human mind is unable to process "full" information; the ability is crippled, limited, caged.

More, human mind can hardly think without underlying __time and space__. Human words, at the bottom layer of the abstraction tower, can hardly go without "human-organ-oriented" __sense elements__. People frequently need daily chats, to sync drifts on abstract concepts. Even language itself is becoming a bottleneck, between human-to-machine, population-to-population information exchange.

For __"software architecture" hole in the world and mind landscape__, you all see more in the following of the article. Though most associate "software architecture" with technology, it is also determined by organization and process needs. Various "needs" in different domains flow into the gap of "software architecture", crafted to be processed and expressed in a suitable language for human mind. Together they evolve into the internal meaning of "software architecture".

For __predict and design what "software architecture" should be__. It can be explained as the method of learning. The plain way is the learn what it is, the structure, the composition, cover the knowledge points, and practice using. The better way is to first understand the driving factors, landscape, and dynamics behind. You can see the source and direction of it, even to the end and final limitation. You can also see the many different alternatives, possible to happen, but eventually not chosen by the real world industry, due to certain reason in the back. You should be able to define your own methodology, given your local customized needs. You can forget the knowledge and create any on your own.


## Why need software architecture

There are various aspects why software architecture is necessary, besides technology. These aspects together define what software architecture should be, and correspondingly the methodology and knowledge landscape developed.

Technology aspects

  * __Handling the complexity__. Software design are separated into architecture level, modular level, and class level. Each level popularize with own techniques: 4+1 view, design patterns, refactoring. Any challenge can be solved by adding one layer of abstraction.

  * __Decide key technology stack__. Internet companies commonly build services atop opensource stacks across different domains, e.g. database, caching, service mesh. Which stack to use affects architecture, and are often evaluated with technology goals and organization resources.

  * __Cost of faults__. The cost of correcting a fault at early design is way lower than at large scale implementation, especially the architecture level faults that need to restructure component interconnects.

Capturing the big

  * __Non-functional requirements__. Typically, availability, scalability, consistency, performance, security, COGS. More importantly, possible worst cases, how to degrade, critical paths. Also, testability, usability, quality, extensibility, delivery & rollout. They are not explicit customer functional needs, but usually more important, and touches wide scope of components to finally implement.

  * __Capturing the changing and non-changing__. Architecture design identifies what changes quickly, and what can be stable. The former is usually localized and encapsulated with abstraction, or outsourced to plugin. The later is designed with an ask "can this architecture run 1/3/5 years without overhaul", usually reflect to components and interconnections.

  * __Issue, strategy, and decision__. Architecture is where to capture key issues in system, technology, organization. Strategies are developed to cope with them. And a explicit track of design decisions are documented.

  * __Clarify the fuzziness__. At architecture step, not uncommon the customer requirements are unclear, problems are complex and clouded, future is unstable, and system scope is unknown. The architecture role analyze, define, design solution/alternatives, and build consensus across team.

Process & Organization

  * __Project management__. Architecture step is usually where the cost effort, touching scope, delivery artifact, development model; and resource, schedule, quality can be determined and evaluated. Project management usually works with the architecture role.

  * __Review and evaluation__. Architecture step is usually where the key designs are reviewed; the key benefit, cost, risk are evaluated; throughput capacity breakdown are verified; and all user scenarios and system scenarios are ensured to be addressed.

  * __Cross team collaboration__. Architecture touches various external systems and stakeholders. It is when to break barrier and build consensus cross teams, BUs. It is when to ensure support and get response from key stakeholders. It is where to drive collaboration.

  * __Tracks and lanes__. The architecture role usually builds the framework, and then the many team members quickly contribute code under given components. It sets tracks and lanes where the code can grow, and where not. I.e. the basis of intra-team collaboration.


## Different architecture organization styles

What an architecture role does and means in real world industry are somehow puzzled. From my experience, this is due to architecture step is organized differently at different companies. At some, architect is the next job position of every software developer; at some others, I didn't see an explicit architect job position. 

  * __Architect the tech lead__. Usually seen at Internet companies. The architecture role is taken by a senior guy in the team, who masters technology stacks and design principles. The architect makes decision on which technology stack to use, and builds the framework for the following team members to fill concrete code. The architecture role is in high demand, because Internet companies quickly spin up Apps after Apps, each needs its architect, while the underlying opensource infrastructure is relatively stable. Both the business value and technology stack win traction.

  * __Architecture BU (i.e. department)__. Seen at Telecom companies. Architects work with architects, software developers work with software developers; they locate at different BUs. The architecture results are handed off in middle, following a waterfall / CMMI model. The architecture designs on more stable, even standardized requirements, with very strict verification, and delivers completeness of documentation. Strong process, and expect more meetings bouncing across BUs. Employees tends to be separated into decision making layer and execution layer, where the later one expects long work, limited growth, and early retire. 

  * __Peer-to-peer architect__. Usually seen at teams building dedicated technology. Unlike Internet companies spinning up Apps horizontally atop many different technologies, such team vertically focuses on one, e.g. to build a database, a cloud storage, an infrastructure component, i.e. 2C (former) vs 2B (later) culture. No dedicated architect job position, but shared by everyone. Anyone can start a design proposal (incremental, new component, even new service). The design undergoes a few rounds of review from a group of senior guys, not fixed but selected by relevance and interest. Anyone can contribute to the design, and can join freely to set off with project development. Quite organic. Technology is the key traction here, where new architecture can be invented for it (e.g. new NVM medium to storage design).

  * __System analyst__. Usually seen at companies selling ERP, or outsourcing. The systems are heavily involved into customer side domain knowledge. And the domain knowledge is invalidated when selling to another customer from a different domain. Because of new background each time, comprehensive requirement analysis and architecture procedures are developed. When domain can be reused, domain experts are valued, where __knowledge and experience themselves are good designs__. Domain knowledge can win more traction than technology, where the later one more lean to stability and cost management.

  * __Borrow and improve__. Usually seen at follower companies. If not edge cutting into no man's land, __reference architecture__ (top product's architecture) can usually be found to borrow from, to customize and improve. This is also benefited by the wide variety of opensource. Reference architecture, standing on the shoulder of giants, are widely used in software architecture processes, e.g. comparing peer works, which is another example of knowledge and experience themselves are good designs. Market technology investigation survey are high demand skills.


## Key processes in software architecture

As preparation, architecture design requires below knowledge and skills

  * Downstream, __understand your customer__. The customer here also includes downstream systems that consume yours. Know customer to capture key aspects to prioritize in architecture, and more importantly what to de-prioritize (E.g. favor latency over cost? Is consistency and HA really needed?). It helps identify the risks (E.g. festival burst usage, backup traffic pattern). Besides, well defining customer space reveals future directions the architecture can evolve.  

  * Upstream, __understand what your system is built atop__. A web App can be built atop a range of server engine, service mesh, database, caching, monitoring, analytics, etc. Mastering the technology stacks is necessary for designing architecture that works with the practical world, and for choosing correct technology stacks that suit project goals and team capabilities. 

  * Externally, __understand the prior of art__. To design a good system, you need to know your position in the industry. Reference architecture can be discovered and borrowed from. Existing technology and experience should be leveraged. E.g. given the richness of opensource databases, designing a new data storage is even a selection and cropping of existing techniques. Participating in meetups helps exchange industry status, and to ensure your design is not drifting away into a pitfall. 

  * Internally, __understand your existing system__. Understand the existing system to make designs that actually work, and to correctly prioritize what helps a lot and what helps little. Learn from past design history, experience, and pitfalls, to reuse and go the right path. 

  * Organizationally, __broaden your scope__. Architecture design involves interacting with multiple external systems and stakeholders. Besure the broaden your scope and get familiar with them. Communicate with more people. Solid soft skills are needed for cross team / BU collaboration, to break barrier and build consensus, and to convey with action-oriented points, concise, big picture integrated with detailed analysis.

I lean more to peer-to-peer architect style mentioned above. Many can be sensed from [GXSC's answer](https://www.zhihu.com/question/24614033/answer/497338972). At each step, besure to engage __talk with different persons__ which significantly improves design robustness. Rather than the design results, it's problem analysis and alternative trade-off analysis that weight most.

  * Firstly, __problem analysis__. Design proposal starts from [innovation](/technology/Notes-on-How-to-do-Innovation). Finding the correct problem to solve is half-way to success. The cost and benefit should be translated to the final __market money__ (Anti-example: we should do it because the technology is remarkable. Good-example: we adopt this design because it maps to $$$ annual COGS saving). The __problem scope__ should be complete, e.g. don't miss out upgrading and rollout scenarios, ripple effect to surrounding systems, or exotic traffic patterns that are rare but do happen in large scale deployment. __Risk__ should be identified, covering technology, market, organization, and external systems. The key of management is to peace out risk, same with managing the design.

  * One important aspect from problem analysis is __prioritization__. Architecture design, even the final system, cannot address each problem. You must decide __what to discard__, what to suppress, what to push down to lower level design, what choices to make now and what to defer, what to push into abstraction, what to rely on external systems, what to push off as future optimization; and to decide what are the __critical properties__ you must grasp tightly throughout the project lifetime and monitor end-to-end. Prioritization are usually determined by organization goals, key project benefits and costs, and the art to coordinate across teams.

  * Next, __find alternatives__. To solve one problem, at least two proposals should be developed. __Trade-off analysis__ is carried out to evaluate the Pros and Cons. Usually, Pros yet have special cases to make it worse, and Cons yet have compensations to make it not so bad. The discussion is carried out across team members, up/downstream teams, stakeholders, which may in turn discover new alternatives. The process is __iterative__, where the effort is non-trivial, multiplied, because it's not developing one but a tree of solutions. Eventually you explored the completeness of __design space__ and __technology space__, and reached consensus across team. Choosing the final alternative can be carried out with team voting, or with a [score matrix](https://www.productplan.com/learn/prioritization-matrix-example/) to compare.

  * __Review__ with more people. Firstly, find one or two local nearby guys for __early review__, to build a more solid proposal. Next, find __senior and experienced__ guys to review, to make sure no scenarios are missing, all can be reused are reused, and the solution is using the best approach. Then, involve key __upstream__ guys, to ensure required features, load level, and hidden constraints, are actually supported; and to ensure their own feature rollout won't impact yours. Involve key __downstream__ guys, to ensure the new system addresses what they actually want. It's important to involve key __stakeholders__; make sure you gain support from organization, you deliver visibility, and you align with high level prioritization.

  * Then __evaluation__ for the architecture design. Make sure the problem analysis, every customer __scenario__ and system scenario, and project goals, are well addressed. Make sure __non-functional__ requirements are addressed. Make sure the key project __benefit and cost__ are verified in a data driven approach, with actual production numbers as input, using a prototype, simulation tools, or math formulas to model. Make sure the system can support required __load level__, by breaking down throughput capacity into each component. Make sure the system handles the __worst case__ and supports graceful throttling and downgrade. Make sure the __logic has completeness__; e.g. when you handle a Yes path, you must also address No path; e.g. you start a workflow, you must also handle how it ends, go back, interleaved, looped. Make sure __development and deliver__ are addressed, e.g. how to infra is to support multi-team development, the branching policy, component start/online/maintenance/retire strategies, CI/CD and rollout safety. Also, make sure __hidden assumptions__ and constraints are explicitly pointed out and address.

  * Finally, it's the __documentation__. On practice, it involves a short "__one-pager__" document (actually can be < 20 pages), and slides for quick presentation, and spreadsheets for data evaluation. Nowadays culture lean more to lightweight document, central truth in codebase, and prioritize agile and peer-to-peer communication. Problem analysis and alternative trade-off analysis usually weight more in document. Architecture design part usually includes key data structure, components, state machines, workflows, interfaces, key scenario walkthrough, and several detailed issue discussion. Importantly, the document should track the change history of design decision, i.e. how they reach today, and more specifically the __Issue, Strategy, Design Decision__ chain. 

  * Another output of architecture design are __interfaces__. Interface design does have principles (see later). They are the tracks and lanes where following development start. They reveal how components are cut and interactions to happen. They also propagate expectations of your system to external systems, such as how they should co-work, what should be passed.

__Architecture is designed to evolve__, and prioritized to make it evolve faster. [Ele.me payment system](https://mp.weixin.qq.com/s/mtPQLSONUCWOC2HDPRwXNQ) is a good example in a 5 year scope. Competency of nowadays software depend on the velocity it evolves, rather than a static function set. 

  * __[Simple is beauty](https://xie.infoq.cn/article/5e899856e29017c1079b3be86)__. Initial architecture usually only address key requirements. What changes and not changes in several year's scope are identified and addressed with abstraction. __[MVP](https://en.wikipedia.org/wiki/Minimum_viable_product)__ is a viable first deployment, after which it yet becomes challenging how to "replace wheels on a racing van". 

  * __Highway is important__. Functionalities in software resembles to tall buildings in a city, where highways and roads are key how they build fast. These architecture aspects are less visible, usually under prioritized, but are life critical. Inside the system, they can be the debugability, logging, visibility and monitoring. Have they defined quality standards? Do monitoring have more 9s when the system is to be reliable? From infrastructure, they can be the tooling, platform, config system, fast rollout, data obtaining convenience and analytics, scripting. At organization level, they can be the team process and culture to facilitate agile move. Externally, they can be the ecosystem and plugin extensibility. E.g. [Chrome](https://developer.chrome.com/docs/apps/first_app/) designs with plugin support to incubate the ecosystem. E.g. [Minecraft](http://gametyrant.com/news/5-best-modding-tools-for-minecraft) even publish tools to build 3rd-party mod. E.g. [Opensource Envoy](https://mattklein123.dev/2021/09/14/5-years-envoy-oss/) designs for community engagement from day 1.

  * Build the __feedback loop__. Eventually after project rollout and deploy, you should be able to collect data and evaluate the actual benefit and costs. New gaps can be found, and yet facilitate a new round of design and improve. How to construct such feedback loop should be taken into consideration of the architecture design. 

The last point is about __driving the project__. The architecture role is usually accompanied with ownership, and be responsible to the progress and final results. Driving goes not only the architecture step, but also along with entire project execution. Many can be sensed from [Daoyan's article](https://mp.weixin.qq.com/s?fontRatio=1&__biz=MzA5OTAyNzQ2OA==&mid=2649721202&idx=1&sn=97b3edaa344a1d901ee6ad4b8c4830e4).

  * There can be timeline schedule issues, new technical __challenges__, new blockers, more necessary communication with up/downstream; previous assumptions may not hold, circumstances can be __changed__, new risk will need engage; there can be many people join and many needs to coordinate, and many items to follow up.  

  * Besides the knowledge and communication skills, driving involves the __long time perseverance__, attention, and care. The ability to find real problems, to prioritize and leverage resources, to push, the experiences, and the skillset of __project management__, are valued. To drive also means to __motivate__ team members to join and innovate. The design becomes more robust, completed, improved, with more people help; and with people from __different perspectives__ to look.

  * More, __driving is a mindset__. You are not who asks questions, people ask questions to you, and you are the final barrier to decide whether problem is solvable or not. The most difficult problems naturally go to you. If solving the problem needs resource, you make the plan and lobby for the support. You make prioritization, you define, and you eat the dogfood. The team follow you to success (if not otherwise). 


## Key methodologies in software architecture

Software architecture is a large topic that I didn't find a canonical structure. I divide it into process (above), methodologies (this chapter), principles, system properties and design patterns, technology design spaces. The article is organized as it.

  * __Process__. Already covered in the above chapters. It involves how real world organizations carry out architecture design, and conceptually what should be done for it. 

  * __Methodologies__. The analysis method, concept framework, and general structure, to carry out architecture design. They also interleave with principles and philosophy. Methodologies change with culture trends, organization styles, and technology paradigms. But throughout the years, there are still valuable points left.

  * __Principles__. Architecture level, component level, class level each has many principles, common or specific. Essentially they are designed to reduce mind burden, by letting the code space to mimic how human mind is organized.

  * __System properties and design patterns__. Distributed systems have non-functional properties like scaleout, consistency, HA (high availability). Various architectural design patterns are developed to address each. They are the reusable knowledge and domain language. Best practices can be learned from reference architecture, more market players, and historical systems; where __architecture archaeology__ systematically surveys though the past history of systems.

  * __Technology design spaces__. A technology, e.g. database, can evolve into different architectures after adapting to respective workload and scenarios, e.g. OLAP vs OLTP, in-memory of on disk. Exploring the choices and architectures, plotting them on the landscape, reveals the design space. With this global picture in mind, the design space landscape greatly helps navigating the new round of architecture design.

__Managing the complexity__

The first and ever biggest topic in architecture design (or software design), is to __handle the complexity__. The essence is to __let the code space mimic human mind__, i.e. how the human language is organized (if you have read the philosophy chapter). Human language is itself the best model of the complex world, which is a "design" polished by human history, and yet shared by everyone. Domain knowledge is thus helpful, as it is the language itself. When code space is close to the language space (or use a good metaphor), it naturally saves everyone's mind burden.

Below are conceptual tools to handle complexity. 

  * __Abstraction__. Any challenge can be solved by adding one layer of abstraction. The tricky part is you must precisely capture, even predict, __what can change and what not__. It's non-trivial. E.g. for long years people try to build abstract interface across Windows API and Linux API, but today what we have is write once glitch somewhere. You still need to examine down the abstraction tower to the bottom. Because coding interface cannot constraint all __hidden assumptions__, and non-functional properties e.g. throughput and latency. Information in the flow can become missing and distorted, after passing along the abstraction tower, resulting in incorrect implementation.

  * __Information flow__. Typical design captures how code objects flow around the system. But no, you should capture how __information described in human language__ flow around the system. Language information is __symmetric__ at the sender and receiver components, but the implementation and representation varies (e.g. you pass "apple" across the system, rather than DB records, DAO, bean objects, etc). __Dependency is essentially a symmetry__, where it's possibly no code references, but semantics linked (e.g. apple has color "red", that's where everywhere of your system must handle correctly). Language information carries the __goal__, which the code should align to, i.e. the code should align to the __human language model__. Human language is consistent compared to the code objects passing in the system; the later one becomes the __source of bug__ when misalignment happens at different layers of system. The design principle eventually leads to "__programming by contract__", "__unbreakable class__" (a component should work, with no assumptions to the outside, regardless what the caller passes into), semantics analysis; but more to learn from. 

  * __High cohesion low coupling__. Human concepts, or say words in language, are all constructed following the rule of "high cohesion low coupling". This is __how human mind works__, and to follow which, the code design saves mind burden. The topic is related to __change and dependency__. High cohesion encapsulates changes, which localizes code modification impact. __Changes pass along the wire of dependency__, that's why low coupling works to reduce undesired propagation. Good encapsulation and delegation requires to predict future changes, which is usually not easy; instead of adding unnecessary OO complexity, it oppositely leads to another [KISS](https://en.wikipedia.org/wiki/KISS_principle) design. 

  * __Name and responsibility__. The most difficult thing in software design is giving names. It's not to say fancy names are hard to find, but to say, __being able to name something means you have already grouped the concept in a high cohesion way__ (e.g. you can name "apple", "desk", but cannot name "half apple + half desk"), which inherently leads to good design. Next, __a name defines__ what a thing is, is not, can do, and cannot do; that's the responsibility. Saying objects should call be their names, is to say objects should call by interfaces and responsibility. Finally, when you can __describe the system with fluent human language__, i.e. with __good names and information flows__, you are naturally doing the good design. To do it better, you can organize the talk with consistent abstraction levels, rather than jumping around; if so, it means the design abstraction levels are consistent and self-contained too. Remember __design is a modeling to human language__ (if you have read the philosophy chapter).

  * __Reuse__. If a component is easy to reuse, it naturally follows high cohesion and good naming responsibility. Design for reuse is recommended, but avoid introduce extra encapsulation and delegation, which results in high OO complexity. Refactor for reuse is recommended, but refactor usually requires global picture knowledge, which contradicts with the goal that changes should be localized. __Reference architecture__ is another reuse to reduce mind complexity. Find the top product and opensource to learn from. Find the popular framework which teaches good designs. The past experience here becomes its domain knowledge, shared by team members, and changing points are more predictable. 

  * __Component boundary__. Separating components and sub-components eases mind memory usage. Component boundary should be cut at what changes together. If an upstream service change is frequently coupled with a downstream service change, they should have been put into the same component. Violating it is the common case where micro-service messes up the system. High organization collaboration cost is another place to cut component boundary, see [Convey's Law](https://en.wikipedia.org/wiki/Conway%27s_law).

Design complexity can be formulated and evaluated using scores on dependency. I found [D Score](https://book.douban.com/subject/26915970/) interesting. And this [article](https://thevaluable.dev/complexity-metrics-software/) lists other measures. These methods are less popular probably because domain knowledge is more effective to handle complexity. In general,

  * "D Score" measures software complexity by the number of dependencies. Dependency links inside the component is adding to cohesion, otherwise adding to coupling if pointing to outside. The two types of dependency links are summed up, with a formula, as the final score.

  * "Halstead Metrics" treat software as operators and operands. The total number of operators and operands, unique numbers, and operand count per operator, are summed up, with a formula, as the final score.

  * "Cyclomatic Complexity" treat software as control flow graph. The number of edges, nodes, and branches, are summed up, with a formula, as the final score.

__Levels of software design__




// TODO 3 layers of architecture design
    // TODO books of DD for middle leve, code complete/refactor for class level
    // TODO give a picture?
        // TODO I should insert more pictures also in former parts to help reading. too many words 
    // TODO what each layer does, focus on, and principles?



// TODO the 4+1 view
  // TODO other architecture paradigm

// TODO architecture styles





-- Key methodologies in software architecture

4+1 view
three layers of architecture, 高中低三层架构整理



四横三纵架构
business,data,app,tech architectures

tech bet, reliability budget,

---- handling complexity, managing complexity,

name and responsibility
coherent and coupling


depend on the stable. abstraction, interface, DIP, arch boundary, ISP.  高内聚低耦合，cut by 耦合min。they are all can be explained. 
The D score in clean architecture book is interesting. measures stable / abstraction. write it. 
广义关联dependency。语言模型。















-- Key principles of architecture design

Simple is beauty, 架构三原则: https://xie.infoq.cn/article/5e899856e29017c1079b3be86

various principles from left ear mouse blog

API design principles, interface design principles
left ear mouse's principle summary


state machine, etc






-- Key styles of architecture design

mapping to real world and organization (convey's law)
different architecture styles
data flow



-- Key system properties and their design patterns

e.g. concurrency of web services, concurrency of manycore
读写分离、CAP
正交，可重入，幂等

-- key db.cache, etc systems and their design spaces


put the LSM tree paper here
  constructing and analyzing the lsm compact design space
  http://vldb.org/pvldb/vol14/p2216-sarkar.pdf
  LSM-based Storage Techniques: A Survey
  https://zhuanlan.zhihu.com/p/351241814
  https://arxiv.org/pdf/1812.07527.pdf

reference to the aws guy's answer
reference to in nek's blog: https://zhuanlan.zhihu.com/p/153030979, but also use the git version
OK .. add reference to each other articles I found interesting?
  https://mp.weixin.qq.com/s/bnhXGD7UhwTxL8fpddzAuw

system perf tuning from in reck's blog about that Linux