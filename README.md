# 真需求验证器 / Revealed Demand

一套面向 AI Builder、独立开发者与知识产品创作者的需求验证 Skill。它不把浏览、点赞或口头兴趣直接写成“市场验证”，而是把想法、MVP 或销售数据整理为可审计的行为证据，并设计下一轮最小付费实验。

An evidence-first Skill for AI builders, independent developers, and knowledge-product creators. It turns an idea, MVP, or sales history into an auditable demand judgment and one small paid experiment, without confusing attention with demand.

[中文说明](#中文说明) · [English](#english) · [最终视频逐字稿](video/final-video-script-zh.md)

## 中文说明

### 它解决什么

- 用户都说想要，上线后却没人买；
- 有浏览、收藏、私信，却不知道哪些信号真正接近付费；
- 产品做得太大，不知道最小可卖结果是什么；
- 定价靠感觉，无法区分价格摩擦、包装摩擦与渠道摩擦；
- 已经有订单，却不知道证据是否能跨价格、渠道或人群复制；
- 每轮同时改很多变量，最后仍然不知道销量为什么变化。

### 核心方法 VOTE

| 模块 | 要回答的问题 | 产出 |
|---|---|---|
| V — Value Moment | 谁在什么具体时刻急需什么结果？ | 可证伪的价值时刻 |
| O — Observable Commitment | 用户为这个结果付出了什么真实成本？ | 带分母、窗口与来源的证据账本 |
| T — Transaction Unit | 最小可以成交并交付的结果是什么？ | 最小可交易结果卡 |
| E — Experiment | 下一轮怎样用一个实验让市场投票？ | 预先写好阈值的实验协议 |

Skill 会把证据状态限制在六个层级：尚不可检验、需求未证实、问题证据、承诺证据、交易证据、可重复需求证据。结论始终绑定具体人群、产品、价格、渠道和时间窗口。

### 它不会做什么

- 不从点赞或问卷直接推算销量；
- 不在缺少分母和时间窗口时伪造转化率；
- 不给出未经实验支持的“最优价格”；
- 不把单次成功写成因果关系或产品市场匹配；
- 不建议虚假稀缺、伪造评价、隐藏收费或误导性价格锚点；
- 不一次输出几十条增长动作，而是选择一个最能产生新证据的动作。

### 安装

把仓库中的 revealed-demand 目录复制到你的 Skills 目录：

~~~bash
git clone https://github.com/dddan777/revealed-demand-skill.git
cp -R revealed-demand-skill/revealed-demand ~/.codex/skills/revealed-demand
~~~

也可以把 revealed-demand 目录安装到任何支持 SKILL.md 目录规范的 Agent 环境。

### 使用示例

~~~text
使用 $revealed-demand 分析这个产品：
我发了 3 篇小红书，合计 8,000 浏览，300 人访问网站，42 人注册，
3 人完成核心操作，0 人付费。我应该先做投流、改产品还是改价格？
~~~

~~~text
使用 $revealed-demand 审计我过去 90 天的销售数据。
请把事实、推断和缺失证据分开，给出一个价格实验，
并预先写清通过、模糊和失败时分别做什么。
~~~

### 固定输出

1. 有边界的证据结论；
2. 事实、推断与缺口表；
3. VOTE 诊断卡；
4. 行为证据账本；
5. 下一轮唯一实验；
6. 通过、模糊、失败三条决策分支；
7. 当前唯一动作。

### 定量分析脚本

仓库附带一个只使用 Python 标准库的实验汇总脚本。它计算漏斗率、退款后净转化率、Wilson 95% 区间、单位曝光收入和贡献利润，但不会自动宣布“赢家”。

~~~bash
python3 revealed-demand/scripts/analyze_experiment.py \
  revealed-demand/examples/experiment-input.json
~~~

输入格式示例见 [experiment-input.json](revealed-demand/examples/experiment-input.json)。计算结果只有在各组的人群、产品、渠道、时间和分配方式具有可比性时，才适合横向比较。

### 项目结构

~~~text
revealed-demand/
├── SKILL.md
├── agents/openai.yaml
├── examples/experiment-input.json
├── references/
│   ├── calibration-cases.md
│   ├── evidence-and-experiments.md
│   └── output-contracts.md
└── scripts/analyze_experiment.py

tests/test_analyze_experiment.py
video/final-video-script-zh.md
~~~

### 方法边界

行为是偏好、约束、信息、信任、时机和可选方案共同作用的结果。因此，“付款”通常比“点赞”强，但也要继续检查折扣、退款、熟人购买、捆绑、激励与渠道偏差。这个 Skill 的目标不是给需求盖章，而是让下一项决策拥有更贵、更清晰、可复核的证据。

## English

### What it solves

- People say they want the product, but nobody buys it.
- Views, saves, and messages exist, but their evidential strength is unclear.
- The product is too broad to expose a small, understandable paid outcome.
- Pricing is based on intuition, so price, packaging, and channel friction are confounded.
- Orders exist, but repeatability across price, audience, or channel is unknown.
- Multiple variables change in every launch, preventing useful learning.

### The VOTE method

| Module | Question | Output |
|---|---|---|
| V — Value Moment | Who needs what result in what concrete moment? | A falsifiable value moment |
| O — Observable Commitment | What real cost did the user accept? | An evidence ledger with denominators and provenance |
| T — Transaction Unit | What is the smallest paid result that can be delivered now? | A minimum transaction-unit card |
| E — Experiment | What single next test lets the market vote? | A precommitted experiment protocol |

The Skill uses six bounded evidence states: Not testable yet, Demand unproven, Problem evidence, Commitment evidence, Transaction evidence, and Repeatable demand evidence. Every conclusion is scoped to a segment, offer, price, channel, and time window.

### What it will not do

- Convert likes or survey answers directly into a sales forecast.
- Invent conversion rates when denominators or windows are missing.
- Claim an optimal price without comparable evidence.
- Turn one successful cohort into a causal or product-market-fit claim.
- Recommend fabricated scarcity, fake reviews, hidden charges, or misleading anchors.
- Produce a large growth checklist when one evidence-producing action is more useful.

### Install

Copy the revealed-demand directory into your Skills directory:

~~~bash
git clone https://github.com/dddan777/revealed-demand-skill.git
cp -R revealed-demand-skill/revealed-demand ~/.codex/skills/revealed-demand
~~~

The directory can also be installed in other agent environments that support the SKILL.md folder convention.

### Example prompts

~~~text
Use $revealed-demand to assess this product:
8,000 content views led to 300 site visits, 42 registrations,
3 completed core actions, and no purchases.
Should I acquire more traffic, change the product, or test pricing?
~~~

~~~text
Use $revealed-demand to audit my last 90 days of sales.
Separate facts, inferences, and missing evidence.
Design one price experiment with pass, ambiguous, and fail actions defined in advance.
~~~

### Required output

1. A scoped evidence verdict;
2. facts, inferences, and gaps;
3. a VOTE card;
4. an evidence ledger;
5. one next experiment;
6. pass, ambiguous, and fail branches;
7. one immediate action.

### Quantitative helper

The included standard-library Python helper calculates funnel rates, net retained conversion, Wilson 95% intervals, revenue per exposure, and contribution metrics. It does not select a winner automatically.

~~~bash
python3 revealed-demand/scripts/analyze_experiment.py \
  revealed-demand/examples/experiment-input.json
~~~

See [experiment-input.json](revealed-demand/examples/experiment-input.json) for the schema. Cross-cell comparison is meaningful only when the cohorts, offer, channel, timing, and assignment method are compatible.

### Method boundary

Behavior reflects preferences under constraints, information, trust, timing, and available alternatives. Payment is usually stronger evidence than a like, but discounts, refunds, warm relationships, bundles, incentives, and channel selection still matter. The Skill is designed to improve the next decision, not to stamp an idea as permanently validated.
