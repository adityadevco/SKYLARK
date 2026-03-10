import os
import json
import requests
import markdown
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configure Gemini with environment variables 
# Using lazy evaluation for environment loading
def lazy_get_env():
    return {
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "monday_api_key": os.getenv("MONDAY_API_KEY"),
        "work_orders_board_id": os.getenv("MONDAY_WORK_ORDERS_BOARD_ID"),
        "deals_board_id": os.getenv("MONDAY_DEALS_BOARD_ID")
    }

# Dynamic initialization inside the fetch view

def fetch_monday_data(board_id: str) -> str:
    """Fetches and cleans current data from a specific Monday board ID."""
    env = lazy_get_env()
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": env["monday_api_key"],
        "API-Version": "2023-10",
        "Content-Type": "application/json"
    }
    
    query = '''
    query ($boardId: [ID!]) {
      boards(ids: $boardId) {
        name
        items_page(limit: 100) {
          items {
            id
            name
            column_values {
              id
              text
              column {
                title
              }
            }
          }
        }
      }
    }
    '''
    try:
        response = requests.post(url, json={"query": query, "variables": {"boardId": [int(board_id)]}}, headers=headers)
        data = response.json()
        if "errors" in data:
            return json.dumps({"error": str(data["errors"])})
        
        boards = data.get("data", {}).get("boards", [])
        if not boards:
            return "No data found."
            
        items = boards[0].get("items_page", {}).get("items", [])
        cleaned = []
        for item in items:
            rec = {"Item Name": item.get("name")}
            for col in item.get("column_values", []):
                title = col.get("column", {}).get("title", col.get("id"))
                text = col.get("text")
                if text:
                    rec[title] = text
            cleaned.append(rec)
        return json.dumps(cleaned)
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_work_orders_data() -> str:
    """Gets all current work orders from the Monday.com board including statuses and assignees."""
    return fetch_monday_data(lazy_get_env()["work_orders_board_id"])

def get_deals_data() -> str:
    """Gets all current sales pipeline deals from the Monday.com board including stages and deal values."""
    return fetch_monday_data(lazy_get_env()["deals_board_id"])

def index(request):
    return render(request, "chat/index.html")

@csrf_exempt
def api_chat(request):
    if request.method == "POST":
        env = lazy_get_env()
        if not env["gemini_api_key"]:
            return JsonResponse({"error": "Gemini API key is not configured in .env.local."}, status=400)
            
        genai.configure(api_key=env["gemini_api_key"])
            
        try:
            data = json.loads(request.body)
            messages = data.get("messages", [])
            
            # format history for gemini
            history = []
            for m in messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history.append({"role": role, "parts": [m["content"]]})
                
            last_msg = messages[-1]["content"]
            
            # Initialize model with tools
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                tools=[get_work_orders_data, get_deals_data],
                system_instruction="You are Skylark, an AI BI Agent analyzing Monday.com data for executives. ALWAYS use your tools to fetch data if you need facts about deals or work orders. Be concise, highly insightful, format numbers perfectly, and synthesize directly from tool returns."
            )
            
            # Start chat session
            chat = model.start_chat(history=history, enable_automatic_function_calling=True)
            response = chat.send_message(last_msg)
            
            # Convert markdown to html for rendering logic
            html_content = markdown.markdown(response.text, extensions=['fenced_code', 'tables'])
            
            return JsonResponse({
                "role": "assistant",
                "content": html_content,
                "raw_content": response.text
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Invalid method"}, status=405)
