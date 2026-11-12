# SEO and generative engine optimization

Search engines and AI answer engines both decide whether a company is found, understood and cited when a buyer researches a problem. This page explains the technical and content mechanics of classic SEO, how AI assistants retrieve and cite sources, and how to measure both honestly given that much of the value is invisible to standard attribution.

## Technical SEO

Technical SEO ensures pages can be fetched, understood and chosen for the index. It does not make content rank on its own, but failures here cap everything else.

**Crawlability.** Can a crawler reach the page?

- `robots.txt` controls what compliant crawlers may fetch. Blocking a path in robots.txt prevents crawling, not indexing: a blocked URL with external links can still appear in results without a description.
- Internal links are the main discovery path. Orphan pages (no internal links) are discovered late or not at all.
- JavaScript-rendered content can be indexed by Google, but rendering is deferred and other crawlers (including many AI crawlers) may not execute JavaScript. Server-render or statically generate important content.

**Indexability.** Will the page be stored?

- `<meta name="robots" content="noindex">` or an `X-Robots-Tag` header removes a page from the index. The crawler must be able to fetch the page to see it, so do not combine noindex with a robots.txt block.
- Thin, duplicate or near-duplicate pages may be crawled but not indexed. Search Console's page indexing report shows reasons.

**Canonical tags.** `<link rel="canonical" href="...">` tells search engines which URL is the preferred version when the same content is reachable at several URLs (tracking parameters, trailing slashes, HTTP vs HTTPS, filtered listings). It is a hint, not a directive. Common errors: canonicals pointing to redirected or noindexed URLs, every page canonicalized to the homepage, canonicals that conflict with sitemap URLs.

**Sitemaps.** An XML sitemap lists canonical, indexable URLs with optional `lastmod`. Include only URLs you want indexed, keep `lastmod` accurate (update it only when content meaningfully changes), and submit through Search Console and Bing Webmaster Tools.

**Core Web Vitals.** Google's user-experience metrics, measured from real-user field data:

