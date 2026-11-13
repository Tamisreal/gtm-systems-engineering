# Decision examples

How I make decisions, written down so anyone can check them later. Each big decision gets a decision record (engineers call these ADRs, short for architecture decision records). Each record has a date and the reasons behind the choice.

## Architecture decision records

| Record | Decision | Based on |
|---|---|---|
| [0001](adr/0001-routehero-data-source.md) | Overture Maps (a free, open map dataset) is RouteHero's one official source for business locations. Google Places and Yelp were rejected because their license terms forbid how RouteHero needs to use the data | Vendor terms read and data measured, 2026-09-12 |
| [0002](adr/0002-routehero-tenant-isolation.md) | Three separate safeguards keep each customer account's data private: the app checks, the database itself blocks one customer from seeing another's data, and the customer setting expires after each request | How the live app is built |
| [0003](adr/0003-routehero-dedupe-review-queue.md) | When two records are a likely match but not certain (under 0.9 confidence), a person reviews them before they are merged | How the live app is built |
| [0004](adr/0004-routehero-remove-circular-factor.md) | Remove contract value from the account score, then reset the tier cutoffs based on how the real scores actually spread out | 2,785 real accounts scored |
| [0005](adr/0005-deterministic-first.md) | Use plain code with fixed rules first, and an AI model (LLM) only as a last resort | Test results in this repo |

New records use the [decision record template](../templates/adr-template.md). The "Observed results" section stays empty until there is real data.

## Scenarios

[scenarios.md](scenarios.md): eight common sales and marketing problems (low reply rates, messy CRM data, picking a data vendor, building your own buying signals, adding an AI agent, keeping customers, forecasting, and building software versus buying it). Each one walks through the problem, the investigation, the options, a testable guess, the work, how to measure it, and the final decision. Each also says when an AI agent is the wrong tool.

## Failure analysis

[failure-analysis.md](failure-analysis.md): things that went wrong. For each one: how it was spotted, the real cause, the fix, how to stop it happening again, what to watch, and the lesson. Then a list of common ways these systems break.

## Related

- [How I think](../README.md)
- [Build vs buy vs extend](../docs/03-data-architecture/build-buy-extend.md)
