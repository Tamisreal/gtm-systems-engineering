# GTM engineering

GTM (go-to-market) engineering turns a revenue strategy into systems that run every day. That includes enrichment (filling in missing company and contact facts), buying signals, scoring, routing, coordinating outreach, and the CRM automation that ties them together. The CRM is the customer relationship management system, such as Salesforce or HubSpot.

The job is less about any one tool. It is about making each step measurable, easy to explain, and cheap enough to run at high volume. This page covers the main building blocks, how to build them, and how to tell whether they work.

## Governing principle: deterministic code first, LLM last

"Deterministic" code is plain code with fixed rules: the same input always gives the same answer. An LLM (large language model) is the type of AI behind ChatGPT and Claude.

Use plain code for anything you can write as a rule, a lookup or a formula. Use an LLM only when the input is human language or the category is fuzzy: reading a job post, sorting a website into an industry, summarizing a call. Scores, routing decisions and CRM updates come from code, not from AI.

This keeps decisions repeatable, checkable and cheap. It also means an AI model update cannot quietly reassign someone's territory.

| Task | Use | Why |
|---|---|---|
| Normalize a domain or phone | Code | Exact rules exist |
| Detect a funding round from a structured feed | Code | Field lookup |
| Extract "new CRO started in March" from a press release | LLM with structured output | Language |
| Classify a company with a vague website into an ICP segment | LLM, then code validates against allowed values | Ambiguity |
| Compute account score and tier | Code | Must be explainable and stable |
| Assign an owner | Code | Must be auditable |
| Draft a first-line personalization | LLM, human or rules gate before send | Language; irreversible action |

"Normalize" means cleaning a value into one standard form. "Structured output" means the AI answers in fixed fields that code can read. ICP is the ideal customer profile. "Auditable" means anyone can check afterward why it happened.

## Enrichment

Enrichment fills in missing company facts (industry, headcount, the software they use) and contact details (checked email, direct phone) from outside data providers.

**Waterfall enrichment** asks providers one at a time and stops at the first good answer. Put providers in order of what it really costs to get a result, not the sticker price per lookup:

```
cost_per_found(provider) = price_per_lookup / hit_rate
cost_per_verified_contact = total_enrichment_spend / verified_contacts
```

Hit rate is the share of lookups where the provider actually has the answer. A provider that charges twice as much per lookup can still be cheaper per result if it finds more than twice as many. Hit rates differ by segment (large software companies vs local service businesses), so test each provider on a sample from your segment before setting the order.

How to build it:

1. Clean up the input (domain, name, location) into a standard form, and check saved results first (the cache), so you never pay twice.
2. Call providers in order. Check each answer before accepting it: is the email verified, does the phone number parse, does the job title match?
3. Save the winning value with its source (`source`), when it was fetched (`fetched_at`) and how sure you are (`confidence`). Save misses too, so you do not pay to ask again tomorrow.
4. Set how often each field gets refreshed. Job titles change faster than headquarters addresses.

| Metric | Formula |
|---|---|
| Coverage | records with a verified value / records attempted |
| Incremental coverage of provider N | records found by N that earlier providers missed / records attempted |
| Cost per verified contact | total spend / verified contacts |
| Bounce rate on enriched emails | bounces / sends to enriched addresses |

Drop a provider when the extra records it finds no longer justify its cost. Check the provider's license terms before saving its data anywhere shared; see [governance](../07-governance-and-operations/README.md#data-licensing). Tools: Clay to run the waterfall, direct provider APIs (the connection points vendors offer to other software) for high volume, and a cache table in Postgres or the data warehouse (the central database that holds a copy of all company data).

## Buying signals

A buying signal is something you can observe that makes it more likely an account will buy soon.

| Signal | Type | Source examples | Typical reason it matters |
|---|---|---|---|
| New leader in role (VP Sales, CRO, CIO) | Third-party | LinkedIn job changes, press releases | New leaders re-evaluate tools and vendors |
| Hiring surge in a function | Third-party | Job boards, careers pages | Team growth creates process and tooling needs |
| Tech-stack change | Third-party | Technographic vendors, site script detection | Adopting or dropping an adjacent tool |
| Funding round | Third-party | Funding databases, press | New budget, growth targets |
| Pricing-page visits, repeat visits | First-party | Web analytics, reverse IP | Active evaluation |
| Product usage spike or seat cap hit | First-party | Product database | Expansion readiness |
| Competitor's pricing-page change | Third-party | Page-change monitoring | Possible churn trigger for their customers |

Technographic vendors track what software companies use. Reverse IP matches a website visitor's internet address to their company. Churn means a customer leaving.

