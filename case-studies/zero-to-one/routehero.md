# Zero to one: RouteHero

**Evidence status:** product facts and timeline are **Measured / Verified** from the code repository's dated commit history and design documents. Commercial outcomes are **Self-reported**: 8 customers. Revenue is private and not published.

## Opportunity identification

Field-service businesses (the first vertical is commercial kitchen exhaust cleaning) grow by winning recurring contracts close to their shop. Their prospect lists come from scraped maps or contact databases, and neither answers the operator's real question: which kitchens near me are worth the most, and who do I call first?

## Market research

The research that shaped the product was about data, because the data decides whether the product can exist:

- A contact-data provider tested live returned people at companies with a headquarters address. A 14-location restaurant group was one row. Wrong shape for a business that services sites. ([ADR 0001](../../decision-examples/adr/0001-routehero-data-source.md))
- Vendor terms ruled out Google Places, Yelp and another lead tool for a stored, shared database.
- Overture Maps gave 2.6x the candidate kitchens of OpenStreetMap in the same Houston area, 86% phone coverage against about 55%, under a license that permits storage and re-serving.
- A finding that a high-value segment (senior care) was missing turned out to be a category-mapping error and was corrected the same day.

## ICP

Owner-operated field-service businesses with a truck-based service radius and recurring, regulated service cycles. Hood cleaning first because the cleaning frequency is set by fire code (NFPA 96), which makes recurring value estimable. The platform was generalized to other verticals by 2026-09-20.

To verify: firmographic ICP rules used in outreach (shop count, crew size, revenue band).

## Positioning

The site moved from "software for your territory" toward "win high-value contracts" (2026-10-15), and a separate page for B2B distributors and suppliers followed (2026-10-16). The product stopped naming its data source publicly (2026-09-30).

## Product design and architecture

Built as a multi-tenant application with a shared canonical graph of locations and tenant-private scores, notes and status. Design rules visible in the code: every score explains itself, every estimate is a range with confidence, and an operator's real data overrides the model and feeds the next version. Details: [project page](../../projects/routehero/README.md).

Timeline from the commit history:

| Date | Milestone |
|---|---|
| 2026-09-12 | Scaffold, schema and tenant isolation; data source evaluation; provider abstraction; Overture adapter; territory, H3 coverage, dedupe, discovery, scoring; first map |
| 2026-09-13 | Accounts screens, dashboard, notes and status, kitchen classifier, per-tier pricing set by the customer |
| 2026-09-14 to 15 | Follow-up queue, contacts, campaigns and inbox screens; county-sized territories |
| 2026-09-20 | Marketing site on live data; billing and paywall; customer data export; every vertical, not only hood cleaning |
| 2026-09-29 | One customer per territory per service (exclusivity); rebrand from RoutePro to RouteHero |
| 2026-10-04 | Route ordering (nearest neighbor plus 2-opt); MCP server and plugin listing so owners can size their market from ChatGPT or Codex; SEO foundations (sitemap, Organization markup, about page); PostHog funnel events |
| 2026-10-04 to 09 | Listed per-territory pricing tested at two price points, then replaced by pricing on a call |
| 2026-10-15 | Site stripped to a marketing site focused on winning high-value contracts, booking-led |

## Distribution and sales motion

The commit history shows a move from self-serve (Clerk billing, paywall, sign-up) to a sales-assisted motion (every call to action opens a booking page, pricing discussed on a call) in about four weeks. See [GTM motions](../../docs/01-gtm-foundations/gtm-motions.md) for why that move usually happens: at this price point and with this buyer, a conversation converts where a checkout page does not.

Outbound I built for RouteHero (self-reported): about 8,000 grease hood cleaning contacts, about 4% reply rate, about 40% of replies positive, and about 30% of positive replies converted to sourced pipeline. See [outbound results](../revenue-impact/historical-outbound.md#outbound-to-grease-hood-cleaning-operators).

To verify: what triggered the change (conversion data, buyer feedback, or a judgment call), and what the funnel looked like before and after.

## Pricing and revenue model

Per territory, per month, with territory exclusivity per service: one operator per territory, which makes the territory itself the scarce product. Contact volume per month was part of the offer. Listed price points changed twice in a week before moving to a call.

To verify: current offer, whether it is software, service or both, and any revenue to date.

## Experimentation

- Data source experiment with a measured result (ADR 0001).
- Score calibration against real businesses: first against 1,904, later against 2,785 accounts, including the empty-Tier-A failure and fix ([ADR 0004](../../decision-examples/adr/0004-routehero-remove-circular-factor.md)).
- Pricing tests on the public site (two price points, then call-based).
- Funnel instrumentation (PostHog page views, traffic channels, funnel events) in place since 2026-10-04.

## Measured outcomes

| Outcome | Value | Status |
|---|---|---|
| Discovery coverage versus OSM, Houston | 24,348 versus 9,464 candidates | Measured, development |
| Customers | 8 | Self-reported |
| Revenue | Private | Not published |
| Sales calls | Convert better when the operator sees a map of their potential customers around their shop | Self-reported |
| Tier A accounts | Convert better for customers: these kitchens care about compliance, real hood cleaning and protecting the equipment in their kitchen | Self-reported, not yet measured as a rate |
| Funnel data since 2026-10-04 | | Pending: export from PostHog |

## Lessons learned

- Showing an operator the map of their own market sells better than describing it. Sales calls convert better when the potential customers around their shop are on the screen.

From the record, not reconstructed:

- Data licensing is an architecture decision. It was settled before the first adapter shipped.
- A score without a feedback path is a map with a list next to it. The verified-count override exists for that reason.
- Thresholds set by intuition fail as soon as inputs change; set them from the distribution.

To verify with Tam: the commercial lessons (buyer objections heard, what the first customers responded to).

## Verification questions

1. What drove the move from self-serve to call-based selling?
2. PostHog funnel numbers since 2026-10-04: visitors, booking-page opens, calls booked.
3. Has any operator entered verified system counts? How many?

## Related

- [RouteHero project page](../../projects/routehero/README.md)
- [Amazon wholesale case study](amazon-wholesale.md)
- [IMPACT.md](../../IMPACT.md)
