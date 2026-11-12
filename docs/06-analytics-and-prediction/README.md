# Analytics and prediction for revenue systems

This section covers the measurement and modeling methods a GTM system needs: funnels, cohorts, attribution, experiments, forecasting and predictive scores. The emphasis is on the failure modes that make GTM numbers wrong in practice, such as summed attribution, peeked experiments, leaked features and models that train on their own recommendations.

## Funnel analytics

**What it is.** A count of entities (leads, accounts, opportunities) reaching each stage, and the conversion and time between stages.

```text
stage_conversion(s -> s+1) = entities that reached s+1 / entities that reached s
time_in_stage              = exited_stage_at - entered_stage_at   (report median and p75, not mean)
```

**Why it matters.** Funnel metrics locate the constraint. If meetings-to-opportunity conversion is healthy but meetings are scarce, more AE training will not help.

**How to implement.**

- Store stage history as events (`entity_id, stage, entered_at, exited_at`), not only the current stage on the record. CRMs overwrite current stage; you cannot reconstruct conversion from a snapshot.
- Define each stage with an entry criterion written in code ("meeting held" means the calendar event occurred and was marked held, not "meeting booked").
- Measure conversion within a cohort window: of leads created in March, how many reached opportunity within 90 days. Comparing this month's opportunities to this month's leads mixes cohorts and lags.
- Handle stage skipping explicitly. A deal that jumps from Discovery to Proposal still passed through the earlier stages for counting purposes, or you will undercount earlier conversion.

**What goes wrong.** Stage definitions drift as reps use stages differently. Mean time-in-stage is dominated by a few stalled deals. Reopened records create duplicate entries. See [the revenue bowtie](../02-revenue-bowtie/README.md) for the stage model across acquisition and expansion.

## Cohort analysis

Group entities by a shared start event (signup month, first meeting week, first campaign touch) and track outcomes by age since start.

```text
cohort_conversion(c, age) = entities in cohort c converted by age / entities in cohort c
net_revenue_retention(c, month m) = MRR of cohort c at month m / MRR of cohort c at month 0
```

Cohorts separate "the business changed" from "the mix changed." If overall conversion dropped, cohort curves show whether recent cohorts convert worse at the same age or whether you are simply comparing young cohorts to mature ones.

Use cohorts for outbound: group prospects by the week they entered a sequence and compare meeting rates at day 7, 14 and 30. This removes the bias of comparing a list that started yesterday to one that has had a month to respond.

## Attribution

**Models.**

| Model | Credit rule | Bias |
|---|---|---|
| First touch | 100% to first recorded touch | Overcredits awareness channels |
| Last touch | 100% to last touch before conversion | Overcredits bottom-funnel channels (branded search, direct) |
| Linear multi-touch | Equal credit to all touches | Credits noise touches equally |
| Position-based (U-shaped) | Heavier weight to first and lead-creation touches | Weights are a choice, not a finding |
| Data-driven | Model-estimated credit | Still correlational; opaque |

All rule-based models distribute credit among touches that were tracked. Touches that were not tracked (podcasts, peer referrals, dark social, AI assistant answers) get zero by construction.

**Sourced vs influenced pipeline.** Sourced: pipeline where the channel created the first qualifying touch or the opportunity. Influenced: pipeline where the channel had any touch before close. One opportunity can be influenced by five channels. Summing influenced pipeline across channels counts the same dollars multiple times and routinely produces totals larger than actual pipeline. Rules:

- Sourced pipeline is mutually exclusive and can be summed to total.
- Influenced pipeline is not exclusive. Report it per channel, never as a sum, and never added to sourced.
- Define the sourcing rule once, in code, with a tie-break (for example, earliest qualifying touch within 90 days before opportunity creation).

**The honest answer: incrementality.** Attribution describes who touched what. It does not tell you what would have happened without the channel. Holdout tests do:

```text
incremental_lift = (conversion_treated - conversion_holdout) / conversion_holdout
incremental_pipeline = (rate_treated - rate_holdout) * treated_population * avg_pipeline_per_conversion
```

