# Contributing and publication rules

This is a public portfolio. Every addition follows these rules, including mine.

## Never publish

Code from an employer or client, client or customer data, call transcripts, passwords or account keys (API keys), or anything that identifies a client without their permission.

## Code

- Demos run on plain Python with nothing extra to install and no logins or keys. Any option that calls a live AI model is clearly marked and never runs during tests.
- Every demo has tests. Minimum scores the code must keep hitting (regression floors) live next to the code they protect.
- Run `python tests/run_all.py` before saving changes to the repo (committing). It runs every project's tests and checks links, links to page sections, diagrams (Mermaid blocks) and writing rules.

## Writing

- Plain English, specific, no filler. Every idea ties to a business problem and a number you can track.
- No em dashes. The repo check blocks them, along with a list of banned filler words.
