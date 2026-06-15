import os
import json
import time
import urllib.request
from flask import Blueprint, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ Gemini API Key is missing. Add GEMINI_API_KEY to your .env file.")

GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
)

chatbot_bp = Blueprint("chatbot", __name__, template_folder="templates")

# Simple in-memory conversation history per session
conversation_history = []

def get_chatbot_response(user_input):
    """Calls Gemini REST API and returns the response text."""
    conversation_history.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })

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

    for attempt in range(2):  # Try twice
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                bot_reply = result["candidates"][0]["content"]["parts"][0]["text"]
                conversation_history.append({
                    "role": "model",
                    "parts": [{"text": bot_reply}]
                })
                return bot_reply
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(6)  # Wait 6s then retry once
                continue
            return "I'm a little busy right now, please try again in a moment! 😊"
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"


@chatbot_bp.route("/", methods=["GET", "POST"])
def chatbot_page():
    if request.method == "POST":
        user_message = request.json.get("message", "")
        bot_response = get_chatbot_response(user_message)
        return jsonify({"response": bot_response})

    return render_template("chatbot.html")
