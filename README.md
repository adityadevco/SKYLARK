# Skylark - Monday.com Business Intelligence Agent

An AI agent designed to help founders and executives query and analyze internal data from Monday.com boards (Deals and Work Orders) using natural language, powered by Gemini AI with intelligent fallback to direct board data.

## Architecture Overview

This project is built using:
- **Framework**: Django 5.2 (Python backend)
- **Frontend**: HTML + Vanilla JavaScript with Tailwind CSS glassmorphism UI
- **AI Integration**: Google Gemini API with automatic fallback to Monday.com board data
- **Data Source**: Monday.com GraphQL API v2 (live, real-time board data—no hardcoded CSVs)

### How it works
1. User asks a natural language question via the conversational chat interface.
2. The backend fetches live data from your Monday.com boards (Deals and Work Orders).
3. If Gemini AI is available and within quota, it analyzes the data and synthesizes an intelligent response.
4. If Gemini is unavailable or rate-limited, the app intelligently falls back to direct board analysis:
   - Parses numeric fields (revenue, count, etc.)
   - Filters by query keywords (deals, pipeline, work orders, etc.)
   - Returns structured summaries from the raw board data.
5. The response is rendered as styled HTML in the chat interface.

## Key Features

- **Resilient Design**: Works even when Gemini API is unavailable; falls back to direct Monday.com board analysis.
- **Live Data**: Pulls fresh data from Monday.com boards on every query—no stale CSVs or caching.
- **Error Handling**: Gracefully handles missing data, malformed fields, and API failures.
- **Conversation Memory**: Maintains chat history for context-aware multi-turn conversations.
- **Gemini Tool Use**: Automatically calls Monday board tools to fetch data as needed for reasoning.

## Setup Instructions

### 1. Monday.com Prerequisites
1. Import the provided `Deal_funnel_Data.csv` and `Work_Order_Tracker_Data.csv` into Monday.com as two separate boards.
2. Obtain your **Monday.com API Token** from your Developer section.
3. Find the **Board IDs** for both boards (usually found in the URL when viewing the board: `monday.com/boards/123456789`).

### 2. Gemini API (Optional but recommended)
- Get a **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey)
- If not provided, the app will still work using direct board data.

### 3. Local Development

```bash
# Navigate to the project directory
cd skylark

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

# Run the Django development server
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### 4. Production Deployment (Vercel)
The app is configured for Vercel Python deployments via `vercel.json`. Set the same environment variables in your Vercel project settings.

## Example Queries

Try asking:
- "What is our projected revenue from deals in negotiation?"
- "Who has the most open work orders right now?"
- "Prepare a leadership update highlighting stalled deals."
- "How many deals are in the pipeline for Q1?"

## Tech Stack Justification

| Component | Choice | Reason |
|-----------|--------|--------|
| Framework | Django | Mature, battle-tested, excellent for rapid API development. Strong security defaults. |
| AI Model | Gemini 2.0-Flash | Cost-effective, fast reasoning for tabular data analysis. Auto-fallback to 1.5-Flash if rate-limited. |
| Frontend | Vanilla JS + Tailwind | Lightweight, no build step needed. Glassmorphism UI provides visual polish. |
| Data | Monday.com API | Live, real-time board data. No CSV hardcoding; always fresh insights. |
| Hosting | Vercel | Seamless Django Python deployment; automatic scaling; GitHub integration. |
