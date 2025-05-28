import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
db = SQLAlchemy()

# Get base project directory (~/ordersys)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Define DB path (~/ordersys/backend/ordersys.db)
DB_PATH = os.path.join(BASE_DIR, 'ordersys.db')

# SQLAlchemy database URL
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"🔍 DB_PATH used by SQLAlchemy: {DB_PATH}")
print(f"🔍 DATABASE_URL used by SQLAlchemy: {DATABASE_URL}")


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Optional: Raw sqlite3 connection (only if you *really* need it)
def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'backend', 'ordersys.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    return conn

def get_user_from_db(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash, role, permissions, can_grant_permissions, store_id FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'id': row['id'],
            'username': row['username'],
            'password_hash': row['password_hash'],
            'role': row['role'],
            'permissions': json.loads(row['permissions']) if row['permissions'] else [],
            'can_grant_permissions': bool(row['can_grant_permissions']),
            'store_id': row['store_id'],
        }
    return None

def save_permissions_to_db(username, permissions):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET permissions = ? WHERE username = ?", (json.dumps(permissions), username))
    conn.commit()
    conn.close()