| Metric | Measures | "Good" threshold (per Google's published guidance) |
|---|---|---|
| LCP, Largest Contentful Paint | Loading: when the main content renders | 2.5 seconds or less |
| INP, Interaction to Next Paint | Responsiveness to user input (replaced FID in 2024) | 200 milliseconds or less |
| CLS, Cumulative Layout Shift | Visual stability | 0.1 or less |

Assessed at the 75th percentile of page loads. Verify thresholds against current Google documentation before setting targets. Field data (CrUX, real-user monitoring) is what counts; lab tools such as Lighthouse diagnose causes. Typical B2B site fixes: compress and size hero images, defer third-party scripts (chat widgets, tag managers and intent pixels often dominate INP), and reserve space for embeds and cookie banners to prevent layout shift.

**Common technical failures on B2B sites.**

| Failure | Symptom | Check | Fix |
|---|---|---|---|
| Staging or preview site indexed | Duplicate pages in results on a non-production domain | `site:` search, Search Console | Auth-protect previews; noindex header on non-production |
| Marketing site rebuild without redirects | Traffic drop after launch, 404s in Search Console | Crawl old URL list against new site | 301 map from every old URL with traffic or links |
| Client-side rendered content | Page indexed with little text | Fetch raw HTML with curl; URL inspection | Server-side or static rendering |
| Parameter duplicates | Many URLs per page (UTM, filters) | Crawl report, canonical audit | Self-referencing canonicals; consistent internal links |
| Gated content only | Thin indexable pages | Content audit | Ungated summary page with the gated asset as an option |
| Heavy third-party scripts | Poor INP in field data | Performance trace of main thread | Defer, load on interaction, remove unused tags |

A quick crawlability check from the command line:

```bash
curl -sI https://www.example.com/pricing | grep -i -E "^(HTTP|x-robots-tag|location)"
curl -s https://www.example.com/pricing | grep -i -E "rel=\"canonical\"|name=\"robots\""
curl -s https://www.example.com/robots.txt
```

## Search intent

Every query has an intent, and a page ranks when it matches it.

| Intent | Example B2B query | Page type that matches |
|---|---|---|
| Informational | "how to calculate pipeline coverage" | Explainer or guide |
| Commercial investigation | "best revenue analytics tools", "X vs Y" | Comparison, alternatives page |
| Transactional | "X pricing", "X demo" | Pricing, demo request |
| Navigational | "X login" | The relevant app or brand page |

Check intent by looking at what currently ranks. If the results are all listicles, a product page will not rank for that query regardless of optimization. Map each target query to one page to avoid several pages competing for the same intent.

## Structured data

Structured data describes page content in machine-readable form, most commonly as schema.org vocabulary in JSON-LD.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Co",
  "url": "https://www.example.com",
  "logo": "https://www.example.com/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/example-co",
    "https://github.com/example-co"
  ],
  "description": "Example Co builds revenue analytics software for B2B SaaS companies."
}
</script>
```

Useful types for B2B sites: `Organization` (entity identity and `sameAs` links to official profiles), `SoftwareApplication` (product name, category, operating system, offers), `Article` (author, dates), `BreadcrumbList`, `FAQPage`.

Expectations: Google restricts which sites receive FAQ rich results (it limited them largely to well-known authoritative government and health sites in 2023), and rich result eligibility for any type is at the search engine's discretion. Treat schema as machine-readable context about entities and relationships, not a guaranteed visual feature. Schema must match visible page content; marking up content that is not on the page violates Google's guidelines. Validate with the Rich Results Test and the Schema Markup Validator.

## Content architecture

**Topic clusters.** A pillar page covers a broad topic (for example, "pipeline forecasting") and links to cluster pages covering subtopics in depth (weighted pipeline, stage probabilities, forecast accuracy). Cluster pages link back to the pillar and to each other where relevant. This gives crawlers a clear structure and gives readers a path.

**Internal links.**

- Link with descriptive anchor text that names the destination topic, not "click here."
- Link from high-traffic pages to pages you want to rank.
- Keep important pages within a few clicks of the homepage.
- Audit for orphans and broken links on a schedule.

**URL structure.** Short, stable, readable paths that reflect the hierarchy (`/guides/forecasting/weighted-pipeline`). Changing URLs requires 301 redirects and loses some signal in transition, so pick a structure and keep it.

**Programmatic pages.** Templated pages from data (integrations, locations, comparisons) can scale coverage, but thin templated pages with little unique content tend to be crawled and not indexed. Each page needs content a person would find useful on its own.

## Organic acquisition

Organic search for B2B usually contributes in two ways: direct conversions (demo requests from comparison and pricing pages) and assisted research (buyers who read guides and return later via direct or branded search). The second is larger in many B2B funnels and mostly invisible to last-touch attribution.

Content that tends to produce pipeline: comparison and alternatives pages for real competitors, integration pages, pricing explanation, and practitioner guides on problems the product solves. Content that tends to produce traffic without pipeline: broad top-of-funnel topics far from the product.

Measure organic by pipeline sourced from organic landing pages, branded search volume over time, and self-reported attribution, not by sessions alone.

## Generative engine optimization

Generative engine optimization (GEO) is the practice of making content likely to be retrieved, understood and cited by AI answer engines: assistants that browse or search (ChatGPT search, Perplexity, Google AI Overviews and AI Mode, Microsoft Copilot, Claude with web search).

**How AI answer engines retrieve and cite.** Mechanics vary by product and are not fully documented, but the general pattern is:

1. The assistant rewrites the user's question into one or more search queries.
2. It retrieves results from a search index (its own, or a partner's).
3. It fetches and reads passages from selected pages.
4. It generates an answer from those passages and may cite some of them.

Separately, a model's training data shapes what it "knows" about a brand without browsing. Both paths matter: retrieval affects current answers with citations; training data affects unbrowsed answers and how the model interprets retrieved content.

Implication: classic search visibility still matters, because many assistants retrieve from search indexes. Pages that do not rank or are not indexed are less likely to be retrieved.

**Being citable.**

- **Clear entity definitions.** State plainly what the company is, what the product does, who it is for and what category it belongs to, in a sentence that can stand alone when extracted.
- **Factual, specific pages.** Passages with definitions, formulas, comparisons and concrete criteria are easier to quote than vague marketing copy.
- **Self-contained sections.** Each section should make sense when extracted without the rest of the page. Use descriptive headings that match how people ask questions.
- **Consistent naming across the web.** Same company name, product name and description on the website, LinkedIn, GitHub, directories and review sites. Inconsistent naming makes entity resolution harder for any system.
- **Third-party mentions.** Assistants often cite sources other than the vendor: review sites, community discussions, industry publications, comparison articles. Being mentioned accurately on credible third-party pages matters, and cannot be fully controlled.
- **Freshness.** Visible dates and current information, especially for pricing, features and comparisons.

**AI crawler access.** AI companies publish user agents for their crawlers. Examples include `GPTBot` and `OAI-SearchBot` (OpenAI), `ClaudeBot` (Anthropic), and `PerplexityBot` (Perplexity). Google uses the `Google-Extended` token in robots.txt to control use of content for some AI training, separate from Googlebot search crawling. Names and purposes change, so check each vendor's current documentation.

```text
# robots.txt: allow search and AI crawlers on public content
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: *
Disallow: /app/
Sitemap: https://www.example.com/sitemap.xml
```

Decide deliberately: blocking training crawlers and blocking search or retrieval crawlers have different consequences, and some vendors use separate agents for each. Check server logs to confirm which agents actually fetch the site, since robots.txt compliance is voluntary.

**llms.txt.** A proposed convention: a Markdown file at `/llms.txt` that summarizes a site and links to its most useful pages for language models. It is a proposal, not a standard, and adoption by major AI providers for retrieval or ranking is uncertain and largely undocumented. It is cheap to publish; do not expect measurable effect from it alone.

## AI answer visibility tracking

There is no AI equivalent of Search Console that reports impressions across assistants. The practical method is a fixed prompt panel run on a schedule.

**Method.**

1. Build a prompt set of 30 to 100 questions buyers plausibly ask, grouped by intent: category ("what tools help with revenue forecasting"), problem ("how do I fix pipeline forecast misses"), comparison ("X vs Y"), and brand ("what is X").
2. Run each prompt on each assistant on a fixed schedule (weekly or monthly), with consistent settings, logged out or in a clean profile where possible, and with location noted.
3. Run each prompt several times per cycle, because answers vary between runs.
4. Store the raw answer, cited URLs and timestamps.
5. Extract with code or a validated classifier: brand mentioned (yes/no), brand cited (own domain in citations), position of first mention, sentiment, and which competitors appear.

```text
prompt_runs(run_id, prompt_id, assistant, model_label, run_at, answer_text, cited_urls[])
mentions(run_id, entity, mentioned, cited, first_position, sentiment)
```

**Caveats.** Results vary by run, user history, location and model version. Small prompt panels produce noisy rates; report with run counts and look at trends over several cycles rather than week-to-week changes. The prompt set reflects your guesses about buyer questions, so refresh it from sales call transcripts and search query data.

## Attribution limitations

- **Zero-click answers.** Search features and AI answers resolve many queries without a visit. Influence occurs with no session to attribute.
- **Referrer loss.** Some assistant traffic arrives with a referrer, and some arrives as direct traffic (copied links, app-based browsing, stripped referrers). AI-referred sessions are undercounted in analytics.
- **Delayed and offline influence.** A buyer reads an AI answer naming three vendors, then searches the brand a week later. Last touch says branded search.
- **Self-reported attribution.** A required free-text or picklist field on demo forms ("How did you hear about us?") captures channels analytics misses, including AI assistants, podcasts and peer referrals. Code free text into categories. It has recall bias, but it is often the only signal for dark channels. Compare self-reported against tracked source per lead.

## Experiment design for SEO and GEO

Search and AI visibility are hard to test because you do not control the ranking system and outcomes are noisy.

- **Page-level split tests.** Group similar templated pages (integration pages, comparison pages), randomly assign half to a change (title format, added schema, rewritten intro), keep half as control, and compare organic clicks over the same period. Requires many comparable pages; does not work for a handful of unique pages.
- **Pre/post with control groups.** When randomization is impossible, compare the change in treated pages against the change in a similar untreated group over the same window (difference-in-differences). This removes site-wide and seasonal effects that a naive pre/post comparison absorbs.
- **Time-series caveats.** Algorithm updates, seasonality, competitor changes and indexing lag all move metrics independently of your change. Use windows long enough to cover re-crawling (often several weeks), avoid launching tests across known major updates, and treat single-page before/after charts as anecdotes.
- **GEO tests.** Run the prompt panel before and after content changes on a defined page set, with an untouched page set as control. Expect high variance; look for consistent direction across several cycles.

## Implementation sequence

Order work by what caps everything downstream:

1. **Access and indexing.** Fix robots rules, noindex errors, canonicals, redirects and sitemaps. Confirm AI crawler policy is a deliberate choice. Nothing else matters for pages that cannot be fetched.
2. **Entity clarity.** One canonical description of the company and product, used on the homepage, `Organization` schema, and every official profile linked in `sameAs`.
3. **Commercial-intent pages.** Pricing explanation, comparison and alternatives pages, integration pages. These sit closest to pipeline.
4. **Topic clusters.** Practitioner guides on the problems the product solves, interlinked, with extractable definitions and formulas.
5. **Third-party presence.** Accurate directory and review-site profiles; contributions to credible industry publications and communities.
6. **Measurement.** Search Console and analytics hygiene, the self-reported attribution field, and the prompt panel, all running before content changes so there is a baseline.

Steps 1, 2 and 6 are mostly one-time engineering work. Steps 3 to 5 are ongoing content operations with an owner and a publishing cadence.

## What can go wrong

- **Optimizing for the panel instead of the buyer.** Rewriting pages to win a fixed prompt set can overfit to prompts you chose. Rotate in new prompts sourced from real buyer language.
- **Treating mentions as pipeline.** A rising mention rate is a leading indicator. Tie it to branded search, self-reported attribution and sourced pipeline before claiming business impact.
- **Classifier errors in tracking.** Brand-mention extraction misses misspellings and confuses similarly named companies. Validate the extractor on a labeled sample of answers, the same way as any [AI evaluation](../../projects/ai-evaluation/README.md).
- **Blocking crawlers by accident.** A broad `Disallow` added during a migration, a WAF rule that blocks unfamiliar user agents, or bot protection that serves challenges to crawlers. Check server logs, not only robots.txt.
- **Inaccurate third-party descriptions.** Outdated directory listings and old review-site descriptions get retrieved and repeated. Audit and correct the profiles you control.

## What would change the approach

- Sites with few pages favor qualitative improvements and pre/post with controls over split tests.
- If assistants publish referral or impression data for publishers, measurement shifts from prompt panels toward direct reporting.
- Regulated or sensitive content may justify blocking some AI crawlers despite visibility cost.

## A proposed measurement framework

This is a proposed framework for teams to adapt. It is not a report of results.

| Metric | Definition | Formula | Data source | Cadence |
|---|---|---|---|---|
| Indexed coverage | Share of intended pages indexed | indexed canonical URLs / URLs in sitemap | Search Console page indexing | Monthly |
| Core Web Vitals pass rate | Share of URLs passing all three CWV at p75 | URLs good on LCP, INP and CLS / URLs with field data | CrUX, Search Console | Monthly |
| Non-branded organic clicks | Clicks on queries without the brand name | sum(clicks) where query excludes brand terms | Search Console | Weekly |
| Branded search demand | Interest in the brand by name | branded query impressions, trend vs prior period | Search Console | Monthly |
| Organic-sourced pipeline | Pipeline from opps whose sourcing touch is organic | sum(opp amount) where source = organic | CRM plus web analytics | Monthly |
| AI-referred sessions | Sessions with an AI assistant referrer | sessions where referrer in assistant domain list | Web analytics | Weekly |
| AI mention rate | Share of prompt runs mentioning the brand | runs with brand mentioned / total runs | Prompt panel | Monthly |
| AI citation rate | Share of prompt runs citing an owned URL | runs citing own domain / total runs | Prompt panel | Monthly |
| Average mention position | Where the brand first appears in answers that mention it | mean(first_position) over runs with a mention | Prompt panel | Monthly |
| Competitor share of voice | Brand mentions relative to competitor set | brand mentions / mentions of all tracked entities | Prompt panel | Monthly |
| Mention sentiment | Tone of answers mentioning the brand | positive runs / runs with a mention | Prompt panel plus validated classifier | Monthly |
| Self-reported AI or search | Leads naming search or an AI assistant | leads coded search or AI / leads with a response | Demo form field | Monthly |

## Related

- [Product marketing as structured data](./README.md)
- [Analytics and prediction](../06-analytics-and-prediction/README.md)
- [AI and agents](../05-ai-and-agents/README.md)
- [GTM learning engine](../../projects/gtm-learning-engine/README.md)
- [Proposed AI experiment](../../case-studies/experimentation/proposed-ai-experiment.md)
- [Data architecture](../03-data-architecture/README.md)
- [GTM engineering](../04-gtm-engineering/README.md)
- [Impact](../../IMPACT.md)
