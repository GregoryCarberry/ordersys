import sqlite3
import json
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
db = SQLAlchemy()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///users.db")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Calculate the correct absolute path
# DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db')

DB_PATH = "/app/users.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
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
