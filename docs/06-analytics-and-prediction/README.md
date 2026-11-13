# Analytics and prediction for revenue systems

This section covers how a GTM team should measure and predict: funnels, cohorts, attribution, experiments, forecasts and predictive scores. The focus is on the common mistakes that make GTM numbers wrong in practice. Examples: adding up attribution credit that overlaps, calling a test early, building models on information you would not have had at the time, and models that learn from their own recommendations.

## Funnel analytics

**What it is.** A count of leads, accounts or opportunities reaching each stage, plus the conversion rate and the time between stages.

```text
stage_conversion(s -> s+1) = entities that reached s+1 / entities that reached s
time_in_stage              = exited_stage_at - entered_stage_at   (report median and p75, not mean)
```

Report time in stage as the median (the middle deal) and the 75th percentile (the point three quarters of deals beat), not the average. A few stuck deals drag the average up.

**Why it matters.** Funnel numbers show where the bottleneck is. If meetings convert to opportunities at a healthy rate but there are too few meetings, more AE training will not help.

**How to implement.**

- Save every stage change as its own record (`entity_id, stage, entered_at, exited_at`), not just the current stage. CRMs overwrite the current stage, so you cannot rebuild conversion rates from a snapshot.
- Define each stage with a written entry rule. For example, "meeting held" means the calendar event happened and was marked held, not that it was booked.
- Measure conversion for a fixed group over a fixed window: of the leads created in March, how many became opportunities within 90 days. Comparing this month's opportunities to this month's leads mixes groups and timing.
- Handle skipped stages on purpose. A deal that jumps from Discovery to Proposal still counts as passing the stages in between, or you will undercount early conversion.

**What goes wrong.** Reps start using stages differently over time, so definitions drift. Average time in stage gets skewed by a few stalled deals. Reopened records create duplicates. See [the revenue bowtie](../02-revenue-bowtie/README.md) for the stage model across both new sales and expansion.

## Cohort analysis

A cohort is a group that started at the same time: same signup month, same first-meeting week, or same first campaign touch. Cohort analysis tracks each group's results by how long it has been since they started.

```text
cohort_conversion(c, age) = entities in cohort c converted by age / entities in cohort c
net_revenue_retention(c, month m) = MRR of cohort c at month m / MRR of cohort c at month 0
```

Cohorts tell you whether the business actually changed or whether the mix just changed. If overall conversion dropped, cohort curves show whether recent groups really convert worse at the same age, or whether you are simply comparing young groups to older ones that have had more time.

Use cohorts for outbound too. Group prospects by the week they entered a sequence, then compare meeting rates at day 7, 14 and 30. This stops you from comparing a list that started yesterday with one that has had a month to respond.

## Attribution

Attribution is how you give credit for a deal to the marketing and sales touches that came before it.

**Models.**

| Model | Credit rule | Bias |
|---|---|---|
| First touch | 100% to first recorded touch | Overcredits awareness channels |
| Last touch | 100% to last touch before conversion | Overcredits bottom-funnel channels (branded search, direct) |
| Linear multi-touch | Equal credit to all touches | Credits noise touches equally |
| Position-based (U-shaped) | Heavier weight to first and lead-creation touches | Weights are a choice, not a finding |
| Data-driven | Model-estimated credit | Still correlational; opaque |

Every rule-based model splits credit among the touches that were tracked. Anything untracked (podcasts, peer referrals, private sharing in Slack groups and DMs, AI assistant answers) gets zero by design.

**Sourced vs influenced pipeline.** Sourced pipeline is pipeline where the channel created the first qualifying touch or the opportunity itself. Influenced pipeline is pipeline where the channel had any touch before the deal closed. One opportunity can be influenced by five channels. So if you add up influenced pipeline across channels, you count the same dollars several times, and the total often comes out bigger than your real pipeline. Rules:

- Each sourced dollar belongs to exactly one channel, so sourced pipeline adds up to the true total.
- Influenced pipeline overlaps. Report it per channel. Never add it up, and never add it to sourced.
- Write the sourcing rule once, in code, with a tie-breaker. For example: the earliest qualifying touch within 90 days before the opportunity was created.

**The honest answer: incrementality.** Attribution tells you who touched what. It does not tell you what would have happened without the channel. A holdout test does. A holdout is a group held back on purpose to compare against.

