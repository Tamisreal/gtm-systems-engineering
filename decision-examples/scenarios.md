# Scenario-based reasoning

**Evidence status: Hypothetical.** None of these scenarios describes a real company, engagement or result. They show how the method in [THINKING.md](../THINKING.md) runs on common GTM problems. All numbers are illustrative.

Each scenario follows the same path: problem, investigation, options, hypothesis, implementation, measurement, decision.

## 1. Low outbound reply rates

**Problem.** Reply rate on a cold email program fell from about 3% to under 1% over six weeks. Leadership asks for new copy.

**Investigation.** Copy is the last thing to check, not the first. In order: deliverability (inbox placement tests, bounce rate, spam complaints, domain and mailbox age, sending volume per mailbox); list quality (bounce rate by data source, share of contacts matching ICP rules); targeting (reply rate by segment, by seniority, by signal); then copy (reply rate by message variant within one segment).

**Options.** New copy; new list source; repair sending infrastructure; pause and warm new domains.

**Hypothesis.** If bounces rose from one data source at the same time replies fell, the cause is list decay hitting sender reputation, not copy. Fixing the source will recover inbox placement before any copy change matters.

**Implementation.** Split reply and bounce rates by data source and mailbox. Suppress the failing source. Verify emails before send. Move volume off damaged mailboxes.

**Measurement.** Inbox placement rate, bounce rate under a set limit, then reply rate and positive reply rate per 1,000 delivered, then qualified meetings per 1,000 delivered.

**Decision.** Only after deliverability recovers does a copy test start, per segment, with a minimum sample and a fixed confidence rule.

**Why not an agent.** Every step here is a query over sending and bounce data. An agent adds cost and nondeterminism to arithmetic.

## 2. Poor CRM data quality

**Problem.** Reps say the CRM is unusable: duplicates, missing titles, wrong owners.

**Investigation.** Measure before fixing: duplicate rate by object and source, null rate per required field, share of records with no activity in 12 months, who and what created bad records (integration user, list import, manual).

**Options.** One-time cleanup project; dedupe tool; prevention at the point of entry (validation rules, matching on create, field ownership per system); all three.

**Hypothesis.** Most new bad records come from two or three integration paths. Fixing entry prevents more damage than a cleanup that decays within a quarter.

**Implementation.** Field ownership map (one system owns each field). Match-before-create on domain and email. Validation at the integration boundary. Then a one-time merge with a review queue for fuzzy matches.

**Measurement.** Weekly duplicate creation rate, required-field fill rate, rep-reported data issues, and downstream: routing errors and time to first touch.

**Decision.** Keep the prevention controls permanently; schedule cleanup only for the backlog.

**Why not an agent.** Matching on exact keys is deterministic. A model can help with fuzzy name matching candidates, but merges stay behind a reviewer.

## 3. Selecting an enrichment vendor

**Problem.** Three enrichment vendors each claim the best coverage.

**Investigation.** Vendor coverage claims are measured on their own data. Build a test set from your own ICP: a few hundred accounts and contacts, including hard segments (SMB, non-tech, international), with known-correct values for a sample.

**Options.** Single vendor; waterfall across vendors; existing vendor plus one gap filler.

**Hypothesis.** A waterfall of two vendors matches the best single vendor's accuracy at higher coverage, and costs less per verified contact because the second vendor is only called on misses.

**Implementation.** Run the same test set through each vendor and each waterfall order. Record match rate, accuracy against the known sample, bounce rate after verification, and cost.

**Measurement.** Cost per verified contact = total spend / verified contacts. Coverage by segment. Bounce rate after send.

**Decision.** Choose the order with the lowest cost per verified contact that meets the bounce limit in your highest-value segment. Check the license: can enriched data be stored, and for how long?

**Why not an agent.** Vendor selection is a structured comparison over a fixed test set.

## 4. Designing custom buying signals

**Problem.** Third-party intent data is noisy and every competitor buys the same feed.

**Investigation.** Look at closed-won deals from the last year. What was true of those accounts 30 to 90 days before the first meeting that was not true of lost or never-engaged accounts? Hiring for a role, a new leader, a tech-stack change, a pricing page change, a regulatory event?

**Options.** Buy more intent data; build first-party signals from public sources; combine.

**Hypothesis.** A signal that appears in a meaningfully higher share of won accounts than of the rest of the ICP, before the first meeting, will raise reply and meeting rates when used for timing and message angle.

