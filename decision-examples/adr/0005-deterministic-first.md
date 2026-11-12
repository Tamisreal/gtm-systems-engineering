# ADR 0005: Deterministic code first, LLM last

- **Status:** accepted
- **Evidence status:** Design principle applied in [GTM Learning Engine](../../projects/gtm-learning-engine/README.md) and measured in [projects/ai-evaluation](../../projects/ai-evaluation/README.md) (synthetic)

## Context

Most steps in a GTM workflow can be done by a rule, a query or a model. Models are flexible, but they cost money per call, add latency, vary between runs and can produce plausible wrong output. A wrong score, route or CRM write costs more than a slightly awkward sentence.

## Decision criteria

1. Cost of an error at that step.
2. Whether the rule can be written down.
3. Cost and latency per run at production volume.
4. Ability to explain the output to a seller.

## Chosen approach

| Step | Implementation | Why |
|---|---|---|
| Competitor detection on websites | String match on script tags and fingerprints, with the snippet and URL stored as evidence | Exact, free, explainable |
| Dedupe on domain or phone | Normalization and exact match | Rule is known |
| Scores, tiers, routing, CRM writes | Code | Errors are expensive and must be explainable |
| Opening lines, summaries | LLM, with a template fallback | Language is the model's strength; the fallback keeps the workflow running when the model fails |
| Signal extraction from calls | Rules for dictionary types, model candidate for paraphrase, both behind the same validator | Measured, not assumed: see the eval |

## Rationale

In the synthetic eval, the rules extractor scored F1 1.0 on competitor mentions and feature requests at zero cost. Its failures were all context and paraphrase. That is where a model is worth testing, and nowhere else.

## Tradeoffs

Rules need maintenance as language changes. That maintenance cost is visible and small next to unreviewed model output reaching the CRM.

## Reconsideration triggers

- A measured LLM result that holds auto-apply precision while cutting review load, at lower cost per correct signal than the reviewer time saved.
- Rule maintenance becoming a recurring weekly cost.
