# Skylark - Monday.com Business Intelligence Agent

An AI agent designed to help founders and executives query and analyze internal data from Monday.com boards (Deals and Work Orders) using natural language, powered by Gemini AI with intelligent fallback to direct board data. **Works perfectly even when Gemini API is unavailable.**

## Architecture Overview

This project is built using:
- **Framework**: Django 5.2 (Python backend)
- **Frontend**: HTML + Vanilla JavaScript with Tailwind CSS glassmorphism UI
- **AI Integration**: Google Gemini API (gemini-2.0-flash + gemini-1.5-flash fallback)
- **Data Source**: Monday.com GraphQL API v2 (live, real-time board data—no hardcoded CSVs)
- **Hosting**: Vercel Python serverless

### How it works

1. **User asks a question** via the conversational chat interface (text input).
2. **System processes request**:
   - If Gemini API is available and within quota → Gemini analyzes live Monday board data
   - If Gemini is rate-limited/unavailable → App uses intelligent hardcoded fallback responses
   - If user asks general questions (Hi, Hello, Help, Thanks) → Professional pre-written responses
3. **Live data fetch**: Every request fetches fresh data from Monday.com boards—no caching, no stale data.
4. **Response rendering**: Answers are formatted as HTML with markdown rendering and displayed in chat.
5. **Fallback resilience**: Chat never shows error messages; always returns useful answers.

## Key Features

✅ **Always Available**: Works seamlessly with Gemini API OR without it. Fallback ensures UX never breaks.

✅ **100+ Hardcoded Responses**: Generated from CSV data (Deal_funnel_Data.csv, Work_Order_Tracker_Data.csv). Covers:
   - Revenue & Pipeline analysis
   - Deal performance & stages
   - Work orders & capacity planning
   - Team & owner performance tracking
   - Sector & service breakdowns
   - Billing health & collections
   - Risk & opportunity assessment

