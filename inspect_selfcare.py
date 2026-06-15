from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
col = db["selfcare_suggestions"]

categories = col.distinct("category")
print(f"Categories: {categories}")

# Show all docs for first category
cat = categories[0] if categories else "Anxiety"
docs = list(col.find({"category": cat}, {"_id": 0}))
print(f"\nDocs for category '{cat}':")
for doc in docs:
    print(json.dumps(doc, indent=2, default=str))
