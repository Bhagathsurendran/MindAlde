from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from database import selfcare_suggestions_collection, reminders_collection, users_collection
from utils import login_required
from bson.objectid import ObjectId
from datetime import datetime

selfcare_bp = Blueprint("selfcare", __name__, template_folder="../templates")

@selfcare_bp.route("/", methods=["GET"])
@login_required
def selfcare_home():
    return render_template("selfcare.html")

@selfcare_bp.route("/suggestions/", methods=["GET"])
@login_required
def suggestions_page():
    category = request.args.get('category')
    if not category:
        return redirect(url_for('selfcare.selfcare_home'))
    return render_template('suggestions.html', category=category)

@selfcare_bp.route("/get_suggestions", methods=["GET"])
@login_required
def get_suggestions():
    category = request.args.get("category")
    if not category:
        return jsonify({"error": "Category is required"}), 400

    suggestions = list(selfcare_suggestions_collection.find({"category": category}, {"_id": 0}))
    return jsonify(suggestions)

@selfcare_bp.route("/save_activity", methods=["POST"])
@login_required
def save_activity():
    data = request.json
    user_id = session.get("user_id")
    title = data.get("title")
    reminder_time = data.get("reminder_time") 

    if not title or not reminder_time:
        return jsonify({"error": "Missing required fields"}), 400

    reminder = {
        "user_id": user_id,
        "title": title,
        "reminder_time": datetime.strptime(reminder_time, "%Y-%m-%d %H:%M"),
        "status": "pending"
    }
    reminders_collection.insert_one(reminder)
    return jsonify({"message": "Activity saved with reminder!"}), 201

@selfcare_bp.route("/update_activity_status", methods=["POST"])
@login_required
def update_activity_status():
    data = request.json
    user_id = session.get("user_id")
    title = data.get("title")
    status = data.get("status")

    if not title or status not in ["Done", "Missed"]:
        return jsonify({"error": "Invalid input"}), 400

    reminders_collection.update_many(
        {"user_id": user_id, "title": title},
        {"$set": {"status": status}}
    )
    return jsonify({"message": "Activity status updated successfully!"}), 200

@selfcare_bp.route("/get_activities", methods=["GET"])
@login_required
def get_activities():
    user_id = session.get("user_id")
    activities = list(reminders_collection.find({"user_id": user_id}))
    for activity in activities:
        activity["_id"] = str(activity["_id"])
        activity["reminder_time"] = activity["reminder_time"].strftime("%Y-%m-%d %H:%M")
    
    return jsonify(activities), 200

@selfcare_bp.route("/get_resources", methods=["GET"])
@login_required
def get_resources():
    category = request.args.get("category")
    if not category:
        return jsonify({"error": "Category is required"}), 400

    # The DB stores flat documents - one per suggestion with a `type` field.
    # Group them into the nested format the frontend expects.
    docs = list(selfcare_suggestions_collection.find({"category": category}, {"_id": 0}))

    if not docs:
        return jsonify({"resources": None})

    resources = {
        "activities": [],
        "exercises": [],
        "youtube_videos": [],
        "articles": [],
        "books": []
    }

    for doc in docs:
        doc_type = (doc.get("type") or "").lower()
        title = doc.get("title", "")
        description = doc.get("description", "")
        link = doc.get("link", doc.get("url", "#"))

        if doc_type in ("activity", "activities", "grounding"):
            resources["activities"].append(description or title)
        elif doc_type in ("exercise", "exercises", "physical"):
            resources["exercises"].append(description or title)
        elif doc_type in ("video", "youtube", "youtube_video"):
            resources["youtube_videos"].append({"title": title, "url": link})
        elif doc_type in ("article", "articles", "reading"):
            resources["articles"].append({"title": title, "url": link})
        elif doc_type in ("book", "books"):
            resources["books"].append({"title": title, "url": link})
        else:
            # Fallback: treat any unrecognized type as an activity using description
            text = description or title
            if text:
                resources["activities"].append(text)

    return jsonify({"resources": resources})