Randomly withhold a channel from a share of eligible accounts (for example, exclude a random 10 to 20% of target accounts from a paid campaign or an outbound sequence) and compare downstream outcomes. Randomize at the account level for B2B, because contacts at the same account influence each other. Geographic holdouts work when account-level suppression is not possible.

## A/B testing and experiment design

**Components.**

1. **Hypothesis.** "Opening with the prospect's recent hiring signal instead of a generic pain statement increases qualified meeting rate for VP-level contacts at mid-market SaaS."
2. **Primary metric.** One metric, decided in advance. Choose a downstream metric: qualified meetings per delivered email, not reply rate. Reply rate counts "unsubscribe" and "not interested" as wins and can move opposite to pipeline.
3. **Guardrail metrics.** Unsubscribe rate, spam complaint rate, bounce rate. The test stops if a guardrail breaches.
4. **Minimum detectable effect (MDE).** The smallest lift worth acting on. Pick it from business value, not from what your sample can detect.
5. **Sample size, duration and stopping rule** fixed before launch.

**Sample size for two proportions** (per arm, two-sided test):

```text
n = (z_alpha/2 + z_beta)^2 * (p1(1 - p1) + p2(1 - p2)) / (p1 - p2)^2

z_alpha/2 = 1.96 for alpha = 0.05
z_beta    = 0.84 for 80% power
```

**Worked illustrative example.** Assume a baseline qualified meeting rate of 2.0% per delivered email (p1 = 0.020) and an MDE of a 50% relative lift (p2 = 0.030).

```text
(1.96 + 0.84)^2           = 7.84
p1(1 - p1) + p2(1 - p2)   = 0.0196 + 0.0291 = 0.0487
(p1 - p2)^2               = 0.0001
n = 7.84 * 0.0487 / 0.0001 = about 3,818 delivered emails per arm
```

Numbers are illustrative. The lesson holds generally: low base rates on downstream metrics need thousands of sends per arm to detect even large lifts. Detecting a 20% relative lift at the same baseline (p2 = 0.024) needs about 21,000 per arm, roughly five and a half times more. This is why many outbound "tests" on a few hundred sends are noise, and why the [GTM learning engine](../../projects/gtm-learning-engine/README.md) uses a fixed minimum of delivered emails before retiring a variant.

**Stopping rules and the peeking problem.** Checking a fixed-horizon test daily and stopping at the first p < 0.05 inflates the false positive rate well above 5%, because random fluctuation crosses the line at some point in most runs. Options:

- Fixed horizon: decide n in advance, look once.
- Sequential testing (for example, alpha-spending or always-valid confidence sequences) if you must monitor continuously.
- Bayesian approaches with a pre-registered decision rule (for example, retire a variant when the posterior probability it is worse exceeds 95% after a minimum sample).

**Segment-level testing.** A message that wins for VP Engineering may lose for CFOs. Either stratify randomization by segment (ICP x seniority) and analyze per segment with adequate sample, or pre-register the segments you will examine. Slicing results into twenty segments after the fact will find a "winner" by chance. Correct for multiple comparisons or treat post-hoc segments as hypotheses for the next test.

**Other outbound-specific issues.** Randomize at the contact level within a send window so both arms share deliverability conditions. Lagged outcomes: a meeting can come from email 3 of a sequence weeks later, so set the measurement window before launch. See [message rotation](../../case-studies/experimentation/message-rotation.md).

## Forecasting

**Weighted pipeline.**

```text
weighted_pipeline = sum over open opps of (amount * P(close | stage, segment))
```

**Stage probabilities from history, not defaults.** CRM default probabilities (10/25/50/75/90) are placeholders. Compute from closed history:

```text
P(won | stage s) = opps that reached s and closed won / opps that reached s and closed (won + lost)
```

Restrict to a recent window (for example, trailing four to six quarters), segment where volume allows (new vs expansion, SMB vs enterprise), and add a time decay: deals well past the median age for their stage close at lower rates.

