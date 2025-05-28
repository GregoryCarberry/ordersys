import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, 'backend', 'users.db')

print("Calculated DB path:", db_path)
