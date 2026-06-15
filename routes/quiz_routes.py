from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database import quiz_collection
from bson.objectid import ObjectId
from services.quiz_service import get_quiz_questions, process_quiz_results
from utils import login_required

quiz_bp = Blueprint("quiz", __name__, template_folder="../templates")

@quiz_bp.route("/", methods=["GET", "POST"])
@login_required
def quiz_page():
    if request.method == "GET":
        questions = get_quiz_questions()
        return render_template("quiz.html", questions=questions)

    elif request.method == "POST":
        user_answers = request.form
        result = process_quiz_results(session.get("user_id"), user_answers)
        session["quiz_result"] = result
        return redirect(url_for("quiz.quiz_result_page"))

@quiz_bp.route("/result")
@login_required
def quiz_result_page():
    result = session.get("quiz_result", "Unknown")
    return render_template("quiz_result.html", result=result)

@quiz_bp.route("/manage", methods=["GET", "POST"])
@login_required
def manage_quiz():
    user = session.get("user", {})
    if user.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        question_text = request.form.get("question_text")
        category = request.form.get("category")
        options = [
            {"text": request.form.get("option1"), "value": f"{category}:4"},
            {"text": request.form.get("option2"), "value": f"{category}:3"},
            {"text": request.form.get("option3"), "value": f"{category}:2"},
            {"text": request.form.get("option4"), "value": f"{category}:1"}
        ]
        if question_text and category:
            quiz_collection.insert_one({
                "question_text": question_text,
                "category": category,
                "options": options
            })
            flash("Question added successfully.", "success")
            return redirect(url_for("quiz.manage_quiz"))

    questions = list(quiz_collection.find())
    return render_template("manage_quiz.html", questions=questions)

@quiz_bp.route("/edit/<question_id>", methods=["GET", "POST"])
@login_required
def edit_quiz(question_id):
    user = session.get("user", {})
    if user.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        question_text = request.form.get("question_text")
        category = request.form.get("category")
        options = [
            {"text": request.form.get("option1"), "value": f"{category}:4"},
            {"text": request.form.get("option2"), "value": f"{category}:3"},
            {"text": request.form.get("option3"), "value": f"{category}:2"},
            {"text": request.form.get("option4"), "value": f"{category}:1"}
        ]
        
        quiz_collection.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": {
                "question_text": question_text,
                "category": category,
                "options": options
            }}
        )
        flash("Question updated successfully.", "success")
        return redirect(url_for("quiz.manage_quiz"))

    question = quiz_collection.find_one({"_id": ObjectId(question_id)})
    if not question:
        flash("Question not found.", "danger")
        return redirect(url_for("quiz.manage_quiz"))
        
    return render_template("edit_quiz.html", question=question)

@quiz_bp.route("/delete/<question_id>")
@login_required
def delete_quiz(question_id):
    user = session.get("user", {})
    if user.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    quiz_collection.delete_one({"_id": ObjectId(question_id)})
    flash("Question deleted successfully.", "success")
    return redirect(url_for("quiz.manage_quiz"))
