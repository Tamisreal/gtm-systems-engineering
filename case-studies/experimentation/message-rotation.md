# Experiment: message rotation versus a static split

**Evidence status: Synthetic Demonstration.** Simulated with invented reply rates in the [GTM Learning Engine](../../projects/gtm-learning-engine/README.md). Not a result from a real outbound program.

## Question

When several messages run against the same segment, does a policy that retires losing messages and moves volume to the winner produce more positive replies than splitting volume evenly for the whole campaign?

## Design

| Element | Choice |
|---|---|
| Unit | One delivered email |
| Segments | Each ICP x seniority combination runs its own message library |
| Policy under test | No message judged before 400 delivered. A message is retired, and a winner scaled, only at 95% confidence |
| Control | Static even split across all messages for the full run |
| Primary metric (simulation) | Positive replies |
| Pre-check | Bounces are checked before copy is blamed |

## Result

In simulation the rotation produced 56% more positive replies than the static split.

## What the result means and does not mean

- It shows the rules behave correctly when messages truly differ: they find the better message and move volume to it without judging too early.
- The size of the lift is set by the invented gap between message reply rates. A real program with messages that perform alike would see a small lift or none.
- Positive replies are a proxy. The production version should be judged on qualified meetings per 1,000 delivered, or it learns to win replies that never become pipeline.

## How to run it on a real program

1. Fix the primary metric (qualified meetings per 1,000 delivered) and minimum sample before launch.
2. Segment first, then test inside segments.
3. Keep a small static-split holdout running so the lift is measured, not assumed.
4. Report with the [experiment template](../../templates/experiment-template.md).

## Related

- [Analytics: experiment design](../../docs/06-analytics-and-prediction/README.md)
- [Proposed AI experiment](proposed-ai-experiment.md)
