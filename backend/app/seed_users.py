from .db import SessionLocal
from .models.user import User
from .models.permission import Permission
from .models.user_permission import UserPermission
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_users():
    db = SessionLocal()
    try:
        # Seed core permissions
        permissions_to_seed = [
            {"name": "grant_permissions", "description": "Can grant permissions to other users"},
            {"name": "manage_users", "description": "Can manage user accounts"},
            {"name": "manage_stock", "description": "Can manage stock levels"},
            {"name": "manage_orders", "description": "Can manage orders"},
            {"name": "root_access", "description": "Full system access"},
        ]

        for perm in permissions_to_seed:
            existing_perm = db.query(Permission).filter_by(name=perm["name"]).first()
            if not existing_perm:
                db.add(Permission(name=perm["name"], description=perm["description"]))
        db.commit()

        # Map of permission names to objects for easy reference
        permissions_map = {p.name: p for p in db.query(Permission).all()}

        # Seed users
        users_to_seed = [
            {
                "username": "root",
                "password": "changeme123",
                "role": "root",
                "store_id": 0,
                "permissions": ["root_access", "grant_permissions", "manage_users", "manage_stock", "manage_orders"]
            },
            {
                "username": "manager",
                "password": "password123",
                "role": "manager",
                "store_id": 1,
                "permissions": ["manage_stock", "manage_orders"]
            },
            {
                "username": "staff",
                "password": "password123",
                "role": "staff",
                "store_id": 1,
                "permissions": []
            },
            {
                "username": "warehouse",
                "password": "warehouse123",
                "role": "warehouse",
                "store_id": 0,
                "permissions": ["manage_stock"]
            }
        ]

        for user_data in users_to_seed:
            existing_user = db.query(User).filter_by(username=user_data["username"]).first()
            if not existing_user:
                new_user = User(
                    username=user_data["username"],
                    password_hash=generate_password_hash(user_data["password"]),
                    role=user_data["role"],
                    store_id=user_data["store_id"]
                )
                db.add(new_user)
                db.flush()  # Ensure new_user gets an ID

                # Add permissions
                for perm_name in user_data["permissions"]:
                    permission = permissions_map.get(perm_name)
                    if permission:
                        db.add(UserPermission(
                            user_id=new_user.id,
                            permission_id=permission.id,
                            valid_from=datetime.utcnow()
                        ))

        db.commit()
        print("[✔] Users and permissions seeded successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