```text
incremental_lift = (conversion_treated - conversion_holdout) / conversion_holdout
incremental_pipeline = (rate_treated - rate_holdout) * treated_population * avg_pipeline_per_conversion
```

Randomly keep a share of eligible accounts out of a channel. For example, leave a random 10 to 20% of target accounts out of a paid campaign or outbound sequence, then compare what happens downstream. In B2B, pick at the account level, not the contact level, because people at the same company influence each other. If you cannot hold out individual accounts, hold out whole regions instead.

## A/B testing and experiment design

**Components.**

1. **Hypothesis.** "Opening with the prospect's recent hiring signal instead of a generic pain statement increases qualified meeting rate for VP-level contacts at mid-market SaaS."
2. **Primary metric.** One metric, chosen before the test starts. Pick one close to revenue: qualified meetings per delivered email, not reply rate. Reply rate counts "unsubscribe" and "not interested" as wins, and it can rise while pipeline falls.
3. **Guardrail metrics.** Unsubscribe rate, spam complaint rate, bounce rate. If one of these crosses its limit, the test stops.
4. **Minimum detectable effect (MDE).** The smallest improvement worth detecting. Choose it based on what is worth acting on for the business, not on what your sample size happens to allow.
5. **Sample size, duration and stopping rule**, all fixed before launch.

**Sample size for two proportions** (per arm, two-sided test). An "arm" is one version in the test. This formula tells you how many sends each version needs:

```text
n = (z_alpha/2 + z_beta)^2 * (p1(1 - p1) + p2(1 - p2)) / (p1 - p2)^2

z_alpha/2 = 1.96 for alpha = 0.05
z_beta    = 0.84 for 80% power
```

In plain terms: alpha = 0.05 means you accept a 5% chance of calling a winner when there is no real difference. 80% power means that if the improvement is real, the test catches it 80% of the time.

**Worked example.** Assume a starting rate of 2.0% qualified meetings per delivered email (p1 = 0.020), and the smallest improvement worth detecting is a 50% relative lift (p2 = 0.030).

```text
(1.96 + 0.84)^2           = 7.84
p1(1 - p1) + p2(1 - p2)   = 0.0196 + 0.0291 = 0.0487
(p1 - p2)^2               = 0.0001
n = 7.84 * 0.0487 / 0.0001 = about 3,818 delivered emails per arm
```

The general lesson: when the outcome you care about is rare, you need thousands of sends per version to detect even a big improvement. Detecting a 20% lift from the same starting rate (p2 = 0.024) needs about 21,000 per version, roughly five and a half times more. This is why many outbound "tests" on a few hundred sends are just noise. It is also why the [GTM learning engine](../../projects/gtm-learning-engine/README.md) requires a fixed minimum of delivered emails before it retires a message variant.

**Stopping rules and the peeking problem.** Suppose you check a test every day and stop the first time the result looks significant (p < 0.05). Your chance of a false winner ends up far above 5%, because random swings cross that line at some point in most tests. Options:

- Fixed horizon: decide the sample size in advance and look once.
- Sequential testing: methods built for checking continuously (for example, alpha-spending or always-valid confidence sequences), if you must watch the test as it runs.
- Bayesian approaches with a decision rule written down in advance. For example: retire a variant once there is more than a 95% probability it is worse, after a minimum sample.

**Segment-level testing.** A message that wins with VPs of Engineering may lose with CFOs. Either split the random assignment by segment (ICP tier x seniority) and analyze each segment with enough sample, or name the segments you will check before the test starts. If you slice results into twenty segments afterward, one will look like a winner by pure chance. Adjust for the number of comparisons, or treat those after-the-fact findings as ideas for the next test.

**Other outbound-specific issues.** Assign contacts randomly within the same send window, so both versions face the same inbox-delivery conditions. Results arrive late: a meeting can come from email 3 of a sequence weeks later, so set the measurement window before launch. See [message rotation](../../case-studies/experimentation/message-rotation.md).

## Forecasting

**Weighted pipeline.** Each open deal's amount, multiplied by its chance of closing given its stage and segment, then added up.

```text
weighted_pipeline = sum over open opps of (amount * P(close | stage, segment))
```

**Stage probabilities from history, not defaults.** The default CRM percentages (10/25/50/75/90) are placeholders. Calculate your own from closed deals:

```text
P(won | stage s) = opps that reached s and closed won / opps that reached s and closed (won + lost)
```

Use a recent window (for example, the last four to six quarters). Split by segment where there is enough volume (new vs expansion, SMB vs enterprise). And lower the odds for aging deals: deals that have sat in a stage well past the typical time close less often.

**Commit and best case.** These are the rep and manager calls that sit on top of the math:

- Commit: the rep expects to close it this period and will be held to it.
- Best case: could close if things go right.
- Pipeline: everything else that is open with a close date in the period.

Run both the rep roll-up and the stage-weighted number. A big gap between them tells you which deals to inspect.

**Forecast accuracy.** Compare every period's forecast to what actually happened:

```text
APE  = |actual - forecast| / actual
MAPE = mean of APE across periods (or teams)
bias = mean(forecast - actual) / mean(actual)   (positive = systematic over-forecast)
```

APE is the percentage miss for one period. MAPE is the average percentage miss across periods. Bias shows whether you lean consistently high (positive) or low (negative).

MAPE breaks down when actual results are near zero (small teams, new segments). In that case divide the total of all misses by the total of all actuals instead (weighted absolute percentage error). Measure accuracy at fixed points in the quarter (week 2, week 6, week 10), because a forecast made on the last day is accurate by default.

## Propensity scoring

**What it is.** A model that estimates how likely an account or contact is to take an action (book a meeting, become an opportunity, buy) within a set time.

**Data.** Company facts (industry, headcount, growth), the tools they use, intent and engagement activity, hiring signals and past interactions. The "right answers" the model learns from come from CRM outcomes.

**How to implement.** Start with logistic regression or gradient-boosted trees, two standard model types, on a clearly defined outcome ("opportunity created within 90 days of entering the target list"). Logistic regression produces weights sales leaders can read. Tree models usually predict better, but need extra tools to explain why each account scored the way it did. Show each score with its top reasons, because reps act on reasons, not decimals.

**Alternative.** A rules-based fit score (ICP criteria with weights) is often the right first version. It needs no history to train on, anyone can see how it works, and it produces the outcome records a model will need later.

## Churn prediction and customer health

**Churn prediction** estimates the chance a customer will not renew, or will shrink their contract, within a window before renewal. Useful inputs: the product usage trend (the direction matters more than the level), the share of paid seats in active use, support ticket volume and severity, champion departure (the contact left the company), executive sponsor engagement, billing issues and contract terms.

**Customer health** is usually a blended score:

```text
health = w1 * usage_score + w2 * engagement_score + w3 * support_score + w4 * sentiment_score
```

A blended score is just an opinion until it is tested. Test it on past data: do accounts in the bottom fifth of health scores churn more than accounts in the top fifth? If not, the weights or the inputs are wrong.

Decide what action each score band triggers before you roll it out. A score with no playbook attached changes nothing.

## Calibration

Calibration is whether a score's percentages match what actually happens. A score is calibrated if, among accounts scored 0.30, about 30% convert. Many models are good at ranking accounts but bad at the actual percentages. Forecasts and cutoffs built on those percentages come out wrong.

**Reliability diagram.** Group predictions into buckets (for example, ten equal groups), then chart the average predicted chance against the actual rate in each bucket. A calibrated model lines up on the diagonal.

**Brier score.** The average squared gap between the predicted chance and what actually happened (1 if it happened, 0 if not). Lower is better.

```text
Brier = (1/N) * sum of (predicted_probability - actual_outcome)^2    (outcome is 0 or 1; lower is better)
```

Compare it with the Brier score you would get by always predicting the average rate. If the model cannot beat that, it adds nothing. To fix percentages that are off, apply a standard correction (Platt scaling or isotonic regression) fitted on data held back from training.

## Model evaluation

**Confusion matrix.** A table of the four possible outcomes for a "will convert to opportunity" model at a chosen cutoff:

| | Actually converts | Does not convert |
|---|---|---|
| Predicted converts | True positive: rep works it, it converts | False positive: rep time wasted |
| Predicted does not | False negative: good account ignored | True negative: correctly deprioritized |