First-party signals come from your own website, product and email. They are cheaper and usually stronger, but they only cover accounts that already know you. Third-party signals come from outside sources. They reach brand-new accounts, but they are noisier, and every competitor buying the same data feed sees them too.

**Signal decay.** A signal loses value as it gets older. Model that directly:

```
signal_weight(t) = base_weight * 0.5 ** (days_since_observed / half_life_days)
```

The half-life is how many days until a signal is worth half as much. Treat half-lives as guesses to test, not facts. A pricing-page visit may go stale in days. A new executive hire may matter for a few months. Once you have results, set them from data: compare meeting rates by how old the signal was.

What goes wrong: the same event counted twice because two feeds reported it (merge duplicates on account + signal type + time window), old signals triggering outreach, and signals that predict nothing. Test each signal against a holdout (a comparison group that gets no outreach) before giving it any weight. See [the GTM learning engine](../../projects/gtm-learning-engine/README.md).

## Account scoring vs lead scoring

| Dimension | Question | Inputs | Changes |
|---|---|---|---|
| Fit | Should this account ever buy? | Industry, size, geography, tech stack, business model | Slowly |
| Intent | Is it in market now? | Third-party signals, research activity | Weeks |
| Engagement | Is it engaging with us? | Web visits, email replies, meetings, product usage | Days |

Lead scoring rates individual people. That made sense when one person filled out one form. B2B purchases involve a buying group, so account scoring is usually the better way to set priorities. It combines fit, intent, and engagement added up across all contacts at the account. Person-level scoring is still useful for picking who to contact inside the account.

**Explainable, factor-based scoring.** Each factor adds points, and the points from each factor are saved, not only the total. A rep should be able to see "62 = industry match 20 + size band 15 + hiring surge 18 + pricing visits 9."

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

The weights above are a starting point. Begin with weights the team can reason about. Then tune them against real results. A reasonable second step is a simple statistical model (logistic regression) trained on past opportunities. Keep its output in points, so it stays easy to explain.

**Tier thresholds come from the measured distribution.** Do not pick "A = 80+" by gut feel. Scores bunch together, and a gut-feel cutoff can put 2 percent or 40 percent of accounts in Tier A. Set tiers by rep capacity and by percentile (where an account ranks against all the others). The query below finds the score at the top 10% and top 30% cutoffs:

```sql
SELECT
  percentile_cont(0.90) WITHIN GROUP (ORDER BY score) AS tier_a_min,
  percentile_cont(0.70) WITHIN GROUP (ORDER BY score) AS tier_b_min
FROM account_score
WHERE scored_at = (SELECT MAX(scored_at) FROM account_score);
```

If reps can work 300 Tier A accounts and there are 3,000 accounts in total, the top 10% is the right cutoff. Then check it: the rate of turning into an opportunity should drop steadily from Tier A to B to C. If it does not, the factors are wrong, not the cutoffs. [RouteHero](../../projects/routehero/README.md) applies this method to local business locations.

## Territory intelligence

Territory design assigns accounts to reps so each territory has similar potential and workable travel or coverage. For field sales and location-based businesses, this is a map problem.

- **Radius queries:** all target locations within a set distance of a rep's base.
- **Polygon queries:** all locations inside a drawn area, such as a territory, a ZIP code or county boundary, or the area reachable within a set drive time.

The queries below use PostGIS, an add-on that gives the Postgres database map and distance features. The first finds Tier A locations within 40 km of a rep. The second finds every location inside a territory's boundary.

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

Move accounts until the gap between the richest and poorest territory is within an agreed limit. Respect the constraints: existing relationships stay with their owner, and travel time has a cap.

What goes wrong: address errors that place a location in the wrong state, moving accounts in the middle of a deal, and territories that look balanced on paper but ignore how much each rep can handle. After one or two quarters, measure pipeline per territory and how widely quota results vary between reps.

## Campaign orchestration

Orchestration coordinates which accounts get which touches, in which channel, in what order, without two campaigns colliding.

Rules that prevent most problems:

- Each contact is in only one active outbound program at a time. Check across all tools, not just inside one email sequencer.
- Check the do-not-contact list right before every send, not only when the list is built. Exclude customers, open deals, recent opt-outs, competitors and anyone marked do-not-contact.
- Every campaign is set up as a test: what you expect to happen, the main number you will judge it by, a comparison group, a sample size and an end date.
- Every touch is logged in the CRM with a campaign ID, so the reporting layer (Layer 5 in the [architecture layers](../03-data-architecture/architecture-layers.md)) can credit the right campaign.

Tools: sequencers (Salesloft, Outreach, Instantly) send the messages. A separate coordinating tool (n8n, Workato or custom code) decides who goes in and when.

