# Outbound and pipeline results

## FiscalNote: 69 meetings, 27 opportunities, about $436,834 in pipeline in three months

**Evidence status: Self-reported.** No source records are attached. No AI was involved.

| | |
|---|---|
| Role | SDR, FiscalNote |
| Period | Three months |
| Result | 69 meetings, 27 opportunities, about $436,834 in associated pipeline ARR |
| Monthly rate | About 23 meetings a month against a goal of 14 to 16 |
| Activity | Among the lowest on the team |

**Business problem.** SDRs were measured on meetings, and the default way to get more was more activity: more dials and more emails into the same accounts everyone else was already working.

**What I did.** I built my own Salesforce reports to find contacts that fit our true ICP and had never been reached out to. Most of the team's activity went into contacts who had already heard from us. These had not, so the same effort produced more conversations.

**Why it worked.** The constraint was not effort. It was targeting. Untouched contacts in the right accounts had no fatigue from earlier outreach, and the report did the prioritization that extra activity was trying to make up for.

**What it shows.** This is the same idea the rest of this repository builds into systems: find where the best opportunities are before adding volume. The [lookalike model](../../projects/lookalike-model/README.md) does it at scale, and the [revenue-target method](../../THINKING.md#1-understand-the-business-objective) explains why targeting is usually a cheaper lever than activity.

**Still to document.** Whether the 69 meetings were booked or held, whether the pipeline is sourced or influenced, and which amount field and date it was measured on.

## Outbound to grease hood cleaning operators

**Evidence status: Self-reported.**

| | |
|---|---|
| Business | RouteHero, outbound I built |
| Market | Grease hood (commercial kitchen exhaust) cleaning operators |
| Offer | Generating leads to grow their business |
| Reach | About 8,000 contacts |
| Reply rate | About 4% |
| Positive replies | About 40% of replies |
| Positive replies to pipeline | About 30%, sourced by this outbound |

**Why this market.** Owner-operated service businesses like hood cleaners are rarely prospected by anyone offering to grow their business. Their inboxes are not full of competing offers, so a relevant message gets read. This was [RouteHero](../../projects/routehero/README.md)'s own outbound, so the pipeline is sourced.

**Still to document.** Period, channel, and whether the reply rate is on sent or delivered email.

## Quorum: expansion whitespace through parent and child accounts

**Evidence status: Self-reported.**

My territory included organizations with affiliate structures: a national organization with state chapters under it. I started from closed-lost opportunities. I read the records and listened to the old calls to understand how the national organizations and their state chapters bought, both from each other and from Quorum. Then I worked those parent and child relationships, using the account a deal was lost on to open its affiliates. That sourced about $300K in pipeline for a newly piloted expansion motion.

**Why it worked.** Closed-lost is the most underused data in a CRM. Each lost deal records who was involved, what they objected to, and which related organizations were in the conversation. Reading it as account structure rather than as a dead deal turns it into a map of where to go next.

The data model behind this (company, location, account, and the relationships between them) is in the [GTM ontology](../../projects/gtm-ontology/README.md) demo.

**Still to document.** How much closed.

## Quorum: 589 ICP contacts added through a title waterfall

**Evidence status: Self-reported.**

An enrichment waterfall that recognized people with exact or similar titles to the buyers we already sold to, and added them to the CRM: lookalikes at the title level. The [lookalike model](../../projects/lookalike-model/README.md) applies the same idea at the account level.

## FiscalNote meeting goal

**Evidence status: Self-reported.** About 23 meetings a month against a monthly goal of 14 to 16, roughly 145% to 165% of goal, using the targeting approach above.

## How results are documented

A figure is labeled Measured / Verified only with a complete record from the [impact record template](../../templates/impact-record-template.md), with sourced and influenced pipeline reported separately and never added together.

## Related

- [IMPACT.md](../../IMPACT.md)
- [Evidence checklist](../../EVIDENCE_CHECKLIST.md)
- [Analytics: attribution](../../docs/06-analytics-and-prediction/README.md)
