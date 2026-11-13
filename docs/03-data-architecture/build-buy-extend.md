# Build vs buy vs extend

No company starts from scratch. Every company already pays for a CRM (customer relationship management system), an email sequencer, a call recorder and data vendors, and its people already know how to use them.

So the default order is: extend what already exists. Buy when a mature product already solves the problem. Build only when the result truly sets the company apart, or fills a gap no tool covers.

## The three options

| Option | What it means | Typical example |
|---|---|---|
| Extend | Configure or add to a system already in place: fields, flows, a webhook-triggered function, an enrichment column | Add a routing exception to native CRM assignment rules |
| Buy | Adopt a product built for the job | A dedicated call recorder instead of recording calls by hand |
| Build | Write and own custom software | A territory engine scoring physical sites by job size and distance, which no CRM does |

A webhook is a message one system sends another the moment something happens. An enrichment column is a field filled in automatically from a data vendor.

## Evaluation criteria

Score each option from 1 to 5 on each criterion below. Decide how much each criterion matters for this decision, and write those weights down before you start scoring, so the scores cannot be bent toward a favorite.

| Criterion | Questions to answer |
|---|---|
| Existing capabilities | What does the current stack already do? Is the gap real or a configuration problem? |
| Total cost of ownership | License, implementation, maintenance labor, data and model costs per year, not just year one |
| Implementation time | Time to first value, not time to finished |
| Vendor dependency | What breaks if the vendor raises prices, changes an API or shuts down? |
| Data ownership | Who owns the data, can it be exported, and do the vendor's terms allow storing what you pull? |
| Security | Access scope, data residency, SOC 2 or equivalent, how credentials are held |
| Maintenance | Who fixes it at 2 a.m., and will they still be here next year? |
| Reliability | Failure modes, retries, monitoring, what happens to data during an outage |
| Business differentiation | Does doing this better than competitors win deals? If not, do not build it |
| User experience | Will reps use it inside the tools they already have open? |
| Organizational adoption | Who has to change how they work, and who owns it after launch? |

An API is the doorway a system offers for other systems to read and write its data. Data residency means which country the data is stored in. SOC 2 is a standard security audit for software vendors.

A simple rule of thumb: building only wins when two things are true. It must set the company apart, and owning the data must matter. On top of that, either no product exists to buy, or the product would hold data you need to keep.

## Example decisions

| Decision | Choice | Reason |
|---|---|---|
| RouteHero's location data | Build on open data (Overture Maps) | Licensed map APIs prohibit storing and re-serving their content, and the shared database is the product. See [ADR 0001](../../decision-examples/adr/0001-routehero-data-source.md) |
| RouteHero auth and organizations | Buy (Clerk) | Organizations map to tenants natively; building auth is not a differentiator |
| RouteHero maps | Buy (Mapbox) | Rendering and clustering at volume is a solved problem |
| Competitor detection on websites | Build a small scanner | Exact string matching on page source is cheap, explainable, and stores evidence. See [GTM Learning Engine](../../projects/gtm-learning-engine/README.md) |
| Call signal extraction | Extend the call recorder's data with a pipeline into the CRM | The recorder already captures calls; the gap is structured fields, review and CRM writes. See [conversation intelligence](../../projects/conversation-intelligence/README.md) |
| Lead routing exceptions | Extend native routing | Build only the exception, not a routing service. See [scenario 8](../../decision-examples/scenarios.md#8-custom-development-versus-existing-saas) |

A few terms from the table: an ADR (architecture decision record) is a short document explaining one technical decision and why it was made. "Auth" is login and access control. "Tenants" are the separate customer companies sharing one app, each seeing only its own data.

## What would change the recommendation

- A vendor raises its price enough to change the total cost comparison.
- A license or terms change removes the right to store the data.
- Something becomes a real competitive advantage, which pushes a "buy" toward "build."
- The person who maintains a custom build leaves without handing it over properly, which pushes a "build" toward "buy."

## Related

- [Architecture layers](architecture-layers.md)
- [Technology ecosystem](technology-ecosystem.md)
- [Governance: vendor evaluation and data licensing](../07-governance-and-operations/README.md)
- [Decision records](../../decision-examples/README.md)
