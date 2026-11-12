# ADR 0001: Overture Maps as RouteHero's canonical location source

- **Status:** accepted
- **Date:** 2026-09-12
- **Evidence status:** Measured during development (vendor terms read and data queried on the date above)

## Context

RouteHero needs one row per physical commercial kitchen, with coordinates, for every territory a customer defines. The product's unit economics assume each business record is acquired once, stored in a shared canonical graph and served to every tenant whose territory contains it. That only works if the data license permits storing and re-serving.

## Business objective

Keep variable data cost per tenant low enough for the subscription to carry a healthy margin, while delivering per-site records an operator can call.

## Existing architecture

A provider interface (`BusinessDataProvider`) already isolates the discovery source from the application, so the choice is one adapter, not a rewrite.

## Constraints

- Licensing: stored and re-served data must be legally storable and re-servable.
- Shape: per-site records with coordinates, not people attached to a headquarters address.
- Budget: a pre-revenue product.

## Options considered

| Option | Per-site, coordinates | Storable and re-servable | Notes |
|---|---|---|---|
| Contact-data provider (tested live) | No: people per company, HQ address, no coordinates | n/a | A 14-location restaurant group came back as one address. Strong for contact enrichment later, wrong for discovery |
| Google Places API | Yes | No | Maps Platform terms prohibit storing and re-hosting names and addresses, and prohibit using Places coordinates for point-in-polygon analysis |
| Yelp Fusion | Yes | No | Terms cap storage at 24 hours and prohibit building a business-listing database or use on behalf of third parties |
| D7 Lead Finder | No coordinates | No | Terms prohibit reproduction or resale |
| OpenStreetMap | Yes | Yes, with ODbL share-alike | Share-alike could require publishing a derived database |
| Overture Maps | Yes | Yes, CDLA-Permissive 2.0 / Apache 2.0 / CC0 per contributor, attribution only | Monthly Parquet releases queryable with DuckDB, no API key |

## Decision criteria

1. License permits storing and re-serving to multiple tenants.
2. Per-site records with coordinates.
3. Coverage and contact fields (phone, website) for calling.
4. Cost.

## Chosen approach

Overture Maps places as the primary source. OpenStreetMap kept as a fallback and cross-check. A contact-data provider is a candidate for a later contact-enrichment slot, behind its own interface.

## Rationale

Same greater-Houston box, measured on 2026-09-12:

| Measure | OpenStreetMap | Overture |
|---|---|---|
| Commercial-kitchen candidates | 9,464 | 24,348 |
| Named | 94% | 100% |
| Street address | about 85% | 99% |
| Phone | about 55% | 86% |
| Query time | 18 s | 3.1 s |

Overture is both the better dataset and the less restrictive license. The Places theme contains no OpenStreetMap data, which is why share-alike does not apply.

## Tradeoffs

- Overture categories differ from OSM's. An early finding that "nursing homes barely exist" was a category-mapping error, not a data gap: Overture files them as `skilled_nursing`, `retirement_home`, `assisted_living_facility` and `senior_citizen_services` (878 facilities in the same box against OSM's 1).
- Monthly releases mean freshness is bounded by the release cycle.

## Risks

- Contributor licensing could change in a future release. Mitigation: record contributor and license per record, check on each release.
- Coverage gaps for very new independents.

## Validation plan

Hand-check a labeled sample per metro for existence and kitchen presence; track phone connect rates once operators call from the list.

## Observed results

Pending. Requires operator calling data.

## Reconsideration triggers

- A contributor license change in a release.
- Measured coverage below a usable level in a target metro.
- A licensed source offering per-site data with storage rights at an acceptable price.
