from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from database import users_collection
from hash_service import generate_password_hash, check_password_hash
from utils import login_required
from bson.objectid import ObjectId
import re

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return render_template("home.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    try:
        data = request.get_json(silent=True) or request.form
        name = data.get("name")
        role = data.get("role")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        age = data.get("age")
        gender = data.get("gender")
        interests = data.get("interests")
        specialization = data.get("specialization")
        qualification = data.get("qualification")
        experience = data.get("experience")
        contact = data.get("contact")
        patient_email = data.get("patient_email")

        if not name or not role or not email or not password or not confirm_password:
            return jsonify({"success": False, "message": "All fields are required"}), 400

        if password != confirm_password:
            return jsonify({"success": False, "message": "Passwords do not match"}), 400

        if len(password) < 6 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            return jsonify({"success": False, "message": "Password must be at least 6 characters long and contain both letters and numbers."}), 400

        if users_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email is already registered"}), 400

        hashed_password = generate_password_hash(password)

        user_data = {
            "name": name,
            "role": role,
            "email": email,
            "password": hashed_password,
        }

        if role == "Patient":
            if not age or not gender:
                return jsonify({"success": False, "message": "Age and Gender are required for Patients"}), 400
            user_data.update({
                "age": int(age),
                "gender": gender,
                "interests": interests or []
            })
        elif role == "Therapist":
            if not specialization or not qualification or not experience or not contact:
                return jsonify({"success": False, "message": "Specialization, Qualification, Experience, and Contact are required for Therapists"}), 400
            
            if not re.fullmatch(r"\d{10}", contact):
                return jsonify({"success": False, "message": "Contact must be a valid 10-digit number"}), 400

            user_data.update({
                "specialization": specialization,
                "qualification": qualification,
                "experience": int(experience),
                "contact": contact,
                "verified": False
            })
        elif role == "Caretaker":
            patient_email = patient_email.strip() if patient_email else ""
            if not patient_email or not users_collection.find_one({"email": {"$regex": f"^{patient_email}$", "$options": "i"}, "role": "Patient"}):
                return jsonify({"success": False, "message": "Invalid patient email"}), 400
            user_data.update({"patient_email": patient_email})

        users_collection.insert_one(user_data)
        return jsonify({"success": True, "message": "Account created successfully!"}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required!"}), 400

        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            if user.get("role", "").lower() == "therapist" and not user.get("verified", False):
                return jsonify({"error": "Your account is pending verification by an Admin."}), 403

            session["user"] = {
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role")
            }
            session["_id"] = str(user["_id"])
            session["user_id"] = str(user["_id"])

            if user.get("role", "").lower() == "therapist" and user.get("verified", False):
                session["therapist_id"] = str(user["_id"])

            return jsonify({"redirect": url_for("auth.dashboard")}), 200
        else:
            return jsonify({"error": "Invalid credentials. Try again!"}), 400

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    user = session.get("user", {})
    user_role = user.get("role", "").lower()
    
    if user_role == "admin":
        return redirect(url_for("auth.admin_dashboard"))
    elif user_role == "therapist":
        return redirect(url_for("therapists.therapist_dashboard"))
    elif user_role == "caretaker":
        return redirect(url_for("auth.caretaker_dashboard"))
    elif user_role == "patient":
        return redirect(url_for("auth.patient_dashboard"))
        
    return redirect(url_for("auth.login"))

@auth_bp.route("/admin_dashboard")
@login_required
def admin_dashboard():
    user = session.get("user", {})
    if user.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html")

@auth_bp.route("/patient_dashboard")
@login_required
def patient_dashboard():
    return render_template("dashboard.html")

@auth_bp.route("/caretaker_dashboard")
@login_required
def caretaker_dashboard():
    caretaker = users_collection.find_one({"_id": ObjectId(session['user_id'])})
    if not caretaker or caretaker.get('role', '').lower() != 'caretaker':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))

    patient_email = caretaker.get("patient_email", "").strip()
    patient = users_collection.find_one({"email": {"$regex": f"^{patient_email}$", "$options": "i"}, "role": "Patient"})

    return render_template("caretaker_dashboard.html", caretaker=caretaker, patient=patient)

@auth_bp.route("/manage_users")
@login_required
def manage_users():
    user = session.get("user", {})
    if user.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))
    
    users = list(users_collection.find({"role": {"$in": ["Patient", "Caretaker"]}}))
    for u in users:
        u["_id"] = str(u["_id"])
    return render_template("manage_users.html", users=users)

@auth_bp.route("/edit_user/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user_session = session.get("user", {})
    if user_session.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if name and email:
            users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": name, "email": email}})
            flash("User updated successfully.", "success")
            return redirect(url_for("auth.manage_users"))
        
    user_doc = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        flash("User not found.", "danger")
        return redirect(url_for("auth.manage_users"))
        
    user_doc["_id"] = str(user_doc["_id"])
    return render_template("edit_user.html", user=user_doc)

@auth_bp.route("/delete_user/<user_id>")
@login_required
def delete_user(user_id):
    user_session = session.get("user", {})
    if user_session.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    users_collection.delete_one({"_id": ObjectId(user_id)})
    flash("User deleted successfully.", "success")
    return redirect(url_for("auth.manage_users"))
