# ADR 0005: Deterministic code first, LLM last

- **Status:** accepted

## Context

Most steps in a sales and marketing (GTM) workflow can be done three ways: a fixed rule, a database lookup, or an AI model (an LLM, the kind of model behind ChatGPT). Models are flexible. But they cost money every time they run, they are slower, they can give different answers to the same input, and they can produce wrong answers that look right. A wrong score, a lead sent to the wrong rep, or a bad CRM update costs more than a slightly awkward sentence.

## Decision criteria

1. What a mistake at that step costs.
2. Whether the rule can be written down.
3. Cost and speed per run at full volume.
4. Whether the result can be explained to a seller.

## Chosen approach

| Step | How it is done | Why |
|---|---|---|
| Spotting a competitor's tool on a website | Text matching on the site's code and known tool signatures. The matching snippet and page URL are saved as proof | Exact, free, easy to explain |
| Removing duplicates by domain or phone | Clean the values into one format, then match exactly | The rule is known |
| Scores, tiers, lead routing, CRM updates | Plain code | Mistakes are expensive and must be explainable |
| Opening lines, summaries | AI model, with a fill-in-the-blank template as backup | Writing is what models are good at. The backup keeps the workflow running when the model fails |
| Pulling signals out of sales calls | Rules for things that match a known word list. A model is tested for things said in other words. Both go through the same checker | Measured, not assumed: see the test results |

## Rationale

In the test in this repo, the rules got a perfect score (F1 of 1.0, meaning no misses and no false alarms) on competitor mentions and feature requests, at zero cost. Every mistake the rules made came from context or from things said in different words. That is where a model is worth testing, and nowhere else.

## Tradeoffs

Rules need updating as the way people talk changes. That upkeep is visible and small compared with unchecked model output landing in the CRM.

## Reconsideration triggers

- A measured model result that stays just as accurate on the changes it makes automatically, cuts the number of items people must review, and costs less per correct signal than the reviewer time it saves.
- Updating the rules turns into a cost every week.
