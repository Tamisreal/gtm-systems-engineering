# Impact scorecard

What has been delivered, how it was measured, and how sure the evidence is. Every entry carries one of five labels, and the labels are never mixed in one number.

| Label | Meaning |
|---|---|
| **Measured / Verified** | Backed by a source record, a metric definition and an attribution method |
| **Self-reported** | A real result I can describe and defend; source records not attached |
| **Historical / Pending Verification** | Self-reported from past work; source records not yet attached |
| **Synthetic Demonstration** | Measured on invented data; proves a method, not a business result |
| **Proposed Experiment** | Designed with a pre-set decision rule; not yet run |
| **Exploratory Research** | Investigation with known validity problems |

A simulated metric is never presented as a commercial outcome. Historical results are not attributed to AI unless a method isolates the AI's contribution.

## 1. Measured / Verified

**Commercial outcomes: none yet published.** Historical results are listed in section 2 until source records are attached. The process is in the [evidence checklist](EVIDENCE_CHECKLIST.md).

**Engineering measurements** (verified from dated project records; these describe the product, not revenue):

| Result | Value | Source |
|---|---|---|
| Location coverage, RouteHero data source versus OpenStreetMap, same greater-Houston area | 24,348 versus 9,464 commercial-kitchen candidates | [ADR 0001](decision-examples/adr/0001-routehero-data-source.md), 2026-09-12 |
| Phone coverage on those locations | 86% versus about 55% | same |
| Tier distribution after score recalibration, 2,785 real accounts | Tier A moved from 0 accounts to roughly the top 2 to 3% | [ADR 0004](decision-examples/adr/0004-routehero-remove-circular-factor.md) |

Outcome chain, stopping where the evidence stops:

Business problem (operators cannot see which nearby kitchens are worth calling) → intervention (licensed per-site data, classified, sized and tiered) → operational change (a callable list with 86% phone coverage) → GTM KPI (meetings per 100 accounts called, by tier): **not yet measured** → revenue impact: **not yet measured**.

## 2. Self-reported results

True, with no source records attached. Not attributed to AI.

| Result | Value | How | Still to document |
|---|---|---|---|
| FiscalNote SDR, three months | 69 meetings, 27 opportunities, about $436,834 associated pipeline ARR | Built Salesforce reports to find true-ICP contacts that had never been reached out to; among the lowest activity on the team | Booked versus held; sourced versus influenced; amount field and date |
| FiscalNote SDR, meeting goal | About 23 meetings a month against a goal of 14 to 16 (roughly 145% to 165% of goal) | Same targeting approach | |
| RouteHero outbound to grease hood cleaning operators, offering to generate leads for their business | About 8,000 contacts, about 4% reply rate, about 40% of replies positive, about 30% of positive replies converted to sourced pipeline | Built the outbound myself for a market that is rarely prospected: owner-operated service businesses nobody was offering growth to | Period, channel, reply denominator |
| Quorum expansion whitespace | About $300K in sourced pipeline for a newly piloted expansion motion | Mined closed-lost opportunities: read the records and listened to old calls, learned how national organizations and their state chapters bought from each other and from Quorum, then worked those parent and child relationships | Closed-won |
| Quorum ICP contacts added to the CRM | 589 | An enrichment waterfall that added contacts with exact or similar titles to existing buyers: title lookalikes | |
| AI call analysis in production (Gong and Salesloft recordings, CRM) | Running workflow; no metric published | Keyword detection flagged signals, AI evaluated each call, results pushed to the CRM | A measured number: calls processed, fields filled, or rep time saved |
| RouteHero customers | 8 (revenue private) | Built the product and the outbound; sales calls convert better when the operator sees the map of potential customers around their shop | |
| Amazon FBA wholesale business, started from zero | Grossed about $3M a year | Zero to one | |

Outcome chain: business problem (meetings pursued through more activity into already-worked contacts) → intervention (Salesforce reports surfacing untouched true-ICP contacts) → operational change (same or less activity, aimed at fresh contacts) → GTM KPI (69 meetings, 27 opportunities in three months) → revenue impact (about $436,834 associated pipeline; closed-won not documented).

