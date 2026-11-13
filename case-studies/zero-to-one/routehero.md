# Zero to one: RouteHero

RouteHero is live with 8 customers. Revenue is private and not published. Product facts and the timeline come from the dated history of changes in the code repository and from design documents.

## Opportunity identification

Field-service businesses grow by winning recurring contracts close to their shop. The first industry is commercial kitchen exhaust cleaning. Their prospect lists come from scraped maps or contact databases. Neither answers the operator's real question: which kitchens near me are worth the most, and who do I call first?

## Market research

The research that shaped the product was about data, because the data decides whether the product can exist at all:

- A live test of a contact-data provider returned people at companies, filed under a headquarters address. A 14-location restaurant group came back as one row. That is the wrong shape for a business that services individual sites. ([ADR 0001](../../decision-examples/adr/0001-routehero-data-source.md), a short write-up of the decision)
- Vendor terms ruled out Google Places, Yelp and another lead tool, because RouteHero needs to store the data and share it across customers.
- Overture Maps found 2.6x as many possible kitchens as OpenStreetMap in the same Houston area, with phone numbers for 86% of them against about 55%. Its license allows storing the data and serving it again.
- One finding said a high-value segment (senior care) was missing. It turned out to be a mistake in how categories were mapped, and it was fixed the same day.

## ICP

The ideal customer profile (ICP): owner-operated field-service businesses whose trucks cover a set radius, with recurring service required by regulation. Hood cleaning came first because fire code (NFPA 96) sets how often hoods must be cleaned, so the recurring value of each kitchen can be estimated. By 2026-09-20 the platform worked for other industries too.

To verify: the company-size rules for the ICP used in outreach (shop count, crew size, revenue band).

## Positioning

The site moved from "software for your territory" toward "win high-value contracts" (2026-10-15). A separate page for B2B distributors and suppliers followed (2026-10-16). The product stopped naming its data source publicly (2026-09-30).

## Product design and architecture

Many customers share one app. They share one official map of locations, while each customer's scores, notes and status stay private to them. Design rules visible in the code: every score explains itself, every estimate is a range with a confidence level, and an operator's real data overrides the model's guess and improves the next version. Details: [project page](../../projects/routehero/README.md).

Timeline from the history of code changes:

| Date | Milestone |
|---|---|
| 2026-09-12 | Basic app and database set up, with each customer's data kept separate; data sources evaluated; a common connector so data sources can be swapped; Overture connector; territories, map coverage using H3 (a grid of hexagons), duplicate removal, kitchen discovery, scoring; first map |
| 2026-09-13 | Account screens, dashboard, notes and status, a tool that sorts kitchens by type, per-tier pricing set by the customer |
| 2026-09-14 to 15 | Follow-up list, contacts, campaigns and inbox screens; county-sized territories |
| 2026-09-20 | Marketing site on live data; billing and paywall; customers can export their data; every industry, not only hood cleaning |
| 2026-09-29 | One customer per territory per service (exclusivity); rebrand from RoutePro to RouteHero |
| 2026-10-04 | Route ordering (nearest stop first, then a 2-opt pass that removes crossed paths); MCP server and plugin listing, so owners can size their market from inside ChatGPT or Codex; SEO basics (sitemap, Organization markup that tells search engines who the company is, about page); PostHog tracking of funnel steps |
| 2026-10-04 to 09 | Listed per-territory pricing tested at two price points, then replaced by pricing on a call |
| 2026-10-15 | Site cut back to a marketing site about winning high-value contracts, built around booking a call |

## Distribution and sales motion

The history of code changes shows a move in about four weeks from self-serve (Clerk billing, paywall, sign-up) to selling with a person involved (every button opens a booking page, and pricing is discussed on a call). See [GTM motions](../../docs/01-gtm-foundations/gtm-motions.md) for why that move usually happens: at this price and with this buyer, a conversation converts where a checkout page does not.

Outbound I built for RouteHero: about 8,000 grease hood cleaning contacts, about 4% reply rate, about 40% of replies positive, and about 30% of positive replies turned into pipeline this outbound created. See [outbound results](../revenue-impact/historical-outbound.md#outbound-to-grease-hood-cleaning-operators).

To verify: what triggered the change (conversion data, buyer feedback, or a judgment call), and what the funnel looked like before and after.

## Pricing and revenue model

Priced per territory, per month. Each territory goes to only one operator per service, which makes the territory itself the scarce product. A monthly number of contacts was part of the offer. The listed prices changed twice in one week before moving to pricing on a call.

To verify: current offer, whether it is software, service or both, and any revenue to date.

## Experimentation

- A data source test with a measured result (ADR 0001).
- Checking the score against real businesses, first 1,904 accounts and later 2,785, including the empty Tier A failure and its fix ([ADR 0004](../../decision-examples/adr/0004-routehero-remove-circular-factor.md)). Tier A is the top group of accounts.
- Pricing tests on the public site (two price points, then pricing on a call).
- Funnel tracking in PostHog (page views, traffic sources, funnel steps) in place since 2026-10-04.

## Outcomes

| Outcome | Value | Source |
|---|---|---|
| Kitchens found versus OpenStreetMap (OSM), Houston | 24,348 versus 9,464 possible kitchens | Measured during development |
| Customers | 8 | |
| Sales calls | Convert better when the operator sees a map of their potential customers around their shop | Selling it myself |
| Tier A accounts | Convert better for customers: these kitchens care about compliance, real hood cleaning and protecting the equipment in their kitchen | Customer feedback |

## Lessons learned

- Showing an operator a map of their own market sells better than describing it. Sales calls convert better when the potential customers around their shop are on the screen.

From the written record, not pieced together later:

- Data licensing is a design decision. It was settled before the first data connector shipped.
- A score that never learns from real results is just a map with a list next to it. That is why operators can enter their own confirmed counts to override the estimate.
- Cutoffs set by gut feel break as soon as the inputs change. Set them from how the scores actually spread out.

To verify with Tam: the commercial lessons (buyer objections heard, what the first customers responded to).

## Verification questions

1. What drove the move from self-serve to selling on calls?
2. PostHog funnel numbers since 2026-10-04: visitors, booking-page opens, calls booked.
3. Has any operator entered confirmed system counts? How many?

## Related

- [RouteHero project page](../../projects/routehero/README.md)
- [Amazon wholesale case study](amazon-wholesale.md)
