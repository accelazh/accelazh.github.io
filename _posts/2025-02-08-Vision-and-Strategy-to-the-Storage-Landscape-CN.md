---
layout: post
title: "Vision and Strategy to the Storage Landscape (Chinese Simplified)"
tagline : "Vision and Strategy to the Storage Landscape (Chinese Simplified)"
description: "Vision and Strategy to the Storage Landscape (Chinese Simplified)"
category: "My Book"
tags: [cloud, storage, vision, strategy, hardware, market]
---
{% include JB/setup %}

# Vision & Strategy 洞察、远见与策略

Vision 与 Strategy 始于提问，1 年、3~5 年后、乃至 10 年后，我们应该处于什么位置，团队和部门应该在做什么，应该以什么样的方式工作。Vision 并不是指寻找最新技术趋势，并学习和应用它们。Vision 是“当事者”需要预测正确的技术趋势，确定投资方向，并用数据驱动和系统分析支持其的结论。

总的来说，其思考方式更接近于 __产品经理__、__商业分析__（Business Analytics）、__市场调研__（Market Research），而不是技术开发工作。当然，向内，其也需要良好的技术基础（见 [A Holistic View of Distributed Storage Architecture and Design Space](https://accelazh.github.io/my%20book/A-Holistic-View-of-Distributed-Storage-Architecture-and-Design-Space)）。向外，其需要勘测市场和竞争对手，以及我们的位置。向前，其需要对趋势和规模（Scale）的预测。

为什么需要 Vision 与 Strategy？有许多方面的原因：

  * __职业发展__：随着级别的提高，职位期望从接收 __输入__ 逐渐变为提供 __输出__。例如，__初级个人开发者__ 关注做好被交给的任务，从管理者接收输入。而 __有经验的个人开发者__ 常常需要制定项目的策略（包括技术上的），并日常地为管理者提供输入，例如可能的创新方向、团队的发展空间。__管理者__ 的工作则更接近于投资（见 _[关于市场的分析](.)_ 章节），洞察未来趋势并执行正确的策略，是本职工作之一。见 [[95]](.)

  * __长远计划__：更高的职位期望能够 __管理更长的时间跨度__。例如，__初级开发者__ 大约需要制定未来 3 个月的计划，而 __有经验的个人开发者__ 常常需要制定未来 1 年的计划。__管理者__ 则更长，往往需要看到未来 3~5 年的，在项目管理计划外，更多的是团队发展的远见和策略。见 [[95]](.)。

  * __Leadership__：Leadership 指在平等交流下，依靠远见和魅力吸引跟随者（__Manage by influence not authority__）。向 Leadership 发展要求当事者成为 __Visionary__ 或 __Thought Leader__。当其他人与当事者交流时，应当总是能够受到 __鼓舞__ 和 __启发__（Inspired）。Leadership 也是管理者（Manager）的职位要求之一。见 [[96]](.)。

  * __系统架构__：良好的系统架构常常能够工作 10 年以上，而考虑到存储系统较慢的迭代速度（数据不容损坏），也许开发就花掉 5 年（至成熟稳定）。架构师本质上是在 __面向未来工作__，需要了解未来的市场需求，在未来的技术发展的基础上做出决定。尤其是，硬件能力的发展是指数速度的。另一方面，架构决策需要被映射到 __财务指标__。

  * __创新__（Innovation）：创新是 __日常工作__（见 _[关于市场的分析](.)_ 章节），也是为团队寻找 __发展空间__。创新即包括寻找技术的发展趋势，也包括分析市场的需求变化，即有 __洞察__ 已有系统的“更进一步”，也有问最好的存储系统应该是什么样（Gap Analysis）。寻找创新需要 Vision，实施创新需要 Strategy。

本文主要围绕存储系统，在（云）存储行业的背景下展开。后文将依次讲解“一些方法论”，“理解股价”，“存储系统的市场”，“关于市场的分析”，“存储系统中的硬件”，“案例分析：EBOX” 各个章节。

  * __方法论__ 部分将搭建 Vision 与 Strategy 的思考框架。

  * __股价__ 部分将分析其原理，理解公司的目标，并映射到团队。

  * __市场__ 部分纵览存储系统的竞争格局，并分析市场的关键特性、颠覆式创新、以及价值。

  * __硬件__ 部分建模其能力和发展速度，并深入观察其要点。

  * __案例分析__ 部分将用一个实例实践本文的分析方法，有许多有趣的结论。

![Fun Header Image of Vision](/images/vision-head-image-mosaic.png "Fun Header Image of Vision")

## 目录

* [一些方法论](.)
  * [Critical Thinking](.)
  * [Case Interview](.)
  * [Strategic Thinking](.)
  * [Business Acumen](.)
  * [信息收集](.)
* [理解股价](.)
  * [股价由什么构成](.)
  * [股价应该涨多快](.)
  * [什么推动股价增长](.)
  * [团队的目标](.)
  * [注意](.)
* [存储系统的市场](.)
  * [分类](.)
  * [A. 云存储](.)
  * [A. 主存储](.)
  * [A. 备份和归档存储](.)
  * [B. 文件存储](.)
  * [B. 对象存储](.)
  * [B. 块存储](.)
  * [B. 数据库](.)
  * [C. SSD 存储](.)
  * [C. HDD 存储](.)
  * [C. 磁带存储](.)
  * [C. 内存存储](.)
* [关于市场的分析](.)
  * [市场的结构](.)
    * [客户组成](.)
    * [市场的天然结构](.)
    * [市场的天花板](.)
    * [对相邻市场的渗透](.)
    * [“推论”](.)
  * [市场的生命周期](.)
    * [市场的阶段](.)
    * [新市场的来源](.)
  * [颠覆式创新](.)
    * [渐进式创新](.)
    * [颠覆式创新](.)
    * [颠覆式创新的特性](.)
    * [“推论”](.)
  * [驱动因素](.)
    * [规模增长](.)
    * [新技术](.)
    * [成熟度](.)
    * [商业模式变化](.)
    * [政策合规](.)
  * [什么是价值](.)
    * [关系](.)
    * [复杂性](.)
    * [速度](.)
    * [文化](.)
    * [资产](.)
    * [数据](.)
    * [粘性](.)
    * [垄断](.)
    * [关于：有价值的技术](.)
    * [关于：价值与市场周期](.)
    * [“推论”](.)
  * [总结](.)
* [存储系统中的硬件](.)
  * [数据表](.)
  * [额外成本](.)
  * [与公有云价格的比较](.)
  * [选择 HDD 和 SSD](.)
  * [硬件发展的推动因素](.)
  * [观察和要点](.)
  * [软件的价值在哪里](.)
* [案例分析：EBOX](.)
  * [什么是 EBOX](.)
  * [存储系统的成本收益](.)
  * [研发成本的摊薄](.)
  * [供应商和市场](.)
* [总结](.)
* [引用](.)

## 一些方法论

Vision 与 Strategy 涉及一系列对未来和趋势的思考，以及对企业架构的理解，以使项目获得确实的投资回报。更重要的是，它需要用系统的分析和数据支持预测的结论。总的来说，其思考方式更接近于 __产品经理__、__商业分析__（Business Analytics）、__市场调研__（Market Research），而不单单是技术开发工作。

本章介绍关于 Vision 与 Strategy 的方法论（Methodologies）。将依次介绍 Critical Thinking、Case Interview、Strategic Thinking、Business Acumen、信息收集。介绍内容更多是大体框架，重要的是思考、实践、经验。

### Critical Thinking

Critical Thinking 和批判性思考关系不大，更接近于 Problem Solving。“Critical” 更接近于 Critical Path。之所以用英文名，是因为直接翻译成中文后，含义一定程度发生曲解，下同。LinkedIn 的 Critical Thinking 课程 [[91]](.) 是不错的学习来源。课程包含完整知识，本文仅列出有趣或重要的点，下同。

Critical Thinking 的（部分）重点：

  * __解决根因（Root Cause）而不是症状__。不要直接开始做老板交给你的任务。首先，在上下游、利益人（Stakeholder）中追索，找到真正的、根因的、需要解决的问题。接下来是 __定义问题__，其中最重要的是 Problem Statement 和定义目标。在开始前，将你的定义讲述给其它团队和成员，看是否合理。

  * __高效开展工作__。你需要在 High Road 和 Low Road 中反复切换，Zoom-in/out 视角。High Road 是俯瞰视角，在 20/80 Rule 中，找到有效用的 20%，__Don't Boil the Ocean__。Low Road 在地面视角，例如分析具体数据。其关键是需要不时返回 High Road，检验其业务价值（Business Impact），__Don't Polish the Dirt__。

  * __“Critical” Path__（关键路径）。你解决问题所走过的应该是一条关键路径（图论），每个任务节点必要且不多余（关联下文 MECE）。做老板不关心的工作没有意义。你提供的是 __专业服务__，购买你的服务很昂贵，不要浪费客户的资金。个人开发者不应只有 Low Road。最后，仔细思考任务的 __优先级__。

  * __一些工具__。例如，“__5 Whys__” 用来追索根因。“__Seven So-whats__” 用来推测行动的结果。“__我们过去也这么做__” 是触发 Critical Thinking 的“坏味道”，昨天的策略适合今天吗？__第一性原理__，更直白地说，是将问题分解（Top-down），然后累加（Bottom-up），以合理计算；这类似系统分析的方法。__模仿训练__（Shadow Practice），例如 Gartner 报告，你能否独立分析并得出同样的结果。__切换角度__，例如向另一人讲述，看其如何 Reframe 你的问题。启发式问题，例如，回顾过去 10 年，__如果重新开始__，你会做哪些不同。另一个 __启发式问题__，如何使你的产出指标（Performance Metrics）翻倍？

  * 某种程度上，对 __高层次__（High Level）的关注和对 __细节__ 的关注都是必要的。高层抽象的思考方式具有强大的力量，但如果长期生活在“云端”，则容易陷于思维定势（Stereotype）而无法自我修复（如管理者需避免）。自我修复需要重新进入细节层面，检验已有假设，换句话说是 __第一性原理__。

![Architecture design feedback loop](/images/arch-design-process-loop.png "Architecture design feedback loop")

### Case Interview

Case Interview [[92]](.) 属于商业分析（Business Analytics）或商业咨询（Business Consultant）领域，是面试商业咨询公司如 McKinsey 的一道环节。但实际上，如 Case Interview Secret（Victor Cheng 著）的书中，讲了大量分析业务问题的框架和范例，十分有益，“面试”反倒在其次。

Case Interview 的一些要点：

  * __用 Proxy 估算__。快速估算和口算是商业咨询的基础要求。估算有一系列方法，其中 Proxy 方法较为有趣，例如用街道人流计数、附近门店上座率等，估算新开门店的营业额。Proxy 方法可以更进一步，如按照人口统计分层、确定 Proxy 变量、分解问题，并切换另一 Proxy 来验算。

  * __Mindset__。商业咨询的思考方法和 __Critical Thinking__ 有很多重合，例如 Don't Boil the Ocean、时间昂贵、专业服务。另一方面是 __Independent Problem Solver__：把你独自一人丢到 Fortune 500 企业的某部门中，你能够说服客户（如下面的 Conclusiveness），解决问题，并维护雇主的形象吗？极强的 __Soft Skill__ 是必须的。

  * __Issue Tree Framework__。Case Interview 的经典分析方法是 Issue Tree Framework，例如 Profitability 框架。其要求首先确定假设（Hypothesis），然后将问题逐层分解。分解需要满足 __MECE__ 测试和 __Conclusiveness__ 测试，前者指不重不漏，后者指如果所有分支为 True，那么父节点的结论无法否定。分析过程沿着树逐层深入，然后反向汇总回树根，过程中常常动态调整树的结构。Issue Tree Framework 有大量模板，但使用时常常根据问题定制。

![Issue Tree Framework: Profitability](/images/vision-method-issue-tree-profitability.png "Issue Tree Framework: Profitability")

### Strategic Thinking

Strategic Thinking 用于制定公司策略，尤其是长期策略，其也往往与 Decision Making 捆绑。它是公司在未来 3~5 年后、乃至 10 年后应处位置的行动计划和导航地图。LinkedIn 的 Strategic Thinking 课程 [[93]](.) 有更多讲解。

Strategic Thinking 的一些重点：

  * __Win the Game__。相比 __Critical Thinking__ 中只有“我”和“问题”，Strategic Thinking 要求必须赢得“游戏”,“对手”被添加到图景中。在市场分析的上下文中，其图景更接近 __Porter 五力分析__。

  * __观察__。Strategic Thinking 首先要求观察人和对手，除了趋势，还要注意 Micro-trends。一个要点是 __坏味道__（Bad Small），不仅适用于编程，也适用于组织和文化，例如听到 “我们从未这么做”、“我们过去也这么做”。另一个要点是 __Not be Surprised__，Surprise 是管理中的术语，如果你感到 Surprise，那说明观察未到位。观察之后是思考（Reflection），__It doesn't take time, it takes space__（见课程小节 Embrace the strategic thinking mindset）。

  * __行动__。决定做某件事，意味着决定 __不__ 做另一件事。什么都不做，__也__ 是一个决定。需要注意价值链中的 __乘法__ 效用：你的时间 -> 在任务上的投资 -> 你的策略 -> 在公司层面的成效。问自己，__3~5 年后__，“我”如何 Win the Game，“我”会在哪里。行动意味着建立从长期到短期的任务 __分解__（关联 Issue Tree Framework），最终映射到 Tactics，即每天可具体执行的任务。在执行中，不时 __切换__ High Road 和 Low Road（关联 Critical Thinking）。

  * __Making Informed Strategy__。好的策略（Strategy）不需要是创新的，策略的 __重点在决策__（Decision Making）。首先是市场 __趋势__、经典的 Porter 五力分析。注意从不同 __来源__ 收集看法，包括新老群体，尤其是不同视角的。绘制（Map Out）你的 __资产__（Assets）和 __盟友__（Allies）的图谱。绘制你的 __限制__（Constraints），特别是 __结构性障碍__（Structural Obstacles）的图谱。以及 __SWOT__ 分析。把它们放到上一张 __行动__ 的地图上，需要是现实的（Realistic）、可达到的（Attainable）。

  * __赢得支持__。如何从老板、同事、雇员中赢得支持？不要急于在会议中发布你的策略或计划，此前有大量工作。首先，系统性地 __与利益人会面__，探讨你的计划，得到反馈并解决疑问。可以预见一定有大量反对，重点是你需要 __预见所有可能的反对__（关联 Not be Surprised），用合适的让步和谈判技巧在 __会议前__ 达成一致（关联 BATNA）。最后，确保所有决定和任务是 __Accountable__ 的，例如邮件会议小结、定期复查 Timeline。

  * __监测执行进度__。常见的 __项目管理__ 被用于策略的执行过程。更为重要的是，设立 __预期__（Expectations）和 __假设__（Assumptions）。环境是不断变化的，时常 __重新检验假设__，并问有没有更好的 __选择__（Alternative）。在项目开始前（Upfront）、结束后（Retro）应该 __复查__。高风险的部分需要 __更早、更频繁__ 地执行。

![Points in Strategic Thinking](/images/vision-method-strategic-thinking.png "Points in Strategic Thinking")

### Business Acumen

Business Acumen 从公司的视角，讲解生意是如何开展的，以及如何推进和优化各部分（Pull the Lever）。其覆盖阅读财报、业务模型、策略、经营等方面。LinkedIn 的 Developing Business Acumen 课程 [[94]](.) 有更多展开。

Business Acumen 中一些和本文有关的要点：

  * __财务报告__：对应公司财报，__损益表__（P&L statement）可以被逐层分解：营收（Revenue）-> 扣除 COGS -> 毛利（Gross Profit）-> 扣除经营费用（Operating Expense、SG&A）-> 营业利润（Operating Profit）-> 扣除利率、税收、折旧等 -> 净利润（Net income）。围绕财务表现有很多可调节的 “__杠杆__”（Pull the Lever），对应上文 Profitability 的 Issue Tree Framework。一些是长期的，例如技术研发、设施兴建，一些是短期的，如减产、裁员。你可以尝试从历届财报中得出结论，并与公司发布的管理层报告（Financial Brief）__对比__。

  * __业务模型__（Business Model）：业务模型定义如何从生产商品中盈利，从原料加工角度有 __价值链__（Value Chain），从业务增长角度有 __增长策略__（Growth Strategy），从投资角度有 __ROI__，从成本角度有 __CapEx__、__固定成本__（Fixed Cost）、__可变成本__（Variable Cost）等概念。

  * __运营__（Operation）：业务模型 __驱动__ 公司策略和人员配置，人员驱动运营，最终财务表现在财报上显现。围绕运营，首先是 __策略__（Strategy），在前文中已提及。公司的投资组合构成 __Initiative Pipeline__，其逐次展开实现公司的未来。__营销策略__ 选择并帮助公司掌控客户。__R&D__ 常与 __并购__ 合并考虑，后者节省上市时间，并可以占有对方市场。在竞争中 __保护产品__ 需要策略，例如快速发布，或者版权、专利。__人员策略__ 涉及如何寻找人员、培训、组织架构、流失率等。观察公司在各个职级中开放招聘的岗位，可以了解其人员策略，以 __推测__ 其业务策略。

![Points in Business Acumen](/images/vision-method-business-acumen.png "Points in Business Acumen")

### 信息收集

本节简单讲述如何收集市场信息，以支持 Vision 与 Strategy 分析。

  * __“水下”的信息__（Underwater）。许多前沿的、有价值的信息，常常并未发表。例如论文作者往往提前一年已经知道某有价值的研究方向，并开始研究。而如果只阅读论文的话，一年后才能获知此信息。同理的是各高校实验室、企业研究院、开源社区等。获取“水下”信息更多依赖 __社交__，参与各式会议、面对面交流、寻找合作者、互惠互利。另一方面，公司拥有真实的的 __客户__ 和 __供应链__，从这些关系更容易获得潜在的市场动向，甚至决定之。

  * __投资__。从投资新闻中可以获得新技术的动向。相比阅读论文，获得投资的技术是 __被“金钱”验证__ 过的，并可以根据投资多少衡量其强度。投资新闻常见的有 Startup、融资、收购等等，或者看到某个新公司开始“有钱”在各媒体撰写文章，推广自己了。另一方面，有潜力的论文经常会迅速获得融资并创立 Startup，至少会开设网站。

  * __研究报告__。许多市场研究乐于预测未来方向，例如 Gartner、IDC。虽然企业可能会付费进行推广，但资金充裕的企业至少说明此方向确有发展前景。_[存储系统的市场](.)_ 章节中，将看到更多例子。

## 理解股价

从公司角度，极为重要的目标是股价的增长（甚至是全部目标）。什么样的股价增长是合理的？如何将股价的增长映射到实际产品？对于部门或团队，需要完成什么样的目标以支撑股价？

这个目标进一步分解为团队 3~5 年的计划，映射到 Vision 与 Strategy。换句话说，股价的分析可以告诉团队，应该做到多好。股价看似和 Vision 与 Strategy 无关，却是极好的切入点。

### 股价由什么构成

理解股价的关键是 __市盈率（P/E，Price-earning ratio）__。英文原文更容易理解：股价 vs 收益的比率。

  * 把股票想象成一张存折，市盈率的倒数就是它的 __利率__。其中，股价是 Share price。

![P/E formula](/images/vision-stock-ep.png "P/E formula")

其中，收益对应 __每股盈余__（EPS，Earning per share）。英文原文直白为，每股的收益。由公司的 __净利润__（Net income）除以股票总数（Average common shares）得到。

  * 公式中，优先股息（Preferred dividends）是优先股（Preferred stock）的股息。可以 __忽略__，通常总量较小，甚至很少使用 [[48]](.)。

![EPS formula](/images/vision-stock-eps.png "EPS formula")

将每股盈余，代入到市盈率的公式，可以发现：

  * 市盈率的倒数，是公司盈利除以公司市值（所有股票之和）。把公司想象成一张巨大的存折，市盈率的倒数就是“公司存折”的 __利率__。

  * 换一种理解，市盈率计算，“公司存折”需要多少年，其“利息”才能付清市值。即市盈率指多少年公司 __“回本”__。

![P/E interest formula](/images/vision-stock-pe-interest.png "P/E interest formula")

上文中的“公司存折”的利率，实际有多高？以 MSFT [[49]](.) 为例：

  * 利率 = 1 / P/E = 1 / 37.32 = __2.68%__。

  * 对比，三十年美国国债利率是 __4.6%__ [[50]](.)。（同期三月美债利率更高，约 5.3%。）

美债利率甚至高出上述“公司存折”的利率许多。相对股价，公司的盈利能力不如购买无风险的国债。为什么？

  * 交易者认为尽管公司目前盈利能力不足，但未来 __股价可能升值__，因此持续买入，造成股价上涨，市盈率上升。

  * 换句话说，股价升值的期望被市盈率反映。或者说，__市盈率反映公司未来的预期__，即对股价上涨的预期 [[52]](.)。

  * 如果公司预期变好，股票被更多买入，市盈率上升。反之， 公司经营不善，市盈率下降。如果希望公司维持当前业绩，__市盈率应该保持平稳__。

另一面，净利润可以继续分解，映射到市场规模：

  * 净利润等于公司的 __营收__（Revenue）乘以 __净利润率__（Net profit margin）。

  * 营收可继续分解为 __市场规模__（Market size）和 __市场占有率__（Market share）。

![Net income decomposition formula](/images/vision-stock-net-income-decomp.png "Net income decomposition formula")

由此，可以总结股价的构成：

  * 首先是公司的 __盈利能力__，取决于市场规模、市场占有率、净利润率。盈利与公司市值对比，反映为利率形式，对应市盈率的倒数。

  * 然后是交易者对 __公司未来的期望__，也由市盈率反映。其与无风险国债利率对比，可反映信念的强烈程度。

![Stock price decomposition formula](/images/vision-stock-price-decomp.png "Stock price decomposition formula")

### 股价应该涨多快

股价应该上涨得多快？其应该能覆盖机会成本和风险溢价（Risk premium），否则交易者会选择卖出股票，购买无风险的国债。除股价上涨外，股票给持有者的另一收益是股息（Dividends）。

  * __机会成本__ 对应无风险利率（Risk-free rate），通常由短期国债利率衡量。

  * __股息收益率（Dividend yield）__，每股按股价比例给持有者的分红收益。

  * __风险溢价__，股票风险高于国债，交易者要求额外的回报。

![Stock price growth formula](/images/vision-stock-stock-growth.png "Stock price growth formula")

首先来看股息收益率如何计算。股息来自于公司净利润，按比例取出后，发配到每股。

  * 如果只求简单，股息收益率一般可以从股票交易网站上直接 __查询__ [[51]](.)。

  * __股息收益率__ 可以分解为股票配息率（EPS payout ratio）除以市盈率。市盈率越高，股票收益率越低。

  * __股票配息率__ 指公司净利润中，有多少比例分配为股息；又等于每股盈余中，有多少比例分配为股息。股票配息率一般不受股价波动影响。它也可以在股票交易网站上查询。

![Dividend yield formula](/images/vision-stock-eps-payout-ratio.png "Dividend yield formula")

接下来看风险溢价的计算，这里使用常见的 CAPM [[55]](.) 资产定价模型。

  * __风险溢价__ 可由 Beta 系数乘以股权风险溢价（ERP，Equity risk premium）得到。

  * __Beta 系数__ 反映某只股票的股价，相对市场均价的波动幅度 [[53]](.)，通常可在股票交易网站上直接查询 [[49]](.) 。

  * __股权风险溢价__ 由预期市场回报（Expected market return）减去无风险利率得到。预期市场回可以股指基金得到，常用选 S&P 500 [[56]](.)。无风险利率前文已经讲到。

  * CAPM 中的 __股本成本（Cost of equity）__ 正是前文提到的无风险利率，与这里的风险溢价之和。股本成本不取决于股价，而是由市场背景决定。

![Risk premium formula](/images/vision-stock-risk-premium.png "Risk premium formula")

套用之前的公式，现在可以计算股价应该上涨多快。以 MSFT 股票为例：

  * 无风险利率取值自三十年美债，4.6% 。股息收益率直接查询，取 0.72% 。Beta 系数直接查询，取 0.89 。预期市场回报取 US S&P 500 过去五年的平均增长率，12.5%（惊人）。

  * __股价上涨（年）__ Share price growth = 0.046 - 0.0072 + 0.89 * (0.125 - 0.046) = 10.9% 。可见，该股价 __一年需上涨 10.9%__，以满足交易者成本收益平衡。

  * 相对高的股价上涨要求，一方面来自于当年较高的美债利息，另一方面来自于美股大盘高启的走势。

可以看到，在高利率牛市下，交易者对公司盈利要求苛刻。如果股价达不到预期，交易者将因机会成本或风险溢价导致亏损，从而卖出股票，降低市盈率和股价。最终的 __股价平衡点__ 在哪里？假设股价不再变化：

  * 继续上文的取值，股价取 \$420。其它同上。假定股票配息率不变（26.9%），每股盈余不变（\$11.25）。股价降低、市盈率降低，会提高股息收益率，从而平衡机会成本和风险溢价。

  * __稳定点的股价__ Share price = (0.0072 * 420) / (0.046 + 0.89 * (0.125 - 0.046)) = 26.0 。此时，市盈率为 2.31，股息收益率为 11.6%。此时，股息收益率正好等于股票的 __股本成本__，11.6%。

  * 除了股价低，这看上去是一支不错的股票。确实，有许多类似的真实股票 [[57]](.) ，低股价、高股息收益率、低市盈率。注意本文只作理论分析，不构成任何股价涨跌预测，不构成任何投资建议。

![Stable stock price](/images/vision-stock-stable-price.png "Stable stock price")

还有一些额外推论：

  * __股票上涨预期与公司市值无关__，假设忽略股息收益率，科技公司的通常很低。从上文公式可以看到，交易者要求的股票上涨幅度取决于市场背景利率和风险。公司股价、市值甚至不在公式中（忽略股息收益率）。

  * __高股价是负面作用__，现在考虑股息收益率。它取决于公司因素，由每股盈余、股票配息率决定。股价出现在分母，会拉低股息收益率，从而更难满足股票上涨预期。

  * __高市盈率是负面作用__。同理，因为它出现在股息收益率的公式的分母。高市盈率意味着，公司盈利能力不足，但股价较高。

本节已经展示，从交易者的角度，预期股价应以多快速度上涨，以保持市盈率和股价的稳定。那么，从公司角度，应该如何促使股价上涨以符合预期？

### 什么推动股价增长

前文提到市盈率反映交易者对公司未来的预期。为保持公司市盈率和股价的稳定，如何促使股价按预期上涨？从股票构成的公式中可见：

  * 首先，股价需要足额上涨，以跑赢无风险利率和风险溢价，即 __股本成本__。科技公司通常股息收益率都很低。

  * 股价上涨的动力来自于公司净利润，__净利润需要和股价等比例上涨__，以支撑股价。

![P/E interest formula](/images/vision-stock-pe-interest.png "P/E interest formula")

  * 净利润展开为 __市场规模、市场占有率、净利润率__，它们是寻求增长的方向。

![Stock price decomposition formula](/images/vision-stock-price-decomp.png "Stock price decomposition formula")

  * __造梦__。即使公司盈利能力不变，通过编织交易者对未来的乐观预期，也可推高市盈率，从而抬升股价。

从公司角度，上策是寻找高增长的新兴市场：

  * 例如，全球 __云存储市场__ 以每年 20% 以上的速率增长 [[46]](.)。单单进入这一市场，即有望满足前文中 11.6% 的股本成本。甚至不需要比同行更加优秀，类似搭便车。

  * 相比成熟大型企业，__小型新兴公司__（SMB）没有存量市场负担。它们反而拥有更加良好的股价上涨动力。

  * 科技、创新、新市场对于维系股价是必要的。

其次，公司可以寻求增加市场占有率：

  * 增加市场占有率意味着 __和竞争对手争夺__，公司业绩必须比同行更加优秀。这是艰难的方向。

  * 另一方面，这意味着在低增长的存量市场中，公司更难完成股价增长预期。大型成熟并不一定是优势。

下一个方向是提高净利润率：

  * 良好的路线是出售 __高附加值产品__，发挥比较优势，提升科技水准，提高市场认可等。

  * 另一条路线是，寻找 __规模效应__。随着规模扩大，固定成本降低，净利润率提高。

  * 常见的路线是 __降本增效__。当净利润率偏低时，降本增效更加有效。见下图。

![Net income growth by decrease cost](/images/vision-stock-net-income-growth-by-cost-decr.png "Net income growth by decrease cost")

此外，公司可以通过造梦来提高市盈率：

  * 市盈率反应交易者对股市预期，__造梦__ 提高预期、卖概念，而不要求公司盈利能力提升。

  * 此方法适合前期投入大，有 __规模效应__ 或 __科技积累__ 的业务。而一旦造梦破裂，股价可迅速下跌。

最后，真实公司的股价上涨是什么样呢？还是以 MSFT [[58]](.) 为例：

  * 公司整体营收以 17% 同比增长，而 __净利润__ 甚至增长更快，达 20%。表现出色。

  * XBox 营收增长达 62%，Azure 云服务增长达 31%，Dynamics 365 增长达 23%，智能云增长达 21%。它们 __远超股本成本__ 11.6%。

  * 此外，Office、Windows、搜索、LinkedIn 都有不错的增长，在 10% ~ 15% 间。

![MSFT cloud revenue growth](/images/vision-stock-ms-cloud-growth.png "MSFT cloud revenue growth")

### 团队的目标

股价分析帮助搭建一个从上到下、从公司顶层到具体团队的框架，明晰该以什么目标工作:

  * __公司__ 需要股价涨幅达到交易者预期，覆盖股本成本（股价应该涨多快）。

  * 增长目标 __分解__ 到市场规模、市场占有率、净利润率、造梦（什么推动股价增长）。

  * 对于具体 __团队__，则需要制定计划以完成上述增长。

  * 对应到团队管理的某个 __产品__，需其市场规模、市场占有率、净利润率等达到增长目标。

具体的增长目标是多少呢？

  * 从前文分析，以 MSFT 为例，增长目标是年度 __10.9%__ 。

  * 对于其它公司，按照前文公式 `4.6% - 股息收益率 + Beta 系数 * (12.5% - 4.6%)` 计算。股息收益率和 Beta 系数与股票相关，可直接查询 [[49]](.) 。计算结果通常在 __11%__ 左右（互联网科技公司）。

  * 对于占有新兴市场的产品，甚至要求其增长 __超过__ 上述增长目标，以弥补公司处在市场衰退期的产品。

  * 普通产品应达到上述目标，作为公司的 __平均值__。它们是公司的大多数。然而，11% 的平均要求并不低。

  * 而 __低于__ 平均值的产品是可能的。这意味着它们处于市场衰退期，员工面临裁员风险，职业发展空间受限。

  * 本质上，增长目标是要求跑赢股市大盘以及国债利率。

最后的问题：

  * 对于 __个体员工__，如何完成至少 11% 的年平均增长要求？注意是每年如此。（__今天，你拖公司的后腿了吗？__）

  * 对于 __团队__，如何制定 3~5 年的计划，确保每年 11% 或以上的增长？这就是需要 __Vision 与 Strategy__ 的地方了。

### 注意

本文是个人非专业的分析，所有文章仅表达作者个人观点，不构成对所述资产的任何投资建议。

## 存储系统的市场

商业策略分析通常可以分解为客户、产品、公司、竞争对手层面，进一步深入（下图）。客户、产品、竞争对手可归结为“市场”格局（Landscape）。本章将纵览存储系统的市场，列举市场的主要分区、产品功能、参与者。之后章节将进一步深入。

在不断变化的市场格局中，我们处于什么位置？3~5 年、或 10 年之后，市场版图又会如何变化，我们应在何处？理解市场是 Vision 与 Strategy 的基础。围绕市场，可以逐步揭示其结构和发展空间，什么是价值，需求，演化周期，以及背后的驱动因素。

![Business Situation](/images/vision-market-business-situation.png "Business Situation")

（详见下文）

![Storage market size compare](/images/vision-market-compare-storage-market-size.png "Storage market size compare")

### 分类

第一个问题是如何将存储市场分类？本章使用如下分类来组织内容。后面各小节标题前的字母对应分类组。

  * A. 经典的分类是 __云存储__ 和 __主存储__。云存储来自公有云。主存储（Primary Storage）[[49]](.) 一词多由 Gartner 使用，指部署在客户本地，服务关键数据的存储系统，通常为传统存储厂商。主存储也被称作“企业存储”（Enterprise Storage）。另外，企业本地使用的另一大类存储是 __备份和归档__ 系统。

  * B. 按使用接口，存储可分类为 __对象、块、文件__ 系统。对象存储服务由 Key 查询的不可变 BLOB，通常为图片、视频、虚拟机镜像、备份镜像等。块存储通常由虚拟机使用，作为其磁盘挂载。文件存储由来已久，存储目录和文件，可由用户直接使用，常见的是 HDFS、NFS、SMB 等。此外 __数据库__ 也可看作存储。

  * C. 按存储介质分类，存储可分类为 __SSD、HDD、磁带__ 系统。SSD 存储昂贵、高性能，常用于文件系统和块存储。HDD 存储廉价、通用，常用于对象存储，或存储冷数据。磁带存储一般用于归档存储。此外，还有全 __内存__ 的存储，一般用作缓存或分析型数据库。

上述对存储市场的分类是经典且常用的，也为本章讲解方便。但事实上，存储市场中的产品更为有机，为渗透对方市场、获得竞争优势，它们 __互相交缠__。例如：

  * A. __云存储__ 也售卖客户近端部署的 Edge 存储，如 AWS S3 Express。__主存储__ 也提供云端部署和云端卸载（Offloading）的版本，如 NetApp ONTAP。__备份和归档__ 在云存储中尤其具有性价比，如 AWS Glacier。

  * B. __对象存储__ 正变得越来越像文件系统，如模拟文件系统的 AWS S3 Mountpoint，如支持对象上的元数据和搜索，支持层级的对象路径。__数据库__ 有 Key-Value 接口的产品如 RocksDB，而 SQL 数据库也往往支持非结构化数据，类似对象存储。__块存储__ 不单用于虚拟机磁盘，也可为数据库提供 Page 存储。另外，各种存储系统的底层也可统一到 __共享日志存储__，如 Azure Storage，Apple FoundationDB、Log is Database 设计。

  * C. __SSD 存储__ 常常将冷数据卸载到 HDD 存储，以节省 SSD 的昂贵成本。__HDD 存储__ 常常将 SSD 作为缓存，或 Write Staging。__内存__ 被用作各种存储介质的缓存和索引，而内存存储系统也往往支持将冷数据或日志写到 SSD。

此外，为了简洁，本章省略了一些次要的分类。例如，

  * 按用户企业规模，可将市场分类为 SMB、大型企业、特殊领域。这个分类基于客户侧。

  * 企业存储也常按 DAS、SAN、NAS 分类。这个分类与对象、块、文件存储部分重合。

  * 除磁带外，归档存储还可使用 DNA 技术，如今正在快速发展。

  * Cyberstorage 是在 Ransomware 背景下的新兴存储分类，不过更多地是作为安全功能集成在已有产品中。

  * 向量数据库是在 AI 背景下的新兴数据库类型，而传统数据库也往往集成向量支持。

![Storage Market Categorization](/images/vision-market-storage-categorization.png "Storage Market Categorization")

### A. 云存储

关于预测市场未来的方向，咨询公司的分析报告是良好的信息来源（Gartner、IDC 等）。尽管报告付费，但通常有 __额外来源__：

  * 头部公司通常愿意提供免费的公开版本，作为公司的自我宣传。

  * 博客、报道尽管不是第一手资料，但也能反映主要内容。一些博主有专门渠道。

  * 在 Google 搜索前加入 `filetype:pdf`，可有效找到资料。

  * 在 Google 搜索后加入 `"Licensed for Distribution"`，可找到 Gartner 公开的文档。

  * 切换英文、中文搜索引擎、Scribd，可以找到不同内容。中文社区可能保存一些文档。

  * 此外，阅读主导产品的用户手册也可了解领域的主要功能和评估指标。

Fortune 预测全球云存储市场规模在 \$161B 左右，约 21.7% 年增长率 [[46]](.)。相比之下，全球数据存储市场规模在 \$218 左右，约 17.1% 年增长率 [[60]](.)。可以看到：

  * 云存储市场有 __极好的增长率__。结合 _[理解股价](.)_ 章节可以看到，该增长率十分有利于支撑股价，而不太需要从挤压竞争对手或削减成本方面下手。

  * 长期看，数据存储有趋势大部分 __被云存储取代__。这是由于云存储规模占比已经较高，且增长率快于数据存储整体。至少从预测来说如此。

![Fortune storage market size forecast](/images/vision-market-fortune-storage-market-size.png "Fortune storage market size forecast")

从 Gartner 的云基础设施的魔力象限中 [[61]](.)（2024），可以找到市场的头部参与者：

  * __Amazon AWS__：持久的领导者。AWS 在全球拥有大规模的基础设施、良好的可靠性和生态系统。AWS 是寻求可扩展性和安全性的企业的首选。然而，其复杂的服务对于新用户来说可能有挑战。

  * __Microsoft Azure__：领导者。Azure 得力于混合云能力、与微软产品的深度集成，以及与 AI 领导者 OpenAI 的合作。Azure 的行业特定解决方案，以及协同战略，对企业有引力。然而，Azure 面临扩容挑战，也受到安全方面的批评。

  * __Google GCP__：领导者。在 AI/ML 创新领域领先，Vertex AI 平台备受好评，云原生技术独树一帜。在环境可持续、AI 服务方面，GCP 对数据为核心的组织很有吸引力。然而，GCP 不足于企业支持和传统工作负载迁移。

  * __Oracle OCI__：领导者。OCI 强于提供灵活的多云和主权云方案，吸引需要强大集成功能的企业。其在 AI 基础设施的投资、与 NVIDIA 的合作，巩固了市场地位。然而，OCI 的生成式 AI 服务和弹性架构仍不足。

  * __Alibaba Cloud__：挑战者。作为亚太区的主力，阿里云在国内市场的电子商务、AI 服务方面领先。尽管拥有出色的合作伙伴生态，阿里云在全球拓展方面受限于地缘政治和基础设施。

  * __IBM Cloud__：特定领域。IBM 借助混合云和面向企业解决方案的优势，与 Red Hat OpenShift 无缝集成。其解决方案对受监管行业有吸引力。但不足于产品组合分散，以及 Edge 战略不完善。

  * __Huawei Cloud__：特定领域参与者。华为是新兴市场的关键参与者，优势于电信领域的集成云解决方案。在 AI/ML 研究方面出色，并在高需求的企业环境中取得成功。然而，地缘政治紧张局势和制裁限制了其全球扩张。

  * __Tencent Cloud__：特定领域参与者。对可扩展和分布式应用优化，在社交网络集成方面独具优势。然而，其全球合作伙伴生态为有限，并且在成熟度上与全球同行存在差距。

![Gartner Magic Quadrant for Cloud Platforms 2024](/images/vision-market-gartner-mq-cloud-platform-2024.png "Gartner Magic Quadrant for Cloud Platforms 2024")

云存储应该提供哪些 __主要功能__？Gartner 的云基础设施计分卡 [[62]](.)（2021）比较了各大公有云厂商，从中可以看到栏目列表，见下图。可以看到 AWS 的强劲实力。

![Gartner Cloud Platforms Storage Scorecard 2021](/images/vision-market-gartner-cloud-storage-scorecard.png "Gartner Cloud Platforms Storage Scorecard 2021")

另一方面，可将云存储看作逐步将传统存储的功能搬到云上，__用主存储对标云存储__。从这个角度来看，云存储应该具备哪些功能？哪些是主存储已有，而云存储未来可能发展的方向？有哪些衡量存储的关键指标？见下一节主存储。

### A. 主存储

本文将主存储对应于云下本地部署的企业存储，服务关键数据，这是存储由来已久的传统领域。其增长率大致对应存储市场的大盘，由 [[60]](.) 及其配图可见（上一节），年增长率在 17.1% 左右，正逐步被云存储侵蚀。当然，实际上主存储已经与云深度结合。

从 Gartner 的主存储魔力象限中 [[59]](.)（2024），可以找到该市场的头部参与者：

  * __Pure Storage__：持久的领导者。通过 Pure1，向用户提供主动 SLA，有利 IT 运维。融合的控制面无需外部云通信和 AIOps 的以来。DirectFlash Module 直接操作裸闪存，推动硬件、SLA、数据管理的创新。但是，Pure Storage 在美国外的用户多元化方面落后，生命周期管理计划增加了阵列的资产和支持成本，不支持计算、存储分离。

  * __NetApp__：领导者。NetApp 提供 Ransomware 恢复保证，不可变快照。通过 Keystone 策略和 Equinix Metal 服务简化 IT 运维。BlueXP 控制面提供 Sustainability 监控管理能耗和碳排放。但是，NetApp 不为块存储提供有竞争力的 Ransomware 检测保证，系列产品不支持更大的 60TB/75TB SSD 盘，不支持计算、存储分离。

  * __IBM__：领导者。IBM 消费计划提供产品生命周期、升级的统一定价，提供能耗效率的保证。Flash Grid 分区、迁移，持续优化负载，跨平台。但是，IBM 不提供容量优化型 QLC 阵列，不在块存储上提供文件服务，本地闪存部署不支持性能、容量分离。

  * __HPE__：领导者。HPE 的 Alletra 服务器允许用户独立扩展容量和性能，以节省成本。GreenLake 可以在本地和 AWS 相同地部署，混合管理。负载模拟可为用户提供整全局的关于性能和容量的负载放置建议。但是，HPE 供应商在 Sustainability 和 Ransomware 方面落后，不支持更大的 60TB/75TB SSD 盘，产品-负载组合存在混淆。

  * __Dell Technologies__：领导者。收购 EMC 后，Dell 拥有灵活的全线存储产品，APEX 提供跨本地和云的多云管理和编排。PowerMax 和 PowerStore 提供行业领先的 5:1 数据缩减和 SLA，与 Data Domain 数据备份整合。但是，Dell 不提供适用中端、高端的统一存储操作系统，这带来管理复杂度。

  * __华为__：挑战者。华为的多层 Ransomware 防护优秀，采用网络协作。闪存阵列提供三年的 100% 可靠性和 5:1 容量缩减保证。NVMe SSD FlashLink 支持高磁盘容量，由 ASIC 引擎加速。但是，华为在北美地区受限，不提供对 AWS、Azure、GCP 的多云扩展方案，客户集中于少数垂直领域而增加风险，多款存储产品许可过于复杂。

  * __Infinidat__：挑战者。Infinidat 在高端全球企业市场享有口碑，提供高质量的服务。SSA Express 能够将多个较小的闪存阵列整合成更经济的单台 InfiniBox 混合阵列。在遭受网络攻击后，可从不可变快照中恢复数据。但是，Infinidat 缺乏中端产品，InfuzeOS 云版本限制为单节点架构，SSD 仅支持 15TB 硬盘。

  * __Hitachi Vantara__：挑战者。Hitachi 允许用户在安装后五年内升级到下一代解决方案，以减少碳排放。EverFlex 简化用户订阅的流程，基于实际使用付费。EverFlex Control 将功能模块化，允许用户根据平台定制需求。但是，Hitachi 在 Ransomware 检测上落后，不提供计算存储的分离扩展，用于备份的 QLC SSD 方面落后。

  * __IEIT SYSTEMS__：特定领域参与者。IEIT 拥有独特背板和四控制器设计，自主负载均衡，可扩展至 48 控制器。提供在线反 Ransomware 功能，通过快照回滚。Infinistor AIOps 工具提供性能工作负载规划和模拟。但是，IEIT 在中国市场之外不为人知，在全球多云扩展方面落后，独立软件供应商（ISV）生态方面落后。

  * __Zadara__：特定领域参与者。Zadara 提供全球化的高技能的托管服务，基于低成本的对象存储和 Disaggregated 的 Key-Value 架构，利用灵活的生命周期管理来减少硬件浪费，多租户环境中的硬件可被动态重组。但是，Zadara 提供的 SLA 有限如 Ransomware 保护，商业规模和覆盖范围较小，第三方集成和 ISV 依赖于托管服务商。

![Gartner Magic Quadrant for Primary Storage 2024](/images/vision-market-gartner-mq-primary-storage-2024.png "Gartner Magic Quadrant for Primary Storage 2024")

主存储应该具备哪些功能？结合上文的魔力象限报告 [[59]](.)，Gartner 主存储关键能力报告 [[64]](.)（2023），企业存储主流趋势报告 [[66]](.)（2023），可以看到：

  * __Consumption-based 售卖模式__：与传统购买整套存储软硬件不同，而是类似云服务，按实际消耗量付费。相应地，SLA 按照用户端的指标重新定义，如 99.99% 可用性。Gartner 预测 2028 年将有 33% 企业投资采用 Consumption-based 模式，从 2024 年的 15% 迅速增长。关联概念：Storage as a Service（STaaS）。

  * __Cyberstorage__：针对 Ransomware 的检测和保护正成为企业标配，例如文件锁、不可变存储、网络监测、主动行为分析、Zero Trust 等功能 [[65]](.)。Gartner 预测 2028 年将有 2/3 企业采用 Cyber liability，从 2024 年的 5% 迅速增长。

  * __软件定义存储（Software-defined Storage，SDS）__：SDS 将用户从厂商专有硬件中解放，提供跨平台的、更灵活的管理方案，利用第三方基础设施，降低运维成本。另一方面，SDS 允许分离部署计算和存储资源、独立弹性地扩展，改善经济效益。__AIOps__ 功能变得重要，常与 SDS 结合。利用公有云的 __混合云__ 功能变得常见，该功能也常归于 SDS 名下。

  * __高级 AIOps__：例如实时事件流，主动的容量管理和负载均衡，持续优化成本和生产力，响应关键运维情形如 Cyber Resiliency 配合全局监控、报警、报告、支持。

  * __SSD / 闪存阵列__ 增长迅速。Gartner 预测 2028 年有 85% 的主存储是闪存阵列，从 2023 年的 63% 逐步增长，而闪存价格可能下降 40%。__QLC Flash__ 正普及，带来 60TB/75TB 的超大 SSD 盘，具有更好的能耗、空间、制冷效率。

  * __单平台支持文件和对象__（Single Platform for File and Object）。针对非结构化数据，__统一存储__（Unified Storage）平台同时支持文件和对象。融合的系统节约成本，Multiprotocol 使管理简化。文件和对象本身有相似性，图片、视频、AI 语料文件的使用方式近似对象，而对象加上元数据和层级路径后类似文件。

  * __混合云文件数据服务__（Hybrid Cloud File Data Services）。混合云为企业提供跨越 Edge、云、数据中心的统一访问和管理，命名空间一致，无需拷贝。企业能够在 Edge 对数据作低延迟访问、大批量的 Ingestion，在数据中心作复杂处理，在公有云存放冷数据和备份。可以看到传统存储产品纷纷上云，公有云纷纷开发 Edge 部署。

  * __数据管理服务__（Data Storage Management Services）。类似数据湖，数据管理服务读取元数据或文件内容，对数据进行分类（Classification）、洞察、优化。它跨越多协议，包括文件、对象，NFS、SMB、S3，跨越不同数据服务如 Box、Dropbox、Google、Microsoft 365。安全、权限、Data Governance、数据保护、Retention 也在议题中。在非结构数据快速增长的背景下，企业需要从数据中提取价值，并按重要性管理。

  * 其它常见特性，例如：__Multiprotocol__ 支持多种访问协议。__碳排放__ 的持续测量、报告、能耗控制。__无干扰的迁移服务__，从当前阵列到下一阵列，其间保证 100% 的数据可用性。__NVMoF__（NVMe over Fabric）是 NVMe 原生的 SAN 网络。__Container Native Storage__ 为容器和 Kubernetes 提供原生存储挂载。__Captive NVMe SSD__，类似 Direct Attached 盘，为专用场景定制，强化性能、耐用（Endurance）。

![Gartner Top Enterprise Storage Trends for 2023](/images/vision-market-primary-storage-top-trends-2023.png "Top Enterprise Storage Trends for 2023")

另外，

  * 主存储需要支持的 __关键用户场景__：OLTP 在线事务处理，虚拟化，容器，应用整合（Application Consolidation），混合云，虚拟桌面基础设施（VDI）。

  * 主存储的 __关键能力指标__：性能，存储效率，RAS（Reliability, availability and serviceability），Scalability，Ecosystem，Multitenancy and Security，Operations Management。

![Gartner Critical Capabilities for Primary Storage 2023](/images/vision-market-primary-storage-core-capabilities-2023.png "Gartner Critical Capabilities for Primary Storage 2023")

了解主存储所需功能的另一渠道是用户的反馈。用户如何看待我们的产品？[[67]](.) 列出了用户访谈中关于某个存储产品喜欢或不喜欢的反馈。[[68]](.) 列出了一份常见的用户招标文件。从中可以看到一些容易忽视的方面：

  * __易用性__。例如配置简单、管理便利，在用户心中占有重要地位，不亚于性能、成本因素。对于企业用户，权限管理，与其它常用系统、协议的集成也很重要，例如文件共享、Active Directory。客户服务和支持能换来真金白银。

  * __资源效率__。用户本地数据中心部署的存储常常面临闲置资源，或者部分资源耗尽而另一部分资源闲置的问题。扩容是常见需求，而又需要与老系统集成兼容。类似云的负载迁移、平衡、持续优化很有用处。Disaggregated 分离扩展、购买资源，避免捆绑，可为用户带来经济效益。

  * 截图只包括部分用户反馈，全文见 [[67]](.) [[68]](.) 原文。

![Customer interview Like and Dislike FlashBlade](/images/vision-market-primary-storage-customer-interview-flashblade.png "Customer interview Like and Dislike FlashBlade")

![Customer bidding storage example](/images/vision-market-primary-storage-bidding.png "Customer bidding storage example")

主存储技术在未来的发展方向为何？可以从 Gartner 的 Hype Cycle 中获悉，下图来自 [[69]](.) [[70]](.) ，有不同的分类。可以看到：

  * __对象存储__、__分布式文件系统__、__超融合__ 已被验证。__DNA 存储__、__Edge 存储__、__Cyberstorage__、__Computational Storage__、__容器存储和备份__ 正在兴起。

  * __Distributed Hybrid Infrastructure (DHI)__ 和 __软件定义存储（SDS）__ 是即将带来变革的技术。DHI 为用户本地数据中心提供云级别的解决方案，如 Consumption-based 模式、弹性、资源效率，并与外部的公有云、Edge 云无缝连接。其关联 __混合云__（Hybrid Cloud）。

  * Hype Cycle of Storage and Data Protection 图类似。Hybrid Cloud Storage 类似 DHI。Immutable Data Value 归于 Cyberstorage。Enterprise Information Archiving 归于归档存储，后者也是被验证的技术，在下一节讲述。

![Gartner hype cycle storage technologies 2024](/images/vision-market-gartner-hype-cycle-storage-2024.png "Gartner hype cycle storage technologies 2024")

![Gartner hype cycle storage technologies priority matrix 2024](/images/vision-market-gartner-hype-cycle-storage-priority-matrix-2024.png "Gartner hype cycle storage technologies priority matrix 2024")

![Gartner hype cycle storage and data protection technologies 2022](/images/vision-market-gartner-hype-cycle-storage-and-data-protection-2022.png "Gartner hype cycle storage and data protection technologies 2022")

### A. 备份和归档存储

第一个问题是，备份和归档存储拥有多大的市场规模、多快的增长率？

  * Market Research Future 预测 [[72]](.) __企业备份存储__ 在 2024 年拥有约 \$27.6B 的市场规模，此后以约 11.2% 的年增长率增长。市场增长主要由数据量增长、数据保护、Ransomware 保护的需求驱动。

![MarketResearchFuture Data Backup And Recovery Market Size](/images/vision-market-mrf-backup-market-size.png "MarketResearchFuture Data Backup And Recovery Market Size")

  * 作为企业备份存储的一部分，__归档存储__ 所占份额较小，但增长更快。Grand View Research 预测 [[73]](.) 其在 2024 年拥有约 \$8.6B 的市场规模，此后以约 14.1% 的年增长率增长。市场增长主要由数据量增长、更严格的合规需求、数据管理和安全驱动。

![GrandViewResearch Enterprise Information Archiving Market Size](/images/vision-market-gvr-archival-storage-market-size.png "GrandViewResearch Enterprise Information Archiving Market Size")

下一个问题是，备份和归档存储的主要市场参与者是谁？从 Gartner 的企业备份和恢复软件方案魔力象限中 [[74]](.)（2023）[[75]](.)（2024），可以找到该市场的头部参与者：

  * __Commonvault__：领导者。BaaS 覆盖广泛，包括 SaaS 应用、多云、本地部署，支持 Oracle OCI。Backup & Recovery 互操作性良好。Commonvault 将企业级功能带入有竞争力的价格。但是，Commonvault 的本地部署方面的创新落后于云端，部分用户反映体验不佳，HTML5 用户界面相比本地应用缺失功能。

  * __Rubrik__：领导者。Rubrik 在产品定价组合方面创新，例如为 Microsoft 365 提供有基于容量的用户 tiers。Rubrik 在 Ransomware 保护方面出色，例如机器学习、在备份数据中检查异常。Rubrik 的扩展能力和出色客服持续吸引大型企业。但是，Rubrik 需平衡在安全和备份的投资，SaaS 应用覆盖有限，可选云存储有限，主要在 Azure Storage。

  * __Veeam__：领导者。Veeam 拥有忠实的用户和 Veeam Community。Veeam 支持混合云和所有主要公有云。Veeam 在全球拥有大量合作伙伴。但是，Veeam 对 BaaS、SaaS、Ransomware 的市场需求反应缓慢，软件过于复杂，实现安全的平台部署需要仔细设计和配置。

  * __Cohesity__：领导者。Helios 是基于 SaaS 的集中控制面，为所用备份产品提供统一、直观的管理体验。DataProtect 和 FortKnox 允许用户选择多个公有云存储位置。Cohesity 积极与不同领域的供应商组成数据安全联盟（Data Security Alliance）。但是，Cohesity 的新投资引入第三方技术依赖，Backup as a Service（BaaS）能力不足，地理覆盖有限。

  * __Veritas__：领导者。Veritas 提供全面的备份产品，例如云和 scale-out & scale-up。NetBackup 和 Alta 服务支持云原生，在公有云运行 Kubernetes。服务和合作伙伴覆盖全球。但是，Veritas 的部分云产品仍处于早期，专注大企业而对中小企业不够友好，缺少 SaaS 应用支持（Microsoft Azure AD, Azure DevOps, Microsoft Dynamics 365 and GitHub）。

  * __Dell Technologies__：领导者。PowerProtect 提供数据保护和 Ransomware 保护，支持本地和云端部署。其允许用户结合多个 Appliance 的平衡容量。它提供跨多个公有云的一致管理，可在 Marketplace 获取。但是，Dell 缺少 SaaS 控制面，不支持选择其它备份存储方案，高级 Ransomware 分析需要专用环境。

  * 其它：挑战者、远见者、特定领域参与者。略，详见 [[74]](.) 报告原文。

![Gartner Magic Quadrant for Enterprise Backup and Recovery 2024](/images/vision-market-gartner-mq-backup-2024.png "Gartner Magic Quadrant for Enterprise Backup and Recovery 2024")

接下来的问题是，备份和归档产品所需的主要功能是什么？从 [[74]](.) 可以看到一系列 Core Capabilities 和 Focus Areas：

  * __备份和恢复数据__：才此基础上，支持本地数据中心和公有云。支持 Point-in-time 备份、支持业务连续、容灾等场景。配置多种备份和 Retention 策略，并与公司政策对齐。Tier 冷热备份数据到不同地点，如公有云、第三方供应商、对象存储。全局去重、数据缩减。

  * __Cyberstorage__：备份数据到不可变存储中，Immutable Data Vault。检测和防御 Ransomware。支持灾难、攻击的恢复测试和演习。为容器、对象存储、Edge 等不同目标提供保护，保护应覆盖本地、云、混合云。快速可靠的恢复，恢复书库、虚拟机、文件系统、Bare-metal 机器，恢复不同的 Point-in-time。

  * __控制面__：集中的控制面，在不同产品见统一，在本地、混合云端统一。管理分布式的备份和恢复任务，管理测试和演习。管理公司合规，数据保护和 Retention 政策。与常见其它 SaaS 产品、BaaS 产品的整合。控制面应是基于 SaaS 的，类似云，而不是让用户自己管理安装升级。

  * __Cloud-native__：备份软件自身可以云原生部署，例如 Kunernetes。数据保护覆盖云原生负载，例如 DBaaS, IaaS and PaaS。与公有云服务结合，支持存放数据到云，支持在云端调度任务。备份产品以接近云的 BaaS 方式提供服务。按实际使用量付费（Consumption-based），而不是让强迫用户购买整台 Appliance。

  * __GenAI & ML__：支持生成式 AI，例如在任务管理、故障排查、客服支持中。支持机器学习，例如用于 Ransomware 检测，自动数据分类（Classification）。

最后的问题是，备份和归档技术未来的发展方向为何？可以从 Gartner 的 Hype Cycle 中获悉 [[69]](.)（2024），见下图。可以看到：

  * __数据归档__、__归档专用 Appliance__、__数据分类__ 已经被验证。__Cyberstorage__、__生成式 AI__、__云恢复（CIRAS）__ [[76]](.)、__备份数据重用分析__ 等正在兴起。

![Gartner hype cycle backup and data protection technologies 2024](/images/vision-market-gartner-hype-cycle-backup-and-data-protection-2024.png "Gartner hype cycle backup and data protection technologies 2024")

### B. 文件存储

文件存储在企业和云存储中占有重要地位。首先，文件存储拥有多大的市场规模、多快的增长率？VMR 的报告 [[78]](.) 指出，

  * 分布式文件系统 & 对象存储在 2023 年拥有约 \$26.6B 的市场规模，__年均增长率约 16%__。这个增长率大致和主存储相仿。略慢于云存储整体。

  * 许多报告中，__文件系统和对象存储被合并统计__。确实，这两种存储的用户场景相通，并且近年发展中也在吸收彼此特性。见本文 “[互相交缠](.)” 段落。

  * 另外，Market Research Future 报告 [[79]](.) 中给出了（云）对象存储单独的市场规模（对象存储主要是云）。对照可发现，对象存储 2024 年市场规模仅 \$7.6B ，__年增长率不及文件存储__，约 11.7% 。

  * VMR 的另一报告 [[81]](.) 中给出了 __块存储__ 的市场规模，可供对比。2023 年拥有约 \$12.8B，约 16.5% 年增长率。块存储市场规模的增长率快于对象存储，与文件存储相仿。

![VMR Global Distributed File Systems and Object Storage Solutions Market By Type](/images/vision-market-msf-file-object-market-size.png "VMR Global Distributed File Systems and Object Storage Solutions Market By Type")

Gartner 的文件和对象存储平台魔力象限中 [[77]](.)（2024），可以看到该市场的主要参与者。注意，文件系统和对象存储仍然被被合并统计。注意，这里主要针对存储厂商，类似主存储，而不是公有云（公有云见 “[云存储](.)” 一节）。

  * __Dell Technologies__：领导者。收购 EMC 后，Dell 拥有最广泛的软硬件产品组合，包括非结构化数据和特定用途产品。Dell 拥有全球供应链和供应商。Dell 与 Nvidia 紧密合作并投资 AI 项目。但是，PowerScale 缺乏全局命名空间和 Edge 缓存，与拥有不同架构的现代闪存存储竞争加剧，依赖 ISV 解决关键需求。

  * __Pure Storage__：领导者。FlashBlade 采用 NVMe QLC SSD，拥有行业最高密度、最低 TB 功耗，价格相比 HDD 混合阵列具有竞争力。Evergreen//One 和 Pure1 的 AIOps 功能和监控确保用户 SLA 。FlashBlade 与 Equinix Metal 合作，将本地基础设施扩展到全球。但是，Evergreen//Forever 方案显著增加了资本支出，Ransomware 检测能力有限，混合云支持有限，如 AWS、Azure、GCP 中以虚拟机、容器部署。

  * __VAST Data__：领导者。VAST 的战略合作、营销大量增加大客户。VAST 使用 QLC 闪存、先进的数据缩减算法、高密度机架。终端用户认可其出色的客户服务，如知识、售前、架构，订购、部署。但是，VAST 缺乏品牌集成的 Appliance 因而难以吸引保守型全球企业，高频软件更新带来不稳定，缺少企业及功能如同步复制、Stretched Cluster、Geodistributed Erasure Coding、Active Cyber Defense，混合云吸引力有限。

  * __IBM__：领导者。IBM 在 HPC 市场处于领导地位，与 AI 结合。文件和对象提供全局命名空间，跨越数据中心、云或 Edge、非 IBM 存储。IBM 持续增强 Ceph 存储，受开源用户青睐，统一文件、块、对象存储。但是，IBM 产品组合复杂，云支持不足，文件存储倾向 HPC 而通用场景不足。

  * __Qumulo__：领导者。Qumulo 在 Azure 上提供 SaaS 的简便和云弹性。其软件在本地和云端部署提供一致的功能和性能。Qumulo 的全局命名空间提供跨越本地和多个云的访问。但是，Qumulo 缺乏 Ransomware 检测能力，不提供自己的硬件设备而依赖第三方，全球覆盖有限。

  * __华为__：挑战者。OceanStor Pacific 提供统一平台文件、块、对象的统一存储。从 AI 性能到数据管理，华为拥有专有硬件技术，包括芯片和闪存。客户支持和服务收到高度评价。但是，美国制裁和地缘政治限制全球扩张，对其它公有云如 AWS、Azure、GCP 的支持有限，不提供灵活的 SDS 方案。

  * __Nutanix__：远见者，远见程度超越所有领导者。NUS 平台可 Consolidate 各类用户存储负载，在混合云下集中管理。NUS 简化实施、运维、监控、扩展的管理。客户支持服务在可靠和响应方面受到认可。但是，超融合（Hyperconverged）平台不受只想购买存储的用户认可，文件和对象在混合云部署中认可有限，不支持 RDMA 访问 NFS 因而不适合低延迟场景。

  * __WEKA__：远见者。并行文件系统适用最苛刻的大规模 HPC 和 AI 负载。Converged 模式允许文件系统和应用运行于同一服务器上，并提高 GPU 利用率。混合云在各公有云、Oracle OCI 中广泛可用，但是，备份和归档方案不具备成本效益，S3 和对象支持有限，缺少 Ransomware 保护、AIOps、同步复制、数据效率保证、地理分布对象存储。

  * __Scality__：远见者。Scality 的 RING 架构支持 EB 级部署，独立扩展性能和容量。Scality 追求纯软件方案，能够运行在广泛的标准硬件上，无论 Edge 还是数据中心。RING 数据保护支持地理分布，跨多个可用区，零 RPO/RTO，极高 Availability 和 Durability。但是，作为 SDS 方案，其依赖外部供应商，不具备交付 Turnkey Appliance 的能力；文件由对象存储集成 POSIX 实现，因而不适用 HPC。

  * 其它：特定领域参与者。略，详见 [[77]](.) 报告原文。

![Gartner Magic Quadrant for File and Object Storage Platforms 2024](/images/vision-market-gartner-mq-file-object-2024.png "Gartner Magic Quadrant for File and Object Storage Platforms 2024")

文件和对象存储系统应该具有哪些主要功能？从 Gartner 魔力象限报告中可以看到一系列 Core Capabilities 和 Top Priorities，如下列出。另一方面，可以发现它们与主存储、备份和归档存储的主要功能 __皆相通相似__。

  * __统一命名空间__（Global Namespace）：文件跨本地数据中心、Edge、多个公有云统一管理和访问。支持地理分布、复制保护。支持 __混合云__、S3，以及多种文件访问协议。__统一存储__（Unified Storage），文件、块、对象由统一平台服务。单一平台处理高性能和数据湖。

  * __AIOps__：支持 AIOps、简化、统一的管理配置，自动化。拥有出色的客户服务，在知识和架构方案等方面。__数据管理__，如元数据分类、成本优化、数据迁移、分析、安全。数据生命周期管理。元数据索引、文件和对象 Labeling/Tagging 。软件定义存储 SDS。

  * __Cyberstorage__：提供 Ransomware 的检测和保护，在攻击中保持业务连续性。响应和恢复数据。当然，传统的数据加密、认证等安全功能必不可少。

  * __成本和性能__：采用具有容量、能耗优势的 QLC 闪存。提高机架存储密度。去重、压缩、纠删码等数据缩减技术，以及数据效率保证。使用闪存或 SSD 加速文件访问，提供缓存，并对闪存作数据缩减。RDMA 访问降低延迟，Edge 存储降低延迟。支持线性扩展，支持分离扩展性能和容量，妥善处理性能和容量的 Burst。__STaaS__ 模式 Consumption-based 付费。管理能耗和碳排放。

  * __不同用户场景__：通用文件系统、数据库、对象（或按对象的方式使用文件）、HPC 及 AI，是不同的用户场景，在功能和性能上各有取舍。或者见下面来自 Nasuni 的“企业文件-数据量”图 [[80]](.) 。

![Nasuni Types & Volume of Files in the Enterprise](/images/vision-market-nasuni-file-types-enterprise.png "Nasuni Types & Volume of Files in the Enterprise")

文件也是主存储功能之一，关于未来发展趋势、Hype Cycle，不再重复。参见 “[主存储](.)” 一节。

### B. 对象存储

对象存储和文件存储经常被合并统计，其功能相通，例如 Gartner 的文件和对象存储平台魔力象限中 [[77]](.)。上一节 “[文件存储](.)” 已经包含对象存储，本节不再复述。

另一方面，对象存储的经典场景是云存储，见前文 “[云存储](.)” 一节，本节不再复述。云存储所需功能也可与存储厂商对标而得，见 “[文件存储](.)” 一节。

### B. 块存储

VMR 的报告 [[81]](.) 中给出了块存储的市场规模和增长率，在 “[文件存储](.)” 一节中已经包含在图中。

块存储是主存储的核心功能之一，通常合并到主存储中统计，“[主存储](.)” 一节已经包含，不再复述。现代平台常常是统一存储，同时提供文件、块、对象服务。

另一方面，块存储是云存储的经典场景之一，见前文 “[云存储](.)” 一节，不再复述。

### B. 数据库

数据库的市场规模和增长率如何？从 Grand View Research 的预测可以看到：

  * __数据库__ 在 2023 年拥有约 \$100.8B 的市场规模，年增长率 13.1% [[82]](.) 。其中，全球 __云数据库__ 在 2022 年拥有约 \$15.05B 的市场规模，年增长率 16.3% [[83]](.) 。

  * 与前文 "__[云存储](.)__” 一节对比，可以发现：1）数据库的主要市场在非云。2）云数据比非云增长更快，但远不及云存储（21.7%）。3）云存储市场比数据库大得多。

![GrandViewResearch Database Market Size](/images/vision-market-gvr-database-market-size.png "GrandViewResearch Database Market Size")

综合前文各节的市场规模和增长率，这里可以绘制 __各存储类型并比较__，可以看到：

  * __云存储__ 拥有最大的市场规模和最快的增长率（21.7%），拥有良好的投资价值。其次是 __非云的数据库__ 市场，规模较大，增长率较低（13.1%）。

  * __文件存储__、__块存储__、__云数据库__ 市场规模较小，但增长率不错（16%~17%）。而 __对象存储__ 较弱，市场规模小，增长率较低（11.7%）。

  * 备份和归档存储中，__归档存储__（14.1%）增长快于 __备份存储__（11.21%）。前者增长快，后者存量大。

![Storage market size compare](/images/vision-market-compare-storage-market-size.png "Storage market size compare")

放大图中较低市场规模的部分：

![Storage market size compare](/images/vision-market-compare-storage-market-size-zoomed.png "Storage market size compare")

虽然数据库存储数据，但在市场划分上， 数据库一般不被分作“存储”市场。存储通常指文件、块、对象，而数据库运行在文件、块存储上。数据库拥有庞大复杂的内容、持久活力的市场，值得另一篇文章，而数据湖跨越数据库和存储两者属性（结构和非结构化数据）。

本文围绕存储，因而不再深入数据库。下面仅列出：

  * Gartner 云数据库魔力象限（2024）[[84]](.) 。

![Gartner Magic Quadrant for Cloud Database Management Systems](/images/vision-market-gartner-mq-cloud-database-2024.png "Gartner Magic Quadrant for Cloud Database Management Systems")

  * Gartner 数据管理技术 Hype Cycle（2023）[[71]](.) 。

![Gartner hype cycle backup and data management 2023](/images/vision-market-gartner-hype-cycle-data-management-2023.png "Gartner hype cycle backup and data management 2023")

### C. SSD 存储

Market Research Future 预测 [[85]](.)，企业闪存存储在 2025 年拥有约 \$67.17B 的市场规模，年增长率约 9.89% 。

![MarketResearchFuture Enterprise Flash Storage Market Size](/images/vision-market-mrf-enterprise-flash-storage-market-size.png "MarketResearchFuture Enterprise Flash Storage Market Size")

闪存存储常用于主存储、文件存储、块存储，它们是分析报告中更常见的分类方式，在前文章节中已经讲述，本节不再复述。相比 SSD，闪存是存储介质，SSD 通常指加上控制器、封装好的存储盘。

### C. HDD 存储

Market Research Future 预测 [[87]](.)，HDD 市场规模在 2024 年有约 \$62.43B，年增长率约 6.1% 。注意，这是磁盘而不是存储的市场。HDD 市场面临衰退，主因是被 SSD 取代。

![MarketResearchFuture Global Hard Disk Market Size](/images/vision-market-mrf-hdd-market-size.png "MarketResearchFuture Global Hard Disk Market Size")

HDD 存储常用于主存储、混合（闪存）阵列，对象存储，备份系统。后者是分析报告中更常见的分类方式，而不是以 SSD/HDD 归类，存储也常常不是使用单一介质。它们在前文章节中已经讲述，本节不再复述。

### C. 磁带存储

Market Research Future 预测 [[86]](.)，磁带存储在 2024 年拥有约 \$3.5B 的市场规模，年增长率约 5.82% 。相比 SSD 和 HDD，磁带的市场规模很小、增长率低。

![MarketResearchFuture Tape Storage Market Size](/images/vision-market-mrf-tape-storage-market-size.png "MarketResearchFuture Tape Storage Market Size")

磁带常用于归档存储。后者在前文章节中已经讲述，本节不再复述。

### C. 内存存储

内存存储一般用于数据库或缓存。存储通常不会是纯内存的，因为难以保证数据持久性，尤其在数据中心断电故障中。内存在存储系统中一般用于服务元数据或索引，并不独立于其它存储类别之外。因此，本节略过内存存储。

## 关于市场的分析

上一章遍历了存储市场的主要分区、其中的重要参与者、各自的产品、产品的核心需求、未来可能的方向。这一章将继续深入。围绕市场，可以揭示其结构和发展空间、驱动因素、核心价值。

在不断变化的市场格局中，我们处于什么位置？3~5 年、或 10 年之后，我们位于何处？通过对规律的把握，能够帮助 Vision 与 Strategy 分析，规划未来 3~5 年、甚至 10 年之后，我们应处的方位。

### 市场的结构

基本的市场分析包括市场分区、市场规模、用户场景、竞争格局（Competitive Landscape）、产品和功能等，在上一章已经讲述。对于存储市场，有更多维度需要考虑。例如，市场的“天然结构”是什么？其决定产品的上限和增长模式。

![Market overview structure](/images/vision-market-overview-struct.png "Market overview structure")

#### 客户组成

考虑开发新的产品、功能， 其对应的市场由哪些客户组成？

典型的划分是，__SMB、大型企业、专业领域__。作为客户类型，SMB（中小企业）、大型企业对产品的需求、营销策略显著不同。尽管大型企业能提供丰厚的销售利润，但 SMB __议价能力__（Buyer Power）的要求更低，避免带来大量定制需求，甚至把公司变成运维。

如今，__政府采购__ 应被添加作新的客户类型。此外，__个人消费者__ 也应被添加，其常购买网盘存储（见下文 Empower Everyone）。在此之上，购买方 __垄断程度__ 应作为市场的结构的关键考量之一。而销售方，__开源__ 应被添加为竞争者。

这个话题进一步引导向 __Porter 五力分析__ [[88]](.)：竞争者、供应商议价能力（Supplier Power）、购买者议价能力（Buyer Power），替代品威胁、新进入者威胁。

相似的分类是，__低端、中端、高端__，覆盖不同偏好、规模的客户。低端走量、标准化。高端服务大型企业、定制需求，或特殊专业领域。

另一个关于客户的维度是 __粘性__，例如社交网络。详细内容见下文 _“[什么是价值](.)”_ 小节。

#### 市场的天然结构

有些市场天然具有 __规模效应__，例如水电、云计算。竞争最终导向参与者兼并，留存少数企业，而存活者享受营收和利润率的双重上升。

而另一些市场具有 __反规模效应__，例如教培、咨询、猎聘、投资。市场允许新小参与者不断加入，大型参与者导致分裂，而成熟的个人、团队倾向单干。

与此相配的市场维度是 __增长模式__。规模效应下，互联网产品的用户数量可以 __指数__ 增长 。高 COGS 、人力成本占固定比例时，如制造、运维服务、外包定制，产品趋于 __线性__ 增长。反规模效应下，产品增长甚至会 __递减__，另一种递减是市场衰退。

#### 市场的天花板

在一轮市场生命周期（见下节）中，市场规模最终能增长到多高？这和市场的天然结构相关。一个参考是 O(P)：调查每一个人，有 P 概率使用该产品。

__O(1) 规模的行业少见且珍贵__，例如社交 App 和支付应用，每人都用。而好莱坞电影虽然知名，却未必每人都看过。O(1) 的行业上限极高，渗透力强。反之，则天花板有限，往往需走高端路线提高单价。

某种意义上，__Enable Everyone / Empower Everyone__ 的经济效益，是增加 O(1) 级行业的数量，扩大 O(P<1) 行业的覆盖。

#### 对相邻市场的渗透

新兴、高速发展的技术不仅能够革新自身行业，往往也对临近行业进行渗透，进一步扩大市场和销售范围。

例如，云计算发起自售卖计算、存储资源，但逐渐取代了企业的本地运维。对象存储原本用于存储图片、视频，但统一存储平台（Unified Storage）有能力兼管文件、块服务。互联网平台对各行业的渗透显而易见。

除增长模式外，__渗透能力__ 是衡量市场潜力的另一维度。另一种说法是，__1+1>2__，多种产品形成逐步加强的循环反馈（__闭环__）。

反过来，__易被渗透__ 的市场是不利的，往往需要配套投资相邻市场，利用产品组合构筑护城河。

#### “推论”

从个人 __职业发展__ 角度考虑，所加入的市场分区起到重要作用。当产品具有规模效应时，企业倾向保留少量、尖端的人力，不吝惜给予高薪酬，因为成本不在此处。__人力是成本还是 Multiplier__？

当产品具有线性增长模式时，薪酬往往不高，但好在工作数量较多。__市场天然利润率预期工资水平__。见 _[理解股价](.)_ 章节。

大规模 __裁员__ 往往意味着市场处于递减、衰退阶段，此市场对职业发展非常不利，“被赶走” 至少避免主动处于不利市场。

### 市场的生命周期

从市场结构继续，下一个关键的维度是市场的生命周期。未来数年后，我们的团队和产品将处于什么位置？市场结构解释增长和上限，而市场生命周期预测其阶段。基于此制定策略，并为下一周期铺路。

![Market growth stages](/images/vision-market-growth-stages.png "Market growth stages")

#### 市场的阶段

市场阶段可以 __划分__ 为导入期（Introduction Stage）、成长期（Growth Stage）、成熟期（Maturity Stage）、衰退期（Decline Stage）。

新技术在导入期潜伏于小众爱好者，先进但增长缓慢。在成长期快速爆发，指数增长。在成熟期激烈竞争和兼并，比拼质量和客户留存。在衰退期被逐渐取代，营收、利润率双降。

更重要的是，通过市场分析预测 __什么时候__ 该市场进入成长期、衰退期等阶段，以此计划策略转向。

#### 新市场的来源

新的市场往往来自 __规模增长__、__新技术__、__成熟度__、__商业模式变化__、__政策合规__。在下文 _“[驱动因素](.)”_ 一节详细讲解。颠覆式创新是市场更新的源动力。

### 颠覆式创新

本节仍属于 __市场的生命周期__ 一节，但因重要性独立。这可以说是最重要的概念。科技行业中，颠覆式创新（Disruptive Innovation）是市场更新的 __源动力__。颠覆式创新是市场周期的开始和终结。

（更多关于创新，见 [Methodologies for Skilled Innovation](https://accelazh.github.io/experience/Methodologies-For-Skilled-Innovation)）。

#### 渐进式创新

在未跳出单一市场生命周期前，企业增长一般依赖 __渐进式创新__。但随着复杂性积累，边际收益（Marginal Gain）降低，阻力增加。市场增长放缓，竞争加剧，陷入“__内卷__”或停滞。

另一方面可以看到，无论是渐进式创新还是颠覆式创新，__企业的日常工作离不开创新__。渐进式创新本身并不简单，其需要经验和洞察，以找到有效的“百尺竿头更进一步”，并带领团队成功实施。

#### 颠覆式创新

颠覆式创新带来新的技术和新的范式，__新一轮市场周期__ 由此开始，并替换、终结上一市场。

新技术在导入期潜伏于低端市场，往往不被原市场的成熟参与者发现。新技术进入成长期后，快速夺取大量用户，而原市场被迫进入衰退期。对于被替代的原市场参与者，此时 __规模大成为负面因素__（见 _[理解股价](.)_ 章节），往往难以自由应对。最终，新技术夺取高端市场的桂冠，完成市场替代。旧新交替，重复循环，行业在一轮轮叠浪式的周期中发展 [[90]](.) 。

![Disruptive Innovation Growth](/images/vision-market-disruptive-innovation-growth.png "Disruptive Innovation Growth")

颠覆式创新有很多例子。例如，云计算渗透企业存储、数据库、运维市场，NewSQL 将 Scale-out 分布式带入数据库，统一存储（Unified Storage）引入 SDS 并实现分布式文件系统，容器和 Kubernetes 革新集群管理。下图中有更多例子 [[90]](.) 。

![Disruptive Innovation Growth](/images/vision-market-disruptive-innovation-examples.png "Disruptive Innovation Growth")

#### 颠覆式创新的特性

颠覆式创新的 __“发展进步”__ 体现在多个方面。新技术比旧技术具有更高的生产力和效率，达到完全替换后，__市场天花板额外增高__。新技术更具活力，除替换原市场外，__对相邻市场进行渗透__，进一步拓宽市场规模。新技术需要翻新原有产品和上下游配套，导致 __重写代码__，带来新一轮劳动力需求，从“内卷”中解放。

“重写”意味着，颠覆式创新并不抛弃上一市场周期的产物。知识、经验、旧有路线被 __带入下一周期复用__，__螺旋上升__。例如，DPU 是存储领域的新近创新，但 ASIC 在交换机中使用已久 [[89]](.)，而 SDS 之前的存储本就是“专用硬件化”的。长期看，软硬互相 __交替摇摆__。上一周期、上上周期的经验有高重用价值。

近年来，__颠覆式创新在加速，市场周期在缩短__。曾经的传统行业，老技术可以干一辈子。存储、服务器等后端技术，大约可以续用十到二十年。而互联网的快速迭代、前端技术，也许五年就已经面目全非。生成式 AI 的快速发展更惊人，突破成果的发布以月记。加速趋势得益于生产效率的提高，全球协作便利，开源基础设施完善，金融投资的远见，以及对企业快速扩张的支持。

#### “推论”

颠覆式创新下的新市场周期，往往“重写”上个周期的产品，重复上上周期的路线，“螺旋上升”。这意味着 __老员工尤其重要__，因为他们经历了上一周期乃至上上周期，其经验和目睹的历史，可以在下一市场周期复刻。（这与如今职场的 35 岁淘汰风气相反。）

另一方面，__新手有特殊价值__。颠覆式创新要求跳出固有范式（Think out of box），新手是难得的屏蔽思维定势和切换视角的机会。向他们咨询，赶在其被团队“污染”之前。而成熟员工往往或多或少已被团队“污染”，沿袭 We always do this before，习惯“成熟”经验和视角，并将“污染”新人。

颠覆式创新意味着，__当前的工作一定会“完蛋”__。而现代的颠覆式创新在加速，市场周期在缩短。这意味着未来的个人 __职业生涯将更短__，可能在五到十年后面临技术换代，大规模裁员。而新一届毕业生更有竞争力，拥有针对新技术的系统完整的训练。

新技术换代的被驱逐者也是 __曾经的得利者__。快速换代的市场中，新人总有大量机会进入，超越老人，获取高薪。市场不易形成“辈分”和壁垒，更加吸引新人加入。

### 驱动因素

是什么驱动源源不断的新需求，供各个市场参与者存活与成长，并周期性地开启新的市场周期？对于存储市场，驱动因素来自多个方面：__规模增长__、__新技术__、__成熟度__、__商业模式变化__、__政策合规__。掌握驱动因素帮助确定未来的发展空间和方向。

![Market demand driving factors](/images/vision-market-growth-driving-factors.png "Market demand driving factors")

#### 规模增长

相比其它市场，存储市场的一大特点是  __天然的规模增长__，不间断且速度不低，支持约 10%~20% 的市场规模增长。

为应对规模增长，__催生各式创新__。例如，软件层面上，分布式文件系统支持线性扩大数据规模，以及整个大数据生态。硬件层面上，多数硬件能力逐年指数增长，见 _[存储系统中的硬件](.)_ 章节，并伴随逐代技术升级，例如 PCIe、QLC 闪存。运维管理上，SDS 允许更便利、弹性地管理大量、异构的存储设备，以及云计算。

数据增长同时伴随 __能力效率的提升__。一个人能管理多少数据？从旧时代的一个人管理一台机器，到运维中一个人管理 1PB 数据，再到云时代一个小团队管理全球数百数据中心。

#### 新技术

市场更新的源动力来自 __颠覆式创新__。技术换代、范式转移（Paradigm Shift），带来原产品的 __“重写”__、重建、上下游重配套
需求，诞生大量工作岗位。新市场在 __替代__ 原市场的过程中，重新产生大量购买需求。新技术往往诞生之前不存在的 __新场景__，
进一步催生需求。

新技术的另一增长来自 __硬件发展__，其能力指数提高。更强、更快、更大、更便宜，使不可能的场景变成可能，使昂贵的产品变得触手可及，奇迹被瓶装出售、打折甩卖。

随之而来的是 __软件层面__ 的需求。软件需要 __整合__ 异构硬件、__适配__ 下一代，__优化__ SKU 组合甚至 Co-design 。软件需要 __集成__ 不同企业系统，并统一 __管理__ 大量设备。软件需要提升 __资源效率__，并尽可能地保留硬件的原生 __性能__。而为了应对 __复杂性__ 和 __易变性__，也催生更多技术。见 _[存储系统中的硬件](.)_ 章节 - “软件的价值”。

#### 成熟度

随着市场走向成熟，客户期望产品提供更丰富细化的功能，这一过程伴随 __渐进式创新__。它们提供了参与者日复一日的工作。

对于存储系统，具体的期望是：更大规模的数据，更好的性能，更高的可靠性，更低的成本，更便利的管理，更安全，更丰富的功能，更强大的集成，客户服务和支持。

![Market driving factor of maturity](/images/vision-market-driving-factor-maturity.png "Market driving factor of maturity")

首先，__更大规模的数据__，催生一系列 Scale-out、Scale-up 相关的容量、性能技术。在容量的基础上，需要分布式一致性（如 Paxos）、分布式事务、数据组织（如列存）、索引技术（如 Mass-tree）。为管理大规模的数据，集群管理（如 K8S）、部署 Orchestration、运维自动化、监控和预警技术（如时间序列数据库），应运而生。

其次，__更好的性能__，催生多个维度的优化，简化调用路径（如 DPDK、SPDK），高速网络（如 RDMA），负载均衡（如 Hedged Request），动态迁移等。另一方面，与硬件发展整合（如 DPU、ZNS SSD）。

在 __更低的成本__ 需求驱动下，数据存储成本被持续降低，如冷热分层、纠删码、数据压缩、全局去重技术。另一方面，数据写入和读取的服务成本被降低，如 Foreground EC、芯片加速、分布式缓存技术。

接下来，__更便利的管理__ 包含多个方面。客户希望见到简单易用的图形化界面，并自动升级。管理需要统一，例如混合云，跨越本地、Edge、云的边界。命名空间需要统一，常用于跨多云的文件系统，并且全球部署和访问。资源响应弹性快捷，如容器。

一大范畴是 __更安全 Safety__。典型的需求是数据复制、校验、QoS、备份、快照、容灾。在全球化部署下，地理复制、可用区容灾日渐普及。保护级别逐渐提高，从 5min RPO 到 Zero RPO，从低频的手动快照到 Point-in-time 和 Time Travel。另一方面，形式化验证如 TLA+，也在存储中应用普及。

另一大范畴是 __更安全 Security__。一部分需求来自传统的存储加密、传输加密、认证、权限、防火墙、密钥管理，补丁升级等。另一部分需求来自时新场景，如 Zero Trust、Ransomware 保护、不可变存储、隐私保护。

接下来是 __更丰富的功能__，有多个方向。单一功能可以 __延伸至上下游__，例如。数据格式 -> 可视化表格 -> 自动 ETL -> BI 统计报表 -> 复杂数据查询 -> 大规模存储 -> 数据湖 -> 专用服务器，形成产品组合，构筑护城河。单一功能可以更 __完善、细化__，如文件系统支持更多格式、访问协议、提供各式工具。甚至支持 __定义外的功能__，如数据仓库支持修改数据和事务，“打开文件”窗口支持顺手编辑无关文件，数据库集成 BLOB、时间序列、向量。功能的丰富如同 __分形触手__，在需求矛盾下层层深入、细化。

最后，__更强大的集成__，是企业应用的常见需求。在上一章 _[存储系统的市场](.)_ 中，集成被反复提及，作为必要的竞争力。例如，办公软件集成数据库和 AI，存储平台集成第三方 ISV，数据管理集成通用的文件共享、Active Directory 等。集成也为产品跨界，__向相邻市场渗透__ 提供窗口。集成包括众多 __繁复__ 的工作，例如不兼容的 API、多样的数据格式、易变的业务流程、来自人的多样需求、报表和可视化、管理 Portal、持续花费的维护。

除此之外，__客户服务和支持__ 也是存储产品走向成熟的需求之一。客户服务不单指解决产品故障，还包括为客户场景架构解决方案、选择费用合理的购买组合、部署实施等，一系列要求大量知识和专业沟通的工作。此外还有专业完善的文档写作。

#### 商业模式变化

需求的驱动一端来自技术，另一端来自商业模式、来自客户。相比电商、社交网络、互联网，存储的商业模式变化相对缓慢，但近年来仍有一些变化。

大流行带来了 __居家办公__、__远程工作__ 的普及。企业借此削减办公室租赁费用，获利于全球招聘，跨州团队日常运作。远程办公催生 Zero Trust 的需求，以及办公软件（如 Office 365）、远程会议（如 Zoom）的增长。办公文档、文件共享、会议视频促进存储需求。

另一反复提及的趋势是 __STaaS__（Storage as a Service，存储即服务）。使用 Web 服务提供存储服务不仅便利，省去客户的升级管理负担，还使得按实际使用量付费（Consumption-based）变得可能。相比 upfront 购买机器，企业降低了成本。__云计算__ 也算作此趋势。

有更多趋势，例如，__生成式 AI__ 在用户界面和客户支持中的集成，客户变得青睐 __SDS 存储__，__容器__ 成为集群管理的基本模式，__归档存储__ 在 GDPR 下的普及。

数据库市场更加活跃，例如，数据库在 SQL、NoSQL、__NewSQL__ 间的变迁，数据仓库的 OLAP、OLTP、__HTAP__ 混合，以及 __数据湖__。

#### 政策合规

市场需求的另一变化来源是政策合规。近年来的变化有 __GDPR__、__数据主权__，以及相应的 __地理跨区存储__ 等。

GDPR 强迫增加业务成本，也意味着增加了客户支出，从而增加市场规模。新政策规范催生新技术，以满足隐私管理、数据归档的需求，进一步扩大市场，驱动增长。

特别地，政策可以被市场的头部参与者 __主动推动__，以加快相对缓慢的商业模式变化。另一方面，严苛的合规要求增加行业准入门槛，排除体量较小的竞争者，加宽现存参与者的护城河。

### 什么是价值

关于市场的分析中，最核心的问题是，什么才是历久弥新的真正价值。这里的“价值”要求很高：

  * __溢价__：即使对手出售拥有同样功能集的产品，我们仍能卖出更高价格。

  * __不可复制__：即使技术完全泄露（或开源），我们的产品仍能卖出更高的价格。

  * __稳定__：不随时间衰减，跨越市场周期，在风险中稳定。

__技术__ 能够提供良好的竞争优势，但“价值”的要求更高。技术容易被复制，专利可能被绕开。颠覆式创新注定瓦解现存技术的优势，市场周期确保这一定会发生。

__核心技术__ 具有同样的不利问题。“核心”意味着在“大量”地方可以“复用”。那么，它是容易迁移的，只要被对手复制，就可为其所用。对手大概率会遇到相似场景，并自发地开发类似技术。一人开发成功技术，即可复用到各处，导致所有人失业（例如，开源的天然垄断性）。相反，复杂性、垄断，反而更容易构筑护城河（见下文）。

技术带来进步的 __效率__，例如网购平台相比实体商店的决定性优势。但这并不能阻止竞争者入场，搭建新的网购平台。相反，护城河常常围绕信任关系、垄断、迭代速度构筑（见下文）。

下面，本文将真正的价值分解为多个方面，并逐一讲解：关系、复杂性、速度、文化、资产、数据、粘性、垄断。

![Overview of what composes true value](/images/vision-market-value-overview.png "Overview of what composes true value")

#### 关系

这里的关系指连接（Connection），更接近图论，而不仅仅指人际关系。自然地，拥有广泛而丰富的连接的实体，更加健壮和稳定。连接组成链条，形成网络。

关系的例子有哪些？良好的 __政府关系__ 帮助大型企业拿到高额的采购订单，甚至有能力影响政策，制定行业准入门槛。__社交网络__ 构建于人际关系，广泛、粘性、挖掘价值巨大。网购平台与 __大量客户连接__，建立信任，获取流量。企业与 __金融信任__ 的关系（Credit），帮助其拿到成本更低、更灵活的融资贷款。企业对 __供应链__ 的培养，与众多供应商的紧密合作，帮助提高产品质量并稳定风险。拥有 __全产业链__ 的企业，能够聚焦投资于单个产品以量突破，相比只有单个产品的企业更具优势。

广泛的连接让居中者成为 __中介__，往往比其连接的单个生产者更具优势，而 __1 对 N 构成垄断优势__。顺风时期，利用关系的弹性，快速扩展规模。面对风险时，中介方容易通过多重连接转嫁风险，而单一生产者则需刚性应对。中介方的优势并不依赖 __技术__ 获得，广泛的连接易于获取 __信息优势__，甚至能够通过与技术端的连接，分享其利润。遍身罗绮者，不是养蚕人；牧畜产肉奶，收获却是人。

对于人而言，在能够自由选择的情况下，关系的根本是 __信任__（Trust）。信任是 __资产__、是价值，需要时间积累、维护，并且随时间增值。

#### 复杂性

上文提到，单一核心技术难以匹配真正的价值。而持久的竞争优势往往来自众多技术组成的复杂性的 __技术体系__。它来自先发优势、常年的积累。其中的单个人极难完整讲述，亦或理清整个体系，乃至复制。

并且，技术体系是是 __活的__：拥有真实活跃的市场、竞争者、客户、销量，在持续的 __反馈循环__ 中改进。其中有人和经验。复制活物更加困难。

如何加快技术体系的积累？持续的高速是真正的价值之一，在下节 __“[速度](.)”__ 中讲解。它需要维持高质量的企业 __组织关系__、__[文化](.)__，维持大规模、复杂 __成熟__ 的产品、产品组合，维持高效的 __执行力__、人才组合、工程实践，维持部门、客户、供应链的 __[关系](.)网络__，并努力降低沟通和交易成本。它们关联到本文的各章节。这些 __无形资产__ 所体现的复杂性，需要长时间的建设，并且极难复制。

复杂性有更多的例子。典型的是 __经验__，其难以通过讲述、书本直接学习，其中混合大量零散片段、错乱交织，以及直觉。必须亲身经历、时间积累，正是“难以复制”。另一方面，其往往难以迁移复用，导致疏于传播、造成稀缺，反而加强在本地企业中的价值。

另一个例子是 __数据__，将在下文讲解。数据是现代企业的核心竞争力之一，庞大、复杂、有待挖掘，并源源不断注入。

#### 速度

速度的英文 Velocity 更应景，指企业产品或技术体系 __快速迭代__ 的能力。如果将产品的功能集比作城市建筑，那么速度类似 __高速公路__，虽然不对应直接产品功能，但对建设速度至关重要。

企业 __持续__ 地高速迭代产品的能力，是真正的价值之一。即使被对手 __完全复制__ 产品和技术（如开源），仍能够通过未来的速度赢得客户。例如 SpaceX 对传统航天机构的决定性优势，例如 Chrome 浏览器的频繁更新 vs IE 浏览器曾经的“年度”更新。此外，速度之外，__加速度__ 甚至更为强大。

企业如何维持速度优势？上一节 “__[复杂性](.)__” 已经列举。企业需要良好的 __管理体系__，控制成本收益，输出高质量产品和服务，并在 __成熟度__（见前文小节）上持续前进，背后是企业 __[文化](.)__。另一方面，企业需着力 __投资__ 和创新孵化，以应对周期性的 __颠覆式创新__ 和原市场衰退。

从系统开发角度，成熟的 __Continuous Integration（CI）系统__、全球协作、GitHub 颇具价值。这里可见为何 GitHub 被 Microsoft 收购。另一方面，2C 产品在迭代速度上，天然对 2B 产品具有优势，后者的数据存储类产品尤其慢（数据不容损坏）。常见的策略是，__用 2C 产品带动 2B__，例如，公有云供应商 Amazon、Google、Microsoft、Alibaba 都兼具两类产品。

从速度作为“价值”的角度看，可以理解互联网公司普遍追求的 __996__、加班文化，此“价值”甚至超越核心技术。尽管对公司的价值与对个人的价值往往并不一致，见下文 “__[推论](.)__” 部分。

#### 文化

企业文化在前文多已提及。根植于人于人 __[关系](.)__ 的无形资产，往往最难以复制。企业文化涉及 __[复杂](.)__ 的组织建设，历经多年积累。__[速度](.)__ 需要企业文化支持，以维持强大的执行力和创新精神。

在与客户的关系中，__品牌文化__ 在消费品市场中极具价值，例如众多的奢侈品。即使对手复制同样的商品，文化加持的产品也能卖出更高的价格。

在企业内部，良好的 __雇佣文化__ 有利于维持员工稳定，以更优惠的价格招揽同样的人才。__末位淘汰制__ 往往以危害文化为代价，牺牲真正的价值以节省开支。管理者的权利来源于裁员；重新招聘类似再抽签，而未修复任何问题。

#### 资产

简单直接地，大量的钱就是“价值”。资产通过利率增值，是乘法，按照 __指数增长__，能在你 __睡觉__ 时为你赚钱，并 __持续__ 下去。而劳动力是加法，“时间-收入”是 __线性__ 的，必须有你在场劳动，一次付出换取薪酬后便消失，并随年龄 __折旧__。

个人开发者与体力劳动者的区别在于，__知识是资产__。知识能够提供额外工资回报，随着经验和更多知识的积累而增值，付出后可重复使用，并得到 __复杂性__ 的保护。知识容量可获得十倍增长，而很难想象体能获得十倍提升，如 100 米短跑从 12 秒变成 1.2 秒。况且，体育竞赛只有一个冠军，其 “__内卷__” 比知识工作更为严苛。类似地，__996__ 式纯体力输出的工作方式并不明智，人无法每天工作十倍多的时间。

相应地，__技术__ 对于公司而言，类似知识资产。公司还能大量拥有 __其它类型的资产__，如现金、证券、存款、品牌、用户、房地产、机器、产权、专利。众多资产需要有效 __管理__（见下文“管理者”），确保每一份资产的产出都至少达到 __市场利率__ 水平。反例是，付出开发成本的项目被取消。另一方面，资产管理需要考虑 __维护和折旧__、__税收__ 成本，以及 __政策风险__。折旧是资产的一大成本。

类似折旧，知识资产 __随时间贬值__（Expiring Asset），对个人开发者影响更大。而普通资产，往往能稳定产生利息，随时间增值，并通过变现阻止折旧。更重要的是，普通资产受私产 __法律保护__，而这并不直接适用于脑中的知识。

快速贬值的资产更需要管理。投资管理的准则之一是 __多元化__。而个人开发者的专精单一技术的 __专家路线__，可以说是背道而驰。尽管专精的技术专家在招聘中受到青睐，但对于公司，从前文看，销售 __产品组合__ 更具竞争力。（同理，个人能力组合是否更利于招聘？）

多元化类似 __众多的连接__，见前文 “[关系](.)” 一节，公司部分已经覆盖。对于个人开发者而言，一种选择是在公司内积累经验并建立广泛的人脉（人脉是互惠的，而非资产排他），另一种选择是在公司外建立连接，确保知识和工作的 __可迁移性__（例如开源技术），第三种选择是 __管理者__。

公司经营的重要一环是管理者，__管理者的工作本质是投资__（前文提到资产管理的“市场利率”）。例如选择项目方向、雇用人员，对应的是工资等的投资。管理者使用 __公司的资金__ 进行投资，并从投资回报中支付自己的工资。相比个人开发者，管理者的工作天然具有 __多元化__（也常常“多线程”）。例如同时运作多个项目、孵化多个创新、雇佣多名员工。管理者与员工满足 __1 对 N 的 [关系](.)__，前者在风险中更加稳定，并可分发裁员名额。管理者并不直接依赖 __技术__ 获取竞争优势，但极具价值。

此外，许多工作岗位不具备资产的特性，却是社会运转的必要工作，献身其中的人是真正的勇士。

#### 数据

数据是现代企业的核心竞争力之一。数据通常拥有 __庞大__ 的体量，多维度的复杂结构，有待挖掘的价值，受到产权保护，并且是“活的”。容易复制产品功能，但难以复制背后的数据。

__活的__ 数据意味着被大量真实客户使用、被维护、并不断地更新。更重要的是，__被验证__，尤其对于存储产品。在用户创作时代，活的数据积累了大量客户创作、社交关系、使用习惯和历史。用户、数据、产品构成不断演进的 __反馈循环__。

另一方面，数据往往具有 __[粘性](.)__（见下文小节）。客户迁出数据的成本高昂，和数据量成正比，随着数据积累增加。迁移数据往往带来格式不兼容、功能不匹配、高昂的传输费用等问题。

公司的 __[速度](.)__（见前文小节）依赖数据。现代项目管理、产品评估、创新，构筑于 __数据驱动__ 之上。例如，评估某新存储功能带来的成本收益，并实时监控上线后的运行反馈。

#### 粘性

粘性与产品的场景和特性有关。粘性提高用户迁出或放弃产品时的成本，例如积累的大量 __数据__，培养的 __用户习惯__。

另一种情况是 __外部粘性__，例如社交网络，一个用户使用产品，导致社交圈下的其他用户也倾向使用同一产品。另一个例子是企业产品组合的互相捆绑，俗称“全家桶”，优化同家产品互联，并劣化与竞争产品的兼容性。

在技术和功能之外，粘性提高了产品的价格，甚至帮助企业走向 __垄断__。即使对手完全复制产品，也难以赢得客户。

#### 垄断

垄断为企业提供决定性的竞争优势，极具价值。垄断能够以高价出售产品，并影响政策以维护自身地位。垄断并不一定依赖技术，甚至常常减缓技术发展。

常见的垄断来自高度的 __规模效应__，例如水电基础设施、云计算、互联网平台。参与者常在早期赤巨资扩展规模，在达成垄断地位后获取超额收益。最终，在反垄断的政策限制下，通常市场上会留下两家企业，形成 __寡头__ 局面。

另一种垄断来自 __粘性__（见前文小节），例如社交网络。第三种来自 __政策性垄断__，常见于公共事业和国家安全，例如石油产业。

此外，一种类似的企业行为是快速 __扩大市场体量__，增幅营收、压低利润率、加速迭代产品。其利用巨大体量获取银行融资的便利，在供应链上下游压货、压款以获取金融利差，并以巨量雇佣岗位获取政策优惠。例如新能源造车行业。

#### 关于：有价值的技术

什么样的技术能够接近“价值”的要求？一则是见前文提及的，具有 __[复杂性](.)__ 和 __[速度](.)__ 的技术体系。或者，尖端技术并且 __被保护__，以对抗可复制性。

生成式 AI 是新近的尖端技术，同时也具有复杂性，但仍难以阻挡众多竞争者入场，并在各国复制和传播该技术。持有该技术不足以使企业生存，要么跑得足够快，见 [速度](.) 一节，要么配合其它产品，意味着企业还持有其它的“价值”。

#### 关于：价值与市场周期

虽然“价值”有利于企业获得竞争优势，但长远来看，许多“价值”追求会降低市场活性，加速市场老化。例如，对 __垄断__ 的追求和设置政策门槛，有意制造产品 __粘性__ 以捆绑客户，编织特殊待遇的政商 __关系__。

最终，价值被排他地锁定在头部参与者中，新人进入市场将处于劣势。要么选择 “__卷__”、激烈竞争、996 式劳动输出，要么选择 “__躺平__”、跟随市场老化。

或者，在旧市场中革命，开辟新的世界。由此，__颠覆式创新__ 到来，开启新一轮市场周期。颠覆式创新的另一个名字是破坏式创新。

#### “推论”

有许多关于个人 __职业发展__ 的讨论，见前文 “[资产](.)” 一节。另一方面，在 __粉丝经济__ 中，粉丝更接近于资产，其价值远超单纯劳动力输出。这解释了为什么“宁可做主播也不进厂”，尽管粉丝并不像普通资产一样受法律保护。

关于 __[关系](.)__ 有进一步的思考。技术链条也是关系的网络，单一技术只是产业链条上下游定义的语言（不可迁移性），部分反映物理世界（__可迁移性__）。薪酬的回报取决于 __上下游__ 市场，技术艰深并不确保之。相反，__虚拟__ 的往往更值钱，因为满足 1 对 N 的关系，例如软件管理硬件、老板管理员工、金融投资实业。虚拟部分掌握资源分配、沟通渠道、信息流通等更具 __价值__ 的部分，乃至法律、政策。

对 __[资产](.)__ 有更多深入的思考。训练有素的分析者看 __一切事物都标记着利率__，__金钱正在无声嘶喊__，比人的嘴更值得信赖。法律、政策同理。社交网络的喧闹信息，其重要性可以按照背后流动的金钱排序。现代社会中，无法听到金钱的声音，无异于盲人聋哑。

通过对金钱的建模也可还原个人乃至社会的真实偏好。人们为保卫生命而激发的杀戮欲望，远超对普通消费品的购买需求。社会仇恨具有良好的资产特性，地缘政治冲突的获利空间巨大，可持续战争光华毕现（不幸）。

### 总结

在前文列举存储市场的基础上，本文分析了市场的诸多特性。例如天然结构、生命周期、颠覆式创新等。接下来，本文分析了背后的驱动因素，它们是预测未来、寻找需求的引导。最后，本文揭示了什么是真正的价值。在技术之上，其为企业和个人带来不可复制的竞争优势。

另外，其它值得一读的文章：

  * 腾讯 22 年前的神级 PPT 立项汇报：[https://zhuanlan.zhihu.com/p/684222828](.) 。Highlight：__市场分析__。

  * 硬核分享云产品定义 - 曹亚孟：[https://mp.weixin.qq.com/s/8sQINI40GZlXm8l9Wd6n-w](.) 。Highlight：__定义的能力__。

  * 技术 Leader 的思考方式 - 朱春茂：[https://developer.aliyun.com/article/940003](.) 。Highlight：__技术产品管理__。

## 存储系统中的硬件

相比软件层面优化所需的人力成本和漫长周期，硬件性能往往指数增长。硬件的快速发展、模式的转变，是存储系统演进的持久动力之一，并向上重塑用户和市场。硬件能提供什么，是思考系统架构和未来战略的基石。

本章讨论存储系统相关的硬件，从数据层面评估，围绕它们的性能、成本、和未来增长。本文之后思考它们对存储系统的影响。

（关于存储中的软件，见 [A Holistic View of Distributed Storage Architecture and Design Space](https://accelazh.github.io/my%20book/A-Holistic-View-of-Distributed-Storage-Architecture-and-Design-Space)）。

### 数据表

下表展示常见存储、网络、计算硬件的容量、带宽、能耗数据，并比较单位价格。数据均来自互联网，力求反映大致规模。准确的数据往往需要专业市场团队，受品牌和采购组合的影响，规模供应商甚至能提供折扣。

  * __HDD__ 吞吐量增长较慢。HDD的容量成本随新技术 SMR、HAMR 等逐步下降，导致单位容量性能缓慢下降。大致上，十年来 HDD 的容量增加了十倍，但吞吐量仅增加两倍。下表使用吞吐量（带宽），忽略IOPS，前者更反映综合性能。

  * __SSD__ 在 NVMe 技术下，近年来吞吐量呈指数增长，延迟接近原生闪存，瓶颈变成 PCIe。ZNS 等技术进一步改善容量和成本，大容量闪存利用并发通道提升性能。大吞吐量下，闪存磨损仍然是问题。近年 SSD 的单位容量成本快速下降，甚至有低于 HDD 的趋势。反直觉地，尽管单价昂贵，SSD 的单位带宽成本和能耗反而低于 HDD。

  * __DRAM__ 带宽随 DDR 技术换代呈指数增长，能耗随降低的电压逐步降低。Amazon 可采样容量和价格，下表以 DDR4 为基准。现代服务器常配备双通道、四通道以进一步提高带宽。DRAM 的能耗常分为静态刷新部分和读写传输部分，总体上与电压平方成正比。

  * __HBM__（High-bandwidth memory）常用于 GPU 或片上内存。相比 DRAM，它采用大接口宽度和堆叠提高带宽到极高水平，读写传输能耗很低。HBM 是随 GPU 变得广为人知的新技术之一，目前缺点是昂贵，单位容量价格是 DRAM 的约十五倍。

![Hardware prices - Storage](/images/vision-hardware-prices-storage.png "Hardware prices - Storage")

  * __Ethernet__ 是近年发展最快的技术之一，带宽呈指数增长，几乎每两年翻倍，成本呈指数下跌。今天 100Gbps 网卡已经常见，200Gbps 正被部署，400Gbps 逐步出现。存储系统架构正被快速提高的网络带宽重塑。相比服务器中的 DPU，ASIC 是交换机中广泛使用的技术。

  * __PCIe__ 带宽随 PCIe Gen 换代呈指数增长，几乎每隔几年翻倍。其延迟取决于频率（100Mhz）。下表使用 PCIe Gen5.0 16x 作为基准。PCIe 价格绑定在主板上，Amazon 可采样主板售价，近年来基本维持稳定。尽管 PCIe 带宽较高，但远不及 GPU/NVLink，也仅勉强跟上 SSD（一机多盘）、Ethernet。

  * __CXL__ 由 Intel 主推，将原来集成到 CPU 的内存桥归还主板控制，整合 PCIe，并实现远程访问的缓存一致性。尽管被热烈讨论，但明确的产品不多。CXL 1.1 和 2.0 使用 PCIe Gen5.0 作为物理层，本文基于 PCIe 推测其性能和成本。

  * __NVLink__ 可替代 PCIe 实现 GPU 互联，相比 PCIe 拥有极高的带宽和相近的延迟。今年 NVLink 带宽呈指数提高，鉴于生成式 AI 的革命性和投资热度，其发展甚至可能加快。结合 AI 对高带宽和 All-to-All 通信的需求，NVLink 正在重塑 AI 集群架构。下表以 NVLink Gen4.0 为基准（ A100 使用 Gen3.0 ）。价格上，NVLink 与 Nvidia GPU 捆绑出售。

![Hardware prices - Networking](/images/vision-hardware-prices-networking.png "Hardware prices - Networking")

  * __CPU__ 性能可分解为核心数 X 频率 X IPC 。IPC 由单线程性能反映，逐年缓慢提高。核心数近年提高较快，尤其是服务器 CPU，甚至有 Manycore 研究方向。而频率的增长受限于芯片散热和服务器能耗。CPU 总体性能常用 Linux 内核编译时间，或网络通信吞吐量来衡量。下表以 AMD EPYC 7702P 64-Core 为基准。

  * __GPU__ 提供极高的 FLOPS 计算性能，核心数和并发数远胜 CPU。相比 CPU 受限于 DRAM 带宽内存墙，GPU 的 NVLink 和 HBM 带宽极高。今天 GPU 售价昂贵且一卡难求，未来预期单位成本的计算能力呈指数提高，并能耗下降。下表以 Nvidia A100 为基准。

![Hardware prices - Computation](/images/vision-hardware-prices-computation.png "Hardware prices - Computation")

注意上表中 Projection 列即使 10% 的差异，因为指数，都可导致翻倍/半衰年数的显著不同。可与下表对比：

![Hardware prices - Projection scale](/images/vision-hardware-prices-projection-scale.png "Hardware prices - Projection scale")

数据来源及引用：

  * HDD: [[1]](.) [[2]](.) [[3]](.)
  * SSD: [[4]](.) [[5]](.) [[22]](.) [[23]](.)
  * DRAM: [[6]](.) [[7]](.) [[8]](.) [[24]](.) [[27]](.)
  * HBM: [[9]](.) [[10]](.) [[11]](.) [[28]](.) [[29]](.)

  * Ethernet: [[12]](.) [[17]](.) [[24]](.)
  * PCIe: [[13]](.) [[14]](.) [[15]](.)
  * CXL: [[30]](.)
  * NVLink: [[16]](.)

  * CPU: [[18]](.) [[19]](.) [[25]](.) [[26]](.) [[41]](.)
  * GPU: [[20]](.) [[21]](.) [[31]](.)

[[1]](.)

![Goughlui.com  HDD throughput by year](/images/vision-goughlui-hdd-throughput-by-year.png "Goughlui.com  HDD throughput by year")

[[3]](.)

![BlocksAndFiles.com Enterprise SSD prices vs HDD by year](/images/vision-blocksandfiles-ssd-price-by-year-hdd.png "Enterprise SSD prices vs HDD by year")

[[6]](.)

![DRAM capacity, bandwidth and latency](/images/vision-modern-primer-dram-growth.png "DRAM capacity, bandwidth and latency")

[[8]](.)

![AIImpacts.org Trends in DRAM price](/images/vision-aiimpacts-trends-in-DRAM-price.png "AIImpacts.org Trends in DRAM price")

[[12]](.)

![NextPlatform.com Trends in Ethernet price](/images/vision-nextplatform-trend-ethernet-price.png "NextPlatform.com Trends in Ethernet price")

[[19]](.)

![AIImpacts.org Geekbench score per CPU price](/images/vision-aiimpacts-core-cpu-price.png "AIImpacts.org Geekbench score per CPU price")

[[26]](.)

![KarlRupp.net CPU, GPU Performance Per Watt](/images/vision-KarlRupp-cpu-gpu-perf-watt.png "KarlRupp.net CPU, GPU Performance Per Watt")

[[31]](.)

![FLOPs/clock-cycle CPU vs GPU](/images/vision-FLOPs-clock-cycle-CPU-vs-GPU.png "FLOPs/clock-cycle CPU vs GPU")

[[32]](.)

![Google Data Centers PUE](/images/vision-google-datacenter-pue.png "Google Data Centers PUE")

[[33]](.)

![Uptime Global Data Centers PUE](/images/vision-uptime-global-datacenter-pue.png "Uptime Global Data Centers PUE")

[[34]](.)

![Server component-wise energy](/images/vision-server-component-wise-energy.png "Server component-wise energy")

上述数据可以用来计算不同架构下的存储成本，以及未来竞争力。特别地，容量、带宽价格反映购买成本，而能耗反映反映运营成本（TCO）。

### 额外成本

首先是能耗及制冷成本，一份能耗同时带来对应的制冷成本，两者加总为数据中心电费开销，几年后电费甚至超过购买成本。

  * __PUE__: 数据中心能耗效率。假如服务器能耗是 500W ，数据中心的 PUE 是 1.5x，则这台服务器包括制冷需要耗能 500W * 1.5 = 0.75KW 。假设电费是 \$0.1 每 KWh ，则一年耗电 $657，五年电费甚至超过服务器购买成本。

  * 常见数据中心 PUE 在 1.5x 左右，并基本维持稳定 [[33]](.) 。Google 数据中心甚至能将其压缩到 1.1x [[32]](.) 。

然后是网络带宽，一份服务器带宽需要配套对应的 T0（TOR）、T1、T2 等交换机带宽。

  * 假设 100Gbps 服务器网卡，T0、T1 层使用 100% 带宽 Full-provisioning ，T2 层使用 50% 带宽 provisioning，忽略更高层次 T*。加起来额外带宽配比有 __2.5x__ 。

除存储、网络、计算组件外，服务器在额外组件上花费的能耗数量可观。约 __30%__ 的额外能耗花费在电力传输（15%）、主板（10%）、冷却风扇上（4%） [[34]](.) 。

### 与公有云价格的比较

如今的公有云价格是作成本评估的良好参考，除非需要重新思考存储系统的架构，和硬件提供的可能性。本节以公有云存储 Azure Storage [[35]](.) 为基准，比较上文计算的存储成本数据。

![Azure Blob Storage pricing](/images/vision-azure-storage-blob-price.png "Azure Blob Storage pricing")

除前文提到的额外成本外，需要计算对于 1GB 存储应配套的 DRAM、Ethernet、PCIe 等。DRAM 涉及被缓存的数据比例。HDD 和 SSD 往往价格显著不同。CPU 需要依带宽处理能力配置。数据复制、压缩、纠删码可显著影响物理数据体积。冷数据可以极低带宽成本存储。

  * 单位全文统一，容量 GB，带宽 GBps，货币 $。

![Storage cost parameters](/images/vision-storage-cost-parameters.png "Storage cost parameters")

下表计算了 __1GB 的 HDD 存储所需成本__，考虑了主要服务器组件、额外网络交换机配套、数据中心制冷等，也考虑了数据复制、压缩，以及部分是冷数据。购买成本和能耗成本都包含，购买成本按 60 个月摊还。可以发现：

  * 相比 Azure Storage Reserved Capacity ，计算出的数据成本是 Cool 的约 1/22x，是 Archival 的约 1/4.5x 。

  * 当然，文中的计算力求简单清晰，比实际 __忽略了诸多开销__。例如互联网带宽费用、数据中心建设、研发费用、销售费用、读写 IO 放大、SSD 磨损、跨区复制、备份和容灾等等。

  * 除存储外，Azure Storage 对数据读写额外收费。持续的高 IOPS ，或对冷数据的大带宽访问，费用高昂。而计算出的数据成本已经将 1GB 对应带宽纳入。

![Storage cost HDD](/images/vision-storage-cost-hdd.png "Storage cost HDD")

  * 计算出的 HDD 存储中，显著的购买成本从高到低分别是 HDD、DRAM。显著的能耗成本从高到低分别是数据中心制冷、HDD、服务器额外、DRAM。总能耗成本约占购买成本的 40%。

![Storage cost HDD ratio](/images/vision-storage-cost-hdd-ratio.png "Storage cost HDD ratio")

  * 同理计算出 5 年后的数据，各成本组分变化不大。主要因为各组件成本都在下降。但总能耗成本占购买成本上升到约 60%。（虽然 1GB 容量对应的 HDD 带宽在下降，计算时假定配套带宽不变。）

![Storage cost HDD ratio 5 years](/images/vision-storage-cost-hdd-ratio-5years.png "Storage cost HDD ratio 5 years")

下表是 __1GB 的 SSD 存储所需成本__，与 HDD 版本对比，可以发现：

  * 相比 Azure Storage Pay-as-you-go ，计算出的数据成本是 Premium 的约 1/34x。当然，文中的计算相比实际忽略了诸多成本。

  * 计算出的 SSD 存储成本是 HDD 的 12x 左右，与 Azure Storage 类似，Premium 是 cool 的 15x 左右。

  * 计算出的 SSD 单位带宽的成本比 HDD 更低，这与 Azure Storage 相符，Premium 的读写价格比 Hot 更低，数据越冷读写成本越高。

![Storage cost SSD](/images/vision-storage-cost-ssd.png "Storage cost SSD")

  * 计算出的 SSD 存储中，显著的购买成本从高到低分别是 SSD、CPU。显著的能耗成本从高到低分别是数据中心制冷、服务器额外、SSD、CPU。总能耗成本约占购买成本的 50%。

![Storage cost SSD ratio](/images/vision-storage-cost-ssd-ratio.png "Storage cost SSD ratio")

  * 同理计算出 5 年后的数据，各成本组分变化不大。主要因为各组件成本都在下降。但总能耗成本占购买成本上升到约 58%。（虽然 1GB 容量对应的 SSD 带宽在上升，计算时假定配套带宽不变。）

![Storage cost SSD ratio 5 years](/images/vision-storage-cost-ssd-ratio-5years.png "Storage cost SSD ratio 5 years")

可以推想，对于 SSD 存储，如果数据热度高、操作频繁、传输带宽大，并且功能简单，使用本地数据中心可能有成本优势。而对于冷数据，公有云是理想的存储地点，利用 Reserved Capacity 能进一步降低成本。

### 选择 HDD 和 SSD

基于需要的容量和带宽，可以将上文数据表中购买 HDD 或 SSD 的成本绘出，比较不同选择。加上能耗开销后结果类似。可以看到：

![HDD/SSD price selection](/images/vision-hardware-hdd-ssd-sel.png "HDD/SSD price selection")

  * __Area 1__ 和 __Area 2__ 分别对应1）低带宽高容量需求，使用 HDD ；2）高带宽低容量需求，使用 SSD。相比 SSD，HDD 的带宽很低，因而 Area 1 面积较小。

  * __Area 2__ 全部使用 HDD，但带宽需求较高，需要为带宽额外购买 HDD 容量。__Area 3__ 全部使用 SSD，但带宽需求较低，给定容量的 SSD 有带宽闲置。

  * 作为改进，__Area 2__ 和 __Area 3__ 适合使用 HDD 和 SSD 的混合存储，或者使用 SSD 作为 HDD 的缓存。

### 硬件发展的推动因素

硬件性能如此高速发展，它受何推动？推动因素可以从技术层面和市场层面分析。

技术层面，总体上，更小的制程、更高的集成度、专用设计的芯片、更高的频率、新型物理介质，__摩尔定律__ 推动硬件性能指数提高。在各个组件上，近年来都有一系列技术创新：

  * __HDD__: 不断提高的存储密度，近年来逐渐推广的 SMR 技术，以及未来将采用的 MAMR、HAMR 等 [[36]](.) 更复杂但密度更高的存储技术。

  * __SSD__: 一系列技术从不同层面提高 SSD 性能。接口协议如 NVMe、NVMoF。简化 FTL 层如 ZNS、FDP [[37]](.) 。闪存架构如 3D NAND 。提高闪存密度，使用新型物理介质如 TLC、QLC、PLC 。

  * __DRAM__: 每一代 DDR 不断提高时钟频率，改进架构，降低电压。DRAM 的密度、封装也在改进，如 3D Stacking 技术。

  * __HBM__: 与 DRAM 一道，HBM 的堆叠技术在持续改进，允许更多层数和更高的跨层传输速度。线路的信号传输速率、接口宽度也在提高。

  * __Ethernet__: 以太网协议不断换代，大幅提高传输带宽。近年来 RDMA RoCEv2 普遍被采用，服务器使用 ASIC 芯片替代 CPU 处理高速网络。光纤交换机也在数据中心采用。

  * __PCIe__: 每一代 PCIe 的不断提速得益于编码协议和同步效率的改进，更多数据在一个时钟周期内传输。传输介质的改进容许更高的速率。然后，Lane 乘数加倍，并行传输。

  * __CPU__: 性能在不同层面得到改进。更多的晶体管数量、集成度，更小的制程。多核、Manycore 集成于一个处理器中。频率的小幅提高。微架构的改进、更高的 IPC 。新型向量处理指令 SIMD 。集成专用任务的加速器。能耗优化、DVFS 等技术。

  * __NVLink__: 类似于 PCIe ，PCIe 本身也在高速发展。NVLink 的提速额外受益于与 GPU 的高度集成、更大的连线宽度等，以及 AI 热度带来的投资。

  * __GPU__: 得益于生成式 AI 的工业革命式的投资热度，GPU 领域快速发展。每一代新 Nvidia GPU 更新架构，更多核数、执行单元，集成更多更大容量的组件，并减小制程。Tensor Core 和 RT Core 为专用任务优化。相比于 CPU ，GPU 将内存、总线集成于自身板上。HBM、PCIe、NVLink 本身也在高速发展。相比于 CPU ，GPU 的时钟频率较低，近年来持续提高。

硬件发展的另一方面推动力来自于市场需求。可以从衡量存储性能的常见指标上理解：

  * __容量__: 经典的大数据 3V [[38]](.) 理论 - volume, velocity and variety 。对比其它行业如彩电、冰箱、汽车，很少有市场能像数据一般贪婪地增长。__热数据量总是有限的__，正比于业务活跃周期 X 事务频率，意味着冷数据有广阔的优化空间；而政策合规进一步推高需求。用户乐于为基于容量的额外需求付费，如安全加密、备份容灾、分析挖掘等。

  * __吞吐量__: 更丰富的媒体体验，图片、视频、流媒体，AI 训练和服务，近年来仍在驱动需求增长。

  * __IOPS__: 事务处理偏向 IOPS 需求，数据库是少见的成熟但经久不衰的市场，近年来仍持续孵化创业公司。另一方面，Web、移动应用、互联网触及并深入每一个人。__O(1)__ 规模的业务极其少见，即使好莱坞大片也难以达到（O(P) 指调查每一个人，有 P 概率使用该产品）。

  * __延迟__: 相对于人的感知，如今的硬件速度已经极快，延迟低于阈值后变得不再重要。但量化交易仍不竭地追求更低延迟；计算复杂的 AI、自动驾驶的延迟需求未被满足；以及物联网、机器人等接入物理的领域。另一方面，软件正变得日益复杂，意味着延迟优化被持续需要。

### 观察和要点

仔细观察上文的硬件数据表，可以发现许多值得思考的要点：

  * __延迟无法购买__。从上文数据表可以看到，带宽、容量均有价格，更多的钱可以购买更多，技术上横向扩展。但延迟例外，甚至不像带宽和容量有逐年的显著提升。改进延迟往往需要技术换代（无法预期），或从头替换存储介质（成本、迁移巨大）。延迟是最昂贵的。

  * __数据容量对应的成本仍然昂贵__。从上文数据表可以看出，无论是购买成本还是能耗成本，无论是 HDD 还是 SSD 存储，硬盘都占据显著位置。可以想见，任何 Data Reduction 技术，如压缩、去重、纠删码，都有显著改进存储系统成本收益的潜力。

  * __DRAM 占有显著的购买和能耗成本__。相比 SSD，DRAM 购买成本昂贵。即使带宽未实际使用，DRAM 的静态刷新也持续耗能。尤其是 HDD 存储，DRAM 成本相比廉价的硬盘更加显著。一些新技术有利成本，如利用 SSD 而不是 DRAM 管理元数据，将冷（元）数据从 DRAM 卸载到 SSD。

  * __DRAM 带宽在未来可能成为瓶颈__。一台服务器不会有太多 DRAM 通道，但可以安装几十盘 SSD 。Ethernet 带宽增长速度也远超 DRAM 。GPU/NVLink 带宽远超 DRAM 。而 DRAM 容量昂贵、能耗高。作为 CPU-IO 的桥梁，DRAM 带宽会被一份数据多次消耗。CPU 内存墙问题今天已经显著。有一些勉强的解决方案，如为服务器插入额外的小容量 DRAM ，使用 DDIO [[39]](.) 技术让短命数据跳过 DRAM 。

  * __SSD 尽管昂贵，但单位带宽价格远好于 HDD__。这意味着用 SSD 作 Write Staging ，用廉价 SSD 为云存储作普适加速，是自然趋势。另一方面，在 SSD 普及到 HDD 存储后，存储系统需要支持适度混合 SSD/HDD 来适配各级别的“带宽/容量比”需求。类似地，NVDIMM-N 使用 DRAM 作 Write Staging ，闪存作断电存储。

  * __在 SSD 存储中，CPU 的购买和能耗成本显著__。这来自于高带宽的配套要求。由此可以看到 DPU 和专用网络芯片在改善成本上的巨大潜力。近年来，ARM CPU 被越来越多的采用，AWS Nitro 芯片取得巨大成功，压缩、加密专用卡已不少见。

  * __CPU 的性能提升较慢，跟不上 SSD 和 Ethernet__ ，CPU 的能耗开销显著。这催生今年来的一系列技术路线：1）使用 DPDK、SPDK 跳过操作系统内核；2）使用 DPU、加速卡替代 CPU 处理负载；3）使用 ARM 替代 Intel CPU ；4）绕过 CPU-DRAM-PCIe 生态，如 GPU，使用 GPU-HBM-NVLink 替代。

  * __Ethernet 和 PCIe 的带宽和价格达到相近水平__，两者也在指数改进。合理的推想是，__能否用 Ethernet 替代 PCIe__，简化计算机体系结构？Ethernet 更容易横向扩展，互联多台机器，池化额外带宽。但相比 PCIe ，Ethernet 延迟更高，难以解决无损传输和一致性问题。CXL 在此路线上。

  * __反过来推想，能否用 PCIe 替代 Ethernet__？集群架构很大程度上取决于机器的互联方式，例如 Hyper-converged、Disaggregated、Geo-replicated 等。鉴于生成式 AI 对 TB 级互联带宽的需求，未来的集群架构可能分化为不同路线：1）大规模、GB 级互联带宽的存储系统；2）小规模、TB 级互联带宽的 HPC-GPU 集群。（1）计算存储分离，而（2）计算存储融合 Co-locating 。公有云需要针对（1）、（2）售卖新型产品。

  * __Ethernet 发展极快，超过所有其它硬件__。这与存储系统和数据库向 Disaggregated 架构、Shared-nothing 架构、存算分离、Shared-logging、Log is database 等方向发展相符。另一方面，__只有 HDD 单位容量的带宽持续下降__，对未来的存储设计提出挑战 [[40]](.) 。主要原因是机械硬盘技术已经十分成熟，性能提升受机械物理的限制，而 SMR、HAMR 等提升存储密度的技术还有空间。

  * __高性能硬件并不一定意味着昂贵的价格，甚至单位带宽成本反而更低__，例如 DRAM < SSD < HDD 。Ethernet 也有类似趋势，单位带宽成本 100 Gbps < 40 Gbps < 10 Gbps 。这暗示共享和池化有利可图，具有规模效应，云存储可率先采用高端硬件。

  * __数据中心制冷的能耗成本显著__。如果把 PUE 从平均水准 1.5x 下降到 Google 数据中心的 1.1x 水准，收益巨大；或者，直接使用云计算服务。能耗并不是数据中心制冷的唯一问题，制冷系统损坏（如雷暴、过热）并不少见。如何向高密度的机架输送足够电力，并配套足够制冷，也有挑战。__服务器能耗是巨大的问题__，甚至可能超过存储系统对性能的关注度，在云存储中尤其显著。反之，高度规模化的云存储比私有数据中心更容易找到优化能耗的办法，例如建设选址和 Free Cooling 。另一方面，公有云厂商可利用规模优势，要求定制的服务器设计，以进一步节约能耗。

### 软件的价值在哪里

从上文的数据表可以发现，硬件普遍存在性能的 __指数增长__，或成本的指数下降。而通过软件改善性能，不仅研发成本昂贵，一年可能也只有 30% 的提升。那么，软件的价值在哪里？

  * __为用户暴露裸硬件延迟__：上文提到“延迟无法购买”，这就是软件的价值之一，尽可能为用户提供裸硬件的原生延迟水平（而不是带宽）。同时，软件层需要对抗系统的复杂性、物理组件的距离、动态负载的变动。许多架构技术来源于此。

  * __管理大量硬件__：只有软件能做到，而硬件本身难以要求一块 SSD 盘去管理另一块 SSD 盘。以此衍生出管理分布式系统、管理复杂性、管理资源效率等方向。相关联的需求是 __系统集成__，企业对集成打通、统一管理不同品牌系统的需求非常常见，见 _[存储系统的市场](.)_ 一章。

  * __分布式系统__：软件层将大量硬件联合成为分布式系统，其间运转复杂的技术。虚拟化、调度、故障恢复、容灾、复制等等。只有软件层能够为硬件带来横向扩展、高可靠、负载均衡、地理复制等功能。直至云计算。

  * __复杂性__：在系统内部，软件层管理复杂的用户需求和复杂的系统需求。跨系统，软件层提供互操作性、兼容性、跨硬件协议接口。在产品和市场层面，软件维护多方参与的生态系统。统一命名空间、文件系统、数据库、访问协议等被设计出来，软件使本地的硬件能力走向全球化。软件受益于复杂非标准的功能带来的差异化竞争，而硬件的接口趋向标准化，激烈的性能、成本竞争削减利润空间。另一种说法是，软件提供 __大量功能__、__统一性__、__简化管理__。

  * __资源效率__：软件层通过负载均衡、拥塞控制、池化共享、并行处理等方式，提高硬件的资源利用效率。软件使统计大量硬件提供监控数据成为可能。软件可以在高低性能硬件间搭配迁移，以最佳成本配比。软件可以预测未来，调度负载和冷热。更重要的是，软件可以管理能耗这一数据中心头等成本。另外，需要减少软件自身带来的额外 __管理成本__。

另一方面，这意味着在选择存储系统架构，或者作为程序开发人员的职业发展上，需要仔细思考何为高价值方向。例如，将开发工资想象为投资投入，软件层性能优化的回报率是否足够高？

## 案例分析：EBOX

本章用一个案例来展示如何使用前文的框架进行分析。它能够帮助团队寻找前瞻性的投资方向，将技术创新映射到财务指标，规划未来 3~5 年的发展策略。EBOX 是个有趣的技术创新。

本章首先介绍什么是 EBOX，它的创新点，可能的收益与风险。接下来，本章从存储系统角度分析成本和收益、未来预期。然后，本章分析研发成本如何摊薄。最后，本章从供应商角度分析售卖 EBOX 是否有利可图。

### 什么是 EBOX

EBOX 是存储系统的一个有趣的可能的创新方向。它将传统的存储服务器进一步分解为 __硬盘框服务器 EBOX__ 和 仅剩计算功能的存储服务器。两者均可独立优化，在此基础上有一系列技术创新。有一系列来源提到了 EBOX 技术，同时介绍了 EBOX 如何工作：

  * __zStorage__ [[42]](.) : 下层存储使用双控的 EBOF 全闪存硬盘框，上层业务运行在标准服务器节点。所有业务节点共享访问 EBOF 存储节点。Vast Data 自己并不生产 EBOF 硬盘框，委托其它厂商生产，目标是让 EBOF 硬盘框变成像标准服务器一样廉价，发展生态。

  * __Vast Data__ [[43]](.) : 未找到 Vast Data 直接提及 EBOF 或 EBOX （同名但不同意，Vast Data 的指 Everything Box）。但如 zStorage 所总结，Vast Data 使用 DBox （NVMe JBOF）存储数据，CNode 计算管理集群，两者通过 NVMoF 联接。任何 CNode 可访问任何 DBox，这种共享架构大幅提高数据节点的可靠性（Availability，不是 Durability）。超长纠删码被允许使用，降低数据副本开销到 1.0x~1.1x 。

![Vast Data DBox](/images/vision-vast-data-dbox.png "Vast Data DBox")

  * __NVMoF for Disaggregated Storage__ [[44]](.) : 见下图，NVMoF 带来的诸多存储架构的创新，如果数据服务器足够简单和标准化，那么可以通过 Direct Access 的方法访问 SSD，不再需要 CPU。甚至 PCIe 也可以省去，与 Ethernet 合二为一。

![NVMoF E-BOF Disaggregated Storage](/images/vision-nvmeof-ebof-disaggregated.png "NVMoF E-BOF Disaggregated Storage")

  * __HammerSpace NFS-eSSD__ [[45]](.) : HammerSpace 的网络文件系统首先利用 NFS4.2 协议，允许客户端跳过元数据服务器，直接访问存储节点。进一步，存储节点不再需要 CPU、DRAM、PCIe，将 SSD 直接接入 Ethernet，用定制芯片控制。

![HammerSpace NFS-eSSD](/images/vision-hammerspace-nfs-essd.png "HammerSpace NFS-eSSD")

可以看到，EBOX 有一系列优势，本文基于它们分析成本收益：

  * __存储服务器与数据节点的全联接（Shared Everything）__。不同于以往数据硬盘被单一存储服务器独占，全联接架构可以将数据盘的可靠性（Availability）提高多个数量级。在此基础上，__超长纠删码__ 进一步降低数据副本开销。Fan-out 的联接有助于负载均衡。从 EBOX 到客户端的 DSR（Direct Server Return）有助于降低延迟。

  * __标准化的 EBOX 可将 CPU 替换为定制芯片或 DPU__。从 _[存储系统中的硬件](.)_ 章节可以看到，CPU 占有显著的购买开销和能耗开销。将 CPU 替换为定制芯片有助于大幅降低对应的成本。另一方面，相比传统存储服务器，定制芯片代劳了巨大的数据流量处理，从而使存储服务器 CPU 可以专注元数据层面工作，转而使用更廉价的 CPU。

  * __Ethernet SSD 替换 PCIe__。如果对 EBOX 的任何访问都来远程的服务器，来自于 Ethernet，那么其 PCIe 可以被省去，整合进 Ethernet。除了简化 EBOX 体系结构，将 PCIe 替代为 Ethernet 还可受益于近年来 Ethernet 在带宽和成本上的飞速进步。

  * __存储服务器和数据盘的 Disaggregation__。Disaggregation 设计常常有助于提高资源效率， 独立横向扩展。想象一个基于 HDD 的集群，如果数据持续变冷，则可以在保持 HDD EBOX 在线的情况下，逐步关闭配套的存储服务器，节省能耗开销。而传统服务器却无法解耦存储服务器和硬盘，单独关闭服务器而保持硬盘在线。

  * __EBOX 间的 Direct Access__。EBOX 可以和另一个（些）EBOX 直接通信，搬迁数据。数据传输过程中不需要存储服务器参与，除了启动阶段。这非常有利于实现存储系统常见的数据修复和数据迁移功能，类似于 EBOX 层面的 RDMA，存储服务器自身的带宽和 CPU 得以节省。

另一方面，EBOX 也有一系列额外成本和风险：

  * __EBOX 没有成熟方案，没有供应商和生态__。不成熟的制造意味着早期的高成本。虽然公有云可以提供大批量的订单，供应商需要思考为何参与。当然，低起点也意味着股票的高增长率、高投资回报。

  * __全联接提高数据可靠性基于假设__：EBOX 拥有比存储服务器高得多的可靠性。这是有理由的，完整的存储服务器比 EBOX 复杂得多，需要频繁升级软件、操作系统、重启。而 EBOX 足够简单，能够标准化操作。已知单独硬盘的可靠性往往远高于整台服务器。此外，双控需要额外的硬件成本。

  * __用 Ethernet 替代 PCIe 基于假设__：Ethernet 拥有比 PCIe 更低的成本，更高的带宽，并且未来增长更快。这不一定正确，PCIe 是为单服务器内传输特化的，特化很可能优于需要兼顾远近传输的 Ethernet 。更重要的是，额外的 Ethernet 建设成本。

  * __额外 Ethernet 建设成本__。存储服务器和硬盘被解耦，之间需要新的 Ethernet 联接，新的交换机、新的端口。但有办法规避，例如，将 EBOX 联接到已有网络，而不需构建新网。用 DSR 返回客户数据，存储服务器与 EBOX 只有元数据交流，甚至不需扩容带宽。

  * __研发成本，数据迁移成本__。基于全新硬件架构研发新系统并不容易，但有办法规避。例如，设计软硬件隔离层并力求只替换低层组件，或利用大规模用户摊薄成本。类似地，数据迁移成本可以摊薄，或设计价格策略引导用户自行迁移。

新技术的哪些优势有巨大潜力，哪些优势不如看上去重要，优势劣势如何映射到成本收益并系统地比较，需要更进一步的分析。

### 存储系统的成本收益

首先，可以定性地分析 EBOX 是否适用于现今的不同存储场景：

  * __高容量、低吞吐__：通常为 HDD 存储系统。适用。EBOX 带来诸多有利特性：超长纠删码降低冷数据的副本开销，将 CPU 替换为专用芯片以降低成本，关闭部分存储服务器以省电，EBOX 直接访问有利数据迁移平衡。

  * __低容量、高吞吐__：通常为 SSD 存储系统。适用。EBOX 除带来上述的有利特性外，数据链路省去 CPU，DSR 可提升吞吐量，降低延迟。

  * __高容量、高吞吐__：可以合并到“低容量、高吞吐”。

  * __低容量、低吞吐__：此场景不现实，并可以合并到“高容量、低吞吐”。

针对存储系统最昂贵的属性——延迟（_[存储系统中的硬件](.)_ 章节），EBOX 能否提供优势：

  * __有利因素__：将 CPU 替换为专用芯片，并且省去操作系统等复杂软件。虽然专用芯片的频率往往低于 CPU（能耗和稳定性约束），但延迟得益于更高并行处理能力，降低等待队列长度。

  * __不利因素__：将存储服务器与硬盘解耦，原本的 PCIe 联接被替换为 Ethernet。PCIe 的延迟在 100ns 级别，而 Ethernet 的延迟在 10us 级别，况且网络包途经额外的交换机。

接下来，针对存储系统的主要指标——容量、带宽、能耗、成本，可以基于 _[存储系统中的硬件](.)_ 章节的成本数据表进行分析。__下面展示 SSD 存储__：

  * __参数设置__：为比较 EBOX ，根据前文提到的潜在优势和额外成本，设定相应的参数。“全联接”带来的可靠性提升将纠删码冗余度从 1.3x 降低到 1.1x 。PCIe 被替换为 Ethernet。CPU 成本因替换为专用芯片而降低。分离的 EBOX 带来额外网卡开销。因早期不成熟，供应商生产成本有额外惩罚，惩罚每年递减 5% 。第 5 年因成熟标准化，没有惩罚，而成本下降 5%。

![EBOX cost parameters](/images/vision-ebox-cost-parameters.png "EBOX cost parameters")

  * 其它参数复用 _[存储系统中的硬件](.)_ 章节。__单位全文统一，容量 GB，带宽 GBps，货币 \$__。

![Storage cost parameters](/images/vision-storage-cost-parameters.png "Storage cost parameters")

  * __购买和能耗成本表__：下表显示采用 EBOX 后，第 0 年 1GB SSD 存储对应的各组件的购买成本和能耗成本。与 _[存储系统中的硬件](.)_ 章节中 SSD 存储成本比较，可以看到成本相仿。CPU 的购买和能耗开销下降，SSD 购买成本下降，但节省的开支被供应商制造惩罚抵消。

![EBOX SSD storage cost](/images/vision-ebox-cost-ssd.png "EBOX SSD storage cost")

  * __购买和能耗成本比例__：下表显示采用 EBOX 后，第 0 年的购买和能耗成本中，各组分的比例。与 _[存储系统中的硬件](.)_ 章节对比，可以看到能耗占购买成本比例下降。各组件大致比例相仿，但 CPU 的购买和能耗占比下降，对应 SSD 占比上升，DRAM 占比也上升。

![EBOX SSD Storage cost ratio](/images/vision-ebox-cost-ssd-ratio.png "EBOX SSD Storage cost ratio")

下面考虑 __未来 5 年__ 硬件的性能成本变化，以 _[存储系统中的硬件](.)_ 章节的存储成本计算作为基准，比较 EBOX 的收益。__首先展示 SSD 存储__。下图分别展示不同特性对成本的影响，纵轴是节省成本的比例（越高越好）。

  * 各图例从左到右依次叠加更多特性，如 "++++ NIC cost extra" 表示开启了纠删码冗余度下降、PCIe 成本下降、CPU 成本下降、额外网卡成本，共 4 个特性（4 个 + 号）。

  * __主要成本节省来自纠删码和 CPU__。纠删码带来了 SSD 购买成本的下降，SSD 占总体成本较高，因而收益显著。另一方面，SSD 存储的高带宽带来高 CPU 成本，因而 CPU 上的改进效果明显。

  * __PCIe 替换为 Ethernet 的收益为负，但不显著__。Ethernet 成本仍然比 PCIe 高。PCIe 原本所占成本比例极小。额外网卡开销相对较小，这也是因为 Ethernet 开销原本所占成本比例相对较小。这也说明，Disaggregated 架构并不会因网络离散而引入过高的成本。

  * __总体成本节省在 20% 左右__，这需要 5 年后供应商制造成熟。5 年 20%，即年均 4% 的成本下降，可支撑多少股价上涨？结合 _[理解股价](.)_ 章节的计算，假设公司营收不变，初始利润率为 20%，则可支撑首年大致 __16% 左右的股价增长__。

  * __总成本节省比例逐年略微下降__，如果除去制造惩罚的影响，尽管下降非常轻微。主要原因是能耗占购买成本比例的上升，而纠删码冗余度下降不算进能耗节省。不能逐年下降的成本组分会逐渐增加占比，从而拖低节总节省，如 SSD 能耗、DRAM 购买成本。

![EBOX SSD Storage cost compare 5 years](/images/vision-ebox-cost-ssd-compare.png "EBOX SSD Storage cost compare 5 years")

__HDD 的版本__ 类似，略过相似的图表。下面展示其未来 5 年的成本变化，以 _[存储系统中的硬件](.)_ 章节的 HDD 存储计算表作为基准，进行比较。

  * __主要成本节省来自纠删码__。原因类似 SSD 存储，即使 HDD 廉价，其成本也占存储的显著比例。而 CPU 改进带来的节省不显著，因为其原本占比较小。类似地，PCIe 替换为 Ethernet 的收益不显著，额外网卡也开销不显著。

  * __PCIe 替换为 Ethernet 的收益不显著__。趋势与 SSD 存储类似。但在 HDD 存储中，PCIe 或 Ethernet 的开销更大，因为 SSD 带来的高带宽。

  * __采用 EBOX 后，各组件成本的比例变化不大__。值得注意的是，DRAM 的购买与能耗是 HDD 存储的显著成本，但 EBOX 并未对此提供改进。

  * __总体成本节省在 10% 左右__，这需要 5 年后供应商制造成熟。相比 SSD 存储，节省比例较低，原因在于 HDD 存储中 CPU 成本并不高。按相同方式换算，5 年 10% 对应年均 2% 的成本下降。可支撑首年大致 8% 左右的股价增长。

![EBOX HDD Storage cost compare 5 years](/images/vision-ebox-cost-hdd-compare.png "EBOX HDD Storage cost compare 5 years")

可以看到，对于 SSD 存储，EBOX 有不错的收益。最有效的改进来自于纠删码和 CPU。意料之外的是，Ethernet 替换 PCIe 并没有太多收益，EBOX 分离引入的额外网络成本也不高。

### 研发成本的摊薄

继续前文，下一个问题是，EBOX 需要多少研发成本？EBOX 需要销售多少 PB 的存储以摊薄其成本？首先，可以合理推测 __成本相关的参数__：

  * 单位 GB 的存储成本数据来自 _[存储系统中的硬件](.)_ 章节的计算。这个成本是较低的，参考此章节的公有云存储的售价对比，下面按 10x 设置销售价格（markup）。

  * 从不同国家雇佣开发者的大致月薪数据来自互联网，以美国最高。可以假设开发 EBOX 同时维持原产品运转需要 200 人。相比月薪，公司需付出 2x 的雇佣成本。

![Storage dev cost parameter](/images/vision-dev-cost-parameters.png "Storage dev cost parameter")

这个规模的研发团队需要销售多少 PB 的存储以 __足够支付自己的月薪__ 呢？这可以被计算出来，见下图：

  * 以最贵的美国雇佣为例，__销售 HDD 存储需要达到约 1.8K PB__。而销售 SSD 存储利润较好，只需约 1/10x PB 即可支付薪水。

  * 如果从其它国家雇佣，有希望立即将 __所需销售的存储 PB 削减一半__，而另一半将变为利润。可见跨国雇佣有巨大的潜在收益。

![Storage dev sell PB to pay salary](/images/vision-dev-cost-salary-sell-pb.png "Storage dev sell PB to pay salary")

一个有趣的发现是，996 可以显著提升员工产出，从而削减员工数量，减少开支。见下图。当然，后文分析仍然是以正常工作时间制为准（周 40 小时）。

  * 一周 40 小时工作制下，__实际开发产出只有 40 小时的 31%__。这是因为开发工作的固定成本很高，例如已有 20% 时间用于开会，20% 时间用于运维和故障修复，20% 时间用于学习。此外，公共假日和带薪年假也占用约 9% 时间。

  * 相对于 40 小时工作制，__996 工作制可迅速将产出提高到 2.6 倍__，对应每周工作 60 小时。这是因为额外加入的工作时间不改变固定成本，直接转变为开发产出，边际效应显著。这里没有考虑长期 996 造成的疲乏。

  * 更加激进的是 早7-晚10-7天 工作制，可将产出进一步提高到 5 倍，对应每周工作 90 小时。这允许资金紧张的 Startup 显著压缩成本，等待后期规模的回报。注意，__每周工作 90 小时是 SpaceX 的常见水准__ [[63]](.)。

![Storage dev efficiency](/images/vision-ebox-dev-efficiency.png "Storage dev efficiency")

随着销售的存储规模增长，研发成本如何摊薄呢？下图展示随销售存储 PB 增长，__营收的变化__。单位是 \$M，周期是年度。

  * 随着销售存储 PB 增长，营收增长呈 __线性__，一分钱一分货。同样的销售存储 PB，SSD 的营收约为 HDD 的 __十倍__。

  * 如果营收过 __\$1B__，HDD 需销售约 __20K PB__ 存储，SSD 需销售约 __2K PB__ 存储。如果营收过 \$10B，HDD 需销售约 200K PB 存储，SSD 需销售约 20K PB 存储。

  * 对于全球约 \$160B 的云存储市场大小 [[46]](.)，可以推测，__\$1B__ 对应小型公有云水准，约 __1%__ 全球份额。\$10B 对应顶级公有云水准，约 10% 全球份额。

![Storage revenue yearly by sold PB](/images/vision-dev-cost-storage-revenue-pb.png "Storage revenue yearly by sold PB")

下面是关键，__净利润率__ 如何随着销售的存储 PB 变化？净利润率由营收扣除存储成本和研发成本计算。下面的计算以人力成本最贵的美国雇佣为例。下图中，可以看到剧烈的规模效应。

  * __何时开始盈利__。HDD 存储销售超过 2K PB 的临界点时开始盈利，SSD 则只需超过 200PB。尽管销售规模较小时，受研发成本拖累，亏损严重。HDD 亏损甚至能到约 -700%，SSD 能到约 -60% 。

  * __超过临界点后，不仅营收上涨，净利润率也迅速上涨__，这是极好的规模效应。普通业务往往在营收上涨的同时，净利润率下降。

  * __净利润率迅速上涨到 90%__。这是极为赚钱的业务水准。通常的经验是，制造业的净利润率在 5% 左右，尖端制造能到 15%~20%，优秀的软件业务可以达到 30% [[47]](.)。

  * __净利润率达到 80%~90% 只需约 \$1B 营收__。结合上一段，__\$1B__ 营收对应约 __1%__ 全球份额，小型公有云供应商。这意味着超高利润的规模效应，实际上并不要求很大的规模。而 10% 全球份额的顶级公有云供应商，可以稳赚巨大营收和极高净利润率。

  * __净利润率对成本不敏感__。下图额外展示了研发成本 X2、X4 后的净利润率。可以看到，具有一定规模后，翻倍的研发成本几乎不影响净利润率，后者仍然保持在 80%~90% 。业务非常健壮。

![Storage net income % by sold PB](/images/vision-dev-cost-net-income-ratio-pb.png "Storage net income % by sold PB")

可以看到，对于具有一定规模的存储业务，负担 EBOX 的研发成本是足够的，甚至有余。当然，本文的分析相比实际作了许多简化，力求简单清晰，表明思路。

### 供应商和市场

Strategic 思考意味着不仅思考存储方自身，也思考对方一侧，这里是销售 EBOX 的供应商。成功的云存储策略需要供应商配合，尤其是新型硬件。假设供应商原本销售硬盘给公有云，本节的问题是，从供应商角度，供应商是否应该推出 EBOX 新产品销售？

作为思考的基础，可以借用 __Issue Tree Framework__（见前文 _[分析方法](.)_ 章节），将问题分解：

  * 市场需求
    * 公有云需求
    * 竞争性产品

  * 产品可行性
    * 技术可行性
    * 制造可行性

  * 财务能力
    * 潜在营收
    * 研发成本

  * 风险
    * 客户采用
    * 供应链

首先看 __市场需求__ 方面：

  * 从前文分析来看，可以和公有云联合生产设计，从而确保需求。公有云方有意通过 EBOX 获取成本优势，寻找供应商。

  * 如果抢先推出产品，则有利于超过竞争对手，扩大现有市场占有率。而公有云更可能大批量采购。

  * 从售卖硬盘到售卖 EBOX 整机，扩大了销售范围，有利于提高营收，以及附加利润。

然后看 __产品可行性__ 方面：

  * 技术可行性方面，EBOX 类似简化定制的服务器，并不是全新技术，关键在有整合和控制成本，具有可行性。

  * 制造方面，前期因不成熟引入额外成本，但可以通过售价转嫁。前文的计算可以看出，公有云方能够接受此价格的制造惩罚。

接下来看 __财务能力__ 方面：

  * 前提提到云存储市场规模 \$160B ，数据表中硬盘约占 80% 成本，假设供应商现已占有 10% 市场份额。则供应商的 __当前营收约为 \$13B__。

  * 抢先推出 EBOX 产品可扩大市场占有率。假设市场占有率从 10% 增长到到 20%，则 __营收增长为约 \$26B__。

  * 从售卖硬盘到售卖 EBOX，扩大了销售范围，进一步提高营收。从前文数据表中估算，营收提高在 13% 左右，__营收进一步增长为约 \$29B__。

  * 相比售卖硬盘，EBOX 更复杂，可提供更高的附加利润。假设净利润率从原先的 10% 提搞到 12%。供应商的 __净利润从约 \$1.3B 增长为约 \$3.5B__。

  * 从 \$1.3B 到 \$3.5B，净利润增长为 270%。假如该增长发生在 10 年间，结合 _[理解股价](.)_ 章节的计算，可支持 __平均每年 10% 的股价增长__。收益良好。

  * 研发成本方面，公有云带来的大批量采购能够摊薄成本。并且，EBOX 不是全新技术，其成本大头的硬盘是供应商经验成熟的领域。即使 200 人的研发成本，利用前文数据表计算，也 __只占 \$13B 的不到 1%__ 。

最后是 __风险__ 方面：

  * 公有云是否愿意持续大批量采购 EBOX 产品是一大风险。从供应商角度，最好避免绑定大客户，同时也向私有云销售 EBOX，并根据实际营收逐步提高投入。

  * EBOX 相比单纯售卖硬盘多出许多组件，其中 CPU 占第二大硬件成本。可从较通用的如 ARM CPU 开始推出产品，在之后几代才考虑更定制化的 DPU 或专用芯片。可以在“允许定制”之名下，把软件成本转嫁给公有云客户。

通过以上浅显的分析，可以看出从供应商角度也能从推出 EBOX 产品中获利，甚至收益良好。

## 总结

全文完。本文在（云）存储的技术和行业背景下，依次讲解 __方法论__，__理解股价__，__市场__，__市场的分析__，__硬件__，__EBOX 案例分析__。方法论部分搭建 Vision 与 Strategy 的思考框架。股价部分分析其原理，理解公司的目标，并映射到团队。市场部分纵览存储系统的竞争格局，并分析市场的关键特性、颠覆式创新、以及价值。硬件部分建模其能力和发展速度，深入观察其要点。最后，案例分析部分用 EBOX 实例实践本文的分析方法，有许多有趣的结论。

## 引用

[1] Hard Drive Performance Over the Years : https://goughlui.com/the-hard-disk-corner/hard-drive-performance-over-the-years/

[2] Disk Prices: https://diskprices.com/

[3] Enterprise SSDs cost ten times more than nearline disk drives : https://blocksandfiles.com/2020/08/24/10x-enterprise-ssd-price-premium-over-nearline-disk-drives/

[4] Next-generation Information Technology Systems for Fast Detectors in Electron Microscopy : https://arxiv.org/ftp/arxiv/papers/2003/2003.11332.pdf

[5] SSDs Have Become Ridiculously Fast, Except in the Cloud : https://databasearchitects.blogspot.com/2024/02/ssds-have-become-ridiculously-fast.html

[6] A Modern Primer on Processing in Memory : https://arxiv.org/pdf/2012.03112

[7] Wikipedia DDR SDRAM : https://en.wikipedia.org/wiki/DDR_SDRAM

[8] Trends in DRAM price per gigabyte : https://aiimpacts.org/trends-in-dram-price-per-gigabyte/

[9] Bandwidth and latency of DRAM and HBM : https://www.researchgate.net/figure/Bandwidth-and-latency-of-DRAM-and-HBM-and-the-impact-of-latency-on-application_fig2_329551516

[10] High-bandwidth memory (HBM) options for demanding compute : https://www.embedded.com/high-bandwidth-memory-hbm-options-for-demanding-compute/

[11] Wikipedia High Bandwidth Memory : https://en.wikipedia.org/wiki/High_Bandwidth_Memory

[12] More Than Anything Else, Cost Per Bit Drives Datacenter Ethernet : https://www.nextplatform.com/2021/08/30/more-than-anything-else-cost-per-bit-drives-datacenter-ethernet/

[13] Wikipedia PCI Express : https://en.wikipedia.org/wiki/PCI_Express

[14] Quora Motherboard price changed over time : https://www.quora.com/How-has-the-cost-of-CPUs-on-motherboards-changed-over-time-Is-there-a-significant-difference-in-their-usage

[15] Quora What is the latency of a PCIe connection : https://www.quora.com/What-is-the-latency-of-a-PCIe-connection

[16] Wikipedia NVLink : https://en.wikipedia.org/wiki/NVLink

[17] Doubling of Data Center Ethernet Switch Bandwidth Every Two Years : https://www.prnewswire.com/news-releases/doubling-of-data-center-ethernet-switch-bandwidth-every-two-years-continued-in-2022-reports-crehan-research-301793556.html

[18] Timed Linux Kernel Compilation: https://openbenchmarking.org/test/pts/build-linux-kernel-1.16.0

[19] 2019 recent trends in Geekbench score per CPU price : https://aiimpacts.org/2019-recent-trends-in-geekbench-score-per-cpu-price/

[20] NVIDIA A100 GPU Benchmarks for Deep Learning : https://lambdalabs.com/blog/nvidia-a100-gpu-deep-learning-benchmarks-and-architectural-overview?srsltid=AfmBOoqh1Spj-txULhl0GTfLiqVJ2A_G-Sv3mCNiPC5UC2fnpuWI9o9s

[21] Trends in GPU Price-Performance : https://epoch.ai/blog/trends-in-gpu-price-performance

[22] Scality claims disk drives can use less electricity than high-density SSDs : https://blocksandfiles.com/2023/08/08/scality-disk-drives-ssds-electricity/

[23] Wikipedia Solid-state drive : https://en.wikipedia.org/wiki/Solid-state_drive

[24] GreenDIMM: OS-assisted DRAM Power Management for DRAM with a Sub-array Granularity Power-Down State : https://dl.acm.org/doi/fullHtml/10.1145/3466752.3480089

[24] ChatGPT Datacenter Networking Device Consuming Power Watt: https://chatgpt.com/share/676e8a82-bbf4-800f-8859-b34f22f95fee

[25] Gigabyte Server "Power Consumption" Roadmap Points To 600W CPUs & 700W GPUs By 2025 : https://wccftech.com/gigabyte-server-power-consumption-roadmap-points-600w-cpus-700w-gpus-by-2025/

[26] CPU, GPU and MIC Hardware Characteristics over Time : https://www.karlrupp.net/2013/06/cpu-gpu-and-mic-hardware-characteristics-over-time/

[27] Understanding the Energy Consumption of Dynamic Random Access Memories : https://www.seas.upenn.edu/~leebcc/teachdir/ece299_fall10/Vogelsang10_dram.pdf

[28] AMD Dives Deep On High Bandwidth Memory - What Will HBM Bring AMD : https://www.anandtech.com/show/9266/amd-hbm-deep-dive/4

[29] Reddit HBM cost and CPU memory cost comparison : https://www.reddit.com/r/chipdesign/comments/166thgi/hbm_cost_and_cpu_memory_cost_comparison/

[30] Compute Express Link (CXL): All you need to know : https://www.rambus.com/blogs/compute-express-link/

[31] Instructions/clock-cycle for each core of Intel Xeon CPUs compared with FLOPs/clock-cycle of Nvidia high-performance GPUs : https://www.researchgate.net/figure/nstructions-clock-cycle-for-each-core-of-Intel-Xeon-CPUs-compared-with-FLOPs-clock-cycle_fig6_319072296

[32] Google Data Centers Efficiency : https://www.google.com/about/datacenters/efficiency/

[33] Global PUEs — are they going anywhere? : https://journal.uptimeinstitute.com/global-pues-are-they-going-anywhere/

[34] Component-wise energy consumption of a server : https://www.researchgate.net/figure/Component-wise-energy-consumption-of-a-server-23-24_fig5_355862079

[35] Azure Blob Storage pricing : https://azure.microsoft.com/en-us/pricing/details/storage/blobs/

[36] Seagate Plans To HAMR WD's MAMR; 20TB HDDs With Lasers Inbound : https://www.tomshardware.com/news/seagate-wd-hamr-mamr-20tb,35821.html

[37] Using SSD data placement to lessen SSD write amplification : https://blocksandfiles.com/2023/08/14/using-ssd-data-placement-to-lessen-write-amplification/

[38] Big Data: The 3 Vs explained : https://www.bigdataldn.com/en-gb/blog/data-engineering-platforms-architecture/big-data-the-3-vs-explained.html

[39] Intel Data Direct I/O Technology : https://www.intel.com/content/www/us/en/io/data-direct-i-o-technology.html

[40] Declarative IO - Cluster Storage Systems Need Declarative I/O Interfaces : https://youtube.com/watch?v=TGWKZnJeNmA&si=AC6gaUtfnPjIt_vB

[41] CPU open IPC_benchmark : https://openbenchmarking.org/test/pts/ipc-benchmark&eval=a29a620e89e1cb4ff15d5d31d24eaae1cc059b0e

[42] zStorage 分布式存储技术：总结2023，展望2024 : https://mp.weixin.qq.com/s/uXH8rkeJL_JMbKT3H9ZuCQ

[43] Vast Data white paper : https://www.vastdata.com/whitepaper/#TheDisaggregatedSharedEverythingArchitecture

[44] NVMe Over Fabrics Architectures for Disaggregated Storage : https://www.snia.org/sites/default/files/ESF/Security-of-Data-on-NVMe-over-Fabrics-Final.pdf#page=25

[45] Network Attached Storage and NFS-eSSD : https://msstconference.org/MSST-history/2023/FlynnPresentation2.pdf#page=7

[46] Fortune Cloud Storage Market Size, Share & Industry Analysis : https://www.fortunebusinessinsights.com/cloud-storage-market-102773

[47] Margins by Sector (US) : https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/margin.html

[48] MSFT (Microsoft) Preferred Stock : https://www.gurufocus.com/term/preferred-stock/MSFT

[49] Stock Analysis MSFT stock analysis : https://stockanalysis.com/stocks/msft/statistics/

[50] Trading Economics United States 30 Year Bond Yield : https://tradingeconomics.com/united-states/3-month-bill-yield

[51] Investing.com Microsoft corp historical dividends : https://in.investing.com/equities/microsoft-corp-dividends

[52] Jacob 从3年后的EPS看，现在的微软是否值得介入 : https://mp.weixin.qq.com/s/IU03qeV53bcK75U-sfRMGg

[53] Wikipedia Beta系数 : https://zh.wikipedia.org/wiki/Beta%E7%B3%BB%E6%95%B0

[54] Equity Risk Premium (ERP) : https://www.wallstreetprep.com/knowledge/equity-risk-premium/

[55] Capital Asset Pricing Model (CAPM) : https://www.wallstreetprep.com/knowledge/capm-capital-asset-pricing-model/

[56] Investing.com S&P 500 : https://in.investing.com/indices/us-spx-500

[57] TradingView US companies with the highest dividend yields : https://www.tradingview.com/markets/stocks-usa/market-movers-high-dividend/

[58] Microsoft Cloud strength fuels third quarter results : https://news.microsoft.com/2024/04/25/microsoft-cloud-strength-fuels-third-quarter-results-3/

[59] Gartner Magic Quadrant for Primary Storage Platforms 2024 : https://www.purestorage.com/resources/gartner-magic-quadrant-primary-storage.html

[60] Fortune Data Storage Market Size, Share & Industry Analysis : https://www.fortunebusinessinsights.com/data-storage-market-102991

[61] Key Insights for Gartner Magic Quadrant 2024 for Strategic Cloud Platforms : https://alnafitha.com/blog/key-insights-from-gartner-magic-quadrant-2024-for-cloud/

[62] Gartner Cloud Integrated IaaS and PaaS Solution Scorecard Comparison 2021 : https://clouddecisions.gartner.com/a/scorecard/#/iaas-alibaba-vs-aws-vs-google-vs-ibm-vs-azure-vs-oracle

[63] Quora What is it like to work at SpaceX? : https://www.quora.com/What-is-it-like-to-work-at-SpaceX

[64] Gartner Critical Capabilities for Primary Storage 2023 : https://mp.weixin.qq.com/s/O5j1nNt3cqQT6RmG7wEy_g

[65] RackTop The Buyer's Guide to Cyberstorage Features : https://www.racktopsystems.com/the-buyers-guide-to-cyberstorage-features/

[66] Gartner Top Trends in Enterprise Data Storage 2023 : https://www.purestorage.com/resources/type-a/gartner-top-trends-enterprise-data-storage-2023.html

[67] 6家存储系统公司的客户反馈 : https://mp.weixin.qq.com/s/Ri6pdeJ5-82pHBaGz-wlKw

[68] 湖南省省级电子政务外网统一云平台资源补充项目 : https://mp.weixin.qq.com/s/S4-2XbFDp6qB-8S01qSEEw

[69] 西瓜哥 Gartner Hype Cycle for Storage Technologies 2024 : https://mp.weixin.qq.com/s/Ct5bq_QsF7Tu_r6bvqUSFg

[70] SmartX Hype Cycle for Storage and Data Protection Technologies, 2022 : https://www.smartx.com/blog/2022/08/gartner-hype-cycle-storage/

[71] 深度数据云 Gartner Hype Cycle for Data Management, 2023 : https://zhuanlan.zhihu.com/p/656920047

[72] MarketResearchFuture Data Backup And Recovery Market Overview : https://www.marketresearchfuture.com/reports/data-backup-recovery-market-29073

[73] GrandViewResearch Enterprise Information Archiving Market Size : https://www.grandviewresearch.com/industry-analysis/enterprise-information-archiving-market-report

[74] Gartner Magic Quadrant for Enterprise Backup and Recovery Software Solutions : https://www.zen.com.my/wp-content/uploads/2024/01/Backup-Vendor-Magic-Quadrant-2023-1-1.pdf

[75] Veeam, Rubrik Lead in Enterprise Backup/Recovery Report : https://virtualizationreview.com/articles/2024/08/09/veeam-rubrik-lead-in-enterprise-backup-recovery-market-report.aspx

[76] Disaster Recovery with Cloud Recovery Assurance : https://www.appranix.com/resources/blogs/2023/07/disaster-recovery-with-cloud-recovery-assurance.html

[77] Gartner Magic Quadrant for File and Object Storage Platforms 2024 : https://www.purestorage.com/resources/gartner-magic-quadrant-file-object-storage-platforms.html

[78] VMR Global Distributed File Systems and Object Storage Solutions Market By Type : https://www.verifiedmarketreports.com/product/distributed-file-systems-and-object-storage-solutions-market/

[79] MarketResearchFuture Global Cloud Object Storage Market Size : https://www.marketresearchfuture.com/reports/cloud-object-storage-market-4202

[80] Nasui Types & Volume of Files in the Enterprise : https://youtu.be/8FHihZvyFFM?si=KbiVDWqHfStLMiZU&t=330

[81] VMR Global Block Storage Software Market By Type : https://www.verifiedmarketreports.com/product/block-storage-software-market/

[82] GrandViewResearch Database Management System Market Size : https://www.grandviewresearch.com/industry-analysis/database-management-systems-dbms-market

[83] GrandViewResearch Cloud Database And DBaaS Market Size : https://www.grandviewresearch.com/industry-analysis/cloud-database-dbaas-market-report

[84] Gartner Magic Quadrant for Cloud Database Management Systems 2024 : https://www.databricks.com/resources/analyst-paper/databricks-named-leader-by-gartner

[85] MarketResearchFuture Enterprise Flash Storage Market Overview : https://www.marketresearchfuture.com/reports/enterprise-flash-storage-market-31294

[86] MarketResearchFuture Tape Storage Market Overview : https://www.marketresearchfuture.com/reports/tape-storage-market-33976

[87] MarketResearchFuture Global Hard Disk Market Overview : https://www.marketresearchfuture.com/reports/hard-disk-market-8306

[88] MBA智库 波特五力分析模型 : https://wiki.mbalib.com/wiki/%E6%B3%A2%E7%89%B9%E4%BA%94%E5%8A%9B%E5%88%86%E6%9E%90%E6%A8%A1%E5%9E%8B

[89] Zartbot DPU及网络处理器的历史 : https://mp.weixin.qq.com/s/BZOvVrg3GtTurMe2Q6ZIcg

[90] Andy730 颠覆性创新？存储界已有所耳闻 : https://mp.weixin.qq.com/s/NFQYEwrYCwKvTjpQdLkcQA

[91] LinkedIn Course Critical Thinking by Mike Figliuolo : https://www.linkedin.com/learning/critical-thinking

[92] Profitability Framework and Profit Trees The Complete Guide : https://www.craftingcases.com/profitability-tree-guide/

[93] LinkedIn Course Strategic Thinking by Dorie Clark : https://www.linkedin.com/learning/strategic-thinking

[94] LinkedIn Course Business Acumen by Mike Figliuolo : https://www.linkedin.com/learning/developing-business-acumen

[95] GetAbstract The Unspoken Truths for Career Success : https://www.getabstract.com/en/summary/the-unspoken-truths-for-career-success/46904

[96] LinkedIn Course Management Foundation by Kevin Eikenberry : https://www.linkedin.com/learning/management-foundations-2019
