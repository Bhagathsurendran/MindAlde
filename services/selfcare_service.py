from database import reminders_collection
from datetime import datetime

def check_reminders():
    current_time = datetime.now()
    pending_reminders = reminders_collection.find({"status": "pending"})

    for reminder in pending_reminders:
        reminder_time = reminder["reminder_time"]
        if current_time >= reminder_time:
            print(f"🔔 Reminder for {reminder['user_id']}: {reminder['title']} is due!")
            reminders_collection.update_one(
                {"_id": reminder["_id"]},
                {"$set": {"status": "notified"}}
            )
