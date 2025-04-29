import sqlite3
import json
import os
import shutil
from werkzeug.security import generate_password_hash
from app.db import engine, Base
from app.models.store import Store
from app.models.order import Order

# Correct absolute path to database file
DB_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db')
DB_FILENAME = os.path.abspath(DB_FILENAME)

def init_db():
    create_db = False

    # Check if users.db exists
    if not os.path.exists(DB_FILENAME):
        create_db = True
    elif os.path.isdir(DB_FILENAME):
        print(f"[!] WARNING: '{DB_FILENAME}' is a folder, not a database file. Removing folder...")
        shutil.rmtree(DB_FILENAME)
        create_db = True
    else:
        # Connect and check if 'users' table exists
        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master WHERE type='table' AND name='users';
            """)
            if cursor.fetchone() is None:
                create_db = True
            conn.close()
        except sqlite3.Error as e:
            print(f"[!] SQLite error while checking database: {e}")
            create_db = True

    if create_db:
        print(f"[+] Initializing database '{DB_FILENAME}'...")

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

        print("[✔] Database initialization complete.")

    # 🔥 Finally create SQLAlchemy tables AFTER DB file exists
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
