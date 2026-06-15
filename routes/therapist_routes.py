from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import users_collection, appointments_collection
from utils import login_required
from bson.objectid import ObjectId
from datetime import datetime

therapist_bp = Blueprint('therapists', __name__)

@therapist_bp.route('/therapists')
@login_required
def view_therapists():
    therapists = list(users_collection.find({"role": "Therapist", "verified": True}))
    
    # Build appointment map for the current user
    user_id = session.get("user_id")
    appointment_map = {}
    if user_id:
        user_appointments = list(appointments_collection.find({"patient_id": user_id}))
        for appt in user_appointments:
            # Map therapist_id to the appointment status (e.g. "Pending", "Accepted")
            appointment_map[str(appt["therapist_id"])] = appt.get("status", "Pending")
            
    return render_template('therapist_suggestions.html', therapists=therapists, appointment_map=appointment_map)

@therapist_bp.route('/manage_therapists')
@login_required
def manage_therapists():
    unverified_therapists = list(users_collection.find({"role": "Therapist", "verified": False}))
    verified_therapists = list(users_collection.find({"role": "Therapist", "verified": True}))
    return render_template('manage_therapists.html',
                           unverified_therapists=unverified_therapists,
                           verified_therapists=verified_therapists)

@therapist_bp.route('/verify_therapist/<therapist_id>')
@login_required
def verify_therapist(therapist_id):
    users_collection.update_one({"_id": ObjectId(therapist_id)}, {"$set": {"verified": True}})
    flash("Therapist has been verified.", "success")
    return redirect(url_for('therapists.manage_therapists'))

@therapist_bp.route('/reject_therapist/<therapist_id>')
@login_required
def reject_therapist(therapist_id):
    users_collection.delete_one({"_id": ObjectId(therapist_id)})
    flash("Therapist application has been rejected.", "warning")
    return redirect(url_for('therapists.manage_therapists'))

@therapist_bp.route('/delete_therapist/<therapist_id>')
@login_required
def delete_therapist(therapist_id):
    users_collection.delete_one({"_id": ObjectId(therapist_id)})
    flash("Therapist has been deleted.", "danger")
    return redirect(url_for('therapists.manage_therapists'))

@therapist_bp.route('/edit_therapist/<therapist_id>', methods=['GET', 'POST'])
@login_required
def edit_therapist(therapist_id):
    user_session = session.get("user", {})
    if user_session.get("role", "").lower() != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        specialization = request.form.get("specialization")
        qualification = request.form.get("qualification")
        experience = request.form.get("experience")
        contact = request.form.get("contact")

        update_data = {
            "name": name,
            "email": email,
            "specialization": specialization,
            "qualification": qualification,
            "contact": contact
        }
        
        if experience and experience.isdigit():
            update_data["experience"] = int(experience)

        users_collection.update_one(
            {"_id": ObjectId(therapist_id)},
            {"$set": update_data}
        )
        flash("Therapist updated successfully.", "success")
        return redirect(url_for("therapists.manage_therapists"))

    therapist = users_collection.find_one({"_id": ObjectId(therapist_id)})
    if not therapist:
        flash("Therapist not found.", "danger")
        return redirect(url_for("therapists.manage_therapists"))
        
    return render_template("edit_therapist.html", therapist=therapist)


@therapist_bp.route('/therapist_dashboard')
@login_required
def therapist_dashboard():
    therapist_id = session.get('therapist_id')
    if not therapist_id:
        return redirect(url_for('auth.login'))

    appointments = list(appointments_collection.find({
        "therapist_id": therapist_id,
        "status": "Pending"
    }))
    return render_template('therapist_dashboard.html', requests=appointments)

@therapist_bp.route('/request_appointment/<therapist_id>', methods=['POST'])
@login_required
def request_appointment(therapist_id):
    user = users_collection.find_one({"_id": ObjectId(session['user_id'])})
    interest = request.form.get("interest", "").strip()
    
    if not interest:
        flash("Please mention your concern before requesting.", "warning")
        return redirect(url_for('therapists.view_therapists'))

    appointment_data = {
        "patient_id": str(user["_id"]),
        "patient_name": user["name"],
        "patient_email": user["email"],
        "interest": interest,
        "therapist_id": therapist_id,
        "status": "Pending",
        "timestamp": datetime.utcnow()
    }

    appointments_collection.insert_one(appointment_data)
    flash("Appointment request sent successfully.", "success")
    return redirect(url_for('therapists.view_therapists'))

@therapist_bp.route('/accept_appointment/<appointment_id>')
@login_required
def accept_appointment(appointment_id):
    appointments_collection.update_one({"_id": ObjectId(appointment_id)}, {"$set": {"status": "Accepted"}})
    flash("Appointment accepted.", "success")
    return redirect(url_for('therapists.therapist_dashboard'))

@therapist_bp.route('/reject_appointment/<appointment_id>')
@login_required
def reject_appointment(appointment_id):
    appointments_collection.update_one({"_id": ObjectId(appointment_id)}, {"$set": {"status": "Rejected"}})
    flash("Appointment rejected.", "warning")
    return redirect(url_for('therapists.therapist_dashboard'))