**Implementation.** Backtest each candidate signal on historical accounts (strictly using data available before the meeting date). Ship the two strongest as scheduled jobs with evidence stored per signal.

**Measurement.** Lift: meeting rate for signaled accounts versus a matched unsignaled group, in a holdout.

**Decision.** Keep signals that show lift in the holdout. Retire signals whose lift fades. Signals decay as competitors copy them.

**Why not an agent.** Detection is a scheduled query or scrape. A model may summarize evidence for the rep; it does not decide whether the signal fired.

## 5. Introducing an AI agent

**Problem.** A sales leader wants "an AI SDR".

**Investigation.** Break the SDR job into tasks and price each: research, list building, writing, sending, replying, booking, CRM updates. For each, is the rule known? What does an error cost? What volume?

**Options.** Autonomous agent across the whole job; workflow automation with an LLM for writing only; agent-assisted human SDRs.

**Hypothesis.** Most of the value comes from research and first-draft writing, which a workflow with an LLM step handles. Autonomous replying carries the highest error cost (a wrong answer to a real buyer) for the least time saved.

**Implementation.** Automate research and drafts with human approval. Measure acceptance rate of drafts. Expand autonomy step by step only where acceptance is near total.

**Measurement.** Draft acceptance rate, edits per draft, meetings per SDR hour, positive reply rate versus a control group, cost per qualified meeting including model spend.

**Decision.** Autonomy is earned per task by measured acceptance, not granted up front.

**Why not an agent (for most of it).** Agents fit open-ended tasks with recoverable errors. Sending email to a buyer is not recoverable.

## 6. Customer retention problems

**Problem.** Gross revenue retention dropped and churn surprised the CS team.

**Investigation.** For every churned account in the last year: what did usage, support tickets, champion changes and call content look like 60, 90 and 120 days before the notice? Compare with retained accounts in the same cohort.

**Options.** A health score; a churn model; a set of early-warning rules tied to playbooks.

**Hypothesis.** Two or three observable events (champion left, usage fell below a threshold, competitor quote requested) precede most churn early enough to act.

**Implementation.** Rules on those events, each creating a CSM task with evidence. Signals from calls go through the review flow in [conversation intelligence](../projects/conversation-intelligence/README.md).

**Measurement.** Share of churned accounts flagged at least 60 days before notice (recall); share of flags that were real risks (precision); save rate on flagged accounts versus unflagged history.

**Decision.** A model is justified only when the simple rules plateau and there is enough churn history to train and validate it without leakage.

**Why not an agent.** The trigger logic is a rule. The CSM's conversation is the intervention.

## 7. Forecasting pipeline

**Problem.** The quarterly forecast misses by a wide margin, in both directions.

**Investigation.** Compare each week's forecast with the final result. Is the error in stage probabilities, in slipped close dates, or in deals that appear late in the quarter?

**Options.** Rep commit only; weighted pipeline with historical stage conversion; a model on deal features.

**Hypothesis.** Stage probabilities set by opinion, not by history, cause most of the error.

**Implementation.** Compute stage-to-close rates and slip rates from closed deals over the last four to six quarters. Weight pipeline with those. Run it beside the rep commit.

**Measurement.** Forecast error (for example MAPE) by week of quarter, for both methods, over at least two quarters.

**Decision.** Use the method with lower error at the weeks that matter for planning. Keep both visible.

**Why not an agent.** A forecast is arithmetic on history plus judgment on a few large deals.

## 8. Custom development versus existing SaaS

**Problem.** The team wants to build a custom lead-routing service because the CRM's native routing "is not flexible enough".

**Investigation.** List the routing rules actually needed. Check how many the CRM's native tools or the existing routing product already support.

**Options.** Configure native routing; buy a routing tool; build a service.

**Hypothesis.** Native tools cover most rules; one or two exceptions justify a small extension, not a service.

**Implementation.** Configure the native path. Build only the exception as a small function triggered by a webhook, with logging.

**Measurement.** Speed to lead, misrouted lead rate, admin hours per month, cost.

**Decision.** Build when the requirement is a real differentiator or a gap no tool fills. Otherwise extend. See [build vs buy vs extend](../docs/03-data-architecture/build-buy-extend.md).

## Related

- [Architecture decision records](README.md)
- [Failure analysis](failure-analysis.md)
- [THINKING.md](../THINKING.md)
