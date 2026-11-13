# ADR 0004: Remove contract value from the account score

- **Status:** accepted
- **Date:** 2026-09

## Context

The first scoring model gave estimated contract value the most weight. Then customers got to set their own price per tier: an operator says what a Tier A job is worth to them. That made the model go in a circle. Value came from tier, tier came from score, and score came from value.

## Business objective

A tier an operator can trust to mean "how big and attractive is this job". The operator's own price then turns that tier into dollars.

## Options considered

| Option | Problem |
|---|---|
| Keep value in the score | Goes in a circle once pricing is per tier. A price change would reshuffle the account ranking |
| Remove value, keep the old tier cutoffs | Measured below: Tier A ends up empty |
| Remove value, give its weight to system count, and reset the cutoffs based on how the real scores spread out | Chosen |

## Chosen approach

- Contract value is no longer part of the score. Estimated value is worked out after the tier is set: tier price x visits per year.
- System count (how many hood systems a kitchen has) now carries the weight value used to carry (0.40). It is the honest measure of job size, and it is a fact about the kitchen, not a pricing choice.
- Distance keeps a high weight (0.25). For a business that runs on trucks, a great account 40 miles away is a worse first call than a good one nearby.

## The failure this exposed

Removing value also removed 40 points from the scale. On 2,785 real Spring, TX accounts, the top score was 74, and nothing reached the old Tier A cutoff of 75. **Tier A came back empty.** A "call these first" list with nothing on it is worse than a wrong list.

The cutoffs were reset based on where real scores actually fell, not on what feels like a high number. The top 5% of accounts scored 56 or more, and the top 15% scored 50 or more. So A at 60 is roughly the top 2 to 3% of accounts, and B at 45 is the next fifth. That gives a list a rep can call in a morning, not just a label.

## Tradeoffs

The cutoffs now depend on how scores fell in one metro. A metro with a different mix may need different cutoffs.

## Validation plan

Results by tier: meetings and contracts per 100 accounts called. If Tier A does not do better than Tier B, the weights are wrong.

## Observed results

Pending results data from operators.

## Reconsideration triggers

- A new metro where the share of accounts in Tier A falls outside roughly 1 to 5%.
- Results data showing the tiers perform about the same.
- The cutoffs are a versioned setting, so any of these means changing a setting, not rebuilding the database.