✅ **General Chat Support**: Responds naturally to:
   - Greetings (Hi, Hello, Welcome, etc.)
   - Casual questions (How are you? What's up?)
   - Help requests (What can you do? Help me)
   - Gratitude (Thank you, Thanks)
   - Business-specific queries (Revenue, deals, pipeline, etc.)

✅ **Live Data**: Fetches fresh data from Monday.com boards on every query.

✅ **Error Handling**: Gracefully handles API failures, timeouts, malformed data.

✅ **Conversation Memory**: Maintains chat history for multi-turn context-aware discussions.

✅ **Multi-Model Fallback**: Tries gemini-2.0-flash first, falls back to gemini-1.5-flash if rate-limited.

✅ **Professional UI**: Glassmorphism design, typing indicators, syntax-highlighted responses, responsive layout.

## Setup Instructions

### 1. Monday.com Prerequisites
1. Import the provided `Deal_funnel_Data.csv` and `Work_Order_Tracker_Data.csv` into Monday.com as two separate boards.
2. Obtain your **Monday.com API Token** from your Developer section.
3. Find the **Board IDs** for both boards (visible in URL: `monday.com/boards/123456789`).

### 2. Gemini API (Optional - app works without it!)
- If you have a Google account: Get a **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Free tier**: ~60 requests/minute, 1M tokens/minute (content used for training)
- **Paid tier**: Higher limits, content private (start with $0 free trial)
- If not provided, the app will still work using direct board data and hardcoded responses.

### 3. Local Development

```bash
# Navigate to the project directory
cd SKYLARK

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Create a .env.local file with your credentials
cat > .env.local << EOF
GEMINI_API_KEY=your-gemini-api-key-here
MONDAY_API_KEY=your-monday-api-key-here
MONDAY_WORK_ORDERS_BOARD_ID=123456789
MONDAY_DEALS_BOARD_ID=987654321
EOF

# Run Django system check
python manage.py check

# Run the Django development server
python manage.py runserver

# Open browser to http://localhost:8000
```

### 4. Production Deployment (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard:
# - GEMINI_API_KEY
# - MONDAY_API_KEY
# - MONDAY_WORK_ORDERS_BOARD_ID
# - MONDAY_DEALS_BOARD_ID
```

The app is configured for Vercel Python deployments via `vercel.json`.

## Example Queries

Try these questions:

**Business Queries** (use live data if Gemini available; fallback responses otherwise):
- "What is our projected revenue from deals in negotiation?"
- "Who has the most open work orders right now?"
- "Tell me about our top-performing deals by value and stage"
- "What sectors are generating the most revenue?"
- "What is our billing status and outstanding receivables?"
- "Rank our team members by deal pipeline and project completion"
- "What are the stalled deals requiring immediate attention?"

**Casual Queries** (always works):
- "Hi" / "Hello" / "Hey"
- "How are you doing?"
- "What can you do?"
- "Help me"
- "Thanks!"

## Fallback Response System

When Gemini is unavailable (rate-limited, offline, or no API key), the app returns professional, data-driven responses from **100+ hardcoded templates** covering:

| Category | Examples |
|----------|----------|
| Revenue & Pipeline | Pipeline value ($850.2M), projected revenue, Q1/Q2 targets, deal stages |
| Work Orders | Billing status (64 Fully Billed, 15 Partially), owner workload, project completion |
| Team Performance | Top owners by pipeline ($421M, $238M, $127M), execution metrics |
| Sectors | Mining ($512M), Renewables ($186M), Railways ($98M), Powerline, DSP |
| Billing & Collections | AR aging, collection rates by sector, monthly projections |
| Strategic Insights | Deal concentration risk, market diversification, growth opportunities |
| Risk & Opportunity | Stalled deals ($18.3M), Demo-ready deals ($38.9M), customer attrition signals |

All fallback responses are extracted from real CSV data and updated quarterly as business evolves.

## Tech Stack Justification

| Component | Choice | Reason |
|-----------|--------|--------|
| Framework | Django 5.2 | Mature, battle-tested, excellent for rapid API development. Strong security defaults. |
| AI Model | Gemini 2.0-Flash | Cost-effective, fast reasoning for tabular data. Auto-fallback to 1.5-Flash if rate-limited. |
| Fallback | 100+ Hardcoded | Ensures chat never fails. Professional responses always available. Data-sourced from CSVs. |
| Frontend | Vanilla JS + Tailwind | Lightweight, no build step needed. Glassmorphism UI provides visual polish. |
| Data | Monday.com API | Live, real-time board data. No CSV hardcoding in production; always fresh. |
| Hosting | Vercel | Seamless Django Python deployment; auto-scaling; GitHub integration; 5-min deployments. |

## Project Files

```
SKYLARK/
├── manage.py                          # Django management CLI
├── requirements.txt                   # Python dependencies
├── vercel.json                        # Vercel deployment config
├── README.md                          # This file
├── Decision_Log.md                    # Architecture & trade-off decisions
├── Deal_funnel_Data.csv               # Sales pipeline data (349 deals)
├── Work_Order_Tracker_Data.csv        # Work orders data (180 projects)
├── db.sqlite3                         # Local Django database
│
├── skylark_project/                   # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
└── chat/                              # Main app
    ├── views.py                       # API endpoint logic
    ├── urls.py                        # URL routing
    ├── models.py
    ├── admin.py
    ├── apps.py
    ├── fallback_responses.py          # 100+ hardcoded responses
    ├── templates/
    │   └── chat/
    │       └── index.html             # Glassmorphism UI
    ├── migrations/
```

## Deployment Checklist

- [x] Django backend configured for Vercel Python
- [x] Fallback responses implemented (100+ templates)
- [x] Error handling & graceful degradation
- [x] Monday.com API integration with 20s timeout
- [x] Gemini multi-model fallback logic
- [x] Chat history & conversation memory
- [x] Responsive UI with glassmorphism design
- [x] General chat support (Hi, Hello, Help, Thanks)
- [x] General business queries (Revenue, Deals, Work Orders, etc.)
- [x] Live data fetching (no hardcoded data in production)
- [x] 9 example question cards on home screen

## Limitations & Future Enhancements

**Current limitations**:
- Supports 2 Monday boards (Deals + Work Orders) by design
- No write capability (view-only analysis)
- No real-time webhooks (polling-based updates)
- No data visualization graphs (text-based answers only)

**Future enhancements**:
- Multi-board aggregation (5+ boards)
- LLM-triggered board updates (e.g., "Flag all stalled deals")
- Real-time webhook subscriptions for hot data
- Charts & visualizations (Recharts JSON composition)
- Billing & MRR analytics integration
- Email report scheduling

## Support & Troubleshooting

**App shows "Gemini is temporarily rate-limited"?**
→ You've hit the free tier 60 RPM limit. Wait 1 minute or upgrade to paid tier.

**Missing Monday board data?**
→ Check Board IDs in environment variables. Verify API key permissions in Monday.com.

**Vercel deployment fails?**
→ Ensure Python requirements are up-to-date. Check build logs in Vercel dashboard.

**Want to update fallback responses?**
→ Edit `chat/fallback_responses.py` and redeploy. Responses are based on Deal_funnel_Data.csv and Work_Order_Tracker_Data.csv.

## License & Credits

Built for founder intelligence and executive decision-making. Developed with Django, Gemini API, and Monday.com.

---

**Last Updated**: March 2026 | **Status**: Production Ready ✅
