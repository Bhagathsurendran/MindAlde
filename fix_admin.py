import hashlib
from pymongo import MongoClient

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

client = MongoClient('mongodb://localhost:27017/')
db = client['mental_health_db']

new_password = 'Admin@123'

# Fix the existing admin user: set correct role and reset password
result = db['users'].update_one(
    {'email': 'admin@gmail.com'},
    {'$set': {'role': 'admin', 'password': hash_pw(new_password), 'name': 'Admin'}}
)

print('Updated:', result.modified_count, 'document(s)')
user = db['users'].find_one({'email': 'admin@gmail.com'}, {'_id': 0, 'email': 1, 'role': 1, 'name': 1})
print('User now:', user)
print()
print('=== LOGIN CREDENTIALS ===')
print('Email   : admin@gmail.com')
print('Password: Admin@123')
