from pymongo import MongoClient
import hashlib
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
users_col = db["users"]

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Clear existing users except admin, or clear all and recreate admin
users_col.delete_many({})

users_to_insert = [
    # Admin
    {
        "name": "Admin User",
        "email": "admin@gmail.com",
        "password": hash_pass("Admin@123"),
        "role": "Admin",
        "verified": True
    },
    # Patients
    {
        "name": "Patient 1",
        "email": "patient1@gmail.com",
        "password": hash_pass("pat123"),
        "role": "Patient",
        "gender": "Male",
        "age": 25,
        "caretaker_email": "caretaker1@gmail.com"
    },
    {
        "name": "Patient 2",
        "email": "patient2@gmail.com",
        "password": hash_pass("pat123"),
        "role": "Patient",
        "gender": "Female",
        "age": 30,
        "caretaker_email": "caretaker2@gmail.com"
    },
    {
        "name": "Patient 3",
        "email": "patient3@gmail.com",
        "password": hash_pass("pat123"),
        "role": "Patient",
        "gender": "Non-binary",
        "age": 22,
        "caretaker_email": ""
    },
    # Caretakers
    {
        "name": "Caretaker 1",
        "email": "caretaker1@gmail.com",
        "password": hash_pass("care123"),
        "role": "Caretaker"
    },
    {
        "name": "Caretaker 2",
        "email": "caretaker2@gmail.com",
        "password": hash_pass("care123"),
        "role": "Caretaker"
    },
    {
        "name": "Caretaker 3",
        "email": "caretaker3@gmail.com",
        "password": hash_pass("care123"),
        "role": "Caretaker"
    },
    # Therapists
    {
        "name": "Therapist 1",
        "email": "therapist1@gmail.com",
        "password": hash_pass("ther123"),
        "role": "Therapist",
        "specialization": "Clinical Psychology",
        "qualification": "PhD",
        "experience": 5,
        "contact": "123-456-7890",
        "verified": True
    },
    {
        "name": "Therapist 2",
        "email": "therapist2@gmail.com",
        "password": hash_pass("ther123"),
        "role": "Therapist",
        "specialization": "CBT",
        "qualification": "MSc Psychology",
        "experience": 3,
        "contact": "123-456-7891",
        "verified": True
    },
    {
        "name": "Therapist 3",
        "email": "therapist3@gmail.com",
        "password": hash_pass("ther123"),
        "role": "Therapist",
        "specialization": "Family Therapy",
        "qualification": "MA Counseling",
        "experience": 8,
        "contact": "123-456-7892",
        "verified": False  # One unverified for testing admin dashboard
    }
]

result = users_col.insert_many(users_to_insert)
print(f"Inserted {len(result.inserted_ids)} users successfully.")