What this means for GTM: false positives cost rep hours and wear down trust in the score. False negatives cost pipeline, and nobody notices, because nobody sees the deal that never happened. When rep time is the limit, focus on precision (how often it was right when it flagged something) in the top-scored accounts. When the market is small and every account matters, focus on recall (how much of what was there it found).

```text
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
F1        = 2 * precision * recall / (precision + recall)
```

F1 is one combined score for accurate and thorough.

**AUC (ROC).** How often the model ranks a buyer above a non-buyer, if you pick one of each at random. It does not depend on a cutoff, so it is good for comparing models. But it ignores whether the percentages are right, and it can look strong when buyers are rare even though the accounts you actually work are poor. For rare outcomes, also check **precision at k**: of the top k accounts your team can actually work, how many convert. That maps straight to team capacity.

**Lift by decile** is the version most sales leaders find easiest: "the top 10% of scored accounts convert at 3x the average rate" (calculated as `rate_in_decile / overall_rate`).

## Data leakage

Data leakage means building a model with information you would not have had at the time of the prediction. Leaky models look excellent in testing and then fail in real use.

| Type | GTM example | Fix |
|---|---|---|
| Target leakage | "Number of AE activities" predicting opportunity creation, when activities mostly happen after an opp exists | Only use features computed as of the prediction date |
| Look-ahead bias | Using a firmographic snapshot pulled today to score accounts as of last year | Point-in-time feature tables with `as_of` dates |
| Current-period data | Training on Q3 outcomes while Q3 deals are still open, labeling open deals as "not won" | Only use cohorts whose outcome window has fully closed |
| Train/test contamination | Same account in train and test via different contacts or opportunities | Split by account, not by row |

The [SPX forecasting research](../../research/spx-forecasting/README.md) documents a look-ahead bias case. It is a useful example of how leakage makes back-tested results look better than they are.

**Walk-forward validation for time series.** For data ordered in time, test the way you would use the model in real life. Train on months 1 to 12 and test on month 13. Then train on 1 to 13 and test on 14, and so on. Never shuffle time-ordered data randomly into training and test sets. Report the spread of results across all test months, not the best one.

## Feedback loops

When a model's recommendations change the data it later learns from, it learns its own bias.

Example: a propensity model sends the top-scored accounts to reps. Reps work those accounts, and they convert. Low-scored accounts never get worked, so they never convert. When the model is retrained, it "confirms" that low-scored accounts do not convert, when the real reason may be that nobody called them.

Fixes:

- **Exploration holdout.** Send a small random share of low-scored accounts to normal outreach anyway, so you have results across the whole score range.
- **Record the treatment.** Log whether each account was worked, how and when. Then train on outcomes given the treatment, or only on accounts that were worked.
- **Watch score spread and outcome rates by band** after every retrain.

The same loop shows up in message tests (the winning version gets all the traffic, so nobody notices when it starts to wear out) and in lead routing (top reps get top leads, so you cannot tell rep skill from lead quality).

## Systems and data

Where these numbers are calculated matters as much as how.

| Layer | Holds | Rule |
|---|---|---|
| Source systems (CRM, MAP, sequencer, product) | Raw records and events | Do not compute reporting metrics here; CRM report logic drifts and cannot be versioned |
| Warehouse raw and staging | Extracted tables, stage history, touch events | Append-only where possible, so history survives overwrites in the source |
| Metric definitions (SQL models or a semantic layer) | Conversion, sourced pipeline, forecast inputs | One definition per metric, version-controlled, with tests |
| Feature tables | Point-in-time features for models | Every row keyed by `entity_id, as_of_date` |
| BI and reverse ETL | Dashboards, scores written back to CRM | Read from metric definitions only |

In this table, the warehouse is the central database where data from all tools lands. A semantic layer is one shared place where each metric is defined. Reverse ETL is the job that pushes results from the warehouse back into tools like the CRM.

Test metric code the same way you test software: row counts match the source, IDs are not duplicated, no negative time in stage, and sourced pipeline adds up to total pipeline. When a dashboard and the CRM disagree, the answer should be a written definition difference, not a mystery.

## Measuring business impact

A prediction is only worth what it changes in decisions. Measure that with a holdout. One group of reps prioritizes using the score. A randomly chosen control group keeps the old method. Compare pipeline or revenue per rep-hour over a fixed window. Model accuracy numbers are early signs. Extra pipeline is the result that counts.

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
