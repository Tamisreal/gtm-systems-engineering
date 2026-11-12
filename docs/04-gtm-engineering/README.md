# GTM engineering

GTM engineering is the work of turning revenue strategy into systems that run every day: enrichment, signals, scoring, routing, orchestration and the CRM automation that connects them. The job is less about any single tool and more about making each step measurable, explainable and cheap enough to run at volume. This page covers the main building blocks, how to implement them, and how to tell whether they are working.

## Governing principle: deterministic code first, LLM last

Use code for anything that can be expressed as a rule, a lookup or a formula. Use an LLM only where the input is language or the category is ambiguous: reading a job post, classifying a website into an industry, summarizing a call. Scores, routing decisions and CRM writes come from code, not from a model. This keeps decisions reproducible, auditable and cheap, and it means a model change cannot silently reassign a territory.

| Task | Use | Why |
|---|---|---|
| Normalize a domain or phone | Code | Exact rules exist |
| Detect a funding round from a structured feed | Code | Field lookup |
| Extract "new CRO started in March" from a press release | LLM with structured output | Language |
| Classify a company with a vague website into an ICP segment | LLM, then code validates against allowed values | Ambiguity |
| Compute account score and tier | Code | Must be explainable and stable |
| Assign an owner | Code | Must be auditable |
| Draft a first-line personalization | LLM, human or rules gate before send | Language; irreversible action |

## Enrichment

Enrichment fills missing firmographic and contact data (industry, headcount, tech stack, verified email, direct phone) from external providers.

**Waterfall enrichment** queries providers in sequence and stops at the first acceptable result. Order providers by expected cost per found record, not by list price per lookup:

```
cost_per_found(provider) = price_per_lookup / hit_rate
cost_per_verified_contact = total_enrichment_spend / verified_contacts
```

A provider charging twice as much per lookup can be cheaper per found record if its hit rate on your segment is more than twice as high. Hit rate varies by segment (enterprise SaaS vs local service businesses), so measure it per segment on a sample before fixing the order.

Implementation pattern:

1. Normalize the input (domain, name, location) and check the cache first.
2. Call providers in order; validate each result (email verification status, phone parse, title match) before accepting it.
3. Store the winning value with `source`, `fetched_at` and `confidence`; store misses too, so you do not pay to ask again tomorrow.
4. Set a re-enrichment interval per field (titles change faster than headquarters).

| Metric | Formula |
|---|---|
| Coverage | records with a verified value / records attempted |
| Incremental coverage of provider N | records found by N that earlier providers missed / records attempted |
| Cost per verified contact | total spend / verified contacts |
| Bounce rate on enriched emails | bounces / sends to enriched addresses |

