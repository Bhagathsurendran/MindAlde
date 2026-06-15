from flask import Blueprint, request, jsonify, render_template, session
from services.chatbot_service import get_chatbot_response
from utils import login_required

chatbot_bp = Blueprint("chatbot", __name__, template_folder="../templates")

@chatbot_bp.route("/", methods=["GET", "POST"])
@login_required
def chatbot_page():
    if request.method == "POST":
        try:
            user_message = (request.json or {}).get("message", "")
            user_id = session.get("user_id", "anonymous")
            bot_response = get_chatbot_response(user_id, user_message)
            return jsonify({"response": bot_response})
        except Exception as e:
            return jsonify({"response": f"Sorry, something went wrong: {str(e)}"}), 200

    return render_template("chatbot.html")

