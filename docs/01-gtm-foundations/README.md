# GTM foundations

This page answers the questions a revenue system has to settle before anyone builds a workflow: who to sell to, how big the opportunity is, how to price it, and whether the math works. Every formula here is something a GTM system should be able to compute from its own data. If a number cannot be computed from the CRM, warehouse or billing system, that gap is the first engineering problem.

## GTM strategy in one sentence

A go-to-market strategy is a decision about **which accounts**, **which problem**, **which channel**, **which motion** and **which price**, made so that the cost to acquire a customer is recovered fast enough to fund the next one.

| Decision | Question it answers | Failure when skipped |
|---|---|---|
| Market | Where are the accounts that have the problem? | Reps prospect anyone with a website |
| ICP | Which of those accounts win, stay and expand? | High activity, low win rate |
| Positioning | Why us instead of the status quo or a competitor? | Discount-led deals, long cycles |
| Motion | How does a buyer go from unaware to signed? | Enterprise process on SMB deal sizes |
| Pricing | What unit of value do we charge for? | Revenue does not grow with customer usage |
| Economics | Does CAC pay back inside the cash runway? | Growth that burns cash faster than it compounds |

## TAM, SAM and SOM

| Term | Definition | Used for |
|---|---|---|
| TAM (total addressable market) | Revenue if every account with the problem bought at your price | Ceiling and investor narrative |
| SAM (serviceable addressable market) | The part of TAM your product, geography and motion can serve today | Territory and capacity planning |
| SOM (serviceable obtainable market) | The part of SAM you can realistically win in a time window given capacity and conversion | Revenue targets and hiring plans |

**Top-down** starts from a published market size and applies percentages ("the category is $X, we serve 20% of it"). It is fast and nearly useless for planning because nobody can call a percentage.

**Bottom-up** starts from countable accounts multiplied by an expected contract value. It is slower and far more useful, because the same account list becomes the prospect list, the territory map and the tiering input.

### Worked bottom-up example (illustrative numbers)

A vendor sells scheduling software to multi-location home-services companies in the US.

| Step | Filter | Accounts | ACV | Value |
|---|---|---|---|---|
| TAM | Home-services companies with 10 to 500 employees | 12,000 | $18,000 | $216.0M |
| SAM | Minus regions without support coverage, minus companies on a locked-in competitor contract | 4,800 | $18,000 | $86.4M |
| SOM (3 years) | 6 reps x 35 new logos per rep per year x 3 years, capped by SAM | 630 | $18,000 | $11.3M |

Two things fall out of this. First, SOM is bounded by **sales capacity**, not by market size, until capacity exceeds what the SAM can absorb. Second, the 4,800 SAM accounts are a finite list: every outbound plan downstream has to respect that number.

ACV should vary by account. A better bottom-up model uses an estimated contract value per account (for example `locations x price per location`) and sums it, which turns TAM into a ranked list instead of a single number. See [RouteHero](../../projects/routehero/README.md) for estimated contract value calculated per account.

## Ideal customer profile (ICP)

The ICP describes the **account** most likely to buy, succeed and expand. It is a hypothesis that closed-won and churn data should keep correcting.

| Criterion type | What it captures | Examples | Typical data source |
|---|---|---|---|
| Firmographic | What the company is | Industry, employee count, revenue band, location count, geography | Registries, data vendors, company website |
| Technographic | What it runs | CRM, ERP, field service platform, data warehouse | Site scans, job posts, vendor data |
| Behavioral | What it does with you | Site visits, content engagement, product usage, reply history | Web analytics, product events, sequencer |
| Situational (trigger) | What just changed | New funding, new executive, new location, hiring for a role, competitor contract renewal | News, job boards, filings, permits |

Firmographic and technographic criteria decide **fit**. Behavioral and situational criteria decide **timing**. A good-fit account with no trigger goes into a nurture tier. A trigger on a poor-fit account is noise.

### ICP vs persona

| | ICP | Persona |
|---|---|---|
| Describes | An account | A person inside an account |
| Answers | Should we pursue this company? | Who do we talk to and what do we say? |
| Built from | Win, churn and expansion data by account | Call notes, win/loss interviews, title and role data |
| Drives | List building, tiering, territory design | Messaging, sequencing, content, demo flow |

## Buyer personas and buying committees

B2B purchases above small deal sizes are made by a group. A persona map should name the role each person plays in the decision, not only their title.

