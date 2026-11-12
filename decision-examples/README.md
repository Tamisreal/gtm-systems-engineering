# Decision examples

How decisions get made, written down where they can be checked later. Real decisions are recorded as architecture decision records (ADRs) with dates and the evidence behind them. Hypothetical scenarios are kept separate and labeled.

## Architecture decision records (real)

| ADR | Decision | Evidence |
|---|---|---|
| [0001](adr/0001-routehero-data-source.md) | Overture Maps as RouteHero's canonical location source; Google Places and Yelp rejected on license terms | Vendor terms read and data measured, 2026-09-12 |
| [0002](adr/0002-routehero-tenant-isolation.md) | Three-layer tenant isolation: app context, row-level security, transaction-scoped setting | Live application design |
| [0003](adr/0003-routehero-dedupe-review-queue.md) | Probabilistic matches go to review below 0.9 confidence | Live application design |
| [0004](adr/0004-routehero-remove-circular-factor.md) | Remove contract value from the score; reset tier thresholds from the measured distribution | 2,785 real accounts scored |
| [0005](adr/0005-deterministic-first.md) | Deterministic code first, LLM last | Synthetic eval in this repo |

New records use the [ADR template](../templates/adr-template.md). The "Observed results" section stays empty until there is data.

## Hypothetical scenarios

[scenarios.md](scenarios.md): eight labeled scenarios (low reply rates, CRM data quality, enrichment vendor selection, custom buying signals, introducing an AI agent, retention, forecasting, build versus buy), each run through problem, investigation, options, hypothesis, implementation, measurement and decision, including when an agent is the wrong tool.

## Failure analysis

[failure-analysis.md](failure-analysis.md): real failures with detection, root cause, remediation, prevention, monitoring and lessons, followed by labeled hypothetical failure modes.

## Related

- [THINKING.md](../THINKING.md)
- [Build vs buy vs extend](../docs/03-data-architecture/build-buy-extend.md)
