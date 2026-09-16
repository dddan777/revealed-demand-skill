---
name: revealed-demand
description: Validate demand for an idea, MVP, paid offer, or existing product using observable commitment and transaction evidence. Use when a builder or creator needs to identify the smallest sellable outcome, test pricing, interpret funnel or sales data, or choose one next market experiment without mistaking attention for demand.
---

# Revealed Demand

Turn a vague demand claim into an evidence ledger, a bounded verdict, and one decision-producing experiment.

Respond in the user's language. Keep facts, user-reported claims, calculations, assumptions, and inferences visibly separate. Observable behavior is evidence under constraints; it is not direct access to a person's true preferences.

## Operating rules

- Diagnose the evidence before recommending growth tactics.
- Prefer denominators, time windows, cohorts, prices, refunds, repeat behavior, and channel provenance over adjectives such as popular or validated.
- Treat likes, saves, comments, survey answers, waitlists, deposits, purchases, retained usage, referrals, and repeat purchases as different signals.
- Do not claim product-market fit, optimal pricing, causality, or repeatable demand from a single unqualified result.
- Do not invent missing metrics. Mark user-provided but unverified numbers as reported.
- Recommend one primary experiment at a time unless the user explicitly asks for a factorial design.
- Never recommend fake scarcity, fabricated testimonials, hidden charges, misleading anchors, or unequal price treatment without a legitimate and disclosed basis.

## Select the evidence stage

Classify the case before making a verdict:

| Stage | Available evidence | Default task |
|---|---|---|
| Idea | No usable offer or transaction evidence | Make the claim testable and design a small commitment experiment |
| MVP | A usable product or offer with little or no paid behavior | Find the smallest paid outcome and test the offer, price, and path |
| Sales | Paid transactions, refunds, activation, repeat use, or cohort data | Audit strength, friction, economics, and repeatability |

When the information is insufficient, ask only for the missing facts that could change the next decision. Do not run a long intake interview by default.

## Apply the VOTE protocol

### V — Value Moment

State one falsifiable job:

Who encounters what concrete situation, wants what result by when, and uses what alternative today?

Reject broad personas without a decision moment. Distinguish the user's stated target from people who have actually taken action.

### O — Observable Commitment

Build an evidence ledger with:

- signal;
- count and denominator;
- time window and channel;
- price or other user cost;
- source: observed, reported, or inferred;
- confounds;
- what the signal supports and does not support.

Judge each signal on user cost, specificity, reversibility, independence, and recurrence. A purchase is usually stronger than a like, but discounted, refunded, bundled, friend-network, or incentivized purchases need qualification.

Read [evidence-and-experiments.md](references/evidence-and-experiments.md) when signal quality, pricing, funnel interpretation, or experiment design is central.

### T — Transaction Unit

Define the smallest paid result the user can understand before purchase and experience soon after purchase. Specify:

- buyer and triggering situation;
- promised result;
- included format and delivery time;
- exclusions and handoff boundary;
- proof or preview;
- price hypothesis and refund or cancellation terms;
- delivery cost and capacity constraint.

Cut scope until the result is concrete. Do not optimize a feature list.

### E — Experiment

Design the smallest ethical test that could change the decision:

- hypothesis and strongest rival explanation;
- one target segment and one channel;
- one transaction unit and one call to action;
- price cells or other single variable;
- assignment method and observation window;
- primary metric, guardrails, and data fields;
- pass, revise, and stop thresholds set before launch;
- action for each outcome.

Use deposits, paid pilots, pre-orders, or direct sales only when the delivery promise and refund terms are clear. For sparse traffic, prefer a small manually delivered paid pilot over an underpowered multivariate test.

## Make a bounded verdict

Use one of these evidence states:

- Not testable yet
- Demand unproven
- Problem evidence
- Commitment evidence
- Transaction evidence
- Repeatable demand evidence

The verdict must name the scope: segment, offer, price, channel, and time window. Then choose one current action:

- Define — the claim is not testable yet
- Test — collect a higher-cost signal
- Repackage — the result or transaction unit is unclear
- Reprice — price friction is plausible and separable from offer friction
- Scale — evidence is repeatable enough for a controlled expansion
- Stop — the precommitted stopping rule was met

## Required output

Return the following sections in this order:

1. Verdict — one sentence with evidence state, scope, and confidence.
2. What is known — a compact fact, inference, and missing-evidence table.
3. VOTE card — value moment, strongest commitment, transaction unit, and testable claim.
4. Evidence ledger — signal quality and caveats.
5. Next experiment — one protocol with precommitted decision thresholds.
6. Decision branches — what to do on pass, ambiguous, and fail.
7. Next single action — one concrete task the user can complete now.

Use [output-contracts.md](references/output-contracts.md) when the user wants a reusable brief, structured template, or full diagnostic card.

Read [calibration-cases.md](references/calibration-cases.md) when testing the Skill, resolving a borderline verdict, or checking whether a conclusion exceeds its evidence.

## Quantitative helper

When the user supplies cohort counts, price cells, revenue, refunds, or delivery cost, use [analyze_experiment.py](scripts/analyze_experiment.py) to compute comparable funnel rates, Wilson intervals, and contribution metrics. Read [experiment-input.json](examples/experiment-input.json) for the input shape.

The helper summarizes evidence. It does not authorize a causal claim or choose a winner automatically.

## Stop conditions

Stop or downgrade the task when:

- no specific buyer, triggering situation, or promised result can be stated;
- counts lack a usable denominator or time window;
- only attention or stated-interest signals exist;
- the offer cannot currently deliver its promise;
- price, packaging, channel, and message changed together, making attribution impossible;
- the proposed test relies on deception or uncompensated risk transfer;
- the requested conclusion exceeds the observed cohort.

State the blocker, preserve what can still be inferred, and give the smallest action that would produce decision-relevant evidence.
