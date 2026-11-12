# ADR 0004: Remove contract value from the account score

- **Status:** accepted
- **Date:** 2026-09
- **Evidence status:** Measured during development (score distribution on 2,785 real Spring, TX locations)

## Context

The first scoring model weighted estimated contract value most heavily. Then customers were given per-tier pricing: an operator says what a Tier A job is worth to them. That made the model circular: value came from tier, tier came from score, and score came from value.

## Business objective

A tier an operator can trust as "how big and attractive is this job", which their own price then turns into money.

## Options considered

| Option | Problem |
|---|---|
| Keep value in the score | Circular once pricing is per tier; a pricing change would re-rank accounts |
| Remove value, keep thresholds | Measured below: Tier A becomes empty |
| Remove value, move its weight to system count, recalibrate thresholds from the measured distribution | Chosen |

## Chosen approach

- Contract value removed as a factor. Estimated value is computed after the tier: tier price x visits per year.
- System count carries the weight value used to carry (now 0.40), because it is the honest measure of job size and a fact about the kitchen rather than a pricing decision.
- Distance stays high (0.25): for a truck-based business, an excellent account 40 miles out is a worse first call than a good one nearby.

## The failure this exposed

With value gone, 40 points of the scale went with it. On 2,785 real Spring, TX accounts, the top score was 74 and nothing reached the old Tier A threshold of 75. **Tier A came back empty.** A "call these first" list with nothing in it is worse than a wrong one.

Thresholds were reset from the measured distribution instead of from what a high number feels like: p95 was 56 and p85 was 50, so A at 60 is roughly the top 2 to 3% and B at 45 the next fifth. That is a callable morning list, not a category.

## Tradeoffs

Thresholds now depend on one metro's distribution. A different metro mix may need different cutoffs.

## Validation plan

Tier-level conversion: meetings and contracts per 100 accounts called, by tier. If Tier A does not convert better than Tier B, the weights are wrong.

## Observed results

Pending operator outcome data.

## Reconsideration triggers

- A new metro where the Tier A share falls outside roughly 1 to 5%.
- Tier conversion data showing no separation between tiers.
- Thresholds are a config version, so any of these is a config change, not a migration.
