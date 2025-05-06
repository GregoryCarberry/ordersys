import os
import sqlite3
import shutil
from app.db import engine, Base
from app.models.store import Store
from app.models.order import Order
from app.models.product import Product

# Absolute path to users.db
DB_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db')
DB_FILENAME = os.path.abspath(DB_FILENAME)

def init_db():
    create_db = False

    if not os.path.exists(DB_FILENAME):
        create_db = True
    elif os.path.isdir(DB_FILENAME):
        print(f"[!] WARNING: '{DB_FILENAME}' is a folder, not a database file. Removing folder...")
        shutil.rmtree(DB_FILENAME)
        create_db = True
    else:
        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
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

        conn.commit()
        conn.close()
        print("[✔] Base users table created.")

    # Always ensure other SQLAlchemy tables are created
    Base.metadata.create_all(bind=engine)
    print("[✔] SQLAlchemy tables created.")

if __name__ == '__main__':
    init_db()