@selfcare_bp.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    data = request.json
    user_id = session.get("user_id")
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"todos": {"text": text, "status": "pending"}}}
    )
    return jsonify({"success": True})

@selfcare_bp.route("/get_todos", methods=["GET"])
@login_required
def get_todos():
    user_id = session.get("user_id")
    user = users_collection.find_one({"_id": ObjectId(user_id)}, {"todos": 1})
    todos = user.get("todos", []) if user else []
    return jsonify(todos)

@selfcare_bp.route("/delete_todo", methods=["POST"])
@login_required
def delete_todo():
    data = request.json
    user_id = session.get("user_id")
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"todos": {"text": text}}}
    )
    return jsonify({"success": True})

@selfcare_bp.route("/add_notification", methods=["POST"])
@login_required
def add_notification():
    data = request.json
    user_id = session.get("user_id")
    text = data.get("text")
    time_str = data.get("time")

    if not text or not time_str:
        return jsonify({"error": "Missing fields"}), 400

    new_reminder = {
        "user_id": user_id,
        "text": text,
        "time": time_str,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    reminders_collection.insert_one(new_reminder)
    return jsonify({"success": True})

@selfcare_bp.route("/get_notifications", methods=["GET"])
@login_required
def get_notifications():
    user_id = session.get("user_id")
    notifs = list(reminders_collection.find({"user_id": user_id}).sort("time", 1))
    
    formatted_notifs = []
    for n in notifs:
        n["_id"] = str(n["_id"])
        formatted_notifs.append(n)
        
    return jsonify({"notifications": formatted_notifs})

@selfcare_bp.route("/mark_notification_done/<notif_id>", methods=["POST"])
@login_required
def mark_notification_done(notif_id):
    reminders_collection.update_one(
        {"_id": ObjectId(notif_id)},
        {"$set": {"status": "done"}}
    )
    return jsonify({"success": True})

@selfcare_bp.route("/delete_notification/<notif_id>", methods=["POST"])
@login_required
def delete_notification(notif_id):
    reminders_collection.delete_one({"_id": ObjectId(notif_id)})
    return jsonify({"success": True})

# ── ADMIN: Self-Care Resource Management ──────────────────────────────────────

@selfcare_bp.route("/manage_resources", methods=["GET"])
@login_required
def manage_resources():
    user_session = session.get("user", {})
    if user_session.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    selected_category = request.args.get("category", "")
    query = {"category": selected_category} if selected_category else {}
    resources = list(selfcare_suggestions_collection.find(query))
    for r in resources:
        r["_id"] = str(r["_id"])
    
    return render_template("manage_resources.html", resources=resources, selected_category=selected_category)

@selfcare_bp.route("/add_resource", methods=["POST"])
@login_required
def add_resource():
    user_session = session.get("user", {})
    if user_session.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    res_type = request.form.get("type", "activity").strip().lower()
    link = request.form.get("link", "").strip()
    description = request.form.get("description", "").strip()

    if not title or not category:
        flash("Title and Category are required.", "danger")
        return redirect(url_for("selfcare.manage_resources"))

    selfcare_suggestions_collection.insert_one({
        "title": title,
        "category": category,
        "type": res_type,
        "link": link or None,
        "description": description,
        "created_at": datetime.utcnow()
    })
    flash(f"Resource '{title}' added successfully!", "success")
    return redirect(url_for("selfcare.manage_resources", category=category))

@selfcare_bp.route("/delete_resource/<resource_id>", methods=["POST"])
@login_required
def delete_resource(resource_id):
    user_session = session.get("user", {})
    if user_session.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    selfcare_suggestions_collection.delete_one({"_id": ObjectId(resource_id)})
    flash("Resource deleted.", "danger")
    return redirect(request.referrer or url_for("selfcare.manage_resources"))