**Commit and best case.** Rep and manager categories layered over the math:

- Commit: rep expects to close this period, will be held to it.
- Best case: plausible with things going right.
- Pipeline: everything else open with a close date in period.

Run both the category roll-up and the stage-weighted number. Large gaps between them are the signal for inspection.

**Forecast accuracy.** Track every period against actual:

```text
APE  = |actual - forecast| / actual
MAPE = mean of APE across periods (or teams)
bias = mean(forecast - actual) / mean(actual)   (positive = systematic over-forecast)
```

MAPE breaks when actuals approach zero (small teams, new segments); use weighted absolute percentage error (sum of absolute errors / sum of actuals) instead. Track accuracy at fixed points (week 2, week 6, week 10 of the quarter) because a forecast taken on the last day is trivially accurate.

## Propensity scoring

**What it is.** A model estimating the probability that an account or contact takes an action (books a meeting, converts to opportunity, buys) within a window.

**Data.** Firmographics (industry, headcount, growth), technographics, intent and engagement events, hiring signals, historical interaction. Labels come from CRM outcomes.

**How to implement.** Start with logistic regression or gradient-boosted trees on a clearly defined label ("opportunity created within 90 days of entering the target list"). Logistic regression gives coefficients sales leadership can read; trees usually perform better and need explanation tools (feature contributions per prediction). Present scores with the top contributing factors, because reps act on reasons, not decimals.

**Alternative.** A rules-based fit score (ICP criteria with weights) is often the right first version: no training data required, fully explainable, and it produces the labeled outcomes a model needs later.

## Churn prediction and customer health

**Churn prediction** estimates P(not renewing or contracting) within a window before renewal. Useful features: product usage trend (slope matters more than level), share of paid seats active, support ticket severity and volume, champion departure (contact left the company), executive sponsor engagement, billing issues, and contract terms.

**Customer health** is usually a composite score:

```text
health = w1 * usage_score + w2 * engagement_score + w3 * support_score + w4 * sentiment_score
```

A weighted composite is an opinion until validated. Test it: do accounts in the bottom health quintile churn at a higher rate than the top quintile, on historical data? If not, the weights are wrong or the inputs are.

Define the action for each band before deploying. A score with no playbook attached changes nothing.

## Calibration

A score is calibrated if, among accounts scored 0.30, about 30% convert. Many models rank well but are poorly calibrated, and forecasting or threshold-setting on uncalibrated scores produces wrong numbers.

**Reliability diagram.** Bin predictions (for example, deciles), plot mean predicted probability against observed rate per bin. A calibrated model sits on the diagonal.

**Brier score.**

```text
Brier = (1/N) * sum of (predicted_probability - actual_outcome)^2    (outcome is 0 or 1; lower is better)
```

Compare against the Brier score of always predicting the base rate. Fix miscalibration with Platt scaling or isotonic regression fitted on a held-out set.

## Model evaluation

**Confusion matrix** for a "will convert to opportunity" model at a chosen threshold:

| | Actually converts | Does not convert |
|---|---|---|
| Predicted converts | True positive: rep works it, it converts | False positive: rep time wasted |
| Predicted does not | False negative: good account ignored | True negative: correctly deprioritized |

GTM interpretation: false positives cost rep hours and erode trust in the score. False negatives cost pipeline and are invisible, because nobody sees the deal that never happened. When rep capacity is the constraint, prioritize precision in the top-scored band. When the market is small and every account matters, prioritize recall.

```text
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
F1        = 2 * precision * recall / (precision + recall)
```

**AUC (ROC).** Probability that a random positive is scored above a random negative. Threshold-independent, good for comparing models, but insensitive to calibration and can look strong on imbalanced data while precision in the region you act on is weak. For rare outcomes, also check precision-recall curves and **precision at k** (precision among the top k accounts a team can actually work), which maps directly to capacity.

**Lift by decile** is the version most sales leaders understand: "the top 10% of scored accounts convert at 3x the average rate" (stated as the formula `rate_in_decile / overall_rate`).

