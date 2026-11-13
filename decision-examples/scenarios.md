# Scenario-based reasoning

Eight common go-to-market (GTM) problems, each worked through with the method in [How I think](../README.md).

Each scenario follows the same path: problem, investigation, options, hypothesis (a testable guess), implementation, measurement, decision.

## 1. Low outbound reply rates

**Problem.** The reply rate on a cold email program fell from about 3% to under 1% over six weeks. Leadership asks for new copy.

**Investigation.** Copy is the last thing to check, not the first. Check in this order:

1. Deliverability: are emails reaching the inbox? Look at inbox placement tests, bounce rate, spam complaints, how old the domains and mailboxes are, and how much each mailbox sends.
2. List quality: bounce rate by data source, and the share of contacts that fit the ideal customer profile (ICP).
3. Targeting: reply rate by segment, by seniority, by buying signal.
4. Copy: reply rate by message version within one segment.

**Options.** New copy; a new list source; fix the sending setup; pause and warm up new domains.

**Hypothesis.** If bounces from one data source went up at the same time replies fell, the cause is a decaying list hurting the sender's reputation, not the copy. Fixing the source will get emails back into the inbox, and that matters before any copy change.

**Implementation.** Break out reply and bounce rates by data source and mailbox. Stop using the failing source. Verify emails before sending. Move sending off damaged mailboxes.

**Measurement.** First, inbox placement rate and bounce rate under a set limit. Then reply rate and positive reply rate per 1,000 emails delivered. Then qualified meetings per 1,000 delivered.

**Decision.** A copy test starts only after deliverability recovers. It runs per segment, with a minimum sample size and a confidence rule set in advance.

**Why not an agent.** Every step here is a lookup over sending and bounce data. An AI agent adds cost and unpredictable results to what is basic math.

## 2. Poor CRM data quality

**Problem.** Reps say the CRM is unusable: duplicates, missing titles, wrong owners.

**Investigation.** Measure before fixing:

- Duplicate rate by record type and by source.
- How often each required field is blank.
- Share of records with no activity in 12 months.
- Who or what created the bad records: an integration, a list import, or a person typing them in.

**Options.** A one-time cleanup project; a dedupe tool; stopping bad data where it enters (validation rules, checking for a match before creating a record, one system in charge of each field); all three.

**Hypothesis.** Most new bad records come from two or three integrations. Fixing where data enters prevents more damage than a cleanup that falls apart again within a quarter.

**Implementation.** A field ownership map (one system is in charge of each field). Check for an existing match on domain and email before creating a record. Validate data where each integration feeds in. Then do a one-time merge, with a person reviewing any records that are a likely match but not certain.

**Measurement.** How many duplicates are created each week, how often required fields are filled in, data problems reported by reps, and the knock-on effects: leads sent to the wrong rep and time to first touch.

**Decision.** Keep the prevention controls for good. Schedule cleanup only for the existing backlog.

**Why not an agent.** Matching on exact values is plain code with fixed rules. A model can help suggest possible name matches, but a person still approves every merge.

## 3. Selecting an enrichment vendor

**Problem.** Three data enrichment vendors (companies that fill in missing contact and company details) each claim the best coverage.

**Investigation.** Vendors measure their coverage on their own data. Build a test set from your own ideal customer profile: a few hundred accounts and contacts, including the hard segments (small businesses, non-tech companies, international), with known-correct answers for a sample.

**Options.** One vendor; a waterfall (try vendor A, and only call vendor B when A has no answer); the current vendor plus one vendor to fill gaps.

**Hypothesis.** A waterfall of two vendors will be as accurate as the best single vendor, find more contacts, and cost less per verified contact, because the second vendor is only paid when the first one misses.

**Implementation.** Run the same test set through each vendor and each waterfall order. Record match rate, accuracy against the known answers, bounce rate after email verification, and cost.

**Measurement.** Cost per verified contact = total spend / verified contacts. Coverage by segment. Bounce rate after sending.

**Decision.** Pick the order with the lowest cost per verified contact that stays under the bounce limit in your most valuable segment. Check the license: are you allowed to store the enriched data, and for how long?

**Why not an agent.** Picking a vendor is a side-by-side comparison on a fixed test set.

## 4. Designing custom buying signals

**Problem.** Third-party intent data (feeds that claim to show which companies are researching a topic) is noisy, and every competitor buys the same feed.

**Investigation.** Look at closed-won deals from the last year. What was true of those accounts 30 to 90 days before the first meeting that was not true of lost or never-engaged accounts? Hiring for a role, a new leader, a change in the software they use, a pricing page change, a new regulation?

**Options.** Buy more intent data; build your own signals from public sources; combine both.

**Hypothesis.** A signal that shows up before the first meeting in a clearly higher share of won accounts than in the rest of the target list will raise reply and meeting rates when used to time outreach and choose the message angle.

