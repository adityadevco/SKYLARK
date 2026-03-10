import os
import json
import re
import requests
import markdown
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .fallback_responses import get_contextual_fallback

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


def _fallback_reply(question: str) -> str:
    """
    Returns a professional, data-driven fallback response when Gemini is unavailable.
    Selects from 100+ CSV-sourced response templates based on query context.
    """
    return get_contextual_fallback(question)

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
        gemini_enabled = bool(env["gemini_api_key"])
        if gemini_enabled:
            genai.configure(api_key=env["gemini_api_key"])
            
        try:
            data = json.loads(request.body)
            messages = data.get("messages", [])

            if not isinstance(messages, list) or not messages:
                return JsonResponse({"error": "At least one message is required."}, status=400)
            if not isinstance(messages[-1], dict) or "content" not in messages[-1]:
                return JsonResponse({"error": "Malformed message payload."}, status=400)
            
            last_msg = messages[-1]["content"]
            if not isinstance(last_msg, str) or not last_msg.strip():
                return JsonResponse({"error": "Last message cannot be empty."}, status=400)
            
            response = None
            last_error = None
            
            # Try Gemini first if enabled
            if gemini_enabled:
                history = []
                for m in messages[:-1]:
                    if not isinstance(m, dict):
                        continue
                    content = m.get("content")
                    if not content:
                        continue
                    role = "user" if m.get("role") == "user" else "model"
                    history.append({"role": role, "parts": [content]})
                    
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
                        if not _is_rate_limit_error(str(model_error)):
                            break
                        continue

            # Fallback to direct Monday board data if Gemini unavailable or failed
            if response is None:
                fallback_text = _fallback_reply(last_msg)
                fallback_html = markdown.markdown(fallback_text, extensions=['fenced_code', 'tables'])
                return JsonResponse({
                    "role": "assistant",
                    "content": fallback_html,
                    "raw_content": fallback_text,
                    "fallback": True,
                })
            
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
            fallback_text = _fallback_reply(last_msg if 'last_msg' in locals() else "")
            fallback_html = markdown.markdown(fallback_text, extensions=['fenced_code', 'tables'])
            return JsonResponse({
                "role": "assistant",
                "content": fallback_html,
                "raw_content": fallback_text,
                "fallback": True,
            })
            
    return JsonResponse({"error": "Invalid method"}, status=405)
