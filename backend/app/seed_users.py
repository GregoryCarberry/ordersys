import sqlite3
import json
import os
from werkzeug.security import generate_password_hash

# Absolute path to users.db inside container
DB_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db')
DB_FILENAME = os.path.abspath(DB_FILENAME)

def seed_users():
    if not os.path.exists(DB_FILENAME):
        print(f"[!] Database not found at {DB_FILENAME}. Run init_db.py first.")
        return

    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    users_to_seed = [
            {
                "username": "root",
                "password": "changeme123",
                "role": "root",
                "permissions": ["*"],
                "can_grant_permissions": 1,
                "store_id": 0
            },
            {
                "username": "manager",
                "password": "password123",
                "role": "manager",
                "permissions": [],
                "can_grant_permissions": 0,
                "store_id": 1
            },
            {
                "username": "staff",
                "password": "password123",
                "role": "staff",
                "permissions": [],
                "can_grant_permissions": 0,
                "store_id": 1
            },
            {
                "username": "warehouse",
                "password": "warehouse123",
                "role": "warehouse",
                "permissions": [],
                "can_grant_permissions": 0,
                "store_id": 0
            }
        ]


    for user in users_to_seed:
        password_hash = generate_password_hash(user["password"])
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password_hash, role, permissions, can_grant_permissions, store_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user["username"],
            password_hash,
            user["role"],
            json.dumps(user["permissions"]),
            user["can_grant_permissions"],
            user["store_id"]
        ))

    conn.commit()
    conn.close()
    print("[✔] Users seeded successfully.")

if __name__ == '__main__':
    seed_users()
