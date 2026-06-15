import requests
import uuid
import sys
import time

BASE_URL = "http://localhost:5000"

def test_api():
    print("Testing Refactored Endpoints...")
    unique_id = str(uuid.uuid4())[:8]
    patient_email = f"patient_{unique_id}@test.com"
    pwd = "Password123"

    session = requests.Session()

    print("1. Registering Patient")
    res = session.post(f"{BASE_URL}/register", json={
        "name": "Refactored Patient",
        "role": "Patient",
        "email": patient_email,
        "password": pwd,
        "confirm_password": pwd,
        "age": 28,
        "gender": "Female",
        "interests": ["meditation"]
    })
    print(res.status_code, res.json())

    print("\n2. Logging in")
    res = session.post(f"{BASE_URL}/login", json={
        "email": patient_email,
        "password": pwd
    })
    print(res.status_code, res.json())

    print("\n3. Testing Protected Chatbot Route")
    res = session.post(f"{BASE_URL}/chatbot/", json={"message": "I feel anxious."})
    if res.status_code != 200:
        print("Chatbot Error:", res.text[:200])
    else:
        print(res.status_code, "Chatbot response received")

    print("\n4. Testing Protected Self-care get_suggestions")
    res = session.get(f"{BASE_URL}/selfcare/get_suggestions?category=Stress")
    print(res.status_code)

    print("\n5. Saving Activity")
    res = session.post(f"{BASE_URL}/selfcare/save_activity", json={
        "title": "Meditation",
        "reminder_time": "2026-05-01 10:00"
    })
    print(res.status_code, res.json())

    print("\n6. Getting Activities")
    res = session.get(f"{BASE_URL}/selfcare/get_activities")
    print(res.status_code, type(res.json()))

    print("\n7. Simulating Quiz Submission")
    # Quiz expects form data normally, simulating process_quiz_results indirectly via form POST
    res = session.post(f"{BASE_URL}/quiz/", data={
        "answers_Feeling nervous, anxious or on edge": "Anxiety:3",
         "answers_Not being able to stop or control worrying": "Anxiety:2"
    })
    print(res.status_code, "Quiz submitted")

    print("\n8. Checking Progress Tracker")
    res = session.get(f"{BASE_URL}/progress/")
    print(res.status_code, res.json())

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print("Script failed:", str(e))
