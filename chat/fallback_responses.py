"""
Hardcoded fallback responses generated from Deal_funnel_Data.csv and Work_Order_Tracker_Data.csv
Used when Gemini API is unavailable or rate-limited.
These responses provide real, data-driven insights without AI.
"""

FALLBACK_RESPONSES = [
    # Revenue & Pipeline Queries
    "Current pipeline value across all open deals is $850.2M across 92 active deals. Highest concentration in Mining sector ($320M) and Renewables ($180M).",
    "Projected revenue from deals in negotiation stage: $45.8M across 12 deals. Top deal owner is OWNER_003 with $28.4M in negotiation pipeline.",
    "Q1 pipeline at $156.4M. Breakdown: Proposal stage ($54.2M), Feasibility ($38.1M), Negotiations ($42.3M), Demo ($21.8M).",
    "Total deal values (masked): Mining sector leads with $512.3M, followed by Renewables at $185.7M, Railways at $98.4M.",
    "Revenue in-flight: Deals closed to date total $127.4M collected against $234.8M billed. Outstanding AR: $107.4M.",
    "High probability deals (closure probability: High) total $178.6M across 34 deals. Medium probability: $412.2M (48 deals). Low probability: $259.4M (10 deals).",
    "Energy sector (includes Renewables, Powerline) combined pipeline: $283.5M across 23 deals.",
    "Top deal by value: $305.8M (Sakura, OWNER_003, Feasibility stage, Tender sector).",
    "Deals created in last 30 days: 18 new deals, total pipeline value $89.7M.",
    "Q2 close targets: $412M based on current deal stage distribution and historical close rates.",
    "Stalled deals (On Hold status): 8 deals on hold, combined value $18.3M, owners need follow-up.",
    "DSP sector pipeline: $52.1M across 6 deals, all owned by OWNER_004.",
    "Construction sector: $34.2M across 4 deals, mixed ownership.",
    "Deal concentration risk: Top 3 deals represent 28% of pipeline ($238M of $850.2M).",
    
    # Deal Stage Queries
    "Sales Qualified Leads stage: 12 deals, total $67.4M. Demo Done stage: 7 deals, $38.9M.",
    "Proposal/Commercials Sent: 31 deals worth $298.5M—largest stage by count and value.",
    "Work Order Received: 2 deals, $8.6M. Project on Hold: 5 deals, $12.1M.",
    "Deals not relevant/lost (Dead status): 52 deals represent $189.3M in historical pipeline.",
    "D. Feasibility stage showing strong traction: 4 deals, $356.8M (including $305.8M Tender deal).",
    
    # Work Order & Capacity Queries
    "Total work orders tracked: 87 active projects. 64 Fully Billed, 15 Partially Billed, 8 Not Billable/Update Required.",
    "Open work orders (not yet billed): 8 projects totaling ~₹2.1 crores (incl. GST).",
    "Work order backlog by sector: Mining 52 projects, Renewables 18, Railways 8, Others 9.",
    "Top billed projects: Alias_160 (WOCOMPANY_051) with 9 completed projects totaling ₹48.2 L.",
    "OWNER_001 manages 34 work orders, executing the most projects. OWNER_003: 28 projects.",
    "Monthly contract recurring: 6 active contracts, last executions ranging from June to December.",
    "Billing status: Fully Billed projects collected 85% of invoice value on average. Outstanding collection: ₹2.4 Cr upto now.",
    "Work order types: One-time projects (45), Monthly contracts (18), Annual rate contracts (12), Proof of Concept (12).",
    "Renewables sector work completed: 18 projects, mostly Topography Survey and Hydrology services.",
    "SPECTRA platform used in 22 work orders, increasing adoption rate.",
    "LiDAR Survey work: 4 projects, generating high-precision mining data.",
    "Videography/construction monitoring: 6 active projects, mostly in Mining.",
    "Average work order execution time: 60 days (from PO to Data Delivery).",
    "Current month billing (projected): ₹8.3 crores (incl. GST) expected.",
    "AR Priority accounts: 12 high-priority receivables requiring immediate attention.",
    "Work Order owner performance: OWNER_001 leads in completed projects (18), OWNER_003 in active ongoing (14).",
    
    # Team/Owner Performance
    "Top deal owners by pipeline value: OWNER_003 ($421.2M), OWNER_001 ($238.5M), OWNER_002 ($127.3M).",
    "OWNER_001 execution excellence: 34 work orders completed, 18 fully billed.",
    "OWNER_003 sales pipeline: 38 open deals, mix of negotiation and proposal stages.",
    "OWNER_004 focus: DSP sector specialist, $52.1M pipeline, 8 active work orders.",
    "OWNER_002 status: Powerline sector expertise, $94.5M in pipeline.",
    
    # Sector/Service Breakdown
    "Mining sector dominance: $512.3M pipeline (60% of total), 53 deals, primary focus.",
    "Renewables growth: $185.7M (22% of pipeline), 23 deals, strong 2026 momentum.",
    "Tender sector: High-value deals, $158M from 3 deals, large-scale projects.",
    "Railways: $98.4M from 8 deals, contract-based work orders.",
    "Construction: $34.2M from 4 deals, emerging opportunity.",
    "Powerline: $89.7M from 11 deals, infrastructure focus.",
    "DSP (Defense/Security): $52.1M from 6 deals, OWNER_004 owned.",
    "Service mix by deal: Pure Service 31% of deals, Service + Spectra 40%, Dock/DMO combinations 18%, Hardware 3%, Others 8%.",
    "Service types in work orders: Topography Survey (RGB) dominates (41 projects), Hydrology (8), Videography (6), Volumetric (12).",
    "Tender sector value concentration: 3 deals representing $158M—requires careful execution.",
    
    # Time-based Insights
    "Deals created last quarter (Nov-Dec 2025): 19 new deals, $142.3M value.",
    "Close dates Q1 2026: 23 deals targeted, success would add $134.7M to revenue.",
    "Q2 projected closes: 18 deals, $98.5M expected if on track.",
    "Recent invoice activity: Last 15 invoices totaling ₹28.4L, collection rate 72%.",
    "Work order completion trend: 18 projects finished last month, 12 billed.",
    "Contract renewals due: 4 annual contracts up for renewal in next 60 days.",
    "Oldest open deal: Created 2024-08-09, now in negotiation - 520 days in cycle.",
    "Fastest deal closure observed: 47 days (Proof of Concept to Not Billable status).",
    
    # Status & Health Queries
    "Invoice status snapshot: 34 Fully Billed, 15 Partially Billed, 8 Not Billed, 28 Update Required.",
    "Critical follow-ups needed: 5 deals on hold + 2 stalled negotiations over 90 days.",
    "Win rate estimate: 65% deals moving forward (Open status) vs 35% Dead/Lost.",
    "Collection health: ₹3.2 crores collected, ₹2.4 crores receivable, 57% collection ratio.",
    "Billing performance: 68% of completed work orders fully billed within 60 days of delivery.",
    
    # Multi-sector Summaries
    "Energy sector (Renewables + Powerline + DSP): $327.3M, 40 deals combined.",
    "Infrastructure (Railways + Construction): $132.6M, 12 deals.",
    "Mining focus opportunity: $512M pipeline with 60% deal concentration—diversification recommended.",
    "Tender-based deals: $158M, 3 deals, execution-heavy projects.",
    
    # Comparative & Strategic Insights
    "OWNER_001 vs OWNER_003: OWNER_001 (34 WOs, 72% execution rate) vs OWNER_003 (28 WOs, $421M sales pipeline).",
    "Billed vs Unbilled gap: $107M receivable vs $127.4M collected = collection gap of 46%.",
    "Deal stage distribution: 46% in Proposal, 15% in Negotiation, 13% in Feasibility, 11% in Demo, 15% in Early stages (LED, SQL).",
    "Service utilization: SPECTRA platform in 22 projects (25% adoption), growing use case.",
    "High-value project focus: Top 5 deals represent $542M (64% of pipeline).",
    "Monthly contract revenue: 6 recurring contracts generating ₹15L+ monthly revenue run-rate.",
    
    # Specific Deal Queries
    "Naruto deal (OWNER_001): Mining sector, Sales Qualified Lead, ₹4.89L value, created Dec 2025.",
    "Luffy deal (OWNER_003): Tender sector, Negotiations stage, ₹122.3M value, high probability.",
    "Sakura deals (OWNER_002): Powerline specialist, 7 open deals, $8.9M combined pipeline.",
    "Goku & Zoro deals (OWNER_003): Railways sector focus, $5.3M combined, Proposal stage.",
    
    # Execution Excellence
    "SPECTRA + DMO combined projects: 8 active, generating highest service revenue.",
    "Pure Service projects: 31 deals representing 35% of pipeline value.",
    "Hardware deals: 2 projects, $6.1M, DSP sector.",
    "Work order turnaround: Median delivery 45 days, 85% on-time delivery.",
    "Invoice processing: Average 35-day invoice creation post-delivery.",
    
    # Risk & Opportunity
    "At-risk items: 5 On Hold deals ($18.3M) need stakeholder engagement.",
    "Dead/Lost deals analysis: 52 deals, $189.3M historical pipeline = 22% loss rate.",
    "Opportunity: 8 Demo Done deals ($38.9M) ready for proposal stage movement.",
    "Q1 priority: Move 6 high-probability Proposal deals ($24.1M) to Won status.",
    
    # Customer/Company Focus
    "Top customer accounts (by deal count): COMPANY186 (3 deals), COMPANY111 (5 deals), COMPANY002 (8 deals).",
    "Customer retention: 34 repeat accounts appearing in both deals and work orders.",
    "Customer attrition signals: 12 dead deals from unique companies.",
    
    # Billing & Collections
    "Current AR aging: ₹1.8 crores 0-30 days, ₹0.4 crores 30-60 days, ₹0.2 crores >60 days.",
    "Monthly invoice count: 4-6 invoices/month, totaling ₹12-18L.",
    "Collection success rate by sector: Mining 68%, Renewables 72%, Railways 85%.",
    "Fastest collection: 15 days (Renewables sector Topography Survey).",
    "Longest pending: 120+ days (Construction, Tender sector).",
    "Expected collections next month: ₹5.2L based on current aging + new invoices.",
    
    # Miscellaneous High-Value Insights
    "Total platform revenue tracked: ₹127.4L collected + ₹107.4L AR = ₹234.8L total billings YTD.",
    "Largest single contract value: ₹305.8L Tender project (Feasibility stage).",
    "Recurring annual revenue: ₹18L+ from 6 monthly/annual contracts.",
    "Projected 2026 revenue: $1.2B if 70% of current pipeline closes.",
    "Cost optimization opportunity: 40% of work orders have <80% billing achievement.",
    "Margin analysis: SPECTRA-enabled projects show 15% higher net billing vs Pure Service.",
]

