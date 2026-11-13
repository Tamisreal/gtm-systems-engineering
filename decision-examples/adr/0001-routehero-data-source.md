# ADR 0001: Overture Maps as RouteHero's canonical location source

- **Status:** accepted
- **Date:** 2026-09-12

## Context

RouteHero needs one record for every physical commercial kitchen, with its map location, inside every territory a customer draws. The business model depends on buying or collecting each business record once, storing it in one shared master list, and showing it to every customer account whose territory includes it. That only works if the data license allows us to store the data and show it to many customers.

## Business objective

Keep the data cost per customer low enough that the subscription still makes good money, while giving operators a record for each location they can actually call.

## Existing architecture

The app already talks to its data source through one plug-in point (`BusinessDataProvider`). Switching sources means writing one new connector, not rebuilding the app.

## Constraints

- Licensing: we must be legally allowed to store the data and show it to customers.
- Shape: one record per location with its map location, not a list of people tied to a head office address.
- Budget: the product has no revenue yet.

## Options considered

| Option | One record per location, with map location | Allowed to store and show to customers | Notes |
|---|---|---|---|
| Contact-data provider (tested live) | No: it lists people per company, the head office address, and no map location | n/a | A restaurant group with 14 locations came back as one address. Good for adding contact details later, wrong for finding locations |
| Google Places API | Yes | No | Google Maps Platform terms forbid storing and re-showing names and addresses. They also forbid using Places map locations to check whether a business sits inside a territory |
| Yelp Fusion | Yes | No | Terms allow storing data for only 24 hours. They forbid building a business-listing database or using the data for other companies |
| D7 Lead Finder | No map location | No | Terms forbid copying or reselling |
| OpenStreetMap | Yes | Yes, under the ODbL license's "share-alike" rule | Share-alike could force us to publish our own combined database |
| Overture Maps | Yes | Yes. Licenses are CDLA-Permissive 2.0, Apache 2.0 or CC0 depending on who contributed the data. All only ask for credit | New data files every month (Parquet format) that can be searched with a free tool (DuckDB), no account key needed |

## Decision criteria

1. The license allows storing the data and showing it to many customer accounts.
2. One record per location, with its map location.
3. Coverage, plus contact fields (phone, website) operators need to call.
4. Cost.

## Chosen approach

Overture Maps places are the main source. OpenStreetMap stays as a backup and a cross-check. A contact-data provider may be added later, through its own plug-in point, to fill in contact details.

## Rationale

Same greater-Houston area, measured on 2026-09-12:

| Measure | OpenStreetMap | Overture |
|---|---|---|
| Possible commercial kitchens found | 9,464 | 24,348 |
| Has a name | 94% | 100% |
| Has a street address | about 85% | 99% |
| Has a phone number | about 55% | 86% |
| Search time | 18 s | 3.1 s |

Overture has the better data and the looser license. Its places data contains no OpenStreetMap data, so OpenStreetMap's share-alike rule does not apply.

## Tradeoffs

- Overture labels business types differently from OpenStreetMap. An early finding that "nursing homes barely exist" was a labeling mix-up, not missing data. Overture files them as `skilled_nursing`, `retirement_home`, `assisted_living_facility` and `senior_citizen_services`. That gave 878 facilities in the same area, against 1 in OpenStreetMap.
- New data comes out monthly, so records can be up to a month out of date.

## Risks

- A data contributor could change its license in a future release. How we handle it: record the contributor and license on every record, and check them on each release.
- Very new independent businesses may be missing.

## Validation plan

In each metro, hand-check a sample of records: does the business exist, and does it have a kitchen? Once operators start calling from the list, track how often the phone number reaches the business.

## Observed results

Pending. Needs data from operators' calls.

## Reconsideration triggers

- A contributor changes its license in a release.
- Coverage in a target metro turns out too thin to use.
- A paid source offers one record per location, with storage rights, at an acceptable price.
