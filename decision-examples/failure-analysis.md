# Failure analysis

Real failures come first and are labeled with their source. Hypothetical failure modes follow and are labeled as such.

## Real failures

### 1. Tier A came back empty

**Source:** RouteHero development, 2026-09. Documented in [ADR 0004](adr/0004-routehero-remove-circular-factor.md).

- **Detection:** after removing contract value from the score, the tiered list for 2,785 real Spring, TX accounts showed zero Tier A accounts. The top score was 74 against a threshold of 75.
- **Root cause:** removing a 40-point factor compressed the whole distribution, and the thresholds were set by what a high number feels like rather than from data.
- **Remediation:** thresholds reset from the measured distribution (p95 = 56, p85 = 50), giving A at 60 and B at 45.
- **Prevention:** thresholds are a config version stored with every score, so changes are visible and reversible.
- **Monitoring:** the share of accounts in each tier per territory. An empty or bloated Tier A is an alert.
- **Lesson:** any change to a score's inputs requires re-reading the score distribution before the output ships.

### 2. "Nursing homes barely exist"

**Source:** RouteHero data-source evaluation, 2026-09-12. Documented in [ADR 0001](adr/0001-routehero-data-source.md).

- **Detection:** the new data source appeared to have almost no senior-care facilities, a high-value institutional segment.
- **Root cause:** a category mapping error. The query used a category name the dataset does not use; the data files these under four other categories.
- **Remediation:** mapped those four categories; 878 facilities appeared in the same area.
- **Prevention:** category mappings are checked against the source's actual category list, and counts per category are compared across sources before concluding that data is missing.
- **Lesson:** a surprising gap in a dataset is more often a mapping or query problem than a data problem. Check the query first.

### 3. Constant factor in the score

**Source:** RouteHero code history.

- **Detection:** one scoring factor (kitchen confidence) never varied across accounts.
- **Root cause:** it was hardcoded to one value for every location, so it added a constant and no information.
- **Remediation:** a versioned kitchen classifier that sets confidence per location with reasons.
- **Lesson:** test each factor's variance across real data. A factor that never moves is either broken or useless.

### 4. Keyword rules in the wrong context

**Source:** [projects/ai-evaluation](../projects/ai-evaluation/README.md), synthetic data.

- **Detection:** the evaluation's failure classification listed three spurious signals, each a correct keyword in the wrong context ("hiring reps this quarter" read as a buying timeline).
- **Root cause:** pattern matching without sentence meaning.
- **Remediation:** these cases are now the regression set an LLM extractor must pass.
- **Lesson:** failure classification turns an F1 score into a to-do list.

## Hypothetical failure modes

**Labeled hypothetical.** These describe common ways GTM systems fail. They are not events from any real engagement.

| Failure | Detection | Root cause | Remediation and prevention |
|---|---|---|---|
| Duplicate tasks after an integration retry | Reps report the same task twice | Retries without idempotency keys | Upsert on an idempotency key; dedupe check in the adapter |
| Silent enrichment decay | Bounce rate creeps up over months | A vendor's coverage changed; no monitoring | Weekly bounce and match rate by source with alert thresholds |
| Review queue nobody works | Queue age grows; signals never reach the CRM | Review designed without an owner or SLA | Named owner, age alert, and threshold review when the queue outgrows labor |
| Prompt injection in an inbound email | Model output includes instructions from the email | Untrusted text treated as instructions | Treat inbound text as data, allowlist actions, validate output, no irreversible write without review |
| Experiment winner that loses on revenue | Reply rate up, meetings flat | Optimizing a proxy metric | Primary metric = qualified meetings; replies as a diagnostic |
| Forecast model trained with leakage | Great backtest, poor live accuracy | Features measured after the outcome | Time-based feature cutoffs and walk-forward validation |

## Related

- [Architecture decision records](README.md)
- [Scenarios](scenarios.md)
- [SPX research: a leakage example](../research/spx-forecasting/README.md)
