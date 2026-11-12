# AI evaluation and observability harness

**Evidence status: Synthetic Demonstration.** Measured on invented data. The numbers prove the harness works; they are not a production result.

An AI demo shows one good output. A reliable AI system shows how often outputs are right, how they fail, what each correct output costs, and fails the build when a change makes things worse. This harness does that for the [conversation intelligence](../conversation-intelligence/README.md) extractor, and it scores the deterministic baseline and the Claude extractor in exactly the same way.

## What it measures

| Area | Measure | Why it matters to the business |
|---|---|---|
| Quality | Precision, recall, F1 per signal type, micro and macro | Precision is the cost of wrong CRM writes. Recall is the signals reps never see. |
| Quality at the write boundary | Precision of auto-applied signals only | This is what reaches the CRM without a person. It has its own floor. |
| Structure | Schema-valid and grounded rate, rejection codes | A model that returns valid JSON quoting things nobody said fails here, not in production. |
| Failures | Each miss classified: `wrong_value`, `negation_or_context`, `spurious`, `missed` | Tells you what to fix: vocabulary, negation handling, or coverage. |
| Human load | Share of kept signals routed to review | The labor cost of the design. A review queue nobody works is a silent failure. |
| Latency | p50, p95 per call | Determines batch versus near-real-time. |
| Cost | Input and output tokens, USD per call, USD per correct signal | Cost per correct signal is the unit that compares a model with a rule. |

Every run writes `results/<extractor>_summary.json` and a per-call log `results/<extractor>_log.jsonl` with raw output, rejections and telemetry. The summary is committed so that a change in quality shows up in a code review diff.

## Run it

```bash
cd projects/ai-evaluation
python -m evalkit.run_eval                    # rules baseline, free, about a second
python -m unittest discover -s tests -t .     # metric unit tests + regression gate
python -m evalkit.run_eval --extractor llm    # Claude, spends API credits
```

## Baseline results (rules extractor, measured 2026-11-12)

| Measure | Value |
|---|---|
| Calls / labels | 12 / 57 |
| Micro precision / recall / F1 (kept) | 0.944 / 0.895 / 0.919 |
| Macro F1 | 0.909 |
| Auto-applied precision / recall | 1.000 / 0.386 |
| Schema-valid and grounded | 1.000 |
| Routing (auto / review / drop) | 22 / 32 / 0 |
| Latency p50 / p95 | under 2 ms per call |
| Cost | $0 |

Weakest types: `content_opportunity` (F1 0.571), `pain_point` (0.80), `timing` (0.80).

Nine failures, all readable in [results/rules_summary.json](results/rules_summary.json):

- **Spurious (3):** "hiring twelve new reps this quarter" tagged as buying timeline; "budget for next year is approved" tagged as a later timeline; "reps went back to spreadsheets" tagged as a manual-reporting pain. Each is a keyword in the wrong context.
- **Missed (4):** content requests phrased as "sure, if you have one" or "send something on that", where the topic lives in the seller's previous turn; a trial request phrased as "I will have our admin test it".
- **Wrong value (2):** "a couple of days" for a report, and "a forecast we can stand behind", where the rules found a different value of the same type.

The pattern is the case for an LLM in this workflow: rules fail on context and paraphrase, which is the part of language a model reads well. That is a hypothesis until the LLM run is measured.

## The LLM comparison (not yet run)

**Evidence status: Proposed Experiment.** The Claude extractor is implemented and validated by the same code path, but its results have not been measured, so none are reported here. The decision rule is written down before the run:

Adopt the LLM extractor for a signal type only if, on held-out data:
1. auto-applied precision stays at or above 0.95,
2. review share falls below 40% (from 59%),
3. schema-valid and grounded rate is at least 98%, with rejected outputs logged, never written,
4. cost per correct signal is lower than the reviewer time it saves, which is a business input: reviewer cost per hour divided by signals reviewed per hour.

These floors are in [thresholds.json](thresholds.json). If the model wins only on paraphrase-heavy types such as pain points and content requests, the right design is a hybrid: rules for dictionary types, the model for the rest.

## Limits of this evaluation

- **Same author for data, labels and rules.** This inflates baseline scores. The fix is a held-out set written and labeled by someone else, or redacted real calls with two labelers and an agreement score.
- **Small sample.** 57 labels give wide error bars. One flipped label moves a per-type F1 by 0.1 or more.
- **Exact (type, value) matching.** A near-miss value counts as both a false positive and a false negative.
- **No production monitoring yet.** In production the same summary would run weekly on a reviewer-labeled sample, with alerts on precision drop, rejection-rate spikes, review-queue age and cost per call.

## Related

- [Conversation intelligence pipeline](../conversation-intelligence/README.md)
- [AI and agents: evaluation and monitoring](../../docs/05-ai-and-agents/README.md)
- [Analytics: model evaluation and calibration](../../docs/06-analytics-and-prediction/README.md)
- [Proposed AI experiment](../../case-studies/experimentation/proposed-ai-experiment.md)
- [IMPACT.md](../../IMPACT.md)