| Role | What they care about | What they need from you |
|---|---|---|
| Economic buyer | Budget, return, risk to their plan | A business case with a payback period |
| Champion | Fixing a problem they own, looking good internally | Material they can forward and defend |
| Technical evaluator | Integration, security, admin effort | Docs, sandbox, architecture answers |
| End user | Daily workflow friction | A demo of their actual task |
| Procurement and legal | Terms, vendor risk, compliance | Security questionnaire, standard contract |
| Blocker | Status quo, competing project, prior vendor | An answer to the objection before it is raised |

Measurable outcome: **multi-threading rate** = opportunities with 3 or more engaged contacts / total open opportunities. Single-threaded deals are exposed to one person leaving or going quiet.

## Segmentation and tiering

Segmentation groups accounts by how they should be served (motion, pricing, channel). Tiering ranks accounts inside a segment by how much effort they deserve.

A simple tier score: `tier_score = fit_score x (1 + timing_score)`, where fit is 0 to 1 from firmographic and technographic criteria and timing is 0 to 1 from triggers and engagement.

| Tier | Rule (illustrative thresholds) | Treatment | Cost per account |
|---|---|---|---|
| A | High fit and an active trigger | Account research, multi-threaded outreach, rep-written first touch, calling | High |
| B | High fit, no current trigger, or medium fit with a trigger | Signal-based sequence, templated personalization, watch for triggers | Medium |
| C | Medium or low fit, no trigger | Marketing nurture, no rep time | Low |

Validate tiers against outcomes: win rate, ACV and cycle length by tier should separate cleanly. If tier A and tier B win at the same rate, the score is not measuring anything.

## Positioning

Positioning is the context that makes the product's value obvious to a specific buyer. A common structure (from April Dunford's *Obviously Awesome*) has five parts:

1. **Competitive alternatives**: what the buyer would do without you (often a spreadsheet or doing nothing).
2. **Unique attributes**: capabilities the alternatives lack.
3. **Value**: the business outcome those attributes produce.
4. **Target customers**: who cares most about that value (this should match the ICP).
5. **Market category**: the frame that tells the buyer how to evaluate you.

Measurable signals that positioning is wrong: win rate drops when a specific competitor appears, discount depth rises, or loss reasons cluster on "no decision". These come from structured loss reasons and call analysis, which is a data problem before it is a messaging problem.

## Pricing models

| Model | Charges for | Works when | Risk | System requirement |
|---|---|---|---|---|
| Per seat | Named or active users | Value scales with people using it | Customers ration seats, expansion stalls | Seat counts synced from product to billing and CRM |
| Usage-based | Consumption (records, calls, API requests) | Value scales with volume | Revenue volatility, hard to forecast | Metering pipeline, usage alerts to account owners |
| Flat | One price for the product | Simple product, SMB, self-serve | Leaves money on the table with large accounts | Minimal |
| Tiered | Packages with feature or volume limits | Clear segments with different needs | Packaging drift, too many tiers | Entitlements mapped to plan, upgrade triggers |
| Per territory or location | Each site, region or service area | Multi-location businesses, field operations | Location counts are hard to verify | Location data per account, identity resolution across sites |

The pricing unit becomes a data requirement. Per-location pricing is only enforceable if the system knows how many locations each account has.

## Unit economics

All formulas below should be computed per segment and per channel, not only company-wide.

| Metric | Formula | Notes |
|---|---|---|
| Blended CAC | Total sales and marketing cost / new customers acquired | Includes all channels, including organic and referral |
| Paid CAC | Paid channel spend / customers attributed to paid | Isolates spend efficiency; understates true cost |
| Fully loaded CAC | (Salaries + commissions + tools + data + ad spend + agency fees + allocated overhead) / new customers | The number finance should use |
| LTV (gross-margin based) | (ARPA x gross margin %) / churn rate | Use the same period for ARPA and churn (both monthly or both annual) |
| LTV:CAC | LTV / fully loaded CAC | Read with payback; a high ratio with a long payback still strains cash |
| CAC payback (months) | Fully loaded CAC / (monthly ARPA x gross margin %) | How long until a customer has repaid its acquisition cost |
| Sales velocity | (Opportunities x win rate x ACV) / sales cycle length (days) | Revenue per day the pipeline produces |
| Pipeline coverage | Open qualified pipeline for the period / remaining quota for the period | Required coverage is roughly 1 / historical win rate by value |

Illustrative check: fully loaded CAC of $9,000, monthly ARPA of $1,500, gross margin 80%. Payback = 9,000 / (1,500 x 0.80) = 7.5 months. Annual churn of 15% gives LTV = (18,000 x 0.80) / 0.15 = $96,000 and LTV:CAC of about 10.7.