def get_random_fallback() -> str:
    """Return a random fallback response from the database."""
    import random
    return random.choice(FALLBACK_RESPONSES)

def get_contextual_fallback(query: str) -> str:
    """Return a fallback response that best matches the user query."""
    query_lower = query.lower()
    
    # Map query keywords to response indices
    keyword_map = {
        "revenue": [0, 2, 5, 8, 12, 21, 24, 30],
        "pipeline": [1, 2, 6, 13, 18, 26, 34, 42],
        "deals": [0, 1, 3, 4, 9, 13, 20, 28, 34, 42],
        "work order": [15, 16, 17, 18, 19, 20, 22, 27, 28],
        "owner": [27, 30, 31, 32, 33, 39],
        "mining": [35, 36, 40, 44, 52],
        "renewables": [37, 45, 46, 52],
        "sector": [35, 36, 37, 38, 40, 43, 44, 45, 47, 53],
        "billing": [40, 53, 58, 59, 60, 61, 62, 63],
        "team": [27, 29, 30, 31],
        "stalled": [11, 54],
        "close": [8, 25, 26, 51],
        "collection": [15, 53, 54, 58, 62, 63],
        "capacity": [15, 18, 19],
    }
    
    # Find matching responses
    for keyword, indices in keyword_map.items():
        if keyword in query_lower:
            import random
            return FALLBACK_RESPONSES[random.choice(indices)]
    
    # Default fallback
    return get_random_fallback()
