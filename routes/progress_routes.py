from flask import Blueprint, jsonify, session
from database import progress_collection, assessments_collection
from utils import login_required

progress_bp = Blueprint("progress", __name__)

@progress_bp.route("/", methods=["GET"])
@login_required
def get_progress():
    user_id = session.get("user_id")
    progress_doc = progress_collection.find_one({"user_id": user_id})
    if not progress_doc:
        return jsonify({"message": "No progress data found.", "history": []})

    history = []
    for assessment_id in progress_doc.get("assessments", []):
        assessment = assessments_collection.find_one({"_id": assessment_id})
        if assessment:
            history.append({
                "date": assessment["date"].strftime("%Y-%m-%d %H:%M:%S"),
                "score": assessment["score"],
                "category": assessment["category"]
            })
    
    return jsonify({"history": history})
