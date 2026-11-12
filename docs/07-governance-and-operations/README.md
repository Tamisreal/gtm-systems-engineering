# Governance and operations for GTM systems

GTM systems touch personal data, send messages on a company's behalf and write to the records that drive forecasts and compensation. That makes governance an engineering requirement, not paperwork: privacy rules, licensing terms, access control and reliability targets all shape what can be built. This page covers the operating practices that keep a GTM stack legal, trustworthy and maintainable after the person who built it moves on.

**This is not legal advice.** Privacy and marketing rules vary by jurisdiction and change over time. The summaries below are high level; confirm current requirements with counsel and the primary texts before relying on them.

## Privacy

### GDPR (EU and UK GDPR)

Processing personal data, including business contact data such as a named work email, requires a lawful basis. For B2B outreach the basis most often relied on is legitimate interest, which requires a documented balancing test (a legitimate interest assessment): the purpose, why processing is necessary for it, and whether the person's rights override it. Other obligations that shape GTM systems:

- Transparency: when data is collected from a third party rather than the person, the person must be informed about the processing within the time limits the regulation sets.
- Right to object to direct marketing: once someone objects, marketing to them must stop. Treat this as absolute.
- Data subject rights: access, rectification, erasure. Systems need a way to find every copy of a person's data, which is an identity resolution problem.
- Data minimization and retention: collect what the purpose needs and delete it when no longer needed.
- Electronic marketing rules sit alongside GDPR (the ePrivacy framework and national laws such as the UK's PECR), and the treatment of B2B email differs by country.

### CCPA / CPRA (California)

California's law gives residents rights to know, delete, correct, and opt out of the sale or sharing of personal information, with obligations on businesses that meet its thresholds. Its temporary exemption for B2B contact data has expired, so business contacts are generally in scope. Other US states have passed comparable laws with different thresholds and details.

### CAN-SPAM (US commercial email)

CAN-SPAM does not require prior opt-in for commercial email, but it does require, among other things: accurate header and sender information, non-deceptive subject lines, a valid physical postal address, a clear way to opt out, and honoring opt-outs promptly (within the deadline the law sets). The sender remains responsible when an agency or tool sends on its behalf.

### Suppression and do-not-contact handling

Most compliance failures in GTM are plumbing failures: someone opted out in one tool and was emailed from another.

| Practice | Implementation |
|---|---|
| One global suppression list | A table keyed on normalized email, domain and phone, with reason, source and timestamp |
| Check at send time | Every sequencer and workflow calls the suppression check immediately before sending, not only at list build |
| Fast propagation | Opt-out events flow through the event pipeline within minutes to every engagement tool |
| Never overwritten | Syncs and enrichment cannot clear a do-not-contact flag; only a documented process can |
| Domain-level suppression | Customers, competitors and accounts that requested no contact are suppressed by domain |
| Retain the suppression record | Keep the minimum needed to honor the request even after deleting other data |

Test it: add a test address to the suppression list, trigger every send path, and confirm none send. Run this after every new tool or workflow goes live.

## Compliance as a system property

Turn rules into checks the system runs, so compliance does not depend on memory:

- Required fields on contact creation: `source`, `lawful_basis` (where applicable), `collected_at`, `country`.
- Region-aware routing: contacts in jurisdictions with stricter email rules go to sequences built for those rules.
- Retention jobs that delete or anonymize records past their retention period, with a log of what was removed.
- A data map: which systems hold personal data, what fields, why, and who owns each. It is needed for subject access requests anyway.

## Data licensing

Many business-data sources restrict what you may do with their content. Common restrictions include: no caching beyond a short period, no storing results in your own database, no combining with other data, no redistributing to third parties, and display-only use inside the provider's own interface. Mapping and review APIs are frequent examples.

Before building a shared database or a product on top of a source, check:

| Question | Why it matters |
|---|---|
| May we store the data, and for how long? | Determines whether a cache or warehouse table is allowed |
| May we derive and keep new fields from it? | Scores and classifications may count as derived works |
| May we share it with other customers or tenants? | Multi-tenant products often violate single-licensee terms |
| Is attribution required? | Display obligations in the UI |
| What happens at contract end? | Deletion obligations can remove your history |

The [RouteHero project](../../projects/routehero/README.md) shows this evaluation in practice: it rejected Google Places and Yelp as the base for a shared location database because of storage and redistribution terms, and chose Overture Maps, an open dataset, instead. Record the decision and the terms reviewed in an architecture decision record ([decision examples](../../decision-examples/README.md)).

## Access control

| Principle | In practice |
|---|---|
| Least privilege | Integration users get only the objects and fields they write; reps see what their role needs |
| Scoped API keys | One key per integration, with the narrowest scopes the vendor offers; never a shared admin key |
| Service accounts | Integrations run as named service users, not as a person's login, so leaving staff do not break automations |
| Secret storage | Keys in a secret manager or environment store; never in code, workflow JSON exports or spreadsheets |
| Rotation | Keys rotated on a schedule and immediately when someone with access leaves |
| Periodic review | Quarterly list of users and integrations with write access to core objects; remove what is unused |

What goes wrong: an enrichment tool connected with a system administrator's credentials, which can then overwrite any field; a workflow export shared on Slack with an API key inside.

## Audit logs

Record who or what changed important data, when, from what value, and why.

```sql
CREATE TABLE audit_event (
  id           bigserial PRIMARY KEY,
  occurred_at  timestamptz NOT NULL DEFAULT now(),
  actor        text NOT NULL,          -- user id or service account
  system       text NOT NULL,          -- crm, scoring-service, router
  entity       text NOT NULL,          -- account:001...
  field        text,
  old_value    text,
  new_value    text,
  reason       text                    -- rule id, run id, or ticket
);
```

CRMs provide field history tracking on a limited number of fields; turn it on for owner, stage, amount, score tier and do-not-contact. For changes made by your own services, write to an audit table like the one above. The test: pick a random owner change from last month and explain it in under five minutes.

## Data integrity

Integrity means the data reflects reality and stays internally consistent. Controls:

- Validation at the boundary (schema, types, allowed values); see [data architecture](../03-data-architecture/README.md#data-validation).
- Referential checks: no contact roles pointing to deleted contacts, no opportunities on merged accounts.
- Reconciliation: counts and sums between source and destination match (CRM closed-won amount vs billing bookings for the same period).
- Lineage: derived fields store source and computation version, so a wrong score can be traced. See [the GTM ontology project](../../projects/gtm-ontology/README.md).

## Reliability and SLOs

Set service level objectives for workflows that affect revenue. An SLO is a target for a measurable indicator over a window.

| Workflow | Indicator | Example target (illustrative) |
|---|---|---|
| Inbound lead routing | Leads assigned within 5 minutes of creation | 99 percent over 30 days |
| Opt-out propagation | Opt-outs applied in all send tools within 15 minutes | 99.9 percent over 30 days |
| Nightly scoring job | Scores refreshed by 07:00 local | 28 of 30 days |
| CRM sync | Changes reflected in warehouse within 1 hour | 99 percent |

Error budget = 1 minus the target. If routing misses its budget, reliability work takes priority over new features in that workflow. Targets should reflect business cost: a delayed score refresh is an inconvenience; a missed opt-out is a legal and reputational problem, so its target is stricter.

## Change management

Most GTM incidents start with a change: a new flow, an edited validation rule, a re-ordered routing rule, a prompt tweak.

| Practice | Implementation |
|---|---|
| Separate environments | Salesforce sandbox or HubSpot test portal for CRM changes; staging copies of workflows for orchestration tools |
| Version control | Store code, workflow definitions, scoring weights and prompts in Git; tag what is deployed |
| Review | A second person reviews changes to routing, scoring, suppression and anything that sends messages |
| Dry runs | Run changed routing or scoring against last week's records and diff the decisions before switching over |
| Rollback plan | Know how to revert before deploying; keep the previous version runnable |
| Change log | Date, change, owner, reason and link to the review, visible to sales and marketing ops |

Freeze non-urgent changes around quarter end, when routing or scoring changes can disrupt forecasts and compensation.

## AI data handling

LLM steps add their own governance questions:

- **What data leaves your systems?** Send the minimum fields needed for the task. Strip or mask personal data that the task does not require.
- **Provider terms.** Check the provider's data retention and training policies for the API tier you use, and record them in the vendor file.
- **Output validation.** Model outputs go to a staging table, are validated against allowed values, and only then are written by code. See [AI and agents](../05-ai-and-agents/README.md).
- **Evaluation records.** Keep the labeled set, the prompt version and the score for each release, so a regression can be traced to a change. See [the AI evaluation project](../../projects/ai-evaluation/README.md).
- **Human review for irreversible actions.** Sends, merges and deletions proposed by an agent pass a human or a deterministic gate.

## Incident handling

When something breaks (a wrong mass assignment, a send to a suppressed segment, a sync that overwrote a field), the order is: stop the damage, assess scope, fix, communicate, learn.

1. **Stop:** pause the workflow or sequence. Every production workflow needs a documented kill switch.
2. **Scope:** use the audit log and run log to list affected records and people.
3. **Fix:** restore from audit `old_value`, a backup or a replay. Handle opt-outs and suppression breaches first.
4. **Communicate:** tell affected owners (reps whose accounts moved, marketing if sends went out) what happened and what was done.
5. **Learn:** a short blameless review: timeline, cause, why existing checks missed it, and one or two concrete follow-ups with owners and dates.

Track incident count and time to detect. Time to detect is usually the bigger lever: a broken workflow found in an hour affects far fewer records than one found at the monthly review.

## Retention schedule

Write down how long each data class is kept and why. Example structure (periods are placeholders to set with counsel):

| Data class | Retention | Action at expiry |
|---|---|---|
| Prospect contacts with no engagement | Set per policy | Delete or anonymize, keep suppression record |
| Customer contacts | Duration of relationship plus policy period | Review, then delete or anonymize |
| Raw webhook payloads | Short, long enough for replay and debugging | Delete |
| Enrichment cache | Per vendor terms | Delete or refresh |
| Audit logs | Per policy and legal requirements | Archive |
| Call recordings and transcripts | Per policy and consent terms | Delete |

## Observability

Observability answers "what happened, and why" without reading code.

- **Logs:** structured run logs with workflow, run id, inputs summary, outputs summary, status, duration and cost.
- **Metrics:** success rate, latency, volume, DLQ depth, spend, per workflow.
- **Alerts:** on failure, on silence (expected run did not happen), and on anomalies (volume or cost far off trailing average). Route each alert to a named owner, not a shared channel nobody watches.
- **Dashboards:** one page per layer, matching the monitors in [architecture layers](../03-data-architecture/architecture-layers.md).

## Vendor evaluation

Score vendors against weighted criteria decided before demos, so the evaluation is not driven by the best presentation.

| Criterion | Weight | What to check | Score 1 to 5 |
|---|---|---|---|
| Fit to the capability gap | 25 | Does it solve the specific problem, tested on your data? | |
| Data quality on your segment | 20 | Hit rate and accuracy on a sample of your accounts | |
| Integration | 15 | API coverage, bulk endpoints, webhooks, rate limits, CRM connector quality | |
| Licensing and compliance | 15 | Storage and redistribution terms, DPA, subprocessors, data residency | |
| Total cost | 10 | Price at current and 3x volume, overage terms, implementation effort | |
| Security | 10 | SSO, scoped keys, audit logs, security attestations | |
| Exit cost | 5 | Data export, contract length, what you lose on leaving | |

Weighted score = sum(weight x score) / 5, out of 100. Weights are examples; set them per decision. Always run a paid or free pilot on a sample of your own records; vendor-reported coverage on their benchmark set tells you little about your segment.

## Technical debt in GTM stacks

GTM debt accumulates faster than in product codebases because many people can create automation and few review it.

| Debt type | Symptom | Remedy |
|---|---|---|
| Field sprawl | Hundreds of custom fields, many unused or duplicated | Usage audit; deprecate with a date; delete after it passes |
| Automation sprawl | Multiple flows and tools writing the same field | Automation inventory; consolidate into one owner per field |
| Orphaned integrations | Tools still syncing after the contract or champion left | Integration inventory with owner and renewal date |
| Undocumented logic | Routing nobody can explain | Move rules to code or one routing tool; document each rule |
| Spreadsheet systems | Critical mappings in personal spreadsheets | Move into a governed table with an owner |

Budget a fixed share of each quarter for debt reduction, and track it with countable items (fields removed, automations consolidated).

## Documentation and runbooks

Each production workflow needs a short runbook:

```
Workflow: inbound-routing
Owner: <role, not a person's name only>  | Backup: <role>
Purpose: assign inbound leads within SLA
Trigger: CRM lead created webhook
Writes: Lead.OwnerId, Lead.Routing_Rule__c, audit_event
Depends on: CRM API, rep roster table, out-of-office calendar sync
SLO: 99 percent assigned within 5 minutes
Alerts: #gtm-alerts, paged to owner after 3 consecutive failures
Common failures and fixes:
  - Roster table stale -> rerun roster sync job
  - CRM API limit reached -> check for runaway sync; throttle bulk jobs
Replay: `replay --workflow inbound-routing --from <ts>`
```

Keep runbooks next to the code or in the same system as the workflow, and review them when the workflow changes.

## Business continuity

No GTM system should depend on one person. Practical checks:

- Every integration runs on a service account owned by the company, with credentials in a shared secret store.
- Every workflow has an owner and a backup who has run it at least once.
- Admin access to CRM, orchestration and sequencer tools is held by at least two people.
- A documented handoff exists: system inventory, field ownership matrix, runbooks, open issues, vendor contacts and renewal dates.
- Exports of configuration (flows, workflow definitions, scoring rules) are versioned, so a broken change can be rolled back.

Test continuity the simple way: have the backup owner handle the next incident or change without help, and fix whatever they could not find.

## Measuring governance

Governance is working when these numbers move in the right direction: sends to suppressed contacts (target zero), time to fulfill data subject requests, share of integrations on service accounts with scoped keys, SLO attainment per workflow, count of fields and automations without an owner, and time to explain a random data change.

## Related

- [Data architecture](../03-data-architecture/README.md)
- [Architecture layers](../03-data-architecture/architecture-layers.md)
- [Build, buy or extend](../03-data-architecture/build-buy-extend.md)
- [Technology ecosystem](../03-data-architecture/technology-ecosystem.md)
- [GTM engineering](../04-gtm-engineering/README.md)
- [AI and agents](../05-ai-and-agents/README.md)
- [RouteHero project](../../projects/routehero/README.md)
- [GTM ontology project](../../projects/gtm-ontology/README.md)
- [Decision examples](../../decision-examples/README.md)
- [IMPACT.md](../../IMPACT.md)