## CRM automation

Good things to automate: stamping dates (first-touch date, the date a deal entered each stage), matching leads to existing accounts, creating tasks when a signal fires, and routine data cleanup. Bad things to automate: anything a rep needs to understand but cannot see the logic behind.

Keep automation in as few places as possible. If Salesforce Flow, custom Salesforce code (Apex), an installed add-on and an outside workflow tool all change the account owner field, nobody can explain why an owner changed. Keep a list of every automation: its name, what triggers it, which fields it changes, who owns it, and when it was last reviewed.

## Sales routing

| Method | How it works | Fits | Risks |
|---|---|---|---|
| Round robin | Next rep in rotation, optionally weighted by capacity | Inbound SMB, homogeneous reps | Ignores existing relationships and expertise |
| Territory | Assign by geography, segment or industry | Field sales, specialized segments | Uneven load if territories are unbalanced |
| Account-based | Route to the existing account owner | Any motion with named accounts | Requires good lead-to-account matching |

SMB means small and mid-sized business. "Homogeneous reps" means reps who all handle the same kind of deal.

Most mature setups combine all three. If the account already has an owner, send it there. If not, apply territory rules. If that still leaves several reps, take turns among them. Skip reps who are out of office or at capacity, and log which rule made the decision.

**SLA and speed to lead.** An SLA (service level agreement) is an agreed deadline, such as "every inbound lead gets a human reply within 15 minutes."

```
speed_to_lead = first_human_touch_at - lead_created_at
sla_attainment = leads touched within SLA / leads routed
```

Look at the typical case (median) and the slow cases (90th percentile). A good median can hide a group of leads nobody called. Send alerts while a missed deadline can still be fixed, not in a weekly report.

## Opportunity management

Deal stages are only useful if each one has exit rules you can check.

| Stage | Exit criteria (example) |
|---|---|
| Discovery | Pain confirmed, buying group identified, next meeting booked |
| Evaluation | Success criteria agreed, technical contact engaged, demo or trial done |
| Proposal | Pricing delivered, economic buyer has seen it, decision date set |
| Negotiation | Legal or procurement engaged, redlines in progress |
| Closed won / lost | Signed, or loss reason recorded from a fixed list |

Enforce the rules in the CRM by making certain fields required at each stage. Record the date each deal enters each stage, so you can calculate how many deals move forward and how fast. Watch for deals that skip stages, and deals that sit in one stage too long.

## Customer health scoring

A health score predicts whether a customer will stay and grow. Build it like account scoring: clear factors, with each factor's points saved.

| Factor | Example measure |
|---|---|
| Usage | Active users / licensed seats, trend over 30 days |
| Adoption depth | Number of core features used |
| Support | Open high-severity tickets, ticket trend |
| Relationship | Executive sponsor engaged in last 90 days |
| Commercial | Days to renewal, payment issues |

Check the score on past data: customers with lower health should have left at higher rates. If they did not, fix the factors before anyone acts on the score.

## Expansion intelligence

Whitespace is the revenue still available inside existing customers.

```
whitespace(account) = sum over products not owned of (product_fit(account, product) * list_value(product, account_size))
```

`product_fit` uses the same factor approach as scoring: does this account's profile and usage look like customers who bought that product? Rank accounts by whitespace times health. Unhealthy accounts need a retention conversation, not an upsell. Send the results to account managers with the reasons attached. Measure the expansion pipeline created, and the win rate on these opportunities, against a comparison group.

## Workflow observability

Observability means being able to see what ran, what failed and why. Every automated workflow should write a run log, one row per run:

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

An upstream schema change means a source system renamed or restructured its data fields.

Alert on silence, not only on errors. If a webhook (a message one system sends another the moment something happens) stops arriving, nothing fails, so no error alert ever fires.

## How to test GTM systems

- Test scoring and routing rules with sample accounts whose correct result you already know.
- Run last week's activity through a changed workflow in a test environment, and compare the decisions with the old version.
- Test CRM updates in a Salesforce sandbox or a HubSpot test account. Never test sending on real prospects.
- For AI steps, keep a set of examples with known correct answers, and rerun it every time the prompt or the AI model changes. See [AI evaluation](../../projects/ai-evaluation/README.md).

## What would change the approach

- Few deals, each worth a lot: fewer automations and more research per account. Choosing the right accounts matters more than scoring.
- Lots of fast inbound leads: speed to lead and routing matter most. Invest there first.
- Product-led sales (customers find and try the product themselves): your own product usage signals matter more than outside intent data.
- Tight budget: spend less on enrichment. Qualify accounts with free public data first, and only pay to enrich accounts that pass the fit check.

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
