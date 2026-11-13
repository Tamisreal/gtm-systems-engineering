# GTM foundations

Before anyone builds a workflow, a revenue team has to answer a few basic questions. Who should we sell to? How big is the opportunity? How should we price it? Does the math work? This page covers those questions.

Every formula here should be something the company can calculate from its own data. If a number cannot be pulled from the CRM (customer relationship management system, such as Salesforce or HubSpot), the data warehouse (the central database that holds a copy of all company data) or the billing system, fixing that gap is the first job.

## GTM strategy in one sentence

A go-to-market (GTM) strategy is a set of choices: **which accounts**, **which problem**, **which channel**, **which motion** (the way a buyer moves from first contact to signed deal) and **which price**. The choices must add up so that the cost of winning a customer is paid back fast enough to fund winning the next one.

| Decision | Question it answers | Failure when skipped |
|---|---|---|
| Market | Where are the accounts that have the problem? | Reps prospect anyone with a website |
| ICP | Which of those accounts win, stay and expand? | High activity, low win rate |
| Positioning | Why us instead of the status quo or a competitor? | Discount-led deals, long cycles |
| Motion | How does a buyer go from unaware to signed? | Enterprise process on SMB deal sizes |
| Pricing | What unit of value do we charge for? | Revenue does not grow with customer usage |
| Economics | Does CAC pay back inside the cash runway? | Growth that burns cash faster than it compounds |

ICP means ideal customer profile. SMB means small and mid-sized business. CAC means customer acquisition cost: what it costs in sales and marketing to win one new customer.

## TAM, SAM and SOM

These three numbers describe how big the opportunity is, from the theoretical maximum down to what you can realistically win.

| Term | Definition | Used for |
|---|---|---|
| TAM (total addressable market) | Revenue if every account with the problem bought at your price | Ceiling and investor narrative |
| SAM (serviceable addressable market) | The part of TAM your product, geography and motion can serve today | Territory and capacity planning |
| SOM (serviceable obtainable market) | The part of SAM you can realistically win in a time window given capacity and conversion | Revenue targets and hiring plans |

**Top-down** sizing starts from a published market size and applies percentages ("the category is $X, we serve 20% of it"). It is fast, but it is nearly useless for planning. Nobody can call a percentage.

**Bottom-up** sizing counts real accounts and multiplies by an expected contract value. It takes longer, but it is far more useful. The same account list becomes the prospect list, the territory map and the starting point for ranking accounts.

### Worked bottom-up example

A vendor sells scheduling software to US home-services companies with several locations. ACV means annual contract value: what one customer pays per year.

| Step | Filter | Accounts | ACV | Value |
|---|---|---|---|---|
| TAM | Home-services companies with 10 to 500 employees | 12,000 | $18,000 | $216.0M |
| SAM | Minus regions without support coverage, minus companies on a locked-in competitor contract | 4,800 | $18,000 | $86.4M |
| SOM (3 years) | 6 reps x 35 new logos per rep per year x 3 years, capped by SAM | 630 | $18,000 | $11.3M |

Two lessons come out of this. First, what you can win (SOM) is limited by **sales capacity**, not market size. That stays true until you have more reps than the SAM can keep busy. Second, the 4,800 SAM accounts are a fixed list. Every outbound plan has to respect that number.

ACV should differ from account to account. A better model estimates a contract value for each account (for example `locations x price per location`) and adds them up. That turns TAM from a single number into a ranked list. See [RouteHero](../../projects/routehero/README.md) for an estimated contract value calculated for each account.

## Ideal customer profile (ICP)

The ICP describes the type of **company** most likely to buy, succeed and grow its spend. Treat it as a working guess. Data on won deals and lost customers should keep correcting it.

| Criterion type | What it captures | Examples | Typical data source |
|---|---|---|---|
| Firmographic | What the company is | Industry, employee count, revenue band, location count, geography | Registries, data vendors, company website |
| Technographic | What it runs | CRM, ERP, field service platform, data warehouse | Site scans, job posts, vendor data |
| Behavioral | What it does with you | Site visits, content engagement, product usage, reply history | Web analytics, product events, sequencer |
| Situational (trigger) | What just changed | New funding, new executive, new location, hiring for a role, competitor contract renewal | News, job boards, filings, permits |

ERP is the software a company runs its finance and operations on. A sequencer is the tool that sends a series of outreach emails.

Firmographic and technographic facts tell you whether an account is a good **fit**. Behavior and recent changes tell you whether the **timing** is right. A good-fit account with no recent change goes into a slower nurture track. A recent change at a poor-fit account is noise.

### ICP vs persona

| | ICP | Persona |
|---|---|---|
| Describes | An account | A person inside an account |
| Answers | Should we pursue this company? | Who do we talk to and what do we say? |
| Built from | Win, churn and expansion data by account | Call notes, win/loss interviews, title and role data |
| Drives | List building, tiering, territory design | Messaging, sequencing, content, demo flow |