**Implementation.** Test each possible signal on past accounts, using only information you would have had before the meeting date. Launch the two strongest as scheduled jobs, saving the proof for each signal.

**Measurement.** Lift: meeting rate for accounts with the signal versus a similar group without it, measured on a held-back group that was not used to pick the signals.

**Decision.** Keep signals that show lift in the held-back group. Retire signals whose lift fades. Signals wear out as competitors copy them.

**Why not an agent.** Spotting the signal is a scheduled lookup or web scrape. A model may summarize the proof for the rep, but it does not decide whether the signal fired.

## 5. Introducing an AI agent

**Problem.** A sales leader wants "an AI SDR".

**Investigation.** Break the SDR job into tasks and put a price on each: research, list building, writing, sending, replying, booking, CRM updates. For each one: is the rule known? What does a mistake cost? How much volume is there?

**Options.** One AI agent doing the whole job on its own; automation with an AI model used only for writing; human SDRs helped by an agent.

**Hypothesis.** Most of the value comes from research and first drafts, which an automated workflow with one AI writing step can handle. Letting the AI reply to buyers on its own carries the highest cost when it gets it wrong (a wrong answer to a real buyer), for the least time saved.

**Implementation.** Automate research and drafts, with a person approving them. Measure how often drafts are accepted. Give the AI more freedom one step at a time, only where nearly every draft is accepted.

**Measurement.** Draft acceptance rate, edits per draft, meetings per SDR hour, positive reply rate compared with a control group, and cost per qualified meeting including AI model spend.

**Decision.** The AI earns freedom task by task through measured acceptance. It is not handed freedom up front.

**Why not an agent (for most of it).** Agents fit open-ended tasks where mistakes can be fixed. An email sent to a buyer cannot be unsent.

## 6. Customer retention problems

**Problem.** Gross revenue retention dropped, and churn caught the customer success (CS) team by surprise.

**Investigation.** For every account that churned in the last year: what did product usage, support tickets, champion changes and call content look like 60, 90 and 120 days before they gave notice? Compare with accounts that stayed, from the same starting group.

**Options.** A health score; a churn prediction model; a set of early-warning rules, each tied to a playbook.

**Hypothesis.** Two or three visible events (the champion left, usage fell below a set level, the customer asked a competitor for a quote) come before most churn, early enough to act.

**Implementation.** Rules on those events, each one creating a task for the customer success manager (CSM) with the proof attached. Signals from calls go through the review steps in [conversation intelligence](../projects/conversation-intelligence/README.md).

**Measurement.** Share of churned accounts flagged at least 60 days before notice (how many real risks were caught). Share of flags that were real risks (how many flags were right). Save rate on flagged accounts versus past accounts that were not flagged.

**Decision.** A prediction model is worth it only when the simple rules stop improving, and when there is enough churn history to build and test it without using information you would not have had at the time.

**Why not an agent.** The trigger is a rule. The CSM's conversation with the customer is the fix.

## 7. Forecasting pipeline

**Problem.** The quarterly forecast misses by a wide margin, in both directions.

**Investigation.** Compare each week's forecast with the final result. Is the error in the win odds given to each stage, in close dates that slip, or in deals that appear late in the quarter?

**Options.** Rep commit only; pipeline weighted by how often each stage has actually closed in the past; a prediction model based on deal details.

**Hypothesis.** Most of the error comes from stage win odds set by opinion instead of by history.

**Implementation.** From closed deals over the last four to six quarters, work out how often each stage ends in a win and how often close dates slip. Weight the pipeline with those numbers. Run it next to the rep commit.

**Measurement.** Forecast error (for example MAPE, the average percentage miss) by week of the quarter, for both methods, over at least two quarters.

**Decision.** Use the method with the smaller error in the weeks that matter for planning. Keep both visible.

**Why not an agent.** A forecast is math on past results plus judgment on a few large deals.

## 8. Custom development versus existing SaaS

**Problem.** The team wants to build its own lead-routing software because the CRM's built-in routing "is not flexible enough".

**Investigation.** List the routing rules that are actually needed. Check how many of them the CRM's built-in tools or the current routing product already handle.

**Options.** Set up the built-in routing; buy a routing tool; build custom software.

**Hypothesis.** The built-in tools cover most rules. One or two exceptions justify a small add-on, not a whole new system.

**Implementation.** Set up the built-in routing. Build only the exception, as a small piece of code that runs automatically when the CRM sends an event (a webhook), and keep a log of what it does.

**Measurement.** Speed to lead, share of leads sent to the wrong rep, admin hours per month, cost.

**Decision.** Build when the need is something that truly sets you apart, or a gap no tool fills. Otherwise extend what you have. See [build vs buy vs extend](../docs/03-data-architecture/build-buy-extend.md).

## Related

- [Architecture decision records](README.md)
- [Failure analysis](failure-analysis.md)
- [How I think](../README.md)
