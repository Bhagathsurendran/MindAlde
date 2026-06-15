from database import quiz_collection, assessments_collection, progress_collection
from datetime import datetime

def get_quiz_questions():
    """Fetch quiz questions from MongoDB"""
    return list(quiz_collection.find({}, {"_id": 0}))

def process_quiz_results(user_id, user_answers):
    scores = {"Stress": 0, "Depression": 0, "Anxiety": 0, "Normal": 0}
    total_score = 0

    for question in get_quiz_questions():
        question_text = question["question_text"]
        category = question["category"]

        selected_value = user_answers.get(f'answers_{question_text}')
        if selected_value and ":" in selected_value:
            try:
                score = selected_value.split(":")[-1]
                score_val = int(score)
            except (ValueError, IndexError):
                continue
            scores[category] += score_val  
            total_score += score_val

    final_category = max(scores, key=scores.get)  

    if user_id:
        assessment_doc = {
            "user_id": user_id,
            "date": datetime.utcnow(),
            "score": total_score,
            "category": final_category
        }
        result = assessments_collection.insert_one(assessment_doc)
        
        progress_collection.update_one(
            {"user_id": user_id},
            {"$push": {"assessments": result.inserted_id}},
            upsert=True
        )

    return final_category
