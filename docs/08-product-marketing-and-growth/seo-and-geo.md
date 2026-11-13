# SEO and generative engine optimization

SEO (search engine optimization) is the work of getting your pages found in Google and Bing. GEO (generative engine optimization) is the same idea for AI assistants like ChatGPT and Perplexity: getting your company mentioned and cited in their answers. Both decide whether a buyer researching a problem finds your company, understands it, and sees it recommended. This page explains how classic SEO works under the hood, how AI assistants find and cite sources, and how to measure both honestly, given that much of the value never shows up in normal attribution reports.

## Technical SEO

Technical SEO makes sure search engines can fetch your pages, understand them and add them to their index (the stored copy of the web they search). It does not make content rank by itself, but problems here limit everything else.

**Crawlability.** Can the search engine's crawler (the bot that visits pages) reach the page?

- `robots.txt` is a file that tells well-behaved crawlers what they may fetch. Blocking a path there stops crawling, not indexing. A blocked page that other sites link to can still show up in results, just without a description.
- Links between your own pages are the main way crawlers find pages. A page with no links pointing to it (an "orphan") gets found late or never.
- Google can index content that is built in the browser by JavaScript, but it does so later, and many other crawlers (including many AI crawlers) do not run JavaScript at all. Make sure important content is in the page when the server sends it.

**Indexability.** Will the search engine store the page?

