# Governance and operations for GTM systems

GTM systems hold personal data, send messages in a company's name, and write to the records that drive forecasts and commissions. So governance is part of the build, not paperwork. Privacy law, data license terms, access control and reliability targets all shape what can be built. This page covers the habits that keep a GTM setup legal, trustworthy and easy to maintain after the person who built it moves on.

**This is not legal advice.** Privacy and marketing rules differ by country and state, and they change over time. The summaries below are high level. Confirm current requirements with a lawyer and the original legal texts before relying on them.

## Privacy

### GDPR (EU and UK GDPR)

GDPR is the European privacy law, with a matching UK version. Using someone's personal data, including business contact data such as a named work email, requires a legal reason ("lawful basis"). For B2B outreach, the reason most companies rely on is "legitimate interest." That requires a written balancing test, called a legitimate interest assessment: what the purpose is, why you need the data for it, and whether the person's rights outweigh your interest. Other rules that shape GTM systems:

- Telling people: when you get someone's data from a third party instead of from them, you must tell them you are using it, within the deadlines the law sets.
- Right to object to marketing: once someone objects, marketing to them must stop. Treat this as absolute.
- People's data rights: they can ask to see, correct or delete their data. Your systems need a way to find every copy of one person's data, which means matching records for the same person across tools.
- Collect less, keep it shorter: collect only what the purpose needs, and delete it when you no longer need it.
- Separate email marketing rules sit alongside GDPR (the EU ePrivacy rules and national laws such as the UK's PECR). How they treat B2B email differs from country to country.

### CCPA / CPRA (California)

California's law gives residents the right to know what data a business has on them, to delete it, to correct it, and to opt out of its sale or sharing. It applies to businesses above certain size thresholds. Its temporary exemption for B2B contact data has expired, so business contacts are generally covered now. Other US states have passed similar laws with different thresholds and details.

### CAN-SPAM (US commercial email)

CAN-SPAM, the US commercial email law, does not require people to opt in before you email them. It does require, among other things: accurate sender and header information, subject lines that do not mislead, a valid physical mailing address, a clear way to opt out, and honoring opt-outs promptly (within the deadline the law sets). The company stays responsible even when an agency or tool sends on its behalf.

### Suppression and do-not-contact handling

A suppression list is the list of people and companies you must not contact. Most GTM compliance failures are plumbing failures: someone opted out in one tool and then got emailed from another.

| Practice | Implementation |
|---|---|
| One global suppression list | A table keyed on normalized email, domain and phone, with reason, source and timestamp |
| Check at send time | Every sequencer and workflow calls the suppression check immediately before sending, not only at list build |
| Fast propagation | Opt-out events flow through the event pipeline within minutes to every engagement tool |
| Never overwritten | Syncs and enrichment cannot clear a do-not-contact flag; only a documented process can |
| Domain-level suppression | Customers, competitors and accounts that requested no contact are suppressed by domain |
| Retain the suppression record | Keep the minimum needed to honor the request even after deleting other data |

Test it: add a test address to the suppression list, trigger every way the system can send, and confirm nothing goes out. Repeat this every time a new tool or workflow goes live.

## Compliance as a system property

Turn the rules into checks the system runs on its own, so compliance does not depend on someone remembering:

- Required fields when a contact is created: `source`, `lawful_basis` (where it applies), `collected_at`, `country`.
- Routing by region: contacts in places with stricter email rules go into sequences built for those rules.
- Scheduled cleanup jobs that delete or anonymize records past their keep-by date, with a log of what was removed.
- A data map: which systems hold personal data, which fields, why, and who owns each one. You need this anyway to answer requests from people asking what data you hold on them.

## Data licensing

Many business-data providers limit what you can do with their data. Common limits: you can only keep it for a short time, you cannot store it in your own database, you cannot mix it with other data, you cannot pass it on to anyone else, or you can only view it inside the provider's own app. Map and review-site data are frequent examples.

Before building a shared database or a product on top of a data source, check:

| Question | Why it matters |
|---|---|
| May we store the data, and for how long? | Determines whether a cache or warehouse table is allowed |
| May we derive and keep new fields from it? | Scores and classifications may count as derived works |
| May we share it with other customers or tenants? | Multi-tenant products often violate single-licensee terms |
| Is attribution required? | Display obligations in the UI |
| What happens at contract end? | Deletion obligations can remove your history |

The [RouteHero project](../../projects/routehero/README.md) shows this check in practice. It turned down Google Places and Yelp as the base for a shared location database because their terms limit storing and sharing the data. It chose Overture Maps, an open dataset, instead. Write down the decision and the terms you reviewed in a short decision record ([decision examples](../../decision-examples/README.md)).

## Access control

| Principle | In practice |
|---|---|
| Least privilege | Integration users get only the objects and fields they write; reps see what their role needs |
| Scoped API keys | One key per integration, with the narrowest scopes the vendor offers; never a shared admin key |
| Service accounts | Integrations run as named service users, not as a person's login, so leaving staff do not break automations |
| Secret storage | Keys in a secret manager or environment store; never in code, workflow JSON exports or spreadsheets |
| Rotation | Keys rotated on a schedule and immediately when someone with access leaves |
| Periodic review | Quarterly list of users and integrations with write access to core objects; remove what is unused |

In short: give every person and tool only the access it needs. API keys are the passwords tools use to connect to each other. A service account is a login that belongs to the company, not to an employee.

What goes wrong: an enrichment tool gets connected using a system administrator's login, so it can overwrite any field. Or a workflow export with an API key inside gets shared in Slack.

## Audit logs

An audit log records who or what changed important data, when, from what value, to what value, and why.

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

CRMs can track change history on a limited number of fields. Turn it on for owner, stage, amount, score tier and do-not-contact. For changes made by your own automations, write to an audit table like the one above. The test: pick a random owner change from last month and explain it in under five minutes.

## Data integrity

Data integrity means the data matches reality and does not contradict itself. Controls:

- Check data as it comes in (format, types, allowed values). See [data architecture](../03-data-architecture/README.md#data-validation).
- Check links between records: no contact roles pointing to deleted contacts, no opportunities sitting on merged accounts.
- Reconcile: counts and totals match between systems, for example CRM closed-won amount vs billing bookings for the same period.
- Track where numbers come from: calculated fields store their source and the version of the calculation, so a wrong score can be traced. See [the GTM ontology project](../../projects/gtm-ontology/README.md).

## Reliability and SLOs

Set reliability targets, called service level objectives (SLOs), for the workflows that affect revenue. An SLO is a target for something you can measure, over a set period.

| Workflow | Indicator | Example target |
|---|---|---|
| Inbound lead routing | Leads assigned within 5 minutes of creation | 99 percent over 30 days |
| Opt-out propagation | Opt-outs applied in all send tools within 15 minutes | 99.9 percent over 30 days |
| Nightly scoring job | Scores refreshed by 07:00 local | 28 of 30 days |
| CRM sync | Changes reflected in warehouse within 1 hour | 99 percent |

The error budget is 1 minus the target: the amount of failure you can accept. If routing uses up its budget, fixing reliability comes before new features in that workflow. Targets should match the business cost of failure. A late score refresh is an inconvenience. A missed opt-out is a legal and reputation problem, so its target is stricter.

## Change management

Most GTM incidents start with a change: a new flow, an edited validation rule, a reordered routing rule, a tweaked AI prompt.

| Practice | Implementation |
|---|---|
| Separate environments | Salesforce sandbox or HubSpot test portal for CRM changes; staging copies of workflows for orchestration tools |
| Version control | Store code, workflow definitions, scoring weights and prompts in Git; tag what is deployed |
| Review | A second person reviews changes to routing, scoring, suppression and anything that sends messages |
| Dry runs | Run changed routing or scoring against last week's records and diff the decisions before switching over |
| Rollback plan | Know how to revert before deploying; keep the previous version runnable |
| Change log | Date, change, owner, reason and link to the review, visible to sales and marketing ops |

The short version: test changes in a copy first, keep a history of every version (Git is the standard tool for this), have a second person review, compare old and new results before switching, and know how to undo.

Freeze non-urgent changes around quarter end, when routing or scoring changes can throw off forecasts and commissions.

## AI data handling

AI steps raise their own governance questions:

- **What data leaves your systems?** Send only the fields the task needs. Remove or mask personal data the task does not require.
- **Provider terms.** Check the AI provider's rules on how long they keep your data and whether they train on it, for the plan you use. Record them in the vendor file.
- **Check AI output.** AI answers go to a holding table first, get checked against allowed values, and only then get written into systems by code. See [AI and agents](../05-ai-and-agents/README.md).
- **Test records.** For each release, keep the test set, the prompt version and the score, so a drop in quality can be traced to a specific change. See [the AI evaluation project](../../projects/ai-evaluation/README.md).
- **Human review for actions that cannot be undone.** Sends, merges and deletions proposed by an AI agent must pass a person or a fixed rule check.

## Incident handling

When something breaks (a wrong mass reassignment, a send to a suppressed group, a sync that overwrote a field), the order is: stop the damage, measure it, fix it, tell people, learn from it.

1. **Stop:** pause the workflow or sequence. Every live workflow needs a documented off switch.
2. **Scope:** use the audit log and run log to list the affected records and people.
3. **Fix:** restore from the audit log's `old_value`, a backup or a replay. Handle opt-out and suppression breaches first.
4. **Communicate:** tell the affected owners (reps whose accounts moved, marketing if emails went out) what happened and what was done.
5. **Learn:** a short no-blame review covering the timeline, the cause, why existing checks missed it, and one or two concrete follow-ups with owners and dates.

Track how many incidents happen and how long each took to spot. Time to spot is usually the bigger lever. A broken workflow found in an hour affects far fewer records than one found at the monthly review.

## Retention schedule

Write down how long each type of data is kept and why. Example layout (the periods are placeholders to set with a lawyer):

| Data class | Retention | Action at expiry |
|---|---|---|
| Prospect contacts with no engagement | Set per policy | Delete or anonymize, keep suppression record |
| Customer contacts | Duration of relationship plus policy period | Review, then delete or anonymize |
| Raw webhook payloads | Short, long enough for replay and debugging | Delete |
| Enrichment cache | Per vendor terms | Delete or refresh |
| Audit logs | Per policy and legal requirements | Archive |
| Call recordings and transcripts | Per policy and consent terms | Delete |

## Observability

Observability means being able to answer "what happened, and why?" without reading code.

- **Logs:** a record of each run, with the workflow, run ID, a summary of inputs and outputs, status, duration and cost.
- **Metrics:** per workflow, the success rate, speed, volume, spend, and the size of the dead-letter queue (DLQ: the pile of failed items waiting to be retried or fixed).
- **Alerts:** when something fails, when something goes quiet (an expected run did not happen), and when something looks odd (volume or cost far off its recent average). Send each alert to a named owner, not a shared channel nobody watches.
- **Dashboards:** one page per layer, matching the monitors in [architecture layers](../03-data-architecture/architecture-layers.md).

## Vendor evaluation

Score vendors against weighted criteria chosen before the demos, so the decision is not won by the best presentation.

| Criterion | Weight | What to check | Score 1 to 5 |
|---|---|---|---|
| Fit to the capability gap | 25 | Does it solve the specific problem, tested on your data? | |
| Data quality on your segment | 20 | Hit rate and accuracy on a sample of your accounts | |
| Integration | 15 | API coverage, bulk endpoints, webhooks, rate limits, CRM connector quality | |
| Licensing and compliance | 15 | Storage and redistribution terms, DPA, subprocessors, data residency | |
| Total cost | 10 | Price at current and 3x volume, overage terms, implementation effort | |
| Security | 10 | SSO, scoped keys, audit logs, security attestations | |
| Exit cost | 5 | Data export, contract length, what you lose on leaving | |

Weighted score = sum(weight x score) / 5, out of 100. The weights are examples. Set them for each decision. Always run a pilot, paid or free, on a sample of your own records. A vendor's coverage claims on their own test set tell you little about your market.

## Technical debt in GTM stacks

Technical debt is the pile of shortcuts and leftovers that make a system harder to change. It builds up faster in GTM tools than in product code, because many people can create automations and few people review them.

| Debt type | Symptom | Remedy |
|---|---|---|
| Field sprawl | Hundreds of custom fields, many unused or duplicated | Usage audit; deprecate with a date; delete after it passes |
| Automation sprawl | Multiple flows and tools writing the same field | Automation inventory; consolidate into one owner per field |
| Orphaned integrations | Tools still syncing after the contract or champion left | Integration inventory with owner and renewal date |
| Undocumented logic | Routing nobody can explain | Move rules to code or one routing tool; document each rule |
| Spreadsheet systems | Critical mappings in personal spreadsheets | Move into a governed table with an owner |

Set aside a fixed share of each quarter for cleanup, and track it with things you can count (fields removed, automations combined).

## Documentation and runbooks

A runbook is a short instruction sheet for running and fixing one workflow. Every live workflow needs one:

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

Keep runbooks next to the code or in the same tool as the workflow, and update them when the workflow changes.

## Business continuity

No GTM system should depend on one person. Practical checks:

- Every integration runs on a company-owned service account, with its credentials in a shared secret store.
- Every workflow has an owner and a backup who has run it at least once.
- At least two people have admin access to the CRM, automation and sequencer tools.
- A written handoff exists: a list of systems, who owns which fields, runbooks, open issues, vendor contacts and renewal dates.
- Settings exports (flows, workflow definitions, scoring rules) are saved with version history, so a bad change can be undone.

Test continuity the simple way: have the backup owner handle the next incident or change without help, then fix whatever they could not find.

## Measuring governance

Governance is working when these numbers move the right way: sends to suppressed contacts (target zero), time to fulfill people's data requests, share of integrations on service accounts with limited-access keys, SLO targets met per workflow, number of fields and automations with no owner, and time needed to explain a random data change.

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
