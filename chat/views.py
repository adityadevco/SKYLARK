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
    if not env["monday_api_key"]:
        return json.dumps({"error": "MONDAY_API_KEY is not configured."})
    if not board_id:
        return json.dumps({"error": "Board ID is not configured."})

    try:
        parsed_board_id = int(board_id)
    except (TypeError, ValueError):
        return json.dumps({"error": f"Invalid board ID: {board_id}"})

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
        response = requests.post(
            url,
            json={"query": query, "variables": {"boardId": [parsed_board_id]}},
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
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
    except (requests.RequestException, ValueError, KeyError) as e:
        return json.dumps({"error": str(e)})


def _is_rate_limit_error(error_text: str) -> bool:
    lowered = (error_text or "").lower()
    return any(
        marker in lowered
        for marker in [
            "429",
            "quota",
            "rate limit",
            "resource exhausted",
            "too many requests",
        ]
    )


def _get_model_candidates() -> list[str]:
    primary_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    configured_fallbacks = [
        model.strip()
        for model in os.getenv("GEMINI_MODEL_FALLBACKS", "gemini-1.5-flash").split(",")
        if model.strip()
    ]
    ordered = [primary_model, *configured_fallbacks]
    deduped: list[str] = []
    for model_name in ordered:
        if model_name not in deduped:
            deduped.append(model_name)
    return deduped

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

            if not isinstance(messages, list) or not messages:
                return JsonResponse({"error": "At least one message is required."}, status=400)
            if not isinstance(messages[-1], dict) or "content" not in messages[-1]:
                return JsonResponse({"error": "Malformed message payload."}, status=400)
            
            # format history for gemini
            history = []
            for m in messages[:-1]:
                if not isinstance(m, dict):
                    continue
                content = m.get("content")
                if not content:
                    continue
                role = "user" if m.get("role") == "user" else "model"
                history.append({"role": role, "parts": [content]})
                
            last_msg = messages[-1]["content"]
            if not isinstance(last_msg, str) or not last_msg.strip():
                return JsonResponse({"error": "Last message cannot be empty."}, status=400)
            
            response = None
            last_error = None
            for model_name in _get_model_candidates():
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        tools=[get_work_orders_data, get_deals_data],
                        system_instruction="You are Skylark, an AI BI Agent analyzing Monday.com data for executives. ALWAYS use your tools to fetch data if you need facts about deals or work orders. Be concise, highly insightful, format numbers perfectly, and synthesize directly from tool returns."
                    )
                    chat = model.start_chat(history=history, enable_automatic_function_calling=True)
                    response = chat.send_message(last_msg)
                    break
                except Exception as model_error:
                    last_error = model_error
                    if _is_rate_limit_error(str(model_error)):
                        continue
                    raise

            if response is None:
                rate_limit_message = (
                    "Gemini API limits were reached across configured models. "
                    "Please retry in about a minute."
                )
                if last_error and not _is_rate_limit_error(str(last_error)):
                    return JsonResponse({"error": str(last_error)}, status=500)
                return JsonResponse({"error": rate_limit_message}, status=429)
            
            # Convert markdown to html for rendering logic
            html_content = markdown.markdown(response.text, extensions=['fenced_code', 'tables'])
            
            return JsonResponse({
                "role": "assistant",
                "content": html_content,
                "raw_content": response.text
            })
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)
        except Exception as e:
            error_str = str(e)
            
            if _is_rate_limit_error(error_str):
                clean_error = "Gemini API rate limits were reached. Please wait a minute and try again."
                status = 429
            else:
                clean_error = error_str
                status = 500
                
            return JsonResponse({"error": clean_error}, status=status)
            
    return JsonResponse({"error": "Invalid method"}, status=405)