- A "noindex" tag in the page (`<meta name="robots" content="noindex">`) or an `X-Robots-Tag` header keeps a page out of the index. The crawler has to be able to fetch the page to see that tag, so do not also block the page in robots.txt.
- Thin pages, duplicates and near-duplicates may be crawled but not stored. The page indexing report in Google Search Console (Google's free site report) shows why.

**Canonical tags.** A canonical tag (`<link rel="canonical" href="...">`) tells search engines which address is the main version when the same content appears at several addresses. This happens with tracking parameters, trailing slashes, HTTP vs HTTPS, and filtered listings. It is a hint, not an order. Common mistakes: pointing the canonical at a page that redirects or is set to noindex, pointing every page at the homepage, and canonicals that disagree with the sitemap.

**Sitemaps.** An XML sitemap is a file listing the pages you want indexed, with an optional `lastmod` date for each. List only the main version of pages you want indexed. Keep `lastmod` honest: change it only when the content really changes. Submit the sitemap in Google Search Console and Bing Webmaster Tools.

**Core Web Vitals.** Google's page experience scores, measured from real visitors:

| Metric | Measures | "Good" threshold (per Google's published guidance) |
|---|---|---|
| LCP, Largest Contentful Paint | Loading: when the main content renders | 2.5 seconds or less |
| INP, Interaction to Next Paint | Responsiveness to user input (replaced FID in 2024) | 200 milliseconds or less |
| CLS, Cumulative Layout Shift | Visual stability | 0.1 or less |

In plain terms: how fast the main content appears, how fast the page reacts to a click, and how much the layout jumps around while loading. Google judges these at the 75th percentile of page loads, meaning 3 out of 4 visits must meet the target. Check the thresholds against Google's current documentation before setting goals. Real-visitor data (from Google's Chrome UX Report, called CrUX, or your own monitoring) is what counts. Test tools such as Lighthouse help find the causes. Typical fixes on B2B sites: shrink and properly size large header images, delay third-party scripts (chat widgets, tag managers and intent-tracking pixels often cause most of the slow response to clicks), and reserve space for embeds and cookie banners so the page does not jump.

**Common technical failures on B2B sites.**

| Failure | Symptom | Check | Fix |
|---|---|---|---|
| Staging or preview site indexed | Duplicate pages in results on a non-production domain | `site:` search, Search Console | Auth-protect previews; noindex header on non-production |
| Marketing site rebuild without redirects | Traffic drop after launch, 404s in Search Console | Crawl old URL list against new site | 301 map from every old URL with traffic or links |
| Client-side rendered content | Page indexed with little text | Fetch raw HTML with curl; URL inspection | Server-side or static rendering |
| Parameter duplicates | Many URLs per page (UTM, filters) | Crawl report, canonical audit | Self-referencing canonicals; consistent internal links |
| Gated content only | Thin indexable pages | Content audit | Ungated summary page with the gated asset as an option |
| Heavy third-party scripts | Poor INP in field data | Performance trace of main thread | Defer, load on interaction, remove unused tags |

A 301 is a permanent redirect from an old address to a new one. A 404 is a "page not found" error.

A quick check, run from the command line, of what a crawler sees on one page:

```bash
curl -sI https://www.example.com/pricing | grep -i -E "^(HTTP|x-robots-tag|location)"
curl -s https://www.example.com/pricing | grep -i -E "rel=\"canonical\"|name=\"robots\""
curl -s https://www.example.com/robots.txt
```

## Search intent

Every search has an intent, meaning what the person actually wants. A page ranks when it matches that intent.

| Intent | Example B2B query | Page type that matches |
|---|---|---|
| Informational | "how to calculate pipeline coverage" | Explainer or guide |
| Commercial investigation | "best revenue analytics tools", "X vs Y" | Comparison, alternatives page |
| Transactional | "X pricing", "X demo" | Pricing, demo request |
| Navigational | "X login" | The relevant app or brand page |

To check intent, look at what ranks today. If the top results are all list articles, a product page will not rank for that search no matter how well it is tuned. Assign each target search to one page, so several of your own pages do not compete for the same intent.

## Structured data

Structured data (often called schema markup) is a hidden block of code that describes the page in a format machines can read. The most common form uses the schema.org vocabulary, written as JSON-LD:

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

Useful types for B2B sites: `Organization` (who the company is, with `sameAs` links to its official profiles), `SoftwareApplication` (product name, category, operating system, pricing), `Article` (author, dates), `BreadcrumbList` and `FAQPage`.

What to expect: Google limits which sites get special FAQ displays in results (in 2023 it restricted them mostly to well-known, authoritative government and health sites), and whether any page gets a special display is up to the search engine. Treat schema as background information about who you are and what you offer, not as a guaranteed visual feature. The markup must match what is visible on the page. Marking up content that is not on the page breaks Google's guidelines. Check your markup with Google's Rich Results Test and the Schema Markup Validator.

## Content architecture

**Topic clusters.** A pillar page covers a broad topic (for example, "pipeline forecasting") and links to cluster pages that go deep on subtopics (weighted pipeline, stage probabilities, forecast accuracy). Cluster pages link back to the pillar and to each other where it makes sense. This gives crawlers a clear structure and gives readers a path.

**Internal links.** These are links from one of your pages to another.

- Use link text that names the topic of the destination, not "click here."
- Link from your most-visited pages to the pages you want to rank.
- Keep important pages within a few clicks of the homepage.
- Check for orphan pages and broken links on a schedule.

**URL structure.** Use short, stable, readable page addresses that reflect the site structure (`/guides/forecasting/weighted-pipeline`). Changing addresses requires 301 redirects and loses some ranking strength along the way, so pick a structure and keep it.

**Programmatic pages.** Pages built from a template and a data table (integrations, locations, comparisons) can cover many searches quickly. But thin template pages with little unique content tend to get crawled and then left out of the index. Each page needs content a person would find useful on its own.

## Organic acquisition

Organic means unpaid search traffic. For B2B, organic search usually helps in two ways. First, direct conversions: demo requests from comparison and pricing pages. Second, research help: buyers read guides and come back later by typing the site name or searching the brand. In many B2B funnels the second is bigger, and last-touch attribution mostly misses it.

Content that tends to produce pipeline: comparison and alternatives pages for real competitors, integration pages, pricing explanations, and practical guides on problems the product solves. Content that tends to bring traffic without pipeline: broad, early-stage topics far from the product.

Measure organic by pipeline sourced from organic landing pages, by how often people search your brand name over time, and by what buyers say when asked how they heard of you, not by visits alone.

## Generative engine optimization

Generative engine optimization (GEO) is the work of making content likely to be found, understood and cited by AI assistants that search the web: ChatGPT search, Perplexity, Google AI Overviews and AI Mode, Microsoft Copilot, and Claude with web search.

**How AI answer engines retrieve and cite.** The details differ by product and are not fully public, but the general pattern is:

1. The assistant turns the user's question into one or more search queries.
2. It pulls results from a search index (its own, or a partner's).
3. It opens selected pages and reads passages from them.
4. It writes an answer from those passages and may cite some of them.

Separately, the material a model was trained on shapes what it "knows" about a brand without searching at all. Both paths matter. Search affects current answers that come with citations. Training data affects answers given without searching, and how the model reads what it finds.

What this means: classic search visibility still matters, because many assistants search the same indexes. Pages that do not rank, or are not indexed, are less likely to be found.

**Being citable.**

- **Say clearly what you are.** State plainly what the company is, what the product does, who it is for and what category it belongs to, in one sentence that still makes sense when quoted on its own.
- **Factual, specific pages.** Definitions, formulas, comparisons and concrete criteria are easier to quote than vague marketing copy.
- **Sections that stand alone.** Each section should make sense if pulled out without the rest of the page. Use headings that match how people phrase their questions.
- **Same name everywhere.** Use the same company name, product name and description on your website, LinkedIn, GitHub, directories and review sites. Inconsistent naming makes it harder for any system to tell that all those pages are about the same company.
- **Mentions on other sites.** Assistants often cite sources other than the vendor: review sites, community discussions, industry publications, comparison articles. Being described accurately on credible outside pages matters, though you cannot fully control it.
- **Freshness.** Show visible dates and keep information current, especially pricing, features and comparisons.

**AI crawler access.** AI companies publish the names their crawlers use (called user agents). Examples: `GPTBot` and `OAI-SearchBot` (OpenAI), `ClaudeBot` (Anthropic), and `PerplexityBot` (Perplexity). Google uses a separate `Google-Extended` setting in robots.txt to control whether your content is used for some AI training, apart from normal Google search crawling. These names and their purposes change, so check each company's current documentation.

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

Make this choice on purpose. Blocking crawlers that collect training data and blocking crawlers that fetch pages for live answers have different effects, and some companies use separate crawlers for each. Check your server logs to see which crawlers actually visit, because following robots.txt is voluntary.

**llms.txt.** A proposed idea: a plain text file at `/llms.txt` that summarizes the site and links to its most useful pages for AI models. It is a proposal, not a standard. Whether the major AI companies use it at all is unclear and mostly undocumented. It is cheap to publish, but do not expect it to make a measurable difference on its own.

## AI answer visibility tracking

There is no AI version of Google Search Console that reports how often you appear across assistants. The practical method is a fixed set of questions run on a schedule (a "prompt panel").

**Method.**

1. Write 30 to 100 questions buyers would plausibly ask, grouped by type: category ("what tools help with revenue forecasting"), problem ("how do I fix pipeline forecast misses"), comparison ("X vs Y") and brand ("what is X").
2. Ask each question in each assistant on a fixed schedule (weekly or monthly), with the same settings each time, logged out or in a clean browser profile where possible, and note the location.
3. Ask each question several times per round, because answers change from one run to the next.
4. Save the full answer, the cited links and the time.
5. Pull out the results with code or a tested classifier (an AI or rules that label each answer): was the brand mentioned (yes/no), was your own site cited, how early the brand first appears, the tone, and which competitors appear.

```text
prompt_runs(run_id, prompt_id, assistant, model_label, run_at, answer_text, cited_urls[])
mentions(run_id, entity, mentioned, cited, first_position, sentiment)
```

**Caveats.** Results vary by run, user history, location and model version. A small question set gives jumpy numbers. Report how many runs sit behind each number, and look at trends over several rounds instead of week-to-week swings. The question set reflects your guesses about what buyers ask, so refresh it from sales call transcripts and real search data.

## Attribution limitations

- **Zero-click answers.** Search features and AI answers settle many questions without anyone visiting your site. You influenced the buyer, but there is no visit to credit.
- **Lost source information.** Some visits from AI assistants arrive labeled with where they came from. Others arrive looking like someone typed your address directly (copied links, in-app browsers, stripped labels). So analytics undercounts visits from AI.
- **Delayed and offline influence.** A buyer reads an AI answer naming three vendors, then searches your brand a week later. Last-touch attribution gives the credit to branded search.
- **Self-reported attribution.** A required question on demo forms ("How did you hear about us?"), as a free-text box or dropdown, catches channels analytics misses, including AI assistants, podcasts and peer referrals. Sort free-text answers into categories. People do not always remember correctly, but it is often the only signal for these hidden channels. Compare what each lead says against the tracked source.

## Experiment design for SEO and GEO

Search and AI visibility are hard to test, because you do not control how results are ranked and the numbers are noisy.

- **Page-level split tests.** Take a group of similar template pages (integration pages, comparison pages). Randomly change half of them (title format, added schema, rewritten intro) and leave the other half alone as a comparison group. Compare search clicks over the same period. This needs many similar pages. It does not work for a handful of unique pages.
- **Before/after with a comparison group.** When random assignment is not possible, compare how much the changed pages moved against how much a similar group of unchanged pages moved over the same time (known as difference-in-differences). This removes site-wide and seasonal swings that a simple before/after comparison would wrongly count as your effect.
- **Timing caveats.** Google algorithm updates, seasons, competitor changes and indexing delays all move the numbers regardless of your change. Use windows long enough for pages to be re-crawled (often several weeks), avoid running tests across known major updates, and treat before/after charts for a single page as anecdotes.
- **GEO tests.** Run the prompt panel before and after content changes on a set of pages, with an untouched set of pages as the comparison. Expect a lot of noise. Look for a consistent direction over several rounds.

## Implementation sequence

Do the work in order of what blocks everything after it:

1. **Access and indexing.** Fix robots rules, noindex mistakes, canonicals, redirects and sitemaps. Make your AI crawler policy a deliberate choice. Nothing else matters for pages that cannot be fetched.
2. **Clear company identity.** Write one official description of the company and product, and use it on the homepage, in the `Organization` schema, and on every official profile listed in `sameAs`.
3. **Pages for buyers close to a decision.** Pricing explanation, comparison and alternatives pages, integration pages. These are closest to pipeline.
4. **Topic clusters.** Practical guides on the problems the product solves, linked together, with definitions and formulas that can be quoted.
5. **Presence on other sites.** Accurate directory and review-site profiles, plus contributions to credible industry publications and communities.
6. **Measurement.** Clean Search Console and analytics setup, the "how did you hear about us" field, and the prompt panel, all running before content changes so you have a starting point to compare against.

Steps 1, 2 and 6 are mostly one-time technical work. Steps 3 to 5 are ongoing content work with an owner and a publishing schedule.

## What can go wrong

- **Writing for the question set instead of the buyer.** Rewriting pages to win your own fixed set of questions can tune you to questions you picked yourself. Keep adding new questions taken from real buyer language.
- **Treating mentions as pipeline.** A rising mention rate is an early sign. Connect it to branded search, "how did you hear about us" answers and sourced pipeline before claiming business impact.
- **Errors in the tracking itself.** Brand-mention detection misses misspellings and confuses companies with similar names. Test the detector on a set of answers you have checked by hand, the same way as any [AI evaluation](../../projects/ai-evaluation/README.md).
- **Blocking crawlers by accident.** A broad `Disallow` rule added during a site migration, a firewall rule that blocks unfamiliar visitors, or bot protection that shows crawlers a challenge page. Check server logs, not just robots.txt.
- **Wrong descriptions on other sites.** Old directory listings and outdated review-site descriptions get picked up and repeated by AI. Audit and fix the profiles you control.

## What would change the approach

- Sites with few pages are better served by quality improvements and before/after comparisons with a control group than by split tests.
- If AI assistants start sharing referral or impression data with site owners, measurement will shift from prompt panels to their direct reports.
- Regulated or sensitive content may justify blocking some AI crawlers, even at a cost to visibility.

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
