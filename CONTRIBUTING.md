# Contributing and publication rules

This is a public portfolio. Every addition follows these rules, including my own.

## Evidence

- Every result carries one label: Measured / Verified, Historical / Pending Verification, Synthetic Demonstration, Proposed Experiment, or Exploratory Research.
- A result moves to Measured / Verified only with a completed [impact record](templates/impact-record-template.md): source, definition, formula, period, attribution method, confounders.
- Sourced and influenced pipeline are reported separately and never summed.
- No result is attributed to AI unless a method (holdout, pre/post with control) isolates the AI's contribution.
- Simulated numbers are never presented as business outcomes.
- Experiments are written up with the [experiment template](templates/experiment-template.md) before launch.
- Decisions that would be expensive to reverse get an [ADR](templates/adr-template.md). "Observed results" stays empty until there is data.

## Never publish

Employer or client code, client or customer data, call transcripts, API keys or credentials, unverified revenue claims, or anything that identifies a client without permission.

## Code

- Demos run with the Python standard library and no credentials. Optional live-model paths are clearly marked and never run in tests.
- Every demo has tests. Regression floors live next to the code they protect.
- Run `python tests/run_all.py` before committing: it runs every project's tests and checks links, anchors, Mermaid blocks and writing rules.

## Writing

- Plain English, specific, no filler. Every concept connects to a business problem and a metric.
- No em dashes. The repository check enforces this and a list of banned filler words.