Drop a provider when its incremental coverage no longer justifies its cost. Check data licensing before writing provider data to a shared store; see [governance](../07-governance-and-operations/README.md#data-licensing). Tools: Clay for waterfall orchestration, direct provider APIs for high volume, a cache table in Postgres or the warehouse.

## Buying signals

A buying signal is an observable event that raises the probability an account will buy in the near term.

| Signal | Type | Source examples | Typical reason it matters |
|---|---|---|---|
| New leader in role (VP Sales, CRO, CIO) | Third-party | LinkedIn job changes, press releases | New leaders re-evaluate tools and vendors |
| Hiring surge in a function | Third-party | Job boards, careers pages | Team growth creates process and tooling needs |
| Tech-stack change | Third-party | Technographic vendors, site script detection | Adopting or dropping an adjacent tool |
| Funding round | Third-party | Funding databases, press | New budget, growth targets |
| Pricing-page visits, repeat visits | First-party | Web analytics, reverse IP | Active evaluation |
| Product usage spike or seat cap hit | First-party | Product database | Expansion readiness |
| Competitor's pricing-page change | Third-party | Page-change monitoring | Possible churn trigger for their customers |

First-party signals (your website, product, email engagement) are cheaper and usually stronger but limited to accounts that already know you. Third-party signals reach net-new accounts but are noisier and shared with every competitor buying the same feed.

**Signal decay.** A signal's value falls with age. Model it explicitly:

```
signal_weight(t) = base_weight * 0.5 ** (days_since_observed / half_life_days)
```

Half-lives are assumptions to test, not facts: a pricing-page visit may be stale in days, a new executive hire may matter for a few months. Fit them from data once you have outcomes: compare meeting rate by signal age bucket.

What goes wrong: counting the same event from two feeds twice (dedupe on account + signal type + window), stale signals triggering outreach, and signals that correlate with nothing. Test each signal with a holdout before it gets a weight. See [the GTM learning engine](../../projects/gtm-learning-engine/README.md).

## Account scoring vs lead scoring

| Dimension | Question | Inputs | Changes |
|---|---|---|---|
| Fit | Should this account ever buy? | Industry, size, geography, tech stack, business model | Slowly |
| Intent | Is it in market now? | Third-party signals, research activity | Weeks |
| Engagement | Is it engaging with us? | Web visits, email replies, meetings, product usage | Days |

Lead scoring rates individual people, which made sense when one person filled one form. B2B purchases involve a buying group, so account scoring (fit + intent + aggregated engagement across contacts) is usually the better unit for prioritization, with person-level scoring kept for choosing who to contact within the account.

**Explainable, factor-based scoring.** Each factor contributes points, and the contributions are stored, not only the total. A rep should be able to see "62 = industry match 20 + size band 15 + hiring surge 18 + pricing visits 9".

```python
FACTORS = {
    "industry_match":  lambda a: 20 if a.industry in ICP_INDUSTRIES else 0,
    "size_band":       lambda a: {"50-199": 15, "200-999": 20}.get(a.size_band, 0),
    "hiring_surge":    lambda a: round(18 * a.hiring_signal_weight),
    "pricing_visits":  lambda a: min(a.pricing_visits_14d * 3, 12),
}

def score(account):
    contributions = {name: fn(account) for name, fn in FACTORS.items()}
    return sum(contributions.values()), contributions   # persist both
```

Weights above are illustrative. Start with weights a team can reason about, then calibrate against outcomes (logistic regression on historical opportunities is a reasonable second step; keep the output in points so it stays explainable).

**Tier thresholds come from the measured distribution.** Do not pick "A = 80+" by intuition; scores cluster, and an intuitive cut can put 2 percent or 40 percent of accounts in Tier A. Pick tiers by capacity and percentile:

```sql
SELECT
  percentile_cont(0.90) WITHIN GROUP (ORDER BY score) AS tier_a_min,
  percentile_cont(0.70) WITHIN GROUP (ORDER BY score) AS tier_b_min
FROM account_score
WHERE scored_at = (SELECT MAX(scored_at) FROM account_score);
```

If reps can work 300 Tier A accounts and the universe is 3,000, the top decile is the right cut. Then validate: conversion to opportunity should fall monotonically from Tier A to C. If it does not, the factors are wrong, not the thresholds. [RouteHero](../../projects/routehero/README.md) applies this pattern to local business locations.

## Territory intelligence

Territory design assigns accounts to reps so each territory has comparable potential and workable travel or coverage. For field sales and location-based businesses, this is a geospatial problem.

- **Radius queries:** all target locations within N km of a rep's base.
- **Polygon queries:** all locations inside a drawn territory, a ZIP or county boundary, or a drive-time isochrone.

```sql
-- PostGIS: Tier A locations within 40 km of a rep's base
SELECT l.id, l.name, l.score
FROM location l
WHERE l.tier = 'A'
  AND ST_DWithin(l.geog, ST_MakePoint(:lon, :lat)::geography, 40000);

-- Locations inside a territory polygon
SELECT l.id FROM location l JOIN territory t ON ST_Contains(t.geom, l.geom) WHERE t.id = :territory_id;
```

**Balancing by potential, not count.** Two territories with 500 accounts each are not equal if one holds most of the high-score accounts.

```
territory_potential = sum(score_i * expected_value_i) for accounts in territory
imbalance = max(potential) / min(potential)
```

Rebalance until imbalance is within an agreed tolerance, subject to constraints (existing relationships stay with their owner, travel time caps). What goes wrong: geocoding errors placing locations in the wrong state, moving accounts mid-deal, and territories that look balanced on paper but ignore rep capacity. Measure with pipeline per territory and quota attainment spread after one or two quarters.

## Campaign orchestration

Orchestration coordinates which accounts get which touches, in which channel, in what order, without collisions.

Rules that prevent most problems:

- One active outbound motion per contact at a time; check enrollment across tools, not only within one sequencer.
- Suppression check immediately before every send, not only at list build: customers, open opportunities, recent opt-outs, competitors, do-not-contact.
- Every campaign has an experiment design: hypothesis, primary metric, holdout or comparison group, sample size and stop date.
- Every touch is logged to the CRM with a campaign id so Layer 5 attribution works.

Tools: sequencers (Salesloft, Outreach, Instantly) execute; an orchestration layer (n8n, Workato or code) decides who enters and when.

## CRM automation

Good candidates: field stamping (first-touch date, stage-entry dates), lead-to-account matching, task creation on signals, data hygiene jobs. Poor candidates: anything a rep must understand but cannot see the logic of.

Keep automation in as few places as possible. When Salesforce Flow, Apex, a managed package and an external workflow all update `Account.OwnerId`, nobody can explain an owner change. Maintain an inventory: automation name, trigger, fields written, owner, last reviewed.

## Sales routing

| Method | How it works | Fits | Risks |
|---|---|---|---|
| Round robin | Next rep in rotation, optionally weighted by capacity | Inbound SMB, homogeneous reps | Ignores existing relationships and expertise |
| Territory | Assign by geography, segment or industry | Field sales, specialized segments | Uneven load if territories are unbalanced |
| Account-based | Route to the existing account owner | Any motion with named accounts | Requires good lead-to-account matching |

Most mature setups combine them: if the account has an owner, route there; else apply territory rules; else round robin within the matched pool. Skip reps who are out of office or at capacity, and log the rule that fired.

**SLA and speed to lead.**

```
speed_to_lead = first_human_touch_at - lead_created_at
sla_attainment = leads touched within SLA / leads routed
```

Measure the median and the 90th percentile; a good median can hide a tail of leads nobody called. Alert on breaches while they can still be fixed, not in a weekly report.

## Opportunity management

Stages are useful only if each has exit criteria that can be checked.

| Stage | Exit criteria (example) |
|---|---|
| Discovery | Pain confirmed, buying group identified, next meeting booked |
| Evaluation | Success criteria agreed, technical contact engaged, demo or trial done |
| Proposal | Pricing delivered, economic buyer has seen it, decision date set |
| Negotiation | Legal or procurement engaged, redlines in progress |
| Closed won / lost | Signed, or loss reason recorded from a fixed list |

Enforce with validation rules (required fields per stage) and stamp stage-entry dates so you can compute stage conversion and velocity. Watch for stage skipping and opportunities parked past a threshold age in one stage.

## Customer health scoring

Health predicts retention and expansion. Build it like account scoring: explainable factors, stored contributions.

| Factor | Example measure |
|---|---|
| Usage | Active users / licensed seats, trend over 30 days |
| Adoption depth | Number of core features used |
| Support | Open high-severity tickets, ticket trend |
| Relationship | Executive sponsor engaged in last 90 days |
| Commercial | Days to renewal, payment issues |

Validate the score by checking that lower health bands churn at higher rates on historical data. If they do not, the factors need work before anyone acts on the score.

## Expansion intelligence

Whitespace is the revenue available inside existing customers.

```
whitespace(account) = sum over products not owned of (product_fit(account, product) * list_value(product, account_size))
```

`product_fit` comes from the same factor approach: does the account's profile and usage pattern match customers who bought that product? Rank accounts by whitespace times health (unhealthy accounts are retention conversations, not upsell ones). Route the result to account managers with the reasons attached. Measure expansion pipeline created and win rate on whitespace-sourced opportunities against a comparison group.

## Workflow observability

Every automated workflow should write a run log.

```sql
CREATE TABLE workflow_run (
  id            bigserial PRIMARY KEY,
  workflow      text NOT NULL,
  started_at    timestamptz NOT NULL,
  finished_at   timestamptz,
  status        text NOT NULL,          -- success | failed | partial
  records_in    int,
  records_out   int,
  error         text,
  cost_usd      numeric(10,4),          -- enrichment + LLM + API spend for this run
  trigger_ref   text                    -- event id or schedule
);
```

| Metric | Formula | Alert when |
|---|---|---|
| Success rate | successful runs / total runs | Below target for the day |
| Silence | time since last successful run | Exceeds expected interval |
| Cost per run | sum(cost_usd) / runs | Jumps versus trailing average |
| Cost per outcome | spend / meetings or opportunities created | Trends up over weeks |
| Yield | records_out / records_in | Drops sharply (often an upstream schema change) |

Alert on silence, not only on errors: a webhook that stops arriving produces no failures.

## How to test GTM systems

- Unit-test scoring and routing rules with fixture accounts whose correct outcome is known.
- Replay last week's events through a changed workflow in a staging environment and diff the decisions.
- Use a Salesforce sandbox or HubSpot test portal for CRM writes; never test sends against real prospects.
- For LLM steps, keep a labeled evaluation set and run it on every prompt or model change. See [AI evaluation](../../projects/ai-evaluation/README.md).

## What would change the approach

- Low volume, high deal value: fewer automations, more research per account; scoring matters less than account selection.
- High-velocity inbound: speed to lead and routing dominate; invest there first.
- Product-led motion: first-party usage signals outweigh third-party intent.
- Thin budget: cut enrichment depth and keep public-data qualification first; enrich only accounts that pass fit.

## Related

- [Lookalike and propensity model](../../projects/lookalike-model/README.md): learned ICP, time-based evaluation, leakage trap, outreach handoff with holdout
- [Data architecture](../03-data-architecture/README.md)
- [Architecture layers](../03-data-architecture/architecture-layers.md)
- [Revenue bowtie](../02-revenue-bowtie/README.md)
- [AI and agents](../05-ai-and-agents/README.md)
- [Analytics and prediction](../06-analytics-and-prediction/README.md)
- [Governance and operations](../07-governance-and-operations/README.md)
- [GTM learning engine project](../../projects/gtm-learning-engine/README.md)
- [RouteHero project](../../projects/routehero/README.md)
- [Conversation intelligence project](../../projects/conversation-intelligence/README.md)
- [Decision examples](../../decision-examples/README.md)
