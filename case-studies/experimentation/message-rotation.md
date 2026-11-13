# Experiment: message rotation versus a static split

Run in simulation in the [GTM Learning Engine](../../projects/gtm-learning-engine/README.md).

## Question

Say several email messages go to the same group of contacts. Do you get more positive replies by dropping the losing messages and sending more volume to the winner? Or by splitting volume evenly across all messages for the whole campaign?

## Design

| Element | Choice |
|---|---|
| Unit | One delivered email |
| Segments | Each mix of ideal customer profile (ICP) and seniority gets its own set of messages |
| Rule being tested | No message is judged before 400 deliveries. A message is dropped, and a winner given more volume, only at 95% confidence, meaning the gap is very unlikely to be chance |
| Comparison | An even split across all messages for the whole run |
| Main number (simulation) | Positive replies |
| Check first | Bounces are checked before anyone blames the copy |

## Result

In simulation the rotation produced 56% more positive replies than the even split.

## What the result means and does not mean

- It shows the rules work when messages really do perform differently: they find the better message and move volume to it without judging too early.
- The size of the gain comes from how far apart the simulated messages' reply rates were. A real campaign whose messages perform about the same would see a small gain or none.
- Positive replies are only a stand-in. The real version should be judged on qualified meetings per 1,000 delivered emails. Otherwise it learns to win replies that never turn into pipeline.

## How to run it on a real program

1. Set the main number (qualified meetings per 1,000 delivered) and the minimum number of sends before launch.
2. Split contacts into segments first, then test inside each segment.
3. Keep a small even-split group running on purpose, so the gain is measured, not assumed.
4. Report with the [experiment template](../../templates/experiment-template.md).

## Related

- [Analytics: experiment design](../../docs/06-analytics-and-prediction/README.md)
- [Proposed AI experiment](proposed-ai-experiment.md)
