# Skylark - Monday.com Business Intelligence Agent

An AI agent designed to help founders query and analyze internal data from Monday.com boards (Deals and Work Orders) using natural language.

## Architecture Overview

This project is built using:
- **Framework**: Next.js 15 (App Router)
- **Styling**: Tailwind CSS @ 4.0 (for stunning glassmorphism UIs)
- **AI Integration**: Vercel AI SDK with OpenAI API (`gpt-4o-mini`)
- **Data Source**: Monday.com GraphQL API v2

### How it works
1. The user provides API keys via a local, secure UI modal (`localStorage`).
2. When the app loads, it makes a concurrent fetch to the Monday.com GraphQL API (via `/api/monday`) for both the Work Orders and Deals boards.
3. The server cleans and normalizes this messy data (handling missing dates, stripping text from numbers, mapping status columns).
4. The user types a natural language query.
5. The unified data context + the user query are sent to the `/api/chat` route, which streams a synthesized business intelligence response back to the client.

## Setup Instructions

### 1. Monday.com Prerequisites
1. Import the provided `Deal_funnel_Data.csv` and `Work_Order_Tracker_Data.csv` into Monday.com as two separate boards.
2. Obtain your **Monday.com API Token** from your Developer section.
3. Find the **Board IDs** for both boards (usually found in the URL when viewing the board: `monday.com/boards/123456789`).

### 2. General Prerequisites
You will need an **OpenAI API Key** to power the intelligence engine.

### 3. Local Development

```bash
# Unzip the source code and cd into the project
cd skylark

# Install dependencies
npm install

# Run the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

Click the **Settings (Gear Icon)** in the top right to configure your:
- Monday.com API Key
- OpenAI API Key
- Deal Board ID
- Work Order Board ID

Once connected, you can ask queries like:
- "How's our pipeline looking for the energy sector?"
- "Prepare a leadership update highlighting stalled deals."