## Data leakage

Leakage is when the model has information at training time that it will not have at prediction time. Leaked models look excellent in validation and fail in production.

| Type | GTM example | Fix |
|---|---|---|
| Target leakage | "Number of AE activities" predicting opportunity creation, when activities mostly happen after an opp exists | Only use features computed as of the prediction date |
| Look-ahead bias | Using a firmographic snapshot pulled today to score accounts as of last year | Point-in-time feature tables with `as_of` dates |
| Current-period data | Training on Q3 outcomes while Q3 deals are still open, labeling open deals as "not won" | Only use cohorts whose outcome window has fully closed |
| Train/test contamination | Same account in train and test via different contacts or opportunities | Split by account, not by row |

The [SPX forecasting research](../../research/spx-forecasting/README.md) documents a look-ahead bias case, a useful reference for how leakage inflates backtests.

**Walk-forward validation for time series.** Train on months 1 to 12, test on month 13; train on 1 to 13, test on 14; and so on. Never randomly shuffle time-ordered data into train and test. Report the distribution of out-of-sample performance across folds, not the best fold.

## Feedback loops

When a model's recommendations change the data it later trains on, it learns its own bias.

Example: a propensity model sends top-scored accounts to reps. Reps work those accounts and they convert. Low-scored accounts are never worked and never convert. Retraining confirms that low-scored accounts do not convert, which may only mean nobody called them.

Mitigations:

- **Exploration holdout.** Route a small random share of low-scored accounts to normal treatment so outcomes exist across the score range.
- **Log treatment.** Record whether each account was worked, how and when. Train on outcome conditional on treatment, or restrict to treated accounts.
- **Monitor score distribution and outcome rates by band** after each retrain.

The same loop affects message experiments (a winning variant gets all traffic, so its decay goes unnoticed) and lead routing (top reps get top leads, so rep performance and lead quality are confounded).

## Systems and data

Where these numbers are computed matters as much as how.

| Layer | Holds | Rule |
|---|---|---|
| Source systems (CRM, MAP, sequencer, product) | Raw records and events | Do not compute reporting metrics here; CRM report logic drifts and cannot be versioned |
| Warehouse raw and staging | Extracted tables, stage history, touch events | Append-only where possible, so history survives overwrites in the source |
| Metric definitions (SQL models or a semantic layer) | Conversion, sourced pipeline, forecast inputs | One definition per metric, version-controlled, with tests |
| Feature tables | Point-in-time features for models | Every row keyed by `entity_id, as_of_date` |
| BI and reverse ETL | Dashboards, scores written back to CRM | Read from metric definitions only |

Test metric code like application code: row-count reconciliation against source, uniqueness on keys, no negative time-in-stage, sourced pipeline summing to total pipeline. When a dashboard and the CRM disagree, the answer should be a documented definition difference, not a mystery.

## Measuring business impact

A prediction is only worth its effect on decisions. Measure impact with a holdout: one group uses the score for prioritization, a randomized control group uses the prior method, and the comparison is pipeline or revenue per rep-hour over a fixed window. Model accuracy metrics are leading indicators; incremental pipeline is the outcome.

## Related

- [Lookalike and propensity model](../../projects/lookalike-model/README.md): learned ICP, time-based evaluation, leakage trap, outreach handoff with holdout
- [Revenue bowtie](../02-revenue-bowtie/README.md)
- [Data architecture](../03-data-architecture/README.md)
- [AI and agents](../05-ai-and-agents/README.md)
- [GTM learning engine](../../projects/gtm-learning-engine/README.md)
- [RouteHero territory scoring](../../projects/routehero/README.md)
- [Message rotation case study](../../case-studies/experimentation/message-rotation.md)
- [Proposed AI experiment](../../case-studies/experimentation/proposed-ai-experiment.md)
- [SPX forecasting research](../../research/spx-forecasting/README.md)
- [Governance and operations](../07-governance-and-operations/README.md)
- [Impact](../../IMPACT.md)
