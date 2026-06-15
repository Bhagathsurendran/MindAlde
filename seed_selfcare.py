from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
col = db["selfcare_suggestions"]

count = col.count_documents({})
print(f"Current document count in selfcare_suggestions: {count}")

if count > 0:
    # Show a sample document to understand the current structure
    sample = col.find_one({}, {"_id": 0})
    print("Sample document:", sample)
else:
    print("Collection is empty. Seeding with default resources...")
    seed_data = [
        {
            "category": "Anxiety",
            "activities": [
                "Practice 4-7-8 breathing technique for 5 minutes",
                "Write down 3 things you are grateful for today",
                "Take a 10-minute walk outside in fresh air",
                "Try progressive muscle relaxation – tense and release each muscle group",
                "Ground yourself with the 5-4-3-2-1 sensory technique"
            ],
            "exercises": [
                "Do 10 minutes of gentle yoga or stretching",
                "Go for a brisk 20-minute walk",
                "Try jumping jacks or light aerobics for 5 minutes",
                "Practice Tai Chi or Qigong movements"
            ],
            "youtube_videos": [
                {"title": "Guided Breathing Exercise for Anxiety Relief", "url": "https://www.youtube.com/watch?v=acUZdGd_3Dg"},
                {"title": "10-Minute Meditation for Anxiety", "url": "https://www.youtube.com/watch?v=O-6f5wQXSu8"},
                {"title": "Progressive Muscle Relaxation", "url": "https://www.youtube.com/watch?v=ihO02wUzgkc"}
            ],
            "articles": [
                {"title": "How to Calm Anxiety: 17 Tips", "url": "https://www.healthline.com/health/how-to-stop-anxiety"},
                {"title": "Anxiety Management Strategies", "url": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety-and-panic-attacks/self-care/"}
            ],
            "books": [
                {"title": "The Anxiety and Worry Workbook – Clark & Beck", "url": "https://www.amazon.com/Anxiety-Worry-Workbook-Cognitive-Behavioral/dp/1606239597"}
            ]
        },
        {
            "category": "Depression",
            "activities": [
                "Schedule one enjoyable activity for today, no matter how small",
                "Write in a journal about your feelings with compassion",
                "Reach out to one friend or family member today",
                "Spend 15 minutes in sunlight or near a bright window",
                "Practice self-compassion meditation"
            ],
            "exercises": [
                "Take a 30-minute walk (even slow is fine)",
                "Do gentle stretching or yoga for 10 minutes",
                "Dance to one favorite song at home",
                "Try swimming or water aerobics"
            ],
            "youtube_videos": [
                {"title": "Understanding Depression – TED Talk", "url": "https://www.youtube.com/watch?v=-eBUcBfkVCo"},
                {"title": "Guided Meditation for Depression", "url": "https://www.youtube.com/watch?v=aq9zb0e2HGk"},
                {"title": "Yoga for Depression and Sadness", "url": "https://www.youtube.com/watch?v=0Ejd5K_gX34"}
            ],
            "articles": [
                {"title": "Self-Care for Depression: What You Can Do", "url": "https://www.healthline.com/health/depression/self-care"},
                {"title": "7 Ways to Fight Depression Without Medication", "url": "https://www.webmd.com/depression/features/natural-treatments"}
            ],
            "books": [
                {"title": "Feeling Good: The New Mood Therapy – David Burns", "url": "https://www.amazon.com/Feeling-Good-New-Mood-Therapy/dp/0380810336"}
            ]
        },
        {
            "category": "Stress",
            "activities": [
                "Take 5 slow deep breaths right now",
                "Write a to-do list to organize your thoughts",
                "Declutter one small area of your workspace",
                "Practice mindfulness for 5 minutes – just observe your thoughts",
                "Do a digital detox for 30 minutes – no screens"
            ],
            "exercises": [
                "Try a 15-minute HIIT routine",
                "Do 3 sets of 10 push-ups or modified push-ups",
                "Go cycling or jogging for 20 minutes",
                "Practice power yoga"
            ],
            "youtube_videos": [
                {"title": "5-Minute Stress Relief Meditation", "url": "https://www.youtube.com/watch?v=inpok4MKVLM"},
                {"title": "Quick Yoga for Stress Relief", "url": "https://www.youtube.com/watch?v=hJbRpHZr_d0"},
                {"title": "How Stress Affects Your Body – TED-Ed", "url": "https://www.youtube.com/watch?v=v-t1Z5-oPtU"}
            ],
            "articles": [
                {"title": "10 Relaxation Techniques That Zap Stress Fast", "url": "https://www.webmd.com/balance/guide/blissing-out-10-relaxation-techniques-reduce-stress-spot"},
                {"title": "Stress Management: How to Reduce and Relieve Stress", "url": "https://www.helpguide.org/articles/stress/stress-management.htm"}
            ],
            "books": [
                {"title": "Why Zebras Don't Get Ulcers – Robert Sapolsky", "url": "https://www.amazon.com/Why-Zebras-Dont-Ulcers-Third/dp/0805073698"}
            ]
        },
        {
            "category": "Normal",
            "activities": [
                "Practice daily gratitude – list 3 good things each morning",
                "Try a new hobby or creative activity this week",
                "Spend quality time with people you care about",
                "Set a personal goal and write your first step toward it",
                "Practice mindful eating during your next meal"
            ],
            "exercises": [
                "Maintain a consistent 30-minute daily walking habit",
                "Try a new workout class or sport",
                "Do morning stretches for 10 minutes",
                "Practice a sport you enjoy"
            ],
            "youtube_videos": [
                {"title": "Daily Mindfulness Practice – 10 Minutes", "url": "https://www.youtube.com/watch?v=ZToicYcHIOU"},
                {"title": "The Secret to Living Well – TED Talk", "url": "https://www.youtube.com/watch?v=uxjFjHFq3WY"},
                {"title": "How to Build Better Habits – James Clear", "url": "https://www.youtube.com/watch?v=YT7tQzmGRLA"}
            ],
            "articles": [
                {"title": "8 Pillars of Wellness to Live Your Best Life", "url": "https://www.verywellmind.com/pillars-of-wellness"},
                {"title": "Simple Daily Habits That Will Change Your Life", "url": "https://www.developgoodhabits.com/good-daily-habits-list/"}
            ],
            "books": [
                {"title": "Atomic Habits – James Clear", "url": "https://www.amazon.com/Atomic-Habits-Proven-Build-Break/dp/0735211299"}
            ]
        }
    ]
    col.insert_many(seed_data)
    print(f"Seeded {len(seed_data)} category documents successfully!")
    for d in seed_data:
        print(f"  - {d['category']}: {len(d['activities'])} activities, {len(d['exercises'])} exercises, {len(d['youtube_videos'])} videos")
