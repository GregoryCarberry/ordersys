from app.db import SessionLocal
from app.models.order import Order
import json

def seed_orders():
    db = SessionLocal()
    try:
        orders = [
            Order(
                store_id=1,
                items=json.dumps([
                    {"sku": "item001", "quantity": 2},
                    {"sku": "item002", "quantity": 5}
                ]),
                status="pending"
            ),
            Order(
                store_id=1,
                items=json.dumps([
                    {"sku": "item003", "quantity": 1},
                    {"sku": "item004", "quantity": 3},
                    {"sku": "item005", "quantity": 2}
                ]),
                status="fulfilled"
            ),
            Order(
                store_id=1,
                items=json.dumps([
                    {"sku": "item006", "quantity": 4}
                ]),
                status="approved"
            )
        ]
        db.add_all(orders)
        db.commit()
        print("[✔] Dummy orders with quantities seeded.")
    finally:
        db.close()

if __name__ == '__main__':
    seed_orders()
