# Decision Log: Skylark Drones - Business Intelligence Agent

## Key Assumptions
1. **Board Structure & IDs**: I assumed the user would import the provided CSVs into Monday.com and that the generated Board IDs would need to be securely provided to the agent.
2. **Data Scale**: Given the founder-level query requirement, I assumed the data fits within the context window of modern LLMs (like GPT-4o-mini) when fetched via the Monday.com GraphQL API.
3. **Bring Your Own Key (BYOK)**: Since the prototype needs to be hosted and accessible without a local Monday.com workspace setup on the evaluator's end, the architecture requires the user to input their API keys locally into the browser memory rather than hardcoding them into the server. This ensures data privacy and portability.

## Trade-offs Chosen & Why
1. **Context-Injection vs. Vector Database (RAG)**
   - *Choice*: I opted to fetch data directly via GraphQL, clean it into a minimized format, and pass it directly into the LLM context prompt (`dataContext`).
   - *Why*: The dataset size for typical work orders / active deals fits well within a 128k token context window. Relying on an external vector DB (like Pinecone) over-complicates the prototype, introduces indexing latency, and creates sync issues if the Monday boards update in real-time. Direct context injection ensures 100% accurate, up-to-the-second data resolution.

2. **GPT-4o-mini over GPT-4o**
   - *Choice*: Selected `gpt-4o-mini` via Vercel AI SDK.
   - *Why*: Analyzing tabular data requires fast reasoning, but founder queries are often well-defined standard analysis. `4o-mini` is extremely fast and cost-effective while still providing rigorous synthesis.

3. **Client-side Storage for Keys**
   - *Choice*: API keys and Board IDs are stored in `localStorage` rather than a server DB.
   - *Why*: Security and simplicity. The Next.js API routes act purely as proxies. No sensitive credentials are ever logged or persisted remotely.

## What I'd do differently with more time
1. **Dynamic GraphQL Schema Introspection**: Currently, the agent fetches a standard set of columns. Given more time, I would build a multi-step chain where the LLM first introspects the Monday.com board schema to understand the fields available, then dynamically constructs the GraphQL query to fetch *only* the required data for that specific user prompt, saving bandwidth and context tokens.
2. **Data Visualisation**: I would implement dynamic chart generation (using Recharts or similar). The LLM could respond with a JSON configuration for a chart alongside its analytical text, providing founders with a graphical breakdown of pipeline health.
3. **Agentic Actions (Write capabilities)**: The current integration is read-only. I would add write integrations so the LLM could execute tasks like: "Flag all stalled deals as 'At Risk' in Monday.com."

## Handling "Leadership Updates"
To fulfill the optional requirement *"The agent should help prepare data for leadership updates"*, the System Prompt explicitly instructs the LLM to format responses with structured summaries, bullet points, and synthesized highlights. By simply prompting the agent with "Prepare a leadership update for the energy sector deals," the AI utilizes the entire available context to generate a ready-to-copy Markdown briefing outlining revenue, bottlenecks, and overall performance.
