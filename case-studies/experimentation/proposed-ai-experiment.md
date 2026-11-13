# Proposed experiment: AI-researched first lines versus template first lines

Not yet run. Written down before launch so the rule for deciding cannot be bent to fit the result.

The hardest thing for this portfolio to show is a measured growth result from AI, with a clear method. This is the smallest experiment that would produce one honestly.

## Business problem

A personalized first line takes research time for every contact. AI can draft one in seconds, but each contact costs money in AI usage. The question: do AI-researched lines produce more qualified meetings per 1,000 delivered emails than a strong template, after paying for the AI?

## Hypothesis

AI-researched first lines produce enough extra qualified meetings per 1,000 delivered emails to pay for the AI, compared with a template written for the segment. Each line must be based on a confirmed buying signal, such as a new leader in the role, a hiring surge, or a pricing page change.

## Design

| Element | Choice |
|---|---|
| Population | One ideal customer profile (ICP) segment, only contacts with at least one confirmed signal |
| Randomization | Each contact is randomly assigned to a group, with seniority balanced across both groups |
| Control | The segment's template first line, same body, same sequence, same senders |
| Treatment | A first line the AI writes from the signal, approved by a person before it is sent |
| Primary metric | Qualified meetings per 1,000 delivered (what counts as qualified is fixed before launch) |
| Secondary | Positive reply rate, reply rate, unsubscribe and spam complaint rate |
| Guardrail | Bounce and complaint rates must not differ between the two groups |
| Sample | Set before launch with a standard calculation of how many sends each group needs to detect a real difference. Meetings are rare, so expect thousands of delivered emails per group |
| Duration | Until both groups reach the planned number of sends; no stopping early because an early look seems good |

## Cost accounting

AI usage is billed per token, a small chunk of text. Input tokens are what the AI reads; output tokens are what it writes.

```
model cost per contact     = (input tokens x input price + output tokens x output price) / 1,000,000
review cost per contact    = reviewer minutes per line x loaded cost per minute
incremental meetings       = (treatment rate - control rate) x delivered / 1,000
cost per incremental meeting = (model cost + review cost) x treatment contacts / incremental meetings
```

Prices come from the vendor's published rates on launch day and are recorded with the result.

## Decision rule (fixed before launch)

- Adopt if qualified meetings go up with the planned level of confidence, and the cost per extra meeting is below what the program pays per qualified meeting today.
- If replies go up but qualified meetings do not, do not adopt: the AI is writing lines that catch the wrong people's attention.
- If there is no clear difference, keep the template and save the cost.

## What gets reported either way

The full funnel for each group, the cost math, the likely range of the true difference between groups, and the decision taken. A result of "no difference" is reported the same way as a win.

## Related

- [AI evaluation harness](../../projects/ai-evaluation/README.md): checks the quality of the AI-written lines before they reach a buyer
- [Experiment template](../../templates/experiment-template.md)
