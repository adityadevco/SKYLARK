# Decision Log: Skylark - Business Intelligence Agent

## Key Assumptions
1. **Board Structure & IDs**: I assumed the user would import the provided CSVs into Monday.com and that the generated Board IDs would need to be securely provided to the agent via environment variables.
2. **Data Scale**: Given the founder-level query requirement, I assumed the data fits within the context window of modern LLMs (Gemini 2.0-Flash) when fetched via the Monday.com GraphQL API.
3. **Always-Available Fallback**: Rather than failing when Gemini is unavailable, the app provides useful answers directly from Monday board data, keeping the UX consistent.
4. **No CSV Hardcoding**: All data is fetched live from Monday.com boards on every request, ensuring fresh insights and no stale data.

## Architecture: Django + Gemini + Monday.com

**Why Django over Next.js?**
- Simpler backend for production BI workloads; built-in security and ORM
- Faster iteration on data-fetching logic and error handling
- Vercel Python support is production-ready; no JavaScript complexity needed

**Why Gemini 2.0-Flash?**
- Cost-effective and fast at reasoning over tabular data
- Automatic tool-calling supports Monday board functions natively
- Fallback to 1.5-Flash if rate-limited (multi-model resilience)

## Trade-offs Chosen & Why

### 1. **Gemini with Intelligent Fallback vs. Pure Vector DB (RAG)**
- *Choice*: Gemini + Monday API direct fetch + fallback template system
- *Why*: 
  - Dataset fits in context window (typical ~100-500 records)
  - No indexing latency or sync issues
  - Fallback ensures UX never breaks even if Gemini quota exhausted
  - Users get immediate answers even in degraded mode

### 2. **Monday.com GraphQL vs. Hardcoded CSV Import**
- *Choice*: Fetch live from Monday.com API every request
- *Why*:
  - Real-time data reflects board changes instantly
  - No sync problems or stale data issues
  - Founder insights are always current
  - API quota is reasonable for typical usage (100-200 requests/month)

### 3. **Client Config vs. Server-Side Secrets**
- *Choice*: Environment variables in Vercel; no localStorage key storage
- *Why*:
  - Production grade: credentials never logged or exposed
  - Vercel secrets are encrypted at rest
  - API keys never leave the server

### 4. **Direct Board Analysis Fallback**
- *Choice*: Hardcoded query templates + numeric parsing
- *Why*:
  - Ensures chat never shows "server error" bubble
  - Provides useful data even without Gemini (e.g., "Projected revenue from deals in negotiation: $2.5M across 8 deals")
  - Users stay engaged; no frustration from API failures

## What I'd do differently with more time

1. **Dynamic GraphQL Introspection**: Build a multi-step chain where Gemini first introspects the Monday board schema, then constructs queries dynamically for that specific user prompt (saves bandwidth and tokens).

2. **Real-time Subscriptions**: Use Monday.com webhooks to stream board updates and cache hot data (e.g., top-3 stalled deals), reducing latency on common queries.

3. **Multi-board Aggregation**: Add support for querying across 5+ boards (e.g., "Is revenue tracking to plan across all channels?"). Current implementation supports 2 boards by design.

4. **Data Visualization**: LLM composes Recharts JSON configs alongside text answers so founders see visual breakdowns (charts, tables) of pipeline health.

5. **Write Capabilities**: Add LLM-triggered actions like "Flag all stalled deals as At Risk" or "Assign overdue work orders to available team members."

6. **Billing Alerts**: Integrate Stripe billing data and let Gemini answer "What's our MRR growth?" or "Are we hitting quota targets?"

## How I Interpreted "Prepare Leadership Updates"

The optional feature *"The agent should help prepare data for leadership updates"* is implemented as follows:

**System Prompt Guidance**: The Gemini system instruction explicitly tells it to format responses for executive consumption:
- Structured bullet points
- Key numbers highlighted with currency/percentages
- Caveats and data gaps flagged
- Actionable insights prioritized over raw metrics

**Example**:
```
User: "Prepare a leadership update on Q1 pipeline health."

Gemini Response:
**Q1 Pipeline Summary**
- **Total pipeline value**: $12.5M across 24 active deals
- **Negotiation stage** (highest risk): $4.2M / 7 deals — *escalate 2 stalled >30 days*
- **Proposal stage** (ready to win): $3.8M / 9 deals
- **Exploration**: $4.5M / 8 deals

**Recommended Actions**: 
1. Schedule executive sponsor calls for 2 stalled deals  
2. Launch counter-proposal for top 3 deals in Proposal stage
3. Prioritize discovery for Energy sector (3 deals, $1.8M potential)

**Data Quality Note**: 2 deals missing revenue estimates; recommend validation.
```

This ensures leadership gets *insights*, not just data dumps.

## Deployment & Resilience

- **Vercel Python**: Serverless Django functions auto-scale during traffic spikes
- **Fallback Mode**: If Gemini rate-limited, app seamlessly switches to direct board analysis
- **Error Transparency**: Users see "AI model unavailable, using direct board mode" (no raw 500 errors)
- **Monitoring**: 5xx errors caught and logged; fallback responses tracked separately

## Conclusion

This implementation prioritizes **reliability and user experience** over feature completeness. A founder asking "How's our pipeline?" should always get an answer—whether Gemini is available or not.

