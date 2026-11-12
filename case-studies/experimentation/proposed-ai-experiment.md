# Proposed experiment: AI-researched first lines versus template first lines

**Evidence status: Proposed Experiment.** Not yet run. Written down before launch so the decision rule cannot be bent to fit the result.

The portfolio's hardest requirement is a measured growth result from AI with a clear method. This is the smallest experiment that would produce one honestly.

## Business problem

Personalized first lines take research time per contact. AI can draft them in seconds, at a model cost per contact. The question is whether AI-researched lines produce more qualified meetings per 1,000 delivered than a strong template, after paying for the model.

## Hypothesis

AI-researched first lines grounded in a verified signal (new leader in role, hiring surge, pricing page change) raise qualified meetings per 1,000 delivered by a margin large enough to cover their model cost, compared with a segment-specific template.

## Design

| Element | Choice |
|---|---|
| Population | One ICP segment, contacts with at least one verified signal |
| Randomization | Contact-level random assignment, stratified by seniority |
| Control | Segment template first line, same body, same sequence, same senders |
| Treatment | AI-written first line from the signal evidence, human-approved before send |
| Primary metric | Qualified meetings per 1,000 delivered (qualification rule fixed before launch) |
| Secondary | Positive reply rate, reply rate, unsubscribe and spam complaint rate |
| Guardrail | Bounce and complaint rates must not differ between arms |
| Sample | Set with a power calculation for two proportions before launch. Meetings are rare events, so expect thousands of delivered emails per arm |
| Duration | Until both arms reach the planned sample; no early stopping on peeks |

## Cost accounting

```
model cost per contact     = (input tokens x input price + output tokens x output price) / 1,000,000
review cost per contact    = reviewer minutes per line x loaded cost per minute
incremental meetings       = (treatment rate - control rate) x delivered / 1,000
cost per incremental meeting = (model cost + review cost) x treatment contacts / incremental meetings
```

Prices are taken from the vendor's published rates on the launch date and recorded with the result.

## Decision rule (fixed before launch)

- Adopt if the primary metric improves at the planned confidence and cost per incremental meeting is below the program's current cost per qualified meeting.
- If replies rise but qualified meetings do not, do not adopt: the model is writing lines that get attention from the wrong people.
- If there is no significant difference, keep the template and drop the cost.

## What gets reported either way

The full funnel per arm, the cost math, the confidence interval on the difference, and the decision taken. A null result is reported the same way as a win.

## Related

- [AI evaluation harness](../../projects/ai-evaluation/README.md): quality of the generated lines is checked before they reach a buyer
- [Experiment template](../../templates/experiment-template.md)
- [IMPACT.md](../../IMPACT.md)