## Buyer personas and buying committees

Most B2B purchases above a small deal size are made by a group, not one person. A persona map should name the role each person plays in the decision, not only their job title.

| Role | What they care about | What they need from you |
|---|---|---|
| Economic buyer | Budget, return, risk to their plan | A business case with a payback period |
| Champion | Fixing a problem they own, looking good internally | Material they can forward and defend |
| Technical evaluator | Integration, security, admin effort | Docs, sandbox, architecture answers |
| End user | Daily workflow friction | A demo of their actual task |
| Procurement and legal | Terms, vendor risk, compliance | Security questionnaire, standard contract |
| Blocker | Status quo, competing project, prior vendor | An answer to the objection before it is raised |

How to measure it: **multi-threading rate** = opportunities with 3 or more engaged contacts / total open opportunities. A deal with only one contact can die when that one person leaves or goes quiet.

## Segmentation and tiering

Segmentation sorts accounts into groups by how they should be served (motion, pricing, channel). Tiering ranks accounts inside a group by how much effort each one deserves.

A simple tier score: `tier_score = fit_score x (1 + timing_score)`. Fit is a number from 0 to 1 based on what the company is and what it runs. Timing is a number from 0 to 1 based on recent changes and engagement.

| Tier | Rule (example thresholds) | Treatment | Cost per account |
|---|---|---|---|
| A | High fit and an active trigger | Account research, multi-threaded outreach, rep-written first touch, calling | High |
| B | High fit, no current trigger, or medium fit with a trigger | Signal-based sequence, templated personalization, watch for triggers | Medium |
| C | Medium or low fit, no trigger | Marketing nurture, no rep time | Low |

Check the tiers against real results. Win rate, ACV and sales cycle length should be clearly different from tier to tier. If tier A and tier B win at the same rate, the score is not measuring anything.

## Positioning

Positioning is the context that makes the product's value obvious to a specific buyer. A common structure, from April Dunford's *Obviously Awesome*, has five parts:

1. **Competitive alternatives**: what the buyer would do without you (often a spreadsheet, or nothing).
2. **Unique attributes**: what you can do that the alternatives cannot.
3. **Value**: the business result those attributes produce.
4. **Target customers**: who cares most about that value (this should match the ICP).
5. **Market category**: the frame that tells the buyer how to judge you.

Signs that positioning is wrong: win rate drops when a certain competitor shows up, discounts get deeper, or most losses are marked "no decision." You only see these patterns if loss reasons are recorded in a consistent way and calls are reviewed. So it is a data problem before it is a messaging problem.

## Pricing models

| Model | Charges for | Works when | Risk | System requirement |
|---|---|---|---|---|
| Per seat | Named or active users | Value scales with people using it | Customers ration seats, expansion stalls | Seat counts synced from product to billing and CRM |
| Usage-based | Consumption (records, calls, API requests) | Value scales with volume | Revenue volatility, hard to forecast | Metering pipeline, usage alerts to account owners |
| Flat | One price for the product | Simple product, SMB, self-serve | Leaves money on the table with large accounts | Minimal |
| Tiered | Packages with feature or volume limits | Clear segments with different needs | Packaging drift, too many tiers | Entitlements mapped to plan, upgrade triggers |
| Per territory or location | Each site, region or service area | Multi-location businesses, field operations | Location counts are hard to verify | Location data per account, identity resolution across sites |

A few terms from the table: an API request is one system asking another for data. Metering means counting how much each customer uses. Entitlements are the features each plan includes. Identity resolution means working out which records are the same company or person.

Whatever you charge for becomes something the system must track. Per-location pricing only works if the system knows how many locations each account has.

## Unit economics

Unit economics answers one question: do we make more from a customer than it cost to win them? Calculate each formula below for each segment and each channel, not only for the whole company.

ARPA means average revenue per account. Churn rate is the share of customers who leave in a period. LTV means lifetime value: the total gross profit a customer brings in before they leave.

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

Example: fully loaded CAC of $9,000, monthly ARPA of $1,500, gross margin 80%. Payback = 9,000 / (1,500 x 0.80) = 7.5 months. Annual churn of 15% gives LTV = (18,000 x 0.80) / 0.15 = $96,000 and LTV:CAC of about 10.7.

Sales velocity shows which lever to pull. With 40 open opportunities, 25% win rate, $18,000 ACV and a 60-day cycle, velocity = (40 x 0.25 x 18,000) / 60 = $3,000 per day. Cutting the cycle to 45 days raises it to $4,000 per day without a single new opportunity.

## Territory planning

Balance territories by how much revenue they could produce, not by how many accounts they hold. Two territories with 400 accounts each can differ in value several times over.

