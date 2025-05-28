from .db import SessionLocal
from .models.order import Order
import json

def seed_orders():
    db = SessionLocal()
    try:
        orders = [
            Order(
                store_id=1,
                items=json.dumps([
                    {"sku": "SHMP-001", "quantity": 2},
                    {"sku": "CNDT-002", "quantity": 5}
                ]),
                status="pending"
            ),
            Order(
                store_id=1,
                items=json.dumps([
                    {"sku": "GEL-009", "quantity": 1},
                    {"sku": "MASK-005", "quantity": 3}
                ]),
                status="fulfilled"
            ),
            Order(
                store_id=1,
                items=json.dumps([
                    {"sku": "OIL-003", "quantity": 4}
                ]),
                status="approved"
            )
        ]

        db.add_all(orders)
        db.commit()
        print("[✔] Dummy orders seeded.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_orders()
