# GTM motions

A go-to-market (GTM) motion is the repeatable path a buyer takes from first contact to signed contract, plus the costs that path brings with it. This page compares the common motions. For each one it gives the numbers that show whether it is working, and it shows where systems connect one motion to the next.

Most companies run two or more motions at once. Most lost revenue happens at the handoffs between them.

## Comparison

ACV means annual contract value. The ACV and sales cycle ranges below are rough planning ranges, not industry benchmarks. Replace them with your own won-deal data.

| Motion | ACV range | Sales cycle | Buyers | Primary channels | Unit-economics constraint | What engineering connects |
|---|---|---|---|---|---|---|
| SMB acquisition | Under $15k | Days to 4 weeks | Owner or single manager | Outbound email, calling, paid search, marketplaces | CAC must stay low, so rep time per deal is capped | List building at volume, routing, sequencer to CRM sync |
| Mid-market | $15k to $100k | 1 to 4 months | 2 to 5 people, department head as economic buyer | Outbound, inbound, events, partners | Rep capacity: each AE carries a limited number of active deals | Tiering, multi-threading data, stage hygiene |
| Enterprise | Over $100k | 4 to 12+ months | Committee including procurement, security, legal | Account-based outbound, executive relationships, partners | Long cycles tie up capital and headcount before revenue | Account hierarchies, buying committee mapping, mutual action plans |
| Self-serve | Under $5k, often monthly | Minutes to days | Individual user with a card | Product, SEO, content, app marketplaces | No human touch is affordable per account | Product analytics, billing events, lifecycle email |
| Product-led growth (PLG) | Starts low, expands with usage | Free to paid is days to months | User first, then team lead, then buyer | Product, word of mouth, templates, integrations | Free users cost infrastructure and support without revenue | Usage tracking, PQL scoring, product-to-CRM sync |
| Sales-assisted conversion | Mid-range, often $5k to $50k | Weeks | User already in product plus a buyer | Product signals routed to sales | Sales time must go only to accounts likely to convert | PQL routing, account matching, alert context for reps |
| Sales-led | Mid-market to enterprise | Months | Committee | Outbound, inbound demo requests, partners | Pipeline coverage and win rate decide the cost of each closed deal | Forecasting, conversation intelligence, CRM data quality |

Terms used in the table: SMB is small and mid-sized business. CAC is customer acquisition cost. AE is account executive. CRM is the customer relationship management system (such as Salesforce or HubSpot). A sequencer is the tool that sends a series of outreach emails. A PQL (product-qualified lead) is a user or account whose product usage suggests they are ready to talk to sales. SEO is search engine optimization.

## SMB acquisition

Many deals, small contract values, short cycles. The business problem is the cost of each closed deal. Picture a rep who spends three hours on each $6,000 deal and closes one in four. That rep has spent twelve hours per customer before onboarding even starts.

**Metrics**

| Metric | Formula |
|---|---|
| Cost per meeting | Channel cost (data + tools + rep time) / meetings held |
| Meeting-to-close rate | Closed-won / meetings held |
| CAC payback (months) | CAC / (monthly ARPA x gross margin %) |
| Speed to lead | Median of (first rep touch time - inbound timestamp) |
| Early churn | Customers churned in first 90 days / customers acquired in the cohort |

ARPA means average revenue per account. A cohort is a group of customers who signed up in the same period.

**Engineering connection:** build prospect lists automatically from public sources. Route leads with fixed rules written in plain code. Write email activity from the sequencer back into the CRM. Hand closed deals to onboarding without the rep typing anything in. Customers who leave in the first 90 days feed back into the ICP (ideal customer profile), so the list stops including accounts like them.

## Mid-market

The business problem is rep capacity. An AE can only run so many active deals at once. Every weak opportunity takes a slot a strong one could have used.

**Metrics**

| Metric | Formula |
|---|---|
| Win rate by tier | Closed-won in tier / closed (won + lost) in tier |
| Stage conversion | Opportunities entering stage N+1 / opportunities entering stage N |
| Pipeline coverage | Open qualified pipeline / remaining quota |
| Multi-threading rate | Opportunities with 3+ engaged contacts / open opportunities |
| Sales velocity | (Opportunities x win rate x ACV) / cycle length |

**Engineering connection:** A/B/C tiering decides which accounts get AE time. The CRM enforces clear rules for when a deal can move to the next stage. Contact research fills in the rest of the buying group before a deal depends on a single person.

## Enterprise

The business problem is risk over a long cycle. A deal can be lost late to procurement, a security review or a reorganization. Every month of sales cycle is another month of salary with no revenue.

**Metrics**

| Metric | Formula |
|---|---|
| Cycle length by stage | Median days in each stage for won deals vs lost deals |
| Committee coverage | Mapped buying roles engaged / required buying roles |
| Late-stage slip rate | Deals whose close date moved out of the quarter / deals forecast to close in the quarter |
| Forecast accuracy | 1 - abs(forecast - actual) / actual |
| Account penetration | Business units or sites under contract / total business units or sites |

**Engineering connection:** store how accounts relate to each other (parent company, subsidiary, site) so you can measure how much of each customer you have won. Link buying-group contacts to each opportunity. Review calls for security, legal and budget-timing concerns and record them in the CRM, before they turn into late surprises.

## Self-serve

The business problem is turning users into paying customers with no human contact, while keeping hosting and support costs below revenue.

**Metrics**

