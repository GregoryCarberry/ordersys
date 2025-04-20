import sqlite3
import json
import os
from werkzeug.security import generate_password_hash

DB_FILENAME = 'users.db'

def init_db():
    create_db = False

    # If database file does not exist, obviously need to create it
    if not os.path.exists(DB_FILENAME):
        create_db = True
    else:
        # Connect and check if 'users' table exists
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='users';
        """)
        if cursor.fetchone() is None:
            create_db = True
        conn.close()

    if not create_db:
        print(f"Database '{DB_FILENAME}' already initialized with 'users' table. Skipping.")
        return

    print(f"Initializing database '{DB_FILENAME}'...")

    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            permissions TEXT DEFAULT '[]',
            can_grant_permissions INTEGER DEFAULT 0,
            store_id INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert root user
    root_password_hash = generate_password_hash('changeme123')
    cursor.execute('''
        INSERT INTO users (username, password_hash, role, permissions, can_grant_permissions, store_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'root',
        root_password_hash,
        'root',
        json.dumps(['*']),
        1,
        0
    ))

    conn.commit()
    conn.close()

    print("Database initialization complete.")

if __name__ == '__main__':
    init_db()
