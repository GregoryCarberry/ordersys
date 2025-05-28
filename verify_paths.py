import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(base_dir, 'backend', 'ordersys.db')

print("Expected DB file path:", db_file)
print("Exists?", os.path.exists(db_file))
