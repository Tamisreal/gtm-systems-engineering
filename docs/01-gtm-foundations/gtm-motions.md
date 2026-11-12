# GTM motions

A GTM motion is the repeatable path a buyer takes from first contact to signed contract, and the cost structure that path implies. This page compares the common motions, gives the metrics and formulas that tell you whether each one is working, and shows where GTM engineering connects them. Most companies run two or more motions at once, and most revenue leakage happens at the handoffs between them.

## Comparison

ACV and cycle ranges below are **illustrative planning ranges**, not benchmarks. Your own closed-won data should replace them.

| Motion | ACV range (illustrative) | Sales cycle (illustrative) | Buyers | Primary channels | Unit-economics constraint | What engineering connects |
|---|---|---|---|---|---|---|
| SMB acquisition | Under $15k | Days to 4 weeks | Owner or single manager | Outbound email, calling, paid search, marketplaces | CAC must stay low, so rep time per deal is capped | List building at volume, routing, sequencer to CRM sync |
| Mid-market | $15k to $100k | 1 to 4 months | 2 to 5 people, department head as economic buyer | Outbound, inbound, events, partners | Rep capacity: each AE carries a limited number of active deals | Tiering, multi-threading data, stage hygiene |
| Enterprise | Over $100k | 4 to 12+ months | Committee including procurement, security, legal | Account-based outbound, executive relationships, partners | Long cycles tie up capital and headcount before revenue | Account hierarchies, buying committee mapping, mutual action plans |
| Self-serve | Under $5k, often monthly | Minutes to days | Individual user with a card | Product, SEO, content, app marketplaces | No human touch is affordable per account | Product analytics, billing events, lifecycle email |
| Product-led growth (PLG) | Starts low, expands with usage | Free to paid is days to months | User first, then team lead, then buyer | Product, word of mouth, templates, integrations | Free users cost infrastructure and support without revenue | Usage tracking, PQL scoring, product-to-CRM sync |
| Sales-assisted conversion | Mid-range, often $5k to $50k | Weeks | User already in product plus a buyer | Product signals routed to sales | Sales time must go only to accounts likely to convert | PQL routing, account matching, alert context for reps |
| Sales-led | Mid-market to enterprise | Months | Committee | Outbound, inbound demo requests, partners | Pipeline coverage and win rate decide the cost of each closed deal | Forecasting, conversation intelligence, CRM data quality |

## SMB acquisition

High volume, low ACV, short cycle. The business problem is cost per closed deal: a rep who spends three hours on a $6,000 deal and closes one in four has spent twelve hours per customer before onboarding.

**Metrics**

| Metric | Formula |
|---|---|
| Cost per meeting | Channel cost (data + tools + rep time) / meetings held |
| Meeting-to-close rate | Closed-won / meetings held |
| CAC payback (months) | CAC / (monthly ARPA x gross margin %) |
| Speed to lead | Median of (first rep touch time - inbound timestamp) |
| Early churn | Customers churned in first 90 days / customers acquired in the cohort |

**Engineering connection:** automated list building from public sources, deterministic routing, sequencer events written back to the CRM, and a close-to-onboarding handoff that requires no rep data entry. Early churn feeds back into ICP criteria so the list stops including accounts that leave in 90 days.

## Mid-market

The business problem is rep capacity. An AE can only run a limited number of active cycles, so every unqualified opportunity displaces a qualified one.

**Metrics**

| Metric | Formula |
|---|---|
| Win rate by tier | Closed-won in tier / closed (won + lost) in tier |
| Stage conversion | Opportunities entering stage N+1 / opportunities entering stage N |
| Pipeline coverage | Open qualified pipeline / remaining quota |
| Multi-threading rate | Opportunities with 3+ engaged contacts / open opportunities |
| Sales velocity | (Opportunities x win rate x ACV) / cycle length |

**Engineering connection:** A/B/C tiering that decides which accounts get AE time, enforced stage exit criteria in the CRM, and contact discovery that fills the buying committee before a deal is single-threaded.

## Enterprise

The business problem is risk over a long cycle. A deal can be lost late to procurement, security review or a reorganization, and each month of cycle length is a month of salary without revenue.

**Metrics**

| Metric | Formula |
|---|---|
| Cycle length by stage | Median days in each stage for won deals vs lost deals |
| Committee coverage | Mapped buying roles engaged / required buying roles |
| Late-stage slip rate | Deals whose close date moved out of the quarter / deals forecast to close in the quarter |
| Forecast accuracy | 1 - abs(forecast - actual) / actual |
| Account penetration | Business units or sites under contract / total business units or sites |

