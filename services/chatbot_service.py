import urllib.request
import urllib.error
import json
import time
import os
from database import chat_history_collection
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

def get_chatbot_response(user_id, user_input):
    # Guard: missing API key
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return "The chatbot is not configured yet. Please add a GEMINI_API_KEY to the .env file."

    try:
        history_doc = chat_history_collection.find_one({"user_id": user_id})
        if not history_doc:
            history_doc = {"user_id": user_id, "messages": [], "timestamp": datetime.utcnow()}
        
        conversation_history = history_doc.get("messages", [])
        conversation_history.append({"role": "user", "parts": [{"text": user_input}]})

        payload = json.dumps({
            "system_instruction": {
                "parts": [{"text": (
                    "You are MindAide, a compassionate and supportive mental health assistant. "
                    "You provide empathetic, helpful responses about mental health topics. "
                    "Always recommend professional help for serious issues."
                )}]
            },
            "contents": conversation_history
        }).encode("utf-8")

        req = urllib.request.Request(
            GEMINI_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        for attempt in range(2):
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    raw = response.read().decode("utf-8")
                    result = json.loads(raw)

                    # Safe extraction — handle unexpected API response shapes
                    candidates = result.get("candidates")
                    if not candidates:
                        error_msg = result.get("error", {}).get("message", "Unknown API error")
                        return f"I'm having a little trouble right now. API says: {error_msg}"

                    bot_reply = candidates[0]["content"]["parts"][0]["text"]

                    conversation_history.append({"role": "model", "parts": [{"text": bot_reply}]})
                    chat_history_collection.update_one(
                        {"user_id": user_id},
                        {"$set": {"messages": conversation_history, "timestamp": datetime.utcnow()}},
                        upsert=True
                    )
                    return bot_reply

            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt == 0:
                    time.sleep(6)
                    continue
                try:
                    error_body = json.loads(e.read().decode("utf-8"))
                    api_error = error_body.get("error", {}).get("message", str(e))
                except Exception:
                    api_error = str(e)
                return f"I'm having a little trouble right now ({e.code}): {api_error}"
            except urllib.error.URLError as e:
                return f"I can't reach the AI server at the moment. Please check your internet connection. ({e.reason})"

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

    return "I'm a little busy right now, please try again in a moment! 😊"
