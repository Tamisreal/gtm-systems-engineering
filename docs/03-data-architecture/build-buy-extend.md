# Build vs buy vs extend

Companies are never greenfield. They already pay for a CRM, a sequencer, a call recorder and data vendors, and their people already know how to use them. The default is to extend what exists, buy where a mature product solves the problem, and build only where the result is a real differentiator or fills a gap no tool covers.

## The three options

| Option | What it means | Typical example |
|---|---|---|
| Extend | Configure or add to a system already in place: fields, flows, a webhook-triggered function, an enrichment column | Add a routing exception to native CRM assignment rules |
| Buy | Adopt a product built for the job | A dedicated call recorder instead of recording calls by hand |
| Build | Write and own custom software | A territory engine scoring physical sites by job size and distance, which no CRM does |

## Evaluation criteria

Score each option 1 to 5 per criterion, weight by what matters for this decision, and write the weights down before scoring.

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

A simple rule of thumb: build scores well only when differentiation and data ownership are high, and a buyable product does not exist or would own data you need to keep.

## Example decisions

| Decision | Choice | Reason |
|---|---|---|
| RouteHero's location data | Build on open data (Overture Maps) | Licensed map APIs prohibit storing and re-serving their content, and the shared database is the product. See [ADR 0001](../../decision-examples/adr/0001-routehero-data-source.md) |
| RouteHero auth and organizations | Buy (Clerk) | Organizations map to tenants natively; building auth is not a differentiator |
| RouteHero maps | Buy (Mapbox) | Rendering and clustering at volume is a solved problem |
| Competitor detection on websites | Build a small scanner | Exact string matching on page source is cheap, explainable, and stores evidence. See [GTM Learning Engine](../../projects/gtm-learning-engine/README.md) |
| Call signal extraction | Extend the call recorder's data with a pipeline into the CRM | The recorder already captures calls; the gap is structured fields, review and CRM writes. See [conversation intelligence](../../projects/conversation-intelligence/README.md) |
| Lead routing exceptions | Extend native routing | Build only the exception, not a routing service. See [scenario 8](../../decision-examples/scenarios.md#8-custom-development-versus-existing-saas) |

## What would change the recommendation

- A vendor price increase that flips total cost of ownership.
- A license or terms change that removes the right to store data.
- A requirement that becomes a competitive differentiator, which moves a buy toward a build.
- Loss of the person who maintains a custom build, with no documented handoff, which moves a build toward a buy.

## Related

- [Architecture layers](architecture-layers.md)
- [Technology ecosystem](technology-ecosystem.md)
- [Governance: vendor evaluation and data licensing](../07-governance-and-operations/README.md)
- [Decision records](../../decision-examples/README.md)