**Engineering connection:** account hierarchies (parent, subsidiary, site) so penetration can be measured, buying committee records tied to opportunities, and call analysis that pulls security, legal and budget-timing signals into the CRM before they become late surprises.

## Self-serve

The business problem is converting users with no human contact while keeping infrastructure and support costs below revenue.

**Metrics**

| Metric | Formula |
|---|---|
| Visitor-to-signup rate | Signups / unique visitors |
| Activation rate | Signups reaching the activation event within N days / signups |
| Free-to-paid conversion | Paid conversions in cohort / signups in cohort |
| Month-1 revenue retention | Revenue from cohort in month 2 / revenue from cohort in month 1 |
| Payback (months) | Acquisition cost per paid user / (monthly revenue per paid user x gross margin %) |

**Engineering connection:** a single event definition for "activated", billing events joined to product events, and lifecycle messaging triggered by product state instead of a calendar.

## Product-led growth

PLG uses the product as the primary acquisition channel. The business problem is identifying which free or low-tier accounts are worth a sales conversation, because revenue concentrates in a small share of accounts.

**Metrics**

| Metric | Formula |
|---|---|
| Activation rate | Accounts reaching activation event / new accounts |
| Product-qualified account (PQA) rate | Accounts meeting PQL criteria / active accounts |
| Team expansion | Accounts with 2+ active users / accounts with 1+ active user |
| Natural rate of growth (approximate) | Share of new ARR from self-serve or product-sourced accounts |
| Net revenue retention | (Starting ARR + expansion - contraction - churn) / starting ARR |

**Engineering connection:** product events land in the warehouse, users are resolved to accounts by email domain and workspace, and accounts are scored on fit plus usage. This identity resolution step is the hard part: personal email signups and multiple workspaces per company break naive matching.

## Sales-assisted conversion

This is the bridge between PLG or self-serve and sales. A rep engages an account already using the product, typically to move it to a team or annual plan. The business problem is precision: if reps get too many weak alerts they ignore all of them.

**Metrics**

| Metric | Formula |
|---|---|
| PQL-to-opportunity rate | Opportunities created from PQLs / PQLs routed |
| PQL-to-close rate | Closed-won from PQLs / PQLs routed |
| Alert precision | PQLs that became opportunities / PQLs routed (track per scoring version) |
| Time to first touch | Median of (rep first touch - PQL timestamp) |
| Revenue uplift | ARR of converted PQL accounts after conversion - ARR before |

**Engineering connection, PQL routing:**

```text
product events -> warehouse -> user-to-account resolution -> fit score (ICP) + usage score
  -> PQL rule (fit >= threshold AND usage event in last 7 days)
  -> reverse ETL to CRM (account owner, score, top usage events)
  -> route: owned account -> owner alert; unowned + tier A -> AE queue; tier C -> stay self-serve
```

The alert should include why it fired (which events, which users, plan limits hit), so the rep can open with context instead of a generic check-in.

## Sales-led

The rep runs the process from first meeting to signature. The business problem is predictability: leadership needs to know how much pipeline converts and when.

**Metrics**

| Metric | Formula |
|---|---|
| Pipeline created | Sum of qualified opportunity value created in period |
| Win rate (by value) | Closed-won value / closed (won + lost) value |
| Sales cycle | Median days from opportunity creation to close for won deals |
| Forecast accuracy | 1 - abs(forecast - actual) / actual |
| Quota attainment distribution | Share of reps at 0-50%, 50-100%, 100%+ of quota |

**Engineering connection:** stage definitions with exit criteria, structured loss reasons, and conversation intelligence that writes objections, competitors and timing from calls into CRM fields so forecasts rely on evidence rather than rep sentiment.

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

The common thread is a shared account identity across product, CRM, billing and support. Without it, each motion optimizes its own funnel and the handoffs leak.

## Related

- [GTM foundations](README.md)
- [Revenue bowtie](../02-revenue-bowtie/README.md)
- [Revenue bowtie stages](../02-revenue-bowtie/stages.md)
- [Data architecture](../03-data-architecture/README.md)
- [GTM engineering](../04-gtm-engineering/README.md)
- [Analytics and prediction](../06-analytics-and-prediction/README.md)
- [GTM ontology](../../projects/gtm-ontology/README.md)
- [Conversation intelligence](../../projects/conversation-intelligence/README.md)
