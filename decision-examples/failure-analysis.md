# Failure analysis

Failures from my own work first, then common ways sales and marketing systems break.

## Real failures

### 1. Tier A came back empty

**Source:** RouteHero development, 2026-09. Written up in [decision record 0004](adr/0004-routehero-remove-circular-factor.md).

- **How it was spotted:** after contract value was removed from the score, the tier list for 2,785 real Spring, TX accounts had zero Tier A accounts. The top score was 74, and the cutoff was 75.
- **Real cause:** removing a factor worth 40 points pushed every score down. The cutoffs had been set by what feels like a high number, not from data.
- **Fix:** cutoffs reset from where real scores actually fell. The top 5% of accounts scored 56 or more, and the top 15% scored 50 or more. That gave A at 60 and B at 45.
- **Prevention:** the cutoffs are a versioned setting saved with every score, so any change is visible and can be undone.
- **What to watch:** the share of accounts in each tier, per territory. A Tier A that is empty or too full triggers an alert.
- **Lesson:** whenever a score's inputs change, look at how the new scores spread out before the results go live.

### 2. "Nursing homes barely exist"

**Source:** RouteHero data source review, 2026-09-12. Written up in [decision record 0001](adr/0001-routehero-data-source.md).

- **How it was spotted:** the new data source seemed to have almost no senior-care facilities, a valuable institutional segment.
- **Real cause:** a labeling mix-up. The search used a business-type label the dataset does not use. The dataset files these places under four other labels.
- **Fix:** added those four labels. 878 facilities showed up in the same area.
- **Prevention:** label lists are checked against the source's real list of labels, and counts per label are compared across sources before deciding any data is missing.
- **Lesson:** a surprising gap in a dataset is more often a problem with the search than with the data. Check the search first.

### 3. Constant factor in the score

**Source:** RouteHero code history.

- **How it was spotted:** one scoring factor (kitchen confidence: how sure the system is that a location has a commercial kitchen) was the same for every account.
- **Real cause:** it was hard-coded to one value for every location. It added the same number to everyone and told you nothing.
- **Fix:** a versioned kitchen checker that sets the confidence for each location and records the reasons.
- **Lesson:** check that each factor actually changes across real data. A factor that never moves is either broken or useless.

### 4. Keyword rules in the wrong context

**Source:** [projects/ai-evaluation](../projects/ai-evaluation/README.md), sample data.

- **How it was spotted:** the test's breakdown of mistakes listed three false signals. Each was the right keyword used in the wrong context ("hiring reps this quarter" was read as a buying timeline).
- **Real cause:** matching words without understanding the sentence.
- **Fix:** these cases are now a fixed test set that any AI model doing this job must pass.
- **Lesson:** sorting mistakes by type turns a single accuracy score (F1) into a to-do list.

## Common failure modes

| Failure | How it is spotted | Real cause | Fix and prevention |
|---|---|---|---|
| Duplicate tasks after an integration retries | Reps see the same task twice | The retry was not safe to run twice without duplicates (no unique ID per request, called an idempotency key) | Give each request a unique ID and update the existing record if that ID is already there; check for duplicates in the connector |
| Enrichment data quietly getting worse | Bounce rate creeps up over months | A vendor's coverage changed, and nobody was watching | Weekly bounce rate and match rate by source, with alert levels |
| Review queue nobody works | Items in the queue get older; signals never reach the CRM | The review step was set up with no owner and no response-time target | A named owner, an alert on item age, and a cutoff review when the queue outgrows the people available |
| Hidden instructions in an inbound email (prompt injection) | The AI model's output follows instructions written in the email | Outside text was treated as instructions | Treat inbound text as data only, allow only a set list of actions, check the output, and never make a change that cannot be undone without a person's review |
| Test "winner" that loses on revenue | Reply rate up, meetings flat | Chasing a stand-in number instead of the real goal | Main metric = qualified meetings; replies are only a diagnostic |
| Forecast model built with information it would not have had at the time | Great results on past data, poor accuracy in real use | It used details recorded after the outcome | Cut off each input at the date of the prediction, and test only on days after the ones it learned from |

## Related

- [Architecture decision records](README.md)
- [Scenarios](scenarios.md)
- [SPX research: a leakage example](../research/spx-forecasting/README.md)
