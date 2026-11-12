# Technology ecosystem

Technologies grouped by the job they do in a GTM stack, with how each one has been used in this work. The depth column separates building on a tool from administering it or working in it daily. Familiarity is not presented as integration.

| Depth | Meaning |
|---|---|
| Built on | Wrote code, workflows or integrations that read from or write to it |
| Administered | Configured it for a team: routing, fields, lifecycle, permissions |
| Daily user | Used it as part of selling or operating |

## CRM and systems of record

| Tool | Depth | How |
|---|---|---|
| Salesforce | Built on | System of record for production GTM workflows: account research, call analysis writing to opportunities, expansion tasks |
| HubSpot | Administered | Lead routing and lifecycle administration |

## Sales engagement and conversation intelligence

| Tool | Depth | How |
|---|---|---|
| Gong, Salesloft | Built on | Call recordings as the input to AI call analysis: competitors, objections with quotes, next steps and whitespace written to the CRM. Salesloft also for sequencing, with personalized first lines written to fields the sequencer reads |
| Outreach | Daily user | Sequencing |
| Smartlead, Instantly | Daily user | Cold email at about 500K emails a month, under 3% bounce |
| EmailBison, HeyReach | Daily user | Cold email at volume and LinkedIn outreach for client programs |

## GTM intelligence and enrichment

| Tool | Depth | How |
|---|---|---|
| Clay | Built on | Signal-based plays (new leader in role, hiring surges, tech stack, funding, job-post language, LinkedIn posts, pricing pages), waterfall enrichment, AI prompts for copy |
| Apollo, Prospeo, ZoomInfo | Daily user | Contact data inside enrichment waterfalls |
| Serper, Exa, Apify, Browser Use | Built on | Public-data list building: Google and Google Maps results, semantic search, scraping sites with no API |
| Overture Maps | Built on | Canonical location data for [RouteHero](../../projects/routehero/README.md), queried with DuckDB |

## AI

| Tool | Depth | How |
|---|---|---|
| Claude (Anthropic) | Built on | Copy generation with template fallbacks, call extraction with structured output ([conversation intelligence](../../projects/conversation-intelligence/README.md)), and the coding agent used to build and run automations |
| OpenAI | Built on | Language tasks in client workflows |

## Workflow orchestration

| Tool | Depth | How |
|---|---|---|
| n8n | Built on | Production orchestration and Slack bots (account research and bounce-check slash commands) |
| Zapier | Built on | Workflow automations between GTM tools |

## Custom engineering

| Technology | Depth | Where |
|---|---|---|
| TypeScript, Next.js | Built on | RouteHero application |
| Python | Built on | The runnable demos in this repository |
| SQL, PostgreSQL, PostGIS | Built on | RouteHero data layer, row-level security, geospatial queries; [GTM ontology](../../projects/gtm-ontology/README.md) |
| REST APIs, webhooks, ETL | Built on | Connecting CRMs, enrichment sources and sequencers inside each client's existing stack |
| Mapbox | Built on | RouteHero maps |
| MCP | Built on | A RouteHero MCP server so owners can size their market from an AI assistant |

## Related

- [Architecture layers](architecture-layers.md)
- [Build vs buy vs extend](build-buy-extend.md)
