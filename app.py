import os
from flask import Flask
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv

from routes.auth_routes import auth_bp
from routes.quiz_routes import quiz_bp
from routes.chatbot_routes import chatbot_bp
from routes.selfcare_routes import selfcare_bp
from routes.therapist_routes import therapist_bp
from routes.progress_routes import progress_bp

from services.selfcare_service import check_reminders
from apscheduler.schedulers.background import BackgroundScheduler
from database import users_collection, assessments_collection, chat_history_collection, therapists_collection
from hash_service import generate_password_hash

load_dotenv()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False 
CORS(app)

app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" 
app.config["SESSION_FILE_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "flask_session_data")
Session(app)

def setup_indexes():
    users_collection.create_index("email", unique=True)
    assessments_collection.create_index("user_id")
    chat_history_collection.create_index("user_id")
    therapists_collection.create_index("specialization")

setup_indexes()

def seed_admin():
    if not users_collection.find_one({"role": "Admin"}):
        users_collection.insert_one({
            "name": "System Admin",
            "email": "admin@mindaide.com",
            "password": generate_password_hash("admin123"),
            "role": "Admin"
        })
        print("Seeded default Admin: admin@mindaide.com / admin123")

seed_admin()

scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders, 'interval', minutes=1)
if not scheduler.running:
    scheduler.start()

app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(selfcare_bp, url_prefix="/selfcare")
app.register_blueprint(therapist_bp)
app.register_blueprint(progress_bp, url_prefix="/progress")

if __name__ == "__main__":
    app.run(debug=True)