| Metric | Formula |
|---|---|
| Visitor-to-signup rate | Signups / unique visitors |
| Activation rate | Signups reaching the activation event within N days / signups |
| Free-to-paid conversion | Paid conversions in cohort / signups in cohort |
| Month-1 revenue retention | Revenue from cohort in month 2 / revenue from cohort in month 1 |
| Payback (months) | Acquisition cost per paid user / (monthly revenue per paid user x gross margin %) |

The activation event is the first action that shows a user got real value from the product.

**Engineering connection:** agree on one definition of "activated." Connect billing records to product usage records. Send lifecycle emails based on what the user has done in the product, not on a fixed calendar.

## Product-led growth

PLG uses the product itself as the main way to win customers. The business problem is spotting which free or low-tier accounts are worth a sales conversation. Most of the revenue comes from a small share of accounts.

**Metrics**

| Metric | Formula |
|---|---|
| Activation rate | Accounts reaching activation event / new accounts |
| Product-qualified account (PQA) rate | Accounts meeting PQL criteria / active accounts |
| Team expansion | Accounts with 2+ active users / accounts with 1+ active user |
| Natural rate of growth (approximate) | Share of new ARR from self-serve or product-sourced accounts |
| Net revenue retention | (Starting ARR + expansion - contraction - churn) / starting ARR |

ARR is annual recurring revenue. Contraction is customers cutting their spend. Churn is customers leaving.

**Engineering connection:** product usage data flows into the data warehouse (the central database that holds a copy of all company data). Each user is matched to their company by email domain and workspace. Each company is then scored on fit plus usage. The matching step is the hard part. People who sign up with personal email, and companies with several workspaces, break simple matching.

## Sales-assisted conversion

This is the bridge between product-led or self-serve and sales. A rep contacts an account that already uses the product, usually to move it to a team plan or an annual contract. The business problem is accuracy. If reps get too many weak alerts, they ignore all of them.

**Metrics**

| Metric | Formula |
|---|---|
| PQL-to-opportunity rate | Opportunities created from PQLs / PQLs routed |
| PQL-to-close rate | Closed-won from PQLs / PQLs routed |
| Alert precision | PQLs that became opportunities / PQLs routed (track per scoring version) |
| Time to first touch | Median of (rep first touch - PQL timestamp) |
| Revenue uplift | ARR of converted PQL accounts after conversion - ARR before |

**Engineering connection, PQL routing:**

The flow below reads left to right. Usage data goes into the warehouse. Users are matched to accounts. Each account gets a fit score and a usage score. If both pass the rule, the account's details are copied back into the CRM ("reverse ETL" means sending data from the warehouse back into a working tool). Then the alert goes to the right person.

```text
product events -> warehouse -> user-to-account resolution -> fit score (ICP) + usage score
  -> PQL rule (fit >= threshold AND usage event in last 7 days)
  -> reverse ETL to CRM (account owner, score, top usage events)
  -> route: owned account -> owner alert; unowned + tier A -> AE queue; tier C -> stay self-serve
```

The alert should say why it fired: which actions, which users, which plan limits they hit. Then the rep can open with real context instead of a generic check-in.

## Sales-led

The rep runs the process from first meeting to signature. The business problem is predictability. Leadership needs to know how much pipeline will close, and when.

**Metrics**

| Metric | Formula |
|---|---|
| Pipeline created | Sum of qualified opportunity value created in period |
| Win rate (by value) | Closed-won value / closed (won + lost) value |
| Sales cycle | Median days from opportunity creation to close for won deals |
| Forecast accuracy | 1 - abs(forecast - actual) / actual |
| Quota attainment distribution | Share of reps at 0-50%, 50-100%, 100%+ of quota |

**Engineering connection:** define each deal stage with clear exit rules. Record loss reasons from a fixed list. Use call-analysis software (conversation intelligence) to pull objections, competitors and timing from calls into CRM fields. Then forecasts rest on what buyers actually said, not on how a rep feels about the deal.

## Where GTM engineering connects motions

| Handoff | From | To | What breaks without engineering | System that fixes it |
|---|---|---|---|---|
| PQL routing | Product (PLG, self-serve) | Sales-assisted | Reps never see usage, or see all of it | Usage scoring and routing to account owner |
| Lead to account matching | Inbound form | Owning rep | Duplicate outreach, wrong rep, slow response | Identity resolution and owner lookup |
| Outbound to inbound | Sequencer | Marketing automation | Same contact gets a cold email and a nurture email the same day | Shared suppression and contact status |
| Closed-won to onboarding | Sales | Customer success | Scope and promises lost, slower time to value | Structured handoff record created at close |
| Usage to expansion | Product | Account management | Seat limits hit with nobody notified | Plan-limit alerts tied to renewal and expansion owners |
| Churn signal to retention | Support, calls, product | Customer success | Risk found after the cancellation notice | Risk scoring with lead time before renewal date |
| SMB to mid-market upgrade | Self-serve billing | AE | Growing accounts stay on a low plan | Fit re-scoring as firmographics change |

Identity resolution means working out which records are the same company or person. Suppression means a shared do-not-contact list. Firmographics are basic company facts such as industry and size.

The common thread is one shared record of each account across the product, CRM, billing and support tools. Without it, each team improves its own funnel, and revenue leaks at the handoffs.

## Related

- [GTM foundations](README.md)
- [Revenue bowtie](../02-revenue-bowtie/README.md)
- [Revenue bowtie stages](../02-revenue-bowtie/stages.md)
- [Data architecture](../03-data-architecture/README.md)
- [GTM engineering](../04-gtm-engineering/README.md)
- [Analytics and prediction](../06-analytics-and-prediction/README.md)
- [GTM ontology](../../projects/gtm-ontology/README.md)
- [Conversation intelligence](../../projects/conversation-intelligence/README.md)
