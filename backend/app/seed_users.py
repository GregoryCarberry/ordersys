from .db import SessionLocal
from .models.user import User
from werkzeug.security import generate_password_hash

def seed_users():
    db = SessionLocal()
    try:
        users_to_seed = [
            {
                "username": "root",
                "password": "changeme123",
                "role": "root",
                "can_grant_permissions": True,
                "store_id": 0
            },
            {
                "username": "manager",
                "password": "password123",
                "role": "manager",
                "can_grant_permissions": False,
                "store_id": 1
            },
            {
                "username": "staff",
                "password": "password123",
                "role": "staff",
                "can_grant_permissions": False,
                "store_id": 1
            },
            {
                "username": "warehouse",
                "password": "warehouse123",
                "role": "warehouse",
                "can_grant_permissions": False,
                "store_id": 0
            }
        ]

        for user_data in users_to_seed:
            exists = db.query(User).filter_by(username=user_data["username"]).first()
            if not exists:
                db.add(User(
                    username=user_data["username"],
                    password_hash=generate_password_hash(user_data["password"]),
                    role=user_data["role"],
                    can_grant_permissions=user_data["can_grant_permissions"],
                    store_id=user_data["store_id"]
                ))
        db.commit()
        print("[✔] Users seeded successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
