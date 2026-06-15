from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
db = client["mental_health_db"]

users_collection = db["users"]
quiz_collection = db["quiz_questions"]
assessments_collection = db["assessments"]
progress_collection = db["progress_tracker"]
chat_history_collection = db["chat_history"]
selfcare_suggestions_collection = db["selfcare_suggestions"]
todos_collection = db["todos"]
reminders_collection = db["reminders"]
appointments_collection = db["appointments"]
therapists_collection = db["therapists"]
notifications_collection = db["notifications"]