Full write-ups: [outbound and pipeline results](case-studies/revenue-impact/historical-outbound.md).

## 3. Historical / Pending Verification

None of these is attributed to AI or agents.

| Metric | Reported | Motion | Verification needed |
|---|---|---|---|
| Research time per rep | about 4 hours a day to 30 minutes | Operational productivity | Measurement method |
| Email infrastructure | about 500K emails a month, under 3% bounce, about 95% coverage | Data and deliverability | Platform reports |

Full detail and documentation requirements: [historical outbound results](case-studies/revenue-impact/historical-outbound.md), [Amazon wholesale](case-studies/zero-to-one/amazon-wholesale.md).

## 4. Synthetic Demonstrations

| Result | Value | What it proves | What it does not prove |
|---|---|---|---|
| Call-signal extraction, rules baseline, 12 calls / 57 labels | F1 0.919; auto-applied precision 1.000 at recall 0.386; 59% of kept signals sent to review; 100% schema-valid and grounded; $0 | The pipeline validates, routes and measures correctly, and the review load is the cost to beat | Accuracy on real calls (same author wrote the data, labels and rules) |
| Lookalike and propensity model, time-based test set | Logistic regression AUC 0.660 versus 0.583 for the written ICP; 1.9x lift in the top 10% | Learning the ICP from outcomes ranks better than a static rule, and the leakage check catches a feature that scores 0.999 but cannot rank uncontacted accounts | Incremental meetings, which need the holdout comparison |
| Message rotation versus static split | 56% more positive replies | The retire-and-scale rules work when messages differ | Any real program's lift |

Sources: [AI evaluation harness](projects/ai-evaluation/README.md), [message rotation](case-studies/experimentation/message-rotation.md), [lookalike model](projects/lookalike-model/README.md).

## 5. Proposed Experiments

| Experiment | Primary metric | Decision rule |
|---|---|---|
| Claude extractor versus rules baseline | Review share of kept signals, at auto-applied precision of at least 0.95 | Adopt per signal type only if review share falls below 40% and cost per correct signal is below the reviewer time saved |
| AI-researched first lines versus template | Qualified meetings per 1,000 delivered | Adopt only if the lift is significant and cost per incremental meeting is below current cost per qualified meeting |

Sources: [AI evaluation harness](projects/ai-evaluation/README.md#the-llm-comparison-not-yet-run), [proposed AI experiment](case-studies/experimentation/proposed-ai-experiment.md).

## How each metric is defined

Definitions are fixed here so a result reported later cannot quietly change what it measures.

| Metric | Definition | Formula |
|---|---|---|
| Qualified pipeline (sourced) | Opportunities created by the motion that met the qualification rule | sum of amount at creation for sourced opportunities |
| Pipeline (influenced) | Opportunities the motion touched before close but did not create | reported separately; never added to sourced |
| Meetings booked / held | Held = took place with an ICP buyer | count per period |
| Opportunity conversion rate | Share of held meetings that became qualified opportunities | opportunities / held meetings |
| Closed-won revenue | First-year contract value of won opportunities | sum of won amount in period |
| Cost per lead | Total program cost / leads | (tools + data + labor + model spend) / leads |
| Cost per qualified meeting | Total program cost / held qualified meetings | same numerator / qualified meetings |
| Cost per opportunity | Total program cost / qualified opportunities | same numerator / opportunities |
| Conversion lift | Treatment rate versus control rate, with confidence interval | (treatment - control) / control |
| Hours saved | Time per task before and after, times frequency, times people | (before - after) x tasks per week x people |
| AI output accuracy | Precision and recall against labeled ground truth | TP / (TP + FP), TP / (TP + FN) |
| AI acceptance rate | Share of AI outputs a reviewer accepted unchanged | accepted / reviewed |
| Agent or model cost | Token cost per run and per correct output | (input tokens x input price + output tokens x output price) / correct outputs |

## Related

- [Evidence checklist](EVIDENCE_CHECKLIST.md)
- [Impact record template](templates/impact-record-template.md)
- [Case studies](case-studies/README.md)
- [THINKING.md](THINKING.md)
