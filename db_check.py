import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]

collections = db.list_collection_names()
schemas = {}

for coll_name in collections:
    doc = db[coll_name].find_one()
    if doc:
        schema = {k: type(v).__name__ for k, v in doc.items()}
        schemas[coll_name] = schema
    else:
        schemas[coll_name] = "Empty"

with open("db_schema.json", "w") as f:
    json.dump({"collections": collections, "schemas": schemas}, f, indent=4)