Sales velocity shows which lever to pull. With 40 open opportunities, 25% win rate, $18,000 ACV and a 60-day cycle, velocity = (40 x 0.25 x 18,000) / 60 = $3,000 per day. Cutting the cycle to 45 days moves it to $4,000 per day without a single new opportunity.

## Territory planning

Balance territories by **potential**, not account count. Two territories with 400 accounts each can differ in value by a multiple.

`territory_potential = sum over accounts of (estimated contract value x probability of fit)`

| Territory (illustrative) | Accounts | Avg estimated contract value | Avg fit probability | Potential |
|---|---|---|---|---|
| North | 400 | $12,000 | 0.30 | $1.44M |
| South | 400 | $26,000 | 0.45 | $4.68M |

Equal counts, a 3x gap in potential. Reps in North will miss quota for reasons unrelated to skill, and attainment data will mislead hiring decisions. Rebalance until potential per rep is within an agreed band, then check travel time or time zones for field and calling motions. Territory design depends on clean location data and account hierarchies (parent company vs site), which is why it sits on the data model in [GTM ontology](../../projects/gtm-ontology/README.md).

## Start from the company's revenue target

Before any funnel math, decompose the company's number for the year or quarter across both sides of the bowtie. New-logo pipeline is only what is left after the existing base has done its part.

```
ending ARR target   = starting ARR x NRR + new-logo ARR
new-logo ARR needed = ending ARR target - (starting ARR x NRR)
```

**Illustrative example.** Starting ARR $8M, target $10M.

| Scenario | Base after NRR | New-logo ARR needed | Deals at $40K ACV | Opportunities at 25% win | Meetings at 60% meeting-to-opp |
|---|---|---|---|---|---|
| NRR 105% | $8.4M | $1.6M | 40 | 160 | about 267 |
| NRR 110% | $8.8M | $1.2M | 30 | 120 | 200 |

Five points of NRR remove 40 opportunities and about 67 held meetings from the outbound plan. So the first question is not "how do we get more pipeline" but "which lever closes the gap at the lowest cost per dollar": retention, expansion, conversion rates or top-of-funnel volume. Usually one or two are worth funding, and that decides what gets built.

Then check the top-down answer against bottom-up capacity: how many ICP accounts exist (SAM), how many accounts and calls reps can work, and the conversion rates actually observed. The gap between what the target demands and what capacity supports is where the engineering work is. If the gap cannot be closed with any lever, the target is the problem, and the right output is that analysis, not more automation.

## Conversion economics: working backward from a revenue target

For the new-logo part of the target, start at the revenue number and divide by each conversion rate to find the required top-of-funnel volume. Then compare the result to the SAM. This is the fastest way to find out whether a plan is possible.

Target: $600,000 in new ARR from outbound in one year, $18,000 ACV, using the SAM of 4,800 accounts from the TAM example. **All rates are illustrative.**

| Step | Rate (illustrative) | Required volume |
|---|---|---|
| New ARR target | | $600,000 |
| Closed-won deals | $600,000 / $18,000 ACV | 34 |
| Qualified opportunities | 25% win rate | 136 |
| Meetings held | 60% meeting-to-opportunity | 227 |
| Meetings booked | 80% show rate | 284 |
| Positive replies | 50% positive reply to booked meeting | 568 |
| Contacts reached | 2% positive reply rate | 28,400 |
| Accounts touched | 3 contacts per account | 9,467 |

The plan needs 9,467 account touches against a SAM of 4,800, so each SAM account gets contacted about twice a year. That is possible but risks list fatigue and domain reputation. The levers, in order of usual cost:

1. **Raise positive reply rate** with trigger-based targeting and lookalikes of closed-won accounts (2% to 3% cuts required contacts by a third). See the [lookalike model](../../projects/lookalike-model/README.md).
2. **Raise ACV** by focusing on larger accounts inside the SAM.
3. **Add channels** (calling, partner referrals, inbound) so outbound does not carry the whole target.
4. **Expand SAM** by adding a region or segment, which changes the ICP and needs validation first.

Build this table as a live model fed by actual rates from the CRM and sequencer. When a rate drifts, the required volume updates and the team sees the gap before the quarter ends.

## Related

- [GTM motions](gtm-motions.md)
- [Revenue bowtie](../02-revenue-bowtie/README.md)
- [Revenue bowtie stages](../02-revenue-bowtie/stages.md)
- [Data architecture](../03-data-architecture/README.md)
- [Analytics and prediction](../06-analytics-and-prediction/README.md)
- [Product marketing and growth](../08-product-marketing-and-growth/README.md)
- [RouteHero](../../projects/routehero/README.md)
- [GTM ontology](../../projects/gtm-ontology/README.md)
- [Engineering method](../../THINKING.md)
