# AI evaluation and observability harness

Runs on sample data, so the numbers describe the sample.

An AI demo shows one good output. A reliable AI system shows four more things: how often its outputs are right, how they go wrong, what each correct output costs, and an automatic check that fails if a change makes results worse. This harness (a test setup) does that for the [conversation intelligence](../conversation-intelligence/README.md) signal finder. It scores the plain-code version (fixed rules) and the Claude version in exactly the same way.

## What it measures

| Area | Question it answers | Why it matters to the business |
|---|---|---|
| Quality | For each signal type: when it flagged something, how often was it right (precision)? Of what was there, how much did it find (recall)? And one combined score for both (F1). Reported both across all signals together (micro) and as an average of each type's score (macro) | Wrong flags mean wrong CRM updates. Missed signals are ones reps never see. |
| Quality where it writes to the CRM | Of the signals written automatically, how often was it right? | This is what reaches the CRM with no person checking, so it has its own minimum. |
| Format | How often the answer is in the right format and backed by a real quote, and the reason code for each rejection | A model that returns a neat answer quoting something nobody said gets caught here, not after it reaches the CRM. |
| Failures | Every miss sorted into a type: `wrong_value`, `negation_or_context`, `spurious` (flagged something that was not there), `missed` | Tells you what to fix: the list of allowed values, handling of "not" and context, or coverage. |
| Human workload | Share of kept signals sent to a person to review | The labor cost of the design. A review queue nobody works is a failure nobody notices. |
| Speed | How long a typical call takes (p50, the middle) and a slow one (p95, slower than 95% of calls) | Decides whether this runs in batches or close to real time. |
| Cost | Input and output tokens (the units AI providers charge by), dollars per call, dollars per correct signal | Cost per correct signal is the number that compares an AI model with a rule fairly. |

Every run writes a summary file, `results/<extractor>_summary.json`, and a log for each call, `results/<extractor>_log.jsonl`, with the raw output, rejections and timing and cost data. The summary is saved in the repository, so a change in quality shows up when someone reviews the code change.

## Run it

```bash
cd projects/ai-evaluation
python -m evalkit.run_eval                    # rules baseline, free, about a second
python -m unittest discover -s tests -t .     # metric unit tests + regression gate
python -m evalkit.run_eval --extractor llm    # Claude, spends API credits
```

## Baseline results (rules extractor, measured 2026-11-12)

| Question | Answer |
|---|---|
| How many calls, and how many hand-labeled answers? | 12 / 57 |
| When it flagged a signal, how often was it right? (precision, all kept signals together) | 94.4% |
| Of the signals that were there, how many did it find? (recall, all kept signals together) | 89.5% |
| One combined score for accurate and thorough (F1, all kept signals together) | 91.9% |
| The same combined score, averaged across signal types so small types count equally (macro F1) | 90.9% |
| Of signals written automatically, how often was it right? / Of all real signals, how many were written automatically? | 100% / 38.6% |
| Share in the right format and backed by a real quote | 100% |
| Where signals went (automatic / review / dropped) | 22 / 32 / 0 |
| Time per call, typical and slow (p50 / p95) | under 2 ms per call |
| Cost | $0 |

Weakest signal types, by combined score (F1): `content_opportunity` (57.1%), `pain_point` (80%), `timing` (80%).

Nine failures, all readable in [results/rules_summary.json](results/rules_summary.json):

- **Flagged something that was not there (3):** "hiring twelve new reps this quarter" tagged as a buying timeline. "Budget for next year is approved" tagged as a later timeline. "Reps went back to spreadsheets" tagged as a manual-reporting pain. Each is a keyword in the wrong context.
- **Missed (4):** content requests phrased as "sure, if you have one" or "send something on that", where the topic was named in the seller's turn just before. A trial request phrased as "I will have our admin test it".
- **Wrong value (2):** "a couple of days" for a report, and "a forecast we can stand behind". In both, the rules found a different value of the same signal type.

That pattern is the argument for AI in this workflow. Rules fail on context and on people saying things in their own words, which is the part of language an AI model reads well. It stays a theory until the AI run is measured.

## The LLM comparison (not yet run)

Not yet run. The Claude version is built and goes through the same checks, but its results have not been measured, so none are reported here. The rule for deciding is written down before the run:

Switch to the AI version for a signal type only if, on test calls it has never seen:
1. signals written automatically stay at least 95% right,
2. the share sent to review falls below 40% (from 59%),
3. at least 98% of answers are in the right format and backed by a real quote, and rejected answers are logged, never written,
4. cost per correct signal is lower than the reviewer time it saves. That is a business input: reviewer cost per hour divided by signals reviewed per hour.

These minimums are in [thresholds.json](thresholds.json). If the AI wins only on types where buyers use their own words, such as pain points and content requests, the right design is a mix: rules for keyword types, AI for the rest.

## Limits of this evaluation

- **Same author for the calls, the answer key and the rules.** This makes the starting scores look better than they would be. The fix is a separate test set written and labeled by someone else, or real calls with personal details removed, labeled by two people with a score for how often they agree.
- **Small sample.** With only 57 labeled answers, the scores could move a lot by chance. Changing a single label can move one signal type's combined score by 10 points or more.
- **Exact matching only.** An answer must match both the signal type and the value exactly. A close-but-wrong value counts twice: once as a wrong flag and once as a miss.
- **No live monitoring yet.** In real use, the same summary would run every week on a sample checked by reviewers. It would send alerts when accuracy drops, when rejections spike, when the review queue gets old, and when cost per call rises.

## Related

- [Conversation intelligence pipeline](../conversation-intelligence/README.md)
- [AI and agents: evaluation and monitoring](../../docs/05-ai-and-agents/README.md)
- [Analytics: model evaluation and calibration](../../docs/06-analytics-and-prediction/README.md)
- [Proposed AI experiment](../../case-studies/experimentation/proposed-ai-experiment.md)
