# Technology ecosystem

This page lists the tools used in this work, grouped by the job each one does in a GTM (go-to-market) stack, and how each was used. The depth column shows the difference between building on a tool, setting it up for a team, and using it every day. Knowing a tool is not presented as having built on it.

| Depth | Meaning |
|---|---|
| Built on | Wrote code, workflows or integrations that read from or write to it |
| Administered | Configured it for a team: routing, fields, lifecycle, permissions |
| Daily user | Used it as part of selling or operating |

## CRM and systems of record

A CRM (customer relationship management system) holds the official records of accounts, contacts and deals.

| Tool | Depth | How |
|---|---|---|
| Salesforce | Built on | System of record for production GTM workflows: account research, call analysis writing to opportunities, expansion tasks |
| HubSpot | Administered | Lead routing and lifecycle administration |

## Sales engagement and conversation intelligence

Sales engagement tools send outreach (emails, calls, LinkedIn messages). Conversation intelligence tools record and analyze sales calls. A sequencer sends a planned series of outreach emails. Whitespace is revenue still available inside an existing customer.

| Tool | Depth | How |
|---|---|---|
| Gong, Salesloft | Built on | Call recordings as the input to AI call analysis: competitors, objections with quotes, next steps and whitespace written to the CRM. Salesloft also for sequencing, with personalized first lines written to fields the sequencer reads |
| Outreach | Daily user | Sequencing |
| Smartlead, Instantly | Daily user | Cold email at about 500K emails a month, under 3% bounce |
| EmailBison, HeyReach | Daily user | Cold email at volume and LinkedIn outreach for client programs |

## GTM intelligence and enrichment

Enrichment means filling in missing facts about a company or person (email, phone, size, tools used) from data vendors. A waterfall tries one vendor after another until one has the answer. A signal-based play is outreach triggered by a recent change at a company, such as a new leader or a hiring surge.

| Tool | Depth | How |
|---|---|---|
| Clay | Built on | Signal-based plays (new leader in role, hiring surges, tech stack, funding, job-post language, LinkedIn posts, pricing pages), waterfall enrichment, AI prompts for copy |
| Apollo, Prospeo, ZoomInfo | Daily user | Contact data inside enrichment waterfalls |
| Serper, Exa, Apify, Browser Use | Built on | Public-data list building: Google and Google Maps results, semantic search, scraping sites with no API |
| Overture Maps | Built on | Canonical location data for [RouteHero](../../projects/routehero/README.md), queried with DuckDB |

Semantic search finds results by meaning, not only exact words. Scraping means pulling information from web pages automatically. An API is the doorway a system offers for other systems to read its data. "Canonical" location data means the one official record for each place. DuckDB is a small, fast database tool.

## AI

Structured output means the AI returns its answer in fixed fields that code can read, instead of free text. A template fallback is a pre-written version used when the AI output is not good enough. A coding agent is an AI tool that writes and runs code.

| Tool | Depth | How |
|---|---|---|
| Claude (Anthropic) | Built on | Copy generation with template fallbacks, call extraction with structured output ([conversation intelligence](../../projects/conversation-intelligence/README.md)), and the coding agent used to build and run automations |
| OpenAI | Built on | Language tasks in client workflows |

## Workflow orchestration

Workflow orchestration tools connect other tools and run multi-step processes automatically. A Slack slash command is a short command typed into Slack (such as `/research`) that starts one of those processes.

| Tool | Depth | How |
|---|---|---|
| n8n | Built on | Production orchestration and Slack bots (account research and bounce-check slash commands) |
| Zapier | Built on | Workflow automations between GTM tools |

## Custom engineering

These are the programming languages and building blocks used to write custom software.

| Technology | Depth | Where |
|---|---|---|
| TypeScript, Next.js | Built on | RouteHero application |
| Python | Built on | The runnable demos in this repository |
| SQL, PostgreSQL, PostGIS | Built on | RouteHero data layer, row-level security, geospatial queries; [GTM ontology](../../projects/gtm-ontology/README.md) |
| REST APIs, webhooks, ETL | Built on | Connecting CRMs, enrichment sources and sequencers inside each client's existing stack |
| Mapbox | Built on | RouteHero maps |
| MCP | Built on | A RouteHero MCP server so owners can size their market from an AI assistant |

In plain terms: TypeScript and Next.js are used to build web apps. Python is a general programming language. SQL is the language for asking a database questions, PostgreSQL is a database, and PostGIS adds map and distance features to it. Row-level security means each customer can only see their own rows of data. Geospatial queries are questions about location, such as "which sites are within 20 miles." Webhooks are messages one system sends another the moment something happens. ETL (extract, transform, load) means moving data from one system to another. Mapbox draws maps. MCP (Model Context Protocol) is a standard way to let an AI assistant use an outside tool.

## Related

- [Architecture layers](architecture-layers.md)
- [Build vs buy vs extend](build-buy-extend.md)