`territory_potential = sum over accounts of (estimated contract value x probability of fit)`

| Territory | Accounts | Avg estimated contract value | Avg fit probability | Potential |
|---|---|---|---|---|
| North | 400 | $12,000 | 0.30 | $1.44M |
| South | 400 | $26,000 | 0.45 | $4.68M |

Same number of accounts, but South is worth about 3x more. Reps in North will miss quota for reasons that have nothing to do with skill, and quota results will mislead hiring decisions. Move accounts around until each rep's potential falls within an agreed range. Then check travel time or time zones for field and calling teams.

Good territory design needs clean location data and a clear parent-to-site structure (which locations belong to which parent company). That is why it is built on the data model in [GTM ontology](../../projects/gtm-ontology/README.md).

## Start from the company's revenue target

Before any funnel math, break the company's annual or quarterly number into two parts: what existing customers will bring, and what new customers must bring. This covers both sides of the bowtie (the revenue model in [section 02](../02-revenue-bowtie/README.md)). New-customer pipeline only has to cover what is left after the existing base does its part.

ARR means annual recurring revenue. NRR means net revenue retention: this year's revenue from last year's customers, divided by what they paid last year. Above 100% means existing customers grew their spend more than others cut or left.

```
ending ARR target   = starting ARR x NRR + new-logo ARR
new-logo ARR needed = ending ARR target - (starting ARR x NRR)
```

**Example.** Starting ARR $8M, target $10M.

| Scenario | Base after NRR | New-logo ARR needed | Deals at $40K ACV | Opportunities at 25% win | Meetings at 60% meeting-to-opp |
|---|---|---|---|---|---|
| NRR 105% | $8.4M | $1.6M | 40 | 160 | about 267 |
| NRR 110% | $8.8M | $1.2M | 30 | 120 | 200 |

Five points of NRR remove 40 opportunities and about 67 held meetings from the outbound plan. So the first question is not "how do we get more pipeline?" It is "which lever closes the gap at the lowest cost?" The options are retention, expansion, conversion rates, or more volume at the top of the funnel. Usually one or two are worth funding, and that decides what gets built.

Then check the target against real capacity. How many ICP accounts exist (SAM)? How many accounts and calls can reps actually work? What conversion rates do we actually see? The gap between what the target needs and what capacity supports is where the systems work belongs. If no lever can close the gap, the target is the problem. The right output then is that analysis, not more automation.

## Conversion economics: working backward from a revenue target

For the new-customer part of the target, start at the revenue number and divide by each conversion rate. That tells you how much activity you need at the top of the funnel. Then compare the result to the SAM. This is the fastest way to find out whether a plan is possible.

Target: $600,000 in new ARR from outbound in one year, $18,000 ACV, using the SAM of 4,800 accounts from the TAM example.

| Step | Rate | Required volume |
|---|---|---|
| New ARR target | | $600,000 |
| Closed-won deals | $600,000 / $18,000 ACV | 34 |
| Qualified opportunities | 25% win rate | 136 |
| Meetings held | 60% meeting-to-opportunity | 227 |
| Meetings booked | 80% show rate | 284 |
| Positive replies | 50% positive reply to booked meeting | 568 |
| Contacts reached | 2% positive reply rate | 28,400 |
| Accounts touched | 3 contacts per account | 9,467 |

The plan needs 9,467 account touches, but the SAM has only 4,800 accounts. Each account would get contacted about twice a year. That can work, but it risks wearing out the list and hurting the sending domain's reputation (how email providers judge whether your mail is spam). The levers, usually cheapest first:

1. **Raise the positive reply rate** by targeting accounts with a recent trigger, and accounts that look like past wins. Going from 2% to 3% cuts the contacts you need by a third. See the [lookalike model](../../projects/lookalike-model/README.md).
2. **Raise ACV** by focusing on larger accounts inside the SAM.
3. **Add channels** (calling, partner referrals, inbound) so outbound does not carry the whole target.
4. **Expand the SAM** by adding a region or segment. This changes the ICP, so test it first.

Build this table as a live model that pulls real rates from the CRM and the email sequencer. When a rate changes, the required volume updates, and the team sees the gap before the quarter ends.

## Related

- [GTM motions](gtm-motions.md)
- [Revenue bowtie](../02-revenue-bowtie/README.md)
- [Revenue bowtie stages](../02-revenue-bowtie/stages.md)
- [Data architecture](../03-data-architecture/README.md)
- [Analytics and prediction](../06-analytics-and-prediction/README.md)
- [Product marketing and growth](../08-product-marketing-and-growth/README.md)
- [RouteHero](../../projects/routehero/README.md)
- [GTM ontology](../../projects/gtm-ontology/README.md)
- [Engineering method](../../README.md)
