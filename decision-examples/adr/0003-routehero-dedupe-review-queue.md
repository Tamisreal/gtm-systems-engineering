# ADR 0003: Review queue for probabilistic location matches

- **Status:** accepted
- **Date:** 2026-09 (Phase 1 architecture)

## Context

The same restaurant shows up from different sources and different monthly releases, with slightly different names, addresses and phone formats. Duplicates make territories look bigger than they are and scatter notes across several records. Wrong merges are worse: two businesses in one strip mall become one account, and the customer calls the wrong one.

## Business objective

One official list where each physical location is one record, with very few wrong merges, because one wrong merge spoils every score built on top of it.

## Options considered

| Option | Duplicates left | Wrong merges | Work for people |
|---|---|---|---|
| Merge only on exact matches | High | Near zero | None |
| Merge automatically when records look similar | Low | High in busy retail areas | None, until the cleanup |
| Exact matches first, then similar-looking matches with a confidence cutoff, and a person reviews anything below it | Low | Low | A review queue |

## Chosen approach

Records are matched in this order:

1. The data provider's own ID.
2. Phone number, cleaned into one standard format (E.164, the international format).
3. Website domain, cleaned into one standard format.
4. Names that are more than 0.85 similar (on a 0 to 1 scale, using a letter-pattern comparison called trigram similarity) and within 100 meters of each other.
5. A cleaned-up address that matches exactly, plus names more than 0.6 similar.

Steps 4 and 5 find likely matches that are not certain. When their confidence is below 0.9, the system does not merge. It adds the pair to a review queue instead.

## Rationale

Auto-merging similar addresses in strip malls creates so many wrong merges that the whole list becomes unreliable. Running a review queue costs less than cleaning up afterward.

## Tradeoffs

Someone has to work the queue. If nobody does, the unreviewed pairs quietly stay as duplicates.

## Validation plan

Track how big the queue is and how old its items are, how often reviewers accept a suggested merge at each confidence level, and a spot-check of merges to count wrong ones. Use the accept rate to move the 0.9 cutoff.

## Observed results

Pending: no reviewer data yet.

## Reconsideration triggers

- Reviewers accept roughly 98% or more of suggestions at a confidence level: let that level merge automatically.
- Queue items getting older week after week: the cutoff is too cautious for the people available to review.
