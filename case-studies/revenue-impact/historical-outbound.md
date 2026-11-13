# Outbound and pipeline work

## FiscalNote: 69 meetings, 27 opportunities, about $436,834 in pipeline in three months

No AI was involved.

| | |
|---|---|
| Role | SDR, FiscalNote |
| Period | Three months |
| Result | 69 meetings, 27 opportunities, about $436,834 in related pipeline, measured as annual recurring revenue (ARR) |
| Monthly rate | About 23 meetings a month against a goal of 14 to 16 |
| Activity | Among the lowest on the team |

**Business problem.** SDRs were measured on meetings. The usual way to get more was more activity: more dials and more emails into the same accounts everyone else was already working.

**What I did.** I built my own Salesforce reports to find contacts who fit our true ideal customer profile (ICP) and had never been contacted. Most of the team's effort went to people who had already heard from us. These people had not, so the same effort produced more conversations.

**Why it worked.** The problem was not effort. It was targeting. Untouched contacts in the right accounts were not worn out by earlier outreach. The report did the sorting that extra activity was trying to make up for.

**What it shows.** The rest of this repository builds the same idea into systems: find where the best opportunities are before adding volume. The [lookalike model](../../projects/lookalike-model/README.md) does it at scale. The [revenue-target method](../../README.md#1-understand-the-business-objective) explains why better targeting is usually cheaper than more activity.

**Still to document.** Whether the 69 meetings were booked or actually held, whether the pipeline was created by this work or only touched by it, and which amount field and date it was measured on.

## Outbound to grease hood cleaning operators

| | |
|---|---|
| Business | RouteHero, outbound I built |
| Market | Grease hood (commercial kitchen exhaust) cleaning operators |
| Offer | Generating leads to grow their business |
| Reach | About 8,000 contacts |
| Reply rate | About 4% |
| Positive replies | About 40% of replies |
| Positive replies to pipeline | About 30%, created by this outbound |

**Why this market.** Almost nobody offering business growth reaches out to owner-operated service businesses like hood cleaners. Their inboxes are not full of competing offers, so a relevant message gets read. This was [RouteHero](../../projects/routehero/README.md)'s own outbound, so the pipeline was created by it.

**Still to document.** Time period, channel, and whether the reply rate is based on emails sent or emails delivered.

## Quorum: expansion whitespace through parent and child accounts

Some organizations in my territory had affiliates: a national organization with state chapters under it. I started from deals we had lost (closed-lost). I read the records and listened to the old calls to learn how the national organizations and their state chapters bought, both from each other and from Quorum. Then I worked those parent and chapter relationships, using the account a deal was lost on to open doors at its affiliates. That created about $300K in pipeline for a new expansion approach Quorum was piloting.

**Why it worked.** Lost deals are the most overlooked data in a CRM. Each one records who was involved, what they objected to, and which related organizations were part of the conversation. Read as a map of how accounts connect, instead of as a dead deal, it shows where to go next.

The data model behind this (company, location, account, and how they connect) is in the [GTM ontology](../../projects/gtm-ontology/README.md) demo.

**Still to document.** How much closed.

## Quorum: 589 ICP contacts added through a title waterfall

A title waterfall searches for job titles in order: exact matches to the buyers we already sold to first, then similar titles. It found these people and added them to the CRM. In short, lookalikes by job title. The [lookalike model](../../projects/lookalike-model/README.md) applies the same idea to whole accounts.

## FiscalNote meeting goal

About 23 meetings a month against a monthly goal of 14 to 16, roughly 145% to 165% of goal, using the targeting approach above.

## Related

- [Analytics: attribution](../../docs/06-analytics-and-prediction/README.md)
