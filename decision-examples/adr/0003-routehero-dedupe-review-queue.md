# ADR 0003: Review queue for probabilistic location matches

- **Status:** accepted
- **Date:** 2026-09 (Phase 1 architecture)
- **Evidence status:** Design decision in a live application; runnable equivalent in [projects/gtm-ontology](../../projects/gtm-ontology/README.md)

## Context

The same restaurant arrives from different sources and releases with slightly different names, addresses and phone formats. Duplicates inflate territory counts and split notes across rows. Wrong merges are worse: two businesses in one strip mall become one account, and the customer calls the wrong one.

## Business objective

A canonical graph where one physical site is one row, with a low rate of wrong merges, because a wrong merge poisons every downstream score.

## Options considered

| Option | Duplicate rate | Wrong-merge rate | Labor |
|---|---|---|---|
| Exact keys only | High | Near zero | None |
| Auto-merge on fuzzy similarity | Low | High in dense retail | None, until cleanup |
| Exact keys, then fuzzy with a confidence threshold and review below it | Low | Low | A review queue |

## Chosen approach

Resolution in order: provider id, normalized E.164 phone, normalized website domain, trigram name similarity above 0.85 within 100 meters, then normalized address hash plus name similarity above 0.6. The probabilistic steps write a merge-candidate row for review instead of merging when confidence is below 0.9.

## Rationale

Auto-merging addresses in strip malls produces wrong merges at a rate that poisons the graph. The review queue is cheaper than the cleanup.

## Tradeoffs

Someone has to work the queue. An unworked queue silently becomes duplicates.

## Validation plan

Track queue size and age, reviewer accept rate per confidence band, and a sampled wrong-merge audit. Move the 0.9 threshold using the accept rate.

## Observed results

Pending: no reviewer data yet.

## Reconsideration triggers

- Reviewer accept rate above roughly 98% in a band: promote that band to auto-merge.
- Queue age growing week over week: the threshold is too conservative for the available labor.
